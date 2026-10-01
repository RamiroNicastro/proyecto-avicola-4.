#!/usr/bin/env python3
"""
MODELO CONCEPTUAL DE SUPERFICIES — versión 1.0.1 (2026-10-01, sesión 12C: layout y obra civil)
=========================================================================================

¿QUÉ ÁREAS NECESITA LA PLANTA, CUÁNTO MIDEN (EN RANGO) Y CUÁNTO TERRENO EXIGEN?

v1.0.1 (corrección de interpretación): sin cambios de cálculo; agrega el tipo de ORIGEN A–E de cada área
(ORIGEN_AREA, columna `origen_superficie`), `supuestos_terreno` en salida_interfaz(), la fila margen_perimetral_m
y los tests T19–T21 (nada etiquetado como verificado; retiro/buffer variables y con efecto sobre el terreno).
Las superficies sirven para comparar escalas y reservar órdenes de magnitud; NO son anteproyecto ni
superficie habilitable.

ESTADO: modelo de ORDEN DE MAGNITUD para prefactibilidad. NO es un programa arquitectónico, NO es un
plano, NO dimensiona equipos, NO calcula CAPEX ni OPEX, NO elige terreno, tecnología de efluentes,
método de enfriamiento, número de líneas ni proveedor. Cada superficie es un RANGO bajo / medio / alto
(bajo = menos m²). Ninguna cifra es un dato de campo argentino.

ENTRADAS (todas editables; ver `entradas_por_defecto()`):
  escala (aves faenadas/día operativo) · horas netas · configuración de producto A/B/C (= mix del balance
  v1.1: entero / trozado / deshuesado) · perfil de destino P1–P3 y días de inventario (base temporal) ·
  automatización (manual / semi / auto) · líneas (1 / 2) · enfriamiento (inmersión / aire / sin_definir) ·
  tecnología de efluentes (cloaca / aerobio_compacto / anaerobio_aerobio / lagunas / sin_definir) ·
  escala objetivo de expansión · reserva para rendering · dotación por turno · aves por camión ·
  t por camión de despacho · footprints de equipos por área (RFQ) · retiros, buffers, FOS.

INSUMOS DE OTROS MÓDULOS (se IMPORTAN; no se recalculan):
  * 05_proceso_industrial/modelo_capacidad_proceso.py (09A): kg/ave por configuración (a trozado, a
    deshuese, a CMS, comestible, garras, menudencias, sólidos), ritmo = escala / horas netas, tiempos de
    residencia del enfriamiento (inmersión 50 min; aire 90–150 min).
  * 11_agua_efluentes/modelo_utilities.py (09C): stock refrigerado y congelado (t), capacidad de
    congelación (t/día), agua descargada (m³/día), caudal horario máximo ilustrativo, cargas de DBO/DQO
    por los dos métodos. El modelo de frío de 09C NO se rehace: aquí solo se convierte t en m².

MÉTODO (por área; detalle en README §3 y en programa_areas.md):
  (1) FOOTPRINT: si se informa la huella de equipos de un área (m², de layout de proveedor/RFQ):
        m² = huella × factor de envolvente (pasillos, mantenimiento, buffers, higiene)       [SUPUESTO]
  (2) DRIVER FÍSICO + DENSIDAD: cámaras = stock (t) × factor de pico ÷ densidad de estiba (t/m²);
        andenes = posiciones de camión × m²/posición; vestuarios = personas × m²/persona; etc.
  (3) PROXY DE INTENSIDAD (si falta la huella de equipos): m² = k × (driver/1.000)^β, con mínimo
        funcional; k y mínimos son [SUPUESTO] de orden de magnitud SIN fuente; se emite la alerta
        FOOTPRINT_DESCONOCIDO y el área queda en estado PROXY. Con `estricto=True` el área queda en
        None (PENDIENTE) y los totales que la incluyen también: NUNCA se convierte en cero.
  (4) NO_APLICA: el área no existe en la configuración (p. ej., deshuese en config. A/B, biológico con
        vuelco a colectora). Se declara explícitamente; no es un cero silencioso.

TOTALES:
  m² construidos (cubiertos) = proceso + frío + servicios + personal/admin
  m² operativos              = construidos + exteriores + efluentes
  terreno conceptual         = (huella + exteriores + efluentes + reserva de expansión)
                               ampliado por retiros y buffers perimetrales (rectángulo de relación
                               largo/ancho dada), y nunca menor que huella ÷ FOS si el FOS se conoce.
  reserva de expansión       = Σ max(0, área(escala objetivo) − área(escala actual)) por categoría
                               (+ reserva para rendering futuro si se pide); sin objetivo: fracción
                               [SUPUESTO] de lo operativo, con alerta.

Uso
---
    python3 09_layout_obra_civil/modelo_superficies.py                # tests + CSV
    python3 09_layout_obra_civil/modelo_superficies.py --solo-tests
    python3 09_layout_obra_civil/modelo_superficies.py --mutaciones   # los tests detectan errores sembrados
    python3 09_layout_obra_civil/modelo_superficies.py --tablas       # tablas resumen para los .md
    python3 09_layout_obra_civil/modelo_superficies.py --escenario --aves-dia 7500 --config C \
        --perfil P3 --dias-congelado 28 --lineas 2 --efluentes lagunas --objetivo 20000

El script se DETIENE (código 1) si falla cualquier prueba. Unidades: m², t, m³, h (regla 14).
Separador decimal del CSV: punto.
"""
import argparse
import copy
import csv
import math
import os
import re
import sys
from functools import lru_cache

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _d in ("05_proceso_industrial", "23_plan_expansion", "11_agua_efluentes"):
    _p = os.path.join(RAIZ, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import modelo_capacidad_proceso as mc   # noqa: E402  (09A; importa 23 → 04 → 03)
import modelo_utilities as mu           # noqa: E402  (09C)

VERSION = "1.0.1"
FECHA = "2026-10-01"
CSV_SALIDA = os.path.join(AQUI, "escenarios_superficies.csv")
ESCALAS = (2500, 5000, 10000, 20000)
NIVELES = ("bajo", "medio", "alto")      # RANGO de superficie: bajo = menos m²
CATEGORIAS = ("proceso", "frio", "servicios", "personal_admin", "exteriores", "efluentes")
CUBIERTAS = ("proceso", "frio", "servicios", "personal_admin")
TECNOLOGIAS = ("cloaca", "aerobio_compacto", "anaerobio_aerobio", "lagunas")
ENFRIAMIENTOS = ("inmersion", "aire", "sin_definir")
AUTOMATIZACION = ("manual", "semi", "auto")
PERFILES = dict(mu.PERFILES)             # P1–P3 de 09C (SUP-055)
_MUT: set = set()                        # mutaciones activas (solo --mutaciones)


class ErrorSuperficies(Exception):
    pass


# ---------------------------------------------------------------------------
# 1. PARÁMETROS — triples (bajo, medio, alto) EN SENTIDO DE SUPERFICIE (el "bajo" da menos m²)
#    Origen: SUPUESTO = hipótesis del analista sin fuente; PVDP = extracto no leído en original;
#    PROXY = sustituto de un dato faltante (genera alerta). Ningún valor está validado.
# ---------------------------------------------------------------------------
def T(b, m, a, origen="SUPUESTO", ref="SUP-107", nota=""):
    return {"v": (b, m, a), "origen": origen, "ref": ref, "nota": nota}


BETA = 0.80   # [SUPUESTO] economía de escala espacial de salas de proceso (SUP-107)

# Proxy de intensidad: m² = k × (driver/1.000)^β, con mínimo funcional (SUP-107, sin fuente)
K = {
    # driver: ritmo por línea (aves/h)
    "colgado_aturdido":            (T(80, 110, 150),  T(30, 40, 55)),
    "sangrado_escaldado_desplumado": (T(170, 230, 310), T(60, 80, 110)),
    "evisceracion_inspeccion":     (T(200, 270, 370), T(60, 80, 110)),
    "clasificacion":               (T(25, 35, 50),    T(10, 15, 20)),
    "lavado_cajones":              (T(60, 90, 130),   T(25, 35, 50)),
    # driver: kg/h de material que entra a la sala (09A, kg_ave_config × ritmo)
    "trozado":                     (T(110, 150, 200), T(25, 35, 50)),
    "deshuese":                    (T(220, 300, 400), T(40, 55, 75)),
    "cms":                         (T(60, 80, 110),   T(20, 25, 35)),
    "coproductos":                 (T(350, 450, 600), T(25, 35, 50)),
    "empaque":                     (T(90, 120, 160),  T(30, 40, 55)),
    # driver: ritmo total (aves/h)
    "residuos_carton":             (T(20, 30, 45),    T(12, 15, 20)),
    "caldera_agua_caliente":       (T(40, 55, 75),    T(20, 25, 35)),
    "aire_comprimido":             (T(12, 18, 25),    T(8, 10, 15)),
    "sala_electrica":              (T(35, 50, 70),    T(20, 25, 35)),
    "generador":                   (T(15, 25, 40),    T(12, 15, 20)),
    "mantenimiento_taller":        (T(60, 90, 130),   T(40, 55, 75)),
    "repuestos":                   (T(25, 40, 60),    T(15, 20, 30)),
    "laboratorio_calidad":         (T(15, 25, 40),    T(12, 15, 20)),
    "quimicos":                    (T(8, 12, 18),     T(6, 8, 12)),
    "oficina_senasa":              (T(20, 30, 45),    T(20, 30, 45)),
    "enfermeria_capacitacion":     (T(15, 25, 40),    T(15, 25, 40)),
}

P = {
    # --- recepción y andén de espera (bahías de camión) ---
    "espera_h": T(1.0, 1.5, 2.0, "SUPUESTO", "SUP-108", "horas de aves en espera (buffer entre llegada y colgado)"),
    "aves_por_camion_proxy": T(6000, 4500, 3000, "PROXY", "DPV-084", "aves por camión de vivo; dato pendiente"),
    "m2_bahia_recepcion": T(70, 90, 120, "SUPUESTO", "SUP-108", "bahía cubierta y ventilada por camión"),
    # --- líneas ---
    "factor_separacion_dos_lineas": T(1.05, 1.10, 1.15, "SUPUESTO", "SUP-109", "pasillos entre líneas"),
    "factor_automatizacion": {"manual": 1.20, "semi": 1.00, "auto": 0.90, "origen": "SUPUESTO",
                              "ref": "SUP-109", "nota": "superficie de salas con puestos (evisceración, "
                                                          "trozado, deshuese, empaque); débil"},
    # --- enfriamiento: m² por carcasa simultánea (residencias de 09A) ---
    "m2_carcasa_inmersion": T(0.15, 0.20, 0.28, "SUPUESTO", "SUP-110", "tanques + perímetro de operación"),
    "m2_carcasa_aire": T(0.10, 0.14, 0.20, "SUPUESTO", "SUP-110", "riel multinivel en cámara"),
    "min_enfriamiento": T(30, 40, 55, "SUPUESTO", "SUP-110"),
    # --- circulación interna de proceso (pasillos técnicos, esclusas, barreras sanitarias) ---
    "f_circulacion_proceso": T(0.15, 0.22, 0.30, "SUPUESTO", "SUP-111"),
    # --- depósito de envases e insumos secos ---
    "m2_envases_por_t_dia": T(5, 8, 12, "SUPUESTO", "SUP-111", "m² por t/día de comestible"),
    "min_envases": T(20, 30, 40, "SUPUESTO", "SUP-111"),
    # --- FRÍO (convierte t de 09C en m²; no rehace el balance frigorífico) ---
    "factor_pico_stock": T(1.15, 1.30, 1.50, "SUPUESTO", "SUP-112", "stock máximo / stock del escenario"),
    "densidad_refrigerado_t_m2": T(1.0, 0.7, 0.5, "PVDP", "FTE-293; SUP-112",
                                   "5–7 m³ brutos/t × altura útil 3,5–5 m (extracto comercial)"),
    "densidad_congelado_t_m2": T(1.75, 1.25, 0.9, "PVDP", "FTE-292; SUP-112",
                                 "~4 m³ brutos/t de carne congelada × altura útil 3,6–7 m (FAO, extracto)"),
    "min_camara_refrigerada": T(20, 25, 30, "SUPUESTO", "SUP-112"),
    "min_camara_congelada": T(15, 20, 30, "SUPUESTO", "SUP-112"),
    "f_antecamara": T(0.20, 0.30, 0.40, "SUPUESTO", "SUP-112", "antecámaras, pasillo frío, preparación de pedidos"),
    "m2_tunel_por_t_dia": T(6, 9, 14, "SUPUESTO", "SUP-112; DPV-137", "túnel/espiral: huella real por RFQ"),
    "min_tunel": T(12, 15, 20, "SUPUESTO", "SUP-112"),
    "factor_tecnologia_congelado": {"sin_definir": 1.0, "estatico": 1.0, "lineal": 1.0, "espiral": 0.35,
                                    "origen": "PVDP", "ref": "FTE-215",
                                    "nota": "espiral 60–70 % menos superficie que túnel lineal (extracto débil)"},
    # --- expedición ---
    "factor_pico_despacho": T(1.0, 1.2, 1.5, "SUPUESTO", "SUP-113"),
    "t_por_camion_proxy": T(12, 8, 5, "PROXY", "DPV-084; DPV-036", "t por camión refrigerado de despacho"),
    "cargas_por_dock_dia": T(4, 3, 2, "SUPUESTO", "SUP-113"),
    "m2_dock_interior": T(35, 45, 60, "SUPUESTO", "SUP-113"),
    "m2_playa_por_dock": T(150, 200, 250, "SUPUESTO", "SUP-113", "maniobra exterior frente a cada dock"),
    # --- subproductos ---
    "dias_subproductos_refrigerados": T(0.5, 1.0, 3.0, "SUPUESTO", "SUP-056; SUP-114"),
    "densidad_subproductos_t_m2": T(0.7, 0.5, 0.35, "SUPUESTO", "SUP-114"),
    "min_camara_subproductos": T(8, 10, 15, "SUPUESTO", "SUP-114"),
    "m2_decomisos": T(6, 8, 12, "SUPUESTO", "SUP-114; DPV-090"),
    "m2_sala_subproductos_por_t_dia": T(10, 15, 22, "SUPUESTO", "SUP-114"),
    "min_sala_subproductos": T(25, 35, 50, "SUPUESTO", "SUP-114"),
    # --- servicios ---
    "f_sala_maquinas_frio": T(0.12, 0.18, 0.25, "PROXY", "SUP-115; DPV-109", "carga frigorífica total PENDIENTE (09C)"),
    "min_sala_maquinas_frio": T(40, 60, 80, "SUPUESTO", "SUP-115"),
    "m2_tratamiento_agua_por_m3_dia": T(0.08, 0.12, 0.18, "SUPUESTO", "SUP-115"),
    "min_tratamiento_agua": T(15, 20, 30, "SUPUESTO", "SUP-115"),
    "dias_reserva_agua": T(0.5, 1.0, 1.5, "SUPUESTO", "SUP-115; DPV-053", "incluye reserva de incendio a definir (DPV-106)"),
    "altura_tanque_m": T(6, 5, 4, "SUPUESTO", "SUP-115"),
    "m2_lavanderia_por_persona": T(0.15, 0.20, 0.30, "SUPUESTO", "SUP-115"),
    # --- personal / admin ---
    "dotacion_base_proxy": T(10, 15, 20, "PROXY", "SUP-116; DPV-138", "personas fijas por turno"),
    "dotacion_por_ave_h_proxy": T(0.05, 0.08, 0.12, "PROXY", "SUP-116; DPV-138", "personas por ave/h"),
    "factor_dotacion_automatizacion": {"manual": 1.35, "semi": 1.0, "auto": 0.75, "origen": "PROXY",
                                       "ref": "SUP-116", "nota": ""},
    "factor_dotacion_config": {"A": 0.9, "B": 1.0, "C": 1.3, "origen": "PROXY", "ref": "SUP-116", "nota": ""},
    "m2_vestuario_por_persona": T(1.0, 1.3, 1.7, "SUPUESTO", "SUP-116; DPV-090", "vestuarios y sanitarios por zona y sexo"),
    "factor_vestuario_segundo_turno": T(0.4, 0.6, 0.8, "SUPUESTO", "SUP-116", "lockers del 2.º turno"),
    "min_vestuarios": T(40, 50, 70, "SUPUESTO", "SUP-116", "dos vestuarios mínimos (sucia/limpia)"),
    "fraccion_comedor_simultaneo": T(0.33, 0.5, 0.5, "SUPUESTO", "SUP-116"),
    "m2_comensal": T(1.2, 1.5, 1.8, "SUPUESTO", "SUP-116"),
    "min_comedor": T(20, 30, 40, "SUPUESTO", "SUP-116"),
    "admin_puestos": T(4, 6, 10, "SUPUESTO", "SUP-116"),
    "m2_puesto_oficina": T(8, 10, 12, "SUPUESTO", "SUP-116"),
    "min_oficinas": T(40, 60, 80, "SUPUESTO", "SUP-116"),
    "m2_porteria": T(10, 15, 20, "SUPUESTO", "SUP-116"),
    "f_circulacion_personal": T(0.10, 0.15, 0.20, "SUPUESTO", "SUP-116"),
    # --- exteriores ---
    "m2_camion_playa": T(150, 200, 250, "SUPUESTO", "SUP-117", "estacionamiento/maniobra de un camión"),
    "m2_lavado_camion": T(100, 130, 160, "SUPUESTO", "SUP-117"),
    "camiones_por_plataforma_lavado": T(12, 10, 8, "SUPUESTO", "SUP-117"),
    "m2_playa_subproductos_base": T(100, 150, 200, "SUPUESTO", "SUP-117"),
    "m2_playa_subproductos_por_t_dia": T(5, 8, 12, "SUPUESTO", "SUP-117"),
    "fraccion_personal_motorizado": T(0.20, 0.35, 0.50, "SUPUESTO", "SUP-117; DPV-139"),
    "m2_plaza_auto": T(20, 25, 28, "SUPUESTO", "SUP-117"),
    "plazas_visitas": T(4, 6, 10, "SUPUESTO", "SUP-117"),
    "f_circulacion_pesada": T(0.25, 0.35, 0.50, "SUPUESTO", "SUP-117", "caminos internos separados por flujo"),
    # --- efluentes (NO se elige tecnología; reglas de ingeniería sanitaria de manual, sin lectura primaria) ---
    "m2_pretrat_por_m3_h": T(1.0, 1.5, 2.0, "SUPUESTO", "SUP-118"),
    "min_pretratamiento": T(40, 60, 80, "SUPUESTO", "SUP-118"),
    "fraccion_ecualizacion": T(0.30, 0.50, 0.70, "SUPUESTO", "SUP-118", "volumen / caudal diario"),
    "prof_ecualizacion_m": T(4.5, 4.0, 3.5, "SUPUESTO", "SUP-118"),
    "carga_superficial_daf_m3_m2_h": T(6, 5, 4, "PVDP", "FTE-294; SUP-118"),
    "factor_huella_daf": T(3, 4, 5, "SUPUESTO", "SUP-118", "equipo + accesos + químicos"),
    "min_daf": T(20, 30, 40, "SUPUESTO", "SUP-118"),
    "remocion_dbo_daf": T(0.60, 0.45, 0.30, "PVDP", "FTE-256 (09C)", "DAF 30–90 % DBO"),
    "remocion_dqo_daf": T(0.80, 0.75, 0.70, "PVDP", "FTE-256 (09C)", "DAF 70–80 % DQO"),
    "carga_vol_aerobia_kg_dbo_m3_d": T(0.8, 0.5, 0.3, "PVDP", "FTE-294; SUP-118"),
    "prof_aerobio_m": T(5.0, 4.5, 4.0, "SUPUESTO", "SUP-118"),
    "factor_huella_aerobio": T(1.4, 1.6, 1.9, "SUPUESTO", "SUP-118", "clarificador, bordes, accesos"),
    "min_biologico": T(10, 20, 30, "SUPUESTO", "SUP-118", "mínimo funcional de un tren biológico"),
    "carga_vol_anaerobia_kg_dqo_m3_d": T(8, 5, 3, "PVDP", "FTE-263 (09C); FTE-294", "7–11 en ensayos"),
    "prof_reactor_anaerobio_m": T(6.0, 5.5, 5.0, "SUPUESTO", "SUP-118"),
    "factor_huella_anaerobio": T(1.3, 1.5, 1.8, "SUPUESTO", "SUP-118"),
    "fraccion_dbo_a_pulido": T(0.20, 0.30, 0.40, "SUPUESTO", "SUP-118", "DBO residual tras anaerobio"),
    "carga_vol_laguna_anaerobia_kg_dbo_m3_d": T(0.35, 0.25, 0.15, "PVDP", "FTE-294; SUP-118"),
    "prof_laguna_anaerobia_m": T(5.0, 4.0, 3.0, "SUPUESTO", "SUP-118"),
    "fraccion_dbo_a_laguna_facultativa": T(0.40, 0.50, 0.60, "SUPUESTO", "SUP-118"),
    "carga_sup_laguna_facultativa_kg_dbo_ha_d": T(350, 250, 150, "PVDP", "FTE-294; SUP-118", "depende del clima"),
    "factor_taludes_lagunas": T(1.2, 1.3, 1.5, "SUPUESTO", "SUP-118"),
    "m2_lodos_por_kg_dbo_d": T(0.10, 0.15, 0.25, "PROXY", "SUP-118; DPV-114", "lodos PENDIENTES en 09C"),
    "min_lodos": T(30, 50, 80, "PROXY", "SUP-118"),
    "f_circulacion_efluentes": T(0.25, 0.30, 0.40, "SUPUESTO", "SUP-118"),
    # --- reserva y terreno ---
    "fraccion_reserva_sin_objetivo": T(0.25, 0.50, 1.00, "SUPUESTO", "SUP-119", "solo si no hay escala objetivo"),
    "m2_rendering_por_t_dia": T(40, 60, 90, "PROXY", "SUP-119; DPV-065; DEC-027", "rendering futuro (reserva, no se construye)"),
    "min_rendering": T(300, 400, 600, "PROXY", "SUP-119"),
    "factor_envolvente_footprint": T(2.2, 2.8, 3.5, "SUPUESTO", "SUP-120", "m² de sala / m² de huella de equipos"),
    "retiro_m": T(5, 10, 15, "SUPUESTO", "SUP-121; DPV-106", "retiro perimetral municipal"),
    "buffer_proxy_m": T(10, 20, 40, "PROXY", "SUP-121; DPV-087", "franja de bioseguridad/vecindad"),
    "relacion_largo_ancho": T(1.5, 1.5, 1.5, "SUPUESTO", "SUP-121"),
}

# Áreas cuya superficie depende de la HUELLA DE EQUIPOS (si falta: PROXY + alerta; estricto: None)
EQUIPOS_POR_AREA = {  # documental: qué huellas pedir en el RFQ (08_maquinaria/matriz_equipos.csv)
    "colgado_aturdido": "EQ-04, EQ-07, EQ-08, EQ-09/EQ-10",
    "sangrado_escaldado_desplumado": "EQ-11 a EQ-18, EQ-20",
    "evisceracion_inspeccion": "EQ-19, EQ-21 a EQ-33",
    "enfriamiento": "EQ-34/EQ-35/EQ-36, EQ-37, EQ-38",
    "clasificacion": "EQ-39",
    "trozado": "EQ-40, EQ-41",
    "deshuese": "EQ-42 a EQ-46",
    "cms": "EQ-48",
    "coproductos": "EQ-28, EQ-33, EQ-47",
    "empaque": "EQ-49 a EQ-56",
    "lavado_cajones": "EQ-05",
    "tunel_congelado": "EQ-57 a EQ-61",
    "sala_maquinas_frio": "EQ-64",
    "caldera_agua_caliente": "EQ-14",
    "aire_comprimido": "EQ-71",
    "generador": "EQ-73",
    "sala_subproductos": "EQ-66 a EQ-69",
}


# Tipo de ORIGEN de cada superficie (v1.0.1, corrección de interpretación 12C). Metadato: no cambia ningún cálculo.
#   A = derivada de un modelo existente (09A/09C: t, kg/h, caudales, residencias)
#   B = calculada con factor de diseño [SUPUESTO] (densidades, m²/persona, fracciones de circulación)
#   C = proxy preliminar (sustituto de un dato faltante; genera alerta)
#   D = footprint pendiente de proveedor (la sala depende de la huella de equipos aún no recibida)
#   E = requisito regulatorio pendiente (norma no leída en original o dependiente de jurisdicción)
# El primer código es el que domina la calidad del resultado. NINGUNA superficie es [VERIFICADO].
TIPOS_ORIGEN = {"A": "DERIVADA DE MODELO EXISTENTE", "B": "CALCULADA CON FACTOR DE DISEÑO",
                "C": "PROXY PRELIMINAR", "D": "FOOTPRINT PENDIENTE DE PROVEEDOR",
                "E": "REQUISITO REGULATORIO PENDIENTE"}
ORIGEN_AREA = {
    "recepcion_espera": "C·B·E", "colgado_aturdido": "C·D", "sangrado_escaldado_desplumado": "C·D·E",
    "evisceracion_inspeccion": "C·D·E", "enfriamiento": "A·B·D", "clasificacion": "C·D", "trozado": "C·D",
    "deshuese": "C·D", "cms": "C·D·E", "coproductos": "C·D", "empaque": "C·D", "lavado_cajones": "C·D",
    "circulacion_proceso": "B·E", "camaras_refrigeradas": "A·B", "camaras_congeladas": "A·B",
    "tunel_congelado": "A·C·D", "antecamaras_preparacion": "B", "expedicion_docks": "C·B",
    "camara_subproductos": "A·B", "camara_decomisos": "B·E", "sala_subproductos": "A·B", "residuos_carton": "B",
    "deposito_envases": "A·B", "sala_maquinas_frio": "C·D", "caldera_agua_caliente": "C·D",
    "aire_comprimido": "C·D", "generador": "C·D", "sala_electrica": "C", "tratamiento_agua": "A·B",
    "mantenimiento_taller": "B", "repuestos": "B", "quimicos": "B", "laboratorio_calidad": "B",
    "vestuarios": "C·B·E", "comedor": "C·B", "lavanderia": "C·B", "oficinas": "B", "oficina_senasa": "B·E",
    "enfermeria_capacitacion": "B", "porterias_seguridad": "B", "circulacion_personal": "B",
    "playa_aves_vivas": "C·B", "lavado_camiones": "B·E", "playa_despacho": "C·B", "playa_subproductos": "A·B",
    "estacionamiento": "C·B", "tanques_agua": "A·B·E", "circulacion_pesada": "B",
    "efl_pretratamiento": "A·B", "efl_ecualizacion": "A·B", "efl_daf": "A·B", "efl_biologico": "A·B·E",
    "efl_lodos": "C", "efl_circulacion": "B", "reserva_expansion": "B·C",
}
ORIGEN_TERRENO = "B·C·E — retiro y buffer VARIABLES (retiro reglamentario: DPV-141; buffer de diseño: SUP-121)"


def entradas_por_defecto():
    """Escenario de referencia (no es decisión): config. B, P1 con 3/14 días, semi, 1 línea."""
    return {
        "aves_dia": 10000, "horas_netas": 8.0, "dias_anio": 250, "config": "B",
        "perfil": "P1", "dias_refrigerado": 3, "dias_congelado": 14, "base_inventario": "dias_produccion",
        "automatizacion": "semi", "lineas": 1, "enfriamiento": "sin_definir",
        "tecnologia_efluentes": "sin_definir", "tecnologia_congelado": "sin_definir",
        "congelado_propio": True, "laboratorio_propio": True,
        "escala_objetivo": None, "reservar_rendering": True,
        "dotacion_turno": None, "aves_por_camion": None, "t_por_camion_despacho": None,
        "footprints": {}, "retiro_m": None, "buffer_m": None, "fos": None,
        "pisos_personal_admin": 1, "porterias": 2, "estricto": False,
    }


def v(nombre, i):
    return P[nombre]["v"][i]


# ---------------------------------------------------------------------------
# 2. INSUMOS DE 09A Y 09C
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _kg_config(config):
    kg, k = mc.kg_ave_config(config)
    return {c: x for c, (x, _) in kg.items()}, dict(k)


def kg_config(config):
    a, b = _kg_config(config)
    return dict(a), dict(b)          # copias: ningún escenario modifica la caché


def masas_utilities(config):
    """kg/ave en las claves de 09C (mu.MASAS) para la configuración pedida."""
    _, k = kg_config(config)
    mapa = {"peso_vivo": "peso_vivo", "agua_incorporada": "agua_incorporada", "comestible": "comestible",
            "comestible_bio": "comestible_bio", "agua_retenida_producto": "agua_retenida_comestible",
            "sangre_recuperada": "sangre", "sangre_drenada": "sangre_drenada", "plumas": "plumas",
            "visceras": "visceras", "cabeza": "cabeza", "garras": "garras", "menudencias": "menudencias",
            "rendering_potencial": "rendering_potencial", "solidos_a_retirar": "solidos_a_retirar",
            "masa_a_efluente_o_perdida": "efluente_o_perdida"}
    return {a: k[b] for a, b in mapa.items()}


def utilities(e, nivel):
    """Variables de 09C usadas aquí (mismos parámetros de inventario que el escenario)."""
    perfil = e["perfil"]
    sh = dict(PERFILES[perfil]) if isinstance(perfil, str) else dict(perfil)
    pid = perfil if isinstance(perfil, str) else "personalizado"
    p = mu.parametros(nivel, perfil=sh, perfil_id=pid, dias_refrigerado=e["dias_refrigerado"],
                      dias_congelado=e["dias_congelado"], base_inventario=e["base_inventario"],
                      horas_netas=min(e["horas_netas"], 20))
    r = mu.calcular(e["aves_dia"], dias_anio=e["dias_anio"], nivel=nivel, masas=masas_utilities(e["config"]), p=p)
    dbo = max(r["metodoA_carga_DBO5_kg_dia"], r["metodoB_carga_DBO5_kg_dia"])
    dqo = max(r["metodoA_carga_DQO_kg_dia"], r["metodoB_carga_DQO_kg_dia"])
    return {"stock_refrigerado_t": r["stock_refrigerado_t"],
            "stock_congelado_t": r["capacidad_almacenamiento_congelado_t"],
            "congelacion_t_dia": r["capacidad_congelacion_t_dia"],
            "agua_utilizada_m3_dia": r["agua_utilizada_m3_dia"],
            "agua_descargada_m3_dia": r["agua_descargada_m3_dia"],
            "caudal_max_m3_h": r["caudal_efluente_horario_maximo_ilustrativo_m3_h"],
            "dbo_kg_dia": dbo, "dqo_kg_dia": dqo,
            "comestible_t_dia": r["t_producto_comestible_dia_operativo"]}


# ---------------------------------------------------------------------------
# 3. VALIDACIÓN DE ENTRADAS
# ---------------------------------------------------------------------------
def validar(e):
    def num(x):
        return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)
    if not num(e["aves_dia"]) or e["aves_dia"] <= 0:
        raise ErrorSuperficies(f"aves/día inválido: {e['aves_dia']}")
    if not num(e["horas_netas"]) or not 0 < e["horas_netas"] <= 20:
        raise ErrorSuperficies("horas netas fuera de (0, 20]")
    if e["config"] not in ("A", "B", "C"):
        raise ErrorSuperficies("configuración debe ser A, B o C (balance v1.1)")
    pf = e["perfil"]
    if isinstance(pf, str):
        if pf not in PERFILES:
            raise ErrorSuperficies(f"perfil {pf} inexistente")
    else:
        if abs(sum(pf.values()) - 1) > 1e-9 or any(x < 0 for x in pf.values()):
            raise ErrorSuperficies("el perfil debe sumar 100 % sin negativos")
    for k in ("dias_refrigerado", "dias_congelado"):
        if not num(e[k]) or not 0 <= e[k] <= 365:
            raise ErrorSuperficies(f"{k} fuera de 0–365")
    if e["automatizacion"] not in AUTOMATIZACION:
        raise ErrorSuperficies(f"automatización: {AUTOMATIZACION}")
    if e["lineas"] not in (1, 2):
        raise ErrorSuperficies("líneas: 1 o 2")
    if e["enfriamiento"] not in ENFRIAMIENTOS:
        raise ErrorSuperficies(f"enfriamiento: {ENFRIAMIENTOS}")
    if e["tecnologia_efluentes"] not in TECNOLOGIAS + ("sin_definir",):
        raise ErrorSuperficies(f"tecnología de efluentes: {TECNOLOGIAS} o sin_definir")
    if e["tecnologia_congelado"] not in P["factor_tecnologia_congelado"]:
        raise ErrorSuperficies("tecnología de congelado inválida")
    obj = e["escala_objetivo"]
    if obj is not None and (not num(obj) or obj <= 0):
        raise ErrorSuperficies("escala objetivo inválida")
    for k in ("dotacion_turno", "aves_por_camion", "t_por_camion_despacho", "retiro_m", "buffer_m", "fos"):
        x = e[k]
        if x is not None and (not num(x) or x < 0 or (k in ("dotacion_turno", "aves_por_camion",
                                                                "t_por_camion_despacho", "fos") and x <= 0)):
            raise ErrorSuperficies(f"{k} inválido: {x}")
    if e["fos"] is not None and e["fos"] > 1:
        raise ErrorSuperficies("FOS es una fracción del terreno (0, 1]")
    for a, fp in (e["footprints"] or {}).items():
        if a not in EQUIPOS_POR_AREA:
            raise ErrorSuperficies(f"footprint para área desconocida: {a}")
        if fp is not None and (not num(fp) or fp <= 0):
            raise ErrorSuperficies(f"footprint de {a} = {fp}: una huella de equipos debe ser > 0 "
                                   "(desconocida = None, nunca 0)")
    if e["pisos_personal_admin"] not in (1, 2):
        raise ErrorSuperficies("pisos de personal/admin: 1 o 2")
    if e["porterias"] < 1:
        raise ErrorSuperficies("al menos una portería")
    # parámetros internos (protege contra factores negativos introducidos por edición)
    for n, d in P.items():
        if "v" in d and any((not math.isfinite(x)) or x < 0 for x in d["v"]):
            raise ErrorSuperficies(f"parámetro {n} negativo o no finito")


# ---------------------------------------------------------------------------
# 4. CÁLCULO
# ---------------------------------------------------------------------------
class Resultado:
    def __init__(self, entradas):
        self.e = entradas
        self.areas = {}          # id -> dict
        self.alertas = []        # (código, mensaje)
        self.ctx = {}

    def alerta(self, cod, msg):
        if "M05" in _MUT:
            return
        if (cod, msg) not in self.alertas:
            self.alertas.append((cod, msg))

    def add(self, aid, nombre, cat, zona, metodo, vals, estado, clasif, ref, nota="", cubierta=None):
        if aid in self.areas:
            raise ErrorSuperficies(f"área duplicada {aid}")
        if cubierta is None:
            cubierta = cat in CUBIERTAS
        self.areas[aid] = {"id": aid, "nombre": nombre, "categoria": cat, "zona": zona, "metodo": metodo,
                           "valores": dict(zip(NIVELES, vals)), "estado": estado, "clasificacion": clasif,
                           "referencia": ref, "nota": nota, "cubierta": cubierta,
                           "origen": ORIGEN_AREA.get(aid, "C")}

    def total(self, cats, nivel):
        xs = [a["valores"][nivel] for a in self.areas.values() if a["categoria"] in cats]
        if "M01" in _MUT:
            xs = xs[:-1]
        if any(x is None for x in xs):
            return None
        return sum(xs)


def _pot(k, x, beta=BETA):
    return k * (x / 1000.0) ** beta


def calcular(entradas=None, _con_reserva=True):
    """Superficies por área (rango), totales y terreno conceptual para un escenario."""
    e = entradas_por_defecto()
    e.update(copy.deepcopy(entradas or {}))
    if "M06" in _MUT and entradas is not None:
        entradas.setdefault("footprints", {})["colgado_aturdido"] = 1.0   # contamina la entrada del llamador
    validar(e)
    R = Resultado(e)
    E, h, L = e["aves_dia"], e["horas_netas"], e["lineas"]
    ritmo = E / h
    ritmo_linea = ritmo / L
    kgh, _ = kg_config(e["config"])
    fa = P["factor_automatizacion"][e["automatizacion"]]
    estricto = e["estricto"]
    U = {n: utilities(e, n) for n in NIVELES}
    turnos = 1 if h <= 10 else 2
    R.ctx = {"ritmo_aves_h": ritmo, "ritmo_por_linea_aves_h": ritmo_linea, "turnos": turnos,
             "utilities": U}
    if h > 10:
        R.alerta("HORAS_NETAS", f"{h:g} h netas: la superficie de línea baja porque cae el ritmo, pero la ecuación "
                                "de 24 h (09A) está en alerta; la planta no se achica sin validar limpieza y frío")

    # -------- helpers ----------------------------------------------------------------
    def proxy_equipos(aid, driver, nombre_k=None, extra=1.0, lineas=1):
        """Área dominada por equipos: footprint si existe; si no, proxy con alerta (o None si estricto)."""
        fp = (e["footprints"] or {}).get(aid)
        if fp is not None:
            vals = [fp * v("factor_envolvente_footprint", i) for i in range(3)]
            return vals, "FOOTPRINT", "[ESTIMACIÓN] huella × envolvente [SUPUESTO]"
        if "M02" in _MUT:
            return [0.0, 0.0, 0.0], "PROXY", ""
        R.alerta("FOOTPRINT_DESCONOCIDO", "huellas de equipos desconocidas (DPV-137): las áreas de equipos usan "
                                          "un PROXY de intensidad sin fuente")
        if estricto:
            return [None, None, None], "PENDIENTE", "[PENDIENTE DE VALIDACIÓN] footprint"
        k, mn = K[nombre_k or aid]
        vals = []
        for i in range(3):
            x = lineas * _pot(k["v"][i], driver) * extra
            if "M07" in _MUT and aid == "evisceracion_inspeccion":
                x = k["v"][i] * 1000.0 / max(driver, 1.0) * 50
            vals.append(max(mn["v"][i], x))
        return vals, "PROXY", "[SUPUESTO] proxy de intensidad"

    # ================================ PROCESO ==========================================
    # Recepción y andén de espera (bahías de camión)
    apc = e["aves_por_camion"]
    if apc is None:
        R.alerta("AVES_POR_CAMION", "aves por camión de vivo desconocidas (DPV-084): se usa PROXY 3.000–6.000")
    bahias = []
    for i in range(3):
        a = apc if apc is not None else v("aves_por_camion_proxy", i)
        bahias.append(math.ceil(ritmo * v("espera_h", i) / a) + 1)
    R.ctx["bahias_recepcion"] = bahias
    R.add("recepcion_espera", "Recepción, andén de espera ventilado y descarga", "proceso", "SUCIA",
          "bahías = ⌈ritmo × horas de espera ÷ aves por camión⌉ + 1; × m²/bahía",
          [bahias[i] * v("m2_bahia_recepcion", i) for i in range(3)],
          "PROXY" if apc is None else "ESTIMACION", "[ESTIMACIÓN] con [SUPUESTO]", "SUP-108; DPV-084")

    sep = [v("factor_separacion_dos_lineas", i) if L == 2 else 1.0 for i in range(3)]
    for aid, nombre, zona, extra in (
            ("colgado_aturdido", "Colgado y aturdido", "SUCIA", 1.0),
            ("sangrado_escaldado_desplumado", "Sangrado, escaldado, desplumado, patas y cabeza", "SUCIA", 1.0),
            ("evisceracion_inspeccion", "Evisceración, inspección oficial post mortem, menudencias en línea",
             "TRANSICION", fa)):
        vals, est, cl = proxy_equipos(aid, ritmo_linea, extra=extra, lineas=L)
        vals = [None if x is None else x * sep[i] for i, x in enumerate(vals)]
        R.add(aid, nombre, "proceso", zona, "k × (ritmo por línea/1.000)^β × líneas (proxy) o huella × envolvente",
              vals, est, cl, "SUP-107; SUP-109; DPV-137; DPV-090")

    # Enfriamiento (residencias de 09A)
    res = mc.RESIDENCIA_MIN
    metodo_enf = e["enfriamiento"]
    if metodo_enf == "sin_definir":
        R.alerta("ENFRIAMIENTO_NO_DEFINIDO", "método de enfriamiento sin decidir (DEC-026): se reserva la superficie "
                                             "MAYOR entre inmersión y aire")
    fp = (e["footprints"] or {}).get("enfriamiento")
    if fp is not None:
        vals = [fp * v("factor_envolvente_footprint", i) for i in range(3)]
        est, cl = "FOOTPRINT", "[ESTIMACIÓN] huella × envolvente"
    elif estricto:
        vals, est, cl = [None] * 3, "PENDIENTE", "[PENDIENTE DE VALIDACIÓN]"
        R.alerta("FOOTPRINT_DESCONOCIDO", "huellas de equipos desconocidas (DPV-137): las áreas de equipos usan "
                                          "un PROXY de intensidad sin fuente")
    else:
        vals = []
        t_aire = (res["aire_min"], (res["aire_min"] + res["aire_max"]) / 2, res["aire_max"])
        for i in range(3):
            inm = ritmo / 60 * res["inmersion"] * v("m2_carcasa_inmersion", i)
            aire = ritmo / 60 * t_aire[i] * v("m2_carcasa_aire", i)
            x = {"inmersion": inm, "aire": aire, "sin_definir": max(inm, aire)}[metodo_enf]
            vals.append(max(v("min_enfriamiento", i), x * sep[i]))
        est, cl = "ESTIMACION", "[ESTIMACIÓN] carcasas simultáneas (09A) × m²/carcasa [SUPUESTO]"
    R.add("enfriamiento", "Enfriamiento (inmersión, aire o mixto) y escurrido", "proceso", "LIMPIA",
          "carcasas simultáneas = ritmo × residencia (09A) × m²/carcasa", vals, est, cl, "SUP-110; DEC-026")

    vals, est, cl = proxy_equipos("clasificacion", ritmo)
    R.add("clasificacion", "Clasificación por peso y calidad", "proceso", "LIMPIA", "k × (ritmo/1.000)^β", vals,
          est, cl, "SUP-107")

    for aid, nombre, kg_key, req in (("trozado", "Trozado (incluye sala mínima en config. A)", "a_trozado", "ABC"),
                                     ("deshuese", "Deshuese, fileteado y trimming", "a_deshuese", "C"),
                                     ("cms", "Sala de CMS (carne separada mecánicamente)", "a_cms", "C")):
        kg_h = kgh[kg_key] * ritmo
        if kg_h <= 0 or e["config"] not in req:
            R.add(aid, nombre, "proceso", "LIMPIA", "no existe en esta configuración", [0.0, 0.0, 0.0], "NO_APLICA",
                  "[NO APLICA]", "DEC-005; DEC-029", f"config. {e['config']} sin {aid}")
            continue
        vals, est, cl = proxy_equipos(aid, kg_h, extra=fa if aid != "cms" else 1.0)
        R.add(aid, nombre, "proceso", "LIMPIA", "k × (kg/h que entran a la sala/1.000)^β (kg/h de 09A)", vals, est,
              cl, "SUP-107; DPV-137")

    vals, est, cl = proxy_equipos("coproductos", (kgh["garras_a_y_segunda"] + kgh["menudencias_y_cuello"]) * ritmo)
    R.add("coproductos", "Coproductos comestibles: garras y menudencias", "proceso", "LIMPIA",
          "k × (kg/h garras + menudencias/1.000)^β", vals, est, cl, "SUP-107; DEC-031")
    vals, est, cl = proxy_equipos("empaque", kgh["comestible_a_empaque"] * ritmo, extra=fa)
    R.add("empaque", "Envasado primario, control, encajonado y paletizado", "proceso", "LIMPIA",
          "k × (kg/h comestible/1.000)^β", vals, est, cl, "SUP-107")
    vals, est, cl = proxy_equipos("lavado_cajones", ritmo)
    R.add("lavado_cajones", "Lavado de cajones/módulos de aves vivas", "proceso", "SUCIA", "k × (ritmo/1.000)^β",
          vals, est, cl, "SUP-107")

    sub_proc = [R.total(("proceso",), n) for n in NIVELES]
    R.add("circulacion_proceso", "Circulación interna de proceso, esclusas y barreras sanitarias", "proceso",
          "TRANSVERSAL", "fracción de las salas de proceso",
          [None if s is None else s * v("f_circulacion_proceso", i) for i, s in enumerate(sub_proc)],
          "ESTIMACION" if None not in sub_proc else "PENDIENTE", "[SUPUESTO]", "SUP-111")

    # ================================ FRÍO ==============================================
    com_t = [U[n]["comestible_t_dia"] for n in NIVELES]
    st_r = [U[n]["stock_refrigerado_t"] for n in NIVELES]
    st_c = [U[n]["stock_congelado_t"] for n in NIVELES]
    if "M03" in _MUT:
        st_c = [U[n]["congelacion_t_dia"] * 14 for n in NIVELES]
    cg = [U[n]["congelacion_t_dia"] for n in NIVELES]
    camr = [max(v("min_camara_refrigerada", i), st_r[i] * v("factor_pico_stock", i) / v("densidad_refrigerado_t_m2", i))
            if st_r[i] > 0 else 0.0 for i in range(3)]
    camc = [max(v("min_camara_congelada", i), st_c[i] * v("factor_pico_stock", i) / v("densidad_congelado_t_m2", i))
            if st_c[i] > 0 else 0.0 for i in range(3)]
    R.add("camaras_refrigeradas", "Cámaras de producto refrigerado", "frio", "FRIA",
          "stock refrigerado (09C) × pico ÷ densidad de estiba", camr, "ESTIMACION" if st_r[1] > 0 else "NO_APLICA",
          "[ESTIMACIÓN] t de 09C; densidad [PVDP]/[SUPUESTO]", "SUP-055; SUP-056; SUP-112; FTE-293")
    R.add("camaras_congeladas", "Cámaras de producto congelado (incluye lotes de exportación)", "frio", "FRIA",
          "stock congelado (09C) × pico ÷ densidad de estiba", camc, "ESTIMACION" if st_c[1] > 0 else "NO_APLICA",
          "[ESTIMACIÓN] t de 09C; densidad [PVDP]", "SUP-055; SUP-056; SUP-112; FTE-292")
    ftec = P["factor_tecnologia_congelado"][e["tecnologia_congelado"]]
    if not e["congelado_propio"]:
        R.add("tunel_congelado", "Congelado (túnel/espiral/placas)", "frio", "FRIA", "tercerizado", [0.0] * 3,
              "NO_APLICA", "[NO APLICA]", "DEC-064", "congelado de terceros (decisión del usuario)")
        R.alerta("CONGELADO_TERCERIZADO", "congelado tercerizado: no se reserva túnel; prever espacio si se internaliza")
    elif cg[1] <= 0:
        R.add("tunel_congelado", "Congelado (túnel/espiral/placas)", "frio", "FRIA", "sin congelado en el perfil",
              [0.0] * 3, "NO_APLICA", "[NO APLICA]", "SUP-055")
    else:
        fp = (e["footprints"] or {}).get("tunel_congelado")
        if fp is not None:
            vals, est = [fp * v("factor_envolvente_footprint", i) for i in range(3)], "FOOTPRINT"
        elif estricto:
            vals, est = [None] * 3, "PENDIENTE"
            R.alerta("FOOTPRINT_DESCONOCIDO", "huellas de equipos desconocidas (DPV-137): las áreas de equipos "
                                              "usan un PROXY de intensidad sin fuente")
        else:
            vals = [max(v("min_tunel", i), cg[i] * v("m2_tunel_por_t_dia", i) * ftec) for i in range(3)]
            est = "PROXY"
            R.alerta("FOOTPRINT_DESCONOCIDO", "huellas de equipos desconocidas (DPV-137): las áreas de equipos "
                                              "usan un PROXY de intensidad sin fuente")
        R.add("tunel_congelado", "Congelado (túnel/espiral/placas)", "frio", "FRIA",
              "capacidad de congelación t/día (09C) × m²/(t/día)", vals, est, "[SUPUESTO] proxy",
              "SUP-112; DPV-137; FTE-215")
    R.add("antecamaras_preparacion", "Antecámaras, pasillo frío y preparación de pedidos", "frio", "FRIA",
          "fracción de cámaras", [(camr[i] + camc[i]) * v("f_antecamara", i) for i in range(3)], "ESTIMACION",
          "[SUPUESTO]", "SUP-112")
    tpc = e["t_por_camion_despacho"]
    if tpc is None:
        R.alerta("T_POR_CAMION", "t por camión de despacho desconocidas (DPV-084, DPV-036): se usa PROXY 5–12 t")
    docks = []
    for i in range(3):
        t = tpc if tpc is not None else v("t_por_camion_proxy", i)
        docks.append(max(1, math.ceil(com_t[i] * v("factor_pico_despacho", i) / (t * v("cargas_por_dock_dia", i)))))
    R.ctx["docks_expedicion"] = docks
    R.add("expedicion_docks", "Expedición: andenes refrigerados con sello", "frio", "DESPACHO",
          "docks = ⌈t/día × pico ÷ (t por camión × cargas por dock)⌉ × m²/dock",
          [docks[i] * v("m2_dock_interior", i) for i in range(3)], "PROXY" if tpc is None else "ESTIMACION",
          "[ESTIMACIÓN] con [SUPUESTO]", "SUP-113; DPV-036; DPV-084")
    _, kfull = kg_config(e["config"])
    sp_t = kfull["c_perecedero_sin_plumas"] * E / 1000
    R.add("camara_subproductos", "Cámara de subproductos perecederos (separada del producto)", "frio", "SUBPRODUCTOS",
          "t/día de C perecederos sin plumas × días ÷ densidad",
          [max(v("min_camara_subproductos", i), sp_t * v("dias_subproductos_refrigerados", i) /
               v("densidad_subproductos_t_m2", i)) for i in range(3)], "ESTIMACION", "[SUPUESTO]",
          "SUP-056; SUP-114; DEC-027")
    R.add("camara_decomisos", "Sala/cámara de decomisos bajo control oficial", "frio", "SUBPRODUCTOS",
          "superficie mínima", [v("m2_decomisos", i) for i in range(3)], "ESTIMACION", "[SUPUESTO]",
          "SUP-114; DPV-090")

    # ================================ SERVICIOS =========================================
    sol_t = kfull["solidos_a_retirar"] * E / 1000
    fp = (e["footprints"] or {}).get("sala_subproductos")
    if fp is not None:
        vals, est = [fp * v("factor_envolvente_footprint", i) for i in range(3)], "FOOTPRINT"
    else:
        vals = [max(v("min_sala_subproductos", i), sol_t * v("m2_sala_subproductos_por_t_dia", i)) for i in range(3)]
        est = "ESTIMACION"
    R.add("sala_subproductos", "Subproductos no comestibles: sangre, plumas, vísceras, cabezas (tanques, tolvas, "
          "contenedores, báscula)", "servicios", "SUBPRODUCTOS", "t/día de sólidos a retirar (09A) × m²/(t/día)",
          vals, est, "[SUPUESTO]", "SUP-114; DEC-027; DEC-044")
    k, mn = K["residuos_carton"]
    R.add("residuos_carton", "Residuos, cartón y compactación", "servicios", "SUBPRODUCTOS", "k × (ritmo/1.000)^β",
          [max(mn["v"][i], _pot(k["v"][i], ritmo)) for i in range(3)], "ESTIMACION", "[SUPUESTO]", "SUP-115")
    envases = [max(v("min_envases", i), com_t[i] * v("m2_envases_por_t_dia", i)) for i in range(3)]
    R.add("deposito_envases", "Depósito de envases, cartón e insumos secos (fuera de salas de proceso)", "servicios",
          "LIMPIA_APOYO", "t/día de comestible × m²/(t/día)", envases, "ESTIMACION", "[SUPUESTO]", "SUP-111")
    frio_camaras = [camr[i] + camc[i] + (R.areas["tunel_congelado"]["valores"][NIVELES[i]] or 0) for i in range(3)]
    fp = (e["footprints"] or {}).get("sala_maquinas_frio")
    if fp is not None:
        vals, est = [fp * v("factor_envolvente_footprint", i) for i in range(3)], "FOOTPRINT"
    elif estricto:
        vals, est = [None] * 3, "PENDIENTE"
    else:
        vals = [max(v("min_sala_maquinas_frio", i), frio_camaras[i] * v("f_sala_maquinas_frio", i)) for i in range(3)]
        est = "PROXY"
        R.alerta("CARGA_FRIGORIFICA_PENDIENTE", "sala de máquinas de frío por proxy: la carga frigorífica total sigue "
                                                "PENDIENTE en 09C (DPV-109)")
    R.add("sala_maquinas_frio", "Sala de máquinas de frío (compresores, condensadores)", "servicios", "UTILITIES",
          "fracción de m² de frío (proxy)", vals, est, "[SUPUESTO] proxy", "SUP-115; DPV-109; DEC-046")
    for aid, nombre, ref in (("caldera_agua_caliente", "Caldera / agua caliente / vapor", "SUP-115; DEC-045"),
                             ("aire_comprimido", "Compresores de aire comprimido", "SUP-115"),
                             ("generador", "Grupo electrógeno de respaldo", "SUP-115; DEC-047")):
        vals, est, cl = proxy_equipos(aid, ritmo)
        R.add(aid, nombre, "servicios", "UTILITIES", "k × (ritmo/1.000)^β (proxy) o huella", vals, est, cl, ref)
    R.alerta("GENERADOR_PENDIENTE", "grupo electrógeno PENDIENTE en 09C (lista de cargas críticas): su área es proxy")
    k, mn = K["sala_electrica"]
    R.add("sala_electrica", "Sala eléctrica, tableros y transformador", "servicios", "UTILITIES",
          "k × (ritmo/1.000)^β (potencia pico PENDIENTE en 09C)",
          [max(mn["v"][i], _pot(k["v"][i], ritmo)) for i in range(3)], "PROXY", "[SUPUESTO] proxy",
          "SUP-115; DPV-095")
    agua = [U[n]["agua_utilizada_m3_dia"] for n in NIVELES]
    R.add("tratamiento_agua", "Tratamiento de agua potable (cloración, filtros, bombeo)", "servicios", "UTILITIES",
          "m³/día (09C) × m²/(m³/día)", [max(v("min_tratamiento_agua", i), agua[i] *
                                             v("m2_tratamiento_agua_por_m3_dia", i)) for i in range(3)],
          "ESTIMACION", "[SUPUESTO]", "SUP-115; DPV-053")
    for aid, nombre, zona in (("mantenimiento_taller", "Mantenimiento y taller", "UTILITIES"),
                              ("repuestos", "Pañol de repuestos", "UTILITIES"),
                              ("quimicos", "Depósito de químicos (bajo llave)", "UTILITIES")):
        k, mn = K[aid]
        R.add(aid, nombre, "servicios", zona, "k × (ritmo/1.000)^β",
              [max(mn["v"][i], _pot(k["v"][i], ritmo)) for i in range(3)], "ESTIMACION", "[SUPUESTO]", "SUP-115")
    k, mn = K["laboratorio_calidad"]
    if e["laboratorio_propio"]:
        R.add("laboratorio_calidad", "Laboratorio de autocontrol / calidad", "servicios", "ADMINISTRATIVA",
              "k × (ritmo/1.000)^β", [max(mn["v"][i], _pot(k["v"][i], ritmo)) for i in range(3)], "ESTIMACION",
              "[SUPUESTO]", "SUP-115; DEC-065")
    else:
        R.add("laboratorio_calidad", "Sala de toma de muestras (laboratorio tercerizado)", "servicios", "ADMINISTRATIVA",
              "superficie mínima", [mn["v"][i] for i in range(3)], "ESTIMACION", "[SUPUESTO]", "DEC-065")

    # ================================ PERSONAL / ADMIN ===================================
    dot_in = e["dotacion_turno"]
    if dot_in is None:
        R.alerta("DOTACION_PROXY", "dotación por turno desconocida (18_recursos_humanos no iniciado; DPV-138): "
                                   "se usa PROXY lineal en el ritmo")
    fda = P["factor_dotacion_automatizacion"][e["automatizacion"]]
    fdc = P["factor_dotacion_config"][e["config"]]
    dot = []
    for i in range(3):
        if dot_in is not None:
            dot.append(float(dot_in))
        elif estricto:
            dot.append(None)
        else:
            dot.append(v("dotacion_base_proxy", i) + v("dotacion_por_ave_h_proxy", i) * ritmo * fda * fdc)
    R.ctx["dotacion_turno"] = dot
    if None in dot:
        vest = comedor = lav = [None] * 3
        est_p = "PENDIENTE"
    else:
        vest = [max(v("min_vestuarios", i), dot[i] * v("m2_vestuario_por_persona", i) *
                    (1 + v("factor_vestuario_segundo_turno", i) * (turnos - 1))) for i in range(3)]
        comedor = [max(v("min_comedor", i), dot[i] * v("fraccion_comedor_simultaneo", i) * v("m2_comensal", i) * 1.15)
                   for i in range(3)]
        lav = [max(10.0, dot[i] * turnos * v("m2_lavanderia_por_persona", i)) for i in range(3)]
        est_p = "PROXY" if dot_in is None else "ESTIMACION"
    R.add("vestuarios", "Vestuarios y sanitarios separados por zona (sucia / limpia) y por sexo", "personal_admin",
          "PERSONAL", "personas por turno × m²/persona (+ lockers del 2.º turno)", vest, est_p, "[SUPUESTO]",
          "SUP-116; DPV-138; DPV-090")
    R.add("comedor", "Comedor y office", "personal_admin", "PERSONAL", "personas simultáneas × m²/comensal",
          comedor, est_p, "[SUPUESTO]", "SUP-116")
    R.add("lavanderia", "Lavandería / ropería de indumentaria por color de zona", "servicios", "PERSONAL",
          "personas × m²/persona", lav, est_p, "[SUPUESTO]", "SUP-115")
    R.add("oficinas", "Oficinas de administración", "personal_admin", "ADMINISTRATIVA", "puestos × m²/puesto",
          [max(v("min_oficinas", i), v("admin_puestos", i) * v("m2_puesto_oficina", i) * (1 + 0.01 * ritmo / 100))
           for i in range(3)], "ESTIMACION", "[SUPUESTO]", "SUP-116")
    for aid, nombre, zona, ref in (
            ("oficina_senasa", "Oficina del servicio de inspección oficial (SENASA) con sanitario propio",
             "ADMINISTRATIVA", "DPV-090; DPV-140"),
            ("enfermeria_capacitacion", "Enfermería, sala de capacitación", "PERSONAL", "SUP-116")):
        k, mn = K[aid]
        R.add(aid, nombre, "personal_admin", zona, "superficie base (crece con el ritmo)",
              [max(mn["v"][i], _pot(k["v"][i], ritmo, 0.5)) for i in range(3)], "ESTIMACION", "[SUPUESTO]", ref)
    R.add("porterias_seguridad", "Porterías y seguridad (accesos separados)", "personal_admin", "ADMINISTRATIVA",
          "porterías × m²", [e["porterias"] * v("m2_porteria", i) for i in range(3)], "ESTIMACION", "[SUPUESTO]",
          "SUP-116")
    sub_p = [R.total(("personal_admin",), n) for n in NIVELES]
    R.add("circulacion_personal", "Circulación de personal y filtros sanitarios", "personal_admin", "PERSONAL",
          "fracción de personal/admin", [None if s is None else s * v("f_circulacion_personal", i)
                                         for i, s in enumerate(sub_p)],
          "ESTIMACION" if None not in sub_p else "PENDIENTE", "[SUPUESTO]", "SUP-116")

    # ================================ EXTERIORES =========================================
    camiones_dia = [E / (apc if apc is not None else v("aves_por_camion_proxy", i)) for i in range(3)]
    R.ctx["camiones_aves_dia"] = camiones_dia
    R.add("playa_aves_vivas", "Playa de camiones de aves vivas (espera exterior y maniobra)", "exteriores", "SUCIA",
          "camiones simultáneos (= bahías) × m²/camión", [bahias[i] * v("m2_camion_playa", i) for i in range(3)],
          "PROXY" if apc is None else "ESTIMACION", "[SUPUESTO]", "SUP-117; DPV-084")
    R.add("lavado_camiones", "Lavado y desinfección de camiones de vivo", "exteriores", "SUCIA",
          "plataformas = ⌈camiones/día ÷ camiones por plataforma⌉",
          [max(1, math.ceil(camiones_dia[i] / v("camiones_por_plataforma_lavado", i))) * v("m2_lavado_camion", i)
           for i in range(3)], "ESTIMACION", "[SUPUESTO]", "SUP-117")
    R.add("playa_despacho", "Playa de maniobra de despacho (frente a docks)", "exteriores", "DESPACHO",
          "docks × m² de maniobra", [docks[i] * v("m2_playa_por_dock", i) for i in range(3)],
          "PROXY" if tpc is None else "ESTIMACION", "[SUPUESTO]", "SUP-113; DPV-036")
    R.add("playa_subproductos", "Playa de contenedores y retiro de subproductos", "exteriores", "SUBPRODUCTOS",
          "base + t/día × m²", [v("m2_playa_subproductos_base", i) + sol_t * v("m2_playa_subproductos_por_t_dia", i)
                                for i in range(3)], "ESTIMACION", "[SUPUESTO]", "SUP-117")
    if None in dot:
        estac = [None] * 3
    else:
        estac = [(dot[i] * (1 + 0.5 * (turnos - 1)) * v("fraccion_personal_motorizado", i) + v("plazas_visitas", i))
                 * v("m2_plaza_auto", i) for i in range(3)]
    R.add("estacionamiento", "Estacionamiento de personal y visitas", "exteriores", "PERSONAL",
          "personas × fracción motorizada × m²/plaza", estac, est_p, "[SUPUESTO]", "SUP-117; DPV-139")
    tanques = [agua[i] * v("dias_reserva_agua", i) / v("altura_tanque_m", i) * 1.3 for i in range(3)]
    R.add("tanques_agua", "Tanques de reserva de agua (incluye incendio a definir)", "exteriores", "UTILITIES",
          "m³/día × días ÷ altura × 1,3", tanques, "ESTIMACION", "[SUPUESTO]", "SUP-115; DPV-053; DPV-106")
    huella_parcial = []
    for n in NIVELES:
        cub = R.total(CUBIERTAS, n)
        huella_parcial.append(cub)
    R.add("circulacion_pesada", "Circulación pesada interna (vivo / producto / subproductos separados)", "exteriores",
          "EXTERIOR", "fracción de la superficie cubierta",
          [None if c is None else c * v("f_circulacion_pesada", i) for i, c in enumerate(huella_parcial)],
          "ESTIMACION" if None not in huella_parcial else "PENDIENTE", "[SUPUESTO]", "SUP-117")

    # ================================ EFLUENTES =========================================
    tec = e["tecnologia_efluentes"]
    efl = areas_efluentes(U, tec)
    if tec == "sin_definir":
        R.alerta("TECNOLOGIA_EFLUENTES_NO_DEFINIDA", "tren de tratamiento sin decidir (DEC-043): el total usa la "
                                                     "reserva de 'anaerobio_aerobio'; ver lagunas y cloaca por separado")
    if tec in ("cloaca", "sin_definir"):
        R.alerta("CLOACA_DEPENDE_DEL_SITIO", "vuelco a colectora solo si el prestador lo acepta (DPV-106); no se supone")
    if tec == "lagunas":
        R.alerta("LAGUNAS_DISTANCIA", "lagunas: la distancia a viviendas y el olor pueden exigir un buffer mayor que el "
                                      "proxy (DPV-087, DPV-106)")
    R.alerta("LODOS_PENDIENTE", "lodos PENDIENTES de dimensionamiento en 09C: su área es proxy (DPV-114)")
    for aid, (nombre, vals, est, ref) in efl.items():
        R.add(aid, nombre, "efluentes", "UTILITIES", "ver areas_efluentes()", vals, est, "[SUPUESTO] / [PVDP]", ref,
              cubierta=False)
    R.ctx["efluentes_por_tecnologia"] = {t: [sum(x[1][i] for x in areas_efluentes(U, t).values()) for i in range(3)]
                                        for t in TECNOLOGIAS}

    # ================================ TOTALES, RESERVA, TERRENO ==========================
    tot = totales(R)
    if _con_reserva:
        reserva(R, tot)
    terreno(R)
    contraste_benchmark(R)
    return R


def areas_efluentes(U, tec):
    """Áreas de efluentes por tecnología (NO se elige ninguna). Devuelve {id: (nombre, [b, m, a], estado, ref)}."""
    t_ref = "anaerobio_aerobio" if tec == "sin_definir" else tec
    out = {}
    q = [U[n]["agua_descargada_m3_dia"] for n in NIVELES]
    qh = [U[n]["caudal_max_m3_h"] for n in NIVELES]
    dbo = [U[n]["dbo_kg_dia"] for n in NIVELES]
    dqo = [U[n]["dqo_kg_dia"] for n in NIVELES]
    out["efl_pretratamiento"] = ("Pretratamiento: rejas, tamiz, desengrasador, bombeo",
                                 [max(v("min_pretratamiento", i), qh[i] * v("m2_pretrat_por_m3_h", i))
                                  for i in range(3)], "ESTIMACION", "SUP-118")
    out["efl_ecualizacion"] = ("Ecualización", [q[i] * v("fraccion_ecualizacion", i) / v("prof_ecualizacion_m", i) * 1.3
                                                for i in range(3)], "ESTIMACION", "SUP-118")
    out["efl_daf"] = ("DAF (flotación por aire disuelto) y química",
                      [max(v("min_daf", i), qh[i] / v("carga_superficial_daf_m3_m2_h", i) * v("factor_huella_daf", i))
                       for i in range(3)], "ESTIMACION", "SUP-118; FTE-294")
    dbo_in = [dbo[i] * (1 - v("remocion_dbo_daf", i)) for i in range(3)]
    dqo_in = [dqo[i] * (1 - v("remocion_dqo_daf", i)) for i in range(3)]

    def aerobio(i, carga_dbo):
        return carga_dbo / v("carga_vol_aerobia_kg_dbo_m3_d", i) / v("prof_aerobio_m", i) * v("factor_huella_aerobio", i)

    if t_ref == "cloaca":
        bio, est = [0.0] * 3, "NO_APLICA"
    elif t_ref == "aerobio_compacto":
        bio, est = [aerobio(i, dbo_in[i]) for i in range(3)], "ESTIMACION"
    elif t_ref == "anaerobio_aerobio":
        bio = [dqo_in[i] / v("carga_vol_anaerobia_kg_dqo_m3_d", i) / v("prof_reactor_anaerobio_m", i)
               * v("factor_huella_anaerobio", i) + aerobio(i, dbo_in[i] * v("fraccion_dbo_a_pulido", i))
               for i in range(3)]
        est = "ESTIMACION"
    else:  # lagunas
        bio = [(dbo_in[i] / v("carga_vol_laguna_anaerobia_kg_dbo_m3_d", i) / v("prof_laguna_anaerobia_m", i)
                + dbo_in[i] * v("fraccion_dbo_a_laguna_facultativa", i)
                / (v("carga_sup_laguna_facultativa_kg_dbo_ha_d", i) / 10000.0)) * v("factor_taludes_lagunas", i)
               for i in range(3)]
        est = "ESTIMACION"
    if t_ref != "cloaca":
        bio = [max(v("min_biologico", i), bio[i]) for i in range(3)]
    out["efl_biologico"] = (f"Tratamiento biológico ({t_ref})", bio, est,
                            "SUP-118; FTE-294; FTE-263; DEC-043")
    lod = [0.0] * 3 if t_ref == "cloaca" else [max(v("min_lodos", i), dbo_in[i] * v("m2_lodos_por_kg_dbo_d", i))
                                               for i in range(3)]
    out["efl_lodos"] = ("Manejo de lodos y flotados (espesado, deshidratación, acopio)", lod,
                        "NO_APLICA" if t_ref == "cloaca" else "PROXY", "SUP-118; DPV-114; DEC-027")
    s = [sum(x[1][i] for x in out.values()) for i in range(3)]
    out["efl_circulacion"] = ("Circulación, laboratorio y operación de efluentes",
                              [s[i] * v("f_circulacion_efluentes", i) for i in range(3)], "ESTIMACION", "SUP-118")
    return out


def totales(R):
    t = {}
    for n in NIVELES:
        d = {c: R.total((c,), n) for c in CATEGORIAS}
        cub = None if any(d[c] is None for c in CUBIERTAS) else sum(d[c] for c in CUBIERTAS)
        oper = None if cub is None or d["exteriores"] is None or d["efluentes"] is None else \
            cub + d["exteriores"] + d["efluentes"]
        d["construido"] = cub
        d["operativo"] = oper
        t[n] = d
    R.totales = t
    return t


def reserva(R, tot):
    e = R.e
    obj = e["escala_objetivo"]
    res = {n: {} for n in NIVELES}
    if obj is not None and obj > e["aves_dia"] and "M04" not in _MUT:
        e2 = dict(e)
        e2["aves_dia"] = obj
        e2["escala_objetivo"] = None
        R2 = calcular(e2, _con_reserva=False)
        for n in NIVELES:
            for c in CATEGORIAS:
                a, b = tot[n][c], R2.totales[n][c]
                res[n][c] = None if a is None or b is None else max(0.0, b - a)
        R.ctx["escala_objetivo_totales"] = R2.totales
    elif obj is not None and obj <= e["aves_dia"]:
        for n in NIVELES:
            res[n] = {c: 0.0 for c in CATEGORIAS}
    else:
        R.alerta("OBJETIVO_EXPANSION_NO_DEFINIDO", "sin escala objetivo: la reserva es una FRACCIÓN [SUPUESTO] de lo "
                                                   "operativo (SUP-119)")
        for i, n in enumerate(NIVELES):
            op = tot[n]["operativo"]
            res[n] = {"sin_objetivo": None if op is None else op * v("fraccion_reserva_sin_objetivo", i)}
    _, k = kg_config(e["config"])
    rend_t = k["rendering_potencial"] * max(e["aves_dia"], obj or 0) / 1000
    for i, n in enumerate(NIVELES):
        res[n]["rendering"] = (max(v("min_rendering", i), rend_t * v("m2_rendering_por_t_dia", i))
                               if e["reservar_rendering"] else 0.0)
        xs = list(res[n].values())
        res[n]["total"] = None if any(x is None for x in xs) else sum(xs)
    if e["reservar_rendering"]:
        R.alerta("RENDERING_RESERVA", "se reserva terreno para un rendering futuro (DEC-027, SUP-049): no se construye")
    R.reserva = res
    for i, n in enumerate(NIVELES):
        tot[n]["reserva"] = res[n]["total"]
    R.add("reserva_expansion", "Reserva de terreno para expansión (incluye rendering futuro si se pide)", "reserva",
          "RESERVA", "Σ max(0, área objetivo − área actual) + rendering", [res[n]["total"] for n in NIVELES],
          "ESTIMACION" if obj is not None else "PROXY", "[ESTIMACIÓN] / [SUPUESTO]", "SUP-119; DEC-035",
          cubierta=False)


def terreno(R):
    e = R.e
    if e["retiro_m"] is None:
        R.alerta("RETIRO_PENDIENTE", "retiros municipales desconocidos (DPV-106): se usan 5 / 10 / 15 m [SUPUESTO]")
    if e["buffer_m"] is None:
        R.alerta("BUFFER_PROXY", "franja de bioseguridad/vecindad desconocida (DPV-087): PROXY 10 / 20 / 40 m")
    if e["fos"] is None:
        R.alerta("FOS_PENDIENTE", "factor de ocupación del suelo (FOS) desconocido: no se verifica (DPV-106)")
    R.terreno = {}
    for i, n in enumerate(NIVELES):
        t = R.totales[n]
        if t["operativo"] is None or t.get("reserva") is None:
            R.terreno[n] = None
            continue
        cub = t["construido"]
        pa = t["personal_admin"]
        huella = cub - pa + pa / e["pisos_personal_admin"]
        a_int = huella + t["exteriores"] + t["efluentes"] + t["reserva"]
        ar = v("relacion_largo_ancho", i)
        ancho = math.sqrt(a_int / ar)
        largo = ar * ancho
        m = (e["retiro_m"] if e["retiro_m"] is not None else v("retiro_m", i)) + \
            (e["buffer_m"] if e["buffer_m"] is not None else v("buffer_proxy_m", i))
        bruto = (largo + 2 * m) * (ancho + 2 * m)
        fos_min = huella / e["fos"] if e["fos"] else 0.0
        if fos_min > bruto:
            R.alerta("FOS_LIMITA", f"el FOS exige más terreno que la suma de áreas (nivel {n})")
        total = max(bruto, fos_min)
        R.terreno[n] = {"huella_edificios": huella, "area_interna": a_int, "retiros_buffers": total - a_int,
                        "margen_perimetral_m": m, "terreno_total": total, "terreno_ha": total / 10000,
                        "ocupacion_huella_pct": 100 * huella / total}


# Benchmarks argentinos de superficie cubierta [PVDP]: extractos de prensa / INTI, nunca leídos en original.
BENCHMARKS = [
    {"planta": "Frigorífico MARK (Buenos Aires)", "aves_dia": (70000, 80000), "m2_cubiertos": (12000, 15000),
     "fuente": "FTE-224"},
    {"planta": "Avex (Río Cuarto, Córdoba)", "aves_dia": (120000, 120000), "m2_cubiertos": (13000, 13000),
     "fuente": "FTE-290"},
    {"planta": "Sala de faena municipal China Muerta (Neuquén)", "aves_dia": (1000, 1000), "m2_cubiertos": (181, 181),
     "fuente": "FTE-291"},
    {"planta": "Sala de faena municipal Ayacucho (Buenos Aires, en obra)", "aves_dia": (200, 300),
     "m2_cubiertos": (290, 290), "fuente": "FTE-296"},
]


def contraste_benchmark(R):
    """m² cubiertos por ave/día vs referencias [PVDP]. Es un CONTRASTE de orden de magnitud, no una calibración."""
    E = R.e["aves_dia"]
    ratios = [None if R.totales[n]["construido"] is None else R.totales[n]["construido"] / E for n in NIVELES]
    R.ctx["m2_cubiertos_por_ave_dia"] = ratios
    lo = min(b["m2_cubiertos"][0] / b["aves_dia"][1] for b in BENCHMARKS)
    hi = max(b["m2_cubiertos"][1] / b["aves_dia"][0] for b in BENCHMARKS)
    if ratios[1] is not None and not lo <= ratios[1] <= hi:
        R.alerta("CONTRASTE_BENCHMARK", f"m² cubiertos/(ave/día) medio = {ratios[1]:.2f} fuera de la banda de "
                                        f"referencias [PVDP] {lo:.2f}–{hi:.2f}")


# ---------------------------------------------------------------------------
# 5. SALIDA PARA LA FUTURA INTERFAZ HTML (no se modifica el HTML desde esta sesión)
# ---------------------------------------------------------------------------
def salida_interfaz(R):
    """Variables que el simulador HTML debería recibir (ver conclusiones_layout.md §8)."""
    def tr(x):
        return {n: x[n] for n in NIVELES}
    return {
        "m2_construidos": tr({n: R.totales[n]["construido"] for n in NIVELES}),
        "m2_operativos": tr({n: R.totales[n]["operativo"] for n in NIVELES}),
        "m2_terreno": tr({n: None if R.terreno[n] is None else R.terreno[n]["terreno_total"] for n in NIVELES}),
        "m2_por_categoria": {c: tr({n: R.totales[n][c] for n in NIVELES}) for c in CATEGORIAS},
        "m2_reserva_expansion": tr({n: R.totales[n].get("reserva") for n in NIVELES}),
        "camaras": {a: tr(R.areas[a]["valores"]) for a in ("camaras_refrigeradas", "camaras_congeladas",
                                                           "tunel_congelado", "camara_subproductos")},
        "t_stock_refrigerado": tr({n: R.ctx["utilities"][n]["stock_refrigerado_t"] for n in NIVELES}),
        "t_stock_congelado": tr({n: R.ctx["utilities"][n]["stock_congelado_t"] for n in NIVELES}),
        "areas_por_funcion": {a: {"nombre": x["nombre"], "zona": x["zona"], "categoria": x["categoria"],
                                  "estado": x["estado"], "origen": x["origen"], **x["valores"]}
                              for a, x in R.areas.items()},
        "supuestos_terreno": {"retiro_m": R.e["retiro_m"] if R.e["retiro_m"] is not None else P["retiro_m"]["v"],
                              "retiro_origen": "INPUT" if R.e["retiro_m"] is not None else "SUPUESTO (DPV-141)",
                              "buffer_m": R.e["buffer_m"] if R.e["buffer_m"] is not None else P["buffer_proxy_m"]["v"],
                              "buffer_origen": "INPUT" if R.e["buffer_m"] is not None else "PROXY (SUP-121)",
                              "fos": R.e["fos"], "nota": "terreno VARIABLE con retiro, buffer y FOS"},
        "efluentes_por_tecnologia": R.ctx["efluentes_por_tecnologia"],
        "alertas": [c for c, _ in R.alertas],
        "estado_global": "INCOMPLETO" if any(x["estado"] == "PENDIENTE" for x in R.areas.values()) else "RANGO",
    }


# ---------------------------------------------------------------------------
# 6. ESCENARIOS Y CSV
# ---------------------------------------------------------------------------
PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen)\b", re.I)
CAMPOS = ["bloque", "escenario", "escala_aves_dia", "horas_netas", "config", "perfil", "dias_refrigerado",
          "dias_congelado", "automatizacion", "lineas", "enfriamiento", "tecnologia_efluentes", "escala_objetivo",
          "variable", "nombre", "categoria", "zona", "bajo", "medio", "alto", "unidad", "metodo", "estado",
          "clasificacion", "referencia", "origen_superficie"]


def _fila(bloque, esc, e, var, nombre, cat, zona, vals, unidad, metodo, estado, clasif, ref, origen=""):
    def f(x):
        return "" if x is None else round(x, 3)
    return {"bloque": bloque, "escenario": esc, "escala_aves_dia": e["aves_dia"], "horas_netas": e["horas_netas"],
            "config": e["config"], "perfil": e["perfil"], "dias_refrigerado": e["dias_refrigerado"],
            "dias_congelado": e["dias_congelado"], "automatizacion": e["automatizacion"], "lineas": e["lineas"],
            "enfriamiento": e["enfriamiento"], "tecnologia_efluentes": e["tecnologia_efluentes"],
            "escala_objetivo": e["escala_objetivo"] or "", "variable": var, "nombre": nombre, "categoria": cat,
            "zona": zona, "bajo": f(vals[0]), "medio": f(vals[1]), "alto": f(vals[2]), "unidad": unidad,
            "metodo": metodo, "estado": estado, "clasificacion": clasif, "referencia": ref,
            "origen_superficie": origen}


def _margen_txt(R):
    e = R.e
    r = f"retiro {e['retiro_m']:g} m informado" if e["retiro_m"] is not None else "retiro 5/10/15 m SUPUESTO"
    b = f"buffer {e['buffer_m']:g} m informado" if e["buffer_m"] is not None else "buffer 10/20/40 m PROXY"
    return f"{r}; {b}"


def filas_totales(bloque, esc, R):
    out = []
    for c in CATEGORIAS + ("construido", "operativo", "reserva"):
        out.append(_fila(bloque, esc, R.e, f"m2_{c}", f"Total {c}", c, "", [R.totales[n].get(c) for n in NIVELES],
                         "m²", "suma de áreas", "ESTIMACION", "[ESTIMACIÓN]", "", "suma (hereda el peor origen)"))
    for k, u in (("terreno_total", "m²"), ("terreno_ha", "ha"), ("huella_edificios", "m²"),
                 ("retiros_buffers", "m²"), ("ocupacion_huella_pct", "%"), ("margen_perimetral_m", "m")):
        out.append(_fila(bloque, esc, R.e, k, k, "terreno", "", [None if R.terreno[n] is None else R.terreno[n][k]
                                                                for n in NIVELES], u,
                         "fórmula de terreno; RETIRO Y BUFFER VARIABLES (" + _margen_txt(R) + ")", "ESTIMACION",
                         "[ESTIMACIÓN] con [SUPUESTO]/[PROXY]", "SUP-121; DPV-141", ORIGEN_TERRENO))
    out.append(_fila(bloque, esc, R.e, "m2_cubiertos_por_ave_dia", "Contraste con benchmarks [PVDP]", "contraste", "",
                     R.ctx["m2_cubiertos_por_ave_dia"], "m²/(ave/día)", "construido ÷ aves/día", "ESTIMACION",
                     "[ESTIMACIÓN]", "FTE-224; 002; 003; 009"))
    for k, u in (("dotacion_turno", "personas"), ("bahias_recepcion", "bahías"), ("docks_expedicion", "docks")):
        out.append(_fila(bloque, esc, R.e, k, k, "driver", "", R.ctx[k], u, "driver del modelo",
                         "PROXY" if (k == "dotacion_turno" and R.e["dotacion_turno"] is None) else "ESTIMACION",
                         "[ESTIMACIÓN] / [PROXY]", ""))
    for k in ("stock_refrigerado_t", "stock_congelado_t", "congelacion_t_dia", "agua_descargada_m3_dia"):
        out.append(_fila(bloque, esc, R.e, k, k, "insumo_09C", "", [R.ctx["utilities"][n][k] for n in NIVELES],
                         "t" if k.endswith("_t") else ("t/día" if "t_dia" in k else "m³/día"),
                         "importado de 11_agua_efluentes/modelo_utilities.py", "ESTIMACION", "[ESTIMACIÓN] 09C",
                         "SUP-055; SUP-056; SUP-070"))
    return out


def escenarios_sensibilidad():
    """Variaciones de a una dimensión alrededor de la referencia, para cada escala."""
    base = entradas_por_defecto()
    var = [("referencia", {})]
    var += [(f"config_{c}", {"config": c}) for c in ("A", "C")]
    var += [(f"perfil_{p}", {"perfil": p}) for p in ("P2", "P3")]
    var += [("inventario_1_7", {"dias_refrigerado": 1, "dias_congelado": 7}),
            ("inventario_7_28", {"dias_refrigerado": 7, "dias_congelado": 28}),
            ("P3_inventario_7_28", {"perfil": "P3", "dias_refrigerado": 7, "dias_congelado": 28})]
    var += [(f"automatizacion_{a}", {"automatizacion": a}) for a in ("manual", "auto")]
    var += [("dos_lineas", {"lineas": 2})]
    var += [(f"enfriamiento_{x}", {"enfriamiento": x}) for x in ("inmersion", "aire")]
    var += [(f"efluentes_{t}", {"tecnologia_efluentes": t}) for t in TECNOLOGIAS]
    var += [("horas_16", {"horas_netas": 16.0}), ("horas_6", {"horas_netas": 6.0})]
    var += [("objetivo_20000", {"escala_objetivo": 20000}), ("sin_rendering", {"reservar_rendering": False})]
    var += [("estricto", {"estricto": True})]
    for E in ESCALAS:
        for nombre, d in var:
            e = dict(base)
            e.update(d)
            e["aves_dia"] = E
            yield f"{nombre}", e


TRAYECTORIAS = {"A_2500_5000_10000_20000": (2500, 5000, 10000, 20000),
                "B_5000_10000_20000": (5000, 10000, 20000),
                "C_10000_20000": (10000, 20000)}


def construir_csv(ruta=CSV_SALIDA):
    filas = []
    base = entradas_por_defecto()
    for E in ESCALAS:                                       # detalle por área
        for t in TECNOLOGIAS:
            e = dict(base, aves_dia=E, tecnologia_efluentes=t)
            R = calcular(e)
            esc = f"detalle_{E}_{t}"
            for a in R.areas.values():
                filas.append(_fila("detalle", esc, R.e, a["id"], a["nombre"], a["categoria"], a["zona"],
                                   [a["valores"][n] for n in NIVELES], "m²", a["metodo"], a["estado"],
                                   a["clasificacion"], a["referencia"], a["origen"]))
            filas += filas_totales("detalle", esc, R)
    for esc, e in escenarios_sensibilidad():               # sensibilidad (totales)
        filas += filas_totales("sensibilidad", esc, calcular(e))
    for tr, etapas in TRAYECTORIAS.items():                 # expansión
        final = etapas[-1]
        for E in etapas:
            e = dict(base, aves_dia=E, escala_objetivo=final)
            R = calcular(e)
            filas += filas_totales("expansion", f"{tr}_etapa_{E}", R)
    for f in filas:
        for k, x in f.items():
            if isinstance(x, float) and not math.isfinite(x):
                raise ErrorSuperficies(f"valor no finito en {f['variable']}")
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    return filas


# ---------------------------------------------------------------------------
# 7. TESTS
# ---------------------------------------------------------------------------
def _lanza(f, *a, **k):
    try:
        f(*a, **k)
    except ErrorSuperficies:
        return True
    return False


def _todas(R):
    return [(a["id"], n, a["valores"][n]) for a in R.areas.values() for n in NIVELES]


def ejecutar_tests(verbose=True):
    res = []

    def chk(cod, desc, ok, det=""):
        res.append((cod, desc, bool(ok), det))

    base = entradas_por_defecto()
    grid = []
    for E in (2500, 5000, 10000, 20000):
        for c in ("A", "B", "C"):
            for p in ("P1", "P3"):
                for t in TECNOLOGIAS:
                    grid.append(dict(base, aves_dia=E, config=c, perfil=p, tecnologia_efluentes=t))
    grid += [dict(base, aves_dia=E, lineas=2, automatizacion="manual", horas_netas=16.0) for E in ESCALAS]
    Rs = [calcular(e) for e in grid]

    # T01 nunca negativas
    neg = [(R.e["aves_dia"], i, n, x) for R in Rs for i, n, x in _todas(R) if x is not None and x < 0]
    neg += [(R.e["aves_dia"], "terreno", n, R.terreno[n]["terreno_total"]) for R in Rs for n in NIVELES
            if R.terreno[n] and R.terreno[n]["terreno_total"] < 0]
    chk("T01", "Ninguna superficie es negativa (áreas, totales y terreno; 100 escenarios)", not neg, str(neg[:3]))

    # T02 total = suma de áreas
    ok = True
    for R in Rs:
        for n in NIVELES:
            for c in CATEGORIAS:
                s = sum(a["valores"][n] for a in R.areas.values() if a["categoria"] == c)
                ok &= abs(s - R.totales[n][c]) < 1e-6
            ok &= abs(R.totales[n]["construido"] - sum(R.totales[n][c] for c in CUBIERTAS)) < 1e-6
            ok &= abs(R.totales[n]["operativo"] - R.totales[n]["construido"] - R.totales[n]["exteriores"]
                      - R.totales[n]["efluentes"]) < 1e-6
            ok &= abs(R.reserva[n]["total"] - sum(x for k, x in R.reserva[n].items() if k != "total")) < 1e-6
            tr = R.terreno[n]
            ok &= abs(tr["terreno_total"] - tr["area_interna"] - tr["retiros_buffers"]) < 1e-6
    chk("T02", "Total = suma de áreas (categorías, construido, operativo, reserva y terreno)", ok)

    # T03 escala monótona
    malos = []
    for c in ("A", "B", "C"):
        for t in TECNOLOGIAS:
            prev = None
            for E in range(2000, 24001, 1000):
                R = calcular(dict(base, aves_dia=E, config=c, tecnologia_efluentes=t))
                if prev is not None:
                    for a in R.areas:
                        for n in NIVELES:
                            if R.areas[a]["valores"][n] + 1e-9 < prev.areas[a]["valores"][n]:
                                malos.append((c, t, E, a, n))
                    for n in NIVELES:
                        if R.terreno[n]["terreno_total"] + 1e-9 < prev.terreno[n]["terreno_total"]:
                            malos.append((c, t, E, "terreno", n))
                prev = R
    chk("T03", "Aumentar la escala no reduce ninguna área ni el terreno (2.000–24.000 aves/día, 12 combinaciones)",
        not malos, str(malos[:3]))
    # explicación documentada: más horas netas reducen la línea con alerta
    r8 = calcular(dict(base, horas_netas=8.0))
    r16 = calcular(dict(base, horas_netas=16.0))
    expl = (r16.areas["colgado_aturdido"]["valores"]["medio"] <= r8.areas["colgado_aturdido"]["valores"]["medio"]
            and any(c == "HORAS_NETAS" for c, _ in r16.alertas)
            and r16.areas["camaras_congeladas"]["valores"] == r8.areas["camaras_congeladas"]["valores"])
    chk("T03b", "Más horas netas reducen solo las salas de línea, con alerta explícita; las cámaras no cambian", expl)

    # T04 inventario no reduce frío
    malos = []
    for p in ("P1", "P2", "P3"):
        prev = None
        for d in (0, 1, 3, 7, 14, 28, 56):
            R = calcular(dict(base, perfil=p, dias_refrigerado=d, dias_congelado=d))
            if prev is not None:
                for n in NIVELES:
                    if R.totales[n]["frio"] + 1e-9 < prev.totales[n]["frio"]:
                        malos.append((p, d, n))
                    for a in ("camaras_refrigeradas", "camaras_congeladas"):
                        if R.areas[a]["valores"][n] + 1e-9 < prev.areas[a]["valores"][n]:
                            malos.append((p, d, a, n))
            prev = R
    r14 = calcular(dict(base, perfil="P3", dias_congelado=14))
    r28 = calcular(dict(base, perfil="P3", dias_congelado=28))
    estricto_sube = r28.areas["camaras_congeladas"]["valores"]["medio"] > r14.areas["camaras_congeladas"]["valores"]["medio"]
    tunel_igual = r28.areas["tunel_congelado"]["valores"] == r14.areas["tunel_congelado"]["valores"]
    chk("T04", "Aumentar días de inventario no reduce el frío; duplicar días agranda la cámara y NO el túnel",
        not malos and estricto_sube and tunel_igual, str(malos[:3]))

    # T05 expansión aumenta reserva
    rs = [calcular(dict(base, aves_dia=5000, escala_objetivo=o, reservar_rendering=False)).totales["medio"]["reserva"]
          for o in (5000, 10000, 15000, 20000)]
    r_sin = calcular(dict(base, aves_dia=5000, escala_objetivo=10000, reservar_rendering=False))
    r_con = calcular(dict(base, aves_dia=5000, escala_objetivo=10000, reservar_rendering=True))
    t_sin = r_sin.terreno["medio"]["terreno_total"]
    t_obj = calcular(dict(base, aves_dia=5000, escala_objetivo=20000, reservar_rendering=False)).terreno["medio"]["terreno_total"]
    chk("T05", "Mayor escala objetivo ⇒ mayor reserva y mayor terreno; objetivo = actual ⇒ reserva 0; rendering suma",
        rs[0] == 0 and all(rs[i] < rs[i + 1] for i in range(3)) and t_obj > t_sin
        and r_con.totales["medio"]["reserva"] > r_sin.totales["medio"]["reserva"], str(rs))

    # T06 faltantes ⇒ alertas
    R = calcular(base)
    cods = {c for c, _ in R.alertas}
    req = {"DOTACION_PROXY", "AVES_POR_CAMION", "T_POR_CAMION", "FOOTPRINT_DESCONOCIDO", "BUFFER_PROXY",
           "FOS_PENDIENTE", "RETIRO_PENDIENTE", "TECNOLOGIA_EFLUENTES_NO_DEFINIDA", "LODOS_PENDIENTE",
           "GENERADOR_PENDIENTE", "ENFRIAMIENTO_NO_DEFINIDO", "OBJETIVO_EXPANSION_NO_DEFINIDO",
           "CARGA_FRIGORIFICA_PENDIENTE"}
    completo = calcular(dict(base, dotacion_turno=100, aves_por_camion=5000, t_por_camion_despacho=10,
                             retiro_m=10, buffer_m=20, fos=0.6, enfriamiento="inmersion",
                             tecnologia_efluentes="aerobio_compacto", escala_objetivo=20000))
    c2 = {c for c, _ in completo.alertas}
    chk("T06", "Cada variable faltante genera su alerta; al informarla, la alerta desaparece",
        req <= cods and not ({"DOTACION_PROXY", "AVES_POR_CAMION", "T_POR_CAMION", "BUFFER_PROXY", "FOS_PENDIENTE",
                              "RETIRO_PENDIENTE", "TECNOLOGIA_EFLUENTES_NO_DEFINIDA", "ENFRIAMIENTO_NO_DEFINIDO",
                              "OBJETIVO_EXPANSION_NO_DEFINIDO"} & c2), str(req - cods))

    # T07 footprint desconocido ≠ 0
    Rp = calcular(base)
    proxies = [a for a in Rp.areas.values() if a["estado"] == "PROXY"]
    no_cero = all(a["valores"][n] > 0 for a in proxies for n in NIVELES)
    Re = calcular(dict(base, estricto=True))
    pend = [a for a in Re.areas.values() if a["estado"] == "PENDIENTE"]
    estricto_ok = (len(pend) > 0 and all(a["valores"]["medio"] is None for a in pend)
                   and Re.totales["medio"]["construido"] is None and Re.terreno["medio"] is None
                   and salida_interfaz(Re)["estado_global"] == "INCOMPLETO")
    rfp = calcular(dict(base, footprints={"colgado_aturdido": 40.0, "enfriamiento": 60.0}))
    fp_ok = (rfp.areas["colgado_aturdido"]["estado"] == "FOOTPRINT"
             and abs(rfp.areas["colgado_aturdido"]["valores"]["medio"] - 40 * v("factor_envolvente_footprint", 1)) < 1e-9)
    cero_rechazado = _lanza(calcular, dict(base, footprints={"colgado_aturdido": 0}))
    na = [a for a in Rp.areas.values() if a["estado"] == "NO_APLICA"]
    na_ok = all(a["clasificacion"] == "[NO APLICA]" or a["id"].startswith("efl_") for a in na)
    chk("T07", "Footprint desconocido: PROXY > 0 con alerta; en modo estricto None y totales None (nunca 0); "
               "footprint 0 rechazado; NO_APLICA explícito", no_cero and estricto_ok and fp_ok and cero_rechazado
        and na_ok)

    # T08 escenarios independientes
    e1 = entradas_por_defecto()
    e1.update(aves_dia=5000, config="C")
    e2 = entradas_por_defecto()
    e2.update(aves_dia=20000, perfil="P3", lineas=2)
    snap = copy.deepcopy(e1)
    a1 = salida_interfaz(calcular(e1))
    calcular(e2)
    a1b = salida_interfaz(calcular(e1))
    chk("T08", "Escenarios independientes: el orden de cálculo no cambia resultados y no se modifican las entradas",
        a1 == a1b and e1 == snap and base == entradas_por_defecto())

    # T09 bajo ≤ medio ≤ alto
    malos = [(R.e["aves_dia"], a, ) for R in Rs for a, x in R.areas.items()
             if not (x["valores"]["bajo"] <= x["valores"]["medio"] + 1e-9 <= x["valores"]["alto"] + 2e-9)]
    malos += [(R.e["aves_dia"], "terreno") for R in Rs
              if not R.terreno["bajo"]["terreno_total"] <= R.terreno["medio"]["terreno_total"] <= R.terreno["alto"]["terreno_total"]]
    chk("T09", "Rango ordenado bajo ≤ medio ≤ alto en todas las áreas, totales y terreno", not malos, str(malos[:3]))

    # T10 terreno ≥ operativo ≥ construido > 0
    ok = all(R.terreno[n]["terreno_total"] >= R.totales[n]["operativo"] >= R.totales[n]["construido"] > 0
             for R in Rs for n in NIVELES)
    chk("T10", "Terreno ≥ m² operativos ≥ m² construidos > 0 (m² de edificio ≠ m² de terreno)", ok)

    # T11 frío desde 09C
    ok = True
    for p in ("P1", "P2", "P3"):
        e = dict(base, perfil=p, dias_refrigerado=5, dias_congelado=21, base_inventario="dias_calendario")
        R = calcular(e)
        pp = mu.parametros("medio", perfil=dict(PERFILES[p]), perfil_id=p, dias_refrigerado=5, dias_congelado=21,
                           base_inventario="dias_calendario")
        r9 = mu.calcular(10000, 250, "medio", masas=masas_utilities("B"), p=pp)
        ok &= abs(R.ctx["utilities"]["medio"]["stock_congelado_t"] - r9["capacidad_almacenamiento_congelado_t"]) < 1e-9
        ok &= abs(R.ctx["utilities"]["medio"]["stock_refrigerado_t"] - r9["stock_refrigerado_t"]) < 1e-9
    mb = masas_utilities("B")
    mref = mu.kg_por_ave()
    ok &= all(abs(mb[k] - mref[k]) <= 1e-6 * max(1.0, abs(mref[k])) for k in mref)   # CSV de escala redondeado
    chk("T11", "Frío y efluentes leídos de 09C sin recalcular; masas de config. B = 09C (±1e-6, redondeo del CSV)", ok)

    # T12 configuración
    ra, rb, rc = (calcular(dict(base, config=c)) for c in "ABC")
    ok = (ra.areas["deshuese"]["estado"] == "NO_APLICA" and rb.areas["deshuese"]["estado"] == "NO_APLICA"
          and rc.areas["deshuese"]["valores"]["bajo"] > 0 and rc.areas["cms"]["valores"]["bajo"] > 0
          and ra.areas["trozado"]["valores"]["bajo"] > 0
          and ra.areas["trozado"]["valores"]["medio"] < rb.areas["trozado"]["valores"]["medio"])
    chk("T12", "Config. A conserva sala mínima de trozado; deshuese y CMS solo en C (NO_APLICA explícito en A/B)", ok)

    # T13 dos líneas
    r1 = calcular(dict(base, aves_dia=20000))
    r2 = calcular(dict(base, aves_dia=20000, lineas=2))
    ok = all(r2.areas[a]["valores"][n] >= r1.areas[a]["valores"][n]
             for a in ("colgado_aturdido", "sangrado_escaldado_desplumado", "evisceracion_inspeccion", "enfriamiento")
             for n in NIVELES) and r2.totales["medio"]["proceso"] > r1.totales["medio"]["proceso"]
    chk("T13", "Dos líneas ocupan más superficie de proceso que una (mismas aves/día)", ok)

    # T14 tecnología de efluentes cambia el terreno
    ts = {t: calcular(dict(base, tecnologia_efluentes=t)) for t in TECNOLOGIAS}
    ef = {t: ts[t].totales["medio"]["efluentes"] for t in TECNOLOGIAS}
    tt = {t: ts[t].terreno["medio"]["terreno_total"] for t in TECNOLOGIAS}
    chk("T14", "Efluentes: cloaca < compacto/anaerobio < lagunas, en área y en terreno",
        ef["cloaca"] < min(ef["aerobio_compacto"], ef["anaerobio_aerobio"]) and
        max(ef["aerobio_compacto"], ef["anaerobio_aerobio"]) < ef["lagunas"] and tt["cloaca"] < tt["lagunas"], str(ef))

    # T15 CSV sin economía y finito
    filas = construir_csv(os.path.join(os.path.dirname(CSV_SALIDA), ".tmp_test_superficies.csv"))
    os.remove(os.path.join(os.path.dirname(CSV_SALIDA), ".tmp_test_superficies.csv"))
    texto = " ".join(str(x) for f in filas for x in f.values())
    chk("T15", "CSV sin variables económicas; todos los números finitos", not PALABRAS_ECONOMICAS.search(texto)
        and len(filas) > 1000)

    # T16 entradas inválidas
    malas = [{"aves_dia": -1}, {"aves_dia": 0}, {"horas_netas": 25}, {"config": "D"},
             {"perfil": {"refrigerado": 0.5, "congelado": 0.4, "exportacion": 0.0}}, {"lineas": 3},
             {"footprints": {"colgado_aturdido": -5}}, {"footprints": {"area_inexistente": 10}},
             {"fos": 1.5}, {"dotacion_turno": 0}, {"tecnologia_efluentes": "humedal"}, {"dias_congelado": -1}]
    chk("T16", "Entradas inválidas se rechazan (escala ≤ 0, perfil ≠ 100 %, footprint ≤ 0, FOS > 1, etc.)",
        all(_lanza(calcular, dict(base, **m)) for m in malas))

    # T17 enfriamiento sin definir reserva el mayor
    ri = calcular(dict(base, enfriamiento="inmersion")).areas["enfriamiento"]["valores"]
    rai = calcular(dict(base, enfriamiento="aire")).areas["enfriamiento"]["valores"]
    rs_ = calcular(base).areas["enfriamiento"]["valores"]
    chk("T17", "Enfriamiento sin decidir reserva la superficie mayor (aire ≥ inmersión)",
        all(rs_[n] == max(ri[n], rai[n]) for n in NIVELES) and all(rai[n] >= ri[n] for n in NIVELES))

    # T18 trayectorias: construido hoy + reserva = escala final; el terreno se decide en la etapa 1
    ok = True
    for tr, etapas in TRAYECTORIAS.items():
        fin = calcular(dict(base, aves_dia=etapas[-1], escala_objetivo=etapas[-1]))
        for E in etapas:
            R = calcular(dict(base, aves_dia=E, escala_objetivo=etapas[-1]))
            for n in NIVELES:
                ok &= abs(R.terreno[n]["terreno_total"] - fin.terreno[n]["terreno_total"]) < 1e-6 * fin.terreno[n]["terreno_total"]
                ok &= R.totales[n]["construido"] <= fin.totales[n]["construido"] + 1e-9
    chk("T18", "Expansión: en cada etapa de A/B/C, construido ≤ final y terreno = terreno de la escala final", ok)

    # T19 ninguna salida proxy etiquetada como verificada; toda área tiene tipo de origen A–E
    Rr = calcular(base)
    ok = all("VERIFICADO" not in (a["clasificacion"] + a["estado"]).upper() for a in Rr.areas.values())
    ok &= all(("SUPUESTO" in a["clasificacion"] or "PROXY" in a["clasificacion"]) for a in Rr.areas.values()
              if a["estado"] == "PROXY")
    ok &= all(a["origen"] and set(a["origen"].replace("·", "")) <= set(TIPOS_ORIGEN) for a in Rr.areas.values())
    ok &= all(a["id"] in ORIGEN_AREA for a in Rr.areas.values())
    ok &= all("C" in a["origen"] for a in Rr.areas.values() if a["estado"] == "PROXY")
    ok &= not any("VERIFICADO" in f["clasificacion"].upper() for f in filas)
    chk("T19", "Ninguna superficie (ni fila del CSV) se etiqueta como verificada; toda área PROXY lleva origen C", ok)

    # T20 el terreno declara que retiro y buffer son variables
    ft = [f for f in filas if f["categoria"] == "terreno"]
    si = salida_interfaz(Rr)["supuestos_terreno"]
    ok = (len(ft) > 0 and all("VARIABLES" in f["metodo"] and "VARIABLES" in f["origen_superficie"] for f in ft)
          and si["retiro_origen"].startswith("SUPUESTO") and si["buffer_origen"].startswith("PROXY")
          and salida_interfaz(calcular(dict(base, retiro_m=12, buffer_m=0)))["supuestos_terreno"]["retiro_origen"]
          == "INPUT")
    chk("T20", "Las salidas de terreno indican que retiro y buffer son variables (supuesto/proxy o input)", ok)

    # T21 modificar retiro o buffer cambia el terreno (y no el edificio)
    ts = [calcular(dict(base, retiro_m=r, buffer_m=b)) for r, b in ((0, 0), (10, 0), (10, 20), (20, 40))]
    tt = [x.terreno["medio"]["terreno_total"] for x in ts]
    ok = all(tt[i] < tt[i + 1] for i in range(3))
    ok &= len({round(x.totales["medio"]["construido"], 6) for x in ts}) == 1
    chk("T21", "Cambiar retiro o buffer cambia el terreno y no los m² construidos", ok, str(tt))

    if verbose:
        for cod, desc, ok, det in res:
            print(f"  [{'OK' if ok else 'FALLA'}] {cod} {desc}" + ("" if ok else f" → {det}"))
        print(f"  {sum(1 for r in res if r[2])}/{len(res)} tests OK")
    return res


MUTACIONES = {
    "M01": "el total omite un área",
    "M02": "footprint desconocido convertido en 0",
    "M03": "la cámara congelada ignora los días de inventario",
    "M04": "la escala objetivo se ignora (reserva no crece)",
    "M05": "se suprimen las alertas",
    "M06": "el cálculo modifica las entradas del llamador",
    "M07": "evisceración inversamente proporcional al ritmo",
}


def prueba_mutaciones():
    global _MUT
    detectadas = 0
    for m, desc in MUTACIONES.items():
        _MUT = {m}
        _kg_config.cache_clear()
        try:
            r = ejecutar_tests(verbose=False)
            fallan = [c for c, _, ok, _ in r if not ok]
        except Exception as ex:   # una excepción también es detección
            fallan = [f"excepción {type(ex).__name__}"]
        _MUT = set()
        ok = bool(fallan)
        detectadas += ok
        print(f"  {m} ({desc}): {'DETECTADA por ' + ', '.join(fallan) if ok else 'NO DETECTADA'}")
    print(f"  {detectadas}/{len(MUTACIONES)} mutaciones detectadas")
    return detectadas == len(MUTACIONES)


# ---------------------------------------------------------------------------
# 8. TABLAS PARA LOS DOCUMENTOS
# ---------------------------------------------------------------------------
def fmt(x, d=0):
    if x is None:
        return "PEND."
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def rng(vals, d=0):
    return " / ".join(fmt(x, d) for x in vals)


def imprimir_tablas():
    base = entradas_por_defecto()
    Rs = {E: calcular(dict(base, aves_dia=E)) for E in ESCALAS}
    print("\n### Áreas por escala (m², bajo / medio / alto) — referencia: config. B, P1 3/14 d, semi, 1 línea, "
          "enfriamiento sin definir (reserva el mayor), efluentes anaerobio+aerobio (reserva)\n")
    print("| Área | Cat. | Zona | Estado | " + " | ".join(f"{E:,}".replace(",", ".") for E in ESCALAS) + " |")
    print("|---|---|---|---|" + "---|" * len(ESCALAS))
    for a in Rs[10000].areas:
        x = Rs[10000].areas[a]
        print(f"| {x['nombre']} | {x['categoria']} | {x['zona']} | {x['estado']} | " +
              " | ".join(rng([Rs[E].areas[a]['valores'][n] for n in NIVELES]) for E in ESCALAS) + " |")
    print("\n### Totales por categoría (m², bajo / medio / alto)\n")
    print("| Categoría | " + " | ".join(f"{E:,}".replace(",", ".") for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for c in CATEGORIAS + ("construido", "operativo", "reserva"):
        print(f"| {c} | " + " | ".join(rng([Rs[E].totales[n].get(c) for n in NIVELES]) for E in ESCALAS) + " |")
    for k, d in (("terreno_total", 0), ("terreno_ha", 2), ("ocupacion_huella_pct", 0)):
        print(f"| {k} | " + " | ".join(rng([Rs[E].terreno[n][k] for n in NIVELES], d) for E in ESCALAS) + " |")
    print("| m² cubiertos/(ave/día) | " + " | ".join(rng(Rs[E].ctx['m2_cubiertos_por_ave_dia'], 2) for E in ESCALAS) + " |")
    print("| dotación por turno (proxy) | " + " | ".join(rng(Rs[E].ctx['dotacion_turno']) for E in ESCALAS) + " |")
    print("| bahías de recepción | " + " | ".join(rng(Rs[E].ctx['bahias_recepcion']) for E in ESCALAS) + " |")
    print("| docks de expedición | " + " | ".join(rng(Rs[E].ctx['docks_expedicion']) for E in ESCALAS) + " |")

    print("\n### Efluentes y terreno por tecnología (medio; m² efluentes · ha de terreno)\n")
    print("| Tecnología | " + " | ".join(f"{E:,}".replace(",", ".") for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for t in TECNOLOGIAS:
        cells = []
        for E in ESCALAS:
            R = calcular(dict(base, aves_dia=E, tecnologia_efluentes=t))
            cells.append(f"{fmt(R.totales['medio']['efluentes'])} · {fmt(R.terreno['medio']['terreno_ha'], 2)} ha "
                         f"({fmt(R.terreno['bajo']['terreno_ha'], 2)}–{fmt(R.terreno['alto']['terreno_ha'], 2)})")
        print(f"| {t} | " + " | ".join(cells) + " |")

    print("\n### Frío por perfil e inventario (m² de frío medio; t congeladas en stock)\n")
    print("| Perfil / días (refr./cong.) | " + " | ".join(f"{E:,}".replace(",", ".") for E in ESCALAS) + " |")
    print("|---|" + "---|" * len(ESCALAS))
    for p in ("P1", "P2", "P3"):
        for dr, dc in ((3, 14), (7, 28)):
            cells = []
            for E in ESCALAS:
                R = calcular(dict(base, aves_dia=E, perfil=p, dias_refrigerado=dr, dias_congelado=dc))
                cells.append(f"{fmt(R.totales['medio']['frio'])} m² · {fmt(R.ctx['utilities']['medio']['stock_congelado_t'])} t")
            print(f"| {p} {dr}/{dc} | " + " | ".join(cells) + " |")

    print("\n### Sensibilidad (10.000 aves/día; m² construidos medio · terreno medio ha)\n")
    for nombre, d in (("referencia", {}), ("config A", {"config": "A"}), ("config C", {"config": "C"}),
                      ("P3 7/28", {"perfil": "P3", "dias_refrigerado": 7, "dias_congelado": 28}),
                      ("manual", {"automatizacion": "manual"}), ("auto", {"automatizacion": "auto"}),
                      ("dos líneas", {"lineas": 2}), ("inmersión", {"enfriamiento": "inmersion"}),
                      ("aire", {"enfriamiento": "aire"}), ("16 h netas", {"horas_netas": 16.0}),
                      ("objetivo 20.000", {"escala_objetivo": 20000}), ("sin rendering", {"reservar_rendering": False})):
        R = calcular(dict(base, **d))
        print(f"- {nombre}: {fmt(R.totales['medio']['construido'])} m² construidos · "
              f"{fmt(R.terreno['medio']['terreno_ha'], 2)} ha")

    print("\n### Trayectorias de expansión (medio; reserva hasta la etapa final)\n")
    for tr, et in TRAYECTORIAS.items():
        for E in et:
            R = calcular(dict(base, aves_dia=E, escala_objetivo=et[-1]))
            print(f"- {tr} · etapa {E}: construido {fmt(R.totales['medio']['construido'])} m²; reserva "
                  f"{fmt(R.totales['medio']['reserva'])} m²; terreno {fmt(R.terreno['medio']['terreno_ha'], 2)} ha")
    R = Rs[10000]
    print("\nAlertas (referencia 10.000):", ", ".join(c for c, _ in R.alertas))


def main():
    ap = argparse.ArgumentParser(description="Modelo conceptual de superficies (12C)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--tablas", action="store_true")
    ap.add_argument("--escenario", action="store_true")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--horas-netas", type=float, default=8.0)
    ap.add_argument("--config", default="B")
    ap.add_argument("--perfil", default="P1")
    ap.add_argument("--dias-refrigerado", type=float, default=3)
    ap.add_argument("--dias-congelado", type=float, default=14)
    ap.add_argument("--automatizacion", default="semi")
    ap.add_argument("--lineas", type=int, default=1)
    ap.add_argument("--enfriamiento", default="sin_definir")
    ap.add_argument("--efluentes", default="sin_definir")
    ap.add_argument("--objetivo", type=float, default=None)
    ap.add_argument("--dotacion", type=float, default=None)
    ap.add_argument("--estricto", action="store_true")
    a = ap.parse_args()
    if a.mutaciones:
        sys.exit(0 if prueba_mutaciones() else 1)
    print(f"Modelo de superficies v{VERSION} ({FECHA}) — tests:")
    r = ejecutar_tests()
    if not all(x[2] for x in r):
        sys.exit(1)
    if a.solo_tests:
        return
    if a.tablas:
        imprimir_tablas()
        return
    if a.escenario:
        R = calcular({"aves_dia": a.aves_dia, "horas_netas": a.horas_netas, "config": a.config, "perfil": a.perfil,
                      "dias_refrigerado": a.dias_refrigerado, "dias_congelado": a.dias_congelado,
                      "automatizacion": a.automatizacion, "lineas": a.lineas, "enfriamiento": a.enfriamiento,
                      "tecnologia_efluentes": a.efluentes, "escala_objetivo": a.objetivo,
                      "dotacion_turno": a.dotacion, "estricto": a.estricto})
        for x in R.areas.values():
            print(f"  {x['nombre'][:60]:60s} {x['estado']:10s} {rng([x['valores'][n] for n in NIVELES])}")
        for c in CATEGORIAS + ("construido", "operativo", "reserva"):
            print(f"  TOTAL {c:15s} {rng([R.totales[n].get(c) for n in NIVELES])}")
        print("  TERRENO m²       ", rng([None if R.terreno[n] is None else R.terreno[n]['terreno_total']
                                         for n in NIVELES]))
        for c, m in R.alertas:
            print(f"  ALERTA {c}: {m}")
        return
    filas = construir_csv()
    print(f"CSV escrito: {os.path.relpath(CSV_SALIDA, RAIZ)} ({len(filas)} filas)")


if __name__ == "__main__":
    main()
