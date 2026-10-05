# Expansión por fases: trayectorias, gatillos y CAPEX por etapa

**Fecha:** 2026-10-04 · Código: `capex_trayectoria()`, etapas y gatillos de `simular()` · Lógica física de CAPEX: [`../19_capex/expansion_capex.md`](../19_capex/expansion_capex.md) · Gates físicos: [`../23_plan_expansion/gates_expansion.md`](../23_plan_expansion/gates_expansion.md)

> **No se supone que crecer por fases sea mejor** ni se elige trayectoria o gatillo (DEC-033, DEC-035, DEC-034 abiertas).

## 0. Alcance real (auditoría 2026-10-05)

| Pregunta | Respuesta |
|---|---|
| ¿Por qué las corridas de referencia de trayectorias son solo de C1? | **A) Limitación deliberada de las corridas actuales: `LIMITACION_ACTUAL_EXPANSION_C1`.** Se eligió C1 como única configuración de referencia para mostrar la estructura sin multiplicar corridas incompletas (todo el CAPEX por etapa está PENDIENTE) |
| ¿El motor puede aplicar una trayectoria de escala a otra configuración? | **B) Sí, pero solo a la MISMA configuración base que crece en escala** (C0, C1, C2, C3 o CF): `capex_trayectoria(cfg, escalas)` usa `expansion()` de 19_capex con `preset(cfg)` (test EX01 lo verifica con C3). Las **variantes** se evalúan a escala única (SUP-208) |
| ¿Puede pasar de una arquitectura a otra (C0→C1→C2→C3)? | **No.** No existe CAPEX ni OPEX de transición entre arquitecturas en 19/20, y no se inventa. La interfaz `configuracion_por_fase` está preparada (una configuración por etapa; queda registrada en cada etapa), pero cualquier valor distinto de la configuración inicial se rechaza con `TRANSICION_DE_ARQUITECTURA_NO_MODELADA` (test EX01) |

Por eso este módulo **no** debe presentarse como expansión genérica de cualquier arquitectura: es expansión de escala dentro de una misma configuración base. Cada corrida multietapa lleva `ALCANCE_EXPANSION` en [`escenarios_financieros.csv`](escenarios_financieros.csv).

## 1. Trayectorias evaluables

| ID | Escalas (aves/día operativo) | Etapas |
|---|---|---|
| `T1_2500_5000_10000_20000` | 2.500 → 5.000 → 10.000 → 20.000 | 1 inicial + 3 expansiones |
| `T2_5000_10000_20000` | 5.000 → 10.000 → 20.000 | 1 + 2 |
| `T3_10000_20000` | 10.000 → 20.000 | 1 + 1 |
| `T4_20000_inicial` | 20.000 | solo inicial |

El CAPEX de cada etapa sale de `expansion()` de 19_capex (acciones REUTILIZA / AMPLIA / DUPLICA / REEMPLAZA / NUEVO por etiqueta de activo): el financiero le pasa la trayectoria pedida y restaura el módulo (no lo modifica; test N20). Las trayectorias solo existen para las **configuraciones base** (SUP-208): `expansion()` parte de `preset()`.

## 2. Estado actual del CAPEX por etapa (C1, MODO EVIDENCIA)

| Trayectoria | Etapa | Escala | Tipo | Conceptos sin costo en la etapa | ¿CAPEX publicable? |
|---|---|---|---|---|---|
| T1 | 1 | 2.500 | INICIAL | 75 | No |
| T1 | 2 | 5.000 | EXPANSION | 72 | No |
| T1 | 3 | 10.000 | EXPANSION | 73 | No |
| T1 | 4 | 20.000 | EXPANSION | 73 | No |
| T2 | 1 / 2 / 3 | 5.000 / 10.000 / 20.000 | INICIAL / EXP / EXP | 75 / 73 / 73 | No |
| T3 | 1 / 2 | 10.000 / 20.000 | INICIAL / EXP | 75 / 73 | No |

Los montos "con precio" de cada etapa son referencias E4 parciales (1–2 conceptos) y **no** se usan. Además falta la prima o penalidad de ampliar una planta en operación (DPV-086) y el valor residual de lo que se reemplaza (DPV-167). T18-13: partir de 5.000 implica reemplazar ≈ 39 equipos al llegar a 20.000 según niveles de automatización hipotéticos.

## 3. Tres tipos de CAPEX, separados

| Tipo | Origen | Columna |
|---|---|---|
| Inicial | Etapa 1: curva de desembolso relativa a su entrada | `CAPEX_INICIAL` |
| Expansión | Etapas 2…n: curva relativa a su entrada (o al gatillo) | `CAPEX_EXPANSION` |
| Reposición | Fin de vida útil de cada activo con `costo_reemplazo_usd` | `CAPEX_REPOSICION` |

## 4. Entrada de una expansión: por fecha o por condición

| Tipo | Regla |
|---|---|
| `FECHA` | `entrada.mes` = primer mes de operación de la etapa (posterior al inicio de la inicial) |
| `CONDICION` | Se evalúan los gatillos al cierre de cada mes con datos hasta ese mes; si se cumplen (todos o alguno, `logica`), la etapa entra `meses_obra + 1` meses después; la curva de desembolso no puede empezar antes del gatillo |

Gatillos preparados (ninguno elegido): `utilizacion_min` (con `meses_consecutivos`), `demanda_asegurada_min` (aves de demanda DOCUMENTADA/ASEGURADA ÷ capacidad), `factor_demanda_capacidad_min`, `caja_min_usd`, `dscr_min`, `anio_min`. Un gatillo que depende de un bloque incompleto **no** se evalúa (la etapa no entra y se anota).

**La capacidad cambia solo desde la entrada en operación** (tests F06 y F07; mutación M15). Cada expansión tiene su propia curva de ramp-up sobre su incremento de capacidad; el OPEX pasa a los rubros de la nueva escala (los semifijos saltan de escalón).

## 5. Qué hará falta para comparar trayectorias (más adelante, no ahora)

CAPEX por etapa con evidencia, prima de ampliación y plazos (DPV-086), valor residual de equipos reemplazados (DPV-167), demanda asegurada en el tiempo, OPEX a cada escala, y criterio de comparación (VAN a igual horizonte y tasa, pico de fondos, riesgo). La comparación y la optimización quedan fuera de esta sesión.
