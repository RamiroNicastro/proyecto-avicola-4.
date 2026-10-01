# Integración upstream: pollitos, alimento y granjas por escala

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de sincronización productiva e inventarios) · Sesión 14B (en paralelo con 14A) · Modelo: [`modelo_upstream.py`](modelo_upstream.py) → [`escenarios_upstream.csv`](escenarios_upstream.csv)

> **Qué es este documento.** El marco transversal del upstream: demanda de pollitos BB por escala, marco *make or buy* (pollito, alimento, granjas), arquitecturas de referencia, sincronización nacimiento–colocación–faena, dependencias al subir de escala y datos de campo a obtener. El detalle vive en: alimento → [`demanda_alimento.md`](demanda_alimento.md), [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md), [`almacenamiento_silos.md`](almacenamiento_silos.md), [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md); incubación → [`../15_incubacion/modelo_incubacion.md`](../15_incubacion/modelo_incubacion.md), [`capacidad_incubacion.md`](../15_incubacion/capacidad_incubacion.md), [`compra_vs_incubacion.md`](../15_incubacion/compra_vs_incubacion.md).
>
> **Qué NO es.** No decide integración total ni parcial (DEC-020, DEC-023, DEC-024 siguen abiertas), no elige fabricante, proveedor ni cadencia, no contiene precios, CAPEX ni OPEX, y no fija escala (regla 9). Las escalas 2.500 / 5.000 / 10.000 / 20.000 **aves faenadas por día de faena** son los mismos escenarios hipotéticos de `03` y `23`. Toda cifra externa es `[PVDP]` (DPV-009).
>
> **Cambios v1.1:** recepción del huevo, carga y nacimiento como eventos distintos; setter y hatcher separados con cadencia; demanda media ≠ lote de nacimiento; granja ≠ galpón y chequeo de sincronización; dependencia de huevo fértil reformulada sin afirmar concentración; opciones como escenarios de comparación (sin "caso base"); fases como arquitecturas de referencia sin orden obligatorio; datos de campo ampliados.

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

`[ESTIMACIÓN]` · ESCENARIO. Con 6 días de faena/semana (medio): 15.837 / 31.674 / 63.348 / 126.696 pollitos por semana plena.

- **Margen por mortalidad** = pollitos alojados − aves faenadas (granja 3 / 5 / 8 % + transporte 0,2 / 0,3 / 0,5 %, SUP-026). Con la mortalidad de 7,7–9,5 % del estudio de Entre Ríos (FTE-151 `[PVDP]`, DPV-044) se acercaría al desfavorable.
- **Margen de pedido** (pollitos extra sobre los alojados) es otra variable: 0 en el valor de parámetro, barrido 1–2 % (SUP-14B-01).
- Estas cifras son **demanda media semanal**: no es el tamaño de cada entrega ni de cada nacimiento (§1.2 y §4).

### 1.2 Tiempos y entregas

- **Incubación ≠ lead time.** La incubación (carga → nacimiento) es de **21 días** en el modelo (18 setter + 3 hatcher, `[SUPUESTO]` SUP-14B-04). El **lead time recepción del huevo → pollito entregado** suma almacenamiento previo (3–7 d, supuesto), selección, vacunación, expedición y viaje (horas PENDIENTES): **≥ 24–28 días**. Detalle: [`../15_incubacion/modelo_incubacion.md` §2.1](../15_incubacion/modelo_incubacion.md). La antelación comercial de pedido es PENDIENTE (DPV-047).
- **Entregas:** el número y tamaño de entregas dependen del **lote de nacimiento** del proveedor (o propio) y de la **unidad de colocación** (galpón o granja), no de la demanda media semanal. Viajes de camión de pollitos con 20 / 40 / 80 mil pollitos por camión (barrido SUP-096, **no capacidad**): 1 / 1 / 1 (2.500), 2 / 1 / 1 (5.000), 3 / 2 / 1 (10.000), 6 / 3 / 2 (20.000) por semana; sin capacidad validada el CSV deja la fila PENDIENTE (DPV-047, DPV-084).
- **Bioseguridad:** cada colocación es una entrada de vehículo y personal ([`../03_produccion_primaria/bioseguridad.md`](../03_produccion_primaria/bioseguridad.md)).

---

## 2. Marco *make or buy* del upstream

### 2.1 Tres eslabones, tres niveles de integración — todos **escenarios de comparación**

| Eslabón | **Comprar** (A) — benchmark de comparación | **Integrar parcialmente** (B) | **Integrar totalmente** (C) |
|---|---|---|---|
| **Pollito BB** | Comprar pollito BB a incubadoras | Comprar **huevo fértil** e incubar en planta propia | Reproductoras propias (y luego genética) → huevo → incubación |
| **Alimento** | Comprar alimento terminado puesto en granja | **Façon**: un tercero elabora la fórmula de la empresa (las materias primas pueden ser de la empresa o del elaborador) | **Planta propia** de alimento |
| **Granjas** | Comprar **pollo vivo** a productores independientes | **Integrados**: la empresa aporta pollito, alimento y sanidad; el productor, galpones y trabajo | **Granjas propias** |

**Benchmark de comparación** = la opción contra la que se miden las diferencias de las demás (capacidad, capital, riesgo). **No es un caso base ni una preferencia**: el modelo marca todas las opciones con el mismo estatus ("escenario de comparación", test U20) para que CAPEX/OPEX pueda compararlas todas sin favorecer ninguna por diseño.

**La demanda física es la misma en las tres columnas** (pollitos, toneladas de alimento, plazas y m²). Lo que cambia es **qué capacidad física debe tener la empresa** y **qué parte del riesgo y del capital asume** (test U05).

### 2.2 Capacidad física propia que requiere cada opción (medio, 5 d)

| Planta | Pollito A | Pollito B: setter / hatcher (posiciones de diseño, 2 nacimientos/semana ilustrativos, margen 15 %) | Pollito C | Alimento A | Alimento B | Alimento C (t/h, 5 d × 16 h, eficiencia 0,85, margen 15 %) | Granjas A / B | Granjas C (m² propios) |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 0 | 55.824 / 18.515 | B + ~3.700 reproductoras | 0 | 0 | 1,0 | 0 | 9.486 |
| 5.000 | 0 | 111.648 / 37.030 | B + ~7.300 | 0 | 0 | 2,1 | 0 | 18.971 |
| 10.000 | 0 | 223.296 / 74.060 | B + ~14.700 | 0 | 0 | 4,2 | 0 | 37.943 |
| 20.000 | 0 | 446.593 / 148.120 | B + ~29.300 | 0 | 0 | 8,4 | 0 | 75.885 |

`[ESTIMACIÓN]` · ESCENARIO. Setter y hatcher **no se suman** como capacidad (etapas distintas); otras cadencias en [`../15_incubacion/capacidad_incubacion.md` §3](../15_incubacion/capacidad_incubacion.md). Reproductoras = ESTIMACIÓN de `03` (DPV-045), solo arquitectura futura. Alimento C: el resultado depende de la cadencia de fabricación ([`planta_alimento_conceptual.md` §2](planta_alimento_conceptual.md)). En granjas B los m² existen igual, pero son de los integrados.

### 2.3 Criterios de comparación (sin costos todavía)

Escala cualitativa: ▲ favorece la opción · ● neutro / depende · ▼ desfavorece. **Sin puntuación ni ganador** (DEC-14B-01).

| Criterio | Pollito A compra | Pollito B huevo fértil | Pollito C reproductoras | Alimento A compra | Alimento B façon | Alimento C planta | Granjas A pollo vivo | Granjas B integrados | Granjas C propias |
|---|---|---|---|---|---|---|---|---|---|
| **Volumen** | ▲ cualquier volumen, si hay oferta | ▼ exige volumen estable para usar la planta | ▼▼ volumen y horizonte largos | ▲ | ● mínimo del elaborador | ● escala y cadencia de fabricación (DPV-14B-07) | ▲ | ● | ▼ |
| **Calidad** | ● por contrato | ▲ control de incubación; ▼ no del huevo | ▲ control total | ● fórmula del fabricante | ▲ fórmula propia | ▲ fórmula y materias primas propias | ▼ mínimo | ▲ alto con asistencia | ▲ máximo |
| **Dependencia** de terceros | ▼ proveedores de pollito (concentración: DPV-047) | ● **sustituye** la dependencia por proveedores de huevo fértil (concentración: DPV-14B-02) | ▲ solo de la genética | ▼ fábricas | ● granos + elaborador | ▲ solo de granos e insumos | ▼▼ spot | ● productores | ▲ |
| **Capital** | ▲ nulo | ▼ planta de incubación | ▼▼ planta + reproductoras + recría | ▲ | ● capital de trabajo en granos si los compra la empresa | ▼ planta + silos + granos | ▲ | ● capital de trabajo (~415–3.320 t de alimento por ciclo) | ▼▼ galpones |
| **Flexibilidad** | ▲ si hay oferta | ▼ capacidad fija | ▼▼ ciclo de reproductoras ~6–7 meses (`[ESTIMACIÓN]` 03) | ▲ | ● | ▼ capacidad fija | ▲ | ● | ▼ |
| **Bioseguridad** | ● depende del proveedor | ▲ propia, si se aísla | ▲ máxima | ● | ● control de recepción | ▲ trazabilidad de materias primas | ▼ | ● con auditoría | ▲ |
| **Know-how** | ▲ bajo | ▼ incubación, sanidad del huevo, vacunación | ▼▼ manejo de reproductoras | ▲ | ● granos, calidad, nutrición | ▼ nutrición, molienda, pellet, mantenimiento | ▲ | ▼ asistencia técnica | ▼▼ |
| **Riesgo de suministro** | ▼ el cliente chico puede quedar último ante escasez | ● se traslada al huevo fértil | ▲ menor, pero un evento sanitario corta todo | ● | ● | ▲ | ▼▼ | ● | ▲ |
| **Capacidad ociosa** | ▲ ninguna | ▼ hatcher 50–75 % y setter 79 % de utilización media de diseño | ▼▼ | ▲ | ▲ | ● depende de la cadencia de fabricación; podría servir a terceros (no se supone) | ▲ | ● | ▼ galpones vacíos |

**Lectura crítica:**
1. **Incubar huevo fértil comprado (B) sustituye la dependencia de proveedores de pollito por dependencia de proveedores de huevo fértil; la concentración y disponibilidad real de esa oferta es un dato por validar (DPV-14B-02).** No hay evidencia de que haya más o menos vendedores de huevo que de pollito. La independencia de suministro solo llega con reproductoras (C).
2. **El alimento es el mayor flujo físico y el principal costo citado** (65–70 %, DPV-019): donde la integración puede mover más el resultado, y donde más importan la compra de granos y la calidad. **Façon** permite controlar la fórmula sin CAPEX de planta, si existe un elaborador dispuesto (DPV-14B-03).
3. **Granjas:** ver [`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md).
4. **Acoplamiento operativo:** integrar granjas (B) obliga a proveer pollito y alimento a los integrados; comprar pollo vivo (A) vuelve irrelevantes las otras dos decisiones. En el modelo físico, en cambio, la demanda no cambia con la opción.

---

## 3. Arquitecturas de madurez de referencia

> **Referencias, no recorrido** (SUP-14B-12). Describen combinaciones crecientes de integración para ordenar el análisis. **La empresa no necesita recorrerlas en ese orden**: si existieran demanda, capital y ventaja económica suficientes (a demostrar en la fase económica), una función podría integrarse antes, o podría saltearse una arquitectura o detenerse en cualquiera. El modelo marca todas con `orden_obligatorio = False` (test U20).

| Arquitectura de referencia | Pollito | Alimento | Granjas | Faena | Capacidad física upstream propia | Condiciones para evaluarla (conceptual) |
|---|---|---|---|---|---|---|
| **0** | Compra | Compra | Terceros (pollo vivo) y/o integrados con insumos comprados | **A façon posible** (DPV-006, DEC-018) | Ninguna | Demanda B/A documentada; oferta de pollo vivo, façon o productores |
| **1** | Compra (≥ 2 proveedores) | Compra o façon | Integrados (+ pollo vivo) | Planta propia | Ninguna física; capital de trabajo si hay integrados | Pollito contratado para la semana plena (gate V7 de `23`); productores (DPV-048) |
| **2** | Compra | Façon o compra | Más integrados; eventualmente granjas propias | Planta propia | Galpones propios (si se evalúan) | Desempeño de campo medido (DPV-044); capital |
| **3** | Huevo fértil + incubación | Planta propia | Integrados + propias | Planta propia | Setter, hatcher, almacén de huevo; planta de alimento y silos | Volumen estable; oferta de huevo (DPV-14B-02); cadencia compatible (§4); comparación económica |
| **Futura** | Reproductoras / genética **solo con justificación** | Planta propia | Integrados + propias | Planta propia | Recría y reproductoras | Justificación económica y sanitaria; acceso a genética |

**Regla del modelo (test U07):** reproductoras = 0 en las arquitecturas 0 y 1.

---

## 4. Sincronización upstream: huevo → nacimiento → colocación → engorde → retiro → faena

### 4.1 Cadena temporal (día 0 = carga en el setter; perfil medio)

| Evento | Día | Evidencia |
|---|---|---|
| Recepción del huevo fértil | −3 / −5 / −7 | `[SUPUESTO]` almacenamiento previo |
| Carga (setting) | 0 | — |
| Transferencia setter → hatcher | 18 | `[SUPUESTO]` SUP-14B-04 (`[PVDP]` FTE-14B-002) |
| Nacimiento | 21 | `[SUPUESTO]` |
| Selección, vacunación, expedición, llegada a granja = **colocación** | 21 + horas | Horas **PENDIENTES** (DPV-14B-09) |
| Retiro de aves (fin del engorde) | ≥ 68 | 47 d de edad de faena (03, `[ESTIMACIÓN]`) |
| Faena | ≥ 68,4 | + 10 h de ventana prefaena (13, escenario) |
| Misma unidad recibe su siguiente colocación | colocación + 62 | 47 d de engorde + 15 d entre lotes (03, SUP-029) |

### 4.2 Granja ≠ galpón

- **Granja:** establecimiento con uno o varios galpones (unidades).
- **Galpón / lote:** la unidad que, según el manejo y la bioseguridad, suele entrar y salir junta (todo dentro–todo fuera). Algunas operaciones llenan la granja completa; otras, galpón por galpón.

El modelo trata la **unidad de colocación** como variable explícita (`unidad = "galpon"` o `"granja"`, test U16). Plazas por galpón = pollitos alojados por m² de `03` (~12,7 en el escenario medio) × m² de galpón (SUP-031: 1.200 / 1.800 / 2.400 m²) = **~15.200 / ~22.900 / ~30.500 plazas** (equivalencias derivadas, no galpones reales). Plazas por granja: barrido de `13` (15 / 30 / 60 mil). **Galpones por granja reales: PENDIENTE** (DPV-048); el modelo solo informa la equivalencia (p. ej. una granja de 30.000 plazas ≈ 1,3 galpones equivalentes de 1.800 m²).

### 4.3 Indicadores por unidad de colocación (medio, 5 d)

| Planta | Unidad de colocación | Plazas | Colocaciones/semana | Intervalo entre colocaciones del sistema (d) | Lotes simultáneos en crianza | Unidades requeridas | Días de faena para cosechar una unidad | Nacimientos por colocación con 1 / 2 / 3 / 5 nacimientos/semana (incubación propia) |
|---|---|---|---|---|---|---|---|---|
| 2.500 | Galpón 1.200 m² | 15.245 | 0,87 | 8,1 | 5,8 | 7,9 | 5,8 | 1,2 / 2,3 / 3,5 / 5,8 |
| 2.500 | Galpón 1.800 m² | 22.868 | 0,58 | 12,1 | 3,9 | 5,3 | 8,7 | 1,7 / 3,5 / 5,2 / 8,7 |
| 2.500 | Galpón 2.400 m² | 30.490 | 0,43 | 16,2 | 2,9 | 4,0 | 11,6 | 2,3 / 4,6 / 6,9 / 11,6 |
| 2.500 | Granja 30.000 plazas | 30.000 | 0,44 | 15,9 | 3,0 | 4,0 | 11,4 | 2,3 / 4,5 / 6,8 / 11,4 |
| 5.000 | Galpón 1.200 m² | 15.245 | 1,73 | 4,0 | 11,6 | 15,8 | 2,9 | 0,6 / 1,2 / 1,7 / 2,9 |
| 5.000 | Galpón 1.800 m² | 22.868 | 1,15 | 6,1 | 7,8 | 10,5 | 4,3 | 0,9 / 1,7 / 2,6 / 4,3 |
| 5.000 | Granja 30.000 plazas | 30.000 | 0,88 | 8,0 | 5,9 | 8,0 | 5,7 | 1,1 / 2,3 / 3,4 / 5,7 |
| 10.000 | Galpón 1.200 m² | 15.245 | 3,46 | 2,0 | 23,3 | 31,6 | 1,4 | 0,3 / 0,6 / 0,9 / 1,4 |
| 10.000 | Galpón 1.800 m² | 22.868 | 2,31 | 3,0 | 15,5 | 21,1 | 2,2 | 0,4 / 0,9 / 1,3 / 2,2 |
| 10.000 | Granja 30.000 plazas | 30.000 | 1,76 | 4,0 | 11,8 | 16,1 | 2,8 | 0,6 / 1,1 / 1,7 / 2,8 |
| 20.000 | Galpón 1.800 m² | 22.868 | 4,62 | 1,5 | 31,0 | 42,2 | 1,1 | 0,2 / 0,4 / 0,6 / 1,1 |
| 20.000 | Granja 30.000 plazas | 30.000 | 3,52 | 2,0 | 23,6 | 32,1 | 1,4 | 0,3 / 0,6 / 0,9 / 1,4 |
| 20.000 | Granja 60.000 plazas | 60.000 | 1,76 | 4,0 | 11,8 | 16,1 | 2,8 | 0,6 / 1,1 / 1,7 / 2,8 |

`[ESTIMACIÓN]` · ESCENARIO. Resto de combinaciones (granjas de 15 y 60 mil, galpón de 2.400 m² en todas las escalas): CSV, bloque `3_sincronizacion`. Identidad verificada (test U16): unidades requeridas = colocaciones/semana × 62 d / 7 / 0,97 (disponibilidad de `03`), igual a la capacidad de alojamiento de `03` / plazas por unidad.

### 4.4 Chequeo conceptual (no optimiza)

El modelo marca **REQUIERE VALIDACIÓN** cuando:

1. **Llenado multi-nacimiento:** una unidad de colocación necesita más de un nacimiento (nacimientos por colocación > 1) → pollitos de edades distintas en el mismo lote (dispersión = días entre nacimientos). La **tolerancia de edad admisible es PENDIENTE** (no se inventa). Con pollito comprado, el lote de nacimiento lo fija el proveedor (PENDIENTE).
2. **Cosecha prolongada:** cosechar una unidad lleva más de **2 días de faena** (referencia de `03`/`13`: una granja "se vacía en 1–2 noches", `[ESTIMACIÓN]`) → dispersión de edad y peso a faena, o necesidad de cosecha escalonada (raleo) o de unidades más chicas.

Resultados (medio, unidad = galpón, 2 nacimientos/semana ilustrativos):

| Planta | Galpón 1.200 m² | Galpón 1.800 m² | Galpón 2.400 m² |
|---|---|---|---|
| 2.500 | Requiere validación (multi-nacimiento + cosecha) | Ídem | Ídem |
| 5.000 | Ídem | Ídem | Ídem |
| 10.000 | Sin conflicto detectado | Requiere validación (cosecha 2,2 d) | Requiere validación (multi-nacimiento + cosecha) |
| 20.000 | Sin conflicto detectado | Sin conflicto detectado | Sin conflicto detectado |

**Lectura (reformulada en v1.1):** existe un **posible problema de sincronización entre tamaño de lote, capacidad de galpones y cadencia de nacimientos y de faena** que debe validarse con la arquitectura real de las granjas. Es más visible a escalas chicas: a 2.500 aves/día la planta cosecha ~2.500 aves por día, de modo que una unidad de 15.000–30.000 aves lleva ~6–12 días de faena. Esto **no demuestra incompatibilidad**: puede resolverse (o no) con galpones más chicos, cosecha escalonada, cadencias distintas, tolerancias de edad o pollito de un proveedor con lotes grandes; nada de eso se decide aquí (DPV-048, DPV-133, DPV-14B-10).

---

## 5. Dependencias al subir de escala

### 5.1 Factor respecto de 2.500 aves/día (medio, 5 d)

| Planta | Pollitos/semana | Alimento t/año | Plazas de granja | Entregas de alimento/semana (granelero 28 t, escenario) | Silos de maíz (m³) | Aves vivas simultáneas | Días de faena por galpón de 1.800 m² |
|---|---|---|---|---|---|---|---|
| 2.500 | 1,00 | 1,00 | 1,00 | 3 (1,00) | 1,00 | 1,00 | 8,7 |
| 5.000 | 2,00 | 2,00 | 2,00 | 5 (1,67) | 2,00 | 2,00 | 4,3 |
| 10.000 | 4,00 | 4,00 | 4,00 | 9 (3,00) | 4,00 | 4,00 | 2,2 |
| 20.000 | 8,00 | 8,00 | 8,00 | 18 (6,00) | 8,00 | 8,00 | 1,1 |

### 5.2 Qué cambia en cada dimensión

| Dimensión | Cómo escala | Por qué no es lineal (si no lo es) | Consecuencia |
|---|---|---|---|
| **Pollitos** | Lineal en la media | El **lote de nacimiento** depende de la cadencia, no solo de la escala | A escala chica, lotes chicos frente a la unidad de colocación (§4) |
| **Incubación** | Setter ~lineal | Hatcher depende de la cadencia (1–2 nacimientos/semana: +50 % frente a 3) | La cadencia es una variable de diseño, no un detalle |
| **Alimento** | Lineal (test U03) | — | De ~62 a ~494 t por semana plena |
| **Granjas** | Lineal en plazas y m² | **Granularidad**: galpones y granjas enteros | Chica: pocas unidades grandes frente a la faena diaria; grande: gestión de 16–64 unidades |
| **Camiones** | Escalonado | Redondeo de viajes enteros | Mejor ocupación al crecer |
| **Silos** | Lineal en m³ para días fijos (test U04) | Celdas mínimas por segregación (5–8) no escalan | A escala chica pesa el número de celdas |
| **Inventario** | Lineal por categoría | Días de stock = decisión de compra | Ver [`almacenamiento_silos.md` §5](almacenamiento_silos.md) |
| **Faena** | Lineal | Días de faena por unidad ∝ plazas / escala | Cosecha prolongada a escala chica (§4.4) |

---

## 6. Datos de campo que se necesitan

Cuestionarios existentes: [incubadoras](../15_incubacion/cuestionario_incubadoras.md), [productores](../03_produccion_primaria/cuestionario_productores.md). **No se crea un cuestionario nuevo** (para no duplicar el plan de campo): las preguntas se proponen para la reconciliación en [`actualizaciones_gestion_14B.md` §6](actualizaciones_gestion_14B.md).

### 6.1 Incubadoras (ampliado en v1.1)

| Dato | Para qué | Registro |
|---|---|---|
| **Días de nacimiento** por semana y calendario | Cadencia; lote de nacimiento; llenado de galpones | DPV-14B-10 |
| **Tamaño mínimo de lote** (por entrega y por nacimiento) | Sincronización con la unidad de colocación | DPV-047, DPV-14B-10 |
| **Mínimo contractual** semanal / mensual | Compatibilidad con la rampa y las semanas con feriados | DPV-047 |
| **Flexibilidad de programación** (cambios de volumen y fecha, preaviso) | Ajuste a la faena | DPV-047 |
| **Uniformidad** (peso, CV) y edad de reproductoras de origen | Calidad del lote | DPV-047, DPV-14B-01 |
| **Ventana de entrega** (horario, horas nacimiento → granja) | Lead time; bienestar | DPV-14B-09 |
| **Disponibilidad estacional** y faltantes del último año | Riesgo de suministro | DPV-047 |
| **Capacidad disponible futura** (planes de ampliación, preaviso) | Crecimiento | DPV-045, DPV-047 |
| Precio, ajuste, plazo de pago; mortalidad 7 d garantizada; vacunas; habilitación SENASA | Ya en el cuestionario (bloques C–E) | DPV-006, DPV-047 |
| Huevo fértil para terceros: volumen, calidad, contrato | Opción B | DPV-14B-02 |

### 6.2 Fábricas de alimento y façon (ampliado en v1.1)

| Dato | Para qué | Registro |
|---|---|---|
| **Quién compra las materias primas** (empresa o elaborador) y bajo qué contrato | Propiedad del inventario y capital de trabajo | DPV-14B-03 |
| **Quién mantiene el inventario** (granos, micros, alimento terminado), dónde y cuántos días | Stock propio vs en tercero | DPV-14B-03, DPV-14B-04 |
| **Mínimo de lote** por fórmula | Frecuencia de fabricación; n.º de fórmulas | DPV-14B-03 |
| **Fórmula / servicio nutricional** (quién formula; confidencialidad) | Control de calidad | DPV-14B-03, DEC-14B-03 |
| **Mermas** de proceso y de almacenamiento | Balance de materias primas | DPV-14B-07 |
| **Almacenamiento** disponible para el cliente (silos, celdas) | Si la empresa necesita silos propios | DPV-14B-04 |
| **Frecuencia de producción** (días por semana, turnos) | Inventario de alimento terminado | DPV-14B-07 |
| **Capacidad disponible** (t/mes, pellet sí/no) | Viabilidad de A y B | DPV-050, DPV-14B-03 |
| Precio del alimento y tarifa de façon; registro SENASA | Fase económica; habilitación | DPV-050, DPV-14B-06 |

### 6.3 Otros actores

| Actor | Precios | Mínimos | Capacidad | Contratos | Plazos | Calidad | Volúmenes | Registro |
|---|---|---|---|---|---|---|---|---|
| **Productores** | Pago esperado como integrado; pollo vivo si venden | Lote mínimo/máximo | **Galpones por granja, plazas por galpón**, tipo de galpón, silos de granja | Escrito o no; quién aporta qué | Días entre lotes; **¿llenan por galpón o por granja?; ¿cosecha en cuántas noches?** | Desempeño de 6–12 lotes; bioseguridad | Disposición a integrarse | DPV-044, DPV-048, DPV-133 |
| **Proveedores de grano** | Maíz, harina de soja, aceite: base, flete | Lote por entrega | t/semana todo el año | A término / forward | Entrega y pago | Humedad, micotoxinas, proteína | t/año en el radio; cosecha | DPV-050, DPV-117, DPV-14B-05 |
| **Integradores** | — | — | Si ofrecen pollito, alimento o crianza a un tercero | Condiciones | Expansión observada | Prácticas de sincronización incubadora–granja–faena | Volumen al que integraron alimento e incubación | DPV-14B-08 |
| **SENASA** | — | — | — | — | Habilitación | Incubación, fábrica de alimentos, reproductoras | — | DPV-14B-06 |

**Evidencia fuerte:** condiciones escritas, con fecha, de al menos dos actores independientes por eslabón. **Débil:** "siempre hay", cifras de un único actor, prensa.

---

## 7. Calidad y límites

- **Fortalezas:** cadena física y temporal cerrada (21 tests; conservación de pollitos/huevos y conservación temporal setter/hatcher simulada); importa `03` sin recalcular; opciones independientes con el mismo estatus; sincronización explícita con granja ≠ galpón; inventarios por categoría y propiedad; faltantes PENDIENTES en lugar de rellenados; sin economía.
- **Debilidades:** parámetros de incubación, cadencia, planta y silos son supuestos (SUP-14B-02 a SUP-14B-14); arquitectura real de granjas desconocida; ninguna cifra externa leída en original; sin costos.
- **Calidad:** MEDIA como marco y modelo físico; BAJA como evidencia para decidir integrar.
