"""Servicios de la app: cada función recibe un escenario de la app (o nada) y devuelve un dict JSON-serializable.

No hay fórmulas económicas aquí. Todo número sale de:
  mf.construir_entrada / mf.simular / mf.resultados / mf.agregar / mf.completitud / mf.estado_bloques   (21)
  mr.Evaluador / sensibilidad_oneway / tornado / sensibilidad_2d / correr_stress / punto_quiebre / monte_carlo (22)
  mopt.correr_universo / consultas / limitacion_principal / que_hacer_ahora / pareto                     (22)
La app solo traduce el escenario, elige qué pedir y da formato (etiquetas, textos, faltantes).

Caché (#45):
  * un Evaluador del motor POR ALTERNATIVA, indexado por la huella de lo que define esa alternativa (comun + su entrada
    en por_alternativa + plantilla + valores base + universo). Cambiar un input invalida solo las alternativas cuya
    huella cambia; nunca se sirve el resultado de otro escenario (la huella incluye todo el contenido).
  * un caché de respuestas por (operación, huella del escenario, parámetros).
"""
import collections
import copy
import io
import json
import math
from contextlib import redirect_stdout

from . import escenario as ES
from . import motor as M
from . import presentacion as TX

mf, mr, mopt = M.mf, M.mr, M.mopt
SQ = mr.STATUS_QUO

_EVALS = collections.OrderedDict()      # huella de alternativa → mr.Evaluador (de una sola alternativa)
_RESP = collections.OrderedDict()       # (operación, huella, params) → respuesta
_CTX = collections.OrderedDict()        # huella del escenario → contexto
MAX_EVALS, MAX_RESP, MAX_CTX = 400, 64, 16
ESTADISTICAS = {"evaluadores_creados": 0, "respuestas_cacheadas": 0, "respuestas_calculadas": 0}


def _lru_get(d, k):
    if k in d:
        d.move_to_end(k)
        return d[k]
    return None


def _lru_put(d, k, v, n):
    d[k] = v
    d.move_to_end(k)
    while len(d) > n:
        d.popitem(last=False)


def limpiar_cache():
    _EVALS.clear()
    _RESP.clear()
    _CTX.clear()


def _limpio(x):
    """JSON seguro: NaN/inf → None (nunca 0), sets → listas, tuplas → listas."""
    if isinstance(x, float):
        return None if (math.isnan(x) or math.isinf(x)) else x
    if isinstance(x, dict):
        return {str(k): _limpio(v) for k, v in x.items() if not callable(v)}
    if isinstance(x, (list, tuple, set)):
        return [_limpio(v) for v in x]
    if callable(x):
        return None
    return x


# ---------------------------------------------------------------------------------------------
# EVALUADOR COMPUESTO (un Evaluador del motor por alternativa; misma interfaz que mr.Evaluador)
# ---------------------------------------------------------------------------------------------
class EvaluadorEscenario:
    def __init__(self, huellas):
        self.huellas = huellas
        self._n0 = {}

    def _e(self, alt):
        h = self.huellas.get(alt["id"]) or ES.huella({"sq": alt["id"], "u": alt["universo"]})
        e = _lru_get(_EVALS, h)
        if e is None:
            e = mr.Evaluador()
            ESTADISTICAS["evaluadores_creados"] += 1
            _lru_put(_EVALS, h, e, MAX_EVALS)
        self._n0.setdefault(h, (e.n_eval, e.n_hit, e))
        return e

    def base(self, alt):
        return self._e(alt).base(alt)

    def evaluar(self, alt, shocks=None, tir=False):
        return self._e(alt).evaluar(alt, shocks, tir)

    @property
    def n_eval(self):
        return sum(e.n_eval - a for a, _, e in self._n0.values())

    @property
    def n_hit(self):
        return sum(e.n_hit - b for _, b, e in self._n0.values())


class Contexto:
    def __init__(self, esc):
        self.esc = ES.validar(esc)
        self.huella = ES.huella(ES.parte_motor(self.esc))
        self.ent = ES.a_motor(self.esc)
        self.alts = ES.alternativas(self.ent)
        self.por_id = {a["id"]: a for a in self.alts}
        comun = self.ent["escenario"]["comun"]
        h = {}
        for a in self.alts:
            if a["tipo"] == SQ:
                continue
            aid = ES.id_motor(a["id"])
            h[a["id"]] = ES.huella({"u": a["universo"], "id": a["id"], "comun": comun, "plantilla": self.ent["escenario"]["plantilla"],
                                    "alt": self.ent["escenario"]["por_alternativa"].get(aid), "bv": a.get("base_valores")})
        self.E = EvaluadorEscenario(h)

    def alt(self, aid):
        if aid not in self.por_id:
            raise ES.ErrorEscenario(f"La alternativa {aid} no existe en este escenario (revise arquitectura y escala).")
        return self.por_id[aid]


def contexto(esc):
    esc = ES.validar(esc)
    h = ES.huella(ES.parte_motor(esc))
    c = _lru_get(_CTX, h)
    if c is None:
        c = Contexto(esc)
        _lru_put(_CTX, h, c, MAX_CTX)
    return c


def _cache(op, ctx, params, fn):
    k = (op, ctx.huella, json.dumps(params, sort_keys=True, default=str))
    r = _lru_get(_RESP, k)
    if r is not None:
        ESTADISTICAS["respuestas_cacheadas"] += 1
        return copy.deepcopy(r)
    r = _limpio(fn())
    ESTADISTICAS["respuestas_calculadas"] += 1
    _lru_put(_RESP, k, r, MAX_RESP)
    return copy.deepcopy(r)


# ---------------------------------------------------------------------------------------------
# FICHAS → JSON
# ---------------------------------------------------------------------------------------------
CAMPOS_RES = ("CAPEX_INICIAL", "CAPEX_EXPANSION", "CAPEX_REPOSICION", "CT_INICIAL", "CT_MAXIMO", "OTROS_REQUERIMIENTOS_CAJA",
              "FONDOS_INICIALES", "PICO_REQUERIMIENTO_FONDOS", "MES_VALLE_CAJA", "VENTA_BRUTA_ULTIMO_ANIO",
              "INGRESO_NETO_ULTIMO_ANIO", "EBITDA_ULTIMO_ANIO", "MARGEN_EBITDA_ULTIMO_ANIO", "VAN", "TIR", "TIR_MENSUAL",
              "TIR_ESTADO", "MIRR", "PAYBACK_SIMPLE_MESES", "PAYBACK_SIMPLE_ANIOS", "PAYBACK_SIMPLE_ESTADO",
              "PAYBACK_DESCONTADO_ANIOS", "PAYBACK_DESCONTADO_ESTADO", "DSCR_MINIMO", "VAN_ACCIONISTA", "TIR_ACCIONISTA",
              "TIR_ACCIONISTA_ESTADO", "APORTES_TOTALES", "DEUDA_TOMADA", "CAJA_MINIMA_LEDGER", "U_EFECTIVA_ULTIMO_ANIO",
              "U_COMERCIAL_REQUERIDA_ULTIMO_ANIO", "U_TECNICA_ULTIMO_ANIO", "BE_UTILIZACION_EBITDA",
              "BE_PRECIO_MEDIO_USD_KG_EBITDA", "BE_ESTADO", "ETIQUETA", "TRAZABILIDAD", "MODO", "HORIZONTE_ANIOS",
              "TASA_DESCUENTO_ANUAL_EFECTIVA", "CONVENCION_DESCUENTO", "BASE_FLUJO", "BASE_FLUJO_ACCIONISTA",
              "OVERRIDES_SIMULACION", "UMBRAL_EVIDENCIA", "FALTANTES") + tuple(f for fl in mf.FLAGS for f in (fl, fl + "_MOTIVO"))


def faltantes_por_bloque(txt):
    out = {}
    for parte in (txt or "").split(" || "):
        if ":" not in parte:
            continue
        b, resto = parte.split(":", 1)
        out[b.strip()] = [x.strip() for x in resto.split("; ") if x.strip()]
    return out


def ficha_json(f, U=None):
    a = f["alt"]
    ev = f["ev"]
    res = ev.get("res") or {}
    out = {"id": a["id"], "tipo": a["tipo"], "universo": a["universo"], "configuracion": a["configuracion"],
           "variante": a.get("variante"), "escalas": list(a.get("escalas") or []), "trayectoria": a.get("trayectoria"),
           "etiqueta_universo": mopt.etiqueta(a["universo"]), "estado_evaluacion": ev["estado"], "motivo_evaluacion": ev["motivo"],
           "metricas": {k: v for k, v in ev["met"].items()}, "resultados": {k: res.get(k) for k in CAMPOS_RES if k in res},
           "faltantes": faltantes_por_bloque(res.get("FALTANTES") if res else ""),
           "completa": f["completa"], "comparabilidad": f.get("COMPARABILIDAD"), "comparabilidad_motivo": f.get("COMPARABILIDAD_MOTIVO"),
           "semaforo": f.get("SEMAFORO"), "factibilidad_fisica": f.get("F_FISICA"), "factibilidad_economica": f.get("F_ECONOMICA"),
           "factibilidad_financiera": f.get("F_FINANCIERA"), "respaldo_comercial": f.get("R_COMERCIAL"),
           "cobertura_evidencia": f.get("cobertura"), "cobertura_nota": f.get("cobertura_nota"),
           "robustez": f.get("ROBUSTEZ"), "robustez_detalle": f.get("ROB"), "score_riesgo": f.get("SCORE_ORDINAL_RIESGO"),
           "riesgo_componentes": f.get("RIESGO_COMP"), "riesgo_nota": f.get("RIESGO_NOTA"),
           "restricciones": f.get("R_CUMPLIMIENTO"), "hard_incumple": f.get("HARD_INCUMPLE"), "hard_pendiente": f.get("HARD_PENDIENTE"),
           "gates": (f.get("fisico") or {}).get("gates"), "dominada_por": f.get("DOMINADA_POR"), "dominancia_estado": f.get("DOM_ESTADO"),
           "limitacion_principal": mopt.limitacion_principal(f) if "R_CUMPLIMIENTO" in f else None,
           "descripcion": a.get("descripcion", "")}
    if a["tipo"] == SQ:
        out["metricas"] = {k: None for k in out["metricas"]}
    if U is not None:
        out["ranking"] = {o: (U["ranking"].get(o) or {}).get(a["id"]) for o in U["ranking"]}
    return out


def _decision_json(d):
    return {k: v for k, v in d.items()}


def _alertas(ctx, fichas=None, extra=None):
    """Alertas visibles (#37). Nunca se dejan solo en consola."""
    al = []
    if ctx.esc.get("solo_demostracion"):
        al.append(TX.alerta("SOLO_DEMOSTRACION", "Datos completamente ficticios (DEMO_ARTIFICIAL). No es información del proyecto."))
    al.append(TX.alerta("SIMULACION", "Todo resultado de este escenario es una SIMULACIÓN HIPOTÉTICA (no validada)."))
    for a in ctx.ent["avisos"]:
        al.append(TX.alerta("DATO_PENDIENTE", a))
    for d in ctx.ent["costos_unitarios"]:
        if d["ESTADO"] not in ("APLICADO",):
            al.append(TX.alerta("NO_APLICA" if d["ESTADO"].startswith("NO_APLICA") else "DATO_PENDIENTE",
                                f"Costo unitario {d.get('CONCEPTO', '')} en {d['ALTERNATIVA']}: {d['ESTADO']} — {d['DETALLE']}"))
    for f in fichas or []:
        if f["alt"]["tipo"] == SQ:
            continue
        ev = f["ev"]
        if ev["estado"] == "ERROR_CONSTRUCCION":
            cod = "OVERRIDE_INCOMPATIBLE" if mf.OVERRIDE_INCOMPATIBLE in ev["motivo"] else "NO_CALCULADA"
            al.append(TX.alerta(cod, f"{f['alt']['id']}: {ev['motivo']}"))
        res = ev.get("res") or {}
        if res.get("ETIQUETA") == mf.ETIQUETA_OVERRIDE_TOTAL:
            al.append(TX.alerta("OVERRIDE_TOTAL", f"{f['alt']['id']}: {res.get('TRAZABILIDAD')}"))
        if mf.NO_CALC_FISCAL in (res.get("FALTANTES") or ""):
            al.append(TX.alerta("REGLA_FISCAL_PENDIENTE", f"{f['alt']['id']}: IIBB con alícuota > 0 sin regla de base por mercado."))
        if f.get("COMPARABILIDAD") == "FALSE" and f["completa"]:
            al.append(TX.alerta("NO_COMPARABLE", f"{f['alt']['id']}: {f.get('COMPARABILIDAD_MOTIVO')}"))
        if f.get("cobertura") is not None and f["cobertura"] < 0.5 and f["completa"]:
            al.append(TX.alerta("EVIDENCIA_BAJA", f"{f['alt']['id']}: cobertura de evidencia {f['cobertura']:.0%}."))
    bajas = [a for a in al if a["codigo"] == "EVIDENCIA_BAJA"]
    if len(bajas) > 2:
        al = [a for a in al if a["codigo"] != "EVIDENCIA_BAJA"]
        al.append(TX.alerta("EVIDENCIA_BAJA", f"{len(bajas)} alternativas con datos completos tienen cobertura de evidencia < 50 % "
                                              "(sus números se apoyan en datos de escenario)."))
    for x in extra or []:
        al.append(x)
    vistos, out = set(), []
    for a in al:
        k = (a["codigo"], a["texto"])
        if k not in vistos:
            vistos.add(k)
            out.append(a)
    return out


# ---------------------------------------------------------------------------------------------
# OPTIMIZAR / COMPARAR
# ---------------------------------------------------------------------------------------------
def _correr(ctx, ids=None, con_consultas=True):
    alts = ctx.alts if ids is None else [ctx.alt(i) for i in ids] + [a for a in ctx.alts if a["tipo"] == SQ]
    with redirect_stdout(io.StringIO()):
        U = mopt.correr_universo(alts, ctx.ent["inp"], ctx.ent["universo"], ctx.ent["stresses"], [], [], E=ctx.E)
        cons = mopt.consultas(U, ctx.ent["inp"]) if con_consultas else {}
    return U, cons


def optimizar(esc):
    ctx = contexto(esc)

    def calc():
        U, cons = _correr(ctx)
        obj = ctx.ent["objetivo_principal"] or "MAX_VAN"
        decs = {d["OBJETIVO"]: _decision_json(d) for d in U["decisiones"]}
        for d in decs.values():
            d["ESTADO_APP"] = ("MEJOR_EN_ESCENARIO" if d.get("ESTADO") == "MEJOR_EN_ESCENARIO" and d.get("DECISION_ESCENARIO") != SQ
                               else TX.texto_no_invertir(d, None)["estado_app"])
        fichas = [ficha_json(f, U) for f in U["fichas"]]
        principal = decs.get(obj)
        n_comp = sum(1 for f in U["fichas"] if f["completa"] and f["alt"]["tipo"] != SQ)
        prio = U.get("prio_esc") or []
        return {"universo": ctx.ent["universo"], "etiqueta": mopt.etiqueta(ctx.ent["universo"]),
                "solo_demostracion": ctx.ent["solo_demostracion"], "objetivo_principal": obj,
                "objetivo_texto": TX.texto_objetivo(obj), "decision_principal": principal, "decisiones": decs,
                "explicacion": TX.explicar_decision(principal, {f["id"]: f for f in fichas}) if principal else None,
                "fichas": fichas, "n_alternativas": len(fichas), "n_completas": n_comp,
                "pareto": U.get("pareto"), "dominancia_dimensiones": U.get("dominancia_dims"),
                "consultas": cons, "prioridad_escenario": prio,
                "que_hacer": mopt.que_hacer_ahora([], prio, 10),
                "restricciones_declaradas": U["restr"], "stress_usados": [s["ID_STRESS"] for s in ctx.ent["stresses"]],
                "evaluaciones_motor": ctx.E.n_eval, "aciertos_cache_motor": ctx.E.n_hit,
                "alertas": _alertas(ctx, U["fichas"]), "costos_unitarios": ctx.ent["costos_unitarios"]}
    return _cache("optimizar", ctx, {}, calc)


def comparar(esc, ids):
    ids = [i for i in ids if i != SQ]
    if not 2 <= len(ids) <= 5:
        raise ES.ErrorEscenario("Seleccione entre 2 y 5 alternativas para comparar.")
    ctx = contexto(esc)

    def calc():
        U, _ = _correr(ctx, ids, con_consultas=False)
        fs = [f for f in U["fichas"] if f["alt"]["tipo"] != SQ]
        fichas = [ficha_json(f, U) for f in fs]
        no_comp = [f for f in fichas if f["comparabilidad"] == "FALSE"]
        comparable = len(fichas) - len(no_comp) >= 2
        decs = {d["OBJETIVO"]: _decision_json(d) for d in U["decisiones"]}
        return {"universo": ctx.ent["universo"], "etiqueta": mopt.etiqueta(ctx.ent["universo"]),
                "solo_demostracion": ctx.ent["solo_demostracion"], "fichas": fichas, "comparable": comparable,
                "no_comparables": [{"id": f["id"], "motivo": f["comparabilidad_motivo"]} for f in no_comp],
                "explicacion_comparabilidad": TX.texto_comparabilidad(comparable, no_comp),
                "decisiones": decs if comparable else {}, "pareto": U.get("pareto") if comparable else [],
                "alertas": _alertas(ctx, U["fichas"])}
    return _cache("comparar", ctx, {"ids": sorted(ids)}, calc)


# ---------------------------------------------------------------------------------------------
# SIMULAR (una alternativa en detalle, o la mejor del escenario)
# ---------------------------------------------------------------------------------------------
SERIES_GRAFICO = {   # serie del motor → bandera de publicabilidad que la habilita
    "venta_bruta": "PUBLICABLE_INGRESOS", "ingreso_neto": "PUBLICABLE_INGRESOS", "opex_total": "PUBLICABLE_EBITDA",
    "ebitda": "PUBLICABLE_EBITDA", "capex_total": "PUBLICABLE_FLUJO", "delta_ct": "PUBLICABLE_FLUJO",
    "ct": "PUBLICABLE_FLUJO", "fcff": "PUBLICABLE_FLUJO", "fcff_pre": "PUBLICABLE_FLUJO",
    "u_efectiva": None, "u_tecnica": None, "u_comercial": None, "aves_faenadas": None, "kg_vendidos": None,
    "caja": "PUBLICABLE_FLUJO_ACCIONISTA", "servicio_deuda": "PUBLICABLE_FLUJO_ACCIONISTA",
    "cfads": "PUBLICABLE_FLUJO_ACCIONISTA", "deuda_saldo_fin": "PUBLICABLE_FLUJO_ACCIONISTA"}


def series_anuales(R, res):
    """Series anuales con mf.periodos_reporte (meses_detalle = 0) y mf.agregar (flujos = suma; saldos = fin de período)."""
    if not R or R.get("N", 0) == 0:
        return None
    P = dict(R["P"], meses_detalle=0)
    per = mf.periodos_reporte(P, R["N"], R["inicio_op"], R["series"]["fase"])
    R2 = dict(R, periodos=per)
    out = {"periodos": [p["PERIODO"] for p in per], "fases": [p["FASE"] for p in per],
           "fechas": [p["FECHA_INICIO"] for p in per], "series": {}, "no_publicadas": {}}
    for s, flag in SERIES_GRAFICO.items():
        if flag and not res.get(flag):
            out["series"][s] = None
            out["no_publicadas"][s] = res.get(flag + "_MOTIVO")
            continue
        out["series"][s] = mf.agregar(R2, s) if R["series"].get(s) is not None else None
    return out


def detalle_alternativa(ctx, aid):
    alt = ctx.alt(aid)
    b = ctx.E.base(alt)
    if b[0] == "ERROR":
        cod = "OVERRIDE_INCOMPATIBLE" if mf.OVERRIDE_INCOMPATIBLE in b[1] else "ERROR_CONSTRUCCION"
        return {"error_construccion": {"codigo": cod, "mensaje": TX.mensaje_error_motor(b[1]), "detalle": b[1]}}
    P0, T = b
    P = copy.deepcopy(P0)
    R = mf.simular(P)
    res = mf.resultados(R, calcular_tir=True)
    estados = mf.estado_bloques(P, R["faltantes"])
    traza = [dict(f) for f in T.filas]
    return {"resultados": {k: res.get(k) for k in CAMPOS_RES if k in res},
            "faltantes": {k: v for k, v in R["faltantes"].items() if v},
            "estado_bloques": estados, "cobertura_bloques": mf.cobertura_bloques(estados),
            "completitud": mf.completitud(P, R, T), "series": series_anuales(R, res), "traza": traza,
            "notas_motor": R.get("notas", []), "productos_kg_ave": {p: x["kg_ave"] for p, x in (P.get("productos") or {}).items()},
            "dias_operativos": [e["dias_operativos_anio"] for e in P["etapas"]],
            "demanda_lineas": [{k: v for k, v in l.items()} for l in (P.get("demanda") or [])]}


def id_simple(ctx):
    """Alternativa pedida en el modo simple (configuración + escala manuales) o None (AUTO)."""
    s = ctx.esc["simple"]
    a, e = s["arquitectura"], s["escala"]
    if a.get("modo") != "MANUAL" or e.get("modo") != "VALOR":
        return None
    aid = mopt.id_alt(a["configuracion"], a.get("variante"), (int(e["valor"]),), "ESCALA_UNICA")
    return (ES.PREFIJO_DEMO + aid) if ctx.ent["universo"] == "ARTIFICIAL_TEST" else aid


def simular(esc, aid=None):
    ctx = contexto(esc)

    def calc():
        elegida = aid or id_simple(ctx)
        modo = "ALTERNATIVA_ELEGIDA" if elegida else "AUTOMATICO"
        opt = None
        if not elegida:
            opt = optimizar(ctx.esc)
            d = opt["decision_principal"] or {}
            if d.get("ESTADO") == "MEJOR_EN_ESCENARIO" and d.get("DECISION_ESCENARIO") != SQ:
                elegida = d["MEJOR"]
            else:
                ni = TX.texto_no_invertir(d, opt["fichas"])
                return {"modo": modo, "resultado": "SIN_INVERSION" if ni["estado_app"] == "NO_INVERTIR_AUN" else ni["estado_app"],
                        "decision": d, "no_invertir": ni,
                        "optimizacion": _resumen_opt(opt), "alertas": opt["alertas"], "universo": ctx.ent["universo"],
                        "etiqueta": opt["etiqueta"], "solo_demostracion": ctx.ent["solo_demostracion"],
                        "disclaimer": TX.DISCLAIMER}
        U, _ = _correr(ctx, [elegida], con_consultas=False)
        f = next(x for x in U["fichas"] if x["alt"]["id"] == elegida)
        fj = ficha_json(f, U)
        det = detalle_alternativa(ctx, elegida)
        dsq = next((d for d in U["decisiones"] if d["OBJETIVO"] == "MAX_VAN"), {})
        out = {"modo": modo, "resultado": "ALTERNATIVA", "alternativa": fj, "detalle": det,
               "decision_status_quo": _decision_json(dsq), "universo": ctx.ent["universo"],
               "etiqueta": mopt.etiqueta(ctx.ent["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"],
               "tarjetas": TX.tarjetas(fj, det), "por_que": TX.por_que(fj, det, opt, U),
               "que_hacer": TX.que_hacer(fj, det, U), "alertas": _alertas(ctx, U["fichas"]), "disclaimer": TX.DISCLAIMER,
               "optimizacion": _resumen_opt(opt) if opt else None}
        return out
    return _cache("simular", ctx, {"aid": aid}, calc)


def _resumen_opt(opt):
    if not opt:
        return None
    d = opt["decision_principal"] or {}
    return {"objetivo": opt["objetivo_principal"], "estado": d.get("ESTADO"), "mejor": d.get("MEJOR"), "segunda": d.get("SEGUNDA"),
            "decision": d.get("DECISION_ESCENARIO"), "diferencia": d.get("DIFERENCIA_VALOR"), "n_alternativas": opt["n_alternativas"],
            "n_completas": opt["n_completas"], "explicacion": opt.get("explicacion")}


# ---------------------------------------------------------------------------------------------
# RIESGO: one-way, tornado, 2D, stress, quiebres, Monte Carlo
# ---------------------------------------------------------------------------------------------
def _alt_riesgo(ctx, aid):
    if not aid:
        aid = id_simple(ctx)
    if not aid:
        opt = optimizar(ctx.esc)
        d = opt["decision_principal"] or {}
        aid = d.get("MEJOR") if d.get("ESTADO") == "MEJOR_EN_ESCENARIO" else None
    if not aid or aid == SQ or aid == "—":
        raise ES.ErrorEscenario("Elija una alternativa de inversión con resultados (el status quo no tiene métricas).")
    return ctx.alt(aid)


def sensibilidad(esc, aid=None, variables=None, shocks=None, metricas=None):
    """One-way (¿qué pasa si…?). shocks relativos (fracción) para variables RELATIVO; días / meses para las absolutas."""
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)
    variables = variables or ["precio_venta"]
    for v in variables:
        if v not in mr.VARIABLES:
            raise ES.ErrorEscenario(f"Variable {v} no soportada por el motor.")

    def calc():
        inp = dict(ctx.ent["inp"])
        if shocks is not None:
            xs = [float(x) for x in shocks]          # en la unidad del tipo de shock de la variable (fracción, días o meses)
            inp["sensibilidad.shocks_relativos"] = xs
            inp["sensibilidad.shocks_dias"] = xs
            inp["sensibilidad.shocks_meses"] = xs
        if metricas and "TIR" in metricas:
            inp["tornado.metricas"] = ["VAN", "TIR"]
        filas = mr.sensibilidad_oneway(ctx.E, alt, variables, inp)
        return {"alternativa": alt["id"], "filas": filas, "variables": [M.variables_riesgo_por_id(v) for v in variables],
                "etiqueta": mopt.etiqueta(alt["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"],
                "nota": "Shocks de sensibilidad: no implican probabilidad. RELATIVO = fracción (−0,10 = −10 %); "
                        "ABSOLUTO_DIAS = días; ABSOLUTO_MESES = meses."}
    return _cache("sensibilidad", ctx, {"aid": alt["id"], "v": variables, "s": shocks, "m": metricas}, calc)


def tornado(esc, aid=None, metrica="VAN", variables=None):
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)

    def calc():
        inp = dict(ctx.ent["inp"])
        vs = variables or [v for v in mr.como_lista(M.inputs_riesgo()[0].get("sensibilidad.variables")) if v in mr.VARIABLES]
        ow = mr.sensibilidad_oneway(ctx.E, alt, vs, inp)
        tor = mr.tornado(ow, metrica, alt["id"])
        calculable = any(t.get("SWING") is not None for t in tor)
        return {"alternativa": alt["id"], "metrica": metrica, "tornado": tor, "calculable": calculable,
                "nota": None if calculable else f"{metrica} no publicable en la base: no se genera tornado (no se fabrica ranking).",
                "etiqueta": mopt.etiqueta(alt["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"]}
    return _cache("tornado", ctx, {"aid": alt["id"], "m": metrica, "v": variables}, calc)


def sensibilidad_2d(esc, aid=None, vx="precio_venta", vy="alimento", shocks=None):
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)
    for v in (vx, vy):
        if v not in mr.VARIABLES:
            raise ES.ErrorEscenario(f"Variable {v} no soportada.")

    def calc():
        inp = dict(ctx.ent["inp"])
        if shocks is not None:
            inp["sensibilidad.shocks_relativos"] = [float(x) for x in shocks]
        filas = mr.sensibilidad_2d(ctx.E, alt, (vx, vy), inp)
        return {"alternativa": alt["id"], "vx": vx, "vy": vy, "filas": filas,
                "umbral_dscr": inp.get("umbral.dscr_2d"), "umbral_payback": inp.get("umbral.payback_2d"),
                "nota": "Zonas DSCR / payback solo con umbrales declarados por el usuario (no se inventan).",
                "etiqueta": mopt.etiqueta(alt["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"]}
    return _cache("sens2d", ctx, {"aid": alt["id"], "x": vx, "y": vy, "s": shocks}, calc)


def stress(esc, aid=None, stresses=None):
    """stresses: [{id, nombre, shocks:{var: valor}}] editables; sin lista → los del escenario o de escenarios_stress.csv."""
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)

    def calc():
        if stresses is not None:
            tmp = copy.deepcopy(ctx.esc)
            tmp["experto"]["stress"] = stresses
            st = ES.stresses(tmp)
        else:
            st = ctx.ent["stresses"]
        filas = mr.correr_stress(ctx.E, alt, st)
        base = ctx.E.evaluar(alt)
        return {"alternativa": alt["id"], "base": base["met"], "filas": filas,
                "nota": "Magnitudes ilustrativas y editables (SUP-223): no son pronósticos ni probabilidades.",
                "etiqueta": mopt.etiqueta(alt["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"]}
    return _cache("stress", ctx, {"aid": alt["id"], "st": stresses}, calc)


QUIEBRES = (   # pregunta de negocio → (variable del motor, métrica, objetivo)
    ("Precio mínimo de venta (VAN = 0)", "precio_venta", "VAN", 0.0),
    ("Costo máximo de alimento (VAN = 0)", "alimento", "VAN", 0.0),
    ("CAPEX máximo (VAN = 0)", "capex", "VAN", 0.0),
    ("Demanda mínima (VAN = 0)", "demanda", "VAN", 0.0),
    ("Utilización mínima (VAN = 0)", "utilizacion", "VAN", 0.0),
    ("Días de cobro máximos (VAN = 0)", "dias_cobro", "VAN", 0.0),
    ("Precio mínimo de venta (EBITDA = 0)", "precio_venta", "EBITDA", 0.0),
)


def quiebres(esc, aid=None):
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)

    def calc():
        filas = []
        for pregunta, var, met, obj in QUIEBRES:
            q = mr.punto_quiebre(ctx.E, alt, var, met, obj, None, 24)
            q["PREGUNTA"] = pregunta
            q["MOSTRAR"] = q.get("ESTADO") == "ENCONTRADO"
            q["TEXTO"] = TX.texto_quiebre(q)
            filas.append(q)
        return {"alternativa": alt["id"], "filas": filas, "etiqueta": mopt.etiqueta(alt["universo"]),
                "solo_demostracion": ctx.ent["solo_demostracion"],
                "nota": "Solo se muestran quiebres ENCONTRADOS dentro del rango del motor; los demás se informan con su estado."}
    return _cache("quiebres", ctx, {"aid": alt["id"]}, calc)


def montecarlo(esc, aid=None, n=None, semilla=None):
    ctx = contexto(esc)
    alt = _alt_riesgo(ctx, aid)

    def calc():
        inp = ctx.ent["inp"]
        dists, corrs = ctx.ent["dists"], ctx.ent["corrs"]
        n_ = int(n or inp.get("montecarlo.n") or 1000)
        sem = int(semilla or inp.get("montecarlo.semilla") or 20261005)
        try:
            est, res, mu, notas = mr.monte_carlo(ctx.E, alt, dists, corrs, n_, sem, alt["universo"],
                                                 mr.num(inp.get("restriccion.CAPITAL_DISPONIBLE.valor")),
                                                 con_tir=False, supuesto_independencia=bool(inp.get("montecarlo.supuesto_independencia")))
        except mr.ErrorRiesgo as e:
            est, res, mu, notas = "NO_DISPONIBLE", {}, [], [str(e)]
        disponible = est == "EJECUTADO"
        hist = [m["VAN"] for m in mu if m.get("VAN") is not None]
        return {"alternativa": alt["id"], "estado": est, "disponible": disponible, "resumen": res, "notas": notas,
                "van_muestras": hist, "n": n_, "semilla": sem,
                "tipo_probabilidad": "PROBABILIDAD_SIMULADA (no histórica, no del proyecto)" if disponible else None,
                "explicacion": None if disponible else "Faltan distribuciones de probabilidad respaldadas (DPV-180). "
                               "Sin ellas no se ejecuta Monte Carlo: no se inventan probabilidades.",
                "distribuciones": dists, "correlaciones": corrs,
                "etiqueta": mopt.etiqueta(alt["universo"]), "solo_demostracion": ctx.ent["solo_demostracion"]}
    return _cache("montecarlo", ctx, {"aid": alt["id"], "n": n, "s": semilla}, calc)


def alternativas_resumen(esc):
    """Lista de alternativas del escenario con una evaluación RÁPIDA del motor (calcular_tir=False): ¿tiene VAN?"""
    ctx = contexto(esc)

    def calc():
        out = []
        for a in ctx.alts:
            if a["tipo"] == SQ:
                out.append({"id": a["id"], "tipo": SQ, "configuracion": SQ, "escalas": [], "completa": None,
                            "descripcion": a["descripcion"]})
                continue
            ev = ctx.E.evaluar(a)
            res = ev.get("res") or {}
            out.append({"id": a["id"], "tipo": a["tipo"], "configuracion": a["configuracion"], "variante": a["variante"],
                        "escalas": list(a["escalas"]), "trayectoria": a["trayectoria"], "estado": ev["estado"],
                        "completa": ev["met"].get("VAN") is not None,
                        "faltan": sorted(faltantes_por_bloque(res.get("FALTANTES")).keys()) if res else [ev["motivo"][:200]]})
        return {"alternativas": out, "universo": ctx.ent["universo"], "etiqueta": mopt.etiqueta(ctx.ent["universo"]),
                "solo_demostracion": ctx.ent["solo_demostracion"], "alertas": _alertas(ctx)}
    return _cache("alternativas", ctx, {}, calc)


def traza_alternativa(esc, aid):
    """Mapa de drivers (Traza del motor) de una alternativa: VARIABLE, VALOR, UNIDAD, ORIGEN, ARCHIVO, EVIDENCIA."""
    ctx = contexto(esc)
    alt = ctx.alt(aid)
    b = ctx.E.base(alt)
    if b[0] == "ERROR":
        raise ES.ErrorEscenario(TX.mensaje_error_motor(b[1]))
    return {"alternativa": aid, "filas": [dict(f) for f in b[1].filas]}


def modulos_alternativa(aid):
    """Módulos de CAPEX y OPEX admitidos por la arquitectura de una alternativa (para cargar overrides compatibles, TF-004)."""
    cfg, var, escs, _ = ES.id_motor(aid).split("|")
    E_ = int(escs.split("-")[0])
    variante = None if var == "BASE" else var
    cc, co = mf.configs(variante or f"{cfg}-{E_}")
    ctx = mf.contexto_override(cfg, variante, E_, cc, co)
    return {"alternativa": aid, "configuracion": cfg, "variante": var, "escala": E_, "capex_modulos": sorted(ctx["capex_mod"]),
            "opex_modulos": sorted(ctx["opex_mod"]), "universos": sorted(mf.UNIVERSO_DIM),
            "arquitectura": {k: str(cc[k]) for k in mf.DIMS_ARQ},
            "meta_requerida": list(mf.CAMPOS_META_OVERRIDE)}


def tir_rapida_completa(esc, aid):
    """Comparación del modo rápido (calcular_tir=False) y el completo para la misma alternativa (test #51)."""
    ctx = contexto(esc)
    alt = ctx.alt(aid)
    r = ctx.E.evaluar(alt, tir=False)
    c = ctx.E.evaluar(alt, tir=True)
    return _limpio({"rapida": r["met"], "completa": c["met"]})


def costo_unitario(esc, aid, concepto, precio):
    """Vista previa: cuánto costea el módulo 20 un precio unitario del escenario en una alternativa."""
    cfg, var, escs, _ = ES.id_motor(aid).split("|")
    rub, est, det = ES.rubro_desde_precio_unitario(cfg, var, int(escs.split("-")[0]), concepto, float(precio))
    return _limpio({"estado": est, "detalle": det, "rubro": rub})
