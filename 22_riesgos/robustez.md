# Robustez y SCORE_ORDINAL_RIESGO

**Fecha:** 2026-10-05 · Código: `escenarios_robustez()`, `robustez()`, `score_riesgo()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salida: [`robustez_alternativas.csv`](robustez_alternativas.csv)

## 1. Robustez

- **Robustez = comportamiento en un conjunto de escenarios**, no un resultado base. Escenarios: stress activos con magnitud declarada + extremos (mín y máx) de los shocks one-way de `robustez.variables` (SUP-226). Deterministas, no probabilísticos; la base no se cuenta.
- Indicadores: % de escenarios con VAN ≥ 0, peor VAN, P10 del VAN (si hay Monte Carlo), máximo pico, máximo payback, # no recuperados, % de escenarios que cumplen las HARD. Indicador para rankear: `robustez.criterio` (default % VAN ≥ 0).
- **Mínimo de escenarios:** `robustez.min_escenarios` (default 3, parámetro técnico). Con menos → `ROBUSTEZ = PENDIENTE`.
- Proyecto real hoy: PENDIENTE (ninguna alternativa completa); NO_INVERTIR_AUN: NO_APLICA. Tests OPT-19, AUD-16.

## 2. SCORE_ORDINAL_RIESGO

- Score **ordinal** para ordenar alternativas dentro de un mismo conjunto. **NO ES PROBABILIDAD** ni expectativa estadística (columna `RIESGO_TIPO` en las salidas).
- Fórmula: Σ wᵢ·cᵢ ÷ Σ wᵢ con componentes en [0, 1]: VAN negativo en escenarios, sensibilidad del VAN (amplitud ÷ (|VAN| + amplitud)), pico de fondos relativo (min–max dentro del conjunto), demanda no respaldada, gates físicos pendientes, evidencia faltante. No usa BAJA/MEDIA/ALTA del registro ni las convierte en números.
- Sin pesos (`riesgo.peso.*`) → PENDIENTE (no 0). Componente faltante: SEPARAR (score PENDIENTE) o PENALIZAR (= 1) (SUP-222). Tests OPT-12, AUD-07.
