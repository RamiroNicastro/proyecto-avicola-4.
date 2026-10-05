"""Lectura (SOLO LECTURA) del estado real del proyecto: evidencia, validación, trazabilidad, riesgos cualitativos.

Fuentes (no se modifican nunca desde la app):
  00_gestion_proyecto/plan_validacion_final.md, datos_por_validar.md, cobertura_motor.csv, completitud_final_motor.csv,
  trazabilidad_end_to_end.csv, interfaz_app_v1.md
  22_riesgos/prioridad_validacion.csv, que_hacer_ahora.csv, matriz_riesgos.csv, decision_optimizador.csv
  21_modelo_financiero/base_precios_venta.csv, inputs_financieros.csv, escenarios_financieros.csv
"""
import os
import re
import statistics

from . import motor as M

mf = M.mf

PAQUETES = ("CLIENTES", "PLANTA", "ALIMENTO", "POLLITOS", "GRANJAS", "UTILITIES", "TERRENO", "LOGÍSTICA", "RRHH",
            "IMPUESTOS", "FINANCIAMIENTO", "EXPORTACIÓN")
ARCH_PLAN = M.ruta("00_gestion_proyecto", "plan_validacion_final.md")
ARCH_DPV = M.ruta("00_gestion_proyecto", "datos_por_validar.md")


def _tabla_md(lineas):
    filas = [l for l in lineas if l.strip().startswith("|")]
    if len(filas) < 2:
        return []
    cab = [c.strip() for c in filas[0].strip().strip("|").split("|")]
    out = []
    for l in filas[2:]:
        celdas = [c.strip() for c in l.strip().strip("|").split("|")]
        out.append(dict(zip(cab, celdas)))
    return out


def _limpiar_md(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t or "")
    return t.replace("**", "").replace("`", "")


def _dpvs(txt):
    """'DPV-001, 002, 013' → ['DPV-001', 'DPV-002', 'DPV-013'] (la tabla del plan abrevia los números)."""
    out = []
    for m in re.finditer(r"DPV-(\d{3})((?:,\s*\d{3})*)", txt or ""):
        out.append(f"DPV-{m.group(1)}")
        out += [f"DPV-{x.strip()}" for x in m.group(2).split(",") if x.strip()]
    return out


def dpv_registro():
    reg = {}
    with open(ARCH_DPV, encoding="utf-8") as fh:
        for l in fh:
            if re.match(r"^\| DPV-\d{3} ", l):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                reg[c[0]] = {"id": c[0], "dato": _limpiar_md(c[1]), "por_que": _limpiar_md(c[2]), "fuente_sugerida": _limpiar_md(c[3]),
                             "responsable": c[4], "estado": c[5], "fte": c[6], "observaciones": _limpiar_md(c[7])[:600] if len(c) > 7 else ""}
    return reg


def plan_validacion():
    with open(ARCH_PLAN, encoding="utf-8") as fh:
        texto = fh.read()
    lineas = texto.splitlines()
    i1 = next(i for i, l in enumerate(lineas) if l.startswith("## 1."))
    i2 = next(i for i, l in enumerate(lineas) if l.startswith("## 2."))
    mapa = _tabla_md(lineas[i1:i2])
    detalle = {}
    actual = None
    bloque = []
    for l in lineas[i2:]:
        m = re.match(r"^### 2\.\d+ (.+?) — (.+)$", l)
        if m or l.startswith("## 3."):
            if actual:
                detalle[actual] = _tabla_md(bloque)
            bloque = []
            actual = m.group(1).split(" / ")[0].strip() if m else None
            if l.startswith("## 3."):
                break
            continue
        bloque.append(l)
    i3 = next((i for i, l in enumerate(lineas) if l.startswith("## 3.")), len(lineas))
    que_cambia = [_limpiar_md(l[2:]) for l in lineas[i3:] if l.startswith("- ")]
    reg = dpv_registro()
    paquetes = []
    for r in mapa:
        nombre = _limpiar_md(r.get("Paquete", ""))
        clave = nombre.split(" / ")[0].strip()
        dpvs = _dpvs(r.get("DPV centrales", ""))
        paquetes.append({"n": r.get("#"), "paquete": nombre, "clave": clave, "prioridad": _limpiar_md(r.get("Prioridad")),
                         "actor": _limpiar_md(r.get("Actor principal")), "desbloquea": _limpiar_md(r.get("Bloques del motor que desbloquea")),
                         "dpv": [reg.get(d, {"id": d, "dato": "(no encontrado en datos_por_validar.md)", "estado": "?"}) for d in dpvs],
                         "pedidos": [{"actor": _limpiar_md(x.get("Actor")), "que_pedir": _limpiar_md(x.get("Qué pedir")),
                                      "unidad": _limpiar_md(x.get("Unidad")), "desbloquea": _limpiar_md(x.get("Desbloquea"))}
                                     for x in detalle.get(clave, [])]})
    intro = next((_limpiar_md(l[2:]) for l in lineas if l.startswith("> **Prioridad**")), "")
    return {"paquetes": paquetes, "que_cambia": que_cambia, "criterio_prioridad": intro, "fuente": "00_gestion_proyecto/plan_validacion_final.md",
            "n_dpv_registro": len(reg), "n_dpv_validados": sum(1 for d in reg.values() if d["estado"].lower().startswith("validad"))}


def prioridad_validacion():
    filas = M.leer_csv(M.ruta("22_riesgos", "prioridad_validacion.csv"))
    qh = M.leer_csv(M.ruta("22_riesgos", "que_hacer_ahora.csv"))
    return {"prioridad": filas, "que_hacer_ahora": qh,
            "nota": "Prioridad DERIVADA DEL MOTOR (bloqueos). Los empates se muestran como empates (RANK_COMPARTIDO): la app no "
                    "inventa desempates. POTENCIAL_DE_CAMBIAR_DECISION = NO_CALCULADO en evidencia."}


def cobertura():
    filas = M.leer_csv(M.ruta("00_gestion_proyecto", "cobertura_motor.csv"))
    por_mod = {}
    for f in filas:
        por_mod.setdefault(f["MODULO"], []).append(f)
    resumen = {}
    for mod, fs in por_mod.items():
        d = {}
        for k in ("ESTRUCTURAL", "FISICA", "ECONOMICA", "EVIDENCIA"):
            xs = [float(f[f"COBERTURA_{k}_PCT"]) for f in fs if f[f"COBERTURA_{k}_PCT"] not in ("", None)]
            d[k] = {"min": min(xs) if xs else None, "max": max(xs) if xs else None,
                    "media": statistics.fmean(xs) if xs else None, "n": len(xs)}
        resumen[mod] = d
    return {"filas": filas, "resumen": resumen, "fuente": "00_gestion_proyecto/cobertura_motor.csv"}


def completitud_motor():
    return M.leer_csv(M.ruta("00_gestion_proyecto", "completitud_final_motor.csv"))


def progreso():
    """Indicador de validación separado en cuatro dimensiones (#31): no hay una barra única."""
    cob = cobertura()["resumen"]
    comp = completitud_motor()
    fin = M.leer_csv(M.ruta("21_modelo_financiero", "escenarios_financieros.csv"))
    evi = [f for f in fin if f.get("MODO") == "EVIDENCIA"]
    n_pub = sum(1 for f in evi if f.get("PUBLICABLE_VAN") in ("True", "TRUE", "1"))
    reg = dpv_registro()
    return {
        "dimensiones": [
            {"id": "ESTRUCTURA", "titulo": "Motor estructural", "estado": "COMPLETO",
             "pct": cob.get("MOTOR_FINANCIERO", {}).get("ESTRUCTURAL", {}).get("media"),
             "texto": "Los motores 03–22 están completos y auditados (MOTOR_V1 = COMPLETO ESTRUCTURALMENTE)."},
            {"id": "FISICA", "titulo": "Datos físicos", "estado": "PARCIAL",
             "pct": cob.get("OPEX", {}).get("FISICA", {}).get("media"),
             "texto": "Cantidades dimensionadas por los modelos (escenarios), sin validación de campo."},
            {"id": "ECONOMICA", "titulo": "Datos económicos", "estado": "INCOMPLETO",
             "pct": cob.get("OPEX", {}).get("ECONOMICA", {}).get("media"),
             "texto": "Precios, CAPEX y OPEX casi sin datos: ninguna arquitectura costeable."},
            {"id": "EVIDENCIA", "titulo": "Evidencia (E1–E3)", "estado": "INSUFICIENTE",
             "pct": cob.get("MOTOR_FINANCIERO", {}).get("EVIDENCIA", {}).get("media"),
             "texto": f"{n_pub} de {len(evi)} corridas del modo evidencia tienen VAN publicable."}],
        "dpv": {"total": len(reg), "pendientes": sum(1 for d in reg.values() if d["estado"].lower().startswith("pendiente"))},
        "completitud_modulos": comp,
        "estado_general": {"MOTOR_V1": "COMPLETO ESTRUCTURALMENTE", "LISTO_APP_V1": "SÍ", "LISTO_DECISION_REAL": "NO"},
        "nota": "Cada dimensión se mide por separado (cobertura_motor.csv, promedio de configuraciones × escalas). "
                "No se combinan en un único porcentaje."}


def evidencia():
    precios = M.leer_csv(mf.ARCHIVO_PRECIOS)
    inputs = [f for f in M.leer_csv(mf.ARCHIVO_INPUTS) if f["ESCENARIO"] == "EVIDENCIA"]
    dec = [f for f in M.leer_csv(M.ruta("22_riesgos", "decision_optimizador.csv")) if f.get("UNIVERSO") == "EVIDENCIA"]
    fin = M.leer_csv(M.ruta("21_modelo_financiero", "escenarios_financieros.csv"))
    evi = [f for f in fin if f.get("MODO") == "EVIDENCIA"]
    flags = {}
    for fl in mf.FLAGS:
        flags[fl] = sum(1 for f in evi if f.get(fl) in ("True", "TRUE", "1"))
    return {"precios": precios, "inputs": inputs,
            "inputs_resumen": {o: sum(1 for f in inputs if f["ORIGEN"] == o) for o in sorted({f["ORIGEN"] for f in inputs})},
            "optimizador_evidencia": dec[:3], "corridas_evidencia": len(evi), "publicables": flags,
            "umbral": list(mf.umbral_evidencia()), "progreso": progreso(),
            "nota": "Universo EVIDENCIA: solo datos E1–E3 (umbral configurable, DEC-084 abierta). La app lo muestra en "
                    "SOLO LECTURA; para cargar evidencia se edita la base correspondiente con su fuente (fuera de la app)."}


def trazabilidad():
    filas = M.leer_csv(M.ruta("00_gestion_proyecto", "trazabilidad_end_to_end.csv"))
    return {"filas": filas, "fuente": "00_gestion_proyecto/trazabilidad_end_to_end.csv",
            "kpis": {"CAPEX": ["CAPEX"], "OPEX": ["OPEX", "RRHH", "ENERGIA", "AGUA", "ALIMENTO", "POLLITOS"], "CT": ["CT"],
                     "INGRESOS": ["DEMANDA", "DEMANDA → UTILIZACIÓN", "PRODUCCION (aves faenadas)", "MASA PRODUCTO", "PRECIO", "INGRESO"],
                     "EBITDA": ["EBITDA"], "FONDOS": ["FCFF", "CT", "CAPEX"], "VAN": ["FCFF", "VAN"], "TIR": ["FCFF", "TIR"],
                     "PAYBACK": ["FCFF"], "DSCR": ["FCFE / CAJA"], "RIESGO": ["RIESGO"], "OPTIMIZADOR": ["OPTIMIZADOR"],
                     "EVIDENCIA": ["COBERTURA"]}}


def riesgos_cualitativos():
    return {"matriz": M.leer_csv(M.ruta("22_riesgos", "matriz_riesgos.csv")),
            "nota": "Registro cualitativo (BAJA / MEDIA / ALTA / PENDIENTE). La probabilidad del proyecto es PENDIENTE "
                    "(SUP-224); la frecuencia sectorial es otra cosa y se muestra aparte."}


def documento(nombre):
    """Documentos de referencia de solo lectura (lista blanca)."""
    permitidos = {"interfaz_app_v1": ("00_gestion_proyecto", "interfaz_app_v1.md"),
                  "plan_validacion_final": ("00_gestion_proyecto", "plan_validacion_final.md"),
                  "estado_proyecto": ("00_gestion_proyecto", "estado_proyecto.md")}
    if nombre not in permitidos:
        raise KeyError(nombre)
    with open(M.ruta(*permitidos[nombre]), encoding="utf-8") as fh:
        return fh.read()


def hashes_evidencia():
    """Huella de los archivos de evidencia (para el test «un escenario no modifica la evidencia»)."""
    import hashlib
    rutas = [mf.ARCHIVO_PRECIOS, mf.ARCHIVO_INPUTS, mf.ARCHIVO_CURVAS, M.ruta("20_opex", "base_costos_opex.csv"),
             M.ruta("22_riesgos", "inputs_riesgo_optimizacion.csv"), M.ruta("22_riesgos", "escenario_optimizador.json"),
             M.ruta("22_riesgos", "escenarios_stress.csv"), M.ruta("22_riesgos", "distribuciones_riesgo.csv"),
             M.ruta("00_gestion_proyecto", "datos_por_validar.md"), M.ruta("25_fuentes", "registro_fuentes.csv")]
    out = {}
    for r in rutas:
        if os.path.exists(r):
            with open(r, "rb") as fh:
                out[os.path.relpath(r, M.RAIZ)] = hashlib.sha256(fh.read()).hexdigest()
    return out
