# Alimentación y agua en la crianza

**Fecha:** 2026-09-29 · **Versión:** 1 · Fase 0

> **Alcance.** Sensibilidad **física** del alimento y del agua: kg por ave, toneladas por escenario, fases y materias primas que mueven el costo. **Sin precios** (esta fase no los habilita) y **sin formular dietas** (tarea de un nutricionista). La decisión de fabricar o comprar alimento corresponde a [`../14_alimento_balanceado/`](../14_alimento_balanceado/README.md) (DEC-024). Escenarios: [`escenarios_produccion.csv`](escenarios_produccion.csv). Fuentes: extractos `[PVDP]` (acceso directo bloqueado).

---

## 1. Conversión alimenticia (FCR)

### 1.1 Definición

**FCR (índice de conversión) = kg de alimento consumido / kg de peso vivo producido.** Un FCR de 1,70 significa que para producir 1 kg de pollo vivo se usaron 1,70 kg de alimento.

Hay varias versiones y **deben declararse siempre**:

| Versión | Numerador | Denominador | Uso |
|---|---|---|---|
| **FCR de campo (la usada en este proyecto)** | Alimento total entregado al lote | kg vivo **cargado** (aves vivas que salen) | Económica: incluye el alimento que comieron las aves que murieron y los desperdicios |
| FCR biológico | Alimento consumido | kg vivo de aves vivas + kg de aves muertas | Técnica: mide la eficiencia del ave, no del lote |
| FCR corregido a peso estándar | FCR ajustado a un peso de referencia (p. ej. ±0,01–0,03 por cada 100 g de diferencia; `[ESTIMACIÓN]`, la regla la define cada empresa) | — | Comparar lotes de pesos distintos |
| FCR de planta | Alimento | kg vivo **recibido en planta** (después de ayuno, merma y DOA) | Liquidación con integrados o compra de pollo vivo |

### 1.2 Qué lo determina

- **Peso y edad de faena:** el FCR **empeora a medida que el ave crece** (cada kg adicional cuesta más alimento). Comparar FCR de lotes con pesos distintos sin corregir es un error frecuente.
- **Genética** (Cobb, Ross, Hubbard) y calidad del pollito.
- **Ambiente:** frío (energía para calefacción corporal), calor (el ave come menos y crece menos), ventilación, calidad de aire.
- **Sanidad:** enfermedades subclínicas (coccidiosis, enteritis) empeoran el FCR sin aumentar mucho la mortalidad.
- **Alimento:** formulación, calidad de materias primas (micotoxinas), forma física (pellet de buena calidad vs harina), desperdicio en comederos.
- **Mortalidad tardía:** un ave que muere a los 40 días comió ~4 kg de alimento que no se venden.

### 1.3 Ejemplos: alimento por ave y por millón de aves

Alimento por ave faenada = **peso vivo × FCR**.

| Peso vivo | FCR 1,5 | FCR 1,6 | FCR 1,7 | FCR 1,8 | FCR 1,9 |
|---|---|---|---|---|---|
| 2,4 kg — kg/ave | 3,60 | 3,84 | 4,08 | 4,32 | 4,56 |
| 2,4 kg — t por millón de aves | 3.600 | 3.840 | 4.080 | 4.320 | 4.560 |
| **2,9 kg — kg/ave** | **4,35** | **4,64** | **4,93** | **5,22** | **5,51** |
| **2,9 kg — t por millón de aves** | **4.350** | **4.640** | **4.930** | **5.220** | **5.510** |
| 3,4 kg — kg/ave | 5,10 | 5,44 | 5,78 | 6,12 | 6,46 |
| 3,4 kg — t por millón de aves | 5.100 | 5.440 | 5.780 | 6.120 | 6.460 |

`[ESTIMACIÓN]` (cálculo).

### 1.4 Cuánto cuesta (físicamente) empeorar 0,1 punto

**+0,1 de FCR = +0,1 kg de alimento por kg vivo.**

| Peso vivo | Alimento extra por ave | Por millón de aves | % sobre FCR 1,7 |
|---|---|---|---|
| 2,4 kg | +0,24 kg | **+240 t** | +5,9 % |
| 2,9 kg | +0,29 kg | **+290 t** | +5,9 % |
| 3,4 kg | +0,34 kg | **+340 t** | +5,9 % |

En el escenario medio de 10.000 aves faenadas/día (2,5 M aves faenadas/año), **+0,1 de FCR ≈ +727 t de alimento por año** (≈ 26 camiones de 28 t). Como el alimento es el principal costo de la crianza (se cita habitualmente "65–70 %", dato a validar: DPV-019), **el FCR es el indicador económico número uno de la granja**. Pasar de FCR 1,85 (desfavorable) a 1,60 (favorable) ahorra ~15 % del alimento.

---

## 2. Alimento por escenario

Total = aves cargadas × peso vivo × FCR de campo. "Planta de N aves/día" = N **aves faenadas** por día de faena. Formato **favorable / medio / desfavorable** (FCR 1,60 / 1,70 / 1,85; mortalidad 3/5/8 %), **perfil medio** (47 d, 2,9 kg).

| Planta (aves **faenadas**/día) | Días/sem | kg de alimento por ave faenada | t/semana plena | t/semana (promedio anual) | t/mes (promedio) | t/año | t de un ciclo de crianza a ritmo pleno* |
|---|---|---|---|---|---|---|---|
| 2.500 | 5 | 4,65 / 4,94 / 5,39 | 58 / 62 / 67 | 56 / 59 / 65 | 242 / 258 / 281 | 2.906 / 3.091 / 3.370 | 390 / 415 / 453 |
| 2.500 | 6 | 4,65 / 4,94 / 5,39 | 70 / 74 / 81 | 67 / 71 / 78 | 291 / 309 / 337 | 3.487 / 3.709 / 4.044 | 468 / 498 / 543 |
| 5.000 | 5 | 4,65 / 4,94 / 5,39 | 116 / 124 / 135 | 111 / 119 / 129 | 484 / 515 / 562 | 5.812 / 6.181 / 6.740 | 780 / 830 / 905 |
| 5.000 | 6 | 4,65 / 4,94 / 5,39 | 139 / 148 / 162 | 134 / 142 / 155 | 581 / 618 / 674 | 6.974 / 7.417 / 8.088 | 937 / 996 / 1.086 |
| 10.000 | 5 | 4,65 / 4,94 / 5,39 | 232 / 247 / 270 | 223 / 237 / 259 | 969 / 1.030 / 1.123 | 11.623 / 12.362 / 13.480 | 1.561 / 1.660 / 1.810 |
| 10.000 | 6 | 4,65 / 4,94 / 5,39 | 279 / 297 / 324 | 267 / 284 / 310 | 1.162 / 1.236 / 1.348 | 13.948 / 14.835 / 16.176 | 1.873 / 1.992 / 2.172 |
| 20.000 | 5 | 4,65 / 4,94 / 5,39 | 465 / 494 / 539 | 446 / 474 / 517 | 1.937 / 2.060 / 2.247 | 23.246 / 24.724 / 26.960 | 3.122 / 3.320 / 3.620 |
| 20.000 | 6 | 4,65 / 4,94 / 5,39 | 558 / 593 / 647 | 535 / 569 / 620 | 2.325 / 2.472 / 2.696 | 27.896 / 29.669 / 32.352 | 3.746 / 3.984 / 4.344 |

\* Alimento de todos los lotes de un ciclo de crianza (edad de faena) al ritmo de la semana plena = t/semana plena × edad / 7. Es una **medida física del capital de trabajo** (cota superior del alimento inmovilizado en aves en crianza), sin plazos de pago ni de cobro. Versión 1.1: se distinguen semana plena y promedio anual (antes se informaba el total anual / 52 como "t/semana").

`[ESTIMACIÓN]` · ESCENARIO. El kg por ave faenada es algo mayor que peso × FCR porque incluye el alimento de las aves muertas en transporte. Con perfiles liviano y pesado (desempeño medio, 10.000 aves faenadas/día, 5 d/sem): **3,80 kg/ave y 9.509 t/año** (liviano) y **6,21 kg/ave y 15.517 t/año** (pesado). Rango completo en el CSV (2.200–40.400 t/año según planta y supuestos).

**Orden de magnitud logístico** `[ESTIMACIÓN]`: con camiones graneleros de ~28 t, el escenario medio de 10.000 aves faenadas/día (247 t por semana plena) implica **~9 entregas de alimento por semana** a granjas; el de 20.000, ~18. Cada entrega es también un riesgo de bioseguridad ([`bioseguridad.md`](bioseguridad.md)).

---

## 3. Fases: inicio, crecimiento y terminación

| Fase | Edad (típica) | Forma física | Característica nutricional (conceptual) | % del alimento total — liviano (38 d) | medio (47 d) | pesado (54 d) |
|---|---|---|---|---|---|---|
| **Inicio** (a veces "preinicio" + "inicio") | 0–10 d | Migaja o micropellet | Mayor proteína y aminoácidos, alta digestibilidad; se consume poco pero es clave para el desarrollo intestinal e inmune | ~7 % | **~5 %** | ~4 % |
| **Crecimiento** | 11–24 d | Pellet | Transición | ~36 % | **~27 %** | ~22 % |
| **Terminación** (puede dividirse en terminación 1 y 2) | 25 d – faena | Pellet | Mayor energía (más maíz y aceite), menor proteína relativa | ~57 % | **~68 %** | ~74 % |
| **Retiro** (dentro de la terminación) | Últimos días | Pellet | Sin aditivos que tengan período de carencia antes de la faena | — | — | — |

`[ESTIMACIÓN]` a partir de una curva de consumo acumulado de referencia con la forma de las tablas de los manuales genéticos (SUP-032; FTE-140, FTE-142 `[PVDP]`). Por ave del perfil medio: **~0,26 kg de inicio, ~1,3 kg de crecimiento y ~3,4 kg de terminación**.

**Implicancia:** la **terminación concentra ~2/3 del tonelaje**. Las aves más pesadas desplazan todavía más el consumo hacia la terminación, que es la fase con peor conversión marginal.

---

## 4. Composición típica y materias primas que mueven el costo

> No es una fórmula. Son **rangos de inclusión de orden de magnitud** para una dieta maíz–soja típica, tomados de literatura técnica general `[ESTIMACIÓN]` / `[PVDP]` (FTE-160). La fórmula real depende del nutricionista, de los precios relativos y de la disponibilidad regional.

| Componente | Inclusión típica (% del alimento) | Función | Peso en el costo (cualitativo) |
|---|---|---|---|
| **Maíz** (o sorgo como sustituto parcial) | ~55–65 % | Energía (almidón) | **Muy alto**: principal insumo por volumen |
| **Harina de soja** (y/o expeller de soja) | ~25–35 % (más en inicio) | Proteína y aminoácidos (aporta la mayor parte de los aminoácidos de la dieta, FTE-160) | **Muy alto** |
| Aceite o grasa (aceite de soja, grasas) | ~1–5 % (más en terminación) | Densidad energética | Medio (alto precio por kg) |
| Fosfato mono/dicálcico | ~1–2 % | Fósforo | Medio |
| Carbonato de calcio (conchilla) | ~1 % | Calcio | Bajo |
| Sal / bicarbonato de sodio | ~0,3–0,5 % | Sodio, cloro | Bajo |
| Premezcla vitamínico-mineral | ~0,2–0,5 % | Vitaminas y oligoelementos | Medio (alto precio por kg) |
| **Aminoácidos sintéticos** (DL-metionina, L-lisina, L-treonina y otros) | ~0,2–0,8 % | Completan los aminoácidos limitantes de maíz–soja: **metionina, lisina y treonina**, en ese orden (FTE-160) | Medio (precio por kg alto; dependen de importación y del dólar) |
| Enzimas (fitasa, carbohidrasas), anticoccidianos, otros aditivos | < 0,5 % | Digestibilidad, sanidad | Bajo–medio |
| Otros posibles | Variable | Harinas de origen animal, DDGS (burlanda), afrechillos, según costo y restricciones de clientes | — |

**Qué mueve el costo:** **maíz + harina de soja ≈ 85–95 % del peso del alimento** y la mayor parte de su costo; su precio en Argentina está ligado a los precios internacionales, al tipo de cambio, a los derechos de exportación de granos y al **flete** desde la zona de producción. Los componentes menores (aminoácidos, premezcla, fosfatos) pesan poco en tonelaje pero se importan o dolarizan.

### 4.1 Materias primas por escenario (orden de magnitud)

Supuesto ilustrativo: 60 % maíz y 30 % harina de soja (SUP-032). Perfil medio, desempeño medio, 5 d/semana.

| Planta (aves faenadas/día) | Alimento (t/año) | Maíz (t/año) | Harina de soja (t/año) | Otros (t/año) |
|---|---|---|---|---|
| 2.500 | 3.091 | ~1.850 | ~930 | ~310 |
| 5.000 | 6.181 | ~3.710 | ~1.850 | ~620 |
| 10.000 | 12.362 | ~7.420 | ~3.710 | ~1.240 |
| 20.000 | 24.724 | ~14.830 | ~7.420 | ~2.470 |

`[ESTIMACIÓN]`. Para escala: 7.400 t de maíz equivalen a la cosecha de ~900–1.200 ha con rindes de 6–8 t/ha `[ESTIMACIÓN]`. La cercanía a zonas productoras de granos es un criterio de localización (DEC-003).

---

## 5. Agua

### 5.1 Consumo por ave y relación con el alimento

| Parámetro | Valor | Clasificación |
|---|---|---|
| Relación agua/alimento (en peso) en ambiente templado (~21 °C) | **1,6–2,0** (escenarios: **1,8**) | `[PVDP]` FTE-155 |
| Aumento por temperatura | ~**6–7 % por cada °C** por encima de 21 °C; a ~35 °C el consumo puede **duplicarse** | `[PVDP]` FTE-155 |
| Agua de bebida por ave en el ciclo (perfil medio, 4,94 kg de alimento) | **~7,9–9,9 L** a temperatura templada; más en verano | `[ESTIMACIÓN]` |
| Agua de bebida por ave en el ciclo (liviano / pesado) | ~6,1–7,6 L / ~9,9–12,4 L | `[ESTIMACIÓN]` |

**El consumo de agua es un indicador de alerta temprana:** una caída diaria del consumo de agua o un cambio en la relación agua/alimento suele anticipar en 12–24 h un problema sanitario o de equipos `[ESTIMACIÓN]` de práctica general. Por eso se mide con **medidores por galpón** ([`kpis_productivos.md`](kpis_productivos.md)).

### 5.2 Órdenes de magnitud por escenario (agua de bebida)

Agua de bebida = alimento × 1,8 L/kg. Perfil medio, formato favorable / medio / desfavorable.

| Planta (aves faenadas/día) | Días/sem | m³/año | m³/día promedio | m³/día en pico de verano (×2–3, orientativo) |
|---|---|---|---|---|
| 2.500 | 5 | 5.230 / 5.563 / 6.066 | 14 / 15 / 17 | ~30–50 |
| 5.000 | 5 | 10.461 / 11.126 / 12.132 | 29 / 30 / 33 | ~60–100 |
| 10.000 | 5 | 20.922 / 22.252 / 24.264 | 57 / 61 / 66 | ~120–200 |
| 20.000 | 5 | 41.844 / 44.504 / 48.528 | 115 / 122 / 133 | ~240–400 |

`[ESTIMACIÓN]` · ESCENARIO. Sin cambio en la versión 1.1 (el agua depende del alimento anual). Con 6 días de faena, +20 %. En una semana plena el consumo promedio diario es ~4 % mayor que el promedio anual. El factor de pico (×2–3) combina el calor (hasta ×2) y la concentración de galpones en terminación; es orientativo y debe calcularse con el calendario real de alojamientos.

**No incluye:** (a) **agua de los paneles evaporativos** (*cooling*), que en verano puede ser una demanda del mismo orden que la de bebida o mayor en galpones túnel (a cuantificar en `11_agua_efluentes`, DPV-053); (b) nebulización; (c) lavado y desinfección entre lotes; (d) uso doméstico del personal.

### 5.3 Calidad

Parámetros a analizar en cada fuente (perforación, red, reservorio), **antes de elegir un sitio**: pH, sólidos disueltos totales, dureza, cloruros, sulfatos, nitratos/nitritos, hierro, manganeso, **arsénico y flúor** (relevantes en acuíferos de la llanura chaco-pampeana), y microbiología (coliformes totales y fecales: objetivo cero). Los límites de referencia deben tomarse de guías técnicas avícolas y de la normativa aplicable; **no se fijan valores en esta fase** (DPV-053).

### 5.4 Almacenamiento y tratamiento

- **Reserva:** tanques con capacidad para **1–3 días del consumo de pico** `[ESTIMACIÓN]`, para cubrir fallas de bomba o de energía. Sin agua, el ave deja de comer en horas y en calor muere rápidamente.
- **Tratamiento:** cloración (u otro desinfectante) con control del residual en el último bebedero; eventual acidificación, filtrado, ablandamiento o remoción de hierro/arsénico según el análisis.
- **Limpieza de líneas** de bebederos entre lotes (biofilm) y **bebederos tipo niple** (menos derrame, cama más seca) frente a bebederos de campana.
- **Protección de la fuente:** reservorios abiertos atraen aves silvestres (riesgo de influenza aviar); ver [`bioseguridad.md`](bioseguridad.md).
