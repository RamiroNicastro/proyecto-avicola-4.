# Integración upstream: pollitos, alimento y granjas por escala

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B (en paralelo con 14A) · Modelo: [`modelo_upstream.py`](modelo_upstream.py) → [`escenarios_upstream.csv`](escenarios_upstream.csv)

> **Qué es este documento.** El marco transversal del upstream: demanda de pollitos BB por escala, marco *make or buy* (pollito, alimento, granjas), arquitectura conceptual de fases, dependencias al subir de escala y datos de campo a obtener. El detalle vive en: alimento → [`demanda_alimento.md`](demanda_alimento.md), [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md), [`almacenamiento_silos.md`](almacenamiento_silos.md), [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md); incubación → [`../15_incubacion/modelo_incubacion.md`](../15_incubacion/modelo_incubacion.md), [`capacidad_incubacion.md`](../15_incubacion/capacidad_incubacion.md), [`compra_vs_incubacion.md`](../15_incubacion/compra_vs_incubacion.md).
>
> **Qué NO es.** No decide integración total ni parcial (DEC-020, DEC-023, DEC-024 siguen abiertas), no elige fabricante ni proveedor, no contiene precios, CAPEX ni OPEX, y no fija escala (regla 9). Las escalas 2.500 / 5.000 / 10.000 / 20.000 **aves faenadas por día de faena** son los mismos escenarios hipotéticos de `03` y `23`. Toda cifra externa es `[PVDP]` (acceso a documentos originales bloqueado, DPV-009).

---

## 1. Demanda de pollitos BB por escala

Los pollitos salen del modelo de producción primaria v1.1 (`03`), **importado sin recalcular** (test U09). Cadena: **pollitos alojados** −(mortalidad en granja)→ **aves cargadas** −(mortalidad en transporte)→ **aves faenadas**.

### 1.1 Pollitos por semana y por año (5 días de faena/semana; favorable / **medio** / desfavorable)

| Planta (aves faenadas/día) | Aves faenadas/semana plena | **Pollitos alojados/semana plena** | Pollitos/semana (promedio anual) | Pollitos/año | Margen por mortalidad (pollitos/semana plena) | Margen por mortalidad (% sobre faenadas) |
|---|---|---|---|---|---|---|
| 2.500 | 12.500 | 12.912 / **13.197** / 13.655 | 12.382 / **12.655** / 13.094 | 645.621 / **659.874** / 682.762 | 412 / **697** / 1.155 | 3,3 / **5,6** / 9,2 % |
| 5.000 | 25.000 | 25.825 / **26.395** / 27.310 | 24.764 / **25.310** / 26.188 | 1.291.242 / **1.319.749** / 1.365.523 | 825 / **1.395** / 2.310 | 3,3 / **5,6** / 9,2 % |
| 10.000 | 50.000 | 51.650 / **52.790** / 54.621 | 49.527 / **50.620** / 52.376 | 2.582.485 / **2.639.497** / 2.731.047 | 1.650 / **2.790** / 4.621 | 3,3 / **5,6** / 9,2 % |
| 20.000 | 100.000 | 103.299 / **105.580** / 109.242 | 99.054 / **101.241** / 104.752 | 5.164.969 / **5.278.995** / 5.462.093 | 3.299 / **5.580** / 9.242 | 3,3 / **5,6** / 9,2 % |

`[ESTIMACIÓN]` · ESCENARIO. Con 6 días de faena/semana (medio): 15.837 / 31.674 / 63.348 / 126.696 pollitos por semana plena y 0,79 / 1,58 / 3,17 / 6,33 M pollitos/año.

- **Margen por mortalidad** = pollitos alojados − aves faenadas: mortalidad en granja (3 / 5 / 8 %, SUP-026) + en transporte (0,2 / 0,3 / 0,5 %). Con la mortalidad de 7,7–9,5 % del estudio de Entre Ríos (FTE-151 `[PVDP]`, DPV-044) el margen se acercaría al escenario desfavorable.
- **Margen de pedido** (pollitos extra pedidos sobre los alojados: reposición, conteo, mortalidad de llegada) es **otra variable**, no mortalidad: base 0, barrido 1–2 % (SUP-14B-01). No se supone que el proveedor entregue un excedente sin cargo.
- **Base de contrato:** la **semana plena** (ritmo nominal de faena), no el promedio anual: es lo que el proveedor debe poder entregar en una semana sin feriados (SUP-025).

### 1.2 Necesidades de entrega

| Planta (aves faenadas/día) | Alojamientos/semana con granjas de 15.000 / 30.000 / 60.000 plazas | Granjas equivalentes (15 / 30 / 60 mil plazas) | Viajes/semana con camión de 20 / 40 / 80 mil pollitos (barrido, **no capacidad**) |
|---|---|---|---|
| 2.500 | 0,9 / 0,4 / 0,2 | 8,0 / 4,0 / 2,0 | 1 / 1 / 1 |
| 5.000 | 1,8 / 0,9 / 0,4 | 16,1 / 8,0 / 4,0 | 2 / 1 / 1 |
| 10.000 | 3,5 / 1,8 / 0,9 | 32,1 / 16,1 / 8,0 | 3 / 2 / 1 |
| 20.000 | 7,0 / 3,5 / 1,8 | 64,3 / 32,1 / 16,1 | 6 / 3 / 2 |

`[ESTIMACIÓN]` (medio, 5 d). Tamaños de granja = barrido de `13` (PLAZAS_GRANJA); capacidad del camión de pollitos **PENDIENTE** (DPV-047, DPV-084; el CSV deja la fila vacía sin capacidad explícita).

**Lectura:**
- **Cada entrega es un lote de granja completo** (todo dentro–todo fuera): a 2.500 aves/día una granja de 30.000 plazas recibe pollitos cada ~2,3 semanas; el proveedor debe poder entregar ~30.000 pollitos **de una vez**, que es más que la demanda semanal (13.200). **El tamaño de lote, no el volumen semanal, puede ser la restricción de compra a escala chica** (relacionado con DPV-133).
- **Antelación física mínima:** el huevo debe cargarse en la incubadora ≥ 21 días antes de la entrega, más 3–7 días de almacenamiento del huevo: **24–28 días** antes del alojamiento. La antelación comercial real de pedido es PENDIENTE (DPV-047, pregunta D5 del [cuestionario](../15_incubacion/cuestionario_incubadoras.md)).
- **Bioseguridad:** cada alojamiento es una entrada de vehículo y personal a la granja ([`../03_produccion_primaria/bioseguridad.md`](../03_produccion_primaria/bioseguridad.md)).

---

## 2. Marco *make or buy* del upstream

### 2.1 Tres eslabones, tres niveles de integración

| Eslabón | **Comprar** (A) | **Integrar parcialmente** (B) | **Integrar totalmente** (C) |
|---|---|---|---|
| **Pollito BB** | Comprar pollito BB a incubadoras | Comprar **huevo fértil** e incubar en planta propia | Reproductoras propias (y luego genética) → huevo → incubación |
| **Alimento** | Comprar alimento terminado puesto en granja | **Façon**: comprar materias primas y hacer elaborar a un tercero con fórmula propia | **Planta propia** de alimento |
| **Granjas** | Comprar **pollo vivo** a productores independientes | **Integrados**: la empresa aporta pollito, alimento y sanidad; el productor, galpones y trabajo | **Granjas propias** |

**La demanda física es la misma en las tres columnas** (pollitos, toneladas de alimento, plazas y m²). Lo que cambia es **qué capacidad física debe tener la empresa** y **qué parte del riesgo y del capital asume**. El modelo calcula cada opción por separado (test U05).

### 2.2 Capacidad física propia que requiere cada opción (medio, 5 d)

| Planta (aves faenadas/día) | Pollito A | Pollito B (posiciones de incubadora, margen 15 %) | Pollito C (B + reproductoras en postura equivalentes) | Alimento A | Alimento B | Alimento C (t/h, 5 d × 16 h, eficiencia 0,85, margen 15 %) | Granjas A / B | Granjas C (m² de galpón propio) |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 0 | 50.508 | 50.508 + ~3.700 | 0 | 0 | 1,0 | 0 | 9.486 |
| 5.000 | 0 | 101.015 | 101.015 + ~7.300 | 0 | 0 | 2,1 | 0 | 18.971 |
| 10.000 | 0 | 202.030 | 202.030 + ~14.700 | 0 | 0 | 4,2 | 0 | 37.943 |
| 20.000 | 0 | 404.060 | 404.060 + ~29.300 | 0 | 0 | 8,4 | 0 | 75.885 |

`[ESTIMACIÓN]` · ESCENARIO. Reproductoras = ESTIMACIÓN de `03` (~3,6 pollitos por reproductora por semana; DPV-045), **solo como fase futura**; no incluye recría, machos ni reposición. En la opción B de granjas los m² existen igual, pero son **de los integrados**. En alimento B (façon) la empresa compra y mueve materias primas (granos: ~56 / 111 / 223 / 445 t/semana) y paga la elaboración; no tiene planta.

### 2.3 Criterios de comparación (sin costos todavía)

Escala cualitativa: ▲ favorece la opción · ● neutro / depende · ▼ desfavorece. **No hay puntuación ni ganador**: los criterios se ponderarán cuando haya datos de campo y costos (DEC-14B-01).

| Criterio | Pollito A compra | Pollito B huevo fértil | Pollito C reproductoras | Alimento A compra | Alimento B façon | Alimento C planta | Granjas A pollo vivo | Granjas B integrados | Granjas C propias |
|---|---|---|---|---|---|---|---|---|---|
| **Volumen** (escala mínima para que tenga sentido) | ▲ cualquier volumen, si hay oferta | ▼ exige volumen estable para llenar la planta | ▼▼ exige volumen y horizonte largos | ▲ | ● mínimo del fabricante | ▼ escala mínima de planta (DPV-14B-07) | ▲ | ● | ▼ |
| **Calidad** (control de especificación) | ● por contrato | ▲ control de incubación; ▼ no del huevo | ▲ control total | ● fórmula del fabricante | ▲ fórmula propia | ▲ fórmula y materias primas propias | ▼ mínimo | ▲ alto con asistencia | ▲ máximo |
| **Dependencia** de terceros | ▼ incubadoras (oferta concentrada) | ▼ **huevo fértil** (mercado más estrecho que el del pollito) | ▲ solo de la genética (abuelas / pollitas de un día) | ▼ fábricas | ● granos + elaborador | ▲ solo de granos e insumos | ▼▼ spot | ● productores | ▲ |
| **Capital** (CAPEX + capital de trabajo físico) | ▲ nulo | ▼ planta de incubación | ▼▼ planta + granjas de reproductoras + recría | ▲ | ● capital de trabajo en granos | ▼ planta + silos + capital en granos | ▲ | ● capital de trabajo (~415–3.320 t de alimento por ciclo) | ▼▼ galpones |
| **Flexibilidad** (ajustar volumen) | ▲ si hay oferta | ▼ capacidad fija | ▼▼ ciclo de reproductoras ~6–7 meses (`[ESTIMACIÓN]` 03) | ▲ | ● | ▼ capacidad fija | ▲ | ● | ▼ |
| **Bioseguridad** | ● depende del proveedor; riesgo compartido con sus otros clientes | ▲ propia, si se aísla | ▲ máxima (compatible con compartimentos) | ● | ● control de recepción | ▲ trazabilidad de materias primas | ▼ | ● con auditoría | ▲ |
| **Know-how** requerido | ▲ bajo (compras y recepción) | ▼ incubación, sanidad de huevo, vacunación | ▼▼ manejo de reproductoras | ▲ | ● compras de granos, control de calidad | ▼ nutrición, molienda, pellet, calidad, mantenimiento | ▲ | ▼ asistencia técnica | ▼▼ |
| **Riesgo de suministro** | ▼ el cliente chico queda último ante escasez | ● se traslada al huevo fértil | ▲ menor, pero un evento sanitario en reproductoras corta todo | ● | ● | ▲ | ▼▼ | ● | ▲ |
| **Capacidad ociosa** | ▲ ninguna | ▼ si la faena no llena la planta de incubación | ▼▼ | ▲ | ▲ | ▼ planta + reserva + 1 turno ocioso | ▲ | ● | ▼ galpones vacíos |

**Lectura crítica:**
1. **Incubar huevo fértil comprado (B) no elimina la dependencia: la traslada.** Quien vende huevo fértil suele ser una integradora o una incubadora con reproductoras; el mercado de huevo fértil para terceros es, previsiblemente, **más estrecho** que el de pollito (no hay datos: DPV-14B-02). La independencia real del suministro solo llega con reproductoras (C), que es la opción más intensiva en capital, know-how y plazo.
2. **El alimento es el mayor flujo físico y el principal costo** (citado 65–70 %, DPV-019): es el eslabón donde la integración puede mover más el resultado, pero también donde más importan la escala de planta, la compra de granos y la calidad (micotoxinas, pellet). **Façon (B) es la forma de controlar fórmula y materias primas sin CAPEX de planta**, si existe un elaborador dispuesto (DPV-14B-03).
3. **Granjas:** la integración (B) es el modelo dominante del sector y traslada el CAPEX de galpones al productor, pero exige capital de trabajo y asistencia técnica ([`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md)). No se repite aquí.
4. **Las tres decisiones no son independientes en el sentido operativo:** integrar granjas (B) obliga a **proveer** pollito y alimento a los integrados (comprados o propios); comprar pollo vivo (A) hace irrelevantes las decisiones de pollito y alimento. Sí son **independientes en el modelo físico**: la demanda de pollitos y alimento no cambia con la opción.

---

## 3. Arquitectura conceptual por fases

> **No es la secuencia recomendada** (SUP-14B-12). Es una forma ordenada de analizar qué capacidad física aparece en cada etapa si el proyecto avanzara de menos a más integración. Cada pasaje requiere un *gate* con datos ([`../23_plan_expansion/gates_expansion.md`](../23_plan_expansion/gates_expansion.md); el gate V7 ya exige pollitos contratados para la etapa siguiente). Podría saltearse una fase o detenerse en cualquiera.

| Fase | Pollito | Alimento | Granjas | Faena | Capacidad física upstream **propia** que aparece | Condición mínima para considerarla (gate conceptual) |
|---|---|---|---|---|---|---|
| **Fase 0** | Compra | Compra | Terceros (pollo vivo) y/o integrados con insumos comprados | **A façon posible** (DPV-006, DEC-018) | Ninguna (solo recepción de datos, auditoría y, si hay integrados, coordinación de entregas) | Demanda B/A documentada; oferta de pollo vivo, façon o productores |
| **Fase 1** | Compra (≥ 2 proveedores) | Compra o façon | Integrados (+ pollo vivo como amortiguador) | Planta propia | Ninguna física; capital de trabajo en pollito y alimento si hay integrados | Contratos de pollito para la semana plena (gate V7); productores en el radio (DPV-048) |
| **Fase 2** | Compra | Façon o compra | Más integrados; eventualmente granjas propias modelo | Planta propia | Galpones propios (si se decide); silos de granja | Desempeño de campo propio medido (DPV-044); capital |
| **Fase 3** | Huevo fértil + incubación propia **si** el volumen lo justifica | **Planta propia si** el volumen lo justifica | Integrados + propias | Planta propia | Planta de incubación (posiciones, nacedoras, almacén de huevo); planta de alimento (t/h) y silos de granos | Volumen estable ≥ escala mínima de cada planta; huevo fértil disponible (DPV-14B-02); comparación económica (fase posterior) |
| **Fase futura** | Reproductoras / genética **solo si existe justificación** | Planta propia | Integrados + propias | Planta propia | Granjas de recría y reproductoras; habilitaciones específicas | Justificación económica y sanitaria; acceso a genética (abuelas / pollitas de un día) |

**Regla del modelo (test U07):** las reproductoras valen **0** en Fase 0 y Fase 1 y solo aparecen en la fase futura. Ninguna fase intermedia las incluye.

---

## 4. Dependencias al subir de escala

### 4.1 Cómo crece cada variable (medio, 5 d; factor respecto de 2.500 aves/día)

| Planta | Pollitos/semana | Alimento t/año | Plazas de granja | Entregas de alimento/semana (granelero 28 t, escenario) | Silos de maíz (m³) | Aves vivas simultáneas |
|---|---|---|---|---|---|---|
| 2.500 | 1,00 | 1,00 | 1,00 | 3 (1,00) | 1,00 | 1,00 |
| 5.000 | 2,00 | 2,00 | 2,00 | 5 (1,67) | 2,00 | 2,00 |
| 10.000 | 4,00 | 4,00 | 4,00 | 9 (3,00) | 4,00 | 4,00 |
| 20.000 | 8,00 | 8,00 | 8,00 | 18 (6,00) | 8,00 | 8,00 |

### 4.2 Qué cambia en cada dimensión

| Dimensión | Cómo escala | Por qué no es lineal (si no lo es) | Consecuencia |
|---|---|---|---|
| **Pollitos** | Lineal | — | El volumen sí; **la oferta disponible no**: a 20.000 aves/día se necesitan ~105.600 pollitos por semana plena, del orden de una planta de incubación industrial completa (ejemplos citados: 80.000 a 400.000 huevos o pollitos por semana, FTE-14B-004 `[PVDP]`) |
| **Alimento** | Lineal (test U03) | — | De ~62 a ~494 t por semana plena; la escala de una planta propia pasa de ~1 a ~8–19 t/h según turnos |
| **Granjas** | Lineal en plazas y m² | **Granularidad**: granjas enteras de 15–60 mil plazas. A escala chica, pocas granjas grandes concentran el riesgo; a escala grande, coordinar 16–64 granjas | La escala chica tiene problema de **tamaño de lote**; la grande, de **gestión y bioseguridad de una red** |
| **Camiones** | Escalonado | **Redondeo hacia arriba** de viajes enteros: a 2.500 la ocupación media del granelero es baja (3 viajes para 62 t); al crecer, la ocupación mejora (factor 6 para ×8 de volumen) | La logística upstream tiene economías de escala por llenado de camiones |
| **Silos** | Lineal en m³ **para días de stock fijos** (test U04) | Discretos si se fija un volumen de silo (PENDIENTE; no hay silo estándar); el mínimo por segregación (una celda por materia prima y por tipo de alimento: ≥ 5–8) **no** escala | A escala chica, el número mínimo de celdas pesa más que el volumen |
| **Inventario** | Lineal (aves vivas, alimento en ciclo, granos, huevos) | Los días de stock de granos son una **decisión de compra** (cosecha, precio, riesgo), no física | Capital de trabajo físico: 415 → 3.320 t de alimento por ciclo de crianza; granos 15 d: ~119 → ~954 t |

---

## 5. Datos de campo que se necesitan

Organizado por actor y por tipo de dato. Los cuestionarios existentes cubren parte ([incubadoras](../15_incubacion/cuestionario_incubadoras.md), [productores](../03_produccion_primaria/cuestionario_productores.md)); se agregan preguntas para fábricas de alimento, proveedores de grano e integradores. Registro: DPV existentes (amplía) y provisionales `DPV-14B-##` ([`actualizaciones_gestion_14B.md`](actualizaciones_gestion_14B.md)).

| Actor | Precios | Mínimos | Capacidad | Contratos | Plazos | Calidad | Volúmenes | Registro |
|---|---|---|---|---|---|---|---|---|
| **Incubadoras** | Pollito BB (moneda, IVA, puesto dónde, fórmula de ajuste); huevo fértil si lo venden | Pollitos por entrega y por semana | Huevos incubados/semana, nacimientos/semana, % para terceros | Anual / plurianual; exigencias (volumen, anticipo, exclusividad); penalidades | Antelación de pedido; aviso para duplicar volumen; plazo de pago | Fertilidad e incubabilidad reales por edad de reproductoras; peso y uniformidad; mortalidad 7 d garantizada; vacunas; habilitación SENASA | Disponible para un cliente nuevo; estacionalidad; faltantes del último año | DPV-006, DPV-047, DPV-14B-01, DPV-14B-02, DPV-14B-09 |
| **Fábricas de alimento** | Alimento por fase puesto en granja; tarifa de façon | Lote mínimo por fórmula; t/mes mínimas | t/h, turnos, capacidad libre; pellet sí/no | Façon con fórmula y materias primas del cliente; exclusividad; prioridad | Plazo de entrega; programación | Control de micotoxinas, humedad, durabilidad del pellet; registro SENASA; trazabilidad por lote | t/mes que podrían atender; estacionalidad | DPV-050, DPV-14B-03, DPV-14B-07 |
| **Productores** | Pago por ave o kg esperado (como integrado); precio del pollo vivo si venden | Lote mínimo/máximo por granja | Plazas, m², tipo de galpón, silos de granja (t y m³) | Escrito o no; duración; quién aporta qué | Días entre lotes; plazo de pago esperado | Desempeño de 6–12 lotes (FCR, mortalidad); bioseguridad | Disposición a integrarse o ampliar | DPV-044, DPV-048, DPV-049, DPV-133 |
| **Proveedores de grano** (acopios, cooperativas, corredores, molinos de soja) | Maíz, harina de soja, aceite: base de precio, flete, fórmula | Lote mínimo por entrega | Capacidad de abastecer t/semana todo el año; acopio propio | Contratos a término / forward; entrega diferida | Plazos de entrega y de pago | Humedad, micotoxinas, proteína de la harina de soja, impurezas; análisis por lote | t/año disponibles en el radio; estacionalidad (cosecha) | DPV-050, DPV-117, DPV-14B-05 |
| **Integradores** (empresas que ya integran) | — (no se pide precio) | — | Si ofrecen pollito, alimento o crianza a façon a un tercero | Condiciones de un acuerdo de abastecimiento | Plazos de expansión observados (reproductoras, plantas) | Prácticas de compra de pollito y alimento; escala mínima a la que integraron incubación y alimento | Volumen a partir del cual consideran rentable una planta de alimento o incubación (dato cualitativo valioso) | DPV-14B-08 |
| **SENASA / organismos** | — | — | — | — | Plazos de habilitación | Requisitos para planta de incubación, fábrica de alimentos (registro de productos para alimentación animal, medicados) y granjas de reproductoras | — | DPV-14B-06 (`[PVDP]` hasta leer el original) |

**Evidencia fuerte:** condiciones escritas, con fecha, de al menos dos actores independientes por eslabón. **Débil:** "siempre hay pollito / alimento", cifras de un único actor, valores de prensa.

---

## 6. Calidad y límites

- **Fortalezas:** cadena física cerrada y probada (11 tests; conservación pollitos/huevos con error ≤ 10⁻⁹); importa `03` sin recalcular; opciones independientes; faltantes PENDIENTES (240 filas del CSV) en lugar de rellenados; sin economía.
- **Debilidades:** parámetros de incubación, planta y silos son supuestos (SUP-14B-02 a SUP-14B-13); ninguna cifra externa leída en original; sin datos argentinos de oferta de pollito, huevo fértil, alimento ni façon; sin costos (por diseño de la fase).
- **Calidad:** MEDIA como marco y modelo físico; BAJA como evidencia para decidir integrar.
