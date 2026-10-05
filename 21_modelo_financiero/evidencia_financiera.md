# Evidencia financiera: completitud y publicabilidad actuales

**Fecha:** 2026-10-04 · Salidas: [`completitud_financiera.csv`](completitud_financiera.csv), [`escenarios_financieros.csv`](escenarios_financieros.csv) · Matriz previa: [`../00_gestion_proyecto/matriz_completitud_economica.csv`](../00_gestion_proyecto/matriz_completitud_economica.csv)

## 1. Resultado central

**En las 61 corridas (42 en modo evidencia, 19 plantillas de escenario) las 10 banderas `PUBLICABLE_*` son FALSE.** Hoy no existe ningún ingreso, EBITDA, flujo, VAN, TIR, payback, break-even, flujo del accionista ni DSCR del proyecto que pueda presentarse, ni siquiera como simulación, porque las plantillas no tienen precios, mix, cronograma ni impuestos (no se rellenan arbitrariamente).

## 2. Completitud por bloque (todas las configuraciones C0–CF, escalas y variantes)

| Bloque | Modo evidencia (42) | Plantillas (19) | Qué falta (resumen) | Registros |
|---|---|---|---|---|
| DEMANDA | PENDIENTE | PARCIAL (referencia de 02 sin mix) | Volumen A/B cuantificado por producto y canal | DPV-002, DPV-004, DPV-020, DPV-037, DPV-040 |
| PRODUCCION | PARCIAL | PARCIAL | Rendimientos 04 sin ensayo en planta; curva de ramp-up; horizonte y fases | DPV-060, DEC-028, DEC-090, DPV-086, DEC-007 |
| PRECIOS | PENDIENTE | PENDIENTE | 42 combinaciones producto × canal × mercado vacías; 2 referencias E4 no usables | DPV-013, DPV-039, DPV-070, DPV-026 |
| INGRESOS | PARCIAL | PARCIAL | Lo anterior + condiciones comerciales por canal | DPV-039, DPV-040 |
| OPEX | PARCIAL | PARCIAL | Ninguna arquitectura costeable; costeo por bloques 0–10 % | T18-02, DPV-047, 050, 052, 148, 157, 170–177 |
| CAPEX | PARCIAL | PARCIAL | Sin total (cobertura 0–2,3 %); sin curva de desembolso; vidas útiles vacías | T18-01, DPV-160–169, DPV-086, DPV-167 |
| CT | PARCIAL | PARCIAL | Días de stock, cobro y pago; propiedad PENDIENTE en C0 | DPV-175, DEC-089, DEC-091, DEC-024 |
| IMPUESTOS | PENDIENTE | PENDIENTE | IIBB, tasas, ganancias, quebrantos, IVA | DPV-043, DPV-169 |
| FINANCIACION | PENDIENTE | PENDIENTE | Estructura (equity / deuda / mixto) | DEC-092, DPV-178 |
| DESCUENTO | PENDIENTE | PENDIENTE | Tasa de descuento | DEC-007, DPV-001 |
| EXPORTACION | NO_APLICA | NO_APLICA | Base sin exportación (SUP-022) | — |

PARCIAL nunca habilita un resultado: indica que existe estructura o datos parciales.

## 3. Montos E4 que existen y **no** se usan

| Configuración (10.000) | CAPEX "con precio" (E4, parcial) | Conceptos CAPEX con precio | OPEX "con precio" (E4, parcial) | Costeo OPEX por bloques |
|---|---|---|---|---|
| C0 | — | 0 / 21 | USD 2.330.038/año (solo pollito BB, POL-COMPRA) | 9,5 % |
| C1 | USD 119.200 | 1 / 76 | USD 2.330.038/año (solo pollito BB) | 7,7 % |
| C2 | USD 1.503.829 | 2 / 88 | USD 2.330.038/año (pollito BB en granjas propias e integradas) | 4,9 % |
| C3 / CF | USD 5.657.713 | 2 / 138 | USD 1.441.539/año (solo maíz pizarra Rosario sobre puerto, ALI-MP-MAIZ) | 0,0 % |

Reflejan **qué concepto tiene precio**, no el costo de cada opción (T18-14): no son comparables entre arquitecturas ni contra USD 2 M. El motor los deja solo en la traza (tests E06, E12).

## 4. Qué puede usarse hoy para decidir

**Umbral usado:** `UMBRAL_EVIDENCIA_PUBLICACION = E1|E2|E3` (default conservador configurable en `inputs_financieros.csv`; DEC-084 abierta; columna `UMBRAL_EVIDENCIA` de cada corrida). Con cualquier umbral razonable el resultado no cambia hoy: no existen precios ni totales de CAPEX/OPEX, y los únicos montos son E4 parciales.

| Sí (como herramienta) | No (todavía) |
|---|---|
| La **estructura** del modelo: qué datos faltan, en qué orden y por qué bloquean cada resultado | Cualquier cifra de rentabilidad del proyecto |
| La **lista priorizada de datos** (§5) para el trabajo de campo | Comparar C0–CF, escalas o trayectorias por rentabilidad |
| El **motor validado** para simular escenarios hipotéticos que cargue el promotor (rotulados) | Afirmar que USD 2 M alcanza o no alcanza |
| La lógica física de ventas: con un mix dado, qué parte limita y cuánto excedente queda (kg) | Decidir escala, integración, financiamiento o gatillos |

## 5. Datos que desbloquean más resultados (orden sugerido)

1. **Precios por producto y canal + condiciones comerciales** (DPV-013, DPV-039, DPV-070, DPV-040) → habilita ingresos con un mix.
2. **Mix y volumen de demanda A/B** (DPV-037, DPV-020, DPV-002) → habilita ventas en modo evidencia.
3. **OPEX costeable** de al menos una arquitectura (alimento, pollito, salarios, utilities, façon) → habilita EBITDA y break-even.
4. **CAPEX con cotizaciones + cronograma de desembolso + vidas útiles** (DPV-160–169, DPV-086) → habilita flujo, VAN, TIR, payback.
5. **Reglas fiscales** (DPV-043, DPV-169) → flujo after-tax.
6. **Tasa de descuento y horizonte** (DEC-007) → VAN publicable.
7. **Financiamiento disponible** (DEC-092, DPV-178) → flujo del accionista y DSCR.
8. **Validación de rendimientos en planta** (DPV-060) y decisión de umbral (DEC-084) → modo evidencia completo.
