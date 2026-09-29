# Mercado de carne aviar en Argentina — radiografía 2026

**Fecha de referencia:** 2026-09-29 · **Fase:** 0 (prefactibilidad) · **Carpeta:** `01_mercado`

Documento base del relevamiento de mercado. Documentos asociados:

- Datos numéricos con fuente y clasificación: [`datos_mercado.csv`](datos_mercado.csv) (IDs `M###`).
- Empresas: [`competidores.md`](competidores.md).
- Comercio exterior y acceso a mercados: [`exportaciones.md`](exportaciones.md).
- Conclusiones para el proyecto: [`conclusiones_mercado.md`](conclusiones_mercado.md).
- Fuentes (IDs `FTE-###`): [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv).

> **Restricciones de fase:** este documento no recomienda montos de inversión, maquinaria, terreno ni capacidad de faena (ver [`estado_proyecto.md`](../00_gestion_proyecto/estado_proyecto.md)).

---

## 0. Alcance, método y limitaciones

### 0.1 Limitación principal de esta versión

Durante la sesión, la política de red del entorno **bloqueó el acceso directo** a los documentos primarios (magyp.gob.ar, argentina.gob.ar, indec.gob.ar, fas.usda.gov, bcr.com.ar y otros). Toda cifra se obtuvo mediante **extractos de buscador** de documentos identificados (título, organismo y URL registrados). En consecuencia:

- Toda cifra conserva la fuente de origen (`FTE-###`), pero su **verificación documental directa queda pendiente** ([DPV-009](../00_gestion_proyecto/datos_por_validar.md)).
- Se etiqueta `[VERIFICADO]` solo cuando la fuente es identificable, confiable (A o B) y la cifra es coherente con otras. Si no, se etiqueta `[PENDIENTE DE VALIDACIÓN]`.
- Los cálculos propios se etiquetan `[ESTIMACIÓN]` y se explica el método.
- Se descartó toda cifra que el buscador pudo haber "eco-repetido" de la consulta.

### 0.2 Definiciones que se usan en todo el documento

| Concepto | Definición | Por qué importa |
|---|---|---|
| **Faena SENASA** | Aves faenadas en plantas con habilitación de SENASA (tránsito federal). Es la serie oficial de cabezas. | **No** es la faena total: existen plantas con habilitación provincial o municipal. |
| **Faena total** | SENASA más plantas provinciales y municipales. No hay serie pública consolidada. | Las cámaras declaran ~900 M de pollos, contra ~750 M de faena SENASA (ver §1.2). |
| **Producción (t)** | Toneladas de carne aviar. SAGyP la estima con faena nacional, provincial y municipal más avimetría ([FTE-002](../25_fuentes/registro_fuentes.csv)). | Distintas fuentes usan bases distintas. **No se debe dividir producción por faena SENASA para obtener kg por ave.** |
| **Consumo aparente** | Producción + importaciones − exportaciones (± stock). Per cápita: dividido por población. | Varía según la metodología de cada fuente (ver §13). |
| **Exportaciones** | Algunas fuentes cuentan solo "productos comestibles"; CEPA incluye además subproductos y alimento balanceado. | Explica las diferencias entre 169 mil, 185 mil y 206 mil t (ver §13). |

---

## 1. Tamaño del mercado

### 1.1 Magnitudes clave 2025

| Indicador | Valor 2025 | Unidad | Fuente | Clasificación |
|---|---|---|---|---|
| Faena en plantas SENASA | 750,2 | millones de cabezas | FTE-001, FTE-020 | [VERIFICADO] |
| Faena total declarada por el sector | ~900 | millones de pollos | FTE-021 | [PENDIENTE DE VALIDACIÓN] |
| Producción de carne aviar | 2,47 | millones de t | FTE-020 (CEPA) | [VERIFICADO] |
| Consumo per cápita (serie de referencia SAGyP) | 47,68 | kg/hab/año | FTE-003 | [VERIFICADO] |
| Consumo per cápita (rango entre fuentes) | 46,8 – 49,4 | kg/hab/año | FTE-027, FTE-030 | [VERIFICADO] |
| Exportaciones (definición amplia CEPA) | 206.436 | t | FTE-020 | [VERIFICADO] |
| Exportaciones (valor, definición amplia) | 246,9 | millones USD FOB | FTE-020 | [VERIFICADO] |
| Destino mercado interno (2024) | 93 | % de la producción | FTE-007 | [VERIFICADO] |
| Participación mundial en producción (2026, USDA) | ~2,3 | % | FTE-018, FTE-019 | [ESTIMACIÓN] |

**Lectura:** Argentina es un mercado **grande y maduro, orientado al consumo interno**. Exporta alrededor del 7–8 % de lo que produce. Tiene uno de los consumos per cápita de pollo más altos del mundo: la prensa lo ubica sexto (FTE-068, [PENDIENTE DE VALIDACIÓN]).

### 1.2 Faena (cabezas) — serie disponible

| Año | Faena SENASA (M cab) | Fuente | Clasificación | Observación |
|---|---|---|---|---|
| 2020 | 757,9 | FTE-026 | [PENDIENTE DE VALIDACIÓN] | Fuente primaria no identificada con precisión |
| 2021 | 741,4 | FTE-023 | [VERIFICADO] | CEPA |
| 2022 | s/d | — | — | Faltante. BCR indica que fue menor que 2020 |
| 2023 | 740,5 (alt. 734,5) | FTE-002 (alt. FTE-025) | [VERIFICADO] / [PENDIENTE] | Contradicción (ver §13) |
| 2024 | 739,1 | FTE-002 | [VERIFICADO] | −0,2 % |
| 2025 | 750,2 | FTE-001, FTE-020 | [VERIFICADO] | +1,5 % |
| Promedio última década | ~740 | FTE-024 | [VERIFICADO] | Faena prácticamente estancada |

Para completar la serie 2015–2019 y 2022 se requiere leer los *Indicadores de Oferta y Demanda 2016-2024* y los anuarios SAGyP (DPV-010).

**Faena fuera de SENASA** `[ESTIMACIÓN]`: CAPIA/CEPA declaran ~900 M pollos/año (FTE-021) y CEPA proyectaba ~1.000 M para 2023 (FTE-022), contra 750 M en plantas SENASA. La diferencia sugiere que **al menos ~150 M de aves/año (~17 %) se faenan en plantas provinciales o municipales**. Hay otro indicio: la producción SAGyP 2024 (2,304 Mt) dividida por la faena SENASA daría 3,12 kg/ave (M023). Esa cifra supera el peso de canal esperable, lo que es coherente con una faena significativa fuera del registro federal. La magnitud exacta es un dato crítico para el proyecto: define el tamaño del segmento donde podría competir un entrante con habilitación no federal (DPV-011).

### 1.3 Producción (toneladas)

| Año | Producción (t) | Base / fuente | Clasificación |
|---|---|---|---|
| 2019 | ~1.831.000 (12 meses, período a confirmar) | FTE-060 | [PENDIENTE DE VALIDACIÓN] |
| 2021 | 2.318.000 | CEPA, incluye faena sin tránsito federal (FTE-023) | [VERIFICADO] |
| 2022 | 2.320.000 (CEPA: 2.450.000) | BCR (FTE-026) / CEPA (FTE-022) | [VERIFICADO] / [PENDIENTE] |
| 2023 | ~2.287.000 (BCR: ~2.500.000) | derivado SAGyP (FTE-002) / BCR (FTE-025) | [ESTIMACIÓN] / [PENDIENTE] |
| 2024 | 2.304.000 | SAGyP (FTE-002) | [VERIFICADO] |
| 2025 | 2.470.000 | CEPA (FTE-020) | [VERIFICADO] |
| 2026 | 2.580.000 (pronóstico) | USDA, anterior a la crisis 2026 (FTE-018) | [VERIFICADO] como pronóstico; probablemente sobreestimado |
| 2026 (a mar.) | −5,9 % interanual | datos oficiales citados por CEPA (FTE-031) | [PENDIENTE DE VALIDACIÓN] |

**Tendencia** `[VERIFICADO]` (FTE-026): la producción creció +16 % entre 2012 y 2022, alrededor de 1 % anual. Ese ritmo contrasta con la década anterior, cuando se pasó de 709 mil t a 2 Mt. Con la faena estable, el crecimiento reciente vino **del mayor peso por ave**. El salto aparente entre 2019 (~1,8 Mt) y 2021 (~2,3 Mt) probablemente refleja un **cambio metodológico** (inclusión de faena no federal) y no un crecimiento real. No debe usarse como tasa de crecimiento.

### 1.4 Consumo interno

**Consumo per cápita de carne aviar (kg/hab/año), por fuente:**

| Año | SAGyP (consumo aparente) | BCR | SSPM | CEPA / Cincap | USDA | Otras |
|---|---|---|---|---|---|---|
| 2004 | — | — | 21,6 | — | — | — |
| 2019 | — | — | — | — | — | 43 (FTE-060) [PENDIENTE] |
| 2020 | — | — | — | — | — | 44 (FTE-060) [PENDIENTE] |
| 2021 | — | — | — | >46 [PENDIENTE] | — | — |
| 2022 | — | — | — | ~47 [PENDIENTE] | — | — |
| 2024 | **46,25** | 45,2 | 44,8 | ~48,5 [ESTIMACIÓN] | — | — |
| 2025 | **47,68** | 46,8 | — | 49,4 | 48 | 47,6 (El Economista) |

Fuentes: FTE-003, FTE-024, FTE-027, FTE-007, FTE-020, FTE-030, FTE-018, FTE-051.

- **Serie de referencia adoptada:** SAGyP (SUP-008). CEPA opera como cota superior y SSPM/BCR como cota inferior.
- **Consumo aparente total** `[VERIFICADO]`: ~2,1 Mt (2022), 2,13 Mt (2023) y 2,1 Mt (2024), sin crecimiento en 2024 (FTE-026, FTE-028, FTE-024).
- **Evolución:** el consumo per cápita se duplicó entre 2004 y 2024 (21,6 → 44,8 kg según SSPM). Desde 2015 se mantiene por encima de 45 kg (según extracto de FTE-007) y crece lentamente. La propia industria reconoce que el mercado interno tiene **menos margen de crecimiento** (FTE-051). GTA, en su presentación judicial, lo describe como un "techo estructural" (FTE-034).

### 1.5 Participación del pollo frente a carne vacuna y porcina

| Carne | 2024 (kg/hab) | 2025 (kg/hab) | Var. | Participación 2025 [ESTIMACIÓN] |
|---|---|---|---|---|
| Vacuna | 48,49 | 49,92 | +2,9 % | 42,9 % |
| Aviar | 46,25 | 47,68 | +3,1 % | 40,9 % |
| Porcina | 17,42 | 18,89 | +8,4 % | 16,2 % |
| **Total** | **112,16** | **116,4** | +3,8 % | 100 % |

Fuente: SAGyP (FTE-003). En 2023 la participación fue 46 % bovina, 39 % aviar y 15 % porcina (FTE-063).

- Según SAGyP, en 2025 el pollo quedó **prácticamente empatado** con la carne vacuna. Según CEPA (49,4 kg) ya la superó. La prensa de 2026 afirma que el pollo pasó a ser la carne más consumida; esa afirmación depende de la serie usada.
- **Motor 2026:** en el primer semestre de 2026 la oferta interna de carne vacuna cayó −11,5 % interanual (CICCRA, FTE-061), por menor faena y más exportación. El precio del asado es 3,5 veces el del pollo entero (§7). La **sustitución hacia pollo** es un factor de demanda favorable. Su contracara: el precio relativo del pollo queda atado al ciclo ganadero.

### 1.6 Exportaciones e importaciones (resumen)

Detalle en [`exportaciones.md`](exportaciones.md).

- Exportaciones `[VERIFICADO]`: 2022: 230 mil t / USD 401 M · 2023: 160,6 mil t / USD 180,4 M · 2024: 185,8 mil t / USD 222,2 M (comestibles) · 2025: 206,4 mil t / USD 246,9 M (definición amplia).
- 2026: brote de IAAP en febrero y pérdida del estatus sanitario. El volumen exportado cayó −21,7 % interanual a marzo (FTE-031). El sector proyecta 170–180 mil t para el año si China sigue cerrada.
- **Importaciones:** no hay serie de volumen obtenida. En mayo de 2025 SENASA suspendió las importaciones avícolas desde Brasil por IAAP (FTE-053). Sin embargo, CEPA y GTA reportan ingreso de pechuga, carne mecánicamente separada (CMS) y prefritos brasileños en 2024–2026, por ~USD 30 M en siete meses de 2025 (FTE-031). Según GTA, estas importaciones ponen un **techo al precio de góndola** (FTE-034). La fecha de levantamiento de la suspensión y los volúmenes quedan pendientes (DPV-014).

### 1.7 Contexto internacional

- La producción mundial de carne de pollo se pronostica en 110,7 Mt para 2026 y las exportaciones mundiales en un récord de ~14,8 Mt. Brasil es el primer exportador y China aumenta sus exportaciones (USDA, FTE-019).
- Argentina aporta ~2,3 % de la producción mundial `[ESTIMACIÓN]` y es un **exportador menor**: exporta menos del 10 % de lo que produce. Compite en precio con Brasil, que tiene mayor escala y acceso a más mercados.

---

## 2. Cadena de valor

### 2.1 Flujo y nivel típico de integración

```
Genética (abuelas, importadas) → Reproductoras padres → Huevo fértil → Incubación → Pollito BB
        ↓                                                                              ↓
   [integrador]                                                          Granja de engorde (integrado)
                                                                                       ↓
Alimento balanceado (maíz + harina de soja + núcleo) ──────────────────────────────────┘
                                                                                       ↓
                                  Captura y transporte vivo → Frigorífico (faena) → Trozado / elaborados
                                                                                       ↓
                             Distribución con frío → Supermercado / mayorista / pollería / gastronomía
                                                                                       ↓
                                                           Consumidor interno / exportación
```

| Eslabón | Cómo funciona en Argentina | Quién lo controla habitualmente | Evidencia |
|---|---|---|---|
| Genética (abuelas) | Líneas Cobb, Ross (Aviagen) y Hubbard, importadas a nivel abuelas. Se estima que ~66 % de la avicultura depende de la genética producida en Santa Elena (ER) por Reproductores Cobb SA. GTA tiene una alianza con Cobb/Tyson. | Pocas empresas globales y sus socios locales | FTE-049, FTE-038, FTE-039 |
| Reproductoras / huevo fértil | Granjas de padres que producen huevo fértil. Alrededor de 9,4 M de cabezas en producción en 2025 (interpretación a confirmar). | Integradores grandes. También existen proveedores independientes. | FTE-001, FTE-062 |
| Incubación → pollito BB | Plantas de incubación. Por ejemplo, Fadel incuba ~1,2 M huevos/semana. | Integradores | FTE-045 |
| Alimento balanceado | Maíz y soja. Es el mayor rubro de costo del pollo vivo: suele citarse **65–70 %**, cifra [PENDIENTE DE VALIDACIÓN] contra el ICPP de SAGyP. | Integradores con planta propia. Algunos siembran (Grupo Cem, >3.000 ha). | FTE-006, FTE-047 |
| Engorde | **Sistema integrado:** el integrador provee pollito, alimento, sanidad y asistencia. El productor aporta galpones, trabajo y energía (gas). La crianza dura 46–50 días hasta ~3 kg vivo. El productor cobra por ave criada: ~$700–800/pollo en 2026 según prensa. Frecuentemente **sin contrato formal** y con cobro a ~60 días. | Productor integrado independiente, bajo dirección del integrador | FTE-050, FTE-051 |
| Captura y transporte | Cuadrillas y camiones jaula de la granja a la planta. | Integrador o tercerizado | Sin dato cuantitativo |
| Faena y procesamiento | Plantas de 80.000 a >200.000 aves/día en las empresas medianas y grandes. El trozado es parte central (Fepasa: 60 % a trozado). | Integrador | FTE-043 a FTE-046 |
| Subproductos | Harina de plumas y vísceras. Menudos y garras comestibles, en parte exportados. | Integrador (rendering propio en los grandes) | FTE-038, FTE-020 |
| Distribución y venta | Frío hasta supermercados, mayoristas, pollerías y locales propios. Grupo Cem tiene >100 locales. | Integrador y distribuidores | FTE-047 |

### 2.2 Qué suele estar integrado

- **Núcleo integrado típico** (alrededor de 40 integradoras, FTE-066): reproductoras, incubación, alimento balanceado, faena y distribución. La producción de CEPA se concentra en integradoras.
- **Normalmente tercerizado** (vía integración contractual): el engorde en granjas de productores integrados. Con eso el integrador evita invertir en galpones, pero depende de la red de productores. La crisis de GTA mostró la fragilidad del esquema: la empresa perdió el 85 % de sus integrados (FTE-036).
- **Genética de abuelas:** nunca es local, siempre depende de proveedores globales.
- **Variantes:** algunos grupos integran hacia atrás, hasta el grano (Grupo Cem), y otros hacia adelante, hasta el minorista (Grupo Cem con Carnave). Hay empresas medianas que compran pollito BB o alimento a terceros (dato puntual no relevado).

**Implicancia para el proyecto:** el modelo dominante no es "todo propio", sino **integrador + productores integrados**. El control del flujo (genética, pollito, alimento y faena) está en manos del integrador, mientras que el engorde lo aportan terceros con sus propios activos.

---

## 3. Geografía productiva

### 3.1 Tabla provincial

No existe una serie pública de producción primaria por provincia. Como indicador se usa la **faena SENASA** (dónde se faena). La producción primaria se aproxima por la cantidad de granjas cuando hay datos.

| Provincia | % faena SENASA 2025 | % producción primaria (dato disponible) | Principales ventajas | Principales desventajas |
|---|---|---|---|---|
| **Entre Ríos** | 50,2 % (CEPA: 50,39 %) | ~62,9 % de las granjas de parrilleros del país (año no identificado); ~2.500 granjas | Cluster completo: genética (Santa Elena), incubación, alimento, granjas integradas, plantas, servicios y mano de obra calificada. Exportación por puertos del río Uruguay y Paraná. | Distancia al AMBA (principal centro de consumo). Concentración sanitaria: un brote afecta a gran parte de la oferta nacional. Productores integrados dependientes de pocos compradores. Competencia intensa por integrados y personal. |
| **Buenos Aires** | 35,4 % (CEPA: 35,47 %) | s/d | Cercanía al mayor mercado consumidor (AMBA). Plantas en el corredor norte (Pilar, Capitán Sarmiento, Esteban Echeverría). Acceso a granos. | Los brotes de IAAP de 2025 y 2026 ocurrieron en BA (FTE-058, FTE-011). Presión urbana y ambiental sobre granjas y plantas. Mayor costo laboral y conflictividad gremial (cierres de plantas de GTA). |
| **Santa Fe** | 5,1 % (CEPA: 4,8 %) | s/d | Zona núcleo de granos (maíz y soja) con bajo flete de alimento. Casos de integración hasta el minorista (Grupo Cem, Esperanza). Cerca de Rosario y de Córdoba. | Menor densidad de proveedores avícolas especializados que ER. Escala regional más acotada. |
| **Córdoba** | 4,1 % (−5,8 % vs 2024) | s/d | Principal productor de maíz y alimento barato. Planta integrada Avex (Río Cuarto). Mercado de Córdoba capital. | Un brote de IAAP en 2026 afectó a ponedoras (FTE-057). La planta Avex opera cedida a ACA y en concurso (FTE-040). Lejos de puertos para exportar. |
| Río Negro | 2,5 % | s/d | Abastecimiento regional de la Patagonia. | Lejos de granos. Escala limitada. |
| Salta, Mendoza, La Rioja, Jujuy | ~2,7 % en conjunto (Salta 1,22 %; Mendoza 0,65 %) | s/d | Abastecimiento regional y fletes largos desde ER/BA que protegen al productor local. | Escala limitada. Costo de alimento por flete. |

Fuentes: FTE-001, FTE-020, FTE-048, FTE-028, FTE-040, FTE-057. Ventajas y desventajas: análisis propio a partir de la evidencia citada.

- ER y BA concentran **~85 %** de la faena SENASA. Para 2019 se mencionaba 83 % de la producción en ambas provincias (FTE-060).
- **Dato pendiente:** la localización de las plantas de alimento balanceado, incubadoras y faena provincial o municipal por provincia (DPV-011). Debe obtenerse del registro de establecimientos de SENASA y de los organismos provinciales.

### 3.2 Clusters y corredores identificados

| Cluster / corredor | Localidades con evidencia | Actores con evidencia |
|---|---|---|
| **Corredor del río Uruguay (ER)** | Concepción del Uruguay, San José, Colón/Pronunciamiento, Villa Elisa, Santa Elena (genética) | GTA (La China, cerrada), Fepasa, Las Camelias, Fadel, Noelma, Reproductores Cobb |
| **Corredor Paraná / sur de ER** | Gualeguay, Hernandarias | Soychú, Indavisa |
| **Norte y oeste del conurbano bonaerense (BA)** | Pilar, Capitán Sarmiento, Esteban Echeverría | Plantas de GTA (paralizadas desde ago-2026) |
| **Centro de Santa Fe** | Esperanza, Humboldt | Grupo Cem (AG Humboldt, Carnave) |
| **Sur de Córdoba** | Río Cuarto | Avex (GTA → ACA) |

---

## 4. Principales empresas (resumen)

Detalle y fuentes en [`competidores.md`](competidores.md).

| Empresa | Base | Escala pública aproximada | Integración | Mercado | Situación 2026 |
|---|---|---|---|---|---|
| Granja Tres Arroyos (GTA) + Wade (ex Cresta Roja) + Avex | BA, ER, Cba, Uruguay | Llegó a ~760.000 aves/día y ~25 % de la faena; en 2026 cayó a ~200.000/día | Total (incluye genética con Cobb/Tyson) | Interno y exportación (~35 %) | **Concurso preventivo** (sept-2026); plantas paralizadas |
| Soychú | Gualeguay (ER) | ~4,5 M pollos/mes; ~12 % de la faena en 2021 | Integrada | 85 % interno | Sin evidencia de crisis |
| Las Camelias | San José (ER) | ~500 t/día de producto; ~6,9 % de la faena en 2021 | Integrada; 250 familias integradas | ~38 % exportación | Invierte (granja de 522.000 aves/ciclo) |
| Noelma | Villa Elisa (ER) | >150.000 aves/día; ~4,9 % en 2021 | Integrada | Interno y exportación | s/d |
| Fadel | Colón (ER) | ~160.000 aves/día | Integrada (también porcinos) | Interno y exportación | s/d |
| Fepasa | C. del Uruguay (ER) | ~80.000 pollos/día | Faena y trozado | s/d | s/d |
| Grupo Cem | Esperanza (SF) | ~600.000 pollos/mes | Del grano al **local propio** (>100 bocas) | Regional (SF, Cba, SdE, Tuc) | s/d |

**Concentración** `[VERIFICADO]`: según CEPA, 10 integradoras concentran más de la mitad de la capacidad (FTE-020). Hacia 2021, las cuatro primeras sumaban aproximadamente la mitad de la faena `[ESTIMACIÓN]` a partir de FTE-041 y FTE-037. La salida parcial de GTA en 2026 redistribuye el mercado.

---

## 5. Productos

| Producto | Tipo | Evidencia / comentario | Potencial exportador |
|---|---|---|---|
| Pollo entero eviscerado (fresco/refrigerado) | **Commodity** | Producto "gancho" de supermercados. En la sobreoferta de sept-2025 se vendió entre $1.999 y $2.700/kg según la cadena (FTE-052). Referencia de precio IPC. | Medio: 23,7 % del volumen exportado en 2025 (enteros, principalmente congelados) |
| Pollo entero congelado | Commodity | Válvula de ajuste ante excedentes y producto típico de exportación | Sí |
| Trozado: pata-muslo, alas | Commodity con algo de diferenciación | 37,2 % del volumen exportado (trozados) | Sí (alas y pata-muslo a China, según FTE-014) |
| Pechuga / supremas / filet | **Mayor valor** en el mercado interno | Brasil ingresa pechuga que compite en precio (FTE-031) | Bajo a medio |
| Menudos (hígado, corazón, molleja) | Subproducto comestible | Bajo valor interno | Sí, en mercados específicos (África, Asia) |
| **Garras / patas** | Subproducto de **bajo valor interno y alto valor exportable** | Producto estrella para China (FTE-014). "Menudos, garras y subproductos" representaron el 32,9 % del volumen exportado en 2025 | **Alto, pero condicionado a China** (restringida en 2026) |
| Marinados / condimentados | Valor agregado | Soychú vende "semipreparados condimentados" (FTE-043) | Bajo |
| Milanesas, hamburguesas, nuggets, prefritos | **Valor agregado** | Brasil exporta cocidos/prefritos a Argentina (FTE-031). GTA tenía línea de prefritos y fiambres. | Bajo: solo 1,6 % del volumen exportado en 2025 |
| CMS (carne mecánicamente separada) | Insumo industrial | Importada desde Brasil para la industria (FTE-031) | Bajo |
| Harinas de plumas y vísceras | Subproducto no comestible | Parte del 4,6 % de alimento balanceado exportado (a confirmar) | Medio (mercados de alimento animal) |

**Síntesis:**

- **Commodity:** pollo entero y trozados básicos. Compiten por costo y escala.
- **Mayor valor agregado:** pechuga y supremas, marinados, elaborados y rebozados, porcionado para gastronomía. Requieren marca o canal, cadena de frío y desarrollo comercial.
- **Potencial exportador:** garras (China), alas y pata-muslo, entero congelado (Asia, África, Medio Oriente), menudos. Todos requieren habilitación SENASA federal y listados por país, y dependen del estatus sanitario.
- **Dato faltante:** no hay mix público del mercado interno por producto (entero vs. trozado vs. elaborados). Una fuente periodística de baja confiabilidad menciona que ~70 % del pollo que llega al minorista se troza; queda [PENDIENTE DE VALIDACIÓN] y sin uso.

---

## 6. Canales comerciales

### 6.1 Importancia relativa (evidencia disponible)

**No existe una serie pública de ventas de pollo por canal** (DPV-012). Lo disponible:

| Canal | Evidencia | Importancia relativa (cualitativa) | Nivel de evidencia |
|---|---|---|---|
| Supermercados (cadenas) | Concentran ~40 % del volumen de consumo masivo general (Scentia, abr–may 2026, FTE-054), no específico de pollo. Usan el pollo entero como producto gancho (FTE-052). | Alta | Indirecta |
| Autoservicios independientes y "chinos" | 16 % del volumen de consumo masivo general (FTE-054) | Media | Indirecta |
| Pollerías y carnicerías (canal tradicional) | Canal clásico de pollo fresco y trozado. Comercios tradicionales: 32 % del consumo masivo general (FTE-054). | Alta en fresco y trozado | Indirecta / cualitativa |
| Mayoristas y distribuidores | Abastecen al canal tradicional y a la gastronomía | Media–alta | Cualitativa |
| Gastronomía (HORECA, rotiserías, cadenas de comida) | Demanda de trozados, porcionados y elaborados | Media | Sin dato |
| Industria alimenticia | Demanda de CMS y cortes industriales, en parte abastecida con importación brasileña (FTE-031) | Baja–media | Cualitativa |
| Locales propios de marca | Modelo Grupo Cem/Carnave con >100 bocas (FTE-047) | Nicho relevante como modelo de negocio | Caso |
| Exportación | ~7–8 % del volumen producido | Baja en volumen, alta como válvula de excedentes | [VERIFICADO] |

### 6.2 Qué ventaja podría representar una red de ~90 supermercados

> **La demanda de esta red NO está validada** (SUP-004, DPV-002, DPV-003). El siguiente es un análisis estratégico condicional.

**Ventajas potenciales (si se valida el acceso):**

1. **Menor costo de conquista comercial.** En un mercado maduro y concentrado, conseguir góndola es una barrera de entrada. Un canal propio o aliado la reduce.
2. **Información de demanda:** volúmenes, mix y precios reales para dimensionar sin suponer (regla 9 de `CLAUDE.md`).
3. **Espacio para marca propia o marca del supermercado** y para productos de mayor margen (trozado, marinados, elaborados), en lugar de competir solo con pollo entero.
4. **Logística concentrada** en un conjunto conocido de bocas.
5. **Referencia de escala:** Grupo Cem abastece >100 locales propios con ~600.000 pollos/mes (FTE-047). Es solo un orden de magnitud de un modelo distinto (locales especializados, no supermercados). **No es una estimación de la demanda de la red.**

**Riesgos del canal supermercado:**

1. **Poder de negociación del comprador:** el pollo entero se usa como producto gancho y se vende cerca del costo (FTE-052).
2. **Plazos de pago largos** frente a un producto perecedero con costo de alimento pagado al contado: **capital de trabajo**.
3. **Dependencia de un solo cliente:** si la red cambia de proveedor o sufre problemas, el negocio pierde su canal.
4. **Exigencias de continuidad:** entregas diarias o semanales sin cortes. El pollo no se puede stockear fresco. Hacen falta congelado, otros canales o exportación para los excedentes.
5. **Habilitación requerida:** si la red opera en más de una provincia, se necesita tránsito federal (SENASA) (DPV-018; DEC-009).
6. **Competencia con integradores de gran escala,** que pueden ofrecer precios bajo costo en momentos de sobreoferta (sept-2025, liquidación de GTA en 2026).

---

## 7. Precios

### 7.1 Precios relevados

| Nivel | Producto | Fecha | Valor | Unidad | Moneda / TC | Fuente | Clasificación |
|---|---|---|---|---|---|---|---|
| Productor (vivo) | Pollo parrillero vivo | semana 2026-07-06 | 2.528 | $/kg vivo | ARS; ≈ USD 1,70 a TC mayorista 1.488,50 (2026-07-06) | FTE-029, FTE-055 | [PENDIENTE DE VALIDACIÓN] |
| Mayorista | Pollo eviscerado, cajón 20 kg, sin IVA | ene-2025 | 1.742,1 | $/kg | ARS | FTE-004 | [VERIFICADO] |
| Mayorista | ídem | ene-2026 | 2.847,5 | $/kg | ARS (+63,5 % interanual [ESTIMACIÓN]) | FTE-004 | [VERIFICADO] |
| Mayorista | ídem, variación interanual | feb–jun 2026 | +50,5 / +24,8 / +15,7 / +27,2 / +17,4 | % | — | FTE-004 | [PENDIENTE] (valores absolutos ambiguos) |
| Consumidor | Pollo entero, GBA | ago-2026 | 4.780,14 | $/kg con IVA | ARS; ≈ USD 3,16 (mayorista 1.514) / 3,10 (MEP 1.542,96) al 2026-08-26 | FTE-008, FTE-055 | [VERIFICADO] (USD: [ESTIMACIÓN]) |
| Consumidor | Asado / nalga / cuadril / picada común | ago-2026 | 16.736,73 / 21.763,38 / 21.102,92 / 10.613,08 | $/kg con IVA | ARS | FTE-008 | [VERIFICADO] |
| Consumidor | Pollo entero en promoción (Coto, Vea, Día, Carrefour) | probable sept-2025 | 1.999 / 2.300 / 2.600 / 2.700 | $/kg | ARS | FTE-052 | [PENDIENTE] (fecha) |
| Integrado | Pago por ave criada | 2026 | 700–800 | $/ave | ARS | FTE-051 | [PENDIENTE] |
| Exportación | Carne aviar, promedio | ene-2026 / feb-2026 | 1.056 / 1.050 | USD/t FOB | USD | FTE-032 | [PENDIENTE] |
| Exportación | Promedio anual 2022 / 2023 / 2024 / 2025 | anual | 1.743 / 1.123 / 1.196 / 1.196 | USD/t FOB | USD | derivado (M067–M070) | [ESTIMACIÓN] |

### 7.2 Lectura y limitaciones

- **Precio relativo** `[ESTIMACIÓN]`: en agosto de 2026, 1 kg de asado equivale a 3,5 kg de pollo entero, y 1 kg de nalga a 4,55 kg. Esta brecha es el principal motor de la sustitución de consumo.
- **Volatilidad:** el precio mayorista de enero de 2026 subió +63,5 % interanual. Con el brote de febrero y el cierre de exportaciones, en 2025 se registraron ventas ~40 % bajo costo durante ~40 días (FTE-052). **El precio interno del pollo es muy sensible a cierres de exportación**, porque el excedente vuelve al mercado local.
- **Inconsistencia detectada:** el precio del pollo vivo de CAPIA (2.528 $/kg, julio 2026) es comparable o superior al precio mayorista del eviscerado. Eso no es coherente con un rendimiento de faena menor al 100 %. Hipótesis: el precio vivo corresponde a otro mercado o condición (IVA, lugar de entrega, volúmenes chicos), o los valores mayoristas del extracto no corresponden a 2026. **No usar ambos precios juntos hasta resolverlo** (DPV-013).
- **Series públicas que existen pero no se pudieron leer:** mayorista y minorista mensual de SAGyP (FTE-004, FTE-005), precios medios de INDEC (serie IPC), cotizaciones de CAPIA y Cátedra Avícola, ICPP (FTE-006).
- **Series que no existen como públicas:** precios mayoristas por corte (pechuga, pata-muslo, alas), precios de elaborados y precios pagados por supermercados a proveedores. Hay que obtenerlos por relevamiento o cotización (DPV-013, DPV-003).
- **Tipo de cambio:** las conversiones son ilustrativas y usan el TC mayorista del día del dato (SUP-009). El criterio definitivo depende de DEC-006.

---

## 8. Exportación (resumen)

Detalle en [`exportaciones.md`](exportaciones.md). Puntos clave:

- **Estado a 2026-09-29:** reabiertos con evidencia UE (desde 2026-08-17), Chile y Perú (junio 2026) y Japón (aves faenadas desde 2026-09-08). **China:** sin evidencia pública de reapertura tras el brote de febrero de 2026. CEPA condiciona su proyección a esa reapertura.
- La **volatilidad sanitaria** es el rasgo central. Hubo brotes con cierre de mercados en 2023, ago-2025 y feb-2026, es decir, tres en cuatro años.
- El acuerdo **UE–Mercosur** rige provisoriamente desde 2026-05-01, con una cuota aviar de 180.000 t/año para el bloque, a repartir con Brasil. Es una oportunidad potencial, no confirmada para Argentina.

---

## 9. Competencia y barreras de entrada

### 9.1 Estructura

- **Oligopolio con franja competitiva:** unas 10 integradoras concentran más de la mitad de la capacidad (FTE-020), alrededor de 40 integradoras relevantes y un segmento de faena provincial y municipal no cuantificado (§1.2).
- **Líder en crisis:** GTA (~25 % de la faena en su pico) está en concurso preventivo con deuda de ~USD 351 M (FTE-034). Su faena cayó de ~700.000 a ~200.000 pollos/día (FTE-036). En 2014 ya había entrado en concurso el entonces segundo actor, Rasic/Cresta Roja, con ~15 % del mercado en su pico (FTE-067). **El sector tiene historia de quiebras de empresas grandes.**

### 9.2 Barreras

| Barrera | Descripción | Intensidad para un entrante |
|---|---|---|
| Economías de escala | La faena, el alimento y la incubación tienen altos costos fijos. Las plantas del sector procesan de 80.000 a >200.000 aves/día. Un entrante chico tiene mayor costo unitario. | Alta |
| Integración vertical | Controlar genética, pollito y alimento da seguridad de abastecimiento y costo. Un no integrado compra pollito BB o pollo vivo a sus competidores. | Alta |
| Acceso a granos | Alimento ~65–70 % del costo del vivo (a validar). Estar en zona de granos y tener capacidad de acopio o compra reduce el costo. | Media (Argentina tiene grano abundante, pero la volatilidad es alta) |
| Acceso a clientes | Góndola concentrada. El pollo entero se usa como gancho y los compradores tienen poder. | Alta (**mitigable con la red de ~90 supermercados si se valida**) |
| Bioseguridad | IAAP recurrente. Un brote implica despoblamiento, pérdida y cierre de exportaciones. | Alta |
| Habilitaciones | SENASA (tránsito federal y exportación: listados por país), provinciales y municipales, ambientales y de efluentes. Decreto 4238/68 y Res. SENASA 592/2026 (FTE-016). | Alta en plazo y costo (ver `16_normativa_senasa`) |
| Frío | Cadena de frío obligatoria desde la faena hasta la góndola. Congelado como válvula. | Media–alta |
| Logística | Transporte de aves vivas (bienestar animal, distancia granja–planta) y distribución refrigerada | Media |
| Capital de trabajo | Ciclo de ~50 días de crianza más plazo de pago de clientes. El alimento es el grueso del costo y se paga antes de cobrar. | **Alta** |
| Red de productores integrados | Hacen falta galpones de terceros. Según Soychú, el sector necesita renovar ~1.200 galpones de ~USD 300.000 c/u (FTE-043). | Alta |

### 9.3 Por qué una empresa nueva puede fracasar aun teniendo capital

1. **El capital no compra escala instantánea ni costo competitivo.** Los márgenes del commodity son finos: en 2025–2026 hubo ventas bajo costo y pagos al integrado que "apenas cubren costos" (FTE-052, FTE-051). GTA tenía escala, integración total y un socio global (Tyson, 34 %), y aun así entró en concurso (FTE-034, FTE-039).
2. **El mercado interno está maduro.** La faena está estancada en ~740 M cab y el consumo per cápita crece poco. Un nuevo volumen **desplaza** a otro en lugar de sumarse, lo que obliga a competir por precio.
3. **Shocks sanitarios exógenos:** un brote de IAAP en cualquier punto del país cierra exportaciones y hace caer el precio interno por sobreoferta. Una planta sin espalda financiera no aguanta varios meses de precios bajo costo.
4. **Capital de trabajo subestimado:** alimento, pollitos y pago a integrados se afrontan antes de cobrar al supermercado.
5. **Dependencia de insumos de competidores:** sin reproductoras ni incubación propias, el entrante compra pollito BB a integradores que compiten con él.
6. **Un canal sin contrato no es demanda.** Si la red de supermercados no firma compromisos de volumen y precio, el entrante carga con el riesgo comercial completo.
7. **Tipo de cambio e importaciones:** con tipo de cambio apreciado y apertura, el pollo brasileño (pechuga, prefritos) pone un techo al precio (FTE-034, FTE-031).

---

## 10. Oportunidades

Solo se incluyen oportunidades con justificación en la evidencia. Cada una requiere validación antes de tomarse como base.

| Ámbito | Oportunidad | Justificación | Condición / dato que la valida |
|---|---|---|---|
| **Mercado local** | Reconfiguración de la oferta por la crisis de GTA (~25 % de la faena en su pico) | La faena de GTA cayó ~500.000 pollos/día. Quedan clientes, productores integrados (85 % perdidos por GTA) y plantas paralizadas (FTE-036, FTE-035). | Verificar cuánto absorbieron otros integradores. Evaluar disponibilidad de faena a façon, alquiler o compra de activos en concurso (DPV-006, DPV-016). **Riesgo:** activos con conflictos laborales y judiciales. |
| **Mercado local** | Sustitución de carne vacuna por pollo | Oferta interna de vacuna −11,5 % en el 1S-2026. Asado a 3,5 veces el precio del pollo entero (FTE-061, FTE-008). | Depende del ciclo ganadero. No es estructural garantizado. |
| **Supermercados** | Canal directo con ~90 bocas | Reduce la barrera de acceso a clientes (§6.2) | **Requiere** volúmenes, precios, plazos de pago y cartas de intención (DPV-002, DPV-003) |
| **Mayor valor** | Trozado, porcionado, marinados y elaborados con marca propia o del supermercado | Los commodities tienen márgenes finos. Brasil demuestra demanda de pechuga y prefritos al importarlos (FTE-031). | Requiere planta con sala de trozado y elaboración, y validar precios y volúmenes por producto (DPV-013) |
| **Subproductos** | Garras, menudos y harinas | Las garras tienen alto valor exportable (China) y bajo valor local. Subproductos y menudos fueron ~33 % del volumen exportado en 2025 (FTE-020). | Garras: depende de la reapertura de China y de una habilitación de exportación. Harinas: requiere rendering o venta a terceros. |
| **Exportación** | Cuota UE–Mercosur (180.000 t para el bloque), Japón, UE, Chile y Perú reabiertos | Acceso vigente en 2026 (FTE-012, FTE-013, FTE-033, FTE-065) | Requiere habilitación SENASA federal y listados por destino, escala exportable y competitividad frente a Brasil. **No es viable para una primera etapa sin validación.** |
| **Integración vertical** | Integración "hacia adelante" (carnicería → supermercados), como Grupo Cem | El proyecto ya parte de una carnicería y un canal minorista potencial (FTE-047) | Evaluar eslabón por eslabón (DEC-002). La integración hacia atrás (reproductoras, incubación) requiere más capital y know-how. |
| **Nichos** | Faena regional con habilitación provincial para abastecer un área cercana | ~150 M aves/año se faenarían fuera de SENASA [ESTIMACIÓN] (§1.2) | Limita a una sola provincia e impide exportar. Magnitud a validar (DPV-011). |

**No se consideran oportunidades justificadas** (por falta de evidencia): pollo orgánico o "de campo" premium (no se relevó demanda ni precios), pollo halal para exportación (sin datos de habilitación actual), crecimiento fuerte del consumo per cápita (la evidencia indica madurez).

---

## 11. Amenazas

| Amenaza | Evidencia | Impacto | Frecuencia / probabilidad (cualitativa) |
|---|---|---|---|
| **Influenza aviar (IAAP)** | Brotes con pérdida de estatus en 2023, ago-2025 y feb-2026. Suspensión a ~40 destinos. Recuperación de estatus en abr-2026 (FTE-011, FTE-057, FTE-058). | Muy alto: cierre de exportaciones, sobreoferta interna, despoblamiento si el brote es propio | Alta (3 eventos en 4 años) |
| Enfermedad de Newcastle | Argentina es libre (FTE-015) | Muy alto si aparece | Baja (sin evidencia reciente) |
| Salmonella / micoplasma | SENASA tiene programa de control (FTE-015) | Medio–alto: inocuidad, rechazos, reputación | Media (riesgo operativo permanente) |
| Volatilidad de maíz y soja | Alimento ~65–70 % del costo (a validar) | Alto | Alta |
| Tipo de cambio | Apreciación que abarata importaciones de Brasil. GTA la cita como causa (FTE-034). | Alto: techo de precios | Media–alta |
| Inflación | Precio mayorista +63,5 % interanual (ene-2026) | Medio: desfasaje entre costos y precios, y en contratos | Alta |
| Costos energéticos | Gas para calefacción en granjas. "Falta de suministro eléctrico" invocada por GTA (FTE-035). Suba de costos (FTE-034). | Medio | Media |
| Dependencia de exportaciones | Excedentes que no salen presionan el precio interno (FTE-052) | Alto para el conjunto del sector | Alta |
| Barreras sanitarias externas | China restringida en 2026. Cada mercado exige listados y protocolos. | Alto para exportadores | Alta |
| Competencia | 10 integradoras con más de la mitad de la capacidad. Importación brasileña. Liquidación de stocks y activos de GTA. | Alto | Alta |
| Sobrecapacidad | Faena estancada. Capacidad ociosa por la crisis de GTA. Posible reactivación de plantas por nuevos dueños. | Alto: presión de precios | Media–alta |
| Dependencia de clientes | Canal supermercados concentrado (§6.2) | Alto | Depende del diseño comercial |
| Capital de trabajo | Ciclo de ~50 días más plazos de pago de clientes | Alto | Alta |
| Conflictividad laboral | Cierres y conflictos en plantas de GTA (FTE-035) | Medio–alto | Media |

---

## 12. Conclusiones para el proyecto

Ver [`conclusiones_mercado.md`](conclusiones_mercado.md): respuesta a las siete preguntas, cinco conclusiones clave e información faltante.

---

## 13. Control de calidad

### 13.1 Datos contradictorios y fuente preferida

| Tema | Valores en conflicto | Causa probable | Fuente preferida y criterio |
|---|---|---|---|
| Consumo aviar 2025 | 46,8 (BCR) · 47,6/47,68 (SAGyP, El Economista) · 48 (USDA) · 49,4 (CEPA) | Metodologías distintas de consumo aparente (base peso, población, stock) | **SAGyP (47,68)**: organismo oficial y serie comparable con vacuna y porcina. CEPA como cota superior. |
| Consumo aviar 2024 | 44,8 (SSPM) · 45,2 (BCR) · 46,25 (SAGyP) · ~48,5 (CEPA) | ídem | **SAGyP (46,25)** |
| Faena 2023 | 740,5 vs 734,5 M cab | Dato preliminar vs definitivo | **740,5** (coherente con la variación publicada por SAGyP para 2024) |
| Producción 2022 | 2,32 Mt (BCR) vs 2,45 Mt (CEPA) | Base distinta | **BCR 2,32** (serie coherente con SAGyP); CEPA a verificar |
| Producción 2023 | ~2,29 Mt (derivado SAGyP) vs ~2,5 Mt (BCR) | Base distinta o redondeo | **SAGyP** (derivado) |
| Exportaciones 2025 | 206.436 t / USD 246,9 M (CEPA) vs 169.000 t / USD 218 M (sin fuente identificada) | CEPA incluye subproductos no comestibles y alimento balanceado (4,6 % del volumen) | Usar **CEPA** como total del sector y un dato "comestible" SAGyP/INDEC cuando se obtenga (DPV-010) |
| Brote ago-2025 | 2025-08-20 (Infobae) vs 2025-08-26 (USDA) | Fecha de suspensión vs fecha de confirmación | Fecha exacta irrelevante para el análisis; se cita "agosto 2025" |
| Faena total | 750 M (SENASA) vs 900 M (CAPIA/CEPA) vs 1.037 M "pollos nacidos" | Distintos universos (federal vs total; nacidos vs faenados) | No son contradictorios: son **universos distintos**. Cuantificar (DPV-011). |
| Precio vivo vs mayorista | 2.528 $/kg vivo vs 2.847,5 $/kg eviscerado (ene-2026) | Condiciones de precio distintas o extracto ambiguo | Ninguna hasta validar (DPV-013) |
| Cuotas de mercado | "GTA 21 %, Rasic 15 %" (prensa) vs "GTA ~25 %" (Ecos365) | El 15 % de Rasic corresponde a 2014, antes de su quiebra | Descartado el par 21 %/15 % por desactualizado |
| Importaciones de Brasil +122 % (2026) | Aparece en búsquedas de pollo | Corresponde a **carne vacuna**, no a pollo | Descartado para pollo |

### 13.2 Verificaciones realizadas

- **Años:** cada cifra indica su año o período. Donde se comparan años distintos se aclara (ej.: participación mundial calculada con pronóstico USDA 2026 para Argentina y el mundo, misma fuente y año).
- **Unidades:** se distinguen t, kg/hab/año, millones de cabezas, USD FOB, ARS/kg con o sin IVA, y USD/t.
- **Producción vs. faena:** se tratan por separado. La relación t/cabeza SENASA (3,12 kg) se muestra solo como indicio y no como rendimiento.
- **Consumo vs. producción:** el consumo aparente (~2,1 Mt) es menor que la producción (~2,3–2,5 Mt) por exportaciones y diferencias de base.
- **Habilitado vs. potencial:** ver la clasificación de mercados en [`exportaciones.md`](exportaciones.md).
- **Cifras descartadas:** "faena 2022 745 M cab", eco del texto de la consulta en el buscador; "Rasic 15 %", desactualizado; "importación +122 %", corresponde a carne vacuna.
