# Utilities, frío, efluentes y servicios generales — CAPEX

**Fecha:** 2026-10-02 (v1.1, auditoría de procedencia) · Drivers: `11_agua_efluentes/modelo_utilities.py` (09C) a través de 12C · Procedencia: [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv) · Sin tecnología elegida (DEC-043, DEC-045, DEC-046, DEC-047)

> Todos los conceptos de este documento están **sin precio**. CAPEX consume las variables de 09C tal como 09C las publica (test N19: C1 reproduce `escenarios_utilities.csv` en 4 escalas y 3 niveles). Lo que 09C deja PENDIENTE (carga frigorífica total, demanda eléctrica máxima, potencia térmica pico, lodos) sigue PENDIENTE en CAPEX: no se reemplaza por una cota.

## 1. Drivers por escala (09C, C1 perfil P1, medio; bajo–alto en el mapa de drivers)

| Driver (variable de 09C) | 2.500 | 5.000 | 10.000 | 20.000 | Uso en CAPEX |
|---|---|---|---|---|---|
| Agua utilizada (L/ave): bajo / medio / alto | 15 / 25 / 38 | ídem | ídem | ídem | sensibilidad de consumo |
| `agua_captada_m3_dia` (medio) | 62,5 | 125 | 250 | 500 | AG-CAP |
| `agua_descargada_m3_dia` = agua × fracción a efluente (0,80 / 0,88 / 0,95) | 55 | 110 | 220 | 440 | EF-PAQ (capacidad) |
| `caudal_horario_maximo_ilustrativo_m3_h` | 9,4 | 18,8 | 37,5 | 75 | AG-TRA, AG-BOM (parámetro) |
| DQO kg/d: método A / método B | 250 / 297 | 500 / 594 | 1.000 / 1.188 | 2.000 / 2.376 | EF-BIO: **ambos informados, no se elige** |
| `masa_biologica_potencialmente_segregable_en_origen_t_dia` | 1,5 | 3,0 | 6,1 | 12,2 | SB-L9 (subproductos). **No** son sólidos del efluente |
| `solidos_que_entran_efectivamente_al_efluente_t_dia` | PENDIENTE | | | | EF-LOD PENDIENTE |

## 2. Frío — cuatro magnitudes que no se mezclan

| Magnitud | Valor (10.000 aves/día, C1) | Origen | Estado |
|---|---|---|---|
| **Carga física calculada** (parcial) | producto 99 kWf + agua de chiller 69 kWf + congelación 10 kWf (media 20 h; C1 perfil P1) | 09C, variables separadas | ESTIMACIÓN con SUPUESTO; **no es la carga total** |
| Cargas adicionales ilustrativas | 67 kWf | 09C | **SUPUESTO** ilustrativo: no se suma como capacidad |
| **Benchmark global** | 2.538 kWh/d de frío de proceso (reparto top-down del indicador kWh/ave) | 09C | energía, **no kWf**; CAPEX no lo convierte a potencia |
| **Contradicción** física vs benchmark | ×5,7 (×5,2–6,2 según nivel) | 09C `brecha_frio_fisico_vs_reparto_indicador_ratio` | **ABIERTA** (T16-04): CAPEX no la resuelve |
| Carga frigorífica total | — | 09C | PENDIENTE (balance frigorífico, DPV-109) |
| **Capacidad de diseño** | — | — | PENDIENTE |
| **Margen** | — | — | PENDIENTE (no adoptado) |

**Corrección v1.1:** la v1.0 publicaba el paquete de frío con una "cota inferior" igual a la **suma** de las cuatro cargas de 09C (incluida la ilustrativa). Esa suma era una magnitud de CAPEX que ningún módulo publica y mezclaba un supuesto con cálculos; además el RFQ la usaba como capacidad. Ahora FR-PAQ no tiene capacidad; su detalle (en BOQ y RFQ) muestra **BASE, BENCHMARK, CONTRADICCIÓN ABIERTA, DISEÑO PENDIENTE, MARGEN PENDIENTE y ESTADO "no cotizable con una sola cifra"**. El agua helada (FR-AGH) tampoco toma la carga parcial de reposición como capacidad.

| Componente del paquete FR-PAQ (incluidos en el paquete, SUP-16-06) | Cantidad | Estado |
|---|---|---|
| FR-PAN Paneles de cámaras | m² de cámaras de 12C | DERIVADO (suma de áreas 12C) |
| FR-COMP / FR-COND / FR-EVAP | — | PENDIENTE (kWf total) |
| FR-PIP / FR-REF / FR-CTL | 1 lote | alcance del paquete; refrigerante abierto (DEC-046) |
| FR-AGH Agua helada (EQ-37) | — | PENDIENTE |
| FR-DCK Docks (EQ-65) | — | PENDIENTE (posiciones, D12-01) |
| FR-TUN Túnel (si congelado propio) | t/día de congelación de 09C | DIRECTO / cálculo del modelo fuente |

## 3. Agua y efluentes — parametrizados, sin tecnología

| Concepto | Cantidad | Origen |
|---|---|---|
| AG-CAP Captación o conexión | agua captada m³/d | 09C directo |
| AG-ALM Almacenamiento (EQ-72) | 0,5 / 1 / 2 días de agua captada | DERIVADO_CAPEX (SUP-16-15) |
| AG-TRA Tratamiento · AG-BOM Bombeo | caudal horario máximo ilustrativo | 09C (SUPUESTO de 09C) |
| AG-DIS Distribución | m² construidos | 12C directo |
| EF-PAQ Paquete de efluentes | m³/d descargados | 09C directo |
| EF-PRE · EF-DAF | caudal máximo ilustrativo de efluente | 09C (SUPUESTO de 09C) |
| EF-ECU Ecualización | **PENDIENTE** (corrección v1.1: la v1.0 tomaba el volumen diario como volumen del tanque, es decir, 24 h de retención implícitas) | tiempo de retención no definido |
| EF-BIO Biológico | **PENDIENTE**; detalle con DQO método A y B (corrección v1.1: la v1.0 elegía el máximo de los dos) | 09C, no se elige método ni tecnología |
| EF-LOD Lodos | PENDIENTE (DPV-114) | — |

## 4. Electricidad y térmico — consumo ≠ potencia ≠ pico

| Magnitud | 10.000 aves/día (C1) | Origen | Uso |
|---|---|---|---|
| Consumo eléctrico | 8.184 kWh/d | 09C `kwh_total_dia_operativo` | OPEX; **nunca** kW |
| Potencia media de proceso | 518 kW | 09C (kWh ÷ 14 h) | solo texto informativo |
| Pico de demanda | — | 09C: PENDIENTE | — |
| Transformador (EL-TRA) | — | PENDIENTE (DPV-095) | no se dimensiona desde kWh ni desde potencia media (tests N05, N06) |
| Grupo electrógeno (EL-GEN) | — | PENDIENTE (DEC-047) | cargas críticas de 09C son ilustrativas; su suma es solo texto |
| UPS (EL-UPS) | — | PENDIENTE | — |
| Térmico medio de escaldado | 140 kWt | 09C | texto informativo |
| Caldera (TE-GEN) | — | PENDIENTE (pico térmico de 09C PENDIENTE) | — |
| Aire comprimido (AC-COM) | — | PENDIENTE (DPV-095) | — |

La auditoría confirmó que la v1.0 **no** convertía kWh en kW ni dimensionaba transformador o grupo: esas cantidades ya eran PENDIENTE. Se agregó la prueba y una mutación (D01) que lo verifica.

## 5. Servicios generales

| Concepto | Cantidad | Nota |
|---|---|---|
| IT-HW, IT-SW, IT-SEN (SCADA EQ-76), IT-RED | 1 lote c/u | Software comprado = CAPEX; suscripciones = OPEX |
| IT-ETQ Balanzas etiquetadoras (EQ-54) | PENDIENTE (puestos) | RFQ L7 |
| LAB-EQ Laboratorio (si propio, DEC-065) | 1 lote | — |
| SI-DET, SI-COM, SI-PRO Incendio | 1 lote c/u | requerimientos municipales y de bomberos PENDIENTES (DPV-106) |
| PER-EQ, MOB-OF | 1 lote c/u | dimensionar con el pico simultáneo (SUP-141) |

## 6. Qué falta

Lista de cargas por equipo (DPV-095) → pico, kVA, kWt, aire; balance frigorífico de proveedor que cierre la brecha ×5,7 (DPV-109); límites de vuelco, tiempo de retención y tecnología de efluentes (DPV-106, DEC-043); política de respaldo (DEC-047); precios (RFQ 4–7 de [`plan_cotizaciones.md`](plan_cotizaciones.md)).
