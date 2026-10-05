# Actualizaciones de gestión — sesión 20 (Riesgos + sensibilidades + optimizador)

**Fecha:** 2026-10-05 · **Rama:** `claude/riesgos-sensibilidades-optimizador-97t4gk` (desde `main` 453d662, posterior al merge de la sesión 19)
**Estado:** PROPUESTA para la próxima reconciliación. Esta sesión **no** modificó `00_gestion_proyecto/`, `25_fuentes/` ni los modelos fuente (`19_capex`, `20_opex`, `21_modelo_financiero`, `04`, `23`, `02`). IDs **provisionales**: `SUP-20-##`, `DPV-20-##`, `DEC-20-##`, `FTE-20-###`.

Últimos IDs oficiales al iniciar: **SUP-188, DPV-177, DEC-092, FTE-322**. Los provisionales de la sesión 19 (SUP-19-##, DPV-19-##, DEC-19-##) siguen pendientes de reconciliación y no se renumeran aquí.

---

## 1. Supuestos propuestos (`supuestos.md`)

Todos son **criterios de la capa de decisión** (cómo se compara), no datos económicos.

| ID provisional | Supuesto | Dónde se usa | Relación |
|---|---|---|---|
| SUP-20-01 | **Shocks one-way** relativos (−30 % … +30 %), en días (−30 … +30) y en meses (−24 … +24): grillas de análisis configurables; **no implican probabilidad** | `inputs_riesgo_optimizacion.csv`, `shocks_de()` | — |
| SUP-20-02 | **Evaluación rápida:** en corridas que no piden la TIR, `mf.tir` se sustituye temporalmente por `NO_CALCULADA_EVALUACION_RAPIDA` (nunca 0) y se restaura; VAN, payback, pico, EBITDA y fondos son idénticos (test SENS-08) | `Evaluador`, `_SinTIR` | SUP-19-25 |
| SUP-20-03 | **NO_INVERTIR_AUN** = status quo: VAN, CAPEX, fondos, pico y EBITDA incrementales = 0 **por definición** (no son faltantes llenados con 0); no incluye costo de oportunidad, valor de la información ni la operación actual de la carnicería | `metricas_status_quo()`, `rankear()` | SUP-003 |
| SUP-20-04 | **Peso vivo (aproximación):** kg comerciales por ave y costo de alimento proporcionales al peso vivo (FCR constante); el balance 04 publica solo 2,9 kg | `_t_peso_vivo()` | DPV-060 |
| SUP-20-05 | **FCR (aproximación):** costo de alimento proporcional al FCR a precio y peso constantes | variable `fcr` | — |
| SUP-20-06 | **Rendimiento de faena (aproximación):** más rendimiento comestible = más kg de productos comestibles; la masa adicional sale de subproductos (la masa por ave no cambia) | `_t_rendimiento()` | DPV-060 |
| SUP-20-07 | **Parámetros técnicos:** grilla de quiebre 24 puntos + bisección (tol 1e-7); Monte Carlo 1.000 simulaciones y semilla 20261005 (solo con distribuciones respaldadas); mínimo 1 escenario para robustez; 10 acciones en QUE_HACER_AHORA | `inputs_riesgo_optimizacion.csv` | — |
| SUP-20-08 | **Preset de pesos `IGUALES`** para el objetivo balanceado (solo si el usuario lo elige; rotulado SUPUESTO) | `pesos_balanceado()` | DEC-20-01 |
| SUP-20-09 | **Restricción HARD no evaluable excluye** del ranking (FACTIBILIDAD_PENDIENTE ≠ FACTIBLE); exigir gates físicos confirmados es opcional | `rankeable()` | regla 3 |
| SUP-20-10 | **CAPITAL_DISPONIBLE se compara contra el PICO_FONDOS** por defecto (incluye pérdidas del ramp-up y CT); alternativa: FONDOS_INICIALES | `capital.metrica` | T19-02 |
| SUP-20-11 | **Componentes faltantes en scores** (riesgo, balanceado): SEPARAR por defecto (score PENDIENTE); PENALIZAR (= peor) opcional | `score_riesgo()`, `score_balanceado()` | — |
| SUP-20-12 | **Magnitudes de stress ilustrativas** tomadas de `STRESS_PREDEFINIDOS` de 21 (demanda −30 %, alimento +20 %, precio −10 %, CAPEX +25 %, ramp-up ×2); stress financiero sin magnitud | `escenarios_stress.csv` | SUP-19-23 |
| SUP-20-13 | **Probabilidad cualitativa del registro** = frecuencia **sectorial** de 01 §11 cuando existe (no es probabilidad del proyecto); "Media–alta" / "Medio–alto" se redondean a ALTA | `registro_riesgos.csv` | regla 16 |
| SUP-20-14 | **Matriz cualitativa 3×3** con clases BAJO / MODERADO / ALTO / CRÍTICO; sin producto numérico P × I | `CLASE_CUALITATIVA` | — |
| SUP-20-15 | **Robustez** = comportamiento en escenarios deterministas (stress activos + extremos one-way de `robustez.variables`); no es una muestra probabilística | `escenarios_robustez()` | — |
| SUP-20-16 | **Asset-light** (faena a façon): terreno, agua y potencia propios requeridos = 0 para las restricciones físicas | `valor_restriccion()` | DEC-002 |
| SUP-20-17 | **COBERTURA_EVIDENCIA** = bloques del motor completos en modo EVIDENCIA ÷ 17 para la misma configuración y escala; mide confianza, no rentabilidad | `cobertura_evidencia()` | SUP-19-02 |
| SUP-20-18 | **VELOCIDAD, CONTROLABILIDAD, DETECTABILIDAD** del registro de riesgos: estimaciones cualitativas revisables; el IMPACTO sin clasificación de 01 se estima por el bloque del motor que afecta | `registro_riesgos.csv` | — |
| SUP-20-19 | **Clasificación de rubros por driver** por prefijo de `COSTO_ID` de 20 (ALI-, POL-, UT-ELE-, LAB-, EMP-, LOG-, FAE-FACON…) y, si falta, por `GRUPO_PROVEEDOR`; el usuario puede declarar `driver_riesgo` | `clasificar_rubro()` | matriz_validacion_opex.csv |

## 2. Datos por validar propuestos (`datos_por_validar.md`)

| ID provisional | Dato | Para qué | Relación |
|---|---|---|---|
| DPV-20-01 | **Interfaz de días operativos:** recalcular OPEX y capacidad con días distintos de 250/300 sin romper la coherencia costo/capacidad | Sensibilidad continua de días operativos (hoy NO_SOPORTADA; se usa la variante C1-6dias) | DEC-033, SUP-025 |
| DPV-20-02 | **Plazo de recupero del IVA** (saldo técnico, bienes de capital) parametrizable en el motor | Sensibilidad de recupero de IVA (hoy NO_SOPORTADA) | **ampliar DPV-169** |
| DPV-20-03 | **Ampliar el mapa de arquitecturas** con combinaciones físicamente válidas relevantes (1.450 no mapeadas) | Evaluar más combinaciones en el optimizador | mapa_arquitecturas_economicas.csv |
| DPV-20-04 | **Moneda original por rubro de OPEX y precio** (ARS / USD) transportada hasta la entrada del motor | Exposición cambiaria (FX) real; hoy solo ítems con `moneda_original = ARS` declarados | DEC-006, regla 2 |
| DPV-20-05 | **Distribuciones respaldadas:** series históricas (precio de pollo y cortes, maíz, harina de soja, FX, tarifas) y dispersión de cotizaciones de CAPEX y OPEX | Monte Carlo del proyecto | **ampliar DPV-013, DPV-050, DPV-157** |
| DPV-20-06 | **Coeficientes de correlación con fuente** (pollo/alimento, maíz/soja, FX/costos, demanda/precio, utilización/eficiencia, inflación/salarios y tarifas) | Cópula del Monte Carlo | DPV-20-05 |
| DPV-20-07 | **Disponibilidades físicas confirmadas** por sitio: terreno, potencia, agua, m² de galpón de integrados, pollitos/semana, alimento t/semana, capacidad de façon, receptor de subproductos, transporte, frío de terceros | Gates de factibilidad física | **ampliar DPV-087, DPV-095, DPV-053, DPV-048, DPV-006, DPV-050** |
| DPV-20-08 | **Valores base** de mortalidad, condenas, FCR y traslado de una devaluación a precios en ARS | Variables REQUIERE_BASE (sensibilidad y quiebre en valores absolutos) | DPV-019, DPV-060 |
| DPV-20-09 | **CAPEX desglosado por clase de activo** (equipos, obra, frío, efluentes, terreno, instalación, importación, contingencia) | Sensibilidad de CAPEX por bloque | **ampliar DPV-167** |
| DPV-20-10 | **Capacidad de façon** (faena y alimento) disponible y su estabilidad | Gate FACON_FAENA / ALIMENTO_FACON y riesgo RG-13 | **ampliar DPV-006, DPV-155** |

## 3. Decisiones pendientes propuestas (`decisiones_pendientes.md`)

| ID provisional | Decisión | Opciones | Quién | Relación |
|---|---|---|---|---|
| DEC-20-01 | **Objetivo(s) de optimización** y pesos del objetivo balanceado | MAX_VAN, MIN_FONDOS, MIN_PAYBACK, MIN_RIESGO, MAX_ROBUSTEZ, BALANCEADO (pesos) | Inversor / promotor | DEC-007 |
| DEC-20-02 | **Restricciones duras y blandas** (capital real comprometido, pico máximo, payback máximo, DSCR mínimo, demanda asegurada mínima) | HARD / SOFT con penalización | Inversor | DEC-010, DEC-092 |
| DEC-20-03 | **Pesos del score de riesgo** y tratamiento de faltantes | SEPARAR / PENALIZAR | Inversor | — |
| DEC-20-04 | **Umbrales de alerta** del registro de riesgos (UAD) | por indicador | Promotor | gates_expansion.md |
| DEC-20-05 | **Tolerancia de equivalencia** entre mejor y segunda alternativa | % de diferencia | Inversor | — |
| DEC-20-06 | **Criterio de robustez y magnitudes de stress** | % escenarios VAN ≥ 0 / peor VAN / P10 VAN; magnitudes por variable | Inversor | SUP-20-12 |
| DEC-20-07 | **Extender la interfaz financiera** a transiciones de arquitectura (C0 → C1 → …) y combinaciones fuera del mapa | sí / no / cuándo | Equipo del estudio | DPV-20-03, T19-04 |

## 4. Fuentes (`registro_fuentes.csv`)

Sin fuentes nuevas: la sesión no consultó documentos externos. La probabilidad cualitativa del registro reutiliza la tabla de amenazas de `01_mercado/mercado_avicola_argentina.md` §11 (con sus fuentes ya registradas).

## 5. Estado del proyecto (`estado_proyecto.md`)

Hito a registrar: **Sesión 20 — capa de riesgo, sensibilidades y optimizador v1.0**: 52 tests, 19/19 mutaciones; `OPTIMIZACION_REAL_NO_DISPONIBLE` (0/54 alternativas con VAN publicable en evidencia); universo ESCENARIO listo y vacío; Monte Carlo del proyecto no disponible por falta de distribuciones; registro de 34 riesgos cualitativos; prioridad de validación derivada del motor.

## 6. Glosario (`glosario.md`)

Términos a agregar: **sensibilidad one-way**, **tornado**, **sensibilidad bidimensional**, **stress test**, **punto de quiebre**, **Monte Carlo**, **cópula gaussiana**, **frontera de Pareto**, **dominancia**, **robustez**, **riesgo inherente / residual**, **valor de la información**, **asset-light**, **OPTIMIZACION_REAL_NO_DISPONIBLE**, **NINGUNA_CONFIGURACION_FACTIBLE**, **DECISION_NO_ROBUSTA**, **COBERTURA_EVIDENCIA**.

## 7. Tensiones nuevas

| ID | Tensión | Qué la cierra |
|---|---|---|
| T20-01 | **Empate de prioridades:** en modo evidencia nueve faltantes bloquean todos los indicadores en todas las alternativas; el modelo no puede decir cuál pesa más sin un escenario | Primer escenario del promotor (tornado) |
| T20-02 | **Espacio evaluable limitado al mapa:** 1.450 combinaciones válidas no son evaluables por la interfaz financiera | DPV-20-03, DEC-20-07 |
| T20-03 | **Exposición cambiaria subrepresentada:** el adaptador OPEX de 21 no transporta la moneda original | DPV-20-04 |
| T20-04 | **Probabilidad sectorial vs del proyecto:** el registro usa frecuencias sectoriales de 01 como mejor información disponible | Evidencia específica del proyecto |
