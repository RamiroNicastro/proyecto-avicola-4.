#!/usr/bin/env python3
"""
TESTS Y MUTACIONES — riesgos, sensibilidades y optimizador (sesión 20)
=====================================================================
Se ejecutan con `python3 22_riesgos/modelo_optimizador.py --solo-tests` (o `--mutaciones`).
Grupos (secciones del encargo): SENS (45), RIE (46), MC (47), OPT (48), COMP (49), QUI (50), MUT (51).
Los casos son ARTIFICIALES (mf.caso_prueba y caso_artificial()); los valores esperados de los puntos de quiebre se
calculan a mano en cada test (CASO: CAPEX 100 en T0, ventas 100/año, OPEX 60/año, 5 años, 10 %, flujos anuales).
"""
import copy
import hashlib
import io
import os
import sys
from contextlib import redirect_stdout

sys.dont_write_bytecode = True
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import motor_riesgo as mr            # noqa: E402
import modelo_optimizador as mo      # noqa: E402

mf = mr.mf
ANUALIDAD = sum(1 / 1.1 ** t for t in range(1, 6))          # 3,790787
E_STAR = 100 / ANUALIDAD                                     # EBITDA anual con VAN = 0: 26,3797


def _alt(aid, **kw):
    kw.setdefault("convencion", "PERIODO_REPORTE")
    bv = kw.pop("base_valores", {})
    return {"id": aid, "tipo": "PLANTA", "universo": "CASO_ARTIFICIAL", "configuracion": aid, "variante": "ART",
            "escalas": (1,), "trayectoria": "ESCALA_UNICA", "construir": (lambda kw=kw: (mf.caso_prueba(**kw), None)),
            "base_valores": bv, "fisico": [], "cobertura": (0.0, "artificial")}


def _cerca(a, b, tol=1e-5):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


def _diff(a, b, p=""):
    """Rutas de hojas distintas entre dos estructuras."""
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for k in set(a) | set(b):
            out += _diff(a.get(k), b.get(k), f"{p}.{k}" if p else str(k))
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        out = []
        for i, (x, y) in enumerate(zip(a, b)):
            out += _diff(x, y, f"{p}[{i}]")
        return out
    return [] if a == b else [p]


PREFIJOS = {"precio": ("precios",), "stress": ("stress",), "canal": ("canales",), "rampup": ("etapas[0].rampup",),
            "rubros": ("etapas[0].opex_rubros",), "productos": ("productos", "meta_productos", "etapas[0].opex_rubros"),
            "capex_bloque": ("etapas[0].activos", "etapas[0].capex_usd"), "tasa_descuento": ("tasa_descuento",),
            "deuda": ("financiamiento.deudas",), "impuestos": ("impuestos",)}


def _familia(v):
    c = mr.VARIABLES[v]["CAMPO_MOTOR"]
    if c.startswith("precios"):
        return "precio"
    if c.startswith("stress"):
        return "stress"
    if c.startswith("canales"):
        return "canal"
    if "rampup" in c:
        return "rampup"
    if "opex_rubros" in c or c.startswith("rubros"):
        return "rubros"
    if c.startswith("productos"):
        return "productos"
    if "activos" in c:
        return "capex_bloque"
    if c.startswith("financiamiento"):
        return "deuda"
    if c.startswith("impuestos"):
        return "impuestos"
    return c


_U = {}


def universo_art():
    """Corrida artificial reducida (rápida) compartida por varios tests."""
    if "U" not in _U:
        inp = mo.inputs_artificiales(mr.leer_inputs()[0])
        inp.update({"sensibilidad.variables": ["precio_venta", "alimento", "capex", "demanda", "dias_cobro"],
                    "sens2d.pares": ["precio_venta×alimento"], "quiebre.variables": ["precio_venta", "capex"],
                    "montecarlo.n": 40, "tornado.metricas": ["VAN"], "robustez.variables": ["precio_venta", "demanda"]})
        dists, corrs = mo.dist_artificiales()
        with redirect_stdout(io.StringIO()):
            _U["U"] = mo.correr_universo(mo.caso_artificial(), inp, "CASO_ARTIFICIAL", mo.stress_artificiales(), dists, corrs)
        _U["inp"] = inp
    return _U["U"], _U["inp"]


def _hash(rutas):
    h = hashlib.sha256()
    for r in sorted(rutas):
        with open(r, "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()


def ejecutar_tests(verbose=True):
    T = []

    def test(tid, desc):
        def deco(fn):
            T.append((tid, desc, fn))
            return fn
        return deco

    # ------------------------------------------------------------------ SENSIBILIDAD (45)
    @test("SENS-01", "un shock +10 % cambia SOLO los campos de la variable elegida")
    def _():
        a = _alt("S01", opex_fijo=40.0, opex_var=20.0, deudas=[{"id": "D", "monto": 50.0, "tasa": 0.08, "tipo_tasa": "EFECTIVA_ANUAL",
                 "base_tasa": "REAL", "plazo_meses": 24, "gracia_meses": 0, "metodo": "FRANCES", "frecuencia_meses": 1,
                 "mes_desembolso": 0}], tasa_gan=0.3, dias_cobro=10.0, dias_pago=10.0,
                 activos=[{"clase": "PROCESO:x", "capex_usd": 60.0, "vida_util_anios": 5, "valor_residual_usd": 0.0, "costo_reemplazo_usd": 60.0},
                          {"clase": "OBRA_CIVIL:y", "capex_usd": 40.0, "vida_util_anios": 5, "valor_residual_usd": 0.0, "costo_reemplazo_usd": 40.0}],
                 base_valores={"mortalidad": 0.05})
        P0 = a["construir"]()[0]
        P0["impuestos"]["pct_iibb"] = 0.02
        P0["canales"]["supermercados"]["pct_descuentos"] = 0.05
        n = 0
        for v, d in mr.VARIABLES.items():
            if d["SOPORTE"] in ("DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"):
                continue
            s = 10.0 if d["TIPO_SHOCK"] != "RELATIVO" else 0.10
            P1, info = mr.aplicar_shocks(P0, {v: s}, a["base_valores"], "CASO_ARTIFICIAL")
            if P1 is None:
                continue
            n += 1
            dif = _diff(P0, P1)
            pref = PREFIJOS.get(_familia(v), (d["CAMPO_MOTOR"],))
            if not dif:
                assert any(("BASE_CERO_SIN_EFECTO" in x or x.startswith("TOPE_")) for x in info["flags"]), f"{v}: el shock no cambió nada"
                continue
            fuera = [x for x in dif if not x.startswith(pref)]
            assert not fuera, f"{v}: cambió {fuera}"
            if _familia(v) == "rubros" and v != "dias_pago":
                for i, (r0, r1) in enumerate(zip(P0["etapas"][0]["opex_rubros"], P1["etapas"][0]["opex_rubros"])):
                    if r0 != r1:
                        assert v in mr.clasificar_rubro(r0) or v == "fcr", f"{v} tocó el rubro {r0['rubro']}"
        assert n >= 20, n

    @test("SENS-02", "el escenario base no se modifica después de cientos de shocks")
    def _():
        a = _alt("S02", opex_fijo=40.0, opex_var=20.0)
        E = mr.Evaluador()
        P0 = copy.deepcopy(E.base(a)[0])
        for v in ("precio_venta", "alimento", "capex", "demanda", "dias_cobro", "utilizacion", "tasa_descuento"):
            for s in (-0.3, 0.1, 0.3):
                E.evaluar(a, {v: s})
        assert E.base(a)[0] == P0

    @test("SENS-03", "la evidencia no se perturba: shock en universo EVIDENCIA → error; archivos de evidencia intactos")
    def _():
        alts = mo.alternativas_reales(mr.leer_inputs()[0], "EVIDENCIA")
        a = alts[0]
        E = mr.Evaluador()
        try:
            E.evaluar(a, {"precio_venta": 0.1})
            raise AssertionError("se perturbó la evidencia")
        except mr.ErrorRiesgo:
            pass
        rutas = [os.path.join(mr.RAIZ, "21_modelo_financiero", x) for x in ("inputs_financieros.csv", "base_precios_venta.csv",
                                                                             "modelo_financiero.py")]
        rutas += [os.path.join(mr.RAIZ, "00_gestion_proyecto", x) for x in os.listdir(os.path.join(mr.RAIZ, "00_gestion_proyecto"))]
        h0 = _hash(rutas)
        U, _ = universo_art()
        E2 = mr.Evaluador()
        for x in mo.alternativas_reales(mr.leer_inputs()[0], "ESCENARIO", mo.leer_escenario())[:3]:
            E2.evaluar(x)
        assert _hash(rutas) == h0

    @test("SENS-04", "monotonía: VAN ↑ con precio y ↓ con CAPEX, alimento, plazo de cobro y tasa")
    def _():
        a = _alt("S04", opex_fijo=40.0, opex_var=20.0)
        E = mr.Evaluador()
        for v, sg, xs in (("precio_venta", 1, (-0.3, -0.1, 0, 0.1, 0.3)), ("capex", -1, (-0.3, 0, 0.3)),
                          ("alimento", -1, (-0.3, 0, 0.3)), ("dias_cobro", -1, (0, 30, 60)), ("tasa_descuento", -1, (-0.3, 0, 0.3))):
            vs = [E.evaluar(a, {v: x})["met"]["VAN"] for x in xs]
            assert all(sg * (b - c) < 0 for b, c in zip(vs, vs[1:])), (v, vs)
            assert mr.VARIABLES[v]["MONOTONIA_VAN"] == sg

    @test("SENS-05", "el tornado ordena por amplitud (máx − mín), no por impacto con signo")
    def _():
        filas = [{"ALTERNATIVA": "X", "VARIABLE": v, "SHOCK": s, "ESTADO": "OK", "VAN": val}
                 for v, s, val in (("a", 0.0, 10.0), ("a", -0.1, 9.0), ("a", 0.1, 11.0),
                                   ("b", 0.0, 10.0), ("b", -0.1, 20.0), ("b", 0.1, 0.0),
                                   ("c", 0.0, 10.0), ("c", -0.1, 7.0), ("c", 0.1, 14.0))]
        t = mr.tornado(filas, "VAN", "X")
        assert [x["VARIABLE"] for x in t] == ["b", "c", "a"], [x["VARIABLE"] for x in t]
        assert [x["RANK"] for x in t] == [1, 2, 3]
        U, _ = universo_art()
        for alt in {x["ALTERNATIVA"] for x in U["tornado"]}:
            sw = [x["SWING"] for x in sorted(U["tornado"], key=lambda r: r.get("RANK") or 99) if x["ALTERNATIVA"] == alt and x.get("RANK")]
            assert sw == sorted(sw, reverse=True)

    @test("SENS-06", "la sensibilidad 2D conserva ambos ejes y su eje Y = 0 coincide con el one-way")
    def _():
        a = _alt("S06", opex_fijo=40.0, opex_var=20.0)
        E = mr.Evaluador()
        inp = mr.leer_inputs()[0]
        f2 = mr.sensibilidad_2d(E, a, ("precio_venta", "alimento"), inp)
        xs, ys = mr.shocks_de("precio_venta", inp), mr.shocks_de("alimento", inp)
        assert len(f2) == len(xs) * len(ys)
        assert {(r["SHOCK_X"], r["SHOCK_Y"]) for r in f2} == {(x, y) for x in xs for y in ys}
        for r in f2:
            if r["SHOCK_Y"] == 0:
                assert _cerca(r["VAN"], E.evaluar(a, {"precio_venta": r["SHOCK_X"]})["met"]["VAN"])
        assert {r["ZONA_DSCR"] for r in f2} <= {"SIN_UMBRAL_DECLARADO", mr.NO_CALC}

    @test("SENS-07", "shock relativo sobre base 0 se informa (BASE_CERO_SIN_EFECTO); sin deuda → NO_APLICA; sin base → NO_CALCULABLE")
    def _():
        a = _alt("S07")
        E = mr.Evaluador()
        ev = E.evaluar(a, {"descuentos": 0.2})
        assert any("BASE_CERO_SIN_EFECTO" in f for f in ev["flags"])
        assert E.evaluar(a, {"tasa_deuda": 0.1})["estado"] == "NO_APLICA"
        assert E.evaluar(a, {"mortalidad": 0.1})["estado"] == mr.NO_CALC
        assert E.evaluar(a, {"dias_operativos": 0.1})["estado"] == "NO_APLICA"

    @test("SENS-08", "modo rápido (sin TIR) = modo completo en VAN, payback, pico y EBITDA; mf.tir se restaura")
    def _():
        a = _alt("S08", opex_fijo=40.0, opex_var=20.0, dias_cobro=20.0)
        E = mr.Evaluador()
        r = E.evaluar(a, {"capex": 0.1})["met"]
        c = mr.Evaluador().evaluar(a, {"capex": 0.1}, tir=True)["met"]
        for k in ("VAN", "PAYBACK", "PICO_FONDOS", "EBITDA", "FONDOS_INICIALES"):
            assert _cerca(r[k], c[k]), k
        assert r["TIR"] is None and r["TIR_ESTADO"] == mr.TIR_OMITIDA and c["TIR"] is not None
        assert mf.tir.__name__ == "tir"

    @test("SENS-09", "métrica no publicable en la base → tornado NO_CALCULABLE sin ranking")
    def _():
        a = _alt("S09")
        E = mr.Evaluador()
        ow = mr.sensibilidad_oneway(E, a, ["precio_venta", "capex"], mr.leer_inputs()[0])
        t = mr.tornado(ow, "DSCR", "S09")
        assert t and all(x["ESTADO"] == mr.NO_CALC and x.get("RANK") is None for x in t)

    # ------------------------------------------------------------------ RIESGO (46)
    reg = mr.leer_registro_riesgos()

    @test("RIE-01", "un riesgo PENDIENTE no se convierte en probabilidad 0 (ni ningún nivel en número)")
    def _():
        assert mr.probabilidad_numerica("PENDIENTE") is None and mr.probabilidad_numerica("ALTA") is None
        assert all(r["PROB_NUMERICA"] is None for r in mr.matriz_riesgos(reg))
        assert any(r["PROBABILIDAD"] == "PENDIENTE" for r in reg)

    @test("RIE-02", "la matriz cualitativa no fabrica score estadístico")
    def _():
        m = mr.matriz_riesgos(reg)
        clases = set(mr.CLASE_CUALITATIVA.values()) | {"PENDIENTE"}
        for r in m:
            assert r["CLASE_INHERENTE"] in clases and r["EXPOSICION_USD"] is None and r["IMPACTO_USD"] is None
            assert not any(isinstance(v, float) for v in r.values())

    @test("RIE-03", "la mitigación no elimina el riesgo inherente; residual = inherente si no está implementada")
    def _():
        m = mr.matriz_riesgos(reg)
        for r, f in zip(m, reg):
            assert r["CLASE_INHERENTE"] == mr.CLASE_CUALITATIVA.get((f["PROBABILIDAD"], f["IMPACTO"]), "PENDIENTE")
            if f["ESTADO_MITIGACION"] != "IMPLEMENTADA_CON_EVIDENCIA":
                assert r["CLASE_RESIDUAL"] == r["CLASE_INHERENTE"]
        fila = dict(reg[0], PROBABILIDAD="ALTA", IMPACTO="ALTA", ESTADO_MITIGACION="IMPLEMENTADA_CON_EVIDENCIA",
                    PROBABILIDAD_RESIDUAL="BAJA", IMPACTO_RESIDUAL="MEDIA")
        x = mr.matriz_riesgos([fila])[0]
        assert x["CLASE_INHERENTE"] == "CRITICO" and x["CLASE_RESIDUAL"] == "BAJO"

    @test("RIE-04", "correlaciones pendientes quedan señaladas (CORRELACIONES_NO_MODELADAS)")
    def _():
        U, _ = universo_art()
        ej = [r for r in U["mc"] if r.get("ESTADO") == "EJECUTADO"]
        assert ej and all(mr.CORR_NM in r["CORRELACIONES"] and "demanda–precio_venta" in r["CORRELACIONES"] for r in ej)
        assert all(c["ESTADO"] == "PENDIENTE" and c["RHO"] is None for c in mr.leer_correlaciones())

    @test("RIE-05", "el registro rechaza probabilidades numéricas y drivers inexistentes")
    def _():
        import tempfile, csv
        for cambio in ({"PROBABILIDAD": "0.3"}, {"DRIVER_AFECTADO": "variable_inexistente"}):
            with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8", newline="") as fh:
                w = csv.DictWriter(fh, fieldnames=list(reg[0]))
                w.writeheader()
                w.writerow(dict(reg[0], **cambio))
            try:
                mr.leer_registro_riesgos(fh.name)
                raise AssertionError(f"aceptó {cambio}")
            except mr.ErrorRiesgo:
                pass
            finally:
                os.unlink(fh.name)

    # ------------------------------------------------------------------ MONTE CARLO (47)
    def _mc(n=30, semilla=7, dists=None, corrs=None, aid="MC"):
        a = _alt(aid, opex_fijo=40.0, opex_var=20.0)
        d = dists or [mr.validar_distribucion({"VARIABLE": "precio_venta", "DISTRIBUCION": "TRIANGULAR",
                                                "PARAMETROS": {"min": -0.3, "moda": 0.0, "max": 0.2}, "FUENTE": "T", "ESTADO": "ARTIFICIAL"})]
        return mr.monte_carlo(mr.Evaluador(), a, d, corrs or [], n, semilla, "CASO_ARTIFICIAL")

    @test("MC-01", "misma semilla → mismos resultados; otra semilla → distintos")
    def _():
        e1, r1, m1, _ = _mc()
        e2, r2, m2, _ = _mc()
        _, r3, _, _ = _mc(semilla=8)
        assert e1 == "EJECUTADO" and [x["VAN"] for x in m1] == [x["VAN"] for x in m2]
        assert r1["VAN"]["MEDIA"] != r3["VAN"]["MEDIA"]

    @test("MC-02", "una distribución determinista produce un resultado determinista")
    def _():
        d = [mr.validar_distribucion({"VARIABLE": "precio_venta", "DISTRIBUCION": "DETERMINISTA", "PARAMETROS": {"valor": 0.1},
                                      "FUENTE": "T", "ESTADO": "ARTIFICIAL"})]
        _, r, m, _ = _mc(dists=d, aid="MC2")
        esperado = mr.Evaluador().evaluar(_alt("MC2b", opex_fijo=40.0, opex_var=20.0), {"precio_venta": 0.1})["met"]["VAN"]
        assert all(_cerca(x["VAN"], esperado) for x in m) and _cerca(r["VAN"]["P5"], r["VAN"]["P95"])

    @test("MC-03", "percentiles ordenados y probabilidades en [0, 1]")
    def _():
        _, r, _, _ = _mc(n=60)
        v = r["VAN"]
        assert v["P5"] <= v["P10"] <= v["P50"] <= v["P90"] <= v["P95"]
        for k in ("PROB_VAN_NEGATIVO", "PROB_NO_RECUPERO"):
            assert 0 <= r[k] <= 1
        assert r["PROB_DEFICIT"] is None or 0 <= r["PROB_DEFICIT"] <= 1

    @test("MC-04", "el proyecto real no corre Monte Carlo sin distribuciones respaldadas; ARTIFICIAL fuera de caso → error")
    def _():
        alts = mo.alternativas_reales(mr.leer_inputs()[0], "ESCENARIO", mo.leer_escenario())
        est, _, _, notas = mr.monte_carlo(mr.Evaluador(), alts[0], mr.leer_distribuciones(), [], 10, 1, "ESCENARIO")
        assert est == mr.MC_ND, est
        d = [mr.validar_distribucion({"VARIABLE": "precio_venta", "DISTRIBUCION": "UNIFORME", "PARAMETROS": {"min": -0.1, "max": 0.1},
                                      "FUENTE": "T", "ESTADO": "ARTIFICIAL"})]
        try:
            mr.monte_carlo(mr.Evaluador(), alts[0], d, [], 10, 1, "ESCENARIO")
            raise AssertionError("aceptó distribución artificial en el proyecto")
        except mr.ErrorRiesgo:
            pass

    @test("MC-05", "cuantiles exactos y cópula: triangular, normal truncada en rango, correlación declarada respetada")
    def _():
        tri = {"DISTRIBUCION": "TRIANGULAR", "PARAMETROS": {"min": 0.0, "moda": 0.0, "max": 1.0}}
        assert _cerca(mr.cuantil(tri, 0.75), 0.5)                       # F(x) = 1 − (1 − x)²
        nt = {"DISTRIBUCION": "NORMAL_TRUNCADA", "PARAMETROS": {"media": 0.0, "desvio": 1.0, "min": -0.5, "max": 0.5}}
        assert all(-0.5 <= mr.cuantil(nt, u) <= 0.5 for u in (0.001, 0.5, 0.999))
        try:
            mr.cholesky([[1.0, 1.2], [1.2, 1.0]])
            raise AssertionError("aceptó matriz no definida positiva")
        except mr.ErrorRiesgo:
            pass
        ds = [mr.validar_distribucion({"VARIABLE": v, "DISTRIBUCION": "UNIFORME", "PARAMETROS": {"min": -0.1, "max": 0.1},
                                       "FUENTE": "T", "ESTADO": "ARTIFICIAL"}) for v in ("precio_venta", "alimento")]
        _, r, m, _ = _mc(n=150, dists=ds, corrs=[{"A": "precio_venta", "B": "alimento", "RHO": 0.9, "ESTADO": "ARTIFICIAL"}], aid="MC5")
        x, y = [s["SHOCK_precio_venta"] for s in m], [s["SHOCK_alimento"] for s in m]
        mx, my = sum(x) / len(x), sum(y) / len(y)
        cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
        rho = cov / (sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y)) ** 0.5
        assert rho > 0.75 and r["CORRELACIONES"] == "CORRELACIONES_DECLARADAS", rho

    # ------------------------------------------------------------------ OPTIMIZADOR (48)
    @test("OPT-01", "ningún ganador ni alternativa rankeada es hard-infeasible o físicamente no factible")
    def _():
        U, _ = universo_art()
        F = {f["id"]: f for f in U["fichas"]}
        for o, rk in U["ranking"].items():
            for aid, r in rk.items():
                if r.get("RANK"):
                    assert not F[aid]["HARD_INCUMPLE"] and F[aid]["F_FISICA"] != mo.NO_FACTIBLE, (o, aid)
        assert F["ART-INTEGRADA"]["HARD_INCUMPLE"] and not any(rk["ART-INTEGRADA"].get("RANK") for rk in U["ranking"].values())

    @test("OPT-02", "respeta el límite de capital (pico de fondos) y calcula el capital faltante")
    def _():
        U, inp = universo_art()
        X = inp["restriccion.CAPITAL_DISPONIBLE.valor"]
        for o, rk in U["ranking"].items():
            for f in U["fichas"]:
                if rk[f["id"]].get("RANK") and f["alt"]["tipo"] != mo.SQ:
                    assert f["ev"]["met"]["PICO_FONDOS"] <= X + 1e-6, (o, f["id"])
        filas, _ = mo.consulta_capital(U["fichas"], 10000.0, inp, ["MAX_VAN"])
        g = next(r for r in filas if r["ALTERNATIVA"] == "ART-PLANTA-GRANDE")
        assert g["CUMPLE_CAPITAL"] == "INCUMPLE" and _cerca(g["CAPITAL_FALTANTE"], g["CAPITAL_REQUERIDO"] - 10000.0)

    @test("OPT-03", "respeta la demanda: ventas ≤ demanda aunque sobre capacidad; consulta de demanda coherente")
    def _():
        U, inp = universo_art()
        g = next(f for f in U["fichas"] if f["id"] == "ART-PLANTA-GRANDE")
        assert g["ev"]["met"]["KG_VENDIDOS_ULT"] <= 150 * 12 + 1e-6, g["ev"]["met"]["KG_VENDIDOS_ULT"]
        assert g["ev"]["met"]["UTILIZACION"] <= 0.75 + 1e-9
        filas, concl = mo.consulta_demanda(U["E"], U["fichas"], inp["consulta.demanda_t_dia"], inp)
        assert concl["CONCLUSION"] and all(r.get("UTILIZACION") is None or r["UTILIZACION"] <= 1 + 1e-9 for r in filas)

    @test("OPT-04", "respeta el payback máximo HARD y la consulta informa (no aplica) los cambios necesarios")
    def _():
        U, inp = universo_art()
        inp2 = dict(inp, **{"restriccion.PAYBACK.valor": 2.0, "restriccion.PAYBACK.tipo": "HARD"})
        fs = [dict(f) for f in U["fichas"]]
        mo.reaplicar_restricciones(fs, mo.leer_restricciones(inp2), inp2)
        rk, dec, orden = mo.rankear(fs, "MAX_VAN", inp2)
        assert all(f["ev"]["met"]["PAYBACK"] <= 2.0 for f in orden if f["alt"]["tipo"] != mo.SQ)
        pb = mo.consulta_payback(U["E"], U["fichas"], 2.0, inp)
        no = [r for r in pb if r["CUMPLE"] == "NO"]
        assert no and all("SHOCK_NECESARIO_precio_venta" in r for r in no)
        base = next(f for f in U["fichas"] if f["id"] == no[0]["ALTERNATIVA"])["ev"]["met"]["PAYBACK"]
        assert _cerca(no[0]["PAYBACK_BASE_ANIOS"], base)

    @test("OPT-05", "puede devolver NINGUNA_CONFIGURACION_FACTIBLE (no elige la menos mala)")
    def _():
        U, inp = universo_art()
        inp2 = dict(inp, **{"restriccion.CAPITAL_DISPONIBLE.valor": 10.0})
        fs = [dict(f) for f in U["fichas"]]
        mo.reaplicar_restricciones(fs, mo.leer_restricciones(inp2), inp2)
        _, dec, orden = mo.rankear(fs, "MAX_VAN", inp2)
        assert dec["ESTADO"] == mo.NINGUNA and mo.SQ in dec["MEJOR"] and all(f["alt"]["tipo"] == mo.SQ for f in orden)

    @test("OPT-06", "NO_INVERTIR_AUN existe y gana MAX_VAN cuando toda inversión tiene VAN < 0 (no obliga a construir)")
    def _():
        assert any(a["id"] == mo.SQ for a in mo.caso_artificial())
        assert any(a["id"] == mo.SQ for a in mo.alternativas_reales(mr.leer_inputs()[0], "EVIDENCIA"))
        alts = [_alt("NEG1", ventas_anio=50.0), _alt("NEG2", ventas_anio=55.0), mr.alternativa_status_quo("CASO_ARTIFICIAL")]
        inp = mr.leer_inputs()[0]
        U = mo.correr_universo(alts, dict(inp, **{"sensibilidad.variables": [], "sens2d.pares": [], "quiebre.variables": [],
                                                   "robustez.variables": []}), "CASO_ARTIFICIAL")
        d = next(x for x in U["decisiones"] if x["OBJETIVO"] == "MAX_VAN")
        assert d["MEJOR"] == mo.SQ, d

    @test("OPT-07", "dominancia: estricta en al menos una dimensión; iguales no se dominan; dimensiones declaradas")
    def _():
        def fk(i, cap, van):
            return {"id": i, "alt": {"tipo": "PLANTA", "universo": "X"}, "COMPARABILIDAD": "TRUE",
                    "ev": {"met": {"FONDOS_INICIALES": cap, "VAN": van}}, "RIESGO_SCORE": None}
        fs = [fk("A", 100, 50), fk("B", 120, 40), fk("C", 100, 50), fk("D", 80, 10)]
        mo.dominancia(fs, {"dominancia.dimensiones": ["FONDOS_INICIALES:-", "VAN:+", "RIESGO_SCORE:-"]})
        d = {f["id"]: f["DOMINADA_POR"] for f in fs}
        assert d["B"] == ["A", "C"] and d["A"] == [] and d["C"] == [] and d["D"] == []
        assert fs[1]["DOM_DIMS"] == "FONDOS_INICIALES, VAN"

    @test("OPT-08", "frontera de Pareto correcta en un caso conocido")
    def _():
        def fk(i, cap, van):
            return {"id": i, "alt": {"tipo": "PLANTA", "universo": "CASO_ARTIFICIAL"}, "COMPARABILIDAD": "TRUE", "HARD_INCUMPLE": [],
                    "ev": {"met": {"FONDOS_INICIALES": cap, "VAN": van}}}
        fs = [fk("A", 10, 5), fk("B", 20, 9), fk("C", 15, 4), fk("D", 30, 9), fk("E", 5, 1)]
        p = mo.pareto(fs, {"pareto.pares": ["VAN:+×FONDOS_INICIALES:-"]})
        assert {r["ALTERNATIVA"] for r in p if r["EN_FRONTERA"]} == {"A", "B", "E"}

    @test("OPT-09", "segunda alternativa = segundo mejor valor del conjunto rankeable; diferencia correcta")
    def _():
        U, _ = universo_art()
        for d in U["decisiones"]:
            if d["ESTADO"] != "MEJOR_EN_ESCENARIO" or d.get("SEGUNDA") in (None, "—") or d["OBJETIVO"] in ("BALANCEADO",):
                continue
            rk = U["ranking"][d["OBJETIVO"]]
            orden = sorted((r["RANK"], a) for a, r in rk.items() if r.get("RANK"))
            assert orden[0][1] == d["MEJOR"] and orden[1][1] == d["SEGUNDA"], d["OBJETIVO"]
            assert _cerca(d["DIFERENCIA_VALOR"], d["VALOR_MEJOR"] - d["VALOR_SEGUNDA"])

    @test("OPT-10", "mismo input + misma semilla = mismo resultado")
    def _():
        _, inp = universo_art()
        dists, corrs = mo.dist_artificiales()
        r = []
        for _i in range(2):
            mo._COB.clear()
            U = mo.correr_universo(mo.caso_artificial(), dict(inp, **{"sensibilidad.variables": ["precio_venta"], "sens2d.pares": [],
                                   "quiebre.variables": [], "montecarlo.n": 20}), "CASO_ARTIFICIAL", mo.stress_artificiales(), dists, corrs)
            r.append((mo.filas_resultados(U), U["decisiones"], U["mc"]))
        strip = lambda t: mr.fmt(t)
        assert strip(r[0]) == strip(r[1])

    @test("OPT-11", "restricción SOFT penaliza sin eliminar; HARD elimina; SOFT sin penalización → error")
    def _():
        U, inp = universo_art()
        inp2 = dict(inp, **{"restriccion.PAYBACK.valor": 3.0, "restriccion.PAYBACK.tipo": "SOFT", "restriccion.PAYBACK.penalizacion": 0.5})
        fs = [dict(f) for f in U["fichas"]]
        mo.reaplicar_restricciones(fs, mo.leer_restricciones(inp2), inp2)
        rk, _, _ = mo.rankear(fs, "MAX_VAN", inp2)
        soft = [f for f in fs if any(r["TIPO"] == "SOFT" and r["ESTADO"] == "INCUMPLE" for r in f["R_CUMPLIMIENTO"])
                and not f["HARD_INCUMPLE"] and f["COMPARABILIDAD"] != "FALSE"]
        assert soft and all(rk[f["id"]]["RANK"] for f in soft) and all(f["SOFT_PENALIZACION"] > 0 for f in soft)
        inp3 = dict(inp2, **{"restriccion.PAYBACK.tipo": "HARD"})
        mo.reaplicar_restricciones(fs, mo.leer_restricciones(inp3), inp3)
        rk3, _, _ = mo.rankear(fs, "MAX_VAN", inp3)
        assert not any(rk3[f["id"]]["RANK"] for f in soft)
        try:
            mo.leer_restricciones({"restriccion.VAN.valor": 1.0, "restriccion.VAN.tipo": "SOFT"})
            raise AssertionError("SOFT sin penalización aceptada")
        except mr.ErrorRiesgo:
            pass

    @test("OPT-12", "sin pesos: BALANCEADO = PESOS_NO_DEFINIDOS y riesgo PENDIENTE (no 0); preset rotulado SUPUESTO")
    def _():
        inp = mr.leer_inputs()[0]
        assert mo.pesos_balanceado(inp) == (None, "PESOS_NO_DEFINIDOS")
        w, o = mo.pesos_balanceado(dict(inp, **{"balanceado.preset": "IGUALES"}))
        assert "SUPUESTO" in o and abs(sum(w.values()) - 1) < 1e-12
        fs = [{"id": "A", "alt": {"tipo": "PLANTA"}, "completa": True, "ev": {"met": {"PICO_FONDOS": 1.0, "VAN": 1.0,
               "DEMANDA_ASEGURADA_PCT": None}}, "ROB": {}, "fisico": {"gates": []}, "cobertura": None}]
        mo.score_riesgo(fs, inp, {})
        assert fs[0]["RIESGO_SCORE"] is None and "PENDIENTE" in fs[0]["RIESGO_NOTA"]

    @test("OPT-13", "objetivo distinto → criterio distinto (MIN_FONDOS ≠ MAX_VAN en el caso artificial)")
    def _():
        U, _ = universo_art()
        d = {x["OBJETIVO"]: x for x in U["decisiones"]}
        assert d["MAX_VAN"]["MEJOR"] != d["MIN_FONDOS_INICIALES"]["MEJOR"]
        assert d["MIN_FONDOS_INICIALES"]["MEJOR"] == "ART-ASSET-LIGHT"

    @test("OPT-14", "DECISION_NO_ROBUSTA si el ganador cambia entre escenarios o mejor/segunda son casi iguales")
    def _():
        U, _ = universo_art()
        d = next(x for x in U["decisiones"] if x["OBJETIVO"] == "MAX_VAN")
        assert mo.NO_ROB in d["ROBUSTEZ_DECISION"] and d["ESTABILIDAD_GANADOR"] < 1
        fs = [{"id": i, "alt": {"tipo": "PLANTA"}, "COMPARABILIDAD": "TRUE", "F_FISICA": mo.FACTIBLE, "HARD_INCUMPLE": [],
               "HARD_PENDIENTE": [], "SOFT_PENALIZACION": 0.0, "ev": {"met": {"VAN": v}}} for i, v in (("A", 100.0), ("B", 99.0))]
        _, dec, _ = mo.rankear(fs, "MAX_VAN", {"decision.tolerancia_equivalencia": 0.05})
        assert mo.NO_ROB in dec["ROBUSTEZ_DECISION"]

    @test("OPT-15", "espacio de decisiones: nada inválido se evalúa; C0 asset-light; rendering exige faena propia")
    def _():
        inp = mr.leer_inputs()[0]
        esp = mo.espacio_decisiones(inp)
        assert all(r["CLASIFICACION"] != "EN_MAPA_EVALUADA" or "INVALID" not in r["MOTIVO"] for r in esp)
        inval = [r for r in esp if r["CLASIFICACION"] == "INVALIDA_FISICAMENTE"]
        assert any(r.get("RENDERING") is True and r["FAENA"] == "facon" for r in inval)
        assert not any(r.get("RENDERING") is True and r["FAENA"] == "facon" for r in esp if r["CLASIFICACION"] != "INVALIDA_FISICAMENTE")
        alts = mo.alternativas_reales(inp, "EVIDENCIA")
        assert all(a["tipo"] == mo.ASSET_LIGHT for a in alts if a["configuracion"] == "C0")
        assert len(alts) == 5 * 4 + 19 + 5 * 3 + 1
        assert len({a["id"] for a in alts}) == len(alts)

    @test("OPT-16", "factibilidad física: sin dato → FACTIBILIDAD_PENDIENTE (nunca FACTIBLE); dato → FACTIBLE / NO_FACTIBLE")
    def _():
        a = next(x for x in mo.alternativas_reales(mr.leer_inputs()[0], "EVIDENCIA") if x["id"] == "C1|BASE|10000|ESCALA_UNICA")
        f = mo.factibilidad_fisica_real(a)
        assert f["ESTADO"] == mo.PEND and next(g for g in f["gates"] if g["GATE"] == "TERRENO")["ESTADO"] == mo.PEND
        a2 = dict(a, disponibilidad={"terreno_m2": 1000.0})
        assert next(g for g in mo.factibilidad_fisica_real(a2)["gates"] if g["GATE"] == "TERRENO")["ESTADO"] == mo.NO_FACTIBLE
        a3 = dict(a, disponibilidad={"terreno_m2": 1e9})
        assert next(g for g in mo.factibilidad_fisica_real(a3)["gates"] if g["GATE"] == "TERRENO")["ESTADO"] == mo.FACTIBLE

    @test("OPT-17", "factibilidades separadas (física, económica, financiera, comercial) y semáforo sin cortes económicos")
    def _():
        U, _ = universo_art()
        for f in U["fichas"]:
            for k in ("F_FISICA", "F_ECONOMICA", "F_FINANCIERA", "R_COMERCIAL", "SEMAFORO"):
                assert f.get(k), (f["id"], k)
        F = {f["id"]: f["SEMAFORO"] for f in U["fichas"]}
        assert F["ART-INCOMPLETA"] == "GRIS" and F["ART-INTEGRADA"] == "ROJO" and F["ART-PLANTA-GRANDE"] == "AMARILLO"

    @test("OPT-18", "USD 2 M nunca se asume: sin capital declarado no hay restricción ni consulta")
    def _():
        inp = mr.leer_inputs()[0]
        assert inp.get("restriccion.CAPITAL_DISPONIBLE.valor") is None and inp.get("consulta.capital_usd") is None
        assert not [r for r in mo.leer_restricciones(inp) if r["NOMBRE"] == "CAPITAL_DISPONIBLE"]
        filas, _ = mo.consulta_capital([], None, inp, ["MAX_VAN"])
        assert filas[0]["ESTADO"] == "SIN_CONSULTA"

    @test("OPT-19", "robustez PENDIENTE sin escenarios suficientes")
    def _():
        a = _alt("R19")
        fs = [mo.ficha(mr.Evaluador(), a, {}, [])]
        mo.finalizar_fichas(fs, {})
        mo.robustez(mr.Evaluador(), fs, {}, [], [])
        assert fs[0]["ROBUSTEZ"] is None and fs[0]["ROB"]["ESTADO"] == "PENDIENTE"

    @test("OPT-20", "las alternativas reales se evalúan con el motor sin errores (sin doble conteo de subproductos)")
    def _():
        E = mr.Evaluador()
        for a in mo.alternativas_reales(mr.leer_inputs()[0], "ESCENARIO", mo.leer_escenario()):
            ev = E.evaluar(a)
            assert ev["estado"] in ("OK", "STATUS_QUO"), (a["id"], ev["estado"], ev["motivo"][:200])

    @test("OPT-21", "fondos iniciales = CAPEX + CT inicial + otros; pico de fondos ≥ CAPEX (capital ≠ CAPEX)")
    def _():
        a = _alt("O21", dias_cobro=30.0, convencion="MENSUAL")
        ev = mr.Evaluador().evaluar(a)
        m, r = ev["met"], ev["res"]
        assert r["CT_INICIAL"] > 0 and _cerca(m["FONDOS_INICIALES"], r["CAPEX_INICIAL"] + r["CT_INICIAL"] + r["OTROS_REQUERIMIENTOS_CAJA"])
        assert m["FONDOS_INICIALES"] > m["CAPEX"] and m["PICO_FONDOS"] >= m["CAPEX"] + 1e-9

    # ------------------------------------------------------------------ COMPARABILIDAD (49)
    def _fc(**cambios):
        firma = {"UNIVERSO": "X", "HORIZONTE": 10, "MODELO_MONETARIO": "REAL", "BASE_TASA": "REAL", "CONVENCION": "MENSUAL",
                 "TIPO_TASA": "EFECTIVA_ANUAL", "TASA": 0.1, "MONEDA": "USD", "BASE_FLUJO": "AFTER_TAX", "PRODUCTO": "B", "FISCAL": "AFTER_TAX"}
        f2 = dict(firma, **cambios)
        return {"alt": {"tipo": "PLANTA"}, "completa": True, "firma": f2, "cobertura": 0.0, "faltantes_cortos": ""}, firma

    @test("COMP-01", "real vs nominal incompatible y horizontes distintos → COMPARABILIDAD FALSE")
    def _():
        for c in ({"MODELO_MONETARIO": "NOMINAL", "BASE_TASA": "NOMINAL"}, {"HORIZONTE": 15}, {"FISCAL": "PRE_TAX"},
                  {"PRODUCTO": "A"}, {"UNIVERSO": "Y"}):
            f, ref = _fc(**c)
            assert mo.comparabilidad(f, ref)[0] == "FALSE", c
        f, ref = _fc()
        assert mo.comparabilidad(f, ref) == ("TRUE", "")
        assert mo.comparabilidad(f, ref, cob_max=0.5)[0] == "PARCIAL"

    @test("COMP-02", "una configuración incompleta nunca vence a una completa (sus costos faltantes no son 0)")
    def _():
        U, _ = universo_art()
        f = next(x for x in U["fichas"] if x["id"] == "ART-INCOMPLETA")
        assert f["ev"]["met"]["VAN"] is None and f["COMPARABILIDAD"] == "FALSE"
        assert not any(rk["ART-INCOMPLETA"].get("RANK") for rk in U["ranking"].values())

    @test("COMP-03", "E4 / faltante no se vuelve costo 0: C1 en evidencia sin CAPEX, fondos ni VAN; métrica None ≠ 0")
    def _():
        a = next(x for x in mo.alternativas_reales(mr.leer_inputs()[0], "EVIDENCIA") if x["id"] == "C1|BASE|10000|ESCALA_UNICA")
        ev = mr.Evaluador().evaluar(a)
        for k in ("CAPEX", "FONDOS_INICIALES", "VAN", "EBITDA", "PICO_FONDOS"):
            assert ev["met"][k] is None and mr.valor_metrica(ev, k) is None, k
        assert ev["res"]["PUBLICABLE_VAN"] is False
        assert mo.cobertura_evidencia(a)[0] < 1

    @test("COMP-04", "un resultado de escenario nunca se presenta como evidencia; universos no se mezclan")
    def _():
        U, _ = universo_art()
        assert all(r["ETIQUETA_EVIDENCIA"] == mr.ETIQ_ART for r in mo.filas_resultados(U))
        assert mo.etiqueta("ESCENARIO") == mr.ETIQ_SIM
        alts = mo.caso_artificial()[:1] + [mr.alternativa_status_quo("ESCENARIO")]
        try:
            mo.correr_universo(alts, mr.leer_inputs()[0], "CASO_ARTIFICIAL")
            raise AssertionError("mezcló universos")
        except mr.ErrorRiesgo:
            pass

    @test("COMP-05", "universo EVIDENCIA: OPTIMIZACION_REAL_NO_DISPONIBLE y prioridades derivadas del motor con DPV existentes")
    def _():
        inp = mr.leer_inputs()[0]
        inp = dict(inp, **{"espacio.configuraciones": ["C0", "C1"], "espacio.escalas": [10000], "espacio.trayectorias": [],
                           "espacio.incluir_variantes": False})
        U = mo.correr_universo(mo.alternativas_reales(inp, "EVIDENCIA"), inp, "EVIDENCIA")
        assert all(d["ESTADO"] == mr.OPT_REAL_ND for d in U["decisiones"])
        pr = mo.prioridad_evidencia(U["E"], U["fichas"])
        assert pr and pr[0]["INDICADORES_BLOQUEADOS"] >= pr[-1]["INDICADORES_BLOQUEADOS"]
        assert any(r["ITEM"] == "OPEX:FAENA_FACON" for r in pr) and any(r["ITEM"].startswith("PRECIOS") for r in pr)
        assert all(r["DPV_EXISTEN"] in ("SÍ", "SIN_DPV") for r in pr), [r for r in pr if r["DPV_EXISTEN"] not in ("SÍ", "SIN_DPV")][:2]
        q = mo.que_hacer_ahora(pr, [])
        assert q and len({x["QUE_HACER_AHORA"] for x in q}) == len(q)

    # ------------------------------------------------------------------ PUNTOS DE QUIEBRE (50)
    @test("QUI-01", "precio break-even (VAN = 0) = solución manual (60 + 26,3797) ÷ 100")
    def _():
        q = mr.punto_quiebre(mr.Evaluador(), _alt("Q1"), "precio_venta")
        assert q["ESTADO"] == "ENCONTRADO" and _cerca(q["FACTOR_SOBRE_BASE"], (60 + E_STAR) / 100), q

    @test("QUI-02", "utilización break-even = (40 + 26,3797) ÷ (100 − 20) con OPEX fijo 40 y variable 20")
    def _():
        q = mr.punto_quiebre(mr.Evaluador(), _alt("Q2", opex_fijo=40.0, opex_var=20.0), "utilizacion")
        assert _cerca(q["FACTOR_SOBRE_BASE"], (40 + E_STAR) / 80), q

    @test("QUI-03", "CAPEX máximo = 40 × anualidad (pre-tax)")
    def _():
        q = mr.punto_quiebre(mr.Evaluador(), _alt("Q3"), "capex")
        assert _cerca(q["FACTOR_SOBRE_BASE"] * 100, 40 * ANUALIDAD), q

    @test("QUI-04", "alimento máximo = (60 − 26,3797) ÷ 20; FCR máximo idéntico (mismos rubros)")
    def _():
        E = mr.Evaluador()
        a = _alt("Q4", opex_fijo=40.0, opex_var=20.0)
        q = mr.punto_quiebre(E, a, "alimento")
        f = mr.punto_quiebre(E, a, "fcr")
        assert _cerca(q["FACTOR_SOBRE_BASE"], (60 - E_STAR) / 20) and _cerca(f["FACTOR_SOBRE_BASE"], q["FACTOR_SOBRE_BASE"]), (q, f)

    @test("QUI-05", "días de cobro máximos y tasa de descuento máxima (= TIR del motor)")
    def _():
        E = mr.Evaluador()
        a = _alt("Q5")
        q = mr.punto_quiebre(E, a, "dias_cobro")
        van0 = -100 + 40 * ANUALIDAD
        assert _cerca(q["SHOCK_QUIEBRE"], van0 * 1.1 / ((100 / 12) / mf.DIAS_MES)), q
        t = mr.punto_quiebre(E, a, "tasa_descuento")
        assert _cerca(t["FACTOR_SOBRE_BASE"] * 0.10, E.evaluar(a, tir=True)["met"]["TIR"], 1e-4)

    @test("QUI-06", "mortalidad máxima = solución manual con pollito como único variable")
    def _():
        a = _alt("Q6", opex_fijo=40.0, opex_var=20.0, base_valores={"mortalidad": 0.05})
        P = a["construir"]()[0]
        P["etapas"][0]["opex_rubros"][1]["grupo_proveedor"] = "pollitos"
        a["construir"] = lambda P=P: (copy.deepcopy(P), None)
        q = mr.punto_quiebre(mr.Evaluador(), a, "mortalidad")
        m1 = 1 - 0.95 / ((60 - E_STAR) / 20)
        assert _cerca(q["SHOCK_QUIEBRE"], m1 / 0.05 - 1), (q, m1 / 0.05 - 1)
        assert _cerca(q["VALOR_ABSOLUTO_QUIEBRE"], m1)

    @test("QUI-07", "NO_ENCONTRADO_EN_RANGO ≠ NO_CALCULABLE")
    def _():
        E = mr.Evaluador()
        q = mr.punto_quiebre(E, _alt("Q7"), "precio_venta", rango=(0.0, 0.5))
        assert q["ESTADO"] == mr.NO_ENC and q.get("SHOCK_QUIEBRE") is None, q
        q2 = mr.punto_quiebre(E, _alt("Q7b"), "precio_venta", metrica="DSCR", objetivo=1.2)
        assert q2["ESTADO"] == mr.NO_CALC
        q3 = mr.punto_quiebre(E, _alt("Q7c"), "mortalidad")
        assert q3["ESTADO"] == mr.NO_CALC

    fallas = []
    for tid, desc, fn in T:
        try:
            with redirect_stdout(io.StringIO()):
                fn()
        except Exception as e:                          # noqa: BLE001
            fallas.append((tid, desc, f"{type(e).__name__}: {e}"[:400]))
    if verbose:
        for tid, desc, _ in T:
            print(f"  [{'FALLA' if any(f[0] == tid for f in fallas) else 'OK'}] {tid} {desc}")
        print(f"Tests: {len(T) - len(fallas)}/{len(T)} OK")
    return fallas, len(T)


# ---------------------------------------------------------------------------------------------
# MUTACIONES (51): cada error sembrado debe ser detectado por al menos un test
# ---------------------------------------------------------------------------------------------
MUTACIONES = {
    "R01": "quitar el límite de capital", "R02": "permitir ventas > demanda (motor M02)", "R03": "convertir faltante en cero",
    "R04": "elegir siempre máximo VAN ignorando el objetivo/riesgo", "R05": "excluir NO_INVERTIR_AUN",
    "R06": "duplicar subproductos (esqueleto + CMS; motor M11)", "R07": "ignorar el CAPEX en fondos", "R08": "ignorar el capital de trabajo",
    "R09": "el shock se filtra a otra variable", "R10": "tornado por impacto con signo", "R11": "Monte Carlo sin semilla / sin caché",
    "R12": "rankear sin comparabilidad", "R13": "costos faltantes completados con 0", "R14": "restricción HARD tratada como SOFT",
    "R15": "dominancia no estricta", "R16": "punto de quiebre devuelve el borde del rango", "R17": "aceptar Monte Carlo/evidencia sin respaldo",
    "R18": "probabilidad numérica para niveles cualitativos", "R19": "la mitigación borra el riesgo inherente",
}
MOTOR = {"R02": "M02", "R06": "M11"}


def prueba_mutaciones():
    det = 0
    for m, desc in MUTACIONES.items():
        mr._MUT = {m} if m not in MOTOR else set()
        mf._MUT = {MOTOR[m]} if m in MOTOR else set()
        mf._CACHE.clear()
        mo._COB.clear()
        _U.clear()
        try:
            with redirect_stdout(io.StringIO()):
                fallas, _ = ejecutar_tests(verbose=False)
        finally:
            mr._MUT, mf._MUT = set(), set()
            mf._CACHE.clear()
            mo._COB.clear()
            _U.clear()
        ok = bool(fallas)
        det += ok
        print(f"  [{'DETECTADA' if ok else 'NO DETECTADA'}] {m} {desc}" + (f" → {fallas[0][0]}" if ok else ""))
    print(f"Mutaciones detectadas: {det}/{len(MUTACIONES)}")
    return det == len(MUTACIONES)
