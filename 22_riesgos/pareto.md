# Dominancia y frontera de Pareto

**Fecha:** 2026-10-05 · Código: `dominancia()`, `pareto()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salidas: columna `DOMINADA` de [`resultados_optimizador.csv`](resultados_optimizador.csv), [`frontera_pareto.csv`](frontera_pareto.csv)

## 1. Dominancia

A domina a B (misma base comparable) si es igual o mejor en todas las dimensiones disponibles (default: fondos iniciales ↓, VAN ↑, SCORE_ORDINAL_RIESGO ↓) y **estrictamente** mejor en al menos una; se requieren ≥ 2 dimensiones y se declaran las usadas. B se marca `DOMINADA_POR`, no se elimina. Solo participan alternativas con COMPARABILIDAD TRUE o PARCIAL: una FALSE queda `NO_EVALUABLE (COMPARABILIDAD FALSE)` y NO_INVERTIR_AUN `NO_APLICA_STATUS_QUO`. Tests OPT-07, AUD-14; mutaciones R15, R27.

## 2. Frontera de Pareto

- Por par de ejes (VAN × fondos, VAN × SCORE_ORDINAL_RIESGO, VAN × pico, VAN × payback): `EN_FRONTERA` y quién domina en el par, entre alternativas comparables.
- Con menos de 2 alternativas comparables con ambos ejes, el par se marca **`PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE`** (no se presenta una "frontera" de un solo punto como descubrimiento). Las alternativas no comparables siguen visibles como `NO_EVALUABLE`; NO_INVERTIR_AUN no participa.
- La frontera no es un ranking. Tests OPT-08, AUD-15; mutación R20.
- Proyecto hoy: todas las alternativas `NO_EVALUABLE` (sin VAN publicable).
