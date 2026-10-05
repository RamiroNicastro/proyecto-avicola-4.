# Metodología — optimizador

**Fecha:** 2026-10-05 · Código: [`modelo_optimizador.py`](modelo_optimizador.py) · Marco general: [`metodologia_riesgo.md`](metodologia_riesgo.md)

## 1. Espacio de decisiones: 2.592 combinaciones vs 54 alternativas

[`espacio_decisiones.csv`](espacio_decisiones.csv) enumera las **2.592** combinaciones de atributos = faena (2) × granjas (3) × pollito (2) × alimento (3) × flota (3) × frío (3) × subproductos (2) × rendering (2) × reproductoras (2), cada una con `ID_COMBINACION` único, clasificada con `validar_config()` de 19:

| Clasificación | Cantidad | Qué significa | ¿Se evalúa? |
|---|---|---|---|
| `FISICAMENTE_INVALIDA` | 1.134 | CAPEX la rechaza (p. ej. rendering sin faena propia; reproductoras sin incubación); motivo informado | No |
| `FISICAMENTE_POSIBLE_NO_MODELADA_ECONOMICAMENTE` | 1.450 | CAPEX la acepta, pero no está en el mapa de arquitecturas: no hay CAPEX/OPEX modelado y **no se inventa** | No (DEC-103) |
| `HABILITADA_EN_MAPA_PARA_EVALUACION` | 8 | coincide con configuraciones del mapa | Sí → genera las alternativas económicas |

Las 8 combinaciones habilitadas agrupan las 24 filas del mapa (5 bases + 19 variantes; varias variantes comparten atributos con su base y difieren en automatización, terreno, días, halal, etc.). Las **alternativas económicas** salen de las filas del mapa, no de las combinaciones:

```
54 = 5 configuraciones base × 4 escalas (2.500, 5.000, 10.000, 20.000)          = 20
   + 19 variantes × 1 escala de referencia (10.000)                              = 19
   + 5 configuraciones base × 3 trayectorias multietapa (T1, T2, T3 de 21)       = 15
   (+ NO_INVERTIR_AUN, alternativa de decisión, no productiva → 55 filas)
```

Por combinación: COMB-0001 (C1 + 13 variantes) 20 · COMB-1385 (C0 + B1 + B2) 9 · COMB-0993 (C2 + B1) 8 · COMB-0829 (C3) 7 · COMB-0832 (CF) 7 · COMB-0005, -0009, -0017 (variantes de subproductos y frío de C1) 1 c/u = 54 (columna `ALTERNATIVAS_ECONOMICAS`). ID de alternativa: `CONFIGURACION|VARIANTE|ESCALAS|TRAYECTORIA` (único; test OPT-15). C0 (faena a façon) se tipifica `OPERAR_ASSET_LIGHT`. Las escalas (`espacio.escalas`) admiten intermedias dentro de 2.500–20.000. Tests OPT-15, AUD-08.

## 2. Factibilidad (cuatro dimensiones separadas)

| Dimensión | Estados | Fuente |
|---|---|---|
| FÍSICA | FACTIBLE / NO_FACTIBLE / FACTIBILIDAD_PENDIENTE | gates con **requerimiento** de los drivers de 19 (terreno, agua, potencia, capacidad de línea, m² de galpón, pollitos/semana, alimento t/semana) y **disponibilidad** declarada (`disponibilidad` del JSON). Sin dato → PENDIENTE, nunca FACTIBLE |
| ECONÓMICA | COSTEABLE / NO_COSTEABLE (CAPEX, OPEX) | bloques CAPEX y OPEX del motor |
| FINANCIERA | SÍ / NO / PENDIENTE / SIN_RESTRICCION_FINANCIERA_DECLARADA | restricciones de capital, DSCR y deuda |
| COMERCIAL | RESPALDADO / PARCIAL / NO_RESPALDADO | % de la capacidad con demanda DOCUMENTADA/ASEGURADA |

**0 estructural ≠ desconocido** (`ESTADO_REQUERIMIENTO` de cada gate): `DIMENSIONADO` (valor de los drivers), `NO_REQUERIDO_POR_ARQUITECTURA` (la arquitectura no tiene el activo: requerimiento 0 y gate NO_APLICA) o `DESCONOCIDO` (no dimensionado: nunca 0). En **C0**, la planta de faena, su terreno industrial, frío y utilities no son de la empresa (NO_REQUERIDO para ese componente), pero la oficina/IT/estructura del CAPEX de C0 —y frío, flota, alimento, granjas, incubación o subproductos propios si una variante los tuviera— no tienen requerimiento dimensionado: TERRENO, AGUA y POTENCIA quedan `DESCONOCIDO` / PENDIENTE (una restricción de agua sobre C0 es NO_EVALUABLE, no CUMPLE). Solo el caso artificial `ART-ASSET-LIGHT`, que declara no tener módulos propios, usa 0 estructural (SUP-227; test AUD-10; mutación R22).

## 3. Comparabilidad y confianza

`COMPARABILIDAD = FALSE` si difieren universo, horizonte, modelo real/nominal, base de la tasa, convención, tipo y valor de la tasa, moneda, base de flujo (pre/after-tax), tratamiento fiscal o definición de producto, o si **faltan bloques económicos** (VAN no publicable). `PARCIAL` si solo difiere la cobertura de evidencia (se rankea, declarado). `NO_APLICA` para NO_INVERTIR_AUN. Una alternativa FALSE no participa en rankings, dominancia ni Pareto (aparece como `NO_EVALUABLE`): un CAPEX/OPEX/precio faltante nunca se interpreta como 0 (tests COMP-02, AUD-14; mutaciones R12, R13, R27).

`COBERTURA_EVIDENCIA` = bloques del motor completos en **modo evidencia** ÷ 17 para la misma configuración y escala: mide confianza, no rentabilidad (SUP-228).

## 4. Semáforo (sin cortes económicos)

GRIS = no evaluable (incompleta, no comparable o status quo). ROJO = incumple una HARD o un gate físico. VERDE = cumple todo, gates FACTIBLES y cobertura de evidencia 100 %. AMARILLO = evaluable y sin incumplimientos, pero con datos o gates pendientes.

## 5. NO_INVERTIR_AUN (status quo)

Es una **alternativa de decisión**, no un proyecto productivo: no tiene VAN, TIR, payback, CAPEX, EBITDA ni robustez propios (todo `None`, estados `NO_APLICA_STATUS_QUO`); no se le asignan ceros que la harían ganar MIN_CAPEX o MIN_PAYBACK, ni TIR infinita (SUP-214, revisado). No entra a ningún ranking, ni a dominancia ni a Pareto. Después del ranking de inversiones, `DECISION_ESCENARIO` es la mejor inversión o NO_INVERTIR_AUN según reglas explícitas (`REGLAS_STATUS_QUO`):

| Regla | Gana NO_INVERTIR_AUN si… | Activación |
|---|---|---|
| SQ-1 | ninguna inversión cumple las condiciones de ranking (`NINGUNA_CONFIGURACION_FACTIBLE`) | siempre |
| SQ-2 | el capital declarado excluye a todas las inversiones restantes | siempre (si hay restricción de capital) |
| SQ-3 | la mejor inversión tiene VAN < 0 en el escenario | siempre |
| SQ-4 | la mejor inversión tiene VAN < 0 en un stress listado en `decision.sq_stress` | input del usuario |
| SQ-5 | su SCORE_ORDINAL_RIESGO supera `decision.sq_score_ordinal_max` | input del usuario |
| SQ-6 | su cobertura de evidencia es menor que `decision.sq_cobertura_min` | input del usuario |

Además, `POR_QUE_NO_INVERTIR_PODRIA_GANAR` lista las condiciones presentes aunque su regla no esté activada (stress con VAN < 0, cobertura < 100 %). En el universo EVIDENCIA sin VAN publicable no hay decisión: `OPTIMIZACION_REAL_NO_DISPONIBLE`. Tests OPT-05, OPT-06, AUD-09; mutaciones R05, R24.

## 6. Universos sin alternativas completas

`OPTIMIZACION_REAL_NO_DISPONIBLE` (evidencia) o `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO` (escenario): no equivalen a `NINGUNA_CONFIGURACION_FACTIBLE` (que exige alternativas evaluables que no cumplen).
