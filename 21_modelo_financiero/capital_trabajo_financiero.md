# Capital de trabajo en el modelo financiero

**Fecha:** 2026-10-04 · Salida: [`capital_trabajo_financiero.csv`](capital_trabajo_financiero.csv) · Estructura consumida: [`../20_opex/capital_trabajo.md`](../20_opex/capital_trabajo.md) e interfaz OPEX §6

## 1. Fórmula (por mes, saldo a fin de mes)

```
CT_OPERATIVO  = INVENTARIOS_PROPIOS + CUENTAS_POR_COBRAR + CAJA_OPERATIVA − CUENTAS_POR_PAGAR    (test I04)
ΔCT(mes)      = CT(mes) − CT(mes − 1)        ← lo que entra al flujo (test I05; mutación M04)
Σ ΔCT         = CT al cierre del horizonte
```

Base de días: `DIAS_MES = 365 ÷ 12` (días calendario; SUP-19-11).

| Componente | Cálculo | Por | Input (hoy) |
|---|---|---|---|
| Inventarios | días de stock × costo mensual de la base ÷ `DIAS_MES` (+ stock fijo opcional) | categoría: materias primas, alimento, packaging, repuestos, producto terminado, activo biológico, otros | `dias_stock.<cat>` PENDIENTES (DPV-175, DEC-089) |
| Cuentas por cobrar | ingreso neto del mes ÷ `DIAS_MES` × días de cobro | canal (plazos distintos por canal) | `canales.<canal>.dias_cobro` PENDIENTES (DPV-039, DPV-175) |
| Caja operativa | días × OPEX del mes ÷ `DIAS_MES`; sin política = 0 `NO_ASIGNADA` (misma convención de 20) | — | `dias_caja_operativa` PENDIENTE (DEC-091) |
| Cuentas por pagar | compra del mes ÷ `DIAS_MES` × días de pago | grupo de proveedor: alimento, pollitos, granos, servicios, packaging, logística, energía | `dias_pago.<grupo>` PENDIENTES (DPV-175) |

## 2. Solo inventario propio

La propiedad por categoría se toma de `capital_trabajo()` de 20_opex (`ENTRA_EN_CT`, `PROPIEDAD_EMPRESA`): el stock de terceros (alimento en la fábrica proveedora, MP del elaborador en façon B2) **no** entra; la propiedad PENDIENTE (façon sin variante B1/B2, DEC-024) deja el CT incompleto. Ejemplos de la corrida:

| Categoría | C1-10000 | C0-10000 |
|---|---|---|
| Materias primas (granos) | No propio (proveedor) | PENDIENTE (DEC-024) |
| Alimento terminado | Propio (en silos de granja) | PENDIENTE (DEC-024) |
| Activo biológico (aves, pollitos) | Propio | Propio |
| Producto terminado | Propio | Propio (en frío del faenador) |
| Packaging, repuestos, otros | Propio | Propio |

Bases de valuación por defecto (`BASE_INVENTARIO`): alimento → rubros del grupo alimento; materias primas → granos y alimento; activo biológico → alimento y pollitos; producto terminado → OPEX total del mes (costo de producción como cota, DEC-089). Son criterios de modelo editables, no valuaciones definitivas.

## 3. Reglas

- **No se supone que el supermercado pague contado**: sin `dias_cobro` el CT queda incompleto.
- Cuentas por cobrar **sin IVA** (el IVA tiene módulo propio).
- Sueldos y cargas devengados **fuera** de CxP por ahora (interfaz OPEX §6); los rubros sin grupo de proveedor no generan CxP.
- **Crecer consume caja:** cada aumento de ventas aumenta CxC e inventarios antes de cobrar; el ΔCT del ramp-up y de cada expansión es negativo para la caja (caso de prueba CP-04: cobrar a 30 días baja el VAN de 51,63 a 44,16 en el caso artificial).

## 4. Capital de trabajo inicial (para fondos iniciales)

`CT_INICIAL` = máximo CT alcanzado hasta el fin del ramp-up de la etapa inicial (SUP-19-19). `CT_MAXIMO` = máximo del horizonte. Ver [`flujo_caja.md`](flujo_caja.md) §3.
