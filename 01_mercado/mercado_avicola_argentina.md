# Mercado de carne aviar en Argentina — radiografía 2026

**Fecha de referencia:** 2026-09-29 · **Versión:** 2 (segunda pasada de control) · **Fase:** 0 (prefactibilidad) · **Carpeta:** `01_mercado`

Documentos asociados:

- Datos numéricos con fuente, estado de verificación y solidez: [`datos_mercado.csv`](datos_mercado.csv) (IDs `M###`).
- Empresas: [`competidores.md`](competidores.md).
- Comercio exterior, acceso a mercados, Halal e ingreso por ave: [`exportaciones.md`](exportaciones.md).
- Conclusiones: [`conclusiones_mercado.md`](conclusiones_mercado.md).
- Fuentes (`FTE-###`): [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv).

> **Restricciones de fase:** no se recomiendan inversión, maquinaria, terreno ni capacidad de faena (ver [`estado_proyecto.md`](../00_gestion_proyecto/estado_proyecto.md)).
> **Visión del proyecto** (ver `CLAUDE.md`): empresa avícola integrada, escalable y con vocación exportadora. La red de ~90 supermercados es una posible ventaja inicial, no el límite de escala.

---

## 0. Estado de verificación y convenciones

### 0.1 Verificación documental: no fue posible en esta sesión

Se intentó dos veces (versión 1 y versión 2, 2026-09-29) leer los documentos originales. La red del entorno bloqueó **todos** los dominios probados: magyp.gob.ar, datos.magyp.gob.ar, datos.gob.ar, argentina.gob.ar, senasa.gob.ar, indec.gob.ar, fas.usda.gov, fao.org, infoleg.gob.ar, aviculturaargentina.com.ar, maizar.org.ar, bcr.com.ar, además de Wikipedia y el archivo web.

Por lo tanto, **ninguna cifra de este documento está confirmada contra su documento original.** Todas provienen de extractos de buscador de documentos identificados. En la versión 2 se hizo una **triangulación**: se buscó cada cifra crítica en fuentes independientes y se registraron las contradicciones.

### 0.2 Etiquetas usadas

| Etiqueta | Significado |
|---|---|
| `[PVDP]` | **PENDIENTE DE VERIFICACIÓN DOCUMENTAL PRIMARIA.** Fuente A o B identificada y cifra coherente con otras fuentes. Utilizable como orden de magnitud; no como dato confirmado. |
| `[PVDP · débil]` | Ídem, pero la fuente es débil (prensa sola, sin fecha), parcial o contradictoria. No usar para decisiones. |
| `[ESTIMACIÓN]` | Cálculo propio. Se explica el método. Sus insumos son `[PVDP]`. |
| `[SUPUESTO]` | Hipótesis de trabajo registrada en `supuestos.md`. |

Ninguna cifra lleva `[VERIFICADO]` en esta versión (regla 16 de `CLAUDE.md`).

### 0.3 Definiciones (evitar mezclar universos)

| Concepto | Definición | Advertencia |
|---|---|---|
| **Faena SENASA** | Aves faenadas en plantas con habilitación de SENASA (tránsito federal). Es la serie oficial de cabezas. | No es la faena total. |
| **Faena total / "pollos producidos"** | Faena SENASA + plantas provinciales y municipales (+ autoconsumo o informal). Sin serie pública. | Las cifras sectoriales (~900 M) no tienen metodología publicada (§1.2). |
| **Pollitos BB parrilleros** | Pollitos de un día producidos por incubación | Antes de la faena hay mortalidad en granja y posibles descartes. No equivale a faena. |
| **Producción (t)** | SAGyP la estima con faena nacional, provincial y municipal más avimetría. CEPA publica su propia cifra. | No dividir producción por faena SENASA para obtener kg/ave. |
| **Consumo aparente** | Producción + importación − exportación (± stock). Per cápita: dividido por población. | Cada fuente usa su metodología (§13). |
| **Exportaciones** | "Comestibles" (SAGyP/INDEC) o "total sector" (CEPA: incluye subproductos y alimento balanceado) | No mezclar definiciones en una serie. |

---

## 1. Tamaño del mercado

### 1.1 Magnitudes clave 2025

| Indicador | Valor | Unidad | Fuente | Estado |
|---|---|---|---|---|
| Faena en plantas SENASA | 750,2 (SAGyP ene–nov: 686; proyección 753) | millones de cabezas | FTE-020, FTE-070 | [PVDP] |
| Producción de carne aviar, estimación oficial | ~2,3 | millones de t | SAGyP vía BCR (FTE-070) | [PVDP] |
| Producción de carne aviar, CEPA | 2,47 | millones de t | FTE-020 | [PVDP · débil] (contradice la oficial) |
| Consumo per cápita (serie de referencia SAGyP) | 47,68 | kg/hab/año | FTE-003 | [PVDP] |
| Consumo per cápita (rango entre fuentes) | 46,8 – 49,4 | kg/hab/año | FTE-027, FTE-030 | [PVDP] |
| Consumo aparente ene–ago | 1,4 (+2 %; máximo de la serie 2016) | millones de t | FTE-070 | [PVDP] |
| Exportaciones, definición amplia CEPA | 206.436 t / USD 246,9 M FOB | t / USD | FTE-020 | [PVDP] |
| Importaciones ene–jul | 12.951 (+295 %) | t | INDEC vía FTE-075 | [PVDP] |
| Destino mercado interno (2024) | 93 | % de la producción | FTE-007 | [PVDP] |

**Lectura:** es un mercado **grande, maduro y orientado al consumo interno** (la prensa ubica a Argentina como sexto consumidor per cápita de pollo del mundo, FTE-068 [PVDP · débil]). Exporta ~7–8 % del volumen. Las importaciones crecen rápido, pero todavía representan ~1 % del consumo `[ESTIMACIÓN]`.

### 1.2 Faena y la brecha "750 M vs ~900 M" (inconsistencia estadística pendiente)

**Serie de faena SENASA (millones de cabezas):**

| Año | Valor | Fuente | Estado | Observación |
|---|---|---|---|---|
| 2020 | 757,9 | FTE-026 | [PVDP · débil] | Fuente primaria no identificada |
| 2021 | 741,4 | FTE-023 (CEPA) | [PVDP] | |
| 2022 | s/d | — | — | Faltante |
| 2023 | 740,5 (alt. 734,5) | FTE-002 (alt. FTE-025) | [PVDP] / [PVDP · débil] | Contradicción (§13) |
| 2024 | 739,1 | FTE-002 | [PVDP] | ER: 374,7 M (50,7 %) según SENASA (FTE-074) |
| 2025 | 750,2 (SAGyP: proyección 753) | FTE-020, FTE-070 | [PVDP] | ER: 378 M (50,4 %) (FTE-074) |
| Promedio última década | ~740 | FTE-024 | [PVDP] | Faena estancada |

**La brecha.** En la versión 1 se concluyó que "900 − 750 = 150 M aves faenadas en plantas provinciales o municipales". **Esa conclusión se retira.** Al analizar los universos de cada cifra aparece lo siguiente:

| Cifra | Qué mide | Período | Metodología | Fuente |
|---|---|---|---|---|
| 750 M | Faena en plantas SENASA | Año calendario 2025 | Registro oficial | FTE-020, FTE-070 |
| ~900 M | "Pollos faenados por año" | Declaración de jul-2025, sin año exacto | No publicada; cifra redondeada de cámaras | FTE-021 |
| ~1.000 M | Pollos proyectados para 2023 | Proyección | A partir de reproductoras alojadas | FTE-022 |
| 18,2–20 M/semana | **Pollitos BB parrilleros** producidos (≈ 946–1.040 M/año) | Proyección 1S-2025 / 1S-2026 | A partir de reproductoras en postura | FTE-071 |
| 5–10 % | Participación de la faena provincial/municipal en el total | Sin año | Dos estimaciones distintas (BolsaCBA, DNCCA) | FTE-072 |

- Si la faena no federal fuera 5–10 %, la faena total sería ~790–830 M, no 900 M ni ~1.000 M.
- Los pollitos BB (~946 M/año en 2025) menos una mortalidad típica dejarían ~150–200 M aves sin faena SENASA registrada `[ESTIMACIÓN]`. Eso **contradice** el 5–10 %.
- Hipótesis no verificadas: el Anuario tal vez proyecte pollitos con parámetros teóricos (sin descontar descartes); la cifra de 900 M podría incluir categorías no comparables o redondeos; o la faena no federal y la informal están subregistradas.

**Conclusión:** la magnitud de la faena fuera de SENASA es una **inconsistencia estadística pendiente** (DPV-011, DPV-021). No se usa ningún valor para decisiones. Solo se afirma, `[PVDP]`, que existen plantas provinciales y municipales (>20 según FTE-072) y que su peso relativo es incierto.

### 1.3 Producción (toneladas)

| Año | Producción (t) | Base / fuente | Estado |
|---|---|---|---|
| 2019 | ~1.831.000 (12 meses; período a confirmar) | FTE-060 | [PVDP · débil] |
| 2021 | 2.318.000 | CEPA, incluye faena sin tránsito federal (FTE-023) | [PVDP] |
| 2022 | 2.320.000 (CEPA: 2.450.000) | BCR (FTE-026) / CEPA (FTE-022) | [PVDP] / [PVDP · débil] |
| 2023 | ~2.287.000 (BCR: ~2.500.000) | derivado de SAGyP (FTE-002) / BCR (FTE-025) | [ESTIMACIÓN] / [PVDP · débil] |
| 2024 | 2.304.000 | SAGyP (FTE-002) | [PVDP] |
| 2025 | **~2.300.000** (SAGyP, +2,2 %); CEPA: 2.470.000 | FTE-070 / FTE-020 | [PVDP] / [PVDP · débil] |
| 2025 ene–may | 958.000 (+1,9 %) | SAGyP (FTE-070) | [PVDP] |
| 2026 | 2.580.000 (pronóstico USDA de 2025, anterior al brote de feb-2026 y a la crisis de GTA) | FTE-018 | Pronóstico; probablemente sobreestimado |
| 2026 (a mar.) | −5,9 % interanual | Datos oficiales citados por CEPA (FTE-031) | [PVDP · débil] |

- **Diferencia SAGyP vs CEPA en 2025:** unas 170.000 t (~7 %). Se adopta **SAGyP** por ser la fuente oficial y coherente con la serie 2024 (+2,2 % sobre 2,304 Mt ≈ 2,35 Mt; el "~2,3" publicado sería un redondeo).
- **Tendencia:** +16 % entre 2012 y 2022, ~1 % anual (FTE-026). El crecimiento viene del mayor peso por ave. El salto 2019→2021 probablemente sea metodológico.
- **Datos parciales 2026:** solo hay la variación a marzo (−5,9 %). La SAGyP publica un tablero de faena 2026 que no fue accesible (DPV-010).

### 1.4 Consumo interno

| Año | SAGyP | BCR | SSPM | CEPA / Cincap | USDA | Otras |
|---|---|---|---|---|---|---|
| 2004 | — | — | 21,6 | — | — | — |
| 2019 | — | — | — | — | — | 43 [débil] |
| 2020 | — | — | — | — | — | 44 [débil] |
| 2021 | — | — | — | >46 [débil] | — | — |
| 2022 | — | — | — | ~47 [débil] | — | — |
| 2024 | **46,25** | 45,2 | 44,8 | ~48,5 [ESTIMACIÓN] | — | — |
| 2025 | **47,68** | 46,8 | — | 49,4 | 48 | 47,6 (El Economista) |
| 2026 (proyección CEPA) | — | — | — | >50 | — | — |

Unidades: kg/hab/año. Fuentes: FTE-003, FTE-024, FTE-027, FTE-007, FTE-020, FTE-030, FTE-018, FTE-051, FTE-077. Estado general: [PVDP].

- **Serie de referencia:** SAGyP (SUP-008). CEPA opera como cota superior.
- **Consumo aparente total:** ~2,1 Mt (2022), 2,13 Mt (2023), 2,1 Mt (2024); ene–ago 2025: 1,4 Mt (+2 %) `[PVDP]`.
- **Madurez:** el consumo per cápita se duplicó entre 2004 y 2024, pero hoy crece ~1–1,5 kg/año y la faena está estancada. El sector habla de un "techo" de demanda interna (FTE-034, FTE-051).

### 1.5 Pollo frente a carne vacuna y porcina

| Carne | 2024 (kg/hab) | 2025 (kg/hab) | Var. | Participación 2025 [ESTIMACIÓN] |
|---|---|---|---|---|
| Vacuna | 48,49 | 49,92 | +2,9 % | 42,9 % |
| Aviar | 46,25 | 47,68 | +3,1 % | 40,9 % |
| Porcina | 17,42 | 18,89 | +8,4 % | 16,2 % |
| **Total** | **112,16** | **116,4** | +3,8 % | 100 % |

Fuente: SAGyP (FTE-003) [PVDP]. En 2023: 46 % bovina, 39 % aviar, 15 % porcina (FTE-063).

- Según SAGyP, en 2025 el pollo quedó **prácticamente empatado** con la carne vacuna. La afirmación de que "ya la superó" depende de usar la serie de CEPA.
- En el 1S-2026 la oferta interna de carne vacuna cayó −11,5 % (CICCRA, FTE-061) [PVDP · débil]. El asado cuesta 3,5 veces el precio del pollo entero (§7). La **sustitución** favorece al pollo, pero depende del ciclo ganadero.

### 1.6 Exportaciones e importaciones (resumen)

Detalle en [`exportaciones.md`](exportaciones.md).

- **Exportaciones** [PVDP]: 2022: 230 mil t / USD 401 M · 2023: 160,6 mil t / USD 180,4 M · 2024: 185,8 mil t / USD 222,2 M (comestibles) · 2025: 206,4 mil t / USD 246,9 M (definición amplia). Ene–jul 2025: 103.454 t (−4,9 %). 2026 a marzo: −21,7 % en volumen.
- **Importaciones** [PVDP] (INDEC vía FTE-075): ene–jul 2025 **12.951 t (+295 %)** vs 3.282 t en ene–jul 2024; ago-2025, récord mensual de 4.360 t (USD 11,6 M); 2024: ~4.000 t desde Brasil. Productos: pechuga, CMS y cocidos/prefritos (FTE-031). Una cifra de "44.000 t ene–ago" se **descartó** por ser incompatible con los datos mensuales. Representan ~1 % del consumo `[ESTIMACIÓN]`, pero concentrado en cortes de mayor valor (pechuga) y en elaborados.
- **Suspensión sanitaria** a Brasil desde 2025-05-16 (FTE-053). El crecimiento de importaciones durante 2025 indica que la suspensión se levantó o fue parcial; fecha no identificada (DPV-014).

### 1.7 Contexto internacional

USDA (FTE-019) [PVDP]: producción mundial de carne de pollo de 110,7 Mt en 2026 y exportaciones mundiales de ~14,8 Mt (récord). Brasil es el primer exportador y China acelera sus exportaciones. Argentina aporta ~2,3 % de la producción mundial `[ESTIMACIÓN]` y es un exportador menor.

---

## 2. Cadena de valor

### 2.1 Flujo y nivel típico de integración

```
Genética (abuelas, importadas) → Reproductoras padres → Huevo fértil → Incubación → Pollito BB
                                                                                        ↓
Alimento balanceado (maíz + harina de soja + núcleo) ───────────────→ Granja de engorde (integrado)
                                                                                        ↓
                          Captura y transporte vivo → Frigorífico (faena) → Trozado / elaborados / subproductos
                                                                                        ↓
       Distribución con frío → Supermercado / mayorista / pollería / gastronomía / industria → Consumidor / exportación
```

| Eslabón | Funcionamiento en Argentina | Control habitual | Evidencia |
|---|---|---|---|
| Genética (abuelas) | Líneas Cobb, Ross (Aviagen) y Hubbard, importadas a nivel abuelas. Se estima que ~66 % depende de la genética producida en Santa Elena (ER) por Reproductores Cobb SA [PVDP · débil]. | Pocas empresas globales y sus socios locales | FTE-049, FTE-038 |
| Reproductoras / huevo fértil | ~5,2 M reproductoras en postura (1S-2025) y ~5,8 M (1S-2026) [PVDP]. Otro extracto cita 9,4 M "en producción": probablemente otro universo (alojadas). | Integradores; algunos proveedores independientes | FTE-071, FTE-001 |
| Incubación → pollito BB | ~18–20 M pollitos BB parrilleros/semana [PVDP]. Ej.: Fadel ~1,2 M huevos/semana. | Integradores | FTE-071, FTE-045 |
| Alimento balanceado | Maíz + soja. El sector consume ~5 Mt de maíz y 2,1 Mt de complejo soja por año, sumando pollo y huevo [PVDP · débil]. Es el mayor rubro de costo del vivo (se cita 65–70 %; a validar con el ICPP). | Integradores con planta propia (Las Camelias abastece ~220 granjas desde su planta de Villaguay) | FTE-077, FTE-006, FTE-081 |
| Engorde | **Sistema integrado:** el integrador provee pollito, alimento y asistencia; el productor aporta galpones, trabajo y energía. Crianza de 46–50 días hasta ~3 kg vivo. Pago por ave (~$700–800 en 2026 según prensa); frecuentemente sin contrato formal; cobro a ~60 días. | Productor integrado | FTE-050, FTE-051 |
| Faena y procesamiento | Plantas de 80.000 a >200.000 aves/día en las empresas medianas y grandes | Integrador | FTE-043 a FTE-046 |
| Subproductos | Harinas de plumas y vísceras; menudos y garras | Integrador | FTE-038, FTE-020 |
| Distribución y venta | Frío hasta supermercados, mayoristas, pollerías, gastronomía y locales propios | Integrador y distribuidores | FTE-047 |

### 2.2 Qué suele estar integrado

- **Núcleo integrado** (~40 integradoras, FTE-066; descripción del modelo en FTE-062): reproductoras, incubación, alimento, faena y distribución.
- **Tercerizado por contrato:** el engorde en granjas de productores integrados. Es frágil: GTA perdió entre 60 % y 85 % de sus integrados según la fuente (FTE-080, FTE-036).
- **Nunca local:** la genética de abuelas.
- **Implicancia:** el modelo dominante es **integrador + productores integrados**. Una empresa escalable necesita, tarde o temprano, controlar el flujo de pollito y alimento. El engorde puede apoyarse en terceros.

---

## 3. Geografía productiva

### 3.1 Tabla provincial

No hay una serie pública de producción primaria por provincia. Se usa la faena SENASA y los datos disponibles de establecimientos.

| Provincia | % faena SENASA 2025 | Plantas de faena (habilitación nacional, s/f) | Producción primaria (dato disponible) | Principales ventajas | Principales desventajas |
|---|---|---|---|---|---|
| **Entre Ríos** | 50,2 % (CEPA: 50,39 %); 378 M cab | 23 | 54 %–62,9 % de las granjas de parrilleros del país (fuentes en conflicto); >6.500 galpones; ~2.500 granjas; 73 % de las granjas en predios <10 ha | Cluster completo (genética, incubación, alimento, integrados, plantas, servicios, mano de obra). Puertos sobre los ríos Uruguay y Paraná. | Lejos del AMBA. Concentración sanitaria. Competencia por integrados y personal. |
| **Buenos Aires** | 35,4 % (CEPA: 35,47 %) | s/d | s/d | Cercanía al mayor mercado (AMBA, donde está la carnicería y, aparentemente, gran parte de la red de supermercados). Acceso a granos y puertos. | Brotes de IAAP de 2025 y 2026 en BA (Ranchos). Presión urbana y ambiental. Costos laborales y conflictividad (cierres de GTA). |
| **Santa Fe** | 5,1 % (CEPA: 4,8 %) | 6 | s/d | Zona núcleo de granos. Caso de integración hasta el minorista (Grupo Cem). | Menor densidad de proveedores avícolas. |
| **Córdoba** | 4,1 % | 4 | s/d | Maíz abundante. Complejo Avex (Río Cuarto). | IAAP 2026 en ponedoras. Avex cedida a ACA y en concurso. Lejos de puertos. |
| **Chaco** | Sin participación relevante en la faena SENASA publicada (queda dentro del 2,7 % "resto" o fuera) | s/d | s/d | Producción de granos. Menor densidad avícola, lo que puede significar menor presión sanitaria (hipótesis no verificada). El contacto personal del promotor es una ventaja cualitativa (SUP-014). | Sin cluster avícola conocido; lejos de AMBA y de los puertos exportadores avícolas; proveedores de genética y pollito lejanos. **Datos insuficientes: requiere relevamiento específico** (DEC-003). |
| Río Negro | 2,5 % | s/d | s/d | Abastecimiento patagónico | Lejos de granos |
| Salta, Mendoza, La Rioja, Jujuy | ~2,7 % en conjunto | s/d | s/d | Mercados regionales protegidos por el flete | Escala limitada |

Fuentes: FTE-001, FTE-020, FTE-048, FTE-072, FTE-073, FTE-074, FTE-040, FTE-057 [PVDP]. Las ventajas y desventajas son análisis propio.

**Establecimientos a nivel país** [PVDP · débil]: 69 plantas de faena con habilitación SENASA (17 suspendidas o inactivas) y >20 con habilitación provincial o municipal (FTE-072, año no identificado); otra fuente cita 101 plantas (55 + 46). ">2.000 establecimientos avícolas" en todo el país (FTE-086) es **incompatible** con ~2.500 granjas solo en ER: contradicción abierta (DPV-023).

### 3.2 Clusters

| Cluster | Localidades | Actores |
|---|---|---|
| Corredor del río Uruguay (ER), con la mayor concentración industrial (departamentos Colón, Uruguay y Gualeguaychú, FTE-072) | Concepción del Uruguay, San José, Colón/Pronunciamiento, Villa Elisa, Santa Elena | GTA (La China, cerrada en may-2026), Fepasa, Las Camelias, Fadel, Noelma, Reproductores Cobb |
| Paraná / sur de ER | Gualeguay, Hernandarias, Villaguay | Soychú, Indavisa, Las Camelias (Villaguay) |
| Conurbano norte y oeste (BA) | Pilar, Capitán Sarmiento, Esteban Echeverría | Plantas de GTA (paralizadas desde ago-2026) |
| Centro de Santa Fe | Esperanza, Humboldt | Grupo Cem |
| Sur de Córdoba | Río Cuarto | Avex (GTA → ACA) |

La localización del proyecto **no se decide aquí** (DEC-003).

---

## 4. Principales empresas (resumen)

Detalle en [`competidores.md`](competidores.md), donde se separan hechos y posibles implicancias.

| Empresa | Base | Escala pública aproximada [PVDP · débil salvo indicación] | Integración | Situación 2026 |
|---|---|---|---|---|
| Grupo GTA (Granja Tres Arroyos, Wade/ex Cresta Roja, Avex, HAISA) | BA, ER, Cba, Uruguay | 670.000 aves/día (2024), 610.000 (2025), ~200.000 (ago-2026) | Total | **Concurso preventivo** (expte. COM 018558/2026) [PVDP] |
| Soychú | Gualeguay (ER) | ~200.000 aves/día; ~12 % de la faena (2021) | Integrada | Sin evidencia de crisis |
| Las Camelias | San José (ER) | ~500 t/día; ~6,9 % (2021); ~220 granjas propias o integradas | Integrada | Invierte (>USD 6 M en Villaguay) |
| Noelma | Villa Elisa (ER) | >150.000 aves/día | Integrada | s/d |
| Fadel | Colón (ER) | ~160.000 aves/día | Integrada | s/d |
| Fepasa | C. del Uruguay (ER) | ~80.000 aves/día | Faena y trozado | s/d |
| Grupo Cem | Esperanza (SF) | ~600.000 pollos/mes; >100 locales propios | Del grano al minorista | s/d |

**Concentración:** 10 integradoras concentran >50 % de la capacidad (CEPA, FTE-020) [PVDP]. La participación de GTA tiene cifras **inconsistentes** entre fuentes (desde 20 % hasta 35 %; §13) y no se usa ninguna como dato.

---

## 5. Productos y aprovechamiento del ave

### 5.1 Clasificación de productos

| Producto | Tipo | Evidencia | Potencial exportador |
|---|---|---|---|
| Pollo entero eviscerado (fresco/refrigerado) | **Commodity** | Producto gancho de supermercados (promociones de $1.999 a $2.700/kg en sept-2025, FTE-052) | Medio (23,7 % del volumen exportado en 2025, congelado) |
| Pollo entero congelado | Commodity | Válvula de excedentes y exportación | Sí |
| Pata-muslo, alas | Commodity / diferenciable | Trozados: 37,2 % del volumen exportado | Sí (China: alas y pata-muslo) |
| Pechuga / supremas / filet | **Mayor valor interno** | Brasil exporta pechuga a Argentina (FTE-031) | Bajo a medio |
| Menudencias | Subproducto comestible | Bajo valor interno | Sí (África, Asia) |
| **Garras / patas** | **Bajo valor interno, alto valor externo** | Producto clave para China (FTE-014) | Alto, **condicionado a China** (cerrada en 2026) |
| Recortes / CMS | Insumo industrial | Se importa CMS de Brasil (FTE-031) | Bajo |
| Marinados, milanesas, hamburguesas, nuggets, prefritos | **Valor agregado** | Importación brasileña de prefritos (FTE-031). Solo 1,6 % del volumen exportado. | Bajo hoy |
| Harinas de plumas y vísceras | Subproducto no comestible | Parte del 4,6 % de "alimento balanceado" exportado | Medio |

### 5.2 Principio estratégico: ingreso total por ave

Registrado como principio en `CLAUDE.md` y en SUP-013. El desarrollo conceptual y los mercados por parte del ave están en [`exportaciones.md` §7](exportaciones.md). En síntesis:

- Un ave no es un producto: es un **conjunto de partes con precios distintos en mercados distintos**. El mismo pollo puede generar pechuga para el mercado interno o la gastronomía, pata-muslo para supermercado o exportación, alas para Asia, garras para China, menudencias para África, recortes para la industria y harinas para alimento animal.
- **Objetivo económico:** maximizar el ingreso total por ave (Σ kg de cada parte × precio del mejor mercado accesible − costos de separación, frío y logística), no maximizar las toneladas de pollo entero.
- **Condiciones:** capacidad de trozado, frío, habilitaciones por destino (sobre todo exportación) y canales para cada parte. Sin salida para garras o menudencias, esas partes valen poco o generan costo.
- La cuantificación (rendimientos por parte y precios) corresponde al balance de masa (`04_balance_masa`) y a la sesión de estrategia exportadora. **No se estima aquí.**

---

## 6. Canales comerciales

### 6.1 Importancia relativa

**No existe una serie pública de ventas de pollo por canal** (DPV-012). Evidencia disponible:

| Canal | Evidencia | Importancia (cualitativa) | Nivel de evidencia |
|---|---|---|---|
| Supermercados de cadena | ~40 % del volumen de consumo masivo general, no específico de pollo (FTE-054). Usan el pollo entero como gancho (FTE-052). | Alta | Indirecta |
| Autoservicios independientes y "chinos" | 16 % del consumo masivo general (FTE-054) | Media | Indirecta |
| Pollerías y carnicerías | Canal clásico de fresco y trozado; comercios tradicionales: 32 % del consumo masivo (FTE-054) | Alta en fresco y trozado | Indirecta |
| Mayoristas y distribuidores | Abastecen al canal tradicional y a la gastronomía | Media–alta | Cualitativa |
| Gastronomía | Trozados, porcionados, elaborados | Media | Sin dato |
| Industria alimenticia | CMS y cortes industriales, en parte importados | Baja–media | Cualitativa |
| Locales propios | Modelo Grupo Cem | Nicho / modelo | Caso |
| Exportación | ~7–8 % del volumen; clave para subproductos (garras) y para colocar excedentes | Baja en volumen, alta en valor por parte | [PVDP] |

### 6.2 Rol de la red de ~90 supermercados

**Situación registrada** (SUP-004, DPV-018): *"Red potencial de aproximadamente 90 supermercados, aparentemente concentrada principalmente en AMBA, pendiente de validación."* No se sabe si es una única cadena o varias sociedades, ni se conocen la distribución por municipio, los centros de distribución, el volumen de compra, el proveedor actual (DPV-020) ni si alguna vez le compró a GTA (no se asume ninguna relación).

**Posibles funciones de la red** (todas condicionadas a validación):

| Función | Qué aportaría | Límite |
|---|---|---|
| Cliente ancla inicial | Volumen base para los primeros años; reduce el riesgo comercial | No define la escala final |
| Canal para ciertos cortes | Salida para pata-muslo, pechuga, entero fresco y elaborados en AMBA | Las garras, menudencias y excedentes requieren otros canales |
| Fuente de información | Datos reales de mix, precios y rotación | — |
| Mitigador de riesgo | Menor costo de conquista comercial | Riesgo de concentración en un solo cliente |

**Riesgos del canal:** poder de negociación (pollo entero como gancho); plazos de pago frente a un producto perecedero (**capital de trabajo**); dependencia de un cliente; exigencia de continuidad diaria; competencia de precios en sobreoferta. Como la red estaría en AMBA y la eventual planta podría estar en otra provincia, **probablemente se requiera tránsito federal SENASA** (DEC-009; a confirmar según la localización).

**Posicionamiento:** en una empresa escalable con vocación exportadora, la red de supermercados sería **uno de varios canales** junto con mayoristas, gastronomía, industria, elaborados y exportación. La escala se define por el conjunto de canales y por el ingreso total por ave, no por la red (`CLAUDE.md`, regla 8).

---

## 7. Precios

### 7.1 Precios relevados

| Nivel | Producto | Fecha | Valor | Unidad | Moneda / TC | Fuente | Estado |
|---|---|---|---|---|---|---|---|
| Productor | Pollo parrillero vivo | semana 2026-07-06 | 2.528 | $/kg vivo | ARS (≈ USD 1,70 a mayorista 1.488,50) | FTE-029, FTE-055 | [PVDP · débil] |
| Mayorista | Pollo eviscerado, cajón 20 kg, sin IVA | ene-2025 / ene-2026 | 1.742,1 / 2.847,5 | $/kg | ARS | FTE-004 | [PVDP] |
| Mayorista | Variación interanual feb–jun 2026 | 2026 | +50,5 / +24,8 / +15,7 / +27,2 / +17,4 | % | — | FTE-004 | [PVDP · débil] |
| Consumidor | Pollo entero, GBA | ago-2026 | 4.780,14 | $/kg con IVA | ARS (≈ USD 3,16 a mayorista 1.514 / 3,10 MEP) | FTE-008, FTE-055 | [PVDP] |
| Consumidor | Asado / nalga / cuadril / picada | ago-2026 | 16.736,73 / 21.763,38 / 21.102,92 / 10.613,08 | $/kg | ARS | FTE-008 | [PVDP] |
| Consumidor | Entero en promoción (Coto, Vea, Día, Carrefour) | probable sept-2025 | 1.999 / 2.300 / 2.600 / 2.700 | $/kg | ARS | FTE-052 | [PVDP · débil] |
| Integrado | Pago por ave criada | 2026 | 700–800 | $/ave | ARS | FTE-051 | [PVDP · débil] |
| Exportación | Carne aviar promedio | ene / feb-2026 | 1.056 / 1.050 | USD/t FOB | USD | FTE-032 | [PVDP · débil] |
| Exportación | Promedio anual 2022 / 2023 / 2024 / 2025 | anual | 1.743 / 1.123 / 1.196 / 1.196 | USD/t FOB | USD | derivado | [ESTIMACIÓN] |
| Importación | Carne aviar, agosto 2025 | ago-2025 | ~2.660 | USD/t | USD (11,6 M / 4.360 t) | FTE-075 | [ESTIMACIÓN] |

### 7.2 Lectura

- **Precio relativo:** 1 kg de asado equivale a 3,5 kg de pollo entero (ago-2026) `[ESTIMACIÓN]`.
- **Importación vs exportación:** el producto importado ingresa a ~2.660 USD/t (ago-2025) y lo exportado sale a ~1.050–1.200 USD/t `[ESTIMACIÓN]`. Es coherente con que se **importan cortes de alto valor** (pechuga, elaborados) y se **exportan cortes y subproductos de menor valor**. Es un argumento a favor del principio de ingreso total por ave.
- **Volatilidad:** los cierres de exportación generan sobreoferta y ventas bajo costo (FTE-052).
- **Inconsistencia vivo vs mayorista:** sin resolver (DPV-013). No usar ambos precios juntos.
- **Series faltantes:** no hay precios públicos por corte ni precios de proveedor a supermercado (DPV-013, DPV-020).

---

## 8. Exportación (resumen)

Ver [`exportaciones.md`](exportaciones.md). Estado al 2026-09-29, con las cuatro categorías de la regla 17:

- **Habilitados sanitariamente, con evidencia 2026:** UE (desde 2026-08-17), Chile y Perú (jun-2026), Japón (aves faenadas desde 2026-09-08).
- **Exportación efectiva documentada 2025:** Vietnam, Sudáfrica, Chile, China (antes del cierre), RD del Congo, entre otros (76 países).
- **Cerrado o suspendido:** China, al menos hasta julio de 2026 (el sector pedía apoyo político para reabrirla; FTE-076). No hay evidencia de reapertura a la fecha.
- **Potenciales:** cuota UE–Mercosur (180.000 t para el bloque); mercados Halal (Arabia Saudita, EAU y otros) que requieren certificación.

---

## 9. Competencia y barreras de entrada

### 9.1 Estructura

Oligopolio con franja competitiva: 10 integradoras concentran >50 % de la capacidad (FTE-020), unas 40 integradoras en total y un segmento de plantas provinciales y municipales de peso incierto (§1.2). El líder histórico (GTA) está en concurso; en 2014 ya había caído el segundo actor (Rasic/Cresta Roja, FTE-067).

### 9.2 Barreras

| Barrera | Intensidad para un entrante |
|---|---|
| Economías de escala (plantas de 80.000 a >200.000 aves/día) | Alta |
| Integración vertical (genética, pollito, alimento) | Alta |
| Acceso a granos (alimento: mayor rubro de costo) | Media |
| Acceso a clientes (góndola concentrada, pollo como gancho) | Alta; mitigable con la red si se valida |
| Bioseguridad (IAAP recurrente) | Alta |
| Habilitaciones (SENASA federal, listados de exportación, Halal, ambiental). Decreto 4238/68 y Res. SENASA 592/2026 y 593/2026 (FTE-016, FTE-083). | Alta |
| Frío y logística | Media–alta |
| Capital de trabajo (~50 días de crianza + plazos de clientes) | **Alta** |
| Red de productores integrados (renovar ~1.200 galpones de ~USD 300.000 c/u, según el sector, FTE-043) | Alta |
| Competencia importada en pechuga y elaborados | Media, creciente |

### 9.3 Por qué una empresa nueva puede fracasar aun teniendo capital

1. El capital no compra costo competitivo ni escala instantánea en un commodity de márgenes finos. GTA tenía escala, integración total y un socio global, y aun así entró en concurso.
2. El mercado interno está maduro: el volumen nuevo desplaza al existente y obliga a competir por precio.
3. Shocks sanitarios exógenos (3 eventos de IAAP en 4 años) cierran exportaciones y deprimen precios internos.
4. Se subestima el capital de trabajo.
5. Dependencia de insumos (pollito, genética) provistos por competidores.
6. Un canal sin contrato no es demanda.
7. El tipo de cambio y las importaciones ponen un techo a los precios de cortes de valor.
8. Si se vende pollo entero en lugar de valorizar cada parte, se deja ingreso sobre la mesa.

---

## 10. Oportunidades

Solo se incluyen oportunidades con justificación. Todas requieren validación.

| Ámbito | Oportunidad | Justificación | Condición |
|---|---|---|---|
| Mercado local | Demanda interna grande y sustitución de carne vacuna | Consumo de 47–49 kg/hab; oferta vacuna −11,5 % en 1S-2026 | Sin crecimiento de volumen fuerte: hay que ganar participación |
| Mercado local | Reconfiguración de la oferta en 2026 | La faena de GTA cayó ~400.000–500.000 aves/día [PVDP · débil] | **Solo evento de mercado.** No se asume disponibilidad de activos, integrados, capacidad a façon ni clientes (DPV-016) |
| Supermercados | Red de ~90 bocas (AMBA) como cliente ancla | Reduce la barrera comercial | Validar volumen, proveedor actual, precios, plazos y contratos (DPV-002, 003, 020) |
| Mayor valor | Pechuga, porcionados, marinados y elaborados | Se importan a ~2.660 USD/t; el mercado interno los demanda | Planta con trozado y elaborados; precios por corte (DPV-013) |
| Subproductos | Garras, menudencias, harinas | ~33 % del volumen exportado en 2025 son menudos, garras y subproductos | Garras: depende de China. Resto: habilitación y canal. |
| Exportación | UE (reabierta; cuota UE–Mercosur), Japón, Chile, Perú; mercados Halal | Acceso vigente en 2026 | Habilitación federal, listados, certificación Halal, competitividad frente a Brasil |
| Integración vertical | Integración progresiva (canal → faena → incubación y alimento) | Todos los actores relevantes están integrados | Evaluar eslabón por eslabón (DEC-002) |
| Nichos | Plantas regionales con habilitación provincial | Existen >20 plantas provinciales o municipales | Limita a una provincia e impide exportar; peso del segmento incierto |

**No justificadas por falta de evidencia:** pollo premium u orgánico, crecimiento fuerte del consumo per cápita, "compra de activos de GTA" como estrategia.

---

## 11. Amenazas

| Amenaza | Evidencia | Impacto | Frecuencia |
|---|---|---|---|
| **Influenza aviar (IAAP)** | 2023, ago-2025, feb-2026 (Ranchos, BA, en granja de reproductoras; 3 casos comerciales en 2026); estatus recuperado en abr-2026 | Muy alto | Alta |
| Newcastle | País libre (FTE-015) | Muy alto si aparece | Baja |
| Salmonella / micoplasma | Programa SENASA | Medio–alto | Media |
| Maíz y soja | ~5 Mt de maíz por año en el sector | Alto | Alta |
| Tipo de cambio | Apreciación → importaciones más baratas | Alto | Media–alta |
| Inflación | Mayorista +63,5 % interanual (ene-2026) | Medio | Alta |
| Energía | Gas en granjas; problemas de suministro invocados por GTA | Medio | Media |
| Dependencia exportadora del sector | Los excedentes presionan el mercado interno | Alto | Alta |
| Barreras sanitarias | China cerrada; listados por planta | Alto | Alta |
| Competencia e importaciones | Importaciones +295 % en 2025 | Alto | Alta |
| Sobrecapacidad | Plantas paralizadas que pueden reactivarse | Alto | Media–alta |
| Dependencia de clientes | Riesgo si la red de supermercados pesa demasiado | Alto | Según diseño |
| Capital de trabajo | Ciclo de ~50 días + plazos | Alto | Alta |
| Conflictividad laboral | Cierres de plantas de GTA | Medio–alto | Media |

---

## 12. Conclusiones

Ver [`conclusiones_mercado.md`](conclusiones_mercado.md).

---

## 13. Control de calidad (versión 2)

### 13.1 Contradicciones y resolución

| Tema | Valores en conflicto | Causa probable | Resolución |
|---|---|---|---|
| **Producción 2025** | 2,3 Mt (SAGyP vía BCR) vs 2,47 Mt (CEPA) | Metodología / base distinta | **SAGyP** (oficial). CEPA queda como referencia sectorial. En la versión 1 se usaba CEPA: **corregido**. |
| **Brecha de faena** | 750 M (SENASA) vs ~900 M (sector) vs ~946–1.040 M pollitos BB vs 5–10 % no federal | Universos, períodos y metodologías distintos | **Conclusión de la versión 1 (150 M no federal) retirada.** Inconsistencia pendiente (DPV-011, DPV-021). |
| Consumo per cápita 2025 | 46,8 / 47,6–47,68 / 48 / 49,4 kg | Metodologías | SAGyP 47,68 |
| Faena 2023 | 740,5 vs 734,5 M | Preliminar vs definitivo | 740,5 |
| Producción 2022 y 2023 | BCR/SAGyP vs CEPA | Base distinta | SAGyP/BCR |
| Exportación 2025 | 206.436 t (CEPA, amplia) vs 169.000 t (sin fuente) | Definición | CEPA como total; la cifra comestible queda pendiente |
| Importaciones ene–ago 2025 | 44.000 t vs 12.951 + 4.360 = 17.311 t | Error de extracto o de definición | **44.000 t descartada** |
| Reproductoras | 9,4 M vs 5,2–5,8 M | Alojadas vs en postura (probable) | Usar 5,2–5,8 M "en postura" |
| Establecimientos | >2.000 en el país vs ~2.500 granjas solo en ER | Universos o fechas distintas | Contradicción abierta (DPV-023) |
| % de granjas en ER | 54 % vs 62,9 % | Fechas distintas | Rango 54–63 % |
| **Participación de GTA** | "~35 %", "~25 %", ">20 % de t", "3,7–3,8 %" | Distintos momentos y bases; el 3,7 % es probablemente un error del extracto | Ninguna se usa. Estimación propia 2025: ~20 % (610.000 aves/día × 250 días / 750 M) `[ESTIMACIÓN]` |
| Deuda de GTA | USD 350,9 M (GTA) vs >USD 540 M (4 sociedades); pasivo declarado $536.000 M | Perímetro societario | Se informan las tres con su perímetro |
| Integrados perdidos por GTA | 60 % (mar-2026) vs 85 % vs "~120 productores" | Fechas distintas | Se informa el rango; no se usa como dato |
| Brote ago-2025 | 20-ago (suspensión) vs 26-ago (USDA) | Evento distinto | "Agosto 2025" |
| Importación +122 % | Corresponde a carne vacuna | Confusión de producto | Descartado |

### 13.2 Controles

- **Años:** cada cifra indica su año o período.
- **Unidades:** t, kg/hab, cabezas, USD FOB, ARS con o sin IVA.
- **Producción ≠ faena ≠ pollitos BB ≠ consumo:** se tratan por separado (regla 18).
- **Habilitado ≠ exportado ≠ potencial ≠ cerrado:** en [`exportaciones.md`](exportaciones.md).
- **Verificación primaria:** 0 cifras verificadas contra el original (acceso bloqueado). Todas son `[PVDP]` o `[PVDP · débil]`.
