# Costos de producción primaria — granja integrada vs propia

**Fecha:** 2026-10-02 · Drivers: 03 vía 14B · Implementación: `Registro.split()` y §PRODUCCIÓN PRIMARIA en [`modelo_opex.py`](modelo_opex.py)

> **No se asume un contrato de integración.** El motor usa el esquema descripto en 03 ([`modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md)) solo para decir **quién aporta** cada concepto en una granja integrada (SUP-17-04), es editable (`aportes_integracion`) y lo que 03 deja "según contrato" queda **PENDIENTE**.

## 1. Quién aporta qué (granja integrada)

| Concepto | Aportante por defecto | Efecto en el registro |
|---|---|---|
| Pollito, alimento, sanidad, asistencia técnica, logística de insumos | EMPRESA (03) | Costo de la empresa |
| Mano de obra, electricidad, agua de la granja | PRODUCTOR_INTEGRADO (03) | Fila **INFORMATIVA** (no es costo de la empresa; test A05) |
| Gas de calefacción, cama, captura, retiro de mortalidad, limpieza de galpones, bioseguridad | PENDIENTE (según contrato) | Cuenta como faltante (`APORTANTE_PENDIENTE`) |
| Pago al integrado | — | Base del contrato **no definida** (por ave o por kg vivo): SIN_CANTIDAD (DEC-17-04). Variante `C1-10000-PAGO-KG-VIVO` |

## 2. Conceptos y drivers

| Concepto | ID | Driver (03/14B) | 10.000 aves/día |
|---|---|---|---|
| Vacunas y medicamentos | PP-SAN | pollitos alojados/año | 2.639.497 |
| Captura y carga | PP-CAPT | aves cargadas/año | 2.507.523 |
| Retiro de mortalidad | PP-MORT | aves muertas en granja/año | 131.975 |
| Limpieza de galpones | PP-LIMP | m² × ciclos/año | 216.670 m²·ciclo |
| Bioseguridad | PP-BIO | m² de galpón | 37.943 m² |
| Agua de bebida | PP-AGUA | m³/año (03) | 22.252 m³ |
| Pago al integrado (por ave / por kg) | PP-PAGO-AVE / PP-PAGO-KG | aves cargadas / kg vivo cargado × fracción integrada | — |
| Cama | PP-CAMA | — (kg/m² PENDIENTE en 12B) | SIN_CANTIDAD |
| Gas / calefacción, electricidad de granja | PP-GAS, PP-ENE | — (DPV-052) | SIN_CANTIDAD |
| Asistencia técnica externa | PP-ATE | — | SIN_CANTIDAD: el veterinario y los técnicos de campo ya están en 14A (no se duplica) |
| Otros (granja propia) | PP-OTR | — | SIN_CANTIDAD |

## 3. Granja propia (C3, CF; 25 % en C2)

Además de lo anterior, la empresa carga: energía y gas (SIN_CANTIDAD, DPV-052), agua, limpieza, bioseguridad, retiro de mortalidad, captura, **personal de granja** (14A no lo dimensiona → FTE PENDIENTE, no 0), seguro de granjas (SEG-GRA) y mantenimiento (MAN-GRA-*). En configuraciones mixtas las cantidades se reparten por `fraccion_granjas_propias` (CAPEX): la parte propia es costo de la empresa y la integrada sigue el cuadro §1.

## 4. Capital de trabajo

Las aves en crianza (≈ 331.000 aves en inventario medio a 10.000 aves/día, 03) son **activo biológico de la empresa** cuando la empresa aporta el pollito (integración) o la granja es propia. Su valuación (costo acumulado medio: pollito + alimento consumido + sanidad) queda **PENDIENTE** (DEC-17-07): ver [`capital_trabajo.md`](capital_trabajo.md).
