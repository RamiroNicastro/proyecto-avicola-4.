"""Textos en lenguaje simple, tarjetas de resultado y alertas.

Reglas:
  * Nunca se muestra un número para un indicador cuyo flag PUBLICABLE_* del motor es FALSE: se muestra NO CALCULABLE y
    debajo QUÉ FALTA (tomado del motivo del motor, no inventado).
  * En escenario / demo, todo texto es condicional («en este escenario…»), nunca categórico.
  * Los cortes del semáforo son los del optimizador (finalizar_fichas); la app no crea cortes económicos.
"""
import re

from . import escenario as ES
from . import motor as M

mf, mr, mopt = M.mf, M.mr, M.mopt

DISCLAIMER = ("Este resultado depende de los datos y supuestos ingresados. No constituye una recomendación de inversión ni "
              "reemplaza validaciones técnicas, comerciales, fiscales o financieras.")

CODIGOS_ALERTA = {
    "SOLO_DEMOSTRACION": ("demo", "Datos ficticios de demostración"),
    "SIMULACION": ("sim", "Simulación hipotética"),
    "DATO_PENDIENTE": ("pend", "Dato pendiente"),
    "EVIDENCIA_BAJA": ("pend", "Evidencia baja"),
    "NO_COMPARABLE": ("nocomp", "No comparable"),
    "OVERRIDE_TOTAL": ("error", "Override total de arquitectura"),
    "OVERRIDE_INCOMPATIBLE": ("error", "Override incompatible con la arquitectura"),
    "REGLA_FISCAL_PENDIENTE": ("pend", "Regla fiscal pendiente"),
    "NO_CALCULADA": ("nocalc", "No calculada"),
    "NO_APLICA": ("na", "No aplica"),
    "ERROR": ("error", "Error"),
}

SEMAFORO = {   # leyenda: describe los cortes que ya aplica el optimizador (modelo_optimizador.finalizar_fichas)
    "VERDE": "Evaluable, cumple todas las restricciones obligatorias, factibilidad física confirmada y 100 % de los bloques "
             "con evidencia.",
    "AMARILLO": "Evaluable y sin incumplimientos, pero con evidencia incompleta, factibilidad física pendiente o "
                "restricciones que no se pudieron evaluar.",
    "ROJO": "Incumple una restricción obligatoria (HARD) o un requisito físico (gate NO_FACTIBLE).",
    "GRIS": "No evaluable: faltan datos, no es comparable o es la alternativa de no invertir.",
}

BLOQUE_TEXTO = {
    "TIEMPO": "Falta cronograma u horizonte", "RAMPUP": "Falta curva de arranque (ramp-up)",
    "PRODUCCION": "Falta dato de producción / rendimientos", "DEMANDA": "Falta demanda", "PRECIOS": "Falta precio de venta",
    "CANALES": "Faltan condiciones comerciales del canal", "OPEX": "Falta OPEX completo",
    "IMPUESTOS_INGRESOS": "Faltan impuestos sobre ingresos", "CAPEX": "Falta CAPEX completo",
    "DEPRECIACION": "Falta vida útil de activos", "REPOSICION": "Falta costo de reposición de activos",
    "CT": "Faltan datos de capital de trabajo", "IVA": "Falta tratamiento del IVA", "GANANCIAS": "Falta impuesto a las ganancias",
    "FINANCIAMIENTO": "Falta estructura de financiamiento", "DESCUENTO": "Falta tasa de descuento",
    "VALOR_TERMINAL": "Falta valor terminal", "TIR matemática": "TIR no definida matemáticamente",
}

CONFIG_TITULO = {k: v[0] for k, v in M.EXPLICACION_CONFIG.items()}


def alerta(codigo, texto):
    tipo, titulo = CODIGOS_ALERTA.get(codigo, ("info", codigo))
    return {"codigo": codigo, "tipo": tipo, "titulo": titulo, "texto": texto}


def faltan_desde_motivo(motivo):
    """'NO_DISPONIBLE_… — falta: PRECIOS: x | CAPEX: y' → [{bloque, texto, detalle}] (sin inventar nada)."""
    if not motivo or "falta:" not in motivo:
        return []
    resto = motivo.split("falta:", 1)[1]
    out, vistos = [], set()
    for parte in resto.split(" | "):
        parte = parte.strip()
        if not parte:
            continue
        b, _, det = parte.partition(": ")
        clave = (b, det)
        if clave in vistos:
            continue
        vistos.add(clave)
        out.append({"bloque": b, "texto": BLOQUE_TEXTO.get(b, b), "detalle": det})
    return out


def _resumen_faltan(items, n=4):
    """Una línea por bloque (el detalle completo se muestra al desplegar)."""
    por, orden = {}, []
    for it in items:
        if it["bloque"] not in por:
            orden.append(it["bloque"])
            por[it["bloque"]] = []
        por[it["bloque"]].append(it["detalle"])
    return [{"bloque": b, "texto": BLOQUE_TEXTO.get(b, b), "detalles": por[b]} for b in orden][: max(n, len(orden))]


def valor(etiqueta, v, formato, flag_ok=True, motivo=None, estado=None, explicacion=None, extra=None):
    """Elemento de tarjeta. estado: VALOR | NO_CALCULABLE | NO_APLICA | NO_CALCULADA | NO_RECUPERADO | NO_EXISTE…"""
    if v is not None and flag_ok:
        e = "VALOR"
    else:
        e = estado or "NO_CALCULABLE"
        v = None
    d = {"etiqueta": etiqueta, "valor": v, "formato": formato, "estado": e,
         "faltan": _resumen_faltan(faltan_desde_motivo(motivo)) if e == "NO_CALCULABLE" else [],
         "explicacion": explicacion if e == "VALOR" else (explicacion if e not in ("NO_CALCULABLE",) else None)}
    if extra:
        d.update(extra)
    return d


def _fmt_usd(x):
    a = abs(x)
    if a >= 1e6:
        s = f"{x / 1e6:,.2f} M"
    elif a >= 1e3:
        s = f"{x / 1e3:,.0f} mil"
    else:
        s = f"{x:,.0f}"
    return "USD " + s.replace(",", "X").replace(".", ",").replace("X", ".")


def _pct(x):
    return f"{x * 100:,.1f} %".replace(".", ",")


def _num(x, d=2):
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def tarjetas(fj, det):
    """Tarjetas del resultado simple (#12) con lenguaje simple (#13) y NO CALCULABLE (#16)."""
    r = (det or {}).get("resultados") or fj.get("resultados") or {}
    m = fj.get("metricas") or {}
    pub = lambda fl: bool(r.get(fl))
    mot = lambda fl: r.get(fl + "_MOTIVO")
    tasa = r.get("TASA_DESCUENTO_ANUAL_EFECTIVA")
    H = r.get("HORIZONTE_ANIOS")
    falt = (det or {}).get("faltantes") or {}
    falt_txt = lambda b: " | ".join(f"{b}: {x}" for x in falt.get(b, []))
    cap_ini = r.get("CAPEX_INICIAL")
    capex = None if cap_ini is None else cap_ini + (r.get("CAPEX_EXPANSION") or 0.0)
    escala = "→".join(f"{e:,}".replace(",", ".") for e in fj.get("escalas") or [])
    cards = []
    cards.append({"id": "alternativa", "titulo": "Alternativa", "items": [
        {"etiqueta": "Configuración", "texto": f"{fj['configuracion']} — {CONFIG_TITULO.get(fj['configuracion'], '')}"
         + (f" · variante {fj['variante']}" if fj.get("variante") not in (None, "BASE") else ""), "estado": "TEXTO"},
        {"etiqueta": "Escala", "texto": f"{escala} aves/día operativo" if escala else "—", "estado": "TEXTO"}]})
    van = r.get("VAN")
    cards.append({"id": "inversion", "titulo": "Inversión", "items": [
        valor("CAPEX", capex, "usd", True, "— falta: " + falt_txt("CAPEX") if capex is None else None,
              explicacion="Inversión en activos de la configuración y escala (inicial + expansiones) en este escenario."),
        valor("Capital de trabajo inicial", r.get("CT_INICIAL"), "usd", True,
              "— falta: " + falt_txt("CT") if r.get("CT_INICIAL") is None else None,
              explicacion="Inventarios + cuentas a cobrar + caja operativa − cuentas a pagar durante el arranque."),
        valor("Fondos iniciales", r.get("FONDOS_INICIALES"), "usd", pub("PUBLICABLE_FLUJO"), mot("PUBLICABLE_FLUJO"),
              explicacion="CAPEX inicial + capital de trabajo inicial + otros requerimientos de caja antes de operar."),
        valor("Pico de fondos", r.get("PICO_REQUERIMIENTO_FONDOS"), "usd", pub("PUBLICABLE_FLUJO"), mot("PUBLICABLE_FLUJO"),
              explicacion=(f"Máxima necesidad acumulada de caja del proyecto (mes {r.get('MES_VALLE_CAJA')}). "
                           "Es el capital que habría que tener disponible en este escenario."))]})
    margen = r.get("MARGEN_EBITDA_ULTIMO_ANIO")
    ventas_kg = m.get("KG_VENDIDOS_ULT")
    cards.append({"id": "negocio", "titulo": "Negocio (último año del horizonte)", "items": [
        valor("Ventas", ventas_kg / 1000 if ventas_kg is not None else None, "t", pub("PUBLICABLE_INGRESOS"), mot("PUBLICABLE_INGRESOS"),
              explicacion="Toneladas vendidas en el año maduro (ventas ≤ mín(producción, demanda))."),
        valor("Facturación bruta", r.get("VENTA_BRUTA_ULTIMO_ANIO"), "usd", pub("PUBLICABLE_INGRESOS"), mot("PUBLICABLE_INGRESOS"),
              explicacion="Kilos vendidos × precio, antes de descuentos y bonificaciones."),
        valor("EBITDA", r.get("EBITDA_ULTIMO_ANIO"), "usd", pub("PUBLICABLE_EBITDA"), mot("PUBLICABLE_EBITDA"),
              explicacion="Resultado operativo antes de depreciación, intereses e impuesto a las ganancias. EBITDA no es caja."),
        valor("Margen EBITDA", margen, "pct", pub("PUBLICABLE_EBITDA"), mot("PUBLICABLE_EBITDA"),
              explicacion="EBITDA ÷ ingreso neto del año maduro.")]})
    tir_est = r.get("TIR_ESTADO") or ""
    tir_e = None if pub("PUBLICABLE_TIR") else ("NO_CALCULADA" if tir_est == mf.TIR_NO_CALCULADA else
                                                ("NO_DEFINIDA" if tir_est and not tir_est.startswith("UNICA") and pub("PUBLICABLE_FLUJO") else None))
    pb_est = r.get("PAYBACK_SIMPLE_ESTADO") or ""
    pb_e = "NO_RECUPERADO" if (pb_est.startswith("NO_RECUPERADO") and pub("PUBLICABLE_PAYBACK")) else None
    cards.append({"id": "retorno", "titulo": "Retorno", "items": [
        valor("VAN", van, "usd", pub("PUBLICABLE_VAN"), mot("PUBLICABLE_VAN"), explicacion=texto_van(van, tasa)),
        valor("TIR", r.get("TIR"), "pct", pub("PUBLICABLE_TIR"), mot("PUBLICABLE_TIR"), estado=tir_e,
              explicacion=texto_tir(r.get("TIR"), tasa) if r.get("TIR") is not None else f"TIR {tir_est}: el flujo no tiene una "
              "tasa interna única (no es 0)."),
        valor("Payback", r.get("PAYBACK_SIMPLE_ANIOS"), "anios", pub("PUBLICABLE_PAYBACK"), mot("PUBLICABLE_PAYBACK"), estado=pb_e,
              explicacion=(f"En este escenario la inversión se recuperaría en {_num(r['PAYBACK_SIMPLE_ANIOS'], 1)} años (flujo sin descontar)."
                           if r.get("PAYBACK_SIMPLE_ANIOS") is not None else f"No se recupera dentro del horizonte de {H} años."))]})
    dscr = r.get("DSCR_MINIMO")
    dscr_mot = mot("PUBLICABLE_DSCR") or ""
    cards.append({"id": "deuda", "titulo": "Deuda", "items": [
        valor("DSCR mínimo", dscr, "veces", pub("PUBLICABLE_DSCR"), dscr_mot,
              estado="NO_APLICA" if dscr_mot.startswith("NO_APLICA") else None, explicacion=texto_dscr(dscr))]})
    rob = fj.get("robustez_detalle") or {}
    cards.append({"id": "riesgo", "titulo": "Riesgo", "items": [
        {"etiqueta": "Semáforo", "texto": fj.get("semaforo") or "GRIS", "estado": "SEMAFORO", "explicacion": SEMAFORO.get(fj.get("semaforo") or "GRIS")},
        valor("Robustez", fj.get("robustez"), "pct", fj.get("robustez") is not None and rob.get("CRITERIO") == "PCT_VAN_NO_NEGATIVO",
              estado="PENDIENTE" if fj.get("robustez") is None else None,
              explicacion=f"% de {rob.get('N_ESCENARIOS')} escenarios de stress y extremos con VAN ≥ 0 (determinístico, no es probabilidad).",
              extra={"nota": rob.get("NOTA")}),
        valor("Score ordinal de riesgo", fj.get("score_riesgo"), "num", fj.get("score_riesgo") is not None,
              estado="PENDIENTE" if fj.get("score_riesgo") is None else None,
              explicacion="Orden relativo dentro del conjunto (0 = menor riesgo). NO es probabilidad.",
              extra={"nota": fj.get("riesgo_nota")})]})
    cob = fj.get("cobertura_evidencia")
    cards.append({"id": "evidencia", "titulo": "Evidencia", "items": [
        valor("Cobertura de evidencia", cob, "pct", cob is not None, estado="PENDIENTE" if cob is None else None,
              explicacion="Bloques del motor con evidencia real (E1–E3) ÷ bloques aplicables. El resto son datos de escenario.",
              extra={"nota": fj.get("cobertura_nota")}),
        {"etiqueta": "Respaldo comercial", "texto": fj.get("respaldo_comercial") or "—", "estado": "TEXTO"}]})
    cards.append({"id": "limitacion", "titulo": "Principal limitación", "items": [
        {"etiqueta": "", "texto": texto_limitacion(fj.get("limitacion_principal")), "estado": "TEXTO",
         "codigo": fj.get("limitacion_principal")}]})
    return cards


def texto_van(van, tasa):
    if van is None:
        return None
    t = f" ({_pct(tasa)} anual)" if tasa is not None else ""
    if van > 0:
        return (f"En este escenario el proyecto crearía valor por encima de la tasa de descuento usada{t}: "
                f"VAN = {_fmt_usd(van)}.")
    if van < 0:
        return (f"En este escenario el proyecto NO alcanzaría a pagar la tasa de descuento usada{t}: destruiría "
                f"{_fmt_usd(-van)} de valor.")
    return f"En este escenario el proyecto rinde exactamente la tasa de descuento usada{t}."


def texto_tir(tir, tasa):
    if tir is None:
        return None
    comp = ""
    if tasa is not None:
        comp = " Supera" if tir > tasa else (" No alcanza" if tir < tasa else " Iguala")
        comp += f" la tasa de descuento usada ({_pct(tasa)})."
    return f"Rentabilidad anual implícita del flujo del proyecto en este escenario: {_pct(tir)}.{comp}"


def texto_dscr(dscr):
    if dscr is None:
        return None
    s = (f"En el período más ajustado de este escenario, el flujo disponible cubriría {_num(dscr)} veces el servicio de la "
         "deuda (intereses + amortización).")
    if dscr < 1:
        s += " Menos de 1: en ese período el flujo no alcanzaría para pagar la deuda sin aportes."
    return s


def texto_limitacion(cod):
    if not cod or cod == "—":
        return "Sin limitación principal identificada por el motor en este escenario (no implica que el proyecto esté validado)."
    tipo, _, det = cod.partition(": ")
    txt = {"GATE_FISICO": "Un requisito físico no se cumple", "RESTRICCION_HARD": "Incumple una restricción obligatoria",
           "DATOS_FALTANTES": "Faltan datos para calcular", "RESTRICCION_NO_EVALUABLE": "Una restricción no se pudo evaluar",
           "FACTIBILIDAD_FISICA_PENDIENTE": "Factibilidad física sin confirmar",
           "EVIDENCIA_INSUFICIENTE": "Los números se apoyan en datos de escenario, no en evidencia"}.get(tipo, tipo)
    return f"{txt}: {det}" if det else txt


def texto_objetivo(obj):
    for k, (o, txt) in ES.OBJETIVOS_SIMPLES.items():
        if o == obj:
            return txt
    return obj


def texto_comparabilidad(comparable, no_comp):
    if comparable and not no_comp:
        return "Las alternativas se comparan sobre la misma base (horizonte, tasa, moneda, base fiscal y de flujo)."
    if not comparable:
        return ("No se puede comparar: menos de dos alternativas son comparables (COMPARABILIDAD = FALSE). Una alternativa sin "
                "datos completos o con otra base (tasa, horizonte, fiscal, override total) no entra en rankings: sus "
                "faltantes nunca valen 0.")
    return ("Algunas alternativas quedan fuera de la comparación (COMPARABILIDAD = FALSE): " +
            "; ".join(f"{f['id']}: {f['comparabilidad_motivo']}" for f in no_comp))


def texto_no_invertir(d, fichas):
    """NO_INVERTIR_AUN explicado con las reglas reales del motor (REGLAS_STATUS_QUO), sin presentarlo como fracaso."""
    estado = d.get("ESTADO")
    if d.get("OBJETIVO") == "BALANCEADO" and d.get("PESOS_BALANCEADO") == "PESOS_NO_DEFINIDOS":
        return {"titulo": "PESOS_NO_DEFINIDOS — el objetivo balanceado necesita sus pesos",
                "texto": ("El objetivo BALANCEADO combina rentabilidad, riesgo, capital, liquidez, crecimiento y robustez con "
                          "pesos que debe declarar usted (la app no define pesos ocultos). Sin pesos el motor no puede "
                          "ordenar alternativas: esto NO significa «no invertir». Cargue los pesos o elija otro objetivo."),
                "reglas": [], "por_que": "PESOS_NO_DEFINIDOS", "estado_app": "PESOS_NO_DEFINIDOS"}
    if estado in (mf.NO_DISP_ESC, mr.OPT_REAL_ND):
        return {"titulo": "Resultado no calculable",
                "texto": ("Ninguna alternativa tiene los datos completos para calcular su VAN en este escenario. Esto NO es "
                          "lo mismo que «no invertir»: falta información. Revise qué falta en cada alternativa."),
                "reglas": [], "por_que": d.get("POR_QUE"), "estado_app": "NO_CALCULABLE"}
    reglas = [x.strip() for x in (d.get("REGLA_STATUS_QUO") or "").split(";") if x.strip().startswith("SQ-")]
    return {"titulo": "NO_INVERTIR_AUN — mantener opciones abiertas",
            "texto": ("Bajo las restricciones y datos ingresados, ninguna inversión productiva cumple los criterios dentro de "
                      "este escenario. La regla de decisión del motor indica no comprometer capital todavía: es una "
                      "decisión válida, no un fracaso. Caminos posibles: mantener una estrategia asset-light (C0) si es "
                      "viable, o validar más información (demanda, precios, costos) antes de invertir."),
            "reglas": reglas, "por_que": d.get("POR_QUE"), "nota": d.get("NOTA"),
            "por_que_no_invertir_podria_ganar": d.get("POR_QUE_NO_INVERTIR_PODRIA_GANAR"), "estado_app": "NO_INVERTIR_AUN"}


def explicar_decision(d, fichas):
    if not d:
        return None
    if d.get("ESTADO") != "MEJOR_EN_ESCENARIO":
        return {"estado": d.get("ESTADO"), "no_invertir": texto_no_invertir(d, fichas)}
    best = fichas.get(d["MEJOR"]) or {}
    sec = fichas.get(d.get("SEGUNDA")) or {}
    return {"estado": d["ESTADO"], "decision_escenario": d.get("DECISION_ESCENARIO"),
            "mejor": d["MEJOR"], "segunda": d.get("SEGUNDA"), "metrica": d.get("METRICA"), "sentido": d.get("SENTIDO"),
            "valor_mejor": d.get("VALOR_MEJOR"), "valor_segunda": d.get("VALOR_SEGUNDA"), "diferencia": d.get("DIFERENCIA_VALOR"),
            "por_que_gana": d.get("POR_QUE"), "diferencias": d.get("VARIABLES_QUE_LA_HACEN_GANAR"),
            "que_podria_hacerla_perder": [x for x in (d.get("VARIABLES_QUE_PODRIAN_CAMBIARLA"), d.get("STRESS_QUE_CAMBIA_DECISION"),
                                                      d.get("ROBUSTEZ_DECISION")) if x],
            "restricciones": d.get("RESTRICCIONES_CUMPLE"), "datos_faltantes": d.get("DATOS_FALTANTES_VALIDAR"),
            "evidencia": d.get("EVIDENCIA_GANADORA"), "variables_criticas": d.get("VARIABLES_CRITICAS"),
            "regla_status_quo": d.get("REGLA_STATUS_QUO"), "no_invertir_podria_ganar": d.get("POR_QUE_NO_INVERTIR_PODRIA_GANAR"),
            "no_invertir": texto_no_invertir(d, fichas) if d.get("DECISION_ESCENARIO") == mr.STATUS_QUO else None,
            "semaforo_mejor": best.get("semaforo"), "semaforo_segunda": sec.get("semaforo"),
            "nota": "«Mejor» significa mejor DENTRO DE ESTE ESCENARIO y para este objetivo; no es una recomendación de inversión."}


def por_que(fj, det, opt, U):
    """«¿Por qué me da este resultado?» (#17) con salidas de explicabilidad del motor."""
    aid = fj["id"]
    tor = sorted([t for t in U.get("tornado", []) if t["ALTERNATIVA"] == aid and t.get("RANK")], key=lambda t: t["RANK"])
    ow = [r for r in U.get("oneway", []) if r["ALTERNATIVA"] == aid and r.get("SHOCK") not in (None, 0.0)]
    traza = (det or {}).get("traza") or []
    usados, escenario, pendientes = [], [], []
    for t in traza:
        (escenario if t["ORIGEN"] == "ESCENARIO_USUARIO" else pendientes if t["ORIGEN"] == "PENDIENTE" else usados).append(
            {"variable": t["VARIABLE"], "valor": t["VALOR"], "unidad": t["UNIDAD"], "origen": t["ORIGEN"], "archivo": t["ARCHIVO"],
             "evidencia": t["EVIDENCIA"], "obs": t["OBSERVACIONES"]})
    dec = (opt or {}).get("decision_principal") or {}
    return {"drivers": [{"variable": t["VARIABLE"], "swing_van": t.get("SWING"), "min": t.get("VALOR_MIN"), "max": t.get("VALOR_MAX"),
                         "shock_min": t.get("SHOCK_MIN"), "shock_max": t.get("SHOCK_MAX")} for t in tor[:8]],
            "restricciones": fj.get("restricciones") or [], "datos_motor": usados, "datos_escenario": escenario,
            "datos_pendientes": pendientes,
            "sensibilidades": [{"variable": r["VARIABLE"], "shock": r["SHOCK"], "VAN": r.get("VAN"), "DELTA_VAN": r.get("DELTA_VAN"),
                                "estado": r["ESTADO"]} for r in ow],
            "que_cambiaria": [x for x in (dec.get("VARIABLES_QUE_PODRIAN_CAMBIARLA"), dec.get("STRESS_QUE_CAMBIA_DECISION"),
                                          dec.get("POR_QUE_NO_INVERTIR_PODRIA_GANAR")) if x],
            "segunda": dec.get("SEGUNDA") if dec.get("MEJOR") == aid else None,
            "explicacion_optimizador": (opt or {}).get("explicacion"),
            "nota": "Drivers = amplitud del VAN en la sensibilidad one-way del escenario (perfil de análisis vigente)."}


def que_hacer(fj, det, U):
    """Acciones: si faltan datos, las del motor para cada faltante (accion_de + DPV); si no, las que pueden cambiar la
    decisión según la sensibilidad (prioridad_escenario + que_hacer_ahora)."""
    falt = (det or {}).get("faltantes") or {}
    if falt:
        vistos, out = set(), []
        for item, bloque, refs in mopt._items_faltantes(falt):
            acc, dpv, existe, nueva = mopt.accion_de(item)
            if acc in vistos:
                continue
            vistos.add(acc)
            out.append({"accion": acc, "bloque": bloque, "dpv": dpv, "origen": "FALTANTE_DEL_MOTOR"})
        return out
    prio = U.get("prio_esc") or []
    return [{"accion": r["QUE_HACER_AHORA"], "bloque": r["ITEM"], "dpv": r["DPV_VINCULADOS"], "rank": r["RANK_COMPARTIDO"],
             "empate": r.get("EMPATE"), "razon": r["RAZON"], "origen": "SENSIBILIDAD_DEL_ESCENARIO"}
            for r in mopt.que_hacer_ahora([], prio, 6)] or [
        {"accion": "Validar con evidencia real los datos de escenario usados (precios, demanda, CAPEX, OPEX)",
         "bloque": "EVIDENCIA", "dpv": "", "origen": "COBERTURA_EVIDENCIA"}]


def texto_quiebre(q):
    if q.get("ESTADO") != "ENCONTRADO":
        return {"NO_ENCONTRADO_EN_RANGO": "No hay quiebre dentro del rango evaluado por el motor.",
                "NO_CALCULABLE": "No calculable: " + str(q.get("MOTIVO") or ""),
                "VARIABLE_NO_APLICA": "La variable no aplica a esta alternativa: " + str(q.get("MOTIVO") or "")}.get(q.get("ESTADO"), q.get("ESTADO"))
    s = q["SHOCK_QUIEBRE"]
    if q.get("TIPO_SHOCK") == "RELATIVO":
        return f"El {q['METRICA']} llega a {q['OBJETIVO']:g} con un cambio de {'+' if s > 0 else ''}{_num(s * 100, 1)} % sobre el valor del escenario."
    unidad = {"ABSOLUTO_DIAS": "días", "ABSOLUTO_MESES": "meses"}.get(q.get("TIPO_SHOCK"), q.get("TIPO_SHOCK"))
    return f"El {q['METRICA']} llega a {q['OBJETIVO']:g} con {s:+.1f} {unidad} respecto del escenario.".replace(".", ",", 1)


def mensaje_error_motor(txt):
    """Mensaje de usuario para errores del motor (el detalle técnico va al log)."""
    t = str(txt)
    if mf.OVERRIDE_INCOMPATIBLE in t:
        return ("El CAPEX/OPEX cargado no corresponde a la arquitectura elegida (OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA). "
                "Revise configuración, escala, variante y módulo de cada monto. Detalle: " + t.split(":", 1)[-1].strip()[:400])
    if "TRANSICION_DE_ARQUITECTURA" in t:
        return "El motor no modela el paso de una arquitectura a otra (TRANSICION_DE_ARQUITECTURA_NO_MODELADA)."
    if "tipo de cambio" in t:
        return "Hay un valor en ARS sin tipo de cambio, tipo de TC y fecha (regla 2 del proyecto)."
    if re.search(r"tasa .*tipo|tipo_tasa", t):
        return "Una tasa no declara su tipo (efectiva / nominal / periódica). " + t[:200]
    return "El motor rechazó la entrada: " + t[:400]
