# Conclusiones de localización industrial (módulo 12A)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · **Sesión:** 12A (en paralelo con 12B Logística y 12C Layout/Obra civil) · **Estado:** metodología y modelo completos; **sin ubicación elegida y sin ranking** (DEC-003 abierta)

> **Resultado central:** se construyó un método reproducible para comparar zonas, pero **con la evidencia actual no se puede ordenar ninguna**. De 559 celdas de la matriz, 0 están verificadas, 35 son `[PVDP]` y 524 están vacías. El modelo lo dice explícitamente en lugar de inventar un orden. Eso no es una falla: es el estado real del conocimiento.

---

## 1. Metodología

Detalle en [`metodologia_localizacion.md`](metodologia_localizacion.md).

- **Niveles:** país → provincia → corredor → municipio → terreno. Esta sesión llega a **provincia + corredor**; municipio y terreno quedan para la lista corta (ola O8).
- **Embudo:** E0 universo → E1 cribado regional (este módulo) → E2 lista corta (después de los hitos H-A capital/ancla y H-B escala/abastecimiento) → E3 municipios (plantilla de 14 temas) → E4 terrenos (ficha + filtros eliminatorios) → E5 decisión junto con escala, CAPEX y finanzas.
- **Matriz multicriterio** en formato largo (13 corredores × 43 subcriterios en 12 grupos) + **perfiles de ponderación** editables + **modelo** que valida, normaliza (min-max o rango fijo, con inversión para "menor es mejor"), pondera y calcula un **intervalo** [observado, máximo] por región sin imputar faltantes.
- **Dos modos:** *estricto* (solo datos verificados, cotizaciones o estimaciones documentadas) y *exploratorio* (acepta `[PVDP]`, siempre rotulado).
- **Reglas de emisión:** puntaje informado solo con cobertura ≥ 75 % del peso; orden solo entre regiones que la alcanzan; subcriterio no comparable si sus datos vienen de una sola provincia o de < 50 % de las regiones; NETWORK nunca puntúa.

## 2. Regiones comparadas

Detalle en [`regiones_preliminares.md`](regiones_preliminares.md). Ninguna elegida ni descartada.

| Provincia | Corredores |
|---|---|
| Buenos Aires | BA-AMBA (periurbano), BA-NORTE (RN9/RN8), BA-OESTE (RN5/RN7), BA-INTERIOR (centro y sur de menor presión urbana) |
| Entre Ríos | ER-SUR (Gualeguaychú–Gualeguay), ER-URUGUAY (cluster del río Uruguay), ER-CENTRO (Paraná–Crespo–Villaguay) |
| Santa Fe | SF-SUR (Gran Rosario y corredor del Paraná), SF-CENTRO (Santa Fe–Esperanza–Rafaela) |
| Córdoba | CBA-SUR (Río Cuarto), CBA-ESTE (Villa María–Marcos Juárez–San Francisco) |
| Chaco | CH-ESTE (Gran Resistencia), CH-CENTRO (Sáenz Peña) |

Referencia secundaria fuera de la matriz: **Río Negro** (2,5 % de la faena SENASA 2025, FTE-001 `[PVDP]`), por evidencia de actividad, sin incorporarla a la comparación. No se agregaron otras provincias por falta de evidencia.

## 3. Criterios principales

Detalle en [`criterios_localizacion.md`](criterios_localizacion.md).

- **12 grupos:** demanda, producción primaria, alimento, faena/industria, agua, efluentes, energía, logística, exportación, terreno, normativa, RRHH.
- **Los que más diferencian corredores** (cuando haya datos): granjas e integrables en radio (PRI-02, PRI-03), pollito BB (PRI-04), densidad avícola como riesgo (PRI-05), maíz y fábricas de alimento (ALI-01, ALI-03), façon (IND-02), calidad del acuífero (AGU-02), cuerpo receptor (EFL-02), potencia y gas (ENE-01, ENE-02), tiempo al AMBA (DEM-02), presión urbana (TER-04).
- **Filtros eliminatorios** (no ponderables, a nivel terreno): uso de suelo, agua, vuelco, energía, riesgo hídrico, vecinos, receptor de subproductos.
- **Fuera de la matriz:** el contacto en Chaco (factor NETWORK, cualitativo, sin peso).

## 4. Información faltante

| Bloque | Qué falta | Registro | Ola |
|---|---|---|---|
| Demanda | Mapa de locales y CD de la red; otros canales | DPV-018, DPV-036, DPV-040 | O1–O2 |
| Producción primaria | Granjas, integrables e incubadoras **georreferenciadas** por corredor; IAAP georreferenciada; clima | DPV-023, DPV-047, DPV-048, DPV-12A-05, DPV-12A-07 | O0, O4 |
| Alimento | Maíz y soja por departamento; plantas de molienda; fábricas y precio puesto | DPV-12A-02, DPV-050 | O0, O4 |
| Industria | Capacidad a façon por radio; servicios técnicos | DPV-006, DPV-089 | O3, O7 |
| Agua y efluentes | Caudal y calidad de acuíferos; límites de vuelco de ER, SF, Cba y Chaco | DPV-053, DPV-067, DPV-106 | O8 |
| Energía | Potencia en MT, gas industrial, calidad de servicio por distribuidora | DPV-052, DPV-087 | O8 |
| Logística y exportación | Distancias y tiempos **medidos**; servicios reefer por terminal | DPV-12A-01, DPV-027 | O0 (con 12B) |
| Terreno y normativa | Parques industriales; riesgo hídrico; densidad por partido; plazos de EIA; superficie por escala | DPV-12A-03, DPV-12A-04, DPV-12A-08, DPV-106, DPV-12A-09 | O0, O8 (con 12C) |
| RRHH | Población activa, experiencia, técnicos | DPV-12A-06 | O8 |

Cobertura por grupo hoy: solo DEM-01 (distancia, estimada), PRI-01 (faena provincial), IND-01 (plantas provinciales) y EFL-01 (vuelco, solo Buenos Aires) tienen algún valor, todos `[PVDP]`.

## 5. Sensibilidad de ponderaciones

**Con los datos reales — modo estricto:** cobertura 0 % en las 13 regiones y en los 4 perfiles; **RANKING NO EMITIDO**.

**Con los datos reales — modo exploratorio** (acepta `[PVDP]`; **no es resultado**), perfil C equilibrado:

| Región | Cobertura | Intervalo de puntaje [observado – máximo] |
|---|---|---|
| BA-AMBA / BA-NORTE / BA-OESTE / BA-INTERIOR | 4 % | 0,030–0,036 → 0,989–0,994 |
| ER-SUR / ER-URUGUAY / ER-CENTRO | 7 % | 0,062–0,067 → 0,991–0,996 |
| SF-SUR / SF-CENTRO | 7 % | 0,018–0,022 → 0,947–0,951 |
| CBA-SUR / CBA-ESTE | 7 % | 0,012–0,013 → 0,941–0,942 |
| CH-ESTE / CH-CENTRO | 2 % | 0,000–0,003 → 0,976–0,979 |

Todas las regiones tienen un intervalo de casi 0 a casi 1: **cualquier orden sería compatible con los datos**. En los perfiles A, B y D ocurre lo mismo (coberturas de 2 % a 10 %). 40 de los 43 subcriterios son NO_COMPARABLES (incluido el límite de vuelco, que solo existe para Buenos Aires).

**Con datos ficticios de demostración** (`--demo`; tres zonas inventadas): el primer lugar cambia de Z-CERCA (perfil A) a Z-CLUSTER (perfiles B, C y D); con ±50 % en el peso de un solo grupo, el orden cambia en 6 de 24 variaciones del perfil A, 7 de 24 del B, 2 de 24 del C y 9 de 24 del D. En el perfil B, las dos primeras zonas quedan a 0,009 de distancia. **Lección:** cuando los datos existan, cualquier "ganador" deberá presentarse con su sensibilidad; si cambia con un ±50 % razonable de un peso, la elección es estratégica (DEC-12A-02), no técnica.

## 6. Principales trade-offs

Detalle en [`escenarios_localizacion.md`](escenarios_localizacion.md).

1. **Mercado vs granjas:** cerca del AMBA se gana distribución y se pierde bioseguridad, bienestar de aves vivas, suelo y expansión; la lógica sectorial es "planta cerca de las granjas, producto refrigerado al mercado".
2. **Ecosistema vs sanidad:** el cluster entrerriano ofrece todo cerca y concentra el riesgo; una zona de baja densidad ofrece sanidad inicial y obliga a construir el ecosistema.
3. **Tierra barata vs servicios:** un terreno barato sin potencia, agua apta o vuelco puede ser el más caro de operar.
4. **Puerto vs granos:** las terminales reefer están en CABA/Dock Sud; el maíz y la soja, en el centro del país. Estar cerca del puerto no vuelve exportadora a una planta.
5. **Planta única vs dos nodos:** faena productiva + nodo comercial en el AMBA (DEC-12A-04).
6. **Red de supermercados:** con ancla fuerte (13,5–27 t/día de prueba), una planta a ~1.000 km mueve ~19 veces más t·km hacia el AMBA que una en el periurbano; sin ancla, la cercanía al AMBA pierde peso relativo. **La arquitectura de distribución (CD vs 90 locales) puede pesar más que la ubicación de la planta.** Demanda no validada: solo sensibilidad.

## 7. Zonas habilitadas para investigación futura

**Las 13 regiones quedan habilitadas para investigación**; ninguna se descarta ni se prioriza por preferencia. Lo que difiere es **qué hay que averiguar primero** en cada una:

| Región | Pregunta que más podría cambiar su evaluación |
|---|---|
| BA-AMBA | ¿Algún municipio admite frigorífico con expansión? ¿Sirve más como nodo comercial (trozado/distribución) que como faena? |
| BA-NORTE, BA-OESTE | ¿Hay productores e incubadoras en radio? ¿Calidad de acuíferos? ¿Servicios reefer en Zárate? |
| BA-INTERIOR | ¿Cuánto cuesta construir el ecosistema (pollito, alimento, servicios)? ¿Riesgo de IAAP georreferenciado? |
| ER-SUR, ER-URUGUAY, ER-CENTRO | ¿Hay productores integrables libres (incluidos ex integrados de GTA, sin suponerlo)? ¿Presión sanitaria real? ¿Límites de vuelco provinciales? |
| SF-SUR, SF-CENTRO | ¿Productores e incubadoras? ¿Ventaja real de alimento (molienda, maíz)? |
| CBA-SUR, CBA-ESTE | ¿Productores? ¿Diferencial de maíz? ¿Situación de Avex sin asumir disponibilidad? |
| CH-ESTE, CH-CENTRO | Prácticamente todo: pollito, alimento, agua, energía, mercado regional. **Requiere relevamiento específico antes de ser comparable** (cobertura 2 %) |

La lista corta (DEC-12A-06) se define **después** de los hitos H-A y H-B del plan de campo, no antes.

## 8. Datos de terreno a levantar en campo

Con la [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md) y los requisitos de [`terreno_ideal.md`](terreno_ideal.md), en este orden (los cinco primeros son eliminatorios y deben estar **por escrito**):

1. Uso de suelo y posibilidad de ampliación.
2. Agua: caudal (ensayo de bombeo) y calidad (análisis).
3. Vuelco: cuerpo receptor, organismo, límites, permiso.
4. Energía: potencia disponible y ampliable; gas natural.
5. Riesgo hídrico: cota, anegamiento, acceso con lluvia.
6. Vecinos y vientos; antecedentes de conflictos; postura municipal.
7. Superficie, forma, topografía, napa, linderos disponibles.
8. Distancias medidas a granjas, incubadoras, alimento, rendering, SENASA, rutas y puertos.
9. Precio como `[COTIZACIÓN]`.

La superficie necesaria **no** se fija todavía: depende de la escala, de la tecnología de efluentes y del layout de 12C (DPV-12A-09).

## 9. Tests

`python3 10_localizacion/modelo_localizacion.py --solo-tests` → **20/20** superadas:

| Test | Qué prueba |
|---|---|
| T01 | Perfiles suman 100; sumas ≠ 100, negativos, grupos desconocidos u omitidos se rechazan; pesos de subcriterios suman 1 |
| T02 | Inversión menor/mejor |
| T03 | Faltantes: aportan 0, cobertura = 1 − peso faltante, ancho del intervalo = peso faltante, no se imputan |
| T04 | Sin ranking ni puntaje cuando la cobertura es insuficiente; alerta de faltantes |
| T05 | Cambiar ponderaciones cambia el resultado (demo: A → Z-CERCA, B → Z-CLUSTER) |
| T06 | `[PVDP]` ignorado en modo estricto; solo el exploratorio lo usa |
| T07 | Ninguna región recibe puntos por datos inexistentes; región sin datos fuera del orden (no última); matriz real con observado 0 |
| T08 | NETWORK (contacto en Chaco): peso > 0 rechazado; su fila no cambia puntajes |
| T09 | Validación: PVDP disfrazado de DISPONIBLE, sin fuente, no numérico, DISPONIBLE sin valor, PENDIENTE con valor; matriz real válida |
| T10 | Dato de una sola provincia → NO_COMPARABLE |
| T11 | Alerta de faltantes solo en la región afectada |
| T12 | `[SUPUESTO]` excluido en modo estricto |
| T13 | Invariancia de unidades (km → m) |
| T14 | Empate y rango fijo con recorte |
| T15 | Suma de contribuciones = observado; observado ≤ sobre disponible ≤ máximo |
| T16 | Con datos completos el intervalo es nulo |
| T17 | Matriz real: grilla completa 13 × 43; ningún perfil emite ranking (estricto ni exploratorio) |
| T18 | Datos provinciales contados por región; vuelco solo-BA NO_COMPARABLE |
| T19 | Evaluar no modifica la matriz (no se rellenan celdas) |
| T20 | Sensibilidad ±50 % detecta cambios de orden en la demo |

T17 y T18 describen el **estado actual de los datos**: cuando la matriz se complete, deberán revisarse (dejarán de cumplirse a propósito).

## 10. Archivos

| Archivo | Contenido |
|---|---|
| [`metodologia_localizacion.md`](metodologia_localizacion.md) | Niveles, embudo, matriz, estados de evidencia, cálculo, limitaciones, interfaces con 12B/12C |
| [`criterios_localizacion.md`](criterios_localizacion.md) | 43 subcriterios, correlaciones, filtros eliminatorios, rúbricas 1–5, bioseguridad, exportación, NETWORK |
| [`regiones_preliminares.md`](regiones_preliminares.md) | 13 corredores, lógicas de Buenos Aires, fichas por provincia, GTA, Chaco |
| [`escenarios_localizacion.md`](escenarios_localizacion.md) | Distancia ≠ costo, arquetipos L1–L5, red de supermercados S0–S2, exportación X0–X5, escala, trade-offs |
| [`terreno_ideal.md`](terreno_ideal.md) | Requisitos del terreno por función, atributos físicos, superficie (pendiente), datos de campo |
| [`matriz_localizacion.csv`](matriz_localizacion.csv) | Matriz región × subcriterio (559 filas; vacías o `[PVDP]`) |
| [`pesos_localizacion.csv`](pesos_localizacion.csv) | Perfiles A–D (fuente única de pesos) |
| [`modelo_localizacion.py`](modelo_localizacion.py) | Modelo reproducible con 20 tests |
| `resultados_localizacion.csv` | Salida generada por el modelo (no editar) |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos para el promotor |
| [`actualizaciones_gestion_12A.md`](actualizaciones_gestion_12A.md) | SUP-12A, DPV-12A, DEC-12A y anotaciones a consolidar |
| [`fuentes_12A.csv`](fuentes_12A.csv) | 14 fuentes identificadas, no consultadas |

**Calidad:** MEDIA como método y modelo; **NULA como evidencia comparativa** (0 celdas verificadas). No se eligió ubicación, no se seleccionaron terrenos, no se calcularon CAPEX ni OPEX, no se modificaron `00_gestion_proyecto/`, `25_fuentes/`, `13_logistica/` ni `09_layout_obra_civil/`.
