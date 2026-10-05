# Metodología — capa de riesgo (marco general)

**Fecha:** 2026-10-05 · **Sesión:** 20 (incluye auditoría final) · Código: [`motor_riesgo.py`](motor_riesgo.py) · Tests: [`tests_riesgo_optimizador.py`](tests_riesgo_optimizador.py)

Todo número económico sale del motor de la sesión 19 ([`../21_modelo_financiero/modelo_financiero.py`](../21_modelo_financiero/modelo_financiero.py)). Esta capa solo (a) arma entradas, (b) les aplica shocks, (c) llama al motor y (d) compara resultados. No contiene fórmulas de ingresos, costos, flujo, VAN, TIR ni payback.

**Documentos de detalle** (cada tema vive en un solo archivo):

| Tema | Archivo |
|---|---|
| Registro y matriz de riesgos; frecuencia sectorial vs probabilidad | [`registro_riesgos.md`](registro_riesgos.md) |
| Sensibilidad one-way, tornado y 2D | [`sensibilidades.md`](sensibilidades.md) |
| Stress tests | [`stress_tests.md`](stress_tests.md) |
| Puntos de quiebre | [`puntos_quiebre.md`](puntos_quiebre.md) |
| Monte Carlo, correlaciones y tipos de probabilidad | [`monte_carlo.md`](monte_carlo.md) |
| Optimizador: espacio, factibilidad, comparabilidad, NO_INVERTIR_AUN | [`metodologia_optimizador.md`](metodologia_optimizador.md) |
| Objetivos y ranking | [`objetivos_optimizacion.md`](objetivos_optimizacion.md) |
| Restricciones y consultas | [`restricciones_optimizacion.md`](restricciones_optimizacion.md) |
| Robustez y SCORE_ORDINAL_RIESGO | [`robustez.md`](robustez.md) |
| Dominancia y Pareto | [`pareto.md`](pareto.md) |
| Explicabilidad, semáforo y dashboard | [`explicabilidad.md`](explicabilidad.md) |
| Valor de la información y QUE_HACER_AHORA | [`valor_informacion.md`](valor_informacion.md) |

## 1. Cadena y universos

```
alternativa (mapa de arquitecturas × escala/trayectoria | NO_INVERTIR_AUN)
  → construir_entrada()  [21: consume 19, 20, 04, 23, 02]
  → aplicar_shocks()     [copia profunda; la base no se toca]
  → simular() + resultados(R, calcular_tir=…)   [21]
  → métricas → restricciones → comparabilidad → robustez → score ordinal → ranking → decisión → explicación
```

| Universo | `AMBITO` | Entradas | Shocks | Etiqueta | Uso |
|---|---|---|---|---|---|
| EVIDENCIA | PROYECTO | modo EVIDENCIA del motor (umbral E1–E3) | **prohibidos** (error) | `MODO_EVIDENCIA` | Sin VAN publicable: `OPTIMIZACION_REAL_NO_DISPONIBLE` y ranking de bloqueos |
| ESCENARIO | PROYECTO | modo ESCENARIO con [`escenario_optimizador.json`](escenario_optimizador.json) | sí | `SIMULACION_HIPOTETICA_NO_VALIDADA` | "Mejor" = mejor **dentro del escenario**, nunca recomendación del proyecto |
| ARTIFICIAL_TEST | ARTIFICIAL_TEST | alternativas `ART-*` armadas con `mf.caso_prueba()` | sí | `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO` | Probar la maquinaria; salidas en [`casos_prueba/`](casos_prueba/) |

Una corrida contiene un solo universo (`correr_universo` rechaza mezclas). Los archivos del proyecto juntan EVIDENCIA y ESCENARIO con las columnas `UNIVERSO` y `AMBITO`; los rankings son siempre internos a cada universo.

## 2. Variables de riesgo y shocks

[`registro_variables_riesgo.csv`](registro_variables_riesgo.csv) lista 59 variables (comerciales, operativas, costos, inversión, financieras, estratégicas). Cada una declara el campo de la entrada del motor que toca y su soporte:

| Soporte | Significado | Ejemplos |
|---|---|---|
| SOPORTADA | el motor tiene el campo; el shock lo modifica | precios por grupo, demanda (`stress.demanda`), días de cobro/pago, utilización (curva, tope 100 %), rubros de OPEX por driver, CAPEX (`stress.capex`), CAPEX por clase de activo, tasas, ganancias, IIBB, ramp-up |
| APROXIMACION | transformación declarada | peso vivo (SUP-20-04), FCR (SUP-20-05), rendimiento de faena (SUP-20-06) |
| REQUIERE_BASE | necesita valor base en `base_valores` | mortalidad, condenas, FX (traslado a precios ARS) |
| DISCRETA | se evalúa como stress o alternativa | mix, canal, exportación, halal, integrados, proveedor de alimento, façon, financiamiento, terreno/utilities |
| NO_SOPORTADA_POR_INTERFAZ | el motor no tiene el campo: se informa, no se simula | días operativos (DPV-20-01), recupero de IVA (DPV-20-02) |

- **Tipos de shock:** RELATIVO (× (1 + s)), ABSOLUTO_DIAS (+ s días), ABSOLUTO_MESES (+ s meses). Grillas en [`inputs_riesgo_optimizacion.csv`](inputs_riesgo_optimizacion.csv); **no implican probabilidad**.
- **Rubros por driver:** prefijo de `COSTO_ID` de 20_opex (ALI-, POL-, UT-ELE-, LAB-, EMP-, LOG-, FAE-FACON…), luego `GRUPO_PROVEEDOR`; el usuario puede declarar `driver_riesgo` (SUP-20-19).
- **Resultados de un shock:** OK, `NO_APLICA`, `NO_CALCULABLE`, `SHOCK_INVALIDO`; base 0 con shock relativo → `BASE_CERO_SIN_EFECTO`; tope físico → `TOPE_…`.

## 3. Performance sin parches globales

- Caché por (alternativa, universo, shocks, **modo**): un pedido rápido nunca devuelve una TIR no solicitada; la base de cada alternativa se construye una vez.
- **Modo rápido = interfaz explícita del motor** `resultados(R, calcular_tir=False)` (cambio mínimo de interfaz/performance en 21, sin cambio de lógica financiera). La TIR del motor (barrido de 4.000 puntos) es ~97 % del tiempo de una corrida. Con `calcular_tir=False` la TIR y la TIR del accionista quedan `None` con estado **`NO_CALCULADA`** (≠ 0, ≠ faltante de datos) y `PUBLICABLE_TIR = FALSE` con motivo `NO_CALCULADA`; todo lo demás es idéntico (tests AUD-01…05). El default `True` reproduce exactamente las salidas de la sesión 19 (las 10 tablas de 21 regeneradas sin diferencias).
- No se reemplaza ninguna función global (la versión inicial sustituía `mf.tir` temporalmente; se eliminó en la auditoría): evaluadores concurrentes, excepciones o futuras sesiones de app no se afectan entre sí (AUD-03, AUD-04).
- Búsqueda exhaustiva sobre un espacio discreto pequeño; grilla + bisección para lo continuo; semilla declarada. `resumen_corrida.csv` registra evaluaciones, aciertos de caché, semilla y hash de inputs.

## 4. Tests y mutaciones

- [`tests_riesgo_optimizador.py`](tests_riesgo_optimizador.py): grupos SENS (sensibilidad), RIE (riesgo), MC (Monte Carlo), OPT (optimizador), COMP (comparabilidad), QUI (puntos de quiebre) y AUD (auditoría final: interfaz rápida, frecuencia ≠ probabilidad, score ordinal, espacio, status quo, 0 estructural, rótulos artificiales, tipos de probabilidad, empates, comparabilidad, Pareto trivial, robustez, explicabilidad).
- Mutaciones R01–R27 (incluyen M02 y M11 del motor). La tabla [`cobertura_mutaciones.csv`](cobertura_mutaciones.csv) (generada por `--mutaciones`) indica, para cada mutación, si fue exigida por el encargo, qué tests la detectan y el resultado.

## 5. Limitaciones conocidas

1. Las transiciones de arquitectura (C0 → C1 → …) no existen en 19/20/21: las trayectorias expanden la **misma** configuración.
2. 1.450 combinaciones físicamente posibles no están modeladas económicamente y no se evalúan (DPV-20-03).
3. La exposición cambiaria solo se modela en ítems con `moneda_original = ARS` (DPV-20-04).
4. Mortalidad: semántica del motor (encarece el pollito por ave faenada).
5. Peso vivo, FCR y rendimiento: aproximaciones lineales declaradas.
6. El SCORE_ORDINAL_RIESGO y la normalización min–max son **relativos** al conjunto evaluado.
