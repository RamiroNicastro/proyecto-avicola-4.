# Utilities, frío, efluentes y servicios generales — CAPEX

**Fecha:** 2026-10-02 · Drivers: `11_agua_efluentes/modelo_utilities.py` (09C) a través de 12C · Sin tecnología elegida (DEC-043, DEC-045, DEC-046, DEC-047)

> Todos los conceptos de este documento están **sin precio**. Varias capacidades también están **PENDIENTES** (demanda eléctrica máxima, potencia térmica pico, carga frigorífica total, caudal de aire): el BOQ muestra cotas inferiores, nunca un valor inventado.

## 1. Drivers por escala (09C, nivel medio)

| Driver | 2.500 | 5.000 | 10.000 | 20.000 | Estado |
|---|---|---|---|---|---|
| Agua captada m³/d | 62,5 | 125 | 250 | 500 | ESTIMACIÓN con rangos `[PVDP]` |
| Efluente m³/d | 55 | 110 | 220 | 440 | ESTIMACIÓN |
| Caudal horario máximo ilustrativo m³/h | 9,4 | 18,8 | 37,5 | 75 | SUPUESTO (factor ilustrativo) |
| DQO kg/d (máx. de métodos A/B) | 297 | 594 | 1.188 | 2.376 | ESTIMACIÓN `[PVDP]` |
| Potencia media de proceso kW | 129,5 | 258,9 | 517,9 | 1.035,7 | ESTIMACIÓN; **pico PENDIENTE** |
| Térmico escaldado medio kWt | 35 | 70 | 140 | 279 | ESTIMACIÓN; **pico PENDIENTE** |
| Frío: cota inferior kWf (C1, P1) | ≥ 61 | ≥ 123 | ≥ 245 | ≥ 491 | Σ cargas preliminares; **total PENDIENTE** (DPV-109) |
| Frío: cota inferior kWf (C3, P2) | ≥ 69 | ≥ 137 | ≥ 275 | ≥ 550 | ídem |
| Agua helada para chiller kWf (C1) | 17 | 35 | 69 | 138 | ESTIMACIÓN preliminar |
| Carga crítica ilustrativa kW (respaldo) | ≈ 10 | ≈ 20 | ≈ 40 | ≈ 80 | SUPUESTO proxy (DEC-047) |

## 2. Frío (paquete FR-PAQ)

Se cotiza como paquete (RFQ 2). Sus componentes son hijos con `INCLUIDO = Sí` (SUP-16-06); si el RFQ viene desglosado (DEC-16-03) se cambia ese campo y se costean uno por uno.

| Concepto | Cantidad en el BOQ | Unidad | Etiqueta |
|---|---|---|---|
| FR-PAN Paneles de cámaras | m² de cámaras de 12C (C1: 98 → 466 m² medio) | m² | ESCALABLE |
| FR-COMP Compresores / sala de máquinas | **PENDIENTE** (kWf total) | kWf | DUPLICABLE |
| FR-COND Condensación | **PENDIENTE** | kWf | DUPLICABLE |
| FR-EVAP Evaporadores | **PENDIENTE** | kWf | DUPLICABLE |
| FR-PIP Piping y aislación | 1 lote | lote | ESCALABLE |
| FR-REF Refrigerante / fluido secundario (NH₃, CO₂, glicol… sin elegir) | 1 lote | lote | ESCALABLE |
| FR-CTL Controles | 1 lote | lote | ESCALABLE |
| FR-AGH Agua helada / hielo (EQ-37) | kWf de reposición del chiller | kWf | ESCALABLE |
| FR-DCK Docks (EQ-65) | **PENDIENTE** (posiciones, D12-01) | unidad | DUPLICABLE |
| FR-TUN Túnel de congelado (solo si congelado propio) | t/día de congelación (C1: 0,6 → 4,8; C3-P2: 2,4 → 19,2) | t/día | DUPLICABLE |

La brecha de 09C entre el cálculo físico y el benchmark (×5,7) sigue abierta (T16-04): la cota inferior no debe usarse para dimensionar la sala de máquinas.

## 3. Agua y efluentes

| Concepto | Cantidad | Fuente de la cantidad |
|---|---|---|
| AG-CAP Captación (perforación) o conexión | agua captada m³/d | 09C; tipo según sitio |
| AG-ALM Almacenamiento (EQ-72) | 0,5 / 1 / 2 días de agua captada (C1-10.000: 125–500 m³) | SUP-16-15 |
| AG-TRA Tratamiento · AG-BOM Bombeo | caudal horario máximo ilustrativo | 09C (SUPUESTO) |
| AG-DIS Distribución interna | m² construidos | 12C |
| EF-PAQ Paquete de efluentes (RFQ 3) | m³/d descargados | 09C; tecnología abierta |
| EF-PRE Pretratamiento (EQ-70) · EF-DAF Fisicoquímico | m³/h máx. ilustrativo | 09C |
| EF-ECU Ecualización | m³/d (tiempo de retención PENDIENTE) | 09C |
| EF-BIO Biológico | kg DQO/d (no aplica si vuelco a colectora) | 09C |
| EF-LOD Lodos | **PENDIENTE** (DPV-114) | — |
| EF-INF Infraestructura asociada | 1 lote | — |

Obra civil de efluentes (OC-EF) en [`obra_civil_capex.md`](obra_civil_capex.md).

## 4. Electricidad, térmico, aire

| Concepto | Cantidad | Estado |
|---|---|---|
| EL-ACO Acometida MT | 1 lote | alcance según distribuidora (DPV-16-11) |
| EL-TRA Transformación | **PENDIENTE** kVA | demanda máxima PENDIENTE (DPV-095); cota: potencia media |
| EL-TAB Tableros | 1 lote | — |
| EL-DIS Distribución e iluminación | m² construidos | — |
| EL-UPS UPS y control | **PENDIENTE** kVA | — |
| EL-GEN Generación de respaldo (EQ-73) | **PENDIENTE** kVA | política abierta (DEC-047); cota: carga crítica ilustrativa |
| TE-GEN Caldera / agua caliente (EQ-14) | **PENDIENTE** kWt | pico PENDIENTE; cota: escaldado medio |
| TE-COM Combustible · TE-DIS Distribución | 1 lote c/u | fuente térmica abierta (DEC-045) |
| AC-COM Aire comprimido (EQ-71) | **PENDIENTE** m³/min | DPV-095 |

## 5. Servicios generales

| Concepto | Cantidad | Nota |
|---|---|---|
| IT-HW, IT-SW, IT-SEN (SCADA EQ-76), IT-RED | 1 lote c/u | Software comprado = CAPEX; suscripciones = OPEX |
| IT-ETQ Balanzas etiquetadoras (EQ-54) | **PENDIENTE** (puestos) | RFQ L7 |
| LAB-EQ Laboratorio (si propio, DEC-065) | 1 lote | — |
| SI-DET, SI-COM, SI-PRO Incendio | 1 lote c/u | **Requerimientos municipales y de bomberos PENDIENTES** (DPV-106): no se inventan |
| PER-EQ Vestuarios y comedor | 1 lote | dimensionar con pico simultáneo (SUP-141) |
| MOB-OF Mobiliario | 1 lote | — |

## 6. Qué falta

Lista de cargas por equipo (DPV-095) → demanda máxima, kVA, kWt pico, caudal de aire; balance frigorífico de proveedor (DPV-109); límites de vuelco y tecnología de efluentes (DPV-106, DEC-043); política de respaldo (DEC-047); precios de todos los conceptos (RFQ 2, 3 y 5 de [`plan_cotizaciones.md`](plan_cotizaciones.md)).
