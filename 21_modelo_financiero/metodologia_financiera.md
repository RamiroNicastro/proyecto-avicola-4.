# Metodología del modelo financiero integral

**Fecha:** 2026-10-04 · **Sesión:** 19 · **Modelo:** [`modelo_financiero.py`](modelo_financiero.py) v1.0 · **Estado:** motor estructural construido y probado (56 tests, 20/20 mutaciones detectadas). **Ningún resultado de rentabilidad del proyecto es publicable hoy** ([`evidencia_financiera.md`](evidencia_financiera.md)).

> Este documento define **cómo** calcula el modelo. La arquitectura del código está en [`arquitectura_financiera.md`](arquitectura_financiera.md); cada bloque tiene su documento (ver [`README.md`](README.md)). Los IDs `SUP-19-##`, `DPV-19-##` y `DEC-19-##` son provisionales ([`actualizaciones_gestion_19.md`](actualizaciones_gestion_19.md)).

## 1. Qué responde y qué no

| Pregunta | Salida del motor | Condición para publicarla |
|---|---|---|
| ¿Cuánto capital necesita esta configuración? | `FONDOS_INICIALES` = CAPEX inicial + CT inicial + otros requerimientos; `PICO_REQUERIMIENTO_FONDOS` (valle del FCFF acumulado) | `PUBLICABLE_FLUJO` |
| ¿Cuánto puede facturar? | `VENTA_BRUTA` e `INGRESO_NETO` por período | `PUBLICABLE_INGRESOS` |
| ¿Cuánto margen genera? | `EBITDA`, margen EBITDA, margen de contribución | `PUBLICABLE_EBITDA` |
| ¿Cuándo recupera la inversión? | Payback simple y descontado (o `NO_RECUPERADO`) | `PUBLICABLE_PAYBACK` |
| ¿Cuál es su VAN y TIR? | VAN (tasa del usuario), TIR (única / `NO_EXISTE` / `TIR_AMBIGUA`), MIRR opcional | `PUBLICABLE_VAN`, `PUBLICABLE_TIR` |
| ¿Qué utilización necesita para no perder dinero? | Break-even en volumen, utilización y precio | `PUBLICABLE_BREAK_EVEN` |
| ¿Cuánto financiamiento necesita en el ramp-up? | Pico de requerimiento de fondos; aportes automáticos; DSCR | `PUBLICABLE_FLUJO`, `PUBLICABLE_FLUJO_ACCIONISTA`, `PUBLICABLE_DSCR` |

**No hace** (fuera de alcance de esta sesión): optimización, ranking, recomendación de arquitectura, escala, financiamiento o gatillo; Monte Carlo; app o presentación final.

## 2. Dos modos que nunca se mezclan

| | MODO EVIDENCIA | MODO ESCENARIO |
|---|---|---|
| Qué acepta | Solo datos **E1–E3** (cotización, precio directo, documento leído en original) y los supuestos **metodológicos** de `SUPUESTOS_METODOLOGICOS` (convenciones de reporte, modelo real, valor terminal por defecto) | Todo lo anterior **más** inputs del usuario (precios, demanda, CAPEX, OPEX, utilización, ramp-up, financiamiento, impuestos, plazos, stress) y las plantillas `SUPUESTO_MODELO` |
| Si falta un bloque material | **`NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE`** + lista exacta de faltantes | `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO` + lista |
| Si está todo | Resultado con rótulo "EVIDENCIA E1–E3 completa" | Resultado rotulado **`SIMULACION_HIPOTETICA_NO_VALIDADA`** |
| E4 `[PVDP]` y E5 | **No** se aceptan (SUP-19-02, provisional hasta DEC-084) | Solo si el usuario los carga explícitamente como escenario |
| Stress | Prohibido (error) | Permitido |

**Umbral provisional de publicación (SUP-19-02):** 100 % de los bloques materiales completos y con evidencia E1–E3. Es el criterio más estricto posible hasta que el promotor decida DEC-084 (ampliada por DEC-19-01).

## 3. Jerarquía de inputs y trazabilidad

Cada variable se resuelve con `resolver()` en este orden (SUP-19-01):

1. **EVIDENCIA_REAL** (E1–E3) — nunca la reemplaza un escenario;
2. **ESCENARIO_USUARIO** — completa lo que falta, solo en modo escenario;
3. **SUPUESTO_MODELO** — plantillas y convenciones; en modo evidencia solo las metodológicas;
4. **PENDIENTE** — vacío; **nunca 0**.

La traza de cada corrida queda en [`mapa_drivers_financieros.csv`](mapa_drivers_financieros.csv) con `VARIABLE, VALOR, UNIDAD, PERIODO, ORIGEN, ARCHIVO, VARIABLE_ORIGEN, MODO, EVIDENCIA, OBSERVACIONES`. Los inputs editables y su procedencia viven en [`inputs_financieros.csv`](inputs_financieros.csv) (filas `EVIDENCIA` y filas de plantilla separadas; los valores de escenario del usuario van en un JSON aparte y nunca se escriben sobre la base: test E03).

## 4. Tiempo

| Elemento | Regla |
|---|---|
| Motor | **Mensual** interno: `k = 0` es **T0** (instante de `FECHA_INICIO`), `k = 1…12·H` son meses |
| Reporte | T0 + meses 1…`MESES_DETALLE` (por defecto **24**, SUP-19-06) + años siguientes. Flujos = suma; saldos = fin de período; utilizaciones = aves ÷ capacidad del período |
| Horizonte | Configurable; **10, 15 o 20 años** son escenarios (DEC-007). El modelo no elige uno |
| Registro | `FECHA_INICIO`, `PERIODO`, `ANIO_PROYECTO`, `ANIO_OPERATIVO`, `FASE` en cada fila periódica |
| Fases | `PREOPERACION → CONSTRUCCION → COMMISSIONING → RAMP_UP → OPERACION_MADURA` (duraciones = inputs, DPV-086) |
| Descuento | Fin de período, tasa anual efectiva, `t = k/12` años (SUP-19-04) |

## 5. Cadena de cálculo (por mes)

```
DEMANDA contable (kg/mes por producto, canal y categoría)
  → UTILIZACIÓN: técnica (curva) · comercial (parte limitante) · efectiva = mín(técnica, comercial)
    → PRODUCCIÓN: aves faenadas × kg por ave (balance 04) × (1 − merma de arranque)
      → VENTAS: ≤ mín(producción + inventario, demanda); el inventario desplaza, no crea
        → INGRESOS: venta bruta − descuentos − bonificaciones − devoluciones − comisiones − derechos = ingreso neto
          → OPEX: rubros de 20_opex (variable × u ÷ eficiencia + fijo)
            → EBITDA → depreciación → EBIT → impuesto (sin deuda / con deuda)
              → CAPITAL DE TRABAJO: inventarios propios + CxC + caja − CxP → ΔCT
                → CAPEX: curva de desembolso (inicial / expansión / reposición)
                  → FCFF (proyecto) → financiamiento → FCFE (accionista) → caja
                    → VAN / TIR / MIRR / PAYBACK / BREAK-EVEN / DSCR
```

Detalle de cada eslabón: ingresos [`modelo_ingresos.md`](modelo_ingresos.md); ramp-up [`modelo_ramp_up.md`](modelo_ramp_up.md); resultados [`estado_resultados.md`](estado_resultados.md); CT [`capital_trabajo_financiero.md`](capital_trabajo_financiero.md); flujos [`flujo_caja.md`](flujo_caja.md); deuda [`financiamiento.md`](financiamiento.md); indicadores [`van_tir_payback.md`](van_tir_payback.md) y [`break_even.md`](break_even.md); fases [`expansion_financiera.md`](expansion_financiera.md).

## 6. Moneda, inflación y precios en el tiempo

- **Moneda funcional USD** (regla 2). Todo valor en ARS exige TC, tipo y fecha (`a_usd()`, test E11). Reporte en ARS solo con un TC por período declarado (`a_moneda_reporte()`, test N22). Moneda original, TC y moneda de reporte se registran por separado.
- **Modelo REAL por defecto** (USD constantes de la fecha base 2026-10-01, sin inflación; SUP-19-07). Modelo **NOMINAL** solo con inflación declarada; la tasa de descuento debe estar en la **misma base** que los flujos (`validar_entrada()` lo exige; test N08 verifica que con tasas consistentes por Fisher el VAN real y el nominal coinciden). Fisher no se aplica en silencio.
- **Precio constante real o serie por año.** No hay crecimiento automático (test N08/N21). Una serie incompleta es faltante (no se extrapola).

## 7. Reglas que el motor hace cumplir (con test)

| Regla | Mecanismo | Test |
|---|---|---|
| Faltante ≠ 0 | `disponibilidad()` + anulación de series (`None`) | E01, E06, E13 |
| E4 no se vuelve validado | `resolver()`, `leer_precios()`, `capex_desde_modulo()`, `opex_desde_modulo()` | E02, E06, E12 |
| El escenario no sobrescribe la evidencia | `resolver()` y fusión de dicts "solo donde falta" | E03 |
| No 100 % de utilización automática | utilización efectiva = mín(técnica, comercial) | F02, F11 |
| Los 90 supermercados no son demanda | `_lineas_contables()`: el modo evidencia vende solo `DOCUMENTADA` / `ASEGURADA` | E08 |
| Ventas ≤ producción y ≤ demanda | asignación por línea | F01, F02, F03, F03b |
| Alternativas exclusivas no duplican masa | rutas del balance; destino C único | F04, F05 |
| Fijos no caen con la utilización | `PCT_VARIABLE` de OPEX | F08 |
| EBITDA ≠ caja; ΔCT, no stock | FCFF con ΔCT | I05, I06 |
| Proyecto ≠ accionista | FCFF sin deuda; FCFE con deuda | N09, N10 |
| IVA no es costo económico | módulo IVA fuera del EBITDA | N15 |
| Real ≠ nominal | validación de base | N08 |
| TIR no forzada | barrido + raíces | N03, N04 |
| Payback sin extrapolación | `NO_RECUPERADO` | N06 |

## 8. Supuestos de modelo de esta sesión

Todos son criterios de cálculo, no datos económicos. Lista completa con ubicación en el código: [`actualizaciones_gestion_19.md`](actualizaciones_gestion_19.md) §1 (SUP-19-01 a SUP-19-24).
