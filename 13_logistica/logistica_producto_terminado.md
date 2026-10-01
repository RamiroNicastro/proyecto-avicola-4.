# Logística de producto terminado — planta → clientes

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de interpretación) · Sesión 12B · Fase 0

> **Alcance:** toneladas que salen por día, separadas en **refrigerado** y **congelado**; viajes, ocupación y frecuencia; comparación **planta → CD → tiendas** vs **planta → tiendas** vs **cross-dock**; escenarios de red ancla A/B/C con demanda variable; relación entre inventario (días de producción vs días calendario) y despacho.
> **No** se asume que los 90 supermercados son clientes (regla 8), ni que reciben directo, ni un volumen. **No** hay costos. Las capacidades de camión son **capacidades de ESCENARIO** (barrido; no validadas ni cotizadas, DPV-084): cada cifra de viajes indica la capacidad que la produce y no es un requerimiento de flota. Sin capacidad elegida, el modelo devuelve PENDIENTE.
> Cifras: bloques `producto_terminado`, `red_ancla`, `asignacion_canales`, `inventario_ciclo` e `inventario_seguridad` de [`escenarios_logistica.csv`](escenarios_logistica.csv).

---

## 1. Toneladas por día y por cadena de frío

Producto comestible en **peso comercial** (configuración B trozado, 2,9 kg): **6,0 / 12,0 / 24,0 / 47,9 t por día operativo** (A entero 24,1 y C deshuesado 20,5 t a 10.000 aves/día). La partición refrigerado / congelado / exportación usa los perfiles **ilustrativos** P1–P3 de `23` (SUP-055; la demanda real por canal es DPV-085):

| t/día operativo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| P1 (90/10/0) refrigerado · congelado | 5,4 · 0,6 | 10,8 · 1,2 | 21,6 · 2,4 | 43,1 · 4,8 |
| P2 (60/40/0) refrigerado · congelado | 3,6 · 2,4 | 7,2 · 4,8 | 14,4 · 9,6 | 28,8 · 19,2 |
| P3 (50/30/20) refrig. · cong. · exportación | 3,0 · 1,8 · 1,2 | 6,0 · 3,6 · 2,4 | 12,0 · 7,2 · 4,8 | 24,0 · 14,4 · 9,6 |

**Refrigerado y congelado nunca comparten cálculo de viajes** (test L11): tienen temperatura, vehículo (o compartimento), vida útil, clientes y frecuencia distintos. El modelo calcula `techo(t_refrigerado/cap)` y `techo(t_congelado/cap)` por separado; nunca `techo(suma/cap)`.

## 2. Refrigerado: frecuencia diaria obligada

El refrigerado vive días (SUP-051; vida útil real DPV-078), así que se despacha casi todos los días. Con 5 días de faena, despachar 6 o 7 días por semana obliga a **guardar producto el fin de semana**.

Perfil P1, troncal de 12 t (capacidad de escenario, no validada), viajes por semana (ocupación) y stock de ciclo máximo:

| Escala | 5 despachos/sem | 6 despachos/sem | 7 despachos/sem | Stock de ciclo máx. (5 · 6 · 7 despachos), t |
|---|---|---|---|---|
| 2.500 | 5 (45 %) | 6 (37 %) | 7 (32 %) | 5,4 · 9,0 · 11,6 |
| 5.000 | 5 (90 %) | 6 (75 %) | 7 (64 %) | 10,8 · 18,0 · 23,1 |
| 10.000 | 10 (90 %) | 12 (75 %) | 14 (64 %) | 21,6 · 35,9 · 46,2 |
| 20.000 | 20 (90 %) | 18 (100 %) | 21 (86 %) | 43,1 · 71,9 · 92,4 |

**Más días de despacho = más viajes con menos carga cada uno y más stock en cámara.** Es la consecuencia física de que la faena es de lunes a viernes y la venta de lunes a domingo.

## 3. Congelado: acumulable para llenar camiones

El congelado tolera semanas a meses en cámara (`[PVDP]`, DPV-078), de modo que **puede acumularse hasta llenar un camión**. Perfil P2, troncal de 12 t (capacidad de escenario, no validada):

| Escala | 1 despacho/sem: viajes (ocup.) · stock máx. | 2/sem | 3/sem | 6/sem |
|---|---|---|---|---|
| 2.500 | 1 (100 %) · 12,0 t | 2 (50 %) · 9,6 t | 3 (33 %) · 7,2 t | 6 (17 %) · 4,0 t |
| 5.000 | 2 (100 %) · 24,0 t | 2 (100 %) · 19,2 t | 3 (67 %) · 14,4 t | 6 (33 %) · 8,0 t |
| 10.000 | 4 (100 %) · 47,9 t | 4 (100 %) · 38,3 t | 6 (67 %) · 28,8 t | 6 (67 %) · 16,0 t |
| 20.000 | 8 (100 %) · 95,9 t | 8 (100 %) · 76,7 t | 9 (89 %) · 57,5 t | 12 (67 %) · 32,0 t |

Con P1 (solo 10 % congelado) a 2.500 aves/día, despachar el congelado a diario llenaría un camión de escenario de 12 t al **4 %** de su capacidad másica; una vez por semana, al 25 %. **El intercambio es explícito:** camiones llenos ↔ más toneladas inmovilizadas en cámara (capital de trabajo físico) — se elige por canal y producto, no por regla (DEC-12B-04).

## 4. Pallets, ventanas de entrega y paradas

- **Pallets:** no hay base suficiente (kg por pallet, tipo de pallet, alturas, pallets por camión: DPV-12B-04). Barrido **ilustrativo**: con 500 / 750 / 1.000 kg por pallet, la salida comestible equivale a 12 / 8 / 6 pallets por día operativo a 2.500 aves/día y 96 / 64 / 48 a 20.000. No se usan para dimensionar nada.
- **Ventana de entrega:** desconocida (DPV-036, DPV-12B-09). El modelo calcula el **tramo de entregas** de cada ruta (paradas × (tiempo de parada + traslado)) y deja `excede_ventana = PENDIENTE` hasta conocer la ventana. Con 7–10 paradas de 0,75 h, el tramo es de **8–11 h**: si las ventanas de recepción fueran cortas (dato pendiente), harían falta más rutas con menos paradas cada una.
- **Jornada:** las rutas se limitan a las paradas que caben en **12 h útiles por camión** (SUP-12B-08) después de cargar e ir y volver; si no cabe ni una parada, la ruta es **inviable en jornada** (flag).

## 5. Red ancla: tres escenarios sin volumen asumido

| Escenario | Locales | Qué representa |
|---|---|---|
| **A — sin red ancla** | 0 | Toda la producción va a otros canales: mayoristas/distribuidores, carnicerías/pollerías, gastronomía, elaboradores, exportación |
| **B — red parcial** | 45 (50 % de 90) | Adhesión parcial; la fracción es un parámetro (`fraccion_locales`) |
| **C — red fuerte** | 90 | Todos los locales compran al proyecto |

El **volumen por local es una variable** (barrido 25 / 50 / 100 / 150 / 300 kg/local/día, los escenarios de prueba de `02`); ningún valor es supuesto de demanda. Los tres escenarios se calculan de forma **independiente** (test L12: cambiar B no altera A ni C) y **no son sumables**.

### 5.1 Densidad de entrega (de `02 §3.1`)

| kg/local/día | kg por parada con 3 entregas/sem | con 6 entregas/sem |
|---|---|---|
| 25 | 58 | 29 |
| 100 | 233 | 117 |
| 300 | 700 | 350 |

Paradas por día de despacho (6 días): B = 22,5 (3/sem) o 45 (6/sem); C = 45 o 90.

### 5.2 Planta → tiendas (directo) vs planta → CD → tiendas vs cross-dock

**Supuestos que generan las cifras** (todos de escenario): 100 kg/local/día; 3 entregas/semana; 6 despachos/semana; camión de reparto de **6 t** y troncal de **20 t** (capacidades de escenario); **0,75 h por parada**; 8 km entre paradas; máx. 10 paradas por recorrido; **12 h útiles por camión**; 1 h de carga en andén; 70 km/h en ruta y 20 km/h urbano; cross-dock a 25 km de las tiendas; distancia planta–AMBA por ruta 30 / 300 / 600 km (sin localización: la define 12A).

| Modo | Escenario | t/día de despacho | Viajes troncales (20 t) | Rutas de reparto, 6 t (paradas/ruta) a 30 · 300 · 600 km | km/día (30 · 300 · 600 km) | km/t (30 · 300 · 600) | Flags |
|---|---|---|---|---|---|---|---|
| **Directo** | B | 5,25 | — | 3 (7,5) · 12 (1,9) · 23 (1,0) | 360 · 7.380 · 27.780 | 69 · 1.406 · 5.291 | 600 km: inviable en jornada con estos supuestos |
| **CD del cliente** | B | 5,25 | 1 | — (última milla del cliente) | 60 · 600 · 1.200 | 11 · 114 · 229 | 600 km: excede conducción y jornada de un chofer |
| **Cross-dock** | B | 5,25 | 1 | 4 (5,6) | 440 · 980 · 1.580 | 84 · 187 · 301 | 600 km: troncal excede jornada |
| **Directo** | C | 10,5 | — | 6 (7,5) · 23 (2,0) · 45 (1,0) | 720 · 14.160 · 54.360 | 69 · 1.349 · 5.177 | 600 km: inviable en jornada con estos supuestos |
| **CD del cliente** | C | 10,5 | 1 | — | 60 · 600 · 1.200 | 6 · 57 · 114 | ídem |
| **Cross-dock** | C | 10,5 | 1 | 7 (6,4) | 770 · 1.310 · 1.910 | 73 · 125 · 182 | ídem |

Camión-horas por día (C, 300 km): directo 272, CD 11, cross-dock 87. Con `n` de CD desconocido (DPV-036) las paradas en CD quedan PENDIENTES; la última milla del CD **no** está en estos km (la hace el cliente).

### 5.3 Sensibilidad directo / CD / cross-dock (un parámetro por vez)

Base: escenario C, 100 kg/local, 3 entregas/semana, 300 km, 10 paradas máx., reparto 6 t / troncal 20 t, 0,75 h por parada, 12 h útiles (bloque `red_ancla_sensibilidad` del CSV). km/t (rutas de reparto):

| Parámetro variado | Valor | Directo | CD del cliente | Cross-dock |
|---|---|---|---|---|
| Distancia planta–AMBA | 30 · 100 · 150 · 300 · 600 km | 69 (6) · 168 (7) · 291 (9) · 1.349 (23) · 5.177 (45, inviable) | 6 · 19 · 29 · 57 · 114 | 73 (7) · 87 (7) · 96 (7) · 125 (7) · 182 (7) |
| Locales por recorrido (máx.) | 6 · 10 · 15 | 1.349 en los tres (a 300 km la jornada solo admite 2 paradas) | 57 | 130 (8) · 125 (7) · 125 (7) |
| kg/local/día | 25 · 100 · 300 | 5.394 · 1.349 · 450 | 229 · 57 · 38 (2 troncales) | 499 · 125 · 61 |
| Capacidad de reparto | 3 · 6 · 12 t | 1.349 (no cambia: manda la jornada) | 57 | 125 |
| Tiempo por parada | 0,5 · 0,75 · 1,0 h | 1.349 · 1.349 · 2.606 (45 rutas) | 57 | 115 · 125 · 130 |
| Horas útiles por camión | 10 · 12 · 14 h | 2.606 (inviable) · 1.349 · 891 | 57 | 134 · 125 · 115 |

**Lecturas (resultado del escenario, no regla):**
1. Con la parametrización actual de distancia, tiempo de servicio por parada, cantidad de locales, carga y jornada, **la distribución directa resulta mucho menos eficiente que la consolidación vía CD o cross-dock** cuando la planta está lejos del AMBA: a 300 km caben ~2 paradas por jornada y el directo requiere ~24 veces más km por tonelada que el CD (1.349 vs 57). **300 km no es una frontera universal**: con 100–150 km la diferencia se reduce (168–291 vs 19–29 km/t), y con más horas útiles, menos tiempo por parada o más kg por local el directo mejora.
2. Cerca del AMBA (30 km) el directo es físicamente posible pero sigue siendo una operación de 3–12 rutas diarias con muchas paradas: **el número de paradas y la jornada, no las toneladas, dimensionan la flota de reparto** (la capacidad del camión de reparto no cambia el resultado en el rango probado).
3. El **CD del cliente** minimiza km propios pero traslada la última milla al supermercado (fee de CD posible, DPV-039) y reduce el control de góndola; el **cross-dock** es el intermedio.
4. Con 600 km, aun el troncal (≈ 17 h de ida y vuelta) excede la jornada de un chofer bajo estos supuestos: requeriría relevo, pernocte o un punto intermedio. Es un insumo para 12A, no una conclusión de localización.

**No se declara ganador** entre directo, CD y cross-dock (DEC-016, DEC-12B-01): faltan la existencia y ubicación de CD de la red, ventanas, fee, costos y nivel de servicio.

### 5.4 Asignación por canal según escala (día calendario)

Producción comestible (P1, 5 días de faena): 4,1 / 8,2 / 16,4 / 32,8 t por día calendario. El resto de la red va a otros canales con el reparto **ilustrativo** de ESC-BAS de `02` (mayorista 50 %, carnicerías/pollerías 33 %, gastronomía 10 %, elaborador 7 %; SUP-12B-13):

| 10.000 aves/día | Red atendida | Participación de la red | Mayorista | Carn./pollerías | Gastronomía | Elaborador |
|---|---|---|---|---|---|---|
| A | 0 | 0 % | 8,2 | 5,5 | 1,6 | 1,1 |
| B · 100 kg/local | 4,5 | 27 % | 6,0 | 4,0 | 1,2 | 0,8 |
| C · 100 kg/local | 9,0 | 55 % | 3,7 | 2,5 | 0,7 | 0,5 |
| C · 150 kg/local | 13,5 | 82 % | 1,5 | 1,0 | 0,3 | 0,2 |

Con C · 150 kg/local, a 2.500 aves/día la planta solo cubre el **30 %** de la demanda de la red, y a 20.000 la red absorbe el **41 %**. La asignación conserva toneladas (red + canales + exportación = comestible, test L05) pero **no resuelve el mix**: qué partes pide la red y qué partes sobran se analiza en `23 §4` y `02 §2.3`.

**Lógica logística por canal (cualitativa):**

| Canal | Forma típica de entrega | Densidad | Comentario |
|---|---|---|---|
| Supermercado con CD | Carga completa a 1–n CD | Alta | Fee y reglas del CD (DPV-039) |
| Supermercado sin CD | Reparto multiparada | Baja | §5.2 |
| Mayorista / distribuidor | Retiro en planta o carga completa | **Alta** | El distribuidor hace la última milla de carnicerías y pollerías |
| Carnicerías / pollerías directas | Reparto multiparada, kg bajos | **Muy baja** | Conviene vía distribuidor salvo zona cercana |
| Gastronomía | Multiparada, entregas chicas y frecuentes | Muy baja | Cadenas con CD = carga consolidada |
| Elaborador / industria | Carga completa programada, a menudo congelada | Alta | Calendario estable, acumulable |
| Puerto / depósito exportador | Contenedor completo | Máxima | [`logistica_exportacion.md`](logistica_exportacion.md) |

## 6. Inventario y logística: días de producción vs días calendario

Se integran los dos conceptos de `23 §11` (SUP-056) y se agrega el **ciclo semanal** que el despacho impone:

1. **Stock de ciclo** (lo que obliga el calendario): producción de lunes a viernes, despacho uniforme en 5, 6 o 7 días, desfase de 1 día (lo faenado hoy se despacha desde mañana; SUP-12B-09). Es el mínimo para que el despacho nunca falte.
2. **Stock de seguridad** (decisión comercial): N días expresados en **días de producción** (t/día operativo × N) o **días calendario** (t/día operativo × días de faena/365 × N).

Comestible total, cota superior:

| Escala | Stock de ciclo máx. con 5 / 6 / 7 despachos (5 d faena), t | Ídem medio | t·día inmovilizadas por semana (5 / 6 / 7) | Seguridad 7 días: producción · calendario, t |
|---|---|---|---|---|
| 2.500 | 6,0 / 10,0 / 12,8 | 6,0 / 7,1 / 8,6 | 42 / 50 / 60 | 41,9 · 28,7 |
| 5.000 | 12,0 / 20,0 / 25,7 | 12,0 / 14,3 / 17,1 | 84 / 100 / 120 | 83,9 · 57,4 |
| 10.000 | 24,0 / 39,9 / 51,4 | 24,0 / 28,5 / 34,2 | 168 / 200 / 240 | 167,8 · 114,9 |
| 20.000 | 47,9 / 79,9 / 102,7 | 47,9 / 57,1 / 68,5 | 336 / 399 / 479 | 335,5 · 229,8 |

(Las cifras de seguridad reproducen `23 §11`, test L14.) Con 6 días de faena y 6 despachos, el stock de ciclo vuelve a 1 día de producción.

**Qué cambia con cada concepto:**

| | Días de producción | Días calendario |
|---|---|---|
| Pregunta | ¿Cuántas jornadas de faena caben en la cámara? | ¿Cuántos días de venta cubre el stock? |
| Almacenamiento | Mayor (base: día de faena) | 68 % del anterior con 250 días de faena (82 % con 300) |
| Frecuencia de despacho | No la cambia | No la cambia |
| Camiones | **No cambian**: los viajes dependen del despacho diario, no del stock (test L10) | Ídem |
| Capital inmovilizado (conceptual) | t·día en cámara: crece con días de despacho y de seguridad | Ídem; **no se calcula capital financiero** |

**Regla del modelo:** stock (t, período "stock") y despacho (t por día de despacho) son variables distintas; el stock nunca se suma a un flujo ni modifica viajes (L10). Lo que sí cambia viajes es el **calendario de despacho** (§2–3).

## 7. Faltantes que bloquean la siguiente iteración

DPV-036 / DPV-12B-09 (CD de la red, ventanas, pedido mínimo, pallets), DPV-084 (capacidades), DPV-085 (refrigerado/congelado por canal), DPV-078 (vida útil), DPV-042 (costos de distribución, para la fase económica), DPV-039 (fee de CD).
