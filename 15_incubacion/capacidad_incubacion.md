# Capacidad de incubación por escala

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B · Cálculo reproducible: `python3 ../14_alimento_balanceado/modelo_upstream.py --tablas` (tablas T3–T3e) · Método: [`modelo_incubacion.md`](modelo_incubacion.md)

> **Solo aplica a las opciones B (huevo fértil comprado + incubación propia) y C (reproductoras, fase futura).** En la opción A (compra de pollito) la capacidad propia de incubación es **0**. Ninguna escala ni opción está elegida. Parámetros = supuestos (SUP-14B-02 a SUP-14B-06).

---

## 1. Cálculo: pollitos requeridos → huevos incubados → capacidad semanal instalada

```
capacidad semanal de carga (huevos/semana)  = huevos incubados/semana × (1 + margen)
posiciones de incubadora (huevos)           = huevos incubados/semana × (18 + 1 d) / 7 × (1 + margen)
posiciones de nacedora (huevos)             = huevos a nacedora/semana × (3 + 1 d) / 7 × (1 + margen)
capacidad de almacén de huevo (huevos)      = huevos recibidos/semana × días de almacenamiento / 7 × (1 + margen)
pollitos por nacimiento                     = pollitos vendibles/semana / nacimientos por semana
pollitos/h en selección-vacunación-carga    = pollitos por nacimiento / horas de ventana
```

Las posiciones salen de la **ley de Little** (ocupación = flujo × tiempo de permanencia), con los días de limpieza entre cargas. Test U02: la capacidad instalada siempre cubre la carga semanal requerida más el margen.

## 2. Resultados (perfil y desempeño de granja medios, 5 d de faena, incubación media, margen 15 %, 5 d de almacenamiento)

| Planta (aves faenadas/día) | Pollitos vendibles/semana | Pollitos nacidos/semana | Huevos fértiles/semana | Huevos incubados/semana | **Huevos recibidos/semana** | Huevos por pollito vendible | **Capacidad semanal de carga** | Posiciones de incubadora | Posiciones de nacedora | Almacén de huevo |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 13.197 | 13.331 | 14.886 | 16.181 | **16.344** | 1,238 | **18.608** | 50.508 | 10.580 | 13.426 |
| 5.000 | 26.395 | 26.662 | 29.773 | 32.362 | **32.689** | 1,238 | **37.216** | 101.015 | 21.160 | 26.851 |
| 10.000 | 52.790 | 53.323 | 59.546 | 64.724 | **65.377** | 1,238 | **74.432** | 202.030 | 42.320 | 53.703 |
| 20.000 | 105.580 | 106.646 | 119.091 | 129.447 | **130.755** | 1,238 | **148.864** | 404.060 | 84.640 | 107.406 |

`[ESTIMACIÓN]` · ESCENARIO. Huevos recibidos por año a ritmo pleno ≈ semana × 52,14 (cota superior; con feriados, algo menos). Con 6 días de faena, todo ×1,2.

### 2.1 Por nivel de incubación (huevos recibidos/semana; favorable / medio / desfavorable)

| Planta | Favorable (HOS 87,1 %) | Medio (82,4 %) | Desfavorable (75,8 %) |
|---|---|---|---|
| 2.500 | 15.298 | 16.344 | 18.130 |
| 5.000 | 30.596 | 32.689 | 36.260 |
| 10.000 | 61.193 | 65.377 | 72.521 |
| 20.000 | 122.385 | 130.755 | 145.041 |

Diferencia entre extremos: **~18,5 %** más huevos en el desfavorable que en el favorable.

### 2.2 Sensibilidad (10.000 aves faenadas/día, medio)

| Variación | Huevos recibidos/semana | Cambio | Posiciones de incubadora | Posiciones de nacedora |
|---|---|---|---|---|
| Base | 65.377 | — | 202.030 | 42.320 |
| Fertilidad 0,85 | 70.761 | +8,2 % | 218.668 | 45.805 |
| Fertilidad 0,96 | 62.653 | −4,2 % | 193.612 | 40.557 |
| Incubabilidad de fértiles 0,85 | 69.223 | +5,9 % | 213.914 | 44.809 |
| Incubabilidad de fértiles 0,935 | 62.930 | −3,7 % | 194.467 | 40.736 |
| Descarte en selección 3 % | 66.725 | +2,1 % | 206.196 | 43.193 |
| Pérdida en recepción 3 % | 66.725 | +2,1 % | 202.030 | 42.320 |
| Margen de capacidad 0 % | 65.377 | 0 % | 175.678 | 36.800 |
| Margen de capacidad 25 % | 65.377 | 0 % | 219.598 | 46.000 |

**Lectura:** la **fertilidad** es la variable más sensible (depende de las reproductoras, que en la opción B **no controla la empresa**). Con ovoscopia en la transferencia, las posiciones de nacedora bajan en la proporción de infértiles retirados (test U10).

### 2.3 Expedición: pollitos por nacimiento (y pollitos/h con 10 h – 6 h de ventana)

| Planta | 1 nacimiento/semana | 2 nacimientos/semana | 3 nacimientos/semana | 4 nacimientos/semana |
|---|---|---|---|---|
| 2.500 | 13.197 (1.320–2.200/h) | 6.599 (660–1.100/h) | 4.399 (440–733/h) | 3.299 (330–550/h) |
| 5.000 | 26.395 (2.639–4.399/h) | 13.197 (1.320–2.200/h) | 8.798 (880–1.466/h) | 6.599 (660–1.100/h) |
| 10.000 | 52.790 (5.279–8.798/h) | 26.395 (2.639–4.399/h) | 17.597 (1.760–2.933/h) | 13.197 (1.320–2.200/h) |
| 20.000 | 105.580 (10.558–17.597/h) | 52.790 (5.279–8.798/h) | 35.193 (3.519–5.866/h) | 26.395 (2.639–4.399/h) |

`[SUPUESTO]` SUP-14B-06. **Tensión de diseño:** los alojamientos en granja son por **lote completo** (15.000–60.000 pollitos; [`integracion_upstream.md` §1.2](../14_alimento_balanceado/integracion_upstream.md)). A 2.500 aves/día, llenar una granja de 30.000 plazas en un solo alojamiento exige **~2,3 semanas de producción de la propia incubadora**: o la incubadora acumula (no se puede: el pollito se entrega el día de nacimiento), o la granja se llena en varios días/edades (peor para todo dentro–todo fuera), o se usan granjas chicas. **La incubación propia a escala chica choca con el tamaño de lote de granja** (DPV-133, DPV-14B-10).

## 3. Opción C (fase futura): reproductoras equivalentes

| Planta | Reproductoras hembras en postura equivalentes |
|---|---|
| 2.500 | ~3.700 |
| 5.000 | ~7.300 |
| 10.000 | ~14.700 |
| 20.000 | ~29.300 |

`[ESTIMACIÓN]` de `03` (~3,6 pollitos por reproductora alojada por semana; DPV-045). **Solo fase futura** (test U07: 0 en Fase 0 y Fase 1). No incluye recría (~24–26 semanas hasta el inicio de postura, `[ESTIMACIÓN]` 03), machos, reposición, granjas de reproductoras ni su capacidad; todo eso queda PENDIENTE.

## 4. Escala relativa (contexto, `[PVDP]`)

Ejemplos de capacidad de plantas de incubación citados en extractos: una planta de **80.000 huevos/semana en dos nacimientos** (tesis de UNCuyo) y una de **~400.000 pollitos/semana en cuatro nacimientos** (FTE-14B-004 `[PVDP]`, contexto y fecha a verificar). La producción nacional se estima en ~18–20 M pollitos/semana (FTE-071 `[PVDP]`). Con esas referencias, la demanda de las escalas 2.500–10.000 equivale a una planta chica o a una fracción de una planta industrial; solo 20.000 se acerca a una planta mediana. **No se infiere la escala mínima eficiente**: requiere datos de incubadoras y costos (DPV-14B-01, fase económica).
