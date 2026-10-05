# Actualizaciones de gestión — sesión 19 (Modelo financiero integral)

> **ARCHIVO HISTÓRICO (2026-10-05).** Las propuestas de este documento se integraron en los registros centrales en la [reconciliación de las sesiones 19–20](../00_gestion_proyecto/reconciliacion_sesiones_19_20.md) (sesión 21); el mapa ID provisional → ID central está en su §2 (SUP-189 a SUP-211, DPV-178, DEC-093 a DEC-096, más consolidaciones en registros existentes). Los IDs provisionales `SUP-19-##`, `DPV-19-##` y `DEC-19-##` que aparecen abajo **ya no están activos**; no editar este archivo.

**Fecha:** 2026-10-04 · **Rama:** `claude/modelo-financiero-integral-llcp3s` (desde `main` 733a166, posterior al merge de la reconciliación 18)
**Estado:** PROPUESTA para la próxima reconciliación. Esta sesión **no** modificó `00_gestion_proyecto/`, `25_fuentes/` ni los modelos fuente (`19_capex`, `20_opex`, `04`, `23`, `02`). IDs **provisionales**: `SUP-19-##`, `DPV-19-##`, `DEC-19-##`, `FTE-19-###`.

Últimos IDs oficiales al iniciar: **SUP-188, DPV-177, DEC-092, FTE-322**.

---

## 1. Supuestos propuestos (`supuestos.md`)

Todos son **criterios de modelo** (cómo se calcula), no datos económicos.

| ID provisional | Supuesto | Dónde se usa | Relación |
|---|---|---|---|
| SUP-19-01 | **Jerarquía de inputs:** EVIDENCIA_REAL > ESCENARIO_USUARIO > SUPUESTO_MODELO > PENDIENTE; el escenario completa faltantes, nunca reemplaza una evidencia ni escribe sobre la base | `resolver()`, `construir_entrada()` | SUP-164 |
| SUP-19-02 | **`UMBRAL_EVIDENCIA_PUBLICACION` configurable** (fila `umbral_evidencia_publicacion` de `inputs_financieros.csv`, se cambia sin tocar código). Default conservador **E1–E3** con 100 % de bloques materiales; E4 `[PVDP]` y E5 no pasan el default. Cada corrida registra el umbral usado. **No es la decisión de DEC-19-01** | `umbral_evidencia()`, `resolver()`, `publicabilidad()` | DEC-084, DEC-19-01 |
| SUP-19-03 | **Supuestos metodológicos admitidos en modo evidencia:** modelo real, base de la tasa, meses de detalle, método de valor terminal por defecto, recupero de CT, moneda funcional, convención de descuento | `SUPUESTOS_METODOLOGICOS` | — |
| SUP-19-04 | **Tiempo:** motor mensual (k = 0 es T0); descuento a fin de período con tasa anual efectiva y t = k/12 | `simular()`, `van()` | DEC-007 |
| SUP-19-05 | **Categorías de demanda:** DOCUMENTADA y ASEGURADA = A; NEGOCIADA = B (× α, DEC-014); INTERESADA entre B y C; POTENCIAL = C/D; ESCENARIO = hipótesis del usuario. El modo evidencia solo vende A | `_lineas_contables()` | 02 §1, SUP-004, DEC-014 |
| SUP-19-06 | **Reporte:** mensual los primeros 24 meses, anual después (editable; múltiplo de 12) | `periodos_reporte()` | — |
| SUP-19-07 | **Modelo REAL** en USD constantes de 2026-10-01, sin inflación; tasa en la misma base que los flujos; nominal solo con inflación declarada | `validar_entrada()` | DEC-006, SUP-155 |
| SUP-19-08 | **Utilización:** técnica (curva) · comercial (parte limitante, criterio de 23; puede > 1) · efectiva = mín(técnica, comercial). Capacidad = escala operativa de 23 × días ÷ 12; en una expansión rigen los días de la etapa activa | `simular()` | SUP-052, SUP-060 |
| SUP-19-09 | **Curvas de ramp-up CONSERVADOR / BASE / RÁPIDO**: ilustrativas, sin fuente, solo utilización técnica; merma, eficiencia y costos extra PENDIENTES | `curvas_rampup.csv` | DEC-090, SUP-181 |
| SUP-19-10 | **OPEX por período:** rubros de 20_opex a escala plena de la etapa activa; variable × u ÷ eficiencia; fijo y semifijo enteros desde el inicio de operación; semifijo salta de escalón entre etapas; OPEX = 0 antes de operar (preoperativos en CAPEX PRE-*) | `simular()` | SUP-180, SUP-181, interfaz OPEX §1 |
| SUP-19-11 | **Capital de trabajo por días** sobre `DIAS_MES = 365 ÷ 12`: inventario = días × costo de la base; CxC = ingreso neto (sin IVA) × días de cobro; CxP = compras × días de pago; sueldos fuera de CxP; caja operativa sin política = 0 `NO_ASIGNADA` (convención de 20) | `simular()` | interfaz OPEX §6, DEC-091 |
| SUP-19-12 | **Valor terminal por defecto = SIN_VALOR_TERMINAL**; sin recupero de CT; la deuda remanente al cierre se cancela en el FCFE | `valor_terminal`, `simular()` | DEC-19-03 |
| SUP-19-13 | **Ganancias** anual al cierre de cada año del proyecto, sin anticipos; quebrantos con vencimiento; intereses y comisiones deducibles en la vista con deuda; el valor terminal no se grava; base = depreciación contable (aproximación hasta DPV-169) | `simular()` | DPV-169 |
| SUP-19-14 | **Deuda:** interés = saldo × tasa del período de servicio según `tipo_tasa` declarado (ver SUP-19-26); gracia solo intereses; un desembolso por tramo; moneda USD; `base_tasa` = modelo monetario | `cronograma_deuda()`, `tasa_deuda_periodo()` | DEC-092 |
| SUP-19-15 | **IVA simplificado:** débito sobre venta interna neta de descuentos, bonificaciones y devoluciones; crédito sobre compras marcadas y CAPEX; arrastre del saldo a favor; efecto de caja = −Δ saldo; exportación sin débito; sin recupero anticipado, percepciones ni retenciones | `simular()` | DPV-169, DPV-043 |
| SUP-19-16 | **Inventario de producto:** FIFO; por defecto sin arrastre (`inventario_max_meses = 0`): el excedente no vendido se informa y no se monetiza | `simular()` | DEC-058 |
| SUP-19-17 | **Asignación de ventas:** por prioridad de la línea; prorrata dentro de la misma prioridad; `toma_todo` solo recibe lo que sobra | `simular()` | — |
| SUP-19-18 | **Depreciación** lineal contable desde la entrada en operación; terreno no depreciable; reposición al fin de la vida útil con costo de reemplazo | `simular()` | DPV-167 |
| SUP-19-19 | **Fondos iniciales:** CT inicial = máximo CT hasta el fin del ramp-up inicial; otros = máximo saldo de IVA a favor antes de operar + intereses y comisiones antes de operar + reservas declaradas. Pico de fondos = −mínimo del FCFF acumulado | `resultados()` | interfaz CAPEX §1 |
| SUP-19-20 | **Break-even** sobre el último año del horizonte con el mismo mix y precios; IIBB y tasas proporcionales al precio | `break_even_anual()` | — |
| SUP-19-21 | **Subproductos por arquitectura:** C0 (façon) = kg PENDIENTES según contrato (FAE-FACON-SUB); CF = rendering FUTURO → venta cruda en la etapa inicial | `construir_entrada()` | DEC-027, DEC-066 |
| SUP-19-22 | **Trayectorias** solo para configuraciones base (`expansion()` de CAPEX parte de `preset()`); las variantes se evalúan a escala única | `capex_trayectoria()` | T18-16 |
| SUP-19-23 | **Stress:** devaluación = valor USD × (1 + traslado × d) ÷ (1 + d) solo en ítems ARS con traslado declarado; mortalidad = factor (1 − m_base) ÷ (1 − m_nueva) sobre el rubro de pollitos | `simular()` | DEC-006 |
| SUP-19-24 | **Costos comerciales:** logística del canal (adicional al OPEX de 20) y costos de exportación = OPEX comercial antes del EBITDA; comisiones y derechos de exportación = deducciones de la venta | `simular()` | DPV-039, DPV-015 |
| SUP-19-25 | **Tasas y descuento:** `TASA_DESCUENTO` anual efectiva (o nominal anual cap. mensual declarada y convertida); tasa mensual = (1 + r)^(1/12) − 1, nunca r/12; convención por defecto **MENSUAL** (cada flujo mensual descontado en su mes; T0 sin descontar); alternativa `PERIODO_REPORTE` declarada; TIR mensual → anual (1 + i)^12 − 1; payback en meses y años = meses ÷ 12 | `tasa_periodica()`, `tasa_anual_efectiva()`, `van_periodico()`, `anualizar()`, `indicadores()` | DEC-007, DEC-19-08 |
| SUP-19-26 | **Tasa de deuda con tipo obligatorio:** EFECTIVA_ANUAL → (1 + TEA)^(f/12) − 1; NOMINAL_ANUAL → TNA × f ÷ 12 solo si capitalización = frecuencia; PERIODICA → solo si su período = frecuencia; cualquier otra combinación → error | `tasa_deuda_periodo()` | DEC-092 |
| SUP-19-27 | **Capa `OVERRIDE_SIMULACION`** (solo escenario): permite evaluar un valor distinto del observado (precio u otra variable) registrando `VALOR/PRECIO_OBSERVADO` y `VALOR/PRECIO_EVALUADO_ESCENARIO`; la base de evidencia no se modifica; la corrida queda rotulada `SIMULACION_HIPOTETICA_NO_VALIDADA` | `construir_entrada()` | SUP-19-01 |
| SUP-19-28 | **Derechos de exportación: ubicación única** = deducción de la venta de exportación (`canales.exportacion.pct_derechos_exportacion`); el módulo de impuestos rechaza esa clave y no se restan otra vez antes del EBITDA | `validar_entrada()`, `simular()` | DPV-015, SUP-19-24 |
| SUP-19-29 | **Corridas con `ID_CORRIDA` único** `MODO\|CONFIGURACION\|VARIANTE\|ESCALAS\|TRAYECTORIA\|ESCENARIO`; sin duplicados de contenido; trayectorias de referencia solo para C1 (`LIMITACION_ACTUAL_EXPANSION_C1`); `configuracion_por_fase` preparada pero sin transiciones de arquitectura | `id_corrida()`, `firma_corrida()`, `construir_entrada()` | DEC-033 |

## 2. Datos por validar propuestos (`datos_por_validar.md`)

| ID provisional | Dato | Para qué | Relación |
|---|---|---|---|
| DPV-19-01 | **Curva de desembolso del CAPEX:** hitos de pago y anticipos por paquete (línea, frío, obra, efluentes), plazos de fabricación, montaje y entrega | `CURVA_DE_DESEMBOLSO_CAPEX`, intereses durante la obra | **ampliar DPV-086, DPV-167** |
| DPV-19-02 | **Condiciones comerciales de todos los canales** (mayoristas, carnicerías/pollerías, gastronomía, industria, exportación): descuentos, bonificaciones, devoluciones, comisiones, fees logísticos, plazos de cobro | Ingreso neto y CxC por canal | **ampliar DPV-039** (hoy solo supermercados) |
| DPV-19-03 | **Duración de preoperación, construcción y commissioning** (permisos, habilitación SENASA, obra, montaje, pruebas) | Fases y línea de tiempo | **ampliar DPV-086** |
| DPV-19-04 | **Costo de capital del grupo inversor** (rendimiento exigido, horizonte) | `TASA_DESCUENTO`, `tasa_descuento_accionista` | **ampliar DPV-001**; DEC-007 |
| DPV-19-05 | **Financiamiento disponible:** bancos, programas públicos, leasing, financiación de proveedores: monto, moneda, tasa, plazo, gracia, garantías, comisiones, DSCR exigido | Módulo de financiamiento | DEC-092 |
| DPV-19-06 | **Reglas fiscales completas:** alícuota de ganancias, quebrantos, IIBB por jurisdicción, tasas municipales, IVA por producto, IVA de bienes de capital y su recupero, amortización impositiva | Módulo de impuestos | **ampliar DPV-043, DPV-169** |
| DPV-19-07 | **Ineficiencias del arranque** en plantas avícolas argentinas: merma, conversión, rendimiento de línea, horas extra durante los primeros meses | Curva de ramp-up | **ampliar DPV-088**; DEC-090 |
| DPV-19-08 | **Vida útil contable y fiscal** por clase de activo | Depreciación, reposición, valor libro | **ampliar DPV-167, DPV-169** |
| DPV-19-09 | **Días de inventario** de producto terminado, packaging, repuestos e insumos y su método de valuación | Capital de trabajo | **ampliar DPV-175**; DEC-089 |
| DPV-19-10 | **Vida comercial del producto** refrigerado y congelado (cuánto puede guardarse un excedente) y capacidad de frío para hacerlo | `inventario_max_meses` | DEC-058 |
| DPV-19-11 | **Signo del ingreso por subproductos crudos:** precio de venta vs costo de retiro por material y receptor | Ingreso SUBPRODUCTOS vs OPEX de retiro | **ampliar DPV-072, DPV-076** |

## 3. Decisiones propuestas (`decisiones_pendientes.md`)

| ID provisional | Tipo | Decisión | Relación |
|---|---|---|---|
| DEC-19-01 | METODOLÓGICA | **Umbral de publicación del modo evidencia** (ampliación de DEC-084): ¿se acepta E4 en algún bloque? ¿se aceptan los rendimientos del balance 04 antes del ensayo en planta? ¿se publica con faltantes no críticos? | DEC-084, DEC-028, SUP-19-02 |
| DEC-19-02 | METODOLÓGICA | **Horizonte de evaluación (10 / 15 / 20 años) y tasa de descuento** de referencia del proyecto y del accionista | **ampliar DEC-007** |
| DEC-19-03 | METODOLÓGICA | **Método de valor residual / terminal** (sin valor, valor libro, explícito, perpetuidad) | SUP-19-12 |
| DEC-19-04 | METODOLÓGICA | **Modelo real vs nominal** y criterio de TC para reportar en ARS | **ampliar DEC-006** |
| DEC-19-05 | NEGOCIO | **Gatillos de expansión:** por fecha o por condición (utilización, demanda asegurada, caja, DSCR, año) y sus umbrales | DEC-033, DEC-035, gates G0–G3 de 23 |
| DEC-19-06 | NEGOCIO | **Política de dividendos y caja mínima** | DEC-092 |
| DEC-19-07 | NEGOCIO | **Política de excedentes de producto** (vender fresco, congelar, canal de liquidación) | DEC-058 |
| DEC-19-08 | METODOLÓGICA | **Base de flujo para publicar indicadores** (¿solo after-tax?), si el break-even oficial es EBITDA o EBIT, y si la convención oficial de descuento es MENSUAL (default) o PERIODO_REPORTE | DEC-084 |

## 4. Fuentes (`registro_fuentes.csv`)

**Ninguna fuente nueva** (`FTE-19-###`: no se asignó ninguna). La sesión no consultó fuentes externas. Las dos referencias de precio de [`base_precios_venta.csv`](base_precios_venta.csv) reutilizan **FTE-004** y **FTE-032** (ya registradas, `[PVDP]`) y quedan como `REFERENCIA_E4_NO_USABLE`.

## 5. Estado del proyecto (`estado_proyecto.md`)

Propuesta de fila para el tablero:

| Módulo | Modelo preliminar | Evidencia de campo | Síntesis |
|---|---|---|---|
| Modelo financiero (`21`) | **MODELO FINANCIERO ESTRUCTURAL COMPLETADO** v1.0 (motor mensual; modos EVIDENCIA y ESCENARIO; 24 configuraciones del mapa + trayectorias de escala de C1; 70 tests, 25/25 mutaciones). **RENTABILIDAD = NO CALCULABLE**: 0 de 61 corridas publicables; ningún bloque completo | Pendiente — precios, demanda A/B, OPEX y CAPEX costeables, fiscal, tasa, financiamiento | [`conclusiones_financieras.md`](conclusiones_financieras.md) |

Matriz central: [`matriz_completitud_economica.csv`](../00_gestion_proyecto/matriz_completitud_economica.csv) puede referenciar [`completitud_financiera.csv`](completitud_financiera.csv) para los bloques financieros (sin cambiar estados: siguen PENDIENTE / PARCIAL).

## 6. Glosario (`glosario.md`)

Términos a agregar: **FCFF** (flujo libre del proyecto), **FCFE** (flujo libre del accionista), **CFADS**, **DSCR**, **MIRR**, **payback descontado**, **valor terminal**, **margen de contribución**, **utilización técnica / comercial / efectiva**, **pico de requerimiento de fondos**, **SIMULACION_HIPOTETICA_NO_VALIDADA**, **NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE**.

## 7. Tensiones nuevas

| ID | Tensión | Qué la cierra |
|---|---|---|
| T19-01 | **Rendimientos modelados vs evidencia:** el modo evidencia no acepta el balance 04 sin ensayo; ingresos nunca publicables hasta DPV-060 o DEC-19-01 | DPV-060, DEC-19-01 |
| T19-02 | **Capital requerido vs CAPEX:** el pico de fondos (pérdidas del ramp-up + ΔCT + IVA) puede superar ampliamente el CAPEX inicial; USD 2 M no es comparable con nada todavía | Datos del §5 de `evidencia_financiera.md` |
| T19-03 | **Plantillas vacías:** las plantillas CONSERVADOR / BASE / EXPANSIVO no producen resultados sin inputs del promotor (decisión deliberada de no rellenar) | Escenarios del promotor |
| T19-04 | **Trayectorias sin prima de ampliación ni valor residual:** comparar 2.500 → 20.000 con 20.000 directo hoy sería artificial | DPV-086, DPV-167 |

## 8. Auditoría financiera final (2026-10-05)

| Punto | Resultado |
|---|---|
| Discrepancia 28,89 vs 51,63 | Eran dos casos distintos informados como uno: after-tax (tasa fiscal de test 30 %, FCFF 34) y pre-tax (sin ganancias, FCFF 40), ambos con convención de fin de año no declarada. Ahora: `CP-PRETAX-ANUAL`, `CP-AFTERTAX-ANUAL`, `CP-PRETAX-MENSUAL`, `CP-SIN-RECUPERO`, `CP-COBRO-30D` (tests C01–C03) |
| Tasas, VAN, TIR, payback | SUP-19-25 (tests R01–R04) |
| Deuda | SUP-19-26 (test R05) |
| Real vs nominal | Error explícito ante cualquier mezcla, incluida la deuda (tests N08, R06) |
| Umbral de evidencia | Configurable (SUP-19-02, test U01) |
| Escenario vs evidencia | `OVERRIDE_SIMULACION` (SUP-19-27, test O01) |
| Derechos de exportación | Ubicación única (SUP-19-28, test X01) |
| 61 corridas | IDs únicos y reconstruibles (SUP-19-29, test ID01) |
| Expansión | `LIMITACION_ACTUAL_EXPANSION_C1`; misma configuración por escala; transiciones bloqueadas (test EX01) |
| Tests | 70/70; mutaciones 25/25 |
