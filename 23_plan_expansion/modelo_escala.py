#!/usr/bin/env python3
"""
MODELO PRELIMINAR DE ESCALA — versión 1.1 (2026-09-30, auditoría conceptual)
============================================================================

v1.1: separa utilización de planta (≤ 100 %), factor demanda/capacidad (puede > 100 %) y
cobertura de demanda (≤ 100 %); obliga a convertir día operativo ↔ día calendario antes de
comparar (función `cociente`); inventario con dos bases temporales (días de producción y días
calendario de cobertura); masa biológica comestible separada del agua retenida y del peso
comercial. Tests T16-T21 y mutaciones M15-M22.

Pregunta: ¿qué tiene que ser verdad para que 2.500 / 5.000 / 10.000 / 20.000
aves faenadas por día tengan sentido?

Integra, SIN MODIFICARLOS ni copiar sus fórmulas, tres modelos existentes:
  * 03_produccion_primaria/modelo_escenarios_produccion.py  (v1.1) -> pollitos, plazas,
    m² de galpón, alimento, agua de bebida, aves vivas simultáneas.
  * 04_balance_masa/modelo_balance_masa.py                  (v1.1) -> kg por ave de cada
    producto, coproducto, subproducto, residuo y pérdida.
  * 07_subproductos/modelo_subproductos.py                  (v1.0) -> variantes de
    configuración y rutas (V1 trozado, V3 deshuesado, V6 entero), agrupación sin doble
    conteo y carga de contenedor de referencia.
y lee dos fuentes de datos de la demanda (sin copiarlas):
  * 02_clientes_demanda/escenarios_demanda.csv   -> escenarios comerciales de prueba.
  * 02_clientes_demanda/supermercados.md §2.2 / §2.3 -> mixes hipotéticos M1-M3 y
    factor de pechuga por kg de milanesa (SUP-023).

ESTADO: ESCENARIOS FÍSICOS de orden de magnitud. NO elige escala, NO fija capacidad
(regla 9), NO calcula CAPEX, OPEX, precios, márgenes ni indicadores financieros,
NO selecciona maquinaria, proveedores, layout ni localización.

Uso
---
    python3 23_plan_expansion/modelo_escala.py                # tests + CSV
    python3 23_plan_expansion/modelo_escala.py --solo-tests   # solo pruebas
    python3 23_plan_expansion/modelo_escala.py --tablas       # + tablas para los .md
    python3 23_plan_expansion/modelo_escala.py --mutaciones   # prueba de mutación de los tests
    python3 23_plan_expansion/modelo_escala.py --escenario --aves-dia 7500 --dias-semana 6 \
        --dias-anio 290 --peso 3.1 --mortalidad 0.07 --fcr 1.78 --config C \
        --utilizacion 0.6 --dias-inventario 5 --horas-netas 8 --demanda ESC-BAS
                                                             # sensibilidad (no escribe CSV)

El script se DETIENE (código 1) si falla cualquier prueba propia o de los modelos
importados (producción 10 grupos, balance 21, subproductos 9).

------------------------------------------------------------------------------
DEFINICIONES (SUP-052)
------------------------------------------------------------------------------
  ESCALA E [aves/día]      = aves EFECTIVAMENTE FAENADAS por día operativo cuando la
                             planta trabaja a su capacidad operativa (utilización 100 %).
  Capacidad nominal        = ritmo nominal de línea [aves/h] × horas netas/día. Depende de
                             equipos NO seleccionados: no se calcula. Nominal ≥ operativa.
  Capacidad operativa      = aves/día sostenibles con las restricciones reales (personal,
                             frío, efluentes, abastecimiento, cuello de botella). En este
                             modelo es la ESCALA E.
  Aves realmente faenadas  = E × u
  Utilización u            = aves realmente faenadas / capacidad operativa.
  Capacidad ≠ demanda ≠ ventas: la demanda se lee de 02_clientes_demanda y se COMPARA
  con la capacidad; nunca la define (tests T12).

------------------------------------------------------------------------------
CALENDARIOS Y PERÍODOS (SUP-025; nunca se mezclan)
------------------------------------------------------------------------------
  5 días/semana -> 250 días operativos/año; 6 días/semana -> 300 días/año (por defecto;
  --dias-anio permite otro valor ≤ días/semana × 52,14).
  día operativo   : día con faena.        día calendario : 365 por año (unidad de la demanda).
  semana plena    : semana sin feriados   (ritmo nominal; dimensiona granjas y pollitos).
  semana promedio : total anual / 52,14   (incluye feriados).
  Conversión:  X/día calendario = X/día operativo × días operativos/año / 365.

------------------------------------------------------------------------------
FÓRMULAS PROPIAS (todo lo demás se importa)
------------------------------------------------------------------------------
  Ritmo de línea [aves/h]            = aves faenadas/día / horas NETAS de faena/día
                                       (horas netas ≠ horas de turno; sin eficiencia de máquina)
  Aves procesadas (utilización u)    = E × u
  t/día operativo de un material     = kg/ave (balance v1.1) × aves faenadas/día / 1.000
  t/año                              = t/día operativo × días operativos/año
  Inventario [t]                     = ver "Inventario" más abajo (dos bases temporales)
  Camiones/día                       = t/día / capacidad útil por camión (capacidad = VARIABLE
                                       sin valor, DPV-084); aves vivas: aves cargadas/día /
                                       aves por camión (SUP-033: 4.000-7.000, sin fuente)
  Días para completar un contenedor  = carga [t] × 1.000 / (kg/ave × aves/día)  (25 t [PVDP])
  Productores necesarios             = m² de galpón / m² por productor (VARIABLE pendiente,
                                       DPV-048; el modelo no la inventa)

  Tres métricas que NO se confunden (SUP-060):
     factor_demanda_capacidad = aves requeridas por la demanda / capacidad   (puede superar 100 %)
     utilizacion_planta       = aves procesadas / capacidad = min(factor, 100 %)
     cobertura_demanda        = producción posible / demanda = min(1 / factor, 100 %)
     kg atendidos = D × cobertura; kg no atendidos = D × (1 − cobertura);
     capacidad ociosa [aves/día operativo] = E × (1 − utilización)
  Bases temporales: la demanda está en día CALENDARIO y la capacidad en día OPERATIVO; solo se
     comparan tras `convertir` (× días operativos / 365); `cociente` rechaza períodos distintos.
  Inventario (SUP-056):  días de producción  = producción/día operativo × días
                         días calendario     = despacho promedio/día calendario × días
                         (despacho promedio/día cal. = producción/día op. × días op. / 365)
  Masa: peso comercial = masa biológica comestible + agua retenida en producto (SUP-042).

  Demanda vs capacidad (SUP-054; demanda en kg de PRODUCTO COMERCIAL por DÍA CALENDARIO):
  M0 "ave completa" (cota INFERIOR de aves): toda la masa comestible del ave (A + B,
     con agua retenida) se vende dentro de la demanda:
         aves/día cal = D / kg comestible por ave (configuración elegida)
  M1-M3 "parte limitante" (mixes hipotéticos de supermercados.md §2.2, rendimientos del
     balance v1.1 en lugar de los ilustrativos):
         aves entero   = kg entero / kg de pollo entero por ave (config. A)
         aves trozado  = max(pechuga deshuesada requerida / kg suprema+solomillo por ave,
                             kg pata-muslo / kg por ave, kg alas / kg por ave,
                             menudencias faltantes / kg por ave)
         pechuga requerida = kg pechuga + kg milanesa × 0,75 (SUP-023)
         "otros elaborados" quedan FUERA del balance (SUP-023)
         excedentes = producido − demandado por parte + partes comestibles no demandadas
  Factor demanda/capacidad = aves/día cal / (E × días operativos / 365)
  kg sin destino a plena escala = producción comestible a plena escala − masa demandada
  Demanda adicional para llenar la planta (mismo mix) = D × (E_cal / aves/día cal − 1)

Unidades: aves; kg; t = 1.000 kg; m²; m³; h. Separador decimal del CSV: punto.
Bases (regla 14): "vivo" (peso vivo), "comercial" (masa biológica + agua retenida en
producto), "biologica+agua" (subproductos con agua adherida), "alimento", "agua".
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True           # no dejar __pycache__ en las carpetas de los modelos

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.environ.get("MODELO_ESCALA_RAIZ") or os.path.dirname(AQUI)
for carpeta in ("03_produccion_primaria", "04_balance_masa", "07_subproductos"):
    sys.path.insert(0, os.path.join(RAIZ, carpeta))
import modelo_escenarios_produccion as mp  # noqa: E402  (producción primaria v1.1)
import modelo_balance_masa as mb           # noqa: E402  (balance de masa v1.1)
import modelo_subproductos as ms           # noqa: E402  (subproductos v1.0)

VERSION = "1.1"
FECHA = "2026-09-30"

# ---------------------------------------------------------------------------
# 1. PARÁMETROS (importados cuando existen; propios solo si son nuevos)
# ---------------------------------------------------------------------------
ESCALAS = list(mp.PLANTAS_AVES_FAENADAS_DIA)        # 2.500 / 5.000 / 10.000 / 20.000
CALENDARIOS = dict(mp.DIAS_FAENA_ANIO)              # {5: 250, 6: 300}  (SUP-025)
SEMANAS_ANIO = mp.SEMANAS_ANIO                      # 365 / 7
DIAS_CALENDARIO = 365
HORAS_NETAS = (6, 8, 10, 16)                        # 16 = dos turnos de 8 h netas (SUP-053)
UTILIZACIONES = (0.30, 0.50, 0.70, 0.85, 1.00)
DIAS_INVENTARIO = (1, 3, 7, 14)
PERFIL, DESEMPENO = "medio", "medio"                # escenario medio de producción (SUP-026/027)
PESO_REF = mp.PERFILES[PERFIL]["peso"]              # 2,9 kg
REND, COND, ENF = ms.REND, ms.COND, ms.ENF          # medio / medio / inmersión (SUP-050)
CONFIG_VARIANTE = {"A": "V6", "B": "V1", "C": "V3"} # variantes de 07_subproductos
CONFIG_REF = "B"                                    # trozado V1 = referencia (SUP-050), no decisión
CONTENEDOR_T = ms.CARGA_CONTENEDOR_T                # 25 t por reefer 40' [PVDP · débil] FTE-135
AVES_POR_CAMION_VIVO = (4000, 7000)                 # SUP-033 (sin fuente; orden de magnitud)
M2_POR_PRODUCTOR = None                             # DPV-048: pendiente, NO se inventa

# Perfiles ilustrativos de destino del producto para el inventario (SUP-055). NO son datos
# ni demanda: la exportación de la demanda es 0 (SUP-022); P3 prueba la opción de diseño.
PERFILES_DESTINO = {
    "P1": ("Mercado interno fresco", {"refrigerado": 0.90, "congelado": 0.10, "exportacion": 0.00}),
    "P2": ("Mercado interno con congelado", {"refrigerado": 0.60, "congelado": 0.40, "exportacion": 0.00}),
    "P3": ("Opción exportadora (prueba de diseño)", {"refrigerado": 0.50, "congelado": 0.30, "exportacion": 0.20}),
}

# Partición de TODOS los componentes del balance v1.1 en ítems físicos (cada componente en
# UN solo ítem: test T06). Etiqueta, componentes, base.
ITEMS = [
    ("pollo_entero", "Pollo entero", {"pollo entero"}),
    ("pechuga", "Pechuga con hueso", {"pechuga con hueso"}),
    ("pechuga_deshuesada", "Suprema + solomillo", {"suprema", "solomillo"}),
    ("pata_muslo", "Pata-muslo", {"pata-muslo"}),
    ("pata_muslo_procesada", "Muslo deshuesado + pata", {"muslo deshuesado", "pata con hueso", "pata deshuesada"}),
    ("alas", "Alas", {"alas"}),
    ("carcasa_esqueleto", "Carcasa-esqueleto", {"carcasa-esqueleto"}),
    ("cms", "CMS", {"CMS"}),
    ("cuello", "Cuello", {"cuello"}),
    ("menudencias", "Menudencias (hígado + corazón + molleja)", {"higado", "corazon", "molleja"}),
    ("garras", "Garras (grado A + segunda)", {"garras grado A", "garras de segunda"}),
    ("recortes_piel", "Recortes y piel comestibles", {"recortes", "piel"}),
    ("sangre", "Sangre recuperada", {"sangre recuperada"}),
    ("plumas", "Plumas crudas húmedas", {"plumas crudas"}),
    ("visceras", "Vísceras no comestibles", {"tracto digestivo", "pulmones", "otros no comestibles"}),
    ("cabeza", "Cabezas", {"cabeza"}),
    ("huesos", "Huesos y residuo óseo de CMS", {"hueso", "residuo oseo de CMS"}),
    ("otros_c", "Otros subproductos C (garras descarte, piel/grasa a rendering)",
     {"garras descarte", "piel a rendering", "grasa abdominal retirada"}),
    ("residuos", "Residuos y efluentes (clase D)",
     {"contenido gastrointestinal", "decomiso total", "decomiso parcial", "sangre no recuperada",
      "merma de acondicionamiento de patas", "agua de goteo del producto"}),
    ("perdidas", "Mermas y pérdidas (clase P)",
     {"merma de trozado", "merma de deshuese", "merma de CMS", "evaporacion en enfriamiento",
      "perdidas no asignadas"}),
]
# Ítems pedidos para el balance por escala (§8 del encargo); el resto va a "otros".
ITEMS_SECCION_8 = ("pechuga", "pata_muslo", "alas", "carcasa_esqueleto", "cuello", "menudencias",
                   "garras", "sangre", "plumas", "visceras", "cabeza", "residuos")
SOLIDOS_D = {"contenido gastrointestinal", "decomiso total", "decomiso parcial"}

# Mix de supermercados.md §2.2 -> rol físico (test T13 exige que todo producto tenga rol)
ROL_MIX = {"Pollo entero": "entero", "Pechuga / suprema / filet": "pechuga", "Pata-muslo": "pata_muslo",
           "Alas": "alas", "Milanesas (de pechuga)": "milanesa", "Menudencias": "menudencias",
           "Otros elaborados (hamburguesas, nuggets, marinados)": "fuera_balance"}

UNIDADES_VALIDAS = {"aves", "aves/h", "pollitos", "plazas", "t", "kg", "kg/ave", "m²", "m³", "galpones",
                    "%", "ratio", "días", "contenedores/mes", "camiones", "productores", "índice"}
PALABRAS_ECONOMICAS = re.compile(r"\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen|"
                                 r"ingreso|ingresos|venta_usd|rentabilidad)\b|\$", re.IGNORECASE)


class ErrorEscala(Exception):
    """Error de parámetros o de consistencia: detiene el modelo."""


# ---------------------------------------------------------------------------
# 2. PRODUCCIÓN PRIMARIA (envoltorio de mp.calcular; no recalcula nada)
# ---------------------------------------------------------------------------
CLAVES_ANUALES = {
    "aves_faenadas_anio", "aves_cargadas_anio", "pollitos_alojados_anio", "pollitos_alojados_semana_promedio",
    "mortalidad_granja_aves_anio", "mortalidad_transporte_aves_anio", "utilizacion_anual_galpones",
    "inventario_aves_promedio_anual", "kg_vivo_cargado_anio", "alimento_t_anio", "alimento_t_mes_promedio",
    "alimento_t_semana_promedio", "alimento_inicio_t_anio", "alimento_crecimiento_t_anio",
    "alimento_terminacion_t_anio", "agua_bebida_m3_anio", "agua_bebida_m3_dia_promedio"}
CLAVES_NO_ANUALES = {
    "dias_faena_anio", "aves_faenadas_semana_plena", "aves_cargadas_dia", "aves_cargadas_semana_plena",
    "pollitos_alojados_por_dia_faena", "pollitos_alojados_semana_plena", "ciclo_total_dias", "ciclos_anio",
    "capacidad_alojamiento_pollitos", "inventario_aves_ritmo_pleno", "m2_galpon", "pollitos_m2_alojamiento",
    "galpones_1200m2", "galpones_1800m2", "galpones_2400m2", "alimento_por_ave_faenada_kg",
    "alimento_por_pollito_alojado_kg", "alimento_t_semana_plena", "alimento_ciclo_crianza_t",
    "agua_bebida_m3_semana_plena"}


def parametros_produccion(peso=None, edad=None, fcr=None, mort=None):
    p, d = mp.PERFILES[PERFIL], mp.DESEMPENO[DESEMPENO]
    return {"edad": edad or p["edad"], "peso": peso or p["peso"],
            "fcr": fcr or round(p["fcr_base"] + d["d_fcr"], 2),
            "mort": d["mort"] if mort is None else mort, "doa": d["doa"], "vacio": d["vacio"], "kg_m2": d["kg_m2"]}


def produccion(aves_faenadas_dia, dias_semana=5, dias_anio=None, **kw):
    """Variables de producción primaria para aves_faenadas_dia (mp.calcular, perfil y desempeño
    medios). Si dias_anio difiere del calendario de SUP-025, las variables anuales se escalan
    linealmente por dias_anio / días de referencia (las de semana plena no cambian)."""
    if dias_semana not in CALENDARIOS:
        raise ErrorEscala(f"días/semana {dias_semana}: el modelo de producción solo admite {list(CALENDARIOS)}")
    base = CALENDARIOS[dias_semana]
    dias_anio = base if dias_anio is None else dias_anio
    if not 0 < dias_anio <= dias_semana * SEMANAS_ANIO:
        raise ErrorEscala(f"{dias_anio} días/año incompatible con {dias_semana} días/semana")
    r = mp.calcular(aves_faenadas_dia, dias_semana, **parametros_produccion(**kw))
    k = dias_anio / base
    for clave in CLAVES_ANUALES:
        r[clave] *= k
    r["dias_faena_anio"] = dias_anio
    return r


# ---------------------------------------------------------------------------
# 3. BALANCE DE MASA (kg por ave desde el balance v1.1 vía las variantes de 07)
# ---------------------------------------------------------------------------
def balance_config(config=CONFIG_REF, peso=PESO_REF, enfriamiento=ENF):
    if config not in CONFIG_VARIANTE:
        raise ErrorEscala(f"Configuración {config} inexistente (A entero / B trozado / C deshuesado)")
    cfg, rutas, _ = ms.VARIANTES[CONFIG_VARIANTE[config]]
    b = mb.balance(peso, cfg, REND, COND, enfriamiento, rutas)
    mb.verificar_cierre(b)
    return b


def kg_por_ave(config=CONFIG_REF, peso=PESO_REF, enfriamiento=ENF):
    """kg por ave de cada ítem y agregados físicos. Salvo las claves *_bio y agua_*, los valores son
    masa biológica + agua incorporada (peso COMERCIAL para productos; SUP-042): el agua retenida
    se vende con el producto pero NUNCA es carne."""
    b = balance_config(config, peso, enfriamiento)
    ms.agrupar(b)                                   # falla si un componente no tiene grupo
    tot = lambda comps: sum(f["bio"] + f["agua"] for f in b["filas"] if f["componente"] in comps)
    cla = lambda c: sum(f["bio"] + f["agua"] for f in b["filas"] if f["clase"] == c)
    etapa = lambda pref: sum(f["bio"] for f in b["filas"] if f["etapa"].startswith(pref))
    k = {clave: tot(comps) for clave, _, comps in ITEMS}
    k["otros_seccion_8"] = sum(k[c] for c, _, _ in ITEMS if c not in ITEMS_SECCION_8)
    k.update({
        "peso_vivo": b["entrada_bio"], "agua_incorporada": b["entrada_agua"],
        "producto_principal": cla("A"), "coproductos": cla("B"), "comestible": cla("A") + cla("B"),
        "subproductos_c": cla("C"), "residuos_d": cla("D"), "perdidas_p": cla("P"),
        "agua_retenida_comestible": sum(f["agua"] for f in b["filas"] if f["clase"] in "AB"),
        # masa biológica (carne y tejidos) SIN agua retenida: nunca aumenta por el chiller
        "comestible_bio": sum(f["bio"] for f in b["filas"] if f["clase"] in "AB"),
        "producto_principal_bio": sum(f["bio"] for f in b["filas"] if f["clase"] == "A"),
        "rendering_potencial": cla("C"),                                 # = D01 de 07_subproductos
        "solidos_a_retirar": cla("C") + tot(SOLIDOS_D),                  # = D02 (C + decomisos + contenido)
        "efluente_o_perdida": cla("D") - tot(SOLIDOS_D) + cla("P"),      # no se transporta
        "c_perecedero_sin_plumas": cla("C") - tot({"plumas crudas"}),
        "garras_grado_a": tot({"garras grado A"}),
        "sangre_drenada": tot({"sangre recuperada", "sangre no recuperada"}),
        "plumas_bio": sum(f["bio"] for f in b["filas"] if f["componente"] == "plumas crudas"),
        # rutas alternativas: fila NO sumable (SUP-045); misma regla que el balance
        "cms_alternativa_no_sumable": (sum(f["bio"] for f in b["filas"] if f["componente"] == "carcasa-esqueleto")
                                       * mb.CMS_RENDIMIENTO[REND]),
        # proxies físicos de procesamiento (kg de masa biológica que pasa por cada operación)
        "kg_trozado": etapa("trozado") + etapa("deshuese"),
        "kg_deshuese": etapa("deshuese"),
        "kg_cms": etapa("CMS"),
        "flujos_comestibles": float(len({f["componente"] for f in b["filas"] if f["clase"] in "AB"
                                          and f["bio"] + f["agua"] > 0})),
    })
    return k, b


# ---------------------------------------------------------------------------
# 4. DEMANDA (lectura; nunca define capacidad)
# ---------------------------------------------------------------------------
def leer_demanda():
    ruta = os.path.join(RAIZ, "02_clientes_demanda", "escenarios_demanda.csv")
    with open(ruta, encoding="utf-8") as fh:
        filas = list(csv.DictReader(fh))
    esc = {r["id"]: r for r in filas if r["bloque"] == "escenario_comercial"}
    locales = max(int(r["locales"]) for r in filas if r["bloque"] == "red_supermercados")
    return esc, locales


def leer_mixes():
    ruta = os.path.join(RAIZ, "02_clientes_demanda", "supermercados.md")
    with open(ruta, encoding="utf-8") as fh:
        txt = fh.read()
    sec = txt.split("### 2.2")[1].split("**Aplicado")[0]
    mixes = {"M1": {}, "M2": {}, "M3": {}}
    for linea in sec.splitlines():
        c = [x.strip() for x in linea.strip().strip("|").split("|")]
        if len(c) == 4 and c[1].endswith("%") and not c[0].startswith("**"):
            for m, v in zip(mixes, c[1:]):
                mixes[m][c[0]] = float(v.replace("%", "").replace(",", ".").strip()) / 100
    mila = re.search(r"1 kg de milanesa requiere ([\d,]+) kg de pechuga", txt)
    if not mila:
        raise ErrorEscala("No se encontró el factor pechuga/milanesa en supermercados.md §2.3")
    return mixes, float(mila.group(1).replace(",", "."))


def rendimientos_mix(peso=PESO_REF):
    """Rendimientos por parte (kg comerciales/ave) del balance v1.1 para los mixes."""
    ka, ba = kg_por_ave("A", peso)
    kb, bb = kg_por_ave("B", peso)
    kc, bc = kg_por_ave("C", peso)
    deshuese_pech_ab = sum(f["bio"] + f["agua"] for f in bc["filas"]
                           if f["etapa"] == "deshuese pechuga" and f["clase"] in "AB")
    return {
        "entero": ka["pollo_entero"], "pechuga": kc["pechuga_deshuesada"], "pata_muslo": kb["pata_muslo"],
        "alas": kb["alas"], "menudencias": kb["menudencias"],
        "comestible_ave_entero": ka["comestible"],
        # ave trozada con pechuga deshuesada: trozado B + deshuese de pechuga de C (misma carcasa fría)
        "comestible_ave_trozada": kb["comestible"] - kb["pechuga"] + deshuese_pech_ab,
    }


def aves_por_mix(D, mix, y, factor_milanesa):
    """Aves/día calendario por la parte limitante y excedentes (kg/día calendario)."""
    kg = {rol: 0.0 for rol in set(ROL_MIX.values())}
    for prod, pct in mix.items():
        kg[ROL_MIX[prod]] += D * pct
    n_ent = kg["entero"] / y["entero"]
    pech_req = kg["pechuga"] + kg["milanesa"] * factor_milanesa
    cand = {"pechuga (incluye milanesas)": pech_req / y["pechuga"], "pata-muslo": kg["pata_muslo"] / y["pata_muslo"],
            "alas": kg["alas"] / y["alas"],
            "menudencias": max(0.0, kg["menudencias"] / y["menudencias"] - n_ent)}
    limitante = max(cand, key=cand.get)
    n_tro = cand[limitante]
    n = n_ent + n_tro
    exc = {"pechuga": n_tro * y["pechuga"] - pech_req, "pata_muslo": n_tro * y["pata_muslo"] - kg["pata_muslo"],
           "alas": n_tro * y["alas"] - kg["alas"], "menudencias": n * y["menudencias"] - kg["menudencias"]}
    otras = (n_tro * (y["comestible_ave_trozada"] - y["pechuga"] - y["pata_muslo"] - y["alas"] - y["menudencias"])
             + n_ent * (y["comestible_ave_entero"] - y["entero"] - y["menudencias"]))
    demandada_ave = kg["entero"] + pech_req + kg["pata_muslo"] + kg["alas"] + kg["menudencias"]
    producida = n_ent * y["comestible_ave_entero"] + n_tro * y["comestible_ave_trozada"]
    return {"aves_dia_cal": n, "aves_entero": n_ent, "aves_trozado": n_tro, "limitante": limitante,
            "excedentes": exc, "otras_partes": otras, "excedente_total": sum(exc.values()) + otras,
            "masa_demandada_ave": demandada_ave, "masa_producida": producida,
            "fuera_balance": kg["fuera_balance"], "comestible_por_ave_mix": producida / n if n else 0.0}


PERIODOS_POR_ANIO = ("dia_operativo", "dia_calendario", "anio")


def convertir(valor, de, a, dias_anio):
    """Convierte un flujo entre día operativo (dias_anio por año), día calendario (365) y año.
    Única vía permitida para pasar de una base temporal a otra (SUP-020, SUP-025, SUP-060)."""
    por_anio = {"dia_operativo": dias_anio, "dia_calendario": DIAS_CALENDARIO, "anio": 1}
    if de not in por_anio or a not in por_anio:
        raise ErrorEscala(f"Conversión no definida: {de} -> {a}")
    return valor * por_anio[de] / por_anio[a]


def cociente(num, den):
    """num, den = (valor, periodo). Impide comparar flujos de bases temporales distintas
    (p. ej. t/día de faena contra t/día calendario de demanda) sin convertir antes."""
    if num[1] != den[1]:
        raise ErrorEscala(f"Comparación inválida: {num[1]} contra {den[1]} sin conversión")
    return num[0] / den[0] if den[0] else math.inf


def comparar_demanda(E, dias_anio, D, res):
    """Demanda vs capacidad con TRES métricas que no deben confundirse (SUP-060):
      factor_demanda_capacidad = capacidad requerida por la demanda / capacidad instalada (puede > 100 %)
      utilizacion_planta       = aves procesadas / capacidad = min(factor, 100 %)  (0-100 %)
      cobertura_demanda        = producción posible / demanda requerida = min(1 / factor, 100 %)
    D en kg de producto COMERCIAL por día CALENDARIO; la capacidad E en aves por día OPERATIVO:
    se comparan solo después de convertir E a día calendario. res = resultado de M0 o de un mix.
    Si la demanda excede la escala, la planta atiende la fracción 'cobertura' de la demanda (mismo
    mix) y sus excedentes de partes escalan en la misma proporción."""
    n = res["aves_dia_cal"]
    cap_cal = convertir(E, "dia_operativo", "dia_calendario", dias_anio)
    factor = cociente((n, "dia_calendario"), (cap_cal, "dia_calendario"))
    utiliz = min(1.0, factor)
    cobertura = min(1.0, 1 / factor) if factor else 1.0
    com = res["comestible_por_ave_mix"]
    return {
        "factor_demanda_capacidad": factor,
        "utilizacion_planta": utiliz,
        "cobertura_demanda": cobertura,
        "aves_necesarias_dia_operativo": convertir(n, "dia_calendario", "dia_operativo", dias_anio),
        "aves_procesadas_dia_operativo": E * utiliz,
        "aves_faltantes_dia_operativo": max(0.0, convertir(n, "dia_calendario", "dia_operativo", dias_anio) - E),
        "capacidad_ociosa_aves_dia_operativo": E * (1 - utiliz),
        "kg_atendidos_dia_cal": D * cobertura,
        "kg_no_atendidos_dia_cal": D * (1 - cobertura),
        "produccion_comestible_plena_kg_dia_cal": cap_cal * com,
        "kg_sin_destino_plena_escala": res["excedente_total"] * cobertura + max(0.0, cap_cal - n) * com,
        "demanda_adicional_para_llenar_kg_dia_cal": max(0.0, D * (1 / factor - 1)) if factor else 0.0,
    }


# ---------------------------------------------------------------------------
# 5. CONSTRUCCIÓN DE FILAS DEL CSV
# ---------------------------------------------------------------------------
CAMPOS = ["bloque", "escala_aves_dia", "dias_semana", "dias_anio", "parametro", "variable", "valor", "unidad",
          "periodo", "base", "fuente_modelo", "clasificacion", "sumable", "nota"]
F_PROD = "03_produccion_primaria/modelo_escenarios_produccion.py (v1.1)"
F_BAL = "04_balance_masa/modelo_balance_masa.py (v1.1) vía 07_subproductos/modelo_subproductos.py"
F_DEM = "02_clientes_demanda/escenarios_demanda.csv + supermercados.md §2.2"
F_PROPIO = "23_plan_expansion/modelo_escala.py"


class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, ds, da, variable, valor, unidad, periodo, base, fuente, parametro="",
            clasif="[ESTIMACIÓN]", sumable="-", nota=""):
        self.filas.append({"bloque": bloque, "escala_aves_dia": E, "dias_semana": ds, "dias_anio": da,
                           "parametro": parametro, "variable": variable, "valor": valor, "unidad": unidad,
                           "periodo": periodo, "base": base, "fuente_modelo": fuente, "clasificacion": clasif,
                           "sumable": sumable, "nota": nota})

    def valor(self, **filtro):
        res = [f["valor"] for f in self.filas if all(f[k] == v for k, v in filtro.items())]
        if len(res) != 1:
            raise ErrorEscala(f"Búsqueda ambigua o vacía ({len(res)}): {filtro}")
        return res[0]


VARS_PRODUCCION = [  # (clave mp, variable, unidad, periodo, base)
    ("pollitos_alojados_semana_plena", "pollitos_bb_semana_plena", "pollitos", "semana_plena", "aves"),
    ("pollitos_alojados_semana_promedio", "pollitos_bb_semana_promedio", "pollitos", "semana_promedio", "aves"),
    ("pollitos_alojados_anio", "pollitos_bb_anio", "pollitos", "anio", "aves"),
    ("aves_cargadas_dia", "aves_cargadas_dia_operativo", "aves", "dia_operativo", "aves"),
    ("aves_cargadas_anio", "aves_cargadas_anio", "aves", "anio", "aves"),
    ("aves_faenadas_semana_plena", "aves_faenadas_semana_plena", "aves", "semana_plena", "aves"),
    ("aves_faenadas_anio", "aves_faenadas_anio", "aves", "anio", "aves"),
    ("capacidad_alojamiento_pollitos", "plazas_simultaneas_granja", "plazas", "stock", "aves"),
    ("m2_galpon", "m2_galpones", "m²", "stock", "superficie"),
    ("galpones_1200m2", "galpones_equivalentes_1200m2", "galpones", "stock", "superficie"),
    ("galpones_2400m2", "galpones_equivalentes_2400m2", "galpones", "stock", "superficie"),
    ("alimento_t_semana_plena", "alimento_t_semana_plena", "t", "semana_plena", "alimento"),
    ("alimento_t_semana_promedio", "alimento_t_semana_promedio", "t", "semana_promedio", "alimento"),
    ("alimento_t_anio", "alimento_t_anio", "t", "anio", "alimento"),
    ("alimento_ciclo_crianza_t", "alimento_un_ciclo_de_crianza_t", "t", "stock", "alimento"),
    ("agua_bebida_m3_semana_plena", "agua_bebida_m3_semana_plena", "m³", "semana_plena", "agua"),
    ("agua_bebida_m3_anio", "agua_bebida_m3_anio", "m³", "anio", "agua"),
    ("agua_bebida_m3_dia_promedio", "agua_bebida_m3_dia_calendario_promedio", "m³", "dia_calendario", "agua"),
    ("inventario_aves_ritmo_pleno", "aves_vivas_simultaneas_ritmo_pleno", "aves", "stock", "aves"),
    ("inventario_aves_promedio_anual", "aves_vivas_simultaneas_promedio_anual", "aves", "stock", "aves"),
]


def construir(peso=PESO_REF, config=CONFIG_REF, escalas=None, calendarios=None, prod_kw=None,
              demanda_override=None):
    """Genera todas las filas. demanda_override (solo tests) reemplaza las demandas leídas."""
    escalas = escalas or ESCALAS
    calendarios = calendarios or CALENDARIOS
    prod_kw = prod_kw or {}
    t = Tabla()
    k, _ = kg_por_ave(config, peso)
    kcfg = {c: kg_por_ave(c, peso)[0] for c in CONFIG_VARIANTE}
    demanda, locales = leer_demanda()
    if demanda_override:
        for i, v in demanda_override.items():
            demanda[i] = dict(demanda[i], total_kg_dia=str(v))
    mixes, f_mila = leer_mixes()
    y = rendimientos_mix(peso)
    cfg_txt = f"config={config}; peso={peso}"

    for E in escalas:
        for ds, da_ref in calendarios.items():
            da = da_ref
            aves = E
            # --- 1. capacidad y ritmo de línea ---------------------------------------
            t.add("capacidad", E, ds, da, "escala_aves_faenadas_dia_operativo", E, "aves", "dia_operativo", "aves",
                  F_PROPIO, clasif="[SUPUESTO]", nota="Escala = capacidad operativa (u = 100 %); SUP-052")
            t.add("capacidad", E, ds, da, "aves_faenadas_anio_plena_escala", E * da, "aves", "anio", "aves", F_PROPIO)
            t.add("capacidad", E, ds, da, "aves_faenadas_dia_calendario_equivalente", E * da / DIAS_CALENDARIO,
                  "aves", "dia_calendario", "aves", F_PROPIO)
            for h in HORAS_NETAS:
                t.add("ritmo_linea", E, ds, da, "aves_por_hora_neta", E / h, "aves/h", "hora", "aves", F_PROPIO,
                      parametro=f"horas_netas={h}", nota="16 h = dos turnos de 8 h netas" if h == 16 else "")
                t.add("ritmo_linea", E, ds, da, "kg_vivo_por_hora_neta", E * peso / h, "kg", "hora", "vivo",
                      F_PROPIO, parametro=f"horas_netas={h}")
            # --- 2. producción primaria (u = 100 %) ------------------------------------
            r = produccion(aves, ds, da, peso=peso, **prod_kw)
            for clave, var, uni, per, base in VARS_PRODUCCION:
                t.add("produccion_primaria", E, ds, da, var, r[clave], uni, per, base, F_PROD,
                      parametro="perfil=medio; desempeno=medio")
            for n_gal in (1, 2, 4):
                t.add("abastecimiento", E, ds, da, "productores_equivalentes_si_cada_uno_tiene_n_galpones_2400m2",
                      r["m2_galpon"] / (n_gal * 2400), "productores", "stock", "superficie", F_PROPIO,
                      parametro=f"galpones_por_productor={n_gal}", clasif="[ESTIMACIÓN] ilustrativa",
                      nota="Aritmética sobre galpones equivalentes; el dato real es DPV-048")
            t.add("abastecimiento", E, ds, da, "productores_necesarios", "", "productores", "stock", "superficie",
                  F_PROPIO, clasif="[PENDIENTE DE VALIDACIÓN]",
                  nota="= m2_galpones / m2_por_productor; m2_por_productor sin dato (DPV-048)")
            # --- 3. utilización -----------------------------------------------------------
            for u in UTILIZACIONES:
                a = E * u
                ru = produccion(a, ds, da, peso=peso, **prod_kw)
                p = f"utilizacion={u:.2f}"
                t.add("utilizacion", E, ds, da, "aves_faenadas_dia_operativo", a, "aves", "dia_operativo", "aves",
                      F_PROPIO, parametro=p)
                t.add("utilizacion", E, ds, da, "aves_faenadas_anio", a * da, "aves", "anio", "aves", F_PROPIO,
                      parametro=p)
                t.add("utilizacion", E, ds, da, "t_vivas_anio", a * da * k["peso_vivo"] / 1000, "t", "anio", "vivo",
                      F_BAL, parametro=p)
                t.add("utilizacion", E, ds, da, "pollitos_bb_anio", ru["pollitos_alojados_anio"], "pollitos", "anio",
                      "aves", F_PROD, parametro=p)
                t.add("utilizacion", E, ds, da, "alimento_t_anio", ru["alimento_t_anio"], "t", "anio", "alimento",
                      F_PROD, parametro=p)
                for clave in ("producto_principal", "comestible", "subproductos_c", "pechuga", "pata_muslo",
                              "carcasa_esqueleto", "plumas", "sangre", "visceras", "rendering_potencial"):
                    t.add("utilizacion", E, ds, da, f"{clave}_t_anio", k[clave] * a * da / 1000, "t", "anio",
                          "comercial" if clave in ("producto_principal", "comestible", "pechuga", "pata_muslo",
                                                   "carcasa_esqueleto") else "biologica+agua",
                          F_BAL, parametro=f"{p}; {cfg_txt}")
            # --- 4. balance de productos por escala (§8) ----------------------------------
            for clave, etiqueta, _ in ITEMS:
                if k[clave] <= 0:
                    continue
                for per, f in (("dia_operativo", 1), ("anio", da)):
                    t.add("balance_productos", E, ds, da, f"{clave}_t", k[clave] * aves * f / 1000, "t", per,
                          "comercial" if clave not in ("sangre", "plumas", "visceras", "cabeza", "huesos", "otros_c",
                                                       "residuos", "perdidas") else "biologica+agua",
                          F_BAL, parametro=cfg_txt, sumable="si", nota=etiqueta)
            t.add("balance_productos", E, ds, da, "entrada_pollo_vivo_t", k["peso_vivo"] * aves / 1000, "t",
                  "dia_operativo", "vivo", F_BAL, parametro=cfg_txt, sumable="no", nota="entrada (no es producto)")
            t.add("balance_productos", E, ds, da, "entrada_agua_incorporada_t", k["agua_incorporada"] * aves / 1000,
                  "t", "dia_operativo", "agua", F_BAL, parametro=cfg_txt, sumable="no",
                  nota="agua incorporada a productos y subproductos; NO es consumo de agua de planta")
            # --- 4b. masa biológica vs peso comercial (SUP-042; el agua no es carne) --------
            for clave, base, nota in (("comestible_bio", "biologica", "masa biológica comestible (carne y tejidos)"),
                                      ("agua_retenida_comestible", "agua", "agua retenida en producto: NO es carne"),
                                      ("comestible", "comercial", "peso comercial = biológica + agua retenida"),
                                      ("producto_principal_bio", "biologica", "clase A, masa biológica"),
                                      ("producto_principal", "comercial", "clase A, peso comercial")):
                for per in PERIODOS_POR_ANIO:
                    t.add("masa_comestible", E, ds, da, f"{clave}_t", convertir(k[clave] * aves / 1000,
                          "dia_operativo", per, da), "t", per, base, F_BAL, parametro=cfg_txt, nota=nota)
            # --- 5. configuraciones comerciales (§9) ---------------------------------------
            for c, kc in kcfg.items():
                pc = f"config={c}; peso={peso}"
                for clave, uni, base, nota in (
                        ("producto_principal", "t", "comercial", "clase A"),
                        ("coproductos", "t", "comercial", "clase B (partes secundarias comestibles)"),
                        ("huesos", "t", "biologica+agua", "hueso separado + residuo óseo de CMS"),
                        ("recortes_piel", "t", "comercial", "recortes y piel comestibles"),
                        ("cms", "t", "comercial", "CMS producida (ruta cms)"),
                        ("cms_alternativa_no_sumable", "t", "comercial",
                         "CMS potencial si el esqueleto vendido fuera a CMS; EXCLUYENTE con la carcasa vendida"),
                        ("subproductos_c", "t", "biologica+agua", "clase C"),
                        ("comestible", "t", "comercial", "A + B"),
                        ("kg_trozado", "t", "biologica", "masa que pasa por trozado (proxy de procesamiento)"),
                        ("kg_deshuese", "t", "biologica", "masa que pasa por deshuese (proxy de procesamiento)"),
                        ("kg_cms", "t", "biologica", "materia prima que pasa por separación mecánica")):
                    t.add("configuraciones", E, ds, da, f"{clave}_t", kc[clave] * aves / 1000, uni, "dia_operativo",
                          base, F_BAL, parametro=pc, sumable="no" if clave == "cms_alternativa_no_sumable" else "-",
                          nota=nota)
                t.add("configuraciones", E, ds, da, "flujos_comestibles_distintos", kc["flujos_comestibles"],
                      "índice", "adimensional", "conteo", F_BAL, parametro=pc,
                      nota="componentes comestibles distintos que requieren frío y canal propio")
                t.add("configuraciones", E, ds, da, "coproductos_por_t_de_producto_principal",
                      kc["coproductos"] / kc["producto_principal"], "ratio", "adimensional", "comercial", F_BAL,
                      parametro=pc, nota="necesidad relativa de colocar coproductos")
            # --- 6. subproductos (§10) -------------------------------------------------------
            for clave, nota in (("plumas", "húmedas (con agua de escaldado)"), ("sangre", "recuperada (85 %)"),
                                ("sangre_drenada", "recuperada + no recuperada (NO sumar con la anterior)"),
                                ("visceras", "tracto + pulmones + otros no comestibles"), ("cabeza", ""),
                                ("garras", "grado A + segunda (comestible, B)"), ("carcasa_esqueleto", "B"),
                                ("huesos", "solo con deshuese/CMS"),
                                ("rendering_potencial", "materia prima potencial de rendering = toda la clase C"),
                                ("solidos_a_retirar", "C + decomisos + contenido GI (rendering ampliado, DPV-066)")):
                t.add("subproductos", E, ds, da, f"{clave}_t", k[clave] * aves / 1000, "t", "dia_operativo",
                      "biologica+agua", F_BAL, parametro=cfg_txt,
                      sumable="no" if clave in ("sangre_drenada", "rendering_potencial", "solidos_a_retirar") else "-",
                      nota=nota)
            # --- 7. inventario conceptual (§11) -----------------------------------------------
            prod_com = k["comestible"] * aves / 1000                  # t comerciales por día OPERATIVO
            desp_cal = convertir(prod_com, "dia_operativo", "dia_calendario", da)   # despacho promedio/día cal.
            sub_frio = k["c_perecedero_sin_plumas"] * aves / 1000
            bases_inv = (("dias_produccion", prod_com, "producción por día operativo × días de producción en stock"),
                         ("dias_calendario", desp_cal, "despacho promedio por día calendario × días calendario de cobertura"))
            for base_t, flujo, nota_b in bases_inv:
                for dinv in DIAS_INVENTARIO:
                    pd = f"base_temporal={base_t}; dias={dinv}"
                    t.add("inventario", E, ds, da, "comestible_total_t", flujo * dinv, "t", "stock", "comercial",
                          F_PROPIO, parametro=pd, nota=f"{nota_b}; toda la producción comestible (cota superior)")
                    for pid, (desc, sh) in PERFILES_DESTINO.items():
                        for cat, sh_ in sh.items():
                            t.add("inventario", E, ds, da, f"{cat}_t", flujo * sh_ * dinv, "t", "stock", "comercial",
                                  F_PROPIO, parametro=f"{pd}; perfil_destino={pid}", clasif="[SUPUESTO] ilustrativo",
                                  nota=f"{desc}; exportación de la demanda = 0 (SUP-022)" if cat == "exportacion"
                                  else desc)
            for dinv in DIAS_INVENTARIO:     # los subproductos solo se generan en días de faena
                t.add("inventario", E, ds, da, "subproductos_perecederos_frio_t", sub_frio * dinv, "t", "stock",
                      "biologica+agua", F_PROPIO, parametro=f"base_temporal=dias_produccion; dias={dinv}",
                      nota="clase C sin plumas, si no se retira en el día (sangre, vísceras, cabezas, huesos)")
            # --- 8. logística (§12) ------------------------------------------------------------
            L = (("aves_vivas_cargadas_t_dia", r["aves_cargadas_dia"] * peso / 1000, "vivo",
                  "peso en granja = peso en planta (SUP-058)"),
                 ("aves_vivas_recibidas_faenadas_t_dia", k["peso_vivo"] * aves / 1000, "vivo", ""),
                 ("producto_comestible_sale_t_dia", prod_com, "comercial", "A + B con agua retenida"),
                 ("subproductos_solidos_salen_t_dia", k["solidos_a_retirar"] * aves / 1000, "biologica+agua",
                  "C + decomisos + contenido GI"),
                 ("masa_a_efluente_o_perdida_t_dia", k["efluente_o_perdida"] * aves / 1000, "biologica+agua",
                  "no se transporta; no es el caudal de efluentes de la planta"))
            for var, v, base, nota in L:
                t.add("logistica", E, ds, da, var, v, "t", "dia_operativo", base, F_PROPIO, nota=nota)
            t.add("logistica", E, ds, da, "alimento_a_granjas_t_dia_semana_plena", r["alimento_t_semana_plena"] / 7,
                  "t", "dia_calendario", "alimento", F_PROD, nota="t/semana plena / 7 días de entrega")
            t.add("logistica", E, ds, da, "alimento_a_granjas_t_dia_promedio_anual", r["alimento_t_anio"] / 365,
                  "t", "dia_calendario", "alimento", F_PROD)
            for cap in AVES_POR_CAMION_VIVO:
                t.add("logistica", E, ds, da, "camiones_aves_vivas_dia", r["aves_cargadas_dia"] / cap, "camiones",
                      "dia_operativo", "aves", F_PROPIO, parametro=f"aves_por_camion={cap}",
                      clasif="[SUPUESTO] SUP-033", nota="sin fuente; orden de magnitud")
            t.add("logistica", E, ds, da, "indice_movimientos_vs_2500", E / ESCALAS[0], "índice", "adimensional",
                  "aves", F_PROPIO, nota="frecuencia relativa de movimientos (lineal en toneladas)")
            # --- 9. exportación (§13): días para completar un contenedor --------------------
            kB = kcfg["B"]        # partes de un ave trozada; el entero, de un ave entera (A)
            for var, kg in (("pollo_entero", kcfg["A"]["pollo_entero"]), ("pechuga", kB["pechuga"]),
                            ("pata_muslo", kB["pata_muslo"]), ("alas", kB["alas"]),
                            ("garras_grado_a", kB["garras_grado_a"]), ("menudencias", kB["menudencias"]),
                            ("cuello", kB["cuello"]), ("carcasa_esqueleto", kB["carcasa_esqueleto"])):
                t.add("exportacion", E, ds, da, f"dias_para_contenedor_{var}", CONTENEDOR_T * 1000 / (kg * aves),
                      "días", "dia_operativo", "comercial", F_BAL, clasif="[ESTIMACIÓN] con carga [PVDP · débil]",
                      nota=f"{CONTENEDOR_T:g} t por reefer 40' (FTE-135); 100 % de la parte; NO es demanda")
                t.add("exportacion", E, ds, da, f"contenedores_mes_si_100pct_{var}", kg * aves * da / 12 / 1000 / CONTENEDOR_T,
                      "contenedores/mes", "anio", "comercial", F_BAL, clasif="[ESTIMACIÓN] con carga [PVDP · débil]",
                      nota="capacidad física de generar lotes; exportación = 0 en la demanda (SUP-022)")
            # --- 10. demanda vs capacidad (§4) --------------------------------------------------
            for eid, e in demanda.items():
                D = float(e["total_kg_dia"])
                if D <= 0:
                    continue
                pe = f"escenario={eid}"
                metodos = {"M0_ave_completa": {"aves_dia_cal": D / k["comestible"], "masa_demandada_ave": D,
                                               "comestible_por_ave_mix": k["comestible"], "excedente_total": 0.0,
                                               "limitante": "ninguna (ave completa)", "fuera_balance": 0.0}}
                for m, mix in mixes.items():
                    metodos[f"{m}_parte_limitante"] = aves_por_mix(D, mix, y, f_mila)
                for met, res in metodos.items():
                    cmp_ = comparar_demanda(E, da, D, res)
                    pm_ = f"{pe}; metodo={met}"
                    nota_cat = (f"demanda {e['categoria_demanda_actual']}; sumable_a_demanda="
                                f"{e['sumable_a_demanda']}; no es venta")
                    t.add("demanda_capacidad", E, ds, da, "demanda_kg_producto_dia_calendario", D, "kg",
                          "dia_calendario", "comercial", F_DEM, parametro=pm_, clasif="[SUPUESTO] SUP-021",
                          nota=nota_cat)
                    t.add("demanda_capacidad", E, ds, da, "aves_necesarias_dia_calendario", res["aves_dia_cal"], "aves",
                          "dia_calendario", "aves", F_PROPIO, parametro=pm_, nota=f"limitante: {res['limitante']}")
                    t.add("demanda_capacidad", E, ds, da, "aves_necesarias_dia_operativo",
                          cmp_["aves_necesarias_dia_operativo"], "aves", "dia_operativo", "aves", F_PROPIO,
                          parametro=pm_)
                    for var, nota in (
                            ("factor_demanda_capacidad", "capacidad requerida / instalada; >100 % = la escala no "
                                                         "alcanza; <100 % = capacidad ociosa. NO es utilización"),
                            ("utilizacion_planta", "aves procesadas / capacidad; siempre 0-100 %"),
                            ("cobertura_demanda", "producción posible / demanda requerida; siempre 0-100 %")):
                        t.add("demanda_capacidad", E, ds, da, var, 100 * cmp_[var], "%", "adimensional", "aves",
                              F_PROPIO, parametro=pm_, nota=nota)
                    for var in ("aves_procesadas_dia_operativo", "aves_faltantes_dia_operativo",
                                "capacidad_ociosa_aves_dia_operativo"):
                        t.add("demanda_capacidad", E, ds, da, var, cmp_[var], "aves", "dia_operativo", "aves",
                              F_PROPIO, parametro=pm_)
                    for var in ("kg_atendidos_dia_cal", "kg_no_atendidos_dia_cal",
                                "produccion_comestible_plena_kg_dia_cal", "kg_sin_destino_plena_escala",
                                "demanda_adicional_para_llenar_kg_dia_cal"):
                        t.add("demanda_capacidad", E, ds, da, var, cmp_[var], "kg", "dia_calendario", "comercial",
                              F_PROPIO, parametro=pm_)
                    t.add("demanda_capacidad", E, ds, da, "excedente_partes_kg_dia_cal", res["excedente_total"], "kg",
                          "dia_calendario", "comercial", F_PROPIO, parametro=pm_,
                          nota="partes producidas sin comprador dentro del escenario (aun sin capacidad ociosa)")
                    if res["fuera_balance"]:
                        t.add("demanda_capacidad", E, ds, da, "demanda_fuera_del_balance_kg_dia_cal",
                              res["fuera_balance"], "kg", "dia_calendario", "comercial", F_DEM, parametro=pm_,
                              clasif="[SUPUESTO] SUP-023", nota="otros elaborados: materia prima no modelada")
            t.add("demanda_capacidad", E, ds, da, "utilizacion_con_demanda_documentada_A_mas_B", 0.0, "%",
                  "adimensional", "aves", F_DEM, parametro="demanda A+B ≈ 0 (conclusiones_demanda.md §1)",
                  clasif="[ESTIMACIÓN]", nota="la carnicería familiar es A pero no está cuantificada (DPV-004)")
            # --- 11. tabla central ---------------------------------------------------------------
            prod_E = kg_com_cal = k["comestible"] * E * da / DIAS_CALENDARIO
            for var, v, uni, per, base in (
                    ("aves_anio", E * da, "aves", "anio", "aves"),
                    ("kg_vivo_dia", k["peso_vivo"] * E, "kg", "dia_operativo", "vivo"),
                    ("t_vivas_anio", k["peso_vivo"] * E * da / 1000, "t", "anio", "vivo"),
                    ("pollitos_semana_plena", r["pollitos_alojados_semana_plena"], "pollitos", "semana_plena", "aves"),
                    ("plazas_granja", r["capacidad_alojamiento_pollitos"], "plazas", "stock", "aves"),
                    ("m2_galpones", r["m2_galpon"], "m²", "stock", "superficie"),
                    ("alimento_t_anio", r["alimento_t_anio"], "t", "anio", "alimento"),
                    ("comestible_masa_biologica_t_dia_operativo", k["comestible_bio"] * E / 1000, "t",
                     "dia_operativo", "biologica"),
                    ("agua_retenida_en_producto_t_dia_operativo", k["agua_retenida_comestible"] * E / 1000, "t",
                     "dia_operativo", "agua"),
                    ("producto_comercial_t_dia_operativo", k["comestible"] * E / 1000, "t", "dia_operativo",
                     "comercial"),
                    ("producto_comercial_t_dia_calendario_promedio", convertir(k["comestible"] * E / 1000,
                     "dia_operativo", "dia_calendario", da), "t", "dia_calendario", "comercial"),
                    ("producto_comercial_t_anio", k["comestible"] * E * da / 1000, "t", "anio", "comercial"),
                    ("producto_principal_t_dia", k["producto_principal"] * E / 1000, "t", "dia_operativo", "comercial"),
                    ("plumas_t_dia", k["plumas"] * E / 1000, "t", "dia_operativo", "biologica+agua"),
                    ("sangre_recuperada_t_dia", k["sangre"] * E / 1000, "t", "dia_operativo", "biologica"),
                    ("visceras_t_dia", k["visceras"] * E / 1000, "t", "dia_operativo", "biologica"),
                    ("ritmo_linea_8h_aves_h", E / 8, "aves/h", "hora", "aves"),
                    ("inventario_7_dias_de_produccion_t", k["comestible"] * E / 1000 * 7, "t", "stock", "comercial"),
                    ("inventario_7_dias_calendario_t", convertir(k["comestible"] * E / 1000, "dia_operativo",
                     "dia_calendario", da) * 7, "t", "stock", "comercial"),
                    ("demanda_necesaria_100pct_kg_dia_cal", prod_E, "kg", "dia_calendario", "comercial"),
                    ("demanda_necesaria_85pct_kg_dia_cal", 0.85 * kg_com_cal, "kg", "dia_calendario", "comercial"),
                    ("demanda_necesaria_70pct_kg_dia_cal", 0.70 * kg_com_cal, "kg", "dia_calendario", "comercial"),
                    ("kg_por_local_dia_si_todo_por_la_red_100pct", prod_E / locales, "kg", "dia_calendario",
                     "comercial")):
                t.add("tabla_central", E, ds, da, var, v, uni, per, base,
                      F_PROD if base in ("alimento", "superficie") or var.startswith(("pollitos", "plazas"))
                      else F_BAL if base in ("comercial", "biologica", "biologica+agua", "vivo") else F_PROPIO,
                      parametro=cfg_txt,
                      nota="M0 ave completa: cota inferior; con mix la demanda útil es menor" if "demanda" in var
                      else (f"{locales} locales (escenarios_demanda.csv); comparar con 25-300 kg/local/día"
                            if "local" in var else ""))
    return t


# ---------------------------------------------------------------------------
# 6. TESTS AUTOMÁTICOS
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def ejecutar_tests(verbose=True):
    res = []

    def chk(nombre, cond, det=""):
        res.append((nombre, bool(cond), det))

    # T00: modelos importados intactos
    rp = mp.ejecutar_pruebas()
    rb = mb.ejecutar_tests(verbose=False)
    rs = ms.tests(ms.balances(), ms.filas_csv(ms.balances()), verbose=False)
    chk("T00 modelos importados intactos: producción, balance v1.1 (21) y subproductos (9) pasan",
        all(m == 0 for _, m in rp.values()) and all(r for _, r, _ in rb) and len(rb) == 21
        and all(r for _, r, _ in rs) and len(rs) == 9,
        f"producción {sum(1 for _, m in rp.values() if m == 0)}/{len(rp)}; balance {sum(r for _, r, _ in rb)}/"
        f"{len(rb)}; subproductos {sum(r for _, r, _ in rs)}/{len(rs)}")
    chk("T00b escalas y peso coherentes entre modelos (2.500-20.000; 2,9 kg; 250/300 días)",
        ESCALAS == list(mb.AVES_DIA) == list(ms.AVES_DIA) and PESO_REF == mb.PESO_REF == ms.PESO
        and CALENDARIOS[5] == mb.DIAS_FAENA_ANIO == ms.DIAS)

    t = construir()
    F = t.filas
    num = [f for f in F if _num(f["valor"])]

    # T01 duplicar aves/día duplica las variables físicas lineales
    t2 = construir(escalas=[2 * e for e in ESCALAS])
    malos = 0
    idx2 = {(f["bloque"], f["escala_aves_dia"], f["dias_semana"], f["parametro"], f["variable"], f["periodo"]):
            f["valor"] for f in t2.filas}
    intensivas = {"factor_demanda_capacidad", "utilizacion_planta", "cobertura_demanda",
                  "aves_procesadas_dia_operativo", "capacidad_ociosa_aves_dia_operativo", "kg_atendidos_dia_cal",
                  "kg_no_atendidos_dia_cal", "flujos_comestibles_distintos", "coproductos_por_t_de_producto_principal",
                  "demanda_kg_producto_dia_calendario", "aves_necesarias_dia_calendario",
                  "aves_necesarias_dia_operativo", "excedente_partes_kg_dia_cal", "demanda_fuera_del_balance_kg_dia_cal",
                  "utilizacion_con_demanda_documentada_A_mas_B", "kg_sin_destino_plena_escala",
                  "demanda_adicional_para_llenar_kg_dia_cal", "aves_faltantes_dia_operativo"}
    n_lin = 0
    for f in num:
        if f["variable"] in intensivas:
            continue
        v2 = idx2[(f["bloque"], 2 * f["escala_aves_dia"], f["dias_semana"], f["parametro"], f["variable"],
                   f["periodo"])]
        esperado = f["valor"] / 2 if f["variable"].startswith("dias_para_contenedor") else 2 * f["valor"]
        n_lin += 1
        malos += not _cerca(v2, esperado)
    chk("T01 duplicar aves/día duplica toda variable física lineal (días de contenedor se reducen a la mitad)",
        malos == 0, f"{n_lin} variables, {malos} fallas")

    # T02 más utilización nunca procesa menos (100 % ≥ 85 % ≥ ... ≥ 30 %)
    ok, n = True, 0
    util = [f for f in F if f["bloque"] == "utilizacion"]
    grupos = {}
    for f in util:
        u = float(f["parametro"].split(";")[0].split("=")[1])
        grupos.setdefault((f["escala_aves_dia"], f["dias_semana"], f["variable"]), []).append((u, f["valor"]))
    for serie in grupos.values():
        serie.sort()
        n += 1
        ok &= all(b[1] >= a[1] for a, b in zip(serie, serie[1:]))
        ok &= _cerca(serie[-1][1] * 0.5, dict(serie)[0.5]) or serie[-1][1] == 0
    chk("T02 100 % de utilización nunca procesa menos que 50 % (monótono y proporcional)", ok, f"{n} series")

    # T03 6 días/semana genera mayor volumen anual y semanal que 5
    ok, n = True, 0
    idx6 = {}
    for x in num:
        if x["dias_semana"] == 6:
            idx6.setdefault((x["bloque"], x["escala_aves_dia"], x["parametro"], x["variable"], x["periodo"]),
                            []).append(x["valor"])
    for f in num:
        if f["dias_semana"] == 5 and f["periodo"] in ("anio", "semana_plena", "semana_promedio", "dia_calendario") \
                and f["bloque"] in ("capacidad", "produccion_primaria", "utilizacion", "balance_productos",
                                    "tabla_central") and f["valor"] > 0:
            g = idx6.get((f["bloque"], f["escala_aves_dia"], f["parametro"], f["variable"], f["periodo"]), [])
            n += 1
            ok &= len(g) == 1 and g[0] > f["valor"]
    chk("T03 6 días/semana > 5 días/semana en volúmenes anuales, semanales y por día calendario", ok and n > 100,
        f"{n} variables")

    # T04 pollitos alojados > aves faenadas cuando hay mortalidad
    ok = True
    for E in ESCALAS:
        for ds in CALENDARIOS:
            pol = t.valor(bloque="produccion_primaria", escala_aves_dia=E, dias_semana=ds,
                          variable="pollitos_bb_semana_plena")
            fae = t.valor(bloque="produccion_primaria", escala_aves_dia=E, dias_semana=ds,
                          variable="aves_faenadas_semana_plena")
            car = t.valor(bloque="produccion_primaria", escala_aves_dia=E, dias_semana=ds,
                          variable="aves_cargadas_anio")
            fan = t.valor(bloque="produccion_primaria", escala_aves_dia=E, dias_semana=ds, variable="aves_faenadas_anio")
            ok &= pol > fae and car > fan and pol > fae / (1 - mp.DESEMPENO[DESEMPENO]["mort"])
    r0 = produccion(10000, 5, mort=0.0)
    chk("T04 pollitos alojados > aves cargadas > aves faenadas con mortalidad (y = sin mortalidad en el límite)",
        ok and r0["pollitos_alojados_anio"] > r0["aves_faenadas_anio"] * 0.999)

    # T05 masa de productos deriva del balance v1.1 (recalculada directamente con mb.balance)
    ok = True
    for c, v in CONFIG_VARIANTE.items():
        cfg, rutas, _ = ms.VARIANTES[v]
        b = mb.balance(PESO_REF, cfg, REND, COND, ENF, rutas)
        k, _ = kg_por_ave(c)
        for clave, _, comps in ITEMS:
            ok &= _cerca(k[clave], sum(f["bio"] + f["agua"] for f in b["filas"] if f["componente"] in comps), 1e-12)
    kB, _ = kg_por_ave("B")
    for E in ESCALAS:
        ok &= _cerca(t.valor(bloque="balance_productos", escala_aves_dia=E, dias_semana=5, variable="pechuga_t",
                             periodo="dia_operativo"), kB["pechuga"] * E / 1000)
    # contra el CSV de 07_subproductos (grupo G01 V1 a 10.000 aves/día)
    fsub = ms.filas_csv(ms.balances())
    g01 = next(r["t_dia_10000"] for r in fsub if r["variante"] == "V1" and r["grupo_id"] == "G01")
    ok &= _cerca(g01, t.valor(bloque="configuraciones", escala_aves_dia=10000, dias_semana=5,
                              parametro=f"config=B; peso={PESO_REF}", variable="producto_principal_t"))
    d01 = next(r["t_dia_10000"] for r in fsub if r["variante"] == "V1" and r["grupo_id"] == "D01")
    ok &= _cerca(d01, t.valor(bloque="subproductos", escala_aves_dia=10000, dias_semana=5,
                              variable="rendering_potencial_t"))
    chk("T05 masas de productos y subproductos = balance v1.1 (y = CSV de 07_subproductos)", ok)

    # T06 subproductos no se duplican: partición completa y cierre
    todos = [c for _, _, comps in ITEMS for c in comps]
    ok = len(todos) == len(set(todos)) and set(todos) == set(mb.DESTINO)
    for c in CONFIG_VARIANTE:
        k, b = kg_por_ave(c)
        s = sum(k[i[0]] for i in ITEMS)
        ok &= _cerca(s, b["entrada_bio"] + b["entrada_agua"], 1e-12)
        s8 = sum(k[i] for i in ITEMS_SECCION_8) + k["otros_seccion_8"]
        ok &= _cerca(s8, s, 1e-12)
        ok &= _cerca(k["comestible"] + k["solidos_a_retirar"] + k["efluente_o_perdida"], s, 1e-12)
        clase_item = {}
        for clave, _, comps in ITEMS:
            clases = {mb.DESTINO[x][0] for x in comps}
            clase_item[clave] = clases
            ok &= len(clases) == 1
    for E in ESCALAS:
        for ds in CALENDARIOS:
            s = sum(f["valor"] for f in F if f["bloque"] == "balance_productos" and f["escala_aves_dia"] == E
                    and f["dias_semana"] == ds and f["periodo"] == "dia_operativo" and f["sumable"] == "si")
            ent = sum(f["valor"] for f in F if f["bloque"] == "balance_productos" and f["escala_aves_dia"] == E
                      and f["dias_semana"] == ds and f["sumable"] == "no")
            ok &= _cerca(s, ent)
            ok &= all(f["sumable"] == "no" for f in F if f["variable"] in
                      ("cms_alternativa_no_sumable_t", "rendering_potencial_t", "sangre_drenada_t",
                       "solidos_a_retirar_t"))
    chk("T06 subproductos no se duplican: cada componente en un ítem y una clase; Σ ítems = PV + agua; "
        "rutas alternativas y agregados marcados no sumables", ok)

    # T07 inventario = flujo diario × días, con el flujo de su base temporal
    def _param(f):
        return dict(x.strip().split("=") for x in f["parametro"].split(";") if "=" in x)
    ok, n = True, 0
    for f in F:
        if f["bloque"] != "inventario":
            continue
        pr = _param(f)
        prod = t.valor(bloque="logistica", escala_aves_dia=f["escala_aves_dia"], dias_semana=f["dias_semana"],
                       variable="producto_comestible_sale_t_dia")
        flujo = prod if pr["base_temporal"] == "dias_produccion" else prod * f["dias_anio"] / 365
        if f["variable"] == "comestible_total_t":
            n += 1
            ok &= _cerca(f["valor"], flujo * int(pr["dias"]))
        elif "perfil_destino" in pr:
            ok &= _cerca(f["valor"], flujo * int(pr["dias"]) * PERFILES_DESTINO[pr["perfil_destino"]][1][
                f["variable"][:-2]])
    ok &= all(_cerca(sum(sh.values()), 1.0) for _, sh in PERFILES_DESTINO.values()) and n > 0
    chk("T07 inventario = flujo diario de su base temporal × días (y perfiles de destino suman 100 %)", ok)

    # T08 ninguna variable física negativa ni no finita
    ok = all(math.isfinite(f["valor"]) and f["valor"] >= 0 for f in num)
    chk("T08 ninguna variable física negativa ni no finita", ok, f"{len(num)} valores")

    # T09 unidades consistentes
    ok = all(f["unidad"] in UNIDADES_VALIDAS for f in F)
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            q = lambda **kw: t.valor(escala_aves_dia=E, dias_semana=ds, **kw)
            ok &= _cerca(q(bloque="tabla_central", variable="t_vivas_anio"),
                         q(bloque="tabla_central", variable="kg_vivo_dia") * da / 1000)
            ok &= _cerca(q(bloque="balance_productos", variable="pata_muslo_t", periodo="anio"),
                         q(bloque="balance_productos", variable="pata_muslo_t", periodo="dia_operativo") * da)
            ok &= _cerca(q(bloque="capacidad", variable="aves_faenadas_dia_calendario_equivalente"), E * da / 365)
            ok &= _cerca(q(bloque="ritmo_linea", variable="aves_por_hora_neta", parametro="horas_netas=8"), E / 8)
            ok &= q(bloque="tabla_central", variable="producto_comercial_t_dia_operativo") < \
                q(bloque="tabla_central", variable="kg_vivo_dia") / 1000
    chk("T09 unidades consistentes (t = kg/1.000; t/año = t/día × días; vivo > comercial; unidades válidas)", ok)

    # T10 semana plena y promedio anual no se mezclan
    ok = True
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            q = lambda v: t.valor(bloque="produccion_primaria", escala_aves_dia=E, dias_semana=ds, variable=v)
            ok &= _cerca(q("aves_faenadas_semana_plena"), E * ds)
            ok &= _cerca(q("pollitos_bb_semana_promedio") * SEMANAS_ANIO, q("pollitos_bb_anio"))
            ok &= q("pollitos_bb_semana_plena") > q("pollitos_bb_semana_promedio")
            ok &= q("alimento_t_semana_plena") > q("alimento_t_semana_promedio")
    ok &= all(("semana_plena" in f["variable"]) == (f["periodo"] == "semana_plena") for f in F
              if f["bloque"] == "produccion_primaria")
    ok &= all(("promedio" in f["variable"]) for f in F if f["periodo"] == "semana_promedio")
    rr = produccion(10000, 5, 240)
    ok &= _cerca(rr["pollitos_alojados_semana_plena"], produccion(10000, 5)["pollitos_alojados_semana_plena"])
    ok &= all(_cerca(produccion(10000, ds)[c], mp.calcular(10000, ds, **parametros_produccion())[c])
              for ds in CALENDARIOS for c in CLAVES_ANUALES | CLAVES_NO_ANUALES)
    ok &= (CLAVES_ANUALES | CLAVES_NO_ANUALES) == set(mp.calcular(10000, 5, **parametros_produccion()))
    ok &= not (CLAVES_ANUALES & CLAVES_NO_ANUALES)
    chk("T10 semana plena ≠ promedio anual (etiquetas, relaciones y días/año sin afectar la semana plena)", ok)

    # T11 ninguna cifra económica
    texto = lambda f: re.sub(r"[_/=;]", " ", f"{f['variable']} {f['unidad']} {f['base']} {f['parametro']}")
    ok = not any(PALABRAS_ECONOMICAS.search(texto(f)) for f in F)
    ok &= bool(PALABRAS_ECONOMICAS.search(re.sub(r"[_/=;]", " ", "precio_usd_kg")))   # el filtro funciona
    ok &= all(_num(f["valor"]) or f["valor"] == "" for f in F)
    chk("T11 ninguna cifra económica (sin precios, costos, CAPEX, OPEX, márgenes ni monedas)", ok)

    # T12 capacidad ≠ demanda: cambiar la demanda no cambia la capacidad ni la producción
    dem, _ = leer_demanda()
    t3 = construir(demanda_override={i: 3 * float(e["total_kg_dia"]) for i, e in dem.items()})
    bloques_fisicos = {"capacidad", "ritmo_linea", "produccion_primaria", "utilizacion", "balance_productos",
                       "configuraciones", "subproductos", "inventario", "logistica", "exportacion", "tabla_central",
                       "masa_comestible"}
    a = [(f["variable"], f["valor"]) for f in F if f["bloque"] in bloques_fisicos]
    b = [(f["variable"], f["valor"]) for f in t3.filas if f["bloque"] in bloques_fisicos]
    ok = a == b
    ok &= all(e["sumable_a_demanda"] == "no" and e["categoria_demanda_actual"].startswith("C/D") for e in dem.values())
    ok &= all(float(e["exportacion_kg_dia"]) == 0 for e in dem.values())
    u_dem = [f["valor"] for f in F if f["variable"] == "factor_demanda_capacidad"]
    u3 = [f["valor"] for f in t3.filas if f["variable"] == "factor_demanda_capacidad"]
    ok &= all(_cerca(y3, 3 * y1) for y1, y3 in zip(u_dem, u3)) and len(set(round(x, 6) for x in u_dem)) > 10
    ok &= all(f["valor"] == 0 for f in F if f["variable"] == "utilizacion_con_demanda_documentada_A_mas_B")
    chk("T12 capacidad ≠ demanda: la demanda (C/D, exportación 0) no altera la capacidad; factor = demanda "
        "/ capacidad", ok)

    # T13 mix: lectura, suma 100 %, roles, cierre de masa y parte limitante ≥ ave completa
    mixes, f_mila = leer_mixes()
    y = rendimientos_mix()
    ok = all(_cerca(sum(m.values()), 1.0) for m in mixes.values()) and all(p in ROL_MIX for m in mixes.values()
                                                                           for p in m)
    ok &= 0 < f_mila < 1
    for m in mixes.values():
        r = aves_por_mix(7500, m, y, f_mila)
        ok &= _cerca(r["masa_producida"], r["masa_demandada_ave"] + r["excedente_total"])
        ok &= all(v >= -1e-9 for v in r["excedentes"].values()) and r["otras_partes"] >= 0
        ok &= r["aves_dia_cal"] >= 7500 / kg_por_ave("A")[0]["comestible"]
        for E in ESCALAS:                # plena escala: producido − sin destino = demandado atendido
            c = comparar_demanda(E, 250, 7500, r)
            ok &= _cerca(c["produccion_comestible_plena_kg_dia_cal"] - c["kg_sin_destino_plena_escala"],
                         r["masa_demandada_ave"] * c["cobertura_demanda"])
    chk("T13 mixes M1-M3 leídos de supermercados.md; masa producida = demandada + excedentes; "
        "parte limitante ≥ ave completa", ok, f"factor pechuga/milanesa {f_mila}")

    # T14 ningún escenario de demanda supone 100 % de utilización y hay filas de utilización < 100 %
    ok = any(abs(x - 100) > 1 for x in u_dem) and min(UTILIZACIONES) < 1
    ok &= all(f["parametro"] for f in F if f["bloque"] == "utilizacion")
    chk("T14 la utilización es una variable (30-100 %), no un supuesto de 100 %", ok)

    # T15 errores de entrada detienen el modelo
    errores = 0
    for fn in (lambda: produccion(10000, 7), lambda: produccion(10000, 5, 400), lambda: kg_por_ave("Z"),
               lambda: kg_por_ave("B", 4.5)):
        try:
            fn()
        except (ErrorEscala, mb.ErrorBalance, KeyError):
            errores += 1
    chk("T15 entradas inválidas (días/semana, días/año, configuración, peso fuera de rango) detienen el modelo",
        errores == 4)

    # --- Auditoría conceptual v1.1 --------------------------------------------------------
    dcap = [f for f in F if f["bloque"] == "demanda_capacidad" and f["parametro"].startswith("escenario=")]
    grupos_d = {}
    for f in dcap:
        grupos_d.setdefault((f["escala_aves_dia"], f["dias_semana"], f["parametro"]), {})[f["variable"]] = f["valor"]

    # T16 utilización de planta y cobertura nunca > 100 %; el factor sí puede superarlo
    ok = all(0 <= g["utilizacion_planta"] <= 100 + 1e-9 and 0 <= g["cobertura_demanda"] <= 100 + 1e-9
             for g in grupos_d.values())
    ok &= all(_cerca(g["utilizacion_planta"], min(100.0, g["factor_demanda_capacidad"])) for g in grupos_d.values())
    ok &= any(g["factor_demanda_capacidad"] > 100 for g in grupos_d.values())
    ok &= any(g["factor_demanda_capacidad"] < 100 for g in grupos_d.values())
    ok &= not any(f["unidad"] == "%" and f["valor"] > 100 + 1e-9 for f in num
                  if f["variable"] != "factor_demanda_capacidad")
    chk("T16 utilización de planta y cobertura de demanda ≤ 100 %; solo el factor demanda/capacidad puede superarlo",
        ok, f"{len(grupos_d)} casos; factor máx {max(g['factor_demanda_capacidad'] for g in grupos_d.values()):.0f} %")

    # T17 demanda > capacidad => demanda no atendida; capacidad > demanda => capacidad ociosa
    ok, n_exc, n_oci = True, 0, 0
    for (E, ds, _), g in grupos_d.items():
        D = g["demanda_kg_producto_dia_calendario"]
        ok &= _cerca(g["kg_atendidos_dia_cal"] + g["kg_no_atendidos_dia_cal"], D)
        ok &= _cerca(g["aves_procesadas_dia_operativo"] + g["capacidad_ociosa_aves_dia_operativo"], E)
        if g["factor_demanda_capacidad"] > 100 + 1e-9:
            n_exc += 1
            ok &= g["kg_no_atendidos_dia_cal"] > 0 and g["aves_faltantes_dia_operativo"] > 0 \
                and _cerca(g["utilizacion_planta"], 100) and g["capacidad_ociosa_aves_dia_operativo"] < 1e-9
        elif g["factor_demanda_capacidad"] < 100 - 1e-9:
            n_oci += 1
            ok &= g["capacidad_ociosa_aves_dia_operativo"] > 0 and _cerca(g["cobertura_demanda"], 100) \
                and g["kg_no_atendidos_dia_cal"] < 1e-6
    chk("T17 si demanda > capacidad hay demanda no atendida (utilización 100 %); si capacidad > demanda hay "
        "capacidad ociosa (cobertura 100 %)", ok and n_exc > 0 and n_oci > 0, f"{n_exc} excedidos, {n_oci} con ociosidad")

    # T18 día operativo ≠ día calendario: toda comparación exige conversión explícita
    ok = True
    try:
        cociente((24.0, "dia_operativo"), (7.5, "dia_calendario"))
        ok = False                                  # debió rechazarse
    except ErrorEscala:
        pass
    for (E, ds, prm), g in grupos_d.items():
        da = CALENDARIOS[ds]
        n_cal = g["aves_necesarias_dia_operativo"] * da / 365
        ok &= _cerca(g["factor_demanda_capacidad"], 100 * n_cal / (E * da / 365))
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            q = lambda v: t.valor(bloque="tabla_central", escala_aves_dia=E, dias_semana=ds, variable=v)
            op, cal, an = (q(f"producto_comercial_t_{x}") for x in ("dia_operativo", "dia_calendario_promedio", "anio"))
            ok &= _cerca(cal, op * da / 365) and _cerca(an, op * da) and _cerca(an, cal * 365)
            ok &= not _cerca(cal, op)               # 250 o 300 días ≠ 365
    ok &= all(f["periodo"] == "dia_calendario" for f in F if f["variable"].endswith(("_dia_cal", "_dia_calendario")))
    ok &= all(f["periodo"] == "dia_operativo" for f in F if f["variable"].endswith("_dia_operativo"))
    chk("T18 día operativo vs día calendario: comparar sin convertir se rechaza; conversiones 250/300/365 "
        "coherentes y etiquetas de período correctas", ok)

    # T19 sexto día: +20 % de volumen anual con la misma capacidad diaria
    ok = True
    for E in ESCALAS:
        q = lambda ds, **kw: t.valor(escala_aves_dia=E, dias_semana=ds, **kw)
        ok &= _cerca(q(6, bloque="capacidad", variable="aves_faenadas_anio_plena_escala"),
                     1.2 * q(5, bloque="capacidad", variable="aves_faenadas_anio_plena_escala"))
        ok &= _cerca(q(6, bloque="tabla_central", variable="producto_comercial_t_anio"),
                     1.2 * q(5, bloque="tabla_central", variable="producto_comercial_t_anio"))
        for var, blo, prm in (("escala_aves_faenadas_dia_operativo", "capacidad", ""),
                              ("aves_por_hora_neta", "ritmo_linea", "horas_netas=8"),
                              ("producto_comercial_t_dia_operativo", "tabla_central", f"config=B; peso={PESO_REF}")):
            ok &= _cerca(q(6, bloque=blo, variable=var, parametro=prm), q(5, bloque=blo, variable=var, parametro=prm))
    tA = construir(escalas=[10000], calendarios={6: 250})
    tB = construir(escalas=[10000], calendarios={6: 300})
    for f, g in zip(tA.filas, tB.filas):
        if f["periodo"] in ("dia_operativo", "hora") and f["bloque"] not in ("demanda_capacidad",) and _num(f["valor"]):
            ok &= _cerca(f["valor"], g["valor"])    # la capacidad diaria no depende de los días/año
    chk("T19 300 días/año = +20 % de volumen anual que 250; los días/año no cambian la capacidad diaria", ok)

    # T20 la masa biológica no aumenta por el agua retenida
    ok = True
    for c in CONFIG_VARIANTE:
        k6, _ = kg_por_ave(c, enfriamiento="inmersion")
        k8, _ = kg_por_ave(c, enfriamiento="inmersion_limite")
        ok &= _cerca(k6["comestible_bio"], k8["comestible_bio"]) and k8["comestible"] > k6["comestible"]
        ok &= _cerca(k6["comestible"], k6["comestible_bio"] + k6["agua_retenida_comestible"])
        ok &= k6["agua_retenida_comestible"] > 0 and k6["comestible_bio"] < k6["comestible"]
    for E in ESCALAS:
        q = lambda v: t.valor(bloque="tabla_central", escala_aves_dia=E, dias_semana=5, variable=v)
        ok &= _cerca(q("producto_comercial_t_dia_operativo"),
                     q("comestible_masa_biologica_t_dia_operativo") + q("agua_retenida_en_producto_t_dia_operativo"))
    chk("T20 masa biológica comestible idéntica con 6 % u 8 % de absorción; peso comercial = biológica + agua", ok)

    # T21 todo inventario declara su base temporal (días de producción o días calendario)
    inv = [f for f in F if f["bloque"] == "inventario"]
    ok = all(_param(f).get("base_temporal") in ("dias_produccion", "dias_calendario") for f in inv)
    ok &= all("inventario_7_dias_de_produccion" in v or "inventario_7_dias_calendario" in v
              for v in {f["variable"] for f in F if f["variable"].startswith("inventario_")})
    for E in ESCALAS:
        for ds, da in CALENDARIOS.items():
            vp, vc = (t.valor(bloque="inventario", escala_aves_dia=E, dias_semana=ds, variable="comestible_total_t",
                              parametro=f"base_temporal={b}; dias=7") for b in ("dias_produccion", "dias_calendario"))
            ok &= _cerca(vc, vp * da / 365) and vc < vp
    chk("T21 el inventario identifica su base temporal; 7 días calendario ≠ 7 días de producción", ok,
        f"{len(inv)} filas")

    if verbose:
        print(f"\nTESTS — modelo_escala.py v{VERSION}")
        for nombre, r, d in res:
            print(f"  [{'OK ' if r else 'FALLA'}] {nombre}" + (f"  ({d})" if d else ""))
        print(f"  Resultado: {sum(r for _, r, _ in res)}/{len(res)} correctos\n")
    return res


# ---------------------------------------------------------------------------
# 7. PRUEBA DE MUTACIÓN (los tests deben detectar errores introducidos a propósito)
# ---------------------------------------------------------------------------
MUTACIONES = [
    ("M01 escalado no lineal", "k[clave] * aves * f / 1000", "k[clave] * aves ** 1.01 * f / 1000"),
    ("M02 utilización invertida", "                a = E * u\n", "                a = E / u\n"),
    ("M03 6 días/semana con 250 días/año", "CALENDARIOS = dict(mp.DIAS_FAENA_ANIO)", "CALENDARIOS = {5: 250, 6: 250}"),
    ("M04 pollitos sin mortalidad", '"mort": d["mort"] if mort is None else mort', '"mort": 0.0'),
    ("M05 pechuga no tomada del balance", 'k = {clave: tot(comps) for clave, _, comps in ITEMS}',
     'k = {clave: tot(comps) * (1.05 if clave == "pechuga" else 1) for clave, _, comps in ITEMS}'),
    ("M06 subproducto duplicado (vísceras en dos ítems)", '("cabeza", "Cabezas", {"cabeza"}),',
     '("cabeza", "Cabezas", {"cabeza", "pulmones"}),'),
    ("M07 inventario = producción × (días + 1)", "flujo * dinv, \"t\"", "flujo * (dinv + 1), \"t\""),
    ("M08 demanda no atendida negativa", '"kg_no_atendidos_dia_cal": D * (1 - cobertura),',
     '"kg_no_atendidos_dia_cal": D * (0.5 - cobertura),'),
    ("M09 unidades: t = kg / 100", '("kg_vivo_dia", k["peso_vivo"] * E, "kg"', '("kg_vivo_dia", k["peso_vivo"] * E * 10, "kg"'),
    ("M10 semana plena mezclada con promedio", '("pollitos_alojados_semana_plena", "pollitos_bb_semana_plena"',
     '("pollitos_alojados_semana_promedio", "pollitos_bb_semana_plena"'),
    ("M11 cifra económica introducida", '("aves_anio", E * da, "aves", "anio", "aves"),',
     '("aves_anio", E * da, "aves", "anio", "aves"), ("precio_usd_kg", 2.5, "kg", "anio", "comercial"),'),
    ("M12 capacidad igualada a la demanda", '"factor_demanda_capacidad": factor,', '"factor_demanda_capacidad": 1.0,'),
    ("M13 CMS alternativa sumada como producto", 'sumable="no" if clave == "cms_alternativa_no_sumable" else "-"',
     'sumable="-"'),
    ("M15 utilización sin tope de 100 %", "utiliz = min(1.0, factor)", "utiliz = factor"),
    ("M16 cobertura sin tope de 100 %", "cobertura = min(1.0, 1 / factor) if factor else 1.0",
     "cobertura = 1 / factor if factor else 1.0"),
    ("M17 demanda calendario comparada con capacidad por día de faena sin convertir",
     'cap_cal = convertir(E, "dia_operativo", "dia_calendario", dias_anio)', "cap_cal = E"),
    ("M18 comparación directa de períodos distintos",
     'factor = cociente((n, "dia_calendario"), (cap_cal, "dia_calendario"))',
     'factor = cociente((n, "dia_calendario"), (E, "dia_operativo"))'),
    ("M19 inventario calendario sin conversión",
     'desp_cal = convertir(prod_com, "dia_operativo", "dia_calendario", da)', "desp_cal = prod_com"),
    ("M20 inventario sin base temporal declarada", 'pd = f"base_temporal={base_t}; dias={dinv}"',
     'pd = f"base_temporal=dias_produccion; dias={dinv}"'),
    ("M21 el sexto día aumenta la capacidad diaria", '"aves_por_hora_neta", E / h,', '"aves_por_hora_neta", E * da / 250 / h,'),
    ("M22 agua retenida contada como masa biológica",
     '"comestible_bio": sum(f["bio"] for f in b["filas"] if f["clase"] in "AB"),',
     '"comestible_bio": sum(f["bio"] + f["agua"] for f in b["filas"] if f["clase"] in "AB"),'),
    ("M14 días/año alteran la semana plena", "    for clave in CLAVES_ANUALES:\n        r[clave] *= k\n",
     "    for clave in CLAVES_ANUALES | {'pollitos_alojados_semana_plena'}:\n        r[clave] *= k\n"),
]


def prueba_mutaciones():
    with open(os.path.abspath(__file__), encoding="utf-8") as fh:
        fuente = fh.read()
    corte = fuente.index("MUTACIONES = [")          # solo se muta el código anterior a esta lista
    codigo, resto = fuente[:corte], fuente[corte:]
    detectadas = 0
    tmp = tempfile.mkdtemp()
    try:
        for nombre, viejo, nuevo in MUTACIONES:
            if codigo.count(viejo) != 1:
                print(f"  [ERROR] {nombre}: el texto a mutar aparece {codigo.count(viejo)} veces")
                continue
            ruta = os.path.join(tmp, "modelo_escala_mutado.py")
            with open(ruta, "w", encoding="utf-8") as fh:
                fh.write(codigo.replace(viejo, nuevo) + resto)
            env = dict(os.environ, MODELO_ESCALA_RAIZ=RAIZ)
            p = subprocess.run([sys.executable, ruta, "--solo-tests"], capture_output=True, text=True, env=env)
            fallas = re.findall(r"\[FALLA\] (T\d+b?)", p.stdout)
            ok = p.returncode != 0
            detectadas += ok
            print(f"  [{'DETECTADA' if ok else 'NO DETECTADA'}] {nombre}"
                  + (f" -> tests que fallan: {', '.join(fallas)}" if fallas else
                     (" -> " + next(ln.strip() for ln in p.stdout.splitlines() if "DETENIDO" in ln)[:110]
                      if "DETENIDO" in p.stdout else
                      (f" -> {p.stderr.strip().splitlines()[-1][:90]}" if p.stderr.strip() else ""))))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print(f"  Mutaciones detectadas: {detectadas}/{len(MUTACIONES)}")
    return detectadas == len(MUTACIONES)


# ---------------------------------------------------------------------------
# 8. SALIDAS
# ---------------------------------------------------------------------------
def escribir_csv(t, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS, lineterminator="\n")
        w.writeheader()
        for f in t.filas:
            v = f["valor"]
            w.writerow(dict(f, valor=(f"{v:.6f}".rstrip("0").rstrip(".") if isinstance(v, float) else v)))
    return len(t.filas)


def fmt(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_tablas(t):
    q = t.valor
    print("\n## Tabla central (5 d/sem · 250 d | 6 d/sem · 300 d), config B, 2,9 kg")
    for var in ("aves_anio", "kg_vivo_dia", "t_vivas_anio", "pollitos_semana_plena", "plazas_granja", "m2_galpones",
                "alimento_t_anio", "comestible_masa_biologica_t_dia_operativo",
                "agua_retenida_en_producto_t_dia_operativo", "producto_comercial_t_dia_operativo",
                "producto_comercial_t_dia_calendario_promedio", "producto_comercial_t_anio",
                "producto_principal_t_dia", "plumas_t_dia",
                "sangre_recuperada_t_dia", "visceras_t_dia", "ritmo_linea_8h_aves_h",
                "inventario_7_dias_de_produccion_t", "inventario_7_dias_calendario_t",
                "demanda_necesaria_100pct_kg_dia_cal",
                "demanda_necesaria_70pct_kg_dia_cal", "kg_por_local_dia_si_todo_por_la_red_100pct"):
        cel = []
        for E in ESCALAS:
            a, b = (q(bloque="tabla_central", escala_aves_dia=E, dias_semana=ds, variable=var) for ds in (5, 6))
            d = 1 if a < 100 else 0
            cel.append(fmt(a, d) if _cerca(a, b) else f"{fmt(a, d)} / {fmt(b, d)}")
        print(f"| {var} | " + " | ".join(cel) + " |")

    print("\n## Ritmo de línea (aves/h) por horas netas")
    for E in ESCALAS:
        print(f"| {fmt(E)} | " + " | ".join(fmt(q(bloque='ritmo_linea', escala_aves_dia=E, dias_semana=5,
                                                     variable='aves_por_hora_neta', parametro=f'horas_netas={h}'))
                                             for h in HORAS_NETAS) + " |")

    print("\n## Producción primaria (medio), 5 d | 6 d")
    for var in [v[1] for v in VARS_PRODUCCION] + ["alimento_a_granjas_t_dia_semana_plena"]:
        cel = []
        for E in ESCALAS:
            vals = []
            for ds in (5, 6):
                blo = "logistica" if var.startswith("alimento_a_granjas") else "produccion_primaria"
                vals.append(q(bloque=blo, escala_aves_dia=E, dias_semana=ds, variable=var))
            d = 1 if vals[0] < 100 else 0
            cel.append(" / ".join(fmt(v, d) for v in vals))
        print(f"| {var} | " + " | ".join(cel) + " |")

    print("\n## Utilización (5 d/250 d): aves/día | aves/año | t vivas/año | producto principal t/año | "
          "comestible t/año | subproductos C t/año | pollitos/año | alimento t/año")
    for E in ESCALAS:
        for u in UTILIZACIONES:
            p = f"utilizacion={u:.2f}"
            pc = f"{p}; config={CONFIG_REF}; peso={PESO_REF}"
            v = [q(bloque="utilizacion", escala_aves_dia=E, dias_semana=5, variable=x, parametro=p)
                 for x in ("aves_faenadas_dia_operativo", "aves_faenadas_anio", "t_vivas_anio", "pollitos_bb_anio",
                           "alimento_t_anio")]
            w = [q(bloque="utilizacion", escala_aves_dia=E, dias_semana=5, variable=x, parametro=pc)
                 for x in ("producto_principal_t_anio", "comestible_t_anio", "subproductos_c_t_anio")]
            print(f"| {fmt(E)} | {u:.0%} | {fmt(v[0])} | {fmt(v[1])} | {fmt(v[2])} | {fmt(w[0])} | {fmt(w[1])} | "
                  f"{fmt(w[2])} | {fmt(v[3])} | {fmt(v[4])} |")

    print("\n## Balance de productos por escala (t/día operativo | t/año 250 d), config B")
    k, _ = kg_por_ave()
    for clave in ITEMS_SECCION_8 + ("otros_seccion_8",):
        cel = [f"{fmt(k[clave] * E / 1000, 2)} / {fmt(k[clave] * E * 250 / 1000)}" for E in ESCALAS]
        print(f"| {clave} | {fmt(k[clave], 3)} | " + " | ".join(cel) + " |")

    print("\n## Configuraciones A/B/C a 10.000 aves/día (t/día) y kg/ave")
    for var in ("producto_principal_t", "coproductos_t", "huesos_t", "recortes_piel_t", "cms_t",
                "cms_alternativa_no_sumable_t", "subproductos_c_t", "comestible_t", "kg_trozado_t", "kg_deshuese_t",
                "kg_cms_t", "flujos_comestibles_distintos", "coproductos_por_t_de_producto_principal"):
        cel = [fmt(q(bloque="configuraciones", escala_aves_dia=10000, dias_semana=5, variable=var,
                     parametro=f"config={c}; peso={PESO_REF}"), 2) for c in "ABC"]
        print(f"| {var} | " + " | ".join(cel) + " |")

    print("\n## Subproductos por escala (t/día operativo)")
    for var in ("plumas_t", "sangre_t", "sangre_drenada_t", "visceras_t", "cabeza_t", "garras_t", "carcasa_esqueleto_t",
                "rendering_potencial_t", "solidos_a_retirar_t"):
        cel = [fmt(q(bloque="subproductos", escala_aves_dia=E, dias_semana=5, variable=var), 2) for E in ESCALAS]
        print(f"| {var} | " + " | ".join(cel) + " |")
    kc, _ = kg_por_ave("C")
    print("| huesos (config C) | " + " | ".join(fmt(kc["huesos"] * E / 1000, 2) for E in ESCALAS) + " |")
    print("| rendering potencial (config C) | " + " | ".join(fmt(kc["rendering_potencial"] * E / 1000, 2)
                                                          for E in ESCALAS) + " |")

    print("\n## Inventario comestible (t): días de producción | días calendario, por días; y subproductos")
    for ds in (5, 6):
        for E in ESCALAS:
            celp = [fmt(q(bloque="inventario", escala_aves_dia=E, dias_semana=ds, variable="comestible_total_t",
                          parametro=f"base_temporal=dias_produccion; dias={d}"), 1) for d in DIAS_INVENTARIO]
            celc = [fmt(q(bloque="inventario", escala_aves_dia=E, dias_semana=ds, variable="comestible_total_t",
                          parametro=f"base_temporal=dias_calendario; dias={d}"), 1) for d in DIAS_INVENTARIO]
            sub = [fmt(q(bloque="inventario", escala_aves_dia=E, dias_semana=ds,
                         variable="subproductos_perecederos_frio_t",
                         parametro=f"base_temporal=dias_produccion; dias={d}"), 1) for d in DIAS_INVENTARIO]
            print(f"| {ds} d | {fmt(E)} | " + " | ".join(celp) + " | " + " | ".join(celc) + " | " + " | ".join(sub) + " |")
    for base_t in ("dias_produccion", "dias_calendario"):
        for pid in PERFILES_DESTINO:
            cel = []
            for E in ESCALAS:
                cel.append(" / ".join(fmt(q(bloque="inventario", escala_aves_dia=E, dias_semana=5, variable=f"{cat}_t",
                                            parametro=f"base_temporal={base_t}; dias={d}; perfil_destino={pid}"), 1)
                                      for cat, d in (("refrigerado", 3), ("congelado", 14), ("exportacion", 14))))
            print(f"| {base_t} | {pid} | " + " | ".join(cel) + " |")

    print("\n## Masa comestible (t): biológica | agua retenida | comercial — día operativo, día calendario, año (5 d)")
    for E in ESCALAS:
        cel = []
        for per in PERIODOS_POR_ANIO:
            cel.append(" / ".join(fmt(q(bloque="masa_comestible", escala_aves_dia=E, dias_semana=5, periodo=per,
                                        variable=f"{c}_t"), 2 if per != "anio" else 0)
                                  for c in ("comestible_bio", "agua_retenida_comestible", "comestible")))
        print(f"| {fmt(E)} | " + " | ".join(cel) + " |")

    print("\n## Logística (t/día operativo; 5 d)")
    for var in ("aves_vivas_cargadas_t_dia", "aves_vivas_recibidas_faenadas_t_dia", "producto_comestible_sale_t_dia",
                "subproductos_solidos_salen_t_dia", "masa_a_efluente_o_perdida_t_dia",
                "alimento_a_granjas_t_dia_semana_plena", "alimento_a_granjas_t_dia_promedio_anual"):
        cel = [fmt(q(bloque="logistica", escala_aves_dia=E, dias_semana=5, variable=var), 1) for E in ESCALAS]
        print(f"| {var} | " + " | ".join(cel) + " |")
    for cap in AVES_POR_CAMION_VIVO:
        cel = [fmt(q(bloque="logistica", escala_aves_dia=E, dias_semana=5, variable="camiones_aves_vivas_dia",
                     parametro=f"aves_por_camion={cap}"), 1) for E in ESCALAS]
        print(f"| camiones vivos ({cap} aves) | " + " | ".join(cel) + " |")

    print("\n## Exportación: días de faena para 25 t | contenedores/mes si 100 % (5 d)")
    for var in ("pollo_entero", "pechuga", "pata_muslo", "alas", "garras_grado_a", "menudencias", "cuello",
                "carcasa_esqueleto"):
        cel = [f"{fmt(q(bloque='exportacion', escala_aves_dia=E, dias_semana=5, variable=f'dias_para_contenedor_{var}'), 1)}"
               f" / {fmt(q(bloque='exportacion', escala_aves_dia=E, dias_semana=5, variable=f'contenedores_mes_si_100pct_{var}'), 1)}"
               for E in ESCALAS]
        print(f"| {var} | " + " | ".join(cel) + " |")

    dem, _ = leer_demanda()
    print("\n## Demanda vs capacidad (5 d/250): factor % | utilización % | cobertura % por escenario y método")
    for eid in dem:
        for met in ("M0_ave_completa", "M1_parte_limitante", "M2_parte_limitante", "M3_parte_limitante"):
            p = f"escenario={eid}; metodo={met}"
            aves = q(bloque="demanda_capacidad", escala_aves_dia=2500, dias_semana=5, parametro=p,
                     variable="aves_necesarias_dia_operativo")
            cel = []
            for E in ESCALAS:
                v = [q(bloque="demanda_capacidad", escala_aves_dia=E, dias_semana=5, parametro=p, variable=x)
                     for x in ("factor_demanda_capacidad", "utilizacion_planta", "cobertura_demanda")]
                cel.append(" / ".join(fmt(x) for x in v))
            print(f"| {eid} | {met} | {fmt(aves)} | " + " | ".join(cel) + " |")
    print("\n## Ídem 6 d/300: factor %")
    for eid in dem:
        for met in ("M0_ave_completa", "M1_parte_limitante", "M3_parte_limitante"):
            p = f"escenario={eid}; metodo={met}"
            print(f"| {eid} | {met} | " + " | ".join(fmt(q(bloque="demanda_capacidad", escala_aves_dia=E, dias_semana=6,
                  parametro=p, variable="factor_demanda_capacidad")) for E in ESCALAS) + " |")

    print("\n## kg/día cal atendidos | no atendidos | capacidad ociosa (aves/día op.) | kg/día cal sin destino a "
          "plena escala | demanda adicional para llenar (5 d)")
    for eid in dem:
        for met in ("M0_ave_completa", "M2_parte_limitante"):
            p = f"escenario={eid}; metodo={met}"
            cel = []
            for E in ESCALAS:
                v = [q(bloque="demanda_capacidad", escala_aves_dia=E, dias_semana=5, parametro=p, variable=x)
                     for x in ("kg_atendidos_dia_cal", "kg_no_atendidos_dia_cal", "capacidad_ociosa_aves_dia_operativo",
                               "kg_sin_destino_plena_escala", "demanda_adicional_para_llenar_kg_dia_cal")]
                cel.append(" / ".join(fmt(x) for x in v))
            print(f"| {eid} | {met} | " + " | ".join(cel) + " |")
    y = rendimientos_mix()
    print("\nRendimientos del mix (kg/ave):", {kk: round(v, 4) for kk, v in y.items()})
    mixes, fm = leer_mixes()
    for m, mix in mixes.items():
        r = aves_por_mix(7500, mix, y, fm)
        print(m, "aves/día cal", round(r["aves_dia_cal"]), "limitante", r["limitante"], "exc", round(r["excedente_total"]),
              {kk: round(v) for kk, v in r["excedentes"].items()}, "otras", round(r["otras_partes"]),
              "fuera", round(r["fuera_balance"]))
    kb, _ = kg_por_ave("B")
    print("kg comestible/ave A/B/C:", [round(kg_por_ave(c)[0]["comestible"], 4) for c in "ABC"],
          "producto principal B", round(kb["producto_principal"], 4))


def resumen_escenario(a):
    """Sensibilidad: imprime un escenario con los parámetros de la línea de comandos (sin CSV)."""
    E, ds = a.aves_dia, a.dias_semana
    da = a.dias_anio or CALENDARIOS[ds]
    u = a.utilizacion
    faen = E * u
    r = produccion(faen, ds, da, peso=a.peso, fcr=a.fcr, mort=a.mortalidad, edad=a.edad)
    k, _ = kg_por_ave(a.config, a.peso)
    print(f"\nESCENARIO — escala {fmt(E)} aves/día · utilización {u:.0%} -> {fmt(faen)} aves faenadas/día operativo · "
          f"{ds} d/sem · {da} d/año · {a.peso} kg · config {a.config}")
    filas = [("Aves faenadas/año", faen * da, 0), ("Ritmo de línea (aves/h netas)", E / a.horas_netas, 0),
             ("t vivas/día operativo", faen * a.peso / 1000, 1), ("t vivas/año", faen * a.peso * da / 1000, 0),
             ("Pollitos BB/semana plena", r["pollitos_alojados_semana_plena"], 0),
             ("Plazas de granja", r["capacidad_alojamiento_pollitos"], 0), ("m² de galpón", r["m2_galpon"], 0),
             ("Alimento t/año", r["alimento_t_anio"], 0), ("Agua de bebida m³/año", r["agua_bebida_m3_anio"], 0),
             ("Producto comercial t/día operativo", k["comestible"] * faen / 1000, 2),
             ("Producto principal t/día", k["producto_principal"] * faen / 1000, 2),
             ("Plumas húmedas t/día", k["plumas"] * faen / 1000, 2), ("Sangre recuperada t/día", k["sangre"] * faen / 1000, 2),
             ("Rendering potencial t/día", k["rendering_potencial"] * faen / 1000, 2),
             ("Comestible masa biológica t/día operativo", k["comestible_bio"] * faen / 1000, 2),
             ("Agua retenida en producto t/día operativo", k["agua_retenida_comestible"] * faen / 1000, 2),
             ("Producto comercial t/día calendario (promedio)",
              convertir(k["comestible"] * faen / 1000, "dia_operativo", "dia_calendario", da), 2),
             (f"Inventario {a.dias_inventario:g} días de producción (t)",
              k["comestible"] * faen / 1000 * a.dias_inventario, 1),
             (f"Inventario {a.dias_inventario:g} días calendario de cobertura (t)",
              convertir(k["comestible"] * faen / 1000, "dia_operativo", "dia_calendario", da) * a.dias_inventario, 1)]
    for n, v, d in filas:
        print(f"  {n:45s} {fmt(v, d):>14s}")
    if a.demanda:
        dem, _ = leer_demanda()
        D = float(dem[a.demanda]["total_kg_dia"])
        cmp_ = comparar_demanda(E, da, D, {"aves_dia_cal": D / k["comestible"], "excedente_total": 0.0,
                                           "comestible_por_ave_mix": k["comestible"]})
        print(f"  Demanda {a.demanda} ({fmt(D)} kg/día cal, categoría C/D), método M0: factor demanda/capacidad "
              f"{cmp_['factor_demanda_capacidad']:.0%}; utilización {cmp_['utilizacion_planta']:.0%}; cobertura "
              f"{cmp_['cobertura_demanda']:.0%}; no atendidos {fmt(cmp_['kg_no_atendidos_dia_cal'])} kg/día cal; "
              f"capacidad ociosa {fmt(cmp_['capacidad_ociosa_aves_dia_operativo'])} aves/día operativo")
        if cmp_["utilizacion_planta"] < u:
            print("  ALERTA: la utilización supuesta supera la que la demanda del escenario justifica.")
        if cmp_["factor_demanda_capacidad"] > 1:
            print("  ALERTA: la demanda del escenario excede la escala.")


def main():
    ap = argparse.ArgumentParser(description="Modelo preliminar de escala (Fase 0; escenarios físicos)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--tablas", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--escenario", action="store_true", help="imprime un escenario de sensibilidad")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--dias-semana", type=int, default=5, choices=sorted(CALENDARIOS))
    ap.add_argument("--dias-anio", type=float, default=None)
    ap.add_argument("--horas-netas", type=float, default=8)
    ap.add_argument("--peso", type=float, default=PESO_REF)
    ap.add_argument("--edad", type=float, default=None)
    ap.add_argument("--mortalidad", type=float, default=None)
    ap.add_argument("--fcr", type=float, default=None)
    ap.add_argument("--config", choices=sorted(CONFIG_VARIANTE), default=CONFIG_REF)
    ap.add_argument("--utilizacion", type=float, default=0.70)
    ap.add_argument("--dias-inventario", type=float, default=7)
    ap.add_argument("--demanda", default=None, help="ESC-CON / ESC-BAS / ESC-EXP")
    a = ap.parse_args()
    try:
        res = ejecutar_tests()
        if not all(r for _, r, _ in res):
            print("DETENIDO: al menos una prueba falló. No se generan salidas.")
            sys.exit(1)
        if a.solo_tests:
            return
        if a.mutaciones:
            sys.exit(0 if prueba_mutaciones() else 1)
        if a.escenario:
            resumen_escenario(a)
            return
        t = construir()
        n = escribir_csv(t, os.path.join(AQUI, "escenarios_escala.csv"))
        print(f"CSV generado: 23_plan_expansion/escenarios_escala.csv ({n} filas)")
        if a.tablas:
            imprimir_tablas(t)
    except (ErrorEscala, mb.ErrorBalance) as e:
        print(f"DETENIDO: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
