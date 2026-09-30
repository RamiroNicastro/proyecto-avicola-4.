#!/usr/bin/env python3
"""
Modelo de BALANCE DE MASA del pollo parrillero — versión 1.1 (2026-09-30)
==========================================================================

Pregunta: si entran X kg de pollo vivo, ¿dónde termina cada kilogramo?

ALCANCE: este es un BALANCE DE MASA DEL AVE Y SUS PRODUCTOS. NO es todavía un
balance de agua industrial, ni de efluentes, ni energético, ni un modelo
económico, ni un diseño de maquinaria: esos módulos usarán después estos
resultados. ESTE BALANCE NO DIMENSIONA EL CONSUMO INDUSTRIAL DE AGUA NI EL
CAUDAL TOTAL DE EFLUENTES DE LA PLANTA.

Fase 0 (prefactibilidad). ESCENARIOS, no diseño. Sin precios, sin maquinaria,
sin capacidad fijada (reglas 7-9 de CLAUDE.md).

Uso
---
    python3 modelo_balance_masa.py                  # tests + CSV + resumen
    python3 modelo_balance_masa.py --solo-tests     # solo pruebas automáticas
    python3 modelo_balance_masa.py --peso 3.1 --config C --rendimiento alto \
        --condenas bajo --enfriamiento aire --ruta-esqueleto venta --aves-dia 8000
    python3 modelo_balance_masa.py --peso 2.9 --auditoria   # tablas de auditoría manual

El script se DETIENE (código de salida 1) si alguna prueba falla o si algún
balance no cierra dentro de la tolerancia (TOL_KG_POR_AVE).

Unidad base y límites del sistema
---------------------------------
* Unidad: 1 POLLO VIVO recibido en planta (después de ayuno y transporte).
  La merma de peso en ayuno/transporte y las aves muertas en transporte (DOA)
  quedan FUERA del balance (ver 03_produccion_primaria; SUP-035).
* Toda masa se expresa en kg. Porcentajes en fracción (0-1) dentro del código.
* Dos flujos que nunca se mezclan:
    - MASA BIOLÓGICA (tejidos del ave): entra solo con el peso vivo.
    - AGUA INCORPORADA A PRODUCTOS Y SUBPRODUCTOS: solo el agua que queda
      físicamente adherida o absorbida en las masas que salen del proceso:
        (a) agua absorbida por la carcasa en el chiller por inmersión, que se
            reparte en AGUA RETENIDA EN PRODUCTO (se vende) y AGUA DE GOTEO
            DEL PRODUCTO (purga antes de la venta);
        (b) agua adherida a las plumas (sale con la pluma húmeda).
      NO es el agua de proceso total utilizada por la planta (lavado,
      escaldado, llenado y renovación del chiller, limpieza, sanitización,
      otros usos), que se calculará en 11_agua_efluentes.
  Peso comercial = masa biológica + agua retenida en producto.  El agua NO es carne.

Ecuación de balance (se verifica para cada escenario)
------------------------------------------------------
    PV + AGUA_INCORPORADA_A_PRODUCTOS_Y_SUBPRODUCTOS
        = PRODUCTOS(A) + COPRODUCTOS(B) + SUBPRODUCTOS(C) + RESIDUOS/EFLUENTES(D) + PÉRDIDAS(P)
    con, por separado:  Σ masa biológica = PV   y   Σ agua = agua incorporada

Clases de salida (cada fila pertenece a UNA sola clase final)
--------------------------------------------------------------
    A  producto principal       (ave entera, pechuga, pata-muslo y derivados)
    B  coproducto comestible    (alas, menudencias, cuello, garras, carcasa-
                                 esqueleto, piel, recortes, CMS)
    C  subproducto valorizable  (sangre recuperada, plumas, cabezas, vísceras no
                                 comestibles, huesos, residuo óseo de CMS, grasa
                                 retirada, garras de descarte, piel a rendering)
    D  residuo / efluente       (contenido gastrointestinal, sangre no
                                 recuperada, merma de acondicionamiento de patas,
                                 agua de goteo del producto, decomisos*)
    P  merma real / pérdida     (evaporación, mermas de trozado/deshuese/CMS,
                                 pérdidas no asignadas)
    * Los decomisos se tratan como D; si la normativa permite enviarlos a
      rendering pasarían a C (DPV-066). NUNCA forman parte de P.

Rutas alternativas (exclusivas): un material se vende O se reprocesa, nunca ambas
---------------------------------------------------------------------------------
    esqueleto      : "venta" (carcasa-esqueleto, B)  | "cms" (CMS B + residuo óseo C)
    cuello         : "venta" (cuello, B)             | "cms"
    hueso_pechuga  : "rendering" (hueso, C)          | "cms"      (solo config. C)
    piel           : "venta" (piel, B)               | "rendering" (piel a rendering, C) (solo C)

Método de dependencia con el peso vivo (no lineal)
--------------------------------------------------
    fracción_i(PV) = fracción_i(2,9 kg) + pendiente_i × (PV − 2,9)   [en % del PV]
    kg_i = PV × fracción_i(PV)   -> cuadrático en PV. Válido solo entre 2,0 y 3,8 kg.
    Dirección de las pendientes: literatura de alometría [PVDP]; magnitud:
    [SUPUESTO] calibrado para que las pérdidas no asignadas no varíen con el
    peso (no hay evidencia de que lo hagan). SUP-036.

Todas las cifras son [ESTIMACIÓN]/[SUPUESTO] construidas con rangos de fuentes
[PVDP] (FTE-140, FTE-142, FTE-161 a FTE-184). Detalle y fuentes por parámetro:
balance_por_ave.md, rendimientos_cortes.md, subproductos_masa.md,
agua_y_mermas.md, auditoria_balance.md. Supuestos: SUP-035 a SUP-045.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import os
import sys
from collections import defaultdict

VERSION = "1.1"
FECHA = "2026-09-30"

# ---------------------------------------------------------------------------
# 1. CONSTANTES GENERALES
# ---------------------------------------------------------------------------
PESO_REF = 2.9                                  # kg vivo de referencia (perfil medio, SUP-027)
PESOS = [2.2, 2.5, 2.8, 3.0, 3.2, 3.5]          # pesos vivos modelados (pedido del promotor)
RANGO_VALIDO = (2.0, 3.8)                       # fuera de este rango no se extrapola
DIAS_FAENA_ANIO = 250                           # 5 días/semana (SUP-025)
AVES_DIA = [2500, 5000, 10000, 20000]           # escenarios de escala (no capacidad)
AVES_ANIO_REF = 1_000_000                       # escenario anual adicional
TOL_KG_POR_AVE = 1e-6                           # tolerancia máxima de cierre: 1 mg por ave
CONFIGS = ["A", "B", "C"]
NOMBRE_CONFIG = {"A": "pollo entero", "B": "trozado", "C": "deshuesado / mayor valor"}

# ---------------------------------------------------------------------------
# 2. FAENA PRIMARIA — composición del ave viva (% del PV a 2,9 kg, escenario medio)
#    (clave, % a 2,9 kg, pendiente en puntos porcentuales por kg de PV)
# ---------------------------------------------------------------------------
PRIMARIOS = [
    # carcasa = canal eviscerada caliente SIN cabeza, patas, cuello ni menudencias,
    # con piel, con grasa abdominal y riñones (definición D5 de balance_por_ave.md)
    ("carcasa",               71.5, +1.90),
    ("sangre",                 3.4, -0.10),   # sangre total drenada en el desangrado
    ("plumas",                 5.2, -0.20),   # masa biológica de plumas (sin agua de escaldado)
    ("cabeza",                 2.5, -0.30),
    ("patas",                  3.9, -0.30),   # pata anatómica cortada en la articulación del tarso
    ("higado",                 1.9, -0.15),
    ("corazon",                0.5, -0.05),
    ("molleja",                1.4, -0.20),   # molleja limpia (sin cutícula ni contenido)
    ("cuello",                 2.6, -0.10),
    ("tracto_digestivo",       3.0, -0.25),   # intestinos, proventrículo, ciegos, cloaca (vacíos)
    ("contenido_gi",           1.2, -0.10),   # contenido gastrointestinal residual tras el ayuno
    ("pulmones",               0.6, -0.05),
    ("otros_no_comestibles",   0.9, -0.10),   # tráquea, esófago y buche, bazo, vesícula, gónadas,
                                              # cutícula y contenido de molleja
]
# Grasa abdominal: sub-componente DENTRO de la carcasa (no se suma aparte)
GRASA_ABDOMINAL = (1.8, +0.30)                # % PV a 2,9 kg; pendiente pp/kg

# Ajustes por escenario de RENDIMIENTO (puntos porcentuales del PV)
AJUSTE_RENDIMIENTO = {
    "bajo":  {"carcasa": -1.5, "contenido_gi": +0.8, "plumas": +0.2},  # ayuno deficiente, lote pobre
    "medio": {},
    "alto":  {"carcasa": +1.2, "contenido_gi": -0.5},                   # cerca del objetivo genético
}

# ---------------------------------------------------------------------------
# 3. TROZADO — fracción de la carcasa apta (base carcasa), a 2,9 kg, escenario medio
#    Todos los cortes de trozado son CON PIEL y CON HUESO.
# ---------------------------------------------------------------------------
CORTES = [
    ("pechuga_con_hueso",  38.5, +1.20),   # pechuga entera con piel y hueso
    ("pata_muslo",         31.0, -0.40),   # cuarto trasero con piel y hueso, sin espinazo
    ("alas",               10.2, -0.50),   # ala entera (3 segmentos), con piel y hueso
    ("carcasa_esqueleto",  19.3, -0.30),   # espinazo, rabadilla, costillar remanente, grasa abdominal
    ("recortes_trozado",    0.5,  0.00),   # recortes comestibles (carne y piel)
    ("merma_trozado",       0.5,  0.00),   # aserrín de hueso, exudado
]
AJUSTE_CORTES = {
    "bajo":  {"pechuga_con_hueso": -1.0, "carcasa_esqueleto": +1.0},
    "medio": {},
    "alto":  {"pechuga_con_hueso": +1.0, "carcasa_esqueleto": -1.0},
}
FRACCION_MUSLO_EN_PATA_MUSLO = 0.58          # resto = pata (drumstick)

# ---------------------------------------------------------------------------
# 4. DESHUESE — fracción del corte de origen (cada fila suma 1)
# ---------------------------------------------------------------------------
DESHUESE = {
    "pechuga_con_hueso": {"suprema": 0.610, "solomillo": 0.150, "piel": 0.080,
                          "hueso": 0.130, "recortes": 0.020, "merma": 0.010},
    "muslo":             {"carne": 0.660, "piel": 0.130, "hueso": 0.170,
                          "recortes": 0.030, "merma": 0.010},
    "pata":              {"carne": 0.560, "piel": 0.110, "hueso": 0.300,
                          "recortes": 0.020, "merma": 0.010},
}
CMS_RENDIMIENTO = {"bajo": 0.55, "medio": 0.60, "alto": 0.65}   # CMS / materia prima
CMS_MERMA = 0.01

# ---------------------------------------------------------------------------
# 5. RUTAS ALTERNATIVAS (exclusivas) — SUP-045
# ---------------------------------------------------------------------------
OPCIONES_RUTA = {
    "esqueleto":     ("venta", "cms"),
    "cuello":        ("venta", "cms"),
    "hueso_pechuga": ("rendering", "cms"),
    "piel":          ("venta", "rendering"),
}
RUTAS_POR_DEFECTO = {
    "A": {"esqueleto": "venta", "cuello": "venta", "hueso_pechuga": "rendering", "piel": "venta"},
    "B": {"esqueleto": "venta", "cuello": "venta", "hueso_pechuga": "rendering", "piel": "venta"},
    "C": {"esqueleto": "cms",   "cuello": "venta", "hueso_pechuga": "rendering", "piel": "venta"},
}

# ---------------------------------------------------------------------------
# 6. SUBPRODUCTOS
# ---------------------------------------------------------------------------
SANGRE_RECUPERADA = 0.85          # fracción de la sangre drenada que llega al tanque de sangre
AGUA_ADHERIDA_PLUMAS = 0.60       # kg de agua adherida por kg de pluma biológica (pluma cruda húmeda)
MERMA_ACOND_PATAS = 0.05          # fracción de la pata removida al escaldar y pelar (cutícula, suciedad)

# ---------------------------------------------------------------------------
# 7. CONDENAS Y MERMAS — escenarios (bajo = pocos problemas)
# ---------------------------------------------------------------------------
CONDENAS = {
    #        decomiso total   decomiso parcial   canales no aptas     garras: grado A / 2.ª / descarte
    #        (fracción aves)  (fracción carcasa) para entero (fr.)
    "bajo":  {"total": 0.004, "parcial": 0.003, "degradadas": 0.03, "garras": (0.90, 0.08, 0.02)},
    "medio": {"total": 0.010, "parcial": 0.008, "degradadas": 0.06, "garras": (0.80, 0.15, 0.05)},
    "alto":  {"total": 0.027, "parcial": 0.015, "degradadas": 0.12, "garras": (0.60, 0.25, 0.15)},
}
ORIGENES_DECOMISO_TOTAL = ("carcasa", "cuello", "higado", "corazon", "molleja", "patas")

# ---------------------------------------------------------------------------
# 8. ENFRIAMIENTO (CHILLER) — agua absorbida por la carcasa / evaporación
# ---------------------------------------------------------------------------
ENFRIAMIENTO = {
    # absorción: kg agua / kg carcasa pre-chiller; goteo: fracción del agua absorbida que se
    # pierde antes de la venta (escurrido + purga); evaporación: fracción de la masa perdida
    "inmersion":        {"absorcion": 0.060, "goteo": 0.30, "evaporacion": 0.000},
    "inmersion_limite": {"absorcion": 0.080, "goteo": 0.30, "evaporacion": 0.000},
    "aire":             {"absorcion": 0.000, "goteo": 0.00, "evaporacion": 0.018},
}

FRACCION_GRASA_RETIRADA = 0.0     # 0 = la grasa abdominal queda en la carcasa (práctica a validar)
MENUDENCIAS_CON_ENTERO = False    # en config. A las menudencias se venden aparte (parámetro)
DESHUESAR_PATA = False            # en config. C la pata (drumstick) se vende con hueso

# ---------------------------------------------------------------------------
# 9. BANDAS DE PLAUSIBILIDAD (para tests; % del PV salvo indicación) — rangos de fuentes [PVDP]
# ---------------------------------------------------------------------------
BANDAS_PV = {
    "carcasa": (66.0, 78.0), "sangre": (2.5, 4.5), "plumas": (3.0, 9.0),
    "cabeza": (2.0, 3.5), "patas": (3.0, 5.5), "menudencias": (3.0, 6.0),
    "cuello": (1.5, 4.5), "no_comestibles": (3.5, 10.0), "perdidas_no_asignadas": (0.0, 4.0),
}
BANDAS_CARCASA = {"pechuga_con_hueso": (33.0, 44.0), "pata_muslo": (27.0, 35.0),
                  "alas": (8.5, 13.0), "carcasa_esqueleto": (14.0, 24.0)}
LIMITE_AGUA_RETENIDA = 0.08       # 8 % del peso (límite argentino según prensa [PVDP], FTE-168)

# ---------------------------------------------------------------------------
# 10. DESCRIPCIÓN DE CADA SALIDA (clase única, destino conceptual)
# ---------------------------------------------------------------------------
DESTINO = {
    "sangre recuperada": ("C", "rendering (harina de sangre) / tratamiento; separada del efluente"),
    "sangre no recuperada": ("D", "efluente (alta DBO/DQO)"),
    "plumas crudas": ("C", "hidrólisis -> harina de plumas (rendering propio o tercero)"),
    "cabeza": ("C", "rendering"),
    "merma de acondicionamiento de patas": ("D", "cutícula y suciedad removidas al escaldar/pelar -> efluente / lodos"),
    "garras grado A": ("B", "coproducto comestible (mercado interno / exportación potencial)"),
    "garras de segunda": ("B", "coproducto comestible de menor grado"),
    "garras descarte": ("C", "rendering"),
    "higado": ("B", "menudencia"), "corazon": ("B", "menudencia"), "molleja": ("B", "menudencia"),
    "cuello": ("B", "coproducto comestible (menudencia)"),
    "tracto digestivo": ("C", "rendering (harina de vísceras)"),
    "contenido gastrointestinal": ("D", "residuo sólido / efluente (tratamiento)"),
    "pulmones": ("C", "rendering"),
    "otros no comestibles": ("C", "rendering"),
    "decomiso total": ("D", "decomiso: destino según normativa (rendering o eliminación)"),
    "decomiso parcial": ("D", "decomiso: destino según normativa (rendering o eliminación)"),
    "grasa abdominal retirada": ("C", "grasa / rendering"),
    "evaporacion en enfriamiento": ("P", "vapor (pérdida de humedad del tejido)"),
    "agua de goteo del producto": ("D", "agua absorbida en el chiller que gotea antes de la venta -> efluente"),
    "pollo entero": ("A", "producto principal"),
    "pechuga con hueso": ("A", "producto principal"),
    "pata-muslo": ("A", "producto principal"),
    "alas": ("B", "coproducto comestible (corte secundario)"),
    "carcasa-esqueleto": ("B", "coproducto comestible (venta para sopa/caldo) — ruta 'venta'"),
    "recortes": ("B", "coproducto comestible (elaborados / CMS)"),
    "merma de trozado": ("P", "merma real (aserrín, exudado) -> efluente"),
    "suprema": ("A", "producto principal"), "solomillo": ("A", "producto principal"),
    "muslo deshuesado": ("A", "producto principal"), "pata con hueso": ("A", "producto principal"),
    "pata deshuesada": ("A", "producto principal"),
    "piel": ("B", "coproducto comestible (elaborados) — ruta 'venta'"),
    "piel a rendering": ("C", "rendering — ruta 'rendering'"),
    "hueso": ("C", "rendering (harina de carne y hueso) / caldos"),
    "merma de deshuese": ("P", "merma real de proceso -> efluente"),
    "CMS": ("B", "coproducto comestible (industria de elaborados) — ruta 'cms'"),
    "residuo oseo de CMS": ("C", "rendering"),
    "merma de CMS": ("P", "merma real de proceso"),
    "perdidas no asignadas": ("P", "humedad, tejidos al efluente, no identificado (a medir en planta)"),
}
COMPONENTES_COMESTIBLES_FAENA = ("higado", "corazon", "molleja", "cuello", "garras grado A", "garras de segunda")


class ErrorBalance(Exception):
    """Error de balance o de parámetros: detiene el modelo."""


# ---------------------------------------------------------------------------
# 11. CÁLCULO
# ---------------------------------------------------------------------------
def fracciones_primarias(peso: float, rendimiento: str) -> dict:
    """Fracciones del PV (0-1) de cada componente primario + pérdidas no asignadas."""
    if not (RANGO_VALIDO[0] <= peso <= RANGO_VALIDO[1]):
        raise ErrorBalance(f"Peso vivo {peso} kg fuera del rango válido {RANGO_VALIDO} (no extrapolar)")
    aj = AJUSTE_RENDIMIENTO[rendimiento]
    fr = {}
    for clave, ref, pend in PRIMARIOS:
        pct = ref + aj.get(clave, 0.0) + pend * (peso - PESO_REF)
        if pct < 0:
            raise ErrorBalance(f"Fracción negativa para {clave} a {peso} kg")
        fr[clave] = pct / 100.0
    fr["perdidas_no_asignadas"] = 1.0 - sum(fr.values())
    if fr["perdidas_no_asignadas"] < -1e-12:
        raise ErrorBalance(f"Componentes primarios suman más del 100 % del PV a {peso} kg")
    return fr


def fracciones_cortes(peso: float, rendimiento: str) -> dict:
    """Fracciones de la carcasa apta (0-1) asignadas a cada corte de trozado."""
    aj = AJUSTE_CORTES[rendimiento]
    return {c: (ref + aj.get(c, 0.0) + pend * (peso - PESO_REF)) / 100.0 for c, ref, pend in CORTES}


def fraccion_grasa(peso: float) -> float:
    return (GRASA_ABDOMINAL[0] + GRASA_ABDOMINAL[1] * (peso - PESO_REF)) / 100.0


def resolver_rutas(config: str, rutas: dict | None) -> dict:
    r = dict(RUTAS_POR_DEFECTO[config])
    for k, v in (rutas or {}).items():
        if k not in OPCIONES_RUTA or v not in OPCIONES_RUTA[k]:
            raise ErrorBalance(f"Ruta inválida: {k}={v}")
        r[k] = v
    return r


def balance(peso: float, config: str = "B", rendimiento: str = "medio",
            condenas: str = "medio", enfriamiento: str = "inmersion", rutas: dict | None = None) -> dict:
    """Balance de masa de UN ave. Devuelve dict con filas, entradas y controles."""
    if config not in CONFIGS:
        raise ErrorBalance(f"Configuración desconocida: {config}")
    ruta = resolver_rutas(config, rutas)
    fr = fracciones_primarias(peso, rendimiento)
    m = {k: v * peso for k, v in fr.items()}            # kg biológicos por componente primario
    cnd = CONDENAS[condenas]
    enf = ENFRIAMIENTO[enfriamiento]
    ft, fp = cnd["total"], cnd["parcial"]
    filas = []

    def fila(etapa, componente, origen, bio, agua=0.0, deriva_de_carcasa=None):
        clase, destino = DESTINO[componente]
        filas.append({"etapa": etapa, "componente": componente, "origen": origen, "clase": clase,
                      "destino": destino, "bio": bio, "agua": agua,
                      "deriva_de_carcasa": (origen == "carcasa") if deriva_de_carcasa is None else deriva_de_carcasa})

    # --- Sangre, plumas, cabeza ------------------------------------------------
    fila("faena", "sangre recuperada", "sangre", m["sangre"] * SANGRE_RECUPERADA)
    fila("faena", "sangre no recuperada", "sangre", m["sangre"] * (1 - SANGRE_RECUPERADA))
    agua_plumas = m["plumas"] * AGUA_ADHERIDA_PLUMAS
    fila("faena", "plumas crudas", "plumas", m["plumas"], agua_plumas)
    fila("faena", "cabeza", "cabeza", m["cabeza"])

    # --- Patas: PATA BRUTA = decomiso + merma de acondicionamiento + garras A + 2.ª + descarte ----
    patas_ok = m["patas"] * (1 - ft)
    fila("condenas", "decomiso total", "patas", m["patas"] * ft)
    fila("acondicionamiento de patas", "merma de acondicionamiento de patas", "patas", patas_ok * MERMA_ACOND_PATAS)
    limpias = patas_ok * (1 - MERMA_ACOND_PATAS)
    qa, q2, qd = cnd["garras"]
    fila("acondicionamiento de patas", "garras grado A", "patas", limpias * qa)
    fila("acondicionamiento de patas", "garras de segunda", "patas", limpias * q2)
    fila("acondicionamiento de patas", "garras descarte", "patas", limpias * qd)

    # --- Menudencias y cuello --------------------------------------------------
    for clave in ("higado", "corazon", "molleja"):
        fila("condenas", "decomiso total", clave, m[clave] * ft)
        fila("faena", clave, clave, m[clave] * (1 - ft))
    fila("condenas", "decomiso total", "cuello", m["cuello"] * ft)
    cuello_ok = m["cuello"] * (1 - ft)

    # --- Vísceras no comestibles y pérdidas no asignadas (de la faena primaria) --
    fila("faena", "tracto digestivo", "tracto_digestivo", m["tracto_digestivo"])
    fila("faena", "contenido gastrointestinal", "contenido_gi", m["contenido_gi"])
    fila("faena", "pulmones", "pulmones", m["pulmones"])
    fila("faena", "otros no comestibles", "otros_no_comestibles", m["otros_no_comestibles"])
    fila("faena", "perdidas no asignadas", "perdidas_no_asignadas", m["perdidas_no_asignadas"])

    # --- Carcasa: condenas, grasa, enfriamiento --------------------------------
    carc = m["carcasa"]
    dec_total_carc = carc * ft
    fila("condenas", "decomiso total", "carcasa", dec_total_carc, deriva_de_carcasa=False)
    c1 = carc - dec_total_carc
    dec_parcial = c1 * fp
    fila("condenas", "decomiso parcial", "carcasa", dec_parcial, deriva_de_carcasa=False)
    c1 -= dec_parcial                                   # carcasa apta (después de inspección)
    grasa = fraccion_grasa(peso) * peso * (1 - ft) * (1 - fp) * FRACCION_GRASA_RETIRADA
    fila("faena", "grasa abdominal retirada", "carcasa", grasa)
    c2 = c1 - grasa                                     # carcasa pre-chiller (biológica)
    evap = c2 * enf["evaporacion"]
    fila("enfriamiento", "evaporacion en enfriamiento", "carcasa", evap, deriva_de_carcasa=False)
    c3 = c2 - evap                                      # carcasa fría disponible, masa biológica
    agua_abs = c2 * enf["absorcion"]                    # agua absorbida por la carcasa en el chiller
    agua_goteo = agua_abs * enf["goteo"]
    agua_ret = agua_abs - agua_goteo                    # agua retenida en producto (se vende)
    filas.append({"etapa": "enfriamiento", "componente": "agua de goteo del producto", "origen": "agua_chiller",
                  "clase": "D", "destino": DESTINO["agua de goteo del producto"][1], "bio": 0.0,
                  "agua": agua_goteo, "deriva_de_carcasa": False})

    # --- Asignación comercial de la carcasa fría (c3) --------------------------
    fc = fracciones_cortes(peso, rendimiento)
    destino_carcasa = []                                # (etapa, componente, kg bio)
    cms_carcasa = []                                    # (material, kg bio) enviados a CMS
    r_cms = CMS_RENDIMIENTO[rendimiento]

    def esqueleto(masa, etapa):
        if ruta["esqueleto"] == "venta":
            destino_carcasa.append((etapa, "carcasa-esqueleto", masa))
        else:
            cms_carcasa.append(("esqueleto", masa))

    def trozar(masa, etapa):
        destino_carcasa.append((etapa, "pechuga con hueso", masa * fc["pechuga_con_hueso"]))
        destino_carcasa.append((etapa, "pata-muslo", masa * fc["pata_muslo"]))
        destino_carcasa.append((etapa, "alas", masa * fc["alas"]))
        esqueleto(masa * fc["carcasa_esqueleto"], etapa)
        destino_carcasa.append((etapa, "recortes", masa * fc["recortes_trozado"]))
        destino_carcasa.append((etapa, "merma de trozado", masa * fc["merma_trozado"]))

    def piel(etapa, kg):
        destino_carcasa.append((etapa, "piel" if ruta["piel"] == "venta" else "piel a rendering", kg))

    if config == "A":
        g = cnd["degradadas"]
        destino_carcasa.append(("entero", "pollo entero", c3 * (1 - g)))
        trozar(c3 * g, "trozado (canales no aptas para entero)")
    elif config == "B":
        trozar(c3, "trozado")
    else:  # C
        pech = c3 * fc["pechuga_con_hueso"]
        pm = c3 * fc["pata_muslo"]
        muslo = pm * FRACCION_MUSLO_EN_PATA_MUSLO
        pata = pm - muslo
        d = DESHUESE["pechuga_con_hueso"]
        destino_carcasa += [("deshuese pechuga", "suprema", pech * d["suprema"]),
                            ("deshuese pechuga", "solomillo", pech * d["solomillo"]),
                            ("deshuese pechuga", "recortes", pech * d["recortes"]),
                            ("deshuese pechuga", "merma de deshuese", pech * d["merma"])]
        piel("deshuese pechuga", pech * d["piel"])
        if ruta["hueso_pechuga"] == "rendering":
            destino_carcasa.append(("deshuese pechuga", "hueso", pech * d["hueso"]))
        else:
            cms_carcasa.append(("hueso de pechuga", pech * d["hueso"]))
        d = DESHUESE["muslo"]
        destino_carcasa += [("deshuese muslo", "muslo deshuesado", muslo * d["carne"]),
                            ("deshuese muslo", "hueso", muslo * d["hueso"]),
                            ("deshuese muslo", "recortes", muslo * d["recortes"]),
                            ("deshuese muslo", "merma de deshuese", muslo * d["merma"])]
        piel("deshuese muslo", muslo * d["piel"])
        if DESHUESAR_PATA:
            d = DESHUESE["pata"]
            destino_carcasa += [("deshuese pata", "pata deshuesada", pata * d["carne"]),
                                ("deshuese pata", "hueso", pata * d["hueso"]),
                                ("deshuese pata", "recortes", pata * d["recortes"]),
                                ("deshuese pata", "merma de deshuese", pata * d["merma"])]
            piel("deshuese pata", pata * d["piel"])
        else:
            destino_carcasa.append(("trozado", "pata con hueso", pata))
        destino_carcasa.append(("trozado", "alas", c3 * fc["alas"]))
        esqueleto(c3 * fc["carcasa_esqueleto"], "trozado")
        destino_carcasa.append(("trozado", "recortes", c3 * fc["recortes_trozado"]))
        destino_carcasa.append(("trozado", "merma de trozado", c3 * fc["merma_trozado"]))

    # Materiales de la carcasa a CMS: una etapa por material (trazabilidad del origen)
    for material, kg in cms_carcasa:
        etapa = f"CMS ({material})"
        destino_carcasa += [(etapa, "CMS", kg * r_cms),
                            (etapa, "residuo oseo de CMS", kg * (1 - r_cms - CMS_MERMA)),
                            (etapa, "merma de CMS", kg * CMS_MERMA)]

    # Agua retenida: se reparte proporcionalmente a la masa biológica de las salidas
    # de la carcasa que no son mermas reales (clase P no retiene agua).
    base_agua = sum(kg for _, comp, kg in destino_carcasa if DESTINO[comp][0] != "P")
    for etapa, comp, kg in destino_carcasa:
        agua = agua_ret * kg / base_agua if (DESTINO[comp][0] != "P" and base_agua > 0) else 0.0
        fila(etapa, comp, "carcasa", kg, agua)

    # Cuello: venta o CMS (sin agua modelada)
    if ruta["cuello"] == "venta":
        fila("faena", "cuello", "cuello", cuello_ok)
    else:
        fila("CMS (cuello)", "CMS", "cuello", cuello_ok * r_cms)
        fila("CMS (cuello)", "residuo oseo de CMS", "cuello", cuello_ok * (1 - r_cms - CMS_MERMA))
        fila("CMS (cuello)", "merma de CMS", "cuello", cuello_ok * CMS_MERMA)

    agua_incorporada = agua_plumas + agua_abs
    salida_bio = sum(f["bio"] for f in filas)
    salida_agua = sum(f["agua"] for f in filas)
    return {
        "peso": peso, "config": config, "rendimiento": rendimiento, "condenas": condenas,
        "enfriamiento": enfriamiento, "rutas": ruta, "filas": filas, "primarios": m, "fracciones": fr,
        "cortes": fc, "carcasa_bio": carc, "carcasa_apta": c1, "carcasa_prechiller": c2,
        "carcasa_fria_bio": c3, "decomiso_total_carcasa": dec_total_carc, "decomiso_parcial": dec_parcial,
        "grasa_retirada": grasa, "evaporacion": evap, "cms_carcasa": cms_carcasa,
        "agua_absorbida_chiller": agua_abs, "agua_retenida_producto": agua_ret,
        "agua_goteo_producto": agua_goteo, "agua_adherida_plumas": agua_plumas,
        "entrada_bio": peso, "entrada_agua": agua_incorporada,
        "salida_bio": salida_bio, "salida_agua": salida_agua,
        "error_kg": (peso + agua_incorporada) - (salida_bio + salida_agua),
    }


def verificar_cierre(b: dict, factor: float = 1.0) -> None:
    """Detiene el modelo si el balance no cierra dentro de la tolerancia."""
    tol = TOL_KG_POR_AVE * factor
    if abs(b["error_kg"]) * factor > tol:
        raise ErrorBalance(f"Balance no cierra: error {b['error_kg']:.3e} kg/ave ({b['config']}, {b['peso']} kg)")
    if abs(b["salida_bio"] - b["entrada_bio"]) * factor > tol:
        raise ErrorBalance("Masa biológica no cierra")
    if abs(b["salida_agua"] - b["entrada_agua"]) * factor > tol:
        raise ErrorBalance("Agua incorporada no cierra")


def agregar(b: dict) -> dict:
    """Suma filas por (clase, componente) -> {(clase, comp): [bio, agua]}."""
    out = defaultdict(lambda: [0.0, 0.0])
    for f in b["filas"]:
        out[(f["clase"], f["componente"])][0] += f["bio"]
        out[(f["clase"], f["componente"])][1] += f["agua"]
    return out


def totales_por_clase(b: dict) -> dict:
    out = defaultdict(lambda: [0.0, 0.0])
    for f in b["filas"]:
        out[f["clase"]][0] += f["bio"]
        out[f["clase"]][1] += f["agua"]
    return out


def suma(b: dict, cond) -> float:
    return sum(f["bio"] for f in b["filas"] if cond(f))


def reconciliacion_comestible(b: dict) -> dict:
    """Masa comestible disponible después de la inspección (misma para A, B y C a igual ave y
    escenario) y su transformación en productos. Todo en masa biológica."""
    disponible = b["carcasa_fria_bio"] + suma(b, lambda f: f["componente"] in COMPONENTES_COMESTIBLES_FAENA) \
        + suma(b, lambda f: f["origen"] == "cuello" and f["etapa"].startswith("CMS"))
    procesados = lambda f: f["origen"] in ("carcasa", "cuello") and f["etapa"] not in ("condenas", "enfriamiento", "faena")
    merma = suma(b, lambda f: procesados(f) and f["clase"] == "P")
    a_c = suma(b, lambda f: procesados(f) and f["clase"] == "C")
    comestible = suma(b, lambda f: f["clase"] in "AB")
    return {"disponible": disponible, "merma_real": merma, "reclasificado_C": a_c,
            "comestible": comestible, "cierre": disponible - merma - a_c - comestible}


# ---------------------------------------------------------------------------
# 12. GRILLA DE ESCENARIOS
# ---------------------------------------------------------------------------
VARIANTES = [("bajo", "medio", "inmersion"), ("medio", "medio", "inmersion"),
             ("alto", "medio", "inmersion"), ("medio", "bajo", "inmersion"),
             ("medio", "alto", "inmersion"), ("medio", "medio", "inmersion_limite"),
             ("medio", "medio", "aire")]
VARIANTES_RUTA = [("B", {"esqueleto": "cms"}), ("C", {"esqueleto": "venta"}),
                  ("C", {"cuello": "cms", "hueso_pechuga": "cms", "piel": "rendering"})]


def grilla():
    """6 pesos × (3 configuraciones × 7 variantes + 3 variantes de ruta) = 144 balances."""
    for peso in PESOS:
        for cfg in CONFIGS:
            for rend, cond, enf in VARIANTES:
                yield balance(peso, cfg, rend, cond, enf)
        for cfg, rutas in VARIANTES_RUTA:
            yield balance(peso, cfg, rutas=rutas)


def todas_las_rutas():
    """Todas las combinaciones de rutas para cada configuración (tests de exclusividad)."""
    claves = list(OPCIONES_RUTA)
    for cfg in CONFIGS:
        for combo in itertools.product(*(OPCIONES_RUTA[k] for k in claves)):
            yield cfg, dict(zip(claves, combo))


def escalas(kg_ave: float) -> dict:
    d = {"kg_1000_aves": kg_ave * 1000}
    for n in AVES_DIA:
        d[f"t_dia_{n}_aves_dia"] = kg_ave * n / 1000
    for n in AVES_DIA:
        d[f"t_anio_{n}_aves_dia"] = kg_ave * n * DIAS_FAENA_ANIO / 1000
    d["t_anio_1M_aves_anio"] = kg_ave * AVES_ANIO_REF / 1000
    d["t_dia_1M_aves_anio"] = kg_ave * AVES_ANIO_REF / DIAS_FAENA_ANIO / 1000
    return d


# ---------------------------------------------------------------------------
# 13. TESTS AUTOMÁTICOS
# ---------------------------------------------------------------------------
def ejecutar_tests(verbose: bool = True) -> list:
    resultados = []

    def chk(nombre, cond, detalle=""):
        resultados.append((nombre, bool(cond), detalle))

    balances = list(grilla())
    rutas_bal = [balance(p, cfg, rend, "medio", enf, rutas=r)
                 for p in (2.2, 2.9, 3.5) for cfg, r in todas_las_rutas()
                 for rend in ("bajo", "medio", "alto") for enf in ("inmersion", "aire")]
    todos = balances + rutas_bal
    n = len(todos)

    # T01 cierre por ave (total, biológico y agua por separado)
    errs = []
    for b in todos:
        try:
            verificar_cierre(b)
        except ErrorBalance as e:
            errs.append(str(e))
    chk(f"T01 cierre por ave ({n} balances; total, masa biológica y agua)", not errs,
        f"error máx = {max(abs(b['error_kg']) for b in todos):.2e} kg/ave; tolerancia {TOL_KG_POR_AVE:.0e}")

    # T02 cierre por 1.000 aves
    ok = True
    for b in todos:
        e_1000 = (b["entrada_bio"] + b["entrada_agua"]) * 1000 - sum((f["bio"] + f["agua"]) * 1000 for f in b["filas"])
        ok &= abs(e_1000) <= TOL_KG_POR_AVE * 1000
    chk("T02 cierre por 1.000 aves", ok, f"tolerancia {TOL_KG_POR_AVE * 1000:.0e} kg por 1.000 aves")

    # T03 ningún componente negativo
    neg = [(b["peso"], b["config"], f["componente"]) for b in todos for f in b["filas"]
           if f["bio"] < -1e-12 or f["agua"] < -1e-12]
    chk("T03 ningún componente negativo", not neg, str(neg[:3]))

    # T04 porcentajes razonables (bandas de fuentes)
    fuera = []
    for b in balances:
        fr = {k: v * 100 for k, v in b["fracciones"].items()}
        vals = {"carcasa": fr["carcasa"], "sangre": fr["sangre"], "plumas": fr["plumas"],
                "cabeza": fr["cabeza"], "patas": fr["patas"],
                "menudencias": fr["higado"] + fr["corazon"] + fr["molleja"], "cuello": fr["cuello"],
                "no_comestibles": fr["tracto_digestivo"] + fr["contenido_gi"] + fr["pulmones"] + fr["otros_no_comestibles"],
                "perdidas_no_asignadas": fr["perdidas_no_asignadas"]}
        for k, v in vals.items():
            lo, hi = BANDAS_PV[k]
            if not lo <= v <= hi:
                fuera.append((b["peso"], b["rendimiento"], k, round(v, 2)))
        for k, (lo, hi) in BANDAS_CARCASA.items():
            if not lo <= b["cortes"][k] * 100 <= hi:
                fuera.append((b["peso"], b["rendimiento"], k, round(b["cortes"][k] * 100, 2)))
        if b["carcasa_fria_bio"] > 0:
            frac_agua = b["agua_retenida_producto"] / (b["carcasa_fria_bio"] + b["agua_retenida_producto"])
            if frac_agua > LIMITE_AGUA_RETENIDA + 1e-12:
                fuera.append((b["peso"], b["enfriamiento"], "agua_retenida", round(frac_agua * 100, 2)))
    chk("T04 porcentajes dentro de bandas de fuentes", not fuera, str(fuera[:5]))

    # T05 suma de cortes = carcasa fría disponible (<= carcasa eviscerada)
    ok = True
    for b in todos:
        cortes = suma(b, lambda f: f["origen"] == "carcasa" and f["etapa"] not in ("condenas", "enfriamiento", "faena"))
        ok &= cortes <= b["carcasa_bio"] + 1e-12 and abs(cortes - b["carcasa_fria_bio"]) <= TOL_KG_POR_AVE
    chk("T05 suma de cortes = carcasa fría disponible (<= carcasa eviscerada)", ok)

    # T06 suma de deshuesados <= cortes de origen; fracciones de deshuese suman 1
    ok = all(abs(sum(v.values()) - 1) < 1e-12 for v in DESHUESE.values())
    for b in (x for x in todos if x["config"] == "C"):
        c3, fc = b["carcasa_fria_bio"], b["cortes"]
        pech_total = c3 * fc["pechuga_con_hueso"]
        pech = suma(b, lambda f: f["etapa"] == "deshuese pechuga") + sum(kg for mat, kg in b["cms_carcasa"] if mat == "hueso de pechuga")
        mus = suma(b, lambda f: f["etapa"] == "deshuese muslo")
        ok &= abs(pech - pech_total) <= TOL_KG_POR_AVE
        ok &= mus <= c3 * fc["pata_muslo"] * FRACCION_MUSLO_EN_PATA_MUSLO + 1e-12
        carne = suma(b, lambda f: f["componente"] in ("suprema", "solomillo", "muslo deshuesado"))
        ok &= carne < pech + mus
    chk("T06 suma de deshuesados <= cortes de origen", ok)

    # T07 escalado lineal
    ok = True
    for f in balance(2.9)["filas"]:
        kg = f["bio"] + f["agua"]
        e = escalas(kg)
        ok &= abs(e["kg_1000_aves"] - 1000 * kg) < 1e-9
        for nn in AVES_DIA:
            ok &= abs(e[f"t_anio_{nn}_aves_dia"] - e[f"t_dia_{nn}_aves_dia"] * DIAS_FAENA_ANIO) < 1e-9
        ok &= abs(e["t_dia_10000_aves_dia"] - 2 * e["t_dia_5000_aves_dia"]) < 1e-9
        ok &= abs(e["t_anio_1M_aves_anio"] - kg * 1000) < 1e-9
    chk("T07 escalado lineal (1 ave -> 1.000 aves -> t/día -> t/año)", ok)

    # T08 agua separada de la masa biológica
    ok = True
    for b in todos:
        ok &= abs(sum(f["bio"] for f in b["filas"]) - b["peso"]) <= TOL_KG_POR_AVE
        ok &= all(f["agua"] == 0.0 for f in b["filas"] if f["clase"] == "P")
        if b["enfriamiento"] == "aire":
            ok &= abs(b["agua_retenida_producto"]) < 1e-15
            ok &= all(f["agua"] == 0 for f in b["filas"] if f["origen"] == "carcasa")
        agua_carc = sum(f["agua"] for f in b["filas"] if f["origen"] == "carcasa")
        ok &= abs(agua_carc - b["agua_retenida_producto"]) <= TOL_KG_POR_AVE
        ok &= abs(b["entrada_agua"] - b["agua_absorbida_chiller"] - b["agua_adherida_plumas"]) <= 1e-15
    chk("T08 agua separada de masa biológica (Σ bio = PV; agua solo en columna agua)", ok)

    # T09 unidades y sumas de fracciones
    ok = True
    for b in todos:
        ok &= abs(sum(b["fracciones"].values()) - 1) < 1e-12
        ok &= abs(sum(b["cortes"].values()) - 1) < 1e-12
        ok &= abs(sum(b["primarios"].values()) - b["peso"]) < 1e-12
    ok &= all(0 <= v <= 1 for v in (SANGRE_RECUPERADA, MERMA_ACOND_PATAS, FRACCION_GRASA_RETIRADA,
                                    FRACCION_MUSLO_EN_PATA_MUSLO))
    ok &= all(abs(sum(c["garras"]) - 1) < 1e-12 for c in CONDENAS.values())
    chk("T09 unidades consistentes (fracciones suman 1; kg primarios = PV)", ok)

    # T10 sin doble conteo: cada componente primario se asigna exactamente una vez
    ok, det = True, []
    for b in todos:
        por_origen = defaultdict(float)
        for f in b["filas"]:
            if f["origen"] != "agua_chiller":
                por_origen[f["origen"]] += f["bio"]
        for k, v in b["primarios"].items():
            if abs(por_origen[k] - v) > TOL_KG_POR_AVE:
                ok = False
                det.append((b["peso"], b["config"], k))
        claves = [(f["etapa"], f["componente"], f["origen"]) for f in b["filas"]]
        ok &= len(claves) == len(set(claves))
        ok &= not any(f["origen"] == "carcasa" and f["componente"] in COMPONENTES_COMESTIBLES_FAENA for f in b["filas"])
    chk("T10 sin doble conteo (cada kg primario asignado a un solo destino)", ok, str(det[:3]))

    # T11 no linealidad con el peso (dirección de alometría)
    b1, b2 = balance(2.2), balance(3.5)
    pech = lambda b: suma(b, lambda f: f["componente"] == "pechuga con hueso")
    ok = pech(b2) / pech(b1) > 3.5 / 2.2
    ok &= (b2["primarios"]["cabeza"] / b1["primarios"]["cabeza"]) < 3.5 / 2.2
    ok &= (b2["primarios"]["patas"] / b1["primarios"]["patas"]) < 3.5 / 2.2
    chk("T11 no linealidad: pechuga crece más que el PV; cabeza y patas, menos", ok)

    # T12 no extrapolar fuera del rango válido
    try:
        balance(4.5)
        ok = False
    except ErrorBalance:
        ok = True
    chk("T12 rechazo de pesos fuera de rango (2,0-3,8 kg)", ok)

    # T13 clases completas y conocidas
    chk("T13 toda salida clasificada A/B/C/D/P", all(f["clase"] in "ABCDP" for b in todos for f in b["filas"]))

    # ---------------- Tests de exclusividad (auditoría conceptual v1.1) ----------------
    # T14 decomisos no duplicados
    ok = True
    for b in todos:
        m, ft = b["primarios"], CONDENAS[b["condenas"]]["total"]
        dec = [f for f in b["filas"] if f["componente"].startswith("decomiso")]
        esperado = ft * sum(m[o] for o in ORIGENES_DECOMISO_TOTAL) + b["decomiso_parcial"]
        ok &= abs(sum(f["bio"] for f in dec) - esperado) <= TOL_KG_POR_AVE
        ok &= all(f["clase"] == "D" and f["etapa"] == "condenas" for f in dec)
        tot = [f["origen"] for f in dec if f["componente"] == "decomiso total"]
        ok &= sorted(tot) == sorted(ORIGENES_DECOMISO_TOTAL)          # una sola vez por origen
        ok &= sum(1 for f in dec if f["componente"] == "decomiso parcial") == 1
        pna = [f for f in b["filas"] if f["componente"] == "perdidas no asignadas"]
        ok &= len(pna) == 1 and pna[0]["origen"] == "perdidas_no_asignadas"
        ok &= abs(pna[0]["bio"] - m["perdidas_no_asignadas"]) <= 1e-15  # no contiene decomisos
        ok &= abs(b["carcasa_bio"] - b["decomiso_total_carcasa"] - b["decomiso_parcial"]
                  - b["grasa_retirada"] - b["evaporacion"] - b["carcasa_fria_bio"]) <= TOL_KG_POR_AVE
    chk("T14 decomisos no duplicados (una vez, en D; fuera de pérdidas y de la carcasa disponible)", ok)

    # T15 PATA BRUTA = garra A + segunda + descarte + merma de acondicionamiento + decomiso de patas
    ok = True
    for b in todos:
        partes = suma(b, lambda f: f["origen"] == "patas")
        comps = {f["componente"] for f in b["filas"] if f["origen"] == "patas"}
        ok &= abs(partes - b["primarios"]["patas"]) <= TOL_KG_POR_AVE
        ok &= comps == {"garras grado A", "garras de segunda", "garras descarte",
                        "merma de acondicionamiento de patas", "decomiso total"}
    chk("T15 pata bruta = garras A + segunda + descarte + merma de acondicionamiento + decomiso", ok)

    # T16 carcasa-esqueleto vendida y CMS derivada de ella no coexisten
    ok = True
    for b in todos:
        vendida = any(f["componente"] == "carcasa-esqueleto" for f in b["filas"])
        cms_esq = any(f["etapa"] == "CMS (esqueleto)" for f in b["filas"])
        ok &= not (vendida and cms_esq)
        ok &= vendida == (b["rutas"]["esqueleto"] == "venta")
        cuello_v = any(f["componente"] == "cuello" for f in b["filas"])
        cuello_cms = any(f["etapa"] == "CMS (cuello)" for f in b["filas"])
        ok &= (cuello_v != cuello_cms) or b["primarios"]["cuello"] == 0
        piel_v = any(f["componente"] == "piel" for f in b["filas"])
        piel_r = any(f["componente"] == "piel a rendering" for f in b["filas"])
        ok &= not (piel_v and piel_r)
    chk("T16 rutas exclusivas: carcasa-esqueleto vendida XOR CMS; cuello XOR CMS; piel venta XOR rendering", ok)

    # T17 hueso original y residuo post-CMS no se duplican
    ok = True
    for b in todos:
        hueso_pech = [f for f in b["filas"] if f["componente"] == "hueso" and f["etapa"] == "deshuese pechuga"]
        cms_pech = [f for f in b["filas"] if f["etapa"] == "CMS (hueso de pechuga)"]
        ok &= not (hueso_pech and cms_pech)
        for material, kg in b["cms_carcasa"]:
            salida = suma(b, lambda f, e=f"CMS ({material})": f["etapa"] == e)
            ok &= abs(salida - kg) <= TOL_KG_POR_AVE                 # CMS + residuo + merma = materia prima
        if b["config"] == "C" and b["rutas"]["hueso_pechuga"] == "cms":
            ok &= not hueso_pech and bool(cms_pech)
    chk("T17 hueso original y residuo óseo post-CMS no se duplican (CMS + residuo + merma = materia prima)", ok)

    # T18 un mismo kg no pertenece a dos categorías finales
    ok = True
    for b in todos:
        clase_de = {}
        for f in b["filas"]:
            ok &= clase_de.setdefault(f["componente"], f["clase"]) == f["clase"]
        ok &= abs(sum(v[0] for v in totales_por_clase(b).values()) - b["peso"]) <= TOL_KG_POR_AVE
    chk("T18 cada salida en una sola categoría final (Σ clases = PV)", ok)

    # T19 masa biológica cierra independientemente del agua
    ok = True
    for p in PESOS:
        for cfg in CONFIGS:
            b6, b8 = balance(p, cfg, enfriamiento="inmersion"), balance(p, cfg, enfriamiento="inmersion_limite")
            bio6 = {(f["etapa"], f["componente"], f["origen"]): f["bio"] for f in b6["filas"]}
            bio8 = {(f["etapa"], f["componente"], f["origen"]): f["bio"] for f in b8["filas"]}
            ok &= bio6.keys() == bio8.keys() and all(abs(bio6[k] - bio8[k]) < 1e-15 for k in bio6)
            ok &= abs(b6["salida_bio"] - p) <= TOL_KG_POR_AVE and abs(b8["salida_bio"] - p) <= TOL_KG_POR_AVE
    chk("T19 masa biológica idéntica con 6 % y 8 % de absorción (cierra sin depender del agua)", ok)

    # T20 el agua retenida nunca aumenta el rendimiento biológico
    ok = True
    for b in todos:
        comestible_bio = suma(b, lambda f: f["clase"] in "AB")
        ok &= comestible_bio <= b["peso"]
        ok &= b["carcasa_fria_bio"] <= b["carcasa_prechiller"] + 1e-15      # el chiller no suma masa biológica
    b_i, b_a = balance(2.9, "B", enfriamiento="inmersion"), balance(2.9, "B", enfriamiento="aire")
    ok &= suma(b_a, lambda f: f["clase"] in "AB") < suma(b_i, lambda f: f["clase"] in "AB")
    ok &= abs(suma(b_i, lambda f: f["clase"] in "AB") - suma(b_a, lambda f: f["clase"] in "AB")
              - b_a["evaporacion"] * (1 - CORTES[-1][1] / 100)) < 1e-12
    chk("T20 agua retenida no aumenta el rendimiento biológico (solo el peso comercial)", ok)

    # T21 reconciliación comestible: disponible − merma real − reclasificado a C = comestible
    ok = True
    for b in todos:
        r = reconciliacion_comestible(b)
        ok &= abs(r["cierre"]) <= TOL_KG_POR_AVE
    for cfg_rutas in [(p, rend, cond, enf) for p in PESOS for rend, cond, enf in VARIANTES]:
        disp = {cfg: reconciliacion_comestible(balance(*cfg_rutas[:1], cfg, *cfg_rutas[1:]))["disponible"] for cfg in CONFIGS}
        ok &= max(disp.values()) - min(disp.values()) <= TOL_KG_POR_AVE   # misma base para A, B y C
    chk("T21 misma masa comestible disponible en A/B/C y reconciliación cierra", ok)

    if verbose:
        print(f"\nTESTS AUTOMÁTICOS — modelo_balance_masa.py v{VERSION}")
        for nombre, r, d in resultados:
            print(f"  [{'OK ' if r else 'FALLA'}] {nombre}" + (f"  ({d})" if d and (not r or 'error máx' in d) else ""))
        print(f"  Resultado: {sum(r for _, r, _ in resultados)}/{len(resultados)} correctos\n")
    return resultados


# ---------------------------------------------------------------------------
# 14. SALIDAS
# ---------------------------------------------------------------------------
CAMPOS_CSV = ["escenario_id", "clasificacion", "peso_vivo_kg", "configuracion", "escenario_rendimiento",
              "escenario_condenas", "enfriamiento", "ruta_esqueleto", "ruta_cuello", "ruta_hueso_pechuga",
              "ruta_piel", "etapa", "componente", "origen", "clase", "destino_conceptual",
              "masa_biologica_kg_ave", "agua_kg_ave", "total_kg_ave", "pct_peso_vivo_bio", "pct_carcasa_bio",
              "kg_1000_aves", "t_dia_2500_aves_dia", "t_dia_5000_aves_dia", "t_dia_10000_aves_dia",
              "t_dia_20000_aves_dia", "t_anio_2500_aves_dia", "t_anio_5000_aves_dia", "t_anio_10000_aves_dia",
              "t_anio_20000_aves_dia", "t_anio_1M_aves_anio", "t_dia_1M_aves_anio"]


def escribir_csv(ruta_csv: str) -> int:
    n = 0
    with open(ruta_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_CSV)
        w.writeheader()
        for i, b in enumerate(grilla(), start=1):
            verificar_cierre(b)
            base = {"escenario_id": f"BAL-{i:03d}", "clasificacion": "ESCENARIO [ESTIMACION] (no diseño)",
                    "peso_vivo_kg": b["peso"], "configuracion": f"{b['config']} {NOMBRE_CONFIG[b['config']]}",
                    "escenario_rendimiento": b["rendimiento"], "escenario_condenas": b["condenas"],
                    "enfriamiento": b["enfriamiento"], "ruta_esqueleto": b["rutas"]["esqueleto"],
                    "ruta_cuello": b["rutas"]["cuello"], "ruta_hueso_pechuga": b["rutas"]["hueso_pechuga"],
                    "ruta_piel": b["rutas"]["piel"]}
            for f in (x for x in b["filas"] if x["bio"] + x["agua"] > 0):
                tot = f["bio"] + f["agua"]
                r = dict(base, etapa=f["etapa"], componente=f["componente"], origen=f["origen"],
                         clase=f["clase"], destino_conceptual=f["destino"],
                         masa_biologica_kg_ave=round(f["bio"], 6), agua_kg_ave=round(f["agua"], 6),
                         total_kg_ave=round(tot, 6), pct_peso_vivo_bio=round(f["bio"] / b["peso"] * 100, 4),
                         pct_carcasa_bio=(round(f["bio"] / b["carcasa_bio"] * 100, 4)
                                          if f["deriva_de_carcasa"] else ""))
                r.update({k: round(v, 6) for k, v in escalas(tot).items()})
                w.writerow(r)
                n += 1
            controles = (
                ("CONTROL masa biológica: entrada (peso vivo)", b["entrada_bio"]),
                ("CONTROL masa biológica: salidas", b["salida_bio"]),
                ("CONTROL agua incorporada a productos y subproductos: entrada (NO es consumo de agua de la planta)", b["entrada_agua"]),
                ("CONTROL   de la cual: agua absorbida por la carcasa en el chiller", b["agua_absorbida_chiller"]),
                ("CONTROL     de la cual: agua retenida en producto (vendida)", b["agua_retenida_producto"]),
                ("CONTROL     de la cual: agua de goteo del producto", b["agua_goteo_producto"]),
                ("CONTROL   de la cual: agua adherida a plumas", b["agua_adherida_plumas"]),
                ("CONTROL agua incorporada: salidas", b["salida_agua"]),
                ("CONTROL error de cierre total", b["error_kg"]))
            for comp, val in controles:
                r = dict(base, etapa="control", componente=comp, origen="", clase="CONTROL",
                         destino_conceptual="", masa_biologica_kg_ave="", agua_kg_ave="",
                         total_kg_ave=f"{val:.9f}", pct_peso_vivo_bio="", pct_carcasa_bio="")
                r.update({k: round(v, 6) for k, v in escalas(val).items()})
                w.writerow(r)
                n += 1
    return n


def imprimir_balance(b: dict, aves_dia: int | None = None) -> None:
    print(f"\nBALANCE — PV {b['peso']} kg | config {b['config']} ({NOMBRE_CONFIG[b['config']]}) | "
          f"rendimiento {b['rendimiento']} | condenas {b['condenas']} | enfriamiento {b['enfriamiento']} | rutas {b['rutas']}")
    print(f"{'clase':5} {'componente':38} {'bio kg':>8} {'agua kg':>8} {'total kg':>9} {'%PV bio':>8}"
          + (f" {'t/día':>8}" if aves_dia else ""))
    for (clase, comp), (bio, agua) in sorted(agregar(b).items()):
        if bio + agua <= 0:
            continue
        linea = f"{clase:5} {comp:38} {bio:8.4f} {agua:8.4f} {bio + agua:9.4f} {bio / b['peso'] * 100:8.2f}"
        if aves_dia:
            linea += f" {(bio + agua) * aves_dia / 1000:8.3f}"
        print(linea)
    print(f"MASA BIOLÓGICA: entrada {b['entrada_bio']:.4f} kg = salidas {b['salida_bio']:.4f} kg")
    print(f"AGUA INCORPORADA A PRODUCTOS Y SUBPRODUCTOS (no es consumo de agua de planta): "
          f"entrada {b['entrada_agua']:.4f} = salidas {b['salida_agua']:.4f} kg")
    print(f"ERROR DE CIERRE: {b['error_kg']:.2e} kg/ave (tolerancia {TOL_KG_POR_AVE:.0e})")


def imprimir_auditoria(b: dict) -> None:
    """Tabla biológica manual y tabla de agua, separadas (nunca mezcladas)."""
    m, ft = b["primarios"], CONDENAS[b["condenas"]]["total"]
    dec = suma(b, lambda f: f["componente"].startswith("decomiso"))
    garras = suma(b, lambda f: f["origen"] == "patas" and f["componente"] != "decomiso total")
    no_com = m["tracto_digestivo"] + m["pulmones"] + m["otros_no_comestibles"]
    t1 = [("Carcasa apta (eviscerada, después de decomisos)", b["carcasa_apta"]),
          ("Cuello (apto)", m["cuello"] * (1 - ft)), ("Hígado (apto)", m["higado"] * (1 - ft)),
          ("Corazón (apto)", m["corazon"] * (1 - ft)), ("Molleja (apta)", m["molleja"] * (1 - ft)),
          ("Patas (aptas, antes de acondicionar)", garras), ("Sangre", m["sangre"]),
          ("Plumas (masa biológica)", m["plumas"]), ("Cabeza", m["cabeza"]),
          ("Vísceras no comestibles (tracto, pulmones, otros)", no_com),
          ("Contenido intestinal", m["contenido_gi"]), ("Decomisos (total + parcial)", dec),
          ("Pérdidas no asignadas", m["perdidas_no_asignadas"])]
    print(f"\nTABLA 1 — MASA BIOLÓGICA (PV {b['peso']} kg, {b['rendimiento']}, condenas {b['condenas']})")
    for k, v in t1:
        print(f"  {k:52} {v:8.4f} kg  {v / b['peso'] * 100:6.2f} %")
    tot = sum(v for _, v in t1)
    print(f"  {'TOTAL SALIDAS BIOLÓGICAS':52} {tot:8.4f} kg  (error {b['peso'] - tot:.1e})")
    print(f"\nTABLA 2 — AGUA INCORPORADA Y PESO COMERCIAL ({b['enfriamiento']}) — no es consumo de agua de planta")
    for k, v in (("Carcasa pre-chiller (masa biológica)", b["carcasa_prechiller"]),
                 ("Evaporación (aire)", -b["evaporacion"]),
                 ("Agua absorbida por la carcasa en el chiller", b["agua_absorbida_chiller"]),
                 ("Agua de goteo del producto (antes de la venta)", -b["agua_goteo_producto"]),
                 ("Agua retenida en producto (vendida)", b["agua_retenida_producto"]),
                 ("Peso comercial de la carcasa (bio + agua retenida)", b["carcasa_fria_bio"] + b["agua_retenida_producto"]),
                 ("Agua adherida a plumas (sale con la pluma húmeda)", b["agua_adherida_plumas"])):
        print(f"  {k:52} {v:8.4f} kg")


def main():
    ap = argparse.ArgumentParser(description="Balance de masa de pollo parrillero (Fase 0, escenarios)")
    ap.add_argument("--peso", type=float, help="peso vivo en planta, kg (2,0-3,8)")
    ap.add_argument("--config", choices=CONFIGS, default="B")
    ap.add_argument("--rendimiento", choices=list(AJUSTE_RENDIMIENTO), default="medio")
    ap.add_argument("--condenas", choices=list(CONDENAS), default="medio")
    ap.add_argument("--enfriamiento", choices=list(ENFRIAMIENTO), default="inmersion")
    for k, ops in OPCIONES_RUTA.items():
        ap.add_argument(f"--ruta-{k.replace('_', '-')}", choices=ops, default=None)
    ap.add_argument("--aves-dia", type=int, default=None)
    ap.add_argument("--auditoria", action="store_true", help="imprime tablas de auditoría manual")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--csv", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "escenarios_balance.csv"))
    a = ap.parse_args()

    res = ejecutar_tests()
    if not all(r for _, r, _ in res):
        print("DETENIDO: al menos una prueba falló. No se generan salidas.")
        sys.exit(1)
    if a.solo_tests:
        return
    try:
        if a.peso is not None:
            rutas = {k: getattr(a, f"ruta_{k}") for k in OPCIONES_RUTA if getattr(a, f"ruta_{k}")}
            b = balance(a.peso, a.config, a.rendimiento, a.condenas, a.enfriamiento, rutas)
            verificar_cierre(b)
            imprimir_balance(b, a.aves_dia)
            if a.auditoria:
                imprimir_auditoria(b)
            return
        n = escribir_csv(a.csv)
    except ErrorBalance as e:
        print(f"DETENIDO: {e}")
        sys.exit(1)
    print(f"CSV generado: {a.csv} ({n} filas)")
    for cfg in CONFIGS:
        imprimir_balance(balance(2.9, cfg), 10000)


if __name__ == "__main__":
    main()
