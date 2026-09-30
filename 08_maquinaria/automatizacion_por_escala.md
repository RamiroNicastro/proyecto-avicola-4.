# Manual vs semiautomático vs automático, por operación y por escala

**Fecha:** 2026-09-30 · **Versión:** 1.1 (corrección conceptual: sin umbral fijo de evisceración manual; niveles como arquitectura de referencia, no obligación) · Fase 0

> **Alcance:** para cada operación, qué puede hacerse a mano, con semiautomatización o con automatización completa, y qué nivel **conviene estudiar** en cada escala. **No** se decide el nivel de automatización (DEC-09A-01), **no** se elige equipo ni proveedor, **no** se calcula dotación (`18_recursos_humanos`) ni CAPEX/OPEX.
> **Base:** niveles por equipo en [`matriz_equipos.csv`](matriz_equipos.csv) (columnas `nivel_*`); ritmos y puestos equivalentes de [`../05_proceso_industrial/modelo_capacidad_proceso.py`](../05_proceso_industrial/modelo_capacidad_proceso.py). Las valoraciones cualitativas son `[SUPUESTO]` (SUP-09A-05) a validar con proveedores y plantas en operación.
> **Regla:** **no** se concluye que más automatización sea siempre mejor. Automatizar cambia mano de obra por capital, repuestos, técnicos, energía, dependencia de proveedor y rigidez.

---

## 1. Definiciones

| Nivel | Qué significa | Ejemplo |
|---|---|---|
| **Manual (M)** | La operación la hace una persona con herramientas simples | Eviscerar con cuchara y cuchillo; trozar en mesa con sierra |
| **Mecanizado (Mc)** | Una máquina ejecuta la operación física, pero sin control automático del proceso ni sincronía con la línea; la persona la alimenta, regula y vigila | Escaldadora por lotes con termostato; desplumadora de tambor; sierra de cinta; transportador aéreo simple |
| **Semiautomático (S)** | Una máquina hace el trabajo pesado o repetitivo; una persona carga, guía o controla cada pieza | Línea de conos para deshuese; peladora de mollejas cargada a mano; embolsadora asistida |
| **Automático (A)** | La máquina procesa en línea sin intervención por pieza, con control de parámetros; las personas supervisan, reparan y hacen el repaso | Evisceradora rotativa; trozadora en línea; balanza de línea con distribución |

Los niveles de las tablas siguientes son una **arquitectura de referencia a estudiar**, no una obligación técnica ni normativa: para una planta comercial habilitada probablemente se estudien soluciones mecanizadas o automatizadas en varias etapas, pero **no se afirma que otra configuración sea imposible** salvo respaldo normativo (norma no leída, DPV-09A-03).

## 2. Matriz por operación (criterios cualitativos)

Escala de valoración: ▲ favorable · ● neutro · ▼ desfavorable, **comparando automático contra manual** en esa operación. "Manual hasta" = ritmo orientativo por encima del cual el manual deja de ser práctico (solo donde hay alguna referencia).

| Operación | Manual posible | Semi | Auto | Sensibilidad a escala | Mano de obra (auto vs manual) | Consistencia | Higiene | Mantenimiento | Flexibilidad |
|---|---|---|---|---|---|---|---|---|---|
| Descarga de aves | Sí (cajones) | Cinta | Volcador de módulos | Alta | ▲ | ▲ (menos golpes) | ● | ▼ | ● |
| Colgado | **Sí (casi universal)** | — | Poco difundido | Media | — | ● | ● | — | ▲ (manual) |
| Aturdido | No | — | Sí (eléctrico o CAS) | Baja | — | ▲ | ● | ● | ● |
| Degüello | Sí | — | Sí + repaso manual | Media | ▲ | ▲ | ● | ▼ | ● |
| Escaldado | Por lotes (artesanal) | — | Tanque en línea | Alta | ▲ | ▲ | ● | ● | ● |
| Desplumado | Por lotes (tambor) | — | En línea | Alta | ▲ | ▲ | ● | ▼ (dedos) | ● |
| Corte de patas / cabeza | Sí | Guías pasivas | Sí | Media | ▲ | ▲ | ● | ▼ | ● |
| Transferencia a evisceración | Sí (recolgado) | — | Sí | Alta | ▲ | ▲ | ▲ (menos contacto) | ▼ | ▼ |
| Corte de cloaca y apertura | Sí | Pistola de vacío | Sí | Media | ▲ | ▲ | ▲ si calibrada · ▼ si el lote es desparejo | ▼ | ▼ (tamaño de ave) |
| **Evisceración** | **Sí**; un fabricante documenta evisceración manual en línea hasta ~1.600 broilers/h (BAADER Compact Plant 396, FTE-09A-007); sin umbral fijo | Sí | Sí | **Muy alta** | ▲▲ | ▲ | ▲/▼ (rotura de intestino si mal calibrada) | ▼▼ (técnico especializado) | ▼ (pesos variables) |
| Presentación para inspección | Sí (vísceras colgando) | Bandejas | Línea sincronizada | Alta | ▲ | ▲ | ▲ | ▼ | ● |
| Menudencias (cosecha, molleja) | Sí | Peladora | Sí | Media | ▲ | ▲ | ● | ▼ | ● |
| Lavado de carcasas | Duchas | — | Lavadora en línea | Media | ▲ | ▲ | ▲ | ● | ● |
| Enfriamiento | No (salvo artesanal) | — | Sí (inmersión/aire) | Alta | — | ▲ | ● | ● | ● |
| Clasificación por peso | Sí (mesa y balanza) | — | Balanza de línea | Alta | ▲ | ▲▲ | ● | ▼ | ▲ (programable) |
| **Trozado** | **Sí** | Sierra de cinta/disco | Trozadora modular | Alta | ▲ | ▲▲ (cortes uniformes) | ● | ▼ | ▼ (pocos programas) vs ▲ manual (cualquier corte) |
| **Deshuese** | **Sí (muy intensivo)** | Línea de conos | Máquinas por pieza | Alta | ▲▲ | ▲ | ● | ▼▼ (repuestos específicos) | ▼ (una máquina por pieza) |
| Fileteado / porcionado | Sí | — | Porcionadora | Media | ▲ | ▲▲ (peso fijo) | ● | ▼ | ▼ |
| Trimming | **Sí (siempre humano)** | — | Rayos X de apoyo | Baja | — | ● | ● | — | ▲ |
| Garras (pelado, clasificación) | Sí (lento) | Peladora | Clasificadora | Media | ▲ | ▲ | ● | ▼ | ● |
| Envasado (bolsa, bandeja) | Sí | Asistido | En línea | Alta | ▲ | ▲ | ▲ | ▼ | ▼ (cambios de formato) |
| Termosellado / termoformado / MAP | No | Termoselladora | Termoformadora | Media | ▲ | ▲ | ▲ | ▼ | ▼ |
| Encajonado / paletizado | Sí | Cerradora | Robot | Media | ▲ | ● | ● | ▼ | ● |
| Congelado | No | Túnel estático | Continuo/espiral | Alta | ▲ | ▲ | ● | ● | ▼ (espiral para un rango de productos) |
| Subproductos (transporte) | Sí (recipientes) | Canal de agua | Vacío/bombas | Alta | ▲ | ● | ▲ (sin cruces) | ▼ | ● |

**Patrón general:** la automatización mejora **consistencia** y reduce **mano de obra por ave**, pero empeora **mantenimiento** (repuestos y técnicos) y **flexibilidad** (sensibilidad a pesos desparejos y a cambios de producto). La higiene mejora solo si el equipo es de diseño higiénico y está bien calibrado.

## 3. Matriz por escala (nivel razonable a estudiar)

Ritmo operativo a 8 h netas: 312 / 625 / 1.250 / 2.500 aves/h (con 6 h: 417 / 833 / 1.667 / 3.333). Códigos como en [`catalogo_equipos.md`](catalogo_equipos.md): **M**, **Mc** (mecanizado), **S**, **A**, **O** (opcional según producto), **T** (tercerizar/postergar). "M/S" = comparar ambas.

| Operación | 2.500 aves/día | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Descarga | M | M/S | S/A | A |
| Colgado | M | M | M | M (más puestos y rotación) |
| Aturdido, escaldado, desplumado (arquitectura de referencia) | Mc/A | A | A | A |
| Degüello | M (o A + repaso) | M/S | A + repaso | A + repaso |
| Patas y cabeza | M | M/S | A | A |
| Transferencia | M | M | M/A | A |
| **Evisceración** | **M** (3–6 puestos eq.) | **M/S** (6–11) | **M/S/A a comparar** (manual: 11–21 puestos eq.; 1.250 aves/h, dentro del rango con evisceración manual documentado por un fabricante) | **S/A**, manual a comparar (21–42 puestos eq.) |
| Presentación para inspección | M | M/S | A | A |
| Menudencias | M | M | S/A | A |
| Enfriamiento (arquitectura de referencia) | A | A | A | A |
| Clasificación | M | M/S | A | A |
| Trozado | M | M/S | S/A | A |
| Deshuese | M | M | M/S (conos) | S + A por pieza (O) |
| Garras | O (si hay comprador) | O | S | S/A |
| CMS | T | T | O | O |
| Envasado | M/S | S | A | A |
| Congelado | T o S (túnel estático) | S | S/A | A |
| Subproductos (transporte) | M/S | S | A | A |

Puestos equivalentes de eviscerado manual: rango referencia–prudente de [`../05_proceso_industrial/cuellos_botella.md` §5](../05_proceso_industrial/cuellos_botella.md) (2 aves/min por operario, FTE-09A-025 `[PVDP]`; 50 % como variante prudente, SUP-09A-03). **No son dotación**: no incluyen rotación, pausas, ausentismo, repaso ni supervisión.

**Lecturas:**

1. **Arquitectura de referencia, no obligación:** para aturdido, escaldado, desplumado y enfriamiento se estudian equipos mecanizados o automáticos continuos en todas las escalas, porque es la configuración habitual de las plantas comerciales y la que ofrecen los fabricantes aun en rangos bajos (600–1.600 aves/h, FTE-09A-007; 150–1.500 aves/h, FTE-09A-015 `[PVDP]`). No se afirma que otra configuración sea técnicamente imposible: dependerá de la norma (no leída) y de la cotización.
2. **Evisceración: sin umbral fijo.** La transición entre evisceración manual, semiautomática y automática depende de velocidad, costo y disponibilidad de mano de obra, ergonomía, inspección, uniformidad, calidad, higiene y economía de escala. Equipos comerciales demuestran que la evisceración manual puede utilizarse al menos en escalas del orden de **1.600 aves/h** (BAADER Compact Plant 396). El umbral económico para Argentina debe determinarse con cotizaciones y productividad real (DPV-09A-05, DEC-09A-01). La cantidad de puestos manuales equivalentes (11–21 a 10.000 aves/día; 21–42 a 20.000) muestra el **tamaño del problema de personal**, no un límite técnico.
3. **El colgado sigue siendo manual** en todas las escalas: es el límite humano de la línea y crece en puestos con la escala.
4. **Trozado y deshuese dependen del mix, no solo de la escala:** una planta de 20.000 aves/día que vende entero casi no necesita trozado automático; una de 5.000 que deshuesa todo necesita mucha más gente o equipos.
5. **Opcionales (O):** garras, CMS, porcionado, deshuese automático y congelado continuo solo se justifican con mercado para el producto (DEC-031, DEC-029, DEC-030).

## 4. Cuándo más automatización NO es mejor

| Situación | Por qué el manual o semiautomático puede convenir |
|---|---|
| **Lotes desparejos de peso** (productores distintos, pesos variables) | Las máquinas se calibran para un rango; fuera de él rompen vísceras o cortan mal. Las personas se adaptan |
| **Muchos productos distintos y lotes chicos** | Cada cambio de programa o formato para la línea; el trozado manual cambia de corte sin parar |
| **Baja utilización** (planta llena al 30–50 %) | El equipo automático ocioso sigue exigiendo mantenimiento y técnicos |
| **Técnicos y repuestos lejanos** | Una evisceradora parada sin técnico en el país detiene la planta; 10 personas con cuchillo no se "rompen" juntas |
| **Escala 2.500–5.000** | La mano de obra por ave es mayor, pero la inversión automática no se diluye |
| **Arranque (curva de aprendizaje)** | Empezar con procesos manuales permite medir rendimientos reales y definir el producto antes de automatizarlo |
| **Operaciones de juicio** (trimming, inspección, clasificación de defectos) | La persona sigue siendo necesaria |

## 5. Cuándo la automatización se vuelve difícil de evitar

| Situación | Por qué |
|---|---|
| Ritmos altos en evisceración (sin umbral fijo; hay evisceración manual documentada hasta ~1.600 aves/h) | La cantidad de puestos manuales crece (espacio en línea, ergonomía, supervisión, higiene, uniformidad); el punto en que conviene automatizar se define con cotizaciones y productividad real |
| Escasez de mano de obra en la localización | El límite es la gente, no el capital (`10_localizacion`, `18_recursos_humanos`) |
| Exigencia de uniformidad (exportación, calibres, porciones de peso fijo) | Consistencia del corte y del peso |
| Dos turnos | Duplicar gente calificada en ambos turnos es más difícil que duplicar horas de máquina |
| Bienestar animal y exigencias de la UE | Aturdido y control de parámetros registrados |

## 6. Qué falta para decidir (DEC-09A-01)

Productividad real de operarios argentinos (DPV-09A-05), costo laboral y disponibilidad de personal por localización (`18_recursos_humanos`), capacidad real y requisitos de cada equipo (RFQ, [`requerimientos_cotizacion.md`](requerimientos_cotizacion.md)), servicio técnico local (DPV-09A-02), mix de productos (DEC-005) y CAPEX/OPEX comparados (`19_capex`, `20_opex`).
