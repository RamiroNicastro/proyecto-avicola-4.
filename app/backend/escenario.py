"""Formato de ESCENARIO de la app (JSON versionado) y su traducción a la entrada de los motores.

Un escenario de la app tiene dos capas:
  * "simple"  : pocos inputs en lenguaje de negocio (objetivo, capital, demanda, precios, arquitectura, escala,
                restricciones). Se TRADUCE a campos del motor; no calcula nada.
  * "experto" : la estructura nativa del motor (misma que 22_riesgos/escenario_optimizador.json: comun +
                por_alternativa + base_valores + disponibilidad) más los parámetros de análisis de
                inputs_riesgo_optimizacion.csv, stress, distribuciones y correlaciones.

La capa simple se aplica SOBRE la experta (el modo simple oculta complejidad; no la elimina). La traducción es
determinística: los mismos inputs dan la misma entrada del motor (test "simple = experto").

Reglas (CLAUDE.md, interfaz_app_v1.md):
  * un campo vacío / "NO SÉ" no se envía: el motor lo informa como PENDIENTE (nunca 0);
  * USD 2 M no es default: capital vacío = sin restricción de capital;
  * la demanda POTENCIAL no se convierte en ASEGURADA; los ~90 supermercados no son demanda;
  * ARS solo con TC, tipo y fecha (mf.a_usd del motor, regla 2);
  * nada de este archivo escribe en archivos de evidencia.
"""
import copy
import hashlib
import io
import json
import uuid
from contextlib import redirect_stdout
from datetime import datetime

from . import motor as M

mf, mr, mopt, mo = M.mf, M.mr, M.mopt, M.mo

FORMATO = "ESCENARIO_APP_AVICOLA"
VERSION_FORMATO = 1
TIPOS = ("USUARIO", "PRESET", "DEMO_ARTIFICIAL")
ESTADOS_DATO = ("VALIDADO", "COTIZACION", "ESCENARIO", "NO_SE")
PREFIJO_DEMO = "DEMO-"

# Objetivo en lenguaje simple → objetivo del optimizador (sin pesos ocultos: BALANCEADO exige pesos visibles).
OBJETIVOS_SIMPLES = {
    "GANAR_MAS": ("MAX_VAN", "Mayor VAN del proyecto (valor creado sobre la tasa de descuento)."),
    "INVERTIR_MENOS": ("MIN_FONDOS_INICIALES", "Menores fondos iniciales (CAPEX inicial + capital de trabajo inicial + otros)."),
    "RECUPERAR_RAPIDO": ("MIN_PAYBACK", "Menor payback simple (años hasta recuperar la inversión)."),
    "REDUCIR_RIESGO": ("MAX_ROBUSTEZ", "Mayor robustez: % de escenarios de stress y extremos con VAN ≥ 0 "
                                       "(no requiere pesos; el score de riesgo MIN_RIESGO exige pesos declarados)."),
    "CRECER": ("MAX_CRECIMIENTO", "Mayor capacidad final (aves/día) alcanzada en el horizonte."),
    "BALANCEADO": ("BALANCEADO", "Combinación de rentabilidad, riesgo, capital, liquidez, crecimiento y robustez con los "
                                 "PESOS QUE USTED DECLARA (sin pesos el balanceado queda PESOS_NO_DEFINIDOS)."),
}

# Precios unitarios de costo del modo simple → concepto del registro de 20_opex (COSTO_ID) cuyo driver de cantidad
# calcula el propio módulo 20 (cantidad × precio = COSTO_CALCULADO_USD_ANIO). Si la arquitectura no tiene el concepto,
# el precio NO_APLICA a esa alternativa.
COSTOS_UNITARIOS = {
    "alimento": {"costo_id": "ALI-A-PT", "unidad": "USD/t", "texto": "Alimento balanceado comprado (puesto en granja)"},
    "pollito": {"costo_id": "POL-COMPRA", "unidad": "USD/pollito", "texto": "Pollito BB comprado"},
    "facon_faena": {"costo_id": "FAE-FACON", "unidad": "USD/ave", "texto": "Tarifa de faena a façon"},
}

# Perfil de análisis RÁPIDO para comparar / optimizar (parámetros de análisis, no decisiones empresariales):
# sensibilidad solo sobre las variables de robustez; sin 2D ni quiebres (se piden en la pantalla de riesgos).
PERFIL_RAPIDO = {"sensibilidad.variables": None, "sens2d.pares": None, "quiebre.variables": None}


def ahora():
    return datetime.now().isoformat(timespec="seconds")


def plantilla_comun():
    """`comun` vacío con la MISMA estructura que la plantilla del motor (todo null = PENDIENTE)."""
    with open(mopt.ARCH_ESCENARIO, encoding="utf-8") as fh:
        spec = json.load(fh)
    return {k: v for k, v in spec["comun"].items() if not k.startswith("_")}


def disponibilidad_vacia():
    with open(mopt.ARCH_ESCENARIO, encoding="utf-8") as fh:
        spec = json.load(fh)
    return dict(spec["disponibilidad"]), dict(spec["base_valores"])


def nuevo(nombre="Escenario sin nombre", tipo="USUARIO"):
    disp, bv = disponibilidad_vacia()
    return {
        "formato": FORMATO, "version_formato": VERSION_FORMATO, "id": uuid.uuid4().hex[:12], "nombre": nombre,
        "descripcion": "", "tipo": tipo, "solo_demostracion": False, "creado": ahora(), "modificado": ahora(),
        "simple": {
            "objetivo": None,
            "capital": {"no_se": True, "valor": None, "moneda": "USD", "tc": None, "tipo_tc": None, "fecha_tc": None,
                        "fuente_tc": None, "metrica": "PICO_FONDOS"},
            "demanda": [], "categorias_vendibles": list(mf.CATEGORIAS_DEMANDA), "alfa_negociada": None,
            "precios_venta": [], "costos_unitarios": [],
            "arquitectura": {"modo": "AUTO", "configuracion": None, "variante": None},
            "escala": {"modo": "AUTO", "valor": None},
            "restricciones": {}, "horizonte_anios": None,
        },
        "experto": {
            "comun": plantilla_comun(), "por_alternativa": {}, "base_valores": bv, "disponibilidad": disp,
            "plantilla": None, "analisis": {}, "perfil_analisis": "RAPIDO", "stress": [], "distribuciones": [],
            "correlaciones": [], "trayectorias": False,
        },
        "procedencia": {},
    }


class ErrorEscenario(Exception):
    """Error de validación del escenario (mensaje para el usuario)."""


def validar(esc):
    """Validación estructural (la económica la hace el motor). Devuelve el escenario normalizado."""
    if not isinstance(esc, dict) or esc.get("formato") != FORMATO:
        raise ErrorEscenario(f"El archivo no es un escenario de la app (formato {FORMATO!r}).")
    v = esc.get("version_formato")
    if v != VERSION_FORMATO:
        raise ErrorEscenario(f"Versión de formato {v!r} no soportada (esta app lee la versión {VERSION_FORMATO}).")
    if esc.get("tipo") not in TIPOS:
        raise ErrorEscenario(f"Tipo de escenario {esc.get('tipo')!r} no admitido {TIPOS}.")
    base = nuevo(esc.get("nombre") or "Escenario", esc["tipo"])
    out = copy.deepcopy(esc)
    for capa in ("simple", "experto"):
        out.setdefault(capa, {})
        for k, x in base[capa].items():
            out[capa].setdefault(k, copy.deepcopy(x))
    out.setdefault("procedencia", {})
    s = out["simple"]
    if s["objetivo"] not in (None, *OBJETIVOS_SIMPLES):
        raise ErrorEscenario(f"Objetivo {s['objetivo']!r} no admitido.")
    for p in s["precios_venta"] + s["costos_unitarios"]:
        if p.get("estado") not in ESTADOS_DATO:
            raise ErrorEscenario(f"Estado de dato {p.get('estado')!r} no admitido {ESTADOS_DATO}.")
    for l in s["demanda"]:
        if l.get("categoria") not in mf.CATEGORIAS_DEMANDA:
            raise ErrorEscenario(f"Categoría de demanda {l.get('categoria')!r} no admitida {mf.CATEGORIAS_DEMANDA}.")
        if l.get("unidad") not in mf.UNIDADES_DEMANDA:
            raise ErrorEscenario(f"Unidad de demanda {l.get('unidad')!r} no admitida.")
    a = s["arquitectura"]
    if a.get("modo") == "MANUAL" and a.get("configuracion") not in M.CONFIGURACIONES:
        raise ErrorEscenario("Arquitectura MANUAL sin configuración válida (C0, C1, C2, C3 o CF).")
    e = s["escala"]
    if e.get("modo") == "VALOR":
        lo, hi = mcx_rango()
        try:
            val = int(e.get("valor"))
        except (TypeError, ValueError):
            raise ErrorEscenario("Escala sin valor numérico.")
        if not lo <= val <= hi:
            raise ErrorEscenario(f"Escala {val} fuera del rango que el motor puede evaluar físicamente ({lo}–{hi} aves/día).")
    if out.get("tipo") == "DEMO_ARTIFICIAL" and not out.get("solo_demostracion"):
        raise ErrorEscenario("Un escenario DEMO_ARTIFICIAL debe estar marcado SOLO_DEMOSTRACION.")
    return out


def mcx_rango():
    return M.mcx.RANGO_ESCALA


def huella(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str, ensure_ascii=False).encode()).hexdigest()


def parte_motor(esc):
    """Lo que determina los resultados (sin nombre, fechas, id ni procedencia): base de la clave de caché."""
    return {"simple": esc["simple"], "experto": esc["experto"], "tipo": esc["tipo"]}


# ---------------------------------------------------------------------------------------------
# TRADUCCIÓN capa simple → motor
# ---------------------------------------------------------------------------------------------
def universo(esc):
    return "ARTIFICIAL_TEST" if esc.get("tipo") == "DEMO_ARTIFICIAL" else "ESCENARIO"


def capital_usd(cap):
    """Capital declarado en USD (ARS solo con TC, tipo y fecha: función del motor). None = sin restricción."""
    if not cap or cap.get("no_se") or cap.get("valor") in (None, ""):
        return None
    try:
        return mf.a_usd(float(cap["valor"]), cap.get("moneda") or "USD", cap.get("tc"), cap.get("fecha_tc"), cap.get("tipo_tc"))
    except mf.ErrorFinanciero as e:
        raise ErrorEscenario(f"Capital en {cap.get('moneda')}: falta tipo de cambio, tipo de TC y fecha (regla 2). {e}")


def precio_usd(p):
    if p.get("estado") == "NO_SE" or p.get("valor") in (None, ""):
        return None
    try:
        return mf.a_usd(float(p["valor"]), p.get("moneda") or "USD", p.get("tc"), p.get("fecha_tc"), p.get("tipo_tc"))
    except mf.ErrorFinanciero as e:
        raise ErrorEscenario(f"{p.get('producto') or p.get('concepto')}: valor en {p.get('moneda')} sin TC, tipo y fecha. {e}")


def aplicar_simple(esc):
    """Devuelve (comun, analisis_extra, avisos): `comun` del experto con la capa simple aplicada encima."""
    s, x = esc["simple"], esc["experto"]
    comun = copy.deepcopy(x["comun"])
    comun.setdefault("valores", {})
    extra, avisos = {}, []
    if s.get("horizonte_anios") not in (None, ""):
        comun["valores"]["horizonte_anios"] = int(s["horizonte_anios"])
    if s["demanda"]:
        lineas = []
        for i, l in enumerate(s["demanda"]):
            if l.get("valor") in (None, ""):
                avisos.append(f"Demanda {l.get('producto')}|{l.get('canal')}: sin volumen → no se envía (PENDIENTE).")
                continue
            ln = {"id": l.get("id") or f"S{i + 1:02d}", "producto": l["producto"], "canal": l["canal"],
                  "mercado": l.get("mercado") or "INTERNO", "categoria": l["categoria"], "valor": float(l["valor"]),
                  "unidad": l["unidad"], "prioridad": int(l.get("prioridad") or 1)}
            if l.get("toma_todo"):
                ln["toma_todo"] = True
            lineas.append(ln)
        comun["demanda"] = lineas                      # la capa simple define la demanda (reemplaza la del experto)
    if s.get("categorias_vendibles"):
        comun["categorias_demanda_usadas"] = list(s["categorias_vendibles"])
    if s.get("alfa_negociada") not in (None, ""):
        comun["alfa_negociada"] = float(s["alfa_negociada"])
    for p in s["precios_venta"]:
        v = precio_usd(p)
        clave = f"{p['producto']}|{p['canal']}|{p.get('mercado') or 'INTERNO'}"
        if v is None:
            comun.setdefault("precios", {}).pop(clave, None)
            avisos.append(f"Precio {clave}: NO SÉ → PENDIENTE (no se usa 0).")
            continue
        comun.setdefault("precios", {})[clave] = {"tipo": "CONSTANTE", "usd_kg": v}
    cap = capital_usd(s.get("capital"))
    if cap is not None:
        extra["restriccion.CAPITAL_DISPONIBLE.valor"] = cap
        extra["restriccion.CAPITAL_DISPONIBLE.tipo"] = "HARD"
        extra["consulta.capital_usd"] = cap
        extra["capital.metrica"] = (s.get("capital") or {}).get("metrica") or "PICO_FONDOS"
    for nombre, val in (s.get("restricciones") or {}).items():
        if val in (None, ""):
            continue
        if nombre == "DEMANDA_MAXIMA_T_DIA":
            extra["consulta.demanda_t_dia"] = float(val)   # consulta del motor (no es restricción del optimizador)
            continue
        if nombre not in mopt.RESTRICCIONES:
            raise ErrorEscenario(f"Restricción {nombre} no existe en el optimizador.")
        extra[f"restriccion.{nombre}.valor"] = float(val)
        extra[f"restriccion.{nombre}.tipo"] = "HARD"
        if nombre == "PAYBACK":
            extra["consulta.payback_max_anios"] = float(val)
    if s.get("objetivo"):
        obj = OBJETIVOS_SIMPLES[s["objetivo"]][0]
        extra["objetivo_principal"] = obj
    return comun, extra, avisos


def inputs_analisis(esc, extra):
    """inputs_riesgo_optimizacion.csv (leído por el motor) + parámetros de análisis del experto + capa simple."""
    inp = copy.deepcopy(M.inputs_riesgo()[0])
    if esc["experto"].get("perfil_analisis", "RAPIDO") == "RAPIDO":
        inp.update(PERFIL_RAPIDO)
        inp["sensibilidad.variables"] = list(mr.como_lista(inp.get("robustez.variables")))
    for k, v in (esc["experto"].get("analisis") or {}).items():
        inp[k] = v
    s = esc["simple"]
    a, e = s["arquitectura"], s["escala"]
    if a.get("modo") == "MANUAL":
        inp["espacio.configuraciones"] = [a["configuracion"]]
        if not a.get("variante"):
            inp["espacio.incluir_variantes"] = False
    if e.get("modo") == "VALOR":
        inp["espacio.escalas"] = [int(e["valor"])]
        inp["espacio.trayectorias"] = None
    if not esc["experto"].get("trayectorias"):
        inp["espacio.trayectorias"] = None
    obj_p = extra.pop("objetivo_principal", None)
    inp.update(extra)
    inp["optimizador.objetivos"] = list(mopt.OBJETIVOS)        # se corren todos; el principal solo se destaca
    return inp, obj_p


def stresses(esc, inp_motor=True):
    """Stress del escenario (editables). Si el usuario no declaró ninguno, se usan los de escenarios_stress.csv."""
    st = esc["experto"].get("stress") or []
    if not st:
        return mr.leer_stress()
    out = []
    for s in st:
        shocks, pend = {}, []
        for var, val in (s.get("shocks") or {}).items():
            if var not in mr.VARIABLES:
                raise ErrorEscenario(f"Stress {s.get('id')}: variable {var} desconocida.")
            if val in (None, ""):
                pend.append(var)
            else:
                shocks[var] = float(val)
        out.append({"ID_STRESS": s.get("id") or f"ST-U{len(out) + 1:02d}", "NOMBRE": s.get("nombre") or "", "shocks": shocks,
                    "pendientes": pend, "activo": s.get("activo", True), "estado": {"USUARIO"}, "origen": {"ESCENARIO_APP"}})
    return out


def distribuciones(esc):
    """Distribuciones y correlaciones del escenario (validadas por el motor). Sin ninguna: las del repo (PENDIENTES)."""
    ds = esc["experto"].get("distribuciones") or []
    cs = esc["experto"].get("correlaciones") or []
    if not ds:
        return mr.leer_distribuciones(), mr.leer_correlaciones()
    out = []
    for d in ds:
        dd = {"VARIABLE": d["VARIABLE"], "DISTRIBUCION": d.get("DISTRIBUCION"), "PARAMETROS": d.get("PARAMETROS") or {},
              "FUENTE": d.get("FUENTE") or "", "ESTADO": d.get("ESTADO") or "PENDIENTE"}
        if dd["VARIABLE"] not in mr.VARIABLES:
            raise ErrorEscenario(f"Distribución de variable desconocida {dd['VARIABLE']}.")
        if dd["ESTADO"] not in mr.ESTADOS_DIST:
            raise ErrorEscenario(f"Estado de distribución {dd['ESTADO']} no admitido {mr.ESTADOS_DIST}.")
        if dd["ESTADO"] == "RESPALDADA" and not dd["FUENTE"]:
            raise ErrorEscenario(f"Distribución {dd['VARIABLE']} RESPALDADA sin fuente.")
        if dd["ESTADO"] != "PENDIENTE":
            try:
                mr.validar_distribucion(dd)
            except mr.ErrorRiesgo as e:
                raise ErrorEscenario(str(e))
        out.append(dd)
    corrs = [{"A": c["A"], "B": c["B"], "RHO": None if c.get("RHO") in (None, "") else float(c["RHO"]),
              "ESTADO": c.get("ESTADO") or "PENDIENTE", "FUENTE": c.get("FUENTE") or ""} for c in cs]
    return out, corrs


# ---------------------------------------------------------------------------------------------
# Costos unitarios del modo simple → rubros de OPEX costeados por el módulo 20 (cantidad del módulo × precio)
# ---------------------------------------------------------------------------------------------
_CACHE_RUBRO = {}


def rubro_desde_precio_unitario(cfg, variante, escala, concepto, precio_usd_u):
    """Corre 20_opex (mo.correr) con una COPIA EN MEMORIA de base_costos_opex.csv donde el concepto lleva el precio del
    escenario. Devuelve (rubro | None, estado, detalle). El archivo base no se modifica."""
    spec = COSTOS_UNITARIOS[concepto]
    key = (cfg, variante or "BASE", int(escala), concepto, round(float(precio_usd_u), 10))
    if key in _CACHE_RUBRO:
        return copy.deepcopy(_CACHE_RUBRO[key])
    cc, co = mf.configs(variante if variante and variante != "BASE" else f"{cfg}-{int(escala)}")
    base = copy.deepcopy(mo.leer_base())
    fila = base.get(spec["costo_id"])
    fila.update(PRECIO_UNITARIO=str(precio_usd_u), MONEDA_ORIGINAL="USD", NIVEL_EVIDENCIA="E5", ESTADO="CON_PRECIO",
                FUENTE="ESCENARIO_APP (no es evidencia)", FECHA_PRECIO="")
    with redirect_stdout(io.StringIO()):
        filas = mo.correr(co, base)[0]
    f = next((r for r in filas if r["COSTO_ID"] == spec["costo_id"] and r["COSTEA"]), None)
    if f is None:
        out = (None, "NO_APLICA_A_LA_ARQUITECTURA", f"{spec['costo_id']} no existe en {cfg}/{variante or 'BASE'}")
    elif f["COSTO_CALCULADO_USD_ANIO"] is None:
        out = (None, "CANTIDAD_PENDIENTE_EN_MODULO_20", f"{spec['costo_id']}: {f['ESTADO']} ({f.get('MOTIVO') or ''})")
    else:
        rub = {"rubro": spec["costo_id"], "grupo_proveedor": f["GRUPO_PROVEEDOR"], "naturaleza": f["NATURALEZA"],
               "costo_pleno_usd_anio": f["COSTO_CALCULADO_USD_ANIO"], "pct_variable": f["PCT_VARIABLE"],
               "es_compra": bool(f["GRUPO_PROVEEDOR"]), "dias_pago": None, "iva_credito": bool(f["GRUPO_PROVEEDOR"]),
               "meta": {"CONFIGURACION": cfg, "ESCALA": int(escala), "VARIANTE": variante or "BASE",
                        "MODULO": f["MODULO_ARQ"], "UNIVERSO": f["MODULO_ARQ"], "ORIGEN": "ESCENARIO_USUARIO"},
               "_app": f"cantidad {f['CANTIDAD']:.6g} {f['UNIDAD']}/año (módulo 20) × {precio_usd_u:g} {spec['unidad']}"}
        out = (rub, "APLICADO", rub["_app"])
    _CACHE_RUBRO[key] = copy.deepcopy(out)
    return out


def aplicar_costos_unitarios(esc, alts_ids, por_alt):
    """Agrega / reemplaza (por COSTO_ID) los rubros costeados en por_alternativa de cada alternativa de etapa única."""
    detalle = []
    costos = [c for c in esc["simple"]["costos_unitarios"] if c.get("estado") != "NO_SE" and c.get("valor") not in (None, "")]
    if not costos:
        return detalle
    for aid in alts_ids:
        cfg, var, escs, tray = aid.split("|")
        if "-" in escs:
            detalle.append({"ALTERNATIVA": aid, "ESTADO": "NO_APLICA_TRAYECTORIA",
                            "DETALLE": "costos unitarios simples solo en alternativas de una etapa"})
            continue
        for c in costos:
            rub, est, det = rubro_desde_precio_unitario(cfg, var, int(escs), c["concepto"], precio_usd(c))
            detalle.append({"ALTERNATIVA": aid, "CONCEPTO": c["concepto"], "ESTADO": est, "DETALLE": det})
            if rub is None:
                continue
            pa = por_alt.setdefault(aid, {})
            ets = pa.setdefault("etapas", [{}])
            rubros = [r for r in (ets[0].get("opex_rubros") or []) if r.get("rubro") != rub["rubro"]]
            rub = {k: v for k, v in rub.items() if k != "_app"}
            dp = (esc["experto"]["comun"].get("valores") or {}).get(f"dias_pago.{rub['grupo_proveedor']}")
            rub["dias_pago"] = dp
            rubros.append(rub)
            ets[0]["opex_rubros"] = rubros
    return detalle


# ---------------------------------------------------------------------------------------------
# ENTRADA COMPLETA PARA LOS MOTORES
# ---------------------------------------------------------------------------------------------
def a_motor(esc):
    """Traduce el escenario de la app a la entrada del optimizador/motor:
    {universo, escenario (formato escenario_optimizador.json), inp, objetivo_principal, stresses, dists, corrs, avisos}."""
    esc = validar(esc)
    verificar_override_total(esc)
    comun, extra, avisos = aplicar_simple(esc)
    inp, obj_p = inputs_analisis(esc, extra)
    x = esc["experto"]
    por_alt = copy.deepcopy(x.get("por_alternativa") or {})
    if universo(esc) == "ARTIFICIAL_TEST":
        por_alt = {k[len(PREFIJO_DEMO):] if k.startswith(PREFIJO_DEMO) else k: v for k, v in por_alt.items()}
    escenario = {"plantilla": x.get("plantilla"), "comun": comun, "por_alternativa": por_alt,
                 "base_valores": copy.deepcopy(x.get("base_valores") or {}),
                 "disponibilidad": copy.deepcopy(x.get("disponibilidad") or {})}
    ids = [a["id"] for a in mopt.alternativas_reales(inp, "ESCENARIO", escenario) if a["tipo"] != mr.STATUS_QUO]
    det_costos = aplicar_costos_unitarios(esc, ids, por_alt)
    dists, corrs = distribuciones(esc)
    return {"universo": universo(esc), "escenario": escenario, "inp": inp, "objetivo_principal": obj_p,
            "stresses": stresses(esc), "dists": dists, "corrs": corrs, "avisos": avisos, "costos_unitarios": det_costos,
            "solo_demostracion": bool(esc.get("solo_demostracion"))}


def verificar_override_total(esc):
    """OVERRIDE_TOTAL_ARQUITECTURA (TF-004) solo con confirmación explícita del usuario en la app: la corrida pierde parte de
    la trazabilidad automática. Sin confirmación → error claro; con confirmación, el motor la rotula
    SIMULACION_HIPOTETICA_OVERRIDE_TOTAL. Valores distintos de true/false los rechaza el propio motor."""
    x = esc["experto"]
    lugares = [("comun", x["comun"])] + [(k, v) for k, v in (x.get("por_alternativa") or {}).items()]
    activos = [k for k, d in lugares if isinstance(d, dict) and d.get("OVERRIDE_TOTAL_ARQUITECTURA") is True]
    if activos and x.get("override_total_confirmado") is not True:
        raise ErrorEscenario("OVERRIDE_TOTAL_SIN_CONFIRMAR: activó OVERRIDE_TOTAL_ARQUITECTURA en " + ", ".join(activos) +
                             ". Esta simulación pierde parte de la trazabilidad automática; confírmelo explícitamente.")
    return activos


def alternativas(entrada):
    """Alternativas del optimizador (funciones del motor). En la DEMO el universo es ARTIFICIAL_TEST y los IDs llevan el
    prefijo DEMO- para que nunca se lean como alternativas del proyecto."""
    alts = mopt.alternativas_reales(entrada["inp"], "ESCENARIO", entrada["escenario"])
    if entrada["universo"] == "ARTIFICIAL_TEST":
        for a in alts:
            a["universo"] = "ARTIFICIAL_TEST"
            if a["tipo"] != mr.STATUS_QUO:
                a["id"] = PREFIJO_DEMO + a["id"]
                a["cobertura"] = (0.0, "DEMO_ARTIFICIAL: ningún bloque tiene evidencia (SOLO_DEMOSTRACION)")
    return alts


def id_motor(aid):
    return aid[len(PREFIJO_DEMO):] if aid.startswith(PREFIJO_DEMO) else aid
