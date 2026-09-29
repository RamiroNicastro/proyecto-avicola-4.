# Conclusiones del estudio de producción primaria

**Fecha:** 2026-09-29 · **Versión:** 1 · Base: [`ciclo_productivo.md`](ciclo_productivo.md), [`alimentacion.md`](alimentacion.md), [`galpones.md`](galpones.md), [`bioseguridad.md`](bioseguridad.md), [`transporte_aves.md`](transporte_aves.md), [`modelos_integracion.md`](modelos_integracion.md), [`kpis_productivos.md`](kpis_productivos.md), [`guia_ramiro.md`](guia_ramiro.md), [`escenarios_produccion.csv`](escenarios_produccion.csv), [`modelo_escenarios_produccion.py`](modelo_escenarios_produccion.py)

> **No** se define el tamaño de la empresa, **no** se decide cuántos galpones construir, **no** se asume granja propia ni incubadora propia y **no** se construye el modelo financiero. Las plantas de 2.500–20.000 aves/día son **escenarios hipotéticos**. No se inicia el balance de masa, ni el dimensionamiento del frigorífico, ni la maquinaria.
> **Fuentes:** acceso directo bloqueado (cuarta sesión consecutiva, DPV-009). Toda cifra externa es `[PVDP]`; los parámetros de trabajo son `[ESTIMACIÓN]` o `[SUPUESTO]` (SUP-025 a SUP-034).

---

## 1. Diez hallazgos productivos principales

1. **La cadena física tiene tres "universos" que no deben mezclarse:** pollitos alojados → aves cargadas (−3 a −8 % o más de mortalidad en granja) → aves llegadas a planta (−0,2 a −0,5 % de DOA). Una planta de 10.000 aves/día necesita **~50.000 pollitos BB por semana** (5 días de faena).
2. **El alimento es la variable física dominante y el FCR la gobierna.** Perfil medio: **~4,6–5,4 kg de alimento por ave** faenada. **+0,1 de FCR = +5,9 % de alimento** (+290 t por millón de aves de 2,9 kg; +727 t/año en el escenario medio de 10.000 aves/día).
3. **La mortalidad local podría ser más alta que la supuesta como "media".** El único dato argentino obtenido (Entre Ríos, 62 crianzas) muestra **7,7 % en galpones tecnificados y 9,5 % en convencionales**; el escenario "medio" usa 5 %. Es el parámetro productivo más urgente de validar.
4. **Capacidad de galpón ≠ producción anual y 365/edad ≠ ciclos/año.** Con 47 días de crianza y 15 días entre lotes salen **~5,7 ciclos/año** (rango razonable ~5–7); usar 365/edad sobreestima la capacidad **25–40 %**.
5. **La superficie depende sobre todo de densidad, peso y ciclos**, no de la mortalidad: para la misma planta, las combinaciones de supuestos mueven los m² **hasta ~3,3 veces**. Escenario medio de 10.000 aves/día: **~36.000 m²** (≈ 30 galpones de 1.200 m² o 15 de 2.400 m²).
6. **La tecnología del galpón define la densidad posible y el riesgo de calor.** Galpones tecnificados/túnel permiten ~35–42 kg/m² y mejores indicadores; los abiertos, ~25–33 kg/m². La comparación correcta es costo por kg vivo producido, no CAPEX por m².
7. **La energía es un riesgo de continuidad crítico:** en un galpón cerrado sin ventilación la temperatura puede subir del orden de **1–2 °C por minuto**; hay mortandades registradas en Entre Ríos y Santa Fe por calor y caídas de tensión. Generador automático, alarmas y calidad de red son requisitos, no opciones.
8. **La bioseguridad es condición de acceso a mercados.** Hay normativa específica (Res. SENASA 1699/2019 con **1.000 m** entre granjas, 106/2013 cama, 86/2016 *Salmonella*, 575/2018 bienestar, 484/2017 compartimentos; todas `[PVDP]`). Los compartimentos certificados hoy son de genética, no de engorde.
9. **La distancia granja–planta es una restricción física** (ayuno total ≈ 8–12 h, DOA, merma, bioseguridad, flete de un producto voluminoso): las granjas deben estar en un **radio acotado** de la planta; la planta cerca de granjas y granos, y el producto terminado viaja al mercado.
10. **El modelo de abastecimiento (propio / integrado / compra / mixto) es una decisión de capital, control y riesgo sin ganador todavía.** La integración es el modelo dominante del sector y traslada el CAPEX de galpones al productor, pero exige capital de trabajo (del orden de **1.600–2.100 t de alimento en proceso** en el escenario medio de 10.000 aves/día) y know-how. La compra spot es flexible pero inestable y débil en bioseguridad. El pollito BB es un insumo concentrado y de ajuste lento (~6–7 meses).

---

## 2. Rangos de peso, edad, FCR y mortalidad

| Variable | BAJO | MEDIO | ALTO | Clasificación |
|---|---|---|---|---|
| **Edad de faena** (perfil de mercado) | 35–40 d (38) | 45–50 d (47) | 52–56 d (54) | `[ESTIMACIÓN]` |
| **Peso vivo** (perfil de mercado) | 2,2–2,5 kg (2,4) | 2,7–3,0 kg (2,9) | 3,2–3,6 kg (3,4) | `[ESTIMACIÓN]`; campo AR 46–50 d ~3 kg (FTE-050), ~2,7 kg a ~50 d (FTE-154); Cobb ~2,86 kg a 42 d (FTE-140) `[PVDP]` |
| **FCR de campo** a 2,9 kg (desempeño) | 1,60 (favorable) | 1,70 | 1,85 (desfavorable) | `[ESTIMACIÓN]` SUP-028 |
| FCR a 2,4 kg / 3,4 kg | 1,48–1,73 | 1,58 / 1,82 | 1,72–1,97 | `[ESTIMACIÓN]` |
| **Mortalidad en granja** | 3 % | 5 % | 8 % (local 7,7–9,5 %, FTE-151 `[PVDP]`) | `[SUPUESTO]` SUP-026 |
| Mortalidad en transporte | 0,2 % | 0,3 % | 0,5 % | `[SUPUESTO]` SUP-026 |
| Ganancia diaria (perfil medio) | ~52–55 g/d | ~58–62 g/d | ~64–68 g/d | `[ESTIMACIÓN]` |
| Uniformidad (CV) | > 12 % | 9–11 % | ≤ 8 % | `[ESTIMACIÓN]` |
| Densidad final | 30 kg/m² | 35 kg/m² | 39 kg/m² (42 máx. UE excepcional) | `[SUPUESTO]`; FTE-143, FTE-144 `[PVDP]` |
| Días entre lotes | 20 | 15 | 12 | `[SUPUESTO]` SUP-029 |
| Ciclos/año | ~4,8 (pesado, 20 d entre lotes) | ~5,7 (medio, 15 d) | ~7,1 (liviano, 12 d) | `[ESTIMACIÓN]`; rango razonable ~5–7 |

---

## 3. Escenarios físicos (perfil medio, 5 días de faena/semana)

> **ESCENARIOS, no diseño recomendado.** Formato: favorable / **medio** / desfavorable. Con 6 días/semana, todo +20 %. Rango completo (3 perfiles × 3 desempeños × 5–6 días) en el CSV y en [`ciclo_productivo.md` §6.3](ciclo_productivo.md).

| Planta (aves/día) | Aves a faena/año | Pollitos BB/semana | Pollitos BB/año | Capacidad de alojamiento (plazas) | Inventario promedio de aves vivas |
|---|---|---|---|---|---|
| 2.500 | 625.000 | 12.400 / **12.700** / 13.100 | 0,65 / **0,66** / 0,68 M | 108.000 / **116.000** / 129.000 | ~82.000–84.000 |
| 5.000 | 1.250.000 | 24.800 / **25.400** / 26.300 | 1,29 / **1,32** / 1,37 M | 215.000 / **231.000** / 258.000 | ~164.000–169.000 |
| 10.000 | 2.500.000 | 49.700 / **50.800** / 52.500 | 2,58 / **2,64** / 2,73 M | 430.000 / **462.000** / 517.000 | ~328.000–338.000 |
| 20.000 | 5.000.000 | 99.300 / **101.500** / 105.000 | 5,16 / **5,28** / 5,46 M | 861.000 / **924.000** / 1.034.000 | ~655.000–675.000 |

## 4. Alimento asociado (perfil medio, 5 días/semana)

| Planta (aves/día) | kg/ave faenada | t/semana | t/mes | t/año | de las cuales terminación (~68 %) |
|---|---|---|---|---|---|
| 2.500 | 4,65 / **4,94** / 5,39 | 56 / **59** / 65 | 242 / **258** / 281 | 2.906 / **3.091** / 3.370 | ~2.100 |
| 5.000 | 4,65 / **4,94** / 5,39 | 112 / **119** / 130 | 484 / **515** / 562 | 5.812 / **6.181** / 6.740 | ~4.200 |
| 10.000 | 4,65 / **4,94** / 5,39 | 224 / **238** / 259 | 969 / **1.030** / 1.123 | 11.623 / **12.362** / 13.480 | ~8.400 |
| 20.000 | 4,65 / **4,94** / 5,39 | 447 / **475** / 518 | 1.937 / **2.060** / 2.247 | 23.246 / **24.724** / 26.960 | ~16.900 |

Reparto (perfil medio): inicio ~5 %, crecimiento ~27 %, terminación ~68 %. Maíz ~60 % y harina de soja ~30 % del tonelaje (ilustrativo). Rango completo: **2.200–40.400 t/año** según planta y supuestos. Agua de bebida (medio): **~15 / 30 / 61 / 122 m³/día** promedio, con picos de verano ×2–3 y sin contar el agua de *cooling*.

## 5. Superficie aproximada de galpones (perfil medio, 5 días/semana)

| Planta (aves/día) | m² de galpón | Galpones de 1.200 m² | Galpones de 1.800 m² | Galpones de 2.400 m² | Rango completo de m² |
|---|---|---|---|---|---|
| 2.500 | 7.760 / **9.100** / 11.490 | 6,5 / **7,6** / 9,6 | 4,3 / **5,1** / 6,4 | 3,2 / **3,8** / 4,8 | 5.400–17.900 |
| 5.000 | 15.520 / **18.190** / 22.980 | 12,9 / **15,2** / 19,1 | 8,6 / **10,1** / 12,8 | 6,5 / **7,6** / 9,6 | 10.900–35.700 |
| 10.000 | 31.040 / **36.380** / 45.960 | 25,9 / **30,3** / 38,3 | 17,2 / **20,2** / 25,5 | 12,9 / **15,2** / 19,1 | 21.800–71.400 |
| 20.000 | 62.080 / **72.770** / 91.930 | 51,7 / **60,6** / 76,6 | 34,5 / **40,4** / 51,1 | 25,9 / **30,3** / 38,3 | 43.500–142.800 |

Galpones sin redondear y **sin reserva**: son equivalentes de superficie, **no una recomendación de cuántos construir**. En el caso de integración, esa superficie sería **de terceros**.

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
| **Golpe de calor / corte o caída de tensión** | Alta en verano | Alto: mortandad masiva en horas | Galpones con cooling, generador automático, alarmas, menor densidad estival |
| **Mortalidad y FCR peores que lo supuesto** | Media–alta (dato local 7,7–9,5 %) | Alto: más pollitos y más alimento por kg | Validar con datos de campo (DPV-044); asistencia técnica; pago por desempeño |
| **Falta de pollito BB o calidad irregular** | Media | Alto: sin pollito no hay lote; ajuste lento | Contratos anuales, dos proveedores, especificaciones de calidad |
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
| Mortalidad de campo | Un solo estudio local (año a confirmar) con 7,7–9,5 %, frente a 5 % usado como "medio" | DPV-044 |
| FCR de campo | Sin datos argentinos por zona y tipo de galpón; valores supuestos | DPV-044 |
| Manuales genéticos | Solo un valor de Cobb leído en extracto (~2,86 kg a 42 d); tablas completas no leídas | DPV-045 |
| Normativa SENASA | Resoluciones citadas por extractos; texto completo no leído (densidad, distancias, cama, transporte) | DPV-046, DPV-058 |
| Superficie y capacidad de granjas en ER | ~30.500 aves/granja (2017) vs ~1.400 m²/granja implican ~22 aves/m² (incompatible con 12–14) | DPV-055 |
| Energía | Extracto de potencia por ave inconsistente (descartado); kWh/m²/año de estudio extranjero | DPV-052 |
| Curva de consumo por fase | Orden de magnitud con forma de manual, no tabla verificada | SUP-032, DPV-045 |
| Densidad de carga en transporte y aves por camión | No leídos / supuestos | DPV-054, SUP-033 |
| Agua de *cooling* | No cuantificada | DPV-053 |

---

## 11. Control de calidad

- [x] Dato real (`[PVDP]` con FTE) separado de escenario (`ESCENARIO`, `[ESTIMACIÓN]`, `[SUPUESTO]`).
- [x] Ninguna conversión única: FCR en rango (1,48–1,97) y sensibilidad 1,5–1,9.
- [x] Ningún peso único: perfiles 2,4 / 2,9 / 3,4 kg.
- [x] Ninguna mortalidad única: 3 / 5 / 8 % (+ 12 % en sensibilidad) y tabla de 2–15 %.
- [x] Pollitos alojados, aves cargadas y aves faenadas separados en todas las tablas.
- [x] Capacidad de alojamiento, inventario promedio y producción anual diferenciados.
- [x] Vacío sanitario incluido en los ciclos (10–21 días entre lotes + disponibilidad 0,97).
- [x] Unidades comprobadas (aves, kg vivo, t, m², m³, días); base de FCR declarada (de campo, kg vivo cargado).
- [x] Balances verificados automáticamente en los 72 escenarios (pollitos ≥ cargadas ≥ faenadas; capacidad × ciclos = pollitos; kg/m² final = máximo; alimento = kg × FCR; fases = total).
- [x] Datos débiles señalados (§10).
- [x] No se recomienda cantidad de galpones, tecnología, proveedor, localización ni modelo de abastecimiento.
- [ ] Verificación documental primaria (bloqueada; DPV-009, DPV-045, DPV-046).
- [ ] Datos de campo argentinos (DPV-044, DPV-048).

## 12. Evaluación de calidad

**MEDIA** como marco técnico y modelo físico de escenarios; **BAJA** como evidencia de campo argentina.

- **Fortalezas:** proceso completo descripto; separación explícita perfil de mercado vs desempeño; modelo reproducible con fórmulas, supuestos y verificaciones de balance; sensibilidad por variable; diferenciación capacidad/inventario/producción; normativa relevante identificada; comparación de modelos de abastecimiento sin sesgo; información de campo priorizada.
- **Debilidades:** ninguna fuente leída en su original (todas `[PVDP]`); casi sin datos argentinos de desempeño (un estudio de mortalidad); parámetros de FCR, uniformidad, consumo por fase, energía y transporte son estimaciones; sin costos (por diseño de la fase). Los escenarios sirven para **ordenar decisiones y preguntas**, no para diseñar granjas.
