#!/usr/bin/env python3
"""
modelo_rrhh.py — Modelo organizacional y de dotación por escala (sesión 14A)
===========================================================================

Versión 1.1 · 2026-10-01 · Fase 0 (prefactibilidad) · Carpeta 18_recursos_humanos
v1.1 = auditoría de unidades laborales: headcount, FTE, dotación simultánea, puestos por turno y pico en
sitio son variables DISTINTAS; headcount de nómina PENDIENTE sin factor de cobertura validado; sin horas
extra automáticas (sólo brecha de jornada); tercerización = horas contratadas; mantenimiento con cobertura
(política) y carga (activos) separadas; matriz de presencia; KPI con denominador declarado.

PREGUNTA
  ¿Qué personas necesita la empresa, dónde trabajan, en qué turnos y cómo cambia la estructura al crecer
  de 2.500 a 5.000, 10.000 y 20.000 aves faenadas por día operativo?

UNIDADES (no se suman entre sí)
  PUESTOS POR TURNO      posiciones que deben cubrirse durante un turno (por cuadrilla).
  DOTACIÓN SIMULTÁNEA    personas presentes al mismo tiempo durante una operación (por puesto y franja).
  PICO EN SITIO          máximo de personas presentes a la vez en el establecimiento (internas + terceros en
                         sitio; excluye inspección oficial, PENDIENTE). Es lo que debe recibir el layout.
  PUESTOS EQUIVALENTES   posiciones distintas a cubrir con personas propias (puestos × cuadrillas; integrantes de
                         la cuadrilla de limpieza; dedicación de roles de estructura). Base del headcount.
  HEADCOUNT DE NÓMINA    puestos equivalentes × FACTOR_COBERTURA_NOMINA (francos, vacaciones, licencias,
                         ausentismo, capacitación, reemplazos). Sin factor validado = PENDIENTE (None).
                         NUNCA se deriva del FTE.
  FTE                    horas-persona por día operativo ÷ jornada de referencia (8 h). 2 personas × 4 h = 1 FTE.
  HORAS CONTRATADAS      horas-persona por día de funciones tercerizadas (no desaparecen al tercerizar).

QUÉ NO HACE
  No calcula salarios, cargas ni OPEX (plantilla con costos VACÍOS). No elige escala, turnos, automatización,
  modalidad de limpieza, mantenimiento ni flota. No calcula horas extra: informa la BRECHA entre presencia
  requerida y jornada de referencia, que puede resolverse con turnos, relevos, escalonamiento, personal
  adicional, horas extraordinarias u otra organización (DPV-14A-01). No modifica los modelos que importa.
  Ninguna productividad es un dato argentino medido: coeficientes [SUPUESTO] de rango (alta / media / baja).

FÓRMULAS (r = E / h, ritmo de la línea en aves/h; n_c = cuadrillas; J = jornada de referencia 8 h)
  presencia de cuadrilla p = h_c / D + pausas(h_c) + limpieza intermedia(h_c) [+ traspaso si n_c = 2]
                             (D, pausas y limpieza intermedia de 09A; h_c = h / n_c)
  puestos por turno (tarea) = ⌈fijo + coef[nivel] × r / 1.000⌉ · ⌈fijo + kg/h ÷ productividad[nivel]⌉ ·
                              ⌈fijo + t/día ÷ n_c ÷ t por persona-turno⌉
  FTE línea                 = puestos × n_c × p / J
  limpieza post-producción  = cuadrilla simultánea ⌈m² (12C) × f_auto ÷ (m²/persona-h) ÷ ventana⌉;
                              horas-persona = cuadrilla × ventana; FTE = horas-persona / J
  mantenimiento             = reconciliación max(COBERTURA, CARGA)
      COBERTURA (política de referencia) = (técnicos simultáneos × horas con activos en marcha
                                            + 1 × horas de limpieza/sanitización/mantenimiento) / J
      CARGA (activos)       = Σ equipos h/semana[nivel] × criticidad × unidades ÷ días ÷ (J × fracción productiva)
  choferes (flota propia)   = horas-camión/día de 12B / J (capacidad de ESCENARIO); producto PENDIENTE
  pico en sitio             = máx_t Σ simultáneos presentes en t (matriz de presencia: ingreso, duración, salida)
  brecha de jornada         = max(0, p − J) por persona de línea; horas-persona a organizar = brecha × puestos × n_c
  24 h                      = modelo_capacidad_proceso.ventana_24h (alerta si holgura < 0)

ENTRADAS (ver ESCENARIO_BASE): aves_dia · horas_netas · turnos (1 / extendido / 2) · automatizacion (manual /
  mecanizado / semiautomatico / automatico) · config (A / B / C) · flota_propia · limpieza (propia /
  tercerizada / hibrida) · mantenimiento (propio / tercerizado / mixto) · productividad (alta / media / baja)
  · ventana · dias_semana · planta_propia (False = asset-light) · abastecimiento (integracion / compra) ·
  laboratorio · factor_cobertura_nomina (None = PENDIENTE) · aves_camion · cap_camion_producto_t ·
  dist_producto_km (None = PENDIENTE).

SALIDAS: escenarios_rrhh.csv (una fila por escenario) · plantilla_costo_laboral.csv (costos vacíos)

USO
  python3 18_recursos_humanos/modelo_rrhh.py                # tests + CSV + tablas
  python3 18_recursos_humanos/modelo_rrhh.py --solo-tests
  python3 18_recursos_humanos/modelo_rrhh.py --tablas
  python3 18_recursos_humanos/modelo_rrhh.py --detalle 10000
  python3 18_recursos_humanos/modelo_rrhh.py --mutaciones

TESTS: R01–R14 de v1.0 adaptados a las nuevas unidades + R15–R23 de la auditoría de unidades (variables
  distintas, cuadrilla parcial ≠ FTE, tercerización conserva horas, sin horas extra automáticas, cobertura vs
  carga, layout recibe pico, KPI con denominador, plantilla sin salarios, SENASA fuera de la empresa).

IDs: SUP-14A-01..18, DPV-14A-##, DEC-14A-##, FTE-14A-### (provisionales; actualizaciones_gestion_14A.md).
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

VERSION = "1.1"
FECHA = "2026-10-01"
CSV_ESCENARIOS = os.path.join(AQUI, "escenarios_rrhh.csv")
CSV_PLANTILLA = os.path.join(AQUI, "plantilla_costo_laboral.csv")
CSV_EQUIPOS = os.path.join(RAIZ, "08_maquinaria", "matriz_equipos.csv")

ESCALAS = tuple(mc.ESCALAS)
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
DRIVERS = ("produccion", "activos", "casi_fijo", "estrategia")
FRANJAS_EN_SITIO = ("linea", "tecnica", "post", "diurna")
PENDIENTE = None
# Sensibilidad del factor de cobertura de nómina: SÓLO para mostrar un rango de headcount (no validado)
FACTOR_COBERTURA_SENSIBILIDAD = (1.08, 1.18)                   # SUP-14A-03 [SUPUESTO DE SENSIBILIDAD]


class ErrorRRHH(Exception):
    pass


def T(alta, media, baja):
    """Triple de sensibilidad: alta productividad (menos personas) / media / baja."""
    return {"alta": alta, "media": media, "baja": baja}


# ---------------------------------------------------------------------------
# 1. PARÁMETROS — todos [SUPUESTO] de rango o [PVDP]; ninguno es dato argentino medido
# ---------------------------------------------------------------------------
P = {
    # --- jornada (SUP-14A-02; DPV-082, DPV-14A-01)
    "jornada_referencia_h": 8.0,          # [PVDP] base del FTE y de la brecha (FTE-14A-001); convenio PENDIENTE
    "solape_cambio_turno_h": 0.25,        # [SUPUESTO] traspaso entre cuadrillas
    # --- operación industrial: puestos por 1.000 aves/h, POR TAREA (SUP-14A-04)
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
    "camaras_t_persona_turno": T(25.0, 18.0, 12.0),
    "subprod_t_persona_turno": {"M": T(6.0, 4.0, 3.0), "S": T(8.0, 6.0, 4.0), "A": T(15.0, 10.0, 8.0)},
    "limpieza_operativa_por_1000": T(0.3, 0.5, 0.8),
    # --- limpieza post-producción (SUP-14A-06; DPV-091). Factor por automatización y fracción híbrida =
    #     [SUPUESTO DE SENSIBILIDAD] genéricos (no son tareas medidas)
    "limpieza_m2_persona_h": T(60.0, 40.0, 25.0),
    "limpieza_factor_auto": {"manual": 1.0, "mecanizado": 1.0, "semiautomatico": 1.1, "automatico": 1.25},
    "limpieza_hibrida_interna": 0.30,
    # --- supervisión (SUP-14A-07)
    "span_supervision": T(30, 22, 15),
    # --- calidad: control operativo QC por cuadrilla (SUP-14A-08)
    "control_calidad_por_1000": T(0.6, 0.8, 1.2),
    # --- mantenimiento: CARGA por activos (SUP-14A-09) y COBERTURA por política (SUP-14A-16)
    "mant_h_semana_equipo": {"M": T(0.0, 0.0, 0.0), "Mc": T(0.5, 0.75, 1.5), "S": T(0.75, 1.5, 3.0),
                             "A": T(1.5, 3.0, 6.0)},
    "mant_peso_criticidad": {"CRÍTICO": 1.5, "IMPORTANTE": 1.0, "SECUNDARIO": 0.5},
    "mant_fraccion_productiva": T(0.9, 0.8, 0.7),                 # horas de mantenimiento / horas de jornada
    "unidades_duplicables_aves_h": 1250.0,
    # política de cobertura de referencia: técnicos presentes mientras los activos críticos funcionan
    # (NO es requisito técnico universal): base 1; +1 desde 5.000; +1 desde 10.000; +1 si automático ≥ 10.000
    "cobertura_umbrales": (5000, 10000),
    "cobertura_guardia_fuera_produccion": 1,
    # --- producción primaria (coordinación; SUP-14A-10)
    "granjas_por_tecnico": T(20, 15, 10),
    "plazas_granja": 30000,
    # --- logística (SUP-14A-11)
    "aves_camion_escenario": 5500,                                # SUP-033 (sin fuente), capacidad de ESCENARIO
    "radio_km_escenario": 100,
    # --- RR. HH. (SUP-14A-12): 1 cada N puestos equivalentes internos
    "puestos_por_rrhh": T(150, 120, 90),
}

BANDAS = (("S", 4000), ("M", 8000), ("L", 15000), ("XL", float("inf")))
ESTRUCTURA = {
    # clave: (puesto, categoría, grupo, zona, {S, M, L, XL}, contrato, nota)  — valores = dedicación (FTE)
    "jefe_produccion": ("Jefe de producción", "operacion_industrial", "supervision", "transversal",
                        {"S": 0, "M": 0, "L": 1, "XL": 1}, "fuera_convenio", "Por debajo de 10.000 lo cubre el gerente de operaciones"),
    "jefe_mantenimiento": ("Jefe de mantenimiento", "soporte_industrial", "soporte", "transversal",
                           {"S": 0, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "En 2.500 lo cubre un técnico líder"),
    "panolero": ("Pañolero / repuestos", "soporte_industrial", "soporte", "transversal",
                 {"S": 0, "M": 0, "L": 1, "XL": 1}, "convenio_pendiente", ""),
    "jefe_calidad": ("Jefe de calidad e inocuidad (QA + inocuidad)", "soporte_industrial", "soporte", "transversal",
                     {"S": 1, "M": 1, "L": 1, "XL": 1}, "fuera_convenio", "Reporta fuera de producción; en 2.500 también APPCC"),
    "analista_appcc": ("Analista APPCC / POES / documentación (inocuidad)", "soporte_industrial", "soporte", "oficinas",
                       {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", "En 2.500 dedicación 0,5 (función combinada)"),
    "trazabilidad": ("Trazabilidad y registros", "soporte_industrial", "soporte", "oficinas",
                     {"S": 0, "M": 0.5, "L": 1, "XL": 1}, "convenio_pendiente", "En 2.500 la cubre el jefe de calidad"),
    "hys": ("Higiene y seguridad laboral (interno)", "soporte_industrial", "soporte", "transversal",
            {"S": 0, "M": 0, "L": 1, "XL": 1}, "fuera_convenio", "Servicio externo en S y M (PENDIENTE, DPV-14A-07)"),
    "lavanderia": ("Lavandería / ropería por zona", "soporte_industrial", "soporte", "personal",
                   {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "convenio_pendiente", "Alternativa tercerizada (DEC-14A-07)"),
    "planificacion_trafico": ("Planificación y tráfico", "logistica", "soporte", "oficinas",
                              {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", ""),
    "deposito_insumos": ("Recepción de insumos y depósito (envases, químicos)", "logistica", "soporte", "deposito",
                         {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "convenio_pendiente", ""),
    "expedicion_adm": ("Administración de expedición (remitos, DT-e)", "logistica", "soporte", "oficinas",
                       {"S": 0, "M": 0.5, "L": 1, "XL": 2}, "convenio_pendiente", ""),
    "compras": ("Compras", "administracion", "administracion", "oficinas",
                {"S": 0.5, "M": 1, "L": 1, "XL": 2}, "fuera_convenio", ""),
    "ventas": ("Ventas / ejecutivos de cuenta", "administracion", "administracion", "oficinas",
               {"S": 1, "M": 2, "L": 3, "XL": 4}, "fuera_convenio", "Depende de canales y clientes, no sólo de aves"),
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
PRIMARIA = {
    "coordinador_integracion": ("Coordinador de producción primaria / integrados", {"S": 0.5, "M": 1, "L": 1, "XL": 1}),
    "veterinario": ("Veterinario de la integración", {"S": 0.5, "M": 1, "L": 1, "XL": 2}),
    "planificacion_crianza": ("Planificación de crianza (pollito BB, alimento, cosecha)", {"S": 0, "M": 0.5, "L": 1, "XL": 1}),
}
PRIMARIA_COMPRA = {
    "coordinador_abastecimiento": ("Coordinador de abastecimiento de pollo vivo y recepción", {"S": 0.5, "M": 1, "L": 1, "XL": 1}),
    "veterinario": ("Veterinario (recepción, bienestar, sanidad de proveedores)", {"S": 0.5, "M": 0.5, "L": 1, "XL": 1}),
}
LAB_PROPIO = {"S": 1, "M": 1, "L": 2, "XL": 3}

# Cómo escala cada función (SUP-14A-17): produccion · activos · casi_fijo · estrategia
DRIVER = {
    **{k: "produccion" for k in ("colgado", "descarga", "faena", "evisceracion", "enfriamiento", "clasificacion",
                                 "trozado", "deshuese", "empaque", "camaras_expedicion", "subproductos",
                                 "limpieza_operativa", "limpieza_sanitizacion", "supervisores_linea", "jefes_turno",
                                 "control_calidad", "trazabilidad", "lavanderia", "planificacion_trafico",
                                 "deposito_insumos", "expedicion_adm", "tecnicos_campo")},
    **{k: "activos" for k in ("tecnicos_mantenimiento", "jefe_mantenimiento", "panolero")},
    **{k: "casi_fijo" for k in ("jefe_produccion", "supervisor_saneamiento", "jefe_calidad", "analista_appcc", "hys",
                                "coordinador_integracion", "coordinador_abastecimiento", "veterinario",
                                "planificacion_crianza", "compras", "administracion", "finanzas", "sistemas", "rrhh",
                                "gerente_general", "gerente_operaciones", "gerente_comercial", "gerente_adm_fin",
                                "gerente_calidad")},
    **{k: "estrategia" for k in ("ventas", "choferes_aves", "choferes_producto", "captura", "laboratorio",
                                 "control_calidad_facon", "hys_externo", "inspeccion_oficial")},
}
SUBFUNCION_CALIDAD = {"control_calidad": "QC", "control_calidad_facon": "QC", "jefe_calidad": "QA",
                      "gerente_calidad": "QA", "analista_appcc": "INOCUIDAD", "trazabilidad": "TRAZABILIDAD",
                      "laboratorio": "LABORATORIO", "inspeccion_oficial": "OFICIAL_SENASA"}
BLOQUE_ASSET_LIGHT = {"ventas": "comercial", "gerente_comercial": "comercial", "gerente_general": "dirección",
                      "administracion": "administración", "finanzas": "administración", "compras": "administración",
                      "rrhh": "administración", "sistemas": "administración", "gerente_adm_fin": "administración",
                      "coordinador_integracion": "coordinación productiva", "veterinario": "coordinación productiva",
                      "planificacion_crianza": "coordinación productiva", "tecnicos_campo": "coordinación productiva",
                      "coordinador_abastecimiento": "coordinación productiva", "jefe_calidad": "calidad",
                      "analista_appcc": "calidad", "trazabilidad": "calidad",
                      "control_calidad_facon": "supervisión de terceros", "planificacion_trafico": "logística",
                      "deposito_insumos": "logística", "expedicion_adm": "logística", "choferes_aves": "logística",
                      "choferes_producto": "logística"}

ESCENARIO_BASE = {
    "aves_dia": 10000, "horas_netas": 8.0, "turnos": "1", "automatizacion": "semiautomatico",
    "config": "B", "flota_propia": False, "limpieza": "propia", "mantenimiento": "propio",
    "productividad": "media", "ventana": None, "dias_semana": 5, "planta_propia": True,
    "abastecimiento": "integracion", "laboratorio": "externo", "factor_cobertura_nomina": None,
    "aves_camion": None, "cap_camion_producto_t": None, "dist_producto_km": None,
}
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
    """Nivel de automatización de cada TAREA bajo el escenario (09A/08 §1). SUP-14A-14."""
    t = NIVEL_OBJETIVO[auto]
    tabla = {
        "descarga": ("M", "M", "S", "A"), "faena": ("M", "Mc", "S", "A"), "evisceracion": ("M", "M", "S", "A"),
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
    f = e["factor_cobertura_nomina"]
    if f is not None and (not isinstance(f, (int, float)) or f < 1):
        raise ErrorRRHH("factor_cobertura_nomina debe ser None (PENDIENTE) o ≥ 1")


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
            "camion_horas_dia": r["camion_horas_dia"]}


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
    ops = set()
    for E in ESCALAS:
        ops |= _opciones(fila[f"nivel_{E}"])
    if not ops:
        return None
    t = NIVEL_OBJETIVO[auto]
    debajo = [o for o in ops if ORDEN_NIVEL[o] <= t]
    return max(debajo, key=ORDEN_NIVEL.get) if debajo else min(ops, key=ORDEN_NIVEL.get)


def presente(fila, E):
    ref = max([x for x in ESCALAS if x <= E] or [ESCALAS[0]])
    return bool(_opciones(fila[f"nivel_{ref}"]))


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


def tecnicos_cobertura(E, auto):
    """POLÍTICA DE COBERTURA DE REFERENCIA (SUP-14A-16): técnicos presentes mientras funcionan los activos.
    No es requisito técnico universal."""
    u1, u2 = P["cobertura_umbrales"]
    return 1 + (E >= u1) + (E >= u2) + (auto == "automatico" and E >= u2)


# ---------------------------------------------------------------------------
# 4. TURNOS, JORNADA Y CALENDARIO DEL DÍA (integra la ecuación de 24 h de 09A)
# ---------------------------------------------------------------------------
def turnos_y_jornada(e):
    h, modo = e["horas_netas"], e["turnos"]
    vent = e["ventana"] or VENTANA_POR_PROD[e["productividad"]]
    v = mc.VENTANAS[vent]
    D = mc.SENSIBILIDAD[v["sens"]]["D"]
    J = P["jornada_referencia_h"]
    n_c = CUADRILLAS[modo]
    h_c = h / n_c
    sol = P["solape_cambio_turno_h"] if n_c == 2 else 0.0
    presencia = h_c / D + v["pausas_8h"] * h_c / 8 + v["limpieza_intermedia_8h"] * h_c / 8 + sol
    v24 = mc.ventana_24h(h, vent, turnos=n_c)
    comp = v24["componentes"]
    pa = comp["preparacion_arranque"]
    inicios = [pa + k * (presencia - sol) for k in range(n_c)]
    fin_prod = inicios[-1] + presencia
    ini_limp = fin_prod + comp["cierre_vaciado"]
    fin_limp = ini_limp + comp["limpieza"] + comp["sanitizacion"]
    fin_mant = fin_limp + comp["mantenimiento"]
    brecha = max(0.0, presencia - J)
    alertas = []
    if v24["alerta"]:
        alertas.append(f"ALERTA_24H(holgura {v24['holgura']:.2f} h)")
    if brecha > 1e-9:
        if modo in ("1", "2"):
            alertas.append(f"INCOMPATIBILIDAD_JORNADA(presencia {presencia:.2f} h > jornada de referencia {J:.0f} h: "
                           "requiere organización adicional)")
        else:
            alertas.append(f"JORNADA_EXTENDIDA_A_VALIDAR(presencia {presencia:.2f} h; DPV-14A-01)")
    elif modo == "extendido":
        alertas.append("NOTA_EXTENDIDO_INNECESARIO(cabe en la jornada de referencia)")
    return {
        "ventana": vent, "D": D, "J": J, "cuadrillas": n_c, "h_netas_cuadrilla": h_c, "presencia_h": presencia,
        "solape_h": sol, "brecha_jornada_h": brecha, "holgura_24h": v24["holgura"], "total_24h": v24["total"],
        "alerta_24h": v24["alerta"], "alertas": alertas, "inicios_cuadrillas": inicios, "fin_produccion": fin_prod,
        "inicio_limpieza": ini_limp, "fin_limpieza": fin_limp, "fin_mantenimiento": fin_mant,
        "t_limpieza": comp["limpieza"], "t_sanitizacion": comp["sanitizacion"], "t_mantenimiento": comp["mantenimiento"],
        "t_cierre": comp["cierre_vaciado"], "t_preparacion": pa,
        "horas_activos_en_marcha": fin_prod + comp["cierre_vaciado"],
        "horas_fuera_produccion": comp["limpieza"] + comp["sanitizacion"] + comp["mantenimiento"],
    }


# ---------------------------------------------------------------------------
# 5. CONSTRUCCIÓN DE PUESTOS
# ---------------------------------------------------------------------------
def _puesto(lst, **k):
    base = {"clave": None, "puesto": None, "categoria": None, "grupo": None, "zona": None, "franja": None,
            "modalidad": None, "puestos_turno": 0, "cuadrillas": 1, "horas_presencia": 0.0, "simultaneos": 0,
            "puestos_equivalentes": 0.0, "fte_interno": 0.0, "fte_tercerizado": 0.0, "horas_persona_dia": 0.0,
            "horas_contratadas_dia": 0.0, "estado": "CALCULADO", "contrato": "convenio_pendiente", "base": "",
            "ref": ""}
    base.update(k)
    base["driver"] = DRIVER.get(base["clave"], "casi_fijo")
    base["subfuncion"] = SUBFUNCION_CALIDAD.get(base["clave"], "")
    base["interno"] = bool(base["fte_interno"]) or bool(base["puestos_equivalentes"])
    base["tercerizado"] = bool(base["fte_tercerizado"])
    lst.append(base)
    return base


def calcular(entradas=None):
    e = dict(ESCENARIO_BASE)
    if entradas:
        e.update(entradas)
    validar(e)
    E, h, pr, auto, cfg = e["aves_dia"], e["horas_netas"], e["productividad"], e["automatizacion"], e["config"]
    b = banda(E)
    tj = turnos_y_jornada(e)
    n_c, pres, dias, J = tj["cuadrillas"], tj["presencia_h"], e["dias_semana"], tj["J"]
    r = E / h
    k = kg_ave(cfg)
    lst = []
    pendientes = []
    planta = e["planta_propia"]

    def linea(clave, puesto, cat, grupo, zona, pt, base="", ref="", contrato="convenio_pendiente", interno=True):
        """Puesto de línea: presente con su cuadrilla durante toda la presencia."""
        hp = pt * n_c * pres
        _puesto(lst, clave=clave, puesto=puesto, categoria=cat, grupo=grupo, zona=zona,
                franja="linea" if interno else "externo_facon", modalidad="turno", puestos_turno=pt, cuadrillas=n_c,
                horas_presencia=pres, simultaneos=pt, puestos_equivalentes=pt * n_c if interno else 0.0,
                fte_interno=hp / J if interno else 0.0, fte_tercerizado=0.0 if interno else hp / J,
                horas_persona_dia=hp, horas_contratadas_dia=0.0 if interno else hp,
                contrato=contrato if interno else "servicio_tercerizado (façon)", base=base, ref=ref)

    def estructura(clave, puesto, cat, grupo, zona, ded, contrato="fuera_convenio", nota=""):
        franja = "diurna" if zona not in ("campo", "ruta", "externo_facon") else zona
        _puesto(lst, clave=clave, puesto=puesto, categoria=cat, grupo=grupo, zona=zona, franja=franja,
                modalidad="estructura", horas_presencia=J if ded else 0.0, simultaneos=ded,
                puestos_equivalentes=ded, fte_interno=ded, horas_persona_dia=ded * J, contrato=contrato, base=nota)

    # ---------------- 5.1 Operación industrial: POR TAREA ----------------
    t_com_dia = k["comestible_a_empaque"] * E / 1000
    t_sol_dia = k["solidos_a_retirar"] * E / 1000
    nr = {a: nivel_area(a, auto) for a in ("descarga", "faena", "evisceracion", "clasificacion", "trozado",
                                           "deshuese", "empaque", "subproductos")}
    nd_ = "M" if nr["descarga"] == "Mc" else nr["descarga"]
    ncl = "M" if nr["clasificacion"] == "Mc" else nr["clasificacion"]
    kg_troz_h, kg_desh_h = k["a_trozado"] * r, k["a_deshuese"] * r
    ns = "S" if nr["subproductos"] == "Mc" else nr["subproductos"]
    ops = [
        ("colgado", "Colgado", "sucia", max(1, techo(P["colgado_por_1000"][pr] * r / 1000)),
         "manual en todos los niveles; FTE-219 [PVDP·débil]/SUP-063"),
        ("descarga", "Descarga, cajones y andén", "sucia", max(1, techo(P["descarga_por_1000"][nd_][pr] * r / 1000)),
         f"nivel {nd_}"),
        ("faena", "Faena (aturdido–desplumado, degüello, patas, transferencia)", "sucia",
         techo(1 + P["faena_por_1000"][nr["faena"]][pr] * r / 1000), f"nivel {nr['faena']}"),
        ("evisceracion", "Evisceración, menudencias y lavado (sin inspección oficial)", "evisceracion",
         techo(P["evisc_fijo"][nr["evisceracion"]] + P["evisc_por_1000"][nr["evisceracion"]][pr] * r / 1000),
         f"nivel {nr['evisceracion']}; manual FTE-218 [PVDP·débil]"),
        ("enfriamiento", "Operación de enfriamiento", "limpia", 1, "1 operador por cuadrilla"),
        ("clasificacion", "Clasificación y calibrado", "limpia",
         max(1, techo(P["clasif_por_1000"][ncl][pr] * r / 1000)), f"nivel {ncl}"),
        ("trozado", "Trozado", "limpia", techo(1 + kg_troz_h / P["trozado_kg_h"][nr["trozado"]][pr]) if kg_troz_h > 0 else 0,
         f"nivel {nr['trozado']}; {kg_troz_h:.0f} kg/h (config. {cfg})"),
        ("deshuese", "Deshuese y trimming", "limpia",
         techo(1 + kg_desh_h / P["deshuese_kg_h"][nr["deshuese"]][pr]) if kg_desh_h > 0 else 0,
         f"nivel {nr['deshuese']}; {kg_desh_h:.0f} kg/h (config. {cfg})"),
        ("empaque", "Empaque, rotulado y control de peso", "limpia",
         techo(1 + k["comestible_a_empaque"] * r / P["empaque_kg_h"][nr["empaque"]][pr]), f"nivel {nr['empaque']}"),
        ("camaras_expedicion", "Cámaras, congelado y expedición (carga)", "frio_expedicion",
         techo(1 + t_com_dia / n_c / P["camaras_t_persona_turno"][pr]), f"{t_com_dia:.1f} t/día"),
        ("subproductos", "Subproductos y decomisos", "subproductos",
         max(1, techo(t_sol_dia / n_c / P["subprod_t_persona_turno"][ns][pr])), f"{t_sol_dia:.1f} t/día; nivel {ns}"),
    ]
    for clave, nombre, zona, pt, base in ops:
        linea(clave, nombre, "operacion_industrial", "directo", zona, pt, base=base, ref="SUP-14A-04/05",
              interno=planta)
    directos_turno = sum(o[3] for o in ops) if planta else 0

    # ---------------- 5.2 Limpieza y sanitización ----------------
    if planta:
        linea("limpieza_operativa", "Limpieza operativa en turno", "operacion_industrial", "soporte", "transversal",
              techo(1 + P["limpieza_operativa_por_1000"][pr] * r / 1000), base="durante producción; siempre interna",
              ref="SUP-14A-06")
        m2 = m2_proceso(E, h, cfg, AUTO_12C[auto], AREA_12C_POR_PROD[pr])
        ph_req = m2 * P["limpieza_factor_auto"][auto] / P["limpieza_m2_persona_h"][pr]
        vent_l = tj["t_limpieza"] + tj["t_sanitizacion"]
        cuadrilla = techo(ph_req / vent_l)
        frac = {"propia": 1.0, "tercerizada": 0.0, "hibrida": P["limpieza_hibrida_interna"]}[e["limpieza"]]
        cu_int = techo(cuadrilla * frac) if frac > 0 else 0
        cu_ext = cuadrilla - cu_int
        _puesto(lst, clave="limpieza_sanitizacion", puesto="Limpieza y sanitización post-producción",
                categoria="operacion_industrial", grupo="soporte", zona="transversal", franja="post",
                modalidad="cuadrilla_post", puestos_turno=cuadrilla, cuadrillas=1, horas_presencia=vent_l,
                simultaneos=cuadrilla, puestos_equivalentes=cu_int, fte_interno=cu_int * vent_l / J,
                fte_tercerizado=cu_ext * vent_l / J, horas_persona_dia=cuadrilla * vent_l,
                horas_contratadas_dia=cu_ext * vent_l,
                contrato="convenio_pendiente" if cu_int else "servicio_tercerizado",
                base=f"{m2:.0f} m² proceso (12C); ventana {vent_l:.2f} h; {e['limpieza']}", ref="SUP-14A-06; DPV-091")
        estructura("supervisor_saneamiento", "Supervisor de saneamiento / verificación POES", "operacion_industrial",
                   "supervision", "transversal", 1 if (cu_int >= 6 or e["limpieza"] != "propia") else 0,
                   nota="interno en toda modalidad (verificación)")

    # ---------------- 5.3 Supervisión ----------------
    if planta:
        sup_c = max(1, techo(directos_turno / P["span_supervision"][pr]))
        linea("supervisores_linea", "Supervisores de línea", "operacion_industrial", "supervision", "transversal",
              sup_c, ref="SUP-14A-07", contrato="fuera_convenio")
        if n_c == 2:
            linea("jefes_turno", "Jefe de turno", "operacion_industrial", "supervision", "transversal", 1,
                  ref="SUP-14A-07", contrato="fuera_convenio")
        x = ESTRUCTURA["jefe_produccion"]
        estructura("jefe_produccion", *x[:4], x[4][b], contrato=x[5], nota=x[6])
    else:
        sup_c = 0

    # ---------------- 5.4 Calidad (empresa) e inspección oficial (SENASA, separada) ----------------
    if planta:
        linea("control_calidad", "Control de calidad operativo (QC)", "soporte_industrial", "soporte", "transversal",
              techo(1 + P["control_calidad_por_1000"][pr] * r / 1000), ref="SUP-14A-08")
    else:
        estructura("control_calidad_facon", "QC propio en la planta del façonier (supervisión de terceros)",
                   "soporte_industrial", "soporte", "externo_facon", 1 if b in ("S", "M") else 2,
                   contrato="convenio_pendiente", nota="asset-light")
    for kk in ("jefe_calidad", "analista_appcc", "trazabilidad"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5], nota=x[6])
    if e["laboratorio"] == "propio" and planta:
        estructura("laboratorio", "Analistas de laboratorio propio", "soporte_industrial", "soporte", "laboratorio",
                   LAB_PROPIO[b], contrato="convenio_pendiente")
    else:
        _puesto(lst, clave="laboratorio", puesto="Laboratorio de autocontrol (servicio externo por análisis)",
                categoria="soporte_industrial", grupo="soporte", zona="laboratorio", franja="sin_presencia",
                modalidad="externo", estado="EXTERNO_POR_SERVICIO", contrato="servicio_tercerizado",
                base="se contrata por análisis, no por horas; toma de muestras interna (QC)")
    _puesto(lst, clave="inspeccion_oficial", puesto="Inspección veterinaria oficial (SENASA) — NO es personal de la empresa",
            categoria="oficial", grupo="oficial", zona="evisceracion", franja="oficial", modalidad="externo_oficial",
            puestos_turno=PENDIENTE, simultaneos=PENDIENTE, puestos_equivalentes=0.0, fte_interno=0.0,
            fte_tercerizado=PENDIENTE, horas_persona_dia=PENDIENTE, horas_contratadas_dia=PENDIENTE,
            estado="PENDIENTE", contrato="oficial",
            base="inspectores por velocidad de línea sin norma leída; tasa o cargo a la empresa sin verificar",
            ref="DPV-090; DPV-14A-05")
    if planta:
        pendientes.append("inspeccion_oficial")

    # ---------------- 5.5 Mantenimiento: COBERTURA (política) vs CARGA (activos) ----------------
    cob = dict(fte=0.0, horas=0.0, simult=0)
    carga = dict(fte=0.0, h_semana=0.0, equipos=0, por_nivel={})
    if planta:
        h_sem, n_eq, por_niv = carga_mantenimiento(E, r, auto, pr)
        fte_carga = h_sem / dias / (J * P["mant_fraccion_productiva"][pr])
        simult = tecnicos_cobertura(E, auto)
        horas_cob = (simult * tj["horas_activos_en_marcha"]
                     + P["cobertura_guardia_fuera_produccion"] * tj["horas_fuera_produccion"])
        fte_cob = horas_cob / J
        cob = dict(fte=fte_cob, horas=horas_cob, simult=simult)
        carga = dict(fte=fte_carga, h_semana=h_sem, equipos=n_eq, por_nivel=por_niv)
        tot = max(fte_cob, fte_carga)
        modo_m = e["mantenimiento"]
        if modo_m == "propio":
            fi, fe = tot, 0.0
        elif modo_m == "tercerizado":
            fi, fe = 0.0, tot
        else:
            fi, fe = fte_cob, max(0.0, fte_carga - fte_cob)
        _puesto(lst, clave="tecnicos_mantenimiento",
                puesto="Técnicos de mantenimiento (mecánica, electricidad, frío/utilities, automatización)",
                categoria="soporte_industrial", grupo="soporte", zona="transversal", franja="tecnica",
                modalidad="cobertura", puestos_turno=simult, cuadrillas=n_c,
                horas_presencia=tj["horas_activos_en_marcha"], simultaneos=simult, puestos_equivalentes=fi,
                fte_interno=fi, fte_tercerizado=fe, horas_persona_dia=tot * J, horas_contratadas_dia=fe * J,
                contrato="convenio_pendiente" if fi else "servicio_tercerizado",
                base=(f"{n_eq} equipos ({por_niv['Mc']} Mc, {por_niv['S']} S, {por_niv['A']} A); carga {h_sem:.0f} h/sem "
                      f"= {fte_carga:.2f} FTE; cobertura {simult} simultáneo(s) = {fte_cob:.2f} FTE; {modo_m}"),
                ref="SUP-14A-09; SUP-14A-16")
        x = ESTRUCTURA["jefe_mantenimiento"]
        estructura("jefe_mantenimiento", x[0] if modo_m != "tercerizado" else "Coordinador de mantenimiento y contratos",
                   *x[1:4], x[4][b] if modo_m != "tercerizado" else max(x[4][b], 0.5), nota="función retenida")
        x = ESTRUCTURA["panolero"]
        estructura("panolero", *x[:4], x[4][b] if modo_m != "tercerizado" else 0, contrato=x[5])

    # ---------------- 5.6 Otros servicios ----------------
    for kk in ("hys", "lavanderia"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b] if planta else 0, contrato=x[5], nota=x[6])
    _puesto(lst, clave="hys_externo", puesto="Servicio externo de higiene y seguridad y medicina laboral",
            categoria="soporte_industrial", grupo="soporte", zona="transversal", franja="sin_presencia",
            modalidad="externo", fte_tercerizado=PENDIENTE, horas_persona_dia=PENDIENTE,
            horas_contratadas_dia=PENDIENTE, estado="PENDIENTE", contrato="servicio_tercerizado",
            base="horas-profesional según norma no leída", ref="DPV-14A-07; FTE-14A-004")
    pendientes.append("hys_externo")

    # ---------------- 5.7 Logística ----------------
    for kk in ("planificacion_trafico", "deposito_insumos", "expedicion_adm"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5])
    ac = e["aves_camion"]
    fp = e["flota_propia"]
    if ac is None:
        _puesto(lst, clave="choferes_aves", puesto="Choferes de aves vivas", categoria="logistica", grupo="soporte",
                zona="ruta", franja="ruta", modalidad="flota", puestos_turno=PENDIENTE, simultaneos=PENDIENTE,
                puestos_equivalentes=PENDIENTE if fp else 0.0, fte_interno=PENDIENTE if fp else 0.0,
                fte_tercerizado=0.0 if fp else PENDIENTE, horas_persona_dia=PENDIENTE,
                horas_contratadas_dia=0.0 if fp else PENDIENTE, estado="PENDIENTE",
                base="capacidad de camión no elegida (DPV-084)", ref="DPV-084; DEC-056")
        pendientes.append("choferes_aves")
    else:
        lv = logistica_vivo(E, dias, h, ac)
        fl, hp = lv["flota_minima"], lv["camion_horas_dia"]
        _puesto(lst, clave="choferes_aves", puesto="Choferes de aves vivas", categoria="logistica", grupo="soporte",
                zona="ruta", franja="ruta", modalidad="flota", puestos_turno=fl, simultaneos=fl,
                horas_presencia=hp / fl, puestos_equivalentes=fl if fp else 0.0, fte_interno=hp / J if fp else 0.0,
                fte_tercerizado=0.0 if fp else hp / J, horas_persona_dia=hp, horas_contratadas_dia=0.0 if fp else hp,
                contrato="CCT 40/89 [PVDP]" if fp else "servicio_tercerizado",
                base=f"flota mínima {fl}; {hp:.1f} h-camión/día (12B; {ac} aves/camión de ESCENARIO)",
                ref="SUP-033; SUP-14A-11")
    cap, dist = e["cap_camion_producto_t"], e["dist_producto_km"]
    cd = logistica_producto(E, dias, cfg, cap, dist) if (cap and dist) else None
    if cd is None:
        _puesto(lst, clave="choferes_producto", puesto="Choferes de producto terminado", categoria="logistica",
                grupo="soporte", zona="ruta", franja="ruta", modalidad="flota", puestos_turno=PENDIENTE,
                simultaneos=PENDIENTE, puestos_equivalentes=PENDIENTE if fp else 0.0,
                fte_interno=PENDIENTE if fp else 0.0, fte_tercerizado=0.0 if fp else PENDIENTE,
                horas_persona_dia=PENDIENTE, horas_contratadas_dia=0.0 if fp else PENDIENTE, estado="PENDIENTE",
                base="capacidad, distancia y modelo de distribución no definidos", ref="DPV-084; DPV-036; DEC-016")
        pendientes.append("choferes_producto")
    else:
        n_ch = techo(cd)
        hp = cd * ml.HORAS_CAMION_DIA
        _puesto(lst, clave="choferes_producto", puesto="Choferes de producto terminado", categoria="logistica",
                grupo="soporte", zona="ruta", franja="ruta", modalidad="flota", puestos_turno=n_ch, simultaneos=n_ch,
                horas_presencia=hp / n_ch, puestos_equivalentes=n_ch if fp else 0.0,
                fte_interno=hp / J if fp else 0.0, fte_tercerizado=0.0 if fp else hp / J, horas_persona_dia=hp,
                horas_contratadas_dia=0.0 if fp else hp, contrato="CCT 40/89 [PVDP]",
                base=f"{cd:.2f} camión-día (12B, {cap} t y {dist} km de ESCENARIO)", ref="SUP-14A-11")
    _puesto(lst, clave="captura", puesto="Cuadrillas de captura y carga en granja", categoria="logistica",
            grupo="soporte", zona="granja", franja="campo", modalidad="externo", fte_tercerizado=PENDIENTE,
            horas_persona_dia=PENDIENTE, horas_contratadas_dia=PENDIENTE, estado="PENDIENTE",
            contrato="servicio_tercerizado", base="función del integrado o contratista", ref="DPV-14A-09")
    pendientes.append("captura")

    # ---------------- 5.8 Producción primaria (sólo coordinación) ----------------
    if e["abastecimiento"] == "integracion":
        for kk, (nombre, tabla) in PRIMARIA.items():
            estructura(kk, nombre, "produccion_primaria", "soporte", "campo", tabla[b],
                       nota="no incluye personal de granjas de terceros")
        gr = logistica_vivo(E, dias, h, ac or P["aves_camion_escenario"])["granjas_equivalentes"]
        estructura("tecnicos_campo", "Técnicos de campo (asistencia a integrados)", "produccion_primaria", "soporte",
                   "campo", techo(gr / P["granjas_por_tecnico"][pr]), nota=f"{gr:.1f} granjas equivalentes (12B/03)")
    else:
        for kk, (nombre, tabla) in PRIMARIA_COMPRA.items():
            estructura(kk, nombre, "produccion_primaria", "soporte", "campo", tabla[b])

    # ---------------- 5.9 Administración y dirección ----------------
    for kk in ("compras", "ventas", "administracion", "finanzas", "sistemas"):
        x = ESTRUCTURA[kk]
        estructura(kk, *x[:4], x[4][b], contrato=x[5], nota=x[6])
    for kk in ("gerente_general", "gerente_operaciones", "gerente_comercial", "gerente_adm_fin", "gerente_calidad"):
        x = ESTRUCTURA[kk]
        val = x[4][b] if (planta or kk not in ("gerente_operaciones", "gerente_calidad")) else 0
        estructura(kk, *x[:4], val, contrato=x[5], nota=x[6])
    pe = sum(p["puestos_equivalentes"] or 0 for p in lst)
    rrhh = math.ceil(max(0.5, pe / P["puestos_por_rrhh"][pr]) * 2 - 1e-9) / 2
    estructura("rrhh", "Recursos humanos (liquidación, selección, capacitación)", "administracion",
               "administracion", "oficinas", rrhh)

    # ---------------- 5.10 Agregados, presencia, pico ----------------
    out = agregar(lst, e, tj, k, pendientes)
    pres_mat = matriz_presencia(lst, tj)
    out.update({"entradas": e, "banda": b, "ritmo": r, "turnos": tj, "puestos": lst, "presencia": pres_mat,
                "pico": pico_en_sitio(pres_mat), "mant_cobertura": cob, "mant_carga": carga,
                "directos_turno": directos_turno, "supervisores_turno": sup_c})
    out["headcount_sensibilidad"] = tuple(out["puestos_equivalentes_internos"] * f for f in FACTOR_COBERTURA_SENSIBILIDAD)
    return out


def _num(x):
    return x or 0.0


def agregar(lst, e, tj, k, pendientes):
    E = e["aves_dia"]
    f_nom = e["factor_cobertura_nomina"]
    fte_i = {g: 0.0 for g in GRUPOS}
    fte_t = {g: 0.0 for g in GRUPOS}
    pe_g = {g: 0.0 for g in GRUPOS}
    drv = {d: 0.0 for d in DRIVERS}
    cat = {}
    for p in lst:
        p["headcount_nomina"] = (None if (f_nom is None or p["puestos_equivalentes"] is None)
                                 else p["puestos_equivalentes"] * f_nom)
        if p["grupo"] not in GRUPOS:
            continue                                  # inspección oficial: fuera de la empresa
        fte_i[p["grupo"]] += _num(p["fte_interno"])
        fte_t[p["grupo"]] += _num(p["fte_tercerizado"])
        pe_g[p["grupo"]] += _num(p["puestos_equivalentes"])
        drv[p["driver"]] += _num(p["fte_interno"]) + _num(p["fte_tercerizado"])
        cat[p["categoria"]] = cat.get(p["categoria"], 0.0) + _num(p["fte_interno"]) + _num(p["fte_tercerizado"])
    fi, ft = sum(fte_i.values()), sum(fte_t.values())
    pe = sum(pe_g.values())
    hp_dir = sum(_num(p["horas_persona_dia"]) for p in lst if p["grupo"] == "directo")
    hp_tot = sum(_num(p["horas_persona_dia"]) for p in lst if p["grupo"] in GRUPOS)
    hc_dia = sum(_num(p["horas_contratadas_dia"]) for p in lst if p["grupo"] in GRUPOS)
    kg_com = k["comestible_a_empaque"] * E
    sim_prod = sum(p["simultaneos"] for p in lst if p["franja"] in ("linea", "tecnica") and p["simultaneos"])
    zonas = {}
    for p in lst:
        if p["franja"] in ("linea", "tecnica") and p["simultaneos"]:
            zonas[p["zona"]] = zonas.get(p["zona"], 0) + p["simultaneos"]
    sup = sum(p["puestos_turno"] for p in lst if p["clave"] in ("supervisores_linea", "jefes_turno"))
    dir_t = sum(p["puestos_turno"] for p in lst if p["grupo"] == "directo" and p["franja"] == "linea")
    fdir = fte_i["directo"] + fte_t["directo"]
    tec = [p for p in lst if p["clave"] == "tecnicos_mantenimiento"]
    n_eq = int(tec[0]["base"].split(" ")[0]) if tec else None
    tec_fte = (_num(tec[0]["fte_interno"]) + _num(tec[0]["fte_tercerizado"])) if tec else 0.0
    funciones = [p for p in lst if p["grupo"] in GRUPOS and (
        _num(p["fte_interno"]) + _num(p["fte_tercerizado"]) > 0 or p["estado"] in ("PENDIENTE", "EXTERNO_POR_SERVICIO"))]
    n_int = sum(1 for p in funciones if _num(p["fte_interno"]) > 0)
    n_ter = sum(1 for p in funciones if _num(p["fte_tercerizado"]) > 0 or p["estado"] == "EXTERNO_POR_SERVICIO")
    n_pen = sum(1 for p in funciones if p["estado"] == "PENDIENTE")

    def kpi(v, den, uni):
        return {"valor": v, "denominador": den, "universo": uni}

    kp = {
        "aves_por_hora_persona_directa": kpi(E / hp_dir if hp_dir else None, "horas-persona/día de puestos directos",
                                             "directos (operación industrial sin limpieza)"),
        "kg_por_hora_persona_directa": kpi(kg_com / hp_dir if hp_dir else None, "horas-persona/día de puestos directos",
                                           "directos; kg comestible (peso comercial, balance v1.1)"),
        "aves_por_hora_persona_total": kpi(E / hp_tot if hp_tot else None,
                                           "horas-persona/día internas + tercerizadas calculadas",
                                           "toda la empresa sin funciones PENDIENTES ni inspección oficial"),
        "fte_directos_por_1000_aves": kpi(fdir / (E / 1000), "1.000 aves faenadas/día operativo", "FTE directos"),
        "fte_totales_por_1000_aves": kpi((fi + ft) / (E / 1000), "1.000 aves faenadas/día operativo",
                                         "FTE internos + tercerizados (sin PENDIENTES)"),
        "ratio_fte_indirecto_directo": kpi(((fi + ft) - fdir) / fdir if fdir else None, "FTE directos",
                                           "FTE internos + tercerizados; informativo, NO dimensiona"),
        "directos_por_supervisor": kpi(dir_t / sup if sup else None, "supervisores de línea por turno",
                                       "puestos directos por turno"),
        "equipos_por_fte_mantenimiento": kpi(n_eq / tec_fte if (n_eq and tec_fte) else None,
                                             "FTE de mantenimiento (interno + tercerizado)", "unidades de equipo (08)"),
    }
    brecha_hp = tj["brecha_jornada_h"] * sum(p["puestos_turno"] * p["cuadrillas"] for p in lst
                                             if p["franja"] == "linea" and p["puestos_equivalentes"])
    return {
        "fte_interno": fte_i, "fte_tercerizado": fte_t, "puestos_equivalentes": pe_g,
        "fte_internos": fi, "fte_tercerizados": ft, "fte_total": fi + ft, "puestos_equivalentes_internos": pe,
        "headcount_nomina": None if f_nom is None else pe * f_nom,
        "horas_persona_dia": hp_tot, "horas_contratadas_dia": hc_dia, "fte_por_driver": drv, "fte_por_categoria": cat,
        "simultaneos_produccion": sim_prod, "zonas_produccion": zonas,
        "funciones": {"internas": n_int, "tercerizadas": n_ter, "pendientes": n_pen, "total": len(funciones)},
        "kpi": kp, "pendientes": sorted(set(pendientes)), "estado": "INCOMPLETO" if pendientes else "COMPLETO",
        "horas_persona_brecha_jornada_dia": brecha_hp,
    }


def matriz_presencia(lst, tj):
    """MATRIZ CONCEPTUAL DE PRESENCIA: puesto → ingreso → duración → salida → franja (h desde el inicio de la
    preparación). Sólo puestos en sitio (internos y terceros en sitio). SUP-14A-18."""
    filas = []
    J = tj["J"]
    for p in lst:
        s = p["simultaneos"]
        if not s or p["franja"] not in FRANJAS_EN_SITIO:
            continue
        if p["franja"] == "linea":
            for i, ini in enumerate(tj["inicios_cuadrillas"]):
                filas.append({"clave": p["clave"], "franja": "linea", "cuadrilla": i + 1, "ingreso": ini,
                              "duracion": tj["presencia_h"], "salida": ini + tj["presencia_h"], "simultaneos": s})
        elif p["franja"] == "tecnica":
            filas.append({"clave": p["clave"], "franja": "tecnica", "cuadrilla": 0, "ingreso": 0.0,
                          "duracion": tj["horas_activos_en_marcha"], "salida": tj["horas_activos_en_marcha"],
                          "simultaneos": s})
            g = P["cobertura_guardia_fuera_produccion"]
            filas.append({"clave": p["clave"] + "_guardia", "franja": "tecnica", "cuadrilla": 0,
                          "ingreso": tj["inicio_limpieza"], "duracion": tj["horas_fuera_produccion"],
                          "salida": tj["fin_mantenimiento"], "simultaneos": g})
        elif p["franja"] == "post":
            filas.append({"clave": p["clave"], "franja": "post", "cuadrilla": 0, "ingreso": tj["inicio_limpieza"],
                          "duracion": tj["fin_limpieza"] - tj["inicio_limpieza"], "salida": tj["fin_limpieza"],
                          "simultaneos": s})
        else:   # diurna: jornada de referencia desde el fin de la preparación
            filas.append({"clave": p["clave"], "franja": "diurna", "cuadrilla": 0, "ingreso": tj["t_preparacion"],
                          "duracion": J, "salida": tj["t_preparacion"] + J, "simultaneos": s})
    return filas


def pico_en_sitio(filas, paso=0.05):
    """Máximo de personas presentes a la vez. Las dedicaciones fraccionarias de la franja diurna se suman y
    se redondean una vez (una persona puede cubrir dos roles de 0,5)."""
    if not filas:
        return {"total": 0, "hora": None, "por_franja": {}}
    fin = max(f["salida"] for f in filas)
    mejor, hora, comp = -1, None, {}
    t = 0.0
    while t <= fin + 1e-9:
        por = {}
        for f in filas:
            if f["ingreso"] - 1e-9 <= t < f["salida"] - 1e-9:
                por[f["franja"]] = por.get(f["franja"], 0) + f["simultaneos"]
        tot = sum(techo(v) if kf == "diurna" else v for kf, v in por.items())
        if tot > mejor:
            mejor, hora, comp = tot, t, {kf: (techo(v) if kf == "diurna" else v) for kf, v in por.items()}
        t = round(t + paso, 6)
    return {"total": mejor, "hora": hora, "por_franja": comp}


def salida_layout(R):
    """Insumo para 09 (vestuarios, comedor, estacionamiento): PICO SIMULTÁNEO, nunca FTE ni headcount."""
    lim = [p for p in R["puestos"] if p["clave"] == "limpieza_sanitizacion"]
    return {"pico_personas_en_sitio": R["pico"]["total"], "hora_del_pico_h": R["pico"]["hora"],
            "simultaneos_produccion_por_zona": dict(R["zonas_produccion"]),
            "cuadrilla_limpieza_simultanea": lim[0]["simultaneos"] if lim else 0,
            "excluye": "inspección oficial (PENDIENTE), choferes en ruta, personal de campo",
            "nota": "agregar margen y requisitos (por zona sucia/limpia y por sexo, DPV-138); no usar FTE"}


# ---------------------------------------------------------------------------
# 6. ESCENARIOS Y CSV
# ---------------------------------------------------------------------------
MODOS_HORAS = (("1", 6.0), ("1", 8.0), ("extendido", 8.0), ("extendido", 10.0), ("2", 12.0), ("2", 16.0))
CAMPOS = [
    "id", "aves_dia", "horas_netas", "turnos", "cuadrillas", "automatizacion", "config", "flota_propia",
    "limpieza", "mantenimiento", "productividad", "ventana", "dias_semana", "planta_propia", "abastecimiento",
    "laboratorio", "banda", "ritmo_aves_h", "presencia_cuadrilla_h", "brecha_jornada_h_persona",
    "horas_persona_brecha_dia", "holgura_24h", "alertas",
    "puestos_directos_turno", "puestos_simultaneos_produccion", "pico_personas_en_sitio", "hora_pico_h",
    "cuadrilla_limpieza_simultanea", "zona_sucia_simult", "zona_evisceracion_simult", "zona_limpia_simult",
    "zona_frio_expedicion_simult", "zona_subproductos_simult", "zona_transversal_simult",
    "puestos_equivalentes_internos", "headcount_nomina", "headcount_sensibilidad_f108", "headcount_sensibilidad_f118",
    "fte_internos", "fte_tercerizados", "fte_total", "horas_persona_dia", "horas_contratadas_dia",
    "fte_directo", "fte_supervision", "fte_soporte", "fte_administracion", "fte_direccion",
    "fte_driver_produccion", "fte_driver_activos", "fte_driver_casi_fijo", "fte_driver_estrategia",
    "mant_fte_cobertura_politica", "mant_fte_carga_activos", "funciones_internas", "funciones_tercerizadas",
    "funciones_pendientes", "funciones_total",
    "kpi_aves_hora_persona_directa", "kpi_kg_hora_persona_directa", "kpi_aves_hora_persona_total",
    "kpi_fte_directos_1000_aves", "kpi_fte_totales_1000_aves", "kpi_ratio_fte_indirecto_directo",
    "kpi_directos_por_supervisor", "kpi_equipos_por_fte_mant", "proxy_12C_turno_medio", "pendientes", "estado",
    "clasificacion",
]


def _r(x, d=3):
    return "" if x is None else round(x, d)


def proxy_12c(E, h, auto, cfg):
    """Dotación proxy por turno de 12C (SUP-116) — sólo para comparar; no se usa."""
    v = ms.P
    a = AUTO_12C[auto]
    return (v["dotacion_base_proxy"]["v"][1] + v["dotacion_por_ave_h_proxy"]["v"][1] * E / h
            * v["factor_dotacion_automatizacion"][a] * v["factor_dotacion_config"][cfg])


def fila_csv(i, R):
    e, tj, kp, z = R["entradas"], R["turnos"], R["kpi"], R["zonas_produccion"]
    fi, ft, dr, f = R["fte_interno"], R["fte_tercerizado"], R["fte_por_driver"], R["funciones"]
    lay = salida_layout(R)
    return {
        "id": i, "aves_dia": e["aves_dia"], "horas_netas": e["horas_netas"], "turnos": e["turnos"],
        "cuadrillas": tj["cuadrillas"], "automatizacion": e["automatizacion"], "config": e["config"],
        "flota_propia": int(e["flota_propia"]), "limpieza": e["limpieza"], "mantenimiento": e["mantenimiento"],
        "productividad": e["productividad"], "ventana": tj["ventana"], "dias_semana": e["dias_semana"],
        "planta_propia": int(e["planta_propia"]), "abastecimiento": e["abastecimiento"], "laboratorio": e["laboratorio"],
        "banda": R["banda"], "ritmo_aves_h": _r(R["ritmo"], 1), "presencia_cuadrilla_h": _r(tj["presencia_h"], 2),
        "brecha_jornada_h_persona": _r(tj["brecha_jornada_h"], 2),
        "horas_persona_brecha_dia": _r(R["horas_persona_brecha_jornada_dia"], 1),
        "holgura_24h": _r(tj["holgura_24h"], 2), "alertas": ";".join(a.split("(")[0] for a in tj["alertas"]),
        "puestos_directos_turno": R["directos_turno"], "puestos_simultaneos_produccion": R["simultaneos_produccion"],
        "pico_personas_en_sitio": lay["pico_personas_en_sitio"], "hora_pico_h": _r(lay["hora_del_pico_h"], 2),
        "cuadrilla_limpieza_simultanea": lay["cuadrilla_limpieza_simultanea"],
        "zona_sucia_simult": z.get("sucia", 0), "zona_evisceracion_simult": z.get("evisceracion", 0),
        "zona_limpia_simult": z.get("limpia", 0), "zona_frio_expedicion_simult": z.get("frio_expedicion", 0),
        "zona_subproductos_simult": z.get("subproductos", 0), "zona_transversal_simult": z.get("transversal", 0),
        "puestos_equivalentes_internos": _r(R["puestos_equivalentes_internos"], 2),
        "headcount_nomina": "PENDIENTE" if R["headcount_nomina"] is None else _r(R["headcount_nomina"], 1),
        "headcount_sensibilidad_f108": _r(R["headcount_sensibilidad"][0], 1),
        "headcount_sensibilidad_f118": _r(R["headcount_sensibilidad"][1], 1),
        "fte_internos": _r(R["fte_internos"], 2), "fte_tercerizados": _r(R["fte_tercerizados"], 2),
        "fte_total": _r(R["fte_total"], 2), "horas_persona_dia": _r(R["horas_persona_dia"], 1),
        "horas_contratadas_dia": _r(R["horas_contratadas_dia"], 1),
        "fte_directo": _r(fi["directo"] + ft["directo"], 2), "fte_supervision": _r(fi["supervision"] + ft["supervision"], 2),
        "fte_soporte": _r(fi["soporte"] + ft["soporte"], 2),
        "fte_administracion": _r(fi["administracion"] + ft["administracion"], 2),
        "fte_direccion": _r(fi["direccion"] + ft["direccion"], 2),
        "fte_driver_produccion": _r(dr["produccion"], 2), "fte_driver_activos": _r(dr["activos"], 2),
        "fte_driver_casi_fijo": _r(dr["casi_fijo"], 2), "fte_driver_estrategia": _r(dr["estrategia"], 2),
        "mant_fte_cobertura_politica": _r(R["mant_cobertura"]["fte"], 2),
        "mant_fte_carga_activos": _r(R["mant_carga"]["fte"], 2),
        "funciones_internas": f["internas"], "funciones_tercerizadas": f["tercerizadas"],
        "funciones_pendientes": f["pendientes"], "funciones_total": f["total"],
        "kpi_aves_hora_persona_directa": _r(kp["aves_por_hora_persona_directa"]["valor"], 1),
        "kpi_kg_hora_persona_directa": _r(kp["kg_por_hora_persona_directa"]["valor"], 1),
        "kpi_aves_hora_persona_total": _r(kp["aves_por_hora_persona_total"]["valor"], 1),
        "kpi_fte_directos_1000_aves": _r(kp["fte_directos_por_1000_aves"]["valor"], 2),
        "kpi_fte_totales_1000_aves": _r(kp["fte_totales_por_1000_aves"]["valor"], 2),
        "kpi_ratio_fte_indirecto_directo": _r(kp["ratio_fte_indirecto_directo"]["valor"], 3),
        "kpi_directos_por_supervisor": _r(kp["directos_por_supervisor"]["valor"], 1),
        "kpi_equipos_por_fte_mant": _r(kp["equipos_por_fte_mantenimiento"]["valor"], 1),
        "proxy_12C_turno_medio": _r(proxy_12c(e["aves_dia"], e["horas_netas"], e["automatizacion"], e["config"]), 1)
        if e["planta_propia"] else "",
        "pendientes": ";".join(R["pendientes"]), "estado": R["estado"], "clasificacion": "[ESTIMACIÓN]",
    }


def grilla():
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


def escenario_referencia(E, pr="media", **extra):
    """Escenario de trabajo para documentos y plantilla (NO es decisión): 1 cuadrilla de 8 h netas en turno
    extendido, automatización de referencia de 09A, config. B, limpieza y mantenimiento propios, flota de
    terceros, capacidad de camión de escenario."""
    d = {"aves_dia": E, "horas_netas": 8.0, "turnos": "extendido", "automatizacion": AUTO_REFERENCIA[E],
         "config": "B", "productividad": pr, "aves_camion": P["aves_camion_escenario"]}
    d.update(extra)
    return d


CAMPOS_COSTO = ["SUELDO_BASE", "CARGAS", "ADICIONALES", "HORAS_EXTRA", "BENEFICIOS", "COSTO_EMPRESA_MENSUAL",
                "COSTO_EMPRESA_ANUAL"]
CAMPOS_PLANTILLA = ["ESCENARIO", "PUESTO", "AREA", "GRUPO", "ZONA", "FRANJA", "MODALIDAD", "PUESTOS_TURNO",
                    "SIMULTANEOS", "PUESTOS_EQUIVALENTES", "HEADCOUNT", "FTE", "HORAS_MES", "TURNOS",
                    "TIPO_CONTRATACION"] + CAMPOS_COSTO + ["MONEDA", "TIPO_CAMBIO_FECHA_FUENTE", "FUENTE", "ESTADO"]


def filas_plantilla(R, nombre):
    """Una fila por puesto y modalidad (interno / tercerizado). HORAS_MES = FTE × jornada × días operativos/mes.
    HEADCOUNT queda PENDIENTE (FACTOR_COBERTURA_NOMINA no validado). Costos VACÍOS."""
    e = R["entradas"]
    dmes = e["dias_semana"] * 52 / 12
    J = R["turnos"]["J"]
    filas = []
    for p in R["puestos"]:
        partes = []
        if p["estado"] == "PENDIENTE":
            partes.append(("PENDIENTE", None))
        else:
            if p["fte_interno"]:
                partes.append(("interno", p["fte_interno"]))
            if p["fte_tercerizado"]:
                partes.append(("tercerizado (horas contratadas)", p["fte_tercerizado"]))
            if p["estado"] == "EXTERNO_POR_SERVICIO":
                partes.append(("servicio externo por unidad", None))
        for mod, fte in partes:
            filas.append({
                "ESCENARIO": nombre, "PUESTO": p["puesto"], "AREA": p["categoria"], "GRUPO": p["grupo"],
                "ZONA": p["zona"], "FRANJA": p["franja"], "MODALIDAD": mod,
                "PUESTOS_TURNO": "" if p["puestos_turno"] is None else p["puestos_turno"],
                "SIMULTANEOS": "" if p["simultaneos"] is None else p["simultaneos"],
                "PUESTOS_EQUIVALENTES": round(p["puestos_equivalentes"], 2) if mod == "interno" else "",
                "HEADCOUNT": "PENDIENTE (FACTOR_COBERTURA_NOMINA)" if mod == "interno" else "no aplica",
                "FTE": "PENDIENTE" if fte is None else round(fte, 3),
                "HORAS_MES": "PENDIENTE" if fte is None else round(fte * J * dmes, 1),
                "TURNOS": p["cuadrillas"],
                "TIPO_CONTRATACION": p["contrato"] if mod == "interno" else (
                    "oficial" if p["grupo"] == "oficial" else "servicio_tercerizado"),
                **{c: "" for c in CAMPOS_COSTO},
                "MONEDA": "USD", "TIPO_CAMBIO_FECHA_FUENTE": "", "FUENTE": "",
                "ESTADO": "COSTO PENDIENTE DE VALIDACIÓN (DPV-14A-03)" + ("; dotación PENDIENTE" if fte is None else ""),
            })
    return filas


def escribir_plantilla(ruta=CSV_PLANTILLA):
    n = 0
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS_PLANTILLA)
        w.writeheader()
        for E in ESCALAS:
            for fila in filas_plantilla(calcular(escenario_referencia(E)), f"REF-{E}"):
                w.writerow(fila)
                n += 1
    return n


# ---------------------------------------------------------------------------
# 7. TESTS
# ---------------------------------------------------------------------------
def _fte_func(p):
    return _num(p["fte_interno"]) + _num(p["fte_tercerizado"])


def _pp(R):
    return {p["clave"]: p for p in R["puestos"]}


def ejecutar_tests(verbose=True):
    res = []

    def ok(nombre, cond, detalle=""):
        res.append((nombre, bool(cond), detalle))

    sub = list(itertools.product(ESCALAS, MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C"), PROD))
    Rs = {}
    for E, (modo, h), auto, cfg, pr in sub:
        Rs[(E, modo, h, auto, cfg, pr)] = calcular({"aves_dia": E, "horas_netas": h, "turnos": modo,
                                                    "automatizacion": auto, "config": cfg, "productividad": pr,
                                                    "aves_camion": P["aves_camion_escenario"]})

    # R01 nada negativo
    campos = ("puestos_turno", "simultaneos", "puestos_equivalentes", "fte_interno", "fte_tercerizado",
              "horas_persona_dia", "horas_contratadas_dia")
    neg = [(k_, p["clave"]) for k_, R in Rs.items() for p in R["puestos"] for c in campos
           if p[c] is not None and p[c] < 0]
    ok("R01 dotación nunca negativa (todas las unidades)", not neg, str(neg[:3]))

    # R02 más escala ⇒ no menos FTE, puestos equivalentes, simultáneos ni pico (mismo nivel, mix y turnos)
    viol = []
    for (modo, h), auto, cfg, pr in itertools.product(MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C"), PROD):
        prev = None
        for E in ESCALAS:
            R = Rs[(E, modo, h, auto, cfg, pr)]
            if prev is not None:
                for c in ("fte_total", "puestos_equivalentes_internos", "simultaneos_produccion"):
                    if R[c] < prev[c] - 1e-9:
                        viol.append((E, modo, h, auto, cfg, pr, c))
                if R["pico"]["total"] < prev["pico"]["total"]:
                    viol.append((E, modo, h, auto, cfg, pr, "pico"))
                for g in GRUPOS:
                    if R["fte_interno"][g] + R["fte_tercerizado"][g] < prev["fte_interno"][g] + prev["fte_tercerizado"][g] - 1e-9:
                        viol.append((E, modo, h, auto, cfg, pr, g))
            prev = R
    ok("R02 más escala ⇒ no menos FTE, puestos, simultáneos ni pico", not viol, str(viol[:3]))

    # R03 automatización no reduce técnicos (cobertura, carga ni reconciliación); R03b reduce directos
    viol = []
    for E, (modo, h), cfg, pr in itertools.product(ESCALAS, MODOS_HORAS, ("A", "B", "C"), PROD):
        prev = None
        for auto in NIVELES_AUTO:
            R = Rs[(E, modo, h, auto, cfg, pr)]
            cur = (_fte_func(_pp(R)["tecnicos_mantenimiento"]), R["mant_carga"]["fte"], R["mant_cobertura"]["fte"])
            if prev is not None and any(c < p_ - 1e-9 for c, p_ in zip(cur, prev)):
                viol.append((E, modo, h, cfg, pr, auto))
            prev = cur
    ok("R03 automatización ⇒ técnicos no disminuyen (cobertura, carga, dotación)", not viol, str(viol[:3]))
    red = all(Rs[(E, "1", 8.0, "automatico", "B", "media")]["directos_turno"]
              < Rs[(E, "1", 8.0, "manual", "B", "media")]["directos_turno"] for E in ESCALAS)
    ok("R03b automatización reduce puestos directos (misma escala y mix)", red)

    # R04 tercerizar retira interno, conserva responsable interno y presencia; asset-light conserva la faena
    base = {"aves_dia": 10000, "aves_camion": P["aves_camion_escenario"]}
    viol = []
    for campo, propio, terc, clave in (("limpieza", "propia", "tercerizada", "limpieza_sanitizacion"),
                                       ("mantenimiento", "propio", "tercerizado", "tecnicos_mantenimiento"),
                                       ("flota_propia", True, False, "choferes_aves")):
        a = calcular(dict(base, **{campo: propio}))
        bb = calcular(dict(base, **{campo: terc}))
        pa_, pb = _pp(a)[clave], _pp(bb)[clave]
        if not (pb["fte_interno"] == 0 and pa_["fte_interno"] > 0 and pb["fte_tercerizado"] > 0
                and pb["horas_contratadas_dia"] > 0 and pb["puestos_equivalentes"] == 0):
            viol.append((campo, "interno/tercerizado"))
        if a["fte_internos"] <= bb["fte_internos"]:
            viol.append((campo, "FTE interno no baja"))
    pt = _pp(calcular(dict(base, limpieza="tercerizada", mantenimiento="tercerizado")))
    for c in ("supervisor_saneamiento", "jefe_mantenimiento"):
        if c not in pt or pt[c]["fte_interno"] < 0.5:
            viol.append(("sin responsable interno", c))
    if pt["limpieza_sanitizacion"]["simultaneos"] <= 0:
        viol.append(("tercerizado desaparece del sitio",))
    al = calcular(dict(base, planta_propia=False))
    if any(p["categoria"] == "operacion_industrial" and p["fte_interno"] for p in al["puestos"]):
        viol.append(("asset-light con directos internos",))
    if not _pp(al)["evisceracion"]["fte_tercerizado"] > 0:
        viol.append(("asset-light borra la faena",))
    ok("R04 tercerizar retira interno y conserva función, responsable y presencia", not viol, str(viol[:3]))

    # R05 ecuación de 24 h y jornada: alertas explícitas, holgura idéntica a 09A
    viol = []
    for R in Rs.values():
        tj = R["turnos"]
        v24 = mc.ventana_24h(R["entradas"]["horas_netas"], tj["ventana"], turnos=tj["cuadrillas"])
        if abs(v24["holgura"] - tj["holgura_24h"]) > 1e-9:
            viol.append("holgura distinta de 09A")
        if (tj["holgura_24h"] < 0) != any(a.startswith("ALERTA_24H") for a in tj["alertas"]):
            viol.append("alerta 24 h")
        if tj["brecha_jornada_h"] > 0 and not any(a.startswith(("INCOMPATIBILIDAD_JORNADA", "JORNADA_EXTENDIDA"))
                                                   for a in tj["alertas"]):
            viol.append("brecha sin alerta")
    ok("R05 24 h y jornada con alerta explícita (09A idéntica)", not viol, str(viol[:3]))

    # R06 escenarios independientes
    a1 = calcular({"aves_dia": 5000})
    calcular({"aves_dia": 20000, "automatizacion": "automatico", "turnos": "2", "horas_netas": 16.0,
              "limpieza": "tercerizada", "flota_propia": True, "aves_camion": 5500, "factor_cobertura_nomina": 1.2})
    a2 = calcular({"aves_dia": 5000})
    ent = {"aves_dia": 2500}
    ent_c = copy.deepcopy(ent)
    P0 = copy.deepcopy(P)
    calcular(ent)
    ok("R06 escenarios independientes", a1["fte_total"] == a2["fte_total"] and a1["pico"] == a2["pico"]
       and a2["headcount_nomina"] is None and ent == ent_c and P == P0
       and ESCENARIO_BASE["factor_cobertura_nomina"] is None)

    # R07 faltantes quedan PENDIENTE
    R = calcular({"aves_dia": 10000, "flota_propia": True})
    pp = _pp(R)
    ok("R07 faltantes PENDIENTE (choferes, inspección, HyS, captura)",
       pp["choferes_aves"]["fte_interno"] is None and pp["choferes_producto"]["fte_interno"] is None
       and pp["inspeccion_oficial"]["fte_tercerizado"] is None and pp["hys_externo"]["fte_tercerizado"] is None
       and pp["captura"]["fte_tercerizado"] is None and R["estado"] == "INCOMPLETO"
       and {"choferes_aves", "choferes_producto", "inspeccion_oficial", "hys_externo", "captura"} <= set(R["pendientes"]))

    # R08 entradas inválidas
    malos = [{"aves_dia": -1}, {"aves_dia": 0}, {"horas_netas": 0}, {"horas_netas": 25}, {"turnos": "3"},
             {"automatizacion": "robot"}, {"limpieza": "nadie"}, {"config": "Z"}, {"aves_camion": -5},
             {"dias_semana": 7}, {"factor_cobertura_nomina": 0.8}]
    rech = 0
    for m in malos:
        try:
            calcular(m)
        except ErrorRRHH:
            rech += 1
    ok("R08 entradas inválidas rechazadas", rech == len(malos), f"{rech}/{len(malos)}")

    # R09 puestos equivalentes = puestos × cuadrillas en roles de línea internos
    viol = [p["clave"] for R in Rs.values() for p in R["puestos"]
            if p["franja"] == "linea" and p["fte_interno"]
            and abs(p["puestos_equivalentes"] - p["puestos_turno"] * p["cuadrillas"]) > 1e-9]
    ok("R09 puestos equivalentes = puestos por turno × cuadrillas", not viol, str(viol[:3]))

    # R10 agregados consistentes
    viol = [k_ for k_, R in Rs.items()
            if abs(sum(R["fte_interno"].values()) - R["fte_internos"]) > 1e-9
            or abs(R["fte_internos"] + R["fte_tercerizados"] - R["fte_total"]) > 1e-9
            or abs(sum(R["fte_por_driver"].values()) - R["fte_total"]) > 1e-9
            or abs(R["horas_persona_dia"] / P["jornada_referencia_h"] - R["fte_total"]) > 1e-6]
    ok("R10 agregados consistentes (FTE = horas-persona / jornada)", not viol, str(viol[:3]))

    # R11 KPI múltiples, positivos
    kp = Rs[(10000, "1", 8.0, "semiautomatico", "B", "media")]["kpi"]
    ok("R11 KPI múltiples presentes y positivos", all(v["valor"] and v["valor"] > 0 for v in kp.values()))

    # R12 09A intacto
    ok("R12 09A intacto (horas netas máx. 16,57 / 13,77 / 10,00)",
       abs(mc.horas_netas_max_24h("optimista") - 16.57) < 0.011 and abs(mc.horas_netas_max_24h("media") - 13.77) < 0.011
       and abs(mc.horas_netas_max_24h("conservadora") - 10.0) < 0.011)

    # R13 rangos ordenados alta ≤ baja (FTE total, simultáneos de producción y puestos por tarea)
    viol = []
    for E, (modo, h), auto, cfg in itertools.product(ESCALAS, MODOS_HORAS, NIVELES_AUTO, ("A", "B", "C")):
        a_, b_ = Rs[(E, modo, h, auto, cfg, "alta")], Rs[(E, modo, h, auto, cfg, "baja")]
        # el pico NO se exige ordenado: depende de cuándo cae el traspaso respecto de la franja diurna
        if a_["fte_total"] > b_["fte_total"] + 1e-9 or a_["simultaneos_produccion"] > b_["simultaneos_produccion"]:
            viol.append((E, modo, h, auto, cfg, "total"))
        pb = _pp(b_)
        for p in a_["puestos"]:
            q = pb.get(p["clave"])
            if q and p["puestos_turno"] is not None and q["puestos_turno"] is not None and p["puestos_turno"] > q["puestos_turno"]:
                viol.append((E, modo, h, auto, cfg, p["clave"]))
    ok("R13 rangos ordenados (alta ≤ baja)", not viol, str(viol[:3]))

    # R14 mix: sala limpia A ≤ B ≤ C
    viol = []
    for E, auto in itertools.product(ESCALAS, NIVELES_AUTO):
        z = [Rs[(E, "1", 8.0, auto, c, "media")]["zonas_produccion"].get("limpia", 0) for c in ("A", "B", "C")]
        if not z[0] <= z[1] <= z[2]:
            viol.append((E, auto, z))
    ok("R14 mix: limpia A ≤ B ≤ C", not viol, str(viol[:3]))

    # ---------- auditoría de unidades ----------
    # R15 headcount, FTE, simultáneos y puestos son variables distintas; headcount PENDIENTE sin factor
    R = Rs[(20000, "extendido", 8.0, "automatico", "B", "media")]
    lim = _pp(R)["limpieza_sanitizacion"]
    distintas = (R["headcount_nomina"] is None and all(p["headcount_nomina"] is None for p in R["puestos"])
                 and abs(R["fte_total"] - R["puestos_equivalentes_internos"]) > 1e-6
                 and R["pico"]["total"] != round(R["fte_total"])
                 and lim["simultaneos"] != lim["fte_interno"])
    Rf = calcular(escenario_referencia(20000, factor_cobertura_nomina=1.15))
    distintas = (distintas and Rf["headcount_nomina"] is not None
                 and abs(Rf["headcount_nomina"] - Rf["puestos_equivalentes_internos"] * 1.15) < 1e-9
                 and abs(Rf["headcount_nomina"] - Rf["fte_internos"] * 1.15) > 1e-6)
    ok("R15 headcount ≠ FTE ≠ simultáneos ≠ puestos; headcount PENDIENTE sin factor y nunca desde FTE", distintas)

    # R16 cuadrilla parcial: FTE = simultáneos × horas / jornada (< simultáneos si horas < jornada)
    viol = []
    for R in Rs.values():
        q = _pp(R)["limpieza_sanitizacion"]
        esperado = q["simultaneos"] * q["horas_presencia"] / P["jornada_referencia_h"]
        if abs(_fte_func(q) - esperado) > 1e-9 or (q["horas_presencia"] < P["jornada_referencia_h"]
                                                    and _fte_func(q) >= q["simultaneos"]):
            viol.append(R["entradas"]["aves_dia"])
    ok("R16 cuadrilla parcial no se cuenta como igual número de FTE", not viol, str(viol[:3]))

    # R17 tercerizar no elimina horas de trabajo (horas-persona de la función idénticas en toda modalidad)
    viol = []
    for E in ESCALAS:
        for campo, ops_, clave in (("limpieza", OPCIONES["limpieza"], "limpieza_sanitizacion"),
                                   ("mantenimiento", OPCIONES["mantenimiento"], "tecnicos_mantenimiento"),
                                   ("flota_propia", (True, False), "choferes_aves")):
            ps = [_pp(calcular(escenario_referencia(E, **{campo: o})))[clave] for o in ops_]
            hs = [p["horas_persona_dia"] for p in ps]
            fts = [_fte_func(p) for p in ps]
            if max(hs) - min(hs) > 1e-9 or max(fts) - min(fts) > 1e-9:
                viol.append((E, campo, hs))
    ok("R17 tercerizar no elimina horas de trabajo (pasan a horas contratadas)", not viol, str(viol[:3]))

    # R18 sin horas extra automáticas: no hay variable de horas extra; "1" y "extendido" = mismas horas
    claves_r = set(CAMPOS)
    for R in list(Rs.values())[::50]:
        claves_r |= set(R) | set(R["turnos"])
    sin_he = not any("extra" in c for c in claves_r)
    for E in ESCALAS:
        a_, b_ = calcular({"aves_dia": E, "turnos": "1"}), calcular({"aves_dia": E, "turnos": "extendido"})
        sin_he = sin_he and abs(a_["fte_total"] - b_["fte_total"]) < 1e-9 and a_["pico"] == b_["pico"]
    ok("R18 sin horas extra automáticas (sólo brecha de jornada)", sin_he)

    # R19 mantenimiento separa cobertura (política) y carga (activos)
    R1 = calcular({"aves_dia": 10000})
    Pm = copy.deepcopy(P)
    P["cobertura_umbrales"] = (10**9, 10**9)
    R2 = calcular({"aves_dia": 10000})
    P.clear()
    P.update(Pm)
    sep = (abs(R1["mant_carga"]["fte"] - R2["mant_carga"]["fte"]) < 1e-12
           and R2["mant_cobertura"]["fte"] < R1["mant_cobertura"]["fte"]
           and abs(_fte_func(_pp(R1)["tecnicos_mantenimiento"])
                   - max(R1["mant_carga"]["fte"], R1["mant_cobertura"]["fte"])) < 1e-9)
    ok("R19 mantenimiento: cobertura y carga separadas; dotación = máx(ambas)", sep)

    # R20 layout recibe el pico simultáneo (no FTE ni headcount)
    viol = []
    for R in list(Rs.values())[::37]:
        lay = salida_layout(R)
        mx = pico_en_sitio(matriz_presencia(R["puestos"], R["turnos"]))["total"]
        if lay.get("pico_personas_en_sitio") != mx or lay["pico_personas_en_sitio"] < R["simultaneos_produccion"]:
            viol.append(R["entradas"]["aves_dia"])
        if any(k_.startswith(("fte", "headcount")) for k_ in lay):
            viol.append("layout con FTE/headcount")
    ok("R20 layout recibe pico simultáneo (matriz de presencia), no FTE", not viol, str(viol[:3]))

    # R21 KPI declaran denominador y universo
    ok("R21 KPI con denominador y universo declarados",
       all(v.get("denominador") and v.get("universo") for R in list(Rs.values())[:50] for v in R["kpi"].values()))

    # R22 plantilla de costos sin salarios ni headcount numérico
    filas = []
    for E in ESCALAS:
        filas += filas_plantilla(calcular(escenario_referencia(E)), f"REF-{E}")
    sin_sal = all(all(f[c] == "" for c in CAMPOS_COSTO) for f in filas) and \
        all(not str(f["HEADCOUNT"]).replace(".", "").isdigit() for f in filas)
    if os.path.exists(CSV_PLANTILLA):
        with open(CSV_PLANTILLA, encoding="utf-8") as fh:
            filas_d = list(csv.DictReader(fh))
        sin_sal = sin_sal and all(c in filas_d[0] for c in CAMPOS_COSTO) and \
            all(all(x[c] == "" for c in CAMPOS_COSTO) for x in filas_d)
    ok("R22 plantilla de costos sin salarios ni headcount numérico", sin_sal)

    # R23 inspección oficial fuera de la nómina y de los FTE de la empresa
    R = Rs[(10000, "1", 8.0, "semiautomatico", "B", "media")]
    io_ = _pp(R)["inspeccion_oficial"]
    ok("R23 SENASA separada de la empresa (no suma FTE, puestos ni pico)",
       io_["grupo"] == "oficial" and io_["fte_interno"] == 0 and io_["puestos_equivalentes"] == 0
       and io_["franja"] not in FRANJAS_EN_SITIO)

    if verbose:
        for n, c, d in res:
            print(f"  [{'OK' if c else 'FALLA'}] {n}" + (f" — {d}" if (d and not c) else ""))
        print(f"  {sum(c for _, c, _ in res)}/{len(res)} tests OK")
    return all(c for _, c, _ in res), res


def prueba_mutaciones():
    """Introduce errores deliberados y verifica que algún test los detecta."""
    original_P = copy.deepcopy(P)
    orig = {n: globals()[n] for n in ("calcular", "salida_layout", "turnos_y_jornada", "filas_plantilla")}
    mut = []

    def restaurar():
        P.clear()
        P.update(copy.deepcopy(original_P))
        globals().update(orig)
        for f in (m2_proceso, logistica_vivo, logistica_producto):
            f.cache_clear()

    def envolver(fn):
        def c2(entradas=None):
            return fn(orig["calcular"](entradas), entradas or {})
        globals()["calcular"] = c2

    def m_rellena():
        def f(R, ent):
            for p in R["puestos"]:
                if p["estado"] == "PENDIENTE":
                    p["fte_interno"] = p["fte_tercerizado"] = 1.0
            R["pendientes"], R["estado"] = [], "COMPLETO"
            return R
        envolver(f)

    def m_silencio():
        def f(R, ent):
            R["turnos"]["alertas"] = []
            return R
        envolver(f)

    def m_borra():
        def f(R, ent):
            if ent.get("limpieza") == "tercerizada":
                R["puestos"] = [p for p in R["puestos"] if p["clave"] != "supervisor_saneamiento"]
            return R
        envolver(f)

    def m_headcount_fte():
        def f(R, ent):
            R["headcount_nomina"] = R["fte_internos"]
            return R
        envolver(f)

    def m_parcial():
        def f(R, ent):
            for p in R["puestos"]:
                if p["clave"] == "limpieza_sanitizacion":
                    if p["fte_interno"]:
                        p["fte_interno"] = float(p["simultaneos"])
                    else:
                        p["fte_tercerizado"] = float(p["simultaneos"])
            return R
        envolver(f)

    def m_terc_borra_horas():
        def f(R, ent):
            for p in R["puestos"]:
                if p["clave"] == "limpieza_sanitizacion" and p["fte_tercerizado"]:
                    p["fte_tercerizado"] = p["horas_contratadas_dia"] = 0.0
                    p["horas_persona_dia"] = p["fte_interno"] * P["jornada_referencia_h"]
            return R
        envolver(f)

    def m_horas_extra():
        def tj2(e):
            t = orig["turnos_y_jornada"](e)
            t["horas_extra_mes"] = max(0, t["presencia_h"] - 8) * 22
            return t
        globals()["turnos_y_jornada"] = tj2

    def m_layout_fte():
        globals()["salida_layout"] = lambda R: {"pico_personas_en_sitio": round(R["fte_total"]),
                                                "fte_total": R["fte_total"]}

    def m_salario():
        def fp(R, n):
            fs = orig["filas_plantilla"](R, n)
            for x in fs:
                x["SUELDO_BASE"] = "1000"
            return fs
        globals()["filas_plantilla"] = fp

    casos = [
        ("rangos invertidos (span)", lambda: P["span_supervision"].update({"alta": 5})),
        ("automatización reduce mantenimiento", lambda: P["mant_h_semana_equipo"].update({"A": T(0.0, 0.0, 0.0)})),
        ("coeficiente negativo", lambda: P["faena_por_1000"].update({"A": T(-5, -5, -5)})),
        ("mix invertido", lambda: P["deshuese_kg_h"].update({"M": T(1e9, 1e9, 1e9), "S": T(1e9, 1e9, 1e9), "A": T(1e9, 1e9, 1e9)})
         or P["trozado_kg_h"].update({k_: T(1e9, 1e9, 1e9) for k_ in ("M", "Mc", "S", "A")})
         or P["empaque_kg_h"].update({"A": T(1, 1, 1)})),
        ("faltantes rellenados", m_rellena), ("alertas silenciadas", m_silencio),
        ("tercerización borra la función", m_borra), ("headcount desde FTE", m_headcount_fte),
        ("cuadrilla parcial = FTE", m_parcial), ("tercerizar elimina horas", m_terc_borra_horas),
        ("horas extra automáticas", m_horas_extra), ("layout recibe FTE", m_layout_fte),
        ("plantilla con salario", m_salario),
    ]
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
# 8. TABLAS
# ---------------------------------------------------------------------------
def fmt(x, d=0):
    if x is None:
        return "PEND."
    s = f"{x:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_tablas():
    print("\n## Escenario de referencia (1 cuadrilla, 8 h netas en turno extendido; auto. 09A; B; propios; flota de terceros)")
    print("| Escala | Puestos simultáneos de producción | Pico en sitio | Puestos equivalentes internos | Headcount de nómina "
          "| FTE internos | FTE tercerizados | Funciones (int./terc./pend./total) |")
    print("|---|---|---|---|---|---|---|---|")
    for E in ESCALAS:
        R = calcular(escenario_referencia(E))
        f = R["funciones"]
        print(f"| {fmt(E)} | {R['simultaneos_produccion']} | {R['pico']['total']} | "
              f"{fmt(R['puestos_equivalentes_internos'], 1)} | PENDIENTE | {fmt(R['fte_internos'], 1)} | "
              f"{fmt(R['fte_tercerizados'], 1)} | {f['internas']}/{f['tercerizadas']}/{f['pendientes']}/{f['total']} |")


def imprimir_detalle(E, pr="media"):
    R = calcular(escenario_referencia(E, pr))
    print(f"\n### Detalle REF-{E}")
    for p in R["puestos"]:
        print(f"  {p['clave']:<26} {p['grupo']:<14} {p['franja']:<13} t={p['puestos_turno']} sim={p['simultaneos']} "
              f"pe={fmt(p['puestos_equivalentes'], 2)} fte_i={fmt(p['fte_interno'], 2)} "
              f"fte_t={fmt(p['fte_tercerizado'], 2)} hp={fmt(p['horas_persona_dia'], 1)} {p['base']}")
    print("  pico:", R["pico"])
    for f in R["presencia"]:
        print(f"   {f['clave']:<28} {f['franja']:<8} c{f['cuadrilla']} {f['ingreso']:5.2f} → {f['salida']:5.2f} "
              f"({f['duracion']:.2f} h) × {f['simultaneos']}")


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
