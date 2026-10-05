"""Tests de FLUJO de usuario contra el servidor HTTP real (#52). Levantan la app en un puerto libre (hilo) y recorren
los 6 flujos con las mismas llamadas que hace la interfaz. Los flujos en navegador están en flujos_ui.mjs (Playwright)."""
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
os.environ.setdefault("APP_AVICOLA_DATOS", tempfile.mkdtemp(prefix="app_avicola_flujos_"))

from backend import servidor as SV   # noqa: E402

C0 = "DEMO-C0|BASE|10000|ESCALA_UNICA"
C1 = "DEMO-C1|BASE|10000|ESCALA_UNICA"


class Cliente:
    def __init__(self, base):
        self.base = base

    def _req(self, metodo, ruta, cuerpo=None):
        data = json.dumps(cuerpo).encode() if cuerpo is not None else None
        r = urllib.request.Request(self.base + ruta, data=data, method=metodo, headers={"Content-Type": "application/json"} if data else {})
        try:
            with urllib.request.urlopen(r, timeout=600) as resp:
                ct, txt = resp.headers.get("Content-Type", ""), resp.read().decode("utf-8")
                st = resp.status
        except urllib.error.HTTPError as e:
            ct, txt, st = e.headers.get("Content-Type", ""), e.read().decode("utf-8"), e.code
        return st, (json.loads(txt) if "json" in ct else txt)

    def get(self, ruta):
        return self._req("GET", ruta)

    def post(self, ruta, cuerpo):
        return self._req("POST", ruta, cuerpo)


class Flujos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.srv = SV.crear_servidor("127.0.0.1", 0)
        cls.hilo = threading.Thread(target=cls.srv.serve_forever, daemon=True)
        cls.hilo.start()
        cls.c = Cliente(f"http://127.0.0.1:{cls.srv.server_address[1]}")

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        cls.srv.server_close()

    def ok(self, st, r):
        self.assertEqual(st, 200, r)
        self.assertTrue(r["ok"], r)
        return r["datos"]

    def test_flujo1_crear_cargar_simular_ver(self):
        st, html = self.c.get("/")
        self.assertEqual(st, 200)
        self.assertIn("Proyecto Avícola", html)
        esc = self.ok(*self.c.post("/api/nuevo", {"nombre": "flujo 1"}))
        esc["simple"]["objetivo"] = "GANAR_MAS"
        esc["simple"]["arquitectura"] = {"modo": "MANUAL", "configuracion": "C1", "variante": None}
        esc["simple"]["escala"] = {"modo": "VALOR", "valor": 5000}
        esc["simple"]["demanda"] = [{"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "categoria": "POTENCIAL",
                                     "valor": 3, "unidad": "t/dia"}]
        esc["simple"]["precios_venta"] = [{"producto": "pechuga", "canal": "supermercados", "mercado": "INTERNO", "valor": 3.1,
                                           "moneda": "USD", "estado": "ESCENARIO", "fuente": "hipótesis"}]
        r = self.ok(*self.c.post("/api/simular", {"escenario": esc}))
        self.assertEqual(r["resultado"], "ALTERNATIVA")
        self.assertEqual(r["alternativa"]["id"], "C1|BASE|5000|ESCALA_UNICA")
        ids = [c["id"] for c in r["tarjetas"]]
        for k in ("alternativa", "inversion", "negocio", "retorno", "deuda", "riesgo", "evidencia", "limitacion"):
            self.assertIn(k, ids)
        self.assertTrue(r["que_hacer"])
        self.assertIn("No constituye una recomendación", r["disclaimer"])

    def test_flujo2_comparar_c0_c1(self):
        demo = self.ok(*self.c.get("/api/escenarios/demo_artificial"))
        alts = self.ok(*self.c.post("/api/alternativas", {"escenario": demo}))
        self.assertTrue(any(a["id"] == C0 and a["completa"] for a in alts["alternativas"]))
        r = self.ok(*self.c.post("/api/comparar", {"escenario": demo, "ids": [C0, C1]}))
        self.assertTrue(r["comparable"])
        self.assertEqual({f["id"] for f in r["fichas"]}, {C0, C1})
        self.assertTrue(all(f["metricas"]["VAN"] is not None for f in r["fichas"]))

    def test_flujo3_optimizar_con_limite_de_capital(self):
        demo = self.ok(*self.c.get("/api/escenarios/demo_artificial"))
        demo["simple"]["capital"] = {"no_se": False, "valor": 1_200_000, "moneda": "USD", "metrica": "PICO_FONDOS"}
        r = self.ok(*self.c.post("/api/optimizar", {"escenario": demo}))
        d = r["decision_principal"]
        self.assertEqual(d["OBJETIVO"], "MAX_VAN")
        cap = next(x for x in r["restricciones_declaradas"] if x["NOMBRE"] == "CAPITAL_DISPONIBLE")
        self.assertEqual(cap["VALOR"], 1_200_000)
        if d["ESTADO"] == "MEJOR_EN_ESCENARIO":
            best = next(f for f in r["fichas"] if f["id"] == d["MEJOR"])
            self.assertLessEqual(best["metricas"]["PICO_FONDOS"], 1_200_000)
        excl = [f for f in r["fichas"] if "CAPITAL_DISPONIBLE" in ((f["ranking"].get("MAX_VAN") or {}).get("MOTIVO") or "")]
        self.assertTrue(excl, "el límite de capital debe excluir alternativas")

    def test_flujo4_stress(self):
        demo = self.ok(*self.c.get("/api/escenarios/demo_artificial"))
        st = [{"id": "U1", "nombre": "alimento +25 %", "shocks": {"alimento": 0.25}}, {"id": "U2", "nombre": "pendiente", "shocks": {"precio_venta": None}}]
        r = self.ok(*self.c.post("/api/riesgo/stress", {"escenario": demo, "alternativa": C1, "stresses": st}))
        f1 = next(f for f in r["filas"] if f["ID_STRESS"] == "U1")
        self.assertEqual(f1["ESTADO"], "OK")
        self.assertLess(f1["VAN"], r["base"]["VAN"])
        f2 = next(f for f in r["filas"] if f["ID_STRESS"] == "U2")
        self.assertEqual(f2["ESTADO"], "NO_EJECUTADO_VALORES_PENDIENTES")

    def test_flujo5_guardar_exportar_importar(self):
        demo = self.ok(*self.c.get("/api/escenarios/demo_artificial"))
        st, r = self.c.post("/api/escenarios", {"escenario": demo})
        self.assertEqual(st, 400)                                   # la demo base es de solo lectura
        demo["id"] = "flujo5"
        g = self.ok(*self.c.post("/api/escenarios", {"escenario": demo}))
        self.assertIn("flujo5", [x["id"] for x in self.ok(*self.c.get("/api/escenarios"))])
        dup = self.ok(*self.c.post("/api/escenarios/flujo5/duplicar", {"nombre": "copia flujo5"}))
        ren = self.ok(*self.c.post(f"/api/escenarios/{dup['id']}/renombrar", {"nombre": "renombrado"}))
        self.assertEqual(ren["nombre"], "renombrado")
        exp = self.ok(*self.c.post("/api/exportar/json", {"escenario": g}))
        self.assertIn("sello", exp)
        imp = self.ok(*self.c.post("/api/escenarios/importar", {"escenario": exp}))
        a = self.ok(*self.c.post("/api/simular", {"escenario": g, "alternativa": C1}))
        b = self.ok(*self.c.post("/api/simular", {"escenario": imp, "alternativa": C1}))
        self.assertEqual(a["alternativa"]["metricas"], b["alternativa"]["metricas"])
        st, csv = self.c.post("/api/exportar/csv", {"escenario": g, "alternativa": C1})
        self.assertEqual(st, 200)
        self.assertTrue(csv.startswith("SECCION,CAMPO,VALOR"))
        st, html = self.c.post("/api/exportar/resumen", {"escenario": g, "alternativa": C1})
        self.assertIn("Resumen de escenario", html)
        st, r = self.c._req("DELETE", f"/api/escenarios/{dup['id']}")
        self.ok(st, r)

    def test_flujo6_que_validar(self):
        r = self.ok(*self.c.get("/api/validacion"))
        claves = [p["clave"] for p in r["plan"]["paquetes"]]
        for p in ("CLIENTES", "PLANTA", "ALIMENTO", "POLLITOS", "GRANJAS", "UTILITIES", "TERRENO", "LOGÍSTICA", "RRHH", "IMPUESTOS",
                  "FINANCIAMIENTO", "EXPORTACIÓN"):
            self.assertIn(p, claves)
        self.assertTrue(all(p["pedidos"] for p in r["plan"]["paquetes"]))
        pr = r["prioridad"]["prioridad"]
        ranks = [int(x["RANK_COMPARTIDO"]) for x in pr]
        self.assertGreater(len(ranks), len(set(ranks)))             # hay empates compartidos y se conservan
        dims = [d["id"] for d in r["progreso"]["dimensiones"]]
        self.assertEqual(dims, ["ESTRUCTURA", "FISICA", "ECONOMICA", "EVIDENCIA"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
