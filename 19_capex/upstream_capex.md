# Upstream opcional — incubación, planta de alimento, granjas y reproductoras

**Fecha:** 2026-10-02 · Drivers: `14_alimento_balanceado/modelo_upstream.py` (14B v1.1) y `03_produccion_primaria` · Decisiones abiertas: DEC-020, DEC-022, DEC-023, DEC-024, DEC-074–DEC-079

> Cada módulo upstream se **activa o desactiva** por arquitectura. Desactivado = bloque `EXCLUIDO_POR_ARQUITECTURA` con 0 (no "falta de dato"). Activado = conceptos con cantidad de 14B y **sin precio** (salvo galpones, E4 cota inferior). No se usan las cifras viejas de capacidad de incubación retiradas en la reconciliación 14.

## 1. Incubación (pollito = `incubacion`; huevo fértil comprado)

Capacidad física de 14B: posiciones de **setter** y de **hatcher** por separado, con cadencia de 2 cargas/semana y margen de diseño 15 % (SUP-146, SUP-147).

| Escala (aves/día) | Setter (posiciones) | Hatcher (posiciones) | Sala de huevo (huevos) |
|---|---|---|---|
| 2.500 | 55.824 | 18.515 | 13.426 |
| 5.000 | 111.648 | 37.030 | 26.851 |
| 10.000 | 223.296 | 74.060 | 53.703 |
| 20.000 | 446.593 | 148.120 | 107.406 |

Conceptos (15): terreno (m² PENDIENTE), edificio (m² PENDIENTE, DPV-16-13), sala de huevo, **setters**, **hatchers**, transferencia, clasificación y conteo, vacunación, lavado, HVAC, bioseguridad, energía, respaldo (kVA PENDIENTE), expedición, auxiliares. Los camiones climatizados de pollitos están en logística (capacidad de camión PENDIENTE: DPV-047). Tecnología (carga única/múltiple, in ovo): DEC-078.

## 2. Planta de alimento (alimento = `propia`)

t/h requerida de 14B (5 días × 8 h, eficiencia 0,85, margen 15 %; SUP-148); **no** se elige una planta de catálogo sobredimensionada. Si se informa una capacidad nominal de catálogo, el motor calcula la utilización y alerta si es < 50 % (SUP-16-17).

| Escala | t/h requerida | Utilización con esa t/h | Silos de materias primas m³ | Silos de producto terminado m³ |
|---|---|---|---|---|
| 2.500 | 2,1 | 0,87 | 196 | 33 |
| 5.000 | 4,2 | 0,87 | 392 | 65 |
| 10.000 | 8,4 | 0,87 | 785 | 131 |
| 20.000 | 16,7 | 0,87 | 1.570 | 262 |

(Silos de producto terminado ≈ 1/6 de los de materias primas con los días de stock base de 14B: 15 d de maíz y soja, 2 d de alimento en planta; DEC-079 abierta.)

Conceptos (18): terreno, recepción, báscula (1, SUP-16-18), silos de MP, transporte interno, molienda, dosificación, mezcla, aceite/líquidos, **peletizado y enfriado condicionales** (DEC-076), silos de producto terminado, despacho, polvo/ATEX, control, laboratorio, obra (m² PENDIENTE), utilities. La referencia de fabricante ALI-REF (USD 150.000–300.000 para 8–10 t/h, equipos, Incoterm desconocido, E4) **no** se usa: no es costo instalado.

Compra y façon (opciones A y B): **sin** activos de planta. Los silos de granja existen en ambas, pero son de quien tenga la granja.

## 3. Granjas

| Escala | Plazas de alojamiento | m² de galpón | Galpón a ≥ USD 11,49/plaza (E4, cota) |
|---|---|---|---|
| 2.500 | 120.507 | ≈ 9.486 | ≥ 1,38 M |
| 5.000 | 241.014 | ≈ 18.971 | ≥ 2,77 M |
| 10.000 | 482.029 | ≈ 37.943 | ≥ 5,54 M |
| 20.000 | 964.058 | ≈ 75.885 | ≥ 11,08 M |

**Capex de la empresa vs capex de productores integrados.** Con granjas propias (fracción f) el motor carga f × galpones al CAPEX de la empresa; el resto (1 − f) se registra con `TITULAR = PRODUCTOR_INTEGRADO` y se informa aparte (`CAPEX_TERCEROS_INFORMATIVO_USD`), **sin** sumarlo (test A05). Integrar productores no tiene CAPEX de galpones para la empresa, pero sí capital de trabajo (alimento por ciclo, 14B) que va a `20_opex`/`21_modelo_financiero`.

**Alcance del precio de galpón.** La cifra de prensa (FTE-081: "más de USD 6 M en galpones para 522.000 aves/ciclo") es una **cota inferior** de alcance desconocido. Los 8 componentes (comederos y bebederos, climatización, silos de granja, agua, energía, bioseguridad, almacenamiento, obras auxiliares) quedan con `INCLUIDO_EN_PAQUETE = PENDIENTE`: no se suman para no contar dos veces lo que el precio quizás ya incluye, y se cuentan como **alcance pendiente** (8 por configuración). Terreno de granjas: PENDIENTE (los m² de galpón son solo una cota inferior; distancias de bioseguridad sin dato). Tecnología de galpón: DEC-022. Fuente oficial a leer: FTE-16-002 (SAGyP) y FTE-16-007 (INTA) (DPV-16-07).

## 4. Reproductoras (solo arquitectura futura)

Con `reproductoras = True` (exige incubación) aparecen REP-GAL (hembras en postura equivalentes de 14B con 3,6 pollitos/reproductora/semana: 3.666 a 2.500 aves/día, 7.332 a 5.000, 14.664 a 10.000 y 29.328 a 20.000; DPV-045) y REP-REC (recría, machos, reposición: PENDIENTE), con `FASE = FUTURO`: **fuera del CAPEX inicial**. El precio de referencia (FTE-16-005, EE. UU., ≥ USD 280.000 por galpón de 10.000–11.000 reproductoras) es E4 y solo ilustra el orden de magnitud por plaza.
