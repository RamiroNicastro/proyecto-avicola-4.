#!/usr/bin/env python3
"""
MODELO MULTICRITERIO DE LOCALIZACIÓN — versión 1.0 (2026-10-01, sesión 12A)
===========================================================================

Compara CORREDORES / REGIONES de Argentina (nivel provincia + corredor) para una futura empresa avícola
integrada. NO elige ubicación, NO selecciona terrenos, NO calcula CAPEX ni OPEX, NO asigna precios.

Qué hace
--------
1. Lee la matriz de criterios en formato largo (`matriz_localizacion.csv`: una fila por región × subcriterio).
2. Lee los perfiles de ponderación (`pesos_localizacion.csv`: peso por GRUPO de criterio, suma 100 por perfil).
3. Valida esquema, estados de evidencia y pesos (se DETIENE ante errores).
4. Selecciona los valores USABLES según el modo:
     - estricto (por defecto): solo ESTADO = DISPONIBLE y TIPO_EVIDENCIA ∈ {VERIFICADO, COTIZACION, ESTIMACION}
       con FUENTE declarada. Los valores [PVDP] y los [SUPUESTO] NO se usan.
     - exploratorio: además usa ESTADO = PVDP y TIPO = SUPUESTO. Todo resultado se rotula EXPLORATORIO:
       sirve para ver la mecánica, NUNCA como resultado.
5. Normaliza cada subcriterio a [0, 1] (1 = mejor):
     minmax, MAYOR_MEJOR:  n = (x − min) / (max − min)
     minmax, MENOR_MEJOR:  n = (max − x) / (max − min)
     rango_fijo:a:b      : igual, con min = a, max = b y x recortado a [a, b] (evita que el resultado dependa
                           del conjunto de regiones comparadas).
     Empate (max = min con ≥ 2 observaciones): n = 1 para todas las regiones con dato.
   Un subcriterio es NO_COMPARABLE (no puntúa para nadie) si tiene menos de `MIN_UNIDADES` unidades de
   observación distintas (provincias si NIVEL_DATO = PROVINCIA; regiones si = CORREDOR) o si menos de
   `MIN_FRAC_REGIONES_CRITERIO` de las regiones tiene dato.
6. Pesos: peso del subcriterio = peso del grupo / 100 / (n.º de subcriterios del grupo en la matriz).
   Suma de pesos de subcriterios = 1.
7. Puntaje por región y perfil — SIN IMPUTAR FALTANTES:
     cobertura   = Σ pesos de subcriterios con valor normalizado               (0–1)
     observado   = Σ peso × n  sobre esos subcriterios  = COTA INFERIOR        (un faltante aporta 0)
     máximo      = observado + (1 − cobertura)          = COTA SUPERIOR        (si todo faltante fuera óptimo)
     sobre_disp. = observado / cobertura   → solo se informa si cobertura ≥ UMBRAL_COBERTURA
   El ancho del intervalo [observado, máximo] es exactamente el peso faltante: mide cuánto podría cambiar
   el resultado con los datos que faltan. Ninguna región recibe puntos por datos inexistentes.
8. Alertas: región con fracción de subcriterios sin dato > UMBRAL_FALTANTES → "DEMASIADOS DATOS FALTANTES".
9. Ranking: solo entre regiones con cobertura ≥ UMBRAL_COBERTURA y si al menos 2 califican; las demás se
   informan "SIN PUNTAJE" (nunca se ubican últimas). Se marca si cada posición es ROBUSTA (cota inferior de
   la región superior > cota superior de la siguiente) o NO ROBUSTA.
10. Comparación por perfil y sensibilidad de pesos (± factor por grupo, renormalizando a 100).

Factores NO puntuables
----------------------
Las filas con CRITERIO = NETWORK (p. ej., el contacto personal en Chaco, SUP-014) se informan aparte y
NUNCA puntúan. Un perfil con peso > 0 en NETWORK es un error.

Unidades y convenciones
-----------------------
Las unidades de cada subcriterio están en la columna UNIDAD (km, h, %, n, t/año, USD/ha, escala 1-5...).
Decimal con punto en los CSV. Los valores de la matriz real son mayoritariamente PENDIENTES o [PVDP]
(regla 16 de CLAUDE.md): con la evidencia actual el modo estricto NO emite ranking, y eso es el resultado
correcto. Supuestos del modelo: SUP-12A-03 a SUP-12A-07 (10_localizacion/actualizaciones_gestion_12A.md).

Uso
---
    python3 10_localizacion/modelo_localizacion.py                      # tests + resumen + resultados CSV
    python3 10_localizacion/modelo_localizacion.py --solo-tests
    python3 10_localizacion/modelo_localizacion.py --modo exploratorio --perfil C --detalle
    python3 10_localizacion/modelo_localizacion.py --demo               # datos FICTICIOS: muestra la mecánica
    python3 10_localizacion/modelo_localizacion.py --demo --sensibilidad 0.5
    python3 10_localizacion/modelo_localizacion.py --peso DEMANDA=40 --peso ALIMENTO=0 ...   # perfil "P"
    python3 10_localizacion/modelo_localizacion.py --pesos-csv otro_archivo.csv --umbral-cobertura 0.8

El script se DETIENE (código 1) si falla cualquier prueba o validación.
"""

import argparse
import copy
import csv
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
MATRIZ = os.path.join(DIR, "matriz_localizacion.csv")
PESOS = os.path.join(DIR, "pesos_localizacion.csv")
RESULTADOS = os.path.join(DIR, "resultados_localizacion.csv")

GRUPOS = ["DEMANDA", "PRODUCCION_PRIMARIA", "ALIMENTO", "FAENA_INDUSTRIA", "AGUA", "EFLUENTES", "ENERGIA",
          "LOGISTICA", "EXPORTACION", "TERRENO", "NORMATIVA", "RRHH"]
NO_PUNTUABLES = {"NETWORK"}
ESTADOS = {"DISPONIBLE", "PVDP", "PENDIENTE", "NO_APLICA"}
TIPOS = {"", "VERIFICADO", "ESTIMACION", "SUPUESTO", "COTIZACION", "PVDP"}
TIPOS_ESTRICTO = {"VERIFICADO", "COTIZACION", "ESTIMACION"}
SENTIDOS = {"MAYOR_MEJOR", "MENOR_MEJOR"}
NIVELES = {"CORREDOR", "PROVINCIA"}
COLUMNAS = ["REGION", "PROVINCIA", "CORREDOR", "CRITERIO", "SUBCRITERIO", "NOMBRE_SUBCRITERIO", "UNIDAD",
            "SENTIDO", "NIVEL_DATO", "VALOR", "TIPO_EVIDENCIA", "FUENTE", "ESTADO", "NORMALIZACION", "PESO",
            "PUNTAJE", "OBSERVACIONES"]

# [SUPUESTO] SUP-12A-04 — umbrales editables por línea de comandos
UMBRAL_COBERTURA = 0.75          # cobertura de peso mínima para informar puntaje y entrar al ranking
UMBRAL_FALTANTES = 0.40          # fracción de subcriterios sin dato que dispara la alerta
MIN_FRAC_REGIONES_CRITERIO = 0.5  # fracción mínima de regiones con dato para que un subcriterio compare
MIN_UNIDADES = 2                 # unidades de observación distintas (provincias o corredores)
TOL_PESOS = 1e-6


class ErrorValidacion(ValueError):
    pass


# ----------------------------------------------------------------------------------------------------------
# Lectura y validación
# ----------------------------------------------------------------------------------------------------------
def leer_csv(ruta):
    with open(ruta, newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def es_numero(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False


def validar_normalizacion(m):
    if m == "minmax":
        return True
    partes = m.split(":")
    return (len(partes) == 3 and partes[0] == "rango_fijo" and es_numero(partes[1]) and es_numero(partes[2])
            and float(partes[2]) > float(partes[1]))


def validar_matriz(filas):
    """Devuelve (errores, advertencias). No modifica las filas."""
    errores, adv = [], []
    if not filas:
        return ["matriz vacía"], adv
    faltan = [c for c in COLUMNAS if c not in filas[0]]
    if faltan:
        return [f"faltan columnas: {faltan}"], adv
    vistos, defin = set(), {}
    for i, r in enumerate(filas, start=2):
        ref = f"fila {i} ({r['REGION']} × {r['SUBCRITERIO']})"
        clave = (r["REGION"], r["SUBCRITERIO"])
        if clave in vistos:
            errores.append(f"{ref}: duplicada")
        vistos.add(clave)
        if r["CRITERIO"] not in GRUPOS and r["CRITERIO"] not in NO_PUNTUABLES:
            errores.append(f"{ref}: CRITERIO desconocido '{r['CRITERIO']}'")
        if r["ESTADO"] not in ESTADOS:
            errores.append(f"{ref}: ESTADO inválido '{r['ESTADO']}'")
        if r["TIPO_EVIDENCIA"] not in TIPOS:
            errores.append(f"{ref}: TIPO_EVIDENCIA inválido '{r['TIPO_EVIDENCIA']}'")
        if r["CRITERIO"] not in NO_PUNTUABLES:
            if r["SENTIDO"] not in SENTIDOS:
                errores.append(f"{ref}: SENTIDO inválido '{r['SENTIDO']}'")
            if r["NIVEL_DATO"] not in NIVELES:
                errores.append(f"{ref}: NIVEL_DATO inválido '{r['NIVEL_DATO']}'")
            if not validar_normalizacion(r["NORMALIZACION"]):
                errores.append(f"{ref}: NORMALIZACION inválida '{r['NORMALIZACION']}'")
        valor = r["VALOR"].strip()
        if valor == "":
            if r["ESTADO"] in ("DISPONIBLE", "PVDP"):
                errores.append(f"{ref}: ESTADO {r['ESTADO']} sin VALOR")
        else:
            if r["ESTADO"] in ("PENDIENTE", "NO_APLICA"):
                errores.append(f"{ref}: tiene VALOR pero ESTADO {r['ESTADO']}")
            if r["CRITERIO"] not in NO_PUNTUABLES and not es_numero(valor):
                errores.append(f"{ref}: VALOR no numérico '{valor}'")
            if r["TIPO_EVIDENCIA"] == "":
                errores.append(f"{ref}: VALOR sin TIPO_EVIDENCIA")
            if r["FUENTE"].strip() == "":
                errores.append(f"{ref}: VALOR sin FUENTE (regla 5)")
        if r["TIPO_EVIDENCIA"] == "PVDP" and r["ESTADO"] != "PVDP":
            errores.append(f"{ref}: un dato [PVDP] no puede tener ESTADO {r['ESTADO']} (regla 16)")
        if r["ESTADO"] == "DISPONIBLE" and r["TIPO_EVIDENCIA"] not in TIPOS_ESTRICTO | {"SUPUESTO"}:
            errores.append(f"{ref}: ESTADO DISPONIBLE con TIPO '{r['TIPO_EVIDENCIA']}'")
        if r["PESO"].strip() or r["PUNTAJE"].strip():
            adv.append(f"{ref}: PESO/PUNTAJE de la matriz se ignoran (pesos en pesos_localizacion.csv)")
        d = (r["CRITERIO"], r["SENTIDO"], r["UNIDAD"], r["NIVEL_DATO"], r["NORMALIZACION"])
        if r["SUBCRITERIO"] in defin and defin[r["SUBCRITERIO"]] != d:
            errores.append(f"{ref}: definición inconsistente del subcriterio {r['SUBCRITERIO']}")
        defin.setdefault(r["SUBCRITERIO"], d)
    regiones = {r["REGION"] for r in filas}
    subs = {r["SUBCRITERIO"] for r in filas if r["CRITERIO"] not in NO_PUNTUABLES}
    for reg in sorted(regiones):
        tiene = {r["SUBCRITERIO"] for r in filas if r["REGION"] == reg}
        falt = subs - tiene
        if falt and any(r["REGION"] == reg and r["CRITERIO"] not in NO_PUNTUABLES for r in filas):
            adv.append(f"{reg}: sin fila para {sorted(falt)} (se tratan como faltantes)")
    return errores, adv


def leer_pesos(ruta):
    perfiles, nombres = {}, {}
    for r in leer_csv(ruta):
        p = r["PERFIL"].strip()
        nombres[p] = r.get("NOMBRE_PERFIL", p).strip()
        if not es_numero(r["PESO"]):
            raise ErrorValidacion(f"perfil {p}: peso no numérico '{r['PESO']}'")
        perfiles.setdefault(p, {})[r["CRITERIO"].strip()] = float(r["PESO"])
    return perfiles, nombres


def validar_pesos(pesos_grupo, nombre="perfil"):
    """Pesos por grupo en puntos (suman 100). Errores → ErrorValidacion."""
    errores = []
    for g, w in pesos_grupo.items():
        if g in NO_PUNTUABLES and w > 0:
            errores.append(f"{nombre}: el factor {g} es cualitativo NO puntuable (SUP-014) y no puede tener peso")
        elif g not in GRUPOS and g not in NO_PUNTUABLES:
            errores.append(f"{nombre}: grupo desconocido '{g}'")
        if w < 0:
            errores.append(f"{nombre}: peso negativo en {g}")
    faltan = [g for g in GRUPOS if g not in pesos_grupo]
    if faltan:
        errores.append(f"{nombre}: faltan grupos {faltan} (declarar 0 explícitamente)")
    suma = sum(w for g, w in pesos_grupo.items() if g in GRUPOS)
    if abs(suma - 100.0) > TOL_PESOS:
        errores.append(f"{nombre}: los pesos suman {suma:g}, deben sumar 100")
    if errores:
        raise ErrorValidacion("; ".join(errores))


# ----------------------------------------------------------------------------------------------------------
# Núcleo del cálculo
# ----------------------------------------------------------------------------------------------------------
def valor_usable(fila, modo):
    """float si el dato puede usarse en el modo; None si no. Nunca imputa."""
    if fila["CRITERIO"] in NO_PUNTUABLES or fila["VALOR"].strip() == "":
        return None
    if modo == "estricto":
        ok = (fila["ESTADO"] == "DISPONIBLE" and fila["TIPO_EVIDENCIA"] in TIPOS_ESTRICTO
              and fila["FUENTE"].strip() != "")
    elif modo == "exploratorio":
        ok = fila["ESTADO"] in ("DISPONIBLE", "PVDP")
    else:
        raise ValueError(f"modo desconocido {modo}")
    return float(fila["VALOR"]) if ok else None


def estructura(filas):
    """regiones (orden de aparición), provincia por región, definición por subcriterio."""
    regiones, prov, defs = [], {}, {}
    for r in filas:
        if r["REGION"] not in prov:
            regiones.append(r["REGION"])
            prov[r["REGION"]] = r["PROVINCIA"]
        if r["CRITERIO"] not in NO_PUNTUABLES and r["SUBCRITERIO"] not in defs:
            defs[r["SUBCRITERIO"]] = {k: r[k] for k in ("CRITERIO", "NOMBRE_SUBCRITERIO", "UNIDAD", "SENTIDO",
                                                         "NIVEL_DATO", "NORMALIZACION")}
    return regiones, prov, defs


def normalizar(valores, sentido, metodo, unidades, n_regiones,
               min_frac=MIN_FRAC_REGIONES_CRITERIO, min_unidades=MIN_UNIDADES):
    """valores: {región: float|None}; unidades: {región: unidad de observación}.
    Devuelve ({región: n|None}, estado) con estado ∈ {COMPARABLE, EMPATE, NO_COMPARABLE}."""
    validos = {r: v for r, v in valores.items() if v is not None}
    nulos = {r: None for r in valores}
    if (len({unidades[r] for r in validos}) < min_unidades
            or n_regiones == 0 or len(validos) / n_regiones < min_frac):
        return nulos, "NO_COMPARABLE"
    if metodo == "minmax":
        lo, hi = min(validos.values()), max(validos.values())
    else:
        _, a, b = metodo.split(":")
        lo, hi = float(a), float(b)
    out = dict(nulos)
    if hi == lo:
        for r in validos:
            out[r] = 1.0
        return out, "EMPATE"
    for r, v in validos.items():
        x = min(max(v, lo), hi)
        n = (x - lo) / (hi - lo)
        out[r] = n if sentido == "MAYOR_MEJOR" else 1.0 - n
    return out, "COMPARABLE"


def pesos_subcriterios(pesos_grupo, defs):
    """Peso de cada subcriterio (suma 1). Error si un grupo con peso no tiene subcriterios en la matriz."""
    validar_pesos(pesos_grupo)
    por_grupo = {}
    for s, d in defs.items():
        por_grupo.setdefault(d["CRITERIO"], []).append(s)
    for g in GRUPOS:
        if pesos_grupo[g] > 0 and g not in por_grupo:
            raise ErrorValidacion(f"el grupo {g} tiene peso pero ningún subcriterio en la matriz")
    total = sum(pesos_grupo[g] for g in GRUPOS if g in por_grupo)
    w = {}
    for g, subs in por_grupo.items():
        for s in subs:
            w[s] = pesos_grupo[g] / total / len(subs)
    return w


def evaluar(filas, pesos_grupo, modo="estricto", umbral_cobertura=UMBRAL_COBERTURA,
            umbral_faltantes=UMBRAL_FALTANTES):
    regiones, prov, defs = estructura(filas)
    w = pesos_subcriterios(pesos_grupo, defs)
    idx = {(r["REGION"], r["SUBCRITERIO"]): r for r in filas}
    norm, estado_crit, crudo = {}, {}, {}
    for s, d in defs.items():
        vals = {}
        for reg in regiones:
            fila = idx.get((reg, s))
            vals[reg] = valor_usable(fila, modo) if fila else None
        unidades = {reg: (prov[reg] if d["NIVEL_DATO"] == "PROVINCIA" else reg) for reg in regiones}
        norm[s], estado_crit[s] = normalizar(vals, d["SENTIDO"], d["NORMALIZACION"], unidades, len(regiones))
        crudo[s] = vals
    res = {}
    for reg in regiones:
        cob = sum(w[s] for s in defs if norm[s][reg] is not None)
        obs = sum(w[s] * norm[s][reg] for s in defs if norm[s][reg] is not None)
        sin_dato = sum(1 for s in defs if crudo[s][reg] is None)
        frac_falt = sin_dato / len(defs)
        prov_usados = sum(1 for s in defs if norm[s][reg] is not None and defs[s]["NIVEL_DATO"] == "PROVINCIA")
        res[reg] = {
            "provincia": prov[reg], "cobertura": cob, "observado": obs, "maximo": obs + (1.0 - cob),
            "sobre_disponible": (obs / cob) if (cob >= umbral_cobertura and cob > 0) else None,
            "frac_faltantes": frac_falt, "alerta_faltantes": frac_falt > umbral_faltantes,
            "datos_provinciales": prov_usados,
            "detalle": {s: {"valor": crudo[s][reg], "normalizado": norm[s][reg], "peso": w[s],
                            "contribucion": (w[s] * norm[s][reg]) if norm[s][reg] is not None else 0.0,
                            "estado_criterio": estado_crit[s]} for s in defs},
        }
    califican = [r for r in regiones if res[r]["sobre_disponible"] is not None]
    ranking, motivo = None, ""
    if len(califican) >= 2:
        orden = sorted(califican, key=lambda r: (-res[r]["sobre_disponible"], r))
        ranking = []
        for i, r in enumerate(orden):
            sig = orden[i + 1] if i + 1 < len(orden) else None
            robusto = None if sig is None else res[r]["observado"] > res[sig]["maximo"]
            ranking.append({"region": r, "posicion": i + 1, "robusto_vs_siguiente": robusto})
        excl = [r for r in regiones if r not in califican]
        if excl:
            motivo = f"ranking PARCIAL: sin puntaje por datos insuficientes {excl}"
    else:
        motivo = (f"RANKING NO EMITIDO: {len(califican)} región(es) alcanzan la cobertura mínima "
                  f"{umbral_cobertura:.0%} (se necesitan ≥ 2)")
    no_comp = sorted(s for s, e in estado_crit.items() if e == "NO_COMPARABLE")
    return {"modo": modo, "regiones": regiones, "resultados": res, "ranking": ranking, "motivo": motivo,
            "no_comparables": no_comp, "estado_criterios": estado_crit,
            "network": [r for r in filas if r["CRITERIO"] in NO_PUNTUABLES]}


def comparar_perfiles(filas, perfiles, modo="estricto", **kw):
    return {p: evaluar(filas, pg, modo, **kw) for p, pg in perfiles.items()}


def sensibilidad(filas, pesos_grupo, factor=0.5, modo="estricto", **kw):
    """Para cada grupo con peso > 0: multiplica su peso por (1 ± factor), renormaliza a 100 y compara el
    orden del ranking con el base. Devuelve lista de (grupo, signo, cambia_orden, ranking)."""
    base = evaluar(filas, pesos_grupo, modo, **kw)
    orden_base = [x["region"] for x in base["ranking"]] if base["ranking"] else None
    out = []
    for g in GRUPOS:
        if pesos_grupo[g] <= 0:
            continue
        for signo in (+1, -1):
            pg = dict(pesos_grupo)
            pg[g] = pesos_grupo[g] * (1 + signo * factor)
            tot = sum(pg[k] for k in GRUPOS)
            pg = {k: (pg[k] * 100.0 / tot if k in GRUPOS else pg[k]) for k in pg}
            # corrige redondeo para que la suma sea exactamente 100
            pg[GRUPOS[-1]] += 100.0 - sum(pg[k] for k in GRUPOS)
            ev = evaluar(filas, pg, modo, **kw)
            orden = [x["region"] for x in ev["ranking"]] if ev["ranking"] else None
            out.append((g, signo, orden != orden_base, orden))
    return orden_base, out


# ----------------------------------------------------------------------------------------------------------
# Datos de DEMOSTRACIÓN (ficticios) — solo para ver la mecánica y para las pruebas
# ----------------------------------------------------------------------------------------------------------
DEMO_SUBS = [  # subcriterio, grupo, unidad, sentido, Z-CERCA, Z-CLUSTER, Z-GRANOS
    ("DEM-01", "DEMANDA", "km", "MENOR_MEJOR", 50, 320, 600),
    ("PRI-02", "PRODUCCION_PRIMARIA", "n", "MAYOR_MEJOR", 20, 900, 150),
    ("PRI-05", "PRODUCCION_PRIMARIA", "granjas/1000 km2", "MENOR_MEJOR", 5, 60, 8),
    ("ALI-01", "ALIMENTO", "t/año", "MAYOR_MEJOR", 800000, 1500000, 4000000),
    ("IND-02", "FAENA_INDUSTRIA", "aves/día", "MAYOR_MEJOR", 0, 20000, 5000),
    ("AGU-02", "AGUA", "escala 1-5", "MAYOR_MEJOR", 3, 3, 2),
    ("EFL-02", "EFLUENTES", "escala 1-5", "MAYOR_MEJOR", 3, 3, 4),
    ("ENE-01", "ENERGIA", "escala 1-5", "MAYOR_MEJOR", 4, 3, 3),
    ("LOG-02", "LOGISTICA", "escala 1-5", "MAYOR_MEJOR", 2, 4, 5),
    ("EXP-01", "EXPORTACION", "km", "MENOR_MEJOR", 40, 320, 600),
    ("TER-02", "TERRENO", "USD/ha", "MENOR_MEJOR", 60000, 25000, 8000),
    ("NOR-02", "NORMATIVA", "escala 1-5", "MAYOR_MEJOR", 3, 4, 3),
    ("RRH-03", "RRHH", "escala 1-5", "MAYOR_MEJOR", 5, 3, 3),
]
DEMO_REGIONES = [("Z-CERCA", "DEMO-1"), ("Z-CLUSTER", "DEMO-2"), ("Z-GRANOS", "DEMO-3")]


def fila(region, provincia, sub, grupo, unidad, sentido, valor="", tipo="", fuente="", estado="PENDIENTE",
         nivel="CORREDOR", normalizacion="minmax"):
    return {"REGION": region, "PROVINCIA": provincia, "CORREDOR": region, "CRITERIO": grupo,
            "SUBCRITERIO": sub, "NOMBRE_SUBCRITERIO": sub, "UNIDAD": unidad, "SENTIDO": sentido,
            "NIVEL_DATO": nivel, "VALOR": "" if valor == "" else str(valor), "TIPO_EVIDENCIA": tipo,
            "FUENTE": fuente, "ESTADO": estado, "NORMALIZACION": normalizacion, "PESO": "", "PUNTAJE": "",
            "OBSERVACIONES": ""}


def matriz_demo():
    filas = []
    for j, (reg, prov) in enumerate(DEMO_REGIONES):
        for sub, grp, uni, sen, *vals in DEMO_SUBS:
            filas.append(fila(reg, prov, sub, grp, uni, sen, vals[j], "ESTIMACION", "DEMO-FICTICIO", "DISPONIBLE"))
    return filas


# ----------------------------------------------------------------------------------------------------------
# Pruebas
# ----------------------------------------------------------------------------------------------------------
def _perfiles_reales():
    return leer_pesos(PESOS)[0]


def pruebas():
    res = []

    def check(nombre, cond, info=""):
        res.append((nombre, bool(cond), info))

    perfiles = _perfiles_reales()
    demo = matriz_demo()

    # T01 pesos que suman 100 y rechazo de pesos mal formados
    ok = True
    for p, pg in perfiles.items():
        try:
            validar_pesos(pg, p)
        except ErrorValidacion:
            ok = False
    malos = 0
    for mod in ({"DEMANDA": 31}, {"DEMANDA": -5, "RRHH": 40}, {"NUEVO": 0}):
        pg = dict(perfiles["C"]); pg.update(mod)
        try:
            validar_pesos(pg)
        except ErrorValidacion:
            malos += 1
    pg = dict(perfiles["C"]); del pg["AGUA"]
    try:
        validar_pesos(pg)
    except ErrorValidacion:
        malos += 1
    w = pesos_subcriterios(perfiles["C"], estructura(leer_csv(MATRIZ))[2])
    check("T01 pesos de perfiles suman 100; sumas ≠ 100, negativos, grupos desconocidos o ausentes se rechazan; "
          "pesos de subcriterios suman 1", ok and malos == 4 and abs(sum(w.values()) - 1) < 1e-12)

    # T02 inversión menor/mejor
    n_menor, _ = normalizar({"a": 100.0, "b": 300.0, "c": 200.0}, "MENOR_MEJOR", "minmax",
                            {"a": "a", "b": "b", "c": "c"}, 3)
    n_mayor, _ = normalizar({"a": 100.0, "b": 300.0, "c": 200.0}, "MAYOR_MEJOR", "minmax",
                            {"a": "a", "b": "b", "c": "c"}, 3)
    check("T02 MENOR_MEJOR invierte: el menor valor obtiene 1 y el mayor 0; MAYOR_MEJOR al revés",
          n_menor == {"a": 1.0, "b": 0.0, "c": 0.5} and n_mayor == {"a": 0.0, "b": 1.0, "c": 0.5})

    # T03 datos faltantes: no aportan puntos, ensanchan el intervalo y no se imputan
    d2 = copy.deepcopy(demo)
    for f in d2:
        if f["REGION"] == "Z-GRANOS" and f["SUBCRITERIO"] in ("ALI-01", "TER-02"):
            f.update(VALOR="", TIPO_EVIDENCIA="", FUENTE="", ESTADO="PENDIENTE")
    ev = evaluar(d2, perfiles["B"])
    r = ev["resultados"]["Z-GRANOS"]
    w_falt = r["detalle"]["ALI-01"]["peso"] + r["detalle"]["TER-02"]["peso"]
    check("T03 faltantes: contribución 0, cobertura = 1 − peso faltante, ancho del intervalo = peso faltante, "
          "valor queda vacío (no imputado)",
          r["detalle"]["ALI-01"]["contribucion"] == 0 and r["detalle"]["ALI-01"]["valor"] is None
          and abs(r["cobertura"] - (1 - w_falt)) < 1e-12 and abs((r["maximo"] - r["observado"]) - w_falt) < 1e-12)

    # T04 sin ranking cuando faltan demasiados datos
    d3 = copy.deepcopy(demo)
    for f in d3:
        if f["SUBCRITERIO"] not in ("DEM-01", "PRI-02", "ALI-01"):
            f.update(VALOR="", TIPO_EVIDENCIA="", FUENTE="", ESTADO="PENDIENTE")
    ev3 = evaluar(d3, perfiles["C"])
    check("T04 con cobertura < umbral no hay ranking ni puntaje informado; se alerta por faltantes",
          ev3["ranking"] is None and "NO EMITIDO" in ev3["motivo"]
          and all(x["sobre_disponible"] is None and x["alerta_faltantes"] for x in ev3["resultados"].values()))

    # T05 el resultado cambia al cambiar las ponderaciones
    top = {p: evaluar(demo, perfiles[p])["ranking"][0]["region"] for p in ("A", "B")}
    check("T05 cambiar ponderaciones cambia el resultado (demo ficticia: primer lugar A ≠ B)",
          top["A"] != top["B"], f"A → {top['A']}, B → {top['B']}")

    # T06 PVDP no se usa como hecho
    d4 = copy.deepcopy(demo)
    for f in d4:
        f.update(TIPO_EVIDENCIA="PVDP", ESTADO="PVDP")
    e_est = evaluar(d4, perfiles["C"], "estricto")
    e_exp = evaluar(d4, perfiles["C"], "exploratorio")
    check("T06 [PVDP]: ignorado en modo estricto (cobertura 0, sin ranking); solo el modo exploratorio lo usa",
          all(x["cobertura"] == 0 and x["observado"] == 0 for x in e_est["resultados"].values())
          and e_est["ranking"] is None and e_exp["ranking"] is not None and e_exp["modo"] == "exploratorio")

    # T07 ninguna región recibe puntos por datos inexistentes
    d5 = copy.deepcopy(demo)
    for f in d5:
        if f["REGION"] == "Z-CLUSTER":
            f.update(VALOR="", TIPO_EVIDENCIA="", FUENTE="", ESTADO="PENDIENTE")
    ev5 = evaluar(d5, perfiles["C"])
    rc = ev5["resultados"]["Z-CLUSTER"]
    real = evaluar(leer_csv(MATRIZ), perfiles["C"], "estricto")
    check("T07 región sin datos: puntaje observado 0, sin puntaje informado, fuera del ranking (no última); "
          "matriz real en modo estricto: observado 0 en todas",
          rc["observado"] == 0 and rc["cobertura"] == 0 and rc["sobre_disponible"] is None
          and all(x["region"] != "Z-CLUSTER" for x in (ev5["ranking"] or []))
          and all(x["observado"] == 0 for x in real["resultados"].values()))

    # T08 el contacto/network de Chaco no puntúa
    d6 = copy.deepcopy(demo)
    d6.append(fila("Z-GRANOS", "DEMO-3", "NET-01", "NETWORK", "cualitativo", "", "contacto", "SUPUESTO",
                   "SUP-014", "DISPONIBLE"))
    pg = dict(perfiles["C"]); pg["NETWORK"] = 10; pg["DEMANDA"] -= 10
    rechazo = False
    try:
        validar_pesos(pg)
    except ErrorValidacion:
        rechazo = True
    e6, e_sin = evaluar(d6, perfiles["C"]), evaluar(demo, perfiles["C"])
    check("T08 factor NETWORK (contacto en Chaco, SUP-014): peso > 0 se rechaza; su fila no cambia ningún puntaje",
          rechazo and len(e6["network"]) == 1 and validar_matriz(d6)[0] == []
          and all(abs(e6["resultados"][r]["observado"] - e_sin["resultados"][r]["observado"]) < 1e-12
                  for r in e_sin["regiones"]))

    # T09 validación de estados de evidencia
    casos = [
        dict(TIPO_EVIDENCIA="PVDP", ESTADO="DISPONIBLE"),           # PVDP disfrazado de hecho
        dict(FUENTE=""),                                           # sin fuente
        dict(VALOR="cerca"),                                       # no numérico
        dict(VALOR="", ESTADO="DISPONIBLE"),                       # disponible sin valor
        dict(ESTADO="PENDIENTE"),                                  # valor con estado pendiente
    ]
    detectados = 0
    for c in casos:
        d7 = copy.deepcopy(demo); d7[0].update(c)
        if validar_matriz(d7)[0]:
            detectados += 1
    errs_real, _ = validar_matriz(leer_csv(MATRIZ))
    check("T09 validación: PVDP con estado DISPONIBLE, valor sin fuente, no numérico, disponible sin valor y "
          "valor con estado pendiente se rechazan; la matriz real valida sin errores",
          detectados == len(casos) and errs_real == [], f"errores matriz real: {errs_real[:3]}")

    # T10 subcriterio con datos de una sola provincia no compara
    filas = []
    for reg, prov in (("R1", "P1"), ("R2", "P1"), ("R3", "P2"), ("R4", "P3")):
        v = "250" if prov == "P1" else ""
        filas.append(fila(reg, prov, "EFL-01", "EFLUENTES", "mg/L", "MAYOR_MEJOR", v, "VERIFICADO" if v else "",
                          "X" if v else "", "DISPONIBLE" if v else "PENDIENTE", nivel="PROVINCIA"))
    n10, est10 = normalizar({f["REGION"]: valor_usable(f, "estricto") for f in filas}, "MAYOR_MEJOR", "minmax",
                            {f["REGION"]: f["PROVINCIA"] for f in filas}, 4)
    check("T10 dato de una sola provincia (aunque cubra 50 % de las regiones) → NO_COMPARABLE: no premia a nadie",
          est10 == "NO_COMPARABLE" and all(v is None for v in n10.values()))

    # T11 alerta por demasiados faltantes en una región concreta
    d8 = copy.deepcopy(demo)
    for f in d8:
        if f["REGION"] == "Z-CERCA" and f["SUBCRITERIO"] not in ("DEM-01", "PRI-02", "PRI-05", "ALI-01", "IND-02",
                                                                    "AGU-02", "EFL-02"):
            f.update(VALOR="", TIPO_EVIDENCIA="", FUENTE="", ESTADO="PENDIENTE")
    ev8 = evaluar(d8, perfiles["C"])
    check("T11 alerta 'demasiados faltantes' solo en la región afectada (6/13 sin dato > 40 %)",
          ev8["resultados"]["Z-CERCA"]["alerta_faltantes"]
          and not ev8["resultados"]["Z-CLUSTER"]["alerta_faltantes"])

    # T12 SUPUESTO excluido en modo estricto
    d9 = copy.deepcopy(demo)
    for f in d9:
        f["TIPO_EVIDENCIA"] = "SUPUESTO"
    check("T12 [SUPUESTO] no se usa en modo estricto",
          evaluar(d9, perfiles["C"], "estricto")["ranking"] is None
          and evaluar(d9, perfiles["C"], "exploratorio")["ranking"] is not None)

    # T13 invariancia de unidades (km vs m) en min-max
    d10 = copy.deepcopy(demo)
    for f in d10:
        if f["SUBCRITERIO"] == "DEM-01":
            f["VALOR"] = str(float(f["VALOR"]) * 1000)
    a, b = evaluar(demo, perfiles["A"]), evaluar(d10, perfiles["A"])
    check("T13 cambiar la unidad de un subcriterio (km → m) no cambia los puntajes",
          all(abs(a["resultados"][r]["observado"] - b["resultados"][r]["observado"]) < 1e-12 for r in a["regiones"]))

    # T14 empate y rango fijo con recorte
    n14, e14 = normalizar({"a": 5.0, "b": 5.0}, "MAYOR_MEJOR", "minmax", {"a": "a", "b": "b"}, 2)
    n15, _ = normalizar({"a": -10.0, "b": 600.0, "c": 2000.0}, "MENOR_MEJOR", "rango_fijo:0:1200",
                        {"a": "a", "b": "b", "c": "c"}, 3)
    check("T14 empate → 1 para ambos; rango fijo 0–1200 km recorta y es independiente del conjunto",
          e14 == "EMPATE" and n14 == {"a": 1.0, "b": 1.0} and n15 == {"a": 1.0, "b": 0.5, "c": 0.0})

    # T15 cotas: observado ≤ sobre_disponible ≤ máximo y suma de contribuciones = observado
    ev15 = evaluar(d2, perfiles["C"])
    ok15 = True
    for x in ev15["resultados"].values():
        s = sum(d["contribucion"] for d in x["detalle"].values())
        ok15 &= abs(s - x["observado"]) < 1e-12 and x["observado"] <= x["maximo"] + 1e-12
        if x["sobre_disponible"] is not None:
            ok15 &= x["observado"] - 1e-12 <= x["sobre_disponible"] <= x["maximo"] + 1e-12
    check("T15 suma de contribuciones = puntaje observado; observado ≤ sobre disponible ≤ máximo", ok15)

    # T16 robustez del ranking: datos faltantes vuelven NO robusta una posición
    ev16 = evaluar(demo, perfiles["A"])
    check("T16 con datos completos el intervalo es nulo (observado = máximo) y el orden es robusto",
          all(abs(x["maximo"] - x["observado"]) < 1e-12 for x in ev16["resultados"].values())
          and ev16["ranking"][0]["robusto_vs_siguiente"] in (True, False))

    # T17 matriz real: grilla completa, sin ranking estricto y sin ranking exploratorio por cobertura
    real_f = leer_csv(MATRIZ)
    regs, _, defs = estructura(real_f)
    grilla = len(real_f) == len(regs) * len(defs)
    exp_real = comparar_perfiles(real_f, perfiles, "exploratorio")
    check("T17 matriz real: grilla completa región × subcriterio; con la evidencia actual ningún perfil emite "
          "ranking (ni estricto ni exploratorio)",
          grilla and all(e["ranking"] is None for e in comparar_perfiles(real_f, perfiles, "estricto").values())
          and all(e["ranking"] is None for e in exp_real.values()),
          f"{len(regs)} regiones × {len(defs)} subcriterios")

    # T18 los valores provinciales se identifican
    ex = exp_real["C"]["resultados"]["ER-URUGUAY"]
    check("T18 los datos de nivel PROVINCIA usados se cuentan por región (no discriminan dentro de la provincia)",
          ex["datos_provinciales"] >= 1 and exp_real["C"]["estado_criterios"]["EFL-01"] == "NO_COMPARABLE")

    # T19 la evaluación no modifica la matriz de entrada
    d11 = copy.deepcopy(d2)
    evaluar(d11, perfiles["B"], "exploratorio")
    check("T19 evaluar no modifica la matriz (no se rellenan celdas)", d11 == d2)

    # T20 sensibilidad: al menos un cambio de ±50 % en un grupo cambia el orden de la demo
    _, sens = sensibilidad(demo, perfiles["C"], 0.5)
    check("T20 sensibilidad ±50 % por grupo: se detectan cambios de orden en la demo",
          any(c for _, _, c, _ in sens))

    return res


def correr_pruebas(verbose=True):
    res = pruebas()
    fallas = [r for r in res if not r[1]]
    if verbose:
        for nombre, ok, info in res:
            print(f"  [{'OK' if ok else 'FALLA'}] {nombre}" + (f"  ({info})" if info else ""))
        print(f"\n  {len(res) - len(fallas)}/{len(res)} pruebas superadas")
    return not fallas


# ----------------------------------------------------------------------------------------------------------
# Salidas
# ----------------------------------------------------------------------------------------------------------
def fmt(x, pct=False):
    if x is None:
        return "—"
    return f"{x:.0%}" if pct else f"{x:.3f}"


def imprimir(ev, nombre, detalle=False, etiqueta=""):
    print(f"\n### Perfil {nombre} · modo {ev['modo'].upper()} {etiqueta}")
    if ev["modo"] == "exploratorio":
        print("    EXPLORATORIO: usa datos [PVDP]/[SUPUESTO]. NO es un resultado ni un ranking de localización.")
    print(f"    {'Región':<12} {'Cobertura':>9} {'Observado':>9} {'Máximo':>7} {'Sobre disp.':>11} "
          f"{'Faltantes':>9}  Alerta")
    for reg in ev["regiones"]:
        x = ev["resultados"][reg]
        alerta = "DEMASIADOS DATOS FALTANTES" if x["alerta_faltantes"] else ""
        print(f"    {reg:<12} {fmt(x['cobertura'], True):>9} {fmt(x['observado']):>9} {fmt(x['maximo']):>7} "
              f"{fmt(x['sobre_disponible']):>11} {fmt(x['frac_faltantes'], True):>9}  {alerta}")
    if ev["ranking"]:
        print("    Orden (solo regiones con cobertura suficiente):")
        for r in ev["ranking"]:
            rob = {True: "separado del siguiente aun con faltantes", False: "NO separado: intervalos por faltantes superpuestos",
                   None: ""}[
                r["robusto_vs_siguiente"]]
            print(f"      {r['posicion']}. {r['region']}  {rob}")
    if ev["motivo"]:
        print(f"    {ev['motivo']}")
    if ev["no_comparables"]:
        print(f"    Subcriterios NO_COMPARABLES (no puntúan para nadie): {len(ev['no_comparables'])}")
    if ev["network"]:
        print(f"    Factores cualitativos NO puntuables informados aparte: "
              f"{[(f['REGION'], f['SUBCRITERIO']) for f in ev['network']]}")
    if detalle:
        for reg in ev["regiones"]:
            usados = {s: d for s, d in ev["resultados"][reg]["detalle"].items() if d["normalizado"] is not None}
            if usados:
                print(f"      {reg}: " + "; ".join(f"{s}={d['valor']:g}→{d['normalizado']:.2f}×{d['peso']:.3f}"
                                                  for s, d in usados.items()))


def escribir_resultados(evs, nombres, ruta=RESULTADOS):
    campos = ["MODO", "PERFIL", "NOMBRE_PERFIL", "REGION", "PROVINCIA", "COBERTURA", "PUNTAJE_OBSERVADO",
              "PUNTAJE_MAXIMO_POSIBLE", "PUNTAJE_SOBRE_DISPONIBLE", "FRACCION_SUBCRITERIOS_SIN_DATO",
              "DATOS_PROVINCIALES_USADOS", "ALERTA", "POSICION", "ESTADO_RANKING"]
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos)
        w.writeheader()
        for (modo, p), ev in evs.items():
            pos = {r["region"]: r["posicion"] for r in (ev["ranking"] or [])}
            estado = ("EMITIDO" if ev["ranking"] and not ev["motivo"] else
                      "PARCIAL" if ev["ranking"] else "NO_EMITIDO")
            for reg in ev["regiones"]:
                x = ev["resultados"][reg]
                w.writerow({"MODO": modo, "PERFIL": p, "NOMBRE_PERFIL": nombres.get(p, p), "REGION": reg,
                            "PROVINCIA": x["provincia"], "COBERTURA": round(x["cobertura"], 4),
                            "PUNTAJE_OBSERVADO": round(x["observado"], 4),
                            "PUNTAJE_MAXIMO_POSIBLE": round(x["maximo"], 4),
                            "PUNTAJE_SOBRE_DISPONIBLE": "" if x["sobre_disponible"] is None
                            else round(x["sobre_disponible"], 4),
                            "FRACCION_SUBCRITERIOS_SIN_DATO": round(x["frac_faltantes"], 4),
                            "DATOS_PROVINCIALES_USADOS": x["datos_provinciales"],
                            "ALERTA": "DEMASIADOS_DATOS_FALTANTES" if x["alerta_faltantes"] else "",
                            "POSICION": pos.get(reg, ""), "ESTADO_RANKING": estado})


def resumen_cobertura(filas):
    regs, _, defs = estructura(filas)
    tot = len(regs) * len(defs)
    c = {"DISPONIBLE": 0, "PVDP": 0, "PENDIENTE": 0, "NO_APLICA": 0}
    for f in filas:
        if f["CRITERIO"] not in NO_PUNTUABLES:
            c[f["ESTADO"]] += 1
    print(f"\nMatriz: {len(regs)} regiones × {len(defs)} subcriterios = {tot} celdas · "
          + " · ".join(f"{k} {v} ({v / tot:.1%})" for k, v in c.items()))


def main():
    global UMBRAL_COBERTURA, UMBRAL_FALTANTES
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--modo", choices=("estricto", "exploratorio", "ambos"), default="ambos")
    ap.add_argument("--perfil", default="todos", help="A, B, C, D, P (personalizado) o todos")
    ap.add_argument("--pesos-csv", default=PESOS)
    ap.add_argument("--matriz", default=MATRIZ)
    ap.add_argument("--peso", action="append", default=[],
                    help="GRUPO=valor; crea el perfil 'P' a partir del C con esos cambios (debe sumar 100)")
    ap.add_argument("--umbral-cobertura", type=float, default=UMBRAL_COBERTURA)
    ap.add_argument("--umbral-faltantes", type=float, default=UMBRAL_FALTANTES)
    ap.add_argument("--demo", action="store_true", help="usa la matriz FICTICIA de demostración")
    ap.add_argument("--sensibilidad", type=float, help="factor ± por grupo (p. ej., 0.5)")
    ap.add_argument("--detalle", action="store_true")
    ap.add_argument("--sin-csv", action="store_true")
    a = ap.parse_args()

    print("Pruebas del modelo de localización:")
    if not correr_pruebas():
        sys.exit(1)
    if a.solo_tests:
        return

    filas = matriz_demo() if a.demo else leer_csv(a.matriz)
    errores, adv = validar_matriz(filas)
    if errores:
        print("ERRORES DE VALIDACIÓN:\n  " + "\n  ".join(errores[:20]))
        sys.exit(1)
    for x in adv[:10]:
        print(f"  advertencia: {x}")
    perfiles, nombres = leer_pesos(a.pesos_csv)
    if a.peso:
        pg = dict(perfiles["C"])
        for item in a.peso:
            g, v = item.split("=")
            pg[g.strip()] = float(v)
        validar_pesos(pg, "P")
        perfiles["P"], nombres["P"] = pg, "PERSONALIZADO"
    for p, pg in perfiles.items():
        validar_pesos(pg, p)
    sel = list(perfiles) if a.perfil == "todos" else [a.perfil]
    modos = ("estricto", "exploratorio") if a.modo == "ambos" and not a.demo else \
        (("estricto",) if a.modo == "ambos" else (a.modo,))
    kw = dict(umbral_cobertura=a.umbral_cobertura, umbral_faltantes=a.umbral_faltantes)

    if a.demo:
        print("\n*** DEMOSTRACIÓN CON DATOS FICTICIOS (Z-CERCA, Z-CLUSTER, Z-GRANOS): no representan ninguna "
              "región real ***")
    else:
        resumen_cobertura(filas)
    evs = {}
    for modo in modos:
        for p in sel:
            ev = evaluar(filas, perfiles[p], modo, **kw)
            evs[(modo, p)] = ev
            imprimir(ev, f"{p} ({nombres.get(p, p)})", a.detalle)
    if a.sensibilidad:
        for p in sel:
            base, sens = sensibilidad(filas, perfiles[p], a.sensibilidad, modos[0], **kw)
            print(f"\n### Sensibilidad perfil {p}: cada grupo × (1 ± {a.sensibilidad}) y renormalizado")
            if base is None:
                print("    Sin ranking base: la sensibilidad de orden no aplica (faltan datos).")
                continue
            print(f"    Orden base: {base}")
            for g, s, cambia, orden in sens:
                if cambia:
                    print(f"    {g} {'+' if s > 0 else '−'}{a.sensibilidad:.0%}: CAMBIA → {orden}")
            print(f"    Cambios de orden: {sum(1 for *_, c, _ in sens if c)} de {len(sens)} variaciones")
    if not a.demo and not a.sin_csv:
        escribir_resultados(evs, nombres)
        print(f"\nResultados escritos en {os.path.relpath(RESULTADOS)}")


if __name__ == "__main__":
    main()
