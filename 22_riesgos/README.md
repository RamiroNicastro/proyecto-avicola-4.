# 22 — Riesgos, sensibilidades y optimizador

**Alcance:** matriz de riesgos (sanitarios —p. ej. influenza aviar—, de mercado, precios de granos, cambiarios, regulatorios, comerciales, operativos, de ejecución y de financiamiento) y **capa de decisión** sobre los motores existentes: sensibilidades, stress, puntos de quiebre, Monte Carlo, comparación de arquitecturas, robustez, restricciones y búsqueda de configuraciones.

**Estado (2026-10-05, sesión 20):** **CAPA DE RIESGO Y OPTIMIZACIÓN ESTRUCTURAL v1.1** (con auditoría final) — 69 tests y 27/27 mutaciones detectadas ([`cobertura_mutaciones.csv`](cobertura_mutaciones.csv)); motor financiero 70/70 con una sola modificación de interfaz (`calcular_tir`, default idéntico a la sesión 19). **`OPTIMIZACION_REAL_NO_DISPONIBLE`**: ninguna de las 54 alternativas de inversión del mapa tiene VAN publicable en modo evidencia (faltan precios, demanda A/B, OPEX y CAPEX costeables, cronograma, fiscal y tasa). El universo ESCENARIO está listo pero vacío (`escenario_optimizador.json` sin completar → `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO`). Monte Carlo del proyecto: `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES`. **Sin recomendación de arquitectura, escala ni inversión.**

## Principio

No hay un segundo modelo financiero. Cada alternativa se arma con `construir_entrada()` y se evalúa con `simular()` + `resultados()` de [`../21_modelo_financiero/modelo_financiero.py`](../21_modelo_financiero/modelo_financiero.py) (sin cambiar su lógica; el modo rápido usa el parámetro explícito `calcular_tir=False`), que consume CAPEX (19), OPEX (20), balance (04), escala (23) y demanda (02):

```
CONFIGURACIÓN + ESCENARIO + RESTRICCIONES + SHOCKS → MOTOR FINANCIERO → RESULTADOS → RIESGO / SENSIBILIDAD / OPTIMIZACIÓN
```

Tres universos que nunca se rankean juntos: **EVIDENCIA** (solo lo respaldado), **ESCENARIO** (inputs del usuario, `SIMULACION_HIPOTETICA_NO_VALIDADA`) y **ARTIFICIAL_TEST** ([`casos_prueba/`](casos_prueba/), alternativas `ART-*` inventadas para probar la maquinaria: `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO`). Toda salida lleva `AMBITO` = PROYECTO o ARTIFICIAL_TEST.

## Uso

```
python3 22_riesgos/modelo_optimizador.py                 # tests + salidas del proyecto + caso artificial
python3 22_riesgos/modelo_optimizador.py --solo-tests
python3 22_riesgos/modelo_optimizador.py --mutaciones
python3 22_riesgos/modelo_optimizador.py --escenario mi_escenario.json --salida carpeta/
```

## Archivos

| Tipo | Archivo | Contenido |
|---|---|---|
| Modelo | [`motor_riesgo.py`](motor_riesgo.py) | Registro de variables y transformaciones, evaluador con caché, one-way, tornado, 2D, stress, puntos de quiebre, Monte Carlo, registro/matriz de riesgos |
| Modelo | [`modelo_optimizador.py`](modelo_optimizador.py) | Espacio de decisiones, factibilidad física, restricciones, comparabilidad, robustez, score de riesgo, objetivos, dominancia, Pareto, consultas, valor de la información, QUE_HACER_AHORA, dashboard, CLI |
| Tests | [`tests_riesgo_optimizador.py`](tests_riesgo_optimizador.py) · [`cobertura_mutaciones.csv`](cobertura_mutaciones.csv) | Tests SENS, RIE, MC, OPT, COMP, QUI, AUD; mutaciones R01–R27 con el test que detecta cada una |
| Input | [`inputs_riesgo_optimizacion.csv`](inputs_riesgo_optimizacion.csv) | Objetivos, restricciones, shocks, rangos, pesos, Monte Carlo, robustez, consultas (sin valores empresariales por defecto) |
| Input | [`escenario_optimizador.json`](escenario_optimizador.json) | Universo ESCENARIO: `comun` (misma estructura que la plantilla de 21), `por_alternativa`, `base_valores`, `disponibilidad` física (todo `null`) |
| Input | [`escenarios_stress.csv`](escenarios_stress.csv) · [`distribuciones_riesgo.csv`](distribuciones_riesgo.csv) · [`correlaciones_riesgo.csv`](correlaciones_riesgo.csv) | Stress editables (ilustrativos), distribuciones y correlaciones (todas PENDIENTES) |
| Input | [`registro_riesgos.csv`](registro_riesgos.csv) | 34 riesgos cualitativos (BAJA / MEDIA / ALTA / PENDIENTE); probabilidad del proyecto PENDIENTE y frecuencia sectorial aparte |
| Salida | [`matriz_riesgos.csv`](matriz_riesgos.csv) · [`registro_variables_riesgo.csv`](registro_variables_riesgo.csv) · [`espacio_decisiones.csv`](espacio_decisiones.csv) | Matriz inherente/residual; 59 variables con su soporte en el motor; 2.592 combinaciones (1.134 físicamente inválidas, 1.450 posibles no modeladas, 8 habilitadas → 54 alternativas) |
| Salida | [`sensibilidad_oneway.csv`](sensibilidad_oneway.csv) · [`sensibilidad_tornado.csv`](sensibilidad_tornado.csv) · [`sensibilidad_2d.csv`](sensibilidad_2d.csv) · [`resultados_stress.csv`](resultados_stress.csv) · [`puntos_quiebre.csv`](puntos_quiebre.csv) · [`monte_carlo_resultados.csv`](monte_carlo_resultados.csv) | Hoy NO_CALCULABLE en el proyecto (ver `casos_prueba/` para la maquinaria funcionando) |
| Salida | [`resultados_optimizador.csv`](resultados_optimizador.csv) · [`decision_optimizador.csv`](decision_optimizador.csv) · [`explicacion_optimizador.csv`](explicacion_optimizador.csv) · [`frontera_pareto.csv`](frontera_pareto.csv) · [`dashboard_decision.csv`](dashboard_decision.csv) | Alternativa × objetivo; decisión por objetivo (mejor, segunda, robustez); explicación; Pareto; datos para la futura app |
| Salida | [`factibilidad_alternativas.csv`](factibilidad_alternativas.csv) · [`restricciones_alternativas.csv`](restricciones_alternativas.csv) · [`robustez_alternativas.csv`](robustez_alternativas.csv) | Gates físicos, restricciones, robustez y componentes del score de riesgo |
| Salida | [`prioridad_validacion.csv`](prioridad_validacion.csv) · [`que_hacer_ahora.csv`](que_hacer_ahora.csv) | Qué dato faltante pesa más (derivado del motor) y acciones vinculadas a DPV existentes |
| Salida | [`consulta_capital.csv`](consulta_capital.csv) · [`consulta_demanda.csv`](consulta_demanda.csv) · [`consulta_payback.csv`](consulta_payback.csv) · [`resumen_corrida.csv`](resumen_corrida.csv) | Consultas del usuario (hoy SIN_CONSULTA: no se asume capital, demanda ni payback) y trazabilidad de la corrida |
| Prueba | [`casos_prueba/`](casos_prueba/) | Las mismas salidas para el universo ARTIFICIAL_TEST (no son resultados del proyecto) |
| Doc | [`metodologia_riesgo.md`](metodologia_riesgo.md) (marco e índice) · [`registro_riesgos.md`](registro_riesgos.md) · [`sensibilidades.md`](sensibilidades.md) · [`stress_tests.md`](stress_tests.md) · [`puntos_quiebre.md`](puntos_quiebre.md) · [`monte_carlo.md`](monte_carlo.md) | Capa de riesgo |
| Doc | [`metodologia_optimizador.md`](metodologia_optimizador.md) · [`objetivos_optimizacion.md`](objetivos_optimizacion.md) · [`restricciones_optimizacion.md`](restricciones_optimizacion.md) · [`robustez.md`](robustez.md) · [`pareto.md`](pareto.md) · [`explicabilidad.md`](explicabilidad.md) · [`valor_informacion.md`](valor_informacion.md) | Optimizador |
| Doc | [`conclusiones_riesgo_optimizacion.md`](conclusiones_riesgo_optimizacion.md) · [`guia_ramiro.md`](guia_ramiro.md) | Conclusiones y guía en lenguaje simple |
| Gestión | [`actualizaciones_gestion_20.md`](actualizaciones_gestion_20.md) | SUP-20-##, DPV-20-##, DEC-20-## provisionales para reconciliar |

**Relacionado:** [`21_modelo_financiero`](../21_modelo_financiero/README.md), [`19_capex`](../19_capex/README.md), [`20_opex`](../20_opex/README.md), [`23_plan_expansion`](../23_plan_expansion/README.md), [`mapa_arquitecturas_economicas.csv`](../00_gestion_proyecto/mapa_arquitecturas_economicas.csv).
