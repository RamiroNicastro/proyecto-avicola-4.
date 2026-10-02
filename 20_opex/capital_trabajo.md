# Capital de trabajo operativo

**Fecha:** 2026-10-02 · Implementación: `capital_trabajo()`, `cto()`, `cuentas_por_cobrar()`, `cuentas_por_pagar()` en [`modelo_opex.py`](modelo_opex.py) · Salida: [`capital_trabajo_opex.csv`](capital_trabajo_opex.csv)

```
CTO = inventarios PROPIOS + cuentas por cobrar + caja operativa − cuentas por pagar
cuentas por cobrar = ventas anuales × días de cobro ÷ 365
cuentas por pagar  = Σ por grupo de proveedor (compras anuales con precio × días de pago ÷ 365)
caja operativa     = OPEX total × días de buffer ÷ 365  (OPCIONAL: sin input = no se asigna)
```

**Resultado: `CAPITAL_TRABAJO = PENDIENTE` en los 29 escenarios.** El motor no fabrica un total: cada fila dice qué falta (test K05).

## 1. Stock físico ≠ stock propiedad de la empresa (corrección de 14B)

Solo entra al capital de trabajo el inventario con `PROPIEDAD_EMPRESA = TRUE`. El stock en manos de terceros entra solo si contractualmente es de la empresa; la arquitectura (planta de alimento, incubación o granjas propias) **no** hace que un inventario de tercero pase al balance propio, y una propiedad PENDIENTE no entra (tests K01–K03, K08, X12; mutación M04).

| Inventario | Propietario | Entra |
|---|---|---|
| Alimento en silos de granja (compra, integración) | Empresa (aporta el alimento) | Sí |
| Alimento y MP en la fábrica proveedora (compra) | Tercero | **No** (se informa como referencia) |
| MP y alimento en el elaborador, façon B1 (MP de la empresa) | Empresa (ubicación: tercero) | Sí |
| MP en el elaborador, façon B2 (MP del elaborador) | Tercero | **No** |
| Façon sin variante definida | PENDIENTE | PROPIEDAD_PENDIENTE (no se asume) |
| Granos, MP y alimento en planta propia | Empresa | Sí |
| Huevo fértil en almacén (5 d) y en incubación (WIP) | Empresa | Sí (WIP valuado al costo del huevo como cota inferior) |
| Pollitos BB | Empresa | Stock ≈ 0 (se alojan al llegar) |
| Aves en crianza (activo biológico) | Empresa si aporta el pollito o la granja es propia | Sí; valuación PENDIENTE (DEC-17-07) |
| Producto terminado refrigerado y congelado (stock medio de ciclo de despacho, 12B) | Empresa (también en façon, en el frío del faenador) | Sí; costo por kg PENDIENTE |
| Subproductos | Empresa | Stock 0 (retiro diario, 12B E1) |
| Envases, repuestos, insumos | Empresa | Días de stock PENDIENTES |

## 2. Magnitudes físicas (escenario medio)

| Ítem | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Alimento en silos de granja (t, 3 d) | 26 | 53 | 106 | 212 |
| Maíz propio (t, 15 d; C3 y façon B1) | 79 | 159 | 318 | 636 |
| …valorizado con el maíz E4 a precio Rosario (USD; **no** puesto en planta) | 15.445 | 30.890 | 61.780 | 123.561 |
| Aves en crianza (inventario medio) | 82.846 | 165.692 | 331.383 | 662.767 |
| Producto refrigerado, stock medio (t; C1) | 6,4 | 12,8 | 25,7 | 51,4 |
| Producto congelado, stock medio (t; C1) | 1,8 | 3,5 | 7,0 | 14,0 |

El único ítem valorizado es el **maíz propio**, con un precio **E4** sobre puerto: es un monto parcial que **no** debe leerse como capital de trabajo (K06). Días de stock de 14B (15 d maíz y soja, 30 d micros, 2 d alimento en planta, 3 d en granja) son SUPUESTOS (SUP-149/150).

## 3. Cuentas por cobrar y por pagar

- **CxC**: las ventas no se modelan en 20_opex (no se asume precio del pollo ni que los 90 supermercados compren). La fórmula está implementada: con `ventas_anuales_usd` y `dias_cobro` (DPV-039) se calcula. Más días de cobro → más CT (test K04).
- **CxP**: por grupo de proveedor (alimento, pollitos, granos, servicios, packaging, logística, energía) con `dias_pago = {grupo: días}`. Requiere que todas las compras del grupo tengan precio. Más días de pago → menos CT (test K04). Sueldos y cargas devengados no se incluyen todavía (se modelarán con el cronograma de pagos del modelo financiero).
- **Caja operativa**: buffer en días de OPEX, **opcional** (sin input: `NO_ASIGNADA`, valor 0, no es faltante).

## 4. Qué falta para un CTO

Precios de alimento, pollito, soja, envases e insumos; método de valuación del activo biológico y costo de producción por kg; días de stock de envases, repuestos e insumos; ventas y días de cobro por canal; días de pago por proveedor. Lista priorizada en [`matriz_validacion_opex.csv`](matriz_validacion_opex.csv) (ítem "capital de trabajo").
