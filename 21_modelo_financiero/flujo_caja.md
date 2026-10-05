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
- La deuda que quede al cierre del horizonte se cancela en el FCFE del último mes (SUP-198): conservador para el accionista.
- **No** se mezcla con el FCFF: el VAN y la TIR del proyecto usan FCFF; los del accionista usan el flujo efectivo con su propia tasa (`tasa_descuento_accionista`).

## 3. ¿Cuánto capital necesita? — tres medidas que no se confunden

| Medida | Definición | Para qué sirve |
|---|---|---|
| `CAPEX_INICIAL` | Σ desembolsos de la etapa inicial | Inversión en activos. **No** es la inversión total |
| `FONDOS_INICIALES` | CAPEX inicial + `CT_INICIAL` + `OTROS_REQUERIMIENTOS_CAJA` | Concepto de la interfaz CAPEX §1. `CT_INICIAL` = máximo CT hasta el fin del ramp-up; `OTROS` = máximo saldo de IVA a favor antes de operar + intereses y comisiones antes de operar + reservas declaradas (SUP-205) |
| `PICO_REQUERIMIENTO_FONDOS` | − mínimo del FCFF acumulado (y `MES_VALLE_CAJA`) | Lo que realmente hay que fondear: incluye las **pérdidas del ramp-up** y el ΔCT. Responde "¿cuánto financiamiento necesita durante el ramp-up?" |

En el caso de prueba CP-SIN-RECUPERO (pre-tax, EBITDA negativo) los fondos iniciales son 100 pero el pico es 200: un proyecto que pierde dinero consume más que su CAPEX.

## 4. IVA (módulo separado; no es costo económico)

| Modo | Tratamiento |
|---|---|
| `null` | PENDIENTE: el flujo no es publicable (el IVA del CAPEX es un requerimiento de fondos material) |
| `EXCLUIDO` | Declaración del usuario: flujos sin IVA, efecto financiero ignorado (rotulado) |
| `SIMPLIFICADO` | Débito = alícuota × venta interna neta de descuentos, bonificaciones y devoluciones; crédito = alícuota × compras marcadas + IVA de CAPEX **solo de etapas con `iva_capex` declarado** (ver abajo); el saldo a favor se **arrastra**; efecto de caja = − Δ saldo a favor (SUP-201). Sin recupero anticipado, percepciones ni retenciones (DPV-169) |

El IVA del CAPEX **no** entra al EBITDA (test N15; mutación M17). La exportación no genera débito.

**Crédito fiscal del IVA de CAPEX (auditoría final 21, TF-076):** con `SIMPLIFICADO`, el crédito del IVA de cada etapa (inicial, expansión y reposición) solo se incorpora a caja si la etapa declara `iva_capex` = {`base`: NETA, `iva_estado`: DECLARADO, `tasa`, `condicion_fiscal`, `elegible_credito`: TRUE, `criterio`} (`iva_capex_declarado()`). Con IVA `DESCONOCIDO` / `INCIERTO` / `NO_DECLARADO` o datos incompletos: `CREDITO_FISCAL_IVA_CAPEX = PENDIENTE` (faltante del bloque IVA: el flujo no se publica) y el monto queda solo como base informativa (`iva_capex_pendiente_base`): **ni costo ni crédito**. Un CAPEX de 19 con conceptos `IVA_INCIERTO` no se usa como total (`capex_desde_modulo()`). La alícuota global `iva.alicuota_capex` ya no genera crédito por sí sola. Tests N15 e integración IV01–IV02; mutación de integración m15.

## 5. Valor residual / terminal (no se elige método)

| Método | Valor al cierre | Nota |
|---|---|---|
| `SIN_VALOR_TERMINAL` | 0 | **Por defecto** para no inflar resultados (SUP-198) |
| `VALOR_LIBRO` | Σ (costo − depreciación acumulada) de los activos vivos; terreno al costo | Requiere depreciación completa |
| `EXPLICITO` | Monto declarado | Escenario |
| `PERPETUIDAD` | FCFF de los últimos 12 meses × (1 + g) ÷ (r − g) | Requiere r > g; domina el VAN con facilidad |

Opción `recuperar_ct` (por defecto no). Test N14. Con `recuperar_ct` el CT del cierre se suma a la serie `valor_terminal` también en PERPETUIDAD (corrección de reporte de la auditoría final 21, TF-009: el FCFF y el VAN ya lo incluían; la identidad FCFF = EBITDA − CAPEX − ΔCT ± IVA + VT cierra con cualquier método, test de integración FI03).

## 6. Real vs nominal y moneda

Ver [`metodologia_financiera.md`](metodologia_financiera.md) §6. El modelo por defecto es real en USD; no se mezcla una tasa nominal con flujos reales (test N08).
