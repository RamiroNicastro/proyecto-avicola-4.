#!/usr/bin/env python3
"""
MODELO OPTIMIZADOR — versión 1.0 (2026-10-05, sesión 20)
========================================================

Busca configuraciones usando el MODELO FINANCIERO (21) como función de evaluación. No duplica fórmulas: cada
alternativa se arma con `modelo_financiero.construir_entrada()` (que consume CAPEX 19, OPEX 20, balance 04,
escala 23 y demanda 02) y se evalúa con `simular()` + `resultados()` a través de motor_riesgo.Evaluador.

DOS UNIVERSOS (nunca se rankean juntos)
  EVIDENCIA : misma corrida que el modo evidencia del motor. Si ninguna alternativa tiene VAN publicable:
              OPTIMIZACION_REAL_NO_DISPONIBLE + qué datos la bloquean (prioridad_validacion.csv).
  ESCENARIO : inputs hipotéticos del usuario (escenario_optimizador.json). Todo se rotula
              SIMULACION_HIPOTETICA_NO_VALIDADA; la "mejor" alternativa lo es DENTRO DEL ESCENARIO.
  Aparte, ARTIFICIAL_TEST (casos_prueba/): alternativas ART-* inventadas para probar la maquinaria.

ESPACIO DE DECISIONES
  Configuraciones del mapa (C0–CF + 19 variantes) × escalas de `inputs_riesgo_optimizacion.csv` (2.500 a 20.000,
  intermedias admitidas por CAPEX) × trayectorias multietapa, + NO_INVERTIR_AUN (status quo). C0 = OPERAR_ASSET_LIGHT.
  Las combinaciones de atributos (faena, granjas, pollito, alimento, flota, frío, subproductos, rendering) se
  enumeran y clasifican: EN_MAPA (evaluada) / VALIDA_NO_MAPEADA (la interfaz financiera no la soporta: no se
  evalúa, se lista) / INVALIDA (validar_config de CAPEX la rechaza). Nada físicamente imposible se evalúa.

CADENA POR ALTERNATIVA
  factibilidad física (gates) → evaluación base → restricciones HARD / SOFT → comparabilidad → cobertura de
  evidencia → robustez (stress + extremos one-way) → score de riesgo (si hay pesos) → ranking por objetivo →
  dominancia / Pareto → segunda alternativa y robustez de la decisión → explicación → valor de la información →
  QUE_HACER_AHORA → semáforo / dashboard.

Uso
    python3 22_riesgos/modelo_optimizador.py                # tests + salidas del proyecto + caso artificial
    python3 22_riesgos/modelo_optimizador.py --solo-tests
    python3 22_riesgos/modelo_optimizador.py --mutaciones
    python3 22_riesgos/modelo_optimizador.py --escenario mi_escenario.json --salida carpeta/
"""
import argparse
import copy
import hashlib
import io
import itertools
import json
import math
import os
import re
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import motor_riesgo as mr          # noqa: E402

mf = mr.mf
mcx = mf.mcx
VERSION = mr.VERSION
FECHA = mr.FECHA
RAIZ = mr.RAIZ
ARCH_ESCENARIO = os.path.join(AQUI, "escenario_optimizador.json")
DIR_CASOS = os.path.join(AQUI, "casos_prueba")
ARCH_DPV = os.path.join(RAIZ, "00_gestion_proyecto", "datos_por_validar.md")
ARCH_DEC = os.path.join(RAIZ, "00_gestion_proyecto", "decisiones_pendientes.md")
NINGUNA = "NINGUNA_CONFIGURACION_FACTIBLE"
SQ = mr.STATUS_QUO
ASSET_LIGHT = "OPERAR_ASSET_LIGHT"
NO_ROB = "DECISION_NO_ROBUSTA"
# Columna futura de prioridad (auditoría final 21): cuánto puede cambiar la decisión obtener el dato. En el universo
# EVIDENCIA no puede calcularse (no hay escenario que perturbar): queda NO_CALCULADO, nunca 0 ni un orden inventado.
POTENCIAL_NO_CALC = "NO_CALCULADO"


# ---------------------------------------------------------------------------------------------
# 1. ESPACIO DE DECISIONES
# ---------------------------------------------------------------------------------------------
DIMENSIONES = ("faena", "granjas", "pollito", "alimento", "flota", "frio", "subproductos", "rendering", "reproductoras")


def _dims(cc):
    return tuple(cc[k] for k in DIMENSIONES)


def configuraciones_mapa():
    """[(configuración base, variante o None, escala de referencia de la variante)] tal como las define el mapa."""
    out = []
    for r in mf.mapa_arquitecturas():
        if r["TIPO"] == "CONFIGURACION_BASE":
            out.append((r["CONFIGURACION"], None, None))
        else:
            ref = r["ESCENARIO_REFERENCIA"]
            out.append((r["VARIANTE_DE"], ref, int(ref.split("-")[1])))
    return out


CLASES_ESPACIO = ("FISICAMENTE_INVALIDA", "FISICAMENTE_POSIBLE_NO_MODELADA_ECONOMICAMENTE", "HABILITADA_EN_MAPA_PARA_EVALUACION")


def n_alternativas_mapa(inp, base, var):
    """Alternativas económicas que genera una fila del mapa: base → escalas + trayectorias multietapa; variante → 1."""
    if var is not None:
        return 0 if mr.como_lista(inp.get("espacio.incluir_variantes")) == [False] else 1
    esc = [e for e in mr.como_lista(inp.get("espacio.escalas")) if mcx.RANGO_ESCALA[0] <= int(e) <= mcx.RANGO_ESCALA[1]]
    tr = [t for t in mr.como_lista(inp.get("espacio.trayectorias")) if len(mf.TRAYECTORIAS_FIN.get(t, ())) > 1]
    return len(esc) + len(tr)


def espacio_decisiones(inp):
    """Enumera TODAS las combinaciones de atributos y las clasifica (nada se descarta en silencio):
      FISICAMENTE_INVALIDA                            validar_config() de 19 la rechaza (motivo informado)
      FISICAMENTE_POSIBLE_NO_MODELADA_ECONOMICAMENTE  CAPEX la acepta, pero no existe en el mapa: no se le inventa
                                                      CAPEX/OPEX y no se evalúa (DEC-103)
      HABILITADA_EN_MAPA_PARA_EVALUACION              coincide con configuraciones del mapa → genera alternativas económicas
    Las alternativas económicas = Σ sobre las filas del mapa de n_alternativas_mapa() (+ NO_INVERTIR_AUN)."""
    mapa = {}
    for base, var, esc in configuraciones_mapa():
        cc, _ = mf.configs(var or f"{base}-10000")
        mapa.setdefault(_dims(cc), []).append((var or base, n_alternativas_mapa(inp, base, var) if base in
                                               mr.como_lista(inp.get("espacio.configuraciones")) else 0))
    filas = []
    ops = [mcx.OPCIONES[k] for k in DIMENSIONES[:7]] + [(False, True), (False, True)]
    c2 = mcx.preset("C2")
    for combo in itertools.product(*ops):
        d = dict(zip(DIMENSIONES, combo))
        c = mcx.config_por_defecto()
        c.update(d)
        c["fraccion_granjas_propias"] = {"integradas": 0.0, "propias": 1.0, "mixto": c2["fraccion_granjas_propias"]}[d["granjas"]]
        if d["flota"] == "mixto":
            c["flota_por_flujo"] = copy.deepcopy(c2["flota_por_flujo"])
        en, n_alt = [], 0
        try:
            mcx.validar_config(c)
            en = mapa.get(combo) or []
            n_alt = sum(n for _, n in en)
            clase = CLASES_ESPACIO[2] if en else CLASES_ESPACIO[1]
            motivo = ("configuraciones del mapa: " + ", ".join(x for x, _ in en)) if en else (
                "físicamente posible para CAPEX, pero no está en el mapa de arquitecturas: no hay CAPEX/OPEX modelado "
                "(no se inventa) y no se evalúa; requiere ampliar el mapa (DEC-103)")
        except mcx.ErrorCapex as e:
            clase, motivo = CLASES_ESPACIO[0], str(e)
        filas.append({"ID_COMBINACION": f"COMB-{len(filas) + 1:04d}", **{k.upper(): v for k, v in d.items()},
                      "CLASIFICACION": clase, "CONFIGURACIONES_DEL_MAPA": ", ".join(x for x, _ in en),
                      "ALTERNATIVAS_ECONOMICAS": n_alt, "MOTIVO": motivo})
    lo, hi = mcx.RANGO_ESCALA
    for E in mr.como_lista(inp.get("espacio.escalas")):
        ok = lo <= E <= hi
        filas.append({"ID_COMBINACION": f"ESC-{E}", "FAENA": "—", "CLASIFICACION": "ESCALA_EVALUADA" if ok else "ESCALA_INVALIDA",
                      "MOTIVO": f"escala {E} aves/día " + ("dentro" if ok else "fuera") + f" del rango estudiado {lo}–{hi}"
                      + ("" if E in mcx.ESCALAS_REF or not ok else " (intermedia: CALCULO_MODELO_FUENTE en CAPEX)")})
    return filas


def id_alt(cfg, var, escalas, tray):
    return f"{cfg}|{var or 'BASE'}|{'-'.join(str(e) for e in escalas)}|{tray}"


def _merge(a, b):
    out = copy.deepcopy(a)
    for k, v in (b or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


def leer_escenario(ruta=ARCH_ESCENARIO):
    with open(ruta, encoding="utf-8") as fh:
        spec = json.load(fh)
    return {k: v for k, v in spec.items() if not k.startswith("_")}


def alternativas_reales(inp, universo, escenario=None):
    """Alternativas del mapa en el universo pedido. EVIDENCIA: construir_entrada en modo EVIDENCIA (sin usuario).
    ESCENARIO: construir_entrada en modo ESCENARIO con `comun` + `por_alternativa[id]` del JSON del usuario."""
    if universo not in ("EVIDENCIA", "ESCENARIO"):
        raise mr.ErrorRiesgo("alternativas reales: universo EVIDENCIA o ESCENARIO")
    escenario = escenario or {}
    cfgs = set(mr.como_lista(inp.get("espacio.configuraciones")))
    escalas = [int(e) for e in mr.como_lista(inp.get("espacio.escalas")) if mcx.RANGO_ESCALA[0] <= int(e) <= mcx.RANGO_ESCALA[1]]
    trays = mr.como_lista(inp.get("espacio.trayectorias"))
    out = []

    def mk(cfg, var, esc, tray):
        aid = id_alt(cfg, var, esc, tray)
        comun = {k: v for k, v in (escenario.get("comun") or {}).items() if not k.startswith("_")}
        usr = _merge(comun, (escenario.get("por_alternativa") or {}).get(aid))
        plantilla = escenario.get("plantilla")
        if universo == "EVIDENCIA":
            fn = (lambda c=cfg, e=esc, v=var, a=aid: mf.construir_entrada(a, c, e, "EVIDENCIA", None, None, v))
        else:
            fn = (lambda c=cfg, e=esc, v=var, a=aid, u=usr, p=plantilla: mf.construir_entrada(a, c, e, "ESCENARIO", p, u, v))
        cc, _ = mf.configs(var or f"{cfg}-{esc[-1]}")
        out.append({"id": aid, "tipo": ASSET_LIGHT if cc["faena"] == "facon" else "PLANTA", "universo": universo,
                    "configuracion": cfg, "variante": var or "BASE", "escalas": tuple(esc), "trayectoria": tray,
                    "construir": fn, "base_valores": dict(escenario.get("base_valores") or {}),
                    "cc": cc, "fisico": None, "disponibilidad": dict(escenario.get("disponibilidad") or {})})
    for base, var, esc_ref in configuraciones_mapa():
        if base not in cfgs:
            continue
        if var is None:
            for E in escalas:
                mk(base, None, (E,), "ESCALA_UNICA")
            for t in trays:
                if t in mf.TRAYECTORIAS_FIN and len(mf.TRAYECTORIAS_FIN[t]) > 1:
                    mk(base, None, mf.TRAYECTORIAS_FIN[t], t)
        elif mr.como_lista(inp.get("espacio.incluir_variantes")) != [False]:
            mk(base, var, (esc_ref,), "ESCALA_UNICA")
    ids = [a["id"] for a in out]
    if len(ids) != len(set(ids)):
        raise mr.ErrorRiesgo("ID de alternativa duplicado")
    if "R05" not in mr._MUT:
        out.append(mr.alternativa_status_quo(universo))
    return out


# ---------------------------------------------------------------------------------------------
# 2. FACTIBILIDAD FÍSICA (gates; sin dato → FACTIBILIDAD_PENDIENTE, nunca FACTIBLE)
# ---------------------------------------------------------------------------------------------
FACTIBLE, NO_FACTIBLE, PEND, NA = "FACTIBLE", "NO_FACTIBLE", "FACTIBILIDAD_PENDIENTE", "NO_APLICA"


def _drv(D, k):
    x = D["proc"].get(k)
    if not x or x["VALOR"][1] is None:
        return None, (x or {}).get("ESTADO_EVIDENCIA", "sin driver")
    return x["VALOR"][1], x["ESTADO_EVIDENCIA"]


REQ_ESTADOS = ("DIMENSIONADO", "NO_REQUERIDO_POR_ARQUITECTURA", "DESCONOCIDO")


def _gate(nombre, req, unidad, disp, dpv, sentido="<=", nota="", estado_req=None):
    """Gate físico. ESTADO_REQUERIMIENTO distingue un 0 ESTRUCTURAL (NO_REQUERIDO_POR_ARQUITECTURA: la arquitectura no
    tiene el activo que consume el recurso) de un dato DESCONOCIDO (requerimiento no dimensionado): nunca se iguala a 0."""
    estado_req = estado_req or ("DESCONOCIDO" if req is None else "DIMENSIONADO")
    if estado_req == "NO_REQUERIDO_POR_ARQUITECTURA":
        return {"GATE": nombre, "REQUERIDO": 0.0, "UNIDAD": unidad, "DISPONIBLE": disp, "ESTADO": NA, "DPV": dpv,
                "ESTADO_REQUERIMIENTO": estado_req, "NOTA": nota or "la arquitectura no requiere este recurso propio"}
    if isinstance(disp, bool) or (req is True):
        est = FACTIBLE if disp is True else (NO_FACTIBLE if disp is False else PEND)
    elif req is None:
        est = PEND
    elif disp is None:
        est = PEND
    else:
        est = FACTIBLE if (req <= disp + 1e-9 if sentido == "<=" else req >= disp - 1e-9) else NO_FACTIBLE
    return {"GATE": nombre, "REQUERIDO": req, "UNIDAD": unidad, "DISPONIBLE": disp, "ESTADO": est, "DPV": dpv,
            "ESTADO_REQUERIMIENTO": estado_req, "NOTA": nota or ("dato de disponibilidad no declarado" if disp is None and req is not None else
                             ("requerimiento no dimensionado por los módulos físicos" if req is None else ""))}


def factibilidad_fisica_real(alt):
    """Gates físicos con requerimientos CONSUMIDOS de los drivers de 19_capex (que a su vez vienen de 03/05/09/11/12/14)
    y disponibilidades declaradas por el usuario (`disponibilidad` del escenario). Escala final de la trayectoria."""
    disp = alt.get("disponibilidad") or {}
    E = alt["escalas"][-1]
    cc = copy.deepcopy(alt["cc"])
    gates = []
    try:
        mcx.validar_config(cc)
        gates.append(_gate("ARQUITECTURA", True, "—", True, "", nota=mcx.etiqueta_arquitectura(cc)))
    except mcx.ErrorCapex as e:
        gates.append(_gate("ARQUITECTURA", True, "—", False, "", nota=str(e)))
        return {"ESTADO": NO_FACTIBLE, "gates": gates}
    lo, hi = mcx.RANGO_ESCALA
    ok = all(lo <= e <= hi for e in alt["escalas"])
    gates.append(_gate("ESCALA", True, "aves/día", ok, "DEC-001", nota=f"rango estudiado {lo}–{hi}"))
    with redirect_stdout(io.StringIO()):
        D = mcx.drivers(cc)
    if cc["faena"] == "propia":
        r, ev = _drv(D, "terreno_requerido_arquitectura")
        gates.append(_gate("TERRENO", r, "m²", disp.get("terreno_m2"), "DPV-087", nota=f"requerido {ev}"))
        r, ev = _drv(D, "agua_captada_m3_dia")
        gates.append(_gate("AGUA", r, "m³/día", disp.get("agua_m3_dia"), "DPV-053", nota=f"requerido {ev}"))
        r, ev = _drv(D, "potencia_pico_demanda_maxima_kw")
        gates.append(_gate("POTENCIA", r, "kW", disp.get("potencia_kw"), "DPV-095", nota=f"requerido {ev}"))
        r, ev = _drv(D, "ritmo_nominal_requerido")
        g, evg = _drv(D, "capacidad_garantizada_linea")
        gates.append(_gate("CAPACIDAD_LINEA", r, "aves/h", g if g is not None else disp.get("capacidad_linea_aves_h"),
                           "DPV-097", nota=f"garantizada {evg}"))
    else:
        gates.append(_gate("FACON_FAENA", float(E), "aves/día", disp.get("facon_faena_aves_dia"), "DPV-006"))
        # Faena a façon: la PLANTA de faena, su terreno industrial, frío y utilities NO son de la empresa
        # (NO_REQUERIDO_POR_ARQUITECTURA para ese componente), pero los módulos propios restantes (oficina/IT/estructura
        # del CAPEX de C0, y frío, flota, alimento, granjas o incubación propios si la variante los tuviera) no tienen
        # requerimiento dimensionado → DESCONOCIDO (no 0).
        propios = modulos_propios_facon(cc)
        for nombre, unidad, clave, dpv in (("TERRENO", "m²", "terreno_m2", "DPV-087"), ("AGUA", "m³/día", "agua_m3_dia", "DPV-053"),
                                           ("POTENCIA", "kW", "potencia_kw", "DPV-095")):
            gates.append(_gate(nombre, None, unidad, disp.get(clave), dpv, estado_req="DESCONOCIDO",
                               nota="planta de faena: NO_REQUERIDO_POR_ARQUITECTURA; módulos propios sin dimensionar: "
                                    + ", ".join(propios)))
    m2, ev = _drv(D, "m2_galpon")
    frac = cc.get("fraccion_granjas_propias") or 0.0
    if cc["granjas"] in ("integradas", "mixto"):
        gates.append(_gate("PRODUCCION_PRIMARIA_INTEGRADOS", None if m2 is None else m2 * (1 - frac), "m² galpón",
                           disp.get("m2_galpon_integrados"), "DPV-048", nota=f"requerido {ev}"))
    if cc["granjas"] in ("propias", "mixto"):
        gates.append(_gate("SITIOS_GRANJAS_PROPIAS", True, "sitios", disp.get("sitios_granja_confirmados"), "DPV-051"))
    pol, ev = _drv(D, "pollitos_a_recibir_semana_plena")
    if cc["pollito"] == "compra":
        gates.append(_gate("POLLITO", pol, "pollitos/semana", disp.get("pollitos_semana"), "DPV-006, DPV-047", nota=f"requerido {ev}"))
    else:
        gates.append(_gate("HUEVO_FERTIL_INCUBACION", True, "—", disp.get("huevo_fertil_confirmado"), "DPV-047"))
    alim, ev = _drv(D, "alimento_t_semana_plena")
    if alim is None:
        a_, ev = _drv(D, "alimento_t_anio")
        alim = None if a_ is None else a_ / 52
    key = {"compra": ("alimento_t_semana", "DPV-050"), "facon": ("facon_alimento_t_semana", "DPV-155"),
           "propia": ("granos_t_semana", "DPV-157")}[cc["alimento"]]
    gates.append(_gate(f"ALIMENTO_{cc['alimento'].upper()}", alim, "t/semana", disp.get(key[0]), key[1], nota=f"requerido {ev}"))
    if cc["subproductos"] == "A_externo":
        gates.append(_gate("RECEPTOR_SUBPRODUCTOS", True, "—", disp.get("receptor_subproductos_confirmado"), "DEC-027"))
    else:
        gates.append(_gate("TRATAMIENTO_SUBPRODUCTOS", True, "—", disp.get("tratamiento_subproductos_habilitado"), "DPV-072"))
    if cc["flota"] in ("tercero", "mixto"):
        gates.append(_gate("TRANSPORTE_TERCERO", True, "—", disp.get("transporte_tercero_confirmado"), "DPV-042"))
    if cc["frio"] == "C_congelado_tercero":
        gates.append(_gate("FRIO_TERCERO", True, "—", disp.get("frio_tercero_confirmado"), "DPV-109"))
    return {"ESTADO": estado_fisico(gates), "gates": gates}


def modulos_propios_facon(cc):
    """Módulos propios de una arquitectura con faena a façon que pueden consumir terreno, agua o potencia."""
    m = ["oficina / IT / estructura (CAPEX de C0 en el mapa)"]
    if cc["frio"] != "C_congelado_tercero":
        m.append(f"frío propio ({cc['frio']})")
    if cc["flota"] != "tercero":
        m.append(f"flota propia ({cc['flota']})")
    if cc["alimento"] == "propia":
        m.append("planta de alimento propia")
    if cc["granjas"] != "integradas":
        m.append(f"granjas propias ({cc['granjas']})")
    if cc["pollito"] == "incubacion":
        m.append("incubación propia")
    if cc["subproductos"] != "A_externo":
        m.append(f"subproductos ({cc['subproductos']})")
    return m


def estado_fisico(gates):
    est = [g["ESTADO"] for g in gates]
    if NO_FACTIBLE in est:
        return NO_FACTIBLE
    if PEND in est:
        return PEND
    return FACTIBLE


# ---------------------------------------------------------------------------------------------
# 3. COBERTURA DE EVIDENCIA (confianza ≠ rentabilidad)
# ---------------------------------------------------------------------------------------------
_COB = {}


def cobertura_evidencia(alt):
    """Fracción de bloques APLICABLES del motor con evidencia presente EN MODO EVIDENCIA (misma configuración y
    escala): CON_EVIDENCIA ÷ (bloques − NO_APLICA). Un bloque VACIO (sin faltantes pero sin contenido) o PENDIENTE no
    suma (auditoría final 21, TF-011). No es una probabilidad: mide cuánto descansa en evidencia dentro del umbral."""
    if alt["tipo"] == SQ:
        return None, "NO_APLICA (status quo)"
    if alt["universo"] == "ARTIFICIAL_TEST":
        return 0.0, "ARTIFICIAL_TEST: ningún bloque tiene evidencia"
    key = (alt["configuracion"], alt["variante"], alt["escalas"])
    if key not in _COB:
        var = None if alt["variante"] == "BASE" else alt["variante"]
        with redirect_stdout(io.StringIO()):
            P, _ = mf.construir_entrada("COB", alt["configuracion"], alt["escalas"], "EVIDENCIA", None, None, var)
        est = mf.estado_bloques(P)                 # TF-011: VACIO y PENDIENTE no suman; NO_APLICA sale del denominador
        cob = mf.cobertura_bloques(est)
        por = {e: [b for b, x in est.items() if x == e] for e in mf.ESTADOS_BLOQUE}
        nota = "; ".join(f"{e} ({len(v)}): {', '.join(v)}" for e, v in por.items() if v)
        _COB[key] = (cob if cob is not None else 0.0, nota)
    return _COB[key]


# ---------------------------------------------------------------------------------------------
# 4. RESTRICCIONES (HARD elimina; SOFT penaliza el score; todas opcionales; capital NUNCA por defecto)
# ---------------------------------------------------------------------------------------------
RESTRICCIONES = {   # nombre → (métrica, sentido, fuente de la métrica)
    "CAPITAL_DISPONIBLE": (None, "<=", "met"), "FONDOS_INICIALES": ("FONDOS_INICIALES", "<=", "met"),
    "PICO_FONDOS": ("PICO_FONDOS", "<=", "met"), "PAYBACK": ("PAYBACK", "<=", "met"), "VAN": ("VAN", ">=", "met"),
    "TIR": ("TIR", ">=", "met"), "DSCR": ("DSCR", ">=", "met"), "DEMANDA_ASEGURADA": ("DEMANDA_ASEGURADA_PCT", ">=", "met"),
    "UTILIZACION": ("UTILIZACION", ">=", "met"), "SUPERFICIE_TERRENO": ("TERRENO", "<=", "fis"),
    "AGUA": ("AGUA", "<=", "fis"), "POTENCIA": ("POTENCIA", "<=", "fis"), "CAPACIDAD": ("CAPACIDAD_FINAL_AVES_DIA", "<=", "met"),
    "DEUDA": ("DEUDA", "<=", "met"), "RIESGO": ("SCORE_ORDINAL_RIESGO", "<=", "ficha")}
RETORNO = {"PAYBACK", "VAN", "TIR", "DSCR", "DEMANDA_ASEGURADA", "UTILIZACION", "RIESGO"}


def leer_restricciones(inp, extra=None):
    out = []
    for nombre in RESTRICCIONES:
        v = inp.get(f"restriccion.{nombre}.valor")
        if extra and nombre in extra:
            v = extra[nombre]
        if v is None:
            continue
        tipo = (extra or {}).get(f"{nombre}.tipo") or inp.get(f"restriccion.{nombre}.tipo") or "HARD"
        if tipo not in ("HARD", "SOFT"):
            raise mr.ErrorRiesgo(f"restricción {nombre}: tipo HARD | SOFT")
        pen = mr.num(inp.get(f"restriccion.{nombre}.penalizacion"))
        if tipo == "SOFT" and pen is None:
            raise mr.ErrorRiesgo(f"restricción SOFT {nombre} sin penalización declarada (no se inventa un peso)")
        if "R01" in mr._MUT and nombre in ("CAPITAL_DISPONIBLE", "FONDOS_INICIALES", "PICO_FONDOS"):
            continue
        out.append({"NOMBRE": nombre, "VALOR": float(v), "TIPO": "SOFT" if "R14" in mr._MUT else tipo, "PENALIZACION": pen})
    return out


def valor_restriccion(ficha, nombre, inp):
    met, src = RESTRICCIONES[nombre][0], RESTRICCIONES[nombre][2]
    if nombre == "CAPITAL_DISPONIBLE":
        met = inp.get("capital.metrica") or "PICO_FONDOS"
        return mr.valor_metrica(ficha["ev"], met)
    if src == "met":
        return mr.valor_metrica(ficha["ev"], met)
    if src == "fis":
        g = next((g for g in (ficha["fisico"] or {}).get("gates", []) if g["GATE"] == met), None)
        if "R22" in mr._MUT and ficha["alt"]["tipo"] == ASSET_LIGHT and (g is None or g["REQUERIDO"] is None):
            return 0.0                                  # mutación: un requerimiento DESCONOCIDO se toma como 0
        if g is None:
            return None                                 # sin gate: desconocido (nunca 0)
        return 0.0 if g.get("ESTADO_REQUERIMIENTO") == "NO_REQUERIDO_POR_ARQUITECTURA" else g["REQUERIDO"]
    return ficha.get(met)


def evaluar_restricciones(ficha, restr, inp):
    out = []
    for r in restr:
        nombre, lim = r["NOMBRE"], r["VALOR"]
        sentido = RESTRICCIONES[nombre][1]
        if ficha["alt"]["tipo"] == SQ:
            out.append(dict(r, VALOR_ALTERNATIVA=None, ESTADO="NO_APLICA_STATUS_QUO", VIOLACION_REL=0.0,
                            NOTA="alternativa de decisión, no proyecto productivo: no se le aplican métricas ni restricciones"))
            continue
        v = valor_restriccion(ficha, nombre, inp)
        if nombre == "PAYBACK" and v is None and str(ficha["ev"]["met"].get("PAYBACK_ESTADO")).startswith("NO_RECUPERADO"):
            out.append(dict(r, VALOR_ALTERNATIVA=None, ESTADO="INCUMPLE", VIOLACION_REL=1.0, NOTA="NO_RECUPERADO en el horizonte"))
            continue
        if v is None:
            out.append(dict(r, VALOR_ALTERNATIVA=None, ESTADO="NO_EVALUABLE", VIOLACION_REL=None))
            continue
        ok = v <= lim + 1e-9 if sentido == "<=" else v >= lim - 1e-9
        viol = 0.0 if ok else abs(v - lim) / max(abs(lim), 1e-9)
        out.append(dict(r, VALOR_ALTERNATIVA=v, ESTADO="CUMPLE" if ok else "INCUMPLE", VIOLACION_REL=viol))
    return out


# ---------------------------------------------------------------------------------------------
# 5. FICHAS: evaluación base + factibilidades separadas + comparabilidad
# ---------------------------------------------------------------------------------------------
def firma_comparabilidad(E, alt):
    if alt["tipo"] == SQ:
        return None
    b = E.base(alt)
    if b[0] == "ERROR":
        return None
    P = b[0]
    return {"UNIVERSO": alt["universo"], "HORIZONTE": P["horizonte_anios"], "MODELO_MONETARIO": P["modelo_monetario"],
            "BASE_TASA": P["base_tasa"], "CONVENCION": P["convencion_descuento"], "TIPO_TASA": P["tipo_tasa_descuento"],
            "TASA": P["tasa_descuento"], "MONEDA": mf.MONEDA, "BASE_FLUJO": None,
            "PRODUCTO": (P.get("meta_productos") or {}).get("config_producto", "DECLARADO_EN_CASO"),
            "FISCAL": "AFTER_TAX" if P["impuestos"].get("tasa_ganancias") is not None else "PRE_TAX",
            "OVERRIDE_TOTAL": bool(P.get("override_total"))}


def comparabilidad(fa, ref, cob_max=None):
    """TRUE / FALSE / PARCIAL con motivos. FALSE: no se rankea. PARCIAL: se rankea con la diferencia declarada."""
    if fa["alt"]["tipo"] == SQ:
        return "NO_APLICA", "alternativa de decisión (status quo): fuera de rankings, dominancia y Pareto"
    if "R12" in mr._MUT:
        return "TRUE", ""
    if not fa["completa"]:
        return "FALSE", "faltan bloques económicos (VAN no publicable): " + fa["faltantes_cortos"]
    fs = fa["firma"]
    if ref is None:
        return "FALSE", "sin referencia comparable"
    mot = [f"{k} {fs[k]!r} ≠ {ref[k]!r}" for k in ("UNIVERSO", "HORIZONTE", "MODELO_MONETARIO", "BASE_TASA", "CONVENCION",
                                                     "TIPO_TASA", "TASA", "MONEDA", "BASE_FLUJO", "PRODUCTO", "FISCAL",
                                                     "OVERRIDE_TOTAL")
           if fs.get(k) != ref.get(k)]
    if mot:
        return "FALSE", "; ".join(mot)
    if cob_max is not None and fa["cobertura"] is not None and fa["cobertura"] < cob_max - 1e-12:
        return "PARCIAL", f"cobertura de evidencia {fa['cobertura']:.0%} < {cob_max:.0%} del mejor respaldado (declarado)"
    return "TRUE", ""


def ficha(E, alt, inp, restr):
    ev = E.evaluar(alt, tir=True)
    res = ev["res"]
    f = {"alt": alt, "ev": ev, "id": alt["id"], "completa": ev["met"].get("VAN") is not None,
         "faltantes": res.get("FALTANTES", ev["motivo"]), "firma": firma_comparabilidad(E, alt)}
    if f["firma"] is not None:
        f["firma"]["BASE_FLUJO"] = res.get("BASE_FLUJO")
    bloques = sorted({x.split(":")[0].strip() for x in (f["faltantes"] or "").split("||") if x.strip()})
    f["faltantes_cortos"] = ", ".join(bloques) or ev["motivo"]
    if alt["tipo"] == SQ:
        f["fisico"] = {"ESTADO": NA, "gates": [_gate("STATUS_QUO", 0.0, "—", None, "", estado_req="NO_REQUERIDO_POR_ARQUITECTURA",
                                                     nota="sin inversión: no aplica factibilidad física")]}
    elif alt.get("fisico") is not None:
        f["fisico"] = {"ESTADO": estado_fisico(alt["fisico"]), "gates": alt["fisico"]}
    else:
        f["fisico"] = factibilidad_fisica_real(alt)
    f["cobertura"], f["cobertura_nota"] = cobertura_evidencia(alt) if alt.get("cobertura") is None else alt["cobertura"]
    # factibilidades separadas (no se condensan en un booleano)
    f["F_FISICA"] = f["fisico"]["ESTADO"]
    if alt["tipo"] == SQ:
        f["F_ECONOMICA"] = "NO_APLICA_STATUS_QUO"
    else:
        flt = (res.get("FALTANTES") or "")
        f["F_ECONOMICA"] = ("COSTEABLE" if not re.search(r"(^|\|\| )(CAPEX|OPEX):", flt) and ev["estado"] == "OK"
                            else "NO_COSTEABLE (" + ", ".join(b for b in ("CAPEX", "OPEX") if re.search(rf"(^|\|\| ){b}:", flt)) + ")")
    f["R_CUMPLIMIENTO"] = evaluar_restricciones(f, restr, inp)
    return f


def finalizar_fichas(fichas, inp):
    """Referencia de comparabilidad (firma más frecuente entre las completas), comparabilidad, factibilidad
    financiera, respaldo comercial y semáforo."""
    comp = [f for f in fichas if f["completa"] and f["alt"]["tipo"] != SQ and f["firma"]]
    ref = None
    if comp:
        cnt = {}
        for f in comp:
            k = json.dumps(f["firma"], sort_keys=True, default=str)
            cnt[k] = cnt.get(k, 0) + 1
        ref = json.loads(sorted(cnt.items(), key=lambda x: (-x[1], x[0]))[0][0])
    cobs = [f["cobertura"] for f in comp if f["cobertura"] is not None]
    cob_max = max(cobs) if cobs else None
    for f in fichas:
        f["COMPARABILIDAD"], f["COMPARABILIDAD_MOTIVO"] = comparabilidad(f, ref, cob_max)
        rc = f["R_CUMPLIMIENTO"]
        hard = [r for r in rc if r["TIPO"] == "HARD"]
        f["HARD_INCUMPLE"] = [r["NOMBRE"] for r in hard if r["ESTADO"] == "INCUMPLE"]
        f["HARD_PENDIENTE"] = [r["NOMBRE"] for r in hard if r["ESTADO"] == "NO_EVALUABLE"]
        f["SOFT_PENALIZACION"] = sum((r["PENALIZACION"] or 0) * (r["VIOLACION_REL"] or 0) for r in rc
                                     if r["TIPO"] == "SOFT" and r["ESTADO"] == "INCUMPLE")
        fin_r = [r for r in hard if r["NOMBRE"] in ("CAPITAL_DISPONIBLE", "FONDOS_INICIALES", "PICO_FONDOS", "DSCR", "DEUDA")]
        if f["alt"]["tipo"] == SQ:
            f["F_FINANCIERA"] = "NO_APLICA_STATUS_QUO"
        elif not f["completa"]:
            f["F_FINANCIERA"] = "NO_EVALUABLE (flujo no publicable)"
        elif any(r["ESTADO"] == "INCUMPLE" for r in fin_r):
            f["F_FINANCIERA"] = "NO (" + ", ".join(r["NOMBRE"] for r in fin_r if r["ESTADO"] == "INCUMPLE") + ")"
        elif not fin_r:
            f["F_FINANCIERA"] = "SIN_RESTRICCION_FINANCIERA_DECLARADA"
        else:
            f["F_FINANCIERA"] = "SÍ" if all(r["ESTADO"] == "CUMPLE" for r in fin_r) else "PENDIENTE"
        da = f["ev"]["met"].get("DEMANDA_ASEGURADA_PCT")
        if f["alt"]["tipo"] == SQ:
            f["R_COMERCIAL"] = "NO_APLICA_STATUS_QUO"
        elif da is None:
            f["R_COMERCIAL"] = "NO_EVALUABLE"
        elif da <= 1e-12:
            f["R_COMERCIAL"] = "NO_RESPALDADO (0 % de la capacidad con demanda DOCUMENTADA/ASEGURADA)"
        else:
            f["R_COMERCIAL"] = f"PARCIAL ({da:.0%} de la capacidad con demanda DOCUMENTADA/ASEGURADA)" if da < 1 - 1e-9 else "RESPALDADO"
        evaluable = f["COMPARABILIDAD"] not in ("FALSE", "NO_APLICA") and f["ev"]["estado"] == "OK"
        if not evaluable:
            f["SEMAFORO"] = "GRIS"
        elif f["HARD_INCUMPLE"] or f["F_FISICA"] == NO_FACTIBLE:
            f["SEMAFORO"] = "ROJO"
        elif f["cobertura"] == 1.0 and f["F_FISICA"] == FACTIBLE and not f["HARD_PENDIENTE"]:
            f["SEMAFORO"] = "VERDE"
        else:
            f["SEMAFORO"] = "AMARILLO"
    return ref


def rankeable(f, inp):
    """Condiciones para entrar a un ranking (todas; las razones de exclusión se informan)."""
    mot = []
    if f["alt"]["tipo"] == SQ and "R24" not in mr._MUT:
        return ["STATUS_QUO: alternativa de decisión, no proyecto productivo (ver DECISION_ESCENARIO / REGLAS_STATUS_QUO)"]
    if f["COMPARABILIDAD"] == "FALSE":
        mot.append("NO_COMPARABLE: " + f["COMPARABILIDAD_MOTIVO"])
    if f["F_FISICA"] == NO_FACTIBLE:
        mot.append("FISICAMENTE_NO_FACTIBLE")
    if f["HARD_INCUMPLE"]:
        mot.append("INCUMPLE_HARD: " + ", ".join(f["HARD_INCUMPLE"]))
    if f["HARD_PENDIENTE"] and inp.get("optimizador.hard_pendiente_excluye") is not False:
        mot.append("HARD_NO_EVALUABLE: " + ", ".join(f["HARD_PENDIENTE"]))
    if f["F_FISICA"] == PEND and inp.get("optimizador.exigir_fisico_confirmado") is True and f["alt"]["tipo"] != SQ:
        mot.append("FACTIBILIDAD_FISICA_PENDIENTE (exigida por el usuario)")
    return mot


# ---------------------------------------------------------------------------------------------
# 6. ROBUSTEZ (comportamiento en VARIOS escenarios, no una rentabilidad base)
# ---------------------------------------------------------------------------------------------
def escenarios_robustez(inp, stresses):
    """Conjunto de escenarios de robustez: stress activos con magnitudes declaradas + extremos (mín y máx) de los
    shocks one-way de las variables de `robustez.variables`. NO es una muestra probabilística."""
    out = []
    for st in stresses:
        if st["activo"] and not st["pendientes"]:
            out.append((f"STRESS:{st['ID_STRESS']}", dict(st["shocks"])))
    for v in mr.como_lista(inp.get("robustez.variables")):
        xs = [x for x in mr.shocks_de(v, inp) if x != 0]
        if xs and mr.VARIABLES[v]["SOPORTE"] not in ("DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"):
            out.append((f"ONEWAY:{v}:{min(xs):g}", {v: min(xs)}))
            out.append((f"ONEWAY:{v}:{max(xs):g}", {v: max(xs)}))
    return out


def robustez(E, fichas, inp, restr, escenarios):
    crit = inp.get("robustez.criterio") or "PCT_VAN_NO_NEGATIVO"
    nmin = int(inp.get("robustez.min_escenarios") or 3)
    for f in fichas:
        f["ESC"] = {}
        r = {"N_ESCENARIOS": 0, "CRITERIO": crit, "MIN_ESCENARIOS": nmin}
        if f["alt"]["tipo"] == SQ:
            f["ROB"] = dict(r, ESTADO="NO_APLICA_STATUS_QUO", NOTA="alternativa de decisión: no se le mide robustez financiera")
            f["ROBUSTEZ"] = None
            continue
        if not f["completa"]:
            f["ROB"] = dict(r, ESTADO="PENDIENTE", NOTA="alternativa no evaluable")
            f["ROBUSTEZ"] = None
            continue
        vans, picos, pbs, nrec, cumple = [], [], [], 0, 0
        for sid, sh in escenarios:
            ev = E.evaluar(f["alt"], sh)
            f["ESC"][sid] = ev
            if ev["estado"] not in ("OK", "STATUS_QUO"):
                continue
            m = ev["met"]
            if m.get("VAN") is not None:
                vans.append(m["VAN"])
            if m.get("PICO_FONDOS") is not None:
                picos.append(m["PICO_FONDOS"])
            if m.get("PAYBACK") is not None:
                pbs.append(m["PAYBACK"])
            elif str(m.get("PAYBACK_ESTADO")).startswith("NO_RECUPERADO"):
                nrec += 1
            pseudo = {"alt": f["alt"], "ev": ev, "fisico": f["fisico"], "SCORE_ORDINAL_RIESGO": f.get("SCORE_ORDINAL_RIESGO")}
            rc = evaluar_restricciones(pseudo, [x for x in restr if x["TIPO"] == "HARD"], inp)
            cumple += all(x["ESTADO"] in ("CUMPLE", "NO_APLICA_STATUS_QUO") for x in rc)
        n = len(vans)
        r.update(N_ESCENARIOS=n, PCT_VAN_NO_NEGATIVO=(sum(1 for x in vans if x >= 0) / n) if n else None,
                 PEOR_VAN=min(vans) if vans else None, P10_VAN=mr.percentil(vans, 0.10) if vans else None,
                 MAX_PICO_FONDOS=max(picos) if picos else None, MAX_PAYBACK=max(pbs) if pbs else None,
                 N_NO_RECUPERADO=nrec, PCT_CUMPLE_HARD=(cumple / len(escenarios)) if escenarios else None,
                 NOTA="escenarios deterministas de stress y extremos one-way (no probabilísticos)")
        if n < nmin:
            r.update(ESTADO="PENDIENTE", NOTA=f"{n} escenarios evaluables (sin contar la base) < mínimo {nmin}: "
                     "un resultado base no es robustez")
            f["ROBUSTEZ"] = None
        else:
            r["ESTADO"] = "CALCULADA"
            f["ROBUSTEZ"] = {"PCT_VAN_NO_NEGATIVO": r["PCT_VAN_NO_NEGATIVO"], "PEOR_VAN": r["PEOR_VAN"],
                             "P10_VAN": r["P10_VAN"]}.get(crit)
        f["ROB"] = r


# ---------------------------------------------------------------------------------------------
# 7. SCORE DE RIESGO (operativo, para ordenar; NO es una probabilidad)
# ---------------------------------------------------------------------------------------------
COMPONENTES_RIESGO = ("VAN_NEGATIVO_ESCENARIOS", "SENSIBILIDAD_VAN", "PICO_FONDOS_RELATIVO", "DEMANDA_NO_RESPALDADA",
                      "FISICO_PENDIENTE", "EVIDENCIA_FALTANTE")


def score_riesgo(fichas, inp, swing_van):
    """Score ∈ [0, 1] (más alto = más riesgo) = Σ w_i·c_i / Σ w_i con pesos de inputs (sin pesos → PENDIENTE).
    Componentes ∈ [0, 1]; PICO_FONDOS_RELATIVO se normaliza min–max dentro del conjunto (relativo, no absoluto).
    Faltante: SEPARAR (score PENDIENTE para esa alternativa) o PENALIZAR (componente = 1). Documentado en
    robustez.md §2."""
    pesos = {c: mr.num(inp.get(f"riesgo.peso.{c}")) for c in COMPONENTES_RIESGO}
    pesos = {c: w for c, w in pesos.items() if w}
    trat = inp.get("riesgo.faltantes") or "SEPARAR"
    picos = [f["ev"]["met"]["PICO_FONDOS"] for f in fichas if f["completa"] and f["alt"]["tipo"] != SQ
             and f["ev"]["met"].get("PICO_FONDOS") is not None]
    lo, hi = (min(picos), max(picos)) if picos else (None, None)
    for f in fichas:
        m = f["ev"]["met"]
        if f["alt"]["tipo"] == SQ:
            f["SCORE_ORDINAL_RIESGO"], f["RIESGO_COMP"], f["RIESGO_NOTA"] = None, {}, "NO_APLICA (status quo; el riesgo de no actuar no se modela)"
            continue
        c = {}
        c["VAN_NEGATIVO_ESCENARIOS"] = (1 - f["ROB"]["PCT_VAN_NO_NEGATIVO"]) if f.get("ROB", {}).get("PCT_VAN_NO_NEGATIVO") is not None else None
        sw, van = swing_van.get(f["id"]), m.get("VAN")
        c["SENSIBILIDAD_VAN"] = (sw / (abs(van) + sw)) if (sw is not None and van is not None and abs(van) + sw > 0) else None
        c["PICO_FONDOS_RELATIVO"] = (((m["PICO_FONDOS"] - lo) / (hi - lo)) if hi > lo else 0.0) if (m.get("PICO_FONDOS") is not None and lo is not None) else None
        da = m.get("DEMANDA_ASEGURADA_PCT")
        c["DEMANDA_NO_RESPALDADA"] = None if da is None else 1 - min(1.0, da)
        gs = [g for g in f["fisico"]["gates"]]
        c["FISICO_PENDIENTE"] = (sum(1 for g in gs if g["ESTADO"] == PEND) / len(gs)) if gs else None
        c["EVIDENCIA_FALTANTE"] = None if f["cobertura"] is None else 1 - f["cobertura"]
        f["RIESGO_COMP"] = c
        if not pesos:
            f["SCORE_ORDINAL_RIESGO"], f["RIESGO_NOTA"] = None, "PENDIENTE: pesos del score de riesgo no definidos (inputs riesgo.peso.*)"
            continue
        falt = [k for k in pesos if c.get(k) is None]
        if falt and trat == "SEPARAR":
            f["SCORE_ORDINAL_RIESGO"], f["RIESGO_NOTA"] = None, "PENDIENTE: componentes sin dato (separados): " + ", ".join(falt)
            continue
        val = {k: (1.0 if c.get(k) is None else c[k]) for k in pesos}
        f["SCORE_ORDINAL_RIESGO"] = sum(pesos[k] * val[k] for k in pesos) / sum(pesos.values())
        f["RIESGO_NOTA"] = ("SCORE_ORDINAL_RIESGO: orden interno relativo al conjunto; NO ES PROBABILIDAD" +
                            (f"; penalizados como 1: {', '.join(falt)}" if falt else ""))


# ---------------------------------------------------------------------------------------------
# 8. OBJETIVOS, RANKING, SEGUNDA ALTERNATIVA
# ---------------------------------------------------------------------------------------------
OBJETIVOS = {"MAX_VAN": ("VAN", 1), "MAX_TIR": ("TIR", 1), "MIN_PAYBACK": ("PAYBACK", -1),
             "MIN_FONDOS_INICIALES": ("FONDOS_INICIALES", -1), "MIN_CAPEX": ("CAPEX", -1),
             "MIN_PICO_FONDOS": ("PICO_FONDOS", -1), "MAX_EBITDA": ("EBITDA", 1), "MAX_DSCR": ("DSCR", 1),
             "MIN_RIESGO": ("SCORE_ORDINAL_RIESGO", -1), "MAX_ROBUSTEZ": ("ROBUSTEZ", 1),
             "MAX_CRECIMIENTO": ("CAPACIDAD_FINAL_AVES_DIA", 1), "BALANCEADO": ("SCORE_BALANCEADO", 1)}
# NO_INVERTIR_AUN no compite en ningún ranking (no es un proyecto productivo). Gana la DECISION_ESCENARIO solo por estas
# reglas explícitas, evaluadas después del ranking de inversiones (las 3 últimas se activan con un input del usuario):
REGLAS_STATUS_QUO = {
    "SQ-1": "NINGUNA_INVERSION_FACTIBLE: ninguna inversión cumple las condiciones de ranking",
    "SQ-2": "RESTRICCION_DE_CAPITAL: el capital declarado excluye a todas las inversiones restantes",
    "SQ-3": "VALOR_NEGATIVO: la mejor inversión tiene VAN < 0 en el escenario (no crea valor)",
    "SQ-4": "STRESS: la mejor inversión tiene VAN < 0 en un stress declarado en decision.sq_stress",
    "SQ-5": "RIESGO: SCORE_ORDINAL_RIESGO de la mejor > decision.sq_score_ordinal_max",
    "SQ-6": "EVIDENCIA: cobertura de evidencia de la mejor < decision.sq_cobertura_min",
}
COMP_BAL = {"rentabilidad": ("VAN", 1), "riesgo": ("SCORE_ORDINAL_RIESGO", -1), "capital": ("FONDOS_INICIALES", -1),
            "liquidez": ("PICO_FONDOS", -1), "crecimiento": ("CAPACIDAD_FINAL_AVES_DIA", 1), "robustez": ("ROBUSTEZ", 1)}


def valor_obj(f, metrica):
    if metrica in ("SCORE_ORDINAL_RIESGO", "ROBUSTEZ", "SCORE_BALANCEADO"):
        v = f.get(metrica)
        return 0.0 if (v is None and "R03" in mr._MUT) else v
    return mr.valor_metrica(f["ev"], metrica)


def pesos_balanceado(inp):
    w = {c: mr.num(inp.get(f"balanceado.peso.{c}")) for c in COMP_BAL}
    w = {c: x for c, x in w.items() if x}
    origen = "USUARIO"
    if not w and inp.get("balanceado.preset") == "IGUALES":
        w, origen = {c: 1.0 for c in COMP_BAL}, "PRESET_IGUALES [SUPUESTO] SUP-219"
    if not w:
        return None, "PESOS_NO_DEFINIDOS"
    s = sum(w.values())
    return {c: x / s for c, x in w.items()}, origen


def _norm(vals, signo):
    xs = [v for v in vals.values() if v is not None]
    if not xs:
        return {}
    lo, hi = min(xs), max(xs)
    return {k: (1.0 if hi == lo else ((v - lo) / (hi - lo) if signo > 0 else (hi - v) / (hi - lo)))
            for k, v in vals.items() if v is not None}


def score_balanceado(cands, inp):
    w, origen = pesos_balanceado(inp)
    if w is None:
        for f in cands:
            f["SCORE_BALANCEADO"] = None
        return origen
    trat = inp.get("balanceado.faltantes") or "SEPARAR"
    norm = {c: _norm({f["id"]: valor_obj(f, COMP_BAL[c][0]) for f in cands}, COMP_BAL[c][1]) for c in w}
    for f in cands:
        falt = [c for c in w if f["id"] not in norm[c]]
        if falt and trat == "SEPARAR":
            f["SCORE_BALANCEADO"], f["BAL_NOTA"] = None, "componentes sin dato (separados): " + ", ".join(falt)
            continue
        f["SCORE_BALANCEADO"] = sum(w[c] * norm[c].get(f["id"], 0.0) for c in w)
        f["BAL_NOTA"] = f"pesos {origen}: " + ", ".join(f"{c} {x:.2f}" for c, x in w.items())
    return origen


def rankear(fichas, objetivo, inp):
    """Ranking dentro del universo y del conjunto rankeable. SCORE = valor normalizado (0–1, mejor = 1) − penalizaciones
    SOFT. Devuelve (filas por alternativa, decisión)."""
    if "R04" in mr._MUT:
        objetivo_eval = "MAX_VAN"
    else:
        objetivo_eval = objetivo
    metrica, signo = OBJETIVOS[objetivo_eval]
    filas, cands = {}, []
    for f in fichas:
        fila = {"RANK": None, "SCORE": None, "MOTIVO": ""}
        mot = rankeable(f, inp)
        if not mot:
            if objetivo_eval == "BALANCEADO":
                cands.append(f)
                continue
            v = valor_obj(f, metrica)
            if v is None:
                if metrica == "PAYBACK" and str(f["ev"]["met"].get("PAYBACK_ESTADO")).startswith("NO_RECUPERADO"):
                    mot.append("NO_RECUPERADO_EN_HORIZONTE")
                elif metrica == "TIR":
                    mot.append("TIR no definida: " + str(f["ev"]["met"].get("TIR_ESTADO")))
                else:
                    mot.append(f"{metrica} no disponible")
            else:
                cands.append(f)
        fila["MOTIVO"] = "; ".join(mot)
        filas[f["id"]] = fila
    origen_bal = ""
    if objetivo_eval == "BALANCEADO":
        origen_bal = score_balanceado(cands, inp)
        for f in list(cands):
            if f.get("SCORE_BALANCEADO") is None:
                filas[f["id"]] = {"RANK": None, "SCORE": None,
                                  "MOTIVO": origen_bal if origen_bal == "PESOS_NO_DEFINIDOS" else f.get("BAL_NOTA", "")}
                cands.remove(f)
    vals = {f["id"]: valor_obj(f, metrica) for f in cands}
    nrm = _norm(vals, signo)
    for f in cands:
        sc = nrm[f["id"]] - f["SOFT_PENALIZACION"]
        filas[f["id"]] = {"RANK": None, "SCORE": sc, "VALOR_OBJETIVO": vals[f["id"]],
                          "MOTIVO": "penalización SOFT %.4f" % f["SOFT_PENALIZACION"] if f["SOFT_PENALIZACION"] else ""}
    orden = sorted(cands, key=lambda f: ((1 if "R20" in mr._MUT else -1) * filas[f["id"]]["SCORE"], f["id"]))
    for i, f in enumerate(orden, 1):
        filas[f["id"]]["RANK"] = i
    inv = [f for f in orden if f["alt"]["tipo"] != SQ]
    dec = {"OBJETIVO": objetivo, "METRICA": metrica, "SENTIDO": "MAX" if signo > 0 else "MIN",
           "N_EVALUADAS": len(fichas), "N_RANKEADAS": len(orden), "PESOS_BALANCEADO": origen_bal}
    if not inv:
        excl = {}
        for f in fichas:
            if f["alt"]["tipo"] == SQ:
                continue
            k = (filas[f["id"]]["MOTIVO"] or "?").split(":")[0]
            excl[k] = excl.get(k, 0) + 1
        cap = any("CAPITAL_DISPONIBLE" in (filas[f["id"]]["MOTIVO"] or "") for f in fichas if f["alt"]["tipo"] != SQ)
        reglas = ["SQ-1"] + (["SQ-2"] if cap else [])
        dec.update(ESTADO=NINGUNA, MEJOR="—", SEGUNDA="—", DECISION_ESCENARIO=SQ if any(f["alt"]["tipo"] == SQ for f in fichas) else "—",
                   REGLA_STATUS_QUO="; ".join(f"{r} {REGLAS_STATUS_QUO[r]}" for r in reglas),
                   POR_QUE="ninguna configuración de inversión cumple las condiciones: " +
                   "; ".join(f"{k} ({n})" for k, n in sorted(excl.items(), key=lambda x: -x[1])),
                   NOTA="no se elige 'la menos mala'; NO_INVERTIR_AUN es la ausencia de inversión, no una recomendación de planta")
        return filas, dec, orden
    best = orden[0]
    dec.update(ESTADO="MEJOR_EN_ESCENARIO", MEJOR=best["id"], VALOR_MEJOR=vals[best["id"]], SCORE_MEJOR=filas[best["id"]]["SCORE"])
    if len(orden) > 1:
        sec = orden[1]
        dec.update(SEGUNDA=sec["id"], VALOR_SEGUNDA=vals[sec["id"]], SCORE_SEGUNDA=filas[sec["id"]]["SCORE"],
                   DIFERENCIA_VALOR=vals[best["id"]] - vals[sec["id"]],
                   DIFERENCIA_SCORE=filas[best["id"]]["SCORE"] - filas[sec["id"]]["SCORE"])
        tol = mr.num(inp.get("decision.tolerancia_equivalencia"))
        den = max(abs(vals[best["id"]]), abs(vals[sec["id"]]), 1e-9)
        if tol is not None and abs(dec["DIFERENCIA_VALOR"]) / den <= tol:
            dec["ROBUSTEZ_DECISION"] = f"{NO_ROB}: diferencia relativa {abs(dec['DIFERENCIA_VALOR']) / den:.2%} ≤ tolerancia {tol:.2%}"
        if dec["DIFERENCIA_SCORE"] == 0:
            dec["ROBUSTEZ_DECISION"] = f"{NO_ROB}: empate"
    else:
        dec.update(SEGUNDA="—", NOTA="una sola alternativa rankeable")
    decidir_status_quo(dec, best, inp)
    return filas, dec, orden


def decidir_status_quo(dec, best, inp):
    """DECISION_ESCENARIO = mejor inversión o NO_INVERTIR_AUN según REGLAS_STATUS_QUO (nunca por comparar contra ceros)."""
    m = best["ev"]["met"]
    reglas, posibles = [], []
    if m.get("VAN") is not None and m["VAN"] < 0:
        reglas.append("SQ-3")
    stress_ids = [str(x) for x in mr.como_lista(inp.get("decision.sq_stress"))]
    neg = [sid for sid, ev in (best.get("ESC") or {}).items() if sid.startswith("STRESS:")
           and ev["met"].get("VAN") is not None and ev["met"]["VAN"] < 0]
    if [x for x in neg if x.split(":", 1)[1] in stress_ids]:
        reglas.append("SQ-4")
    smax = mr.num(inp.get("decision.sq_score_ordinal_max"))
    if smax is not None and best.get("SCORE_ORDINAL_RIESGO") is not None and best["SCORE_ORDINAL_RIESGO"] > smax:
        reglas.append("SQ-5")
    cmin = mr.num(inp.get("decision.sq_cobertura_min"))
    if cmin is not None and best.get("cobertura") is not None and best["cobertura"] < cmin:
        reglas.append("SQ-6")
    if neg:
        posibles.append("VAN < 0 de la mejor en " + ", ".join(neg) + " (SQ-4 si se declara ese stress)")
    if best.get("cobertura") is not None and best["cobertura"] < 1:
        posibles.append(f"cobertura de evidencia {best['cobertura']:.0%} (SQ-6 si se declara un mínimo)")
    if m.get("VAN") is not None and m["VAN"] < 0:
        posibles.append("VAN base < 0 (SQ-3)")
    dec["DECISION_ESCENARIO"] = SQ if reglas else best["id"]
    dec["REGLA_STATUS_QUO"] = "; ".join(f"{r} {REGLAS_STATUS_QUO[r]}" for r in reglas) or "ninguna regla de status quo se cumple"
    dec["POR_QUE_NO_INVERTIR_PODRIA_GANAR"] = "; ".join(posibles) or "con los datos del escenario, ninguna condición explícita"


def estabilidad_ganador(fichas_orden, dec, objetivo, escenarios):
    """¿El ganador sigue primero en cada escenario de robustez? (solo objetivos sobre métricas del motor)."""
    metrica, signo = OBJETIVOS[objetivo]
    if metrica in ("SCORE_ORDINAL_RIESGO", "ROBUSTEZ", "SCORE_BALANCEADO", "TIR") or len(fichas_orden) < 2 or not escenarios:
        return None, []
    cambios, n = [], 0
    for sid, _ in escenarios:
        vals = {}
        for f in fichas_orden:
            ev = f["ESC"].get(sid)
            if ev is None or ev["estado"] not in ("OK", "STATUS_QUO"):
                continue
            v = mr.valor_metrica(ev, metrica)
            if v is not None:
                vals[f["id"]] = v
        if dec["MEJOR"] not in vals or len(vals) < 2:
            continue
        n += 1
        g = max(vals, key=lambda k: (signo * vals[k], k == dec["MEJOR"]))
        if g != dec["MEJOR"]:
            cambios.append(f"{sid} → {g}")
    return (1 - len(cambios) / n) if n else None, cambios


# ---------------------------------------------------------------------------------------------
# 9. DOMINANCIA Y PARETO (no eliminan: marcan)
# ---------------------------------------------------------------------------------------------
def _parse_dims(txt):
    out = []
    for d in mr.como_lista(txt):
        m, s = str(d).split(":")
        out.append((m, 1 if s == "+" else -1))
    return out


PARETO_NI = "PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE"


def _comparables(fichas):
    """Solo alternativas de inversión comparables (TRUE / PARCIAL). COMPARABILIDAD FALSE (faltan bloques o distinta
    base) y el status quo (NO_APLICA) no participan en dominancia, Pareto ni rankings: sus faltantes jamás valen 0."""
    if "R27" in mr._MUT:
        return [f for f in fichas if f["alt"]["tipo"] != SQ]
    return [f for f in fichas if f["COMPARABILIDAD"] in ("TRUE", "PARCIAL")]


def dominancia(fichas, inp):
    dims = _parse_dims(inp.get("dominancia.dimensiones") or "FONDOS_INICIALES:-|VAN:+|SCORE_ORDINAL_RIESGO:-")
    cand = _comparables(fichas)
    for f in fichas:
        f["DOMINADA_POR"], f["DOM_DIMS"] = [], ""
        f["DOM_ESTADO"] = ("EVALUADA" if f in cand else
                           "NO_APLICA_STATUS_QUO" if f["alt"]["tipo"] == SQ else "NO_EVALUABLE (COMPARABILIDAD FALSE)")
    for b in cand:
        for a in cand:
            if a is b:
                continue
            usadas = [(m, s) for m, s in dims if valor_obj(a, m) is not None and valor_obj(b, m) is not None]
            if len(usadas) < 2:
                continue
            ge = all(s * valor_obj(a, m) >= s * valor_obj(b, m) - 1e-9 for m, s in usadas)
            gt = any(s * valor_obj(a, m) > s * valor_obj(b, m) + 1e-9 for m, s in usadas)
            if ge and (gt or "R15" in mr._MUT):
                b["DOMINADA_POR"].append(a["id"])
                b["DOM_DIMS"] = ", ".join(m for m, _ in usadas)
    return dims


def pareto(fichas, inp):
    """Frontera por par de ejes entre alternativas COMPARABLES. Con menos de 2 puntos comparables el par se marca
    PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE (no se presenta una 'frontera' trivial). Las no comparables quedan
    visibles como NO_EVALUABLE; el status quo no participa."""
    pares = []
    for p in mr.como_lista(inp.get("pareto.pares") or "VAN:+×FONDOS_INICIALES:-"):
        x, y = str(p).split("×")
        pares.append((_parse_dims(x)[0], _parse_dims(y)[0]))
    filas = []
    cand = _comparables(fichas)
    for (mx, sx), (my, sy) in pares:
        pts = [(f, valor_obj(f, mx), valor_obj(f, my)) for f in cand]
        pts = [p for p in pts if p[1] is not None and p[2] is not None]
        insuf = len(pts) < 2
        en_pts = {p[0]["id"] for p in pts}
        for f, vx, vy in pts:
            dom = [g["id"] for g, wx, wy in pts if g is not f and sx * wx >= sx * vx - 1e-9 and sy * wy >= sy * vy - 1e-9
                   and (sx * wx > sx * vx + 1e-9 or sy * wy > sy * vy + 1e-9)]
            frontera = (not dom) if "R20" not in mr._MUT else bool(dom)
            filas.append({"PAR": f"{mx}×{my}", "ALTERNATIVA": f["id"], "TIPO": f["alt"]["tipo"], "UNIVERSO": f["alt"]["universo"],
                          "EJE_X": mx, "VALOR_X": vx, "EJE_Y": my, "VALOR_Y": vy,
                          "EN_FRONTERA": PARETO_NI if insuf else frontera, "DOMINADA_EN_PAR_POR": ", ".join(dom),
                          "N_PUNTOS_COMPARABLES": len(pts), "CUMPLE_HARD": not f["HARD_INCUMPLE"],
                          "ETIQUETA": etiqueta(f["alt"]["universo"]),
                          "NOTA": (f"{PARETO_NI}: menos de 2 alternativas comparables con ambos ejes" if insuf else
                                   "la frontera no es un ranking: muestra el compromiso entre ejes")})
        for f in fichas:
            if f["alt"]["tipo"] == SQ or f["id"] in en_pts:
                continue
            filas.append({"PAR": f"{mx}×{my}", "ALTERNATIVA": f["id"], "TIPO": f["alt"]["tipo"], "UNIVERSO": f["alt"]["universo"],
                          "EJE_X": mx, "EJE_Y": my, "EN_FRONTERA": "NO_EVALUABLE", "N_PUNTOS_COMPARABLES": len(pts),
                          "ETIQUETA": etiqueta(f["alt"]["universo"]),
                          "NOTA": (f["COMPARABILIDAD_MOTIVO"] if f["COMPARABILIDAD"] == "FALSE" else "eje sin valor publicable")})
    return filas


def etiqueta(universo):
    if "R21" in mr._MUT:
        return "RESULTADO"                              # mutación: se elimina la etiqueta de simulación
    return {"EVIDENCIA": "MODO_EVIDENCIA", "ESCENARIO": mr.ETIQ_SIM, "ARTIFICIAL_TEST": mr.ETIQ_ART}[universo]


def ambito(universo):
    """PROYECTO (evidencia o escenario del proyecto) vs ARTIFICIAL_TEST (casos de prueba inventados)."""
    return "ARTIFICIAL_TEST" if universo == "ARTIFICIAL_TEST" else "PROYECTO"


# ---------------------------------------------------------------------------------------------
# 10. CONSULTAS: capital, demanda, payback (inputs del usuario; nada se asume)
# ---------------------------------------------------------------------------------------------
def reaplicar_restricciones(fichas, restr, inp):
    for f in fichas:
        f["R_CUMPLIMIENTO"] = evaluar_restricciones(f, restr, inp)
    finalizar_fichas(fichas, inp)


def limitacion_principal(f):
    if f["alt"]["tipo"] == SQ:
        return "—"
    if f["F_FISICA"] == NO_FACTIBLE:
        return "GATE_FISICO: " + ", ".join(g["GATE"] for g in f["fisico"]["gates"] if g["ESTADO"] == NO_FACTIBLE)
    inc = [r for r in f["R_CUMPLIMIENTO"] if r["TIPO"] == "HARD" and r["ESTADO"] == "INCUMPLE"]
    if inc:
        r = max(inc, key=lambda x: x["VIOLACION_REL"] or 0)
        return f"RESTRICCION_HARD: {r['NOMBRE']} ({r['VALOR_ALTERNATIVA']} vs {r['VALOR']})"
    if not f["completa"]:
        return "DATOS_FALTANTES: " + f["faltantes_cortos"]
    if f["HARD_PENDIENTE"]:
        return "RESTRICCION_NO_EVALUABLE: " + ", ".join(f["HARD_PENDIENTE"])
    pend = [g["GATE"] for g in f["fisico"]["gates"] if g["ESTADO"] == PEND]
    if pend:
        return "FACTIBILIDAD_FISICA_PENDIENTE: " + ", ".join(pend)
    if f["cobertura"] is not None and f["cobertura"] < 1:
        return "EVIDENCIA_INSUFICIENTE: " + f["cobertura_nota"]
    return "—"


def consulta_capital(fichas, X, inp, objetivos):
    """«Tengo X de capital.» X es input; jamás se asume USD 2 M."""
    if X is None:
        return [{"ESTADO": "SIN_CONSULTA", "NOTA": "capital no declarado (consulta.capital_usd vacío); no se asume USD 2 M"}], []
    inp2 = dict(inp)
    inp2["restriccion.CAPITAL_DISPONIBLE.valor"], inp2["restriccion.CAPITAL_DISPONIBLE.tipo"] = X, "HARD"
    fs = [dict(f) for f in fichas]
    restr = leer_restricciones(inp2)
    reaplicar_restricciones(fs, restr, inp2)
    met = inp.get("capital.metrica") or "PICO_FONDOS"
    filas = []
    for f in fs:
        req = valor_restriccion(f, "CAPITAL_DISPONIBLE", inp2)
        rc = next((r for r in f["R_CUMPLIMIENTO"] if r["NOMBRE"] == "CAPITAL_DISPONIBLE"), None)
        est = rc["ESTADO"] if rc else "NO_EVALUABLE"
        filas.append({"ALTERNATIVA": f["id"], "UNIVERSO": f["alt"]["universo"], "CAPITAL_DECLARADO": X, "METRICA_CAPITAL": met,
                      "CAPITAL_REQUERIDO": req, "CUMPLE_CAPITAL": est,
                      "CAPITAL_FALTANTE": (max(0.0, req - X) if req is not None else None),
                      "FACTIBLE_TOTAL": "SÍ" if not rankeable(f, inp2) else "NO",
                      "PRINCIPAL_RESTRICCION": limitacion_principal(f), "ETIQUETA": etiqueta(f["alt"]["universo"])})
    decs = []
    for o in objetivos:
        _, dec, _ = rankear(fs, o, inp2)
        decs.append(dict(dec, CONSULTA=f"capital {X:,.0f} ({met})"))
    return filas, decs


def _demanda_base_t_dia(P):
    tot = 0.0
    for l in mf._lineas_contables(P) if P.get("demanda") else []:
        q = l["kg_mes"]
        q = q["por_anio"].get(1) if isinstance(q, dict) else (sum(q) / len(q) if isinstance(q, list) else q)
        if q is None:
            return None
        if l["categoria"] == "NEGOCIADA":
            q *= P["alfa_negociada"] or 0.0
        tot += q
    return tot / mf.DIAS_MES / 1000 if tot else None


def consulta_demanda(E, fichas, X, inp):
    """«Tengo X t/día de demanda asegurada.» Escala compatible, utilización, capacidad ociosa, demanda faltante."""
    if X is None:
        return [{"ESTADO": "SIN_CONSULTA", "UNIVERSO": fichas[0]["alt"]["universo"] if fichas else "",
                 "NOTA": "demanda asegurada no declarada (consulta.demanda_t_dia vacío)"}], {}
    filas = []
    for f in fichas:
        if f["alt"]["tipo"] == SQ or not f["completa"]:
            continue
        P = E.base(f["alt"])[0]
        D = _demanda_base_t_dia(P)
        if D is None:
            filas.append({"ALTERNATIVA": f["id"], "ESTADO": NO_CALC_D, "NOTA": "demanda base no cuantificable"})
            continue
        s = X / D - 1
        ev = E.evaluar(f["alt"], {"demanda": s})
        m = ev["met"]
        pq = mr.punto_quiebre(E, f["alt"], "demanda", "VAN", 0.0, (-0.99, 5.0), 30)
        dmin = D * (1 + pq["SHOCK_QUIEBRE"]) if pq.get("ESTADO") == "ENCONTRADO" else None
        cap = (m.get("CAPACIDAD_KG_DIA") or 0) / 1000 if m.get("CAPACIDAD_KG_DIA") else None
        filas.append({"ALTERNATIVA": f["id"], "TIPO": f["alt"]["tipo"], "UNIVERSO": f["alt"]["universo"], "DEMANDA_DECLARADA_T_DIA": X,
                      "DEMANDA_BASE_ESCENARIO_T_DIA": D, "ESTADO": ev["estado"], "CAPACIDAD_T_DIA": cap,
                      "RATIO_CAPACIDAD_DEMANDA": (cap / X) if (cap and X) else None,
                      "UTILIZACION": m.get("UTILIZACION"), "CAPACIDAD_OCIOSA": (1 - m["UTILIZACION"]) if m.get("UTILIZACION") is not None else None,
                      "BREAK_EVEN_U": m.get("BREAK_EVEN_U"), "VAN_CON_DEMANDA_DECLARADA": m.get("VAN"),
                      "DEMANDA_MINIMA_VAN0_T_DIA": dmin, "ESTADO_DEMANDA_MINIMA": pq.get("ESTADO"),
                      "DEMANDA_FALTANTE_T_DIA": max(0.0, dmin - X) if dmin is not None else None,
                      "SOBREDIMENSIONAMIENTO": ("UTILIZACION_BAJO_BREAK_EVEN" if (m.get("UTILIZACION") is not None and m.get("BREAK_EVEN_U") is not None
                                                and m["UTILIZACION"] < m["BREAK_EVEN_U"]) else
                                                ("CAPACIDAD_OCIOSA_SIN_PERDIDA_OPERATIVA" if m.get("UTILIZACION") is not None else NO_CALC_D)),
                      "ETIQUETA": etiqueta(f["alt"]["universo"])})
    ok = [r for r in filas if (r.get("VAN_CON_DEMANDA_DECLARADA") or -1) >= 0]
    al = [r for r in ok if r.get("TIPO") == ASSET_LIGHT]
    pl = [r for r in ok if r.get("TIPO") == "PLANTA"]
    if not filas:
        concl = "NO_CALCULABLE: ninguna alternativa completa en el universo"
    elif al and not pl:
        concl = "FACON_ASSET_LIGHT_HASTA_VALIDAR_MAS_DEMANDA (solo asset-light tiene VAN ≥ 0 con la demanda declarada)"
    elif not ok:
        concl = f"{SQ}: ninguna alternativa con VAN ≥ 0 con la demanda declarada; validar más demanda"
    else:
        concl = "ALTERNATIVAS_CON_PLANTA_COMPATIBLES: " + ", ".join(r["ALTERNATIVA"] for r in pl)
    return filas, {"CONCLUSION": concl}


NO_CALC_D = mr.NO_CALC


def consulta_payback(E, fichas, X, inp):
    """«Quiero recuperar en máximo X años.» No ajusta parámetros: informa el cambio mínimo que haría falta."""
    if X is None:
        return [{"ESTADO": "SIN_CONSULTA", "UNIVERSO": fichas[0]["alt"]["universo"] if fichas else "",
                 "NOTA": "payback máximo no declarado (consulta.payback_max_anios vacío)"}]
    filas = []
    vs = mr.como_lista(inp.get("consulta.payback_variables") or ["precio_venta", "capex", "demanda", "alimento"])
    pred = (lambda x, X=X: x is not None and x <= X + 1e-9)
    for f in fichas:
        if f["alt"]["tipo"] == SQ or not f["completa"]:
            continue
        pb = f["ev"]["met"].get("PAYBACK")
        cumple = pred(pb)
        fila = {"ALTERNATIVA": f["id"], "UNIVERSO": f["alt"]["universo"], "PAYBACK_MAX_ANIOS": X, "PAYBACK_BASE_ANIOS": pb,
                "PAYBACK_ESTADO": f["ev"]["met"].get("PAYBACK_ESTADO"), "CUMPLE": "SÍ" if cumple else "NO",
                "ETIQUETA": etiqueta(f["alt"]["universo"]), "NOTA": "cambios necesarios informados, NO aplicados"}
        if not cumple:
            for v in vs:
                q = mr.punto_quiebre(E, f["alt"], v, "PAYBACK", X, None, 30, predicado=pred)
                fila[f"SHOCK_NECESARIO_{v}"] = q.get("SHOCK_QUIEBRE")
                fila[f"ESTADO_{v}"] = q.get("ESTADO")
        filas.append(fila)
    return filas


# ---------------------------------------------------------------------------------------------
# 11. VALOR DE LA INFORMACIÓN Y QUE_HACER_AHORA
# ---------------------------------------------------------------------------------------------
ACCIONES = (
    (r"^PRECIOS", "Relevar precios por producto × canal × mercado (lista, descuentos, plazos) y cargarlos en 21_modelo_financiero/base_precios_venta.csv", "DPV-013, DPV-039, DPV-070"),
    (r"^DEMANDA", "Conseguir cartas de intención / volúmenes por producto (demanda A/B); empezar por la red de supermercados", "DPV-002, DPV-020, DPV-037, DPV-040"),
    (r"^CANALES|^CT:días de cobro", "Relevar condiciones comerciales y plazos de cobro por canal", "DPV-039, DPV-175"),
    (r"^CAPEX:TOTAL", "Cotizar CAPEX: línea de faena, frío, obra y utilities (RFQ de 19_capex/matriz_rfq_capex.csv)", "DPV-097, DPV-095, DPV-161"),
    (r"^CAPEX:CRONOGRAMA|^TIEMPO:duración|^TIEMPO:.*mes", "Cronograma de permisos, obra, montaje y habilitación (con proveedores)", "DPV-086"),
    (r"^TIEMPO:horizonte|^DESCUENTO", "Decidir horizonte de evaluación y tasa de descuento del inversor", "DEC-007, DPV-001"),
    (r"^OPEX:FAENA_FACON", "Cotizar faena a façon (tarifa, frío, subproductos)", "DPV-006"),
    (r"^OPEX:FAENA_PROPIA", "Cotizar insumos y servicios de faena propia; validar tarifa eléctrica", "DPV-052, DPV-095, DPV-172"),
    (r"^OPEX:ALIMENTO_COMPRADO", "Cotizar alimento balanceado puesto en granja", "DPV-050"),
    (r"^OPEX:ALIMENTO_FACON", "Cotizar alimento a façon", "DPV-155"),
    (r"^OPEX:PLANTA_ALIMENTO_PROPIA", "Cotizar granos (maíz, soja) puestos en planta", "DPV-157"),
    (r"^OPEX:POLLITO_COMPRADO", "Cotizar pollito BB", "DPV-006, DPV-047"),
    (r"^OPEX:INCUBACION_PROPIA", "Cotizar huevo fértil e insumos de incubación", "DPV-047"),
    (r"^OPEX:GRANJAS_INTEGRADAS", "Relevar productores integrables y pago por ave", "DPV-048, DPV-170"),
    (r"^OPEX:GRANJAS_PROPIAS", "Costear granjas propias (galpones, energía, mano de obra)", "DPV-051"),
    (r"^OPEX:ESTRUCTURA", "Validar salarios, cargas y estructura", "DPV-148, DPV-146"),
    (r"^OPEX:TRATAMIENTO_SUBPRODUCTOS", "Costear tratamiento propio de subproductos o receptor", "DEC-027"),
    (r"^OPEX", "Completar costeo OPEX (20_opex/matriz_validacion_opex.csv)", ""),
    (r"^RAMPUP", "Definir curva de ramp-up con referencias de arranque", "DEC-090"),
    (r"^PRODUCCION", "Ensayo de rendimientos en planta o decisión de aceptar el balance 04", "DPV-060, DEC-028"),
    (r"^IMPUESTOS_INGRESOS", "Relevar IIBB y tasas municipales por jurisdicción", "DPV-043"),
    (r"^GANANCIAS|^IVA", "Definir tratamiento fiscal (ganancias, quebrantos, IVA)", "DPV-169, DPV-043"),
    (r"^CT", "Definir días de stock, de pago y propiedad de inventarios", "DPV-175, DEC-024"),
    (r"^DEPRECIACION|^REPOSICION", "Cargar vida útil, valor residual y costo de reemplazo en el BOQ", "DPV-167"),
    (r"^FINANCIAMIENTO", "Definir estructura de financiamiento (sin asumir USD 2 M)", "DEC-092, DPV-001"),
    (r"^FISICO:TERRENO", "Confirmar terreno (superficie, zonificación, accesos)", "DPV-087"),
    (r"^FISICO:POTENCIA", "Validar factibilidad y tarifa eléctrica (potencia disponible)", "DPV-095, DPV-052"),
    (r"^FISICO:AGUA", "Validar fuente y caudal de agua", "DPV-053"),
    (r"^FISICO:CAPACIDAD_LINEA", "Obtener capacidad garantizada de línea (cotización)", "DPV-097"),
    (r"^FISICO:FACON_FAENA", "Confirmar capacidad de faena a façon disponible", "DPV-006"),
    (r"^FISICO:PRODUCCION_PRIMARIA", "Relevar m² de galpón de integrados disponibles", "DPV-048"),
    (r"^FISICO:POLLITO|^FISICO:HUEVO", "Confirmar disponibilidad de pollito BB / huevo fértil", "DPV-006, DPV-047"),
    (r"^FISICO:ALIMENTO", "Confirmar abastecimiento de alimento", "DPV-050, DPV-155, DPV-157"),
    (r"^FISICO:RECEPTOR|^FISICO:TRATAMIENTO", "Confirmar receptor o tratamiento de subproductos", "DEC-027, DPV-072"),
    (r"^FISICO:TRANSPORTE", "Confirmar transportistas", "DPV-042"),
    (r"^FISICO:FRIO", "Confirmar frío de terceros", "DPV-109"),
    (r"^FISICO:SITIOS", "Identificar sitios de granjas propias", "DPV-051"),
)
VAR_A_ITEM = {"demanda": "DEMANDA", "capex": "CAPEX:TOTAL", "alimento": "OPEX:ALIMENTO_COMPRADO", "fcr": "OPEX:ALIMENTO_COMPRADO",
              "maiz": "OPEX:PLANTA_ALIMENTO_PROPIA", "soja": "OPEX:PLANTA_ALIMENTO_PROPIA", "pollito": "OPEX:POLLITO_COMPRADO",
              "electricidad": "FISICO:POTENCIA", "gas": "OPEX:FAENA_PROPIA", "agua": "FISICO:AGUA", "salarios": "OPEX:ESTRUCTURA",
              "facon": "OPEX:FAENA_FACON", "dias_cobro": "CANALES", "descuentos": "CANALES", "devoluciones": "CANALES",
              "tasa_descuento": "DESCUENTO", "tasa_deuda": "FINANCIAMIENTO", "plazo_deuda": "FINANCIAMIENTO", "dias_pago": "CT",
              "tasa_ganancias": "GANANCIAS", "iibb": "IMPUESTOS_INGRESOS", "packaging": "OPEX", "mantenimiento": "OPEX",
              "logistica": "OPEX", "opex_total": "OPEX"}


def item_de_variable(v):
    if v in VAR_A_ITEM:
        return VAR_A_ITEM[v]
    if v.startswith("precio"):
        return "PRECIOS"
    if v.startswith("capex"):
        return "CAPEX:TOTAL"
    return mr.VARIABLES[v]["BLOQUE_MOTOR"]


_REGS = {}


def registros_existentes():
    if not _REGS:
        ids = set()
        for ruta, pat in ((ARCH_DPV, r"^\| (DPV-\d{3})"), (ARCH_DEC, r"^\| (DEC-\d{3})")):
            with open(ruta, encoding="utf-8") as fh:
                for linea in fh:
                    m = re.match(pat, linea)
                    if m:
                        ids.add(m.group(1))
        _REGS["ids"] = ids
    return _REGS["ids"]


def accion_de(item):
    for pat, acc, dpv in ACCIONES:
        if re.search(pat, item):
            ids = [x.strip() for x in dpv.split(",") if x.strip()]
            exist = registros_existentes()
            falt = [x for x in ids if x not in exist]
            return acc, dpv, ("SÍ" if ids and not falt else ("PARCIAL: no encontrados " + ", ".join(falt) if ids else "SIN_DPV")), "NO"
    return f"NUEVA: resolver '{item}'", "", "SIN_DPV", "SÍ"


def _items_faltantes(F):
    out = []
    for b, xs in F.items():
        for x in xs:
            t = re.sub(r"^E\d+-\d+: ", "", x)
            refs = set(re.findall(r"(D(?:PV|EC)-\d+)", x))
            if b == "OPEX" and "módulos incompletos" in x:
                mods = re.findall(r"módulos incompletos: ([A-Z_, ]+)", x)[0]
                for mo_ in [y.strip() for y in mods.split(",") if y.strip()]:
                    out.append((f"OPEX:{mo_}", b, refs))
                continue
            if b == "CAPEX":
                out.append(("CAPEX:CRONOGRAMA" if "CURVA_DE_DESEMBOLSO" in t else "CAPEX:TOTAL", b, refs))
                continue
            out.append((f"{b}:{t.split(' (')[0].strip()}", b, refs))
    return out


def prioridad_evidencia(E, fichas):
    """Ranking de datos faltantes DERIVADO del motor: cuántos indicadores bloquea cada bloque (DEPENDENCIAS_FLAG de 21)
    y en cuántas alternativas falta. Orden: (indicadores bloqueados ↓, alternativas bloqueadas ↓, posición en la cadena)."""
    agg = {}
    n_alt = 0
    for f in fichas:
        if f["alt"]["tipo"] == SQ:
            continue
        n_alt += 1
        b = E.base(f["alt"])
        items = _items_faltantes(mf.disponibilidad(b[0])) if b[0] != "ERROR" else []
        items += [(f"FISICO:{g['GATE']}", "FISICO", set(x.strip() for x in g["DPV"].split(",") if x.strip()))
                  for g in f["fisico"]["gates"] if g["ESTADO"] == PEND]
        for it, bl, refs in set((i, b_, frozenset(r)) for i, b_, r in items):
            a = agg.setdefault(it, {"ITEM": it, "BLOQUE": bl, "ALTS": set(), "REFS": set()})
            a["ALTS"].add(f["id"])
            a["REFS"] |= set(refs)
    filas = []
    for it, a in agg.items():
        nfl = sum(1 for fl, deps in mf.DEPENDENCIAS_FLAG.items() if a["BLOQUE"] in deps)
        acc, dpv, existe, nueva = accion_de(it)
        orden = mf.BLOQUES.index(a["BLOQUE"]) if a["BLOQUE"] in mf.BLOQUES else len(mf.BLOQUES)
        filas.append({"UNIVERSO": "EVIDENCIA", "ITEM": it, "BLOQUE": a["BLOQUE"], "INDICADORES_BLOQUEADOS": nfl,
                      "N_ALTERNATIVAS_BLOQUEADAS": len(a["ALTS"]), "N_ALTERNATIVAS": n_alt,
                      "REGISTROS_EN_FALTANTE": ", ".join(sorted(a["REFS"])), "ACCION": acc, "DPV_VINCULADOS": dpv,
                      "DPV_EXISTEN": existe, "NUEVA": nueva, "_orden": orden,
                      "POTENCIAL_DE_CAMBIAR_DECISION": POTENCIAL_NO_CALC,
                      "METODO": "faltantes de disponibilidad() del motor × DEPENDENCIAS_FLAG; gates físicos pendientes"})
    asignar_rank_compartido(filas, lambda r: (r["INDICADORES_BLOQUEADOS"], r["N_ALTERNATIVAS_BLOQUEADAS"]),
                            "indicadores bloqueados y alternativas bloqueadas")
    for r in filas:
        r.pop("_orden")
    return filas


def asignar_rank_compartido(filas, clave, criterio):
    """RANK_COMPARTIDO = 1 + # ítems estrictamente mejores según `clave` (mayor = más prioritario). Los empates NO se
    desempatan por orden de archivo, ID, posición en código ni nombre: quedan con el mismo rango y se informa. El
    desempate futuro corresponde a sensibilidad, magnitud económica, capacidad de cambiar la decisión y costo del dato."""
    for r in filas:
        mejores = sum(1 for x in filas if clave(x) > clave(r))
        emp = sum(1 for x in filas if clave(x) == clave(r))
        r["RANK_COMPARTIDO"] = mejores + 1 if "R25" not in mr._MUT else None
        r["N_EMPATADOS"] = emp
        r["EMPATE"] = (f"EMPATE entre {emp} ítems por {criterio}: sin desempate (pendiente de sensibilidad, magnitud "
                       "económica, impacto en la decisión y costo del dato)") if emp > 1 else ""
    if "R25" in mr._MUT:                                         # mutación: desempate por posición
        for i, r in enumerate(sorted(filas, key=lambda r: (-clave(r)[0], r["ITEM"])), 1):
            r["RANK_COMPARTIDO"], r["EMPATE"] = i, ""
    filas.sort(key=lambda r: (r["RANK_COMPARTIDO"], r["ITEM"]))   # orden de presentación; dentro del empate NO significa nada
    for r in filas:
        r["ORDEN_DENTRO_DEL_EMPATE"] = "NO_SIGNIFICATIVO" if r["N_EMPATADOS"] > 1 else ""


def prioridad_escenario(oneway, dec_van, fichas):
    """Qué dato puede cambiar más la decisión DENTRO DEL ESCENARIO: (puede invertir el orden mejor/segunda o cruzar
    VAN = 0 frente al status quo) → amplitud del VAN de la mejor → cercanía entre alternativas."""
    if dec_van.get("ESTADO") != "MEJOR_EN_ESCENARIO":
        return []
    best, sec = dec_van["MEJOR"], dec_van.get("SEGUNDA")
    gap = abs(dec_van.get("DIFERENCIA_VALOR") or 0.0)
    rows = {}
    for r in oneway:
        if r.get("SHOCK") is None or r["ESTADO"] != "OK" or r.get("VAN") is None:
            continue
        rows.setdefault((r["ALTERNATIVA"], r["VARIABLE"]), {})[r["SHOCK"]] = r["VAN"]
    filas = []
    ev_falta = {}
    for f in fichas:
        for b in (f["faltantes_cortos"] or "").split(", "):
            ev_falta[b] = True
    for (alt, var), d in rows.items():
        if alt != best:
            continue
        vals = list(d.values())
        sw = max(vals) - min(vals)
        flip = []
        if sec and sec != SQ and (sec, var) in rows:
            for s_, v in d.items():
                w = rows[(sec, var)].get(s_)
                if w is not None and w > v:
                    flip.append(f"{var} {s_:+g}: {sec} supera a {best}")
        for s_, v in sorted(d.items()):
            if v < 0:
                flip.append(f"{var} {s_:+g}: VAN < 0 (no invertir le gana)")
                break
        it = item_de_variable(var)
        acc, dpv, existe, nueva = accion_de(it)
        filas.append({"UNIVERSO": fichas[0]["alt"]["universo"] if fichas else "", "ITEM": it, "VARIABLE_RIESGO": var,
                      "BLOQUE": mr.VARIABLES[var]["BLOQUE_MOTOR"], "SWING_VAN_MEJOR": sw,
                      "PUEDE_CAMBIAR_DECISION": "SÍ" if flip else "NO", "COMO_CAMBIA": " | ".join(flip[:3]),
                      "CERCANIA_ALTERNATIVAS": (gap / sw) if sw > 0 else None, "ACCION": acc, "DPV_VINCULADOS": dpv,
                      "POTENCIAL_DE_CAMBIAR_DECISION": ("SÍ" if flip else "NO") + " (one-way dentro del escenario; no es VOI)",
                      "DPV_EXISTEN": existe, "NUEVA": nueva,
                      "METODO": "sensibilidad one-way de la mejor y la segunda (MAX_VAN); sin distribuciones: no es VOI bayesiano"})
    asignar_rank_compartido(filas, lambda r: (r["PUEDE_CAMBIAR_DECISION"] == "SÍ", round(r["SWING_VAN_MEJOR"], 6)),
                            "capacidad de cambiar la decisión y amplitud del VAN")
    return filas


def que_hacer_ahora(prio_ev, prio_esc, n=10):
    """Acciones de las prioridades (evidencia primero, luego escenario). Se incluyen GRUPOS de empate completos: si el
    corte de n cae dentro de un empate, entra todo el grupo (no se elige arbitrariamente dentro del empate)."""
    out, vistos = [], set()
    for origen, lista in (("PRIORIDAD_EVIDENCIA (bloqueos del motor)", prio_ev), ("PRIORIDAD_ESCENARIO (sensibilidad)", prio_esc)):
        rango_corte = None
        for r in lista:
            if rango_corte is not None and r["RANK_COMPARTIDO"] != rango_corte:
                break
            if r["ACCION"] in vistos:
                continue
            vistos.add(r["ACCION"])
            out.append({"RANK_COMPARTIDO": r["RANK_COMPARTIDO"], "EMPATE": r.get("EMPATE", ""), "QUE_HACER_AHORA": r["ACCION"],
                        "ITEM": r["ITEM"], "DPV_VINCULADOS": r["DPV_VINCULADOS"],
                        "DPV_EXISTEN": r["DPV_EXISTEN"], "NUEVA": r["NUEVA"], "ORIGEN_RANKING": origen,
                        "POTENCIAL_DE_CAMBIAR_DECISION": r.get("POTENCIAL_DE_CAMBIAR_DECISION", POTENCIAL_NO_CALC),
                        "RAZON": (f"bloquea {r['INDICADORES_BLOQUEADOS']} indicadores en {r['N_ALTERNATIVAS_BLOQUEADAS']}/{r['N_ALTERNATIVAS']} alternativas"
                                  if "INDICADORES_BLOQUEADOS" in r else
                                  f"amplitud VAN {r['SWING_VAN_MEJOR']:,.0f}; puede cambiar la decisión: {r['PUEDE_CAMBIAR_DECISION']}"),
                        "UNIVERSO": r["UNIVERSO"]})
            if len(out) >= n and rango_corte is None:
                rango_corte = r["RANK_COMPARTIDO"]
        if rango_corte is not None:
            break
    return out


# ---------------------------------------------------------------------------------------------
# 12. ORQUESTACIÓN POR UNIVERSO
# ---------------------------------------------------------------------------------------------
def objetivos_de(inp):
    o = mr.como_lista(inp.get("optimizador.objetivos") or "TODOS")
    if o == ["TODOS"]:
        return list(OBJETIVOS)
    for x in o:
        if x not in OBJETIVOS:
            raise mr.ErrorRiesgo(f"objetivo {x} no admitido {tuple(OBJETIVOS)}")
    return o


def correr_universo(alts, inp, universo, stresses=None, dists=None, corrs=None, E=None):
    """Corre la cadena completa para UN universo. Nunca mezcla universos."""
    if any(a["universo"] != universo for a in alts):
        raise mr.ErrorRiesgo("alternativas de distintos universos en una misma corrida")
    E = E or mr.Evaluador()
    restr = leer_restricciones(inp)
    fichas = [ficha(E, a, inp, restr) for a in alts]
    finalizar_fichas(fichas, inp)
    out = {"universo": universo, "fichas": fichas, "E": E, "oneway": [], "tornado": [], "sens2d": [], "stress": [],
           "quiebres": [], "mc": [], "mc_muestras": [], "decisiones": [], "ranking": {}, "restr": restr}
    completas = [f for f in fichas if f["completa"] and f["alt"]["tipo"] != SQ and f["COMPARABILIDAD"] != "FALSE"]
    perturbable = universo != "EVIDENCIA"
    variables = [v for v in mr.como_lista(inp.get("sensibilidad.variables")) if v in mr.VARIABLES]
    stresses = stresses or []
    swing_van = {}
    if perturbable:
        for f in completas:
            ow = mr.sensibilidad_oneway(E, f["alt"], variables, inp)
            out["oneway"] += ow
            for met in mr.como_lista(inp.get("tornado.metricas") or "VAN"):
                tor = mr.tornado(ow, met, f["id"])
                out["tornado"] += tor
                if mr.ALIAS_METRICA.get(met, met) == "VAN":
                    sws = [t["SWING"] for t in tor if t.get("SWING") is not None]
                    swing_van[f["id"]] = max(sws) if sws else None
            for par in mr.como_lista(inp.get("sens2d.pares")):
                vx, vy = str(par).split("×")
                out["sens2d"] += mr.sensibilidad_2d(E, f["alt"], (vx, vy), inp)
            out["stress"] += mr.correr_stress(E, f["alt"], stresses)
            for v in mr.como_lista(inp.get("quiebre.variables")):
                met = "VAN_ACCIONISTA" if v == "tasa_deuda" else (inp.get("quiebre.metrica") or "VAN")
                out["quiebres"].append(mr.punto_quiebre(E, f["alt"], v, met, mr.num(inp.get("quiebre.objetivo")) or 0.0,
                                                        None, int(inp.get("quiebre.n_grilla") or 24)))
    escenarios = escenarios_robustez(inp, stresses) if perturbable else []
    robustez(E, fichas, inp, restr, escenarios)
    score_riesgo(fichas, inp, swing_van)
    reaplicar_restricciones(fichas, restr, inp)          # RIESGO como restricción usa el score recién calculado
    # Monte Carlo
    capital = mr.num(inp.get("restriccion.CAPITAL_DISPONIBLE.valor"))
    if not perturbable:
        out["mc"].append({"ALTERNATIVA": "TODAS", "UNIVERSO": universo, "ESTADO": mr.MC_ND,
                          "NOTA": "universo EVIDENCIA: no se perturba la evidencia; además no hay distribuciones respaldadas"})
    elif not completas:
        out["mc"].append({"ALTERNATIVA": "TODAS", "UNIVERSO": universo, "ESTADO": mr.NO_CALC, "NOTA": "ninguna alternativa completa"})
    else:
        for f in completas:
            est, res, mu, notas = mr.monte_carlo(E, f["alt"], dists or [], corrs or [], inp.get("montecarlo.n"),
                                                 inp.get("montecarlo.semilla"), universo, capital,
                                                 con_tir=bool(inp.get("montecarlo.incluir_tir")),
                                                 supuesto_independencia=bool(inp.get("montecarlo.supuesto_independencia")))
            out["mc"] += mr.filas_mc(f["id"], est, res, notas, universo)
            out["mc_muestras"] += [dict(x, ALTERNATIVA=f["id"]) for x in mu]
            f["MC"] = res if est == "EJECUTADO" else None
    # rankings
    for o in objetivos_de(inp):
        filas, dec, orden = rankear(fichas, o, inp)
        if dec["ESTADO"] == NINGUNA and not completas:
            if universo == "EVIDENCIA":
                dec.update(ESTADO=mr.OPT_REAL_ND, DECISION_ESCENARIO="—", REGLA_STATUS_QUO="NO_APLICA",
                           POR_QUE="ninguna alternativa con VAN publicable en modo evidencia; ver prioridad_validacion.csv (bloqueos)",
                           NOTA="sin recomendación real: no se genera explicación de recomendación")
            else:
                dec.update(ESTADO=mf.NO_DISP_ESC, DECISION_ESCENARIO="—", REGLA_STATUS_QUO="NO_APLICA",
                           POR_QUE="ninguna alternativa con inputs completos en el escenario (escenario_optimizador.json); "
                           "no es lo mismo que NINGUNA_CONFIGURACION_FACTIBLE", NOTA="sin recomendación de escenario")
        est, cambios = estabilidad_ganador(orden, dec, o, escenarios) if dec["ESTADO"] == "MEJOR_EN_ESCENARIO" else (None, [])
        dec["ESTABILIDAD_GANADOR"] = est
        dec["STRESS_QUE_CAMBIA_DECISION"] = "; ".join(c for c in cambios if c.startswith("STRESS:")) or (
            "ninguno de los stress evaluados" if dec["ESTADO"] == "MEJOR_EN_ESCENARIO" and est is not None else "NO_EVALUADO")
        if cambios:
            dec["ROBUSTEZ_DECISION"] = (dec.get("ROBUSTEZ_DECISION", "") + " | " if dec.get("ROBUSTEZ_DECISION") else "") + \
                f"{NO_ROB}: el ganador cambia en " + "; ".join(cambios[:5])
        elif dec["ESTADO"] == "MEJOR_EN_ESCENARIO" and "ROBUSTEZ_DECISION" not in dec:
            dec["ROBUSTEZ_DECISION"] = ("ROBUSTA_EN_ESCENARIOS_EVALUADOS" if est is not None else
                                        "NO_EVALUADA (objetivo sin re-ranking por escenario o sin escenarios)")
        dec["UNIVERSO"], dec["ETIQUETA"], dec["AMBITO"] = universo, etiqueta(universo), ambito(universo)
        out["ranking"][o] = filas
        explicar_decision(dec, fichas, out, o)
        out["decisiones"].append(dec)
    out["dominancia_dims"] = dominancia(fichas, inp)
    out["pareto"] = pareto(fichas, inp)
    dv = next((d for d in out["decisiones"] if d["OBJETIVO"] == "MAX_VAN"), {})
    out["prio_esc"] = prioridad_escenario(out["oneway"], dv, fichas) if perturbable else []
    return out


CAMPOS_EXPLICACION = ("QUE_ELIGIO", "CONTRA_QUE", "RESTRICCIONES_CUMPLE", "VARIABLES_CRITICAS", "VARIABLES_QUE_LA_HACEN_GANAR",
                      "VARIABLES_QUE_PODRIAN_CAMBIARLA", "DATOS_FALTANTES_VALIDAR", "EVIDENCIA_GANADORA",
                      "POR_QUE_NO_INVERTIR_PODRIA_GANAR")


def explicar_decision(dec, fichas, out, objetivo):
    """Explicación de la recomendación DEL ESCENARIO (nunca del proyecto). Sin ganador no se fabrica explicación."""
    if dec.get("ESTADO") != "MEJOR_EN_ESCENARIO":
        for c in CAMPOS_EXPLICACION:
            dec.setdefault(c, f"NO_APLICA: {dec.get('ESTADO')}")
        if dec.get("ESTADO") == NINGUNA:
            dec["QUE_ELIGIO"] = dec.get("DECISION_ESCENARIO", "—")
            dec["POR_QUE_NO_INVERTIR_PODRIA_GANAR"] = dec.get("REGLA_STATUS_QUO", "")
        return
    F = {f["id"]: f for f in fichas}
    b = F[dec["MEJOR"]]
    s = F.get(dec.get("SEGUNDA"))
    dec["QUE_ELIGIO"] = dec["MEJOR"]
    dec["POR_QUE"] = f"{dec['SENTIDO']} {dec['METRICA']} = {mr.fmt(dec['VALOR_MEJOR'], 2)} entre {dec['N_RANKEADAS']} rankeadas"
    dec["CONTRA_QUE"] = ", ".join(f["id"] for f in fichas if f["id"] != b["id"] and out_rank(out, objetivo, f["id"]) is not None)
    dec["RESTRICCIONES_CUMPLE"] = ", ".join(f"{r['NOMBRE']}({r['TIPO']})" for r in b["R_CUMPLIMIENTO"] if r["ESTADO"] == "CUMPLE") or "sin restricciones declaradas"
    if s is not None:
        dif = []
        for m in ("CAPEX", "FONDOS_INICIALES", "PICO_FONDOS", "EBITDA", "INGRESOS", "VAN"):
            x, y = b["ev"]["met"].get(m), s["ev"]["met"].get(m)
            if x is not None and y is not None and abs(x - y) > 1e-9:
                dif.append(f"{m} {x - y:+,.0f}")
        dec["VARIABLES_QUE_LA_HACEN_GANAR"] = "; ".join(dif) + f" (vs {s['id']})"
    flips = [r for r in out.get("oneway", []) if r["ALTERNATIVA"] == b["id"] and r.get("VAN") is not None and r["VAN"] < 0]
    vs = sorted({r["VARIABLE"] for r in flips})
    dec["VARIABLES_QUE_PODRIAN_CAMBIARLA"] = (("VAN < 0 con shocks en: " + ", ".join(vs)) if vs else "") + \
        ((" | " if vs else "") + dec["ROBUSTEZ_DECISION"] if NO_ROB in str(dec.get("ROBUSTEZ_DECISION")) else "")
    dec["DATOS_FALTANTES_VALIDAR"] = b["cobertura_nota"] + ("; gates pendientes: " + ", ".join(
        g["GATE"] for g in b["fisico"]["gates"] if g["ESTADO"] == PEND) if any(g["ESTADO"] == PEND for g in b["fisico"]["gates"]) else "")
    tor = sorted([t for t in out.get("tornado", []) if t["ALTERNATIVA"] == b["id"] and t["METRICA"] == "VAN" and t.get("RANK")],
                 key=lambda t: t["RANK"])[:5]
    dec["VARIABLES_CRITICAS"] = "; ".join(f"{t['VARIABLE']} (amplitud VAN {t['SWING']:,.0f})" for t in tor) or "NO_CALCULADO (sin tornado)"
    dec["EVIDENCIA_GANADORA"] = (f"COBERTURA_EVIDENCIA {b['cobertura']:.0%}; semáforo {b['SEMAFORO']}"
                                 if b["cobertura"] is not None else b["cobertura_nota"])
    if s is None:
        dec["VARIABLES_QUE_LA_HACEN_GANAR"] = "única alternativa rankeable"


def out_rank(out, objetivo, aid):
    return (out["ranking"].get(objetivo) or {}).get(aid, {}).get("RANK")


# ---------------------------------------------------------------------------------------------
# 13. TABLAS DE SALIDA
# ---------------------------------------------------------------------------------------------
CAMPOS_RES = ["ID_CORRIDA", "UNIVERSO", "AMBITO", "ALTERNATIVA", "TIPO", "CONFIGURACION", "ESCALA", "VARIANTE", "TRAYECTORIA", "OBJETIVO",
              "ESTADO_OPTIMIZACION", "FACTIBILIDAD_FISICA", "FACTIBILIDAD_ECONOMICA", "FACTIBILIDAD_FINANCIERA",
              "RESPALDO_COMERCIAL", "COMPARABILIDAD", "CAPEX", "FONDOS_INICIALES", "PICO_FONDOS", "EBITDA", "VAN", "TIR",
              "PAYBACK", "DSCR", "RIESGO", "RIESGO_TIPO", "ROBUSTEZ", "SCORE", "DOMINADA", "RANK", "MOTIVO", "LIMITACION_PRINCIPAL",
              "DATOS_FALTANTES", "COBERTURA_EVIDENCIA", "SEMAFORO", "ETIQUETA_EVIDENCIA"]


def filas_resultados(U):
    out = []
    dec = {d["OBJETIVO"]: d for d in U["decisiones"]}
    for o, rk in U["ranking"].items():
        for f in U["fichas"]:
            a, m, r = f["alt"], f["ev"]["met"], rk.get(f["id"], {})
            out.append({"ID_CORRIDA": f"{U['universo']}|{f['id']}|{o}", "UNIVERSO": U["universo"], "ALTERNATIVA": f["id"],
                        "TIPO": a["tipo"], "CONFIGURACION": a["configuracion"], "ESCALA": "→".join(str(e) for e in a["escalas"]) or "—",
                        "VARIANTE": a["variante"], "TRAYECTORIA": a["trayectoria"], "OBJETIVO": o,
                        "ESTADO_OPTIMIZACION": dec[o]["ESTADO"], "FACTIBILIDAD_FISICA": f["F_FISICA"],
                        "FACTIBILIDAD_ECONOMICA": f["F_ECONOMICA"], "FACTIBILIDAD_FINANCIERA": f["F_FINANCIERA"],
                        "RESPALDO_COMERCIAL": f["R_COMERCIAL"], "COMPARABILIDAD": f["COMPARABILIDAD"],
                        "CAPEX": m.get("CAPEX"), "FONDOS_INICIALES": m.get("FONDOS_INICIALES"), "PICO_FONDOS": m.get("PICO_FONDOS"),
                        "EBITDA": m.get("EBITDA"), "VAN": m.get("VAN"), "TIR": m.get("TIR"), "PAYBACK": m.get("PAYBACK"),
                        "DSCR": m.get("DSCR"), "RIESGO": f.get("SCORE_ORDINAL_RIESGO") if f.get("SCORE_ORDINAL_RIESGO") is not None else f.get("RIESGO_NOTA"),
                        "RIESGO_TIPO": "SCORE_ORDINAL_RIESGO (orden interno; NO ES PROBABILIDAD)",
                        "ROBUSTEZ": f.get("ROBUSTEZ") if f.get("ROBUSTEZ") is not None else (f.get("ROB") or {}).get("ESTADO"),
                        "SCORE": r.get("SCORE"), "DOMINADA": (("DOMINADA_POR: " + ", ".join(f["DOMINADA_POR"])) if f["DOMINADA_POR"] else
                                                      ("NO" if f.get("DOM_ESTADO") == "EVALUADA" else f.get("DOM_ESTADO"))),
                        "RANK": r.get("RANK"), "MOTIVO": r.get("MOTIVO") or (f["COMPARABILIDAD_MOTIVO"] if f["COMPARABILIDAD"] != "TRUE" else ""),
                        "LIMITACION_PRINCIPAL": limitacion_principal(f), "DATOS_FALTANTES": f["faltantes_cortos"],
                        "COBERTURA_EVIDENCIA": f["cobertura"], "SEMAFORO": f["SEMAFORO"], "ETIQUETA_EVIDENCIA": etiqueta(U["universo"])})
    return out


CAMPOS_DEC = ["UNIVERSO", "AMBITO", "OBJETIVO", "METRICA", "SENTIDO", "ESTADO", "MEJOR", "VALOR_MEJOR", "SEGUNDA", "VALOR_SEGUNDA",
              "DIFERENCIA_VALOR", "DIFERENCIA_SCORE", "DECISION_ESCENARIO", "REGLA_STATUS_QUO", "ROBUSTEZ_DECISION",
              "ESTABILIDAD_GANADOR", "STRESS_QUE_CAMBIA_DECISION", "N_EVALUADAS", "N_RANKEADAS", "QUE_ELIGIO", "POR_QUE",
              "CONTRA_QUE", "RESTRICCIONES_CUMPLE", "VARIABLES_CRITICAS", "VARIABLES_QUE_LA_HACEN_GANAR",
              "VARIABLES_QUE_PODRIAN_CAMBIARLA", "DATOS_FALTANTES_VALIDAR", "EVIDENCIA_GANADORA", "POR_QUE_NO_INVERTIR_PODRIA_GANAR",
              "PESOS_BALANCEADO", "NOTA", "ETIQUETA"]


def filas_explicacion(U):
    out = []
    tor = {}
    for t in U["tornado"]:
        if t["METRICA"] == "VAN" and t.get("RANK"):
            tor.setdefault(t["ALTERNATIVA"], []).append(t)
    qb = {}
    for q in U["quiebres"]:
        if q.get("ESTADO") == "ENCONTRADO":
            qb.setdefault(q["ALTERNATIVA"], []).append(f"{q['VARIABLE']} {q['SHOCK_QUIEBRE']:+.4g}" +
                                                       (" (rel.)" if q["TIPO_SHOCK"] == "RELATIVO" else ""))
    prio = U.get("prio_esc") or []
    for f in U["fichas"]:
        pro, con = [], []
        for o, rk in U["ranking"].items():
            if rk.get(f["id"], {}).get("RANK") == 1:
                pro.append(f"mejor en {o}")
        if f["R_CUMPLIMIENTO"] and not f["HARD_INCUMPLE"] and not f["HARD_PENDIENTE"]:
            pro.append("cumple las restricciones duras declaradas")
        if f["COMPARABILIDAD"] == "FALSE":
            con.append(f["COMPARABILIDAD_MOTIVO"])
        if f["HARD_INCUMPLE"]:
            con.append("incumple " + ", ".join(f["HARD_INCUMPLE"]))
        if f["DOMINADA_POR"]:
            con.append("dominada por " + ", ".join(f["DOMINADA_POR"]))
        if str(f["ev"]["met"].get("PAYBACK_ESTADO")).startswith("NO_RECUPERADO"):
            con.append("no recupera la inversión en el horizonte")
        pend = [g["GATE"] for g in f["fisico"]["gates"] if g["ESTADO"] in (PEND, NO_FACTIBLE)]
        if pend:
            con.append("gates físicos no confirmados: " + ", ".join(pend))
        crit = sorted(tor.get(f["id"], []), key=lambda t: t["RANK"])[:3]
        dato = next((p for p in prio if p["PUEDE_CAMBIAR_DECISION"] == "SÍ"), None) if prio else None
        out.append({"UNIVERSO": U["universo"], "ALTERNATIVA": f["id"], "TIPO": f["alt"]["tipo"],
                    "RAZONES_A_FAVOR": "; ".join(pro) or "—", "RAZONES_EN_CONTRA": "; ".join(con) or "—",
                    "DRIVERS_CRITICOS": "; ".join(f"{t['VARIABLE']} (amplitud VAN {t['SWING']:,.0f})" for t in crit) or
                    ("NO_CALCULABLE (sin VAN publicable)" if not f["completa"] else "—"),
                    "PUNTO_QUIEBRE": "; ".join(qb.get(f["id"], [])) or "—",
                    "RESTRICCIONES_INCUMPLIDAS": ", ".join(f["HARD_INCUMPLE"] + [r["NOMBRE"] + "(SOFT)" for r in f["R_CUMPLIMIENTO"]
                                                                                 if r["TIPO"] == "SOFT" and r["ESTADO"] == "INCUMPLE"]) or "—",
                    "DATO_QUE_MAS_PODRIA_CAMBIAR_DECISION": (f"{dato['VARIABLE_RIESGO']} → {dato['ACCION']}" if dato else
                                                             (f["faltantes_cortos"] or "—")),
                    "DATOS_FALTANTES": f["faltantes_cortos"] or "—", "COBERTURA_EVIDENCIA": f["cobertura"],
                    "CONFIANZA": ("NO_APLICA" if f["cobertura"] is None else "SUFICIENTE_SEGUN_UMBRAL" if f["cobertura"] >= 1 else "BAJA"),
                    "SEMAFORO": f["SEMAFORO"], "ETIQUETA": etiqueta(U["universo"])})
    return out


def filas_dashboard(U):
    out = []
    dec = U["decisiones"]
    for f in U["fichas"]:
        m = f["ev"]["met"]
        rec = [f"{d['OBJETIVO']}: 1.ª" for d in dec if d.get("MEJOR") == f["id"]] + \
              [f"{d['OBJETIVO']}: 2.ª" for d in dec if d.get("SEGUNDA") == f["id"]] + \
              [f"{d['OBJETIVO']}: DECISION_ESCENARIO ({d.get('REGLA_STATUS_QUO', '')[:4]})" for d in dec
               if f["alt"]["tipo"] == SQ and d.get("DECISION_ESCENARIO") == SQ]
        out.append({"UNIVERSO": U["universo"], "ALTERNATIVA": f["id"], "TIPO": f["alt"]["tipo"], "CAPEX": m.get("CAPEX"),
                    "FONDOS_INICIALES": m.get("FONDOS_INICIALES"), "PICO_FONDOS": m.get("PICO_FONDOS"), "VAN": m.get("VAN"),
                    "TIR": m.get("TIR"), "PAYBACK": m.get("PAYBACK"), "SCORE_ORDINAL_RIESGO": f.get("SCORE_ORDINAL_RIESGO"),
                    "ROBUSTEZ": f.get("ROBUSTEZ"), "PCT_ESCENARIOS_VAN_NO_NEG": (f.get("ROB") or {}).get("PCT_VAN_NO_NEGATIVO"),
                    "RESTRICCIONES": f"cumple {sum(1 for r in f['R_CUMPLIMIENTO'] if r['ESTADO'] == 'CUMPLE')} / incumple "
                                     f"{sum(1 for r in f['R_CUMPLIMIENTO'] if r['ESTADO'] == 'INCUMPLE')} / no evaluables "
                                     f"{sum(1 for r in f['R_CUMPLIMIENTO'] if r['ESTADO'] == 'NO_EVALUABLE')}",
                    "FACTIBILIDAD_FISICA": f["F_FISICA"], "COBERTURA_EVIDENCIA": f["cobertura"], "SEMAFORO": f["SEMAFORO"],
                    "RECOMENDACION_ESCENARIO": "; ".join(rec) or "—", "QUE_VALIDAR": limitacion_principal(f),
                    "ETIQUETA": etiqueta(U["universo"]),
                    "NOTA": ("dentro del escenario; no es recomendación del proyecto" if U["universo"] != "EVIDENCIA" else mr.OPT_REAL_ND
                             if not f["completa"] else "")})
    return out


def filas_factibilidad(U):
    out = []
    for f in U["fichas"]:
        for g in f["fisico"]["gates"]:
            out.append(dict(g, UNIVERSO=U["universo"], ALTERNATIVA=f["id"], ESTADO_ALTERNATIVA=f["F_FISICA"]))
    return out


def filas_restricciones(U):
    out = []
    for f in U["fichas"]:
        for r in f["R_CUMPLIMIENTO"]:
            out.append({"UNIVERSO": U["universo"], "ALTERNATIVA": f["id"], **{k: r.get(k) for k in
                        ("NOMBRE", "TIPO", "VALOR", "VALOR_ALTERNATIVA", "ESTADO", "VIOLACION_REL", "PENALIZACION", "NOTA")}})
    if not out:
        out.append({"UNIVERSO": U["universo"], "ESTADO": "SIN_RESTRICCIONES_DECLARADAS",
                    "NOTA": "todas las restricciones son opcionales; no se asume capital ni demanda"})
    return out


def filas_robustez(U):
    return [dict(f.get("ROB") or {}, UNIVERSO=U["universo"], ALTERNATIVA=f["id"], ROBUSTEZ=f.get("ROBUSTEZ"),
                 SCORE_ORDINAL_RIESGO=f.get("SCORE_ORDINAL_RIESGO"), RIESGO_NOTA=f.get("RIESGO_NOTA"),
                 **{f"C_{k}": (f.get("RIESGO_COMP") or {}).get(k) for k in COMPONENTES_RIESGO}) for f in U["fichas"]]


def _vacio(Us, motivo):
    return [{"UNIVERSO": U["universo"], "ESTADO": mr.NO_CALC, "NOTA": motivo} for U in Us]


def escribir_salidas(Us, carpeta, extra):
    """Une los universos en archivos con columna UNIVERSO (los rankings son siempre internos a cada universo)."""
    def w(nombre, filas, campos=None):
        filas = [dict(f, AMBITO=ambito(f["UNIVERSO"])) if f.get("UNIVERSO") in mr.UNIVERSOS else f for f in filas]
        mr.escribir(os.path.join(carpeta, nombre), filas, campos or sorted({k for f in filas for k in f}) or ["ESTADO"])
    cat = lambda fn: [x for U in Us for x in fn(U)]
    w("resultados_optimizador.csv", cat(filas_resultados), CAMPOS_RES)
    w("decision_optimizador.csv", [d for U in Us for d in U["decisiones"]], CAMPOS_DEC)
    w("explicacion_optimizador.csv", cat(filas_explicacion))
    w("dashboard_decision.csv", cat(filas_dashboard))
    w("factibilidad_alternativas.csv", cat(filas_factibilidad))
    w("restricciones_alternativas.csv", cat(filas_restricciones))
    w("robustez_alternativas.csv", cat(filas_robustez))
    w("frontera_pareto.csv", cat(lambda U: U["pareto"]) or _vacio(Us, "sin alternativas con ambos ejes publicables"))
    sin = "ninguna alternativa completa y comparable en el universo (ver resultados_optimizador.csv: DATOS_FALTANTES)"
    for nombre, clave in (("sensibilidad_oneway.csv", "oneway"), ("sensibilidad_tornado.csv", "tornado"),
                          ("sensibilidad_2d.csv", "sens2d"), ("resultados_stress.csv", "stress"), ("puntos_quiebre.csv", "quiebres")):
        filas = [dict(x, UNIVERSO=U["universo"], ETIQUETA=etiqueta(U["universo"])) for U in Us for x in U[clave]]
        w(nombre, filas or [{"UNIVERSO": U["universo"], "ESTADO": mr.NO_CALC,
                              "NOTA": ("universo EVIDENCIA: la evidencia no se perturba; " if U["universo"] == "EVIDENCIA" else "") + sin}
                             for U in Us])
    w("monte_carlo_resultados.csv", [x for U in Us for x in U["mc"]])
    if any(U["mc_muestras"] for U in Us):
        w("monte_carlo_muestras.csv", [dict(x, UNIVERSO=U["universo"]) for U in Us for x in U["mc_muestras"]])
    prio = [r for U in Us for r in (U.get("prio_ev") or [])] + [r for U in Us for r in (U.get("prio_esc") or [])]
    w("prioridad_validacion.csv", prio or _vacio(Us, "sin faltantes ni sensibilidades"))
    w("que_hacer_ahora.csv", extra["que_hacer"] or _vacio(Us, "sin acciones derivadas"))
    for nombre in ("consulta_capital.csv", "consulta_demanda.csv", "consulta_payback.csv"):
        w(nombre, extra.get(nombre) or [{"ESTADO": "SIN_CONSULTA"}])


# ---------------------------------------------------------------------------------------------
# 14. CASO ARTIFICIAL (prueba de la maquinaria; NO es el proyecto)
# ---------------------------------------------------------------------------------------------
def _rub(rubro, nat, costo, grupo="servicios", moneda=None, driver=None, dias_pago=15.0):
    r = {"rubro": rubro, "grupo_proveedor": grupo, "naturaleza": nat, "costo_pleno_usd_anio": costo, "es_compra": True,
         "dias_pago": dias_pago, "iva_credito": True}
    if moneda:
        r["moneda_original"] = moneda
    if driver:
        r["driver_riesgo"] = driver
    return r


CURVA_ART = [{"mes": 1, "utilizacion": 0.5, "merma": 0.02, "eficiencia": 0.9, "costos_extra_usd_mes": 0.0},
             {"mes": 4, "utilizacion": 0.8, "merma": 0.01, "eficiencia": 0.95, "costos_extra_usd_mes": 0.0},
             {"mes": 7, "utilizacion": 1.0, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}]


def _p_art(nombre, escala, demanda, capex, rubros, con=6, deuda=None, precio=10.0):
    P = mf.caso_prueba(H=10, capex=capex, escala=escala, dias=12, demanda_kg_mes=demanda, tasa=0.12, tasa_gan=0.30,
                       dias_cobro=30.0, con=con, curva=copy.deepcopy(CURVA_ART), nombre=nombre, deudas=deuda,
                       convencion="PERIODO_REPORTE",
                       activos=[{"clase": "PROCESO:linea", "capex_usd": capex * 0.6, "vida_util_anios": 10, "valor_residual_usd": 0.0,
                                 "costo_reemplazo_usd": capex * 0.6},
                                {"clase": "OBRA_CIVIL:nave", "capex_usd": capex * 0.4, "vida_util_anios": 10, "valor_residual_usd": 0.0,
                                 "costo_reemplazo_usd": capex * 0.4}])
    P["etapas"][0]["opex_rubros"] = rubros
    P["precios"] = {"pollo_entero|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": precio}}
    P["valor_terminal"]["metodo"] = "SIN_VALOR_TERMINAL"
    P["tasa_descuento_accionista"] = 0.15
    return P


def caso_artificial():
    """Cinco alternativas ART-* + status quo. Números INVENTADOS para probar la maquinaria (ETIQUETA
    CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO). Nombres sin C0–CF para que nadie los lea como resultados del proyecto."""
    deuda = lambda m: [{"id": "D1", "monto": m, "tasa": 0.08, "tipo_tasa": "EFECTIVA_ANUAL", "base_tasa": "REAL", "plazo_meses": 60,
                        "gracia_meses": 12, "metodo": "FRANCES", "frecuencia_meses": 1, "mes_desembolso": 0}]
    defs = {
        "ART-ASSET-LIGHT": (ASSET_LIGHT, 100, 100, 500.0, [
            _rub("FAE-FACON", "variable", 5400.0), _rub("ALI-A-PT", "variable", 3600.0, "alimento"),
            _rub("LAB-ESTR", "fijo", 600.0, moneda="ARS")], 1, None),
        "ART-PLANTA-CHICA": ("PLANTA", 100, 100, 8000.0, [
            _rub("ALI-A-PT", "variable", 3600.0, "alimento"), _rub("POL-COMPRA", "variable", 1800.0, "pollitos"),
            _rub("LAB-PLANTA", "fijo", 1800.0, moneda="ARS"), _rub("UT-ELE-KWH", "variable", 300.0, "energia"),
            _rub("mantenimiento planta", "fijo", 300.0)], 6, None),
        "ART-PLANTA-GRANDE": ("PLANTA", 200, 150, 14000.0, [
            _rub("ALI-A-PT", "variable", 7200.0, "alimento"), _rub("POL-COMPRA", "variable", 3600.0, "pollitos"),
            _rub("LAB-PLANTA", "fijo", 2800.0, moneda="ARS"), _rub("UT-ELE-KWH", "variable", 600.0, "energia"),
            _rub("mantenimiento planta", "fijo", 500.0)], 6, deuda(7000.0)),
        "ART-INTEGRADA": ("PLANTA", 150, 150, 22000.0, [
            _rub("ALI-A-PT", "variable", 4000.0, "alimento"), _rub("ALI-MP-MAIZ", "variable", 1000.0, "granos"),
            _rub("POL-COMPRA", "variable", 1500.0, "pollitos"), _rub("LAB-PLANTA", "fijo", 3500.0, moneda="ARS"),
            _rub("UT-ELE-KWH", "variable", 450.0, "energia"), _rub("mantenimiento planta", "fijo", 800.0)], 8, deuda(10000.0)),
        "ART-INCOMPLETA": ("PLANTA", 100, 100, 6000.0, [
            _rub("ALI-A-PT", "variable", 3600.0, "alimento"), _rub("POL-COMPRA", "variable", 1800.0, "pollitos"),
            _rub("LAB-PLANTA", "fijo", None, moneda="ARS")], 6, None),
    }
    fis = {
        "ART-ASSET-LIGHT": [_gate("FACON_FAENA", 100.0, "aves/día", 150.0, "ARTIFICIAL")] +
                           [_gate(g, 0.0, u, None, "ARTIFICIAL", estado_req="NO_REQUERIDO_POR_ARQUITECTURA",
                                  nota="ARTIFICIAL: el caso declara que no tiene ningún módulo propio")
                            for g, u in (("TERRENO", "m²"), ("AGUA", "m³/día"), ("POTENCIA", "kW"))],
        "ART-PLANTA-CHICA": [_gate("TERRENO", 10000.0, "m²", 30000.0, "ARTIFICIAL"), _gate("AGUA", 100.0, "m³/día", 300.0, "ARTIFICIAL"),
                             _gate("POTENCIA", None, "kW", 500.0, "ARTIFICIAL")],
        "ART-PLANTA-GRANDE": [_gate("TERRENO", 20000.0, "m²", 30000.0, "ARTIFICIAL"), _gate("AGUA", 200.0, "m³/día", 300.0, "ARTIFICIAL"),
                              _gate("POTENCIA", 400.0, "kW", 500.0, "ARTIFICIAL")],
        "ART-INTEGRADA": [_gate("TERRENO", 25000.0, "m²", 30000.0, "ARTIFICIAL"), _gate("AGUA", 400.0, "m³/día", 300.0, "ARTIFICIAL")],
        "ART-INCOMPLETA": [_gate("TERRENO", 10000.0, "m²", 30000.0, "ARTIFICIAL")],
    }
    alts = []
    for aid, (tipo, esc, dem, capex, rub, con, deu) in defs.items():
        alts.append({"id": aid, "tipo": tipo, "universo": "ARTIFICIAL_TEST", "configuracion": aid, "variante": "ARTIFICIAL",
                     "escalas": (esc,), "trayectoria": "ESCALA_UNICA",
                     "construir": (lambda a=aid, e=esc, d=dem, c=capex, r=rub, cn=con, dd=deu: (_p_art(a, e, d, c, copy.deepcopy(r), cn, dd), None)),
                     "base_valores": {"mortalidad": 0.05, "condenas": 0.01, "traslado_fx": 0.5, "precio_venta": 10.0},
                     "fisico": fis[aid], "cobertura": (0.0, "ARTIFICIAL_TEST: ningún bloque tiene evidencia")})
    alts.append(mr.alternativa_status_quo("ARTIFICIAL_TEST"))
    return alts


def inputs_artificiales(inp):
    """Inputs del caso artificial: parten de los del proyecto y agregan restricciones, pesos y consultas ARTIFICIALES."""
    a = dict(inp)
    a.update({"restriccion.CAPITAL_DISPONIBLE.valor": 16000.0, "restriccion.CAPITAL_DISPONIBLE.tipo": "HARD",
              "restriccion.PAYBACK.valor": 6.0, "restriccion.PAYBACK.tipo": "SOFT", "restriccion.PAYBACK.penalizacion": 0.5,
              "restriccion.AGUA.valor": 350.0, "restriccion.AGUA.tipo": "HARD",
              "riesgo.peso.VAN_NEGATIVO_ESCENARIOS": 3.0, "riesgo.peso.SENSIBILIDAD_VAN": 2.0, "riesgo.peso.PICO_FONDOS_RELATIVO": 1.0,
              "riesgo.peso.FISICO_PENDIENTE": 1.0,
              "balanceado.peso.rentabilidad": 3.0, "balanceado.peso.riesgo": 2.0, "balanceado.peso.capital": 1.0,
              "balanceado.peso.liquidez": 1.0, "balanceado.peso.robustez": 1.0,
              "decision.tolerancia_equivalencia": 0.05, "montecarlo.n": 200, "montecarlo.semilla": 20261005,
              "montecarlo.incluir_tir": False,
              "consulta.capital_usd": 16000.0, "consulta.demanda_t_dia": 0.004, "consulta.payback_max_anios": 5.0,
              "umbral.dscr_2d": 1.2, "umbral.payback_2d": 5.0,
              "tornado.metricas": ["VAN", "EBITDA", "PICO_FONDOS", "PAYBACK", "DSCR"]})
    return a


def stress_artificiales():
    base = [("ST-DEM", "Stress demanda", {"demanda": -0.30}), ("ST-ALI", "Stress alimento", {"alimento": 0.20}),
            ("ST-PRE", "Stress precio", {"precio_venta": -0.10}), ("ST-CAP", "Stress CAPEX", {"capex": 0.25}),
            ("ST-RAMP", "Stress ramp-up", {"rampup": 1.0}), ("ST-FIN", "Stress financiero", {"tasa_descuento": 0.5, "dias_cobro": 30.0}),
            ("ST-COMB", "Stress combinado", {"precio_venta": -0.10, "alimento": 0.20, "demanda": -0.20, "capex": 0.25})]
    return [{"ID_STRESS": i, "NOMBRE": n, "shocks": s, "pendientes": [], "activo": True, "estado": {"ARTIFICIAL"},
             "origen": {"ARTIFICIAL"}} for i, n, s in base]


def dist_artificiales():
    D = [("precio_venta", "TRIANGULAR", {"min": -0.2, "moda": 0.0, "max": 0.15}),
         ("alimento", "NORMAL_TRUNCADA", {"media": 0.0, "desvio": 0.1, "min": -0.3, "max": 0.4}),
         ("demanda", "UNIFORME", {"min": -0.2, "max": 0.05}),
         ("capex", "TRIANGULAR", {"min": -0.05, "moda": 0.0, "max": 0.3})]
    dists = [mr.validar_distribucion({"VARIABLE": v, "DISTRIBUCION": t, "PARAMETROS": p, "FUENTE": "ARTIFICIAL", "ESTADO": "ARTIFICIAL"})
             for v, t, p in D]
    corrs = [{"A": "precio_venta", "B": "alimento", "RHO": 0.5, "ESTADO": "ARTIFICIAL", "FUENTE": "ARTIFICIAL"},
             {"A": "demanda", "B": "precio_venta", "RHO": 0.0, "ESTADO": "ARTIFICIAL",
              "FUENTE": "ARTIFICIAL: independencia declarada explícitamente (cero explícito, no faltante)"}]
    return dists, corrs


# ---------------------------------------------------------------------------------------------
# 15. CORRIDAS COMPLETAS
# ---------------------------------------------------------------------------------------------
def consultas(U, inp):
    E, fs = U["E"], U["fichas"]
    obj = mr.como_lista(inp.get("consulta.objetivos") or "MAX_VAN")
    cap, cap_dec = consulta_capital(fs, mr.num(inp.get("consulta.capital_usd")), inp, obj)
    dem, concl = consulta_demanda(E, fs, mr.num(inp.get("consulta.demanda_t_dia")), inp)
    pb = consulta_payback(E, fs, mr.num(inp.get("consulta.payback_max_anios")), inp)
    for x in cap + cap_dec:
        x.setdefault("UNIVERSO", U["universo"])
    if concl:
        dem.append({"ALTERNATIVA": "CONCLUSION", "UNIVERSO": U["universo"], "ESTADO": concl["CONCLUSION"],
                    "ETIQUETA": etiqueta(U["universo"])})
    return {"consulta_capital.csv": cap + [dict(d, ALTERNATIVA="MEJOR_CON_CAPITAL") for d in cap_dec],
            "consulta_demanda.csv": dem, "consulta_payback.csv": pb}


def correr_proyecto(inp=None, escenario=None, carpeta=AQUI, verbose=True):
    inp = inp or mr.leer_inputs()[0]
    escenario = escenario if escenario is not None else leer_escenario()
    stresses = mr.leer_stress()
    dists, corrs = mr.leer_distribuciones(), mr.leer_correlaciones()
    U_ev = correr_universo(alternativas_reales(inp, "EVIDENCIA"), inp, "EVIDENCIA")
    U_ev["prio_ev"] = prioridad_evidencia(U_ev["E"], U_ev["fichas"])
    U_es = correr_universo(alternativas_reales(inp, "ESCENARIO", escenario), inp, "ESCENARIO", stresses, dists, corrs)
    extra = {}
    for U in (U_ev, U_es):
        for k, v in consultas(U, inp).items():
            extra[k] = extra.get(k, []) + v
    extra["que_hacer"] = que_hacer_ahora(U_ev["prio_ev"], U_es.get("prio_esc") or [], int(inp.get("que_hacer.n") or 10))
    escribir_salidas([U_ev, U_es], carpeta, extra)
    reg = mr.leer_registro_riesgos()
    sw = {t["VARIABLE"]: t["SWING"] for t in U_es["tornado"] if t["METRICA"] == "VAN" and t.get("SWING") is not None}
    mr.escribir(os.path.join(carpeta, "matriz_riesgos.csv"), mr.matriz_riesgos(reg, sw),
                list(mr.matriz_riesgos(reg[:1])[0].keys()))
    mr.escribir(os.path.join(carpeta, "registro_variables_riesgo.csv"), mr.registro_variables_filas(inp),
                list(mr.registro_variables_filas(inp)[0].keys()))
    esp = espacio_decisiones(inp)
    mr.escribir(os.path.join(carpeta, "espacio_decisiones.csv"), esp, ["ID_COMBINACION"] + [k.upper() for k in DIMENSIONES] +
                ["CLASIFICACION", "CONFIGURACIONES_DEL_MAPA", "ALTERNATIVAS_ECONOMICAS", "MOTIVO"])
    resumen = resumen_corrida([U_ev, U_es], inp, "PROYECTO")
    mr.escribir(os.path.join(carpeta, "resumen_corrida.csv"), resumen, list(resumen[0].keys()))
    if verbose:
        for U in (U_ev, U_es):
            d = next(d for d in U["decisiones"] if d["OBJETIVO"] == "MAX_VAN")
            print(f"  {U['universo']}: {len(U['fichas'])} alternativas; MAX_VAN → {d['ESTADO']} ({d.get('MEJOR')})")
        c = {}
        for r in esp:
            c[r["CLASIFICACION"]] = c.get(r["CLASIFICACION"], 0) + 1
        print("  espacio de decisiones:", c)
    return U_ev, U_es, extra


def correr_artificial(inp=None, carpeta=DIR_CASOS, verbose=True):
    inp = inputs_artificiales(inp or mr.leer_inputs()[0])
    dists, corrs = dist_artificiales()
    U = correr_universo(caso_artificial(), inp, "ARTIFICIAL_TEST", stress_artificiales(), dists, corrs)
    extra = consultas(U, inp)
    U["prio_ev"] = []
    extra["que_hacer"] = que_hacer_ahora([], U["prio_esc"], 10)
    escribir_salidas([U], carpeta, extra)
    resumen = resumen_corrida([U], inp, "ARTIFICIAL_TEST")
    mr.escribir(os.path.join(carpeta, "resumen_corrida.csv"), resumen, list(resumen[0].keys()))
    if verbose:
        for d in U["decisiones"]:
            print(f"  [ARTIFICIAL] {d['OBJETIVO']}: {d['ESTADO']} → {d.get('MEJOR')} / 2.ª {d.get('SEGUNDA', '—')} "
                  f"({d.get('ROBUSTEZ_DECISION', '')[:60]})")
    return U, extra


def resumen_corrida(Us, inp, nombre):
    h = hashlib.sha256(json.dumps(inp, sort_keys=True, default=str).encode()).hexdigest()[:16]
    return [{"CORRIDA": nombre, "UNIVERSO": U["universo"], "VERSION": VERSION, "FECHA_MODELO": FECHA,
             "N_ALTERNATIVAS": len(U["fichas"]), "N_COMPLETAS": sum(1 for f in U["fichas"] if f["completa"] and f["alt"]["tipo"] != SQ),
             "N_EVALUACIONES_MOTOR": U["E"].n_eval, "N_ACIERTOS_CACHE": U["E"].n_hit,
             "SEMILLA_MC": inp.get("montecarlo.semilla"), "N_SIMULACIONES": inp.get("montecarlo.n"), "HASH_INPUTS": h,
             "OBJETIVOS": "|".join(objetivos_de(inp)), "ETIQUETA": etiqueta(U["universo"])} for U in Us]


# ---------------------------------------------------------------------------------------------
# 16. CLI
# ---------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description="Riesgos, sensibilidades y optimizador (sesión 20)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--escenario", help="JSON del universo ESCENARIO (ver escenario_optimizador.json)")
    ap.add_argument("--salida", help="carpeta de salida para --escenario")
    a = ap.parse_args()
    import tests_riesgo_optimizador as T
    print(f"RIESGOS + SENSIBILIDADES + OPTIMIZADOR v{VERSION} ({FECHA})")
    fallas, n = T.ejecutar_tests(verbose=True)
    if fallas:
        for f in fallas:
            print("FALLA", *f)
        sys.exit(1)
    if a.mutaciones:
        sys.exit(0 if T.prueba_mutaciones() else 1)
    if a.solo_tests:
        return
    if a.escenario:
        correr_proyecto(escenario=leer_escenario(a.escenario), carpeta=a.salida or os.path.join(AQUI, "salida_escenario"))
        return
    print("Proyecto (universos EVIDENCIA y ESCENARIO):")
    correr_proyecto()
    print("Caso artificial (casos_prueba/):")
    correr_artificial()


if __name__ == "__main__":
    main()
