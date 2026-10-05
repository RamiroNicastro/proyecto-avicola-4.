"""Tests de la corrección de UX (sesión 22, v1.1): contenido del estudio, navegación, búsqueda, glosario, BALANCEADO y DSCR.

Los criterios de usuario no técnico que requieren navegador (clics desde el inicio, recorrido, estados vacíos, códigos
técnicos fuera del texto principal) están en flujos_ui.mjs. Aquí se verifica el contrato de datos que los sostiene.
"""
import copy
import csv
import os
import re
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
os.environ.setdefault("APP_AVICOLA_DATOS", tempfile.mkdtemp(prefix="app_avicola_test_"))

from backend import almacen as A                 # noqa: E402
from backend import escenario as ES              # noqa: E402
from backend import estudio as EST               # noqa: E402
from backend import estudio_contenido as C       # noqa: E402
from backend import motor as M                   # noqa: E402
from backend import servicios as S               # noqa: E402
from backend import servidor as SV               # noqa: E402

TEMAS = ["mercado", "demanda", "producción", "balance de masa", "productos", "subproductos", "proceso", "maquinaria", "agua", "efluentes",
         "energía", "frío", "normativa", "exportación", "localización", "logística", "layout", "rrhh", "incubación", "alimento",
         "capex", "opex", "capital de trabajo", "finanzas", "riesgos", "optimizador"]
SECCIONES_ENTENDER = ["mercado", "produccion", "incubacion", "alimento", "granjas", "transporte_vivo", "faena", "proceso", "productos",
                      "subproductos", "frio", "agua", "energia", "logistica", "localizacion", "layout", "rrhh", "normativa", "exportacion",
                      "capex", "opex", "finanzas", "riesgos", "crecimiento"]


def get(ruta, q=None):
    st, _, c = SV.manejar("GET", ruta, None, q or {})
    return st, c


class U01Estudio(unittest.TestCase):
    def test_estudio_completo_tiene_todos_los_modulos(self):
        ix = EST.indice()
        temas = [t["tema"].lower() for t in ix["estudio_completo"]]
        for t in TEMAS:
            self.assertIn(t, temas, f"falta {t} en ESTUDIO COMPLETO")
        ids = {m["id"] for m in C.MODULOS}
        for s in SECCIONES_ENTENDER:
            self.assertIn(s, ids, f"falta la sección {s} en ENTENDER EL PROYECTO")

    def test_cada_modulo_responde_cinco_preguntas_y_dpv_existen(self):
        dpv = EST.PR.dpv_registro()
        for m in C.MODULOS:
            f = EST.modulo(m["id"])
            self.assertEqual([p["id"] for p in f["preguntas"]], ["que_es", "por_que", "que_modelamos"])
            self.assertTrue(f["que_sabemos"] and all(x["etiqueta"] in C.ETIQUETAS_CONFIANZA for x in f["que_sabemos"]))
            for d in f["que_falta"]:
                self.assertIn(d["id"], dpv, f"{m['id']}: {d['id']} no existe en datos_por_validar.md")
            for d in m["docs"] + m["tablas"]:
                self.assertTrue(os.path.exists(M.ruta(d)), d)

    def test_ningun_dato_del_estudio_figura_como_validado(self):
        """Ninguna cifra del proyecto está VERIFICADA hoy (DPV-009): el contenido no puede rotular nada como validado."""
        self.assertFalse(any(e == "VERIFICADO" for m in C.MODULOS for _, e in m["que_sabemos"]))

    def test_cadena_y_ramas(self):
        c = EST.cadena()
        self.assertEqual([n["id"] for n in c["nodos"]][:1] + [n["id"] for n in c["nodos"]][-1:], ["huevo", "cliente"])
        self.assertEqual({r["id"] for r in c["ramas"]}, {"subproductos", "efluentes", "rendering", "exportacion"})

    def test_documento_tecnico_solo_lista_blanca(self):
        st, c = get("/api/doc_estudio", {"ruta": "10_localizacion/conclusiones_localizacion.md"})
        self.assertEqual(st, 200)
        st, c = get("/api/doc_estudio", {"ruta": "../../etc/passwd"})
        self.assertEqual(st, 400)


class U02Localizacion(unittest.TestCase):
    def test_sin_ranking_inventado(self):
        L = EST.localizacion()
        self.assertEqual(L["mensaje"], "Todavía no existe una ubicación ganadora porque faltan datos de campo.")
        self.assertEqual(L["ranking"]["estado"], "NO_EMITIDO")
        self.assertEqual(L["celdas"]["verificadas"], 0)
        self.assertEqual(len(L["regiones"]), 13)
        self.assertFalse(any("lat" in r or "lon" in r or "puntaje" in r for r in L["regiones"]))     # sin coordenadas ni puntajes
        self.assertEqual({g["tipo"] for g in L["gates"]}, {"DURO", "CONDICIONAL"})
        self.assertEqual(len(L["gates"]), 11)


class U03ProcesoProductosEscalas(unittest.TestCase):
    def test_proceso_ordenado_con_aviso_de_benchmark(self):
        P = EST.proceso(10000)
        ns = [e["n"] for e in P["etapas"]]
        self.assertEqual(ns, sorted(ns))
        self.assertGreaterEqual(len(P["etapas"]), 20)
        self.assertIn("no son una especificación", P["aviso"])
        e1 = P["etapas"][0]
        self.assertTrue(e1["equipos"] and e1["capacidad"])

    def test_productos_avisan_que_las_rutas_no_se_suman(self):
        P = EST.productos()
        self.assertIn("NO se suman", P["aviso_rutas"])
        motor = {x["producto"]: x["kg_ave"] for x in P["balance_motor"]}
        self.assertEqual(motor, {p: x["kg_ave"] for p, x in M.mf.productos_balance("B", None, "venta_directa")[0].items()})

    def test_escalas_solo_modeladas_y_aviso(self):
        S_ = EST.escalas()
        self.assertEqual(S_["aviso"], "Capacidad no significa que vayamos a vender todo.")
        aves = next(f for f in S_["filas"] if f["id"] == "aves_dia")
        self.assertEqual(aves["valores"], [2500, 5000, 10000, 20000])
        anio = next(f for f in S_["filas"] if f["id"] == "aves_anio")
        self.assertEqual(anio["valores"], [625000, 1250000, 2500000, 5000000])

    def test_arquitecturas_respetan_csv_maestro(self):
        A_ = EST.arquitecturas()
        with open(M.ruta("00_gestion_proyecto", "arquitecturas_maestras.csv"), encoding="utf-8") as fh:
            maestras = {r["CONFIGURACION"]: r for r in csv.DictReader(fh)}
        self.assertEqual([a["id"] for a in A_["arquitecturas"]], ["C0", "C1", "C2", "C3", "CF"])
        self.assertEqual([a["nombre"] for a in A_["arquitecturas"]], ["ARRANQUE ASSET-LIGHT", "PLANTA DE FAENA PROPIA", "INTEGRACIÓN SELECTIVA",
                                                                      "MAYOR INTEGRACIÓN", "ARQUITECTURA FUTURA"])
        for a in A_["arquitecturas"]:
            for d in a["dimensiones"]:
                self.assertEqual(d["definicion"], maestras[a["id"]][d["id"]])          # definición exacta, sin reinterpretar
                self.assertIn(d["clase"], ("PROPIO", "TERCERIZADO", "MIXTO", "FUTURO", "NO TIENE"))
        c0 = {d["id"]: d["clase"] for d in A_["arquitecturas"][0]["dimensiones"]}
        cf = {d["id"]: d["clase"] for d in A_["arquitecturas"][4]["dimensiones"]}
        self.assertEqual(c0["FAENA"], "TERCERIZADO")
        self.assertEqual(cf["RENDERING"], "FUTURO")


class U04BusquedaGlosario(unittest.TestCase):
    def test_busqueda_lleva_a_la_seccion(self):
        casos = {"localización": "localizacion", "faena": "proceso", "agua": "estudio/agua", "10.000": "escalas", "CAPEX": "estudio/capex",
                 "pollitos": "estudio/incubacion", "Chaco": "localizacion", "halal": "estudio/exportacion"}
        for q, ruta in casos.items():
            st, c = get("/api/buscar", {"q": q})
            self.assertEqual(st, 200)
            self.assertEqual(c["datos"]["resultados"][0]["ruta"], ruta, q)

    def test_glosario_buscable(self):
        G = EST.glosario()
        self.assertGreater(len(G["terminos"]), 300)
        terms = {t["termino"].upper() for t in G["terminos"]}
        for t in ("VAN", "TIR", "DSCR", "CAPEX", "OPEX", "FCR", "FTE", "RENDERING", "FAÇON", "RAMP-UP"):
            self.assertTrue(any(t in x for x in terms) or t in C.AYUDAS, t)
        st, c = get("/api/buscar", {"q": "conversión alimenticia"})
        self.assertTrue(any(r["tipo"] == "TERMINO" for r in c["datos"]["resultados"]))

    def test_ayudas_kpi_textos_pedidos(self):
        self.assertTrue(C.AYUDAS["VAN"].startswith("Valor actual neto: cuánto valor genera el proyecto por encima de la rentabilidad mínima que le exigís"))
        for k in ("VAN", "TIR", "DSCR", "CAPEX", "OPEX", "FCR", "FTE", "RENDERING", "FAÇON", "RAMP-UP"):
            self.assertIn(k, C.AYUDAS)
            self.assertLessEqual(C.AYUDAS[k].count(". "), 3)

    def test_estados_en_castellano(self):
        self.assertEqual(C.ESTADOS["NO_CALCULABLE_REGLA_FISCAL_PENDIENTE"][:60],
                         "No se puede calcular todavía porque falta definir el tratamiento fiscal"[:60])
        for cod in ("NO_INVERTIR_AUN", "PESOS_NO_DEFINIDOS", "NO_CALCULABLE", "OPTIMIZACION_REAL_NO_DISPONIBLE"):
            self.assertNotRegex(C.ESTADOS[cod], r"[A-Z]+_[A-Z]+")
        self.assertNotEqual(C.ESTADOS["PESOS_NO_DEFINIDOS"], C.ESTADOS["NO_INVERTIR_AUN"])


class U05EstadoYSeguir(unittest.TestCase):
    def test_donde_estamos(self):
        E_ = EST.estado_proyecto()
        self.assertEqual(E_["intro"], "Hoy el motor está construido, pero los datos reales todavía no están validados.")
        sem = {s["id"]: s["estado"] for s in E_["semaforo"]}
        self.assertEqual(sem, {"MOTOR": "COMPLETO", "FISICOS": "PARCIALES", "ECONOMICOS": "MUY INCOMPLETOS", "EVIDENCIA": "0 %", "DECISION": "NO DISPONIBLE"})
        self.assertTrue(E_["terminado"] and E_["pendiente"] and E_["se_puede_simular"] and E_["no_se_puede_decidir"])

    def test_para_seguir_avanzando_conserva_empates(self):
        Q = EST.que_hacer_agrupado()
        g1 = Q["grupos"][0]
        self.assertTrue(g1["titulo"].startswith("PRIORIDAD 1 — EMPATE"))
        with open(M.ruta("22_riesgos", "prioridad_validacion.csv"), encoding="utf-8") as fh:
            n1 = sum(1 for r in csv.DictReader(fh) if r["UNIVERSO"] == "EVIDENCIA" and r["RANK_COMPARTIDO"] == "1")
        self.assertEqual(len(g1["items"]), n1)


class U06BalanceadoDscr(unittest.TestCase):
    def test_pesos_no_definidos_no_es_no_invertir(self):
        e = A.leer("demo_artificial")
        e["simple"]["objetivo"] = "BALANCEADO"
        with self.assertRaises(ES.ErrorEscenario) as cm:
            S.simular(e)
        self.assertIn("NO significa «no invertir»", str(cm.exception))
        e["experto"]["analisis"] = {k: v for k, v in e["experto"]["analisis"].items() if not k.startswith("riesgo.peso.")}
        e["experto"]["analisis"]["balanceado.peso.riesgo"] = 100                      # riesgo sin pesos del score → bloquea
        with self.assertRaises(ES.ErrorEscenario) as cm:
            S.optimizar(e)
        self.assertTrue(str(cm.exception).startswith("RIESGO_SIN_PESOS"))

    def test_dscr_minimo_indica_rampa(self):
        e = A.leer("demo_artificial")
        r = S.simular(e, "DEMO-C1|BASE|10000|ESCALA_UNICA")
        d = r["detalle"]["dscr"]
        self.assertIsNotNone(d)
        self.assertAlmostEqual(d["dscr_minimo"], r["detalle"]["resultados"]["DSCR_MINIMO"])     # mismo valor que el motor
        self.assertAlmostEqual(min(p["dscr"] for p in d["periodos"]), d["dscr_minimo"])
        self.assertTrue(d["incluye_rampa"])
        self.assertIn("no significa que la deuda sea impagable", d["nota"])
        self.assertNotIn("impagable.", d["nota"].replace("no significa que la deuda sea impagable", ""))

    def test_rutas_nuevas_responden(self):
        for r in ("/api/estudio", "/api/cadena", "/api/localizacion", "/api/proceso", "/api/productos_ave", "/api/arquitecturas",
                  "/api/escalas", "/api/glosario", "/api/estado_proyecto", "/api/seguir", "/api/textos", "/api/estudio/faena"):
            st, c = get(r)
            self.assertEqual(st, 200, r)
        self.assertEqual(get("/api/estudio/no_existe")[0], 404)


if __name__ == "__main__":
    unittest.main(verbosity=2)
