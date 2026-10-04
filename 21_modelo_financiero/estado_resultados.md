# Estado de resultados — OPEX, EBITDA, depreciación, EBIT e impuestos

**Fecha:** 2026-10-04 · Salida: [`estado_resultados.csv`](estado_resultados.csv) · Interfaz consumida: [`../00_gestion_proyecto/interfaz_opex_finanzas.md`](../00_gestion_proyecto/interfaz_opex_finanzas.md)

## 1. Estructura

```
  VENTA BRUTA (por categoría de ingreso)
− descuentos − bonificaciones − devoluciones − comisiones − derechos de exportación
= INGRESO NETO
− OPEX variable − OPEX fijo − OPEX semifijo − OPEX semivariable        (rubros de 20_opex)
− costos extra del ramp-up
− costos logísticos del canal − costos de exportación                   (comerciales, adicionales al OPEX de 20)
− impuestos sobre ingresos (IIBB + tasas municipales, % de la venta bruta) − otros impuestos fijos
= EBITDA                                                                 (sin depreciación, intereses, CAPEX ni CT)
− depreciación contable
= EBIT
− intereses y comisiones de deuda (solo en la vista con deuda)
= resultado antes de impuesto → impuesto a las ganancias (operativo / con deuda)
```

Identidades con test: ingreso neto (I01), EBITDA (I02), EBIT (I03). EBITDA **no** es caja: la caja está en [`flujo_caja.md`](flujo_caja.md).

## 2. OPEX: consumo del motor de la sesión 17 (no se reconstruye)

El OPEX llega como **rubros** = filas del registro de [`20_opex`](../20_opex/modelo_opex.py) (`COSTO_CALCULADO_USD_ANIO` a escala plena, `NATURALEZA`, `PCT_VARIABLE`, `GRUPO_PROVEEDOR`) por etapa. El financiero solo los distribuye en el tiempo, como pide la interfaz §1:

```
OPEX(mes) = Σ rubros  costo_pleno ÷ 12 × [ PCT_VARIABLE × u_efectiva ÷ eficiencia + (1 − PCT_VARIABLE) ] × índice × stress
```

| Naturaleza | PCT_VARIABLE | Comportamiento |
|---|---|---|
| variable | 100 % | × utilización |
| fijo | 0 % | constante desde el inicio de la operación |
| semifijo | 0 % | constante dentro de la etapa; salta al entrar una expansión (escalón) |
| semivariable | declarado | sin % → PENDIENTE (no se reparte 50/50) |

- **Solo** se usan rubros si OPEX publica `TOTAL_PRELIMINAR_USD_ANIO` y la arquitectura es costeable con evidencia E1–E3. Hoy ninguna lo es: el monto E4 parcial (p. ej. maíz Rosario) queda **solo en la traza**, nunca como costo total (tests E06, E12).
- Antes del inicio de operación OPEX = 0: los preoperativos están en CAPEX (PRE-*; interfaz CAPEX §5).
- En modo escenario el usuario puede cargar rubros propios (JSON) con las mismas claves.

## 3. Depreciación (contable, no fiscal)

Por activo o clase: `capex_usd`, `vida_util_anios`, `valor_residual_usd`, `costo_reemplazo_usd`, `depreciable` (SUP-19-18):

- Método **lineal** desde la entrada en operación de la etapa; terreno no depreciable.
- Al terminar la vida útil, si hay `costo_reemplazo_usd`, se registra **CAPEX de reposición** (flujo) y se deprecia de nuevo (test N17). La depreciación es contable: **no** es caja ni CAPEX de reposición.
- Vida fiscal ≠ vida contable: la amortización impositiva definitiva requiere DPV-169; hoy el impuesto usa la depreciación contable como aproximación declarada (DPV-19-08).
- Hoy los campos `VIDA_UTIL_ANIOS / VALOR_RESIDUAL` del BOQ están vacíos en el 100 % de los activos (DPV-167): **EBIT no calculable**.

## 4. Módulo de impuestos (separado; sin tasas hardcodeadas)

| Impuesto | Tratamiento | Input (hoy) |
|---|---|---|
| Ingresos brutos y tasas municipales | % de la venta bruta; antes del EBITDA | `impuestos.pct_iibb`, `impuestos.pct_tasas_municipales` — PENDIENTES (DPV-043) |
| Otros impuestos operativos | USD/año, antes del EBITDA | `impuestos.otros_impuestos_usd_anio` — PENDIENTE |
| Ganancias | Anual, al cierre de cada año del proyecto, sobre EBIT (vista proyecto) o EBIT − intereses − comisiones (vista accionista); quebrantos con vencimiento en `anios_quebranto`; sin anticipos (SUP-19-13); test N16 | `impuestos.tasa_ganancias`, `impuestos.anios_quebranto` — PENDIENTES (DPV-169) |
| IVA | Módulo aparte, fuera del resultado ([`flujo_caja.md`](flujo_caja.md) §4) | `iva.*` — PENDIENTES |
| Derechos de exportación | Deducción de la venta de exportación | `canales.exportacion.pct_derechos_exportacion` — PENDIENTE (DPV-015) |

El modelo corre **PRE-TAX** (sin ganancias) y **AFTER-TAX**. `BASE_FLUJO` indica cuál se usó para los indicadores. After-tax queda NO PUBLICABLE si faltan tasas o reglas (`PUBLICABLE_FLUJO_AFTER_TAX`).
