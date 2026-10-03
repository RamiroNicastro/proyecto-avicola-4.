# Upstream opcional — incubación, planta de alimento, granjas y reproductoras

**Fecha:** 2026-10-02 (v1.1, auditoría de procedencia) · Drivers: `14_alimento_balanceado/modelo_upstream.py` (14B v1.1) y `03_produccion_primaria` · Decisiones abiertas: DEC-020, DEC-022, DEC-023, DEC-024, DEC-074–DEC-079

> Cada módulo upstream se **activa o desactiva** por arquitectura. Desactivado = bloque `EXCLUIDO_POR_ARQUITECTURA` con 0 (no "falta de dato"). Activado = conceptos con cantidad de 14B y **sin precio** (salvo galpones, E4 cota inferior). No se usan las cifras viejas de capacidad de incubación retiradas en la reconciliación 14.

## 1. Incubación (pollito = `incubacion`; huevo fértil comprado)

Capacidad física de 14B: posiciones de **setter** y de **hatcher** por separado. Dependen de la cadencia de nacimientos, que ahora es un **input explícito** (`cadencia_nacimientos`, 1–5 cargas/semana) y un **escenario etiquetado**, no una verdad. Por defecto el motor usa 2 cargas/semana con margen 15 % (SUP-146, SUP-147) y lo declara en `escenarios_referencia` y en el mapa de drivers. La v1.0 usaba la misma cadencia sin declararla como escenario. Las cifras de la tabla reproducen exactamente `escenarios_upstream.csv` (bloque `2_incubacion_cadencia`, test N07).

| Escala (aves/día) | Setter (posiciones) | Hatcher (posiciones) | Sala de huevo (huevos) |
|---|---|---|---|
| 2.500 | 55.824 | 18.515 | 13.426 |
| 5.000 | 111.648 | 37.030 | 26.851 |
| 10.000 | 223.296 | 74.060 | 53.703 |
| 20.000 | 446.593 | 148.120 | 107.406 |

Sensibilidad a la cadencia (5.000 aves/día, margen 15 %, 14B): con 1 o 2 cargas/semana hay 37.030 hatchers; con 3, 24.687. Los setters no cambian (111.648). Elegir la cadencia es decisión de diseño (DEC-060, DEC-078), no de CAPEX.

Conceptos (15): terreno (m² PENDIENTE), edificio (m² PENDIENTE, DPV-166), sala de huevo, **setters**, **hatchers**, transferencia, clasificación y conteo, vacunación, lavado, HVAC, bioseguridad, energía, respaldo (kVA PENDIENTE), expedición, auxiliares. Los camiones climatizados de pollitos están en logística (capacidad de camión PENDIENTE: DPV-047). Tecnología (carga única/múltiple, in ovo): DEC-078.

## 2. Planta de alimento (alimento = `propia`)

t/h requerida de 14B para un **perfil de fabricación declarado** (inputs `dias_op_planta_alimento`, `horas_dia_planta_alimento`, `eficiencia_planta_alimento`, `margen_planta_alimento`). El perfil por defecto (5 días × 8 h, eficiencia 0,85, margen 15 %; SUP-148) es un **escenario etiquetado**: a 10.000 aves/día, 3 días × 8 h con eficiencia 0,75 exigen 15,8 t/h y 3 × 16 h con 0,85, 7,0 t/h (14B). t/año, t/semana, t/h y silos reproducen `escenarios_upstream.csv` (test N08). **No** se elige una planta de catálogo sobredimensionada. Si se informa una capacidad nominal de catálogo, el motor calcula la utilización y alerta si es < 50 % (SUP-171).

| Escala | t/h requerida | Utilización con esa t/h | Silos de materias primas m³ | Silos de producto terminado m³ |
|---|---|---|---|---|
| 2.500 | 2,1 | 0,87 | 196 | 33 |
| 5.000 | 4,2 | 0,87 | 392 | 65 |
| 10.000 | 8,4 | 0,87 | 785 | 131 |
| 20.000 | 16,7 | 0,87 | 1.570 | 262 |

Los silos salen de **volumen** = consumo × días de stock ÷ densidad ÷ llenado (14B; 15 d de maíz y soja, 2 d en planta, 3 d en granja; densidad 0,60; DEC-079 abierta), **no** de un tamaño comercial de silo (el volumen unitario sigue PENDIENTE, así que el número de silos no se calcula). Los m³ de materias primas son la suma de maíz y soja de 14B (DERIVADO_CAPEX declarado).

Conceptos (18): terreno, recepción, báscula (1, SUP-172), silos de MP, transporte interno, molienda, dosificación, mezcla, aceite/líquidos, **peletizado y enfriado condicionales** (DEC-076), silos de producto terminado, despacho, polvo/ATEX, control, laboratorio, obra (m² PENDIENTE), utilities. La referencia de fabricante ALI-REF (USD 150.000–300.000 para 8–10 t/h, equipos, Incoterm desconocido, E4) **no** se usa: no es costo instalado.

Compra y façon (opciones A y B): **sin** activos de planta. Los silos de granja existen en ambas, pero son de quien tenga la granja.

## 3. Granjas

| Escala | Plazas de alojamiento | m² de galpón | Galpón a ≥ USD 11,49/plaza (E4, cota) |
|---|---|---|---|
| 2.500 | 120.507 | ≈ 9.486 | ≥ 1,38 M |
| 5.000 | 241.014 | ≈ 18.971 | ≥ 2,77 M |
| 10.000 | 482.029 | ≈ 37.943 | ≥ 5,54 M |
| 20.000 | 964.058 | ≈ 75.885 | ≥ 11,08 M |

**Plazas ≠ galpones ≠ granjas.** Las plazas totales, los m² productivos y el número conceptual de galpones (m² ÷ 1.200 / 1.800 / 2.400 m², sin redondear) salen de 03 vía 14B y reproducen `escenarios_produccion.csv` (test N09): a 10.000 aves/día, 482.029 plazas, 37.943 m², 31,6 / 21,1 / 15,8 galpones. El **número real de granjas es PENDIENTE** (DPV-048): una plaza de alojamiento no es la capacidad de una granja, y el `plazas_granja` de 12B es un escenario, no un dato.

**Capex de la empresa vs capex de productores integrados.** Con granjas propias (fracción f) el motor carga f × galpones al CAPEX de la empresa; el resto (1 − f) se registra con `TITULAR = PRODUCTOR_INTEGRADO` y se informa aparte (`CAPEX_TERCEROS_INFORMATIVO_USD`), **sin** sumarlo (test A05). Integrar productores no tiene CAPEX de galpones para la empresa, pero sí capital de trabajo (alimento por ciclo, 14B) que va a `20_opex`/`21_modelo_financiero`.

**Alcance del precio de galpón.** La cifra de prensa (FTE-081: "más de USD 6 M en galpones para 522.000 aves/ciclo") es una **cota inferior** de alcance desconocido. Los 8 componentes (comederos y bebederos, climatización, silos de granja, agua, energía, bioseguridad, almacenamiento, obras auxiliares) quedan con `INCLUIDO_EN_PAQUETE = PENDIENTE`: no se suman para no contar dos veces lo que el precio quizás ya incluye, y se cuentan como **alcance pendiente** (8 por configuración). Terreno de granjas: PENDIENTE (los m² de galpón son solo una cota inferior; distancias de bioseguridad sin dato). Tecnología de galpón: DEC-022. Fuente oficial a leer: FTE-311 (SAGyP) y FTE-316 (INTA) (DPV-051).

## 4. Reproductoras (solo arquitectura futura)

Con `reproductoras = True` (exige incubación) aparecen REP-GAL (hembras en postura equivalentes de 14B con 3,6 pollitos/reproductora/semana: 3.666 a 2.500 aves/día, 7.332 a 5.000, 14.664 a 10.000 y 29.328 a 20.000; DPV-045) y REP-REC (recría, machos, reposición: PENDIENTE), con `FASE = FUTURO`: **fuera del CAPEX inicial**. El precio de referencia (FTE-314, EE. UU., ≥ USD 280.000 por galpón de 10.000–11.000 reproductoras) es E4 y solo ilustra el orden de magnitud por plaza.
