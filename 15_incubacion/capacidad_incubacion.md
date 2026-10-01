# Capacidad de incubación por escala: setter, hatcher y cadencia

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de sincronización: setter y hatcher por separado, cadencia de cargas/nacimientos) · Cálculo reproducible: `python3 ../14_alimento_balanceado/modelo_upstream.py --tablas` (tablas A–D) · Método: [`modelo_incubacion.md`](modelo_incubacion.md)

> **Solo aplica a las opciones B (huevo fértil comprado + incubación propia) y C (reproductoras, arquitectura futura).** En la opción A (compra de pollito) la capacidad propia de incubación es **0**. Ninguna escala, opción ni cadencia está elegida. Parámetros = supuestos (SUP-14B-02 a SUP-14B-06).

---

## 1. Corrección de la versión 1.0: qué eran las "posiciones de incubadora"

Las cifras **50.508 / 101.015 / 202.030 / 404.060** de la v1.0 eran **solo setter** (incubadora), calculadas como **flujo continuo** (ley de Little: huevos cargados/semana × (18 + 1 d de limpieza) / 7) **× 1,15 de margen**. No mezclaban hatcher, pero tenían dos problemas:

1. **Ignoraban que la carga es por lotes.** Una incubadora se carga en lotes discretos (1 a 5 por semana); la ocupación **máxima** es mayor que la media continua. Con cualquier cadencia simulada, el setter necesita **48.543** posiciones (2.500 aves/día) antes de margen, no 43.920; con margen, **55.824** (+10,5 % sobre la v1.0).
2. **El hatcher quedaba subdimensionado con pocos nacimientos por semana:** con 1–2 nacimientos/semana necesita 16.100 posiciones antes de margen (2.500 aves/día), no 9.200; con margen, **18.515** (+75 % sobre los 10.580 de la v1.0).

**Las cifras v1.0 se retiran.** En su lugar se informan: (a) ocupación media continua **sin margen** (referencia), (b) ocupación máxima por cadencia (simulada) y (c) posiciones de diseño = (b) × (1 + margen).

## 2. Cálculo

```
huevos cargados/semana    = pollitos vendibles / (1 − descarte) / (fertilidad × incubabilidad × (1 − pérdida en transferencia))
huevos transferidos/sem   = cargados × (1 − pérdida en transferencia) × (fertilidad, solo si hay ovoscopia)

SETTER  continuo (medio)  = cargados/semana    × (18 + 1) / 7          ← permanencia setter + limpieza
HATCHER continuo (medio)  = transferidos/semana × (3 + 1) / 7          ← permanencia hatcher + limpieza

CADENCIA: N cargas = N nacimientos por semana, en días fijos de la semana, lotes iguales
  lote de carga           = cargados/semana / N
  lote de nacimiento      = pollitos vendibles/semana / N
  setter por cadencia     = ocupación MÁXIMA simulada (cada lote ocupa [t, t+19) en setter)
  hatcher por cadencia    = ocupación MÁXIMA simulada (cada lote ocupa [t+18, t+22) en hatcher)
  posiciones de diseño    = por cadencia × (1 + margen)
  utilización media       = ocupación media / posiciones de diseño
```

- **Setter y hatcher no se suman como capacidad:** son etapas y máquinas distintas, con flujos distintos (cargados vs transferidos) y permanencias distintas. La suma solo se informa como **posiciones físicas instaladas** (inventario de máquinas), no como capacidad de producción.
- **Huevos en proceso (WIP)** = cargados × 18/7 + transferidos × 3/7: huevos físicamente en máquinas en un momento medio (sin días de limpieza). Aquí sí tiene sentido sumar.
- Patrones de cadencia **ilustrativos** (SUP-14B-06): 1 = lunes; 2 = lunes y jueves; 3 = lunes, miércoles, viernes; 4 = lunes, martes, jueves, viernes; 5 = lunes a viernes. La granularidad real de las máquinas (tamaño de cada incubadora o sala) **no se modela** (sin fabricante): se supone que las posiciones son divisibles.
- **Tests:** U12 (setter y hatcher con permanencias y flujos propios; cambiar el hatcher no cambia el setter), U13 (la media temporal simulada coincide exactamente con Little; los huevos cargados en régimen igualan la demanda; la ocupación máxima nunca supera las posiciones de diseño), U02 (diseño ≥ continuo × (1 + margen)).

## 3. Resultados (perfil y desempeño de granja medios, 5 d de faena, incubación media)

### 3.1 Flujos semanales y ocupación media

| Planta (aves faenadas/día) | Pollitos vendibles/semana | **Huevos recibidos/semana** | **Huevos cargados/semana** | **Huevos transferidos/semana** | Setter continuo (sin margen) | Hatcher continuo (sin margen) | Huevos en proceso (WIP) | Capacidad semanal de carga (+15 %) |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 13.197 | 16.344 | 16.181 | 16.100 | 43.920 | 9.200 | 48.508 | 18.608 |
| 5.000 | 26.395 | 32.689 | 32.362 | 32.200 | 87.839 | 18.400 | 97.016 | 37.216 |
| 10.000 | 52.790 | 65.377 | 64.724 | 64.400 | 175.678 | 36.800 | 194.032 | 74.432 |
| 20.000 | 105.580 | 130.755 | 129.447 | 128.800 | 351.357 | 73.600 | 388.064 | 148.864 |

`[ESTIMACIÓN]` · ESCENARIO. Huevos por pollito vendible: ~1,238. Con ovoscopia en la transferencia, los transferidos (y el hatcher) bajan ~8 % (infértiles retirados).

### 3.2 Setter y hatcher por cadencia (margen 15 %)

| Planta | Cargas = nacimientos/semana | Lote de carga (huevos) | **Lote de nacimiento (pollitos)** | Setter por cadencia | **Setter diseño** | Hatcher por cadencia | **Hatcher diseño** | Utilización media setter / hatcher |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 1 | 16.181 | 13.197 | 48.543 | **55.824** | 16.100 | **18.515** | 79 % / 50 % |
| 2.500 | 2 | 8.090 | 6.599 | 48.543 | **55.824** | 16.100 | **18.515** | 79 % / 50 % |
| 2.500 | 3 | 5.394 | 4.399 | 48.543 | **55.824** | 10.733 | **12.343** | 79 % / 75 % |
| 2.500 | 5 | 3.236 | 2.639 | 48.543 | **55.824** | 12.880 | **14.812** | 79 % / 62 % |
| 5.000 | 1 | 32.362 | 26.395 | 97.085 | **111.648** | 32.200 | **37.030** | 79 % / 50 % |
| 5.000 | 2 | 16.181 | 13.197 | 97.085 | **111.648** | 32.200 | **37.030** | 79 % / 50 % |
| 5.000 | 3 | 10.787 | 8.798 | 97.085 | **111.648** | 21.467 | **24.687** | 79 % / 75 % |
| 5.000 | 5 | 6.472 | 5.279 | 97.085 | **111.648** | 25.760 | **29.624** | 79 % / 62 % |
| 10.000 | 1 | 64.724 | 52.790 | 194.171 | **223.296** | 64.400 | **74.060** | 79 % / 50 % |
| 10.000 | 2 | 32.362 | 26.395 | 194.171 | **223.296** | 64.400 | **74.060** | 79 % / 50 % |
| 10.000 | 3 | 21.575 | 17.597 | 194.171 | **223.296** | 42.933 | **49.373** | 79 % / 75 % |
| 10.000 | 5 | 12.945 | 10.558 | 194.171 | **223.296** | 51.520 | **59.248** | 79 % / 62 % |
| 20.000 | 1 | 129.447 | 105.580 | 388.342 | **446.593** | 128.800 | **148.120** | 79 % / 50 % |
| 20.000 | 2 | 64.724 | 52.790 | 388.342 | **446.593** | 128.800 | **148.120** | 79 % / 50 % |
| 20.000 | 3 | 43.149 | 35.193 | 388.342 | **446.593** | 85.867 | **98.747** | 79 % / 75 % |
| 20.000 | 5 | 25.889 | 21.116 | 388.342 | **446.593** | 103.040 | **118.496** | 79 % / 62 % |

`[SUPUESTO]` (cadencias ilustrativas). La cadencia 4 está en el CSV (bloque `2_incubacion_cadencia`). Márgenes de 10 % y 20 %: CSV.

**Lectura:**
- **Setter:** con 19 días de ocupación por lote (18 + limpieza), en régimen siempre conviven ~3 semanas de carga, sea cual sea la cadencia; las posiciones del setter dependen poco de la cadencia (con patrones semanales fijos).
- **Hatcher:** depende **mucho** de la cadencia. Con 1–2 nacimientos por semana cada lote ocupa el hatcher 4 días y no se superpone con el siguiente lo suficiente: hay que tener capacidad para **una semana entera de nacimientos** en un momento dado, y la utilización media cae al 50 %. Con 3 nacimientos (lunes, miércoles, viernes) el hatcher baja ~33 %.
- **Utilización media de diseño:** setter 79 % y hatcher 50–75 %, **antes** de cualquier rampa o caída de la faena. No es una conclusión económica: es el costo físico de la cadencia y del margen.

## 4. Demanda media semanal ≠ tamaño de lote de nacimiento

La demanda de pollitos es una **media semanal**; la incubadora produce **lotes** (nacimientos). Con N nacimientos por semana, **lote = demanda / N** (test U15). Ejemplo a 10.000 aves/día: demanda 52.790 pollitos/semana → lotes de 52.790 (1 nacimiento), 26.395 (2), 17.597 (3) o 10.558 (5).

El tamaño de lote importa para:

| Tema | Por qué |
|---|---|
| Utilización de incubadoras | Pocos nacimientos grandes → hatcher grande y subutilizado (§3.2) |
| Transporte | Lotes grandes concentran camiones en un día; lotes chicos los reparten (capacidad de camión PENDIENTE) |
| Llenado de galpones | Si el lote de nacimiento es menor que el galpón, un galpón se llena con varios nacimientos (edades distintas) |
| Sincronización con faena | La edad de las aves a la faena hereda la dispersión de edad de la colocación |

Selección, vacunación y expedición por nacimiento (pollitos/h con 10 h – 6 h de ventana, SUP-14B-06):

| Planta | 1 nacimiento/semana | 2 | 3 | 5 |
|---|---|---|---|---|
| 2.500 | 13.197 (1.320–2.200/h) | 6.599 (660–1.100/h) | 4.399 (440–733/h) | 2.639 (264–440/h) |
| 10.000 | 52.790 (5.279–8.798/h) | 26.395 (2.639–4.399/h) | 17.597 (1.760–2.933/h) | 10.558 (1.056–1.760/h) |
| 20.000 | 105.580 (10.558–17.597/h) | 52.790 (5.279–8.798/h) | 35.193 (3.519–5.866/h) | 21.116 (2.112–3.519/h) |

**No se selecciona cadencia.** La cadencia real la fija la incubadora (si se compra pollito) o la operación (si se incuba): DPV-14B-10.

## 5. Sensibilidad a fertilidad e incubabilidad

Huevos recibidos = demanda / (fertilidad × incubabilidad de fértiles × otros rendimientos). Ambos son **factores multiplicativos**: la **elasticidad** de los huevos respecto de cada uno es exactamente **−1** (test U17): un 1 % menos de fertilidad o un 1 % menos de incubabilidad exigen el mismo ~1 % más de huevos.

| (10.000 aves/día, medio) | Fertilidad | Incubabilidad de fértiles |
|---|---|---|
| Elasticidad de huevos recibidos | −1,000 | −1,000 |
| Rango de supuesto (SUP-14B-02) | 0,88–0,95 (7,6 % del valor medio) | 0,87–0,92 (5,6 %) |
| Variación de huevos en el extremo bajo / alto | +4,5 % / −3,2 % | +3,4 % / −2,2 % |

Otras variaciones (10.000, medio): descarte en selección 3 % → +2,1 % de huevos; pérdida en recepción 3 % → +2,1 % (no cambia el setter, porque se pierde antes de cargar).

**Lectura (corrige la v1.0):** ninguno de los dos factores es "más sensible" por la fórmula. En este modelo la fertilidad genera más variación **solo porque su rango supuesto es más ancho**. Lo que sí distingue a la fertilidad en la opción B es **quién la controla**: depende de las reproductoras del proveedor del huevo; la incubabilidad depende en parte del manejo propio de la incubación (y también de la calidad del huevo).

## 6. Opción C (arquitectura futura): reproductoras equivalentes

| Planta | Reproductoras hembras en postura equivalentes |
|---|---|
| 2.500 | ~3.700 |
| 5.000 | ~7.300 |
| 10.000 | ~14.700 |
| 20.000 | ~29.300 |

`[ESTIMACIÓN]` de `03` (~3,6 pollitos por reproductora alojada por semana; DPV-045). **Solo arquitectura futura** (test U07: 0 en las arquitecturas 0 y 1). No incluye recría, machos, reposición ni granjas de reproductoras: PENDIENTE.

## 7. Escala relativa (contexto, `[PVDP]`)

Ejemplos de capacidad de plantas de incubación citados en extractos: una planta de **80.000 huevos/semana en dos nacimientos** (tesis de UNCuyo) y una de **~400.000 pollitos/semana en cuatro nacimientos** (FTE-14B-004 `[PVDP]`, contexto y fecha a verificar). La producción nacional se estima en ~18–20 M pollitos/semana (FTE-071 `[PVDP]`). **No se infiere la escala mínima eficiente** (requiere datos de incubadoras y costos: DPV-14B-01, fase económica).

Sincronización con granjas y faena: [`../14_alimento_balanceado/integracion_upstream.md` §4](../14_alimento_balanceado/integracion_upstream.md).
