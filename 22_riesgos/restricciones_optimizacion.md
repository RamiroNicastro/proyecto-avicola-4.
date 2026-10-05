# Restricciones y consultas

**Fecha:** 2026-10-05 · Inputs: [`inputs_riesgo_optimizacion.csv`](inputs_riesgo_optimizacion.csv) (`restriccion.<NOMBRE>.valor/.tipo/.penalizacion`, `consulta.*`) · Código: `leer_restricciones()`, `evaluar_restricciones()`, `consulta_*()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salidas: [`restricciones_alternativas.csv`](restricciones_alternativas.csv), `consulta_*.csv`

## 1. Restricciones

Todas opcionales (vacío = no hay); **ninguna viene cargada** y nunca se asume USD 2 M.

| Nombre | Métrica | Sentido |
|---|---|---|
| CAPITAL_DISPONIBLE | pico de fondos (o fondos iniciales, `capital.metrica`; SUP-221) | ≤ |
| FONDOS_INICIALES, PICO_FONDOS, DEUDA | métricas del motor | ≤ |
| PAYBACK | payback simple (NO_RECUPERADO = incumple) | ≤ |
| VAN, TIR, DSCR | métricas del motor | ≥ |
| DEMANDA_ASEGURADA | % de la capacidad con demanda DOCUMENTADA/ASEGURADA | ≥ |
| UTILIZACION | utilización efectiva del último año | ≥ |
| SUPERFICIE_TERRENO, AGUA, POTENCIA | requerimiento de los gates (0 solo si es estructural; DESCONOCIDO → NO_EVALUABLE) | ≤ |
| CAPACIDAD | capacidad final (aves/día) | ≤ |
| RIESGO | SCORE_ORDINAL_RIESGO | ≤ |

- **HARD** excluye del ranking; **SOFT** resta `penalización × violación relativa` al score (sin penalización declarada → error). Una HARD no evaluable excluye por defecto (SUP-220).
- NO_INVERTIR_AUN: todas `NO_APLICA_STATUS_QUO`.
- Tests OPT-01, OPT-02, OPT-04, OPT-11, OPT-18; mutaciones R01, R14.

## 2. Consultas (input del usuario)

- **Capital** (`consulta.capital_usd`): factibles, no factibles, capital faltante = requerido − X, principal restricción y mejor por objetivo con esa restricción.
- **Demanda** (`consulta.demanda_t_dia`): escala la demanda del escenario a X; utilización, capacidad ociosa, ratio capacidad/demanda, demanda mínima para VAN = 0 (punto de quiebre) y faltante; conclusión `FACON_ASSET_LIGHT_HASTA_VALIDAR_MAS_DEMANDA` si solo el asset-light tiene VAN ≥ 0.
- **Payback** (`consulta.payback_max_anios`): quién cumple y el cambio mínimo de precio, CAPEX, demanda o alimento que haría falta (informado, **no aplicado**).

Hoy las tres consultas del proyecto están en `SIN_CONSULTA`.
