#!/usr/bin/env python3
"""
MODELO FINANCIERO INTEGRAL — versión 1.0 (2026-10-04, sesión 19)
=================================================================

DEMANDA → UTILIZACIÓN → PRODUCCIÓN → VENTAS → INGRESOS → OPEX → EBITDA → CAPITAL DE TRABAJO → CAPEX
        → FLUJO DE CAJA DEL PROYECTO (FCFF) → FLUJO DEL ACCIONISTA (FCFE) → VAN / TIR / PAYBACK / BREAK-EVEN

El motor NO elige escala, arquitectura, financiamiento ni gatillo de expansión, NO optimiza y NO recomienda.
Evalúa las MISMAS configuraciones de `00_gestion_proyecto/mapa_arquitecturas_economicas.csv` (C0–CF y sus
variantes) consumiendo, sin modificarlos ni copiar sus fórmulas:
  * 19_capex/modelo_capex.py   (preset(), correr(), expansion() con su lógica de acciones por etiqueta)
  * 20_opex/modelo_opex.py     (config_opex(), correr(): registro por concepto con NATURALEZA y PCT_VARIABLE,
                                capital de trabajo con PROPIEDAD_EMPRESA)
  * 04_balance_masa/modelo_balance_masa.py + 23_plan_expansion/modelo_escala.py (kg por ave de cada producto,
                                rutas exclusivas esqueleto/CMS, agrupación ITEMS)
  * 02_clientes_demanda/escenarios_demanda.csv (escenarios comerciales de prueba: SUPUESTO, no demanda)

DOS MODOS (nunca se mezclan)
  EVIDENCIA : solo datos dentro de UMBRAL_EVIDENCIA_PUBLICACION (default E1–E3, configurable en
              inputs_financieros.csv sin tocar código; DEC-084 abierta) y los supuestos
              metodológicos permitidos (SUPUESTOS_METODOLOGICOS). Si falta un bloque material, NO publica
              (NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE) y lista exactamente qué falta.
  ESCENARIO : acepta inputs del usuario (precios, demanda, CAPEX, OPEX, utilización, ramp-up, financiamiento,
              impuestos, plazos). Todo resultado se rotula SIMULACION_HIPOTETICA_NO_VALIDADA. Jerarquía:
              EVIDENCIA_REAL > ESCENARIO_USUARIO > SUPUESTO_MODELO > PENDIENTE; el escenario nunca
              sobrescribe la base de evidencia (la completa donde falta).

MÉTODO TEMPORAL
  Motor interno MENSUAL (k = 0 es T0, instante de FECHA_INICIO; k = 1…12·H son meses) agregado a períodos de
  reporte: T0, meses 1…MESES_DETALLE (por defecto 24) y años posteriores. Flujos = suma; saldos = fin de
  período. Indicadores (convención MENSUAL por defecto): TASA_DESCUENTO anual EFECTIVA → mensual
  (1 + r)^(1/12) − 1; VAN = Σ F_k ÷ (1 + i_m)^k (T0 sin descontar); TIR mensual → anual (1 + i)^12 − 1;
  payback en meses y años = meses ÷ 12. Convención alternativa PERIODO_REPORTE: flujos agregados al fin de
  cada período de reporte (declarada en cada corrida).
  Fases: PREOPERACION → CONSTRUCCION → COMMISSIONING → RAMP_UP → OPERACION_MADURA (duraciones = inputs).

FÓRMULAS (identidades verificadas por tests)
  capacidad_aves_mes      = escala_aves_dia_operativo × días_operativos_año ÷ 12          (etapa activa)
  aves_disponibles        = Σ_etapas Δescala × días ÷ 12 × u_técnica_etapa(meses desde su entrada)
  aves_requeridas         = máx_producto (demanda_kg − inventario_kg) ÷ (kg_por_ave × (1 − merma))  (parte limitante)
  aves_faenadas           = mín(aves_disponibles, aves_requeridas)
  u_técnica = disponibles ÷ capacidad ; u_comercial = requeridas ÷ capacidad (puede > 1) ; u_efectiva = faenadas ÷ capacidad
  ventas_kg(línea)        ≤ mín(disponible = producción + inventario, demanda)   (inventario no crea producto)
  venta_bruta             = Σ ventas_kg × precio
  ingreso_neto            = venta_bruta − descuentos − bonificaciones − devoluciones − comisiones − derechos de exportación
  opex(mes)               = Σ_rubros costo_pleno ÷ 12 × [PCT_VARIABLE × u_efectiva ÷ eficiencia + (1 − PCT_VARIABLE)]
                            (fijos y semifijos NO bajan con la utilización; semivariable sin % → PENDIENTE)
  EBITDA                  = ingreso_neto − opex − costos comerciales del canal − impuestos sobre ingresos − extras de ramp-up
  EBIT                    = EBITDA − depreciación
  CT                      = inventarios propios + CxC + caja operativa − CxP ;  flujo usa ΔCT
  FCFF                    = EBIT − impuestos operativos (sobre EBIT, sin deuda) + depreciación − CAPEX − ΔCT + flujo IVA
                            (= EBITDA − impuestos operativos − CAPEX − ΔCT + flujo IVA) [+ valor terminal]
  FCFE                    = EBITDA − impuestos con deuda − CAPEX − ΔCT + flujo IVA − intereses − comisiones
                            + desembolsos de deuda − amortizaciones [+ valor terminal − deuda remanente]
  caja(k)                 = caja(k−1) + FCFE(k) + aportes(k) − dividendos(k)
  deuda                   : saldo inicial + altas − amortización = saldo final ; interés = saldo × tasa del período
                            (EFECTIVA_ANUAL: (1+TEA)^(f/12) − 1 · NOMINAL_ANUAL: TNA × f ÷ 12 con capitalización = f ·
                            PERIODICA: tasa del período = f); combinaciones ambiguas → error
  VAN = Σ F_t ÷ (1 + r)^t ; TIR única o NO_EXISTE / TIR_AMBIGUA ; payback simple y descontado o NO_RECUPERADO
  break-even (año maduro) : q* = fijos ÷ (margen de contribución por ave) ; u* = q* ÷ capacidad ;
                            precio* = precio medio × (variables + fijos) ÷ (ingreso neto − impuestos ∝ precio)

Uso
---
    python3 21_modelo_financiero/modelo_financiero.py                 # tests + CSV de salida
    python3 21_modelo_financiero/modelo_financiero.py --solo-tests
    python3 21_modelo_financiero/modelo_financiero.py --mutaciones    # los tests detectan errores sembrados
    python3 21_modelo_financiero/modelo_financiero.py --escenario mi_escenario.json   # MODO ESCENARIO

El script se DETIENE (código 1) si falla cualquier prueba. Unidades métricas; CSV con punto decimal; USD.
IDs reconciliados en 00_gestion_proyecto/reconciliacion_sesiones_19_20.md (SUP-189 a SUP-211; DPV-178; DEC-093 a DEC-096).
"""
import argparse
import copy
import csv
import io
import json
import math
import os
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _d in ("20_opex", "19_capex", "04_balance_masa", "23_plan_expansion"):
    _p = os.path.join(RAIZ, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
with redirect_stdout(io.StringIO()):
    import modelo_opex as mo            # noqa: E402  (17 → 16 → 12C, 09C, 12B, 14A, 14B, 05, 04)
    import modelo_escala as me          # noqa: E402  (23 → 03, 04, 07)
mcx, mb = mo.mcx, mo.mb

VERSION = "1.0"
FECHA = "2026-10-04"
FUENTE = "21_modelo_financiero/modelo_financiero.py"
MONEDA = "USD"
DIAS_ANIO = 365
DIAS_MES = DIAS_ANIO / 12                      # 30,4167: base de CxC, CxP, inventarios y caja (días calendario)
TOL = 1e-9
_MUT: set = set()                              # mutaciones sembradas (solo prueba_mutaciones)

ARCHIVO_MAPA_ARQ = os.path.join(RAIZ, "00_gestion_proyecto", "mapa_arquitecturas_economicas.csv")
ARCHIVO_ARQ_MAESTRAS = os.path.join(RAIZ, "00_gestion_proyecto", "arquitecturas_maestras.csv")
ARCHIVO_MATRIZ_ECO = os.path.join(RAIZ, "00_gestion_proyecto", "matriz_completitud_economica.csv")
ARCHIVO_DEMANDA = os.path.join(RAIZ, "02_clientes_demanda", "escenarios_demanda.csv")
ARCHIVO_PRECIOS = os.path.join(AQUI, "base_precios_venta.csv")
ARCHIVO_INPUTS = os.path.join(AQUI, "inputs_financieros.csv")
ARCHIVO_CURVAS = os.path.join(AQUI, "curvas_rampup.csv")
SALIDAS = {k: os.path.join(AQUI, f"{k}.csv") for k in (
    "escenarios_financieros", "flujo_caja_proyecto", "flujo_accionista", "estado_resultados",
    "capital_trabajo_financiero", "deuda", "break_even", "completitud_financiera", "mapa_drivers_financieros",
    "casos_prueba_motor")}

MODOS = ("EVIDENCIA", "ESCENARIO")
ORIGENES = ("EVIDENCIA_REAL", "ESCENARIO_USUARIO", "SUPUESTO_MODELO", "PENDIENTE")
NIVELES = ("E1", "E2", "E3", "E4", "E5")
# UMBRAL_EVIDENCIA_PUBLICACION: niveles que el modo evidencia acepta. Se lee de inputs_financieros.csv (variable
# `umbral_evidencia_publicacion`, p. ej. "E1|E2|E3") para poder cambiarlo SIN tocar código (DEC-084 abierta).
# Este valor es solo el default conservador si la fila no existe. E4 [PVDP] no pasa el default.
UMBRAL_EVIDENCIA_DEFAULT = ("E1", "E2", "E3")             # SUP-190
NIVELES_EVIDENCIA_ACEPTADOS = UMBRAL_EVIDENCIA_DEFAULT    # compatibilidad: default, no decisión
ETIQUETA_SIM = "SIMULACION_HIPOTETICA_NO_VALIDADA"
NO_PUB = "NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE"
NO_DISP_ESC = "NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO"
# Interfaz de performance (sesión 20): resultados(R, calcular_tir=False) omite SOLO la TIR. La métrica queda en este
# estado (no es 0 ni un faltante de datos); el default True reproduce exactamente la sesión 19.
TIR_NO_CALCULADA = "NO_CALCULADA"
# Defensas de la auditoría final 21 (TF-004, TF-005, TF-076)
OVERRIDE_INCOMPATIBLE = "OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA"
ETIQUETA_OVERRIDE_TOTAL = "SIMULACION_HIPOTETICA_OVERRIDE_TOTAL"
CAMPOS_META_OVERRIDE = ("CONFIGURACION", "ESCALA", "VARIANTE", "MODULO", "UNIVERSO", "ORIGEN")
NO_CALC_FISCAL = "NO_CALCULABLE_REGLA_FISCAL_PENDIENTE"
CREDITO_IVA_CAPEX_PEND = "CREDITO_FISCAL_IVA_CAPEX = PENDIENTE"
ESTADOS_IVA_CAPEX_INCIERTO = ("DESCONOCIDO", "INCIERTO", "NO_DECLARADO")
ESTADOS_BLOQUE = ("CON_EVIDENCIA", "PENDIENTE", "VACIO", "NO_APLICA")
# Convenciones que el MODO EVIDENCIA admite como SUPUESTO_MODELO (no son datos económicos; SUP-191)
SUPUESTOS_METODOLOGICOS = {"modelo_monetario", "base_tasa", "meses_detalle", "valor_terminal.metodo",
                           "valor_terminal.recuperar_ct", "moneda_funcional", "convencion_descuento",
                           "tipo_tasa_descuento", "umbral_evidencia_publicacion"}
# Convenciones de tasa (SUP-192 / SUP-200). La tasa de descuento es ANUAL EFECTIVA salvo declaración expresa.
TIPOS_TASA_DESCUENTO = ("EFECTIVA_ANUAL", "NOMINAL_ANUAL_CAP_MENSUAL")
TIPOS_TASA_DEUDA = ("EFECTIVA_ANUAL", "NOMINAL_ANUAL", "PERIODICA")
CONVENCIONES_DESCUENTO = ("MENSUAL", "PERIODO_REPORTE")
CLAVES_IMPUESTOS = ("tasa_ganancias", "anios_quebranto", "pct_iibb", "pct_tasas_municipales", "otros_impuestos_usd_anio",
                    "intereses_deducibles", "iibb_aplica_domestico", "iibb_aplica_exportacion")   # los derechos de exportación NO van aquí: solo en canales.exportacion

# Demanda (02 §1): A = asegurada / documentada; B = negociada; entre B y C = interesada; C/D = potencial
CATEGORIAS_DEMANDA = ("DOCUMENTADA", "ASEGURADA", "NEGOCIADA", "INTERESADA", "POTENCIAL", "ESCENARIO")
CATEGORIAS_DEMANDA_EVIDENCIA = ("DOCUMENTADA", "ASEGURADA")   # únicas que el modo evidencia vende (SUP-193)
CANALES = ("supermercados", "mayoristas", "carnicerias_pollerias", "gastronomia", "industria", "exportacion", "otros")
CATEGORIAS_INGRESO = ("PRODUCTO_PRINCIPAL", "MENUDENCIAS", "PATAS_GARRAS", "SUBPRODUCTOS", "RENDERING", "OTROS")
# Productos = claves ITEMS de 23 (una sola agrupación del balance 04, sin doble conteo). None = no vendible.
CATEGORIA_PRODUCTO = {
    "pollo_entero": "PRODUCTO_PRINCIPAL", "pechuga": "PRODUCTO_PRINCIPAL", "pechuga_deshuesada": "PRODUCTO_PRINCIPAL",
    "pata_muslo": "PRODUCTO_PRINCIPAL", "pata_muslo_procesada": "PRODUCTO_PRINCIPAL",
    "alas": "OTROS", "carcasa_esqueleto": "OTROS", "cms": "OTROS", "recortes_piel": "OTROS",
    "menudencias": "MENUDENCIAS", "cuello": "MENUDENCIAS", "garras": "PATAS_GARRAS",
    "sangre": "SUBPRODUCTOS", "plumas": "SUBPRODUCTOS", "visceras": "SUBPRODUCTOS", "cabeza": "SUBPRODUCTOS",
    "huesos": "SUBPRODUCTOS", "otros_c": "SUBPRODUCTOS",
    "residuos": None, "perdidas": None,
}
PRODUCTOS_CLASE_C = ("sangre", "plumas", "visceras", "cabeza", "huesos", "otros_c")
PRODUCTO_RENDERING = "harinas_rendering"        # salida del rendering propio (FUTURO; rendimiento DPV-065)
DESTINOS_C = ("venta_directa", "rendering_propio", "contrato_facon")
NATURALEZAS = ("variable", "fijo", "semifijo", "semivariable")
CATEGORIAS_INVENTARIO = ("materias_primas", "alimento", "packaging", "repuestos", "producto_terminado",
                         "activo_biologico", "otros")
METODOS_DEUDA = ("FRANCES", "ALEMAN", "BULLET", "PERSONALIZADO")
METODOS_VT = ("SIN_VALOR_TERMINAL", "VALOR_LIBRO", "EXPLICITO", "PERPETUIDAD")
UNIDADES_DEMANDA = {"kg/dia": DIAS_MES, "t/dia": 1000 * DIAS_MES, "kg/mes": 1.0, "t/mes": 1000.0,
                    "kg/anio": 1 / 12, "t/anio": 1000 / 12}          # "dia" = día CALENDARIO (02, SUP-020)
FASES = ("T0", "PREOPERACION", "CONSTRUCCION", "COMMISSIONING", "RAMP_UP", "OPERACION_MADURA")
CLAVES_STRESS = ("precio", "alimento", "demanda", "capex", "opex", "rampup_lento_factor", "mortalidad",
                 "corte_exportacion_desde_mes", "devaluacion")
# Plantillas de stress (infraestructura; no son pronósticos ni se aplican solas). Monte Carlo: NO (fase posterior).
STRESS_PREDEFINIDOS = {
    "ALIMENTO_+20": {"alimento": 1.20}, "PRECIO_POLLO_-10": {"precio": 0.90}, "DEMANDA_-30": {"demanda": 0.70},
    "CAPEX_+25": {"capex": 1.25}, "RAMPUP_LENTO_x2": {"rampup_lento_factor": 2.0},
    "MORTALIDAD_MAYOR": {"mortalidad": {"base": None, "nueva": None}},          # requiere base y nueva declaradas
    "DEVALUACION": {"devaluacion": {"pct": None, "traslado_precios_ars": None}},  # requiere pct y traslado declarados
    "CORTE_EXPORTACION": {"corte_exportacion_desde_mes": None},
}
GATILLOS = ("utilizacion_min", "demanda_asegurada_min", "factor_demanda_capacidad_min", "caja_min_usd",
            "dscr_min", "anio_min")


class ErrorFinanciero(Exception):
    pass


# ---------------------------------------------------------------------------------------------
# 0. UTILIDADES
# ---------------------------------------------------------------------------------------------
def _s(*xs):
    """Suma None-segura: cualquier None → None (un faltante nunca se vuelve 0)."""
    if any(x is None for x in xs):
        return None
    return sum(xs)


def _sum(it):
    it = list(it)
    return None if any(x is None for x in it) else sum(it)


def _fmt(x, dec=4):
    if x is None:
        return ""
    if isinstance(x, bool):
        return "TRUE" if x else "FALSE"
    if isinstance(x, float):
        if math.isinf(x) or math.isnan(x):
            return str(x)
        return f"{x:.{dec}f}".rstrip("0").rstrip(".") if abs(x) < 1e15 else f"{x:.6g}"
    return str(x)


def escribir(ruta, filas, campos):
    with open(ruta, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos, extrasaction="raise", lineterminator="\n")
        w.writeheader()
        for f in filas:
            w.writerow({k: _fmt(f.get(k)) for k in campos})


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def _num(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "":
        return None
    return float(x)


def sumar_meses(fecha, n):
    a, m, d = (int(x) for x in fecha.split("-"))
    m0 = a * 12 + (m - 1) + n
    return f"{m0 // 12:04d}-{m0 % 12 + 1:02d}-{d:02d}"


def convertir_demanda(valor, unidad, dias_operativos_anio=None):
    """kg/mes desde kg/día, t/día, t/mes, t/año (días calendario, convención de 02) o kg/dia_operativo."""
    if valor is None:
        return None
    if unidad == "kg/dia_operativo":
        if not dias_operativos_anio:
            raise ErrorFinanciero("kg/dia_operativo exige días operativos por año")
        return valor * dias_operativos_anio / 12
    if unidad not in UNIDADES_DEMANDA:
        raise ErrorFinanciero(f"unidad de demanda {unidad!r} no admitida {tuple(UNIDADES_DEMANDA) + ('kg/dia_operativo',)}")
    return valor * UNIDADES_DEMANDA[unidad]


def a_usd(valor, moneda, tc=None, fecha_tc=None, tipo_tc=None):
    """Regla 2: un valor en ARS (u otra moneda) exige TC, tipo y fecha. Nunca se convierte en silencio."""
    if valor is None:
        return None
    if moneda == "USD":
        return valor
    if not tc or not fecha_tc or not tipo_tc:
        raise ErrorFinanciero(f"valor en {moneda} sin tipo de cambio, tipo y fecha (regla 2 de CLAUDE.md)")
    return valor / tc


def a_moneda_reporte(valores_usd, moneda, fx_por_periodo=None, tipo_tc=None):
    """Moneda funcional USD; reporte en ARS solo con un TC por período declarado (tipo y fuente). No se mezcla
    inflación ARS con flujos USD reales en silencio: un reporte ARS de un modelo REAL usa TC real declarado."""
    if moneda == "USD":
        return list(valores_usd)
    if moneda != "ARS":
        raise ErrorFinanciero("moneda de reporte: USD | ARS")
    if not fx_por_periodo or not tipo_tc or len(fx_por_periodo) != len(valores_usd) or any(x is None for x in fx_por_periodo):
        raise ErrorFinanciero("reporte en ARS exige un TC por período con tipo declarado (regla 2)")
    return [None if v is None else v * fx for v, fx in zip(valores_usd, fx_por_periodo)]


# ---------------------------------------------------------------------------------------------
# 1. TRAZABILIDAD Y JERARQUÍA DE INPUTS
# ---------------------------------------------------------------------------------------------
class Traza:
    CAMPOS = ["ESCENARIO", "VARIABLE", "VALOR", "UNIDAD", "PERIODO", "ORIGEN", "ARCHIVO", "VARIABLE_ORIGEN", "MODO",
              "EVIDENCIA", "OBSERVACIONES"]

    def __init__(self, escenario, modo):
        self.escenario, self.modo, self.filas = escenario, modo, []

    def add(self, variable, valor, unidad, origen, archivo="", variable_origen="", evidencia="", obs="", periodo="TODOS"):
        if origen not in ORIGENES:
            raise ErrorFinanciero(f"origen inválido {origen}")
        if isinstance(valor, (list, dict, tuple)):
            valor = json.dumps(valor, ensure_ascii=False, default=str)[:300]
        self.filas.append({"ESCENARIO": self.escenario, "VARIABLE": variable, "VALOR": valor, "UNIDAD": unidad,
                           "PERIODO": periodo, "ORIGEN": origen, "ARCHIVO": archivo, "VARIABLE_ORIGEN": variable_origen,
                           "MODO": self.modo, "EVIDENCIA": evidencia or ("PENDIENTE" if origen == "PENDIENTE" else ""),
                           "OBSERVACIONES": obs})


def tasa_periodica(tasa_anual_efectiva, meses):
    """Tasa efectiva de un período de `meses` equivalente a una tasa ANUAL EFECTIVA: (1 + r)^(meses/12) − 1.
    Nunca r/12 (eso solo vale para una tasa nominal anual convertible mensualmente, que debe declararse)."""
    if tasa_anual_efectiva is None:
        return None
    if tasa_anual_efectiva <= -1:
        raise ErrorFinanciero("tasa ≤ −100 %")
    if "M22" in _MUT:
        return tasa_anual_efectiva * meses / 12
    return (1 + tasa_anual_efectiva) ** (meses / 12) - 1


def tasa_anual_efectiva(tasa, tipo):
    """Normaliza la tasa de descuento declarada a anual efectiva. Tipo obligatorio y explícito."""
    if tasa is None:
        return None
    if tipo == "EFECTIVA_ANUAL":
        return tasa
    if tipo == "NOMINAL_ANUAL_CAP_MENSUAL":
        return (1 + tasa / 12) ** 12 - 1
    raise ErrorFinanciero(f"tipo de tasa de descuento {tipo!r}: declarar uno de {TIPOS_TASA_DESCUENTO}")


def umbral_evidencia(filas=None):
    """UMBRAL_EVIDENCIA_PUBLICACION desde inputs_financieros.csv; si la fila no existe, default conservador."""
    filas = filas if filas is not None else leer_inputs()
    f = [x for x in filas if x["ESCENARIO"] == "EVIDENCIA" and x["VARIABLE"] == "umbral_evidencia_publicacion"]
    if not f or not f[0]["VALOR"].strip():
        return UMBRAL_EVIDENCIA_DEFAULT
    niv = tuple(x.strip() for x in f[0]["VALOR"].split("|") if x.strip())
    if not niv or set(niv) - set(NIVELES):
        raise ErrorFinanciero(f"umbral_evidencia_publicacion inválido: {f[0]['VALOR']!r} (niveles {NIVELES})")
    return niv


def resolver(variable, modo, evidencia=None, usuario=None, supuesto=None, umbral=None):
    """Jerarquía EVIDENCIA_REAL > ESCENARIO_USUARIO > SUPUESTO_MODELO > PENDIENTE.
    evidencia = (valor, nivel, fuente); usuario = valor; supuesto = (valor, fuente).
    Devuelve (valor, origen, nivel, fuente). El valor de escenario nunca reemplaza a una evidencia válida."""
    if modo not in MODOS:
        raise ErrorFinanciero(f"modo {modo!r} inválido")
    ev_ok = evidencia is not None and evidencia[0] is not None and (
        evidencia[1] in (umbral or UMBRAL_EVIDENCIA_DEFAULT) or ("M09" in _MUT and evidencia[1] == "E4"))
    if "M10" in _MUT and modo == "ESCENARIO" and usuario is not None:
        return usuario, "ESCENARIO_USUARIO", "", "usuario"
    if ev_ok:
        return evidencia[0], "EVIDENCIA_REAL", evidencia[1], evidencia[2]
    if modo == "ESCENARIO" and usuario is not None:
        return usuario, "ESCENARIO_USUARIO", "", "escenario del usuario"
    if supuesto is not None and supuesto[0] is not None and (modo == "ESCENARIO" or variable in SUPUESTOS_METODOLOGICOS):
        return supuesto[0], "SUPUESTO_MODELO", "", supuesto[1]
    return None, "PENDIENTE", "", ""


# ---------------------------------------------------------------------------------------------
# 2. PRODUCTOS VENDIBLES (balance de masa 04 agrupado con ITEMS de 23; rutas exclusivas)
# ---------------------------------------------------------------------------------------------
def productos_balance(config_producto="B", rutas=None, destino_c="venta_directa"):
    """kg COMERCIALES por ave (masa biológica + agua retenida) de cada producto vendible, para el peso de
    referencia (2,9 kg, único que publican 03/14B). Las rutas esqueleto/cuello/hueso/piel son EXCLUSIVAS (las
    resuelve el balance: un material se vende O se reprocesa). La masa clase C se vende cruda O va a rendering
    propio, nunca ambas. `cms_alternativa_no_sumable` de 23 no se usa nunca."""
    if destino_c not in DESTINOS_C:
        raise ErrorFinanciero(f"destino de subproductos C {destino_c!r} inválido {DESTINOS_C}")
    b = mb.balance(me.PESO_REF, config_producto, me.REND, me.COND, me.ENF, rutas)
    mb.verificar_cierre(b)
    out = {}
    for clave, nombre, comps in me.ITEMS:
        kg = sum(f["bio"] + f["agua"] for f in b["filas"] if f["componente"] in comps)
        cat = CATEGORIA_PRODUCTO[clave]
        if cat is None:
            continue
        if cat == "SUBPRODUCTOS" and destino_c == "rendering_propio" and "M11" not in _MUT:
            kg = 0.0                               # la masa C entra al rendering: no se vende cruda
        if cat == "SUBPRODUCTOS" and destino_c == "contrato_facon":
            kg = None                              # façon: destino y propiedad de subproductos según contrato (FAE-FACON-SUB)
        out[clave] = {"kg_ave": kg, "categoria_ingreso": cat, "nombre": nombre}
    if "M11" in _MUT:                              # mutación: monetiza esqueleto vendido y su CMS a la vez
        out["cms"]["kg_ave"] += out["carcasa_esqueleto"]["kg_ave"] * mb.CMS_RENDIMIENTO[me.REND]
    out[PRODUCTO_RENDERING] = {"kg_ave": None if destino_c == "rendering_propio" else 0.0,
                               "categoria_ingreso": "RENDERING",
                               "nombre": "Harinas y grasas de rendering propio (rendimiento PENDIENTE, DPV-065)"}
    meta = {"peso_vivo": b["entrada_bio"], "agua_incorporada": b["entrada_agua"], "config_producto": config_producto,
            "rutas": b["rutas"], "destino_c": destino_c}
    return out, meta


# ---------------------------------------------------------------------------------------------
# 3. ENTRADA DEL MOTOR (valores ya resueltos; None = PENDIENTE, nunca 0)
# ---------------------------------------------------------------------------------------------
def entrada_vacia(nombre="sin_nombre", modo="ESCENARIO"):
    """Estructura completa de inputs del motor. Todo lo económico empieza en None (PENDIENTE)."""
    return {
        "nombre": nombre, "modo": modo, "configuracion": "", "trayectoria": "",
        "fecha_inicio": None,                      # AAAA-MM-DD; solo rotula fechas (no bloquea el cálculo)
        "horizonte_anios": None, "meses_detalle": 24,
        "meses_preoperacion": None, "meses_construccion": None, "meses_commissioning": None,
        "modelo_monetario": "REAL", "inflacion_anual": None, "base_tasa": "REAL",
        "tasa_descuento": None, "tasa_descuento_accionista": None, "tasa_reinversion": None,
        "tipo_tasa_descuento": "EFECTIVA_ANUAL", "convencion_descuento": "MENSUAL",
        "umbral_evidencia": UMBRAL_EVIDENCIA_DEFAULT,
        "etapas": [],
        "productos": None, "validacion_rendimientos": False, "meta_productos": {},
        "demanda": None, "categorias_demanda_usadas": CATEGORIAS_DEMANDA_EVIDENCIA, "alfa_negociada": None,
        "precios": {}, "canales": {}, "inventario_max_meses": {},
        "inventarios": None, "dias_caja_operativa": None,
        "impuestos": {"tasa_ganancias": None, "anios_quebranto": None, "pct_iibb": None,
                      "pct_tasas_municipales": None, "otros_impuestos_usd_anio": None, "intereses_deducibles": True,
                      # base del IIBB separada (TF-005): None = regla PENDIENTE (no se asume alcanzado ni exento)
                      "iibb_aplica_domestico": None, "iibb_aplica_exportacion": None},
        "iva": {"modo": None, "alicuota_ventas": None, "alicuota_compras": None, "alicuota_capex": None},
        "financiamiento": None,
        "valor_terminal": {"metodo": "SIN_VALOR_TERMINAL", "monto": None, "g": None, "recuperar_ct": False},
        "stress": {},
        "override_total": False,                   # OVERRIDE_TOTAL_ARQUITECTURA declarado por el usuario (TF-004)
    }


def etapa_vacia(id_etapa, escala, dias, tipo="INICIAL"):
    return {"id": id_etapa, "escala_aves_dia": escala, "dias_operativos_anio": dias,
            "entrada": {"tipo": tipo, "mes": None, "condiciones": {}, "logica": "TODAS", "meses_consecutivos": 1,
                        "meses_obra": None},
            "capex_usd": None, "curva_desembolso": None, "rampup": None, "opex_rubros": None, "activos": None,
            "tipo_capex": "INICIAL" if tipo == "INICIAL" else "EXPANSION",
            # IVA del CAPEX de la etapa (TF-076): crédito fiscal solo con declaración completa (iva_capex_declarado())
            "iva_capex": None,
            # módulos OPEX de la arquitectura que un OPEX de usuario debe cubrir (TF-004); None = OPEX del módulo 20
            "opex_modulos_requeridos": None}


BLOQUES = ("TIEMPO", "RAMPUP", "PRODUCCION", "DEMANDA", "PRECIOS", "CANALES", "OPEX", "IMPUESTOS_INGRESOS",
           "CAPEX", "DEPRECIACION", "REPOSICION", "CT", "IVA", "GANANCIAS", "FINANCIAMIENTO", "DESCUENTO",
           "VALOR_TERMINAL")


def validar_entrada(P):
    """Errores ESTRUCTURALES (se detiene). Los faltantes de datos no son error: los informa disponibilidad()."""
    if P["modo"] not in MODOS:
        raise ErrorFinanciero(f"modo {P['modo']!r}")
    if P["modelo_monetario"] not in ("REAL", "NOMINAL"):
        raise ErrorFinanciero("modelo_monetario: REAL | NOMINAL")
    if P["base_tasa"] != P["modelo_monetario"]:
        raise ErrorFinanciero(f"tasa de descuento {P['base_tasa']} con flujos {P['modelo_monetario']}: no se mezclan "
                              "(convertir la tasa con Fisher de forma explícita antes de cargarla)")
    if P["modelo_monetario"] == "REAL" and P["inflacion_anual"] not in (None, 0):
        raise ErrorFinanciero("modelo REAL: no se carga inflación (DEC-006)")
    for k, v in P["precios"].items():
        if v and v.get("tipo") == "SERIE" and v.get("base", "REAL") != P["modelo_monetario"]:
            raise ErrorFinanciero(f"precio {k}: serie {v.get('base')} en modelo {P['modelo_monetario']}")
    if P["stress"] and P["modo"] != "ESCENARIO":
        raise ErrorFinanciero("el modo stress solo existe en MODO ESCENARIO")
    if set(P["stress"] or {}) - set(CLAVES_STRESS):
        raise ErrorFinanciero(f"claves de stress admitidas: {CLAVES_STRESS}")
    dv = (P["stress"] or {}).get("devaluacion")
    if dv is not None and (dv.get("pct") is None or dv.get("traslado_precios_ars") is None):
        raise ErrorFinanciero("devaluación: declarar pct y traslado_precios_ars (no se supone traslado)")
    if P["meses_detalle"] is None or P["meses_detalle"] % 12 or P["meses_detalle"] < 0:
        raise ErrorFinanciero("meses_detalle: múltiplo de 12 ≥ 0")
    if P["horizonte_anios"] is not None and (int(P["horizonte_anios"]) != P["horizonte_anios"] or P["horizonte_anios"] < 1
                                             or P["meses_detalle"] > 12 * P["horizonte_anios"]):
        raise ErrorFinanciero("horizonte entero ≥ 1 y ≥ meses de detalle")
    if P["convencion_descuento"] not in CONVENCIONES_DESCUENTO:
        raise ErrorFinanciero(f"convención de descuento: {CONVENCIONES_DESCUENTO}")
    if P["tipo_tasa_descuento"] not in TIPOS_TASA_DESCUENTO:
        raise ErrorFinanciero(f"tipo de tasa de descuento: {TIPOS_TASA_DESCUENTO}")
    if set(P["impuestos"]) - set(CLAVES_IMPUESTOS):
        raise ErrorFinanciero(f"claves de impuestos no admitidas {sorted(set(P['impuestos']) - set(CLAVES_IMPUESTOS))}: "
                              "los derechos de exportación se cargan SOLO en canales.exportacion.pct_derechos_exportacion "
                              "(deducción de la venta; ubicación única para evitar doble conteo)")
    for c_, ch in (P["canales"] or {}).items():
        if c_ != "exportacion" and ch and ch.get("pct_derechos_exportacion") is not None:
            raise ErrorFinanciero("derechos de exportación solo en el canal exportacion")
    for k in ("iibb_aplica_domestico", "iibb_aplica_exportacion"):
        if P["impuestos"].get(k) not in (None, True, False):
            raise ErrorFinanciero(f"{k}: TRUE / FALSE / vacío (PENDIENTE); no se admite otro valor")
    if P["valor_terminal"]["metodo"] not in METODOS_VT:
        raise ErrorFinanciero(f"valor terminal: {METODOS_VT}")
    prev = 0
    for i, e in enumerate(P["etapas"]):
        t = e["entrada"]["tipo"]
        if (i == 0) != (t == "INICIAL"):
            raise ErrorFinanciero("la primera etapa es INICIAL y solo ella")
        if t not in ("INICIAL", "FECHA", "CONDICION"):
            raise ErrorFinanciero(f"entrada {t}")
        if e["escala_aves_dia"] is not None:
            if e["escala_aves_dia"] <= prev:
                raise ErrorFinanciero("las escalas de una trayectoria son crecientes (capacidad acumulada)")
            prev = e["escala_aves_dia"]
        if e["curva_desembolso"] is not None and abs(sum(f for _, f in e["curva_desembolso"]) - 1) > 1e-6:
            raise ErrorFinanciero(f"curva de desembolso de {e['id']} no suma 1")
        if t == "CONDICION" and set(e["entrada"]["condiciones"]) - set(GATILLOS):
            raise ErrorFinanciero(f"gatillos admitidos: {GATILLOS}")
        for r in e["opex_rubros"] or []:
            if r["naturaleza"] not in NATURALEZAS:
                raise ErrorFinanciero(f"naturaleza {r['naturaleza']}")
        if e["activos"] is not None and e["capex_usd"] is not None:
            tot = sum(a["capex_usd"] for a in e["activos"] if a["capex_usd"] is not None)
            if all(a["capex_usd"] is not None for a in e["activos"]) and abs(tot - e["capex_usd"]) > 1e-6 * max(1, e["capex_usd"]):
                raise ErrorFinanciero(f"Σ activos ({tot}) ≠ CAPEX de la etapa {e['id']} ({e['capex_usd']})")
    if P["productos"]:
        for l in P["demanda"] or []:
            if l["producto"] not in P["productos"]:
                raise ErrorFinanciero(f"demanda de producto inexistente en el balance: {l['producto']}")
            if l["categoria"] not in CATEGORIAS_DEMANDA:
                raise ErrorFinanciero(f"categoría de demanda {l['categoria']}")
            if l["canal"] not in CANALES:
                raise ErrorFinanciero(f"canal {l['canal']} no admitido {CANALES}")
        masa = sum(p["kg_ave"] for p in P["productos"].values() if p["kg_ave"])
        lim = P["meta_productos"].get("peso_vivo", math.inf) + P["meta_productos"].get("agua_incorporada", 0)
        if masa > lim + 1e-9:
            raise ErrorFinanciero(f"productos vendibles ({masa:.4f} kg/ave) superan la masa del ave ({lim:.4f}): doble conteo")
    if P["financiamiento"]:
        for d in P["financiamiento"].get("deudas", []):
            if d["metodo"] not in METODOS_DEUDA:
                raise ErrorFinanciero(f"método de deuda {d['metodo']}")
            if d.get("moneda", "USD") != "USD":
                raise ErrorFinanciero("deuda en moneda distinta de USD: cargar con TC explícito (módulo de moneda)")
            if d.get("base_tasa") != P["modelo_monetario"]:
                raise ErrorFinanciero(f"deuda {d.get('id')}: base de la tasa {d.get('base_tasa')!r} ≠ modelo "
                                      f"{P['modelo_monetario']} (no se convierte en silencio)")
    return P


def _lineas_contables(P):
    """Líneas de demanda que el modo permite vender (separadas por categoría; nunca A+B+C+D)."""
    out = []
    for l in P["demanda"] or []:
        if l["categoria"] not in P["categorias_demanda_usadas"]:
            continue
        if P["modo"] == "EVIDENCIA" and l["categoria"] not in CATEGORIAS_DEMANDA_EVIDENCIA:
            continue
        if l["categoria"] == "NEGOCIADA" and P["alfa_negociada"] is None:
            continue
        out.append(l)
    return out


def _clave_precio(l):
    return f"{l['producto']}|{l['canal']}|{l.get('mercado', 'INTERNO')}"


def iva_capex_declarado(d):
    """(True, "") solo si la etapa declara EXPLÍCITAMENTE el IVA de su CAPEX (TF-076): base neta (sin IVA), IVA
    declarado, tasa, condición fiscal y elegibilidad al crédito con su criterio. Un IVA DESCONOCIDO / INCIERTO /
    NO_DECLARADO no genera crédito fiscal ni se convierte en costo: queda CREDITO_FISCAL_IVA_CAPEX = PENDIENTE."""
    if not d:
        return False, "sin declaración de IVA del CAPEX"
    estado = str(d.get("iva_estado") or "NO_DECLARADO").upper()
    if estado in ESTADOS_IVA_CAPEX_INCIERTO or estado != "DECLARADO":
        return False, f"IVA del CAPEX {estado}"
    falt = [k for k in ("condicion_fiscal", "criterio") if not d.get(k)]
    if d.get("base") != "NETA":
        falt.append("base NETA (sin IVA)")
    if not isinstance(d.get("tasa"), (int, float)) or d["tasa"] < 0:
        falt.append("tasa")
    if d.get("elegible_credito") is not True:
        falt.append("elegible_credito = TRUE")
    return (not falt), ("falta " + ", ".join(falt)) if falt else ""


def estado_bloques(P, F=None):
    """Estado de cada bloque del motor (TF-011): CON_EVIDENCIA (completo con datos presentes para el modo) ·
    PENDIENTE (tiene faltantes) · VACIO (sin faltantes declarados pero sin contenido: no es evidencia) · NO_APLICA
    (el bloque no corresponde: puede salir del denominador). Un bloque VACIO o PENDIENTE nunca suma al numerador."""
    F = F if F is not None else disponibilidad(P)
    out = {}
    vt = P["valor_terminal"]
    etapas = P["etapas"] or []
    hay_activos = bool(etapas) and all(e["activos"] for e in etapas)
    N = 12 * P["horizonte_anios"] if P["horizonte_anios"] else None
    for b in BLOQUES:
        if F[b]:
            out[b] = "PENDIENTE"
        elif b == "VALOR_TERMINAL":
            out[b] = "NO_APLICA" if vt["metodo"] == "SIN_VALOR_TERMINAL" and not vt.get("recuperar_ct") else "CON_EVIDENCIA"
        elif b == "REPOSICION":
            if not hay_activos:
                out[b] = "VACIO"           # sin activos declarados no hay faltante… ni contenido
            else:
                rep_ = [a for e in etapas for a in e["activos"] if a.get("depreciable", True) and N
                        and (a.get("vida_util_anios") or 0) * 12 < N]
                out[b] = "CON_EVIDENCIA" if rep_ else "NO_APLICA"
        elif b == "IVA" and P["iva"]["modo"] == "EXCLUIDO":
            out[b] = "NO_APLICA"
        elif b == "FINANCIAMIENTO" and not (P["financiamiento"] or {}).get("deudas") and not (P["financiamiento"] or {}).get("aportes"):
            out[b] = "VACIO"
        else:
            out[b] = "CON_EVIDENCIA"
    return out


def cobertura_bloques(estados):
    """Cobertura = bloques CON_EVIDENCIA ÷ bloques aplicables (todos menos NO_APLICA). None si nada aplica."""
    aplic = [b for b, e in estados.items() if e != "NO_APLICA"]
    return (sum(1 for b in aplic if estados[b] == "CON_EVIDENCIA") / len(aplic)) if aplic else None


def disponibilidad(P):
    """Qué falta, por bloque. Lista vacía = bloque completo para el modo."""
    F = {b: [] for b in BLOQUES}
    H = P["horizonte_anios"]
    if H is None:
        F["TIEMPO"].append("horizonte de evaluación (DEC-007; 10 / 15 / 20 años como escenarios, ninguno elegido)")
    for k, txt in (("meses_preoperacion", "preoperación"), ("meses_construccion", "construcción"),
                   ("meses_commissioning", "commissioning")):
        if P[k] is None:
            F["TIEMPO"].append(f"duración de {txt} (DPV-086)")
    if not P["etapas"]:
        F["PRODUCCION"].append("sin etapa de capacidad (escala no elegida: DEC-001, DEC-033)")
    N = 12 * H if H else None
    for e in P["etapas"]:
        eid = e["id"]
        if e["escala_aves_dia"] is None or e["dias_operativos_anio"] is None:
            F["PRODUCCION"].append(f"{eid}: escala o días operativos")
        if e["entrada"]["tipo"] == "FECHA" and e["entrada"]["mes"] is None:
            F["TIEMPO"].append(f"{eid}: mes de entrada en operación")
        if e["entrada"]["tipo"] == "CONDICION" and e["entrada"]["meses_obra"] is None:
            F["TIEMPO"].append(f"{eid}: meses de obra desde el gatillo (DPV-086)")
        if not e["rampup"]:
            F["RAMPUP"].append(f"{eid}: curva de ramp-up (DEC-090)")
        else:
            for r in e["rampup"]:
                if r.get("utilizacion") is None:
                    F["RAMPUP"].append(f"{eid}: utilización del mes {r.get('mes')}")
                    break
            for campo in ("merma", "eficiencia", "costos_extra_usd_mes"):
                if any(r.get(campo) is None for r in e["rampup"]):
                    F["RAMPUP"].append(f"{eid}: {campo} del ramp-up (ineficiencias del arranque, DEC-090)")
        if e["capex_usd"] is None:
            F["CAPEX"].append(f"{eid}: CAPEX total de la etapa ({e.get('motivo_capex', 'sin total publicable')})")
        if e["curva_desembolso"] is None:
            F["CAPEX"].append(f"{eid}: CURVA_DE_DESEMBOLSO_CAPEX (cronograma de obra y anticipos, DPV-086, DPV-167)")
        if e["opex_rubros"] is None:
            F["OPEX"].append(f"{eid}: OPEX por rubro ({e.get('motivo_opex', 'sin total publicable')})")
        else:
            req_mod = e.get("opex_modulos_requeridos")
            if req_mod:
                cubiertos = {(r.get("meta") or {}).get("MODULO") for r in e["opex_rubros"]}
                faltan = sorted(set(req_mod) - cubiertos)
                if faltan:
                    F["OPEX"].append(f"{eid}: OPEX del usuario sin rubros de los módulos {', '.join(faltan)} de la "
                                     "arquitectura (completitud TF-004: una arquitectura incompleta no gana por costos faltantes)")
            for r in e["opex_rubros"]:
                if r["costo_pleno_usd_anio"] is None:
                    F["OPEX"].append(f"{eid}: rubro {r['rubro']} sin costo")
                if r["naturaleza"] == "semivariable" and r.get("pct_variable") is None:
                    F["OPEX"].append(f"{eid}: rubro {r['rubro']} semivariable sin % variable")
                if r.get("es_compra") and r.get("dias_pago") is None:
                    F["CT"].append(f"{eid}: días de pago de {r['rubro']} (DPV-175)")
        if e["activos"] is None:
            F["DEPRECIACION"].append(f"{eid}: activos por clase con vida útil y valor residual (DPV-167, DPV-169)")
        else:
            for a in e["activos"]:
                if a.get("depreciable", True):
                    if a.get("vida_util_anios") is None or a.get("valor_residual_usd") is None:
                        F["DEPRECIACION"].append(f"{eid}: vida útil / valor residual de {a['clase']}")
                    elif N and a["vida_util_anios"] * 12 < N and a.get("costo_reemplazo_usd") is None:
                        F["REPOSICION"].append(f"{eid}: costo de reemplazo de {a['clase']} (vida < horizonte; DPV-167)")
    if P["productos"] is None:
        F["PRODUCCION"].append("productos vendibles por ave (balance de masa)")
    elif P["modo"] == "EVIDENCIA" and not P["validacion_rendimientos"]:
        F["PRODUCCION"].append("rendimientos del balance 04 v1.1 sin ensayo en planta (DPV-060, DEC-028)")
    if P["demanda"] is None:
        F["DEMANDA"].append("sin demanda contable: demanda A+B documentada ≈ 0 y no cuantificada (DPV-002, DPV-020, "
                            "DPV-037, DPV-040); los ~90 supermercados son canal potencial, no clientes")
    else:
        lineas = _lineas_contables(P)
        if not lineas:
            F["DEMANDA"].append("ninguna línea de demanda en categorías vendibles para el modo")
        for l in lineas:
            q = l["kg_mes"]
            if q is None or (isinstance(q, dict) and H and any(q["por_anio"].get(y) is None for y in range(1, H + 1))):
                F["DEMANDA"].append(f"{l['id']}: volumen")
            prod = P["productos"].get(l["producto"]) if P["productos"] else None
            if prod is not None and prod["kg_ave"] is None:
                F["PRODUCCION"].append(f"{l['producto']}: rendimiento PENDIENTE (DPV-065)")
            if prod is not None and prod["kg_ave"] == 0:
                continue                           # producto no producido por esta ruta: no necesita precio
            pr = P["precios"].get(_clave_precio(l))
            if pr is None and "M01" not in _MUT:
                F["PRECIOS"].append(f"precio {_clave_precio(l)} (DPV-013, DPV-039, DPV-070)")
            elif pr is not None and pr.get("tipo") == "SERIE" and H and any(pr["por_anio"].get(y) is None for y in range(1, H + 1)):
                F["PRECIOS"].append(f"precio {_clave_precio(l)}: serie incompleta (no se extrapola)")
            ch = P["canales"].get(l["canal"])
            req = ["pct_descuentos", "pct_bonificaciones", "pct_devoluciones", "pct_comisiones", "costo_logistico_usd_kg"]
            if l.get("mercado", "INTERNO") != "INTERNO":
                req += ["pct_derechos_exportacion", "costo_exportacion_usd_kg"]
            if ch is None or any(ch.get(c) is None for c in req):
                F["CANALES"].append(f"canal {l['canal']}: condiciones comerciales {req} (DPV-039)")
            if ch is None or ch.get("dias_cobro") is None:
                F["CT"].append(f"canal {l['canal']}: días de cobro (DPV-175)")
    if P["demanda"] is None or not _lineas_contables(P):
        if not P["precios"]:
            F["PRECIOS"].append("ningún precio de venta con evidencia E1–E3 en base_precios_venta.csv (DPV-013, DPV-039, DPV-070)")
        if not P["canales"]:
            F["CANALES"].append("condiciones comerciales por canal: descuentos, bonificaciones, devoluciones, comisiones, "
                                "logística, plazos (DPV-039)")
            F["CT"].append("días de cobro por canal (DPV-175)")
    imp = P["impuestos"]
    for k in ("pct_iibb", "pct_tasas_municipales", "otros_impuestos_usd_anio"):
        if imp.get(k) is None:
            F["IMPUESTOS_INGRESOS"].append(f"{k} (DPV-043)")
    if imp.get("pct_iibb"):                           # TF-005: con alícuota > 0, la base exige regla por mercado
        lc = _lineas_contables(P) if P["demanda"] is not None else []
        for flag, hay in (("iibb_aplica_domestico", any(l.get("mercado", "INTERNO") == "INTERNO" for l in lc)),
                          ("iibb_aplica_exportacion", any(l.get("mercado", "INTERNO") != "INTERNO" for l in lc))):
            if hay and imp.get(flag) is None:
                F["IMPUESTOS_INGRESOS"].append(f"{NO_CALC_FISCAL}: {flag} (jurisdicción y tratamiento de la base; "
                                               "no se asume alcanzada ni exenta; DPV-043, DPV-169)")
    for k in ("tasa_ganancias", "anios_quebranto"):
        if imp.get(k) is None:
            F["GANANCIAS"].append(f"{k} (DPV-169)")
    if P["inventarios"] is None:
        F["CT"].append("días de stock y propiedad por categoría de inventario (DPV-175, DEC-089, DEC-091)")
    else:
        for cat, x in P["inventarios"].items():
            if cat not in CATEGORIAS_INVENTARIO:
                raise ErrorFinanciero(f"categoría de inventario {cat}")
            if x.get("propiedad_empresa") is None:
                F["CT"].append(f"inventario {cat}: propiedad PENDIENTE (DEC-024)")
            elif x["propiedad_empresa"] and x.get("dias") is None:
                F["CT"].append(f"inventario {cat}: días de stock")
    iva = P["iva"]
    if iva["modo"] is None:
        F["IVA"].append("tratamiento del IVA (débito, crédito, saldo técnico, recupero de IVA de CAPEX; DPV-169, DPV-043)")
    elif iva["modo"] == "SIMPLIFICADO" and any(iva.get(k) is None for k in ("alicuota_ventas", "alicuota_compras")):
        F["IVA"].append("alícuotas de IVA (ventas, compras)")
    if iva["modo"] == "SIMPLIFICADO":                 # TF-076: crédito de IVA de CAPEX solo con declaración explícita
        for e in P["etapas"]:
            if e["capex_usd"] or any(a.get("costo_reemplazo_usd") for a in (e["activos"] or [])):
                ok_, mot = iva_capex_declarado(e.get("iva_capex"))
                if not ok_:
                    F["IVA"].append(f"{CREDITO_IVA_CAPEX_PEND}: {e['id']} — {mot} (base neta, IVA, tasa, condición fiscal y "
                                    "elegibilidad; el IVA incierto no es costo ni crédito; DPV-093, DPV-169)")
    if P["financiamiento"] is None:
        F["FINANCIAMIENTO"].append("estructura de financiamiento (DEC-092); USD 2 M no es capital confirmado (SUP-003)")
    if P["tasa_descuento"] is None:
        F["DESCUENTO"].append("TASA_DESCUENTO (DEC-007; no se inventa un WACC)")
    vt = P["valor_terminal"]
    if vt["metodo"] == "EXPLICITO" and vt.get("monto") is None:
        F["VALOR_TERMINAL"].append("monto del valor residual explícito")
    if vt["metodo"] == "PERPETUIDAD" and (vt.get("g") is None or P["tasa_descuento"] is None):
        F["VALOR_TERMINAL"].append("crecimiento g y tasa para la perpetuidad")
    if vt["metodo"] == "VALOR_LIBRO" and F["DEPRECIACION"]:
        F["VALOR_TERMINAL"].append("valor libro requiere depreciación completa")
    return F


def flags_calculo(F, P):
    ok = {b: not v for b, v in F.items()}
    r = {}
    r["tiempo"] = ok["TIEMPO"]
    r["fisico"] = ok["TIEMPO"] and ok["RAMPUP"] and ok["PRODUCCION"] and ok["DEMANDA"]
    r["bruto"] = r["fisico"] and ok["PRECIOS"]
    r["neto"] = r["bruto"] and ok["CANALES"]
    r["opex"] = r["fisico"] and ok["OPEX"]
    r["ebitda"] = r["neto"] and r["opex"] and ok["IMPUESTOS_INGRESOS"]
    r["capex"] = ok["TIEMPO"] and ok["CAPEX"]
    r["dep"] = ok["TIEMPO"] and ok["DEPRECIACION"]
    r["ebit"] = r["ebitda"] and r["dep"]
    r["ct"] = r["neto"] and r["opex"] and ok["CT"]
    r["iva"] = ok["IVA"] and (P["iva"]["modo"] != "SIMPLIFICADO" or (r["neto"] and r["opex"] and r["capex"]))
    r["fcff_pre"] = r["ebitda"] and r["capex"] and r["ct"] and r["iva"] and ok["REPOSICION"] and ok["VALOR_TERMINAL"]
    r["fcff_post"] = r["fcff_pre"] and r["ebit"] and ok["GANANCIAS"]
    r["fin"] = ok["FINANCIAMIENTO"]
    r["fcfe_pre"] = r["fcff_pre"] and r["fin"]
    r["fcfe_post"] = r["fcff_post"] and r["fin"]
    r["desc"] = ok["DESCUENTO"]
    if "M20" in _MUT:
        r["ebitda"] = r["neto"]                    # mutación: publica EBITDA sin OPEX completo
    return r


# ---------------------------------------------------------------------------------------------
# 4. DEUDA (cronograma independiente de la operación)
# ---------------------------------------------------------------------------------------------
def tasa_deuda_periodo(d):
    """Tasa efectiva de cada período de servicio (frecuencia f meses), según el TIPO declarado (SUP-200):
      EFECTIVA_ANUAL : (1 + TEA)^(f/12) − 1
      NOMINAL_ANUAL  : TNA × f ÷ 12, solo si la capitalización declarada coincide con la frecuencia de pago
      PERIODICA      : tasa del período, solo si su período declarado coincide con la frecuencia de pago
    Sin tipo, o con períodos que no coinciden → error (combinación ambigua bloqueada)."""
    r, f, t = d.get("tasa"), d["frecuencia_meses"], d.get("tipo_tasa")
    if r is None:
        raise ErrorFinanciero(f"deuda {d['id']}: tasa PENDIENTE")
    if "M24" in _MUT:
        return r * f / 12
    if t == "EFECTIVA_ANUAL":
        return (1 + r) ** (f / 12) - 1
    if t == "NOMINAL_ANUAL":
        if d.get("capitalizacion_meses") != f:
            raise ErrorFinanciero(f"deuda {d['id']}: TNA con capitalización {d.get('capitalizacion_meses')} ≠ frecuencia {f}: "
                                  "convención ambigua (declarar la tasa como EFECTIVA_ANUAL o PERIODICA)")
        return r * f / 12
    if t == "PERIODICA":
        if d.get("periodo_tasa_meses") != f:
            raise ErrorFinanciero(f"deuda {d['id']}: tasa periódica de {d.get('periodo_tasa_meses')} meses ≠ frecuencia {f}")
        return r
    raise ErrorFinanciero(f"deuda {d['id']}: declarar tipo_tasa {TIPOS_TASA_DEUDA}")


def cronograma_deuda(d, N):
    """saldo_ini + alta − amortización = saldo_fin, mes a mes. Interés = saldo × tasa del período de servicio
    (`tasa_deuda_periodo`, según tipo declarado) en cada fecha de pago. Gracia = solo intereses.
    Métodos: FRANCES, ALEMAN, BULLET, PERSONALIZADO."""
    z = lambda: [0.0] * (N + 1)
    alta, interes, amort, comision, s_ini, s_fin = z(), z(), z(), z(), z(), z()
    S, r, f = d["monto"], d["tasa"], d["frecuencia_meses"]
    m0, plazo, gracia = d["mes_desembolso"], d["plazo_meses"], d.get("gracia_meses", 0)
    if (plazo - gracia) % f or gracia % f or plazo <= gracia:
        raise ErrorFinanciero(f"deuda {d['id']}: plazo y gracia múltiplos de la frecuencia y plazo > gracia")
    i = tasa_deuda_periodo(d)
    n = (plazo - gracia) // f
    pagos = {}
    saldo = S
    cuota = S * i / (1 - (1 + i) ** -n) if (d["metodo"] == "FRANCES" and i > 0) else (S / n if d["metodo"] == "FRANCES" else None)
    pers = dict(d.get("cronograma", []))
    if d["metodo"] == "PERSONALIZADO" and abs(sum(pers.values()) - S) > 1e-6:
        raise ErrorFinanciero(f"deuda {d['id']}: el cronograma personalizado no suma el monto")
    for j in range(1, plazo // f + 1):
        mes = m0 + j * f
        it = saldo * i
        if j * f <= gracia:
            am = 0.0
        else:
            q = j - gracia // f
            am = {"FRANCES": (cuota - it) if cuota is not None else 0.0, "ALEMAN": S / n,
                  "BULLET": S if q == n else 0.0, "PERSONALIZADO": pers.get(j * f, 0.0)}[d["metodo"]]
            if q == n:
                am = saldo                          # cierra residuos de redondeo
        saldo -= am
        pagos[mes] = (it, am)
    saldo = 0.0
    for k in range(N + 1):
        s_ini[k] = saldo
        if k == m0:
            alta[k] = S
            comision[k] = S * d.get("comision_pct", 0.0)
        it, am = pagos.get(k, (0.0, 0.0))
        interes[k] = it
        amort[k] = am if "M18" not in _MUT else 0.0
        saldo = saldo + alta[k] - am
        s_fin[k] = saldo
    return {"id": d["id"], "alta": alta, "interes": interes, "amort": amort, "comision": comision,
            "saldo_ini": s_ini, "saldo_fin": s_fin, "saldo_al_cierre": s_fin[N] if N >= 0 else 0.0}


# ---------------------------------------------------------------------------------------------
# 5. MOTOR MENSUAL
# ---------------------------------------------------------------------------------------------
def _fila_curva(curva, n, estirar=1.0):
    """Fila vigente de una curva (MES desde la entrada de la etapa, 1-based): última fila con MES ≤ n.
    Después de la última fila rige su valor (madurez). estirar > 1 = ramp-up más lento (stress)."""
    if n < 1:
        return None
    n_ef = (n - 1) / estirar + 1
    fila = None
    for r in sorted(curva, key=lambda x: x["mes"]):
        if r["mes"] <= n_ef + 1e-9:
            fila = r
    return fila


def _meses_rampup(curva, estirar=1.0):
    return max(r["mes"] for r in curva) * estirar if curva else 0


def _kg_linea(l, k, anio):
    q = l["kg_mes"]
    if l.get("desde_mes") and k < l["desde_mes"]:
        return 0.0
    if l.get("hasta_mes") and k > l["hasta_mes"]:
        return 0.0
    if isinstance(q, dict):
        return q["por_anio"].get(anio)
    if isinstance(q, list):
        return q[k]
    return q


def _precio(spec, anio):
    if spec is None:
        return None
    if spec.get("tipo", "CONSTANTE") == "CONSTANTE":
        return spec["usd_kg"]
    return spec["por_anio"].get(anio)


def simular(P):
    """Corre el motor. Devuelve dict con faltantes por bloque, flags de cálculo, series mensuales (None = no
    calculable) y la agregación a períodos de reporte."""
    P = copy.deepcopy(P)
    validar_entrada(P)
    F = disponibilidad(P)
    ok = flags_calculo(F, P)
    R = {"P": P, "faltantes": F, "ok": ok, "notas": [], "series": {}, "periodos": [], "N": 0}
    if not ok["tiempo"] or not P["etapas"]:
        return R
    H = P["horizonte_anios"]
    N = 12 * H
    R["N"] = N
    st = P["stress"] or {}
    idx = [((1 + (P["inflacion_anual"] or 0)) ** (k / 12)) if P["modelo_monetario"] == "NOMINAL" else
           (1.02 ** (k / 12) if "M14" in _MUT else 1.0) for k in range(N + 1)]
    inicio_op = P["meses_preoperacion"] + P["meses_construccion"] + P["meses_commissioning"] + 1
    R["inicio_op"] = inicio_op
    etapas = P["etapas"]
    entrada = [None] * len(etapas)
    entrada[0] = inicio_op
    for i, e in enumerate(etapas[1:], 1):
        if e["entrada"]["tipo"] == "FECHA" and e["entrada"]["mes"] is not None:
            entrada[i] = e["entrada"]["mes"]
            if entrada[i] <= inicio_op:
                raise ErrorFinanciero(f"{e['id']}: una expansión no entra antes de la etapa inicial")
    disparo = [None] * len(etapas)
    estirar = st.get("rampup_lento_factor", 1.0)
    dv = st.get("devaluacion")
    # devaluación d con traslado p a precios en ARS: valor USD × (1 + p·d) ÷ (1 + d) (solo ítems en ARS)
    f_dev = (1 + dv["traslado_precios_ars"] * dv["pct"]) / (1 + dv["pct"]) if dv else 1.0
    lineas = _lineas_contables(P) if P["demanda"] is not None else []
    prods = P["productos"] or {}
    fin = P["financiamiento"] or {}
    deudas = [cronograma_deuda(d, N) for d in fin.get("deudas", [])]
    imp, iva_p, vt_p = P["impuestos"], P["iva"], P["valor_terminal"]
    z = lambda: [0.0] * (N + 1)
    S = {k: z() for k in (
        "capacidad_aves", "aves_disponibles", "aves_requeridas", "aves_requeridas_aseguradas", "aves_faenadas",
        "u_tecnica", "u_comercial", "u_efectiva", "kg_producidos", "kg_vendidos", "kg_excedente_sin_venta",
        "kg_inventario", "kg_merma_rampup", "venta_bruta", "descuentos", "bonificaciones", "devoluciones",
        "comisiones", "derechos_exportacion", "ingreso_neto", "opex_variable", "opex_fijo", "opex_semifijo",
        "opex_semivariable", "opex_total", "costos_extra_rampup", "costos_logistica_canal", "costos_exportacion",
        "impuestos_sobre_ingresos", "otros_impuestos", "costo_iva_capex_mutante", "ebitda", "depreciacion", "ebit",
        "capex_inicial", "capex_expansion", "capex_reposicion", "capex_total", "inv_materias_primas", "inv_alimento",
        "inv_packaging", "inv_repuestos", "inv_producto_terminado", "inv_activo_biologico", "inv_otros",
        "inventarios", "cxc", "caja_operativa", "cxp", "ct", "delta_ct", "iva_debito", "iva_credito",
        "iva_saldo_favor", "iva_pago_fisco", "flujo_iva", "impuesto_operativo", "impuesto_con_deuda",
        "valor_terminal", "fcff_pre", "fcff", "deuda_alta", "deuda_interes", "deuda_amort", "deuda_comision",
        "deuda_saldo_ini", "deuda_saldo_fin", "deuda_remanente_cierre", "fcfe_pre", "fcfe", "aportes",
        "dividendos", "caja", "cfads", "servicio_deuda", "valor_libro",
        "venta_bruta_domestica", "venta_bruta_exportacion", "iva_credito_capex", "iva_capex_pendiente_base")}
    iva_capex_ok = {e["id"]: (iva_capex_declarado(e.get("iva_capex"))[0], (e.get("iva_capex") or {}).get("tasa")) for e in etapas}
    for c in CATEGORIAS_INGRESO:
        S[f"venta_{c}"] = z()
    S["fase"] = [""] * (N + 1)
    S["fase"][0] = "T0"
    por_linea = {l["id"]: {"kg": z(), "bruto": z(), "neto": z()} for l in lineas}
    lotes = {p: [] for p in prods}                 # inventario FIFO: [edad_meses, kg]
    saldo_favor = 0.0
    quebr_u, quebr_l = [], []                      # quebrantos: [año, monto]
    activos_vivos = []                             # [costo, residual, vida_meses, inicio, depreciable, clase, etapa, costo_reemplazo]
    caja = 0.0
    hist_u = []
    for k in range(N + 1):
        anio = (k - 1) // 12 + 1 if k >= 1 else 1
        # --- gatillos de expansión (estado hasta k-1) ---
        for i, e in enumerate(etapas):
            if i == 0 or entrada[i] is not None or e["entrada"]["tipo"] != "CONDICION" or k == 0:
                continue
            cond = e["entrada"]["condiciones"]
            res, n_c = [], e["entrada"].get("meses_consecutivos", 1)
            for g, umbral in cond.items():
                if g == "utilizacion_min":
                    v = ok["fisico"] and len(hist_u) >= n_c and all(u >= umbral - 1e-12 for u in hist_u[-n_c:])
                elif g == "factor_demanda_capacidad_min":
                    v = ok["fisico"] and k > 1 and S["u_comercial"][k - 1] >= umbral
                elif g == "demanda_asegurada_min":
                    v = ok["fisico"] and k > 1 and S["capacidad_aves"][k - 1] > 0 and \
                        S["aves_requeridas_aseguradas"][k - 1] / S["capacidad_aves"][k - 1] >= umbral
                elif g == "caja_min_usd":
                    v = (ok["fcfe_post"] or ok["fcfe_pre"]) and k > 1 and S["caja"][k - 1] >= umbral
                elif g == "dscr_min":
                    sv = sum(S["servicio_deuda"][max(1, k - 12):k])
                    v = (ok["fcfe_post"] or ok["fcfe_pre"]) and sv > 0 and sum(S["cfads"][max(1, k - 12):k]) / sv >= umbral
                elif g == "anio_min":
                    v = anio >= umbral
                res.append(bool(v))
            disparar = all(res) if e["entrada"].get("logica", "TODAS") == "TODAS" else any(res)
            if disparar and entrada[i - 1] is not None and entrada[i - 1] < k:
                disparo[i] = k - 1
                entrada[i] = k - 1 + e["entrada"]["meses_obra"] + 1 if "M15" not in _MUT else k
                for off, _ in e["curva_desembolso"] or []:
                    if entrada[i] + off < k:
                        raise ErrorFinanciero(f"{e['id']}: la curva de desembolso empieza antes del gatillo (mes {k - 1})")
                R["notas"].append(f"{e['id']}: gatillo cumplido al cierre del mes {k - 1}; entra en operación el mes {entrada[i]}")
        # --- fase ---
        if k >= 1:
            pm, cm, mm = P["meses_preoperacion"], P["meses_construccion"], P["meses_commissioning"]
            if k <= pm:
                S["fase"][k] = "PREOPERACION"
            elif k <= pm + cm:
                S["fase"][k] = "CONSTRUCCION"
            elif k < inicio_op:
                S["fase"][k] = "COMMISSIONING"
            else:
                activas = [i for i in range(len(etapas)) if entrada[i] is not None and entrada[i] <= k]
                en_ramp = any(e["rampup"] and k - entrada[i] + 1 <= _meses_rampup(e["rampup"], estirar)
                              for i, e in enumerate(etapas) if i in activas)
                S["fase"][k] = "RAMP_UP" if en_ramp else "OPERACION_MADURA"
        # --- CAPEX (inicial / expansión) y reposición ---
        for i, e in enumerate(etapas):
            if entrada[i] is None or not e["curva_desembolso"] or e["capex_usd"] is None:
                continue
            for off, fr in e["curva_desembolso"]:
                if entrada[i] + off == k:
                    if k < 0:
                        raise ErrorFinanciero("desembolso antes de T0")
                    monto = e["capex_usd"] * fr * idx[k] * st.get("capex", 1.0)
                    S["capex_inicial" if i == 0 else "capex_expansion"][k] += monto
                    ok_iva, tasa_iva = iva_capex_ok[e["id"]]
                    if ok_iva:                     # TF-076: crédito solo con IVA declarado (base neta, tasa, elegible)
                        S["iva_credito_capex"][k] += monto * tasa_iva
                    else:
                        S["iva_capex_pendiente_base"][k] += monto   # informativo: ni costo ni crédito
        if any(entrada[i] + off < 0 for i, e in enumerate(etapas) if entrada[i] is not None
               for off, _ in (e["curva_desembolso"] or [])):
            raise ErrorFinanciero("la curva de desembolso cae antes de T0")
        for i, e in enumerate(etapas):
            if entrada[i] == k and e["activos"] is not None:
                for a in e["activos"]:
                    if a["capex_usd"] is None:
                        continue
                    vida = (a.get("vida_util_anios") or 0) * 12
                    activos_vivos.append([a["capex_usd"] * st.get("capex", 1.0) * idx[k], a.get("valor_residual_usd") or 0.0,
                                          vida, k, a.get("depreciable", True) and vida > 0, a["clase"], e["id"],
                                          a.get("costo_reemplazo_usd")])
        nuevos = []
        for a in activos_vivos:
            if a[4] and a[2] > 0 and k == a[3] + a[2] and a[7] is not None:
                costo_r = a[7] * idx[k] * st.get("capex", 1.0)
                S["capex_reposicion"][k] += costo_r
                ok_iva, tasa_iva = iva_capex_ok.get(a[6], (False, None))
                if ok_iva:
                    S["iva_credito_capex"][k] += costo_r * tasa_iva
                else:
                    S["iva_capex_pendiente_base"][k] += costo_r
                nuevos.append([costo_r, a[1], a[2], k, True, a[5] + " (reposición)", a[6], a[7]])
        activos_vivos += nuevos
        dep = 0.0
        for a in activos_vivos:
            if a[4] and a[3] <= k < a[3] + a[2]:
                dep += (a[0] - a[1]) / a[2]
        S["depreciacion"][k] = dep
        S["valor_libro"][k] = sum(a[0] - (((a[0] - a[1]) / a[2]) * min(max(k - a[3] + 1, 0), a[2]) if a[4] else 0.0)
                                  for a in activos_vivos if not (a[4] and k >= a[3] + a[2] and a[7] is not None))
        S["capex_total"][k] = S["capex_inicial"][k] + S["capex_expansion"][k] + S["capex_reposicion"][k]
        # --- operación ---
        activas = [i for i in range(len(etapas)) if entrada[i] is not None and entrada[i] <= k and k >= 1]
        opex_mes, rub_mes = 0.0, {}
        if activas:
            a_ = activas[-1]
            ea = etapas[a_]
            dias = ea["dias_operativos_anio"]
            cap = ea["escala_aves_dia"] * dias / 12
            disp, merma_w, ef_w, extra = 0.0, 0.0, 0.0, 0.0
            prev_esc = 0
            for i in activas:
                e = etapas[i]
                incr = (e["escala_aves_dia"] - prev_esc) * dias / 12
                prev_esc = e["escala_aves_dia"]
                fila = _fila_curva(e["rampup"] or [], k - entrada[i] + 1, estirar) or {}
                u_i = fila.get("utilizacion") or 0.0
                disp += incr * u_i
                merma_w += incr * u_i * (fila.get("merma") or 0.0)
                ef_w += incr * u_i * (fila.get("eficiencia") if fila.get("eficiencia") is not None else 1.0)
                extra += (fila.get("costos_extra_usd_mes") or 0.0) * idx[k]
            merma = merma_w / disp if disp > 0 else 0.0
            ef = ef_w / disp if disp > 0 else 1.0
            # demanda (kg/mes) por producto, solo líneas contables
            D, D_aseg = {}, {}
            for l in lineas:
                q = _kg_linea(l, k, anio) or 0.0
                q *= st.get("demanda", 1.0)
                if l["categoria"] == "NEGOCIADA":
                    q *= P["alfa_negociada"]
                if st.get("corte_exportacion_desde_mes") and k >= st["corte_exportacion_desde_mes"] and \
                        l.get("mercado", "INTERNO") != "INTERNO":
                    q = 0.0
                l["_q"] = q
                if not l.get("toma_todo"):
                    D[l["producto"]] = D.get(l["producto"], 0.0) + q
                    if l["categoria"] in CATEGORIAS_DEMANDA_EVIDENCIA:
                        D_aseg[l["producto"]] = D_aseg.get(l["producto"], 0.0) + q
            inv_p = {p: sum(x[1] for x in lotes[p]) for p in prods}

            def _req(dd):
                r_ = 0.0
                for p, q in dd.items():
                    kg = prods[p]["kg_ave"]
                    if not kg:
                        if q > 0 and kg == 0:
                            R["notas"].append(f"demanda de {p} sin producción en esta ruta del balance (mes {k})") \
                                if len(R["notas"]) < 200 else None
                        continue
                    r_ = max(r_, max(0.0, q - inv_p[p]) / (kg * (1 - merma)))
                return r_
            req = _req(D)
            aves = min(disp, req) if "M02" not in _MUT else disp
            S["capacidad_aves"][k], S["aves_disponibles"][k] = cap, disp
            S["aves_requeridas"][k], S["aves_faenadas"][k] = req, aves
            S["aves_requeridas_aseguradas"][k] = _req(D_aseg)
            S["u_tecnica"][k], S["u_comercial"][k], S["u_efectiva"][k] = disp / cap, req / cap, aves / cap
            hist_u.append(aves / cap)
            # producción, ventas, inventario (FIFO; el inventario desplaza ventas, nunca crea producto)
            for p, pr in prods.items():
                kg_ave = pr["kg_ave"] or 0.0
                prod_kg = aves * kg_ave * (1 - merma)
                S["kg_producidos"][k] += prod_kg
                S["kg_merma_rampup"][k] += aves * kg_ave * merma
                disp_kg = prod_kg + sum(x[1] for x in lotes[p])
                ls = [l for l in lineas if l["producto"] == p]
                vend_l = {}
                resto = disp_kg
                for prio in sorted({l.get("prioridad", 1) for l in ls if not l.get("toma_todo")}):
                    grupo = [l for l in ls if not l.get("toma_todo") and l.get("prioridad", 1) == prio]
                    pedido = sum(l["_q"] for l in grupo)
                    fr = 1.0 if pedido <= resto or pedido == 0 else resto / pedido
                    for l in grupo:
                        vend_l[l["id"]] = l["_q"] * fr if "M03" not in _MUT else l["_q"]
                    resto = max(0.0, resto - pedido * fr)
                tt = [l for l in ls if l.get("toma_todo")]
                for l in tt:
                    vend_l[l["id"]] = resto / len(tt)
                if tt:
                    resto = 0.0
                if "M02" in _MUT:
                    for l in ls:
                        vend_l[l["id"]] = disp_kg / max(1, len(ls))
                    resto = 0.0 if ls else resto
                vendido = sum(vend_l.values())
                # consumir lotes viejos primero, luego la producción del mes
                cons = vendido
                if "M16" not in _MUT:
                    for x in lotes[p]:
                        t_ = min(x[1], cons)
                        x[1] -= t_
                        cons -= t_
                lotes[p] = [x for x in lotes[p] if x[1] > 1e-12]
                nuevo = max(0.0, prod_kg - cons)
                if nuevo > 0:
                    lotes[p].append([0, nuevo])
                for x in lotes[p]:
                    x[0] += 1
                lim = P["inventario_max_meses"].get(p, 0)
                vencido = sum(x[1] for x in lotes[p] if x[0] > lim)
                lotes[p] = [x for x in lotes[p] if x[0] <= lim]
                S["kg_excedente_sin_venta"][k] += vencido
                S["kg_inventario"][k] += sum(x[1] for x in lotes[p])
                S["kg_vendidos"][k] += vendido
                for l in ls:
                    kg_v = vend_l.get(l["id"], 0.0)
                    pl = por_linea[l["id"]]
                    pl["kg"][k] = kg_v
                    precio = _precio(P["precios"].get(_clave_precio(l)), anio)
                    precio = (precio or 0.0) * idx[k] * st.get("precio", 1.0)
                    if st.get("devaluacion") and (P["precios"].get(_clave_precio(l)) or {}).get("moneda_original") == "ARS":
                        precio *= f_dev
                    bruto = kg_v * precio
                    ch = P["canales"].get(l["canal"], {})
                    g = lambda c_: ch.get(c_) or 0.0
                    desc, bon, dev, com = bruto * g("pct_descuentos"), bruto * g("pct_bonificaciones"), \
                        bruto * g("pct_devoluciones"), bruto * g("pct_comisiones")
                    exp_ = l.get("mercado", "INTERNO") != "INTERNO"
                    der = bruto * g("pct_derechos_exportacion") if exp_ else 0.0
                    neto = bruto - desc - bon - dev - com - der
                    pl["bruto"][k], pl["neto"][k] = bruto, neto
                    for nom, v in (("venta_bruta", bruto), ("descuentos", desc), ("bonificaciones", bon),
                                   ("devoluciones", dev), ("comisiones", com), ("derechos_exportacion", der),
                                   ("ingreso_neto", neto)):
                        S[nom][k] += v
                    S[f"venta_{pr['categoria_ingreso']}"][k] += bruto
                    S["venta_bruta_exportacion" if exp_ else "venta_bruta_domestica"][k] += bruto
                    S["costos_logistica_canal"][k] += kg_v * g("costo_logistico_usd_kg") * idx[k]
                    if exp_:
                        S["costos_exportacion"][k] += kg_v * g("costo_exportacion_usd_kg") * idx[k]
                    S["cxc"][k] += neto / DIAS_MES * g("dias_cobro")
                    if not exp_:
                        S["iva_debito"][k] += (bruto - desc - bon - dev) * (iva_p.get("alicuota_ventas") or 0.0)
            # OPEX por rubro de la etapa activa (escala plena de esa etapa): variables × u ÷ eficiencia; fijos enteros
            u = aves / cap
            mort = st.get("mortalidad")
            f_mort = (1 - mort["base"]) / (1 - mort["nueva"]) if mort else 1.0
            for r in ea["opex_rubros"] or []:
                pv = {"variable": 1.0, "fijo": 0.0, "semifijo": 0.0}.get(r["naturaleza"])
                if pv is None:
                    pv = (r.get("pct_variable") or 0.0) / 100
                costo = (r["costo_pleno_usd_anio"] or 0.0) * idx[k] * st.get("opex", 1.0)
                if st.get("devaluacion") and r.get("moneda_original") == "ARS":
                    costo *= f_dev
                if r.get("grupo_proveedor") in ("alimento", "granos"):
                    costo *= st.get("alimento", 1.0)
                if r.get("grupo_proveedor") == "pollitos":
                    costo *= f_mort
                u_fijo = u if "M07" in _MUT else 1.0
                m_var = costo / 12 * pv * u / ef
                m_fij = costo / 12 * (1 - pv) * u_fijo
                mes = m_var + m_fij
                rub_mes[r["rubro"]] = mes
                S[f"opex_{r['naturaleza']}"][k] += mes
                opex_mes += mes
                if r.get("es_compra"):
                    S["cxp"][k] += mes / DIAS_MES * (r.get("dias_pago") or 0.0)
                if r.get("iva_credito"):
                    S["iva_credito"][k] += mes * (iva_p.get("alicuota_compras") or 0.0)
            S["opex_total"][k] = opex_mes
            S["costos_extra_rampup"][k] = extra
            # IIBB sobre la base declarada por mercado (TF-005): una base con regla PENDIENTE no se grava ni se exime en
            # silencio; disponibilidad() deja el bloque IMPUESTOS_INGRESOS como NO_CALCULABLE_REGLA_FISCAL_PENDIENTE
            base_iibb = (S["venta_bruta_domestica"][k] * (1.0 if imp.get("iibb_aplica_domestico") else 0.0) +
                         S["venta_bruta_exportacion"][k] * (1.0 if imp.get("iibb_aplica_exportacion") else 0.0))
            S["impuestos_sobre_ingresos"][k] = ((imp.get("pct_iibb") or 0.0) * base_iibb +
                                               S["venta_bruta"][k] * (imp.get("pct_tasas_municipales") or 0.0))
            S["otros_impuestos"][k] = (imp.get("otros_impuestos_usd_anio") or 0.0) / 12 * idx[k]
        elif k >= 1:
            hist_u.append(0.0)
        if "M17" in _MUT:
            S["costo_iva_capex_mutante"][k] = S["capex_total"][k] * (iva_p.get("alicuota_capex") or 0.0)
        S["ebitda"][k] = (S["ingreso_neto"][k] - S["opex_total"][k] - S["costos_logistica_canal"][k]
                          - S["costos_exportacion"][k] - S["impuestos_sobre_ingresos"][k] - S["otros_impuestos"][k]
                          - S["costos_extra_rampup"][k] - S["costo_iva_capex_mutante"][k]
                          - (S["derechos_exportacion"][k] if "M21" in _MUT else 0.0))
        S["ebit"][k] = S["ebitda"][k] - S["depreciacion"][k]
        # --- capital de trabajo (saldos a fin de mes; solo inventario propio) ---
        inv_tot = 0.0
        for cat, x in (P["inventarios"] or {}).items():
            if not x.get("propiedad_empresa"):
                continue                           # stock de terceros no entra (interfaz OPEX §6)
            base = x.get("base", "OPEX_TOTAL")
            if base == "OPEX_TOTAL":
                b_ = opex_mes
            elif "grupos" in base:
                b_ = sum(rub_mes.get(r["rubro"], 0.0) for r in (etapas[activas[-1]]["opex_rubros"] or [])
                         if r.get("grupo_proveedor") in base["grupos"]) if activas else 0.0
            else:
                b_ = sum(rub_mes.get(rn, 0.0) for rn in base["rubros"])
            v = b_ / DIAS_MES * (x.get("dias") or 0.0) + (x.get("stock_fijo_usd") or 0.0) * (1 if activas else 0)
            S[f"inv_{cat}"][k] = v
            inv_tot += v
        S["inventarios"][k] = inv_tot
        if P["dias_caja_operativa"] is not None:
            S["caja_operativa"][k] = opex_mes / DIAS_MES * P["dias_caja_operativa"]
        S["ct"][k] = S["inventarios"][k] + S["cxc"][k] + S["caja_operativa"][k] - S["cxp"][k]
        S["delta_ct"][k] = S["ct"][k] - (S["ct"][k - 1] if k else 0.0)
        # --- IVA (simplificado: arrastre del saldo a favor; efecto de caja = −Δ saldo) ---
        if iva_p["modo"] == "SIMPLIFICADO":
            S["iva_credito"][k] += S["iva_credito_capex"][k]   # TF-076: solo IVA de CAPEX declarado y elegible
            neto_iva = S["iva_debito"][k] - S["iva_credito"][k]
            pago = max(0.0, neto_iva - saldo_favor)
            nuevo_saldo = max(0.0, saldo_favor - neto_iva)
            S["iva_pago_fisco"][k], S["flujo_iva"][k] = pago, -(nuevo_saldo - saldo_favor)
            saldo_favor = nuevo_saldo
            S["iva_saldo_favor"][k] = saldo_favor
        else:
            S["iva_debito"][k] = S["iva_credito"][k] = S["iva_credito_capex"][k] = S["iva_capex_pendiente_base"][k] = 0.0
        # --- deuda ---
        for d in deudas:
            for a_, b_ in (("deuda_alta", "alta"), ("deuda_interes", "interes"), ("deuda_amort", "amort"),
                           ("deuda_comision", "comision"), ("deuda_saldo_ini", "saldo_ini"), ("deuda_saldo_fin", "saldo_fin")):
                S[a_][k] += d[b_][k]
        # --- impuesto a las ganancias (anual, al cierre de cada año del proyecto; quebrantos con vencimiento) ---
        if k >= 1 and k % 12 == 0 and imp.get("tasa_ganancias") is not None:
            y = k // 12
            ebit_y = sum(S["ebit"][k - 11:k + 1])
            fin_y = sum(S["deuda_interes"][k - 11:k + 1]) + sum(S["deuda_comision"][k - 11:k + 1])
            for base_, pool, serie in ((ebit_y, quebr_u, "impuesto_operativo"),
                                       (ebit_y - (fin_y if imp.get("intereses_deducibles", True) else 0.0), quebr_l,
                                        "impuesto_con_deuda")):
                pool[:] = [q for q in pool if y - q[0] <= (imp.get("anios_quebranto") or 0)]
                if base_ < 0:
                    pool.append([y, -base_])
                    S[serie][k] = 0.0
                else:
                    imponible = base_
                    for q in pool:
                        t_ = min(q[1], imponible)
                        q[1] -= t_
                        imponible -= t_
                    pool[:] = [q for q in pool if q[1] > 1e-9]
                    S[serie][k] = imp["tasa_ganancias"] * imponible
        # --- valor terminal (al cierre del horizonte) ---
        if k == N:
            m = vt_p["metodo"]
            if m == "VALOR_LIBRO":
                S["valor_terminal"][k] = S["valor_libro"][k]
            elif m == "EXPLICITO":
                S["valor_terminal"][k] = (vt_p.get("monto") or 0.0) * idx[k]
            if vt_p.get("recuperar_ct"):
                S["valor_terminal"][k] += S["ct"][k]
            S["deuda_remanente_cierre"][k] = S["deuda_saldo_fin"][k]
        # --- flujos ---
        base_flujo = S["ebitda"][k] if "M05" not in _MUT else S["ebit"][k]
        dct = S["delta_ct"][k] if "M04" not in _MUT else S["ct"][k]
        S["fcff_pre"][k] = base_flujo - S["capex_total"][k] - dct + S["flujo_iva"][k] + S["valor_terminal"][k]
        if "M06" in _MUT:
            S["fcff_pre"][k] += S["deuda_alta"][k]
        if k == N and vt_p["metodo"] == "PERPETUIDAD" and P["tasa_descuento"] is not None and vt_p.get("g") is not None:
            r_, g_ = P["tasa_descuento"], vt_p["g"]
            if r_ <= g_:
                raise ErrorFinanciero("perpetuidad: la tasa debe superar al crecimiento g")
            ult = (sum(S["fcff_pre"][N - 11:N + 1]) - S["valor_terminal"][N]
                   - sum(S["impuesto_operativo"][N - 11:N + 1]))
            perp = ult * (1 + g_) / (r_ - g_)
            S["valor_terminal"][k] += perp             # suma al CT recuperado (si lo hay): la serie cierra la identidad del FCFF
            S["fcff_pre"][k] += perp
        S["fcff"][k] = S["fcff_pre"][k] - S["impuesto_operativo"][k]
        financ = (- S["deuda_interes"][k] - S["deuda_comision"][k] + S["deuda_alta"][k] - S["deuda_amort"][k]
                  - S["deuda_remanente_cierre"][k])
        S["fcfe_pre"][k] = S["fcff_pre"][k] + financ
        S["fcfe"][k] = S["fcff_pre"][k] - S["impuesto_con_deuda"][k] + financ
        S["cfads"][k] = (S["ebitda"][k] - S["impuesto_con_deuda"][k] - S["delta_ct"][k] + S["flujo_iva"][k]
                         - S["capex_reposicion"][k])
        S["servicio_deuda"][k] = S["deuda_interes"][k] + S["deuda_amort"][k]
        # --- caja del accionista (cierra período a período) ---
        flujo_acc = S["fcfe"][k] if ok["fcfe_post"] else S["fcfe_pre"][k]
        aporte = sum(m_ for mm_, m_ in fin.get("aportes", []) if mm_ == k)
        caja_pre = caja + flujo_acc + aporte
        if fin.get("aporte_automatico") and caja_pre < (fin.get("caja_minima_usd") or 0.0):
            aporte += (fin.get("caja_minima_usd") or 0.0) - caja_pre
            caja_pre = fin.get("caja_minima_usd") or 0.0
        div = 0.0
        pol = fin.get("politica_dividendos")
        if pol and k >= 1 and k % 12 == 0:
            div = pol["pct_caja_excedente"] * max(0.0, caja_pre - (pol.get("caja_minima_usd") or 0.0))
        S["aportes"][k], S["dividendos"][k] = aporte, div
        caja = caja_pre - (div if "M19" not in _MUT else 0.0)
        S["caja"][k] = caja
    R["entrada_etapas"], R["disparo_etapas"] = entrada, disparo
    R["deudas"] = deudas
    R["por_linea"] = por_linea
    # --- anular series no calculables (un faltante nunca se publica como 0) ---
    grupos = {
        "fisico": ("capacidad_aves", "aves_disponibles", "aves_requeridas", "aves_requeridas_aseguradas", "aves_faenadas",
                   "u_tecnica", "u_comercial", "u_efectiva", "kg_producidos", "kg_vendidos", "kg_excedente_sin_venta",
                   "kg_inventario", "kg_merma_rampup"),
        "bruto": ("venta_bruta", "venta_bruta_domestica", "venta_bruta_exportacion") + tuple(f"venta_{c}" for c in CATEGORIAS_INGRESO),
        "neto": ("descuentos", "bonificaciones", "devoluciones", "comisiones", "derechos_exportacion", "ingreso_neto",
                 "costos_logistica_canal", "costos_exportacion", "cxc"),
        "opex": ("opex_variable", "opex_fijo", "opex_semifijo", "opex_semivariable", "opex_total", "costos_extra_rampup"),
        "ebitda": ("impuestos_sobre_ingresos", "otros_impuestos", "ebitda", "costo_iva_capex_mutante"),
        "dep": ("depreciacion", "valor_libro"), "ebit": ("ebit",),
        "capex": ("capex_inicial", "capex_expansion", "capex_reposicion", "capex_total"),
        "ct": ("inv_materias_primas", "inv_alimento", "inv_packaging", "inv_repuestos", "inv_producto_terminado",
               "inv_activo_biologico", "inv_otros", "inventarios", "caja_operativa", "cxp", "ct", "delta_ct"),
        "iva": ("iva_debito", "iva_credito", "iva_saldo_favor", "iva_pago_fisco", "flujo_iva", "iva_credito_capex",
                "iva_capex_pendiente_base"),
        "fcff_pre": ("fcff_pre", "valor_terminal"), "fcff_post": ("impuesto_operativo", "fcff"),
        "fin": ("deuda_alta", "deuda_interes", "deuda_amort", "deuda_comision", "deuda_saldo_ini", "deuda_saldo_fin",
                "deuda_remanente_cierre", "servicio_deuda"),
        "fcfe_pre": ("fcfe_pre", "aportes", "dividendos", "caja"),
        "fcfe_post": ("impuesto_con_deuda", "fcfe", "cfads"),
    }
    if not ok["capex"]:
        ok["fcff_pre"] = ok["fcff_post"] = ok["fcfe_pre"] = ok["fcfe_post"] = False
    for g, series in grupos.items():
        if not ok[g]:
            for s_ in series:
                S[s_] = None
    if not ok["neto"]:
        for v in por_linea.values():
            v["neto"] = None
        if not ok["bruto"]:
            for v in por_linea.values():
                v["bruto"] = None
    if not ok["fisico"]:
        R["por_linea"] = {}
    R["series"] = S
    R["periodos"] = periodos_reporte(P, N, inicio_op, S["fase"])
    return R


def periodos_reporte(P, N, inicio_op, fase):
    M = P["meses_detalle"]
    fi = P["fecha_inicio"]
    out = [{"PERIODO": "T0", "TIPO": "T0", "K0": 0, "K1": 0, "T_ANIOS": 0.0, "ANIO_PROYECTO": 0, "FECHA_INICIO": fi or "",
            "FASE": "T0"}]
    for k in range(1, M + 1):
        out.append({"PERIODO": f"M{k:02d}", "TIPO": "MES", "K0": k, "K1": k, "T_ANIOS": k / 12,
                    "ANIO_PROYECTO": (k - 1) // 12 + 1, "FECHA_INICIO": sumar_meses(fi, k - 1) if fi else "",
                    "FASE": fase[k]})
    for y in range(M // 12 + 1, N // 12 + 1):
        k0, k1 = 12 * (y - 1) + 1, 12 * y
        fs = []
        for k in range(k0, k1 + 1):
            if fase[k] not in fs:
                fs.append(fase[k])
        out.append({"PERIODO": f"A{y:02d}", "TIPO": "ANIO", "K0": k0, "K1": k1, "T_ANIOS": float(y), "ANIO_PROYECTO": y,
                    "FECHA_INICIO": sumar_meses(fi, k0 - 1) if fi else "", "FASE": "→".join(fs)})
    for p in out:
        p["ANIO_OPERATIVO"] = 0 if p["K1"] < inicio_op else (p["K1"] - inicio_op) // 12 + 1
    return out


SALDOS = {"kg_inventario", "inventarios", "cxc", "caja_operativa", "cxp", "ct", "iva_saldo_favor", "deuda_saldo_fin",
          "caja", "valor_libro", "capacidad_aves"} | {f"inv_{c}" for c in CATEGORIAS_INVENTARIO}
SALDOS_INICIALES = {"deuda_saldo_ini"}
PROMEDIOS = {"u_tecnica": "aves_disponibles", "u_comercial": "aves_requeridas", "u_efectiva": "aves_faenadas"}


def agregar(R, serie):
    """Serie mensual → períodos de reporte. Flujos = suma; saldos = fin de período; utilizaciones = aves ÷ capacidad."""
    S = R["series"]
    if S.get(serie) is None:
        return [None] * len(R["periodos"])
    out = []
    for p in R["periodos"]:
        k0, k1 = p["K0"], p["K1"]
        if serie in SALDOS:
            out.append(S[serie][k1])
        elif serie in SALDOS_INICIALES:
            out.append(S[serie][k0])
        elif serie in PROMEDIOS:
            cap = sum(S["capacidad_aves"][k0:k1 + 1])
            out.append(sum(S[PROMEDIOS[serie]][k0:k1 + 1]) / cap if cap else None)
        else:
            out.append(sum(S[serie][k0:k1 + 1]))
    return out


# ---------------------------------------------------------------------------------------------
# 6. INDICADORES (funciones puras: se prueban contra casos manuales)
# ---------------------------------------------------------------------------------------------
def van(flujos, tiempos, tasa):
    """VAN = Σ F_i ÷ (1 + tasa)^t_i ; tasa ANUAL EFECTIVA; t en años (fin de período). Con t = k/12 equivale a
    descontar cada mes k con (1 + r)^(1/12) − 1 (ver van_periodico)."""
    if tasa is None or any(f is None for f in flujos):
        return None
    if tasa <= -1:
        raise ErrorFinanciero("tasa ≤ −100 %")
    return sum(f / (1 + tasa) ** (t - (1 / 12 if "M08" in _MUT and t > 0 else 0)) for f, t in zip(flujos, tiempos))


def van_periodico(flujos, tasa_periodo):
    """VAN de flujos equiespaciados: Σ F_k ÷ (1 + i)^k ; k = 0 es T0 (sin descontar). i = tasa del período
    (mensual: tasa_periodica(r_anual_efectiva, 1))."""
    if tasa_periodo is None or any(f is None for f in flujos):
        return None
    return sum(f / (1 + tasa_periodo) ** (k - (1 if "M08" in _MUT and k > 0 else 0)) for k, f in enumerate(flujos))


def anualizar(tasa_periodo, periodos_por_anio=12):
    """Tasa anual efectiva equivalente: (1 + i)^n − 1. Nunca i × n."""
    if tasa_periodo is None:
        return None
    if "M23" in _MUT:
        return tasa_periodo * periodos_por_anio
    return (1 + tasa_periodo) ** periodos_por_anio - 1


def indicadores(flujos, convencion, r_anual, r_reinv=None, tiempos_anios=None, calcular_tir=True):
    """VAN, TIR (periódica y anual efectiva), MIRR y payback (meses y años) de un flujo.
    calcular_tir=False (interfaz de performance, sesión 20): TIR = None con estado TIR_NO_CALCULADA; el resto, idéntico.
    MENSUAL         : flujos = serie mensual del motor (k = 0…N); tasa mensual = (1 + r)^(1/12) − 1; TIR mensual → anual.
    PERIODO_REPORTE : flujos agregados a períodos de reporte, descontados al fin de cada período (t en años)."""
    out = {}
    if convencion == "MENSUAL":
        k = list(range(len(flujos)))
        i_m = tasa_periodica(r_anual, 1)
        out["VAN"] = van_periodico(flujos, i_m)
        tm, est = tir(flujos, k, r_min=-0.5, r_max=2.0) if calcular_tir else (None, TIR_NO_CALCULADA)  # tasa MENSUAL
        out["TIR_MENSUAL"], out["TIR"], out["TIR_ESTADO"] = tm, anualizar(tm), est
        out["MIRR"] = mirr(flujos, [x / 12 for x in k], r_anual, r_reinv)
        pm, out["PAYBACK_SIMPLE_ESTADO"] = payback(flujos, k)
        pdm, out["PAYBACK_DESCONTADO_ESTADO"] = payback(flujos, k, i_m) if i_m is not None else (None, "NO_CALCULABLE")
    else:
        t = tiempos_anios
        out["VAN"] = van(flujos, t, r_anual)
        ta, est = tir(flujos, t) if calcular_tir else (None, TIR_NO_CALCULADA)
        out["TIR"], out["TIR_ESTADO"] = ta, est
        out["TIR_MENSUAL"] = tasa_periodica(ta, 1) if ta is not None else None
        out["MIRR"] = mirr(flujos, t, r_anual, r_reinv)
        pa, out["PAYBACK_SIMPLE_ESTADO"] = payback(flujos, t)
        pda, out["PAYBACK_DESCONTADO_ESTADO"] = payback(flujos, t, r_anual) if r_anual is not None else (None, "NO_CALCULABLE")
        pm = pa * 12 if pa is not None else None
        pdm = pda * 12 if pda is not None else None
    out["PAYBACK_SIMPLE_MESES"], out["PAYBACK_DESCONTADO_MESES"] = pm, pdm
    div = 1 if "M25" in _MUT else 12
    out["PAYBACK_SIMPLE_ANIOS"] = pm / div if pm is not None else None
    out["PAYBACK_DESCONTADO_ANIOS"] = pdm / div if pdm is not None else None
    return out


def cambios_de_signo(flujos):
    sg = [1 if f > 0 else -1 for f in flujos if abs(f) > 1e-9]
    return sum(1 for a, b in zip(sg, sg[1:]) if a != b)


def tir(flujos, tiempos, r_min=-0.99, r_max=10.0, n_grilla=4000):
    """TIR por barrido + bisección. NO fuerza una TIR: devuelve (valor, estado):
    UNICA | UNICA_FLUJO_NO_CONVENCIONAL | NO_EXISTE (sin cambio de signo) | NO_EXISTE_EN_RANGO | TIR_AMBIGUA."""
    if any(f is None for f in flujos):
        return None, "NO_CALCULABLE"
    cs = cambios_de_signo(flujos)
    if cs == 0:
        return None, "NO_EXISTE (el flujo no cambia de signo)"
    def f(r):
        try:
            return sum(x / (1 + r) ** t for x, t in zip(flujos, tiempos))
        except (OverflowError, ZeroDivisionError):
            return math.inf
    grid = [r_min + (r_max - r_min) * (i / n_grilla) ** 2 for i in range(n_grilla + 1)]
    raices = []
    prev_r, prev_v = grid[0], f(grid[0])
    for r in grid[1:]:
        v = f(r)
        if prev_v == 0:
            raices.append(prev_r)
        elif prev_v * v < 0:
            a, b, fa = prev_r, r, prev_v
            for _ in range(200):
                m = (a + b) / 2
                fm = f(m)
                if fa * fm <= 0:
                    b = m
                else:
                    a, fa = m, fm
            raices.append((a + b) / 2)
        prev_r, prev_v = r, v
    raices = sorted({round(x, 10) for x in raices})
    if "M12" in _MUT and raices:
        return raices[0], "UNICA"
    if not raices:
        return None, f"NO_EXISTE_EN_RANGO ({r_min:.0%} a {r_max:.0%} por período)"
    if len(raices) > 1:
        return None, "TIR_AMBIGUA: raíces " + ", ".join(f"{x:.4%}" for x in raices)
    return raices[0], ("UNICA" if cs == 1 else "UNICA_FLUJO_NO_CONVENCIONAL (verificar con VAN)")


def mirr(flujos, tiempos, tasa_fin, tasa_reinv):
    if None in (tasa_fin, tasa_reinv) or any(f is None for f in flujos):
        return None
    T = tiempos[-1]
    vp_neg = sum(-f / (1 + tasa_fin) ** t for f, t in zip(flujos, tiempos) if f < 0)
    vf_pos = sum(f * (1 + tasa_reinv) ** (T - t) for f, t in zip(flujos, tiempos) if f > 0)
    if vp_neg <= 0 or vf_pos <= 0 or T <= 0:
        return None
    return (vf_pos / vp_neg) ** (1 / T) - 1


def payback(flujos, tiempos, tasa=None):
    """Años hasta que el acumulado (descontado si hay tasa) vuelve a ≥ 0, con interpolación lineal DENTRO del
    período de recupero (flujo uniforme en el período). Sin recupero en el horizonte → NO_RECUPERADO (no se
    extrapola)."""
    if any(f is None for f in flujos):
        return None, "NO_CALCULABLE"
    if tasa is not None:
        flujos = [f / (1 + tasa) ** t for f, t in zip(flujos, tiempos)]
    acum, fue_neg, t_prev = 0.0, False, 0.0
    for i, (f, t) in enumerate(zip(flujos, tiempos)):
        nuevo = acum + f
        if acum < -1e-9 and nuevo >= -1e-12:
            t_rec = t_prev + (-acum / f) * (t - t_prev)
            a2, vuelve = nuevo, False
            for f2 in flujos[i + 1:]:
                a2 += f2
                vuelve = vuelve or a2 < -1e-9
            return t_rec, "RECUPERADO" + (" (el acumulado vuelve a ser negativo después)" if vuelve else "")
        fue_neg = fue_neg or nuevo < -1e-9
        acum, t_prev = nuevo, t
    if not fue_neg:
        return None, "NO_APLICA (sin inversión neta)"
    if "M13" in _MUT and flujos[-1] > 0:
        return tiempos[-1] + (-acum) / flujos[-1], "RECUPERADO"
    return None, "NO_RECUPERADO"


def break_even_simple(precio, costo_variable_unitario, costos_fijos, capacidad=None):
    """q* = fijos ÷ (precio − variable). Devuelve (q*, u*) o (None, motivo)."""
    mc = precio - costo_variable_unitario
    if mc <= 0:
        return None, "NO_EXISTE (margen de contribución ≤ 0)"
    q = costos_fijos / mc
    return q, (q / capacidad if capacidad else None)


def break_even_anual(R, k0, k1, con_depreciacion=False):
    """Break-even del año [k0, k1] (año maduro): margen de contribución por ave con el MISMO mix y precios.
    Variables = OPEX variable y la parte variable de los semivariables, costos logísticos/exportación por kg y
    extras de ramp-up; ∝ precio = impuestos sobre ingresos; fijos = fijos + semifijos + parte fija de semivariables
    + otros impuestos fijos (+ depreciación si con_depreciacion)."""
    S, P = R["series"], R["P"]
    if S.get("ebitda") is None:
        return None
    rng = range(k0, k1 + 1)
    tot = lambda s: sum(S[s][k] for k in rng)
    aves, cap = tot("aves_faenadas"), tot("capacidad_aves")
    if aves <= 0:
        return {"ESTADO": "SIN_PRODUCCION_EN_EL_AÑO"}
    ea = None
    for i, e in enumerate(P["etapas"]):
        if R["entrada_etapas"][i] is not None and R["entrada_etapas"][i] <= k0:
            ea = e
    var_semi = 0.0
    fij_semi = tot("opex_semivariable")
    if ea and ea["opex_rubros"]:
        sv = [r for r in ea["opex_rubros"] if r["naturaleza"] == "semivariable"]
        tot_sv_pleno = sum(r["costo_pleno_usd_anio"] for r in sv)
        if tot_sv_pleno > 0:
            var_frac = sum(r["costo_pleno_usd_anio"] * r["pct_variable"] / 100 for r in sv) / tot_sv_pleno
            var_semi = fij_semi * var_frac        # aproximación: reparto del año por peso pleno
            fij_semi -= var_semi
    cv = tot("opex_variable") + var_semi + tot("costos_logistica_canal") + tot("costos_exportacion") + tot("costos_extra_rampup")
    cf = tot("opex_fijo") + tot("opex_semifijo") + fij_semi + tot("otros_impuestos")
    if con_depreciacion:
        if S.get("depreciacion") is None:
            return None
        cf += tot("depreciacion")
    rn, imp_p, bruto, kg = tot("ingreso_neto"), tot("impuestos_sobre_ingresos"), tot("venta_bruta"), tot("kg_vendidos")
    mc = rn - imp_p - cv
    out = {"AVES_ANIO": aves, "CAPACIDAD_AVES_ANIO": cap, "U_EFECTIVA": aves / cap, "INGRESO_NETO": rn,
           "IMPUESTOS_PROPORCIONALES_AL_PRECIO": imp_p, "COSTOS_VARIABLES": cv, "COSTOS_FIJOS": cf,
           "MARGEN_CONTRIBUCION": mc, "MC_POR_AVE": mc / aves, "KG_VENDIDOS": kg,
           "PRECIO_MEDIO_BRUTO_USD_KG": bruto / kg if kg else None,
           "REQ_DEMANDA_AVES_ANIO": sum(S["aves_requeridas"][k] for k in rng)}
    if mc <= 0:
        out.update({"ESTADO": "NO_EXISTE (margen de contribución ≤ 0: ninguna escala cubre los fijos)",
                    "BE_AVES_ANIO": None, "BE_UTILIZACION": None})
    else:
        q = cf / (mc / aves)
        out.update({"ESTADO": "CALCULADO", "BE_AVES_ANIO": q, "BE_UTILIZACION": q / cap,
                    "BE_KG_VENDIDOS": q * kg / aves if kg else None})
        if q > cap:
            out["ESTADO"] = "NO_ALCANZABLE_CON_LA_CAPACIDAD (q* > capacidad)"
        elif q > out["REQ_DEMANDA_AVES_ANIO"] + 1e-9:
            out["ESTADO"] = "CALCULADO; q* SUPERA LA DEMANDA CONTABLE DEL AÑO"
    k_p = (cv + cf) / (rn - imp_p) if rn - imp_p > 0 else None
    out["BE_FACTOR_PRECIO"] = k_p
    out["BE_PRECIO_MEDIO_BRUTO_USD_KG"] = k_p * out["PRECIO_MEDIO_BRUTO_USD_KG"] if (k_p and out["PRECIO_MEDIO_BRUTO_USD_KG"]) else None
    return out


# ---------------------------------------------------------------------------------------------
# 7. RESULTADOS, PUBLICABILIDAD Y CAPITAL REQUERIDO
# ---------------------------------------------------------------------------------------------
FLAGS = ("PUBLICABLE_INGRESOS", "PUBLICABLE_EBITDA", "PUBLICABLE_FLUJO", "PUBLICABLE_FLUJO_AFTER_TAX",
         "PUBLICABLE_VAN", "PUBLICABLE_TIR", "PUBLICABLE_PAYBACK", "PUBLICABLE_BREAK_EVEN",
         "PUBLICABLE_FLUJO_ACCIONISTA", "PUBLICABLE_DSCR")
DEPENDENCIAS_FLAG = {
    "PUBLICABLE_INGRESOS": ("TIEMPO", "RAMPUP", "PRODUCCION", "DEMANDA", "PRECIOS", "CANALES"),
    "PUBLICABLE_EBITDA": ("TIEMPO", "RAMPUP", "PRODUCCION", "DEMANDA", "PRECIOS", "CANALES", "OPEX", "IMPUESTOS_INGRESOS"),
    "PUBLICABLE_FLUJO": ("TIEMPO", "RAMPUP", "PRODUCCION", "DEMANDA", "PRECIOS", "CANALES", "OPEX", "IMPUESTOS_INGRESOS",
                         "CAPEX", "CT", "IVA", "REPOSICION", "VALOR_TERMINAL"),
}
DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO_AFTER_TAX"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO"] + ("DEPRECIACION", "GANANCIAS")
DEPENDENCIAS_FLAG["PUBLICABLE_VAN"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO"] + ("DESCUENTO",)
DEPENDENCIAS_FLAG["PUBLICABLE_TIR"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO"]
DEPENDENCIAS_FLAG["PUBLICABLE_PAYBACK"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO"]
DEPENDENCIAS_FLAG["PUBLICABLE_BREAK_EVEN"] = DEPENDENCIAS_FLAG["PUBLICABLE_EBITDA"]
DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO_ACCIONISTA"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO"] + ("FINANCIAMIENTO",)
DEPENDENCIAS_FLAG["PUBLICABLE_DSCR"] = DEPENDENCIAS_FLAG["PUBLICABLE_FLUJO_AFTER_TAX"] + ("FINANCIAMIENTO",)


def publicabilidad(R):
    F, P = R["faltantes"], R["P"]
    out = {}
    for fl in FLAGS:
        falt = [f"{b}: {x}" for b in DEPENDENCIAS_FLAG[fl] for x in F[b]]
        if "M20" in _MUT and fl == "PUBLICABLE_EBITDA":
            falt = [x for x in falt if not x.startswith("OPEX")]
        extra = ""
        if fl == "PUBLICABLE_TIR" and not falt and R.get("tir_estado") == TIR_NO_CALCULADA:
            out[fl] = (False, f"{TIR_NO_CALCULADA}: TIR no solicitada en esta evaluación (calcular_tir=False)")
            continue
        if fl == "PUBLICABLE_TIR" and not falt and R.get("tir_estado") and not R["tir_estado"].startswith("UNICA"):
            falt = [f"TIR matemática: {R['tir_estado']}"]
        if fl == "PUBLICABLE_DSCR" and not falt and not (P["financiamiento"] or {}).get("deudas"):
            falt = ["sin deuda en la estructura: DSCR no aplica"]
        val = not falt
        if val:
            extra = (ETIQUETA_OVERRIDE_TOTAL if P.get("override_total") else ETIQUETA_SIM) if P["modo"] == "ESCENARIO" else \
                f"EVIDENCIA completa dentro del umbral {'|'.join(P['umbral_evidencia'])} (DEC-084 abierta)"
        pref = "TIR_NO_DEFINIDA_MATEMATICAMENTE" if falt and falt[0].startswith("TIR matemática") else \
            "NO_APLICA" if falt and falt[0].startswith("sin deuda") else (NO_PUB if P["modo"] == "EVIDENCIA" else NO_DISP_ESC)
        motivo = extra if val else pref + " — falta: " + " | ".join(falt)
        out[fl] = (val, motivo)
    return out


def resultados(R, calcular_tir=True):
    """Indicadores sobre los períodos de reporte. Nunca devuelve un número para un flag FALSE.
    calcular_tir=False: interfaz de performance (sesión 20); omite solo TIR / TIR_ACCIONISTA (estado NO_CALCULADA)."""
    P = R["P"]
    out = {"ESCENARIO": P["nombre"], "MODO": P["modo"], "CONFIGURACION": P["configuracion"], "TRAYECTORIA": P["trayectoria"],
           "HORIZONTE_ANIOS": P["horizonte_anios"], "MODELO_MONETARIO": P["modelo_monetario"],
           "ETIQUETA": (ETIQUETA_OVERRIDE_TOTAL if P.get("override_total") else ETIQUETA_SIM) if P["modo"] == "ESCENARIO" else "MODO_EVIDENCIA",
           "TRAZABILIDAD": ("PARCIAL: OVERRIDE_TOTAL_ARQUITECTURA (CAPEX/OPEX del usuario sin verificar contra la arquitectura)"
                            if P.get("override_total") else "COMPLETA"),
           "UMBRAL_EVIDENCIA": "|".join(P.get("umbral_evidencia") or UMBRAL_EVIDENCIA_DEFAULT),
           "OVERRIDES_SIMULACION": ", ".join(P.get("overrides_simulacion") or []),
           "CONVENCION_DESCUENTO": P["convencion_descuento"]}
    if R["N"] == 0:
        R["tir_estado"] = None
        pub = publicabilidad(R)
        for fl, (v, m) in pub.items():
            out[fl], out[fl + "_MOTIVO"] = v, m
        out["FALTANTES"] = " || ".join(f"{b}: {'; '.join(x)}" for b, x in R["faltantes"].items() if x)
        return out
    per = R["periodos"]
    t = [p["T_ANIOS"] for p in per]
    ok = R["ok"]
    S = R["series"]
    base = "fcff" if ok["fcff_post"] else "fcff_pre"
    conv = P["convencion_descuento"]
    tipo = P["tipo_tasa_descuento"]
    r_ef = tasa_anual_efectiva(P["tasa_descuento"], tipo)
    r_acc = tasa_anual_efectiva(P["tasa_descuento_accionista"], tipo)
    r_rei = tasa_anual_efectiva(P["tasa_reinversion"], tipo)
    out["BASE_FLUJO"] = "AFTER_TAX" if ok["fcff_post"] else "PRE_TAX"
    out["CONVENCION_DESCUENTO"] = conv
    out["TASA_DESCUENTO_ANUAL_EFECTIVA"] = r_ef
    out["TASA_DESCUENTO_MENSUAL_EQUIVALENTE"] = tasa_periodica(r_ef, 1)
    if ok["fcff_pre"]:
        fl = S[base] if conv == "MENSUAL" else agregar(R, base)
        out.update(indicadores(fl, conv, r_ef, r_rei, t, calcular_tir))
    else:
        out.update({k: None for k in ("VAN", "TIR", "TIR_MENSUAL", "MIRR", "PAYBACK_SIMPLE_MESES", "PAYBACK_SIMPLE_ANIOS",
                                      "PAYBACK_DESCONTADO_MESES", "PAYBACK_DESCONTADO_ANIOS")})
        out.update({"TIR_ESTADO": "NO_CALCULABLE", "PAYBACK_SIMPLE_ESTADO": "NO_CALCULABLE",
                    "PAYBACK_DESCONTADO_ESTADO": "NO_CALCULABLE"})
    R["tir_estado"] = out["TIR_ESTADO"]
    # capital requerido
    if S["capex_total"] is not None:
        out["CAPEX_INICIAL"] = sum(S["capex_inicial"])
        out["CAPEX_EXPANSION"] = sum(S["capex_expansion"])
        out["CAPEX_REPOSICION"] = sum(S["capex_reposicion"])
    io_ = R["inicio_op"]
    curva0 = P["etapas"][0]["rampup"] or []
    fin_ramp = min(R["N"], io_ + int(math.ceil(_meses_rampup(curva0, (P["stress"] or {}).get("rampup_lento_factor", 1.0)))) - 1)
    if S["ct"] is not None:
        out["CT_INICIAL"] = max(S["ct"][: fin_ramp + 1])
        out["CT_MAXIMO"] = max(S["ct"])
    if S["capex_total"] is not None and S["ct"] is not None and S["iva_saldo_favor"] is not None:
        otros = max(S["iva_saldo_favor"][:io_]) if io_ > 0 else 0.0
        if S["deuda_interes"] is not None:
            otros += sum(S["deuda_interes"][:io_]) + sum(S["deuda_comision"][:io_])
            otros += (P["financiamiento"] or {}).get("reservas_usd") or 0.0
        out["OTROS_REQUERIMIENTOS_CAJA"] = otros
        out["FONDOS_INICIALES"] = out["CAPEX_INICIAL"] + out["CT_INICIAL"] + otros
    if S[base] is not None:
        acum, minimo, mes_min = 0.0, 0.0, 0
        for k, x in enumerate(S[base]):
            acum += x
            if acum < minimo:
                minimo, mes_min = acum, k
        out["PICO_REQUERIMIENTO_FONDOS"] = -minimo
        out["MES_VALLE_CAJA"] = mes_min
    # año maduro = último año del horizonte
    N = R["N"]
    k0, k1 = N - 11, N
    if S["venta_bruta"] is not None:
        out["VENTA_BRUTA_ULTIMO_ANIO"] = sum(S["venta_bruta"][k0:k1 + 1])
    if S["ingreso_neto"] is not None:
        out["INGRESO_NETO_ULTIMO_ANIO"] = sum(S["ingreso_neto"][k0:k1 + 1])
    if S["ebitda"] is not None:
        out["EBITDA_ULTIMO_ANIO"] = sum(S["ebitda"][k0:k1 + 1])
        out["MARGEN_EBITDA_ULTIMO_ANIO"] = (out["EBITDA_ULTIMO_ANIO"] / out["INGRESO_NETO_ULTIMO_ANIO"]
                                            if out["INGRESO_NETO_ULTIMO_ANIO"] else None)
    if S["u_efectiva"] is not None:
        cap = sum(S["capacidad_aves"][k0:k1 + 1])
        out["U_EFECTIVA_ULTIMO_ANIO"] = sum(S["aves_faenadas"][k0:k1 + 1]) / cap if cap else None
        out["U_COMERCIAL_REQUERIDA_ULTIMO_ANIO"] = sum(S["aves_requeridas"][k0:k1 + 1]) / cap if cap else None
        out["U_TECNICA_ULTIMO_ANIO"] = sum(S["aves_disponibles"][k0:k1 + 1]) / cap if cap else None
    be = break_even_anual(R, k0, k1)
    R["break_even"] = {"EBITDA": be, "EBIT": break_even_anual(R, k0, k1, True) if ok["ebit"] else None}
    if be:
        out["BE_UTILIZACION_EBITDA"] = be.get("BE_UTILIZACION")
        out["BE_AVES_ANIO_EBITDA"] = be.get("BE_AVES_ANIO")
        out["BE_PRECIO_MEDIO_USD_KG_EBITDA"] = be.get("BE_PRECIO_MEDIO_BRUTO_USD_KG")
        out["BE_ESTADO"] = be.get("ESTADO")
    if S["fcfe"] is not None or S["fcfe_pre"] is not None:
        ser = "fcfe" if S["fcfe"] is not None else "fcfe_pre"
        fe = agregar(R, ser)
        if conv == "MENSUAL":
            efectivo = [-a + d for a, d in zip(S["aportes"], S["dividendos"])]
        else:
            efectivo = [-a + d for a, d in zip(agregar(R, "aportes"), agregar(R, "dividendos"))]
        efectivo[-1] += S["caja"][N]
        out["BASE_FLUJO_ACCIONISTA"] = "AFTER_TAX" if ser == "fcfe" else "PRE_TAX"
        out["APORTES_TOTALES"] = sum(S["aportes"])
        out["DEUDA_TOMADA"] = sum(S["deuda_alta"])
        ia = indicadores(efectivo, conv, r_acc, None, t, calcular_tir)
        out["VAN_ACCIONISTA"], out["TIR_ACCIONISTA"], out["TIR_ACCIONISTA_ESTADO"] = ia["VAN"], ia["TIR"], ia["TIR_ESTADO"]
        out["CAJA_MINIMA_LEDGER"] = min(S["caja"])
        R["flujo_accionista_efectivo"] = efectivo
        R["fcfe_agregado"] = fe
    if S["cfads"] is not None and S["servicio_deuda"] is not None:
        cf_, sv_ = agregar(R, "cfads"), agregar(R, "servicio_deuda")
        ds = [c / s for c, s in zip(cf_, sv_) if s > 1e-9]
        out["DSCR_MINIMO"] = min(ds) if ds else None
    pub = publicabilidad(R)
    for fl_, (v, m) in pub.items():
        out[fl_], out[fl_ + "_MOTIVO"] = v, m
    # bloqueo final: nada se publica como número si su flag es FALSE
    bloqueo = {"PUBLICABLE_INGRESOS": ("VENTA_BRUTA_ULTIMO_ANIO", "INGRESO_NETO_ULTIMO_ANIO"),
               "PUBLICABLE_EBITDA": ("EBITDA_ULTIMO_ANIO", "MARGEN_EBITDA_ULTIMO_ANIO"),
               "PUBLICABLE_FLUJO": ("FONDOS_INICIALES", "PICO_REQUERIMIENTO_FONDOS", "OTROS_REQUERIMIENTOS_CAJA"),
               "PUBLICABLE_VAN": ("VAN",), "PUBLICABLE_TIR": ("TIR", "TIR_MENSUAL", "MIRR"),
               "PUBLICABLE_PAYBACK": ("PAYBACK_SIMPLE_ANIOS", "PAYBACK_DESCONTADO_ANIOS", "PAYBACK_SIMPLE_MESES",
                                      "PAYBACK_DESCONTADO_MESES"),
               "PUBLICABLE_BREAK_EVEN": ("BE_UTILIZACION_EBITDA", "BE_AVES_ANIO_EBITDA", "BE_PRECIO_MEDIO_USD_KG_EBITDA"),
               "PUBLICABLE_FLUJO_ACCIONISTA": ("VAN_ACCIONISTA", "TIR_ACCIONISTA", "APORTES_TOTALES"),
               "PUBLICABLE_DSCR": ("DSCR_MINIMO",)}
    for fl_, campos in bloqueo.items():
        if not out[fl_]:
            for c in campos:
                if c in out and out[c] is not None:
                    out[c] = None
    out["FALTANTES"] = " || ".join(f"{b}: {'; '.join(x)}" for b, x in R["faltantes"].items() if x)
    return out


# ---------------------------------------------------------------------------------------------
# 8. ADAPTADORES AL PROYECTO (consumen CAPEX, OPEX, balance, demanda y arquitecturas; no recalculan)
# ---------------------------------------------------------------------------------------------
TRAYECTORIAS_FIN = {"T1_2500_5000_10000_20000": (2500, 5000, 10000, 20000),
                    "T2_5000_10000_20000": (5000, 10000, 20000),
                    "T3_10000_20000": (10000, 20000),
                    "T4_20000_inicial": (20000,)}
PLANTILLAS = ("PLANTILLA_CONSERVADOR", "PLANTILLA_BASE", "PLANTILLA_EXPANSIVO")
MAPA_INVENTARIO_OPEX = (("alimento: alimento_terminado", "alimento"), ("alimento: maiz", "materias_primas"),
                        ("alimento: harina_soja", "materias_primas"), ("alimento: micros", "materias_primas"),
                        ("alimento: material_en_proceso", "materias_primas"),
                        ("alimento y materias primas", "alimento"), ("alimento y materias primas", "materias_primas"),
                        ("pollitos BB", "activo_biologico"), ("huevo", "activo_biologico"),
                        ("aves en crianza", "activo_biologico"), ("producto terminado", "producto_terminado"),
                        ("subproductos", "producto_terminado"), ("envases", "packaging"), ("repuestos", "repuestos"),
                        ("insumos", "otros"))
BASE_INVENTARIO = {"alimento": {"grupos": ["alimento"]}, "materias_primas": {"grupos": ["granos", "alimento"]},
                   "packaging": {"grupos": ["packaging"]}, "repuestos": {"grupos": ["servicios"]},
                   "producto_terminado": "OPEX_TOTAL", "activo_biologico": {"grupos": ["alimento", "pollitos"]},
                   "otros": {"grupos": ["servicios", "energia"]}}
_CACHE = {}


def mapa_arquitecturas():
    """Configuraciones evaluables = filas CONFIGURACION_BASE y VARIANTE del mapa (sin redefinirlas)."""
    return [r for r in leer_csv(ARCHIVO_MAPA_ARQ) if r["TIPO"] in ("CONFIGURACION_BASE", "VARIANTE")]


def configs(nombre_escenario):
    """(config CAPEX, config OPEX) de un escenario de referencia de CAPEX u OPEX (p. ej. 'C1-10000',
    'C1-10000-congelado_tercero', 'C1-10000-HALAL'). Cuando la variante es de un solo módulo, el otro se corre con
    los MISMOS inputs (T18-16)."""
    if "esc_capex" not in _CACHE:
        _CACHE["esc_capex"] = dict(mcx.escenarios_referencia())
        _CACHE["esc_opex"] = dict(mo.escenarios_opex())
    ec, eo = _CACHE["esc_capex"], _CACHE["esc_opex"]
    if nombre_escenario in eo:
        co = copy.deepcopy(eo[nombre_escenario])
        return mo.config_capex(co), co
    if nombre_escenario in ec:
        cc = copy.deepcopy(ec[nombre_escenario])
        co = mo.config_opex(None)
        co.update(copy.deepcopy(cc))               # misma arquitectura en OPEX (config_opex = defaults + kw)
        return cc, co
    base, esc = nombre_escenario.split("-")[:2]
    cc = mcx.preset(base, aves_dia=int(esc))
    return cc, mo.config_opex(base, aves_dia=int(esc))


def _correr_capex(cc):
    key = ("capex", mcx.etiqueta_arquitectura(cc), cc["aves_dia"], cc["dias_semana"], cc.get("criterio_terreno"),
           cc.get("escala_objetivo"))
    if key not in _CACHE:
        with redirect_stdout(io.StringIO()):
            _CACHE[key] = mcx.correr(cc)
    return _CACHE[key]


def _correr_opex(co):
    key = ("opex", json.dumps({k: co[k] for k in sorted(co)}, default=str))
    if key not in _CACHE:
        with redirect_stdout(io.StringIO()):
            _CACHE[key] = mo.correr(co)
    return _CACHE[key]


def _niveles_con_monto(T, prefijo):
    niv = set()
    for g, ls in (("E1_E2", ("E1", "E2")), ("E3", ("E3",)), ("E4", ("E4",)), ("E5", ("E5",))):
        if T.get(f"N_CONCEPTOS_{g}"):
            niv |= set(ls)
    return niv


def capex_desde_modulo(cc, umbral=None):
    """CAPEX total SOLO si el motor CAPEX publica TOTAL_PRELIMINAR y todo el monto es E1–E3. Un monto E4 parcial
    nunca se usa como total (devuelve None + motivo)."""
    filas, res, _ = _correr_capex(cc)
    T = res["TOTAL"]
    inciertos = [f for f in filas if f["COSTEA"] and f["TITULAR"] == "EMPRESA" and "IVA_INCIERTO" in (f.get("ALERTAS") or "")]
    if T["TOTAL_PRELIMINAR_USD"] is not None and inciertos:
        return None, "PENDIENTE", (f"CAPEX con IVA_INCIERTO en {len(inciertos)} conceptos: el total no se usa (ni el IVA como costo ni "
                                   "como crédito) hasta declarar el tratamiento del IVA (TF-076, DPV-093)")
    if T["TOTAL_PRELIMINAR_USD"] is not None and _niveles_con_monto(T, "CAPEX") <= set(umbral or UMBRAL_EVIDENCIA_DEFAULT):
        niv = "E1" if not T["N_CONCEPTOS_E3"] else "E3"
        return T["TOTAL_PRELIMINAR_USD"], niv, ""
    parcial = T["MONTO_CON_PRECIO_USD"]
    motivo = (f"CAPEX {T['TOTAL_PRELIMINAR']}; con precio {T['CONCEPTOS_CON_PRECIO']}/{T['CONCEPTOS_COSTEABLES']} "
              f"conceptos ({T['CALIDAD_MONTO']})" + (f"; monto parcial USD {parcial:,.0f} NO usado como total" if parcial else ""))
    return None, "PENDIENTE", motivo


def activos_desde_boq(cc):
    """Activos por bloque con vida útil y residual del BOQ. Hoy los campos están vacíos (DPV-167) → None."""
    filas, _, _ = _correr_capex(cc)
    emp = [f for f in filas if f["FASE"] == "INICIAL" and f["TITULAR"] == "EMPRESA" and f["COSTEA"]]
    sin_vida = [f for f in emp if f.get("VIDA_UTIL_ANIOS") in (None, "")]
    if sin_vida or any(f["ESTADO_COSTO"] != "CON_PRECIO" for f in emp):
        return None, f"VIDA_UTIL_ANIOS / VALOR_RESIDUAL vacíos en {len(sin_vida)} de {len(emp)} activos del BOQ (DPV-167)"
    out = []
    for f in emp:
        out.append({"clase": f"{f['BLOQUE']}:{f['ACTIVO_ID']}", "capex_usd": f["COSTO_INSTALADO_USD"],
                    "vida_util_anios": _num(f["VIDA_UTIL_ANIOS"]), "valor_residual_usd": _num(f["VALOR_RESIDUAL"]),
                    "costo_reemplazo_usd": _num(f["COSTO_REEMPLAZO"]), "depreciable": f["BLOQUE"] != "TERRENO"})
    return out, ""


def opex_desde_modulo(co, umbral=None):
    """Rubros = filas del registro OPEX (NATURALEZA, PCT_VARIABLE, GRUPO_PROVEEDOR) SOLO si OPEX publica total y la
    arquitectura es costeable con evidencia E1–E3. Si no, None + motivo (los montos E4 parciales no se usan)."""
    filas, res, DR, ct_rows, ct = _correr_opex(co)
    T = res["TOTAL"]
    if T["TOTAL_PRELIMINAR_USD_ANIO"] is not None and _niveles_con_monto(T, "OPEX") <= set(umbral or UMBRAL_EVIDENCIA_DEFAULT):
        rub = [{"rubro": f["COSTO_ID"] or f["CONCEPTO"], "grupo_proveedor": f["GRUPO_PROVEEDOR"], "naturaleza": f["NATURALEZA"],
                "costo_pleno_usd_anio": f["COSTO_CALCULADO_USD_ANIO"], "pct_variable": f["PCT_VARIABLE"],
                "es_compra": bool(f["GRUPO_PROVEEDOR"]), "dias_pago": None, "iva_credito": bool(f["GRUPO_PROVEEDOR"])}
               for f in filas if f["COSTEA"] and f["ESTADO"] == "CON_PRECIO"]
        return rub, "E3", ""
    parcial = T["MONTO_PARCIAL_CON_PRECIO_USD_ANIO"]
    motivo = (f"OPEX {T['TOTAL_PRELIMINAR']}; costeo por bloques {T['COBERTURA_COSTEO_BLOQUES_PCT']:.1f} %, "
              f"arquitectura costeable = {T['ARQUITECTURA_COSTEABLE']} ({T['CALIDAD_MONTO']})"
              + (f"; monto parcial USD {parcial:,.0f}/año NO usado como costo total" if parcial else ""))
    return None, "PENDIENTE", motivo


def propiedad_inventarios(co):
    """Propiedad por categoría desde capital_trabajo() de OPEX (solo stock propio entra al CT)."""
    _, _, _, ct_rows, _ = _correr_opex(co)
    prop = {}
    for r in ct_rows:
        if r["COMPONENTE"] != "INVENTARIO":
            continue
        for pref, cat in MAPA_INVENTARIO_OPEX:
            if r["SUBCOMPONENTE"].startswith(pref):
                v = {"Sí": True, "PENDIENTE": None}.get(r["ENTRA_EN_CT"], False)
                if cat not in prop:
                    prop[cat] = v
                elif prop[cat] is not None:
                    prop[cat] = None if v is None else (prop[cat] or v)
    return prop


def capex_trayectoria(cfg_nombre, escalas):
    """CAPEX por etapa con la lógica de expansión de CAPEX (acciones por etiqueta). Se pasa la trayectoria pedida
    reemplazando temporalmente TRAYECTORIAS del módulo (sin modificar su archivo) y se restaura siempre."""
    key = ("tray", cfg_nombre, tuple(escalas))
    if key in _CACHE:
        return _CACHE[key]
    orig = mcx.TRAYECTORIAS
    try:
        mcx.TRAYECTORIAS = {"FIN": tuple(escalas)}
        with redirect_stdout(io.StringIO()):
            _, resumen = mcx.expansion(cfg_nombre)
    finally:
        mcx.TRAYECTORIAS = orig
    _CACHE[key] = resumen
    return resumen


def leer_precios(ruta=None, niveles=None):
    """Precios con evidencia (CON_PRECIO y nivel dentro del umbral; default E1–E3). Vacío = PENDIENTE; jamás 0.
    REFERENCIA_E4_NO_USABLE nunca se usa."""
    ruta = ruta or ARCHIVO_PRECIOS
    niveles = niveles or UMBRAL_EVIDENCIA_DEFAULT
    out, refs = {}, []
    for r in leer_csv(ruta):
        p = _num(r["PRECIO"])
        if r["ESTADO"] == "CON_PRECIO":
            if p is None or p <= 0:
                raise ErrorFinanciero(f"{r['ID_PRECIO']}: CON_PRECIO exige precio > 0 (un faltante es vacío, nunca 0)")
            usd = a_usd(p, r["MONEDA"], _num(r.get("TC_USADO")), r.get("FECHA_TC"), r.get("TIPO_TC"))
            if r["NIVEL_EVIDENCIA"] in niveles:
                out[f"{r['PRODUCTO']}|{r['CANAL']}|{r['MERCADO']}"] = {"tipo": "CONSTANTE", "usd_kg": usd,
                                                                       "nivel": r["NIVEL_EVIDENCIA"], "fuente": r["FUENTE"]}
            else:
                refs.append(r)
        elif p is not None and r["ESTADO"] in ("PENDIENTE",):
            raise ErrorFinanciero(f"{r['ID_PRECIO']}: estado PENDIENTE con precio cargado")
        elif r["ESTADO"] == "REFERENCIA_E4_NO_USABLE":
            refs.append(r)
    return out, refs


def leer_inputs(ruta=ARCHIVO_INPUTS):
    filas = leer_csv(ruta)
    ids = [f["ID_INPUT"] for f in filas]
    if len(ids) != len(set(ids)):
        raise ErrorFinanciero("ID_INPUT duplicado en inputs_financieros.csv")
    for f in filas:
        if f["ORIGEN"] not in ORIGENES:
            raise ErrorFinanciero(f"{f['ID_INPUT']}: origen {f['ORIGEN']}")
        if f["ORIGEN"] == "EVIDENCIA_REAL" and f["NIVEL_EVIDENCIA"] not in NIVELES:
            raise ErrorFinanciero(f"{f['ID_INPUT']}: evidencia sin nivel E1–E5")
        if f["ORIGEN"] == "PENDIENTE" and f["VALOR"].strip():
            raise ErrorFinanciero(f"{f['ID_INPUT']}: PENDIENTE con valor")
    return filas


def leer_curvas(ruta=ARCHIVO_CURVAS):
    cur = {}
    for r in leer_csv(ruta):
        cur.setdefault(r["CURVA"], []).append({"mes": int(r["MES"]), "utilizacion": _num(r["UTILIZACION"]),
                                               "merma": _num(r["MERMA"]), "eficiencia": _num(r["EFICIENCIA"]),
                                               "costos_extra_usd_mes": _num(r["COSTOS_EXTRA_USD_MES"]),
                                               "origen": r["ORIGEN"]})
    return cur


def _valor_input(txt):
    t = txt.strip()
    if t == "":
        return None
    if t in ("TRUE", "FALSE"):
        return t == "TRUE"
    try:
        return float(t) if any(c in t for c in ".eE") else int(t)
    except ValueError:
        return t


def _set_path(P, path, valor):
    partes = path.split(".")
    d = P
    for p_ in partes[:-1]:
        if d.get(p_) is None:
            d[p_] = {}
        d = d[p_]
    d[partes[-1]] = valor


def _get_path(P, path):
    d = P
    for p_ in path.split("."):
        if not isinstance(d, dict) or p_ not in d:
            return None
        d = d[p_]
    return d


UNIVERSO_DIM = {   # universo declarado en un override → atributo de la arquitectura que debe tenerlo (TF-004)
    "FAENA_PROPIA": ("faena", {"propia"}), "FAENA_FACON": ("faena", {"facon"}), "FACON": ("faena", {"facon"}),
    "INCUBACION": ("pollito", {"incubacion"}), "INCUBACION_PROPIA": ("pollito", {"incubacion"}),
    "POLLITO_COMPRADO": ("pollito", {"compra"}), "PLANTA_ALIMENTO": ("alimento", {"propia"}),
    "PLANTA_ALIMENTO_PROPIA": ("alimento", {"propia"}), "ALIMENTO_PROPIO": ("alimento", {"propia"}),
    "ALIMENTO_COMPRADO": ("alimento", {"compra"}), "ALIMENTO_FACON": ("alimento", {"facon"}),
    "GRANJAS_PROPIAS": ("granjas", {"propias", "mixto"}), "GRANJAS_INTEGRADAS": ("granjas", {"integradas", "mixto"}),
    "FLOTA_PROPIA": ("flota", {"propia", "mixto"}), "RENDERING": ("rendering", {True}), "REPRODUCTORAS": ("reproductoras", {True})}
DIMS_ARQ = ("faena", "granjas", "pollito", "alimento", "flota", "frio", "subproductos", "rendering", "reproductoras")
COL_MAESTRA = {"faena": "FAENA", "granjas": "GRANJAS", "pollito": "POLLITO", "alimento": "ALIMENTO", "flota": "FLOTA",
               "frio": "FRIO", "subproductos": "SUBPRODUCTOS", "rendering": "RENDERING", "reproductoras": "UPSTREAM_REPRODUCTORAS"}


def fila_maestra(configuracion, variante):
    """Fila de 00_gestion_proyecto/arquitecturas_maestras.csv de la corrida (base o variante)."""
    filas = leer_csv(ARCHIVO_ARQ_MAESTRAS)
    if variante and variante != "BASE":
        f = [r for r in filas if r["ESCENARIO_REFERENCIA"] == variante]
    else:
        f = [r for r in filas if r["CONFIGURACION"] == configuracion and r["TIPO"] == "CONFIGURACION_BASE"]
    if not f:
        raise ErrorFinanciero(f"{OVERRIDE_INCOMPATIBLE}: {configuracion}/{variante} no figura en arquitecturas_maestras.csv")
    return f[0]


def contexto_override(configuracion, variante, escala, cc, co):
    """Arquitectura y módulos de la corrida contra los que se valida un override de usuario."""
    m = fila_maestra(configuracion, variante)
    dims_m = {k: m[c].split(" ")[0] for k, c in COL_MAESTRA.items()}
    if any(dims_m[k] != str(cc[k]) for k in DIMS_ARQ):
        raise ErrorFinanciero(f"{OVERRIDE_INCOMPATIBLE}: arquitecturas_maestras.csv no coincide con la corrida {configuracion}/{variante}")
    filas_c, _, _ = _correr_capex(cc)
    filas_o = _correr_opex(co)[0]
    return {"CONFIGURACION": configuracion, "VARIANTE": variante or "BASE", "ESCALA": escala, "cc": cc,
            "capex_mod": {f["MODULO"] for f in filas_c if f["COSTEA"] and f["TITULAR"] == "EMPRESA"} | {"TOTAL_ETAPA"},
            "opex_mod": {f["MODULO_ARQ"] for f in filas_o if f["COSTEA"] and f.get("MODULO_ARQ")}}


def verificar_override(meta, ctx, tipo, modulo=None):
    """Compatibilidad de un override de usuario (CAPEX u OPEX) con la arquitectura de la corrida (TF-004). Devuelve la
    lista de incompatibilidades (vacía = compatible). Nunca corrige el escenario ni usa el valor en silencio."""
    meta = meta or {}
    mot = [f"falta {k}" for k in CAMPOS_META_OVERRIDE if meta.get(k) in (None, "")]
    if mot:
        return mot
    if meta["CONFIGURACION"] != ctx["CONFIGURACION"]:
        mot.append(f"CONFIGURACION {meta['CONFIGURACION']} ≠ corrida {ctx['CONFIGURACION']}")
    if str(meta["VARIANTE"]) != ctx["VARIANTE"]:
        mot.append(f"VARIANTE {meta['VARIANTE']} ≠ corrida {ctx['VARIANTE']}")
    try:
        if int(meta["ESCALA"]) != int(ctx["ESCALA"]):
            mot.append(f"ESCALA {meta['ESCALA']} ≠ etapa {ctx['ESCALA']}")
    except (TypeError, ValueError):
        mot.append(f"ESCALA {meta['ESCALA']!r} inválida")
    mod = modulo or meta["MODULO"]
    permitidos = ctx["capex_mod"] if tipo == "CAPEX" else ctx["opex_mod"]
    if mod not in permitidos:
        mot.append(f"MÓDULO {tipo} {mod} no existe en {ctx['CONFIGURACION']}/{ctx['VARIANTE']} ({', '.join(sorted(permitidos))})")
    u = str(meta["UNIVERSO"]).upper()
    if u in UNIVERSO_DIM:
        dim, vals = UNIVERSO_DIM[u]
        if ctx["cc"][dim] not in vals:
            mot.append(f"UNIVERSO {u} requiere {dim} ∈ {sorted(map(str, vals))}; la arquitectura tiene {dim} = {ctx['cc'][dim]}")
    return mot


VARIABLES_ESPECIALES = ("curva_rampup", "demanda_referencia_02", "mix_demanda", "dias_pago", "dias_stock",
                        "propiedad_rendimientos_validados", "demanda", "financiamiento", "umbral_evidencia_publicacion")


def construir_entrada(nombre, configuracion, escalas, modo, plantilla=None, usuario=None, escenario_capex=None,
                      configuracion_por_fase=None):
    """Arma la entrada del motor para una configuración del mapa y una escala o trayectoria. Capas:
    evidencia (módulos y CSV dentro del UMBRAL_EVIDENCIA_PUBLICACION) → escenario del usuario → plantilla/supuesto
    → PENDIENTE. Aparte, solo en escenario, la capa OVERRIDE_SIMULACION evalúa otro valor sin tocar el observado.
    configuracion_por_fase: interfaz preparada; hoy solo admite la MISMA configuración en todas las etapas
    (una transición C0→C1→C2→C3 no tiene CAPEX ni OPEX de transición modelados: LIMITACION_ACTUAL_EXPANSION)."""
    usuario = copy.deepcopy(usuario or {})
    if usuario and modo != "ESCENARIO":
        raise ErrorFinanciero("los inputs de usuario solo existen en MODO ESCENARIO")
    cpf = list(configuracion_por_fase or usuario.get("configuracion_por_fase") or [configuracion] * len(escalas))
    if len(cpf) != len(escalas):
        raise ErrorFinanciero("configuracion_por_fase: una configuración por etapa")
    if any(c_ != configuracion for c_ in cpf):
        raise ErrorFinanciero(f"TRANSICION_DE_ARQUITECTURA_NO_MODELADA {cpf}: el motor solo expande la MISMA configuración "
                              "por escala; el CAPEX/OPEX de pasar de una arquitectura a otra no existe en 19/20")
    P = entrada_vacia(nombre, modo)
    T = Traza(nombre, modo)
    P["configuracion"] = configuracion
    P["trayectoria"] = "→".join(str(e) for e in escalas)
    filas_in = leer_inputs()
    umbral = umbral_evidencia(filas_in)
    P["umbral_evidencia"] = umbral
    vals_usr = {k: v for k, v in usuario.get("valores", {}).items() if not k.startswith("_")}
    ev_rows = {f["VARIABLE"]: f for f in filas_in if f["ESCENARIO"] == "EVIDENCIA"}
    pl_rows = {f["VARIABLE"]: f for f in filas_in if plantilla and f["ESCENARIO"] == plantilla}
    variables = sorted(set(ev_rows) | set(pl_rows) | set(vals_usr))
    resueltos = {}
    for var in variables:
        ev = ev_rows.get(var)
        evid = (_valor_input(ev["VALOR"]), ev["NIVEL_EVIDENCIA"], ev["FUENTE"]) if ev and ev["ORIGEN"] == "EVIDENCIA_REAL" else None
        sup_row = ev if ev and ev["ORIGEN"] == "SUPUESTO_MODELO" else pl_rows.get(var)
        sup = (_valor_input(sup_row["VALOR"]), sup_row["ID_INPUT"]) if sup_row and sup_row["ORIGEN"] == "SUPUESTO_MODELO" else None
        v, org, niv, fte = resolver(var, modo, evid, vals_usr.get(var), sup, umbral)
        resueltos[var] = v
        fila = ev or pl_rows.get(var) or {}
        T.add(var, v, fila.get("UNIDAD", ""), org, "inputs_financieros.csv" if org != "ESCENARIO_USUARIO" else "escenario del usuario",
              fila.get("ID_INPUT", var), niv, fila.get("OBSERVACIONES", "") if org == "PENDIENTE" else fte)
        base_var = var.split(".")[0]
        if v is not None and base_var not in VARIABLES_ESPECIALES:
            _set_path(P, var, v)
    # 0. OVERRIDE_SIMULACION (solo escenario): evalúa otro valor; el observado queda en la traza y en la base intacta
    P["overrides_simulacion"] = []
    for var, v in (usuario.get("override_simulacion") or {}).items():
        if var.startswith("_"):
            continue
        obs = resueltos.get(var)
        resueltos[var] = v
        if var.split(".")[0] not in VARIABLES_ESPECIALES:
            _set_path(P, var, v)
        P["overrides_simulacion"].append(var)
        T.add(var, v, "", "ESCENARIO_USUARIO", "override_simulacion", var, "",
              f"OVERRIDE_SIMULACION: VALOR_OBSERVADO={obs!r}; VALOR_EVALUADO_ESCENARIO={v!r}; {ETIQUETA_SIM}")
    # 1. productos (balance 04; rutas del preset; propiedad de subproductos en façon según contrato)
    cc0, co0 = configs(escenario_capex or f"{configuracion}-{escalas[0]}")
    destino_c = "contrato_facon" if cc0["faena"] == "facon" else "venta_directa"
    prods, meta = productos_balance(cc0["config_producto"], None, destino_c)
    P["productos"], P["meta_productos"] = prods, meta
    P["validacion_rendimientos"] = bool(resueltos.get("propiedad_rendimientos_validados"))
    for p, x in prods.items():
        T.add(f"kg_ave.{p}", x["kg_ave"], "kg comercial/ave", "SUPUESTO_MODELO" if x["kg_ave"] is not None else "PENDIENTE",
              "04_balance_masa/modelo_balance_masa.py vía 23_plan_expansion/modelo_escala.py ITEMS", p, "",
              f"config. {cc0['config_producto']}, 2,9 kg vivo, destino C = {destino_c}; modelo físico sin ensayo en planta (DPV-060)")
    # 2. etapas: CAPEX, OPEX, activos, ramp-up
    tray = capex_trayectoria(configuracion, escalas) if len(escalas) > 1 else None
    curvas = leer_curvas()
    nombre_curva = resueltos.get("curva_rampup")
    usr_et = usuario.get("etapas", [])
    override_total = usuario.get("OVERRIDE_TOTAL_ARQUITECTURA") is True
    if usuario.get("OVERRIDE_TOTAL_ARQUITECTURA") not in (None, True, False):
        raise ErrorFinanciero("OVERRIDE_TOTAL_ARQUITECTURA: TRUE / FALSE (declaración explícita)")
    P["override_total"] = override_total
    for j, E in enumerate(escalas):
        cc, co = configs(escenario_capex if (escenario_capex and len(escalas) == 1) else f"{configuracion}-{E}")
        e = etapa_vacia(f"E{j + 1}-{E}", E, mcx.dias_anio(cc), "INICIAL" if j == 0 else "FECHA")
        ue = usr_et[j] if j < len(usr_et) else {}
        if modo == "ESCENARIO" and any(ue.get(c) is not None for c in ("capex_usd", "activos", "opex_rubros")):
            if override_total:
                T.add(f"{e['id']}.OVERRIDE_TOTAL_ARQUITECTURA", True, "—", "ESCENARIO_USUARIO", "escenario del usuario",
                      "OVERRIDE_TOTAL_ARQUITECTURA", "", f"{ETIQUETA_OVERRIDE_TOTAL}: CAPEX/OPEX del usuario NO verificados contra "
                      "la arquitectura; PERDIDA_DE_TRAZABILIDAD_PARCIAL (módulos, universos y completitud sin control)")
            else:
                ctx = contexto_override(configuracion, escenario_capex if len(escalas) == 1 else None, E, cc, co)
                malos = []
                if ue.get("capex_usd") is not None or ue.get("activos") is not None:
                    malos += [f"CAPEX: {m}" for m in verificar_override(ue.get("capex_meta"), ctx, "CAPEX")]
                    for a in ue.get("activos") or []:
                        am = a.get("meta") or ue.get("capex_meta")
                        mod_a = (a.get("meta") or {}).get("MODULO") or (a["clase"].split(":")[0] if ":" in a["clase"] else None)
                        if mod_a is None:
                            malos.append(f"activo {a['clase']}: sin MODULO")
                        else:
                            malos += [f"activo {a['clase']}: {m}" for m in verificar_override(am, ctx, "CAPEX", mod_a)]
                for r in ue.get("opex_rubros") or []:
                    malos += [f"OPEX {r.get('rubro')}: {m}" for m in verificar_override(r.get("meta"), ctx, "OPEX")]
                if malos:
                    raise ErrorFinanciero(f"{OVERRIDE_INCOMPATIBLE} ({e['id']}): " + "; ".join(dict.fromkeys(malos)))
                if ue.get("opex_rubros") is not None:
                    e["opex_modulos_requeridos"] = sorted(ctx["opex_mod"])
        if j == 0:
            cap, niv, mot = capex_desde_modulo(cc, umbral)
        else:
            st_ = [r for r in tray if r["ESCALA"] == E][0]
            completo = st_["CONCEPTOS_SIN_COSTO_ETAPA"] == 0 and capex_desde_modulo(cc, umbral)[0] is not None
            cap, niv = (st_["CAPEX_ETAPA_CON_PRECIO_USD"], "E3") if completo else (None, "PENDIENTE")
            mot = (f"expansión {escalas[j - 1]}→{E}: {st_['CONCEPTOS_SIN_COSTO_ETAPA']} conceptos sin costo en la etapa "
                   "(prima de ampliación DPV-086)")
        e["capex_usd"], o_, _, _ = resolver("capex_usd", modo, (cap, niv, "19_capex") if cap is not None else None, ue.get("capex_usd"),
                                            None, umbral)
        e["motivo_capex"] = mot
        T.add(f"{e['id']}.capex_usd", e["capex_usd"], "USD", o_, "19_capex/modelo_capex.py", "TOTAL_PRELIMINAR_USD" if j == 0 else
              "expansion(): CAPEX_ETAPA", niv if o_ == "EVIDENCIA_REAL" else "", mot)
        rub, niv_o, mot_o = opex_desde_modulo(co, umbral)
        e["opex_rubros"], o_, _, _ = resolver("opex_rubros", modo, (rub, niv_o, "20_opex") if rub is not None else None,
                                              ue.get("opex_rubros"), None, umbral)
        e["motivo_opex"] = mot_o
        T.add(f"{e['id']}.opex_rubros", f"{len(e['opex_rubros'])} rubros" if e["opex_rubros"] else None, "USD/año escala plena",
              o_, "20_opex/modelo_opex.py", "registro_costos_operativos (COSTO_CALCULADO_USD_ANIO, NATURALEZA, PCT_VARIABLE)",
              niv_o if o_ == "EVIDENCIA_REAL" else "", mot_o)
        act, mot_a = activos_desde_boq(cc) if j == 0 else (None, "activos de expansión: vida útil PENDIENTE (DPV-167)")
        e["activos"], o_, _, _ = resolver("activos", modo, (act, "E3", "19_capex") if act else None, ue.get("activos"),
                                          None, umbral)
        e["configuracion"] = cpf[j]
        T.add(f"{e['id']}.activos", "definidos" if e["activos"] else None, "clase", o_, "19_capex/boq_capex.csv",
              "VIDA_UTIL_ANIOS, VALOR_RESIDUAL, COSTO_REEMPLAZO", "", mot_a)
        curva = ue.get("rampup") or (curvas.get(nombre_curva) if nombre_curva else None)
        if modo == "EVIDENCIA":
            curva = None                            # ninguna curva tiene evidencia (DEC-090)
        e["rampup"] = copy.deepcopy(curva)
        inef = usuario.get("rampup_ineficiencias") if modo == "ESCENARIO" else None
        if e["rampup"] and inef:
            for r in e["rampup"]:
                for c_ in ("merma", "eficiencia", "costos_extra_usd_mes"):
                    if r.get(c_) is None and inef.get(c_) is not None:
                        r[c_] = inef[c_]
            T.add(f"{e['id']}.rampup_ineficiencias", inef, "—", "ESCENARIO_USUARIO", "escenario del usuario",
                  "merma / eficiencia / costos extra", "", "declaración del usuario (no es dato)")
        T.add(f"{e['id']}.rampup", nombre_curva if (curva and not ue.get("rampup")) else ("usuario" if curva else None), "curva",
              "ESCENARIO_USUARIO" if ue.get("rampup") else ("SUPUESTO_MODELO" if curva else "PENDIENTE"), "curvas_rampup.csv",
              "CURVA", "", "plantilla ilustrativa SIN fuente (SUP-196)" if curva else "curva de ramp-up PENDIENTE (DEC-090)")
        e["curva_desembolso"] = ue.get("curva_desembolso") if modo == "ESCENARIO" else None
        e["iva_capex"] = copy.deepcopy(ue.get("iva_capex")) if modo == "ESCENARIO" else None   # TF-076
        T.add(f"{e['id']}.curva_desembolso", e["curva_desembolso"], "[offset_mes, fracción]",
              "ESCENARIO_USUARIO" if e["curva_desembolso"] else "PENDIENTE", "", "CURVA_DE_DESEMBOLSO_CAPEX", "",
              "cronograma de obra, anticipos y plazos de entrega PENDIENTES (DPV-086, DPV-167)")
        if j > 0 and modo == "ESCENARIO" and ue.get("entrada"):
            e["entrada"].update(ue["entrada"])
        # días de pago por grupo de proveedor (inputs dias_pago.<grupo>)
        for r in e["opex_rubros"] or []:
            if r.get("es_compra") and r.get("dias_pago") is None:
                r["dias_pago"] = resueltos.get(f"dias_pago.{r['grupo_proveedor']}")
        P["etapas"].append(e)
    # 3. inventarios: propiedad desde OPEX; días desde inputs
    prop = propiedad_inventarios(co0)
    P["inventarios"] = {}
    for cat in CATEGORIAS_INVENTARIO:
        if cat not in prop:
            continue
        P["inventarios"][cat] = {"propiedad_empresa": prop[cat], "dias": resueltos.get(f"dias_stock.{cat}"),
                                 "base": BASE_INVENTARIO[cat]}
        T.add(f"inventario.{cat}.propiedad_empresa", prop[cat], "bool", "SUPUESTO_MODELO" if prop[cat] is not None else "PENDIENTE",
              "20_opex/capital_trabajo_opex.csv", "PROPIEDAD_EMPRESA / ENTRA_EN_CT", "", "solo stock propio entra al CT")
    # 4. precios
    precios_ev, refs = leer_precios(None, umbral)
    P["precios"] = dict(precios_ev)
    for k, v in usuario.get("precios", {}).items():
        if isinstance(v, dict) and "por_anio" in v:
            v["por_anio"] = {int(a): x for a, x in v["por_anio"].items()}
        if k not in P["precios"] and modo == "ESCENARIO":
            P["precios"][k] = v                     # el escenario completa; nunca reemplaza una evidencia
    for k, v in (usuario.get("override_precios") or {}).items():
        if modo != "ESCENARIO" or k.startswith("_"):
            continue
        obs = P["precios"].get(k)
        nuevo = dict(v)
        nuevo.update({"origen": "OVERRIDE_SIMULACION", "observado": copy.deepcopy(obs)})
        P["precios"][k] = nuevo
        P["overrides_simulacion"].append(f"precio:{k}")
        T.add(f"PRECIO_EVALUADO_ESCENARIO.{k}", v, "USD/kg", "ESCENARIO_USUARIO", "override_precios", k,
              (obs or {}).get("nivel", ""), f"PRECIO_OBSERVADO={(obs or {}).get('usd_kg')!r} "
              f"(fuente {(obs or {}).get('fuente', '—')}); la base no se modifica; {ETIQUETA_SIM}")
    for r in refs:
        T.add(f"precio_referencia.{r['ID_PRECIO']}", r["PRECIO"], f"{r['MONEDA']}/{r['UNIDAD']}", "PENDIENTE",
              "base_precios_venta.csv", r["ID_PRECIO"], r["NIVEL_EVIDENCIA"], "referencia E4 [PVDP]: NO se usa como precio")
    # 5. canales
    for k, v in usuario.get("canales", {}).items():
        if modo == "ESCENARIO":
            P["canales"].setdefault(k, {})
            for c_, x in v.items():
                if P["canales"][k].get(c_) is None:
                    P["canales"][k][c_] = x
    # 6. demanda: evidencia (DOCUMENTADA / ASEGURADA con E1–E3) ∪ escenario; 02 como referencia de escenario
    lineas = []
    for f in filas_in:
        if f["ESCENARIO"] == "EVIDENCIA" and f["VARIABLE"].startswith("demanda.") and f["ORIGEN"] == "EVIDENCIA_REAL" and \
                f["NIVEL_EVIDENCIA"] in umbral:
            prod, canal, merc, cat = f["VARIABLE"].split(".")[1:5]
            lineas.append({"id": f["ID_INPUT"], "producto": prod, "canal": canal, "mercado": merc, "categoria": cat,
                           "kg_mes": convertir_demanda(_valor_input(f["VALOR"]), f["UNIDAD"]), "prioridad": 1})
    if modo == "ESCENARIO":
        for i, l in enumerate(usuario.get("demanda", [])):
            l = dict(l)
            l.setdefault("id", f"U{i + 1:02d}")
            l.setdefault("mercado", "INTERNO")
            l.setdefault("categoria", "ESCENARIO")
            if "valor" in l:
                l["kg_mes"] = convertir_demanda(l.pop("valor"), l.pop("unidad"))
            lineas.append(l)
        ref, mix = resueltos.get("demanda_referencia_02"), resueltos.get("mix_demanda") or usuario.get("mix_demanda")
        if ref:
            fila02 = {r["id"]: r for r in leer_csv(ARCHIVO_DEMANDA)}[ref]
            T.add("demanda_referencia_02", f"{fila02['total_kg_dia']} kg/día calendario", "kg/día", "SUPUESTO_MODELO",
                  "02_clientes_demanda/escenarios_demanda.csv", ref, "", f"{fila02['clasificacion_dato']}: {fila02['observaciones']}")
            if isinstance(mix, dict):
                canales02 = {"supermercados": "supermercados_kg_dia", "mayoristas": "mayoristas_distribuidores_kg_dia",
                             "carnicerias_pollerias": "carnicerias_pollerias_kg_dia", "gastronomia": "gastronomia_kg_dia",
                             "industria": "industria_kg_dia", "otros": "otros_canales_kg_dia", "exportacion": "exportacion_kg_dia"}
                for canal, col in canales02.items():
                    kg = _num(fila02[col]) or 0.0
                    for prod, fr in mix.items():
                        if kg * fr > 0:
                            lineas.append({"id": f"{ref}-{canal}-{prod}", "producto": prod, "canal": canal,
                                           "mercado": "INTERNO" if canal != "exportacion" else "EXPORTACION",
                                           "categoria": "ESCENARIO", "kg_mes": convertir_demanda(kg * fr, "kg/dia"),
                                           "prioridad": 1})
            else:
                T.add("mix_demanda", None, "fracción por producto", "PENDIENTE", "02_clientes_demanda/supermercados.md §2.2",
                      "M1–M3", "", "mix por producto no elegido (DPV-037): sin mix no hay ventas por producto")
        P["categorias_demanda_usadas"] = tuple(usuario.get("categorias_demanda_usadas", CATEGORIAS_DEMANDA))
        P["alfa_negociada"] = usuario.get("alfa_negociada")
    P["demanda"] = lineas or None
    if not lineas:
        T.add("demanda", None, "kg/mes", "PENDIENTE", "02_clientes_demanda", "categorías A/B", "",
              "demanda A+B documentada ≈ 0 y no cuantificada; los ~90 supermercados son canal potencial (SUP-004)")
    # 7. resto de bloques del usuario (solo escenario; nunca sobre evidencia)
    if modo == "ESCENARIO":
        for k in ("financiamiento", "stress", "inventario_max_meses"):
            if usuario.get(k) is not None:
                P[k] = usuario[k]
        if usuario.get("inventarios"):
            for cat, x in usuario["inventarios"].items():
                P["inventarios"].setdefault(cat, {"base": BASE_INVENTARIO.get(cat, "OPEX_TOTAL")})
                for c_, v in x.items():
                    if P["inventarios"][cat].get(c_) is None:
                        P["inventarios"][cat][c_] = v
    return P, T


# ---------------------------------------------------------------------------------------------
# 9. CORRIDAS DE REFERENCIA Y SALIDAS
# ---------------------------------------------------------------------------------------------
def id_corrida(modo, configuracion, escalas, variante=None, trayectoria=None, plantilla=None):
    """Identificador único y reconstruible: MODO | CONFIGURACION | VARIANTE | ESCALAS | TRAYECTORIA | ESCENARIO."""
    return "|".join((modo, configuracion, variante or "BASE", "-".join(str(e) for e in escalas),
                     trayectoria or ("ESCALA_UNICA" if len(escalas) == 1 else "TRAYECTORIA_SIN_NOMBRE"),
                     plantilla or ("SIN_PLANTILLA" if modo == "ESCENARIO" else "EVIDENCIA")))


def corridas_referencia():
    """61 corridas = 42 MODO EVIDENCIA + 19 MODO ESCENARIO.
    EVIDENCIA: 5 configuraciones base × 4 escalas (20) + 19 variantes del mapa a su escala de referencia (19) + C1 en
    las 3 trayectorias multietapa T1–T3 (3). T4 (20.000 inicial) NO se repite en evidencia: es idéntica a C1-20000.
    ESCENARIO: 3 plantillas × 5 configuraciones base a 10.000 (15) + plantilla BASE × C1 × 4 trayectorias (4).
    Las plantillas no tienen precios, mix, cronograma ni impuestos: muestran qué falta (no se rellena)."""
    out = []

    def add(nombre, modo, cfg, escalas, variante=None, trayectoria=None, plantilla=None):
        out.append({"ID_CORRIDA": id_corrida(modo, cfg, escalas, variante, trayectoria, plantilla), "NOMBRE": nombre,
                    "MODO": modo, "CONFIGURACION": cfg, "ESCALAS": tuple(escalas), "VARIANTE": variante,
                    "TRAYECTORIA": trayectoria, "PLANTILLA": plantilla})
    for r in mapa_arquitecturas():
        if r["TIPO"] == "CONFIGURACION_BASE":
            for E in mcx.ESCALAS_REF:
                add(f"EVI-{r['CONFIGURACION']}-{E}", "EVIDENCIA", r["CONFIGURACION"], (E,))
        else:
            ref = r["ESCENARIO_REFERENCIA"]
            add(f"EVI-{ref}", "EVIDENCIA", r["VARIANTE_DE"], (int(ref.split("-")[1]),), ref)
    for t, esc in TRAYECTORIAS_FIN.items():
        if len(esc) > 1:
            add(f"EVI-C1-{t}", "EVIDENCIA", "C1", esc, None, t)
    for pl in PLANTILLAS:
        for cfg in ("C0", "C1", "C2", "C3", "CF"):
            add(f"ESC-{pl.split('_')[1]}-{cfg}-10000", "ESCENARIO", cfg, (10000,), None, None, pl)
    for t, esc in TRAYECTORIAS_FIN.items():
        add(f"ESC-BASE-C1-{t}", "ESCENARIO", "C1", esc, None, t, "PLANTILLA_BASE")
    return out


def firma_corrida(c):
    """Contenido económico de una corrida (para detectar duplicados con nombres distintos)."""
    partes = [c["MODO"], c["PLANTILLA"] or ""]
    for E in c["ESCALAS"]:
        cc, co = configs(c["VARIANTE"] if (c["VARIANTE"] and len(c["ESCALAS"]) == 1) else f"{c['CONFIGURACION']}-{E}")
        partes.append(json.dumps({k: co[k] for k in sorted(co) if k != "nombre"}, sort_keys=True, default=str))
    return "||".join(partes)


def correr_escenario(nombre, configuracion, escalas, modo, plantilla=None, usuario=None, escenario_capex=None,
                     meta=None):
    P, T = construir_entrada(nombre, configuracion, escalas, modo, plantilla, usuario, escenario_capex)
    R = simular(P)
    res = resultados(R)
    res["ESCALAS"] = "→".join(str(e) for e in escalas)
    res["PLANTILLA"] = plantilla or ""
    meta = meta or {"ID_CORRIDA": id_corrida(modo, configuracion, escalas, escenario_capex, None, plantilla),
                    "VARIANTE": escenario_capex, "TRAYECTORIA": None}
    res["ID_CORRIDA"], res["VARIANTE"], res["TRAYECTORIA_ID"] = meta["ID_CORRIDA"], meta["VARIANTE"] or "BASE", \
        meta["TRAYECTORIA"] or ("ESCALA_UNICA" if len(escalas) == 1 else "")
    res["ALCANCE_EXPANSION"] = ("" if len(escalas) == 1 else
                                "LIMITACION_ACTUAL_EXPANSION_C1 (corridas de referencia); misma configuración por escala, "
                                "sin transición de arquitectura")
    return P, T, R, res


CAMPOS_ESC = ["ID_CORRIDA", "ESCENARIO", "MODO", "ETIQUETA", "CONFIGURACION", "VARIANTE", "ESCALAS", "TRAYECTORIA_ID",
              "PLANTILLA", "ALCANCE_EXPANSION", "UMBRAL_EVIDENCIA", "OVERRIDES_SIMULACION", "HORIZONTE_ANIOS",
              "MODELO_MONETARIO", "CONVENCION_DESCUENTO", "TASA_DESCUENTO_ANUAL_EFECTIVA",
              "TASA_DESCUENTO_MENSUAL_EQUIVALENTE", "BASE_FLUJO", "CAPEX_INICIAL", "CAPEX_EXPANSION", "CAPEX_REPOSICION", "CT_INICIAL", "CT_MAXIMO",
              "OTROS_REQUERIMIENTOS_CAJA", "FONDOS_INICIALES", "PICO_REQUERIMIENTO_FONDOS", "MES_VALLE_CAJA",
              "VENTA_BRUTA_ULTIMO_ANIO", "INGRESO_NETO_ULTIMO_ANIO", "EBITDA_ULTIMO_ANIO", "MARGEN_EBITDA_ULTIMO_ANIO",
              "U_TECNICA_ULTIMO_ANIO", "U_COMERCIAL_REQUERIDA_ULTIMO_ANIO", "U_EFECTIVA_ULTIMO_ANIO",
              "BE_UTILIZACION_EBITDA", "BE_AVES_ANIO_EBITDA", "BE_PRECIO_MEDIO_USD_KG_EBITDA", "BE_ESTADO",
              "VAN", "TIR", "TIR_MENSUAL", "TIR_ESTADO", "MIRR", "PAYBACK_SIMPLE_MESES", "PAYBACK_SIMPLE_ANIOS",
              "PAYBACK_SIMPLE_ESTADO", "PAYBACK_DESCONTADO_MESES", "PAYBACK_DESCONTADO_ANIOS", "PAYBACK_DESCONTADO_ESTADO", "BASE_FLUJO_ACCIONISTA", "APORTES_TOTALES",
              "DEUDA_TOMADA", "VAN_ACCIONISTA", "TIR_ACCIONISTA", "TIR_ACCIONISTA_ESTADO", "CAJA_MINIMA_LEDGER",
              "DSCR_MINIMO"] + [x for f in FLAGS for x in (f, f + "_MOTIVO")] + ["FALTANTES"]

CAMPOS_PER = ["ESCENARIO", "MODO", "ETIQUETA", "CONFIGURACION", "ESCALAS", "PERIODO", "TIPO", "FECHA_INICIO", "ANIO_PROYECTO",
              "ANIO_OPERATIVO", "FASE"]
SERIES_ER = ["capacidad_aves", "aves_faenadas", "u_tecnica", "u_comercial", "u_efectiva", "kg_producidos", "kg_vendidos",
             "kg_excedente_sin_venta", "venta_bruta"] + [f"venta_{c}" for c in CATEGORIAS_INGRESO] + [
             "descuentos", "bonificaciones", "devoluciones", "comisiones", "derechos_exportacion", "ingreso_neto",
             "opex_variable", "opex_fijo", "opex_semifijo", "opex_semivariable", "opex_total", "costos_extra_rampup",
             "costos_logistica_canal", "costos_exportacion", "impuestos_sobre_ingresos", "otros_impuestos", "ebitda",
             "depreciacion", "ebit", "deuda_interes", "impuesto_operativo", "impuesto_con_deuda"]
SERIES_FCFF = ["ebitda", "depreciacion", "ebit", "impuesto_operativo", "capex_inicial", "capex_expansion", "capex_reposicion",
               "capex_total", "delta_ct", "flujo_iva", "valor_terminal", "fcff_pre", "fcff"]
SERIES_ACC = ["fcff_pre", "impuesto_con_deuda", "deuda_alta", "deuda_interes", "deuda_comision", "deuda_amort",
              "deuda_remanente_cierre", "fcfe_pre", "fcfe", "aportes", "dividendos", "caja", "cfads", "servicio_deuda"]
SERIES_CT = ["inv_materias_primas", "inv_alimento", "inv_packaging", "inv_repuestos", "inv_producto_terminado",
             "inv_activo_biologico", "inv_otros", "inventarios", "cxc", "caja_operativa", "cxp", "ct", "delta_ct",
             "iva_saldo_favor"]
SERIES_DEUDA = ["deuda_saldo_ini", "deuda_alta", "deuda_interes", "deuda_amort", "deuda_comision", "deuda_saldo_fin"]
FLAG_TABLA = {"estado_resultados": "PUBLICABLE_EBITDA", "flujo_caja_proyecto": "PUBLICABLE_FLUJO",
              "flujo_accionista": "PUBLICABLE_FLUJO_ACCIONISTA", "capital_trabajo_financiero": "PUBLICABLE_FLUJO",
              "deuda": "PUBLICABLE_FLUJO_ACCIONISTA"}


def filas_periodicas(R, res, series, tabla):
    """Una fila por período. Si no hay línea de tiempo, UNA fila que explica por qué. Valores None = no publicables."""
    P = R["P"]
    comun = {"ESCENARIO": P["nombre"], "MODO": P["modo"], "ETIQUETA": res["ETIQUETA"], "CONFIGURACION": P["configuracion"],
             "ESCALAS": res.get("ESCALAS", "")}
    flag = FLAG_TABLA[tabla]
    estado = (res[flag + "_MOTIVO"] if res[flag] else res[flag + "_MOTIVO"])
    if R["N"] == 0:
        return [dict(comun, PERIODO="—", FASE="SIN_LINEA_DE_TIEMPO", ESTADO_PUBLICACION=estado)]
    ag = {s: agregar(R, s) for s in series}
    out = []
    for i, p in enumerate(R["periodos"]):
        f = dict(comun, **{k: p[k] for k in ("PERIODO", "TIPO", "FECHA_INICIO", "ANIO_PROYECTO", "ANIO_OPERATIVO", "FASE")})
        for s in series:
            f[s.upper()] = ag[s][i]
        f["ESTADO_PUBLICACION"] = estado
        out.append(f)
    return out


ESTADOS_COMPLETITUD = ("COMPLETO", "PARCIAL", "PENDIENTE", "NO_APLICA")
BLOQUES_COMPLETITUD = {   # bloque pedido → bloques del motor
    "DEMANDA": ("DEMANDA",), "PRODUCCION": ("PRODUCCION", "RAMPUP", "TIEMPO"), "PRECIOS": ("PRECIOS",),
    "INGRESOS": ("DEMANDA", "PRODUCCION", "RAMPUP", "TIEMPO", "PRECIOS", "CANALES"), "OPEX": ("OPEX",),
    "CAPEX": ("CAPEX", "DEPRECIACION", "REPOSICION"), "CT": ("CT",), "IMPUESTOS": ("IMPUESTOS_INGRESOS", "GANANCIAS", "IVA"),
    "FINANCIACION": ("FINANCIAMIENTO",), "DESCUENTO": ("DESCUENTO",)}


def completitud(P, R, T):
    """Estado por bloque: COMPLETO (sin faltantes) / PARCIAL (hay estructura o datos parciales) / PENDIENTE /
    NO_APLICA. PARCIAL nunca habilita un resultado."""
    F = R["faltantes"]
    presente = {
        "DEMANDA": P["demanda"] is not None or any(f["VARIABLE"] == "demanda_referencia_02" and f["ORIGEN"] != "PENDIENTE" for f in T.filas),
        "PRODUCCION": P["productos"] is not None, "PRECIOS": bool(P["precios"]),
        "INGRESOS": P["productos"] is not None,
        "OPEX": True, "CAPEX": True,                # estructura 100 % en 19/20 con montos E4 parciales no usados
        "CT": bool(P["inventarios"]), "IMPUESTOS": any(v is not None for v in P["impuestos"].values() if not isinstance(v, bool)),
        "FINANCIACION": P["financiamiento"] is not None, "DESCUENTO": P["tasa_descuento"] is not None}
    out = []
    for b, sub in BLOQUES_COMPLETITUD.items():
        falt = [f"{s}: {x}" for s in sub for x in F[s]]
        estado = "COMPLETO" if not falt else ("PARCIAL" if presente[b] else "PENDIENTE")
        regs = sorted({w.strip("(),;:") for x in falt for w in x.split() if w.strip("(),;:").startswith(("DPV-", "DEC-", "SUP-"))})
        out.append({"ESCENARIO": P["nombre"], "MODO": P["modo"], "CONFIGURACION": P["configuracion"], "ESCALAS": P["trayectoria"],
                    "BLOQUE": b, "ESTADO": estado, "QUE_FALTA": " | ".join(falt), "REGISTROS": ", ".join(regs),
                    "BLOQUEA_RENTABILIDAD": "SÍ" if estado != "COMPLETO" and b != "FINANCIACION" else
                    ("SOLO_FLUJO_ACCIONISTA" if estado != "COMPLETO" else "NO")})
    exp_ = any(l.get("mercado", "INTERNO") != "INTERNO" for l in P["demanda"] or [])
    out.append({"ESCENARIO": P["nombre"], "MODO": P["modo"], "CONFIGURACION": P["configuracion"], "ESCALAS": P["trayectoria"],
                "BLOQUE": "EXPORTACION", "ESTADO": "PARCIAL" if exp_ else "NO_APLICA",
                "QUE_FALTA": "precio FOB/CIF, logística, certificación, halal, derechos y FX por destino (DPV-015, DPV-024, DPV-026)"
                if exp_ else "sin líneas de exportación en la demanda (base sin exportación, SUP-022)",
                "REGISTROS": "DPV-015, DPV-024, DPV-026" if exp_ else "", "BLOQUEA_RENTABILIDAD": "SÍ" if exp_ else "NO"})
    return out


def break_even_filas(R, res):
    P = R["P"]
    out = []
    for base in ("EBITDA", "EBIT"):
        be = (R.get("break_even") or {}).get(base)
        f = {"ESCENARIO": P["nombre"], "MODO": P["modo"], "ETIQUETA": res["ETIQUETA"], "CONFIGURACION": P["configuracion"],
             "ESCALAS": res.get("ESCALAS", ""), "BASE": base, "ANIO": f"A{P['horizonte_anios']:02d}" if R["N"] else "—"}
        pub = res["PUBLICABLE_BREAK_EVEN"] and (base == "EBITDA" or res["PUBLICABLE_FLUJO_AFTER_TAX"] or R["ok"]["ebit"])
        if be and pub:
            f.update({k: be.get(k) for k in CAMPOS_BE if k in be})
            f["ESTADO_PUBLICACION"] = res["PUBLICABLE_BREAK_EVEN_MOTIVO"]
        else:
            f["ESTADO"] = "NO_CALCULABLE"
            f["ESTADO_PUBLICACION"] = res["PUBLICABLE_BREAK_EVEN_MOTIVO"] if not res["PUBLICABLE_BREAK_EVEN"] else \
                "EBIT: falta depreciación (DPV-167)"
        out.append(f)
    return out


CAMPOS_BE = ["ESTADO", "AVES_ANIO", "CAPACIDAD_AVES_ANIO", "U_EFECTIVA", "INGRESO_NETO", "IMPUESTOS_PROPORCIONALES_AL_PRECIO",
             "COSTOS_VARIABLES", "COSTOS_FIJOS", "MARGEN_CONTRIBUCION", "MC_POR_AVE", "KG_VENDIDOS", "PRECIO_MEDIO_BRUTO_USD_KG",
             "REQ_DEMANDA_AVES_ANIO", "BE_AVES_ANIO", "BE_UTILIZACION", "BE_KG_VENDIDOS", "BE_FACTOR_PRECIO",
             "BE_PRECIO_MEDIO_BRUTO_USD_KG"]


def construir_salidas(verbose=True):
    tablas = {k: [] for k in ("escenarios_financieros", "estado_resultados", "flujo_caja_proyecto", "flujo_accionista",
                              "capital_trabajo_financiero", "deuda", "break_even", "completitud_financiera",
                              "mapa_drivers_financieros")}
    corr = corridas_referencia()
    ids = [c["ID_CORRIDA"] for c in corr]
    if len(ids) != len(set(ids)):
        raise ErrorFinanciero("ID_CORRIDA duplicado")
    for c in corr:
        P, T, R, res = correr_escenario(c["NOMBRE"], c["CONFIGURACION"], c["ESCALAS"], c["MODO"], c["PLANTILLA"], None,
                                        c["VARIANTE"], c)
        tablas["escenarios_financieros"].append(res)
        for tabla, series in (("estado_resultados", SERIES_ER), ("flujo_caja_proyecto", SERIES_FCFF),
                              ("flujo_accionista", SERIES_ACC), ("capital_trabajo_financiero", SERIES_CT),
                              ("deuda", SERIES_DEUDA)):
            tablas[tabla] += filas_periodicas(R, res, series, tabla)
        tablas["break_even"] += break_even_filas(R, res)
        tablas["completitud_financiera"] += completitud(P, R, T)
        tablas["mapa_drivers_financieros"] += T.filas
    escribir(SALIDAS["escenarios_financieros"], tablas["escenarios_financieros"], CAMPOS_ESC)
    for tabla, series in (("estado_resultados", SERIES_ER), ("flujo_caja_proyecto", SERIES_FCFF),
                          ("flujo_accionista", SERIES_ACC), ("capital_trabajo_financiero", SERIES_CT), ("deuda", SERIES_DEUDA)):
        escribir(SALIDAS[tabla], tablas[tabla], CAMPOS_PER + [s.upper() for s in series] + ["ESTADO_PUBLICACION"])
    escribir(SALIDAS["break_even"], tablas["break_even"],
             ["ESCENARIO", "MODO", "ETIQUETA", "CONFIGURACION", "ESCALAS", "BASE", "ANIO"] + CAMPOS_BE + ["ESTADO_PUBLICACION"])
    escribir(SALIDAS["completitud_financiera"], tablas["completitud_financiera"],
             ["ESCENARIO", "MODO", "CONFIGURACION", "ESCALAS", "BLOQUE", "ESTADO", "QUE_FALTA", "REGISTROS", "BLOQUEA_RENTABILIDAD"])
    escribir(SALIDAS["mapa_drivers_financieros"], tablas["mapa_drivers_financieros"], Traza.CAMPOS)
    escribir(SALIDAS["casos_prueba_motor"], casos_prueba_resumen(), CAMPOS_CASOS)
    if verbose:
        n_ev = [r for r in tablas["escenarios_financieros"] if r["MODO"] == "EVIDENCIA"]
        print(f"Salidas: {len(tablas['escenarios_financieros'])} corridas ({len(n_ev)} en modo evidencia).")
        for fl in FLAGS:
            print(f"  {fl}: TRUE en {sum(1 for r in tablas['escenarios_financieros'] if r[fl])} de "
                  f"{len(tablas['escenarios_financieros'])}")
    return tablas


# ---------------------------------------------------------------------------------------------
# 10. CASOS DE PRUEBA ARTIFICIALES (son TESTS, no escenarios del proyecto)
# ---------------------------------------------------------------------------------------------
def caso_prueba(H=5, M=0, capex=100.0, ventas_anio=100.0, opex_fijo=60.0, opex_var=0.0, demanda_kg_mes=1.0, escala=1,
                dias=12, tasa=0.10, tasa_gan=None, quebranto=5, dias_cobro=0.0, dias_pago=0.0, pre=0, con=0, com=0, curva=None,
                deudas=None, aportes=None, vida=5, iva=None, modelo="REAL", inflacion=None, curva_desembolso=None,
                activos=None, inventario_max=0, nombre="CASO_PRUEBA", pct_desc=0.0, dividendos=None,
                convencion="MENSUAL"):
    """Caso controlado: 1 producto de 1 kg/ave; capacidad = escala × días ÷ 12 aves/mes; precio = ventas_anio ÷ 12
    por kg con demanda de 1 kg/mes a plena capacidad. Con los valores por defecto: CAPEX 100 en T0, ventas 100/año,
    OPEX fijo 60/año → EBITDA 40/año."""
    P = entrada_vacia(nombre, "ESCENARIO")
    P.update(horizonte_anios=H, meses_detalle=M, meses_preoperacion=pre, meses_construccion=con, meses_commissioning=com,
             tasa_descuento=tasa, modelo_monetario=modelo, base_tasa=modelo, inflacion_anual=inflacion,
             fecha_inicio="2030-01-01", convencion_descuento=convencion)
    P["productos"] = {"pollo_entero": {"kg_ave": 1.0, "categoria_ingreso": "PRODUCTO_PRINCIPAL", "nombre": "prueba"}}
    e = etapa_vacia("E1", escala, dias)
    rub = [{"rubro": "fijo", "grupo_proveedor": "servicios", "naturaleza": "fijo", "costo_pleno_usd_anio": opex_fijo,
            "es_compra": True, "dias_pago": dias_pago, "iva_credito": True}]
    if opex_var:
        rub.append({"rubro": "variable", "grupo_proveedor": "alimento", "naturaleza": "variable",
                    "costo_pleno_usd_anio": opex_var, "es_compra": True, "dias_pago": dias_pago, "iva_credito": True})
    e.update(capex_usd=capex, curva_desembolso=curva_desembolso or [(-(pre + con + com + 1), 1.0)],
             rampup=curva or [{"mes": 1, "utilizacion": 1.0, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}],
             opex_rubros=rub,
             activos=activos or [{"clase": "planta", "capex_usd": capex, "vida_util_anios": vida, "valor_residual_usd": 0.0,
                                  "costo_reemplazo_usd": capex}])
    P["etapas"] = [e]
    P["demanda"] = [{"id": "D1", "producto": "pollo_entero", "canal": "supermercados", "mercado": "INTERNO",
                     "categoria": "ESCENARIO", "kg_mes": demanda_kg_mes, "prioridad": 1}]
    P["categorias_demanda_usadas"] = ("ESCENARIO",)
    cap_kg_mes = escala * dias / 12
    P["precios"] = {"pollo_entero|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": ventas_anio / 12 / cap_kg_mes}}
    P["canales"] = {"supermercados": {"dias_cobro": dias_cobro, "pct_descuentos": pct_desc, "pct_bonificaciones": 0.0,
                                      "pct_devoluciones": 0.0, "pct_comisiones": 0.0, "costo_logistico_usd_kg": 0.0}}
    P["inventarios"] = {}
    P["inventario_max_meses"] = {"pollo_entero": inventario_max}
    P["impuestos"].update(pct_iibb=0.0, pct_tasas_municipales=0.0, otros_impuestos_usd_anio=0.0, tasa_ganancias=tasa_gan,
                          anios_quebranto=quebranto)
    P["iva"] = iva or {"modo": "EXCLUIDO", "alicuota_ventas": None, "alicuota_compras": None, "alicuota_capex": None}
    P["financiamiento"] = {"aportes": aportes if aportes is not None else [(0, capex)], "deudas": deudas or [],
                           "politica_dividendos": dividendos}
    return P


CAMPOS_CASOS = ["CASO", "DESCRIPCION", "CONVENCION_DESCUENTO", "TASA_FISCAL_TEST", "DEPRECIACION_ANUAL",
                "BASE_IMPONIBLE_ANUAL", "IMPUESTO_ANUAL", "FCFF_ANUAL", "BASE_FLUJO", "VAN", "TIR", "TIR_MENSUAL",
                "TIR_ESTADO", "PAYBACK_SIMPLE_MESES", "PAYBACK_SIMPLE_ANIOS", "PAYBACK_DESCONTADO_ANIOS",
                "EBITDA_ULTIMO_ANIO", "BE_UTILIZACION_EBITDA", "FONDOS_INICIALES", "PICO_REQUERIMIENTO_FONDOS",
                "VALOR_ESPERADO_MANUAL", "ETIQUETA"]
# Casos de prueba ARTIFICIALES con nombre propio (nunca "el caso artificial" a secas). Comunes: CAPEX 100 en T0;
# ingresos 100/año; OPEX fijo 60/año; ΔCT 0; sin CAPEX posterior; horizonte 5 años; valor terminal 0; tasa anual
# efectiva 10 %. NO son parámetros del proyecto: la tasa fiscal de test (30 %) solo existe aquí.
CASOS_PRUEBA = (
    ("CP-PRETAX-ANUAL", "PRE-TAX: tasa_ganancias = None; flujos a fin de año (PERIODO_REPORTE anual)",
     dict(convencion="PERIODO_REPORTE"), None,
     "FCFF 40/año; VAN = −100 + 40 × 3,790787 = 51,6315; TIR 28,65 %; payback 2,5 años = 30 meses"),
    ("CP-AFTERTAX-ANUAL", "AFTER-TAX: tasa fiscal de TEST 30 %; depreciación lineal 100 ÷ 5 = 20/año; fin de año",
     dict(convencion="PERIODO_REPORTE", tasa_gan=0.30), 0.30,
     "base imponible = EBITDA 40 − depreciación 20 = 20; impuesto 0,3 × 20 = 6; FCFF 34/año; VAN 28,887; "
     "TIR 20,76 %; payback 100 ÷ 34 = 2,94 años"),
    ("CP-PRETAX-MENSUAL", "Mismo caso PRE-TAX con la convención por defecto del motor: flujo de 40/12 cada mes",
     dict(convencion="MENSUAL"), None,
     "VAN = −100 + Σ_{k=1..60} (40/12) ÷ 1,1^(k/12) ≈ 58,46; payback 30 meses = 2,5 años (difiere del anual por la "
     "oportunidad de los flujos, no por error)"),
    ("CP-SIN-RECUPERO", "PRE-TAX anual con OPEX fijo 120/año (EBITDA −20/año)",
     dict(convencion="PERIODO_REPORTE", opex_fijo=120.0), None, "TIR NO_EXISTE; payback NO_RECUPERADO; pico de fondos 200"),
    ("CP-COBRO-30D", "CP-PRETAX-ANUAL con cobro a 30 días",
     dict(convencion="PERIODO_REPORTE", dias_cobro=30.0), None,
     "CxC = 8,333 × 30 ÷ 30,4167 = 8,22 (ΔCT solo en el primer mes); VAN ≈ 44,16"),
)


def casos_prueba_resumen():
    out = []
    for cid, desc, kw, tg, esperado in CASOS_PRUEBA:
        R = simular(caso_prueba(**kw))
        r = resultados(R)
        dep = agregar(R, "depreciacion")
        imp = agregar(R, "impuesto_operativo") if R["series"]["impuesto_operativo"] is not None else None
        fl = agregar(R, "fcff" if r["BASE_FLUJO"] == "AFTER_TAX" else "fcff_pre")
        y1 = [p["PERIODO"] for p in R["periodos"]].index("A01") if "A01" in [p["PERIODO"] for p in R["periodos"]] else None
        out.append({"CASO": cid, "DESCRIPCION": desc, **{k: r.get(k) for k in CAMPOS_CASOS if k in r},
                    "TASA_FISCAL_TEST": tg if tg is not None else "0 (sin ganancias: PRE_TAX)",
                    "DEPRECIACION_ANUAL": dep[y1] if y1 is not None else sum(dep[1:13]),
                    "BASE_IMPONIBLE_ANUAL": (agregar(R, "ebit")[y1] if (tg is not None and y1 is not None) else "no aplica"),
                    "IMPUESTO_ANUAL": (imp[y1] if (imp and y1 is not None) else 0.0),
                    "FCFF_ANUAL": fl[y1] if y1 is not None else sum(R["series"]["fcff_pre"][1:13]),
                    "VALOR_ESPERADO_MANUAL": esperado, "ETIQUETA": "CASO_PRUEBA_ARTIFICIAL (no es escenario del proyecto)"})
    return out


# ---------------------------------------------------------------------------------------------
# 11. TESTS
# ---------------------------------------------------------------------------------------------
def _cerca(a, b, tol=1e-6):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


def _lanza(fn, *a, **k):
    try:
        fn(*a, **k)
    except (ErrorFinanciero, mb.ErrorBalance, mcx.ErrorCapex, mo.ErrorOpex):
        return True
    return False


def ejecutar_tests(verbose=True):
    T = []

    def test(tid, desc):
        def deco(fn):
            T.append((tid, desc, fn))
            return fn
        return deco

    # ---------------- identidades contables ----------------
    @test("I01", "INGRESO NETO = venta bruta − deducciones")
    def _():
        P = caso_prueba(pct_desc=0.05)
        P["canales"]["supermercados"].update(pct_bonificaciones=0.02, pct_devoluciones=0.01, pct_comisiones=0.03)
        S = simular(P)["series"]
        for k in range(61):
            ded = S["descuentos"][k] + S["bonificaciones"][k] + S["devoluciones"][k] + S["comisiones"][k] + S["derechos_exportacion"][k]
            assert _cerca(S["ingreso_neto"][k], S["venta_bruta"][k] - ded, 1e-9)
        assert _cerca(sum(S["ingreso_neto"]), 500 * (1 - 0.11), 1e-9)

    @test("I02", "EBITDA = ingreso neto − OPEX operativo (sin depreciación, intereses, CAPEX ni CT)")
    def _():
        P = caso_prueba(opex_var=12.0, dias_cobro=45, deudas=[{"id": "D", "monto": 50.0, "tasa": 0.1, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 24,
                                                              "gracia_meses": 0, "metodo": "FRANCES", "capitalizacion_meses": 1, "frecuencia_meses": 1,
                                                              "mes_desembolso": 0}])
        S = simular(P)["series"]
        for k in range(61):
            op = (S["opex_total"][k] + S["costos_logistica_canal"][k] + S["costos_exportacion"][k] + S["impuestos_sobre_ingresos"][k]
                  + S["otros_impuestos"][k] + S["costos_extra_rampup"][k])
            assert _cerca(S["ebitda"][k], S["ingreso_neto"][k] - op, 1e-9)
        assert _cerca(sum(S["ebitda"]), 5 * (100 - 60 - 12), 1e-9)

    @test("I03", "EBIT = EBITDA − depreciación")
    def _():
        S = simular(caso_prueba(tasa_gan=0.3))["series"]
        assert all(_cerca(S["ebit"][k], S["ebitda"][k] - S["depreciacion"][k], 1e-12) for k in range(61))
        assert _cerca(sum(S["depreciacion"]), 100.0)

    @test("I04", "CT = inventarios + CxC + caja − CxP (período a período)")
    def _():
        P = caso_prueba(opex_var=24.0, dias_cobro=30, dias_pago=45)
        P["inventarios"] = {"alimento": {"propiedad_empresa": True, "dias": 15, "base": {"grupos": ["alimento"]}},
                            "packaging": {"propiedad_empresa": False, "dias": 99, "base": "OPEX_TOTAL"}}
        P["dias_caja_operativa"] = 10
        S = simular(P)["series"]
        for k in range(61):
            assert _cerca(S["ct"][k], S["inventarios"][k] + S["cxc"][k] + S["caja_operativa"][k] - S["cxp"][k], 1e-12)
        assert S["inv_packaging"][30] == 0.0                     # stock de terceros no entra
        assert _cerca(S["inv_alimento"][30], 2.0 / DIAS_MES * 15)

    @test("I05", "ΔCT: el flujo usa la variación, no el stock (Σ ΔCT = CT final)")
    def _():
        P = caso_prueba(dias_cobro=30.0)
        R = simular(P)
        S = R["series"]
        assert _cerca(sum(S["delta_ct"]), S["ct"][-1], 1e-12)
        cxc = 100 / 12 / DIAS_MES * 30
        assert _cerca(S["delta_ct"][1], cxc) and all(abs(x) < 1e-12 for x in S["delta_ct"][2:])
        assert _cerca(sum(S["fcff_pre"]), -100 + 5 * 40 - cxc, 1e-9)

    @test("I06", "FCFF cierra: EBIT − impuestos + depreciación − CAPEX − ΔCT + IVA + VT")
    def _():
        P = caso_prueba(tasa_gan=0.35, dias_cobro=20, dias_pago=10, opex_var=10.0)
        S = simular(P)["series"]
        for k in range(61):
            alt = (S["ebit"][k] - S["impuesto_operativo"][k] + S["depreciacion"][k] - S["capex_total"][k] - S["delta_ct"][k]
                   + S["flujo_iva"][k] + S["valor_terminal"][k])
            assert _cerca(S["fcff"][k], alt, 1e-9)

    @test("I07", "Deuda: saldo inicial + altas − amortización = saldo final; continuidad entre meses")
    def _():
        for met in ("FRANCES", "ALEMAN", "BULLET"):
            d = cronograma_deuda({"id": "D", "monto": 100.0, "tasa": 0.12, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 36, "gracia_meses": 6,
                                  "metodo": met, "capitalizacion_meses": 3, "frecuencia_meses": 3, "mes_desembolso": 2}, 60)
            for k in range(61):
                assert _cerca(d["saldo_ini"][k] + d["alta"][k] - d["amort"][k], d["saldo_fin"][k], 1e-9)
                if k:
                    assert _cerca(d["saldo_ini"][k], d["saldo_fin"][k - 1], 1e-12)
            assert abs(d["saldo_fin"][60]) < 1e-9 and _cerca(sum(d["amort"]), 100.0)

    @test("I08", "Caja del accionista cierra período a período (con dividendos)")
    def _():
        P = caso_prueba(dividendos={"pct_caja_excedente": 0.5, "caja_minima_usd": 5.0},
                        deudas=[{"id": "D", "monto": 40.0, "tasa": 0.1, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 24, "gracia_meses": 0,
                                 "metodo": "ALEMAN", "capitalizacion_meses": 6, "frecuencia_meses": 6, "mes_desembolso": 0}], aportes=[(0, 60.0)])
        S = simular(P)["series"]
        caja = 0.0
        for k in range(61):
            caja = caja + S["fcfe_pre"][k] + S["aportes"][k] - S["dividendos"][k]
            assert _cerca(S["caja"][k], caja, 1e-9)
        assert sum(S["dividendos"]) > 0

    @test("I09", "Agregación: Σ períodos de reporte = Σ mensual; saldos = fin de período")
    def _():
        R = simular(caso_prueba(H=4, M=24, dias_cobro=30))
        assert [p["PERIODO"] for p in R["periodos"]][:3] == ["T0", "M01", "M02"] and R["periodos"][-1]["PERIODO"] == "A04"
        assert _cerca(sum(agregar(R, "fcff_pre")), sum(R["series"]["fcff_pre"]), 1e-12)
        assert agregar(R, "ct")[-1] == R["series"]["ct"][48]

    # ---------------- limitaciones físicas ----------------
    @test("F01", "Ventas ≤ producción disponible (producción + inventario)")
    def _():
        R = simular(caso_prueba(demanda_kg_mes=5.0, inventario_max=2))
        S = R["series"]
        for k in range(1, 61):
            assert S["kg_vendidos"][k] <= S["kg_producidos"][k] + (S["kg_inventario"][k - 1] if k > 1 else 0) + 1e-12

    @test("F02", "Ventas ≤ demanda")
    def _():
        R = simular(caso_prueba(demanda_kg_mes=0.4))
        S = R["series"]
        assert all(S["kg_vendidos"][k] <= 0.4 + 1e-12 for k in range(61))
        assert _cerca(S["u_efectiva"][5], 0.4) and _cerca(S["u_tecnica"][5], 1.0) and _cerca(S["u_comercial"][5], 0.4)

    @test("F03", "El inventario desplaza ventas pero no crea producto (balance de kg en el horizonte)")
    def _():
        P = caso_prueba(demanda_kg_mes=0.5, inventario_max=3)
        P["demanda"][0]["kg_mes"] = [0.0] + [0.2 if k % 2 else 1.4 for k in range(1, 61)]
        P["etapas"][0]["rampup"] = [{"mes": 1, "utilizacion": 0.8, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}]
        S = simular(P)["series"]
        assert _cerca(sum(S["kg_producidos"]), sum(S["kg_vendidos"]) + sum(S["kg_excedente_sin_venta"]) + S["kg_inventario"][60], 1e-9)
        assert all(S["kg_vendidos"][k] <= P["demanda"][0]["kg_mes"][k] + 1e-12 for k in range(61))

    @test("F03b", "Inventario con dos productos (parte limitante): el excedente se guarda y luego se vende sin duplicarse")
    def _():
        P = caso_prueba(inventario_max=3)
        P["productos"]["alas"] = {"kg_ave": 0.5, "categoria_ingreso": "OTROS", "nombre": "prueba"}
        P["demanda"].append({"id": "D2", "producto": "alas", "canal": "supermercados", "mercado": "INTERNO",
                             "categoria": "ESCENARIO", "kg_mes": [0.0] + [0.0 if k % 2 else 1.0 for k in range(1, 61)]})
        P["precios"]["alas|supermercados|INTERNO"] = {"tipo": "CONSTANTE", "usd_kg": 1.0}
        P["inventario_max_meses"]["alas"] = 3
        S = simular(P)["series"]
        assert _cerca(sum(S["kg_producidos"]), sum(S["kg_vendidos"]) + sum(S["kg_excedente_sin_venta"]) + S["kg_inventario"][60], 1e-9)
        ventas_alas = sum(simular(P)["por_linea"]["D2"]["kg"])
        assert ventas_alas <= 0.5 * 60 + 1e-9 and _cerca(ventas_alas, 30.0, 1e-9)

    @test("F04", "Productos vendibles del balance ≤ masa del ave; mix sobre 100 % rechazado")
    def _():
        for cfg in ("A", "B", "C"):
            pr, meta = productos_balance(cfg)
            assert sum(x["kg_ave"] or 0 for x in pr.values()) <= meta["peso_vivo"] + meta["agua_incorporada"] + 1e-9
        P = caso_prueba()
        P["productos"]["pechuga"] = {"kg_ave": 5.0, "categoria_ingreso": "PRODUCTO_PRINCIPAL", "nombre": "x"}
        P["meta_productos"] = {"peso_vivo": 2.9, "agua_incorporada": 0.2}
        assert _lanza(simular, P)

    @test("F05", "Alternativas exclusivas: esqueleto vendido XOR CMS; subproductos crudos XOR rendering")
    def _():
        v, _ = productos_balance("B", {"esqueleto": "venta"})
        c, _ = productos_balance("B", {"esqueleto": "cms"})
        assert v["carcasa_esqueleto"]["kg_ave"] > 0 and v["cms"]["kg_ave"] == 0
        assert c["cms"]["kg_ave"] > 0 and c["carcasa_esqueleto"]["kg_ave"] == 0
        r, _ = productos_balance("B", None, "rendering_propio")
        assert all(r[p]["kg_ave"] == 0 for p in PRODUCTOS_CLASE_C) and r[PRODUCTO_RENDERING]["kg_ave"] is None
        d, _ = productos_balance("B")
        assert d[PRODUCTO_RENDERING]["kg_ave"] == 0 and d["sangre"]["kg_ave"] > 0
        assert "cms_alternativa_no_sumable" not in d

    @test("F06", "Una expansión cambia la capacidad solo desde su entrada en operación (por fecha)")
    def _():
        P = caso_prueba(H=4)
        e2 = etapa_vacia("E2", 2, 12, "FECHA")
        e2.update(capex_usd=50.0, curva_desembolso=[(-6, 0.5), (-1, 0.5)], rampup=P["etapas"][0]["rampup"],
                  opex_rubros=P["etapas"][0]["opex_rubros"], activos=[{"clase": "x", "capex_usd": 50.0, "vida_util_anios": 10,
                                                                       "valor_residual_usd": 0.0, "costo_reemplazo_usd": None}])
        e2["entrada"]["mes"] = 25
        P["etapas"].append(e2)
        S = simular(P)["series"]
        assert all(S["capacidad_aves"][k] == 1.0 for k in range(1, 25)) and all(S["capacidad_aves"][k] == 2.0 for k in range(25, 49))
        assert _cerca(S["capex_expansion"][19], 25.0) and _cerca(S["capex_expansion"][24], 25.0)
        assert _cerca(sum(S["capex_inicial"]), 100.0)

    @test("F07", "Gatillo por condición: entra meses_obra después del gatillo, nunca antes")
    def _():
        P = caso_prueba(H=6, demanda_kg_mes=1.5)
        e2 = etapa_vacia("E2", 2, 12, "CONDICION")
        e2.update(capex_usd=50.0, curva_desembolso=[(-4, 1.0)], rampup=P["etapas"][0]["rampup"],
                  opex_rubros=P["etapas"][0]["opex_rubros"], activos=[{"clase": "x", "capex_usd": 50.0, "vida_util_anios": 20,
                                                                       "valor_residual_usd": 0.0, "costo_reemplazo_usd": None}])
        e2["entrada"].update(condiciones={"utilizacion_min": 0.99, "anio_min": 2}, meses_consecutivos=3, meses_obra=6)
        P["etapas"].append(e2)
        R = simular(P)
        assert R["disparo_etapas"][1] == 12 and R["entrada_etapas"][1] == 19
        S = R["series"]
        assert S["capacidad_aves"][18] == 1.0 and S["capacidad_aves"][19] == 2.0 and _cerca(S["capex_expansion"][15], 50.0)

    @test("F08", "Los fijos no caen con la utilización; los variables sí")
    def _():
        P = caso_prueba(opex_var=24.0, demanda_kg_mes=0.5)
        S = simular(P)["series"]
        assert _cerca(S["opex_fijo"][3], 5.0) and _cerca(S["opex_variable"][3], 1.0)

    @test("F09", "Productos = balance 04 vía ITEMS de 23 (reproduce kg_por_ave; no copia fórmulas)")
    def _():
        for cfg in ("A", "B", "C"):
            k, _ = me.kg_por_ave(cfg)
            pr, _ = productos_balance(cfg)
            for p in pr:
                if p != PRODUCTO_RENDERING:
                    assert _cerca(pr[p]["kg_ave"], k[p], 1e-12)

    @test("F10", "Conversión de demanda kg/día, t/día, t/mes, t/año (día calendario)")
    def _():
        a = convertir_demanda(1000, "kg/dia")
        assert _cerca(convertir_demanda(1, "t/dia"), a) and _cerca(convertir_demanda(365, "t/anio"), a)
        assert _cerca(convertir_demanda(a / 1000, "t/mes"), a) and _cerca(convertir_demanda(1000, "kg/dia_operativo", 365), a)
        assert _lanza(convertir_demanda, 1, "cajas/dia")

    @test("F11", "Utilización efectiva = mín(técnica, comercial) ≤ 1; la comercial puede superar 1")
    def _():
        P = caso_prueba(demanda_kg_mes=1.8)
        P["etapas"][0]["rampup"] = [{"mes": 1, "utilizacion": 0.5, "merma": 0.1, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0},
                                    {"mes": 7, "utilizacion": 1.0, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}]
        S = simular(P)["series"]
        assert _cerca(S["u_efectiva"][3], 0.5) and S["u_comercial"][3] > 1 and _cerca(S["u_efectiva"][10], 1.0)
        assert _cerca(S["kg_merma_rampup"][3], 0.05) and S["fase"][3] == "RAMP_UP" and S["fase"][10] == "OPERACION_MADURA"

    # ---------------- evidencia ----------------
    @test("E01", "Precio faltante ≠ 0: la venta bruta queda NO CALCULABLE y se dice por qué")
    def _():
        P = caso_prueba()
        P["precios"] = {}
        R = simular(P)
        r = resultados(R)
        assert R["series"]["venta_bruta"] is None and r["PUBLICABLE_INGRESOS"] is False and "precio" in r["PUBLICABLE_INGRESOS_MOTIVO"]
        assert r["VAN"] is None

    @test("E02", "E4 no se transforma en validado (modo evidencia y base de precios)")
    def _():
        assert resolver("x", "EVIDENCIA", (10.0, "E4", "FTE"))[1] == "PENDIENTE"
        assert resolver("x", "EVIDENCIA", (10.0, "E2", "COT"))[1] == "EVIDENCIA_REAL"
        ev, refs = leer_precios()
        assert not ev and refs and all(r["NIVEL_EVIDENCIA"] == "E4" for r in refs)

    @test("E03", "El escenario del usuario no sobrescribe la evidencia (y la base queda intacta)")
    def _():
        assert resolver("x", "ESCENARIO", (10.0, "E1", "COT"), 99.0)[0] == 10.0
        assert resolver("x", "ESCENARIO", None, 99.0) == (99.0, "ESCENARIO_USUARIO", "", "escenario del usuario")
        antes = open(ARCHIVO_PRECIOS, encoding="utf-8").read() + open(ARCHIVO_INPUTS, encoding="utf-8").read()
        P, Tz = construir_entrada("t", "C1", (10000,), "ESCENARIO", "PLANTILLA_BASE",
                                  {"precios": {"pollo_entero|supermercados|INTERNO": {"tipo": "CONSTANTE", "usd_kg": 9.0}},
                                   "valores": {"horizonte_anios": 10}})
        assert P["horizonte_anios"] == 10 and P["precios"]["pollo_entero|supermercados|INTERNO"]["usd_kg"] == 9.0
        assert antes == open(ARCHIVO_PRECIOS, encoding="utf-8").read() + open(ARCHIVO_INPUTS, encoding="utf-8").read()

    @test("E04", "Modo evidencia bloquea rentabilidad incompleta (C1-10000: todo NO PUBLICABLE con faltantes)")
    def _():
        P, Tz, R, r = correr_escenario("t", "C1", (10000,), "EVIDENCIA")
        for fl in FLAGS:
            assert r[fl] is False and r[fl + "_MOTIVO"].startswith(NO_PUB)
        assert all(r.get(k) is None for k in ("VAN", "TIR", "EBITDA_ULTIMO_ANIO", "PAYBACK_SIMPLE_ANIOS", "FONDOS_INICIALES"))
        assert R["faltantes"]["DEMANDA"] and R["faltantes"]["PRECIOS"] and R["faltantes"]["OPEX"] and R["faltantes"]["CAPEX"]

    @test("E05", "Modo escenario etiqueta todos los resultados como SIMULACION_HIPOTETICA_NO_VALIDADA")
    def _():
        r = resultados(simular(caso_prueba(tasa_gan=0.3)))
        assert r["ETIQUETA"] == ETIQUETA_SIM and r["PUBLICABLE_VAN"] and r["PUBLICABLE_VAN_MOTIVO"] == ETIQUETA_SIM

    @test("E06", "CAPEX/OPEX parcial E4 no genera total ni VAN")
    def _():
        cc, co = configs("C2-10000")
        cap, niv, mot = capex_desde_modulo(cc)
        rub, niv2, mot2 = opex_desde_modulo(co)
        assert cap is None and "NO usado como total" in mot and rub is None and "NO usado" in mot2
        P = caso_prueba()
        P["etapas"][0]["capex_usd"] = None
        r = resultados(simular(P))
        assert r["VAN"] is None and r["PUBLICABLE_VAN"] is False

    @test("E07", "Inputs de usuario y stress solo en MODO ESCENARIO")
    def _():
        assert _lanza(construir_entrada, "t", "C1", (10000,), "EVIDENCIA", None, {"valores": {"horizonte_anios": 10}})
        P = caso_prueba()
        P["modo"], P["stress"] = "EVIDENCIA", {"precio": 0.9}
        assert _lanza(simular, P)

    @test("E08", "Los ~90 supermercados no son demanda: modo evidencia sin demanda; 02 = SUPUESTO")
    def _():
        P, Tz = construir_entrada("t", "C1", (10000,), "EVIDENCIA")
        assert P["demanda"] is None
        red = [r for r in leer_csv(ARCHIVO_DEMANDA) if r["id"].startswith("RED-")]
        assert red and all(r["clasificacion_dato"] == "SUPUESTO" and r["sumable_a_demanda"] == "no" for r in red)
        P["demanda"] = [{"id": "x", "producto": "pollo_entero", "canal": "supermercados", "mercado": "INTERNO",
                         "categoria": "POTENCIAL", "kg_mes": 1e6}]
        assert _lineas_contables(P) == []

    @test("E09", "Se evalúan exactamente las configuraciones del mapa (24, sin redefinirlas)")
    def _():
        mapa = mapa_arquitecturas()
        assert len(mapa) == 24
        corr = corridas_referencia()
        for r in mapa:
            if r["TIPO"] == "VARIANTE":
                assert any(c["VARIANTE"] == r["ESCENARIO_REFERENCIA"] for c in corr)
                cc, co = configs(r["ESCENARIO_REFERENCIA"])
                assert mcx.etiqueta_arquitectura(cc) == mcx.etiqueta_arquitectura(mo.config_capex(co))
        cc, co = configs("C3-10000")
        assert cc == mcx.preset("C3", aves_dia=10000) and mo.config_capex(co) == cc

    @test("E10", "inputs_financieros.csv y base_precios_venta.csv válidos (PENDIENTE sin valor; precio vacío ≠ 0)")
    def _():
        filas = leer_inputs()
        assert all(f["VALOR"] == "" for f in filas if f["ORIGEN"] == "PENDIENTE")
        assert all(f["ORIGEN"] in ("PENDIENTE", "SUPUESTO_MODELO") for f in filas)
        for r in leer_csv(ARCHIVO_PRECIOS):
            assert r["PRECIO"] == "" if r["ESTADO"] == "PENDIENTE" else _num(r["PRECIO"]) > 0
        met = {f["VARIABLE"] for f in filas if f["ESCENARIO"] == "EVIDENCIA" and f["ORIGEN"] == "SUPUESTO_MODELO"}
        assert met <= SUPUESTOS_METODOLOGICOS

    @test("E11", "Valor en ARS sin tipo de cambio → error (regla 2)")
    def _():
        assert _lanza(a_usd, 1000.0, "ARS") and _cerca(a_usd(1500.0, "ARS", 1500.0, "2026-10-01", "A3500"), 1.0)

    @test("E12", "Montos E4 de CAPEX/OPEX quedan solo en la traza, nunca en el motor")
    def _():
        P, Tz = construir_entrada("t", "C3", (10000,), "EVIDENCIA")
        e = P["etapas"][0]
        assert e["capex_usd"] is None and e["opex_rubros"] is None and "E4" in e["motivo_capex"] + e["motivo_opex"]

    @test("E13", "OPEX incompleto: EBITDA no se calcula ni se publica aunque los ingresos estén completos")
    def _():
        P = caso_prueba()
        P["etapas"][0]["opex_rubros"][0]["costo_pleno_usd_anio"] = None
        R = simular(P)
        r = resultados(R)
        assert R["series"]["ingreso_neto"] is not None and R["series"]["ebitda"] is None
        assert r["PUBLICABLE_INGRESOS"] and not r["PUBLICABLE_EBITDA"] and "OPEX" in r["PUBLICABLE_EBITDA_MOTIVO"]

    # ---------------- finanzas ----------------
    @test("N01", "VAN contra caso manual (−100; 40 × 5; 10 %)")
    def _():
        assert _cerca(van([-100, 40, 40, 40, 40, 40], [0, 1, 2, 3, 4, 5], 0.10), 51.63147, 1e-6)
        r = resultados(simular(caso_prueba(convencion="PERIODO_REPORTE")))
        assert _cerca(r["VAN"], 51.63147, 1e-5) and r["BASE_FLUJO"] == "PRE_TAX"

    @test("N02", "TIR correcta en flujos simples conocidos")
    def _():
        assert _cerca(tir([-100, 110], [0, 1])[0], 0.10, 1e-8)
        x, est = tir([-100, 40, 40, 40, 40, 40], [0, 1, 2, 3, 4, 5])
        assert est == "UNICA" and _cerca(x, 0.286493, 1e-5)

    @test("N03", "TIR ambigua detectada (−100, 230, −132: raíces 10 % y 20 %)")
    def _():
        x, est = tir([-100, 230, -132], [0, 1, 2])
        assert x is None and est.startswith("TIR_AMBIGUA") and "10.0000%" in est and "20.0000%" in est

    @test("N04", "TIR inexistente cuando el flujo no cambia de signo")
    def _():
        assert tir([10, 20], [0, 1]) == (None, "NO_EXISTE (el flujo no cambia de signo)")
        r = resultados(simular(caso_prueba(opex_fijo=120.0)))
        assert r["TIR"] is None and r["PUBLICABLE_TIR"] is False

    @test("N05", "Payback simple y descontado contra cálculo manual")
    def _():
        f, t = [-100, 40, 40, 40, 40, 40], [0, 1, 2, 3, 4, 5]
        assert _cerca(payback(f, t)[0], 2.5)
        d = [x / 1.1 ** tt for x, tt in zip(f, t)]
        acum = -100 + d[1] + d[2] + d[3]          # −0,53: recupera dentro del año 4
        assert acum < 0 and _cerca(payback(f, t, 0.10)[0], 3 + (-acum) / d[4], 1e-9)

    @test("N06", "NO RECUPERADO detectado (sin extrapolación)")
    def _():
        assert payback([-100, 10, 10], [0, 1, 2]) == (None, "NO_RECUPERADO")
        r = resultados(simular(caso_prueba(opex_fijo=95.0)))
        assert r["PAYBACK_SIMPLE_ANIOS"] is None and r["PAYBACK_SIMPLE_ESTADO"] == "NO_RECUPERADO"

    @test("N07", "Break-even correcto (simple y del motor)")
    def _():
        assert break_even_simple(10, 6, 400, 200) == (100.0, 0.5)
        assert break_even_simple(5, 6, 400)[0] is None
        r = resultados(simular(caso_prueba(opex_var=24.0)))
        # MC por ave = 100/12 − 24/12 = 76/12 ; fijos 60 → q* = 60 × 12 / 76 aves/año ; capacidad 12
        assert _cerca(r["BE_UTILIZACION_EBITDA"], 60 / 76, 1e-9)
        assert _cerca(r["BE_PRECIO_MEDIO_USD_KG_EBITDA"], 84 / 12, 1e-9)

    @test("N08", "Real y nominal no se mezclan; con tasas consistentes (Fisher) el VAN coincide")
    def _():
        P = caso_prueba(modelo="REAL")
        P["base_tasa"] = "NOMINAL"
        assert _lanza(simular, P)
        assert _lanza(simular, caso_prueba(modelo="REAL", inflacion=0.05))
        P = caso_prueba()
        P["precios"]["pollo_entero|supermercados|INTERNO"] = {"tipo": "SERIE", "base": "NOMINAL", "por_anio": {1: 1.0}}
        assert _lanza(simular, P)
        rr = resultados(simular(caso_prueba(H=3, M=36, tasa=0.08)))
        rn = resultados(simular(caso_prueba(H=3, M=36, tasa=1.08 * 1.05 - 1, modelo="NOMINAL", inflacion=0.05)))
        assert _cerca(rr["VAN"], rn["VAN"], 1e-9)
        S = simular(caso_prueba())["series"]
        assert len({round(x, 12) for x in S["venta_bruta"][1:]}) == 1       # modelo real: sin crecimiento automático

    @test("N09", "FCFF independiente de la financiación")
    def _():
        d = [{"id": "D", "monto": 70.0, "tasa": 0.15, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 36, "gracia_meses": 12, "metodo": "FRANCES",
              "capitalizacion_meses": 6, "frecuencia_meses": 6, "mes_desembolso": 0, "comision_pct": 0.01}]
        a = simular(caso_prueba(tasa_gan=0.3))["series"]
        b = simular(caso_prueba(tasa_gan=0.3, deudas=d, aportes=[(0, 30.0)]))["series"]
        assert all(_cerca(x, y, 1e-12) for x, y in zip(a["fcff"], b["fcff"]))

    @test("N10", "El flujo del accionista sí responde a la deuda (y al escudo fiscal de intereses)")
    def _():
        d = [{"id": "D", "monto": 70.0, "tasa": 0.15, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 36, "gracia_meses": 12, "metodo": "FRANCES",
              "capitalizacion_meses": 6, "frecuencia_meses": 6, "mes_desembolso": 0}]
        a = simular(caso_prueba(tasa_gan=0.3))["series"]
        b = simular(caso_prueba(tasa_gan=0.3, deudas=d, aportes=[(0, 30.0)]))["series"]
        assert _cerca(b["fcfe"][0] - a["fcfe"][0], 70.0, 1e-9)
        assert sum(b["impuesto_con_deuda"]) < sum(a["impuesto_con_deuda"])

    @test("N11", "Cronograma de deuda: francés cuota constante, alemán amortización constante, bullet")
    def _():
        f = cronograma_deuda({"id": "F", "monto": 100.0, "tasa": 0.12, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 12, "metodo": "FRANCES",
                              "capitalizacion_meses": 1, "frecuencia_meses": 1, "mes_desembolso": 0}, 24)
        cuotas = {round(f["interes"][k] + f["amort"][k], 9) for k in range(1, 13)}
        assert len(cuotas) == 1 and _cerca(list(cuotas)[0], 8.884879, 1e-6)
        a = cronograma_deuda({"id": "A", "monto": 120.0, "tasa": 0.1, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 12, "metodo": "ALEMAN",
                              "capitalizacion_meses": 3, "frecuencia_meses": 3, "mes_desembolso": 0}, 24)
        assert all(_cerca(a["amort"][k], 30.0) for k in (3, 6, 9, 12))
        b = cronograma_deuda({"id": "B", "monto": 100.0, "tasa": 0.10, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 12, "metodo": "BULLET",
                              "capitalizacion_meses": 12, "frecuencia_meses": 12, "mes_desembolso": 0}, 24)
        assert _cerca(b["interes"][12], 10.0) and _cerca(b["amort"][12], 100.0)

    @test("N12", "DSCR = CFADS ÷ servicio de deuda; no publicable sin deuda")
    def _():
        d = [{"id": "D", "monto": 50.0, "tasa": 0.1, "tipo_tasa": "NOMINAL_ANUAL", "base_tasa": "REAL", "plazo_meses": 24, "metodo": "ALEMAN", "capitalizacion_meses": 12, "frecuencia_meses": 12,
              "mes_desembolso": 0}]
        R = simular(caso_prueba(tasa_gan=0.3, deudas=d, aportes=[(0, 50.0)]))
        r = resultados(R)
        cf, sv = agregar(R, "cfads"), agregar(R, "servicio_deuda")
        assert _cerca(r["DSCR_MINIMO"], min(c / s for c, s in zip(cf, sv) if s > 0))
        assert resultados(simular(caso_prueba(tasa_gan=0.3)))["PUBLICABLE_DSCR"] is False

    @test("N13", "MIRR contra cálculo manual")
    def _():
        assert _cerca(mirr([-100, 50, 60], [0, 1, 2], 0.10, 0.12), 1.16 ** 0.5 - 1, 1e-12)

    @test("N14", "Valor terminal: SIN = 0; VALOR_LIBRO = valor libro; PERPETUIDAD = F(1+g)/(r−g)")
    def _():
        S = simular(caso_prueba(vida=10))["series"]
        assert S["valor_terminal"][-1] == 0.0
        P = caso_prueba(vida=10)
        P["valor_terminal"]["metodo"] = "VALOR_LIBRO"
        S = simular(P)["series"]
        assert _cerca(S["valor_terminal"][-1], 50.0, 1e-9)
        P = caso_prueba()
        P["valor_terminal"].update(metodo="PERPETUIDAD", g=0.0)
        S = simular(P)["series"]
        assert _cerca(S["valor_terminal"][-1], 40.0 / 0.10, 1e-9)

    @test("N15", "IVA: el IVA de CAPEX no es costo económico; arrastre del saldo a favor")
    def _():
        iva = {"modo": "SIMPLIFICADO", "alicuota_ventas": 0.105, "alicuota_compras": 0.21, "alicuota_capex": 0.21}
        a = simular(caso_prueba())["series"]
        Pb = caso_prueba(iva=iva)
        Pb["etapas"][0]["iva_capex"] = {"base": "NETA", "iva_estado": "DECLARADO", "tasa": 0.21,
                                        "condicion_fiscal": "TEST", "elegible_credito": True, "criterio": "caso de prueba"}
        b = simular(Pb)["series"]
        assert all(_cerca(x, y, 1e-12) for x, y in zip(a["ebitda"], b["ebitda"]))
        assert _cerca(b["iva_saldo_favor"][0], 21.0) and b["flujo_iva"][0] < 0
        assert _cerca(sum(b["flujo_iva"]), -b["iva_saldo_favor"][-1], 1e-9)
        # sin declaración (TF-076): CREDITO_FISCAL_IVA_CAPEX = PENDIENTE; ni crédito en caja ni costo
        Rc = simular(caso_prueba(iva=iva))
        assert any(CREDITO_IVA_CAPEX_PEND in x for x in Rc["faltantes"]["IVA"])
        assert Rc["series"]["flujo_iva"] is None and Rc["series"]["fcff_pre"] is None
        assert all(_cerca(x, y, 1e-12) for x, y in zip(a["ebitda"], Rc["series"]["ebitda"]))

    @test("N16", "Impuesto a las ganancias anual con quebrantos")
    def _():
        P = caso_prueba(H=3, tasa_gan=0.3, vida=50, opex_fijo=60.0)
        P["etapas"][0]["rampup"] = [{"mes": 1, "utilizacion": 0.4, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0},
                                    {"mes": 13, "utilizacion": 1.0, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}]
        S = simular(P)["series"]
        y1, y2 = sum(S["ebit"][1:13]), sum(S["ebit"][13:25])
        assert y1 < 0 and S["impuesto_operativo"][12] == 0.0
        assert _cerca(S["impuesto_operativo"][24], 0.3 * (y2 + y1), 1e-9)

    @test("N17", "CAPEX inicial, de expansión y de reposición separados; reposición al fin de la vida útil")
    def _():
        S = simular(caso_prueba(H=6, vida=3))["series"]
        assert _cerca(S["capex_reposicion"][37], 100.0) and _cerca(sum(S["capex_inicial"]), 100.0)
        assert _cerca(sum(S["depreciacion"]), 100.0 + 100.0, 1e-9)

    @test("N18", "Curva de desembolso: el CAPEX no ocurre todo en T0")
    def _():
        P = caso_prueba(pre=3, con=6, com=2, curva_desembolso=[(-12, 0.1), (-8, 0.5), (-3, 0.4)])
        R = simular(P)
        S = R["series"]
        assert R["inicio_op"] == 12 and _cerca(S["capex_inicial"][0], 10.0) and _cerca(S["capex_inicial"][4], 50.0)
        assert S["fase"][2] == "PREOPERACION" and S["fase"][5] == "CONSTRUCCION" and S["fase"][10] == "COMMISSIONING"
        assert S["venta_bruta"][11] == 0.0 and S["venta_bruta"][12] > 0 and S["opex_total"][11] == 0.0

    @test("N19", "Stress (solo escenario): precio −10 %, ramp-up lento y corte de exportación")
    def _():
        base = resultados(simular(caso_prueba()))
        P = caso_prueba()
        P["stress"] = {"precio": 0.9}
        assert _cerca(resultados(simular(P))["EBITDA_ULTIMO_ANIO"], 30.0, 1e-9) and base["EBITDA_ULTIMO_ANIO"] > 30
        P = caso_prueba()
        P["etapas"][0]["rampup"] = [{"mes": 1, "utilizacion": 0.5, "merma": 0, "eficiencia": 1, "costos_extra_usd_mes": 0},
                                    {"mes": 4, "utilizacion": 1.0, "merma": 0, "eficiencia": 1, "costos_extra_usd_mes": 0}]
        P["stress"] = {"rampup_lento_factor": 2.0}
        S = simular(P)["series"]
        assert S["u_tecnica"][6] == 0.5 and S["u_tecnica"][7] == 1.0

    @test("N21", "Precio constante real vs serie por año (sin crecimiento automático; serie incompleta = faltante)")
    def _():
        P = caso_prueba(H=2)
        P["precios"]["pollo_entero|supermercados|INTERNO"] = {"tipo": "SERIE", "base": "REAL", "por_anio": {1: 100 / 12, 2: 120 / 12}}
        S = simular(P)["series"]
        assert _cerca(sum(S["venta_bruta"][1:13]), 100.0) and _cerca(sum(S["venta_bruta"][13:25]), 120.0)
        P["precios"]["pollo_entero|supermercados|INTERNO"]["por_anio"] = {1: 100 / 12}
        R = simular(P)
        assert R["series"]["venta_bruta"] is None and any("serie incompleta" in x for x in R["faltantes"]["PRECIOS"])

    @test("N22", "Devaluación con traslado explícito y reporte en ARS solo con TC declarado")
    def _():
        P = caso_prueba()
        P["etapas"][0]["opex_rubros"][0]["moneda_original"] = "ARS"
        P["stress"] = {"devaluacion": {"pct": 0.5}}
        assert _lanza(simular, P)
        P["stress"] = {"devaluacion": {"pct": 0.5, "traslado_precios_ars": 0.0}}
        S = simular(P)["series"]
        assert _cerca(S["opex_fijo"][3], 5.0 / 1.5)
        assert _lanza(a_moneda_reporte, [1.0, 2.0], "ARS", [1500.0, None], "A3500")
        assert a_moneda_reporte([1.0, None], "ARS", [1500.0, 1600.0], "A3500") == [1500.0, None]

    @test("N20", "Trayectorias de expansión consumen la lógica de CAPEX y restauran el módulo")
    def _():
        orig = mcx.TRAYECTORIAS
        r = capex_trayectoria("C1", (2500, 5000, 10000, 20000))
        assert mcx.TRAYECTORIAS is orig and [x["ESCALA"] for x in r] == [2500, 5000, 10000, 20000]
        assert [x["TIPO"] for x in r] == ["INICIAL", "EXPANSION", "EXPANSION", "EXPANSION"]
        P, Tz = construir_entrada("t", "C1", (5000, 10000, 20000), "EVIDENCIA")
        assert [e["entrada"]["tipo"] for e in P["etapas"]] == ["INICIAL", "FECHA", "FECHA"] and \
            all(e["capex_usd"] is None for e in P["etapas"])

    # ---------------- auditoría final: casos explícitos, tasas, IDs, exportación, umbral, overrides ----------------
    @test("C01", "CP-PRETAX-ANUAL: FCFF 40/año, VAN 51,63, TIR 28,65 %, payback 2,5 años = 30 meses")
    def _():
        R = simular(caso_prueba(convencion="PERIODO_REPORTE"))
        r = resultados(R)
        assert r["BASE_FLUJO"] == "PRE_TAX" and r["CONVENCION_DESCUENTO"] == "PERIODO_REPORTE"
        assert R["series"]["impuesto_operativo"] is None              # sin tasa fiscal: no hay after-tax
        assert all(_cerca(x, 40.0, 1e-9) for x in agregar(R, "fcff_pre")[1:])
        assert _cerca(r["VAN"], 51.631470, 1e-6) and _cerca(r["TIR"], 0.2864929, 1e-5)
        assert _cerca(r["PAYBACK_SIMPLE_ANIOS"], 2.5) and _cerca(r["PAYBACK_SIMPLE_MESES"], 30.0)

    @test("C02", "CP-AFTERTAX-ANUAL: tasa test 30 %, depreciación 20, base 20, impuesto 6, FCFF 34; VAN 28,89, TIR 20,76 %")
    def _():
        R = simular(caso_prueba(convencion="PERIODO_REPORTE", tasa_gan=0.30))
        r = resultados(R)
        assert r["BASE_FLUJO"] == "AFTER_TAX"
        assert all(_cerca(x, 20.0, 1e-9) for x in agregar(R, "depreciacion")[1:])
        assert all(_cerca(x, 20.0, 1e-9) for x in agregar(R, "ebit")[1:])
        assert all(_cerca(x, 6.0, 1e-9) for x in agregar(R, "impuesto_operativo")[1:])
        assert all(_cerca(x, 34.0, 1e-9) for x in agregar(R, "fcff")[1:])
        assert _cerca(r["VAN"], -100 + 34 * sum(1.1 ** -y for y in range(1, 6)), 1e-9) and _cerca(r["VAN"], 28.8868, 1e-4)
        assert _cerca(r["TIR"], 0.207616, 1e-5) and _cerca(r["PAYBACK_SIMPLE_ANIOS"], 100 / 34, 1e-9)
        assert all(f["VALOR"] == "" for f in leer_inputs() if f["VARIABLE"] == "impuestos.tasa_ganancias")

    @test("C03", "CP-PRETAX-MENSUAL: misma economía, convención mensual; VAN contra fórmula independiente")
    def _():
        r = resultados(simular(caso_prueba()))
        esperado = -100 + sum((40 / 12) / 1.1 ** (k / 12) for k in range(1, 61))
        assert r["CONVENCION_DESCUENTO"] == "MENSUAL" and _cerca(r["VAN"], esperado, 1e-9) and abs(r["VAN"] - 51.63) > 1
        assert _cerca(r["PAYBACK_SIMPLE_MESES"], 30.0) and _cerca(r["PAYBACK_SIMPLE_ANIOS"], 2.5)
        ids = [c[0] for c in CASOS_PRUEBA]
        assert len(ids) == len(set(ids)) and all(c[0].startswith("CP-") and ("TAX" in c[0] or "-" in c[0][3:]) for c in CASOS_PRUEBA)

    @test("R01", "Tasa anual efectiva → mensual = (1 + r)^(1/12) − 1 (nunca r/12 salvo nominal declarada)")
    def _():
        assert _cerca(tasa_periodica(0.10, 1), 1.1 ** (1 / 12) - 1, 1e-15) and abs(tasa_periodica(0.10, 1) - 0.10 / 12) > 3e-4
        assert _cerca(tasa_periodica(0.126825030131969, 1), 0.01, 1e-12)
        assert _cerca(tasa_anual_efectiva(0.12, "NOMINAL_ANUAL_CAP_MENSUAL"), 1.01 ** 12 - 1, 1e-15)
        assert _lanza(tasa_anual_efectiva, 0.1, "ANUAL")
        P = caso_prueba(tasa=0.12)
        P["tipo_tasa_descuento"] = "NOMINAL_ANUAL_CAP_MENSUAL"
        r = resultados(simular(P))
        assert _cerca(r["TASA_DESCUENTO_MENSUAL_EQUIVALENTE"], 0.01, 1e-12)

    @test("R02", "VAN mensual: T0 sin descontar; cada mes k descontado k períodos con la tasa mensual equivalente")
    def _():
        f = [-100.0] + [10.0] * 12
        assert _cerca(van_periodico(f, 0.01), -100 + 10 * (1 - 1.01 ** -12) / 0.01, 1e-12)
        assert van_periodico([5.0], 0.5) == 5.0
        assert _cerca(van_periodico(f, tasa_periodica(0.10, 1)), van(f, [k / 12 for k in range(13)], 0.10), 1e-12)
        R = simular(caso_prueba(tasa=0.10))
        assert _cerca(resultados(R)["VAN"], van_periodico(R["series"]["fcff_pre"], tasa_periodica(0.10, 1)), 1e-12)

    @test("R03", "TIR: periódica mensual primero; anual efectiva = (1 + i)^12 − 1 (no × 12); ambigüedad detectada")
    def _():
        cuota = 100 * 0.01 / (1 - 1.01 ** -12)
        o = indicadores([-100.0] + [cuota] * 12, "MENSUAL", 0.10)
        assert _cerca(o["TIR_MENSUAL"], 0.01, 1e-8) and _cerca(o["TIR"], 1.01 ** 12 - 1, 1e-7) and abs(o["TIR"] - 0.12) > 6e-3
        o = indicadores([-100.0, 230.0, -132.0], "MENSUAL", 0.10)
        assert o["TIR"] is None and o["TIR_ESTADO"].startswith("TIR_AMBIGUA")
        assert indicadores([10.0, 20.0], "MENSUAL", 0.1)["TIR_ESTADO"].startswith("NO_EXISTE")

    @test("R04", "Payback en meses y años = meses ÷ 12 (sin confundir índice de período con meses)")
    def _():
        o = indicadores([-100.0] + [10.0] * 24, "MENSUAL", 0.10)
        assert _cerca(o["PAYBACK_SIMPLE_MESES"], 10.0) and _cerca(o["PAYBACK_SIMPLE_ANIOS"], 10 / 12)
        R = simular(caso_prueba(H=4, M=24, convencion="PERIODO_REPORTE"))
        r = resultados(R)                          # períodos: T0, M01…M24, A03, A04 → el índice NO es el mes
        assert _cerca(r["PAYBACK_SIMPLE_MESES"], 30.0) and _cerca(r["PAYBACK_SIMPLE_ANIOS"], 2.5)

    @test("R05", "Deuda: tasa EFECTIVA_ANUAL / NOMINAL_ANUAL / PERIODICA coherente con la frecuencia; ambiguas bloqueadas")
    def _():
        base = {"id": "D", "monto": 100.0, "plazo_meses": 12, "metodo": "FRANCES", "frecuencia_meses": 1, "mes_desembolso": 0}
        for extra in ({"tasa": 1.01 ** 12 - 1, "tipo_tasa": "EFECTIVA_ANUAL"},
                      {"tasa": 0.12, "tipo_tasa": "NOMINAL_ANUAL", "capitalizacion_meses": 1},
                      {"tasa": 0.01, "tipo_tasa": "PERIODICA", "periodo_tasa_meses": 1}):
            d = cronograma_deuda(dict(base, **extra), 12)
            assert _cerca(d["interes"][1], 1.0, 1e-9) and _cerca(d["interes"][1] + d["amort"][1], 8.884879, 1e-6)
        b = cronograma_deuda(dict(base, metodo="BULLET", frecuencia_meses=12, tasa=0.10, tipo_tasa="EFECTIVA_ANUAL"), 12)
        assert _cerca(b["interes"][12], 10.0)
        q = cronograma_deuda(dict(base, metodo="ALEMAN", frecuencia_meses=3, tasa=0.10, tipo_tasa="EFECTIVA_ANUAL"), 12)
        assert _cerca(q["interes"][3], 100 * (1.1 ** 0.25 - 1), 1e-12)
        assert _lanza(cronograma_deuda, dict(base, tasa=0.12), 12)
        assert _lanza(cronograma_deuda, dict(base, tasa=0.12, tipo_tasa="NOMINAL_ANUAL", capitalizacion_meses=12), 12)
        assert _lanza(cronograma_deuda, dict(base, tasa=0.03, tipo_tasa="PERIODICA", periodo_tasa_meses=3), 12)

    @test("R06", "Real ↔ real y nominal ↔ nominal: incompatibilidades de tasa o de deuda dan error explícito")
    def _():
        d = [{"id": "D", "monto": 50.0, "tasa": 0.1, "tipo_tasa": "EFECTIVA_ANUAL", "base_tasa": "NOMINAL",
              "plazo_meses": 12, "metodo": "ALEMAN", "frecuencia_meses": 12, "mes_desembolso": 0}]
        assert _lanza(simular, caso_prueba(deudas=d))
        d[0]["base_tasa"] = "REAL"
        assert not _lanza(simular, caso_prueba(deudas=d))
        assert _lanza(simular, caso_prueba(modelo="NOMINAL", inflacion=0.03, deudas=d))
        P = caso_prueba(modelo="NOMINAL", inflacion=0.03)
        P["base_tasa"] = "REAL"
        assert _lanza(simular, P)

    @test("U01", "UMBRAL_EVIDENCIA_PUBLICACION configurable sin tocar código; default E1–E3; E4 no pasa el default")
    def _():
        filas = leer_inputs()
        assert umbral_evidencia(filas) == ("E1", "E2", "E3")
        mod = [dict(f, VALOR="E1|E2|E3|E4") if f["VARIABLE"] == "umbral_evidencia_publicacion" else f for f in filas]
        u = umbral_evidencia(mod)
        assert "E4" in u and resolver("x", "EVIDENCIA", (10.0, "E4", "F"), umbral=u)[1] == "EVIDENCIA_REAL"
        assert resolver("x", "EVIDENCIA", (10.0, "E4", "F"))[1] == "PENDIENTE"
        assert _lanza(umbral_evidencia, [dict(f, VALOR="E9") if f["VARIABLE"] == "umbral_evidencia_publicacion" else f
                                         for f in filas])
        P, Tz, R, r = correr_escenario("t", "C1", (10000,), "EVIDENCIA")
        assert r["UMBRAL_EVIDENCIA"] == "E1|E2|E3"

    @test("O01", "OVERRIDE_SIMULACION: evalúa otro valor sobre una evidencia sin sobrescribir el dato observado")
    def _():
        global ARCHIVO_PRECIOS
        import tempfile
        orig = ARCHIVO_PRECIOS
        filas = leer_csv(orig)
        cab = list(filas[0].keys())
        nueva = dict(filas[0], PRECIO="2.0", MONEDA="USD", NIVEL_EVIDENCIA="E2", ESTADO="CON_PRECIO", FUENTE="TEST")
        k = f"{nueva['PRODUCTO']}|{nueva['CANAL']}|{nueva['MERCADO']}"
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cab)
            w.writeheader()
            w.writerows([nueva] + filas[1:])
            tmp = fh.name
        try:
            ARCHIVO_PRECIOS = tmp
            antes = open(tmp, encoding="utf-8").read()
            P, Tz = construir_entrada("t", "C1", (10000,), "ESCENARIO", None,
                                      {"precios": {k: {"tipo": "CONSTANTE", "usd_kg": 9.0}}})
            assert P["precios"][k]["usd_kg"] == 2.0                     # el escenario no pisa la evidencia
            P, Tz = construir_entrada("t", "C1", (10000,), "ESCENARIO", None,
                                      {"override_precios": {k: {"tipo": "CONSTANTE", "usd_kg": 3.0}},
                                       "valores": {"horizonte_anios": 10}, "override_simulacion": {"horizonte_anios": 15}})
            assert P["precios"][k]["usd_kg"] == 3.0 and P["precios"][k]["observado"]["usd_kg"] == 2.0
            assert P["horizonte_anios"] == 15 and resultados(simular(P))["ETIQUETA"] == ETIQUETA_SIM
            txt = json.dumps(Tz.filas, ensure_ascii=False)
            assert "PRECIO_OBSERVADO=2.0" in txt and "VALOR_OBSERVADO=10" in txt
            assert open(tmp, encoding="utf-8").read() == antes and leer_precios()[0][k]["usd_kg"] == 2.0
            assert _lanza(construir_entrada, "t", "C1", (10000,), "EVIDENCIA", None, {"override_precios": {k: {}}})
        finally:
            ARCHIVO_PRECIOS = orig
            os.unlink(tmp)

    @test("X01", "Derechos de exportación: una sola ubicación (deducción de la venta), nunca dos veces")
    def _():
        P = caso_prueba()
        P["impuestos"]["pct_derechos_exportacion"] = 0.1
        assert _lanza(simular, P)
        P = caso_prueba()
        P["canales"]["supermercados"]["pct_derechos_exportacion"] = 0.1
        assert _lanza(simular, P)
        P = caso_prueba()
        P["demanda"][0].update(canal="exportacion", mercado="EXPORTACION")
        P["precios"] = {"pollo_entero|exportacion|EXPORTACION": {"tipo": "CONSTANTE", "usd_kg": 100 / 12}}
        P["canales"] = {"exportacion": dict(P["canales"]["supermercados"], pct_derechos_exportacion=0.10,
                                            costo_exportacion_usd_kg=0.0)}
        S = simular(P)["series"]
        assert _cerca(sum(S["derechos_exportacion"]), 0.10 * sum(S["venta_bruta"]), 1e-12)
        assert _cerca(sum(S["ingreso_neto"]), 0.90 * sum(S["venta_bruta"]), 1e-12)
        assert _cerca(sum(S["ebitda"]), sum(S["ingreso_neto"]) - sum(S["opex_total"]), 1e-12)

    @test("ID01", "61 corridas con ID_CORRIDA único, reconstruible y sin duplicados de contenido")
    def _():
        corr = corridas_referencia()
        assert len(corr) == 61 and sum(c["MODO"] == "EVIDENCIA" for c in corr) == 42
        ids = [c["ID_CORRIDA"] for c in corr]
        assert len(set(ids)) == 61 and len({c["NOMBRE"] for c in corr}) == 61
        for c in corr:
            modo, cfg, var, esc, tray, pl = c["ID_CORRIDA"].split("|")
            assert (modo, cfg) == (c["MODO"], c["CONFIGURACION"]) and esc == "-".join(map(str, c["ESCALAS"]))
            assert var == (c["VARIANTE"] or "BASE") and pl == (c["PLANTILLA"] or "EVIDENCIA")
        assert len({firma_corrida(c) for c in corr}) == 61

    @test("EX01", "Expansión: misma configuración por escala (cualquier base); transición de arquitectura bloqueada")
    def _():
        assert _lanza(construir_entrada, "t", "C1", (5000, 10000), "EVIDENCIA", None, None, None, ["C1", "C2"])
        r = capex_trayectoria("C3", (5000, 10000))
        assert [x["TIPO"] for x in r] == ["INICIAL", "EXPANSION"]
        assert {c["CONFIGURACION"] for c in corridas_referencia() if len(c["ESCALAS"]) > 1} == {"C1"}
        P, Tz = construir_entrada("t", "C1", (5000, 10000), "EVIDENCIA")
        assert [e["configuracion"] for e in P["etapas"]] == ["C1", "C1"]

    fallas = []
    for tid, desc, fn in T:
        try:
            fn()
            ok = True
        except Exception as ex:                    # noqa: BLE001
            ok = False
            fallas.append((tid, desc, f"{type(ex).__name__}: {ex}"))
        if verbose:
            print(f"  [{'OK' if ok else 'FALLA'}] {tid} {desc}")
    if verbose:
        print(f"Tests: {len(T) - len(fallas)}/{len(T)} OK")
    return fallas, len(T)


MUTACIONES = {
    "M01": "un precio faltante se trata como 0", "M02": "ventas no limitadas por la demanda",
    "M03": "ventas no limitadas por la producción", "M04": "el flujo usa el stock de CT en lugar de ΔCT",
    "M05": "el FCFF parte del EBIT (no suma la depreciación)", "M06": "la deuda entra al FCFF",
    "M07": "los costos fijos caen con la utilización", "M08": "el VAN descuenta un mes de menos",
    "M09": "el modo evidencia acepta E4", "M10": "el escenario sobrescribe la evidencia",
    "M11": "esqueleto vendido y CMS monetizados a la vez", "M12": "se fuerza una TIR con raíces múltiples",
    "M13": "payback extrapolado más allá del horizonte", "M14": "inflación aplicada en el modelo real",
    "M15": "la expansión suma capacidad desde el gatillo (sin obra)", "M16": "el inventario crea producto",
    "M17": "el IVA del CAPEX se trata como costo", "M18": "la amortización de deuda no se registra",
    "M19": "los dividendos no salen de la caja", "M20": "se publica EBITDA con OPEX incompleto",
    "M21": "los derechos de exportación se restan dos veces", "M22": "tasa mensual = anual ÷ 12",
    "M23": "TIR anual = TIR mensual × 12", "M24": "la deuda ignora el tipo de tasa (siempre TNA × f ÷ 12)",
    "M25": "payback en años = meses (sin ÷ 12)",
}


def prueba_mutaciones():
    global _MUT
    detectadas = 0
    for m, desc in MUTACIONES.items():
        _MUT = {m}
        _CACHE.clear()
        try:
            with redirect_stdout(io.StringIO()):
                fallas, _ = ejecutar_tests(verbose=False)
        finally:
            _MUT = set()
            _CACHE.clear()
        ok = bool(fallas)
        detectadas += ok
        print(f"  [{'DETECTADA' if ok else 'NO DETECTADA'}] {m} {desc}" + (f" → {fallas[0][0]}" if ok else ""))
    print(f"Mutaciones detectadas: {detectadas}/{len(MUTACIONES)}")
    return detectadas == len(MUTACIONES)


# ---------------------------------------------------------------------------------------------
# 12. CLI
# ---------------------------------------------------------------------------------------------
def correr_json(ruta, salida=None):
    with open(ruta, encoding="utf-8") as fh:
        spec = json.load(fh)
    spec = {k: v for k, v in spec.items() if not k.startswith("_")}
    P, T, R, res = correr_escenario(spec.get("nombre", "USUARIO"), spec["configuracion"], tuple(spec["escalas"]), "ESCENARIO",
                                    spec.get("plantilla"), spec, spec.get("escenario_capex"))
    print(f"ESCENARIO {P['nombre']} — {ETIQUETA_SIM}")
    for k in CAMPOS_ESC:
        if res.get(k) not in (None, ""):
            print(f"  {k}: {_fmt(res[k])}")
    if salida:
        os.makedirs(salida, exist_ok=True)
        escribir(os.path.join(salida, "escenario.csv"), [res], CAMPOS_ESC)
        for tabla, series in (("estado_resultados", SERIES_ER), ("flujo_caja_proyecto", SERIES_FCFF),
                              ("flujo_accionista", SERIES_ACC), ("capital_trabajo_financiero", SERIES_CT), ("deuda", SERIES_DEUDA)):
            escribir(os.path.join(salida, f"{tabla}.csv"), filas_periodicas(R, res, series, tabla),
                     CAMPOS_PER + [s.upper() for s in series] + ["ESTADO_PUBLICACION"])
        escribir(os.path.join(salida, "mapa_drivers.csv"), T.filas, Traza.CAMPOS)
        escribir(os.path.join(salida, "completitud.csv"), completitud(P, R, T),
                 ["ESCENARIO", "MODO", "CONFIGURACION", "ESCALAS", "BLOQUE", "ESTADO", "QUE_FALTA", "REGISTROS", "BLOQUEA_RENTABILIDAD"])
    return res


def main():
    ap = argparse.ArgumentParser(description="Modelo financiero integral (sesión 19)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--escenario", help="archivo JSON de MODO ESCENARIO (ver plantilla_escenario_usuario.json)")
    ap.add_argument("--salida", help="carpeta de salida del escenario del usuario")
    a = ap.parse_args()
    print(f"MODELO FINANCIERO INTEGRAL v{VERSION} ({FECHA})")
    fallas, n = ejecutar_tests(verbose=True)
    if fallas:
        for f in fallas:
            print("FALLA", *f)
        sys.exit(1)
    if a.mutaciones:
        sys.exit(0 if prueba_mutaciones() else 1)
    if a.solo_tests:
        return
    if a.escenario:
        correr_json(a.escenario, a.salida)
        return
    construir_salidas()


if __name__ == "__main__":
    main()
