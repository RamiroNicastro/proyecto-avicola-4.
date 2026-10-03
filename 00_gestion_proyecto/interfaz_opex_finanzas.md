# Interfaz OPEX + capital de trabajo → modelo financiero

**Fecha:** 2026-10-03 · **Origen:** reconciliación 16–17 ([`reconciliacion_sesiones_16_17.md`](reconciliacion_sesiones_16_17.md)) · **Emisor:** [`20_opex/modelo_opex.py`](../20_opex/modelo_opex.py) · **Receptor:** `21_modelo_financiero` (no construido)

> Define **qué entregará** OPEX al modelo financiero y cómo debe consumirse. Hoy **no existe OPEX total, costo por ave/kg ni capital de trabajo** para ninguna configuración, y **ninguna arquitectura es costeable** (SUP-164, SUP-185). No se calculan ingresos, EBITDA, VAN, TIR ni payback. Vacío = desconocido, nunca 0.

## 1. Principio: OPEX por período, no una cifra anual eterna

El financiero **no** debe tomar un OPEX anual fijo y repetirlo. Debe reconstruir el costo de cada período `t` desde el registro por concepto:

```
OPEX(t) = Σ_conceptos  costo_concepto_pleno × (PCT_VARIABLE × u(t) + PCT_FIJO)  × índice(t)
u(t)    = producción(t) ÷ producción plena de la configuración        (input; no 100 % automático)
```

- `costo_concepto_pleno` = `COSTO_CALCULADO_USD_ANIO` de [`registro_costos_operativos.csv`](../20_opex/registro_costos_operativos.csv) a escala plena (hoy casi todo PENDIENTE).
- `u(t)` sale de la cadena de §2 y del ramp-up (DEC-090); etapas arranque/estabilización **sin factor** hoy (SUP-181).
- `índice(t)` = actualización de precios (DEC-006; campos `INDICE_ACTUALIZACION` / `FECHA_ACTUALIZACION` preparados, vacíos).
- Semivariables sin `PCT_VARIABLE` declarado → el ajuste devuelve **PENDIENTE** (test R03); no se reparte 50/50.
- Ineficiencias del arranque (mortalidad, conversión, rendimiento, scrap, horas extra) no están modeladas.

## 2. Cadena demanda → flujo (obligatoria)

```
DEMANDA (validada por canal y producto)
  → UTILIZACIÓN u(t) (≤ capacidad; ramp-up)
    → PRODUCCIÓN (aves faenadas, kg por producto: balance de masa 04 y mix 06)
      → VENTAS (cantidades × precio por producto, canal y mercado)
        → OPEX VARIABLE (drivers × u)
          → CAPITAL DE TRABAJO (inventarios propios, CxC, CxP, caja)
            → FLUJO DE FONDOS
```

El financiero **no** debe asumir 100 % de utilización. Utilización y ramp-up son **inputs** (DEC-090, DPV-088). La capacidad física de los equipos no es capacidad comercial (la demanda A+B documentada es ≈ 0; DEC-001).

## 3. Campos que entrega OPEX

| Campo para finanzas | Fuente en OPEX | Estado hoy |
|---|---|---|
| **OPEX fijo** | `NATURALEZA = fijo` (`PCT_FIJO` = 100) | Estructura disponible; montos PENDIENTES |
| **OPEX variable** | `NATURALEZA = variable` (`PCT_VARIABLE` = 100) | Ídem |
| **Semifijo** | `NATURALEZA = semifijo` (escalón de capacidad: cuadrillas, turnos, estructura) | Ídem; escalones = 14A |
| **Semivariable** | `NATURALEZA = semivariable`, `PCT_VARIABLE` vacío | **PENDIENTE** (sin reparto declarado; SUP-180) |
| **Costo por centro** | `CENTRO_COSTO` (producción primaria, incubación, alimento, faena, frío, mantenimiento, calidad, logística, administración, comercial, servicios generales, terceros) | Estructura disponible |
| **Costo laboral** | `modelo_costo_laboral.csv`: FTE de 14A × costo empresa por FTE (SUP-182); horas tercerizadas × tarifa | **PENDIENTE**: sin salarios (DPV-148, DPV-146); headcount PENDIENTE; FTE upstream no dimensionados (DPV-176) |
| **Servicios** (utilities, efluentes, façon, flete, seguros, calidad, administración) | módulos UTILITIES, EFLUENTES, FAENA, LOGISTICA, SEGUROS, CALIDAD, ADMINISTRACION | **PENDIENTE** (DPV-052, 053, 006, 134, 171–174) |
| **Inventarios** | `capital_trabajo_opex.csv`, `COMPONENTE = INVENTARIO`, con `PROPIEDAD_EMPRESA` y `ENTRA_EN_CT` | Cantidades físicas disponibles; valores PENDIENTES (solo maíz valorizado, E4, no es CT) |
| **Cuentas por pagar** | `COMPONENTE = CUENTAS_POR_PAGAR` por `GRUPO_PROVEEDOR` (alimento, pollitos, granos, servicios, packaging, logística, energía) | **PENDIENTE**: compras sin precio; días de pago sin dato (DPV-175) |
| **Días** (cobro, pago, stock, caja) | inputs `dias_cobro`, `dias_pago`, `dias_stock_*`, `dias_caja_operativa` | **Vacíos** (DPV-175, DEC-091) |
| **Ramp-up** | `rampup()`, `ETAPAS_RAMPUP` | Estructura; factores PENDIENTES (DEC-090) |
| **Propiedad del stock** | `PROPIETARIO`, `PROPIEDAD_EMPRESA`, `UBICACION` | Disponible por arquitectura; façon sin variante → `PROPIEDAD_PENDIENTE` |
| Aportante | `APORTANTE` (EMPRESA / PRODUCTOR_INTEGRADO / TERCERO / PENDIENTE) | Solo EMPRESA es costo de la empresa; PENDIENTE cuenta como faltante |
| Comparabilidad | `COMPARABILIDAD = MONTOS_PARCIALES_E4_NO_COMPARABLES` | Los montos parciales **no** sirven para comparar arquitecturas |

## 4. Precio observado vs conversión

Cada precio conserva la observación (`PRECIO_ORIGINAL_OBSERVADO`, `MONEDA_ORIGINAL`, `FECHA_PRECIO`, `CONDICION_ENTREGA`, `IVA_PRECIO`) separada de su conversión (`TC_USADO`, `FECHA_TC`, `ORIGEN_PRECIO_USD = CONVERSION_MODELO`) (SUP-187). Verificado en la base:

| Concepto | Observación | Conversión | Evidencia |
|---|---|---|---|
| Pollito BB (POL-COMPRA) | ARS 1.312,22 / unidad sin IVA, semana 2026-07-06 (FTE-029) | TC A3500 2026-07-06 (FTE-319) | E4 `[PVDP]`; anterior a la fecha base; entrega y vacunas desconocidas |
| Maíz (ALI-MP-MAIZ) | ARS 295.800 / t, pizarra Rosario **sobre puerto**, 2026-09-29 (FTE-317) | TC mayorista 2026-09-29 (FTE-318) | E4 `[PVDP]`; **precio Rosario ≠ costo puesto en planta** (diferencial ALI-MP-DIF-MAIZ y flete LOG-GRA-* PENDIENTES) |

Ninguna conversión eleva la evidencia.

## 5. Mantenimiento, importación y preoperativos

- OPEX contiene mantenimiento, repuestos, contratos y horas técnicas; **no** la reposición completa del activo (CAPEX de reposición en el financiero; [`interfaz_capex_finanzas.md`](interfaz_capex_finanzas.md) §4).
- OPEX no recarga el arancel de la compra inicial; solo costos recurrentes (repuestos, servicios, insumos importados) dentro de sus conceptos.
- Preoperativos: `NO_APLICA_EN_OPERACION_NORMAL` en OPEX (viven en CAPEX PRE-*; [`interfaz_capex_finanzas.md`](interfaz_capex_finanzas.md) §5).

## 6. Capital de trabajo (reconciliación formal)

```
CAPITAL_TRABAJO_OPERATIVO = INVENTARIOS_PROPIOS + CUENTAS_POR_COBRAR + CAJA_OPERATIVA − CUENTAS_POR_PAGAR
INVENTARIOS_PROPIOS       = Σ inventario × valuación   solo si PROPIEDAD_EMPRESA = TRUE
CUENTAS_POR_COBRAR        = ventas × días de cobro ÷ 365          (por canal)
CUENTAS_POR_PAGAR         = compras × días de pago ÷ 365          (por grupo de proveedor)
CAJA_OPERATIVA            = según la política elegida (DEC-091); sin política = NO_ASIGNADA
CAPITAL_TRABAJO_TOTAL     = PENDIENTE   (hasta tener precios, ventas y plazos)
```

| Regla | Estado verificado |
|---|---|
| Inventario de terceros (alimento en la fábrica proveedora, MP del elaborador en façon B2) **no** entra | `ENTRA_EN_CT` falso en esas filas (§14 de la reconciliación) |
| Propiedad PENDIENTE (façon sin variante) **no** entra | Se informa `PROPIEDAD_PENDIENTE` |
| Integrar cambia **propiedad, ubicación y CT**, no el requerimiento físico de la cadena | SUP-154 |
| El **maíz valorizado** (USD 15.445–123.561, E4 a precio Rosario) **no** es proxy del CT total | Único ítem valorizado; rotulado como parcial |
| CAPITAL_TRABAJO = PENDIENTE en los 29 escenarios | Verificado |
| Sueldos y cargas devengados | Fuera por ahora; se modelarán con el cronograma de pagos del financiero |

Valuación de inventarios: DEC-089 (activo biológico, producto terminado, alimento propio, WIP de huevo — cota inferior, SUP-184).

## 7. Frontera fiscal

OPEX actual = costos **antes de tratamiento fiscal definitivo**. El financiero tratará IVA (débito y crédito), impuesto a las ganancias, ingresos brutos, tasas municipales, derechos de exportación, percepciones y regímenes de beneficios (DPV-043, DPV-169, DPV-015). No se calculan ahora.

## 8. Categorías de ingreso preparadas (sin precio)

El financiero deberá consumir **cantidades** del balance de masa (`04_balance_masa`) y del mix comercial (`06_productos`, `07_subproductos`) por configuración de producto, y asignar a cada parte el mercado que mejor la paga (principio de ingreso total por ave, SUP-013). **No se carga ningún precio.**

| Categoría de ingreso | Cantidad desde | Precio (futuro) |
|---|---|---|
| Pollo entero | 04 / 06 (configuración A/B/C) | DPV-013, DPV-039 |
| Cortes (pechuga, suprema, pata-muslo, alas, otros) | 04 (trozado y deshuese) | DPV-013, DPV-070 |
| Menudencias (hígado, corazón, molleja, cuello) | 04 | DPV-070 |
| Patas / garras | 04 | DPV-064, DPV-077 |
| Coproductos (CMS, recortes, piel, carcasa) | 04 / 07 | DPV-071, DPV-075 |
| Subproductos no comestibles (venta o costo de retiro) | 04 / 07 | DPV-072, DPV-076, DPV-080 — nunca neteados contra costos (test C02 / M07 de OPEX) |
| Rendering (solo si se activa, FUTURO) | 07 | DPV-065, DPV-076 |
| Servicios / otros (p. ej. façon a terceros, fletes de retorno) | — | Sin escenario; backhaul = 0 (SUP-103) |
| Exportación (separada por mercado y categoría A–D) | 0 en la base (SUP-022) | DPV-024, DPV-026, DPV-030 — halal = módulo futuro de mercado |

Deducciones comerciales del canal (descuentos, fees, rebates) se tratarán como deducción o gasto comercial en el financiero (DPV-039), no en OPEX.

## 9. Qué falta para que OPEX entregue un total

Alimento (DPV-050), granos (DPV-157), pollito y huevo (DPV-047, DPV-154), integración (DPV-170, DEC-086), salarios y normativa laboral (DPV-146, DPV-148), utilities (DPV-052, DPV-053), façon y frío de terceros (DPV-006, DPV-171), consumibles (DPV-172), mantenimiento (DPV-150, DEC-088), seguros (DPV-173), calidad (DPV-174), logística (DPV-134, DEC-087), parámetros de CT (DPV-175, DEC-091), dotaciones y consumos upstream (DPV-176, DPV-177); umbral de publicación (DEC-084).
