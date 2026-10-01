#!/usr/bin/env python3
"""
MODELO LOGÍSTICO FÍSICO — versión 1.1 (2026-10-01, sesión 12B; auditoría final de interpretación)
=================================================================================================

v1.1: ventana prefaena desagregada (retiro de alimento, captura/carga, espera en granja, transporte,
espera en planta, descarga) con alerta; tiempo de transporte disponible y alcance = RESULTADOS DE
ESCENARIO, nunca límites reglamentarios; retorno sin carga comercial (con jaulas) ≠ vacío y backhaul de
aves deshabilitado por defecto (no prohibido); tiempo de ciclo explícito y utilización derivada de él;
capacidad de ESCENARIO declarada en cada fila (sin capacidad elegida = PENDIENTE); capacidad másica vs
volumétrica en subproductos; acumulación en cinco dimensiones; exportación como sensibilidad;
sensibilidad directo/CD/cross-dock. Tests L21-L28.

Pregunta: ¿QUÉ se mueve, CUÁNTO, DESDE DÓNDE, HACIA DÓNDE, con qué FRECUENCIA y bajo qué
RESTRICCIONES en toda la cadena avícola (insumos → granjas → planta → clientes / puerto /
receptores de subproductos)?  NO responde cuánto cuesta.

Integra, SIN MODIFICARLOS ni copiar sus fórmulas:
  * 23_plan_expansion/modelo_escala.py (v1.1) -> escalas aprobadas (2.500 / 5.000 / 10.000 /
    20.000 aves faenadas por día operativo), calendarios (5 d = 250 d; 6 d = 300 d), perfiles de
    destino P1-P3 (refrigerado / congelado / exportación), contenedor de referencia, y a través de
    él:
      - 03_produccion_primaria/modelo_escenarios_produccion.py (v1.1): aves cargadas, pollitos,
        alimento, plazas de alojamiento, ciclos/año;
      - 04_balance_masa/modelo_balance_masa.py (v1.1) vía 07_subproductos: kg/ave de cada
        producto, coproducto, subproducto, residuo y pérdida (configuraciones A / B / C).
  * 02_clientes_demanda/escenarios_demanda.csv (lectura): locales de la red y reparto
    ilustrativo entre canales del escenario de prueba ESC-BAS.

ESTADO: escenarios FÍSICOS de orden de magnitud. NO elige escala, localización, radio óptimo,
transportista, flota propia/tercerizada, ni calcula CAPEX/OPEX, fletes, precios ni costos.

Uso
---
    python3 13_logistica/modelo_logistica.py                 # tests + escribe escenarios_logistica.csv
    python3 13_logistica/modelo_logistica.py --solo-tests    # solo pruebas
    python3 13_logistica/modelo_logistica.py --resumen       # tablas de resumen por escala
    python3 13_logistica/modelo_logistica.py --escenario --aves-dia 7500 --radio-km 120 \
        --aves-camion 6000 --cap-refrigerado 8 --dias-despacho 6 --perfil P2 \
        --ancla B --kg-local-dia 100 --modo crossdock --dist-mercado-km 300
                                                             # sensibilidad (no escribe CSV)

El script se DETIENE (código 1) si falla cualquier prueba propia (L01-L28) o el modelo de escala.

------------------------------------------------------------------------------
REGLAS DE DATOS (CLAUDE.md reglas 3, 4, 15, 16)
------------------------------------------------------------------------------
  * Toda capacidad de vehículo SIN dato validado vale None (= PENDIENTE). Un resultado que
    depende de un None vale None y se escribe "PENDIENTE" en el CSV; la variable faltante se
    registra en `faltantes`. NUNCA se reemplaza por 0 ni por un valor por defecto (test L13).
  * Los valores de BARRIDO (sensibilidad) se declaran como tales en la columna `parametros`:
    no son capacidades estándar ni recomendaciones.
  * CAPACIDAD DE ESCENARIO ≠ CAPACIDAD VALIDADA / COTIZADA. Ninguna capacidad está validada. Las de
    escenario (camión de aves 4.000-7.000, SUP-033; granelero ~28 t, [ESTIMACIÓN] de 03; contenedor
    25 t, [PVDP · débil] FTE-135; barridos de refrigerado, reparto y subproductos) solo se usan si se
    pasan EXPLÍCITAMENTE; cada fila del CSV declara `capacidad_vehiculo` y `tipo_capacidad` (L25).
  * La ventana prefaena (10 h) es un parámetro de ESCENARIO (8-12 h citadas como práctica, FTE-156
    [PVDP]); no existe fuente primaria que fije un máximo normativo. El tiempo de transporte
    disponible y el alcance en km son resultados, no límites (L21).

------------------------------------------------------------------------------
FÓRMULAS
------------------------------------------------------------------------------
Aves vivas (por día operativo de faena):
  aves cargadas            = aves faenadas / (1 - DOA)                  (mp.calcular, sin copiar)
  merma de viaje [frac]    = tasa de merma [1/h] × (h de transporte medio + espera en planta + descarga)
  peso en granja           = peso en planta / (1 - merma)   (peso en planta = 2,9 kg: ancla del balance)
  kg cargados              = aves cargadas × peso en granja
                           = kg faenables (aves faenadas × peso planta) + kg DOA + kg merma  (L01)
  capacidad efectiva       = aves por camión × (1 - reducción estacional)
  viajes (entero)          = techo(aves cargadas / capacidad efectiva)    (L06)
  ocupación                = aves cargadas / (viajes × capacidad efectiva)  ≤ 100 % (L08)
  distancia geográfica media = radio × factor de distribución (2/3 = media de puntos uniformes
                             en un disco; SUP-093)
  distancia por ruta       = distancia geográfica × factor de ruta (≥ 1; SUP-092) (L18)
  km/día                   = viajes × (ida cargado + retorno sin carga comercial, con jaulas)  (L15, L23)
  tiempo de ciclo [h]      = ida + captura/carga + espera en granja + espera en planta + descarga
                             + regreso + lavado/desinfección                                   (L24)
  ciclos posibles/jornada  = piso(horas útiles / ciclo)
  camión-horas/día         = viajes × ciclo ;  camión-día = camión-horas / horas útiles por camión
  intervalo entre arribos  = aves faenadas por camión / (aves faenadas / horas netas de faena)
  flota mínima             = max(techo(camión-horas / horas útiles), min(viajes, techo(ciclo / intervalo)))
  utilización diaria       = camión-horas / (flota × horas útiles); semanal × días de faena / 7
  total prefaena           = retiro de alimento + captura/carga + espera en granja + transporte
                             + espera en planta + descarga ; alerta si > ventana configurada  (L20)
  transporte disponible    = ventana − (todos los tramos que no son transporte)   [ESCENARIO]  (L22)
  alcance de escenario     = transporte disponible × velocidad (÷ factor de ruta = geográfico)
  alerta de cosecha        = días de faena para retirar un lote > referencia de 03 (1-2 noches):
                             incompatibilidad POTENCIAL bajo la cadencia modelada
Insumos:
  alimento t/día (7 d)     = alimento t/semana plena / 7 ; viajes = techo(t/semana / capacidad)
  pollitos/semana plena    = mp.calcular ; viajes = PENDIENTE sin capacidad validada
Producto terminado (peso comercial):
  t/día operativo          = kg comestible/ave (config.) × aves faenadas / 1.000
  partición                = perfil de destino P1-P3 (SUP-055): refrigerado + congelado + exportación
  t por día de despacho    = t/día operativo × días de faena/semana / días de despacho/semana
  viajes refrigerado y congelado se calculan POR SEPARADO (nunca techo de la suma; L11)
Red ancla (escenarios A / B / C; volumen = variable, no supuesto):
  locales                  = 90 (leído de 02) × fracción adherida (A = 0)
  kg/parada                = kg/local/día × 7 / entregas por semana         (02 §3.1)
  paradas/día de despacho  = locales × entregas por semana / días de despacho
  rutas directas           = max(techo(paradas/día / paradas máx. por ruta), techo(t/día / capacidad))
Asignación por escala (calendario):
  red atendida = min(demanda de la red, comestible no exportado); resto → canales con el reparto
  ilustrativo de ESC-BAS (02); red + canales + exportación = comestible (L05)
Inventario (dos bases, SUP-056 de 23):
  ciclo semanal: producción en días 1..d_faena, despacho uniforme en días 1..d_despacho,
  desfase de 1 día (lo faenado hoy se despacha desde mañana); stock base mínimo para que el
  despacho nunca falte ; stock de seguridad aparte: días de PRODUCCIÓN (t/día op × días) o días
  CALENDARIO (t/día op × días de faena/365 × días). El stock NO modifica los viajes (L10).
Exportación:
  días de faena para llenar un contenedor = carga / t exportadas por día operativo
  contenedores/mes = t exportadas/año / 12 / carga ; 1 contenedor por camión portacontenedor
  SENSIBILIDAD: % exportado y payload explícitos; utilización = t/año / (contenedores enteros × carga) (L27)
  etapas: consolidación (d) + terrestre (h) + espera en terminal (PENDIENTE) + marítimo (PVDP)
Subproductos (sólidos y líquidos a retirar = clase C + decomisos + contenido GI; L04):
  E1 retiro diario | E2 cada 2 días de faena | E3 acumulación refrigerada N días | E4 salida conjunta
  t por retiro = t/día operativo × días acumulados ; ocupación MÁSICA = t / (viajes × t de capacidad)
  m³ = Σ t / densidad aparente (PENDIENTE) ; ocupación VOLUMÉTRICA = m³ / (viajes × m³ útiles)  (L26)
  viajes vinculantes = max(por masa, por volumen) — PENDIENTE si falta densidad o m³
  acumulación: físicamente posible / sanitariamente permitida / aceptada por receptor / frío /
  olores — evaluadas por separado, PENDIENTES sin evidencia (L28)

Unidades: aves; kg; t = 1.000 kg; km; h; d. Separador decimal del CSV: punto.
Bases (regla 14): "vivo", "comercial" (masa biológica + agua retenida), "biologica+agua".
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys

sys.dont_write_bytecode = True           # no dejar __pycache__ en las carpetas de los modelos

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.environ.get("MODELO_LOGISTICA_RAIZ") or os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "23_plan_expansion"))
import modelo_escala as me  # noqa: E402  (escala v1.1; importa producción, balance y subproductos)

mp = me.mp
VERSION = "1.1"
FECHA = "2026-10-01"
FUENTE = "13_logistica/modelo_logistica.py"
TOL = 1e-9


class ErrorLogistica(Exception):
    """Parámetro inválido (capacidad ≤ 0, distancia negativa, backhaul sin evidencia...)."""


# ---------------------------------------------------------------------------
# 1. PARÁMETROS (importados cuando existen; propios con ID SUP-### de la reconciliación 12: SUP-085, SUP-091 a SUP-106)
# ---------------------------------------------------------------------------
ESCALAS = list(me.ESCALAS)                          # leídas del modelo de escala aprobado
CALENDARIOS = dict(me.CALENDARIOS)                  # {5: 250, 6: 300}
PESO = me.PESO_REF                                  # 2,9 kg vivo en planta (ancla del balance)
DOA_BASE = me.parametros_produccion()["doa"]        # 0,3 % (SUP-026, desempeño medio)
CONTENEDOR_T = me.CONTENEDOR_T                      # 25 t [PVDP · débil] FTE-135
PERFILES = me.PERFILES_DESTINO                      # P1 / P2 / P3 (SUP-055)
CONFIGS = tuple(me.CONFIG_VARIANTE)                 # A / B / C

# Aves vivas
AVES_CAMION = (4000, 5500, 7000)      # SUP-033 (sin fuente); 5.500 = punto medio de barrido
AVES_CAMION_BASE = 5500                       # punto medio de barrido; se usa SOLO si se elige explícitamente
ESTACIONES = {"normal": 0.0, "verano": 0.15}   # SUP-097: reducción de carga en verano (barrido 0,10-0,25)
DOA_BARRIDO = (0.002, 0.003, 0.005, 0.010, 0.0163)   # SUP-026 + condiciones adversas FTE-156 [PVDP]
RADIOS_KM = (25, 50, 100, 150, 200, 300)      # SUP-091: radios de SENSIBILIDAD, no óptimos
FACTOR_RUTA = (1.2, 1.3, 1.4)                 # SUP-092 (FTE-286 [PVDP]); base 1,3
FACTOR_RUTA_BASE = 1.3
FACTOR_DISTRIBUCION = 2.0 / 3.0               # SUP-093: media de puntos uniformes en un disco
VEL_VIVO = 60.0                               # km/h; 03 transporte_aves.md [ESTIMACIÓN] 60-70 (barrido 50-70)
# Ventana prefaena DESAGREGADA (SUP-095). Todos son parámetros de escenario, no normas.
T_RETIRO_ALIMENTO_H = 3.0                     # retiro de alimento → inicio de captura (barrido 2-4), sin fuente
T_CAPTURA_CARGA_H = 1.5                       # captura y carga por camión (barrido 1,0-2,5), sin fuente
T_ESPERA_GRANJA_H = 0.0                       # espera adicional en granja tras cargar (barrido 0-1), sin fuente
T_ESPERA_PLANTA_H = 0.75                      # espera en planta hasta descargar (barrido 0,5-2,0), sin fuente
T_DESCARGA_H = 0.25                           # descarga / colgado (barrido 0,25-0,5), sin fuente
T_LAVADO_H = 0.75                             # SUP-095 (barrido 0,5-1,0); Res. SENASA 723/2025 (FTE-234) [PVDP]
VENTANA_PREFAENA_H = 10.0                     # VENTANA DE ESCENARIO: 8-12 h citadas como práctica (FTE-156 [PVDP]);
                                              # NO es un máximo normativo (no hay fuente primaria que lo fije)
DIAS_COSECHA_REFERENCIA = 2                   # 03 transporte_aves.md: una granja "se vacía en 1-2 noches" [ESTIMACIÓN]
HORAS_CAMION_DIA = 12.0                       # SUP-098: horas útiles por camión-día (barrido)
HORAS_NETAS = 8                               # 23/05: referencia de sensibilidad (DEC-036)
MERMA_H_BARRIDO = (0.0, 0.002, 0.005)         # 03 [ESTIMACIÓN] 0,2-0,5 %/h; 0 = SUP-058 (base)
PLAZAS_GRANJA = (15000, 30000, 60000)         # 03 [ESTIMACIÓN] 15-30 mil; 60 mil = barrido

# Insumos
CAP_GRANELERO_T = 28.0                        # 03 alimentacion.md [ESTIMACIÓN] sin fuente; DPV-084. Capacidad de
                                              # ESCENARIO: se usa solo si se pasa explícitamente (por defecto PENDIENTE)
DIST_FABRICA_KM = (25, 75, 150)               # SUP-091 (sin ubicación)
CAP_POLLITOS = None                           # PENDIENTE (DPV-047, DPV-084)
CAP_POLLITOS_BARRIDO = (20000, 40000, 80000)  # barrido ilustrativo, NO capacidad estándar
KG_CAMA_M2 = None                             # PENDIENTE
KG_ENVASE_POR_KG = None                       # PENDIENTE
KG_POR_PALLET = None                          # PENDIENTE
KG_POR_PALLET_BARRIDO = (500, 750, 1000)      # barrido ilustrativo
CONSUMO_L_KM = None                           # PENDIENTE (combustible)

# Producto terminado y red
CAP_REFRIGERADO = None                        # PENDIENTE (DPV-084)
CAP_CONGELADO = None                          # PENDIENTE (DPV-084)
CAP_TRONCAL_BARRIDO = (3, 6, 12, 20)          # t; barrido de SENSIBILIDAD, no capacidad estándar
CAP_REPARTO_BARRIDO = (3, 6)                  # t; barrido (reparto urbano)
DIAS_DESPACHO = (5, 6, 7)                     # SUP-099 (refrigerado)
DESPACHOS_CONGELADO = (1, 2, 3, 6)            # SUP-099: despachos/semana del congelado (acumulable)
DESFASE_DESPACHO = 1                          # SUP-099: despacho desde el día siguiente a la faena
DIST_MERCADO_KM = (30, 150, 300, 600, 1000)   # planta → AMBA por ruta; SUP-091 (sin ubicación)
VEL_TRONCAL = 70.0                            # SUP-094 (barrido 60-80), sin fuente
VEL_URBANA = 20.0                             # SUP-094 (barrido 15-30), sin fuente
T_PARADA_H = 0.75                             # SUP-100 (barrido 0,5-1,0), sin fuente
KM_ENTRE_PARADAS = 8.0                        # SUP-100 (barrido 5-15), sin fuente
PARADAS_RUTA_MAX = (6, 10, 15)                # SUP-100 barrido
T_CARGA_PT_H = 1.0                            # SUP-100: carga en andén de planta, sin fuente
CONDUCCION_MAX_H = 10.0                       # CCT 40/89 [PVDP] FTE-287 (media/larga distancia)
VENTANA_RECEPCION_H = None                    # PENDIENTE (DPV-036)
ENTREGAS_SEMANA = (3, 6)                      # 02 supermercados.md §3.1
KG_LOCAL_DIA = (25, 50, 100, 150, 300)        # 02 escenarios_demanda.csv (RED-xxx): barrido de prueba
ANCLA = {"A": 0.0, "B": 0.5, "C": 1.0}        # SUP-085: fracción de locales adheridos (variable)
N_CD = None                                   # PENDIENTE (DPV-036)
DIST_CROSSDOCK_KM = 25.0                      # SUP-100: cross-dock → tiendas en el AMBA (15-40)

# Exportación
CUOTAS_EXPORT = (0.10, 0.20, 0.50)            # barrido; P3 = 20 % (SUP-055). Demanda = 0 (SUP-022)
DIST_PUERTO_KM = (30, 150, 300, 600, 1000)    # SUP-091 (sin ubicación ni puerto elegido)
TRANSITO_MARITIMO_D = (20, 45)                # 17 logistica_exportacion.md [PVDP · débil]
ESPERA_TERMINAL_D = None                      # PENDIENTE (DPV-027)

# Subproductos
CAP_SUBPROD_BARRIDO = (5, 10, 20)             # t; barrido, NO capacidad estándar
CAP_SUBPROD = None                            # PENDIENTE (DPV-084)
DIST_RECEPTOR_KM = (10, 50, 150)              # SUP-091 (receptor no identificado, DPV-065)
DIAS_MAX_REFRIGERADO_SUBPROD = None           # PENDIENTE [PVDP] (SUP-101)
CAP_SUBPROD_M3 = None                         # capacidad VOLUMÉTRICA útil del vehículo/contenedor: PENDIENTE (DPV-135)
# Densidad aparente (t/m³) por corriente, en el estado y acondicionamiento en que se transporta: SIN EVIDENCIA.
# Sin densidad NO se calcula ocupación volumétrica (las plumas pueden saturar volumen antes que peso).
DENSIDAD_APARENTE_T_M3 = {"plumas": None, "sangre": None, "visceras": None, "cabeza": None, "huesos": None,
                          "otros_c": None, "decomisos_gi": None}

# Backhaul (retorno con carga). Estado por flujo; NO se aplica sin evidencia (L15).
BACKHAUL_POSIBLE = {
    "pollitos_bb": ("REQUIERE_EVIDENCIA", "Vehículo climatizado de la incubadora; retorno con cajas/bandejas vacías propias. Carga de terceros: bioseguridad"),
    "alimento_granel": ("REQUIERE_EVIDENCIA", "Retorno con granos hacia la fábrica de alimento si el origen coincide; bioseguridad de granja"),
    "aves_vivas": ("DESHABILITADO_POR_DEFECTO", "Supuesto conservador (BACKHAUL_AVES = false): el modelo considera el retorno sin carga comercial para no asumir compatibilidades sanitarias o logísticas no verificadas. Otra utilización requiere validar habilitación, lavado/desinfección (Res. SENASA 723/2025 exige lavado y desinfección de superficies a cada viaje, FTE-234), tiempos de ciclo, tipo de vehículo y compatibilidad sanitaria. No es una prohibición normativa general"),
    "refrigerado_troncal": ("REQUIERE_EVIDENCIA", "Carga refrigerada de terceros o insumos (envases, cajas) en sentido inverso; habilitación SENASA del vehículo"),
    "refrigerado_reparto": ("REQUIERE_EVIDENCIA", "Logística inversa: cajas, pallets vacíos, devoluciones (no es carga paga)"),
    "congelado": ("REQUIERE_EVIDENCIA", "Igual que refrigerado; compatibilidad de temperatura y de mercadería"),
    "exportacion_reefer": ("REQUIERE_EVIDENCIA", "Retorno del contenedor vacío o de otra carga: gestión de naviera/operador"),
    "subproductos": ("DESHABILITADO_POR_DEFECTO", "Supuesto conservador: vehículo de subproductos no aptos para consumo humano; otra carga requiere verificar habilitación y compatibilidad sanitaria (DPV-066). No se afirma prohibición normativa sin fuente específica"),
}
BACKHAUL_AVES = False                         # SUP-103: deshabilitado por defecto (no es prohibición)
ESTADOS_BACKHAUL = ("NO", "DESHABILITADO_POR_DEFECTO", "REQUIERE_EVIDENCIA", "SI_CON_EVIDENCIA")
# "NO" se reserva para flujos con prohibición respaldada por fuente normativa específica (hoy: ninguno)

# Tres tipos de retorno que NO se confunden: sin carga comercial · con envases/jaulas · backhaul comercial.
# Un camión que vuelve con jaulas o cajones vacíos NO está físicamente vacío aunque no lleve carga comercial.
TIPO_RETORNO = {
    "aves_vivas": "con envases (jaulas/cajones/módulos vacíos), sin carga comercial",
    "pollitos_bb": "con envases (cajas de pollitos), sin carga comercial",
    "alimento_granel": "sin carga comercial",
    "refrigerado_troncal": "sin carga comercial o con envases/pallets (logística inversa)",
    "refrigerado_reparto": "con envases/pallets y devoluciones (logística inversa)",
    "congelado": "sin carga comercial o con pallets",
    "exportacion_reefer": "con contenedor vacío",
    "subproductos": "con contenedores vacíos (rotativos), sin carga comercial",
}

# Corrientes de subproductos a retirar (partición exacta de `solidos_a_retirar`; L04)
CORRIENTES = {   # clave: (etiqueta, estado físico, vehículo, grupo de salida conjunta, vida sin frío)
    "plumas": ("Plumas húmedas", "sólido húmedo", "contenedor estanco / volcador", "G1-plumas", "horas a 1 día [PVDP]"),
    "sangre": ("Sangre recuperada", "líquido", "cisterna", "G2-sangre", "horas [PVDP]"),
    "visceras": ("Vísceras no comestibles", "sólido húmedo", "contenedor estanco", "G3-visceras", "horas [PVDP]"),
    "cabeza": ("Cabezas", "sólido", "contenedor estanco", "G3-visceras", "horas [PVDP]"),
    "huesos": ("Huesos y residuo óseo (config. C)", "sólido", "contenedor estanco", "G3-visceras", "horas [PVDP]"),
    "otros_c": ("Otros C (garras descarte, piel/grasa a rendering)", "sólido", "contenedor estanco", "G3-visceras", "horas [PVDP]"),
    "decomisos_gi": ("Decomisos + contenido GI", "sólido húmedo", "contenedor estanco segregado", "G4-decomisos", "horas [PVDP]; destino según normativa (DPV-066)"),
}
ESTRATEGIAS = {
    "E1": ("Retiro diario (cada día de faena)", 1),
    "E2": ("Retiro cada 2 días de faena", 2),
    "E3": ("Acumulación refrigerada 3 días de faena", 3),
}

UNIDADES_VALIDAS = {"aves", "aves/h", "pollitos", "t", "kg", "kg/ave", "km", "km/ave", "km/t", "h", "d",
                    "viajes", "camiones", "camión-h", "camión-día", "%", "ratio", "paradas", "kg/parada",
                    "granjas", "cosechas", "contenedores", "pallets", "t·d", "t·km", "ave·h", "índice",
                    "retiros", "km/h", "aves/viaje", "t/viaje", "flag", "rutas", "m³", "t/m³"}


# ---------------------------------------------------------------------------
# 2. UTILIDADES (validación, redondeo, faltantes)
# ---------------------------------------------------------------------------
def _cap(valor, nombre, faltantes):
    """Capacidad: None -> PENDIENTE (se registra el faltante); ≤ 0 -> error. Nunca se rellena."""
    if valor is None:
        faltantes.add(nombre)
        return None
    if valor <= 0:
        raise ErrorLogistica(f"Capacidad {nombre} = {valor}: debe ser > 0")
    return float(valor)


def _dist(valor, nombre):
    if valor is None:
        raise ErrorLogistica(f"Distancia {nombre} sin valor")
    if valor < 0:
        raise ErrorLogistica(f"Distancia {nombre} = {valor}: no puede ser negativa")
    return float(valor)


def _pos(valor, nombre, cero=False):
    if valor is None or valor < 0 or (valor == 0 and not cero):
        raise ErrorLogistica(f"Parámetro {nombre} = {valor} inválido")
    return float(valor)


def _frac(valor, nombre, maximo=1.0):
    if valor is None or not 0 <= valor < maximo + TOL:
        raise ErrorLogistica(f"Fracción {nombre} = {valor} fuera de [0, {maximo}]")
    return float(valor)


class _NoAplica:
    """Valor de una variable que no existe en el escenario (p. ej. ocupación sin viajes).
    Distinto de PENDIENTE (dato faltante): se escribe "NO_APLICA" y nunca entra en cálculos."""
    def __repr__(self):
        return "NO_APLICA"


NA = _NoAplica()


def viajes_enteros(equivalentes):
    """Viajes enteros = techo de los equivalentes (tolerancia numérica). None -> None."""
    if equivalentes is None:
        return None
    if equivalentes < -TOL:
        raise ErrorLogistica(f"Viajes negativos: {equivalentes}")
    if equivalentes <= TOL:
        return 0
    return int(math.ceil(equivalentes - 1e-9))


def dividir(num, cap):
    return None if num is None or cap is None else num / cap


def ocupacion(carga, viajes, cap):
    if carga is None or viajes is None or cap is None:
        return None
    if viajes == 0:
        return NA
    return carga / (viajes * cap)


def mul(*xs):
    if any(x is None for x in xs):
        return None
    r = 1.0
    for x in xs:
        r *= x
    return r


def km_retorno(km_ida, flujo, evidencia=False, fraccion_retorno_cargado=0.0):
    """km de retorno SIN CARGA COMERCIAL (puede llevar envases/jaulas: TIPO_RETORNO). Sin evidencia no se
    aplica backhaul comercial. "DESHABILITADO_POR_DEFECTO" y "REQUIERE_EVIDENCIA" admiten backhaul solo
    con evidencia explícita; "NO" (reservado a prohibición con fuente normativa) nunca lo admite."""
    estado = BACKHAUL_POSIBLE[flujo][0]
    if estado not in ESTADOS_BACKHAUL:
        raise ErrorLogistica(f"Estado de backhaul desconocido: {estado}")
    if not evidencia:
        if fraccion_retorno_cargado:
            raise ErrorLogistica(f"Backhaul en {flujo} sin evidencia: no se aplica")
        return km_ida
    if estado == "NO":
        raise ErrorLogistica(f"Backhaul en {flujo}: estado NO ({BACKHAUL_POSIBLE[flujo][1]})")
    return km_ida * (1 - _frac(fraccion_retorno_cargado, "fraccion_retorno_cargado"))


# ---------------------------------------------------------------------------
# 3. AVES VIVAS (granja → planta)
# ---------------------------------------------------------------------------
def aves_vivas(E, dias_semana=5, doa=DOA_BASE, aves_camion=None, reduccion=0.0,
               radio_km=100, factor_ruta=FACTOR_RUTA_BASE, factor_distribucion=FACTOR_DISTRIBUCION,
               vel=VEL_VIVO, t_retiro_alimento=T_RETIRO_ALIMENTO_H, t_captura_carga=T_CAPTURA_CARGA_H,
               t_espera_granja=T_ESPERA_GRANJA_H, t_espera_planta=T_ESPERA_PLANTA_H, t_descarga=T_DESCARGA_H,
               t_lavado=T_LAVADO_H, ventana_prefaena=VENTANA_PREFAENA_H, horas_camion_dia=HORAS_CAMION_DIA,
               horas_netas=HORAS_NETAS, merma_h=0.0, plazas_granja=30000, dias_cosecha_ref=DIAS_COSECHA_REFERENCIA):
    """Aves vivas granja → planta. `aves_camion` = CAPACIDAD DE ESCENARIO elegida explícitamente; si es
    None, todo resultado que depende del camión queda PENDIENTE. La ventana prefaena es un PARÁMETRO
    DE ESCENARIO (no una norma): el tiempo disponible para transporte y el alcance en km que de ella
    resultan son consecuencias de los supuestos, no límites sanitarios ni reglamentarios."""
    faltantes = set()
    _pos(E, "aves_dia")
    _frac(doa, "doa", 0.2)
    cap = _cap(aves_camion, "aves_por_camion_vivo", faltantes)
    _frac(reduccion, "reduccion_estacional", 0.9)
    radio = _dist(radio_km, "radio_km")
    if factor_ruta < 1:
        raise ErrorLogistica("Factor de ruta < 1: la distancia por ruta no puede ser menor que la geográfica")
    _frac(factor_distribucion, "factor_distribucion")
    for n, v in (("vel", vel), ("horas_camion_dia", horas_camion_dia), ("horas_netas", horas_netas),
                 ("plazas_granja", plazas_granja), ("dias_cosecha_ref", dias_cosecha_ref)):
        _pos(v, n)
    for n, v in (("t_retiro_alimento", t_retiro_alimento), ("t_captura_carga", t_captura_carga),
                 ("t_espera_granja", t_espera_granja), ("t_espera_planta", t_espera_planta),
                 ("t_descarga", t_descarga), ("t_lavado", t_lavado), ("merma_h", merma_h)):
        _pos(v, n, cero=True)
    if ventana_prefaena is None:
        faltantes.add("ventana_prefaena_h")
    else:
        _pos(ventana_prefaena, "ventana_prefaena")

    par = me.parametros_produccion()
    par["doa"] = doa
    pr = mp.calcular(E, dias_semana, **par)              # aves cargadas, plazas, ciclos (03 v1.1)
    cargadas = pr["aves_cargadas_dia"]
    aves_doa = cargadas - E

    d_geo_media = radio * factor_distribucion
    d_ruta_media = d_geo_media * factor_ruta
    d_ruta_max = radio * factor_ruta
    h_viaje = d_ruta_media / vel
    h_viaje_max = d_ruta_max / vel
    merma = merma_h * (h_viaje + t_espera_planta + t_descarga)
    if merma >= 0.2:
        raise ErrorLogistica(f"Merma de viaje {merma:.1%} implausible: revisar tasa y horas")
    peso_granja = PESO / (1 - merma)
    kg_cargado = cargadas * peso_granja
    kg_faenable = E * PESO
    kg_doa = aves_doa * peso_granja
    kg_merma = E * (peso_granja - PESO)

    # --- ventana prefaena (secuencia: retiro de alimento → captura y carga → espera en granja →
    #     transporte → espera en planta → descarga/colgado). Ningún tramo es una norma.
    no_transporte = t_retiro_alimento + t_captura_carga + t_espera_granja + t_espera_planta + t_descarga
    total_medio = no_transporte + h_viaje
    total_max = no_transporte + h_viaje_max
    if ventana_prefaena is None:
        disponible = alcance_ruta = alcance_geo = alerta_medio = alerta_max = None
    else:
        disponible = ventana_prefaena - no_transporte
        alcance_ruta = max(disponible, 0.0) * vel
        alcance_geo = alcance_ruta / factor_ruta
        alerta_medio = 1.0 if total_medio > ventana_prefaena + TOL else 0.0
        alerta_max = 1.0 if total_max > ventana_prefaena + TOL else 0.0

    # --- ciclo del camión = ida + captura/carga + espera en granja + espera en planta + descarga
    #     + regreso + lavado/desinfección (independiente de la capacidad)
    ciclo = h_viaje + t_captura_carga + t_espera_granja + t_espera_planta + t_descarga + h_viaje + t_lavado
    aves_h = E / horas_netas
    out = {
        "faltantes": faltantes,
        "aves_faenadas_dia": E, "aves_cargadas_dia": cargadas, "aves_doa_dia": aves_doa,
        "aves_doa_anio": aves_doa * CALENDARIOS[dias_semana],
        "kg_vivo_cargado_dia": kg_cargado, "kg_vivo_faenable_dia": kg_faenable,
        "kg_doa_dia": kg_doa, "kg_merma_viaje_dia": kg_merma, "merma_viaje_frac": merma,
        "t_vivo_cargado_dia": kg_cargado / 1000, "aves_por_hora_neta": aves_h,
        "distancia_geo_media_km": d_geo_media, "distancia_ruta_media_km": d_ruta_media,
        "distancia_ruta_max_km": d_ruta_max, "h_viaje_medio": h_viaje, "h_viaje_max": h_viaje_max,
        "t_retiro_alimento_h": t_retiro_alimento, "t_captura_carga_h": t_captura_carga,
        "t_espera_granja_h": t_espera_granja, "t_transporte_medio_h": h_viaje, "t_transporte_max_h": h_viaje_max,
        "t_espera_planta_h": t_espera_planta, "t_descarga_h": t_descarga,
        "t_total_prefaena_medio_h": total_medio, "t_total_prefaena_max_h": total_max,
        "ventana_prefaena_escenario_h": ventana_prefaena,
        "t_transporte_disponible_escenario_h": disponible,
        "alcance_ruta_escenario_km": alcance_ruta, "alcance_geo_escenario_km": alcance_geo,
        "alerta_prefaena_excede_ventana_medio": alerta_medio, "alerta_prefaena_excede_ventana_max": alerta_max,
        "ave_horas_transito_dia": cargadas * h_viaje,
        "t_ida_h": h_viaje, "t_regreso_h": h_viaje, "t_lavado_h": t_lavado, "tiempo_ciclo_h": ciclo,
        "ciclos_posibles_por_camion_jornada": float(math.floor(horas_camion_dia / ciclo + 1e-9)),
        "granjas_equivalentes": pr["capacidad_alojamiento_pollitos"] / plazas_granja,
        "aves_cargadas_por_cosecha": plazas_granja * (1 - par["mort"]),
        "ciclos_anio_por_granja": pr["ciclos_anio"],
    }
    por_cosecha = out["aves_cargadas_por_cosecha"]
    out.update({"cosechas_semana": cargadas * dias_semana / por_cosecha,
                "dias_faena_por_cosecha": por_cosecha / cargadas,
                "alerta_cosecha_prolongada_potencial": 1.0 if por_cosecha / cargadas > dias_cosecha_ref + TOL else 0.0})
    if cap is None:                       # capacidad no elegida: resultados de camión PENDIENTES
        for k_ in ("capacidad_efectiva_aves", "viajes_equivalentes_dia", "viajes_dia", "ocupacion", "t_por_viaje",
                   "km_cargado_dia", "km_retorno_sin_carga_comercial_dia", "km_total_dia",
                   "pct_km_sin_carga_comercial", "t_km_dia", "km_por_ave", "km_por_t_vivo", "camion_horas_dia",
                   "camion_dia", "flota_minima", "utilizacion_flota", "utilizacion_semanal_flota",
                   "intervalo_arribos_h", "viajes_por_cosecha"):
            out[k_] = None
        return out
    cap_ef = cap * (1 - reduccion)
    equiv = cargadas / cap_ef
    viajes = viajes_enteros(equiv)
    km_ida = viajes * d_ruta_media
    km_vuelta = km_retorno(km_ida, "aves_vivas")          # retorno sin carga comercial (con jaulas)
    km_total = km_ida + km_vuelta
    camion_h = viajes * ciclo
    intervalo = cap_ef * (1 - doa) / aves_h
    flota_horas = viajes_enteros(camion_h / horas_camion_dia)
    flota_continuo = min(viajes, viajes_enteros(ciclo / intervalo))
    flota = max(flota_horas, flota_continuo)
    out.update({
        "capacidad_efectiva_aves": cap_ef, "viajes_equivalentes_dia": equiv, "viajes_dia": viajes,
        "ocupacion": ocupacion(cargadas, viajes, cap_ef), "t_por_viaje": kg_cargado / 1000 / viajes,
        "km_cargado_dia": km_ida, "km_retorno_sin_carga_comercial_dia": km_vuelta, "km_total_dia": km_total,
        "pct_km_sin_carga_comercial": km_vuelta / km_total if km_total else None,
        "t_km_dia": kg_cargado / 1000 * d_ruta_media,
        "km_por_ave": km_total / E, "km_por_t_vivo": km_total / (kg_cargado / 1000),
        "camion_horas_dia": camion_h, "camion_dia": camion_h / horas_camion_dia,
        "flota_minima": flota, "utilizacion_flota": camion_h / (flota * horas_camion_dia),
        "utilizacion_semanal_flota": camion_h * dias_semana / (flota * horas_camion_dia * 7),
        "intervalo_arribos_h": intervalo, "viajes_por_cosecha": viajes_enteros(por_cosecha / cap_ef),
    })
    return out


# ---------------------------------------------------------------------------
# 4. INSUMOS (hacia granjas y planta)
# ---------------------------------------------------------------------------
def insumos(E, dias_semana=5, cap_granelero=None, dist_fabrica=75, cap_pollitos=CAP_POLLITOS,
            dist_incubadora=150, kg_cama_m2=KG_CAMA_M2, kg_envase_por_kg=KG_ENVASE_POR_KG,
            kg_pallet=KG_POR_PALLET, consumo_l_km=CONSUMO_L_KM, config=me.CONFIG_REF):
    faltantes = set()
    pr = me.produccion(E, dias_semana)
    k, _ = me.kg_por_ave(config)
    cg = _cap(cap_granelero, "cap_granelero_t", faltantes)
    cp = _cap(cap_pollitos, "cap_camion_pollitos", faltantes)
    df_ = _dist(dist_fabrica, "dist_fabrica_granja_km")
    di = _dist(dist_incubadora, "dist_incubadora_granja_km")
    alim_sem = pr["alimento_t_semana_plena"]
    v_alim = viajes_enteros(dividir(alim_sem, cg))
    km_alim = None if v_alim is None else v_alim * df_ + km_retorno(v_alim * df_, "alimento_granel")
    poll_sem = pr["pollitos_alojados_semana_plena"]
    v_poll = viajes_enteros(dividir(poll_sem, cp))
    km_poll = None if v_poll is None else 2 * v_poll * di
    t_com = k["comestible"] * E / 1000
    if kg_cama_m2 is None:
        faltantes.add("kg_cama_m2")
    if kg_envase_por_kg is None:
        faltantes.add("kg_envase_por_kg_producto")
    if kg_pallet is not None and kg_pallet <= 0:
        raise ErrorLogistica("kg por pallet debe ser > 0")
    if kg_pallet is None:
        faltantes.add("kg_por_pallet")
    if consumo_l_km is None:
        faltantes.add("consumo_combustible_l_km")
    return {
        "faltantes": faltantes,
        "alimento_t_semana_plena": alim_sem, "alimento_t_dia_7d": alim_sem / 7,
        "alimento_viajes_semana": v_alim, "alimento_viajes_dia_7d": None if v_alim is None else v_alim / 7,
        "alimento_ocupacion": ocupacion(alim_sem, v_alim, cg), "alimento_km_semana": km_alim,
        "pollitos_semana_plena": poll_sem, "pollitos_viajes_semana": v_poll, "pollitos_km_semana": km_poll,
        "pollitos_ocupacion": ocupacion(poll_sem, v_poll, cp),
        "m2_galpon": pr["m2_galpon"], "ciclos_anio": pr["ciclos_anio"],
        "cama_t_lote": mul(pr["m2_galpon"], kg_cama_m2, 1 / 1000) if kg_cama_m2 is not None else None,
        "envases_t_dia": mul(t_com, kg_envase_por_kg),
        "pallets_dia": None if kg_pallet is None else t_com * 1000 / kg_pallet,
        "combustible_l_semana": None,      # requiere consumo y km de todos los flujos: PENDIENTE
    }


# ---------------------------------------------------------------------------
# 5. PRODUCTO TERMINADO (troncal planta → punto de entrega; refrigerado y congelado SEPARADOS)
# ---------------------------------------------------------------------------
def producto(E, dias_semana=5, config=me.CONFIG_REF, perfil="P1", dias_despacho=6,
             cap_refrigerado=CAP_REFRIGERADO, cap_congelado=CAP_CONGELADO, dist_km=300,
             vel=VEL_TRONCAL, horas_camion_dia=HORAS_CAMION_DIA, despachos_congelado=None):
    """Refrigerado: `dias_despacho` por semana. Congelado: `despachos_congelado` por semana
    (por defecto = dias_despacho); el congelado puede acumularse para llenar camiones (SUP-099)."""
    faltantes = set()
    if perfil not in PERFILES:
        raise ErrorLogistica(f"Perfil {perfil} inexistente")
    despachos_congelado = dias_despacho if despachos_congelado is None else despachos_congelado
    if not 1 <= dias_despacho <= 7 or not 1 <= despachos_congelado <= 7:
        raise ErrorLogistica("días de despacho fuera de 1-7")
    cr = _cap(cap_refrigerado, "cap_camion_refrigerado_t", faltantes)
    cc = _cap(cap_congelado, "cap_camion_congelado_t", faltantes)
    d = _dist(dist_km, "dist_planta_destino_km")
    k, _ = me.kg_por_ave(config)
    com = k["comestible"] * E / 1000
    sh = PERFILES[perfil][1]
    out = {"faltantes": faltantes, "comestible_t_dia_op": com, "dias_despacho": dias_despacho}
    for cadena, capx, dd in (("refrigerado", cr, dias_despacho), ("congelado", cc, despachos_congelado)):
        t_op = com * sh[cadena]
        t_desp = t_op * dias_semana / dd
        v = viajes_enteros(dividir(t_desp, capx))
        km = None if v is None else 2 * v * d
        ciclo = 2 * T_CARGA_PT_H + 2 * d / vel
        out.update({
            f"{cadena}_t_dia_op": t_op, f"{cadena}_t_semana": t_op * dias_semana,
            f"{cadena}_t_dia_despacho": t_desp, f"{cadena}_viajes_dia_despacho": v,
            f"{cadena}_viajes_semana": None if v is None else v * dd, f"{cadena}_despachos_semana": dd,
            f"{cadena}_stock_ciclo_max_t": inventario(t_op, dias_semana, dd)["stock_ciclo_max_t"],
            f"{cadena}_ocupacion": ocupacion(t_desp, v, capx), f"{cadena}_km_dia_despacho": km,
            f"{cadena}_km_por_t": None if km is None else (NA if t_desp == 0 else km / t_desp),
            f"{cadena}_camion_dia": None if v is None else v * ciclo / horas_camion_dia,
            f"{cadena}_tiempo_ciclo_h": ciclo,
        })
    out["exportacion_t_dia_op"] = com * sh["exportacion"]
    return out


# ---------------------------------------------------------------------------
# 6. RED ANCLA (A sin red / B parcial / C fuerte) — volumen VARIABLE
# ---------------------------------------------------------------------------
def locales_red():
    _, locales = me.leer_demanda()            # 90 (02_clientes_demanda/escenarios_demanda.csv)
    return locales


def red_ancla(escenario, kg_local_dia, entregas_semana=3, modo="directo", dias_despacho=6,
              paradas_ruta_max=10, cap_reparto=None, cap_troncal=None, dist_mercado_km=300,
              km_entre_paradas=KM_ENTRE_PARADAS, t_parada=T_PARADA_H, vel_troncal=VEL_TRONCAL,
              vel_urbana=VEL_URBANA, dist_crossdock_km=DIST_CROSSDOCK_KM, n_cd=N_CD,
              ventana_h=VENTANA_RECEPCION_H, conduccion_max_h=CONDUCCION_MAX_H,
              horas_camion_dia=HORAS_CAMION_DIA, fraccion_locales=None, locales_totales=None):
    """Logística de la red de supermercados. `fraccion_locales` sobreescribe la del escenario."""
    faltantes = set()
    if escenario not in ANCLA:
        raise ErrorLogistica(f"Escenario ancla {escenario} inexistente (A/B/C)")
    if modo not in ("directo", "cd", "crossdock"):
        raise ErrorLogistica(f"Modo {modo} inexistente")
    frac = ANCLA[escenario] if fraccion_locales is None else _frac(fraccion_locales, "fraccion_locales")
    if escenario == "A" and frac:
        raise ErrorLogistica("El escenario A es sin red: fracción de locales = 0")
    tot = locales_red() if locales_totales is None else locales_totales
    locales = round(tot * frac)
    _pos(kg_local_dia, "kg_local_dia", cero=True)
    _pos(entregas_semana, "entregas_semana")
    d = _dist(dist_mercado_km, "dist_planta_mercado_km")
    dx = _dist(dist_crossdock_km, "dist_crossdock_tiendas_km")
    kpar = _dist(km_entre_paradas, "km_entre_paradas")
    kg_cal = locales * kg_local_dia
    t_disp = kg_cal * 7 / dias_despacho / 1000
    out = {"faltantes": faltantes, "escenario": escenario, "modo": modo, "locales": locales,
           "demanda_red_t_dia_cal": kg_cal / 1000, "t_dia_despacho": t_disp,
           "kg_por_parada_tienda": kg_local_dia * 7 / entregas_semana if locales else 0.0,
           "paradas_tienda_semana": locales * entregas_semana}
    if locales == 0:
        out.update({k: 0.0 for k in ("paradas_planta_dia", "viajes_troncal_dia", "rutas_reparto_dia",
                                     "km_dia_despacho", "camion_horas_dia")})
        out.update({"ocupacion_troncal": NA, "ocupacion_reparto": NA, "km_por_t": NA,
                    "h_ruta_reparto": NA, "h_conduccion_reparto": NA, "excede_conduccion": 0.0,
                    "excede_ventana": NA, "paradas_por_ruta": 0.0, "excede_jornada": 0.0,
                    "inviable_en_jornada": 0.0})
        return out
    paradas_dia = locales * entregas_semana / dias_despacho

    def reparto(dist_origen, cap, vel_acceso):
        capr = _cap(cap, "cap_camion_reparto_t", faltantes)
        # paradas que caben en la jornada útil del camión (SUP-098) después de cargar e ir y volver
        libre = horas_camion_dia - T_CARGA_PT_H - 2 * dist_origen / vel_acceso
        por_tiempo = math.floor(libre / (t_parada + kpar / vel_urbana) + 1e-9) if libre > 0 else 0
        inviable = 1.0 if por_tiempo < 1 else 0.0
        limite = max(1, min(paradas_ruta_max, por_tiempo))
        r_par = viajes_enteros(paradas_dia / limite)
        r_cap = viajes_enteros(dividir(t_disp, capr))
        rutas = None if r_cap is None else max(r_par, r_cap)
        ppr = paradas_dia / (rutas if rutas else r_par)
        h_cond = 2 * dist_origen / vel_acceso + ppr * kpar / vel_urbana
        h_ruta = T_CARGA_PT_H + h_cond + ppr * t_parada
        tramo_entregas = ppr * (t_parada + kpar / vel_urbana)
        km = None if rutas is None else rutas * (2 * dist_origen + ppr * kpar)
        return {"rutas_min_por_paradas": r_par, "rutas_reparto_dia": rutas, "paradas_por_ruta": ppr,
                "ocupacion_reparto": ocupacion(t_disp, rutas, capr), "h_conduccion_reparto": h_cond,
                "h_ruta_reparto": h_ruta, "excede_conduccion": 1.0 if h_cond > conduccion_max_h else 0.0,
                "paradas_max_por_jornada": float(por_tiempo), "inviable_en_jornada": inviable,
                "excede_jornada": 1.0 if h_ruta > horas_camion_dia + TOL else 0.0,
                "excede_ventana": None if ventana_h is None else (1.0 if tramo_entregas > ventana_h else 0.0),
                "tramo_entregas_h": tramo_entregas, "km_reparto": km,
                "camion_horas_reparto": None if rutas is None else rutas * h_ruta}

    if ventana_h is None:
        faltantes.add("ventana_recepcion_h")
    if modo == "directo":
        r = reparto(d, cap_reparto, vel_troncal)
        out.update(r)
        out.update({"paradas_planta_dia": r["rutas_reparto_dia"], "viajes_troncal_dia": 0.0,
                    "ocupacion_troncal": None, "km_dia_despacho": r["km_reparto"],
                    "camion_horas_dia": r["camion_horas_reparto"]})
    else:
        ct = _cap(cap_troncal, "cap_camion_troncal_t", faltantes)
        vt = viajes_enteros(dividir(t_disp, ct))
        km_t = None if vt is None else 2 * vt * d
        h_t = 2 * T_CARGA_PT_H + 2 * d / vel_troncal
        out.update({"viajes_troncal_dia": vt, "ocupacion_troncal": ocupacion(t_disp, vt, ct),
                    "h_conduccion_troncal": 2 * d / vel_troncal,
                    "excede_conduccion": 1.0 if 2 * d / vel_troncal > conduccion_max_h else 0.0,
                    "excede_jornada": 1.0 if h_t > horas_camion_dia + TOL else 0.0})
        if modo == "cd":
            if n_cd is None:
                faltantes.add("n_centros_distribucion")
            out.update({"paradas_planta_dia": None if n_cd is None else n_cd, "rutas_reparto_dia": 0.0,
                        "paradas_por_ruta": None if n_cd is None or vt in (None, 0) else n_cd / vt,
                        "km_dia_despacho": km_t, "camion_horas_dia": None if vt is None else vt * h_t,
                        "excede_ventana": NA, "h_ruta_reparto": NA, "ocupacion_reparto": NA,
                        "nota_ultima_milla": "a cargo del cliente (fee de CD: DPV-039)"})
        else:
            r = reparto(dx, cap_reparto, vel_urbana)
            out.update({k: v for k, v in r.items() if k != "excede_conduccion"})
            out["excede_conduccion"] = max(out["excede_conduccion"], r["excede_conduccion"])
            out["excede_jornada"] = max(r["excede_jornada"], 1.0 if h_t > horas_camion_dia + TOL else 0.0)
            out.update({"paradas_planta_dia": vt,
                        "km_dia_despacho": None if km_t is None or r["km_reparto"] is None else km_t + r["km_reparto"],
                        "camion_horas_dia": None if vt is None or r["camion_horas_reparto"] is None
                        else vt * h_t + r["camion_horas_reparto"]})
    km = out["km_dia_despacho"]
    out["km_por_t"] = None if km is None else km / t_disp
    return out


# ---------------------------------------------------------------------------
# 7. ASIGNACIÓN POR ESCALA (red + otros canales + exportación = comestible; día calendario)
# ---------------------------------------------------------------------------
def reparto_otros_canales():
    """Participación ilustrativa de los canales NO supermercado en ESC-BAS (02; SUP-102)."""
    esc, _ = me.leer_demanda()
    r = esc["ESC-BAS"]
    canales = {"mayorista_distribuidor": float(r["mayoristas_distribuidores_kg_dia"]),
               "carnicerias_pollerias": float(r["carnicerias_pollerias_kg_dia"]),
               "gastronomia": float(r["gastronomia_kg_dia"]),
               "elaborador_industria": float(r["industria_kg_dia"])}
    tot = sum(canales.values())
    return {c: v / tot for c, v in canales.items()}


def asignacion(E, dias_semana=5, config=me.CONFIG_REF, perfil="P1", escenario="B", kg_local_dia=100,
               fraccion_locales=None):
    dias_anio = CALENDARIOS[dias_semana]
    k, _ = me.kg_por_ave(config)
    com_cal = k["comestible"] * E / 1000 * dias_anio / 365
    exp_cal = com_cal * PERFILES[perfil][1]["exportacion"]
    disponible = com_cal - exp_cal
    red = red_ancla(escenario, kg_local_dia, fraccion_locales=fraccion_locales)
    dem = red["demanda_red_t_dia_cal"]
    atend = min(dem, disponible)
    resto = disponible - atend
    sh = reparto_otros_canales()
    out = {"comestible_t_dia_cal": com_cal, "exportacion_t_dia_cal": exp_cal,
           "demanda_red_t_dia_cal": dem, "red_atendida_t_dia_cal": atend,
           "red_no_atendida_t_dia_cal": dem - atend,
           "cobertura_red": NA if dem == 0 else atend / dem,
           "participacion_red": atend / com_cal, "otros_canales_t_dia_cal": resto,
           "locales": red["locales"]}
    for c, s in sh.items():
        out[f"canal_{c}_t_dia_cal"] = resto * s
    return out


# ---------------------------------------------------------------------------
# 8. INVENTARIO: ciclo semanal + stock de seguridad (dos bases) — separado del despacho
# ---------------------------------------------------------------------------
def inventario(t_op_dia, dias_faena=5, dias_despacho=6, dias_seguridad=0, base="produccion",
               desfase=DESFASE_DESPACHO, cap=None):
    faltantes = set()
    if base not in ("produccion", "calendario"):
        raise ErrorLogistica("base temporal: produccion | calendario")
    if dias_faena not in CALENDARIOS:
        raise ErrorLogistica("días de faena: 5 o 6")
    if not 1 <= dias_despacho <= 7 or desfase not in (0, 1):
        raise ErrorLogistica("días de despacho 1-7; desfase 0 o 1")
    _pos(t_op_dia, "t_op_dia", cero=True)
    _pos(dias_seguridad, "dias_seguridad", cero=True)
    prod = [t_op_dia if i < dias_faena else 0.0 for i in range(7)]
    desp_d = t_op_dia * dias_faena / dias_despacho
    desp = [desp_d if i < dias_despacho else 0.0 for i in range(7)]
    acum, c = [], 0.0
    for i in range(7):
        c += prod[i] - desp[i]
        acum.append(c)
    previo = [0.0] + acum[:-1]
    if desfase == 1:      # se despacha lo que existía al comenzar el día
        base_min = max(max(desp[i] - previo[i] for i in range(7)), 0.0)
    else:
        base_min = max(-min(acum), 0.0)
    stock_fin = [base_min + a for a in acum]
    dias_anio = CALENDARIOS[dias_faena]
    seg = t_op_dia * dias_seguridad * (1 if base == "produccion" else dias_anio / 365)
    capx = _cap(cap, "cap_camion_despacho_t", faltantes)
    v = viajes_enteros(dividir(desp_d, capx))
    return {"faltantes": faltantes, "produccion_semana_t": sum(prod), "despacho_semana_t": sum(desp),
            "despacho_t_dia_despacho": desp_d, "stock_ciclo_max_t": max(stock_fin + [base_min]),
            "stock_ciclo_medio_t": sum(stock_fin) / 7, "stock_seguridad_t": seg,
            "stock_total_max_t": max(stock_fin + [base_min]) + seg,
            "t_dias_inmovilizadas_semana": sum(stock_fin) + 7 * seg,
            "viajes_dia_despacho": v, "viajes_semana": None if v is None else v * dias_despacho,
            "ocupacion": ocupacion(desp_d, v, capx)}


# ---------------------------------------------------------------------------
# 9. EXPORTACIÓN (planta → consolidación → puerto → reefer)
# ---------------------------------------------------------------------------
def exportacion(E, dias_semana=5, config=me.CONFIG_REF, cuota=0.20, carga_t=CONTENEDOR_T,
                dist_puerto_km=300, vel=VEL_TRONCAL, espera_terminal_d=ESPERA_TERMINAL_D,
                transito_d=TRANSITO_MARITIMO_D):
    faltantes = set()
    _frac(cuota, "cuota_exportacion")
    c = _cap(carga_t, "carga_contenedor_t", faltantes)
    d = _dist(dist_puerto_km, "dist_planta_puerto_km")
    dias_anio = CALENDARIOS[dias_semana]
    k, _ = me.kg_por_ave(config)
    t_op = k["comestible"] * E / 1000 * cuota
    t_anio = t_op * dias_anio
    if espera_terminal_d is None:
        faltantes.add("espera_terminal_d")
    if transito_d is None:
        faltantes.add("transito_maritimo_d")
    d_op = None if t_op == 0 or c is None else c / t_op
    cont_anio = dividir(t_anio, c)
    h_terr = d / vel
    conocido = None
    if d_op is not None and espera_terminal_d is not None and transito_d is not None:
        conocido = d_op * 365 / dias_anio + h_terr / 24 + espera_terminal_d + max(transito_d)
    cont_ent = viajes_enteros(cont_anio)
    return {"faltantes": faltantes, "cuota_exportacion": cuota, "carga_contenedor_t": c,
            "export_t_dia_op": t_op, "export_t_anio": t_anio,
            "utilizacion_carga_contenedores": None if not cont_ent else t_anio / (cont_ent * c),
            "dias_faena_llenar_contenedor": d_op,
            "dias_calendario_llenar_contenedor": None if d_op is None else d_op * 365 / dias_anio,
            "contenedores_mes": None if cont_anio is None else cont_anio / 12,
            "contenedores_anio_enteros": viajes_enteros(cont_anio),
            "viajes_terrestres_anio": viajes_enteros(cont_anio),   # 1 contenedor por camión (a validar)
            "h_terrestre_planta_puerto": h_terr, "km_terrestre_anio": None if cont_anio is None
            else 2 * viajes_enteros(cont_anio) * d,
            "espera_terminal_d": espera_terminal_d,
            "transito_maritimo_d_min": None if transito_d is None else min(transito_d),
            "transito_maritimo_d_max": None if transito_d is None else max(transito_d),
            "stock_consolidacion_max_t": c, "lead_time_total_max_d": conocido}


# ---------------------------------------------------------------------------
# 10. SUBPRODUCTOS (retiro diario / cada 2 días / acumulación refrigerada / salida conjunta)
# ---------------------------------------------------------------------------
def corrientes_subproductos(E, config=me.CONFIG_REF):
    k, _ = me.kg_por_ave(config)
    kg = {c: k[c] for c in CORRIENTES if c != "decomisos_gi"}
    kg["decomisos_gi"] = k["solidos_a_retirar"] - k["subproductos_c"]
    t = {c: v * E / 1000 for c, v in kg.items()}
    coprod = {c: k[c] * E / 1000 for c in ("garras", "menudencias", "carcasa_esqueleto", "cuello")}
    return t, k["solidos_a_retirar"] * E / 1000, coprod


def subproductos(E, dias_semana=5, config=me.CONFIG_REF, estrategia="E1", cap=CAP_SUBPROD,
                 dist_receptor_km=50, corriente=None, dias_max_refrigerado=DIAS_MAX_REFRIGERADO_SUBPROD,
                 cap_m3=CAP_SUBPROD_M3, densidades=None):
    """Una corriente (o un grupo de salida conjunta si `corriente` empieza con 'G').
    `cap` = capacidad MÁSICA de escenario (t); `cap_m3` = capacidad VOLUMÉTRICA útil (m³); `densidades` =
    densidad aparente t/m³ por corriente. Ocupación másica y volumétrica son variables distintas; la
    volumétrica queda PENDIENTE si falta la densidad de algún miembro o la capacidad en m³."""
    faltantes = set()
    if estrategia not in ESTRATEGIAS:
        raise ErrorLogistica(f"Estrategia {estrategia} inexistente")
    capx = _cap(cap, "cap_vehiculo_subproductos_t", faltantes)
    capv = _cap(cap_m3, "cap_vehiculo_subproductos_m3", faltantes)
    d = _dist(dist_receptor_km, "dist_receptor_km")
    t, _, _ = corrientes_subproductos(E, config)
    if corriente is None:
        raise ErrorLogistica("Indicar corriente o grupo")
    miembros = [c for c in CORRIENTES if CORRIENTES[c][3] == corriente] if corriente.startswith("G") else [corriente]
    if not miembros or any(m not in CORRIENTES for m in miembros):
        raise ErrorLogistica(f"Corriente {corriente} inexistente")
    dens = dict(DENSIDAD_APARENTE_T_M3, **(densidades or {}))
    t_dia = sum(t[m] for m in miembros)
    activos = [m for m in miembros if t[m] > 0]
    for m in activos:
        if dens.get(m) is None:
            faltantes.add(f"densidad_aparente_{m}")
        elif dens[m] <= 0:
            raise ErrorLogistica(f"Densidad aparente de {m} debe ser > 0")
    m3_dia = None if any(dens.get(m) is None for m in activos) else sum(t[m] / dens[m] for m in activos)
    acum = ESTRATEGIAS[estrategia][1]
    retiros = viajes_enteros(dias_semana / acum)
    t_ret = t_dia * acum
    m3_ret = None if m3_dia is None else m3_dia * acum
    v_masa = viajes_enteros(dividir(t_ret, capx))
    v_vol = viajes_enteros(dividir(m3_ret, capv))
    v_vinc = None if v_masa is None or v_vol is None else max(v_masa, v_vol)
    if acum > 1:
        faltantes.update({"dias_max_refrigerado_subproductos", "requisitos_receptor_acumulacion",
                          "normativa_acumulacion_subproductos", "capacidad_almacenamiento_refrigerado_subproductos"})
    else:
        faltantes.update({"requisitos_receptor_acumulacion", "normativa_acumulacion_subproductos"})
    return {"faltantes": faltantes, "miembros": miembros, "t_dia_op": t_dia, "t_semana": t_dia * dias_semana,
            "m3_dia_op": m3_dia, "dias_acumulados": acum, "t_por_retiro": t_ret, "m3_por_retiro": m3_ret,
            "retiros_semana": retiros,
            "viajes_por_retiro_criterio_masa": v_masa,
            "viajes_semana_criterio_masa": None if v_masa is None else v_masa * retiros,
            "ocupacion_masica": ocupacion(t_ret, v_masa, capx),
            "viajes_por_retiro_criterio_volumen": v_vol,
            "ocupacion_volumetrica": ocupacion(m3_ret, v_vol, capv),
            "viajes_por_retiro_vinculante": v_vinc,
            "km_semana_criterio_masa": None if v_masa is None else 2 * v_masa * retiros * d,
            "stock_refrigerado_max_t": t_dia * (acum - 1),
            "dias_faena_para_llenar_capacidad_masica": None if capx is None or t_dia == 0 else capx / t_dia,
            # acumulación: cinco dimensiones separadas (SUP-101); ninguna se da por cumplida sin evidencia
            "fisicamente_posible": 1.0 if acum == 1 else None,          # >1 día: depende de cámara/recipientes (12C)
            "sanitariamente_permitido": None,                            # normativa no leída (DPV-066, DPV-128)
            "aceptado_por_receptor": None,                               # DPV-065
            "requiere_frio": 1.0 if acum > 1 else 0.0,                   # frío o recipiente específico si se acumula
            "riesgo_olores_degradacion_aumentado": 1.0 if acum > 1 else 0.0}


# ---------------------------------------------------------------------------
# 11. CONSTRUCCIÓN DEL CSV
# ---------------------------------------------------------------------------
CAMPOS = ["bloque", "escala_aves_dia", "dias_semana", "dias_anio", "escenario", "parametros", "variable",
          "valor", "unidad", "periodo", "base", "cadena", "clasificacion", "tipo_kpi", "sumable",
          "capacidad_vehiculo", "tipo_capacidad", "fuente", "nota"]
# Variables cuyo valor depende de la capacidad del vehículo: toda fila debe declarar la capacidad usada (L25)
PATRON_DEPENDE_CAPACIDAD = ("viajes", "rutas", "flota", "ocupacion", "camion_dia", "camion_horas", "km_total",
                            "km_cargado", "km_retorno", "km_por_", "km_dia_despacho", "km_semana", "km_reparto",
                            "t_por_viaje", "pct_km", "utilizacion_flota", "utilizacion_semanal_flota", "intervalo",
                            "capacidad_efectiva", "contenedores", "llenar", "paradas_planta", "t_km")
TIPOS_CAPACIDAD = ("ESCENARIO", "ESCENARIO [ESTIMACIÓN 03]", "ESCENARIO [PVDP]", "PENDIENTE", "VALIDADA", "COTIZADA")
NOTA_ALCANCE = ("Resultado del escenario (ventana prefaena, tiempos y velocidad supuestos: SUP-094/095); "
                "NO es límite sanitario, reglamentario ni radio óptimo")


def depende_capacidad(var):
    return any(p_ in var for p_ in PATRON_DEPENDE_CAPACIDAD)

def _unidad(var):
    """Unidad por nombre de variable (reglas en orden; L16 verifica que toda unidad sea válida)."""
    reglas = [("m3_", "m³"), ("cuota", "ratio"), ("alerta", "flag"), ("fisicamente", "flag"),
              ("sanitariamente", "flag"), ("aceptado", "flag"), ("riesgo_", "flag"),
              ("despachos_semana", "d"), ("inviable", "flag"), ("_frac", "ratio"), ("ocupacion", "%"), ("pct_", "%"), ("utilizacion", "%"), ("cobertura", "%"),
              ("participacion", "%"), ("km_por_ave", "km/ave"), ("km_por_t", "km/t"), ("t_km", "t·km"),
              ("t_dias", "t·d"), ("t_dia", "t"), ("t_vivo", "t"), ("_t_", "t"), ("t_por_retiro", "t"),
              ("t_por_viaje", "t/viaje"), ("t_semana", "t"), ("t_lote", "t"), ("t_anio", "t"),
              ("km_", "km"), ("_km", "km"), ("distancia", "km"), ("ave_horas", "ave·h"),
              ("camion_horas", "camión-h"), ("camion_dia", "camión-día"), ("intervalo", "h"), ("h_", "h"),
              ("_h", "h"), ("tiempo", "h"), ("viajes", "viajes"), ("rutas", "rutas"), ("flota", "camiones"),
              ("kg_por_parada", "kg/parada"), ("paradas", "paradas"), ("aves_por_hora", "aves/h"),
              ("capacidad_efectiva", "aves/viaje"), ("kg_", "kg"), ("aves_", "aves"), ("pollitos", "pollitos"),
              ("granjas", "granjas"), ("cosechas", "cosechas"), ("contenedores", "contenedores"),
              ("pallets", "pallets"), ("retiros", "retiros"), ("dias_", "d"), ("_d_", "d"), ("_d", "d"),
              ("despachos_semana", "d"), ("dentro_", "flag"), ("excede", "flag"), ("inviable", "flag"), ("requiere", "flag"),
              ("ciclos", "índice"), ("m2", "m²"), ("locales", "índice"), ("_t", "t"), ("stock", "t"),
              ("combustible", "índice")]
    for pat, u in reglas:
        if pat in var:
            return u
    return "índice"


PERIODOS_VAR = [  # (patrón en el nombre, período) — se aplica antes del período del bloque
    ("cuota", "-"), ("carga_contenedor", "embarque"), ("utilizacion_carga", "anio"), ("ventana_prefaena", "lote"),
    ("t_retiro_alimento", "lote"), ("t_captura", "viaje"), ("t_espera", "viaje"), ("t_transporte", "viaje"),
    ("t_descarga", "viaje"), ("t_total_prefaena", "lote"), ("alcance", "viaje"), ("alerta_prefaena", "lote"),
    ("t_ida", "viaje"), ("t_regreso", "viaje"), ("t_lavado", "viaje"), ("ciclos_posibles", "dia_operativo"),
    ("utilizacion_semanal", "semana"), ("m3_dia", "dia_operativo"), ("m3_por_retiro", "retiro"),
    ("stock", "stock"), ("t_dias_inmovilizadas", "semana"), ("_anio", "anio"), ("contenedores_mes", "mes"),
    ("_semana", "semana"), ("por_cosecha", "cosecha"), ("t_dia_cal", "dia_calendario"),
    ("t_dia_op", "dia_operativo"), ("t_dia_7d", "dia_calendario"), ("viajes_dia_7d", "dia_calendario"),
    ("t_lote", "lote"), ("tiempo_ciclo", "viaje"), ("h_viaje", "viaje"),
    ("t_por_viaje", "viaje"), ("capacidad_efectiva", "viaje"), ("distancia", "viaje"),
    ("h_terrestre", "viaje"), ("llenar", "lote"), ("transito", "embarque"), ("espera_terminal", "embarque"),
    ("lead_time", "embarque"), ("t_por_retiro", "retiro"), ("por_retiro", "retiro"), ("m2_galpon", "-"),
    ("granjas_equivalentes", "-"), ("intervalo", "-"), ("locales", "-"), ("kg_por_parada", "entrega"),
    ("paradas_por_ruta", "ruta"), ("h_ruta", "ruta"), ("h_conduccion", "ruta"), ("tramo_entregas", "ruta"),
]


def _periodo(var, defecto):
    for pat, p in PERIODOS_VAR:
        if pat in var:
            return p
    return defecto


class Tabla:
    def __init__(self):
        self.filas = []

    def add(self, bloque, E, ds, escenario, parametros, variable, valor, periodo, base="-", cadena="-",
            clasif=None, tipo_kpi="fisico", sumable="no", nota="", unidad=None, capacidad="-", tipo_capacidad="-"):
        if isinstance(valor, bool):
            valor = 1.0 if valor else 0.0
        if valor is NA:
            valor, clasif = "NO_APLICA", "[ESTIMACIÓN]"
        pend = valor is None
        unidad = unidad or _unidad(variable)
        if unidad == "%" and isinstance(valor, (int, float)) and bloque != "parametros":
            valor = valor * 100.0                     # convención del repositorio (23): % = ×100
        self.filas.append({
            "bloque": bloque, "escala_aves_dia": E if E is not None else "-", "dias_semana": ds or "-",
            "dias_anio": CALENDARIOS.get(ds, "-") if ds else "-", "escenario": escenario or "-",
            "parametros": parametros or "-", "variable": variable,
            "valor": "PENDIENTE" if pend else (round(valor, 6) if isinstance(valor, float) else valor),
            "unidad": unidad, "periodo": _periodo(variable, periodo), "base": base, "cadena": cadena,
            "clasificacion": "[PENDIENTE DE VALIDACIÓN]" if pend else (clasif or "[ESTIMACIÓN]"),
            "tipo_kpi": tipo_kpi, "sumable": sumable, "capacidad_vehiculo": capacidad,
            "tipo_capacidad": tipo_capacidad, "fuente": FUENTE,
            "nota": nota or (NOTA_ALCANCE if any(x in variable for x in ("alcance", "t_transporte_disponible",
                                                                         "ventana_prefaena", "alerta_prefaena")) else "")})

    def volcar(self, bloque, E, ds, escenario, parametros, res, periodo, claves=None, cadena="-", base="-",
               excluir=("faltantes",), capacidad="-", tipo_capacidad="-"):
        lista = sorted(res.get("faltantes", ())) if isinstance(res, dict) else []
        falt = ";".join(lista[:3]) + (f";+{len(lista) - 3} (ver parametros)" if len(lista) > 3 else "")
        for k_, v in res.items():
            if k_ in excluir or isinstance(v, (str, list, set, tuple)):
                continue
            if claves and k_ not in claves:
                continue
            cap_, tipo_ = (capacidad, tipo_capacidad) if depende_capacidad(k_) else ("-", "-")
            self.add(bloque, E, ds, escenario, parametros, k_, v, periodo, base=base, cadena=cadena,
                     nota=(f"faltante: {falt}" if v is None and falt else ""), capacidad=cap_, tipo_capacidad=tipo_)


PARAMETROS_TABLA = [  # (variable, valor, unidad, clasificación, referencia/nota)
    ("escalas_aves_faenadas_dia", "2500/5000/10000/20000", "aves", "[SUPUESTO]", "Leídas de 23_plan_expansion/modelo_escala.py (ESCALAS); no es escala elegida"),
    ("calendarios", "5 d=250 d; 6 d=300 d", "d", "[SUPUESTO]", "SUP-025"),
    ("peso_vivo_planta_kg", PESO, "kg", "[SUPUESTO]", "Perfil medio 03 (SUP-026/058)"),
    ("doa_base", DOA_BASE, "ratio", "[SUPUESTO]", "SUP-026; barrido 0,2-1,63 % (FTE-156 [PVDP])"),
    ("aves_por_camion_vivo", "4000/5500/7000", "aves/viaje", "[SUPUESTO]", "Capacidad de ESCENARIO (SUP-033 sin fuente; DPV-084); sin elección explícita = PENDIENTE; ninguna validada ni cotizada"),
    ("reduccion_carga_verano", "0.15 (0.10-0.25)", "ratio", "[SUPUESTO]", "SUP-097; 03: 1-2 aves menos por cajón"),
    ("radios_km", "25/50/100/150/200/300", "km", "[SUPUESTO]", "SUP-091: sensibilidad, NO radio óptimo"),
    ("factor_ruta", "1.2/1.3/1.4 (base 1.3)", "ratio", "[SUPUESTO]", "SUP-092; FTE-286 [PVDP]"),
    ("factor_distribucion", round(FACTOR_DISTRIBUCION, 6), "ratio", "[ESTIMACIÓN]", "SUP-093: media de puntos uniformes en un disco = 2R/3"),
    ("velocidad_aves_vivas_kmh", VEL_VIVO, "km/h", "[ESTIMACIÓN]", "03 transporte_aves.md §4 (60-70); sin fuente"),
    ("t_retiro_alimento_h", T_RETIRO_ALIMENTO_H, "h", "[SUPUESTO]", "SUP-095: retiro de alimento → inicio de captura; sin fuente (DPV-127)"),
    ("t_captura_carga_h", T_CAPTURA_CARGA_H, "h", "[SUPUESTO]", "SUP-095 sin fuente (DPV-127)"),
    ("t_espera_granja_h", T_ESPERA_GRANJA_H, "h", "[SUPUESTO]", "SUP-095: sin espera adicional en granja (barrido 0-1 h)"),
    ("t_espera_planta_h", T_ESPERA_PLANTA_H, "h", "[SUPUESTO]", "SUP-095 sin fuente"),
    ("t_descarga_h", T_DESCARGA_H, "h", "[SUPUESTO]", "SUP-095: descarga/colgado; sin fuente"),
    ("t_lavado_desinfeccion_h", T_LAVADO_H, "h", "[SUPUESTO]", "SUP-095: duración sin fuente. La obligación de lavar y desinfectar superficies a cada viaje proviene de la Res. SENASA 723/2025 (FTE-234, confirmada en revisión externa); la resolución no fija duración"),
    ("ventana_prefaena_escenario_h", VENTANA_PREFAENA_H, "h", "[SUPUESTO]", "SUP-095: parámetro de ESCENARIO dentro del rango 8-12 h citado como práctica (FTE-156 [PVDP]); NO es un máximo normativo (sin fuente primaria que lo establezca)"),
    ("dias_cosecha_referencia", DIAS_COSECHA_REFERENCIA, "d", "[ESTIMACIÓN]", "03 transporte_aves.md §5: granja de 15-30 mil aves se vacía en 1-2 noches; solo dispara una alerta POTENCIAL"),
    ("horas_utiles_camion_dia", HORAS_CAMION_DIA, "h", "[SUPUESTO]", "SUP-098"),
    ("horas_netas_faena", HORAS_NETAS, "h", "[SUPUESTO]", "23 / 05 (DEC-036)"),
    ("merma_viaje_por_h", "0/0.002/0.005", "ratio", "[ESTIMACIÓN]", "03 transporte_aves.md §3; 0 = SUP-058"),
    ("plazas_por_granja", "15000/30000/60000", "aves", "[ESTIMACIÓN]", "03 transporte_aves.md §5 (15-30 mil); 60 mil = barrido; DPV-048"),
    ("cap_granelero_t", CAP_GRANELERO_T, "t", "[ESTIMACIÓN]", "03 alimentacion.md, sin fuente; DPV-084"),
    ("cap_camion_pollitos", None, "pollitos", "[PENDIENTE DE VALIDACIÓN]", "DPV-047/084; barrido 20/40/80 mil solo ilustrativo"),
    ("cap_camion_refrigerado_t", None, "t", "[PENDIENTE DE VALIDACIÓN]", "DPV-084; barrido 3/6/12/20 t (no estándar)"),
    ("cap_camion_congelado_t", None, "t", "[PENDIENTE DE VALIDACIÓN]", "DPV-084; barrido 3/6/12/20 t"),
    ("cap_vehiculo_subproductos_t", None, "t", "[PENDIENTE DE VALIDACIÓN]", "DPV-084; barrido 5/10/20 t"),
    ("carga_contenedor_reefer_t", CONTENEDOR_T, "t", "[PVDP]", "FTE-135 (24-27 t, débil)"),
    ("kg_por_pallet", None, "kg", "[PENDIENTE DE VALIDACIÓN]", "DPV-129; barrido 500/750/1000"),
    ("kg_cama_m2", None, "kg", "[PENDIENTE DE VALIDACIÓN]", "DPV-130"),
    ("kg_envase_por_kg", None, "ratio", "[PENDIENTE DE VALIDACIÓN]", "DPV-129"),
    ("consumo_combustible_l_km", None, "índice", "[PENDIENTE DE VALIDACIÓN]", "DPV-131"),
    ("dias_despacho_semana", "5/6/7", "d", "[SUPUESTO]", "SUP-099"),
    ("desfase_despacho_d", DESFASE_DESPACHO, "d", "[SUPUESTO]", "SUP-099"),
    ("dist_planta_mercado_km", "30/150/300/600/1000", "km", "[SUPUESTO]", "SUP-091 (sin localización; 12A)"),
    ("velocidad_troncal_kmh", VEL_TRONCAL, "km/h", "[SUPUESTO]", "SUP-094 sin fuente"),
    ("velocidad_urbana_kmh", VEL_URBANA, "km/h", "[SUPUESTO]", "SUP-094 sin fuente"),
    ("t_parada_h", T_PARADA_H, "h", "[SUPUESTO]", "SUP-100 sin fuente"),
    ("km_entre_paradas", KM_ENTRE_PARADAS, "km", "[SUPUESTO]", "SUP-100 sin fuente"),
    ("paradas_ruta_max", "6/10/15", "paradas", "[SUPUESTO]", "SUP-100 barrido"),
    ("conduccion_max_h", CONDUCCION_MAX_H, "h", "[PVDP]", "CCT 40/89 (FTE-287): 8 h urbano, 10 h media/larga distancia"),
    ("ventana_recepcion_h", None, "h", "[PENDIENTE DE VALIDACIÓN]", "DPV-036"),
    ("entregas_semana_local", "3/6", "índice", "[SUPUESTO]", "02 supermercados.md §3.1"),
    ("kg_local_dia", "25/50/100/150/300", "kg", "[SUPUESTO]", "02 escenarios_demanda.csv RED-xxx; demanda NO validada"),
    ("fraccion_locales_A_B_C", "0/0.5/1", "ratio", "[SUPUESTO]", "SUP-085: escenarios logísticos; volumen variable"),
    ("n_centros_distribucion", None, "índice", "[PENDIENTE DE VALIDACIÓN]", "DPV-036"),
    ("dist_crossdock_tiendas_km", DIST_CROSSDOCK_KM, "km", "[SUPUESTO]", "SUP-100 (15-40)"),
    ("reparto_otros_canales", "ESC-BAS", "ratio", "[SUPUESTO]", "SUP-102: leído de 02 (ilustrativo)"),
    ("cuota_exportacion", "0.10/0.20/0.50", "ratio", "[SUPUESTO]", "Barrido; P3 = 20 % (SUP-055); demanda de exportación = 0 (SUP-022)"),
    ("dist_planta_puerto_km", "30/150/300/600/1000", "km", "[SUPUESTO]", "SUP-091 (sin puerto elegido)"),
    ("transito_maritimo_d", "20-45", "d", "[PVDP]", "17 logistica_exportacion.md §4 (débil)"),
    ("espera_terminal_d", None, "d", "[PENDIENTE DE VALIDACIÓN]", "DPV-027"),
    ("dias_max_refrigerado_subproductos", None, "d", "[PENDIENTE DE VALIDACIÓN]", "SUP-101 / DPV-128 [PVDP]"),
    ("backhaul_aplicado", 0, "ratio", "[SUPUESTO]", "SUP-103: 0 salvo evidencia; BACKHAUL_AVES = false como supuesto conservador, NO como prohibición normativa"),
    ("cap_vehiculo_subproductos_m3", None, "m³", "[PENDIENTE DE VALIDACIÓN]", "DPV-135: capacidad volumétrica útil"),
    ("densidad_aparente_subproductos_t_m3", None, "t/m³", "[PENDIENTE DE VALIDACIÓN]", "DPV-135: por corriente (plumas, sangre, vísceras, cabezas, decomisos); sin ella no se calcula ocupación volumétrica"),
]

# Variables por bloque: las que NO dependen de la capacidad del vehículo se escriben una sola vez
VIVO_FLUJO = ["aves_cargadas_dia", "aves_doa_dia", "aves_doa_anio", "t_vivo_cargado_dia", "kg_vivo_faenable_dia",
              "kg_doa_dia", "aves_por_hora_neta"]
VIVO_CAMION = ["capacidad_efectiva_aves", "viajes_equivalentes_dia", "viajes_dia", "ocupacion", "t_por_viaje",
               "km_cargado_dia", "km_retorno_sin_carga_comercial_dia", "km_total_dia", "pct_km_sin_carga_comercial",
               "t_km_dia", "km_por_ave", "km_por_t_vivo", "tiempo_ciclo_h", "ciclos_posibles_por_camion_jornada",
               "camion_horas_dia", "camion_dia", "flota_minima", "utilizacion_flota", "utilizacion_semanal_flota",
               "intervalo_arribos_h", "ave_horas_transito_dia"]
VIVO_RUTA = ["distancia_geo_media_km", "distancia_ruta_media_km", "distancia_ruta_max_km",
             "t_retiro_alimento_h", "t_captura_carga_h", "t_espera_granja_h", "t_transporte_medio_h",
             "t_transporte_max_h", "t_espera_planta_h", "t_descarga_h", "t_total_prefaena_medio_h",
             "t_total_prefaena_max_h", "ventana_prefaena_escenario_h", "alerta_prefaena_excede_ventana_medio",
             "alerta_prefaena_excede_ventana_max", "t_ida_h", "t_regreso_h", "t_lavado_h", "tiempo_ciclo_h"]
VIVO_ALCANCE = ["t_total_prefaena_max_h", "t_transporte_disponible_escenario_h", "alcance_ruta_escenario_km",
                "alcance_geo_escenario_km", "alerta_prefaena_excede_ventana_max", "tiempo_ciclo_h"]
PT_FLUJO = ["t_dia_op", "t_semana", "despachos_semana", "t_dia_despacho", "stock_ciclo_max_t", "tiempo_ciclo_h"]
PT_CAMION = ["viajes_dia_despacho", "viajes_semana", "ocupacion", "km_dia_despacho", "km_por_t", "camion_dia"]
SUB_FLUJO = ["t_dia_op", "t_semana", "m3_dia_op", "dias_acumulados", "t_por_retiro", "m3_por_retiro",
             "retiros_semana", "stock_refrigerado_max_t", "fisicamente_posible", "sanitariamente_permitido",
             "aceptado_por_receptor", "requiere_frio", "riesgo_olores_degradacion_aumentado"]
SUB_CAMION = ["viajes_por_retiro_criterio_masa", "viajes_semana_criterio_masa", "ocupacion_masica",
              "km_semana_criterio_masa", "dias_faena_para_llenar_capacidad_masica",
              "viajes_por_retiro_criterio_volumen", "ocupacion_volumetrica", "viajes_por_retiro_vinculante"]
RED_VARS = ["locales", "demanda_red_t_dia_cal", "t_dia_despacho", "kg_por_parada_tienda", "paradas_tienda_semana",
            "paradas_planta_dia", "viajes_troncal_dia", "ocupacion_troncal", "rutas_min_por_paradas",
            "rutas_reparto_dia", "paradas_por_ruta", "paradas_max_por_jornada", "ocupacion_reparto",
            "h_conduccion_troncal", "h_conduccion_reparto", "h_ruta_reparto", "tramo_entregas_h",
            "excede_conduccion", "excede_jornada", "inviable_en_jornada", "excede_ventana",
            "km_dia_despacho", "km_por_t", "camion_horas_dia"]
RED_SENS = ["t_dia_despacho", "kg_por_parada_tienda", "viajes_troncal_dia", "rutas_reparto_dia",
            "paradas_max_por_jornada", "paradas_por_ruta", "inviable_en_jornada", "excede_jornada",
            "km_dia_despacho", "km_por_t", "camion_horas_dia"]
INV_CICLO = ["produccion_semana_t", "despacho_semana_t", "despacho_t_dia_despacho", "stock_ciclo_max_t",
             "stock_ciclo_medio_t", "viajes_dia_despacho", "viajes_semana", "ocupacion"]
INV_SEG = ["stock_seguridad_t", "stock_total_max_t", "t_dias_inmovilizadas_semana"]
EXP_FLUJO = ["cuota_exportacion", "carga_contenedor_t", "export_t_dia_op", "export_t_anio",
             "dias_faena_llenar_contenedor", "dias_calendario_llenar_contenedor", "contenedores_mes",
             "contenedores_anio_enteros", "utilizacion_carga_contenedores", "viajes_terrestres_anio",
             "espera_terminal_d", "transito_maritimo_d_min", "transito_maritimo_d_max", "stock_consolidacion_max_t",
             "lead_time_total_max_d"]
EXP_RUTA = ["h_terrestre_planta_puerto", "km_terrestre_anio"]

# Base de la sensibilidad directo / CD / cross-dock (SUP-100/085): un parámetro por vez
RED_BASE = {"escenario": "C", "kg_local_dia": 100, "entregas_semana": 3, "dist_mercado_km": 300,
            "paradas_ruta_max": 10, "cap_reparto": 6, "cap_troncal": 20, "t_parada": T_PARADA_H,
            "horas_camion_dia": HORAS_CAMION_DIA}
RED_BARRIDOS = {"dist_mercado_km": (30, 100, 150, 300, 600), "paradas_ruta_max": (6, 10, 15),
                "kg_local_dia": (25, 100, 300), "cap_reparto": (3, 6, 12), "t_parada": (0.5, 0.75, 1.0),
                "horas_camion_dia": (10, 12, 14)}
# Barrido de la ventana prefaena (un parámetro por vez; base = constantes SUP-095)
PREFAENA_BARRIDOS = {"ventana_prefaena": (8, 10, 12), "t_retiro_alimento": (2, 3, 4),
                     "t_captura_carga": (1.0, 1.5, 2.5), "t_espera_granja": (0.0, 0.5, 1.0),
                     "t_espera_planta": (0.5, 0.75, 2.0)}


def _cap_txt(cap):
    return "PENDIENTE" if cap is None else f"{cap} (barrido)"


def _cap_col(cap, unidad, tipo="ESCENARIO"):
    """(capacidad_vehiculo, tipo_capacidad): capacidad de ESCENARIO elegida o PENDIENTE."""
    return ("PENDIENTE", "PENDIENTE") if cap is None else (f"{cap} {unidad}", tipo)


def construir():
    t = Tabla()
    for var, val, uni, cla, ref in PARAMETROS_TABLA:
        t.add("parametros", None, None, None, "-", var, None if isinstance(val, str) else val, "-",
              clasif=cla, nota=ref, unidad=uni)
        t.filas[-1]["periodo"] = "-"
        if isinstance(val, str):          # barridos y rangos: se guardan como texto (no son PENDIENTES)
            t.filas[-1]["valor"] = val
            t.filas[-1]["clasificacion"] = cla
    for flujo, (estado, motivo) in BACKHAUL_POSIBLE.items():
        t.add("backhaul", None, None, flujo, f"BACKHAUL_POSIBLE={estado}; retorno: {TIPO_RETORNO[flujo]}",
              "fraccion_retorno_cargado_aplicada", 0.0, "viaje", clasif="[SUPUESTO]", unidad="ratio",
              nota=f"{motivo}. Backhaul comercial solo con evidencia (carga identificada o contrato)")

    ds = 5
    for E in ESCALAS:
        # --- aves vivas: flujo (no depende del camión)
        t.volcar("aves_vivas_flujo", E, ds, "-", f"doa={DOA_BASE}", aves_vivas(E, ds), "dia_operativo",
                 claves=VIVO_FLUJO, base="vivo")
        # --- camión × radio × estación (capacidad de ESCENARIO explícita); sin capacidad elegida = PENDIENTE
        for R in RADIOS_KM:
            for cap in ((None,) if R == 100 else ()) + tuple(AVES_CAMION):
                for est, red in ESTACIONES.items():
                    if cap is None and est == "verano":
                        continue
                    r = aves_vivas(E, ds, aves_camion=cap, reduccion=red, radio_km=R)
                    capv, tipo = _cap_col(cap, "aves/camión")
                    t.volcar("aves_vivas", E, ds, est, f"radio_km={R}; aves_por_camion={_cap_txt(cap)}", r,
                             "dia_operativo", claves=VIVO_CAMION, base="vivo", capacidad=capv, tipo_capacidad=tipo)
        # --- secuencia prefaena y ciclo por radio y factor de ruta (no dependen del camión ni de la escala:
        #     se escriben una sola vez, en la fila de 10.000 aves/día)
        for fr in (FACTOR_RUTA if E == 10000 else ()):
            for R in RADIOS_KM:
                r = aves_vivas(E, ds, radio_km=R, factor_ruta=fr)
                t.volcar("aves_vivas_ruta", E, ds, "-", f"factor_ruta={fr}; radio_km={R}", r, "viaje",
                         claves=VIVO_RUTA, base="vivo")
        for doa in DOA_BARRIDO:
            for cap in (4000, 7000):
                r = aves_vivas(E, ds, doa=doa, aves_camion=cap)
                capv, tipo = _cap_col(cap, "aves/camión")
                t.volcar("aves_vivas_doa", E, ds, "-", f"doa={doa}; aves_por_camion={cap} (barrido)", r,
                         "dia_operativo", claves=["aves_cargadas_dia", "aves_doa_dia", "aves_doa_anio", "kg_doa_dia",
                                                  "viajes_equivalentes_dia", "viajes_dia", "ocupacion"],
                         base="vivo", capacidad=capv, tipo_capacidad=tipo)
        for m in MERMA_H_BARRIDO:
            for R in (50, 150, 300):
                r = aves_vivas(E, ds, radio_km=R, merma_h=m)
                t.volcar("aves_vivas_merma", E, ds, "-", f"merma_por_h={m}; radio_km={R}", r, "dia_operativo",
                         claves=["merma_viaje_frac", "kg_merma_viaje_dia", "t_vivo_cargado_dia",
                                 "kg_vivo_faenable_dia"], base="vivo")
        for pg in PLAZAS_GRANJA:
            capv, tipo = _cap_col(AVES_CAMION_BASE, "aves/camión")
            t.volcar("granjas", E, ds, "-", f"plazas_por_granja={pg} (DPV-048); aves_por_camion=5500 (barrido); "
                     f"cadencia de retiro = ritmo de faena modelado", aves_vivas(E, ds, plazas_granja=pg,
                                                                                aves_camion=AVES_CAMION_BASE),
                     "dia_operativo", claves=["granjas_equivalentes", "aves_cargadas_por_cosecha", "cosechas_semana",
                                              "dias_faena_por_cosecha", "alerta_cosecha_prolongada_potencial",
                                              "viajes_por_cosecha", "ciclos_anio_por_granja"],
                     capacidad=capv, tipo_capacidad=tipo)
            for f in t.filas[-8:]:
                if f["variable"] in ("alerta_cosecha_prolongada_potencial", "dias_faena_por_cosecha"):
                    f["nota"] = ("Incompatibilidad operativa POTENCIAL si el lote se retira con la cadencia modelada; "
                                 "validar retiros parciales, all-in/all-out, tamaño real de lote y programación "
                                 "entre granjas (DPV-133). Referencia 1-2 noches: 03 [ESTIMACIÓN]")
        # --- insumos (granelero: capacidad de ESCENARIO de 03, pasada explícitamente)
        for dfab in DIST_FABRICA_KM:
            capv, tipo = _cap_col(CAP_GRANELERO_T, "t (granelero)", "ESCENARIO [ESTIMACIÓN 03]")
            t.volcar("insumos_alimento", E, ds, "-", f"cap_granelero_t=28 ([ESTIMACIÓN] 03); dist_fabrica_km={dfab}",
                     insumos(E, ds, cap_granelero=CAP_GRANELERO_T, dist_fabrica=dfab), "semana_plena", base="alimento",
                     claves=["alimento_t_semana_plena", "alimento_t_dia_7d", "alimento_viajes_semana",
                             "alimento_viajes_dia_7d", "alimento_ocupacion", "alimento_km_semana"],
                     capacidad=capv, tipo_capacidad=tipo)
        t.volcar("insumos_otros", E, ds, "-", "capacidades y coeficientes sin dato = PENDIENTE", insumos(E, ds),
                 "semana_plena", claves=["pollitos_semana_plena", "pollitos_viajes_semana", "pollitos_km_semana",
                                         "m2_galpon", "ciclos_anio", "cama_t_lote", "envases_t_dia", "pallets_dia",
                                         "combustible_l_semana"], capacidad="PENDIENTE", tipo_capacidad="PENDIENTE")
        for cp in CAP_POLLITOS_BARRIDO:
            capv, tipo = _cap_col(cp, "pollitos/camión")
            t.volcar("insumos_pollitos_barrido", E, ds, "-", f"cap_pollitos={cp} (barrido ilustrativo, NO dato); "
                     f"dist_incubadora_km=150", insumos(E, ds, cap_pollitos=cp), "semana_plena",
                     claves=["pollitos_viajes_semana", "pollitos_ocupacion", "pollitos_km_semana"],
                     capacidad=capv, tipo_capacidad=tipo)
        for kp in KG_POR_PALLET_BARRIDO:
            t.volcar("insumos_pallets_barrido", E, ds, "-", f"kg_por_pallet={kp} (barrido ilustrativo)",
                     insumos(E, ds, kg_pallet=kp), "dia_operativo", claves=["pallets_dia"], base="comercial")
        # --- producto terminado: refrigerado y congelado SEPARADOS (frecuencias propias)
        for perfil in PERFILES:
            for cad, frecs in (("refrigerado", DIAS_DESPACHO), ("congelado", DESPACHOS_CONGELADO)):
                for dd in frecs:
                    for cap in (None,) + CAP_TRONCAL_BARRIDO:
                        r = producto(E, ds, perfil=perfil, dias_despacho=dd, despachos_congelado=dd,
                                     cap_refrigerado=cap, cap_congelado=cap, dist_km=300)
                        par = f"perfil={perfil}; despachos_semana={dd}; dist_km=300; config=B"
                        res = {k_[len(cad) + 1:]: v for k_, v in r.items() if k_.startswith(cad + "_")}
                        res["faltantes"] = r["faltantes"]
                        if cap is None:
                            t.volcar("producto_terminado", E, ds, perfil, par, res, "dia_despacho", claves=PT_FLUJO,
                                     cadena=cad, base="comercial")
                        capv, tipo = _cap_col(cap, "t/camión")
                        t.volcar("producto_terminado", E, ds, perfil, f"{par}; cap_t={_cap_txt(cap)}", res,
                                 "dia_despacho", claves=PT_CAMION, cadena=cad, base="comercial",
                                 capacidad=capv, tipo_capacidad=tipo)
            t.add("producto_terminado", E, ds, perfil, "config=B", "exportacion_t_dia_op",
                  producto(E, ds, perfil=perfil)["exportacion_t_dia_op"], "dia_operativo", base="comercial",
                  cadena="exportacion", nota="ver bloque exportacion (contenedores)")
        for cfg in CONFIGS:
            t.add("producto_config", E, ds, cfg, "perfil=P1", "comestible_t_dia_op",
                  producto(E, ds, config=cfg)["comestible_t_dia_op"], "dia_operativo", base="comercial",
                  nota="A entero / B trozado / C deshuesado (07): cambia t y flujos, no la lógica de viajes")
        # --- asignación red / canales / exportación (día calendario)
        for esc in ANCLA:
            for kl in ((100,) if esc == "A" else (50, 100, 150)):
                for perfil in ("P1", "P3"):
                    t.volcar("asignacion_canales", E, ds, esc, f"kg_local_dia={kl}; perfil={perfil}",
                             asignacion(E, ds, perfil=perfil, escenario=esc, kg_local_dia=kl), "dia_calendario",
                             base="comercial")
        # --- inventario: ciclo semanal (despacho) y stock de seguridad (dos bases) separados
        com = producto(E, ds)["comestible_t_dia_op"]
        for dsf in CALENDARIOS:
            for dd in DIAS_DESPACHO:
                r = inventario(com, dsf, dd, 0, cap=12)
                capv, tipo = _cap_col(12, "t/camión")
                t.volcar("inventario_ciclo", E, dsf, "-", f"dias_despacho={dd}; desfase=1 d; cap_t=12 (barrido)", r,
                         "dia_despacho", claves=INV_CICLO, base="comercial", capacidad=capv, tipo_capacidad=tipo)
            for seg in (1, 3, 7, 14):
                for base in ("produccion", "calendario"):
                    r = inventario(com, dsf, 6, seg, base)
                    t.volcar("inventario_seguridad", E, dsf, base, f"dias_seguridad={seg}; dias_despacho=6", r, "stock",
                             claves=INV_SEG, base="comercial")
        # --- exportación: SENSIBILIDAD (no es estrategia comercial; demanda de exportación = 0, SUP-022)
        for q in CUOTAS_EXPORT:
            capv, tipo = _cap_col(CONTENEDOR_T, "t/contenedor reefer 40'", "ESCENARIO [PVDP]")
            t.volcar("exportacion", E, ds, "SENSIBILIDAD", f"cuota_exportada={q}; carga_t=25 [PVDP]",
                     exportacion(E, ds, cuota=q), "anio", claves=EXP_FLUJO, cadena="congelado", base="comercial",
                     capacidad=capv, tipo_capacidad=tipo)
            for dp in DIST_PUERTO_KM:
                t.volcar("exportacion_ruta", E, ds, "SENSIBILIDAD", f"cuota_exportada={q}; dist_puerto_km={dp}",
                         exportacion(E, ds, cuota=q, dist_puerto_km=dp), "anio", claves=EXP_RUTA, cadena="congelado",
                         capacidad=capv, tipo_capacidad=tipo)
        # --- subproductos: corrientes, coproductos comestibles y estrategias de retiro
        for cfg in ("B", "C"):
            tt, tot, coprod = corrientes_subproductos(E, cfg)
            for c, v in tt.items():
                et, est, veh, grp, vida = CORRIENTES[c]
                t.add("subproductos_corrientes", E, ds, cfg, f"corriente={c}; grupo={grp}", "t_dia_op", v,
                      "dia_operativo", base="biologica+agua", cadena="subproducto", sumable="si",
                      nota=f"{et}; {est}; {veh}; vida sin frío: {vida}; densidad aparente, temperatura y "
                           f"acondicionamiento PENDIENTES (DPV-135)")
            t.add("subproductos_corrientes", E, ds, cfg, "total", "solidos_a_retirar_t_dia_op", tot, "dia_operativo",
                  base="biologica+agua", cadena="subproducto", nota="= suma de corrientes (L04); 23 §12")
            for c, v in coprod.items():
                t.add("coproductos_frio", E, ds, cfg, f"coproducto={c}", "t_dia_op", v, "dia_operativo",
                      base="comercial", cadena="refrigerado/congelado",
                      nota="Comestible (ya incluido en producto terminado): NO sumar; sin comprador → rendering (SUP-046)")
            objetivos = sorted({v[3] for v in CORRIENTES.values()}) + (list(CORRIENTES) if cfg == "B" else [])
            for c in objetivos:
                for est in (ESTRATEGIAS if c.startswith("G") else ("E1",)):   # E2/E3 por grupo (E4)
                    esc = ("E4-" + est) if c.startswith("G") else est
                    base_par = f"config={cfg}; corriente={c}; dist_receptor_km=50"
                    r0 = subproductos(E, ds, cfg, est, cap=None, corriente=c)
                    if r0["t_dia_op"] == 0:
                        continue
                    t.volcar("subproductos_retiro", E, ds, esc, base_par, r0, "retiro", claves=SUB_FLUJO,
                             cadena="subproducto", base="biologica+agua")
                    caps = ((None,) if E == 10000 and cfg == "B" else ()) + CAP_SUBPROD_BARRIDO
                    for cap in caps:
                        r = subproductos(E, ds, cfg, est, cap=cap, corriente=c)
                        capv = "PENDIENTE" if cap is None else f"{cap} t (másica); m³ PENDIENTE"
                        t.volcar("subproductos_retiro", E, ds, esc, f"{base_par}; cap_t={_cap_txt(cap)}; cap_m3=PENDIENTE",
                                 r, "retiro", claves=SUB_CAMION, cadena="subproducto", base="biologica+agua",
                                 capacidad=capv, tipo_capacidad="PENDIENTE" if cap is None else "ESCENARIO")
        t.add("subproductos_corrientes", E, ds, "B", "corriente=DOA", "kg_doa_dia", aves_vivas(E, ds)["kg_doa_dia"],
              "dia_operativo", base="vivo", cadena="subproducto",
              nota="Aves muertas en transporte: fuera del balance (SUP-035); destino restringido (07 rendering.md §2)")
    # --- ventana prefaena: sensibilidad del tiempo de transporte disponible y del alcance (escala-independiente)
    for clave, valores in PREFAENA_BARRIDOS.items():
        for v in valores:
            r = aves_vivas(10000, 5, **{clave: v})
            t.volcar("aves_vivas_prefaena_sens", None, None, "ESCENARIO", f"{clave}={v} (resto: base SUP-095)", r,
                     "lote", claves=VIVO_ALCANCE, base="vivo")
    # --- red ancla (no depende de la escala de la planta)
    for esc in ANCLA:
        kls = (100,) if esc == "A" else KG_LOCAL_DIA
        ents = (3,) if esc == "A" else ENTREGAS_SEMANA
        for kl in kls:
            for ent in ents:
                for modo in ("directo", "cd", "crossdock"):
                    for dm in (30, 300, 600):
                        r = red_ancla(esc, kl, ent, modo, cap_reparto=6, cap_troncal=20, dist_mercado_km=dm)
                        t.volcar("red_ancla", None, None, esc, f"kg_local_dia={kl}; entregas_semana={ent}; modo={modo}; "
                                 f"dist_mercado_km={dm} (resto: SUP-100, ver parametros)",
                                 r, "dia_despacho", claves=RED_VARS, cadena="refrigerado", base="comercial",
                                 capacidad="reparto 6 t / troncal 20 t", tipo_capacidad="ESCENARIO")
    # --- sensibilidad directo / CD / cross-dock: un parámetro por vez alrededor de RED_BASE
    for clave, valores in RED_BARRIDOS.items():
        for v in valores:
            p_ = dict(RED_BASE, **{clave: v})
            for modo in ("directo", "cd", "crossdock"):
                r = red_ancla(p_["escenario"], p_["kg_local_dia"], p_["entregas_semana"], modo,
                              paradas_ruta_max=p_["paradas_ruta_max"], cap_reparto=p_["cap_reparto"],
                              cap_troncal=p_["cap_troncal"], dist_mercado_km=p_["dist_mercado_km"],
                              t_parada=p_["t_parada"], horas_camion_dia=p_["horas_camion_dia"])
                par = f"base RED_BASE (C; 100 kg; 3 ent/sem; 300 km; 10 paradas; 6/20 t; 0,75 h; 12 h)"
                t.volcar("red_ancla_sensibilidad", None, None, f"{clave}={v}", f"modo={modo}; {par}", r,
                         "dia_despacho", claves=RED_SENS, cadena="refrigerado", base="comercial",
                         capacidad=f"reparto {p_['cap_reparto']} t / troncal {p_['cap_troncal']} t",
                         tipo_capacidad="ESCENARIO")
    # --- KPI de resumen por escala (caso de referencia de sensibilidad)
    for E in ESCALAS:
        for k_, v, per, capv in kpis_escala(E):
            t.add("kpi_resumen", E, 5, "referencia", "radio 100 km; P1; refrigerado 6 y congelado 2 despachos/sem",
                  k_, v, per, tipo_kpi="fisico", capacidad=capv,
                  tipo_capacidad="ESCENARIO" if depende_capacidad(k_) else "-",
                  nota="Caso de sensibilidad, NO escenario recomendado ni requerimiento de flota")
            if not depende_capacidad(k_):
                t.filas[-1]["capacidad_vehiculo"] = "-"
    return t


def kpis_escala(E):
    """KPI físicos de un caso de referencia de sensibilidad (no es escenario recomendado). Cada KPI lleva la
    capacidad de ESCENARIO que lo produce."""
    v = aves_vivas(E, 5, radio_km=100, aves_camion=AVES_CAMION_BASE)
    p = producto(E, 5, perfil="P1", dias_despacho=6, cap_refrigerado=12, cap_congelado=12, despachos_congelado=2)
    s = subproductos(E, 5, "B", "E1", cap=10, corriente="G3-visceras")
    sp = subproductos(E, 5, "B", "E1", cap=10, corriente="G1-plumas")
    i = insumos(E, 5, cap_granelero=CAP_GRANELERO_T)
    cv, ct, cg, cs = "5500 aves/camión", "12 t/camión", "28 t (granelero)", "10 t (másica); m³ PENDIENTE"
    return [
        ("vivo_viajes_dia", v["viajes_dia"], "dia_operativo", cv), ("vivo_ocupacion", v["ocupacion"], "dia_operativo", cv),
        ("vivo_km_por_ave", v["km_por_ave"], "dia_operativo", cv), ("vivo_km_por_t_vivo", v["km_por_t_vivo"], "dia_operativo", cv),
        ("vivo_pct_km_sin_carga_comercial", v["pct_km_sin_carga_comercial"], "dia_operativo", cv),
        ("vivo_tiempo_ciclo_h", v["tiempo_ciclo_h"], "viaje", "-"),
        ("vivo_flota_minima", v["flota_minima"], "dia_operativo", cv),
        ("vivo_utilizacion_flota", v["utilizacion_flota"], "dia_operativo", cv),
        ("vivo_utilizacion_semanal_flota", v["utilizacion_semanal_flota"], "semana", cv),
        ("refrigerado_viajes_dia_despacho", p["refrigerado_viajes_dia_despacho"], "dia_despacho", ct),
        ("refrigerado_ocupacion", p["refrigerado_ocupacion"], "dia_despacho", ct),
        ("congelado_viajes_dia_despacho", p["congelado_viajes_dia_despacho"], "dia_despacho", ct),
        ("congelado_ocupacion", p["congelado_ocupacion"], "dia_despacho", ct),
        ("alimento_viajes_semana", i["alimento_viajes_semana"], "semana", cg),
        ("visceras_ocupacion_masica_retiro_diario", s["ocupacion_masica"], "retiro", cs),
        ("plumas_ocupacion_masica_retiro_diario", sp["ocupacion_masica"], "retiro", cs),
        ("plumas_ocupacion_volumetrica_retiro_diario", sp["ocupacion_volumetrica"], "retiro", cs),
    ]


def escribir_csv(t, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(t.filas)


# ---------------------------------------------------------------------------
# 12. PRUEBAS (L01-L20 originales; L21-L28 auditoría de interpretación)
# ---------------------------------------------------------------------------
def _cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _leer_csv_escala():
    ruta = os.path.join(RAIZ, "23_plan_expansion", "escenarios_escala.csv")
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def ejecutar_tests(verbose=True, tabla=None):
    res = []

    def ok(nombre, cond, detalle=""):
        res.append((nombre, bool(cond), detalle))

    def lanza(f, *a, **kw):
        try:
            f(*a, **kw)
        except ErrorLogistica:
            return True
        return False

    # L01 conservación de masa viva: cargado = faenable + DOA + merma
    errs = 0
    for E in ESCALAS:
        for doa in DOA_BARRIDO:
            for m in MERMA_H_BARRIDO:
                for R in RADIOS_KM:
                    r = aves_vivas(E, 5, doa=doa, merma_h=m, radio_km=R)
                    if not _cerca(r["kg_vivo_cargado_dia"], r["kg_vivo_faenable_dia"] + r["kg_doa_dia"] + r["kg_merma_viaje_dia"]):
                        errs += 1
    ok("L01 conservación t vivas (cargado = faenable + DOA + merma)", errs == 0, f"{errs} errores")

    # L02 conservación en planta: vivo + agua = comestible + sólidos a retirar + efluente/pérdida
    errs = 0
    for cfg in CONFIGS:
        k, _ = me.kg_por_ave(cfg)
        if not _cerca(k["peso_vivo"] + k["agua_incorporada"],
                      k["comestible"] + k["solidos_a_retirar"] + k["efluente_o_perdida"], 1e-12):
            errs += 1
    ok("L02 conservación planta (entrada = producto + subproductos + efluente)", errs == 0)

    # L03 partición del producto y conservación semanal del despacho
    errs = 0
    for E in ESCALAS:
        for perfil in PERFILES:
            for dd in DIAS_DESPACHO:
                r = producto(E, 5, perfil=perfil, dias_despacho=dd, cap_refrigerado=6, cap_congelado=6)
                s = r["refrigerado_t_dia_op"] + r["congelado_t_dia_op"] + r["exportacion_t_dia_op"]
                if not _cerca(s, r["comestible_t_dia_op"]):
                    errs += 1
                for cad in ("refrigerado", "congelado"):
                    if not _cerca(r[f"{cad}_t_dia_despacho"] * dd, r[f"{cad}_t_dia_op"] * 5):
                        errs += 1
    ok("L03 refrigerado + congelado + exportación = comestible; despacho semanal = producción semanal", errs == 0)

    # L04 corrientes de subproductos = sólidos a retirar
    errs = 0
    for E in ESCALAS:
        for cfg in CONFIGS:
            tt, tot, _ = corrientes_subproductos(E, cfg)
            if not _cerca(sum(tt.values()), tot):
                errs += 1
            grupos = {v[3] for v in CORRIENTES.values()}
            sg = sum(subproductos(E, 5, cfg, "E1", corriente=g)["t_dia_op"] for g in grupos)
            if not _cerca(sg, tot):
                errs += 1
    ok("L04 conservación subproductos (corrientes y grupos = sólidos a retirar)", errs == 0)

    # L05 asignación: red + canales + exportación = comestible (calendario)
    errs = 0
    for E in ESCALAS:
        for esc in ANCLA:
            for kl in KG_LOCAL_DIA:
                for perfil in PERFILES:
                    a = asignacion(E, 5, perfil=perfil, escenario=esc, kg_local_dia=kl)
                    canales = sum(v for k_, v in a.items() if k_.startswith("canal_"))
                    if not _cerca(a["red_atendida_t_dia_cal"] + canales + a["exportacion_t_dia_cal"], a["comestible_t_dia_cal"]):
                        errs += 1
                    if a["red_atendida_t_dia_cal"] > a["demanda_red_t_dia_cal"] + TOL:
                        errs += 1
    ok("L05 conservación de la asignación por canal (sin vender más que la demanda)", errs == 0)

    # L06 redondeo de viajes
    errs = 0
    for x in (0, 1e-12, 0.3, 1.0, 1.0000000001, 2.5, 7.999999999999, 12.0):
        v = viajes_enteros(x)
        if not isinstance(v, int) or v < x - 1e-9 or v - x >= 1:
            errs += 1
    for E in ESCALAS:
        for cap in AVES_CAMION:
            r = aves_vivas(E, 5, aves_camion=cap)
            if r["viajes_dia"] != math.ceil(r["viajes_equivalentes_dia"] - 1e-9) or r["viajes_dia"] < r["viajes_equivalentes_dia"] - 1e-9:
                errs += 1
    ok("L06 viajes enteros = techo de equivalentes (0 carga → 0 viajes)", errs == 0 and viajes_enteros(0) == 0)

    # L07 capacidad > 0
    casos = [lambda: aves_vivas(10000, aves_camion=0), lambda: aves_vivas(10000, aves_camion=-5),
             lambda: insumos(10000, cap_granelero=0), lambda: producto(10000, cap_refrigerado=0),
             lambda: producto(10000, cap_congelado=-1), lambda: red_ancla("B", 100, cap_reparto=0),
             lambda: red_ancla("C", 100, modo="cd", cap_troncal=0), lambda: exportacion(10000, carga_t=0),
             lambda: subproductos(10000, cap=0, corriente="plumas"), lambda: inventario(10, cap=0),
             lambda: insumos(10000, kg_pallet=0)]
    ok("L07 capacidad ≤ 0 → error en todos los flujos", all(lanza(f) for f in casos))

    # L08 ocupación ≤ 100 % (y > 0 cuando hay viajes)
    occ = []
    for E in ESCALAS:
        for cap in AVES_CAMION:
            for est in ESTACIONES.values():
                occ.append(aves_vivas(E, aves_camion=cap, reduccion=est)["ocupacion"])
        for c in CAP_TRONCAL_BARRIDO:
            for perfil in PERFILES:
                r = producto(E, perfil=perfil, cap_refrigerado=c, cap_congelado=c)
                occ += [r["refrigerado_ocupacion"], r["congelado_ocupacion"]]
        for c in CAP_SUBPROD_BARRIDO:
            for cor in CORRIENTES:
                for est in ESTRATEGIAS:
                    occ.append(subproductos(E, 5, "C", est, cap=c, corriente=cor)["ocupacion_masica"])
        occ.append(insumos(E, cap_granelero=CAP_GRANELERO_T)["alimento_ocupacion"])
    for esc in ("B", "C"):
        for modo in ("directo", "crossdock", "cd"):
            r = red_ancla(esc, 300, 3, modo, cap_reparto=3, cap_troncal=12)
            occ += [r.get("ocupacion_reparto"), r.get("ocupacion_troncal")]
    occ = [o for o in occ if o is not None and o is not NA]
    ok("L08 0 < ocupación ≤ 100 %", all(0 < o <= 1 + 1e-12 for o in occ), f"{len(occ)} casos; máx {max(occ):.4f}")

    # L09 distancias nunca negativas
    casos = [lambda: aves_vivas(10000, radio_km=-1), lambda: insumos(10000, dist_fabrica=-5),
             lambda: producto(10000, dist_km=-1), lambda: red_ancla("B", 100, dist_mercado_km=-3),
             lambda: exportacion(10000, dist_puerto_km=-10), lambda: subproductos(10000, corriente="sangre", dist_receptor_km=-1),
             lambda: red_ancla("B", 100, km_entre_paradas=-1)]
    vals = [aves_vivas(E, radio_km=R, aves_camion=AVES_CAMION_BASE)[k_] for E in ESCALAS for R in RADIOS_KM
            for k_ in ("distancia_geo_media_km", "distancia_ruta_media_km", "km_total_dia")]
    ok("L09 distancia negativa → error; distancias y km ≥ 0", all(lanza(f) for f in casos) and min(vals) >= 0)

    # L10 inventario no se mezcla con despacho
    errs = 0
    for E in ESCALAS:
        com = me.kg_por_ave()[0]["comestible"] * E / 1000
        for dsf in CALENDARIOS:
            for dd in DIAS_DESPACHO:
                rs = [inventario(com, dsf, dd, seg, b, cap=12) for seg in (0, 3, 7, 14) for b in ("produccion", "calendario")]
                if len({r["viajes_dia_despacho"] for r in rs}) != 1 or len({round(r["despacho_t_dia_despacho"], 9) for r in rs}) != 1:
                    errs += 1
                for r in rs:
                    if not _cerca(r["produccion_semana_t"], r["despacho_semana_t"]) or r["stock_ciclo_max_t"] < -TOL:
                        errs += 1
    if tabla is not None:
        for f in tabla.filas:
            if f["bloque"].startswith("inventario") and f["variable"].startswith("stock") and (f["periodo"] != "stock" or f["sumable"] != "no"):
                errs += 1
    # dos bases: calendario = producción × días de faena / 365
    a = inventario(10, 5, 6, 7, "produccion")["stock_seguridad_t"]
    b = inventario(10, 5, 6, 7, "calendario")["stock_seguridad_t"]
    ok("L10 inventario separado del despacho (viajes no cambian con el stock; bases distintas)",
       errs == 0 and _cerca(b, a * 250 / 365))

    # L11 refrigerado / congelado separados
    r1 = producto(10000, perfil="P2", cap_refrigerado=6, cap_congelado=6)
    r2 = producto(10000, perfil="P2", cap_refrigerado=6, cap_congelado=20)
    sep = r1["refrigerado_viajes_dia_despacho"] == r2["refrigerado_viajes_dia_despacho"] \
        and r1["congelado_viajes_dia_despacho"] != r2["congelado_viajes_dia_despacho"]
    junta = viajes_enteros((r1["refrigerado_t_dia_despacho"] + r1["congelado_t_dia_despacho"]) / 6)
    sep = sep and r1["refrigerado_viajes_dia_despacho"] + r1["congelado_viajes_dia_despacho"] >= junta
    if tabla is not None:
        sep = sep and all(f["cadena"] in ("refrigerado", "congelado", "exportacion") for f in tabla.filas
                          if f["bloque"] == "producto_terminado")
    ok("L11 refrigerado y congelado con viajes, capacidad y filas separados", sep)

    # L12 escenarios A/B/C independientes
    base = {e: red_ancla(e, 100, 3, "directo", cap_reparto=6) for e in ANCLA}
    _ = red_ancla("B", 300, 6, "directo", cap_reparto=3, fraccion_locales=0.8)
    despues = {e: red_ancla(e, 100, 3, "directo", cap_reparto=6) for e in ANCLA}
    indep = all({k_: v for k_, v in base[e].items() if k_ != "faltantes"} ==
                {k_: v for k_, v in despues[e].items() if k_ != "faltantes"} for e in ANCLA)
    indep = indep and base["A"]["locales"] == 0 and base["A"]["paradas_tienda_semana"] == 0 \
        and base["A"]["km_dia_despacho"] == 0 and base["C"]["locales"] > base["B"]["locales"] > 0
    indep = indep and lanza(lambda: red_ancla("A", 100, fraccion_locales=0.3))
    indep = indep and base["A"]["ocupacion_reparto"] is NA and asignacion(10000, escenario="A")["cobertura_red"] is NA
    if tabla is not None:
        indep = indep and all(f["sumable"] == "no" for f in tabla.filas if f["bloque"] == "red_ancla")
    ok("L12 escenarios ancla A/B/C independientes y no sumables (A sin red)", indep)

    # L13 ningún faltante se rellena silenciosamente
    p = producto(10000)                       # capacidades PENDIENTES por defecto
    i = insumos(10000)
    s = subproductos(10000, corriente="plumas")
    e = exportacion(10000)
    cd = red_ancla("C", 100, modo="cd", cap_troncal=20)
    cond = p["refrigerado_viajes_dia_despacho"] is None and "cap_camion_refrigerado_t" in p["faltantes"] \
        and i["pollitos_viajes_semana"] is None and "cap_camion_pollitos" in i["faltantes"] \
        and i["pallets_dia"] is None and i["cama_t_lote"] is None and i["envases_t_dia"] is None \
        and s["viajes_semana_criterio_masa"] is None and s["ocupacion_masica"] is None \
        and aves_vivas(10000)["viajes_dia"] is None and "aves_por_camion_vivo" in aves_vivas(10000)["faltantes"] \
        and insumos(10000)["alimento_viajes_semana"] is None \
        and e["lead_time_total_max_d"] is None and "espera_terminal_d" in e["faltantes"] \
        and cd["paradas_planta_dia"] is None and "n_centros_distribucion" in cd["faltantes"] \
        and subproductos(10000, estrategia="E2", corriente="sangre")["sanitariamente_permitido"] is None
    if tabla is not None:
        pend = [f for f in tabla.filas if f["valor"] == "PENDIENTE"]
        cond = cond and len(pend) > 0 and all(f["clasificacion"] == "[PENDIENTE DE VALIDACIÓN]" for f in pend)
        cond = cond and not any(f["valor"] in ("", None, "nan") for f in tabla.filas)
    ok("L13 datos faltantes → PENDIENTE (nunca 0 ni valor por defecto)", cond)

    # L14 reproduce el modelo de escala (23 §12 y §11)
    filas23 = _leer_csv_escala()
    errs = 0
    n = 0
    for f in filas23:
        if f["bloque"] not in ("logistica", "inventario"):
            continue
        E, ds = int(f["escala_aves_dia"]), int(f["dias_semana"])
        v = float(f["valor"])
        if f["bloque"] == "logistica":
            if f["variable"] == "aves_vivas_cargadas_t_dia":
                n += 1
                errs += not _cerca(aves_vivas(E, ds)["t_vivo_cargado_dia"], v, 1e-6)
            elif f["variable"] == "producto_comestible_sale_t_dia":
                n += 1
                errs += not _cerca(producto(E, ds)["comestible_t_dia_op"], v, 1e-6)
            elif f["variable"] == "subproductos_solidos_salen_t_dia":
                n += 1
                errs += not _cerca(corrientes_subproductos(E)[1], v, 1e-6)
            elif f["variable"] == "alimento_a_granjas_t_dia_semana_plena":
                n += 1
                errs += not _cerca(insumos(E, ds)["alimento_t_dia_7d"], v, 1e-6)
            elif f["variable"] == "camiones_aves_vivas_dia":
                n += 1
                cap = int(f["parametro"].split("=")[1])
                errs += not _cerca(aves_vivas(E, ds, aves_camion=cap)["viajes_equivalentes_dia"], v, 1e-6)
        elif f["bloque"] == "inventario" and f["variable"] == "comestible_total_t":
            par = dict(x.strip().split("=") for x in f["parametro"].split(";"))
            com = producto(E, ds)["comestible_t_dia_op"]
            b = "produccion" if par["base_temporal"] == "dias_produccion" else "calendario"
            n += 1
            errs += not _cerca(inventario(com, ds, 6, int(par["dias"]), b)["stock_seguridad_t"], v, 1e-6)
    ok("L14 reproduce 23 (t vivas, comestible, sólidos, alimento, camiones, inventario dos bases)",
       errs == 0 and n >= 60, f"{n} cifras comparadas, {errs} diferencias")

    # L15 backhaul = 0 sin evidencia; con evidencia solo donde el estado lo admite; "NO" nunca
    b = aves_vivas(10000, aves_camion=AVES_CAMION_BASE)
    cond = _cerca(b["km_retorno_sin_carga_comercial_dia"], b["km_cargado_dia"]) \
        and lanza(km_retorno, 100, "aves_vivas", False, 0.5) and lanza(km_retorno, 100, "subproductos", False, 0.5) \
        and lanza(km_retorno, 100, "refrigerado_troncal", False, 0.5) \
        and _cerca(km_retorno(100, "refrigerado_troncal", True, 0.5), 50) \
        and all(v[0] in ESTADOS_BACKHAUL for v in BACKHAUL_POSIBLE.values())
    BACKHAUL_POSIBLE["_prueba_no"] = ("NO", "estado reservado a prohibición con fuente normativa")
    try:
        cond = cond and lanza(km_retorno, 100, "_prueba_no", True, 0.5)
    finally:
        del BACKHAUL_POSIBLE["_prueba_no"]
    ok("L15 backhaul = 0 sin evidencia; aves vivas y subproductos deshabilitados por defecto", cond)

    # L16 sin economía en variables y unidades
    if tabla is not None:
        malas = [f["variable"] for f in tabla.filas if me.PALABRAS_ECONOMICAS.search(f["variable"])
                 or me.PALABRAS_ECONOMICAS.search(f["unidad"])]
        malas += [f["unidad"] for f in tabla.filas if f["unidad"] not in UNIDADES_VALIDAS | {"m²"}]
        ok("L16 sin variables ni unidades económicas; unidades válidas", not malas, ";".join(sorted(set(malas))[:5]))
    else:
        ok("L16 sin variables ni unidades económicas", True, "(sin tabla)")

    # L17 escalas leídas del modelo aprobado
    cond = ESCALAS == [2500, 5000, 10000, 20000] and ESCALAS == list(me.ESCALAS)
    if tabla is not None:
        cond = cond and {f["escala_aves_dia"] for f in tabla.filas if f["bloque"] == "aves_vivas"} == set(ESCALAS)
    ok("L17 escalas = las aprobadas en 23 (sin escala nueva)", cond)

    # L18 distancia por ruta ≥ geográfica; factor < 1 rechazado
    cond = all(aves_vivas(10000, radio_km=R, factor_ruta=f)["distancia_ruta_media_km"] >=
               aves_vivas(10000, radio_km=R, factor_ruta=f)["distancia_geo_media_km"] for R in RADIOS_KM for f in FACTOR_RUTA)
    ok("L18 distancia por ruta ≥ distancia geográfica", cond and lanza(lambda: aves_vivas(10000, factor_ruta=0.9)))

    # L19 monotonía: más DOA → más aves cargadas y viajes no decrecientes; más radio → más km y ciclo
    cond = True
    for E in ESCALAS:
        prev = None
        for doa in sorted(DOA_BARRIDO):
            r = aves_vivas(E, doa=doa, aves_camion=AVES_CAMION_BASE)
            if prev and (r["aves_cargadas_dia"] <= prev["aves_cargadas_dia"] or r["viajes_dia"] < prev["viajes_dia"]):
                cond = False
            prev = r
        km = [aves_vivas(E, radio_km=R, aves_camion=AVES_CAMION_BASE)["km_total_dia"] for R in RADIOS_KM]
        cond = cond and all(b_ > a_ for a_, b_ in zip(km, km[1:]))
    ok("L19 monotonía DOA → aves y viajes; radio → km", cond)

    # L20 ventana prefaena coherente (tiempo de transporte disponible = ventana − tramos no de transporte)
    r = aves_vivas(10000, radio_km=300)
    r2 = aves_vivas(10000, radio_km=25)
    no_tr = T_RETIRO_ALIMENTO_H + T_CAPTURA_CARGA_H + T_ESPERA_GRANJA_H + T_ESPERA_PLANTA_H + T_DESCARGA_H
    cond = _cerca(r["t_transporte_disponible_escenario_h"], VENTANA_PREFAENA_H - no_tr) \
        and _cerca(r["t_total_prefaena_max_h"], no_tr + r["t_transporte_max_h"]) \
        and r["alerta_prefaena_excede_ventana_max"] == (1.0 if r["t_total_prefaena_max_h"] > VENTANA_PREFAENA_H else 0.0) \
        and r2["alerta_prefaena_excede_ventana_max"] == 0.0 \
        and aves_vivas(10000, ventana_prefaena=None)["t_transporte_disponible_escenario_h"] is None
    ok("L20 ventana prefaena desagregada y alerta coherente (sin ventana → PENDIENTE)", cond)

    # ===================== controles de la auditoría de interpretación (L21-L28) =====================
    # L21 alcance / distancia nunca etiquetado como reglamentario u óptimo
    prohibidas = ("reglamentari", "admisible", "maximo_legal", "optimo", "normativo")
    cond = not any(any(x in k_ for x in prohibidas) for k_ in aves_vivas(10000, aves_camion=5500))
    if tabla is not None:
        filas_alc = [f for f in tabla.filas if any(x in f["variable"] for x in ("alcance", "t_transporte_disponible"))]
        cond = cond and filas_alc and all("NO es límite" in f["nota"] for f in filas_alc) \
            and not any(any(x in f["variable"] for x in prohibidas) for f in tabla.filas) \
            and all(f["clasificacion"] != "[VERIFICADO]" for f in tabla.filas if "ventana" in f["variable"])
    ok("L21 alcance/radio resultante del escenario, nunca etiquetado como reglamentario u óptimo", cond)

    # L22 cambiar tiempos de captura, espera o retiro de alimento cambia el tiempo disponible de transporte
    base_ = aves_vivas(10000)["t_transporte_disponible_escenario_h"]
    cond = all(aves_vivas(10000, **{k_: v})["t_transporte_disponible_escenario_h"] < base_ - 1e-9
               for k_, v in (("t_captura_carga", 2.5), ("t_espera_planta", 2.0), ("t_espera_granja", 1.0),
                             ("t_retiro_alimento", 4.0), ("t_descarga", 0.5)))
    cond = cond and aves_vivas(10000, t_captura_carga=2.5)["alcance_ruta_escenario_km"] < aves_vivas(10000)["alcance_ruta_escenario_km"]
    ok("L22 tiempos de captura/espera/retiro modifican el tiempo de transporte disponible y el alcance", cond)

    # L23 backhaul de aves deshabilitado por defecto pero NO como prohibición normativa
    est_aves, txt_aves = BACKHAUL_POSIBLE["aves_vivas"]
    cond = BACKHAUL_AVES is False and est_aves == "DESHABILITADO_POR_DEFECTO" and "No es una prohibición" in txt_aves \
        and not lanza(km_retorno, 100, "aves_vivas", True, 0.3) and _cerca(km_retorno(100, "aves_vivas", True, 0.3), 70) \
        and "envases" in TIPO_RETORNO["aves_vivas"] and set(TIPO_RETORNO) == set(BACKHAUL_POSIBLE)
    ok("L23 backhaul de aves deshabilitado por defecto (supuesto), no prohibición; retorno con jaulas ≠ vacío", cond)

    # L24 la utilización de flota responde al tiempo de ciclo
    a_ = aves_vivas(10000, aves_camion=5500, radio_km=50)
    b_ = aves_vivas(10000, aves_camion=5500, radio_km=50, t_lavado=1.5, t_espera_planta=1.5)
    componentes = a_["t_ida_h"] + a_["t_captura_carga_h"] + a_["t_espera_granja_h"] + a_["t_espera_planta_h"] \
        + a_["t_descarga_h"] + a_["t_regreso_h"] + a_["t_lavado_h"]
    cond = _cerca(a_["tiempo_ciclo_h"], componentes) and b_["tiempo_ciclo_h"] > a_["tiempo_ciclo_h"] \
        and _cerca(a_["utilizacion_flota"], a_["viajes_dia"] * a_["tiempo_ciclo_h"] / (a_["flota_minima"] * HORAS_CAMION_DIA)) \
        and _cerca(b_["utilizacion_flota"], b_["viajes_dia"] * b_["tiempo_ciclo_h"] / (b_["flota_minima"] * HORAS_CAMION_DIA)) \
        and b_["camion_horas_dia"] > a_["camion_horas_dia"] \
        and _cerca(a_["utilizacion_semanal_flota"], a_["camion_horas_dia"] * 5 / (a_["flota_minima"] * HORAS_CAMION_DIA * 7))
    ok("L24 utilización de flota = f(tiempo de ciclo = ida + carga + esperas + descarga + regreso + lavado)", cond)

    # L25 todo resultado de viajes/ocupación declara la capacidad usada (o PENDIENTE)
    if tabla is not None:
        malas = [f for f in tabla.filas if f["bloque"] not in ("parametros", "backhaul")
                 and depende_capacidad(f["variable"]) and (f["capacidad_vehiculo"] in ("", "-")
                                                           or f["tipo_capacidad"] not in TIPOS_CAPACIDAD)]
        incoh = [f for f in tabla.filas if f["tipo_capacidad"] == "PENDIENTE" and depende_capacidad(f["variable"])
                 and f["valor"] not in ("PENDIENTE", "NO_APLICA") and "llenar" not in f["variable"]]
        ok("L25 cada resultado de viajes/ocupación indica la capacidad de escenario usada (o PENDIENTE)",
           not malas and not incoh, f"{len(malas)} sin capacidad, {len(incoh)} incoherentes")
    else:
        ok("L25 capacidad declarada", aves_vivas(10000)["viajes_dia"] is None)

    # L26 ocupación por masa y por volumen distintas; sin densidad no hay ocupación volumétrica
    sin = subproductos(10000, 5, "B", "E1", cap=10, corriente="G1-plumas", cap_m3=40)
    con = subproductos(10000, 5, "B", "E1", cap=10, corriente="G1-plumas", cap_m3=40, densidades={"plumas": 0.1})
    cond = sin["ocupacion_volumetrica"] is None and sin["m3_dia_op"] is None and "densidad_aparente_plumas" in sin["faltantes"] \
        and sin["ocupacion_masica"] is not None and sin["viajes_por_retiro_vinculante"] is None \
        and con["ocupacion_volumetrica"] is not None and not _cerca(con["ocupacion_volumetrica"], con["ocupacion_masica"]) \
        and con["viajes_por_retiro_vinculante"] == max(con["viajes_por_retiro_criterio_masa"], con["viajes_por_retiro_criterio_volumen"]) \
        and lanza(lambda: subproductos(10000, corriente="plumas", densidades={"plumas": 0}))
    if tabla is not None:
        cond = cond and all(f["valor"] in ("PENDIENTE", "NO_APLICA") for f in tabla.filas if f["variable"] == "ocupacion_volumetrica"
                            or f["variable"].startswith("m3_"))
    ok("L26 ocupación másica ≠ volumétrica; sin densidad aparente la volumétrica queda PENDIENTE", cond)

    # L27 exportación: cada escenario indica % exportado y payload; utilización ≤ 100 %
    cond = True
    for E in ESCALAS:
        for q in CUOTAS_EXPORT:
            r = exportacion(E, cuota=q)
            cond = cond and _cerca(r["cuota_exportacion"], q) and _cerca(r["carga_contenedor_t"], CONTENEDOR_T) \
                and 0 < r["utilizacion_carga_contenedores"] <= 1 + 1e-12
    if tabla is not None:
        grupos = {}
        for f in tabla.filas:
            if f["bloque"] == "exportacion":
                grupos.setdefault((f["escala_aves_dia"], f["parametros"]), set()).add(f["variable"])
        cond = cond and grupos and all({"cuota_exportacion", "carga_contenedor_t", "utilizacion_carga_contenedores"} <= v
                                       for v in grupos.values()) \
            and all(f["escenario"] == "SENSIBILIDAD" for f in tabla.filas if f["bloque"].startswith("exportacion"))
    ok("L27 exportación como SENSIBILIDAD con % exportado, payload y utilización explícitos", cond)

    # L28 acumulación de subproductos: ninguna dimensión se da por cumplida sin evidencia
    cond = True
    for est in ESTRATEGIAS:
        r = subproductos(10000, estrategia=est, corriente="G3-visceras", cap=10)
        cond = cond and r["sanitariamente_permitido"] is None and r["aceptado_por_receptor"] is None
        if ESTRATEGIAS[est][1] > 1:
            cond = cond and r["fisicamente_posible"] is None and r["requiere_frio"] == 1.0 \
                and r["riesgo_olores_degradacion_aumentado"] == 1.0 and "normativa_acumulacion_subproductos" in r["faltantes"]
    ok("L28 acumulación: físico / sanitario / receptor / frío / olores separados y PENDIENTES sin evidencia", cond)

    fallas = [x for x in res if not x[1]]
    if verbose:
        for nombre, b_, det in res:
            print(f"  [{'OK ' if b_ else 'FALLA'}] {nombre}" + (f" — {det}" if det else ""))
        print(f"  {len(res) - len(fallas)}/{len(res)} pruebas OK")
    return not fallas, res


# ---------------------------------------------------------------------------
# 13. SALIDAS
# ---------------------------------------------------------------------------
def fmt(x, d=1):
    if x is None:
        return "PEND."
    if x is NA:
        return "N/A"
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def resumen():
    print("\nAVES VIVAS (radio 100 km, ruta ×1,3, CAPACIDAD DE ESCENARIO 5.500 aves/camión, DOA 0,3 %, normal | verano −15 %)")
    print("escala | aves cargadas | t vivas | viajes (normal/verano) | ocup. | km/día | km/ave | ciclo h | flota | utiliz.")
    for E in ESCALAS:
        n, v = aves_vivas(E, aves_camion=AVES_CAMION_BASE), aves_vivas(E, aves_camion=AVES_CAMION_BASE, reduccion=0.15)
        print(f"{E:>6} | {fmt(n['aves_cargadas_dia'],0):>8} | {fmt(n['t_vivo_cargado_dia'])} | {n['viajes_dia']}/{v['viajes_dia']} "
              f"| {fmt(n['ocupacion']*100,0)} % | {fmt(n['km_total_dia'],0)} | {fmt(n['km_por_ave'],3)} | "
              f"{fmt(n['tiempo_ciclo_h'])} | {n['flota_minima']} | {fmt(n['utilizacion_flota']*100,0)} %")
    r0 = aves_vivas(10000)
    print(f"\nVENTANA PREFAENA DE ESCENARIO {fmt(VENTANA_PREFAENA_H)} h (no normativa): retiro de alimento {fmt(T_RETIRO_ALIMENTO_H)} + "
          f"captura/carga {fmt(T_CAPTURA_CARGA_H)} + espera granja {fmt(T_ESPERA_GRANJA_H)} + espera planta {fmt(T_ESPERA_PLANTA_H,2)} + "
          f"descarga {fmt(T_DESCARGA_H,2)} → transporte disponible {fmt(r0['t_transporte_disponible_escenario_h'])} h → alcance de "
          f"escenario {fmt(r0['alcance_ruta_escenario_km'],0)} km por ruta ({fmt(r0['alcance_geo_escenario_km'],0)} km geo)")
    print("RADIOS (10.000 aves/día, 5.500 aves/camión): km ruta medio, h transporte máx, total prefaena máx, alerta, km/día")
    for R in RADIOS_KM:
        r = aves_vivas(10000, radio_km=R, aves_camion=AVES_CAMION_BASE)
        print(f"  {R:>3} km → {fmt(r['distancia_ruta_media_km'],0)} km · {fmt(r['t_transporte_max_h'])} h · "
              f"{fmt(r['t_total_prefaena_max_h'])} h · {'ALERTA' if r['alerta_prefaena_excede_ventana_max'] else 'ok'} · "
              f"{fmt(r['km_total_dia'],0)} km/día · ciclo {fmt(r['tiempo_ciclo_h'])} h")
    print("\nGRANJAS (plazas por granja 15/30/60 mil): granjas equivalentes y cosechas por semana")
    for E in ESCALAS:
        print(f"  {E:>6}: " + " | ".join(f"{fmt(aves_vivas(E, plazas_granja=p)['granjas_equivalentes'])} granjas, "
                                         f"{fmt(aves_vivas(E, plazas_granja=p)['cosechas_semana'])} cos/sem" for p in PLAZAS_GRANJA))
    print("\nPRODUCTO (P1/P2/P3, 6 d despacho): t/día de despacho refrigerado · congelado; viajes con cap 6 / 12 / 20 t")
    for E in ESCALAS:
        txt = []
        for perfil in PERFILES:
            r = [producto(E, perfil=perfil, cap_refrigerado=c, cap_congelado=c) for c in (6, 12, 20)]
            txt.append(f"{perfil}: {fmt(r[0]['refrigerado_t_dia_despacho'])}·{fmt(r[0]['congelado_t_dia_despacho'])} t "
                       f"({'/'.join(str(x['refrigerado_viajes_dia_despacho']) for x in r)} R; "
                       f"{'/'.join(str(x['congelado_viajes_dia_despacho']) for x in r)} C)")
        print(f"  {E:>6}: " + " | ".join(txt))
    print("\nRED ANCLA (100 kg/local/día, 3 entregas/sem, 6 d despacho; reparto 6 t, troncal 20 t barrido; 300 km)")
    for esc in ANCLA:
        for modo in ("directo", "cd", "crossdock"):
            r = red_ancla(esc, 100, 3, modo, cap_reparto=6, cap_troncal=20, dist_mercado_km=300)
            print(f"  {esc} {modo:>9}: locales {r['locales']}, t/día {fmt(r['t_dia_despacho'])}, kg/parada {fmt(r['kg_por_parada_tienda'],0)}, "
                  f"troncal {r.get('viajes_troncal_dia')}, rutas {r.get('rutas_reparto_dia')}, km/día {fmt(r['km_dia_despacho'],0)}, "
                  f"km/t {fmt(r['km_por_t'],0)}, excede conducción {r.get('excede_conduccion')}")
    print("\nEXPORTACIÓN (cuota 20 %): t/día op, días de faena y calendario para 1 contenedor, contenedores/mes")
    for E in ESCALAS:
        r = exportacion(E)
        print(f"  {E:>6}: {fmt(r['export_t_dia_op'],2)} t · {fmt(r['dias_faena_llenar_contenedor'])} d faena · "
              f"{fmt(r['dias_calendario_llenar_contenedor'])} d cal · {fmt(r['contenedores_mes'])} cont/mes")
    print("\nSUBPRODUCTOS (config. B): t/día por grupo; % de la capacidad MÁSICA 5/10/20 t (barrido); volumétrica PENDIENTE")
    for E in ESCALAS:
        txt = []
        for g in sorted({v[3] for v in CORRIENTES.values()}):
            rr = [subproductos(E, 5, "B", "E1", cap=c, corriente=g) for c in CAP_SUBPROD_BARRIDO]
            if rr[0]["t_dia_op"] == 0:
                continue
            txt.append(f"{g} {fmt(rr[0]['t_dia_op'],2)} t ({'/'.join(fmt(x['ocupacion_masica']*100,0) for x in rr)} % másica)")
        print(f"  {E:>6}: " + " | ".join(txt))
    print("\nINVENTARIO (10.000 aves/día, comestible, 5 d faena): stock de ciclo máx. según días de despacho")
    com = producto(10000)["comestible_t_dia_op"]
    for dd in DIAS_DESPACHO:
        r = inventario(com, 5, dd, 0, cap=12)
        print(f"  {dd} d despacho: {fmt(r['despacho_t_dia_despacho'])} t/día despacho, stock ciclo máx {fmt(r['stock_ciclo_max_t'])} t, "
              f"medio {fmt(r['stock_ciclo_medio_t'])} t, {fmt(r['t_dias_inmovilizadas_semana'],0)} t·d/sem, viajes/día {r['viajes_dia_despacho']}")


def main():
    ap = argparse.ArgumentParser(description="Modelo logístico físico (12B)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--resumen", action="store_true")
    ap.add_argument("--escenario", action="store_true")
    ap.add_argument("--aves-dia", type=float, default=10000)
    ap.add_argument("--dias-semana", type=int, default=5)
    ap.add_argument("--radio-km", type=float, default=100)
    ap.add_argument("--factor-ruta", type=float, default=FACTOR_RUTA_BASE)
    ap.add_argument("--aves-camion", type=float, default=None, help="capacidad de escenario; sin valor = PENDIENTE")
    ap.add_argument("--ventana-prefaena", type=float, default=VENTANA_PREFAENA_H)
    ap.add_argument("--t-retiro-alimento", type=float, default=T_RETIRO_ALIMENTO_H)
    ap.add_argument("--t-captura-carga", type=float, default=T_CAPTURA_CARGA_H)
    ap.add_argument("--t-espera-granja", type=float, default=T_ESPERA_GRANJA_H)
    ap.add_argument("--t-espera-planta", type=float, default=T_ESPERA_PLANTA_H)
    ap.add_argument("--cap-subproductos-m3", type=float, default=None)
    ap.add_argument("--doa", type=float, default=DOA_BASE)
    ap.add_argument("--reduccion-verano", type=float, default=0.0)
    ap.add_argument("--cap-refrigerado", type=float, default=None)
    ap.add_argument("--cap-congelado", type=float, default=None)
    ap.add_argument("--cap-subproductos", type=float, default=None)
    ap.add_argument("--dias-despacho", type=int, default=6)
    ap.add_argument("--perfil", default="P1")
    ap.add_argument("--config", default="B")
    ap.add_argument("--ancla", default="B")
    ap.add_argument("--kg-local-dia", type=float, default=100)
    ap.add_argument("--entregas-semana", type=int, default=3)
    ap.add_argument("--modo", default="crossdock")
    ap.add_argument("--dist-mercado-km", type=float, default=300)
    ap.add_argument("--cuota-exportacion", type=float, default=0.2)
    ap.add_argument("--dist-puerto-km", type=float, default=300)
    a = ap.parse_args()

    print(f"Modelo logístico físico v{VERSION} ({FECHA}) — pruebas:")
    bien, _ = ejecutar_tests(verbose=True)
    if not bien:
        sys.exit(1)
    if a.escenario:
        E, ds = a.aves_dia, a.dias_semana
        out = {"aves_vivas": aves_vivas(E, ds, doa=a.doa, aves_camion=a.aves_camion, reduccion=a.reduccion_verano,
                                        radio_km=a.radio_km, factor_ruta=a.factor_ruta, ventana_prefaena=a.ventana_prefaena,
                                        t_retiro_alimento=a.t_retiro_alimento, t_captura_carga=a.t_captura_carga,
                                        t_espera_granja=a.t_espera_granja, t_espera_planta=a.t_espera_planta),
               "producto": producto(E, ds, a.config, a.perfil, a.dias_despacho, a.cap_refrigerado, a.cap_congelado,
                                    a.dist_mercado_km),
               "red_ancla": red_ancla(a.ancla, a.kg_local_dia, a.entregas_semana, a.modo, a.dias_despacho,
                                      cap_reparto=a.cap_refrigerado, cap_troncal=a.cap_refrigerado,
                                      dist_mercado_km=a.dist_mercado_km),
               "exportacion": exportacion(E, ds, a.config, a.cuota_exportacion, dist_puerto_km=a.dist_puerto_km)}
        for g in sorted({v[3] for v in CORRIENTES.values()}):
            out[f"subproductos_{g}"] = subproductos(E, ds, a.config, "E1", a.cap_subproductos, corriente=g,
                                                    cap_m3=a.cap_subproductos_m3)
        for nombre, r in out.items():
            print(f"\n[{nombre}]  faltantes: {', '.join(sorted(r.get('faltantes', []))) or '—'}")
            for k_, v in r.items():
                if k_ != "faltantes":
                    print(f"  {k_}: {'PENDIENTE' if v is None else (fmt(v, 3) if isinstance(v, float) or v is NA else v)}")
        return
    if a.solo_tests:
        return
    t = construir()
    bien, _ = ejecutar_tests(verbose=False, tabla=t)
    if not bien:
        ejecutar_tests(verbose=True, tabla=t)
        sys.exit(1)
    ruta = os.path.join(AQUI, "escenarios_logistica.csv")
    escribir_csv(t, ruta)
    pend = sum(1 for f in t.filas if f["valor"] == "PENDIENTE")
    print(f"\nCSV escrito: {ruta} ({len(t.filas)} filas; {pend} PENDIENTE). Pruebas con la tabla: OK")
    if a.resumen:
        resumen()


if __name__ == "__main__":
    main()
