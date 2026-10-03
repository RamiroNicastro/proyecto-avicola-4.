# Costos de pollito BB, incubación y reproductoras

**Fecha:** 2026-10-02 · Drivers: 14B (`pollitos`, `incubacion` con la cadencia y el margen del escenario CAPEX) · Implementación: `generar_registro()` §POLLITOS en [`modelo_opex.py`](modelo_opex.py)

## 1. Pollito comprado (C0, C1, C2)

`costo = pollitos a recibir (14B) × USD/pollito` + flete del flujo POL (logística).

| Escala | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Pollitos a recibir (por año) | 659.874 | 1.319.749 | 2.639.497 | 5.278.995 |
| Monto con precio E4 (USD/año) | 582.509 | 1.165.020 | 2.330.040 | 4.660.080 |

Precio: CAPIA, pollito BB parrillero, **ARS 1.312,22 sin IVA** (semana 2026-07-06) ÷ 1.486,50 ARS/USD (A3500 del 2026-07-06) = **USD 0,8828/pollito** — **E4** `[PVDP]` (extracto de buscador, página bloqueada). Alertas: `PRECIO_ANTERIOR_A_FECHA_BASE` (no se indexa) y `FLETE_INCLUIDO_PENDIENTE` (no se sabe si el precio es puesto en granja; posible doble conteo con LOG-POL). Equivale a ≈ USD 0,93 por ave faenada (por la mortalidad y el DOA de 03) **solo por el pollito**.

Un extracto de la misma cámara con "$ 16 por unidad" (2026-09-13) es incompatible con el anterior y se **descarta** (REF-POL-CONTRA; regla 16).

## 2. Incubación propia con huevo comprado (C3, CF)

| Concepto | ID | Driver | Estado |
|---|---|---|---|
| Huevo fértil | INC-OP-HUEVO | huevos/año = huevos por pollito vendible (14B, ≈ 1,24) × pollitos/año | Sin precio (DPV-047) |
| Vacunas y aplicación | INC-OP-VAC | pollitos/año | Sin precio |
| Insumos de expedición | INC-OP-INS | pollitos/año | Sin precio |
| Limpieza y desinfección | INC-OP-LIM | cargas/año = cargas/semana (cadencia 2) × semanas equivalentes ≈ 100 | Sin precio; agua y energía en INC-OP-AGUA / INC-OP-ENE |
| Descartes | INC-OP-DES | huevos recibidos − pollitos vendibles (unidades/año) | Sin precio; masa por unidad PENDIENTE |
| Energía eléctrica y HVAC (climatización de salas, setters, hatchers) | INC-OP-ENE | — | **PENDIENTE_CANTIDAD**: 09C no dimensiona la incubadora y su kWh **no** se reutiliza (test X04, mutación M12) |
| Agua | INC-OP-AGUA | — | PENDIENTE_CANTIDAD (universo de utilities INCUBACION) |
| Calidad y bioseguridad | INC-OP-CAL | análisis | PENDIENTE (v1.1) |
| Personal | COSTO_LABORAL (`RRHH_INCUBACION_PENDIENTE`) | — | PENDIENTE_CANTIDAD: 14A no dimensiona la incubadora (no se fabrican FTE) |
| Mantenimiento | MAN-INC-* | activos de la incubadora (BOQ 16) según método | Método PENDIENTE |
| Transporte de huevo / de pollito | LOG-HUE-*, LOG-POL-* | viajes PENDIENTES (capacidad de camión, DPV-047) | — |

| Escala | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Huevos fértiles (por año) | 817.217 | 1.634.434 | 3.268.868 | 6.537.737 |
| Descartes (unidades/año) | 157.343 | 314.685 | 629.371 | 1.258.742 |
| Stock de huevos en almacén (5 d) | 11.675 | 23.349 | 46.698 | 93.396 |
| Huevos en incubación (WIP) | 48.508 | 97.016 | 194.032 | 388.064 |

Setter y hatcher **no** generan costos separados por máquina: su energía depende de un dimensionamiento que no existe; la cadencia es un escenario etiquetado (SUP-147). Test A03: pollito comprado no carga incubación y viceversa.

## 3. Reproductoras (CF, arquitectura futura)

Estructura preparada sin valores: REP-AVE (reposición), REP-ALI, REP-SAN, REP-ENE, REP-OTR con `FASE = FUTURO`. No cuentan como costo (test A08). Requiere evidencia (DPV-045).

## 4. Completitud (auditoría v1.1)

La incubación propia tiene representados sus **12 bloques materiales** (huevo, vacunas, energía/HVAC, RRHH, agua, lavado/desinfección, mantenimiento, consumibles, descartes, transporte de huevo, transporte de pollito, calidad/bioseguridad) en [`completitud_arquitecturas_opex.csv`](completitud_arquitecturas_opex.csv): cobertura estructural 100 %, física 42 % (C3-10000), de costeo 0 %. Setter y hatcher son drivers de CAPEX y de capacidad, no costos operativos por sí mismos (test X02, mutación M14).
