# Escenarios y trade-offs de localización

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría metodológica) · **Sesión:** 12A · Método en [`metodologia_localizacion.md`](metodologia_localizacion.md)

> Escenarios para **pensar** la localización, no para elegirla. Las cifras son aritmética sobre escenarios ya existentes del proyecto (demanda de prueba de `02`, flujos de `23`) y distancias de orden de magnitud no medidas (SUP-12A-02). **No son costos** (sin CAPEX ni OPEX en esta fase) **ni pronósticos**.

---

## 1. Distancia no es costo

Una zona más lejos del mercado puede ser más barata de operar, y una zona cercana puede ser más cara. El costo que importa es el **costo total puesto en el cliente** (producción primaria + alimento + faena + servicios + transporte de cada flujo + riesgo), no los kilómetros a CABA.

| Una zona **lejos** del mercado puede… | Una zona **cerca** del mercado puede… |
|---|---|
| estar más cerca de las granjas (viajes cortos de aves vivas: menos DOA, merma y estrés) | reducir el costo y el tiempo de distribución diaria del fresco |
| estar más cerca del maíz y la soja (el alimento es el mayor flujo físico del sistema) | facilitar el contacto comercial, la reposición y las devoluciones |
| tener tierra más barata y espacio para tratamiento de efluentes y expansión | complicar la bioseguridad (granjas dispersas, tránsito de aves vivas por zonas pobladas) |
| tener servicios (agua, potencia, vuelco) menos disputados por otros usuarios | encarecer el suelo y restringir la expansión |
| tener menor presión urbana (olores, tránsito, vecinos) | tener más conflicto vecinal y restricciones de horario y tránsito |
| tener mano de obra con experiencia avícola (si es zona de cluster) | tener más competencia por mano de obra con otros sectores |

**Los flujos no pesan igual.** A 10.000 aves faenadas/día (escenario medio de [`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §12): entran ~29 t/día de aves vivas, salen ~24 t/día de producto comestible y ~6 t/día de subproductos sólidos, y a las granjas llegan ~35 t/día de alimento. El argumento principal para acercar la planta a las granjas **no** es la masa (29 t entran contra 24 t que salen), sino que el ave viva es un **animal** sensible al tiempo, al calor y a la bioseguridad, mientras que el producto refrigerado o congelado viaja con riesgos más controlables ([`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §8).

## 2. Arquetipos de localización de **una** planta (sin ganador) y arquitecturas de red

### 2.1 Arquetipos de localización (para una planta)

| Arquetipo | Descripción | Gana | Pierde | Regiones donde podría darse (hipótesis) |
|---|---|---|---|---|
| **L1 — Planta cerca del mercado** | Faena y procesamiento en el periurbano del AMBA; aves vivas traídas de granjas lejanas | Distribución, frescura, control comercial | Exposición sanitaria, viajes largos de aves vivas, suelo, vecinos, expansión | BA-AMBA |
| **L2 — Planta en el cluster avícola** | Planta dentro de una zona con muchas granjas, incubadoras y fábricas de alimento | Ecosistema avícola inmediato, servicios, mano de obra con experiencia | Exposición sanitaria, competencia por productores y personal, distribución larga | ER-URUGUAY, ER-CENTRO, ER-SUR |
| **L3 — Planta en zona de granos y baja densidad** | Planta y granjas nuevas en una zona agrícola con poca avicultura | Exposición sanitaria inicial baja, tierra, alimento cerca, espacio para crecer | Construir el ecosistema desde cero; pollito, servicios y técnicos lejos; distribución larga | BA-OESTE, BA-INTERIOR, CBA-SUR, CBA-ESTE, SF-CENTRO, CH-ESTE, CH-CENTRO |
| **L4 — Corredor intermedio** | Planta entre el cluster y el mercado, sobre rutas troncales | Compromiso entre abastecimiento y mercado; acceso a nodos portuarios | No es óptima en nada; depende de que haya productores en radio | BA-NORTE, ER-SUR, SF-SUR |

### 2.2 Arquitecturas de red (decisión abierta, DEC-12A-04)

"Una planta" y "faena productiva + CD en el AMBA" **no son dos localizaciones comparables en la matriz**: son **dos arquitecturas de red diferentes**.

| Arquitectura | Descripción | Cómo se localiza |
|---|---|---|
| **R1 — Planta única** | Faena, procesamiento, frío y despacho en un solo sitio | Con la matriz de corredores (arquetipos L1–L4) |
| **R2 — Planta + CD (o cross-dock / trozado) en el AMBA** | Faena en zona productiva; un segundo nodo en el AMBA recibe producto (no aves vivas) y distribuye | La planta, con la matriz de corredores; el segundo nodo, con su propia lógica (mercado, accesos, frío, habilitación), fuera de esta matriz |

La comparación posterior R1 vs R2 deberá considerar, **sin calcular costos todavía**: inversión (dos instalaciones, doble habilitación), inventario (stock en planta y en el CD), frío (cámaras en ambos nodos), doble manipulación, transporte primario (planta → CD, troncal), distribución secundaria (CD → clientes) y nivel de servicio (frecuencia, vida útil remanente, tiempos de respuesta). Una etapa inicial sin planta propia (compraventa o faena a façon, DEC-004, DEC-018) puede usar el AMBA solo como nodo comercial y postergar la decisión de localización industrial.

## 3. Red de ~90 supermercados: sensibilidad logística futura

**Demanda NO validada** (SUP-004; demanda documentada ≈ 0). Los escenarios siguientes **no dimensionan** la planta ni su ubicación; solo muestran cuánto cambia el peso de la distancia al AMBA según el rol que pudiera tener la red. Volúmenes tomados de [`../02_clientes_demanda/escenarios_demanda.csv`](../02_clientes_demanda/escenarios_demanda.csv) (SUP-021, valores de prueba).

| Escenario | Volumen de la red (t/día calendario) | Origen del valor | Lectura para la localización |
|---|---|---|---|
| **S0 — Sin cliente ancla** | 0 | La red no compra o no se valida | La localización se define por producción, costos y **otros canales** (mayoristas, gastronomía, industria, regionales); la cercanía al AMBA pierde peso relativo, aunque el AMBA siga siendo el mayor mercado del país |
| **S1 — Ancla parcial** | 1,0 – 4,5 | ESC-CON (20 locales × 50 kg) a ESC-BAS (45 locales × 100 kg) | La red justifica una **logística propia o tercerizada al AMBA**, pero no define sola la planta; las partes que la red no compra deben venderse en otros canales (SUP-013) |
| **S2 — Ancla fuerte** | 13,5 – 27 | ESC-EXP (90 × 150 kg) a RED-300 (90 × 300 kg, todos los locales compran todo su pollo) | La distancia planta–AMBA pesa más; aparece la pregunta de **CD de la red vs entrega a 90 locales** (DPV-036) y el riesgo de concentración (DEC-017) |

### 3.1 Aritmética de traslado troncal planta → AMBA

**Parámetros de la tabla (todos explícitos):**

| Parámetro | Valor usado |
|---|---|
| Origen | Centro de referencia de cada corredor (SUP-12A-01): Pilar, Gualeguaychú, Concepción del Uruguay, Río Cuarto, Resistencia |
| Distancia por ruta | Orden de magnitud **no medido** (SUP-12A-02): ~55 / 230 / 320 / 600 / 1.020 km (medición pendiente, DPV-12A-01, con 12B) |
| Toneladas | Volumen de la red en cada escenario: 1,0 / 4,5 / 13,5 / 27 t/día calendario (valores de prueba) |
| Porcentaje dirigido al AMBA | **100 %** del volumen de la red (la tabla 3.2 lo varía) |
| Existencia de CD | Se supone una **entrega troncal a un único punto** del AMBA (CD de la red o cross-dock propio). **No está confirmado** que la red tenga CD (DPV-036) |
| Qué se mide | t·km por día calendario = t/día × km; solo ida cargada; **no** es costo ni incluye la distribución dentro del AMBA |

| km a CABA (orden, SUP-12A-02) | S1 bajo (1,0 t/día) | S1 alto (4,5 t/día) | S2 bajo (13,5 t/día) | S2 alto (27 t/día) |
|---|---|---|---|---|
| ~55 (BA-AMBA, Pilar) | 55 | 248 | 743 | 1.485 |
| ~230 (ER-SUR, Gualeguaychú) | 230 | 1.035 | 3.105 | 6.210 |
| ~320 (ER-URUGUAY, C. del Uruguay) | 320 | 1.440 | 4.320 | 8.640 |
| ~600 (CBA-SUR, Río Cuarto) | 600 | 2.700 | 8.100 | 16.200 |
| ~1.020 (CH-ESTE, Resistencia) | 1.020 | 4.590 | 13.770 | 27.540 |

### 3.2 Sensibilidad al porcentaje dirigido al AMBA (S2 bajo, 13,5 t/día; mismos supuestos)

| Origen | 100 % al AMBA | 60 % al AMBA | 30 % al AMBA |
|---|---|---|---|
| ~55 km (Pilar) | 743 | 446 | 223 |
| ~1.020 km (Resistencia) | 13.770 | 8.262 | 4.131 |

`[ESTIMACIÓN]`. Lecturas:

1. **El múltiplo no es una característica de una provincia.** Con los parámetros de la tabla (Resistencia ~1.020 km vs Pilar ~55 km por ruta, distancias no medidas; mismo volumen; mismo porcentaje al AMBA; entrega troncal a un único punto) el traslado troncal es **≈ 18,5 veces** mayor: ese número es solo el cociente de las dos distancias supuestas (1.020 ÷ 55). Cambia si cambian el origen, la distancia medida o el destino; las toneladas y el porcentaje al AMBA cambian los t·km absolutos pero no el cociente, y la parte del volumen que se vende en el mercado regional del corredor no viaja al AMBA.
2. **La forma de distribución puede cambiar sustancialmente el resultado.** Con un CD o cross-dock en el AMBA, la distribución urbana (paradas, ventanas horarias, 90 locales) **no depende** de dónde esté la planta. **Sin** CD, cada ruta de reparto empezaría en la planta: para una planta lejana eso es prácticamente inviable y obliga a la arquitectura R2 (§2.2), con sus propios costos. En [`../02_clientes_demanda/supermercados.md`](../02_clientes_demanda/supermercados.md) §3.1 el costo por kg de la entrega directa varía ~12 veces según los kg por parada: **la arquitectura de distribución puede pesar más que la ubicación de la planta**.
3. Con S0 o S1 bajo, la diferencia de t·km entre corredores es pequeña en términos absolutos.
4. El tiempo también cuenta: a 60–70 km/h medios (mismo orden que [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §4), ~1.000 km son ~14–17 h de viaje `[ESTIMACIÓN]`: un día menos de vida útil comercial del fresco (DPV-078).
5. Costos por t·km, capacidad útil del camión refrigerado (variable sin valor, SUP-057, DPV-084) y fee de CD (DPV-039) son de **12B** y de OPEX; aquí no se calculan.

## 4. Exportación y localización

Exportar depende primero de habilitación, listado, producto autorizado y comprador ([`criterios_localizacion.md`](criterios_localizacion.md) §8). La exportación vale **0** en los escenarios de demanda (SUP-022).

**Cercanía a puerto ≠ disponibilidad reefer ≠ servicio marítimo adecuado ≠ exportación habilitada.** Buenos Aires / Dock Sud son **nodos logísticos de referencia** para contenedores (FTE-134 `[PVDP]`) y deben compararse con otras alternativas portuarias; no se afirma que sean los únicos nodos con servicio reefer, porque no existe un inventario nacional de terminales reefer verificado. Cada nodo se releva con los mismos datos (DPV-12A-10): terminal de contenedores, enchufes y capacidad reefer, frecuencia de servicios, destinos, cut-off, costos y disponibilidad real.

| Escenario | Cómo se exporta | Qué importa de la localización | Qué **no** resuelve la localización |
|---|---|---|---|
| **X0 — Sin exportación** (caso base) | — | Nada específico | — |
| **X1 — Venta a traders o exportadores que consolidan** | La planta vende partes (garras, menudencias, cortes) a quien exporta (DPV-081) | Cercanía a esos compradores y a cámaras de congelado | Habilitación compatible con el destino del comprador; especificación |
| **X2 — Por Buenos Aires / Dock Sud** | Reefer desde nodos de referencia para contenedores (FTE-134 `[PVDP]`) | Distancia y tiempo planta–nodo; disponibilidad de contenedores vacíos | Listado de la planta, acceso sanitario del país (regla 17), lote mínimo y congelado (escala) |
| **X3 — Rosario y corredor del Paraná** | Nodos de la zona núcleo | Cercanía a granos (molienda de soja, maíz); la salida en contenedor reefer **debe verificarse por nodo** (un análisis preliminar del proyecto la registra como escasa, [`../17_exportacion/logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md) §3) | Servicio marítimo reefer por destino |
| **X4 — Zárate y puertos entrerrianos (Concepción del Uruguay, otros)** | Nodos más cercanos al cluster entrerriano | Menor congestión que CABA (Zárate); cercanía al cluster | Volumen, frecuencia y servicio reefer a verificar por nodo |
| **X5 — Chile y países limítrofes por camión** | Logística terrestre (pasos cordilleranos) | Distancia al paso fronterizo (las regiones del centro del país quedan geográficamente más cerca de Cuyo; a medir) | Cierres de paso por nieve; costo por t; acceso sanitario vigente |

**Conclusión del escenario:** la distancia al puerto **reduce un costo**, no abre un mercado. Estar cerca de Rosario no vuelve exportadora a una planta; estar en Chaco no la inhabilita. En el modelo, los km al nodo (EXP-01) **solo puntúan si ese nodo tiene servicio reefer verificado** (EXP-04 ≥ 3); sin eso no hay puntaje exportador por cercanía (test T27).

## 5. Escala y localización

La escala cambia qué criterio domina (escalas de prueba 2.500–20.000 aves/día, sin escala elegida):

| Si la escala futura fuera… | Lo que más pesaría en la localización (hipótesis) |
|---|---|
| Pequeña (orden 2.500 aves/día) | Comprar pollo vivo o integrar pocos productores existentes; cercanía al mercado; terreno pequeño con servicios; quizás una etapa a façon sin planta |
| Media (orden 5.000–10.000) | Productores integrables en radio; vuelco y agua del sitio; potencia; reserva de expansión |
| Grande (orden 20.000 y más) | Abastecimiento de pollito y alimento (incubadora y fábrica propias o contratos firmes); tratamiento de efluentes de gran superficie; mano de obra; expansión; exportación |

Por eso el orden lógico es: **demanda y abastecimiento (hitos H-A y H-B del plan de campo) → rango de escala → lista corta de corredores → municipios → terrenos**.

## 6. Resumen de trade-offs principales

| Trade-off | Lado A | Lado B | Decisión a la que alimenta |
|---|---|---|---|
| Mercado vs granjas | Cerca del AMBA | Cerca de las granjas | DEC-003, DEC-12A-04 |
| Ecosistema avícola vs exposición sanitaria | Cluster avícola (más ecosistema, más exposición) | Baja densidad (menos exposición, ecosistema a construir) | DEC-025, DEC-020, DEC-12A-02 |
| Tierra barata vs servicios | Zona remota | Parque industrial con servicios | DEC-035, DEC-043 |
| Puerto vs granos | Cerca de nodos portuarios de referencia para contenedores (hoy, Buenos Aires / Dock Sud) | Cerca de maíz y soja (centro) | DEC-011, DEC-024 |
| Arquitectura de red (no criterio de localización) | R1 planta única | R2 planta + CD/cross-dock en el AMBA | DEC-12A-04 |
| Decidir ahora vs postergar | Comprometer ubicación temprano | Etapa sin planta propia (compraventa o façon) | DEC-004, DEC-018 |
