"""Escenario DEMO_ARTIFICIAL — SOLO_DEMOSTRACION.

TODOS LOS NÚMEROS DE ESTE ARCHIVO SON FICTICIOS. No son datos, estimaciones ni supuestos del proyecto: existen para que
la app muestre todas sus funciones (simular, comparar, optimizar, sensibilidad, stress, Monte Carlo, Pareto) aunque la
evidencia real esté incompleta. El escenario se corre en el universo ARTIFICIAL_TEST del motor (etiqueta
CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO) y sus alternativas llevan el prefijo DEMO-.

Construcción: se completa `experto` con la misma estructura del motor (comun + por_alternativa) para C0–CF ×
2.500 / 5.000 / 10.000 / 20.000 aves/día. Los CAPEX y OPEX ficticios se generan con reglas simples por escala
(declaradas abajo) y llevan los metadatos de arquitectura exigidos por el motor (TF-004), de modo que pasan las mismas
defensas que un escenario real.
"""
from . import escenario as ES
from . import motor as M

NOTA = "FICTICIO — SOLO_DEMOSTRACION (no es dato del proyecto)"
ESCALAS = (2500, 5000, 10000, 20000)
DIAS = 250                                   # calendario base del motor (días operativos/año)

# Reglas ficticias por configuración: CAPEX = fijo + por_ave_dia × escala (USD); OPEX por módulo en USD/ave faenada
# (variable) o USD/año (fijo). Valores inventados, redondos a propósito.
CAPEX_DEMO = {"C0": (150_000, 20), "C1": (2_500_000, 650), "C2": (3_000_000, 850),
              "C3": (4_000_000, 1_300), "CF": (5_000_000, 1_600)}
OPEX_DEMO = {   # módulo → (naturaleza, USD/ave si variable | USD/año si fijo, grupo proveedor, driver de riesgo)
    "C0": {"FAENA_FACON": ("variable", 0.85, "servicios", "facon"), "ALIMENTO_FACON": ("variable", 1.60, "alimento", "alimento"),
           "POLLITO_COMPRADO": ("variable", 0.45, "pollitos", "pollito"),
           "GRANJAS_INTEGRADAS": ("variable", 0.40, "servicios", ""), "ESTRUCTURA": ("fijo", 300_000, "servicios", "salarios")},
    "C1": {"FAENA_PROPIA": ("variable", 0.22, "servicios", "salarios"), "ALIMENTO_COMPRADO": ("variable", 1.55, "alimento", "alimento"),
           "POLLITO_COMPRADO": ("variable", 0.45, "pollitos", "pollito"),
           "GRANJAS_INTEGRADAS": ("variable", 0.40, "servicios", ""), "ESTRUCTURA": ("fijo", 700_000, "servicios", "salarios")},
    "C2": {"FAENA_PROPIA": ("variable", 0.22, "servicios", "salarios"), "ALIMENTO_FACON": ("variable", 1.50, "alimento", "alimento"),
           "POLLITO_COMPRADO": ("variable", 0.45, "pollitos", "pollito"),
           "GRANJAS_INTEGRADAS": ("variable", 0.30, "servicios", ""), "GRANJAS_PROPIAS": ("variable", 0.12, "servicios", "electricidad"),
           "ESTRUCTURA": ("fijo", 850_000, "servicios", "salarios")},
    "C3": {"FAENA_PROPIA": ("variable", 0.22, "servicios", "salarios"), "PLANTA_ALIMENTO_PROPIA": ("variable", 1.35, "granos", "alimento"),
           "INCUBACION_PROPIA": ("variable", 0.36, "servicios", "pollito"), "GRANJAS_PROPIAS": ("variable", 0.42, "servicios", "electricidad"),
           "TRATAMIENTO_SUBPRODUCTOS_PROPIO": ("variable", 0.05, "servicios", ""), "ESTRUCTURA": ("fijo", 1_200_000, "servicios", "salarios")},
    "CF": {"FAENA_PROPIA": ("variable", 0.22, "servicios", "salarios"), "PLANTA_ALIMENTO_PROPIA": ("variable", 1.33, "granos", "alimento"),
           "INCUBACION_PROPIA": ("variable", 0.30, "servicios", "pollito"), "GRANJAS_PROPIAS": ("variable", 0.42, "servicios", "electricidad"),
           "TRATAMIENTO_SUBPRODUCTOS_PROPIO": ("variable", 0.03, "servicios", ""), "ESTRUCTURA": ("fijo", 1_500_000, "servicios", "salarios")},
}
# Activos ficticios: (clase "MODULO:nombre", fracción del CAPEX, vida útil años, depreciable)
ACTIVOS_DEMO = {
    "C0": (("IT_TRAZABILIDAD:sistemas", 0.5, 5, True), ("OBRA_CIVIL:oficina", 0.5, 30, True)),
    "C1": (("TERRENO:lote", 0.05, 0, False), ("OBRA_CIVIL:nave", 0.40, 30, True), ("PROCESO:linea", 0.40, 15, True),
           ("FRIO:camaras", 0.15, 15, True)),
    "C2": (("TERRENO:lote", 0.05, 0, False), ("OBRA_CIVIL:nave", 0.35, 30, True), ("PROCESO:linea", 0.30, 15, True),
           ("FRIO:camaras", 0.15, 15, True), ("GRANJAS:galpones", 0.15, 20, True)),
    "C3": (("TERRENO:lote", 0.04, 0, False), ("OBRA_CIVIL:nave", 0.26, 30, True), ("PROCESO:linea", 0.22, 15, True),
           ("FRIO:camaras", 0.10, 15, True), ("GRANJAS:galpones", 0.20, 20, True), ("ALIMENTO:planta", 0.10, 20, True),
           ("INCUBACION:planta", 0.08, 15, True)),
    "CF": (("TERRENO:lote", 0.04, 0, False), ("OBRA_CIVIL:nave", 0.22, 30, True), ("PROCESO:linea", 0.20, 15, True),
           ("FRIO:camaras", 0.09, 15, True), ("GRANJAS:galpones", 0.18, 20, True), ("ALIMENTO:planta", 0.09, 20, True),
           ("INCUBACION:planta", 0.08, 15, True), ("REPRODUCTORAS:nucleo", 0.10, 15, True)),
}
UNIVERSO_CAPEX = {"C0": "ESTRUCTURA", "C1": "FAENA_PROPIA", "C2": "FAENA_PROPIA", "C3": "FAENA_PROPIA", "CF": "FAENA_PROPIA"}


def _meta(cfg, escala, modulo, universo):
    return {"CONFIGURACION": cfg, "ESCALA": escala, "VARIANTE": "BASE", "MODULO": modulo, "UNIVERSO": universo,
            "ORIGEN": "ESCENARIO_USUARIO"}


def por_alternativa():
    out = {}
    for cfg in M.CONFIGURACIONES:
        fijo, por_ave = CAPEX_DEMO[cfg]
        for E in ESCALAS:
            capex = float(fijo + por_ave * E)
            aves = E * DIAS
            rubros = []
            for mod, (nat, x, grupo, drv) in OPEX_DEMO[cfg].items():
                costo = x * aves if nat == "variable" else x * (E / 10000) ** 0.6
                r = {"rubro": f"DEMO-{mod}", "grupo_proveedor": grupo, "naturaleza": nat, "costo_pleno_usd_anio": round(costo, 2),
                     "es_compra": True, "dias_pago": 30.0, "iva_credito": False, "meta": _meta(cfg, E, mod, mod)}
                if drv:
                    r["driver_riesgo"] = drv
                rubros.append(r)
            activos = [{"clase": cl, "capex_usd": round(capex * fr, 2), "vida_util_anios": vida, "valor_residual_usd": 0.0,
                        "costo_reemplazo_usd": round(capex * fr, 2), "depreciable": dep}
                       for cl, fr, vida, dep in ACTIVOS_DEMO[cfg]]
            dif = capex - sum(a["capex_usd"] for a in activos)
            activos[-1]["capex_usd"] = round(activos[-1]["capex_usd"] + dif, 2)
            deuda = round(capex * 0.4, 2)
            out[f"{ES.PREFIJO_DEMO}{cfg}|BASE|{E}|ESCALA_UNICA"] = {
                "etapas": [{"capex_usd": capex, "capex_meta": _meta(cfg, E, "TOTAL_ETAPA", UNIVERSO_CAPEX[cfg]),
                            "curva_desembolso": [[-12, 0.3], [-6, 0.4], [-1, 0.3]] if cfg != "C0" else [[-1, 1.0]],
                            "opex_rubros": rubros, "activos": activos,
                            "rampup": [{"mes": 1, "utilizacion": 0.5, "merma": 0.03, "eficiencia": 0.90, "costos_extra_usd_mes": 0.0},
                                       {"mes": 4, "utilizacion": 0.75, "merma": 0.02, "eficiencia": 0.95, "costos_extra_usd_mes": 0.0},
                                       {"mes": 9, "utilizacion": 1.0, "merma": 0.0, "eficiencia": 1.0, "costos_extra_usd_mes": 0.0}]}],
                "financiamiento": {"aportes": [], "aporte_automatico": True, "caja_minima_usd": 0.0, "politica_dividendos": None,
                                   "deudas": [{"id": "D1", "monto": deuda, "tasa": 0.09, "tipo_tasa": "EFECTIVA_ANUAL",
                                               "base_tasa": "REAL", "plazo_meses": 84, "gracia_meses": 12, "metodo": "FRANCES",
                                               "frecuencia_meses": 1, "mes_desembolso": 1, "comision_pct": 0.0}]}
                if cfg != "C0" else {"aportes": [], "aporte_automatico": True, "caja_minima_usd": 0.0, "deudas": [],
                                     "politica_dividendos": None},
            }
    return out


def escenario_demo():
    esc = ES.nuevo("DEMO_ARTIFICIAL — SOLO_DEMOSTRACION", "DEMO_ARTIFICIAL")
    esc["id"] = "demo_artificial"
    esc["solo_demostracion"] = True
    esc["descripcion"] = ("Datos COMPLETAMENTE FICTICIOS para mostrar las funciones de la app. No usar como información del "
                          "proyecto. Universo ARTIFICIAL_TEST (CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO).")
    s = esc["simple"]
    s["objetivo"] = "GANAR_MAS"
    s["horizonte_anios"] = 10
    s["demanda"] = [
        {"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "categoria": "ASEGURADA", "valor": 2.0, "unidad": "t/dia"},
        {"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 6.0, "unidad": "t/dia"},
        {"producto": "pata_muslo", "canal": "supermercados", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 6.0, "unidad": "t/dia"},
        {"producto": "alas", "canal": "mayoristas", "mercado": "INTERNO", "categoria": "POTENCIAL", "valor": 2.0, "unidad": "t/dia"},
        {"producto": "menudencias", "canal": "mayoristas", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 1.0, "unidad": "t/dia"},
        {"producto": "garras", "canal": "mayoristas", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 1.0, "unidad": "t/dia"},
        {"producto": "carcasa_esqueleto", "canal": "industria", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 1.0,
         "unidad": "t/dia", "toma_todo": True},
        {"producto": "cuello", "canal": "industria", "mercado": "INTERNO", "categoria": "ESCENARIO", "valor": 1.0, "unidad": "t/dia",
         "toma_todo": True},
    ]
    for l in s["demanda"]:
        l.update(fuente=NOTA, estado="ESCENARIO")
    precios = (("pechuga", "supermercados", 3.10), ("pata_muslo", "supermercados", 1.90), ("alas", "mayoristas", 1.60),
               ("menudencias", "mayoristas", 1.00), ("garras", "mayoristas", 1.20), ("carcasa_esqueleto", "industria", 0.30),
               ("cuello", "industria", 0.40))
    s["precios_venta"] = [{"producto": p, "canal": c, "mercado": "INTERNO", "valor": v, "moneda": "USD", "unidad": "USD/kg",
                           "fuente": NOTA, "estado": "ESCENARIO"} for p, c, v in precios]
    x = esc["experto"]
    v = x["comun"]["valores"]
    v.update({"horizonte_anios": 10, "fecha_inicio": "2027-01-01", "meses_preoperacion": 2, "meses_construccion": 10,
              "meses_commissioning": 2, "tasa_descuento": 0.12, "tasa_descuento_accionista": 0.15,
              "impuestos.pct_iibb": 0.02, "impuestos.iibb_aplica_domestico": True, "impuestos.iibb_aplica_exportacion": False,
              "impuestos.pct_tasas_municipales": 0.005, "impuestos.otros_impuestos_usd_anio": 0.0,
              "impuestos.tasa_ganancias": 0.30, "impuestos.anios_quebranto": 5, "iva.modo": "EXCLUIDO",
              "dias_pago.alimento": 30, "dias_pago.pollitos": 21, "dias_pago.servicios": 30, "dias_pago.packaging": 30,
              "dias_pago.logistica": 30, "dias_pago.energia": 30,
              "dias_stock.producto_terminado": 4, "dias_stock.activo_biologico": 20, "dias_stock.alimento": 7,
              "dias_stock.packaging": 15, "dias_stock.repuestos": 30, "dias_stock.otros": 5, "dias_caja_operativa": 5})
    x["comun"]["inventarios"] = {"alimento": {"propiedad_empresa": True}, "materias_primas": {"propiedad_empresa": True, "dias": 15}}
    x["comun"]["canales"] = {
        "supermercados": {"dias_cobro": 45, "pct_descuentos": 0.03, "pct_bonificaciones": 0.01, "pct_devoluciones": 0.01,
                          "pct_comisiones": 0.0, "costo_logistico_usd_kg": 0.10},
        "mayoristas": {"dias_cobro": 21, "pct_descuentos": 0.02, "pct_bonificaciones": 0.0, "pct_devoluciones": 0.005,
                       "pct_comisiones": 0.0, "costo_logistico_usd_kg": 0.06},
        "industria": {"dias_cobro": 30, "pct_descuentos": 0.0, "pct_bonificaciones": 0.0, "pct_devoluciones": 0.0,
                      "pct_comisiones": 0.0, "costo_logistico_usd_kg": 0.04}}
    x["comun"]["alfa_negociada"] = None
    x["por_alternativa"] = por_alternativa()
    x["base_valores"].update({"mortalidad": 0.05, "condenas": 0.01, "traslado_fx": 0.5})
    x["disponibilidad"].update({"terreno_m2": 60000, "agua_m3_dia": 600, "potencia_kw": 1500, "facon_faena_aves_dia": 12000,
                                "m2_galpon_integrados": 250000, "pollitos_semana": 120000, "alimento_t_semana": 900,
                                "facon_alimento_t_semana": 900, "transporte_tercero_confirmado": True,
                                "frio_tercero_confirmado": True, "receptor_subproductos_confirmado": True})
    x["analisis"] = {"riesgo.peso.VAN_NEGATIVO_ESCENARIOS": 3.0, "riesgo.peso.SENSIBILIDAD_VAN": 2.0,
                     "riesgo.peso.PICO_FONDOS_RELATIVO": 1.0, "riesgo.peso.DEMANDA_NO_RESPALDADA": 1.0,
                     "decision.tolerancia_equivalencia": 0.05, "montecarlo.n": 200, "umbral.dscr_2d": 1.2,
                     "umbral.payback_2d": 6.0}
    x["stress"] = [
        {"id": "ST-DEM", "nombre": "Demanda −30 %", "shocks": {"demanda": -0.30}},
        {"id": "ST-ALI", "nombre": "Alimento +20 %", "shocks": {"alimento": 0.20}},
        {"id": "ST-PRE", "nombre": "Precio −10 %", "shocks": {"precio_venta": -0.10}},
        {"id": "ST-CAP", "nombre": "CAPEX +25 %", "shocks": {"capex": 0.25}},
        {"id": "ST-FIN", "nombre": "Financiero (tasa +50 %, cobro +30 días)", "shocks": {"tasa_descuento": 0.5, "dias_cobro": 30}},
        {"id": "ST-COMB", "nombre": "Combinado", "shocks": {"precio_venta": -0.10, "alimento": 0.20, "demanda": -0.20, "capex": 0.25}},
    ]
    x["distribuciones"] = [
        {"VARIABLE": "precio_venta", "DISTRIBUCION": "TRIANGULAR", "PARAMETROS": {"min": -0.2, "moda": 0.0, "max": 0.15},
         "FUENTE": NOTA, "ESTADO": "ARTIFICIAL"},
        {"VARIABLE": "alimento", "DISTRIBUCION": "NORMAL_TRUNCADA",
         "PARAMETROS": {"media": 0.0, "desvio": 0.1, "min": -0.3, "max": 0.4}, "FUENTE": NOTA, "ESTADO": "ARTIFICIAL"},
        {"VARIABLE": "demanda", "DISTRIBUCION": "UNIFORME", "PARAMETROS": {"min": -0.2, "max": 0.05}, "FUENTE": NOTA,
         "ESTADO": "ARTIFICIAL"}]
    x["correlaciones"] = [{"A": "precio_venta", "B": "alimento", "RHO": 0.5, "ESTADO": "ARTIFICIAL", "FUENTE": NOTA},
                          {"A": "demanda", "B": "precio_venta", "RHO": 0.0, "ESTADO": "ARTIFICIAL", "FUENTE": NOTA}]
    esc["procedencia"] = {"*": NOTA}
    return ES.validar(esc)
