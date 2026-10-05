# Metodología — riesgos, sensibilidades y optimizador

**Fecha:** 2026-10-05 · **Sesión:** 20 · Código: [`motor_riesgo.py`](motor_riesgo.py), [`modelo_optimizador.py`](modelo_optimizador.py) · Tests: [`tests_riesgo_optimizador.py`](tests_riesgo_optimizador.py)

Todo número económico sale del motor de la sesión 19 ([`../21_modelo_financiero/modelo_financiero.py`](../21_modelo_financiero/modelo_financiero.py)). Esta capa solo (a) arma entradas, (b) les aplica shocks, (c) llama al motor y (d) compara resultados. No contiene fórmulas de ingresos, costos, flujo, VAN, TIR ni payback.

## 1. Cadena y universos

```
alternativa (mapa de arquitecturas × escala/trayectoria | NO_INVERTIR_AUN)
  → construir_entrada()  [21: consume 19, 20, 04, 23, 02]
  → aplicar_shocks()     [copia profunda; la base no se toca]
  → simular() + resultados()   [21]
  → métricas → restricciones → comparabilidad → robustez → score → ranking → explicación
```

| Universo | Entradas | Shocks | Etiqueta | Uso |
|---|---|---|---|---|
| EVIDENCIA | modo EVIDENCIA del motor (umbral E1–E3 de `inputs_financieros.csv`) | **prohibidos** (error) | `MODO_EVIDENCIA` | Si no hay VAN publicable: `OPTIMIZACION_REAL_NO_DISPONIBLE` y ranking de bloqueos |
| ESCENARIO | modo ESCENARIO con [`escenario_optimizador.json`](escenario_optimizador.json) | sí | `SIMULACION_HIPOTETICA_NO_VALIDADA` | "Mejor" = mejor **dentro del escenario**, nunca recomendación del proyecto |
| CASO_ARTIFICIAL | alternativas `ART-*` armadas con `mf.caso_prueba()` | sí | `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO` | Probar la maquinaria; salidas en `casos_prueba/` |

Una corrida contiene un solo universo (`correr_universo` rechaza mezclas). Los archivos del proyecto juntan EVIDENCIA y ESCENARIO con la columna `UNIVERSO`; los rankings son siempre internos a cada universo.

## 2. Registro y matriz de riesgos

- [`registro_riesgos.csv`](registro_riesgos.csv): 34 riesgos con los campos pedidos más `ESTADO_MITIGACION`, `PROBABILIDAD_RESIDUAL`, `IMPACTO_RESIDUAL`. Niveles admitidos: **BAJA / MEDIA / ALTA / PENDIENTE**; un número en esas columnas es error de lectura.
- **Probabilidad:** solo cuando existe una clasificación documentada; hoy proviene de la tabla de amenazas de [`../01_mercado/mercado_avicola_argentina.md`](../01_mercado/mercado_avicola_argentina.md) §11 (frecuencia **sectorial**, fuentes de sector y prensa, parte `[PVDP]`). No es la probabilidad del proyecto. "Media–alta" y "Medio–alto" se redondean a ALTA (criterio conservador, SUP-20-13). Sin clasificación → PENDIENTE.
- **Impacto:** clasificación de 01 §11 cuando existe; en el resto, `[ESTIMACIÓN]` cualitativa según el bloque del motor que el driver bloquea o mueve (p. ej. sin demanda no hay ingresos publicables). VELOCIDAD, CONTROLABILIDAD y DETECTABILIDAD son estimaciones cualitativas revisables (SUP-20-18).
- **Matriz** ([`matriz_riesgos.csv`](matriz_riesgos.csv)): celda `P×I` y clase por tabla 3×3 de etiquetas (BAJO / MODERADO / ALTO / CRÍTICO; SUP-20-14). **No se multiplica** P × I ni se asigna probabilidad numérica (`PROB_NUMERICA`, `IMPACTO_USD`, `EXPOSICION_USD` vacíos: cuantificación futura con distribución respaldada).
- **Inherente vs residual:** el residual solo difiere del inherente si `ESTADO_MITIGACION = IMPLEMENTADA_CON_EVIDENCIA`; una mitigación PROPUESTA o EN_CURSO deja residual = inherente. El inherente nunca se modifica.
- `SWING_VAN_SIMULADO`: cuando exista un escenario completo, la amplitud del VAN de los drivers del riesgo (tornado) se agrega como referencia simulada.

## 3. Variables de riesgo y shocks

[`registro_variables_riesgo.csv`](registro_variables_riesgo.csv) lista 59 variables (comerciales, operativas, costos, inversión, financieras, estratégicas). Cada una declara el campo de la entrada del motor que toca y su soporte:

| Soporte | Significado | Ejemplos |
|---|---|---|
| SOPORTADA | el motor tiene el campo; el shock lo modifica | precios por grupo, demanda (`stress.demanda`), días de cobro/pago, utilización (curva, tope 100 %), rubros de OPEX por driver, CAPEX (`stress.capex`), CAPEX por clase de activo, tasa de descuento, tasa y plazo de deuda, ganancias, IIBB, ramp-up |
| APROXIMACION | transformación declarada | peso vivo (kg/ave y alimento ∝ peso, SUP-20-04), FCR (alimento ∝ FCR, SUP-20-05), rendimiento de faena (la masa extra sale de subproductos, SUP-20-06) |
| REQUIERE_BASE | necesita valor base declarado en `base_valores` | mortalidad (stress del motor sobre pollito), condenas, FX (traslado a precios ARS) |
| DISCRETA | se evalúa como stress o alternativa | mix, canal, exportación disponible, halal, integrados, proveedor de alimento, façon, financiamiento, terreno/utilities |
| NO_SOPORTADA_POR_INTERFAZ | el motor no tiene el campo: se informa, no se simula | días operativos (romperían la coherencia costo/capacidad: se evalúan con la variante C1-6dias, DPV-20-01), recupero de IVA (DPV-20-02) |

- **Tipos de shock:** RELATIVO (× (1 + s)), ABSOLUTO_DIAS (+ s días), ABSOLUTO_MESES (+ s meses, múltiplo de la frecuencia de la deuda). Grillas en [`inputs_riesgo_optimizacion.csv`](inputs_riesgo_optimizacion.csv); **no implican probabilidad**.
- **Rubros por driver:** por prefijo de `COSTO_ID` del registro de 20_opex (ALI-, POL-, UT-ELE-, LAB-, EMP-, LOG-, FAE-FACON…) y, si no hay prefijo, por `GRUPO_PROVEEDOR`; un rubro del usuario puede declarar `driver_riesgo`. Maíz y soja son subconjuntos de alimento.
- **Resultados de un shock:** OK, `NO_APLICA` (la variable no existe en el escenario: sin deuda no hay tasa de deuda), `NO_CALCULABLE` (falta el valor base), `SHOCK_INVALIDO` (precio ≤ 0, mortalidad ≥ 100 %, rendimiento mayor que la masa del ave). Base 0 con shock relativo → `BASE_CERO_SIN_EFECTO`; tope físico → `TOPE_…`.

## 4. Sensibilidad, tornado, 2D y stress

- **One-way:** una variable por vez; todas las demás iguales. Métricas: ingresos, EBITDA, margen, FCFF total, fondos iniciales, pico de fondos, VAN, TIR, payback, break-even, DSCR, utilización y CT. Una métrica que la base no publica queda vacía en todas las filas.
- **Tornado:** por métrica elegida (`tornado.metricas`, default VAN); orden por **amplitud** = máximo − mínimo entre los shocks evaluados (no por impacto con signo). Sin métrica en la base → `NO_CALCULABLE`, sin ranking.
- **2D:** grilla completa de dos variables; zonas de VAN y EBITDA por signo; DSCR y payback solo con umbral declarado (`SIN_UMBRAL_DECLARADO` si falta).
- **Stress** ([`escenarios_stress.csv`](escenarios_stress.csv)): varias variables a la vez. Las magnitudes de los stress de demanda, alimento, precio, CAPEX y ramp-up son las plantillas `STRESS_PREDEFINIDOS` de 21 (ilustrativas, SUP-20-12); el stress financiero queda `NO_EJECUTADO_VALORES_PENDIENTES` hasta que se declaren sus magnitudes.

## 5. Puntos de quiebre

Para la métrica M y el objetivo m* (default VAN = 0): grilla uniforme en el rango de la variable (incluye s = 0) → intervalos con cambio de signo de M − m* → bisección (tolerancia 1e-7) sobre el cruce más cercano a la base. Varios cruces → `MULTIPLES_CRUCES` (se informa el más cercano). Estados: `ENCONTRADO`, `NO_ENCONTRADO_EN_RANGO` (la métrica existe pero no cruza), `NO_CALCULABLE` (no hay métrica en la base o falta el valor base), `VARIABLE_NO_APLICA`. Para umbrales no continuos (payback ≤ X, que puede ser NO_RECUPERADO) se busca el borde del predicado. La tasa de deuda se evalúa sobre `VAN_ACCIONISTA` (el FCFF no depende de ella). Validado contra soluciones manuales (tests QUI-01…06).

## 6. Monte Carlo y correlaciones

- [`distribuciones_riesgo.csv`](distribuciones_riesgo.csv): `DISTRIBUCION`, `PARAMETROS` (en la unidad del shock), `FUENTE`, `ESTADO` (PENDIENTE / RESPALDADA / ARTIFICIAL). Tipos: triangular, normal truncada, uniforme, lognormal, discreta, determinista, empírica.
- Muestreo por **inversa de la CDF** a partir de uniformes; con correlaciones declaradas, **cópula gaussiana** (Cholesky de la matriz; matriz no definida positiva → error).
- [`correlaciones_riesgo.csv`](correlaciones_riesgo.csv): 9 pares con relación evidente (pollo/alimento, maíz/soja, FX/costos, demanda/precio, utilización/eficiencia, inflación–FX/salarios y tarifas) **sin coeficiente**. Un Monte Carlo con un par pendiente queda rotulado `CORRELACIONES_NO_MODELADAS` con los pares; nunca se asume independencia en silencio.
- **Proyecto:** exige todas las distribuciones usadas RESPALDADAS → hoy `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES`. Distribuciones ARTIFICIALES solo en casos artificiales.
- Resultados: media, mediana, P5/P10/P50/P90/P95 (interpolación lineal) de VAN, TIR (si se pide), pico de fondos, DSCR y payback; P(VAN < 0); P(déficit) = P(pico > capital declarado) o, sin capital, P(caja del accionista < 0); P(no recupero). Todas rotuladas `PROBABILIDAD_SIMULADA_NO_HISTORICA`. Semilla obligatoria.

## 7. Optimizador

### 7.1 Espacio de decisiones
- Alternativas evaluadas = filas del mapa: {C0, C1, C2, C3, CF} × escalas (`espacio.escalas`, 2.500–20.000; intermedias admitidas) + 19 variantes a su escala de referencia + trayectorias multietapa de 21 (misma configuración por etapa) + **NO_INVERTIR_AUN**. C0 (faena a façon) se tipifica `OPERAR_ASSET_LIGHT`. Hoy: 54 + 1.
- [`espacio_decisiones.csv`](espacio_decisiones.csv) enumera las 2.592 combinaciones de faena × granjas × pollito × alimento × flota × frío × subproductos × rendering × reproductoras y las clasifica con `validar_config()` de 19: `EN_MAPA_EVALUADA`, `VALIDA_NO_MAPEADA_NO_EVALUADA` (la interfaz financiera solo consume el mapa; DPV-20-03) o `INVALIDA_FISICAMENTE` (con el motivo). Nada imposible se evalúa; nada se descarta en silencio.

### 7.2 Factibilidad (cuatro dimensiones separadas)
| Dimensión | Estados | Fuente |
|---|---|---|
| FÍSICA | FACTIBLE / NO_FACTIBLE / FACTIBILIDAD_PENDIENTE | gates con **requerimiento** de los drivers de 19 (terreno, agua, potencia, capacidad de línea, m² de galpón de integrados, pollitos/semana, alimento t/semana) y **disponibilidad** declarada (`disponibilidad` del JSON). Sin dato → PENDIENTE, nunca FACTIBLE |
| ECONÓMICA | COSTEABLE / NO_COSTEABLE (CAPEX, OPEX) | bloques CAPEX y OPEX del motor |
| FINANCIERA | SÍ / NO / PENDIENTE / SIN_RESTRICCION_FINANCIERA_DECLARADA | restricciones de capital, DSCR y deuda |
| COMERCIAL | RESPALDADO / PARCIAL / NO_RESPALDADO | % de la capacidad cubierta por demanda DOCUMENTADA/ASEGURADA |

Asset-light: terreno, agua y potencia propios requeridos = 0 (SUP-20-16).

### 7.3 Restricciones
Todas opcionales (vacío = no hay). **HARD** excluye del ranking; **SOFT** resta `penalización × violación relativa` al score (sin penalización declarada → error). Una HARD no evaluable (dato faltante) excluye por defecto (SUP-20-09). `CAPITAL_DISPONIBLE` se compara con el **pico de fondos** (incluye pérdidas del ramp-up y CT; SUP-20-10). Nunca se asume USD 2 M.

### 7.4 Comparabilidad y confianza
`COMPARABILIDAD = FALSE` si difieren universo, horizonte, modelo real/nominal, base de la tasa, convención, tipo y valor de la tasa, moneda, base de flujo (pre/after-tax), tratamiento fiscal o definición de producto, o si **faltan bloques económicos** (VAN no publicable). `PARCIAL` si solo difiere la cobertura de evidencia (se rankea, declarado). La referencia es la firma más frecuente entre las alternativas completas.
`COBERTURA_EVIDENCIA` = bloques del motor completos en **modo evidencia** ÷ 17 para la misma configuración y escala: mide confianza, no rentabilidad (SUP-20-17).

### 7.5 Robustez y score de riesgo
- **Robustez** = comportamiento en un conjunto de escenarios deterministas: stress activos + extremos (mín y máx) de `robustez.variables` (SUP-20-15). Indicadores: % de escenarios con VAN ≥ 0, peor VAN, P10 del VAN (si hay Monte Carlo), máximo pico, máximo payback, # no recuperados, % de escenarios que cumplen las HARD. Criterio para rankear: `robustez.criterio`. Menos escenarios que `robustez.min_escenarios` → PENDIENTE.
- **Score de riesgo** (operativo, para ordenar; **no es probabilidad**): Σ wᵢ·cᵢ ÷ Σ wᵢ con componentes en [0, 1]: VAN negativo en escenarios, sensibilidad del VAN (amplitud ÷ (|VAN| + amplitud)), pico de fondos relativo (min–max dentro del conjunto), demanda no respaldada, gates físicos pendientes, evidencia faltante. Sin pesos → PENDIENTE. Componente faltante: SEPARAR (score PENDIENTE) o PENALIZAR (= 1) (SUP-20-11).

### 7.6 Objetivos y ranking
MAX_VAN, MAX_TIR, MIN_PAYBACK, MIN_FONDOS_INICIALES, MIN_CAPEX, MIN_PICO_FONDOS, MAX_EBITDA, MAX_DSCR, MIN_RIESGO, MAX_ROBUSTEZ, MAX_CRECIMIENTO (capacidad final alcanzada) y BALANCEADO. `TODOS` (default) = un ranking por objetivo; **ninguno es "el" criterio**.
- Conjunto rankeable: mismo universo, comparable, físicamente no infactible, sin HARD incumplidas ni pendientes, con la métrica del objetivo. Payback NO_RECUPERADO y TIR ambigua/inexistente se excluyen con el motivo.
- SCORE = valor normalizado min–max (mejor = 1) − penalizaciones SOFT.
- **BALANCEADO:** pesos de rentabilidad, riesgo, capital, liquidez, crecimiento y robustez, normalizados a 1; sin pesos → `PESOS_NO_DEFINIDOS`; preset `IGUALES` rotulado SUP-20-08.
- **NO_INVERTIR_AUN:** VAN, CAPEX, fondos, pico y EBITDA incrementales = 0 **por definición** (SUP-20-03). Compite en MAX_VAN, MAX_EBITDA y BALANCEADO; en MIN_FONDOS, MIN_CAPEX, MIN_PICO y MAX_ROBUSTEZ es `REFERENCIA_TRIVIAL`; en el resto `NO_APLICA`. Gana MAX_VAN si toda inversión tiene VAN < 0.
- Sin ninguna inversión rankeable → `NINGUNA_CONFIGURACION_FACTIBLE` con las causas contadas; no se elige "la menos mala". Sin alternativas completas: `OPTIMIZACION_REAL_NO_DISPONIBLE` (evidencia) o `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO` (escenario).
- **Segunda alternativa** y diferencia. `DECISION_NO_ROBUSTA` si (a) el ganador cambia en algún escenario de robustez (`ESTABILIDAD_GANADOR` < 1, con la lista), (b) la diferencia relativa ≤ `decision.tolerancia_equivalencia` (si se declara) o (c) empate.

### 7.7 Dominancia y Pareto
A domina a B (misma base comparable) si es igual o mejor en todas las dimensiones disponibles (default: fondos iniciales ↓, VAN ↑, score de riesgo ↓) y estrictamente mejor en al menos una; se requieren ≥ 2 dimensiones y se declaran las usadas. B se marca `DOMINADA_POR`, no se elimina. [`frontera_pareto.csv`](frontera_pareto.csv): por par de ejes (VAN × fondos, VAN × riesgo, VAN × pico, VAN × payback), `EN_FRONTERA` y quién la domina en el par. La frontera no es un ranking.

### 7.8 Consultas
- **Capital** (`consulta.capital_usd`): factibles, no factibles, capital faltante = requerido − X, principal restricción y mejor por objetivo con esa restricción.
- **Demanda** (`consulta.demanda_t_dia`): escala la demanda del escenario a X; utilización, capacidad ociosa, ratio capacidad/demanda, demanda mínima para VAN = 0 (punto de quiebre) y faltante; conclusión `FACON_ASSET_LIGHT_HASTA_VALIDAR_MAS_DEMANDA` si solo el asset-light tiene VAN ≥ 0.
- **Payback** (`consulta.payback_max_anios`): quién cumple y el cambio mínimo de precio, CAPEX, demanda o alimento que haría falta (informado, **no aplicado**).

### 7.9 Valor de la información y QUE_HACER_AHORA
- **Universo evidencia** ([`prioridad_validacion.csv`](prioridad_validacion.csv)): cada faltante de `disponibilidad()` del motor (desagregado por módulo de OPEX y por gate físico) se ordena por (indicadores publicables que bloquea según `DEPENDENCIAS_FLAG` de 21 ↓, alternativas que bloquea ↓, posición en la cadena). Es un ranking derivado del modelo, no una lista fija.
- **Universo escenario:** variables ordenadas por (¿pueden invertir el orden mejor/segunda o llevar el VAN de la mejor bajo 0? → amplitud del VAN → cercanía entre alternativas). Sin distribuciones no es VOI bayesiano.
- [`que_hacer_ahora.csv`](que_hacer_ahora.csv): acción por ítem (tabla de correspondencia ítem → acción), con DPV/DEC vinculados verificados contra `datos_por_validar.md` y `decisiones_pendientes.md`; ítems sin registro se marcan `NUEVA`.

### 7.10 Semáforo
GRIS = no evaluable (incompleta o no comparable). ROJO = incumple una HARD o un gate físico. VERDE = cumple todo, gates FACTIBLES y cobertura de evidencia 100 %. AMARILLO = evaluable y sin incumplimientos, pero con datos o gates pendientes. Sin cortes económicos arbitrarios.

## 8. Performance y reproducibilidad
- Caché por (alternativa, universo, shocks, con/sin TIR); entrada base de cada alternativa construida una vez; CAPEX/OPEX cacheados por el propio motor.
- **Evaluación rápida:** la TIR del motor (barrido de 4.000 puntos) es ~97 % del tiempo de una corrida; durante las corridas que no la necesitan `mf.tir` se sustituye por un aviso (`NO_CALCULADA_EVALUACION_RAPIDA`, nunca 0) y se restaura siempre (SUP-20-02). VAN, payback, pico, EBITDA y fondos son idénticos (test SENS-08). Las fichas base de cada alternativa usan la TIR completa.
- Búsqueda exhaustiva sobre un espacio discreto pequeño; grilla + bisección para lo continuo; semilla declarada. `resumen_corrida.csv` registra evaluaciones, aciertos de caché, semilla y hash de inputs.

## 9. Tests y mutaciones
Ver [`tests_riesgo_optimizador.py`](tests_riesgo_optimizador.py): sensibilidad (solo cambia la variable elegida, base intacta, evidencia intacta, monotonía, orden del tornado, 2D con ambos ejes), riesgo (pendiente ≠ 0, sin score estadístico, inherente ≠ residual, correlaciones señaladas), Monte Carlo (semilla, determinismo, percentiles, probabilidades, proyecto sin distribuciones), optimizador (nunca hard-infeasible, capital, demanda, payback, NINGUNA, NO_INVERTIR_AUN, dominancia, Pareto, segunda, reproducibilidad), comparabilidad (real/nominal, horizontes, incompleta no gana, E4 ≠ 0, escenario ≠ evidencia) y puntos de quiebre contra solución manual. Mutaciones R01–R19 (incluye M02 y M11 del motor).

## 10. Limitaciones conocidas
1. Las transiciones de arquitectura (C0 → C1 → …) no existen en 19/20/21: las trayectorias expanden la **misma** configuración.
2. 1.450 combinaciones físicamente válidas no están en el mapa y no pueden evaluarse (DPV-20-03).
3. La exposición cambiaria solo se modela en ítems con `moneda_original = ARS`; el adaptador OPEX de 21 no transporta `MONEDA_ORIGINAL` (DPV-20-04).
4. Mortalidad: semántica del motor (encarece el pollito por ave faenada; no el alimento consumido por aves muertas).
5. Peso vivo, FCR y rendimiento: aproximaciones lineales declaradas.
6. El score de riesgo y la normalización min–max son **relativos** al conjunto evaluado.
