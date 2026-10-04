# Flujo de caja del proyecto (FCFF), del accionista (FCFE) y fondos requeridos

**Fecha:** 2026-10-04 · Salidas: [`flujo_caja_proyecto.csv`](flujo_caja_proyecto.csv), [`flujo_accionista.csv`](flujo_accionista.csv)

## 1. Flujo del proyecto (sin financiación) — base para evaluar la inversión

```
FCFF = EBIT − impuesto operativo (sobre EBIT, sin deuda) + depreciación − CAPEX − ΔCT + flujo IVA [+ valor terminal]
     = EBITDA − impuesto operativo − CAPEX − ΔCT + flujo IVA [+ valor terminal]          (fórmula equivalente usada)
CAPEX = inicial + expansión + reposición
```

- Test I06: ambas formas cierran mes a mes. Mutación M05 (partir del EBIT sin sumar la depreciación) se detecta.
- **Independiente de cómo se financie** (test N09; mutación M06: si la deuda entra al FCFF, se detecta).
- `FCFF_PRE` = antes de ganancias; `FCFF` = después. `BASE_FLUJO` dice cuál se usó en los indicadores.

## 2. Flujo del accionista (separado)

```
FCFE = EBITDA − impuesto con deuda − CAPEX − ΔCT + flujo IVA [+ valor terminal]
       − intereses − comisiones + deuda recibida − amortizaciones [− deuda remanente al cierre]
caja(k) = caja(k − 1) + FCFE(k) + aportes(k) − dividendos(k)                (test I08; mutación M19)
FLUJO EFECTIVO DEL ACCIONISTA = − aportes + dividendos (+ caja remanente al cierre)
```

- El FCFE responde a la deuda (test N10) e incorpora el escudo fiscal de los intereses.
- La deuda que quede al cierre del horizonte se cancela en el FCFE del último mes (SUP-19-12): conservador para el accionista.
- **No** se mezcla con el FCFF: el VAN y la TIR del proyecto usan FCFF; los del accionista usan el flujo efectivo con su propia tasa (`tasa_descuento_accionista`).

## 3. ¿Cuánto capital necesita? — tres medidas que no se confunden

| Medida | Definición | Para qué sirve |
|---|---|---|
| `CAPEX_INICIAL` | Σ desembolsos de la etapa inicial | Inversión en activos. **No** es la inversión total |
| `FONDOS_INICIALES` | CAPEX inicial + `CT_INICIAL` + `OTROS_REQUERIMIENTOS_CAJA` | Concepto de la interfaz CAPEX §1. `CT_INICIAL` = máximo CT hasta el fin del ramp-up; `OTROS` = máximo saldo de IVA a favor antes de operar + intereses y comisiones antes de operar + reservas declaradas (SUP-19-19) |
| `PICO_REQUERIMIENTO_FONDOS` | − mínimo del FCFF acumulado (y `MES_VALLE_CAJA`) | Lo que realmente hay que fondear: incluye las **pérdidas del ramp-up** y el ΔCT. Responde "¿cuánto financiamiento necesita durante el ramp-up?" |

En el caso de prueba CP-03 (EBITDA negativo) los fondos iniciales son 100 pero el pico es 200: un proyecto que pierde dinero consume más que su CAPEX.

## 4. IVA (módulo separado; no es costo económico)

| Modo | Tratamiento |
|---|---|
| `null` | PENDIENTE: el flujo no es publicable (el IVA del CAPEX es un requerimiento de fondos material) |
| `EXCLUIDO` | Declaración del usuario: flujos sin IVA, efecto financiero ignorado (rotulado) |
| `SIMPLIFICADO` | Débito = alícuota × venta interna neta de descuentos, bonificaciones y devoluciones; crédito = alícuota × compras marcadas + alícuota de bienes de capital × CAPEX; el saldo a favor se **arrastra**; efecto de caja = − Δ saldo a favor (SUP-19-15). Sin recupero anticipado, percepciones ni retenciones (DPV-169) |

El IVA del CAPEX **no** entra al EBITDA (test N15; mutación M17). La exportación no genera débito.

## 5. Valor residual / terminal (no se elige método)

| Método | Valor al cierre | Nota |
|---|---|---|
| `SIN_VALOR_TERMINAL` | 0 | **Por defecto** para no inflar resultados (SUP-19-12) |
| `VALOR_LIBRO` | Σ (costo − depreciación acumulada) de los activos vivos; terreno al costo | Requiere depreciación completa |
| `EXPLICITO` | Monto declarado | Escenario |
| `PERPETUIDAD` | FCFF de los últimos 12 meses × (1 + g) ÷ (r − g) | Requiere r > g; domina el VAN con facilidad |

Opción `recuperar_ct` (por defecto no). Test N14.

## 6. Real vs nominal y moneda

Ver [`metodologia_financiera.md`](metodologia_financiera.md) §6. El modelo por defecto es real en USD; no se mezcla una tasa nominal con flujos reales (test N08).
