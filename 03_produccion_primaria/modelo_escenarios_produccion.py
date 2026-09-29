"""
Modelo físico de escenarios de producción primaria (pollo parrillero).

Genera `escenarios_produccion.csv`, ejecuta las pruebas automáticas y, con
`--tablas`, imprime las tablas usadas en los .md de esta carpeta.

    python3 modelo_escenarios_produccion.py            # CSV + pruebas
    python3 modelo_escenarios_produccion.py --tablas   # además, tablas

ESTADO: ESCENARIOS de orden de magnitud. NO es un diseño recomendado, NO fija
capacidad de faena (regla 9 de CLAUDE.md) y NO decide cantidad de galpones.
Sin precios (esta fase solo analiza sensibilidad física).

Versión 1.1 (2026-09-29, auditoría): corrige el cálculo semanal de pollitos
(antes = total anual con 250 días de faena / 52, equivalente a solo ~4,8 días
de faena por semana) y dimensiona los galpones con el ritmo de faena de una
SEMANA PLENA. Separa explícitamente pollitos alojados, aves cargadas y aves
faenadas. Agrega pruebas automáticas.

Unidades: aves (cabezas), kg de peso vivo, días, semanas, m² de piso de
galpón, t = 1.000 kg, m³ de agua. Separador decimal: punto (regla de CSV).

------------------------------------------------------------------------------
TRES CATEGORÍAS DE AVES (no mezclar)
------------------------------------------------------------------------------
  POLLITOS BB ALOJADOS  --(mortalidad en granja, m)-->  AVES CARGADAS en granja
  AVES CARGADAS         --(mortalidad en transporte, DOA)-->  AVES FAENADAS
"Planta de N aves/día" = N AVES EFECTIVAMENTE FAENADAS por día de faena.
Aves recibidas vivas en planta = aves faenadas (los decomisos ocurren después
de la faena y no reducen las aves faenadas).

Sentido de cálculo (se parte de la faena objetivo y se "sube" la cadena):
  aves_cargadas = aves_faenadas / (1 − DOA)
  pollitos      = aves_cargadas / (1 − m)
equivalente a: aves_faenadas = pollitos × (1 − m) × (1 − DOA).

------------------------------------------------------------------------------
CALENDARIO
------------------------------------------------------------------------------
SEMANAS_ANIO        = 365 / 7 = 52,14
dias_faena_anio     = 250 (5 d/semana: 5 × 52,14 = 260,7 − ~10,7 días sin faena
                      por feriados) | 300 (6 d/semana: 312,9 − ~12,9)      [SUP-025]
Semana plena        = semana sin feriados, con todos los días de faena.
La capacidad de galpones se dimensiona para la SEMANA PLENA (ritmo nominal de
la planta); en las semanas con feriados se alojan menos pollitos, por lo que la
utilización anual de los galpones es 250 / 260,7 ≈ 0,96 (5 d) o 300/312,9 (6 d).

------------------------------------------------------------------------------
FÓRMULAS
------------------------------------------------------------------------------
Ritmo pleno (por día de faena y por semana plena):
  aves_cargadas_dia            = aves_faenadas_dia / (1 − DOA)
  pollitos_por_dia_faena       = aves_cargadas_dia / (1 − m)
  X_semana_plena               = X_dia × dias_faena_semana
Anual:
  aves_faenadas_anio           = aves_faenadas_dia × dias_faena_anio
  aves_cargadas_anio           = aves_faenadas_anio / (1 − DOA)
  pollitos_alojados_anio       = aves_cargadas_anio / (1 − m)
  mortalidad_granja_aves_anio  = pollitos_alojados_anio − aves_cargadas_anio
  mortalidad_transp_aves_anio  = aves_cargadas_anio − aves_faenadas_anio
  X_semana_promedio            = X_anio / SEMANAS_ANIO
Galpones:
  ciclo_total_dias             = edad_faena + dias_entre_lotes (captura, cama,
                                 lavado, desinfección, vacío sanitario, preparación)
  ciclos_anio                  = 365 / ciclo_total_dias × DISPONIBILIDAD (0,97:
                                 encaje de calendario y esperas; los feriados ya
                                 están en dias_faena_anio)
  capacidad_alojamiento        = pollitos_semana_plena × SEMANAS_ANIO / ciclos_anio
                                 (plazas = pollitos que caben al alojar, suma de
                                 galpones, para sostener el ritmo pleno)
  utilizacion_anual_galpones   = pollitos_alojados_anio / (capacidad × ciclos_anio)
  m2_galpon                    = capacidad × (1 − m) × peso_vivo / kg_m2_max
                                 (densidad limitada al final, en kg vivo/m²)
  galpones_N                   = m2_galpon / N (N = 1.200, 1.800, 2.400 m²)
Aves simultáneas (ley de Little; supervivencia media ≈ 1 − m/2):
  inventario_ritmo_pleno       = pollitos_semana_plena / 7 × edad × (1 − m/2)
  inventario_promedio_anual    = pollitos_alojados_anio / 365 × edad × (1 − m/2)
Alimento (FCR de campo = alimento entregado / kg vivo CARGADO):
  alimento_anio_kg             = aves_cargadas_anio × peso_vivo × FCR
  alimento_semana_plena_kg     = aves_cargadas_semana_plena × peso_vivo × FCR
  alimento_por_ave_faenada     = alimento_anio / aves_faenadas_anio
  alimento_ciclo_crianza_t     = alimento_semana_plena × edad / 7
                                 (alimento de todos los lotes de un ciclo de
                                 crianza a ritmo pleno: cota superior del
                                 alimento inmovilizado en aves en crianza,
                                 medida FÍSICA del capital de trabajo; sin plazos
                                 de cobro/pago)
Agua de bebida (1,8 L/kg de alimento; NO incluye cooling, nebulización, lavado):
  agua_bebida_m3               = alimento_kg × 1,8 / 1.000

Reparto del alimento por fase (inicio 0–10 d / crecimiento 11–24 d /
terminación 25 d–faena): tabla CONSUMO_ACUMULADO_REF (orden de magnitud).

------------------------------------------------------------------------------
PARÁMETROS Y SU ORIGEN (ver 03_produccion_primaria/ciclo_productivo.md)
------------------------------------------------------------------------------
Perfiles de mercado (peso/edad) — [ESTIMACIÓN] a partir de manuales Cobb/Ross
(FTE-140, FTE-142, FTE-143 [PVDP]) y referencias de campo argentinas
(FTE-050, FTE-154 [PVDP]):
  liviano : 38 d, 2,4 kg vivo
  medio   : 47 d, 2,9 kg vivo
  pesado  : 54 d, 3,4 kg vivo
Niveles de desempeño — [SUPUESTO SUP-026]:
  favorable     : FCR base − 0,10; mort. granja 3 %; DOA 0,2 %; 12 d entre lotes; 39 kg/m²
  medio         : FCR base;        mort. granja 5 %; DOA 0,3 %; 15 d entre lotes; 35 kg/m²
  desfavorable  : FCR base + 0,15; mort. granja 8 %; DOA 0,5 %; 20 d entre lotes; 30 kg/m²
FCR base de campo por perfil — [ESTIMACIÓN]: 1,58 / 1,70 / 1,82
"""

import csv
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

SEMANAS_ANIO = 365 / 7
PLANTAS_AVES_FAENADAS_DIA = [2500, 5000, 10000, 20000]
DIAS_FAENA_ANIO = {5: 250, 6: 300}
DISPONIBILIDAD = 0.97
TAMANOS_GALPON_M2 = [1200, 1800, 2400]
RELACION_AGUA_ALIMENTO = 1.8

PERFILES = {
    "liviano": {"edad": 38, "peso": 2.4, "fcr_base": 1.58},
    "medio": {"edad": 47, "peso": 2.9, "fcr_base": 1.70},
    "pesado": {"edad": 54, "peso": 3.4, "fcr_base": 1.82},
}

DESEMPENO = {
    "favorable": {"d_fcr": -0.10, "mort": 0.03, "doa": 0.002, "vacio": 12, "kg_m2": 39},
    "medio": {"d_fcr": 0.00, "mort": 0.05, "doa": 0.003, "vacio": 15, "kg_m2": 35},
    "desfavorable": {"d_fcr": 0.15, "mort": 0.08, "doa": 0.005, "vacio": 20, "kg_m2": 30},
}

# Consumo acumulado de alimento por ave (kg) según edad (días): curva de
# referencia de ORDEN DE MAGNITUD con la forma de las tablas de los manuales
# genéticos (FTE-140, FTE-142 [PVDP]); se usa SOLO para repartir el alimento
# entre fases, no para calcular el total (que sale de peso × FCR).
CONSUMO_ACUMULADO_REF = {10: 0.28, 24: 1.70, 38: 3.95, 47: 5.35, 54: 6.55}


def consumo_acumulado(edad):
    """Interpolación lineal en CONSUMO_ACUMULADO_REF (extrapola con el último tramo)."""
    xs = sorted(CONSUMO_ACUMULADO_REF)
    if edad in CONSUMO_ACUMULADO_REF:
        return CONSUMO_ACUMULADO_REF[edad]
    i = max(1, min(len(xs) - 1, sum(1 for x in xs if x < edad)))
    x0, x1 = xs[i - 1], xs[i]
    y0, y1 = CONSUMO_ACUMULADO_REF[x0], CONSUMO_ACUMULADO_REF[x1]
    return y0 + (y1 - y0) * (edad - x0) / (x1 - x0)


def reparto_fases(edad):
    total = consumo_acumulado(edad)
    inicio = CONSUMO_ACUMULADO_REF[10] / total
    crecimiento = (CONSUMO_ACUMULADO_REF[24] - CONSUMO_ACUMULADO_REF[10]) / total
    return inicio, crecimiento, 1 - inicio - crecimiento


def calcular(aves_faenadas_dia, dias_semana, edad, peso, fcr, mort, doa, vacio, kg_m2):
    """Devuelve todas las variables físicas (sin redondear)."""
    dias_anio = DIAS_FAENA_ANIO[dias_semana]
    # --- ritmo pleno (día de faena y semana plena)
    cargadas_dia = aves_faenadas_dia / (1 - doa)
    pollitos_dia = cargadas_dia / (1 - mort)
    faenadas_sem = aves_faenadas_dia * dias_semana
    cargadas_sem = cargadas_dia * dias_semana
    pollitos_sem = pollitos_dia * dias_semana
    # --- anual
    faenadas_anio = aves_faenadas_dia * dias_anio
    cargadas_anio = faenadas_anio / (1 - doa)
    pollitos_anio = cargadas_anio / (1 - mort)
    # --- galpones
    ciclo_total = edad + vacio
    ciclos = 365 / ciclo_total * DISPONIBILIDAD
    capacidad = pollitos_sem * SEMANAS_ANIO / ciclos
    m2 = capacidad * (1 - mort) * peso / kg_m2
    # --- alimento y agua
    alimento_anio_kg = cargadas_anio * peso * fcr
    alimento_sem_kg = cargadas_sem * peso * fcr
    ini, cre, ter = reparto_fases(edad)
    return {
        "dias_faena_anio": dias_anio,
        # tres categorías de aves: ritmo pleno
        "aves_faenadas_semana_plena": faenadas_sem,
        "aves_cargadas_dia": cargadas_dia,
        "aves_cargadas_semana_plena": cargadas_sem,
        "pollitos_alojados_por_dia_faena": pollitos_dia,
        "pollitos_alojados_semana_plena": pollitos_sem,
        # tres categorías de aves: anual
        "aves_faenadas_anio": faenadas_anio,
        "aves_cargadas_anio": cargadas_anio,
        "pollitos_alojados_anio": pollitos_anio,
        "pollitos_alojados_semana_promedio": pollitos_anio / SEMANAS_ANIO,
        "mortalidad_granja_aves_anio": pollitos_anio - cargadas_anio,
        "mortalidad_transporte_aves_anio": cargadas_anio - faenadas_anio,
        # galpones
        "ciclo_total_dias": ciclo_total,
        "ciclos_anio": ciclos,
        "capacidad_alojamiento_pollitos": capacidad,
        "utilizacion_anual_galpones": pollitos_anio / (capacidad * ciclos),
        "inventario_aves_ritmo_pleno": pollitos_sem / 7 * edad * (1 - mort / 2),
        "inventario_aves_promedio_anual": pollitos_anio / 365 * edad * (1 - mort / 2),
        "m2_galpon": m2,
        "pollitos_m2_alojamiento": capacidad / m2,
        **{f"galpones_{t}m2": m2 / t for t in TAMANOS_GALPON_M2},
        # producción y alimento
        "kg_vivo_cargado_anio": cargadas_anio * peso,
        "alimento_por_ave_faenada_kg": alimento_anio_kg / faenadas_anio,
        "alimento_por_pollito_alojado_kg": alimento_anio_kg / pollitos_anio,
        "alimento_t_anio": alimento_anio_kg / 1000,
        "alimento_t_mes_promedio": alimento_anio_kg / 1000 / 12,
        "alimento_t_semana_promedio": alimento_anio_kg / 1000 / SEMANAS_ANIO,
        "alimento_t_semana_plena": alimento_sem_kg / 1000,
        "alimento_inicio_t_anio": alimento_anio_kg / 1000 * ini,
        "alimento_crecimiento_t_anio": alimento_anio_kg / 1000 * cre,
        "alimento_terminacion_t_anio": alimento_anio_kg / 1000 * ter,
        "alimento_ciclo_crianza_t": alimento_sem_kg / 1000 * edad / 7,
        # agua
        "agua_bebida_m3_anio": alimento_anio_kg * RELACION_AGUA_ALIMENTO / 1000,
        "agua_bebida_m3_dia_promedio": alimento_anio_kg * RELACION_AGUA_ALIMENTO / 1000 / 365,
        "agua_bebida_m3_semana_plena": alimento_sem_kg * RELACION_AGUA_ALIMENTO / 1000,
    }


def escenarios():
    """Genera (id, parámetros, resultados) sin redondear."""
    n = 0
    for aves in PLANTAS_AVES_FAENADAS_DIA:
        for dias_sem in DIAS_FAENA_ANIO:
            for perfil, p in PERFILES.items():
                for nivel, d in DESEMPENO.items():
                    n += 1
                    par = dict(aves_faenadas_dia=aves, dias_semana=dias_sem, edad=p["edad"],
                               peso=p["peso"], fcr=round(p["fcr_base"] + d["d_fcr"], 2),
                               mort=d["mort"], doa=d["doa"], vacio=d["vacio"], kg_m2=d["kg_m2"])
                    yield f"ESC-{n:03d}", perfil, nivel, par, calcular(**par)


DOS_DEC = ("ciclos_anio", "pollitos_m2_alojamiento", "alimento_por_ave_faenada_kg",
           "alimento_por_pollito_alojado_kg", "utilizacion_anual_galpones")


def generar_csv():
    filas = []
    for id_, perfil, nivel, par, r in escenarios():
        fila = {
            "id": id_,
            "clasificacion": "ESCENARIO (no diseño recomendado)",
            "aves_faenadas_dia": par["aves_faenadas_dia"],
            "dias_faena_semana": par["dias_semana"],
            "perfil_mercado": perfil,
            "nivel_desempeno": nivel,
            "edad_faena_d": par["edad"],
            "peso_vivo_kg": par["peso"],
            "fcr_campo": par["fcr"],
            "mort_granja_pct": round(par["mort"] * 100, 2),
            "mort_transporte_pct": round(par["doa"] * 100, 2),
            "dias_entre_lotes": par["vacio"],
            "densidad_max_kg_m2": par["kg_m2"],
        }
        for k, v in r.items():
            if isinstance(v, float):
                v = round(v, 2) if (k in DOS_DEC or k.startswith("galpones")) else round(v)
            fila[k] = v
        fila["observaciones"] = (
            "aves_faenadas = aves vivas que llegan y se faenan; cargadas = salen de granja; "
            "pollitos = alojados. Galpones = m² / tamaño, sin redondear ni reserva. "
            "Agua solo de bebida."
        )
        filas.append(fila)
    with open(AQUI / "escenarios_produccion.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), lineterminator="\n")
        w.writeheader()
        w.writerows(filas)
    return filas


# ------------------------------------------------------------------------------
# PRUEBAS AUTOMÁTICAS
# ------------------------------------------------------------------------------

LINEALES = ("aves_faenadas_semana_plena", "aves_cargadas_dia", "aves_cargadas_semana_plena",
            "pollitos_alojados_semana_plena", "aves_faenadas_anio", "aves_cargadas_anio",
            "pollitos_alojados_anio", "pollitos_alojados_semana_promedio",
            "mortalidad_granja_aves_anio", "mortalidad_transporte_aves_anio",
            "capacidad_alojamiento_pollitos", "inventario_aves_ritmo_pleno",
            "inventario_aves_promedio_anual", "m2_galpon", "galpones_1800m2",
            "kg_vivo_cargado_anio", "alimento_t_anio", "alimento_t_semana_plena",
            "alimento_ciclo_crianza_t", "agua_bebida_m3_anio")
INTENSIVAS = ("ciclos_anio", "utilizacion_anual_galpones", "pollitos_m2_alojamiento",
              "alimento_por_ave_faenada_kg", "alimento_por_pollito_alojado_kg")


def _cerca(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def ejecutar_pruebas():
    res = {}

    def prueba(nombre, cond):
        res.setdefault(nombre, [0, 0])
        res[nombre][0 if cond else 1] += 1

    todos = list(escenarios())
    for _, _, _, p, r in todos:
        fd, m, doa = p["aves_faenadas_dia"], p["mort"], p["doa"]
        # A. pollitos alojados > aves faenadas (m > 0)
        prueba("A pollitos > faenadas", r["pollitos_alojados_semana_plena"] > r["aves_faenadas_semana_plena"]
               and r["pollitos_alojados_anio"] > r["aves_faenadas_anio"])
        # B. aves cargadas > aves faenadas (DOA > 0)
        prueba("B cargadas > faenadas", r["aves_cargadas_anio"] > r["aves_faenadas_anio"]
               and r["aves_cargadas_semana_plena"] > r["aves_faenadas_semana_plena"])
        # C. pollitos alojados > aves cargadas (m > 0)
        prueba("C pollitos > cargadas", r["pollitos_alojados_anio"] > r["aves_cargadas_anio"]
               and r["pollitos_alojados_semana_plena"] > r["aves_cargadas_semana_plena"])
        # C'. control del usuario: pollitos semana plena > faenadas semana / (1 − m)
        prueba("C' pollitos > faenadas/(1-m)",
               r["pollitos_alojados_semana_plena"] > r["aves_faenadas_semana_plena"] / (1 - m))
        # D. más mortalidad (granja o transporte) nunca reduce pollitos
        for dm, dd in ((0.01, 0), (0.05, 0), (0, 0.005)):
            q = dict(p, mort=m + dm, doa=doa + dd)
            rq = calcular(**q)
            prueba("D mortalidad monótona",
                   rq["pollitos_alojados_anio"] >= r["pollitos_alojados_anio"]
                   and rq["pollitos_alojados_semana_plena"] >= r["pollitos_alojados_semana_plena"]
                   and rq["capacidad_alojamiento_pollitos"] >= r["capacidad_alojamiento_pollitos"])
        # E. peor FCR nunca reduce alimento
        rq = calcular(**dict(p, fcr=p["fcr"] + 0.1))
        prueba("E FCR monótono", rq["alimento_t_anio"] > r["alimento_t_anio"]
               and rq["alimento_t_semana_plena"] > r["alimento_t_semana_plena"])
        # F. duplicar la faena duplica lo lineal y deja igual lo intensivo
        r2 = calcular(**dict(p, aves_faenadas_dia=2 * fd))
        prueba("F linealidad ×2", all(_cerca(r2[k], 2 * r[k]) for k in LINEALES)
               and all(_cerca(r2[k], r[k]) for k in INTENSIVAS))
        # G. consistencia de unidades y de balances
        g = [
            _cerca(r["aves_faenadas_anio"], r["pollitos_alojados_anio"] * (1 - m) * (1 - doa)),
            _cerca(r["aves_faenadas_semana_plena"], fd * p["dias_semana"]),
            _cerca(r["pollitos_alojados_anio"], r["aves_cargadas_anio"] + r["mortalidad_granja_aves_anio"]),
            _cerca(r["aves_cargadas_anio"], r["aves_faenadas_anio"] + r["mortalidad_transporte_aves_anio"]),
            _cerca(r["pollitos_alojados_semana_promedio"] * SEMANAS_ANIO, r["pollitos_alojados_anio"]),
            _cerca(r["capacidad_alojamiento_pollitos"] * r["ciclos_anio"] * r["utilizacion_anual_galpones"],
                   r["pollitos_alojados_anio"]),
            0 < r["utilizacion_anual_galpones"] <= 1,
            r["inventario_aves_promedio_anual"] <= r["inventario_aves_ritmo_pleno"] <= r["capacidad_alojamiento_pollitos"],
            _cerca(r["m2_galpon"] * p["kg_m2"], r["capacidad_alojamiento_pollitos"] * (1 - m) * p["peso"]),
            _cerca(r["alimento_t_anio"] * 1000, r["kg_vivo_cargado_anio"] * p["fcr"]),
            _cerca(r["agua_bebida_m3_anio"], r["alimento_t_anio"] * RELACION_AGUA_ALIMENTO),
            _cerca(r["alimento_inicio_t_anio"] + r["alimento_crecimiento_t_anio"]
                   + r["alimento_terminacion_t_anio"], r["alimento_t_anio"]),
            _cerca(r["alimento_t_mes_promedio"] * 12, r["alimento_t_anio"]),
            _cerca(r["alimento_por_ave_faenada_kg"], p["peso"] * p["fcr"] / (1 - doa)),
            r["alimento_t_semana_promedio"] < r["alimento_t_semana_plena"],
        ]
        prueba("G unidades y balances", all(g))
    # Casos límite
    base = dict(aves_faenadas_dia=10000, dias_semana=5, edad=47, peso=2.9, fcr=1.7,
                mort=0.0, doa=0.0, vacio=15, kg_m2=35)
    r0 = calcular(**base)
    prueba("Límite sin mortalidad: pollitos = faenadas",
           _cerca(r0["pollitos_alojados_anio"], r0["aves_faenadas_anio"]))
    # Reparto por fases suma 1 para cualquier edad del rango de sensibilidad
    for e in range(35, 57):
        prueba("Fases suman el total (35–56 d)", _cerca(sum(reparto_fases(e)), 1.0)
               and all(x > 0 for x in reparto_fases(e)))
    return res


def imprimir_pruebas(res):
    ok = True
    for nombre, (bien, mal) in res.items():
        estado = "OK" if mal == 0 else "FALLA"
        ok &= mal == 0
        print(f"  [{estado}] {nombre}: {bien} casos correctos, {mal} fallas")
    return ok


# ------------------------------------------------------------------------------
# TABLAS PARA LOS DOCUMENTOS
# ------------------------------------------------------------------------------

def md(fila):
    return "| " + " | ".join(str(x) for x in fila) + " |"


def fmt(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(a, b):
    v = (a / b - 1) * 100
    return "0 %" if abs(v) < 0.05 else f"{v:+.1f} %".replace(".", ",")


def imprimir_tablas():
    print("\n## Prueba manual: 10.000 aves faenadas/día, 5 d/sem, perfil medio, desempeño medio")
    r = calcular(10000, 5, 47, 2.9, 1.70, 0.05, 0.003, 15, 35)
    for k, v in r.items():
        print(f"  {k} = {v:,.3f}")

    print("\n## Tabla por planta (perfil medio, 5 d/sem): favorable / medio / desfavorable")
    for dias in (5, 6):
        for a in PLANTAS_AVES_FAENADAS_DIA:
            rr = [calcular(a, dias, 47, 2.9, round(1.70 + d["d_fcr"], 2), d["mort"], d["doa"],
                           d["vacio"], d["kg_m2"]) for d in DESEMPENO.values()]
            j = lambda k, dec=0: " / ".join(fmt(x[k], dec) for x in rr)
            print(md([fmt(a), dias, fmt(rr[0]["aves_faenadas_semana_plena"]), j("aves_cargadas_semana_plena"),
                      j("pollitos_alojados_semana_plena"), j("pollitos_alojados_semana_promedio"),
                      j("aves_faenadas_anio"), j("pollitos_alojados_anio"),
                      j("capacidad_alojamiento_pollitos"), j("inventario_aves_ritmo_pleno"),
                      j("inventario_aves_promedio_anual"), j("m2_galpon"),
                      j("galpones_1200m2", 1), j("galpones_1800m2", 1), j("galpones_2400m2", 1),
                      j("alimento_por_ave_faenada_kg", 2), j("alimento_t_semana_plena"),
                      j("alimento_t_semana_promedio"), j("alimento_t_mes_promedio"), j("alimento_t_anio"),
                      j("alimento_ciclo_crianza_t"), j("agua_bebida_m3_dia_promedio"),
                      j("agua_bebida_m3_anio")]))

    print("\n## Rango completo por planta")
    todos = list(escenarios())
    for a in PLANTAS_AVES_FAENADAS_DIA:
        rr = [r for _, _, _, p, r in todos if p["aves_faenadas_dia"] == a]
        mm = lambda k, dec=0: fmt(min(x[k] for x in rr), dec) + "–" + fmt(max(x[k] for x in rr), dec)
        print(md([fmt(a), mm("aves_faenadas_anio"), mm("pollitos_alojados_semana_plena"),
                  mm("capacidad_alojamiento_pollitos"), mm("m2_galpon"), mm("galpones_1800m2", 1),
                  mm("alimento_t_anio"), mm("agua_bebida_m3_dia_promedio")]))

    print("\n## Perfiles (10.000 faenadas/día, 5 d, desempeño medio)")
    for perfil, p in PERFILES.items():
        r = calcular(10000, 5, p["edad"], p["peso"], p["fcr_base"], 0.05, 0.003, 15, 35)
        print(perfil, fmt(r["alimento_por_ave_faenada_kg"], 2), fmt(r["alimento_t_anio"]),
              fmt(r["m2_galpon"]), fmt(r["capacidad_alojamiento_pollitos"]), fmt(r["ciclos_anio"], 2))

    print("\n## Sensibilidad (base: 10.000 aves faenadas/día, 5 d/sem, perfil y desempeño medios)")
    base = dict(aves_faenadas_dia=10000, dias_semana=5, edad=47, peso=2.9, fcr=1.70,
                mort=0.05, doa=0.003, vacio=15, kg_m2=35)
    rb = calcular(**base)
    variaciones = [
        ("Base", {}),
        ("FCR 1,60", {"fcr": 1.60}), ("FCR 1,80", {"fcr": 1.80}), ("FCR 1,90", {"fcr": 1.90}),
        ("Mortalidad 3 %", {"mort": 0.03}), ("Mortalidad 8 %", {"mort": 0.08}),
        ("Mortalidad 12 %", {"mort": 0.12}),
        ("Peso 2,6 kg (misma edad y FCR)", {"peso": 2.6}), ("Peso 3,2 kg (misma edad y FCR)", {"peso": 3.2}),
        ("Edad 42 d", {"edad": 42}), ("Edad 54 d", {"edad": 54}),
        ("Densidad 30 kg/m²", {"kg_m2": 30}), ("Densidad 39 kg/m²", {"kg_m2": 39}),
        ("10 días entre lotes", {"vacio": 10}), ("21 días entre lotes", {"vacio": 21}),
        ("6 días de faena/semana", {"dias_semana": 6}),
    ]
    for nombre, cambio in variaciones:
        r = calcular(**dict(base, **cambio))
        print(md([nombre, fmt(r["alimento_t_anio"]), pct(r["alimento_t_anio"], rb["alimento_t_anio"]),
                  fmt(r["pollitos_alojados_semana_plena"]),
                  pct(r["pollitos_alojados_semana_plena"], rb["pollitos_alojados_semana_plena"]),
                  fmt(r["capacidad_alojamiento_pollitos"]), fmt(r["m2_galpon"]),
                  pct(r["m2_galpon"], rb["m2_galpon"]), fmt(r["galpones_1800m2"], 1),
                  fmt(r["ciclos_anio"], 2)]))


if __name__ == "__main__":
    filas = generar_csv()
    print(f"CSV: {len(filas)} escenarios escritos en escenarios_produccion.csv")
    print("Pruebas automáticas:")
    if not imprimir_pruebas(ejecutar_pruebas()):
        sys.exit("ERROR: hay pruebas que fallan; no usar los resultados")
    if "--tablas" in sys.argv:
        imprimir_tablas()
