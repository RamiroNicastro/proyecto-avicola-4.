#!/usr/bin/env python3
"""
MOTOR OPEX + CAPITAL DE TRABAJO — versión 1.1 (2026-10-02, sesión 17 + auditoría de completitud y costo laboral)
=================================================================================================================

v1.1: cada fila tiene MODULO_ARQ y BLOQUE operativo; la matriz `completitud_arquitecturas_opex.csv` verifica que todo
módulo propio tenga sus bloques materiales (aunque estén PENDIENTES) y separa cobertura ESTRUCTURAL ("sé qué costos
existen"), FÍSICA (cantidades) y de COSTEO ("sé cuánto cuestan"); ARQUITECTURA_COSTEABLE bloquea totales y costos
unitarios; montos parciales rotulados MONTOS_PARCIALES_E4_NO_COMPARABLES; RRHH industrial (14A) separado de los
universos upstream no dimensionados (FTE_TOTAL_CONOCIDO vs FTE_ADICIONAL_PENDIENTE); utilities por universo (09C = faena);
el SAC es una regla laboral (`reglas_laborales_opex.csv`), no un precio; precio observado ≠ conversión USD.

¿CUÁNTO CUESTA OPERAR CADA CONFIGURACIÓN DEL PROYECTO Y CUÁNTO CAPITAL QUEDA INMOVILIZADO EN LA OPERACIÓN?

El motor NO elige escala, arquitectura, make-or-buy ni proveedor. Para cada configuración arma el REGISTRO DE
COSTOS OPERATIVOS (una fila por concepto) con CANTIDADES consumidas de los módulos físicos aprobados y PRECIOS
leídos de una base externa (`base_costos_opex.csv`). Si un concepto no tiene precio o cantidad queda PENDIENTE:
nunca se reemplaza por cero y nunca se publica un "OPEX total" con faltantes.

QUÉ NO HACE: ingresos, EBITDA, VAN/TIR/payback, depreciación, impuesto a las ganancias, IVA definitivo, CAPEX
(19_capex), recomendación de escala, arquitectura o integración, precios argentinos inventados.

PRINCIPIO
  COSTO = DRIVER FÍSICO (cantidad/año, de 03 · 04 · 05 · 09C · 12B · 14A · 14B · 19_capex)
          × PRECIO UNITARIO (base_costos_opex.csv; USD = original ÷ TC declarado)

INSUMOS IMPORTADOS (no se recalculan; se llaman las funciones de cada módulo):
  * 19_capex/modelo_capex.py (16): presets C0–C3/CF, validación de arquitectura, BOQ por bloque (base de
    mantenimiento) y, a través de él, 12C, 09C (agua, efluente, kWh, térmico, frío), 12B (flota) y 14B.
  * 14_alimento_balanceado/modelo_upstream.py (14B, que consume 03): pollitos, huevos, incubación, alimento,
    composición ilustrativa de materias primas, inventarios por categoría y PROPIETARIO.
  * 13_logistica/modelo_logistica.py (12B): viajes, km y t por flujo con capacidades de ESCENARIO.
  * 18_recursos_humanos/modelo_rrhh.py (14A): puestos, FTE, horas, modalidad (interno / tercerizado).
  * 05_proceso_industrial (kg comestible a empaque por ave) y 04_balance_masa (decomisos).

FÓRMULAS
  costo_concepto (USD/año) = cantidad_anual × precio_USD                    (solo si ambos existen)
  precio_USD               = precio_original ÷ TC_MONEDA_POR_USD             (TC, tipo y fecha obligatorios)
  porcentaje (mantenimiento %CAPEX) = % × base CAPEX del bloque              (base sin precio → PENDIENTE)
  costo empresa por FTE    = salario × meses × (1 + adicionales%) × (1 + cargas% + ART%) + beneficios × 12
                             + EPP + capacitación                            (cualquier componente vacío → PENDIENTE)
  costo laboral interno    = FTE (14A) × costo empresa por FTE              (PROVISIONAL POR FTE; headcount PENDIENTE)
  costo tercerizado        = horas contratadas (14A) × tarifa horaria
  ramp-up                  = variable × u ; fijo y semifijo × 1 ; semivariable según % variable (si existe)
  CTO = inventarios propios + cuentas por cobrar + caja operativa − cuentas por pagar   (faltante → PENDIENTE)
  cuentas por cobrar = ventas × días de cobro ÷ 365 ; cuentas por pagar = compras × días de pago ÷ 365

Uso
---
    python3 20_opex/modelo_opex.py                  # tests + CSV de salida
    python3 20_opex/modelo_opex.py --solo-tests
    python3 20_opex/modelo_opex.py --mutaciones     # los tests detectan errores sembrados
    python3 20_opex/modelo_opex.py --escenario --config C3 --aves-dia 10000
    python3 20_opex/modelo_opex.py --escenario --config C1 --aves-dia 5000 --costos mi_base.csv

El script se DETIENE (código 1) si falla cualquier prueba. Unidades métricas; CSV con punto decimal.
IDs provisionales: SUP-17-##, DPV-17-##, DEC-17-##, FTE-17-### (ver actualizaciones_gestion_17.md).
"""
import argparse
import copy
import csv
import io
import math
import os
import re
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _d in ("19_capex", "18_recursos_humanos", "04_balance_masa"):
    _p = os.path.join(RAIZ, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
with redirect_stdout(io.StringIO()):
    import modelo_capex as mcx          # noqa: E402  (16 → 12C, 09C, 12B, 14B, 05, 08)
    import modelo_rrhh as mr            # noqa: E402  (14A)
    import modelo_balance_masa as mb    # noqa: E402  (04)
ms, ml, mup = mcx.ms, mcx.ml, mcx.mup

VERSION = "1.1"
FECHA = "2026-10-02"
FUENTE = "20_opex/modelo_opex.py"
FECHA_BASE_OPEX = "2026-10-01"                 # SUP-17-01: editable (--fecha-base); sin indexación automática
MONEDA = "USD"
ARCHIVO_COSTOS = os.path.join(AQUI, "base_costos_opex.csv")
SALIDA_REG = os.path.join(AQUI, "registro_costos_operativos.csv")
SALIDA_ESC = os.path.join(AQUI, "escenarios_opex.csv")
SALIDA_MAPA = os.path.join(AQUI, "mapa_drivers_opex.csv")
SALIDA_LAB = os.path.join(AQUI, "modelo_costo_laboral.csv")
SALIDA_CT = os.path.join(AQUI, "capital_trabajo_opex.csv")
SALIDA_MATRIZ = os.path.join(AQUI, "matriz_validacion_opex.csv")
SALIDA_COMP = os.path.join(AQUI, "completitud_arquitecturas_opex.csv")

ESCALAS_REF = mcx.ESCALAS_REF
PESO_REF = 2.9                                 # perfil medio de 03/14B (SUP-027): único publicado por las fuentes
EVIDENCIAS = ("E1", "E2", "E3", "E4", "E5")
NIVELES_EVIDENCIA = EVIDENCIAS + ("PENDIENTE",)
GRUPOS_EVIDENCIA = {"E1_E2": ("E1", "E2"), "E3": ("E3",), "E4": ("E4",), "E5": ("E5",)}
NATURALEZAS = ("variable", "fijo", "semifijo", "semivariable")
CENTROS = ("produccion_primaria", "incubacion", "alimento", "faena", "frio", "mantenimiento", "calidad", "logistica",
           "administracion", "comercial", "servicios_generales", "terceros")
TIPOS = ("interno", "tercerizado", "comprado", "propio")
APORTANTES = ("EMPRESA", "PRODUCTOR_INTEGRADO", "TERCERO", "PENDIENTE")
FASES = ("OPERACION", "FUTURO", "OPCIONAL_MERCADO")
ESTADOS_DIM = ("DIMENSIONADO", "PENDIENTE", "INCLUIDO", "INFORMATIVO")
ESTADOS_BASE = ("PENDIENTE", "CON_PRECIO", "REFERENCIA", "DESCARTADO", "FUTURO", "OPCIONAL")
TIPOS_DRIVER = ("DIRECTO", "CALCULO_MODELO_FUENTE", "CONSUMIDO_CAPEX", "DERIVADO_OPEX", "SUPUESTO_OPEX", "PENDIENTE")
UNIDADES_PCT = ("%", "meses")
TOL = 1e-9
_MUT: set = set()

# Flujos logísticos de OPEX: código → (nombre, flujo de CAPEX que define propia/tercero, unidad física de tarifa)
FLUJOS = {"POL": ("pollitos", "pollitos", "pollito"), "HUE": ("huevos", "pollitos", "huevo"),
          "ALI": ("alimento", "alimento", "t"), "GRA": ("grano", "alimento", "t"), "VIV": ("vivo", "vivo", "t"),
          "REF": ("refrigerado", "refrigerado", "t"), "CON": ("congelado", "congelado", "t"),
          "SUB": ("subproductos", "subproductos", "t")}
MODELOS_TARIFA = ("viaje", "km", "unidad", "contrato")
METODOS_MANT = ("pct_capex", "por_activo", "horas_tecnicas", "contrato")
AREAS_MANT = ("PROC", "FRIO", "ELEC", "UTIL", "EDIF", "INC", "ALI", "GRA")
TIPOS_MANT_POR_METODO = {"por_activo": ("PREV", "CORR", "REP", "LUB"), "horas_tecnicas": ("STEC",), "contrato": ("CONT",),
                         "pct_capex": ("PCT",)}
AUTO_RRHH = {"manual": "manual", "semi": "semiautomatico", "auto": "automatico"}
COMBUSTIBLES = {"gas_natural": ("UT-TER-GN", "equivalente_gas_natural_m3_dia", "m³"),
                "glp": ("UT-TER-GLP", "equivalente_glp_kg_dia", "kg"),
                "biomasa": ("UT-TER-BIO", "equivalente_biomasa_chip_kg_dia", "kg")}
GRUPOS_CXP = ("alimento", "pollitos", "granos", "servicios", "packaging", "logistica", "energia")
# SUP-17-04: esquema de integración descripto en 03 (modelos_integracion.md): qué aporta cada parte en una granja
# INTEGRADA. No es un contrato: es editable y lo que 03 deja "según contrato" queda PENDIENTE.
APORTES_03 = {"pollito": "EMPRESA", "alimento": "EMPRESA", "sanidad": "EMPRESA", "asistencia_tecnica": "EMPRESA",
              "logistica_insumos": "EMPRESA", "mano_obra_granja": "PRODUCTOR_INTEGRADO",
              "electricidad_granja": "PRODUCTOR_INTEGRADO", "agua_granja": "PRODUCTOR_INTEGRADO",
              "gas_calefaccion": "PENDIENTE", "cama": "PENDIENTE", "captura": "PENDIENTE",
              "mortalidad_retiro": "PENDIENTE", "limpieza_galpon": "PENDIENTE", "bioseguridad": "PENDIENTE"}
# Ramp-up: etapas sin factores definitivos (SUP-17-09). None = PENDIENTE; finanzas carga la curva.
ETAPAS_RAMPUP = {"arranque": None, "estabilizacion": None, "madura": 1.0}

OPEX_DEFAULTS = {
    "utilizacion": 1.0, "etapa": "madura", "peso_kg": PESO_REF, "fecha_base_opex": FECHA_BASE_OPEX, "moneda_opex": MONEDA,
    "alimento_facon_mp": None,           # None | "empresa" | "elaborador" (variante del façon: DEC-17-02)
    "composicion_alimento": None,        # None = puntos ilustrativos de 14B; dict de fracciones (suma 1) = SUPUESTO
    "aportes_integracion": None,         # None = APORTES_03
    "base_pago_integrado": None,         # None | "ave" | "kg_vivo" (contrato no definido)
    "facon_aporta_empaque": None,        # None (PENDIENTE) | True (lo pone la empresa) | False (incluido en la tarifa)
    "combustible_termico": None,         # None | gas_natural | glp | biomasa
    "fuente_agua": None,                 # None | red | pozo
    "modelo_tarifa_flete": None,         # None | modelo | {código de flujo: modelo}
    "mantenimiento_metodo": None,        # None | pct_capex | por_activo | horas_tecnicas | contrato (no se mezclan)
    "limpieza_modalidad": "propia", "mantenimiento_modalidad": "propio",   # 14A ESCENARIO_BASE
    "turnos": "extendido", "productividad": "media",                        # 14A escenario_referencia
    "rrhh_cap_camion_producto_t": "capex", "rrhh_dist_producto_km": "capex",
    "modulo_halal": False,
    "ventas_anuales_usd": None, "dias_cobro": None, "dias_pago": None, "dias_caja_operativa": None,
    "dias_stock_envases": None, "dias_stock_repuestos": None, "dias_stock_insumos": None,
}


class ErrorOpex(Exception):
    pass


# ---------------------------------------------------------------------------------------------
# 1. CONFIGURACIÓN
# ---------------------------------------------------------------------------------------------
def config_opex(nombre=None, **kw):
    """Configuración = arquitectura de CAPEX (preset o por defecto) + parámetros de OPEX. No es decisión."""
    c = mcx.preset(nombre) if nombre else mcx.config_por_defecto()
    c.update(copy.deepcopy(OPEX_DEFAULTS))
    c.update(kw)
    return c


def config_capex(c):
    return {k: copy.deepcopy(c[k]) for k in mcx.config_por_defecto()}


def aportes(c):
    a = dict(APORTES_03)
    a.update(c["aportes_integracion"] or {})
    return a


def validar_config_opex(c):
    mcx.validar_config(config_capex(c))
    if abs(c["peso_kg"] - PESO_REF) > TOL:
        raise ErrorOpex("peso distinto de 2,9 kg: los módulos fuente (03/14B) solo publican el perfil medio; OPEX no "
                        "recalcula drivers (cambiar el peso exige correr 03, 04, 09C, 12B y 14B con otro perfil)")
    if not 0 < c["utilizacion"] <= 1:
        raise ErrorOpex("utilización en (0, 1]")
    if c["moneda_opex"] != MONEDA:
        raise ErrorOpex("moneda del modelo: USD (regla 2); otras monedas solo como original")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c["fecha_base_opex"])):
        raise ErrorOpex("FECHA_BASE_OPEX debe ser AAAA-MM-DD")
    if c["alimento_facon_mp"] not in (None, "empresa", "elaborador"):
        raise ErrorOpex("alimento_facon_mp: None | empresa | elaborador")
    if c["alimento_facon_mp"] is not None and c["alimento"] != "facon":
        raise ErrorOpex("alimento_facon_mp solo aplica con alimento = facon")
    if c["base_pago_integrado"] not in (None, "ave", "kg_vivo"):
        raise ErrorOpex("base_pago_integrado: None | ave | kg_vivo")
    if c["combustible_termico"] not in (None,) + tuple(COMBUSTIBLES):
        raise ErrorOpex(f"combustible_termico: None | {tuple(COMBUSTIBLES)}")
    if c["fuente_agua"] not in (None, "red", "pozo"):
        raise ErrorOpex("fuente_agua: None | red | pozo")
    mt = c["modelo_tarifa_flete"]
    vals = mt.values() if isinstance(mt, dict) else [mt]
    if any(v not in (None,) + MODELOS_TARIFA for v in vals) or (isinstance(mt, dict) and set(mt) - set(FLUJOS)):
        raise ErrorOpex(f"modelo_tarifa_flete: un modelo por flujo entre {MODELOS_TARIFA} (no se mezclan)")
    if c["mantenimiento_metodo"] not in (None,) + METODOS_MANT:
        raise ErrorOpex(f"mantenimiento_metodo: None | {METODOS_MANT} (un solo método)")
    if c["limpieza_modalidad"] not in mr.OPCIONES["limpieza"] or c["mantenimiento_modalidad"] not in mr.OPCIONES["mantenimiento"]:
        raise ErrorOpex("limpieza / mantenimiento: opciones de 14A")
    comp = c["composicion_alimento"]
    if comp is not None:
        if set(comp) - {"maiz", "harina_soja", "aceite", "nucleo", "otros", "resto"} or abs(sum(comp.values()) - 1) > 1e-6 \
                or any(v < 0 for v in comp.values()) or ("resto" in comp and set(comp) & {"aceite", "nucleo", "otros"}):
            raise ErrorOpex("composicion_alimento: fracciones ≥ 0 que suman 1; 'resto' excluye aceite/nucleo/otros")
    ap = aportes(c)
    if set(ap) != set(APORTES_03) or any(v not in APORTANTES for v in ap.values()):
        raise ErrorOpex("aportes_integracion: claves de APORTES_03 y valores de APORTANTES")
    if c["alimento"] in ("facon", "propia") and c["granjas"] != "propias" and ap["alimento"] != "EMPRESA":
        raise ErrorOpex("incoherente: la empresa fabrica / manda elaborar el alimento pero el integrado lo aporta")
    for k in ("dias_cobro", "dias_caja_operativa", "ventas_anuales_usd"):
        if c[k] is not None and c[k] < 0:
            raise ErrorOpex(f"{k} ≥ 0")
    dp = c["dias_pago"] or {}
    if set(dp) - set(GRUPOS_CXP) or any(v is not None and v < 0 for v in dp.values()):
        raise ErrorOpex(f"dias_pago: {{grupo: días ≥ 0}} con grupos {GRUPOS_CXP}")
    return c


def modelo_tarifa(c, f):
    mt = c["modelo_tarifa_flete"]
    return mt.get(f) if isinstance(mt, dict) else mt


# ---------------------------------------------------------------------------------------------
# 2. DRIVERS FÍSICOS (consumidos; procedencia registrada en mapa_drivers_opex.csv)
# ---------------------------------------------------------------------------------------------
ARCH = dict(mcx.ARCH, **{"14A": "18_recursos_humanos/escenarios_rrhh.csv (modelo_rrhh.py)",
                         "04": "04_balance_masa/escenarios_balance.csv (modelo_balance_masa.py)",
                         "CAPEX16": "19_capex/boq_capex.csv (modelo_capex.py)", "OPEX": FUENTE})


def _reg(DR, driver, valor, unidad, fuente, variable, tipo, evidencia, uso="", obs="", escenario="", bajo=None, alto=None):
    if tipo not in TIPOS_DRIVER:
        raise ErrorOpex(f"tipo de driver inválido: {tipo}")
    DR["proc"][driver] = {"DRIVER": driver, "VALOR_BAJO": bajo, "VALOR": valor, "VALOR_ALTO": alto, "UNIDAD": unidad,
                          "FUENTE": ARCH.get(fuente, fuente), "VARIABLE_ORIGEN": variable, "ESCENARIO_FUENTE": escenario,
                          "TIPO": tipo, "EVIDENCIA": evidencia, "USO_EN_OPEX": uso, "OBSERVACIONES": obs}
    DR["v"][driver] = valor
    return valor


def entradas_rrhh(c):
    """Mapeo arquitectura OPEX → entradas de 14A (no recalcula 14A: llama su función)."""
    fv = mcx.flota_de(config_capex(c), "vivo") == "propia"
    cap = c["cap_camion_refrigerado_t"] if c["rrhh_cap_camion_producto_t"] == "capex" else c["rrhh_cap_camion_producto_t"]
    dist = c["dist_mercado_km"] if c["rrhh_dist_producto_km"] == "capex" else c["rrhh_dist_producto_km"]
    return dict(mr.ESCENARIO_BASE, aves_dia=c["aves_dia"], horas_netas=c["horas_netas"], turnos=c["turnos"],
                automatizacion=AUTO_RRHH[c["automatizacion"]], config=c["config_producto"], flota_propia=fv,
                limpieza=c["limpieza_modalidad"], mantenimiento=c["mantenimiento_modalidad"],
                productividad=c["productividad"], dias_semana=c["dias_semana"], planta_propia=c["faena"] == "propia",
                abastecimiento="integracion", laboratorio="propio" if c["laboratorio_propio"] else "externo",
                aves_camion=c["aves_camion_vivo"], cap_camion_producto_t=cap, dist_producto_km=dist)


def arquitectura_inventario(c):
    if c["alimento"] == "compra":
        return "A_compra"
    if c["alimento"] == "propia":
        return "C_planta_propia"
    return {"empresa": "B_facon_mp_empresa", "elaborador": "B_facon_mp_elaborador", None: None}[c["alimento_facon_mp"]]


def drivers_opex(c):
    """Cantidades anuales por arquitectura, CONSUMIDAS de los módulos fuente. Nada económico."""
    E, ds = c["aves_dia"], c["dias_semana"]
    cc = config_capex(c)
    da = mcx.dias_anio(cc)
    pub = E in ESCALAS_REF
    t = "DIRECTO" if pub else "CALCULO_MODELO_FUENTE"
    DR = {"E": E, "ds": ds, "dias_anio": da, "sem_op": da / ds, "proc": {}, "v": {}, "alertas": [], "c": c}
    if not pub:
        DR["alertas"].append(f"ESCALA_INTERMEDIA: {E:g} aves/día no publicada; drivers = CALCULO_MODELO_FUENTE")
    # ---- CAPEX (arquitectura, BOQ por bloque, flota, 09C) ------------------------------------
    filas, res, D = mcx.correr(cc)
    DR["capex_filas"], DR["capex_res"], DR["capex_D"] = filas, res, D
    _reg(DR, "dias_operativos_anio", da, "d/año", "CAPEX", "dias_anio()", "CONSUMIDO_CAPEX", "[SUPUESTO] SUP-025",
         "anualización de drivers por día operativo")
    _reg(DR, "semanas_operativas_anio", da / ds, "semanas/año", "OPEX", "días operativos ÷ días/semana", "DERIVADO_OPEX",
         "[ESTIMACIÓN]", "anualización de drivers semanales de 12B (producto, subproductos)")
    # ---- Producción primaria (03 vía 14B) ----------------------------------------------------
    pr = mup.produccion(E, ds)
    for k, un, uso in (("aves_faenadas_anio", "aves/año", "FAE-FACON, FAE-QUIM, empaque"),
                       ("aves_cargadas_anio", "aves/año", "captura, pago por ave"),
                       ("pollitos_alojados_anio", "pollitos/año", "sanidad de crianza"),
                       ("kg_vivo_cargado_anio", "kg vivo/año", "pago por kg vivo"),
                       ("mortalidad_granja_aves_anio", "aves/año", "retiro de mortalidad"),
                       ("agua_bebida_m3_anio", "m³/año", "agua de granja propia"),
                       ("ciclos_anio", "ciclos/año", "limpieza de galpones"),
                       ("m2_galpon", "m²", "limpieza y bioseguridad de galpones"),
                       ("inventario_aves_promedio_anual", "aves", "activo biológico (capital de trabajo)")):
        _reg(DR, k, pr[k], un, "03", k, t, "[ESTIMACIÓN]", uso, escenario="perfil medio, desempeño medio")
    po = mup.pollitos(E, ds)
    _reg(DR, "pollitos_a_recibir_anio", po["pollitos_a_recibir_anio"], "pollitos/año", "14B", "pollitos_a_recibir_anio", t,
         "[ESTIMACIÓN]", "POL-COMPRA / base de incubación", escenario="margen_pedido = 0 (SUP-142)")
    _reg(DR, "pollitos_a_recibir_semana_plena", po["pollitos_a_recibir_semana_plena"], "pollitos/semana", "14B",
         "pollitos_a_recibir_semana_plena", t, "[ESTIMACIÓN]", "incubación (14B)")
    al = mup.alimento(E, ds)
    t_alim = al["alimento_t_anio"]
    if "D01" in _MUT:                                            # mutación: OPEX recalcula alimento con su FCR
        t_alim = pr["aves_cargadas_anio"] * PESO_REF * 1.6 / 1000
    _reg(DR, "alimento_t_anio", t_alim, "t/año", "14B", "alimento_t_anio", t, "[ESTIMACIÓN] (03: peso × FCR)",
         "alimento comprado / elaborado / materias primas")
    _reg(DR, "alimento_t_semana_plena", al["alimento_t_semana_plena"], "t/semana", "14B", "alimento_t_semana_plena", t,
         "[ESTIMACIÓN]", "anualización de viajes de alimento")
    comp_ilus = {"maiz": mup.COMPOSICION["maiz"][2], "harina_soja": mup.COMPOSICION["harina_soja"][2],
                 "resto": mup.FRACCION_MICROS}
    comp = c["composicion_alimento"] or comp_ilus
    DR["composicion"] = comp
    DR["composicion_origen"] = "SUPUESTO_OPEX (input)" if c["composicion_alimento"] else "14B puntos ilustrativos (SUP-032)"
    for k, f in comp.items():
        _reg(DR, f"mp_{k}_t_anio", t_alim * f, "t/año", "14B" if not c["composicion_alimento"] else "OPEX",
             f"alimento_t_anio × {k} ({f:g})", "DERIVADO_OPEX" if c["composicion_alimento"] else t,
             "[SUPUESTO] composición" + ("" if c["composicion_alimento"] else " ilustrativa 14B"), "ALI-MP-*",
             obs="NO es una fórmula de dieta; mermas aparte (ALI-MERMA)")
    # ---- Incubación (14B) ----------------------------------------------------------------------
    if c["pollito"] == "incubacion":
        inc = mup.incubacion(po["pollitos_a_recibir_semana_plena"], cadencia=c["cadencia_nacimientos"],
                             margen_cap=c["margen_capacidad_incubacion"])
        f_anual = po["pollitos_a_recibir_anio"] / po["pollitos_a_recibir_semana_plena"]   # semanas equivalentes/año
        esc = f"cadencia={c['cadencia_nacimientos']}; margen={c['margen_capacidad_incubacion']}; nivel medio"
        _reg(DR, "huevos_por_pollito_vendible", inc["huevos_por_pollito_vendible"], "huevos/pollito", "14B",
             "huevos_por_pollito_vendible", t, "[SUPUESTO] fertilidad/incubabilidad (SUP-143)", escenario=esc)
        _reg(DR, "huevos_recibidos_anio", inc["huevos_por_pollito_vendible"] * po["pollitos_a_recibir_anio"], "huevos/año",
             "OPEX", "huevos_por_pollito_vendible × pollitos_a_recibir_anio", "DERIVADO_OPEX", "[ESTIMACIÓN]", "INC-OP-HUEVO",
             obs=f"14B publica {inc['huevos_recibidos_anio']:.0f} = ritmo pleno × 52,14 semanas (cota superior)")
        _reg(DR, "cargas_incubacion_anio", inc["cargas_semana"] * f_anual, "cargas/año", "OPEX",
             "cargas_semana (14B) × semanas equivalentes", "DERIVADO_OPEX", "[SUPUESTO] cadencia de ESCENARIO", "INC-OP-LIM")
        _reg(DR, "descartes_incubacion_anio", (inc["huevos_recibidos_semana"] - inc["pollitos_vendibles_semana"]) * f_anual,
             "unidades/año", "OPEX", "(huevos recibidos − pollitos vendibles) × semanas equivalentes", "DERIVADO_OPEX",
             "[ESTIMACIÓN]", "INC-OP-DES")
        _reg(DR, "stock_huevos_almacen", inc["huevos_recibidos_semana"] * mup.D_ALMACEN_BASE / 7, "huevos", "OPEX",
             f"huevos_recibidos_semana × {mup.D_ALMACEN_BASE} d / 7", "DERIVADO_OPEX", "[SUPUESTO] días de almacén (SUP-145)",
             "capital de trabajo (sin margen de capacidad)")
        _reg(DR, "huevos_en_proceso_wip", inc["huevos_en_proceso_wip"], "huevos", "14B", "huevos_en_proceso_wip", t,
             "[ESTIMACIÓN]", "capital de trabajo")
    # ---- Inventario de alimento por categoría y PROPIETARIO (14B) -------------------------------
    arq = arquitectura_inventario(c)
    DR["arq_inventario"] = arq
    if arq:
        DR["inventario_alimento"] = mup.inventario_alimento(E, arq, ds)
        if "M04" in _MUT:                                         # mutación: stock de tercero como propio
            for v in DR["inventario_alimento"].values():
                if v["stock_cadena_t"] is not None:
                    v["stock_propio_t"] = v["stock_cadena_t"]
    # ---- 09C (solo faena propia) ---------------------------------------------------------------
    perfil, _ = mcx.FRIO_A_PERFIL[c["frio"]]
    if c["faena"] == "propia":
        u = D["util"]
        t09 = "DIRECTO" if (pub and perfil == "P1" and c["horas_netas"] == 8 and c["config_producto"] == "B") \
            else "CALCULO_MODELO_FUENTE"
        esc09 = f"perfil {perfil}, {c['horas_netas']:g} h, config. {c['config_producto']}; nivel bajo/medio/alto de 09C"

        def r09(clave, var, factor, un, uso, ev="[ESTIMACIÓN]", obs=""):
            v3 = [None if u[n].get(var) is None else u[n][var] * factor for n in mcx.NIVELES]
            return _reg(DR, clave, v3[1], un, "09C", var + ("" if factor == 1 else f" × {factor:g}"), t09, ev, uso,
                        "UNIVERSO 09C = planta de FAENA; no se extiende a incubación, alimento, granjas ni rendering"
                        + (f"; {obs}" if obs else ""), esc09, v3[0], v3[2])
        r09("kwh_anio", "kwh_total_anio", 1, "kWh/año", "UT-ELE-KWH (incluye frío, aire, bombeo, efluentes aerobios)")
        r09("kwh_frio_proceso_anio", "kwh_proceso_frio_de_proceso_agua_helada_hielo_dia", da, "kWh/año",
            "INFORMATIVO: ya incluido en kwh_anio (no se duplica)", "[SUPUESTO] reparto ilustrativo")
        r09("kwh_congelacion_anio", "kwh_congelacion_dia", da, "kWh/año", "INFORMATIVO: ya incluido en kwh_anio")
        r09("kwh_almacen_frio_anio", "kwh_almacenamiento_frio_dia_calendario", 365, "kWh/año",
            "INFORMATIVO: ya incluido en kwh_anio")
        r09("kwh_efluentes_anio", "kwh_tratamiento_aerobio_dia", da, "kWh/año", "INFORMATIVO: ya incluido en kwh_anio")
        r09("kwh_bombeo_anio", "kwh_proceso_bombas_agua_y_efluentes_dia", da, "kWh/año", "INFORMATIVO: ya incluido en kwh_anio")
        r09("agua_m3_anio", "agua_captada_m3_dia", da, "m³/año", "UT-AGUA-*")
        r09("agua_limpieza_m3_anio", "agua_limpieza_m3_dia", da, "m³/año", "INFORMATIVO: ya incluida en agua_m3_anio")
        r09("efluente_m3_anio", "agua_descargada_m3_dia", da, "m³/año", "EF-QUIM, EF-CANON")
        r09("energia_termica_kwh_t_anio", "energia_combustible_kwh_termicos_dia", da, "kWh_t/año", "UT-TER-* (combustible)")
        for comb, (_, var, un) in COMBUSTIBLES.items():
            r09(f"combustible_{comb}_anio", var, da, f"{un}/año", f"UT-TER ({comb}) si se elige", "[SUPUESTO] PCI")
        for g, var in (("sangre", "segregable_sangre_recuperada_t_dia"), ("plumas", "segregable_plumas_t_dia"),
                       ("visceras", "segregable_visceras_t_dia"), ("cabezas", "segregable_cabeza_t_dia")):
            r09(f"subproducto_{g}_t_anio", var, da, "t/año", f"SUB-RET-{g.upper()}")
        bal = mb.balance(c["peso_kg"], c["config_producto"])
        kg_dec = sum(f["bio"] for f in bal["filas"] if f["componente"].startswith("decomiso"))
        _reg(DR, "decomisos_t_anio", kg_dec * pr["aves_faenadas_anio"] / 1000, "t/año", "04",
             "Σ filas 'decomiso*' de balance() × aves/año", "CALCULO_MODELO_FUENTE", "[ESTIMACIÓN] condenas medias",
             "SUB-RET-DECOMISOS")
    # ---- Producto (05) e inventario de producto (12B) -----------------------------------------
    kg_ave = ms.mc.kg_ave_config(c["config_producto"])[0]["comestible_a_empaque"][0]
    _reg(DR, "kg_producto_anio", kg_ave * pr["aves_faenadas_anio"], "kg producto/año", "05",
         "kg_ave_config()['comestible_a_empaque'] × aves/año", "CALCULO_MODELO_FUENTE", "[ESTIMACIÓN] balance v1.1",
         "EMP-* (base comercial; incluye garras y menudencias, 12B)")
    p = ml.producto(E, ds, perfil=perfil, dias_despacho=6, cap_refrigerado=c["cap_camion_refrigerado_t"],
                    cap_congelado=c["cap_camion_congelado_t"], dist_km=c["dist_mercado_km"], despachos_congelado=2)
    DR["producto_12b"] = p
    so = DR["sem_op"]
    esc12 = (f"perfil {perfil}; 6 despachos refrigerado y 2 congelado/sem; {c['cap_camion_refrigerado_t']:g} t; "
             f"{c['dist_mercado_km']:g} km (ESCENARIO, SUP-16-20)")
    t12 = "DIRECTO" if (pub and perfil == "P1" and c["dist_mercado_km"] == 300 and c["cap_camion_refrigerado_t"] == 12) \
        else "CALCULO_MODELO_FUENTE"
    for ch in ("refrigerado", "congelado"):
        _reg(DR, f"{ch}_t_anio", p[f"{ch}_t_semana"] * so, "t/año", "12B", f"{ch}_t_semana × semanas operativas", t12,
             "[ESTIMACIÓN]", f"flujo {ch}", escenario=esc12)
        vs = p.get(f"{ch}_viajes_semana")
        _reg(DR, f"{ch}_viajes_anio", None if vs is None else vs * so, "viajes/año", "12B", f"{ch}_viajes_semana × semanas",
             t12 if vs is not None else "PENDIENTE", "[ESTIMACIÓN] capacidad de ESCENARIO", f"LOG-{ch[:3].upper()}-*", escenario=esc12)
        kd = p.get(f"{ch}_km_dia_despacho")
        _reg(DR, f"{ch}_km_anio", None if kd is None else kd * p[f"{ch}_despachos_semana"] * so, "km/año", "12B",
             f"{ch}_km_dia_despacho × despachos/semana × semanas", t12 if kd is not None else "PENDIENTE",
             "[ESTIMACIÓN] troncal; reparto capilar PENDIENTE (DEC-053)", f"LOG-{ch[:3].upper()}-*", escenario=esc12)
        inv = ml.inventario(p[f"{ch}_t_dia_op"], ds, dias_despacho=6 if ch == "refrigerado" else 2)
        _reg(DR, f"stock_{ch}_medio_t", inv["stock_ciclo_medio_t"] + inv["stock_seguridad_t"], "t", "12B",
             f"inventario(t_dia_op, despachos={6 if ch == 'refrigerado' else 2}): stock_ciclo_medio + seguridad (0)",
             "CALCULO_MODELO_FUENTE", "[ESTIMACIÓN]; stock comercial adicional PENDIENTE", "capital de trabajo")
    # ---- Logística: aves vivas, alimento, grano, pollitos, subproductos (12B / 14B) -----------
    v = ml.aves_vivas(E, ds, radio_km=c["radio_granjas_km"], aves_camion=c["aves_camion_vivo"])
    tv = "DIRECTO" if (pub and c["radio_granjas_km"] in ml.RADIOS_KM and c["aves_camion_vivo"] in ml.AVES_CAMION) \
        else "CALCULO_MODELO_FUENTE"
    escv = f"radio {c['radio_granjas_km']} km; {c['aves_camion_vivo']} aves/camión (ESCENARIO)"
    _reg(DR, "vivo_viajes_anio", v["viajes_dia"] * da, "viajes/año", "12B", "viajes_dia × días", tv, "[ESTIMACIÓN]",
         "LOG-VIV-*", escenario=escv)
    _reg(DR, "vivo_km_anio", v["km_total_dia"] * da, "km/año", "12B", "km_total_dia × días", tv, "[ESTIMACIÓN]",
         "LOG-VIV-*", escenario=escv)
    _reg(DR, "vivo_t_anio", v["t_vivo_cargado_dia"] * da, "t/año", "12B", "t_vivo_cargado_dia × días", tv, "[ESTIMACIÓN]",
         "LOG-VIV-TER-UNI", escenario=escv)
    i = ml.insumos(E, ds, cap_granelero=c["cap_granelero_t"], dist_fabrica=c["dist_fabrica_granja_km"])
    fa = t_alim / i["alimento_t_semana_plena"]                       # semanas equivalentes de alimento por año
    ti = "DIRECTO" if pub and c["cap_granelero_t"] == ml.CAP_GRANELERO_T and c["dist_fabrica_granja_km"] in ml.DIST_FABRICA_KM \
        else "CALCULO_MODELO_FUENTE"
    esci = f"granelero {c['cap_granelero_t']:g} t; {c['dist_fabrica_granja_km']} km fábrica–granja (ESCENARIO)"
    _reg(DR, "alimento_viajes_anio", i["alimento_viajes_semana"] * fa, "viajes/año", "12B",
         "alimento_viajes_semana × (t_año ÷ t_semana_plena)", ti, "[ESTIMACIÓN]", "LOG-ALI-*", escenario=esci)
    _reg(DR, "alimento_km_anio", i["alimento_km_semana"] * fa, "km/año", "12B",
         "alimento_km_semana × (t_año ÷ t_semana_plena)", ti, "[ESTIMACIÓN]", "LOG-ALI-*", escenario=esci)
    if c["alimento"] == "propia" or arq == "B_facon_mp_empresa":
        g = sum(DR["v"].get(f"mp_{k}_t_anio", 0.0) for k in ("maiz", "harina_soja"))
        _reg(DR, "grano_t_anio", g, "t/año", "OPEX", "mp maíz + harina de soja (t/año)", "DERIVADO_OPEX", "[ESTIMACIÓN]",
             "LOG-GRA-TER-UNI")
        _reg(DR, "grano_viajes_anio", None, "viajes/año", "14B", "viajes_grano_semana (cap_grano = None)", "PENDIENTE",
             "PENDIENTE (capacidad y distancia del acopio, DPV-157)", "LOG-GRA-*")
    _reg(DR, "pollitos_viajes_anio", None, "viajes/año", "12B", "pollitos_viajes_semana (cap_pollitos = None)", "PENDIENTE",
         "PENDIENTE (DPV-047, DPV-084)", "LOG-POL-*")
    if c["faena"] == "propia":
        vs = ks = ts = 0.0
        for gr in ("G1-plumas", "G2-sangre", "G3-visceras", "G4-decomisos"):
            s_ = ml.subproductos(E, ds, c["config_producto"], "E1", cap=c["cap_vehiculo_subproductos_t"], corriente=gr,
                                 dist_receptor_km=c["dist_receptor_subproductos_km"])
            vs += s_["viajes_semana_criterio_masa"]
            ks += s_["km_semana_criterio_masa"]
            ts += s_["t_semana"]
        _reg(DR, "subproductos_viajes_anio", vs * so, "viajes/año", "12B", "Σ viajes_semana_criterio_masa × semanas",
             "CALCULO_MODELO_FUENTE", "COTA INFERIOR (volumétrico PENDIENTE, DPV-135)", "LOG-SUB-*")
        _reg(DR, "subproductos_km_anio", ks * so, "km/año", "12B", "Σ km_semana_criterio_masa × semanas",
             "CALCULO_MODELO_FUENTE", "COTA INFERIOR", "LOG-SUB-*")
        _reg(DR, "subproductos_t_anio", ts * so, "t/año", "12B", "Σ t_semana × semanas", "CALCULO_MODELO_FUENTE",
             "[ESTIMACIÓN]", "LOG-SUB-TER-UNI")
    # ---- Flota propia (CAPEX, que consume 12B) ------------------------------------------------
    for f, (_, fc, _) in FLUJOS.items():
        fl = D["flota"].get(fc) if f not in ("HUE", "GRA") else None
        _reg(DR, f"vehiculos_{f}", None if fl is None else fl["unidades"], "vehículos", "CAPEX16",
             f"flota[{fc}].unidades" if f not in ("HUE", "GRA") else "—",
             "CONSUMIDO_CAPEX" if fl and fl["unidades"] is not None else "PENDIENTE",
             "[ESTIMACIÓN] con reserva SUP-16-02" if fl and fl["unidades"] is not None else "PENDIENTE",
             f"LOG-{f}-PAT, SEG-FLOTA-{f}")
    # ---- RRHH (14A) ---------------------------------------------------------------------------
    ent = entradas_rrhh(c)
    R = mr.calcular(ent)
    DR["rrhh"], DR["rrhh_entradas"] = R, ent
    _reg(DR, "fte_industrial_14a", R["fte_total"], "FTE", "14A", "fte_total", "CALCULO_MODELO_FUENTE", "[SUPUESTO] productividad",
         "RRHH INDUSTRIAL + estructura + coordinación primaria (14A). NO es el FTE total de una empresa verticalmente "
         "integrada: granjas propias, incubación, planta de alimento, reproductoras y rendering no están dimensionados",
         obs="headcount de nómina PENDIENTE (factor de cobertura no validado); incluye horas de terceros que luego "
             "pueden quedar INCLUIDAS en tarifas (faenador, choferes)",
         escenario=f"turnos={ent['turnos']}; autom={ent['automatizacion']}; limpieza={ent['limpieza']}; "
                   f"mant={ent['mantenimiento']}; lab={ent['laboratorio']}")
    _reg(DR, "fte_directos_14a", R["fte_interno"]["directo"] + R["fte_tercerizado"]["directo"], "FTE", "14A",
         "fte_interno + fte_tercerizado (directo)", "CALCULO_MODELO_FUENTE", "[SUPUESTO]", "FAE-CUCH")
    _reg(DR, "horas_brecha_jornada_anio", R["horas_persona_brecha_jornada_dia"] * da, "h-persona/año", "14A",
         "horas_persona_brecha_jornada_dia × días", "CALCULO_MODELO_FUENTE", "[ESTIMACIÓN]",
         "INFORMATIVO: no son horas extra automáticas (DPV-146)")
    _reg(DR, "headcount_nomina", None, "personas", "14A", "headcount_nomina", "PENDIENTE", "PENDIENTE (factor de cobertura)",
         "NO se usa: costeo provisional por FTE")
    # ---- Granjas propias (fracción) -----------------------------------------------------------
    _reg(DR, "fraccion_granjas_propias", c["fraccion_granjas_propias"], "fracción", "CAPEX16", "fraccion_granjas_propias",
         "CONSUMIDO_CAPEX", "ESCENARIO (SUP-16-09)", "reparto propia / integrada")
    for k in ("kwh_granja", "gas_granja", "cama_t", "personal_granja", "personal_incubadora", "personal_planta_alimento",
              "personal_reproductoras", "personal_rendering", "kwh_incubadora", "agua_incubadora", "kwh_planta_alimento",
              "vapor_planta_alimento", "agua_planta_alimento", "kwh_rendering", "lodos_t", "potencia_contratada_kw"):
        _reg(DR, k, None, "—", "OPEX", "—", "PENDIENTE", "PENDIENTE: el módulo fuente no lo dimensiona",
             "concepto PENDIENTE_CANTIDAD (no se inventa)")
    DR["alertas"] += [a for a in D["alertas"] if a.startswith(("DRIVER_INCONSISTENTE", "ESCALA"))]
    if mcx.flota_de(cc, "vivo") != mcx.flota_de(cc, "refrigerado"):
        DR["alertas"].append("RRHH_FLOTA_MIXTA: 14A usa un único indicador de flota propia (se toma el de aves vivas)")
    return DR


# ---------------------------------------------------------------------------------------------
# 3. BASE DE COSTOS
# ---------------------------------------------------------------------------------------------
def _num(x):
    if x is None:
        return None
    s = str(x).strip()
    if s == "":
        return None
    return float(s)


def leer_base(ruta=ARCHIVO_COSTOS):
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    validar_base(filas)
    return {r["ID_COSTO"]: r for r in filas}


def precio_usd(r):
    """USD por unidad, o None. Los % y parámetros se devuelven tal cual (no tienen moneda)."""
    if r is None:
        return None
    p = _num(r["PRECIO_UNITARIO"])
    if p is None:
        return None
    if r["UNIDAD"] in UNIDADES_PCT or r["MONEDA_ORIGINAL"] in ("", "NA"):
        return p
    if r["MONEDA_ORIGINAL"] == "USD":
        return p
    tc = _num(r["TC_MONEDA_POR_USD"])
    return None if not tc else p / tc


def validar_base(filas):
    ids = [r["ID_COSTO"] for r in filas]
    if len(ids) != len(set(ids)):
        raise ErrorOpex("ID_COSTO duplicado en la base")
    for r in filas:
        i = r["ID_COSTO"]
        if r["NATURALEZA"] not in NATURALEZAS or r["CENTRO_COSTO"] not in CENTROS or r["TIPO"] not in TIPOS:
            raise ErrorOpex(f"{i}: naturaleza / centro / tipo inválidos")
        if r["ESTADO"] not in ESTADOS_BASE or r["NIVEL_EVIDENCIA"] not in NIVELES_EVIDENCIA:
            raise ErrorOpex(f"{i}: estado o nivel de evidencia inválido")
        p = _num(r["PRECIO_UNITARIO"])
        if p is not None and p < 0:
            raise ErrorOpex(f"{i}: precio negativo (un ingreso no se netea en OPEX)")
        if p is None and r["NIVEL_EVIDENCIA"] != "PENDIENTE":
            raise ErrorOpex(f"{i}: sin precio debe ser PENDIENTE (vacío ≠ 0)")
        if p is not None:
            if r["NIVEL_EVIDENCIA"] == "PENDIENTE" or not r["FUENTE"]:
                raise ErrorOpex(f"{i}: con precio exige nivel E1–E5 y fuente")
            if r["NIVEL_EVIDENCIA"] == "E1" and r["TIPO_PRECIO"] != "cotizacion":
                raise ErrorOpex(f"{i}: E1 exige TIPO_PRECIO = cotizacion")
            if r["NIVEL_EVIDENCIA"] in ("E1", "E2", "E3") and r["LECTURA_PRIMARIA"] != "Sí":
                raise ErrorOpex(f"{i}: E1–E3 exigen lectura primaria (regla 16)")
            mon = r["MONEDA_ORIGINAL"]
            if r["UNIDAD"] not in UNIDADES_PCT and mon not in ("USD", "NA", ""):
                if r["ESTADO"] == "CON_PRECIO" and not (_num(r["TC_MONEDA_POR_USD"]) and r["TIPO_TC"] and r["FECHA_TC"]):
                    raise ErrorOpex(f"{i}: precio en {mon} sin tipo de cambio, tipo y fecha")
            eq = _num(r["PRECIO_USD_EQUIVALENTE"])
            pu = precio_usd(r)
            if eq is not None and pu is not None and abs(eq - pu) > 0.005 * max(1.0, abs(pu)):
                raise ErrorOpex(f"{i}: PRECIO_USD_EQUIVALENTE {eq} no coincide con precio ÷ TC = {pu:.4f}")
            if r["UNIDAD"] == "%" and not 0 <= p <= 100:
                raise ErrorOpex(f"{i}: porcentaje fuera de [0, 100]")
        pv = _num(r["PCT_VARIABLE"])
        if pv is not None and not 0 <= pv <= 100:
            raise ErrorOpex(f"{i}: PCT_VARIABLE fuera de [0, 100]")
        if r["NATURALEZA"] == "semivariable" and pv is not None and not r["ORIGEN_PCT_VARIABLE"].startswith(("SUP", "[SUP")):
            raise ErrorOpex(f"{i}: % variable de un semivariable debe declararse como SUPUESTO")
        for k in ("PRECIO_BAJO", "PRECIO_ALTO"):
            if _num(r[k]) is not None and not r["ORIGEN_RANGO"]:
                raise ErrorOpex(f"{i}: un rango exige ORIGEN_RANGO (sin ±% automático)")


ARCHIVO_REGLAS = os.path.join(AQUI, "reglas_laborales_opex.csv")
COMPONENTES_LAB = ("SAL", "ADI", "VAC", "CAR", "ART", "BEN", "EPP", "CAP", "OTR")   # HEX: solo si se organizan horas extra


def leer_reglas(ruta=ARCHIVO_REGLAS):
    """Reglas laborales (SAC, vacaciones, horas extra…). NO son precios: no tienen nivel E1–E5."""
    with open(ruta, encoding="utf-8") as f:
        reglas = {r["REGLA"]: r for r in csv.DictReader(f)}
    return validar_reglas(reglas)


def validar_reglas(reglas):
    for r in reglas.values():
        if r["TIPO"].startswith(("precio", "cotizacion")) or r["EVIDENCIA"] in EVIDENCIAS:
            raise ErrorOpex(f"regla {r['REGLA']}: una regla laboral no es un precio ni lleva nivel E1–E5")
    return reglas


def costo_empresa_fte(cat, base, reglas=None):
    """Costo empresa anual por FTE de una categoría laboral desde sus componentes. Cualquier faltante → None.
    remuneración mensual = salario × (1 + adicionales % + vacaciones %); anual = mensual × (12 + SAC);
    costo = anual × (1 + cargas % + ART %) + beneficios × 12 + EPP + capacitación + otros. Horas extra: NO automáticas."""
    reglas = reglas if reglas is not None else leer_reglas()
    comp = {k: base.get(f"LAB-{cat}-{k}") for k in COMPONENTES_LAB}
    val = {k: precio_usd(r) for k, r in comp.items()}
    sac = _num(reglas.get("SAC", {}).get("VALOR"))
    val["SAC"] = sac
    falt = [k for k, x in val.items() if x is None]
    niveles = [r["NIVEL_EVIDENCIA"] for r in comp.values() if r]
    peor = max((n for n in niveles if n in EVIDENCIAS), default="PENDIENTE")
    if falt:
        return None, "PENDIENTE", falt, val
    rem = val["SAL"] * (1 + val["ADI"] / 100 + val["VAC"] / 100) * (12 + sac)
    return (rem * (1 + val["CAR"] / 100 + val["ART"] / 100) + val["BEN"] * 12 + val["EPP"] + val["CAP"] + val["OTR"],
            peor, [], val)


# ---------------------------------------------------------------------------------------------
# 4. REGISTRO DE COSTOS OPERATIVOS (una fila por concepto y arquitectura)
# ---------------------------------------------------------------------------------------------
CAMPOS_REG = ["ESCENARIO", "CONFIGURACION", "ESCALA_AVES_DIA", "MODULO", "SUBMODULO", "CONCEPTO", "COSTO_ID", "FLUJO",
              "CENTRO_COSTO", "NATURALEZA", "TIPO", "APORTANTE", "FASE", "DRIVER", "CANTIDAD", "UNIDAD",
              "ESTADO_DIMENSION", "INCLUIDO_EN", "MOTIVO", "COSTEA", "PRECIO_USD", "COSTO_CALCULADO_USD_ANIO",
              "COSTO_CONCEPTO_USD_AVE", "EVIDENCIA", "PCT_VARIABLE", "PCT_FIJO", "FIJO_VARIABLE", "ESTADO",
              "GRUPO_PROVEEDOR", "MODULO_ARQ", "BLOQUE", "AMBITO_GRANJA", "UNIVERSO_RRHH", "UNIVERSO_UTILITIES",
              "PRECIO_ORIGINAL_OBSERVADO", "MONEDA_ORIGINAL", "FECHA_PRECIO", "CONDICION_ENTREGA", "IVA_PRECIO",
              "TC_USADO", "FECHA_TC", "ORIGEN_PRECIO_USD", "ALERTAS"]


class Registro:
    def __init__(self, c, DR, base):
        self.c, self.DR, self.base, self.filas = c, DR, base, []

    def add(self, modulo, costo_id, cantidad, driver="", unidad=None, concepto=None, submodulo=None, flujo="",
            aportante="EMPRESA", fase="OPERACION", estado_dim=None, incluido_en="", motivo="", centro=None,
            naturaleza=None, tipo=None, ambito="", universo_rrhh=""):
        b = self.base.get(costo_id) if costo_id else None
        if costo_id and b is None and not costo_id.startswith("LAB-"):
            raise ErrorOpex(f"COSTO_ID {costo_id} inexistente en la base")
        if estado_dim is None:
            estado_dim = "DIMENSIONADO" if cantidad is not None else "PENDIENTE"
        if cantidad is not None and cantidad < 0:
            raise ErrorOpex(f"cantidad negativa en {costo_id}")
        f = {k: "" for k in CAMPOS_REG}
        f.update(MODULO=modulo, SUBMODULO=submodulo or (b["SUBMODULO"] if b else ""),
                 CONCEPTO=concepto or (b["CONCEPTO"] if b else ""), COSTO_ID=costo_id or "", FLUJO=flujo,
                 CENTRO_COSTO=centro or (b["CENTRO_COSTO"] if b else ""), NATURALEZA=naturaleza or (b["NATURALEZA"] if b else ""),
                 TIPO=tipo or (b["TIPO"] if b else ""), APORTANTE=aportante, FASE=fase, DRIVER=driver,
                 CANTIDAD=cantidad, UNIDAD=unidad or (b["UNIDAD"] if b else ""), ESTADO_DIMENSION=estado_dim,
                 INCLUIDO_EN=incluido_en, MOTIVO=motivo, GRUPO_PROVEEDOR=b["GRUPO_PROVEEDOR"] if b else "",
                 AMBITO_GRANJA=ambito, UNIVERSO_RRHH=universo_rrhh,
                 COSTEA=(aportante in ("EMPRESA", "PENDIENTE") and fase in ("OPERACION", "OPCIONAL_MERCADO")
                         and estado_dim in ("DIMENSIONADO", "PENDIENTE")))
        if b and f["UNIDAD"] != b["UNIDAD"]:
            raise ErrorOpex(f"{costo_id}: unidad del driver ({f['UNIDAD']}) ≠ unidad del precio ({b['UNIDAD']})")
        self.filas.append(f)
        return f

    def split(self, modulo, costo_id, aporte, q_total, driver, **kw):
        """Reparte una cantidad entre granjas PROPIAS (costo de la empresa) e INTEGRADAS (según el aportante del
        concepto). Con granjas mixtas siempre hay dos filas separadas (ámbito PROPIA / INTEGRADA)."""
        fp = self.c["fraccion_granjas_propias"]
        ap = aportes(self.c)[aporte]
        mot = kw.pop("motivo", "")
        out = []
        if fp > TOL:
            q = None if q_total is None else q_total * fp
            out.append(self.add(modulo, costo_id, q, driver + ("" if fp >= 1 - TOL else " × fracción propia"),
                                motivo=mot, ambito="PROPIA", **kw))
        if fp < 1 - TOL:
            q = None if q_total is None else q_total * (1 - fp)
            d = driver + ("" if fp <= TOL else " × fracción integrada")
            if ap == "EMPRESA":
                out.append(self.add(modulo, costo_id, q, d, motivo=mot, ambito="INTEGRADA", **kw))
            elif ap == "PRODUCTOR_INTEGRADO":
                out.append(self.add(modulo, costo_id, q, d, aportante=ap, estado_dim="INFORMATIVO", ambito="INTEGRADA",
                                    motivo="COSTO DEL PRODUCTOR (aporte del integrado, SUP-17-04): no es costo de la empresa"
                                    + (f"; {mot}" if mot else ""), **kw))
            else:
                out.append(self.add(modulo, costo_id, q, d, aportante=ap, ambito="INTEGRADA",
                                    motivo="APORTANTE_PENDIENTE: según contrato (03)" + (f"; {mot}" if mot else ""), **kw))
        return out


def generar_registro(c, DR, base):
    R = Registro(c, DR, base)
    v = DR["v"]
    fp = c["fraccion_granjas_propias"]
    propia = c["faena"] == "propia"
    rrhh = DR["rrhh"]
    # ---------------- ALIMENTO ----------------
    t_al = v["alimento_t_anio"]
    if c["alimento"] == "compra":
        R.split("ALIMENTO", "ALI-A-PT", "alimento", t_al, "alimento_t_anio")
        R.split("ALIMENTO", "ALI-A-DES", "alimento", t_al, "alimento_t_anio")
        if "M03" in _MUT:                                         # mutación: compra con costo interno de fábrica
            R.add("ALIMENTO", "ALI-C-ENE", None, "kwh_planta_alimento")
    elif c["alimento"] == "facon" and c["alimento_facon_mp"] is None:
        R.add("ALIMENTO", "", t_al, "alimento_t_anio", unidad="t", submodulo="facon",
              concepto="Alimento a façon: materias primas (B1) o precio integral (B2) — variante NO definida",
              motivo="VARIANTE_FACON_NO_DEFINIDA (DEC-17-02): sin variante no hay precio aplicable; la cantidad sí existe",
              centro="alimento", naturaleza="variable", tipo="comprado")
        R.add("ALIMENTO", "ALI-B-SRV", None, "alimento_t_anio", motivo="VARIANTE_FACON_NO_DEFINIDA (DEC-17-02): "
              "MP de la empresa (MP + servicio) o del elaborador (precio integral)")
    elif c["alimento"] == "facon" and c["alimento_facon_mp"] == "elaborador":
        R.add("ALIMENTO", "ALI-B-PTE", t_al, "alimento_t_anio")
    if c["alimento"] == "propia" or c["alimento_facon_mp"] == "empresa":
        comp = DR["composicion"]
        ids = {"maiz": "ALI-MP-MAIZ", "harina_soja": "ALI-MP-SOJA", "aceite": "ALI-MP-ACEITE", "nucleo": "ALI-MP-NUCLEO",
               "otros": "ALI-MP-OTROS", "resto": "ALI-MP-RESTO"}
        for k, i in ids.items():
            if k in comp:
                R.add("ALIMENTO", i, v[f"mp_{k}_t_anio"], f"mp_{k}_t_anio")
            elif k in ("aceite", "nucleo", "otros") and "resto" in comp:
                R.add("ALIMENTO", i, None, "—", estado_dim="INCLUIDO", incluido_en="ALI-MP-RESTO",
                      motivo="desagregación PENDIENTE: 14B solo da rangos")
        # Precio Rosario ≠ costo puesto en planta: diferencial aparte (el flete va en LOG-GRA-*)
        for k, i in (("maiz", "ALI-MP-DIF-MAIZ"), ("harina_soja", "ALI-MP-DIF-SOJA")):
            if k in comp:
                R.add("ALIMENTO", i, v[f"mp_{k}_t_anio"], f"mp_{k}_t_anio",
                      motivo="precio de referencia (pizarra) ≠ puesto en planta; diferencial PENDIENTE (DPV-17-02)")
        R.add("ALIMENTO", "ALI-MERMA", None, "% merma × t MP", motivo="% de merma no dimensionado (DPV-158)")
        if c["alimento"] == "facon":
            R.add("ALIMENTO", "ALI-B-SRV", t_al, "alimento_t_anio")
            st = sum(x["stock_propio_t"] or 0 for k, x in DR["inventario_alimento"].items()
                     if k in ("maiz", "harina_soja", "micros_aceite_otros"))
            R.add("ALIMENTO", "ALI-B-ALM", st * 12, "stock propio de MP (14B) × 12 meses")
        else:
            R.add("ALIMENTO", "ALI-C-ENE", None, "kwh_planta_alimento", motivo="kWh/t de molienda, mezcla y pellet no "
                  "dimensionado (DPV-158); NO se usa el kWh de la planta de faena (09C)")
            R.add("ALIMENTO", "ALI-C-TER", None, "vapor_planta_alimento", motivo="vapor de peletizado no dimensionado (DPV-158)")
            R.add("ALIMENTO", "ALI-C-AGUA", None, "agua_planta_alimento", motivo="no dimensionado; NO se usa el agua de 09C")
            R.add("ALIMENTO", "ALI-C-MOV", None, "—", motivo="movimientos internos no dimensionados")
            R.add("ALIMENTO", "ALI-C-ANA", None, "—", motivo="plan de muestreo PENDIENTE")
            R.add("ALIMENTO", "ALI-C-ALM", None, "—", motivo="no dimensionado")
    # ---------------- POLLITOS / INCUBACIÓN / REPRODUCTORAS ----------------
    if c["pollito"] == "compra":
        R.split("POLLITOS", "POL-COMPRA", "pollito", v["pollitos_a_recibir_anio"], "pollitos_a_recibir_anio")
    else:
        R.add("INCUBACION", "INC-OP-HUEVO", v["huevos_recibidos_anio"], "huevos_recibidos_anio")
        R.add("INCUBACION", "INC-OP-VAC", v["pollitos_a_recibir_anio"], "pollitos_a_recibir_anio")
        R.add("INCUBACION", "INC-OP-INS", v["pollitos_a_recibir_anio"], "pollitos_a_recibir_anio")
        R.add("INCUBACION", "INC-OP-LIM", v["cargas_incubacion_anio"], "cargas_incubacion_anio")
        R.add("INCUBACION", "INC-OP-DES", v["descartes_incubacion_anio"], "descartes_incubacion_anio")
        kwh_inc = DR["v"]["kwh_anio"] if "M12" in _MUT else None   # mutación: reutiliza el kWh de faena (09C)
        R.add("INCUBACION", "INC-OP-ENE", kwh_inc, "kwh_anio" if "M12" in _MUT else "kwh_incubadora",
              motivo="energía y HVAC de la incubadora no dimensionados; NO se usa el kWh de la planta de faena (09C)")
        R.add("INCUBACION", "INC-OP-AGUA", None, "agua_incubadora", motivo="no dimensionado; NO se usa el agua de 09C")
        R.add("INCUBACION", "INC-OP-CAL", None, "—", motivo="plan de control y bioseguridad PENDIENTE")
    if c["reproductoras"]:
        for i in ("REP-AVE", "REP-ALI", "REP-SAN", "REP-ENE", "REP-AGUA", "REP-MAN", "REP-RES", "REP-LOG", "REP-OTR"):
            R.add("REPRODUCTORAS", i, None, "—", fase="FUTURO", motivo="arquitectura futura sin evidencia (DPV-045)")
    # ---------------- PRODUCCIÓN PRIMARIA ----------------
    R.split("PRODUCCION_PRIMARIA", "PP-SAN", "sanidad", v["pollitos_alojados_anio"], "pollitos_alojados_anio")
    R.split("PRODUCCION_PRIMARIA", "PP-CAMA", "cama", None, "cama_t", motivo="kg de cama/m² PENDIENTE")
    R.split("PRODUCCION_PRIMARIA", "PP-GAS", "gas_calefaccion", None, "gas_granja", motivo="DPV-052")
    R.split("PRODUCCION_PRIMARIA", "PP-CAPT", "captura", v["aves_cargadas_anio"], "aves_cargadas_anio")
    R.split("PRODUCCION_PRIMARIA", "PP-MORT", "mortalidad_retiro", v["mortalidad_granja_aves_anio"], "mortalidad_granja_aves_anio")
    R.split("PRODUCCION_PRIMARIA", "PP-LIMP", "limpieza_galpon", v["m2_galpon"] * v["ciclos_anio"], "m2_galpon × ciclos_anio")
    R.split("PRODUCCION_PRIMARIA", "PP-BIO", "bioseguridad", v["m2_galpon"], "m2_galpon")
    R.split("PRODUCCION_PRIMARIA", "PP-ENE", "electricidad_granja", None, "kwh_granja", motivo="DPV-052")
    R.split("PRODUCCION_PRIMARIA", "PP-AGUA", "agua_granja", v["agua_bebida_m3_anio"], "agua_bebida_m3_anio")
    R.split("PRODUCCION_PRIMARIA", "PP-VET", "sanidad", None, "—", motivo="plan sanitario y de análisis PENDIENTE")
    if fp < 1 - TOL:
        R.add("PRODUCCION_PRIMARIA", "PP-ATE", None, "—", motivo="necesidad PENDIENTE: 14A ya dimensiona veterinario y "
              "técnicos de campo (no se duplica)", ambito="INTEGRADA")
        base_pago = c["base_pago_integrado"]
        if base_pago is None:
            R.add("PRODUCCION_PRIMARIA", "PP-PAGO-AVE", None, "—", concepto="Pago al productor integrado (base del contrato NO definida)",
                  motivo="CONTRATO_NO_DEFINIDO (DEC-17-04)", ambito="INTEGRADA")
        elif base_pago == "ave":
            R.add("PRODUCCION_PRIMARIA", "PP-PAGO-AVE", v["aves_cargadas_anio"] * (1 - fp), "aves_cargadas_anio × fracción integrada",
                  ambito="INTEGRADA")
        else:
            R.add("PRODUCCION_PRIMARIA", "PP-PAGO-KG", v["kg_vivo_cargado_anio"] * (1 - fp), "kg_vivo_cargado_anio × fracción integrada",
                  ambito="INTEGRADA")
    if fp > TOL:
        R.add("PRODUCCION_PRIMARIA", "PP-OTR", None, "—", motivo="otros insumos de granja propia: no definidos", ambito="PROPIA")
    # ---------------- FAENA ----------------
    if propia:
        R.add("FAENA", "FAE-QUIM", v["aves_faenadas_anio"], "aves_faenadas_anio")
        R.add("FAENA", "FAE-ELEM", 1.0, "1 año")
        R.add("FAENA", "FAE-CUCH", v["fte_directos_14a"], "fte_directos_14a")
        R.add("FAENA", "FAE-SERV", 12.0, "12 meses")
        R.add("FAENA", "", v["agua_limpieza_m3_anio"], "agua_limpieza_m3_anio", unidad="m³", concepto="Agua y energía de limpieza y sanitización",
              submodulo="limpieza", estado_dim="INCLUIDO", incluido_en="UT-AGUA / UT-ELE-KWH / UT-TER",
              motivo="09C ya incluye agua de limpieza y calor de limpieza: no se cargan de nuevo",
              centro="faena", naturaleza="variable", tipo="comprado")
        if "M08" in _MUT:                                         # mutación: limpieza vuelve a cobrar el agua
            R.add("FAENA", "UT-AGUA-TRAT", v["agua_limpieza_m3_anio"], "agua_limpieza_m3_anio", submodulo="limpieza")
    else:
        R.add("FAENA", "FAE-FACON", v["aves_faenadas_anio"], "aves_faenadas_anio", motivo="tarifa NO asumida (DPV-006)")
        R.add("FAENA", "FAE-FACON-FRIO", None, "—", motivo="alcance del contrato PENDIENTE")
        R.add("FAENA", "FAE-FACON-SUB", None, "—", motivo="alcance del contrato PENDIENTE (DPV-17-07)")
    # ---------------- EMPAQUE ----------------
    if propia:
        ap_emp = "EMPRESA"
    else:
        ap_emp = {None: "PENDIENTE", True: "EMPRESA", False: "TERCERO"}[c["facon_aporta_empaque"]]
    for i in ("EMP-BOLSA", "EMP-BANDEJA", "EMP-FILM", "EMP-CAJA", "EMP-ETIQ", "EMP-SEP", "EMP-PALLET", "EMP-FLEJE",
              "EMP-OTROS"):
        R.add("EMPAQUE", i, v["kg_producto_anio"], "kg_producto_anio", aportante=ap_emp,
              estado_dim="INFORMATIVO" if ap_emp == "TERCERO" else None,
              motivo={"PENDIENTE": "quién aporta el empaque en el façon: PENDIENTE",
                      "TERCERO": "incluido en la tarifa de façon"}.get(ap_emp, ""))
    # ---------------- UTILITIES Y EFLUENTES (solo planta propia) ----------------
    if propia:
        kwh = v["kwh_anio"]
        R.add("UTILITIES", "UT-ELE-KWH", kwh, "kwh_anio")
        R.add("UTILITIES", "UT-ELE-POT", None, "potencia_contratada_kw", motivo="potencia pico no dimensionada (DPV-095); "
              "no se multiplica kW por tarifa de kWh")
        R.add("UTILITIES", "UT-ELE-FIJO", 12.0, "12 meses")
        for k, con in (("kwh_frio_proceso_anio", "Energía de frío de proceso (agua helada, hielo)"),
                       ("kwh_congelacion_anio", "Energía de congelación"), ("kwh_almacen_frio_anio", "Energía de cámaras"),
                       ("kwh_efluentes_anio", "Energía de tratamiento aerobio de efluentes"),
                       ("kwh_bombeo_anio", "Energía de bombeo de agua y efluentes")):
            R.add("UTILITIES", "", v[k], k, unidad="kWh", concepto=con, submodulo="frio" if "frio" in k or "cong" in k else "electricidad",
                  estado_dim="INCLUIDO", incluido_en="UT-ELE-KWH", motivo="ya incluido en kWh totales de 09C (no se duplica)",
                  centro="frio" if "frio" in k or "cong" in k else "servicios_generales", naturaleza="variable", tipo="comprado")
        if "M02" in _MUT:                                         # mutación: segundo costo energético de frío
            R.add("UTILITIES", "UT-ELE-KWH", v["kwh_frio_proceso_anio"], "kwh_frio_proceso_anio")
        comb = c["combustible_termico"]
        if comb:
            i, _, _ = COMBUSTIBLES[comb]
            R.add("UTILITIES", i, v[f"combustible_{comb}_anio"], f"combustible_{comb}_anio")
        else:
            R.add("UTILITIES", "UT-TER-NS", v["energia_termica_kwh_t_anio"], "energia_termica_kwh_t_anio",
                  motivo="COMBUSTIBLE_NO_SELECCIONADO (DEC-045)")
        fa = c["fuente_agua"]
        if fa == "red":
            R.add("UTILITIES", "UT-AGUA-RED", v["agua_m3_anio"], "agua_m3_anio")
        elif fa == "pozo":
            R.add("UTILITIES", "UT-AGUA-CANON", v["agua_m3_anio"], "agua_m3_anio")
        else:
            R.add("UTILITIES", "UT-AGUA-NS", v["agua_m3_anio"], "agua_m3_anio", motivo="FUENTE_AGUA_NO_SELECCIONADA (DEC-17-03)")
        R.add("UTILITIES", "UT-AGUA-TRAT", v["agua_m3_anio"], "agua_m3_anio")
        R.add("EFLUENTES", "EF-QUIM", v["efluente_m3_anio"], "efluente_m3_anio", motivo="tecnología PENDIENTE (DEC-043)")
        R.add("EFLUENTES", "EF-ANA", None, "—", motivo="frecuencia PENDIENTE")
        R.add("EFLUENTES", "EF-LODO", None, "lodos_t", motivo="lodos no dimensionados en 09C")
        R.add("EFLUENTES", "EF-CANON", v["efluente_m3_anio"], "efluente_m3_anio")
    if c["frio"] == "C_congelado_tercero":
        R.add("UTILITIES", "UT-FRIO-TER", v["congelado_t_anio"], "congelado_t_anio")
    # ---------------- SUBPRODUCTOS (no se netean con ingresos) ----------------
    if propia:
        for g in ("sangre", "plumas", "visceras", "cabezas"):
            R.add("SUBPRODUCTOS", f"SUB-RET-{g.upper()}", v[f"subproducto_{g}_t_anio"], f"subproducto_{g}_t_anio")
        R.add("SUBPRODUCTOS", "SUB-RET-DECOMISOS", v["decomisos_t_anio"], "decomisos_t_anio")
        R.add("SUBPRODUCTOS", "SUB-CONT", 12.0, "12 meses")
        if c["subproductos"] == "B_basico_propio":
            R.add("SUBPRODUCTOS", "SUB-TRAT-B", None, "—", motivo="tecnología no definida (SUP-16-14)")
            R.add("SUBPRODUCTOS", "SUB-TRAT-ENE", None, "—", motivo="energía del tratamiento no incluida en 09C (tecnología no definida)")
        if c["rendering"]:
            for i in ("SUB-REN-ENE", "SUB-REN-TER", "SUB-REN-AGUA", "SUB-REN-MAN", "SUB-REN-INS", "SUB-REN-TRAT",
                      "SUB-REN-RES", "SUB-REN-LOG"):
                R.add("SUBPRODUCTOS", i, None, "kwh_rendering" if i == "SUB-REN-ENE" else "—", fase="FUTURO",
                      motivo="rendering: arquitectura futura; NO se usan los consumos de 09C (planta de faena)")
    # ---------------- LOGÍSTICA ----------------
    cc = config_capex(c)
    activos = {"POL": True, "HUE": c["pollito"] == "incubacion", "ALI": True,
               "GRA": c["alimento"] == "propia" or c["alimento_facon_mp"] == "empresa", "VIV": True,
               "REF": True, "CON": (v["congelado_t_anio"] or 0) > TOL, "SUB": propia}
    datos = {"POL": (None, None, v["pollitos_a_recibir_anio"]),
             "HUE": (None, None, v.get("huevos_recibidos_anio")),
             "ALI": (v["alimento_viajes_anio"], v["alimento_km_anio"], t_al),
             "GRA": (None, None, v.get("grano_t_anio")),
             "VIV": (v["vivo_viajes_anio"], v["vivo_km_anio"], v["vivo_t_anio"]),
             "REF": (v["refrigerado_viajes_anio"], v["refrigerado_km_anio"], v["refrigerado_t_anio"]),
             "CON": (v["congelado_viajes_anio"], v["congelado_km_anio"], v["congelado_t_anio"]),
             "SUB": (v.get("subproductos_viajes_anio"), v.get("subproductos_km_anio"), v.get("subproductos_t_anio"))}
    for f, (nombre, fc, uni) in FLUJOS.items():
        if not activos[f]:
            continue
        viajes, km, unidades = datos[f]
        ap = "EMPRESA"
        if f in ("POL", "ALI") and aportes(c)["logistica_insumos"] != "EMPRESA" and fp < 1 - TOL:
            ap = aportes(c)["logistica_insumos"]
        propia_f = mcx.flota_de(cc, fc) == "propia"
        if "M09" in _MUT and f == "VIV":                         # mutación: flota tercerizada con costos propios
            propia_f = True
        if propia_f:
            R.add("LOGISTICA", "LOG-COMB-GASOIL", None, "km × L/km", flujo=nombre, aportante=ap,
                  motivo="consumo L/km PENDIENTE (12B CONSUMO_L_KM)")
            R.add("LOGISTICA", f"LOG-{f}-MANT", km, f"{nombre}_km_anio", flujo=nombre, aportante=ap)
            R.add("LOGISTICA", f"LOG-{f}-NEUM", km, f"{nombre}_km_anio", flujo=nombre, aportante=ap)
            R.add("LOGISTICA", f"LOG-{f}-PAT", v[f"vehiculos_{f}"], f"vehiculos_{f}", flujo=nombre, aportante=ap)
            R.add("LOGISTICA", f"LOG-{f}-PEAJ", viajes, f"{nombre}_viajes_anio", flujo=nombre, aportante=ap)
            R.add("LOGISTICA", f"LOG-{f}-LAV", viajes, f"{nombre}_viajes_anio", flujo=nombre, aportante=ap)
            if f in ("POL", "HUE", "REF", "CON"):
                R.add("LOGISTICA", f"LOG-{f}-FRIO", None, "—", flujo=nombre, aportante=ap, motivo="horas de equipo PENDIENTES")
            R.add("LOGISTICA", f"LOG-{f}-TEV", None, "—", flujo=nombre, aportante=ap, motivo="no definido")
            if f not in ("VIV", "REF", "CON"):
                R.add("COSTO_LABORAL", "LAB-CHOF", None, "—", unidad="FTE-año", concepto=f"Choferes de flota propia ({nombre})",
                      submodulo="choferes", flujo=nombre, aportante=ap, motivo="14A no dimensiona choferes de este flujo",
                      centro="logistica", naturaleza="semifijo", tipo="interno",
                      universo_rrhh="RRHH_LOGISTICA_NO_DIMENSIONADO_14A")
        else:
            m = modelo_tarifa(c, f)
            if m is None:
                R.add("LOGISTICA", "", None, "—", unidad="", concepto=f"Flete tercerizado ({nombre}) — modelo de tarifa NO definido",
                      submodulo="tercerizado", flujo=nombre, aportante=ap, motivo="MODELO_TARIFA_NO_DEFINIDO (DEC-17-05)",
                      centro="logistica", naturaleza="variable", tipo="tercerizado")
            else:
                q = {"viaje": viajes, "km": km, "unidad": unidades, "contrato": 1.0}[m]
                sufijo = {"viaje": "VIAJE", "km": "KM", "unidad": "UNI", "contrato": "CONT"}[m]
                R.add("LOGISTICA", f"LOG-{f}-TER-{sufijo}", q, f"{nombre}_{m}", flujo=nombre, aportante=ap,
                      motivo="" if q is not None else "cantidad del modelo elegido PENDIENTE en 12B")
    # ---------------- MANTENIMIENTO ----------------
    areas = {"PROC": propia, "FRIO": propia, "ELEC": propia, "UTIL": propia, "EDIF": True,
             "INC": c["pollito"] == "incubacion", "ALI": c["alimento"] == "propia", "GRA": fp > TOL}
    met = c["mantenimiento_metodo"]
    for a, act in areas.items():
        if not act:
            continue
        if met is None:
            R.add("MANTENIMIENTO", "", None, "—", unidad="", concepto=f"Mantenimiento — área {a} (método NO definido)",
                  submodulo=a.lower(), motivo="METODO_MANTENIMIENTO_NO_DEFINIDO (DEC-17-06); no se usa % CAPEX como verdad",
                  centro="mantenimiento", naturaleza="semivariable", tipo="propio")
            continue
        for tp in TIPOS_MANT_POR_METODO[met]:
            i = f"MAN-{a}-{tp}"
            if met == "pct_capex":
                q, mot = base_capex_area(DR, a), ""
                if q is None:
                    mot = "BASE_SIN_PRECIO: el CAPEX del bloque no tiene total (19_capex)"
                R.add("MANTENIMIENTO", i, q, f"CAPEX USD del área {a}", motivo=mot)
            elif met == "por_activo":
                R.add("MANTENIMIENTO", i, n_activos_area(DR, a), f"activos costeables del área {a} (BOQ 16)")
            elif met == "horas_tecnicas":
                R.add("MANTENIMIENTO", i, None, "—", motivo="horas técnicas externas no dimensionadas (además de 14A)")
            else:
                R.add("MANTENIMIENTO", i, 1.0, "1 contrato-año")
    R.add("MANTENIMIENTO", "", None, "—", unidad="FTE-año", concepto="Mano de obra de mantenimiento", submodulo="personal",
          estado_dim="INCLUIDO", incluido_en="COSTO_LABORAL (14A)", motivo="técnicos y jefe de mantenimiento en 14A",
          centro="mantenimiento", naturaleza="semifijo", tipo="interno")
    # ---------------- CALIDAD / SENASA / HALAL ----------------
    R.add("CALIDAD", "CAL-ANA-MICRO", None, "—", motivo="plan de muestreo PENDIENTE")
    if propia:
        R.add("CALIDAD", "CAL-ANA-AGUA", None, "—", motivo="frecuencia PENDIENTE")
        if c["laboratorio_propio"]:
            R.add("CALIDAD", "CAL-LAB-INS", 1.0, "1 año")
        R.add("CALIDAD", "CAL-SENASA", None, "—", motivo="estructura y base de tasas PENDIENTES (DPV-101); no se inventa")
    R.add("CALIDAD", "CAL-CERT", 1.0, "1 año")
    R.add("CALIDAD", "CAL-AUD", 1.0, "1 año")
    R.add("CALIDAD", "CAL-DOC", 1.0, "1 año")
    R.add("CALIDAD", "CAL-TRAZ", 12.0, "12 meses")
    if c["modulo_halal"]:
        for i in ("HAL-CERT", "HAL-AUD", "HAL-SUP", "HAL-SEG", "HAL-DOC", "HAL-ETQ", "HAL-LOG", "HAL-ANA"):
            R.add("HALAL", i, None, "—", fase="OPCIONAL_MERCADO", motivo="módulo opcional de mercado: sin evidencia")
    # ---------------- ADMINISTRACIÓN, COMERCIAL, SEGUROS ----------------
    for i in ("ADM-CONT", "ADM-LEG", "ADM-SIS", "ADM-COM", "ADM-SEGUR", "ADM-LIMP", "ADM-OTR", "COM-MKT", "COM-VIAJ"):
        R.add("ADMINISTRACION" if i.startswith("ADM") else "COMERCIAL", i, 12.0, "12 meses")
    if any(p["clave"] == "hys_externo" for p in rrhh["puestos"]):
        R.add("ADMINISTRACION", "ADM-HYS", 12.0, "12 meses")
    if propia or c["pollito"] == "incubacion" or c["alimento"] == "propia":
        for i in ("SEG-PLANTA", "SEG-INC", "SEG-INT"):
            R.add("SEGUROS", i, 1.0, "1 póliza-año")
    for i in ("SEG-RC", "SEG-MERC"):
        R.add("SEGUROS", i, 1.0, "1 póliza-año")
    if fp > TOL:
        R.add("SEGUROS", "SEG-GRA", 1.0, "1 póliza-año")
    for f, (nombre, fc, _) in FLUJOS.items():
        if activos[f] and mcx.flota_de(cc, fc) == "propia":
            R.add("SEGUROS", f"SEG-FLOTA-{f}", v[f"vehiculos_{f}"], f"vehiculos_{f}", flujo=nombre)
    # ---------------- COSTO LABORAL (14A) ----------------
    lineas_laborales(R, c, DR)
    clasificar_filas(R.filas, c)
    return R.filas


# ---------------------------------------------------------------------------------------------
# 4 bis. MÓDULO DE ARQUITECTURA Y BLOQUE OPERATIVO DE CADA FILA (completitud estructural)
# ---------------------------------------------------------------------------------------------
BLOQUE_POR_ID = {
    "ALI-A-PT": "materia_prima", "ALI-B-PTE": "materia_prima", "ALI-A-DES": "logistica", "ALI-B-SRV": "servicio_tercero",
    "ALI-B-ALM": "almacenamiento", "ALI-C-ALM": "almacenamiento", "ALI-MERMA": "mermas", "ALI-C-ENE": "energia",
    "ALI-C-TER": "termico", "ALI-C-AGUA": "agua", "ALI-C-ANA": "laboratorio", "ALI-C-MOV": "movimientos_internos",
    "ALI-MP-DIF-MAIZ": "diferencial", "ALI-MP-DIF-SOJA": "diferencial", "POL-COMPRA": "materia_prima",
    "INC-OP-HUEVO": "materia_prima", "INC-OP-VAC": "sanidad", "INC-OP-ENE": "energia", "INC-OP-AGUA": "agua",
    "INC-OP-LIM": "limpieza", "INC-OP-INS": "consumibles", "INC-OP-DES": "residuos", "INC-OP-CAL": "calidad",
    "REP-AVE": "materia_prima", "REP-ALI": "alimento", "REP-SAN": "sanidad", "REP-ENE": "energia", "REP-AGUA": "agua",
    "REP-MAN": "mantenimiento", "REP-RES": "residuos", "REP-LOG": "logistica", "REP-OTR": "otros",
    "PP-SAN": "sanidad", "PP-CAMA": "cama", "PP-GAS": "termico", "PP-CAPT": "captura", "PP-MORT": "residuos",
    "PP-LIMP": "limpieza", "PP-BIO": "bioseguridad", "PP-ENE": "energia", "PP-AGUA": "agua", "PP-VET": "veterinaria",
    "PP-ATE": "sanidad", "PP-PAGO-AVE": "servicio_tercero", "PP-PAGO-KG": "servicio_tercero", "PP-OTR": "otros",
    "FAE-FACON": "servicio_tercero", "FAE-FACON-FRIO": "frio", "FAE-FACON-SUB": "residuos", "FAE-QUIM": "limpieza",
    "FAE-ELEM": "limpieza", "FAE-CUCH": "consumibles", "FAE-SERV": "otros", "UT-FRIO-TER": "frio",
    "SUB-CONT": "residuos", "SUB-TRAT-B": "consumibles", "SUB-TRAT-ENE": "energia", "SUB-REN-ENE": "energia",
    "SUB-REN-TER": "termico", "SUB-REN-AGUA": "agua", "SUB-REN-MAN": "mantenimiento", "SUB-REN-INS": "consumibles",
    "SUB-REN-TRAT": "tratamiento", "SUB-REN-RES": "residuos", "SUB-REN-LOG": "logistica",
}
UNIVERSO_UTIL_POR_PREFIJO = (("UT-", "FAENA_09C"), ("EF-", "FAENA_09C"), ("INC-OP-ENE", "INCUBACION"),
                             ("INC-OP-AGUA", "INCUBACION"), ("ALI-C-ENE", "PLANTA_ALIMENTO"), ("ALI-C-TER", "PLANTA_ALIMENTO"),
                             ("ALI-C-AGUA", "PLANTA_ALIMENTO"), ("PP-ENE", "GRANJAS"), ("PP-GAS", "GRANJAS"),
                             ("PP-AGUA", "GRANJAS"), ("SUB-REN-ENE", "RENDERING"), ("SUB-REN-TER", "RENDERING"),
                             ("SUB-REN-AGUA", "RENDERING"), ("SUB-TRAT-ENE", "TRATAMIENTO_SUBPRODUCTOS"),
                             ("REP-ENE", "REPRODUCTORAS"), ("REP-AGUA", "REPRODUCTORAS"))
AREA_MODULO = {"proc": "FAENA_PROPIA", "frio": "FAENA_PROPIA", "elec": "FAENA_PROPIA", "util": "FAENA_PROPIA",
               "inc": "INCUBACION_PROPIA", "ali": "PLANTA_ALIMENTO_PROPIA", "gra": "GRANJAS_PROPIAS"}
UNIVERSO_RRHH_MODULO = {"RRHH_GRANJAS_PROPIAS_PENDIENTE": "GRANJAS_PROPIAS", "RRHH_INCUBACION_PENDIENTE": "INCUBACION_PROPIA",
                        "RRHH_PLANTA_ALIMENTO_PENDIENTE": "PLANTA_ALIMENTO_PROPIA",
                        "RRHH_REPRODUCTORAS_FUTURO": "REPRODUCTORAS_FUTURO", "RRHH_RENDERING_FUTURO": "RENDERING_FUTURO"}


def _modulos_flujo(c):
    faena = "FAENA_PROPIA" if c["faena"] == "propia" else "FAENA_FACON"
    alim = {"compra": "ALIMENTO_COMPRADO", "facon": "ALIMENTO_FACON", "propia": "PLANTA_ALIMENTO_PROPIA"}[c["alimento"]]
    pol = "POLLITO_COMPRADO" if c["pollito"] == "compra" else "INCUBACION_PROPIA"
    return faena, alim, pol


def clasificar_fila(f, c):
    """(MODULO_ARQ, BLOQUE) de una fila: a qué módulo de la arquitectura pertenece y qué bloque operativo cubre."""
    faena, alim, pol = _modulos_flujo(c)
    i, mod, sub, fl = f["COSTO_ID"], f["MODULO"], f["SUBMODULO"], f["FLUJO"]
    granja = "GRANJAS_PROPIAS" if f["AMBITO_GRANJA"] == "PROPIA" else "GRANJAS_INTEGRADAS"
    if mod == "ALIMENTO":
        return alim, BLOQUE_POR_ID.get(i, "materia_prima")
    if mod == "POLLITOS":
        return "POLLITO_COMPRADO", "materia_prima"
    if mod == "INCUBACION":
        return "INCUBACION_PROPIA", BLOQUE_POR_ID[i]
    if mod == "REPRODUCTORAS":
        return "REPRODUCTORAS_FUTURO", BLOQUE_POR_ID[i]
    if mod == "PRODUCCION_PRIMARIA":
        return granja, BLOQUE_POR_ID[i]
    if mod == "FAENA":
        return ("FAENA_FACON" if i.startswith("FAE-FACON") else faena), BLOQUE_POR_ID.get(i, "limpieza")
    if mod == "EMPAQUE":
        return faena, "empaque"
    if mod == "UTILITIES":
        if i == "UT-FRIO-TER":
            return faena, "frio"
        return "FAENA_PROPIA", ("termico" if i.startswith("UT-TER") else "agua" if i.startswith("UT-AGUA") else "energia")
    if mod == "EFLUENTES":
        return "FAENA_PROPIA", "efluentes"
    if mod == "SUBPRODUCTOS":
        if i.startswith("SUB-REN"):
            return "RENDERING_FUTURO", BLOQUE_POR_ID[i]
        if i.startswith("SUB-TRAT"):
            return "TRATAMIENTO_SUBPRODUCTOS_PROPIO", BLOQUE_POR_ID[i]
        return "FAENA_PROPIA", "residuos"
    if mod == "LOGISTICA" or (mod == "SEGUROS" and i.startswith("SEG-FLOTA")) or (mod == "COSTO_LABORAL" and sub == "choferes"):
        if fl == "huevos":
            return "INCUBACION_PROPIA", "logistica_huevo"
        if fl == "pollitos":
            return pol, ("logistica_pollito" if pol == "INCUBACION_PROPIA" else "logistica")
        if fl in ("alimento", "grano"):
            return alim, "logistica"
        if fl == "subproductos":
            return "FAENA_PROPIA", "logistica"
        return faena, "logistica"
    if mod == "MANTENIMIENTO":
        area = i.split("-")[1].lower() if i.startswith("MAN-") else sub
        if area == "edif" or area == "personal":
            return (faena if c["faena"] == "propia" else "ESTRUCTURA"), "mantenimiento"
        return AREA_MODULO.get(area, faena), "mantenimiento"
    if mod == "CALIDAD":
        if i in ("CAL-CERT", "CAL-AUD", "CAL-DOC", "CAL-TRAZ"):
            return "ESTRUCTURA", "calidad"
        return faena, "calidad"
    if mod == "HALAL":
        return "MERCADO_HALAL_OPCIONAL", "calidad"
    if mod in ("ADMINISTRACION", "COMERCIAL"):
        return "ESTRUCTURA", "administracion"
    if mod == "SEGUROS":
        if i == "SEG-GRA":
            return "GRANJAS_PROPIAS", "seguros"
        if i in ("SEG-PLANTA", "SEG-INC", "SEG-INT"):
            return (faena if c["faena"] == "propia" else "ESTRUCTURA"), "seguros"
        return "ESTRUCTURA", "seguros"
    if mod == "COSTO_LABORAL":
        u = f["UNIVERSO_RRHH"]
        if u in UNIVERSO_RRHH_MODULO:
            return UNIVERSO_RRHH_MODULO[u], "rrhh"
        if sub == "tratamiento_subproductos":
            return "TRATAMIENTO_SUBPRODUCTOS_PROPIO", "rrhh"
        if sub == "captura":
            return granja if c["fraccion_granjas_propias"] < 1 - TOL else "GRANJAS_PROPIAS", "captura"
        if sub == "laboratorio":
            return faena, "calidad"
        if u == "COORDINACION_PRIMARIA_14A":
            return ("GRANJAS_INTEGRADAS" if c["fraccion_granjas_propias"] < 1 - TOL else "GRANJAS_PROPIAS"), "rrhh"
        if u in ("ESTRUCTURA_14A",) or sub == "hys_externo":
            return "ESTRUCTURA", "rrhh"
        if sub in ("choferes_aves", "choferes_producto"):
            return faena, "logistica"
        return faena, "rrhh"
    return "ESTRUCTURA", "otros"


def clasificar_filas(filas, c):
    for f in filas:
        f["MODULO_ARQ"], f["BLOQUE"] = clasificar_fila(f, c)
        f["UNIVERSO_UTILITIES"] = "" if f["COSTO_ID"] == "UT-FRIO-TER" else next(
            (u for pre, u in UNIVERSO_UTIL_POR_PREFIJO if f["COSTO_ID"].startswith(pre)), "")
        if f["MODULO"] == "UTILITIES" and not f["COSTO_ID"]:
            f["UNIVERSO_UTILITIES"] = "FAENA_09C"                   # energía de frío/bombeo/efluentes ya incluida en 09C


# Mantenimiento: áreas ↔ bloques del BOQ de CAPEX
AREA_BLOQUES = {"PROC": ("PROCESO", "SUBPRODUCTOS"), "FRIO": ("FRIO",), "ELEC": ("UTILITIES",), "UTIL": ("UTILITIES", "EFLUENTES"),
                "EDIF": ("OBRA_CIVIL",), "INC": ("INCUBACION",), "ALI": ("ALIMENTO",), "GRA": ("GRANJAS",)}


def _filas_area(DR, a):
    out = []
    for f in DR["capex_filas"]:
        if f["BLOQUE"] not in AREA_BLOQUES[a] or not f["COSTEA"] or f["FASE"] != "INICIAL" or f["TITULAR"] != "EMPRESA":
            continue
        es_el = f["ACTIVO_ID"].startswith("EL-")
        if (a == "ELEC" and not es_el) or (a == "UTIL" and f["BLOQUE"] == "UTILITIES" and es_el):
            continue
        out.append(f)
    return out


def n_activos_area(DR, a):
    n = len(_filas_area(DR, a))
    return float(n) if n else None


def base_capex_area(DR, a):
    fs = _filas_area(DR, a)
    if not fs or any(f["ESTADO_COSTO"] != "CON_PRECIO" for f in fs):
        return None
    return sum(f["COSTO_INSTALADO_USD"] for f in fs)


def categoria_laboral(p):
    if p["clave"] in ("choferes_aves", "choferes_producto"):
        return "CHOF"
    g, k = p["grupo"], p["contrato"]
    if g == "directo":
        return "CONV_DIR"
    if g == "supervision":
        return "FC_SUP"
    if g == "direccion":
        return "DIR"
    if g == "administracion":
        return "FC_ADM"
    return "CONV_SOP" if k == "convenio_pendiente" else "FC_PRO"


def centro_laboral(p):
    k, cat = p["clave"], p["categoria"]
    if p.get("subfuncion") in ("QC", "QA", "INOCUIDAD", "TRAZABILIDAD", "LABORATORIO"):
        return "calidad"
    if k in ("tecnicos_mantenimiento", "jefe_mantenimiento", "panolero"):
        return "mantenimiento"
    if k in ("hys", "lavanderia"):
        return "servicios_generales"
    if k in ("ventas", "gerente_comercial"):
        return "comercial"
    return {"operacion_industrial": "faena", "logistica": "logistica", "produccion_primaria": "produccion_primaria",
            "administracion": "administracion", "direccion": "administracion"}.get(cat, "servicios_generales")


AREA_TERCERIZADA = {"limpieza_operativa": "LIMP", "limpieza_sanitizacion": "LIMP", "supervisor_saneamiento": "LIMP",
                    "tecnicos_mantenimiento": "MANT", "jefe_mantenimiento": "MANT"}
NATURALEZA_DRIVER_14A = {"produccion": "semifijo", "activos": "semifijo", "casi_fijo": "fijo", "estrategia": "semifijo"}
INCLUIDO_SERVICIO = {"captura": "PP-CAPT", "hys_externo": "ADM-HYS", "laboratorio": "CAL-ANA-MICRO"}


UNIVERSO_14A = {"operacion_industrial": "INDUSTRIAL_14A", "soporte_industrial": "INDUSTRIAL_14A",
                "logistica": "INDUSTRIAL_14A", "administracion": "ESTRUCTURA_14A", "direccion": "ESTRUCTURA_14A",
                "produccion_primaria": "COORDINACION_PRIMARIA_14A"}
# Universos de RRHH que 14A NO dimensiona: se registran como PENDIENTE (o FUTURO), nunca con FTE fabricados
UNIVERSOS_PENDIENTES = {"personal_granja": ("RRHH_GRANJAS_PROPIAS_PENDIENTE", "Personal de granjas propias", "produccion_primaria"),
                        "personal_incubadora": ("RRHH_INCUBACION_PENDIENTE", "Personal de incubadora", "incubacion"),
                        "personal_planta_alimento": ("RRHH_PLANTA_ALIMENTO_PENDIENTE", "Personal de planta de alimento", "alimento"),
                        "operacion_efluentes": ("RRHH_INDUSTRIAL_NO_DIMENSIONADO_14A",
                                                "Operación de planta de efluentes (puede estar cubierta por mantenimiento)",
                                                "servicios_generales"),
                        "tratamiento_subproductos": ("RRHH_INDUSTRIAL_NO_DIMENSIONADO_14A",
                                                     "Operación del tratamiento básico de subproductos", "servicios_generales"),
                        "personal_reproductoras": ("RRHH_REPRODUCTORAS_FUTURO", "Personal de reproductoras", "incubacion"),
                        "personal_rendering": ("RRHH_RENDERING_FUTURO", "Personal de rendering", "servicios_generales")}


def lineas_laborales(R, c, DR):
    DR["_filas_lab_pend"] = []
    rr = DR["rrhh"]
    da = DR["dias_anio"]
    cc = config_capex(c)
    for p in rr["puestos"]:
        if p["grupo"] not in mr.GRUPOS:
            continue                                            # inspección oficial: fuera de la empresa (CAL-SENASA)
        cat = categoria_laboral(p)
        cen = centro_laboral(p)
        nat = NATURALEZA_DRIVER_14A.get(p["driver"], "semifijo")
        uni = UNIVERSO_14A.get(p["categoria"], "INDUSTRIAL_14A")
        kw = dict(submodulo=p["clave"], concepto=p["puesto"], centro=cen)
        if p["clave"] in INCLUIDO_SERVICIO and not (p["fte_interno"] or 0) > TOL:
            R.add("COSTO_LABORAL", "", None, "—", unidad="", estado_dim="INCLUIDO", incluido_en=INCLUIDO_SERVICIO[p["clave"]],
                  motivo="servicio por unidad: se costea en el concepto de servicio", naturaleza=nat, tipo="tercerizado",
                  universo_rrhh="TERCERO_INCLUIDO_EN_SERVICIO", **kw)
            continue
        if p["estado"] == "PENDIENTE":
            R.add("COSTO_LABORAL", f"LAB-{cat}", None, p["clave"], unidad="FTE-año", motivo="dotación PENDIENTE en 14A",
                  naturaleza=nat, tipo="interno", universo_rrhh=uni, **kw)
            continue
        if (p["fte_interno"] or 0) > TOL:
            R.add("COSTO_LABORAL", f"LAB-{cat}", p["fte_interno"], f"FTE interno 14A ({p['clave']})", unidad="FTE-año",
                  motivo="PROVISIONAL_POR_FTE (headcount PENDIENTE)", naturaleza=nat, tipo="interno", universo_rrhh=uni, **kw)
        if (p["fte_tercerizado"] or 0) > TOL:
            horas = (p["horas_contratadas_dia"] or 0) * da
            if c["faena"] == "facon" and p["categoria"] == "operacion_industrial" and "M11" not in _MUT:
                R.add("COSTO_LABORAL", "", horas, f"horas contratadas 14A ({p['clave']})", unidad="hora", aportante="TERCERO",
                      estado_dim="INCLUIDO", incluido_en="FAE-FACON", motivo="RECURSO_FISICO_DE_TERCERO (personal del faenador): "
                      "costo INCLUIDO_EN_TARIFA_FACON; horas visibles para trazabilidad (14A)", naturaleza="variable",
                      tipo="tercerizado", universo_rrhh="TERCERO_INCLUIDO_EN_TARIFA", **kw)
                continue
            if p["clave"] in ("choferes_aves", "choferes_producto"):
                fl = "vivo" if p["clave"] == "choferes_aves" else "refrigerado"
                incl = "flete tercerizado (LOG-*-TER)" if mcx.flota_de(cc, fl) != "propia" else ""
                if "M10" in _MUT:
                    incl = ""
                if incl:
                    R.add("COSTO_LABORAL", "", horas, f"horas contratadas 14A ({p['clave']})", unidad="hora",
                          aportante="TERCERO", estado_dim="INCLUIDO", incluido_en=incl,
                          motivo="RECURSO_FISICO_DE_TERCERO (chofer del transportista): costo INCLUIDO_EN_TARIFA_FLETE; "
                          "horas visibles", naturaleza="variable", tipo="tercerizado",
                          universo_rrhh="TERCERO_INCLUIDO_EN_TARIFA", **kw)
                    continue
                area = "LOG"
            else:
                area = AREA_TERCERIZADA.get(p["clave"], "OTR")
            R.add("COSTO_LABORAL", f"LAB-TER-{area}", horas, f"horas contratadas 14A ({p['clave']})",
                  naturaleza="variable", tipo="tercerizado", universo_rrhh=uni, **kw)
    # Universos de RRHH que 14A NO dimensiona (no se inventan dotaciones)
    faltan = []
    if c["fraccion_granjas_propias"] > TOL:
        faltan.append("personal_granja")
    if c["pollito"] == "incubacion":
        faltan.append("personal_incubadora")
    if c["alimento"] == "propia":
        faltan.append("personal_planta_alimento")
    if c["faena"] == "propia":
        faltan.append("operacion_efluentes")
    if c["subproductos"] == "B_basico_propio" and c["faena"] == "propia":
        faltan.append("tratamiento_subproductos")
    if c["reproductoras"]:
        faltan.append("personal_reproductoras")
    if c["rendering"]:
        faltan.append("personal_rendering")
    if "M14" in _MUT and "personal_incubadora" in faltan:     # mutación: se omite un bloque material
        faltan.remove("personal_incubadora")
    for k in faltan:
        uni, n, cen = UNIVERSOS_PENDIENTES[k]
        fut = uni.endswith("FUTURO")
        DR.setdefault("_filas_lab_pend", []).append(R.add(
              "COSTO_LABORAL", "LAB-CONV_SOP", None, k, unidad="FTE-año", concepto=n, submodulo=k, centro=cen,
              naturaleza="semifijo", tipo="interno", fase="FUTURO" if fut else "OPERACION", universo_rrhh=uni,
              motivo=("arquitectura FUTURA: dotación sin evidencia" if fut else
                      "14A no dimensiona esta función: FTE PENDIENTE (no se reutilizan FTE industriales)")))
    R.add("COSTO_LABORAL", "", DR["v"]["horas_brecha_jornada_anio"], "horas_brecha_jornada_anio", unidad="h-persona",
          concepto="Brecha de jornada a organizar (turnos, relevos, personal adicional u horas extra)", submodulo="brecha",
          estado_dim="INFORMATIVO", motivo="NO son horas extra automáticas (14A, DPV-146)", centro="faena",
          naturaleza="semivariable", tipo="interno", universo_rrhh="INDUSTRIAL_14A")


def fte_universos(c, DR):
    """FTE por universo. FTE_TOTAL_CONOCIDO = solo lo que 14A dimensiona para la EMPRESA (industrial + estructura +
    coordinación primaria), sin terceros cuyo costo está dentro de una tarifa. Lo no dimensionado es PENDIENTE."""
    cc = config_capex(c)
    emp = terc = 0.0
    for p in DR["rrhh"]["puestos"]:
        if p["grupo"] not in mr.GRUPOS:
            continue
        emp += p["fte_interno"] or 0
        ft = p["fte_tercerizado"] or 0
        if not ft:
            continue
        incluido = (c["faena"] == "facon" and p["categoria"] == "operacion_industrial") or (
            p["clave"] in ("choferes_aves", "choferes_producto")
            and mcx.flota_de(cc, "vivo" if p["clave"] == "choferes_aves" else "refrigerado") != "propia")
        if incluido:
            terc += ft
        else:
            emp += ft
    pend = []
    if c["fraccion_granjas_propias"] > TOL:
        pend.append("granjas propias")
    if c["pollito"] == "incubacion":
        pend.append("incubación")
    if c["alimento"] == "propia":
        pend.append("planta de alimento")
    if c["faena"] == "propia":
        pend.append("operación de efluentes")
    if c["subproductos"] == "B_basico_propio" and c["faena"] == "propia":
        pend.append("tratamiento de subproductos")
    fut = [x for x, ok in (("reproductoras", c["reproductoras"]), ("rendering", c["rendering"])) if ok]
    return {"FTE_INDUSTRIAL_14A": DR["rrhh"]["fte_total"], "FTE_TOTAL_CONOCIDO": emp,
            "FTE_TERCEROS_INCLUIDOS_EN_TARIFAS": terc,
            "FTE_ADICIONAL_PENDIENTE": ("PENDIENTE: " + ", ".join(pend)) if pend else "NINGUNO IDENTIFICADO",
            "FTE_FUTURO_NO_DIMENSIONADO": ", ".join(fut)}


# ---------------------------------------------------------------------------------------------
# 5. COSTEO
# ---------------------------------------------------------------------------------------------
def costear(filas, base, fecha_base=FECHA_BASE_OPEX, aves_anio=None):
    for f in filas:
        al = []
        f["PRECIO_USD"] = None
        f["COSTO_CALCULADO_USD_ANIO"] = None
        f["COSTO_CONCEPTO_USD_AVE"] = None
        f["EVIDENCIA"] = "PENDIENTE"
        nat = f["NATURALEZA"]
        b = base.get(f["COSTO_ID"]) if f["COSTO_ID"] else None
        pv = _num(b["PCT_VARIABLE"]) if b else ({"variable": 100.0, "fijo": 0.0, "semifijo": 0.0}.get(nat))
        if f["COSTO_ID"].startswith("LAB-") and not b:
            pv = {"variable": 100.0, "fijo": 0.0, "semifijo": 0.0}.get(nat)
        f["PCT_VARIABLE"] = pv
        f["PCT_FIJO"] = None if pv is None else 100 - pv
        f["FIJO_VARIABLE"] = nat + ("" if pv is not None else " (reparto PENDIENTE)")
        if b and _num(b["PRECIO_UNITARIO"]) is not None and b["ESTADO"] == "CON_PRECIO":
            # PRECIO OBSERVADO (moneda original) ≠ CONVERSIÓN DEL MODELO (USD): se guardan por separado
            f.update(PRECIO_ORIGINAL_OBSERVADO=_num(b["PRECIO_UNITARIO"]), MONEDA_ORIGINAL=b["MONEDA_ORIGINAL"],
                     FECHA_PRECIO=b["FECHA_PRECIO"], CONDICION_ENTREGA=b["CONDICION_ENTREGA"], IVA_PRECIO=b["IVA_TRATAMIENTO"],
                     TC_USADO=_num(b["TC_MONEDA_POR_USD"]), FECHA_TC=b["FECHA_TC"],
                     ORIGEN_PRECIO_USD=b["ORIGEN_PRECIO_USD"] or ("OBSERVADO_EN_USD" if b["MONEDA_ORIGINAL"] == "USD" else ""))
        if f["ESTADO_DIMENSION"] in ("INCLUIDO", "INFORMATIVO"):
            if f["ESTADO_DIMENSION"] == "INFORMATIVO":
                f["ESTADO"] = "INFORMATIVO"
            elif f["INCLUIDO_EN"] == "FAE-FACON":
                f["ESTADO"] = "INCLUIDO_EN_TARIFA_FACON"
            elif f["INCLUIDO_EN"].startswith("flete"):
                f["ESTADO"] = "INCLUIDO_EN_TARIFA_FLETE"
            else:
                f["ESTADO"] = "INCLUIDO_EN_OTRO_CONCEPTO"
            continue
        if f["FASE"] == "FUTURO":
            f["ESTADO"] = "FUTURO"
            continue
        if f["APORTANTE"] == "PENDIENTE":
            f["ESTADO"] = "APORTANTE_PENDIENTE"
            continue
        if f["CANTIDAD"] is None:
            f["ESTADO"] = "PENDIENTE_CANTIDAD"
            continue
        # precio
        if f["COSTO_ID"].startswith("LAB-") and not b:
            p, niv, falt, _ = costo_empresa_fte(f["COSTO_ID"][4:], base)
            if p is None:
                f["ESTADO"] = "PENDIENTE_PRECIO"
                al.append("COMPONENTES_FALTANTES:" + "/".join(falt))
            else:
                f["PRECIO_USD"], f["EVIDENCIA"] = p, niv
        elif b is None:
            f["ESTADO"] = "PENDIENTE_PRECIO"
        else:
            p = precio_usd(b)
            if _num(b["PRECIO_UNITARIO"]) is None:
                f["ESTADO"] = "PENDIENTE_PRECIO"
            elif p is None:
                f["ESTADO"] = "SIN_TIPO_DE_CAMBIO"
            elif b["ESTADO"] != "CON_PRECIO":
                f["ESTADO"] = "PENDIENTE_PRECIO"
                al.append(f"PRECIO_{b['ESTADO']}_NO_USADO")
            else:
                f["PRECIO_USD"], f["EVIDENCIA"] = p, b["NIVEL_EVIDENCIA"]
                if b["FECHA_PRECIO"] and b["FECHA_PRECIO"] < fecha_base:
                    al.append("PRECIO_ANTERIOR_A_FECHA_BASE (sin indexar)")
                if b["FLETE_INCLUIDO"] == "PENDIENTE":
                    al.append("FLETE_INCLUIDO_PENDIENTE (posible doble conteo con LOG-*)")
                if b["IVA_TRATAMIENTO"] in ("", "PENDIENTE"):
                    al.append("IVA_NO_RESUELTO")
        if f["PRECIO_USD"] is not None:
            if f["UNIDAD"] == "%":
                f["COSTO_CALCULADO_USD_ANIO"] = f["CANTIDAD"] * f["PRECIO_USD"] / 100
            else:
                f["COSTO_CALCULADO_USD_ANIO"] = f["CANTIDAD"] * f["PRECIO_USD"]
            f["ESTADO"] = "CON_PRECIO"
            if aves_anio:
                f["COSTO_CONCEPTO_USD_AVE"] = f["COSTO_CALCULADO_USD_ANIO"] / aves_anio
        elif "M01" in _MUT:                                       # mutación: faltante → 0
            f["COSTO_CALCULADO_USD_ANIO"] = 0.0
            f["ESTADO"] = "CON_PRECIO"
            f["EVIDENCIA"] = "E5"
        if "M06" in _MUT and f["EVIDENCIA"] == "E4":
            f["EVIDENCIA"] = "E1"
        if "M07" in _MUT and f["COSTO_CALCULADO_USD_ANIO"]:
            f["COSTO_CALCULADO_USD_ANIO"] = -f["COSTO_CALCULADO_USD_ANIO"]
        f["ALERTAS"] = "; ".join(al)
    return filas


def calidad_monto(niveles):
    return mcx.calidad_monto(niveles)


# ---------------------------------------------------------------------------------------------
# 5 bis. COMPLETITUD DE ARQUITECTURAS (estructura ≠ dimensión física ≠ costeo)
# ---------------------------------------------------------------------------------------------
# Bloques operativos MATERIALES de cada módulo propio o contratado. Un bloque sin fila = AUSENTE (error de modelo);
# con filas sin cantidad o precio = PENDIENTE; nunca 0.
BLOQUES_REQUERIDOS = {
    "FAENA_PROPIA": ("rrhh", "energia", "termico", "agua", "efluentes", "consumibles", "limpieza", "empaque",
                     "mantenimiento", "residuos", "calidad", "seguros", "logistica"),
    "FAENA_FACON": ("servicio_tercero", "rrhh", "frio", "residuos", "empaque", "calidad", "logistica"),
    "GRANJAS_PROPIAS": ("rrhh", "energia", "termico", "agua", "cama", "limpieza", "bioseguridad", "sanidad",
                        "mantenimiento", "residuos", "seguros", "veterinaria", "captura", "otros"),
    "GRANJAS_INTEGRADAS": ("servicio_tercero", "sanidad", "rrhh", "captura", "costo_productor"),
    "POLLITO_COMPRADO": ("materia_prima", "logistica"),
    "INCUBACION_PROPIA": ("materia_prima", "sanidad", "energia", "rrhh", "agua", "limpieza", "mantenimiento",
                          "consumibles", "residuos", "logistica_huevo", "logistica_pollito", "calidad"),
    "ALIMENTO_COMPRADO": ("materia_prima", "logistica"),
    "ALIMENTO_FACON": ("materia_prima", "servicio_tercero", "logistica"),
    "PLANTA_ALIMENTO_PROPIA": ("materia_prima", "diferencial", "rrhh", "energia", "termico", "agua", "mantenimiento",
                               "laboratorio", "mermas", "almacenamiento", "movimientos_internos", "logistica"),
    "TRATAMIENTO_SUBPRODUCTOS_PROPIO": ("rrhh", "energia", "consumibles"),
    "ESTRUCTURA": ("rrhh", "administracion", "seguros", "calidad"),
    "REPRODUCTORAS_FUTURO": ("rrhh", "materia_prima", "alimento", "sanidad", "energia", "agua", "mantenimiento",
                             "residuos", "logistica"),
    "RENDERING_FUTURO": ("rrhh", "energia", "termico", "agua", "mantenimiento", "consumibles", "tratamiento", "residuos",
                         "logistica"),
}
BLOQUES_FACON_B1 = ("diferencial", "almacenamiento", "mermas")
COLUMNAS_BLOQUE = {"RRHH": ("rrhh",), "ENERGIA": ("energia",), "TERMICO": ("termico",), "AGUA": ("agua",),
                   "MANTENIMIENTO": ("mantenimiento",), "CONSUMIBLES": ("consumibles", "cama", "empaque"),
                   "LIMPIEZA": ("limpieza",), "LOGISTICA": ("logistica", "logistica_huevo", "logistica_pollito", "captura")}


def modulos_activos(c):
    faena, alim, pol = _modulos_flujo(c)
    fp = c["fraccion_granjas_propias"]
    act = {faena: "INICIAL", alim: "INICIAL", pol: "INICIAL", "ESTRUCTURA": "INICIAL"}
    if fp > TOL:
        act["GRANJAS_PROPIAS"] = "INICIAL"
    if fp < 1 - TOL:
        act["GRANJAS_INTEGRADAS"] = "INICIAL"
    if c["subproductos"] == "B_basico_propio" and c["faena"] == "propia":
        act["TRATAMIENTO_SUBPRODUCTOS_PROPIO"] = "INICIAL"
    if c["reproductoras"]:
        act["REPRODUCTORAS_FUTURO"] = "FUTURO"
    if c["rendering"]:
        act["RENDERING_FUTURO"] = "FUTURO"
    return act


def requeridos(c, m):
    req = BLOQUES_REQUERIDOS[m]
    if m == "ALIMENTO_FACON" and c["alimento_facon_mp"] == "empresa":
        req = req + BLOQUES_FACON_B1
    if m == "ALIMENTO_FACON" and c["alimento_facon_mp"] == "elaborador":
        req = ("materia_prima", "logistica")            # B2: precio integral (el servicio está dentro del precio)
    return req


def _estado(filas_b, cuenta):
    """Estado de un bloque según sus filas costeables (o futuras): COMPLETO / PARCIAL / PENDIENTE."""
    if not filas_b:
        return "INCLUIDO_EN_OTRO"
    n = len(filas_b)
    k = sum(1 for f in filas_b if cuenta(f))
    return "COMPLETO" if k == n else ("PARCIAL" if k else "PENDIENTE")


def _combinar(estados):
    e = [x for x in estados if x != "NO_APLICA"]
    if not e:
        return "NO_APLICA"
    if "AUSENTE" in e:
        return "AUSENTE"
    e = [x for x in e if x != "INCLUIDO_EN_OTRO"] or ["COMPLETO"]
    if all(x == "COMPLETO" for x in e):
        return "COMPLETO"
    if all(x == "PENDIENTE" for x in e):
        return "PENDIENTE"
    return "PARCIAL"


CAMPOS_COMP = ["ESCENARIO", "CONFIGURACION", "ESCALA_AVES_DIA", "MODULO_ARQ", "FASE", "DRIVER_FISICO", "CANTIDAD", "PRECIO",
               "RRHH", "ENERGIA", "TERMICO", "AGUA", "MANTENIMIENTO", "CONSUMIBLES", "LIMPIEZA", "LOGISTICA",
               "OTROS_BLOQUES", "BLOQUES_REQUERIDOS", "BLOQUES_REPRESENTADOS", "BLOQUES_AUSENTES",
               "BLOQUES_CON_CANTIDAD", "BLOQUES_COSTEADOS", "COBERTURA_ESTRUCTURAL_PCT", "COBERTURA_FISICA_PCT",
               "COBERTURA_COSTEO_PCT", "FILAS_COSTO_PRODUCTOR", "MODULO_ESTRUCTURA_COMPLETA",
               "MODULO_OPERATIVAMENTE_COMPLETO", "MODULO_COSTEABLE", "ESTADO_MODULO", "FALTANTES"]


def completitud(c, filas):
    """Matriz de completitud por módulo y banderas de la arquitectura. Distingue:
    ESTRUCTURAL ('sé qué costos existen': bloque representado aunque esté PENDIENTE), FÍSICA (bloque con cantidades) y
    COSTEO ('sé cuánto cuestan': bloque con precio)."""
    rows = []
    tot = {"req": 0, "rep": 0, "fis": 0, "cos": 0}
    flags = {"estructura": True, "operativa": True, "costeable": True}
    for m, fase in modulos_activos(c).items():
        fm = [f for f in filas if f["MODULO_ARQ"] == m]
        req = requeridos(c, m)
        est_b, cant_b, cost_b, ausentes, falt = {}, {}, {}, [], []
        for b in req:
            if b == "costo_productor":
                fb = [f for f in fm if f["APORTANTE"] == "PRODUCTOR_INTEGRADO"]
                est_b[b] = cost_b[b] = "INFORMATIVO" if fb else "AUSENTE"
                cant_b[b] = "COMPLETO" if fb else "AUSENTE"
                if not fb:
                    ausentes.append(b)
                continue
            fb = [f for f in fm if f["BLOQUE"] == b]
            if not fb:
                est_b[b] = cant_b[b] = cost_b[b] = "AUSENTE"
                ausentes.append(b)
                continue
            fc = [f for f in fb if f["COSTEA"] or f["FASE"] == "FUTURO"]
            cost_b[b] = _estado(fc, lambda f: f["ESTADO"] == "CON_PRECIO")
            cant_b[b] = _estado(fc, lambda f: f["CANTIDAD"] is not None)
            # estado del bloque: COMPLETO (con precio) / PARCIAL (algo dimensionado o con precio) / PENDIENTE (nada)
            est_b[b] = cost_b[b] if cost_b[b] != "PENDIENTE" else ("PARCIAL" if cant_b[b] in ("COMPLETO", "PARCIAL") else "PENDIENTE")
            if cost_b[b] not in ("COMPLETO", "INCLUIDO_EN_OTRO"):
                falt.append(f"{b}: precio {cost_b[b]}, cantidad {cant_b[b]}")
        fcost = [f for f in fm if f["COSTEA"] or f["FASE"] == "FUTURO"]
        n_req = len(req)
        rep_ = n_req - len(ausentes)
        fis = sum(1 for b in req if cant_b[b] in ("COMPLETO", "INCLUIDO_EN_OTRO"))
        cos = sum(1 for b in req if cost_b[b] in ("COMPLETO", "INCLUIDO_EN_OTRO", "INFORMATIVO"))
        r = {"MODULO_ARQ": m, "FASE": fase,
             "DRIVER_FISICO": _estado(fcost, lambda f: f["DRIVER"] not in ("", "—")) if fcost else "NO_APLICA",
             "CANTIDAD": _estado(fcost, lambda f: f["CANTIDAD"] is not None) if fcost else "NO_APLICA",
             "PRECIO": _estado(fcost, lambda f: f["ESTADO"] == "CON_PRECIO") if fcost else "NO_APLICA",
             **{col: _combinar([est_b[b] if b in req else "NO_APLICA" for b in bs]) for col, bs in COLUMNAS_BLOQUE.items()},
             "OTROS_BLOQUES": "; ".join(f"{b}:{est_b[b]}" for b in req
                                        if not any(b in bs for bs in COLUMNAS_BLOQUE.values())),
             "BLOQUES_REQUERIDOS": n_req, "BLOQUES_REPRESENTADOS": rep_, "BLOQUES_AUSENTES": ", ".join(ausentes),
             "BLOQUES_CON_CANTIDAD": fis, "BLOQUES_COSTEADOS": cos,
             "COBERTURA_ESTRUCTURAL_PCT": 100 * rep_ / n_req, "COBERTURA_FISICA_PCT": 100 * fis / n_req,
             "COBERTURA_COSTEO_PCT": 100 * cos / n_req,
             "FILAS_COSTO_PRODUCTOR": sum(1 for f in fm if f["APORTANTE"] == "PRODUCTOR_INTEGRADO"),
             "MODULO_ESTRUCTURA_COMPLETA": not ausentes, "MODULO_OPERATIVAMENTE_COMPLETO": not ausentes and fis == n_req,
             "FALTANTES": "; ".join(([f"AUSENTE: {', '.join(ausentes)}"] if ausentes else []) + falt)}
        r["MODULO_COSTEABLE"] = r["MODULO_OPERATIVAMENTE_COMPLETO"] and cos == n_req and not any(
            f["ESTADO"] == "APORTANTE_PENDIENTE" for f in fm)
        r["ESTADO_MODULO"] = ("COMPLETO" if r["MODULO_COSTEABLE"] else "PENDIENTE" if cos == 0 and fis == 0 else "PARCIAL")
        rows.append(r)
        if fase == "INICIAL":
            tot["req"] += n_req
            tot["rep"] += rep_
            tot["fis"] += fis
            tot["cos"] += cos
            flags["estructura"] &= r["MODULO_ESTRUCTURA_COMPLETA"]
            flags["operativa"] &= r["MODULO_OPERATIVAMENTE_COMPLETO"]
            flags["costeable"] &= r["MODULO_COSTEABLE"]
    # bloques FUTUROS: su estructura también debe estar representada (no bloquean la etapa inicial)
    fut_ok = all(r["MODULO_ESTRUCTURA_COMPLETA"] for r in rows if r["FASE"] == "FUTURO")
    if "M17" in _MUT:                                             # mutación: costeable sin mirar los módulos
        flags["costeable"] = flags["operativa"] = True
    res = {"ARQUITECTURA_ESTRUCTURA_COMPLETA": flags["estructura"] and fut_ok,
           "ARQUITECTURA_OPERATIVAMENTE_COMPLETA": flags["operativa"],
           "ARQUITECTURA_COSTEABLE": flags["operativa"] and flags["costeable"],
           "COBERTURA_ESTRUCTURAL_PCT": 100 * tot["rep"] / tot["req"], "COBERTURA_FISICA_PCT": 100 * tot["fis"] / tot["req"],
           "COBERTURA_COSTEO_BLOQUES_PCT": 100 * tot["cos"] / tot["req"],
           "MODULOS_INCOMPLETOS": ", ".join(r["MODULO_ARQ"] for r in rows if r["FASE"] == "INICIAL" and not r["MODULO_COSTEABLE"])}
    return rows, res


def comparabilidad(publicable, niveles):
    if publicable:
        return "COMPARABLE (arquitectura costeable y cobertura completa)"
    if not niveles:
        return "SIN_MONTO"
    return "MONTOS_PARCIALES_E4_NO_COMPARABLES" if "E4" in niveles else "MONTOS_PARCIALES_NO_COMPARABLES"


def resumir(filas, DR, arq=None):
    """Resumen por módulo y total. Nunca publica un total ni un costo unitario si (a) falta algún concepto o (b) la
    arquitectura no es COSTEABLE (algún bloque operativo material sin cantidad o sin precio)."""
    if arq is None:
        arq = completitud(DR["c"], filas)[1]
    costeable = arq["ARQUITECTURA_COSTEABLE"]
    mods = sorted({f["MODULO"] for f in filas})
    out = {}
    v = DR["v"]
    for m in mods + ["TOTAL"]:
        fs = [f for f in filas if m == "TOTAL" or f["MODULO"] == m]
        cost = [f for f in fs if f["COSTEA"]]
        con = [f for f in cost if f["ESTADO"] == "CON_PRECIO"]
        tot = sum(f["COSTO_CALCULADO_USD_ANIO"] for f in con)
        por_e = {e: sum(f["COSTO_CALCULADO_USD_ANIO"] for f in con if f["EVIDENCIA"] == e) for e in EVIDENCIAS}
        var = sum(f["COSTO_CALCULADO_USD_ANIO"] * f["PCT_VARIABLE"] / 100 for f in con if f["PCT_VARIABLE"] is not None)
        fij = sum(f["COSTO_CALCULADO_USD_ANIO"] * f["PCT_FIJO"] / 100 for f in con if f["PCT_FIJO"] is not None)
        sin = sum(f["COSTO_CALCULADO_USD_ANIO"] for f in con if f["PCT_VARIABLE"] is None)
        falt = [f for f in cost if f["ESTADO"] != "CON_PRECIO"]
        d = {"ESTADO_MODULO": "SIN_CONCEPTOS" if not cost else ("COMPLETO" if not falt else "INCOMPLETO"),
             "CONCEPTOS_COSTEABLES": len(cost), "CONCEPTOS_CON_PRECIO": len(con),
             "CONCEPTOS_SIN_PRECIO": sum(1 for f in cost if f["ESTADO"] in ("PENDIENTE_PRECIO", "SIN_TIPO_DE_CAMBIO")),
             "CONCEPTOS_SIN_CANTIDAD": sum(1 for f in cost if f["ESTADO"] == "PENDIENTE_CANTIDAD"),
             "CONCEPTOS_APORTANTE_PENDIENTE": sum(1 for f in cost if f["ESTADO"] == "APORTANTE_PENDIENTE"),
             **{f"OPEX_{g}_USD_ANIO": (sum(por_e[e] for e in GRUPOS_EVIDENCIA[g]) if con else None) for g in GRUPOS_EVIDENCIA},
             **{f"N_CONCEPTOS_{g}": sum(1 for f in con if f["EVIDENCIA"] in GRUPOS_EVIDENCIA[g]) for g in GRUPOS_EVIDENCIA},
             "N_CONCEPTOS_PENDIENTES": len(falt),
             "CALIDAD_MONTO": calidad_monto({f["EVIDENCIA"] for f in con}),
             "MONTO_PARCIAL_CON_PRECIO_USD_ANIO": tot if con else None,
             "MONTO_VARIABLE_USD_ANIO": var if con else None, "MONTO_FIJO_USD_ANIO": fij if con else None,
             "MONTO_SIN_CLASIFICAR_USD_ANIO": sin if con else None,
             "COBERTURA_CONCEPTOS_PCT": (100 * len(con) / len(cost)) if cost else None,
             "CONCEPTOS_INFORMATIVOS_TERCEROS": sum(1 for f in fs if f["ESTADO_DIMENSION"] == "INFORMATIVO"),
             "CONCEPTOS_INCLUIDOS_EN_OTRO": sum(1 for f in fs if f["ESTADO_DIMENSION"] == "INCLUIDO"),
             "CONCEPTOS_FUTUROS_U_OPCIONALES": sum(1 for f in fs if f["FASE"] != "OPERACION")}
        if not cost:
            d["COBERTURA_VALOR"] = "NO APLICA"
        elif not falt:
            d["COBERTURA_VALOR"] = "100"
        else:
            d["COBERTURA_VALOR"] = f"NO CALCULABLE: {len(falt)} conceptos sin magnitud"
        completo = bool(cost) and not falt and costeable
        d["COMPARABILIDAD"] = comparabilidad(completo, {f["EVIDENCIA"] for f in con})
        d["TOTAL_PRELIMINAR_USD_ANIO"] = tot if completo else None
        d["TOTAL_PRELIMINAR"] = f"{tot:.0f}" if completo else ("NO APLICA" if not cost else (
            f"NO DISPONIBLE: {len(falt)} conceptos sin costo" if falt else "NO DISPONIBLE: arquitectura no costeable")
            + ("" if costeable else f"; módulos incompletos: {arq['MODULOS_INCOMPLETOS']}"))
        kp = {"COSTO_USD_AVE": v["aves_faenadas_anio"], "COSTO_USD_KG_VIVO": v["kg_vivo_cargado_anio"],
              "COSTO_USD_KG_PRODUCTO": v["kg_producto_anio"], "COSTO_USD_DIA": DR["dias_anio"], "COSTO_USD_MES": 12}
        for k, den in kp.items():
            d[k] = (tot / den) if (completo and m == "TOTAL") else (
                f"NO DISPONIBLE (cobertura de costeo {d['COBERTURA_CONCEPTOS_PCT']:.1f} %; arquitectura "
                f"{'costeable' if costeable else 'NO costeable'})" if cost else "NO APLICA")
        if m == "TOTAL":
            d.update({k: arq[k] for k in ("ARQUITECTURA_ESTRUCTURA_COMPLETA", "ARQUITECTURA_OPERATIVAMENTE_COMPLETA",
                                          "ARQUITECTURA_COSTEABLE", "COBERTURA_ESTRUCTURAL_PCT", "COBERTURA_FISICA_PCT",
                                          "COBERTURA_COSTEO_BLOQUES_PCT", "MODULOS_INCOMPLETOS")})
            d.update(fte_universos(DR["c"], DR))
        out[m] = d
    return out


# ---------------------------------------------------------------------------------------------
# 6. CAPITAL DE TRABAJO (stock propio ≠ stock de la cadena)
# ---------------------------------------------------------------------------------------------
def cuentas_por_cobrar(ventas_anuales, dias):
    if ventas_anuales is None or dias is None:
        return None
    return ventas_anuales * dias / 365


def cuentas_por_pagar(compras_anuales, dias):
    if compras_anuales is None or dias is None:
        return None
    return compras_anuales * dias / 365


def cto(inventarios, cxc, caja, cxp):
    """Capital de trabajo operativo. Cualquier componente None → None (PENDIENTE): no se fabrica un total."""
    if any(x is None for x in (inventarios, cxc, caja, cxp)):
        return None
    return inventarios + cxc + caja - cxp


CAMPOS_CT = ["ESCENARIO", "COMPONENTE", "SUBCOMPONENTE", "CANTIDAD", "UNIDAD", "PROPIETARIO", "PROPIEDAD_EMPRESA", "UBICACION",
             "ENTRA_EN_CT",
             "PRECIO_ID", "PRECIO_USD", "VALOR_USD", "EVIDENCIA", "ESTADO", "FALTA"]


def capital_trabajo(c, DR, filas, base, opex_total=None):
    v = DR["v"]
    rows = []

    def row(comp, sub, cant, uni, prop, ubic, pid, falta="", valor_forzado=None, entra=None):
        r = base.get(pid) if pid else None
        p = precio_usd(r) if (r and r["ESTADO"] == "CON_PRECIO") else None
        prop_emp = {"empresa": "TRUE", "tercero": "FALSE"}.get(prop, "PENDIENTE")
        if prop_emp != "TRUE":                     # solo el stock PROPIEDAD de la empresa entra al CT (nunca por arquitectura)
            entra = None
        if entra is None:
            entra = "Sí" if prop_emp == "TRUE" else ("No (propiedad de tercero)" if prop_emp == "FALSE" else "PENDIENTE")
        val = valor_forzado
        if val is None and entra == "Sí" and cant is not None and p is not None:
            val = cant * p
        if entra == "Sí" and cant is not None and abs(cant) < TOL:
            val = 0.0
        est = ("NO_ENTRA" if entra.startswith("No") else "PROPIEDAD_PENDIENTE" if entra == "PENDIENTE" else
               "VALORIZADO" if val is not None else "PENDIENTE")
        if est == "PENDIENTE" and not falta:
            falta = "cantidad" if cant is None else "precio"
        rows.append({"ESCENARIO": "", "COMPONENTE": comp, "SUBCOMPONENTE": sub, "CANTIDAD": cant, "UNIDAD": uni,
                     "PROPIETARIO": prop, "PROPIEDAD_EMPRESA": prop_emp, "UBICACION": ubic, "ENTRA_EN_CT": entra, "PRECIO_ID": pid or "",
                     "PRECIO_USD": p, "VALOR_USD": val, "EVIDENCIA": r["NIVEL_EVIDENCIA"] if (r and p is not None) else "",
                     "ESTADO": est, "FALTA": falta})
    # Inventarios de alimento (14B: categoría × propietario)
    arq = DR["arq_inventario"]
    if arq is None:
        row("INVENTARIO", "alimento y materias primas", None, "t", "PENDIENTE", "—", "",
            "variante del façon no definida: propietario de las MP PENDIENTE (DEC-17-02)")
    else:
        precio_pt = {"A_compra": "ALI-A-PT", "B_facon_mp_elaborador": "ALI-B-PTE"}.get(arq)
        ids = {"alimento_terminado_granja": precio_pt, "alimento_terminado_planta": precio_pt, "maiz": "ALI-MP-MAIZ",
               "harina_soja": "ALI-MP-SOJA", "micros_aceite_otros": "ALI-MP-RESTO", "material_en_proceso": None}
        ap_al = aportes(c)["alimento"]
        for cat, x in DR["inventario_alimento"].items():
            prop = "empresa" if x["propietario"] == "empresa" else "tercero"
            if cat == "alimento_terminado_granja" and c["granjas"] != "propias" and ap_al != "EMPRESA":
                prop = "PENDIENTE" if ap_al == "PENDIENTE" else "tercero"
            cant = x["stock_propio_t"] if prop == "empresa" else x["stock_tercero_referencial_t"]
            falta = ""
            if prop == "empresa" and cat.startswith("alimento_terminado") and ids[cat] is None:
                falta = "costo de producción del alimento (MP + conversión) PENDIENTE"
            if prop == "empresa" and cat == "maiz":
                falta = "valuado a precio Rosario sobre puerto (E4), NO al costo puesto en planta (diferencial PENDIENTE)"
            row("INVENTARIO", f"alimento: {cat}", cant, "t", prop, x["ubicacion"], ids[cat], falta)
    if c["pollito"] == "incubacion":
        row("INVENTARIO", "huevo fértil en almacén", v["stock_huevos_almacen"], "huevos", "empresa", "incubadora", "INC-OP-HUEVO")
        row("INVENTARIO", "huevos en incubación (WIP, al costo del huevo como cota inferior)", v["huevos_en_proceso_wip"],
            "huevos", "empresa", "incubadora", "INC-OP-HUEVO")
    else:
        row("INVENTARIO", "pollitos BB", 0.0, "pollitos", "empresa", "—", "",
            entra="Sí", falta="se alojan al recibirse (stock ≈ 0)")
    prop_aves = "empresa" if (c["granjas"] == "propias" or aportes(c)["pollito"] == "EMPRESA") else "PENDIENTE"
    row("INVENTARIO", "aves en crianza (activo biológico)", v["inventario_aves_promedio_anual"], "aves", prop_aves,
        "granjas", "", "método de valuación PENDIENTE (DEC-17-07: costo acumulado medio)")
    ubic = "planta propia" if c["faena"] == "propia" else "faenador / frío de tercero (propiedad de la empresa)"
    for ch in ("refrigerado", "congelado"):
        row("INVENTARIO", f"producto terminado {ch}", v[f"stock_{ch}_medio_t"], "t", "empresa", ubic, "",
            "costo de producción por kg PENDIENTE")
    if c["faena"] == "propia":
        row("INVENTARIO", "subproductos", 0.0, "t", "empresa", "planta", "", entra="Sí",
            falta="retiro diario (12B, estrategia E1): stock 0")
    for sub, k in (("envases", "dias_stock_envases"), ("repuestos", "dias_stock_repuestos"),
                   ("insumos (químicos, laboratorio, combustibles)", "dias_stock_insumos")):
        row("INVENTARIO", sub, None, "USD", "empresa", "—", "", f"días de stock PENDIENTES ({k}) y compras con precio")
    inv_vals = [r for r in rows if r["COMPONENTE"] == "INVENTARIO" and r["ENTRA_EN_CT"] == "Sí"]
    inv_falt = [r["SUBCOMPONENTE"] for r in rows if r["COMPONENTE"] == "INVENTARIO" and r["ESTADO"] in ("PENDIENTE", "PROPIEDAD_PENDIENTE")]
    inv_total = None if inv_falt else sum(r["VALOR_USD"] for r in inv_vals)
    inv_parcial = sum(r["VALOR_USD"] for r in inv_vals if r["VALOR_USD"] is not None)
    # Cuentas por cobrar
    cxc = cuentas_por_cobrar(c["ventas_anuales_usd"], c["dias_cobro"])
    rows.append({**{k: "" for k in CAMPOS_CT}, "COMPONENTE": "CUENTAS_POR_COBRAR", "SUBCOMPONENTE": "ventas × días ÷ 365",
                 "VALOR_USD": cxc, "ENTRA_EN_CT": "Sí", "ESTADO": "VALORIZADO" if cxc is not None else "PENDIENTE",
                 "FALTA": "" if cxc is not None else "ventas (no se modelan en 20_opex) y/o días de cobro (DPV-039)"})
    # Cuentas por pagar por grupo de proveedor
    dp = c["dias_pago"] or {}
    cxp_tot, cxp_falt = 0.0, []
    for g in GRUPOS_CXP:
        lg = [f for f in filas if f["COSTEA"] and f["GRUPO_PROVEEDOR"] == g]
        if not lg:
            continue
        compras = None if any(f["ESTADO"] != "CON_PRECIO" for f in lg) else sum(f["COSTO_CALCULADO_USD_ANIO"] for f in lg)
        x = cuentas_por_pagar(compras, dp.get(g))
        falta = []
        if compras is None:
            falta.append(f"{sum(1 for f in lg if f['ESTADO'] != 'CON_PRECIO')} de {len(lg)} compras sin costo")
        if dp.get(g) is None:
            falta.append("días de pago")
        rows.append({**{k: "" for k in CAMPOS_CT}, "COMPONENTE": "CUENTAS_POR_PAGAR", "SUBCOMPONENTE": g,
                     "CANTIDAD": compras, "UNIDAD": "USD/año de compras", "VALOR_USD": x, "ENTRA_EN_CT": "Sí (resta)",
                     "ESTADO": "VALORIZADO" if x is not None else "PENDIENTE", "FALTA": "; ".join(falta)})
        if x is None:
            cxp_falt.append(g)
        else:
            cxp_tot += x
    cxp = None if cxp_falt else cxp_tot
    # Caja operativa (opcional)
    if c["dias_caja_operativa"] is None:
        caja, est_caja = 0.0, "NO_ASIGNADA (opcional; no obligatoria)"
    else:
        caja = None if opex_total is None else opex_total * c["dias_caja_operativa"] / 365
        est_caja = "VALORIZADO" if caja is not None else "PENDIENTE (OPEX total no disponible)"
    rows.append({**{k: "" for k in CAMPOS_CT}, "COMPONENTE": "CAJA_OPERATIVA", "SUBCOMPONENTE": "días de OPEX",
                 "CANTIDAD": c["dias_caja_operativa"], "UNIDAD": "días", "VALOR_USD": caja, "ENTRA_EN_CT": "Sí",
                 "ESTADO": est_caja})
    total = cto(inv_total, cxc, caja, cxp)
    falta = []
    if inv_total is None:
        falta.append(f"inventarios ({len(inv_falt)} ítems sin valor)")
    if cxc is None:
        falta.append("cuentas por cobrar (ventas y días)")
    if cxp is None:
        falta.append(f"cuentas por pagar ({', '.join(cxp_falt)})")
    if caja is None:
        falta.append("caja operativa")
    res = {"INVENTARIOS_USD": inv_total, "INVENTARIOS_VALORIZADOS_PARCIAL_USD": inv_parcial, "CXC_USD": cxc, "CXP_USD": cxp,
           "CAJA_USD": caja, "CAPITAL_TRABAJO_USD": total,
           "CAPITAL_TRABAJO": f"{total:.0f}" if total is not None else "PENDIENTE",
           "FALTA": "; ".join(falta)}
    rows.append({**{k: "" for k in CAMPOS_CT}, "COMPONENTE": "CAPITAL_TRABAJO_OPERATIVO",
                 "SUBCOMPONENTE": "inventarios + CxC + caja − CxP", "VALOR_USD": total, "ENTRA_EN_CT": "—",
                 "ESTADO": "VALORIZADO" if total is not None else "PENDIENTE", "FALTA": res["FALTA"]})
    return rows, res


# ---------------------------------------------------------------------------------------------
# 7. RAMP-UP (sin curva definitiva)
# ---------------------------------------------------------------------------------------------
def aplicar_utilizacion(filas, u):
    """Costo anual con utilización u: variables × u; fijos y semifijos × 1; semivariables según % variable.
    Devuelve None si u es None o si algún concepto con precio no tiene reparto fijo/variable."""
    if u is None:
        return None
    if not 0 < u <= 1:
        raise ErrorOpex("utilización en (0, 1]")
    tot = 0.0
    for f in filas:
        if not f["COSTEA"] or f["ESTADO"] != "CON_PRECIO":
            continue
        if f["PCT_VARIABLE"] is None:
            return None
        x = f["COSTO_CALCULADO_USD_ANIO"]
        tot += x * (f["PCT_VARIABLE"] / 100 * u + f["PCT_FIJO"] / 100)
    return tot


def rampup(filas, etapas=None):
    return {k: aplicar_utilizacion(filas, u) for k, u in (etapas or ETAPAS_RAMPUP).items()}


# ---------------------------------------------------------------------------------------------
# 8. CORRIDA, ESCENARIOS Y SALIDAS
# ---------------------------------------------------------------------------------------------
def correr(c, base=None):
    validar_config_opex(c)
    base = base or leer_base()
    DR = drivers_opex(c)
    filas = generar_registro(c, DR, base)
    costear(filas, base, c["fecha_base_opex"], DR["v"]["aves_faenadas_anio"])
    if c["utilizacion"] < 1:
        DR["alertas"].append(f"UTILIZACION {c['utilizacion']:.0%}: el registro informa la escala plena; el ajuste por "
                             "utilización se publica con aplicar_utilizacion() (fijos no bajan)")
    comp_rows, arq = completitud(c, filas)
    DR["completitud"], DR["arquitectura"] = comp_rows, arq
    res = resumir(filas, DR, arq)
    ct_rows, ct = capital_trabajo(c, DR, filas, base, res["TOTAL"]["TOTAL_PRELIMINAR_USD_ANIO"])
    return filas, res, DR, ct_rows, ct


def escenarios_opex():
    esc = []
    for cfg in ("C0", "C1", "C2", "C3", "CF"):
        for E in ESCALAS_REF:
            esc.append((f"{cfg}-{E}", config_opex(cfg, aves_dia=E)))
    var = [("C0-10000-FACON-MP-EMPRESA", "C0", dict(alimento_facon_mp="empresa")),
           ("C0-10000-FACON-MP-ELABORADOR", "C0", dict(alimento_facon_mp="elaborador")),
           ("C2-10000-FACON-MP-EMPRESA", "C2", dict(alimento_facon_mp="empresa")),
           ("C1-10000-GN-RED", "C1", dict(combustible_termico="gas_natural", fuente_agua="red")),
           ("C1-10000-LIMPIEZA-TERC", "C1", dict(limpieza_modalidad="tercerizada")),
           ("C1-10000-MANT-CONTRATO", "C1", dict(mantenimiento_metodo="contrato")),
           ("C1-10000-FLETE-POR-UNIDAD", "C1", dict(modelo_tarifa_flete="unidad")),
           ("C1-10000-PAGO-KG-VIVO", "C1", dict(base_pago_integrado="kg_vivo")),
           ("C1-10000-HALAL", "C1", dict(modulo_halal=True))]
    for nombre, cfg, kw in var:
        esc.append((nombre, config_opex(cfg, aves_dia=10000, **kw)))
    return esc


CAMPOS_ESC = ["ESCENARIO", "CONFIGURACION", "ESCALA_AVES_DIA", "DIAS_ANIO", "ARQUITECTURA", "ETAPA", "UTILIZACION",
              "FECHA_BASE_OPEX", "MONEDA", "MODULO", "ESTADO_MODULO", "CONCEPTOS_COSTEABLES", "CONCEPTOS_CON_PRECIO",
              "CONCEPTOS_SIN_PRECIO", "CONCEPTOS_SIN_CANTIDAD", "CONCEPTOS_APORTANTE_PENDIENTE", "OPEX_E1_E2_USD_ANIO",
              "OPEX_E3_USD_ANIO", "OPEX_E4_USD_ANIO", "OPEX_E5_USD_ANIO", "N_CONCEPTOS_E1_E2", "N_CONCEPTOS_E3",
              "N_CONCEPTOS_E4", "N_CONCEPTOS_E5", "N_CONCEPTOS_PENDIENTES", "CALIDAD_MONTO", "MONTO_PARCIAL_CON_PRECIO_USD_ANIO",
              "MONTO_VARIABLE_USD_ANIO", "MONTO_FIJO_USD_ANIO", "MONTO_SIN_CLASIFICAR_USD_ANIO", "COBERTURA_CONCEPTOS_PCT",
              "COBERTURA_VALOR", "COMPARABILIDAD", "ARQUITECTURA_ESTRUCTURA_COMPLETA",
              "ARQUITECTURA_OPERATIVAMENTE_COMPLETA", "ARQUITECTURA_COSTEABLE", "COBERTURA_ESTRUCTURAL_PCT",
              "COBERTURA_FISICA_PCT", "COBERTURA_COSTEO_BLOQUES_PCT", "MODULOS_INCOMPLETOS", "FTE_INDUSTRIAL_14A",
              "FTE_TOTAL_CONOCIDO", "FTE_TERCEROS_INCLUIDOS_EN_TARIFAS", "FTE_ADICIONAL_PENDIENTE",
              "FTE_FUTURO_NO_DIMENSIONADO", "TOTAL_PRELIMINAR", "COSTO_USD_AVE", "COSTO_USD_KG_VIVO", "COSTO_USD_KG_PRODUCTO",
              "COSTO_USD_DIA", "COSTO_USD_MES", "CONCEPTOS_INFORMATIVOS_TERCEROS", "CONCEPTOS_INCLUIDOS_EN_OTRO",
              "CONCEPTOS_FUTUROS_U_OPCIONALES", "CAPITAL_TRABAJO", "ALERTAS"]
CAMPOS_MAPA = ["ESCENARIO", "CONFIGURACION", "ESCALA_AVES_DIA", "DRIVER", "VALOR_BAJO", "VALOR", "VALOR_ALTO", "UNIDAD",
               "FUENTE", "VARIABLE_ORIGEN", "ESCENARIO_FUENTE", "TIPO", "EVIDENCIA", "USO_EN_OPEX", "OBSERVACIONES"]
CAMPOS_LAB = ["ESCENARIO", "UNIVERSO_RRHH", "PUESTO", "CLAVE", "AREA", "GRUPO", "CENTRO_COSTO", "MODALIDAD",
              "CATEGORIA_LABORAL", "COSTO_ID", "PUESTOS_TURNO", "SIMULTANEOS", "PUESTOS_EQUIVALENTES", "HEADCOUNT", "FTE",
              "HORAS_PERSONA_DIA", "HORAS_ANIO", "HORAS_CONTRATADAS_ANIO", "TURNOS", "TIPO_CONTRATACION",
              "REMUNERACION_BASE_MENSUAL_USD", "ADICIONALES_PCT", "VACACIONES_PCT", "SAC_SUELDOS_ANIO (regla)",
              "CARGAS_PCT", "ART_PCT", "BENEFICIOS_USD_MES", "EPP_UNIFORME_USD_ANIO", "CAPACITACION_USD_ANIO",
              "OTROS_USD_ANIO", "HORAS_EXTRA", "COSTO_EMPRESA_ANUAL_FTE_USD", "TARIFA_HORA_USD", "COSTO_ANUAL_USD",
              "BASE_COSTEO", "ESTADO", "FUENTE"]


def filas_costo_laboral(nombre, c, DR, base, reglas=None):
    """Una fila por puesto y modalidad de 14A (RRHH INDUSTRIAL / estructura / coordinación primaria) + una fila por
    universo de RRHH NO dimensionado (granjas, incubación, planta de alimento, reproductoras, rendering) + totales.
    Ningún salario cargado → COSTO_LABORAL_TOTAL = PENDIENTE."""
    reglas = reglas if reglas is not None else leer_reglas()
    out = []
    da = DR["dias_anio"]
    sac = reglas.get("SAC", {}).get("VALOR", "")
    cc = config_capex(c)
    for p in DR["rrhh"]["puestos"]:
        if p["grupo"] not in mr.GRUPOS:
            continue
        cat = categoria_laboral(p)
        mods = []
        if p["clave"] in INCLUIDO_SERVICIO and not (p["fte_interno"] or 0) > TOL:
            mods.append(("servicio externo por unidad", None))
        elif p["estado"] == "PENDIENTE":
            mods.append(("PENDIENTE", None))
        else:
            if (p["fte_interno"] or 0) > TOL:
                mods.append(("interno", p["fte_interno"]))
            if (p["fte_tercerizado"] or 0) > TOL:
                mods.append(("tercerizado (horas contratadas)", p["fte_tercerizado"]))
        for mod, fte in mods:
            r = {k: "" for k in CAMPOS_LAB}
            r.update(ESCENARIO=nombre, UNIVERSO_RRHH=UNIVERSO_14A.get(p["categoria"], "INDUSTRIAL_14A"), PUESTO=p["puesto"],
                     CLAVE=p["clave"], AREA=p["categoria"], GRUPO=p["grupo"], CENTRO_COSTO=centro_laboral(p), MODALIDAD=mod,
                     PUESTOS_TURNO=p["puestos_turno"], SIMULTANEOS=p["simultaneos"], TURNOS=p["cuadrillas"],
                     TIPO_CONTRATACION=p["contrato"],
                     HEADCOUNT="PENDIENTE (FACTOR_COBERTURA_NOMINA)" if mod == "interno" else "no aplica",
                     HORAS_EXTRA="NO AUTOMÁTICAS (brecha de jornada informativa; LAB-<CAT>-HEX solo si se organizan)",
                     FUENTE="14A (modelo_rrhh.calcular) + base_costos_opex.csv + reglas_laborales_opex.csv")
            if mod == "interno":
                cost, niv, falt, val = costo_empresa_fte(cat, base, reglas)
                r.update(CATEGORIA_LABORAL=cat, COSTO_ID=f"LAB-{cat}", PUESTOS_EQUIVALENTES=round(p["puestos_equivalentes"] or 0, 3),
                         FTE=round(fte, 4), HORAS_PERSONA_DIA=round(p["horas_persona_dia"] or 0, 3),
                         HORAS_ANIO=round((p["horas_persona_dia"] or 0) * da, 1),
                         REMUNERACION_BASE_MENSUAL_USD=val["SAL"], ADICIONALES_PCT=val["ADI"], VACACIONES_PCT=val["VAC"],
                         **{"SAC_SUELDOS_ANIO (regla)": sac}, CARGAS_PCT=val["CAR"], ART_PCT=val["ART"],
                         BENEFICIOS_USD_MES=val["BEN"], EPP_UNIFORME_USD_ANIO=val["EPP"], CAPACITACION_USD_ANIO=val["CAP"],
                         OTROS_USD_ANIO=val["OTR"], COSTO_EMPRESA_ANUAL_FTE_USD=cost,
                         COSTO_ANUAL_USD=None if cost is None else cost * fte, BASE_COSTEO="PROVISIONAL_POR_FTE",
                         ESTADO="COSTEADO" if cost is not None else "PENDIENTE: " + "/".join(falt) + " (DPV-148)")
            elif mod.startswith("tercerizado"):
                horas = (p["horas_contratadas_dia"] or 0) * da
                chofer = p["clave"] in ("choferes_aves", "choferes_producto")
                fl = "vivo" if p["clave"] == "choferes_aves" else "refrigerado"
                incl = chofer and mcx.flota_de(cc, fl) != "propia"
                incl_facon = c["faena"] == "facon" and p["categoria"] == "operacion_industrial"
                area = "LOG" if chofer else AREA_TERCERIZADA.get(p["clave"], "OTR")
                tar = None if (incl or incl_facon) else precio_usd(base.get(f"LAB-TER-{area}"))
                r.update(CATEGORIA_LABORAL=f"TER-{area}", COSTO_ID="" if (incl or incl_facon) else f"LAB-TER-{area}",
                         FTE=round(fte, 4), HORAS_CONTRATADAS_ANIO=round(horas, 1), TARIFA_HORA_USD=tar,
                         COSTO_ANUAL_USD=None if tar is None else tar * horas, BASE_COSTEO="HORAS_CONTRATADAS",
                         ESTADO=("INCLUIDO_EN_TARIFA_FLETE (recurso físico de tercero)" if incl else
                                 "INCLUIDO_EN_TARIFA_FACON (recurso físico de tercero)" if incl_facon else
                                 "COSTEADO" if tar is not None else "PENDIENTE (tarifa)"))
                if incl or incl_facon:
                    r["UNIVERSO_RRHH"] = "TERCERO_INCLUIDO_EN_TARIFA"
            else:
                r.update(ESTADO=("INCLUIDO_EN " + INCLUIDO_SERVICIO[p["clave"]]) if mod.startswith("servicio")
                         else "DOTACIÓN PENDIENTE (14A)", FTE="" if mod.startswith("servicio") else "PENDIENTE")
                if mod.startswith("servicio"):
                    r["UNIVERSO_RRHH"] = "TERCERO_INCLUIDO_EN_SERVICIO"
            out.append(r)
    # Universos de RRHH NO dimensionados: filas explícitas, FTE PENDIENTE (no se fabrican)
    fu = fte_universos(c, DR)
    pend = [f for f in DR.get("_filas_lab_pend", [])]
    for f in pend:
        r = {k: "" for k in CAMPOS_LAB}
        r.update(ESCENARIO=nombre, UNIVERSO_RRHH=f["UNIVERSO_RRHH"], PUESTO=f["CONCEPTO"], CLAVE=f["SUBMODULO"],
                 MODALIDAD="PENDIENTE", FTE="PENDIENTE", HEADCOUNT="PENDIENTE", CENTRO_COSTO=f["CENTRO_COSTO"],
                 ESTADO=("FUTURO: sin dimensionamiento" if f["FASE"] == "FUTURO" else
                         "PENDIENTE: 14A no dimensiona esta función (DPV-17-15)"),
                 FUENTE="sin modelo físico de dotación")
        out.append(r)
    tot = [r["COSTO_ANUAL_USD"] for r in out if not str(r["ESTADO"]).startswith(("INCLUIDO", "FUTURO"))]
    total = None if any(x in ("", None) for x in tot) else sum(tot)
    for nombre_t, fte_t, est in (
            ("FTE_INDUSTRIAL_14A (RRHH industrial + estructura + coordinación primaria; NO es FTE total de empresa integrada)",
             round(fu["FTE_INDUSTRIAL_14A"], 3), "incluye horas de terceros que pueden quedar en tarifas"),
            ("FTE_TERCEROS_INCLUIDOS_EN_TARIFAS (faenador a façon, choferes con flete tercerizado)",
             round(fu["FTE_TERCEROS_INCLUIDOS_EN_TARIFAS"], 3), "recurso físico de tercero: sin costo laboral propio"),
            ("FTE_TOTAL_CONOCIDO (empresa, dimensionado por 14A)", round(fu["FTE_TOTAL_CONOCIDO"], 3), "conocido"),
            ("FTE_ADICIONAL_PENDIENTE", fu["FTE_ADICIONAL_PENDIENTE"], "no se fabrican FTE para módulos sin modelo físico")):
        fila = {k: "" for k in CAMPOS_LAB}
        fila.update(ESCENARIO=nombre, PUESTO=nombre_t, FTE=fte_t, ESTADO=est, BASE_COSTEO="RESUMEN")
        out.append(fila)
    fila_tot = {k: "" for k in CAMPOS_LAB}
    fila_tot.update(ESCENARIO=nombre, PUESTO="COSTO_LABORAL_TOTAL", FTE="no se suma (universos pendientes)" if pend else
                    round(fu["FTE_TOTAL_CONOCIDO"], 3), COSTO_ANUAL_USD=total if (total is not None and not pend) else "PENDIENTE",
                    ESTADO="COSTEADO" if (total is not None and not pend) else
                    "PENDIENTE: salarios y cargas sin fuente (DPV-148)" + ("; universos de RRHH sin dimensionar" if pend else ""),
                    BASE_COSTEO="PROVISIONAL_POR_FTE")
    out.append(fila_tot)
    return out


def _fmt(x):
    if x is None:
        return ""
    if isinstance(x, bool):
        return "Sí" if x else "No"
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            raise ErrorOpex("NaN/inf en la salida")
        return f"{x:.6g}" if abs(x) < 1e15 else f"{x:.0f}"
    return str(x)


def escribir(ruta, filas, campos):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({k: _fmt(r.get(k)) for k in campos})


def construir_salidas(base=None):
    base = base or leer_base()
    reg, esc, mapa, lab, cts, comp = [], [], [], [], [], []
    resumen = {}
    for nombre, c in escenarios_opex():
        filas, res, DR, ct_rows, ct = correr(c, base)
        cab = {"ESCENARIO": nombre, "CONFIGURACION": c["nombre"], "ESCALA_AVES_DIA": c["aves_dia"]}
        for f in filas:
            reg.append({**f, **cab})
        arq = mcx.etiqueta_arquitectura(config_capex(c)) + (f"|facon_mp={c['alimento_facon_mp']}" if c["alimento_facon_mp"] else "")
        for m, d in res.items():
            esc.append({**cab, "DIAS_ANIO": DR["dias_anio"], "ARQUITECTURA": arq, "ETAPA": c["etapa"],
                        "UTILIZACION": c["utilizacion"], "FECHA_BASE_OPEX": c["fecha_base_opex"], "MONEDA": MONEDA,
                        "MODULO": m, **d, "CAPITAL_TRABAJO": ct["CAPITAL_TRABAJO"] if m == "TOTAL" else "",
                        "ALERTAS": " | ".join(DR["alertas"]) if m == "TOTAL" else ""})
        for p in DR["proc"].values():
            mapa.append({**cab, **p})
        lab += filas_costo_laboral(nombre, c, DR, base)
        for r in ct_rows:
            cts.append({**r, "ESCENARIO": nombre})
        for r in DR["completitud"]:
            comp.append({**cab, **r})
        resumen[nombre] = (res, ct, DR)
    escribir(SALIDA_REG, reg, CAMPOS_REG)
    escribir(SALIDA_ESC, esc, CAMPOS_ESC)
    escribir(SALIDA_MAPA, mapa, CAMPOS_MAPA)
    escribir(SALIDA_LAB, lab, CAMPOS_LAB)
    escribir(SALIDA_CT, cts, CAMPOS_CT)
    escribir(SALIDA_MATRIZ, matriz_validacion(resumen), CAMPOS_MATRIZ)
    escribir(SALIDA_COMP, comp, CAMPOS_COMP)
    return {"registro": len(reg), "escenarios": len(esc), "mapa": len(mapa), "laboral": len(lab), "ct": len(cts),
            "completitud": len(comp)}


# ---------------------------------------------------------------------------------------------
# 9. MATRIZ DE VALIDACIÓN (agrupada; magnitudes físicas de C1/C3 a 10.000 como orden de magnitud)
# ---------------------------------------------------------------------------------------------
CAMPOS_MATRIZ = ["ITEM", "DRIVER", "UNIDAD", "MAGNITUD_FISICA_REFERENCIA", "VALOR_NECESARIO", "ACTOR", "ESTADO",
                 "PRIORIDAD", "IMPACTO", "CONCEPTOS", "DPV", "OBSERVACIONES"]
MATRIZ = [
    ("alimento", "alimento_t_anio", "t/año", "C1-10000", "USD/t de alimento terminado por fase (puesto en granja y en fábrica), con flete y descarga separados",
     "Fábricas de alimento que venden a terceros (DPV-050)", "ALTA", "MUY ALTO: probable mayor costo del OPEX", "ALI-A-PT, ALI-A-DES", "DPV-050, DPV-17-01, DPV-17-17"),
    ("façon de alimento", "alimento_t_anio", "t/año", "C0-10000", "Tarifa de elaboración USD/t y precio integral con MP del elaborador; quién compra MP y mantiene inventario; mermas",
     "Fábricas con disposición a façon (DPV-155)", "ALTA", "ALTO", "ALI-B-SRV, ALI-B-PTE, ALI-B-ALM, ALI-MERMA", "DPV-155"),
    ("granos y materias primas", "mp_maiz_t_anio", "t/año", "C3-10000", "Maíz y harina de soja puestos en planta (precio + flete), núcleo, aceite, aminoácidos; contratos",
     "Acopios, corredores, Bolsa (lectura primaria de pizarra), proveedores de núcleo", "ALTA", "ALTO en C3 y façon B1", "ALI-MP-*", "DPV-157, DPV-17-02"),
    ("pollito BB", "pollitos_a_recibir_anio", "pollitos/año", "C1-10000", "USD/pollito (vacunas incluidas o no, lugar de entrega, flete) — leer CAPIA en original",
     "Incubadoras que venden a terceros; CAPIA", "ALTA", "ALTO", "POL-COMPRA, LOG-POL-*", "DPV-006, DPV-17-03, DPV-17-17"),
    ("huevo fértil", "huevos_recibidos_anio", "huevos/año", "C3-10000", "USD/huevo incubable puesto en incubadora; disponibilidad",
     "Productores de huevo fértil / reproductoras", "MEDIA", "ALTO en C3/CF", "INC-OP-HUEVO", "DPV-17-03"),
    ("salarios y cargas", "fte_industrial_14a", "FTE", "C1-10000", "Salario de convenio por categoría, cargas, ART, adicionales, beneficios, EPP; convenio aplicable",
     "Convenio colectivo (lectura primaria), estudio contable laboral", "ALTA", "MUY ALTO", "LAB-*", "DPV-148, DPV-146"),
    ("energía eléctrica", "kwh_anio", "kWh/año", "C1-10000", "Tarifa industrial (cargo variable USD/kWh, cargo por potencia USD/kW·mes, cargo fijo) de la distribuidora del sitio",
     "Cuadro tarifario oficial de la distribuidora / ente regulador provincial", "ALTA", "ALTO", "UT-ELE-*", "DPV-052, DPV-095, DPV-17-05"),
    ("gas / combustible térmico", "energia_termica_kwh_t_anio", "kWh_t/año", "C1-10000", "Combustible elegido y su precio (gas natural USD/m³, GLP USD/kg, biomasa USD/kg)",
     "Distribuidora de gas / proveedores de GLP y biomasa", "MEDIA", "MEDIO", "UT-TER-*", "DPV-052, DEC-045"),
    ("agua", "agua_m3_anio", "m³/año", "C1-10000", "Tarifa de red o canon de agua subterránea; químicos de potabilización",
     "Prestadora / autoridad del agua provincial", "MEDIA", "BAJO-MEDIO", "UT-AGUA-*", "DPV-053"),
    ("tratamiento de efluentes", "efluente_m3_anio", "m³/año", "C1-10000", "Químicos por m³, análisis de vuelco, canon, lodos (t y USD/t)",
     "Proveedores de tratamiento; autoridad de vuelco", "MEDIA", "MEDIO", "EF-*", "DPV-072, DEC-043"),
    ("químicos de limpieza", "aves_faenadas_anio", "aves/año", "C1-10000", "USD por ave (o por m²) de químicos de limpieza y sanitización",
     "Proveedores de químicos para industria cárnica", "MEDIA", "MEDIO", "FAE-QUIM, INC-OP-LIM, PP-LIMP", "DPV-17-08"),
    ("packaging", "kg_producto_anio", "kg producto/año", "C1-10000", "Precio por kg de producto de bolsas, bandejas, film, cajas, etiquetas, pallets según mix",
     "Proveedores de envases", "MEDIA", "ALTO", "EMP-*", "DPV-17-09"),
    ("mantenimiento", "activos BOQ 16", "activo-año", "C1-10000", "Método (contrato, por activo, horas) y precios; repuestos críticos; refrigerante",
     "Proveedores de equipos (con RFQ) y de servicios técnicos", "MEDIA", "MEDIO-ALTO", "MAN-*", "DEC-17-06, DPV-17-10"),
    ("faena a façon", "aves_faenadas_anio", "aves/año", "C0-10000", "Tarifa USD/ave y alcance (empaque, frío, subproductos, rendimiento garantizado)",
     "Frigoríficos con capacidad ociosa (DPV-006, DPV-016)", "ALTA", "MUY ALTO en C0", "FAE-FACON*", "DPV-006, DPV-17-07"),
    ("logística", "vivo_km_anio / refrigerado_km_anio", "km/año", "C1-10000", "Tarifas tercerizadas (viaje / km / t) por flujo; costos de flota propia (consumo L/km, mantenimiento/km, seguros)",
     "Transportistas de aves vivas, refrigerado y granel", "ALTA", "ALTO", "LOG-*", "DPV-042, DPV-054, DPV-084"),
    ("integración y granjas", "aves_cargadas_anio / kg_vivo_cargado_anio", "aves/año", "C1-10000", "Contrato de integración (base de pago, ajustes, aportes de cada parte), captura, cama, gas",
     "Productores integrados, integradoras", "ALTA", "MUY ALTO en C0–C2", "PP-*", "DPV-17-04, DPV-054"),
    ("seguros", "pólizas", "póliza-año", "C1-10000", "Prima anual por póliza (planta, incendio, RC, flota, mercadería, interrupción)",
     "Brokers / aseguradoras", "BAJA", "MEDIO", "SEG-*", "DPV-17-11"),
    ("análisis y laboratorio", "plan de muestreo", "análisis/año", "C1-10000", "Plan de autocontrol y precio por análisis (microbiología, agua, alimento, vuelco)",
     "Laboratorios acreditados", "MEDIA", "BAJO-MEDIO", "CAL-ANA-*, ALI-C-ANA, EF-ANA", "DPV-17-12"),
    ("certificaciones y SENASA", "establecimiento", "año", "C1-10000", "Tasas/aranceles SENASA, certificaciones, auditorías; halal (opcional)",
     "SENASA (lectura primaria de aranceles), certificadoras", "MEDIA", "MEDIO", "CAL-SENASA, CAL-CERT, CAL-AUD, HAL-*", "DPV-101, DPV-17-13"),
    ("capital de trabajo", "días", "días", "todas", "Días de cobro por canal, días de pago por proveedor, días de stock de envases, repuestos e insumos, método de valuación del activo biológico",
     "Clientes potenciales (DPV-039), proveedores, contador", "ALTA", "MUY ALTO para la caja", "CT", "DPV-039, DPV-17-14"),
]


def matriz_validacion(resumen):
    out = []
    for item, drv, uni, esc, val, actor, prio, imp, conc, dpv in MATRIZ:
        mag = ""
        if esc in resumen and drv in resumen[esc][2]["v"]:
            x = resumen[esc][2]["v"][drv]
            mag = "" if x is None else f"{x:,.0f} {uni} ({esc})".replace(",", ".")
        out.append({"ITEM": item, "DRIVER": drv, "UNIDAD": uni, "MAGNITUD_FISICA_REFERENCIA": mag, "VALOR_NECESARIO": val,
                    "ACTOR": actor, "ESTADO": "PENDIENTE", "PRIORIDAD": prio, "IMPACTO": imp, "CONCEPTOS": conc,
                    "DPV": dpv, "OBSERVACIONES": "Magnitud física = orden de magnitud, no compromiso de compra"})
    return out


# ---------------------------------------------------------------------------------------------
# 10. TESTS
# ---------------------------------------------------------------------------------------------
def _base_sintetica(precio=10.0, nivel="E3", pct_var=None):
    """Copia de la base con TODOS los precios llenos (solo para probar la matemática)."""
    base = copy.deepcopy(leer_base())
    for r in base.values():
        if r["ESTADO"] in ("REFERENCIA", "DESCARTADO"):
            continue
        r.update(PRECIO_UNITARIO=str(5.0 if r["UNIDAD"] == "%" else precio), MONEDA_ORIGINAL="USD",
                 TC_MONEDA_POR_USD="1", NIVEL_EVIDENCIA=nivel, LECTURA_PRIMARIA="Sí", FUENTE="TEST", ESTADO="CON_PRECIO",
                 PRECIO_USD_EQUIVALENTE="", FECHA_PRECIO="2026-10-01", FLETE_INCLUIDO="No", IVA_TRATAMIENTO="sin_iva")
        if r["NATURALEZA"] == "semivariable" and pct_var is not None:
            r.update(PCT_VARIABLE=str(pct_var), ORIGEN_PCT_VARIABLE="SUP-TEST")
    return base


def _csv(ruta):
    with open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _lanza(fn, *a, **k):
    try:
        fn(*a, **k)
    except (ErrorOpex, mcx.ErrorCapex):
        return True
    return False


def _cerca(a, b, rel=1e-4):
    return a is not None and b is not None and abs(a - b) <= rel * max(1.0, abs(b))


def ejecutar_tests(verbose=True):
    res = []

    def chk(i, desc, ok):
        res.append((i, desc, bool(ok)))
        if verbose:
            print(f"  [{'OK ' if ok else 'FALLA'}] {i} {desc}")

    base = leer_base()
    sint = _base_sintetica()
    run = {}
    for cfg in ("C0", "C1", "C2", "C3", "CF"):
        for E in (2500, 10000):
            run[(cfg, E)] = correr(config_opex(cfg, aves_dia=E), base)
    f1, r1, D1, _, ct1 = run[("C1", 10000)]
    f3, r3, D3, _, ct3 = run[("C3", 10000)]
    f0, r0, D0, _, ct0 = run[("C0", 10000)]
    # ---------------- DRIVERS ----------------
    c03 = mcx._csv_03()
    ok = all(abs(run[(cf, E)][2]["v"]["alimento_t_anio"] - float(c03[str(E)]["alimento_t_anio"])) <= 0.5
             and abs(run[(cf, E)][2]["v"]["pollitos_alojados_anio"] - float(c03[str(E)]["pollitos_alojados_anio"])) <= 0.5
             for cf in ("C0", "C3") for E in (2500, 10000))
    chk("D01", "Alimento (t/año) y pollitos alojados reproducen el CSV de 03 (redondeado a unidades; perfil y desempeño medios, 5 d)", ok)
    u14 = {}
    for r in _csv("14_alimento_balanceado/escenarios_upstream.csv"):
        if r["dias_faena_semana"] == "5" and r["nivel_produccion"] == "medio" and r["bloque"] in ("4_alimento", "1_pollitos") \
                and r["valor"] not in ("", "None"):
            u14.setdefault((r["bloque"], r["escala_aves_faenadas_dia"], r["variable"]), float(r["valor"]))
    ok = all(_cerca(run[(cf, E)][2]["v"]["alimento_t_anio"], u14[("4_alimento", str(E), "alimento_t_anio")])
             and _cerca(run[(cf, E)][2]["v"]["pollitos_a_recibir_anio"], u14[("1_pollitos", str(E), "pollitos_a_recibir_anio")])
             for cf in ("C1", "C3") for E in (2500, 10000))
    chk("D02", "Alimento y pollitos a recibir reproducen el CSV de 14B", ok)
    t_alim_regs = [f["CANTIDAD"] for f in f1 if f["COSTO_ID"] == "ALI-A-PT"]
    chk("D03", "El concepto ALI-A-PT usa exactamente la t/año de 14B (sin FCR propio de OPEX)",
        len(t_alim_regs) == 1 and _cerca(t_alim_regs[0], D1["v"]["alimento_t_anio"]))
    # 14A
    rr = _csv("18_recursos_humanos/escenarios_rrhh.csv")
    ok_rr = True
    for E in (2500, 10000):
        c = config_opex("C1", aves_dia=E, laboratorio_propio=False, rrhh_cap_camion_producto_t=None, rrhh_dist_producto_km=None)
        R = mr.calcular(entradas_rrhh(c))
        fila = [r for r in rr if r["aves_dia"] == str(E) and r["horas_netas"] == "8.0" and r["turnos"] == "extendido"
                and r["automatizacion"] == "semiautomatico" and r["config"] == "B" and r["limpieza"] == "propia"
                and r["mantenimiento"] == "propio" and r["flota_propia"] == "0" and r["productividad"] == "media"
                and r["planta_propia"] == "1"]
        ok_rr &= len(fila) == 1 and abs(R["fte_total"] - float(fila[0]["fte_total"])) < 0.01
    chk("D04", "RRHH: FTE de OPEX reproduce el CSV de 14A con las mismas entradas (mapeo sin recálculo)", ok_rr)
    lab_fte = sum(f["CANTIDAD"] for f in f1 if f["MODULO"] == "COSTO_LABORAL" and f["COSTO_ID"].startswith("LAB-")
                  and not f["COSTO_ID"].startswith("LAB-TER") and f["UNIDAD"] == "FTE-año" and f["CANTIDAD"] is not None)
    chk("D05", "FTE internos del registro = FTE internos de 14A (ningún puesto se pierde ni se duplica)",
        _cerca(lab_fte, D1["rrhh"]["fte_internos"]))
    c09 = mcx._csv_09c()
    ok = all(_cerca(run[("C1", E)][2]["v"]["kwh_anio"], c09[(str(E), "medio", "kwh_total_anio")])
             and _cerca(run[("C1", E)][2]["v"]["agua_m3_anio"], c09[(str(E), "medio", "agua_captada_m3_dia")] * 250)
             for E in (2500, 10000))
    chk("D06", "Utilities: kWh/año y agua (m³/año) de C1 reproducen el CSV de 09C (nivel medio)", ok)
    k12 = {}
    for r in _csv("13_logistica/escenarios_logistica.csv"):
        if r["bloque"] == "kpi_resumen":
            k12[(r["escala_aves_dia"], r["variable"])] = r["valor"]
        if r["bloque"] == "insumos_alimento" and "dist_fabrica_km=75" in r["parametros"]:
            k12[(r["escala_aves_dia"], "alim_" + r["variable"])] = r["valor"]
    ok = all(_cerca(run[("C1", E)][2]["v"]["vivo_viajes_anio"], float(k12[(str(E), "vivo_viajes_dia")]) * 250)
             and _cerca(run[("C1", E)][2]["v"]["vivo_km_anio"],
                        float(k12[(str(E), "vivo_km_por_ave")]) * E * 250, rel=1e-3)
             and _cerca(run[("C1", E)][2]["v"]["alimento_km_anio"] / (run[("C1", E)][2]["v"]["alimento_t_anio"]
                                                                       / run[("C1", E)][2]["v"]["alimento_t_semana_plena"]),
                        float(k12[(str(E), "alim_alimento_km_semana")]))
             for E in (2500, 10000))
    chk("D07", "Logística: viajes y km de aves vivas y km semanales de alimento reproducen el CSV de 12B", ok)
    ok = all(_cerca(run[(cf, 10000)][2]["v"]["vehiculos_VIV"] or -1,
                    run[(cf, 10000)][2]["capex_D"]["flota"]["vivo"]["unidades"]) for cf in ("C2", "C3"))
    chk("D08", "Vehículos de flota propia = los del CAPEX (no se redimensiona la flota)", ok)
    tipos = {p["TIPO"] for (_, _, DR, _, _) in run.values() for p in DR["proc"].values()}
    sin_fuente = [p for (_, _, DR, _, _) in run.values() for p in DR["proc"].values() if not p["FUENTE"]]
    chk("D09", "Todo driver tiene tipo de procedencia válido y fuente; nunca INTERPOLADO", tipos <= set(TIPOS_DRIVER)
        and not sin_fuente)
    deriv = [p for (_, _, DR, _, _) in run.values() for p in DR["proc"].values()
             if p["TIPO"] == "DERIVADO_OPEX" and not p["VARIABLE_ORIGEN"]]
    iguales = all(_cerca(f["CANTIDAD"], DR["v"][f["DRIVER"]]) for (fl, _, DR, _, _) in run.values() for f in fl
                  if f["DRIVER"] in DR["v"] and f["CANTIDAD"] is not None and DR["v"][f["DRIVER"]] is not None
                  and f["ESTADO_DIMENSION"] == "DIMENSIONADO")
    chk("D10", "Ningún driver se recalcula en silencio: los DERIVADO_OPEX declaran su operación y toda cantidad del "
        "registro que cita un driver es igual a su valor registrado", not deriv and iguales)
    # ---------------- COSTOS ----------------
    chk("C01", "Faltante ≠ cero: ningún concepto sin precio o sin cantidad tiene costo", all(
        f["COSTO_CALCULADO_USD_ANIO"] is None for (fl, *_r) in run.values() for f in fl if f["ESTADO"] != "CON_PRECIO"))
    chk("C01b", "Todo concepto CON_PRECIO tiene precio y su evidencia es la de la base (nunca un E5 fabricado)", all(
        f["PRECIO_USD"] is not None and (f["COSTO_ID"] not in base or f["EVIDENCIA"] == base[f["COSTO_ID"]]["NIVEL_EVIDENCIA"])
        for (fl, *_r) in run.values() for f in fl if f["ESTADO"] == "CON_PRECIO"))
    chk("C02", "Ningún costo negativo", all((f["COSTO_CALCULADO_USD_ANIO"] or 0) >= 0 for (fl, *_r) in run.values() for f in fl))
    chk("C03", "Base: precio negativo o vacío con nivel E1–E5 es rechazado", _lanza(validar_base, [dict(
        next(iter(base.values())), ID_COSTO="X", PRECIO_UNITARIO="-1", NIVEL_EVIDENCIA="E4", FUENTE="x")]) and _lanza(
        validar_base, [dict(next(iter(base.values())), ID_COSTO="Y", PRECIO_UNITARIO="", NIVEL_EVIDENCIA="E4")]))
    fs, rs, Ds, _, _ = correr(config_opex("C1", aves_dia=10000), sint)
    tot = sum(f["COSTO_CALCULADO_USD_ANIO"] for f in fs if f["COSTEA"] and f["ESTADO"] == "CON_PRECIO")
    suma_mod = sum(d["MONTO_PARCIAL_CON_PRECIO_USD_ANIO"] or 0 for m, d in rs.items() if m != "TOTAL")
    chk("C04", "Total = suma válida: TOTAL = Σ módulos = Σ conceptos con precio (base sintética)",
        _cerca(rs["TOTAL"]["MONTO_PARCIAL_CON_PRECIO_USD_ANIO"], tot) and _cerca(suma_mod, tot))
    ids_cost = [(f["COSTO_ID"], f["FLUJO"], f["SUBMODULO"]) for f in f1 if f["COSTEA"] and f["COSTO_ID"]]
    clave = lambda f: (f["COSTO_ID"], f["FLUJO"], f["SUBMODULO"], f["APORTANTE"], f["AMBITO_GRANJA"])  # noqa: E731
    chk("C05", "Sin doble conteo: cada (COSTO_ID, flujo, puesto, aportante, ámbito propia/integrada) aparece una sola vez "
        "como costo en un escenario", all(len(ids_cost) == len(set(ids_cost)) for _ in [0]) and all(
            len([clave(f) for f in fl if f["COSTEA"] and f["COSTO_ID"]]) ==
            len({clave(f) for f in fl if f["COSTEA"] and f["COSTO_ID"]}) for (fl, *_r) in run.values()))
    kwh_cost = [f for f in fs if f["COSTO_ID"] == "UT-ELE-KWH" and f["COSTEA"]]
    frio_cost = [f for f in fs if f["CENTRO_COSTO"] == "frio" and f["COSTEA"] and f["UNIDAD"] == "kWh"]
    chk("C06", "Energía de frío no se duplica: un solo UT-ELE-KWH y las energías de frío son INCLUIDO (sin costo)",
        len(kwh_cost) == 1 and not frio_cost and all(f["COSTO_CALCULADO_USD_ANIO"] is None for f in fs
                                                     if f["CENTRO_COSTO"] == "frio" and f["UNIDAD"] == "kWh"))
    limp = [f for f in fs if f["MODULO"] == "FAENA" and f["SUBMODULO"] == "limpieza" and f["UNIDAD"] in ("m³", "kWh", "kWh_t")]
    chk("C07", "Limpieza no duplica agua ni energía: esos conceptos están INCLUIDOS en utilities (sin costo)",
        limp and all(not f["COSTEA"] and f["INCLUIDO_EN"] for f in limp))
    fl_t, _, Dt, _, _ = correr(config_opex("C1", aves_dia=10000, limpieza_modalidad="tercerizada"), sint)
    san_t = [f for f in fl_t if f["SUBMODULO"] == "limpieza_sanitizacion"]
    san_p = [f for f in fs if f["SUBMODULO"] == "limpieza_sanitizacion"]
    chk("C08", "Tercerizar la sanitización reemplaza su costo interno (sin FTE internos) y conserva la función "
        "(horas contratadas > 0, costeadas con tarifa horaria)",
        any(f["COSTO_ID"].startswith("LAB-CONV") and f["CANTIDAD"] for f in san_p) and
        not any(f["COSTO_ID"].startswith("LAB-CONV") for f in san_t) and
        any(f["COSTO_ID"] == "LAB-TER-LIMP" and f["CANTIDAD"] > 0 and f["ESTADO"] == "CON_PRECIO" for f in san_t))
    chof = [f for f in f1 if f["SUBMODULO"] == "choferes_aves"]
    chk("C09", "Flota tercerizada: las horas de choferes de 14A quedan visibles pero INCLUIDAS en el flete (no se cobran dos veces)",
        chof and all(f["ESTADO_DIMENSION"] == "INCLUIDO" and not f["COSTEA"] for f in chof))
    chk("C10", "Los conceptos INCLUIDOS remiten a otro concepto existente o a 14A", all(
        f["INCLUIDO_EN"] for (fl, *_r) in run.values() for f in fl if f["ESTADO_DIMENSION"] == "INCLUIDO"))
    # ---------------- ARQUITECTURAS ----------------
    ids1 = {f["COSTO_ID"] for f in f1 if f["COSTEA"]}
    ids3 = {f["COSTO_ID"] for f in f3 if f["COSTEA"]}
    chk("A01", "Compra de alimento no carga costos internos de fábrica (ALI-C-*, ALI-MP-*, ALI-MERMA)",
        not any(i.startswith(("ALI-C-", "ALI-MP-", "ALI-MERMA", "MAN-ALI")) for i in ids1))
    chk("A02", "Planta propia no carga simultáneamente el precio completo del alimento terminado",
        "ALI-A-PT" not in ids3 and "ALI-B-PTE" not in ids3 and "ALI-MP-MAIZ" in ids3)
    chk("A03", "Pollito comprado no carga incubación propia; incubación no carga pollito comprado",
        not any(i.startswith("INC-") for i in ids1) and "POL-COMPRA" not in ids3 and "INC-OP-HUEVO" in ids3)
    ids0 = {f["COSTO_ID"] for f in f0 if f["COSTEA"]}
    chk("A04", "Faena a façon no carga OPEX de planta propia (utilities, efluentes, químicos, subproductos, mantenimiento de planta)",
        "FAE-FACON" in ids0 and not any(i.startswith(("UT-ELE", "UT-AGUA", "UT-TER", "EF-", "FAE-QUIM", "SUB-RET", "MAN-PROC"))
                                        for i in ids0))
    fac = [f for f in f0 if f["MODULO"] == "COSTO_LABORAL" and f["SUBMODULO"] in ("colgado", "evisceracion", "trozado", "empaque")]
    chk("A04b", "Façon: las horas del personal del faenador (14A) quedan visibles pero INCLUIDAS en FAE-FACON (sin LAB-TER)",
        fac and all(f["ESTADO_DIMENSION"] == "INCLUIDO" and f["INCLUIDO_EN"] == "FAE-FACON" and (f["CANTIDAD"] or 0) > 0
                    for f in fac))
    gra1 = [f for f in f1 if f["COSTO_ID"] in ("PP-ENE", "PP-AGUA")]
    chk("A05", "Granjas integradas no cargan nómina ni energía de granja propia (aporte del integrado = INFORMATIVO)",
        gra1 and all(not f["COSTEA"] for f in gra1) and not any(f["SUBMODULO"] == "personal_granja" for f in f1))
    chk("A06", "Flota tercerizada no carga mantenimiento, combustible ni patentes propios",
        not any(i.startswith(("LOG-COMB", "SEG-FLOTA")) or re.match(r"LOG-\w+-(MANT|NEUM|PAT)$", i) for i in ids1))
    chk("A07", "Flota propia (C3) carga mantenimiento y patentes del flujo y no carga flete tercerizado",
        "LOG-VIV-MANT" in ids3 and "LOG-VIV-PAT" in ids3 and not any(i.startswith("LOG-") and "-TER-" in i for i in ids3))
    cf = run[("CF", 10000)][0]
    chk("A08", "Reproductoras y rendering (CF) quedan FUTURO: no cuentan como costo", all(
        not f["COSTEA"] for f in cf if f["COSTO_ID"].startswith(("REP-", "SUB-REN"))) and any(
        f["COSTO_ID"].startswith("REP-") for f in cf))
    fh, rh, *_ = correr(config_opex("C1", aves_dia=10000, modulo_halal=True), base)
    chk("A09", "Halal es módulo opcional: sin costos asignados y ausente si no se activa",
        all(f["COSTO_CALCULADO_USD_ANIO"] is None for f in fh if f["MODULO"] == "HALAL") and
        any(f["MODULO"] == "HALAL" for f in fh) and not any(f["MODULO"] == "HALAL" for f in f1))
    fm, *_ = correr(config_opex("C1", aves_dia=10000, mantenimiento_metodo="pct_capex"), base)
    fa_, *_ = correr(config_opex("C1", aves_dia=10000, mantenimiento_metodo="por_activo"), base)
    chk("A10", "Mantenimiento: un solo método por corrida; % CAPEX sin CAPEX con precio → BASE_SIN_PRECIO (no 0)",
        all(f["COSTO_ID"].endswith("-PCT") for f in fm if f["MODULO"] == "MANTENIMIENTO" and f["COSTEA"]) and
        not any(f["COSTO_ID"].endswith("-PCT") for f in fa_) and all(
            f["ESTADO"] == "PENDIENTE_CANTIDAD" for f in fm if f["COSTO_ID"].endswith("-PCT")))
    chk("A11", "Tarifa de flete: un modelo por flujo (no se mezclan viaje/km/unidad/contrato)",
        _lanza(validar_config_opex, config_opex("C1", modelo_tarifa_flete="peso")) and all(
            len({f["COSTO_ID"] for f in fl if f["FLUJO"] == fn and "-TER-" in f["COSTO_ID"]}) <= 1
            for (fl, *_r) in run.values() for fn in {f["FLUJO"] for f in fl}))
    chk("A12", "Combinaciones inválidas se rechazan (peso ≠ 2,9; façon sin variante válida; alimento propio con aporte del integrado)",
        _lanza(validar_config_opex, config_opex("C1", peso_kg=3.1)) and
        _lanza(validar_config_opex, config_opex("C1", alimento_facon_mp="empresa")) and
        _lanza(validar_config_opex, config_opex("C3", granjas="mixto", fraccion_granjas_propias=0.5,
                                                aportes_integracion={"alimento": "PRODUCTOR_INTEGRADO"})))
    # ---------------- CAPITAL DE TRABAJO ----------------
    inv1 = {r["SUBCOMPONENTE"]: r for r in run[("C1", 10000)][3]}
    chk("K01", "Stock propio sí: alimento en silos de granja (compra) entra al CT",
        inv1["alimento: alimento_terminado_granja"]["ENTRA_EN_CT"] == "Sí")
    chk("K02", "Stock ajeno no: el stock de la fábrica proveedora (compra) NO entra al CT",
        inv1["alimento: maiz"]["ENTRA_EN_CT"].startswith("No") and inv1["alimento: alimento_terminado_planta"]["ENTRA_EN_CT"].startswith("No"))
    ce = {r["SUBCOMPONENTE"]: r for r in correr(config_opex("C0", aves_dia=10000, alimento_facon_mp="empresa"), base)[3]}
    cl = {r["SUBCOMPONENTE"]: r for r in correr(config_opex("C0", aves_dia=10000, alimento_facon_mp="elaborador"), base)[3]}
    chk("K03", "Façon: MP en el elaborador entran al CT solo si son propiedad de la empresa (B1 sí, B2 no)",
        ce["alimento: maiz"]["ENTRA_EN_CT"] == "Sí" and cl["alimento: maiz"]["ENTRA_EN_CT"].startswith("No"))
    chk("K04", "Más días de cobro aumentan el CT; más días de pago lo reducen",
        cto(100, cuentas_por_cobrar(1000, 60), 0, 10) > cto(100, cuentas_por_cobrar(1000, 30), 0, 10) and
        cto(100, 50, 0, cuentas_por_pagar(1000, 60)) < cto(100, 50, 0, cuentas_por_pagar(1000, 30)))
    chk("K05", "Faltantes impiden un total definitivo: CAPITAL_TRABAJO = PENDIENTE con desglose", all(
        x[4]["CAPITAL_TRABAJO"] == "PENDIENTE" and x[4]["FALTA"] for x in run.values()) and cto(1, None, 0, 1) is None)
    chk("K06", "El CT de C3 valoriza el maíz propio con E4 pero no publica total (otros ítems pendientes)",
        ct3["INVENTARIOS_VALORIZADOS_PARCIAL_USD"] > 0 and ct3["CAPITAL_TRABAJO_USD"] is None)
    chk("K07", "Variante de façon sin definir → propiedad de MP PENDIENTE (no se asume)",
        any(r["ESTADO"] == "PROPIEDAD_PENDIENTE" for r in run[("C0", 10000)][3]))
    chk("K08", "Inventario de alimento: stock propio + stock en tercero = stock de la cadena por categoría (14B); "
        "el CT solo valoriza el propio", all(
            abs((x["stock_propio_t"] or 0) + (x["stock_tercero_referencial_t"] or 0) - x["stock_cadena_t"]) < 1e-6
            for (_, _, DR, _, _) in run.values() if DR.get("inventario_alimento")
            for x in DR["inventario_alimento"].values() if x["stock_cadena_t"] is not None))
    # ---------------- EVIDENCIA ----------------
    chk("E01", "E4 no aparece como costo validado: OPEX_E1_E2 = 0 y CALIDAD = REFERENCIAS_DEBILES_E4 donde solo hay E4",
        all(d["OPEX_E1_E2_USD_ANIO"] in (None, 0) for x in run.values() for d in x[1].values()) and
        r1["TOTAL"]["CALIDAD_MONTO"] == "MONTO_CON_REFERENCIAS_DEBILES_E4")
    chk("E02", "Cobertura por conceptos ≠ cobertura por valor (la de valor es NO CALCULABLE con faltantes)", all(
        "NO CALCULABLE" in x[1]["TOTAL"]["COBERTURA_VALOR"] and x[1]["TOTAL"]["COBERTURA_CONCEPTOS_PCT"] < 100
        for x in run.values()))
    chk("E03", "Sin total ni costo unitario con cobertura incompleta", all(
        x[1]["TOTAL"]["TOTAL_PRELIMINAR_USD_ANIO"] is None and str(x[1]["TOTAL"]["COSTO_USD_AVE"]).startswith("NO DISPONIBLE")
        for x in run.values()))
    fs_ok = [f for f in fs if not f["COSTEA"] or f["ESTADO"] == "CON_PRECIO"]
    arq_forz = dict(Ds["arquitectura"], ARQUITECTURA_COSTEABLE=True, MODULOS_INCOMPLETOS="")
    rok = resumir(fs_ok, Ds, arq_forz)["TOTAL"]
    chk("E04", "Aritmética del total: con conceptos completos y arquitectura COSTEABLE (forzada en el test) hay total y "
        "costo por ave = total ÷ aves",
        rok["TOTAL_PRELIMINAR_USD_ANIO"] is not None and _cerca(rok["COSTO_USD_AVE"],
                                                               rok["TOTAL_PRELIMINAR_USD_ANIO"] / Ds["v"]["aves_faenadas_anio"]))
    chk("E05", "Base: precio en ARS sin TC rechazado; E1 sin cotización rechazado; E3 sin lectura primaria rechazado",
        _lanza(validar_base, [dict(base["ALI-MP-MAIZ"], TC_MONEDA_POR_USD="", PRECIO_USD_EQUIVALENTE="")]) and
        _lanza(validar_base, [dict(base["ALI-MP-MAIZ"], NIVEL_EVIDENCIA="E1", LECTURA_PRIMARIA="Sí")]) and
        _lanza(validar_base, [dict(base["ALI-MP-MAIZ"], NIVEL_EVIDENCIA="E3")]))
    chk("E06", "Conversión de moneda: maíz = ARS ÷ TC A3500 del día del precio; pollito con TC de su fecha",
        _cerca(precio_usd(base["ALI-MP-MAIZ"]), 295800 / 1522) and _cerca(precio_usd(base["POL-COMPRA"]), 1312.22 / 1486.5))
    chk("E07", "Referencias no comparables y extractos contradictorios no se usan como costo", all(
        f["COSTO_ID"] not in ("REF-SOJA-POROTO", "REF-HSOJA-INT", "REF-POL-CONTRA") for (fl, *_r) in run.values() for f in fl))
    chk("E08", "Precio anterior a la fecha base se marca (no se indexa)", any(
        "PRECIO_ANTERIOR_A_FECHA_BASE" in f["ALERTAS"] for f in f1 if f["COSTO_ID"] == "POL-COMPRA"))
    # ---------------- LABORAL ----------------
    lab = filas_costo_laboral("T", config_opex("C1", aves_dia=10000), D1, base)
    chk("L01", "Costo laboral total = PENDIENTE sin salarios; headcount PENDIENTE; sin horas extra automáticas",
        lab[-1]["COSTO_ANUAL_USD"] == "PENDIENTE" and all(r["HEADCOUNT"].startswith("PENDIENTE") for r in lab
                                                          if r["MODALIDAD"] == "interno"))
    labs = filas_costo_laboral("T", config_opex("C1", aves_dia=10000), D1, sint)
    esperado = 10 * (1 + 0.05 + 0.05) * (12 + 1) * (1 + 0.05 + 0.05) + 10 * 12 + 10 + 10 + 10
    chk("L02", "Costo empresa por FTE = salario × (1 + adic. + vac.) × (12 + SAC) × (1 + cargas + ART) + beneficios × 12 "
        "+ EPP + capac. + otros (SAC = regla, no precio)",
        all(_cerca(r["COSTO_EMPRESA_ANUAL_FTE_USD"], esperado) for r in labs if r["MODALIDAD"] == "interno"))
    chk("L03", "Funciones que 14A no dimensiona (granja, incubadora, planta de alimento) quedan PENDIENTE_CANTIDAD, no en 0",
        all(f["ESTADO"] == "PENDIENTE_CANTIDAD" for f in f3 if f["SUBMODULO"] in ("personal_granja", "personal_incubadora",
                                                                         "personal_planta_alimento")) and
        {"personal_granja", "personal_incubadora", "personal_planta_alimento"} <= {f["SUBMODULO"] for f in f3})
    # ---------------- RAMP-UP ----------------
    sv = _base_sintetica(pct_var=50)
    fr_, *_ = correr(config_opex("C1", aves_dia=10000), sv)
    full = aplicar_utilizacion(fr_, 1.0)
    half = aplicar_utilizacion(fr_, 0.5)
    fijo = sum(f["COSTO_CALCULADO_USD_ANIO"] * f["PCT_FIJO"] / 100 for f in fr_ if f["COSTEA"] and f["ESTADO"] == "CON_PRECIO")
    chk("R01", "Ramp-up: variables acompañan el volumen, fijos se mantienen (u = 0,5 → fijo + 0,5 × variable)",
        _cerca(half, fijo + 0.5 * (full - fijo)) and half < full)
    chk("R02", "Ramp-up sin curva definida → PENDIENTE (arranque y estabilización None)",
        rampup(fr_)["arranque"] is None and rampup(fr_)["estabilizacion"] is None)
    chk("R03", "Semivariable sin % variable declarado impide el ajuste (no se inventa el reparto)",
        aplicar_utilizacion(fs, 0.5) is None)
    # ---------------- ESCENARIOS ----------------
    a = correr(config_opex("C3", aves_dia=5000), base)[1]["TOTAL"]["CONCEPTOS_COSTEABLES"]
    correr(config_opex("C1", aves_dia=20000), base)
    b = correr(config_opex("C3", aves_dia=5000), base)[1]["TOTAL"]["CONCEPTOS_COSTEABLES"]
    chk("S01", "Escenarios independientes: correr otro escenario no altera el resultado", a == b)
    nan = [f for (fl, *_r) in run.values() for f in fl for k in ("CANTIDAD", "COSTO_CALCULADO_USD_ANIO")
           if isinstance(f[k], float) and (math.isnan(f[k]) or math.isinf(f[k]))]
    chk("S02", "Sin NaN ni infinitos en cantidades y costos", not nan)
    chk("S03", "Unidades válidas: unidad del driver = unidad del precio en todas las filas con COSTO_ID de la base",
        all(f["UNIDAD"] == base[f["COSTO_ID"]]["UNIDAD"] for (fl, *_r) in run.values() for f in fl
            if f["COSTO_ID"] in base))
    chk("S04", "Clasificación completa: naturaleza, centro de costo y tipo válidos en todas las filas", all(
        f["NATURALEZA"] in NATURALEZAS and f["CENTRO_COSTO"] in CENTROS and f["TIPO"] in TIPOS
        for (fl, *_r) in run.values() for f in fl))
    chk("S05", "Escala fuera de rango y escala intermedia: rechazo y alerta ESCALA_INTERMEDIA",
        _lanza(correr, config_opex("C1", aves_dia=30000), base) and any(
            a.startswith("ESCALA_INTERMEDIA") for a in correr(config_opex("C1", aves_dia=7500), base)[2]["alertas"]))
    chk("S06", "No hay CAPEX dentro del OPEX: ningún concepto OPEX usa IDs de la base CAPEX ni depreciación",
        not any(f["COSTO_ID"] in mcx.leer_base() for (fl, *_r) in run.values() for f in fl) and not any(
            "deprecia" in f["CONCEPTO"].lower() for (fl, *_r) in run.values() for f in fl))
    # ---------------- COMPLETITUD DE ARQUITECTURAS (auditoría de cierre 17) ----------------
    comp3 = {r["MODULO_ARQ"]: r for r in D3["completitud"]}
    gr3 = [f for f in f3 if f["MODULO_ARQ"] == "GRANJAS_PROPIAS"]
    chk("X01", "C3 con granjas propias tiene el bloque RRHH de granjas (PENDIENTE_CANTIDAD, universo propio) y todos sus "
        "bloques materiales (energía, calefacción, agua, cama, limpieza, bioseguridad, mantenimiento, mortalidad, seguros, "
        "veterinaria, otros)", any(f["BLOQUE"] == "rrhh" and f["UNIVERSO_RRHH"] == "RRHH_GRANJAS_PROPIAS_PENDIENTE"
                                   and f["ESTADO"] == "PENDIENTE_CANTIDAD" for f in gr3)
        and not comp3["GRANJAS_PROPIAS"]["BLOQUES_AUSENTES"]
        and {"PP-ENE", "PP-GAS", "PP-AGUA", "PP-CAMA", "PP-LIMP", "PP-BIO", "PP-MORT", "SEG-GRA", "PP-VET", "PP-OTR"}
        <= {f["COSTO_ID"] for f in gr3})
    inc = {f["COSTO_ID"] for f in f3 if f["MODULO_ARQ"] == "INCUBACION_PROPIA"}
    chk("X02", "Incubación propia contiene todos sus bloques materiales (huevo, vacunas, energía/HVAC, RRHH, agua, lavado, "
        "mantenimiento, consumibles, descartes, transporte de huevo y de pollito, calidad/bioseguridad)",
        not comp3["INCUBACION_PROPIA"]["BLOQUES_AUSENTES"] and
        {"INC-OP-HUEVO", "INC-OP-VAC", "INC-OP-ENE", "INC-OP-AGUA", "INC-OP-LIM", "INC-OP-INS", "INC-OP-DES", "INC-OP-CAL",
         "LAB-CONV_SOP"} <= inc and any(f["FLUJO"] == "huevos" for f in f3) and any(f["FLUJO"] == "pollitos" for f in f3))
    ali = {f["COSTO_ID"] for f in f3 if f["MODULO_ARQ"] == "PLANTA_ALIMENTO_PROPIA"}
    chk("X03", "Planta de alimento propia contiene todos sus bloques materiales (maíz, soja, aceite, núcleo, otros, "
        "diferencial a planta, RRHH, electricidad, vapor, agua, mantenimiento, laboratorio, mermas, almacenamiento, "
        "movimientos internos, transporte)", not comp3["PLANTA_ALIMENTO_PROPIA"]["BLOQUES_AUSENTES"] and
        {"ALI-MP-MAIZ", "ALI-MP-SOJA", "ALI-MP-ACEITE", "ALI-MP-NUCLEO", "ALI-MP-OTROS", "ALI-MP-DIF-MAIZ", "ALI-C-ENE",
         "ALI-C-TER", "ALI-C-AGUA", "ALI-C-ANA", "ALI-MERMA", "ALI-C-ALM", "ALI-C-MOV", "LAB-CONV_SOP"} <= ali)
    k09 = {k for (_, _, DR, _, _) in run.values() for k, p in DR["proc"].items() if p["FUENTE"].startswith("11_agua")}
    usa09 = [f for (fl, *_r) in run.values() for f in fl if f["DRIVER"].split(" ")[0] in k09]
    up = [f for (fl, *_r) in run.values() for f in fl if f["UNIVERSO_UTILITIES"] not in ("", "FAENA_09C")]
    chk("X04", "Utilities de faena (09C) no se reutilizan para upstream: todo driver de 09C se usa solo en FAENA_PROPIA; "
        "incubación, alimento, rendering y tratamiento quedan PENDIENTE_CANTIDAD; en granjas solo el agua de bebida de 03",
        usa09 and all(f["MODULO_ARQ"] == "FAENA_PROPIA" for f in usa09) and up and all(
            f["DRIVER"].split(" ")[0] not in k09 for f in up) and all(
            f["CANTIDAD"] is None for f in up if f["UNIVERSO_UTILITIES"] != "GRANJAS")
        and all(f["CANTIDAD"] is None for f in up if f["UNIVERSO_UTILITIES"] == "GRANJAS" and f["COSTO_ID"] != "PP-AGUA"))
    fu3 = r3["TOTAL"]
    chk("X05", "FTE de 14A no se etiqueta como FTE total de la empresa integrada: driver fte_industrial_14a; C3 con "
        "FTE_ADICIONAL_PENDIENTE (granjas, incubación, planta de alimento); en C0 el personal del faenador no es FTE propio",
        not any(k.startswith("fte_total") for (_, _, DR, _, _) in run.values() for k in DR["proc"])
        and "NO es el FTE total" in D3["proc"]["fte_industrial_14a"]["USO_EN_OPEX"]
        and fu3["FTE_ADICIONAL_PENDIENTE"].startswith("PENDIENTE") and all(
            x in fu3["FTE_ADICIONAL_PENDIENTE"] for x in ("granjas", "incubación", "planta de alimento"))
        and r0["TOTAL"]["FTE_TOTAL_CONOCIDO"] < r0["TOTAL"]["FTE_INDUSTRIAL_14A"] - 10)
    arq_ok = completitud(config_opex("C1", aves_dia=10000), fs_ok)[1]
    chk("X06", "Un módulo con un bloque material faltante bloquea el OPEX total aunque los conceptos presentes tengan precio "
        "(y hoy ninguna arquitectura es costeable ni publica total)",
        not arq_ok["ARQUITECTURA_COSTEABLE"] and resumir(fs_ok, Ds, arq_ok)["TOTAL"]["TOTAL_PRELIMINAR_USD_ANIO"] is None
        and all(not x[2]["arquitectura"]["ARQUITECTURA_COSTEABLE"] and x[1]["TOTAL"]["TOTAL_PRELIMINAR_USD_ANIO"] is None
                for x in run.values()))
    reglas = leer_reglas()
    con_precio = [r for r in base.values() if r["ESTADO"] == "CON_PRECIO"]
    chk("X07", "13 meses / SAC no figura como precio ni evidencia E4: no hay fila de 'meses' en la base; con precio quedan 2",
        not any(r["UNIDAD"] == "meses" or "MESES" in r["ID_COSTO"] or "SAC" in r["ID_COSTO"] for r in base.values())
        and len(con_precio) == 2 and {r["ID_COSTO"] for r in con_precio} == {"POL-COMPRA", "ALI-MP-MAIZ"})
    chk("X08", "El SAC es una regla laboral (no cotización): sin nivel E1–E5; una regla con evidencia E4 es rechazada",
        reglas["SAC"]["ESTADO"].startswith("REGLA") and reglas["SAC"]["EVIDENCIA"] not in EVIDENCIAS
        and _lanza(validar_reglas, {"X": dict(reglas["SAC"], EVIDENCIA="E4")}))
    pol = next(f for f in f1 if f["COSTO_ID"] == "POL-COMPRA")
    chk("X09", "Precio ARS observado y conversión USD separados (pollito: ARS 1.312,22, fecha, IVA, TC 1.486,5 y su fecha, "
        "USD = conversión del modelo)", pol["PRECIO_ORIGINAL_OBSERVADO"] == 1312.22 and pol["MONEDA_ORIGINAL"] == "ARS"
        and pol["FECHA_PRECIO"] == "2026-07-06" and pol["IVA_PRECIO"].startswith("sin_iva") and pol["TC_USADO"] == 1486.5
        and pol["FECHA_TC"] == "2026-07-06" and pol["ORIGEN_PRECIO_USD"].startswith("CONVERSION_MODELO")
        and _cerca(pol["PRECIO_USD"], 1312.22 / 1486.5) and base["POL-COMPRA"]["MONEDA_ORIGINAL"] == "ARS")
    dif = [f for f in f3 if f["COSTO_ID"] == "ALI-MP-DIF-MAIZ"]
    mz = next(f for f in f3 if f["COSTO_ID"] == "ALI-MP-MAIZ")
    ctm = next(r for r in run[("C3", 10000)][3] if r["SUBCOMPONENTE"] == "alimento: maiz")
    chk("X10", "Maíz Rosario no se etiqueta 'puesto en planta': condición SOBRE_PUERTO, diferencial a planta como concepto "
        "PENDIENTE y CT advierte la valuación", "SOBRE_PUERTO" in mz["CONDICION_ENTREGA"]
        and "NO es costo puesto en planta" in mz["CONDICION_ENTREGA"] and dif and dif[0]["ESTADO"] == "PENDIENTE_PRECIO"
        and _cerca(dif[0]["CANTIDAD"], mz["CANTIDAD"]) and "Rosario" in ctm["FALTA"])
    fac0 = [f for f in f0 if f["MODULO"] == "COSTO_LABORAL" and f["SUBMODULO"] in ("colgado", "evisceracion", "trozado")]
    chk("X11", "Façon no duplica personal: horas del faenador = RECURSO FÍSICO DE TERCERO, INCLUIDO_EN_TARIFA_FACON, sin "
        "costo laboral propio de operación industrial", fac0 and all(
            f["APORTANTE"] == "TERCERO" and f["ESTADO"] == "INCLUIDO_EN_TARIFA_FACON" and not f["COSTEA"] for f in fac0)
        and not any(f["COSTEA"] and f["MODULO"] == "COSTO_LABORAL" and f["SUBMODULO"] in
                    ("colgado", "descarga", "faena", "evisceracion", "enfriamiento", "clasificacion", "trozado", "empaque",
                     "camaras_expedicion", "subproductos") for f in f0))
    ctall = [r for x in run.values() for r in x[3] if r["COMPONENTE"] == "INVENTARIO"]
    chk("X12", "Stock de tercero no entra al CT propio en ninguna arquitectura (entra solo con PROPIEDAD_EMPRESA = TRUE)",
        all((r["ENTRA_EN_CT"] == "Sí") == (r["PROPIEDAD_EMPRESA"] == "TRUE") for r in ctall)
        and all(r["VALOR_USD"] is None for r in ctall if r["PROPIEDAD_EMPRESA"] != "TRUE")
        and any(r["PROPIEDAD_EMPRESA"] == "FALSE" for r in ctall))
    chk("X13", "Montos parciales E4 marcados NO COMPARABLES (ningún escenario aparece como resultado económico comparable)",
        all(x[1]["TOTAL"]["COMPARABILIDAD"] == "MONTOS_PARCIALES_E4_NO_COMPARABLES" for x in run.values())
        and not any(d["COMPARABILIDAD"].startswith("COMPARABLE") for x in run.values() for d in x[1].values()))
    compF = {r["MODULO_ARQ"]: r for r in run[("CF", 10000)][2]["completitud"]}
    chk("X14", "Rendering y reproductoras (CF, FUTURO): estructura completa (RRHH, energía, térmico, agua, mantenimiento, "
        "insumos, tratamiento, residuos, logística) sin costos y sin bloquear la etapa inicial",
        not compF["RENDERING_FUTURO"]["BLOQUES_AUSENTES"] and not compF["REPRODUCTORAS_FUTURO"]["BLOQUES_AUSENTES"]
        and all(f["COSTO_CALCULADO_USD_ANIO"] is None for f in run[("CF", 10000)][0] if f["FASE"] == "FUTURO"))
    var = [correr(config_opex(cf, aves_dia=10000, alimento_facon_mp=v_), base) for cf in ("C0", "C2")
           for v_ in ("empresa", "elaborador")]
    chk("X15", "Cobertura estructural ≠ cobertura de costeo: estructura 100 % en todas las arquitecturas y variantes de "
        "façon (sé qué costos existen) y costeo por bloques < 100 % (no sé cuánto cuestan)", all(
            abs(x[2]["arquitectura"]["COBERTURA_ESTRUCTURAL_PCT"] - 100) < TOL and x[2]["arquitectura"]["ARQUITECTURA_ESTRUCTURA_COMPLETA"]
            and x[2]["arquitectura"]["COBERTURA_COSTEO_BLOQUES_PCT"] < 100 for x in list(run.values()) + var))
    propios = [fn for fn in ("vivo", "refrigerado", "alimento", "pollitos", "huevos", "subproductos")]
    chk("X16", "Flota propia (C3): cada flujo tiene combustible, mantenimiento, choferes y seguro (aunque PENDIENTES)", all(
        any(f["COSTO_ID"] == "LOG-COMB-GASOIL" and f["FLUJO"] == fn for f in f3)
        and any(f["COSTO_ID"].endswith("-MANT") and f["FLUJO"] == fn for f in f3)
        and any(f["COSTO_ID"].startswith("SEG-FLOTA") and f["FLUJO"] == fn for f in f3)
        and (fn in ("vivo", "refrigerado", "congelado") or any(f["COSTO_ID"] == "LAB-CHOF" and f["FLUJO"] == fn for f in f3))
        for fn in propios))
    return res


MUTACIONES = {"D01": "OPEX recalcula el alimento con un FCR propio", "M01": "un faltante se convierte en 0",
              "M02": "duplica la energía de frío", "M03": "compra de alimento carga energía de fábrica propia",
              "M08": "limpieza vuelve a cobrar agua ya incluida en utilities", "M04": "el stock de un tercero entra al CT",
              "M06": "una referencia E4 se presenta como E1", "M07": "un costo negativo (neteo)",
              "M09": "flota tercerizada carga costos de flota propia", "M10": "choferes tercerizados cobrados además del flete",
              "M11": "personal del faenador cobrado además de la tarifa de façon",
              "M12": "la incubadora reutiliza el kWh de la planta de faena (09C)",
              "M14": "se omite el bloque RRHH de la incubación propia",
              "M17": "se publica total sin mirar la completitud de los módulos"}


def prueba_mutaciones():
    print("Mutaciones (cada una debe hacer fallar al menos un test):")
    ok_all = True
    for m, desc in MUTACIONES.items():
        _MUT.clear()
        _MUT.add(m)
        try:
            res = ejecutar_tests(verbose=False)
            fallan = [i for i, _, ok in res if not ok]
        except Exception as e:                                   # noqa: BLE001
            fallan = [f"excepción: {type(e).__name__}"]
        _MUT.clear()
        det = bool(fallan)
        ok_all &= det
        print(f"  [{'DETECTADA' if det else 'NO DETECTADA'}] {m} {desc} → {', '.join(fallan[:4])}")
    return ok_all


# ---------------------------------------------------------------------------------------------
# 11. CLI
# ---------------------------------------------------------------------------------------------
def escenario_cli(a):
    base = leer_base(a.costos) if a.costos else leer_base()
    c = config_opex(a.config, aves_dia=a.aves_dia, fecha_base_opex=a.fecha_base)
    filas, res, DR, ct_rows, ct = correr(c, base)
    print(f"Escenario {a.config}-{a.aves_dia:g} — {mcx.etiqueta_arquitectura(config_capex(c))}")
    for m, d in res.items():
        print(f"  {m:20s} conceptos {d['CONCEPTOS_COSTEABLES']:3d} | con precio {d['CONCEPTOS_CON_PRECIO']:3d} | "
              f"monto parcial {_fmt(d['MONTO_PARCIAL_CON_PRECIO_USD_ANIO']) or '—':>12} USD/año ({d['COMPARABILIDAD']}) | "
              f"{d['TOTAL_PRELIMINAR']}")
    arq = DR["arquitectura"]
    print(f"  Arquitectura: estructura completa {arq['ARQUITECTURA_ESTRUCTURA_COMPLETA']} | operativamente completa "
          f"{arq['ARQUITECTURA_OPERATIVAMENTE_COMPLETA']} | costeable {arq['ARQUITECTURA_COSTEABLE']} | cobertura estructural "
          f"{arq['COBERTURA_ESTRUCTURAL_PCT']:.0f} % / física {arq['COBERTURA_FISICA_PCT']:.0f} % / costeo "
          f"{arq['COBERTURA_COSTEO_BLOQUES_PCT']:.0f} %")
    print(f"  Capital de trabajo: {ct['CAPITAL_TRABAJO']} — falta: {ct['FALTA']}")
    for al in DR["alertas"]:
        print("  ALERTA:", al)


def main():
    ap = argparse.ArgumentParser(description="Motor OPEX + capital de trabajo (sesión 17)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--escenario", action="store_true")
    ap.add_argument("--config", default="C1")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--costos", default=None)
    ap.add_argument("--fecha-base", default=FECHA_BASE_OPEX)
    a = ap.parse_args()
    if a.escenario:
        if a.aves_dia == int(a.aves_dia):
            a.aves_dia = int(a.aves_dia)
        escenario_cli(a)
        return 0
    if a.mutaciones:
        return 0 if prueba_mutaciones() else 1
    print(f"MOTOR OPEX v{VERSION} — tests")
    res = ejecutar_tests()
    fallas = [r for r in res if not r[2]]
    print(f"{len(res) - len(fallas)}/{len(res)} tests OK")
    if fallas:
        print("FALLAN:", ", ".join(i for i, _, _ in fallas))
        return 1
    if a.solo_tests:
        return 0
    n = construir_salidas()
    print("Salidas escritas:", n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
