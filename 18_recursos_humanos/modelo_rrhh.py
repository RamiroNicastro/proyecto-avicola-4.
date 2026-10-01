#!/usr/bin/env python3
"""
modelo_rrhh.py — Modelo organizacional y de dotación por escala (sesión 14A)
===========================================================================

Versión 1.0 · 2026-10-01 · Fase 0 (prefactibilidad) · Carpeta 18_recursos_humanos

PREGUNTA
  ¿Qué personas necesita la empresa, dónde trabajan, en qué turnos y cómo cambia la estructura
  al crecer de 2.500 a 5.000, 10.000 y 20.000 aves faenadas por día operativo?

QUÉ HACE
  Para un escenario (aves/día, horas netas, modo de turnos, automatización, mix, flota,
  limpieza, mantenimiento, productividad) construye la lista de PUESTOS con:
    personas por turno · equipos de turno · personas físicas · equivalentes (FTE por horas) ·
    zona de trabajo · grupo (directo / supervisión / soporte / administración / dirección) ·
    modalidad (interno / externo / PENDIENTE).
  Agrega: directos, indirectos, supervisión, soporte, administración, dirección, total; externos
  equivalentes de las funciones tercerizadas; alertas de jornada y de la ecuación de 24 h de 09A;
  indicadores de productividad (varios, ninguno es "la verdad").

QUÉ NO HACE
  No calcula salarios, cargas sociales ni OPEX (la plantilla de costo queda VACÍA). No elige escala,
  turnos, automatización, modalidad de limpieza, mantenimiento ni flota. No modifica los modelos
  que importa (05/09A, 09/12C, 13/12B, 23). No usa ninguna productividad como dato argentino real:
  todos los coeficientes son [SUPUESTO] de rango (alta / media / baja) o [PVDP] débiles.

DEFINICIONES
  E            = aves faenadas por día operativo.
  h            = horas NETAS de faena por día (todas las cuadrillas); ritmo r = E / h (aves/h).
  turnos       = "1" (una cuadrilla, jornada normal) · "extendido" (una cuadrilla con horas extra)
                 · "2" (dos cuadrillas; cada una h/2 netas). Ninguno se presume viable.
  cuadrillas   = 1, 1, 2 respectivamente (n_c).
  presencia    = horas de presencia de una cuadrilla de línea por día
                 = h_c / D + pausas(h_c) + limpieza_intermedia(h_c) [+ solapamiento de cambio de turno]
                 con h_c = h / n_c y D, pausas, limpieza intermedia de 09A (VENTANAS, SUP-061/062).
  puesto/turno = posición ocupada simultáneamente en una cuadrilla.
  personas     = personas físicas = ⌈ puestos/turno × n_c × factor de cobertura ⌉ (ausentismo,
                 vacaciones, licencias: SUP-14A-03). Roles de estructura: sin factor.
  equivalentes = FTE por horas = puestos × n_c × presencia × días / horas normales semanales
                 × factor de cobertura (incluye horas extra como fracción de persona).
  productividad "alta" = menos personas (coeficientes optimistas); "baja" = más personas.

FÓRMULAS PRINCIPALES (puestos por cuadrilla; r_c = r, ritmo de la línea mientras corre)
  área por ritmo      = ⌈ fijo + coef[nivel] × r / 1.000 ⌉                    (aves/h)
  área por kg         = ⌈ fijo + (kg/ave × r) / productividad_kg_h[nivel] ⌉   (trozado, deshuese, empaque)
  área por t          = ⌈ fijo + t/día / n_c / t_por_persona_turno ⌉           (cámaras, subproductos)
  supervisores        = ⌈ directos por cuadrilla / span ⌉ (mínimo 1)
  limpieza post-prod. = ⌈ m² de proceso (12C) × f_auto / (m²/persona-h) / (t_limpieza + t_sanitización) ⌉
  mantenimiento       = max( cobertura presencial , carga por activos )
      cobertura       = días × (horas de producción × técnicos simultáneos + horas fuera de producción × 1)
                        / horas normales × cobertura
      carga           = Σ_equipos presentes  h_semana[nivel efectivo] × peso_criticidad × unidades
                        / horas productivas de técnico      (matriz 08_maquinaria/matriz_equipos.csv)
  choferes aves vivas = flota mínima (13_logistica, capacidad de ESCENARIO 5.500 aves/camión, SUP-033)
                        × factor de cobertura — sólo si la flota es propia
  choferes producto   = PENDIENTE salvo capacidad de camión y distancia explícitas (DPV-084, DPV-036)
  24 h                = 05_proceso_industrial/modelo_capacidad_proceso.ventana_24h (alerta si holgura < 0)

ENTRADAS (escenario; ver ESCENARIO_BASE)
  aves_dia · horas_netas · turnos · automatizacion (manual / mecanizado / semiautomatico /
  automatico) · config (A entero / B trozado / C deshuesado, balance v1.1) · flota_propia ·
  limpieza (propia / tercerizada / hibrida) · mantenimiento (propio / tercerizado / mixto) ·
  productividad (alta / media / baja) · ventana (optimista / media / conservadora; por defecto
  ligada a la productividad) · dias_semana (5 / 6) · planta_propia (False = asset-light, faena a
  façon) · abastecimiento (integracion / compra) · laboratorio (externo / propio) ·
  aves_camion (None = PENDIENTE) · cap_camion_producto_t y dist_producto_km (None = PENDIENTE).

SALIDAS
  18_recursos_humanos/escenarios_rrhh.csv           (una fila por escenario; punto decimal)
  18_recursos_humanos/plantilla_costo_laboral.csv   (puesto × escenario de referencia; costos VACÍOS)

UNIDADES: personas, personas/turno, FTE, h, h/semana, aves/h, kg/h, t/día, m².

USO
  python3 18_recursos_humanos/modelo_rrhh.py                # tests + CSV + tablas resumen
  python3 18_recursos_humanos/modelo_rrhh.py --solo-tests
  python3 18_recursos_humanos/modelo_rrhh.py --tablas       # sólo tablas (sin escribir CSV)
  python3 18_recursos_humanos/modelo_rrhh.py --mutaciones   # verifica que los tests detectan errores

TESTS (15) R01 dotación ≥ 0 · R02 más escala ⇒ no menos personal · R03/R03b automatización no reduce
  técnicos y sí directos · R04 tercerizar retira interno y conserva la función · R05 24 h y jornada con alerta
  explícita · R06 escenarios independientes · R07 faltantes PENDIENTE · R08 entradas inválidas · R09–R11
  consistencia y KPI · R12 09A intacto · R13 rangos ordenados · R14 mix. --mutaciones: 8 errores deliberados.

IDs: supuestos SUP-14A-01..15, datos por validar DPV-14A-##, decisiones DEC-14A-##, fuentes FTE-14A-###
(provisionales; ver actualizaciones_gestion_14A.md). Registros centrales NO modificados.
"""

from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import argparse  # noqa: E402
import copy  # noqa: E402
import csv  # noqa: E402
import io  # noqa: E402
import itertools  # noqa: E402
import math  # noqa: E402
import os  # noqa: E402
from contextlib import redirect_stdout  # noqa: E402
from functools import lru_cache  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _sub in ("05_proceso_industrial", "09_layout_obra_civil", "13_logistica", "23_plan_expansion"):
    sys.path.insert(0, os.path.join(RAIZ, _sub))
with redirect_stdout(io.StringIO()):
    import modelo_capacidad_proceso as mc  # noqa: E402  (09A v1.1: ventana de 24 h, D, kg/ave)
    import modelo_superficies as ms        # noqa: E402  (12C v1.0.1: m² de proceso para limpieza)
    import modelo_logistica as ml          # noqa: E402  (12B v1.1: flota de aves vivas, granjas eq.)

VERSION = "1.0"
FECHA = "2026-10-01"
CSV_ESCENARIOS = os.path.join(AQUI, "escenarios_rrhh.csv")
CSV_PLANTILLA = os.path.join(AQUI, "plantilla_costo_laboral.csv")
CSV_EQUIPOS = os.path.join(RAIZ, "08_maquinaria", "matriz_equipos.csv")

ESCALAS = tuple(mc.ESCALAS)                                    # 2.500 / 5.000 / 10.000 / 20.000
NIVELES_AUTO = ("manual", "mecanizado", "semiautomatico", "automatico")
ORDEN_NIVEL = {"M": 0, "Mc": 1, "S": 2, "A": 3}
NIVEL_OBJETIVO = {"manual": 0, "mecanizado": 1, "semiautomatico": 2, "automatico": 3}
MODOS_TURNO = ("1", "extendido", "2")
CUADRILLAS = {"1": 1, "extendido": 1, "2": 2}
PROD = ("alta", "media", "baja")                               # alta = menos personas
VENTANA_POR_PROD = {"alta": "optimista", "media": "media", "baja": "conservadora"}
AREA_12C_POR_PROD = {"alta": "bajo", "media": "medio", "baja": "alto"}
AUTO_12C = {"manual": "manual", "mecanizado": "manual", "semiautomatico": "semi", "automatico": "auto"}
GRUPOS = ("directo", "supervision", "soporte", "administracion", "direccion")
PENDIENTE = None


class ErrorRRHH(Exception):
    pass


def T(alta, media, baja):
    """Triple de sensibilidad: alta productividad (menos personas) / media / baja."""
    return {"alta": alta, "media": media, "baja": baja}


# ---------------------------------------------------------------------------
# 1. PARÁMETROS — todos [SUPUESTO] de rango o [PVDP]; ninguno es dato argentino medido
# ---------------------------------------------------------------------------
P = {
    # --- jornada y cobertura (SUP-14A-02, SUP-14A-03; DPV-082, DPV-14A-01, DPV-14A-02)
    "jornada_normal_h": 8.0,              # [PVDP] Ley 11.544 (FTE-14A-001); convenio aplicable PENDIENTE
    "jornada_extendida_max_h": 10.0,      # [SUPUESTO] SUP-14A-02: tope de trabajo de un turno extendido
    "horas_extra_mes_ref": 30.0,          # [PVDP] referencia de tope mensual (FTE-14A-002); a verificar
    "horas_semana_normal": T(48.0, 45.0, 44.0),   # [PVDP/SUPUESTO] Ley 11.544 vs convenio (DPV-14A-01)
    "factor_cobertura": T(1.08, 1.12, 1.18),      # [SUPUESTO] SUP-14A-03 ausentismo+vacaciones+licencias
    "solape_cambio_turno_h": 0.25,        # [SUPUESTO] SUP-14A-02: traspaso entre cuadrillas
    # --- operación industrial: puestos por 1.000 aves/h (SUP-14A-04)
    "colgado_por_1000": T(1000 / 1380, 1.0, 1000 / 690),   # FTE-219 [PVDP·débil] 23 aves/min; prudente 50 % (SUP-063)
    "descarga_por_1000": {"M": T(0.6, 0.8, 1.0), "S": T(0.4, 0.5, 0.7), "A": T(0.2, 0.3, 0.4)},
    "faena_por_1000": {"M": T(1.6, 2.2, 3.0), "Mc": T(1.2, 1.6, 2.2), "S": T(0.6, 0.9, 1.3), "A": T(0.2, 0.5, 0.8)},
    # eviscerado manual: FTE-218 [PVDP·débil] 2 aves/min/operario = 8,3 por 1.000 aves/h; media al 75 %,
    # baja al 50 % (prudente SUP-063); + cosecha de menudencias y lavado 1,5 / 2,5 / 3,5
    "evisc_por_1000": {"M": T(8.3 + 1.5, 8.3 / 0.75 + 2.5, 8.3 / 0.5 + 3.5), "S": T(4.0, 6.0, 9.0),
                       "A": T(1.0, 2.2, 3.5)},
    "evisc_fijo": {"M": 1, "S": 1, "A": 2},
    "clasif_por_1000": {"M": T(1.0, 1.5, 2.0), "S": T(0.5, 0.8, 1.0), "A": T(0.2, 0.3, 0.5)},
    # kg/persona-h (base: kg que entran a la operación, balance v1.1) — sin fuente (SUP-14A-05)
    "trozado_kg_h": {"M": T(250, 180, 120), "Mc": T(300, 220, 150), "S": T(450, 320, 220), "A": T(1500, 800, 500)},
    "deshuese_kg_h": {"M": T(70, 50, 35), "S": T(100, 75, 55), "A": T(350, 250, 180)},
    "empaque_kg_h": {"M": T(350, 250, 170), "Mc": T(450, 330, 230), "S": T(700, 500, 350), "A": T(2000, 1100, 700)},
    "camaras_t_persona_turno": T(25.0, 18.0, 12.0),               # t comestible movida por persona-turno
    "subprod_t_persona_turno": {"M": T(6.0, 4.0, 3.0), "S": T(8.0, 6.0, 4.0), "A": T(15.0, 10.0, 8.0)},
    "limpieza_operativa_por_1000": T(0.3, 0.5, 0.8),              # en turno (pisos, derrames, recipientes)
    # --- limpieza post-producción (SUP-14A-06; DPV-091)
    "limpieza_m2_persona_h": T(60.0, 40.0, 25.0),                 # m² de salas de proceso por persona-hora
    "limpieza_factor_auto": {"manual": 1.0, "mecanizado": 1.0, "semiautomatico": 1.1, "automatico": 1.25},
    "limpieza_hibrida_interna": 0.30,                             # fracción interna en esquema híbrido
    # --- supervisión (SUP-14A-07)
    "span_supervision": T(30, 22, 15),                            # directos por supervisor de línea
    # --- calidad: control operativo por cuadrilla (SUP-14A-08)
    "control_calidad_por_1000": T(0.6, 0.8, 1.2),
    # --- mantenimiento por activos (SUP-14A-09)
    "mant_h_semana_equipo": {"M": T(0.0, 0.0, 0.0), "Mc": T(0.5, 0.75, 1.5), "S": T(0.75, 1.5, 3.0),
                             "A": T(1.5, 3.0, 6.0)},
    "mant_peso_criticidad": {"CRÍTICO": 1.5, "IMPORTANTE": 1.0, "SECUNDARIO": 0.5},
    "mant_h_productivas_tecnico": T(36.0, 32.0, 28.0),
    "unidades_duplicables_aves_h": 1250.0,                        # 1 unidad por cada 1.250 aves/h (SUP-14A-09)
    # --- producción primaria (coordinación; SUP-14A-10)
    "granjas_por_tecnico": T(20, 15, 10),
    "plazas_granja": 30000,                                       # 12B/03 [ESTIMACIÓN]
    # --- logística (SUP-14A-11)
    "aves_camion_escenario": 5500,                                # SUP-033 (sin fuente), capacidad de ESCENARIO
    "radio_km_escenario": 100,                                    # SUP-091 (sensibilidad, no ubicación)
    # --- RR. HH. (SUP-14A-12)
    "personas_por_rrhh": T(150, 120, 90),
}

# Roles de estructura por banda de escala (equivalentes internos; 0,5 = rol compartido).
# Bandas: S < 4.000 · M < 8.000 · L < 15.000 · XL ≥ 15.000 aves/día (SUP-14A-13).
BANDAS = (("S", 4000), ("M", 8000), ("L", 15000), ("XL", float("inf")))
ESTRUCTURA = {
    # clave: (puesto, categoría, grupo, zona, {S, M, L, XL}, contrato, nota)
    "jefe_produccion": ("Jefe de producción", "operacion_industrial", "supervision", "transversal",
                        {"S": 0, "M": 0, "L": 1, "XL": 1}, "fuera_convenio", "Por debajo de 10.000 lo cubre el gerente de operaciones"),
    "jefe_mantenimiento": ("Jefe de mantenimiento", "soporte_industrial", "soporte", "transversal",
                           {"S": 0, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "En 2.500 lo cubre un técnico líder"),
    "panolero": ("Pañolero / repuestos", "soporte_industrial", "soporte", "transversal",
                 {"S": 0, "M": 0, "L": 1, "XL": 1}, "convenio_pendiente", ""),
    "jefe_calidad": ("Jefe de calidad e inocuidad", "soporte_industrial", "soporte", "transversal",
                     {"S": 1, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "Reporta fuera de producción (independencia)"),
    "analista_appcc": ("Analista APPCC / documentación", "soporte_industrial", "soporte", "oficinas",
                       {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", "En 2.500 compartido con el jefe de calidad"),
    "trazabilidad": ("Trazabilidad y registros", "soporte_industrial", "soporte", "oficinas",
                     {"S": 0, "M": 0.5, "L": 1, "XL": 1}, "convenio_pendiente", ""),
    "hys": ("Higiene y seguridad laboral (interno)", "soporte_industrial", "soporte", "transversal",
            {"S": 0, "M": 0, "L": 1, "XL": 1}, "fuera_convenio", "Servicio externo en S y M; horas mínimas por norma PENDIENTE (DPV-14A-07)"),
    "lavanderia": ("Lavandería / ropería por zona", "soporte_industrial", "soporte", "personal",
                   {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "convenio_pendiente", "Alternativa tercerizada (12C)"),
    "planificacion_trafico": ("Planificación y tráfico", "logistica", "soporte", "oficinas",
                              {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", ""),
    "deposito_insumos": ("Recepción de insumos y depósito (envases, químicos)", "logistica", "soporte", "deposito",
                         {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "convenio_pendiente", ""),
    "expedicion_adm": ("Administración de expedición (remitos, DT-e)", "logistica", "soporte", "oficinas",
                       {"S": 0, "M": 0.5, "L": 1, "XL": 2}, "convenio_pendiente", ""),
    "compras": ("Compras", "administracion", "administracion", "oficinas",
                {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", ""),
    "ventas": ("Ventas / ejecutivos de cuenta", "administracion", "administracion", "oficinas",
               {"S": 1, "M": 2, "L": 3, "XL": 4}, "fuera_convenio", "Depende de canales y clientes, no sólo de aves (02_clientes_demanda)"),
    "administracion": ("Administración (facturación, cobranzas, pagos)", "administracion", "administracion", "oficinas",
                       {"S": 1, "M": 1, "L": 2, "XL": 3}, "fuera_convenio", ""),
    "finanzas": ("Finanzas, contabilidad y tesorería", "administracion", "administracion", "oficinas",
                 {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", "En 2.500 con contador externo"),
    "sistemas": ("Sistemas y datos", "administracion", "administracion", "oficinas",
                 {"S": 0, "M": 0.5, "L": 1, "XL": 2}, "fuera_convenio", "En 2.500 servicio externo"),
    "gerente_general": ("Gerente general", "direccion", "direccion", "oficinas",
                        {"S": 1, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "En 2.500 también comercial y adm./finanzas"),
    "gerente_operaciones": ("Gerente de operaciones / planta", "direccion", "direccion", "oficinas",
                            {"S": 1, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "Sólo con planta propia"),
    "gerente_comercial": ("Gerente comercial", "direccion", "direccion", "oficinas",
                          {"S": 0, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", ""),
    "gerente_adm_fin": ("Gerente de administración y finanzas", "direccion", "direccion", "oficinas",
                        {"S": 0, "M": 0, "L": 1, "XL": 1}, "fuera_convenio", ""),
    "gerente_calidad": ("Gerente de calidad e inocuidad", "direccion", "direccion", "oficinas",
                        {"S": 0, "M": 0, "L": 0, "XL": 1}, "fuera_convenio", "Antes, el jefe de calidad reporta al gerente general"),
}
PRIMARIA = {   # abastecimiento por integración (no incluye personal de granjas de terceros)
    "coordinador_integracion": ("Coordinador de producción primaria / integrados", {"S": 0.5, "M": 1, "L": 1, "XL": 1}),
    "veterinario": ("Veterinario de la integración", {"S": 0.5, "M": 1, "L": 1, "XL": 2}),
    "planificacion_crianza": ("Planificación de crianza (pollito BB, alimento, cosecha)", {"S": 0, "M": 0.5, "L": 1, "XL": 1}),
}
PRIMARIA_COMPRA = {
    "coordinador_abastecimiento": ("Coordinador de abastecimiento de pollo vivo y recepción", {"S": 0.5, "M": 1, "L": 1, "XL": 1}),
    "veterinario": ("Veterinario (recepción, bienestar, sanidad de proveedores)", {"S": 0.5, "M": 0.5, "L": 1, "XL": 1}),
}
LAB_PROPIO = {"S": 1, "M": 1, "L": 2, "XL": 3}

ESCENARIO_BASE = {
    "aves_dia": 10000, "horas_netas": 8.0, "turnos": "1", "automatizacion": "semiautomatico",
    "config": "B", "flota_propia": False, "limpieza": "propia", "mantenimiento": "propio",
    "productividad": "media", "ventana": None, "dias_semana": 5, "planta_propia": True,
    "abastecimiento": "integracion", "laboratorio": "externo", "aves_camion": None,
    "cap_camion_producto_t": None, "dist_producto_km": None,
}
# Referencia de trabajo por escala (09A §4; NO es decisión, DEC-037)
AUTO_REFERENCIA = {2500: "manual", 5000: "mecanizado", 10000: "semiautomatico", 20000: "automatico"}

OPCIONES = {
    "turnos": MODOS_TURNO, "automatizacion": NIVELES_AUTO, "config": ("A", "B", "C"),
    "flota_propia": (False, True), "limpieza": ("propia", "tercerizada", "hibrida"),
    "mantenimiento": ("propio", "tercerizado", "mixto"), "productividad": PROD,
    "ventana": (None, "optimista", "media", "conservadora"), "dias_semana": (5, 6),
    "planta_propia": (True, False), "abastecimiento": ("integracion", "compra"),
    "laboratorio": ("externo", "propio"),
}


# ---------------------------------------------------------------------------
# 2. UTILIDADES
# ---------------------------------------------------------------------------
def banda(E):
    for nombre, tope in BANDAS:
        if E < tope:
            return nombre
    raise ErrorRRHH("banda")


def nivel_area(area, auto):
    """Nivel de automatización de un área para el escenario (09A/08 §1)."""
    t = NIVEL_OBJETIVO[auto]
    tabla = {
        "recepcion": ("M", "M", "S", "A"), "faena": ("M", "Mc", "S", "A"), "evisceracion": ("M", "M", "S", "A"),
        "clasificacion": ("M", "M", "S", "A"), "trozado": ("M", "Mc", "S", "A"), "deshuese": ("M", "M", "S", "A"),
        "empaque": ("M", "Mc", "S", "A"), "subproductos": ("M", "S", "S", "A"),
    }
    return tabla[area][t]


def techo(x):
    return int(math.ceil(x - 1e-9))


def validar(e):
    for k in ESCENARIO_BASE:
        if k not in e:
            raise ErrorRRHH(f"Falta la entrada {k}")
    for k, ops in OPCIONES.items():
        if e[k] not in ops:
            raise ErrorRRHH(f"{k}={e[k]!r} fuera de {ops}")
    E, h = e["aves_dia"], e["horas_netas"]
    if not isinstance(E, (int, float)) or E <= 0:
        raise ErrorRRHH("aves_dia debe ser > 0")
    if not isinstance(h, (int, float)) or not 0 < h <= 24:
        raise ErrorRRHH("horas_netas debe estar en (0, 24]")
    for k in ("aves_camion", "cap_camion_producto_t", "dist_producto_km"):
        if e[k] is not None and (not isinstance(e[k], (int, float)) or e[k] <= 0):
            raise ErrorRRHH(f"{k} debe ser None (PENDIENTE) o > 0")


# ---------------------------------------------------------------------------
# 3. INSUMOS DE OTROS MÓDULOS (sólo lectura; cacheados)
# ---------------------------------------------------------------------------
@lru_cache(maxsize=None)
def kg_ave(config):
    kg, _ = mc.kg_ave_config(config)
    return {k: v for k, (v, _) in kg.items()}


@lru_cache(maxsize=None)
def m2_proceso(E, h, config, auto12c, nivel12c):
    e = ms.entradas_por_defecto()
    e.update({"aves_dia": E, "horas_netas": h, "config": config, "automatizacion": auto12c})
    return ms.calcular(e).totales[nivel12c]["proceso"]


@lru_cache(maxsize=None)
def logistica_vivo(E, dias, h, aves_camion):
    r = ml.aves_vivas(E, dias_semana=dias, aves_camion=aves_camion, radio_km=P["radio_km_escenario"],
                      horas_netas=h, plazas_granja=P["plazas_granja"])
    return {"flota_minima": r["flota_minima"], "granjas_equivalentes": r["granjas_equivalentes"],
            "viajes_dia": r["viajes_dia"]}


@lru_cache(maxsize=None)
def logistica_producto(E, dias, config, cap, dist):
    r = ml.producto(E, dias_semana=dias, config=config, cap_refrigerado=cap, cap_congelado=cap, dist_km=dist)
    cd = [r.get("refrigerado_camion_dia"), r.get("congelado_camion_dia")]
    return None if any(x is None for x in cd) else sum(cd)


@lru_cache(maxsize=None)
def equipos():
    with open(CSV_EQUIPOS, newline="", encoding="utf-8") as f:
        return tuple(csv.DictReader(f))


def _opciones(txt):
    return {p for p in txt.split("/") if p in ORDEN_NIVEL}


def nivel_efectivo_equipo(fila, auto):
    """Nivel del equipo bajo el escenario: la opción técnica más cercana por debajo del objetivo
    (unión de opciones de la matriz en todas las escalas); si no hay ninguna, la mínima disponible."""
    ops = set()
    for E in ESCALAS:
        ops |= _opciones(fila[f"nivel_{E}"])
    if not ops:
        return None
    t = NIVEL_OBJETIVO[auto]
    debajo = [o for o in ops if ORDEN_NIVEL[o] <= t]
    return max(debajo, key=ORDEN_NIVEL.get) if debajo else min(ops, key=ORDEN_NIVEL.get)


def presente(fila, E):
    """Equipo presente a la escala E: se usa la columna de la mayor escala de referencia ≤ E."""
    ref = max([x for x in ESCALAS if x <= E] or [ESCALAS[0]])
    return bool(_opciones(fila[f"nivel_{ref}"]))      # '—', 'O' (opcional) y 'T' (tercerizar) no cuentan


def carga_mantenimiento(E, ritmo, auto, prod):
    """Horas-técnico por semana por activos (08_maquinaria/matriz_equipos.csv). [ESTIMACIÓN] con SUP-14A-09."""
    total, n_eq, por_nivel = 0.0, 0, {"M": 0, "Mc": 0, "S": 0, "A": 0}
    for f in equipos():
        if not presente(f, E):
            continue
        niv = nivel_efectivo_equipo(f, auto)
        if niv is None:
            continue
        crit = "CRÍTICO" if f["criticidad"].startswith("CRÍTICO") else f["criticidad"].split(" ")[0]
        unidades = techo(ritmo / P["unidades_duplicables_aves_h"]) if f["modularidad"].startswith("Duplicar") else 1
        unidades = max(unidades, 1)
        total += P["mant_h_semana_equipo"][niv][prod] * P["mant_peso_criticidad"].get(crit, 1.0) * unidades
        n_eq += unidades
        por_nivel[niv] += unidades
    return total, n_eq, por_nivel


# ---------------------------------------------------------------------------
# 4. TURNOS Y JORNADA (integra la ecuación de 24 h de 09A)
# ---------------------------------------------------------------------------
def turnos_y_jornada(e):
    h, modo = e["horas_netas"], e["turnos"]
    vent = e["ventana"] or VENTANA_POR_PROD[e["productividad"]]
    v = mc.VENTANAS[vent]
    D = mc.SENSIBILIDAD[v["sens"]]["D"]
    n_c = CUADRILLAS[modo]
    h_c = h / n_c
    presencia = h_c / D + v["pausas_8h"] * h_c / 8 + v["limpieza_intermedia_8h"] * h_c / 8
    if n_c == 2:
        presencia += P["solape_cambio_turno_h"]
    v24 = mc.ventana_24h(h, vent, turnos=n_c)
    hs = P["horas_semana_normal"][e["productividad"]]
    dias = e["dias_semana"]
    extra_sem = max(0.0, presencia * dias - hs, (presencia - P["jornada_normal_h"]) * dias)
    extra_mes = extra_sem * 52 / 12
    alertas = []
    if v24["alerta"]:
        alertas.append(f"ALERTA_24H(holgura {v24['holgura']:.2f} h)")
    if modo in ("1", "2") and presencia > P["jornada_normal_h"] + 1e-9:
        alertas.append(f"ALERTA_JORNADA(presencia {presencia:.2f} h > {P['jornada_normal_h']:.0f} h)")
    if modo == "extendido":
        if presencia > P["jornada_extendida_max_h"] + 1e-9:
            alertas.append(f"ALERTA_JORNADA_EXTENDIDA(presencia {presencia:.2f} h > {P['jornada_extendida_max_h']:.0f} h)")
        if extra_mes > P["horas_extra_mes_ref"] + 1e-9:
            alertas.append(f"ALERTA_HORAS_EXTRA({extra_mes:.0f} h/mes > ref. {P['horas_extra_mes_ref']:.0f})")
    if modo == "extendido" and presencia <= P["jornada_normal_h"] + 1e-9:
        alertas.append("NOTA_EXTENDIDO_INNECESARIO(cabe en jornada normal)")
    comp = v24["componentes"]
    fuera_prod = sum(comp[k] for k in ("preparacion_arranque", "cierre_vaciado", "limpieza", "sanitizacion",
                                       "mantenimiento"))
    return {
        "ventana": vent, "D": D, "cuadrillas": n_c, "h_netas_cuadrilla": h_c, "presencia_h": presencia,
        "horas_extra_semana": extra_sem, "horas_extra_mes": extra_mes, "holgura_24h": v24["holgura"],
        "total_24h": v24["total"], "alerta_24h": v24["alerta"], "alertas": alertas,
        "t_limpieza": comp["limpieza"], "t_sanitizacion": comp["sanitizacion"], "t_mantenimiento": comp["mantenimiento"],
        "horas_produccion_planta": presencia * n_c - (P["solape_cambio_turno_h"] if n_c == 2 else 0.0),
        "horas_fuera_produccion": fuera_prod, "horas_semana_normal": hs,
    }


# ---------------------------------------------------------------------------
# 5. CONSTRUCCIÓN DE PUESTOS
# ---------------------------------------------------------------------------
def _puesto(lista, clave, puesto, categoria, grupo, zona, modalidad, por_turno=None, cuadrillas=1,
            equivalentes=None, personas=None, interno=True, externos=0.0, contrato="convenio_pendiente",
            estado="CALCULADO", base="", ref=""):
    lista.append({
        "clave": clave, "puesto": puesto, "categoria": categoria, "grupo": grupo, "zona": zona,
        "modalidad": modalidad, "por_turno": por_turno, "cuadrillas": cuadrillas, "personas": personas,
        "equivalentes": equivalentes, "interno": interno, "externos_equivalentes": externos,
        "contrato": contrato, "estado": estado, "base": base, "ref": ref,
    })


def calcular(entradas=None):
    e = dict(ESCENARIO_BASE)
    if entradas:
        e.update(entradas)
    validar(e)
    E, h, pr, auto, cfg = e["aves_dia"], e["horas_netas"], e["productividad"], e["automatizacion"], e["config"]
    b = banda(E)
    tj = turnos_y_jornada(e)
    n_c, pres, dias, hs = tj["cuadrillas"], tj["presencia_h"], e["dias_semana"], tj["horas_semana_normal"]
    cob = P["factor_cobertura"][pr]
    r = E / h                                            # ritmo de línea mientras corre (aves/h)
    k = kg_ave(cfg)
    lst = []
    pendientes = []

    def turno(clave, puesto, cat, grupo, zona, pt, interno=True, base="", ref="", contrato="convenio_pendiente"):
        """Puesto por cuadrilla: personas físicas y equivalentes por horas."""
        if interno:
            pers = techo(pt * n_c * cob) if pt > 0 else 0
            eq = pt * n_c * pres * dias / hs * cob
            _puesto(lst, clave, puesto, cat, grupo, zona, "turno", pt, n_c, eq, pers, True, 0.0, contrato,
                    base=base, ref=ref)
        else:
            eq = pt * n_c * pres * dias / hs * cob
            _puesto(lst, clave, puesto, cat, grupo, zona, "turno", 0, n_c, 0.0, 0, False, eq, "servicio_tercerizado",
                    base=base, ref=ref)

    def estructura(clave, puesto, cat, grupo, zona, eq, contrato="fuera_convenio", nota="", interno=True, ext=0.0):
        pers = int(math.floor(eq + 1e-9)) if eq > 0 else 0       # fracciones → "roles compartidos" (5.10)
        _puesto(lst, clave, puesto, cat, grupo, zona, "estructura", None, 1, eq if interno else 0.0,
                pers if interno else 0, interno, ext, contrato, base=nota)

    planta = e["planta_propia"]
    # ---------------- 5.1 Operación industrial (directos) ----------------
    t_com_dia = k["comestible_a_empaque"] * E / 1000
    t_sol_dia = k["solidos_a_retirar"] * E / 1000
    nr = {a: nivel_area(a, auto) for a in ("recepcion", "faena", "evisceracion", "clasificacion", "trozado",
                                           "deshuese", "empaque", "subproductos")}
    ops = []
    ops.append(("recepcion_colgado", "Recepción, descarga y colgado", "sucia",
                techo(1 + (P["colgado_por_1000"][pr] + P["descarga_por_1000"][nr["recepcion"] if nr["recepcion"] != "Mc" else "M"][pr]) * r / 1000),
                f"nivel {nr['recepcion']}; colgado FTE-219 [PVDP·débil]/SUP-063"))
    ops.append(("faena", "Faena (aturdido–desplumado, patas, transferencia)", "sucia",
                techo(1 + P["faena_por_1000"][nr["faena"]][pr] * r / 1000), f"nivel {nr['faena']}; aturdido–desplumado continuo Mc/A en todos los casos (09A)"))
    ops.append(("evisceracion", "Evisceración, menudencias y lavado (sin inspección oficial)", "evisceracion",
                techo(P["evisc_fijo"][nr["evisceracion"]] + P["evisc_por_1000"][nr["evisceracion"]][pr] * r / 1000),
                f"nivel {nr['evisceracion']}; manual FTE-218 [PVDP·débil]"))
    ops.append(("enfriamiento_clasificacion", "Enfriamiento y clasificación", "limpia",
                techo(1 + P["clasif_por_1000"][nr["clasificacion"] if nr["clasificacion"] != "Mc" else "M"][pr] * r / 1000),
                f"nivel {nr['clasificacion']}"))
    kg_troz_h = k["a_trozado"] * r
    kg_desh_h = k["a_deshuese"] * r
    nt = nr["trozado"]
    ops.append(("trozado", "Trozado", "limpia",
                techo(1 + kg_troz_h / P["trozado_kg_h"][nt][pr]) if kg_troz_h > 0 else 0,
                f"nivel {nt}; {kg_troz_h:.0f} kg/h (config. {cfg})"))
    nd = nr["deshuese"]
    ops.append(("deshuese", "Deshuese y trimming", "limpia",
                techo(1 + kg_desh_h / P["deshuese_kg_h"][nd][pr]) if kg_desh_h > 0 else 0,
                f"nivel {nd}; {kg_desh_h:.0f} kg/h (config. {cfg})"))
    ne = nr["empaque"]
    ops.append(("empaque", "Empaque, rotulado y control de peso", "limpia",
                techo(1 + k["comestible_a_empaque"] * r / P["empaque_kg_h"][ne][pr]), f"nivel {ne}"))
    ops.append(("camaras_expedicion", "Cámaras, congelado y expedición (carga)", "frio_expedicion",
                techo(1 + t_com_dia / n_c / P["camaras_t_persona_turno"][pr]), f"{t_com_dia:.1f} t/día"))
    ns = nr["subproductos"] if nr["subproductos"] != "Mc" else "S"
    ops.append(("subproductos", "Subproductos y decomisos (manejo y despacho)", "subproductos",
                max(1, techo(t_sol_dia / n_c / P["subprod_t_persona_turno"][ns][pr])), f"{t_sol_dia:.1f} t/día; nivel {ns}"))
    for clave, nombre, zona, pt, base in ops:
        turno(clave, nombre, "operacion_industrial", "directo", zona, pt, interno=planta, base=base,
              ref="SUP-14A-04/05")
    directos_turno = sum(o[3] for o in ops) if planta else 0

    # ---------------- 5.2 Limpieza y sanitización (función crítica) ----------------
    if planta:
        pt_lo = techo(1 + P["limpieza_operativa_por_1000"][pr] * r / 1000)
        turno("limpieza_operativa", "Limpieza operativa en turno", "operacion_industrial", "soporte", "transversal",
              pt_lo, base="durante producción; siempre interna", ref="SUP-14A-06")
        m2 = m2_proceso(E, h, cfg, AUTO_12C[auto], AREA_12C_POR_PROD[pr])
        ph = m2 * P["limpieza_factor_auto"][auto] / P["limpieza_m2_persona_h"][pr]
        ventana_l = tj["t_limpieza"] + tj["t_sanitizacion"]
        cuadrilla_l = techo(ph / ventana_l)
        eq_l = cuadrilla_l * ventana_l * dias / hs * cob
        pers_l = techo(cuadrilla_l * cob)
        modo_l = e["limpieza"]
        frac_int = {"propia": 1.0, "tercerizada": 0.0, "hibrida": P["limpieza_hibrida_interna"]}[modo_l]
        cu_int = techo(cuadrilla_l * frac_int) if frac_int > 0 else 0
        cu_ext = cuadrilla_l - cu_int
        base_l = f"{m2:.0f} m² proceso (12C) × {ph / max(m2, 1):.3f} persona-h/m²; ventana {ventana_l:.2f} h"
        _puesto(lst, "limpieza_sanitizacion", "Limpieza y sanitización post-producción (cuadrilla)",
                "operacion_industrial", "soporte", "transversal", "cuadrilla_post", cu_int, 1,
                eq_l * cu_int / cuadrilla_l if cuadrilla_l else 0.0, techo(cu_int * cob) if cu_int else 0,
                cu_int > 0, eq_l * cu_ext / cuadrilla_l if cuadrilla_l else 0.0,
                "convenio_pendiente" if cu_int else "servicio_tercerizado", base=base_l, ref="SUP-14A-06; DPV-091")
        lider = 1 if (cu_int >= 6 or modo_l != "propia") else 0
        estructura("supervisor_saneamiento", "Supervisor de saneamiento / verificación POES", "operacion_industrial",
                   "supervision", "transversal", lider, nota="interno aun si la limpieza se terceriza (verificación)")
        pers_limp_total = pers_l
    else:
        pers_limp_total = 0

    # ---------------- 5.3 Supervisión de línea ----------------
    if planta:
        span = P["span_supervision"][pr]
        sup_c = max(1, techo(directos_turno / span))
        turno("supervisores_linea", "Supervisores de línea", "operacion_industrial", "supervision", "transversal",
              sup_c, ref="SUP-14A-07", contrato="fuera_convenio")
        if n_c == 2:
            turno("jefes_turno", "Jefe de turno", "operacion_industrial", "supervision", "transversal", 1,
                  ref="SUP-14A-07", contrato="fuera_convenio")
        estructura("jefe_produccion", *ESTRUCTURA["jefe_produccion"][:4], ESTRUCTURA["jefe_produccion"][4][b])
    else:
        sup_c = 0

    # ---------------- 5.4 Calidad e inocuidad ----------------
    if planta:
        pt_q = techo(1 + P["control_calidad_por_1000"][pr] * r / 1000)
        turno("control_calidad", "Control de calidad operativo (recepción, línea, empaque)", "soporte_industrial",
              "soporte", "transversal", pt_q, ref="SUP-14A-08")
    else:
        estructura("control_calidad_facon", "Control de calidad propio en la planta del façonier",
                   "soporte_industrial", "soporte", "externo_facon", 1 if b in ("S", "M") else 2,
                   contrato="convenio_pendiente", nota="asset-light: la empresa conserva el control de especificaciones")
    for kk in ("jefe_calidad", "analista_appcc", "trazabilidad"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5], nota=x[6])
    if e["laboratorio"] == "propio" and planta:
        estructura("laboratorio", "Analistas de laboratorio propio", "soporte_industrial", "soporte", "laboratorio",
                   LAB_PROPIO[b], contrato="convenio_pendiente")
    else:
        estructura("laboratorio", "Laboratorio de autocontrol (externo; toma de muestras interna)", "soporte_industrial",
                   "soporte", "laboratorio", 0, interno=False, ext=0.0)
        lst[-1]["estado"] = "EXTERNO_SIN_DOTACION"
    _puesto(lst, "inspeccion_oficial", "Inspección veterinaria oficial (SENASA) y eventuales auxiliares",
            "soporte_industrial", "soporte", "evisceracion", "externo_oficial", PENDIENTE, n_c, 0.0, 0, False,
            PENDIENTE, "oficial", estado="PENDIENTE", base="puestos por velocidad de línea sin norma leída",
            ref="DPV-090; DPV-14A-05")
    if planta:
        pendientes.append("inspeccion_oficial")

    # ---------------- 5.5 Mantenimiento y utilities ----------------
    if planta:
        carga_h, n_eq, por_niv = carga_mantenimiento(E, r, auto, pr)
        fte_carga = carga_h / P["mant_h_productivas_tecnico"][pr]
        simult = 1 + (E >= 5000) + (E >= 10000) + (auto == "automatico" and E >= 10000)
        cov_h = dias * (tj["horas_produccion_planta"] * simult + tj["horas_fuera_produccion"] * 1)
        fte_cov = cov_h / hs * cob
        modo_m = e["mantenimiento"]
        tecnicos_tot = max(fte_cov, fte_carga)
        if modo_m == "propio":
            int_eq, ext_eq = tecnicos_tot, 0.0
        elif modo_m == "tercerizado":
            int_eq, ext_eq = 0.0, tecnicos_tot
        else:                                         # mixto: cobertura interna + especialidades externas
            int_eq, ext_eq = fte_cov, max(0.0, fte_carga - fte_cov)
        base_m = (f"{n_eq} equipos ({por_niv['Mc']} Mc, {por_niv['S']} S, {por_niv['A']} A); carga {carga_h:.0f} h/sem; "
                  f"cobertura {simult} técnico(s) simultáneo(s) en producción")
        _puesto(lst, "tecnicos_mantenimiento", "Técnicos de mantenimiento (mecánica, electricidad, frío/utilities, automatización)",
                "soporte_industrial", "soporte", "transversal", "cobertura", simult if int_eq else 0, 1, int_eq,
                techo(int_eq) if int_eq else 0, int_eq > 0, ext_eq,
                "convenio_pendiente" if int_eq else "servicio_tercerizado", base=base_m, ref="SUP-14A-09")
        lst[-1]["fte_carga"] = fte_carga
        lst[-1]["fte_cobertura"] = fte_cov
        x = ESTRUCTURA["jefe_mantenimiento"]
        jm = x[4][b] if modo_m != "tercerizado" else max(x[4][b], 0.5)
        estructura("jefe_mantenimiento", x[0] if modo_m != "tercerizado" else "Coordinador de mantenimiento y contratos",
                   *x[1:4], jm, nota="función retenida aun si se terceriza")
        x = ESTRUCTURA["panolero"]
        estructura("panolero", *x[:4], x[4][b] if modo_m != "tercerizado" else 0, contrato=x[5])
    else:
        fte_carga = fte_cov = 0.0
        n_eq = 0

    # ---------------- 5.6 Otros servicios de soporte ----------------
    for kk in ("hys", "lavanderia"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b] if planta else 0, contrato=x[5], nota=x[6])
    _puesto(lst, "hys_externo", "Servicio externo de higiene y seguridad y medicina laboral", "soporte_industrial",
            "soporte", "transversal", "externo", PENDIENTE, 1, 0.0, 0, False, PENDIENTE, "servicio_tercerizado",
            estado="PENDIENTE", base="horas-profesional según norma no leída", ref="DPV-14A-07; FTE-14A-004")
    pendientes.append("hys_externo")

    # ---------------- 5.7 Logística ----------------
    for kk in ("planificacion_trafico", "deposito_insumos", "expedicion_adm"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5])
    ac = e["aves_camion"]
    if ac is None:
        _puesto(lst, "choferes_aves", "Choferes de aves vivas", "logistica", "soporte", "ruta", "flota",
                PENDIENTE, 1, PENDIENTE if e["flota_propia"] else 0.0, PENDIENTE if e["flota_propia"] else 0,
                e["flota_propia"], PENDIENTE if not e["flota_propia"] else 0.0, "convenio_pendiente",
                estado="PENDIENTE", base="capacidad de camión no elegida (DPV-084)", ref="DPV-084; DEC-056")
        pendientes.append("choferes_aves")
    else:
        lv = logistica_vivo(E, dias, h, ac)
        fl = lv["flota_minima"]
        eq_ch = fl * cob
        _puesto(lst, "choferes_aves", "Choferes de aves vivas", "logistica", "soporte", "ruta", "flota", fl, 1,
                eq_ch if e["flota_propia"] else 0.0, techo(eq_ch) if e["flota_propia"] else 0, e["flota_propia"],
                0.0 if e["flota_propia"] else eq_ch, "CCT 40/89 [PVDP]" if e["flota_propia"] else "servicio_tercerizado",
                base=f"flota mínima {fl} (12B; {ac} aves/camión de ESCENARIO, radio {P['radio_km_escenario']} km)",
                ref="SUP-033; SUP-14A-11")
    cap, dist = e["cap_camion_producto_t"], e["dist_producto_km"]
    cd = logistica_producto(E, dias, cfg, cap, dist) if (cap and dist) else None
    if cd is None:
        _puesto(lst, "choferes_producto", "Choferes de producto terminado", "logistica", "soporte", "ruta", "flota",
                PENDIENTE, 1, PENDIENTE if e["flota_propia"] else 0.0, PENDIENTE if e["flota_propia"] else 0,
                e["flota_propia"], PENDIENTE if not e["flota_propia"] else 0.0, "convenio_pendiente",
                estado="PENDIENTE", base="capacidad, distancia y modelo de distribución no definidos",
                ref="DPV-084; DPV-036; DEC-016; DEC-056")
        pendientes.append("choferes_producto")
    else:
        n_ch = techo(cd)
        eq_ch = n_ch * cob
        _puesto(lst, "choferes_producto", "Choferes de producto terminado", "logistica", "soporte", "ruta", "flota",
                n_ch, 1, eq_ch if e["flota_propia"] else 0.0, techo(eq_ch) if e["flota_propia"] else 0,
                e["flota_propia"], 0.0 if e["flota_propia"] else eq_ch, "CCT 40/89 [PVDP]",
                base=f"{cd:.2f} camión-día (12B, capacidad {cap} t y {dist} km de ESCENARIO)", ref="SUP-14A-11")
    _puesto(lst, "captura", "Cuadrillas de captura y carga en granja", "logistica", "soporte", "granja", "externo",
            PENDIENTE, 1, 0.0, 0, False, PENDIENTE, "servicio_tercerizado", estado="PENDIENTE",
            base="función del integrado o contratista; dotación no modelada", ref="DPV-14A-09")
    pendientes.append("captura")

    # ---------------- 5.8 Producción primaria (sólo coordinación) ----------------
    if e["abastecimiento"] == "integracion":
        for kk, (nombre, tabla) in PRIMARIA.items():
            estructura(kk, nombre, "produccion_primaria", "soporte", "campo", tabla[b], nota="no incluye personal de granjas de terceros")
        lv = logistica_vivo(E, dias, h, ac or P["aves_camion_escenario"])
        gr = lv["granjas_equivalentes"]
        estructura("tecnicos_campo", "Técnicos de campo (asistencia a integrados)", "produccion_primaria", "soporte",
                   "campo", techo(gr / P["granjas_por_tecnico"][pr]),
                   nota=f"{gr:.1f} granjas equivalentes de {P['plazas_granja']} plazas (12B/03)")
    else:
        for kk, (nombre, tabla) in PRIMARIA_COMPRA.items():
            estructura(kk, nombre, "produccion_primaria", "soporte", "campo", tabla[b])

    # ---------------- 5.9 Administración y dirección ----------------
    for kk in ("compras", "ventas", "administracion", "finanzas", "sistemas"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5], nota=x[6])
    for kk in ("gerente_general", "gerente_operaciones", "gerente_comercial", "gerente_adm_fin", "gerente_calidad"):
        x = ESTRUCTURA[kk]
        val = x[4][b] if (planta or kk != "gerente_operaciones") else 0
        if kk == "gerente_calidad" and not planta:
            val = 0
        estructura(kk, *x[:4], val, contrato=x[5], nota=x[6])
    # RR. HH. al final: depende de las personas internas (sin incluirse)
    pers_previas = sum((p["personas"] or 0) + ((p["equivalentes"] or 0) - (p["personas"] or 0)
                       if p["modalidad"] == "estructura" else (p["personas"] or 0)) for p in lst if p["interno"])
    rrhh = max(0.5, pers_previas / P["personas_por_rrhh"][pr])
    rrhh = math.ceil(rrhh * 2 - 1e-9) / 2                       # medios puestos
    estructura("rrhh", "Recursos humanos (liquidación, selección, capacitación)", "administracion",
               "administracion", "oficinas", rrhh, nota="liquidación externa posible en 2.500")

    # ---------------- 5.10 Roles compartidos: las fracciones de puestos de estructura se suman por
    # categoría y se redondean hacia arriba una sola vez (no se infla la estructura chica)
    fr = {}
    for p in lst:
        if p["modalidad"] == "estructura" and p["interno"] and p["equivalentes"]:
            f = p["equivalentes"] - p["personas"]
            if f > 1e-9:
                fr.setdefault((p["categoria"], p["grupo"]), []).append(p["clave"])
    for (cat, grupo), claves in sorted(fr.items()):
        suma = sum(p["equivalentes"] - p["personas"] for p in lst if p["clave"] in claves and p["categoria"] == cat)
        _puesto(lst, f"compartidos_{cat}_{grupo}", f"Roles compartidos ({', '.join(claves)})", cat, grupo,
                "oficinas", "compartido", None, 1, 0.0, techo(suma), True, 0.0, "fuera_convenio",
                base=f"Σ fracciones = {suma:.2f} equivalentes (ya contados en cada rol)")
    # ---------------- 5.11 Agregados ----------------
    out = agregar(lst, e, tj, r, k, pendientes)
    out.update({"entradas": e, "banda": b, "ritmo": r, "turnos": tj, "puestos": lst,
                "mant_fte_carga": fte_carga, "mant_fte_cobertura": fte_cov, "mant_equipos": n_eq,
                "pers_limpieza_cuadrilla": pers_limp_total})
    return out


def agregar(lst, e, tj, r, k, pendientes):
    E = e["aves_dia"]
    g_pers = {g: 0 for g in GRUPOS}
    g_eq = {g: 0.0 for g in GRUPOS}
    ext = 0.0
    zonas = {}
    cat_eq = {}
    por_turno_planta = 0.0
    for p in lst:
        if p["interno"] and p["personas"] is not None:
            g_pers[p["grupo"]] += p["personas"]
            g_eq[p["grupo"]] += p["equivalentes"] or 0.0
            cat_eq[p["categoria"]] = cat_eq.get(p["categoria"], 0.0) + (p["equivalentes"] or 0.0)
        if p["externos_equivalentes"]:
            ext += p["externos_equivalentes"]
        if p["modalidad"] == "turno" and p["interno"] and p["por_turno"]:
            zonas[p["zona"]] = zonas.get(p["zona"], 0) + p["por_turno"]
            por_turno_planta += p["por_turno"]
        if p["modalidad"] == "cobertura" and p["interno"] and p["por_turno"]:
            zonas["transversal"] = zonas.get("transversal", 0) + p["por_turno"]
            por_turno_planta += p["por_turno"]
    tot_pers = sum(g_pers.values())
    tot_eq = sum(g_eq.values())
    directos_turno = sum(p["por_turno"] for p in lst if p["grupo"] == "directo" and p["interno"] and p["por_turno"])
    sup_turno = sum(p["por_turno"] for p in lst if p["clave"] in ("supervisores_linea", "jefes_turno") and p["interno"])
    hp_dir = directos_turno * tj["cuadrillas"] * tj["presencia_h"]
    kg_com = k["comestible_a_empaque"] * E
    tecnicos = [p for p in lst if p["clave"] == "tecnicos_mantenimiento"]
    tec_tot = (tecnicos[0]["equivalentes"] or 0) + (tecnicos[0]["externos_equivalentes"] or 0) if tecnicos else 0.0
    n_eq = None
    for p in tecnicos:
        n_eq = p["base"].split(" ")[0]
    hp_total_dia = tot_eq * tj["horas_semana_normal"] / e["dias_semana"]
    kpi = {
        "aves_persona_h_directa": E / hp_dir if hp_dir else None,
        "kg_persona_h_directa": kg_com / hp_dir if hp_dir else None,
        "aves_persona_h_total": E / hp_total_dia if hp_total_dia else None,
        "personas_por_1000_aves": tot_pers / (E / 1000),
        "directos_por_1000_aves": g_pers["directo"] / (E / 1000),
        "ratio_indirecta_directa": (tot_eq - g_eq["directo"]) / g_eq["directo"] if g_eq["directo"] else None,
        "directos_por_supervisor": directos_turno / sup_turno if sup_turno else None,
        "equipos_por_tecnico": (float(n_eq) / tec_tot) if (n_eq and tec_tot) else None,
    }
    return {
        "personas": g_pers, "equivalentes": g_eq, "total_personas": tot_pers, "total_equivalentes": tot_eq,
        "indirectos_equivalentes": tot_eq - g_eq["directo"], "externos_equivalentes": ext,
        "por_turno_planta": por_turno_planta, "directos_turno": directos_turno, "zonas_turno": zonas,
        "categorias_eq": cat_eq, "kpi": kpi, "pendientes": sorted(set(pendientes)),
        "estado": "INCOMPLETO" if pendientes else "COMPLETO",
    }


# ---------------------------------------------------------------------------
# 6. ESCENARIOS Y CSV
# ---------------------------------------------------------------------------
MODOS_HORAS = (("1", 6.0), ("1", 8.0), ("extendido", 8.0), ("extendido", 10.0), ("2", 12.0), ("2", 16.0))
CAMPOS = [
    "id", "aves_dia", "horas_netas", "turnos", "cuadrillas", "automatizacion", "config", "flota_propia",
    "limpieza", "mantenimiento", "productividad", "ventana", "dias_semana", "planta_propia", "abastecimiento",
    "laboratorio", "banda", "ritmo_aves_h", "presencia_cuadrilla_h", "horas_extra_mes_persona", "holgura_24h",
    "alertas", "directos_por_turno", "personas_por_turno_planta", "zona_sucia_turno", "zona_evisceracion_turno",
    "zona_limpia_turno", "zona_frio_expedicion_turno", "zona_subproductos_turno", "zona_transversal_turno",
    "directos_personas", "supervision_personas", "soporte_personas", "administracion_personas",
    "direccion_personas", "total_personas_internas", "directos_eq", "indirectos_eq", "supervision_eq",
    "soporte_eq", "administracion_eq", "direccion_eq", "total_equivalentes_internos", "externos_equivalentes",
    "eq_operacion_industrial", "eq_soporte_industrial", "eq_logistica", "eq_produccion_primaria",
    "eq_administracion", "eq_direccion", "mant_fte_carga", "mant_fte_cobertura",
    "aves_persona_h_directa", "kg_persona_h_directa", "aves_persona_h_total", "personas_por_1000_aves",
    "ratio_indirecta_directa", "directos_por_supervisor", "equipos_por_tecnico", "proxy_12C_turno_medio",
    "pendientes", "estado", "clasificacion",
]


def _r(x, d=3):
    return "" if x is None else round(x, d)


def proxy_12c(E, h, auto, cfg):
    """Dotación proxy por turno de 12C (SUP-116) — sólo para comparar; no se usa."""
    v = ms.P
    ritmo = E / h
    a = AUTO_12C[auto]
    return (v["dotacion_base_proxy"]["v"][1] + v["dotacion_por_ave_h_proxy"]["v"][1] * ritmo
            * v["factor_dotacion_automatizacion"][a] * v["factor_dotacion_config"][cfg])


def fila_csv(i, R):
    e, tj, kp, z = R["entradas"], R["turnos"], R["kpi"], R["zonas_turno"]
    ce = R["categorias_eq"]
    return {
        "id": i, "aves_dia": e["aves_dia"], "horas_netas": e["horas_netas"], "turnos": e["turnos"],
        "cuadrillas": tj["cuadrillas"], "automatizacion": e["automatizacion"], "config": e["config"],
        "flota_propia": int(e["flota_propia"]), "limpieza": e["limpieza"], "mantenimiento": e["mantenimiento"],
        "productividad": e["productividad"], "ventana": tj["ventana"], "dias_semana": e["dias_semana"],
        "planta_propia": int(e["planta_propia"]), "abastecimiento": e["abastecimiento"],
        "laboratorio": e["laboratorio"], "banda": R["banda"], "ritmo_aves_h": _r(R["ritmo"], 1),
        "presencia_cuadrilla_h": _r(tj["presencia_h"], 2), "horas_extra_mes_persona": _r(tj["horas_extra_mes"], 1),
        "holgura_24h": _r(tj["holgura_24h"], 2), "alertas": ";".join(tj["alertas"]),
        "directos_por_turno": R["directos_turno"], "personas_por_turno_planta": _r(R["por_turno_planta"], 1),
        "zona_sucia_turno": z.get("sucia", 0), "zona_evisceracion_turno": z.get("evisceracion", 0),
        "zona_limpia_turno": z.get("limpia", 0), "zona_frio_expedicion_turno": z.get("frio_expedicion", 0),
        "zona_subproductos_turno": z.get("subproductos", 0), "zona_transversal_turno": z.get("transversal", 0),
        "directos_personas": R["personas"]["directo"], "supervision_personas": R["personas"]["supervision"],
        "soporte_personas": R["personas"]["soporte"], "administracion_personas": R["personas"]["administracion"],
        "direccion_personas": R["personas"]["direccion"], "total_personas_internas": R["total_personas"],
        "directos_eq": _r(R["equivalentes"]["directo"], 2), "indirectos_eq": _r(R["indirectos_equivalentes"], 2),
        "supervision_eq": _r(R["equivalentes"]["supervision"], 2), "soporte_eq": _r(R["equivalentes"]["soporte"], 2),
        "administracion_eq": _r(R["equivalentes"]["administracion"], 2),
        "direccion_eq": _r(R["equivalentes"]["direccion"], 2),
        "total_equivalentes_internos": _r(R["total_equivalentes"], 2),
        "externos_equivalentes": _r(R["externos_equivalentes"], 2),
        "eq_operacion_industrial": _r(ce.get("operacion_industrial", 0.0), 2),
        "eq_soporte_industrial": _r(ce.get("soporte_industrial", 0.0), 2),
        "eq_logistica": _r(ce.get("logistica", 0.0), 2), "eq_produccion_primaria": _r(ce.get("produccion_primaria", 0.0), 2),
        "eq_administracion": _r(ce.get("administracion", 0.0), 2), "eq_direccion": _r(ce.get("direccion", 0.0), 2),
        "mant_fte_carga": _r(R["mant_fte_carga"], 2), "mant_fte_cobertura": _r(R["mant_fte_cobertura"], 2),
        "aves_persona_h_directa": _r(kp["aves_persona_h_directa"], 1), "kg_persona_h_directa": _r(kp["kg_persona_h_directa"], 1),
        "aves_persona_h_total": _r(kp["aves_persona_h_total"], 1), "personas_por_1000_aves": _r(kp["personas_por_1000_aves"], 2),
        "ratio_indirecta_directa": _r(kp["ratio_indirecta_directa"], 3),
        "directos_por_supervisor": _r(kp["directos_por_supervisor"], 1),
        "equipos_por_tecnico": _r(kp["equipos_por_tecnico"], 1),
        "proxy_12C_turno_medio": _r(proxy_12c(e["aves_dia"], e["horas_netas"], e["automatizacion"], e["config"]), 1)
        if e["planta_propia"] else "",
        "pendientes": ";".join(R["pendientes"]), "estado": R["estado"],
        "clasificacion": "[ESTIMACIÓN]",
    }


def grilla():
    """Grilla de escenarios (independientes). Planta propia: escala × turnos/horas × automatización × mix ×
    limpieza × mantenimiento × flota × productividad. Asset-light: escala × flota × productividad."""
    for E, (modo, h), auto, cfg, limp, mant, flota, pr in itertools.product(
            ESCALAS, MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C"), OPCIONES["limpieza"], OPCIONES["mantenimiento"],
            (False, True), PROD):
        yield {"aves_dia": E, "horas_netas": h, "turnos": modo, "automatizacion": auto, "config": cfg,
               "limpieza": limp, "mantenimiento": mant, "flota_propia": flota, "productividad": pr,
               "aves_camion": P["aves_camion_escenario"]}
    for E, flota, pr in itertools.product(ESCALAS, (False, True), PROD):
        yield {"aves_dia": E, "planta_propia": False, "flota_propia": flota, "productividad": pr,
               "aves_camion": P["aves_camion_escenario"]}


def escribir_csv(ruta=CSV_ESCENARIOS):
    n = 0
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for i, ent in enumerate(grilla(), 1):
            w.writerow(fila_csv(f"RH-{i:05d}", calcular(ent)))
            n += 1
    return n


def escenario_referencia(E, pr="media"):
    """Escenario de trabajo para documentos y plantilla de costo (NO es decisión): 1 cuadrilla de 8 h netas
    en turno extendido, automatización de referencia de 09A, config. B, limpieza y mantenimiento propios,
    flota tercerizada, capacidad de camión de escenario."""
    return {"aves_dia": E, "horas_netas": 8.0, "turnos": "extendido", "automatizacion": AUTO_REFERENCIA[E],
            "config": "B", "productividad": pr, "aves_camion": P["aves_camion_escenario"]}


CAMPOS_PLANTILLA = ["escenario", "PUESTO", "area_categoria", "grupo", "zona", "CANTIDAD", "por_turno",
                    "cuadrillas", "HORAS", "equivalentes", "TIPO_CONTRATO", "interno_externo",
                    "COSTO_EMPRESA_MENSUAL", "COSTO_ANUAL", "moneda", "tipo_cambio_fecha_fuente",
                    "fuente_costo", "estado_costo"]


def escribir_plantilla(ruta=CSV_PLANTILLA):
    n = 0
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_PLANTILLA)
        w.writeheader()
        for E in ESCALAS:
            R = calcular(escenario_referencia(E))
            tj = R["turnos"]
            for p in R["puestos"]:
                if p["modalidad"] in ("turno", "cuadrilla_post"):
                    horas = round(tj["presencia_h"] * R["entradas"]["dias_semana"], 1) if p["modalidad"] == "turno" else \
                        round((tj["t_limpieza"] + tj["t_sanitizacion"]) * R["entradas"]["dias_semana"], 1)
                else:
                    horas = tj["horas_semana_normal"]
                w.writerow({
                    "escenario": f"REF-{E}", "PUESTO": p["puesto"], "area_categoria": p["categoria"],
                    "grupo": p["grupo"], "zona": p["zona"],
                    "CANTIDAD": "PENDIENTE" if p["personas"] is None else p["personas"],
                    "por_turno": "" if p["por_turno"] is None else p["por_turno"], "cuadrillas": p["cuadrillas"],
                    "HORAS": horas, "equivalentes": "" if p["equivalentes"] is None else round(p["equivalentes"], 2),
                    "TIPO_CONTRATO": p["contrato"],
                    "interno_externo": "interno" if p["interno"] else ("externo" if p["estado"] != "PENDIENTE" else "PENDIENTE"),
                    "COSTO_EMPRESA_MENSUAL": "", "COSTO_ANUAL": "", "moneda": "USD", "tipo_cambio_fecha_fuente": "",
                    "fuente_costo": "", "estado_costo": "PENDIENTE DE VALIDACIÓN (DPV-14A-03)",
                })
                n += 1
    return n


# ---------------------------------------------------------------------------
# 7. TESTS
# ---------------------------------------------------------------------------
def _total_func(R):
    return R["total_equivalentes"] + R["externos_equivalentes"]


def ejecutar_tests(verbose=True):
    res = []

    def ok(nombre, cond, detalle=""):
        res.append((nombre, bool(cond), detalle))

    # Subconjunto representativo de la grilla (todas las combinaciones de dimensiones críticas)
    sub = list(itertools.product(ESCALAS, MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C"), PROD))
    Rs = {}
    for E, (modo, h), auto, cfg, pr in sub:
        Rs[(E, modo, h, auto, cfg, pr)] = calcular({"aves_dia": E, "horas_netas": h, "turnos": modo,
                                                    "automatizacion": auto, "config": cfg, "productividad": pr,
                                                    "aves_camion": P["aves_camion_escenario"]})

    # R01 dotación nunca negativa
    neg = [(k_, p["clave"]) for k_, R in Rs.items() for p in R["puestos"]
           for c in ("personas", "equivalentes", "externos_equivalentes", "por_turno")
           if p[c] is not None and p[c] < 0]
    ok("R01 dotación nunca negativa", not neg, str(neg[:3]))

    # R02 aumentar escala no reduce personal (total interno+externo, y cada grupo) sin explicación
    viol = []
    for (modo, h), auto, cfg, pr in itertools.product(MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C"), PROD):
        prev = None
        for E in ESCALAS:
            R = Rs[(E, modo, h, auto, cfg, pr)]
            if prev is not None:
                if _total_func(R) < _total_func(prev) - 1e-9 or R["total_personas"] < prev["total_personas"]:
                    viol.append((E, modo, h, auto, cfg, pr, "total"))
                for g in GRUPOS:
                    if R["personas"][g] < prev["personas"][g]:
                        viol.append((E, modo, h, auto, cfg, pr, g))
            prev = R
    ok("R02 más escala ⇒ no menos personal (total y por grupo)", not viol, str(viol[:3]))

    # R03 automatización no reduce el personal técnico (mantenimiento interno+externo; carga por activos)
    viol = []
    for E, (modo, h), cfg, pr in itertools.product(ESCALAS, MODOS_HORAS, ("A", "B", "C"), PROD):
        prev = None
        for auto in NIVELES_AUTO:
            R = Rs[(E, modo, h, auto, cfg, pr)]
            t = [p for p in R["puestos"] if p["clave"] == "tecnicos_mantenimiento"][0]
            tec = (t["equivalentes"] or 0) + (t["externos_equivalentes"] or 0)
            if prev is not None and (tec < prev[0] - 1e-9 or R["mant_fte_carga"] < prev[1] - 1e-9):
                viol.append((E, modo, h, cfg, pr, auto))
            prev = (tec, R["mant_fte_carga"])
    ok("R03 automatización ⇒ técnicos no disminuyen", not viol, str(viol[:3]))
    # R03b y sí reduce directos (si no, el modelo no representaría la automatización)
    red = all(Rs[(E, "1", 8.0, "automatico", "B", "media")]["personas"]["directo"]
              < Rs[(E, "1", 8.0, "manual", "B", "media")]["personas"]["directo"] for E in ESCALAS)
    ok("R03b automatización reduce directos (con la misma escala y mix)", red)

    # R04 tercerización retira personal interno sin borrar la función
    base = {"aves_dia": 10000, "aves_camion": P["aves_camion_escenario"]}
    viol = []
    for campo, propio, terc, clave in (("limpieza", "propia", "tercerizada", "limpieza_sanitizacion"),
                                       ("mantenimiento", "propio", "tercerizado", "tecnicos_mantenimiento"),
                                       ("flota_propia", True, False, "choferes_aves")):
        a = calcular(dict(base, **{campo: propio}))
        bb = calcular(dict(base, **{campo: terc}))
        pa = [p for p in a["puestos"] if p["clave"] == clave][0]
        pb = [p for p in bb["puestos"] if p["clave"] == clave][0]
        if not (pb["personas"] == 0 and pa["personas"] > 0 and pb["externos_equivalentes"] > 0):
            viol.append((campo, "interno/externo"))
        if abs((pa["equivalentes"] + pa["externos_equivalentes"]) - (pb["equivalentes"] + pb["externos_equivalentes"])) > 1e-9:
            viol.append((campo, "la función cambia de tamaño al tercerizar"))
        if bb["total_personas"] >= a["total_personas"]:
            viol.append((campo, "el total interno no baja"))
    hib = calcular(dict(base, limpieza="hibrida"))
    ph = [p for p in hib["puestos"] if p["clave"] == "limpieza_sanitizacion"][0]
    if not (ph["personas"] > 0 and ph["externos_equivalentes"] > 0):
        viol.append(("limpieza", "híbrida sin ambas partes"))
    terc = calcular(dict(base, limpieza="tercerizada", mantenimiento="tercerizado"))
    claves = {p["clave"] for p in terc["puestos"]}
    for c in ("supervisor_saneamiento", "jefe_mantenimiento", "limpieza_sanitizacion", "tecnicos_mantenimiento"):
        if c not in claves:
            viol.append(("función borrada", c))
    sv = [p for p in terc["puestos"] if p["clave"] in ("supervisor_saneamiento", "jefe_mantenimiento")]
    if any((p["personas"] or 0) < 1 for p in sv):
        viol.append(("sin responsable interno", [p["clave"] for p in sv]))
    al = calcular(dict(base, planta_propia=False))
    if any(p["interno"] and p["categoria"] == "operacion_industrial" and p["personas"] for p in al["puestos"]):
        viol.append(("asset-light con directos internos",))
    if not any(p["clave"] == "evisceracion" and p["externos_equivalentes"] > 0 for p in al["puestos"]):
        viol.append(("asset-light borra la función de faena",))
    ok("R04 tercerizar retira interno y conserva la función", not viol, str(viol[:3]))

    # R05 turnos no violan la ecuación de 24 h en silencio
    viol = []
    for R in Rs.values():
        tj = R["turnos"]
        v24 = mc.ventana_24h(R["entradas"]["horas_netas"], tj["ventana"], turnos=tj["cuadrillas"])
        if abs(v24["holgura"] - tj["holgura_24h"]) > 1e-9:
            viol.append("holgura distinta de 09A")
        if (tj["holgura_24h"] < 0) != any(a.startswith("ALERTA_24H") for a in tj["alertas"]):
            viol.append(("alerta 24 h faltante", R["entradas"]["horas_netas"], tj["ventana"]))
        if R["entradas"]["turnos"] in ("1", "2") and tj["presencia_h"] > P["jornada_normal_h"] + 1e-9 and \
                not any(a.startswith("ALERTA_JORNADA") for a in tj["alertas"]):
            viol.append("alerta de jornada faltante")
    r16 = Rs[(10000, "2", 16.0, "semiautomatico", "B", "baja")]["turnos"]
    if not r16["alerta_24h"]:
        viol.append("16 h conservador sin alerta (09A: −8,3 h)")
    ok("R05 turnos con ecuación de 24 h y jornada explícitas", not viol, str(viol[:3]))

    # R06 escenarios independientes (orden de cálculo y entradas no se contaminan)
    a1 = calcular({"aves_dia": 5000})
    _ = calcular({"aves_dia": 20000, "automatizacion": "automatico", "turnos": "2", "horas_netas": 16.0,
                  "limpieza": "tercerizada", "flota_propia": True, "aves_camion": 5500})
    a2 = calcular({"aves_dia": 5000})
    ent = {"aves_dia": 2500}
    ent_copia = copy.deepcopy(ent)
    calcular(ent)
    P_antes = copy.deepcopy(P)
    calcular({"aves_dia": 10000, "productividad": "baja"})
    ok("R06 escenarios independientes", a1["total_equivalentes"] == a2["total_equivalentes"]
       and a1["total_personas"] == a2["total_personas"] and ent == ent_copia and P == P_antes
       and ESCENARIO_BASE["aves_dia"] == 10000)

    # R07 datos faltantes no se rellenan
    R = calcular({"aves_dia": 10000, "flota_propia": True})          # sin capacidad de camión
    ch = {p["clave"]: p for p in R["puestos"]}
    cond = (ch["choferes_aves"]["personas"] is None and ch["choferes_producto"]["personas"] is None
            and ch["inspeccion_oficial"]["externos_equivalentes"] is None
            and ch["hys_externo"]["externos_equivalentes"] is None and R["estado"] == "INCOMPLETO"
            and {"choferes_aves", "choferes_producto", "inspeccion_oficial"} <= set(R["pendientes"]))
    with open(CSV_PLANTILLA if os.path.exists(CSV_PLANTILLA) else os.devnull, encoding="utf-8") as f:
        filas = list(csv.DictReader(f)) if os.path.exists(CSV_PLANTILLA) else []
    cond = cond and all(x["COSTO_EMPRESA_MENSUAL"] == "" and x["COSTO_ANUAL"] == "" for x in filas)
    ok("R07 faltantes quedan PENDIENTE (choferes, inspección, HyS, costos)", cond)

    # R08 entradas inválidas se rechazan
    malos = [{"aves_dia": -1}, {"aves_dia": 0}, {"horas_netas": 0}, {"horas_netas": 25}, {"turnos": "3"},
             {"automatizacion": "robot"}, {"limpieza": "nadie"}, {"config": "Z"}, {"aves_camion": -5},
             {"dias_semana": 7}]
    rech = 0
    for m in malos:
        try:
            calcular(m)
        except ErrorRRHH:
            rech += 1
    ok("R08 entradas inválidas rechazadas", rech == len(malos), f"{rech}/{len(malos)}")

    # R09 personas físicas ≥ puestos por turno × cuadrillas (cobertura ≥ 1) y equivalentes coherentes
    viol = []
    for R in Rs.values():
        for p in R["puestos"]:
            if p["modalidad"] == "turno" and p["interno"] and p["por_turno"]:
                if p["personas"] < p["por_turno"] * p["cuadrillas"]:
                    viol.append(p["clave"])
    ok("R09 personas ≥ puestos × cuadrillas", not viol, str(viol[:3]))

    # R10 suma de grupos = total; indirectos = total − directos
    viol = [k_ for k_, R in Rs.items() if abs(sum(R["equivalentes"].values()) - R["total_equivalentes"]) > 1e-9
            or abs(R["indirectos_equivalentes"] - (R["total_equivalentes"] - R["equivalentes"]["directo"])) > 1e-9
            or sum(R["personas"].values()) != R["total_personas"]]
    ok("R10 consistencia de agregados", not viol)

    # R11 KPIs múltiples y coherentes (ninguno único)
    R = Rs[(10000, "1", 8.0, "semiautomatico", "B", "media")]
    kp = R["kpi"]
    ok("R11 indicadores múltiples presentes y positivos",
       all(kp[x] and kp[x] > 0 for x in ("aves_persona_h_directa", "kg_persona_h_directa", "personas_por_1000_aves",
                                          "ratio_indirecta_directa", "directos_por_supervisor", "equipos_por_tecnico")))

    # R12 modelos importados sin cambios (ritmos y horas 24 h de 09A)
    ok("R12 09A intacto (horas netas máx. 16,57 / 13,77 / 10,00)",
       abs(mc.horas_netas_max_24h("optimista") - 16.57) < 0.011 and abs(mc.horas_netas_max_24h("media") - 13.77) < 0.011
       and abs(mc.horas_netas_max_24h("conservadora") - 10.0) < 0.011)

    # R13 la productividad "alta" nunca da más personas que la "baja" (rangos ordenados)
    viol = []
    for E, (modo, h), auto, cfg in itertools.product(ESCALAS, MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C")):
        a_, b_ = Rs[(E, modo, h, auto, cfg, "alta")], Rs[(E, modo, h, auto, cfg, "baja")]
        pb = {p["clave"]: p for p in b_["puestos"]}
        if a_["total_personas"] > b_["total_personas"]:
            viol.append((E, modo, h, auto, cfg, "total"))
        for p in a_["puestos"]:
            q = pb.get(p["clave"])
            if q and p["personas"] is not None and q["personas"] is not None and p["personas"] > q["personas"] \
                    and not p["clave"].startswith("compartidos_"):
                viol.append((E, modo, h, auto, cfg, p["clave"]))
    ok("R13 rangos ordenados (alta ≤ baja, total y por puesto)", not viol, str(viol[:3]))

    # R14 el mix cambia la sala de corte: C (deshuese) ≥ B ≥ A en directos de salas limpias
    viol = []
    for E, auto in itertools.product(ESCALAS, NIVELES_AUTO):
        z = [Rs[(E, "1", 8.0, auto, c, "media")]["zonas_turno"].get("limpia", 0) for c in ("A", "B", "C")]
        if not z[0] <= z[1] <= z[2]:
            viol.append((E, auto, z))
    ok("R14 mix: limpia A ≤ B ≤ C", not viol, str(viol[:3]))

    if verbose:
        for n, c, d in res:
            print(f"  [{'OK' if c else 'FALLA'}] {n}" + (f" — {d}" if (d and not c) else ""))
        print(f"  {sum(c for _, c, _ in res)}/{len(res)} tests OK")
    return all(c for _, c, _ in res), res


def prueba_mutaciones():
    """Introduce errores deliberados y verifica que algún test los detecta."""
    global calcular
    original_P = copy.deepcopy(P)
    orig_calc = calcular
    mut = []

    def restaurar():
        P.clear()
        P.update(copy.deepcopy(original_P))
        globals()["calcular"] = orig_calc
        for f in (m2_proceso, logistica_vivo, logistica_producto):
            f.cache_clear()

    casos = [
        ("productividad alta con más gente que baja", lambda: P["span_supervision"].update({"alta": 5})),
        ("automatización reduce mantenimiento", lambda: P["mant_h_semana_equipo"].update({"A": T(0.0, 0.0, 0.0)})),
        ("cobertura < 1", lambda: P["factor_cobertura"].update({"media": 0.5, "alta": 0.5, "baja": 0.5})),
        ("coeficiente negativo", lambda: P["faena_por_1000"].update({"A": T(-5, -5, -5)})),
        ("deshuese menos productivo en manual que en auto (orden invertido de mix)",
         lambda: P["trozado_kg_h"].update({"M": T(1e9, 1e9, 1e9), "Mc": T(1e9, 1e9, 1e9), "S": T(1e9, 1e9, 1e9), "A": T(1e9, 1e9, 1e9)})
         or P["deshuese_kg_h"].update({"M": T(1e9, 1e9, 1e9), "S": T(1e9, 1e9, 1e9), "A": T(1e9, 1e9, 1e9)})
         or P["empaque_kg_h"].update({"A": T(1, 1, 1)})),
    ]

    def m_rellena():
        def c2(entradas=None):
            R = orig_calc(entradas)
            for p in R["puestos"]:
                if p["estado"] == "PENDIENTE":
                    p["personas"] = 1
                    p["externos_equivalentes"] = 1.0
            R["pendientes"] = []
            R["estado"] = "COMPLETO"
            return R
        globals()["calcular"] = c2

    def m_silencio():
        def c2(entradas=None):
            R = orig_calc(entradas)
            R["turnos"]["alertas"] = []
            return R
        globals()["calcular"] = c2

    def m_borra_funcion():
        def c2(entradas=None):
            R = orig_calc(entradas)
            if (entradas or {}).get("limpieza") == "tercerizada":
                R["puestos"] = [p for p in R["puestos"] if p["clave"] != "supervisor_saneamiento"]
            return R
        globals()["calcular"] = c2

    casos += [("faltantes rellenados", m_rellena), ("alertas 24 h silenciadas", m_silencio),
              ("tercerización borra la función", m_borra_funcion)]
    for nombre, aplicar in casos:
        restaurar()
        aplicar()
        with redirect_stdout(io.StringIO()):
            try:
                todo_ok, _ = ejecutar_tests(verbose=False)
            except Exception:
                todo_ok = False
        mut.append((nombre, not todo_ok))
    restaurar()
    for n, det in mut:
        print(f"  [{'DETECTADA' if det else 'NO DETECTADA'}] {n}")
    print(f"  {sum(d for _, d in mut)}/{len(mut)} mutaciones detectadas")
    return all(d for _, d in mut)


# ---------------------------------------------------------------------------
# 8. TABLAS RESUMEN
# ---------------------------------------------------------------------------
def fmt(x, d=0):
    if x is None:
        return "PEND."
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_tablas():
    print("\n## Escenario de referencia por escala (1 cuadrilla, 8 h netas en turno extendido; auto. de referencia 09A; B; propios; flota de terceros)")
    print("| Escala | Auto | Directos/turno | Personas/turno planta | Directos | Supervisión | Soporte | Administración | Dirección | Total personas (baja–media–alta prod.) | Equivalentes internos | Externos eq. | Personas/1.000 aves | Alertas |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for E in ESCALAS:
        Rr = {pr: calcular(escenario_referencia(E, pr)) for pr in PROD}
        R = Rr["media"]
        g = R["personas"]
        print(f"| {fmt(E)} | {AUTO_REFERENCIA[E]} | {R['directos_turno']} | {fmt(R['por_turno_planta'])} | {g['directo']} | "
              f"{g['supervision']} | {g['soporte']} | {g['administracion']} | {g['direccion']} | "
              f"{Rr['alta']['total_personas']}–**{R['total_personas']}**–{Rr['baja']['total_personas']} | "
              f"{fmt(R['total_equivalentes'], 1)} | {fmt(R['externos_equivalentes'], 1)} | "
              f"{fmt(R['kpi']['personas_por_1000_aves'], 1)} | {'; '.join(R['turnos']['alertas']) or '—'} |")
    print("\n## Total de personas internas por escala, automatización y modo de turno (config. B, propios, media)")
    print("| Escala | Modo (h netas) | manual | mecanizado | semiautomático | automático | holgura 24 h | presencia cuadrilla h | alertas |")
    print("|---|---|---|---|---|---|---|---|---|")
    for E in ESCALAS:
        for modo, h in MODOS_HORAS:
            Rs = [calcular({"aves_dia": E, "horas_netas": h, "turnos": modo, "automatizacion": a}) for a in NIVELES_AUTO]
            tj = Rs[0]["turnos"]
            print(f"| {fmt(E)} | {modo} ({fmt(h)}) | " + " | ".join(str(R["total_personas"]) for R in Rs)
                  + f" | {fmt(tj['holgura_24h'], 1)} | {fmt(tj['presencia_h'], 2)} | {len(tj['alertas'])} |")


def imprimir_detalle(E, pr="media"):
    R = calcular(escenario_referencia(E, pr))
    print(f"\n### Detalle REF-{E}")
    for p in R["puestos"]:
        print(f"  {p['clave']:<28} {p['grupo']:<14} {p['zona']:<16} t={p['por_turno']} c={p['cuadrillas']} "
              f"pers={p['personas']} eq={fmt(p['equivalentes'], 2) if p['equivalentes'] is not None else 'PEND.'} "
              f"ext={fmt(p['externos_equivalentes'], 2) if p['externos_equivalentes'] is not None else 'PEND.'} {p['base']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--tablas", action="store_true")
    ap.add_argument("--detalle", type=int, default=None)
    ap.add_argument("--mutaciones", action="store_true")
    a = ap.parse_args()
    if a.mutaciones:
        sys.exit(0 if prueba_mutaciones() else 1)
    if a.detalle:
        imprimir_detalle(a.detalle)
        return
    if a.tablas:
        imprimir_tablas()
        return
    if not a.solo_tests:
        n1 = escribir_plantilla()
        n2 = escribir_csv()
        print(f"Escritos: {os.path.relpath(CSV_ESCENARIOS, RAIZ)} ({n2} escenarios), "
              f"{os.path.relpath(CSV_PLANTILLA, RAIZ)} ({n1} filas)")
    print(f"modelo_rrhh.py v{VERSION} — tests:")
    todo_ok, _ = ejecutar_tests()
    if not a.solo_tests:
        imprimir_tablas()
    sys.exit(0 if todo_ok else 1)


if __name__ == "__main__":
    main()
