"""Tests de backend de la APP V1 (#51). Ejecutar: python3 app/tests/correr_tests.py  (o python3 -m unittest desde app/).

Usan el escenario DEMO_ARTIFICIAL (datos ficticios) y escenarios vacíos. Ningún test escribe en archivos de evidencia: los
datos locales van a una carpeta temporal (APP_AVICOLA_DATOS).
"""
import copy
import json
import os
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
os.environ.setdefault("APP_AVICOLA_DATOS", tempfile.mkdtemp(prefix="app_avicola_test_"))

from backend import almacen as A            # noqa: E402
from backend import demo, generar_base       # noqa: E402
from backend import escenario as ES          # noqa: E402
from backend import exportar as X            # noqa: E402
from backend import motor as M               # noqa: E402
from backend import proyecto as PR           # noqa: E402
from backend import servicios as S           # noqa: E402
from backend import servidor as SV           # noqa: E402

C0 = "DEMO-C0|BASE|10000|ESCALA_UNICA"
C1 = "DEMO-C1|BASE|10000|ESCALA_UNICA"
HALAL = "DEMO-C1|C1-10000-HALAL|10000|ESCALA_UNICA"
_DEMO = None


def demo_esc():
    global _DEMO
    if _DEMO is None:
        _DEMO = A.leer("demo_artificial")
    return copy.deepcopy(_DEMO)


def vacio(cfg="C1", escala=10000):
    e = ES.nuevo("vacío")
    e["simple"]["arquitectura"] = {"modo": "MANUAL", "configuracion": cfg, "variante": None}
    e["simple"]["escala"] = {"modo": "VALOR", "valor": escala}
    return e


def items(sim):
    return [it for c in sim["tarjetas"] for it in c["items"] if it.get("estado") not in ("TEXTO", "SEMAFORO")]


class T01EvidenciaIntacta(unittest.TestCase):
    def test_escenario_no_modifica_evidencia(self):
        """Simular, optimizar, stress, guardar, importar y staging NO cambian ningún archivo de evidencia."""
        antes = PR.hashes_evidencia()
        self.assertGreaterEqual(len(antes), 8)
        e = demo_esc()
        e["simple"]["costos_unitarios"] = [{"concepto": "alimento", "valor": 300, "moneda": "USD", "estado": "COTIZACION", "fuente": "test"}]
        S.simular(e, C1)
        S.stress(e, C1)
        S.sensibilidad(e, C1, ["alimento"], [-0.1, 0, 0.1])
        g = A.guardar(dict(e, id="test_evidencia", tipo="DEMO_ARTIFICIAL"))
        A.importar(A.exportar(g))
        A.staging_agregar({"concepto": "alimento", "valor": "310", "unidad": "USD/t", "moneda": "USD", "fecha": "2026-10-05",
                           "fuente": "test", "tipo": "cotizacion"})
        self.assertEqual(antes, PR.hashes_evidencia())

    def test_staging_no_es_evidencia(self):
        f = A.staging_agregar({"concepto": "x", "valor": "1", "unidad": "USD/kg", "moneda": "USD", "fecha": "2026-10-05",
                               "fuente": "test", "tipo": "factura"})
        self.assertFalse(f["incorporado_a_evidencia"])
        self.assertTrue(f["nivel_evidencia"].startswith("SIN_CLASIFICAR"))
        with self.assertRaises(ES.ErrorEscenario):
            A.staging_agregar({"concepto": "x", "valor": "1", "unidad": "u", "moneda": "USD", "fecha": "2026-10-05", "fuente": "t", "tipo": "E1"})


class T02PendienteNoEsCero(unittest.TestCase):
    def test_campos_pendientes_no_se_muestran_como_cero(self):
        r = S.simular(vacio())
        self.assertEqual(r["resultado"], "ALTERNATIVA")
        its = items(r)
        nocalc = [i for i in its if i["estado"] == "NO_CALCULABLE"]
        self.assertTrue(nocalc)
        for i in its:
            if i["estado"] != "VALOR":
                self.assertIsNone(i["valor"], i["etiqueta"])
        for i in nocalc:
            self.assertTrue(i["faltan"], f"{i['etiqueta']} sin explicación de qué falta")
        van = next(i for i in its if i["etiqueta"] == "VAN")
        self.assertEqual(van["estado"], "NO_CALCULABLE")
        self.assertTrue(any(f["bloque"] == "PRECIOS" for f in van["faltan"]))
        self.assertIsNone(r["alternativa"]["metricas"]["VAN"])
        self.assertIsNone(r["detalle"]["series"])                 # sin horizonte no hay línea de tiempo (no ceros)

    def test_precio_no_se_queda_pendiente(self):
        e = demo_esc()
        for p in e["simple"]["precios_venta"]:
            if p["producto"] == "pechuga":
                p["estado"] = "NO_SE"
        ent = ES.a_motor(e)
        self.assertNotIn("pechuga|supermercados|INTERNO", ent["escenario"]["comun"]["precios"])
        r = S.simular(e, C1)
        van = next(i for i in items(r) if i["etiqueta"] == "VAN")
        self.assertEqual(van["estado"], "NO_CALCULABLE")
        self.assertIn("pechuga|supermercados|INTERNO", json.dumps(van["faltan"], ensure_ascii=False))

    def test_csv_no_convierte_faltante_en_cero(self):
        txt = X.csv_resultado(vacio())
        fila_van = next(l for l in txt.splitlines() if "Retorno · VAN" in l)
        self.assertIn("NO_CALCULABLE", fila_van)
        self.assertNotIn(",0,", fila_van)


class T03SimpleIgualExperto(unittest.TestCase):
    def test_modo_simple_igual_a_experto(self):
        """Los mismos inputs cargados por la capa simple o directamente en la estructura del motor dan el mismo resultado."""
        a = demo_esc()
        a["simple"]["restricciones"] = {"PAYBACK": 9.0}
        b = demo_esc()
        sb, cb = b["simple"], b["experto"]["comun"]
        cb["demanda"] = [{"id": f"S{i + 1:02d}", "producto": l["producto"], "canal": l["canal"], "mercado": l["mercado"],
                          "categoria": l["categoria"], "valor": float(l["valor"]), "unidad": l["unidad"], "prioridad": 1,
                          **({"toma_todo": True} if l.get("toma_todo") else {})} for i, l in enumerate(sb["demanda"])]
        cb["precios"] = {f"{p['producto']}|{p['canal']}|{p['mercado']}": {"tipo": "CONSTANTE", "usd_kg": p["valor"]} for p in sb["precios_venta"]}
        cb["valores"]["horizonte_anios"] = sb["horizonte_anios"]
        b["experto"]["analisis"].update({"restriccion.PAYBACK.valor": 9.0, "restriccion.PAYBACK.tipo": "HARD", "consulta.payback_max_anios": 9.0})
        sb["demanda"], sb["precios_venta"], sb["horizonte_anios"] = [], [], None
        ra, rb = S.simular(a, C1), S.simular(b, C1)
        self.assertEqual(ra["alternativa"]["metricas"], rb["alternativa"]["metricas"])
        self.assertEqual(ra["tarjetas"], rb["tarjetas"])
        self.assertEqual(ra["alternativa"]["restricciones"], rb["alternativa"]["restricciones"])


class T04Overrides(unittest.TestCase):
    def test_override_incompatible_se_rechaza(self):
        e = demo_esc()
        pa = e["experto"]["por_alternativa"][C1]
        pa["etapas"][0]["opex_rubros"].append({"rubro": "maíz", "grupo_proveedor": "granos", "naturaleza": "variable",
                                               "costo_pleno_usd_anio": 10.0, "es_compra": True, "dias_pago": 30.0, "iva_credito": False,
                                               "meta": {"CONFIGURACION": "C1", "ESCALA": 10000, "VARIANTE": "BASE",
                                                        "MODULO": "PLANTA_ALIMENTO_PROPIA", "UNIVERSO": "PLANTA_ALIMENTO",
                                                        "ORIGEN": "ESCENARIO_USUARIO"}})
        r = S.simular(e, C1)
        self.assertEqual(r["detalle"]["error_construccion"]["codigo"], "OVERRIDE_INCOMPATIBLE")
        self.assertIn("no corresponde a la arquitectura", r["detalle"]["error_construccion"]["mensaje"])
        self.assertIn("OVERRIDE_INCOMPATIBLE", [x["codigo"] for x in r["alertas"]])
        self.assertIsNone(r["alternativa"]["metricas"]["VAN"])

    def test_override_total_requiere_confirmacion(self):
        e = demo_esc()
        e["experto"]["comun"]["OVERRIDE_TOTAL_ARQUITECTURA"] = True
        with self.assertRaises(ES.ErrorEscenario) as cm:
            S.simular(e, C1)
        self.assertIn("OVERRIDE_TOTAL_SIN_CONFIRMAR", str(cm.exception))
        e["experto"]["override_total_confirmado"] = True
        r = S.simular(e, C1)
        self.assertEqual(r["detalle"]["resultados"]["ETIQUETA"], M.mf.ETIQUETA_OVERRIDE_TOTAL)
        self.assertIn("OVERRIDE_TOTAL", [x["codigo"] for x in r["alertas"]])


class T05NoInvertirAun(unittest.TestCase):
    def test_no_invertir_aun_se_representa(self):
        e = demo_esc()
        e["simple"]["capital"] = {"no_se": False, "valor": 50000, "moneda": "USD", "metrica": "PICO_FONDOS"}
        r = S.simular(e)                                         # arquitectura AUTO
        self.assertEqual(r["resultado"], "SIN_INVERSION")
        ni = r["no_invertir"]
        self.assertEqual(ni["estado_app"], "NO_INVERTIR_AUN")
        self.assertTrue(any(x.startswith("SQ-1") for x in ni["reglas"]))
        self.assertTrue(any(x.startswith("SQ-2") for x in ni["reglas"]))
        self.assertNotIn("fracaso", ni["titulo"].lower())
        self.assertIn("no un fracaso", ni["texto"])
        o = S.optimizar(e)
        sq = next(f for f in o["fichas"] if f["tipo"] == M.mr.STATUS_QUO)
        self.assertTrue(all(v is None for v in sq["metricas"].values()))         # sin VAN, TIR ni ranking
        self.assertTrue(all((x or {}).get("RANK") is None for x in sq["ranking"].values()))

    def test_balanceado_sin_pesos_no_es_no_invertir(self):
        """BALANCEADO sin pesos NO se ejecuta (bloqueo PESOS_NO_DEFINIDOS) y nunca se presenta como NO_INVERTIR_AUN."""
        e = demo_esc()
        e["simple"]["objetivo"] = "BALANCEADO"
        for fn in (S.simular, S.optimizar):
            with self.assertRaises(ES.ErrorEscenario) as cm:
                fn(e)
            self.assertTrue(str(cm.exception).startswith("PESOS_NO_DEFINIDOS"))
            self.assertNotIn("NO_INVERTIR_AUN", str(cm.exception))
        st, _, c = SV.manejar("POST", "/api/simular", {"escenario": e})
        self.assertEqual((st, c["error"]["codigo"]), (400, "PESOS_NO_DEFINIDOS"))
        e["experto"]["analisis"].update({f"balanceado.peso.{k}": 20 for k in ("rentabilidad", "capital", "liquidez", "robustez", "crecimiento")})
        o = S.optimizar(e)                                       # con pesos declarados sí se ejecuta
        self.assertEqual(o["decision_principal"]["OBJETIVO"], "BALANCEADO")
        self.assertNotEqual(o["decision_principal"].get("PESOS_BALANCEADO"), "PESOS_NO_DEFINIDOS")


class T06Comparabilidad(unittest.TestCase):
    def test_comparabilidad_se_respeta(self):
        r = S.comparar(demo_esc(), [C0, HALAL])
        self.assertFalse(r["comparable"])
        self.assertEqual(r["decisiones"], {})
        self.assertEqual(r["pareto"], [])
        self.assertEqual([x["id"] for x in r["no_comparables"]], [HALAL])
        ok = S.comparar(demo_esc(), [C0, C1])
        self.assertTrue(ok["comparable"])
        self.assertEqual(ok["decisiones"]["MAX_VAN"]["ESTADO"], "MEJOR_EN_ESCENARIO")
        with self.assertRaises(ES.ErrorEscenario):
            S.comparar(demo_esc(), [C0])


class T07ExportarImportar(unittest.TestCase):
    def test_exportado_importado_reproduce(self):
        e = demo_esc()
        e["simple"]["restricciones"] = {"VAN": 0.0}
        r1 = S.simular(e, C1)
        exp = json.loads(json.dumps(A.exportar(e)))
        self.assertEqual(exp["formato"], ES.FORMATO)
        self.assertIn("sello", exp)
        imp = A.importar(exp)
        S.limpiar_cache()
        r2 = S.simular(imp, C1)
        self.assertEqual(r1["alternativa"]["metricas"], r2["alternativa"]["metricas"])
        self.assertEqual(r1["tarjetas"], r2["tarjetas"])

    def test_formato_versionado(self):
        e = demo_esc()
        e["version_formato"] = 99
        with self.assertRaises(ES.ErrorEscenario):
            ES.validar(e)
        with self.assertRaises(ES.ErrorEscenario):
            ES.validar({"formato": "otro"})


class T08Etiquetas(unittest.TestCase):
    def test_simulacion_queda_etiquetada(self):
        r = S.simular(demo_esc(), C1)
        self.assertEqual(r["etiqueta"], M.mr.ETIQ_ART)
        self.assertTrue(r["solo_demostracion"])
        self.assertEqual(r["detalle"]["resultados"]["ETIQUETA"], M.mf.ETIQUETA_SIM)
        cods = [a["codigo"] for a in r["alertas"]]
        self.assertIn("SIMULACION", cods)
        self.assertIn("SOLO_DEMOSTRACION", cods)
        self.assertIn(TXT_DISCLAIMER, r["disclaimer"])
        u = S.simular(vacio())
        self.assertEqual(u["etiqueta"], M.mf.ETIQUETA_SIM)
        self.assertFalse(u["solo_demostracion"])
        html = X.resumen_html(demo_esc(), C1)
        self.assertIn("SOLO DEMOSTRACIÓN", html)
        self.assertIn(TXT_DISCLAIMER, html)

    def test_evidencia_queda_etiquetada(self):
        ev = PR.evidencia()
        self.assertEqual(ev["umbral"], ["E1", "E2", "E3"])
        self.assertEqual(ev["publicables"]["PUBLICABLE_VAN"], 0)
        self.assertTrue(all("NIVEL_EVIDENCIA" in p for p in ev["precios"]))
        # un precio declarado VALIDADO en el escenario NO se vuelve evidencia: su origen en la traza es ESCENARIO_USUARIO
        e = vacio()
        e["simple"]["demanda"] = [{"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "categoria": "ASEGURADA",
                                   "valor": 1, "unidad": "t/dia"}]
        e["simple"]["precios_venta"] = [{"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "valor": 3,
                                         "moneda": "USD", "estado": "VALIDADO", "fuente": "test"}]
        r = S.simular(e)
        self.assertEqual(r["etiqueta"], M.mf.ETIQUETA_SIM)
        origenes = {t["ORIGEN"] for t in r["detalle"]["traza"] if "precio" in t["VARIABLE"].lower()}
        self.assertNotIn("EVIDENCIA_REAL", origenes)


TXT_DISCLAIMER = "No constituye una recomendación de inversión"


class T09TirRapidaCompleta(unittest.TestCase):
    def test_tir_rapida_y_completa_consistentes(self):
        r = S.tir_rapida_completa(demo_esc(), C1)
        rap, com = r["rapida"], r["completa"]
        self.assertIsNone(rap["TIR"])
        self.assertEqual(rap["TIR_ESTADO"], M.mf.TIR_NO_CALCULADA)
        for k, v in com.items():
            if k in ("TIR", "TIR_ESTADO"):
                continue
            self.assertEqual(v, rap[k], k)
        self.assertNotEqual(com["TIR_ESTADO"], M.mf.TIR_NO_CALCULADA)


class T10Errores(unittest.TestCase):
    def test_errores_backend_mensaje_manejable(self):
        st, tipo, c = SV.manejar("POST", "/api/simular", {"escenario": {"formato": "x"}})
        self.assertEqual(st, 400)
        self.assertFalse(c["ok"])
        self.assertIn("mensaje", c["error"])
        st, _, c = SV.manejar("POST", "/api/simular", {})
        self.assertEqual(st, 400)
        orig = S.optimizar
        try:
            S.optimizar = lambda esc: 1 / 0
            SV.RUTAS_POST["/api/optimizar"] = lambda b: S.optimizar(b["escenario"])
            st, _, c = SV.manejar("POST", "/api/optimizar", {"escenario": demo_esc()})
        finally:
            S.optimizar = orig
            SV.RUTAS_POST["/api/optimizar"] = lambda b: S.optimizar(SV._esc(b))
        self.assertEqual(st, 500)
        self.assertEqual(c["error"]["codigo"], "ERROR_INTERNO")
        self.assertIn(c["error"]["ref"], c["error"]["mensaje"])
        self.assertNotIn("Traceback", json.dumps(c))
        self.assertNotIn("ZeroDivisionError", json.dumps(c))
        st, _, c = SV.manejar("GET", "/api/no_existe")
        self.assertEqual(st, 404)

    def test_ars_sin_tipo_de_cambio(self):
        e = vacio()
        e["simple"]["capital"] = {"no_se": False, "valor": 1e9, "moneda": "ARS"}
        st, _, c = SV.manejar("POST", "/api/simular", {"escenario": e})
        self.assertEqual(st, 400)
        self.assertIn("tipo de cambio", c["error"]["mensaje"])

    def test_escala_fuera_de_rango(self):
        e = vacio(escala=50000)
        with self.assertRaises(ES.ErrorEscenario):
            ES.validar(e)


class T11Extras(unittest.TestCase):
    def test_capital_no_asume_2M(self):
        e = ES.nuevo("x")
        self.assertTrue(e["simple"]["capital"]["no_se"])
        ent = ES.a_motor(e)
        self.assertIsNone(ent["inp"].get("restriccion.CAPITAL_DISPONIBLE.valor"))
        self.assertNotIn("2000000", json.dumps(ent["escenario"]))

    def test_demanda_potencial_no_se_convierte(self):
        e = demo_esc()
        cats = {l["categoria"] for l in ES.a_motor(e)["escenario"]["comun"]["demanda"]}
        self.assertIn("POTENCIAL", cats)
        r = S.simular(e, C1)
        self.assertTrue(r["alternativa"]["respaldo_comercial"].startswith("PARCIAL"))   # solo la ASEGURADA respalda

    def test_presets_sin_valores_economicos(self):
        for p in generar_base.presets():
            self.assertEqual(p["simple"]["precios_venta"], [])
            self.assertEqual(p["simple"]["demanda"], [])
            self.assertEqual(p["experto"]["por_alternativa"], {})
            vals = [v for k, v in p["experto"]["comun"]["valores"].items() if k not in ("valor_terminal.metodo", "tipo_tasa_descuento", "convencion_descuento")]
            self.assertTrue(all(v is None for v in vals))

    def test_demo_base_igual_al_generador(self):
        with open(os.path.join(M.APP_DIR, "escenarios_base", "demo_artificial.json"), encoding="utf-8") as fh:
            archivo = json.load(fh)
        self.assertEqual(archivo, json.loads(json.dumps(generar_base.demo_fijo())))
        self.assertTrue(archivo["solo_demostracion"])
        self.assertEqual(ES.universo(archivo), "ARTIFICIAL_TEST")

    def test_cache_no_sirve_otro_escenario(self):
        e = demo_esc()
        r1 = S.simular(e, C1)
        e2 = demo_esc()
        e2["simple"]["precios_venta"][0]["valor"] = 3.5
        r2 = S.simular(e2, C1)
        self.assertNotEqual(r1["alternativa"]["metricas"]["VAN"], r2["alternativa"]["metricas"]["VAN"])
        r3 = S.simular(demo_esc(), C1)
        self.assertEqual(r1["alternativa"]["metricas"], r3["alternativa"]["metricas"])

    def test_costo_unitario_via_modulo_20(self):
        rub, est, det = ES.rubro_desde_precio_unitario("C1", None, 10000, "alimento", 300.0)
        self.assertEqual(est, "APLICADO")
        self.assertEqual(rub["meta"]["MODULO"], "ALIMENTO_COMPRADO")
        self.assertGreater(rub["costo_pleno_usd_anio"], 0)
        rub, est, _ = ES.rubro_desde_precio_unitario("C3", None, 10000, "alimento", 300.0)
        self.assertIsNone(rub)
        self.assertEqual(est, "NO_APLICA_A_LA_ARQUITECTURA")

    def test_montecarlo(self):
        r = S.montecarlo(demo_esc(), C1, n=60)
        self.assertTrue(r["disponible"])
        self.assertIn("PROBABILIDAD_SIMULADA", r["tipo_probabilidad"])
        e = vacio()
        e["experto"]["distribuciones"] = []
        st, _, c = SV.manejar("POST", "/api/riesgo/montecarlo", {"escenario": e})
        self.assertEqual(st, 200)
        self.assertFalse(c["datos"]["disponible"])        # escenario vacío: NO_DISPONIBLE (no se inventan probabilidades)
        p = demo_esc()
        p["tipo"], p["solo_demostracion"] = "USUARIO", False
        p["experto"]["por_alternativa"] = {k[len(ES.PREFIJO_DEMO):]: v for k, v in p["experto"]["por_alternativa"].items()}
        p["experto"]["distribuciones"] = []
        r = S.montecarlo(p, "C1|BASE|10000|ESCALA_UNICA", n=50)
        self.assertFalse(r["disponible"])
        self.assertIn("Faltan distribuciones", r["explicacion"])

    def test_tornado_no_calculable_sin_van(self):
        e = demo_esc()
        e["experto"]["comun"]["valores"]["tasa_descuento"] = None
        with self.assertRaises(ES.ErrorEscenario):        # ninguna alternativa completa → no hay alternativa analizable
            S.tornado(e, None)
        r = S.tornado(e, C1)
        self.assertFalse(r["calculable"])
        self.assertTrue(all(t.get("SWING") is None for t in r["tornado"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
