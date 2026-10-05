# Conclusiones de la sesión 20 — riesgos, sensibilidades y optimizador (con auditoría final)

**Fecha:** 2026-10-05 · **Estado:** CAPA DE RIESGO Y OPTIMIZACIÓN ESTRUCTURAL v1.1 (auditoría final). **`OPTIMIZACION_REAL_NO_DISPONIBLE`.** No se elige arquitectura, escala, financiamiento ni momento de inversión.

## 1. Qué se construyó

Una capa de decisión que usa el motor financiero de la sesión 19 como **función de evaluación** (sin copiar fórmulas; única modificación del motor: el parámetro de interfaz `calcular_tir`, ver [`metodologia_riesgo.md`](metodologia_riesgo.md) §3) y permite responder, cuando haya datos:

| Pregunta | Dónde |
|---|---|
| ¿Qué variables afectan más? | `sensibilidad_tornado.csv` (amplitud por variable y métrica) |
| ¿Qué pasa si cambia precio, alimento, demanda, CAPEX, FX o utilización? | `sensibilidad_oneway.csv`, `sensibilidad_2d.csv`, `resultados_stress.csv` |
| ¿Hasta dónde aguanta? | `puntos_quiebre.csv` (precio mínimo, alimento máximo, demanda y utilización mínimas, CAPEX máximo, cobro máximo, tasa máxima, mortalidad y FCR máximos) |
| ¿Qué arquitectura es más robusta / menos riesgosa? | `robustez_alternativas.csv`, `monte_carlo_resultados.csv`, objetivos MAX_ROBUSTEZ / MIN_RIESGO |
| ¿Cuál maximiza VAN, requiere menos capital, recupera antes? | `decision_optimizador.csv` (un ranking por objetivo, con segunda alternativa y robustez de la decisión) |
| ¿Qué configuración cumple mis restricciones? | `restricciones_alternativas.csv`, `consulta_capital.csv`, `consulta_payback.csv` |
| ¿Construir ahora, tercerizar o esperar? | `OPERAR_ASSET_LIGHT` (C0) compite en los rankings; `NO_INVERTIR_AUN` gana la `DECISION_ESCENARIO` por reglas explícitas SQ-1…SQ-6; `consulta_demanda.csv`; `prioridad_validacion.csv` |

## 2. Qué dice hoy para el proyecto

1. **Universo EVIDENCIA:** las 54 alternativas de inversión (5 configuraciones × 4 escalas, 19 variantes, 15 trayectorias) quedan sin VAN publicable → **`OPTIMIZACION_REAL_NO_DISPONIBLE`** en todos los objetivos. No hay decisión ni explicación de recomendación (`DECISION_ESCENARIO = —`).
2. **Universo ESCENARIO:** listo, pero `escenario_optimizador.json` está vacío (no se inventan precios, demanda ni costos) → `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO`. Sensibilidades, stress, quiebres y Monte Carlo del proyecto: NO_CALCULABLE.
3. **Monte Carlo del proyecto:** `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES` (14 variables declaradas sin distribución; 9 correlaciones evidentes con `CORRELACION = PENDIENTE`, que no se trata como 0). Robustez, Pareto y dominancia: no evaluables (PENDIENTE / NO_EVALUABLE).
4. **Qué validar primero** ([`que_hacer_ahora.csv`](que_hacer_ahora.csv), derivado de los bloqueos del motor): **nueve ítems empatados con `RANK_COMPARTIDO` = 1** bloquean los 10 indicadores en las 54 alternativas — cronograma (DPV-086), horizonte y tasa (DEC-007, DPV-001), curva de ramp-up (DEC-090), rendimientos (DPV-060, DEC-028), demanda A/B (DPV-002, 020, 037, 040), precios (DPV-013, 039, 070) y condiciones de canal (DPV-039, 175). El empate se mantiene: no se desempata por orden de archivo, ID ni nombre; lo harán la sensibilidad, la magnitud económica, la capacidad de cambiar la decisión y el costo del dato ([`valor_informacion.md`](valor_informacion.md)). Siguen estructura y salarios, IIBB, OPEX de faena propia (45/54), integrados y pollito (40/54), alimento, y luego CAPEX total y cronograma (7 indicadores en 54/54).
5. **Riesgos:** 34 riesgos cualitativos, **todos con PROBABILIDAD = PENDIENTE**: no existe probabilidad específica del proyecto. Las frecuencias sectoriales de 01 §11 (influenza aviar, granos, tipo de cambio, barreras sanitarias, competencia, conflictividad, capital de trabajo, energía, inflación) se registran aparte en `FRECUENCIA_SECTORIAL_REFERENCIA` y no se convierten en probabilidad; no se calcula riesgo esperado ([`registro_riesgos.md`](registro_riesgos.md)). **Ninguna mitigación está implementada con evidencia**: residual = inherente en los 34.
6. **Espacio de decisiones:** de 2.592 combinaciones de atributos, 1.134 son `FISICAMENTE_INVALIDA`, 1.450 `FISICAMENTE_POSIBLE_NO_MODELADA_ECONOMICAMENTE` (sin CAPEX/OPEX: no se evalúan, DEC-103) y 8 `HABILITADA_EN_MAPA_PARA_EVALUACION`, que generan las 54 alternativas = 5 × 4 escalas + 19 variantes + 5 × 3 trayectorias ([`metodologia_optimizador.md`](metodologia_optimizador.md) §1).

## 3. Qué demuestra el caso artificial (`AMBITO = ARTIFICIAL_TEST`; no es el proyecto)

Con cinco alternativas `ART-*` inventadas ([`casos_prueba/`](casos_prueba/)), la maquinaria muestra comportamientos que importan para cuando haya datos:
- **El objetivo cambia la respuesta:** MAX_VAN elige la planta grande; MIN_FONDOS, MIN_PAYBACK y BALANCEADO eligen el asset-light. No hay "mejor" sin criterio declarado.
- **Una decisión puede ser no robusta:** la planta grande gana MAX_VAN por apenas +1.067 de VAN con +13.500 de CAPEX frente al asset-light, y pierde el primer puesto en los stress de demanda, alimento, precio, CAPEX y financiero (`DECISION_NO_ROBUSTA`, estabilidad del ganador 47 % de los 19 escenarios). Con el stress combinado todas las alternativas tienen VAN < 0: `POR_QUE_NO_INVERTIR_PODRIA_GANAR` lo informa, y si ese stress se declara en `decision.sq_stress` la decisión pasa a NO_INVERTIR_AUN (regla SQ-4).
- **Dominancia sin eliminación:** la planta chica queda `DOMINADA_POR` el asset-light (menos capital, más VAN), pero sigue listada.
- **Restricciones:** la integrada queda ROJO (agua y capital), la incompleta GRIS (su OPEX faltante nunca se toma como 0).
- **Confianza ≠ rentabilidad:** todas las alternativas artificiales tienen cobertura de evidencia 0 → semáforo AMARILLO aunque tengan VAN alto.

## 4. Hallazgos críticos

1. **El cuello de botella sigue siendo comercial y de cronograma**, no de modelado: sin precios, demanda y tiempos no hay ni simulación del proyecto.
2. **El capital relevante es el pico de fondos**, no el CAPEX (test OPT-21): la restricción `CAPITAL_DISPONIBLE` se compara contra el pico por defecto.
3. **La opción de no construir todavía es una alternativa de decisión real**, no un proyecto con ceros: gana la decisión solo por reglas explícitas (ninguna inversión factible, capital, VAN < 0, stress, riesgo o evidencia declarados); con demanda chica, la consulta de demanda puede concluir `FACON_ASSET_LIGHT_HASTA_VALIDAR_MAS_DEMANDA`.
4. **Limitaciones de interfaz detectadas** (para sesiones futuras; en 21 solo se agregó `calcular_tir`): días operativos como variable continua (TF-001), recupero de IVA (TF-002), combinaciones fuera del mapa (DEC-103), moneda original de los rubros para FX (DPV-179), transiciones de arquitectura (DEC-103).

## 5. Próximos pasos (sin decidir nada)

1. Reconciliar [`actualizaciones_gestion_20.md`](actualizaciones_gestion_20.md).
2. Decisiones del inversor que la capa necesita como input: objetivo(s) y pesos (DEC-097), restricciones duras/blandas incluido el capital real (DEC-098), pesos del score de riesgo (DEC-099).
3. Trabajo de campo según `que_hacer_ahora.csv`.
4. Primer escenario del promotor en `escenario_optimizador.json` (rotulado simulación) para obtener el primer tornado y el primer ranking de variables por valor de la información.
5. Recién con series o cotizaciones múltiples: distribuciones y correlaciones respaldadas → Monte Carlo del proyecto.
