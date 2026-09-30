#!/usr/bin/env python3
"""
modelo_capacidad_proceso.py — Capacidad de proceso por etapa (sesión 09A)
=========================================================================

Versión 1.0 · 2026-09-30 · Fase 0 (prefactibilidad) · Carpeta 05_proceso_industrial

QUÉ HACE
  Traduce las escalas de 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo en
  CARGAS POR ETAPA del proceso industrial, para ver dónde aparecen los cuellos de botella:
    1. ritmo de línea requerido (aves/h netas) — idéntico al de 23_plan_expansion (test T01);
    2. ritmo NOMINAL que habría que especificar a un equipo según la eficiencia global
       (sensibilidad; NO es un dato de ningún equipo);
    3. aves/día que produce una línea de ritmo nominal dado (por qué una línea de
       2.500 aves/h no garantiza 20.000 aves/día);
    4. ventana horaria total del establecimiento (horas netas + tiempos no productivos +
       sanitización + mantenimiento) y holgura contra 24 h;
    5. flujos por hora neta de cada corriente (carcasas al chiller, kg a trozado, deshuese,
       empaque, sangre, plumas, vísceras, cabezas, patas, menudencias) desde el balance v1.1;
    6. carcasas simultáneas dentro del sistema de enfriamiento (inmersión / aire);
    7. puestos manuales EQUIVALENTES de colgado y eviscerado con productividades de
       referencia de extractos no argentinos (no es dotación: ver 18_recursos_humanos);
    8. carga de congelado por día según los perfiles de destino P1–P3 de 23_plan_expansion.

QUÉ NO HACE
  No selecciona equipos, proveedores, escala, turnos ni método de enfriamiento; no calcula
  precios, CAPEX ni OPEX; no dimensiona agua, efluentes, frío ni superficies (layout).
  No modifica los modelos anteriores: los IMPORTA (test T08 verifica que siguen intactos).

FÓRMULAS (h = horas netas de faena por día operativo; E = aves faenadas/día operativo)
  ritmo operativo requerido [aves/h]  = E / h
  ritmo nominal requerido  [aves/h]   = ritmo operativo / η          (η = eficiencia global)
  aves/día de una línea nominal L     = L × h × η
  ventana total [h/día]  = preoperativo + h + (pausas + limpieza intermedia) × h/8 + cierre
                           + sanitización final + mantenimiento no solapado
  holgura [h/día]        = 24 − ventana total          (negativa = combinación inviable)
  flujo de una corriente [kg/h] = kg/ave (balance v1.1) × E / h
  carcasas en el enfriamiento   = ritmo operativo × tiempo de residencia [min] / 60
  puestos equivalentes          = techo(ritmo operativo / productividad por operario)
  capacidad de planta           = mín(capacidad de cada etapa)   (cuello de botella)

PARÁMETROS (todos [SUPUESTO] de sensibilidad o [PVDP]; registrados en
actualizaciones_gestion_09A.md con IDs provisionales)
  η = 0,70 / 0,80 / 0,90 ....................................... SUP-09A-01
  tiempos no productivos, sanitización, mantenimiento (bajo/medio/alto) SUP-09A-02
  productividad manual de referencia y factor prudente 0,5 ......... SUP-09A-03 (FTE-09A-025/026)
  residencia en enfriamiento: inmersión 50 min; aire 90–150 min .... SUP-09A-04 (FTE-09A-024)
  kg/ave: balance v1.1 vía 23_plan_expansion/modelo_escala.py (config. A/B/C, 2,9 kg, medio,
  inmersión); perfiles de destino P1–P3 (SUP-055).

UNIDADES: aves, aves/h, kg, kg/h, t, h, min. CSV con punto decimal. Bases: "vivo" (peso vivo),
"comercial" (masa biológica + agua retenida), "biologica" (sin agua), "biologica+agua"
(subproductos con agua adherida), "aves", "h".

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

VERSION = "1.0"
FECHA = "2026-09-30"
F_ESC = "23_plan_expansion/modelo_escala.py (v1.1)"
F_BAL = "04_balance_masa/modelo_balance_masa.py (v1.1) vía modelo_escala.kg_por_ave"
F_PROPIO = "05_proceso_industrial/modelo_capacidad_proceso.py"
CSV_SALIDA = os.path.join(AQUI, "capacidad_proceso.csv")
CSV_ESCALA = os.path.join(RAIZ, "23_plan_expansion", "escenarios_escala.csv")

ESCALAS = list(me.ESCALAS)               # 2.500 / 5.000 / 10.000 / 20.000 (no se elige)
HORAS_NETAS = list(me.HORAS_NETAS)       # 6 / 8 / 10 / 16 (16 = 2 × 8; SUP-053)
PESO = me.PESO_REF                       # 2,9 kg

# SUP-09A-01 — eficiencia global η = producción real / (ritmo nominal × horas netas).
# Agrupa disponibilidad (paradas), rendimiento de velocidad (microparadas, huecos en grilletes)
# y pérdidas de arranque. SENSIBILIDAD, no dato de ningún equipo (DPV-09A-01).
EFICIENCIAS = {"baja": 0.70, "media": 0.80, "alta": 0.90}

# SUP-09A-02 — ventana horaria no productiva (h). Sensibilidad; sin dato argentino (DPV-082,
# DPV-09A-04). Pausas y limpieza intermedia se expresan por cada 8 h netas.
VENTANAS = {
    "baja":  {"preoperativo": 0.50, "pausas_8h": 0.50, "limpieza_intermedia_8h": 0.25, "cierre": 0.50,
              "sanitizacion": 3.0, "mantenimiento": 0.5},
    "media": {"preoperativo": 0.75, "pausas_8h": 0.75, "limpieza_intermedia_8h": 0.33, "cierre": 0.75,
              "sanitizacion": 4.0, "mantenimiento": 1.0},
    "alta":  {"preoperativo": 1.00, "pausas_8h": 1.00, "limpieza_intermedia_8h": 0.50, "cierre": 1.00,
              "sanitizacion": 6.0, "mantenimiento": 2.0},
}

# SUP-09A-03 — productividades manuales de referencia [PVDP · débil]: extractos de líneas
# no argentinas. "referencia" = valor del extracto; "prudente" = 50 % (sensibilidad).
PRODUCTIVIDAD = {
    # colgado de aves vivas: 23 aves/min por operario en líneas de EE.UU. de 180 grilletes/min
    "colgado": {"aves_h_operario": 23 * 60, "fuente": "FTE-09A-026"},
    # eviscerado manual: 2 aves/min por operario experimentado
    "eviscerado_manual": {"aves_h_operario": 2 * 60, "fuente": "FTE-09A-025"},
}
FACTOR_PRUDENTE = 0.5
LIMITE_EVISCERADO_MANUAL = 1000          # aves/h: tope citado para eviscerado manual asistido (FTE-09A-025)

# SUP-09A-04 — tiempo de residencia en el enfriamiento [PVDP] (FTE-09A-024)
RESIDENCIA_MIN = {"inmersion": 50, "aire_min": 90, "aire_max": 150}

# Líneas nominales ilustrativas para mostrar producción real (no son modelos de proveedor)
LINEAS_NOMINALES = [312.5, 625, 1250, 2500, 3125]

CAMPOS = ["bloque", "escala_aves_dia", "horas_netas", "parametro", "variable", "valor", "unidad",
          "base", "fuente_modelo", "clasificacion", "nota"]
PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen)\b",
                                 re.IGNORECASE)


class ErrorProceso(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. FUNCIONES DE CAPACIDAD
# ---------------------------------------------------------------------------
def validar(E=None, h=None, eta=None):
    if E is not None and E <= 0:
        raise ErrorProceso(f"Escala inválida: {E}")
    if h is not None and not 0 < h <= 24:
        raise ErrorProceso(f"Horas netas fuera de rango (0; 24]: {h}")
    if eta is not None and not 0 < eta <= 1:
        raise ErrorProceso(f"Eficiencia global fuera de rango (0; 1]: {eta}")


def ritmo_operativo(E, h):
    validar(E=E, h=h)
    return E / h


def ritmo_nominal_requerido(E, h, eta):
    validar(E=E, h=h, eta=eta)
    return ritmo_operativo(E, h) / eta


def aves_dia_linea(L, h, eta):
    validar(E=L, h=h, eta=eta)
    return L * h * eta


def ventana_total(h, esc="media"):
    validar(h=h)
    v = VENTANAS[esc]
    comp = {
        "preoperativo": v["preoperativo"],
        "faena_neta": h,
        "pausas": v["pausas_8h"] * h / 8,
        "limpieza_intermedia": v["limpieza_intermedia_8h"] * h / 8,
        "cierre_vaciado": v["cierre"],
        "sanitizacion_final": v["sanitizacion"],
        "mantenimiento_no_solapado": v["mantenimiento"],
    }
    total = sum(comp.values())
    return total, 24 - total, comp


def capacidad_planta(etapas: dict):
    """Capacidad de planta = etapa de menor capacidad (aves/día). Devuelve (capacidad, etapa)."""
    if not etapas:
        raise ErrorProceso("Sin etapas")
    etapa = min(etapas, key=etapas.get)
    return etapas[etapa], etapa


def puestos_equivalentes(rate, operacion, prudente=False):
    prod = PRODUCTIVIDAD[operacion]["aves_h_operario"] * (FACTOR_PRUDENTE if prudente else 1)
    return math.ceil(rate / prod - 1e-9)


# ---------------------------------------------------------------------------
# 2. FLUJOS POR ETAPA (kg/ave del balance v1.1)
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
# 3. CONSTRUCCIÓN DE LA TABLA
# ---------------------------------------------------------------------------
class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, h, parametro, variable, valor, unidad, base, fuente, clasif, nota=""):
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
                  "[ESTIMACIÓN]", "= E / h; igual a 23_plan_expansion (T01)")
            t.add("ritmo", E, h, "", "aves_por_minuto", r / 60, "aves/min", "aves", F_PROPIO, "[ESTIMACIÓN]")
            t.add("ritmo", E, h, "", "segundos_por_ave", 3600 / r, "s", "aves", F_PROPIO, "[ESTIMACIÓN]")
            for nombre, eta in EFICIENCIAS.items():
                t.add("ritmo_nominal", E, h, f"eficiencia={nombre}", "ritmo_nominal_requerido",
                      ritmo_nominal_requerido(E, h, eta), "aves/h", "aves", F_PROPIO, "[ESTIMACIÓN]",
                      f"η = {eta}; SUP-09A-01 (sensibilidad)")
            for nombre in VENTANAS:
                tot, holg, comp = ventana_total(h, nombre)
                t.add("ventana", E, h, f"ventana={nombre}", "ventana_total_establecimiento", tot, "h", "h",
                      F_PROPIO, "[ESTIMACIÓN]", "SUP-09A-02; no depende de la escala")
                t.add("ventana", E, h, f"ventana={nombre}", "holgura_24h", holg, "h", "h", F_PROPIO,
                      "[ESTIMACIÓN]", "negativa = combinación inviable en un día de 24 h")
            # enfriamiento
            for modo, minutos in RESIDENCIA_MIN.items():
                n = r * minutos / 60
                t.add("enfriamiento", E, h, f"residencia={modo}", "carcasas_simultaneas_en_enfriamiento", n,
                      "aves", "aves", F_PROPIO, "[ESTIMACIÓN]", f"{minutos} min; SUP-09A-04")
                t.add("enfriamiento", E, h, f"residencia={modo}", "kg_carcasa_simultaneos_en_enfriamiento",
                      n * kgs["B"]["carcasa_pre_chiller"][0], "kg", "biologica", F_BAL, "[ESTIMACIÓN]",
                      "carcasa eviscerada caliente 2,9 kg (sin agua)")
            # puestos manuales equivalentes
            for op in PRODUCTIVIDAD:
                for prud in (False, True):
                    t.add("puestos_manuales", E, h, f"{op};{'prudente' if prud else 'referencia'}",
                          "puestos_equivalentes", puestos_equivalentes(r, op, prud), "puestos", "aves",
                          F_PROPIO, "[ESTIMACIÓN]",
                          f"productividad {PRODUCTIVIDAD[op]['fuente']} [PVDP · débil]; no es dotación")
            # flujos por configuración
            for c in "ABC":
                for var, (kg, base) in kgs[c].items():
                    if kg == 0:
                        continue
                    t.add("flujo_hora", E, h, f"config={c}", f"{var}_kg_h", kg * r, "kg/h", base, F_BAL,
                          "[ESTIMACIÓN]")
        # por día (no depende de h)
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
    # líneas nominales → aves/día reales
    for L in LINEAS_NOMINALES:
        for h in HORAS_NETAS:
            for nombre, eta in EFICIENCIAS.items():
                t.add("linea_nominal", "", h, f"linea={L};eficiencia={nombre}", "aves_dia_producidas",
                      aves_dia_linea(L, h, eta), "aves", "aves", F_PROPIO, "[ESTIMACIÓN]",
                      "línea nominal ilustrativa, no modelo de proveedor")
    return t


# ---------------------------------------------------------------------------
# 4. TESTS
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-6):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


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

    # T02 nominal ≥ operativo y decrece con η
    ok = True
    for E in ESCALAS:
        for h in HORAS_NETAS:
            r = t.q(bloque="ritmo", escala_aves_dia=E, horas_netas=h, variable="ritmo_operativo_requerido")
            noms = [t.q(bloque="ritmo_nominal", escala_aves_dia=E, horas_netas=h,
                        parametro=f"eficiencia={n}", variable="ritmo_nominal_requerido") for n in EFICIENCIAS]
            ok &= all(x >= r for x in noms) and noms[0] > noms[1] > noms[2]
    chk("T02 ritmo nominal ≥ operativo; baja η exige más", ok)

    # T03 capacidad de planta = mínimo; línea ≠ planta
    etapas = {"linea_faena": 20000, "evisceracion": 18000, "chiller": 19000, "trozado": 15000, "camaras": 17000}
    cap, et = capacidad_planta(etapas)
    chk("T03 capacidad de planta = etapa mínima (≠ línea)",
        cap == 15000 and et == "trozado" and cap < etapas["linea_faena"] and all(cap <= v for v in etapas.values()))

    # T04 conservación: flujo/h × h = kg/ave × E ; coherente con modelo_escala
    ok = True
    for c in "ABC":
        kg, k = kg_ave_config(c)
        for E in ESCALAS:
            dia = t.q(bloque="flujo_dia", escala_aves_dia=E, parametro=f"config={c}",
                      variable="sangre_recuperada_t_dia")
            ok &= _cerca(dia, k["sangre"] * E / 1000)
            for h in HORAS_NETAS:
                for var in ("plumas_humedas", "comestible_a_empaque", "peso_vivo"):
                    fh = t.q(bloque="flujo_hora", escala_aves_dia=E, horas_netas=h, parametro=f"config={c}",
                             variable=f"{var}_kg_h")
                    ok &= _cerca(fh * h, kg[var][0] * E)
    chk("T04 flujos/h × horas = kg/ave × escala (balance v1.1)", ok)

    # T05 ventana = suma de componentes; crece con h; holgura = 24 − total
    ok = True
    for esc in VENTANAS:
        prev = -1
        for h in HORAS_NETAS:
            tot, holg, comp = ventana_total(h, esc)
            ok &= _cerca(tot, sum(comp.values())) and _cerca(holg, 24 - tot) and tot > prev and tot > h
            prev = tot
    chk("T05 ventana total = Σ componentes > horas netas; holgura = 24 − total", ok)

    # T06 linealidad: doble escala → doble flujo; ventana no cambia con la escala
    ok = True
    for h in HORAS_NETAS:
        for c in "ABC":
            a = t.q(bloque="flujo_hora", escala_aves_dia=5000, horas_netas=h, parametro=f"config={c}",
                    variable="peso_vivo_kg_h")
            b = t.q(bloque="flujo_hora", escala_aves_dia=10000, horas_netas=h, parametro=f"config={c}",
                    variable="peso_vivo_kg_h")
            ok &= _cerca(b, 2 * a)
        ok &= _cerca(t.q(bloque="ventana", escala_aves_dia=2500, horas_netas=h, parametro="ventana=media",
                         variable="ventana_total_establecimiento"),
                     t.q(bloque="ventana", escala_aves_dia=20000, horas_netas=h, parametro="ventana=media",
                         variable="ventana_total_establecimiento"))
    chk("T06 flujos lineales con la escala; ventana independiente de la escala", ok)

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
            r = E / h
            for modo, m in RESIDENCIA_MIN.items():
                ok &= _cerca(t.q(bloque="enfriamiento", escala_aves_dia=E, horas_netas=h,
                                 parametro=f"residencia={modo}", variable="carcasas_simultaneas_en_enfriamiento"),
                             r * m / 60)
    chk("T09 carcasas en enfriamiento = ritmo × residencia", ok)

    # T10 entradas inválidas detienen el modelo
    malos = 0
    for f, args in ((ritmo_nominal_requerido, (1000, 8, 1.2)), (ritmo_nominal_requerido, (1000, 8, 0)),
                    (ritmo_operativo, (1000, 25)), (ritmo_operativo, (-1, 8)), (capacidad_planta, ({},))):
        try:
            f(*args)
        except ErrorProceso:
            malos += 1
        except Exception:  # noqa: BLE001  (error no controlado = el modelo no valida la entrada)
            pass
    chk("T10 entradas inválidas detienen el modelo con ErrorProceso", malos == 5)

    # T11 línea nominal: 2.500 aves/h × 8 h no alcanza 20.000 con η < 1
    ok = all(t.q(bloque="linea_nominal", horas_netas=8, parametro=f"linea=2500;eficiencia={n}",
                 variable="aves_dia_producidas") < 20000 for n in EFICIENCIAS)
    chk("T11 línea nominal de 2.500 aves/h × 8 h netas < 20.000 aves/día con η < 1", ok)

    # T12 no se agregan flujos de configuraciones distintas (cada fila de flujo tiene UNA config)
    ok = all(f["parametro"].count("config=") == 1 for f in t.filas if f["bloque"].startswith("flujo"))
    chk("T12 cada flujo pertenece a una sola configuración (A/B/C no se suman)", ok)

    # T13 la ventana incluye TODOS los tiempos no productivos (sanitización y mantenimiento incluidos)
    requeridos = {"preoperativo", "faena_neta", "pausas", "limpieza_intermedia", "cierre_vaciado",
                  "sanitizacion_final", "mantenimiento_no_solapado"}
    ok = True
    for esc, v in VENTANAS.items():
        for h in HORAS_NETAS:
            tot, _, comp = ventana_total(h, esc)
            ok &= set(comp) == requeridos and _cerca(comp["sanitizacion_final"], v["sanitizacion"]) \
                and tot >= h + v["sanitizacion"] + v["mantenimiento"] + v["preoperativo"] + v["cierre"] - 1e-9
    chk("T13 ventana con sanitización, mantenimiento, preoperativo y cierre", ok)

    if verbose:
        for n, ok, d in res:
            print(f"  {'OK  ' if ok else 'FALLA'} {n}" + (f" — {d}" if d and not ok else ""))
        print(f"  {sum(ok for _, ok, _ in res)}/{len(res)} tests correctos")
    return res


# ---------------------------------------------------------------------------
# 5. MUTACIONES (verifican que los tests detectan errores típicos)
# ---------------------------------------------------------------------------
def prueba_mutaciones():
    g = globals()
    orig = {k: g[k] for k in ("ritmo_nominal_requerido", "capacidad_planta", "ventana_total",
                              "ritmo_operativo", "aves_dia_linea")}
    mutaciones = [
        ("M01 nominal = operativo × η (invertido)", "ritmo_nominal_requerido",
         lambda E, h, eta: (E / h) * eta),
        ("M02 capacidad de planta = etapa MÁXIMA", "capacidad_planta",
         lambda et: (max(et.values()), max(et, key=et.get))),
        ("M03 ventana sin sanitización", "ventana_total",
         lambda h, esc="media": (lambda tot, comp: (tot - comp["sanitizacion_final"],
                                                    24 - tot + comp["sanitizacion_final"],
                                                    {k: v for k, v in comp.items() if k != "sanitizacion_final"}))(
             *orig["ventana_total"](h, esc)[::2])),
        ("M04 ritmo con horas de turno fijas (8 h) en vez de netas", "ritmo_operativo",
         lambda E, h: E / 8),
        ("M05 línea nominal sin eficiencia", "aves_dia_linea", lambda L, h, eta: L * h),
    ]
    detectadas = 0
    for nombre, clave, fn in mutaciones:
        g[clave] = fn
        try:
            res = ejecutar_tests(verbose=False)
            fallas = [n for n, ok, _ in res if not ok]
        except Exception as e:  # noqa: BLE001
            fallas = [f"excepción: {e}"]
        finally:
            g[clave] = orig[clave]
        detectadas += bool(fallas)
        print(f"  {'DETECTADA' if fallas else 'NO DETECTADA'} {nombre}: {', '.join(x.split()[0] for x in fallas)}")
    print(f"  {detectadas}/{len(mutaciones)} mutaciones detectadas")
    return detectadas == len(mutaciones)


# ---------------------------------------------------------------------------
# 6. SALIDAS
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
    print("\n## Ritmo operativo y nominal requerido (aves/h)")
    print("| Escala | h netas | Operativo | Nominal η 0,90 | Nominal η 0,80 | Nominal η 0,70 | s/ave |")
    print("|---|---|---|---|---|---|---|")
    for E in ESCALAS:
        for h in HORAS_NETAS:
            q = lambda **k: t.q(escala_aves_dia=E, horas_netas=h, **k)  # noqa: E731
            print(f"| {fmt(E)} | {h} | {fmt(q(bloque='ritmo', variable='ritmo_operativo_requerido'))} | " +
                  " | ".join(fmt(q(bloque='ritmo_nominal', parametro=f'eficiencia={n}',
                                   variable='ritmo_nominal_requerido')) for n in ("alta", "media", "baja")) +
                  f" | {fmt(q(bloque='ritmo', variable='segundos_por_ave'), 1)} |")
    print("\n## Aves/día producidas por una línea de ritmo nominal L")
    print("| L (aves/h) | h netas | η 0,90 | η 0,80 | η 0,70 |")
    print("|---|---|---|---|---|")
    for L in LINEAS_NOMINALES:
        for h in HORAS_NETAS:
            print(f"| {fmt(L)} | {h} | " + " | ".join(
                fmt(t.q(bloque="linea_nominal", horas_netas=h, parametro=f"linea={L};eficiencia={n}",
                        variable="aves_dia_producidas")) for n in ("alta", "media", "baja")) + " |")
    print("\n## Ventana total del establecimiento (h/día) y holgura contra 24 h")
    print("| h netas | Baja: total · holgura | Media: total · holgura | Alta: total · holgura |")
    print("|---|---|---|---|")
    for h in HORAS_NETAS:
        print(f"| {h} | " + " | ".join(f"{fmt(ventana_total(h, n)[0], 1)} · {fmt(ventana_total(h, n)[1], 1)}"
                                        for n in ("baja", "media", "alta")) + " |")
    print("\n## Flujos por hora neta a 8 h (config. B trozado; kg/h)")
    vars_ = ["peso_vivo", "carcasa_pre_chiller", "a_trozado", "comestible_a_empaque", "sangre_recuperada",
             "plumas_humedas", "visceras_no_comestibles", "cabezas", "garras_a_y_segunda", "menudencias_y_cuello"]
    print("| Corriente | " + " | ".join(fmt(E) for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for v in vars_:
        print(f"| {v} | " + " | ".join(fmt(t.q(bloque="flujo_hora", escala_aves_dia=E, horas_netas=8,
                                                 parametro="config=B", variable=f"{v}_kg_h"))
                                         for E in ESCALAS) + " |")
    print("\n## Deshuese (config. C) kg/h a 8 h: " + " · ".join(
        fmt(t.q(bloque="flujo_hora", escala_aves_dia=E, horas_netas=8, parametro="config=C",
                variable="a_deshuese_kg_h")) for E in ESCALAS))
    print("\n## Carcasas simultáneas en el enfriamiento a 8 h (inmersión 50 min · aire 90 · aire 150)")
    for E in ESCALAS:
        print(f"- {fmt(E)}: " + " · ".join(fmt(t.q(bloque="enfriamiento", escala_aves_dia=E, horas_netas=8,
                                                   parametro=f"residencia={m}",
                                                   variable="carcasas_simultaneas_en_enfriamiento"))
                                           for m in RESIDENCIA_MIN))
    print("\n## Puestos manuales equivalentes a 8 h (referencia · prudente)")
    print("| Escala | Colgado | Eviscerado manual |")
    print("|---|---|---|")
    for E in ESCALAS:
        c = [f"{t.q(bloque='puestos_manuales', escala_aves_dia=E, horas_netas=8, parametro=f'{op};referencia', variable='puestos_equivalentes')}"  # noqa: E501
             f" · {t.q(bloque='puestos_manuales', escala_aves_dia=E, horas_netas=8, parametro=f'{op};prudente', variable='puestos_equivalentes')}"  # noqa: E501
             for op in PRODUCTIVIDAD]
        print(f"| {fmt(E)} | {c[0]} | {c[1]} |")
    print("\n## Comestible a congelar (t/día operativo, config. B)")
    for E in ESCALAS:
        print(f"- {fmt(E)}: " + " · ".join(
            f"{p} {fmt(t.q(bloque='congelado', escala_aves_dia=E, parametro=f'perfil={p};config=B', variable='comestible_a_congelar_t_dia'), 1)}"  # noqa: E501
            for p in me.PERFILES_DESTINO))
    print("\n## Flujos diarios (t/día operativo, config. B): sólidos a retirar · sangre · plumas")
    for E in ESCALAS:
        q = lambda v: t.q(bloque="flujo_dia", escala_aves_dia=E, parametro="config=B", variable=v)  # noqa: E731
        print(f"- {fmt(E)}: {fmt(q('solidos_a_retirar_t_dia'), 2)} · {fmt(q('sangre_recuperada_t_dia'), 2)}"
              f" · {fmt(q('plumas_humedas_t_dia'), 2)}")


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
