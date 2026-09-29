"""
Modelo físico de escenarios de producción primaria (pollo parrillero).

Genera `escenarios_produccion.csv` y, con `--tablas`, imprime las tablas de
sensibilidad usadas en los .md de esta carpeta.

ESTADO: ESCENARIOS de orden de magnitud. NO es un diseño recomendado, NO fija
capacidad de faena (regla 9 de CLAUDE.md) y NO decide cantidad de galpones.
Sin precios (esta fase solo analiza sensibilidad física).

Unidades: aves (cabezas), kg de peso vivo, días, m² de piso de galpón,
t = 1.000 kg, m³ de agua. Separador decimal: punto (regla de CSV).

------------------------------------------------------------------------------
FÓRMULAS (una ave "a faena" = ave viva que llega y se cuelga en la planta)
------------------------------------------------------------------------------
dias_faena_anio      = 250 (5 d/semana) | 300 (6 d/semana)            [SUPUESTO SUP-025]
aves_faena_anio      = aves_dia × dias_faena_anio
aves_cargadas_anio   = aves_faena_anio / (1 − mort_transporte)        (DOA)
pollitos_alojados    = aves_cargadas_anio / (1 − mort_granja)
ciclo_total_dias     = edad_faena + dias_vacio                         (vacío = captura
                       + retiro de cama + lavado + desinfección + vacío sanitario
                       + preparación / precalentamiento)
ciclos_anio          = 365 / ciclo_total_dias × disponibilidad        (disponibilidad 0,97:
                       pérdidas por encaje de calendario, feriados, esperas de faena)
capacidad_alojamiento= pollitos_alojados / ciclos_anio                 (plazas = pollitos
                       que caben al alojar, sumando todos los galpones)
inventario_promedio  = pollitos_alojados × edad_faena / 365 × (1 − mort_granja / 2)
                       (ley de Little: aves vivas presentes en promedio)
m2_galpon            = capacidad_alojamiento × (1 − mort_granja) × peso_vivo / kg_m2_max
                       (la densidad se limita al final de la crianza, en kg vivo/m²)
aves_m2_alojamiento  = capacidad_alojamiento / m2_galpon
galpones_N           = m2_galpon / N  (N = 1.200, 1.800 y 2.400 m² por galpón)
alimento_anio_kg     = aves_cargadas_anio × peso_vivo × FCR_campo
                       (FCR de campo = alimento total entregado al lote / kg vivo
                       cargado; incluye el alimento comido por las aves muertas)
alimento_por_ave_faenada = alimento_anio / aves_faena_anio
agua_bebida_m3_anio  = alimento_anio_kg × relacion_agua_alimento / 1.000
                       (1,8 L/kg a ~21 °C; en calor puede duplicarse; NO incluye
                       agua de paneles evaporativos, nebulización ni lavado)

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
  favorable     : FCR base − 0,10; mort. granja 3 %; DOA 0,2 %; vacío 12 d; 39 kg/m²
  medio         : FCR base;        mort. granja 5 %; DOA 0,3 %; vacío 15 d; 35 kg/m²
  desfavorable  : FCR base + 0,15; mort. granja 8 %; DOA 0,5 %; vacío 20 d; 30 kg/m²
FCR base de campo por perfil — [ESTIMACIÓN]: 1,58 / 1,70 / 1,82
"""

import csv
import math
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent

PLANTAS_AVES_DIA = [2500, 5000, 10000, 20000]
DIAS_FAENA = {5: 250, 6: 300}
DISPONIBILIDAD = 0.97
TAMANOS_GALPON_M2 = [1200, 1800, 2400]
RELACION_AGUA_ALIMENTO = 1.8
PESO_POLLITO_KG = 0.042

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


def reparto_fases(edad):
    total = CONSUMO_ACUMULADO_REF[edad]
    inicio = CONSUMO_ACUMULADO_REF[10] / total
    crecimiento = (CONSUMO_ACUMULADO_REF[24] - CONSUMO_ACUMULADO_REF[10]) / total
    return inicio, crecimiento, 1 - inicio - crecimiento


def calcular(aves_dia, dias_semana, edad, peso, fcr, mort, doa, vacio, kg_m2):
    dias_anio = DIAS_FAENA[dias_semana]
    faena_anio = aves_dia * dias_anio
    cargadas_anio = faena_anio / (1 - doa)
    pollitos_anio = cargadas_anio / (1 - mort)
    ciclo_total = edad + vacio
    ciclos = 365 / ciclo_total * DISPONIBILIDAD
    capacidad = pollitos_anio / ciclos
    inventario = pollitos_anio * edad / 365 * (1 - mort / 2)
    m2 = capacidad * (1 - mort) * peso / kg_m2
    alimento_kg = cargadas_anio * peso * fcr
    return {
        "dias_faena_anio": dias_anio,
        "aves_faena_anio": faena_anio,
        "aves_cargadas_anio": cargadas_anio,
        "pollitos_alojados_anio": pollitos_anio,
        "pollitos_alojados_semana": pollitos_anio / 52,
        "ciclo_total_dias": ciclo_total,
        "ciclos_anio": ciclos,
        "capacidad_alojamiento_aves": capacidad,
        "inventario_promedio_aves": inventario,
        "m2_galpon": m2,
        "aves_m2_alojamiento": capacidad / m2,
        "kg_vivo_anio": cargadas_anio * peso,
        "alimento_por_ave_faenada_kg": alimento_kg / faena_anio,
        "alimento_por_pollito_alojado_kg": alimento_kg / pollitos_anio,
        "alimento_t_anio": alimento_kg / 1000,
        "alimento_t_mes": alimento_kg / 1000 / 12,
        "alimento_t_semana": alimento_kg / 1000 / 52,
        "agua_bebida_m3_anio": alimento_kg * RELACION_AGUA_ALIMENTO / 1000,
        "agua_bebida_m3_dia_prom": alimento_kg * RELACION_AGUA_ALIMENTO / 1000 / 365,
    }


def generar_csv():
    filas = []
    n = 0
    for aves_dia in PLANTAS_AVES_DIA:
        for dias_sem in DIAS_FAENA:
            for perfil, p in PERFILES.items():
                for nivel, d in DESEMPENO.items():
                    n += 1
                    fcr = round(p["fcr_base"] + d["d_fcr"], 2)
                    r = calcular(aves_dia, dias_sem, p["edad"], p["peso"], fcr,
                                 d["mort"], d["doa"], d["vacio"], d["kg_m2"])
                    ini, cre, ter = reparto_fases(p["edad"])
                    fila = {
                        "id": f"ESC-{n:03d}",
                        "clasificacion": "ESCENARIO (no diseño recomendado)",
                        "aves_faena_dia": aves_dia,
                        "dias_faena_semana": dias_sem,
                        "perfil_mercado": perfil,
                        "nivel_desempeno": nivel,
                        "edad_faena_d": p["edad"],
                        "peso_vivo_kg": p["peso"],
                        "fcr_campo": fcr,
                        "mort_granja_pct": d["mort"] * 100,
                        "mort_transporte_pct": d["doa"] * 100,
                        "vacio_dias": d["vacio"],
                        "densidad_max_kg_m2": d["kg_m2"],
                    }
                    for k, v in r.items():
                        fila[k] = v
                    for tam in TAMANOS_GALPON_M2:
                        fila[f"galpones_{tam}m2"] = r["m2_galpon"] / tam
                    fila["alimento_inicio_t_anio"] = r["alimento_t_anio"] * ini
                    fila["alimento_crecimiento_t_anio"] = r["alimento_t_anio"] * cre
                    fila["alimento_terminacion_t_anio"] = r["alimento_t_anio"] * ter
                    fila["observaciones"] = (
                        "Galpones = m² / tamaño (sin redondear; no incluye reserva "
                        "ni galpones fuera de servicio). Agua solo de bebida."
                    )
                    filas.append(fila)
    # redondeo legible
    for f in filas:
        for k, v in f.items():
            if isinstance(v, float):
                if k.startswith("galpones") or k in ("ciclos_anio", "aves_m2_alojamiento",
                                                      "alimento_por_ave_faenada_kg",
                                                      "alimento_por_pollito_alojado_kg",
                                                      "fcr_campo", "mort_granja_pct",
                                                      "mort_transporte_pct", "peso_vivo_kg"):
                    f[k] = round(v, 2)
                else:
                    f[k] = round(v)
    with open(AQUI / "escenarios_produccion.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
        w.writeheader()
        w.writerows(filas)
    return filas


def verificar_balances(filas):
    """Controles de cierre de balances físicos."""
    for f in filas:
        # 1) pollitos ≥ cargadas ≥ faenadas
        assert f["pollitos_alojados_anio"] >= f["aves_cargadas_anio"] >= f["aves_faena_anio"]
        # 2) capacidad × ciclos = pollitos/año
        assert abs(f["capacidad_alojamiento_aves"] * f["ciclos_anio"]
                   - f["pollitos_alojados_anio"]) / f["pollitos_alojados_anio"] < 0.01
        # 3) densidad final en kg/m² = máxima declarada
        dens = (f["capacidad_alojamiento_aves"] * (1 - f["mort_granja_pct"] / 100)
                * f["peso_vivo_kg"] / f["m2_galpon"])
        assert abs(dens - f["densidad_max_kg_m2"]) < 0.5
        # 4) alimento = kg vivo × FCR
        assert abs(f["kg_vivo_anio"] * f["fcr_campo"] / 1000 - f["alimento_t_anio"]) < 2
        # 5) fases suman el total
        s = (f["alimento_inicio_t_anio"] + f["alimento_crecimiento_t_anio"]
             + f["alimento_terminacion_t_anio"])
        assert abs(s - f["alimento_t_anio"]) <= 3
    return True


def md(fila):
    return "| " + " | ".join(str(x) for x in fila) + " |"


def fmt(x, dec=0):
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def imprimir_tablas():
    print("\n## FCR × peso: alimento por ave faenada y por millón de aves")
    for peso in (2.4, 2.9, 3.4):
        for fcr in (1.5, 1.6, 1.7, 1.8, 1.9):
            print(md([fmt(peso, 1), fmt(fcr, 1), fmt(peso * fcr, 2), fmt(peso * fcr * 1000)]))
    print("\n## Pollitos a alojar según mortalidad de granja")
    for n in (1000, 5000, 10000, 20000, 100000, 1000000):
        print(md([fmt(n)] + [fmt(math.ceil(n / (1 - m))) for m in (0.02, 0.03, 0.05, 0.08, 0.10, 0.15)]))
    print("\n## m² por cada 10.000 aves a faena por ciclo según densidad y peso")
    for kg in (25, 30, 33, 35, 39, 42):
        print(md([kg] + [fmt(10000 * p / kg) + f" ({fmt(kg / p, 1)} av/m²)" for p in (2.4, 2.9, 3.4)]))
    print("\n## ciclos/año según edad y vacío (×0,97)")
    for e in (35, 38, 42, 47, 50, 54, 56):
        print(md([e] + [fmt(365 / (e + v) * DISPONIBILIDAD, 2) for v in (10, 12, 15, 18, 21)] + [fmt(365 / e, 2)]))
    print("\n## Sensibilidad (base: 10.000 aves/día, 5 d/sem, perfil medio, desempeño medio)")
    base = dict(aves_dia=10000, dias_semana=5, edad=47, peso=2.9, fcr=1.70,
                mort=0.05, doa=0.003, vacio=15, kg_m2=35)
    rb = calcular(**base)
    variaciones = [
        ("Base", {}),
        ("FCR 1,60", {"fcr": 1.60}), ("FCR 1,80", {"fcr": 1.80}), ("FCR 1,90", {"fcr": 1.90}),
        ("Mortalidad 3 %", {"mort": 0.03}), ("Mortalidad 8 %", {"mort": 0.08}),
        ("Mortalidad 12 %", {"mort": 0.12}),
        ("Peso 2,6 kg (misma edad)", {"peso": 2.6}), ("Peso 3,2 kg (misma edad)", {"peso": 3.2}),
        ("Edad 42 d", {"edad": 42}), ("Edad 54 d", {"edad": 54}),
        ("Densidad 30 kg/m²", {"kg_m2": 30}), ("Densidad 39 kg/m²", {"kg_m2": 39}),
        ("Vacío 10 d", {"vacio": 10}), ("Vacío 21 d", {"vacio": 21}),
        ("6 días de faena/semana", {"dias_semana": 6}),
    ]
    for nombre, cambio in variaciones:
        p = dict(base)
        p.update(cambio)
        r = calcular(**p)
        print(md([
            nombre,
            fmt(r["alimento_t_anio"]), f"{(r['alimento_t_anio'] / rb['alimento_t_anio'] - 1) * 100:+.1f} %".replace(".", ","),
            fmt(r["pollitos_alojados_anio"] / 1e6, 2), f"{(r['pollitos_alojados_anio'] / rb['pollitos_alojados_anio'] - 1) * 100:+.1f} %".replace(".", ","),
            fmt(r["capacidad_alojamiento_aves"]),
            fmt(r["m2_galpon"]), f"{(r['m2_galpon'] / rb['m2_galpon'] - 1) * 100:+.1f} %".replace(".", ","),
            fmt(r["m2_galpon"] / 1800, 1),
            fmt(r["ciclos_anio"], 2),
        ]))


if __name__ == "__main__":
    filas = generar_csv()
    verificar_balances(filas)
    print(f"OK: {len(filas)} escenarios escritos y balances verificados")
    if "--tablas" in sys.argv:
        imprimir_tablas()
