# Explicabilidad, semáforo y dashboard

**Fecha:** 2026-10-05 · Código: `explicar_decision()`, `filas_explicacion()`, `filas_dashboard()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salidas: [`decision_optimizador.csv`](decision_optimizador.csv), [`explicacion_optimizador.csv`](explicacion_optimizador.csv), [`dashboard_decision.csv`](dashboard_decision.csv)

## 1. Recomendación DEL ESCENARIO (por objetivo)

Cuando hay ganador (`ESTADO = MEJOR_EN_ESCENARIO`), [`decision_optimizador.csv`](decision_optimizador.csv) informa:

| Pregunta | Campo |
|---|---|
| Qué ganó / objetivo | `QUE_ELIGIO`, `MEJOR`, `OBJETIVO`, `METRICA`, `POR_QUE` |
| Segunda y diferencia | `SEGUNDA`, `DIFERENCIA_VALOR`, `DIFERENCIA_SCORE` |
| Contra qué | `CONTRA_QUE` |
| Restricciones que cumple | `RESTRICCIONES_CUMPLE` |
| Variables críticas | `VARIABLES_CRITICAS` (tornado del ganador) |
| Qué la hace ganar | `VARIABLES_QUE_LA_HACEN_GANAR` (diferencias vs la segunda) |
| Qué podría cambiarla | `VARIABLES_QUE_PODRIAN_CAMBIARLA`, `STRESS_QUE_CAMBIA_DECISION`, `ROBUSTEZ_DECISION`, `ESTABILIDAD_GANADOR` |
| Datos faltantes y evidencia | `DATOS_FALTANTES_VALIDAR`, `EVIDENCIA_GANADORA` |
| Por qué NO_INVERTIR_AUN podría ganar | `POR_QUE_NO_INVERTIR_PODRIA_GANAR`, `DECISION_ESCENARIO`, `REGLA_STATUS_QUO` |

Etiqueta `SIMULACION_HIPOTETICA_NO_VALIDADA` (escenario) o `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO`. **Sin ganador** (`OPTIMIZACION_REAL_NO_DISPONIBLE`, `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO`) no se fabrica explicación: los campos dicen `NO_APLICA: <estado>` y `DECISION_ESCENARIO = —`. Con `NINGUNA_CONFIGURACION_FACTIBLE` se explica la regla SQ que aplica. Test AUD-17.

## 2. Por alternativa

[`explicacion_optimizador.csv`](explicacion_optimizador.csv): razones a favor y en contra, drivers críticos, puntos de quiebre, restricciones incumplidas, dato que más podría cambiar la decisión, datos faltantes, cobertura de evidencia y confianza (BAJA si cobertura < 100 %).

## 3. Semáforo y dashboard

Semáforo GRIS / ROJO / AMARILLO / VERDE ([`metodologia_optimizador.md`](metodologia_optimizador.md) §4), sin cortes económicos. [`dashboard_decision.csv`](dashboard_decision.csv): una fila por alternativa con inversión, retorno, riesgo, robustez, restricciones, evidencia, semáforo, recomendación del escenario y qué validar, para la futura app (no creada).
