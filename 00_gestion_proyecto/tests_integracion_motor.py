#!/usr/bin/env python3
"""
TESTS DE INTEGRACIÓN FINAL DEL MOTOR v1 — sesión 21 (auditoría + reconciliación final), 2026-10-05
================================================================================================

Qué prueba (además de las suites de cada módulo, que se corren aparte):
  * que los módulos hablen el mismo idioma: IDs centrales, arquitecturas C0–CF, variantes, escalas, unidades, tiempo;
  * identidades de punta a punta sobre un CASO ARTIFICIAL completo (demanda → producción → ventas → CAPEX → OPEX →
    CT → flujo → VAN/TIR → riesgo → optimizador) con valores INVENTADOS y verificables a mano (nunca es el proyecto);
  * que un faltante nunca se publique como 0, que la evidencia no se altere con escenarios, que el optimizador
    rankee solo alternativas comparables y que NO_INVERTIR_AUN no tenga métricas;
  * MUTACIONES DE INTEGRACIÓN: errores sembrados entre módulos (no locales) que los detectores deben atrapar;
  * integridad del repositorio (merge markers, CSV, links, caches, IDs provisionales activos).

No modifica ningún modelo ni ninguna salida del proyecto. Lee los motores 19–22 y los registros de 00/25.
`--generar` escribe `cobertura_motor.csv` (métrica transversal de cobertura, derivada de los motores).

Uso
    python3 00_gestion_proyecto/tests_integracion_motor.py              # tests + mutaciones de integración
    python3 00_gestion_proyecto/tests_integracion_motor.py --generar    # regenera cobertura_motor.csv y corre todo
El script termina con código 1 si falla un test o si una mutación no es detectada.
"""
import argparse
import copy
import csv
import hashlib
import io
import json
import math
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for d in ("21_modelo_financiero", "22_riesgos"):
    p = os.path.join(RAIZ, d)
    if p not in sys.path:
        sys.path.insert(0, p)
import modelo_financiero as mf      # noqa: E402
import motor_riesgo as mr           # noqa: E402
import modelo_optimizador as mopt   # noqa: E402

mcx, mo, mb, me = mf.mcx, mf.mo, mf.mb, mf.me
VERSION = "1.0"
FECHA = "2026-10-05"
TOL = 1e-6
BASES = ("C0", "C1", "C2", "C3", "CF")
DIM = mopt.DIMENSIONES
ARCH_MAESTRAS = os.path.join(AQUI, "arquitecturas_maestras.csv")
ARCH_COBERTURA = os.path.join(AQUI, "cobertura_motor.csv")
ARCH_TENSIONES = os.path.join(AQUI, "tensiones_finales.csv")
ARCH_RECONC = os.path.join(AQUI, "reconciliacion_sesiones_19_20.md")
# Archivos HISTÓRICOS: pueden conservar IDs provisionales (están marcados como tales).
HISTORICOS = (re.compile(r"(^|/)actualizaciones_gestion_[0-9A-Z]+\.md$"),
              re.compile(r"(^|/)fuentes_[0-9]{2}[A-D]?\.csv$"),
              re.compile(r"^00_gestion_proyecto/reconciliacion_sesiones_[0-9_]+\.md$"))
EXT_TEXTO = (".md", ".csv", ".py", ".json", ".js", ".html", ".txt")
# patrón de ID provisional de las sesiones paralelas: prefijo, sesión de 2 dígitos (+ letra opcional) y número o "##"
PROVISIONAL = re.compile(r"\b(?:SUP|DPV|DEC|FTE)-[0-9]{2}[A-D]?-[0-9#]{2,3}\b")


def _ok(cond, detalle=""):
    return bool(cond), detalle


def silencio(fn, *a, **k):
    with redirect_stdout(io.StringIO()):
        return fn(*a, **k)


def archivos_repo():
    """Archivos versionados (git ls-files) + nuevos no ignorados."""
    out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"], cwd=RAIZ,
                         capture_output=True, text=True, check=True).stdout.split("\n")
    return sorted(f for f in out if f and os.path.exists(os.path.join(RAIZ, f)))


def texto(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8") as fh:
        return fh.read()


def es_historico(rel):
    return any(p.search(rel) for p in HISTORICOS)


def ids_registro(nombre, pref):
    ids = []
    for linea in texto(f"00_gestion_proyecto/{nombre}").split("\n"):
        m = re.match(rf"^\| ({pref}-\d{{3}}) \|", linea)
        if m:
            ids.append(m.group(1))
    return ids


def leer_csv(rel):
    with open(os.path.join(RAIZ, rel), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


# =============================================================================================
# A. IDs Y REGISTROS
# =============================================================================================
def t_id01():
    """ID01 sin IDs provisionales activos (solo en archivos históricos marcados)"""
    malos = []
    for f in archivos_repo():
        if not f.endswith(EXT_TEXTO) or es_historico(f):
            continue
        for i, l in enumerate(texto(f).split("\n"), 1):
            for m in PROVISIONAL.findall(l):
                malos.append(f"{f}:{i} {m}")
    return _ok(not malos, "; ".join(malos[:8]) + (f" … ({len(malos)})" if len(malos) > 8 else ""))


def t_id02():
    """ID02 IDs centrales únicos y correlativos en supuestos, DPV, decisiones y fuentes"""
    det = []
    for nombre, pref in (("supuestos.md", "SUP"), ("datos_por_validar.md", "DPV"), ("decisiones_pendientes.md", "DEC")):
        ids = ids_registro(nombre, pref)
        nums = [int(x[4:]) for x in ids]
        if len(ids) != len(set(ids)):
            det.append(f"{pref} duplicados")
        if sorted(nums) != list(range(1, max(nums) + 1)):
            det.append(f"{pref} no correlativos: faltan {sorted(set(range(1, max(nums) + 1)) - set(nums))[:5]}")
        det.append(f"{pref}-001…{pref}-{max(nums):03d}")
    fte = [r["id"] for r in leer_csv("25_fuentes/registro_fuentes.csv")]
    if len(fte) != len(set(fte)):
        det.append("FTE duplicados")
    det.append(f"FTE-001…{max(fte)}")
    return _ok(not [d for d in det if "duplic" in d or "no correl" in d], "; ".join(det))


def t_id03():
    """ID03 toda referencia SUP/DPV/DEC/FTE/TF en archivos activos existe en su registro central"""
    reg = set(ids_registro("supuestos.md", "SUP") + ids_registro("datos_por_validar.md", "DPV") +
              ids_registro("decisiones_pendientes.md", "DEC"))
    reg |= {r["id"] for r in leer_csv("25_fuentes/registro_fuentes.csv")}
    reg |= {r["ID"] for r in leer_csv(f"00_gestion_proyecto/{os.path.basename(ARCH_TENSIONES)}")}
    malos = set()
    for f in archivos_repo():
        if not f.endswith(EXT_TEXTO) or es_historico(f) or f.endswith("tests_integracion_motor.py"):
            continue
        for m in re.findall(r"\b((?:SUP|DPV|DEC|FTE)-\d{3}|TF-\d{3})\b", texto(f)):
            if m not in reg:
                malos.add(f"{f}:{m}")
    return _ok(not malos, "; ".join(sorted(malos)[:10]))


def t_id04():
    """ID04 cada DPV del registro tiene fila en matriz_validacion_campo.csv (y viceversa)"""
    d = set(ids_registro("datos_por_validar.md", "DPV"))
    m = {r["ID_DPV"] for r in leer_csv("00_gestion_proyecto/matriz_validacion_campo.csv")}
    return _ok(d == m, f"solo en registro {sorted(d - m)[:5]}; solo en matriz {sorted(m - d)[:5]}; {len(d)} DPV")


def t_id05():
    """ID05 mapa de reconciliación 19–20 completo: cada propuesta provisional tiene un ID central existente"""
    props = set()
    for f in ("21_modelo_financiero/actualizaciones_gestion_19.md", "22_riesgos/actualizaciones_gestion_20.md"):
        props |= set(re.findall(r"^\| ((?:SUP|DPV|DEC)-(?:19|20)-\d{2}) \|", texto(f), re.M))
    mapa = {}
    for l in texto(os.path.relpath(ARCH_RECONC, RAIZ)).split("\n"):
        m = re.match(r"^\| ((?:SUP|DPV|DEC)-(?:19|20)-\d{2}) \| \*\*((?:SUP|DPV|DEC|TF)-\d{3})\*\*", l)
        if m:
            mapa[m.group(1)] = m.group(2)
    reg = set(ids_registro("supuestos.md", "SUP") + ids_registro("datos_por_validar.md", "DPV") +
              ids_registro("decisiones_pendientes.md", "DEC")) | {r["ID"] for r in leer_csv("00_gestion_proyecto/tensiones_finales.csv")}
    sin = sorted(props - set(mapa))
    inex = sorted(k for k, v in mapa.items() if v not in reg)
    return _ok(props and not sin and not inex, f"{len(props)} propuestas; sin mapa {sin[:5]}; destino inexistente {inex[:5]}")


# =============================================================================================
# B. INTEGRIDAD DEL REPOSITORIO
# =============================================================================================
def t_rp01():
    """RP01 sin marcadores de merge"""
    malos = [f for f in archivos_repo() if f.endswith(EXT_TEXTO) and
             re.search(r"^(<<<<<<< |>>>>>>> )", texto(f), re.M)]
    return _ok(not malos, ", ".join(malos))


def t_rp02():
    """RP02 todos los CSV parsean y tienen el mismo número de columnas que su encabezado"""
    malos, n = [], 0
    for f in archivos_repo():
        if not f.endswith(".csv"):
            continue
        n += 1
        with open(os.path.join(RAIZ, f), encoding="utf-8", newline="") as fh:
            filas = list(csv.reader(fh))
        if not filas or not all(filas[0]):
            malos.append(f"{f}: encabezado vacío")
            continue
        malas = [i for i, r in enumerate(filas[1:], 2) if r and len(r) != len(filas[0])]
        if malas:
            malos.append(f"{f}: filas {malas[:3]}")
    return _ok(not malos, f"{n} CSV; " + "; ".join(malos[:5]))


def t_rp03():
    """RP03 links internos de los .md resuelven a archivos existentes"""
    malos, n = [], 0
    for f in archivos_repo():
        if not f.endswith(".md"):
            continue
        base = os.path.dirname(os.path.join(RAIZ, f))
        for destino in re.findall(r"\]\(([^)\s]+)\)", texto(f)):
            if re.match(r"^(https?:|mailto:|#)", destino):
                continue
            n += 1
            ruta = destino.split("#")[0]
            if ruta and not os.path.exists(os.path.normpath(os.path.join(base, ruta))):
                malos.append(f"{f} → {destino}")
    return _ok(not malos, f"{n} links; " + "; ".join(malos[:6]))


def t_rp04():
    """RP04 sin caches, scratch ni temporales versionados"""
    pat = re.compile(r"(__pycache__|\.pyc$|\.ipynb_checkpoints|\.DS_Store|~$|\.tmp$|\.bak$|\.swp$|(^|/)scratch|(^|/)tmp/|\.log$)")
    malos = [f for f in archivos_repo() if pat.search(f)]
    return _ok(not malos, ", ".join(malos[:10]))


def t_rp05():
    """RP05 cada carpeta temática 01–24 tiene README.md (regla del README raíz; 25_fuentes es el registro maestro)"""
    falt = [d for d in sorted(os.listdir(RAIZ)) if re.match(r"^(0[1-9]|1\d|2[0-4])_", d)
            and not os.path.exists(os.path.join(RAIZ, d, "README.md"))]
    return _ok(not falt, ", ".join(falt))


def t_rp06():
    """RP06 cobertura_motor.csv está al día con los motores (salida generada no desactualizada)"""
    actual = leer_csv(os.path.relpath(ARCH_COBERTURA, RAIZ))
    nuevo = [{k: str(v) for k, v in r.items()} for r in filas_cobertura()]
    norm = lambda rs: [{k: (f"{float(v):.6f}" if re.match(r"^-?\d+(\.\d+)?$", v or "") else v) for k, v in r.items()} for r in rs]
    return _ok(norm(actual) == norm(nuevo), f"{len(actual)} filas vs {len(nuevo)} regeneradas")


# =============================================================================================
# C. ARQUITECTURAS C0–CF Y VARIANTES
# =============================================================================================
def dims(c):
    return tuple(c.get(k) for k in DIM)


def t_ar01():
    """AR01 C0–CF significan lo mismo en CAPEX (preset), OPEX (config_opex), financiero (configs) y optimizador"""
    det = []
    for b in BASES:
        p = mcx.preset(b)
        o = mo.config_opex(b)
        for esc in (2500, 10000, 20000):
            cc, co = mf.configs(f"{b}-{esc}")
            if not (dims(p) == dims(o) == dims(cc) == dims(co)):
                det.append(f"{b}-{esc}")
    alts = [a for a in mopt.alternativas_reales(mr.leer_inputs()[0], "EVIDENCIA") if a["tipo"] != mr.STATUS_QUO]
    for a in alts:
        if a["variante"] == "BASE" and dims(a["cc"]) != dims(mcx.preset(a["configuracion"])):
            det.append(a["id"])
    return _ok(not det, f"{len(alts)} alternativas del optimizador; difieren: {det}")


def t_ar02():
    """AR02 tabla maestra arquitecturas_maestras.csv = presets de los motores (atributo por atributo)"""
    filas = {r["CONFIGURACION"]: r for r in leer_csv(os.path.relpath(ARCH_MAESTRAS, RAIZ))}
    det = []
    col = {"faena": "FAENA", "granjas": "GRANJAS", "pollito": "POLLITO", "alimento": "ALIMENTO", "flota": "FLOTA",
           "frio": "FRIO", "subproductos": "SUBPRODUCTOS", "rendering": "RENDERING", "reproductoras": "UPSTREAM_REPRODUCTORAS"}
    for r in mf.mapa_arquitecturas():
        nombre = r["CONFIGURACION"]
        ref = r["ESCENARIO_REFERENCIA"] if r["TIPO"] == "VARIANTE" else f"{nombre}-10000"
        cc, co = mf.configs(ref)
        m = filas.get(nombre)
        if m is None:
            det.append(f"{nombre} falta en la tabla maestra")
            continue
        for k, c in col.items():
            v = m[c].split(" ")[0]
            if v != str(cc[k]) or v != str(co[k]):
                det.append(f"{nombre}.{c}={m[c]!r} ≠ {cc[k]!r}")
    extra = set(filas) - {r["CONFIGURACION"] for r in mf.mapa_arquitecturas()}
    if extra:
        det.append(f"filas sin configuración del mapa: {sorted(extra)}")
    return _ok(not det, f"{len(filas)} filas; " + "; ".join(det[:6]))


def _modulos_capex(b, esc=10000):
    cc, _ = mf.configs(f"{b}-{esc}")
    filas, _, _ = mf._correr_capex(cc)
    return {f["MODULO"] for f in filas if f["COSTEA"] and f["TITULAR"] == "EMPRESA" and f["FASE"] == "INICIAL"}


def _modulos_opex(b, esc=10000):
    _, co = mf.configs(f"{b}-{esc}")
    fo = mf._correr_opex(co)[0]
    return {f["MODULO"] for f in fo if f["COSTEA"]}


def _gates(b, esc=10000):
    cc, _ = mf.configs(f"{b}-{esc}")
    alt = {"cc": cc, "escalas": (esc,), "disponibilidad": {}}
    return {g["GATE"]: g for g in mopt.factibilidad_fisica_real(alt)["gates"]}


def t_ar03():
    """AR03 (test 51) C0 sin activos de planta; C1 con faena propia; C3 con upstream propio — igual en CAPEX, OPEX, financiero y optimizador"""
    det = []
    planta = {"PROCESO", "FRIO", "TERRENO", "AGUA", "EFLUENTES", "ELECTRICIDAD", "TERMICO"}
    upstream = {"INCUBACION", "ALIMENTO", "GRANJAS"}
    k0, k1, k3 = _modulos_capex("C0"), _modulos_capex("C1"), _modulos_capex("C3")
    if k0 & (planta | upstream):
        det.append(f"C0 CAPEX con {sorted(k0 & (planta | upstream))}")
    if not planta <= k1 or k1 & upstream:
        det.append(f"C1 CAPEX planta {sorted(planta - k1)} faltan / upstream {sorted(k1 & upstream)}")
    if not (planta | upstream) <= k3:
        det.append(f"C3 CAPEX sin {sorted((planta | upstream) - k3)}")
    o0, o1, o3 = _modulos_opex("C0"), _modulos_opex("C1"), _modulos_opex("C3")
    if "INCUBACION" in o0 | o1 or "INCUBACION" not in o3 or "EFLUENTES" in o0 or "EFLUENTES" not in o1:
        det.append(f"OPEX módulos C0 {sorted(o0)} / C1 / C3 incoherentes")
    g0, g1, g3 = _gates("C0"), _gates("C1"), _gates("C3")
    if "FACON_FAENA" not in g0 or "CAPACIDAD_LINEA" in g0 or "CAPACIDAD_LINEA" not in g1:
        det.append("gates faena C0/C1")
    if not {"HUEVO_FERTIL_INCUBACION", "SITIOS_GRANJAS_PROPIAS", "ALIMENTO_PROPIA"} <= set(g3):
        det.append(f"gates upstream C3: {sorted(g3)}")
    for b in ("C0", "C1", "C3"):
        P, _ = silencio(mf.construir_entrada, "AR03", b, (10000,), "EVIDENCIA")
        dest = P["meta_productos"]["destino_c"]
        if (b == "C0") != (dest == "contrato_facon"):
            det.append(f"{b}: destino de subproductos {dest}")
    return _ok(not det, "; ".join(det))


def t_ar04():
    """AR04 variantes: ID único, base existente, mismos inputs en CAPEX y OPEX, solo cambian atributos declarados"""
    mapa = mf.mapa_arquitecturas()
    ids = [r["CONFIGURACION"] for r in mapa]
    det = [] if len(ids) == len(set(ids)) else ["IDs duplicados"]
    bases = {r["CONFIGURACION"] for r in mapa if r["TIPO"] == "CONFIGURACION_BASE"}
    cambios = {"C1-congelado_tercero": {"frio"}, "C1-congelado_propio": {"frio"}, "C1-subprod_basico": {"subproductos"}}
    for r in mapa:
        if r["TIPO"] != "VARIANTE":
            continue
        if r["VARIANTE_DE"] not in bases:
            det.append(f"{r['CONFIGURACION']}: base {r['VARIANTE_DE']} inexistente")
        cc, co = mf.configs(r["ESCENARIO_REFERENCIA"])
        if dims(cc) != dims(co):
            det.append(f"{r['CONFIGURACION']}: CAPEX ≠ OPEX")
        base = mcx.preset(r["VARIANTE_DE"])
        dif = {k for k in DIM if cc[k] != base[k]}
        if dif != cambios.get(r["CONFIGURACION"], set()):
            det.append(f"{r['CONFIGURACION']}: atributos cambiados {sorted(dif)}")
    return _ok(not det, f"{len(ids) - len(bases)} variantes; " + "; ".join(det))


# =============================================================================================
# D. ESCALAS, TIEMPO Y UNIDADES
# =============================================================================================
def t_es01():
    """ES01 capacidad mensual = aves/día operativo × días operativos/año ÷ 12 (250 con 5 d, 300 con 6 d); escalas intermedias"""
    det = []
    for ref, dias in (("C1-10000", 250), ("C1-10000-6dias", 300)):
        cc, _ = mf.configs(ref)
        if mcx.dias_anio(cc) != dias:
            det.append(f"{ref}: {mcx.dias_anio(cc)} días")
    for esc in (2500, 7500, 20000):
        cc, _ = mf.configs(f"C1-{esc}")
        P, _ = silencio(mf.construir_entrada, "ES01", "C1", (esc,), "EVIDENCIA")
        e = P["etapas"][0]
        if e["escala_aves_dia"] != esc or e["dias_operativos_anio"] != mcx.dias_anio(cc):
            det.append(f"C1-{esc}")
    if not (mcx.RANGO_ESCALA[0] <= 2500 and mcx.RANGO_ESCALA[1] >= 20000):
        det.append("rango de escalas")
    return _ok(not det, "; ".join(det) or f"rango {mcx.RANGO_ESCALA}")


def t_es02():
    """ES02 base temporal única de días calendario (DIAS_MES = 365/12) para demanda, CT e inventario del financiero"""
    det = []
    if abs(mf.DIAS_MES - 365 / 12) > 1e-12:
        det.append("DIAS_MES")
    if abs(mf.convertir_demanda(1.0, "kg/dia") - 365 / 12) > 1e-12 or abs(mf.convertir_demanda(1.0, "t/dia") - 1000 * 365 / 12) > 1e-9:
        det.append("convertir_demanda")
    try:
        mf.convertir_demanda(1.0, "kg/dia_operativo")
        det.append("unidad ambigua aceptada")
    except (mf.ErrorFinanciero, KeyError, TypeError):
        pass
    return _ok(not det, "; ".join(det))


def t_un01():
    """UN01 moneda: un precio en ARS sin TC, fecha y tipo de TC no se convierte en silencio; precio observado ≠ conversión"""
    det = []
    for kw in ({}, {"tc": 1000.0}, {"tc": 1000.0, "fecha_tc": "2026-07-01"}):
        try:
            mf.a_usd(1000.0, "ARS", **kw)
            det.append(f"ARS aceptado con {kw}")
        except mf.ErrorFinanciero:
            pass
    if abs(mf.a_usd(10.0, "USD") - 10.0) > TOL:
        det.append("USD")
    for r in leer_csv("21_modelo_financiero/base_precios_venta.csv"):
        if r["MONEDA"] == "ARS" and r["ESTADO"] == "CON_PRECIO" and not (r.get("TC_USADO") and r.get("FECHA_TC") and r.get("TIPO_TC")):
            det.append(f"{r['ID_PRECIO']} sin TC")
    return _ok(not det, "; ".join(det))


def t_un02():
    """UN02 OPEX: todo precio en ARS conserva PRECIO_ORIGINAL_OBSERVADO, MONEDA_ORIGINAL, TC_USADO y FECHA_TC"""
    det, n = [], 0
    for b in BASES:
        _, co = mf.configs(f"{b}-10000")
        for f in mf._correr_opex(co)[0]:
            if f.get("MONEDA_ORIGINAL") == "ARS":
                n += 1
                if not (f.get("PRECIO_ORIGINAL_OBSERVADO") and f.get("TC_USADO") and f.get("FECHA_TC")):
                    det.append(f"{b}:{f['COSTO_ID']}")
    return _ok(not det, f"{n} filas ARS; sin trazabilidad FX: {det[:5]}")


# =============================================================================================
# E. DEMANDA
# =============================================================================================
def t_dm01():
    """DM01 los ~90 supermercados no son demanda contable: el modo evidencia no tiene ventas en ninguna arquitectura"""
    det = []
    for b in BASES:
        P, _ = silencio(mf.construir_entrada, "DM01", b, (10000,), "EVIDENCIA")
        if P["demanda"] is not None:
            det.append(f"{b}: demanda {len(P['demanda'])} líneas")
        if not any("supermercados son canal potencial" in x for x in mf.disponibilidad(P)["DEMANDA"]):
            det.append(f"{b}: faltante de demanda sin la aclaración del canal potencial")
    ev = [f for f in leer_csv("21_modelo_financiero/inputs_financieros.csv") if f["VARIABLE"].startswith("demanda.")
          and f["ORIGEN"] == "EVIDENCIA_REAL"]
    if ev:
        det.append(f"{len(ev)} líneas de demanda con EVIDENCIA_REAL")
    return _ok(not det, "; ".join(det))


def t_dm02():
    """DM02 categorías: el modo evidencia vende solo DOCUMENTADA/ASEGURADA; POTENCIAL/INTERESADA/NEGOCIADA no se venden"""
    P = caso_e2e()
    P["modo"] = "EVIDENCIA"
    det = []
    for cat in ("POTENCIAL", "INTERESADA", "NEGOCIADA", "ESCENARIO"):
        Q = copy.deepcopy(P)
        Q["demanda"][0]["categoria"] = cat
        Q["categorias_demanda_usadas"] = mf.CATEGORIAS_DEMANDA
        Q["alfa_negociada"] = 1.0
        if mf._lineas_contables(Q):
            det.append(cat)
    Q = copy.deepcopy(P)
    Q["demanda"][0]["categoria"] = "ASEGURADA"
    Q["categorias_demanda_usadas"] = mf.CATEGORIAS_DEMANDA
    if not mf._lineas_contables(Q):
        det.append("ASEGURADA no vendible")
    return _ok(not det, "categorías vendidas en evidencia: " + ", ".join(det))


def t_dm03():
    """DM03 respaldo comercial separado de la rentabilidad: en ESCENARIO la demanda hipotética no se cuenta como asegurada"""
    R = mf.simular(caso_e2e())
    m = mr.metricas(mf.resultados(R), R)
    return _ok(m["DEMANDA_ASEGURADA_PCT"] == 0.0 and m["VAN"] is not None,
               f"demanda asegurada {m['DEMANDA_ASEGURADA_PCT']} con VAN de escenario {m['VAN']}")


# =============================================================================================
# F. BALANCE DE MASA Y PRODUCTOS
# =============================================================================================
def t_bm01():
    """BM01 identidad de masa por ruta: entrada viva (+ agua) = salidas; componentes asignados a un solo producto"""
    det = []
    comp_items = [c for _, _, cs in me.ITEMS for c in cs]
    if len(comp_items) != len(set(comp_items)):
        det.append("componente en dos productos")
    for cfg in ("A", "B", "C"):
        b = mb.balance(me.PESO_REF, cfg, me.REND, me.COND, me.ENF, None)
        sb, sa = sum(f["bio"] for f in b["filas"]), sum(f["agua"] for f in b["filas"])
        if abs(sb - b["entrada_bio"]) > 1e-9 or abs(sa - b["entrada_agua"]) > 1e-9:
            det.append(f"{cfg}: bio {sb:.6f}/{b['entrada_bio']:.6f} agua {sa:.6f}/{b['entrada_agua']:.6f}")
        sin = {f["componente"] for f in b["filas"]} - set(comp_items)
        if sin:
            det.append(f"{cfg}: componentes sin producto {sorted(sin)}")
    return _ok(not det, "; ".join(det))


def t_bm02():
    """BM02 (test 9) entero / trozado / deshuesado / CMS: rutas exclusivas; nunca carcasa entera + sus cortes de la misma ave"""
    det = []
    for cfg in ("A", "B", "C"):
        pr, meta = mf.productos_balance(cfg)
        kg = {k: (v["kg_ave"] or 0.0) for k, v in pr.items()}
        tot = sum(kg.values())
        if tot > meta["peso_vivo"] + meta["agua_incorporada"] + 1e-9:
            det.append(f"{cfg}: vendible {tot:.4f} > masa {meta['peso_vivo'] + meta['agua_incorporada']:.4f}")
        if kg["cms"] > 0 and kg["carcasa_esqueleto"] > 0:
            det.append(f"{cfg}: CMS y esqueleto simultáneos")
        if cfg == "A":
            b = mb.balance(me.PESO_REF, "A", me.REND, me.COND, me.ENF, None)
            ent = sum(f["bio"] + f["agua"] for f in b["filas"] if f["componente"] == "pollo entero")
            cortes = sum(kg[k] for k in ("pechuga", "pata_muslo", "alas", "carcasa_esqueleto"))
            # en A, los cortes provienen solo de carcasas degradadas (no aptas para entero): entero + cortes ≤ carcasa
            if ent + cortes > b["carcasa_fria_bio"] + b["agua_retenida_producto"] + 1e-6:
                det.append("A: entero + cortes > carcasa disponible")
    return _ok(not det, "; ".join(det))


def t_bm03():
    """BM03 agua retenida separada: kg comerciales = biológicos + agua; el validador del financiero rechaza masa duplicada"""
    pr, meta = mf.productos_balance("B")
    P = caso_e2e()
    P["productos"] = copy.deepcopy(pr)
    P["meta_productos"] = meta
    P["demanda"][0]["producto"] = "pechuga"
    ok_base = not _lanza(mf.validar_entrada, P)
    Q = copy.deepcopy(P)
    Q["productos"]["pollo_entero"]["kg_ave"] = mf.productos_balance("A")[0]["pollo_entero"]["kg_ave"]   # ave entera + sus cortes
    return _ok(ok_base and _lanza(mf.validar_entrada, Q) and meta["agua_incorporada"] > 0,
               f"agua incorporada {meta['agua_incorporada']:.4f} kg/ave")


def _lanza(fn, *a, **k):
    try:
        silencio(fn, *a, **k)
    except (mf.ErrorFinanciero, mr.ErrorRiesgo, mcx.ErrorCapex, mo.ErrorOpex, mb.ErrorBalance):
        return True
    return False


# =============================================================================================
# G. UTILITIES, RRHH, UPSTREAM, CT (universos y propiedad)
# =============================================================================================
def t_ut01():
    """UT01 electricidad de frío, efluentes y bombeo INCLUIDA en UT-ELE-KWH (no se costea dos veces); un kWh costeado por universo"""
    det = []
    for b in ("C1", "C3"):
        _, co = mf.configs(f"{b}-10000")
        fo = mf._correr_opex(co)[0]
        ele = [f for f in fo if f["COSTO_ID"] == "UT-ELE-KWH"]
        inc = [f for f in fo if f.get("INCLUIDO_EN") == "UT-ELE-KWH"]
        if len(ele) != 1 or not inc or any(f["COSTEA"] for f in inc):
            det.append(f"{b}: UT-ELE-KWH {len(ele)}; incluidos {len(inc)} costeados {sum(1 for f in inc if f['COSTEA'])}")
        faena = [f for f in fo if f["COSTEA"] and f["UNIDAD"] == "kWh" and f.get("UNIVERSO_UTILITIES") == "FAENA_09C"]
        if len(faena) != 1 or not detector_electricidad(fo):
            det.append(f"{b}: filas kWh costeadas del universo faena {[f['CONCEPTO'][:30] for f in faena]}")
    return _ok(not det, "; ".join(det))


def t_ut02():
    """UT02 utilities y RRHH de faena (09C/14A) no se extrapolan a upstream: incubación, planta de alimento y granjas PENDIENTES en C3"""
    _, co = mf.configs("C3-10000")
    fo = mf._correr_opex(co)[0]
    det = []
    for f in fo:
        uu, ur = f.get("UNIVERSO_UTILITIES") or "", f.get("UNIVERSO_RRHH") or ""
        if uu in ("INCUBACION", "PLANTA_ALIMENTO", "TRATAMIENTO_SUBPRODUCTOS") and f["ESTADO_DIMENSION"] != "PENDIENTE":
            det.append(f"utilities {uu}:{f['CONCEPTO'][:30]} {f['ESTADO_DIMENSION']}")
        if ur.endswith("_PENDIENTE") and f["ESTADO_DIMENSION"] != "PENDIENTE":
            det.append(f"RRHH {ur} {f['ESTADO_DIMENSION']}")
    ups = {f.get("UNIVERSO_RRHH") for f in fo}
    falt = {"RRHH_INCUBACION_PENDIENTE", "RRHH_PLANTA_ALIMENTO_PENDIENTE", "RRHH_GRANJAS_PROPIAS_PENDIENTE"} - ups
    if falt:
        det.append(f"universos RRHH upstream ausentes {sorted(falt)}")
    return _ok(not det, "; ".join(det[:6]))


def t_ut03():
    """UT03 (puntos 11–12) efluente: SST = g/ave × aves (no masa de subproductos); lodos PENDIENTES sin dimensionar"""
    sys.path.insert(0, os.path.join(RAIZ, "11_agua_efluentes"))
    import modelo_utilities as mu
    r = mu.calcular(10000)
    v = {f["variable"]: f["valor"] for f in r.filas}
    lod = [f for f in r.filas if f["bloque"] == "lodos"]
    det = []
    if abs(v["metodoA_carga_SST_kg_dia"] - v["metodoA_carga_SST_g_ave"] * 10000 / 1000) > 1e-9:
        det.append("SST no proviene de g/ave")
    sub = sum((p["kg_ave"] or 0) for k, p in mf.productos_balance("B")[0].items() if p["categoria_ingreso"] == "SUBPRODUCTOS") * 10000
    if abs(v["metodoA_carga_SST_kg_dia"] - sub) < 1e-6:
        det.append("SST = masa de subproductos")
    if not lod or any(f["valor"] is not None for f in lod):
        det.append("lodos dimensionados sin datos")
    return _ok(not det, f"SST {v['metodoA_carga_SST_kg_dia']:.0f} kg/día vs subproductos C {sub:.0f} kg/día; lodos PENDIENTES ({len(lod)} variables)")


def t_lo01():
    """LO01 (punto 13) localización: sin ranking emitido; contacto en Chaco sin peso; gates duros y condicionales separados"""
    res = leer_csv("10_localizacion/resultados_localizacion.csv")
    pesos = leer_csv("10_localizacion/pesos_localizacion.csv")
    det = []
    if any(r["ESTADO_RANKING"] not in ("NO_EMITIDO",) or r["POSICION"] for r in res if r["MODO"] == "estricto"):
        det.append("ranking emitido en modo estricto")
    if any(r["CRITERIO"] == "NETWORK" and float(r["PESO"] or 0) != 0 for r in pesos if r["PERFIL"] in "ABCD"):
        det.append("NETWORK con peso")
    txt = texto("10_localizacion/metodologia_localizacion.md")
    if not (re.search(r"gate[s]? dur", txt, re.I) and re.search(r"condicional", txt, re.I)):
        det.append("gates duros/condicionales no documentados por separado")
    return _ok(not det, f"{len(res)} filas de resultados; " + "; ".join(det))


def t_rh01():
    """RH01 (puntos 16 y 20) RR. HH. y agua sin doble conteo: faenador y servicios tercerizados INCLUIDOS en su tarifa; limpieza tercerizada reemplaza (no suma) la fila laboral; agua de limpieza INCLUIDA en UT-AGUA"""
    det = []
    _, co = mf.configs("C0-10000")
    fo = mf._correr_opex(co)[0]
    ter = [f for f in fo if f.get("UNIVERSO_RRHH", "").startswith("TERCERO_INCLUIDO")]
    if not ter or any(f["COSTEA"] for f in ter):
        det.append(f"C0: {sum(1 for f in ter if f['COSTEA'])} filas de terceros costeadas")
    for ref in ("C1-10000", "C1-10000-LIMPIEZA-TERC"):
        _, co = mf.configs(ref)
        fo = mf._correr_opex(co)[0]
        post = [f for f in fo if f["COSTEA"] and f["CONCEPTO"].startswith("Limpieza y sanitización post-producción")]
        if len(post) != 1:
            det.append(f"{ref}: limpieza post-producción costeada {len(post)} veces")
        agua = [f for f in fo if f["CONCEPTO"].startswith("Agua y energía de limpieza")]
        if not agua or any(f["COSTEA"] or "UT-AGUA" not in f["INCLUIDO_EN"] for f in agua):
            det.append(f"{ref}: agua de limpieza fuera de UT-AGUA")
    return _ok(not det, "; ".join(det))


def t_ct01():
    """CT01 solo stock propiedad de la empresa entra al CT (C0 vs C1 vs C3) y el CT del financiero respeta la propiedad"""
    det = []
    props = {b: mf.propiedad_inventarios(mf.configs(f"{b}-10000")[1]) for b in ("C0", "C1", "C3")}
    if props["C3"].get("materias_primas") is not True:
        det.append("C3: granos propios no entran al CT")
    if props["C1"].get("materias_primas") is True:
        det.append("C1: MP del proveedor de alimento entran al CT")
    P = caso_e2e(dias_cobro=0.0)
    P["inventarios"] = {"alimento": {"propiedad_empresa": False, "dias": 30.0, "base": "OPEX_TOTAL"},
                        "packaging": {"propiedad_empresa": True, "dias": 15.0, "base": "OPEX_TOTAL"}}
    S = mf.simular(P)["series"]
    if abs(S["inv_alimento"][13]) > TOL or abs(S["inv_packaging"][13] - 48 / 12 / mf.DIAS_MES * 15) > TOL:
        det.append(f"inventarios {S['inv_alimento'][13]} / {S['inv_packaging'][13]}")
    return _ok(not det, "; ".join(det) + f" | propiedad {props}")


# =============================================================================================
# H. CASO ARTIFICIAL DE PUNTA A PUNTA (test 49) — valores INVENTADOS y verificables a mano
# =============================================================================================
# Demanda 1,5 kg/mes de un producto de 1 kg/ave; planta de 1 ave/día × 12 días/año = 1 ave/mes (capacidad < demanda);
# precio 10 USD/kg → ventas 120/año; OPEX fijo 30 + variable 18 → EBITDA 72/año; CAPEX 200 en T0; cobro a 1 mes
# (DIAS_MES días) → CxC = 10 desde el mes 1 (ΔCT = 10 una sola vez); sin impuestos, IVA ni deuda; 5 años; 10 % anual
# efectiva; flujos a fin de año (PERIODO_REPORTE). Nada de esto es un dato del proyecto.
AF5 = (1 - 1.1 ** -5) / 0.1


def caso_e2e(dias_cobro=None):
    return mf.caso_prueba(H=5, capex=200.0, ventas_anio=120.0, opex_fijo=30.0, opex_var=18.0, demanda_kg_mes=1.5,
                          escala=1, dias=12, tasa=0.10, dias_cobro=mf.DIAS_MES if dias_cobro is None else dias_cobro,
                          convencion="PERIODO_REPORTE", nombre="E2E-ARTIFICIAL-01")


def esperado_e2e(precio=10.0):
    ing = 12 * precio
    ebitda = ing - 48.0
    fcff = [-200.0, ebitda - ing / 12] + [ebitda] * 4
    van = sum(f / 1.1 ** t for t, f in enumerate(fcff))
    lo, hi = -0.99, 10.0                     # TIR por bisección independiente del motor
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if sum(f / (1 + mid) ** t for t, f in enumerate(fcff)) > 0 else (lo, mid)
    acum, pb = 0.0, None
    for t, f in enumerate(fcff):
        if acum < 0 <= acum + f and t > 0:
            pb = (t - 1) + (-acum) / f
        acum += f
    return {"INGRESO": ing, "EBITDA": ebitda, "FCFF": fcff, "VAN": van, "TIR": (lo + hi) / 2, "PAYBACK": pb, "CT": ing / 12,
            "CAJA_FINAL": sum(fcff) + 200.0}


def t_e2e01():
    """E2E01 demanda → capacidad → producción → ventas: capacidad ≠ demanda ≠ producción; ventas ≤ mín(producción, demanda)"""
    R = mf.simular(caso_e2e())
    S = R["series"]
    k = 13
    det = []
    if not (abs(S["capacidad_aves"][k] - 1) < TOL and abs(S["aves_requeridas"][k] - 1.5) < TOL and abs(S["aves_faenadas"][k] - 1) < TOL):
        det.append("capacidad/requeridas/faenadas")
    if not (abs(S["u_comercial"][k] - 1.5) < TOL and abs(S["u_efectiva"][k] - 1) < TOL):
        det.append("utilizaciones")
    for kk in range(1, R["N"] + 1):
        for lid, pl in R["por_linea"].items():
            if pl["kg"][kk] > min(S["kg_producidos"][kk] + (S["kg_inventario"][kk - 1] if kk > 1 else 0), 1.5) + TOL:
                det.append(f"ventas > mín(producción, demanda) en mes {kk}")
    return _ok(not det, "; ".join(det) or "cap 1 / req 1,5 / faenadas 1 ave/mes; u_comercial 1,5; u_efectiva 1")


def t_e2e02():
    """E2E02 identidades contables mes a mes: neto, EBITDA, EBIT, CT, ΔCT, FCFF, FCFE y caja"""
    R = mf.simular(caso_e2e())
    S, N = R["series"], R["N"]
    det = []
    for k in range(N + 1):
        neto = S["venta_bruta"][k] - S["descuentos"][k] - S["bonificaciones"][k] - S["devoluciones"][k] - S["comisiones"][k] - S["derechos_exportacion"][k]
        eb = (S["ingreso_neto"][k] - S["opex_total"][k] - S["costos_logistica_canal"][k] - S["costos_exportacion"][k]
              - S["impuestos_sobre_ingresos"][k] - S["otros_impuestos"][k] - S["costos_extra_rampup"][k])
        ct = S["inventarios"][k] + S["cxc"][k] + S["caja_operativa"][k] - S["cxp"][k]
        dct = ct - (S["ct"][k - 1] if k else 0.0)
        fcff = S["ebitda"][k] - S["capex_total"][k] - S["delta_ct"][k] + S["flujo_iva"][k] + S["valor_terminal"][k]
        fin = -S["deuda_interes"][k] - S["deuda_comision"][k] + S["deuda_alta"][k] - S["deuda_amort"][k] - S["deuda_remanente_cierre"][k]
        for nom, a, b in (("neto", neto, S["ingreso_neto"][k]), ("EBITDA", eb, S["ebitda"][k]),
                          ("EBIT", S["ebitda"][k] - S["depreciacion"][k], S["ebit"][k]), ("CT", ct, S["ct"][k]),
                          ("ΔCT", dct, S["delta_ct"][k]), ("FCFF", fcff, S["fcff_pre"][k]), ("FCFE", fcff + fin, S["fcfe_pre"][k])):
            if abs(a - b) > 1e-9:
                det.append(f"{nom} mes {k}")
    if abs(sum(S["delta_ct"]) - S["ct"][N]) > 1e-9:
        det.append("Σ ΔCT ≠ CT final")
    if abs(S["caja"][N] - (sum(S["fcfe_pre"]) + sum(S["aportes"]) - sum(S["dividendos"]))) > 1e-9:
        det.append("caja")
    return _ok(not det, "; ".join(sorted(set(det))[:6]))


def t_e2e03():
    """E2E03 indicadores = cálculo manual (VAN, TIR, payback, EBITDA, fondos, caja) con el caso artificial"""
    res = mf.resultados(mf.simular(caso_e2e()))
    x = esperado_e2e()
    det = []
    for nom, a, b, tol in (("EBITDA", res["EBITDA_ULTIMO_ANIO"], x["EBITDA"], 1e-9), ("VAN", res["VAN"], x["VAN"], 1e-6),
                           ("TIR", res["TIR"], x["TIR"], 1e-6), ("PAYBACK", res["PAYBACK_SIMPLE_ANIOS"], x["PAYBACK"], 1e-6),
                           ("FONDOS", res["FONDOS_INICIALES"], 200.0 + x["CT"], 1e-9),
                           # pico (serie mensual): −200 en T0 y mes 1 = EBITDA 6 − ΔCT 10 = −4 → −204
                           ("PICO", res["PICO_REQUERIMIENTO_FONDOS"], 200.0 + x["CT"] - x["EBITDA"] / 12, 1e-9)):
        if a is None or abs(a - b) > tol * max(1, abs(b)):
            det.append(f"{nom} {a} ≠ {b}")
    if res["ETIQUETA"] != mf.ETIQUETA_SIM:
        det.append("etiqueta de simulación ausente")
    return _ok(not det, "; ".join(det) or f"VAN {x['VAN']:.4f}; TIR {x['TIR']:.4%}; payback {x['PAYBACK']:.4f} años")


def t_e2e04():
    """E2E04 riesgo: shock de precio −10 % (one-way) = recálculo manual; la base no cambia"""
    P = caso_e2e()
    antes = json.dumps(P, sort_keys=True, default=str)
    P2, info = mr.aplicar_shocks(P, {"precio_venta": -0.10}, {"precio_venta": 10.0}, "ESCENARIO")
    res = mf.resultados(mf.simular(P2))
    x = esperado_e2e(9.0)
    return _ok(json.dumps(P, sort_keys=True, default=str) == antes and abs(res["VAN"] - x["VAN"]) < 1e-6 and
               set(info["cambios"]) == {"precio_venta"},
               f"VAN con shock {res['VAN']:.4f} vs manual {x['VAN']:.4f}")


def t_e2e05():
    """E2E05 optimizador evalúa con el motor financiero (sin fórmulas propias) y el modo rápido solo omite la TIR"""
    alt = _alt_art("E2E", lambda: (caso_e2e(), None))
    E = mr.Evaluador()
    lento, rapido = E.evaluar(alt, tir=True), E.evaluar(alt, tir=False)
    res = mf.resultados(mf.simular(caso_e2e()))
    det = []
    if abs(lento["met"]["VAN"] - res["VAN"]) > 1e-12:
        det.append("VAN del optimizador ≠ motor")
    for k, v in lento["met"].items():
        if k in ("TIR", "TIR_ESTADO"):
            continue
        if rapido["met"].get(k) != v:
            det.append(f"modo rápido cambia {k}")
    if rapido["met"]["TIR"] is not None or rapido["res"].get("TIR_ESTADO") != mf.TIR_NO_CALCULADA:
        det.append("modo rápido publica TIR")
    return _ok(not det, "; ".join(det))


# =============================================================================================
# I. FINANCIERO: FCFF SIN DEUDA, PERIODICIDAD, VALOR TERMINAL, IMPUESTOS
# =============================================================================================
def t_fi01():
    """FI01 FCFF no contiene financiación: agregar deuda cambia FCFE y caja, nunca FCFF ni VAN del proyecto"""
    P = caso_e2e()
    P["tasa_descuento_accionista"] = 0.15
    Q = copy.deepcopy(P)
    Q["financiamiento"]["deudas"] = [{"id": "D1", "monto": 100.0, "tasa": 0.08, "tipo_tasa": "EFECTIVA_ANUAL", "base_tasa": "REAL",
                                      "plazo_meses": 36, "gracia_meses": 0, "metodo": "FRANCES", "frecuencia_meses": 1,
                                      "mes_desembolso": 0}]
    Ra, Rb = mf.simular(P), mf.simular(Q)
    ra, rb = mf.resultados(Ra), mf.resultados(Rb)
    same = all(abs(a - b) < 1e-12 for a, b in zip(Ra["series"]["fcff_pre"], Rb["series"]["fcff_pre"]))
    return _ok(same and abs(ra["VAN"] - rb["VAN"]) < 1e-12 and ra["VAN_ACCIONISTA"] != rb["VAN_ACCIONISTA"],
               f"VAN proyecto {ra['VAN']:.4f} = {rb['VAN']:.4f}; VAN accionista {ra['VAN_ACCIONISTA']:.4f} ≠ {rb['VAN_ACCIONISTA']:.4f}")


def t_fi02():
    """FI02 periodicidad: tasa mensual = (1+r)^(1/12)−1; VAN mensual = Σ F_k/(1+i)^k; TIR anual = (1+i_m)^12−1; payback meses/12"""
    P = caso_e2e()
    P["convencion_descuento"] = "MENSUAL"
    R = mf.simular(P)
    res = mf.resultados(R)
    i = 1.1 ** (1 / 12) - 1
    van = sum(f / (1 + i) ** k for k, f in enumerate(R["series"]["fcff_pre"]))
    det = []
    if abs(res["TASA_DESCUENTO_MENSUAL_EQUIVALENTE"] - i) > 1e-15:
        det.append("tasa mensual")
    if abs(res["VAN"] - van) > 1e-9:
        det.append(f"VAN mensual {res['VAN']} ≠ {van}")
    if abs((1 + res["TIR_MENSUAL"]) ** 12 - 1 - res["TIR"]) > 1e-12:
        det.append("TIR anualizada")
    if abs(res["PAYBACK_SIMPLE_ANIOS"] * 12 - res["PAYBACK_SIMPLE_MESES"]) > 1e-9:
        det.append("payback")
    Q = copy.deepcopy(P)
    Q["base_tasa"] = "NOMINAL"
    if not _lanza(mf.validar_entrada, Q):
        det.append("mezcla real/nominal aceptada")
    return _ok(not det, "; ".join(det) or f"i_m = {i:.6%}")


def t_fi03():
    """FI03 valor terminal: por defecto SIN_VALOR_TERMINAL (serie = 0); con método, la serie cierra la identidad del FCFF"""
    P = mf.entrada_vacia()
    det = [] if P["valor_terminal"]["metodo"] == "SIN_VALOR_TERMINAL" and not P["valor_terminal"]["recuperar_ct"] else ["default"]
    S = mf.simular(caso_e2e())["series"]
    if any(abs(x) > 0 for x in S["valor_terminal"]):
        det.append("VT ≠ 0 por defecto")
    for metodo, extra in (("PERPETUIDAD", {"g": 0.0}), ("VALOR_LIBRO", {}), ("EXPLICITO", {"monto": 50.0})):
        Q = caso_e2e()
        Q["valor_terminal"].update(metodo=metodo, recuperar_ct=True, **extra)
        R = mf.simular(Q)
        S2, N = R["series"], R["N"]
        ident = S2["ebitda"][N] - S2["capex_total"][N] - S2["delta_ct"][N] + S2["flujo_iva"][N] + S2["valor_terminal"][N]
        if abs(ident - S2["fcff_pre"][N]) > 1e-9:
            det.append(f"{metodo}: identidad FCFF no cierra ({ident:.4f} vs {S2['fcff_pre'][N]:.4f})")
    filas = [f for f in leer_csv("21_modelo_financiero/inputs_financieros.csv") if f["VARIABLE"] == "valor_terminal.metodo"]
    if not filas or any(f["VALOR"] not in ("", "SIN_VALOR_TERMINAL") for f in filas if f["ESCENARIO"] == "EVIDENCIA"):
        det.append("inputs: método de VT en evidencia")
    return _ok(not det, "; ".join(det))


def t_fi04():
    """FI04 impuestos: derechos de exportación en una sola ubicación; impuestos sobre ingresos una vez; IVA fuera del EBITDA"""
    det = []
    P = caso_e2e()
    P["impuestos"]["pct_derechos_exportacion"] = 0.05
    if not _lanza(mf.validar_entrada, P):
        det.append("derechos en el módulo de impuestos aceptados")
    P = caso_e2e()
    P["impuestos"]["pct_iibb"] = 0.03
    P["impuestos"]["iibb_aplica_domestico"] = True          # regla declarada en el caso artificial (TF-005)
    S = mf.simular(P)["series"]
    if abs(S["impuestos_sobre_ingresos"][13] - 0.03 * S["venta_bruta"][13]) > 1e-12:
        det.append("IIBB")
    P = caso_e2e()
    P["iva"] = {"modo": "SIMPLIFICADO", "alicuota_ventas": 0.105, "alicuota_compras": 0.21, "alicuota_capex": 0.105}
    S2 = mf.simular(P)["series"]
    S1 = mf.simular(caso_e2e())["series"]
    if any(abs(a - b) > 1e-12 for a, b in zip(S1["ebitda"], S2["ebitda"])):
        det.append("el IVA cambia el EBITDA")
    return _ok(not det, "; ".join(det))


def t_fi05():
    """FI05 publicabilidad: un número nunca se publica con su flag FALSE; el modo evidencia del proyecto publica 0 indicadores"""
    det = []
    for b in BASES:
        P, _ = silencio(mf.construir_entrada, "FI05", b, (10000,), "EVIDENCIA")
        res = mf.resultados(mf.simular(P))
        for fl in mf.FLAGS:
            if res.get(fl):
                det.append(f"{b}:{fl}")
        for c in ("VAN", "TIR", "EBITDA_ULTIMO_ANIO", "INGRESO_NETO_ULTIMO_ANIO", "FONDOS_INICIALES", "PAYBACK_SIMPLE_ANIOS"):
            if res.get(c) is not None:
                det.append(f"{b}:{c}={res[c]}")
    return _ok(not det, "; ".join(det[:6]))


# =============================================================================================
# J. FALTANTES (test 50)
# =============================================================================================
def t_fa01():
    """FA01 falta CAPEX / OPEX / precio → NO PUBLICABLE (None + motivo), nunca 0"""
    det = []
    casos = {"CAPEX": lambda P: P["etapas"][0].update(capex_usd=None),
             "OPEX": lambda P: P["etapas"][0]["opex_rubros"][0].update(costo_pleno_usd_anio=None),
             "PRECIO": lambda P: P.update(precios={})}
    for nom, f in casos.items():
        P = caso_e2e()
        f(P)
        res = mf.resultados(mf.simular(P))
        if res["VAN"] is not None or res["PUBLICABLE_VAN"] or nom.split()[0] not in res["FALTANTES"].replace("PRECIOS", "PRECIO"):
            det.append(f"{nom}: VAN {res['VAN']} / {res['PUBLICABLE_VAN']}")
        if nom == "CAPEX" and (res.get("FONDOS_INICIALES") is not None or res.get("EBITDA_ULTIMO_ANIO") is None):
            det.append("CAPEX: fondos publicados o EBITDA bloqueado sin motivo")
        if nom in ("OPEX", "PRECIO") and res.get("EBITDA_ULTIMO_ANIO") is not None:
            det.append(f"{nom}: EBITDA publicado")
        if not str(res["PUBLICABLE_VAN_MOTIVO"]).startswith(mf.NO_DISP_ESC):
            det.append(f"{nom}: motivo {res['PUBLICABLE_VAN_MOTIVO'][:40]}")
    return _ok(not det, "; ".join(det))


def t_fa02():
    """FA02 CAPEX y OPEX del proyecto: montos E4 parciales jamás entran como total al financiero"""
    det = []
    for b in BASES:
        cc, co = mf.configs(f"{b}-10000")
        cap = mf.capex_desde_modulo(cc)
        op = mf.opex_desde_modulo(co)
        if cap[0] is not None or op[0] is not None:
            det.append(b)
        if "NO usado" not in (cap[2] + op[2]) and b != "C0":
            det.append(f"{b}: motivo sin aclarar el monto parcial")
    return _ok(not det, "; ".join(det))


# =============================================================================================
# K. EVIDENCIA VS ESCENARIO (tests 28, 29, 52)
# =============================================================================================
def _hash(rel):
    with open(os.path.join(RAIZ, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def t_ev01():
    """EV01 (test 52) ida y vuelta: stress/override en escenario → la base de evidencia queda idéntica (memoria y archivos)"""
    archivos = ("21_modelo_financiero/base_precios_venta.csv", "21_modelo_financiero/inputs_financieros.csv",
                "22_riesgos/inputs_riesgo_optimizacion.csv", "22_riesgos/distribuciones_riesgo.csv")
    h0 = {a: _hash(a) for a in archivos}
    P0, _ = silencio(mf.construir_entrada, "EV01", "C1", (10000,), "EVIDENCIA")
    j0 = json.dumps(P0, sort_keys=True, default=str)
    det = []
    if not _lanza(mr.aplicar_shocks, P0, {"demanda": -0.3}, None, "EVIDENCIA"):
        det.append("shock aceptado en EVIDENCIA")
    if not _lanza(mf.construir_entrada, "EV01", "C1", (10000,), "EVIDENCIA", None, {"valores": {"tasa_descuento": 0.1}}):
        det.append("inputs de usuario aceptados en EVIDENCIA")
    P1, _ = mr.aplicar_shocks(P0, {"demanda": -0.3, "capex": 0.25}, None, "ESCENARIO")
    usr = {"precios": {"pollo_entero|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": 3.0}},
           "override_precios": {"pechuga|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": 4.0}},
           "valores": {"tasa_descuento": 0.12}}
    Pe, T = silencio(mf.construir_entrada, "EV01-ESC", "C1", (10000,), "ESCENARIO", None, usr)
    silencio(mf.simular, Pe)
    P2, _ = silencio(mf.construir_entrada, "EV01", "C1", (10000,), "EVIDENCIA")
    if json.dumps(P0, sort_keys=True, default=str) != j0 or json.dumps(P2, sort_keys=True, default=str) != j0:
        det.append("la base de evidencia cambió")
    if any(_hash(a) != h for a, h in h0.items()):
        det.append("un archivo de evidencia cambió")
    if not Pe["overrides_simulacion"] or mf.resultados(mf.simular(Pe))["ETIQUETA"] != mf.ETIQUETA_SIM:
        det.append("escenario sin rótulo de simulación")
    return _ok(not det, "; ".join(det))


def t_ev02():
    """EV02 (test 29) UMBRAL_EVIDENCIA_PUBLICACION configurable; default E1–E3 documentado; E4/E5 fuera del default"""
    filas = mf.leer_inputs()
    det = []
    if mf.umbral_evidencia(filas) != ("E1", "E2", "E3"):
        det.append(f"default {mf.umbral_evidencia(filas)}")
    mod = copy.deepcopy(filas)
    for f in mod:
        if f["VARIABLE"] == "umbral_evidencia_publicacion":
            f["VALOR"] = "E1|E2|E3|E4"
    if mf.umbral_evidencia(mod) != ("E1", "E2", "E3", "E4"):
        det.append("no configurable")
    for f in mod:
        if f["VARIABLE"] == "umbral_evidencia_publicacion":
            f["VALOR"] = "E9"
    if not _lanza(mf.umbral_evidencia, mod):
        det.append("valor inválido aceptado")
    v = mf.resolver("x", "EVIDENCIA", (1.0, "E4", "FTE"), None, None)
    if v[1] != "PENDIENTE":
        det.append("E4 aceptado como evidencia con el default")
    return _ok(not det, "; ".join(det) or "default E1|E2|E3 (SUP-190); DEC-084 abierta")


def t_ev03():
    """EV03 precios E4 [PVDP] de base_precios_venta.csv nunca se usan como precio (solo REFERENCIA_E4_NO_USABLE)"""
    precios, refs = mf.leer_precios()
    filas = leer_csv("21_modelo_financiero/base_precios_venta.csv")
    e4 = [r for r in filas if r["NIVEL_EVIDENCIA"] in ("E4", "E5") and r["ESTADO"] == "CON_PRECIO"]
    return _ok(not precios and not e4 and len(refs) >= 1, f"{len(precios)} precios usables; {len(refs)} referencias E4")


# =============================================================================================
# L. RIESGO, SENSIBILIDADES, STRESS, QUIEBRE, MONTE CARLO
# =============================================================================================
def _difs(a, b, path=""):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            out += _difs(a.get(k), b.get(k), f"{path}.{k}")
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            out += _difs(x, y, f"{path}[{i}]")
    elif a != b:
        out.append(path)
    return out


def t_ri01():
    """RI01 one-way cambia solo su driver; two-way solo dos; la base queda intacta"""
    P = caso_e2e()
    det = []
    d1 = _difs(P, mr.aplicar_shocks(P, {"precio_venta": 0.1}, {"precio_venta": 10.0}, "ESCENARIO")[0])
    if not d1 or any(".precios" not in x for x in d1):
        det.append(f"one-way toca {d1[:3]}")
    P2, info = mr.aplicar_shocks(P, {"precio_venta": 0.1, "capex": 0.2}, {"precio_venta": 10.0}, "ESCENARIO")
    d2 = _difs(P, P2)
    if set(info["cambios"]) != {"precio_venta", "capex"} or any(not (".precios" in x or "capex" in x or ".stress" in x) for x in d2):
        det.append(f"two-way toca {d2[:4]}")
    if _difs(P, caso_e2e()):
        det.append("base modificada")
    return _ok(not det, "; ".join(det))


def t_ri02():
    """RI02 stress multivariable = escenario determinista (sin probabilidad) y fuera del universo evidencia"""
    st = mr.leer_stress()
    det = [s["ID_STRESS"] for s in st if any("PROBAB" in str(v).upper() for v in s.values() if isinstance(v, str))]
    filas = leer_csv("22_riesgos/resultados_stress.csv")
    if any(r.get("UNIVERSO") == "EVIDENCIA" and r.get("ESTADO") not in (mr.NO_CALC,) for r in filas):
        det.append("stress calculado sobre evidencia")
    return _ok(not det, f"{len(st)} stress declarados; " + "; ".join(det))


def t_ri03():
    """RI03 puntos de quiebre: los del proyecto no contienen casos artificiales; los artificiales tienen ÁMBITO ARTIFICIAL_TEST"""
    pq = leer_csv("22_riesgos/puntos_quiebre.csv")
    art = leer_csv("22_riesgos/casos_prueba/puntos_quiebre.csv")
    det = []
    if any(r.get("AMBITO") == "ARTIFICIAL_TEST" or str(r.get("ALTERNATIVA", "")).startswith("ART-") for r in pq):
        det.append("caso artificial en el proyecto")
    if any(r.get("AMBITO") != "ARTIFICIAL_TEST" for r in art):
        det.append("quiebre artificial sin ámbito")
    return _ok(not det, f"proyecto {len(pq)} filas ({{{', '.join(sorted({r.get('ESTADO', '') for r in pq}))}}}); artificial {len(art)}")


def t_ri04():
    """RI04 Monte Carlo del proyecto NO_DISPONIBLE: ninguna distribución RESPALDADA ni correlación inventada"""
    d = leer_csv("22_riesgos/distribuciones_riesgo.csv")
    c = leer_csv("22_riesgos/correlaciones_riesgo.csv")
    mc = leer_csv("22_riesgos/monte_carlo_resultados.csv")
    det = []
    if any(r["ESTADO"] == "RESPALDADA" for r in d):
        det.append("distribución respaldada sin DPV-180 validado")
    if any(r.get("ESTADO") not in ("PENDIENTE",) for r in c):
        det.append("correlación no pendiente")
    if not mc or any(r["ESTADO"] not in (mr.MC_ND, mr.NO_CALC, mr.MC_CORR_PEND) for r in mc):
        det.append(f"MC proyecto {[r['ESTADO'] for r in mc]}")
    return _ok(not det, "; ".join(det))


def t_ri05():
    """RI05 registro de riesgos: frecuencia sectorial separada de la probabilidad del proyecto (PENDIENTE sin método)"""
    reg = leer_csv("22_riesgos/registro_riesgos.csv")
    det = [r["ID_RIESGO"] for r in reg if r["PROBABILIDAD"] not in ("PENDIENTE",) and not r.get("METODO_PROBABILIDAD")]
    return _ok(reg and not det and "FRECUENCIA_SECTORIAL_REFERENCIA" in reg[0],
               f"{len(reg)} riesgos; probabilidad sin método: {det}")


# =============================================================================================
# M. OPTIMIZADOR (tests 36, 37, 39, 40, 41, 53)
# =============================================================================================
def _alt_art(aid, construir, fis=None):
    return {"id": aid, "tipo": "PLANTA", "universo": "ARTIFICIAL_TEST", "configuracion": aid, "variante": "ARTIFICIAL",
            "escalas": (1,), "trayectoria": "ESCALA_UNICA", "construir": construir, "base_valores": {"precio_venta": 10.0},
            "fisico": fis or [mopt._gate("TERRENO", 1.0, "m²", 2.0, "ARTIFICIAL")], "cobertura": (0.0, "ARTIFICIAL_TEST")}


def caso_opt(capex, opex_fijo, H=5):
    return mf.caso_prueba(H=H, capex=capex, opex_fijo=opex_fijo, convencion="PERIODO_REPORTE", nombre=f"OPT-{capex}")


ESPERADO_OPT = {   # VAN manual: −CAPEX + EBITDA × factor de anualidad (5 años, 10 %); FONDOS = CAPEX (CT 0)
    "ALT-A": (100.0, 40.0), "ALT-B": (50.0, 18.0), "ALT-D": (120.0, 30.0)}


def inp_opt(**extra):
    inp = dict(mr.leer_inputs()[0])
    inp.update({"sensibilidad.variables": [], "sens2d.pares": [], "quiebre.variables": [], "tornado.metricas": ["VAN"],
                "robustez.variables": ["precio_venta", "capex"], "optimizador.objetivos": ["MAX_VAN", "MIN_FONDOS_INICIALES"],
                "montecarlo.n": 10})
    inp.update(extra)
    return inp


def correr_opt(ids=("ALT-A", "ALT-B", "ALT-D"), H=None, **extra):
    alts = []
    for aid in ids:
        c, e = ESPERADO_OPT[aid]
        alts.append(_alt_art(aid, (lambda c=c, e=e: (caso_opt(c, 100.0 - e, H or 5), None))))
    alts.append(mr.alternativa_status_quo("ARTIFICIAL_TEST"))
    return silencio(mopt.correr_universo, alts, inp_opt(**extra), "ARTIFICIAL_TEST")


def t_op01():
    """OP01 (test 53) mejor VAN, menor capital, dominada y Pareto = cálculo manual"""
    U = correr_opt()
    dec = {d["OBJETIVO"]: d for d in U["decisiones"]}
    van = {k: -c + e * AF5 for k, (c, e) in ESPERADO_OPT.items()}
    f = {x["id"]: x for x in U["fichas"]}
    det = []
    for k, v in van.items():
        if abs(f[k]["ev"]["met"]["VAN"] - v) > 1e-6:
            det.append(f"VAN {k}")
    if dec["MAX_VAN"]["MEJOR"] != max(van, key=van.get):
        det.append(f"MAX_VAN → {dec['MAX_VAN']['MEJOR']}")
    if dec["MIN_FONDOS_INICIALES"]["MEJOR"] != "ALT-B":
        det.append(f"MIN_FONDOS → {dec['MIN_FONDOS_INICIALES']['MEJOR']}")
    if set(f["ALT-D"]["DOMINADA_POR"]) != {"ALT-A", "ALT-B"} or f["ALT-A"]["DOMINADA_POR"] or f["ALT-B"]["DOMINADA_POR"]:
        det.append(f"dominancia {[(k, f[k]['DOMINADA_POR']) for k in ESPERADO_OPT]}")
    fr = {r["ALTERNATIVA"]: r["EN_FRONTERA"] for r in U["pareto"] if r["PAR"] == "VAN×FONDOS_INICIALES"}
    if fr.get("ALT-A") is not True or fr.get("ALT-B") is not True or fr.get("ALT-D") is not False:
        det.append(f"Pareto {fr}")
    if mr.STATUS_QUO in fr:
        det.append("status quo en Pareto")
    if dec["MAX_VAN"]["DECISION_ESCENARIO"] != "ALT-A":
        det.append("decisión")
    return _ok(not det, "; ".join(det) or ", ".join(f"{k} VAN {v:.4f}" for k, v in van.items()))


def t_op02():
    """OP02 (tests 36, 53) NO_INVERTIR_AUN gana solo por regla (capital HARD, VAN < 0); sin métricas ni ranking"""
    det = []
    U = correr_opt(**{"restriccion.CAPITAL_DISPONIBLE.valor": 40.0, "restriccion.CAPITAL_DISPONIBLE.tipo": "HARD"})
    d = next(x for x in U["decisiones"] if x["OBJETIVO"] == "MAX_VAN")
    if d["ESTADO"] != mopt.NINGUNA or d["DECISION_ESCENARIO"] != mr.STATUS_QUO or "SQ-2" not in d["REGLA_STATUS_QUO"]:
        det.append(f"capital: {d['ESTADO']} / {d['DECISION_ESCENARIO']} / {d['REGLA_STATUS_QUO'][:30]}")
    U = correr_opt(ids=("ALT-D",))
    d = next(x for x in U["decisiones"] if x["OBJETIVO"] == "MAX_VAN")
    if d["DECISION_ESCENARIO"] != mr.STATUS_QUO or "SQ-3" not in d["REGLA_STATUS_QUO"]:
        det.append(f"VAN < 0: {d['DECISION_ESCENARIO']}")
    sq = next(f for f in U["fichas"] if f["alt"]["tipo"] == mr.STATUS_QUO)
    if any(v is not None for k, v in sq["ev"]["met"].items() if k not in ("TIR_ESTADO", "PAYBACK_ESTADO")):
        det.append("status quo con métricas")
    if any(U["ranking"][o][sq["id"]]["RANK"] is not None for o in U["ranking"]):
        det.append("status quo rankeado")
    filas = leer_csv("22_riesgos/resultados_optimizador.csv")
    if any(r["ALTERNATIVA"] == mr.STATUS_QUO and (r["VAN"] or r["TIR"] or r["RANK"]) for r in filas):
        det.append("status quo con VAN/TIR/RANK en la salida del proyecto")
    return _ok(not det, "; ".join(det))


def t_op03():
    """OP03 (test 39) una alternativa no comparable (otro horizonte) o incompleta (falta OPEX) no se rankea ni domina"""
    alts = [_alt_art(k, (lambda c=c, e=e: (caso_opt(c, 100.0 - e), None))) for k, (c, e) in ESPERADO_OPT.items()]
    alts.append(_alt_art("ALT-H10", lambda: (caso_opt(10.0, 10.0, H=10), None)))          # mejor VAN pero otro horizonte
    def incompleta():
        P = caso_opt(10.0, 10.0)
        P["etapas"][0]["opex_rubros"][0]["costo_pleno_usd_anio"] = None                   # "ganaría" por costos faltantes
        return P, None
    alts.append(_alt_art("ALT-SIN-OPEX", incompleta))
    alts.append(mr.alternativa_status_quo("ARTIFICIAL_TEST"))
    U = silencio(mopt.correr_universo, alts, inp_opt(), "ARTIFICIAL_TEST")
    f = {x["id"]: x for x in U["fichas"]}
    rk = U["ranking"]["MAX_VAN"]
    det = []
    for k in ("ALT-H10", "ALT-SIN-OPEX"):
        if f[k]["COMPARABILIDAD"] != "FALSE" or rk[k]["RANK"] is not None or f[k]["DOM_ESTADO"].startswith("EVALUADA"):
            det.append(f"{k}: {f[k]['COMPARABILIDAD']} rank {rk[k]['RANK']}")
    if next(d for d in U["decisiones"] if d["OBJETIVO"] == "MAX_VAN")["MEJOR"] != "ALT-A":
        det.append("ganador incorrecto")
    return _ok(not det, "; ".join(det))


def t_op04():
    """OP04 (tests 40, 41) Pareto con < 2 comparables = PARETO_NO_INFORMATIVO; robustez exige ≥ 3 escenarios (la base no cuenta)"""
    U = correr_opt(ids=("ALT-A",))
    det = []
    par = [r for r in U["pareto"] if r["PAR"] == "VAN×FONDOS_INICIALES" and r["ALTERNATIVA"] == "ALT-A"]
    if not par or any(r["EN_FRONTERA"] != mopt.PARETO_NI for r in par):
        det.append("Pareto informativo con 1 punto")
    U2 = correr_opt(ids=("ALT-A", "ALT-B"), **{"robustez.variables": ["precio_venta"]})   # 2 escenarios < 3
    if any(f["ROB"]["ESTADO"] != "PENDIENTE" for f in U2["fichas"] if f["alt"]["tipo"] != mr.STATUS_QUO):
        det.append("robustez calculada con 2 escenarios")
    U3 = correr_opt(ids=("ALT-A", "ALT-B"))                                                # 4 escenarios
    if any(f["ROB"]["ESTADO"] != "CALCULADA" for f in U3["fichas"] if f["alt"]["tipo"] != mr.STATUS_QUO):
        det.append("robustez no calculada con 4 escenarios")
    return _ok(not det, "; ".join(det))


def t_op05():
    """OP05 (test 37) C0 asset-light: requerimientos propios DESCONOCIDO (no 0); 0 solo con NO_REQUERIDO_POR_ARQUITECTURA"""
    g = _gates("C0")
    det = []
    for k in ("TERRENO", "AGUA", "POTENCIA"):
        if g[k]["ESTADO_REQUERIMIENTO"] != "DESCONOCIDO" or g[k]["REQUERIDO"] is not None:
            det.append(f"{k}: {g[k]['ESTADO_REQUERIMIENTO']} {g[k]['REQUERIDO']}")
    for gg in list(g.values()) + list(_gates("C1").values()) + list(_gates("C3").values()):
        if gg["REQUERIDO"] == 0 and gg["ESTADO_REQUERIMIENTO"] != "NO_REQUERIDO_POR_ARQUITECTURA":
            det.append(f"{gg['GATE']}: 0 sin ser estructural")
    if mopt._gate("X", None, "u", 1.0, "")["ESTADO"] != mopt.PEND:
        det.append("requerimiento desconocido no queda pendiente")
    return _ok(not det, "; ".join(det))


def t_op06():
    """OP06 (test 38) factibilidades separadas (física, económica, financiera, comercial, evidencia): no hay un FACTIBLE único"""
    h = list(leer_csv("22_riesgos/resultados_optimizador.csv")[0].keys())
    req = {"FACTIBILIDAD_FISICA", "FACTIBILIDAD_ECONOMICA", "FACTIBILIDAD_FINANCIERA", "RESPALDO_COMERCIAL", "COBERTURA_EVIDENCIA"}
    return _ok(req <= set(h) and "FACTIBLE" not in h, f"faltan {sorted(req - set(h))}")


def t_op07():
    """OP07 (test 42) prioridades: empates como RANK_COMPARTIDO; columna futura POTENCIAL_DE_CAMBIAR_DECISION sin completar en evidencia"""
    det, prio = [], []
    for rel in ("22_riesgos/prioridad_validacion.csv", "22_riesgos/que_hacer_ahora.csv"):
        filas = leer_csv(rel)
        if "POTENCIAL_DE_CAMBIAR_DECISION" not in filas[0]:
            det.append(f"{rel}: sin columna")
            continue
        for r in filas:
            if r.get("UNIVERSO") == "EVIDENCIA" and r["POTENCIAL_DE_CAMBIAR_DECISION"] != mopt.POTENCIAL_NO_CALC:
                det.append(f"{rel}: {r['POTENCIAL_DE_CAMBIAR_DECISION']}")
        if rel.endswith("prioridad_validacion.csv"):
            grupos = {}
            for r in filas:
                if r.get("UNIVERSO") == "EVIDENCIA":
                    grupos.setdefault((r["INDICADORES_BLOQUEADOS"], r["N_ALTERNATIVAS_BLOQUEADAS"]), []).append(r)
            for k, g in grupos.items():
                if len({r["RANK_COMPARTIDO"] for r in g}) != 1 or any(int(r["N_EMPATADOS"]) != len(g) for r in g):
                    det.append(f"empate {k} con rangos distintos o N_EMPATADOS ≠ {len(g)}")
            prio = filas
        else:
            acc = {r["QUE_HACER_AHORA"] for r in filas if r.get("UNIVERSO") == "EVIDENCIA"}
            for rk in {r["RANK_COMPARTIDO"] for r in filas if r.get("UNIVERSO") == "EVIDENCIA"}:
                falt = {r["ACCION"] for r in prio if r.get("UNIVERSO") == "EVIDENCIA" and r["RANK_COMPARTIDO"] == rk} - acc
                if falt:
                    det.append(f"que_hacer_ahora corta el empate de rango {rk}: faltan {sorted(falt)[:2]}")
    return _ok(not det, "; ".join(det[:4]))


# =============================================================================================
# N. MUTACIONES DE INTEGRACIÓN (test 54): errores entre módulos que los detectores deben atrapar
# =============================================================================================
def detector_masa(P):
    """Σ kg vendibles por ave ≤ masa del ave (+ agua) y rutas exclusivas (esqueleto vs CMS)."""
    if P["productos"] is None:
        return True
    kg = {k: (v["kg_ave"] or 0.0) for k, v in P["productos"].items()}
    lim = P["meta_productos"].get("peso_vivo", math.inf) + P["meta_productos"].get("agua_incorporada", 0)
    return sum(kg.values()) <= lim + 1e-9 and not (kg.get("cms", 0) > 0 and kg.get("carcasa_esqueleto", 0) > 0) \
        and not _lanza(mf.validar_entrada, P)


def detector_electricidad(filas_opex):
    """Un solo concepto costeado de energía eléctrica activa por universo; lo demás INCLUIDO."""
    cuenta = {}
    for f in filas_opex:
        if f["COSTEA"] and f.get("UNIDAD") == "kWh":
            cuenta[f.get("UNIVERSO_UTILITIES")] = cuenta.get(f.get("UNIVERSO_UTILITIES"), 0) + 1
    return all(v <= 1 for v in cuenta.values())


def detector_identidades(R):
    S = R["series"]
    ok = abs(sum(S["delta_ct"]) - S["ct"][R["N"]]) < 1e-9
    for k in range(R["N"] + 1):
        ok &= abs(S["fcff_pre"][k] - (S["ebitda"][k] - S["capex_total"][k] - S["delta_ct"][k] + S["flujo_iva"][k]
                                      + S["valor_terminal"][k])) < 1e-9
    return ok


def detector_fcff_sin_deuda(fn_simular):
    P = caso_e2e()
    Q = copy.deepcopy(P)
    Q["financiamiento"]["deudas"] = [{"id": "D", "monto": 80.0, "tasa": 0.1, "tipo_tasa": "EFECTIVA_ANUAL", "base_tasa": "REAL",
                                      "plazo_meses": 24, "gracia_meses": 0, "metodo": "FRANCES", "frecuencia_meses": 1,
                                      "mes_desembolso": 0}]
    a, b = fn_simular(P)["series"]["fcff_pre"], fn_simular(Q)["series"]["fcff_pre"]
    return all(abs(x - y) < 1e-12 for x, y in zip(a, b))


def detector_umbral(P, precios_usados):
    """Todo precio usado en EVIDENCIA tiene nivel dentro del umbral declarado de la corrida."""
    return all(v.get("nivel") in P["umbral_evidencia"] for v in precios_usados.values())


def _precios_con_e4_aceptado():
    """Copia temporal de base_precios_venta.csv donde la referencia E4 (FTE-004) figura CON_PRECIO con TC declarado."""
    import tempfile
    filas = leer_csv("21_modelo_financiero/base_precios_venta.csv")
    for r in filas:
        if r["NIVEL_EVIDENCIA"] == "E4" and r["MONEDA"] == "ARS":
            r.update(ESTADO="CON_PRECIO", TC_USADO="1000", FECHA_TC="2026-01-31", TIPO_TC="A3500")
    fd, ruta = tempfile.mkstemp(suffix=".csv")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, list(filas[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    return ruta


def detector_faltante_cero(P, T):
    """Lo que la traza marca PENDIENTE debe ser None en la entrada (un faltante no es 0)."""
    pend = {r["VARIABLE"] for r in T.filas if r["ORIGEN"] == "PENDIENTE"} if hasattr(T, "filas") else set()
    for e in P["etapas"]:
        if e["capex_usd"] == 0 and f"{e['id']}.capex_usd" in pend | {f"{e['id']}.capex_usd"}:
            return False
        if e["opex_rubros"] is not None and any(r["costo_pleno_usd_anio"] == 0 for r in e["opex_rubros"]):
            return False
    return True


def detector_ventas_demanda(R):
    S = R["series"]
    for k in range(1, R["N"] + 1):
        dem = sum(l["_q"] for l in R["P"]["demanda"] if not l.get("toma_todo")) if R["P"]["demanda"] else 0
        if sum(pl["kg"][k] for pl in R["por_linea"].values()) > min(dem, S["kg_producidos"][k] + 1e9) + 1e-9:
            return False
    return True


def detector_arquitectura(cc, co):
    return dims(cc) == dims(co)


def detector_c0(gates):
    return all(not (g["REQUERIDO"] == 0 and g["ESTADO_REQUERIMIENTO"] != "NO_REQUERIDO_POR_ARQUITECTURA") and
               not (g["GATE"] in ("TERRENO", "AGUA", "POTENCIA") and g["REQUERIDO"] is not None and
                    g["ESTADO_REQUERIMIENTO"] != "DIMENSIONADO") for g in gates)


def detector_ranking(U):
    """Toda alternativa rankeada es completa (VAN publicable) y comparte horizonte y base con las demás."""
    rk = U["ranking"]["MAX_VAN"]
    f = {x["id"]: x for x in U["fichas"]}
    rank = [k for k, v in rk.items() if v["RANK"] is not None]
    hor = {mr.Evaluador().base(f[k]["alt"])[0]["horizonte_anios"] for k in rank}
    return all(f[k]["ev"]["met"].get("VAN") is not None for k in rank) and len(hor) <= 1


def detector_status_quo(U):
    sq = [x for x in U["fichas"] if x["alt"]["tipo"] == mr.STATUS_QUO]
    return all(all(v is None for k, v in x["ev"]["met"].items() if k not in ("TIR_ESTADO", "PAYBACK_ESTADO")) and
               all(U["ranking"][o][x["id"]]["RANK"] is None for o in U["ranking"]) for x in sq)


class MutMF:
    """Activa una mutación sembrada del motor financiero / de riesgo solo dentro del bloque."""
    def __init__(self, mod, m):
        self.mod, self.m = mod, m

    def __enter__(self):
        self.prev = self.mod._MUT
        self.mod._MUT = {self.m}

    def __exit__(self, *a):
        self.mod._MUT = self.prev


def _p_balance():
    pr, meta = mf.productos_balance("B")
    P = caso_e2e()
    P["productos"], P["meta_productos"] = copy.deepcopy(pr), meta
    P["demanda"][0]["producto"] = "pechuga"
    P["precios"] = {"pechuga|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": 10.0}}
    return P


def m01():
    """duplicar una masa vendida (esqueleto vendido y además su CMS)"""
    P = _p_balance()
    P["productos"]["cms"]["kg_ave"] = P["productos"]["carcasa_esqueleto"]["kg_ave"]
    return detector_masa(P)


def m02():
    """duplicar electricidad (energía de frío costeada aparte además de UT-ELE-KWH)"""
    _, co = mf.configs("C1-10000")
    fo = copy.deepcopy(mf._correr_opex(co)[0])
    for f in fo:
        if f.get("INCLUIDO_EN") == "UT-ELE-KWH" and "frío" in f["CONCEPTO"].lower():
            f["COSTEA"] = True
    return detector_electricidad(fo)


def m03():
    """usar CT total en lugar de ΔCT en el flujo"""
    with MutMF(mf, "M04"):
        R = mf.simular(caso_e2e())
    return detector_identidades(R)


def m04():
    """meter deuda en el FCFF"""
    with MutMF(mf, "M06"):
        return detector_fcff_sin_deuda(mf.simular)


def m05():
    """usar un precio E4 [PVDP] como validado en modo evidencia (umbral ampliado en silencio a E4)"""
    P, _ = silencio(mf.construir_entrada, "M05", "C1", (10000,), "EVIDENCIA")
    ruta = _precios_con_e4_aceptado()
    try:
        precios, _ = mf.leer_precios(ruta, ("E1", "E2", "E3", "E4"))
    finally:
        os.remove(ruta)
    with MutMF(mf, "M09"):
        r = mf.resolver("precio", "EVIDENCIA", (2.85, "E4", "FTE-004"), None, None, P["umbral_evidencia"])
    return detector_umbral(P, precios) and (r[1] != "EVIDENCIA_REAL" or r[2] in P["umbral_evidencia"])


def m06():
    """convertir un faltante en cero (CAPEX y OPEX PENDIENTES → 0)"""
    P, T = silencio(mf.construir_entrada, "M06", "C1", (10000,), "EVIDENCIA")
    for e in P["etapas"]:
        e["capex_usd"] = 0.0 if e["capex_usd"] is None else e["capex_usd"]
        e["opex_rubros"] = e["opex_rubros"] or [{"rubro": "x", "naturaleza": "fijo", "costo_pleno_usd_anio": 0.0}]
    return detector_faltante_cero(P, T)


def m07():
    """permitir ventas > demanda (la producción se vende entera)"""
    P = caso_e2e()
    P["demanda"][0]["kg_mes"] = 0.5
    with MutMF(mf, "M02"):
        R = mf.simular(P)
    return detector_ventas_demanda(R)


def m08():
    """cambiar la arquitectura entre CAPEX y OPEX (C1 en CAPEX, C3 en OPEX)"""
    cc, _ = mf.configs("C1-10000")
    _, co = mf.configs("C3-10000")
    return detector_arquitectura(cc, co)


def m09():
    """tratar C0 desconocido como cero (módulos propios de C0 con requerimiento 0)"""
    gates = copy.deepcopy(list(_gates("C0").values()))
    for g in gates:
        if g["GATE"] in ("TERRENO", "AGUA", "POTENCIA"):
            g.update(REQUERIDO=0.0, ESTADO_REQUERIMIENTO="DIMENSIONADO")
    return detector_c0(gates)


def m10():
    """rankear una alternativa no comparable (comparabilidad forzada a TRUE)"""
    alts = [_alt_art(k, (lambda c=c, e=e: (caso_opt(c, 100.0 - e), None))) for k, (c, e) in ESPERADO_OPT.items()]
    alts.append(_alt_art("ALT-H10", lambda: (caso_opt(10.0, 10.0, H=10), None)))
    alts.append(mr.alternativa_status_quo("ARTIFICIAL_TEST"))
    with MutMF(mr, "R12"):
        U = silencio(mopt.correr_universo, alts, inp_opt(), "ARTIFICIAL_TEST")
    return detector_ranking(U)


def m11():
    """permitir NO_INVERTIR_AUN con TIR/VAN ficticios (tratado como proyecto con ceros)"""
    with MutMF(mr, "R24"):
        U = correr_opt()
    return detector_status_quo(U)


MUTACIONES = [m01, m02, m03, m04, m05, m06, m07, m08, m09, m10, m11]  # + m12–m15 al final del módulo


def t_mu00():
    """MU00 sin mutación, todos los detectores de integración aceptan los motores tal como están"""
    det = []
    if not detector_masa(_p_balance()):
        det.append("masa")
    _, co = mf.configs("C1-10000")
    if not detector_electricidad(mf._correr_opex(co)[0]):
        det.append("electricidad")
    if not detector_identidades(mf.simular(caso_e2e())):
        det.append("identidades")
    if not detector_fcff_sin_deuda(mf.simular):
        det.append("FCFF")
    P, T = silencio(mf.construir_entrada, "MU00", "C1", (10000,), "EVIDENCIA")
    if not detector_umbral(P, mf.leer_precios(None, P["umbral_evidencia"])[0]) or not detector_faltante_cero(P, T):
        det.append("umbral / faltantes")
    if not detector_ventas_demanda(mf.simular(caso_e2e())):
        det.append("ventas")
    if not detector_arquitectura(*mf.configs("C3-10000")):
        det.append("arquitectura")
    if not detector_c0(list(_gates("C0").values())):
        det.append("C0")
    U = correr_opt()
    if not detector_ranking(U) or not detector_status_quo(U):
        det.append("ranking / status quo")
    return _ok(not det, "; ".join(det))


# =============================================================================================
# O. MÉTRICA TRANSVERSAL DE COBERTURA (test 43): cuatro coberturas que no se condensan
# =============================================================================================
CAMPOS_COBERTURA = ["CONFIGURACION", "ESCALA_AVES_DIA", "MODULO", "COBERTURA_ESTRUCTURAL_PCT", "COBERTURA_FISICA_PCT",
                    "COBERTURA_ECONOMICA_PCT", "COBERTURA_EVIDENCIA_PCT", "BASE_ESTRUCTURAL", "BASE_FISICA", "BASE_ECONOMICA",
                    "BASE_EVIDENCIA", "NOTA"]


def filas_cobertura():
    """Por configuración base y escala de referencia: CAPEX, OPEX y MOTOR (financiero). Derivada de los motores; nada se
    estima aquí. La cobertura de EVIDENCIA del motor es la de 22 (bloques completos en modo evidencia ÷ 17)."""
    out = []
    for b in BASES:
        for esc in (2500, 10000, 20000):
            cc, co = mf.configs(f"{b}-{esc}")
            _, rc, _ = mf._correr_capex(cc)
            T = rc["TOTAL"]
            n = T["CONCEPTOS_COSTEABLES"]
            ev_c = T["N_CONCEPTOS_E1_E2"] + T["N_CONCEPTOS_E3"]
            out.append({"CONFIGURACION": b, "ESCALA_AVES_DIA": esc, "MODULO": "CAPEX",
                        "COBERTURA_ESTRUCTURAL_PCT": 100.0, "COBERTURA_FISICA_PCT": round(100 * (n - T["CONCEPTOS_SIN_CANTIDAD"]) / n, 6),
                        "COBERTURA_ECONOMICA_PCT": round(T["COBERTURA_CONCEPTOS_PCT"], 6),
                        "COBERTURA_EVIDENCIA_PCT": round(100 * ev_c / n, 6),
                        "BASE_ESTRUCTURAL": f"{n} conceptos costeables definidos en el BOQ",
                        "BASE_FISICA": f"conceptos con cantidad ({n - T['CONCEPTOS_SIN_CANTIDAD']}/{n})",
                        "BASE_ECONOMICA": f"conceptos con precio ({T['CONCEPTOS_CON_PRECIO']}/{n}; {T['CALIDAD_MONTO']})",
                        "BASE_EVIDENCIA": f"conceptos con precio E1–E3 ({ev_c}/{n})",
                        "NOTA": "por conceptos; la cobertura por valor es NO CALCULABLE"})
            To = mf._correr_opex(co)[1]["TOTAL"]
            no = To["CONCEPTOS_COSTEABLES"]
            ev_o = To["N_CONCEPTOS_E1_E2"] + To["N_CONCEPTOS_E3"]
            out.append({"CONFIGURACION": b, "ESCALA_AVES_DIA": esc, "MODULO": "OPEX",
                        "COBERTURA_ESTRUCTURAL_PCT": round(To["COBERTURA_ESTRUCTURAL_PCT"], 6),
                        "COBERTURA_FISICA_PCT": round(To["COBERTURA_FISICA_PCT"], 6),
                        "COBERTURA_ECONOMICA_PCT": round(To["COBERTURA_COSTEO_BLOQUES_PCT"], 6),
                        "COBERTURA_EVIDENCIA_PCT": round(100 * ev_o / no, 6),
                        "BASE_ESTRUCTURAL": "bloques operativos materiales definidos por módulo (SUP-185)",
                        "BASE_FISICA": "bloques con cantidades (ARQUITECTURA_OPERATIVAMENTE_COMPLETA)",
                        "BASE_ECONOMICA": f"bloques costeados (ARQUITECTURA_COSTEABLE = {To['ARQUITECTURA_COSTEABLE']})",
                        "BASE_EVIDENCIA": f"conceptos con precio E1–E3 ({ev_o}/{no})",
                        "NOTA": "por bloques (estructural, física, económica) y por conceptos (evidencia)"})
            alt = {"tipo": "PLANTA", "universo": "EVIDENCIA", "configuracion": b, "variante": "BASE", "escalas": (esc,)}
            cob, nota = silencio(mopt.cobertura_evidencia, alt)
            P, _ = silencio(mf.construir_entrada, "COB", b, (esc,), "EVIDENCIA")
            est = mf.estado_bloques(P)
            fis = ("TIEMPO", "RAMPUP", "PRODUCCION", "DEMANDA")
            eco = ("PRECIOS", "CANALES", "OPEX", "IMPUESTOS_INGRESOS", "CAPEX", "DEPRECIACION", "REPOSICION", "CT", "IVA",
                   "GANANCIAS", "FINANCIAMIENTO", "DESCUENTO", "VALOR_TERMINAL")
            cf, ce = mf.cobertura_bloques({k: est[k] for k in fis}), mf.cobertura_bloques({k: est[k] for k in eco})
            n_eco = sum(1 for k in eco if est[k] != "NO_APLICA")
            out.append({"CONFIGURACION": b, "ESCALA_AVES_DIA": esc, "MODULO": "MOTOR_FINANCIERO",
                        "COBERTURA_ESTRUCTURAL_PCT": 100.0,
                        "COBERTURA_FISICA_PCT": round(100 * (cf or 0.0), 6),
                        "COBERTURA_ECONOMICA_PCT": round(100 * (ce or 0.0), 6),
                        "COBERTURA_EVIDENCIA_PCT": round(100 * cob, 6),
                        "BASE_ESTRUCTURAL": f"{len(mf.BLOQUES)} bloques del motor definidos",
                        "BASE_FISICA": "bloques TIEMPO, RAMPUP, PRODUCCION, DEMANDA con contenido en modo evidencia",
                        "BASE_ECONOMICA": f"bloques económicos aplicables con contenido ({n_eco} de 13; NO_APLICA fuera del denominador)",
                        "BASE_EVIDENCIA": "COBERTURA_EVIDENCIA de 22: CON_EVIDENCIA ÷ bloques aplicables (VACIO y PENDIENTE no suman; TF-011)",
                        "NOTA": nota})
    return out


def escribir_cobertura():
    with open(ARCH_COBERTURA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, CAMPOS_COBERTURA, lineterminator="\n")
        w.writeheader()
        for r in filas_cobertura():
            w.writerow({k: (f"{v:.6f}".rstrip("0").rstrip(".") if isinstance(v, float) else v) for k, v in r.items()})


def t_cv01():
    """CV01 (test 43) cuatro coberturas separadas por módulo; ninguna arquitectura condensada en un solo número"""
    filas = leer_csv(os.path.relpath(ARCH_COBERTURA, RAIZ))
    req = {"COBERTURA_ESTRUCTURAL_PCT", "COBERTURA_FISICA_PCT", "COBERTURA_ECONOMICA_PCT", "COBERTURA_EVIDENCIA_PCT"}
    mods = {r["MODULO"] for r in filas}
    return _ok(req <= set(filas[0]) and mods == {"CAPEX", "OPEX", "MOTOR_FINANCIERO"} and len(filas) == 45,
               f"{len(filas)} filas; módulos {sorted(mods)}")


# =============================================================================================
# P. TABLAS FINALES DE GESTIÓN
# =============================================================================================
def t_tb01():
    """TB01 tablas finales: tensiones, completitud, trazabilidad y arquitecturas con los campos pedidos"""
    req = {
        "tensiones_finales.csv": ["ID", "MODULO_A", "MODULO_B", "DESCRIPCION", "TIPO", "IMPACTO", "ESTADO", "RESOLUCION_NECESARIA",
                                  "DPV", "DEC", "OBSERVACIONES"],
        "completitud_final_motor.csv": ["MODULO", "ESTRUCTURA", "DRIVERS", "VALIDACION_FISICA", "PRECIOS", "EVIDENCIA", "TESTS",
                                        "LISTO_APP", "LISTO_DECISION_REAL", "OBSERVACIONES"],
        "trazabilidad_end_to_end.csv": ["VARIABLE", "ORIGEN", "TRANSFORMACION", "DESTINO", "UNIDAD", "EVIDENCIA", "ESTADO", "TEST"],
        "arquitecturas_maestras.csv": ["CONFIGURACION", "FAENA", "GRANJAS", "POLLITO", "ALIMENTO", "FLOTA", "FRIO", "SUBPRODUCTOS",
                                       "RENDERING", "UPSTREAM", "CAPEX", "OPEX", "CT", "FINANZAS", "RIESGOS", "OPTIMIZADOR",
                                       "ESTADO", "OBSERVACIONES"],
    }
    det = []
    for f, cols in req.items():
        filas = leer_csv(f"00_gestion_proyecto/{f}")
        falt = [c for c in cols if c not in filas[0]]
        if falt or not filas:
            det.append(f"{f}: faltan {falt}")
    comp = leer_csv("00_gestion_proyecto/completitud_final_motor.csv")
    if any(r["LISTO_DECISION_REAL"] == "TRUE" for r in comp):
        det.append("algún módulo LISTO_DECISION_REAL = TRUE sin datos reales")
    ten = leer_csv("00_gestion_proyecto/tensiones_finales.csv")
    if any(r["ESTADO"] in ("RESUELTA",) and r["TIPO"] == "NEGOCIO" for r in ten):
        det.append("tensión de negocio resuelta en la auditoría")
    ids = [r["ID"] for r in ten]
    if len(ids) != len(set(ids)):
        det.append("IDs de tensiones duplicados")
    return _ok(not det, "; ".join(det))


# =============================================================================================
# Q. DEFENSAS DE LA AUDITORÍA FINAL (TF-004 overrides · TF-011 cobertura · TF-005 IIBB · TF-076 IVA de CAPEX)
# =============================================================================================
def _meta(cfg="C1", esc=10000, var="BASE", mod="TOTAL_ETAPA", uni="FAENA_PROPIA", org="ESCENARIO_USUARIO"):
    return {"CONFIGURACION": cfg, "ESCALA": esc, "VARIANTE": var, "MODULO": mod, "UNIVERSO": uni, "ORIGEN": org}


def _rub_u(rubro, mod, uni, cfg="C1", costo=100.0, nat="fijo", grupo="servicios"):
    return {"rubro": rubro, "grupo_proveedor": grupo, "naturaleza": nat, "costo_pleno_usd_anio": costo, "es_compra": True,
            "dias_pago": 30.0, "iva_credito": True, "meta": _meta(cfg, mod=mod, uni=uni)}


def _construir_esc(cfg, etapa, extra=None):
    usr = {"etapas": [etapa]}
    usr.update(extra or {})
    return silencio(mf.construir_entrada, "OV", cfg, (10000,), "ESCENARIO", None, usr)


def _rechaza_override(cfg, etapa, extra=None):
    try:
        _construir_esc(cfg, etapa, extra)
    except mf.ErrorFinanciero as e:
        return mf.OVERRIDE_INCOMPATIBLE in str(e), str(e)
    return False, "aceptado"


def t_ov01():
    """OV01 (TF-004) CAPEX de otra arquitectura rechazado: CAPEX de C3 en una corrida C1; módulo de incubación en C1; sin metadatos"""
    det = []
    for nom, cfg, et in (("CAPEX de C3 en C1", "C1", {"capex_usd": 1000.0, "capex_meta": _meta("C3", uni="INCUBACION")}),
                         ("módulo INCUBACION en C1", "C1", {"capex_usd": 1000.0, "capex_meta": _meta("C1", mod="INCUBACION")}),
                         ("activo de planta de faena en C0", "C0", {"capex_usd": 10.0, "capex_meta": _meta("C0", uni="FACON"),
                                                                    "activos": [{"clase": "PROCESO:linea", "capex_usd": 10.0}]}),
                         ("sin metadatos", "C1", {"capex_usd": 1000.0})):
        ok, txt = _rechaza_override(cfg, et)
        if not ok:
            det.append(f"{nom}: {txt[:80]}")
    P, _ = _construir_esc("C1", {"capex_usd": 1000.0, "capex_meta": _meta("C1")})
    if P["etapas"][0]["capex_usd"] != 1000.0 or P["override_total"]:
        det.append("override compatible no aceptado")
    return _ok(not det, "; ".join(det))


def t_ov02():
    """OV02 (TF-004) OPEX de otra arquitectura rechazado: planta propia en façon; alimento propio con alimento comprado; completitud exigida"""
    det = []
    for nom, cfg, rub in (("faena propia en C0 (façon)", "C0", [_rub_u("operarios", "FAENA_PROPIA", "FAENA_PROPIA", "C0")]),
                          ("universo de planta de faena en C0", "C0", [_rub_u("x", "ESTRUCTURA", "FAENA_PROPIA", "C0")]),
                          ("planta de alimento propia en C1", "C1", [_rub_u("maíz", "PLANTA_ALIMENTO_PROPIA", "PLANTA_ALIMENTO")]),
                          ("universo alimento propio en C1", "C1", [_rub_u("maíz", "ALIMENTO_COMPRADO", "ALIMENTO_PROPIO")])):
        ok, txt = _rechaza_override(cfg, {"opex_rubros": rub})
        if not ok:
            det.append(f"{nom}: {txt[:80]}")
    # compatible pero incompleto: queda PENDIENTE (no publica), nunca gana por costos faltantes
    P, _ = _construir_esc("C1", {"opex_rubros": [_rub_u("alimento", "ALIMENTO_COMPRADO", "ALIMENTO_COMPRADO", grupo="alimento")]})
    falt = mf.disponibilidad(P)["OPEX"]
    if not any("completitud TF-004" in x for x in falt):
        det.append("OPEX incompleto del usuario sin faltante de completitud")
    return _ok(not det, "; ".join(det))


def t_ov03():
    """OV03 (TF-004) override total solo con OVERRIDE_TOTAL_ARQUITECTURA = TRUE: corrida SIMULACION_HIPOTETICA_OVERRIDE_TOTAL con trazabilidad parcial"""
    det = []
    et = {"capex_usd": 1000.0, "capex_meta": _meta("C3"), "opex_rubros": [_rub_u("x", "PLANTA_ALIMENTO_PROPIA", "PLANTA_ALIMENTO", "C3")]}
    ok, _ = _rechaza_override("C1", et)
    if not ok:
        det.append("aceptado sin flag")
    ok, _ = _rechaza_override("C1", et, {"OVERRIDE_TOTAL_ARQUITECTURA": "SI"})
    if _lanza(_construir_esc, "C1", et, {"OVERRIDE_TOTAL_ARQUITECTURA": "SI"}) is False:
        det.append("flag ambiguo aceptado")
    P, T = _construir_esc("C1", et, {"OVERRIDE_TOTAL_ARQUITECTURA": True})
    res = mf.resultados(mf.simular(P))
    if not P["override_total"] or res["ETIQUETA"] != mf.ETIQUETA_OVERRIDE_TOTAL or not res["TRAZABILIDAD"].startswith("PARCIAL"):
        det.append(f"etiqueta {res['ETIQUETA']} / {res.get('TRAZABILIDAD')}")
    if not any("PERDIDA_DE_TRAZABILIDAD_PARCIAL" in str(r.get("OBSERVACIONES", "")) or "PERDIDA_DE_TRAZABILIDAD_PARCIAL" in str(r)
               for r in T.filas):
        det.append("traza sin aviso de pérdida de trazabilidad")
    alt_a = {"tipo": "PLANTA", "universo": "ESCENARIO"}
    fa = {"alt": alt_a, "completa": True, "cobertura": None, "firma": {"OVERRIDE_TOTAL": True}}
    if mopt.comparabilidad(fa, {"OVERRIDE_TOTAL": False})[0] != "FALSE":
        det.append("override total comparable con corridas verificadas")
    return _ok(not det, "; ".join(det))


def t_cv02():
    """CV02 (TF-011) bloque VACIO no suma cobertura de evidencia; con todos los bloques económicos vacíos o pendientes = 0 %"""
    det = []
    for b in BASES:
        P, _ = silencio(mf.construir_entrada, "CV02", b, (10000,), "EVIDENCIA")
        est = mf.estado_bloques(P)
        if est["REPOSICION"] != "VACIO" or mf.cobertura_bloques(est) != 0.0:
            det.append(f"{b}: {est['REPOSICION']} {mf.cobertura_bloques(est)}")
    P = caso_e2e()
    P["etapas"][0]["activos"] = None
    est = mf.estado_bloques(P)
    if est["REPOSICION"] != "VACIO" or est["DEPRECIACION"] != "PENDIENTE":
        det.append("vacío no detectado en el caso artificial")
    cob = [float(r["COBERTURA_EVIDENCIA_PCT"]) for r in leer_csv("00_gestion_proyecto/cobertura_motor.csv") if r["MODULO"] == "MOTOR_FINANCIERO"]
    if any(c != 0.0 for c in cob):
        det.append(f"cobertura del proyecto {sorted(set(cob))}")
    return _ok(not det, "; ".join(det) or "COBERTURA_EVIDENCIA del proyecto = 0 % en las 15 combinaciones")


def t_cv03():
    """CV03 (TF-011) NO_APLICA no penaliza: un caso completo con valor terminal y reposición no aplicables tiene cobertura 100 %"""
    P = caso_e2e()
    P["impuestos"]["tasa_ganancias"] = 0.30                      # tasa de TEST (caso artificial)
    est = mf.estado_bloques(P)
    aplic = {b: e for b, e in est.items() if e != "NO_APLICA"}
    ok = est["VALOR_TERMINAL"] == "NO_APLICA" and mf.cobertura_bloques(est) == 1.0 and all(e == "CON_EVIDENCIA" for e in aplic.values())
    return _ok(ok, f"{est}")


def _p_export(**imp):
    P = caso_e2e()
    P["demanda"].append({"id": "D2", "producto": "pollo_entero", "canal": "exportacion", "mercado": "EXPORTACION",
                         "categoria": "ESCENARIO", "kg_mes": 0.5, "prioridad": 1})
    P["demanda"][0]["kg_mes"] = 0.5
    P["precios"]["pollo_entero|exportacion|EXPORTACION"] = {"tipo": "CONSTANTE", "usd_kg": 10.0}
    P["canales"]["exportacion"] = {"dias_cobro": 0.0, "pct_descuentos": 0.0, "pct_bonificaciones": 0.0, "pct_devoluciones": 0.0,
                                   "pct_comisiones": 0.0, "costo_logistico_usd_kg": 0.0, "pct_derechos_exportacion": 0.0,
                                   "costo_exportacion_usd_kg": 0.0}
    P["impuestos"].update(pct_iibb=0.03, **imp)
    return P


def t_fs01():
    """FS01 (TF-005) IIBB de exportación no se asume: base separada doméstica / exportación y regla explícita por mercado"""
    det = []
    R = mf.simular(_p_export(iibb_aplica_domestico=True, iibb_aplica_exportacion=False))
    S = R["series"]
    k = 13
    if abs(S["impuestos_sobre_ingresos"][k] - 0.03 * S["venta_bruta_domestica"][k]) > 1e-12 or S["venta_bruta_exportacion"][k] <= 0:
        det.append("exportación gravada con regla FALSE")
    S2 = mf.simular(_p_export(iibb_aplica_domestico=True, iibb_aplica_exportacion=True))["series"]
    if abs(S2["impuestos_sobre_ingresos"][k] - 0.03 * S2["venta_bruta"][k]) > 1e-12:
        det.append("regla TRUE no grava ambas bases")
    if _lanza(mf.validar_entrada, _p_export(iibb_aplica_exportacion="SI")) is False:
        det.append("regla con valor ambiguo aceptada")
    return _ok(not det, "; ".join(det))


def t_fs02():
    """FS02 (TF-005) regla fiscal PENDIENTE bloquea el cálculo: NO_CALCULABLE_REGLA_FISCAL_PENDIENTE y EBITDA / after-tax no publicables"""
    det = []
    R = mf.simular(_p_export(iibb_aplica_domestico=True))
    res = mf.resultados(R)
    if not any(mf.NO_CALC_FISCAL in x and "exportacion" in x for x in R["faltantes"]["IMPUESTOS_INGRESOS"]):
        det.append("sin faltante de regla de exportación")
    if res.get("EBITDA_ULTIMO_ANIO") is not None or res["PUBLICABLE_FLUJO_AFTER_TAX"] or res.get("VAN") is not None:
        det.append("indicadores publicados con regla pendiente")
    R0 = mf.simular(caso_e2e())                                 # sin IIBB (alícuota 0) no se exige regla
    if R0["faltantes"]["IMPUESTOS_INGRESOS"]:
        det.append("regla exigida con alícuota 0")
    ev = [f for f in leer_csv("21_modelo_financiero/inputs_financieros.csv") if f["VARIABLE"].startswith("impuestos.iibb_aplica_")]
    if len(ev) != 2 or any(f["ESTADO"] != "PENDIENTE" or f["VALOR"] for f in ev):
        det.append("reglas IIBB no registradas como PENDIENTE")
    return _ok(not det, "; ".join(det))


IVA_SIMPL = {"modo": "SIMPLIFICADO", "alicuota_ventas": 0.105, "alicuota_compras": 0.21, "alicuota_capex": 0.21}
IVA_DECL = {"base": "NETA", "iva_estado": "DECLARADO", "tasa": 0.105, "condicion_fiscal": "ARTIFICIAL", "elegible_credito": True,
            "criterio": "caso de prueba"}


def t_iv01():
    """IV01 (TF-076) IVA de CAPEX DESCONOCIDO / INCIERTO / NO_DECLARADO no genera crédito fiscal: CREDITO_FISCAL_IVA_CAPEX = PENDIENTE"""
    det = []
    for decl in (None, dict(IVA_DECL, iva_estado="INCIERTO"), dict(IVA_DECL, iva_estado="DESCONOCIDO"),
                 dict(IVA_DECL, iva_estado="NO_DECLARADO"), dict(IVA_DECL, condicion_fiscal=""), dict(IVA_DECL, elegible_credito=None),
                 dict(IVA_DECL, base="BRUTA")):
        P = caso_e2e()
        P["iva"] = dict(IVA_SIMPL)
        P["etapas"][0]["iva_capex"] = decl
        R = mf.simular(P)
        if not any(mf.CREDITO_IVA_CAPEX_PEND in x for x in R["faltantes"]["IVA"]) or R["series"]["flujo_iva"] is not None:
            det.append(f"crédito aceptado con {decl and decl.get('iva_estado')}")
    P = caso_e2e()
    P["iva"] = dict(IVA_SIMPL)
    P["etapas"][0]["iva_capex"] = dict(IVA_DECL)
    S = mf.simular(P)["series"]
    if abs(S["iva_credito_capex"][0] - 200.0 * 0.105) > 1e-9:
        det.append(f"crédito declarado {S['iva_credito_capex'][0]}")
    return _ok(not det, "; ".join(det))


def t_iv02():
    """IV02 (TF-076) IVA de CAPEX incierto tampoco se convierte en costo: CAPEX, OPEX y EBITDA idénticos; un CAPEX del módulo con IVA_INCIERTO no se usa"""
    det = []
    a = mf.simular(caso_e2e())["series"]
    P = caso_e2e()
    P["iva"] = dict(IVA_SIMPL)
    P["etapas"][0]["iva_capex"] = dict(IVA_DECL, iva_estado="INCIERTO")
    b = mf.simular(P)["series"]
    for s_ in ("capex_total", "opex_total", "ebitda"):
        if any(abs(x - y) > 1e-12 for x, y in zip(a[s_], b[s_])):
            det.append(f"{s_} cambia con IVA incierto")
    orig = mf._correr_capex
    try:
        filas = [{"COSTEA": True, "TITULAR": "EMPRESA", "ALERTAS": "IVA_INCIERTO;INCOTERM=EXW"}]
        T = {"TOTAL_PRELIMINAR_USD": 1000.0, "N_CONCEPTOS_E1_E2": 1, "N_CONCEPTOS_E3": 0, "N_CONCEPTOS_E4": 0, "N_CONCEPTOS_E5": 0}
        mf._correr_capex = lambda cc: (filas, {"TOTAL": T}, None)
        v, niv, mot = mf.capex_desde_modulo({})
        if v is not None or "IVA_INCIERTO" not in mot:
            det.append("CAPEX del módulo con IVA_INCIERTO usado como total")
    finally:
        mf._correr_capex = orig
    return _ok(not det, "; ".join(det))


def m12():
    """aceptar un override de usuario sin verificar su arquitectura (CAPEX de C3 en C1)"""
    orig = mf.verificar_override
    mf.verificar_override = lambda *a, **k: []
    try:
        return _rechaza_override("C1", {"capex_usd": 1000.0, "capex_meta": _meta("C3")})[0]
    finally:
        mf.verificar_override = orig


def m13():
    """contar un bloque VACIO como evidencia (cobertura inflada)"""
    orig = mf.estado_bloques
    mf.estado_bloques = lambda P, F=None: {b: ("CON_EVIDENCIA" if e == "VACIO" else e) for b, e in orig(P, F).items()}
    try:
        P, _ = silencio(mf.construir_entrada, "M13", "C1", (10000,), "EVIDENCIA")
        return mf.cobertura_bloques(mf.estado_bloques(P)) == 0.0
    finally:
        mf.estado_bloques = orig


def m14():
    """calcular IIBB de exportación con la regla PENDIENTE (aplicación silenciosa)"""
    orig = mf.disponibilidad
    def disp(P):
        F = orig(P)
        F["IMPUESTOS_INGRESOS"] = [x for x in F["IMPUESTOS_INGRESOS"] if mf.NO_CALC_FISCAL not in x]
        return F
    mf.disponibilidad = disp
    try:
        return mf.resultados(mf.simular(_p_export(iibb_aplica_domestico=True))).get("EBITDA_ULTIMO_ANIO") is None
    finally:
        mf.disponibilidad = orig


def m15():
    """generar crédito fiscal de IVA de CAPEX con IVA incierto (alícuota global aplicada en silencio)"""
    orig = mf.iva_capex_declarado
    mf.iva_capex_declarado = lambda d: (True, "")
    try:
        P = caso_e2e()
        P["iva"] = dict(IVA_SIMPL)
        P["etapas"][0]["iva_capex"] = dict(IVA_DECL, iva_estado="INCIERTO")
        S = mf.simular(P)["series"]
        return S["iva_credito_capex"] is None or sum(S["iva_credito_capex"]) == 0
    finally:
        mf.iva_capex_declarado = orig

# =============================================================================================
# EJECUCIÓN
# =============================================================================================
TESTS = [t_id01, t_id02, t_id03, t_id04, t_id05, t_rp01, t_rp02, t_rp03, t_rp04, t_rp05, t_rp06,
         t_ar01, t_ar02, t_ar03, t_ar04, t_es01, t_es02, t_un01, t_un02, t_dm01, t_dm02, t_dm03,
         t_bm01, t_bm02, t_bm03, t_ut01, t_ut02, t_ut03, t_lo01, t_rh01, t_ct01, t_e2e01, t_e2e02, t_e2e03, t_e2e04, t_e2e05,
         t_fi01, t_fi02, t_fi03, t_fi04, t_fi05, t_fa01, t_fa02, t_ev01, t_ev02, t_ev03,
         t_ri01, t_ri02, t_ri03, t_ri04, t_ri05, t_op01, t_op02, t_op03, t_op04, t_op05, t_op06, t_op07,
         t_cv01, t_tb01, t_mu00, t_ov01, t_ov02, t_ov03, t_cv02, t_cv03, t_fs01, t_fs02, t_iv01, t_iv02]


MUTACIONES += [m12, m13, m14, m15]


def ejecutar_tests(verbose=True):
    res = []
    for t in TESTS:
        try:
            ok, det = t()
        except Exception as e:                       # un test que se rompe es un test que falla
            ok, det = False, f"EXCEPCIÓN {type(e).__name__}: {e}"
        res.append((t.__doc__.split(" ")[0], ok, t.__doc__, det))
        if verbose:
            print(f"  [{'OK' if ok else 'FALLA'}] {t.__doc__}" + (f" — {det}" if det and not ok else ""))
    return res


def prueba_mutaciones(verbose=True):
    res = []
    for m in MUTACIONES:
        try:
            pasa = m()
        except Exception as e:                       # el motor rechazó la mutación con un error: también es detección
            pasa = False
            m.__doc__ += f" [rechazada por el motor: {type(e).__name__}]"
        res.append((m.__name__, not pasa, m.__doc__))
        if verbose:
            print(f"  [{'DETECTADA' if not pasa else 'NO DETECTADA'}] {m.__name__}: {m.__doc__}")
    return res


def main():
    ap = argparse.ArgumentParser(description="Tests de integración final del motor v1 (sesión 21)")
    ap.add_argument("--generar", action="store_true", help="regenera cobertura_motor.csv antes de correr")
    a = ap.parse_args()
    if a.generar:
        escribir_cobertura()
        print("cobertura_motor.csv regenerado")
    print(f"TESTS DE INTEGRACIÓN FINAL DEL MOTOR v{VERSION} ({FECHA})")
    r = ejecutar_tests()
    n_ok = sum(1 for x in r if x[1])
    print(f"Tests: {n_ok}/{len(r)} OK")
    print("MUTACIONES DE INTEGRACIÓN")
    m = prueba_mutaciones()
    n_det = sum(1 for x in m if x[1])
    print(f"Mutaciones detectadas: {n_det}/{len(m)}")
    if n_ok != len(r) or n_det != len(m):
        sys.exit(1)


if __name__ == "__main__":
    main()
