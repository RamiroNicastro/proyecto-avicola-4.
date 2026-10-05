# Conclusiones de la sesión 19 — modelo financiero integral

**Fecha:** 2026-10-04 · **Estado:** MODELO FINANCIERO ESTRUCTURAL COMPLETADO v1.0 (70 tests, 25/25 mutaciones). **RENTABILIDAD DEL PROYECTO = NO CALCULABLE** con la evidencia actual. No se recomienda arquitectura, escala, financiamiento ni gatillo.

## 1. Qué se construyó

Un motor mensual que conecta demanda → utilización → producción → ventas → ingresos → OPEX → EBITDA → capital de trabajo → CAPEX → FCFF → FCFE → VAN / TIR / payback / break-even / DSCR, evaluando **las mismas 24 configuraciones** del mapa de arquitecturas (C0–CF y 19 variantes) y las trayectorias de expansión 2.500 → 20.000, consumiendo sin modificar los motores CAPEX y OPEX, el balance de masa y los escenarios de demanda ([`arquitectura_financiera.md`](arquitectura_financiera.md)).

## 2. Qué puede usarse hoy para tomar decisiones

1. **El mapa de faltantes**: para cada configuración y bloque, qué dato bloquea qué resultado ([`completitud_financiera.csv`](completitud_financiera.csv), [`evidencia_financiera.md`](evidencia_financiera.md) §5). Es la guía del trabajo de campo económico.
2. **El orden de prioridad de datos**: precios por producto y canal con condiciones → mix y volumen A/B → OPEX costeable → CAPEX cotizado con cronograma y vidas útiles → reglas fiscales → tasa y horizonte → financiamiento.
3. **El motor validado** para simulaciones del promotor (modo escenario), siempre rotuladas.
4. **Criterios conceptuales** ya incorporados: fondos iniciales ≠ CAPEX; pico de fondos incluye pérdidas del ramp-up y ΔCT; fijos no bajan con la utilización; proyecto ≠ accionista; IVA no es costo.

## 3. Qué todavía es simulación (o ni siquiera eso)

- **Todo** número de rentabilidad del proyecto: hoy ni siquiera hay simulación de proyecto, porque las plantillas no tienen precios, mix, cronograma ni impuestos (no se inventan).
- Las curvas de ramp-up CONSERVADOR / BASE / RÁPIDO (SUP-19-09): ilustrativas, sin fuente.
- Los escenarios de demanda de 02 (incluidos los ~90 supermercados): supuestos de prueba, no demanda.
- Los montos E4 parciales de CAPEX (p. ej. USD 5,66 M de galpones en C3) y de OPEX (pollito, maíz): no son totales ni comparables.

## 4. Hallazgos del diseño (críticos)

1. **No hay un solo bloque completo en ninguna configuración**: ingresos y costos están a la vez sin datos. El cuello de botella es comercial (precios y demanda), no de modelado.
2. **El capital necesario no es el CAPEX**: con ramp-up y cobro a plazo, el pico de fondos supera al CAPEX inicial (casos de prueba CP-SIN-RECUPERO y CP-COBRO-30D). USD 2 M no puede compararse con nada todavía.
3. **El modo evidencia exige hoy rendimientos validados en planta** (DPV-060): aunque hubiera precios, los ingresos seguirían sin publicarse en ese modo hasta el ensayo o hasta que se decida aceptar el balance 04 como metodología (DEC-19-01).
4. **C0 no puede tener ingresos de subproductos** hasta conocer el contrato de façon; **C0 tampoco tiene propiedad definida** del alimento y materias primas (DEC-024), por lo que su CT es incompleto por diseño.
5. **Crecer por fases** cambia el CAPEX por etapa (72–75 conceptos sin costo por etapa en C1) y requiere la prima de ampliación y el valor residual de lo reemplazado: sin eso, cualquier comparación entre trayectorias sería artificial.

## 5. Próximos pasos (sin decidir nada)

1. Reconciliación de esta sesión ([`actualizaciones_gestion_19.md`](actualizaciones_gestion_19.md)).
2. Decidir el umbral de publicación (DEC-084 / DEC-19-01), horizonte y tasa (DEC-007), valor terminal (DEC-19-03).
3. Trabajo de campo comercial y de costos según [`evidencia_financiera.md`](evidencia_financiera.md) §5.
4. Recién con datos: escenarios del promotor, stress, comparación de trayectorias; después Monte Carlo y optimización (fuera de esta sesión).
