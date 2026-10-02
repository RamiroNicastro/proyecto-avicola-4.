"""
Modelo físico del UPSTREAM avícola (sesión 14B): pollitos BB, incubación, alimento balanceado,
almacenamiento e inventarios, sincronización granja–faena, abastecimiento de granjas y
necesidades logísticas, por escala.

Genera `escenarios_upstream.csv`, ejecuta las pruebas automáticas y, con `--tablas`, imprime las
tablas usadas en los .md de `14_alimento_balanceado/` y `15_incubacion/`.

    python3 modelo_upstream.py            # CSV + pruebas
    python3 modelo_upstream.py --tablas   # además, tablas para los documentos

ESTADO: ESCENARIOS de orden de magnitud (Fase 0). NO es diseño, NO elige fabricante, NO decide
integración, NO fija capacidad de faena (regla 9) y NO contiene precios ni costos (sin CAPEX/OPEX).
Las escalas 2.500 / 5.000 / 10.000 / 20.000 aves FAENADAS por día de faena son las mismas
escalas hipotéticas de 03 y 23 (no son la escala del proyecto).

Versión 1.1 · 2026-10-01 (auditoría de sincronización productiva e inventarios)
  - recepción de huevo, carga (setting) y nacimiento como eventos distintos; lead time
    recepción → pollito entregado separado del período de incubación (21 d en el modelo);
  - setter y hatcher dimensionados por separado, con CADENCIA de cargas/nacimientos simulada
    (las "posiciones de incubadora" de v1.0 eran solo setter en flujo continuo × margen);
  - tamaño de lote de nacimiento ≠ demanda media semanal;
  - granja ≠ galpón; chequeo conceptual de sincronización nacimiento–colocación–faena;
  - elasticidades de fertilidad e incubabilidad;
  - inventarios de alimento por categoría y por propiedad (propio / en tercero / cadena);
  - opciones make-or-buy como escenarios de comparación (sin "caso base"); fases como
    arquitecturas de referencia sin orden obligatorio.
IDs definitivos de los registros centrales (00_gestion_proyecto/, 25_fuentes/); mapa de IDs
provisionales 14B → definitivos en 00_gestion_proyecto/reconciliacion_sesiones_14.md (2026-10-02).

------------------------------------------------------------------------------------------------
ORIGEN DE LOS DATOS
------------------------------------------------------------------------------------------------
Producción primaria: se IMPORTA 03_produccion_primaria/modelo_escenarios_produccion.py (v1.1) y
se usa `mp.calcular` sin recalcular nada. Perfil MEDIO (47 d, 2,9 kg) y desempeño favorable /
medio / desfavorable (SUP-026 a SUP-028).

Unidades: aves, pollitos, huevos (unidades); kg; t = 1.000 kg; m³; h; d; semanas (52,14/año).
Separador decimal del CSV: punto. Bases (regla 14): pollitos = pollitos BB ALOJADOS en granja;
huevos = huevos fértiles (incubables) en unidades; alimento = alimento terminado entregado a
granja (base del FCR de campo de 03); materias primas = t de ingrediente tal cual.

------------------------------------------------------------------------------------------------
1. POLLITOS BB (demanda; viene de 03)
------------------------------------------------------------------------------------------------
  margen_mortalidad_pollitos = pollitos_alojados − aves_faenadas   (granja + transporte)
  pollitos_a_recibir         = pollitos_alojados × (1 + margen_pedido)   (SUP-142; base 0)

------------------------------------------------------------------------------------------------
2. CADENA TEMPORAL (día 0 = CARGA / SETTING)
------------------------------------------------------------------------------------------------
  recepción del huevo    = −días_almacenamiento                (SUP-145: 3 / 5 / 7)
  carga (setting)        = 0
  transferencia          = D_SETTER (18)
  nacimiento             = D_SETTER + D_HATCHER (21)          → período de incubación (setting→nacimiento)
  selección/vacunación/expedición/llegada a granja = nacimiento + horas PENDIENTES (DPV-047)
  colocación             = llegada a granja
  retiro (carga de aves) = colocación + edad de faena (03)
  faena                  = retiro + ventana prefaena (13: 10 h de escenario)
  lead_time_recepcion_a_entrega = días_almacenamiento + 21 + expedición(PENDIENTE) — NO es incubación

------------------------------------------------------------------------------------------------
3. INCUBACIÓN (cálculo inverso) — SETTER Y HATCHER POR SEPARADO
------------------------------------------------------------------------------------------------
  pollitos_nacidos       = vendibles / (1 − descarte)
  huevos_cargados        = nacidos / (fertilidad × incubabilidad_fértiles × (1 − pérdida_transferencia))
  huevos_transferidos    = cargados × (1 − pérdida_transferencia) × (fertilidad si ovoscopia, si no 1)
  huevos_recibidos       = cargados / (1 − pérdida_recepción_almacén)
  Flujo continuo (ley de Little; ocupación MEDIA, sin margen):
    setter_continuo  = cargados_sem   × (D_SETTER + limpieza_setter) / 7
    hatcher_continuo = transferidos_sem × (D_HATCHER + limpieza_hatcher) / 7
  Con CADENCIA (N cargas = N nacimientos por semana, días de la semana dados; lotes iguales):
    lote_carga = cargados_sem / N ; lote_nacimiento = vendibles_sem / N
    posiciones_X_cadencia = ocupación MÁXIMA simulada en régimen (varias semanas)
    posiciones_X_diseño   = posiciones_X_cadencia × (1 + margen)          (SUP-146)
  huevos_en_proceso (WIP) = setter_continuo_sin_limpieza + hatcher_continuo_sin_limpieza
  Setter y hatcher NO se suman como "capacidad": son máquinas/etapas distintas; la suma de
  posiciones solo se informa como posiciones físicas instaladas.

------------------------------------------------------------------------------------------------
4. SINCRONIZACIÓN (granja ≠ galpón)
------------------------------------------------------------------------------------------------
  unidad de colocación   = "galpon" (plazas = pollitos/m² de 03 × m² de galpón SUP-031) o
                           "granja" (plazas de granja: barrido de 13; o galpones × plazas)
  colocaciones/semana    = pollitos_sem / plazas_unidad
  lotes_simultaneos      = colocaciones/semana × edad / 7          (unidades con aves)
  unidades_requeridas    = capacidad_alojamiento (03) / plazas_unidad
  nacimientos_por_colocacion = plazas_unidad / lote_nacimiento     (>1 ⇒ edades mezcladas)
  dias_faena_por_unidad  = plazas × (1−m)(1−DOA) / aves_faenadas_dia
  Chequeos (no optimiza): llenado multi-nacimiento (tolerancia de edad PENDIENTE) y cosecha de
  una unidad > DIAS_COSECHA_REFERENCIA días de faena (03/13: 1–2 noches, [ESTIMACIÓN]).

------------------------------------------------------------------------------------------------
5-8. ALIMENTO, PLANTA, SILOS E INVENTARIOS
------------------------------------------------------------------------------------------------
  t_h_requerida = t_semana_plena × factor_pico / (días_op × horas × eficiencia) × (1 + margen)
  horas_produccion_semana(C) = t_semana / (C × eficiencia)     (planta de capacidad C dada)
  inventario por CATEGORÍA (alimento terminado en granja / en planta, maíz, soja, micros-aceite-
  otros, material en proceso): t = consumo diario de la categoría × días de stock (SUPUESTOS);
  cada categoría tiene PROPIETARIO y UBICACIÓN según la arquitectura; stock de la cadena =
  propio + en tercero (referencial con los mismos días), por categoría — nunca se suman
  categorías distintas.

------------------------------------------------------------------------------------------------
9-10. MAKE OR BUY Y ARQUITECTURAS DE REFERENCIA
------------------------------------------------------------------------------------------------
  Todas las opciones son ESCENARIOS DE COMPARACIÓN con el mismo estatus; "compra" es solo el
  BENCHMARK de comparación (punto contra el que se miden las demás), no una preferencia.
  Fases 0 / 1 / 2 / 3 / futura = arquitecturas de madurez de referencia, sin orden obligatorio.
"""

from __future__ import annotations

import csv
import math
import os
import re
import sys

sys.dont_write_bytecode = True           # no dejar __pycache__ en las carpetas de los modelos

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.environ.get("MODELO_UPSTREAM_RAIZ") or os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "03_produccion_primaria"))
import modelo_escenarios_produccion as mp  # noqa: E402  (producción primaria v1.1)

VERSION = "1.1"
FECHA = "2026-10-01"
FUENTE = "14_alimento_balanceado/modelo_upstream.py"
TOL = 1e-9
SEMANAS_ANIO = mp.SEMANAS_ANIO

# ------------------------------------------------------------------------------------------------
# 1. PARÁMETROS (importados cuando existen; propios con ID central SUP-142 a SUP-154)
# ------------------------------------------------------------------------------------------------
ESCALAS = list(mp.PLANTAS_AVES_FAENADAS_DIA)       # 2.500 / 5.000 / 10.000 / 20.000 (escenarios)
CALENDARIOS = dict(mp.DIAS_FAENA_ANIO)             # {5: 250, 6: 300} (SUP-025)
PERFIL = "medio"                                   # 47 d, 2,9 kg (SUP-027)
NIVELES = tuple(mp.DESEMPENO)                      # favorable / medio / desfavorable (SUP-026)

# Pollitos
MARGEN_PEDIDO_BASE = 0.0                           # SUP-142: valor de parámetro (no opción)
MARGEN_PEDIDO_BARRIDO = (0.0, 0.01, 0.02)          # SUP-142: barrido, sin fuente
CAP_CAMION_POLLITOS = None                         # PENDIENTE (DPV-047, DPV-084)
CAP_CAMION_POLLITOS_BARRIDO = (20000, 40000, 80000)  # SUP-096: barrido ilustrativo, NO capacidad

# Incubación: niveles de SUPUESTO (SUP-143 / 03). Referencia de PICO (FTE-305 [PVDP]):
# fertilidad ≥ 96,7 %, incubabilidad de fértiles 93,5 %; los promedios de vida del lote son menores.
INCUBACION = {
    "favorable":    {"fertilidad": 0.95, "hof": 0.92, "perdida_alm": 0.005, "perdida_tr": 0.003, "descarte": 0.005},
    "medio":        {"fertilidad": 0.92, "hof": 0.90, "perdida_alm": 0.010, "perdida_tr": 0.005, "descarte": 0.010},
    "desfavorable": {"fertilidad": 0.88, "hof": 0.87, "perdida_alm": 0.020, "perdida_tr": 0.010, "descarte": 0.020},
}
# Tiempos (SUP-145): 18 d setter + 3 d hatcher = 21 d de incubación (práctica general; transferencia
# e in ovo a 18-19 d citada, FTE-306 [PVDP]); limpieza por carga: sin fuente.
D_SETTER = 18.0
D_HATCHER = 3.0
D_LIMPIEZA_SETTER = 1.0
D_LIMPIEZA_HATCHER = 1.0
D_ALMACEN_HUEVO = (3, 5, 7)                        # barrido; óptimo 3-6 d citado (FTE-305 [PVDP])
D_ALMACEN_BASE = 5
H_NACIMIENTO_A_GRANJA = None                       # PENDIENTE: selección + vacunación + carga + viaje (DPV-047)
VENTANA_PREFAENA_H = 10.0                          # 13 (SUP-095): parámetro de escenario, no norma
OVOSCOPIA_RETIRA_INFERTILES = False                # base: no se retiran infértiles al transferir
MARGEN_CAPACIDAD = (0.10, 0.15, 0.20)              # SUP-146 (reserva de diseño, no óptimo)
MARGEN_CAPACIDAD_BASE = 0.15
# CADENCIA (SUP-147): cargas = nacimientos por semana y días de la semana (0 = lunes). Patrones
# ILUSTRATIVOS, no seleccionados; lotes iguales. La cadencia real la fija la incubadora (DPV-133).
CADENCIAS = {1: (0,), 2: (0, 3), 3: (0, 2, 4), 4: (0, 1, 3, 4), 5: (0, 1, 2, 3, 4)}
HORAS_VENTANA_PROCESO = (6, 10)                    # SUP-147: horas para seleccionar/vacunar/expedir un nacimiento
POLLITOS_REPRODUCTORA_SEMANA = 3.6                 # 03 §4.2 [ESTIMACIÓN], solo fase futura (DPV-045)

# Granjas y galpones (granja ≠ galpón)
PLAZAS_GRANJA = (15000, 30000, 60000)              # de 13 (PLAZAS_GRANJA; 03 [ESTIMACIÓN] 15-30 mil)
GALPON_M2 = tuple(mp.TAMANOS_GALPON_M2)            # 1.200 / 1.800 / 2.400 m² (SUP-031, ilustrativos)
GALPONES_POR_GRANJA = None                         # PENDIENTE: arquitectura real de las granjas (DPV-048)
TOLERANCIA_EDAD_COLOCACION_D = None                # PENDIENTE: diferencia de edad admisible en un mismo lote
DIAS_COSECHA_REFERENCIA = 2                        # 03 transporte_aves.md / 13: una granja "se vacía en 1-2 noches" [ESTIMACIÓN]
LOTE_PROVEEDOR_POLLITOS = None                     # PENDIENTE: tamaño de nacimiento del proveedor (opción A)

# Alimento: categorías de materias primas (fracción del alimento, rango de 03 alimentacion.md §4)
COMPOSICION = {   # categoría: (mín, máx, punto ilustrativo o None)
    "maiz":       (0.55, 0.65, 0.60),
    "harina_soja": (0.25, 0.35, 0.30),
    "aceite":     (0.01, 0.05, None),
    "minerales":  (0.023, 0.035, None),   # fosfatos 1-2 % + carbonato ~1 % + sal/bicarbonato 0,3-0,5 %
    "vitaminas":  (0.002, 0.005, None),   # premezcla vitamínico-mineral
    "otros":      (0.002, 0.013, None),   # aminoácidos 0,2-0,8 % + enzimas/aditivos < 0,5 %
}
FRACCION_MICROS = 1 - COMPOSICION["maiz"][2] - COMPOSICION["harina_soja"][2]   # 10 % agregado (SUP-032)

# Planta de alimento (SUP-148): parámetros operativos de ESCENARIO
DIAS_OPERACION_PLANTA = (3, 5, 6)
HORAS_DIA_PLANTA = (8, 16)
EFICIENCIA_PLANTA = (0.75, 0.85)
FACTOR_PICO_ALIMENTO = 1.0         # semana plena ya es el ritmo nominal; estacionalidad: PENDIENTE
N_TIPOS_ALIMENTO = (3, 4)          # inicio / crecimiento / terminación (+ retiro), 03 §3

# Silos e inventarios (SUP-149 / 10): densidades y días de stock = VARIABLES
DENSIDAD_T_M3 = {"maiz": (0.72,), "harina_soja": (0.56, 0.60, 0.67), "alimento": (0.55, 0.60, 0.65)}
FACTOR_LLENADO = 0.90
DIAS_STOCK = {                     # días calendario de consumo; SUPUESTOS hasta validación
    "maiz": (7, 15, 30),
    "harina_soja": (7, 15),
    "micros": (15, 30, 60),        # aceite + minerales + vitaminas + otros (SUP-150, v1.1)
    "alimento_planta": (1, 2, 3),
    "alimento_granja": (2, 3, 5),
}
DIAS_STOCK_BASE = {"maiz": 15, "harina_soja": 15, "micros": 30, "alimento_planta": 2, "alimento_granja": 3}
N_MP_GRANEL = (2, 3, 4)
VOLUMEN_UNITARIO_SILO_M3 = None    # PENDIENTE: no se inventa un silo estándar

# Logística (capacidades de ESCENARIO de SUP-096; sin elección explícita → PENDIENTE)
CAP_GRANELERO_T = 28.0
CAP_CAMION_GRANO_BARRIDO = (25.0, 28.0, 30.0)  # SUP-096
CAP_CAMION_HUEVOS = None           # PENDIENTE (DPV-047)

# Make or buy: TODAS las opciones son escenarios de comparación con el mismo estatus.
# "benchmark" = punto de comparación para medir diferencias; NO implica preferencia.
OPCIONES = {
    "pollito":  {"A_compra": "comparacion", "B_huevo_fertil": "comparacion", "C_reproductoras": "comparacion"},
    "alimento": {"A_compra": "comparacion", "B_facon": "comparacion", "C_planta_propia": "comparacion"},
    "granjas":  {"A_terceros": "comparacion", "B_integrados": "comparacion", "C_propias": "comparacion",
                 "B+C_mixto": "comparacion"},
}
BENCHMARK = {"pollito": "A_compra", "alimento": "A_compra", "granjas": "A_terceros"}

# Arquitecturas de madurez de REFERENCIA (SUP-152): sin orden obligatorio; una función puede
# integrarse antes si hay demanda, capital y ventaja económica (a demostrar en fase económica).
FASES = {
    "F0": {"nombre": "Arquitectura de referencia 0: pollito comprado + alimento comprado + granjas de terceros + faena a façon posible",
           "pollito": "A_compra", "alimento": "A_compra", "granjas": "A_terceros", "faena": "facon_posible"},
    "F1": {"nombre": "Arquitectura de referencia 1: planta de faena propia; upstream comprado o integrado parcialmente",
           "pollito": "A_compra", "alimento": "B_facon", "granjas": "B_integrados", "faena": "propia"},
    "F2": {"nombre": "Arquitectura de referencia 2: más granjas e integración",
           "pollito": "A_compra", "alimento": "B_facon", "granjas": "B_integrados+C_propias", "faena": "propia"},
    "F3": {"nombre": "Arquitectura de referencia 3: alimento y/o incubación propios",
           "pollito": "B_huevo_fertil", "alimento": "C_planta_propia", "granjas": "B_integrados+C_propias",
           "faena": "propia"},
    "FF": {"nombre": "Arquitectura de referencia futura: reproductoras / genética solo con justificación",
           "pollito": "C_reproductoras", "alimento": "C_planta_propia", "granjas": "B_integrados+C_propias",
           "faena": "propia"},
}
for _f in FASES.values():
    _f["orden_obligatorio"] = False
FASES_SIN_REPRODUCTORAS = ("F0", "F1")   # test U07

PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|precios|costo|costos|capex|opex|ebitda|van|tir|"
                                 r"payback|margen_bruto|ingreso|ingresos|rentabilidad)\b|\$", re.IGNORECASE)
PALABRAS_PREFERENCIA = re.compile(r"caso base|recomendad|preferid|ganador", re.IGNORECASE)
UNIDADES_VALIDAS = {"aves", "pollitos", "huevos", "posiciones", "reproductoras", "t", "t/h", "kg", "m³",
                    "m²", "ratio", "d", "h", "viajes", "colocaciones", "unidades", "lotes", "silos",
                    "pollitos/h", "indicador", "nacimientos"}


class ErrorUpstream(Exception):
    """Parámetro inválido (fracción fuera de [0,1), capacidad ≤ 0, días negativos...)."""


# ------------------------------------------------------------------------------------------------
# 2. UTILIDADES
# ------------------------------------------------------------------------------------------------
def _frac(nombre, x, incluye_cero=True):
    if x is None:
        raise ErrorUpstream(f"{nombre} no puede ser None")
    if not ((0 <= x < 1) if incluye_cero else (0 < x <= 1)):
        raise ErrorUpstream(f"{nombre}={x} fuera de rango")
    return x


def _pos(nombre, x):
    if x is not None and x <= 0:
        raise ErrorUpstream(f"{nombre}={x} debe ser > 0")
    return x


def viajes(cantidad, capacidad):
    """Viajes enteros; None (PENDIENTE) si no hay capacidad explícita."""
    if capacidad is None:
        return None
    _pos("capacidad", capacidad)
    return math.ceil(cantidad / capacidad - 1e-12)


def _cerca(a, b, tol=TOL):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _div(a, b):
    return None if (a is None or b is None) else a / b


# ------------------------------------------------------------------------------------------------
# 3. PRODUCCIÓN (envoltorio de mp.calcular, sin recalcular)
# ------------------------------------------------------------------------------------------------
def parametros_produccion(E, dias_semana=5, nivel="medio"):
    p, d = mp.PERFILES[PERFIL], mp.DESEMPENO[nivel]
    return dict(aves_faenadas_dia=E, dias_semana=dias_semana, edad=p["edad"], peso=p["peso"],
                fcr=round(p["fcr_base"] + d["d_fcr"], 2), mort=d["mort"], doa=d["doa"],
                vacio=d["vacio"], kg_m2=d["kg_m2"])


def produccion(E, dias_semana=5, nivel="medio"):
    if dias_semana not in CALENDARIOS:
        raise ErrorUpstream(f"días/semana {dias_semana} no admitido por 03 ({list(CALENDARIOS)})")
    return mp.calcular(**parametros_produccion(E, dias_semana, nivel))


# ------------------------------------------------------------------------------------------------
# 4. POLLITOS BB
# ------------------------------------------------------------------------------------------------
def pollitos(E, dias_semana=5, nivel="medio", margen_pedido=MARGEN_PEDIDO_BASE, cap_camion=CAP_CAMION_POLLITOS):
    _frac("margen_pedido", margen_pedido)
    pr = produccion(E, dias_semana, nivel)
    sem, anio = pr["pollitos_alojados_semana_plena"], pr["pollitos_alojados_anio"]
    fae_sem, fae_anio = pr["aves_faenadas_semana_plena"], pr["aves_faenadas_anio"]
    recibir_sem = sem * (1 + margen_pedido)
    return {
        "aves_faenadas_semana_plena": fae_sem,
        "aves_cargadas_semana_plena": pr["aves_cargadas_semana_plena"],
        "pollitos_alojados_semana_plena": sem,
        "pollitos_alojados_semana_promedio": pr["pollitos_alojados_semana_promedio"],
        "pollitos_alojados_anio": anio,
        "pollitos_por_dia_faena": pr["pollitos_alojados_por_dia_faena"],
        "margen_mortalidad_pollitos_semana_plena": sem - fae_sem,
        "margen_mortalidad_pollitos_anio": anio - fae_anio,
        "margen_mortalidad_pct": sem / fae_sem - 1,
        "mortalidad_granja_aves_anio": pr["mortalidad_granja_aves_anio"],
        "mortalidad_transporte_aves_anio": pr["mortalidad_transporte_aves_anio"],
        "margen_pedido": margen_pedido,
        "pollitos_a_recibir_semana_plena": recibir_sem,
        "pollitos_a_recibir_anio": anio * (1 + margen_pedido),
        "viajes_pollitos_semana": viajes(recibir_sem, cap_camion),
        "capacidad_alojamiento_pollitos": pr["capacidad_alojamiento_pollitos"],
        "m2_galpon": pr["m2_galpon"],
        "inventario_aves_ritmo_pleno": pr["inventario_aves_ritmo_pleno"],
    }


# ------------------------------------------------------------------------------------------------
# 5. CADENA TEMPORAL (recepción ≠ carga ≠ nacimiento ≠ llegada a granja)
# ------------------------------------------------------------------------------------------------
def cadena_temporal(dias_almacen=D_ALMACEN_BASE, nivel="medio", h_nacimiento_a_granja=H_NACIMIENTO_A_GRANJA):
    """Días relativos a la CARGA (setting = día 0). Las horas entre nacimiento y llegada a granja
    son PENDIENTES: los eventos posteriores se informan como cota inferior (+ esas horas)."""
    if dias_almacen < 0:
        raise ErrorUpstream("días de almacenamiento < 0")
    edad = mp.PERFILES[PERFIL]["edad"]
    exp_d = None if h_nacimiento_a_granja is None else h_nacimiento_a_granja / 24
    nac = D_SETTER + D_HATCHER
    llegada = nac + (exp_d or 0.0)
    return {
        "dia_recepcion_huevo": -float(dias_almacen),
        "dia_carga_setting": 0.0,
        "dia_transferencia": D_SETTER,
        "dia_nacimiento": nac,
        "dia_llegada_granja_cota_inferior": llegada,
        "dia_retiro_aves_cota_inferior": llegada + edad,
        "dia_faena_cota_inferior": llegada + edad + VENTANA_PREFAENA_H / 24,
        "periodo_incubacion_d": nac,                                   # setting → nacimiento
        "almacenamiento_previo_d": float(dias_almacen),
        "expedicion_a_granja_d": exp_d,                                # PENDIENTE
        "lead_time_recepcion_a_nacimiento_d": dias_almacen + nac,
        "lead_time_recepcion_a_entrega_d": None if exp_d is None else dias_almacen + nac + exp_d,
        "lead_time_recepcion_a_entrega_d_cota_inferior": dias_almacen + nac,
        "lead_time_huevo_a_faena_d_cota_inferior": dias_almacen + nac + edad + VENTANA_PREFAENA_H / 24,
    }


# ------------------------------------------------------------------------------------------------
# 6. INCUBACIÓN: cálculo inverso, setter y hatcher por separado, cadencia simulada
# ------------------------------------------------------------------------------------------------
def simular_ocupacion(lote_carga, lote_transferido, dias_carga, semanas=16, d_setter=D_SETTER,
                      d_hatcher=D_HATCHER, limp_s=D_LIMPIEZA_SETTER, limp_h=D_LIMPIEZA_HATCHER):
    """Simula cargas semanales en los días `dias_carga` (lotes iguales). Cada lote ocupa el setter
    [t, t+18+limpieza) y el hatcher [t+18, t+18+3+limpieza). Devuelve ocupación máxima y media en
    régimen (descarta las semanas de arranque y cierre) y huevos cargados/transferidos en régimen."""
    eventos = [7 * w + d for w in range(semanas) for d in dias_carga]
    occ_s = [(t, t + d_setter + limp_s) for t in eventos]
    occ_h = [(t + d_setter, t + d_setter + d_hatcher + limp_h) for t in eventos]
    ini, fin = 7 * 5, 7 * (semanas - 5)
    puntos = sorted({p for a, b in occ_s + occ_h for p in (a, b) if ini <= p < fin} | {ini})

    def ocup(intervalos, t):
        return sum(1 for a, b in intervalos if a <= t < b)

    max_s = max(ocup(occ_s, p) for p in puntos) * lote_carga
    max_h = max(ocup(occ_h, p) for p in puntos) * lote_transferido

    def media(intervalos, lote):   # integral exacta de ocupación en [ini, fin) / duración
        return sum(max(0.0, min(b, fin) - max(a, ini)) for a, b in intervalos) * lote / (fin - ini)

    n_reg = sum(1 for t in eventos if ini <= t < fin)
    return {"max_setter": max_s, "max_hatcher": max_h, "media_setter": media(occ_s, lote_carga),
            "media_hatcher": media(occ_h, lote_transferido), "cargados_regimen_semana": n_reg * lote_carga / ((fin - ini) / 7),
            "transferidos_regimen_semana": n_reg * lote_transferido / ((fin - ini) / 7)}


def incubacion(pollitos_vendibles_sem, nivel="medio", margen_cap=MARGEN_CAPACIDAD_BASE, dias_almacen=D_ALMACEN_BASE,
               cadencia=None, horas_ventana=None, ovoscopia=OVOSCOPIA_RETIRA_INFERTILES, **override):
    """Pollitos vendibles/semana → huevos, setter y hatcher. `cadencia` = n.º de cargas (= nacimientos)
    por semana (clave de CADENCIAS) o una tupla de días; None → solo flujo continuo (diseño PENDIENTE)."""
    p = dict(INCUBACION[nivel], **override)
    F = _frac("fertilidad", p["fertilidad"], incluye_cero=False)
    H = _frac("hof", p["hof"], incluye_cero=False)
    pa, pt, ds = (_frac("perdida_alm", p["perdida_alm"]), _frac("perdida_tr", p["perdida_tr"]),
                  _frac("descarte", p["descarte"]))
    _frac("margen_cap", margen_cap)
    if dias_almacen < 0:
        raise ErrorUpstream("días de almacenamiento < 0")
    _pos("horas_ventana", horas_ventana)
    vend = pollitos_vendibles_sem
    nacidos = vend / (1 - ds)
    hos = F * H * (1 - pt)
    cargados = nacidos / hos
    fertiles = cargados * F
    transferidos = cargados * (1 - pt) * (F if ovoscopia else 1.0)
    recibidos = cargados / (1 - pa)
    k = 1 + margen_cap
    out = {
        "nivel_incubacion": nivel, "fertilidad": F, "incubabilidad_fertiles": H,
        "perdida_recepcion_almacen": pa, "perdida_transferencia": pt, "descarte_seleccion": ds,
        "incubabilidad_sobre_cargados": hos,
        "pollitos_vendibles_semana": vend,
        "pollitos_descarte_semana": nacidos - vend,
        "pollitos_nacidos_semana": nacidos,
        "huevos_recibidos_semana": recibidos,
        "huevos_descarte_recepcion_semana": recibidos - cargados,
        "huevos_cargados_semana": cargados,
        "huevos_fertiles_semana": fertiles,
        "huevos_infertiles_semana": cargados - fertiles,
        "huevos_transferidos_semana": transferidos,
        "huevos_por_pollito_vendible": recibidos / vend,
        "huevos_recibidos_anio": recibidos * SEMANAS_ANIO,   # ritmo pleno todo el año (cota superior)
        "margen_capacidad": margen_cap,
        "capacidad_semanal_carga_huevos": cargados * k,
        # flujo continuo (Little): ocupación MEDIA, sin margen
        "posiciones_setter_continuo": cargados * (D_SETTER + D_LIMPIEZA_SETTER) / 7,
        "posiciones_hatcher_continuo": transferidos * (D_HATCHER + D_LIMPIEZA_HATCHER) / 7,
        "huevos_en_proceso_wip": cargados * D_SETTER / 7 + transferidos * D_HATCHER / 7,
        "capacidad_almacen_huevos": recibidos * dias_almacen / 7 * k,
        "dias_almacen_huevo": dias_almacen,
        "viajes_huevos_semana": viajes(recibidos, CAP_CAMION_HUEVOS),
    }
    cad = None if cadencia is None else (CADENCIAS[cadencia] if isinstance(cadencia, int) else tuple(cadencia))
    if cad is None:
        out.update({k2: None for k2 in ("cargas_semana", "lote_carga_huevos", "lote_nacimiento_pollitos",
                                         "intervalo_medio_carga_d", "posiciones_setter_cadencia",
                                         "posiciones_hatcher_cadencia", "posiciones_setter_diseno",
                                         "posiciones_hatcher_diseno", "posiciones_fisicas_instaladas",
                                         "utilizacion_media_setter", "utilizacion_media_hatcher",
                                         "pollitos_h_seleccion_vacunacion")})
        return out
    if not cad or len(set(cad)) != len(cad) or not all(0 <= d < 7 for d in cad):
        raise ErrorUpstream(f"cadencia inválida: {cad}")
    n = len(cad)
    lote_c, lote_t, lote_n = cargados / n, transferidos / n, vend / n
    sim = simular_ocupacion(lote_c, lote_t, cad)
    ps_d, ph_d = sim["max_setter"] * k, sim["max_hatcher"] * k
    out.update({
        "cargas_semana": n, "lote_carga_huevos": lote_c, "lote_nacimiento_pollitos": lote_n,
        "intervalo_medio_carga_d": 7 / n,
        "posiciones_setter_cadencia": sim["max_setter"], "posiciones_hatcher_cadencia": sim["max_hatcher"],
        "posiciones_setter_diseno": ps_d, "posiciones_hatcher_diseno": ph_d,
        "posiciones_fisicas_instaladas": ps_d + ph_d,     # inventario de posiciones, NO capacidad de producción
        "utilizacion_media_setter": sim["media_setter"] / ps_d,
        "utilizacion_media_hatcher": sim["media_hatcher"] / ph_d,
        "pollitos_h_seleccion_vacunacion": None if horas_ventana is None else lote_n / horas_ventana,
    })
    return out


def elasticidades(pollitos_vendibles_sem, nivel="medio", h=1e-6):
    """Elasticidad de los huevos recibidos respecto de fertilidad e incubabilidad de fértiles
    (d ln huevos / d ln x), por diferencias centradas, y variación en los rangos de supuesto."""
    base = INCUBACION[nivel]
    out = {}
    for var in ("fertilidad", "hof"):
        x = base[var]
        up = incubacion(pollitos_vendibles_sem, nivel, **{var: x * (1 + h)})["huevos_recibidos_semana"]
        dn = incubacion(pollitos_vendibles_sem, nivel, **{var: x * (1 - h)})["huevos_recibidos_semana"]
        out[f"elasticidad_huevos_{var}"] = (math.log(up) - math.log(dn)) / (math.log(1 + h) - math.log(1 - h))
        b = incubacion(pollitos_vendibles_sem, nivel)["huevos_recibidos_semana"]
        lo = min(v[var] for v in INCUBACION.values())
        hi = max(v[var] for v in INCUBACION.values())
        out[f"rango_{var}_pct"] = (hi - lo) / x
        out[f"var_huevos_{var}_en_min_pct"] = incubacion(pollitos_vendibles_sem, nivel, **{var: lo})["huevos_recibidos_semana"] / b - 1
        out[f"var_huevos_{var}_en_max_pct"] = incubacion(pollitos_vendibles_sem, nivel, **{var: hi})["huevos_recibidos_semana"] / b - 1
    return out


def reproductoras_fase_futura(pollitos_vendibles_sem, fase, pollitos_reproductora_semana=POLLITOS_REPRODUCTORA_SEMANA):
    """Opción C. Solo en la arquitectura futura; en cualquier otra devuelve 0 (no se asumen
    reproductoras). Recría, machos y reposición: PENDIENTES (DPV-045)."""
    if FASES[fase]["pollito"] != "C_reproductoras":
        return {"reproductoras_hembras_postura_equiv": 0.0, "estado": "NO APLICA en esta arquitectura"}
    _pos("pollitos_reproductora_semana", pollitos_reproductora_semana)
    return {"reproductoras_hembras_postura_equiv": pollitos_vendibles_sem / pollitos_reproductora_semana,
            "estado": "ESTIMACIÓN de 03 (DPV-045); recría, machos y reposición PENDIENTES"}


# ------------------------------------------------------------------------------------------------
# 7. SINCRONIZACIÓN NACIMIENTO – COLOCACIÓN – ENGORDE – FAENA (granja ≠ galpón)
# ------------------------------------------------------------------------------------------------
def plazas_galpon(galpon_m2, dias_semana=5, nivel="medio"):
    """Plazas de un galpón = pollitos alojados por m² (03, depende de densidad, peso y mortalidad)
    × m² del galpón (SUP-031). Equivalencia derivada, no dato de una granja real."""
    _pos("galpon_m2", galpon_m2)
    return produccion(10000, dias_semana, nivel)["pollitos_m2_alojamiento"] * galpon_m2


def sincronizacion(E, dias_semana=5, nivel="medio", unidad="galpon", galpon_m2=None, plazas_granja=None,
                   galpones_por_granja=GALPONES_POR_GRANJA, origen_pollito="B_huevo_fertil", cadencia=None,
                   lote_proveedor=LOTE_PROVEEDOR_POLLITOS, dias_cosecha_ref=DIAS_COSECHA_REFERENCIA,
                   tolerancia_edad_d=TOLERANCIA_EDAD_COLOCACION_D):
    """Chequeo conceptual (no optimiza). `unidad` = "galpon" (unidad de colocación = un galpón) o
    "granja" (toda la granja se coloca junta). Devuelve indicadores y banderas; PENDIENTE si falta un dato."""
    if unidad not in ("galpon", "granja"):
        raise ErrorUpstream("unidad debe ser 'galpon' o 'granja'")
    pr = produccion(E, dias_semana, nivel)
    p = parametros_produccion(E, dias_semana, nivel)
    dem = pollitos(E, dias_semana, nivel)["pollitos_a_recibir_semana_plena"]
    pg = None if galpon_m2 is None else plazas_galpon(galpon_m2, dias_semana, nivel)
    if unidad == "galpon":
        U = pg
    else:
        _pos("plazas_granja", plazas_granja)
        U = plazas_granja if plazas_granja is not None else (
            None if (galpones_por_granja is None or pg is None) else galpones_por_granja * pg)
    if U is None:
        lote = None
    elif origen_pollito == "B_huevo_fertil":
        lote = None if cadencia is None else dem / (len(CADENCIAS[cadencia]) if isinstance(cadencia, int) else len(cadencia))
    elif origen_pollito == "A_compra":
        lote = lote_proveedor
    else:
        raise ErrorUpstream(f"origen de pollito desconocido: {origen_pollito}")
    ciclo = p["edad"] + p["vacio"]
    supervivencia = (1 - p["mort"]) * (1 - p["doa"])
    col_sem = _div(dem, U)
    nac_por_col = _div(U, lote)
    n_cad = None if (origen_pollito != "B_huevo_fertil" or cadencia is None) else (
        len(CADENCIAS[cadencia]) if isinstance(cadencia, int) else len(cadencia))
    spread = None if (nac_por_col is None or n_cad is None) else (math.ceil(nac_por_col - 1e-9) - 1) * 7 / n_cad
    dias_fae_unidad = None if U is None else U * supervivencia / E
    flag_multi = None if nac_por_col is None else int(nac_por_col > 1 + 1e-9)
    flag_cosecha = None if dias_fae_unidad is None else int(dias_fae_unidad > dias_cosecha_ref + 1e-9)
    motivos, faltan = [], []
    if flag_multi is None:
        faltan.append("lote de nacimiento")
    elif flag_multi and (tolerancia_edad_d is None or spread is None or spread > tolerancia_edad_d):
        motivos.append("una colocación requiere varios nacimientos (edades mezcladas; tolerancia PENDIENTE)")
    if flag_cosecha is None:
        faltan.append("plazas de la unidad")
    elif flag_cosecha:
        motivos.append(f"cosechar una unidad lleva más de {dias_cosecha_ref} días de faena")
    if motivos:
        estado = "REQUIERE VALIDACIÓN: " + "; ".join(motivos) + (f" (PENDIENTE: {', '.join(faltan)})" if faltan else "")
    elif faltan:
        estado = f"PENDIENTE (faltan: {', '.join(faltan)})"
    else:
        estado = "SIN CONFLICTO DETECTADO con estos supuestos"
    return {
        "unidad_colocacion": unidad, "estado_sincronizacion": estado,
        "plazas_por_galpon_equivalente": pg,
        "plazas_unidad_colocacion": U,
        "galpones_por_granja_real": galpones_por_granja,                      # PENDIENTE si None
        "galpones_por_granja_equivalente": _div(plazas_granja, pg),
        "demanda_media_pollitos_semana": dem,
        "lote_nacimiento_pollitos": lote,
        "colocaciones_semana": col_sem,
        "intervalo_entre_colocaciones_sistema_d": _div(7, col_sem),
        "intervalo_entre_colocaciones_misma_unidad_d": float(ciclo),
        "lotes_simultaneos_en_crianza": None if col_sem is None else col_sem * p["edad"] / 7,
        "unidades_requeridas": _div(pr["capacidad_alojamiento_pollitos"], U),
        "nacimientos_por_colocacion": nac_por_col,
        "dispersion_edad_colocacion_d": spread,
        "aves_a_faena_por_unidad": None if U is None else U * supervivencia,
        "dias_faena_por_unidad": dias_fae_unidad,
        "unidades_cosechadas_por_dia_faena": None if dias_fae_unidad is None else 1 / dias_fae_unidad,
        "flag_llenado_multinacimiento": flag_multi,
        "flag_cosecha_excede_referencia": flag_cosecha,
    }


# ------------------------------------------------------------------------------------------------
# 8. ALIMENTO
# ------------------------------------------------------------------------------------------------
def alimento(E, dias_semana=5, nivel="medio"):
    pr = produccion(E, dias_semana, nivel)
    t_anio, t_sem = pr["alimento_t_anio"], pr["alimento_t_semana_plena"]
    out = {
        "alimento_por_ave_faenada_kg": pr["alimento_por_ave_faenada_kg"],
        "alimento_t_dia_entrega_7d": t_sem / 7,
        "alimento_t_dia_promedio_calendario": t_anio / 365,
        "alimento_t_semana_plena": t_sem,
        "alimento_t_semana_promedio": pr["alimento_t_semana_promedio"],
        "alimento_t_mes_promedio": pr["alimento_t_mes_promedio"],
        "alimento_t_anio": t_anio,
        "alimento_inicio_t_anio": pr["alimento_inicio_t_anio"],
        "alimento_crecimiento_t_anio": pr["alimento_crecimiento_t_anio"],
        "alimento_terminacion_t_anio": pr["alimento_terminacion_t_anio"],
        "alimento_ciclo_crianza_t": pr["alimento_ciclo_crianza_t"],
    }
    for mpk, (lo, hi, punto) in COMPOSICION.items():
        out[f"mp_{mpk}_t_anio_min"] = t_anio * lo
        out[f"mp_{mpk}_t_anio_max"] = t_anio * hi
        out[f"mp_{mpk}_t_anio_ilustrativo"] = None if punto is None else t_anio * punto
    out["mp_resto_t_anio_ilustrativo"] = t_anio * FRACCION_MICROS
    return out


def planta_alimento(t_semana, dias_op=5, horas_dia=8, eficiencia=0.85, margen=MARGEN_CAPACIDAD_BASE,
                    factor_pico=FACTOR_PICO_ALIMENTO):
    """Capacidad de producción requerida (t/h de alimento terminado) para la cadencia de fabricación
    dada. Sin fabricante."""
    for n, v in (("dias_op", dias_op), ("horas_dia", horas_dia), ("factor_pico", factor_pico)):
        _pos(n, v)
    if not 0 < dias_op <= 7 or not 0 < horas_dia <= 24:
        raise ErrorUpstream("días u horas de operación fuera de rango")
    _frac("eficiencia", eficiencia, incluye_cero=False)
    _frac("margen", margen)
    t_h_neta = t_semana * factor_pico / (dias_op * horas_dia)
    t_h_req = t_h_neta / eficiencia * (1 + margen)
    instalada_sem = t_h_req * dias_op * horas_dia * eficiencia
    return {"dias_operacion": dias_op, "horas_dia": horas_dia, "eficiencia": eficiencia, "margen": margen,
            "t_dia_operacion": t_semana * factor_pico / dias_op,
            "t_h_neta": t_h_neta, "t_h_requerida": t_h_req,
            "t_semana_capacidad_efectiva": instalada_sem,
            "capacidad_ociosa_t_semana": instalada_sem - t_semana * factor_pico,
            "utilizacion": t_semana * factor_pico / instalada_sem}


def horas_produccion_semana(t_semana, capacidad_t_h, eficiencia=0.85):
    """Horas de producción por semana que necesita una planta de capacidad nominal dada para
    cubrir la demanda propia (y fracción de las 168 h de la semana)."""
    _pos("capacidad_t_h", capacidad_t_h)
    _frac("eficiencia", eficiencia, incluye_cero=False)
    h = t_semana / (capacidad_t_h * eficiencia)
    return {"horas_produccion_semana": h, "fraccion_semana_168h": h / 168}


# ------------------------------------------------------------------------------------------------
# 9. SILOS (solo desde variables) e INVENTARIOS por categoría y propiedad
# ------------------------------------------------------------------------------------------------
def silo(consumo_t_dia, dias_stock, densidad, factor_llenado=FACTOR_LLENADO, volumen_unitario=VOLUMEN_UNITARIO_SILO_M3):
    if consumo_t_dia < 0 or dias_stock < 0:
        raise ErrorUpstream("consumo y días de stock deben ser ≥ 0")
    if densidad is None:
        return {"t": consumo_t_dia * dias_stock, "m3_utiles": None, "m3_brutos": None, "n_silos": None}
    _pos("densidad", densidad)
    _frac("factor_llenado", factor_llenado, incluye_cero=False)
    t = consumo_t_dia * dias_stock
    m3u = t / densidad
    m3b = m3u / factor_llenado
    return {"t": t, "m3_utiles": m3u, "m3_brutos": m3b,
            "n_silos": None if volumen_unitario is None else math.ceil(m3b / _pos("volumen_unitario", volumen_unitario) - 1e-12)}


def almacenamiento(E, modo_alimento, dias_semana=5, nivel="medio", dias_maiz=15, dias_soja=15, dias_alim_planta=2,
                   dias_alim_granja=3, dens_maiz=0.72, dens_soja=0.60, dens_alim=0.60, n_mp_granel=2,
                   n_tipos_alimento=3, volumen_unitario=VOLUMEN_UNITARIO_SILO_M3):
    """Volumen de silos (m³) de las instalaciones que la arquitectura obliga a TENER (no propiedad
    del material: ver `inventario_alimento`). A compra: silos de granja. B façon: granja (los granos
    se almacenan en el elaborador o acopio: sus t se informan, el silo no es propio). C planta
    propia: granos + alimento terminado + granja."""
    al = alimento(E, dias_semana, nivel)
    t_dia = al["alimento_t_dia_entrega_7d"]
    r = {"modo_alimento": modo_alimento}
    g = silo(t_dia, dias_alim_granja, dens_alim, volumen_unitario=volumen_unitario)
    r.update({"granja_t": g["t"], "granja_m3_brutos": g["m3_brutos"]})
    maiz_dia, soja_dia = t_dia * COMPOSICION["maiz"][2], t_dia * COMPOSICION["harina_soja"][2]
    if modo_alimento == "A_compra":
        r.update({"maiz_t": 0.0, "maiz_m3_brutos": 0.0, "soja_t": 0.0, "soja_m3_brutos": 0.0,
                  "alim_planta_t": 0.0, "alim_planta_m3_brutos": 0.0, "silos_minimos_segregacion_planta": 0,
                  "n_silos_planta": 0})
    else:
        m = silo(maiz_dia, dias_maiz, dens_maiz, volumen_unitario=volumen_unitario)
        s = silo(soja_dia, dias_soja, dens_soja, volumen_unitario=volumen_unitario)
        propio = modo_alimento == "C_planta_propia"
        a = silo(t_dia, dias_alim_planta if propio else 0, dens_alim, volumen_unitario=volumen_unitario)
        r.update({"maiz_t": m["t"], "maiz_m3_brutos": m["m3_brutos"], "soja_t": s["t"], "soja_m3_brutos": s["m3_brutos"],
                  "alim_planta_t": a["t"], "alim_planta_m3_brutos": a["m3_brutos"],
                  "silos_minimos_segregacion_planta": (n_mp_granel + n_tipos_alimento) if propio else 0,
                  "n_silos_planta": (None if volumen_unitario is None else
                                     (m["n_silos"] + s["n_silos"] + a["n_silos"])) if propio else 0})
    return r


ARQUITECTURAS_INVENTARIO = ("A_compra", "B_facon_mp_empresa", "B_facon_mp_elaborador", "C_planta_propia")
CATEGORIAS_INVENTARIO = ("alimento_terminado_granja", "alimento_terminado_planta", "maiz", "harina_soja",
                         "micros_aceite_otros", "material_en_proceso")
_DIAS_CAT = {"alimento_terminado_granja": "alimento_granja", "alimento_terminado_planta": "alimento_planta",
             "maiz": "maiz", "harina_soja": "harina_soja", "micros_aceite_otros": "micros"}
_FRAC_CAT = {"alimento_terminado_granja": 1.0, "alimento_terminado_planta": 1.0,
             "maiz": COMPOSICION["maiz"][2], "harina_soja": COMPOSICION["harina_soja"][2],
             "micros_aceite_otros": FRACCION_MICROS}
# (propietario, ubicación) por arquitectura y categoría. "empresa" = stock PROPIO; "tercero" = en tercero.
PROPIEDAD = {
    "A_compra": {
        "alimento_terminado_granja": ("empresa", "silos de granja (integrado o propia)"),
        "alimento_terminado_planta": ("tercero", "fábrica proveedora"),
        "maiz": ("tercero", "fábrica proveedora / su acopio"), "harina_soja": ("tercero", "fábrica proveedora"),
        "micros_aceite_otros": ("tercero", "fábrica proveedora"), "material_en_proceso": ("tercero", "fábrica proveedora")},
    "B_facon_mp_empresa": {
        "alimento_terminado_granja": ("empresa", "silos de granja"),
        "alimento_terminado_planta": ("empresa", "elaborador (hasta el despacho)"),
        "maiz": ("empresa", "elaborador o acopio"), "harina_soja": ("empresa", "elaborador o acopio"),
        "micros_aceite_otros": ("empresa", "elaborador"), "material_en_proceso": ("empresa", "elaborador")},
    "B_facon_mp_elaborador": {
        "alimento_terminado_granja": ("empresa", "silos de granja"),
        "alimento_terminado_planta": ("tercero", "elaborador"),
        "maiz": ("tercero", "elaborador"), "harina_soja": ("tercero", "elaborador"),
        "micros_aceite_otros": ("tercero", "elaborador"), "material_en_proceso": ("tercero", "elaborador")},
    "C_planta_propia": {c: ("empresa", "planta propia") for c in CATEGORIAS_INVENTARIO[1:]}
    | {"alimento_terminado_granja": ("empresa", "silos de granja")},
}


def inventario_alimento(E, arquitectura, dias_semana=5, nivel="medio", dias=None):
    """Inventario por CATEGORÍA con propietario y ubicación. El stock de la cadena por categoría se
    calcula con los MISMOS días supuestos en todas las arquitecturas (lo que cambia es quién lo
    posee). Los días que mantiene un tercero son PENDIENTES: su stock es REFERENCIAL. Material en
    proceso: PENDIENTE (depende del equipo y la operación). Nunca se suman categorías distintas."""
    if arquitectura not in PROPIEDAD:
        raise ErrorUpstream(f"arquitectura desconocida: {arquitectura}")
    d = dict(DIAS_STOCK_BASE, **(dias or {}))
    t_dia = alimento(E, dias_semana, nivel)["alimento_t_dia_entrega_7d"]
    out = {}
    for cat in CATEGORIAS_INVENTARIO:
        prop, ubic = PROPIEDAD[arquitectura][cat]
        if cat == "material_en_proceso":
            t_cad, dias_c, cons = None, None, None
        else:
            dias_c = d[_DIAS_CAT[cat]]
            if dias_c < 0:
                raise ErrorUpstream("días de stock < 0")
            cons = t_dia * _FRAC_CAT[cat]
            t_cad = cons * dias_c
        out[cat] = {"propietario": prop, "ubicacion": ubic, "consumo_t_dia": cons, "dias_cobertura": dias_c,
                    "stock_cadena_t": t_cad,
                    "stock_propio_t": (t_cad if prop == "empresa" else 0.0) if t_cad is not None else None,
                    "stock_tercero_referencial_t": (t_cad if prop == "tercero" else 0.0) if t_cad is not None else None,
                    "dias_tercero_validados": False if prop == "tercero" else None}
    return out


def inventario_plano(inv):
    """Aplana para el CSV: <categoria>__<campo> (solo numéricos)."""
    return {f"{c}__{k}": v for c, dd in inv.items() for k, v in dd.items()
            if k in ("consumo_t_dia", "dias_cobertura", "stock_cadena_t", "stock_propio_t", "stock_tercero_referencial_t")}


# ------------------------------------------------------------------------------------------------
# 10. OPCIONES (make or buy): capacidad física PROPIA requerida, calculada por separado
# ------------------------------------------------------------------------------------------------
def opcion_pollito(E, modo, dias_semana=5, nivel="medio", nivel_inc="medio", margen_cap=MARGEN_CAPACIDAD_BASE,
                   cadencia=2):
    if modo not in OPCIONES["pollito"]:
        raise ErrorUpstream(f"modo de pollito desconocido: {modo}")
    po = pollitos(E, dias_semana, nivel)
    dem = po["pollitos_a_recibir_semana_plena"]
    base = {"modo": modo, "pollitos_demanda_semana": dem, "pollitos_comprados_semana": 0.0,
            "huevos_comprados_semana": 0.0, "capacidad_semanal_carga_huevos_propia": 0.0,
            "posiciones_setter_propias": 0.0, "posiciones_hatcher_propias": 0.0, "reproductoras_propias": 0.0}
    if modo == "A_compra":
        base["pollitos_comprados_semana"] = dem
    else:
        inc = incubacion(dem, nivel_inc, margen_cap, cadencia=cadencia)
        base.update({"capacidad_semanal_carga_huevos_propia": inc["capacidad_semanal_carga_huevos"],
                     "posiciones_setter_propias": inc["posiciones_setter_diseno"],
                     "posiciones_hatcher_propias": inc["posiciones_hatcher_diseno"]})
        if modo == "B_huevo_fertil":
            base["huevos_comprados_semana"] = inc["huevos_recibidos_semana"]
        else:
            base["reproductoras_propias"] = reproductoras_fase_futura(dem, "FF")["reproductoras_hembras_postura_equiv"]
    return base


def opcion_alimento(E, modo, dias_semana=5, nivel="medio", dias_op=5, horas=16, eficiencia=0.85,
                    margen=MARGEN_CAPACIDAD_BASE):
    if modo not in OPCIONES["alimento"]:
        raise ErrorUpstream(f"modo de alimento desconocido: {modo}")
    al = alimento(E, dias_semana, nivel)
    t_sem = al["alimento_t_semana_plena"]
    base = {"modo": modo, "alimento_demanda_t_semana": t_sem, "alimento_comprado_t_semana": 0.0,
            "materias_primas_compradas_t_semana": 0.0, "elaboracion_terceros_t_semana": 0.0,
            "capacidad_planta_propia_t_h": 0.0}
    if modo == "A_compra":
        base["alimento_comprado_t_semana"] = t_sem
    elif modo == "B_facon":
        base["materias_primas_compradas_t_semana"] = t_sem
        base["elaboracion_terceros_t_semana"] = t_sem
    else:
        base["materias_primas_compradas_t_semana"] = t_sem
        base["capacidad_planta_propia_t_h"] = planta_alimento(t_sem, dias_op, horas, eficiencia, margen)["t_h_requerida"]
    return base


def opcion_granjas(E, modo, dias_semana=5, nivel="medio", fraccion_propia=0.0):
    if modo not in OPCIONES["granjas"]:
        raise ErrorUpstream(f"modo de granjas desconocido: {modo}")
    if not 0 <= fraccion_propia <= 1:
        raise ErrorUpstream("fraccion_propia fuera de [0, 1]")
    pr = produccion(E, dias_semana, nivel)
    plazas, m2 = pr["capacidad_alojamiento_pollitos"], pr["m2_galpon"]
    base = {"modo": modo, "plazas_demanda": plazas, "m2_demanda": m2, "plazas_terceros_independientes": 0.0,
            "plazas_integrados": 0.0, "plazas_propias": 0.0, "m2_propios": 0.0}
    if modo == "A_terceros":
        base["plazas_terceros_independientes"] = plazas
    elif modo == "B_integrados":
        base["plazas_integrados"] = plazas
    elif modo == "C_propias":
        base.update({"plazas_propias": plazas, "m2_propios": m2})
    else:
        base.update({"plazas_propias": plazas * fraccion_propia, "m2_propios": m2 * fraccion_propia,
                     "plazas_integrados": plazas * (1 - fraccion_propia)})
    return base


# ------------------------------------------------------------------------------------------------
# 11. LOGÍSTICA UPSTREAM
# ------------------------------------------------------------------------------------------------
def logistica(E, dias_semana=5, nivel="medio", modo_alimento="A_compra", cap_granelero=CAP_GRANELERO_T,
              cap_grano=None, cap_pollitos=CAP_CAMION_POLLITOS):
    al, po = alimento(E, dias_semana, nivel), pollitos(E, dias_semana, nivel)
    t_sem = al["alimento_t_semana_plena"]
    granos_sem = t_sem * (COMPOSICION["maiz"][2] + COMPOSICION["harina_soja"][2])
    entra_grano = modo_alimento in ("B_facon", "C_planta_propia")
    return {
        "viajes_alimento_granja_semana": viajes(t_sem, cap_granelero),
        "viajes_alimento_granja_dia_7d": None if cap_granelero is None else viajes(t_sem, cap_granelero) / 7,
        "granos_t_semana_entrada": granos_sem if entra_grano else 0.0,
        "viajes_grano_semana": (viajes(granos_sem, cap_grano) if entra_grano else 0),
        "viajes_pollitos_semana": viajes(po["pollitos_a_recibir_semana_plena"], cap_pollitos),
    }


# ------------------------------------------------------------------------------------------------
# 12. CSV (formato largo; sin precios)
# ------------------------------------------------------------------------------------------------
COLUMNAS = ["bloque", "escala_aves_faenadas_dia", "dias_faena_semana", "nivel_produccion", "opcion",
            "parametros", "variable", "valor", "unidad", "periodo", "clasificacion", "estado", "fuente", "nota"]

UNIDAD = [  # (fragmento, unidad) — primera coincidencia
    ("flag_", "indicador"), ("pollitos_h", "pollitos/h"), ("elasticidad", "ratio"), ("var_huevos", "ratio"),
    ("rango_", "ratio"), ("posiciones", "posiciones"), ("reproductoras", "reproductoras"),
    ("huevos_por_pollito", "ratio"), ("cargas_semana", "nacimientos"), ("nacimientos_por", "ratio"),
    ("utilizacion", "ratio"), ("fraccion", "ratio"), ("intervalo", "d"), ("dispersion", "d"), ("lead_time", "d"),
    ("dia_", "d"), ("periodo_", "d"), ("almacenamiento_previo", "d"), ("expedicion", "d"), ("dias_faena_por", "d"),
    ("dias_cobertura", "d"), ("huevos", "huevos"), ("lote_nacimiento", "pollitos"), ("pollitos", "pollitos"),
    ("plazas", "pollitos"), ("aves", "aves"), ("mortalidad", "aves"), ("colocaciones", "colocaciones"),
    ("lotes_simultaneos", "lotes"), ("unidades", "unidades"), ("galpones_por", "unidades"), ("t_h", "t/h"),
    ("horas", "h"), ("_m3", "m³"), ("m3_", "m³"), ("m2", "m²"), ("_kg", "kg"), ("_pct", "ratio"),
    ("margen", "ratio"), ("eficiencia", "ratio"), ("fertilidad", "ratio"), ("incubabilidad", "ratio"),
    ("perdida", "ratio"), ("descarte", "ratio"), ("viajes", "viajes"), ("silos", "silos"), ("dias", "d"),
    ("_t", "t"), ("t_", "t"),
]


def unidad(var):
    for clave, u in UNIDAD:
        if clave in var:
            return u
    return "texto"


def periodo(var):
    if "anio" in var:
        return "año"
    if "semana_promedio" in var or "mes_promedio" in var:
        return "promedio anual"
    if "semana" in var:
        return "semana plena"
    if "lote" in var or "nacimiento" in var:
        return "por lote / nacimiento"
    if "_dia" in var or var.startswith("dia_"):
        return "día"
    return "instantáneo / capacidad"


class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, ds, nivel, opcion, params, d, clasif, fuente, nota="", claves=None):
        for k in (claves or d):
            v = d[k]
            if isinstance(v, (str, bool)):
                continue
            estado = "PENDIENTE" if v is None else "CALCULADO"
            self.filas.append({
                "bloque": bloque, "escala_aves_faenadas_dia": E, "dias_faena_semana": ds, "nivel_produccion": nivel,
                "opcion": opcion, "parametros": params, "variable": k,
                "valor": "" if v is None else (round(v, 4) if isinstance(v, float) else v),
                "unidad": unidad(k), "periodo": periodo(k),
                "clasificacion": clasif if v is not None else "[PENDIENTE DE VALIDACIÓN]",
                "estado": estado, "fuente": fuente, "nota": nota})


def _codigo(s):
    """Código breve del estado de sincronización para la columna nota del CSV."""
    e = s["estado_sincronizacion"]
    if e.startswith("SIN CONFLICTO"):
        return "SIN_CONFLICTO_DETECTADO"
    partes = [c for c, f in (("multinacimiento", "flag_llenado_multinacimiento"), ("cosecha", "flag_cosecha_excede_referencia"))
              if s[f] == 1]
    pend = [c for c, f in (("lote", "flag_llenado_multinacimiento"), ("plazas", "flag_cosecha_excede_referencia"))
            if s[f] is None]
    return ("REQUIERE_VALIDACION:" + "+".join(partes) if partes else "PENDIENTE") + ("|pendiente:" + "+".join(pend) if pend else "")


def construir():
    t = Tabla()
    F03 = "03 modelo_escenarios_produccion.py v1.1 (importado)"
    for da in D_ALMACEN_HUEVO:
        t.add("2_cadena_temporal", "-", "-", "medio", "-", f"dias_almacen={da}; setter=18; hatcher=3",
              cadena_temporal(da), "[SUPUESTO]", FUENTE,
              "Día 0 = carga (setting). Incubación = 21 d; lead time recepción→entrega incluye almacenamiento; "
              "horas nacimiento→granja PENDIENTES (cota inferior)")
    for E in ESCALAS:
        for ds in CALENDARIOS:
            for nv in NIVELES:
                po = pollitos(E, ds, nv)
                dem = po["pollitos_a_recibir_semana_plena"]
                t.add("1_pollitos", E, ds, nv, "-", "margen_pedido=0", po, "[ESTIMACIÓN]", F03,
                      "Demanda física MEDIA de pollitos; igual para todas las opciones de abastecimiento",
                      claves=[k for k in po if k != "viajes_pollitos_semana"])
                for mpd in MARGEN_PEDIDO_BARRIDO[1:]:
                    t.add("1_pollitos", E, ds, nv, "-", f"margen_pedido={mpd} (SUP-142)",
                          pollitos(E, ds, nv, margen_pedido=mpd), "[SUPUESTO]", FUENTE,
                          "Sensibilidad del pedido; no es mortalidad",
                          claves=["pollitos_a_recibir_semana_plena", "pollitos_a_recibir_anio"])
                t.add("1_pollitos_entregas", E, ds, nv, "-", "cap_camion_pollitos=None", po, "[PENDIENTE DE VALIDACIÓN]",
                      FUENTE, "Sin capacidad validada (DPV-047, DPV-084)", claves=["viajes_pollitos_semana"])
                for cp in CAP_CAMION_POLLITOS_BARRIDO:
                    t.add("1_pollitos_entregas", E, ds, nv, "-", f"cap_camion_pollitos={cp} (SUP-096 barrido)",
                          pollitos(E, ds, nv, cap_camion=cp), "[SUPUESTO]", FUENTE, "Barrido ilustrativo, NO capacidad",
                          claves=["viajes_pollitos_semana"])
                # Incubación: flujo continuo por nivel; setter/hatcher por cadencia (nivel medio de incubación)
                for ni in INCUBACION:
                    inc = incubacion(dem, ni)
                    t.add("2_incubacion", E, ds, nv, "B_huevo_fertil", f"nivel_incubacion={ni}; margen_cap=0.15; "
                          f"dias_almacen=5; cadencia=None (flujo continuo)", inc, "[SUPUESTO]", FUENTE,
                          "Cálculo inverso; posiciones *_continuo = ocupación media (Little) sin margen; diseño requiere cadencia",
                          claves=[k for k in inc if inc[k] is not None or k in ("posiciones_setter_diseno",
                                                                                  "posiciones_hatcher_diseno")])
                for n in (CADENCIAS if nv == "medio" else ()):
                    for mc in MARGEN_CAPACIDAD:
                        q = incubacion(dem, margen_cap=mc, cadencia=n, horas_ventana=None)
                        t.add("2_incubacion_cadencia", E, ds, nv, "B_huevo_fertil",
                              f"cadencia={n} cargas=nacimientos/semana dias={CADENCIAS[n]}; margen_cap={mc}",
                              q, "[SUPUESTO]", FUENTE,
                              "Setter y hatcher por separado; ocupación máxima simulada × (1+margen); patrón ilustrativo (SUP-147)",
                              claves=["cargas_semana", "lote_carga_huevos", "lote_nacimiento_pollitos",
                                      "intervalo_medio_carga_d", "posiciones_setter_cadencia", "posiciones_hatcher_cadencia",
                                      "posiciones_setter_diseno", "posiciones_hatcher_diseno",
                                      "posiciones_fisicas_instaladas", "utilizacion_media_setter",
                                      "utilizacion_media_hatcher"])
                    for h in HORAS_VENTANA_PROCESO:
                        q = incubacion(dem, cadencia=n, horas_ventana=h)
                        t.add("2_incubacion_expedicion", E, ds, nv, "B_huevo_fertil",
                              f"cadencia={n}; horas_ventana={h} (SUP-147)", q, "[SUPUESTO]", FUENTE,
                              "Tamaño de lote de nacimiento ≠ demanda media semanal",
                              claves=["lote_nacimiento_pollitos", "pollitos_h_seleccion_vacunacion"])
                for da in D_ALMACEN_HUEVO:
                    t.add("2_incubacion_almacen", E, ds, nv, "B_huevo_fertil", f"dias_almacen={da}",
                          incubacion(dem, dias_almacen=da), "[SUPUESTO]", FUENTE,
                          "Flujo continuo de recepción; óptimo 3-6 d citado (FTE-305 [PVDP])",
                          claves=["capacidad_almacen_huevos"])
                t.add("2_incubacion_logistica", E, ds, nv, "B_huevo_fertil", "cap_camion_huevos=None", incubacion(dem),
                      "[PENDIENTE DE VALIDACIÓN]", FUENTE, "DPV-047", claves=["viajes_huevos_semana"])
                if nv == "medio":
                    t.add("2_incubacion_elasticidad", E, ds, nv, "B_huevo_fertil", "diferencias centradas; rangos SUP-143",
                          elasticidades(dem), "[ESTIMACIÓN]", FUENTE,
                          "Elasticidad −1 para ambos factores; la variación depende del rango de incertidumbre")
                t.add("2_reproductoras_fase_futura", E, ds, nv, "C_reproductoras", "pollitos_reproductora_semana=3.6",
                      reproductoras_fase_futura(dem, "FF"), "[ESTIMACIÓN]", "03 modelos_integracion.md §4.2",
                      "SOLO arquitectura futura; recría, machos y reposición PENDIENTES (DPV-045)")
                # Sincronización (galpón y granja como unidades distintas) — nivel medio
                for gm2 in (GALPON_M2 if nv == "medio" else ()):
                    for n in CADENCIAS:
                        s = sincronizacion(E, ds, nv, "galpon", galpon_m2=gm2, cadencia=n)
                        t.add("3_sincronizacion", E, ds, nv, "B_huevo_fertil",
                              f"unidad=galpon; galpon_m2={gm2} (SUP-031); cadencia={n}", s, "[ESTIMACIÓN]", FUENTE,
                              _codigo(s))
                for pg in (PLAZAS_GRANJA if nv == "medio" else ()):
                    for n in CADENCIAS:
                        s = sincronizacion(E, ds, nv, "granja", plazas_granja=pg, galpon_m2=1800, cadencia=n)
                        t.add("3_sincronizacion", E, ds, nv, "B_huevo_fertil",
                              f"unidad=granja (llenado conjunto); plazas_granja={pg} (barrido 13); cadencia={n}", s,
                              "[ESTIMACIÓN]", FUENTE, _codigo(s))
                s = sincronizacion(E, ds, nv, "galpon", galpon_m2=1800, origen_pollito="A_compra")
                t.add("3_sincronizacion", E, ds, nv, "A_compra", "unidad=galpon; galpon_m2=1800; lote_proveedor=None",
                      s, "[ESTIMACIÓN]", FUENTE, _codigo(s))
                # Alimento
                al = alimento(E, ds, nv)
                t.add("4_alimento", E, ds, nv, "-", "perfil medio", al, "[ESTIMACIÓN]", F03,
                      "Demanda física de alimento; igual para compra, façon o planta propia",
                      claves=[k for k in al if not k.startswith("mp_")])
                t.add("5_materias_primas", E, ds, nv, "-", "rangos 03 alimentacion.md §4; punto SUP-032", al,
                      "[ESTIMACIÓN]", "03 alimentacion.md §4 (FTE-160 [PVDP])",
                      "NO es fórmula: categorías y rangos; recetas = nutricionista",
                      claves=[k for k in al if k.startswith("mp_") and al[k] is not None])
                for dop in DIAS_OPERACION_PLANTA:
                    for h in HORAS_DIA_PLANTA:
                        for ef in EFICIENCIA_PLANTA:
                            t.add("6_planta_alimento", E, ds, nv, "C_planta_propia",
                                  f"dias_op={dop}; horas={h}; eficiencia={ef}; margen=0.15",
                                  planta_alimento(al["alimento_t_semana_plena"], dop, h, ef), "[SUPUESTO]", FUENTE,
                                  "Capacidad requerida para esa cadencia de fabricación; sin fabricante (SUP-148)",
                                  claves=["t_dia_operacion", "t_h_neta", "t_h_requerida", "capacidad_ociosa_t_semana",
                                          "utilizacion"])
                if nv == "medio":
                    for Eref in ESCALAS:
                        cap = planta_alimento(alimento(Eref)["alimento_t_semana_plena"], 5, 8, 0.85)["t_h_requerida"]
                        t.add("6_planta_horas", E, ds, nv, "C_planta_propia",
                              f"capacidad={round(cap, 2)} t/h (requerida por {Eref} aves/día con 5 d × 8 h, ef 0,85)",
                              horas_produccion_semana(al["alimento_t_semana_plena"], cap), "[ESTIMACIÓN]", FUENTE,
                              "Horas de producción/semana para la demanda propia con esa capacidad")
                    for modo in ("A_compra", "B_facon", "C_planta_propia"):
                        for dm, dsj, dap, dg in zip(DIAS_STOCK["maiz"], (7, 15, 15), DIAS_STOCK["alimento_planta"],
                                                    DIAS_STOCK["alimento_granja"]):
                            for dal in DENSIDAD_T_M3["alimento"]:
                                t.add("7_silos", E, ds, nv, modo,
                                      f"dias_stock maiz={dm} soja={dsj} alim_planta={dap} granja={dg}; "
                                      f"dens maiz=0.72 soja=0.60 alim={dal}; llenado=0.9",
                                      almacenamiento(E, modo, ds, nv, dm, dsj, dap, dg, 0.72, 0.60, dal), "[SUPUESTO]",
                                      FUENTE, "m³ de silos que la arquitectura obliga a tener; n_silos PENDIENTE (sin silo estándar)")
                    for arq in ARQUITECTURAS_INVENTARIO:
                        t.add("7_inventarios", E, ds, nv, arq,
                              "dias: " + "; ".join(f"{k}={v}" for k, v in DIAS_STOCK_BASE.items()),
                              inventario_plano(inventario_alimento(E, arq, ds, nv)), "[SUPUESTO]", FUENTE,
                              "Por categoría; propio vs en tercero (referencial, días del tercero PENDIENTES); no sumar categorías")
                for modo in OPCIONES["pollito"]:
                    t.add("8_opcion_pollito", E, ds, nv, modo, "nivel_inc=medio; margen_cap=0.15; cadencia=2 (ilustrativa)",
                          opcion_pollito(E, modo, ds, nv), "[ESTIMACIÓN]", FUENTE,
                          ("escenario de comparación" + (" (benchmark)" if BENCHMARK["pollito"] == modo else "")
                           + ("; solo arquitectura futura" if modo.startswith("C") else "")))
                for modo in OPCIONES["alimento"]:
                    t.add("8_opcion_alimento", E, ds, nv, modo, "dias_op=5; horas=16; eficiencia=0.85; margen=0.15",
                          opcion_alimento(E, modo, ds, nv), "[ESTIMACIÓN]", FUENTE,
                          "escenario de comparación" + (" (benchmark)" if BENCHMARK["alimento"] == modo else ""))
                for modo in ("A_terceros", "B_integrados", "C_propias"):
                    t.add("8_opcion_granjas", E, ds, nv, modo, "-", opcion_granjas(E, modo, ds, nv), "[ESTIMACIÓN]",
                          FUENTE, "escenario de comparación" + (" (benchmark)" if BENCHMARK["granjas"] == modo else "")
                          + "; plazas y m² = 03")
                for modo in ("A_compra", "B_facon", "C_planta_propia"):
                    t.add("10_logistica", E, ds, nv, modo, "granelero=28 t (SUP-096); cap_grano=None; cap_pollitos=None",
                          logistica(E, ds, nv, modo), "[SUPUESTO]", FUENTE, "Sin capacidad explícita → PENDIENTE")
                    if modo != "A_compra":
                        for cg in CAP_CAMION_GRANO_BARRIDO:
                            t.add("10_logistica", E, ds, nv, modo, f"cap_grano={cg} (SUP-096 barrido)",
                                  logistica(E, ds, nv, modo, cap_grano=cg), "[SUPUESTO]", FUENTE,
                                  "Barrido ilustrativo, no capacidad legal", claves=["viajes_grano_semana"])
    for f, d in FASES.items():
        for E in ESCALAS:
            t.add("9_arquitecturas_referencia", E, 5, "medio",
                  f"{f}: pollito={d['pollito']}; alimento={d['alimento']}; granjas={d['granjas']}",
                  d["nombre"], reproductoras_fase_futura(pollitos(E)["pollitos_a_recibir_semana_plena"], f),
                  "[SUPUESTO]", FUENTE, "Arquitectura de madurez de referencia (SUP-152); orden NO obligatorio")
    return t


def escribir_csv(t, ruta=None):
    ruta = ruta or os.path.join(AQUI, "escenarios_upstream.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(t.filas)
    return ruta


# ------------------------------------------------------------------------------------------------
# 13. PRUEBAS AUTOMÁTICAS
# ------------------------------------------------------------------------------------------------
def ejecutar_tests(t=None, verbose=True):
    global D_HATCHER, D_SETTER   # U12 los modifica temporalmente y los restaura
    res = []

    def ok(nombre, cond, detalle=""):
        res.append((nombre, bool(cond), detalle))

    t = t or construir()
    # U01 conservación de pollitos y huevos y orden de la cadena
    errs = 0
    for E in ESCALAS:
        for ds in CALENDARIOS:
            for nv in NIVELES:
                po = pollitos(E, ds, nv)
                for ni in INCUBACION:
                    inc = incubacion(po["pollitos_a_recibir_semana_plena"], ni)
                    p = INCUBACION[ni]
                    fwd = (inc["huevos_recibidos_semana"] * (1 - p["perdida_alm"]) * p["fertilidad"] * p["hof"]
                           * (1 - p["perdida_tr"]) * (1 - p["descarte"]))
                    cadena = [inc["huevos_recibidos_semana"], inc["huevos_cargados_semana"], inc["huevos_fertiles_semana"],
                              inc["pollitos_nacidos_semana"], inc["pollitos_vendibles_semana"],
                              po["pollitos_alojados_semana_plena"], po["aves_cargadas_semana_plena"],
                              po["aves_faenadas_semana_plena"]]
                    errs += not _cerca(fwd, po["pollitos_a_recibir_semana_plena"])
                    errs += not all((a >= b) if i == 4 else (a > b) for i, (a, b) in enumerate(zip(cadena, cadena[1:])))
                    errs += not _cerca(inc["huevos_recibidos_semana"], inc["huevos_cargados_semana"]
                                       + inc["huevos_descarte_recepcion_semana"])
                    errs += not _cerca(inc["huevos_cargados_semana"], inc["huevos_fertiles_semana"]
                                       + inc["huevos_infertiles_semana"])
                    errs += not _cerca(inc["pollitos_nacidos_semana"], inc["pollitos_vendibles_semana"]
                                       + inc["pollitos_descarte_semana"])
                errs += not _cerca(po["margen_mortalidad_pollitos_anio"],
                                   po["mortalidad_granja_aves_anio"] + po["mortalidad_transporte_aves_anio"])
    ok("U01 conservación pollitos/huevos; cadena recibidos > cargados > fértiles > nacidos > vendibles ≥ alojados > cargadas > faenadas",
       errs == 0, f"{errs} errores")

    # U02 (adaptado v1.1) capacidad instalada ≥ requerida: setter, hatcher, almacén, planta de alimento
    errs = 0
    for E in ESCALAS:
        dem = pollitos(E)["pollitos_a_recibir_semana_plena"]
        for ni in INCUBACION:
            for mc in MARGEN_CAPACIDAD:
                for n in CADENCIAS:
                    inc = incubacion(dem, ni, mc, cadencia=n)
                    errs += not (inc["posiciones_setter_diseno"] >= inc["posiciones_setter_continuo"] * (1 + mc) - 1e-6)
                    errs += not (inc["posiciones_hatcher_diseno"] >= inc["posiciones_hatcher_continuo"] * (1 + mc) - 1e-6)
                    errs += not (inc["capacidad_semanal_carga_huevos"] >= inc["huevos_cargados_semana"])
                    errs += not (0 < inc["utilizacion_media_setter"] <= 1 / (1 + mc) + 1e-9)
                    errs += not (0 < inc["utilizacion_media_hatcher"] <= 1 / (1 + mc) + 1e-9)
                inc = incubacion(dem, ni, mc)
                errs += not (inc["capacidad_almacen_huevos"] >= inc["huevos_recibidos_semana"] * 5 / 7)
        t_sem = alimento(E)["alimento_t_semana_plena"]
        for dop in DIAS_OPERACION_PLANTA:
            for h in HORAS_DIA_PLANTA:
                for ef in EFICIENCIA_PLANTA:
                    pa = planta_alimento(t_sem, dop, h, ef)
                    errs += not (pa["t_h_requerida"] * dop * h * ef >= t_sem - 1e-9)
                    errs += not _cerca(pa["utilizacion"], 1 / 1.15)
    ok("U02 capacidad instalada ≥ requerida (setter, hatcher, almacén, planta de alimento)", errs == 0, f"{errs} errores")

    # U03 alimento lineal (viajes enteros: no lineales por redondeo, acotados)
    errs = 0
    for E in ESCALAS:
        for ds in CALENDARIOS:
            for nv in NIVELES:
                a1, a2 = alimento(E, ds, nv), alimento(2 * E, ds, nv)
                for k, v in a1.items():
                    if v is None:
                        continue
                    errs += not (_cerca(a2[k], v) if k == "alimento_por_ave_faenada_kg" else _cerca(a2[k], 2 * v))
                p1, p2 = planta_alimento(a1["alimento_t_semana_plena"]), planta_alimento(a2["alimento_t_semana_plena"])
                errs += not _cerca(p2["t_h_requerida"], 2 * p1["t_h_requerida"])
                v1 = logistica(E, ds, nv)["viajes_alimento_granja_semana"]
                v2 = logistica(2 * E, ds, nv)["viajes_alimento_granja_semana"]
                errs += not (2 * v1 - 1 <= v2 <= 2 * v1)
    ok("U03 alimento lineal con la escala (viajes enteros: redondeo explicado y acotado)", errs == 0, f"{errs} errores")

    # U04 silos ∝ días de stock, ∝ 1/densidad
    errs = 0
    for E in ESCALAS:
        for modo in ("A_compra", "B_facon", "C_planta_propia"):
            s1 = almacenamiento(E, modo, dias_maiz=10, dias_soja=10, dias_alim_planta=2, dias_alim_granja=3)
            s2 = almacenamiento(E, modo, dias_maiz=20, dias_soja=20, dias_alim_planta=4, dias_alim_granja=6)
            s3 = almacenamiento(E, modo, dias_maiz=0, dias_soja=0, dias_alim_planta=0, dias_alim_granja=0)
            for k in ("granja_m3_brutos", "maiz_m3_brutos", "soja_m3_brutos", "alim_planta_m3_brutos"):
                errs += not _cerca(s2[k], 2 * s1[k])
                errs += not _cerca(s3[k], 0.0)
            sd, sb = almacenamiento(E, modo, dens_alim=0.5), almacenamiento(E, modo, dens_alim=0.6)
            errs += not _cerca(sd["granja_m3_brutos"] * 0.5, sb["granja_m3_brutos"] * 0.6)
            errs += not (s1["n_silos_planta"] is None or s1["n_silos_planta"] == 0)
        errs += not (almacenamiento(E, "C_planta_propia", n_mp_granel=3, n_tipos_alimento=4)
                     ["silos_minimos_segregacion_planta"] == 7)
        i1 = inventario_alimento(E, "C_planta_propia", dias={"maiz": 10})
        i2 = inventario_alimento(E, "C_planta_propia", dias={"maiz": 20})
        errs += not _cerca(i2["maiz"]["stock_cadena_t"], 2 * i1["maiz"]["stock_cadena_t"])
    ok("U04 silos e inventarios ∝ días de stock, ∝ 1/densidad; n_silos PENDIENTE sin volumen unitario", errs == 0,
       f"{errs} errores")

    # U05 opciones independientes; misma demanda física
    errs = 0
    for E in ESCALAS:
        A1, B, A2 = opcion_pollito(E, "A_compra"), opcion_pollito(E, "B_huevo_fertil"), opcion_pollito(E, "A_compra")
        errs += not (A1 == A2)
        errs += not _cerca(A1["pollitos_demanda_semana"], B["pollitos_demanda_semana"])
        errs += not (A1["posiciones_setter_propias"] == 0 and B["pollitos_comprados_semana"] == 0)
        errs += not (B["posiciones_setter_propias"] > 0 and B["posiciones_hatcher_propias"] > 0
                     and B["reproductoras_propias"] == 0)
        fa = [opcion_alimento(E, m) for m in OPCIONES["alimento"]]
        errs += not all(_cerca(x["alimento_demanda_t_semana"], fa[0]["alimento_demanda_t_semana"]) for x in fa)
        errs += not (fa[0]["capacidad_planta_propia_t_h"] == 0 and fa[1]["capacidad_planta_propia_t_h"] == 0
                     and fa[2]["capacidad_planta_propia_t_h"] > 0)
        gr = [opcion_granjas(E, m) for m in ("A_terceros", "B_integrados", "C_propias")]
        errs += not all(_cerca(sum(x[k] for k in ("plazas_terceros_independientes", "plazas_integrados", "plazas_propias")),
                               x["plazas_demanda"]) for x in gr)
        mx = opcion_granjas(E, "B+C_mixto", fraccion_propia=0.3)
        errs += not _cerca(mx["plazas_propias"] + mx["plazas_integrados"], mx["plazas_demanda"])
    ok("U05 opciones compra / integración parcial / total calculadas por separado; misma demanda física", errs == 0,
       f"{errs} errores")

    # U06 faltantes NO se rellenan
    errs = 0
    errs += not (pollitos(10000)["viajes_pollitos_semana"] is None)
    i0 = incubacion(52790)
    errs += not (i0["viajes_huevos_semana"] is None and i0["posiciones_setter_diseno"] is None
                 and i0["lote_nacimiento_pollitos"] is None)
    errs += not (incubacion(52790, cadencia=2)["pollitos_h_seleccion_vacunacion"] is None)
    errs += not (cadena_temporal()["lead_time_recepcion_a_entrega_d"] is None)
    errs += not (sincronizacion(10000, unidad="galpon")["plazas_unidad_colocacion"] is None)
    errs += not (sincronizacion(10000, galpon_m2=1800, origen_pollito="A_compra")["lote_nacimiento_pollitos"] is None)
    errs += not (sincronizacion(10000, unidad="granja", plazas_granja=30000)["galpones_por_granja_real"] is None)
    errs += not (logistica(10000, modo_alimento="C_planta_propia")["viajes_grano_semana"] is None)
    errs += not (silo(10, 5, None)["m3_brutos"] is None)
    errs += not (inventario_alimento(10000, "C_planta_propia")["material_en_proceso"]["stock_cadena_t"] is None)
    pend = [f for f in t.filas if f["estado"] == "PENDIENTE"]
    errs += not (len(pend) > 0 and all(f["valor"] == "" for f in pend))
    errs += not all(f["valor"] != "" for f in t.filas if f["estado"] == "CALCULADO")
    for fn in (lambda: incubacion(1000, fertilidad=0), lambda: incubacion(1000, descarte=1.0),
               lambda: incubacion(1000, cadencia=(0, 0)), lambda: planta_alimento(100, eficiencia=0),
               lambda: silo(10, 5, 0), lambda: viajes(10, 0), lambda: produccion(10000, 7),
               lambda: sincronizacion(10000, unidad="corral"), lambda: inventario_alimento(10000, "Z"),
               lambda: opcion_pollito(10000, "Z")):
        try:
            fn()
            errs += 1
        except (ErrorUpstream, KeyError):
            pass
    ok("U06 faltantes PENDIENTES (valor vacío), nunca rellenados; parámetros inválidos se rechazan",
       errs == 0, f"{errs} errores; {len(pend)} filas PENDIENTES")

    # U07 reproductoras no desde la arquitectura 1
    errs = 0
    for f in FASES_SIN_REPRODUCTORAS:
        errs += not (FASES[f]["pollito"] != "C_reproductoras")
        errs += not (reproductoras_fase_futura(1000, f)["reproductoras_hembras_postura_equiv"] == 0)
    errs += not all(FASES[f]["pollito"] != "C_reproductoras" for f in FASES if f != "FF")
    for f in t.filas:
        if f["bloque"] == "9_arquitecturas_referencia" and f["opcion"].split(":")[0] in FASES_SIN_REPRODUCTORAS:
            errs += not (f["valor"] == 0)
    ok("U07 reproductoras solo en la arquitectura futura (0 en F0 y F1)", errs == 0, f"{errs} errores")

    # U08 sin economía
    texto = " ".join(" ".join(str(v) for v in f.values()) for f in t.filas) + " ".join(COLUMNAS)
    hall = PALABRAS_ECONOMICAS.findall(texto)
    ok("U08 sin precios ni variables económicas en el CSV", not hall, f"hallazgos: {hall[:5]}")

    # U09 coherencia con 03
    errs = 0
    for E in ESCALAS:
        r = mp.calcular(**parametros_produccion(E))
        errs += not _cerca(pollitos(E)["pollitos_alojados_semana_plena"], r["pollitos_alojados_semana_plena"])
        errs += not _cerca(alimento(E)["alimento_t_anio"], r["alimento_t_anio"])
    ok("U09 pollitos y alimento reproducen exactamente 03 (importado, no recalculado)", errs == 0, f"{errs} errores")

    # U10 monotonía
    errs = 0
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        hs = [incubacion(d, n)["huevos_recibidos_semana"] for n in ("favorable", "medio", "desfavorable")]
        errs += not (hs[0] < hs[1] < hs[2])
        cs = [incubacion(d, margen_cap=m, cadencia=2)["posiciones_setter_diseno"] for m in MARGEN_CAPACIDAD]
        errs += not (cs[0] < cs[1] < cs[2])
        ps = [pollitos(E, nivel=n)["pollitos_alojados_semana_plena"] for n in NIVELES]
        errs += not (ps[0] < ps[1] < ps[2])
        errs += not (incubacion(d, ovoscopia=True, cadencia=2)["posiciones_hatcher_diseno"]
                     < incubacion(d, cadencia=2)["posiciones_hatcher_diseno"])
    ok("U10 monotonía (incubación, margen, mortalidad; ovoscopia reduce hatcher)", errs == 0, f"{errs} errores")

    # U11 unidades
    malas = {f["variable"] for f in t.filas if f["unidad"] not in UNIDADES_VALIDAS}
    ok("U11 toda variable tiene unidad válida", not malas, f"{sorted(malas)[:5]}")

    # U12 setter y hatcher dimensionados por separado
    errs = 0
    d = pollitos(10000)["pollitos_a_recibir_semana_plena"]
    for n in CADENCIAS:
        a = incubacion(d, cadencia=n)
        h0, s0 = D_HATCHER, D_SETTER
        try:
            D_HATCHER = 4.0
            b = incubacion(d, cadencia=n)
            errs += not (_cerca(b["posiciones_setter_diseno"], a["posiciones_setter_diseno"])
                         and b["posiciones_hatcher_diseno"] >= a["posiciones_hatcher_diseno"])
            D_HATCHER = h0
            D_SETTER = 19.0
            c = incubacion(d, cadencia=n)
            errs += not (c["posiciones_setter_diseno"] >= a["posiciones_setter_diseno"])
        finally:
            D_HATCHER, D_SETTER = h0, s0
        # hatcher se alimenta de TRANSFERIDOS (no de cargados): con ovoscopia cambia solo el hatcher
        o = incubacion(d, cadencia=n, ovoscopia=True)
        errs += not (_cerca(o["posiciones_setter_diseno"], a["posiciones_setter_diseno"])
                     and o["posiciones_hatcher_diseno"] < a["posiciones_hatcher_diseno"])
        errs += not _cerca(a["posiciones_fisicas_instaladas"], a["posiciones_setter_diseno"] + a["posiciones_hatcher_diseno"])
    errs += "posiciones_incubadora" in incubacion(d, cadencia=2)
    ok("U12 setter y hatcher dimensionados por separado (permanencias y flujos propios)", errs == 0, f"{errs} errores")

    # U13 conservación temporal y capacidad suficiente para la cadencia (simulación)
    errs = 0
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        for n, dias_c in CADENCIAS.items():
            inc = incubacion(d, cadencia=n)
            sim = simular_ocupacion(inc["lote_carga_huevos"], inc["huevos_transferidos_semana"] / n, dias_c)
            # media temporal simulada = ley de Little (conservación temporal)
            errs += not _cerca(sim["media_setter"], inc["posiciones_setter_continuo"], 1e-9)
            errs += not _cerca(sim["media_hatcher"], inc["posiciones_hatcher_continuo"], 1e-9)
            errs += not _cerca(sim["cargados_regimen_semana"], inc["huevos_cargados_semana"], 1e-9)
            errs += not _cerca(sim["transferidos_regimen_semana"], inc["huevos_transferidos_semana"], 1e-9)
            # la ocupación máxima nunca supera las posiciones de diseño
            errs += not (sim["max_setter"] <= inc["posiciones_setter_diseno"] + 1e-6)
            errs += not (sim["max_hatcher"] <= inc["posiciones_hatcher_diseno"] + 1e-6)
            # una carga por semana: setter = lote × techo((18 + 1) / 7) = 3 lotes
            if n == 1:
                errs += not _cerca(sim["max_setter"], inc["lote_carga_huevos"] * math.ceil(19 / 7))
    ok("U13 conservación temporal (media simulada = Little; cargas = demanda) y capacidad ≥ ocupación máxima",
       errs == 0, f"{errs} errores")

    # U14 recepción y carga son eventos distintos; incubación ≠ lead time
    errs = 0
    for da in (0, 3, 5, 7):
        c = cadena_temporal(da)
        errs += not (c["dia_recepcion_huevo"] == -da and c["dia_carga_setting"] == 0)
        errs += not (c["periodo_incubacion_d"] == D_SETTER + D_HATCHER == 21)
        errs += not _cerca(c["lead_time_recepcion_a_nacimiento_d"], da + 21)
        errs += not (c["lead_time_recepcion_a_entrega_d"] is None)
        errs += not (c["dia_recepcion_huevo"] < c["dia_carga_setting"] < c["dia_transferencia"] < c["dia_nacimiento"]
                     <= c["dia_llegada_granja_cota_inferior"] < c["dia_retiro_aves_cota_inferior"]
                     < c["dia_faena_cota_inferior"]) if da > 0 else 0
    c = cadena_temporal(5, h_nacimiento_a_granja=12)
    errs += not _cerca(c["lead_time_recepcion_a_entrega_d"], 5 + 21 + 0.5)
    errs += not _cerca(c["periodo_incubacion_d"], 21)
    ok("U14 recepción ≠ carga ≠ nacimiento ≠ entrega; incubación = 21 d independiente del almacenamiento",
       errs == 0, f"{errs} errores")

    # U15 tamaño de lote de nacimiento ≠ demanda media semanal
    errs = 0
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        for n in CADENCIAS:
            inc = incubacion(d, cadencia=n)
            errs += not _cerca(inc["lote_nacimiento_pollitos"] * n, d)
            errs += not ((inc["lote_nacimiento_pollitos"] < d) if n > 1 else _cerca(inc["lote_nacimiento_pollitos"], d))
    errs += not (incubacion(d)["lote_nacimiento_pollitos"] is None)   # sin cadencia no se deduce el lote
    ok("U15 lote de nacimiento = demanda / cadencia ≠ demanda media semanal; sin cadencia → PENDIENTE",
       errs == 0, f"{errs} errores")

    # U16 granja y galpón no son sinónimos
    errs = 0
    for E in ESCALAS:
        g = sincronizacion(E, unidad="galpon", galpon_m2=1800, cadencia=2)
        f1 = sincronizacion(E, unidad="granja", plazas_granja=30000, galpon_m2=1800, cadencia=2)
        f2 = sincronizacion(E, unidad="granja", galpones_por_granja=3, galpon_m2=1800, cadencia=2)
        errs += not _cerca(g["plazas_unidad_colocacion"], plazas_galpon(1800))
        errs += not (f1["plazas_unidad_colocacion"] == 30000 and f1["plazas_unidad_colocacion"] != g["plazas_unidad_colocacion"])
        errs += not _cerca(f2["plazas_unidad_colocacion"], 3 * g["plazas_unidad_colocacion"])
        errs += not _cerca(f1["galpones_por_granja_equivalente"], 30000 / plazas_galpon(1800))
        # identidad de capacidad: unidades requeridas = colocaciones/semana × ciclo / 7 / disponibilidad (03)
        p = parametros_produccion(E)
        errs += not _cerca(g["unidades_requeridas"], g["colocaciones_semana"] * (p["edad"] + p["vacio"]) / 7 / mp.DISPONIBILIDAD)
        errs += not (g["lotes_simultaneos_en_crianza"] < g["unidades_requeridas"])
    ok("U16 granja ≠ galpón (unidad de colocación explícita; plazas por separado; identidad de capacidad con 03)",
       errs == 0, f"{errs} errores")

    # U17 fertilidad e incubabilidad: elasticidad −1 ambas; variación ∝ rango
    errs = 0
    for E in ESCALAS:
        el = elasticidades(pollitos(E)["pollitos_a_recibir_semana_plena"])
        errs += not (abs(el["elasticidad_huevos_fertilidad"] + 1) < 1e-6 and abs(el["elasticidad_huevos_hof"] + 1) < 1e-6)
        errs += not ((el["rango_fertilidad_pct"] > el["rango_hof_pct"])
                     == (el["var_huevos_fertilidad_en_min_pct"] - el["var_huevos_fertilidad_en_max_pct"]
                         > el["var_huevos_hof_en_min_pct"] - el["var_huevos_hof_en_max_pct"]))
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        # simetría: el mismo cambio relativo en F o en H produce el mismo cambio en huevos
        errs += not _cerca(incubacion(d, fertilidad=0.92 * 0.95)["huevos_recibidos_semana"],
                           incubacion(d, hof=0.90 * 0.95)["huevos_recibidos_semana"])
    ok("U17 elasticidad de huevos = −1 para fertilidad y para incubabilidad; diferencias solo por rango", errs == 0,
       f"{errs} errores")

    # U18 alimento terminado no se mezcla con materias primas; U19 propio vs tercero separados
    e18 = e19 = 0
    for E in ESCALAS:
        cad = {}
        for arq in ARQUITECTURAS_INVENTARIO:
            inv = inventario_alimento(E, arq)
            e18 += not (set(inv) == set(CATEGORIAS_INVENTARIO))
            e18 += any(k.startswith("total") for k in inventario_plano(inv))
            for c, v in inv.items():
                if v["stock_cadena_t"] is None:
                    e19 += not (v["stock_propio_t"] is None and v["stock_tercero_referencial_t"] is None)
                    continue
                e19 += not _cerca(v["stock_propio_t"] + v["stock_tercero_referencial_t"], v["stock_cadena_t"])
                e19 += not (v["stock_propio_t"] == 0 or v["stock_tercero_referencial_t"] == 0)
                e19 += not ((v["propietario"] == "tercero") == (v["dias_tercero_validados"] is False))
                cad.setdefault(c, []).append(v["stock_cadena_t"])
        for c, vals in cad.items():   # el stock de la cadena por categoría no depende de quién lo posee
            e19 += not all(_cerca(x, vals[0]) for x in vals)
        a = inventario_alimento(E, "A_compra")
        e19 += not (a["maiz"]["stock_propio_t"] == 0 and a["alimento_terminado_granja"]["stock_propio_t"] > 0)
        c = inventario_alimento(E, "C_planta_propia")
        e19 += not all(v["stock_tercero_referencial_t"] in (0.0, None) for v in c.values())
        e18 += not _cerca(c["maiz"]["consumo_t_dia"] + c["harina_soja"]["consumo_t_dia"]
                          + c["micros_aceite_otros"]["consumo_t_dia"], c["alimento_terminado_granja"]["consumo_t_dia"])
    for f in t.filas:   # toda variable de inventario del CSV pertenece a UNA categoría; ningún total entre categorías
        if f["bloque"] == "7_inventarios":
            e18 += not (f["variable"].split("__")[0] in CATEGORIAS_INVENTARIO and "total" not in f["variable"])
    ok("U18 alimento terminado y materias primas en categorías separadas (sin totales mezclados)", e18 == 0,
       f"{e18} errores")
    ok("U19 stock propio vs en tercero separados; stock de la cadena por categoría igual en toda arquitectura",
       e19 == 0, f"{e19} errores")

    # U20 ninguna opción tratada como recomendación
    errs = 0
    for esl, ops in OPCIONES.items():
        errs += not all(v == "comparacion" for v in ops.values())
        errs += not (BENCHMARK[esl] in ops)
    errs += not all(f["orden_obligatorio"] is False for f in FASES.values())
    hall = PALABRAS_PREFERENCIA.findall(" ".join(" ".join(str(v) for v in f.values()) for f in t.filas)
                                        + " ".join(f["nombre"] for f in FASES.values()))
    errs += len(hall)
    ok("U20 todas las opciones = escenario de comparación; benchmark ≠ preferencia; sin 'caso base' ni orden obligatorio",
       errs == 0, f"{errs} errores {hall[:3]}")

    # U21 chequeo de sincronización coherente con sus banderas
    errs = 0
    for E in ESCALAS:
        for n in CADENCIAS:
            for gm2 in GALPON_M2:
                s = sincronizacion(E, unidad="galpon", galpon_m2=gm2, cadencia=n)
                errs += not (s["flag_cosecha_excede_referencia"] == int(s["dias_faena_por_unidad"] > DIAS_COSECHA_REFERENCIA + 1e-9))
                errs += not (s["flag_llenado_multinacimiento"] == int(s["nacimientos_por_colocacion"] > 1 + 1e-9))
                conflicto = s["flag_cosecha_excede_referencia"] or s["flag_llenado_multinacimiento"]
                errs += not (s["flag_llenado_multinacimiento"] == 0 or s["dispersion_edad_colocacion_d"] > 0)
                errs += not (s["estado_sincronizacion"].startswith("REQUIERE") == bool(conflicto))
                errs += not _cerca(s["unidades_cosechadas_por_dia_faena"] * s["aves_a_faena_por_unidad"], E)
    errs += not sincronizacion(20000, galpon_m2=1800).get("estado_sincronizacion", "").startswith("PENDIENTE")
    errs += not sincronizacion(2500, galpon_m2=1800, origen_pollito="A_compra")["estado_sincronizacion"].startswith("REQUIERE")
    ok("U21 sincronización: banderas coherentes; sin dato → PENDIENTE; cosecha × aves por unidad = faena diaria",
       errs == 0, f"{errs} errores")

    if verbose:
        for n, c, d in res:
            print(f"  [{'OK' if c else 'FALLA'}] {n} — {d}")
    return all(c for _, c, _ in res), res


# ------------------------------------------------------------------------------------------------
# 14. TABLAS PARA LOS DOCUMENTOS
# ------------------------------------------------------------------------------------------------
def fmt(x, dec=0):
    if x is None:
        return "PENDIENTE"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def md(fila):
    return "| " + " | ".join(str(x) for x in fila) + " |"


def imprimir_tablas():
    print("\n## A Cadena temporal (día 0 = carga)")
    for da in D_ALMACEN_HUEVO:
        c = cadena_temporal(da)
        print(md([da, c["dia_recepcion_huevo"], c["dia_transferencia"], c["dia_nacimiento"], c["periodo_incubacion_d"],
                  c["lead_time_recepcion_a_nacimiento_d"], fmt(c["lead_time_huevo_a_faena_d_cota_inferior"], 1)]))
    print("\n## B Setter / hatcher por cadencia (medio, margen 15 %)")
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        i0 = incubacion(d)
        print(md([fmt(E), fmt(i0["huevos_cargados_semana"]), fmt(i0["huevos_transferidos_semana"]),
                  fmt(i0["posiciones_setter_continuo"]), fmt(i0["posiciones_hatcher_continuo"]), fmt(i0["huevos_en_proceso_wip"])]))
        for n in CADENCIAS:
            i = incubacion(d, cadencia=n)
            print(md(["", n, fmt(i["lote_carga_huevos"]), fmt(i["lote_nacimiento_pollitos"]),
                      fmt(i["posiciones_setter_cadencia"]), fmt(i["posiciones_setter_diseno"]),
                      fmt(i["posiciones_hatcher_cadencia"]), fmt(i["posiciones_hatcher_diseno"]),
                      fmt(i["utilizacion_media_setter"] * 100, 0), fmt(i["utilizacion_media_hatcher"] * 100, 0)]))
    print("\n## C Sincronización: galpón (1.200/1.800/2.400 m²) y granja (15/30/60 mil), cadencia 1..5 (medio, 5 d)")
    for E in ESCALAS:
        for gm2 in GALPON_M2:
            row = [fmt(E), f"galpón {gm2}"]
            s = sincronizacion(E, unidad="galpon", galpon_m2=gm2, cadencia=2)
            row += [fmt(s["plazas_unidad_colocacion"]), fmt(s["colocaciones_semana"], 2), fmt(s["dias_faena_por_unidad"], 1),
                    fmt(s["lotes_simultaneos_en_crianza"], 1)]
            row += [fmt(sincronizacion(E, unidad="galpon", galpon_m2=gm2, cadencia=n)["nacimientos_por_colocacion"], 2)
                    for n in CADENCIAS]
            print(md(row))
        for pg in PLAZAS_GRANJA:
            row = [fmt(E), f"granja {pg}"]
            s = sincronizacion(E, unidad="granja", plazas_granja=pg, galpon_m2=1800, cadencia=2)
            row += [fmt(s["plazas_unidad_colocacion"]), fmt(s["colocaciones_semana"], 2), fmt(s["dias_faena_por_unidad"], 1),
                    fmt(s["lotes_simultaneos_en_crianza"], 1)]
            row += [fmt(sincronizacion(E, unidad="granja", plazas_granja=pg, galpon_m2=1800, cadencia=n)
                        ["nacimientos_por_colocacion"], 2) for n in CADENCIAS]
            print(md(row))
    print("plazas galpón:", [fmt(plazas_galpon(g)) for g in GALPON_M2], "equiv galpones/granja 30k (1800):",
          fmt(30000 / plazas_galpon(1800), 2))
    print("\n## D Elasticidades (10.000)")
    el = elasticidades(pollitos(10000)["pollitos_a_recibir_semana_plena"])
    for k, v in el.items():
        print(k, fmt(v * (1 if k.startswith("elas") else 100), 3 if k.startswith("elas") else 1))
    print("\n## E Planta de alimento: t/h (medio y desfavorable 6 d) por días×horas×eficiencia")
    for nv, ds in (("medio", 5), ("desfavorable", 6)):
        for E in ESCALAS:
            ts = alimento(E, ds, nv)["alimento_t_semana_plena"]
            row = [nv, ds, fmt(E), fmt(ts)]
            for dop in DIAS_OPERACION_PLANTA:
                for h in HORAS_DIA_PLANTA:
                    v = [planta_alimento(ts, dop, h, ef)["t_h_requerida"] for ef in (0.85, 0.75)]
                    row.append(f"{fmt(v[0], 1)}–{fmt(v[1], 1)}")
            print(md(row))
    print("\n## E2 Horas de producción/semana para la demanda propia (filas) con la capacidad requerida por (columnas) a 5 d × 8 h, ef 0,85")
    caps = {E: planta_alimento(alimento(E)["alimento_t_semana_plena"], 5, 8, 0.85)["t_h_requerida"] for E in ESCALAS}
    print("caps", {E: round(c, 2) for E, c in caps.items()})
    for E in ESCALAS:
        ts = alimento(E)["alimento_t_semana_plena"]
        print(md([fmt(E)] + [f"{fmt(horas_produccion_semana(ts, c)['horas_produccion_semana'])} h "
                             f"({fmt(horas_produccion_semana(ts, c)['fraccion_semana_168h'] * 100)} %)" for c in caps.values()]))
    print("\n## F Inventarios por categoría (medio, 5 d; días base)")
    for E in ESCALAS:
        for arq in ARQUITECTURAS_INVENTARIO:
            inv = inventario_alimento(E, arq)
            print(md([fmt(E), arq] + [f"{fmt(v['stock_propio_t'])}/{fmt(v['stock_tercero_referencial_t'])}"
                                      for v in inv.values()]))
        inv = inventario_alimento(E, "C_planta_propia")
        print(md([fmt(E), "cadena (t; días)"] + [f"{fmt(v['stock_cadena_t'])} ({v['dias_cobertura']})" for v in inv.values()]))


def main():
    t = construir()
    ruta = escribir_csv(t)
    pend = sum(1 for f in t.filas if f["estado"] == "PENDIENTE")
    print(f"CSV: {len(t.filas)} filas ({pend} PENDIENTES) escritas en {os.path.relpath(ruta, RAIZ)}")
    print("Pruebas automáticas:")
    todo_ok, _ = ejecutar_tests(t)
    if not todo_ok:
        sys.exit("ERROR: hay pruebas que fallan; no usar los resultados")
    if "--tablas" in sys.argv:
        imprimir_tablas()


if __name__ == "__main__":
    main()
