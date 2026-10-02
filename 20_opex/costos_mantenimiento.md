# Costos de mantenimiento

**Fecha:** 2026-10-02 · Implementación: §MANTENIMIENTO de `generar_registro()`, `base_capex_area()`, `n_activos_area()` en [`modelo_opex.py`](modelo_opex.py)

> **El % del CAPEX no se usa como verdad.** Es uno de cuatro métodos alternativos, cualquier valor que se cargue es `[SUPUESTO]`/`[PVDP]` (SUP-17-06), y hoy no puede calcularse porque el CAPEX no tiene precio.

## 1. Áreas y tipos

Áreas (activas según los activos propios de la arquitectura): PROC (línea y subproductos), FRIO, ELEC (electricidad y automatización: activos EL-* del BOQ), UTIL (agua, térmico, aire y efluentes), EDIF (obra civil; en C0 la oficina), INC (incubadora), ALI (planta de alimento), GRA (granjas propias).

Tipos: preventivo, correctivo, repuestos, lubricantes, servicios técnicos externos, contratos. La **mano de obra propia** (técnicos, jefe de mantenimiento, pañolero) está en costo laboral (14A) y aparece en este módulo como fila `INCLUIDO`. El mantenimiento de la flota propia va en logística (por km).

## 2. Métodos (uno por corrida; no se mezclan)

| `mantenimiento_metodo` | Conceptos | Cantidad | Estado hoy |
|---|---|---|---|
| `None` (por defecto) | una fila por área | — | `METODO_MANTENIMIENTO_NO_DEFINIDO` (DEC-17-06) |
| `pct_capex` | MAN-<área>-PCT | CAPEX con precio del área (bloques del BOQ de 19) | `BASE_SIN_PRECIO`: el CAPEX no tiene total (test A10) |
| `por_activo` | MAN-<área>-PREV / CORR / REP / LUB | activos costeables del área en el BOQ (activo-año) | Cantidades disponibles; precios PENDIENTES |
| `horas_tecnicas` | MAN-<área>-STEC | horas técnicas externas | PENDIENTE_CANTIDAD (no dimensionadas más allá de 14A) |
| `contrato` | MAN-<área>-CONT | 1 contrato-año | Sin precio (variante `C1-10000-MANT-CONTRATO`) |

## 3. Por qué no un % fijo

Un porcentaje anual sobre el CAPEX mezcla tecnologías con desgaste distinto (frío y línea vs obra civil), depende de un CAPEX que hoy no existe y, aplicado a una planta "barata", subestima: los equipos de menor costo suelen requerir más correctivo y repuestos. Los métodos por activo o por contrato se pueden cotizar con el mismo RFQ de los equipos (`19_capex/plan_cotizaciones.md`), pidiendo el plan de mantenimiento y los repuestos críticos (DPV-17-10).
