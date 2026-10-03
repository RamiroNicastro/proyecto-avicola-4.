# Interfaz CAPEX → modelo financiero

**Fecha:** 2026-10-03 · **Origen:** reconciliación 16–17 ([`reconciliacion_sesiones_16_17.md`](reconciliacion_sesiones_16_17.md)) · **Emisor:** [`19_capex/modelo_capex.py`](../19_capex/modelo_capex.py) · **Receptor:** `21_modelo_financiero` (no construido)

> Define **qué entregará** CAPEX al modelo financiero integral y en qué estado está cada campo hoy. **No** calcula depreciaciones, impuestos, VAN, TIR ni payback, y **no** publica ningún total: hoy **no existe CAPEX total confiable** para ninguna configuración (SUP-164). Vacío = desconocido, nunca 0.

## 1. Principios del contrato

1. **CAPEX ≠ capital de trabajo.** El BOQ no contiene alimento, pollitos, inventarios ni cuentas por cobrar (test P05 de CAPEX). El capital de trabajo lo entrega OPEX ([`interfaz_opex_finanzas.md`](interfaz_opex_finanzas.md) §6).
2. **Fondos iniciales (conceptual, no calculado):**
   ```
   FONDOS_INICIALES = CAPEX_INICIAL (directo + indirecto + preoperativo + contingencia + terreno)
                    + CAPITAL_TRABAJO_INICIAL (de OPEX)
                    + otros requerimientos financieros pertinentes (costos de financiamiento durante la obra,
                      IVA de la inversión a financiar hasta su recupero, garantías, reservas que exija el fondeo)
   ```
   Ningún término está disponible; el modelo financiero **no** debe completar faltantes con cero ni con porcentajes no documentados. USD 2 M no es límite ni referencia de suficiencia (SUP-003, DEC-010).
3. **Unidad y fecha:** USD a la fecha base 2026-10-01 (SUP-155); sin indexación automática (DEC-006). Precios en ARS solo con TC, tipo y fecha.
4. **Evidencia separada:** todo monto viaja con su nivel (`CAPEX_E1_E2_USD`, `CAPEX_E3_USD`, `CAPEX_E4_USD`, `CAPEX_E5_USD`) y `CALIDAD_MONTO`. Un monto E4 no se suma con uno E2 como si fueran equivalentes; montos `MONTO_CON_REFERENCIAS_DEBILES_E4` **no son comparables** entre arquitecturas.
5. **Misma arquitectura en CAPEX y OPEX:** la configuración se identifica por el preset de [`mapa_arquitecturas_economicas.csv`](mapa_arquitecturas_economicas.csv) (C0–CF + variantes). El financiero consume ambos módulos **con el mismo nombre de configuración y escala**.

## 2. Campos que entrega CAPEX

| # | Campo para finanzas | Fuente en CAPEX | Granularidad | Estado hoy |
|---|---|---|---|---|
| 1 | **CAPEX directo** | `boq_capex.csv`: `CATEGORIA_CAPEX = DIRECTO`, `COSTO_INSTALADO_USD` (low / medio / high) | activo × escenario | **PENDIENTE**: 1–2 conceptos con precio E4 por configuración |
| 2 | **CAPEX indirecto** (ingeniería, arquitectura, proyecto ejecutivo, dirección de obra, PM, permisos, estudios) | `CATEGORIA_CAPEX = INDIRECTO` (IND-*) | concepto | **PENDIENTE**: % no adoptados (SUP-161, DPV-164, DEC-083) |
| 3 | **Preoperativos** (commissioning, puesta en marcha, pruebas FAT/SAT, capacitación inicial, repuestos iniciales, herramientas iniciales, insumos iniciales de laboratorio, IT inicial) | `CATEGORIA_CAPEX = PREOPERATIVO` (PRE-*) | concepto | **PENDIENTE** (DPV-163). Viven **solo** en CAPEX; OPEX los marca `NO_APLICA_EN_OPERACION_NORMAL` (§5) |
| 4 | **Contingencia** (diseño/cantidades, costo, escalación) | `CATEGORIA_CAPEX = CONTINGENCIA` (CON-DIS, CON-COS, CON-ESC) | concepto | **PENDIENTE** (DPV-165, DEC-083) |
| 5 | **Terreno** | bloque TERRENO; `criterio_terreno` | lote | **PROVISIONAL**: terreno conceptual ≠ terreno adquirido; sin criterio elegido (DEC-063, SUP-175); sin precio (DPV-087) |
| 6 | **Inversión por fase** | `FASE` (`INICIAL` / `FUTURO`); `expansion_capex.csv` (`ETAPA`, `ACCION`, `DELTA_A_ADQUIRIR`, `COSTO_ETAPA_USD`) | activo × etapa de trayectoria | **Estructura disponible**; costos PENDIENTES; prima de ampliación PENDIENTE (DPV-086) |
| 7 | **Inversión acumulada** | Σ por etapa de `expansion_capex.csv` | trayectoria | **PENDIENTE**. Un acumulado igual entre trayectorias es artefacto del precio lineal (no usar) |
| 8 | **Inversiones futuras** (reproductoras, rendering, halal, exportación) | `FASE = FUTURO` (informativo, no suma); halal sin bloque | concepto | **Estructura parcial**: reproductoras y rendering estructurados; **halal sin conceptos de CAPEX** (módulo futuro de mercado, §6) |
| 9 | **Reposiciones (CAPEX de reposición)** | `VIDA_UTIL_ANIOS`, `REEMPLAZO_ANIO`, `COSTO_REEMPLAZO` | activo | **Campos vacíos** (DPV-167). Los reemplazos mayores van al financiero como CAPEX de reposición, **no** al OPEX ordinario (§4) |
| 10 | **Vida útil** | `VIDA_UTIL_ANIOS` | activo / clase | **Vacío** (DPV-167). La amortización impositiva es otro dato (DPV-169) |
| 11 | **Valor residual futuro** | `VALOR_RESIDUAL` | activo | **Vacío** (DPV-167) |
| 12 | **Fecha / desembolso** | no existe aún: requiere cronograma de obra, anticipos y plazos de entrega | concepto × período | **PENDIENTE**: campo a crear en el financiero; plazos de entrega en DPV-167 y DPV-086 |
| 13 | Activos de terceros | `TITULAR = PRODUCTOR_INTEGRADO` | activo | Informativo: **no** es inversión de la empresa |
| 14 | Calidad y cobertura | `escenarios_capex.csv`: `CONCEPTOS_*`, `COBERTURA_CONCEPTOS_PCT`, `COBERTURA_VALOR`, `TOTAL_PRELIMINAR`, `ALERTAS` | escenario × bloque | Disponible; hoy `TOTAL_PRELIMINAR = NO DISPONIBLE` en los 33 escenarios |

**No se calculan depreciaciones** en esta etapa: el financiero las calculará con vida útil contable/impositiva cuando exista evidencia (DPV-167, DPV-169).

## 3. Importación: capas que se conservan en CAPEX

El precio de un equipo importado se lleva por capas, **solo en CAPEX**: EXW / FOB → CIF (flete y seguro) → **landed** (gastos portuarios, despachante, derechos y tasas, flete puerto → sitio) → **instalado** (montaje, supervisión, puesta en marcha). Columnas `COSTO_EQUIPO_USD`, `COSTO_LANDED_USD`, `COSTO_INSTALADO_USD` del BOQ y tabla externa `capas_importacion_capex.csv` (hoy vacía). Datos: DPV-162 (logística de importación), DPV-093 (régimen y aranceles, bienes nuevos y usados), DPV-163 (alcance de instalación).

**El arancel de la compra inicial no vuelve a cargarse como OPEX anual.** OPEX solo conserva costos recurrentes asociados a importación (repuestos, servicios técnicos del proveedor, insumos importados) dentro de sus conceptos de mantenimiento y consumibles; hoy no tiene ningún concepto de importación (0 coincidencias en `base_costos_opex.csv`).

## 4. Mantenimiento y reposición

| Concepto | Vive en | Nota |
|---|---|---|
| Activo (equipo, obra, instalación) | CAPEX | BOQ |
| Mantenimiento preventivo/correctivo, repuestos, lubricantes, servicios técnicos, contratos | OPEX (MAN-*) | Método único por corrida (SUP-178, DEC-088) |
| Mano de obra de mantenimiento | OPEX (costo laboral, 14A) | No se duplica en MAN-* |
| Reemplazo completo de un activo | **Financiero: CAPEX de reposición** | Requiere `REEMPLAZO_ANIO` y `COSTO_REEMPLAZO` (DPV-167) |
| Mantenimiento como % CAPEX | OPEX, solo benchmark | Base = CAPEX con precio del área; sin base → `BASE_SIN_PRECIO` |

## 5. Preoperativos sin doble conteo (verificado)

| Concepto | CAPEX | OPEX | Resultado |
|---|---|---|---|
| Commissioning | PRE-COM | — | Solo CAPEX |
| Puesta en marcha / pruebas | PRE-PEM, PRE-PRU | — | Solo CAPEX |
| Ingeniería | IND-ING (indirecto) | — | Solo CAPEX |
| Herramientas iniciales | PRE-HER | FAE-CUCH = reposición **recurrente** de cuchillería por FTE | Distintos: inicial vs recurrente |
| Capacitación inicial | PRE-CAP | LAB-*-CAP = capacitación **recurrente** del costo empresa por FTE | Distintos: inicial vs recurrente |
| Repuestos iniciales | PRE-REP | MAN-*-REP = consumo recurrente de repuestos | Distintos: stock inicial vs consumo |
| Insumos iniciales de laboratorio / IT inicial | PRE-LAB, PRE-IT | CAL-ANA-*, ADM-SIS = recurrentes | Distintos |

En OPEX, los preoperativos se tratan como **NO_APLICA_EN_OPERACION_NORMAL**: `estructura_opex.md` §6 los asigna a CAPEX, `ramp_up.md` §3 los excluye y `metodologia_opex.md` §4 (test S06) prohíbe usar IDs de la base CAPEX. Ningún ID PRE-* aparece en el registro OPEX (verificado en §14 de la reconciliación).

## 6. Halal y exportación (módulo futuro de mercado)

CAPEX **puede** incorporar la inversión específica futura (segregación, salas, aturdido, equipos de etiquetado; DPV-145) como conceptos nuevos de la base con `FASE = FUTURO` u opcional, sin tocar el código de costeo; hoy **no** hay conceptos halal en CAPEX ni importes. No se desarrolla el proceso halal.

## 7. Frontera fiscal

| CAPEX actual | Modelo financiero futuro |
|---|---|
| Costos **antes de tratamiento fiscal definitivo**: IVA `pendiente` incluido con alerta IVA_INCIERTO; `con_iva` sin alícuota fuera del costo económico (SUP-166); aranceles como capa landed PENDIENTE | IVA de la inversión (crédito fiscal, recupero, efecto financiero), impuesto a las ganancias, depreciaciones contables e impositivas, derechos y tasas de importación, tasas municipales, beneficios o regímenes de promoción |

Datos: DPV-169 (tratamiento fiscal de la inversión y la operación), DPV-093 (importación), DPV-043 (impuestos sobre ventas). **No se calcula ninguno en esta sesión.**

## 8. Qué falta para que CAPEX entregue un total

Precios de paquetes (DPV-160), USD/m² de obra (DPV-161), terreno y conexiones (DPV-087), importación (DPV-162, DPV-093), alcance de instalación (DPV-163), indirectos (DPV-164), contingencia (DPV-165), galpones (DPV-051), vehículos (DPV-168), vidas útiles (DPV-167); criterio de terreno (DEC-063), criterio de contingencia (DEC-083) y umbral de publicación (DEC-084).
