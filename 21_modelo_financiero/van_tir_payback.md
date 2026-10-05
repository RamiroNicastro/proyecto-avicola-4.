# VAN, TIR, MIRR y payback

**Fecha:** 2026-10-04 (auditoría final 2026-10-05) · Código: `tasa_periodica()`, `tasa_anual_efectiva()`, `van_periodico()`, `van()`, `tir()`, `anualizar()`, `mirr()`, `payback()`, `indicadores()` · Casos: [`casos_prueba_motor.csv`](casos_prueba_motor.csv)

## 0. Convención de tasas y de descuento (SUP-192)

| Concepto | Regla | Test |
|---|---|---|
| `TASA_DESCUENTO` | Anual **efectiva** (`tipo_tasa_descuento = EFECTIVA_ANUAL`). Si se declara `NOMINAL_ANUAL_CAP_MENSUAL` j, se convierte antes a efectiva: (1 + j/12)^12 − 1 | R01 |
| Tasa mensual | `i_m = (1 + r)^(1/12) − 1`. **Nunca** `r/12` (mutación M22) | R01 |
| Convención por defecto: `MENSUAL` | Los indicadores se calculan sobre la **serie mensual** del motor: k = 0 (T0) sin descontar; el mes k se descuenta k períodos con `i_m` | R02, C03 |
| Convención alternativa: `PERIODO_REPORTE` | Flujos agregados a los períodos de reporte (T0, meses, años) y descontados al **fin** de cada período con `t` en años | C01, C02 |
| Base real / nominal | La tasa debe estar en la misma base que los flujos; si no, error explícito (no se convierte en silencio) | N08, R06 |

La convención usada y las dos tasas (anual efectiva y mensual equivalente) se registran en cada corrida (`CONVENCION_DESCUENTO`, `TASA_DESCUENTO_ANUAL_EFECTIVA`, `TASA_DESCUENTO_MENSUAL_EQUIVALENTE` en [`escenarios_financieros.csv`](escenarios_financieros.csv)).

## 1. VAN

```
MENSUAL:          VAN = Σ_k F_k ÷ (1 + i_m)^k            k = 0…12·H ; i_m = (1 + r)^(1/12) − 1
PERIODO_REPORTE:  VAN = Σ_p F_p ÷ (1 + r)^(t_p)          t_p = fin del período p en años
```

Ambas son equivalentes para un mismo flujo mensual (t = k/12); difieren solo si el flujo se **agrega** antes de descontar (los meses de un año se tratan como cobrados a fin de año).

- **Flujo:** FCFF del proyecto (after-tax si el bloque fiscal está completo; si no, pre-tax: `BASE_FLUJO`).
- **Tasa:** input; **no se inventa un WACC** (DEC-007, DPV-001). Un VAN con tasa del usuario es escenario.
- **VAN del accionista:** flujo efectivo del accionista con `tasa_descuento_accionista`, misma convención.

## 2. TIR

Con la convención MENSUAL se calcula primero la **TIR mensual** (periódica) sobre la serie mensual y se reporta:

```
TIR_MENSUAL = i  tal que Σ_k F_k ÷ (1 + i)^k = 0
TIR (anual efectiva) = (1 + TIR_MENSUAL)^12 − 1        nunca TIR_MENSUAL × 12 (mutación M23; test R03)
```

Con PERIODO_REPORTE la TIR sale directamente anual efectiva (t en años) y `TIR_MENSUAL` es la equivalente.

Búsqueda en grilla + bisección en cada cambio de signo (mensual: −50 % a 200 % por mes; anual: −99 % a 1.000 %):

| Resultado | Cuándo |
|---|---|
| `UNICA` | Una raíz y un solo cambio de signo |
| `UNICA_FLUJO_NO_CONVENCIONAL` | Una raíz pero varios cambios de signo: verificar con VAN |
| `NO_EXISTE` | El flujo no cambia de signo |
| `NO_EXISTE_EN_RANGO` | Cambia de signo pero sin raíz en el rango |
| `TIR_AMBIGUA` | Más de una raíz (se informan todas; no se elige) |

**No se fuerza una TIR** (tests N03 y R03; mutación M12). `PUBLICABLE_TIR` exige además una TIR matemáticamente definida. MIRR (opcional) = (VF de positivos a la tasa de reinversión ÷ VP de negativos a la tasa de descuento)^(1/T) − 1 (test N13).

## 3. Payback

| | Definición |
|---|---|
| Simple | Primer momento en que el acumulado del FCFF vuelve a ≥ 0, interpolando linealmente **dentro** del período de recupero |
| Descontado | Igual, con flujos descontados (`i_m` en MENSUAL; `r` en PERIODO_REPORTE) |
| Unidades | `PAYBACK_*_MESES` y `PAYBACK_*_ANIOS = meses ÷ 12`. En MENSUAL el tiempo es el **mes del motor**; en PERIODO_REPORTE es el fin de cada período en años (× 12 = meses). Nunca el índice de período de reporte (test R04; mutación M25) |
| `NO_RECUPERADO` | No recupera dentro del horizonte: **no se extrapola** (test N06; mutación M13) |
| `RECUPERADO (el acumulado vuelve a ser negativo después)` | Advertencia (p. ej. una expansión posterior) |

## 4. Casos de prueba con nombre propio (artificiales; NO son parámetros del proyecto)

Comunes a todos: CAPEX inicial 100 en T0; ingresos 100/año; OPEX fijo 60/año; ΔCT 0 (salvo CP-COBRO-30D); sin CAPEX posterior; horizonte 5 años; valor terminal 0; tasa anual efectiva 10 %.

**Causa de la discrepancia detectada en la auditoría:** los dos juegos de resultados que se informaron como "el caso artificial" eran **dos casos distintos**. El de FCFF 34/año (VAN 28,89; TIR 20,76 %; payback 2,94) se corrió con `tasa_ganancias = 0,30` (after-tax); el de FCFF 40/año (VAN 51,63; TIR 28,65 %; payback 2,5) con `tasa_ganancias = None` (pre-tax). Ambos usaban además la convención de fin de año sin declararla. Desde esta auditoría cada caso tiene nombre, tasa fiscal, base imponible y convención explícitos.

| Caso | Diferencia | Tasa fiscal de TEST | Depreciación | Base imponible | Impuesto | FCFF/año | VAN 10 % | TIR | Payback |
|---|---|---|---|---|---|---|---|---|---|
| `CP-PRETAX-ANUAL` | Pre-tax; fin de año | — (sin ganancias) | 20 (no grava) | no aplica | 0 | **40** | **51,6315** (= −100 + 40 × 3,790787) | **28,65 %** | **2,5 años = 30 meses** |
| `CP-AFTERTAX-ANUAL` | After-tax; fin de año | **30 %** (solo test) | 100 ÷ 5 = **20/año** | EBITDA 40 − 20 = **20** | 0,3 × 20 = **6** | **34** | **28,8868** | **20,76 %** | **100 ÷ 34 = 2,94 años** |
| `CP-PRETAX-MENSUAL` | Pre-tax; convención mensual del motor (40/12 por mes) | — | 20 | no aplica | 0 | 40 | 58,4617 (= −100 + Σ (40/12) ÷ 1,1^(k/12)) | 36,58 % (2,63 % mensual) | 30 meses = 2,5 años |
| `CP-SIN-RECUPERO` | Pre-tax anual; OPEX 120/año | — | 20 | no aplica | 0 | −20 | −175,82 | `NO_EXISTE` | `NO_RECUPERADO`; pico de fondos 200 |
| `CP-COBRO-30D` | `CP-PRETAX-ANUAL` + cobro a 30 días | — | 20 | no aplica | 0 | 31,78 el año 1 (ΔCT 8,22), luego 40 | 44,1595 | 25,47 % | 2,71 años |

La tasa fiscal de test (30 %) existe **solo** en `caso_prueba()`; ningún escenario del proyecto la usa (`impuestos.tasa_ganancias` sigue vacía en [`inputs_financieros.csv`](inputs_financieros.csv); test C02). Tests: C01, C02, C03, N01, N05, N06.

## 5. Por qué un indicador solo no alcanza

Ver [`guia_ramiro.md`](guia_ramiro.md) §15 (TIR alta ≠ mejor proyecto) y §16 (planta grande: mejor margen, más riesgo).
