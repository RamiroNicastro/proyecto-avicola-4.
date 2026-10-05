"""Constructores de «ENTENDER EL PROYECTO» (SOLO LECTURA): leen los archivos del estudio y devuelven contenido para la UI.

No se calcula nada económico ni se inventan cifras: las tablas se leen de los CSV/markdown de cada módulo y los textos
de `estudio_contenido.py` resumen las conclusiones ya escritas. Lo que no existe se informa como PENDIENTE.

Fuentes leídas:
  05_proceso_industrial/flujo_proceso.md §2 (etapas), capacidad_proceso.csv (ritmos y flujos por escala)
  08_maquinaria/matriz_equipos.csv (equipos por etapa: referencia técnica, no especificación)
  10_localizacion/regiones_preliminares.md, matriz_localizacion.csv, pesos_localizacion.csv, resultados_localizacion.csv,
      criterios_localizacion.md §4 (gates)
  06_productos/matriz_productos.csv, 07_subproductos/matriz_valorizacion.csv, balance del motor (mf.productos_balance)
  00_gestion_proyecto/arquitecturas_maestras.csv, glosario.md, estado_proyecto.md, completitud_final_motor.csv,
      decisiones_pendientes.md, datos_por_validar.md
  23_plan_expansion/escenarios_escala.csv
  22_riesgos/que_hacer_ahora.csv
"""
import os
import re
import unicodedata
from collections import Counter, OrderedDict

from . import estudio_contenido as C
from . import motor as M
from . import proyecto as PR

ESCALAS = (2500, 5000, 10000, 20000)
AVISO_BENCHMARK = ("Los equipos y capacidades son una REFERENCIA TÉCNICA para estudiar (arquitectura de referencia, "
                   "[SUPUESTO] SUP-065): no son una especificación, ni una cotización, ni una elección de proveedor.")
SIN_GANADORA = "Todavía no existe una ubicación ganadora porque faltan datos de campo."


# ----------------------------------------------------------------------------------------------- utilidades
def _norm(t):
    t = unicodedata.normalize("NFKD", str(t or "").lower())
    t = "".join(ch for ch in t if not unicodedata.combining(ch))
    t = re.sub(r"(\d)\.(\d{3})\b", r"\1\2", t)          # 10.000 → 10000
    return t


def _limpiar(t):
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t or "")
    return t.replace("**", "").replace("`", "").strip()


def _leer(*partes):
    with open(M.ruta(*partes), encoding="utf-8") as fh:
        return fh.read()


def _tabla_md(lineas):
    filas = [l for l in lineas if l.strip().startswith("|")]
    if len(filas) < 2:
        return []
    cab = [_limpiar(c) for c in filas[0].strip().strip("|").split("|")]
    return [dict(zip(cab, [_limpiar(c) for c in l.strip().strip("|").split("|")])) for l in filas[2:]]


def _seccion(texto, inicio, fin_regex=r"^## "):
    lineas = texto.splitlines()
    i = next((k for k, l in enumerate(lineas) if l.startswith(inicio)), None)
    if i is None:
        return []
    out = []
    for l in lineas[i + 1:]:
        if re.match(fin_regex, l):
            break
        out.append(l)
    return out


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def _etiqueta(clasif):
    c = _norm(clasif)
    if "verificado" in c:
        return "VERIFICADO"
    if "pvdp" in c:
        return "PVDP"
    if "estimacion" in c:
        return "ESTIMACION"
    if "supuesto" in c:
        return "SUPUESTO"
    return "PENDIENTE"


_DEC = None


def dec_registro():
    global _DEC
    if _DEC is None:
        reg = {}
        for l in _leer("00_gestion_proyecto", "decisiones_pendientes.md").splitlines():
            if re.match(r"^\| DEC-\d{3} ", l):
                c = [x.strip() for x in l.strip().strip("|").split("|")]
                reg[c[0]] = {"id": c[0], "decision": _limpiar(c[1]), "prioridad": c[2], "estado": c[5] if len(c) > 5 else ""}
        _DEC = reg
    return _DEC


_MODS = {m["id"]: m for m in C.MODULOS}


def _chips(m):
    cnt = Counter(e for _, e in m["que_sabemos"])
    return [{"etiqueta": k, "texto": C.ETIQUETAS_CONFIANZA[k], "n": cnt[k]} for k in C.ETIQUETAS_CONFIANZA if cnt.get(k)]


def _ficha_corta(m):
    return {"id": m["id"], "icono": m["icono"], "titulo": m["titulo"], "resumen": m["resumen"], "grupo": m["grupo"],
            "chips": _chips(m)}


# ----------------------------------------------------------------------------------------------- índice y módulos
# «ESTUDIO COMPLETO»: los 26 temas pedidos, cada uno con el módulo que lo explica (efluentes vive en agua).
ESTUDIO_COMPLETO = [
    ("Mercado", "mercado"), ("Demanda", "demanda"), ("Producción", "produccion"), ("Balance de masa", "balance"),
    ("Productos", "productos"), ("Subproductos", "subproductos"), ("Proceso", "proceso"), ("Maquinaria", "maquinaria"),
    ("Agua", "agua"), ("Efluentes", "agua"), ("Energía", "energia"), ("Frío", "frio"), ("Normativa", "normativa"),
    ("Exportación", "exportacion"), ("Localización", "localizacion"), ("Logística", "logistica"), ("Layout", "layout"),
    ("RRHH", "rrhh"), ("Incubación", "incubacion"), ("Alimento", "alimento"), ("CAPEX", "capex"), ("OPEX", "opex"),
    ("Capital de trabajo", "capital_trabajo"), ("Finanzas", "finanzas"), ("Riesgos", "riesgos"), ("Optimizador", "optimizador"),
]

# Vistas visuales que amplían un módulo (la UI muestra un botón «Ver …»).
VISTAS_MODULO = {"localizacion": ("localizacion", "¿Dónde podría estar la planta?"),
                 "proceso": ("proceso", "¿Qué pasa dentro de la planta?"),
                 "faena": ("proceso", "¿Qué pasa dentro de la planta?"),
                 "maquinaria": ("proceso", "Equipos por etapa"),
                 "productos": ("productos", "¿Qué sale de un pollo?"),
                 "balance": ("productos", "¿Qué sale de un pollo?"),
                 "subproductos": ("productos", "¿Qué sale de un pollo?"),
                 "crecimiento": ("escalas", "¿Qué significa cada escala?"),
                 "capex": ("arquitecturas", "Las 5 arquitecturas"),
                 "optimizador": ("optimizar", "Abrir el optimizador"),
                 "finanzas": ("simular", "Simular un escenario"),
                 "riesgos": ("riesgos", "Probar riesgos (stress)")}


def indice():
    grupos = []
    for gid, (titulo, seccion, texto) in C.GRUPOS.items():
        grupos.append({"id": gid, "titulo": titulo, "seccion": seccion, "texto": texto,
                       "modulos": [_ficha_corta(m) for m in C.MODULOS if m["grupo"] == gid]})
    return {"grupos": grupos,
            "estudio_completo": [{"tema": t, "modulo": mid, "icono": _MODS[mid]["icono"], "titulo": _MODS[mid]["titulo"]}
                                 for t, mid in ESTUDIO_COMPLETO],
            "confianza": C.ETIQUETAS_CONFIANZA,
            "nota": "Resumen en lenguaje simple de las conclusiones de cada módulo. Ninguna cifra del proyecto está "
                    "validada en campo todavía: las etiquetas indican si es una estimación de un modelo, un supuesto, un dato "
                    "externo sin verificar (PVDP) o un pendiente."}


def _completitud_de(carpeta):
    for f in PR.completitud_motor():
        if f.get("CARPETA", "").split("/")[0].split(",")[0].strip() == carpeta or carpeta in f.get("CARPETA", ""):
            return {"modulo": f["MODULO"], "estado_motor": f["ESTADO_MOTOR"], "listo_app": f["LISTO_APP"],
                    "listo_decision_real": f["LISTO_DECISION_REAL"], "precios": f["PRECIOS"], "evidencia": f["EVIDENCIA"]}
    return None


def _titulo_doc(rel):
    try:
        with open(M.ruta(rel), encoding="utf-8") as fh:
            for l in fh:
                if l.startswith("# "):
                    return _limpiar(l[2:])
    except OSError:
        pass
    return os.path.basename(rel)


def modulo(mid):
    m = _MODS.get(mid)
    if not m:
        raise KeyError(mid)
    dpv = PR.dpv_registro()
    dec = dec_registro()
    grupo = C.GRUPOS[m["grupo"]]
    vista = VISTAS_MODULO.get(mid)
    return {"id": mid, "icono": m["icono"], "titulo": m["titulo"], "resumen": m["resumen"],
            "grupo": {"id": m["grupo"], "titulo": grupo[0], "seccion": grupo[1]},
            "preguntas": [
                {"id": "que_es", "titulo": "¿Qué es?", "texto": m["que_es"]},
                {"id": "por_que", "titulo": "¿Por qué importa?", "texto": m["por_que"]},
                {"id": "que_modelamos", "titulo": "¿Qué modelamos?", "texto": m["que_modelamos"]}],
            "que_sabemos": [{"texto": t, "etiqueta": e, "etiqueta_texto": C.ETIQUETAS_CONFIANZA[e]} for t, e in m["que_sabemos"]],
            "que_falta": [{"id": d, "dato": dpv.get(d, {}).get("dato", "(no encontrado en el registro)"),
                           "estado": dpv.get(d, {}).get("estado", "?"), "responsable": dpv.get(d, {}).get("responsable", ""),
                           "por_que": dpv.get(d, {}).get("por_que", "")} for d in m["dpv"]],
            "decisiones": [{"id": d, "decision": dec.get(d, {}).get("decision", "(no encontrada)"),
                            "estado": dec.get(d, {}).get("estado", "?")} for d in m["dec"]],
            "chips": _chips(m),
            "completitud": _completitud_de(m["carpeta"]),
            "vista": {"ruta": vista[0], "texto": vista[1]} if vista else None,
            "detalle_tecnico": {"carpeta": m["carpeta"],
                                "documentos": [{"ruta": d, "titulo": _titulo_doc(d)} for d in m["docs"]],
                                "tablas": m["tablas"]},
            "fuente": "Resumen de las conclusiones del módulo; DPV de 00_gestion_proyecto/datos_por_validar.md; "
                      "DEC de 00_gestion_proyecto/decisiones_pendientes.md."}


def documento_estudio(rel):
    """Markdown de un documento del estudio para «VER DETALLE TÉCNICO» (solo los listados en algún módulo)."""
    permitidos = {d for m in C.MODULOS for d in m["docs"]}
    if rel not in permitidos:
        raise KeyError(rel)
    return {"ruta": rel, "titulo": _titulo_doc(rel), "texto": _leer(rel)}


# ----------------------------------------------------------------------------------------------- cadena
def cadena():
    nodos = []
    for nid, titulo, texto, mid in C.CADENA:
        m = _MODS[mid]
        nodos.append({"id": nid, "titulo": titulo, "texto": texto, "modulo": mid, "modulo_titulo": m["titulo"], "icono": m["icono"],
                      "numeros": [{"texto": t, "etiqueta": e} for t, e in m["que_sabemos"] if e != "PENDIENTE"][:3]})
    ramas = []
    for rid, titulo, texto, mid, padre in C.RAMAS:
        m = _MODS[mid]
        ramas.append({"id": rid, "titulo": titulo, "texto": texto, "modulo": mid, "padre": padre, "icono": m["icono"],
                      "numeros": [{"texto": t, "etiqueta": e} for t, e in m["que_sabemos"] if e != "PENDIENTE"][:3]})
    return {"nodos": nodos, "ramas": ramas,
            "nota": "Los números son los ya calculados por los módulos del estudio (con su etiqueta). Hacé clic en un bloque "
                    "para ver qué es y abrir el módulo."}


# ----------------------------------------------------------------------------------------------- localización
CRITERIOS_LOC = OrderedDict([
    ("DEMANDA", ("Cercanía comercial", "Distancia y tiempo al mercado principal (AMBA) y a los clientes.")),
    ("ECOSISTEMA_AVICOLA", ("Acceso a productores", "Productores integrables, incubadoras y servicios avícolas cerca.")),
    ("EXPOSICION_SANITARIA", ("Exposición sanitaria", "Distancia entre granjas, movimientos de aves, eventos de influenza.")),
    ("CLIMA", ("Clima", "Estrés térmico para las aves y para la operación.")),
    ("ALIMENTO", ("Alimento y granos", "Maíz, molienda de soja y fábricas de alimento cerca.")),
    ("FAENA_INDUSTRIA", ("Industria y façon", "Frigoríficos y capacidad a façon en la región.")),
    ("AGUA", ("Agua", "Disponibilidad y calidad del agua.")),
    ("EFLUENTES", ("Efluentes", "Dónde y cómo se puede volcar o tratar el agua usada.")),
    ("ENERGIA", ("Energía", "Red eléctrica, potencia y gas.")),
    ("LOGISTICA", ("Logística", "Rutas, accesos y transporte.")),
    ("EXPORTACION", ("Puertos y exportación", "Nodos portuarios con servicio refrigerado verificado.")),
    ("TERRENO", ("Terreno", "Precio, riesgo hídrico, parques industriales.")),
    ("NORMATIVA", ("Normativa local", "Presión urbana, zonificación y plazos ambientales.")),
    ("RRHH", ("Personas", "Mano de obra disponible.")),
    ("TRADE_OFF", ("Compensaciones (sin puntaje)", "Variables de doble efecto: se analizan cualitativamente.")),
    ("NETWORK", ("Red (sin puntaje)", "Arquitectura de red: una planta o planta + centro de distribución.")),
])


def localizacion():
    txt = _leer("10_localizacion", "regiones_preliminares.md")
    lineas = txt.splitlines()
    tablas, actual = [], []
    for l in lineas:
        if l.strip().startswith("|"):
            actual.append(l)
        elif actual:
            tablas.append(_tabla_md(actual))
            actual = []
    if actual:
        tablas.append(_tabla_md(actual))
    regiones = next((t for t in tablas if t and "Código" in t[0]), [])
    logicas = next((t for t in tablas if t and "Región" in t[0] and "Qué gana" in t[0]), [])
    por_region_logica = {}
    for f in logicas:
        for cod in re.findall(r"[A-Z]{2,3}-[A-Z]+", f.get("Región", "")):
            por_region_logica[cod] = f
    celdas = M.leer_csv(M.ruta("10_localizacion", "matriz_localizacion.csv"))
    estado_celdas = Counter((c["ESTADO"] or "SIN_DATO") if c["VALOR"] not in ("", None) else "SIN_DATO" for c in celdas)
    por_reg = {}
    for c in celdas:
        d = por_reg.setdefault(c["REGION"], Counter())
        d["total"] += 1
        if c["VALOR"] not in ("", None):
            d["con_dato"] += 1
    criterios = []
    for cid, (titulo, texto) in CRITERIOS_LOC.items():
        sub = [c for c in celdas if c["CRITERIO"] == cid]
        nombres = list(OrderedDict.fromkeys(c["NOMBRE_SUBCRITERIO"] for c in sub))
        criterios.append({"id": cid, "titulo": titulo, "texto": texto, "subcriterios": nombres,
                          "celdas": len(sub), "con_dato": sum(1 for c in sub if c["VALOR"] not in ("", None))})
    out_reg = []
    for r in regiones:
        cod = r.get("Código")
        km = _num(re.sub(r"[^\d]", "", r.get("km a CABA (orden)", "")) or None)
        lg = por_region_logica.get(cod, {})
        cnt = por_reg.get(cod, Counter())
        out_reg.append({"codigo": cod, "provincia": r.get("Provincia"), "corredor": r.get("Corredor"),
                        "centro": r.get("Centro de referencia"), "km_caba_orden": km, "logica": r.get("Lógica de la región"),
                        "que_gana": lg.get("Qué gana"), "que_arriesga": lg.get("Qué arriesga"),
                        "preguntas": lg.get("Preguntas que la decidirían"),
                        "celdas": cnt.get("total", 0), "con_dato": cnt.get("con_dato", 0)})
    gates = []
    for f in _tabla_md(_seccion(_leer("10_localizacion", "criterios_localizacion.md"), "## 4.")):
        if f.get("ID", "").startswith("G-"):
            gates.append({"id": f["ID"], "tipo": "DURO" if f["ID"].startswith("G-D") else "CONDICIONAL", "gate": f.get("Gate"),
                          "detalle": f.get("Cuándo es duro / cómo se resuelve si es condicional")})
    perfiles = OrderedDict()
    for p in M.leer_csv(M.ruta("10_localizacion", "pesos_localizacion.csv")):
        perfiles.setdefault(p["PERFIL"], {"id": p["PERFIL"], "nombre": p["NOMBRE_PERFIL"], "pesos": []})["pesos"].append(
            {"criterio": CRITERIOS_LOC.get(p["CRITERIO"], (p["CRITERIO"],))[0], "peso": _num(p["PESO"])})
    res = M.leer_csv(M.ruta("10_localizacion", "resultados_localizacion.csv"))
    emitidos = sum(1 for r in res if r.get("ESTADO_RANKING") != "NO_EMITIDO")
    cob = [_num(r.get("COBERTURA_DE_INFORMACION")) for r in res if _num(r.get("COBERTURA_DE_INFORMACION")) is not None]
    return {"mensaje": SIN_GANADORA, "regiones": out_reg, "criterios": criterios, "gates": gates, "perfiles": list(perfiles.values()),
            "celdas": {"total": len(celdas), "por_estado": dict(estado_celdas),
                       "por_tipo": dict(Counter((c["TIPO_EVIDENCIA"] or "SIN_DATO") if c["VALOR"] not in ("", None) else "SIN_DATO"
                                                for c in celdas)),
                       "verificadas": sum(1 for c in celdas if "VERIFICADO" in (c["ESTADO"] or "").upper())},
            "ranking": {"emitidos": emitidos, "filas": len(res), "estado": "NO_EMITIDO" if emitidos == 0 else "EMITIDO",
                        "cobertura_max": max(cob) if cob else None},
            "nota_km": "Distancia a CABA = orden de magnitud NO medido (SUP-079; medir con ruteo, DPV-116). Sirve para ubicar "
                       "las regiones en un esquema, no como dato ni como puntaje.",
            "nota_gates": "Los gates se aplican a un municipio o terreno concreto, nunca eliminan una región completa. "
                          "Un gate duro solo cuenta con imposibilidad demostrada por escrito.",
            "nota_perfiles": "Perfiles de ponderación ILUSTRATIVOS (SUP-080): ninguno es el recomendado. Los pesos son una "
                             "decisión estratégica (DEC-051).",
            "puertos": "Cercanía a puerto ≠ servicio refrigerado disponible ≠ exportación habilitada (DPV-125).",
            "fuentes": ["10_localizacion/regiones_preliminares.md", "10_localizacion/matriz_localizacion.csv",
                        "10_localizacion/criterios_localizacion.md", "10_localizacion/resultados_localizacion.csv"],
            "dpv": [d for d in _MODS["localizacion"]["dpv"]]}


# ----------------------------------------------------------------------------------------------- proceso
def _rango(etq):
    """'E04–E10' / 'E01;E03' / 'E10/E16' / 'E12–E13' → {4..10} …  (códigos X/Z → set vacío)."""
    out = set()
    for parte in re.split(r"[;/,]", etq or ""):
        nums = re.findall(r"E(\d+)", parte)
        if len(nums) == 2 and re.search(r"[–-]", parte):
            out |= set(range(int(nums[0]), int(nums[1]) + 1))
        else:
            out |= {int(n) for n in nums}
    return out


def _cap(escala):
    filas = M.leer_csv(M.ruta("05_proceso_industrial", "capacidad_proceso.csv"))
    d = {}
    for f in filas:
        if f["escala_aves_dia"] != str(escala) or f["horas_netas"] not in ("8", ""):
            continue
        d[(f["variable"], f["parametro"])] = (_num(f["valor"]), f["unidad"], _etiqueta(f["clasificacion"]))
    return d


def _v(cap, var, par, texto):
    x = cap.get((var, par))
    if not x or x[0] is None:
        return None
    return {"texto": texto, "valor": x[0], "unidad": x[1], "etiqueta": x[2]}


def _capacidad_etapa(n, cap):
    v = []
    if 1 <= n <= 11:
        v += [_v(cap, "ritmo_operativo_requerido", "", "Ritmo de línea (8 h netas)"),
              _v(cap, "peso_vivo_kg_h", "config=B", "Peso vivo que entra por hora")]
    if n == 4:
        v += [_v(cap, "puestos_equivalentes", "colgado;referencia", "Puestos de colgado (referencia)"),
              _v(cap, "puestos_equivalentes", "colgado;prudente", "Puestos de colgado (prudente)")]
    if 12 <= n <= 17:
        v += [_v(cap, "carcasa_pre_chiller_kg_h", "config=B", "Carcasas que salen de evisceración"),
              _v(cap, "puestos_equivalentes", "eviscerado_manual;referencia", "Puestos si se eviscera a mano (referencia)")]
    if n in (18, 19):
        v += [_v(cap, "carcasas_simultaneas_en_enfriamiento", "residencia=inmersion", "Carcasas a la vez en enfriamiento por inmersión"),
              _v(cap, "carcasas_simultaneas_en_enfriamiento", "residencia=aire_min", "Carcasas a la vez en enfriamiento por aire (mín.)")]
    if n == 20:
        v += [_v(cap, "carcasa_pre_chiller_kg_h", "config=B", "Carcasas que llegan a clasificar (antes del agua del enfriamiento)")]
    if 21 <= n <= 23:
        v += [_v(cap, "a_trozado_kg_h", "config=B", "Kilos a trozar por hora (mix trozado)"),
              _v(cap, "a_deshuese_kg_h", "config=C", "Kilos a deshuesar por hora (mix deshuesado)")]
    if 24 <= n <= 26:
        v += [_v(cap, "comestible_a_empaque_kg_h", "config=B", "Producto a empacar por hora")]
    if 27 <= n <= 29:
        v += [_v(cap, "comestible_a_congelar_t_dia", "perfil=P1;config=B", "A congelar por día — perfil P1 (poco congelado)"),
              _v(cap, "comestible_a_congelar_t_dia", "perfil=P3;config=B", "A congelar por día — perfil P3 (mucho congelado)")]
    if n == 30:
        v += [_v(cap, "garras_a_y_segunda_kg_h", "config=B", "Garras por hora")]
    if n == 31:
        v += [_v(cap, "menudencias_y_cuello_kg_h", "config=B", "Menudencias y cuello por hora")]
    if n == 32:
        v += [_v(cap, "a_cms_kg_h", "config=C", "A CMS por hora (si se hace CMS)")]
    return [x for x in v if x]


SERVICIOS_TXT = {"elec": "electricidad", "agua": "agua", "agua_caliente": "agua caliente", "agua_helada": "agua helada",
                 "agua_helada/hielo": "agua helada / hielo", "frío": "frío", "aire": "aire comprimido", "vacío": "vacío",
                 "gas": "gas", "gasoil": "gasoil", "gas MAP": "gas para envase", "gas criogénico": "gas criogénico"}


def proceso(escala=10000):
    escala = int(escala) if str(escala).isdigit() and int(escala) in ESCALAS else 10000
    txt = _leer("05_proceso_industrial", "flujo_proceso.md")
    filas = _tabla_md(_seccion(txt, "## 2."))
    equipos = M.leer_csv(M.ruta("08_maquinaria", "matriz_equipos.csv"))
    cap = _cap(escala)
    etapas = []
    for f in filas:
        cod = f.get("#", "")
        nums = _rango(cod)
        if not nums:
            continue
        eqs = [e for e in equipos if _rango(e["etapas"]) & nums]
        serv = OrderedDict()
        for e in eqs:
            for s in e["servicios"].split(";"):
                s = s.strip()
                if s and s != "—":
                    base = s.split(" (")[0]
                    serv[SERVICIOS_TXT.get(base, base)] = True
        texto_fila = " ".join(f.values())
        pend = sorted(set(re.findall(r"(?:DPV|DEC)-\d{3}", texto_fila + " " + " ".join(e["nota"] for e in eqs))))
        etapas.append({"codigo": cod, "n": min(nums), "nombre": f.get("Etapa"), "que_pasa": f.get("Función"),
                       "controlar": f.get("Qué hay que controlar (cualitativo)"), "riesgo": f.get("Riesgo si falla"),
                       "salida_lateral": f.get("Salida lateral (kg/ave)"),
                       "equipos": [{"id": e["id"], "equipo": e["equipo"], "funcion": e["funcion"], "criticidad": e["criticidad"],
                                    "nivel": e[f"nivel_{escala}"], "alternativas": e["alternativas"],
                                    "clasificacion": _etiqueta(e["clasificacion"])} for e in eqs],
                       "servicios": list(serv.keys()), "capacidad": _capacidad_etapa(min(nums), cap), "pendiente": pend})
    laterales = [{"variable": t, "valor": cap.get((v, "config=B"), (None,))[0], "unidad": "kg/h", "etiqueta": "ESTIMACION"}
                 for v, t in (("sangre_recuperada_kg_h", "Sangre recuperada"), ("plumas_humedas_kg_h", "Plumas húmedas"),
                              ("visceras_no_comestibles_kg_h", "Vísceras no comestibles"), ("cabezas_kg_h", "Cabezas"),
                              ("rendering_potencial_kg_h", "Material que podría ir a rendering"))]
    return {"escala": escala, "escalas": list(ESCALAS), "etapas": etapas, "laterales": [l for l in laterales if l["valor"] is not None],
            "aviso": AVISO_BENCHMARK,
            "niveles": {"M": "Manual", "Mc": "Mecanizado", "S": "Semiautomático", "A": "Automático",
                        "nota": "Nivel de automatización de referencia a estudiar para esa escala (estudio de maquinaria, automatización por escala); "
                                "no es una obligación técnica ni normativa."},
            "utilities_planta": _utilities(escala),
            "base": "Capacidades con 8 h netas de faena por día operativo y mix de productos B (trozado), salvo que se indique. "
                    "Ritmo = aves/día ÷ horas netas: es lo que la línea tiene que procesar, no la capacidad de una máquina.",
            "fuentes": ["05_proceso_industrial/flujo_proceso.md", "05_proceso_industrial/capacidad_proceso.csv",
                        "08_maquinaria/matriz_equipos.csv"]}


# Cifras por escala citadas de las conclusiones (orden 2.500 / 5.000 / 10.000 / 20.000; escenario medio).
_POR_ESCALA = {
    "agua_m3_dia": ((62, 125, 250, 500), "m³/día", "ESTIMACION", "11_agua_efluentes/conclusiones_agua_efluentes.md",
                    "Agua usada por la planta (medio, 25 L/ave)"),
    "energia_kwh_dia": ((2046, 4092, 8184, 16368), "kWh/día operativo", "ESTIMACION", "12_energia_frio/conclusiones_energia_frio.md",
                        "Energía eléctrica por día (sensibilidad ~0,8 kWh/ave)"),
    "construidos_m2": ((1780, 2600, 4310, 7450), "m² construidos", "ESTIMACION", "09_layout_obra_civil/conclusiones_layout.md",
                       "Superficie construida de la planta (medio; rango de ~2–3 veces)"),
    "terreno_ha": ((2.0, 2.3, 3.1, 4.4), "ha", "ESTIMACION", "09_layout_obra_civil/conclusiones_layout.md",
                   "Terreno conceptual (medio, sin reservar escala futura; orden de magnitud)"),
    "fte": ((55, 77, 99, 126), "FTE internos", "ESTIMACION", "18_recursos_humanos/conclusiones_rrhh.md",
            "Carga de trabajo interna (FTE, no personas en nómina)"),
    "demanda_t_dia": ((4.1, 8.2, 16.4, 32.8), "t/día calendario", "ESTIMACION", "23_plan_expansion/conclusiones_escala.md",
                      "Demanda necesaria para vender toda la producción (cota inferior, vendiendo el ave completa)"),
}


def _utilities(escala):
    i = ESCALAS.index(escala)
    return [{"id": k, "texto": t, "valor": v[i], "unidad": u, "etiqueta": e, "fuente": f}
            for k, (v, u, e, f, t) in _POR_ESCALA.items() if k in ("agua_m3_dia", "energia_kwh_dia")]


# ----------------------------------------------------------------------------------------------- escalas
def escalas():
    filas = M.leer_csv(M.ruta("23_plan_expansion", "escenarios_escala.csv"))
    sel = {e: {} for e in ESCALAS}
    camiones = {e: [] for e in ESCALAS}
    for f in filas:
        try:
            e = int(f["escala_aves_dia"])
        except ValueError:
            continue
        if e not in sel or f["dias_semana"] != "5":
            continue
        par, var = f["parametro"], f["variable"]
        if var == "camiones_aves_vivas_dia":
            camiones[e].append({"parametro": par, "valor": _num(f["valor"]), "etiqueta": _etiqueta(f["clasificacion"])})
            continue
        ok = (par == "" or par == "perfil=medio; desempeno=medio" or par == "config=B; peso=2.9" or par == "horas_netas=8")
        if ok:
            sel[e][(var, f["periodo"])] = (_num(f["valor"]), f["unidad"], _etiqueta(f["clasificacion"]))
    filas_out = [
        ("aves_dia", "Aves faenadas por día de planta", ("escala_aves_faenadas_dia_operativo", "dia_operativo")),
        ("aves_anio", "Aves por año (250 días operativos)", ("aves_faenadas_anio_plena_escala", "anio")),
        ("ritmo", "Aves por hora (8 h netas)", ("aves_por_hora_neta", "hora")),
        ("comestible_anio", "Producto comestible por año", ("comestible_t", "anio")),
        ("comestible_dia", "Producto comestible por día de planta", ("comestible_t", "dia_operativo")),
        ("pollitos_semana", "Pollitos BB por semana (plena)", ("pollitos_bb_semana_plena", "semana_plena")),
        ("pollitos_anio", "Pollitos BB por año", ("pollitos_bb_anio", "anio")),
        ("alimento_anio", "Alimento por año", ("alimento_t_anio", "anio")),
        ("galpones_m2", "Superficie de galpones", ("m2_galpones", "stock")),
        ("galpones_eq", "Galpones equivalentes de 2.400 m²", ("galpones_equivalentes_2400m2", "stock")),
        ("subproductos_dia", "Subproductos sólidos que salen por día", ("subproductos_solidos_salen_t_dia", "dia_operativo")),
    ]
    tabla = []
    for fid, texto, clave in filas_out:
        vals = [sel[e].get(clave) for e in ESCALAS]
        tabla.append({"id": fid, "texto": texto, "valores": [v[0] if v else None for v in vals],
                      "unidad": next((v[1] for v in vals if v), ""), "etiqueta": next((v[2] for v in vals if v), "PENDIENTE"),
                      "fuente": "23_plan_expansion/escenarios_escala.csv"})
    for k, (v, u, e, f, t) in _POR_ESCALA.items():
        tabla.append({"id": k, "texto": t, "valores": list(v), "unidad": u, "etiqueta": e, "fuente": f})
    cam = []
    for e in ESCALAS:
        cam.append(sorted(camiones[e], key=lambda x: x["parametro"]))
    return {"escalas": list(ESCALAS), "filas": tabla, "camiones": cam,
            "aviso": "Capacidad no significa que vayamos a vender todo.",
            "base": "Escenario medio (perfil y desempeño medios), 5 días de faena por semana (250 días/año), mix B (trozado), "
                    "peso vivo 2,9 kg. Son cifras de los modelos del estudio, no datos de campo.",
            "nota": "Ninguna escala está elegida (DEC-001, DEC-033). La escala es la capacidad de la planta: si la demanda real "
                    "es menor, la planta trabaja con capacidad ociosa.",
            "fuentes": sorted({r["fuente"] for r in tabla})}


# ----------------------------------------------------------------------------------------------- productos
def productos():
    prods, meta = M.productos()
    val = M.leer_csv(M.ruta("07_subproductos", "matriz_valorizacion.csv"))
    clases = {"A": "Producto principal", "B": "Coproducto comestible", "C": "Subproducto valorizable (si hay comprador o proceso)",
              "D": "Residuo / efluente (costo de tratamiento)", "P": "Pérdidas no asignadas"}
    mats = []
    for v in val:
        if v["kg_ave"] in ("", "-"):
            continue
        mats.append({"id": v["id"], "material": v["material"], "kg_ave": _num(v["kg_ave"]), "base": v["base_kg"],
                     "pct_peso_vivo": _num(v["pct_peso_vivo"]), "configuracion": v["config_origen"],
                     "clase": v["clase_con_comprador"], "clase_sin_comprador": v["clase_sin_comprador"],
                     "rutas": [r for r in (v["ruta_1"], v["ruta_2"], v["ruta_3"]) if r and r != "—"],
                     "incompatible": v["rutas_incompatibles"] if v["rutas_incompatibles"] not in ("—", "") else None,
                     "mercado": v["mercado"], "nivel_valor": v["nivel_valor_con_comprador"], "dpv_precio": v["dato_precio_pendiente"]})
    rutas = [
        {"id": "A", "titulo": "Ruta A — pollo entero", "texto": "Se vende el ave entera (con o sin menudencias)."},
        {"id": "B", "titulo": "Ruta B — trozado", "texto": "Se corta en pechuga, pata-muslo, alas, carcasa…"},
        {"id": "C", "titulo": "Ruta C — deshuesado", "texto": "Se deshuesa: suprema, solomillo, muslo deshuesado, piel, recortes, hueso."},
    ]
    return {"balance_motor": prods, "balance_meta": {k: v for k, v in (meta or {}).items() if isinstance(v, (str, int, float))},
            "materiales": mats, "clases": clases, "rutas": rutas,
            "aviso_rutas": "Las rutas son ALTERNATIVAS para el mismo kilo: un kilo de pechuga se vende con hueso O deshuesado, "
                           "la carcasa se vende O va a CMS O a rendering. Por eso los kg/ave de rutas distintas NO se suman.",
            "aviso_clase": "La clase supone que existe un comprador o un proceso habilitado; sin comprador, la salida baja de clase "
                           "(SUP-046). Ningún subproducto es ingreso sin comprador identificado.",
            "base": "kg por ave de 2,9 kg de peso vivo (balance de masa v1.1, masa biológica salvo plumas húmedas y agua). "
                    "La lista «del motor» es el mix B (trozado) que usa el modelo financiero.",
            "fuentes": ["04_balance_masa", "07_subproductos/matriz_valorizacion.csv", "06_productos/matriz_productos.csv"]}


# ----------------------------------------------------------------------------------------------- arquitecturas
NOMBRES_ARQ = {"C0": "ARRANQUE ASSET-LIGHT", "C1": "PLANTA DE FAENA PROPIA", "C2": "INTEGRACIÓN SELECTIVA",
               "C3": "MAYOR INTEGRACIÓN", "CF": "ARQUITECTURA FUTURA"}
DIMS_ARQ = [("FAENA", "Faena"), ("GRANJAS", "Granjas"), ("POLLITO", "Pollitos"), ("ALIMENTO", "Alimento"), ("FLOTA", "Flota"),
            ("FRIO", "Frío"), ("SUBPRODUCTOS", "Subproductos"), ("RENDERING", "Rendering"),
            ("UPSTREAM_REPRODUCTORAS", "Reproductoras")]


def clasificar_dim(texto):
    t = _norm(texto)
    if "futuro" in t:
        return "FUTURO"
    if t.startswith("false"):
        return "NO TIENE"
    if t.startswith("mixto"):
        return "MIXTO"
    if t.startswith(("propia", "propias", "incubacion", "a_refrigerado", "b_refrigerado", "b_basico")):
        return "PROPIO"
    if t.startswith(("facon", "compra", "tercero", "integradas", "a_externo", "c_congelado")):
        return "TERCERIZADO"
    return "VER DEFINICIÓN"


def arquitecturas():
    filas = [r for r in M.leer_csv(M.ruta("00_gestion_proyecto", "arquitecturas_maestras.csv")) if r["TIPO"] == "CONFIGURACION_BASE"]
    out = []
    for r in filas:
        cfg = r["CONFIGURACION"]
        out.append({"id": cfg, "nombre": NOMBRES_ARQ.get(cfg, cfg), "titulo": M.EXPLICACION_CONFIG.get(cfg, ("", ""))[0],
                    "explicacion": M.EXPLICACION_CONFIG.get(cfg, ("", ""))[1], "estado": r["ESTADO"],
                    "dimensiones": [{"id": k, "titulo": t, "clase": clasificar_dim(r[k]), "definicion": r[k]} for k, t in DIMS_ARQ],
                    "upstream": r["UPSTREAM"]})
    return {"arquitecturas": out,
            "leyenda": {"PROPIO": "La empresa lo tiene y lo opera.", "TERCERIZADO": "Lo hace un tercero (compra, façon, integrados, flete).",
                        "MIXTO": "Una parte propia y otra de terceros.", "FUTURO": "Previsto para más adelante; no suma a la inversión inicial.",
                        "NO TIENE": "No forma parte de esta arquitectura."},
            "nota": "Definiciones exactas de 00_gestion_proyecto/arquitecturas_maestras.csv (se muestran debajo de cada casilla). "
                    "Ninguna arquitectura está recomendada ni es costeable hoy.",
            "fuente": "00_gestion_proyecto/arquitecturas_maestras.csv"}


# ----------------------------------------------------------------------------------------------- glosario
def glosario():
    terminos = []
    for l in _leer("00_gestion_proyecto", "glosario.md").splitlines():
        if l.startswith("| ") and not l.startswith("| Término") and not l.startswith("|---"):
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) >= 2 and c[0]:
                terminos.append({"termino": _limpiar(c[0]), "definicion": _limpiar(c[1]), "origen": "GLOSARIO"})
    vistos = {_norm(t["termino"]) for t in terminos}
    for k, v in C.AYUDAS.items():
        if _norm(k) not in vistos:
            terminos.append({"termino": k, "definicion": v, "origen": "AYUDA_APP"})
    terminos.sort(key=lambda t: _norm(t["termino"]))
    return {"terminos": terminos, "ayudas": C.AYUDAS,
            "fuente": "00_gestion_proyecto/glosario.md (+ ayudas breves de la app)"}


# ----------------------------------------------------------------------------------------------- estado del proyecto
def estado_proyecto():
    txt = _leer("00_gestion_proyecto", "estado_proyecto.md")
    tablero = _tabla_md(_seccion(txt, "## Tablero de estado"))
    comp = PR.completitud_motor()
    prog = PR.progreso()
    reg = PR.dpv_registro()
    evi = PR.evidencia()
    n_val = sum(1 for d in reg.values() if d["estado"].lower().startswith("validad"))
    terminado = [{"modulo": t.get("Módulo"), "texto": t.get("Modelo preliminar")} for t in tablero
                 if re.search(r"complet|construid", _norm(t.get("Modelo preliminar", "")))]
    pendiente = [{"modulo": t.get("Módulo"), "texto": t.get("Evidencia de campo") or t.get("Modelo preliminar")} for t in tablero
                 if re.search(r"pendiente", _norm(t.get("Evidencia de campo", "") + " " + t.get("Modelo preliminar", "")))]
    return {
        "intro": "Hoy el motor está construido, pero los datos reales todavía no están validados.",
        "semaforo": [
            {"id": "MOTOR", "titulo": "Motor", "estado": "COMPLETO", "icono": "✅", "texto": "Todos los modelos 03–22 están construidos y probados."},
            {"id": "FISICOS", "titulo": "Datos físicos", "estado": "PARCIALES", "icono": "⚠", "texto": "Cantidades calculadas por los modelos, sin validar en campo."},
            {"id": "ECONOMICOS", "titulo": "Datos económicos", "estado": "MUY INCOMPLETOS", "icono": "⚠", "texto": "Casi no hay precios, cotizaciones ni costos reales."},
            {"id": "EVIDENCIA", "titulo": "Evidencia", "estado": f"{round(100 * n_val / max(len(reg), 1))} %", "icono": "○",
             "texto": f"{n_val} de {len(reg)} datos por validar están validados."},
            {"id": "DECISION", "titulo": "Decisión real", "estado": "NO DISPONIBLE", "icono": "⛔",
             "texto": f"{evi['publicables'].get('PUBLICABLE_VAN', 0)} de {evi['corridas_evidencia']} corridas con datos reales tienen VAN publicable."}],
        "terminado": terminado, "pendiente": pendiente,
        "se_puede_simular": ["Escenarios hipotéticos con tus propios precios, costos y demanda (rotulados SIMULACIÓN).",
                             "Comparar arquitecturas C0–CF y escalas dentro de un escenario.",
                             "Probar riesgos: qué pasa si sube el alimento o baja el precio.",
                             "La demostración con datos ficticios (DEMO), para aprender a usar la app."],
        "no_se_puede_decidir": ["Si conviene o no invertir: no hay precios, costos ni demanda reales (0 corridas publicables).",
                                "Qué arquitectura o escala elegir (DEC-001, DEC-033 abiertas).",
                                "Dónde ubicar la planta: no hay ranking de regiones (0 de 624 celdas verificadas).",
                                "Cuánto capital hace falta: CAPEX y OPEX no costeables con evidencia."],
        "tablero": tablero, "completitud": comp, "progreso": prog,
        "dpv": {"total": len(reg), "validados": n_val},
        "fuentes": ["00_gestion_proyecto/estado_proyecto.md", "00_gestion_proyecto/completitud_final_motor.csv",
                    "00_gestion_proyecto/datos_por_validar.md"]}


# ----------------------------------------------------------------------------------------------- qué hacer ahora
def que_hacer_agrupado():
    """«PARA SEGUIR AVANZANDO»: la prioridad de validación del motor agrupada por puesto compartido (empates intactos)."""
    filas = [f for f in M.leer_csv(M.ruta("22_riesgos", "prioridad_validacion.csv")) if f.get("UNIVERSO") == "EVIDENCIA"]
    filas.sort(key=lambda f: (int(f["RANK_COMPARTIDO"]) if (f.get("RANK_COMPARTIDO") or "").isdigit() else 999,
                              int(f["ORDEN_DENTRO_DEL_EMPATE"]) if (f.get("ORDEN_DENTRO_DEL_EMPATE") or "").isdigit() else 0))
    grupos = OrderedDict()
    for f in filas:
        rank = f.get("RANK_COMPARTIDO") or "?"
        g = grupos.setdefault(rank, {"rank": rank, "items": [], "nota_empate": f.get("EMPATE", "")})
        g["items"].append({"accion": f.get("ACCION"), "ambito": f.get("AMBITO"), "bloque": f.get("BLOQUE"),
                           "item": (f.get("ITEM") or "").split(":", 1)[-1].strip(),
                           "razon": f"bloquea {f.get('INDICADORES_BLOQUEADOS')} indicadores en {f.get('N_ALTERNATIVAS_BLOQUEADAS')} de "
                                    f"{f.get('N_ALTERNATIVAS')} alternativas",
                           "dpv": [d.strip() for d in (f.get("DPV_VINCULADOS") or "").split(",") if d.strip().startswith("DPV")]})
    out = []
    for n, g in enumerate(grupos.values(), 1):
        g["empate"] = len(g["items"]) > 1
        g["titulo"] = f"PRIORIDAD {g['rank']}" + (f" — EMPATE ({len(g['items'])} ítems)" if g["empate"] else "")
        g["puesto_motor"] = g["rank"]
        out.append(g)
    return {"grupos": out,
            "nota": "Prioridad derivada del motor: primero lo que bloquea más resultados. Los empates se muestran como empates: "
                    "la app no inventa un orden dentro de cada grupo (POTENCIAL_DE_CAMBIAR_DECISION = NO_CALCULADO).",
            "fuente": "22_riesgos/prioridad_validacion.csv"}


# ----------------------------------------------------------------------------------------------- búsqueda
# Destinos fijos (vistas) con palabras clave; prioridad alta para que los atajos naturales lleven a la vista visual.
VISTAS = [
    ("localizacion", "¿Dónde podría estar la planta?", "Regiones, criterios, gates y estado de la información.",
     "localizacion ubicacion donde region regiones provincia mapa terreno gates buenos aires entre rios santa fe cordoba chaco puerto"),
    ("proceso", "¿Qué pasa dentro de la planta?", "Etapas del frigorífico, equipos, capacidad y riesgos.",
     "faena proceso planta frigorifico etapas maquinaria equipos linea enfriamiento eviscerado trozado empaque chiller"),
    ("productos", "¿Qué sale de un pollo?", "Partes del ave en kg por ave y sus destinos.",
     "productos partes pollo pechuga pata muslo alas garras menudencias subproductos rendering cms kg ave balance"),
    ("escalas", "¿Qué significa cada escala?", "2.500 / 5.000 / 10.000 / 20.000 aves por día.",
     "escala escalas 2500 5000 10000 20000 aves por dia capacidad tamaño"),
    ("arquitecturas", "Las 5 arquitecturas", "C0 a CF: qué es propio y qué tercerizado.",
     "arquitectura arquitecturas c0 c1 c2 c3 cf asset light integracion propio tercerizado facon"),
    ("como-funciona", "¿Cómo funciona el negocio?", "La cadena del huevo al cliente.",
     "cadena negocio como funciona huevo pollito cliente"),
    ("estado", "¿Dónde estamos parados?", "Qué está terminado, qué falta y qué se puede decidir.",
     "estado avance donde estamos terminado pendiente progreso"),
    ("seguir", "Para seguir avanzando", "Qué hacer ahora, por prioridad.",
     "que hacer ahora proximos pasos prioridad avanzar"),
    ("validacion", "Qué falta validar", "Checklist de datos a pedir por paquete.",
     "validar validacion checklist dpv datos faltantes pedir campo"),
    ("simular", "Simular un escenario", "Cargar tus datos y ver un resultado rotulado.",
     "simular escenario simulacion calcular resultado van tir"),
    ("comparar", "Comparar alternativas", "Comparar arquitecturas y escalas lado a lado.", "comparar comparacion"),
    ("optimizar", "Optimizar", "Buscar la alternativa que mejor cumple tu objetivo.", "optimizar optimizador mejor alternativa"),
    ("diccionario", "Diccionario", "Términos técnicos explicados.", "diccionario glosario terminos definicion"),
    ("evidencia", "Evidencia", "Qué datos reales hay hoy.", "evidencia datos reales precios"),
]


def _indice_busqueda():
    idx = []
    for ruta, titulo, texto, claves in VISTAS:
        idx.append({"tipo": "VISTA", "ruta": ruta, "titulo": titulo, "texto": texto, "claves": _norm(claves), "peso": 3})
    for m in C.MODULOS:
        idx.append({"tipo": "MODULO", "ruta": f"estudio/{m['id']}", "titulo": f"{m['icono']} {m['titulo']}", "texto": m["resumen"],
                    "claves": _norm(" ".join([m["titulo"], m["claves"], m["resumen"]])),
                    "cuerpo": _norm(" ".join([m["que_es"], m["por_que"], m["que_modelamos"]] + [t for t, _ in m["que_sabemos"]])),
                    "peso": 2})
    for cod, provincia, centro in _regiones_simple():
        idx.append({"tipo": "REGION", "ruta": "localizacion", "titulo": f"📍 {cod} — {centro} ({provincia})",
                    "texto": "Región en estudio (sin ranking: faltan datos de campo).",
                    "claves": _norm(f"{cod} {provincia} {centro}"), "peso": 2})
    for t in glosario()["terminos"]:
        idx.append({"tipo": "TERMINO", "ruta": "diccionario", "q": t["termino"], "titulo": f"📖 {t['termino']}",
                    "texto": t["definicion"][:160], "claves": _norm(t["termino"]), "cuerpo": _norm(t["definicion"]), "peso": 1})
    return idx


def _regiones_simple():
    try:
        return [(r["codigo"], r["provincia"], r["centro"]) for r in localizacion()["regiones"]]
    except Exception:   # noqa: BLE001 — la búsqueda no debe caerse por una tabla
        return []


_IDX = None


def buscar(q, n=12):
    global _IDX
    if _IDX is None:
        _IDX = _indice_busqueda()
    toks = [t for t in re.split(r"[^\w]+", _norm(q)) if t]
    if not toks:
        return {"q": q, "resultados": []}
    res = []
    for it in _IDX:
        claves, cuerpo, titulo = it["claves"], it.get("cuerpo", ""), _norm(it["titulo"])
        s = 0
        for t in toks:
            if re.search(rf"\b{re.escape(t)}", titulo):
                s += 14 * it["peso"]
            elif re.search(rf"\b{re.escape(t)}", claves):
                s += 10 * it["peso"]
            elif t in titulo:
                s += 6 * it["peso"]
            elif t in cuerpo:
                s += 1 * it["peso"]
            else:
                s -= 5
        if s > 0:
            res.append((s, it))
    res.sort(key=lambda x: -x[0])
    out = [{k: v for k, v in it.items() if k not in ("claves", "cuerpo", "peso")} for _, it in res[:n]]
    return {"q": q, "resultados": out}
