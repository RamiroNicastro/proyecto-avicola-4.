"""
Modelo físico del UPSTREAM avícola (sesión 14B): pollitos BB, incubación, alimento balanceado,
almacenamiento (silos), abastecimiento de granjas y necesidades logísticas, por escala.

Genera `escenarios_upstream.csv`, ejecuta las pruebas automáticas y, con `--tablas`, imprime las
tablas usadas en los .md de `14_alimento_balanceado/` y `15_incubacion/`.

    python3 modelo_upstream.py            # CSV + pruebas
    python3 modelo_upstream.py --tablas   # además, tablas para los documentos

ESTADO: ESCENARIOS de orden de magnitud (Fase 0). NO es diseño, NO elige fabricante, NO decide
integración, NO fija capacidad de faena (regla 9) y NO contiene precios ni costos (sin CAPEX/OPEX).
Las escalas 2.500 / 5.000 / 10.000 / 20.000 aves FAENADAS por día de faena son las mismas
escalas hipotéticas de 03 y 23 (no son la escala del proyecto).

Versión 1.0 · 2026-10-01 · IDs provisionales SUP-14B-## / DPV-14B-## / DEC-14B-## / FTE-14B-###
(registros centrales NO modificados; ver actualizaciones_gestion_14B.md).

------------------------------------------------------------------------------------------------
ORIGEN DE LOS DATOS
------------------------------------------------------------------------------------------------
Producción primaria: se IMPORTA 03_produccion_primaria/modelo_escenarios_produccion.py (v1.1) y
se usa `mp.calcular` sin recalcular nada: pollitos alojados, aves cargadas, aves faenadas,
alimento (t/año, semana plena, promedio, fases), capacidad de alojamiento, m² de galpón,
inventario de aves y alimento de un ciclo de crianza. Perfil MEDIO (47 d, 2,9 kg) y desempeño
favorable / medio / desfavorable (SUP-026 a SUP-028).

Unidades: aves, pollitos, huevos (unidades); kg; t = 1.000 kg; m³; h; d; semanas (52,14/año).
Separador decimal del CSV: punto. Bases (regla 14): pollitos = pollitos BB ALOJADOS en granja;
huevos = huevos fértiles (incubables) en unidades; alimento = alimento terminado entregado a
granja (base del FCR de campo de 03); materias primas = t de ingrediente tal cual.

------------------------------------------------------------------------------------------------
1. POLLITOS BB (demanda; viene de 03)
------------------------------------------------------------------------------------------------
  pollitos_alojados_semana_plena = mp.calcular(...)            (dimensiona contratos y capacidad)
  margen_mortalidad_pollitos     = pollitos_alojados − aves_faenadas   (granja + transporte)
  margen_mortalidad_pct          = pollitos_alojados / aves_faenadas − 1
  pollitos_a_recibir             = pollitos_alojados × (1 + margen_pedido)   (SUP-14B-01; base 0)
  alojamientos_semana            = pollitos_a_recibir_semana / plazas_por_granja  (barrido de 13)
  viajes_pollitos_semana         = techo(pollitos_a_recibir / cap_camion_pollitos)  PENDIENTE sin cap
  antelacion_fisica_minima_d     = dias_almacenamiento_huevo + dias_incubadora + dias_nacedora
                                   (el huevo debe cargarse en incubadora ≥ 21 d antes de la entrega)

------------------------------------------------------------------------------------------------
2-3. INCUBACIÓN (cálculo inverso; huevo fértil → almacenamiento → incubadora → nacedora →
     selección → vacunación → expedición). Todos los parámetros son SUPUESTOS (SUP-14B-02/03/04)
------------------------------------------------------------------------------------------------
  pollitos_vendibles_sem   = pollitos_a_recibir_sem                      (expedición = demanda)
  pollitos_nacidos_sem     = vendibles / (1 − descarte_seleccion)
  huevos_incubados_sem     = nacidos / (fertilidad × incubabilidad_fertiles × (1 − perdida_transferencia))
  huevos_a_nacedora_sem    = incubados × (1 − perdida_transferencia) × (fertilidad si ovoscopia, si no 1)
  huevos_recibidos_sem     = incubados / (1 − perdida_recepcion_almacen)
  incubabilidad_s_cargados = fertilidad × incubabilidad_fertiles × (1 − perdida_transferencia)
  CAPACIDAD (con margen de capacidad, SUP-14B-05; ocupación = ley de Little):
  capacidad_semanal_carga  = huevos_incubados_sem × (1 + margen)            (huevos/semana)
  posiciones_incubadora    = huevos_incubados_sem × (d_incubadora + d_limpieza_inc) / 7 × (1 + margen)
  posiciones_nacedora      = huevos_a_nacedora_sem × (d_nacedora + d_limpieza_nac) / 7 × (1 + margen)
  capacidad_almacen_huevo  = huevos_recibidos_sem × d_almacenamiento / 7 × (1 + margen)
  pollitos_por_nacimiento  = vendibles_sem / nacimientos_semana            (si nacimientos dado)
  pollitos_h_seleccion_vac = pollitos_por_nacimiento / horas_ventana_proceso (si ambos dados)
  Conservación (test U01): huevos_recibidos → incubados → fértiles → nacidos → vendibles se
  recalcula hacia adelante y debe devolver la demanda con error ≤ 1e-9.

  Opción C (reproductoras, SOLO fase futura; nunca fase 0 ni 1 — test U07):
  reproductoras_equivalentes = vendibles_sem / pollitos_por_reproductora_semana (ESTIMACIÓN de 03
  §4.2: ~3,6; a verificar DPV-045). Recría, machos, reposición y granjas de reproductoras: PENDIENTE.

------------------------------------------------------------------------------------------------
4-5. ALIMENTO (viene de 03) y categorías de materias primas (NO es fórmula)
------------------------------------------------------------------------------------------------
  t_dia_entrega_7d = t_semana_plena / 7 ;  t_dia_promedio_calendario = t_anio / 365
  materia_prima_t  = alimento_t × inclusión (rango mín–máx de 03 alimentacion.md §4; punto
                     ilustrativo SUP-032 60 % maíz / 30 % harina de soja). Categorías: maíz, harina
                     de soja, aceite, minerales, vitaminas (premezcla), otros (aminoácidos, enzimas,
                     aditivos, sustitutos). Recetas reales = nutricionista (DEC-14B-03).

------------------------------------------------------------------------------------------------
6. PLANTA DE ALIMENTO (conceptual; capacidad requerida, sin fabricante)
------------------------------------------------------------------------------------------------
  t_h_requerida = t_semana_plena × factor_pico / (dias_operacion × horas_dia × eficiencia) × (1 + margen)
  (eficiencia = fracción de horas programadas con producción efectiva: cambios de fórmula,
   limpieza, mantenimiento; SUP-14B-07). La planta podría elaborar también para terceros: no se
   supone (capacidad ociosa = capacidad instalada − requerida; se informa, no se vende).

------------------------------------------------------------------------------------------------
7. SILOS (SOLO desde variables; no hay silo estándar)
------------------------------------------------------------------------------------------------
  t_almacenadas_i = consumo_t_dia_i × dias_stock_i
  m3_utiles_i     = t_almacenadas_i / densidad_aparente_i
  m3_brutos_i     = m3_utiles_i / factor_llenado
  silos_minimos_por_segregacion = n_materias_primas_granel + n_tipos_alimento_terminado
  n_silos = techo(m3_brutos_i / volumen_unitario) → PENDIENTE si volumen_unitario es None (no se
  inventa un silo estándar; test U04 exige que los m³ dependan de los días de stock).

------------------------------------------------------------------------------------------------
8-10. MAKE OR BUY, FASES, DEPENDENCIAS
------------------------------------------------------------------------------------------------
  Pollito : A compra de pollito | B huevo fértil comprado + incubación propia | C reproductoras
  Alimento: A compra de alimento | B façon (materias primas propias, elaboración de terceros) |
            C planta propia
  Granjas : A pollo vivo de terceros | B integrados | C granjas propias
  La DEMANDA FÍSICA (pollitos, alimento, plazas) es la misma en todas las opciones; cambia QUÉ
  capacidad física debe tener la empresa. Cada opción se calcula por separado (test U05).
  Fases 0 / 1 / 2 / 3 / futura = ARQUITECTURA DE ANÁLISIS (SUP-14B-12), no secuencia recomendada.
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

VERSION = "1.0"
FECHA = "2026-10-01"
FUENTE = "14_alimento_balanceado/modelo_upstream.py"
TOL = 1e-9
SEMANAS_ANIO = mp.SEMANAS_ANIO

# ------------------------------------------------------------------------------------------------
# 1. PARÁMETROS (importados cuando existen; propios con ID provisional SUP-14B-##)
# ------------------------------------------------------------------------------------------------
ESCALAS = list(mp.PLANTAS_AVES_FAENADAS_DIA)       # 2.500 / 5.000 / 10.000 / 20.000 (escenarios)
CALENDARIOS = dict(mp.DIAS_FAENA_ANIO)             # {5: 250, 6: 300} (SUP-025)
PERFIL = "medio"                                   # 47 d, 2,9 kg (SUP-027)
NIVELES = tuple(mp.DESEMPENO)                      # favorable / medio / desfavorable (SUP-026)

# Pollitos
MARGEN_PEDIDO_BASE = 0.0                           # SUP-14B-01: pollitos extra pedidos sobre los alojados
MARGEN_PEDIDO_BARRIDO = (0.0, 0.01, 0.02)          # SUP-14B-01: barrido, sin fuente
PLAZAS_GRANJA = (15000, 30000, 60000)              # de 13 (PLAZAS_GRANJA; 03 [ESTIMACIÓN] 15-30 mil)
CAP_CAMION_POLLITOS = None                         # PENDIENTE (DPV-047, DPV-084)
CAP_CAMION_POLLITOS_BARRIDO = (20000, 40000, 80000)  # SUP-096: barrido ilustrativo, NO capacidad

# Incubación: niveles de SUPUESTO (SUP-14B-02 / 03). Referencia de pico de un manual de
# reproductoras: fertilidad ≥ 96,7 % e incubabilidad de fértiles 93,5 % EN PICO (FTE-14B-001
# [PVDP]); los promedios de vida del lote son menores y dependen de la edad de las reproductoras.
# HOS resultante (medio) ≈ 82 %, dentro del 80-85 % usado por 03 (modelos_integracion.md §4.2).
INCUBACION = {
    "favorable":    {"fertilidad": 0.95, "hof": 0.92, "perdida_alm": 0.005, "perdida_tr": 0.003, "descarte": 0.005},
    "medio":        {"fertilidad": 0.92, "hof": 0.90, "perdida_alm": 0.010, "perdida_tr": 0.005, "descarte": 0.010},
    "desfavorable": {"fertilidad": 0.88, "hof": 0.87, "perdida_alm": 0.020, "perdida_tr": 0.010, "descarte": 0.020},
}
# Tiempos (SUP-14B-04): incubación total ~21 d (18 incubadora + 3 nacedora; la transferencia con
# vacunación in ovo se cita a 18-19 d, FTE-14B-002 [PVDP]); limpieza por carga: sin fuente.
D_INCUBADORA = 18.0
D_NACEDORA = 3.0
D_LIMPIEZA_INC = 1.0
D_LIMPIEZA_NAC = 1.0
D_ALMACEN_HUEVO = (3, 5, 7)                        # barrido; óptimo 3-6 d citado (FTE-14B-001 [PVDP])
OVOSCOPIA_RETIRA_INFERTILES = False                # base: no se retiran infértiles al transferir
MARGEN_CAPACIDAD = (0.10, 0.15, 0.20)              # SUP-14B-05 (reserva de diseño, no óptimo)
MARGEN_CAPACIDAD_BASE = 0.15
NACIMIENTOS_SEMANA = (1, 2, 3, 4)                  # SUP-14B-06: barrido operativo, sin fuente
HORAS_VENTANA_PROCESO = (6, 10)                    # SUP-14B-06: horas para seleccionar/vacunar/expedir un nacimiento
# Opción C (fase futura): pollitos por reproductora alojada por semana (03 §4.2 [ESTIMACIÓN], DPV-045)
POLLITOS_REPRODUCTORA_SEMANA = 3.6

# Alimento: categorías de materias primas (fracción del alimento, rango de 03 alimentacion.md §4)
# NO es fórmula; el punto ilustrativo solo respeta SUP-032 (60 % maíz, 30 % harina de soja).
COMPOSICION = {   # categoría: (mín, máx, punto ilustrativo o None)
    "maiz":       (0.55, 0.65, 0.60),
    "harina_soja": (0.25, 0.35, 0.30),
    "aceite":     (0.01, 0.05, None),
    "minerales":  (0.023, 0.035, None),   # fosfatos 1-2 % + carbonato ~1 % + sal/bicarbonato 0,3-0,5 %
    "vitaminas":  (0.002, 0.005, None),   # premezcla vitamínico-mineral
    "otros":      (0.002, 0.013, None),   # aminoácidos 0,2-0,8 % + enzimas/aditivos < 0,5 %
}
RESTO_ILUSTRATIVO = "aceite+minerales+vitaminas+otros"   # 10 % agregado en el punto SUP-032

# Planta de alimento (SUP-14B-07): parámetros operativos de ESCENARIO
DIAS_OPERACION_PLANTA = (5, 6)
HORAS_DIA_PLANTA = (8, 16)
EFICIENCIA_PLANTA = (0.75, 0.85)
FACTOR_PICO_ALIMENTO = 1.0         # semana plena ya es el ritmo nominal; estacionalidad: PENDIENTE
N_TIPOS_ALIMENTO = (3, 4)          # inicio / crecimiento / terminación (+ retiro), 03 §3

# Silos (SUP-14B-09 / 10): densidades aparentes y días de stock = VARIABLES
DENSIDAD_T_M3 = {                  # t/m³ aparente; [PVDP] FTE-14B-003 (extractos, no leídos)
    "maiz": (0.72,),               # maíz desgranado ~0,72
    "harina_soja": (0.56, 0.60, 0.67),
    "alimento": (0.55, 0.60, 0.65),  # alimento terminado (pellet/harina): barrido, sin dato propio
}
FACTOR_LLENADO = 0.90              # SUP-14B-09: fracción útil del volumen bruto
DIAS_STOCK = {                     # SUP-14B-10: barridos de días calendario de consumo
    "maiz": (7, 15, 30),
    "harina_soja": (7, 15),
    "alimento_planta": (1, 2, 3),
    "alimento_granja": (2, 3, 5),
}
N_MP_GRANEL = (2, 3, 4)            # materias primas a granel (maíz, harina de soja, sorgo/expeller...)
VOLUMEN_UNITARIO_SILO_M3 = None    # PENDIENTE: no se inventa un silo estándar

# Logística (capacidades de ESCENARIO de SUP-096; sin elección explícita → PENDIENTE)
CAP_GRANELERO_T = 28.0             # alimento a granel a granjas ([ESTIMACIÓN] 03; DPV-084)
CAP_CAMION_GRANO_BARRIDO = (25.0, 28.0, 30.0)  # SUP-14B-13: barrido ilustrativo, no capacidad legal
CAP_CAMION_HUEVOS = None           # PENDIENTE (DPV-14B-09)

# Fases (SUP-14B-12): arquitectura conceptual; NO es la secuencia recomendada
FASES = {
    "F0": {"nombre": "Fase 0: compra de pollito + alimento comprado + granjas de terceros + façon posible",
           "pollito": "A_compra", "alimento": "A_compra", "granjas": "A_terceros", "faena": "facon_posible"},
    "F1": {"nombre": "Fase 1: planta de faena propia; upstream comprado o integrado parcialmente",
           "pollito": "A_compra", "alimento": "B_facon", "granjas": "B_integrados", "faena": "propia"},
    "F2": {"nombre": "Fase 2: más granjas e integración",
           "pollito": "A_compra", "alimento": "B_facon", "granjas": "B_integrados+C_propias", "faena": "propia"},
    "F3": {"nombre": "Fase 3: alimento y/o incubación propios si el volumen lo justifica",
           "pollito": "B_huevo_fertil", "alimento": "C_planta_propia", "granjas": "B_integrados+C_propias",
           "faena": "propia"},
    "FF": {"nombre": "Fase futura: reproductoras / genética solo si existe justificación",
           "pollito": "C_reproductoras", "alimento": "C_planta_propia", "granjas": "B_integrados+C_propias",
           "faena": "propia"},
}
FASES_SIN_REPRODUCTORAS = ("F0", "F1")   # test U07

PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|precios|costo|costos|capex|opex|ebitda|van|tir|"
                                 r"payback|margen_bruto|ingreso|ingresos|rentabilidad)\b|\$", re.IGNORECASE)
UNIDADES_VALIDAS = {"aves", "pollitos", "huevos", "posiciones", "reproductoras", "t", "t/h", "kg", "m³",
                    "m²", "%", "ratio", "d", "h", "viajes", "alojamientos", "granjas", "silos", "pollitos/h",
                    "texto"}


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
def pollitos(E, dias_semana=5, nivel="medio", margen_pedido=MARGEN_PEDIDO_BASE, plazas_granja=None,
             cap_camion=CAP_CAMION_POLLITOS):
    _frac("margen_pedido", margen_pedido)
    _pos("plazas_granja", plazas_granja)
    pr = produccion(E, dias_semana, nivel)
    sem, anio = pr["pollitos_alojados_semana_plena"], pr["pollitos_alojados_anio"]
    fae_sem, fae_anio = pr["aves_faenadas_semana_plena"], pr["aves_faenadas_anio"]
    recibir_sem = sem * (1 + margen_pedido)
    out = {
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
        "alojamientos_semana": None if plazas_granja is None else recibir_sem / plazas_granja,
        "granjas_equivalentes": None if plazas_granja is None else pr["capacidad_alojamiento_pollitos"] / plazas_granja,
        "capacidad_alojamiento_pollitos": pr["capacidad_alojamiento_pollitos"],
        "m2_galpon": pr["m2_galpon"],
        "inventario_aves_ritmo_pleno": pr["inventario_aves_ritmo_pleno"],
        "antelacion_fisica_minima_d_min": min(D_ALMACEN_HUEVO) + D_INCUBADORA + D_NACEDORA,
        "antelacion_fisica_minima_d_max": max(D_ALMACEN_HUEVO) + D_INCUBADORA + D_NACEDORA,
    }
    return out


# ------------------------------------------------------------------------------------------------
# 5. INCUBACIÓN (cálculo inverso y capacidad)
# ------------------------------------------------------------------------------------------------
def incubacion(pollitos_vendibles_sem, nivel="medio", margen_cap=MARGEN_CAPACIDAD_BASE, dias_almacen=5,
               nacimientos_semana=None, horas_ventana=None, ovoscopia=OVOSCOPIA_RETIRA_INFERTILES,
               **override):
    """Pollitos vendibles/semana → huevos y capacidad instalada. `override` permite cambiar
    fertilidad, hof, perdida_alm, perdida_tr, descarte (variables, no datos)."""
    p = dict(INCUBACION[nivel], **override)
    F = _frac("fertilidad", p["fertilidad"], incluye_cero=False)
    H = _frac("hof", p["hof"], incluye_cero=False)
    pa, pt, ds = (_frac("perdida_alm", p["perdida_alm"]), _frac("perdida_tr", p["perdida_tr"]),
                  _frac("descarte", p["descarte"]))
    _frac("margen_cap", margen_cap)
    if dias_almacen < 0:
        raise ErrorUpstream("días de almacenamiento < 0")
    _pos("nacimientos_semana", nacimientos_semana)
    _pos("horas_ventana", horas_ventana)
    vend = pollitos_vendibles_sem
    nacidos = vend / (1 - ds)
    hos = F * H * (1 - pt)
    incubados = nacidos / hos
    fertiles = incubados * F
    a_nacedora = incubados * (1 - pt) * (F if ovoscopia else 1.0)
    recibidos = incubados / (1 - pa)
    k = 1 + margen_cap
    por_nac = None if nacimientos_semana is None else vend / nacimientos_semana
    return {
        "nivel_incubacion": nivel, "fertilidad": F, "incubabilidad_fertiles": H,
        "perdida_recepcion_almacen": pa, "perdida_transferencia": pt, "descarte_seleccion": ds,
        "incubabilidad_sobre_cargados": hos,
        "pollitos_vendibles_semana": vend,
        "pollitos_descarte_semana": nacidos - vend,
        "pollitos_nacidos_semana": nacidos,
        "huevos_fertiles_semana": fertiles,
        "huevos_infertiles_semana": incubados - fertiles,
        "huevos_incubados_semana": incubados,
        "huevos_a_nacedora_semana": a_nacedora,
        "huevos_descarte_recepcion_semana": recibidos - incubados,
        "huevos_recibidos_semana": recibidos,
        "huevos_por_pollito_vendible": recibidos / vend,
        "huevos_recibidos_anio": recibidos * SEMANAS_ANIO,   # ritmo pleno todo el año (cota superior)
        "margen_capacidad": margen_cap,
        "capacidad_semanal_carga_huevos": incubados * k,
        "posiciones_incubadora": incubados * (D_INCUBADORA + D_LIMPIEZA_INC) / 7 * k,
        "posiciones_nacedora": a_nacedora * (D_NACEDORA + D_LIMPIEZA_NAC) / 7 * k,
        "capacidad_almacen_huevos": recibidos * dias_almacen / 7 * k,
        "dias_almacen_huevo": dias_almacen,
        "pollitos_por_nacimiento": por_nac,
        "pollitos_h_seleccion_vacunacion": None if (por_nac is None or horas_ventana is None) else por_nac / horas_ventana,
        "viajes_huevos_semana": viajes(recibidos, CAP_CAMION_HUEVOS),
    }


def reproductoras_fase_futura(pollitos_vendibles_sem, fase, pollitos_reproductora_semana=POLLITOS_REPRODUCTORA_SEMANA):
    """Opción C. Solo se calcula en la fase futura; en cualquier otra fase devuelve 0 (no se
    asumen reproductoras). Recría, machos y reposición: PENDIENTES (DPV-045)."""
    if FASES[fase]["pollito"] != "C_reproductoras":
        return {"reproductoras_hembras_postura_equiv": 0.0, "estado": "NO APLICA en esta fase"}
    _pos("pollitos_reproductora_semana", pollitos_reproductora_semana)
    return {"reproductoras_hembras_postura_equiv": pollitos_vendibles_sem / pollitos_reproductora_semana,
            "estado": "ESTIMACIÓN de 03 (DPV-045); recría, machos y reposición PENDIENTES"}


# ------------------------------------------------------------------------------------------------
# 6. ALIMENTO
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
    out["mp_resto_t_anio_ilustrativo"] = t_anio * (1 - COMPOSICION["maiz"][2] - COMPOSICION["harina_soja"][2])
    return out


def planta_alimento(t_semana, dias_op=5, horas_dia=8, eficiencia=0.85, margen=MARGEN_CAPACIDAD_BASE,
                    factor_pico=FACTOR_PICO_ALIMENTO):
    """Capacidad de producción requerida (t/h de alimento terminado). Sin fabricante."""
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


# ------------------------------------------------------------------------------------------------
# 7. SILOS (solo desde variables)
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
    """Almacenamiento físico según la opción de alimento. A compra: solo silos de granja.
    B façon: granja + (granos propios: en la fábrica del tercero o en acopio; se informan las t,
    no el silo propio). C planta propia: granos + alimento terminado + granja."""
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
    r["stock_total_t"] = r["granja_t"] + r["maiz_t"] + r["soja_t"] + r["alim_planta_t"]
    return r


# ------------------------------------------------------------------------------------------------
# 8. OPCIONES (make or buy): capacidad física PROPIA requerida por opción, calculada por separado
# ------------------------------------------------------------------------------------------------
def opcion_pollito(E, modo, dias_semana=5, nivel="medio", nivel_inc="medio", margen_cap=MARGEN_CAPACIDAD_BASE):
    po = pollitos(E, dias_semana, nivel)
    dem = po["pollitos_a_recibir_semana_plena"]
    base = {"modo": modo, "pollitos_demanda_semana": dem, "pollitos_comprados_semana": 0.0,
            "huevos_comprados_semana": 0.0, "capacidad_semanal_carga_huevos_propia": 0.0,
            "posiciones_incubadora_propias": 0.0, "posiciones_nacedora_propias": 0.0,
            "reproductoras_propias": 0.0}
    if modo == "A_compra":
        base["pollitos_comprados_semana"] = dem
    elif modo in ("B_huevo_fertil", "C_reproductoras"):
        inc = incubacion(dem, nivel_inc, margen_cap)
        base.update({"capacidad_semanal_carga_huevos_propia": inc["capacidad_semanal_carga_huevos"],
                     "posiciones_incubadora_propias": inc["posiciones_incubadora"],
                     "posiciones_nacedora_propias": inc["posiciones_nacedora"]})
        if modo == "B_huevo_fertil":
            base["huevos_comprados_semana"] = inc["huevos_recibidos_semana"]
        else:
            base["reproductoras_propias"] = reproductoras_fase_futura(dem, "FF")["reproductoras_hembras_postura_equiv"]
    else:
        raise ErrorUpstream(f"modo de pollito desconocido: {modo}")
    return base


def opcion_alimento(E, modo, dias_semana=5, nivel="medio", dias_op=5, horas=16, eficiencia=0.85,
                    margen=MARGEN_CAPACIDAD_BASE):
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
    elif modo == "C_planta_propia":
        base["materias_primas_compradas_t_semana"] = t_sem
        base["capacidad_planta_propia_t_h"] = planta_alimento(t_sem, dias_op, horas, eficiencia, margen)["t_h_requerida"]
    else:
        raise ErrorUpstream(f"modo de alimento desconocido: {modo}")
    return base


def opcion_granjas(E, modo, dias_semana=5, nivel="medio", fraccion_propia=0.0):
    _frac("fraccion_propia", fraccion_propia) if fraccion_propia < 1 else None
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
    elif modo == "B+C_mixto":
        base.update({"plazas_propias": plazas * fraccion_propia, "m2_propios": m2 * fraccion_propia,
                     "plazas_integrados": plazas * (1 - fraccion_propia)})
    else:
        raise ErrorUpstream(f"modo de granjas desconocido: {modo}")
    return base


# ------------------------------------------------------------------------------------------------
# 9. LOGÍSTICA UPSTREAM
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
# 10. CSV (formato largo; sin precios)
# ------------------------------------------------------------------------------------------------
COLUMNAS = ["bloque", "escala_aves_faenadas_dia", "dias_faena_semana", "nivel_produccion", "opcion",
            "parametros", "variable", "valor", "unidad", "periodo", "clasificacion", "estado", "fuente", "nota"]

UNIDAD = [  # (prefijo/sufijo, unidad) — primera coincidencia
    ("pollitos_h", "pollitos/h"), ("posiciones", "posiciones"), ("reproductoras", "reproductoras"),
    ("huevos_por_pollito", "ratio"), ("huevos", "huevos"), ("pollitos", "pollitos"), ("aves", "aves"),
    ("mortalidad", "aves"), ("t_h", "t/h"), ("_m3", "m³"), ("m3_", "m³"), ("m2", "m²"), ("plazas", "pollitos"),
    ("_kg", "kg"), ("_pct", "ratio"), ("margen", "ratio"), ("utilizacion", "ratio"), ("eficiencia", "ratio"),
    ("fertilidad", "ratio"), ("incubabilidad", "ratio"), ("perdida", "ratio"), ("descarte", "ratio"),
    ("viajes", "viajes"), ("alojamientos", "alojamientos"), ("granjas", "granjas"), ("silos", "silos"),
    ("antelacion", "d"), ("dias", "d"), ("horas", "h"), ("_t", "t"), ("t_", "t"),
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
    if "semana" in var or "nacimiento" in var:
        return "semana plena"
    if "dia" in var:
        return "día"
    return "instantáneo / capacidad"


class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, ds, nivel, opcion, params, d, clasif, fuente, nota="", claves=None):
        for k in (claves or d):
            v = d[k]
            if isinstance(v, str):
                continue
            estado = "PENDIENTE" if v is None else "CALCULADO"
            self.filas.append({
                "bloque": bloque, "escala_aves_faenadas_dia": E, "dias_faena_semana": ds, "nivel_produccion": nivel,
                "opcion": opcion, "parametros": params, "variable": k,
                "valor": "" if v is None else (round(v, 4) if isinstance(v, float) else v),
                "unidad": unidad(k), "periodo": periodo(k), "clasificacion": clasif if v is not None else "[PENDIENTE DE VALIDACIÓN]",
                "estado": estado, "fuente": fuente, "nota": nota})


def construir():
    t = Tabla()
    F03 = "03 modelo_escenarios_produccion.py v1.1 (importado)"
    for E in ESCALAS:
        for ds in CALENDARIOS:
            for nv in NIVELES:
                # 1. Pollitos
                po = pollitos(E, ds, nv)
                t.add("1_pollitos", E, ds, nv, "-", "margen_pedido=0", po, "[ESTIMACIÓN]", F03,
                      "Demanda física de pollitos; igual para todas las opciones de abastecimiento",
                      claves=[k for k in po if k not in ("viajes_pollitos_semana", "alojamientos_semana",
                                                         "granjas_equivalentes")])
                for mpd in MARGEN_PEDIDO_BARRIDO[1:]:
                    q = pollitos(E, ds, nv, margen_pedido=mpd)
                    t.add("1_pollitos", E, ds, nv, "-", f"margen_pedido={mpd} (SUP-14B-01)", q, "[SUPUESTO]",
                          FUENTE, "Sensibilidad del pedido; no es mortalidad",
                          claves=["pollitos_a_recibir_semana_plena", "pollitos_a_recibir_anio"])
                for pl in PLAZAS_GRANJA:
                    q = pollitos(E, ds, nv, plazas_granja=pl)
                    t.add("1_pollitos_entregas", E, ds, nv, "-", f"plazas_granja={pl} (barrido 13)", q, "[ESTIMACIÓN]",
                          FUENTE, "Granja llenada en un alojamiento (todo dentro-todo fuera)",
                          claves=["alojamientos_semana", "granjas_equivalentes"])
                t.add("1_pollitos_entregas", E, ds, nv, "-", "cap_camion_pollitos=None", po, "[PENDIENTE DE VALIDACIÓN]",
                      FUENTE, "Sin capacidad validada (DPV-047, DPV-084)", claves=["viajes_pollitos_semana"])
                for cp in CAP_CAMION_POLLITOS_BARRIDO:
                    q = pollitos(E, ds, nv, cap_camion=cp)
                    t.add("1_pollitos_entregas", E, ds, nv, "-", f"cap_camion_pollitos={cp} (SUP-096 barrido)", q,
                          "[SUPUESTO]", FUENTE, "Barrido ilustrativo, NO capacidad", claves=["viajes_pollitos_semana"])
                # 2-3. Incubación (opción B; también C) — nivel de incubación × margen
                for ni in INCUBACION:
                    inc = incubacion(po["pollitos_a_recibir_semana_plena"], ni)
                    t.add("2_incubacion", E, ds, nv, "B_huevo_fertil", f"nivel_incubacion={ni}; margen_cap=0.15; "
                          f"dias_almacen=5", inc, "[SUPUESTO]", FUENTE,
                          "Cálculo inverso; parámetros SUP-14B-02/03/04/05 (no datos)",
                          claves=[k for k in inc if k not in ("pollitos_por_nacimiento", "pollitos_h_seleccion_vacunacion",
                                                              "viajes_huevos_semana")])
                    for mc in (MARGEN_CAPACIDAD[0], MARGEN_CAPACIDAD[2]):
                        q = incubacion(po["pollitos_a_recibir_semana_plena"], ni, mc)
                        t.add("2_incubacion", E, ds, nv, "B_huevo_fertil", f"nivel_incubacion={ni}; margen_cap={mc}",
                              q, "[SUPUESTO]", FUENTE, "Sensibilidad del margen de capacidad (SUP-14B-05)",
                              claves=["capacidad_semanal_carga_huevos", "posiciones_incubadora", "posiciones_nacedora",
                                      "capacidad_almacen_huevos"])
                inc = incubacion(po["pollitos_a_recibir_semana_plena"])
                for n in NACIMIENTOS_SEMANA:
                    for h in HORAS_VENTANA_PROCESO:
                        q = incubacion(po["pollitos_a_recibir_semana_plena"], nacimientos_semana=n, horas_ventana=h)
                        t.add("2_incubacion_expedicion", E, ds, nv, "B_huevo_fertil",
                              f"nacimientos_semana={n}; horas_ventana={h} (SUP-14B-06)", q, "[SUPUESTO]", FUENTE,
                              "Sala de pollitos, selección, vacunación y expedición por nacimiento",
                              claves=["pollitos_por_nacimiento", "pollitos_h_seleccion_vacunacion"])
                for da in D_ALMACEN_HUEVO:
                    q = incubacion(po["pollitos_a_recibir_semana_plena"], dias_almacen=da)
                    t.add("2_incubacion_almacen", E, ds, nv, "B_huevo_fertil", f"dias_almacen={da}", q, "[SUPUESTO]",
                          FUENTE, "Óptimo 3-6 d citado (FTE-14B-001 [PVDP])", claves=["capacidad_almacen_huevos"])
                t.add("2_incubacion_logistica", E, ds, nv, "B_huevo_fertil", "cap_camion_huevos=None", inc,
                      "[PENDIENTE DE VALIDACIÓN]", FUENTE, "DPV-14B-09", claves=["viajes_huevos_semana"])
                rep = reproductoras_fase_futura(po["pollitos_a_recibir_semana_plena"], "FF")
                t.add("2_reproductoras_fase_futura", E, ds, nv, "C_reproductoras", "pollitos_reproductora_semana=3.6",
                      rep, "[ESTIMACIÓN]", "03 modelos_integracion.md §4.2",
                      "SOLO fase futura; recría, machos y reposición PENDIENTES (DPV-045)")
                # 4-5. Alimento
                al = alimento(E, ds, nv)
                t.add("4_alimento", E, ds, nv, "-", "perfil medio", al, "[ESTIMACIÓN]", F03,
                      "Demanda física de alimento; igual para compra, façon o planta propia",
                      claves=[k for k in al if not k.startswith("mp_")])
                t.add("5_materias_primas", E, ds, nv, "-", "rangos 03 alimentacion.md §4; punto SUP-032", al,
                      "[ESTIMACIÓN]", "03 alimentacion.md §4 (FTE-160 [PVDP])",
                      "NO es fórmula: categorías y rangos; recetas = nutricionista",
                      claves=[k for k in al if k.startswith("mp_") and al[k] is not None])
                # 6. Planta de alimento (opción C)
                for dop in DIAS_OPERACION_PLANTA:
                    for h in HORAS_DIA_PLANTA:
                        for ef in EFICIENCIA_PLANTA:
                            pa = planta_alimento(al["alimento_t_semana_plena"], dop, h, ef)
                            t.add("6_planta_alimento", E, ds, nv, "C_planta_propia",
                                  f"dias_op={dop}; horas={h}; eficiencia={ef}; margen=0.15", pa, "[SUPUESTO]", FUENTE,
                                  "Capacidad requerida de alimento terminado; sin fabricante (SUP-14B-07)",
                                  claves=["t_dia_operacion", "t_h_neta", "t_h_requerida", "capacidad_ociosa_t_semana",
                                          "utilizacion"])
                # 7. Silos por opción y barrido de días de stock / densidades (solo nivel medio)
                if nv == "medio":
                    for modo in ("A_compra", "B_facon", "C_planta_propia"):
                        for i, (dm, dsj, dap, dg) in enumerate(zip(DIAS_STOCK["maiz"], (7, 15, 15),
                                                                   DIAS_STOCK["alimento_planta"],
                                                                   DIAS_STOCK["alimento_granja"])):
                            for dal in DENSIDAD_T_M3["alimento"]:
                                st = almacenamiento(E, modo, ds, nv, dm, dsj, dap, dg, 0.72, 0.60, dal)
                                t.add("7_silos", E, ds, nv, modo,
                                      f"dias_stock maiz={dm} soja={dsj} alim_planta={dap} granja={dg}; "
                                      f"dens maiz=0.72 soja=0.60 alim={dal}; llenado=0.9", st, "[SUPUESTO]",
                                      FUENTE, "m³ desde variables; n_silos PENDIENTE (sin silo estándar)")
                        for dsoja in (DENSIDAD_T_M3["harina_soja"][0], DENSIDAD_T_M3["harina_soja"][2]):
                            if modo != "A_compra":
                                st = almacenamiento(E, modo, ds, nv, dens_soja=dsoja)
                                t.add("7_silos", E, ds, nv, modo, f"dias_stock base; dens soja={dsoja}", st, "[SUPUESTO]",
                                      FUENTE, "Sensibilidad de densidad de harina de soja", claves=["soja_m3_brutos"])
                # 8. Opciones make-or-buy (calculadas por separado)
                for modo in ("A_compra", "B_huevo_fertil", "C_reproductoras"):
                    t.add("8_opcion_pollito", E, ds, nv, modo, "nivel_inc=medio; margen_cap=0.15",
                          opcion_pollito(E, modo, ds, nv), "[ESTIMACIÓN]", FUENTE,
                          "C solo como fase futura" if modo.startswith("C") else "")
                for modo in ("A_compra", "B_facon", "C_planta_propia"):
                    t.add("8_opcion_alimento", E, ds, nv, modo, "dias_op=5; horas=16; eficiencia=0.85; margen=0.15",
                          opcion_alimento(E, modo, ds, nv), "[ESTIMACIÓN]", FUENTE)
                for modo in ("A_terceros", "B_integrados", "C_propias"):
                    t.add("8_opcion_granjas", E, ds, nv, modo, "-", opcion_granjas(E, modo, ds, nv), "[ESTIMACIÓN]",
                          FUENTE, "Plazas y m² = 03; cambia quién las aporta, no cuántas son")
                # 10. Logística upstream
                for modo in ("A_compra", "B_facon", "C_planta_propia"):
                    lg = logistica(E, ds, nv, modo)
                    t.add("10_logistica", E, ds, nv, modo, "granelero=28 t (SUP-096); cap_grano=None; cap_pollitos=None",
                          lg, "[SUPUESTO]", FUENTE, "Sin capacidad explícita → PENDIENTE")
                    if modo != "A_compra":
                        for cg in CAP_CAMION_GRANO_BARRIDO:
                            lg2 = logistica(E, ds, nv, modo, cap_grano=cg)
                            t.add("10_logistica", E, ds, nv, modo, f"cap_grano={cg} (SUP-14B-13 barrido)", lg2,
                                  "[SUPUESTO]", FUENTE, "Barrido ilustrativo, no capacidad legal",
                                  claves=["viajes_grano_semana"])
    # Fases (texto → filas con valor numérico de capacidad propia, escala 10.000 / 5 d / medio como ejemplo)
    for f, d in FASES.items():
        for E in ESCALAS:
            rep = reproductoras_fase_futura(pollitos(E)["pollitos_a_recibir_semana_plena"], f)
            t.add("9_fases", E, 5, "medio", f"{f}: pollito={d['pollito']}; alimento={d['alimento']}; granjas={d['granjas']}",
                  d["nombre"], rep, "[SUPUESTO]", FUENTE,
                  "Arquitectura conceptual (SUP-14B-12); NO secuencia recomendada")
    return t


def escribir_csv(t, ruta=None):
    ruta = ruta or os.path.join(AQUI, "escenarios_upstream.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNAS, lineterminator="\n")
        w.writeheader()
        w.writerows(t.filas)
    return ruta


# ------------------------------------------------------------------------------------------------
# 11. PRUEBAS AUTOMÁTICAS
# ------------------------------------------------------------------------------------------------
def ejecutar_tests(t=None, verbose=True):
    res = []

    def ok(nombre, cond, detalle=""):
        res.append((nombre, bool(cond), detalle))

    t = t or construir()
    # U01 conservación de pollitos y huevos (hacia adelante devuelve la demanda) y orden de la cadena
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
                    cadena = [inc["huevos_recibidos_semana"], inc["huevos_incubados_semana"], inc["huevos_fertiles_semana"],
                              inc["pollitos_nacidos_semana"], inc["pollitos_vendibles_semana"],
                              po["pollitos_alojados_semana_plena"], po["aves_cargadas_semana_plena"],
                              po["aves_faenadas_semana_plena"]]
                    errs += not _cerca(fwd, po["pollitos_a_recibir_semana_plena"])
                    # vendibles = alojados × (1 + margen_pedido) ≥ alojados (igual con margen 0); el resto, estricto
                    errs += not all((a >= b) if i == 4 else (a > b) for i, (a, b) in enumerate(zip(cadena, cadena[1:])))
                    errs += not _cerca(inc["huevos_recibidos_semana"], inc["huevos_incubados_semana"]
                                       + inc["huevos_descarte_recepcion_semana"])
                    errs += not _cerca(inc["huevos_incubados_semana"], inc["huevos_fertiles_semana"]
                                       + inc["huevos_infertiles_semana"])
                    errs += not _cerca(inc["pollitos_nacidos_semana"], inc["pollitos_vendibles_semana"]
                                       + inc["pollitos_descarte_semana"])
                errs += not _cerca(po["margen_mortalidad_pollitos_anio"],
                                   po["mortalidad_granja_aves_anio"] + po["mortalidad_transporte_aves_anio"])
    ok("U01 conservación pollitos/huevos y cadena huevos > incubados > fértiles > nacidos > vendibles ≥ alojados > cargadas > faenadas",
       errs == 0, f"{errs} errores")

    # U02 capacidad instalada suficiente (incubación y planta de alimento)
    errs = 0
    for E in ESCALAS:
        dem = pollitos(E)["pollitos_a_recibir_semana_plena"]
        for ni in INCUBACION:
            for mc in MARGEN_CAPACIDAD:
                inc = incubacion(dem, ni, mc)
                cap_inc = inc["posiciones_incubadora"] / ((D_INCUBADORA + D_LIMPIEZA_INC) / 7)
                cap_nac = inc["posiciones_nacedora"] / ((D_NACEDORA + D_LIMPIEZA_NAC) / 7)
                errs += not (cap_inc >= inc["huevos_incubados_semana"] * (1 + mc) - 1e-6)
                errs += not (cap_nac >= inc["huevos_a_nacedora_semana"] - 1e-6)
                errs += not (inc["capacidad_semanal_carga_huevos"] >= inc["huevos_incubados_semana"])
                errs += not (inc["capacidad_almacen_huevos"] >= inc["huevos_recibidos_semana"] * 5 / 7)
        t_sem = alimento(E)["alimento_t_semana_plena"]
        for dop in DIAS_OPERACION_PLANTA:
            for h in HORAS_DIA_PLANTA:
                for ef in EFICIENCIA_PLANTA:
                    pa = planta_alimento(t_sem, dop, h, ef)
                    errs += not (pa["t_h_requerida"] * dop * h * ef >= t_sem - 1e-9)
                    errs += not (0 < pa["utilizacion"] <= 1)
                    errs += not _cerca(pa["utilizacion"], 1 / 1.15)
    ok("U02 capacidad instalada ≥ requerida (incubadora, nacedora, almacén, planta de alimento)", errs == 0, f"{errs} errores")

    # U03 alimento escala linealmente (salvo enteros: viajes) y lo intensivo no cambia
    errs = 0
    for E in ESCALAS:
        for ds in CALENDARIOS:
            for nv in NIVELES:
                a1, a2 = alimento(E, ds, nv), alimento(2 * E, ds, nv)
                for k, v in a1.items():
                    if v is None:
                        continue
                    if k == "alimento_por_ave_faenada_kg":
                        errs += not _cerca(a2[k], v)
                    else:
                        errs += not _cerca(a2[k], 2 * v)
                p1, p2 = planta_alimento(a1["alimento_t_semana_plena"]), planta_alimento(a2["alimento_t_semana_plena"])
                errs += not _cerca(p2["t_h_requerida"], 2 * p1["t_h_requerida"])
                # viajes: enteros, NO lineales exactos (explicación: techo) pero acotados
                v1 = logistica(E, ds, nv)["viajes_alimento_granja_semana"]
                v2 = logistica(2 * E, ds, nv)["viajes_alimento_granja_semana"]
                errs += not (2 * v1 - 1 <= v2 <= 2 * v1)
    ok("U03 alimento lineal con la escala (viajes enteros: no lineales por redondeo, acotados)", errs == 0, f"{errs} errores")

    # U04 silos dependen de los días de stock (monótonos y proporcionales) y de la densidad (inversa)
    errs = 0
    for E in ESCALAS:
        for modo in ("A_compra", "B_facon", "C_planta_propia"):
            s1 = almacenamiento(E, modo, dias_maiz=10, dias_soja=10, dias_alim_planta=2, dias_alim_granja=3)
            s2 = almacenamiento(E, modo, dias_maiz=20, dias_soja=20, dias_alim_planta=4, dias_alim_granja=6)
            s3 = almacenamiento(E, modo, dias_maiz=0, dias_soja=0, dias_alim_planta=0, dias_alim_granja=0)
            for k in ("granja_m3_brutos", "maiz_m3_brutos", "soja_m3_brutos", "alim_planta_m3_brutos", "stock_total_t"):
                errs += not _cerca(s2[k], 2 * s1[k])
                errs += not _cerca(s3[k], 0.0)
            sd = almacenamiento(E, modo, dens_alim=0.5)
            sb = almacenamiento(E, modo, dens_alim=0.6)
            errs += not _cerca(sd["granja_m3_brutos"] * 0.5, sb["granja_m3_brutos"] * 0.6)
            errs += not (s1["n_silos_planta"] is None or s1["n_silos_planta"] == 0)   # sin volumen unitario
        c = almacenamiento(E, "C_planta_propia", n_mp_granel=3, n_tipos_alimento=4)
        errs += not (c["silos_minimos_segregacion_planta"] == 7)
        errs += not (almacenamiento(E, "A_compra")["maiz_t"] == 0)
    ok("U04 silos ∝ días de stock, ∝ 1/densidad, 0 sin stock; n_silos PENDIENTE sin volumen unitario", errs == 0,
       f"{errs} errores")

    # U05 compra vs integración son escenarios independientes: la demanda física es la misma y
    # calcular una opción no altera otra; la capacidad propia de la opción de compra es 0
    errs = 0
    for E in ESCALAS:
        A1 = opcion_pollito(E, "A_compra")
        B = opcion_pollito(E, "B_huevo_fertil")
        A2 = opcion_pollito(E, "A_compra")
        errs += not (A1 == A2)
        errs += not _cerca(A1["pollitos_demanda_semana"], B["pollitos_demanda_semana"])
        errs += not (A1["posiciones_incubadora_propias"] == 0 and B["pollitos_comprados_semana"] == 0)
        errs += not (B["posiciones_incubadora_propias"] > 0 and B["reproductoras_propias"] == 0)
        fa = [opcion_alimento(E, m) for m in ("A_compra", "B_facon", "C_planta_propia")]
        errs += not all(_cerca(x["alimento_demanda_t_semana"], fa[0]["alimento_demanda_t_semana"]) for x in fa)
        errs += not (fa[0]["capacidad_planta_propia_t_h"] == 0 and fa[1]["capacidad_planta_propia_t_h"] == 0
                     and fa[2]["capacidad_planta_propia_t_h"] > 0)
        errs += not _cerca(fa[0]["alimento_comprado_t_semana"], fa[2]["materias_primas_compradas_t_semana"])
        gr = [opcion_granjas(E, m) for m in ("A_terceros", "B_integrados", "C_propias")]
        errs += not all(_cerca(sum(x[k] for k in ("plazas_terceros_independientes", "plazas_integrados", "plazas_propias")),
                               x["plazas_demanda"]) for x in gr)
        mx = opcion_granjas(E, "B+C_mixto", fraccion_propia=0.3)
        errs += not _cerca(mx["plazas_propias"] + mx["plazas_integrados"], mx["plazas_demanda"])
        # la elección de alimento no cambia pollitos ni granjas
        errs += not (logistica(E, modo_alimento="A_compra")["viajes_alimento_granja_semana"]
                     == logistica(E, modo_alimento="C_planta_propia")["viajes_alimento_granja_semana"])
    ok("U05 opciones compra / integración parcial / total calculadas por separado; misma demanda física", errs == 0,
       f"{errs} errores")

    # U06 datos faltantes NO se rellenan: sin capacidad, volumen o parámetro → None/PENDIENTE
    errs = 0
    errs += not (pollitos(10000)["viajes_pollitos_semana"] is None)
    errs += not (incubacion(52790)["viajes_huevos_semana"] is None)
    errs += not (incubacion(52790)["pollitos_por_nacimiento"] is None)
    errs += not (incubacion(52790, nacimientos_semana=2)["pollitos_h_seleccion_vacunacion"] is None)
    errs += not (logistica(10000, modo_alimento="C_planta_propia")["viajes_grano_semana"] is None)
    errs += not (logistica(10000, cap_granelero=None)["viajes_alimento_granja_semana"] is None)
    errs += not (silo(10, 5, None)["m3_brutos"] is None)
    errs += not (almacenamiento(10000, "C_planta_propia")["n_silos_planta"] is None)
    errs += not (VOLUMEN_UNITARIO_SILO_M3 is None and CAP_CAMION_POLLITOS is None and CAP_CAMION_HUEVOS is None)
    pend = [f for f in t.filas if f["estado"] == "PENDIENTE"]
    errs += not (len(pend) > 0 and all(f["valor"] == "" for f in pend))
    errs += not all(f["valor"] != "" for f in t.filas if f["estado"] == "CALCULADO")
    for fn in (lambda: incubacion(1000, fertilidad=0), lambda: incubacion(1000, descarte=1.0),
               lambda: planta_alimento(100, eficiencia=0), lambda: silo(10, 5, 0), lambda: viajes(10, 0),
               lambda: pollitos(10000, plazas_granja=0), lambda: produccion(10000, 7)):
        try:
            fn()
            errs += 1
        except ErrorUpstream:
            pass
    ok("U06 faltantes quedan PENDIENTES (valor vacío), nunca rellenados; parámetros inválidos se rechazan",
       errs == 0, f"{errs} errores; {len(pend)} filas PENDIENTES")

    # U07 reproductoras no se asumen desde fase 1
    errs = 0
    for f in FASES_SIN_REPRODUCTORAS:
        errs += not (FASES[f]["pollito"] != "C_reproductoras")
        for E in ESCALAS:
            errs += not (reproductoras_fase_futura(1000, f)["reproductoras_hembras_postura_equiv"] == 0)
    errs += not (FASES["FF"]["pollito"] == "C_reproductoras")
    errs += not all(FASES[f]["pollito"] != "C_reproductoras" for f in FASES if f != "FF")
    for f in t.filas:
        if f["bloque"] == "9_fases" and f["opcion"].split(":")[0] in FASES_SIN_REPRODUCTORAS:
            errs += not (f["valor"] == 0)
    ok("U07 reproductoras solo en fase futura (0 en F0 y F1; ninguna otra fase las incluye)", errs == 0, f"{errs} errores")

    # U08 sin precios ni economía en el CSV
    texto = " ".join(" ".join(str(v) for v in f.values()) for f in t.filas) + " ".join(COLUMNAS)
    hall = PALABRAS_ECONOMICAS.findall(texto)
    ok("U08 sin precios ni variables económicas en el CSV", not hall, f"hallazgos: {hall[:5]}")

    # U09 coherencia con 03 (no se recalcula): pollitos y alimento idénticos a mp.calcular
    errs = 0
    for E in ESCALAS:
        r = mp.calcular(**parametros_produccion(E))
        errs += not _cerca(pollitos(E)["pollitos_alojados_semana_plena"], r["pollitos_alojados_semana_plena"])
        errs += not _cerca(alimento(E)["alimento_t_anio"], r["alimento_t_anio"])
    ok("U09 pollitos y alimento reproducen exactamente 03 (importado, no recalculado)", errs == 0, f"{errs} errores")

    # U10 monotonía: peor incubación → más huevos; más margen → más capacidad; más mortalidad → más pollitos
    errs = 0
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        hs = [incubacion(d, n)["huevos_recibidos_semana"] for n in ("favorable", "medio", "desfavorable")]
        errs += not (hs[0] < hs[1] < hs[2])
        cs = [incubacion(d, margen_cap=m)["posiciones_incubadora"] for m in MARGEN_CAPACIDAD]
        errs += not (cs[0] < cs[1] < cs[2])
        ps = [pollitos(E, nivel=n)["pollitos_alojados_semana_plena"] for n in NIVELES]
        errs += not (ps[0] < ps[1] < ps[2])
        ov = incubacion(d, ovoscopia=True)["posiciones_nacedora"] < incubacion(d)["posiciones_nacedora"]
        errs += not ov
    ok("U10 monotonía (incubación, margen, mortalidad, ovoscopia reduce nacedora)", errs == 0, f"{errs} errores")

    # U11 unidades válidas y períodos declarados
    malas = {f["unidad"] for f in t.filas if f["unidad"] not in UNIDADES_VALIDAS or f["unidad"] == "texto"}
    ok("U11 toda variable tiene unidad válida (ninguna 'texto')", not malas, f"{malas}")

    if verbose:
        for n, c, d in res:
            print(f"  [{'OK' if c else 'FALLA'}] {n} — {d}")
    return all(c for _, c, _ in res), res


# ------------------------------------------------------------------------------------------------
# 12. TABLAS PARA LOS DOCUMENTOS
# ------------------------------------------------------------------------------------------------
def fmt(x, dec=0):
    if x is None:
        return "PENDIENTE"
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def md(fila):
    return "| " + " | ".join(str(x) for x in fila) + " |"


def imprimir_tablas():
    print("\n## T1 Pollitos por escala (5 d/sem; favorable / medio / desfavorable)")
    for E in ESCALAS:
        rr = [pollitos(E, 5, n) for n in NIVELES]
        j = lambda k, dec=0, f=1: " / ".join(fmt(r[k] * f, dec) for r in rr)
        print(md([fmt(E), fmt(rr[0]["aves_faenadas_semana_plena"]), j("pollitos_alojados_semana_plena"),
                  j("pollitos_alojados_semana_promedio"), j("pollitos_alojados_anio"),
                  j("margen_mortalidad_pollitos_semana_plena"), j("margen_mortalidad_pct", 1, 100)]))
    print("\n## T1b 6 d/sem (medio)")
    for E in ESCALAS:
        r = pollitos(E, 6)
        print(md([fmt(E), fmt(r["pollitos_alojados_semana_plena"]), fmt(r["pollitos_alojados_anio"])]))
    print("\n## T2 Entregas de pollitos (medio, 5 d): alojamientos/semana y granjas equivalentes por tamaño de granja")
    for E in ESCALAS:
        row = [fmt(E)]
        for pl in PLAZAS_GRANJA:
            r = pollitos(E, plazas_granja=pl)
            row += [fmt(r["alojamientos_semana"], 1), fmt(r["granjas_equivalentes"], 1)]
        for cp in CAP_CAMION_POLLITOS_BARRIDO:
            row.append(fmt(pollitos(E, cap_camion=cp)["viajes_pollitos_semana"]))
        print(md(row))
    print("\n## T3 Incubación (opción B; nivel medio; margen 15 %; 5 d de almacenamiento)")
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        i = incubacion(d)
        print(md([fmt(E), fmt(d), fmt(i["pollitos_nacidos_semana"]), fmt(i["huevos_fertiles_semana"]),
                  fmt(i["huevos_incubados_semana"]), fmt(i["huevos_recibidos_semana"]),
                  fmt(i["huevos_por_pollito_vendible"], 3), fmt(i["capacidad_semanal_carga_huevos"]),
                  fmt(i["posiciones_incubadora"]), fmt(i["posiciones_nacedora"]), fmt(i["capacidad_almacen_huevos"])]))
    print("\n## T3b Huevos recibidos/semana por nivel de incubación (fav / medio / desf) y HOS")
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        ii = [incubacion(d, n) for n in INCUBACION]
        print(md([fmt(E)] + [fmt(i["huevos_recibidos_semana"]) for i in ii]
                 + [" / ".join(fmt(i["incubabilidad_sobre_cargados"] * 100, 1) for i in ii)]))
    print("\n## T3c Sensibilidad incubación a 10.000 (medio)")
    d = pollitos(10000)["pollitos_a_recibir_semana_plena"]
    base = incubacion(d)
    for nombre, kw in [("Base", {}), ("Fertilidad 0,85", {"fertilidad": 0.85}), ("Fertilidad 0,96", {"fertilidad": 0.96}),
                       ("Incubabilidad fértiles 0,85", {"hof": 0.85}), ("Incubabilidad fértiles 0,935", {"hof": 0.935}),
                       ("Descarte selección 3 %", {"descarte": 0.03}), ("Pérdida recepción 3 %", {"perdida_alm": 0.03}),
                       ("Margen capacidad 0 %", {"margen_cap": 0.0}), ("Margen capacidad 25 %", {"margen_cap": 0.25})]:
        mc = kw.pop("margen_cap", MARGEN_CAPACIDAD_BASE)
        i = incubacion(d, margen_cap=mc, **kw)
        print(md([nombre, fmt(i["huevos_recibidos_semana"]),
                  f"{(i['huevos_recibidos_semana'] / base['huevos_recibidos_semana'] - 1) * 100:+.1f} %".replace(".", ","),
                  fmt(i["posiciones_incubadora"]), fmt(i["posiciones_nacedora"])]))
    print("\n## T3d Expedición por nacimiento (medio): pollitos por nacimiento y pollitos/h con 6 y 10 h")
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        row = [fmt(E)]
        for n in NACIMIENTOS_SEMANA:
            i6 = incubacion(d, nacimientos_semana=n, horas_ventana=6)
            i10 = incubacion(d, nacimientos_semana=n, horas_ventana=10)
            row.append(f"{fmt(i6['pollitos_por_nacimiento'])} ({fmt(i10['pollitos_h_seleccion_vacunacion'])}–"
                       f"{fmt(i6['pollitos_h_seleccion_vacunacion'])}/h)")
        print(md(row))
    print("\n## T3e Reproductoras equivalentes (SOLO fase futura; ESTIMACIÓN 03)")
    for E in ESCALAS:
        d = pollitos(E)["pollitos_a_recibir_semana_plena"]
        print(md([fmt(E), fmt(reproductoras_fase_futura(d, "FF")["reproductoras_hembras_postura_equiv"])]))
    print("\n## T4 Alimento por escala (5 d; fav / medio / desf)")
    for E in ESCALAS:
        aa = [alimento(E, 5, n) for n in NIVELES]
        j = lambda k, dec=0: " / ".join(fmt(a[k], dec) for a in aa)
        print(md([fmt(E), j("alimento_t_dia_entrega_7d", 1), j("alimento_t_dia_promedio_calendario", 1),
                  j("alimento_t_semana_plena"), j("alimento_t_semana_promedio"), j("alimento_t_anio"),
                  j("alimento_ciclo_crianza_t")]))
    print("\n## T4b 6 d/sem medio")
    for E in ESCALAS:
        a = alimento(E, 6)
        print(md([fmt(E), fmt(a["alimento_t_dia_entrega_7d"], 1), fmt(a["alimento_t_semana_plena"]), fmt(a["alimento_t_anio"])]))
    print("\n## T5 Materias primas t/año (medio, 5 d): rango mín–máx (punto SUP-032)")
    for E in ESCALAS:
        a = alimento(E)
        row = [fmt(E)]
        for k in COMPOSICION:
            s = f"{fmt(a[f'mp_{k}_t_anio_min'])}–{fmt(a[f'mp_{k}_t_anio_max'])}"
            if a[f"mp_{k}_t_anio_ilustrativo"] is not None:
                s += f" ({fmt(a[f'mp_{k}_t_anio_ilustrativo'])})"
            row.append(s)
        print(md(row))
    print("\n## T6 Planta de alimento: t/h requeridas (medio, 5 d faena; margen 15 %) por días×horas×eficiencia")
    for E in ESCALAS:
        ts = alimento(E)["alimento_t_semana_plena"]
        row = [fmt(E), fmt(ts)]
        for dop in DIAS_OPERACION_PLANTA:
            for h in HORAS_DIA_PLANTA:
                v = [planta_alimento(ts, dop, h, ef)["t_h_requerida"] for ef in EFICIENCIA_PLANTA]
                row.append(f"{fmt(min(v), 1)}–{fmt(max(v), 1)}")
        print(md(row))
    print("\n## T6b Planta: t/h requeridas en escenario desfavorable 6 d faena (cota alta)")
    for E in ESCALAS:
        ts = alimento(E, 6, "desfavorable")["alimento_t_semana_plena"]
        print(md([fmt(E), fmt(ts), fmt(planta_alimento(ts, 5, 8, 0.75)["t_h_requerida"], 1),
                  fmt(planta_alimento(ts, 6, 16, 0.85)["t_h_requerida"], 1)]))
    print("\n## T7 Almacenamiento (medio, 5 d): t y m³ brutos; maíz 15 d, soja 15 d, alim planta 2 d, granja 3 d; dens 0,72/0,60/0,60")
    for E in ESCALAS:
        for modo in ("A_compra", "B_facon", "C_planta_propia"):
            s = almacenamiento(E, modo)
            print(md([fmt(E), modo, fmt(s["granja_t"]), fmt(s["granja_m3_brutos"]), fmt(s["maiz_t"]), fmt(s["maiz_m3_brutos"]),
                      fmt(s["soja_t"]), fmt(s["soja_m3_brutos"]), fmt(s["alim_planta_t"]), fmt(s["alim_planta_m3_brutos"]),
                      fmt(s["stock_total_t"]), s["silos_minimos_segregacion_planta"], fmt(s["n_silos_planta"])]))
    print("\n## T7b Barrido de días de stock (planta propia, 10.000): m³ brutos totales planta (maíz+soja+alim)")
    for dm in DIAS_STOCK["maiz"]:
        for dap in DIAS_STOCK["alimento_planta"]:
            s = almacenamiento(10000, "C_planta_propia", dias_maiz=dm, dias_soja=min(dm, 15), dias_alim_planta=dap)
            print(md([dm, min(dm, 15), dap, fmt(s["maiz_m3_brutos"] + s["soja_m3_brutos"] + s["alim_planta_m3_brutos"])]))
    print("\n## T8 Logística upstream (medio, 5 d)")
    for E in ESCALAS:
        lg = logistica(E, modo_alimento="C_planta_propia", cap_grano=28.0)
        print(md([fmt(E), fmt(alimento(E)["alimento_t_semana_plena"]), lg["viajes_alimento_granja_semana"],
                  fmt(lg["viajes_alimento_granja_dia_7d"], 1), fmt(lg["granos_t_semana_entrada"]), lg["viajes_grano_semana"],
                  fmt(incubacion(pollitos(E)["pollitos_a_recibir_semana_plena"])["huevos_recibidos_semana"])]))
    print("\n## T9 Capacidad propia por opción (medio, 5 d)")
    for E in ESCALAS:
        row = [fmt(E)]
        for m in ("A_compra", "B_huevo_fertil", "C_reproductoras"):
            o = opcion_pollito(E, m)
            row.append(f"{fmt(o['posiciones_incubadora_propias'])} pos.; {fmt(o['reproductoras_propias'])} repr.")
        for m in ("A_compra", "B_facon", "C_planta_propia"):
            row.append(fmt(opcion_alimento(E, m)["capacidad_planta_propia_t_h"], 1))
        print(md(row))
    print("\n## T10 Dependencias: factor respecto de 2.500 (medio, 5 d)")
    b = {"pollitos": pollitos(2500)["pollitos_alojados_semana_plena"], "alimento": alimento(2500)["alimento_t_anio"],
         "plazas": pollitos(2500)["capacidad_alojamiento_pollitos"],
         "camiones": logistica(2500)["viajes_alimento_granja_semana"],
         "silos": almacenamiento(2500, "C_planta_propia")["maiz_m3_brutos"],
         "inv": pollitos(2500)["inventario_aves_ritmo_pleno"]}
    for E in ESCALAS:
        print(md([fmt(E), fmt(pollitos(E)["pollitos_alojados_semana_plena"] / b["pollitos"], 2),
                  fmt(alimento(E)["alimento_t_anio"] / b["alimento"], 2),
                  fmt(pollitos(E)["capacidad_alojamiento_pollitos"] / b["plazas"], 2),
                  f"{logistica(E)['viajes_alimento_granja_semana']} ({fmt(logistica(E)['viajes_alimento_granja_semana'] / b['camiones'], 2)})",
                  fmt(almacenamiento(E, "C_planta_propia")["maiz_m3_brutos"] / b["silos"], 2),
                  fmt(pollitos(E)["inventario_aves_ritmo_pleno"] / b["inv"], 2)]))


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
