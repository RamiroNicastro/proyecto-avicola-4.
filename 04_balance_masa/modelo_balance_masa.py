#!/usr/bin/env python3
"""
Modelo de BALANCE DE MASA del pollo parrillero — versión 1.0 (2026-09-30)
==========================================================================

Pregunta: si entran X kg de pollo vivo, ¿dónde termina cada kilogramo?

Fase 0 (prefactibilidad). ESCENARIOS, no diseño. Sin precios, sin maquinaria,
sin capacidad fijada (reglas 7-9 de CLAUDE.md).

Uso
---
    python3 modelo_balance_masa.py                  # tests + CSV + resumen
    python3 modelo_balance_masa.py --solo-tests     # solo pruebas automáticas
    python3 modelo_balance_masa.py --peso 3.1 --config C --rendimiento alto \
        --condenas bajo --enfriamiento aire --aves-dia 8000   # un balance a medida

El script se DETIENE (código de salida 1) si alguna prueba falla o si algún
balance no cierra dentro de la tolerancia (TOL_KG_POR_AVE).

Unidad base y límites del sistema
---------------------------------
* Unidad: 1 POLLO VIVO recibido en planta (después de ayuno y transporte).
  La merma de peso en ayuno/transporte y las aves muertas en transporte (DOA)
  quedan FUERA del balance (ver 03_produccion_primaria; SUP-035).
* Toda masa se expresa en kg. Porcentajes en fracción (0-1) dentro del código.
* Se separan dos flujos que nunca se mezclan:
    - MASA BIOLÓGICA (tejidos del ave): entra solo con el peso vivo.
    - AGUA INCORPORADA en el proceso (chiller por inmersión, agua arrastrada
      por las plumas): entra aparte y sale aparte.
  Peso comercial = masa biológica + agua retenida.  El agua NO es carne.

Ecuación de balance (se verifica para cada escenario)
------------------------------------------------------
    PV + AGUA_INCORPORADA = PRODUCTOS(A) + COPRODUCTOS(B) + SUBPRODUCTOS(C)
                            + RESIDUOS/EFLUENTES(D) + PÉRDIDAS(P)
    con, por separado:  Σ masa biológica = PV   y   Σ agua = AGUA_INCORPORADA

Clases de salida
----------------
    A  producto principal       (ave entera, pechuga, pata-muslo y derivados)
    B  coproducto comestible    (alas, menudencias, cuello, garras, carcasa,
                                 piel, recortes, CMS)
    C  subproducto valorizable  (sangre recuperada, plumas, cabezas, vísceras no
                                 comestibles, huesos, grasa retirada, garras de
                                 descarte) -> rendering u otro uso permitido
    D  residuo / efluente       (contenido gastrointestinal, sangre no
                                 recuperada, cutícula de patas, agua de goteo,
                                 decomisos*)
    P  pérdida                  (evaporación, mermas de trozado/deshuese,
                                 pérdidas no asignadas)
    * Los decomisos se tratan como D; si la normativa permite enviarlos a
      rendering pasarían a C (DPV-066).

Método de dependencia con el peso vivo (no lineal)
--------------------------------------------------
    fracción_i(PV) = fracción_i(2,9 kg) + pendiente_i × (PV − 2,9)   [en % del PV]
    kg_i = PV × fracción_i(PV)   -> cuadrático en PV: una parte con pendiente
    positiva (carcasa, pechuga) crece MÁS que proporcionalmente; cabeza, patas,
    vísceras crecen MENOS. Válido solo entre 2,0 y 3,8 kg (no extrapolar).
    Dirección de las pendientes: literatura de alometría [PVDP]; magnitud:
    [SUPUESTO] calibrado para que las pérdidas no asignadas no varíen con el
    peso (no hay evidencia de que lo hagan). SUP-036.

Todas las cifras son [ESTIMACIÓN]/[SUPUESTO] construidas con rangos de fuentes
[PVDP] (FTE-140, FTE-142, FTE-161 a FTE-184). Detalle y fuentes por parámetro:
balance_por_ave.md, rendimientos_cortes.md, subproductos_masa.md,
agua_y_mermas.md. Supuestos registrados: SUP-035 a SUP-044.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict

VERSION = "1.0"
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
    # con piel, con grasa abdominal y riñones (definición D4 de balance_por_ave.md)
    ("carcasa",               71.5, +1.90),
    ("sangre",                 3.4, -0.10),   # sangre total drenada en el desangrado
    ("plumas",                 5.2, -0.20),   # masa biológica de plumas (sin agua de escaldado)
    ("cabeza",                 2.5, -0.30),
    ("patas",                  3.9, -0.30),   # pata cortada en la articulación del tarso (crudas)
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
# 3. TROZADO — fracción de la carcasa (base carcasa), a 2,9 kg, escenario medio
# ---------------------------------------------------------------------------
CORTES = [
    ("pechuga_con_hueso",  38.5, +1.20),   # pechuga entera con piel y hueso
    ("pata_muslo",         31.0, -0.40),   # cuarto trasero sin espinazo
    ("alas",               10.2, -0.50),   # ala entera (3 segmentos)
    ("carcasa_esqueleto",  19.3, -0.30),   # espinazo, rabadilla y costillar remanente
    ("recortes_trozado",    0.5,  0.00),   # recortes comestibles
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
CMS_RENDIMIENTO = {"bajo": 0.55, "medio": 0.60, "alto": 0.65}   # CMS / carcasa_esqueleto
CMS_MERMA = 0.01

# ---------------------------------------------------------------------------
# 5. SUBPRODUCTOS
# ---------------------------------------------------------------------------
SANGRE_RECUPERADA = 0.85          # fracción de la sangre drenada que llega al tanque de sangre
AGUA_ARRASTRE_PLUMAS = 0.60       # kg de agua por kg de pluma biológica (pluma cruda húmeda)
CUTICULA_PATAS = 0.05             # fracción de la pata removida en escaldado/pelado

# ---------------------------------------------------------------------------
# 6. CONDENAS Y MERMAS — escenarios (bajo = pocos problemas)
# ---------------------------------------------------------------------------
CONDENAS = {
    #        decomiso total   decomiso parcial   canales no aptas     garras: grado A / 2.ª / descarte
    #        (fracción aves)  (fracción carcasa) para entero (fr.)
    "bajo":  {"total": 0.004, "parcial": 0.003, "degradadas": 0.03, "garras": (0.90, 0.08, 0.02)},
    "medio": {"total": 0.010, "parcial": 0.008, "degradadas": 0.06, "garras": (0.80, 0.15, 0.05)},
    "alto":  {"total": 0.027, "parcial": 0.015, "degradadas": 0.12, "garras": (0.60, 0.25, 0.15)},
}

# ---------------------------------------------------------------------------
# 7. ENFRIAMIENTO (CHILLER) — agua incorporada / evaporación
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
HUESO_PECHUGA_A_CMS = False       # en config. C el hueso de pechuga va a rendering, no a CMS

# ---------------------------------------------------------------------------
# 8. BANDAS DE PLAUSIBILIDAD (para tests; % del PV salvo indicación) — rangos de fuentes [PVDP]
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
# 9. DESCRIPCIÓN DE CADA SALIDA (clase, destino conceptual)
# ---------------------------------------------------------------------------
DESTINO = {
    "sangre recuperada": ("C", "rendering (harina de sangre) / tratamiento; separada del efluente"),
    "sangre no recuperada": ("D", "efluente (alta DBO/DQO)"),
    "plumas crudas": ("C", "hidrólisis -> harina de plumas (rendering propio o tercero)"),
    "cabeza": ("C", "rendering"),
    "cuticula de patas": ("D", "efluente / lodos (o rendering)"),
    "garras grado A": ("B", "coproducto comestible (mercado interno / exportación potencial)"),
    "garras de segunda": ("B", "coproducto comestible de menor grado"),
    "garras descarte": ("C", "rendering"),
    "higado": ("B", "menudencia"), "corazon": ("B", "menudencia"), "molleja": ("B", "menudencia"),
    "cuello": ("B", "coproducto comestible (menudencia / CMS)"),
    "tracto digestivo": ("C", "rendering (harina de vísceras)"),
    "contenido gastrointestinal": ("D", "residuo sólido / efluente (tratamiento)"),
    "pulmones": ("C", "rendering"),
    "otros no comestibles": ("C", "rendering"),
    "decomiso total": ("D", "decomiso: destino según normativa (rendering o eliminación)"),
    "decomiso parcial": ("D", "decomiso: destino según normativa (rendering o eliminación)"),
    "grasa abdominal retirada": ("C", "grasa / rendering"),
    "evaporacion en enfriamiento": ("P", "vapor (pérdida de humedad del tejido)"),
    "agua de goteo": ("D", "agua (purga) -> efluente"),
    "pollo entero": ("A", "producto principal"),
    "pechuga con hueso": ("A", "producto principal"),
    "pata-muslo": ("A", "producto principal"),
    "alas": ("B", "coproducto comestible (corte secundario)"),
    "carcasa-esqueleto": ("B", "coproducto comestible (sopa / CMS)"),
    "recortes": ("B", "coproducto comestible (elaborados / CMS)"),
    "merma de trozado": ("P", "pérdida de proceso (aserrín, exudado) -> efluente"),
    "suprema": ("A", "producto principal"), "solomillo": ("A", "producto principal"),
    "muslo deshuesado": ("A", "producto principal"), "pata con hueso": ("A", "producto principal"),
    "pata deshuesada": ("A", "producto principal"),
    "piel": ("B", "coproducto comestible (elaborados) o rendering"),
    "hueso": ("C", "rendering (harina de carne y hueso) / caldos"),
    "merma de deshuese": ("P", "pérdida de proceso -> efluente"),
    "CMS": ("B", "coproducto comestible (industria de elaborados)"),
    "residuo oseo de CMS": ("C", "rendering"),
    "merma de CMS": ("P", "pérdida de proceso"),
    "perdidas no asignadas": ("P", "humedad, tejidos al efluente, no identificado (a medir en planta)"),
}


class ErrorBalance(Exception):
    """Error de balance o de parámetros: detiene el modelo."""


# ---------------------------------------------------------------------------
# 10. CÁLCULO
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
    """Fracciones de la carcasa (0-1) asignadas a cada corte de trozado."""
    aj = AJUSTE_CORTES[rendimiento]
    fr = {c: (ref + aj.get(c, 0.0) + pend * (peso - PESO_REF)) / 100.0 for c, ref, pend in CORTES}
    return fr


def fraccion_grasa(peso: float) -> float:
    return (GRASA_ABDOMINAL[0] + GRASA_ABDOMINAL[1] * (peso - PESO_REF)) / 100.0


def balance(peso: float, config: str = "B", rendimiento: str = "medio",
            condenas: str = "medio", enfriamiento: str = "inmersion") -> dict:
    """Balance de masa de UN ave. Devuelve dict con filas, entradas y controles."""
    if config not in CONFIGS:
        raise ErrorBalance(f"Configuración desconocida: {config}")
    fr = fracciones_primarias(peso, rendimiento)
    m = {k: v * peso for k, v in fr.items()}            # kg biológicos por componente primario
    cnd = CONDENAS[condenas]
    enf = ENFRIAMIENTO[enfriamiento]
    ft, fp = cnd["total"], cnd["parcial"]
    filas = []

    def fila(etapa, componente, origen, bio, agua=0.0, pct_carcasa=True):
        clase, destino = DESTINO[componente]
        filas.append({"etapa": etapa, "componente": componente, "origen": origen, "clase": clase,
                      "destino": destino, "bio": bio, "agua": agua,
                      "deriva_de_carcasa": origen == "carcasa" and pct_carcasa})

    # --- Sangre, plumas, cabeza ------------------------------------------------
    fila("faena", "sangre recuperada", "sangre", m["sangre"] * SANGRE_RECUPERADA)
    fila("faena", "sangre no recuperada", "sangre", m["sangre"] * (1 - SANGRE_RECUPERADA))
    agua_plumas = m["plumas"] * AGUA_ARRASTRE_PLUMAS
    fila("faena", "plumas crudas", "plumas", m["plumas"], agua_plumas)
    fila("faena", "cabeza", "cabeza", m["cabeza"])

    # --- Patas / garras --------------------------------------------------------
    patas_ok = m["patas"] * (1 - ft)
    fila("condenas", "decomiso total", "patas", m["patas"] * ft)
    fila("faena", "cuticula de patas", "patas", patas_ok * CUTICULA_PATAS)
    limpias = patas_ok * (1 - CUTICULA_PATAS)
    qa, q2, qd = cnd["garras"]
    fila("faena", "garras grado A", "patas", limpias * qa)
    fila("faena", "garras de segunda", "patas", limpias * q2)
    fila("faena", "garras descarte", "patas", limpias * qd)

    # --- Menudencias y cuello --------------------------------------------------
    for clave, nombre in (("higado", "higado"), ("corazon", "corazon"),
                          ("molleja", "molleja"), ("cuello", "cuello")):
        fila("condenas", "decomiso total", clave, m[clave] * ft)
        fila("faena", nombre, clave, m[clave] * (1 - ft))

    # --- Vísceras no comestibles ----------------------------------------------
    fila("faena", "tracto digestivo", "tracto_digestivo", m["tracto_digestivo"])
    fila("faena", "contenido gastrointestinal", "contenido_gi", m["contenido_gi"])
    fila("faena", "pulmones", "pulmones", m["pulmones"])
    fila("faena", "otros no comestibles", "otros_no_comestibles", m["otros_no_comestibles"])
    fila("faena", "perdidas no asignadas", "perdidas_no_asignadas", m["perdidas_no_asignadas"])

    # --- Carcasa: condenas, grasa, enfriamiento --------------------------------
    carc = m["carcasa"]
    fila("condenas", "decomiso total", "carcasa", carc * ft, pct_carcasa=False)
    c1 = carc * (1 - ft)
    fila("condenas", "decomiso parcial", "carcasa", c1 * fp, pct_carcasa=False)
    c1 *= (1 - fp)
    grasa = fraccion_grasa(peso) * peso * (1 - ft) * (1 - fp) * FRACCION_GRASA_RETIRADA
    fila("faena", "grasa abdominal retirada", "carcasa", grasa)
    c2 = c1 - grasa                                     # carcasa pre-chiller (biológica)
    evap = c2 * enf["evaporacion"]
    fila("enfriamiento", "evaporacion en enfriamiento", "carcasa", evap, pct_carcasa=False)
    c3 = c2 - evap                                      # carcasa fría, masa biológica
    agua_abs = c2 * enf["absorcion"]                    # agua absorbida en el chiller
    agua_goteo = agua_abs * enf["goteo"]
    agua_ret = agua_abs - agua_goteo                    # agua que queda en el producto vendido
    filas.append({"etapa": "enfriamiento", "componente": "agua de goteo", "origen": "agua_proceso",
                  "clase": "D", "destino": DESTINO["agua de goteo"][1], "bio": 0.0,
                  "agua": agua_goteo, "deriva_de_carcasa": False})

    # --- Asignación comercial de la carcasa fría (c3) --------------------------
    fc = fracciones_cortes(peso, rendimiento)
    destino_carcasa = []                                # (etapa, componente, kg bio)

    def trozar(masa, etapa):
        destino_carcasa.append((etapa, "pechuga con hueso", masa * fc["pechuga_con_hueso"]))
        destino_carcasa.append((etapa, "pata-muslo", masa * fc["pata_muslo"]))
        destino_carcasa.append((etapa, "alas", masa * fc["alas"]))
        destino_carcasa.append((etapa, "carcasa-esqueleto", masa * fc["carcasa_esqueleto"]))
        destino_carcasa.append((etapa, "recortes", masa * fc["recortes_trozado"]))
        destino_carcasa.append((etapa, "merma de trozado", masa * fc["merma_trozado"]))

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
        esq = c3 * fc["carcasa_esqueleto"]
        d = DESHUESE["pechuga_con_hueso"]
        destino_carcasa += [("deshuese pechuga", "suprema", pech * d["suprema"]),
                            ("deshuese pechuga", "solomillo", pech * d["solomillo"]),
                            ("deshuese pechuga", "piel", pech * d["piel"]),
                            ("deshuese pechuga", "recortes", pech * d["recortes"]),
                            ("deshuese pechuga", "merma de deshuese", pech * d["merma"])]
        hueso_pech = pech * d["hueso"]
        d = DESHUESE["muslo"]
        destino_carcasa += [("deshuese muslo", "muslo deshuesado", muslo * d["carne"]),
                            ("deshuese muslo", "piel", muslo * d["piel"]),
                            ("deshuese muslo", "hueso", muslo * d["hueso"]),
                            ("deshuese muslo", "recortes", muslo * d["recortes"]),
                            ("deshuese muslo", "merma de deshuese", muslo * d["merma"])]
        if DESHUESAR_PATA:
            d = DESHUESE["pata"]
            destino_carcasa += [("deshuese pata", "pata deshuesada", pata * d["carne"]),
                                ("deshuese pata", "piel", pata * d["piel"]),
                                ("deshuese pata", "hueso", pata * d["hueso"]),
                                ("deshuese pata", "recortes", pata * d["recortes"]),
                                ("deshuese pata", "merma de deshuese", pata * d["merma"])]
        else:
            destino_carcasa.append(("trozado", "pata con hueso", pata))
        destino_carcasa.append(("trozado", "alas", c3 * fc["alas"]))
        destino_carcasa.append(("trozado", "recortes", c3 * fc["recortes_trozado"]))
        destino_carcasa.append(("trozado", "merma de trozado", c3 * fc["merma_trozado"]))
        ent_cms = esq + (hueso_pech if HUESO_PECHUGA_A_CMS else 0.0)
        if not HUESO_PECHUGA_A_CMS:
            destino_carcasa.append(("deshuese pechuga", "hueso", hueso_pech))
        r = CMS_RENDIMIENTO[rendimiento]
        destino_carcasa += [("CMS", "CMS", ent_cms * r),
                            ("CMS", "residuo oseo de CMS", ent_cms * (1 - r - CMS_MERMA)),
                            ("CMS", "merma de CMS", ent_cms * CMS_MERMA)]

    # Agua retenida: se reparte proporcionalmente a la masa biológica de las salidas
    # de la carcasa que no son pérdidas (clase P no retiene agua).
    base_agua = sum(kg for _, comp, kg in destino_carcasa if DESTINO[comp][0] != "P")
    for etapa, comp, kg in destino_carcasa:
        agua = agua_ret * kg / base_agua if (DESTINO[comp][0] != "P" and base_agua > 0) else 0.0
        fila(etapa, comp, "carcasa", kg, agua)

    entradas_agua = agua_plumas + agua_abs
    salida_bio = sum(f["bio"] for f in filas)
    salida_agua = sum(f["agua"] for f in filas)
    return {
        "peso": peso, "config": config, "rendimiento": rendimiento, "condenas": condenas,
        "enfriamiento": enfriamiento, "filas": filas, "primarios": m, "fracciones": fr,
        "cortes": fc, "carcasa_bio": carc, "carcasa_fria_bio": c3, "carcasa_prechiller": c2,
        "agua_absorbida": agua_abs, "agua_retenida": agua_ret, "agua_plumas": agua_plumas,
        "entrada_bio": peso, "entrada_agua": entradas_agua,
        "salida_bio": salida_bio, "salida_agua": salida_agua,
        "error_kg": (peso + entradas_agua) - (salida_bio + salida_agua),
    }


def verificar_cierre(b: dict, factor: float = 1.0) -> None:
    """Detiene el modelo si el balance no cierra dentro de la tolerancia."""
    tol = TOL_KG_POR_AVE * factor
    if abs(b["error_kg"]) * factor > tol:
        raise ErrorBalance(f"Balance no cierra: error {b['error_kg']:.3e} kg/ave ({b['config']}, {b['peso']} kg)")
    if abs(b["salida_bio"] - b["entrada_bio"]) * factor > tol:
        raise ErrorBalance("Masa biológica no cierra")
    if abs(b["salida_agua"] - b["entrada_agua"]) * factor > tol:
        raise ErrorBalance("Agua no cierra")


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


# ---------------------------------------------------------------------------
# 11. GRILLA DE ESCENARIOS
# ---------------------------------------------------------------------------
def grilla():
    """Combinaciones generadas: 6 pesos × 3 configuraciones × 7 variantes = 126 balances."""
    variantes = [("bajo", "medio", "inmersion"), ("medio", "medio", "inmersion"),
                 ("alto", "medio", "inmersion"), ("medio", "bajo", "inmersion"),
                 ("medio", "alto", "inmersion"), ("medio", "medio", "inmersion_limite"),
                 ("medio", "medio", "aire")]
    for peso in PESOS:
        for cfg in CONFIGS:
            for rend, cond, enf in variantes:
                yield balance(peso, cfg, rend, cond, enf)


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
# 12. TESTS AUTOMÁTICOS
# ---------------------------------------------------------------------------
def ejecutar_tests(verbose: bool = True) -> list:
    resultados = []

    def chk(nombre, cond, detalle=""):
        resultados.append((nombre, bool(cond), detalle))

    balances = list(grilla())
    # T01 cierre por ave (total, biológico y agua por separado)
    errs = []
    for b in balances:
        try:
            verificar_cierre(b)
        except ErrorBalance as e:
            errs.append(str(e))
    chk("T01 cierre por ave (126 balances; total, masa biológica y agua)", not errs,
        f"error máx = {max(abs(b['error_kg']) for b in balances):.2e} kg/ave; tolerancia {TOL_KG_POR_AVE:.0e}")

    # T02 cierre por 1.000 aves
    ok = True
    for b in balances:
        e_1000 = (b["entrada_bio"] + b["entrada_agua"]) * 1000 - sum((f["bio"] + f["agua"]) * 1000 for f in b["filas"])
        ok &= abs(e_1000) <= TOL_KG_POR_AVE * 1000
    chk("T02 cierre por 1.000 aves", ok, f"tolerancia {TOL_KG_POR_AVE * 1000:.0e} kg por 1.000 aves")

    # T03 ningún componente negativo
    neg = [(b["peso"], b["config"], f["componente"]) for b in balances for f in b["filas"]
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
        # agua retenida en el producto comercial <= límite
        if b["carcasa_fria_bio"] > 0:
            frac_agua = b["agua_retenida"] / (b["carcasa_fria_bio"] + b["agua_retenida"])
            if frac_agua > LIMITE_AGUA_RETENIDA + 1e-12:
                fuera.append((b["peso"], b["enfriamiento"], "agua_retenida", round(frac_agua * 100, 2)))
    chk("T04 porcentajes dentro de bandas de fuentes", not fuera, str(fuera[:5]))

    # T05 suma de cortes <= carcasa (y = carcasa fría asignada)
    ok, det = True, ""
    for b in balances:
        cortes = sum(f["bio"] for f in b["filas"] if f["origen"] == "carcasa" and f["etapa"] not in ("condenas", "enfriamiento", "faena"))
        ok &= cortes <= b["carcasa_bio"] + 1e-12 and abs(cortes - b["carcasa_fria_bio"]) <= TOL_KG_POR_AVE
    chk("T05 suma de cortes <= carcasa (igual a la carcasa fría asignada)", ok)

    # T06 suma de deshuesados <= cortes de origen; fracciones de deshuese suman 1
    ok = all(abs(sum(v.values()) - 1) < 1e-12 for v in DESHUESE.values())
    for b in (x for x in balances if x["config"] == "C"):
        c3, fc = b["carcasa_fria_bio"], b["cortes"]
        pech = sum(f["bio"] for f in b["filas"] if f["etapa"] == "deshuese pechuga")
        mus = sum(f["bio"] for f in b["filas"] if f["etapa"] == "deshuese muslo")
        ok &= pech <= c3 * fc["pechuga_con_hueso"] + 1e-12
        ok &= mus <= c3 * fc["pata_muslo"] * FRACCION_MUSLO_EN_PATA_MUSLO + 1e-12
        carne = sum(f["bio"] for f in b["filas"] if f["componente"] in ("suprema", "solomillo", "muslo deshuesado"))
        ok &= carne < pech + mus
    chk("T06 suma de deshuesados <= cortes de origen", ok)

    # T07 escalado lineal
    ok = True
    b = balance(2.9)
    for f in b["filas"]:
        kg = f["bio"] + f["agua"]
        e = escalas(kg)
        ok &= abs(e["kg_1000_aves"] - 1000 * kg) < 1e-9
        for n in AVES_DIA:
            ok &= abs(e[f"t_anio_{n}_aves_dia"] - e[f"t_dia_{n}_aves_dia"] * DIAS_FAENA_ANIO) < 1e-9
        ok &= abs(e["t_dia_10000_aves_dia"] - 2 * e["t_dia_5000_aves_dia"]) < 1e-9
        ok &= abs(e["t_anio_1M_aves_anio"] - kg * 1000) < 1e-9
    chk("T07 escalado lineal (1 ave -> 1.000 aves -> t/día -> t/año)", ok)

    # T08 agua absorbida separada de la masa biológica
    ok = True
    for b in balances:
        ok &= abs(sum(f["bio"] for f in b["filas"]) - b["peso"]) <= TOL_KG_POR_AVE
        ok &= all(f["agua"] == 0.0 for f in b["filas"] if f["clase"] == "P")
        if b["enfriamiento"] == "aire":
            ok &= abs(b["agua_retenida"]) < 1e-15
            ok &= all(f["agua"] == 0 for f in b["filas"] if f["origen"] == "carcasa")
        agua_carc = sum(f["agua"] for f in b["filas"] if f["origen"] == "carcasa")
        ok &= abs(agua_carc - b["agua_retenida"]) <= TOL_KG_POR_AVE
    chk("T08 agua separada de masa biológica (Σ bio = PV; agua solo en columna agua)", ok)

    # T09 unidades y sumas de fracciones
    ok = True
    for b in balances:
        ok &= abs(sum(b["fracciones"].values()) - 1) < 1e-12
        ok &= abs(sum(b["cortes"].values()) - 1) < 1e-12
        ok &= abs(sum(b["primarios"].values()) - b["peso"]) < 1e-12
    ok &= all(0 <= v <= 1 for v in (SANGRE_RECUPERADA, CUTICULA_PATAS, FRACCION_GRASA_RETIRADA,
                                    FRACCION_MUSLO_EN_PATA_MUSLO))
    ok &= all(abs(sum(c["garras"]) - 1) < 1e-12 for c in CONDENAS.values())
    chk("T09 unidades consistentes (fracciones suman 1; kg primarios = PV)", ok)

    # T10 sin doble conteo: cada componente primario se asigna exactamente una vez
    ok, det = True, []
    for b in balances:
        por_origen = defaultdict(float)
        for f in b["filas"]:
            if f["origen"] != "agua_proceso":
                por_origen[f["origen"]] += f["bio"]
        for k, v in b["primarios"].items():
            if abs(por_origen[k] - v) > TOL_KG_POR_AVE:
                ok = False
                det.append((b["peso"], b["config"], k))
        claves = [(f["etapa"], f["componente"], f["origen"]) for f in b["filas"]]
        ok &= len(claves) == len(set(claves))
        # patas y menudencias nunca aparecen dentro del flujo de la carcasa
        ok &= not any(f["origen"] == "carcasa" and f["componente"] in
                      ("higado", "corazon", "molleja", "cuello", "garras grado A") for f in b["filas"])
    chk("T10 sin doble conteo (cada kg asignado a un solo destino)", ok, str(det[:3]))

    # T11 no linealidad con el peso (dirección de alometría)
    b1, b2 = balance(2.2), balance(3.5)
    pech = lambda b: sum(f["bio"] for f in b["filas"] if f["componente"] == "pechuga con hueso")
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
    ok = all(f["clase"] in "ABCDP" for b in balances for f in b["filas"])
    chk("T13 toda salida clasificada A/B/C/D/P", ok)

    if verbose:
        print(f"\nTESTS AUTOMÁTICOS — modelo_balance_masa.py v{VERSION}")
        for n, r, d in resultados:
            print(f"  [{'OK ' if r else 'FALLA'}] {n}" + (f"  ({d})" if d and (not r or 'error máx' in d) else ""))
        n_ok = sum(r for _, r, _ in resultados)
        print(f"  Resultado: {n_ok}/{len(resultados)} correctos\n")
    return resultados


# ---------------------------------------------------------------------------
# 13. SALIDAS
# ---------------------------------------------------------------------------
CAMPOS_CSV = ["escenario_id", "clasificacion", "peso_vivo_kg", "configuracion", "escenario_rendimiento",
              "escenario_condenas", "enfriamiento", "etapa", "componente", "origen", "clase", "destino_conceptual",
              "masa_biologica_kg_ave", "agua_kg_ave", "total_kg_ave", "pct_peso_vivo_bio", "pct_carcasa_bio",
              "kg_1000_aves", "t_dia_2500_aves_dia", "t_dia_5000_aves_dia", "t_dia_10000_aves_dia",
              "t_dia_20000_aves_dia", "t_anio_2500_aves_dia", "t_anio_5000_aves_dia", "t_anio_10000_aves_dia",
              "t_anio_20000_aves_dia", "t_anio_1M_aves_anio", "t_dia_1M_aves_anio"]


def escribir_csv(ruta: str) -> int:
    n = 0
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS_CSV)
        w.writeheader()
        for i, b in enumerate(grilla(), start=1):
            verificar_cierre(b)
            eid = f"BAL-{i:03d}"
            base = {"escenario_id": eid, "clasificacion": "ESCENARIO [ESTIMACION] (no diseño)",
                    "peso_vivo_kg": b["peso"], "configuracion": f"{b['config']} {NOMBRE_CONFIG[b['config']]}",
                    "escenario_rendimiento": b["rendimiento"], "escenario_condenas": b["condenas"],
                    "enfriamiento": b["enfriamiento"]}
            filas = [f for f in b["filas"] if f["bio"] + f["agua"] > 0]
            for f in filas:
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
            # filas de control del balance
            for comp, val in (("CONTROL entradas: peso vivo", b["entrada_bio"]),
                              ("CONTROL entradas: agua incorporada", b["entrada_agua"]),
                              ("CONTROL salidas: total", b["salida_bio"] + b["salida_agua"]),
                              ("CONTROL error de cierre", b["error_kg"])):
                r = dict(base, etapa="control", componente=comp, origen="", clase="CONTROL",
                         destino_conceptual="", masa_biologica_kg_ave="", agua_kg_ave="",
                         total_kg_ave=f"{val:.9f}", pct_peso_vivo_bio="", pct_carcasa_bio="")
                r.update({k: round(v, 6) for k, v in escalas(val).items()})
                w.writerow(r)
                n += 1
    return n


def imprimir_balance(b: dict, aves_dia: int | None = None) -> None:
    print(f"\nBALANCE — PV {b['peso']} kg | config {b['config']} ({NOMBRE_CONFIG[b['config']]}) | "
          f"rendimiento {b['rendimiento']} | condenas {b['condenas']} | enfriamiento {b['enfriamiento']}")
    print(f"{'clase':5} {'componente':32} {'bio kg':>8} {'agua kg':>8} {'total kg':>9} {'%PV bio':>8}"
          + (f" {'t/día':>8}" if aves_dia else ""))
    for (clase, comp), (bio, agua) in sorted(agregar(b).items()):
        if bio + agua <= 0:
            continue
        linea = f"{clase:5} {comp:32} {bio:8.4f} {agua:8.4f} {bio + agua:9.4f} {bio / b['peso'] * 100:8.2f}"
        if aves_dia:
            linea += f" {(bio + agua) * aves_dia / 1000:8.3f}"
        print(linea)
    print(f"ENTRADAS: PV {b['entrada_bio']:.4f} + agua {b['entrada_agua']:.4f} = {b['entrada_bio'] + b['entrada_agua']:.4f} kg")
    print(f"SALIDAS : bio {b['salida_bio']:.4f} + agua {b['salida_agua']:.4f} = {b['salida_bio'] + b['salida_agua']:.4f} kg")
    print(f"ERROR DE CIERRE: {b['error_kg']:.2e} kg/ave (tolerancia {TOL_KG_POR_AVE:.0e})")


def main():
    ap = argparse.ArgumentParser(description="Balance de masa de pollo parrillero (Fase 0, escenarios)")
    ap.add_argument("--peso", type=float, help="peso vivo en planta, kg (2,0-3,8)")
    ap.add_argument("--config", choices=CONFIGS, default="B")
    ap.add_argument("--rendimiento", choices=list(AJUSTE_RENDIMIENTO), default="medio")
    ap.add_argument("--condenas", choices=list(CONDENAS), default="medio")
    ap.add_argument("--enfriamiento", choices=list(ENFRIAMIENTO), default="inmersion")
    ap.add_argument("--aves-dia", type=int, default=None)
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
            b = balance(a.peso, a.config, a.rendimiento, a.condenas, a.enfriamiento)
            verificar_cierre(b)
            imprimir_balance(b, a.aves_dia)
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
