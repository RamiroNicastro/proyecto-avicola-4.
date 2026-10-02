# Conclusiones de incubación y pollito BB (sesión 14B)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de sincronización productiva) · Base: [`modelo_incubacion.md`](modelo_incubacion.md), [`capacidad_incubacion.md`](capacidad_incubacion.md), [`compra_vs_incubacion.md`](compra_vs_incubacion.md), [`guia_ramiro.md`](guia_ramiro.md), [`../14_alimento_balanceado/integracion_upstream.md`](../14_alimento_balanceado/integracion_upstream.md), [`../14_alimento_balanceado/modelo_upstream.py`](../14_alimento_balanceado/modelo_upstream.py)

> **Modelo preliminar completado** (físico, 21/21 tests). **Sin decisión:** DEC-023 abierta; SUP-034 vigente (no se asume incubadora propia); reproductoras solo en la arquitectura futura. **Sin costos, sin fabricante, sin cadencia elegida, sin datos de campo.** Toda cifra externa `[PVDP]`.

---

## 1. Hallazgos

1. **Demanda de pollitos (medio, 5 d):** 13.197 / 26.395 / 52.790 / 105.580 pollitos por **semana plena** y 0,66 / 1,32 / 2,64 / 5,28 M pollitos/año para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas/día. El margen por mortalidad (granja + transporte) es 3,3 / **5,6** / 9,2 % sobre las aves faenadas (favorable / medio / desfavorable).
2. **Tiempos (corregido en v1.1):** la **incubación** (carga → nacimiento) dura **21 días** en el modelo (18 setter + 3 hatcher). El **lead time recepción del huevo → nacimiento** es 24 / 26 / 28 días con 3 / 5 / 7 días de almacenamiento previo; el lead time **recepción → pollito entregado** agrega selección, vacunación, expedición y viaje (horas **PENDIENTES**), por lo que el modelo solo informa la cota inferior. Huevo → faena: ≥ 71–75 días.
3. **Huevos (opción B, incubación media):** ~1,24 huevos recibidos por pollito vendible; 16.344 / 32.689 / 65.377 / 130.755 huevos recibidos y 16.181 / 32.362 / 64.724 / 129.447 **cargados** por semana (−6 % / +11 % en los niveles favorable / desfavorable).
4. **Setter y hatcher por separado (corregido en v1.1):** las cifras v1.0 (50.508 / 101.015 / 202.030 / 404.060) eran solo setter en flujo continuo × margen; se retiran. Con cadencia por lotes y margen de 15 %: **setter 55.824 / 111.648 / 223.296 / 446.593 posiciones** (igual para las cinco cadencias ilustrativas) y **hatcher 12.343–18.515 / 24.687–37.030 / 49.373–74.060 / 98.747–148.120** según 3 o 1–2 nacimientos por semana. Utilización media de diseño: setter 79 %, hatcher 50–75 %.
5. **Demanda media semanal ≠ lote de nacimiento:** con N nacimientos por semana, el lote es la demanda / N (a 10.000 aves/día: 52.790 / 26.395 / 17.597 / 10.558 pollitos con 1 / 2 / 3 / 5 nacimientos). La cadencia **no se elige**: define el tamaño del hatcher, los camiones, el llenado de galpones y la dispersión de edad a faena.
6. **Fertilidad e incubabilidad tienen la misma elasticidad (−1)** (corregido en v1.1): ninguna es "más sensible" por la fórmula. En el modelo, la fertilidad mueve más los huevos (+4,5 % / −3,2 % en sus extremos, contra +3,4 % / −2,2 % de la incubabilidad) **solo porque su rango supuesto es más ancho** (7,6 % vs 5,6 % del valor medio). En la opción B, la fertilidad depende del proveedor del huevo.
7. **Incubar huevo comprado sustituye la dependencia** de proveedores de pollito por dependencia de proveedores de huevo fértil; la concentración y disponibilidad real de esa oferta es **DPV-154** (no hay evidencia de que sea mayor o menor que la de pollito). La independencia de suministro solo llega con reproductoras (C), la opción más intensiva en capital, know-how y plazo.
8. **Sincronización con galpones y faena (reformulado en v1.1):** existe un **posible problema de sincronización** entre tamaño de lote de nacimiento, capacidad de galpones y cadencia de faena, más visible a escala chica (a 2.500 aves/día, un galpón equivalente de 1.800 m² necesita ~1,7–8,7 nacimientos para llenarse según la cadencia y ~8,7 días de faena para cosecharse). **No demuestra incompatibilidad:** debe validarse con la arquitectura real de las granjas (galpones por granja, plazas por galpón, tolerancia de edad, cosecha escalonada). Detalle: [`../14_alimento_balanceado/integracion_upstream.md` §4](../14_alimento_balanceado/integracion_upstream.md).
9. **Escala relativa:** las demandas de 2.500–10.000 aves/día equivalen a una planta de incubación chica o a una fracción de una industrial (ejemplos de 80.000–400.000/semana citados, `[PVDP]`); la escala mínima eficiente **no se infiere** sin costos.

## 2. Opciones a comparar por arquitectura de referencia (sin orden obligatorio)

| Arquitectura de referencia | Pollito | Capacidad propia de incubación |
|---|---|---|
| 0 y 1 | A. Compra (≥ 2 proveedores, contratos) | 0 |
| 2 | A. Compra | 0 |
| 3 | B. Huevo fértil + incubación | Setter y hatcher según cadencia ([`capacidad_incubacion.md` §3](capacidad_incubacion.md)) |
| Futura | C. Reproductoras, solo con justificación | B + reproductoras |

Las arquitecturas son **referencias de madurez**, no un recorrido obligatorio: si hubiera demanda, capital y ventaja económica demostrada, la incubación podría evaluarse antes. Las tres opciones son **escenarios de comparación**; la compra de pollito es solo el **benchmark** contra el que se miden las demás en CAPEX/OPEX.

## 3. Datos faltantes críticos

| Dato | Registro |
|---|---|
| Oferta de pollito para terceros: volumen, **días de nacimiento**, **tamaño mínimo de lote**, mínimo contractual semanal/mensual, flexibilidad de programación, uniformidad, ventana de entrega, estacionalidad, capacidad futura | DPV-006, DPV-047, DPV-133 |
| Fertilidad e incubabilidad reales (por edad de reproductoras), descarte, pérdidas | DPV-153, DPV-045 |
| Oferta de huevo fértil para terceros (concentración y disponibilidad) | DPV-154 |
| Habilitación SENASA de planta de incubación | DPV-007 |
| Horas de selección, vacunación, expedición y viaje; capacidad de camiones de pollitos y huevos | DPV-047, DPV-084 |
| Arquitectura real de granjas: galpones por granja, plazas por galpón, llenado por galpón o granja, tolerancia de edad, cosecha escalonada | DPV-048, DPV-133 |

## 4. Calidad

**MEDIA** como modelo físico (cadena y tiempos explícitos, setter/hatcher con cadencia simulada, conservación temporal probada); **BAJA** como evidencia (ningún parámetro de incubación ni de cadencia verificado; referencias de pico de manual leídas en extractos).
