#!/usr/bin/env python3
"""
MOTOR DE RIESGO — versión 1.0 (2026-10-05, sesión 20)
=====================================================

Capa de decisión SOBRE el modelo financiero de la sesión 19. NO es un segundo modelo financiero:
toda cifra económica sale de `21_modelo_financiero/modelo_financiero.py` (construir_entrada → simular →
resultados), que a su vez consume CAPEX (19), OPEX (20), balance de masa (04) y escala (23) sin copiarlos.

    CONFIGURACIÓN + ESCENARIO + RESTRICCIONES + SHOCKS  →  MOTOR FINANCIERO  →  RESULTADOS
                                                        →  RIESGO / SENSIBILIDAD / OPTIMIZACIÓN

Qué hace este archivo (el optimizador está en modelo_optimizador.py):
  * REGISTRO DE VARIABLES DE RIESGO: cada variable declara QUÉ campo de la entrada del motor toca, cómo
    (RELATIVO = × (1 + s); ABSOLUTO_DIAS / ABSOLUTO_MESES = + s), y su SOPORTE:
      SOPORTADA                   el motor tiene el campo; el shock lo modifica tal cual
      APROXIMACION                transformación declarada sobre campos existentes (SUP-20-04…06)
      REQUIERE_BASE               necesita un valor base declarado (mortalidad, condenas, FCR absoluto, FX)
      DISCRETA                    se evalúa como stress o como alternativa, no como shock continuo
      NO_SOPORTADA_POR_INTERFAZ   el motor no tiene el campo: se informa, no se simula (DPV-20-xx)
  * EVALUADOR con caché (misma alternativa + mismos shocks = misma corrida; base de cada alternativa
    construida una sola vez). La base nunca se modifica: cada shock trabaja sobre una copia profunda.
  * SENSIBILIDAD ONE-WAY, TORNADO, SENSIBILIDAD 2D, STRESS (multivariable), PUNTOS DE QUIEBRE (grilla +
    bisección), MONTE CARLO (distribuciones declaradas + cópula gaussiana con correlaciones declaradas).
  * REGISTRO y MATRIZ DE RIESGOS cualitativos (sin probabilidades inventadas; inherente ≠ residual).

Reglas que el código hace cumplir (tests en tests_riesgo_optimizador.py):
  * Los shocks solo existen en el universo ESCENARIO o en CASOS ARTIFICIALES; el universo EVIDENCIA no se
    perturba (un shock sobre evidencia la convertiría en simulación).
  * Un faltante del motor (None) nunca se vuelve 0: una métrica no publicable no entra a rankings.
  * Un shock relativo sobre una base 0 no tiene efecto y se informa (BASE_CERO_SIN_EFECTO).
  * Monte Carlo del proyecto exige distribuciones RESPALDADAS; si no, NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES.
  * Toda probabilidad de Monte Carlo es SIMULADA (PROBABILIDAD_SIMULADA_NO_HISTORICA).

Unidades: USD (moneda del motor), kg, días, meses, fracciones. CSV con punto decimal.
IDs provisionales: SUP-20-##, DPV-20-##, DEC-20-## (ver actualizaciones_gestion_20.md).
"""
import copy
import csv
import io
import json
import math
import os
import random
import re
import statistics
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
_FIN = os.path.join(RAIZ, "21_modelo_financiero")
if _FIN not in sys.path:
    sys.path.insert(0, _FIN)
with redirect_stdout(io.StringIO()):
    import modelo_financiero as mf      # noqa: E402  (21 → 20 → 19 → 04/23)

VERSION = "1.0"
FECHA = "2026-10-05"
TOL = 1e-9
_MUT: set = set()                       # mutaciones sembradas de esta capa (solo tests)

ETIQ_SIM = mf.ETIQUETA_SIM              # SIMULACION_HIPOTETICA_NO_VALIDADA
ETIQ_ART = "CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO"
OPT_REAL_ND = "OPTIMIZACION_REAL_NO_DISPONIBLE"
MC_ND = "NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES"
CORR_NM = "CORRELACIONES_NO_MODELADAS"
PROB_SIM = "PROBABILIDAD_SIMULADA_NO_HISTORICA"
# Tres tipos de probabilidad que NUNCA se confunden. Monte Carlo solo produce la primera.
TIPOS_PROBABILIDAD = ("PROBABILIDAD_SIMULADA", "PROBABILIDAD_HISTORICA", "PROBABILIDAD_DEL_PROYECTO")
SUP_INDEP = "SUPUESTO_INDEPENDENCIA_ESCENARIO"
MC_CORR_PEND = "NO_EJECUTADO_CORRELACION_PENDIENTE"
NO_CALC = "NO_CALCULABLE"
NO_ENC = "NO_ENCONTRADO_EN_RANGO"
UNIVERSOS = ("EVIDENCIA", "ESCENARIO", "ARTIFICIAL_TEST")

ARCH_INPUTS = os.path.join(AQUI, "inputs_riesgo_optimizacion.csv")
ARCH_STRESS = os.path.join(AQUI, "escenarios_stress.csv")
ARCH_DIST = os.path.join(AQUI, "distribuciones_riesgo.csv")
ARCH_CORR = os.path.join(AQUI, "correlaciones_riesgo.csv")
ARCH_REG_RIESGOS = os.path.join(AQUI, "registro_riesgos.csv")


class ErrorRiesgo(Exception):
    pass


class NoAplica(Exception):
    """La variable no existe en este escenario (p. ej. sin deuda no hay tasa de deuda)."""


class NoCalculable(Exception):
    """Falta un dato para aplicar el shock (p. ej. mortalidad base no declarada)."""


class ShockInvalido(Exception):
    """El shock lleva la variable fuera de su dominio físico o matemático (p. ej. precio ≤ 0)."""


# ---------------------------------------------------------------------------------------------
# 0. UTILIDADES
# ---------------------------------------------------------------------------------------------
def fmt(x, dec=6):
    if x is None:
        return ""
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return str(x)
        return f"{x:.{dec}f}".rstrip("0").rstrip(".") if abs(x) < 1e15 else f"{x:.6g}"
    if isinstance(x, (list, tuple, dict)):
        return json.dumps(x, ensure_ascii=False, default=str)
    return str(x)


def escribir(ruta, filas, campos):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction="raise", lineterminator="\n")
        w.writeheader()
        for f in filas:
            w.writerow({k: fmt(f.get(k)) for k in campos})


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    t = str(x).strip()
    return None if t == "" else float(t)


def percentil(xs, p):
    """Percentil con interpolación lineal entre estadísticos de orden (p en [0, 1])."""
    xs = sorted(xs)
    if not xs:
        return None
    if len(xs) == 1:
        return xs[0]
    h = (len(xs) - 1) * p
    lo = math.floor(h)
    hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (h - lo) * (xs[hi] - xs[lo])


def clave_shocks(shocks):
    return json.dumps(sorted((shocks or {}).items()), default=str)


# ---------------------------------------------------------------------------------------------
# 1. INPUTS DE LA CAPA (inputs_riesgo_optimizacion.csv)
# ---------------------------------------------------------------------------------------------
def _parse_valor(t):
    t = (t or "").strip()
    if t == "":
        return None
    if t in ("TRUE", "FALSE"):
        return t == "TRUE"
    if "|" in t:
        return [_parse_valor(x) for x in t.split("|")]
    try:
        return float(t) if any(c in t for c in ".eE") else int(t)
    except ValueError:
        return t


def leer_inputs(ruta=ARCH_INPUTS):
    """PARAMETRO → valor. Vacío = None (no se completa con un default empresarial)."""
    filas = leer_csv(ruta)
    ids = [f["ID_INPUT"] for f in filas]
    if len(ids) != len(set(ids)):
        raise ErrorRiesgo("ID_INPUT duplicado en inputs_riesgo_optimizacion.csv")
    out, meta = {}, {}
    for f in filas:
        p = f["PARAMETRO"]
        if p in out:
            raise ErrorRiesgo(f"parámetro duplicado {p}")
        out[p] = _parse_valor(f["VALOR"])
        meta[p] = f
    return out, meta


def como_lista(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


# ---------------------------------------------------------------------------------------------
# 2. CLASIFICACIÓN DE RUBROS DE OPEX (para shocks de costo por driver)
# ---------------------------------------------------------------------------------------------
# Por COSTO_ID del registro de 20_opex (prefijos documentados en matriz_validacion_opex.csv). Un rubro del usuario
# puede declarar "driver_riesgo" (texto o lista) y entonces manda esa declaración.
REGLAS_RUBRO = (
    ("maiz", (r"^ALI-MP-(DIF-)?MAIZ",)),
    ("soja", (r"^ALI-MP-(DIF-)?SOJA",)),
    ("alimento", (r"^ALI-A-PT", r"^ALI-B-", r"^ALI-MP-", r"^ALI-MERMA", r"^REP-ALI")),
    ("pollito", (r"^POL-", r"^INC-OP-HUEVO", r"^REP-AVE")),
    ("gas", (r"^PP-GAS", r"^UT-TER", r"^ALI-C-TER", r"^SUB-REN-TER")),
    ("electricidad", (r"^UT-ELE", r"^PP-ENE", r"^ALI-C-ENE", r"^INC-OP-ENE", r"^SUB-TRAT-ENE", r"^SUB-REN-ENE",
                      r"^REP-ENE", r"^energ[ií]a ")),
    ("agua", (r"^UT-AGUA", r"^PP-AGUA", r"^ALI-C-AGUA", r"^INC-OP-AGUA", r"^SUB-REN-AGUA", r"^REP-AGUA")),
    ("salarios", (r"^LAB-", r"^mano de obra")),
    ("packaging", (r"^EMP-", r"^INC-OP-INS")),
    ("mantenimiento", (r"^mantenimiento", r"^SUB-REN-MAN", r"^REP-MAN", r"^MAN-")),
    ("logistica", (r"^LOG-", r"^flete")),
    ("facon", (r"^FAE-FACON", r"^ALI-B-SRV")),
)
_REGLAS_C = [(t, [re.compile(p, re.I) for p in ps]) for t, ps in REGLAS_RUBRO]
GRUPO_A_DRIVER = {"alimento": "alimento", "granos": "alimento", "pollitos": "pollito", "packaging": "packaging",
                  "logistica": "logistica"}


def clasificar_rubro(r):
    dr = r.get("driver_riesgo")
    if dr:
        return set(como_lista(dr))
    nombre = str(r.get("rubro") or "")
    tags = {t for t, pats in _REGLAS_C if any(p.search(nombre) for p in pats)}
    if not tags and r.get("grupo_proveedor") in GRUPO_A_DRIVER:
        tags.add(GRUPO_A_DRIVER[r["grupo_proveedor"]])
    return tags


# ---------------------------------------------------------------------------------------------
# 3. TRANSFORMACIONES (actúan sobre la ENTRADA del motor; nunca sobre resultados)
# ---------------------------------------------------------------------------------------------
CORTES = {"pechuga", "pechuga_deshuesada", "pata_muslo", "pata_muslo_procesada", "alas"}
COPRODUCTOS_OTROS = {"carcasa_esqueleto", "cms", "recortes_piel"}


def _cat_precio(producto):
    """Grupo de precio de un producto (claves ITEMS del balance usadas por el motor)."""
    if producto == "pollo_entero":
        return "pollo_entero"
    if producto in CORTES:
        return "cortes"
    c = mf.CATEGORIA_PRODUCTO.get(producto)
    if c == "MENUDENCIAS":
        return "menudencias"
    if c == "PATAS_GARRAS":
        return "patas_garras"
    if c in ("SUBPRODUCTOS",) or producto in COPRODUCTOS_OTROS or producto == mf.PRODUCTO_RENDERING:
        return "subproductos"
    return "otros"


def _factor(s, minimo=0.0, estricto=True):
    f = 1.0 + s
    if (f <= minimo) if estricto else (f < minimo):
        raise ShockInvalido(f"factor {f:.4f} fuera de dominio")
    return f


def _t_precios(grupos):
    def t(P, s, ctx):
        f = _factor(s)
        cambios = []
        for k, spec in P["precios"].items():
            if grupos is not None and _cat_precio(k.split("|")[0]) not in grupos:
                continue
            if spec.get("tipo", "CONSTANTE") == "CONSTANTE":
                if spec.get("usd_kg") is None:
                    continue
                spec["usd_kg"] *= f
            else:
                spec["por_anio"] = {a: (None if v is None else v * f) for a, v in spec["por_anio"].items()}
            cambios.append(f"precios.{k}")
        if not cambios:
            raise NoAplica("el escenario no tiene precios de este grupo")
        return cambios
    return t


def _t_stress_mult(clave, minimo=0.0):
    def t(P, s, ctx):
        f = _factor(s, minimo)
        st = P["stress"]
        st[clave] = st.get(clave, 1.0) * f
        return [f"stress.{clave}"]
    return t


def _t_canal(campo, absoluto=False, minimo=0.0):
    def t(P, s, ctx):
        cambios = []
        for c, ch in (P.get("canales") or {}).items():
            if ch is None or ch.get(campo) is None:
                continue
            if absoluto:
                ch[campo] = max(minimo, ch[campo] + s)
                if ch[campo] == minimo and s < 0:
                    ctx["flags"].append(f"TOPE_{minimo:g}:{c}.{campo}")
            else:
                if ch[campo] == 0 and s != 0:
                    ctx["flags"].append(f"BASE_CERO_SIN_EFECTO:{c}.{campo}")
                ch[campo] = ch[campo] * _factor(s, 0.0, estricto=False)
            cambios.append(f"canales.{c}.{campo}")
        if not cambios:
            raise NoAplica(f"ningún canal con {campo}")
        return cambios
    return t


def _t_rampup(campo, tope=None):
    def t(P, s, ctx):
        f = _factor(s, 0.0, estricto=(campo != "merma"))
        cambios = []
        for i, e in enumerate(P["etapas"]):
            for r in e.get("rampup") or []:
                if r.get(campo) is None:
                    continue
                v = r[campo] * f
                if tope is not None and v > tope:
                    v = tope
                    ctx["flags"].append(f"TOPE_{tope:g}:{campo}")
                if r[campo] == 0 and s != 0:
                    ctx["flags"].append(f"BASE_CERO_SIN_EFECTO:{campo}")
                r[campo] = v
            if e.get("rampup"):
                cambios.append(f"etapas[{i}].rampup.{campo}")
        if not cambios:
            raise NoAplica(f"sin curva de ramp-up con {campo}")
        return sorted(set(cambios))
    return t


def _t_rubros(driver, campo="costo_pleno_usd_anio", absoluto=False):
    def t(P, s, ctx):
        cambios = []
        for i, e in enumerate(P["etapas"]):
            for r in e.get("opex_rubros") or []:
                if driver != "*" and driver not in clasificar_rubro(r):
                    continue
                if campo == "dias_pago" and not r.get("es_compra"):
                    continue
                if r.get(campo) is None:
                    continue
                if absoluto:
                    r[campo] = max(0.0, r[campo] + s)
                else:
                    r[campo] = r[campo] * _factor(s, 0.0, estricto=False)
                cambios.append(f"etapas[{i}].opex_rubros.{r['rubro']}.{campo}")
        if not cambios:
            raise NoAplica(f"ningún rubro de OPEX clasificado como '{driver}'")
        return cambios
    return t


def _t_peso_vivo(P, s, ctx):
    """APROXIMACIÓN (SUP-20-04): kg comerciales por ave ∝ peso vivo y alimento ∝ peso vivo (FCR constante).
    El balance 04 solo publica 2,9 kg: la linealidad no está verificada."""
    f = _factor(s)
    if not P.get("productos"):
        raise NoCalculable("sin productos por ave")
    for p in P["productos"].values():
        if p.get("kg_ave") is not None:
            p["kg_ave"] *= f
    for k in ("peso_vivo", "agua_incorporada"):
        if k in (P.get("meta_productos") or {}):
            P["meta_productos"][k] *= f
    cambios = ["productos.*.kg_ave", "meta_productos.peso_vivo"]
    try:
        cambios += _t_rubros("alimento")(P, s, ctx)
    except NoAplica:
        ctx["flags"].append("SIN_RUBRO_ALIMENTO: solo cambian los kg vendibles")
    return cambios


def _t_rendimiento(P, s, ctx):
    """APROXIMACIÓN (SUP-20-05): más rendimiento comestible = más kg de productos comestibles; la masa agregada
    sale de subproductos (la masa total por ave no cambia). Si no alcanza la masa → ShockInvalido."""
    f = _factor(s)
    prods = P.get("productos")
    if not prods:
        raise NoCalculable("sin productos por ave")
    com = [k for k, p in prods.items() if p.get("kg_ave") and p["categoria_ingreso"] not in ("SUBPRODUCTOS", "RENDERING")]
    sub = [k for k, p in prods.items() if p.get("kg_ave") and p["categoria_ingreso"] == "SUBPRODUCTOS"]
    delta = sum(prods[k]["kg_ave"] for k in com) * (f - 1)
    for k in com:
        prods[k]["kg_ave"] *= f
    disp = sum(prods[k]["kg_ave"] for k in sub)
    if delta > disp + 1e-12:
        raise ShockInvalido("rendimiento comestible supera la masa disponible del ave")
    for k in sub:
        prods[k]["kg_ave"] -= delta * (prods[k]["kg_ave"] / disp) if disp else 0.0
    return ["productos.*.kg_ave"]


def _t_condenas(P, s, ctx):
    c0 = ctx["base"].get("condenas")
    if c0 is None:
        raise NoCalculable("tasa de condenas base no declarada (base.condenas)")
    c1 = c0 * _factor(s, 0.0, estricto=False)
    if c1 >= 1:
        raise ShockInvalido("condenas ≥ 100 %")
    f = (1 - c1) / (1 - c0)
    for p in (P.get("productos") or {}).values():
        if p.get("kg_ave") and p["categoria_ingreso"] not in ("SUBPRODUCTOS", "RENDERING"):
            p["kg_ave"] *= f
    return ["productos.*.kg_ave"]


def _t_mortalidad(P, s, ctx):
    m0 = ctx["base"].get("mortalidad")
    if m0 is None:
        raise NoCalculable("mortalidad base no declarada (base.mortalidad)")
    m1 = m0 * _factor(s, 0.0, estricto=False)
    if m1 >= 1:
        raise ShockInvalido("mortalidad ≥ 100 %")
    st = P["stress"]
    if st.get("mortalidad"):
        raise ErrorRiesgo("mortalidad ya estresada en la base: no se componen dos shocks de mortalidad")
    st["mortalidad"] = {"base": m0, "nueva": m1}
    return ["stress.mortalidad"]


def _t_fx(P, s, ctx):
    tr = ctx["base"].get("traslado_fx")
    if tr is None:
        raise NoCalculable("traslado de la devaluación a precios en ARS no declarado (base.traslado_fx)")
    expuesto = any((v or {}).get("moneda_original") == "ARS" for v in P["precios"].values()) or any(
        r.get("moneda_original") == "ARS" for e in P["etapas"] for r in (e.get("opex_rubros") or []))
    if not expuesto:
        raise NoAplica("sin ítems con moneda_original = ARS: exposición cambiaria no declarada (DPV-20-04)")
    if s <= -1:
        raise ShockInvalido("devaluación ≤ −100 %")
    st = P["stress"]
    st["devaluacion"] = {"pct": s, "traslado_precios_ars": tr}
    return ["stress.devaluacion"]


def _t_campo(path, minimo=-1.0):
    def t(P, s, ctx):
        v = mf._get_path(P, path)
        if v is None:
            raise NoCalculable(f"{path} no definido en la base")
        nv = v * _factor(s, 0.0, estricto=False)
        if nv <= minimo:
            raise ShockInvalido(f"{path} fuera de dominio")
        mf._set_path(P, path, nv)
        return [path]
    return t


def _t_deuda(campo):
    def t(P, s, ctx):
        ds = (P.get("financiamiento") or {}).get("deudas") or []
        if not ds:
            raise NoAplica("sin deuda en la estructura")
        for d in ds:
            if campo == "tasa":
                d["tasa"] = d["tasa"] * _factor(s, 0.0, estricto=False)
            else:
                f = d["frecuencia_meses"]
                nuevo = d["plazo_meses"] + int(round(s / f)) * f
                if nuevo <= d.get("gracia_meses", 0):
                    raise ShockInvalido("plazo ≤ gracia")
                d["plazo_meses"] = nuevo
        return [f"financiamiento.deudas.{campo}"]
    return t


BLOQUES_CAPEX = {"equipos": ("PROCESO", "EQUIPOS"), "obra": ("OBRA_CIVIL", "OBRA"), "frio": ("FRIO",),
                 "efluentes": ("EFLUENTES",), "terreno": ("TERRENO",), "instalacion": ("INSTALACION",),
                 "importacion": ("IMPORTACION",), "contingencia": ("CONTINGENCIA",)}


def _t_capex_bloque(nombre):
    pref = BLOQUES_CAPEX[nombre]

    def t(P, s, ctx):
        f = _factor(s, 0.0, estricto=False)
        cambios = []
        for i, e in enumerate(P["etapas"]):
            if e.get("activos") is None:
                raise NoCalculable("CAPEX sin desglose por clase de activo (activos PENDIENTES, DPV-167)")
            delta = 0.0
            for a in e["activos"]:
                if str(a.get("clase", "")).upper().startswith(pref) and a.get("capex_usd") is not None:
                    d_ = a["capex_usd"] * (f - 1)
                    a["capex_usd"] += d_
                    if a.get("costo_reemplazo_usd") is not None:
                        a["costo_reemplazo_usd"] *= f
                    delta += d_
                    cambios.append(f"etapas[{i}].activos.{a['clase']}")
            if delta and e.get("capex_usd") is not None:
                e["capex_usd"] += delta
                cambios.append(f"etapas[{i}].capex_usd")
        if not cambios:
            raise NoAplica(f"ningún activo de la clase {pref}")
        return cambios
    return t


def _no_soportada(motivo):
    def t(P, s, ctx):
        raise NoAplica("NO_SOPORTADA_POR_INTERFAZ: " + motivo)
    return t


# ---------------------------------------------------------------------------------------------
# 4. REGISTRO DE VARIABLES
# ---------------------------------------------------------------------------------------------
# (id, categoría, descripción, tipo_shock, soporte, transformación, campo del motor, bloque del motor, DPV,
#  monotonía esperada del VAN (+1 crece con s, −1 decrece, None = no monótona/no aplica), rango de quiebre)
R_ = "RELATIVO"
D_ = "ABSOLUTO_DIAS"
M_ = "ABSOLUTO_MESES"
VARIABLES = {}


def _var(vid, cat, desc, tipo, soporte, fn, campo, bloque, dpv="", mono=None, rango=(-0.95, 3.0), nota=""):
    VARIABLES[vid] = {"ID": vid, "CATEGORIA": cat, "DESCRIPCION": desc, "TIPO_SHOCK": tipo, "SOPORTE": soporte,
                      "aplicar": fn, "CAMPO_MOTOR": campo, "BLOQUE_MOTOR": bloque, "DPV": dpv, "MONOTONIA_VAN": mono,
                      "RANGO_QUIEBRE": rango, "NOTA": nota}


# COMERCIALES
_var("precio_venta", "COMERCIAL", "Todos los precios de venta", R_, "SOPORTADA", _t_precios(None), "precios.*", "PRECIOS",
     "DPV-013, DPV-039, DPV-070", +1, (-0.95, 3.0))
_var("precio_pollo_entero", "COMERCIAL", "Precio del pollo entero", R_, "SOPORTADA", _t_precios({"pollo_entero"}),
     "precios.pollo_entero|*", "PRECIOS", "DPV-013", +1)
_var("precio_cortes", "COMERCIAL", "Precios de cortes (pechuga, pata-muslo, alas)", R_, "SOPORTADA", _t_precios({"cortes"}),
     "precios.<corte>|*", "PRECIOS", "DPV-013", +1)
_var("precio_menudencias", "COMERCIAL", "Precios de menudencias", R_, "SOPORTADA", _t_precios({"menudencias"}),
     "precios.<menudencia>|*", "PRECIOS", "DPV-013", +1)
_var("precio_patas_garras", "COMERCIAL", "Precio de patas / garras", R_, "SOPORTADA", _t_precios({"patas_garras"}),
     "precios.garras|*", "PRECIOS", "DPV-013, DPV-026", +1)
_var("precio_subproductos", "COMERCIAL", "Precios de subproductos y coproductos (C, carcasa, CMS, piel, rendering)", R_,
     "SOPORTADA", _t_precios({"subproductos"}), "precios.<subproducto>|*", "PRECIOS", "DEC-027", +1)
_var("demanda", "COMERCIAL", "Volumen demandado (todas las líneas)", R_, "SOPORTADA", _t_stress_mult("demanda", 0.0),
     "stress.demanda", "DEMANDA", "DPV-002, DPV-020, DPV-037, DPV-040", None,
     nota="Monótona solo si la planta no está limitada por capacidad (más demanda que capacidad no vende más)")
_var("mix", "COMERCIAL", "Mix de productos", "DISCRETO", "DISCRETA", _no_soportada("el mix se evalúa con líneas de demanda "
     "alternativas declaradas por el usuario (stress o alternativa), no con un shock continuo"), "demanda[].producto",
     "DEMANDA", "DPV-037")
_var("dias_cobro", "COMERCIAL", "Plazo de cobro (todos los canales)", D_, "SOPORTADA", _t_canal("dias_cobro", True),
     "canales.*.dias_cobro", "CT", "DPV-039, DPV-175", -1, (-365.0, 365.0))
_var("descuentos", "COMERCIAL", "Descuentos en factura (todos los canales)", R_, "SOPORTADA", _t_canal("pct_descuentos"),
     "canales.*.pct_descuentos", "CANALES", "DPV-039", -1)
_var("devoluciones", "COMERCIAL", "Devoluciones (todos los canales)", R_, "SOPORTADA", _t_canal("pct_devoluciones"),
     "canales.*.pct_devoluciones", "CANALES", "DPV-039", -1)
_var("canal", "COMERCIAL", "Reparto por canal", "DISCRETO", "DISCRETA", _no_soportada("el reparto por canal se evalúa "
     "como alternativa de demanda declarada (stress), no como shock continuo"), "demanda[].canal", "DEMANDA", "DPV-039")
# OPERATIVAS
_var("utilizacion", "OPERATIVA", "Utilización técnica (curva de ramp-up; tope 100 %)", R_, "SOPORTADA",
     _t_rampup("utilizacion", 1.0), "etapas[].rampup.utilizacion", "RAMPUP", "DEC-090", +1, (-0.95, 0.0),
     nota="Si la demanda limita las ventas, más utilización técnica no cambia nada")
_var("peso_vivo", "OPERATIVA", "Peso vivo de faena", R_, "APROXIMACION", _t_peso_vivo, "productos.*.kg_ave + rubros alimento",
     "PRODUCCION", "DPV-060", None, (-0.5, 0.5), nota="SUP-20-04: linealidad no verificada")
_var("mortalidad", "OPERATIVA", "Mortalidad en granja", R_, "REQUIERE_BASE", _t_mortalidad, "stress.mortalidad", "OPEX",
     "DPV-019", -1, (0.0, 20.0), nota="Semántica del motor: solo encarece el pollito por ave faenada")
_var("fcr", "OPERATIVA", "Conversión alimenticia (FCR)", R_, "APROXIMACION", _t_rubros("alimento"),
     "rubros alimento × FCR/FCR_base", "OPEX", "DPV-019", -1, (-0.5, 5.0),
     nota="SUP-20-05: costo de alimento ∝ FCR a precio y peso constantes")
_var("rendimiento_faena", "OPERATIVA", "Rendimiento comestible de faena", R_, "APROXIMACION", _t_rendimiento,
     "productos.*.kg_ave", "PRODUCCION", "DPV-060", +1, (-0.5, 0.3), nota="SUP-20-06: masa adicional sale de subproductos")
_var("condenas", "OPERATIVA", "Condenas / decomisos", R_, "REQUIERE_BASE", _t_condenas, "productos.*.kg_ave", "PRODUCCION",
     "DPV-060", -1, (0.0, 20.0))
_var("merma", "OPERATIVA", "Merma del ramp-up", R_, "SOPORTADA", _t_rampup("merma", 1.0), "etapas[].rampup.merma", "RAMPUP",
     "DEC-090", -1)
_var("eficiencia_linea", "OPERATIVA", "Eficiencia de línea (variables ÷ eficiencia)", R_, "SOPORTADA",
     _t_rampup("eficiencia"), "etapas[].rampup.eficiencia", "RAMPUP", "DEC-090, DPV-097", +1, (-0.9, 0.5))
_var("dias_operativos", "OPERATIVA", "Días operativos por año", "DISCRETO", "NO_SOPORTADA_POR_INTERFAZ",
     _no_soportada("cambiar días sin recalcular OPEX rompe la coherencia costo/capacidad; se evalúa con la variante "
                   "C1-6dias del mapa (DPV-20-01)"), "etapas[].dias_operativos_anio", "PRODUCCION", "DEC-033")
_var("rampup", "OPERATIVA", "Velocidad del ramp-up (factor de estiramiento)", R_, "SOPORTADA",
     _t_stress_mult("rampup_lento_factor", 0.0), "stress.rampup_lento_factor", "RAMPUP", "DEC-090", -1, (-0.9, 5.0))
# COSTOS
for _d, _desc, _dpv in (("alimento", "Alimento balanceado (todo el costo de alimento)", "DPV-050, DPV-155, DPV-157"),
                        ("maiz", "Maíz (solo planta de alimento propia o façon B1)", "DPV-157"),
                        ("soja", "Harina / expeller de soja", "DPV-157"),
                        ("pollito", "Pollito BB / huevo fértil", "DPV-006, DPV-047"),
                        ("gas", "Gas / combustible térmico", "DPV-052, DEC-045"),
                        ("electricidad", "Energía eléctrica", "DPV-052, DPV-095"),
                        ("agua", "Agua", "DPV-053"),
                        ("salarios", "Salarios y cargas", "DPV-148, DPV-146"),
                        ("packaging", "Packaging", "DPV-172"),
                        ("mantenimiento", "Mantenimiento", "DEC-088, DPV-150"),
                        ("logistica", "Logística (flete y flota)", "DPV-042, DPV-054, DPV-084"),
                        ("facon", "Tarifas de façon (faena / alimento)", "DPV-006, DPV-155")):
    _var(_d, "COSTO", _desc, R_, "SOPORTADA", _t_rubros(_d), f"etapas[].opex_rubros[{_d}].costo_pleno_usd_anio", "OPEX",
         _dpv, -1)
_var("opex_total", "COSTO", "Todo el OPEX (stress nativo del motor)", R_, "SOPORTADA", _t_stress_mult("opex", 0.0), "stress.opex",
     "OPEX", "", -1)
# INVERSIÓN
_var("capex", "INVERSION", "CAPEX total (desembolsos, activos y reposiciones; incluye sobrecostos y contingencia global)",
     R_, "SOPORTADA", _t_stress_mult("capex", 0.0), "stress.capex", "CAPEX", "DPV-097, DPV-086, DPV-167", -1, (-0.95, 10.0))
for _b in ("equipos", "obra", "frio", "efluentes", "terreno", "instalacion", "importacion", "contingencia"):
    _var(f"capex_{_b}", "INVERSION", f"CAPEX del bloque {_b}", R_, "SOPORTADA", _t_capex_bloque(_b),
         f"etapas[].activos[clase {'/'.join(BLOQUES_CAPEX[_b])}]", "CAPEX", "DPV-167", -1, (-0.95, 10.0),
         nota="Requiere activos con clase; hoy los activos del BOQ no tienen vida útil (DPV-167)")
# FINANCIERAS
_var("fx", "FINANCIERA", "Devaluación del ARS (solo ítems con moneda_original ARS)", R_, "REQUIERE_BASE", _t_fx,
     "stress.devaluacion", "PRECIOS", "DPV-20-04", None, (-0.5, 3.0))
_var("tasa_descuento", "FINANCIERA", "Tasa de descuento (anual efectiva)", R_, "SOPORTADA", _t_campo("tasa_descuento"),
     "tasa_descuento", "DESCUENTO", "DEC-007, DPV-001", -1, (-0.99, 20.0))
_var("tasa_deuda", "FINANCIERA", "Tasa de la deuda", R_, "SOPORTADA", _t_deuda("tasa"), "financiamiento.deudas[].tasa",
     "FINANCIAMIENTO", "DEC-092", None, (-0.99, 20.0), nota="No cambia el VAN del proyecto (FCFF): usar VAN_ACCIONISTA o DSCR")
_var("plazo_deuda", "FINANCIERA", "Plazo de la deuda", M_, "SOPORTADA", _t_deuda("plazo"), "financiamiento.deudas[].plazo_meses",
     "FINANCIAMIENTO", "DEC-092", None, (-120.0, 120.0))
_var("dias_pago", "FINANCIERA", "Días de pago a proveedores", D_, "SOPORTADA", _t_rubros("*", "dias_pago", True),
     "etapas[].opex_rubros[].dias_pago", "CT", "DPV-175", +1, (-365.0, 365.0))
_var("tasa_ganancias", "FINANCIERA", "Alícuota de ganancias", R_, "SOPORTADA", _t_campo("impuestos.tasa_ganancias"),
     "impuestos.tasa_ganancias", "GANANCIAS", "DPV-169", -1)
_var("iibb", "FINANCIERA", "Ingresos brutos", R_, "SOPORTADA", _t_campo("impuestos.pct_iibb"), "impuestos.pct_iibb",
     "IMPUESTOS_INGRESOS", "DPV-043", -1)
_var("recuperacion_iva", "FINANCIERA", "Plazo de recupero del IVA", "DISCRETO", "NO_SOPORTADA_POR_INTERFAZ",
     _no_soportada("el IVA SIMPLIFICADO del motor arrastra saldo técnico sin plazo de recupero parametrizable (DPV-20-02)"),
     "iva", "IVA", "DPV-169")
# ESTRATÉGICAS (discretas: stress o alternativa / gate físico)
for _v, _desc, _dpv, _camp in (
        ("exportacion_disponible", "Exportación disponible / cerrada", "DPV-015, DPV-024", "stress.corte_exportacion_desde_mes"),
        ("halal", "Certificación halal", "DPV-101", "variante C1-HALAL"),
        ("integrados_disponibles", "Disponibilidad de productores integrados", "DPV-048", "gate PRODUCCION_PRIMARIA"),
        ("proveedor_alimento", "Proveedor de alimento disponible", "DPV-050, DPV-155", "gate ALIMENTO"),
        ("faena_tercerizada", "Capacidad de faena a façon disponible", "DPV-006", "gate FACON_FAENA"),
        ("financiamiento", "Financiamiento disponible", "DEC-092, DPV-001", "restricción CAPITAL / DEUDA"),
        ("terreno_utilities", "Terreno, potencia y agua disponibles", "DPV-087, DPV-095, DPV-053", "gates TERRENO/AGUA/POTENCIA")):
    _var(_v, "ESTRATEGICA", _desc, "DISCRETO", "DISCRETA", _no_soportada(f"variable discreta: se evalúa vía {_camp}"),
         _camp, "ESTRATEGICA", _dpv)


def aplicar_shocks(P0, shocks, base=None, universo="ESCENARIO"):
    """Devuelve (P_nuevo, info). P0 NO se modifica. shocks = {variable: valor del shock (en la unidad de su tipo)}.
    info = {"cambios": {var: [paths]}, "flags": [...], "estado": OK | NO_APLICA | NO_CALCULABLE | SHOCK_INVALIDO}."""
    if shocks and universo == "EVIDENCIA":
        raise ErrorRiesgo("el universo EVIDENCIA no admite shocks: perturbar la evidencia la convierte en simulación")
    P = copy.deepcopy(P0)
    if P.get("stress") is None:
        P["stress"] = {}
    ctx = {"base": base or {}, "flags": []}
    info = {"cambios": {}, "flags": ctx["flags"], "estado": "OK", "motivo": ""}
    for var, s in sorted((shocks or {}).items()):
        if var not in VARIABLES:
            raise ErrorRiesgo(f"variable de riesgo desconocida {var}")
        if s is None:
            raise ErrorRiesgo(f"shock de {var} sin valor (un faltante no es 0)")
        if s == 0 and "R09" not in _MUT:
            info["cambios"][var] = []
            continue
        try:
            info["cambios"][var] = VARIABLES[var]["aplicar"](P, s, ctx)
            if "R09" in _MUT and var != "precio_venta" and P["precios"]:
                _t_precios(None)(P, 0.01, ctx)                     # mutación: el shock se filtra a otra variable
        except NoAplica as e:
            info.update(estado="NO_APLICA", motivo=f"{var}: {e}")
            return None, info
        except NoCalculable as e:
            info.update(estado=NO_CALC, motivo=f"{var}: {e}")
            return None, info
        except ShockInvalido as e:
            info.update(estado="SHOCK_INVALIDO", motivo=f"{var}: {e}")
            return None, info
    return P, info


# ---------------------------------------------------------------------------------------------
# 5. EVALUADOR (motor financiero como función de evaluación; caché reproducible)
# ---------------------------------------------------------------------------------------------
METRICAS = ("INGRESOS", "EBITDA", "MARGEN_EBITDA", "FCFF_TOTAL", "CAPEX", "FONDOS_INICIALES", "PICO_FONDOS", "VAN", "TIR",
            "PAYBACK", "PAYBACK_DESCONTADO", "BREAK_EVEN_U", "DSCR", "UTILIZACION", "CT_MAX", "VAN_ACCIONISTA",
            "CAJA_MINIMA", "DEUDA", "CAPACIDAD_FINAL_AVES_DIA", "DEMANDA_ASEGURADA_PCT", "KG_VENDIDOS_ULT",
            "CAPACIDAD_KG_DIA")
ALIAS_METRICA = {"PAYBACK_ANIOS": "PAYBACK", "PICO": "PICO_FONDOS", "DSCR_MIN": "DSCR"}
STATUS_QUO = "NO_INVERTIR_AUN"


def metricas(res, R):
    """Métricas de decisión leídas de resultados() del motor (None = no publicable; jamás 0 por defecto)."""
    g = res.get
    m = {"INGRESOS": g("INGRESO_NETO_ULTIMO_ANIO"), "EBITDA": g("EBITDA_ULTIMO_ANIO"),
         "MARGEN_EBITDA": g("MARGEN_EBITDA_ULTIMO_ANIO"), "FONDOS_INICIALES": g("FONDOS_INICIALES"),
         "PICO_FONDOS": g("PICO_REQUERIMIENTO_FONDOS"), "VAN": g("VAN"), "TIR": g("TIR"),
         "PAYBACK": g("PAYBACK_SIMPLE_ANIOS"), "PAYBACK_DESCONTADO": g("PAYBACK_DESCONTADO_ANIOS"),
         "BREAK_EVEN_U": g("BE_UTILIZACION_EBITDA"), "DSCR": g("DSCR_MINIMO"), "UTILIZACION": g("U_EFECTIVA_ULTIMO_ANIO"),
         "CT_MAX": g("CT_MAXIMO") if g("PUBLICABLE_FLUJO") else None, "VAN_ACCIONISTA": g("VAN_ACCIONISTA"),
         "CAJA_MINIMA": g("CAJA_MINIMA_LEDGER") if g("PUBLICABLE_FLUJO_ACCIONISTA") else None,
         "DEUDA": g("DEUDA_TOMADA") if g("PUBLICABLE_FLUJO_ACCIONISTA") else None,
         "TIR_ESTADO": g("TIR_ESTADO"), "PAYBACK_ESTADO": g("PAYBACK_SIMPLE_ESTADO")}
    if "R07" in _MUT and m["FONDOS_INICIALES"] is not None:                       # mutación: ignora el CAPEX
        m["FONDOS_INICIALES"] -= res.get("CAPEX_INICIAL") or 0.0
        m["PICO_FONDOS"] = max(0.0, (m["PICO_FONDOS"] or 0.0) - (res.get("CAPEX_INICIAL") or 0.0))
    if "R08" in _MUT and m["FONDOS_INICIALES"] is not None:                       # mutación: ignora el CT
        m["FONDOS_INICIALES"] -= res.get("CT_INICIAL") or 0.0
        m["PICO_FONDOS"] = res.get("CAPEX_INICIAL")
    capex = None
    if res.get("CAPEX_INICIAL") is not None:
        capex = res["CAPEX_INICIAL"] + (res.get("CAPEX_EXPANSION") or 0.0)
    m["CAPEX"] = capex
    S = (R or {}).get("series") or {}
    N = (R or {}).get("N") or 0
    base = "fcff" if res.get("BASE_FLUJO") == "AFTER_TAX" else "fcff_pre"
    m["FCFF_TOTAL"] = sum(S[base]) if (N and res.get("PUBLICABLE_FLUJO") and S.get(base) is not None) else None
    m["CAPACIDAD_FINAL_AVES_DIA"] = m["DEMANDA_ASEGURADA_PCT"] = m["KG_VENDIDOS_ULT"] = m["CAPACIDAD_KG_DIA"] = None
    if N and S.get("capacidad_aves") is not None:
        P = R["P"]
        ent = R.get("entrada_etapas") or []
        esc = [e["escala_aves_dia"] for i, e in enumerate(P["etapas"]) if i < len(ent) and ent[i] is not None and ent[i] <= N]
        m["CAPACIDAD_FINAL_AVES_DIA"] = float(max(esc)) if esc else 0.0
        k0 = N - 11
        cap = sum(S["capacidad_aves"][k0:N + 1])
        m["DEMANDA_ASEGURADA_PCT"] = sum(S["aves_requeridas_aseguradas"][k0:N + 1]) / cap if cap else None
        m["KG_VENDIDOS_ULT"] = sum(S["kg_vendidos"][k0:N + 1])
        kg_ave = sum(p["kg_ave"] for p in (P.get("productos") or {}).values() if p.get("kg_ave"))
        m["CAPACIDAD_KG_DIA"] = S["capacidad_aves"][N] * 12 / mf.DIAS_ANIO * kg_ave
    return m


def metricas_status_quo():
    """NO_INVERTIR_AUN es una ALTERNATIVA DE DECISIÓN (status quo), no un proyecto productivo: no tiene VAN, TIR, payback,
    CAPEX ni EBITDA propios. No se le asignan ceros (que la harían "ganar" MIN_CAPEX o MIN_PAYBACK por ausencia de
    inversión) ni TIR infinita. Gana solo por las reglas explícitas de decisión del optimizador (REGLAS_STATUS_QUO)."""
    m = {k: None for k in METRICAS}
    if "R24" in _MUT:                                             # mutación: se la trata como proyecto con ceros
        m.update(VAN=0.0, CAPEX=0.0, FONDOS_INICIALES=0.0, PICO_FONDOS=0.0, EBITDA=0.0, PAYBACK=0.0)
    m.update(TIR_ESTADO="NO_APLICA_STATUS_QUO", PAYBACK_ESTADO="NO_APLICA_STATUS_QUO")
    return m


def alternativa_status_quo(universo):
    return {"id": STATUS_QUO, "tipo": STATUS_QUO, "universo": universo, "configuracion": STATUS_QUO, "variante": "—",
            "escalas": (), "trayectoria": "—", "construir": None, "base_valores": {}, "fisico": None,
            "descripcion": "No ejecutar inversión todavía: mantener operación actual, pilotear / validar demanda, "
                           "esperar información. Alternativa de decisión, no proyecto productivo: sin métricas financieras."}


TIR_OMITIDA = mf.TIR_NO_CALCULADA      # evaluación rápida: la TIR no se pidió (≠ 0, ≠ faltante de datos)


class Evaluador:
    """Evalúa (alternativa, shocks) con el motor financiero. Caché por (alternativa, universo, shocks, modo).
    Modo RÁPIDO (tir=False): mf.resultados(R, calcular_tir=False) — interfaz explícita del motor (sesión 20); no se
    reemplaza ninguna función global, así que evaluadores concurrentes o una excepción no se afectan entre sí.
    Cada modo tiene su propia entrada de caché (un pedido rápido nunca devuelve una TIR no solicitada)."""

    def __init__(self, guardar_R=False):
        self.cache, self.bases = {}, {}
        self.n_eval = self.n_hit = 0
        self.guardar_R = guardar_R

    def base(self, alt):
        if alt["id"] not in self.bases:
            try:
                with redirect_stdout(io.StringIO()):
                    self.bases[alt["id"]] = alt["construir"]()
            except (mf.ErrorFinanciero, mf.mcx.ErrorCapex, mf.mo.ErrorOpex) as e:
                self.bases[alt["id"]] = ("ERROR", str(e))
        return self.bases[alt["id"]]

    def evaluar(self, alt, shocks=None, tir=False):
        key = (alt["id"], alt["universo"], clave_shocks(shocks), bool(tir))
        if key in self.cache and "R11" not in _MUT:
            self.n_hit += 1
            return self.cache[key]
        self.n_eval += 1
        out = {"alt": alt["id"], "shocks": dict(shocks or {}), "estado": "OK", "motivo": "", "flags": [], "res": {},
               "met": {k: None for k in METRICAS}, "cambios": {}}
        if alt["tipo"] == STATUS_QUO:
            out.update(estado="STATUS_QUO", met=metricas_status_quo())
            self.cache[key] = out
            return out
        b = self.base(alt)
        if b[0] == "ERROR":
            out.update(estado="ERROR_CONSTRUCCION", motivo=b[1])
            self.cache[key] = out
            return out
        P0 = b[0]
        if "R13" in _MUT:                           # mutación: faltantes de costo convertidos en cero
            P0 = copy.deepcopy(P0)
            for e in P0["etapas"]:
                e["capex_usd"] = 0.0 if e["capex_usd"] is None else e["capex_usd"]
                for r in e.get("opex_rubros") or []:
                    r["costo_pleno_usd_anio"] = r["costo_pleno_usd_anio"] or 0.0
        P1, info = aplicar_shocks(P0, shocks, alt.get("base_valores"), alt["universo"])
        out.update(flags=info["flags"], cambios=info["cambios"])
        if P1 is None:
            out.update(estado=info["estado"], motivo=info["motivo"])
            self.cache[key] = out
            return out
        try:
            R = mf.simular(P1)
            res = mf.resultados(R, calcular_tir=bool(tir))
        except mf.ErrorFinanciero as e:
            out.update(estado="ERROR_MOTOR", motivo=str(e))
            self.cache[key] = out
            return out
        out["res"] = res
        out["met"] = metricas(res, R)
        if self.guardar_R:
            out["R"] = R
        self.cache[key] = out
        return out


def valor_metrica(ev, metrica):
    metrica = ALIAS_METRICA.get(metrica, metrica)
    v = ev["met"].get(metrica)
    if "R03" in _MUT and v is None:
        return 0.0                                  # mutación: faltante → 0
    return v


# ---------------------------------------------------------------------------------------------
# 6. SENSIBILIDAD ONE-WAY, TORNADO Y 2D
# ---------------------------------------------------------------------------------------------
METRICAS_SENS = ("INGRESOS", "EBITDA", "MARGEN_EBITDA", "FCFF_TOTAL", "FONDOS_INICIALES", "PICO_FONDOS", "VAN", "TIR",
                 "PAYBACK", "BREAK_EVEN_U", "DSCR", "UTILIZACION", "CT_MAX")


def shocks_de(var, inp):
    """Lista de shocks según el tipo de la variable (configurable; no implican probabilidad)."""
    t = VARIABLES[var]["TIPO_SHOCK"]
    clave = {"RELATIVO": "sensibilidad.shocks_relativos", "ABSOLUTO_DIAS": "sensibilidad.shocks_dias",
             "ABSOLUTO_MESES": "sensibilidad.shocks_meses"}.get(t)
    xs = [float(x) for x in como_lista(inp.get(clave))] if clave else []
    if 0.0 not in xs and xs:
        xs.append(0.0)
    return sorted(xs)


def sensibilidad_oneway(E, alt, variables, inp):
    con_tir = "TIR" in [str(x) for x in como_lista(inp.get("tornado.metricas"))]
    base = E.evaluar(alt, tir=con_tir)
    filas = []
    for var in variables:
        v = VARIABLES[var]
        if v["SOPORTE"] in ("DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"):
            filas.append({"ALTERNATIVA": alt["id"], "VARIABLE": var, "SHOCK": None, "TIPO_SHOCK": v["TIPO_SHOCK"],
                          "ESTADO": v["SOPORTE"], "MOTIVO": v["NOTA"] or VARIABLES[var]["CAMPO_MOTOR"]})
            continue
        for s in shocks_de(var, inp):
            ev = E.evaluar(alt, {var: s}, tir=con_tir)
            f = {"ALTERNATIVA": alt["id"], "VARIABLE": var, "SHOCK": s, "TIPO_SHOCK": v["TIPO_SHOCK"], "ESTADO": ev["estado"],
                 "MOTIVO": ev["motivo"], "FLAGS": "; ".join(ev["flags"]), "CAMPOS_MODIFICADOS": "; ".join(ev["cambios"].get(var, []))}
            for m in METRICAS_SENS:
                b_ = base["met"].get(m)
                x = ev["met"].get(m)
                f[m] = x if b_ is not None else None          # no se publica lo que la base no permite calcular
                f[f"DELTA_{m}"] = (x - b_) if (x is not None and b_ is not None) else None
            filas.append(f)
    return filas


def tornado(filas_oneway, metrica, alt_id):
    """Ordena variables por el rango (máx − mín) de la métrica entre los shocks evaluados. Sin métrica en la base:
    NO_CALCULABLE y sin ranking."""
    metrica = ALIAS_METRICA.get(metrica, metrica)
    fs = [f for f in filas_oneway if f["ALTERNATIVA"] == alt_id]
    base = next((f[metrica] for f in fs if f.get("SHOCK") == 0.0 and f["ESTADO"] == "OK"), None)
    out = []
    por_var = {}
    for f in fs:
        if f.get("SHOCK") is None:
            continue
        por_var.setdefault(f["VARIABLE"], []).append(f)
    for var, rows in por_var.items():
        vals = [(r["SHOCK"], r[metrica]) for r in rows if r["ESTADO"] == "OK" and r.get(metrica) is not None]
        fila = {"ALTERNATIVA": alt_id, "METRICA": metrica, "VARIABLE": var, "BASE": base}
        if base is None:
            fila.update(ESTADO=NO_CALC, NOTA=f"{metrica} no publicable en la base: no se fabrica ranking")
        elif not [x for x in vals if x[0] != 0]:
            est = sorted({r["ESTADO"] for r in rows})
            fila.update(ESTADO="SIN_VALORES", NOTA="; ".join(est) + " | " + "; ".join(sorted({r["MOTIVO"] for r in rows if r["MOTIVO"]}))[:300])
        else:
            lo = min(vals, key=lambda x: x[1])
            hi = max(vals, key=lambda x: x[1])
            n_nd = sum(1 for r in rows if r["ESTADO"] != "OK" or r.get(metrica) is None)
            sw = hi[1] - lo[1]
            fila.update(VALOR_MIN=lo[1], SHOCK_MIN=lo[0], VALOR_MAX=hi[1], SHOCK_MAX=hi[0], SWING=sw,
                        IMPACTO_ABS_MAX=max(abs(x[1] - base) for x in vals),
                        ESTADO="OK" if not n_nd else "OK_PARCIAL",
                        NOTA="" if not n_nd else f"{n_nd} shocks sin valor (no definidos / no aplicables)")
        out.append(fila)
    rank = [f for f in out if f.get("SWING") is not None]
    clave = (lambda f: f["SWING"]) if "R10" not in _MUT else (lambda f: f["VALOR_MAX"] - f["BASE"])
    rank.sort(key=clave, reverse=True)
    for i, f in enumerate(rank, 1):
        f["RANK"] = i
    return sorted(out, key=lambda f: (f.get("RANK") is None, f.get("RANK") or 0, f["VARIABLE"]))


def zona(valor, umbral, sentido, etiquetas):
    if valor is None:
        return NO_CALC
    if umbral is None:
        return "SIN_UMBRAL_DECLARADO"
    ok = valor >= umbral if sentido == ">=" else valor <= umbral
    return etiquetas[0] if ok else etiquetas[1]


def sensibilidad_2d(E, alt, par, inp):
    vx, vy = par
    umb_dscr, umb_pb = num(inp.get("umbral.dscr_2d")), num(inp.get("umbral.payback_2d"))
    filas = []
    for sx in shocks_de(vx, inp):
        for sy in shocks_de(vy, inp):
            ev = E.evaluar(alt, {vx: sx, vy: sy} if vx != vy else {vx: sx})
            m = ev["met"]
            van, eb = m.get("VAN"), m.get("EBITDA")
            pb = m.get("PAYBACK")
            filas.append({"ALTERNATIVA": alt["id"], "PAR": f"{vx}×{vy}", "VAR_X": vx, "SHOCK_X": sx, "VAR_Y": vy, "SHOCK_Y": sy,
                          "ESTADO": ev["estado"], "VAN": van, "EBITDA": eb, "DSCR": m.get("DSCR"), "PAYBACK": pb,
                          "ZONA_VAN": NO_CALC if van is None else ("POSITIVO" if van > 0 else ("NEGATIVO" if van < 0 else "CERO")),
                          "ZONA_EBITDA": NO_CALC if eb is None else ("POSITIVO" if eb > 0 else ("NEGATIVO" if eb < 0 else "CERO")),
                          "ZONA_DSCR": zona(m.get("DSCR"), umb_dscr, ">=", ("SUFICIENTE", "INSUFICIENTE")),
                          "ZONA_PAYBACK": ("NO_RECUPERADO" if (pb is None and str(m.get("PAYBACK_ESTADO")).startswith("NO_RECUPERADO"))
                                           else zona(pb, umb_pb, "<=", ("DENTRO_DEL_UMBRAL", "FUERA_DEL_UMBRAL")))})
    return filas


# ---------------------------------------------------------------------------------------------
# 7. STRESS (varias variables a la vez; plantillas editables)
# ---------------------------------------------------------------------------------------------
def leer_stress(ruta=ARCH_STRESS):
    grupos = {}
    for f in leer_csv(ruta):
        g = grupos.setdefault(f["ID_STRESS"], {"ID_STRESS": f["ID_STRESS"], "NOMBRE": f["NOMBRE"], "shocks": {},
                                                "pendientes": [], "activo": True, "estado": set(), "origen": set()})
        if f["ESTADO"] == "DESACTIVADO":
            g["activo"] = False
        g["estado"].add(f["ESTADO"])
        g["origen"].add(f["ORIGEN"])
        if f["VARIABLE"] not in VARIABLES:
            raise ErrorRiesgo(f"stress {f['ID_STRESS']}: variable desconocida {f['VARIABLE']}")
        v = num(f["VALOR_SHOCK"])
        if v is None:
            g["pendientes"].append(f["VARIABLE"])
        else:
            g["shocks"][f["VARIABLE"]] = v
    return list(grupos.values())


def correr_stress(E, alt, stresses):
    base = E.evaluar(alt)
    filas = []
    for st in stresses:
        f = {"ALTERNATIVA": alt["id"], "ID_STRESS": st["ID_STRESS"], "NOMBRE": st["NOMBRE"], "SHOCKS": st["shocks"],
             "ORIGEN_VALORES": "|".join(sorted(st["origen"]))}
        if not st["activo"]:
            f.update(ESTADO="DESACTIVADO")
        elif st["pendientes"]:
            f.update(ESTADO="NO_EJECUTADO_VALORES_PENDIENTES", MOTIVO="sin magnitud: " + ", ".join(st["pendientes"]))
        else:
            ev = E.evaluar(alt, st["shocks"])
            f.update(ESTADO=ev["estado"], MOTIVO=ev["motivo"])
            for m in ("EBITDA", "VAN", "TIR", "PAYBACK", "PICO_FONDOS", "FONDOS_INICIALES", "DSCR", "CAJA_MINIMA"):
                b_ = base["met"].get(m)
                x = ev["met"].get(m)
                f[m] = x if b_ is not None else None
                f[f"DELTA_{m}"] = (x - b_) if (x is not None and b_ is not None) else None
        filas.append(f)
    return filas


# ---------------------------------------------------------------------------------------------
# 8. PUNTOS DE QUIEBRE (grilla + bisección)
# ---------------------------------------------------------------------------------------------
def _m(E, alt, var, s, metrica):
    ev = E.evaluar(alt, {var: s}, tir=(metrica == "TIR"))
    return valor_metrica(ev, metrica) if ev["estado"] == "OK" else None


def punto_quiebre(E, alt, var, metrica="VAN", objetivo=0.0, rango=None, n_grilla=40, tol=1e-7, predicado=None):
    """Shock s* tal que métrica(s*) = objetivo, buscando el cruce más cercano a la base (s = 0).
    Método: grilla uniforme en `rango` (incluye 0) → intervalos con cambio de signo → bisección.
    predicado(valor) → bool permite umbrales no continuos (p. ej. payback ≤ X): se busca el borde del predicado.
    Estados: ENCONTRADO | NO_ENCONTRADO_EN_RANGO | NO_CALCULABLE | VARIABLE_NO_APLICA."""
    v = VARIABLES[var]
    out = {"ALTERNATIVA": alt["id"], "VARIABLE": var, "METRICA": metrica, "OBJETIVO": objetivo, "TIPO_SHOCK": v["TIPO_SHOCK"],
           "METODO": f"grilla {n_grilla} + bisección (tol {tol:g})"}
    if v["SOPORTE"] in ("DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"):
        out.update(ESTADO=NO_CALC, MOTIVO=f"variable {v['SOPORTE']}")
        return out
    b = E.evaluar(alt, tir=(metrica == "TIR"))
    lo, hi = rango or v["RANGO_QUIEBRE"]
    out.update(RANGO_MIN=lo, RANGO_MAX=hi)
    ev0 = E.evaluar(alt, {var: (lo + hi) / 2 if not (lo <= 0 <= hi) else (hi if hi != 0 else lo)})
    if ev0["estado"] == "NO_APLICA":
        out.update(ESTADO="VARIABLE_NO_APLICA", MOTIVO=ev0["motivo"])
        return out
    if ev0["estado"] == NO_CALC:
        out.update(ESTADO=NO_CALC, MOTIVO=ev0["motivo"])
        return out
    base_v = valor_metrica(b, metrica)
    out["VALOR_BASE"] = base_v
    if base_v is None and predicado is None:
        out.update(ESTADO=NO_CALC, MOTIVO=f"{metrica} no publicable en la base")
        return out
    g = sorted({lo + (hi - lo) * i / n_grilla for i in range(n_grilla + 1)} | ({0.0} if lo <= 0 <= hi else set()))

    def h(s):
        x = _m(E, alt, var, s, metrica)
        if predicado is not None:
            return 1.0 if predicado(x) else -1.0
        return None if x is None else x - objetivo

    vals = [(s, h(s)) for s in g]
    cruces = []
    for (s1, h1), (s2, h2) in zip(vals, vals[1:]):
        if h1 is None or h2 is None:
            continue
        if h1 == 0:
            cruces.append((s1, s1))
        elif h1 * h2 < 0:
            cruces.append((s1, s2))
    if vals and vals[-1][1] == 0:
        cruces.append((vals[-1][0], vals[-1][0]))
    if not cruces:
        num_ = [x for x in vals if x[1] is not None]
        out.update(ESTADO=NO_ENC, N_CRUCES=0, MOTIVO=(f"sin cruce en [{lo:g}, {hi:g}]; "
                   + (f"{metrica} − objetivo entre {min(x[1] for x in num_):.6g} y {max(x[1] for x in num_):.6g}" if num_ else
                      "métrica no definida en la grilla")))
        if "R16" in _MUT:
            out.update(ESTADO="ENCONTRADO", SHOCK_QUIEBRE=hi)
        return out
    a, c = min(cruces, key=lambda x: min(abs(x[0]), abs(x[1])))
    ha = h(a)
    for _ in range(200):
        if abs(c - a) <= tol:
            break
        mid = (a + c) / 2
        hm = h(mid)
        if hm is None:
            break
        if ha * hm <= 0:
            c = mid
        else:
            a, ha = mid, hm
    s_ = (a + c) / 2 if predicado is None else (c if h(c) > 0 else a)
    out.update(ESTADO="ENCONTRADO", SHOCK_QUIEBRE=s_, N_CRUCES=len(cruces),
               MOTIVO="" if len(cruces) == 1 else f"MULTIPLES_CRUCES ({len(cruces)}): se informa el más cercano a la base")
    if v["TIPO_SHOCK"] == "RELATIVO":
        out["FACTOR_SOBRE_BASE"] = 1 + s_
    base_abs = (alt.get("base_valores") or {}).get(var)
    if base_abs is not None:
        out["VALOR_ABSOLUTO_QUIEBRE"] = base_abs * (1 + s_) if v["TIPO_SHOCK"] == "RELATIVO" else base_abs + s_
    return out


# ---------------------------------------------------------------------------------------------
# 9. MONTE CARLO (infraestructura; distribuciones y correlaciones declaradas, nunca supuestas)
# ---------------------------------------------------------------------------------------------
DISTRIBUCIONES = ("TRIANGULAR", "NORMAL_TRUNCADA", "UNIFORME", "LOGNORMAL", "DISCRETA", "DETERMINISTA", "EMPIRICA")
ESTADOS_DIST = ("PENDIENTE", "RESPALDADA", "ARTIFICIAL")
_N01 = statistics.NormalDist()


def _params(txt):
    out = {}
    for par in (txt or "").split(";"):
        if not par.strip():
            continue
        k, v = par.split("=", 1)
        out[k.strip()] = [float(x) for x in v.split(",")] if "," in v else float(v)
    return out


def leer_distribuciones(ruta=ARCH_DIST):
    out = []
    for f in leer_csv(ruta):
        if f["VARIABLE"] not in VARIABLES:
            raise ErrorRiesgo(f"distribución de variable desconocida {f['VARIABLE']}")
        if f["ESTADO"] not in ESTADOS_DIST:
            raise ErrorRiesgo(f"estado de distribución {f['ESTADO']}")
        d = {"VARIABLE": f["VARIABLE"], "DISTRIBUCION": f["DISTRIBUCION"] or None, "PARAMETROS": _params(f["PARAMETROS"]),
             "FUENTE": f["FUENTE"], "ESTADO": f["ESTADO"]}
        if d["ESTADO"] != "PENDIENTE":
            validar_distribucion(d)
        out.append(d)
    return out


def validar_distribucion(d):
    t, p = d["DISTRIBUCION"], d["PARAMETROS"]
    if t not in DISTRIBUCIONES:
        raise ErrorRiesgo(f"{d['VARIABLE']}: distribución {t!r} no admitida {DISTRIBUCIONES}")
    req = {"TRIANGULAR": ("min", "moda", "max"), "NORMAL_TRUNCADA": ("media", "desvio", "min", "max"),
           "UNIFORME": ("min", "max"), "LOGNORMAL": ("mu", "sigma"), "DISCRETA": ("valores", "probs"),
           "DETERMINISTA": ("valor",), "EMPIRICA": ("valores",)}[t]
    if any(k not in p for k in req):
        raise ErrorRiesgo(f"{d['VARIABLE']}: {t} requiere {req}")
    if t == "TRIANGULAR" and not p["min"] <= p["moda"] <= p["max"]:
        raise ErrorRiesgo(f"{d['VARIABLE']}: triangular min ≤ moda ≤ max")
    if t == "DISCRETA" and abs(sum(como_lista(p["probs"])) - 1) > 1e-9:
        raise ErrorRiesgo(f"{d['VARIABLE']}: probabilidades discretas no suman 1")
    if t in ("NORMAL_TRUNCADA",) and (p["desvio"] <= 0 or p["min"] >= p["max"]):
        raise ErrorRiesgo(f"{d['VARIABLE']}: normal truncada con desvío > 0 y min < max")
    return d


def cuantil(d, u):
    """Inversa de la CDF (u ∈ (0, 1)). El valor es el SHOCK de la variable (en la unidad de su tipo)."""
    t, p = d["DISTRIBUCION"], d["PARAMETROS"]
    if t == "DETERMINISTA":
        return p["valor"]
    if t == "UNIFORME":
        return p["min"] + u * (p["max"] - p["min"])
    if t == "TRIANGULAR":
        a, c, b = p["min"], p["moda"], p["max"]
        if b == a:
            return a
        fc = (c - a) / (b - a)
        return a + math.sqrt(u * (b - a) * (c - a)) if u < fc else b - math.sqrt((1 - u) * (b - a) * (b - c))
    if t == "NORMAL_TRUNCADA":
        mu, sd = p["media"], p["desvio"]
        Fa, Fb = _N01.cdf((p["min"] - mu) / sd), _N01.cdf((p["max"] - mu) / sd)
        return mu + sd * _N01.inv_cdf(min(max(Fa + u * (Fb - Fa), 1e-12), 1 - 1e-12))
    if t == "LOGNORMAL":
        return math.exp(p["mu"] + p["sigma"] * _N01.inv_cdf(min(max(u, 1e-12), 1 - 1e-12))) - p.get("desplazamiento", 0.0)
    if t == "DISCRETA":
        acc = 0.0
        for v, pr in zip(como_lista(p["valores"]), como_lista(p["probs"])):
            acc += pr
            if u <= acc + 1e-15:
                return v
        return como_lista(p["valores"])[-1]
    if t == "EMPIRICA":
        return percentil(como_lista(p["valores"]), u)
    raise ErrorRiesgo(t)


def leer_correlaciones(ruta=ARCH_CORR):
    out = []
    for f in leer_csv(ruta):
        for v in (f["VARIABLE_A"], f["VARIABLE_B"]):
            if v not in VARIABLES:
                raise ErrorRiesgo(f"correlación con variable desconocida {v}")
        rho = num(f["COEFICIENTE"])
        if f["ESTADO"] != "PENDIENTE" and (rho is None or not -1 < rho < 1):
            raise ErrorRiesgo(f"correlación {f['VARIABLE_A']}–{f['VARIABLE_B']}: coeficiente en (−1, 1)")
        if f["ESTADO"] == "PENDIENTE" and rho is not None:
            raise ErrorRiesgo(f"correlación {f['VARIABLE_A']}–{f['VARIABLE_B']}: PENDIENTE con coeficiente cargado")
        out.append({"A": f["VARIABLE_A"], "B": f["VARIABLE_B"], "RHO": rho, "ESTADO": f["ESTADO"], "FUENTE": f["FUENTE"],
                    "RELACION": f.get("RELACION", "")})
    return out


def cholesky(M):
    n = len(M)
    L = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                d = M[i][i] - s
                if d <= 1e-12:
                    raise ErrorRiesgo("matriz de correlaciones no definida positiva")
                L[i][j] = math.sqrt(d)
            else:
                L[i][j] = (M[i][j] - s) / L[j][j]
    return L


def monte_carlo(E, alt, dists, corrs, n, semilla, universo, capital=None, exigir_respaldo=True, con_tir=False,
                supuesto_independencia=False):
    """Devuelve (estado, resumen, muestras, notas). Proyecto real: toda distribución usada debe estar RESPALDADA.
    Correlaciones: solo las declaradas con coeficiente (cópula gaussiana; un 0 explícito es una declaración). Un par
    relacionado con correlación PENDIENTE no se toma como 0: la corrida no se ejecuta (NO_EJECUTADO_CORRELACION_PENDIENTE)
    salvo que el usuario declare supuesto_independencia → rótulo SUPUESTO_INDEPENDENCIA_ESCENARIO con los pares."""
    notas = []
    usadas = [d for d in dists if d["ESTADO"] != "PENDIENTE"]
    pend = [d["VARIABLE"] for d in dists if d["ESTADO"] == "PENDIENTE"]
    if universo != "ARTIFICIAL_TEST" and "R17" not in _MUT:      # mutación R17: acepta distribuciones sin respaldo
        if any(d["ESTADO"] == "ARTIFICIAL" for d in usadas):
            raise ErrorRiesgo("distribuciones ARTIFICIALES solo en casos artificiales")
        if exigir_respaldo and (pend or not usadas):
            return MC_ND, {}, [], [f"distribuciones PENDIENTES: {', '.join(pend) or '(ninguna declarada)'}"]
    if not usadas:
        return MC_ND, {}, [], ["sin distribuciones declaradas"]
    if n is None or semilla is None:
        return NO_CALC, {}, [], ["número de simulaciones y semilla son obligatorios (reproducibilidad)"]
    var = [d["VARIABLE"] for d in usadas]
    tgt = {}
    for v_ in var:
        tgt.setdefault(VARIABLES[v_]["CAMPO_MOTOR"], []).append(v_)
    sol = [v for vs in tgt.values() if len(vs) > 1 for v in vs]
    if {"alimento", "maiz"} <= set(var) or {"alimento", "soja"} <= set(var) or {"alimento", "fcr"} <= set(var):
        notas.append("SOLAPAMIENTO: alimento y maíz/soja/FCR actúan sobre los mismos rubros (efectos multiplicativos)")
    if sol:
        notas.append("SOLAPAMIENTO_DE_CAMPOS: " + ", ".join(sol))
    idx = {v: i for i, v in enumerate(var)}
    M = [[1.0 if i == j else 0.0 for j in range(len(var))] for i in range(len(var))]
    no_mod, decl = [], []
    for c in corrs:
        if c["A"] in idx and c["B"] in idx:
            if c["ESTADO"] == "PENDIENTE" or c["RHO"] is None:
                no_mod.append(f"{c['A']}–{c['B']}")
            else:
                if universo != "ARTIFICIAL_TEST" and c["ESTADO"] == "ARTIFICIAL":
                    raise ErrorRiesgo("correlación ARTIFICIAL fuera de un caso artificial")
                M[idx[c["A"]]][idx[c["B"]]] = M[idx[c["B"]]][idx[c["A"]]] = c["RHO"]
                decl.append(f"{c['A']}–{c['B']}={c['RHO']:g}")
    if no_mod and not supuesto_independencia and "R26" not in _MUT:
        return MC_CORR_PEND, {}, [], [f"{CORR_NM}: correlación PENDIENTE (≠ 0) en {', '.join(no_mod)}; declarar el coeficiente "
                                      f"o el {SUP_INDEP} (montecarlo.supuesto_independencia)"]
    if no_mod and "R26" in _MUT:
        estado_corr = "CORRELACIONES_DECLARADAS"                  # mutación: pendiente tratada como 0 sin rotular
    elif no_mod:
        estado_corr = f"{SUP_INDEP}: " + ", ".join(no_mod) + ("; declaradas: " + ", ".join(decl) if decl else "")
    elif decl:
        estado_corr = "CORRELACIONES_DECLARADAS: " + ", ".join(decl)
    else:
        estado_corr = "SIN_PARES_RELACIONADOS_DECLARADOS (independencia no verificada)"
    L = cholesky(M)
    rng = random.Random(semilla if "R11" not in _MUT else None)
    muestras = []
    for it in range(int(n)):
        z = [rng.gauss(0.0, 1.0) for _ in var]
        zc = [sum(L[i][k] * z[k] for k in range(i + 1)) for i in range(len(var))]
        sh = {v: cuantil(usadas[i], _N01.cdf(zc[i])) for i, v in enumerate(var)}
        ev = E.evaluar(alt, sh, tir=con_tir)
        muestras.append({"ITER": it + 1, **{f"SHOCK_{v}": sh[v] for v in var}, "ESTADO": ev["estado"],
                         **{m: ev["met"].get(m) for m in ("VAN", "TIR", "PICO_FONDOS", "DSCR", "PAYBACK", "CAJA_MINIMA")},
                         "PAYBACK_ESTADO": ev["met"].get("PAYBACK_ESTADO")})
    res = {"N": len(muestras), "SEMILLA": semilla, "CORRELACIONES": estado_corr, "VARIABLES": var}
    res["TIR_CALCULADA"] = con_tir
    for m in ("VAN", "TIR", "PICO_FONDOS", "DSCR", "PAYBACK"):
        xs = [x[m] for x in muestras if x[m] is not None]
        res[m] = {"N_VALIDOS": len(xs)}
        if xs:
            res[m].update(MEDIA=statistics.fmean(xs), MEDIANA=statistics.median(xs),
                          **{f"P{int(p * 100)}": percentil(xs, p) for p in (0.05, 0.10, 0.50, 0.90, 0.95)})
    vans = [x["VAN"] for x in muestras if x["VAN"] is not None]
    res["PROB_VAN_NEGATIVO"] = (sum(1 for x in vans if x < 0) / len(vans)) if vans else None
    pic = [x["PICO_FONDOS"] for x in muestras if x["PICO_FONDOS"] is not None]
    if capital is not None and pic:
        res["PROB_DEFICIT"] = sum(1 for x in pic if x > capital) / len(pic)
        res["DEFINICION_DEFICIT"] = f"PICO_FONDOS > capital declarado ({capital:,.0f})"
    else:
        caj = [x["CAJA_MINIMA"] for x in muestras if x["CAJA_MINIMA"] is not None]
        res["PROB_DEFICIT"] = (sum(1 for x in caj if x < -1e-9) / len(caj)) if caj else None
        res["DEFINICION_DEFICIT"] = "caja mínima del accionista < 0" if caj else "NO_CALCULABLE (sin capital declarado ni flujo del accionista)"
    res["PROB_NO_RECUPERO"] = (sum(1 for x in muestras if str(x["PAYBACK_ESTADO"]).startswith("NO_RECUPERADO")) / len(muestras))
    return "EJECUTADO", res, muestras, notas


def filas_mc(alt_id, estado, res, notas, universo):
    if estado != "EJECUTADO":
        return [{"ALTERNATIVA": alt_id, "UNIVERSO": universo, "ESTADO": estado, "METRICA": "", "ESTADISTICO": "",
                 "VALOR": None, "NOTA": "; ".join(notas)}]
    out = []
    base = {"ALTERNATIVA": alt_id, "UNIVERSO": universo, "ESTADO": estado, "N_TOTAL": res["N"], "SEMILLA": res["SEMILLA"],
            "TIPO_PROBABILIDAD": TIPOS_PROBABILIDAD[0], "ES_PROBABILIDAD_HISTORICA": False, "ES_PROBABILIDAD_DEL_PROYECTO": False,
            "CORRELACIONES": res["CORRELACIONES"], "ETIQUETA": PROB_SIM + (f" | {ETIQ_ART}" if universo == "ARTIFICIAL_TEST" else f" | {ETIQ_SIM}"),
            "NOTA": "; ".join(notas)}
    for m in ("VAN", "TIR", "PICO_FONDOS", "DSCR", "PAYBACK"):
        for k, v in res[m].items():
            if k == "N_VALIDOS":
                continue
            out.append(dict(base, METRICA=m, ESTADISTICO=k, VALOR=v, N_VALIDOS=res[m]["N_VALIDOS"]))
        if not res[m]["N_VALIDOS"]:
            out.append(dict(base, METRICA=m, ESTADISTICO="SIN_VALORES", VALOR=None, N_VALIDOS=0))
    for k in ("PROB_VAN_NEGATIVO", "PROB_DEFICIT", "PROB_NO_RECUPERO"):
        out.append(dict(base, METRICA=k, ESTADISTICO="PROBABILIDAD_SIMULADA", VALOR=res[k],
                        N_VALIDOS=res["N"], NOTA=(res.get("DEFINICION_DEFICIT") if k == "PROB_DEFICIT" else base["NOTA"])))
    return out


# ---------------------------------------------------------------------------------------------
# 10. REGISTRO Y MATRIZ DE RIESGOS (cualitativos; sin probabilidad numérica inventada)
# ---------------------------------------------------------------------------------------------
NIVELES_CUAL = ("BAJA", "MEDIA", "ALTA", "PENDIENTE")
CAMPOS_REGISTRO = ("ID_RIESGO", "CATEGORIA", "RIESGO", "DRIVER_AFECTADO", "PROBABILIDAD", "METODO_PROBABILIDAD",
                   "FRECUENCIA_SECTORIAL_REFERENCIA", "UNIDAD_FRECUENCIA", "PERIODO_REFERENCIA", "FUENTE", "IMPACTO", "VELOCIDAD",
                   "CONTROLABILIDAD", "DETECTABILIDAD", "INTERDEPENDENCIAS", "MITIGACION", "ESTADO_MITIGACION",
                   "PROBABILIDAD_RESIDUAL", "IMPACTO_RESIDUAL", "INDICADOR_ALERTA", "UMBRAL_ALERTA", "EVIDENCIA", "ESTADO",
                   "OBSERVACIONES")
# Matriz cualitativa 3×3 (etiquetas, NO números). Documentada en registro_riesgos.md §3.
CLASE_CUALITATIVA = {("BAJA", "BAJA"): "BAJO", ("BAJA", "MEDIA"): "BAJO", ("BAJA", "ALTA"): "MODERADO",
                     ("MEDIA", "BAJA"): "BAJO", ("MEDIA", "MEDIA"): "MODERADO", ("MEDIA", "ALTA"): "ALTO",
                     ("ALTA", "BAJA"): "MODERADO", ("ALTA", "MEDIA"): "ALTO", ("ALTA", "ALTA"): "CRITICO"}


def leer_registro_riesgos(ruta=ARCH_REG_RIESGOS):
    filas = leer_csv(ruta)
    if not filas:
        raise ErrorRiesgo("registro de riesgos vacío")
    falt = set(CAMPOS_REGISTRO) - set(filas[0])
    if falt:
        raise ErrorRiesgo(f"registro_riesgos.csv sin campos {sorted(falt)}")
    ids = [f["ID_RIESGO"] for f in filas]
    if len(ids) != len(set(ids)):
        raise ErrorRiesgo("ID_RIESGO duplicado")
    for f in filas:
        for c in ("PROBABILIDAD", "IMPACTO", "PROBABILIDAD_RESIDUAL", "IMPACTO_RESIDUAL"):
            if f[c] and f[c] not in NIVELES_CUAL:
                raise ErrorRiesgo(f"{f['ID_RIESGO']}: {c} = {f[c]!r} (admitidos {NIVELES_CUAL}; sin números)")
        # PROBABILIDAD = probabilidad ESPECÍFICA del proyecto (cualitativa). Exige método explícito; una frecuencia o
        # antecedente sectorial NO es probabilidad futura del proyecto y va en FRECUENCIA_SECTORIAL_REFERENCIA.
        if f["PROBABILIDAD"] not in ("", "PENDIENTE"):
            m = f["METODO_PROBABILIDAD"].strip().upper()
            if not m or "FRECUENCIA_SECTORIAL" in m or "01 §11" in m:
                raise ErrorRiesgo(f"{f['ID_RIESGO']}: PROBABILIDAD {f['PROBABILIDAD']} sin METODO_PROBABILIDAD específico del "
                                  "proyecto (una frecuencia sectorial no es probabilidad: dejar PENDIENTE)")
        for d in [x.strip() for x in f["DRIVER_AFECTADO"].split("|") if x.strip()]:
            if d not in VARIABLES:
                raise ErrorRiesgo(f"{f['ID_RIESGO']}: driver {d} no está en el registro de variables")
    return filas


def probabilidad_numerica(nivel):
    """Un nivel cualitativo NO tiene probabilidad numérica: siempre None (nunca 0 para PENDIENTE)."""
    if "R18" in _MUT:
        return {"BAJA": 0.1, "MEDIA": 0.3, "ALTA": 0.6}.get(nivel, 0.0)
    return None


def matriz_riesgos(registro, tornado_por_var=None):
    out = []
    for f in registro:
        p, i = f["PROBABILIDAD"] or "PENDIENTE", f["IMPACTO"] or "PENDIENTE"
        if "R23" in _MUT and p == "PENDIENTE" and f.get("FRECUENCIA_SECTORIAL_REFERENCIA"):
            p = "ALTA" if "Alta" in f["FRECUENCIA_SECTORIAL_REFERENCIA"] else "MEDIA"   # mutación: frecuencia → probabilidad
        inh = CLASE_CUALITATIVA.get((p, i), "PENDIENTE")
        impl = f["ESTADO_MITIGACION"] == "IMPLEMENTADA_CON_EVIDENCIA"
        pr = (f["PROBABILIDAD_RESIDUAL"] or "PENDIENTE") if impl else p
        ir = (f["IMPACTO_RESIDUAL"] or "PENDIENTE") if impl else i
        res = CLASE_CUALITATIVA.get((pr, ir), "PENDIENTE")
        if "R19" in _MUT and f["MITIGACION"]:
            inh = res = "BAJO"                                  # mutación: la mitigación borra el riesgo inherente
        drivers = [x.strip() for x in f["DRIVER_AFECTADO"].split("|") if x.strip()]
        sw = [(d, tornado_por_var[d]) for d in drivers if tornado_por_var and tornado_por_var.get(d) is not None]
        out.append({"ID_RIESGO": f["ID_RIESGO"], "CATEGORIA": f["CATEGORIA"], "RIESGO": f["RIESGO"],
                    "PROBABILIDAD_INHERENTE": p, "IMPACTO_INHERENTE": i, "CELDA_INHERENTE": f"{p}×{i}",
                    "FRECUENCIA_SECTORIAL_REFERENCIA": f.get("FRECUENCIA_SECTORIAL_REFERENCIA", ""),
                    "NOTA_FRECUENCIA": ("frecuencia/antecedente SECTORIAL: no es probabilidad del proyecto"
                                        if f.get("FRECUENCIA_SECTORIAL_REFERENCIA") else ""),
                    "CLASE_INHERENTE": inh, "ESTADO_MITIGACION": f["ESTADO_MITIGACION"],
                    "PROBABILIDAD_RESIDUAL": pr, "IMPACTO_RESIDUAL": ir, "CELDA_RESIDUAL": f"{pr}×{ir}", "CLASE_RESIDUAL": res,
                    "RESIDUAL_IGUAL_INHERENTE": "SÍ (mitigación no implementada o sin evidencia)" if not impl else "NO",
                    "TIPO_MATRIZ": "CUALITATIVA (BAJA/MEDIA/ALTA son etiquetas; sin producto numérico P×I)",
                    "PROB_NUMERICA": probabilidad_numerica(p), "IMPACTO_USD": None, "EXPOSICION_USD": None,
                    "RIESGO_ESPERADO": None if "R23" not in _MUT else 0.0,
                    "RIESGO_ESPERADO_ESTADO": "NO_CALCULADO: no existe probabilidad específica del proyecto",
                    "ESTADO_CUANTITATIVO": "FUTURO: requiere distribución respaldada y escenario completo",
                    "SWING_VAN_SIMULADO": "; ".join(f"{d}: {v:,.0f}" for d, v in sw) if sw else "",
                    "DRIVERS": " | ".join(drivers)})
    return out


def registro_variables_filas(inp=None):
    inp = inp or {}
    out = []
    for v in VARIABLES.values():
        out.append({k: v[k] for k in ("ID", "CATEGORIA", "DESCRIPCION", "TIPO_SHOCK", "SOPORTE", "CAMPO_MOTOR",
                                      "BLOQUE_MOTOR", "DPV", "NOTA")} |
                   {"MONOTONIA_VAN_ESPERADA": {1: "CRECIENTE", -1: "DECRECIENTE"}.get(v["MONOTONIA_VAN"], "NO_MONOTONA / NO_APLICA"),
                    "RANGO_QUIEBRE": f"{v['RANGO_QUIEBRE'][0]:g} a {v['RANGO_QUIEBRE'][1]:g}",
                    "SHOCKS_CONFIGURADOS": "|".join(f"{x:g}" for x in shocks_de(v["ID"], inp)) if inp else ""})
    return out
