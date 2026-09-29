# Mercado internacional de carne aviar

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 · **Fase:** 0 (prefactibilidad) · **Carpeta:** `17_exportacion`

Documentos asociados: [`mercados_por_pais.md`](mercados_por_pais.md) (acceso de Argentina por país, China, Halal, UE) · [`productos_exportables.md`](productos_exportables.md) (productos y precios) · [`estrategia_valorizacion_ave.md`](estrategia_valorizacion_ave.md) · [`requisitos_planta_exportadora.md`](requisitos_planta_exportadora.md) · [`logistica_exportacion.md`](logistica_exportacion.md) · [`datos_exportacion.csv`](datos_exportacion.csv) (IDs `E###`) · [`conclusiones_exportacion.md`](conclusiones_exportacion.md).
Antecedentes del lado argentino (serie de exportación, importaciones): [`../01_mercado/exportaciones.md`](../01_mercado/exportaciones.md).

> **Restricciones de fase:** no se selecciona país objetivo, no se dimensiona la planta y no se define CAPEX. No se supone que exportar sea más rentable que vender en el mercado interno.

---

## 0. Estado de verificación

- En esta sesión (2026-09-29) la red del entorno volvió a **bloquear la lectura directa** de todos los documentos (USDA, FAO, SENASA, argentina.gob.ar, Comisión Europea, sitios sectoriales). Solo funcionó el buscador web.
- Por lo tanto **ninguna cifra de este documento está verificada contra su documento original**. Se usan las etiquetas de [`01_mercado/mercado_avicola_argentina.md` §0.2](../01_mercado/mercado_avicola_argentina.md): `[PVDP]` (fuente A/B identificada, coherente) · `[PVDP · débil]` (prensa sola, sitio comercial, fecha dudosa o contradicción) · `[ESTIMACIÓN]` (cálculo propio, método explicado).
- Fuentes: IDs `FTE-###` en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv). Datos tabulados: [`datos_exportacion.csv`](datos_exportacion.csv).
- **Universos (regla 18):** USDA mide "carne de pollo" (*chicken meat*, equivalente listo para cocinar) y excluye patas/garras en algunas series; CEPA mide "productos avícolas" en sentido amplio (incluye subproductos y alimento balanceado); ABPA mide "carne de frango" (incluye procesados). Las cifras de distintos organismos **no se suman ni se restan** entre sí.

---

## 1. Magnitudes mundiales

| Indicador | Valor | Período | Fuente | Estado |
|---|---|---|---|---|
| Producción mundial de carne de pollo | 110,7 Mt (+~3 %) | 2026 (pronóstico abr-2026) | USDA FAS (FTE-019) | [PVDP] |
| Exportaciones mundiales de carne de pollo | ~14,8 Mt (récord; +498.000 t, +3 %) | 2026 (pronóstico) | FTE-019 | [PVDP] |
| Exportaciones mundiales | 13,8 Mt (pronóstico de 2025) | 2025 | FTE-019 (extracto de la edición 2025) | [PVDP] |
| Parte de la producción que se comercia internacionalmente | ~13 % | 2026 | 14,8 / 110,7 | [ESTIMACIÓN] |
| Crecimiento del comercio mundial de carne de pollo | +9 % acumulado | 2020–2025 | USDA (FTE-125) | [PVDP] |
| Crecimiento del consumo mundial de carne aviar | ~+21 % | 2025–2034 (proyección) | OECD-FAO (FTE-124) | [PVDP] |

**Lectura:** la carne aviar es la carne de mayor crecimiento del mundo, pero **~87 % se consume en el país donde se produce** `[ESTIMACIÓN]`. El comercio internacional es un mercado de excedentes, cortes y partes específicas, dominado por pocos exportadores de muy bajo costo.

---

## 2. Principales productores

| País | Producción | Período | Fuente | Estado | Comentario |
|---|---|---|---|---|---|
| China | 17,3 Mt (+5 %) | 2026 (pronóstico) | FTE-019 | [PVDP] | Crecimiento por inventario alto de abuelas y expansión de integradoras (FTE-019); un título de prensa sectorial habla de +9,3 % en el 1T-2026 `[PENDIENTE DE VALIDACIÓN]` (fuente no registrada) |
| Brasil | 15,8 Mt (+2 %) | 2026 (pronóstico) | FTE-019 | [PVDP] | Costos bajos y real débil |
| Estados Unidos | **no obtenido en esta sesión** | — | — | [PENDIENTE DE VALIDACIÓN] | Históricamente el mayor productor mundial (DPV-010 ampliado a series mundiales, ver DPV-025) |
| Unión Europea | no obtenido | — | — | [PENDIENTE DE VALIDACIÓN] | Cuota UE–Mercosur = 1,3 % de su producción (FTE-103) |
| Argentina | ~2,3 Mt (SAGyP) | 2025 | [`01_mercado`](../01_mercado/mercado_avicola_argentina.md) §1.3 | [PVDP] | ~2 % de la producción mundial `[ESTIMACIÓN]` |

> Faltan las cifras de EE.UU., UE, India, Rusia, México y Tailandia para una tabla completa. Se registra como dato faltante (DPV-025). No se completan de memoria.

---

## 3. Principales exportadores

| País / bloque | Exportación | Período | Fuente | Estado | Perfil de producto y destinos |
|---|---|---|---|---|---|
| **Brasil** | **5,324 Mt**; USD 9.790 M (−1,4 %) | 2025 | ABPA (FTE-087) | [PVDP] | ~36 % del comercio mundial (FTE-019). Todo el espectro: entero congelado (Medio Oriente), cortes (Japón, China, UE), garras (China), CMS (Filipinas, Sudáfrica). Destinos 2025: EAU 479,9 kt; Japón 402,9 kt; Arabia Saudita 397,2 kt; Sudáfrica 336 kt; Filipinas 264,2 kt (FTE-087). Precio medio 2025 ≈ 1.839 USD/t `[ESTIMACIÓN: 9.790 / 5,324]` |
| **Estados Unidos** | ~3,0 Mt (6,7 mil millones de libras) | 2025 y 2026 (pronóstico) | USDA (FTE-139) | [PVDP] | Cuartos traseros y carne oscura (México, Angola, Vietnam, Filipinas); garras tratadas térmicamente a China. Exporta ~13,9 % de su producción (FTE-120). Conversión a t: 6,7 × 0,4536 `[ESTIMACIÓN]` |
| **Unión Europea** | 3° exportador (volumen no obtenido) | 2025 | FTE-019 (extracto) | [PVDP · débil] | Países Bajos y Polonia; carne congelada, partes de bajo valor a África y Asia (ej.: 28–30 kt a Vietnam en 1S-2025, FTE-130) |
| **Tailandia** | 1,3 Mt; USD 4.250 M | 2025 | FTE-121 | [PVDP · débil] | **~70 % procesado/cocido.** Japón ~500 kt; Reino Unido ~200 kt; UE 170–180 kt. Precio medio ≈ 3.270 USD/t `[ESTIMACIÓN]`: el más alto entre los grandes por su mix de cocidos |
| **China** | 1,4 Mt (pronóstico 2025); ene–may 2026: 546.000 t (+51 %) | 2025–2026 | FTE-019, FTE-090 | [PVDP] | Pasó de ser el gran importador a exportador creciente: pechuga (más de la mitad en el 1T-2026), cortes con hueso y cocidos a Japón, Hong Kong, Rusia, Medio Oriente, Irak, África y Asia Central |
| **Turquía** | 420.000 t (+5 %) | 2025 (estimación USDA) | FTE-122 | [PVDP] | Halal por origen y cercanía a Irak (180.000 t en 2024, −24 %), Siria, Arabia Saudita. Exportaciones a Irak −57 % en el 1S-2025 (IAAP y protección iraquí) |
| **Ucrania** | 436.000 t (−2 %) | 2025 | FTE-123 | [PVDP · débil] | MHP explica ~368.600 t. Destinos: UE 30,6 %, Medio Oriente 27,2 %, Europa extra-UE 22,6 %. Acceso a la UE limitado por cuotas desde 2024–2025 |
| **Rusia** | 134.000 t solo a China (USD 381 M) | ene–oct 2025 | FTE-090 (extracto TASS) | [PVDP · débil] | 25,9 % de las garras importadas por China en 2025 (FTE-089) |
| **Argentina** | 206.436 t (definición amplia CEPA); USD 246,9 M | 2025 | [`01_mercado/exportaciones.md`](../01_mercado/exportaciones.md) | [PVDP] | ~1–1,5 % del comercio mundial `[ESTIMACIÓN; definiciones no homogéneas]`. Precio medio ~1.050–1.200 USD/t. **Exportador marginal y precio-aceptante** |

### 3.1 Ventajas competitivas de los líderes

| Líder | Ventajas | Implicancia para un entrante argentino |
|---|---|---|
| Brasil | Costo de grano y escala; integradoras globales (BRF, JBS/Seara); >150 destinos; habilitaciones consolidadas (Halal sin aturdimiento para Arabia Saudita, UE, Japón, China); plantas dedicadas por mercado; logística portuaria del sur; **regionalización** que acota cierres (China reabrió ~5,5 meses después del brote de may-2025 y la UE a los ~4 meses, con zonificación: FTE-088) | Compite en los mismos productos y destinos que Argentina, con más escala y más peso diplomático. Es el formador de precio en Medio Oriente, África, Chile y el propio mercado argentino (importaciones) |
| EE.UU. | Grano barato; demanda interna de carne blanca que deja la carne oscura (cuartos) como excedente exportable barato | Pone un **techo bajo** al precio internacional del cuarto trasero |
| Tailandia | Mano de obra y know-how en **cocidos** de alto valor; acceso preferente a Japón, UK y UE (cocidos no sufren las mismas barreras sanitarias por IAAP que la carne cruda) | Muestra que el valor está en el procesado, pero exige otra escala industrial y otra planta |
| China | Escala y costo; ahora con excedentes | Reduce su demanda de importación y compite como exportador en Asia (Japón, Hong Kong) |
| Turquía / Ucrania | Cercanía y Halal (Turquía); costo y cuotas UE (Ucrania) | Compiten en Medio Oriente y UE |
| UE | Estándares altos, mercado interno protegido; exporta partes de bajo valor | Protegida por aranceles; el acceso para terceros se da por cuotas |

**Ventaja transversal de los líderes: poder negociar acceso sanitario (regionalización) y mantener abiertos los mercados durante un brote.** Argentina lo logró parcialmente con Arabia Saudita, EAU, Vietnam, Singapur y Brasil (FTE-097), pero no con China, la UE, Chile ni Japón en 2026 (ver [`mercados_por_pais.md`](mercados_por_pais.md)).

---

## 4. Principales importadores

| Importador | Volumen / indicador | Período | Principales proveedores | Fuente | Estado |
|---|---|---|---|---|---|
| Japón | ~647.000 t | 2024–2025 (período a confirmar) | Brasil (402,9 kt en 2025), Tailandia (~500 kt, mayormente cocido) | FTE-127, FTE-087, FTE-121 | [PVDP · débil] (las cifras de distintas fuentes no cierran: cocidos vs carne cruda) |
| México | 1,1 Mt (+8 %) | 2026 (pronóstico) | EE.UU.; Brasil con acceso libre de aranceles | FTE-125 | [PVDP] |
| Unión Europea | 388.000 t (−4 %) | 2024 | Brasil (49 % en 4T-2024), Ucrania, Tailandia | FTE-112 | [PVDP] |
| Reino Unido | Importador relevante (volumen no obtenido) | 2025 | Tailandia (~200 kt, mayormente cocido), Brasil, UE | FTE-121 | [PVDP · débil]; tamaño `[PENDIENTE DE VALIDACIÓN]` (DPV-025) |
| Emiratos Árabes Unidos | 573.000 t | 2024 | Brasil (479,9 kt en 2025) | FTE-117, FTE-087 | [PVDP · débil] (FTE-117 es consultora; el dato de Brasil es ABPA) |
| Arabia Saudita | 509.000 t | 2024 | Brasil (~70 % en 2025; 397,2 kt) | FTE-117, FTE-087, FTE-113 | [PVDP · débil] |
| Qatar / Omán / Kuwait | 147.000 t / ~5,9 % / ~5,5 % del CCG | 2024 | Brasil | FTE-117 | [PVDP · débil] |
| Filipinas | Brasil: 264,2 kt (2025); 41,3 % del mercado de carnes importadas | 2025 | Brasil (>60 % de su pollo es CMS), EE.UU. | FTE-087, FTE-131 | [PVDP] |
| Sudáfrica | Brasil: 336 kt (2025) | 2025 | Brasil (>50 % del pollo congelado importado), UE, EE.UU., Argentina | FTE-087, FTE-128 | [PVDP] |
| China | En caída; garras ~3.500 USD/t | 2025–2026 | Brasil (47,9 % de garras), Rusia (25,9 %), Tailandia, EE.UU., Belarús; Chile y Argentina >10.000 t cada uno en 2025 | FTE-089, FTE-090 | [PVDP] |
| Vietnam | ~11 % del consumo es importado; 1S-2025: EE.UU. 115–120 kt, UE 28–30 kt, Brasil 24–26 kt | 2025 | EE.UU. (cuartos traseros) | FTE-130 | [PVDP · débil] |
| Irak | Turquía 180.000 t (2024) | 2024 | Turquía, Brasil, China | FTE-122 | [PVDP] |
| África subsahariana | Brasil >1 Mt a África en 2025; Angola 106.346 t | 2025 | Brasil, EE.UU., UE | FTE-129 | [PVDP · débil] |
| Chile | ~100.000 t/año `[ESTIMACIÓN: 33.382 t = 57,3 % en 7 meses]` | ene–jul 2025 | Brasil 57,3 %, EE.UU. 34,1 %, **Argentina 8,1 %** | FTE-126 | [PVDP] |

**Lectura:**

1. **Mercado grande ≠ mercado accesible.** De los cinco mayores importadores, México no está confirmado como habilitado para Argentina, Japón reabrió recién el 2026-09-08, la UE funciona por cuotas, Arabia Saudita exige Halal sin aturdimiento y China está cerrada (ver [`mercados_por_pais.md`](mercados_por_pais.md)).
2. **Los importadores del Golfo se autoabastecen cada vez más:** Arabia Saudita pasó de 45 % de autoabastecimiento (2016) a 68 % (2022) con meta de 80 % en 2025; un extracto habla de ~90 % (FTE-114, contradicción registrada). El mercado importador saudita tiende a achicarse.
3. **China dejó de ser un importador en expansión:** su producción crece más que su demanda, sus importaciones caen y sus exportaciones crecen +51 % (FTE-090). Esto afecta directamente la tesis "garras a China".

---

## 5. Evolución reciente (2023–2026)

| Fecha | Evento | Efecto | Fuente |
|---|---|---|---|
| 2023–2025 | IAAP recurrente en Argentina: cierres de China (mar-2023 a abr-2025 y desde ago-2025), UE, Chile | Exportación argentina volátil; precio medio cae de ~1.700 a ~1.100 USD/t al perder China | [`01_mercado/exportaciones.md`](../01_mercado/exportaciones.md), FTE-092 |
| 2025-05-16 | Primer caso de IAAP comercial en Brasil (Montenegro, RS) | China suspende a Brasil hasta nov-2025; la UE cierra ~4 meses con zonificación; precios en Medio Oriente en mínimos (pechuga CIF 2.700 USD/t el 2025-05-30) | FTE-088, FTE-118 |
| 2025 | Brasil igual logra récord de exportación (5,324 Mt) | Muestra la resiliencia de un exportador diversificado | FTE-087 |
| 2025–2026 | China pasa a exportador neto creciente | Menor demanda de importación de garras y alas; competencia en Asia | FTE-090 |
| 2026-05-01 | Aplicación provisional del acuerdo UE–Mercosur (cuota aviar 180.000 t para el bloque) | Acceso con arancel preferencial, reparto intra-Mercosur pendiente | FTE-103, FTE-105 |
| 2026-04-01 | S&P Global Platts lanza precios diarios CIF Jebel Ali (pollo entero, cuarto trasero, carne para shawarma) | Mejora la transparencia de precios en Medio Oriente | FTE-118 |
| 2026-09-03 | La UE aplica el art. 118 del Reg. (UE) 2019/6 (antimicrobianos); **Brasil queda excluido** de la lista para aves, bovinos y otros | Ventana temporal para otros proveedores. La auditoría de la Comisión (informe del 2026-09-28) fue favorable para aves de Brasil: su regreso requiere voto de los Estados miembros | FTE-107, FTE-108 |
| 2026 | Argentina: brote de feb-2026, autodeclaración de país libre (publicada ante la OMSA el 6-may según FTE-098; abril según FTE-011), reaperturas de Chile/Perú (jun), Corea (2026-08-10), UE (2026-08-17), Japón (2026-09-08). China sigue cerrada | Exportación argentina 1S-2026: −27,2 % en valor según INDEC (USD 93 M) o −38 % según el Consejo Agroindustrial (contradicción) | FTE-094, FTE-095, FTE-101, FTE-102 |
| 2026-09-16 | Caso de IAAP en aves de traspatio (Carlos Spegazzini, BA) | Según SENASA no afecta el estatus ni el comercio | FTE-099 |

---

## 6. Tendencias de consumo y crecimiento por regiones

Fuente principal: OECD-FAO Agricultural Outlook 2025-2034 (FTE-124) `[PVDP]`.

| Región | Tendencia | Relevancia para Argentina |
|---|---|---|
| Asia (55 % del crecimiento de la producción de carne) | Crecimiento del consumo en Indonesia, Filipinas, Vietnam, India; China crece pero se autoabastece | Vietnam ya es el primer destino argentino (~17 % en 2024; ~20–21 % en 2026, FTE-091). Filipinas crece pero con proveedores muy baratos (CMS de Brasil) |
| África (+33 % del consumo de carne a 2034 por crecimiento poblacional) | Importación de partes baratas (cuartos, CMS, menudencias) y pollo entero | Destino natural de partes de bajo valor. Riesgo de cobro y aranceles/antidumping (Sudáfrica) |
| Medio Oriente | Demanda Halal estable, pero autoabastecimiento creciente (Arabia Saudita) | Requiere Halal; mercado de precio (Brasil) |
| América Latina | Importadores netos cercanos (Chile, Perú, México) | Ventaja logística (camión a Chile); competencia de Brasil y EE.UU. |
| Europa | Demanda de pechuga y preparados; importación por cuotas | Acceso legal limitado a cuotas; competitividad frente a Brasil a verificar |
| Japón / Corea | Alto valor, exigencia de calidad y especificación (deshuesado de pata, cocidos) | Reaperturas 2026: oportunidad a investigar, no a presumir |

**Tendencias de producto** (cualitativas, `[PVDP · débil]` salvo indicación): crecimiento de productos cocidos y listos para consumir (Tailandia 70 % procesado, FTE-121); pechuga como producto de exportación china (FTE-090); cuarto trasero y CMS como insumos baratos para industria (México, Filipinas, Sudáfrica: FTE-120, FTE-131, FTE-128); garras dependientes casi exclusivamente de China/Hong Kong/Vietnam.

---

## 7. Implicancias para el proyecto

1. **Argentina es un exportador pequeño y precio-aceptante** (~1–1,5 % del comercio mundial). Un nuevo actor argentino no mueve precios: debe competir con Brasil en costo, habilitaciones y regularidad.
2. **El valor internacional está en tres lugares:** (a) partes de bajo valor local que otro mercado paga más (garras, alas, menudencias); (b) productos de alta especificación (deshuesado para Japón, pechuga para UE/Golfo); (c) cocidos/procesados (Tailandia). Cada uno exige una planta y habilitaciones distintas.
3. **El acceso sanitario es el cuello de botella argentino**, no la demanda mundial: con IAAP recurrente, los mercados que exigen país libre se cierran meses o años (China: ver [`mercados_por_pais.md` §3](mercados_por_pais.md)). La regionalización reconocida por algunos destinos es un activo del país, no de la empresa.
4. **Los grandes compradores se autoabastecen cada vez más** (China, Arabia Saudita): diseñar el proyecto sobre la demanda de importación de esos mercados es riesgoso.
5. **Ventanas coyunturales** (Brasil fuera de la UE desde el 2026-09-03; crisis de GTA en Argentina) no son estrategia: la exclusión de Brasil de la UE podría revertirse en semanas (FTE-108).
