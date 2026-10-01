# Logística de aves vivas — granja → planta

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de interpretación) · Sesión 12B · Fase 0

> **Alcance:** cuántas aves y toneladas vivas se mueven por día de faena, cuántos viajes, con qué ocupación, a qué distancia, con qué tiempo de ciclo y cuántas granjas abastecen cada escala. Complementa (no repite) la práctica de captura, densidad, bienestar y lavado de [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md).
> **No** se declara radio óptimo ni reglamentario, ni capacidad estándar de camión, ni se elige transportista o flota.
> Cifras: bloques `aves_vivas*` y `granjas` de [`escenarios_logistica.csv`](escenarios_logistica.csv).
> **v1.1:** la ventana prefaena se desagrega por tramos; el tiempo de transporte disponible y su alcance en km son **resultados del escenario**, no límites; el retorno del camión se describe como "sin carga comercial (con jaulas)"; los viajes muestran siempre la capacidad de escenario que los produce.

---

## 1. Base de cálculo

| Parámetro | Valor de referencia | Clasificación |
|---|---|---|
| Aves faenadas/día operativo | 2.500 / 5.000 / 10.000 / 20.000 (escalas **aprobadas** de `23`, leídas por el modelo) | `[SUPUESTO]` SUP-025/052; no es escala elegida |
| Aves cargadas = faenadas / (1 − DOA) | DOA 0,3 % (barrido 0,2–1,63 %) | SUP-026; FTE-156 `[PVDP]` |
| Peso vivo | 2,9 kg **en planta** (ancla del balance, SUP-035/058); el peso en granja se recalcula si se activa la merma de viaje | `[SUPUESTO]` |
| **Aves por camión** | **Capacidad de ESCENARIO**, editable: barrido 4.000 / 5.500 / 7.000 (SUP-033, sin fuente). **Ninguna está validada ni cotizada.** Si no se elige una, el modelo devuelve los viajes como **PENDIENTE** | `[SUPUESTO]` SUP-096; DPV-084 |
| Reducción de carga en verano | 15 % (barrido 10–25 %): 03 indica 1–2 aves menos por cajón | `[SUPUESTO]` SUP-097 |
| Velocidad media cargado | 60 km/h (03: 60–70) | `[ESTIMACIÓN]` sin fuente |
| Tramos de la ventana prefaena y del ciclo | §3 | `[SUPUESTO]` SUP-095, sin fuente (DPV-127) |
| Horas útiles por camión-día | 12 h (no descuenta mantenimiento: DPV-136) | `[SUPUESTO]` SUP-098 |

**Capacidad de escenario ≠ capacidad validada o cotizada.** Las cifras de viajes de este documento indican siempre la capacidad que las produce (columna `capacidad_vehiculo` del CSV, con `tipo_capacidad` = ESCENARIO o PENDIENTE). **No son requerimientos de flota.** Un extracto de foros (FTE-289 `[PVDP · débil]`) indica 8–12 pollos por jaula según peso; no permite derivar aves por camión.

## 2. Aves, toneladas y viajes por escala (radio 100 km, factor de ruta 1,3)

| Escala | Aves cargadas/día | t vivas/día | Aves/h de línea (8 h netas) | Viajes/día con **4.000 · 5.500 · 7.000 aves/camión (escenario)** | Ídem en verano (−15 %) | Ocupación con 5.500 (normal · verano) | Intervalo entre camiones para alimentar la línea (5.500) |
|---|---|---|---|---|---|---|---|
| 2.500 | 2.508 | 7,3 | 312 | 1 · 1 · 1 | 1 · 1 · 1 | **46 % · 54 %** | 17,6 h |
| 5.000 | 5.015 | 14,5 | 625 | 2 · 1 · 1 | 2 · 2 · 1 | 91 % · 54 % | 8,8 h |
| 10.000 | 10.030 | 29,1 | 1.250 | 3 · 2 · 2 | 3 · 3 · 2 | 91 % · 72 % | 4,4 h |
| 20.000 | 20.060 | 58,2 | 2.500 | 6 · 4 · 3 | 6 · 5 · 4 | 91 % · 86 % | 2,2 h |
| Sin capacidad elegida | = | = | = | **PENDIENTE** | PENDIENTE | PENDIENTE | PENDIENTE |

Viajes = **techo** de aves cargadas / capacidad efectiva (test L06); ocupación ≤ 100 % (L08). Reproduce las t vivas y los camiones fraccionarios de `23 §12` sin diferencias (L14).

**Lecturas (del escenario):**
1. Con un camión de 5.500 aves, a 2.500 aves/día el viaje sale al 46 % de su capacidad de escenario: o el vehículo es más chico, o se acepta la baja ocupación (cargar dos días de faena en un viaje no es compatible con la secuencia prefaena modelada).
2. Con 5.500 aves por camión, la reducción de verano agrega un viaje en 5.000, 10.000 y 20.000 aves/día.
3. A 20.000 aves/día llega un camión cada ~2 h durante la faena: la coordinación captura–recepción es una operación en sí misma.

## 3. Ventana prefaena ≠ tiempo de viaje

La ventana prefaena es el tiempo **total** entre el retiro del alimento y la faena; el transporte es **solo una parte**:

```
retiro de alimento → captura y carga → espera en granja → TRANSPORTE → espera en planta → descarga/colgado → faena
|<--------------------------------- ventana prefaena de ESCENARIO (10 h) --------------------------------->|
```

| Tramo | Variable del modelo | Valor de escenario | Fuente |
|---|---|---|---|
| Retiro de alimento → inicio de captura | `t_retiro_alimento` | 3,0 h (barrido 2–4) | `[SUPUESTO]` sin fuente |
| Captura y carga | `t_captura_carga` | 1,5 h (1,0–2,5) | `[SUPUESTO]` sin fuente |
| Espera en granja tras cargar | `t_espera_granja` | 0 h (0–1) | `[SUPUESTO]` |
| **Transporte** | `t_transporte` (medio y máximo según el radio) | resultado | distancia / 60 km/h |
| Espera en planta | `t_espera_planta` | 0,75 h (0,5–2,0) | `[SUPUESTO]` sin fuente |
| Descarga / colgado | `t_descarga` | 0,25 h (0,25–0,5) | `[SUPUESTO]` sin fuente |
| **Total prefaena** | `t_total_prefaena` | suma de los anteriores | — |
| Ventana configurada | `ventana_prefaena_escenario` | **10 h** | **Parámetro de escenario** dentro del rango 8–12 h citado como práctica (FTE-156 `[PVDP]`). **No es un máximo normativo**: no se encontró fuente primaria que lo establezca |

**Tiempo de transporte disponible bajo la parametrización actual del escenario** = ventana − (retiro + captura/carga + esperas + descarga) = 10 − 5,5 = **4,5 h**. No es un límite sanitario general.

**Alcance resultante del escenario** = 4,5 h × 60 km/h = **≈ 270 km por ruta (≈ 208 km de radio geográfico con factor 1,3)**. Combina tiempo disponible y velocidad **supuestos**: **no es un radio máximo reglamentario ni óptimo**. El modelo genera `alerta_prefaena_excede_ventana` cuando la suma de tramos supera la ventana configurada; si no se configura ventana, el tiempo disponible queda PENDIENTE.

### 3.1 Sensibilidad del tiempo disponible y del alcance (un parámetro por vez)

| Parámetro variado | Valores | Transporte disponible (h) | Alcance por ruta (km) | Alcance geográfico (km) |
|---|---|---|---|---|
| Ventana configurada | 8 · 10 · 12 h | 2,5 · 4,5 · 6,5 | 150 · 270 · 390 | 115 · 208 · 300 |
| Retiro de alimento | 2 · 3 · 4 h | 5,5 · 4,5 · 3,5 | 330 · 270 · 210 | 254 · 208 · 162 |
| Captura y carga | 1,0 · 1,5 · 2,5 h | 5,0 · 4,5 · 3,5 | 300 · 270 · 210 | 231 · 208 · 162 |
| Espera en granja | 0 · 0,5 · 1,0 h | 4,5 · 4,0 · 3,5 | 270 · 240 · 210 | 208 · 185 · 162 |
| Espera en planta | 0,5 · 0,75 · 2,0 h | 4,75 · 4,5 · 3,25 | 285 · 270 · 195 | 219 · 208 · 150 |

Cualquier hora ganada en captura, espera o recepción **amplía el tiempo de transporte disponible** (test L22). Por eso el alcance no es una propiedad del territorio sino de **cómo se organiza la operación**.

## 4. Distancia geográfica vs distancia por ruta

| Concepto | Definición | Valor en el modelo |
|---|---|---|
| **Radio** (geográfico) | Distancia en línea recta de la granja más lejana a la planta | Barrido 25 / 50 / 100 / 150 / 200 / 300 km (**sensibilidad**, SUP-091) |
| Distancia geográfica **media** | Con granjas repartidas uniformemente en un círculo, la media es 2/3 del radio (SUP-093) | 2/3 × R |
| **Factor de ruta** | km por ruta / km en línea recta | 1,2 / 1,3 / 1,4 (base 1,3). Estudios internacionales: ~1,2–1,42 (FTE-286 `[PVDP]`); **sin medición argentina** (DPV-116) |
| Distancia **por ruta** | Geográfica × factor de ruta (≥ geográfica; test L18) | — |

## 5. Escenarios de radio (10.000 aves/día, factor 1,3; camión de escenario de 5.500 aves)

| Radio (km) | Dist. ruta media · máx. | Transporte medio · máx. (h) | Total prefaena máx. (h) | Alerta vs ventana de 10 h | Ciclo del camión (h) | km/día | km/ave | Flota mínima · utilización (día de faena) | Ave·h en tránsito/día |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 22 · 32 | 0,4 · 0,5 | 6,0 | — | 4,0 | 87 | 0,009 | 1 · 66 % | 3.622 |
| 50 | 43 · 65 | 0,7 · 1,1 | 6,6 | — | 4,7 | 173 | 0,017 | 2 · 39 % | 7.244 |
| 100 | 87 · 130 | 1,4 · 2,2 | 7,7 | — | 6,1 | 347 | 0,035 | 2 · 51 % | 14.488 |
| 150 | 130 · 195 | 2,2 · 3,2 | 8,8 | — | 7,6 | 520 | 0,052 | 2 · 63 % | 21.732 |
| 200 | 173 · 260 | 2,9 · 4,3 | 9,8 | — (al límite) | 9,0 | 693 | 0,069 | 2 · 75 % | 28.976 |
| 300 | 260 · 390 | 4,3 · 6,5 | 12,0 | **Alerta** | 11,9 | 1.040 | 0,104 | 2 · 99 % | 43.464 |

La alerta indica que, **con esta parametrización**, las granjas del borde de un radio de 300 km exceden la ventana configurada; con otra organización de captura y recepción (§3.1) el resultado cambia.

### 5.1 Cómo afecta el radio a cada dimensión (sin declarar un óptimo)

| Dimensión | Efecto de un radio mayor | Cuantificable hoy | Qué falta |
|---|---|---|---|
| **Tiempo** | +1 h de viaje por cada ~60 km de ruta | Sí (velocidad supuesta) | Velocidades reales por camino (DPV-116) |
| **Bienestar** | Más ave·horas en tránsito (×12 de 25 a 300 km); exposición a calor | Ave·h (exposición, no daño) | Relación con lesiones y DOA en Argentina |
| **Mortalidad (DOA)** | Puede aumentar con tiempo y calor, pero **no hay función validada DOA–distancia** | **No**: barrido independiente (§6) | DPV-054 |
| **Bioseguridad** | Rutas más largas cruzan más zonas; más dispersión reduce el impacto de un brote en un sitio | No | Mapa de granjas y rutas (12A) |
| **Costo** | km/día ×12 entre 25 y 300 km; camión-horas ×3 | Drivers físicos sí; costo **no** | Tarifas (DPV-054) |
| **Utilización de camiones** | Ciclos más largos llenan más la jornada (39 % → 99 %) pero bajan los ciclos posibles por camión (3 → 1) | Sí | Horas útiles reales, mantenimiento |
| **Coordinación de faena** | Con ciclos de 9–12 h cada camión hace un viaje por jornada | Sí (intervalo vs ciclo) | Capacidad del galpón de espera (12C) |

## 6. Sensibilidad a la mortalidad en transporte (DOA)

10.000 aves faenadas/día, camión de escenario de 5.500 aves:

| DOA | Aves cargadas/día | Aves DOA/día | Aves DOA/año (250 d) | kg DOA/día | Viajes/día (5.500) |
|---|---|---|---|---|---|
| 0,2 % | 10.020 | 20 | 5.010 | 58 | 2 |
| 0,3 % (base) | 10.030 | 30 | 7.523 | 87 | 2 |
| 0,5 % | 10.050 | 50 | 12.563 | 146 | 2 |
| 1,0 % | 10.101 | 101 | 25.253 | 293 | 2 |
| 1,63 % (adverso, FTE-156) | 10.166 | 166 | 41.425 | 481 | 2 |

El DOA casi no cambia los viajes (a 20.000 aves/día con 4.000 aves/camión, los equivalentes van de 5,01 a 5,08: siguen siendo 6), pero sí las **aves pagadas y no faenadas**, el **bienestar auditable** y un flujo de material de destino restringido.

## 7. Merma de peso en el viaje (sensibilidad)

Con 0,2–0,5 % del peso por hora de transporte, espera en planta y descarga (`[ESTIMACIÓN]` de 03; base = 0, SUP-058), las aves faenadas no cambian pero el peso cargado sube:

| Tasa · radio | 50 km | 150 km | 300 km |
|---|---|---|---|
| 0,2 %/h | 0,34 % · 100 kg/día | 0,63 % · 185 kg/día | 1,07 % · 313 kg/día |
| 0,5 %/h | 0,86 % · 252 kg/día | 1,58 % · 467 kg/día | 2,67 % · 795 kg/día |

(10.000 aves/día). Conservación: kg cargados = faenables + DOA + merma (L01). Quién paga la merma es una cláusula del contrato de integración ([`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md)).

## 8. Tiempo de ciclo y utilización de camiones

**Tiempo de ciclo = ida + captura/carga + espera en granja + espera en planta + descarga + regreso + lavado/desinfección** (variables `t_ida_h`, `t_captura_carga_h`, `t_espera_granja_h`, `t_espera_planta_h`, `t_descarga_h`, `t_regreso_h`, `t_lavado_h`; test L24). La utilización **sale del ciclo**:

```
camión-horas/día   = viajes × ciclo
flota mínima       = max(techo(camión-horas / horas útiles), camiones necesarios para alimentar la línea en continuo)
utilización diaria = camión-horas / (flota × horas útiles)
utilización semanal= camión-horas × días de faena / (flota × horas útiles × 7)
ciclos posibles por camión y jornada = piso(horas útiles / ciclo)
```

Camión de escenario de 5.500 aves, 12 h útiles, 5 días de faena:

| Escala · radio | Viajes/día | Ciclo (h) | Ciclos posibles por camión | Flota mínima | Utilización diaria · semanal |
|---|---|---|---|---|---|
| 2.500 · 25 / 100 / 300 km | 1 | 4,0 / 6,1 / 11,9 | 3 / 1 / 1 | 1 | 33 · 24 % / 51 · 37 % / 99 · 71 % |
| 10.000 · 25 / 100 / 300 km | 2 | 4,0 / 6,1 / 11,9 | 3 / 1 / 1 | 1 / 2 / 2 | 66 · 47 % / 51 · 37 % / 99 · 71 % |
| 20.000 · 25 / 100 / 300 km | 4 | 4,0 / 6,1 / 11,9 | 3 / 1 / 1 | 2 / 3 / 4 | 66 · 47 % / 68 · 49 % / 99 · 71 % |

La utilización semanal de **37–49 % (radio 100 km)** es un **resultado del escenario**: depende de los días de faena (5 de 7), la cantidad de viajes, la distancia, los tiempos de carga, descarga, espera y lavado, la posibilidad de hacer varios ciclos por día y el mantenimiento (no descontado). No se deriva de una prohibición de otros usos.

## 9. Retorno del camión de aves

| Tipo de retorno | Definición | Aves vivas en el modelo |
|---|---|---|
| **Sin carga comercial** | No transporta mercadería que genere ingreso o reemplace otro flete | **Sí** (base) |
| **Con envases / jaulas** | Lleva jaulas, cajones o módulos vacíos: **no está físicamente vacío** aunque no lleve carga comercial | **Sí**: vuelve con sus jaulas/cajones |
| **Backhaul comercial** | Transporta otra carga con valor | **No** en el modelo base |

`BACKHAUL_AVES = false` es un **supuesto conservador**: el modelo considera el retorno sin carga comercial para no asumir compatibilidades sanitarias o logísticas no verificadas. La posibilidad de otra utilización requiere validar habilitación del vehículo, lavado/desinfección, tiempos de ciclo, tipo de vehículo y compatibilidad sanitaria. **No se afirma que esté jurídicamente prohibido en todos los casos.** La Res. SENASA 723/2025 (FTE-234, confirmada en revisión externa) exige, entre otros puntos, lavado y desinfección de superficies externas e internas a cada viaje; eso condiciona el ciclo, pero **no se usa** como respaldo de una obligación general de retorno vacío. El KPI asociado se llama **% de km sin carga comercial** (50 % en el modelo base).

## 10. Granjas abastecedoras y frecuencia

| Escala | Granjas equivalentes con 15.000 · 30.000 · 60.000 plazas | Cosechas/semana | Días de faena para retirar un lote completo con la cadencia modelada | Viajes por cosecha (5.500 aves/camión, escenario) |
|---|---|---|---|---|
| 2.500 | 8,0 · 4,0 · 2,0 | 0,9 · 0,4 · 0,2 | 5,7 · 11,4 · 22,7 | 3 · 6 · 11 |
| 5.000 | 16,1 · 8,0 · 4,0 | 1,8 · 0,9 · 0,4 | 2,8 · 5,7 · 11,4 | 3 · 6 · 11 |
| 10.000 | 32,1 · 16,1 · 8,0 | 3,5 · 1,8 · 0,9 | 1,4 · 2,8 · 5,7 | 3 · 6 · 11 |
| 20.000 | 64,3 · 32,1 · 16,1 | 7,0 · 3,5 · 1,8 | 0,7 · 1,4 · 2,8 | 3 · 6 · 11 |

Granjas equivalentes = plazas de alojamiento de 03 v1.1 ÷ plazas por granja (dato real DPV-048). Cada granja entrega ~5,7 veces por año.

**Incompatibilidad operativa POTENCIAL bajo el supuesto de que el lote se retire con la cadencia modelada:** si toda una granja de 30.000 aves se retirara a ritmo de 2.500 aves/día, tardaría ~11 días de faena, frente a la referencia de "1–2 noches" de 03 (`[ESTIMACIÓN]`). El modelo marca `alerta_cosecha_prolongada_potencial` cuando se supera esa referencia. **No se concluye que ambas escalas sean incompatibles**: hay que validar retiros parciales (raleo), el esquema all-in/all-out, el tamaño real de los lotes por galpón, la programación entre varias granjas y las restricciones sanitarias y productivas (DPV-133, DEC-060).

## 11. Bioseguridad y bienestar en la operación

- Camiones y cajones circulan entre granjas: lavado y desinfección después de cada descarga (03 §7; Res. SENASA 723/2025, FTE-234).
- Orden de captura "limpia → sucia"; cuadrillas sin visitar dos granjas el mismo día salvo protocolo (03).
- Verano: viaje nocturno, menos aves por cajón (+1 viaje con 5.500 aves por camión), espera ventilada. Contingencias en [`conclusiones_logistica.md` §5](conclusiones_logistica.md).

## 12. Qué debe validarse en campo

DPV-054 (contratistas, aves/camión, radio real, DOA, lavado), DPV-058 (normativa de transporte), DPV-048 (productores), DPV-127 (tiempos de cada tramo), DPV-054 (DOA vs distancia y estación), DPV-116 (velocidades y factor de ruta), DPV-133 (lotes y cadencia de retiro), DPV-136 (disponibilidad de flota y mantenimiento).
