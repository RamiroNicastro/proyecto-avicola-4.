#!/usr/bin/env python3
"""
MODELO PRELIMINAR DE UTILITIES — versión 1.0 (2026-09-30, sesión 09C)
=====================================================================

AGUA INDUSTRIAL -> EFLUENTES -> ENERGÍA ELÉCTRICA -> AGUA CALIENTE/VAPOR -> FRÍO INDUSTRIAL
-> CONGELADO -> RESPALDO, para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo
(o cualquier valor con --aves-dia).

ESTADO: órdenes de magnitud de PREFACTIBILIDAD. NO selecciona equipos, NO calcula CAPEX ni OPEX,
NO asigna precios, NO elige tecnología de tratamiento, refrigerante ni fuente térmica, NO elige
ubicación. Ninguna cifra es un dato de campo argentino.

FUENTE DE VERDAD DE LA MASA: 23_plan_expansion/escenarios_escala.csv (modelo de escala v1.1, que a
su vez integra el balance de masa v1.1 y subproductos v1.0). Este modelo LEE ese CSV y NO lo
modifica ni recalcula el balance: toma kg/ave (valor / escala, lineal por el test T01 del modelo de
escala) de: comestible (peso comercial), masa biológica comestible, agua retenida en producto, agua
incorporada, sangre recuperada y drenada, plumas, vísceras, cabezas, garras, menudencias,
sólidos a retirar y masa a efluente o pérdida. El inventario reproduce exactamente las filas del
bloque `inventario` de ese CSV (test U07).

Uso
---
    python3 11_agua_efluentes/modelo_utilities.py                 # tests + CSV
    python3 11_agua_efluentes/modelo_utilities.py --solo-tests     # solo pruebas
    python3 11_agua_efluentes/modelo_utilities.py --mutaciones     # prueba de mutación de los tests
    python3 11_agua_efluentes/modelo_utilities.py --tablas         # tablas resumen para los .md
    python3 11_agua_efluentes/modelo_utilities.py --escenario --aves-dia 7500 --nivel medio \
        --l-ave 22 --frac-efluente 0.9 --dqo-g-ave 90 --perfil 0.6,0.4,0 --dias-refrigerado 3 \
        --dias-congelado 14 --base-inventario dias_calendario --dias-anio 250
                                                                 # sensibilidad (no escribe CSV)

El script se DETIENE (código 1) si falla cualquier prueba.

------------------------------------------------------------------------------
TRES AGUAS QUE NUNCA SE MEZCLAN
------------------------------------------------------------------------------
  AGUA UTILIZADA   [m³/día operativo] = Σ etapas L/ave × aves / 1.000      (consumo industrial)
  AGUA DESCARGADA  [m³/día operativo] = agua utilizada × fracción a efluente
  AGUA RETENIDA en producto y subproductos [t/día] = kg/ave del balance v1.1 × aves / 1.000
  El agua retenida (0,09 kg/ave en producto; 0,21 kg/ave incorporada con plumas) sale con la masa;
  NUNCA se usa para calcular el consumo industrial (test U03: cambiarla no mueve el agua utilizada).
  Cierre: utilizada = descargada + no descargada (evaporación, retenida, salida con subproductos,
  pérdidas); retenida ≤ no descargada (test U04).

------------------------------------------------------------------------------
FÓRMULAS
------------------------------------------------------------------------------
  Agua [m³/día op.]           = L/ave × aves / 1.000;   caudal medio [m³/h] = m³/día / horas con uso
  Carga [kg/día op.]          = g/ave × aves / 1.000    (carga ESPECÍFICA por ave: el parámetro)
  Concentración [mg/L]        = g/ave / L efluente por ave × 1.000  (resultado, no parámetro)
  DQO extra si se pierde sangre = (f_ref − f) × sangre drenada [kg/ave] × DQO de la sangre [kg/kg]
  Remoción requerida          = 1 − límite de vuelco / concentración cruda  (ilustrativa)
  Electricidad proceso [kWh]  = kWh/t de peso vivo × t vivas/día op.  (indicador de referencia;
                                incluye enfriado de producto fresco; NO incluye congelado, almacenamiento
                                prolongado ni tratamiento aeróbico, que se suman aparte)
  Congelado [kWh]             = kWh/t congelada × t/día congeladas
  Almacenamiento [kWh/día cal.] = kWh/(t·día) × t almacenadas     (las cámaras funcionan 365 días)
  Aireación [kWh/día op.]     = DBO que llega al biológico × remoción × kWh/kg DBO
  Potencia media [kW]         = kWh / horas en que se consume;  pico [kW] = media × factor de pico
  Calor útil [kJ/ave]         = Σ L/ave × 4,186 kJ/(kg·K) × ΔT (× pérdidas)  (escaldado, limpieza,
                                sanitización);  combustible = útil / rendimiento
  Frío de enfriado [kJ/ave]   = kg comestible × cp_fresco × (T_entrada − T_salida)
                                + L/ave de reposición del chiller × 4,186 × (T_red − T_agua_chiller)
                                × (1 + cargas adicionales de salas, docks, infiltración)
  kW frigoríficos             = kJ/día / (horas × 3.600);  kW eléctricos = kW frigoríficos / COP
  TR (tonelada de refrigeración) = kW frigoríficos / 3,517
  Congelación [kJ/kg]         = cp_f × (T_ent − T_cong) + x_agua × 334 + cp_c × (T_cong − T_final)
  Capacidad DIARIA de congelación [t/día op.] = comestible × (congelado + exportación) del perfil
  Capacidad ESTÁTICA de almacenamiento [t]    = flujo × días de inventario (dos bases temporales)
     días de producción: flujo = producción por día operativo
     días calendario:    flujo = producción por día operativo × días op./año / 365

Unidades: aves; L; m³; kg; t; kWh; kW; kJ; MJ; TR; mg/L; h. Separador decimal del CSV: punto.
Columna `origen` del CSV: FUENTE (valor tomado de una fuente, siempre [PVDP] en esta sesión),
ESTIMACIÓN (cálculo propio) o SUPUESTO (hipótesis de trabajo).
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import sys

sys.dont_write_bytecode = True

VERSION = "1.0"
FECHA = "2026-09-30"
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CSV_ESCALA = os.path.join(RAIZ, "23_plan_expansion", "escenarios_escala.csv")
CSV_SALIDA = os.path.join(AQUI, "escenarios_utilities.csv")

ESCALAS = (2500, 5000, 10000, 20000)
CALENDARIOS = {5: 250, 6: 300}                     # SUP-025 (mismo que el modelo de escala)
DIAS_CALENDARIO = 365
NIVELES = ("bajo", "medio", "alto")                 # nivel de DEMANDA de servicios (bajo = menos)
I = {n: i for i, n in enumerate(NIVELES)}
CP_AGUA = 4.186                                     # kJ/(kg·K)
KW_POR_TR = 3.517                                   # 1 TR = 3,517 kW frigoríficos (definición)
KJ_POR_KWH = 3600.0

_MUT: set = set()                                   # mutaciones activas (solo --mutaciones)


class ErrorUtilities(Exception):
    """Parámetro inválido o inconsistencia: detiene el modelo."""


# ---------------------------------------------------------------------------
# 1. PARÁMETROS  (valor bajo / medio / alto; origen; referencia)
#    "bajo/medio/alto" = nivel de DEMANDA del servicio (bajo = planta más eficiente)
#    Referencias FTE-09C-xx: 11_agua_efluentes/fuentes_09C.csv (todas [PVDP])
# ---------------------------------------------------------------------------
# 1.1 Agua industrial por etapa [L/ave faenada]. Totales calibrados a rangos de fuentes
#     (13,2–37,8 L/ave; 22–30 L/ave; 26 L/ave; FTE-09C-01 a 04); reparto por etapa: SUPUESTO guiado
#     por el desglose de EE.UU. (evisceración 7,6; lavado 4,3; chiller 2,1; despiece 3,0 L/ave).
AGUA_ETAPAS = [
    # clave, etiqueta, (bajo, medio, alto), origen, referencia
    ("recepcion", "Recepción: lavado de jaulas/módulos, camiones y andén", (0.5, 1.0, 2.0), "SUPUESTO",
     "sin fuente por ave; DPV propuesto"),
    ("escaldado", "Escaldado: llenado, reposición y desborde", (0.9, 1.2, 2.0), "FUENTE",
     "mín. ~1 cuarto de galón (0,95 L)/ave (FTE-09C-11, FTE-09C-18)"),
    ("desplumado", "Desplumado: duchas y transporte de plumas", (1.0, 2.0, 3.5), "SUPUESTO",
     "incluido en totales de FTE-09C-01/02"),
    ("evisceracion", "Evisceración: lavados interior/exterior y transporte hidráulico de vísceras",
     (4.0, 6.0, 8.0), "FUENTE", "7,57 L/ave (FTE-09C-01)"),
    ("lavado", "Lavado final de carcasas", (1.5, 3.0, 4.5), "FUENTE", "4,25–4,35 L/ave (FTE-09C-01)"),
    ("chiller", "Chiller: reposición de agua (contracorriente)", (1.9, 2.8, 4.5), "FUENTE",
     "mín. 0,5 gal = 1,9 L/ave; típico 2,8–5,7 L/ave (FTE-09C-18); 2,12 L/ave (FTE-09C-01)"),
    ("despiece", "Sala de despiece y deshuese", (0.5, 1.0, 2.0), "FUENTE", "3,03 L/ave (FTE-09C-01)"),
    ("limpieza", "Limpieza de equipos y salas (fin de turno)", (3.0, 5.0, 7.5), "FUENTE",
     "1,5–3 gal = 5,7–11,4 L/ave saneamiento + 0,9–3,8 L equipos (FTE-09C-01)"),
    ("sanitizacion", "Sanitización: esterilizadores, lavamanos, pediluvios, enjuagues", (0.7, 1.0, 1.5),
     "SUPUESTO", "sin fuente separada"),
    ("auxiliares", "Servicios auxiliares: caldera, condensadores evaporativos, vestuarios, comedor",
     (1.0, 2.0, 2.5), "SUPUESTO", "sin fuente separada"),
]
FRAC_EFLUENTE = ((0.80, 0.88, 0.95), "SUPUESTO",
                 "fracción del agua utilizada que se descarga; el resto se evapora (escaldado, caldera, "
                 "condensadores), sale con producto/subproductos o se pierde")
FACTOR_PICO_AGUA = ((1.5, 1.8, 2.2), "SUPUESTO", "caudal horario máximo / medio")
HORAS_NETAS = 8                                     # SUP-053 (sensibilidad en el modelo de escala)
HORAS_LIMPIEZA = 4                                  # SUPUESTO: ventana de limpieza diaria
HORAS_ARRANQUE_CIERRE = 2                           # SUPUESTO

# 1.2 Carga contaminante específica del efluente CRUDO [g/ave], con sangre recuperada al 85 %
#     (SUP-040) y sólidos gruesos retirados en seco. ESTIMACIÓN = concentraciones de fuentes
#     (DQO 1.223–9.695 mg/L; DBO 1.341–2.900 mg/L; SST 378–5.462 mg/L; G y A ~500 mg/L tamizado;
#     NTK 150–296 mg/L; PT ~18,5 mg/L; FTE-181, FTE-09C-05, 06) × caudales de 1.1.
CARGA_G_AVE = {
    "DQO": ((50.0, 100.0, 180.0), "FTE-181; FTE-09C-05"),
    "DBO5": ((25.0, 50.0, 90.0), "FTE-181; FTE-09C-05 (DBO/DQO ~0,4–0,6)"),
    "SST": ((15.0, 35.0, 80.0), "FTE-181; FTE-09C-05"),
    "GyA": ((5.0, 11.0, 25.0), "FTE-09C-06 (~500 mg/L tamizado)"),
    "NTK": ((3.0, 5.0, 8.0), "FTE-09C-06 (150–296 mg/L)"),
    "PT": ((0.3, 0.5, 1.0), "FTE-09C-06 (~18,5 mg/L)"),
}
RANGO_DQO_FUENTES_MG_L = (1223.0, 9695.0)           # FTE-09C-05 [PVDP]
DQO_SANGRE_KG_KG = 375.0 / 1.05 / 1000             # 375.000 mg/L = 375 g/L ÷ 1,05 kg/L = 0,357 kg/kg (FTE-181)
LIMITE_DQO_ILUSTRATIVO = (250.0, "FUENTE", "Res. ADA 336/2003 (PBA), vuelco a conducto pluvial, [PVDP] "
                          "FTE-09C-08; otras jurisdicciones y cuerpos receptores sin relevar")
LIMITE_DBO_ILUSTRATIVO = (50.0, "FUENTE", "idem")

# 1.3 Pretratamiento y lodos
REM_DAF = {  # fracción removida por DAF (FTE-09C-05: DBO 30–90 %, SST 38–70 %, grasas 63–95 %)
    "DBO5": ((0.60, 0.45, 0.30), "FUENTE"),         # bajo = más remoción = menos carga al biológico
    "SST": ((0.70, 0.54, 0.38), "FUENTE"),
    "GyA": ((0.95, 0.80, 0.63), "FUENTE"),
}
FRAC_QUIMICOS_LODO_DAF = ((0.10, 0.15, 0.25), "SUPUESTO", "coagulante/floculante sobre MS removida")
MS_LODO_DAF = ((0.15, 0.12, 0.10), "FUENTE", "5–30 %, habitual 10–15 % de sólidos (FTE-09C-13)")
REMOCION_DBO_BIOLOGICO = 0.95                       # SUPUESTO (para aireación y lodo)
RENDIMIENTO_LODO_AEROBIO = ((0.30, 0.40, 0.50), "SUPUESTO", "kg MS / kg DBO removida (aerobio)")
MS_LODO_DESHIDRATADO = ((0.20, 0.18, 0.15), "SUPUESTO", "fracción de sólidos tras deshidratar")
KWH_KG_DBO = ((0.7, 1.2, 2.0), "SUPUESTO", "kWh eléctricos por kg de DBO removida en tratamiento aerobio")

# 1.4 Electricidad
KWH_T_PV = ((150.0, 250.0, 450.0), "FUENTE",
            "UE 152–860 kWh/t faenada; Brasil 165 kWh/t; 1,19 MJ/kg = 330 kWh/t (FTE-09C-09, FTE-09C-03)")
KWH_T_CONGELADA = ((120.0, 190.0, 260.0), "FUENTE", "120–260 kWh/t de ave congelada; 133 kWh/t (FTE-09C-10)")
KWH_T_DIA_REFRIGERADO = ((0.5, 1.0, 2.0), "SUPUESTO", "cámara 0–4 °C, por t almacenada y día; sin fuente")
KWH_T_DIA_CONGELADO = ((1.5, 3.0, 5.0), "SUPUESTO", "cámara −18/−25 °C, por t almacenada y día; sin fuente")
FACTOR_PICO_ELECTRICO = ((1.3, 1.5, 1.8), "SUPUESTO", "potencia máxima / potencia media de proceso")
# Reparto ilustrativo del consumo de proceso (medio). SUPUESTO guiado por FTE-09C-09 ("agua helada y
# aire comprimido, el mayor uso eléctrico"). Solo didáctico: no se usa en otros cálculos.
REPARTO_ELECTRICO = {"frio_de_proceso_agua_helada_hielo": 0.35, "motores_de_linea_y_transportadores": 0.20,
                     "aire_comprimido": 0.10, "bombas_agua_y_efluentes": 0.10, "climatizacion_salas": 0.08,
                     "iluminacion": 0.07, "oficinas_vestuarios_servicios": 0.05, "otros": 0.05}

# 1.5 Agua caliente / vapor (física; SUPUESTOS de temperatura salvo rangos de fuentes)
T_RED = 18.0                                        # SUPUESTO: agua de red/perforación (varía 10–25 °C)
T_ESCALDADO = ((54.0, 58.0, 62.0), "FUENTE", "suave 51–54 °C; fuerte 60–66 °C (FTE-09C-11)")
FACTOR_PERDIDAS_ESCALDADO = ((1.5, 2.0, 3.0), "SUPUESTO",
                             "calor a las aves, evaporación y pérdidas de la escaldadora sobre el calentamiento "
                             "del agua de reposición")
T_LIMPIEZA = ((50.0, 55.0, 60.0), "FUENTE", "lavado 49–71 °C (FTE-09C-11)")
FRAC_LIMPIEZA_CALIENTE = ((0.5, 0.6, 0.7), "SUPUESTO", "fracción del agua de limpieza que se calienta")
T_ESTERILIZACION = 82.0                             # FUENTE: 82–93 °C (FTE-09C-11) [PVDP]
FRAC_SANITIZACION_CALIENTE = ((0.3, 0.5, 0.7), "SUPUESTO", "fracción del agua de sanitización a 82 °C")
RENDIMIENTO_TERMICO = ((0.85, 0.75, 0.65), "SUPUESTO", "generación + distribución de calor")
PCI_MJ = {"gas_natural_m3": (38.9, "SUPUESTO", "~9.300 kcal/m³ (a verificar con distribuidora)"),
          "glp_kg": (46.0, "SUPUESTO", "~11.000 kcal/kg"),
          "biomasa_chip_kg": (14.0, "SUPUESTO", "chip de madera ~20–25 % humedad; muy variable")}

# 1.6 Frío
T_ENTRADA_CARCASA = 38.0                            # SUPUESTO: carcasa post-evisceración
T_SALIDA_CARCASA = 4.0                              # SUPUESTO: objetivo de enfriado (norma a verificar)
T_AGUA_CHILLER = 1.0                                # SUPUESTO
CP_FRESCO = 3.5                                     # kJ/(kg·K) SUPUESTO típico de carne (ASHRAE, FTE-09C-14)
CP_CONGELADO = 1.8                                  # kJ/(kg·K) SUPUESTO típico
T_CONGELACION_INICIAL = -1.5                        # °C SUPUESTO
T_FINAL_CONGELADO = -18.0                           # °C (exigencia usual de exportación, FTE-135 [PVDP])
FRAC_AGUA_PRODUCTO = 0.74                           # SUPUESTO; latente = x_agua × 334 kJ/kg (FTE-09C-14)
CALOR_LATENTE_AGUA = 334.0                          # kJ/kg (propiedad física)
FRAC_CARGAS_ADICIONALES = ((0.25, 0.40, 0.60), "SUPUESTO",
                           "salas climatizadas, docks, infiltración, motores e iluminación en recintos fríos")
FACTOR_TUNEL = ((1.2, 1.3, 1.5), "SUPUESTO", "envases, ventiladores, deshielo y pérdidas del túnel")
HORAS_TUNEL = 20                                    # SUPUESTO: horas/día de congelación efectiva
COP_ENFRIADO = ((4.0, 3.0, 2.3), "SUPUESTO", "agua helada / hielo, evaporación ~−5/0 °C")
COP_CONGELADO = ((1.8, 1.4, 1.1), "SUPUESTO", "túnel, evaporación ~−35/−40 °C")

# 1.7 Inventario (mismos perfiles y definiciones que el modelo de escala; SUP-055, SUP-056)
PERFILES = {"P1": {"refrigerado": 0.90, "congelado": 0.10, "exportacion": 0.00},
            "P2": {"refrigerado": 0.60, "congelado": 0.40, "exportacion": 0.00},
            "P3": {"refrigerado": 0.50, "congelado": 0.30, "exportacion": 0.20}}
DIAS_INVENTARIO = (1, 3, 7, 14)
DIAS_REFRIGERADO_DEF, DIAS_CONGELADO_DEF = 3, 14    # especificación del simulador (SUP-056)
FRAC_GARRAS_CONGELADAS = ((0.0, 1.0, 1.0), "SUPUESTO", "garras para exportación: siempre congeladas")
FRAC_MENUDENCIAS_CONGELADAS = ((0.0, 0.5, 1.0), "SUPUESTO", "")

# 1.8 Respaldo
FACTOR_REARRANQUE = ((1.3, 1.5, 2.0), "SUPUESTO", "recuperación de temperatura tras un corte")
FRAC_RESPALDO = {"control_it_seguridad": 0.02, "iluminacion_emergencia": 0.01, "bombeo_agua_minimo": 0.03,
                 "anden_aves_ventilacion": 0.02}     # SUPUESTO: fracción de la potencia pico de proceso
FRAC_EFLUENTE_MINIMO = 0.5                          # SUPUESTO: aireación/bombas mínimas en corte
FACTOR_POTENCIA = 0.8                               # SUPUESTO: kVA = kW / 0,8

PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen|"
                                 r"ingreso|ingresos|rentabilidad)\b|\$", re.IGNORECASE)


def nv(param, nivel):
    """Valor de un parámetro (tupla de 3 o (tupla, origen, ref)) para el nivel."""
    t = param[0] if isinstance(param[0], tuple) else param
    return t[I[nivel]]


# ---------------------------------------------------------------------------
# 2. LECTURA DEL MODELO DE ESCALA (fuente de verdad de la masa)
# ---------------------------------------------------------------------------
_CACHE: dict = {}


def leer_escala():
    if "filas" not in _CACHE:
        if not os.path.exists(CSV_ESCALA):
            raise ErrorUtilities(f"No existe {CSV_ESCALA}: correr 23_plan_expansion/modelo_escala.py")
        with open(CSV_ESCALA, encoding="utf-8") as fh:
            _CACHE["filas"] = list(csv.DictReader(fh))
    return _CACHE["filas"]


def valor_escala(E, ds, bloque, variable, periodo="dia_operativo", parametro=None):
    res = [float(f["valor"]) for f in leer_escala()
           if f["bloque"] == bloque and int(f["escala_aves_dia"]) == E and int(f["dias_semana"]) == ds
           and f["variable"] == variable and f["periodo"] == periodo
           and (parametro is None or f["parametro"] == parametro)]
    if len(res) != 1:
        raise ErrorUtilities(f"Búsqueda ambigua o vacía en escenarios_escala.csv ({len(res)}): "
                             f"{bloque}/{variable}/{E}/{ds}/{periodo}/{parametro}")
    return res[0]


MASAS = {  # clave: (bloque, variable)  -> kg/ave = t/día / aves × 1.000
    "peso_vivo": ("balance_productos", "entrada_pollo_vivo_t"),
    "agua_incorporada": ("balance_productos", "entrada_agua_incorporada_t"),
    "comestible": ("masa_comestible", "comestible_t"),
    "comestible_bio": ("masa_comestible", "comestible_bio_t"),
    "agua_retenida_producto": ("masa_comestible", "agua_retenida_comestible_t"),
    "sangre_recuperada": ("subproductos", "sangre_t"),
    "sangre_drenada": ("subproductos", "sangre_drenada_t"),
    "plumas": ("subproductos", "plumas_t"),
    "visceras": ("subproductos", "visceras_t"),
    "cabeza": ("subproductos", "cabeza_t"),
    "garras": ("subproductos", "garras_t"),
    "menudencias": ("balance_productos", "menudencias_t"),
    "rendering_potencial": ("subproductos", "rendering_potencial_t"),
    "solidos_a_retirar": ("subproductos", "solidos_a_retirar_t"),
    "masa_a_efluente_o_perdida": ("logistica", "masa_a_efluente_o_perdida_t_dia"),
}


def kg_por_ave(E=10000, ds=5):
    """kg/ave de cada masa, desde el CSV de escala (config. B, 2,9 kg, medio, inmersión)."""
    return {k: valor_escala(E, ds, b, v) * 1000 / E for k, (b, v) in MASAS.items()}


# ---------------------------------------------------------------------------
# 3. CÁLCULO
# ---------------------------------------------------------------------------
class R:
    """Resultados con metadatos (una fila del CSV por variable)."""

    def __init__(self):
        self.filas, self.v = [], {}

    def add(self, bloque, var, val, unidad, periodo, base, origen, clasif, ref="", nota="", parametro=""):
        if var in self.v:
            raise ErrorUtilities(f"Variable duplicada: {var}")
        self.v[var] = val
        self.filas.append({"bloque": bloque, "parametro": parametro, "variable": var, "valor": val,
                           "unidad": unidad, "periodo": periodo, "base": base, "origen": origen,
                           "clasificacion": clasif, "referencia": ref, "nota": nota})

    def __getitem__(self, k):
        return self.v[k]


def parametros(nivel="medio", **ov):
    """Parámetros del nivel; ov reemplaza cualquiera (validados)."""
    if nivel not in NIVELES:
        raise ErrorUtilities(f"Nivel {nivel} inexistente ({NIVELES})")
    p = {"nivel": nivel,
         "l_ave_etapas": {c: nv(v, nivel) for c, _, v, _, _ in AGUA_ETAPAS},
         "frac_efluente": nv(FRAC_EFLUENTE, nivel),
         "factor_pico_agua": nv(FACTOR_PICO_AGUA, nivel),
         "carga_g_ave": {k: nv(v, nivel) for k, v in CARGA_G_AVE.items()},
         "frac_sangre_recuperada": None,           # None = la del balance (SUP-040, 85 %)
         "perfil": dict(PERFILES["P1"]), "perfil_id": "P1",
         "dias_refrigerado": DIAS_REFRIGERADO_DEF, "dias_congelado": DIAS_CONGELADO_DEF,
         "base_inventario": "dias_produccion",
         "horas_netas": HORAS_NETAS, "horas_limpieza": HORAS_LIMPIEZA,
         "limite_dqo_mg_l": LIMITE_DQO_ILUSTRATIVO[0]}
    l_total = ov.pop("l_ave_total", None)
    p.update(ov)
    if l_total is not None:                           # escala todas las etapas en proporción
        s = sum(p["l_ave_etapas"].values())
        p["l_ave_etapas"] = {c: v * l_total / s for c, v in p["l_ave_etapas"].items()}
    validar(p)
    return p


def validar(p):
    if any(v < 0 or not math.isfinite(v) for v in p["l_ave_etapas"].values()):
        raise ErrorUtilities("L/ave negativo o no finito")
    if sum(p["l_ave_etapas"].values()) > 200:
        raise ErrorUtilities("L/ave > 200: fuera de todo rango de faena avícola (revisar unidades: ¿m³?)")
    if not 0 < p["frac_efluente"] <= 1:
        raise ErrorUtilities("La fracción de agua a efluente debe estar en (0, 1]: no se descarga más de lo usado")
    if any(v < 0 for v in p["carga_g_ave"].values()):
        raise ErrorUtilities("Carga específica negativa")
    fs = p["frac_sangre_recuperada"]
    if fs is not None and not 0 <= fs <= 1:
        raise ErrorUtilities("Fracción de sangre recuperada fuera de [0, 1]")
    if abs(sum(p["perfil"].values()) - 1) > 1e-9 or any(v < 0 for v in p["perfil"].values()):
        raise ErrorUtilities("El perfil refrigerado/congelado/exportación debe sumar 100 % sin negativos")
    if p["base_inventario"] not in ("dias_produccion", "dias_calendario"):
        raise ErrorUtilities("Base de inventario: dias_produccion o dias_calendario")
    for k in ("dias_refrigerado", "dias_congelado"):
        if not 0 <= p[k] <= 365:
            raise ErrorUtilities(f"{k} fuera de 0–365")
    if not 0 < p["horas_netas"] <= 20 or not 0 <= p["horas_limpieza"] <= 12:
        raise ErrorUtilities("Horas netas (0–20] o de limpieza [0–12] inválidas")


def calcular(aves, dias_anio=250, nivel="medio", masas=None, p=None):
    """Todas las variables de utilities para `aves` faenadas por día operativo."""
    if not (isinstance(aves, (int, float)) and aves > 0 and math.isfinite(aves)):
        raise ErrorUtilities(f"aves/día inválido: {aves}")
    if not 0 < dias_anio <= 6 * 365 / 7 + 1e-9:
        raise ErrorUtilities(f"días/año {dias_anio} fuera de rango (máx. 6 días/semana)")
    p = p or parametros(nivel)
    k = dict(masas or kg_por_ave())
    if p["frac_sangre_recuperada"] is None:
        p = dict(p, frac_sangre_recuperada=k["sangre_recuperada"] / k["sangre_drenada"])
    n = nivel
    A = aves ** 1.01 if "M02" in _MUT else aves          # M02: escalado no lineal
    r = R()
    f_cal = dias_anio / DIAS_CALENDARIO
    h_op = p["horas_netas"] + p["horas_limpieza"]
    h_planta = h_op + HORAS_ARRANQUE_CIERRE
    t_vivas = k["peso_vivo"] * A / 1000
    r.add("entrada", "aves_faenadas_dia_operativo", A, "aves", "dia_operativo", "aves", "SUPUESTO", "[SUPUESTO]",
          "SUP-052", "escala = capacidad operativa")
    r.add("entrada", "t_vivas_dia_operativo", t_vivas, "t", "dia_operativo", "vivo", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "escenarios_escala.csv")

    # --- 1. AGUA INDUSTRIAL -------------------------------------------------------
    conv = 1.0 if "M08" in _MUT else 1000.0             # M08: L confundidos con m³
    l_ave = sum(p["l_ave_etapas"].values())
    ret_prod = k["agua_retenida_producto"]
    if "M01" in _MUT:                                   # M01: agua retenida sumada al consumo
        l_ave += ret_prod
    for c, etq, _, org, ref in AGUA_ETAPAS:
        v = p["l_ave_etapas"][c]
        r.add("agua", f"agua_{c}_l_ave", v, "L/ave", "por_ave", "agua_utilizada", org,
              f"[{org}]" + (" [PVDP]" if org == "FUENTE" else ""), ref, etq, parametro=f"nivel={n}")
        r.add("agua", f"agua_{c}_m3_dia", v * A / conv, "m³", "dia_operativo", "agua_utilizada", "ESTIMACIÓN",
              "[ESTIMACIÓN]", "", etq, parametro=f"nivel={n}")
    m3_uso = l_ave * A / conv
    r.add("agua", "agua_utilizada_l_ave", l_ave, "L/ave", "por_ave", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN] con rangos [PVDP]", "FTE-09C-01 a 04", "consumo industrial; NO incluye agua retenida",
          parametro=f"nivel={n}")
    r.add("agua", "agua_utilizada_m3_dia", m3_uso, "m³", "dia_operativo", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
    r.add("agua", "agua_utilizada_m3_anio", m3_uso * dias_anio, "m³", "anio", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
    r.add("agua", "agua_utilizada_m3_h_medio", m3_uso / h_op, "m³/h", "hora", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", f"sobre {h_op} h (faena + limpieza)", parametro=f"nivel={n}")
    r.add("agua", "agua_utilizada_m3_h_pico", m3_uso / h_op * p["factor_pico_agua"], "m³/h", "hora",
          "agua_utilizada", "SUPUESTO", "[SUPUESTO] factor de pico", "", "dimensiona captación, bombeo y reserva",
          parametro=f"nivel={n}")
    r.add("agua", "reserva_agua_1_dia_m3", m3_uso, "m³", "stock", "agua_utilizada", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "", "volumen equivalente a un día de uso (referencia conceptual, no diseño)", parametro=f"nivel={n}")
    fe = p["frac_efluente"]
    m3_desc = m3_uso * (1.1 if "M03" in _MUT else fe)     # M03: se descarga más de lo usado
    r.add("agua", "agua_descargada_m3_dia", m3_desc, "m³", "dia_operativo", "agua_descargada", "SUPUESTO",
          "[ESTIMACIÓN] con fracción [SUPUESTO]", "", f"fracción a efluente = {fe:.2f}", parametro=f"nivel={n}")
    r.add("agua", "agua_descargada_l_ave", m3_desc * 1000 / A if conv == 1000 else m3_desc / A * 1000, "L/ave",
          "por_ave", "agua_descargada", "ESTIMACIÓN", "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
    r.add("agua", "agua_no_descargada_m3_dia", m3_uso - m3_desc, "m³", "dia_operativo", "agua_no_descargada",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "evaporación + retenida + sale con subproductos + pérdidas",
          parametro=f"nivel={n}")
    r.add("agua_retenida", "agua_retenida_en_producto_t_dia", ret_prod * A / 1000, "t", "dia_operativo",
          "agua_retenida", "ESTIMACIÓN", "[ESTIMACIÓN] del balance v1.1", "escenarios_escala.csv",
          "sale vendida con el producto; NO es consumo industrial ni efluente")
    r.add("agua_retenida", "agua_incorporada_producto_y_subproductos_t_dia", k["agua_incorporada"] * A / 1000,
          "t", "dia_operativo", "agua_retenida", "ESTIMACIÓN", "[ESTIMACIÓN] del balance v1.1",
          "escenarios_escala.csv", "absorbida en chiller + adherida a plumas (incluye goteo posterior)")
    r.add("agua_retenida", "agua_retenida_sobre_agua_utilizada_pct",
          100 * ret_prod / (m3_uso / A * 1000 if conv == 1000 else m3_uso / A), "%", "adimensional", "agua",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "cuánto del agua usada termina dentro del producto")

    # --- 2. EFLUENTES Y CARGA ORGÁNICA -----------------------------------------------
    l_desc_ave = m3_desc / A * (1000 if conv == 1000 else 1)
    f_ref = k["sangre_recuperada"] / k["sangre_drenada"]
    extra_dqo = 0.0 if "M07" in _MUT else (f_ref - p["frac_sangre_recuperada"]) * k["sangre_drenada"] \
        * DQO_SANGRE_KG_KG * 1000
    for par, (vals, ref) in CARGA_G_AVE.items():
        g = p["carga_g_ave"][par] + (extra_dqo if par == "DQO" else 0.0)
        r.add("efluente", f"carga_{par}_g_ave", g, "g/ave", "por_ave", "efluente_crudo", "ESTIMACIÓN",
              "[ESTIMACIÓN] con rangos [PVDP]", ref, "efluente crudo tras retirar sangre y sólidos gruesos",
              parametro=f"nivel={n}")
        r.add("efluente", f"carga_{par}_kg_dia", g * A / 1000, "kg", "dia_operativo", "efluente_crudo",
              "ESTIMACIÓN", "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
        r.add("efluente", f"concentracion_{par}_mg_l", g / l_desc_ave * 1000, "mg/L", "adimensional",
              "efluente_crudo", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "resultado (carga / caudal), no parámetro",
              parametro=f"nivel={n}")
    r.add("efluente", "dqo_extra_por_sangre_no_recuperada_g_ave", extra_dqo, "g/ave", "por_ave", "efluente_crudo",
          "ESTIMACIÓN", "[ESTIMACIÓN] con DQO de sangre [PVDP]", "FTE-181",
          f"recuperación {p['frac_sangre_recuperada']:.2f} vs referencia {f_ref:.2f}")
    dqo_sangre_evitada = k["sangre_recuperada"] * DQO_SANGRE_KG_KG
    r.add("efluente", "dqo_evitada_por_recuperar_sangre_kg_dia", dqo_sangre_evitada * A, "kg", "dia_operativo",
          "efluente_crudo", "ESTIMACIÓN", "[ESTIMACIÓN] con DQO de sangre [PVDP]", "FTE-181",
          "orden de magnitud; no es una reducción medida")
    r.add("efluente", "caudal_efluente_m3_h_pico", m3_desc / h_op * p["factor_pico_agua"], "m³/h", "hora",
          "agua_descargada", "SUPUESTO", "[SUPUESTO] factor de pico", "", "dimensiona ecualización",
          parametro=f"nivel={n}")
    c_dqo = r[f"concentracion_DQO_mg_l"]
    r.add("efluente", "remocion_dqo_requerida_ilustrativa_pct", 100 * max(0.0, 1 - p["limite_dqo_mg_l"] / c_dqo),
          "%", "adimensional", "efluente_crudo", "ESTIMACIÓN", "[ESTIMACIÓN] con límite [PVDP]",
          "FTE-09C-08", f"límite ilustrativo {p['limite_dqo_mg_l']:g} mg/L (ADA 336/03, pluvial; a confirmar "
          "según sitio y cuerpo receptor)", parametro=f"nivel={n}")
    # masa que puede evitar llegar al efluente (del balance; no son reducciones medidas)
    for clave, nota in (("sangre_recuperada", "sangre recuperada por separado (85 %, SUP-040)"),
                        ("plumas", "plumas húmedas retiradas"), ("visceras", "vísceras no comestibles"),
                        ("cabeza", "cabezas"), ("solidos_a_retirar", "total sólidos a retirar en seco "
                                                                   "(C + decomisos + contenido GI; NO sumar)"),
                        ("masa_a_efluente_o_perdida", "masa que el balance ya envía a efluente o pérdida "
                                                      "(sangre no recuperada, cutícula, goteo, pérdidas)")):
        r.add("masa_evitable", f"{clave}_t_dia", k[clave] * A / 1000, "t", "dia_operativo", "biologica+agua",
              "ESTIMACIÓN", "[ESTIMACIÓN] del balance v1.1", "escenarios_escala.csv", nota)

    # --- 3. PRETRATAMIENTO Y LODOS (orden de magnitud) --------------------------------
    sst, gya, dbo = (r[f"carga_{x}_kg_dia"] for x in ("SST", "GyA", "DBO5"))
    ms_daf = (sst * nv(REM_DAF["SST"], n) + gya * nv(REM_DAF["GyA"], n)) * (1 + nv(FRAC_QUIMICOS_LODO_DAF, n))
    r.add("lodos", "lodo_daf_kg_ms_dia", ms_daf, "kg", "dia_operativo", "materia_seca", "ESTIMACIÓN",
          "[ESTIMACIÓN] con remociones [PVDP]", "FTE-09C-05, FTE-09C-13", "sólidos + grasas flotados + químicos",
          parametro=f"nivel={n}")
    r.add("lodos", "lodo_daf_t_humedo_dia", ms_daf / nv(MS_LODO_DAF, n) / 1000, "t", "dia_operativo",
          "lodo_humedo", "ESTIMACIÓN", "[ESTIMACIÓN] con % sólidos [PVDP]", "FTE-09C-13", parametro=f"nivel={n}")
    dbo_bio = dbo * (1 - nv(REM_DAF["DBO5"], n))
    r.add("lodos", "dbo_al_tratamiento_biologico_kg_dia", dbo_bio, "kg", "dia_operativo", "efluente_pretratado",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "después de DAF", parametro=f"nivel={n}")
    ms_bio = dbo_bio * REMOCION_DBO_BIOLOGICO * nv(RENDIMIENTO_LODO_AEROBIO, n)
    r.add("lodos", "lodo_biologico_aerobio_kg_ms_dia", ms_bio, "kg", "dia_operativo", "materia_seca", "SUPUESTO",
          "[ESTIMACIÓN] con rendimiento [SUPUESTO]", "", "si el tratamiento fuera aerobio completo; "
          "anaerobio genera mucho menos lodo", parametro=f"nivel={n}")
    r.add("lodos", "lodos_deshidratados_t_dia", (ms_daf + ms_bio) / nv(MS_LODO_DESHIDRATADO, n) / 1000, "t",
          "dia_operativo", "lodo_humedo", "SUPUESTO", "[ESTIMACIÓN] con [SUPUESTO]", "",
          "DAF + biológico deshidratados; disposición/valorización a definir", parametro=f"nivel={n}")

    # --- 4. ELECTRICIDAD ---------------------------------------------------------------
    kwh_proc = nv(KWH_T_PV, n) * t_vivas
    r.add("electricidad", "kwh_proceso_dia", kwh_proc, "kWh", "dia_operativo", "energia_electrica", "FUENTE",
          "[ESTIMACIÓN] con indicador [PVDP]", KWH_T_PV[2], "faena, proceso, enfriado fresco, aire, agua, "
          "servicios", parametro=f"nivel={n}")
    for c, f in REPARTO_ELECTRICO.items():
        r.add("electricidad", f"kwh_proceso_{c}_dia", kwh_proc * f, "kWh", "dia_operativo", "energia_electrica",
              "SUPUESTO", "[SUPUESTO] reparto ilustrativo", "FTE-09C-09 (cualitativo)", "didáctico; no sumar "
              "con kwh_proceso_dia", parametro=f"nivel={n}")

    # --- 5. INVENTARIO (reproduce el modelo de escala) -----------------------------------
    com = k["comestible"] * A / 1000                     # t comerciales por día OPERATIVO
    flujo_inv = com * (1 if ("M05" in _MUT or p["base_inventario"] == "dias_produccion") else f_cal)
    sh = p["perfil"]
    d_ref, d_cong = p["dias_refrigerado"], p["dias_congelado"]
    t_refr = flujo_inv * sh["refrigerado"] * d_ref
    t_cong = flujo_inv * (sh["congelado"] + sh["exportacion"]) * (1 if "M06" in _MUT else d_cong)
    r.add("inventario", "stock_refrigerado_t", t_refr, "t", "stock", "comercial", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "SUP-055, SUP-056", f"base={p['base_inventario']}; días={d_ref}; perfil={p['perfil_id']}")
    r.add("inventario", "stock_congelado_t", t_cong, "t", "stock", "comercial", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "SUP-055, SUP-056", f"base={p['base_inventario']}; días={d_cong}; incluye exportación")

    # --- 6. CONGELADO: capacidad DIARIA vs ESTÁTICA -----------------------------------
    t_cong_dia = com * (sh["congelado"] + sh["exportacion"])
    r.add("congelado", "capacidad_congelacion_t_dia", t_cong_dia, "t", "dia_operativo", "comercial", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "SUP-055", "t que hay que congelar cada día de faena (túneles/IQF)")
    r.add("congelado", "capacidad_almacenamiento_congelado_t", t_cong, "t", "stock", "comercial", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", "t que hay que guardar (cámaras); NO es capacidad de congelación")
    garras_c = k["garras"] * A / 1000 * nv(FRAC_GARRAS_CONGELADAS, n)
    menud_c = k["menudencias"] * A / 1000 * nv(FRAC_MENUDENCIAS_CONGELADAS, n)
    r.add("congelado", "garras_a_congelar_t_dia_informativo", garras_c, "t", "dia_operativo", "comercial",
          "SUPUESTO", "[SUPUESTO]", "", "ya incluidas dentro del comestible: NO sumar al perfil",
          parametro=f"nivel={n}")
    r.add("congelado", "menudencias_a_congelar_t_dia_informativo", menud_c, "t", "dia_operativo", "comercial",
          "SUPUESTO", "[SUPUESTO]", "", "ya incluidas dentro del comestible: NO sumar al perfil",
          parametro=f"nivel={n}")
    kj_kg_cong = (CP_FRESCO * (T_SALIDA_CARCASA - T_CONGELACION_INICIAL) + FRAC_AGUA_PRODUCTO * CALOR_LATENTE_AGUA
                  + CP_CONGELADO * (T_CONGELACION_INICIAL - T_FINAL_CONGELADO)) * nv(FACTOR_TUNEL, n)
    r.add("congelado", "calor_a_extraer_congelacion_kj_kg", kj_kg_cong, "kJ/kg", "adimensional", "producto",
          "ESTIMACIÓN", "[ESTIMACIÓN] con propiedades [PVDP]", "FTE-09C-14", "de +4 °C a −18 °C, con pérdidas",
          parametro=f"nivel={n}")
    kwf_cong = t_cong_dia * 1000 * kj_kg_cong / (HORAS_TUNEL * 3600)

    # --- 7. FRÍO ------------------------------------------------------------------------
    kj_ave_enf = (k["comestible"] * CP_FRESCO * (T_ENTRADA_CARCASA - T_SALIDA_CARCASA)
                  + p["l_ave_etapas"]["chiller"] * CP_AGUA * (T_RED - T_AGUA_CHILLER)) \
        * (1 + nv(FRAC_CARGAS_ADICIONALES, n))
    kwf_enf = kj_ave_enf * A / (p["horas_netas"] * 3600)
    cop_e, cop_c = nv(COP_ENFRIADO, n), nv(COP_CONGELADO, n)
    if "M04" in _MUT:
        cop_e = cop_c = 1.0                                 # M04: kW eléctrico = kW frigorífico
    kwh_alm_refr = t_refr * nv(KWH_T_DIA_REFRIGERADO, n)
    kwh_alm_cong = t_cong * nv(KWH_T_DIA_CONGELADO, n)
    kwe_alm = (kwh_alm_refr + kwh_alm_cong) / 24
    kwf_alm = kwh_alm_refr / 24 * cop_e + kwh_alm_cong / 24 * cop_c
    for var, kwf, cop, nota in (("enfriado_producto_fresco", kwf_enf, cop_e,
                                 f"chiller + menudencias + salas/docks; durante {p['horas_netas']} h netas"),
                                ("congelacion_tuneles", kwf_cong, cop_c, f"durante {HORAS_TUNEL} h/día"),
                                ("camaras_almacenamiento", kwf_alm, None, "24 h, 365 días; desde kWh/(t·día)")):
        r.add("frio", f"kw_frigorificos_{var}", kwf, "kW frigoríficos", "potencia", "frio", "ESTIMACIÓN",
              "[ESTIMACIÓN] con [SUPUESTO]", "", nota, parametro=f"nivel={n}")
        r.add("frio", f"tr_{var}", kwf / KW_POR_TR, "TR", "potencia", "frio", "ESTIMACIÓN", "[ESTIMACIÓN]", "",
              "1 TR = 3,517 kW frigoríficos", parametro=f"nivel={n}")
        kwe = kwf / cop if cop else kwe_alm
        r.add("frio", f"kw_electricos_{var}", kwe, "kW eléctricos", "potencia", "energia_electrica", "SUPUESTO",
              "[ESTIMACIÓN] con COP [SUPUESTO]", "", "kW eléctricos = kW frigoríficos / COP",
              parametro=f"nivel={n}")
    r.add("frio", "kj_frio_enfriado_por_ave", kj_ave_enf, "kJ/ave", "por_ave", "frio", "ESTIMACIÓN",
          "[ESTIMACIÓN] con [SUPUESTO]", "FTE-09C-14", parametro=f"nivel={n}")
    kwh_cong = nv(KWH_T_CONGELADA, n) * t_cong_dia
    r.add("electricidad", "kwh_congelacion_dia", kwh_cong, "kWh", "dia_operativo", "energia_electrica", "FUENTE",
          "[ESTIMACIÓN] con indicador [PVDP]", KWH_T_CONGELADA[2], parametro=f"nivel={n}")
    r.add("electricidad", "kwh_almacenamiento_frio_dia_calendario", kwh_alm_refr + kwh_alm_cong, "kWh",
          "dia_calendario", "energia_electrica", "SUPUESTO", "[ESTIMACIÓN] con [SUPUESTO]", "",
          "las cámaras funcionan también sin faena", parametro=f"nivel={n}")
    kwh_efl = dbo_bio * REMOCION_DBO_BIOLOGICO * nv(KWH_KG_DBO, n)
    r.add("electricidad", "kwh_tratamiento_aerobio_dia", kwh_efl, "kWh", "dia_operativo", "energia_electrica",
          "SUPUESTO", "[ESTIMACIÓN] con [SUPUESTO]", "", "cota: si todo el biológico fuera aerobio",
          parametro=f"nivel={n}")
    kwh_op = kwh_proc + kwh_cong + kwh_efl
    kwh_anio = kwh_op * dias_anio + (kwh_alm_refr + kwh_alm_cong) * DIAS_CALENDARIO
    r.add("electricidad", "kwh_total_dia_operativo", kwh_op + kwh_alm_refr + kwh_alm_cong, "kWh", "dia_operativo",
          "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "proceso + congelado + aerobio + cámaras",
          parametro=f"nivel={n}")
    r.add("electricidad", "kwh_total_anio", kwh_anio, "kWh", "anio", "energia_electrica", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", "cámaras × 365 días; resto × días de faena", parametro=f"nivel={n}")
    r.add("electricidad", "kwh_por_ave_promedio_anual", kwh_anio / (A * dias_anio), "kWh/ave", "por_ave",
          "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
    kw_media_proc = kwh_proc / h_planta
    kw_pico_proc = kw_media_proc * nv(FACTOR_PICO_ELECTRICO, n)
    kw_media_total = kw_media_proc + kwh_cong / HORAS_TUNEL + kwe_alm + kwh_efl / 24
    kw_pico = kw_pico_proc + kwh_cong / HORAS_TUNEL + kwe_alm + kwh_efl / 24
    if "M09" in _MUT:
        kw_pico = kw_media_total * 0.9                      # M09: pico menor que la media
    r.add("electricidad", "kw_potencia_media_operacion", kw_media_total, "kW", "potencia", "energia_electrica",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", f"proceso sobre {h_planta} h + túneles + cámaras + efluentes",
          parametro=f"nivel={n}")
    r.add("electricidad", "kw_potencia_pico_estimada", kw_pico, "kW", "potencia", "energia_electrica", "SUPUESTO",
          "[ESTIMACIÓN] con factor de pico [SUPUESTO]", "", "orden de magnitud para pedir potencia; no es diseño",
          parametro=f"nivel={n}")

    # --- 8. AGUA CALIENTE / VAPOR -----------------------------------------------------
    le = p["l_ave_etapas"]
    kj_esc = le["escaldado"] * CP_AGUA * (nv(T_ESCALDADO, n) - T_RED) * nv(FACTOR_PERDIDAS_ESCALDADO, n)
    kj_lim = le["limpieza"] * nv(FRAC_LIMPIEZA_CALIENTE, n) * CP_AGUA * (nv(T_LIMPIEZA, n) - T_RED)
    kj_san = le["sanitizacion"] * nv(FRAC_SANITIZACION_CALIENTE, n) * CP_AGUA * (T_ESTERILIZACION - T_RED)
    util_mj_ave = (kj_esc + kj_lim + kj_san) / 1000
    comb_mj_ave = util_mj_ave / nv(RENDIMIENTO_TERMICO, n)
    for var, kj, h in (("escaldado", kj_esc, p["horas_netas"]), ("limpieza", kj_lim, p["horas_limpieza"]),
                       ("sanitizacion", kj_san, h_op)):
        r.add("termico", f"calor_util_{var}_mj_dia", kj * A / 1000, "MJ", "dia_operativo", "energia_termica",
              "ESTIMACIÓN", "[ESTIMACIÓN] con temperaturas [PVDP]/[SUPUESTO]", "FTE-09C-11", parametro=f"nivel={n}")
        r.add("termico", f"kw_termicos_{var}", kj * A / (h * 3600) if h else 0.0, "kW térmicos", "potencia",
              "energia_termica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", f"durante {h} h", parametro=f"nivel={n}")
    r.add("termico", "calor_util_mj_ave", util_mj_ave, "MJ/ave", "por_ave", "energia_termica", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=f"nivel={n}")
    r.add("termico", "energia_combustible_mj_dia", comb_mj_ave * A, "MJ", "dia_operativo", "energia_termica",
          "ESTIMACIÓN", "[ESTIMACIÓN] con rendimiento [SUPUESTO]", "", parametro=f"nivel={n}")
    r.add("termico", "energia_combustible_kwh_dia", comb_mj_ave * A / 3.6, "kWh", "dia_operativo",
          "energia_termica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "kWh TÉRMICOS (no eléctricos)", parametro=f"nivel={n}")
    for comb, (pci, org, ref) in PCI_MJ.items():
        r.add("termico", f"equivalente_{comb}_dia", comb_mj_ave * A / pci, comb.split("_")[-1], "dia_operativo",
              "energia_termica", "SUPUESTO", "[ESTIMACIÓN] con PCI [SUPUESTO]", ref, "equivalencia, no elección",
              parametro=f"nivel={n}")
    r.add("termico", "equivalente_electricidad_resistiva_kwh_dia", util_mj_ave * A / 3.6 / 0.98, "kWh",
          "dia_operativo", "energia_termica", "SUPUESTO", "[ESTIMACIÓN]", "", "rendimiento 98 %; bomba de calor "
          "dividiría por su COP (limitada a ~60–70 °C)", parametro=f"nivel={n}")

    # --- 9. RESPALDO ------------------------------------------------------------------
    crit = {"camaras_frio": kwe_alm * nv(FACTOR_REARRANQUE, n),
            "efluentes_minimo": kwh_efl / 24 * FRAC_EFLUENTE_MINIMO}
    crit.update({c: f * kw_pico_proc for c, f in FRAC_RESPALDO.items()})
    for c, v in crit.items():
        r.add("respaldo", f"kw_critico_{c}", v, "kW", "potencia", "energia_electrica", "SUPUESTO",
              "[ESTIMACIÓN] con [SUPUESTO]", "", parametro=f"nivel={n}")
    kw_crit = sum(crit.values())
    r.add("respaldo", "kw_respaldo_cargas_criticas", kw_crit, "kW", "potencia", "energia_electrica", "SUPUESTO",
          "[ESTIMACIÓN] con [SUPUESTO]", "", "cámaras + control + emergencia + efluentes + agua + andén",
          parametro=f"nivel={n}")
    r.add("respaldo", "kva_respaldo_cargas_criticas", kw_crit / FACTOR_POTENCIA, "kVA", "potencia",
          "energia_electrica", "SUPUESTO", "[ESTIMACIÓN]", "", "fp 0,8", parametro=f"nivel={n}")
    r.add("respaldo", "kva_respaldo_planta_completa", kw_pico / FACTOR_POTENCIA, "kVA", "potencia",
          "energia_electrica", "SUPUESTO", "[ESTIMACIÓN]", "", "si se quisiera sostener también la línea",
          parametro=f"nivel={n}")
    return r


def inventario_escala(E, dias_anio):
    """Filas equivalentes al bloque `inventario` del modelo de escala, recalculadas desde el
    comestible por día operativo (test U07). Devuelve {(base, dias, perfil, cat): t}."""
    com = kg_por_ave()["comestible"] * E / 1000
    out = {}
    for base in ("dias_produccion", "dias_calendario"):
        flujo = com if (base == "dias_produccion" or "M05" in _MUT) else com * dias_anio / DIAS_CALENDARIO
        for d in DIAS_INVENTARIO:
            out[(base, d, "", "comestible_total")] = flujo * d
            for pid, sh in PERFILES.items():
                for cat, s in sh.items():
                    out[(base, d, pid, cat)] = flujo * s * d
    return out


# ---------------------------------------------------------------------------
# 4. TESTS
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def tests():
    res = []

    def t(nombre, cond, msg=""):
        res.append((nombre, bool(cond), msg))

    k = kg_por_ave()
    # U00 fuente de masa: kg/ave idénticos en las 4 escalas y 2 calendarios (linealidad del CSV de escala)
    ok = all(_cerca(kg_por_ave(E, ds)[x], k[x], 1e-6) for E in ESCALAS for ds in CALENDARIOS for x in MASAS)
    t("U00 masas del CSV de escala lineales y coherentes", ok)
    # U01 escalabilidad: duplicar aves duplica todo flujo (no los por-ave ni %)
    ok, n_var = True, 0
    for niv in NIVELES:
        a, b = calcular(5000, 250, niv), calcular(10000, 250, niv)
        for f in a.filas:
            v1, v2 = f["valor"], b[f["variable"]]
            if f["periodo"] in ("por_ave", "adimensional") or f["unidad"] in ("kJ/kg",):
                ok &= _cerca(v1, v2, 1e-9)
            else:
                ok &= _cerca(2 * v1, v2, 1e-9)
            n_var += 1
    t("U01 escalabilidad lineal (duplicar aves duplica flujos; intensivos constantes)", ok, f"{n_var} variables")
    # U02 unidades
    r = calcular(10000, 250, "medio")
    ok = _cerca(r["agua_utilizada_m3_dia"], r["agua_utilizada_l_ave"] * 10000 / 1000)
    ok &= _cerca(r["agua_utilizada_m3_anio"], r["agua_utilizada_m3_dia"] * 250)
    ok &= _cerca(r["tr_enfriado_producto_fresco"] * KW_POR_TR, r["kw_frigorificos_enfriado_producto_fresco"])
    ok &= _cerca(r["energia_combustible_kwh_dia"] * 3.6, r["energia_combustible_mj_dia"])
    ok &= _cerca(r["carga_DQO_kg_dia"], r["carga_DQO_g_ave"] * 10000 / 1000)
    ok &= _cerca(r["concentracion_DQO_mg_l"], r["carga_DQO_g_ave"] / r["agua_descargada_l_ave"] * 1000)
    ok &= 5 <= r["agua_utilizada_l_ave"] <= 60      # rango físico plausible de faena avícola
    t("U02 unidades (L↔m³, día↔año, kW↔TR, MJ↔kWh, g/ave↔kg/día, mg/L)", ok)
    # U03 el agua retenida nunca calcula el consumo
    m2 = dict(k, agua_retenida_producto=k["agua_retenida_producto"] * 3, agua_incorporada=k["agua_incorporada"] * 3)
    r2 = calcular(10000, 250, "medio", masas=m2)
    ok = _cerca(r2["agua_utilizada_m3_dia"], r["agua_utilizada_m3_dia"]) and \
        _cerca(r2["agua_descargada_m3_dia"], r["agua_descargada_m3_dia"])
    ok &= not _cerca(r2["agua_retenida_en_producto_t_dia"], r["agua_retenida_en_producto_t_dia"])
    ok &= _cerca(r["agua_utilizada_l_ave"], sum(nv(v, "medio") for _, _, v, _, _ in AGUA_ETAPAS))
    t("U03 agua retenida separada: triplicarla no cambia agua utilizada ni descargada", ok)
    # U04 cierre del agua
    ok = True
    for niv in NIVELES:
        x = calcular(10000, 250, niv)
        ok &= _cerca(x["agua_utilizada_m3_dia"], x["agua_descargada_m3_dia"] + x["agua_no_descargada_m3_dia"])
        ok &= 0 < x["agua_descargada_m3_dia"] <= x["agua_utilizada_m3_dia"]
        ok &= x["agua_retenida_en_producto_t_dia"] <= x["agua_no_descargada_m3_dia"]
    t("U04 cierre: utilizada = descargada + no descargada; retenida ≤ no descargada", ok)
    # U05 orden bajo < medio < alto en demandas
    rs = [calcular(10000, 250, niv) for niv in NIVELES]
    claves = ("agua_utilizada_m3_dia", "agua_descargada_m3_dia", "carga_DQO_kg_dia", "carga_DBO5_kg_dia",
              "kwh_total_dia_operativo", "kw_potencia_pico_estimada", "energia_combustible_mj_dia",
              "kw_frigorificos_enfriado_producto_fresco", "kw_electricos_enfriado_producto_fresco",
              "lodos_deshidratados_t_dia")
    t("U05 bajo < medio < alto", all(rs[0][c] < rs[1][c] < rs[2][c] for c in claves))
    # U06 etapas suman el total
    ok = all(_cerca(sum(x[f"agua_{c}_m3_dia"] for c, *_ in AGUA_ETAPAS), x["agua_utilizada_m3_dia"]) for x in rs)
    t("U06 Σ etapas = agua utilizada", ok)
    # U07 inventario reproduce el modelo de escala (todas las filas)
    n_ok = n_tot = 0
    for f in leer_escala():
        if f["bloque"] != "inventario" or f["variable"] == "subproductos_perecederos_frio_t":
            continue
        E, da = int(f["escala_aves_dia"]), int(f["dias_anio"])
        par = dict(x.split("=") for x in f["parametro"].split("; "))
        inv = inventario_escala(E, da)
        cat = f["variable"][:-2] if f["variable"] != "comestible_total_t" else "comestible_total"
        v = inv[(par["base_temporal"], int(par["dias"]), par.get("perfil_destino", ""), cat)]
        n_tot += 1
        n_ok += _cerca(v, float(f["valor"]), 1e-6)
    t("U07 inventario = escenarios_escala.csv", n_ok == n_tot and n_tot > 0, f"{n_ok}/{n_tot} filas")
    # U08 días calendario < días de producción; y el cálculo principal respeta la base
    pc = parametros("medio", base_inventario="dias_calendario", perfil=dict(PERFILES["P2"]), perfil_id="P2")
    pp = parametros("medio", perfil=dict(PERFILES["P2"]), perfil_id="P2")
    rc, rp = calcular(10000, 250, p=pc), calcular(10000, 250, p=pp)
    ok = rc["stock_congelado_t"] < rp["stock_congelado_t"]
    ok &= _cerca(rc["stock_congelado_t"], rp["stock_congelado_t"] * 250 / 365)
    ok &= _cerca(rp["stock_congelado_t"], valor_escala(10000, 5, "inventario", "congelado_t", "stock",
                                                        "base_temporal=dias_produccion; dias=14; perfil_destino=P2"), 1e-6)
    t("U08 días calendario = días de producción × días op./365 < días de producción", ok)
    # U09 congelación diaria ≠ almacenamiento
    p1 = parametros("medio", perfil=dict(PERFILES["P3"]), perfil_id="P3", dias_congelado=1)
    p14 = parametros("medio", perfil=dict(PERFILES["P3"]), perfil_id="P3", dias_congelado=28)
    a, b = calcular(10000, 250, p=p1), calcular(10000, 250, p=p14)
    ok = _cerca(a["capacidad_congelacion_t_dia"], b["capacidad_congelacion_t_dia"])
    ok &= _cerca(b["capacidad_almacenamiento_congelado_t"], 28 * a["capacidad_almacenamiento_congelado_t"])
    ok &= _cerca(a["capacidad_almacenamiento_congelado_t"], a["capacidad_congelacion_t_dia"])
    t("U09 capacidad diaria de congelación independiente de los días de stock", ok)
    # U10 kW frigoríficos vs eléctricos; potencia vs energía
    ok = True
    for x in rs:
        for v in ("enfriado_producto_fresco", "congelacion_tuneles", "camaras_almacenamiento"):
            ok &= x[f"kw_electricos_{v}"] < x[f"kw_frigorificos_{v}"]
    t("U10 kW eléctricos = kW frigoríficos / COP (COP > 1)", ok)
    # U11 potencia pico ≥ media; kWh ≠ kW
    ok = all(x["kw_potencia_pico_estimada"] >= x["kw_potencia_media_operacion"] for x in rs)
    ok &= all(x["kwh_total_dia_operativo"] > x["kw_potencia_media_operacion"] for x in rs)
    t("U11 pico ≥ media y energía diaria > potencia", ok)
    # U12 finitos y no negativos en todo el CSV
    filas = construir()
    ok = all(isinstance(f["valor"], (int, float)) and math.isfinite(f["valor"]) and f["valor"] >= 0 for f in filas)
    t("U12 ningún valor negativo ni no finito", ok, f"{len(filas)} valores")
    # U13 sin cifras económicas
    ok = not any(PALABRAS_ECONOMICAS.search(f"{f['variable']} {f['unidad']}") for f in filas)
    t("U13 ninguna variable económica", ok)
    # U14 entradas inválidas detienen el modelo
    malos = 0
    for kw in ({"frac_efluente": 1.2}, {"frac_efluente": 0}, {"l_ave_total": -5}, {"l_ave_total": 25000},
               {"frac_sangre_recuperada": 1.5}, {"perfil": {"refrigerado": 0.7, "congelado": 0.4, "exportacion": 0}},
               {"base_inventario": "semanas"}, {"dias_congelado": -1}):
        try:
            parametros("medio", **kw)
        except ErrorUtilities:
            malos += 1
    for args in ((-100, 250), (10000, 400), (0, 250)):
        try:
            calcular(*args)
        except ErrorUtilities:
            malos += 1
    t("U14 entradas inválidas rechazadas", malos == 11, f"{malos}/11")
    # U15 sangre: menos recuperación = más DQO; recuperación de referencia = balance
    r0 = calcular(10000, 250, p=parametros("medio", frac_sangre_recuperada=0.0))
    ok = r0["carga_DQO_kg_dia"] > r["carga_DQO_kg_dia"]
    ok &= _cerca(r0["carga_DQO_kg_dia"] - r["carga_DQO_kg_dia"], r["dqo_evitada_por_recuperar_sangre_kg_dia"], 1e-9)
    ok &= _cerca(r["dqo_extra_por_sangre_no_recuperada_g_ave"], 0.0)
    ok &= _cerca(k["sangre_recuperada"] / k["sangre_drenada"], 0.85, 1e-6)
    t("U15 DQO extra = sangre no recuperada × DQO de la sangre; referencia 85 % (SUP-040)", ok)
    # U16 masa evitable = CSV de escala
    ok = all(_cerca(calcular(E, 250)[f"{c}_t_dia"], valor_escala(E, 5, "subproductos", v), 1e-6)
             for E in ESCALAS for c, v in (("sangre_recuperada", "sangre_t"),
                                           ("solidos_a_retirar", "solidos_a_retirar_t")))
    t("U16 masa que evita el efluente = balance/escala", ok)
    # U17 perfiles suman 1; concentraciones medias dentro del rango de fuentes
    ok = all(_cerca(sum(s.values()), 1.0) for s in PERFILES.values())
    ok &= RANGO_DQO_FUENTES_MG_L[0] <= r["concentracion_DQO_mg_l"] <= RANGO_DQO_FUENTES_MG_L[1]
    t("U17 perfiles = 100 %; DQO media resultante dentro del rango de fuentes", ok,
      f"{r['concentracion_DQO_mg_l']:.0f} mg/L")
    # U18 energía anual: cámaras 365 días, proceso días de faena
    r3 = calcular(10000, 300, "medio")
    ok = _cerca(r3["kwh_total_anio"] - r["kwh_total_anio"],
                (r["kwh_total_dia_operativo"] - r["kwh_almacenamiento_frio_dia_calendario"]) * 50)
    t("U18 sexto día: +50 días de proceso; cámaras sin cambio (365 días)", ok)
    # U19 l_ave_total escala las etapas en proporción
    pl = parametros("medio", l_ave_total=50)
    x = calcular(10000, 250, p=pl)
    ok = _cerca(x["agua_utilizada_l_ave"], 50) and _cerca(x["agua_evisceracion_l_ave"] / 50,
                                                           r["agua_evisceracion_l_ave"] / r["agua_utilizada_l_ave"])
    t("U19 cambiar L/ave total mantiene el reparto por etapa", ok)
    return res


def correr_tests(verbose=True):
    res = tests()
    if verbose:
        for nombre, ok, msg in res:
            print(f"  {'OK   ' if ok else 'FALLA'} {nombre} {('— ' + msg) if msg else ''}")
    return all(ok for _, ok, _ in res), res


MUTACIONES = {
    "M01": "agua retenida sumada al consumo industrial",
    "M02": "escalado no lineal (aves^1,01)",
    "M03": "se descarga más agua de la utilizada",
    "M04": "kW eléctrico = kW frigorífico (sin COP)",
    "M05": "inventario calendario sin conversión",
    "M06": "almacenamiento congelado = capacidad diaria (ignora días)",
    "M07": "sangre no recuperada no suma DQO",
    "M08": "L/ave interpretados como m³/ave",
    "M09": "potencia pico menor que la media",
}


def mutaciones():
    print("Prueba de mutación (cada mutación debe hacer fallar al menos un test):")
    todas = True
    for m, desc in MUTACIONES.items():
        _MUT.clear()
        _MUT.add(m)
        try:
            _, res = correr_tests(verbose=False)
            fallan = [n.split()[0] for n, ok, _ in res if not ok]
        except (ErrorUtilities, ZeroDivisionError, KeyError) as e:
            fallan = [f"detiene: {e}"]
        _MUT.clear()
        print(f"  {m} {desc}: {'DETECTADA por ' + ', '.join(fallan) if fallan else 'NO DETECTADA'}")
        todas &= bool(fallan)
    return todas


# ---------------------------------------------------------------------------
# 5. CSV
# ---------------------------------------------------------------------------
CAMPOS = ["bloque", "escala_aves_dia", "dias_semana", "dias_anio", "nivel", "parametro", "variable", "valor",
          "unidad", "periodo", "base", "origen", "clasificacion", "referencia", "nota"]


def construir():
    filas = []
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            for niv in NIVELES:
                for f in calcular(E, da, niv).filas:
                    filas.append(dict(f, escala_aves_dia=E, dias_semana=ds, dias_anio=da, nivel=niv))
                for pid in ("P2", "P3"):          # perfil de frío (P1 ya está en el bloque principal)
                    p = parametros(niv, perfil=dict(PERFILES[pid]), perfil_id=pid)
                    r = calcular(E, da, niv, p=p)
                    for var in ("capacidad_congelacion_t_dia", "capacidad_almacenamiento_congelado_t",
                                "stock_refrigerado_t", "kw_frigorificos_congelacion_tuneles",
                                "kw_electricos_congelacion_tuneles", "kw_frigorificos_camaras_almacenamiento",
                                "kwh_congelacion_dia", "kwh_almacenamiento_frio_dia_calendario",
                                "kw_respaldo_cargas_criticas"):
                        f = next(x for x in r.filas if x["variable"] == var)
                        filas.append(dict(f, bloque="perfil_frio", escala_aves_dia=E, dias_semana=ds, dias_anio=da,
                                          nivel=niv, parametro=f"perfil={pid}"))
            for (base, d, pid, cat), v in inventario_escala(E, da).items():
                filas.append({"bloque": "inventario", "escala_aves_dia": E, "dias_semana": ds, "dias_anio": da,
                              "nivel": "-", "parametro": f"base_temporal={base}; dias={d}"
                                                         + (f"; perfil_destino={pid}" if pid else ""),
                              "variable": f"{cat}_t", "valor": v, "unidad": "t", "periodo": "stock",
                              "base": "comercial", "origen": "ESTIMACIÓN", "clasificacion": "[ESTIMACIÓN]",
                              "referencia": "SUP-055, SUP-056; = escenarios_escala.csv",
                              "nota": "días de producción" if base == "dias_produccion" else
                              "días calendario de cobertura (× días op./365)"})
    # tabla de parámetros
    for c, etq, vals, org, ref in AGUA_ETAPAS:
        for niv in NIVELES:
            filas.append({"bloque": "parametros", "escala_aves_dia": 0, "dias_semana": 0, "dias_anio": 0,
                          "nivel": niv, "parametro": "", "variable": f"param_agua_{c}_l_ave", "valor": nv(vals, niv),
                          "unidad": "L/ave", "periodo": "por_ave", "base": "agua_utilizada", "origen": org,
                          "clasificacion": f"[{org}]" + (" [PVDP]" if org == "FUENTE" else ""),
                          "referencia": ref, "nota": etq})
    for par, (vals, ref) in CARGA_G_AVE.items():
        for niv in NIVELES:
            filas.append({"bloque": "parametros", "escala_aves_dia": 0, "dias_semana": 0, "dias_anio": 0,
                          "nivel": niv, "parametro": "", "variable": f"param_carga_{par}_g_ave", "valor": nv(vals, niv),
                          "unidad": "g/ave", "periodo": "por_ave", "base": "efluente_crudo", "origen": "ESTIMACIÓN",
                          "clasificacion": "[ESTIMACIÓN] con rangos [PVDP]", "referencia": ref, "nota": ""})
    for f in filas:
        f["valor"] = round(float(f["valor"]), 6)
    return filas


def escribir_csv(filas):
    with open(CSV_SALIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


# ---------------------------------------------------------------------------
# 6. TABLAS Y CLI
# ---------------------------------------------------------------------------
def fmt(x, d=1):
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tablas():
    rs = {(E, n): calcular(E, 250, n) for E in ESCALAS for n in NIVELES}
    filas = [
        ("Agua utilizada m³/día (bajo · medio · alto)", "agua_utilizada_m3_dia", 0),
        ("Agua descargada m³/día", "agua_descargada_m3_dia", 0),
        ("Caudal medio / pico m³/h (medio)", None, 0),
        ("Agua retenida en producto t/día", "agua_retenida_en_producto_t_dia", 2),
        ("DQO kg/día", "carga_DQO_kg_dia", 0), ("DBO5 kg/día", "carga_DBO5_kg_dia", 0),
        ("SST kg/día", "carga_SST_kg_dia", 0), ("GyA kg/día", "carga_GyA_kg_dia", 0),
        ("NTK kg/día", "carga_NTK_kg_dia", 0),
        ("DQO evitada por recuperar sangre kg/día", "dqo_evitada_por_recuperar_sangre_kg_dia", 0),
        ("Sólidos a retirar en seco t/día", "solidos_a_retirar_t_dia", 1),
        ("Lodos deshidratados t/día", "lodos_deshidratados_t_dia", 1),
        ("Electricidad kWh/día operativo (total)", "kwh_total_dia_operativo", 0),
        ("Electricidad MWh/año", None, 0),
        ("kWh/ave (promedio anual)", "kwh_por_ave_promedio_anual", 2),
        ("Potencia media / pico kW", None, 0),
        ("Calor combustible GJ/día", None, 1),
        ("Gas natural equivalente m³/día", "equivalente_gas_natural_m3_dia", 0),
        ("Frío enfriado fresco kW frig (TR)", None, 0),
        ("Congelación P1 t/día · kW frig", None, 1),
        ("Stock refrigerado 3 d prod. P1 t", "stock_refrigerado_t", 0),
        ("Stock congelado 14 d prod. P1 t", "stock_congelado_t", 0),
        ("Respaldo crítico kVA", "kva_respaldo_cargas_criticas", 0),
        ("Respaldo planta completa kVA", "kva_respaldo_planta_completa", 0),
    ]
    print("| Variable | " + " | ".join(fmt(E, 0) for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for etq, var, d in filas:
        celdas = []
        for E in ESCALAS:
            b, m, a = (rs[(E, n)] for n in NIVELES)
            if var:
                celdas.append(" · ".join(fmt(x[var], d) for x in (b, m, a)))
            elif etq.startswith("Caudal"):
                celdas.append(f"{fmt(m['agua_utilizada_m3_h_medio'])} / {fmt(m['agua_utilizada_m3_h_pico'])}")
            elif etq.startswith("Electricidad MWh"):
                celdas.append(" · ".join(fmt(x["kwh_total_anio"] / 1000, 0) for x in (b, m, a)))
            elif etq.startswith("Potencia"):
                celdas.append(" · ".join(f"{fmt(x['kw_potencia_media_operacion'], 0)}/{fmt(x['kw_potencia_pico_estimada'], 0)}"
                                         for x in (b, m, a)))
            elif etq.startswith("Calor"):
                celdas.append(" · ".join(fmt(x["energia_combustible_mj_dia"] / 1000, 1) for x in (b, m, a)))
            elif etq.startswith("Frío"):
                celdas.append(" · ".join(f"{fmt(x['kw_frigorificos_enfriado_producto_fresco'], 0)} "
                                         f"({fmt(x['tr_enfriado_producto_fresco'], 0)})" for x in (b, m, a)))
            elif etq.startswith("Congelación"):
                celdas.append(f"{fmt(m['capacidad_congelacion_t_dia'], 1)} · "
                              + " / ".join(fmt(x["kw_frigorificos_congelacion_tuneles"], 0) for x in (b, m, a)))
        print(f"| {etq} | " + " | ".join(celdas) + " |")


def escenario_cli(a):
    ov = {}
    if a.l_ave is not None:
        ov["l_ave_total"] = a.l_ave
    if a.frac_efluente is not None:
        ov["frac_efluente"] = a.frac_efluente
    if a.dqo_g_ave is not None:
        c = {k: nv(v, a.nivel) for k, v in CARGA_G_AVE.items()}
        f = a.dqo_g_ave / c["DQO"]
        ov["carga_g_ave"] = {k: v * f for k, v in c.items()}   # todos los parámetros en proporción a la DQO
    if a.frac_sangre is not None:
        ov["frac_sangre_recuperada"] = a.frac_sangre
    if a.perfil:
        x = [float(v) for v in a.perfil.split(",")]
        ov["perfil"] = dict(zip(("refrigerado", "congelado", "exportacion"), x))
        ov["perfil_id"] = "manual"
    for k in ("dias_refrigerado", "dias_congelado", "base_inventario", "horas_netas"):
        if getattr(a, k) is not None:
            ov[k] = getattr(a, k)
    r = calcular(a.aves_dia, a.dias_anio, a.nivel, p=parametros(a.nivel, **ov))
    print(f"Escenario: {fmt(a.aves_dia, 0)} aves/día · {a.dias_anio} días/año · nivel {a.nivel}")
    for f in r.filas:
        print(f"  {f['bloque']:<14} {f['variable']:<52} {fmt(f['valor'], 2):>14} {f['unidad']:<16} {f['clasificacion']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--tablas", action="store_true")
    ap.add_argument("--escenario", action="store_true")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--dias-anio", type=int, default=250)
    ap.add_argument("--nivel", choices=NIVELES, default="medio")
    ap.add_argument("--l-ave", type=float, help="agua utilizada total L/ave (reparte por etapa en proporción)")
    ap.add_argument("--frac-efluente", type=float)
    ap.add_argument("--dqo-g-ave", type=float, help="carga DQO g/ave (DBO, SST, GyA, NTK, PT en proporción)")
    ap.add_argument("--frac-sangre", type=float, help="fracción de sangre recuperada (0–1)")
    ap.add_argument("--perfil", help="refrigerado,congelado,exportacion (fracciones que suman 1)")
    ap.add_argument("--dias-refrigerado", type=float)
    ap.add_argument("--dias-congelado", type=float)
    ap.add_argument("--base-inventario", choices=("dias_produccion", "dias_calendario"))
    ap.add_argument("--horas-netas", type=float)
    a = ap.parse_args()
    try:
        if a.mutaciones:
            sys.exit(0 if mutaciones() else 1)
        print(f"Modelo de utilities v{VERSION} ({FECHA}) — tests:")
        ok, _ = correr_tests()
        if not ok:
            print("TESTS FALLIDOS: el modelo se detiene.")
            sys.exit(1)
        if a.escenario:
            escenario_cli(a)
            return
        if a.tablas:
            tablas()
        if not a.solo_tests:
            filas = construir()
            escribir_csv(filas)
            print(f"CSV escrito: {os.path.relpath(CSV_SALIDA, RAIZ)} ({len(filas)} filas)")
    except ErrorUtilities as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
