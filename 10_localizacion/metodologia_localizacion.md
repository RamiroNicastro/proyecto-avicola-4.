# Metodología de localización industrial (módulo 12A)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · **Sesión:** 12A (en paralelo con 12B Logística y 12C Layout/Obra civil) · **Estado:** modelo preliminar, **sin ubicación elegida** (DEC-003 abierta)

> **Pregunta de este módulo:** ¿qué zonas tienen mejores condiciones para desarrollar progresivamente producción primaria, faena, frío, distribución y eventualmente exportación?
> **No es todavía:** ¿dónde compramos un terreno? Ningún documento de esta carpeta recomienda una provincia, un corredor, un municipio ni un lote.

Documentos del módulo: criterios en [`criterios_localizacion.md`](criterios_localizacion.md) · regiones en [`regiones_preliminares.md`](regiones_preliminares.md) · escenarios y trade-offs en [`escenarios_localizacion.md`](escenarios_localizacion.md) · terreno en [`terreno_ideal.md`](terreno_ideal.md) · guía en [`guia_ramiro.md`](guia_ramiro.md) · resultados en [`conclusiones_localizacion.md`](conclusiones_localizacion.md) · registros propuestos en [`actualizaciones_gestion_12A.md`](actualizaciones_gestion_12A.md).

---

## 1. Niveles de análisis

La localización se decide **de arriba hacia abajo**, y cada nivel usa información distinta. Mezclar niveles es el error más común (p. ej., descartar una provincia por el precio de un lote, o elegir un lote sin saber si la zona tiene productores).

| Nivel | Pregunta | Información típica | Estado en 12A |
|---|---|---|---|
| **País** | ¿Argentina? | Dado (SUP-001) | Cerrado |
| **Provincia** | ¿Qué marco normativo, fiscal, ambiental y productivo? | Faena por provincia, autoridad hídrica y ambiental, régimen de habilitación, distancia gruesa a AMBA | **Trabajado** (con datos `[PVDP]` y huecos) |
| **Corredor / región** | ¿Qué franja de territorio sobre qué rutas, con qué ecosistema? | Granjas, incubadoras y alimento en radio; tiempos a mercado y puerto; presión urbana; acuíferos; redes de energía y gas | **Trabajado** (13 corredores definidos; datos casi todos pendientes) |
| **Municipio / partido / departamento** | ¿Qué municipio admite la actividad y con qué reglas? | Zonificación, parques industriales, tasas, postura municipal, riesgo hídrico local | **No iniciado** (se habilita con lista corta, DEC-12A-06) |
| **Terreno** | ¿Qué lote concreto? | Ficha de relevamiento ([`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md)), factibilidades escritas, vecinos, drenaje | **No iniciado** (ola O8 del plan de campo) |

**Esta sesión llega hasta provincia + corredor.** Un corredor no es un sitio: es un ámbito de búsqueda definido por un eje vial y un ecosistema (SUP-12A-01). Su "centro de referencia" (p. ej., Pilar, Gualeguaychú, Rosario) se usa solo para medir distancias de orden de magnitud y **no** implica ubicar la planta en esa ciudad.

## 2. Embudo de decisión (etapas)

```
E0 UNIVERSO           5 provincias pedidas (BA, ER, SF, Cba, Chaco) → 13 corredores; otras provincias solo con evidencia
   │
E1 CRIBADO REGIONAL   Matriz multicriterio por corredor (este módulo). Resultado: corredores "habilitados para investigar",
   │                  nunca "elegidos". Ranking solo si la cobertura de datos lo permite (§5).
E2 LISTA CORTA        Después de los hitos H-A (capital y ancla) y H-B (rango de escala y abastecimiento) del plan de campo:
   │                  2–4 corredores con relevamiento dirigido (DEC-12A-06).
E3 MUNICIPIOS         Plantilla jurisdiccional de 14 temas (16_normativa_senasa/habilitacion_planta.md §5) por municipio.
   │
E4 TERRENOS           Ficha de terreno + filtros eliminatorios (criterios_localizacion.md §4) + factibilidades escritas.
   │                  Regla de la ruta crítica: no comprometer un terreno sin uso de suelo, agua y vuelco por escrito.
E5 DECISIÓN           Junto con escala (DEC-001), abastecimiento (DEC-020), CAPEX/OPEX y modelo financiero. Fuera de Fase 0.
```

Las etapas E2–E5 dependen de datos que hoy no existen: la demanda documentada es ≈ 0 ([`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md)) y no hay escala elegida ([`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md)). **La localización no puede adelantarse a la escala y al modelo de abastecimiento**: una planta de 2.500 aves/día abastecida por compra de pollo vivo y una de 20.000 aves/día con integración propia no buscan el mismo corredor.

## 3. Qué es la matriz multicriterio y cómo está construida

Una matriz multicriterio (en inglés *MCDA*, análisis de decisión multicriterio) descompone la pregunta "¿qué zona es mejor?" en criterios medibles, asigna a cada uno un peso explícito y combina los resultados. Su valor no es dar "la respuesta", sino **hacer visibles los supuestos**: qué se midió, con qué evidencia y cuánto importa cada cosa para quien decide.

**Componentes:**

1. **Matriz de datos** — [`matriz_localizacion.csv`](matriz_localizacion.csv): formato largo, una fila por región × subcriterio (13 × 43 = 559 filas). Columnas: `REGION`, `PROVINCIA`, `CORREDOR`, `CRITERIO` (grupo), `SUBCRITERIO`, `NOMBRE_SUBCRITERIO`, `UNIDAD`, `SENTIDO`, `NIVEL_DATO`, `VALOR`, `TIPO_EVIDENCIA`, `FUENTE`, `ESTADO`, `NORMALIZACION`, `PESO`, `PUNTAJE`, `OBSERVACIONES`. `PESO` y `PUNTAJE` quedan **vacíos** en la matriz: los pesos viven en un único archivo (regla 13) y los puntajes los calcula el modelo.
2. **Perfiles de ponderación** — [`pesos_localizacion.csv`](pesos_localizacion.csv): peso por grupo de criterio (12 grupos, suma 100) para los perfiles A MERCADO, B PRODUCCIÓN, C EQUILIBRADO y D EXPORTADOR. **Ninguno es el correcto** (SUP-12A-03, DEC-12A-02).
3. **Modelo** — [`modelo_localizacion.py`](modelo_localizacion.py): valida, normaliza, pondera, calcula intervalos y decide si corresponde emitir un orden. Resultados en `resultados_localizacion.csv` (archivo generado; no editar a mano).

**Grupos de criterios (12):** DEMANDA · PRODUCCION_PRIMARIA · ALIMENTO · FAENA_INDUSTRIA · AGUA · EFLUENTES · ENERGIA · LOGISTICA · EXPORTACION · TERRENO · NORMATIVA · RRHH. Definición, unidad, sentido y fuente sugerida de cada uno de los 43 subcriterios en [`criterios_localizacion.md`](criterios_localizacion.md) §2.

**Fuera de la matriz (no puntúan):** el factor **NETWORK** (contactos personales, como el de Chaco, SUP-014) y los criterios que solo existen a nivel de terreno (vecinos inmediatos, cota del lote, forma, dominio). El modelo rechaza cualquier perfil que asigne peso a NETWORK.

## 4. Estados de evidencia y modos de cálculo

Cada celda tiene `TIPO_EVIDENCIA` (`VERIFICADO`, `ESTIMACION`, `SUPUESTO`, `COTIZACION`, `PVDP` o vacío) y `ESTADO`:

| ESTADO | Significado | ¿Puntúa en modo estricto? | ¿Puntúa en modo exploratorio? |
|---|---|---|---|
| `DISPONIBLE` | Dato usable con fuente | Sí, si el tipo es VERIFICADO, COTIZACION o ESTIMACION con fuente | Sí |
| `PVDP` | Visto en extracto o estimado sin medir (regla 16) | **No** | Sí, con rótulo EXPLORATORIO |
| `PENDIENTE` | Falta el dato | No (celda vacía) | No |
| `NO_APLICA` | El subcriterio no aplica a esa región | No | No |

Reglas de validación (el modelo se detiene si se violan): un dato `[PVDP]` no puede figurar como `DISPONIBLE`; todo valor lleva tipo y fuente; un `DISPONIBLE` sin valor o un `PENDIENTE` con valor son errores; la definición (grupo, sentido, unidad, nivel, normalización) de un subcriterio es la misma en todas las regiones.

**Modo estricto (por defecto)** = lo que se puede afirmar. **Modo exploratorio** = cómo funcionaría la mecánica con los extractos disponibles; **nunca** se cita como resultado.

## 5. Cálculo

### 5.1 Normalización (1 = mejor)

| Método | Mayor es mejor | Menor es mejor | Uso |
|---|---|---|---|
| `minmax` (por defecto) | n = (x − mín) / (máx − mín) | n = (máx − x) / (máx − mín) | Compara contra las regiones del conjunto |
| `rango_fijo:a:b` | igual con mín = a, máx = b y x recortado a [a, b] | ídem | Cuando el resultado no debe depender de qué regiones se agregan (evita la "inversión de ranking") |

- **Empate** (todas las regiones con dato tienen el mismo valor): n = 1 para todas; no discrimina.
- **Subcriterio NO_COMPARABLE** (no puntúa para ninguna región) si: (a) hay datos de menos de 2 unidades de observación distintas — provincias cuando `NIVEL_DATO = PROVINCIA`, corredores cuando `= CORREDOR` —, o (b) menos del 50 % de las regiones tiene dato (SUP-12A-04). Así un dato que solo existe para una provincia (p. ej., el límite de vuelco de la Res. ADA 336/2003 de Buenos Aires) **no premia ni castiga a nadie**.
- **Valores provinciales asignados a corredores** (`NIVEL_DATO = PROVINCIA`): son un proxy (SUP-12A-07) que no distingue entre corredores de la misma provincia; el modelo los cuenta por región para advertirlo.

### 5.2 Pesos

Peso del subcriterio = peso del grupo ÷ 100 ÷ n.º de subcriterios del grupo en la matriz (SUP-12A-05). Suma = 1. Los perfiles se validan: suma exactamente 100, sin negativos, sin grupos desconocidos ni omitidos, NETWORK = 0.

### 5.3 Puntaje con intervalo — sin imputar datos faltantes

Para cada región y perfil:

```
cobertura          = Σ pesos de los subcriterios con valor normalizado             (0 – 1)
puntaje observado  = Σ peso × n  sobre esos subcriterios      = COTA INFERIOR (el faltante aporta 0)
puntaje máximo     = observado + (1 − cobertura)               = COTA SUPERIOR (si todo faltante fuera el mejor)
sobre disponible   = observado ÷ cobertura                     → solo se informa si cobertura ≥ 75 %
```

El **ancho del intervalo es exactamente el peso de lo que no se sabe**. Una región con 7 % de cobertura tiene un puntaje "entre 0,07 y 0,99": no dice nada, y el modelo lo muestra así. **Ninguna región recibe puntos por datos inexistentes** (test T07) y ninguna es castigada como "la peor" por falta de datos: queda "SIN PUNTAJE".

### 5.4 Cuándo se emite un orden

- Solo entran al orden las regiones con cobertura ≥ 75 % (umbral editable, SUP-12A-04); si califican menos de 2, **RANKING NO EMITIDO**.
- Si algunas califican y otras no, el orden es **PARCIAL** y se listan las excluidas (no se las ubica últimas).
- Cada posición se marca **separada** del siguiente (cota inferior propia > cota superior del siguiente) o **no separada** (los faltantes podrían invertir el orden).
- Alerta "DEMASIADOS DATOS FALTANTES" si una región tiene más del 40 % de subcriterios sin dato.

### 5.5 Sensibilidad de ponderaciones

`--sensibilidad 0.5` multiplica el peso de cada grupo por 1,5 y por 0,5 (renormalizando a 100) y reporta si cambia el orden. Si una conclusión cambia con un ±50 % razonable en un peso, **la conclusión depende de un juicio de valor, no de los datos**, y debe discutirse con los decisores en lugar de presentarse como resultado técnico.

## 6. Limitaciones conocidas del método

1. **Compensación:** la suma ponderada permite que un muy buen puntaje en un criterio compense uno muy malo en otro. Por eso los criterios que pueden **impedir** el proyecto (sin agua apta, sin vuelco posible, uso de suelo prohibido, zona inundable) **no se ponderan**: son filtros eliminatorios a nivel de terreno ([`criterios_localizacion.md`](criterios_localizacion.md) §4).
2. **Inversión de ranking con min-max:** agregar o quitar una región puede cambiar el orden entre otras dos. Mitigación: `rango_fijo` para los criterios con escala natural (km, h, USD/ha).
3. **Doble conteo por correlación:** distancia a CABA (DEM-01) y distancia al puerto reefer (EXP-01) están casi alineadas porque las terminales reefer principales están en CABA y Dock Sud ([`../17_exportacion/logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md) §3); "granjas en radio" (PRI-02) y "densidad de granjas" (PRI-05) son la misma realidad vista como oportunidad y como riesgo. Las correlaciones declaradas están en [`criterios_localizacion.md`](criterios_localizacion.md) §3; la ponderación debe tenerlas en cuenta.
4. **Granularidad:** muchos datos públicos son provinciales; un corredor del norte bonaerense y el periurbano del AMBA comparten provincia pero no realidad.
5. **Escalas cualitativas 1–5:** solo con rúbrica ([`criterios_localizacion.md`](criterios_localizacion.md) §5) y con evidencia citada; una escala sin evidencia es `PENDIENTE`, no "3".
6. **Distancia ≠ costo:** el modelo compara condiciones, no costos. El costo logístico total (aves vivas + alimento + distribución + exportación) se calcula con 12B y luego en OPEX ([`escenarios_localizacion.md`](escenarios_localizacion.md) §1).

## 7. Interfaces con los módulos paralelos y con el resto del proyecto

| Desde / hacia | Qué fluye | Estado |
|---|---|---|
| **12B Logística (`13_logistica`) → 12A** | Distancias y tiempos medidos por ruta (DEM-01, DEM-02, EXP-01, LOG-01); costo por t·km de aves vivas, alimento, refrigerado y reefer; arquitectura de distribución (directa / CD / distribuidor / cross-dock en AMBA) | 12A **no modifica** `13_logistica`; consume sus resultados cuando existan (DPV-12A-01) |
| **12C Layout y obra civil (`09_layout_obra_civil`) → 12A** | Superficie de planta por escala y por módulo; playas, tratamiento, reserva de expansión, retiros | 12A **no modifica** `09_layout_obra_civil`; [`terreno_ideal.md`](terreno_ideal.md) deja la superficie como `[PVDP]` hasta tenerla (DPV-12A-09) |
| **12A → 12B / 12C** | Lista de corredores y centros de referencia (SUP-12A-01); requisitos de terreno por función | Este documento y [`regiones_preliminares.md`](regiones_preliminares.md) |
| `03`, `23` → 12A | Radio práctico de aves vivas (~2–4 h, ~120–250 km `[ESTIMACIÓN]`, [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §4); flujos por escala ([`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §12) | Usado como contexto, sin cambios |
| `11`, `12` → 12A | Agua, vuelco, potencia, gas y calidad de red como criterios que **pueden limitar la escala del sitio** | Incorporados como grupos AGUA, EFLUENTES, ENERGIA |
| `16` → 12A | Plantilla jurisdiccional de 14 temas (DPV-106) | Se aplica en la etapa E3 |
| `00_gestion_proyecto` | Registros maestros | **No modificados**; propuestas en [`actualizaciones_gestion_12A.md`](actualizaciones_gestion_12A.md) |

## 8. Cómo se actualiza la matriz (procedimiento)

1. Obtener el dato con su documento (descarga, factibilidad escrita, medición) y registrar la fuente (`FTE-12A-###` provisional en [`fuentes_12A.csv`](fuentes_12A.csv) hasta la consolidación).
2. Completar `VALOR`, `TIPO_EVIDENCIA`, `FUENTE` y `ESTADO` de la fila; si solo se vio un extracto, `ESTADO = PVDP`.
3. Para escalas 1–5, citar en `OBSERVACIONES` el nivel de la rúbrica y la evidencia.
4. Correr `python3 10_localizacion/modelo_localizacion.py` (las pruebas corren primero; si fallan, el script se detiene).
5. Leer **primero la cobertura y los intervalos**; recién después, si se emitió, el orden y su sensibilidad.
6. No cambiar pesos para "acomodar" un resultado: un cambio de perfil se registra como decisión (DEC-12A-02) con su justificación.
