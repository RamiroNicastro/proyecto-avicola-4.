#!/usr/bin/env python3
"""
MODELO PRELIMINAR DE UTILITIES — versión 1.1 (2026-09-30, sesión 09C, auditoría conceptual)
==========================================================================================

AGUA INDUSTRIAL -> EFLUENTES -> ENERGÍA ELÉCTRICA -> AGUA CALIENTE/VAPOR -> FRÍO INDUSTRIAL
-> CONGELADO -> RESPALDO, para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo
(o cualquier valor con --aves-dia).

ESTADO: modelo TOP-DOWN de SENSIBILIDAD para prefactibilidad. Los rangos bajo/medio/alto NO son el
consumo esperado de la futura planta ni especificaciones de diseño. NO selecciona equipos, NO calcula
CAPEX ni OPEX, NO asigna precios, NO elige tecnología de tratamiento, refrigerante, fuente térmica ni
generador, NO elige ubicación. Ninguna cifra es un dato de campo argentino.

v1.1 (auditoría conceptual):
  * Agua: cinco conceptos (captada, utilizada, incorporada al producto/subproductos, evaporada o
    arrastrada, descargada); fracción a efluente = SUPUESTO editable; segunda unidad m³/t de producto.
  * Efluentes: dos métodos INDEPENDIENTES (A carga específica g/ave; B caudal × concentración); nunca se
    calibra uno con el otro; si divergen más que la tolerancia, alerta "DATOS DE EFLUENTE REQUIEREN
    VALIDACIÓN DE CAMPO".
  * Límites de vuelco: solo EJEMPLOS REGULATORIOS con jurisdicción, autoridad, norma y tipo de descarga.
  * Subproductos del balance = masa potencialmente segregable en origen; NO son SST del efluente. Los
    sólidos que efectivamente entran al efluente quedan PENDIENTES (dependen del diseño y la operación).
  * Lodos: PENDIENTE DE DIMENSIONAMIENTO salvo que se carguen explícitamente SST removidos, químicos,
    biomasa y % de sólidos de torta (escenario ilustrativo con cada supuesto visible).
  * Energía: kWh/ave -> energía diaria -> POTENCIA MEDIA EQUIVALENTE bajo X horas. La POTENCIA PICO, la
    potencia contratada, el transformador y el generador NO se calculan desde kWh: quedan PENDIENTES
    hasta tener una lista de cargas (kW nominal, factor de carga, simultaneidad, arranque, cos φ).
  * Calor: MJ/día y potencia térmica media equivalente; el pico térmico queda PENDIENTE (perfil horario).
  * Frío: "carga sensible preliminar asociada al enfriamiento del producto" (no es la capacidad
    frigorífica de planta); la carga frigorífica total queda PENDIENTE (balance frigorífico). kW
    eléctricos aproximados = kW frigoríficos / COP supuesto, con el COP declarado en el CSV.
  * Respaldo: "carga crítica ilustrativa de escenario" (proxy); el grupo electrógeno queda PENDIENTE.
  * Contraste futuro TOP-DOWN (este modelo) vs BOTTOM-UP (equipos de 09A cotizados): función
    `contraste_bottom_up`; las diferencias generan alerta.

FUENTE DE VERDAD DE LA MASA: 23_plan_expansion/escenarios_escala.csv (modelo de escala v1.1 <- balance
de masa v1.1 <- subproductos v1.0). Este modelo solo LEE ese CSV (kg/ave = valor / escala).

Uso
---
    python3 11_agua_efluentes/modelo_utilities.py                 # tests + CSV
    python3 11_agua_efluentes/modelo_utilities.py --solo-tests     # solo pruebas
    python3 11_agua_efluentes/modelo_utilities.py --mutaciones     # prueba de mutación de los tests
    python3 11_agua_efluentes/modelo_utilities.py --tablas         # tablas resumen para los .md
    python3 11_agua_efluentes/modelo_utilities.py --escenario --aves-dia 7500 --nivel medio \
        --l-ave 22 --frac-efluente 0.9 --dqo-g-ave 90 --dqo-mg-l 4000 --frac-sangre 0.9 \
        --perfil 0.6,0.4,0 --dias-refrigerado 3 --dias-congelado 14 --base-inventario dias_calendario

El script se DETIENE (código 1) si falla cualquier prueba.

------------------------------------------------------------------------------
AGUA — CINCO CONCEPTOS QUE NO SE MEZCLAN
------------------------------------------------------------------------------
  CAPTADA/COMPRADA   = utilizada / (1 − fracción de rechazo de potabilización)   [SUPUESTO: 0 si no hay
                       potabilización con rechazo; dato de sitio]
  UTILIZADA en proceso = Σ etapas L/ave × aves / 1.000          (RANGO DE SENSIBILIDAD 15/25/38 L/ave)
  INCORPORADA al producto y subproductos = kg/ave del balance v1.1 (retenida en producto, goteo del
                       producto y adherida a plumas). NUNCA calcula el consumo.
  DESCARGADA (efluente) = utilizada × fracción a efluente       [SUPUESTO editable; la relación no es fija]
  EVAPORADA o ARRASTRADA = utilizada − descargada − incorporada  (por diferencia; si es < 0, alerta)
  Segunda unidad: m³ de agua utilizada / t de producto comestible (peso comercial), contrastada con el
  rango de fuentes (3,8–17,9 m³/t de carcasa, FTE-09C-04 [PVDP]; base distinta: solo contraste).

------------------------------------------------------------------------------
EFLUENTES — DOS MÉTODOS INDEPENDIENTES
------------------------------------------------------------------------------
  MÉTODO A (carga específica):     kg/día = aves/día × g/ave / 1.000
  MÉTODO B (caudal × concentración): kg/día = m³ efluente/día × mg/L / 1.000
  Relación B/A; si B/A > tolerancia o < 1/tolerancia (tolerancia = 2, SUPUESTO editable) -> alerta.
  Remoción bajo EJEMPLO de límite = 1 − límite / concentración (con jurisdicción y tipo de descarga).

------------------------------------------------------------------------------
ENERGÍA, CALOR, FRÍO, RESPALDO
------------------------------------------------------------------------------
  Energía eléctrica de proceso [kWh/día] = kWh/t de peso vivo × t vivas/día (≡ aves × kWh/ave)
  Potencia media equivalente [kW] = kWh/día / horas consideradas   (el nombre incluye "_bajo_<h>h")
  Potencia pico / demanda máxima = Σ (kW nominal × factor de carga × simultaneidad) + arranque del mayor
     motor; kVA = kW / cos φ  -> SOLO desde una lista de cargas; si no existe: PENDIENTE.
  Calor útil [MJ/día] = Σ L × 4,186 × ΔT (× pérdidas) × aves / 1.000; potencia térmica media equivalente
     = MJ/día / (horas × 3,6); pico térmico: PENDIENTE (perfil horario y simultaneidad).
  Carga sensible preliminar del producto [kJ/ave] = kg comestible × cp × (T_entrada − T_salida)
     (enfriamiento del agua de reposición del chiller y cargas adicionales: filas separadas, no sumadas
     como capacidad total; la carga frigorífica total queda PENDIENTE: balance frigorífico)
  Calor de congelación del producto [kJ/kg] = cp_f × (T_ent − T_cong) + x_agua × 334 + cp_c × (T_cong − T_fin)
  kW eléctricos aproximados = kW frigoríficos / COP supuesto (fila cop_supuesto_* en el CSV)
  CAPACIDAD DE CONGELACIÓN [t/día op.] = t NUEVAS que deben atravesar la congelación por día
  CAPACIDAD DE ALMACENAMIENTO [t]      = t YA congeladas que permanecen guardadas
     días de producción: flujo = producción/día operativo; días calendario: × días op./365
  Carga crítica ilustrativa [kW] = proxy de sensibilidad; generador: PENDIENTE (lista de cargas críticas)

Unidades: aves; L; m³; kg; t; kWh; kW; kJ; MJ; TR; mg/L; h. Separador decimal del CSV: punto.
Columna `origen`: FUENTE ([PVDP] en esta sesión) / ESTIMACIÓN / SUPUESTO / PENDIENTE (valor vacío).
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import sys

sys.dont_write_bytecode = True

VERSION = "1.1"
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
PENDIENTE = None                                    # valor aún no calculable (se escribe vacío en el CSV)
ALERTA_EFLUENTE = "DATOS DE EFLUENTE REQUIEREN VALIDACIÓN DE CAMPO"

_MUT: set = set()                                   # mutaciones activas (solo --mutaciones)


class ErrorUtilities(Exception):
    """Parámetro inválido o inconsistencia: detiene el modelo."""


# ---------------------------------------------------------------------------
# 1. PARÁMETROS  (valor bajo / medio / alto; origen; referencia)
#    "bajo/medio/alto" = nivel de DEMANDA del servicio (bajo = planta más eficiente).
#    Son RANGOS DE SENSIBILIDAD PRELIMINAR, no consumos esperados ni especificaciones.
#    Referencias FTE-09C-xx: 11_agua_efluentes/fuentes_09C.csv (todas [PVDP])
# ---------------------------------------------------------------------------
# 1.1 Agua utilizada en proceso por etapa [L/ave faenada]. Totales 15/25/38 calibrados a rangos de fuentes
#     (13,2–37,8 L/ave; 22–30 L/ave; 26 L/ave; FTE-09C-01 a 04); reparto por etapa: SUPUESTO.
AGUA_ETAPAS = [
    # clave, etiqueta, (bajo, medio, alto), origen, referencia
    ("recepcion", "Recepción: lavado de jaulas/módulos, camiones y andén", (0.5, 1.0, 2.0), "SUPUESTO",
     "sin fuente por ave"),
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
RANGO_L_AVE_FUENTES = (13.2, 37.8)                  # FTE-09C-02 [PVDP]
RANGO_M3_T_FUENTES = (3.8, 17.9)                    # m³/t de CARCASA, FTE-09C-04 [PVDP] (base distinta)
FRAC_EFLUENTE = ((0.80, 0.88, 0.95), "SUPUESTO",
                 "fracción del agua utilizada que se descarga; SUPUESTO editable: la relación NO es fija "
                 "(depende de evaporación, arrastre con subproductos y lodos, reúso y fugas)")
FRAC_RECHAZO_POTABILIZACION = 0.0                   # SUPUESTO editable: dato de sitio (p. ej. ósmosis)
FACTOR_MAXIMO_HORARIO_AGUA = ((1.5, 1.8, 2.2), "SUPUESTO", "caudal horario máximo / medio (ilustrativo)")
HORAS_NETAS = 8                                     # SUP-053 (sensibilidad en el modelo de escala)
HORAS_LIMPIEZA = 4                                  # SUPUESTO: ventana de limpieza diaria
HORAS_ARRANQUE_CIERRE = 2                           # SUPUESTO

# 1.2 Efluentes. MÉTODO A: carga específica [g/ave] (escenarios [PVDP], con sangre recuperada al 85 %,
#     SUP-040). MÉTODO B: concentración [mg/L] (valores citados en fuentes [PVDP]). Independientes:
#     ninguno se calibra con el otro.
CARGA_G_AVE = {
    "DQO": ((50.0, 100.0, 180.0), "escenario [PVDP] (FTE-181; FTE-09C-05)"),
    "DBO5": ((25.0, 50.0, 90.0), "escenario [PVDP] (FTE-181; FTE-09C-05)"),
    "SST": ((15.0, 35.0, 80.0), "escenario [PVDP] (FTE-181; FTE-09C-05)"),
    "GyA": ((5.0, 11.0, 25.0), "escenario [PVDP] (FTE-09C-06)"),
    "NTK": ((3.0, 5.0, 8.0), "escenario [PVDP] (FTE-09C-06)"),
    "PT": ((0.3, 0.5, 1.0), "escenario [PVDP] (FTE-09C-06)"),
}
CONC_MG_L = {  # MÉTODO B: solo parámetros con rangos de concentración citados
    "DQO": ((2000.0, 5400.0, 9695.0), "promedio ~2.000; centro de 3.154–7.719; máx. 9.695 mg/L (FTE-09C-05)"),
    "DBO5": ((970.0, 1600.0, 2900.0), "~970–2.900; centro de 1.341–1.821 mg/L (FTE-181; FTE-09C-05)"),
    "SST": ((378.0, 1410.0, 5462.0), "378–5.462 mg/L; caso 1.410 mg/L (FTE-09C-05; FTE-09C-07)"),
}
RANGO_DQO_FUENTES_MG_L = (1223.0, 9695.0)           # FTE-09C-05 [PVDP]
TOLERANCIA_METODOS = 2.0                            # SUPUESTO editable: B/A fuera de [1/2, 2] -> alerta
DQO_SANGRE_KG_KG = 375.0 / 1.05 / 1000             # 375.000 mg/L = 375 g/L ÷ 1,05 kg/L = 0,357 kg/kg (FTE-181)
# Ejemplos regulatorios de referencia (NO requisitos del proyecto): la localización los reemplazará.
LIMITES_EJEMPLO = [
    {"parametro": "DQO", "mg_l": 250.0, "jurisdiccion": "Provincia de Buenos Aires", "autoridad": "ADA",
     "norma": "Res. ADA 336/2003", "tipo_descarga": "conducto pluvial", "ref": "FTE-09C-08 [PVDP]"},
    {"parametro": "DBO5", "mg_l": 50.0, "jurisdiccion": "Provincia de Buenos Aires", "autoridad": "ADA",
     "norma": "Res. ADA 336/2003", "tipo_descarga": "conducto pluvial", "ref": "FTE-09C-08 [PVDP]"},
]
CAMPOS_LIMITE = ("parametro", "mg_l", "jurisdiccion", "autoridad", "norma", "tipo_descarga")

# 1.3 Lodos: escenario ILUSTRATIVO (cada supuesto visible y editable). Por defecto el modelo NO calcula
#     lodos (PENDIENTE DE DIMENSIONAMIENTO).
LODOS_ILUSTRATIVO = {  # clave: ((bajo, medio, alto), unidad, origen, referencia)
    "rem_sst_separacion_mecanica_y_daf": ((0.70, 0.54, 0.38), "fracción", "FUENTE",
                                          "DAF 38–70 % SST (FTE-09C-05 [PVDP])"),
    "rem_grasas_daf": ((0.95, 0.80, 0.63), "fracción", "FUENTE", "DAF 63–95 % grasas (FTE-09C-05 [PVDP])"),
    "dosis_quimicos_g_m3": ((50.0, 100.0, 200.0), "g/m³", "SUPUESTO", "coagulante + floculante; sin fuente"),
    "rem_dbo_daf": ((0.60, 0.45, 0.30), "fracción", "FUENTE", "DAF 30–90 % DBO (FTE-09C-05 [PVDP])"),
    "remocion_dbo_biologico": ((0.95, 0.95, 0.95), "fracción", "SUPUESTO", ""),
    "rendimiento_biomasa_kg_ms_kg_dbo": ((0.30, 0.40, 0.50), "kg MS/kg DBO", "SUPUESTO",
                                         "tecnología aerobia; anaerobia genera mucho menos"),
    "fraccion_solidos_torta": ((0.20, 0.18, 0.15), "fracción", "SUPUESTO", "tras deshidratación"),
}
KWH_KG_DBO = ((0.7, 1.2, 2.0), "SUPUESTO", "kWh eléctricos por kg de DBO removida (tratamiento aerobio)")
REM_DBO_PRETRAT_ENERGIA = ((0.60, 0.45, 0.30), "FUENTE", "DAF 30–90 % DBO (FTE-09C-05 [PVDP])")

# 1.4 Electricidad (indicadores TOP-DOWN)
KWH_T_PV = ((150.0, 250.0, 450.0), "FUENTE",
            "UE 152–860 kWh/t faenada; Brasil 165 kWh/t; 1,19 MJ/kg = 330 kWh/t (FTE-09C-09, FTE-09C-03)")
KWH_T_CONGELADA = ((120.0, 190.0, 260.0), "FUENTE", "120–260 kWh/t de ave congelada; 133 kWh/t (FTE-09C-10)")
KWH_T_DIA_REFRIGERADO = ((0.5, 1.0, 2.0), "SUPUESTO", "cámara 0–4 °C, por t almacenada y día; sin fuente")
KWH_T_DIA_CONGELADO = ((1.5, 3.0, 5.0), "SUPUESTO", "cámara −18/−25 °C, por t almacenada y día; sin fuente")
REPARTO_ELECTRICO = {"frio_de_proceso_agua_helada_hielo": 0.35, "motores_de_linea_y_transportadores": 0.20,
                     "aire_comprimido": 0.10, "bombas_agua_y_efluentes": 0.10, "climatizacion_salas": 0.08,
                     "iluminacion": 0.07, "oficinas_vestuarios_servicios": 0.05, "otros": 0.05}  # SUPUESTO didáctico

# 1.5 Agua caliente / vapor
T_RED = 18.0                                        # SUPUESTO
T_ESCALDADO = ((54.0, 58.0, 62.0), "FUENTE", "suave 51–54 °C; fuerte 60–66 °C (FTE-09C-11)")
FACTOR_PERDIDAS_ESCALDADO = ((1.5, 2.0, 3.0), "SUPUESTO", "calor a las aves, evaporación y pérdidas")
T_LIMPIEZA = ((50.0, 55.0, 60.0), "FUENTE", "lavado 49–71 °C (FTE-09C-11)")
FRAC_LIMPIEZA_CALIENTE = ((0.5, 0.6, 0.7), "SUPUESTO", "")
T_ESTERILIZACION = 82.0                             # FUENTE: 82–93 °C (FTE-09C-11) [PVDP]
FRAC_SANITIZACION_CALIENTE = ((0.3, 0.5, 0.7), "SUPUESTO", "")
RENDIMIENTO_TERMICO = ((0.85, 0.75, 0.65), "SUPUESTO", "generación + distribución de calor")
PCI_MJ = {"gas_natural_m3": (38.9, "SUPUESTO", "~9.300 kcal/m³ (a verificar con distribuidora)"),
          "glp_kg": (46.0, "SUPUESTO", "~11.000 kcal/kg"),
          "biomasa_chip_kg": (14.0, "SUPUESTO", "chip de madera ~20–25 % humedad; muy variable")}

# 1.6 Frío (propiedades y temperaturas: SUPUESTOS salvo lo indicado)
T_ENTRADA_CARCASA, T_SALIDA_CARCASA, T_AGUA_CHILLER = 38.0, 4.0, 1.0
CP_FRESCO, CP_CONGELADO = 3.5, 1.8                  # kJ/(kg·K) típicos (ASHRAE, FTE-09C-14 [PVDP])
T_CONGELACION_INICIAL, T_FINAL_CONGELADO = -1.5, -18.0
FRAC_AGUA_PRODUCTO, CALOR_LATENTE_AGUA = 0.74, 334.0  # latente = x_agua × 334 kJ/kg (FTE-09C-14)
FRAC_CARGAS_ADICIONALES = ((0.25, 0.40, 0.60), "SUPUESTO",
                           "ilustrativo: salas, docks, infiltración, motores e iluminación; NO es balance")
HORAS_TUNEL = 20                                    # SUPUESTO: horas/día de congelación (media)
COP_ENFRIADO = ((4.0, 3.0, 2.3), "SUPUESTO", "agua helada / hielo, evaporación ~−5/0 °C")
COP_CONGELADO = ((1.8, 1.4, 1.1), "SUPUESTO", "túnel, evaporación ~−35/−40 °C")

# 1.7 Inventario (mismos perfiles y definiciones que el modelo de escala; SUP-055, SUP-056)
PERFILES = {"P1": {"refrigerado": 0.90, "congelado": 0.10, "exportacion": 0.00},
            "P2": {"refrigerado": 0.60, "congelado": 0.40, "exportacion": 0.00},
            "P3": {"refrigerado": 0.50, "congelado": 0.30, "exportacion": 0.20}}
DIAS_INVENTARIO = (1, 3, 7, 14)
DIAS_REFRIGERADO_DEF, DIAS_CONGELADO_DEF = 3, 14
FRAC_GARRAS_CONGELADAS = ((0.0, 1.0, 1.0), "SUPUESTO", "")
FRAC_MENUDENCIAS_CONGELADAS = ((0.0, 0.5, 1.0), "SUPUESTO", "")

# 1.8 Respaldo: PROXY ILUSTRATIVO (fracciones de la potencia MEDIA equivalente de proceso)
FACTOR_REARRANQUE = ((1.3, 1.5, 2.0), "SUPUESTO", "recuperación de temperatura tras un corte")
FRAC_CRITICA_ILUSTRATIVA = {"control_it_seguridad": 0.03, "iluminacion_emergencia": 0.015,
                            "bombeo_agua_minimo": 0.045, "anden_aves_ventilacion": 0.03}  # SUPUESTO
FRAC_EFLUENTE_MINIMO = 0.5                          # SUPUESTO
TOLERANCIA_BOTTOM_UP = 1.5                          # SUPUESTO editable: top-down vs bottom-up

PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen|"
                                 r"ingreso|ingresos|rentabilidad)\b|\$", re.IGNORECASE)


def nv(param, nivel):
    """Valor de un parámetro (tupla de 3 o (tupla, ...)) para el nivel."""
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
# 3. FUNCIONES AUXILIARES: límites, lodos, lista de cargas, contraste bottom-up
# ---------------------------------------------------------------------------
def validar_limite(lim):
    """Un límite regulatorio solo se usa si declara jurisdicción, autoridad, norma y tipo de descarga."""
    for c in CAMPOS_LIMITE:
        if lim.get(c) in (None, "") and "M19" not in _MUT:
            raise ErrorUtilities(f"Límite sin '{c}': todo límite debe asociarse a jurisdicción y tipo de descarga")
    return lim


def remocion_bajo_ejemplo(conc_mg_l, lim):
    validar_limite(lim)
    return max(0.0, 1 - lim["mg_l"] / conc_mg_l) if conc_mg_l else 0.0


def lodos(sst_kg, gya_kg, dbo_kg, m3_efluente, prm):
    """Cadena explícita: SST removidos + grasas flotadas + químicos + biomasa -> kg sólidos secos ->
    % sólidos de torta -> t húmedas. Cualquier eslabón sin parámetro -> PENDIENTE (None)."""
    prm = prm or {}
    g = prm.get
    sst_rem = sst_kg * g("rem_sst_separacion_mecanica_y_daf") if g("rem_sst_separacion_mecanica_y_daf") is not None \
        else PENDIENTE
    gya_rem = gya_kg * g("rem_grasas_daf") if g("rem_grasas_daf") is not None else PENDIENTE
    quim = m3_efluente * g("dosis_quimicos_g_m3") / 1000 if g("dosis_quimicos_g_m3") is not None else PENDIENTE
    if None not in (g("rem_dbo_daf"), g("remocion_dbo_biologico"), g("rendimiento_biomasa_kg_ms_kg_dbo")):
        biomasa = dbo_kg * (1 - g("rem_dbo_daf")) * g("remocion_dbo_biologico") * g("rendimiento_biomasa_kg_ms_kg_dbo")
    else:
        biomasa = PENDIENTE
    comps = (sst_rem, gya_rem, quim, biomasa)
    if "M14" in _MUT:
        seco = 2400.0 * 0.18                                  # M14: lodo seco fijo sin modelo
    else:
        seco = sum(comps) if None not in comps else PENDIENTE
    pct = g("fraccion_solidos_torta")
    if "M13" in _MUT and pct is None:
        pct = 0.18                                            # M13: % de sólidos por defecto
    humedo = seco / pct / 1000 if (seco is not None and pct) else PENDIENTE
    return {"sst_removidos_kg_dia": sst_rem, "grasas_flotadas_kg_dia": gya_rem, "solidos_quimicos_kg_dia": quim,
            "biomasa_kg_ms_dia": biomasa, "lodo_solidos_secos_kg_dia": seco, "lodo_humedo_t_dia": humedo}


CAMPOS_CARGA = ("equipo", "kw_nominal", "factor_carga", "simultaneidad", "cos_phi")


def demanda_maxima(lista):
    """Potencia pico / demanda máxima desde una LISTA DE CARGAS (única vía admitida).
    Cada carga: equipo, kw_nominal, factor_carga, simultaneidad, cos_phi y opcional factor_arranque."""
    if not lista:
        return PENDIENTE, PENDIENTE
    kw = kva = 0.0
    arranque_extra = 0.0
    for c in lista:
        for campo in CAMPOS_CARGA:
            if c.get(campo) in (None, ""):
                raise ErrorUtilities(f"Carga sin '{campo}': {c}")
        if not (0 < c["cos_phi"] <= 1 and 0 <= c["factor_carga"] <= 1 and 0 <= c["simultaneidad"] <= 1):
            raise ErrorUtilities(f"Carga con factores fuera de rango: {c}")
        p = c["kw_nominal"] * c["factor_carga"] * c["simultaneidad"]
        kw += p
        kva += p / c["cos_phi"]
        arranque_extra = max(arranque_extra, c["kw_nominal"] * (c.get("factor_arranque", 1.0) - 1))
    return kw + arranque_extra, kva + arranque_extra / 0.8


def contraste_bottom_up(r, equipos, tolerancia=TOLERANCIA_BOTTOM_UP):
    """Compara el modelo TOP-DOWN (r) con la suma BOTTOM-UP de equipos (futuro: matriz de equipos de 09A
    + cotizaciones). Cada equipo puede declarar kw_nominal, factor_carga, horas_dia, agua_m3_dia,
    calor_util_mj_dia y frio_kwf. Devuelve filas de contraste y alertas (no ajusta ningún valor)."""
    bu = {"kwh_proceso_dia": sum(e.get("kw_nominal", 0) * e.get("factor_carga", 1) * e.get("horas_dia", 0)
                                 for e in equipos),
          "agua_utilizada_m3_dia": sum(e.get("agua_m3_dia", 0) for e in equipos),
          "calor_util_mj_dia": sum(e.get("calor_util_mj_dia", 0) for e in equipos),
          "carga_sensible_preliminar_producto_kwf_bajo_8h": sum(e.get("frio_kwf", 0) for e in equipos)}
    filas, alertas = [], []
    for k, v_bu in bu.items():
        v_td = r[k]
        if not v_bu or v_td is None:
            continue
        ratio = v_bu / v_td
        filas.append((k, v_td, v_bu, ratio))
        if not 1 / tolerancia <= ratio <= tolerancia:
            alertas.append(f"TOP-DOWN vs BOTTOM-UP: {k} difiere ×{ratio:.2f} (tolerancia ×{tolerancia:g})")
    return filas, alertas


# ---------------------------------------------------------------------------
# 4. CÁLCULO
# ---------------------------------------------------------------------------
class R:
    """Resultados con metadatos (una fila del CSV por variable) y alertas."""

    def __init__(self):
        self.filas, self.v, self.alertas = [], {}, []

    def add(self, bloque, var, val, unidad, periodo, base, origen, clasif, ref="", nota="", parametro=""):
        if var in self.v:
            raise ErrorUtilities(f"Variable duplicada: {var}")
        if val is None:
            origen, clasif = "PENDIENTE", "[PENDIENTE DE DIMENSIONAMIENTO]"
        self.v[var] = val
        self.filas.append({"bloque": bloque, "parametro": parametro, "variable": var, "valor": val,
                           "unidad": unidad, "periodo": periodo, "base": base, "origen": origen,
                           "clasificacion": clasif, "referencia": ref, "nota": nota})

    def alerta(self, codigo, mensaje):
        self.alertas.append((codigo, mensaje))

    def __getitem__(self, k):
        return self.v[k]


def parametros(nivel="medio", **ov):
    """Parámetros del nivel; ov reemplaza cualquiera (validados)."""
    if nivel not in NIVELES:
        raise ErrorUtilities(f"Nivel {nivel} inexistente ({NIVELES})")
    p = {"nivel": nivel,
         "l_ave_etapas": {c: nv(v, nivel) for c, _, v, _, _ in AGUA_ETAPAS},
         "frac_efluente": nv(FRAC_EFLUENTE, nivel),
         "frac_rechazo_potabilizacion": FRAC_RECHAZO_POTABILIZACION,
         "factor_maximo_horario_agua": nv(FACTOR_MAXIMO_HORARIO_AGUA, nivel),
         "carga_g_ave": {k: nv(v, nivel) for k, v in CARGA_G_AVE.items()},
         "conc_mg_l": {k: nv(v, nivel) for k, v in CONC_MG_L.items()},
         "tolerancia_metodos": TOLERANCIA_METODOS,
         "fraccion_sangre_recuperada": None,       # None = la del balance (SUP-040, 85 %)
         "limites": [dict(x) for x in LIMITES_EJEMPLO],
         "lodos": None,                            # None = PENDIENTE DE DIMENSIONAMIENTO
         "lista_cargas": None,                     # None = potencia pico PENDIENTE
         "lista_cargas_criticas": None,            # None = generador PENDIENTE
         "perfil": dict(PERFILES["P1"]), "perfil_id": "P1",
         "dias_refrigerado": DIAS_REFRIGERADO_DEF, "dias_congelado": DIAS_CONGELADO_DEF,
         "base_inventario": "dias_produccion",
         "horas_netas": HORAS_NETAS, "horas_limpieza": HORAS_LIMPIEZA}
    l_total = ov.pop("l_ave_total", None)
    p.update(ov)
    if l_total is not None:                           # escala todas las etapas en proporción
        s = sum(p["l_ave_etapas"].values())
        p["l_ave_etapas"] = {c: v * l_total / s for c, v in p["l_ave_etapas"].items()}
    validar(p)
    return p


def lodos_ilustrativo(nivel):
    return {k: nv(v, nivel) for k, v in LODOS_ILUSTRATIVO.items()}


def validar(p):
    if any(v < 0 or not math.isfinite(v) for v in p["l_ave_etapas"].values()):
        raise ErrorUtilities("L/ave negativo o no finito")
    if sum(p["l_ave_etapas"].values()) > 200:
        raise ErrorUtilities("L/ave > 200: fuera de todo rango de faena avícola (revisar unidades: ¿m³?)")
    if not 0 < p["frac_efluente"] <= 1:
        raise ErrorUtilities("La fracción de agua a efluente debe estar en (0, 1]: no se descarga más de lo usado")
    if not 0 <= p["frac_rechazo_potabilizacion"] < 1:
        raise ErrorUtilities("Fracción de rechazo de potabilización fuera de [0, 1)")
    if any(v < 0 for v in p["carga_g_ave"].values()) or any(v <= 0 for v in p["conc_mg_l"].values()):
        raise ErrorUtilities("Carga específica negativa o concentración no positiva")
    if p["tolerancia_metodos"] < 1:
        raise ErrorUtilities("La tolerancia entre métodos debe ser ≥ 1")
    fs = p["fraccion_sangre_recuperada"]
    if fs is not None and not 0 <= fs <= 1:
        raise ErrorUtilities("Fracción de sangre recuperada fuera de [0, 1]")
    for lim in p["limites"]:
        validar_limite(lim)
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
    f_ref = k["sangre_recuperada"] / k["sangre_drenada"]
    f_sangre = f_ref if p["fraccion_sangre_recuperada"] is None else p["fraccion_sangre_recuperada"]
    n = nivel
    pn = f"nivel={n}"
    A = aves ** 1.01 if "M02" in _MUT else aves          # M02: escalado no lineal
    r = R()
    f_cal = dias_anio / DIAS_CALENDARIO
    h_op = p["horas_netas"] + p["horas_limpieza"]
    h_planta = h_op + HORAS_ARRANQUE_CIERRE
    t_vivas = k["peso_vivo"] * A / 1000
    com = k["comestible"] * A / 1000                     # t comerciales por día OPERATIVO
    r.add("entrada", "aves_faenadas_dia_operativo", A, "aves", "dia_operativo", "aves", "SUPUESTO", "[SUPUESTO]",
          "SUP-052", "escala = capacidad operativa")
    r.add("entrada", "t_vivas_dia_operativo", t_vivas, "t", "dia_operativo", "vivo", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "escenarios_escala.csv")
    r.add("entrada", "t_producto_comestible_dia_operativo", com, "t", "dia_operativo", "comercial", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "escenarios_escala.csv", "peso comercial (masa biológica + agua retenida)")

    # --- 1. AGUA: cinco conceptos -------------------------------------------------------
    sens = "RANGO DE SENSIBILIDAD PRELIMINAR; no es el consumo esperado de la planta"
    conv = 1.0 if "M08" in _MUT else 1000.0             # M08: L confundidos con m³
    l_ave = sum(p["l_ave_etapas"].values())
    if "M01" in _MUT:                                   # M01: agua retenida sumada al consumo
        l_ave += k["agua_retenida_producto"]
    for c, etq, _, org, ref in AGUA_ETAPAS:
        v = p["l_ave_etapas"][c]
        r.add("agua", f"agua_{c}_l_ave", v, "L/ave", "por_ave", "agua_utilizada", org,
              f"[{org}]" + (" [PVDP]" if org == "FUENTE" else ""), ref, f"{etq}; {sens}", parametro=pn)
        r.add("agua", f"agua_{c}_m3_dia", v * A / conv, "m³", "dia_operativo", "agua_utilizada", "ESTIMACIÓN",
              "[ESTIMACIÓN]", "", etq, parametro=pn)
    m3_uso = l_ave * A / conv
    m3_capt = m3_uso / (1 - p["frac_rechazo_potabilizacion"])
    r.add("agua", "agua_utilizada_l_ave", l_ave, "L/ave", "por_ave", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN] con rangos [PVDP]", "FTE-09C-01 a 04", sens, parametro=pn)
    r.add("agua", "agua_utilizada_m3_dia", m3_uso, "m³", "dia_operativo", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", sens, parametro=pn)
    r.add("agua", "agua_utilizada_m3_anio", m3_uso * dias_anio, "m³", "anio", "agua_utilizada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=pn)
    r.add("agua", "agua_captada_m3_dia", m3_capt, "m³", "dia_operativo", "agua_captada", "SUPUESTO",
          "[ESTIMACIÓN] con rechazo [SUPUESTO]", "", f"rechazo de potabilización = "
          f"{p['frac_rechazo_potabilizacion']:.2f} (dato de sitio)", parametro=pn)
    r.add("agua", "agua_utilizada_m3_por_t_producto", m3_uso / com, "m³/t", "adimensional", "agua_utilizada",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "segunda unidad: m³ por t de producto comestible (peso comercial)",
          parametro=pn)
    r.add("agua", "agua_utilizada_m3_por_t_vivo", m3_uso / t_vivas, "m³/t", "adimensional", "agua_utilizada",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "por t de peso vivo faenado", parametro=pn)
    m3t = m3_uso / com
    if not RANGO_M3_T_FUENTES[0] <= m3t <= RANGO_M3_T_FUENTES[1]:
        r.alerta("AGUA_M3_T", f"m³/t de producto ({m3t:.1f}) fuera del rango de contraste {RANGO_M3_T_FUENTES} "
                              f"m³/t (base carcasa, [PVDP]): revisar L/ave")
    if not RANGO_L_AVE_FUENTES[0] <= l_ave <= RANGO_L_AVE_FUENTES[1]:
        r.alerta("AGUA_L_AVE", f"L/ave ({l_ave:.1f}) fuera del rango citado {RANGO_L_AVE_FUENTES} ([PVDP])")
    r.add("agua", f"caudal_horario_medio_m3_h_bajo_{h_op:g}h", m3_uso / h_op, "m³/h", "hora", "agua_utilizada",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", f"sobre {h_op:g} h (faena + limpieza)", parametro=pn)
    r.add("agua", "caudal_horario_maximo_ilustrativo_m3_h", m3_uso / h_op * p["factor_maximo_horario_agua"],
          "m³/h", "hora", "agua_utilizada", "SUPUESTO", "[SUPUESTO] factor ilustrativo", "",
          "orden de magnitud; el caudal de diseño surgirá del perfil horario", parametro=pn)
    fe = p["frac_efluente"]
    m3_desc = m3_uso * (1.1 if "M03" in _MUT else fe)     # M03: se descarga más de lo usado
    t_incorp = k["agua_incorporada"] * A / 1000
    m3_evap = m3_uso - m3_desc - t_incorp
    if "M09" in _MUT:
        m3_evap = max(0.0, m3_evap) + 1.0                 # M09: cierre forzado
    r.add("agua", "fraccion_agua_a_efluente_supuesta", fe, "fracción", "adimensional", "agua_descargada",
          "SUPUESTO", "[SUPUESTO] editable", "", FRAC_EFLUENTE[2], parametro=pn)
    r.add("agua", "agua_descargada_m3_dia", m3_desc, "m³", "dia_operativo", "agua_descargada", "SUPUESTO",
          "[ESTIMACIÓN] con fracción [SUPUESTO]", "", f"= utilizada × {fe:.2f}", parametro=pn)
    l_desc_ave = m3_desc / A * (1000 if conv == 1000 else 1)
    r.add("agua", "agua_descargada_l_ave", l_desc_ave, "L/ave", "por_ave", "agua_descargada", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=pn)
    r.add("agua", "agua_evaporada_o_arrastrada_m3_dia", m3_evap, "m³", "dia_operativo", "agua_evaporada",
          "ESTIMACIÓN", "[ESTIMACIÓN] por diferencia", "", "utilizada − descargada − incorporada", parametro=pn)
    if m3_evap < 0:
        r.alerta("AGUA_CIERRE", "Agua evaporada/arrastrada negativa: la fracción a efluente supuesta es "
                                "incompatible con el agua incorporada al producto")
    r.add("agua_incorporada", "agua_retenida_en_producto_t_dia", k["agua_retenida_producto"] * A / 1000, "t",
          "dia_operativo", "agua_incorporada", "ESTIMACIÓN", "[ESTIMACIÓN] del balance v1.1", "escenarios_escala.csv",
          "sale vendida con el producto; NO es consumo industrial ni efluente")
    r.add("agua_incorporada", "agua_incorporada_producto_y_subproductos_t_dia", t_incorp, "t", "dia_operativo",
          "agua_incorporada", "ESTIMACIÓN", "[ESTIMACIÓN] del balance v1.1", "escenarios_escala.csv",
          "retenida + goteo del producto + adherida a plumas")
    r.add("agua_incorporada", "agua_retenida_sobre_agua_utilizada_pct",
          100 * k["agua_retenida_producto"] * A / 1000 / m3_uso, "%", "adimensional", "agua", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", "cuánto del agua usada termina dentro del producto", parametro=pn)

    # --- 2. EFLUENTES: MÉTODO A y MÉTODO B (independientes) -------------------------------
    extra_dqo = 0.0 if "M07" in _MUT else (f_ref - f_sangre) * k["sangre_drenada"] * DQO_SANGRE_KG_KG * 1000
    r.add("efluente", "fraccion_sangre_recuperada", f_sangre, "fracción", "adimensional", "sangre", "SUPUESTO",
          "[SUPUESTO] editable", "SUP-040", f"referencia del balance {f_ref:.2f}; validar con masa recuperada")
    for par, (vals, ref) in CARGA_G_AVE.items():
        g = p["carga_g_ave"][par] + (extra_dqo if par == "DQO" else 0.0)
        r.add("efluente", f"metodoA_carga_{par}_g_ave", g, "g/ave", "por_ave", "efluente_crudo", "FUENTE",
              "[PVDP] escenario", ref, "carga específica; no calibrada con el método B", parametro=pn)
        r.add("efluente", f"metodoA_carga_{par}_kg_dia", g * A / 1000, "kg", "dia_operativo", "efluente_crudo",
              "ESTIMACIÓN", "[ESTIMACIÓN] método A", "", "aves/día × g/ave / 1.000", parametro=pn)
        r.add("efluente", f"metodoA_concentracion_implicita_{par}_mg_l", g / l_desc_ave * 1000, "mg/L",
              "adimensional", "efluente_crudo", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "carga A / caudal (no es dato)",
              parametro=pn)
    for par, (vals, ref) in CONC_MG_L.items():
        c = p["conc_mg_l"][par]
        if "M20" in _MUT:                                 # M20: B calibrado para cerrar con A
            c = r[f"metodoA_concentracion_implicita_{par}_mg_l"]
        kg_b = m3_desc * c / 1000
        r.add("efluente", f"metodoB_concentracion_{par}_mg_l", c, "mg/L", "adimensional", "efluente_crudo",
              "FUENTE", "[PVDP] valor citado", ref, "concentración; no calibrada con el método A", parametro=pn)
        r.add("efluente", f"metodoB_carga_{par}_kg_dia", kg_b, "kg", "dia_operativo", "efluente_crudo",
              "ESTIMACIÓN", "[ESTIMACIÓN] método B", "", "m³ efluente/día × mg/L / 1.000", parametro=pn)
        kg_a = r[f"metodoA_carga_{par}_kg_dia"]
        ratio = kg_b / kg_a if kg_a else math.inf
        r.add("efluente", f"relacion_B_sobre_A_{par}", ratio, "ratio", "adimensional", "efluente_crudo",
              "ESTIMACIÓN", "[ESTIMACIÓN]", "", f"compatible si está entre 1/{p['tolerancia_metodos']:g} y "
              f"{p['tolerancia_metodos']:g}", parametro=pn)
        compatible = 1 / p["tolerancia_metodos"] <= ratio <= p["tolerancia_metodos"]
        r.add("efluente", f"metodos_compatibles_{par}", 1.0 if compatible else 0.0, "índice", "adimensional",
              "efluente_crudo", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "1 = mismo orden de magnitud; 0 = alerta",
              parametro=pn)
        if not compatible:
            r.alerta(f"EFLUENTE_{par}", f"{ALERTA_EFLUENTE}: {par} método B/A = {ratio:.2f}")
    r.add("efluente", "dqo_potencial_sangre_recuperada_referencia_kg_dia",
          k["sangre_recuperada"] * DQO_SANGRE_KG_KG * A, "kg", "dia_operativo", "efluente_crudo", "FUENTE",
          "[PVDP] referencia de sensibilidad", "FTE-181",
          "DQO que aportaría la sangre recuperada si llegara al drenaje; validar midiendo DQO antes/después "
          "o masa recuperada y carga específica")
    r.add("efluente", "sensibilidad_dqo_si_no_se_recuperara_sangre_pct",
          100 * k["sangre_recuperada"] * DQO_SANGRE_KG_KG * 1000 / p["carga_g_ave"]["DQO"], "%", "adimensional",
          "efluente_crudo", "FUENTE", "[PVDP] sensibilidad", "FTE-181",
          "respecto del método A; NO es un resultado de la planta", parametro=pn)
    r.add("efluente", "caudal_efluente_horario_maximo_ilustrativo_m3_h", m3_desc / h_op * p["factor_maximo_horario_agua"],
          "m³/h", "hora", "agua_descargada", "SUPUESTO", "[SUPUESTO] factor ilustrativo", "", parametro=pn)
    for lim in p["limites"]:
        par = lim["parametro"]
        txt = (f"EJEMPLO REGULATORIO DE REFERENCIA ({lim['jurisdiccion']}, {lim['norma']}, {lim['tipo_descarga']}, "
               f"{par} {lim['mg_l']:g} mg/L): bajo el ejemplo de límite utilizado, el escenario exigiría "
               f"aproximadamente este % de remoción. NO es requisito del proyecto: la localización lo reemplazará "
               f"por el límite real (provincia, autoridad, cuerpo receptor, red, permiso, normativa vigente)")
        for met, conc in (("metodoA", r[f"metodoA_concentracion_implicita_{par}_mg_l"]),
                          ("metodoB", r[f"metodoB_concentracion_{par}_mg_l"])):
            r.add("efluente", f"remocion_{par}_bajo_ejemplo_limite_{met}_pct",
                  100 * remocion_bajo_ejemplo(conc, lim), "%", "adimensional", "efluente_crudo", "ESTIMACIÓN",
                  "[ESTIMACIÓN] con límite de ejemplo [PVDP]", lim.get("ref", ""), txt,
                  parametro=f"{pn}; jurisdiccion={lim.get('jurisdiccion', '')}; "
                            f"tipo_descarga={lim.get('tipo_descarga', '')}")

    # --- 3. MASA SEGREGABLE EN ORIGEN (del balance) ≠ SÓLIDOS DEL EFLUENTE ≠ SST ------------
    for clave, nota in (("sangre_recuperada", "sangre recuperable por separado (85 %, SUP-040)"),
                        ("plumas", "plumas húmedas"), ("visceras", "vísceras no comestibles"),
                        ("cabeza", "cabezas"),
                        ("solidos_a_retirar", "total (C + decomisos + contenido GI); no sumar con las anteriores"),
                        ("masa_a_efluente_o_perdida", "masa que el balance asigna a efluente o pérdida; NO equivale "
                                                      "a SST")):
        var = ("masa_biologica_potencialmente_segregable_en_origen_t_dia" if clave == "solidos_a_retirar"
               else f"segregable_{clave}_t_dia")
        r.add("masa_segregable", var, k[clave] * A / 1000, "t", "dia_operativo", "biologica+agua", "ESTIMACIÓN",
              "[ESTIMACIÓN] del balance v1.1", "escenarios_escala.csv", nota)
    r.add("masa_segregable", "solidos_que_entran_efectivamente_al_efluente_t_dia", PENDIENTE, "t", "dia_operativo",
          "biologica+agua", "PENDIENTE", "", "", "depende de diseño, pérdidas, lavado, tamizado, manejo de "
          "subproductos y disciplina operativa; medir")
    if "M12" in _MUT:                                     # M12: SST = subproductos del balance
        r.v["metodoA_carga_SST_kg_dia"] = k["solidos_a_retirar"] * A

    # --- 4. LODOS ---------------------------------------------------------------------------
    lo = lodos(r["metodoA_carga_SST_kg_dia"], r["metodoA_carga_GyA_kg_dia"], r["metodoA_carga_DBO5_kg_dia"],
               m3_desc, p["lodos"])
    ilus = p["lodos"] is not None
    for var, v in lo.items():
        r.add("lodos", var, v, "t" if var.endswith("_t_dia") else "kg", "dia_operativo", "materia_seca"
              if "humedo" not in var else "lodo_humedo", "SUPUESTO", "[ESTIMACIÓN ILUSTRATIVA] con [SUPUESTO] visibles"
              if ilus else "", "", "escenario ilustrativo: cada supuesto en el bloque lodos_ilustrativo" if ilus
              else "LODO = PENDIENTE DE DIMENSIONAMIENTO", parametro=pn)

    # --- 5. ELECTRICIDAD: energía -> potencia MEDIA equivalente; pico PENDIENTE --------------
    kwh_proc = nv(KWH_T_PV, n) * t_vivas
    r.add("electricidad", "kwh_proceso_dia", kwh_proc, "kWh", "dia_operativo", "energia_electrica", "FUENTE",
          "[ESTIMACIÓN] con indicador [PVDP]", KWH_T_PV[2], "top-down; faena, proceso, enfriado fresco, aire, agua, "
          "servicios", parametro=pn)
    r.add("electricidad", "kwh_proceso_por_ave", kwh_proc / A, "kWh/ave", "por_ave", "energia_electrica", "FUENTE",
          "[PVDP] sensibilidad", KWH_T_PV[2], "kWh/día = aves/día × kWh/ave", parametro=pn)
    for c, f in REPARTO_ELECTRICO.items():
        r.add("electricidad", f"kwh_proceso_{c}_dia", kwh_proc * f, "kWh", "dia_operativo", "energia_electrica",
              "SUPUESTO", "[SUPUESTO] reparto ilustrativo", "FTE-09C-09 (cualitativo)", "didáctico; no sumar",
              parametro=pn)

    # --- 6. INVENTARIO (reproduce el modelo de escala) ---------------------------------------
    flujo_inv = com * (1 if ("M05" in _MUT or p["base_inventario"] == "dias_produccion") else f_cal)
    sh = p["perfil"]
    d_ref, d_cong = p["dias_refrigerado"], p["dias_congelado"]
    t_refr = flujo_inv * sh["refrigerado"] * d_ref
    t_cong = flujo_inv * (sh["congelado"] + sh["exportacion"]) * (1 if "M06" in _MUT else d_cong)
    r.add("inventario", "stock_refrigerado_t", t_refr, "t", "stock", "comercial", "ESTIMACIÓN", "[ESTIMACIÓN]",
          "SUP-055, SUP-056", f"base={p['base_inventario']}; días={d_ref}; perfil={p['perfil_id']}")

    # --- 7. CONGELACIÓN (t nuevas/día) ≠ ALMACENAMIENTO (t guardadas) ------------------------
    t_cong_dia = com * (sh["congelado"] + sh["exportacion"])
    r.add("congelado", "capacidad_congelacion_t_dia", t_cong_dia, "t/día", "dia_operativo", "comercial",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "SUP-055", "t NUEVAS que deben atravesar la congelación por día de faena "
          "(túneles/IQF)")
    var_alm = "capacidad_congelacion_t_dia_x" if "M17" in _MUT else "capacidad_almacenamiento_congelado_t"
    r.add("congelado", var_alm, t_cong, "t/día" if "M17" in _MUT else "t", "stock", "comercial", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", f"t YA congeladas que permanecen guardadas (cámaras); base={p['base_inventario']}; "
          f"días={d_cong}. Guardar 300 t NO es poder congelar 300 t/día")
    for var, kg, fr in (("garras", k["garras"], FRAC_GARRAS_CONGELADAS),
                        ("menudencias", k["menudencias"], FRAC_MENUDENCIAS_CONGELADAS)):
        r.add("congelado", f"{var}_a_congelar_t_dia_informativo", kg * A / 1000 * nv(fr, n), "t/día",
              "dia_operativo", "comercial", "SUPUESTO", "[SUPUESTO]", "", "ya incluidas en el comestible: NO sumar",
              parametro=pn)
    kj_sens1 = CP_FRESCO * (T_SALIDA_CARCASA - T_CONGELACION_INICIAL)
    kj_lat = FRAC_AGUA_PRODUCTO * CALOR_LATENTE_AGUA
    kj_sens2 = CP_CONGELADO * (T_CONGELACION_INICIAL - T_FINAL_CONGELADO)
    kj_kg_cong = kj_sens1 + kj_lat + kj_sens2
    for var, v in (("calor_congelacion_sensible_sobre_cero_kj_kg", kj_sens1),
                   ("calor_congelacion_latente_kj_kg", kj_lat),
                   ("calor_congelacion_sensible_bajo_cero_kj_kg", kj_sens2),
                   ("calor_congelacion_producto_total_kj_kg", kj_kg_cong)):
        r.add("congelado", var, v, "kJ/kg", "adimensional", "producto", "ESTIMACIÓN",
              "[ESTIMACIÓN] con propiedades [PVDP]/[SUPUESTO]", "FTE-09C-14", "solo producto; sin envases, "
              "ventiladores, desescarche ni pérdidas del túnel")
    kwf_cong = t_cong_dia * 1000 * kj_kg_cong / (HORAS_TUNEL * 3600)

    # --- 8. FRÍO: carga sensible del producto ≠ carga frigorífica total -----------------------
    kj_prod = k["comestible"] * CP_FRESCO * (T_ENTRADA_CARCASA - T_SALIDA_CARCASA)
    kj_agua_ch = p["l_ave_etapas"]["chiller"] * CP_AGUA * (T_RED - T_AGUA_CHILLER)
    hn = p["horas_netas"]
    kwf_prod = kj_prod * A / (hn * 3600)
    kwf_agua = kj_agua_ch * A / (hn * 3600)
    kwf_adic = (kwf_prod + kwf_agua) * nv(FRAC_CARGAS_ADICIONALES, n)
    var_sens = "capacidad_frigorifica_total_kwf" if "M15" in _MUT else "carga_sensible_preliminar_producto_kwf_bajo_8h"
    r.add("frio", var_sens, kwf_prod, "kW frigoríficos", "potencia", "frio", "ESTIMACIÓN",
          "[ESTIMACIÓN] con [SUPUESTO]", "FTE-09C-14", "carga sensible preliminar asociada al enfriamiento del "
          f"producto (38 → 4 °C) durante {hn:g} h; NO es la capacidad frigorífica de planta", parametro=pn)
    r.add("frio", "carga_sensible_preliminar_producto_tr", kwf_prod / KW_POR_TR, "TR", "potencia", "frio",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "1 TR = 3,517 kW frigoríficos", parametro=pn)
    r.add("frio", "carga_enfriamiento_agua_reposicion_chiller_kwf_bajo_8h", kwf_agua, "kW frigoríficos", "potencia",
          "frio", "ESTIMACIÓN", "[ESTIMACIÓN] con [SUPUESTO]", "", "agua de reposición de 18 a 1 °C; fila separada",
          parametro=pn)
    r.add("frio", "cargas_adicionales_ilustrativas_kwf", kwf_adic, "kW frigoríficos", "potencia", "frio",
          "SUPUESTO", "[SUPUESTO] ilustrativo", "", FRAC_CARGAS_ADICIONALES[2], parametro=pn)
    r.add("frio", "carga_media_congelacion_producto_kwf_bajo_20h", kwf_cong, "kW frigoríficos", "potencia", "frio",
          "ESTIMACIÓN", "[ESTIMACIÓN] con [SUPUESTO]", "", "solo calor del producto repartido en 20 h; la potencia "
          "instalada de túneles depende del tiempo de congelación (lotes)", parametro=pn)
    r.add("frio", "carga_frigorifica_total_kwf", PENDIENTE, "kW frigoríficos", "potencia", "frio", "PENDIENTE", "",
          "", "balance frigorífico: producto (sensible y latente), transmisión, infiltración, puertas, personas, "
          "iluminación, motores, docks, salas, cámaras, túneles, desescarche, otras")
    cop_e, cop_c = nv(COP_ENFRIADO, n), nv(COP_CONGELADO, n)
    for var, kwf, cop, ref in (("producto", kwf_prod, cop_e, COP_ENFRIADO[2]),
                               ("agua_chiller", kwf_agua, cop_e, COP_ENFRIADO[2]),
                               ("congelacion_producto", kwf_cong, cop_c, COP_CONGELADO[2])):
        if "M16" not in _MUT:
            r.add("frio", f"cop_supuesto_{var}", cop, "COP", "adimensional", "frio", "SUPUESTO", "[SUPUESTO]", ref,
                  "kW frigoríficos / kW eléctricos", parametro=pn)
        r.add("frio", f"kw_electricos_aprox_{var}", kwf / (1.0 if "M04" in _MUT else cop), "kW eléctricos",
              "potencia", "energia_electrica", "SUPUESTO", "[ESTIMACIÓN] con COP [SUPUESTO]", "",
              f"= kW frigoríficos / COP supuesto ({cop:g}); no es consumo garantizado", parametro=pn)
    kwh_frio_bu = (r["kw_electricos_aprox_producto"] + r["kw_electricos_aprox_agua_chiller"]) * hn
    kwh_frio_td = kwh_proc * REPARTO_ELECTRICO["frio_de_proceso_agua_helada_hielo"]
    r.add("frio", "brecha_frio_fisico_vs_reparto_indicador_ratio", kwh_frio_td / kwh_frio_bu, "ratio",
          "adimensional", "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "",
          f"reparto top-down ({kwh_frio_td:.0f} kWh) / cálculo físico producto + agua de chiller "
          f"({kwh_frio_bu:.0f} kWh); brecha NO cerrada", parametro=pn)

    kwh_cong = nv(KWH_T_CONGELADA, n) * t_cong_dia
    kwh_alm = t_refr * nv(KWH_T_DIA_REFRIGERADO, n) + t_cong * nv(KWH_T_DIA_CONGELADO, n)
    dbo_bio = r["metodoA_carga_DBO5_kg_dia"] * (1 - nv(REM_DBO_PRETRAT_ENERGIA, n))
    kwh_efl = dbo_bio * 0.95 * nv(KWH_KG_DBO, n)
    r.add("electricidad", "kwh_congelacion_dia", kwh_cong, "kWh", "dia_operativo", "energia_electrica", "FUENTE",
          "[ESTIMACIÓN] con indicador [PVDP]", KWH_T_CONGELADA[2], parametro=pn)
    r.add("electricidad", "kwh_almacenamiento_frio_dia_calendario", kwh_alm, "kWh", "dia_calendario",
          "energia_electrica", "SUPUESTO", "[ESTIMACIÓN] con [SUPUESTO]", "", "cámaras 365 días; ilustrativo",
          parametro=pn)
    r.add("electricidad", "kwh_tratamiento_aerobio_dia", kwh_efl, "kWh", "dia_operativo", "energia_electrica",
          "SUPUESTO", "[ESTIMACIÓN] con [SUPUESTO]", "", "cota si todo el biológico fuera aerobio", parametro=pn)
    kwh_dia = kwh_proc + kwh_cong + kwh_efl + kwh_alm
    kwh_anio = (kwh_proc + kwh_cong + kwh_efl) * dias_anio + kwh_alm * DIAS_CALENDARIO
    r.add("electricidad", "kwh_total_dia_operativo", kwh_dia, "kWh", "dia_operativo", "energia_electrica",
          "ESTIMACIÓN", "[ESTIMACIÓN]", "", "proceso + congelado + aerobio + cámaras", parametro=pn)
    r.add("electricidad", "kwh_total_anio", kwh_anio, "kWh", "anio", "energia_electrica", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", "cámaras × 365 días; resto × días de faena", parametro=pn)
    r.add("electricidad", "kwh_por_ave_promedio_anual", kwh_anio / (A * dias_anio), "kWh/ave", "por_ave",
          "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", parametro=pn)
    pm_proc = kwh_proc / h_planta
    if "M11" in _MUT:
        r.add("electricidad", "potencia_media_proceso_kw", pm_proc, "kW", "potencia", "energia_electrica",
              "ESTIMACIÓN", "[ESTIMACIÓN]", "", "", parametro=pn)
    else:
        r.add("electricidad", f"potencia_media_equivalente_proceso_kw_bajo_{h_planta:g}h", pm_proc, "kW",
              "potencia", "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "",
              f"= kWh de proceso / {h_planta:g} h; NO es potencia pico", parametro=pn)
    r.add("electricidad", "potencia_media_equivalente_total_kw_bajo_24h", kwh_dia / 24, "kW", "potencia",
          "energia_electrica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "= kWh totales del día / 24 h; NO es potencia pico",
          parametro=pn)
    pico_kw, pico_kva = demanda_maxima(p["lista_cargas"])
    if "M10" in _MUT:
        pico_kw = pm_proc * 1.5                           # M10: pico derivado de kWh/ave
    r.add("electricidad", "potencia_pico_demanda_maxima_kw", pico_kw, "kW", "potencia", "energia_electrica",
          "ESTIMACIÓN", "[ESTIMACIÓN] desde lista de cargas", "", "solo desde lista de cargas (kW nominal, factor de "
          "carga, simultaneidad, arranque, cos φ); también potencia contratada y transformador", parametro=pn)
    r.add("electricidad", "potencia_pico_demanda_maxima_kva", pico_kva, "kVA", "potencia", "energia_electrica",
          "ESTIMACIÓN", "[ESTIMACIÓN] desde lista de cargas", "", "", parametro=pn)

    # --- 9. AGUA CALIENTE / VAPOR: MJ/día y potencia térmica MEDIA; pico PENDIENTE -------------
    le = p["l_ave_etapas"]
    kj_esc = le["escaldado"] * CP_AGUA * (nv(T_ESCALDADO, n) - T_RED) * nv(FACTOR_PERDIDAS_ESCALDADO, n)
    kj_lim = le["limpieza"] * nv(FRAC_LIMPIEZA_CALIENTE, n) * CP_AGUA * (nv(T_LIMPIEZA, n) - T_RED)
    kj_san = le["sanitizacion"] * nv(FRAC_SANITIZACION_CALIENTE, n) * CP_AGUA * (T_ESTERILIZACION - T_RED)
    util_mj_ave = (kj_esc + kj_lim + kj_san) / 1000
    comb_mj_ave = util_mj_ave / nv(RENDIMIENTO_TERMICO, n)
    for var, kj, h in (("escaldado", kj_esc, p["horas_netas"]), ("limpieza", kj_lim, p["horas_limpieza"]),
                       ("sanitizacion", kj_san, h_op)):
        r.add("termico", f"calor_util_{var}_mj_dia", kj * A / 1000, "MJ", "dia_operativo", "energia_termica",
              "ESTIMACIÓN", "[ESTIMACIÓN] con temperaturas [PVDP]/[SUPUESTO]", "FTE-09C-11", parametro=pn)
        r.add("termico", f"potencia_termica_media_equivalente_{var}_kw_bajo_{h:g}h",
              kj * A / (h * 3600) if h else 0.0, "kW térmicos", "potencia", "energia_termica", "ESTIMACIÓN",
              "[ESTIMACIÓN]", "", f"= MJ/día / {h:g} h; no es pico", parametro=pn)
    r.add("termico", "calor_util_mj_ave", util_mj_ave, "MJ/ave", "por_ave", "energia_termica", "ESTIMACIÓN",
          "[ESTIMACIÓN] sensibilidad preliminar", "", parametro=pn)
    r.add("termico", "calor_util_mj_dia", util_mj_ave * A, "MJ", "dia_operativo", "energia_termica", "ESTIMACIÓN",
          "[ESTIMACIÓN]", "", parametro=pn)
    r.add("termico", "energia_combustible_mj_dia", comb_mj_ave * A, "MJ", "dia_operativo", "energia_termica",
          "ESTIMACIÓN", "[ESTIMACIÓN] con rendimiento [SUPUESTO]", "", parametro=pn)
    r.add("termico", "energia_combustible_kwh_termicos_dia", comb_mj_ave * A / 3.6, "kWh", "dia_operativo",
          "energia_termica", "ESTIMACIÓN", "[ESTIMACIÓN]", "", "kWh TÉRMICOS (no eléctricos)", parametro=pn)
    for comb, (pci, org, ref) in PCI_MJ.items():
        r.add("termico", f"equivalente_{comb}_dia", comb_mj_ave * A / pci, comb.split("_")[-1], "dia_operativo",
              "energia_termica", "SUPUESTO", "[ESTIMACIÓN] con PCI [SUPUESTO]", ref, "equivalencia, no elección; "
              "el consumo diario no define capacidad de caldera", parametro=pn)
    r.add("termico", "equivalente_electricidad_resistiva_kwh_dia", util_mj_ave * A / 3.6 / 0.98, "kWh",
          "dia_operativo", "energia_termica", "SUPUESTO", "[ESTIMACIÓN]", "", "rendimiento 98 %", parametro=pn)
    r.add("termico", "potencia_termica_pico_kw", PENDIENTE, "kW térmicos", "potencia", "energia_termica",
          "PENDIENTE", "", "", "requiere perfil horario y simultaneidad de escaldado, limpieza, sanitización y "
          "otros usos; define la caldera", parametro=pn)

    # --- 10. RESPALDO: carga crítica ILUSTRATIVA; generador PENDIENTE -------------------------
    kwe_alm = kwh_alm / 24
    crit = {"camaras_frio": kwe_alm * nv(FACTOR_REARRANQUE, n), "efluentes_minimo": kwh_efl / 24 * FRAC_EFLUENTE_MINIMO}
    crit.update({c: f * pm_proc for c, f in FRAC_CRITICA_ILUSTRATIVA.items()})
    for c, v in crit.items():
        r.add("respaldo", f"carga_critica_ilustrativa_{c}_kw", v, "kW", "potencia", "energia_electrica", "SUPUESTO",
              "[SUPUESTO] proxy", "", "carga crítica ilustrativa de escenario", parametro=pn)
    r.add("respaldo", "carga_critica_ilustrativa_escenario_kw", sum(crit.values()), "kW", "potencia",
          "energia_electrica", "SUPUESTO", "[SUPUESTO] proxy preliminar de sensibilidad", "",
          "NO es el generador necesario", parametro=pn)
    gen_kw, gen_kva = demanda_maxima(p["lista_cargas_criticas"])
    if "M18" in _MUT:
        gen_kva = 0.10 * pm_proc / 0.8                    # M18: generador como % fijo de la planta
    r.add("respaldo", "grupo_electrogeno_kva", gen_kva, "kVA", "potencia", "energia_electrica", "ESTIMACIÓN",
          "[ESTIMACIÓN] desde lista de cargas críticas", "", "requiere lista de cargas críticas, kW/kVA, cos φ, "
          "arranque de motores/compresores, secuencia, simultaneidad, autonomía, combustible, redundancia, "
          "black-start", parametro=pn)
    return r


def inventario_escala(E, dias_anio):
    """Filas equivalentes al bloque `inventario` del modelo de escala, recalculadas (test U07)."""
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
# 5. TESTS
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


CARGAS_DEMO = [  # lista sintética SOLO para probar la función (no es un listado del proyecto)
    {"equipo": "compresor", "kw_nominal": 100.0, "factor_carga": 0.8, "simultaneidad": 1.0, "cos_phi": 0.85,
     "factor_arranque": 3.0},
    {"equipo": "bomba", "kw_nominal": 20.0, "factor_carga": 0.7, "simultaneidad": 0.5, "cos_phi": 0.8}]


def tests():
    res = []

    def t(nombre, cond, msg=""):
        res.append((nombre, bool(cond), msg))

    k = kg_por_ave()
    ok = all(_cerca(kg_por_ave(E, ds)[x], k[x], 1e-6) for E in ESCALAS for ds in CALENDARIOS for x in MASAS)
    t("U00 masas del CSV de escala lineales y coherentes", ok)
    # U01 escalabilidad
    ok, n_var = True, 0
    for niv in NIVELES:
        a, b = calcular(5000, 250, niv), calcular(10000, 250, niv)
        for f in a.filas:
            v1, v2 = f["valor"], b[f["variable"]]
            if v1 is None or v2 is None:
                ok &= v1 is None and v2 is None
            elif f["periodo"] in ("por_ave", "adimensional") or f["unidad"] in ("kJ/kg", "COP"):
                ok &= _cerca(v1, v2, 1e-9)
            else:
                ok &= _cerca(2 * v1, v2, 1e-9)
            n_var += 1
    t("U01 escalabilidad lineal (duplicar aves duplica flujos; intensivos constantes)", ok, f"{n_var} variables")
    r = calcular(10000, 250, "medio")
    ok = _cerca(r["agua_utilizada_m3_dia"], r["agua_utilizada_l_ave"] * 10000 / 1000)
    ok &= _cerca(r["agua_utilizada_m3_anio"], r["agua_utilizada_m3_dia"] * 250)
    ok &= _cerca(r["carga_sensible_preliminar_producto_tr"] * KW_POR_TR, r["carga_sensible_preliminar_producto_kwf_bajo_8h"])
    ok &= _cerca(r["energia_combustible_kwh_termicos_dia"] * 3.6, r["energia_combustible_mj_dia"])
    ok &= _cerca(r["metodoA_carga_DQO_kg_dia"], r["metodoA_carga_DQO_g_ave"] * 10000 / 1000)
    ok &= _cerca(r["metodoB_carga_DQO_kg_dia"], r["agua_descargada_m3_dia"] * r["metodoB_concentracion_DQO_mg_l"] / 1000)
    ok &= 5 <= r["agua_utilizada_l_ave"] <= 60
    t("U02 unidades (L↔m³, día↔año, kW↔TR, MJ↔kWh, g/ave↔kg/día, m³×mg/L↔kg/día)", ok)
    m2 = dict(k, agua_retenida_producto=k["agua_retenida_producto"] * 3, agua_incorporada=k["agua_incorporada"] * 3)
    r2 = calcular(10000, 250, "medio", masas=m2)
    ok = _cerca(r2["agua_utilizada_m3_dia"], r["agua_utilizada_m3_dia"]) and \
        _cerca(r2["agua_descargada_m3_dia"], r["agua_descargada_m3_dia"])
    ok &= _cerca(r["agua_utilizada_l_ave"], sum(nv(v, "medio") for _, _, v, _, _ in AGUA_ETAPAS))
    t("U03 agua incorporada separada: triplicarla no cambia agua utilizada ni descargada", ok)
    ok = True
    for niv in NIVELES:
        x = calcular(10000, 250, niv)
        ok &= _cerca(x["agua_utilizada_m3_dia"], x["agua_descargada_m3_dia"] + x["agua_incorporada_producto_y_subproductos_t_dia"]
                     + x["agua_evaporada_o_arrastrada_m3_dia"])
        ok &= x["agua_evaporada_o_arrastrada_m3_dia"] >= 0 and x["agua_captada_m3_dia"] >= x["agua_utilizada_m3_dia"]
        ok &= 0 < x["agua_descargada_m3_dia"] <= x["agua_utilizada_m3_dia"]
    xc = calcular(10000, 250, p=parametros("medio", frac_rechazo_potabilizacion=0.25))
    ok &= _cerca(xc["agua_captada_m3_dia"], r["agua_utilizada_m3_dia"] / 0.75)
    xe = calcular(10000, 250, p=parametros("medio", frac_efluente=0.999))
    ok &= any(a[0] == "AGUA_CIERRE" for a in xe.alertas)
    t("U04 cierre: captada ≥ utilizada = descargada + incorporada + evaporada (≥ 0); fracción editable", ok)
    rs = [calcular(10000, 250, niv) for niv in NIVELES]
    claves = ("agua_utilizada_m3_dia", "agua_descargada_m3_dia", "metodoA_carga_DQO_kg_dia", "metodoB_carga_DQO_kg_dia",
              "kwh_total_dia_operativo", "energia_combustible_mj_dia", "kw_electricos_aprox_producto")
    t("U05 bajo < medio < alto", all(rs[0][c] < rs[1][c] < rs[2][c] for c in claves))
    ok = all(_cerca(sum(x[f"agua_{c}_m3_dia"] for c, *_ in AGUA_ETAPAS), x["agua_utilizada_m3_dia"]) for x in rs)
    t("U06 Σ etapas = agua utilizada", ok)
    n_ok = n_tot = 0
    for f in leer_escala():
        if f["bloque"] != "inventario" or f["variable"] == "subproductos_perecederos_frio_t":
            continue
        E, da = int(f["escala_aves_dia"]), int(f["dias_anio"])
        par = dict(x.split("=") for x in f["parametro"].split("; "))
        cat = f["variable"][:-2] if f["variable"] != "comestible_total_t" else "comestible_total"
        v = inventario_escala(E, da)[(par["base_temporal"], int(par["dias"]), par.get("perfil_destino", ""), cat)]
        n_tot += 1
        n_ok += _cerca(v, float(f["valor"]), 1e-6)
    t("U07 inventario = escenarios_escala.csv", n_ok == n_tot and n_tot > 0, f"{n_ok}/{n_tot} filas")
    pc = parametros("medio", base_inventario="dias_calendario", perfil=dict(PERFILES["P2"]), perfil_id="P2")
    pp = parametros("medio", perfil=dict(PERFILES["P2"]), perfil_id="P2")
    rc, rp = calcular(10000, 250, p=pc), calcular(10000, 250, p=pp)
    ok = _cerca(rc["capacidad_almacenamiento_congelado_t"], rp["capacidad_almacenamiento_congelado_t"] * 250 / 365)
    ok &= _cerca(rp["capacidad_almacenamiento_congelado_t"], valor_escala(
        10000, 5, "inventario", "congelado_t", "stock", "base_temporal=dias_produccion; dias=14; perfil_destino=P2"), 1e-6)
    t("U08 días calendario = días de producción × días op./365 < días de producción", ok)
    # U09 congelación ≠ almacenamiento (variables, unidades e independencia)
    p1 = parametros("medio", perfil=dict(PERFILES["P3"]), perfil_id="P3", dias_congelado=1)
    p28 = parametros("medio", perfil=dict(PERFILES["P3"]), perfil_id="P3", dias_congelado=28)
    a, b = calcular(10000, 250, p=p1), calcular(10000, 250, p=p28)
    ok = "capacidad_almacenamiento_congelado_t" in b.v and "capacidad_congelacion_t_dia" in b.v
    ok = ok and _cerca(a["capacidad_congelacion_t_dia"], b["capacidad_congelacion_t_dia"])
    ok = ok and _cerca(b["capacidad_almacenamiento_congelado_t"], 28 * a["capacidad_almacenamiento_congelado_t"])
    uni = {f["variable"]: f["unidad"] for f in b.filas}
    ok = ok and uni.get("capacidad_congelacion_t_dia") == "t/día" and uni.get("capacidad_almacenamiento_congelado_t") == "t"
    t("U09 congelación (t/día nuevas) y almacenamiento (t guardadas) son variables distintas e independientes", ok)
    # U10 COP declarado para toda conversión frigorífico -> eléctrico
    ok = True
    for x in rs:
        for f in x.filas:
            if f["variable"].startswith("kw_electricos_aprox_"):
                suf = f["variable"][len("kw_electricos_aprox_"):]
                cop = x.v.get(f"cop_supuesto_{suf}")
                ok &= cop is not None and cop > 1 and "COP" in f["nota"]
                kwf = {"producto": "carga_sensible_preliminar_producto_kwf_bajo_8h",
                       "agua_chiller": "carga_enfriamiento_agua_reposicion_chiller_kwf_bajo_8h",
                       "congelacion_producto": "carga_media_congelacion_producto_kwf_bajo_20h"}[suf]
                ok &= _cerca(f["valor"], x[kwf] / cop)
    t("U10 kW eléctricos aprox = kW frigoríficos / COP supuesto declarado (fila cop_supuesto_*)", ok)
    # U11 energía diaria = aves × kWh/ave
    ok = _cerca(r["kwh_proceso_dia"], 10000 * r["kwh_proceso_por_ave"])
    t("U11 kWh/día = aves/día × kWh/ave", ok)
    filas = construir()
    ok = all(f["valor"] == "" or (isinstance(f["valor"], (int, float)) and math.isfinite(f["valor"]) and f["valor"] >= 0)
             for f in filas)
    t("U12 ningún valor negativo ni no finito (PENDIENTE = vacío)", ok, f"{len(filas)} filas")
    ok = not any(PALABRAS_ECONOMICAS.search(f"{f['variable']} {f['unidad']}") for f in filas)
    t("U13 ninguna variable económica", ok)
    malos = 0
    for kw in ({"frac_efluente": 1.2}, {"frac_efluente": 0}, {"l_ave_total": -5}, {"l_ave_total": 25000},
               {"fraccion_sangre_recuperada": 1.5}, {"perfil": {"refrigerado": 0.7, "congelado": 0.4, "exportacion": 0}},
               {"base_inventario": "semanas"}, {"dias_congelado": -1}, {"frac_rechazo_potabilizacion": 1.0},
               {"tolerancia_metodos": 0.5}):
        try:
            parametros("medio", **kw)
        except ErrorUtilities:
            malos += 1
    for args in ((-100, 250), (10000, 400), (0, 250)):
        try:
            calcular(*args)
        except ErrorUtilities:
            malos += 1
    t("U14 entradas inválidas rechazadas", malos == 13, f"{malos}/13")
    r0 = calcular(10000, 250, p=parametros("medio", fraccion_sangre_recuperada=0.0))
    ok = r0["metodoA_carga_DQO_kg_dia"] > r["metodoA_carga_DQO_kg_dia"]
    ok &= _cerca(r0["metodoA_carga_DQO_kg_dia"] - r["metodoA_carga_DQO_kg_dia"],
                 r["dqo_potencial_sangre_recuperada_referencia_kg_dia"], 1e-9)
    ok &= _cerca(r["fraccion_sangre_recuperada"], 0.85, 1e-6)
    cls = {f["variable"]: f["clasificacion"] for f in r.filas}
    ok &= "PVDP" in cls["sensibilidad_dqo_si_no_se_recuperara_sangre_pct"]
    t("U15 fracción de sangre recuperada editable; efecto como referencia [PVDP]", ok)
    ok = all(_cerca(calcular(E, 250)[v], valor_escala(E, 5, "subproductos", c), 1e-6)
             for E in ESCALAS for v, c in (("segregable_sangre_recuperada_t_dia", "sangre_t"),
                                           ("masa_biologica_potencialmente_segregable_en_origen_t_dia",
                                            "solidos_a_retirar_t")))
    t("U16 masa segregable en origen = balance/escala", ok)
    ok = all(_cerca(sum(s.values()), 1.0) for s in PERFILES.values())
    ok &= all(RANGO_DQO_FUENTES_MG_L[0] <= x["metodoB_concentracion_DQO_mg_l"] <= RANGO_DQO_FUENTES_MG_L[1] for x in rs)
    t("U17 perfiles = 100 %; concentraciones del método B dentro del rango de fuentes", ok)
    r3 = calcular(10000, 300, "medio")
    ok = _cerca(r3["kwh_total_anio"] - r["kwh_total_anio"],
                (r["kwh_total_dia_operativo"] - r["kwh_almacenamiento_frio_dia_calendario"]) * 50)
    t("U18 sexto día: +50 días de proceso; cámaras sin cambio (365 días)", ok)
    x = calcular(10000, 250, p=parametros("medio", l_ave_total=50))
    ok = _cerca(x["agua_utilizada_l_ave"], 50) and _cerca(x["agua_evisceracion_l_ave"] / 50,
                                                           r["agua_evisceracion_l_ave"] / r["agua_utilizada_l_ave"])
    t("U19 cambiar L/ave total mantiene el reparto por etapa", ok)
    # ---- auditoría v1.1 ------------------------------------------------------------------------
    # U20 kWh/ave nunca produce "pico"; pico solo desde lista de cargas
    ok = all(v is None for x in rs for kk, v in x.v.items() if "pico" in kk)
    import copy
    global KWH_T_PV
    xl = calcular(10000, 250, p=parametros("medio", lista_cargas=copy.deepcopy(CARGAS_DEMO)))
    guard = KWH_T_PV
    KWH_T_PV = ((1.0, 1.0, 1.0),) + KWH_T_PV[1:]
    try:
        xl2 = calcular(10000, 250, p=parametros("medio", lista_cargas=copy.deepcopy(CARGAS_DEMO)))
    finally:
        KWH_T_PV = guard
    esperado = 100 * 0.8 + 20 * 0.7 * 0.5 + 100 * 2.0
    ok &= _cerca(xl["potencia_pico_demanda_maxima_kw"], esperado) and \
        _cerca(xl2["potencia_pico_demanda_maxima_kw"], xl["potencia_pico_demanda_maxima_kw"])
    t("U20 potencia pico: PENDIENTE sin lista de cargas; con lista, independiente de kWh/ave", ok)
    ok = all(re.search(r"_bajo_\d+(\.\d+)?h$", kk) for x in rs for kk in x.v
             if kk.startswith("potencia_media") or kk.startswith("potencia_termica_media"))
    ok &= any(kk.startswith("potencia_media_equivalente") for kk in r.v)
    ok &= not any(kk.startswith("potencia_media") and not re.search(r"_bajo_\d", kk) for kk in r.v)
    t("U21 toda potencia media declara las horas usadas (_bajo_<h>h)", ok)
    m3 = dict(k, solidos_a_retirar=k["solidos_a_retirar"] * 3, plumas=k["plumas"] * 3, visceras=k["visceras"] * 3)
    r4 = calcular(10000, 250, "medio", masas=m3)
    ok = all(_cerca(r4[f"metodo{m}_carga_SST_kg_dia"], r[f"metodo{m}_carga_SST_kg_dia"]) for m in "AB")
    ok &= r["solidos_que_entran_efectivamente_al_efluente_t_dia"] is None
    ok &= not any("solidos_secos_retirados" in kk or "retirados_del_efluente" in kk for kk in r.v)
    t("U22 subproductos del balance no se contabilizan como SST ni como sólidos del efluente", ok)
    ok = r["lodo_solidos_secos_kg_dia"] is None and r["lodo_humedo_t_dia"] is None
    pl = lodos_ilustrativo("medio")
    sin_pct = dict(pl, fraccion_solidos_torta=None)
    sin_bio = dict(pl, rendimiento_biomasa_kg_ms_kg_dbo=None)
    l1 = lodos(350, 110, 500, 220, sin_pct)
    l2 = lodos(350, 110, 500, 220, sin_bio)
    l3 = lodos(350, 110, 500, 220, pl)
    ok &= l1["lodo_humedo_t_dia"] is None and l1["lodo_solidos_secos_kg_dia"] is not None
    ok &= l2["lodo_solidos_secos_kg_dia"] is None and l2["lodo_humedo_t_dia"] is None
    ok &= _cerca(l3["lodo_humedo_t_dia"], l3["lodo_solidos_secos_kg_dia"] / pl["fraccion_solidos_torta"] / 1000)
    ok &= _cerca(l3["lodo_solidos_secos_kg_dia"], l3["sst_removidos_kg_dia"] + l3["grasas_flotadas_kg_dia"]
                 + l3["solidos_quimicos_kg_dia"] + l3["biomasa_kg_ms_dia"])
    t("U23 lodos: PENDIENTE por defecto; sin % sólidos no hay lodo húmedo; sin modelo no hay lodo seco", ok)
    ok = all(v is None for kk, v in r.v.items() if kk.startswith("capacidad_frigorifica") or kk == "carga_frigorifica_total_kwf")
    ok &= "carga_frigorifica_total_kwf" in r.v and "carga_sensible_preliminar_producto_kwf_bajo_8h" in r.v
    notas = {f["variable"]: f["nota"] for f in r.filas}
    ok &= "NO es la capacidad frigorífica" in notas["carga_sensible_preliminar_producto_kwf_bajo_8h"]
    t("U24 carga sensible del producto no se denomina capacidad frigorífica; total PENDIENTE", ok)
    ok = r["grupo_electrogeno_kva"] is None
    xg = calcular(10000, 250, p=parametros("medio", lista_cargas_criticas=copy.deepcopy(CARGAS_DEMO[:1])))
    xg2 = calcular(20000, 250, p=parametros("medio", lista_cargas_criticas=copy.deepcopy(CARGAS_DEMO[:1])))
    ok &= xg["grupo_electrogeno_kva"] is not None and _cerca(xg["grupo_electrogeno_kva"], xg2["grupo_electrogeno_kva"])
    t("U25 grupo electrógeno: PENDIENTE sin lista de cargas críticas; nunca % fijo de la planta", ok)
    ok = all(all(lim.get(c) not in (None, "") for c in CAMPOS_LIMITE) for lim in LIMITES_EJEMPLO)
    try:
        parametros("medio", limites=[{"parametro": "DQO", "mg_l": 250.0}])
        ok = False
    except ErrorUtilities:
        pass
    ok &= all("jurisdiccion=" in f["parametro"] and "tipo_descarga=" in f["parametro"] and "EJEMPLO" in f["nota"]
              for f in r.filas if f["variable"].startswith("remocion_"))
    t("U26 límites regulatorios asociados a jurisdicción y tipo de descarga (solo ejemplo)", ok)
    rA = calcular(10000, 250, p=parametros("medio", conc_mg_l={"DQO": 9000.0, "DBO5": 1600.0, "SST": 1410.0}))
    rB = calcular(10000, 250, p=parametros("medio", carga_g_ave=dict(parametros("medio")["carga_g_ave"], DQO=300.0)))
    ok = _cerca(rA["metodoA_carga_DQO_kg_dia"], r["metodoA_carga_DQO_kg_dia"])
    ok &= _cerca(rB["metodoB_carga_DQO_kg_dia"], r["metodoB_carga_DQO_kg_dia"])
    ok &= not any(a[0] == "EFLUENTE_DQO" for a in r.alertas) and any(a[0] == "EFLUENTE_DQO" for a in rB.alertas)
    ok &= any(ALERTA_EFLUENTE in a[1] for a in rB.alertas)
    t("U27 métodos A y B independientes (sin calibración cruzada); divergencia -> alerta de validación", ok)
    ok = _cerca(r["agua_utilizada_m3_por_t_producto"], r["agua_utilizada_m3_dia"] / r["t_producto_comestible_dia_operativo"])
    xa = calcular(10000, 250, p=parametros("medio", l_ave_total=60))
    ok &= any(a[0] == "AGUA_M3_T" for a in xa.alertas) and not any(a[0] == "AGUA_M3_T" for a in r.alertas)
    t("U28 m³/t de producto coherente con L/ave; contraste fuera de rango -> alerta", ok)
    fil, al = contraste_bottom_up(r, [{"kw_nominal": 100.0, "factor_carga": 1.0, "horas_dia": 10.0}])
    ok = len(fil) == 1 and len(al) == 1
    fil2, al2 = contraste_bottom_up(r, [{"kw_nominal": r["kwh_proceso_dia"] / 10, "factor_carga": 1.0, "horas_dia": 10.0}])
    ok &= len(al2) == 0 and _cerca(fil2[0][3], 1.0)
    t("U29 contraste TOP-DOWN vs BOTTOM-UP (equipos 09A futuros): diferencias -> alerta, sin ajuste", ok)
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
    "M09": "cierre del agua forzado (evaporada inventada)",
    "M10": "potencia pico derivada de kWh/ave",
    "M11": "potencia media sin horas en el nombre",
    "M12": "SST = subproductos segregables del balance",
    "M13": "lodo húmedo con % de sólidos por defecto",
    "M14": "lodo seco fijo sin modelo de generación",
    "M15": "carga sensible del producto llamada capacidad frigorífica total",
    "M16": "kW eléctricos sin COP declarado",
    "M17": "congelación y almacenamiento en la misma variable/unidad",
    "M18": "grupo electrógeno = % fijo de la planta",
    "M19": "límite regulatorio sin jurisdicción ni tipo de descarga",
    "M20": "método B calibrado para cerrar con el método A",
}


def mutaciones():
    print("Prueba de mutación (cada mutación debe hacer fallar al menos un test):")
    todas = True
    for m, desc in MUTACIONES.items():
        _MUT.clear()
        _MUT.add(m)
        try:
            _, res = correr_tests(verbose=False)
            fallan = [nn.split()[0] for nn, ok, _ in res if not ok]
        except (ErrorUtilities, ZeroDivisionError, KeyError, TypeError) as e:
            fallan = [f"detiene: {type(e).__name__}: {e}"[:90]]
        _MUT.clear()
        print(f"  {m} {desc}: {'DETECTADA por ' + ', '.join(fallan) if fallan else 'NO DETECTADA'}")
        todas &= bool(fallan)
    return todas


# ---------------------------------------------------------------------------
# 6. CSV
# ---------------------------------------------------------------------------
CAMPOS = ["bloque", "escala_aves_dia", "dias_semana", "dias_anio", "nivel", "parametro", "variable", "valor",
          "unidad", "periodo", "base", "origen", "clasificacion", "referencia", "nota"]


def _fila_param(var, val, uni, org, ref, nota="", niv="-", bloque="parametros", E=0, ds=0, da=0, parametro=""):
    return {"bloque": bloque, "escala_aves_dia": E, "dias_semana": ds, "dias_anio": da, "nivel": niv,
            "parametro": parametro, "variable": var, "valor": val, "unidad": uni, "periodo": "parametro",
            "base": "-", "origen": org, "clasificacion": f"[{org}]" + (" [PVDP]" if org == "FUENTE" else ""),
            "referencia": ref, "nota": nota}


def construir():
    filas = []
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            for niv in NIVELES:
                r = calcular(E, da, niv)
                for f in r.filas:
                    filas.append(dict(f, escala_aves_dia=E, dias_semana=ds, dias_anio=da, nivel=niv))
                for cod, msg in r.alertas:
                    filas.append({"bloque": "alertas", "escala_aves_dia": E, "dias_semana": ds, "dias_anio": da,
                                  "nivel": niv, "parametro": "", "variable": f"alerta_{cod}", "valor": 1,
                                  "unidad": "índice", "periodo": "adimensional", "base": "-", "origen": "ESTIMACIÓN",
                                  "clasificacion": "[ALERTA]", "referencia": "", "nota": msg})
                pl = lodos_ilustrativo(niv)
                ri = calcular(E, da, niv, p=parametros(niv, lodos=pl))
                for f in ri.filas:
                    if f["bloque"] == "lodos":
                        filas.append(dict(f, bloque="lodos_ilustrativo", escala_aves_dia=E, dias_semana=ds,
                                          dias_anio=da, nivel=niv))
                for pid in ("P2", "P3"):
                    rp = calcular(E, da, niv, p=parametros(niv, perfil=dict(PERFILES[pid]), perfil_id=pid))
                    for var in ("capacidad_congelacion_t_dia", "capacidad_almacenamiento_congelado_t",
                                "stock_refrigerado_t", "carga_media_congelacion_producto_kwf_bajo_20h",
                                "kw_electricos_aprox_congelacion_producto", "kwh_congelacion_dia",
                                "kwh_almacenamiento_frio_dia_calendario", "carga_critica_ilustrativa_escenario_kw"):
                        f = next(x for x in rp.filas if x["variable"] == var)
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
    for niv in NIVELES:
        for c, etq, vals, org, ref in AGUA_ETAPAS:
            filas.append(_fila_param(f"param_agua_{c}_l_ave", nv(vals, niv), "L/ave", org, ref,
                                     f"{etq}; rango de sensibilidad", niv))
        filas.append(_fila_param("param_fraccion_agua_a_efluente", nv(FRAC_EFLUENTE, niv), "fracción", "SUPUESTO",
                                 "", "editable (--frac-efluente)", niv))
        for par, (vals, ref) in CARGA_G_AVE.items():
            filas.append(_fila_param(f"param_metodoA_{par}_g_ave", nv(vals, niv), "g/ave", "FUENTE", ref,
                                     "escenario", niv))
        for par, (vals, ref) in CONC_MG_L.items():
            filas.append(_fila_param(f"param_metodoB_{par}_mg_l", nv(vals, niv), "mg/L", "FUENTE", ref, "", niv))
        for kk, (vals, uni, org, ref) in LODOS_ILUSTRATIVO.items():
            filas.append(_fila_param(f"param_lodos_ilustrativo_{kk}", nv(vals, niv), uni, org, ref,
                                     "solo escenario ilustrativo", niv))
        for var, prm in (("cop_enfriado", COP_ENFRIADO), ("cop_congelado", COP_CONGELADO)):
            filas.append(_fila_param(f"param_{var}", nv(prm, niv), "COP", "SUPUESTO", prm[2], "", niv))
    filas.append(_fila_param("param_tolerancia_metodos_efluente", TOLERANCIA_METODOS, "ratio", "SUPUESTO", "",
                             "B/A fuera de [1/t, t] -> alerta"))
    filas.append(_fila_param("param_fraccion_rechazo_potabilizacion", FRAC_RECHAZO_POTABILIZACION, "fracción",
                             "SUPUESTO", "", "dato de sitio"))
    for lim in LIMITES_EJEMPLO:
        filas.append(_fila_param(f"limite_ejemplo_{lim['parametro']}_mg_l", lim["mg_l"], "mg/L", "FUENTE", lim["ref"],
                                 "EJEMPLO REGULATORIO DE REFERENCIA; no es requisito del proyecto",
                                 parametro=f"jurisdiccion={lim['jurisdiccion']}; autoridad={lim['autoridad']}; "
                                           f"norma={lim['norma']}; tipo_descarga={lim['tipo_descarga']}"))
    for f in filas:
        f["valor"] = "" if f["valor"] is None else round(float(f["valor"]), 6)
    return filas


def escribir_csv(filas):
    with open(CSV_SALIDA, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, lineterminator="\n")
        w.writeheader()
        w.writerows(filas)


# ---------------------------------------------------------------------------
# 7. TABLAS Y CLI
# ---------------------------------------------------------------------------
def fmt(x, d=1):
    if x is None:
        return "PENDIENTE"
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def tablas():
    rs = {(E, n): calcular(E, 250, n) for E in ESCALAS for n in NIVELES}
    ri = {(E, n): calcular(E, 250, n, p=parametros(n, lodos=lodos_ilustrativo(n))) for E in ESCALAS for n in NIVELES}
    filas = [("Agua utilizada m³/día", "agua_utilizada_m3_dia", 0), ("Agua captada m³/día", "agua_captada_m3_dia", 0),
             ("Agua descargada m³/día", "agua_descargada_m3_dia", 0),
             ("Agua incorporada t/día", "agua_incorporada_producto_y_subproductos_t_dia", 2),
             ("Agua evaporada/arrastrada m³/día", "agua_evaporada_o_arrastrada_m3_dia", 1),
             ("m³/t producto", "agua_utilizada_m3_por_t_producto", 1),
             ("DQO A kg/día", "metodoA_carga_DQO_kg_dia", 0), ("DQO B kg/día", "metodoB_carga_DQO_kg_dia", 0),
             ("B/A DQO", "relacion_B_sobre_A_DQO", 2), ("DBO A kg/día", "metodoA_carga_DBO5_kg_dia", 0),
             ("DBO B kg/día", "metodoB_carga_DBO5_kg_dia", 0), ("B/A DBO", "relacion_B_sobre_A_DBO5", 2),
             ("SST A kg/día", "metodoA_carga_SST_kg_dia", 0), ("SST B kg/día", "metodoB_carga_SST_kg_dia", 0),
             ("B/A SST", "relacion_B_sobre_A_SST", 2),
             ("Conc. implícita A DQO mg/L", "metodoA_concentracion_implicita_DQO_mg_l", 0),
             ("Remoción DQO ejemplo A %", "remocion_DQO_bajo_ejemplo_limite_metodoA_pct", 1),
             ("Remoción DQO ejemplo B %", "remocion_DQO_bajo_ejemplo_limite_metodoB_pct", 1),
             ("Segregable en origen t/día", "masa_biologica_potencialmente_segregable_en_origen_t_dia", 1),
             ("kWh/día operativo", "kwh_total_dia_operativo", 0),
             ("P media proceso kW (14 h)", "potencia_media_equivalente_proceso_kw_bajo_14h", 0),
             ("P media total kW (24 h)", "potencia_media_equivalente_total_kw_bajo_24h", 0),
             ("Calor útil MJ/día", "calor_util_mj_dia", 0),
             ("P térmica media limpieza kW (4 h)", "potencia_termica_media_equivalente_limpieza_kw_bajo_4h", 0),
             ("P térmica media escaldado kW (8 h)", "potencia_termica_media_equivalente_escaldado_kw_bajo_8h", 0),
             ("Carga sensible producto kWf (8 h)", "carga_sensible_preliminar_producto_kwf_bajo_8h", 0),
             ("Agua chiller kWf (8 h)", "carga_enfriamiento_agua_reposicion_chiller_kwf_bajo_8h", 0),
             ("Adicionales ilustrativas kWf", "cargas_adicionales_ilustrativas_kwf", 0),
             ("kWe aprox producto", "kw_electricos_aprox_producto", 0),
             ("Brecha top-down/físico", "brecha_frio_fisico_vs_reparto_indicador_ratio", 1),
             ("Carga crítica ilustrativa kW", "carga_critica_ilustrativa_escenario_kw", 0)]
    print("| Variable | " + " | ".join(fmt(E, 0) for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for etq, var, d in filas:
        print(f"| {etq} | " + " | ".join(" · ".join(fmt(rs[(E, n)][var], d) for n in NIVELES) for E in ESCALAS) + " |")
    for var in ("sst_removidos_kg_dia", "grasas_flotadas_kg_dia", "solidos_quimicos_kg_dia", "biomasa_kg_ms_dia",
                "lodo_solidos_secos_kg_dia", "lodo_humedo_t_dia"):
        print(f"| ILUSTRATIVO {var} | " + " | ".join(" · ".join(fmt(ri[(E, n)][var], 1) for n in NIVELES)
                                                   for E in ESCALAS) + " |")
    print("\nAlertas (10.000 aves/día):")
    for n in NIVELES:
        for cod, msg in rs[(10000, n)].alertas:
            print(f"  {n}: {cod} — {msg}")


def escenario_cli(a):
    ov = {}
    if a.l_ave is not None:
        ov["l_ave_total"] = a.l_ave
    if a.frac_efluente is not None:
        ov["frac_efluente"] = a.frac_efluente
    if a.dqo_g_ave is not None:
        c = {k: nv(v, a.nivel) for k, v in CARGA_G_AVE.items()}
        f = a.dqo_g_ave / c["DQO"]
        ov["carga_g_ave"] = {k: v * f for k, v in c.items()}   # método A en proporción a la DQO
    if a.dqo_mg_l is not None:
        c = {k: nv(v, a.nivel) for k, v in CONC_MG_L.items()}
        f = a.dqo_mg_l / c["DQO"]
        ov["conc_mg_l"] = {k: v * f for k, v in c.items()}     # método B en proporción a la DQO
    if a.frac_sangre is not None:
        ov["fraccion_sangre_recuperada"] = a.frac_sangre
    if a.perfil:
        x = [float(v) for v in a.perfil.split(",")]
        ov["perfil"] = dict(zip(("refrigerado", "congelado", "exportacion"), x))
        ov["perfil_id"] = "manual"
    if a.lodos_ilustrativo:
        ov["lodos"] = lodos_ilustrativo(a.nivel)
    for k in ("dias_refrigerado", "dias_congelado", "base_inventario", "horas_netas"):
        if getattr(a, k) is not None:
            ov[k] = getattr(a, k)
    r = calcular(a.aves_dia, a.dias_anio, a.nivel, p=parametros(a.nivel, **ov))
    print(f"Escenario: {fmt(a.aves_dia, 0)} aves/día · {a.dias_anio} días/año · nivel {a.nivel}")
    for f in r.filas:
        print(f"  {f['bloque']:<16} {f['variable']:<58} {fmt(f['valor'], 2):>14} {f['unidad']:<16} {f['clasificacion']}")
    for cod, msg in r.alertas:
        print(f"  ALERTA {cod}: {msg}")


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
    ap.add_argument("--frac-efluente", type=float, help="SUPUESTO editable: fracción del agua utilizada a efluente")
    ap.add_argument("--dqo-g-ave", type=float, help="método A: g DQO/ave (DBO, SST, GyA, NTK, PT en proporción)")
    ap.add_argument("--dqo-mg-l", type=float, help="método B: mg/L DQO (DBO y SST en proporción)")
    ap.add_argument("--frac-sangre", type=float, help="fracción de sangre recuperada (0–1)")
    ap.add_argument("--perfil", help="refrigerado,congelado,exportacion (fracciones que suman 1)")
    ap.add_argument("--lodos-ilustrativo", action="store_true", help="calcula lodos con los supuestos ilustrativos")
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
