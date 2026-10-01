# 15 — Incubación

**Alcance:** abastecimiento de pollito BB y huevo fértil, reproductoras, planta de incubación propia vs. compra a terceros, parámetros de incubabilidad.

**Relacionado:** `03_produccion_primaria`, `04_balance_masa`, `14_alimento_balanceado` (modelo físico del upstream), DPV-006, DPV-047, DEC-023.

**Contenido (2026-09-30):** [`cuestionario_incubadoras.md`](cuestionario_incubadoras.md) — preguntas para incubadoras y proveedores de pollito BB (capacidad, disponibilidad, genética, calidad, vacunación, precio, volumen mínimo, contratos, expansión) y tabla comparativa. No se asume incubadora propia (SUP-034).

## Contenido (v1.0, 2026-10-01; sesión 14B)

| Archivo | Contenido |
|---|---|
| [`conclusiones_incubacion.md`](conclusiones_incubacion.md) | **Síntesis**: pollitos, huevos, capacidad, opciones por fase, faltantes |
| [`modelo_incubacion.md`](modelo_incubacion.md) | Proceso huevo fértil → almacenamiento → incubadora → nacedora → selección → vacunación → expedición; cadena de cálculo y parámetros (supuestos) |
| [`capacidad_incubacion.md`](capacidad_incubacion.md) | Pollitos → huevos → capacidad semanal instalada por escala; sensibilidad; expedición por nacimiento; reproductoras (solo fase futura) |
| [`compra_vs_incubacion.md`](compra_vs_incubacion.md) | A comprar pollitos / B incubar huevo fértil comprado / C reproductoras (fase futura), sin costos |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin jerga |

El cálculo está en [`../14_alimento_balanceado/modelo_upstream.py`](../14_alimento_balanceado/modelo_upstream.py) (bloques `2_*` de `escenarios_upstream.csv`). **Sin decisión:** DEC-023 abierta; SUP-034 vigente.
