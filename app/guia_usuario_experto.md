# Guía de usuario — modo experto

Acceso completo a los inputs del motor, agrupados por pestañas. Todo lo editado es **ESCENARIO** (rotulado SIMULACION_HIPOTETICA_NO_VALIDADA): la evidencia central no se modifica. Vacío = PENDIENTE (nunca 0).

| Pestaña | Campos (motor) | Notas |
|---|---|---|
| Tiempo, tasas y ramp-up | `horizonte_anios`, `fecha_inicio`, `meses_preoperacion/construccion/commissioning`, `tasa_descuento`, `tasa_descuento_accionista`, `tipo_tasa_descuento`, `convencion_descuento`, `valor_terminal.metodo`, plantilla de curva (SUP-196), `rampup_ineficiencias` | Tasa real anual efectiva; mezclar real y nominal → error del motor (SUP-195) |
| Demanda, canales y precios | `canales.<canal>` (cobro, descuentos, bonificaciones, devoluciones, comisiones, logística, derechos y costos de exportación), `mix_demanda`, `precios` (CONSTANTE o SERIE base REAL), `override_precios` (solo simulación) | La demanda y los precios simples se cargan en SIMULAR (un solo lugar) y se aplican encima |
| Arquitectura y escala | `espacio.configuraciones`, `espacio.escalas` (intermedias admitidas), `espacio.incluir_variantes`, trayectorias T1–T3 | Misma configuración por etapa (TRANSICION_DE_ARQUITECTURA_NO_MODELADA) |
| CAPEX / OPEX por alternativa | `etapas[0]`: `capex_usd` + `capex_meta`, `curva_desembolso`, `activos` (clase `MODULO:nombre`, vida útil, residual, reemplazo), `iva_capex` (TF-076), `opex_rubros` (con `meta`: CONFIGURACION, ESCALA, VARIANTE, MODULO, UNIVERSO, ORIGEN), `rampup`, `financiamiento` | Se listan los módulos CAPEX/OPEX que admite la arquitectura. Un monto de otro módulo → **OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA** (error claro); faltar un módulo OPEX → OPEX incompleto |
| Override total | `OVERRIDE_TOTAL_ARQUITECTURA` | Exige confirmación: «Esta simulación pierde parte de la trazabilidad automática». La corrida queda SIMULACION_HIPOTETICA_OVERRIDE_TOTAL y no es comparable con corridas verificadas |
| Impuestos e IVA | `impuestos.*` (IIBB con reglas por mercado TF-005, municipales, otros, ganancias, quebrantos), `iva.*` | IIBB > 0 sin regla → NO_CALCULABLE_REGLA_FISCAL_PENDIENTE |
| Capital de trabajo | `dias_pago.*`, `dias_stock.*`, `dias_caja_operativa`, propiedad de inventarios | Días calendario (365/12 por mes) |
| Deuda y financiamiento | `financiamiento` común (aportes, aporte automático, caja mínima, deudas con tipo de tasa obligatorio, dividendos) | USD 2 M no es un default |
| Stress y status quo | stress del escenario (vacío = `escenarios_stress.csv`), `decision.sq_stress`, `sq_score_ordinal_max`, `sq_cobertura_min` | Magnitudes ilustrativas, no pronósticos (SUP-223) |
| Distribuciones y correlaciones | distribución, parámetros, fuente, estado (PENDIENTE / RESPALDADA / ARTIFICIAL), correlaciones | Monte Carlo del proyecto solo con RESPALDADAS; ARTIFICIAL solo en la demo; correlación vacía ≠ 0 |
| Optimizador | perfil RÁPIDO / COMPLETO, tolerancia, exigir físico, métrica de capital, umbrales 2D, pesos BALANCEADO, pesos del score de riesgo, restricciones HARD/SOFT con penalización | Sin pesos no hay score (no se inventan) |
| Factibilidad física | `disponibilidad` (terreno, agua, potencia, façon, m² de integrados, pollitos, alimento, booleanos de terceros) y `base_valores` (mortalidad, condenas, traslado FX) | Sin dato → FACTIBILIDAD_PENDIENTE, nunca FACTIBLE |
| Evidencia | Umbral vigente (solo lectura) | La evidencia se edita fuera de la app, con fuente y nivel |
| Trazabilidad | **VER DE DÓNDE SALE**: por KPI (CAPEX, OPEX, CT, INGRESOS, EBITDA, FONDOS, VAN, TIR, PAYBACK, DSCR, RIESGO, OPTIMIZADOR, EVIDENCIA) → VARIABLE, ORIGEN, TRANSFORMACIÓN, UNIDAD, EVIDENCIA, TEST (`trazabilidad_end_to_end.csv`) + mapa de drivers de la alternativa (traza del motor: valor, origen, archivo, evidencia) | |
| JSON | Escenario completo editable, «Validar y aplicar», descargar | Se valida antes de aplicar |

## Pareto, dominancia y robustez

En OPTIMIZAR: frontera de Pareto VAN vs fondos iniciales entre alternativas **comparables**; con menos de 2 → «PARETO NO INFORMATIVO». La frontera no es un ranking. La robustez es el % de escenarios de stress y extremos one-way con VAN ≥ 0 (determinístico, no probabilidad).

## Buenas prácticas

- Cargar CAPEX/OPEX por alternativa con su `meta` (la pestaña la completa con la configuración, escala y variante de la alternativa elegida).
- Registrar en `procedencia` (vía JSON) o en «fuente» de los campos simples de dónde sale cada valor.
- Cotizaciones reales: cargarlas en STAGING (Validación) para que el analista las clasifique; usarlas en un escenario solo como ESCENARIO o COTIZACIÓN.
