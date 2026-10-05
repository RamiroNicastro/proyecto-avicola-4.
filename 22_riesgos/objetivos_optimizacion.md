# Objetivos de optimización y ranking

**Fecha:** 2026-10-05 · Código: `rankear()`, `score_balanceado()`, `estabilidad_ganador()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salidas: [`resultados_optimizador.csv`](resultados_optimizador.csv), [`decision_optimizador.csv`](decision_optimizador.csv)

## 1. Objetivos

| Objetivo | Métrica | Sentido |
|---|---|---|
| MAX_VAN | VAN | máx |
| MAX_TIR | TIR (única; ambigua o inexistente → excluida con motivo) | máx |
| MIN_PAYBACK | payback simple (NO_RECUPERADO → excluida con motivo) | mín |
| MIN_FONDOS_INICIALES / MIN_CAPEX / MIN_PICO_FONDOS | fondos / CAPEX / pico | mín |
| MAX_EBITDA / MAX_DSCR | EBITDA del último año / DSCR mínimo | máx |
| MIN_RIESGO | SCORE_ORDINAL_RIESGO ([`robustez.md`](robustez.md)) | mín |
| MAX_ROBUSTEZ | indicador de robustez | máx |
| MAX_CRECIMIENTO | capacidad final alcanzada (aves/día) | máx |
| BALANCEADO | score ponderado | máx |

`optimizador.objetivos = TODOS` (default): un ranking por objetivo. **Ninguno es "el" criterio empresarial** (DEC-097).

## 2. Conjunto rankeable y score

Entra al ranking una alternativa de inversión del mismo universo, comparable (TRUE/PARCIAL), no físicamente infactible, sin HARD incumplidas ni pendientes y con la métrica del objetivo. NO_INVERTIR_AUN nunca entra ([`metodologia_optimizador.md`](metodologia_optimizador.md) §5). SCORE = valor normalizado min–max (mejor = 1) − penalizaciones SOFT ([`restricciones_optimizacion.md`](restricciones_optimizacion.md)).

## 3. Objetivo balanceado

Pesos de rentabilidad (VAN), riesgo (SCORE_ORDINAL_RIESGO), capital (fondos), liquidez (pico), crecimiento y robustez, normalizados a 1. Sin pesos → `PESOS_NO_DEFINIDOS` (no se cargan pesos "correctos"); preset `IGUALES` solo si el usuario lo pide, rotulado SUP-219. Componente faltante: SEPARAR (default) o PENALIZAR.

## 4. Mejor, segunda y robustez de la decisión

Cada objetivo informa `MEJOR`, `SEGUNDA`, `DIFERENCIA_VALOR` y `DIFERENCIA_SCORE`. `DECISION_NO_ROBUSTA` si (a) el ganador cambia en algún escenario de robustez (`ESTABILIDAD_GANADOR` < 1, con la lista y el campo `STRESS_QUE_CAMBIA_DECISION`), (b) la diferencia relativa ≤ `decision.tolerancia_equivalencia` (si se declara) o (c) empate. Luego `DECISION_ESCENARIO` aplica las reglas de status quo. Sin inversión rankeable → `NINGUNA_CONFIGURACION_FACTIBLE` con las causas contadas; no se elige "la menos mala". Tests OPT-09, OPT-13, OPT-14; mutaciones R04, R20.
