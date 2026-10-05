# Financiamiento, cronograma de deuda y DSCR

**Fecha:** 2026-10-04 · Código: `cronograma_deuda()`, bloque "caja del accionista" de `simular()` · Salidas: [`deuda.csv`](deuda.csv), [`flujo_accionista.csv`](flujo_accionista.csv)

> **No se asume financiación disponible** y **no** se recomienda estructura (DEC-092 abierta). USD 2 M es un escenario de referencia no comprometido (SUP-003, DEC-010): el modelo no lo usa como capital.

## 1. Estructura configurable (solo modo escenario hoy)

```json
"financiamiento": {
  "aportes": [[mes, monto], ...],             // equity programado
  "aporte_automatico": false,                 // true: aporta lo necesario para no bajar de caja_minima_usd
  "caja_minima_usd": null,
  "reservas_usd": null,                       // reservas exigidas por el fondeo (entran a OTROS_REQUERIMIENTOS_CAJA)
  "deudas": [{"id", "monto", "moneda": "USD", "tasa", "tipo_tasa", "capitalizacion_meses", "periodo_tasa_meses",
              "base_tasa", "plazo_meses", "gracia_meses", "metodo", "frecuencia_meses", "comision_pct",
              "mes_desembolso", "cronograma"}],
  "politica_dividendos": null                 // {"pct_caja_excedente", "caja_minima_usd"}; null = caja retenida
}
```

| Tipo | Cómo se modela |
|---|---|
| EQUITY | `aportes` y/o `aporte_automatico` (mide cuánto equity requiere el plan) |
| DEUDA | Uno o más tramos |
| MIXTO | Ambos |

Moneda: USD; una deuda en otra moneda se rechaza hasta cargarla con TC explícito (regla 2).

## 2. Cronograma de deuda

```
saldo_final = saldo_inicial + altas − amortización          (test I07; mutación M18)
interés     = saldo × i_período                en cada fecha de pago (frecuencia f meses)
```

**Convención de tasa (obligatoria, SUP-19-26; test R05; mutación M24):**

| `tipo_tasa` | Tasa del período de servicio `i_período` | Condición |
|---|---|---|
| `EFECTIVA_ANUAL` (TEA) | (1 + TEA)^(f/12) − 1 | — |
| `NOMINAL_ANUAL` (TNA) | TNA × f ÷ 12 | `capitalizacion_meses` declarada **igual** a la frecuencia de pago; si difiere → error |
| `PERIODICA` | la tasa declarada | `periodo_tasa_meses` declarado **igual** a la frecuencia; si difiere → error |
| sin tipo | — | error: combinación ambigua bloqueada |

`base_tasa` (REAL / NOMINAL) debe coincidir con el modelo monetario; si no, error (test R06). No se carga ninguna tasa.

| Método | Regla | Test |
|---|---|---|
| FRANCES | Cuota constante = S·i ÷ (1 − (1 + i)^−n) | N11, R05 (cuota 8,8849 para 100 al 1 % mensual en 12 cuotas: TEA 12,6825 % = TNA 12 % cap. mensual = 1 % periódica) |
| ALEMAN | Amortización constante S ÷ n | N11 |
| BULLET | Todo el capital en la última fecha; intereses periódicos | N11 |
| PERSONALIZADO | Cronograma `[[mes_relativo, amortización]]` que suma el monto | validación |

Gracia = solo intereses (no capitaliza). Comisión = % del monto al desembolso. El saldo pendiente al cierre del horizonte se informa y se cancela en el FCFE.

## 3. DSCR

```
CFADS = EBITDA − impuesto con deuda − ΔCT + flujo IVA − CAPEX de reposición
DSCR  = CFADS ÷ (intereses + amortización)        por período de reporte; se informa el mínimo
```

No se publica si el flujo after-tax o el financiamiento están incompletos, ni si no hay deuda (`NO_APLICA`). Test N12. El DSCR puede usarse como **gatillo** de expansión (`dscr_min`), sin decidir el umbral.

## 4. Separación proyecto / accionista

La deuda nunca entra al FCFF (test N09). El accionista ve: deuda recibida, intereses, comisiones, amortización, aportes y dividendos ([`flujo_caja.md`](flujo_caja.md) §2).
