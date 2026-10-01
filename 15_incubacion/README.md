# 15 — Incubación

**Alcance:** abastecimiento de pollito BB y huevo fértil, reproductoras, planta de incubación propia vs. compra a terceros, parámetros de incubabilidad.

**Relacionado:** `03_produccion_primaria`, `04_balance_masa`, `14_alimento_balanceado` (modelo físico del upstream), DPV-006, DPV-047, DEC-023.

**Contenido (2026-09-30):** [`cuestionario_incubadoras.md`](cuestionario_incubadoras.md) — preguntas para incubadoras y proveedores de pollito BB (capacidad, disponibilidad, genética, calidad, vacunación, precio, volumen mínimo, contratos, expansión) y tabla comparativa. No se asume incubadora propia (SUP-034).

## Contenido (v1.1, 2026-10-01; sesión 14B con auditoría de sincronización)

| Archivo | Contenido |
|---|---|
| [`conclusiones_incubacion.md`](conclusiones_incubacion.md) | **Síntesis**: pollitos, tiempos, setter/hatcher, cadencia, sincronización, opciones por arquitectura de referencia, faltantes |
| [`modelo_incubacion.md`](modelo_incubacion.md) | Proceso y **cadena temporal** (recepción ≠ carga ≠ nacimiento ≠ llegada a granja; incubación 21 d ≠ lead time); cadena de cálculo y parámetros (supuestos) |
| [`capacidad_incubacion.md`](capacidad_incubacion.md) | Pollitos → huevos cargados/transferidos → **setter y hatcher por separado con cadencia**; lote de nacimiento ≠ demanda semanal; elasticidades; reproductoras (solo arquitectura futura) |
| [`compra_vs_incubacion.md`](compra_vs_incubacion.md) | A comprar pollitos (benchmark) / B incubar huevo fértil comprado / C reproductoras (arquitectura futura): escenarios de comparación, sin costos |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin jerga |

El cálculo está en [`../14_alimento_balanceado/modelo_upstream.py`](../14_alimento_balanceado/modelo_upstream.py) (bloques `2_*` de `escenarios_upstream.csv`). **Sin decisión:** DEC-023 abierta; SUP-034 vigente.
