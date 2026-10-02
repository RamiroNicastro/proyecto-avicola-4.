# Costos de faena, empaque y subproductos

**Fecha:** 2026-10-02 · Implementación: §FAENA, §EMPAQUE y §SUBPRODUCTOS de `generar_registro()` en [`modelo_opex.py`](modelo_opex.py)

## 1. Faena a façon (`faena = facon`, C0)

| Concepto | ID | Driver | Estado |
|---|---|---|---|
| Servicio de faena | FAE-FACON | aves faenadas/año (625.000 / 1.250.000 / 2.500.000 / 5.000.000) | Tarifa **no asumida** (DPV-006) |
| Frío en el faenador | FAE-FACON-FRIO | t·mes | Alcance PENDIENTE |
| Subproductos en façon | FAE-FACON-SUB | t | Alcance PENDIENTE (DPV-17-07); un crédito sería ingreso, no se netea |
| Empaque | EMP-* | kg de producto | Aportante PENDIENTE (`facon_aporta_empaque`) |
| Personal del faenador | 14A (horas tercerizadas) | horas | **RECURSO FÍSICO DE TERCERO** (`APORTANTE = TERCERO`): horas visibles para trazabilidad, costo `INCLUIDO_EN_TARIFA_FACON` (tests A04b, X11; mutación M11) |
| Control de calidad propio en el faenador | 14A `control_calidad_facon` | FTE | Costo laboral de la empresa |
| Congelado en tercero | UT-FRIO-TER | t congeladas/año (12B) | Sin precio |

Test A04: façon no carga utilities, efluentes, químicos de planta, subproductos ni mantenimiento de planta.

## 2. Planta propia (C1–C3, CF)

| Rubro | Dónde se costea |
|---|---|
| RRHH | Costo laboral (14A): [`costos_rrhh.md`](costos_rrhh.md) |
| Agua, energía, térmico, frío | Utilities (09C): [`costos_utilities.md`](costos_utilities.md) |
| Limpieza: químicos | FAE-QUIM (por ave faenada) |
| Limpieza: elementos | FAE-ELEM (año, semifijo) |
| Limpieza: agua y calor | **INCLUIDO** en utilities (fila informativa con 12.500 m³/año a 10.000; test C07, mutación M08) |
| Limpieza tercerizada | Horas contratadas de 14A × tarifa (LAB-TER-LIMP); el costo interno de la cuadrilla desaparece y la función se conserva (test C08) |
| Cuchillería y herramientas | FAE-CUCH por FTE directo de 14A (47 FTE a 10.000) |
| Servicios de planta | FAE-SERV (mes) |
| Mantenimiento | [`costos_mantenimiento.md`](costos_mantenimiento.md) |
| Calidad | [`costos_calidad.md`](costos_calidad.md) |
| Descarte y decomisos | Subproductos §4 |
| Empaque | §3 |

## 3. Empaque

Estructura por kg de producto comercial (05: comestible a empaque, incluye garras y menudencias según 12B): bolsas, bandejas, film, cajas, etiquetas, separadores, pallets, flejes, otros. Cantidad: 1.498 / 2.996 / 5.991 / 11.982 t de producto/año (configuración B). El **coeficiente de cada material por kg depende del mix y del formato** (bandeja vs caja máster, entero vs trozado): no hay mix definitivo, por eso el precio se pide "por kg de producto" por material y queda PENDIENTE (DPV-17-09). Cambiar `config_producto` (A/B/C) cambia los kg por ave (05).

## 4. Subproductos (costos, no ingresos)

| Corriente | ID | t/año a 10.000 aves/día | Fuente |
|---|---|---|---|
| Sangre recuperada | SUB-RET-SANGRE | 210 | 09C (segregable) |
| Plumas húmedas | SUB-RET-PLUMAS | 603 | 09C |
| Vísceras no comestibles | SUB-RET-VISCERAS | 326 | 09C |
| Cabezas | SUB-RET-CABEZAS | 181 | 09C |
| Decomisos | SUB-RET-DECOMISOS | 100 | 04 (filas `decomiso*`) |

Más contenedores (SUB-CONT), transporte (LOG-SUB-*, criterio másico = cota inferior), frío (incluido en kWh si aplica; 12B: retiro diario sin stock refrigerado), clasificación (personal de subproductos de 14A) y, si `subproductos = B_basico_propio`, insumos y energía del tratamiento (SUB-TRAT-B, PENDIENTE_CANTIDAD; operación sin FTE en 14A). Rendering propio: SUB-REN-* con `FASE = FUTURO`.

**No se netean ingresos**: si un receptor paga por la sangre o las plumas, ese ingreso va al modelo financiero; el precio de retiro en la base nunca es negativo (test C02, mutación M07).

## 5. Rendering (CF, FUTURO) — estructura completa sin costos

SUB-REN-ENE (electricidad), SUB-REN-TER (térmico), SUB-REN-AGUA, SUB-REN-MAN (mantenimiento), SUB-REN-INS (químicos/insumos), SUB-REN-TRAT (gases, olores y efluentes), SUB-REN-RES (residuos), SUB-REN-LOG (harinas y grasas) y RRHH (`RRHH_RENDERING_FUTURO`): todos `FASE = FUTURO`, PENDIENTES, sin cantidades de 09C (test X14). El tratamiento básico propio (B) tiene RRHH, energía (SUB-TRAT-ENE, v1.1) e insumos.
