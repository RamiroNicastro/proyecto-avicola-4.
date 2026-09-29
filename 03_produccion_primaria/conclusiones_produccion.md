# Conclusiones del estudio de producción primaria

**Fecha:** 2026-09-29 · **Versión:** 1.1 (auditoría del modelo físico, 2026-09-29) · Base: [`ciclo_productivo.md`](ciclo_productivo.md), [`alimentacion.md`](alimentacion.md), [`galpones.md`](galpones.md), [`bioseguridad.md`](bioseguridad.md), [`transporte_aves.md`](transporte_aves.md), [`modelos_integracion.md`](modelos_integracion.md), [`kpis_productivos.md`](kpis_productivos.md), [`guia_ramiro.md`](guia_ramiro.md), [`escenarios_produccion.csv`](escenarios_produccion.csv), [`modelo_escenarios_produccion.py`](modelo_escenarios_produccion.py)

> **No** se define el tamaño de la empresa, **no** se decide cuántos galpones construir, **no** se asume granja propia ni incubadora propia y **no** se construye el modelo financiero. Las plantas de 2.500–20.000 **aves faenadas/día** son **escenarios hipotéticos**. No se inicia el balance de masa, ni el dimensionamiento del frigorífico, ni la maquinaria.
> **Fuentes:** acceso directo bloqueado (cuarta sesión consecutiva, DPV-009). Toda cifra externa es `[PVDP]`; los parámetros de trabajo son `[ESTIMACIÓN]` o `[SUPUESTO]` (SUP-025 a SUP-034).

---

## 1. Diez hallazgos productivos principales

1. **La cadena física tiene tres categorías que no deben mezclarse:** pollitos BB alojados → aves cargadas (−3 a −8 % o más de mortalidad en granja) → aves faenadas (−0,2 a −0,5 % de mortalidad en transporte). Una planta de 10.000 aves faenadas/día con 5 días de faena necesita **~52.800 pollitos BB alojados por semana plena** (~50.600 en promedio anual, por los feriados).
2. **El alimento es la variable física dominante y el FCR la gobierna.** Perfil medio: **~4,6–5,4 kg de alimento por ave** faenada. **+0,1 de FCR = +5,9 % de alimento** (+290 t por millón de aves de 2,9 kg; +727 t/año en el escenario medio de 10.000 aves faenadas/día).
3. **Señal de riesgo en mortalidad.** Se encontró un estudio local de Entre Ríos (62 crianzas; FTE-151 `[PVDP]`) con mortalidades de **7,7–9,5 %**, superiores al supuesto medio del modelo (5 %). Debe validarse si ese desempeño es representativo de operaciones tecnificadas actuales; **no es un promedio argentino** (DPV-044).
4. **Capacidad de galpón ≠ producción anual y 365/edad ≠ ciclos/año.** Con 47 días de crianza y 15 días entre lotes salen **~5,7 ciclos/año** (rango razonable ~5–7); usar 365/edad sobreestima la capacidad **25–40 %**.
5. **La superficie depende sobre todo de densidad, peso y ciclos**, no de la mortalidad: para la misma planta, las combinaciones de supuestos mueven los m² **hasta ~3,3 veces**. Escenario medio de 10.000 aves faenadas/día: **~37.900 m²** (≈ 32 galpones de 1.200 m² o 16 de 2.400 m²).
6. **La tecnología del galpón define la densidad posible y el riesgo de calor.** Galpones tecnificados/túnel permiten ~35–42 kg/m² y mejores indicadores; los abiertos, ~25–33 kg/m². La comparación correcta es costo por kg vivo producido, no CAPEX por m².
7. **La energía es un riesgo de continuidad crítico:** en galpones intensivos/climatizados, una falla de ventilación durante períodos de calor puede provocar rápidamente estrés térmico y mortalidad significativa; la prensa registra mortandades en Entre Ríos y Santa Fe por calor y caídas de tensión (FTE-157 `[PVDP]`). Generación de respaldo, alarmas, procedimientos de emergencia y calidad de red son requisitos, no opciones.
8. **La bioseguridad es condición de acceso a mercados.** Hay normativa específica identificada (Res. SENASA 1699/2019 bioseguridad y distancias —1.000 m entre granjas según extractos, sin verificar alcance, excepciones, vigencia ni forma de medición—, 106/2013 cama, 86/2016 *Salmonella*, 575/2018 bienestar, 484/2017 compartimentos; todas `[PVDP]`). Los ejemplos de compartimentos identificados corresponden a empresas de genética; el universo actual y su aplicabilidad al engorde deben verificarse con SENASA.
9. **La distancia granja–planta es una restricción física** (ayuno total ≈ 8–12 h, DOA, merma, bioseguridad, flete de un producto voluminoso): las granjas deben estar en un **radio acotado** de la planta; la planta cerca de granjas y granos, y el producto terminado viaja al mercado.
10. **El modelo de abastecimiento (propio / integrado / compra / mixto) es una decisión de capital, control y riesgo sin ganador todavía.** La integración es el modelo dominante del sector y traslada el CAPEX de galpones al productor, pero exige capital de trabajo (físicamente, **~1.660 t de alimento** para los lotes de un ciclo de crianza en el escenario medio de 10.000 aves faenadas/día, sin contar plazos de pago y cobro) y know-how. La compra spot es flexible pero inestable y débil en bioseguridad. El pollito BB es un insumo concentrado cuya oferta no puede expandirse instantáneamente: ampliar reproductoras lleva del orden de 6–7 meses hasta el primer pollito adicional (cría hasta el inicio de postura + incubación; `[ESTIMACIÓN]` a verificar, DPV-045).

---

## 2. Rangos de peso, edad, FCR y mortalidad

| Variable | BAJO | MEDIO | ALTO | Clasificación |
|---|---|---|---|---|
| **Edad de faena** (perfil de mercado) | 35–40 d (38) | 45–50 d (47) | 52–56 d (54) | `[ESTIMACIÓN]` |
| **Peso vivo** (perfil de mercado) | 2,2–2,5 kg (2,4) | 2,7–3,0 kg (2,9) | 3,2–3,6 kg (3,4) | `[ESTIMACIÓN]`; campo AR 46–50 d ~3 kg (FTE-050), ~2,7 kg a ~50 d (FTE-154); Cobb ~2,86 kg a 42 d (FTE-140) `[PVDP]` |
| **FCR de campo** a 2,9 kg (desempeño) | 1,60 (favorable) | 1,70 | 1,85 (desfavorable) | `[ESTIMACIÓN]` SUP-028 |
| FCR a 2,4 kg / 3,4 kg | 1,48–1,73 | 1,58 / 1,82 | 1,72–1,97 | `[ESTIMACIÓN]` |
| **Mortalidad en granja** | 3 % | 5 % | 8 % (un estudio de Entre Ríos: 7,7–9,5 %, FTE-151 `[PVDP]`; señal a validar) | `[SUPUESTO]` SUP-026 |
| Mortalidad en transporte | 0,2 % | 0,3 % | 0,5 % | `[SUPUESTO]` SUP-026 |
| Ganancia diaria (perfil medio) | ~52–55 g/d | ~58–62 g/d | ~64–68 g/d | `[ESTIMACIÓN]` |
| Uniformidad (CV) | > 12 % | 9–11 % | ≤ 8 % | `[ESTIMACIÓN]` |
| Densidad final | 30 kg/m² | 35 kg/m² | 39 kg/m² (42 máx. UE excepcional) | `[SUPUESTO]`; FTE-143, FTE-144 `[PVDP]` |
| Días entre lotes | 20 | 15 | 12 | `[SUPUESTO]` SUP-029 |
| Ciclos/año | ~4,8 (pesado, 20 d entre lotes) | ~5,7 (medio, 15 d) | ~7,1 (liviano, 12 d) | `[ESTIMACIÓN]`; rango razonable ~5–7 |

---

## 3. Escenarios físicos (perfil medio, 5 días de faena/semana)

> **ESCENARIOS, no diseño recomendado.** "Planta de N aves/día" = N **aves efectivamente faenadas** por día de faena. Formato: favorable / **medio** / desfavorable. Con 6 días/semana, todo +20 %. Rango completo en el CSV y en [`ciclo_productivo.md` §6.7](ciclo_productivo.md). **Versión 1.1:** pollitos por semana plena y galpones corregidos (ver §13).

Cadena: **pollitos BB alojados** −(mortalidad en granja)→ **aves cargadas** −(mortalidad en transporte)→ **aves faenadas**. Semana plena = semana sin feriados (ritmo nominal); promedio anual = total anual / 52,14 (incluye feriados: 250 o 300 días de faena/año).

| Planta (aves **faenadas**/día) | Aves faenadas/semana plena | Aves cargadas/semana plena | **Pollitos BB alojados/semana plena** | Pollitos BB/semana (promedio anual) | Aves faenadas/año | Pollitos BB alojados/año | Capacidad de alojamiento (plazas) | Aves vivas simultáneas (ritmo pleno) |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 12.500 | 12.525 / **12.538** / 12.563 | 12.912 / **13.197** / 13.655 | 12.382 / **12.655** / 13.094 | 625.000 | 645.621 / **659.874** / 682.762 | 112.199 / **120.507** / 134.742 | 85.397 / **86.396** / 88.018 |
| 5.000 | 25.000 | 25.050 / **25.075** / 25.126 | 25.825 / **26.395** / 27.310 | 24.764 / **25.310** / 26.188 | 1.250.000 | 1.291.242 / **1.319.749** / 1.365.523 | 224.399 / **241.014** / 269.485 | 170.794 / **172.793** / 176.035 |
| 10.000 | 50.000 | 50.100 / **50.150** / 50.251 | 51.650 / **52.790** / 54.621 | 49.527 / **50.620** / 52.376 | 2.500.000 | 2.582.485 / **2.639.497** / 2.731.047 | 448.797 / **482.029** / 538.969 | 341.589 / **345.586** / 352.071 |
| 20.000 | 100.000 | 100.200 / **100.301** / 100.503 | 103.299 / **105.580** / 109.242 | 99.054 / **101.241** / 104.752 | 5.000.000 | 5.164.969 / **5.278.995** / 5.462.093 | 897.594 / **964.058** / 1.077.939 | 683.178 / **691.171** / 704.142 |

Prueba manual (10.000 aves faenadas/día, medio): 10.000 × 5 = 50.000 aves faenadas/semana plena → / 0,997 = 50.150 aves cargadas → / 0,95 = **52.790 pollitos alojados** (> 50.000 / 0,95 = 52.632 ✔). Detalle en [`ciclo_productivo.md` §6.4](ciclo_productivo.md).

## 4. Alimento asociado (perfil medio, 5 días/semana)

| Planta (aves **faenadas**/día) | kg/ave faenada | t/semana plena | t/semana (promedio) | t/mes (promedio) | t/año | de las cuales terminación (~68 %) | Alimento de un ciclo de crianza (capital de trabajo físico) |
|---|---|---|---|---|---|---|---|
| 2.500 | 4,65 / **4,94** / 5,39 | 58 / **62** / 67 | 56 / **59** / 65 | 242 / **258** / 281 | 2.906 / **3.091** / 3.370 | ~2.100 | 390 / **415** / 453 |
| 5.000 | 4,65 / **4,94** / 5,39 | 116 / **124** / 135 | 111 / **119** / 129 | 484 / **515** / 562 | 5.812 / **6.181** / 6.740 | ~4.200 | 780 / **830** / 905 |
| 10.000 | 4,65 / **4,94** / 5,39 | 232 / **247** / 270 | 223 / **237** / 259 | 969 / **1.030** / 1.123 | 11.623 / **12.362** / 13.480 | ~8.400 | 1.561 / **1.660** / 1.810 |
| 20.000 | 4,65 / **4,94** / 5,39 | 465 / **494** / 539 | 446 / **474** / 517 | 1.937 / **2.060** / 2.247 | 23.246 / **24.724** / 26.960 | ~16.900 | 3.122 / **3.320** / 3.620 |

Reparto (perfil medio): inicio ~5 %, crecimiento ~27 %, terminación ~68 %. Maíz ~60 % y harina de soja ~30 % del tonelaje (ilustrativo). Rango completo: **2.200–40.400 t/año** según planta y supuestos. Agua de bebida (medio): **~15 / 30 / 61 / 122 m³/día** promedio anual, con picos de verano ×2–3 y sin contar el agua de *cooling*. **El alimento y el agua anuales no cambiaron en la versión 1.1.**

## 5. Superficie aproximada de galpones (perfil medio, 5 días/semana)

| Planta (aves **faenadas**/día) | m² de galpón | Galpones de 1.200 m² | Galpones de 1.800 m² | Galpones de 2.400 m² | Rango completo de m² |
|---|---|---|---|---|---|
| 2.500 | 8.093 / **9.486** / 11.983 | 6,7 / **7,9** / 10,0 | 4,5 / **5,3** / 6,7 | 3,4 / **4,0** / 5,0 | 5.676–18.620 |
| 5.000 | 16.185 / **18.971** / 23.966 | 13,5 / **15,8** / 20,0 | 9,0 / **10,5** / 13,3 | 6,7 / **7,9** / 10,0 | 11.352–37.241 |
| 10.000 | 32.371 / **37.943** / 47.932 | 27,0 / **31,6** / 39,9 | 18,0 / **21,1** / 26,6 | 13,5 / **15,8** / 20,0 | 22.703–74.481 |
| 20.000 | 64.742 / **75.885** / 95.865 | 54,0 / **63,2** / 79,9 | 36,0 / **42,2** / 53,3 | 27,0 / **31,6** / 39,9 | 45.406–148.963 |

Galpones sin redondear y **sin reserva**: son equivalentes de superficie, **no una recomendación de cuántos construir**. En el caso de integración, esa superficie sería **de terceros**. Dimensionados para sostener el ritmo de una semana plena (utilización anual ~0,96).

## 6. Granjas propias vs integrados vs compra (síntesis)

| | A. Propias | B. Integrados | C. Compra de pollo vivo |
|---|---|---|---|
| Capital (CAPEX) | Muy alto | Bajo | Nulo |
| Capital de trabajo | Alto | Alto | Bajo |
| Control y bioseguridad | Máximos | Altos con contrato y auditoría | Mínimos |
| Riesgo productivo | Propio | Compartido | Del proveedor |
| Riesgo de precio | Granos | Granos | Precio del pollo vivo |
| Flexibilidad | Baja | Media | Alta (si hay oferta) |
| Know-how requerido | Máximo | Alto | Bajo en crianza |
| Escalabilidad | Lenta y cara | Rápida si hay productores | Limitada por el spot |
| Estabilidad de suministro | Alta | Media–alta | Baja |
| Exportación/trazabilidad | Plena | Buena | Débil |

**Mixto** (base propia pequeña + integrados + spot como amortiguador): útil para crecer sin CAPEX excesivo, dispersar el riesgo sanitario, absorber demanda variable y aprender. **Sin ganador** (DEC-020). Detalle: [`modelos_integracion.md`](modelos_integracion.md).

## 7. Principales riesgos productivos

| Riesgo | Probabilidad | Impacto | Mitigación conceptual |
|---|---|---|---|
| **Influenza aviar (IAAP)** en la zona o en granjas propias/integradas | Media–alta (brotes en 2023, 2025, 2026) | Muy alto: eliminación de aves, inmovilización de granjas, cierre de exportaciones, caída de precios | Bioseguridad, localización de baja densidad avícola, dispersión geográfica de granjas, plan de contingencia |
| **Golpe de calor / corte o caída de tensión** | Alta en verano | Alto: estrés térmico y mortalidad significativa si falla la ventilación con calor | Galpones con cooling, generador automático, alarmas, menor densidad estival |
| **Mortalidad y FCR peores que lo supuesto** | Media–alta (un estudio de Entre Ríos registró 7,7–9,5 %; representatividad a validar) | Alto: más pollitos y más alimento por kg | Validar con datos de campo (DPV-044); asistencia técnica; pago por desempeño |
| **Falta de pollito BB o calidad irregular** | Media | Alto: sin pollito no hay lote; la oferta no se expande instantáneamente (ciclo de reproductoras) | Contratos anuales, dos proveedores, especificaciones de calidad |
| **Falta de productores integrables** confiables en el radio de la planta | Desconocida | Muy alto para el modelo B | Relevamiento en campo (DPV-048); contratos atractivos; base propia |
| **Precio y disponibilidad de granos** | Alta volatilidad | Muy alto (principal costo) | Localización cercana a granos; estrategia de compra (`14_alimento_balanceado`) |
| **Enfermedades endémicas** (Gumboro, bronquitis, coccidiosis, *Salmonella*) | Media | Medio–alto: FCR, decomisos, faena controlada | Plan sanitario, veterinario, bioseguridad |
| **Calidad de agua** (arsénico, sales, contaminación) | Media según zona | Medio–alto | Análisis antes de elegir sitio (DPV-053) |
| **Transporte** (DOA, merma, bienestar) | Media | Medio | Radio acotado, transporte nocturno en verano, capacitación de cuadrillas |
| **Conflicto con integrados** (pagos, contratos informales) | Media (antecedentes sectoriales) | Alto | Contratos escritos, pago puntual, reglas claras |
| **Regulatorio / ambiental** (cama, mortalidad, distancias, olores) | Media | Medio | Habilitaciones y gestión de residuos desde el diseño (DPV-046, DPV-057) |

Se incorporarán a la matriz de `22_riesgos`.

---

## 8. Información a conseguir fuera de Internet

### 8.1 Para pedir a contactos (productores, integradores, veterinarios, técnicos del sector)

| Información | A quién | Registro |
|---|---|---|
| Registros de 6–12 lotes: edad, peso, FCR, mortalidad (y de 7 días), días entre lotes, kg/m² por estación y tipo de galpón | Productores integrados, asesores, INTA (EEA Concepción del Uruguay) | DPV-044 |
| Esquemas de pago a integrados (por ave/kg, premios y castigos, plazo), contratos tipo y problemas frecuentes | Productores integrados, cámaras de productores | DPV-048 |
| Cantidad de productores y m² de galpón disponibles o subutilizados en zonas candidatas (incluida la situación de ex-integrados de GTA, sin suponer disponibilidad) | Productores, técnicos, municipios, cooperativas | DPV-048, DPV-016 |
| Oferta y precio de pollo vivo spot; quién vende y con qué regularidad | Productores independientes, frigoríficos chicos | DPV-049 |
| Incubadoras que venden a terceros: capacidad, genética, calidad, contratos | Incubadoras, empresas de genética | DPV-006, DPV-047 |
| Plan sanitario/vacunal típico y costos de sanidad; laboratorios de diagnóstico | Veterinarios avícolas | DPV-056 |
| Radio típico granja–planta, DOA y merma reales, tarifas de captura y flete | Frigoríficos, contratistas de captura, transportistas | DPV-054 |
| Tablas completas de manuales Cobb/Ross y normas SENASA (descarga manual por el promotor) | Promotor (descarga) | DPV-045, DPV-046 |

### 8.2 Para cotizar (cuando la fase lo habilite)

| Información | A quién | Registro |
|---|---|---|
| Galpón por tipo (convencional, climatizado, túnel, dark house) y equipamiento (comederos, bebederos, ventilación, cooling, calefacción, controlador, generador) | Constructores y proveedores de equipamiento avícola (relevamiento, sin selección) | DPV-051 |
| Pollito BB (precio, fórmula de ajuste, plazo) | Incubadoras | DPV-047 |
| Alimento balanceado puesto en granja (por fase) y materias primas (maíz, harina de soja, núcleo) con flete | Fábricas de alimento, acopios, corredores | DPV-050 |
| Energía: tarifas rurales, costo de extender líneas, gas natural vs GLP | Distribuidoras eléctricas y de gas | DPV-052 |
| Perforación, análisis y tratamiento de agua | Perforistas, laboratorios | DPV-053 |
| Captura y transporte de aves vivas; lavado de camiones | Contratistas, transportistas | DPV-054 |
| Tierra (compra o alquiler) y alquiler de galpones existentes | Inmobiliarias rurales, productores | DPV-057 |

### 8.3 Para validar en visitas

| Qué observar | Dónde | Registro |
|---|---|---|
| Estado real de galpones y equipos; bioseguridad aplicada (no declarada) | Granjas integradas y de productores independientes | DPV-048 |
| Calidad de cama, olor a amoníaco, uniformidad visual, manejo de mortalidad | Granjas en distintas edades del lote | DPV-044 |
| Calidad de la red eléctrica, generador y alarmas funcionando | Granjas en zonas candidatas | DPV-052 |
| Fuentes de agua y reservas | Granjas | DPV-053 |
| Captura nocturna, carga y recepción en planta; lavado de camiones | Frigorífico y granja durante una carga | DPV-054 |
| Distancias reales a otras granjas y caminos rurales en época de lluvia | Zonas candidatas | DPV-057, DEC-003 |
| Recepción de pollitos y primera semana | Granja + incubadora | DPV-047 |

---

## 9. Conceptos que Ramiro debe aprender

Resumen en [`guia_ramiro.md`](guia_ramiro.md): los 10 conceptos (pollitos ≠ faenados; FCR y alimento; FCR según peso; capacidad ≠ producción; ciclos ≠ 365/edad; densidad en kg/m²; peso = decisión comercial; bioseguridad = mercados; dependencia eléctrica; propio/integrado/compra = capital-control-riesgo), los 10 indicadores y las preguntas para productores, incubadoras e integradores.

---

## 10. Datos débiles e inconsistencias

| Tema | Problema | Registro |
|---|---|---|
| Mortalidad de campo | Un solo estudio local de Entre Ríos (año de los datos a confirmar) con 7,7–9,5 %, frente a 5 % usado como "medio"; no generalizable sin validar | DPV-044 |
| FCR de campo | Sin datos argentinos por zona y tipo de galpón; valores supuestos | DPV-044 |
| Manuales genéticos | Solo un valor de Cobb leído en extracto (~2,86 kg a 42 d); tablas completas no leídas | DPV-045 |
| Normativa SENASA | Resoluciones citadas por extractos; texto completo no leído (densidad, distancias, cama, transporte) | DPV-046, DPV-058 |
| Superficie y capacidad de granjas en ER | ~30.500 aves/granja (2017) vs ~1.400 m²/granja implican ~22 aves/m² (incompatible con 12–14) | DPV-055 |
| Energía | Extracto de potencia por ave inconsistente (descartado); kWh/m²/año de estudio extranjero; velocidad de calentamiento ante falla de ventilación sin fuente (estimación retirada en v1.1) | DPV-052 |
| Distancia mínima entre granjas | 1.000 m solo por extractos de la Res. 1699/2019 | DPV-046, DPV-057 |
| Compartimentos | Lista de empresas sin fecha; universo actual y aplicabilidad al engorde sin verificar | DPV-046 |
| Plazo de expansión del pollito BB | ~6–7 meses estimados por ciclo de reproductoras; semanas exactas sin verificar | DPV-045 |
| Curva de consumo por fase | Orden de magnitud con forma de manual, no tabla verificada | SUP-032, DPV-045 |
| Densidad de carga en transporte y aves por camión | No leídos / supuestos | DPV-054, SUP-033 |
| Agua de *cooling* | No cuantificada | DPV-053 |

---

## 11. Control de calidad

- [x] Dato real (`[PVDP]` con FTE) separado de escenario (`ESCENARIO`, `[ESTIMACIÓN]`, `[SUPUESTO]`).
- [x] Ninguna conversión única: FCR en rango (1,48–1,97) y sensibilidad 1,5–1,9.
- [x] Ningún peso único: perfiles 2,4 / 2,9 / 3,4 kg.
- [x] Ninguna mortalidad única: 3 / 5 / 8 % (+ 12 % en sensibilidad) y tabla de 2–15 %.
- [x] Pollitos alojados, aves cargadas y aves faenadas separados en todas las tablas; "aves/día" siempre significa aves faenadas (v1.1).
- [x] Semana plena y promedio anual diferenciados; 52,14 semanas/año (v1.1).
- [x] Capacidad de alojamiento, aves simultáneas (ritmo pleno y promedio anual) y producción anual diferenciados.
- [x] Vacío sanitario incluido en los ciclos (10–21 días entre lotes + disponibilidad 0,97).
- [x] Unidades comprobadas (aves, kg vivo, t, m², m³, días); base de FCR declarada (de campo, kg vivo cargado).
- [x] Pruebas automáticas A–G, límite y fases: **todas correctas** en los 72 escenarios y sus variaciones (743 comprobaciones; ver [`ciclo_productivo.md` §8](ciclo_productivo.md)).
- [x] Datos débiles señalados (§10).
- [x] No se recomienda cantidad de galpones, tecnología, proveedor, localización ni modelo de abastecimiento.
- [ ] Verificación documental primaria (bloqueada; DPV-009, DPV-045, DPV-046).
- [ ] Datos de campo argentinos (DPV-044, DPV-048).

## 12. Evaluación de calidad

**MEDIA** como marco técnico y modelo físico de escenarios; **BAJA** como evidencia de campo argentina.

- **Fortalezas:** proceso completo descripto; modelo auditado (v1.1) con pruebas automáticas; separación explícita perfil de mercado vs desempeño; modelo reproducible con fórmulas, supuestos y verificaciones de balance; sensibilidad por variable; diferenciación capacidad/inventario/producción; normativa relevante identificada; comparación de modelos de abastecimiento sin sesgo; información de campo priorizada.
- **Debilidades:** ninguna fuente leída en su original (todas `[PVDP]`); casi sin datos argentinos de desempeño (un estudio de mortalidad); parámetros de FCR, uniformidad, consumo por fase, energía y transporte son estimaciones; sin costos (por diseño de la fase). Los escenarios sirven para **ordenar decisiones y preguntas**, no para diseñar granjas.

## 13. Auditoría del modelo físico (versión 1.1, 2026-09-29)

**Error encontrado en pollitos BB por semana.** La cadena de porcentajes estaba en el sentido correcto (aves cargadas = faenadas / (1 − DOA); pollitos = cargadas / (1 − m)), pero "pollitos/semana" se calculaba como total anual (250 días de faena) / 52, que equivale a solo ~4,8 días de faena por semana. Para 10.000 aves faenadas/día daba 50.760 pollitos/semana, **menos que el mínimo lógico de 52.632** (50.000 / 0,95). La capacidad de galpones se calculaba con ese promedio anual.

**Corrección:** se separan la **semana plena** (ritmo nominal, 5 o 6 días de faena) y el **promedio anual** (/52,14); la capacidad de alojamiento se dimensiona para la semana plena; se agregan aves cargadas, muertes en granja y en transporte, aves simultáneas a ritmo pleno y alimento de un ciclo de crianza (capital de trabajo físico).

| Variable (10.000 aves faenadas/día, 5 d, medio) | Versión 1 | Versión 1.1 | Cambio |
|---|---|---|---|
| Pollitos BB alojados/semana | 50.760 (mal rotulado) | **52.790** (semana plena) · 50.620 (promedio anual) | +4,0 % |
| Capacidad de alojamiento | 462.220 | 482.029 | +4,3 % |
| m² de galpón | 36.383 | 37.943 | +4,3 % |
| Galpones de 1.200 / 1.800 / 2.400 m² | 30,3 / 20,2 / 15,2 | 31,6 / 21,1 / 15,8 | +4,3 % |
| Aves vivas simultáneas | 331.383 (promedio) | 345.586 (ritmo pleno) · 331.383 (promedio) | nueva variable |
| Alimento t/año · agua m³/año | 12.362 · 22.252 | 12.362 · 22.252 | sin cambio |
| Alimento t/semana | 238 (anual / 52) | 247 (semana plena) · 237 (promedio) | aclarado |
| Capital de trabajo físico (alimento) | "1.600–2.100 t" (aproximación) | 1.660 t (ciclo de crianza a ritmo pleno) | calculado en el modelo |

El mismo +4,3 % se aplica a capacidad, m² y galpones en los 72 escenarios; alimento, agua, aves faenadas/año y pollitos/año no cambian.

**Afirmaciones moderadas:** mortalidad de Entre Ríos (señal de riesgo, no promedio argentino); velocidad de calentamiento ante falla de ventilación (cifras retiradas); distancia de 1.000 m (pendiente de verificación documental, no criterio de diseño); compartimentos (ejemplos de genética, universo a verificar); plazo de expansión del pollito BB (explicado por el ciclo de reproductoras y marcado como estimación).
