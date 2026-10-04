# VAN, TIR, MIRR y payback

**Fecha:** 2026-10-04 · Código: `van()`, `tir()`, `mirr()`, `payback()` (funciones puras) · Casos: [`casos_prueba_motor.csv`](casos_prueba_motor.csv)

## 1. VAN

```
VAN = Σ_períodos F_t ÷ (1 + r)^t       t = fin del período en años (T0 = 0; mes k = k/12; año y = y)
```

- **Flujo:** FCFF del proyecto (after-tax si el bloque fiscal está completo; si no, pre-tax y así se rotula en `BASE_FLUJO`).
- **Tasa:** input `TASA_DESCUENTO` (anual efectiva, en la misma base real/nominal que los flujos). **No se inventa un WACC** (DEC-007, DPV-001). Un VAN con tasa del usuario es escenario.
- **VAN del accionista:** sobre el flujo efectivo del accionista con `tasa_descuento_accionista`.

## 2. TIR

Búsqueda en grilla de −99 % a 1.000 % y bisección en cada cambio de signo del VAN:

| Resultado | Cuándo |
|---|---|
| `UNICA` | Una raíz y un solo cambio de signo |
| `UNICA_FLUJO_NO_CONVENCIONAL` | Una raíz pero varios cambios de signo: verificar con VAN |
| `NO_EXISTE` | El flujo no cambia de signo |
| `NO_EXISTE_EN_RANGO` | Cambia de signo pero sin raíz entre −99 % y 1.000 % |
| `TIR_AMBIGUA` | Más de una raíz (se informan todas; no se elige) |

**No se fuerza una TIR** (test N03 con −100, 230, −132 → raíces 10 % y 20 %; mutación M12). `PUBLICABLE_TIR` exige además una TIR matemáticamente definida. MIRR (opcional) = (VF de positivos a la tasa de reinversión ÷ VP de negativos a la tasa de descuento)^(1/T) − 1 (test N13).

## 3. Payback

| | Definición |
|---|---|
| Simple | Primer momento en que el acumulado del FCFF vuelve a ≥ 0, interpolando linealmente **dentro** del período de recupero (flujo uniforme en el período) |
| Descontado | Igual, con flujos descontados a la tasa |
| `NO_RECUPERADO` | No recupera dentro del horizonte: **no se extrapola** (test N06; mutación M13) |
| `RECUPERADO (el acumulado vuelve a ser negativo después)` | Advertencia (p. ej. una expansión posterior) |

## 4. Casos de prueba (artificiales, no del proyecto)

| Caso | Datos | Resultado del motor | Cálculo manual |
|---|---|---|---|
| CP-01 | CAPEX 100 en T0; ventas 100/año; OPEX fijo 60/año; 5 años; 10 %; pre-tax | VAN 51,6315; TIR 28,65 %; payback 2,5; descontado 3,02; u* 60 % | −100 + 40 × 3,790787 = 51,6315 |
| CP-02 | CP-01 + ganancias 30 % y depreciación lineal 5 años | FCFF 34/año; VAN 28,887; TIR 20,76 %; payback 2,94 | 40 − 0,3 × (40 − 20) = 34 |
| CP-03 | OPEX fijo 120/año | TIR `NO_EXISTE`; payback `NO_RECUPERADO`; pico de fondos 200 | EBITDA −20/año |
| CP-04 | CP-01 con cobro a 30 días | VAN 44,16; fondos iniciales 108,2 | CxC = 8,33 × 30 ÷ 30,42 = 8,22 |

## 5. Por qué un indicador solo no alcanza

Ver [`guia_ramiro.md`](guia_ramiro.md) §15 (TIR alta ≠ mejor proyecto) y §16 (planta grande: mejor margen, más riesgo).
