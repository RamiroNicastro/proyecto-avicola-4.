"""Carga de los motores existentes (19–22) y catálogo de lo que la app puede pedir.

La app NO tiene fórmulas económicas: todo cálculo pasa por
  21_modelo_financiero/modelo_financiero.py  (construir_entrada, simular, resultados)
  22_riesgos/motor_riesgo.py                 (Evaluador, sensibilidades, stress, quiebres, Monte Carlo)
  22_riesgos/modelo_optimizador.py           (alternativas, fichas, ranking, Pareto, explicación)
Este módulo solo los importa (silenciando su salida por consola) y expone constantes de lectura.
"""
import csv
import io
import os
import sys
from contextlib import redirect_stdout

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(APP_DIR)
for _d in ("21_modelo_financiero", "22_riesgos"):
    _p = os.path.join(RAIZ, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
sys.dont_write_bytecode = True

with redirect_stdout(io.StringIO()):
    import modelo_financiero as mf      # noqa: E402
    import motor_riesgo as mr           # noqa: E402
    import modelo_optimizador as mopt   # noqa: E402

mcx, mo = mf.mcx, mf.mo

CONFIGURACIONES = ("C0", "C1", "C2", "C3", "CF")

# Explicación simple de cada configuración (texto de la app; la definición técnica vive en
# 00_gestion_proyecto/arquitecturas_maestras.csv y se muestra al lado, sin reinterpretarla).
EXPLICACION_CONFIG = {
    "C0": ("Sin planta propia (asset-light)",
           "La empresa compra pollitos, hace faenar a façon en un frigorífico de terceros, el alimento se elabora a façon "
           "y las granjas son de productores integrados. Poca inversión propia; depende de terceros."),
    "C1": ("Planta de faena propia",
           "Frigorífico propio. Pollito y alimento comprados; granjas de productores integrados; fletes de terceros."),
    "C2": ("Planta propia + parte de las granjas",
           "Frigorífico propio, una fracción de granjas propias (25 % en el preset), alimento a façon, flota mixta y "
           "frío refrigerado + congelado."),
    "C3": ("Integración amplia",
           "Frigorífico, granjas propias, incubación propia, planta de alimento propia, flota propia y tratamiento "
           "básico de subproductos."),
    "CF": ("Integración total (futuro)",
           "Como C3 más reproductoras y rendering propios. Es la configuración de mayor inversión y complejidad."),
}


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ruta(*partes):
    return os.path.join(RAIZ, *partes)


def versiones_motor():
    return {"modelo_financiero (21)": mf.VERSION, "motor_riesgo (22)": mr.VERSION,
            "modelo_optimizador (22)": mopt.VERSION, "modelo_capex (19)": mcx.VERSION, "modelo_opex (20)": mo.VERSION}


def arquitecturas():
    """Configuraciones base y variantes del mapa, con su definición técnica (sin reinterpretar)."""
    maestras = {r["CONFIGURACION"]: r for r in leer_csv(mf.ARCHIVO_ARQ_MAESTRAS)}
    out = []
    for r in mf.mapa_arquitecturas():
        es_base = r["TIPO"] == "CONFIGURACION_BASE"
        cfg = r["CONFIGURACION"] if es_base else r["VARIANTE_DE"]
        m = maestras.get(r["CONFIGURACION"]) or {}
        out.append({"id": r["CONFIGURACION"], "tipo": r["TIPO"], "configuracion": cfg,
                    "variante": None if es_base else r["ESCENARIO_REFERENCIA"],
                    "escala_referencia": None if es_base else int(r["ESCENARIO_REFERENCIA"].split("-")[1]),
                    "titulo": EXPLICACION_CONFIG.get(cfg, ("", ""))[0] if es_base else r["CONFIGURACION"],
                    "explicacion": EXPLICACION_CONFIG.get(cfg, ("", ""))[1] if es_base else r["OBSERVACIONES"],
                    "faena": r["FAENA"], "granjas": r["GRANJAS"], "pollito": r["POLLITO"], "alimento": r["ALIMENTO"],
                    "flota": r["FLOTA"], "frio": r["FRIO"], "subproductos": r["SUBPRODUCTOS"], "rendering": r["RENDERING"],
                    "estado_capex": r["ESTADO_CAPEX"], "estado_opex": r["ESTADO_OPEX"], "costeable": r["COSTEABLE"],
                    "observaciones_maestra": m.get("OBSERVACIONES", "")})
    return out


def escalas():
    """Escalas que el motor soporta: rango continuo de CAPEX (intermedias admitidas) y las de referencia."""
    lo, hi = mcx.RANGO_ESCALA
    return {"rango_min": lo, "rango_max": hi, "referencia": list(mcx.ESCALAS_REF), "unidad": "aves/día operativo",
            "trayectorias": {k: list(v) for k, v in mf.TRAYECTORIAS_FIN.items() if len(v) > 1},
            "nota": "Escalas intermedias admitidas por CAPEX dentro del rango; fuera del rango → gate ESCALA NO_FACTIBLE. "
                    "Calendario base 250 días operativos/año (variante C1-6dias = 300); días arbitrarios NO soportados (TF-001)."}


def productos():
    """Productos vendibles del balance 04 (kg comercial/ave por configuración de producto) consumidos vía el motor."""
    with redirect_stdout(io.StringIO()):
        prods, meta = mf.productos_balance("B", None, "venta_directa")
    return [{"producto": p, "kg_ave": x["kg_ave"], "categoria_ingreso": mf.CATEGORIA_PRODUCTO.get(p, ""),
             "grupo_precio": mr._cat_precio(p)} for p, x in prods.items()], meta


def variables_riesgo():
    return [{"id": v["ID"], "categoria": v["CATEGORIA"], "descripcion": v["DESCRIPCION"], "tipo_shock": v["TIPO_SHOCK"],
             "soporte": v["SOPORTE"], "campo_motor": v["CAMPO_MOTOR"], "bloque": v["BLOQUE_MOTOR"], "dpv": v["DPV"],
             "nota": v["NOTA"], "rango_quiebre": list(v["RANGO_QUIEBRE"])} for v in mr.VARIABLES.values()]


def inputs_riesgo():
    """Inputs de 22 (inputs_riesgo_optimizacion.csv) tal como los lee el motor."""
    inp, filas = mr.leer_inputs()
    return inp, filas


def catalogo():
    prods, meta = productos()
    inp, filas = inputs_riesgo()
    return {
        "arquitecturas": arquitecturas(), "escalas": escalas(), "productos": prods, "meta_productos": meta,
        "canales": list(mf.CANALES), "mercados": ["INTERNO", "EXPORTACION"],
        "categorias_demanda": list(mf.CATEGORIAS_DEMANDA),
        "categorias_demanda_evidencia": list(mf.CATEGORIAS_DEMANDA_EVIDENCIA),
        "unidades_demanda": ["kg/dia", "t/dia", "t/mes", "t/anio"],
        "objetivos": list(mopt.OBJETIVOS), "componentes_balanceado": list(mopt.COMP_BAL),
        "restricciones": {k: {"metrica": v[0], "sentido": v[1]} for k, v in mopt.RESTRICCIONES.items()},
        "reglas_status_quo": mopt.REGLAS_STATUS_QUO, "componentes_riesgo": list(mopt.COMPONENTES_RIESGO),
        "variables_riesgo": variables_riesgo(), "metricas_sensibilidad": list(mr.METRICAS_SENS),
        "distribuciones": list(mr.DISTRIBUCIONES), "estados_distribucion": list(mr.ESTADOS_DIST),
        "stress_motor": [{"id": s["ID_STRESS"], "nombre": s["NOMBRE"], "shocks": s["shocks"], "pendientes": s["pendientes"],
                          "activo": s["activo"], "origen": sorted(s["origen"])} for s in mr.leer_stress()],
        "inputs_riesgo": [{"parametro": f.get("PARAMETRO"), "valor": f.get("VALOR"), "unidad": f.get("UNIDAD"),
                           "estado": f.get("ESTADO"), "grupo": f.get("GRUPO")} for f in filas.values()],
        "metodos_deuda": list(mf.METODOS_DEUDA), "tipos_tasa_deuda": list(mf.TIPOS_TASA_DEUDA),
        "tipos_tasa_descuento": list(mf.TIPOS_TASA_DESCUENTO), "metodos_valor_terminal": list(mf.METODOS_VT),
        "categorias_inventario": list(mf.CATEGORIAS_INVENTARIO), "grupos_proveedor": list(mo.GRUPOS_CXP),
        "naturalezas_opex": list(mf.NATURALEZAS), "plantillas_rampup": list(mf.PLANTILLAS),
        "etiquetas": {"simulacion": mf.ETIQUETA_SIM, "override_total": mf.ETIQUETA_OVERRIDE_TOTAL,
                      "artificial": mr.ETIQ_ART, "no_publicable": mf.NO_PUB, "no_disponible_escenario": mf.NO_DISP_ESC},
    }


def variables_riesgo_por_id(vid):
    return next(v for v in variables_riesgo() if v["id"] == vid)
