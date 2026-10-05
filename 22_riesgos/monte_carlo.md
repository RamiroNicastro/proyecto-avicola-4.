# Monte Carlo y correlaciones

**Fecha:** 2026-10-05 · Inputs: [`distribuciones_riesgo.csv`](distribuciones_riesgo.csv), [`correlaciones_riesgo.csv`](correlaciones_riesgo.csv) · Código: `monte_carlo()`, `cuantil()`, `cholesky()` en [`motor_riesgo.py`](motor_riesgo.py) · Salidas: [`monte_carlo_resultados.csv`](monte_carlo_resultados.csv) (+ `monte_carlo_muestras.csv` en el caso artificial)

## 1. Distribuciones

Cada variable declara `DISTRIBUCION`, `PARAMETROS` (en la unidad del shock), `FUENTE` y `ESTADO` (PENDIENTE / RESPALDADA / ARTIFICIAL). Tipos: triangular, normal truncada, uniforme, lognormal, discreta, determinista, empírica. Muestreo por **inversa de la CDF**; con correlaciones declaradas, **cópula gaussiana** (Cholesky; matriz no definida positiva → error).

- **Proyecto:** exige todas las distribuciones usadas RESPALDADAS → hoy `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES` (14 variables declaradas sin distribución; DPV-180). En el universo EVIDENCIA, además, no se perturba la evidencia.
- **Caso artificial:** ejecutable con distribuciones ARTIFICIALES (solo permitidas en `ARTIFICIAL_TEST`; fuera de él → error).

## 2. Correlaciones

- 9 pares con relación evidente (pollo/alimento, maíz/soja, FX/precio, FX/alimento, demanda/precio, utilización/eficiencia, inflación–FX/salarios y tarifas, alimento/FCR) con **`CORRELACION = PENDIENTE`** (coeficiente vacío, ESTADO PENDIENTE; DPV-180). Pendiente **no** es 0.
- Si un par pendiente afecta variables muestreadas, la corrida **no se ejecuta** (`NO_EJECUTADO_CORRELACION_PENDIENTE`), salvo que el usuario declare `montecarlo.supuesto_independencia = TRUE` en un escenario hipotético: entonces se rotula **`SUPUESTO_INDEPENDENCIA_ESCENARIO`** con los pares.
- Un 0 explícito es una declaración (el caso artificial declara demanda–precio = 0 como `ARTIFICIAL`) y se informa en `CORRELACIONES_DECLARADAS`.
- Tests RIE-04, MC-05; mutación R26.

## 3. Resultados y tipos de probabilidad

Media, mediana, P5/P10/P50/P90/P95 (interpolación lineal) de VAN, TIR (si se pide), pico de fondos, DSCR y payback; P(VAN < 0); P(déficit) = P(pico > capital declarado) o, sin capital, P(caja del accionista < 0); P(no recupero). Semilla obligatoria (MC-01).

Tres tipos de probabilidad que nunca se confunden (`TIPOS_PROBABILIDAD`):

| Tipo | Qué es | Dónde aparece |
|---|---|---|
| `PROBABILIDAD_SIMULADA` | frecuencia dentro de las simulaciones, condicionada a las distribuciones declaradas | única que produce Monte Carlo (`TIPO_PROBABILIDAD`, `ES_PROBABILIDAD_HISTORICA = FALSE`, `ES_PROBABILIDAD_DEL_PROYECTO = FALSE`, etiqueta `PROBABILIDAD_SIMULADA_NO_HISTORICA`) |
| `PROBABILIDAD_HISTORICA` | frecuencia observada en datos | no existe en el repo para el proyecto |
| `PROBABILIDAD_DEL_PROYECTO` | probabilidad específica del proyecto con método | `PROBABILIDAD` del registro de riesgos: hoy PENDIENTE en los 34 ([`registro_riesgos.md`](registro_riesgos.md)) |

Test AUD-12.
