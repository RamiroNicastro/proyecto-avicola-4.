#!/usr/bin/env python3
"""
modelo_capacidad_proceso.py — Capacidad de proceso por etapa (sesión 09A)
=========================================================================

Versión 1.1 · 2026-09-30 · Fase 0 (prefactibilidad) · Carpeta 05_proceso_industrial
v1.1 = corrección conceptual: disponibilidad y velocidad separadas y SOLO como sensibilidad;
jerarquía de capacidades; ecuación explícita de 24 h con alerta (no descarte); tiempo de
limpieza provisional t_limpieza(escala, configuración, automatización); capacidades publicadas
por proveedores bloqueadas como dato de diseño.

QUÉ HACE
  Traduce las escalas de 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo en
  CARGAS POR ETAPA del proceso industrial:
    1. ritmo operativo requerido (aves/h netas) — idéntico a 23_plan_expansion (test T01);
    2. ritmo NOMINAL a pedir a un equipo con factores de SENSIBILIDAD de velocidad y
       disponibilidad (no son desempeño industrial demostrado);
    3. aves/día de una línea de ritmo nominal dado (línea ≠ planta);
    4. ecuación de 24 h del establecimiento, holgura y ALERTA de calendario;
    5. flujos por hora y por día de cada corriente desde el balance v1.1;
    6. carcasas simultáneas en el enfriamiento; 7. puestos manuales equivalentes;
    8. carga de congelado según perfiles P1–P3; 9. jerarquía de capacidades (funciones).

QUÉ NO HACE
  No selecciona equipos, proveedores, escala, turnos ni método de enfriamiento; no calcula
  precios, CAPEX ni OPEX; no dimensiona agua, efluentes, frío ni superficies. No modifica los
  modelos anteriores: los IMPORTA (test T08).

DEFINICIONES (ver cuellos_botella.md §2)
  h        = horas NETAS de faena: tiempo en que la línea está en marcha recibiendo aves
             (misma definición que capacidad_preliminar.md; excluye paradas y cambios).
  R        = factor de velocidad: velocidad operativa media en marcha / velocidad nominal
             (microparadas, grilletes vacíos, velocidad reducida). SENSIBILIDAD.
  D        = disponibilidad: tiempo en marcha / tiempo programado de producción
             (paradas no planificadas y cambios de producto). SENSIBILIDAD.
  η = D×R  = factor global (análogo a OEE sin el término de calidad). SENSIBILIDAD 0,70–0,90,
             NO es una eficiencia universal de línea.

FÓRMULAS (E = aves faenadas/día operativo)
  ritmo operativo requerido [aves/h]            = E / h
  ritmo nominal requerido (h netas en marcha)   = E / (h × R)
  ritmo nominal requerido (h programadas)       = E / (h × D × R)      (si h incluyera paradas)
  horas programadas de producción               = h / D
  paradas durante producción [h]                = h × (1/D − 1)
  aves/día de una línea nominal L               = L × T_prog × D × R    (T_prog programadas)
  24 h = faena neta + paradas durante producción + pausas + cambios de turno
         + preparación/arranque + cierre/vaciado + limpieza intermedia
         + limpieza + sanitización + mantenimiento + holgura
  alerta de calendario si holgura < 0 (restricción severa: VALIDAR, no descartar)
  capacidad teórica de equipo   = nominal × horas (solo con nominal de sensibilidad, RFQ
                                  garantizada o medición; nunca una capacidad publicada)
  capacidad efectiva subsistema = nominal × T_prog × D × R  (≤ teórica salvo justificación)
  capacidad del cuello          = mín(capacidades efectivas de subsistemas modelados)
  capacidad operativa de planta = mín(cuello; restricciones externas: aves, subproductos, ...)
  producción real (período)     = capacidad operativa × (días de faena − paradas planificadas
                                  de día completo) × utilización (≤ 1)

PARÁMETROS (todos [SUPUESTO] de sensibilidad o [PVDP]; IDs provisionales en
actualizaciones_gestion_09A.md)
  D, R por escenario .............................................. SUP-061
  ventanas no productivas y t_limpieza provisional ................ SUP-062
  productividad manual de referencia y factor prudente 0,5 ........ SUP-063
  residencia en enfriamiento: inmersión 50 min; aire 90–150 min ... SUP-064
  kg/ave: balance v1.1 vía 23_plan_expansion/modelo_escala.py; perfiles P1–P3 (SUP-055).

UNIDADES: aves, aves/h, kg, kg/h, t, h, min. CSV con punto decimal.

USO
  python3 05_proceso_industrial/modelo_capacidad_proceso.py              # tests + CSV + tablas
  python3 05_proceso_industrial/modelo_capacidad_proceso.py --solo-tests
  python3 05_proceso_industrial/modelo_capacidad_proceso.py --mutaciones # prueba los tests
Salida: 05_proceso_industrial/capacidad_proceso.csv
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True           # no dejar __pycache__ en las carpetas de los modelos

import argparse  # noqa: E402
import csv  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
import re  # noqa: E402
import subprocess  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "23_plan_expansion"))
import modelo_escala as me  # noqa: E402  (escala v1.1; importa producción, balance y subproductos)

VERSION = "1.1"
FECHA = "2026-09-30"
F_ESC = "23_plan_expansion/modelo_escala.py (v1.1)"
F_BAL = "04_balance_masa/modelo_balance_masa.py (v1.1) vía modelo_escala.kg_por_ave"
F_PROPIO = "05_proceso_industrial/modelo_capacidad_proceso.py"
CSV_SALIDA = os.path.join(AQUI, "capacidad_proceso.csv")
CSV_ESCALA = os.path.join(RAIZ, "23_plan_expansion", "escenarios_escala.csv")

ESCALAS = list(me.ESCALAS)               # 2.500 / 5.000 / 10.000 / 20.000 (no se elige)
HORAS_NETAS = list(me.HORAS_NETAS)       # 6 / 8 / 10 / 16 (16 = 2 × 8; SUP-053)
PESO = me.PESO_REF                       # 2,9 kg
SUP = "[SUPUESTO]"
NOTA_SENS = "sensibilidad del modelo; NO es desempeño industrial demostrado"

# SUP-061 — factores de SENSIBILIDAD (no datos): D disponibilidad, R factor de velocidad.
# η = D × R ≈ 0,70 / 0,80 / 0,90. Ningún fabricante ni planta argentina respalda estos valores.
SENSIBILIDAD = {
    "baja":  {"D": 0.85, "R": 0.82},
    "media": {"D": 0.90, "R": 0.89},
    "alta":  {"D": 0.95, "R": 0.95},
}

# SUP-062 — ventanas no productivas (h). Tres escenarios de calendario; cada uno toma la
# disponibilidad D del escenario de sensibilidad asociado. Sin dato argentino (DPV-082, DPV-091).
VENTANAS = {
    "optimista":    {"sens": "alta", "preparacion_arranque": 0.50, "pausas_8h": 0.50, "limpieza_intermedia_8h": 0.25,
                     "cierre_vaciado": 0.50, "cambio_turno": 0.25, "limpieza": 2.00, "sanitizacion": 1.00,
                     "mantenimiento": 0.50},
    "media":        {"sens": "media", "preparacion_arranque": 0.75, "pausas_8h": 0.75, "limpieza_intermedia_8h": 0.33,
                     "cierre_vaciado": 0.75, "cambio_turno": 0.33, "limpieza": 2.75, "sanitizacion": 1.25,
                     "mantenimiento": 1.00},
    "conservadora": {"sens": "baja", "preparacion_arranque": 1.00, "pausas_8h": 1.00, "limpieza_intermedia_8h": 0.50,
                     "cierre_vaciado": 1.00, "cambio_turno": 0.50, "limpieza": 4.00, "sanitizacion": 2.00,
                     "mantenimiento": 2.00},
}
COMPONENTES_24H = ("faena_neta", "paradas_durante_produccion", "pausas", "cambio_turno", "preparacion_arranque",
                   "cierre_vaciado", "limpieza_intermedia", "limpieza", "sanitizacion", "mantenimiento")
# Relación de la limpieza con escala, configuración y automatización: PROVISIONAL (factor 1).
# Dato de campo pendiente: duración, dotación, simultaneidad, CIP/manual, preoperacional (DPV-091).
LIMPIEZA_PROVISIONAL = True

# SUP-063 — productividades manuales de referencia [PVDP · débil] (no argentinas; no dotación)
PRODUCTIVIDAD = {
    "colgado": {"aves_h_operario": 23 * 60, "fuente": "FTE-219"},
    "eviscerado_manual": {"aves_h_operario": 2 * 60, "fuente": "FTE-218"},
}
FACTOR_PRUDENTE = 0.5

# SUP-064 — tiempo de residencia en el enfriamiento [PVDP] (FTE-217)
RESIDENCIA_MIN = {"inmersion": 50, "aire_min": 90, "aire_max": 150}

# Referencias de proveedores: capacidades NOMINALES DECLARADAS en páginas oficiales. Evidencia de
# que existen arquitecturas; PROHIBIDO usarlas como capacidad de diseño (test T18).
REFERENCIAS_PROVEEDORES = {
    "baader_compact_plant_396": {"min_aves_h": 600, "max_aves_h": 1600, "fuente": "FTE-200",
                                 "nota": "evisceración manual; según tamaño de ave; expansión prevista"},
    "meyn_leap": {"min_aves_h": 1300, "max_aves_h": 15000, "fuente": "FTE-194",
                  "nota": "concepto modular; no implica que la inversión inicial llegue a 15.000"},
    "jbt_marel_calisa2": {"min_aves_h": 9500, "max_aves_h": 15000, "fuente": "FTE-197",
                          "nota": "planta argentina; referencia tecnológica, NO benchmark económico"},
}
ORIGENES_VALIDOS = {"sensibilidad", "rfq_garantizada", "medicion_planta"}

# Líneas nominales ilustrativas (no modelos de proveedor)
LINEAS_NOMINALES = [312.5, 625, 1250, 2500, 3125]

CAMPOS = ["bloque", "escala_aves_dia", "horas_netas", "parametro", "variable", "valor", "unidad",
          "base", "fuente_modelo", "clasificacion", "nota"]
PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen)\b",
                                 re.IGNORECASE)


class ErrorProceso(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. RITMOS, LÍNEAS Y JERARQUÍA DE CAPACIDADES
# ---------------------------------------------------------------------------
def validar(E=None, h=None, f=None):
    if E is not None and E <= 0:
        raise ErrorProceso(f"Valor de aves inválido: {E}")
    if h is not None and not 0 < h <= 24:
        raise ErrorProceso(f"Horas fuera de rango (0; 24]: {h}")
    if f is not None and not 0 < f <= 1:
        raise ErrorProceso(f"Factor fuera de rango (0; 1]: {f}")


def eta(sens):
    s = SENSIBILIDAD[sens]
    return s["D"] * s["R"]


def ritmo_operativo(E, h):
    validar(E=E, h=h)
    return E / h


def ritmo_nominal_requerido(E, h, R, D=1.0):
    """Nominal a pedir para E aves/día. Con D = 1, h son horas netas en marcha; con D < 1, h son
    horas programadas que incluyen paradas."""
    validar(E=E, h=h, f=R)
    validar(f=D)
    return ritmo_operativo(E, h) / (R * D)


def aves_dia_linea(L, t_prog, D, R):
    validar(E=L, h=t_prog, f=D)
    validar(f=R)
    return L * t_prog * D * R


def capacidad_teorica_equipo(nominal_aves_h, horas, origen):
    """Capacidad teórica = nominal × horas. El nominal debe venir de sensibilidad, RFQ con
    capacidad garantizada o medición en planta; nunca de una capacidad publicada."""
    if origen not in ORIGENES_VALIDOS:
        raise ErrorProceso(f"Origen '{origen}' no admitido como diseño (capacidades publicadas por "
                           f"proveedores son referencia, no diseño)")
    validar(E=nominal_aves_h, h=horas)
    return nominal_aves_h * horas


def capacidad_efectiva(nominal_aves_h, t_prog, D, R, origen="sensibilidad", justificacion=None):
    """Capacidad efectiva de un subsistema. D o R > 1 (capacidad efectiva > teórica) exige
    justificación explícita (p. ej., capacidad garantizada medida por encima de la nominal)."""
    teorica = capacidad_teorica_equipo(nominal_aves_h, t_prog, origen)
    for f in (D, R):
        if f <= 0:
            raise ErrorProceso(f"Factor no positivo: {f}")
        if f > 1 and not justificacion:
            raise ErrorProceso("Capacidad operativa superior a la nominal sin justificación")
    return teorica * D * R


def capacidad_cuello(subsistemas: dict):
    """Capacidad del cuello de botella = mínimo de las capacidades efectivas modeladas."""
    if not subsistemas:
        raise ErrorProceso("Sin subsistemas")
    k = min(subsistemas, key=subsistemas.get)
    return subsistemas[k], k


def capacidad_planta(etapas: dict):
    """Compatibilidad v1.0: capacidad = mínimo de etapas (aves/día)."""
    return capacidad_cuello(etapas)


def capacidad_operativa_planta(subsistemas: dict, restricciones_externas: dict | None = None):
    todas = dict(subsistemas)
    todas.update(restricciones_externas or {})
    return capacidad_cuello(todas)


def produccion_real(cap_operativa_dia, dias_faena, dias_parada_planificada=0, utilizacion=1.0):
    if not 0 <= utilizacion <= 1:
        raise ErrorProceso(f"Utilización fuera de [0; 1]: {utilizacion}")
    if not 0 <= dias_parada_planificada <= dias_faena:
        raise ErrorProceso("Días de parada planificada inválidos")
    return cap_operativa_dia * (dias_faena - dias_parada_planificada) * utilizacion


def puestos_equivalentes(rate, operacion, prudente=False):
    prod = PRODUCTIVIDAD[operacion]["aves_h_operario"] * (FACTOR_PRUDENTE if prudente else 1)
    return math.ceil(rate / prod - 1e-9)


# ---------------------------------------------------------------------------
# 2. ECUACIÓN DE 24 HORAS
# ---------------------------------------------------------------------------
def t_limpieza(escala=None, configuracion="B", automatizacion=None, escenario="media"):
    """Tiempo de limpieza (h/día). PROVISIONAL: hoy no varía con escala, configuración ni
    automatización (factor 1). Reemplazar con datos de campo (DPV-091)."""
    base = VENTANAS[escenario]["limpieza"]
    factor = 1.0                              # f(escala, configuracion, automatizacion) pendiente
    return base * factor


def ventana_24h(h, escenario="media", limpieza_h=None, escala=None, configuracion="B", automatizacion=None,
                turnos=None):
    """24 h = componentes + holgura. turnos por defecto: 1 hasta 10 h netas (turno extendido, a validar
    con el convenio, DPV-082); por encima, un turno por cada 8 h netas."""
    validar(h=h)
    v = VENTANAS[escenario]
    D = SENSIBILIDAD[v["sens"]]["D"]
    if turnos is None:
        turnos = 1 if h <= 10 else math.ceil(h / 8 - 1e-9)
    comp = {
        "faena_neta": h,
        "paradas_durante_produccion": h * (1 / D - 1),
        "pausas": v["pausas_8h"] * h / 8,
        "cambio_turno": v["cambio_turno"] * max(turnos - 1, 0),
        "preparacion_arranque": v["preparacion_arranque"],
        "cierre_vaciado": v["cierre_vaciado"],
        "limpieza_intermedia": v["limpieza_intermedia_8h"] * h / 8,
        "limpieza": t_limpieza(escala, configuracion, automatizacion, escenario) if limpieza_h is None else limpieza_h,
        "sanitizacion": v["sanitizacion"],
        "mantenimiento": v["mantenimiento"],
    }
    total = sum(comp.values())
    holgura = 24 - total
    return {"total": total, "holgura": holgura, "alerta": holgura < 0, "componentes": comp}


def ventana_total(h, esc="media"):
    """Compatibilidad v1.0: (total, holgura, componentes)."""
    r = ventana_24h(h, esc)
    return r["total"], r["holgura"], r["componentes"]


def horas_netas_max_24h(escenario="media", paso=0.01):
    """Máximas horas netas que caben en 24 h con el escenario de ventanas (búsqueda por pasos)."""
    h, mejor = paso, 0.0
    while h <= 24:
        if ventana_24h(h, escenario)["holgura"] >= 0:
            mejor = h
        h = round(h + paso, 6)
    return mejor


# ---------------------------------------------------------------------------
# 3. FLUJOS POR ETAPA (kg/ave del balance v1.1)
# ---------------------------------------------------------------------------
def kg_ave_config(config):
    k, b = me.kg_por_ave(config)
    fr = me.mb.fracciones_primarias(PESO, me.REND)
    kg = {
        "peso_vivo": (k["peso_vivo"], "vivo"),
        "carcasa_pre_chiller": (fr["carcasa"] * PESO, "biologica"),
        "a_trozado": (k["kg_trozado"], "biologica"),
        "a_deshuese": (k["kg_deshuese"], "biologica"),
        "a_cms": (k["kg_cms"], "biologica"),
        "comestible_a_empaque": (k["comestible"], "comercial"),
        "sangre_recuperada": (k["sangre"], "biologica"),
        "plumas_humedas": (k["plumas"], "biologica+agua"),
        "visceras_no_comestibles": (k["visceras"], "biologica"),
        "cabezas": (k["cabeza"], "biologica"),
        "garras_a_y_segunda": (k["garras"], "comercial"),
        "menudencias_y_cuello": (k["menudencias"] + k["cuello"], "comercial"),
        "solidos_a_retirar": (k["solidos_a_retirar"], "biologica+agua"),
        "rendering_potencial": (k["rendering_potencial"], "biologica+agua"),
    }
    return kg, k


# ---------------------------------------------------------------------------
# 4. CONSTRUCCIÓN DE LA TABLA
# ---------------------------------------------------------------------------
class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, h, parametro, variable, valor, unidad, base, fuente, clasif, nota=""):
        if isinstance(valor, bool):
            valor = int(valor)
        if not isinstance(valor, (int, float)) or math.isnan(valor) or math.isinf(valor):
            raise ErrorProceso(f"Valor no numérico en {bloque}/{variable}")
        self.filas.append({"bloque": bloque, "escala_aves_dia": E, "horas_netas": h, "parametro": parametro,
                           "variable": variable, "valor": valor, "unidad": unidad, "base": base,
                           "fuente_modelo": fuente, "clasificacion": clasif, "nota": nota})

    def q(self, **f):
        r = [x for x in self.filas if all(x[k] == v for k, v in f.items())]
        if len(r) != 1:
            raise ErrorProceso(f"Consulta ambigua o vacía ({len(r)}): {f}")
        return r[0]["valor"]


def construir(escalas=None, horas=None):
    escalas = escalas or ESCALAS
    horas = horas or HORAS_NETAS
    t = Tabla()
    kgs = {c: kg_ave_config(c)[0] for c in "ABC"}
    for E in escalas:
        for h in horas:
            r = ritmo_operativo(E, h)
            t.add("ritmo", E, h, "", "ritmo_operativo_requerido", r, "aves/h", "aves", F_PROPIO,
                  "[ESTIMACIÓN]", "= E / h netas; igual a 23_plan_expansion (T01)")
            t.add("ritmo", E, h, "", "aves_por_minuto", r / 60, "aves/min", "aves", F_PROPIO, "[ESTIMACIÓN]")
            t.add("ritmo", E, h, "", "segundos_por_ave", 3600 / r, "s", "aves", F_PROPIO, "[ESTIMACIÓN]")
            for nombre, s in SENSIBILIDAD.items():
                t.add("ritmo_nominal", E, h, f"sensibilidad={nombre}", "ritmo_nominal_requerido_h_netas",
                      ritmo_nominal_requerido(E, h, s["R"]), "aves/h", "aves", F_PROPIO, SUP,
                      f"= E/(h×R); R = {s['R']}; SUP-061; {NOTA_SENS}")
                t.add("ritmo_nominal", E, h, f"sensibilidad={nombre}", "ritmo_nominal_requerido_h_programadas",
                      ritmo_nominal_requerido(E, h, s["R"], s["D"]), "aves/h", "aves", F_PROPIO, SUP,
                      f"= E/(h×D×R) si h incluyera paradas; η = {eta(nombre):.3f}; {NOTA_SENS}")
            for esc in VENTANAS:
                w = ventana_24h(h, esc, escala=E)
                pref = f"ventana={esc}"
                for c, val in w["componentes"].items():
                    t.add("ventana_24h", E, h, pref, f"h_{c}", val, "h", "h", F_PROPIO,
                          "[ESTIMACIÓN]" if c == "faena_neta" else SUP,
                          "t_limpieza PROVISIONAL (no varía con escala)" if c == "limpieza" else "SUP-062")
                t.add("ventana_24h", E, h, pref, "ventana_total_establecimiento", w["total"], "h", "h", F_PROPIO, SUP,
                      "SUP-062; relación con la escala provisional")
                t.add("ventana_24h", E, h, pref, "holgura_24h", w["holgura"], "h", "h", F_PROPIO, SUP,
                      "negativa = restricción severa de calendario; validar con proveedores y plantas antes de descartar")
                t.add("ventana_24h", E, h, pref, "alerta_calendario", w["alerta"], "0/1", "h", F_PROPIO, SUP,
                      "1 = alerta (no descarte)")
            for modo, minutos in RESIDENCIA_MIN.items():
                n = r * minutos / 60
                t.add("enfriamiento", E, h, f"residencia={modo}", "carcasas_simultaneas_en_enfriamiento", n,
                      "aves", "aves", F_PROPIO, SUP, f"{minutos} min; SUP-064 [PVDP]")
                t.add("enfriamiento", E, h, f"residencia={modo}", "kg_carcasa_simultaneos_en_enfriamiento",
                      n * kgs["B"]["carcasa_pre_chiller"][0], "kg", "biologica", F_BAL, SUP,
                      "carcasa eviscerada caliente 2,9 kg (sin agua)")
            for op in PRODUCTIVIDAD:
                for prud in (False, True):
                    t.add("puestos_manuales", E, h, f"{op};{'prudente' if prud else 'referencia'}",
                          "puestos_equivalentes", puestos_equivalentes(r, op, prud), "puestos", "aves",
                          F_PROPIO, SUP, f"productividad {PRODUCTIVIDAD[op]['fuente']} [PVDP · débil]; no es dotación")
            for c in "ABC":
                for var, (kg, base) in kgs[c].items():
                    if kg == 0:
                        continue
                    t.add("flujo_hora", E, h, f"config={c}", f"{var}_kg_h", kg * r, "kg/h", base, F_BAL,
                          "[ESTIMACIÓN]")
        for c in "ABC":
            for var, (kg, base) in kgs[c].items():
                if kg == 0:
                    continue
                t.add("flujo_dia", E, "", f"config={c}", f"{var}_t_dia", kg * E / 1000, "t", base, F_BAL,
                      "[ESTIMACIÓN]", "por día operativo")
        for p, (nombre, perfil) in me.PERFILES_DESTINO.items():
            frac = perfil["congelado"] + perfil["exportacion"]
            t.add("congelado", E, "", f"perfil={p};config=B", "comestible_a_congelar_t_dia",
                  kgs["B"]["comestible_a_empaque"][0] * E * frac / 1000, "t", "comercial", F_ESC, "[ESTIMACIÓN]",
                  f"{nombre}: {frac:.0%} congelado o exportación (SUP-055, ilustrativo)")
    for esc in VENTANAS:
        t.add("ventana_24h", "", "", f"ventana={esc}", "horas_netas_max_en_24h", horas_netas_max_24h(esc), "h", "h",
              F_PROPIO, SUP, "máximo de horas netas con holgura ≥ 0; sensibilidad")
    for L in LINEAS_NOMINALES:
        for h in HORAS_NETAS:
            for nombre, s in SENSIBILIDAD.items():
                t.add("linea_nominal", "", h, f"linea={L};sensibilidad={nombre}", "aves_dia_con_h_programadas",
                      aves_dia_linea(L, h, s["D"], s["R"]), "aves", "aves", F_PROPIO, SUP,
                      f"= L × h programadas × D × R; línea ilustrativa, no modelo de proveedor; {NOTA_SENS}")
    for k, ref in REFERENCIAS_PROVEEDORES.items():
        for lim in ("min_aves_h", "max_aves_h"):
            t.add("referencia_proveedor", "", "", k, lim, ref[lim], "aves/h", "aves", ref["fuente"],
                  "[VERIFICADO · fuente primaria del fabricante; lectura del promotor]",
                  f"capacidad NOMINAL DECLARADA; referencia, no diseño; {ref['nota']}")
    return t


# ---------------------------------------------------------------------------
# 5. TESTS
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _lanza(f, *a, **k):
    try:
        f(*a, **k)
    except ErrorProceso:
        return True
    except Exception:  # noqa: BLE001  (error no controlado = el modelo no valida la entrada)
        return False
    return False


def ejecutar_tests(verbose=True):
    t = construir()
    res = []

    def chk(nombre, ok, detalle=""):
        res.append((nombre, bool(ok), detalle))

    # T01 trazabilidad con 23_plan_expansion
    ok, n = True, 0
    with open(CSV_ESCALA, newline="", encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            if fila["bloque"] == "ritmo_linea" and fila["variable"] == "aves_por_hora_neta" \
                    and fila["dias_semana"] == "5":
                E, h = int(fila["escala_aves_dia"]), int(fila["parametro"].split("=")[1])
                ok &= _cerca(t.q(bloque="ritmo", escala_aves_dia=E, horas_netas=h,
                                 variable="ritmo_operativo_requerido"), float(fila["valor"]))
                n += 1
    chk("T01 ritmo = escenarios_escala.csv", ok and n == len(ESCALAS) * len(HORAS_NETAS), f"{n} valores")

    # T02 nominal ≥ operativo; menor factor exige más; con paradas incluidas exige más
    ok = True
    for E in ESCALAS:
        for h in HORAS_NETAS:
            r = t.q(bloque="ritmo", escala_aves_dia=E, horas_netas=h, variable="ritmo_operativo_requerido")
            a = [t.q(bloque="ritmo_nominal", escala_aves_dia=E, horas_netas=h, parametro=f"sensibilidad={n}",
                     variable="ritmo_nominal_requerido_h_netas") for n in ("baja", "media", "alta")]
            b = [t.q(bloque="ritmo_nominal", escala_aves_dia=E, horas_netas=h, parametro=f"sensibilidad={n}",
                     variable="ritmo_nominal_requerido_h_programadas") for n in ("baja", "media", "alta")]
            ok &= all(x >= r for x in a) and a[0] > a[1] > a[2] and all(y > x for x, y in zip(a, b))
    chk("T02 ritmo nominal ≥ operativo; menor factor o paradas incluidas exigen más", ok)

    # T03 jerarquía: cuello = mínimo; operativa = mín(cuello, externas); real ≤ operativa × días
    subs = {"linea_faena": 20000, "evisceracion": 18000, "chiller": 19000, "trozado": 15000, "camaras": 17000}
    cap, et = capacidad_cuello(subs)
    op, et2 = capacidad_operativa_planta(subs, {"abastecimiento_aves": 16000, "retiro_subproductos": 14000})
    real = produccion_real(op, 250, 5, 0.9)
    chk("T03 cuello = mínimo; operativa = mín(cuello, restricciones); real ≤ operativa × días",
        cap == 15000 and et == "trozado" and cap < subs["linea_faena"] and op == 14000
        and et2 == "retiro_subproductos" and _cerca(real, 14000 * 245 * 0.9) and real <= op * 250
        and capacidad_planta(subs)[0] == 15000)

    # T04 conservación: flujo/h × h = kg/ave × E
    ok = True
    for c in "ABC":
        kg, k = kg_ave_config(c)
        for E in ESCALAS:
            ok &= _cerca(t.q(bloque="flujo_dia", escala_aves_dia=E, parametro=f"config={c}",
                             variable="sangre_recuperada_t_dia"), k["sangre"] * E / 1000)
            for h in HORAS_NETAS:
                for var in ("plumas_humedas", "comestible_a_empaque", "peso_vivo"):
                    fh = t.q(bloque="flujo_hora", escala_aves_dia=E, horas_netas=h, parametro=f"config={c}",
                             variable=f"{var}_kg_h")
                    ok &= _cerca(fh * h, kg[var][0] * E)
    chk("T04 flujos/h × horas = kg/ave × escala (balance v1.1)", ok)

    # T05 ecuación de 24 h: total = Σ componentes; holgura = 24 − total; crece con h
    ok = True
    for esc in VENTANAS:
        prev = -1
        for h in HORAS_NETAS:
            w = ventana_24h(h, esc)
            ok &= _cerca(w["total"], sum(w["componentes"].values())) and _cerca(w["holgura"], 24 - w["total"])
            ok &= w["total"] > prev and w["total"] > h
            prev = w["total"]
    chk("T05 24 h = Σ componentes + holgura; total > horas netas", ok)

    # T06 linealidad de flujos; ventana independiente de la escala (provisional)
    ok = True
    for h in HORAS_NETAS:
        for c in "ABC":
            a = t.q(bloque="flujo_hora", escala_aves_dia=5000, horas_netas=h, parametro=f"config={c}",
                    variable="peso_vivo_kg_h")
            b = t.q(bloque="flujo_hora", escala_aves_dia=10000, horas_netas=h, parametro=f"config={c}",
                    variable="peso_vivo_kg_h")
            ok &= _cerca(b, 2 * a)
    chk("T06 flujos lineales con la escala", ok and LIMPIEZA_PROVISIONAL)

    # T07 sin cifras económicas
    txt = " ".join(" ".join(str(v) for v in f.values()) for f in t.filas)
    chk("T07 sin cifras económicas", not PALABRAS_ECONOMICAS.search(txt.replace("_", " ")))

    # T08 modelos anteriores intactos (git)
    try:
        carpetas = ["03_produccion_primaria", "04_balance_masa", "07_subproductos", "23_plan_expansion"]
        d = subprocess.run(["git", "-C", RAIZ, "status", "--porcelain", "--"] + carpetas,
                           capture_output=True, text=True, check=True).stdout.strip()
        chk("T08 modelos anteriores sin cambios (git status)", d == "", d[:200])
    except (OSError, subprocess.CalledProcessError) as e:
        chk("T08 modelos anteriores sin cambios (git status)", True, f"git no disponible: {e}")

    # T09 inventario del enfriamiento = ritmo × residencia
    ok = True
    for E in ESCALAS:
        for h in HORAS_NETAS:
            for modo, m in RESIDENCIA_MIN.items():
                ok &= _cerca(t.q(bloque="enfriamiento", escala_aves_dia=E, horas_netas=h,
                                 parametro=f"residencia={modo}", variable="carcasas_simultaneas_en_enfriamiento"),
                             E / h * m / 60)
    chk("T09 carcasas en enfriamiento = ritmo × residencia", ok)

    # T10 entradas inválidas detienen el modelo con ErrorProceso
    casos = [(ritmo_nominal_requerido, (1000, 8, 1.2)), (ritmo_nominal_requerido, (1000, 8, 0)),
             (ritmo_operativo, (1000, 25)), (ritmo_operativo, (-1, 8)), (capacidad_cuello, ({},)),
             (produccion_real, (1000, 250, 0, 1.2)), (ventana_24h, (30,))]
    chk("T10 entradas inválidas detienen el modelo con ErrorProceso", all(_lanza(f, *a) for f, a in casos))

    # T11 línea nominal 2.500 aves/h × 8 h programadas < 20.000 con factores < 1
    chk("T11 línea nominal de 2.500 aves/h × 8 h programadas < 20.000 aves/día (sensibilidad)",
        all(t.q(bloque="linea_nominal", horas_netas=8, parametro=f"linea=2500;sensibilidad={n}",
                variable="aves_dia_con_h_programadas") < 20000 for n in SENSIBILIDAD))

    # T12 cada flujo pertenece a una sola configuración
    chk("T12 cada flujo pertenece a una sola configuración (A/B/C no se suman)",
        all(f["parametro"].count("config=") == 1 for f in t.filas if f["bloque"].startswith("flujo")))

    # T13 la ecuación de 24 h contiene todos los componentes exigidos
    ok = True
    for esc, v in VENTANAS.items():
        for h in HORAS_NETAS:
            c = ventana_24h(h, esc)["componentes"]
            ok &= tuple(c) == COMPONENTES_24H and _cerca(c["sanitizacion"], v["sanitizacion"]) \
                and _cerca(c["mantenimiento"], v["mantenimiento"]) and c["limpieza"] > 0
    chk("T13 24 h incluye paradas, limpieza, sanitización, mantenimiento, arranque y otras ventanas", ok)

    # T14 factores de sensibilidad nunca como dato verificado
    sens_bloques = {"ritmo_nominal", "ventana_24h", "linea_nominal", "puestos_manuales", "enfriamiento"}
    ok = all(f["clasificacion"] == SUP for f in t.filas if f["bloque"] in sens_bloques and f["variable"] != "h_faena_neta")
    ok &= not any("VERIFICADO" in f["clasificacion"] for f in t.filas if f["bloque"] != "referencia_proveedor")
    ok &= all(NOTA_SENS in f["nota"] for f in t.filas if f["bloque"] in {"ritmo_nominal", "linea_nominal"})
    chk("T14 disponibilidad/velocidad/eficiencia siempre [SUPUESTO] de sensibilidad, nunca [VERIFICADO]", ok)

    # T15 capacidad operativa no supera la nominal sin justificación
    ok = _lanza(capacidad_efectiva, 1000, 8, 1.05, 0.9)
    ok &= _lanza(capacidad_efectiva, 1000, 8, 0.9, 1.1)
    ok &= _cerca(capacidad_efectiva(1000, 8, 1.02, 1.0, "medicion_planta", justificacion="medición"), 8160)
    for s in SENSIBILIDAD.values():
        ok &= capacidad_efectiva(1000, 8, s["D"], s["R"]) <= capacidad_teorica_equipo(1000, 8, "sensibilidad")
    chk("T15 capacidad efectiva ≤ teórica salvo justificación explícita", ok)

    # T16 total > 24 h genera ALERTA (no excepción, no descarte)
    ok, n_alerta = True, 0
    for esc in VENTANAS:
        for h in HORAS_NETAS:
            w = ventana_24h(h, esc)
            ok &= w["alerta"] == (w["total"] > 24)
            n_alerta += w["alerta"]
            ok &= t.q(bloque="ventana_24h", escala_aves_dia=ESCALAS[0], horas_netas=h, parametro=f"ventana={esc}",
                      variable="alerta_calendario") == int(w["alerta"])
    chk("T16 horas netas + ventanas > 24 h ⇒ alerta de calendario (sin excepción)", ok and n_alerta > 0)

    # T17 modificar el tiempo de limpieza cambia la holgura en la misma magnitud
    ok = True
    for esc in VENTANAS:
        for h in HORAS_NETAS:
            base = ventana_24h(h, esc)
            mas = ventana_24h(h, esc, limpieza_h=base["componentes"]["limpieza"] + 1.5)
            ok &= _cerca(mas["holgura"], base["holgura"] - 1.5)
    chk("T17 +Δ en t_limpieza ⇒ −Δ en holgura", ok)

    # T18 capacidades de proveedores no se usan como diseño
    ok = all(_lanza(capacidad_teorica_equipo, ref["max_aves_h"], 8, "referencia_proveedor")
             for ref in REFERENCIAS_PROVEEDORES.values())
    refs = {v for r in REFERENCIAS_PROVEEDORES.values() for v in (r["min_aves_h"], r["max_aves_h"])}
    ok &= not refs & set(LINEAS_NOMINALES)
    fuentes_ref = {r["fuente"] for r in REFERENCIAS_PROVEEDORES.values()}
    ok &= not any(f["fuente_modelo"] in fuentes_ref for f in t.filas if f["bloque"] != "referencia_proveedor")
    chk("T18 capacidades publicadas por proveedores = referencia, nunca capacidad de diseño", ok)

    if verbose:
        for nombre, ok, d in res:
            print(f"  {'OK  ' if ok else 'FALLA'} {nombre}" + (f" — {d}" if d and not ok else ""))
        print(f"  {sum(ok for _, ok, _ in res)}/{len(res)} tests correctos")
    return res


# ---------------------------------------------------------------------------
# 6. MUTACIONES (verifican que los tests detectan errores típicos)
# ---------------------------------------------------------------------------
def prueba_mutaciones():
    g = globals()
    claves = ("ritmo_nominal_requerido", "capacidad_cuello", "ventana_24h", "ritmo_operativo", "aves_dia_linea",
              "t_limpieza", "capacidad_efectiva", "capacidad_teorica_equipo")
    orig = {k: g[k] for k in claves}

    def ventana_sin_sanit(h, escenario="media", **kw):
        w = orig["ventana_24h"](h, escenario, **kw)
        c = {k: v for k, v in w["componentes"].items() if k != "sanitizacion"}
        tot = sum(c.values())
        return {"total": tot, "holgura": 24 - tot, "alerta": tot > 24, "componentes": c}

    def ventana_sin_alerta(h, escenario="media", **kw):
        w = orig["ventana_24h"](h, escenario, **kw)
        w["alerta"] = False
        return w

    def ventana_ignora_limpieza(h, escenario="media", limpieza_h=None, **kw):
        return orig["ventana_24h"](h, escenario, **kw)

    mutaciones = [
        ("M01 nominal = operativo × factor (invertido)", "ritmo_nominal_requerido",
         lambda E, h, R, D=1.0: (E / h) * R * D),
        ("M02 cuello = subsistema MÁXIMO", "capacidad_cuello",
         lambda s: (max(s.values()), max(s, key=s.get)) if s else (_ for _ in ()).throw(ErrorProceso("x"))),
        ("M03 24 h sin sanitización", "ventana_24h", ventana_sin_sanit),
        ("M04 ritmo con horas de turno fijas (8 h)", "ritmo_operativo", lambda E, h: E / 8),
        ("M05 línea nominal sin factores", "aves_dia_linea", lambda L, t, D, R: L * t),
        ("M06 alerta de calendario desactivada", "ventana_24h", ventana_sin_alerta),
        ("M07 el tiempo de limpieza ingresado se ignora", "ventana_24h", ventana_ignora_limpieza),
        ("M08 capacidad efectiva sin tope (factores > 1 aceptados)", "capacidad_efectiva",
         lambda n, t, D, R, origen="sensibilidad", justificacion=None: n * t * D * R),
        ("M09 capacidad publicada aceptada como diseño", "capacidad_teorica_equipo",
         lambda n, h, origen: n * h),
    ]
    detectadas = 0
    for nombre, clave, fn in mutaciones:
        g[clave] = fn
        try:
            fallas = [n for n, ok, _ in ejecutar_tests(verbose=False) if not ok]
        except Exception as e:  # noqa: BLE001
            fallas = [f"excepción: {e}"]
        finally:
            g[clave] = orig[clave]
        detectadas += bool(fallas)
        print(f"  {'DETECTADA' if fallas else 'NO DETECTADA'} {nombre}: {', '.join(x.split()[0] for x in fallas)}")
    print(f"  {detectadas}/{len(mutaciones)} mutaciones detectadas")
    return detectadas == len(mutaciones)


# ---------------------------------------------------------------------------
# 7. SALIDAS
# ---------------------------------------------------------------------------
def escribir_csv(t, ruta=CSV_SALIDA):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for fila in t.filas:
            x = dict(fila)
            if isinstance(x["valor"], float):
                x["valor"] = f"{x['valor']:.6f}".rstrip("0").rstrip(".")
            w.writerow(x)
    return len(t.filas)


def fmt(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir(t):
    print("\n## Ritmo operativo y nominal requerido (aves/h) — factores = SENSIBILIDAD")
    print("| Escala | h netas | Operativo | Nominal h netas (R 0,95 · 0,89 · 0,82) | Nominal si h incluye paradas (η 0,90 · 0,80 · 0,70) |")
    print("|---|---|---|---|---|")
    for E in ESCALAS:
        for h in HORAS_NETAS:
            q = lambda **k: t.q(escala_aves_dia=E, horas_netas=h, **k)  # noqa: E731
            a = " · ".join(fmt(q(bloque="ritmo_nominal", parametro=f"sensibilidad={n}",
                                 variable="ritmo_nominal_requerido_h_netas")) for n in ("alta", "media", "baja"))
            b = " · ".join(fmt(q(bloque="ritmo_nominal", parametro=f"sensibilidad={n}",
                                 variable="ritmo_nominal_requerido_h_programadas")) for n in ("alta", "media", "baja"))
            print(f"| {fmt(E)} | {h} | {fmt(q(bloque='ritmo', variable='ritmo_operativo_requerido'))} | {a} | {b} |")
    print("\n## Aves/día de una línea nominal L con h horas PROGRAMADAS (η alta · media · baja)")
    for L in LINEAS_NOMINALES:
        print(f"- L {fmt(L)}: " + " | ".join(
            f"{h} h: " + " · ".join(fmt(t.q(bloque="linea_nominal", horas_netas=h,
                                            parametro=f"linea={L};sensibilidad={n}",
                                            variable="aves_dia_con_h_programadas")) for n in ("alta", "media", "baja"))
            for h in HORAS_NETAS))
    print("\n## Ecuación de 24 h (h/día) por escenario de calendario")
    for esc in VENTANAS:
        print(f"\n### {esc}")
        print("| h netas | " + " | ".join(COMPONENTES_24H[1:]) + " | total | holgura | alerta |")
        print("|---|" + "---|" * (len(COMPONENTES_24H) + 2))
        for h in HORAS_NETAS:
            w = ventana_24h(h, esc)
            print(f"| {h} | " + " | ".join(fmt(w['componentes'][c], 2) for c in COMPONENTES_24H[1:]) +
                  f" | {fmt(w['total'], 1)} | {fmt(w['holgura'], 1)} | {'ALERTA' if w['alerta'] else '—'} |")
        print(f"Horas netas máximas con holgura ≥ 0: {fmt(horas_netas_max_24h(esc), 2)}")
    print("\n## Flujos por hora neta a 8 h (config. B; kg/h)")
    for v in ["peso_vivo", "carcasa_pre_chiller", "a_trozado", "comestible_a_empaque", "sangre_recuperada",
              "plumas_humedas", "visceras_no_comestibles"]:
        print(f"- {v}: " + " · ".join(fmt(t.q(bloque="flujo_hora", escala_aves_dia=E, horas_netas=8,
                                               parametro="config=B", variable=f"{v}_kg_h")) for E in ESCALAS))
    print("\n## Puestos manuales equivalentes a 8 h (referencia · prudente): colgado | eviscerado")
    for E in ESCALAS:
        c = [f"{t.q(bloque='puestos_manuales', escala_aves_dia=E, horas_netas=8, parametro=f'{op};referencia', variable='puestos_equivalentes')}"  # noqa: E501
             f" · {t.q(bloque='puestos_manuales', escala_aves_dia=E, horas_netas=8, parametro=f'{op};prudente', variable='puestos_equivalentes')}"  # noqa: E501
             for op in PRODUCTIVIDAD]
        print(f"- {fmt(E)}: {c[0]} | {c[1]}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    a = ap.parse_args()
    print(f"modelo_capacidad_proceso.py v{VERSION} ({FECHA})")
    res = ejecutar_tests()
    if not all(ok for _, ok, _ in res):
        sys.exit(1)
    if a.mutaciones:
        sys.exit(0 if prueba_mutaciones() else 1)
    if a.solo_tests:
        return
    t = construir()
    n = escribir_csv(t)
    print(f"CSV: {os.path.relpath(CSV_SALIDA, RAIZ)} ({n} filas)")
    imprimir(t)


if __name__ == "__main__":
    main()
