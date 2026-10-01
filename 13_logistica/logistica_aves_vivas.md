# Logística de aves vivas — granja → planta

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 12B · Fase 0

> **Alcance:** cuántas aves y toneladas vivas se mueven por día de faena, cuántos viajes, con qué ocupación, a qué distancia, con qué tiempo de ciclo y cuántas granjas abastecen cada escala. Complementa (no repite) la práctica de captura, densidad, bienestar y lavado de [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md).
> **No** se declara radio óptimo, ni capacidad estándar de camión, ni se elige transportista o flota.
> Cifras: bloques `aves_vivas*` y `granjas` de [`escenarios_logistica.csv`](escenarios_logistica.csv).

---

## 1. Base de cálculo

| Parámetro | Valor de referencia | Clasificación |
|---|---|---|
| Aves faenadas/día operativo | 2.500 / 5.000 / 10.000 / 20.000 (escalas **aprobadas** de `23`, leídas por el modelo) | `[SUPUESTO]` SUP-025/052; no es escala elegida |
| Aves cargadas = faenadas / (1 − DOA) | DOA 0,3 % (barrido 0,2–1,63 %) | SUP-026; FTE-156 `[PVDP]` |
| Peso vivo | 2,9 kg **en planta** (ancla del balance, SUP-035/058); el peso en granja se recalcula si se activa la merma de viaje | `[SUPUESTO]` |
| **Aves por camión** | **Variable editable**: barrido 4.000 / 5.500 / 7.000 (SUP-033, sin fuente). 5.500 es el punto medio del barrido, **no** una capacidad estándar | `[SUPUESTO]` SUP-12B-06; DPV-084 |
| Reducción de carga en verano | 15 % (barrido 10–25 %): 03 indica 1–2 aves menos por cajón | `[SUPUESTO]` SUP-12B-07 |
| Velocidad media cargado | 60 km/h (03: 60–70) | `[ESTIMACIÓN]` sin fuente |
| Carga en granja / espera y descarga / lavado | 1,5 h / 1,0 h / 0,75 h | `[SUPUESTO]` SUP-12B-05, sin fuente (DPV-12B-01) |
| Ayuno total máximo / ayuno previo en granja | 10 h (rango 8–12) / 3 h | FTE-156 `[PVDP]` / SUP-12B-05 |
| Horas útiles por camión-día | 12 h | `[SUPUESTO]` SUP-12B-08 |

Un dato de foros técnicos indica **8–12 pollos por jaula según peso** (≤ 8 con más de 2,2 kg) y camiones de "4 filas × 8 jaulas de alto" (FTE-12B-004, fuente comercial/foro no argentina `[PVDP · débil]`). **No** permite derivar aves por camión (falta el número de columnas y el tipo de jaula): queda como orientación para la entrevista a contratistas.

## 2. Aves, toneladas y viajes por escala (radio 100 km, factor de ruta 1,3)

| Escala | Aves cargadas/día | t vivas/día | Aves/h de línea (8 h netas) | Viajes/día con 4.000 · 5.500 · 7.000 aves/camión | Ídem en verano (−15 %) | Ocupación con 5.500 (normal · verano) | Intervalo entre camiones para alimentar la línea |
|---|---|---|---|---|---|---|---|
| 2.500 | 2.508 | 7,3 | 312 | 1 · 1 · 1 | 1 · 1 · 1 | **46 % · 54 %** | 17,6 h (un camión cubre más que la jornada) |
| 5.000 | 5.015 | 14,5 | 625 | 2 · 1 · 1 | 2 · 2 · 1 | 91 % · 54 % | 8,8 h |
| 10.000 | 10.030 | 29,1 | 1.250 | 3 · 2 · 2 | 3 · 3 · 2 | 91 % · 72 % | 4,4 h |
| 20.000 | 20.060 | 58,2 | 2.500 | 6 · 4 · 3 | 6 · 5 · 4 | 91 % · 86 % | 2,2 h |

Viajes = **techo** de aves cargadas / capacidad efectiva (test L06); ocupación ≤ 100 % (L08). Reproduce las t vivas y los camiones fraccionarios de `23 §12` sin diferencias (L14).

**Lecturas:**
1. **A 2.500 aves/día un camión de 5.500 aves va medio vacío** (46 %): o el camión es más chico, o se cargan dos días de faena con el mismo viaje (no admisible: el ayuno lo impide), o se acepta la baja ocupación. Es la primera señal de "falta de densidad logística".
2. **El verano agrega un viaje** en 5.000, 10.000 y 20.000 aves/día con 5.500 aves por camión: el plan de flota debe dimensionarse para la estación más exigente, no para el promedio.
3. A 20.000 aves/día llega un camión cada ~2 h durante la faena: la **coordinación** (programación de captura, espera en planta, galpón de recepción) pasa a ser una operación en sí misma.

## 3. Distancia geográfica vs distancia por ruta

| Concepto | Definición | Valor en el modelo |
|---|---|---|
| **Radio** (geográfico) | Distancia en línea recta de la granja más lejana a la planta | Barrido 25 / 50 / 100 / 150 / 200 / 300 km (**sensibilidad**, SUP-12B-01) |
| Distancia geográfica **media** | Con granjas repartidas uniformemente en un círculo, la media es 2/3 del radio (SUP-12B-03) | 2/3 × R |
| **Factor de ruta** | km por ruta / km en línea recta | 1,2 / 1,3 / 1,4 (base 1,3). Estudios internacionales citan ~1,2–1,42 (FTE-12B-001 `[PVDP]`); **en Argentina no se midió** (DPV-12B-07) |
| Distancia **por ruta** | Geográfica × factor de ruta (≥ geográfica; test L18) | — |

El radio y el factor de ruta se definirán con 12A (localización) usando rutas reales de las zonas candidatas: caminos rurales de tierra, puentes, accesos inundables y pasos urbanos pueden alargar más que el factor promedio.

## 4. Escenarios de radio (10.000 aves/día, 5.500 aves/camión, factor 1,3)

| Radio (km) | Dist. geo media | Dist. ruta media | Dist. ruta máx. | h de viaje (media · máx.) | ¿Dentro de la ventana de ayuno? (máx.) | Ciclo del camión (h) | km/día | km/ave | Flota mínima · utilización | Ave·h en tránsito/día |
|---|---|---|---|---|---|---|---|---|---|---|
| 25 | 17 | 22 | 32 | 0,4 · 0,5 | Sí | 4,0 | 87 | 0,009 | 1 · 66 % | 3.622 |
| 50 | 33 | 43 | 65 | 0,7 · 1,1 | Sí | 4,7 | 173 | 0,017 | 2 · 39 % | 7.244 |
| 100 | 67 | 87 | 130 | 1,4 · 2,2 | Sí | 6,1 | 347 | 0,035 | 2 · 51 % | 14.488 |
| 150 | 100 | 130 | 195 | 2,2 · 3,2 | Sí | 7,6 | 520 | 0,052 | 2 · 63 % | 21.732 |
| 200 | 133 | 173 | 260 | 2,9 · 4,3 | Sí (al límite: 4,3 vs 4,5 h) | 9,0 | 693 | 0,069 | 2 · 75 % | 28.976 |
| 300 | 200 | 260 | 390 | 4,3 · **6,5** | **No** | 11,9 | 1.040 | 0,104 | 2 · 99 % | 43.464 |

Viaje admisible = ayuno máximo (10 h) − ayuno previo en granja (3 h) − carga (1,5 h) − espera (1 h) = **4,5 h** (test L20). Con ayuno de 8 h quedaría 2,5 h y el radio de 150 km ya fallaría en su borde; con 12 h, 6,5 h.

Flota mínima a 20.000 aves/día: 2 camiones con radio 25 km, 3 con 50–100 km y 4 con 150–300 km.

### 4.1 Cómo afecta el radio a cada dimensión (sin declarar un óptimo)

| Dimensión | Efecto de un radio mayor | Cuantificable hoy | Qué falta |
|---|---|---|---|
| **Tiempo** | Lineal: +1 h de viaje por cada ~60 km de ruta | Sí (velocidad supuesta) | Velocidades reales por tipo de camino (DPV-12B-07) |
| **Bienestar** | Más ave·horas en tránsito (×12 de 25 a 300 km); exposición a calor | Ave·h (indicador de exposición, no de daño) | Relación con lesiones y DOA en Argentina |
| **Mortalidad (DOA)** | Aumenta con tiempo y calor, pero **no hay función validada DOA–distancia** | **No**: el DOA se trata como barrido independiente (§5) | DPV-12B-02 (registros SENASA/frigoríficos) |
| **Bioseguridad** | Rutas más largas cruzan más zonas y granjas de terceros; pero más dispersión reduce el impacto de un brote en un sitio | No | Mapa de granjas y rutas (12A) |
| **Costo** | km/día ×12 entre 25 y 300 km; camión-horas ×3 | Drivers físicos sí; costo **no** | Tarifas (DPV-054) |
| **Utilización de camiones** | Ciclos más largos ocupan mejor la jornada de un camión dedicado (39 % → 99 %), pero no reducen camiones necesarios | Sí | Horas útiles reales por camión |
| **Coordinación de faena** | Con ciclos de 9–12 h un camión hace un solo viaje por jornada; la llegada a la línea depende más de la puntualidad de la captura | Sí (intervalo vs ciclo) | Capacidad del galpón de espera (12C) |

**No se declara radio óptimo:** depende de dónde estén los productores disponibles (DPV-048), del ayuno real, de la estación, de los caminos y del costo, que hoy no se conocen. Lo que sí muestra el modelo es un **límite de bienestar**: con los supuestos actuales, granjas a más de ~200 km de ruta comprometen la ventana de ayuno.

## 5. Sensibilidad a la mortalidad en transporte (DOA)

10.000 aves faenadas/día, 5.500 aves/camión:

| DOA | Aves cargadas/día | Aves DOA/día | Aves DOA/año (250 d) | kg DOA/día | Viajes/día |
|---|---|---|---|---|---|
| 0,2 % | 10.020 | 20 | 5.010 | 58 | 2 |
| 0,3 % (base) | 10.030 | 30 | 7.523 | 87 | 2 |
| 0,5 % | 10.050 | 50 | 12.563 | 146 | 2 |
| 1,0 % | 10.101 | 101 | 25.253 | 293 | 2 |
| 1,63 % (adverso, FTE-156) | 10.166 | 166 | 41.425 | 481 | 2 |

**Lectura:** el DOA casi **no cambia los viajes** (a 20.000 aves/día con 4.000 aves/camión, los viajes equivalentes van de 5,01 a 5,08: siguen siendo 6), pero sí cambia **aves pagadas y no faenadas, bienestar auditable y un flujo de material de destino restringido** (S5 en el mapa). Es un KPI de calidad de la logística, no de capacidad.

## 6. Merma de peso en el viaje (sensibilidad)

Si se activa una merma de 0,2–0,5 % del peso por hora de viaje y espera (`[ESTIMACIÓN]` de 03; base del proyecto = 0, SUP-058), las aves faenadas no cambian pero el peso cargado en granja sube:

| Tasa · radio | 50 km | 150 km | 300 km |
|---|---|---|---|
| 0,2 %/h | 0,34 % · 100 kg/día | 0,63 % · 185 kg/día | 1,07 % · 313 kg/día |
| 0,5 %/h | 0,86 % · 252 kg/día | 1,58 % · 467 kg/día | 2,67 % · 795 kg/día |

(10.000 aves/día; kg vivos que se pagan en granja y no llegan a planta). Conservación: kg cargados = kg faenables + kg DOA + kg merma (test L01). **Quién paga la merma** (kg en granja vs kg en planta) es una cláusula del contrato de integración ([`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md)).

## 7. Granjas abastecedoras y frecuencia

| Escala | Granjas equivalentes con 15.000 · 30.000 · 60.000 plazas | Cosechas/semana | Días de faena que tarda en vaciarse una granja | Viajes por cosecha (5.500 aves) |
|---|---|---|---|---|
| 2.500 | 8,0 · 4,0 · 2,0 | 0,9 · 0,4 · 0,2 | **5,7 · 11,4 · 22,7** | 3 · 6 · 11 |
| 5.000 | 16,1 · 8,0 · 4,0 | 1,8 · 0,9 · 0,4 | 2,8 · 5,7 · 11,4 | 3 · 6 · 11 |
| 10.000 | 32,1 · 16,1 · 8,0 | 3,5 · 1,8 · 0,9 | 1,4 · 2,8 · 5,7 | 3 · 6 · 11 |
| 20.000 | 64,3 · 32,1 · 16,1 | 7,0 · 3,5 · 1,8 | 0,7 · 1,4 · 2,8 | 3 · 6 · 11 |

Granjas equivalentes = plazas de alojamiento del modelo de producción (03 v1.1) ÷ plazas por granja (15–30 mil: orden de magnitud de 03; 60 mil: barrido; dato real DPV-048). Cada granja entrega ~5,7 veces por año (ciclos de 03).

**Hallazgo crítico — tamaño de lote vs ritmo de faena:** 03 indica que una granja de 15.000–30.000 aves "se vacía en 1–2 noches". Eso solo es compatible con plantas de ≥ 10.000–20.000 aves/día. **A 2.500 aves/día, una granja de 30.000 aves tardaría ~11 días de faena en vaciarse**: las últimas aves se faenarían con 2 semanas más de edad y peso, rompiendo el "todo dentro–todo fuera" y el peso objetivo. A escala chica hacen falta lotes chicos (galpones de ~2.500–5.000 aves por cosecha), alojamientos escalonados por galpón (granjas multiedad, peores para bioseguridad) o comprar aves a terceros. Se registra como DPV-12B-10 y DEC-12B-06.

## 8. Bioseguridad y bienestar en la operación logística

- **Camión y cajones son el puente sanitario entre granjas**: la Res. SENASA 723/2025 exige, según extracto, lavado y desinfección en establecimiento registrado antes de una nueva carga y un certificado único que acompaña al vehículo (FTE-234 `[PVDP]`). Lavadero propio en planta vs de terceros: DEC-12B-07 (interfaz con 12C).
- **Sin backhaul:** el camión jaula vuelve vacío (BACKHAUL_POSIBLE = **NO**): el 50 % de los km son vacíos por diseño, no por mala gestión.
- **Ruta "limpia → sucia"**: ordenar la captura de granjas por estado sanitario y edad; las cuadrillas no visitan dos granjas el mismo día salvo protocolo (03).
- **Verano**: viajar de noche, menos aves por cajón (+1 viaje), espera ventilada; el plan de contingencia por ola de calor está en [`conclusiones_logistica.md` §5](conclusiones_logistica.md).

## 9. Qué debe validarse en campo

DPV-054 (contratistas, aves/camión, radio real, DOA, lavado), DPV-058 y DPV-12B-11 (Res. 723/2025), DPV-048 (productores en el radio), DPV-12B-01 (tiempos), DPV-12B-02 (DOA vs distancia y estación), DPV-12B-07 (velocidades y factor de ruta), DPV-12B-10 (tamaño de lote vs ritmo de faena).
