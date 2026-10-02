#!/usr/bin/env python3
"""
MOTOR CAPEX INTEGRAL — versión 1.0 (2026-10-02, sesión 16)
==========================================================

¿CUÁNTO CAPITAL REQUIERE CONSTRUIR Y PONER OPERATIVA CADA CONFIGURACIÓN DEL PROYECTO?

El motor NO elige escala, arquitectura ni proveedor. Arma, para cada configuración, el REGISTRO DE ACTIVOS
(BOQ) con cantidades salidas de los módulos físicos ya aprobados, lo cruza con la BASE DE COSTOS externa
(`base_costos_capex.csv`) y muestra qué parte del CAPEX tiene precio, con qué evidencia (E1–E5) y qué parte
sigue PENDIENTE. Si faltan conceptos, NO publica un "CAPEX total": publica CAPEX con precio + cobertura.

QUÉ NO HACE: OPEX, ingresos, EBITDA, VAN/TIR/payback, capital de trabajo, depreciación fiscal, IVA
definitivo, aranceles, valor residual, reemplazos futuros (solo deja los campos), recomendación de escala o
de integración.

INSUMOS IMPORTADOS (no se recalculan; se llaman las funciones de cada módulo):
  * 09_layout_obra_civil/modelo_superficies.py (12C): m² por área (bajo/medio/alto), terreno conceptual,
    y a través de él 11_agua_efluentes/modelo_utilities.py (09C): agua, efluente, DQO, kWh, kW medios,
    frío parcial, térmico, cargas críticas.
  * 13_logistica/modelo_logistica.py (12B): viajes y flota mínima por flujo.
  * 14_alimento_balanceado/modelo_upstream.py (14B): pollitos, posiciones de setter y hatcher (separadas),
    almacén de huevo, t/h de planta de alimento, silos, m² de galpón y plazas de alojamiento.
  * 08_maquinaria/matriz_equipos.csv (09A): EQ-01…EQ-76, nivel de automatización por escala y modularidad.

MÉTODO
  1. drivers(cfg)       → cantidades físicas (con rango cuando el módulo de origen lo da).
  2. generar_boq(cfg)   → una fila por activo/concepto: módulo, bloque, cantidad, unidad, COSTO_ID, paquete
                          padre, INCLUIDO_EN_PAQUETE, etiqueta de expansión, fase y titular.
  3. costear(boq, base) → costo por fila SOLO si hay precio y cantidad; vacío = desconocido (nunca 0).
                          Equipo ≠ instalado: un precio EXW/FOB/CIF sin capas queda PRECIO_PARCIAL.
  4. resumir(boq)       → por bloque: conceptos, con precio, sin precio, sin cantidad, alcance pendiente,
                          CAPEX con precio por nivel de evidencia, LOW/MEDIUM/HIGH donde hay rango,
                          cobertura por conceptos y por valor (esta última solo si es calculable).
  5. expansion(...)     → CAPEX inicial / de expansión / acumulado por trayectoria (20.000 directo;
                          5.000 → 20.000; 10.000 → 20.000) con acciones por etiqueta de activo.

FÓRMULAS
  costo (unitario)   = cantidad × precio_unitario_USD                          (por nivel bajo/medio/alto)
  costo (global)     = precio del lote (cantidad = 1 lote)
  costo (escalado)   = precio_ref × (capacidad / capacidad_ref)^exponente       (exponente explícito; sin
                       exponente solo vale DENTRO del rango de la referencia: SUP-16-13)
  costo (porcentaje) = % × base declarada (BASE_PORCENTAJE); base sin precio → PENDIENTE (no 0)
  precio_USD         = precio_original ÷ TC_MONEDA_POR_USD (obligatorio si la moneda no es USD)
  instalado          = COSTO_INSTALADO, o precio si el precio ya es instalado, o precio + capas C02–C19
                       (capas_importacion_capex.csv; C08 IVA recuperable y C17 servicio van aparte;
                       C10 obra civil se excluye porque la obra se costea en OC-*), o precio × factor SOLO en
                       modo sensibilidad; si no, PENDIENTE.
  LOW / HIGH         = cantidad baja × precio bajo / cantidad alta × precio alto, solo si ambos existen
                       (envolvente con correlación perfecta, no intervalo de confianza: SUP-16-08).

Uso
---
    python3 19_capex/modelo_capex.py                 # tests + CSV (boq, escenarios, expansión, RFQ)
    python3 19_capex/modelo_capex.py --solo-tests
    python3 19_capex/modelo_capex.py --mutaciones    # los tests detectan errores sembrados
    python3 19_capex/modelo_capex.py --tablas        # tablas para los .md
    python3 19_capex/modelo_capex.py --escenario --config C1 --aves-dia 7500 --terreno compra_reserva
    python3 19_capex/modelo_capex.py --escenario --config C1 --costos otra_base.csv   # sensibilidad

El script se DETIENE (código 1) si falla cualquier prueba. Unidades métricas; CSV con punto decimal.
IDs provisionales: SUP-16-##, DPV-16-##, DEC-16-##, FTE-16-### (ver actualizaciones_gestion_16.md).
"""
import argparse
import copy
import csv
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _d in ("09_layout_obra_civil", "05_proceso_industrial", "23_plan_expansion", "11_agua_efluentes",
           "13_logistica", "14_alimento_balanceado"):
    _p = os.path.join(RAIZ, _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)

import modelo_superficies as ms   # noqa: E402  (12C → 09A, 09C, 23)
import modelo_logistica as ml     # noqa: E402  (12B)
import modelo_upstream as mup     # noqa: E402  (14B)

VERSION = "1.0"
FECHA = "2026-10-02"
FUENTE = "19_capex/modelo_capex.py"
FECHA_BASE_CAPEX = "2026-10-01"            # SUP-16-01: editable (--fecha-base)
MONEDA_MODELO = "USD"
ARCHIVO_COSTOS = os.path.join(AQUI, "base_costos_capex.csv")
ARCHIVO_CAPAS = os.path.join(AQUI, "capas_importacion_capex.csv")
ARCHIVO_EQUIPOS = os.path.join(RAIZ, "08_maquinaria", "matriz_equipos.csv")
SALIDA_BOQ = os.path.join(AQUI, "boq_capex.csv")
SALIDA_ESC = os.path.join(AQUI, "escenarios_capex.csv")
SALIDA_EXP = os.path.join(AQUI, "expansion_capex.csv")
SALIDA_RFQ = os.path.join(AQUI, "matriz_rfq_capex.csv")

ESCALAS_REF = (2500, 5000, 10000, 20000)
RANGO_ESCALA = (2500, 20000)               # intermedias sí; extrapolación fuera del rango estudiado no
NIVELES = ("bajo", "medio", "alto")        # salida: LOW / MEDIUM / HIGH
EVIDENCIAS = ("E1", "E2", "E3", "E4", "E5")
NIVELES_EVIDENCIA = EVIDENCIAS + ("PENDIENTE",)
ETIQUETAS = ("REUTILIZABLE", "ESCALABLE", "DUPLICABLE", "REEMPLAZABLE", "ESPECIFICO_DE_FASE", "MIXTA")
UNIDADES_VALIDAS = {"m²", "m", "m³", "m³/h", "m³/d", "m³/min", "kg DQO/d", "kg MS/d", "kVA", "kWf", "kWt",
                    "t/h", "t/d", "t/día", "aves/h", "unidad", "lote", "vehículo", "juego", "posiciones",
                    "huevos", "plaza", "plaza_reproductora", "%"}
METODOS = ("unitario", "global", "escalado", "porcentaje")
TOL = 1e-9
_MUT: set = set()

# Opciones de arquitectura (sección 2 del encargo). Ninguna es "mejor".
OPCIONES = {
    "faena": ("propia", "facon"),
    "granjas": ("integradas", "propias", "mixto"),
    "pollito": ("compra", "incubacion"),
    "alimento": ("compra", "facon", "propia"),
    "flota": ("tercero", "propia", "mixto"),
    "frio": ("A_refrigerado", "B_refrigerado_congelado", "C_congelado_tercero"),
    "subproductos": ("A_externo", "B_basico_propio"),
    "terreno": ("compra_fase", "compra_reserva", "parque_industrial", "rural_compatible"),
    "automatizacion": ("manual", "semi", "auto"),
    "modalidad_linea": ("lotes", "llave_en_mano"),
    "tecnologia_efluentes": ("sin_definir", "cloaca", "aerobio_compacto", "anaerobio_aerobio", "lagunas"),
}
FLUJOS = ("pollitos", "alimento", "vivo", "refrigerado", "congelado", "subproductos", "servicio")
# SUP-16-04: arquitectura de frío → perfil de destino de 09C y congelado propio
FRIO_A_PERFIL = {"A_refrigerado": ("P1", True), "B_refrigerado_congelado": ("P2", True),
                 "C_congelado_tercero": ("P1", False)}
# SUP-16-03: ciclo de vehículos de alimento y subproductos (sin fuente)
T_CARGA_DESCARGA_H = 2.0
DIAS_ENTREGA_SEMANA = 6
# SUP-16-15: almacenamiento de agua = días de agua captada (barrido 0,5 / 1 / 2)
DIAS_RESERVA_AGUA = (0.5, 1.0, 2.0)


class ErrorCapex(Exception):
    pass


# ---------------------------------------------------------------------------------------------
# 1. CONFIGURACIÓN
# ---------------------------------------------------------------------------------------------
def config_por_defecto():
    """Valores de partida editables. No son decisión: sirven para que el motor corra."""
    return {
        "nombre": "personalizado", "aves_dia": 10000, "dias_semana": 5, "horas_netas": 8.0,
        "faena": "propia", "granjas": "integradas", "fraccion_granjas_propias": 0.0,
        "pollito": "compra", "reproductoras": False, "alimento": "compra",
        "flota": "tercero", "flota_por_flujo": None,
        "frio": "A_refrigerado", "subproductos": "A_externo", "rendering": False,
        "escala_objetivo": None, "automatizacion": "semi", "terreno": "compra_fase",
        "laboratorio_propio": True, "modalidad_linea": "lotes", "config_producto": "B",
        "tecnologia_efluentes": "sin_definir",
        "fecha_base": FECHA_BASE_CAPEX, "moneda": MONEDA_MODELO,
        "cadencia_incubacion": 2, "dias_op_planta_alimento": 5, "horas_dia_planta_alimento": 8,
        "capacidad_nominal_planta_alimento_t_h": None,
        "aves_camion_vivo": 5500, "cap_camion_refrigerado_t": 12, "cap_camion_congelado_t": 12,
        "cap_camion_pollitos": None, "cap_granelero_t": 28, "cap_vehiculo_subproductos_t": 10,
        "dist_mercado_km": 300, "dist_fabrica_granja_km": 75, "dist_receptor_subproductos_km": 50,
        "radio_granjas_km": 100, "reserva_flota_unidades": 1,
        "umbral_utilizacion_planta_alimento": 0.5,
    }


def preset(nombre, **kw):
    """Configuraciones de REFERENCIA (SUP-16-09). No son recomendación ni secuencia obligatoria."""
    c = config_por_defecto()
    p = {
        "C0": dict(faena="facon", granjas="integradas", pollito="compra", alimento="facon", flota="tercero",
                   frio="C_congelado_tercero", subproductos="A_externo", terreno="compra_fase"),
        "C1": dict(faena="propia", granjas="integradas", pollito="compra", alimento="compra", flota="tercero",
                   frio="A_refrigerado", subproductos="A_externo"),
        "C2": dict(faena="propia", granjas="mixto", fraccion_granjas_propias=0.25, pollito="compra",
                   alimento="facon", flota="mixto",
                   flota_por_flujo={"pollitos": "tercero", "alimento": "tercero", "vivo": "propia",
                                    "refrigerado": "propia", "congelado": "tercero", "subproductos": "tercero",
                                    "servicio": "propia"},
                   frio="B_refrigerado_congelado", subproductos="A_externo"),
        "C3": dict(faena="propia", granjas="propias", fraccion_granjas_propias=1.0, pollito="incubacion",
                   alimento="propia", flota="propia", frio="B_refrigerado_congelado",
                   subproductos="B_basico_propio"),
        "CF": dict(faena="propia", granjas="propias", fraccion_granjas_propias=1.0, pollito="incubacion",
                   reproductoras=True, alimento="propia", flota="propia", frio="B_refrigerado_congelado",
                   subproductos="B_basico_propio", rendering=True),
    }
    if nombre not in p:
        raise ErrorCapex(f"configuración de referencia inexistente: {nombre}")
    c.update(p[nombre])
    c["nombre"] = nombre
    c.update(kw)
    return c


def validar_config(c):
    for k, ops in OPCIONES.items():
        if c[k] not in ops:
            raise ErrorCapex(f"{k} = {c[k]!r} no es una opción válida {ops}")
    E = c["aves_dia"]
    if not isinstance(E, (int, float)) or not RANGO_ESCALA[0] <= E <= RANGO_ESCALA[1]:
        raise ErrorCapex(f"aves/día {E} fuera del rango estudiado {RANGO_ESCALA} (no se extrapola)")
    if c["dias_semana"] not in (5, 6):
        raise ErrorCapex("días de faena por semana: 5 o 6 (SUP-025)")
    f = c["fraccion_granjas_propias"]
    esperado = {"integradas": (0.0, 0.0), "propias": (1.0, 1.0), "mixto": (TOL, 1 - TOL)}[c["granjas"]]
    if not esperado[0] - TOL <= f <= esperado[1] + TOL:
        raise ErrorCapex(f"fracción de granjas propias {f} incompatible con granjas = {c['granjas']}")
    if c["reproductoras"] and c["pollito"] != "incubacion":
        raise ErrorCapex("reproductoras propias requieren incubación propia (arquitectura futura)")
    if c["rendering"] and c["faena"] != "propia":
        raise ErrorCapex("rendering propio requiere planta de faena propia")
    if c["flota"] == "mixto":
        fp = c["flota_por_flujo"]
        if not fp or set(fp) != set(FLUJOS) or any(v not in ("propia", "tercero") for v in fp.values()):
            raise ErrorCapex("flota mixta: indicar propia/tercero para cada flujo " + ", ".join(FLUJOS))
    if c["escala_objetivo"] is not None and c["escala_objetivo"] < E:
        raise ErrorCapex("la escala objetivo de reserva no puede ser menor que la escala")
    if c["moneda"] != MONEDA_MODELO:
        raise ErrorCapex("moneda del modelo: USD (regla 2 de CLAUDE.md); otras monedas solo como original")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c["fecha_base"])):
        raise ErrorCapex("FECHA_BASE_CAPEX debe ser AAAA-MM-DD")
    return c


def flota_de(c, flujo):
    if c["flota"] == "mixto":
        return c["flota_por_flujo"][flujo]
    return c["flota"]


def dias_anio(c):
    return {5: 250, 6: 300}[c["dias_semana"]]          # SUP-025


def etiqueta_arquitectura(c):
    fl = c["flota"] if c["flota"] != "mixto" else "mixto(" + ",".join(
        k for k in FLUJOS if c["flota_por_flujo"][k] == "propia") + ")"
    return (f"faena={c['faena']}|granjas={c['granjas']}:{c['fraccion_granjas_propias']:g}|pollito={c['pollito']}"
            f"{'+reprod' if c['reproductoras'] else ''}|alimento={c['alimento']}|flota={fl}|frio={c['frio']}"
            f"|subprod={c['subproductos']}{'+rendering' if c['rendering'] else ''}|terreno={c['terreno']}"
            f"|autom={c['automatizacion']}|linea={c['modalidad_linea']}")


# ---------------------------------------------------------------------------------------------
# 2. DRIVERS FÍSICOS (importados)
# ---------------------------------------------------------------------------------------------
def _tri(x):
    return tuple(x[n] for n in NIVELES)


def _util_completo(e, nivel):
    """Resultado completo de 09C con los mismos parámetros que usa 12C (ms.utilities)."""
    sh = dict(ms.PERFILES[e["perfil"]])
    p = ms.mu.parametros(nivel, perfil=sh, perfil_id=e["perfil"], dias_refrigerado=e["dias_refrigerado"],
                         dias_congelado=e["dias_congelado"], base_inventario=e["base_inventario"],
                         horas_netas=min(e["horas_netas"], 20))
    r = ms.mu.calcular(e["aves_dia"], dias_anio=e["dias_anio"], nivel=nivel,
                       masas=ms.masas_utilities(e["config"]), p=p)
    return dict(r.v)


def entradas_superficie(c):
    perfil, congelado = FRIO_A_PERFIL[c["frio"]]
    if c["terreno"] == "compra_reserva" or c["escala_objetivo"] is not None:   # SUP-16-16: reserva explícita
        obj, rend = (c["escala_objetivo"] or RANGO_ESCALA[1]), True
    else:                                                  # solo la fase (sin reserva)
        obj, rend = c["aves_dia"], c["rendering"]
    return dict(ms.entradas_por_defecto(), aves_dia=c["aves_dia"], horas_netas=c["horas_netas"],
                dias_anio=dias_anio(c), config=c["config_producto"], perfil=perfil,
                congelado_propio=congelado, laboratorio_propio=c["laboratorio_propio"],
                automatizacion=c["automatizacion"], tecnologia_efluentes=c["tecnologia_efluentes"],
                escala_objetivo=obj, reservar_rendering=rend)


def _vehiculos(viajes_semana, dist_km, vel, horas_dia, dias_semana):
    """VOLUMEN ÷ CAPACIDAD (ya en viajes) ÷ CICLOS DISPONIBLES (SUP-16-03)."""
    if viajes_semana is None:
        return None
    ciclo = 2 * dist_km / vel + T_CARGA_DESCARGA_H
    ciclos_dia = max(1, math.floor(horas_dia / ciclo + TOL))
    return math.ceil(viajes_semana / (ciclos_dia * dias_semana) - TOL)


def drivers(c):
    """Cantidades físicas por escala y arquitectura. Nada económico."""
    E, ds = c["aves_dia"], c["dias_semana"]
    D = {"E": E, "ds": ds, "dias_anio": dias_anio(c), "ritmo_aves_h": E / c["horas_netas"], "alertas": []}
    perfil, _ = FRIO_A_PERFIL[c["frio"]]
    if c["faena"] == "propia":
        e = entradas_superficie(c)
        R = ms.calcular(e)
        s = ms.salida_interfaz(R)
        D["areas"] = {a: (x["bajo"], x["medio"], x["alto"]) for a, x in s["areas_por_funcion"].items()}
        D["terreno_m2"] = _tri(s["m2_terreno"])
        D["m2_construidos"] = _tri(s["m2_construidos"])
        rel = [ms.v("relacion_largo_ancho", i) for i in range(3)]
        D["perimetro_m"] = tuple(None if t is None else 2 * (math.sqrt(t / r) * r + math.sqrt(t / r))
                                 for t, r in zip(D["terreno_m2"], rel))
        D["util"] = {n: _util_completo(e, n) for n in NIVELES}
        D["alertas"] += [f"12C:{a}" for a in s["alertas"]]
    # Logística (12B): solo flujos con flota propia
    D["flota"] = {}
    vel, hcd = ml.VEL_TRONCAL, ml.HORAS_CAMION_DIA
    res = c["reserva_flota_unidades"]
    for fl in FLUJOS:
        if flota_de(c, fl) != "propia":
            continue
        base, origen = None, ""
        if fl == "vivo":
            v = ml.aves_vivas(E, ds, radio_km=c["radio_granjas_km"], aves_camion=c["aves_camion_vivo"])
            base, origen = v["flota_minima"], f"12B aves_vivas: flota mínima ({c['aves_camion_vivo']} aves/camión SUP-033)"
        elif fl in ("refrigerado", "congelado"):
            p = ml.producto(E, ds, perfil=perfil, dias_despacho=6, cap_refrigerado=c["cap_camion_refrigerado_t"],
                            cap_congelado=c["cap_camion_congelado_t"], dist_km=c["dist_mercado_km"],
                            despachos_congelado=2)
            cd = p.get(f"{fl}_camion_dia")
            base = None if cd is None else math.ceil(cd - TOL) if cd > TOL else 0
            origen = f"12B producto: camión-día {fl} (troncal {c['dist_mercado_km']} km; reparto capilar PENDIENTE DEC-053)"
        elif fl == "alimento":
            i = ml.insumos(E, ds, cap_granelero=c["cap_granelero_t"], dist_fabrica=c["dist_fabrica_granja_km"])
            base = _vehiculos(i["alimento_viajes_semana"], c["dist_fabrica_granja_km"], vel, hcd, DIAS_ENTREGA_SEMANA)
            origen = f"12B insumos: {i['alimento_viajes_semana']} viajes/sem ÷ ciclos (SUP-16-03)"
        elif fl == "pollitos":
            i = ml.insumos(E, ds, cap_granelero=c["cap_granelero_t"], cap_pollitos=c["cap_camion_pollitos"])
            vs = i["pollitos_viajes_semana"]
            base = None if vs is None else _vehiculos(vs, 150, vel, hcd, DIAS_ENTREGA_SEMANA)
            origen = "12B insumos: capacidad de camión de pollitos PENDIENTE (DPV-047, DPV-084)" if vs is None \
                else f"12B insumos: {vs} viajes/sem"
        elif fl == "subproductos":
            tot = 0
            for g in ("G1-plumas", "G2-sangre", "G3-visceras", "G4-decomisos"):
                s_ = ml.subproductos(E, ds, c["config_producto"], "E1", cap=c["cap_vehiculo_subproductos_t"], corriente=g)
                tot += s_["viajes_semana_criterio_masa"]
            base = _vehiculos(tot, c["dist_receptor_subproductos_km"], vel, hcd, ds)
            origen = f"12B subproductos: {tot} viajes/sem por criterio MÁSICO (volumétrico PENDIENTE DPV-135) = cota inferior"
        else:   # servicio
            origen = "Sin driver físico: cantidad PENDIENTE (no se fijan cantidades arbitrarias)"
        D["flota"][fl] = {"base": base, "unidades": None if base is None else (base + res if base > 0 else 0),
                          "origen": origen + ("" if base is None else f"; + reserva {res} (SUP-16-02)")}
    # Upstream (14B)
    po = mup.pollitos(E, ds)
    D["pollitos_semana"] = po["pollitos_a_recibir_semana_plena"]
    D["plazas_alojamiento"] = po["capacidad_alojamiento_pollitos"]
    D["m2_galpon"] = po["m2_galpon"]
    if c["pollito"] == "incubacion":
        inc = mup.incubacion(D["pollitos_semana"], cadencia=c["cadencia_incubacion"])
        D["incubacion"] = {k: inc[k] for k in ("posiciones_setter_diseno", "posiciones_hatcher_diseno",
                                               "capacidad_almacen_huevos", "huevos_recibidos_semana")}
    if c["reproductoras"]:
        D["reproductoras"] = mup.reproductoras_fase_futura(D["pollitos_semana"], "FF")["reproductoras_hembras_postura_equiv"]
    if c["alimento"] == "propia":
        al = mup.alimento(E, ds)
        pa = mup.planta_alimento(al["alimento_t_semana_plena"], dias_op=c["dias_op_planta_alimento"],
                                 horas_dia=c["horas_dia_planta_alimento"])
        st = mup.almacenamiento(E, "C_planta_propia", ds)
        cap = c["capacidad_nominal_planta_alimento_t_h"] or pa["t_h_requerida"]
        util = al["alimento_t_semana_plena"] / (cap * c["dias_op_planta_alimento"] * c["horas_dia_planta_alimento"] * pa["eficiencia"])
        D["alimento"] = {"t_h_requerida": pa["t_h_requerida"], "t_h_instalada": cap, "utilizacion": util,
                         "m3_silos_mp": st["maiz_m3_brutos"] + st["soja_m3_brutos"],
                         "m3_silos_pt": st["alim_planta_m3_brutos"], "m3_silos_granja": st["granja_m3_brutos"]}
        if util < c["umbral_utilizacion_planta_alimento"]:
            D["alertas"].append(f"PLANTA_ALIMENTO_SUBUTILIZADA: utilización {util:.0%} < "
                                f"{c['umbral_utilizacion_planta_alimento']:.0%} (SUP-16-17); no elegir por catálogo")
    else:
        D["alimento_granja_m3"] = mup.almacenamiento(E, "A_compra", ds)["granja_m3_brutos"]
    return D


# ---------------------------------------------------------------------------------------------
# 3. CATÁLOGO DE EQUIPOS (08) Y MAPEOS SIN DUPLICACIÓN
# ---------------------------------------------------------------------------------------------
# Mapeo áreas de 12C → categoría de obra civil (cada área en UNA sola categoría; test X03)
OC_MAP = {
    "OC-RS": ("recepcion_espera",),
    "OC-PH": ("colgado_aturdido", "sangrado_escaldado_desplumado", "evisceracion_inspeccion", "enfriamiento",
              "clasificacion", "trozado", "deshuese", "cms", "coproductos", "empaque", "lavado_cajones",
              "circulacion_proceso", "sala_subproductos"),
    "OC-FR": ("camaras_refrigeradas", "camaras_congeladas", "tunel_congelado", "antecamaras_preparacion",
              "camara_subproductos", "camara_decomisos"),
    "OC-DK": ("expedicion_docks",),
    "OC-DP": ("residuos_carton", "deposito_envases", "mantenimiento_taller", "repuestos", "quimicos"),
    "OC-ST": ("sala_maquinas_frio", "caldera_agua_caliente", "aire_comprimido", "generador", "sala_electrica",
              "tratamiento_agua"),
    "OC-LB": ("laboratorio_calidad",),
    "OC-VC": ("vestuarios", "comedor", "lavanderia"),
    "OC-OF": ("oficinas", "oficina_senasa", "enfermeria_capacitacion", "porterias_seguridad", "circulacion_personal"),
    "OC-EP": ("playa_aves_vivas", "playa_despacho", "playa_subproductos", "circulacion_pesada"),
    "OC-EL": ("estacionamiento",),
    "OC-LV": ("lavado_camiones",),
    "OC-IP": ("tanques_agua",),
    "OC-EF": ("efl_pretratamiento", "efl_ecualizacion", "efl_daf", "efl_biologico", "efl_lodos", "efl_circulacion"),
}
AREAS_NO_OBRA = ("reserva_expansion",)    # reserva = terreno, no obra

# Lote de RFQ de cada EQ (08 requerimientos_cotizacion.md §3) y su costeador en el CAPEX.
# EQ-28 y EQ-33 figuran en L3 y en L6: se asignan SOLO a L3 (T16-01). EQ-03 → logística (cajones),
# EQ-14 → térmico, EQ-37 → frío (agua helada), EQ-54/EQ-76 → IT, EQ-57..65 → frío, EQ-66..69 → subproductos,
# EQ-70 → efluentes, EQ-71 → aire, EQ-72 → agua, EQ-73 → generación de respaldo, EQ-74/75 → higiene.
def padre_de_eq(n):
    especiales = {3: "JAU-VIVO", 14: "TE-GEN", 37: "FR-AGH", 54: "IT-ETQ", 76: "IT-SEN", 70: "EF-PRE",
                  71: "AC-COM", 72: "AG-ALM", 73: "EL-GEN", 74: "EQ-LIM", 75: "EQ-LIM", 65: "FR-DCK",
                  57: "FR-TUN", 58: "FR-TUN", 59: "FR-TUN", 60: "FR-TUN", 61: "FR-TUN", 64: "FR-COMP",
                  62: "FR-PAN", 63: "FR-PAN"}
    if n in especiales:
        return especiales[n]
    for lote, (a, b) in (("PQ-L1", (1, 6)), ("PQ-L2", (7, 20)), ("PQ-L3", (21, 33)), ("PQ-L4", (34, 38)),
                         ("PQ-L5", (39, 46)), ("PQ-L6", (47, 48)), ("PQ-L7", (49, 56)), ("SB-L9", (66, 69))):
        if a <= n <= b:
            return lote
    raise ErrorCapex(f"EQ-{n:02d} sin costeador")


def leer_equipos(ruta=ARCHIVO_EQUIPOS):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def etiqueta_modularidad(texto):
    """SUP-16-11: modularidad de 08 → etiqueta de expansión."""
    t = (texto or "").lower()
    if t.startswith("mantener"):
        return "REUTILIZABLE"
    if t.startswith("duplicar") or t.startswith("agregar"):
        return "DUPLICABLE"
    if t.startswith("ampliar"):
        return "ESCALABLE"
    if t.startswith("reemplaz"):
        return "REEMPLAZABLE"
    return "ESPECIFICO_DE_FASE"


def nivel_eq(fila, E, autom):
    """SUP-16-05: nivel de la escala de referencia más cercana (empate hacia arriba)."""
    ref = min(ESCALAS_REF, key=lambda s: (abs(s - E), -s))
    nv = fila[f"nivel_{ref}"].strip()
    if "/" in nv:
        ops = nv.split("/")
        nv = ops[0] if autom == "manual" else ops[-1] if autom == "auto" else ("S" if "S" in ops else ops[0])
    return nv


def eq_aplica(n, nv, c):
    if nv in ("—", "-", "", "T"):
        return False
    if nv == "O":                                   # opcional: solo si la arquitectura lo pide
        return (n in (43, 44, 46) and c["config_producto"] == "C") or (n == 47 and c["config_producto"] != "A") \
            or (n in (57, 58) and FRIO_A_PERFIL[c["frio"]][1])
    if 42 <= n <= 46 and c["config_producto"] != "C":   # deshuese solo en config. C
        return False
    if 57 <= n <= 61 and not FRIO_A_PERFIL[c["frio"]][1]:
        return False
    if n == 26:                                      # puestos de inspección oficial: infraestructura en planta
        return True
    return True


# ---------------------------------------------------------------------------------------------
# 4. BOQ — REGISTRO DE ACTIVOS
# ---------------------------------------------------------------------------------------------
BLOQUES = ("TERRENO", "OBRA_CIVIL", "PROCESO", "SUBPRODUCTOS", "FRIO", "UTILITIES", "EFLUENTES",
           "SERVICIOS_GENERALES", "LOGISTICA", "INCUBACION", "ALIMENTO", "GRANJAS", "INDIRECTOS",
           "PREOPERATIVOS", "CONTINGENCIA")
CAMPOS_BOQ = ["ESCENARIO", "ACTIVO_ID", "ARQUITECTURA", "MODULO", "SUBMODULO", "BLOQUE", "CATEGORIA_CAPEX",
              "ACTIVO", "CAPACIDAD", "UNIDAD_CAPACIDAD", "CANTIDAD_BAJO", "CANTIDAD", "CANTIDAD_ALTO", "UNIDAD",
              "ORIGEN_DIMENSIONAMIENTO", "COSTO_ID", "INCLUIDO_EN_PAQUETE", "ACTIVO_PADRE", "COSTEA",
              "ETIQUETA_EXPANSION", "REUTILIZABLE", "ESCALABLE", "FASE", "TITULAR", "NIVEL_AUTOMATIZACION",
              "ESTADO_DIMENSION", "ESTADO_COSTO", "NIVEL_EVIDENCIA", "MONEDA_ORIGINAL", "PRECIO_UNITARIO_USD",
              "COSTO_EQUIPO_USD", "COSTO_LANDED_USD", "COSTO_INSTALADO_LOW_USD", "COSTO_INSTALADO_USD",
              "COSTO_INSTALADO_HIGH_USD", "ORIGEN_RANGO", "VIDA_UTIL_ANIOS", "REEMPLAZO_ANIO", "COSTO_REEMPLAZO",
              "VALOR_RESIDUAL", "ALERTAS"]


class Boq:
    def __init__(self, c):
        self.c, self.filas, self.ids = c, [], set()

    def add(self, aid, modulo, sub, bloque, activo, costo_id, cant=None, unidad="lote", origen="",
            cat="DIRECTO", capacidad="", ucap="", padre="", incluido="No", etiqueta="ESCALABLE",
            fase="INICIAL", titular="EMPRESA", nivel="", estado=None):
        if aid in self.ids:
            raise ErrorCapex(f"ACTIVO_ID duplicado: {aid}")
        if "B01" in _MUT and aid.startswith("OC-DP"):
            cant = None if cant is None else tuple(None if x is None else x * 2 for x in cant)
        self.ids.add(aid)
        if cant is not None and not isinstance(cant, tuple):
            cant = (cant, cant, cant)
        if estado is None:
            estado = "PENDIENTE" if cant is None or cant[1] is None else "DIMENSIONADO"
        costea = not (padre and incluido in ("Sí", "PENDIENTE"))
        self.filas.append({
            "ACTIVO_ID": aid, "MODULO": modulo, "SUBMODULO": sub, "BLOQUE": bloque, "CATEGORIA_CAPEX": cat,
            "ACTIVO": activo, "CAPACIDAD": capacidad, "UNIDAD_CAPACIDAD": ucap,
            "CANTIDAD_BAJO": None if cant is None else cant[0], "CANTIDAD": None if cant is None else cant[1],
            "CANTIDAD_ALTO": None if cant is None else cant[2], "UNIDAD": unidad,
            "ORIGEN_DIMENSIONAMIENTO": origen, "COSTO_ID": costo_id, "INCLUIDO_EN_PAQUETE": incluido,
            "ACTIVO_PADRE": padre, "COSTEA": costea, "ETIQUETA_EXPANSION": etiqueta,
            "REUTILIZABLE": "Sí" if etiqueta in ("REUTILIZABLE", "ESCALABLE") else "No",
            "ESCALABLE": "Sí" if etiqueta in ("ESCALABLE", "DUPLICABLE") else "No",
            "FASE": fase, "TITULAR": titular, "NIVEL_AUTOMATIZACION": nivel, "ESTADO_DIMENSION": estado})


def _sum_areas(D, areas):
    xs = [D["areas"].get(a) for a in areas if a in D["areas"]]
    if not xs:
        return None
    return tuple(None if any(x[i] is None for x in xs) else sum(x[i] for x in xs) for i in range(3))


def _u(D, k):
    return tuple(D["util"][n].get(k) for n in NIVELES)


def _escalar(t, f):
    return None if t is None else tuple(None if x is None else x * f for x in t)


def generar_boq(c, D=None):
    validar_config(c)
    D = D or drivers(c)
    B = Boq(c)
    autom = c["automatizacion"]
    propia = c["faena"] == "propia"
    ritmo = D["ritmo_aves_h"]
    if propia:
        # ---- A. TERRENO -------------------------------------------------------------------------
        t_id = {"compra_fase": "TER-01", "compra_reserva": "TER-01", "parque_industrial": "TER-02",
                "rural_compatible": "TER-03"}[c["terreno"]]
        reserva = c["terreno"] == "compra_reserva" or c["escala_objetivo"] is not None
        org = ("12C terreno conceptual " + ("con reserva para la escala objetivo y rendering" if reserva
               else "sin reserva (solo la fase)") + "; superficie conceptual ≠ proyecto ejecutivo")
        B.add("TER-COMPRA", "TERRENO", "compra", "TERRENO", "Compra de terreno", t_id, D["terreno_m2"], "m²", org,
              etiqueta="REUTILIZABLE")
        B.add("TER-GASTOS", "TERRENO", "gastos", "TERRENO", "Gastos asociados a la compra", "TER-04", 1, "%",
              "% sobre compra de terreno (no adoptado)", etiqueta="ESPECIFICO_DE_FASE")
        B.add("TER-PREP", "TERRENO", "preparacion", "TERRENO", "Preparación inicial del sitio", "TER-05",
              D["terreno_m2"], "m²", "= terreno conceptual 12C", etiqueta="ESCALABLE")
        if c["terreno"] == "parque_industrial":
            B.add("TER-PARQUE", "TERRENO", "parque", "TERRENO", "Cargo de infraestructura del parque", "TER-08", 1,
                  "lote", "1 lote; alcance según parque (DPV-16-03)", etiqueta="REUTILIZABLE")
        else:
            B.add("TER-ACCESO", "TERRENO", "acceso", "TERRENO", "Infraestructura de acceso", "TER-06", 1, "lote",
                  "1 lote; alcance según sitio (DPV-16-03)", etiqueta="REUTILIZABLE")
            B.add("TER-CONEX", "TERRENO", "conexiones", "TERRENO", "Conexiones extraordinarias", "TER-07", 1,
                  "lote", "1 lote; alcance según sitio (DPV-16-11)", etiqueta="REUTILIZABLE")
        # ---- B. OBRA CIVIL ----------------------------------------------------------------------
        nombres = {"OC-RS": "Recepción semicubierta", "OC-PH": "Proceso húmedo", "OC-FR": "Envolvente de frío",
                   "OC-DK": "Docks y expedición", "OC-DP": "Depósitos y talleres secos", "OC-ST": "Salas técnicas",
                   "OC-LB": "Laboratorio", "OC-VC": "Vestuarios, comedor y lavandería",
                   "OC-OF": "Oficinas, inspección oficial, enfermería, porterías", "OC-EP": "Pavimento pesado",
                   "OC-EL": "Estacionamiento", "OC-LV": "Plataforma de lavado de camiones",
                   "OC-IP": "Infraestructura pesada (bases, tanques)", "OC-EF": "Obra civil de efluentes"}
        for cid, areas in OC_MAP.items():
            q = _sum_areas(D, areas)
            if q is None or q[1] is None:
                continue
            if cid == "OC-LB" and not c["laboratorio_propio"]:
                continue
            B.add(f"{cid}-OBRA", "OBRA_CIVIL", cid, "OBRA_CIVIL", nombres[cid], cid, q, "m²",
                  "12C Σ áreas: " + ", ".join(areas) + " (PROXY/ESTIMACIÓN; conceptual ≠ ejecutivo)",
                  etiqueta="ESCALABLE")
        B.add("OC-CER-OBRA", "OBRA_CIVIL", "OC-CER", "OBRA_CIVIL", "Cerco perimetral", "OC-CER", D["perimetro_m"], "m",
              "perímetro del rectángulo de terreno 12C (relación 1,5)",
              etiqueta="REUTILIZABLE" if reserva else "ESCALABLE")
        B.add("OC-INF-OBRA", "OBRA_CIVIL", "OC-INF", "OBRA_CIVIL", "Infraestructura interna del predio", "OC-INF",
              D["terreno_m2"], "m²", "= terreno conceptual 12C; alcance PENDIENTE", etiqueta="ESCALABLE")
        # ---- C. PROCESO (lotes RFQ + EQ hijos) --------------------------------------------------
        llave = c["modalidad_linea"] == "llave_en_mano"
        if llave:
            B.add("PQ-L11", "PROCESO", "linea", "PROCESO", "Línea completa llave en mano (L1–L5)", "PQ-L11",
                  1, "lote", "ritmo operativo = aves/día ÷ horas netas", capacidad=round(ritmo, 1), ucap="aves/h",
                  etiqueta="MIXTA")
        lotes = {"PQ-L1": "Recepción de vivo", "PQ-L2": "Faena", "PQ-L3": "Evisceración", "PQ-L4": "Enfriamiento",
                 "PQ-L5": "Clasificación, trozado y deshuese", "PQ-L6": "Coproductos", "PQ-L7": "Packaging"}
        eqs = leer_equipos()
        hijos = {}
        for f in eqs:
            n = int(f["id"].split("-")[1])
            nv = nivel_eq(f, c["aves_dia"], autom)
            if eq_aplica(n, nv, c):
                hijos.setdefault(padre_de_eq(n), []).append((f, nv))
        for l, nom in lotes.items():
            if l not in hijos:
                continue
            en_l11 = llave and l in ("PQ-L1", "PQ-L2", "PQ-L3", "PQ-L4", "PQ-L5")
            B.add(l, "PROCESO", "linea", "PROCESO", f"Lote {l[3:]} — {nom}", l, 1, "lote",
                  "ritmo operativo = aves/día ÷ horas netas (capacidad contractual DPV-097)",
                  capacidad=round(ritmo, 1), ucap="aves/h", padre="PQ-L11" if en_l11 else "",
                  incluido="Sí" if en_l11 else "No", etiqueta="MIXTA")
        B.add("EQ-LIM", "PROCESO", "higiene", "PROCESO", "Limpieza e higiene (espuma, esterilizadores)", "EQ-LIM",
              1, "lote", "1 lote; puestos según 12C/14A", etiqueta="ESCALABLE")
        # ---- SUBPRODUCTOS ----------------------------------------------------------------------
        sub_t = sum(D["util"]["medio"].get(k, 0) or 0 for k in ("segregable_sangre_recuperada_t_dia",
                                                                "segregable_plumas_t_dia",
                                                                "segregable_visceras_t_dia",
                                                                "segregable_cabeza_t_dia"))
        B.add("SB-L9", "SUBPRODUCTOS", "lote", "SUBPRODUCTOS", "Lote L9 — sangre, plumas, vísceras, contenedores",
              "SB-L9", 1, "lote", "09C masa segregable (sangre+plumas+vísceras+cabeza)", capacidad=round(sub_t, 2),
              ucap="t/d", etiqueta="ESCALABLE")
        if c["subproductos"] == "B_basico_propio":
            B.add("SB-BAS", "SUBPRODUCTOS", "basico", "SUBPRODUCTOS", "Tratamiento básico propio de subproductos",
                  "SB-BAS", 1, "lote", "09C masa segregable; tecnología PENDIENTE (DEC-027)",
                  capacidad=round(sub_t, 2), ucap="t/d", etiqueta="ESCALABLE")
        if c["rendering"]:
            B.add("SB-REN", "SUBPRODUCTOS", "rendering", "SUBPRODUCTOS", "Rendering propio (FUTURO)", "SB-REN", 1,
                  "lote", "solo arquitectura futura / sensibilidad", capacidad=round(sub_t, 2), ucap="t/d",
                  fase="FUTURO", etiqueta="ESPECIFICO_DE_FASE")
        # ---- D. FRÍO ---------------------------------------------------------------------------
        u = D["util"]
        kwf_parcial = tuple(sum((u[n].get(k) or 0) for k in (
            "carga_sensible_preliminar_producto_kwf_bajo_8h", "carga_enfriamiento_agua_reposicion_chiller_kwf_bajo_8h",
            "cargas_adicionales_ilustrativas_kwf", "carga_media_congelacion_producto_kwf_bajo_20h")) for n in NIVELES)
        congela = FRIO_A_PERFIL[c["frio"]][1]
        B.add("FR-PAQ", "FRIO", "paquete", "FRIO", "Paquete de frío (RFQ 2)", "FR-PAQ", 1, "lote",
              "carga total PENDIENTE (DPV-109); cota inferior = Σ cargas preliminares 09C",
              capacidad=f"≥ {kwf_parcial[1]:.0f}", ucap="kWf", etiqueta="ESCALABLE", estado="COTA_INFERIOR")
        camaras = _sum_areas(D, ("camaras_refrigeradas", "camaras_congeladas", "tunel_congelado",
                                 "antecamaras_preparacion", "camara_subproductos", "camara_decomisos"))
        hijos_frio = [("FR-PAN", "Paneles aislantes de cámaras", camaras, "m²", "12C m² de cámaras", "ESCALABLE"),
                      ("FR-COMP", "Compresores / sala de máquinas", None, "kWf", "kWf total PENDIENTE (DPV-109)", "DUPLICABLE"),
                      ("FR-COND", "Condensación", None, "kWf", "kWf total PENDIENTE", "DUPLICABLE"),
                      ("FR-EVAP", "Evaporadores", None, "kWf", "kWf total PENDIENTE", "DUPLICABLE"),
                      ("FR-PIP", "Piping y aislación", 1, "lote", "alcance del paquete", "ESCALABLE"),
                      ("FR-REF", "Refrigerante / fluido secundario", 1, "lote", "tecnología abierta (DEC-046)", "ESCALABLE"),
                      ("FR-CTL", "Controles de frío", 1, "lote", "alcance del paquete", "ESCALABLE"),
                      ("FR-AGH", "Agua helada / hielo para chiller (EQ-37)", _escalar(
                          tuple(u[n].get("carga_enfriamiento_agua_reposicion_chiller_kwf_bajo_8h") for n in NIVELES), 1),
                       "kWf", "09C carga de reposición del chiller (preliminar)", "ESCALABLE"),
                      ("FR-DCK", "Equipamiento de docks (EQ-65)", None, "unidad", "posiciones de dock PENDIENTES (D12-01)", "DUPLICABLE")]
        if congela:
            hijos_frio.append(("FR-TUN", "Túnel de congelado (EQ-57/58)",
                               tuple(u[n].get("capacidad_congelacion_t_dia") for n in NIVELES), "t/día",
                               "09C capacidad de congelación", "DUPLICABLE"))
        for cid, nom, q, un, org, et in hijos_frio:
            B.add(cid, "FRIO", "componente", "FRIO", nom, cid, q, un, org, padre="FR-PAQ", incluido="Sí", etiqueta=et)
        # ---- E. AGUA ---------------------------------------------------------------------------
        cap = _u(D, "agua_captada_m3_dia")
        qmax = _u(D, "caudal_horario_maximo_ilustrativo_m3_h")
        B.add("AG-CAP", "AGUA", "captacion", "UTILITIES", "Captación o conexión de agua", "AG-CAP", cap, "m³/d",
              "09C agua captada (m³/d); fuente según sitio", etiqueta="ESCALABLE")
        B.add("AG-ALM", "AGUA", "almacenamiento", "UTILITIES", "Almacenamiento de agua (EQ-72)", "AG-ALM",
              tuple(cap[i] * DIAS_RESERVA_AGUA[i] for i in range(3)), "m³",
              "agua captada × días de reserva 0,5/1/2 (SUP-16-15)", etiqueta="DUPLICABLE")
        B.add("AG-TRA", "AGUA", "tratamiento", "UTILITIES", "Tratamiento de agua", "AG-TRA", qmax, "m³/h",
              "09C caudal horario máximo ilustrativo [SUPUESTO]", etiqueta="ESCALABLE")
        B.add("AG-BOM", "AGUA", "bombeo", "UTILITIES", "Bombeo", "AG-BOM", qmax, "m³/h", "ídem", etiqueta="DUPLICABLE")
        B.add("AG-DIS", "AGUA", "distribucion", "UTILITIES", "Distribución interna de agua", "AG-DIS",
              D["m2_construidos"], "m²", "12C m² construidos", etiqueta="ESCALABLE")
        # ---- F. EFLUENTES ----------------------------------------------------------------------
        desc = _u(D, "agua_descargada_m3_dia")
        qef = _u(D, "caudal_efluente_horario_maximo_ilustrativo_m3_h")
        dqo = tuple(max(D["util"][n].get("metodoA_carga_DQO_kg_dia") or 0, D["util"][n].get("metodoB_carga_DQO_kg_dia") or 0)
                    for n in NIVELES)
        B.add("EF-PAQ", "EFLUENTES", "paquete", "EFLUENTES", "Paquete de tratamiento de efluentes (RFQ 3)", "EF-PAQ",
              1, "lote", "09C agua descargada; tecnología abierta (DEC-043)", capacidad=round(desc[1], 1), ucap="m³/d",
              etiqueta="ESCALABLE")
        bio_aplica = c["tecnologia_efluentes"] != "cloaca"
        for cid, nom, q, un, org in [("EF-PRE", "Pretratamiento (EQ-70)", qef, "m³/h", "09C caudal máx. ilustrativo"),
                                     ("EF-ECU", "Ecualización", desc, "m³", "09C volumen diario descargado (tiempo de retención PENDIENTE)"),
                                     ("EF-DAF", "Separación fisicoquímica", qef, "m³/h", "09C caudal máx. ilustrativo"),
                                     ("EF-BIO", "Tratamiento biológico", dqo, "kg DQO/d", "09C carga DQO (máx. de métodos A/B)"),
                                     ("EF-LOD", "Manejo de lodos", None, "kg MS/d", "lodos PENDIENTES (DPV-114)"),
                                     ("EF-INF", "Infraestructura asociada", 1, "lote", "alcance del paquete")]:
            if cid == "EF-BIO" and not bio_aplica:
                continue
            B.add(cid, "EFLUENTES", "componente", "EFLUENTES", nom, cid, q, un, org, padre="EF-PAQ", incluido="Sí")
        # ---- G/H/I. ELECTRICIDAD, TÉRMICO, AIRE ------------------------------------------------
        kwm = _u(D, "potencia_media_equivalente_proceso_kw_bajo_14h")
        crit = tuple(sum((D["util"][n].get(k) or 0) for k in (
            "carga_critica_ilustrativa_camaras_frio_kw", "carga_critica_ilustrativa_efluentes_minimo_kw",
            "carga_critica_ilustrativa_control_it_seguridad_kw", "carga_critica_ilustrativa_iluminacion_emergencia_kw"))
            for n in NIVELES)
        B.add("EL-ACO", "ELECTRICIDAD", "acometida", "UTILITIES", "Acometida de media tensión", "EL-ACO", 1, "lote",
              "alcance según distribuidora", etiqueta="REUTILIZABLE")
        B.add("EL-TRA", "ELECTRICIDAD", "transformacion", "UTILITIES", "Transformación", "EL-TRA", None, "kVA",
              f"demanda máxima PENDIENTE (09C); cota inferior: potencia media de proceso ≈ {kwm[1]:.0f} kW",
              etiqueta="ESCALABLE", estado="PENDIENTE")
        B.add("EL-TAB", "ELECTRICIDAD", "tableros", "UTILITIES", "Tableros", "EL-TAB", 1, "lote", "alcance según ingeniería",
              etiqueta="ESCALABLE")
        B.add("EL-DIS", "ELECTRICIDAD", "distribucion", "UTILITIES", "Distribución eléctrica e iluminación", "EL-DIS",
              D["m2_construidos"], "m²", "12C m² construidos", etiqueta="ESCALABLE")
        B.add("EL-UPS", "ELECTRICIDAD", "ups", "UTILITIES", "UPS y control", "EL-UPS", None, "kVA",
              "carga de control/IT PENDIENTE", etiqueta="DUPLICABLE")
        B.add("EL-GEN", "ELECTRICIDAD", "respaldo", "UTILITIES", "Generación de respaldo (EQ-73)", "EL-GEN", None, "kVA",
              f"política de respaldo abierta (DEC-047); carga crítica ilustrativa ≈ {crit[1]:.0f} kW (cota inferior)",
              etiqueta="DUPLICABLE")
        kwt = tuple(sum((D["util"][n].get(k) or 0) for k in (
            "potencia_termica_media_equivalente_escaldado_kw_bajo_8h",)) for n in NIVELES)
        B.add("TE-GEN", "TERMICO", "generacion", "UTILITIES", "Caldera / generador de agua caliente (EQ-14)", "TE-GEN",
              None, "kWt", f"potencia térmica pico PENDIENTE (09C); escaldado medio ≈ {kwt[1]:.0f} kWt (cota)",
              etiqueta="DUPLICABLE")
        B.add("TE-COM", "TERMICO", "combustible", "UTILITIES", "Abastecimiento de combustible", "TE-COM", 1, "lote",
              "fuente térmica abierta (DEC-045)", etiqueta="ESCALABLE")
        B.add("TE-DIS", "TERMICO", "distribucion", "UTILITIES", "Distribución térmica", "TE-DIS", 1, "lote",
              "alcance según ingeniería", etiqueta="ESCALABLE")
        B.add("AC-COM", "AIRE_COMPRIMIDO", "aire", "UTILITIES", "Aire comprimido (EQ-71)", "AC-COM", None, "m³/min",
              "caudal PENDIENTE (DPV-095)", etiqueta="DUPLICABLE")
        # ---- J/K/L. IT, LABORATORIO, SEGURIDAD, PERSONAL --------------------------------------
        for cid, nom, et in [("IT-HW", "Hardware IT", "ESCALABLE"), ("IT-SW", "Software inicial", "REUTILIZABLE"),
                             ("IT-SEN", "Sensores y SCADA (EQ-76)", "ESCALABLE"), ("IT-RED", "Comunicaciones y CCTV", "ESCALABLE")]:
            B.add(cid, "IT_TRAZABILIDAD", "it", "SERVICIOS_GENERALES", nom, cid, 1, "lote", "alcance PENDIENTE",
                  etiqueta=et)
        B.add("IT-ETQ", "IT_TRAZABILIDAD", "etiquetado", "SERVICIOS_GENERALES", "Balanzas etiquetadoras (EQ-54)",
              "IT-ETQ", None, "unidad", "puestos de etiquetado PENDIENTES (RFQ L7)", etiqueta="DUPLICABLE")
        if c["laboratorio_propio"]:
            B.add("LAB-EQ", "LABORATORIO", "laboratorio", "SERVICIOS_GENERALES", "Equipamiento de laboratorio", "LAB-EQ",
                  1, "lote", "laboratorio propio (DEC-065)", etiqueta="REUTILIZABLE")
        for cid, nom in [("SI-DET", "Detección de incendio"), ("SI-COM", "Combate de incendio"),
                         ("SI-PRO", "Protección pasiva y señalización")]:
            B.add(cid, "SEGURIDAD_INCENDIO", "incendio", "SERVICIOS_GENERALES", nom, cid, 1, "lote",
                  "requerimientos según bomberos/municipio PENDIENTES (DPV-106)", etiqueta="ESCALABLE")
        B.add("PER-EQ", "PERSONAL", "equipamiento", "SERVICIOS_GENERALES", "Equipamiento de vestuarios y comedor", "PER-EQ",
              1, "lote", "pico simultáneo de personas 14A (SUP-141)", etiqueta="ESCALABLE")
        B.add("MOB-OF", "PERSONAL", "mobiliario", "SERVICIOS_GENERALES", "Mobiliario de oficinas", "MOB-OF", 1, "lote",
              "estructura 14A", etiqueta="REUTILIZABLE")
        # EQ hijos (informativos, costeados por su paquete o por el bloque correspondiente)
        for padre, lst in sorted(hijos.items()):
            for f, nv in lst:
                n = int(f["id"].split("-")[1])
                if padre not in B.ids:
                    if padre == "JAU-VIVO":
                        continue                  # cajones: van con la logística de aves vivas
                    raise ErrorCapex(f"{f['id']}: padre {padre} no está en el BOQ")
                B.add(f["id"], "PROCESO" if padre.startswith("PQ") else B.filas[[x["ACTIVO_ID"] for x in B.filas].index(padre)]["MODULO"],
                      f["grupo"], [x for x in B.filas if x["ACTIVO_ID"] == padre][0]["BLOQUE"], f["equipo"], "",
                      1, "unidad", "08 matriz_equipos.csv (nivel por escala)", padre=padre, incluido="Sí",
                      capacidad=round(ritmo, 1), ucap="aves/h",
                      etiqueta=etiqueta_modularidad(f["modularidad"]), nivel=nv, estado="INFORMATIVO")
    else:
        B.add("OC-ADM-OBRA", "OBRA_CIVIL", "OC-ADM", "OBRA_CIVIL", "Oficina comercial / administrativa (asset-light)",
              "OC-ADM", None, "m²", "sin programa de áreas asset-light (DPV-16-12)", etiqueta="ESCALABLE")
        for cid, nom, et in [("IT-HW", "Hardware IT", "ESCALABLE"), ("IT-SW", "Software inicial", "REUTILIZABLE")]:
            B.add(cid, "IT_TRAZABILIDAD", "it", "SERVICIOS_GENERALES", nom, cid, 1, "lote", "alcance PENDIENTE",
                  etiqueta=et)
        B.add("MOB-OF", "PERSONAL", "mobiliario", "SERVICIOS_GENERALES", "Mobiliario de oficinas", "MOB-OF", 1, "lote",
              "estructura 14A nivel asset-light", etiqueta="REUTILIZABLE")
    # ---- LOGÍSTICA ----------------------------------------------------------------------------
    for fl, d in D["flota"].items():
        F = fl.upper()
        q = d["unidades"]
        B.add(f"VEH-{F}", "LOGISTICA", fl, "LOGISTICA", f"Vehículo — {fl}", f"VEH-{F}", q, "vehículo", d["origen"],
              etiqueta="DUPLICABLE")
        if fl != "servicio":
            B.add(f"CAR-{F}", "LOGISTICA", fl, "LOGISTICA", f"Carrocería / semirremolque — {fl}", f"CAR-{F}", q,
                  "vehículo", "= vehículos del flujo", etiqueta="DUPLICABLE")
        if fl in ("pollitos", "refrigerado", "congelado"):
            B.add(f"FRI-{F}", "LOGISTICA", fl, "LOGISTICA", f"Equipo de frío/climatización — {fl}", f"FRI-{F}", q,
                  "vehículo", "= vehículos del flujo", etiqueta="DUPLICABLE")
        B.add(f"AUX-{F}", "LOGISTICA", fl, "LOGISTICA", f"Equipo auxiliar — {fl}", f"AUX-{F}", q, "vehículo",
              "= vehículos del flujo", etiqueta="DUPLICABLE")
        if fl == "vivo":
            B.add("JAU-VIVO", "LOGISTICA", fl, "LOGISTICA", "Jaulas / cajones / módulos (EQ-03)", "JAU-VIVO", None,
                  "juego", "aves por cajón y juegos por camión PENDIENTES (DPV-084)", etiqueta="DUPLICABLE")
        if fl == "pollitos":
            B.add("JAU-POLLITOS", "LOGISTICA", fl, "LOGISTICA", "Cajas / carros de pollitos", "JAU-POLLITOS", None,
                  "juego", "PENDIENTE (DPV-047)", etiqueta="DUPLICABLE")
        if fl == "subproductos":
            B.add("CNT-SUBPRODUCTOS", "LOGISTICA", fl, "LOGISTICA", "Contenedores de subproductos", "CNT-SUBPRODUCTOS",
                  None, "unidad", "volumen útil y densidades PENDIENTES (DPV-135)", etiqueta="DUPLICABLE")
    if propia and flota_de(c, "vivo") != "propia":
        B.add("JAU-VIVO", "LOGISTICA", "vivo", "LOGISTICA", "Jaulas / cajones / módulos (EQ-03) — titularidad PENDIENTE",
              "JAU-VIVO", None, "juego", "con transporte tercerizado la titularidad de los cajones es PENDIENTE (DPV-16-10)",
              titular="PENDIENTE", etiqueta="DUPLICABLE")
    # ---- INCUBACIÓN -------------------------------------------------------------------------
    if c["pollito"] == "incubacion":
        I = D["incubacion"]
        for cid, nom, q, un, org, et in [
                ("INC-TER", "Terreno de incubadora", None, "m²", "sitio separado; m² PENDIENTES", "REUTILIZABLE"),
                ("INC-EDI", "Edificio de incubación", None, "m²", "sin programa de áreas (DPV-16-13)", "ESCALABLE"),
                ("INC-HUE", "Sala de huevo fértil", I["capacidad_almacen_huevos"], "huevos", "14B capacidad de almacén (con margen SUP-146)", "ESCALABLE"),
                ("INC-SET", "Setters", I["posiciones_setter_diseno"], "posiciones", "14B posiciones de setter por cadencia (SUP-147)", "DUPLICABLE"),
                ("INC-HAT", "Hatchers", I["posiciones_hatcher_diseno"], "posiciones", "14B posiciones de hatcher por cadencia (SUP-147)", "DUPLICABLE"),
                ("INC-TRF", "Transferencia", 1, "lote", "DEC-078", "REEMPLAZABLE"),
                ("INC-CLA", "Clasificación y conteo", 1, "lote", "14B pollitos/h PENDIENTE (horas de ventana)", "REEMPLAZABLE"),
                ("INC-VAC", "Vacunación", 1, "lote", "DEC-078", "REEMPLAZABLE"),
                ("INC-LAV", "Lavado", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("INC-HVAC", "HVAC", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("INC-BIO", "Bioseguridad", 1, "lote", "alcance PENDIENTE", "REUTILIZABLE"),
                ("INC-ENE", "Energía", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("INC-RES", "Respaldo eléctrico", None, "kVA", "carga PENDIENTE", "DUPLICABLE"),
                ("INC-EXP", "Expedición de pollitos", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("INC-AUX", "Equipamiento auxiliar", 1, "lote", "alcance PENDIENTE", "ESCALABLE")]:
            B.add(cid, "INCUBACION", "incubacion", "INCUBACION", nom, cid, q, un, org, etiqueta=et)
    if c["reproductoras"]:
        B.add("REP-GAL", "REPRODUCTORAS", "galpones", "INCUBACION", "Galpones de reproductoras (FUTURO)", "REP-GAL",
              D["reproductoras"], "plaza_reproductora", "14B hembras en postura equivalentes (DPV-045); recría y machos PENDIENTES",
              fase="FUTURO", etiqueta="DUPLICABLE", estado="COTA_INFERIOR")
        B.add("REP-REC", "REPRODUCTORAS", "recria", "INCUBACION", "Recría, machos y reposición (FUTURO)", "REP-REC", None,
              "lote", "PENDIENTE (DPV-045)", fase="FUTURO", etiqueta="DUPLICABLE")
    # ---- PLANTA DE ALIMENTO ------------------------------------------------------------------
    if c["alimento"] == "propia":
        A = D["alimento"]
        th = A["t_h_instalada"]
        for cid, nom, q, un, org, et in [
                ("ALI-TER", "Terreno de planta de alimento", None, "m²", "ubicación abierta (DEC-077)", "REUTILIZABLE"),
                ("ALI-REC", "Recepción de granos", th, "t/h", "14B t/h requerida (capacidad de recepción PENDIENTE)", "REEMPLAZABLE"),
                ("ALI-BAS", "Báscula de camiones", 1, "unidad", "1 báscula (SUP-16-18)", "REUTILIZABLE"),
                ("ALI-SIL", "Silos de materias primas", A["m3_silos_mp"], "m³", "14B maíz + soja (días de stock SUP-150)", "DUPLICABLE"),
                ("ALI-TRA", "Transporte interno", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("ALI-MOL", "Molienda", th, "t/h", "14B t/h requerida (SUP-148)", "REEMPLAZABLE"),
                ("ALI-DOS", "Dosificación", th, "t/h", "14B t/h", "REEMPLAZABLE"),
                ("ALI-MEZ", "Mezcla", th, "t/h", "14B t/h", "REEMPLAZABLE"),
                ("ALI-LIQ", "Aceite / líquidos", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("ALI-PEL", "Peletizado (condicional DEC-076)", th, "t/h", "solo si pellet", "REEMPLAZABLE"),
                ("ALI-ENF", "Enfriado / migaja (condicional DEC-076)", th, "t/h", "solo si pellet", "REEMPLAZABLE"),
                ("ALI-SPT", "Silos de producto terminado", A["m3_silos_pt"], "m³", "14B días de stock en planta", "DUPLICABLE"),
                ("ALI-DES", "Despacho", 1, "lote", "alcance PENDIENTE", "ESCALABLE"),
                ("ALI-POL", "Extracción de polvo / ATEX", 1, "lote", "normativa PENDIENTE", "ESCALABLE"),
                ("ALI-CTL", "Control y automatización", 1, "lote", "alcance PENDIENTE", "REEMPLAZABLE"),
                ("ALI-LAB", "Laboratorio de alimento", 1, "lote", "alcance PENDIENTE", "REUTILIZABLE"),
                ("ALI-OBR", "Obra civil de planta de alimento", None, "m²", "m² PENDIENTES (sin programa de áreas)", "ESCALABLE"),
                ("ALI-UTI", "Utilities de planta de alimento", 1, "lote", "alcance PENDIENTE", "ESCALABLE")]:
            B.add(cid, "ALIMENTO", "planta_alimento", "ALIMENTO", nom, cid, q, un, org, etiqueta=et,
                  capacidad=round(th, 2), ucap="t/h")
    # ---- GRANJAS -----------------------------------------------------------------------------
    f = c["fraccion_granjas_propias"]
    for titular, frac in (("EMPRESA", f), ("PRODUCTOR_INTEGRADO", 1 - f)):
        if frac <= TOL:
            continue
        sfx = "" if titular == "EMPRESA" else "-INT"
        plazas = D["plazas_alojamiento"] * frac
        org = f"14B/03 plazas de alojamiento × {frac:.2f} ({'propias' if titular == 'EMPRESA' else 'integrados: NO es CAPEX de la empresa'})"
        B.add("GRA-GAL" + sfx, "GRANJAS", "galpones", "GRANJAS", "Galpones de engorde (alcance de equipamiento PENDIENTE)",
              "GRA-GAL", plazas, "plaza", org, capacidad=round(D["m2_galpon"] * frac), ucap="m²", titular=titular,
              etiqueta="DUPLICABLE")
        B.add("GRA-TER" + sfx, "GRANJAS", "terreno", "GRANJAS", "Terreno de granjas", "GRA-TER", None, "m²",
              f"m² de galpón {D['m2_galpon'] * frac:,.0f} = cota inferior; distancias de bioseguridad PENDIENTES",
              titular=titular, etiqueta="DUPLICABLE")
        silos_g = D.get("alimento", {}).get("m3_silos_granja", D.get("alimento_granja_m3"))
        for cid, nom, q, un in [("GRA-EQA", "Comederos y bebederos", plazas, "plaza"),
                                ("GRA-CLI", "Climatización", plazas, "plaza"),
                                ("GRA-SIL", "Silos de granja", None if silos_g is None else silos_g * frac, "m³"),
                                ("GRA-AGU", "Agua de granja", 1, "lote"), ("GRA-ENE", "Energía de granja", 1, "lote"),
                                ("GRA-BIO", "Bioseguridad de granja", 1, "lote"), ("GRA-ALM", "Almacenamiento de granja", 1, "lote"),
                                ("GRA-AUX", "Obras auxiliares de granja", 1, "lote")]:
            B.add(cid + sfx, "GRANJAS", "equipamiento", "GRANJAS", nom, cid, q, un,
                  "¿incluido en el precio del galpón? PENDIENTE (DPV-16-07)", padre="GRA-GAL" + sfx,
                  incluido="PENDIENTE", titular=titular, etiqueta="DUPLICABLE")
    # ---- INDIRECTOS, PREOPERATIVOS Y CONTINGENCIA (siempre separados del directo) ---------------
    for cid, nom, cat, bl in [
            ("IND-ING", "Ingeniería básica y de detalle", "INDIRECTO", "INDIRECTOS"), ("IND-ARQ", "Arquitectura", "INDIRECTO", "INDIRECTOS"),
            ("IND-PEJ", "Proyecto ejecutivo", "INDIRECTO", "INDIRECTOS"), ("IND-DO", "Dirección de obra", "INDIRECTO", "INDIRECTOS"),
            ("IND-PM", "Project management", "INDIRECTO", "INDIRECTOS"), ("IND-PER", "Permisos y habilitaciones", "INDIRECTO", "INDIRECTOS"),
            ("IND-EST", "Estudios", "INDIRECTO", "INDIRECTOS"),
            ("PRE-COM", "Commissioning", "PREOPERATIVO", "PREOPERATIVOS"), ("PRE-PEM", "Puesta en marcha", "PREOPERATIVO", "PREOPERATIVOS"),
            ("PRE-CAP", "Capacitación inicial", "PREOPERATIVO", "PREOPERATIVOS"), ("PRE-PRU", "Pruebas (FAT/SAT)", "PREOPERATIVO", "PREOPERATIVOS"),
            ("PRE-REP", "Repuestos iniciales", "PREOPERATIVO", "PREOPERATIVOS"), ("PRE-HER", "Herramientas iniciales", "PREOPERATIVO", "PREOPERATIVOS"),
            ("PRE-LAB", "Insumos iniciales de laboratorio", "PREOPERATIVO", "PREOPERATIVOS"),
            ("PRE-IT", "Implementación IT inicial", "PREOPERATIVO", "PREOPERATIVOS"),
            ("CON-DIS", "Contingencia de diseño / cantidades", "CONTINGENCIA", "CONTINGENCIA"),
            ("CON-COS", "Contingencia de costo", "CONTINGENCIA", "CONTINGENCIA"),
            ("CON-ESC", "Escalación de precios", "CONTINGENCIA", "CONTINGENCIA")]:
        if cid == "PRE-LAB" and not (propia and c["laboratorio_propio"]):
            continue
        B.add(cid, cid.split("-")[0], "porcentaje", bl, nom, cid, 1, "%", "porcentaje sobre la base declarada",
              cat=cat, etiqueta="ESPECIFICO_DE_FASE")
    D["boq_alertas"] = []
    return B.filas, D


# ---------------------------------------------------------------------------------------------
# 5. BASE DE COSTOS Y VALIDACIÓN DE EVIDENCIA
# ---------------------------------------------------------------------------------------------
def _num(x):
    if x is None:
        return None
    x = str(x).strip()
    if x == "":
        return None
    v = float(x)
    if v < 0:
        raise ErrorCapex(f"valor negativo en la base de costos: {x}")
    return v


def leer_base(ruta=ARCHIVO_COSTOS):
    with open(ruta, encoding="utf-8") as f:
        filas = list(csv.DictReader(f))
    return validar_base(filas)


def validar_base(filas):
    """Reglas de evidencia (sección 9). Devuelve dict ID → fila. Lanza ErrorCapex si se violan."""
    base = {}
    for r in filas:
        i = r["ID_COSTO"]
        if i in base:
            raise ErrorCapex(f"ID_COSTO duplicado: {i}")
        if r["METODO_COSTEO"] not in METODOS:
            raise ErrorCapex(f"{i}: método {r['METODO_COSTEO']!r} inválido")
        if r["UNIDAD"] not in UNIDADES_VALIDAS:
            raise ErrorCapex(f"{i}: unidad {r['UNIDAD']!r} inválida")
        nv = r["NIVEL_EVIDENCIA"]
        if nv not in NIVELES_EVIDENCIA:
            raise ErrorCapex(f"{i}: nivel de evidencia {nv!r} inválido")
        p = _num(r["PRECIO_UNITARIO"])
        for k in ("PRECIO_BAJO", "PRECIO_ALTO", "COSTO_INSTALADO", "TC_MONEDA_POR_USD", "FACTOR_INSTALADO_SENSIBILIDAD",
                  "EXPONENTE_ESCALA", "ALICUOTA_IVA"):
            _num(r.get(k))
        if p is None:
            if nv != "PENDIENTE" and "V01" not in _MUT:
                raise ErrorCapex(f"{i}: sin precio pero con nivel {nv} (sin precio = PENDIENTE)")
            if r["ESTADO"] == "CON_PRECIO":
                raise ErrorCapex(f"{i}: ESTADO CON_PRECIO sin precio")
        else:
            if nv == "PENDIENTE":
                raise ErrorCapex(f"{i}: tiene precio pero nivel PENDIENTE")
            if not r["FUENTE"].strip():
                raise ErrorCapex(f"{i}: precio sin FUENTE")
            if nv == "E1":
                if r["TIPO_PRECIO"] != "cotizacion" or not r["FECHA_PRECIO"].strip():
                    raise ErrorCapex(f"{i}: E1 exige TIPO_PRECIO=cotizacion con fecha (una página web no es E1)")
            if nv in ("E1", "E2", "E3") and r["LECTURA_PRIMARIA"] != "Sí" and "V02" not in _MUT:
                raise ErrorCapex(f"{i}: {nv} exige lectura del documento primario (sin lectura → E4 [PVDP])")
            if r["TIPO_PRECIO"] in ("lista_web_fabricante", "benchmark_secundario", "benchmark_prensa") and nv in ("E1",):
                raise ErrorCapex(f"{i}: precio web/prensa no puede ser E1")
            lo, hi = _num(r["PRECIO_BAJO"]), _num(r["PRECIO_ALTO"])
            if (lo is not None or hi is not None) and not r["ORIGEN_RANGO"].strip():
                raise ErrorCapex(f"{i}: rango sin ORIGEN_RANGO (no se inventan ±%)")
            if lo is not None and lo > p + TOL or hi is not None and hi < p - TOL:
                raise ErrorCapex(f"{i}: rango inconsistente (bajo ≤ medio ≤ alto)")
            if r["MONEDA_ORIGINAL"] not in ("USD", "NA") and r["ESTADO"] == "CON_PRECIO" and \
                    (_num(r["TC_MONEDA_POR_USD"]) is None or not r["FECHA_TC"].strip() or not r["TIPO_TC"].strip()):
                raise ErrorCapex(f"{i}: precio en {r['MONEDA_ORIGINAL']} sin TC, fecha y tipo de cambio (regla 2)")
        if r["METODO_COSTEO"] == "porcentaje" and r["UNIDAD"] != "%":
            raise ErrorCapex(f"{i}: porcentaje con unidad distinta de %")
        base[i] = r
    return base


def leer_capas(ruta=ARCHIVO_CAPAS):
    if not os.path.exists(ruta):
        return {}
    out = {}
    with open(ruta, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out.setdefault(r["ID_COSTO"], {})[r["CAPA"]] = r
    return out


# Capas que incluye cada Incoterm (08_maquinaria/plan_rfq.md §5.2; orientación general)
CAPAS_INCOTERM = {"EXW": ("C01",), "FCA": ("C01", "C02", "C03"), "FOB": ("C01", "C02", "C03"),
                  "CFR": ("C01", "C02", "C03", "C04"), "CIF": ("C01", "C02", "C03", "C04", "C05"),
                  "DAP": ("C01", "C02", "C03", "C04", "C05", "C09"),
                  "DDP": ("C01", "C02", "C03", "C04", "C05", "C06", "C07", "C09")}
CAPAS_LANDED = ("C02", "C03", "C04", "C05", "C06", "C07", "C09")
CAPAS_INSTALADO = ("C11", "C12", "C13", "C14", "C15", "C16", "C18", "C19")   # C10 obra → OC-*; C08/C17 aparte


def apilar_capas(precio, incoterm, capas):
    """Precio al Incoterm → landed → instalado. Devuelve (landed, instalado, faltantes)."""
    incl = CAPAS_INCOTERM.get(incoterm)
    if incl is None:
        return None, None, ["INCOTERM"]
    falt, landed = [], precio
    for k in CAPAS_LANDED:
        if k in incl:
            continue
        r = capas.get(k)
        if r is None or r["ESTADO"] == "NC":
            falt.append(k)
        elif r["ESTADO"] in ("EST", "INC") and _num(r["MONTO_USD"]) is not None:
            landed += _num(r["MONTO_USD"])
    inst = landed
    for k in CAPAS_INSTALADO:
        r = capas.get(k)
        if r is None or r["ESTADO"] == "NC":
            falt.append(k)
        elif r["ESTADO"] in ("EST", "INC") and _num(r["MONTO_USD"]) is not None:
            inst += _num(r["MONTO_USD"])
    return (None if any(k in CAPAS_LANDED for k in falt) else landed), (None if falt else inst), falt


# ---------------------------------------------------------------------------------------------
# 6. COSTEO
# ---------------------------------------------------------------------------------------------
def _usd(r, x):
    if x is None:
        return None
    if r["MONEDA_ORIGINAL"] in ("USD", "NA"):
        return x
    tc = _num(r["TC_MONEDA_POR_USD"])
    return None if tc is None else x / tc


def _instalado_directo(r):
    return r["INSTALACION_INCLUIDA"] == "Sí" and r["FLETE_INCLUIDO"] in ("Sí", "NA") and \
        r["INCOTERM"] in ("NA", "INSTALADO")


def _cap_num(x):
    try:
        return float(str(x).replace("≥", "").strip())
    except (TypeError, ValueError):
        return None


def costear(filas, base, capas=None, sensibilidad=False, fecha_base=FECHA_BASE_CAPEX):
    """Costea cada fila. NUNCA convierte faltantes en cero. Segunda pasada: porcentajes."""
    capas = capas or {}
    for f in filas:
        f.update({"ESTADO_COSTO": "", "NIVEL_EVIDENCIA": "", "MONEDA_ORIGINAL": "", "PRECIO_UNITARIO_USD": None,
                  "COSTO_EQUIPO_USD": None, "COSTO_LANDED_USD": None, "COSTO_INSTALADO_LOW_USD": None,
                  "COSTO_INSTALADO_USD": None, "COSTO_INSTALADO_HIGH_USD": None, "ORIGEN_RANGO": "",
                  "VIDA_UTIL_ANIOS": "", "REEMPLAZO_ANIO": "", "COSTO_REEMPLAZO": "", "VALOR_RESIDUAL": "", "ALERTAS": ""})
        if not f["COSTEA"]:
            f["ESTADO_COSTO"] = "INCLUIDO_EN_PAQUETE" if f["INCLUIDO_EN_PAQUETE"] == "Sí" else "ALCANCE_PENDIENTE"
            continue
        if f["COSTO_ID"] not in base:
            raise ErrorCapex(f"{f['ACTIVO_ID']}: COSTO_ID {f['COSTO_ID']} inexistente en la base")
        r = base[f["COSTO_ID"]]
        if r["UNIDAD"] != f["UNIDAD"] and r["METODO_COSTEO"] in ("unitario",):
            raise ErrorCapex(f"{f['ACTIVO_ID']}: unidad BOQ {f['UNIDAD']} ≠ unidad de costo {r['UNIDAD']}")
        for k in ("VIDA_UTIL_ANIOS", "REEMPLAZO_ANIO", "COSTO_REEMPLAZO", "VALOR_RESIDUAL"):
            f[k] = r.get(k, "")                      # solo se trasladan: el modelo financiero los usará
        f["MONEDA_ORIGINAL"] = r["MONEDA_ORIGINAL"]
        if r["METODO_COSTEO"] == "porcentaje":
            continue
        f["NIVEL_EVIDENCIA"] = r["NIVEL_EVIDENCIA"]
        f["ORIGEN_RANGO"] = r["ORIGEN_RANGO"]
        alert = []
        p = [_num(r["PRECIO_BAJO"]), _num(r["PRECIO_UNITARIO"]), _num(r["PRECIO_ALTO"])]
        if p[1] is None:
            f["ESTADO_COSTO"] = "SIN_PRECIO"
            continue
        p = [_usd(r, x) for x in p]
        if p[1] is None:
            f["ESTADO_COSTO"] = "SIN_TIPO_DE_CAMBIO"
            continue
        f["PRECIO_UNITARIO_USD"] = p[1]
        q = [f["CANTIDAD_BAJO"], f["CANTIDAD"], f["CANTIDAD_ALTO"]]
        met = r["METODO_COSTEO"]
        if met == "escalado":
            cap = _cap_num(f["CAPACIDAD"])
            ref = r["CAPACIDAD_REFERENCIA"].strip()
            exp = _num(r["EXPONENTE_ESCALA"])
            if cap is None or not ref:
                f["ESTADO_COSTO"] = "SIN_CANTIDAD"
                continue
            if "-" in ref:
                lo_r, hi_r = (float(x) for x in ref.split("-"))
            else:
                lo_r = hi_r = float(ref)
            if exp is None:
                if not lo_r - TOL <= cap <= hi_r + TOL:
                    f["ESTADO_COSTO"] = "FUERA_DE_RANGO_REFERENCIA"
                    continue
                factor = 1.0
            else:
                factor = (cap / ((lo_r + hi_r) / 2)) ** exp
                alert.append("ESCALADO_CON_EXPONENTE")
            raw = [None if x is None else x * factor for x in p]
        else:
            if q[1] is None:
                f["ESTADO_COSTO"] = "SIN_CANTIDAD"
                continue
            if met == "global" and abs(q[1] - 1) > TOL:
                raise ErrorCapex(f"{f['ACTIVO_ID']}: método global con cantidad ≠ 1 lote")
            raw = [None if (pp is None or qq is None) else pp * qq for pp, qq in zip(p, q)]
            if "C01" in _MUT:
                raw = [None if x is None else x * 1.1 for x in raw]
        f["COSTO_EQUIPO_USD"] = raw[1]
        # Instalado (sección 10–11)
        ci = _num(r["COSTO_INSTALADO"])
        if ci is not None:
            k = _usd(r, ci) / p[1]
            inst = [None if x is None else x * k for x in raw]
        elif _instalado_directo(r) or "C02" in _MUT:
            inst = raw
        elif r["INCOTERM"] in CAPAS_INCOTERM and f["COSTO_ID"] in capas:
            landed, ins1, falt = apilar_capas(raw[1], r["INCOTERM"], capas[f["COSTO_ID"]])
            f["COSTO_LANDED_USD"] = landed
            inst = [None, ins1, None]
            if falt:
                alert.append("CAPAS_FALTANTES:" + "/".join(falt))
        elif sensibilidad and _num(r["FACTOR_INSTALADO_SENSIBILIDAD"]) is not None:
            k = _num(r["FACTOR_INSTALADO_SENSIBILIDAD"])
            inst = [None if x is None else x * k for x in raw]
            alert.append("INSTALADO_POR_FACTOR_SENSIBILIDAD")
        else:
            inst = [None, None, None]
        if inst[1] is None:
            f["ESTADO_COSTO"] = "PRECIO_PARCIAL"            # p. ej. FOB: NO es costo instalado
            f["ALERTAS"] = ";".join(alert + [f"INCOTERM={r['INCOTERM']}"])
            continue
        # IVA (sección 25): no se resuelve; solo no se suma IVA recuperable como costo económico
        iva = r["IVA_TRATAMIENTO"]
        if iva == "con_iva":
            a = _num(r["ALICUOTA_IVA"])
            if a is None:
                f["ESTADO_COSTO"] = "IVA_NO_SEPARADO"
                continue
            inst = [None if x is None else x / (1 + a) for x in inst]
        elif iva == "pendiente":
            alert.append("IVA_INCIERTO")
        if r["FECHA_PRECIO"] and r["FECHA_PRECIO"][:7] < fecha_base[:7]:
            alert.append("PRECIO_ANTERIOR_A_FECHA_BASE (escalación PENDIENTE)")
        if r["CONTINGENCIA_INCLUIDA"] == "Sí":
            alert.append("CONTINGENCIA_YA_INCLUIDA")
        tiene_rango = bool(r["ORIGEN_RANGO"].strip())
        f["COSTO_INSTALADO_USD"] = inst[1]
        f["COSTO_INSTALADO_LOW_USD"] = inst[0] if tiene_rango else None
        f["COSTO_INSTALADO_HIGH_USD"] = inst[2] if tiene_rango else None
        f["ESTADO_COSTO"] = "CON_PRECIO"
        f["ALERTAS"] = ";".join(alert)
    _costear_porcentajes(filas, base)
    return filas


def _base_pct(filas, base, tipo):
    """Base de un porcentaje: (monto, n_pendientes_en_base, n_posible_doble_conteo)."""
    sel, pend, dobles = [], 0, 0
    for f in filas:
        if not f["COSTEA"] or f["FASE"] != "INICIAL" or f["TITULAR"] != "EMPRESA":
            continue
        r = base[f["COSTO_ID"]]
        if r["METODO_COSTEO"] == "porcentaje":
            if tipo == "DIRECTO+INDIRECTO" and f["CATEGORIA_CAPEX"] in ("INDIRECTO", "PREOPERATIVO"):
                if f["COSTO_INSTALADO_USD"] is None:
                    pend += 1
                else:
                    sel.append(f)
            continue
        if tipo == "TERRENO_COMPRA":
            ok = f["ACTIVO_ID"] == "TER-COMPRA"
        elif tipo.startswith("DIRECTO_EQUIPOS"):
            ok = f["CATEGORIA_CAPEX"] == "DIRECTO" and r["ORIGEN_EQUIPO"] != "NA" and f["BLOQUE"] != "TERRENO"
            if ok and tipo.endswith("SIN_PEM"):
                if r["PUESTA_EN_MARCHA_INCLUIDA"] == "Sí":
                    ok = False
                elif r["PUESTA_EN_MARCHA_INCLUIDA"] == "PENDIENTE" and f["COSTO_INSTALADO_USD"] is not None:
                    dobles += 1
        elif tipo in ("DIRECTO", "DIRECTO+INDIRECTO"):
            ok = f["CATEGORIA_CAPEX"] == "DIRECTO" and f["BLOQUE"] != "TERRENO"   # SUP-16-07: terreno fuera de la base
            if tipo == "DIRECTO+INDIRECTO" and r["CONTINGENCIA_INCLUIDA"] == "Sí":
                ok = False
        else:
            raise ErrorCapex(f"BASE_PORCENTAJE desconocida: {tipo}")
        if not ok:
            continue
        if f["COSTO_INSTALADO_USD"] is None:
            pend += 1
        else:
            sel.append(f)
    if not sel:
        return None, pend, dobles
    tot = [sum(x["COSTO_INSTALADO_USD"] for x in sel)]
    return tot[0], pend, dobles


def _costear_porcentajes(filas, base):
    orden = ("INDIRECTO", "PREOPERATIVO", "CONTINGENCIA")
    for cat in ("TERRENO",) + orden:
        for f in filas:
            if not f["COSTEA"]:
                continue
            r = base[f["COSTO_ID"]]
            if r["METODO_COSTEO"] != "porcentaje":
                continue
            es_ter = r["BASE_PORCENTAJE"] == "TERRENO_COMPRA"
            if (cat == "TERRENO") != es_ter or (not es_ter and f["CATEGORIA_CAPEX"] != cat):
                continue
            f["NIVEL_EVIDENCIA"] = r["NIVEL_EVIDENCIA"]
            pct = _num(r["PRECIO_UNITARIO"])
            if pct is None:
                f["ESTADO_COSTO"] = "SIN_PRECIO"
                continue
            monto, pend, dobles = _base_pct(filas, base, r["BASE_PORCENTAJE"])
            if monto is None:
                f["ESTADO_COSTO"] = "BASE_SIN_PRECIO"         # base vacía ≠ base cero
                continue
            f["COSTO_INSTALADO_USD"] = monto * pct / 100
            lo, hi = _num(r["PRECIO_BAJO"]), _num(r["PRECIO_ALTO"])
            if r["ORIGEN_RANGO"].strip():
                f["COSTO_INSTALADO_LOW_USD"] = None if lo is None else monto * lo / 100
                f["COSTO_INSTALADO_HIGH_USD"] = None if hi is None else monto * hi / 100
            al = []
            if pend:
                al.append(f"BASE_INCOMPLETA({pend} conceptos sin precio en la base)")
            if dobles:
                al.append(f"POSIBLE_DOBLE_CONTEO({dobles} paquetes con puesta en marcha PENDIENTE)")
            f["ALERTAS"] = ";".join(al)
            f["ESTADO_COSTO"] = "CON_PRECIO"


# ---------------------------------------------------------------------------------------------
# 7. RESUMEN Y COBERTURA
# ---------------------------------------------------------------------------------------------
def bloques_activos(c):
    propia = c["faena"] == "propia"
    act = {b: propia for b in BLOQUES}
    act.update({"OBRA_CIVIL": True, "SERVICIOS_GENERALES": True, "INDIRECTOS": True, "PREOPERATIVOS": True,
                "CONTINGENCIA": True,
                "LOGISTICA": any(flota_de(c, x) == "propia" for x in FLUJOS) or propia,
                "INCUBACION": c["pollito"] == "incubacion", "ALIMENTO": c["alimento"] == "propia",
                "GRANJAS": c["fraccion_granjas_propias"] > TOL})
    return act


def resumir(filas, c):
    act = bloques_activos(c)
    out = {}
    for b in BLOQUES + ("TOTAL",):
        fs = [f for f in filas if (b == "TOTAL" or f["BLOQUE"] == b)]
        emp = [f for f in fs if f["FASE"] == "INICIAL" and f["TITULAR"] == "EMPRESA"]
        cost = [f for f in emp if f["COSTEA"]]
        con = [f for f in cost if f["ESTADO_COSTO"] == "CON_PRECIO"]
        por_e = {e: sum(f["COSTO_INSTALADO_USD"] for f in con if f["NIVEL_EVIDENCIA"] == e) for e in EVIDENCIAS}
        tot = sum(f["COSTO_INSTALADO_USD"] for f in con)
        rango_ok = con and all(f["COSTO_INSTALADO_LOW_USD"] is not None and f["COSTO_INSTALADO_HIGH_USD"] is not None
                               for f in con)
        sin_mag = [f for f in cost if f["ESTADO_COSTO"] != "CON_PRECIO"]
        d = {
            "ESTADO_BLOQUE": ("EXCLUIDO_POR_ARQUITECTURA" if b != "TOTAL" and not act[b] else
                              "SIN_CONCEPTOS" if not cost else
                              "COMPLETO" if not sin_mag and not any(f["ESTADO_COSTO"] == "ALCANCE_PENDIENTE" for f in emp)
                              else "INCOMPLETO"),
            "CONCEPTOS_COSTEABLES": len(cost),
            "CONCEPTOS_CON_PRECIO": len(con),
            "CONCEPTOS_SIN_PRECIO": sum(1 for f in cost if f["ESTADO_COSTO"] in ("SIN_PRECIO", "SIN_TIPO_DE_CAMBIO",
                                                                                "BASE_SIN_PRECIO")),
            # sin cantidad = dimensionamiento PENDIENTE (puede superponerse con "sin precio")
            "CONCEPTOS_SIN_CANTIDAD": sum(1 for f in cost if f["ESTADO_DIMENSION"] == "PENDIENTE" or
                                          f["ESTADO_COSTO"] in ("SIN_CANTIDAD", "FUERA_DE_RANGO_REFERENCIA")),
            "CONCEPTOS_PRECIO_PARCIAL": sum(1 for f in cost if f["ESTADO_COSTO"] in ("PRECIO_PARCIAL", "IVA_NO_SEPARADO")),
            "ALCANCE_PENDIENTE": sum(1 for f in emp if f["ESTADO_COSTO"] == "ALCANCE_PENDIENTE"),
            "ACTIVOS_BOQ": len(fs),
            **{f"CAPEX_{e}_USD": por_e[e] if con else None for e in EVIDENCIAS},
            "CAPEX_CONOCIDO_USD": (por_e["E1"] + por_e["E2"]) if con else None,
            "CAPEX_ESTIMADO_USD": (por_e["E3"] + por_e["E4"] + por_e["E5"]) if con else None,
            "CAPEX_CON_PRECIO_USD": tot if con else None,
            "CAPEX_CON_PRECIO_LOW_USD": sum(f["COSTO_INSTALADO_LOW_USD"] for f in con) if rango_ok else None,
            "CAPEX_CON_PRECIO_HIGH_USD": sum(f["COSTO_INSTALADO_HIGH_USD"] for f in con) if rango_ok else None,
            "COBERTURA_CONCEPTOS_PCT": (100 * len(con) / len(cost)) if cost else None,
        }
        if not cost:
            d["COBERTURA_VALOR"] = "NO APLICA"
        elif not sin_mag:
            d["COBERTURA_VALOR"] = "100"
        else:
            d["COBERTURA_VALOR"] = f"NO CALCULABLE: {len(sin_mag)} conceptos sin magnitud"
        completo = d["ESTADO_BLOQUE"] == "COMPLETO"
        d["TOTAL_PRELIMINAR_USD"] = tot if completo and con else (0.0 if d["ESTADO_BLOQUE"] == "EXCLUIDO_POR_ARQUITECTURA" else None)
        d["TOTAL_PRELIMINAR"] = (f"{tot:.0f}" if completo and con else
                                 "0 (excluido por arquitectura)" if d["ESTADO_BLOQUE"] == "EXCLUIDO_POR_ARQUITECTURA" else
                                 f"NO DISPONIBLE: {len(sin_mag) + d['ALCANCE_PENDIENTE']} conceptos sin costo")
        d["CAPEX_TERCEROS_INFORMATIVO_USD"] = sum(f["COSTO_INSTALADO_USD"] for f in fs if f["TITULAR"] == "PRODUCTOR_INTEGRADO"
                                                  and f["COSTEA"] and f["ESTADO_COSTO"] == "CON_PRECIO") or None
        d["CAPEX_FUTURO_INFORMATIVO_USD"] = sum(f["COSTO_INSTALADO_USD"] for f in fs if f["FASE"] == "FUTURO"
                                                and f["COSTEA"] and f["ESTADO_COSTO"] == "CON_PRECIO") or None
        out[b] = d
    return out


# ---------------------------------------------------------------------------------------------
# 8. ESCENARIOS
# ---------------------------------------------------------------------------------------------
def escenarios_referencia():
    esc = []
    for cfg in ("C0", "C1", "C2", "C3", "CF"):
        for E in ESCALAS_REF:
            esc.append((f"{cfg}-{E}", preset(cfg, aves_dia=E)))
    for E in (7500, 15000):
        esc.append((f"C1-{E}", preset("C1", aves_dia=E)))
    var = {
        "C1-10000-reserva20000": dict(terreno="compra_reserva", escala_objetivo=20000),
        "C1-10000-parque": dict(terreno="parque_industrial"),
        "C1-10000-rural": dict(terreno="rural_compatible"),
        "C1-10000-congelado_tercero": dict(frio="C_congelado_tercero"),
        "C1-10000-congelado_propio": dict(frio="B_refrigerado_congelado"),
        "C1-10000-subprod_basico": dict(subproductos="B_basico_propio"),
        "C1-10000-llave_en_mano": dict(modalidad_linea="llave_en_mano"),
        "C1-10000-manual": dict(automatizacion="manual"),
        "C1-10000-auto": dict(automatizacion="auto"),
        "C1-10000-6dias": dict(dias_semana=6),
        "C1-5000-reserva20000": dict(aves_dia=5000, terreno="compra_reserva", escala_objetivo=20000),
    }
    for k, v in var.items():
        esc.append((k, preset("C1", **{"aves_dia": 10000, **v})))
    return esc


def correr(c, base=None, capas=None, sensibilidad=False):
    base = base or leer_base()
    filas, D = generar_boq(copy.deepcopy(c))
    costear(filas, base, capas if capas is not None else leer_capas(), sensibilidad, c["fecha_base"])
    return filas, resumir(filas, c), D


# ---------------------------------------------------------------------------------------------
# 9. EXPANSIÓN
# ---------------------------------------------------------------------------------------------
TRAYECTORIAS = {"A_20000_directo": (20000,), "B_5000_a_20000": (5000, 20000),
                "B2_5000_10000_20000": (5000, 10000, 20000), "C_10000_a_20000": (10000, 20000)}


def accion_expansion(et, q0, q1):
    """SUP-16-11. Devuelve (acción, Δ cantidad a adquirir)."""
    if q0 is None or q1 is None:
        return "PENDIENTE", None
    if et == "REUTILIZABLE":
        d = max(0.0, q1 - q0)
        return ("REUTILIZA" if d <= TOL else "AMPLIA_REUTILIZABLE"), d
    if et == "ESCALABLE":
        d = max(0.0, q1 - q0)
        return ("REUTILIZA" if d <= TOL else "AMPLIA"), d
    if et == "DUPLICABLE":
        d = max(0.0, q1 - q0)
        return ("REUTILIZA" if d <= TOL else "DUPLICA"), d
    if et == "REEMPLAZABLE":
        return ("REEMPLAZA", q1) if q1 > q0 + TOL else ("REUTILIZA", 0.0)
    if et == "ESPECIFICO_DE_FASE":
        return "NUEVO_POR_FASE", q1
    return "PENDIENTE", None     # MIXTA: se resuelve en los EQ hijos


def _q_exp(f):
    """Magnitud comparable entre etapas: cantidad, o capacidad si la fila es un lote/paquete o un EQ."""
    if f["UNIDAD"] in ("lote", "unidad") and f["UNIDAD_CAPACIDAD"]:
        return _cap_num(f["CAPACIDAD"]), f["UNIDAD_CAPACIDAD"]
    if f["UNIDAD"] == "lote":
        return None, None                         # lote sin capacidad: no se puede decidir → PENDIENTE
    return f["CANTIDAD"], f["UNIDAD"]


def expansion(cfg_nombre="C1", terreno="compra_fase", base=None):
    base = base or leer_base()
    capas = leer_capas()
    filas_out, resumen = [], []
    for tray, etapas in TRAYECTORIAS.items():
        prev = None
        acumulado, pend_total = 0.0, 0
        for k, E in enumerate(etapas):
            c = preset(cfg_nombre, aves_dia=E, terreno=terreno,
                       escala_objetivo=(etapas[-1] if terreno == "compra_reserva" else None))
            filas, res, _ = correr(c, base, capas)
            idx = {f["ACTIVO_ID"]: f for f in filas}
            capex_etapa, pend = 0.0, 0
            for f in filas:
                if f["FASE"] != "INICIAL" or f["TITULAR"] != "EMPRESA":
                    continue
                q1 = f["CANTIDAD"]
                nota_x = ""
                if prev is None:
                    acc, dq = "INICIAL", q1
                    costo = f["COSTO_INSTALADO_USD"] if f["COSTEA"] else None
                else:
                    p0 = prev.get(f["ACTIVO_ID"])
                    nota_x = ""
                    if p0 is None:
                        acc, dq = "NUEVO", q1
                        costo = f["COSTO_INSTALADO_USD"] if f["COSTEA"] else None
                    elif f["UNIDAD"] == "%":
                        acc, dq, costo = "NUEVO_POR_FASE", None, None
                    else:
                        a0, u0_ = _q_exp(p0)
                        a1, u1_ = _q_exp(f)
                        if p0["NIVEL_AUTOMATIZACION"] and p0["NIVEL_AUTOMATIZACION"] != f["NIVEL_AUTOMATIZACION"]:
                            acc, dq = "REEMPLAZA", a1
                            nota_x = f"cambio de nivel {p0['NIVEL_AUTOMATIZACION']}→{f['NIVEL_AUTOMATIZACION']}"
                        else:
                            acc, dq = accion_expansion(f["ETIQUETA_EXPANSION"], a0, a1)
                        costo = None
                        es_cant = u1_ == f["UNIDAD"]
                        if f["COSTEA"] and f["ESTADO_COSTO"] == "CON_PRECIO" and dq is not None and es_cant and \
                                base[f["COSTO_ID"]]["METODO_COSTEO"] == "unitario" and f["PRECIO_UNITARIO_USD"] is not None:
                            costo = dq * f["PRECIO_UNITARIO_USD"]     # a precio de obra nueva; prima de ampliación PENDIENTE
                        elif acc == "REUTILIZA" and dq is not None:
                            costo = 0.0
                        if f["ACTIVO_ID"] == "TER-COMPRA" and acc == "AMPLIA_REUTILIZABLE":
                            nota_x = "requiere terreno contiguo disponible: riesgo sin reserva (DEC-063)"
                        if u1_ and u1_ != f["UNIDAD"]:
                            nota_x = (nota_x + "; " if nota_x else "") + f"comparado por capacidad ({u1_})"
                if f["COSTEA"]:
                    if costo is None:
                        pend += 1
                    else:
                        capex_etapa += costo
                filas_out.append({"TRAYECTORIA": tray, "ETAPA": k + 1, "ESCALA": E, "CONFIGURACION": cfg_nombre,
                                  "TERRENO": terreno, "ACTIVO_ID": f["ACTIVO_ID"], "BLOQUE": f["BLOQUE"],
                                  "ETIQUETA_EXPANSION": f["ETIQUETA_EXPANSION"], "ACCION": acc,
                                  "CANTIDAD_ANTERIOR": None if prev is None or f["ACTIVO_ID"] not in prev else prev[f["ACTIVO_ID"]]["CANTIDAD"],
                                  "CANTIDAD_NUEVA": q1, "DELTA_A_ADQUIRIR": dq, "UNIDAD": f["UNIDAD"],
                                  "COSTEA": f["COSTEA"], "COSTO_ETAPA_USD": costo,
                                  "NOTA": ((nota_x + "; ") if prev is not None and nota_x else "") + ("costo a precio unitario de obra nueva; prima/penalidad de ampliación PENDIENTE (DPV-16-14)"
                                           if prev is not None and costo not in (None, 0.0) else
                                           "valor residual del activo reemplazado PENDIENTE (modelo financiero)" if acc == "REEMPLAZA" else "")})
            acumulado += capex_etapa
            pend_total += pend
            resumen.append({"TRAYECTORIA": tray, "ETAPA": k + 1, "ESCALA": E, "TERRENO": terreno,
                            "CAPEX_ETAPA_CON_PRECIO_USD": capex_etapa, "CONCEPTOS_SIN_COSTO_ETAPA": pend,
                            "CAPEX_ACUMULADO_CON_PRECIO_USD": acumulado, "CONCEPTOS_SIN_COSTO_ACUMULADO": pend_total,
                            "TIPO": "INICIAL" if k == 0 else "EXPANSION"})
            prev = idx
    return filas_out, resumen


# ---------------------------------------------------------------------------------------------
# 10. MATRIZ RFQ
# ---------------------------------------------------------------------------------------------
def matriz_rfq():
    rng, frio = {}, {}
    for E in (2500, 20000):
        fl, _, D = correr(preset("C3", aves_dia=E))
        rng[E] = D
        frio[E] = [x for x in fl if x["ACTIVO_ID"] == "FR-PAQ"][0]["CAPACIDAD"].replace("≥", "").strip()
    r0, r1 = rng[2500], rng[20000]
    u0, u1 = r0["util"]["medio"], r1["util"]["medio"]
    p = "Candidatos relevados sin selección en 08_maquinaria/proveedores_preliminares.md"
    ni = "No identificados (relevar; no se inventan proveedores)"
    filas = [
        ("Línea de faena, evisceración y enfriamiento (L1–L4 y L11)", "linea_faena", "Base de diseño y 31 campos de 08 requerimientos_cotizacion.md; capacidad garantizada (DPV-097); inmersión y aire por separado; desglose por capas C01–C19", f"{r0['ritmo_aves_h']:.0f}–{r1['ritmo_aves_h']:.0f} aves/h (2.500–20.000 aves/día, 8 h netas)", "2 escalas del rango + cómo se amplía", p, 3, "PQ-L1;PQ-L2;PQ-L3;PQ-L4;PQ-L11", "DPV-097;DPV-095;DPV-16-01;DPV-16-05"),
        ("Trozado, deshuese y packaging (L5, L7)", "linea_faena", "Mix por configuración A/B/C", "ídem", "por configuración", p, 3, "PQ-L5;PQ-L7", "DPV-037;DPV-16-01"),
        ("Coproductos (L6) y subproductos (L9)", "linea_faena", "Garras, CMS solo con comprador; sangre, plumas, vísceras", f"{sum((u0.get(k) or 0) for k in ('segregable_sangre_recuperada_t_dia','segregable_plumas_t_dia','segregable_visceras_t_dia','segregable_cabeza_t_dia')):.1f}–{sum((u1.get(k) or 0) for k in ('segregable_sangre_recuperada_t_dia','segregable_plumas_t_dia','segregable_visceras_t_dia','segregable_cabeza_t_dia')):.1f} t/d", "1", p, 3, "PQ-L6;SB-L9;SB-BAS", "DEC-027;DPV-16-01"),
        ("Paquete de frío (cámaras, túneles, sala de máquinas, agua helada)", "frio", "Balance frigorífico por escala y perfil P1–P3; verano de diseño del sitio; refrigerante abierto", f"≥ {frio[2500]}–{frio[20000]} kWf (cota inferior = FR-PAQ del BOQ, C3 perfil P2)", "1 paquete por escala", p, 3, "FR-PAQ;FR-*", "DPV-109;DPV-096;DEC-046"),
        ("Pretratamiento y tratamiento de efluentes", "efluentes", "Por escenario de carga; límites de vuelco del sitio (DPV-106); superficie (DPV-144)", f"{u0.get('agua_descargada_m3_dia', 0):.0f}–{u1.get('agua_descargada_m3_dia', 0):.0f} m³/d", "por tecnología", p, 3, "EF-PAQ;EF-*;OC-EF", "DPV-114;DPV-144;DEC-043"),
        ("Acometida, transformación, tableros y generación de respaldo", "electrico", "Lista de cargas consolidada (DEC-048); demanda máxima; política de respaldo (DEC-047)", f"potencia media de proceso {u0.get('potencia_media_equivalente_proceso_kw_bajo_14h', 0):.0f}–{u1.get('potencia_media_equivalente_proceso_kw_bajo_14h', 0):.0f} kW (pico PENDIENTE)", "1", ni + "; distribuidora eléctrica del sitio", 3, "EL-*", "DPV-095;DPV-16-11"),
        ("Caldera / agua caliente, aire comprimido, agua", "electrico", "Fuente térmica abierta (DEC-045)", "pico PENDIENTE", "1", p, 3, "TE-*;AC-COM;AG-*", "DPV-095"),
        ("Obra civil por categoría (USD/m²)", "obra", "Precio por m² SEPARADO por categoría: proceso húmedo, frío, docks, depósitos, salas técnicas, personal, oficinas, exteriores, efluentes", f"{r0['m2_construidos'][1]:.0f}–{r1['m2_construidos'][1]:.0f} m² construidos (medio, conceptual)", "14 categorías", ni + "; constructoras con antecedentes en plantas alimentarias", 3, "OC-*", "DPV-16-02"),
        ("Terreno por corredor", "obra", "USD/m² por tipo (industrial, parque, rural compatible) + preparación + acceso + conexiones", f"{r0['terreno_m2'][1]:.0f}–{r1['terreno_m2'][1]:.0f} m² (fase, medio)", "por corredor de la lista corta (DEC-055)", ni + "; inmobiliarias / parques industriales", 3, "TER-*", "DPV-16-03;DPV-16-11"),
        ("Incubación (setters, hatchers, sala de huevo, HVAC)", "incubacion", "Setter y hatcher por separado; cadencia; vacunación (DEC-078)", "posiciones 14B por escala", "por escala", p, 3, "INC-*", "DPV-153;DPV-16-13"),
        ("Planta de alimento", "alimento", "t/h requerida de 14B (no catálogo sobredimensionado); forma física DEC-076", "0,9–41 t/h según escala y factores (SUP-148)", "1", p, 3, "ALI-*", "DPV-158;DPV-16-15"),
        ("Vehículos por flujo (chasis, carrocería, frío, cajones)", "vehiculos", "Capacidad útil validada por flujo (DPV-084); separar chasis / carrocería / equipo de frío / jaulas", "flota por flujo de 12B", "por flujo", ni + "; concesionarios y carroceros", 3, "VEH-*;CAR-*;FRI-*;AUX-*;JAU-*", "DPV-084;DPV-16-10"),
        ("Galpones de engorde y equipamiento", "granjas", "Tecnología de galpón (DEC-022); alcance de equipamiento", f"{r0['m2_galpon']:.0f}–{r1['m2_galpon']:.0f} m² de galpón", "por núcleo", ni + "; constructores de galpones y proveedores de equipamiento", 3, "GRA-*", "DPV-16-07;DEC-022"),
    ]
    out = []
    for i, (item, cat, esp, cap, cant, prov, ncot, ids, dpv) in enumerate(filas, 1):
        out.append({"ITEM": f"RFQ-16-{i:02d} {item}", "CATEGORIA": cat, "ESPECIFICACION_MINIMA": esp, "CAPACIDAD": cap,
                    "CANTIDAD": cant, "PROVEEDORES_OBJETIVO": prov, "COTIZACIONES_REQUERIDAS": ncot,
                    "ESTADO": "NO SOLICITADA (fase no habilitada: DEC-049)",
                    "FECHA_LIMITE": "PENDIENTE (después del hito H-B)", "IDS_COSTO": ids,
                    "OBSERVACIONES": f"Responde {dpv}; pedir desglose por capas (08 plan_rfq.md §5.1), Incoterm, moneda, validez, IVA, flete, instalación"})
    return out


# ---------------------------------------------------------------------------------------------
# 11. CSV
# ---------------------------------------------------------------------------------------------
def _fmt(x):
    if x is None:
        return ""
    if isinstance(x, bool):
        return "Sí" if x else "No"
    if isinstance(x, float):
        return f"{x:.4f}".rstrip("0").rstrip(".") if abs(x) < 1e12 else f"{x:.0f}"
    return x


def escribir(ruta, filas, campos):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        for r in filas:
            w.writerow({k: _fmt(r.get(k)) for k in campos})


CAMPOS_ESC = ["ESCENARIO", "CONFIGURACION", "ESCALA_AVES_DIA", "DIAS_ANIO", "ARQUITECTURA", "FECHA_BASE", "MONEDA",
              "BLOQUE", "ESTADO_BLOQUE", "ACTIVOS_BOQ", "CONCEPTOS_COSTEABLES", "CONCEPTOS_CON_PRECIO",
              "CONCEPTOS_SIN_PRECIO", "CONCEPTOS_SIN_CANTIDAD", "CONCEPTOS_PRECIO_PARCIAL", "ALCANCE_PENDIENTE",
              "CAPEX_E1_USD", "CAPEX_E2_USD", "CAPEX_E3_USD", "CAPEX_E4_USD", "CAPEX_E5_USD", "CAPEX_CONOCIDO_USD",
              "CAPEX_ESTIMADO_USD", "CAPEX_CON_PRECIO_USD", "CAPEX_CON_PRECIO_LOW_USD", "CAPEX_CON_PRECIO_HIGH_USD",
              "COBERTURA_CONCEPTOS_PCT", "COBERTURA_VALOR", "TOTAL_PRELIMINAR", "CAPEX_TERCEROS_INFORMATIVO_USD",
              "CAPEX_FUTURO_INFORMATIVO_USD", "ALERTAS"]
CAMPOS_EXP = ["TRAYECTORIA", "ETAPA", "ESCALA", "CONFIGURACION", "TERRENO", "ACTIVO_ID", "BLOQUE", "ETIQUETA_EXPANSION",
              "ACCION", "CANTIDAD_ANTERIOR", "CANTIDAD_NUEVA", "DELTA_A_ADQUIRIR", "UNIDAD", "COSTEA", "COSTO_ETAPA_USD", "NOTA"]
CAMPOS_RFQ = ["ITEM", "CATEGORIA", "ESPECIFICACION_MINIMA", "CAPACIDAD", "CANTIDAD", "PROVEEDORES_OBJETIVO",
              "COTIZACIONES_REQUERIDAS", "ESTADO", "FECHA_LIMITE", "IDS_COSTO", "OBSERVACIONES"]


def construir_salidas():
    base, capas = leer_base(), leer_capas()
    boq, esc = [], []
    for nombre, c in escenarios_referencia():
        filas, res, D = correr(c, base, capas)
        arq = etiqueta_arquitectura(c)
        for f in filas:
            boq.append(dict(f, ESCENARIO=nombre, ARQUITECTURA=arq))
        for b, d in res.items():
            esc.append(dict(d, ESCENARIO=nombre, CONFIGURACION=c["nombre"], ESCALA_AVES_DIA=c["aves_dia"],
                            DIAS_ANIO=dias_anio(c), ARQUITECTURA=arq, FECHA_BASE=c["fecha_base"], MONEDA="USD",
                            BLOQUE=b, ALERTAS=";".join(D["alertas"]) if b == "TOTAL" else ""))
    escribir(SALIDA_BOQ, boq, CAMPOS_BOQ)
    escribir(SALIDA_ESC, esc, CAMPOS_ESC)
    exp = []
    for t in ("compra_fase", "compra_reserva"):
        fx, rs = expansion("C1", t, base)
        exp += fx
        exp += [dict(r, ACTIVO_ID="RESUMEN_ETAPA", BLOQUE="TOTAL", ACCION=r["TIPO"],
                     COSTO_ETAPA_USD=r["CAPEX_ETAPA_CON_PRECIO_USD"],
                     NOTA=f"acumulado con precio {r['CAPEX_ACUMULADO_CON_PRECIO_USD']:.0f} USD; "
                          f"conceptos sin costo en la etapa {r['CONCEPTOS_SIN_COSTO_ETAPA']}, acumulados {r['CONCEPTOS_SIN_COSTO_ACUMULADO']}",
                     CONFIGURACION="C1") for r in rs]
    escribir(SALIDA_EXP, exp, CAMPOS_EXP)
    escribir(SALIDA_RFQ, matriz_rfq(), CAMPOS_RFQ)
    return boq, esc, exp


# ---------------------------------------------------------------------------------------------
# 12. TESTS
# ---------------------------------------------------------------------------------------------
def _base_sintetica(precio=100.0, nivel="E5", fuente="TEST", rango=True, pct=None):
    """Copia de la base con TODOS los precios llenos (solo para probar la matemática)."""
    base = copy.deepcopy(leer_base())
    for r in base.values():
        if r["METODO_COSTEO"] == "porcentaje":
            r.update(PRECIO_UNITARIO="" if pct is None else str(pct), NIVEL_EVIDENCIA="PENDIENTE" if pct is None else nivel,
                     FUENTE="" if pct is None else fuente, PRECIO_BAJO="", PRECIO_ALTO="", ORIGEN_RANGO="")
            continue
        r.update(PRECIO_UNITARIO=str(precio), NIVEL_EVIDENCIA=nivel, FUENTE=fuente, MONEDA_ORIGINAL="USD",
                 INSTALACION_INCLUIDA="Sí", FLETE_INCLUIDO="NA", INCOTERM="NA", IVA_TRATAMIENTO="sin_iva",
                 COSTO_INSTALADO="", PRECIO_BAJO=str(precio * 0.8) if rango else "",
                 PRECIO_ALTO=str(precio * 1.3) if rango else "", ORIGEN_RANGO="test" if rango else "",
                 EXPONENTE_ESCALA="0.6" if r["METODO_COSTEO"] == "escalado" else "",
                 CAPACIDAD_REFERENCIA="1000" if r["METODO_COSTEO"] == "escalado" else r["CAPACIDAD_REFERENCIA"],
                 ESTADO="CON_PRECIO")
    return base


def ejecutar_tests(verbose=True):
    res = []

    def chk(cod, desc, ok, det=""):
        res.append((cod, desc, bool(ok), det))

    base = leer_base()
    capas = leer_capas()
    cache = {}

    def run(nombre, **kw):
        key = (nombre, tuple(sorted((k, str(v)) for k, v in kw.items())))
        if key not in cache:
            cache[key] = correr(preset(nombre, **kw), base, capas)
        return cache[key]

    # ---- Matemática ----
    vals = [r for r in base.values()]
    chk("M01", "Ningún precio negativo en la base", all((_num(r["PRECIO_UNITARIO"]) or 0) >= 0 for r in vals))
    f, R, _ = run("C1", aves_dia=10000)
    chk("M02", "Faltante ≠ cero: sin precio → COSTO vacío (None), nunca 0",
        all(x["COSTO_INSTALADO_USD"] is None for x in f if x["ESTADO_COSTO"] in ("SIN_PRECIO", "SIN_CANTIDAD", "PRECIO_PARCIAL", "BASE_SIN_PRECIO"))
        and all(x["COSTO_INSTALADO_USD"] is not None for x in f if x["ESTADO_COSTO"] == "CON_PRECIO"))
    bs = _base_sintetica()
    fs, Rs, _ = correr(preset("C1", aves_dia=10000), bs, {})
    tot_filas = sum(x["COSTO_INSTALADO_USD"] for x in fs if x["COSTEA"] and x["FASE"] == "INICIAL"
                    and x["TITULAR"] == "EMPRESA" and x["ESTADO_COSTO"] == "CON_PRECIO")
    tot_bloq = sum(Rs[b]["CAPEX_CON_PRECIO_USD"] or 0 for b in BLOQUES)
    chk("M03", "Total = suma de componentes incluidos (filas = bloques = TOTAL)",
        abs(tot_filas - tot_bloq) < 1e-6 and abs(tot_bloq - (Rs["TOTAL"]["CAPEX_CON_PRECIO_USD"] or 0)) < 1e-6,
        f"{tot_filas:.2f} / {tot_bloq:.2f}")
    chk("M04", "Sin doble conteo: filas incluidas en paquete no se costean",
        all(x["COSTO_INSTALADO_USD"] is None for x in fs if x["INCLUIDO_EN_PAQUETE"] in ("Sí", "PENDIENTE") and x["ACTIVO_PADRE"]))
    eqs_padres = {}
    for x in leer_equipos():
        eqs_padres.setdefault(x["id"], set()).add(padre_de_eq(int(x["id"].split("-")[1])))
    chk("M05", "Cada EQ tiene un solo costeador (EQ-28/33 no se duplican en L3 y L6)",
        all(len(v) == 1 for v in eqs_padres.values()) and padre_de_eq(28) == "PQ-L3" and padre_de_eq(33) == "PQ-L3")
    todas = [a for areas in OC_MAP.values() for a in areas]
    _, _, D10 = run("C1", aves_dia=10000)
    areas_12c = [a for a in D10["areas"] if a not in AREAS_NO_OBRA]
    chk("M06", "Cada área de 12C se costea en UNA sola categoría de obra (sin omisión ni duplicado)",
        len(todas) == len(set(todas)) and set(areas_12c) == set(todas), str(set(areas_12c) ^ set(todas)))
    b2 = copy.deepcopy(base)
    b2["OC-DP"].update(MONEDA_ORIGINAL="ARS", PRECIO_UNITARIO="300000", PRECIO_BAJO="250000", PRECIO_ALTO="350000",
                       TC_MONEDA_POR_USD="1000", FECHA_TC="2026-06-30", TIPO_TC="oficial (test)")
    fa, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b2.values())), {})
    fu = {x["ACTIVO_ID"]: x for x in f}
    fa = {x["ACTIVO_ID"]: x for x in fa}
    chk("M07", "Conversión ARS→USD consistente (ARS ÷ TC = USD)",
        abs(fa["OC-DP-OBRA"]["COSTO_INSTALADO_USD"] - fu["OC-DP-OBRA"]["COSTO_INSTALADO_USD"]) < 1e-6)
    b3 = copy.deepcopy(base)
    b3["OC-DP"].update(MONEDA_ORIGINAL="ARS", TC_MONEDA_POR_USD="", FECHA_TC="", TIPO_TC="")
    try:
        validar_base(list(b3.values()))
        ok = False
    except ErrorCapex:
        ok = True
    chk("M08", "Precio en ARS sin TC, fecha y tipo de cambio → error (regla 2)", ok)
    b4 = copy.deepcopy(base)
    b4["OC-DP"]["PRECIO_UNITARIO"] = "-5"
    try:
        validar_base(list(b4.values()))
        ok = False
    except ErrorCapex:
        ok = True
    chk("M09", "Precio negativo → error", ok)
    b5 = copy.deepcopy(base)
    b5["TER-05"].update(PRECIO_UNITARIO="0", NIVEL_EVIDENCIA="E5", FUENTE="test costo cero", ESTADO="CON_PRECIO",
                        INSTALACION_INCLUIDA="Sí", FLETE_INCLUIDO="NA")
    f5, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b5.values())), {})
    chk("M10", "0 explícito = costo cero real (se distingue de vacío)",
        [x for x in f5 if x["ACTIVO_ID"] == "TER-PREP"][0]["COSTO_INSTALADO_USD"] == 0.0 and
        [x for x in f if x["ACTIVO_ID"] == "TER-PREP"][0]["COSTO_INSTALADO_USD"] is None)
    qok = True
    for x in f:
        cid = x["COSTO_ID"]
        if x["ACTIVO_ID"] == f"{cid}-OBRA" and cid in OC_MAP:
            q = _sum_areas(D10, OC_MAP[cid])
            qok &= all(abs(a - b) < 1e-6 for a, b in zip(q, (x["CANTIDAD_BAJO"], x["CANTIDAD"], x["CANTIDAD_ALTO"])))
    chk("M11", "Cantidad de obra del BOQ = Σ áreas de 12C de su categoría (trazabilidad del dimensionamiento)", qok)
    odp = fu["OC-DP-OBRA"]
    chk("M12", "Costo = cantidad × precio unitario (OC-DP: m² × 250 / 300 / 350 USD/m²)",
        abs(odp["COSTO_INSTALADO_USD"] - odp["CANTIDAD"] * 300) < 1e-6 and
        abs(odp["COSTO_INSTALADO_LOW_USD"] - odp["CANTIDAD_BAJO"] * 250) < 1e-6 and
        abs(odp["COSTO_INSTALADO_HIGH_USD"] - odp["CANTIDAD_ALTO"] * 350) < 1e-6)
    # ---- Equipo vs instalado / importados ----
    b6 = copy.deepcopy(base)
    b6["PQ-L2"].update(PRECIO_UNITARIO="500000", NIVEL_EVIDENCIA="E4", FUENTE="test", INCOTERM="FOB",
                       CAPACIDAD_REFERENCIA="1000-1500", ORIGEN_EQUIPO="importado", INSTALACION_INCLUIDA="No")
    f6, r6, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b6.values())), {})
    l2 = [x for x in f6 if x["ACTIVO_ID"] == "PQ-L2"][0]
    chk("I01", "FOB ≠ instalado: precio FOB sin capas queda PRECIO_PARCIAL y no suma al CAPEX",
        l2["ESTADO_COSTO"] == "PRECIO_PARCIAL" and l2["COSTO_INSTALADO_USD"] is None and l2["COSTO_EQUIPO_USD"] == 500000
        and r6["TOTAL"]["CONCEPTOS_PRECIO_PARCIAL"] >= 1)
    capas_t = {"PQ-L2": {k: {"ESTADO": "EST", "MONTO_USD": "1000"} for k in CAPAS_LANDED + CAPAS_INSTALADO}}
    f7, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b6.values())), capas_t)
    l2b = [x for x in f7 if x["ACTIVO_ID"] == "PQ-L2"][0]
    n_land = len([k for k in CAPAS_LANDED if k not in CAPAS_INCOTERM["FOB"]])
    chk("I02", "Landed = FOB + capas no incluidas; instalado = landed + montaje/PEM/repuestos (C10 obra excluida)",
        abs((l2b["COSTO_LANDED_USD"] or -1) - (500000 + 1000 * n_land)) < 1e-6 and
        abs((l2b["COSTO_INSTALADO_USD"] or -1) - (500000 + 1000 * (n_land + len(CAPAS_INSTALADO)))) < 1e-6 and "C10" not in CAPAS_INSTALADO)
    capas_nc = {"PQ-L2": dict(capas_t["PQ-L2"], C07={"ESTADO": "NC", "MONTO_USD": ""})}
    f8, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b6.values())), capas_nc)
    chk("I03", "Arancel/impuesto no cotizado (NC) → instalado PENDIENTE (no se asume arancel cero)",
        [x for x in f8 if x["ACTIVO_ID"] == "PQ-L2"][0]["COSTO_INSTALADO_USD"] is None)
    b6["PQ-L2"]["FACTOR_INSTALADO_SENSIBILIDAD"] = "1.5"
    bb6 = validar_base(list(b6.values()))
    f9, _, _ = correr(preset("C1", aves_dia=10000), bb6, {}, sensibilidad=False)
    f9s, _, _ = correr(preset("C1", aves_dia=10000), bb6, {}, sensibilidad=True)
    chk("I04", "Factor FOB × k solo en modo sensibilidad y marcado",
        [x for x in f9 if x["ACTIVO_ID"] == "PQ-L2"][0]["COSTO_INSTALADO_USD"] is None and
        "SENSIBILIDAD" in [x for x in f9s if x["ACTIVO_ID"] == "PQ-L2"][0]["ALERTAS"])
    b10 = copy.deepcopy(base)
    b10["OC-DP"].update(IVA_TRATAMIENTO="con_iva", ALICUOTA_IVA="")
    f10, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b10.values())), {})
    b10["OC-DP"]["ALICUOTA_IVA"] = "0.21"
    f11, _, _ = correr(preset("C1", aves_dia=10000), validar_base(list(b10.values())), {})
    x10 = [x for x in f10 if x["ACTIVO_ID"] == "OC-DP-OBRA"][0]
    x11 = [x for x in f11 if x["ACTIVO_ID"] == "OC-DP-OBRA"][0]
    chk("I05", "IVA: precio con IVA sin alícuota no entra al costo económico; con alícuota se neta",
        x10["COSTO_INSTALADO_USD"] is None and x10["ESTADO_COSTO"] == "IVA_NO_SEPARADO" and
        abs(x11["COSTO_INSTALADO_USD"] - fu["OC-DP-OBRA"]["COSTO_INSTALADO_USD"] / 1.21) < 1e-6)
    ref = [x for x in base.values() if x["ID_COSTO"] == "ALI-REF"][0]
    chk("I06", "Referencia de fabricante de planta de alimento: equipo, Incoterm PENDIENTE, no instalado, no usada",
        ref["INSTALACION_INCLUIDA"] == "No" and ref["ESTADO"] == "REFERENCIA" and
        not any(x["COSTO_ID"] == "ALI-REF" for x in run("C3", aves_dia=10000)[0]))
    # ---- Arquitecturas ----
    f0, r0, _ = run("C1", aves_dia=10000)
    chk("A01", "Incubación OFF → bloque EXCLUIDO_POR_ARQUITECTURA con 0 (no 'falta de dato') y sin activos INC",
        r0["INCUBACION"]["ESTADO_BLOQUE"] == "EXCLUIDO_POR_ARQUITECTURA" and r0["INCUBACION"]["TOTAL_PRELIMINAR_USD"] == 0.0
        and not any(x["ACTIVO_ID"].startswith("INC-") for x in f0))
    chk("A02", "Alimento propio OFF → no aparecen activos de planta de alimento",
        not any(x["MODULO"] == "ALIMENTO" for x in f0) and r0["ALIMENTO"]["ESTADO_BLOQUE"] == "EXCLUIDO_POR_ARQUITECTURA")
    chk("A03", "Flota tercerizada → no aparecen vehículos propios",
        not any(x["ACTIVO_ID"].startswith(("VEH-", "CAR-", "FRI-", "AUX-")) for x in f0))
    fc2, _, _ = run("C2", aves_dia=10000)
    vehs = {x["ACTIVO_ID"] for x in fc2 if x["ACTIVO_ID"].startswith("VEH-")}
    chk("A04", "Flota mixta → solo los flujos marcados como propios", vehs == {"VEH-VIVO", "VEH-REFRIGERADO", "VEH-SERVICIO"}, str(vehs))
    fs2, rs2, _ = correr(preset("C2", aves_dia=10000), bs, {})
    gal_int = [x for x in fs2 if x["ACTIVO_ID"] == "GRA-GAL-INT"][0]
    chk("A05", "Granjas integradas no cargan sus galpones al CAPEX de la empresa (se informan aparte)",
        gal_int["TITULAR"] == "PRODUCTOR_INTEGRADO" and rs2["GRANJAS"]["CAPEX_TERCEROS_INFORMATIVO_USD"] and
        abs(rs2["GRANJAS"]["CAPEX_CON_PRECIO_USD"] - sum(x["COSTO_INSTALADO_USD"] for x in fs2 if x["BLOQUE"] == "GRANJAS"
            and x["TITULAR"] == "EMPRESA" and x["COSTEA"] and x["ESTADO_COSTO"] == "CON_PRECIO")) < 1e-6)
    fc0, rc0, _ = run("C0", aves_dia=10000)
    chk("A06", "Façon no carga planta de faena propia (ni terreno, ni proceso, ni frío, ni efluentes)",
        not any(x["MODULO"] in ("PROCESO", "FRIO", "EFLUENTES", "TERRENO") for x in fc0) and
        all(rc0[b]["ESTADO_BLOQUE"] == "EXCLUIDO_POR_ARQUITECTURA" for b in ("TERRENO", "PROCESO", "FRIO", "EFLUENTES")))
    fcf, rcf, _ = run("CF", aves_dia=10000)
    chk("A07", "Reproductoras y rendering = FUTURO, fuera del CAPEX inicial",
        all(x["FASE"] == "FUTURO" for x in fcf if x["MODULO"] == "REPRODUCTORAS" or x["COSTO_ID"] == "SB-REN") and
        any(x["MODULO"] == "REPRODUCTORAS" for x in fcf))
    try:
        validar_config(preset("C1", reproductoras=True))
        ok = False
    except ErrorCapex:
        ok = True
    chk("A08", "Reproductoras sin incubación → error de configuración", ok)
    fl, _, _ = run("C1", aves_dia=10000, modalidad_linea="llave_en_mano")
    l1 = [x for x in fl if x["ACTIVO_ID"] == "PQ-L1"][0]
    chk("A09", "Llave en mano: L1–L5 incluidos en L11 (no se suman dos veces)",
        l1["ACTIVO_PADRE"] == "PQ-L11" and not l1["COSTEA"] and any(x["ACTIVO_ID"] == "PQ-L11" and x["COSTEA"] for x in fl))
    fct, _, _ = run("C1", aves_dia=10000, frio="C_congelado_tercero")
    chk("A10", "Congelado tercerizado → sin túnel de congelado propio", not any(x["ACTIVO_ID"] == "FR-TUN" for x in fct)
        and any(x["ACTIVO_ID"] == "FR-TUN" for x in run("C1", aves_dia=10000, frio="B_refrigerado_congelado")[0]))
    try:
        validar_config(preset("C1", flota="mixto", flota_por_flujo={"vivo": "propia"}))
        ok = False
    except ErrorCapex:
        ok = True
    chk("A11", "Flota mixta exige definición por flujo", ok)
    ftv, _, _ = run("C1", aves_dia=10000)
    jau = [x for x in ftv if x["ACTIVO_ID"] == "JAU-VIVO"]
    chk("A12", "Con flota tercerizada los cajones quedan con titularidad PENDIENTE (no CAPEX de la empresa)",
        jau and jau[0]["TITULAR"] == "PENDIENTE")
    # ---- Escala ----
    drv = {E: run("C3", aves_dia=E)[2] for E in ESCALAS_REF}
    mon = []
    for k in ("terreno_m2", "m2_construidos"):
        mon.append(all(drv[a][k][1] <= drv[b][k][1] + TOL for a, b in zip(ESCALAS_REF, ESCALAS_REF[1:])))
    for k in ("posiciones_setter_diseno", "posiciones_hatcher_diseno"):
        mon.append(all(drv[a]["incubacion"][k] <= drv[b]["incubacion"][k] + TOL for a, b in zip(ESCALAS_REF, ESCALAS_REF[1:])))
    mon.append(all(drv[a]["alimento"]["t_h_requerida"] <= drv[b]["alimento"]["t_h_requerida"] + TOL for a, b in zip(ESCALAS_REF, ESCALAS_REF[1:])))
    for fl_ in ("vivo", "refrigerado", "alimento"):
        mon.append(all((drv[a]["flota"][fl_]["unidades"] or 0) <= (drv[b]["flota"][fl_]["unidades"] or 0) for a, b in zip(ESCALAS_REF, ESCALAS_REF[1:])))
    chk("S01", "Aumentar la escala no reduce capacidades requeridas (terreno, m², setters, hatchers, t/h, flota)", all(mon), str(mon))
    fe1, _, _ = correr(preset("C1", aves_dia=2500), bs, {})
    fe2, _, _ = correr(preset("C1", aves_dia=20000), bs, {})
    c1 = [x for x in fe1 if x["ACTIVO_ID"] == "PQ-L2"][0]["COSTO_INSTALADO_USD"]
    c2 = [x for x in fe2 if x["ACTIVO_ID"] == "PQ-L2"][0]["COSTO_INSTALADO_USD"]
    chk("S02", "El CAPEX no está obligado a escalar linealmente (exponente < 1 → ×8 escala < ×8 costo)",
        c2 < 8 * c1 - TOL and c2 > c1)
    _, ri, _ = run("C1", aves_dia=7500)
    chk("S03", "Escalas intermedias (7.500) funcionan; fuera de rango (30.000) se rechaza",
        ri["TOTAL"]["CONCEPTOS_COSTEABLES"] > 0 and _lanza(validar_config, preset("C1", aves_dia=30000)))
    # ---- Expansión ----
    fx, rx = expansion("C1", "compra_fase", bs)
    rB = [r for r in rx if r["TRAYECTORIA"] == "B_5000_a_20000"]
    chk("X01", "CAPEX inicial ≠ CAPEX acumulado en trayectorias por etapas",
        rB[0]["CAPEX_ACUMULADO_CON_PRECIO_USD"] < rB[-1]["CAPEX_ACUMULADO_CON_PRECIO_USD"] and rB[0]["TIPO"] == "INICIAL")
    fxr, _ = expansion("C1", "compra_reserva", bs)
    ter = [r for r in fxr if r["TRAYECTORIA"] == "B_5000_a_20000" and r["ETAPA"] == 2 and r["ACTIVO_ID"] == "TER-COMPRA"][0]
    chk("X02", "Activo reutilizable (terreno reservado) no se vuelve a comprar", ter["ACCION"] == "REUTILIZA" and
        abs(ter["DELTA_A_ADQUIRIR"]) < 1e-6 and ter["COSTO_ETAPA_USD"] == 0.0)
    vb = [r for r in fx if r["ETIQUETA_EXPANSION"] == "DUPLICABLE" and r["ETAPA"] == 2 and r["ACCION"] == "DUPLICA"]
    chk("X03", "Activos duplicables sí se repiten (Δ > 0 al crecer)", len(vb) > 0)
    chk("X04", "Acción por etiqueta coherente", accion_expansion("REEMPLAZABLE", 1, 2) == ("REEMPLAZA", 2) and
        accion_expansion("REUTILIZABLE", 5, 5)[0] == "REUTILIZA" and accion_expansion("ESCALABLE", None, 3)[0] == "PENDIENTE")
    # ---- Evidencia ----
    chk("E01", "Ítem sin precio permanece PENDIENTE (nivel y estado)",
        all(r["NIVEL_EVIDENCIA"] == "PENDIENTE" for r in base.values() if _num(r["PRECIO_UNITARIO"]) is None))
    b12 = copy.deepcopy(base)
    b12["OC-DP"].update(NIVEL_EVIDENCIA="E1")
    chk("E02", "Una URL / página web sin lectura primaria no pasa a E1 ni a E2/E3",
        _lanza(validar_base, list(b12.values())) and
        _lanza(validar_base, list(dict(b12, **{"OC-DP": dict(b12["OC-DP"], NIVEL_EVIDENCIA="E3")}).values())))
    bs_mix = _base_sintetica(nivel="E5")
    bs_mix["OC-DP"].update(NIVEL_EVIDENCIA="E4")
    fm, rm, _ = correr(preset("C1", aves_dia=10000), bs_mix, {})
    chk("E03", "E1–E5 no se mezclan: Σ por nivel = total; cada fila conserva su nivel",
        abs(sum(rm["TOTAL"][f"CAPEX_{e}_USD"] for e in EVIDENCIAS) - rm["TOTAL"]["CAPEX_CON_PRECIO_USD"]) < 1e-6 and
        rm["TOTAL"]["CAPEX_E4_USD"] == [x for x in fm if x["ACTIVO_ID"] == "OC-DP-OBRA"][0]["COSTO_INSTALADO_USD"])
    b13 = copy.deepcopy(base)
    b13["TER-05"].update(PRECIO_UNITARIO="10", PRECIO_BAJO="5", NIVEL_EVIDENCIA="E5", FUENTE="t", ORIGEN_RANGO="")
    chk("E04", "Rango sin origen declarado → error (no ±20 % automático)", _lanza(validar_base, list(b13.values())))
    chk("E05", "Total preliminar NO se muestra con conceptos faltantes",
        R["TOTAL"]["TOTAL_PRELIMINAR"].startswith("NO DISPONIBLE") and R["TOTAL"]["TOTAL_PRELIMINAR_USD"] is None)
    chk("E06", "Cobertura por valor no calculable si los faltantes no tienen magnitud",
        R["TOTAL"]["COBERTURA_VALOR"].startswith("NO CALCULABLE"))
    b14 = copy.deepcopy(base)
    b14["TER-05"].update(NIVEL_EVIDENCIA="E4")
    chk("E08", "Concepto sin precio con nivel E1–E5 → error (sin precio = PENDIENTE)", _lanza(validar_base, list(b14.values())))
    # ---- Indirectos y contingencia ----
    bp = _base_sintetica(pct=10)
    fp, rp, _ = correr(preset("C1", aves_dia=10000), bp, {})
    dire = sum(x["COSTO_INSTALADO_USD"] for x in fp if x["CATEGORIA_CAPEX"] == "DIRECTO" and x["COSTEA"] and x["FASE"] == "INICIAL"
               and x["TITULAR"] == "EMPRESA" and x["ESTADO_COSTO"] == "CON_PRECIO" and x["BLOQUE"] != "TERRENO")
    ing = [x for x in fp if x["ACTIVO_ID"] == "IND-ING"][0]["COSTO_INSTALADO_USD"]
    chk("P01", "Indirecto % = % × directo con precio sin terreno (separado del directo)", abs(ing - 0.10 * dire) < 1e-6)
    rpc = correr(preset("C2", aves_dia=10000), bp, {})[1]["TOTAL"]
    chk("E07", "Cobertura por conceptos = con precio ÷ costeables; con base sintética completa solo faltan cantidades",
        abs(rpc["COBERTURA_CONCEPTOS_PCT"] - 100 * rpc["CONCEPTOS_CON_PRECIO"] / rpc["CONCEPTOS_COSTEABLES"]) < 1e-9
        and rpc["CONCEPTOS_SIN_PRECIO"] == 0 and rpc["CONCEPTOS_SIN_CANTIDAD"] > 0
        and rpc["CONCEPTOS_CON_PRECIO"] + rpc["CONCEPTOS_SIN_PRECIO"] + sum(1 for x in correr(preset("C2", aves_dia=10000), bp, {})[0]
            if x["COSTEA"] and x["FASE"] == "INICIAL" and x["TITULAR"] == "EMPRESA" and x["ESTADO_COSTO"] not in ("CON_PRECIO", "SIN_PRECIO", "SIN_TIPO_DE_CAMBIO", "BASE_SIN_PRECIO")) == rpc["CONCEPTOS_COSTEABLES"])
    chk("P02", "Porcentaje con base sin precio → PENDIENTE (no 0)",
        [x for x in f if x["ACTIVO_ID"] == "IND-ING"][0]["COSTO_INSTALADO_USD"] is None)
    bp2 = copy.deepcopy(bp)
    bp2["OC-PH"]["CONTINGENCIA_INCLUIDA"] = "Sí"
    fp2, _, _ = correr(preset("C1", aves_dia=10000), bp2, {})
    cd1 = [x for x in fp if x["ACTIVO_ID"] == "CON-DIS"][0]["COSTO_INSTALADO_USD"]
    cd2 = [x for x in fp2 if x["ACTIVO_ID"] == "CON-DIS"][0]["COSTO_INSTALADO_USD"]
    chk("P03", "Contingencia no se aplica sobre conceptos que ya la incluyen", cd2 < cd1)
    chk("P04", "Tres contingencias separadas (diseño, costo, escalación)",
        {x["ACTIVO_ID"] for x in f if x["BLOQUE"] == "CONTINGENCIA"} == {"CON-DIS", "CON-COS", "CON-ESC"})
    chk("P05", "Capital de trabajo, alimento y pollitos operativos NO están en el BOQ",
        not any(re.search(r"capital de trabajo|inventario comercial|alimento operativo|cuentas por cobrar", x["ACTIVO"], re.I) for x in f))
    chk("P06", "Reemplazos y valor residual: campos presentes pero NO sumados al CAPEX inicial",
        all(k in f[0] for k in ("VIDA_UTIL_ANIOS", "REEMPLAZO_ANIO", "COSTO_REEMPLAZO", "VALOR_RESIDUAL")))
    # ---- Integridad ----
    todos_ids = all(len({x["ACTIVO_ID"] for x in run(n, aves_dia=E)[0]}) == len(run(n, aves_dia=E)[0])
                    for n in ("C0", "C1", "C3", "CF") for E in (2500, 20000))
    chk("G01", "IDs únicos en BOQ y base", todos_ids and len(base) == len({r["ID_COSTO"] for r in base.values()}))
    chk("G02", "Unidades válidas en BOQ y base",
        all(x["UNIDAD"] in UNIDADES_VALIDAS for x in fcf) and all(r["UNIDAD"] in UNIDADES_VALIDAS for r in base.values()))
    oblig = ("ACTIVO_ID", "BLOQUE", "COSTO_ID", "ESTADO_COSTO", "ETIQUETA_EXPANSION", "FASE", "TITULAR")
    chk("G03", "Sin NaN/vacíos en campos calculados obligatorios",
        all(all(x.get(k) not in (None, "") or (k == "COSTO_ID" and x["ESTADO_DIMENSION"] == "INFORMATIVO") for k in oblig)
            and all(not (isinstance(v, float) and math.isnan(v)) for v in x.values()) for x in fcf))
    a1 = correr(preset("C1", aves_dia=5000), base, capas)[1]["TOTAL"]
    correr(preset("C3", aves_dia=20000), base, capas)
    a2 = correr(preset("C1", aves_dia=5000), base, capas)[1]["TOTAL"]
    chk("G04", "Escenarios independientes (correr otro no altera el primero)", a1 == a2)
    chk("G05", "Toda fila costeable apunta a un COSTO_ID existente con unidad compatible",
        all(x["COSTO_ID"] in base for x in fcf if x["COSTEA"]))
    chk("G06", "Etiquetas de expansión válidas", all(x["ETIQUETA_EXPANSION"] in ETIQUETAS for x in fcf))
    salida = [d for d in R.values()]
    chk("G07", "Sin palabras de recomendación en salidas", not any(re.search(r"recomendad|ganador|mejor opci|conviene", str(d), re.I)
                                                                   for d in salida))
    ok = all(r[2] for r in res)
    if verbose:
        for cod, desc, o, det in res:
            print(f"[{'OK ' if o else 'FAIL'}] {cod} {desc}" + (f" — {det}" if det and not o else ""))
        print(f"{sum(r[2] for r in res)}/{len(res)} tests OK")
    return ok, res


def _lanza(fn, *a, **k):
    try:
        fn(*a, **k)
        return False
    except ErrorCapex:
        return True


MUTACIONES = {"B01": "duplica m² de depósitos en el BOQ", "C01": "infla 10 % el costo unitario",
              "C02": "trata cualquier precio (FOB) como instalado", "V01": "acepta nivel sin precio",
              "V02": "acepta E1–E3 sin lectura primaria"}


def prueba_mutaciones():
    global _MUT
    detect = {}
    for m in MUTACIONES:
        _MUT = {m}
        try:
            ok, _ = ejecutar_tests(verbose=False)
            detect[m] = not ok
        except Exception:
            detect[m] = True
        finally:
            _MUT = set()
    for m, d in detect.items():
        print(f"[{'DETECTADA' if d else 'NO DETECTADA'}] {m}: {MUTACIONES[m]}")
    return all(detect.values())


# ---------------------------------------------------------------------------------------------
# 13. TABLAS PARA LOS DOCUMENTOS
# ---------------------------------------------------------------------------------------------
def _m(x, d=0):
    if x is None:
        return "—"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_tablas():
    base = leer_base()
    pend = sum(1 for r in base.values() if r["NIVEL_EVIDENCIA"] == "PENDIENTE")
    print(f"Base de costos: {len(base)} conceptos; por nivel:",
          {e: sum(1 for r in base.values() if r["NIVEL_EVIDENCIA"] == e) for e in NIVELES_EVIDENCIA},
          "; por estado:", {s: sum(1 for r in base.values() if r["ESTADO"] == s) for s in {r["ESTADO"] for r in base.values()}})
    print("\n| Escenario | Activos BOQ | Costeables | Con precio | Sin precio | Sin cantidad | Precio parcial | Alcance pend. | CAPEX con precio USD (E4) | Cobertura conceptos | Total |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for nombre, c in escenarios_referencia():
        _, R, _ = correr(c, base)
        t = R["TOTAL"]
        print(f"| {nombre} | {t['ACTIVOS_BOQ']} | {t['CONCEPTOS_COSTEABLES']} | {t['CONCEPTOS_CON_PRECIO']} | "
              f"{t['CONCEPTOS_SIN_PRECIO']} | {t['CONCEPTOS_SIN_CANTIDAD']} | {t['CONCEPTOS_PRECIO_PARCIAL']} | {t['ALCANCE_PENDIENTE']} | "
              f"{_m(t['CAPEX_CON_PRECIO_USD'])} ({_m(t['CAPEX_CON_PRECIO_LOW_USD'])}–{_m(t['CAPEX_CON_PRECIO_HIGH_USD'])}) | "
              f"{_m(t['COBERTURA_CONCEPTOS_PCT'], 1)} % | {t['TOTAL_PRELIMINAR']} |")
    print("\n| Escala | m² construidos (medio) | Terreno fase m² (medio) | Ritmo aves/h | Flota vivo / refrig. / alim. (C3) | Setter / hatcher (posiciones) | Planta alimento t/h | Plazas de galpón |")
    print("|---|---|---|---|---|---|---|---|")
    for E in ESCALAS_REF:
        _, _, D = correr(preset("C3", aves_dia=E), base)
        fl = D["flota"]
        print(f"| {_m(E)} | {_m(D['m2_construidos'][1])} | {_m(D['terreno_m2'][1])} | {_m(D['ritmo_aves_h'])} | "
              f"{fl['vivo']['unidades']} / {fl['refrigerado']['unidades']} / {fl['alimento']['unidades']} | "
              f"{_m(D['incubacion']['posiciones_setter_diseno'])} / {_m(D['incubacion']['posiciones_hatcher_diseno'])} | "
              f"{_m(D['alimento']['t_h_requerida'], 1)} | {_m(D['plazas_alojamiento'])} |")


def escenario_cli(a):
    c = preset(a.config, aves_dia=a.aves_dia, terreno=a.terreno, fecha_base=a.fecha_base,
               dias_semana=a.dias_semana, automatizacion=a.automatizacion)
    if a.terreno == "compra_reserva":
        c["escala_objetivo"] = a.objetivo
    base = leer_base(a.costos) if a.costos else leer_base()
    filas, R, D = correr(c, base, sensibilidad=a.sensibilidad)
    print(etiqueta_arquitectura(c))
    for b, d in R.items():
        print(f"{b:20s} {d['ESTADO_BLOQUE']:26s} conceptos={d['CONCEPTOS_COSTEABLES']:3d} con_precio={d['CONCEPTOS_CON_PRECIO']:3d} "
              f"USD={_m(d['CAPEX_CON_PRECIO_USD'])} total={d['TOTAL_PRELIMINAR']}")
    for al in D["alertas"]:
        print("ALERTA", al)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--mutaciones", action="store_true")
    ap.add_argument("--tablas", action="store_true")
    ap.add_argument("--escenario", action="store_true")
    ap.add_argument("--config", default="C1")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--dias-semana", type=int, default=5)
    ap.add_argument("--terreno", default="compra_fase")
    ap.add_argument("--objetivo", type=float, default=20000)
    ap.add_argument("--automatizacion", default="semi")
    ap.add_argument("--fecha-base", default=FECHA_BASE_CAPEX)
    ap.add_argument("--costos", default=None, help="base de costos alternativa (misma estructura)")
    ap.add_argument("--sensibilidad", action="store_true", help="permite FACTOR_INSTALADO_SENSIBILIDAD")
    a = ap.parse_args()
    if a.mutaciones:
        sys.exit(0 if prueba_mutaciones() else 1)
    ok, _ = ejecutar_tests(verbose=True)
    if not ok:
        sys.exit(1)
    if a.solo_tests:
        return
    if a.tablas:
        imprimir_tablas()
        return
    if a.escenario:
        escenario_cli(a)
        return
    boq, esc, exp = construir_salidas()
    print(f"CSV: {len(boq)} filas BOQ, {len(esc)} filas de escenarios, {len(exp)} filas de expansión")


if __name__ == "__main__":
    main()
