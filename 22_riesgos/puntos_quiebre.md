# Puntos de quiebre

**Fecha:** 2026-10-05 · Código: `punto_quiebre()` en [`motor_riesgo.py`](motor_riesgo.py) · Salida: [`puntos_quiebre.csv`](puntos_quiebre.csv)

## 1. Método

Para la métrica M y el objetivo m* (default VAN = 0): grilla uniforme en el rango de la variable (incluye s = 0) → intervalos con cambio de signo de M − m* → bisección (tolerancia 1e-7) sobre el cruce más cercano a la base. Varios cruces → `MULTIPLES_CRUCES` (se informa el más cercano). Para umbrales no continuos (payback ≤ X, que puede ser NO_RECUPERADO) se busca el borde del predicado. La tasa de deuda se evalúa sobre `VAN_ACCIONISTA` (el FCFF no depende de ella).

| Estado | Significado |
|---|---|
| `ENCONTRADO` | hay cruce; se informa el shock, el factor (relativos) y el valor absoluto si hay base declarada |
| `NO_ENCONTRADO_EN_RANGO` | la métrica existe pero no cruza el objetivo en el rango |
| `NO_CALCULABLE` | no hay métrica en la base o falta el valor base (p. ej. mortalidad sin base) |
| `VARIABLE_NO_APLICA` | la variable no existe en el escenario (p. ej. sin deuda) |

Variables por defecto: precio de venta, alimento, demanda, utilización, CAPEX, días de cobro, tasa de deuda, mortalidad, FCR y tasa de descuento.

## 2. Validación contra solución manual — `AMBITO = ARTIFICIAL_TEST`

Los siguientes valores son de un **caso de prueba artificial** (CAPEX 100 en T0, ventas 100/año, OPEX 60/año, 5 años, tasa 10 %, flujos anuales). **No son umbrales del proyecto avícola**; solo prueban que el método reproduce la solución calculada a mano (tests QUI-01…06).

| Caso (ARTIFICIAL_TEST) | Solución manual | Test |
|---|---|---|
| Precio que lleva el VAN a 0 | factor (60 + 26,3797) ÷ 100 = 0,8638 | QUI-01 |
| Utilización con OPEX fijo 40 y variable 20 | (40 + 26,3797) ÷ 80 = 0,8297 | QUI-02 |
| CAPEX máximo | 40 × 3,7908 = 151,63 (factor 1,5163) | QUI-03 |
| Alimento máximo (= FCR máximo) | (60 − 26,3797) ÷ 20 = 1,6810 | QUI-04 |
| Días de cobro máximos / tasa máxima | 207,3 días / tasa = TIR del motor | QUI-05 |
| Mortalidad máxima (pollito único variable) | 1 − 0,95 ÷ 1,6810 | QUI-06 |

## 3. Estado en el proyecto

`puntos_quiebre.csv` del proyecto: NO_CALCULABLE (ninguna alternativa completa); ningún `ENCONTRADO` (test AUD-11). Los puntos de quiebre de [`casos_prueba/`](casos_prueba/) llevan `AMBITO = ARTIFICIAL_TEST` y alternativas `ART-*`.
