#!/usr/bin/env python3
"""
GENERADOR DE DATOS DEL SIMULADOR HTML v0.1 — 23_plan_expansion/simulador_html
============================================================================

Qué hace
--------
1. Importa, SIN MODIFICARLOS, los modelos aprobados:
     23_plan_expansion/modelo_escala.py            (v1.1)  -> que a su vez importa:
     03_produccion_primaria/modelo_escenarios_produccion.py (v1.1)
     04_balance_masa/modelo_balance_masa.py        (v1.1)
     07_subproductos/modelo_subproductos.py        (v1.0)
2. Ejecuta las pruebas de esos modelos (modelo_escala.ejecutar_tests: 23 propias + las de
   los tres modelos importados). Si alguna falla, se DETIENE y no escribe datos.
3. Exporta COEFICIENTES (no resultados precalculados por escala):
     - kg por ave de cada ítem y agregado físico, por configuración comercial (A/B/C) y por
       peso vivo en pasos de 0,1 kg dentro del rango válido del balance (2,0-3,8 kg), tal
       como los devuelve modelo_escala.kg_por_ave();
     - rendimientos por parte para los mixes (modelo_escala.rendimientos_mix) por peso;
     - parámetros de producción primaria (perfiles, desempeños, calendario, constantes);
     - escenarios de demanda (02_clientes_demanda/escenarios_demanda.csv vía
       modelo_escala.leer_demanda) y mixes M1-M3 (modelo_escala.leer_mixes);
     - perfiles de destino de inventario, carga de contenedor, aves por camión.
   El HTML aplica sobre ellos solo fórmulas lineales o cerradas documentadas en
   calculo.js (× aves, × días, ÷ horas, ÷ capacidad) y el port 1:1 de mp.calcular.
4. Exporta CASOS DE PRUEBA calculados en Python con las funciones de los modelos
   (producción con parámetros aleatorios y demanda vs capacidad M0-M3) y una
   REFERENCIA leída del CSV maestro (escenarios_escala.csv, bloque tabla_central), para
   que validar_simulador.js y la autoverificación del navegador comprueben que el
   JavaScript reproduce los modelos.
5. Escribe dos archivos con el MISMO contenido:
     data/simulador_data.json  (lectura por herramientas / validación)
     data/simulador_data.js    (window.SIMULADOR_DATA = {...}; lo carga index.html con
                                <script>, porque los navegadores bloquean fetch() de JSON
                                desde file://)

Uso
---
    python3 23_plan_expansion/simulador_html/generar_datos_simulador.py

NO editar a mano data/simulador_data.json ni data/simulador_data.js: se regeneran.
Sin precios, costos, CAPEX, OPEX ni indicadores financieros (el modelo de escala lo
verifica con su test T11 y este script vuelve a verificarlo sobre el JSON).
"""

from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import random
import re
import subprocess
import sys

sys.dont_write_bytecode = True           # no dejar __pycache__ en las carpetas de los modelos

AQUI = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.dirname(AQUI)             # 23_plan_expansion
RAIZ = os.path.dirname(PLAN)
sys.path.insert(0, PLAN)
import modelo_escala as me               # noqa: E402  (importa mp, mb y ms)

mp, mb, ms = me.mp, me.mb, me.ms

VERSION_SIMULADOR = "0.1"
SEMILLA = 20260930                       # casos de prueba reproducibles
N_CASOS_PRODUCCION = 300
N_CASOS_DEMANDA = 300
PASO_PESO = 0.1

ARCHIVOS_MODELO = {
    "escala": "23_plan_expansion/modelo_escala.py",
    "produccion": "03_produccion_primaria/modelo_escenarios_produccion.py",
    "balance": "04_balance_masa/modelo_balance_masa.py",
    "subproductos": "07_subproductos/modelo_subproductos.py",
    "csv_escala": "23_plan_expansion/escenarios_escala.csv",
    "demanda": "02_clientes_demanda/escenarios_demanda.csv",
    "mixes": "02_clientes_demanda/supermercados.md",
}
VERSIONES = {"escala": me.VERSION, "produccion": "1.1", "balance": mb.VERSION, "subproductos": ms.VERSION}

PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen|"
                                 r"ingresos?|rentabilidad)\b", re.IGNORECASE)


def sha256(ruta):
    with open(os.path.join(RAIZ, ruta), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def git(*args):
    try:
        return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True, check=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return ""


def pesos_validos():
    lo, hi = mb.RANGO_VALIDO
    n = int(round((hi - lo) / PASO_PESO))
    return [round(lo + i * PASO_PESO, 1) for i in range(n + 1)]


def clave_peso(p):
    return f"{p:.1f}"


# ---------------------------------------------------------------------------
# Coeficientes
# ---------------------------------------------------------------------------
def coeficientes_balance():
    out = {}
    for c in me.CONFIG_VARIANTE:
        out[c] = {}
        for p in pesos_validos():
            k, _ = me.kg_por_ave(c, p)
            out[c][clave_peso(p)] = {kk: float(v) for kk, v in k.items()}
    return out


def coeficientes_mix():
    return {clave_peso(p): {k: float(v) for k, v in me.rendimientos_mix(p).items()} for p in pesos_validos()}


def parametros():
    p_med, d_med = mp.PERFILES[me.PERFIL], mp.DESEMPENO[me.DESEMPENO]
    return {
        "escalas": list(me.ESCALAS),
        "calendarios": {str(k): v for k, v in me.CALENDARIOS.items()},
        "semanas_anio": me.SEMANAS_ANIO,
        "dias_calendario": me.DIAS_CALENDARIO,
        "horas_netas_ref": list(me.HORAS_NETAS),
        "utilizaciones_ref": list(me.UTILIZACIONES),
        "dias_inventario_ref": list(me.DIAS_INVENTARIO),
        "rango_peso": list(mb.RANGO_VALIDO),
        "paso_peso": PASO_PESO,
        "peso_ref": me.PESO_REF,
        "config_ref": me.CONFIG_REF,
        "nombre_config": mb.NOMBRE_CONFIG,
        "config_variante": me.CONFIG_VARIANTE,
        "variantes_subproductos": {v: d for v, (_, _, d) in ms.VARIANTES.items()},
        "produccion": {
            "perfil_ref": me.PERFIL, "desempeno_ref": me.DESEMPENO,
            "perfiles": mp.PERFILES, "desempenos": mp.DESEMPENO,
            "defaults": me.parametros_produccion(),
            "disponibilidad": mp.DISPONIBILIDAD,
            "tamanos_galpon_m2": mp.TAMANOS_GALPON_M2,
            "relacion_agua_alimento": mp.RELACION_AGUA_ALIMENTO,
            "consumo_acumulado_ref": {str(k): v for k, v in mp.CONSUMO_ACUMULADO_REF.items()},
            "claves_anuales": sorted(me.CLAVES_ANUALES),
            "fcr_base_medio": p_med["fcr_base"], "mort_medio": d_med["mort"],
        },
        "perfiles_destino": {k: {"nombre": n, "reparto": r} for k, (n, r) in me.PERFILES_DESTINO.items()},
        "contenedor_t": me.CONTENEDOR_T,
        "aves_por_camion_vivo": list(me.AVES_POR_CAMION_VIVO),
        "m2_por_productor": me.M2_POR_PRODUCTOR,
        "items": [{"clave": c, "etiqueta": e, "clase": sorted({mb.DESTINO[x][0] for x in comps})[0],
                   "componentes": sorted(comps)} for c, e, comps in me.ITEMS],
        "items_seccion_8": list(me.ITEMS_SECCION_8),
    }


def demanda():
    esc, locales = me.leer_demanda()
    ruta = os.path.join(RAIZ, "02_clientes_demanda", "escenarios_demanda.csv")
    with open(ruta, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    lista = []
    for r in filas:
        if r["bloque"] not in ("escenario_comercial", "red_supermercados"):
            continue
        lista.append({"id": r["id"], "bloque": r["bloque"], "nombre": r["escenario"], "descripcion": r["descripcion"],
                      "total_kg_dia": float(r["total_kg_dia"]), "exportacion_kg_dia": float(r["exportacion_kg_dia"]),
                      "categoria": r["categoria_demanda_actual"], "clasificacion": r["clasificacion_dato"],
                      "sumable_a_demanda": r["sumable_a_demanda"], "observaciones": r["observaciones"],
                      "canales": {k.replace("_kg_dia", ""): float(r[k]) for k in
                                  ("supermercados_kg_dia", "mayoristas_distribuidores_kg_dia",
                                   "carnicerias_pollerias_kg_dia", "gastronomia_kg_dia", "industria_kg_dia",
                                   "exportacion_kg_dia")}})
    mixes, f_mila = me.leer_mixes()
    return {"escenarios": lista, "ids_modelo_escala": list(esc), "locales": locales, "mixes": mixes,
            "factor_milanesa": f_mila, "rol_mix": me.ROL_MIX, "demanda_documentada_A_mas_B_kg_dia": 0.0}


# ---------------------------------------------------------------------------
# Casos de prueba (Python = verdad; el JS debe reproducirlos)
# ---------------------------------------------------------------------------
def produccion_completa(aves, ds, da, edad, peso, fcr, mort, doa, vacio, kg_m2):
    """Misma lógica que modelo_escala.produccion (mp.calcular + escalado de las claves anuales por
    días/año), pero con todos los parámetros de mp.calcular expuestos (DOA, días entre lotes y
    densidad, que modelo_escala fija en el desempeño medio)."""
    r = mp.calcular(aves, ds, edad=edad, peso=peso, fcr=fcr, mort=mort, doa=doa, vacio=vacio, kg_m2=kg_m2)
    k = da / me.CALENDARIOS[ds]
    for clave in me.CLAVES_ANUALES:
        r[clave] *= k
    r["dias_faena_anio"] = da
    return r


def casos_produccion(rng):
    casos = []
    # los 8 casos exactos de modelo_escala.produccion (desempeño medio, calendario SUP-025)
    for E in me.ESCALAS:
        for ds, da in me.CALENDARIOS.items():
            r = me.produccion(E, ds, da)
            casos.append({"entrada": {"aves": E, "dias_semana": ds, "dias_anio": da, **me.parametros_produccion()},
                          "salida": r})
    while len(casos) < N_CASOS_PRODUCCION:
        ds = rng.choice(list(me.CALENDARIOS))
        par = {"aves": round(rng.uniform(300, 30000), 1), "dias_semana": ds,
               "dias_anio": round(rng.uniform(150, ds * me.SEMANAS_ANIO), 1),
               "edad": rng.randint(35, 56), "peso": round(rng.choice(pesos_validos()), 1),
               "fcr": round(rng.uniform(1.4, 2.2), 2), "mort": round(rng.uniform(0, 0.15), 4),
               "doa": round(rng.uniform(0, 0.02), 4), "vacio": rng.randint(8, 30),
               "kg_m2": round(rng.uniform(25, 45), 1)}
        a = dict(par)
        r = produccion_completa(a.pop("aves"), a.pop("dias_semana"), a.pop("dias_anio"), **a)
        casos.append({"entrada": par, "salida": r})
    return casos


def casos_demanda(rng):
    mixes, f_mila = me.leer_mixes()
    casos = []
    for _ in range(N_CASOS_DEMANDA):
        peso = rng.choice(pesos_validos())
        config = rng.choice(list(me.CONFIG_VARIANTE))
        E = round(rng.uniform(500, 30000), 1)
        ds = rng.choice(list(me.CALENDARIOS))
        da = round(rng.uniform(150, ds * me.SEMANAS_ANIO), 1)
        D = round(rng.choice([rng.uniform(100, 5000), rng.uniform(5000, 60000)]), 1)
        metodo = rng.choice(["M0", "M1", "M2", "M3"])
        k, _ = me.kg_por_ave(config, peso)
        if metodo == "M0":
            res = {"aves_dia_cal": D / k["comestible"], "masa_demandada_ave": D, "comestible_por_ave_mix": k["comestible"],
                   "excedente_total": 0.0, "limitante": "ninguna (ave completa)", "fuera_balance": 0.0}
        else:
            res = me.aves_por_mix(D, mixes[metodo], me.rendimientos_mix(peso), f_mila)
        cmp_ = me.comparar_demanda(E, da, D, res)
        casos.append({"entrada": {"escala": E, "dias_semana": ds, "dias_anio": da, "demanda_kg_dia_cal": D,
                                  "metodo": metodo, "config": config, "peso": peso},
                      "salida": {**{kk: v for kk, v in cmp_.items()},
                                 "aves_dia_cal": res["aves_dia_cal"], "excedente_total": res["excedente_total"],
                                 "limitante": res["limitante"], "fuera_balance": res["fuera_balance"]}})
    return casos


def referencia_tabla_central():
    """Lee el bloque tabla_central del CSV maestro (no lo recalcula)."""
    ruta = os.path.join(RAIZ, ARCHIVOS_MODELO["csv_escala"])
    out = []
    with open(ruta, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["bloque"] == "tabla_central":
                out.append({"escala": int(r["escala_aves_dia"]), "dias_semana": int(r["dias_semana"]),
                            "dias_anio": int(r["dias_anio"]), "variable": r["variable"], "valor": float(r["valor"]),
                            "unidad": r["unidad"], "periodo": r["periodo"], "base": r["base"]})
    return out


# ---------------------------------------------------------------------------
def main():
    res = me.ejecutar_tests(verbose=False)
    fallas = [n for n, ok, _ in res if not ok]
    if fallas:
        print("DETENIDO: fallan pruebas de los modelos aprobados:\n  " + "\n  ".join(fallas))
        sys.exit(1)
    rng = random.Random(SEMILLA)
    data = {
        "meta": {
            "simulador_version": VERSION_SIMULADOR,
            "generado": dt.date.today().isoformat(),
            "generador": "23_plan_expansion/simulador_html/generar_datos_simulador.py",
            "versiones_modelos": VERSIONES,
            "fecha_modelo_escala": me.FECHA,
            "commit_repositorio": git("rev-parse", "--short", "HEAD"),
            "archivos_fuente": {k: {"ruta": v, "sha256": sha256(v),
                                    "ultimo_commit": git("log", "-1", "--format=%h %ad", "--date=short", "--", v)}
                                for k, v in ARCHIVOS_MODELO.items()},
            "tests_modelos": f"{sum(ok for _, ok, _ in res)}/{len(res)} (modelo_escala.ejecutar_tests, incluye "
                             f"producción, balance y subproductos)",
            "semilla_casos": SEMILLA,
            "aviso": "Escenarios físicos de orden de magnitud. Sin precios, costos, CAPEX, OPEX ni indicadores "
                     "financieros. No elige escala ni capacidad.",
        },
        "parametros": parametros(),
        "coeficientes": coeficientes_balance(),
        "rendimientos_mix": coeficientes_mix(),
        "demanda": demanda(),
        "referencia_tabla_central": referencia_tabla_central(),
        "casos_prueba": {"produccion": casos_produccion(rng), "demanda": casos_demanda(rng)},
    }
    texto = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    # control: ninguna clave económica en el JSON (las notas de texto de la demanda sí pueden mencionar
    # "precio" al describir datos faltantes, por eso se revisan solo las CLAVES)
    claves = set(re.findall(r'"([A-Za-z_0-9]+)":', texto))
    econ = [c for c in claves if PALABRAS_ECONOMICAS.search(c.replace("_", " "))]
    if econ:
        print(f"DETENIDO: claves económicas en los datos: {econ}")
        sys.exit(1)
    os.makedirs(os.path.join(AQUI, "data"), exist_ok=True)
    with open(os.path.join(AQUI, "data", "simulador_data.json"), "w", encoding="utf-8") as fh:
        fh.write(texto + "\n")
    with open(os.path.join(AQUI, "data", "simulador_data.js"), "w", encoding="utf-8") as fh:
        fh.write("// ARCHIVO GENERADO por generar_datos_simulador.py — NO EDITAR A MANO.\n"
                 "// Mismo contenido que simulador_data.json, embebido para abrir index.html desde file:// sin servidor.\n"
                 f"window.SIMULADOR_DATA = {texto};\n")
    print(f"Pruebas de los modelos: {data['meta']['tests_modelos']}")
    print(f"Datos generados: data/simulador_data.json y data/simulador_data.js ({len(texto) / 1024:.0f} KB); "
          f"{len(pesos_validos())} pesos × {len(me.CONFIG_VARIANTE)} configuraciones; "
          f"{N_CASOS_PRODUCCION} + {N_CASOS_DEMANDA} casos de prueba")


if __name__ == "__main__":
    main()
