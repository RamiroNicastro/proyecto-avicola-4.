# Conclusiones de localización industrial (módulo 12A)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría metodológica final) · **Sesión:** 12A (en paralelo con 12B Logística y 12C Layout/Obra civil) · **Estado:** metodología y modelo completos y auditados; **sin ubicación elegida y sin ranking** (DEC-003 abierta)

> **Resultado central:** se construyó un método reproducible para comparar zonas, pero **con la evidencia actual no se puede ordenar ninguna**. De 624 celdas de la matriz, 0 están verificadas, 35 son `[PVDP]` y 589 están vacías. Ninguna región alcanza la cobertura de información mínima con umbrales de 60, 75 ni 90 %, en ningún modo ni perfil. El modelo lo dice explícitamente en lugar de inventar un orden.

---

## 1. Metodología

Detalle en [`metodologia_localizacion.md`](metodologia_localizacion.md).

- **Niveles:** país → provincia → corredor → municipio → terreno. Esta sesión llega a **provincia + corredor**.
- **Embudo:** E0 universo → E1 cribado regional (este módulo) → E2 lista corta (después de los hitos H-A y H-B del plan de campo) → E3 municipios → E4 terrenos (ficha + gates) → E5 decisión con escala, CAPEX y finanzas.
- **Matriz multicriterio** en formato largo (13 corredores × 48 subcriterios: 45 monotónicos en 14 grupos ponderables + 3 trade-offs; más 2 filas NETWORK) + **4 perfiles de ponderación** editables + **modelo** que valida, normaliza, pondera y calcula la **envolvente por faltantes** y la **cobertura de información** sin imputar faltantes.
- **Sentidos:** `MAYOR_MEJOR`, `MENOR_MEJOR`, `NO_MONOTONICO` (nunca lineal) y `GATE_DURO` / `GATE_CONDICIONAL` (no puntúan; municipio/terreno).
- **Dos modos:** *estricto* (solo datos verificados, cotizaciones o estimaciones documentadas) y *exploratorio* (acepta `[PVDP]`, rotulado).
- **Datos provinciales:** `PROVINCIA_NORMA` se aplica a cada corredor; `PROVINCIA_AGREGADO` no puntúa corredores.

## 2. Densidad / ecosistema avícola (cambio de la auditoría)

La densidad avícola dejó de ser un criterio "menor es mejor". Ahora hay:

| Dimensión | Sentido | Variables (distintas entre sí) | Estado de los datos |
|---|---|---|---|
| **ECOSISTEMA_AVICOLA** | Más presencia = favorable | ECO-02 productores integrables, ECO-03 incubadoras con venta a terceros, ECO-04 servicios avícolas especializados (veterinarios, técnicos, contratistas de captura, transportistas de aves vivas, proveedores); ECO-01 faena provincial 2024 (agregado, **no puntúa**) | Vacías por corredor; ECO-01 con valores provinciales `[PVDP]` |
| **EXPOSICION_SANITARIA** | Más exposición = desfavorable | SAN-01 distancia mediana entre establecimientos, SAN-02 movimientos de aves (DT-e), SAN-03 eventos de IAAP en 50 km, SAN-04 lejanía de humedales y aves silvestres | Vacías |
| **TRADE_OFF** | No monotónico | TOF-01 densidad de granjas (variable de doble efecto), TOF-02 concentración industrial, TOF-03 distancia al borde urbano | Sin puntaje; análisis cualitativo |

Ninguna variable representa las dos cosas a la vez (test T22). El peso entre ecosistema y exposición es una decisión estratégica (DEC-12A-02).

## 3. Criterios monotónicos vs trade-off

- **Monotónicos (45):** cada uno mide **una sola dimensión** en la que más (o menos) es mejor: distancia y tiempo al AMBA, productores, incubadoras, servicios, exposición sanitaria, clima, maíz, molienda, fábricas, façon, agua, vuelco, energía, accesos, nodo reefer, parques industriales, precio de tierra (solo DPV), riesgo hídrico, presión urbana, plazos ambientales, mano de obra.
- **No monotónicos (3, sin puntaje):** densidad de granjas, concentración industrial, cercanía al borde urbano. No hay función defendible (registro `FUNCIONES_NO_MONOTONICAS` vacío): se analizan cualitativamente o se dividen en componentes. Un intento de normalizarlos linealmente es rechazado por el modelo (T21).
- DEM-01 (distancia a CABA) sigue siendo monotónico porque mide **solo** la dimensión de distribución; las compensaciones (granjas, tierra, sanidad) están en otros criterios.

## 4. Gates duros vs condicionales

| Tipo | Gates | Efecto |
|---|---|---|
| **Duro** (solo con imposibilidad demostrada por escrito) | G-D1 uso de suelo incompatible sin vía legal · G-D2 imposibilidad demostrada de agua mínima · G-D3 imposibilidad legal de gestionar efluentes · G-D4 imposibilidad física de energía indispensable | Descarta **ese terreno** (o municipio) |
| **Condicional** | G-C1 riesgo hídrico mitigable · G-C2 vecinos · G-C3 receptor de subproductos · G-C4 falta inicial de gas · G-C5 potencia limitada ampliable · G-C6 agua que requiere tratamiento · G-C7 acceso | Marca el terreno **CONDICIONADO** (inversión, tratamiento, tercerización, mitigación o diseño) |

Se aplican en E3/E4 (municipio/terreno). **Ningún gate de un terreno elimina una región completa**; un gate duro afirmado solo de palabra deja el terreno condicionado, no descartado (T23). Umbrales concretos: DEC-12A-03.

## 5. Sensibilidad del umbral de cobertura 60 / 75 / 90 %

El 75 % es un **criterio de control del modelo / supuesto metodológico**, no un estándar de análisis multicriterio.

| Modo | Perfil | Elegibles con 60 % | con 75 % | con 90 % |
|---|---|---|---|---|
| Estricto | A, B, C, D | 0 | 0 | 0 |
| Exploratorio | A, B, C, D | 0 | 0 | 0 |

Con los datos actuales **el conjunto elegible no cambia porque es vacío en todos los casos**: la cobertura de información máxima es 6 % (exploratorio, perfil A, solo por la distancia estimada a CABA). Con datos ficticios de demostración (T24), el conjunto sí cambia: 3 regiones elegibles con 60 %, 2 con 75 % y 1 con 90 % (sin orden). Cuando haya datos reales, el resultado deberá informarse junto con esta sensibilidad.

## 6. Interpretación correcta de los rangos por faltantes

- **Qué es:** la **envolvente de peor/mejor caso producida exclusivamente por la información faltante**: mínimo = cada faltante vale 0; máximo = cada faltante vale 1. Su ancho es exactamente el peso de lo que no se sabe.
- **Qué NO es:** no es un intervalo de confianza, no es una probabilidad, no es un error estadístico. No dice qué valor es más probable ni mide la incertidumbre de los datos que sí existen.
- **Cómo se muestra:** siempre junto con la **COBERTURA_DE_INFORMACION** (% del peso con dato admisible), en consola, en `resultados_localizacion.csv` (`PUNTAJE_MIN_FALTANTES_0`, `PUNTAJE_MAX_FALTANTES_1`, `COBERTURA_DE_INFORMACION`) y en la futura interfaz (T25).

Datos reales, modo exploratorio (**no es resultado**):

| Perfil | Cobertura de información | Envolvente por faltantes |
|---|---|---|
| A — Mercado | 6 % en todas las regiones | de 0,000–0,060 (mínimo) a 0,940–1,000 (máximo) |
| B — Producción | 2 % | 0,000–0,016 → 0,984–1,000 |
| C — Equilibrado | 2 % | 0,000–0,024 → 0,976–1,000 |
| D — Exportador | 2 % | 0,000–0,016 → 0,984–1,000 |

Cualquier orden es compatible con lo que se sabe. Respecto de la v1.0 la cobertura exploratoria bajó (de hasta 10 % a hasta 6 %) porque los agregados provinciales (faena, plantas) ya no puntúan corredores: es una corrección, no una pérdida de información.

## 7. Fuentes oficiales incorporadas

En [`fuentes_12A.csv`](fuentes_12A.csv), con trazabilidad "**confirmado en revisión externa del proyecto; lectura directa pendiente en este entorno**" (el acceso a magyp.gob.ar y argentina.gob.ar/senasa sigue bloqueado; prueba 2026-10-01):

| ID | Fuente | Universo · año | Dato | Uso en 12A |
|---|---|---|---|---|
| FTE-12A-015 | SAGyP, "Faena Provincial 2024–2025" | **Faena habilitada por SENASA · 2024** | ER ~50,90 %; BA ~34,89 %; SF ~5,09 %; Cba ~4,49 %; RN ~2,41 % | ECO-01 (agregado provincial: **no puntúa corredores**) y contexto en regiones |
| FTE-12A-016 | SAGyP, "Faena Provincial 2025–2026" | Faena habilitada por SENASA · 2025–2026 | No leída | Actualización futura de ECO-01 |
| FTE-12A-017 | SENASA, publicación del 2024-07-02 | **Actividad avícola** | Casi 90 % en Entre Ríos y Buenos Aires | Solo contexto; **no** es participación de faena |

No se mezclan actividad avícola, producción primaria y faena; tampoco el extracto 2025 de FTE-001 con la tabla oficial 2024 (regla 18).

## 8. Corrección de Río Negro

Antes: "Río Negro tiene 2,5 % de la faena". Ahora: **"Río Negro representó aproximadamente 2,4 % de la faena nacional habilitada por SENASA en 2024 según la tabla oficial de Secretaría de Agricultura"** (FTE-12A-015, confirmado en revisión externa; lectura directa pendiente). Sigue como **referencia secundaria**: no se descarta ni se incorpora automáticamente a la matriz principal.

## 9. Corrección de puertos / exportación

- Se eliminó "las terminales refrigeradas están en CABA y Dock Sud". Ahora: **"Buenos Aires / Dock Sud son nodos logísticos de referencia para contenedores y deben compararse con otras alternativas portuarias"**, porque no hay un inventario nacional de terminales reefer verificado.
- **Cercanía a puerto ≠ disponibilidad reefer ≠ servicio marítimo adecuado ≠ exportación habilitada.**
- Nuevo DPV-12A-10 **por nodo** (Buenos Aires, Dock Sud, Zárate, Gran Rosario, Concepción del Uruguay u otros): terminal de contenedores, enchufes/capacidad reefer, frecuencia, destinos, cut-off, costos y disponibilidad real.
- Nuevo subcriterio EXP-04 (servicio reefer verificado del nodo) y **dependencia**: los km al nodo (EXP-01) solo puntúan si EXP-04 ≥ 3. La proximidad a un puerto no produce por sí sola puntaje exportador (T27).

## 10. Sensibilidad t·km (red ancla)

Se mantiene la sensibilidad, ahora con **todos los parámetros explícitos** ([`escenarios_localizacion.md`](escenarios_localizacion.md) §3): origen = centro de referencia del corredor; distancia por ruta = orden de magnitud no medido (SUP-12A-02); toneladas = 1,0 / 4,5 / 13,5 / 27 t/día de prueba; 100 % al AMBA (con variante 60 % y 30 %); entrega troncal a un único punto del AMBA cuya existencia (CD de la red o cross-dock) **no está confirmada** (DPV-036).

- Con esos parámetros, Resistencia (~1.020 km) frente a Pilar (~55 km) da **≈ 18,5 veces** más t·km de traslado troncal (antes se citaba "~19 veces" sin parámetros). Ese múltiplo es **solo el cociente de dos distancias supuestas**; no es una característica de una provincia.
- La forma de distribución puede cambiar sustancialmente el resultado: sin CD, una planta lejana no puede repartir a 90 locales desde su origen y necesita la arquitectura R2.
- **Una planta vs planta + CD** quedan como **arquitecturas de red diferentes** (DEC-12A-04, abierta), no como criterios equivalentes de localización. La comparación futura considerará inversión, inventario, frío, doble manipulación, transporte primario, distribución secundaria y nivel de servicio, **sin calcular costos todavía**.

## 11. Integración con 12C

12C está generando una estimación conceptual de superficie en su propia rama; 12A **no la leyó ni la modificó**. La superficie del terreno sigue **pendiente** en 12A. En la reconciliación 12A–12C se reemplazará el estado genérico por **el rango conceptual de 12C + las restricciones reales municipales y del terreno** (DPV-12A-09, [`terreno_ideal.md`](terreno_ideal.md) §4).

## 12. Zonas habilitadas para investigación y datos de campo

Sin cambios respecto de la v1.0: **las 13 regiones siguen habilitadas para investigación**, ninguna descartada ni priorizada por preferencia; Río Negro como referencia secundaria. La lista corta (DEC-12A-06) se define después de los hitos H-A y H-B. Datos de terreno a levantar: los que alimentan los gates (uso de suelo, agua, efluentes, energía, riesgo hídrico, vecinos, subproductos), por escrito, más superficie, topografía, distancias medidas y precio como `[COTIZACIÓN]` ([`terreno_ideal.md`](terreno_ideal.md) §6). Nuevos datos regionales: servicios avícolas especializados (DPV-12A-11), exposición sanitaria por corredor (DPV-12A-12) y nodos portuarios (DPV-12A-10).

## 13. Tests

`python3 10_localizacion/modelo_localizacion.py --solo-tests` → **28/28** superadas.

| Test | Qué prueba | v1.1 |
|---|---|---|
| T01 | Perfiles suman 100 (14 grupos); errores de pesos rechazados; pesos de subcriterios suman 1 | sin cambios |
| T02 | Inversión menor/mejor | sin cambios |
| T03 | Faltantes: aportan 0, ancho de la envolvente = peso faltante, no se imputan | redacción |
| T04 | Sin ranking ni puntaje cuando la cobertura es insuficiente | códigos de la demo |
| T05 | Cambiar ponderaciones cambia el resultado (A → Z-CERCA, B → Z-CLUSTER) | sin cambios |
| T06 | `[PVDP]` ignorado en modo estricto | sin cambios |
| T07 | Ninguna región recibe puntos por datos inexistentes | sin cambios |
| T08 | NETWORK con peso > 0 rechazado; su fila no cambia puntajes | sin cambios |
| T09 | Validación de estados de evidencia; matriz real válida | sin cambios |
| T10 | Dato de una sola provincia → NO_COMPARABLE | nivel `PROVINCIA_NORMA` |
| T11 | Alerta de faltantes solo en la región afectada | códigos de la demo (8/15) |
| T12 | `[SUPUESTO]` excluido en modo estricto | sin cambios |
| T13 | Invariancia de unidades | sin cambios |
| T14 | Empate y rango fijo | sin cambios |
| T15 | Suma de contribuciones = mínimo; mínimo ≤ sobre disponible ≤ máximo | sin cambios |
| T16 | Con datos completos la envolvente es nula | redacción |
| T17 | Matriz real: grilla completa 13 × 48; ningún ranking (estricto ni exploratorio) | grilla con trade-offs y NETWORK |
| T18 | Agregados provinciales excluidos por defecto en la matriz real; con autorización se cuentan; vuelco solo-BA NO_COMPARABLE | **actualizado**: antes contaba el agregado como dato de corredor |
| T19 | Evaluar no modifica la matriz | sin cambios |
| T20 | Sensibilidad ±50 %: detecta cambios con margen chico (A: 8/28) y estabilidad con margen amplio (C: 0/28) | **actualizado**: la demo reestructurada dejó a C estable; la prueba ahora exige ambas cosas |
| T21 | `NO_MONOTONICO` sin min-max lineal (validación y normalizar); se informa como trade-off | nuevo |
| T22 | Ecosistema y exposición: variables disjuntas, sentidos opuestos; densidad no puntúa | nuevo |
| T23 | Gate condicional no elimina; duro descarta solo el terreno y solo con documento; nunca la región | nuevo |
| T24 | Sensibilidad de cobertura 60/75/90 % (3/2/1 elegibles en la demo) | nuevo |
| T25 | El rango nunca se denomina intervalo de confianza; cobertura junto al rango | nuevo |
| T26 | `PROVINCIA_AGREGADO` no se usa automáticamente como dato de corredor | nuevo |
| T27 | La proximidad al puerto no puntúa sin servicio reefer verificado | nuevo |
| T28 | Contacto de Chaco: solo en regiones de Chaco, peso cero, no cambia puntajes | nuevo |

T17 y T18 describen el estado actual de los datos: cuando la matriz se complete, deberán revisarse a propósito.

## 14. Archivos

| Archivo | Contenido |
|---|---|
| [`metodologia_localizacion.md`](metodologia_localizacion.md) | Niveles, embudo, matriz, sentidos, evidencia, cálculo, envolvente, cobertura y su sensibilidad, gates, arquitecturas de red, interfaces |
| [`criterios_localizacion.md`](criterios_localizacion.md) | Ecosistema vs exposición, subcriterios monotónicos y trade-offs, gates, correlaciones, rúbricas, bioseguridad, exportación, NETWORK |
| [`regiones_preliminares.md`](regiones_preliminares.md) | 13 corredores, faena 2024 con año y universo, Río Negro, Buenos Aires, GTA, Chaco |
| [`escenarios_localizacion.md`](escenarios_localizacion.md) | Distancia ≠ costo, arquetipos L1–L4, arquitecturas R1/R2, red ancla con parámetros explícitos, exportación por nodo |
| [`terreno_ideal.md`](terreno_ideal.md) | Requisitos del terreno, gates, superficie pendiente de la reconciliación con 12C |
| [`matriz_localizacion.csv`](matriz_localizacion.csv) | 626 filas (624 celdas + 2 NETWORK); vacías o `[PVDP]` |
| [`pesos_localizacion.csv`](pesos_localizacion.csv) | Perfiles A–D con 14 grupos |
| [`modelo_localizacion.py`](modelo_localizacion.py) | Modelo v1.1 con 28 tests |
| `resultados_localizacion.csv` | Salida generada (envolvente, cobertura, elegibilidad 60/75/90) |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos para el promotor |
| [`actualizaciones_gestion_12A.md`](actualizaciones_gestion_12A.md) | Registros provisionales (§6: auditoría) |
| [`fuentes_12A.csv`](fuentes_12A.csv) | 17 fuentes provisionales (3 oficiales en revisión externa) |

**Calidad:** MEDIA–ALTA como método y modelo tras la auditoría; **NULA como evidencia comparativa** (0 celdas verificadas). No se eligió ubicación, no se seleccionaron terrenos, no se calcularon CAPEX ni OPEX, no se modificaron `00_gestion_proyecto/`, `25_fuentes/`, `13_logistica/` ni `09_layout_obra_civil/`.
