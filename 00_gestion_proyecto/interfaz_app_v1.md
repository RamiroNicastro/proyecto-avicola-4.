# Interfaz del motor para la app v1 (contrato)

**Fecha:** 2026-10-05 · **Origen:** sesión 21 (auditoría + reconciliación final del motor) · **Estado:** contrato de datos **definido**; la app se construyó en la sesión 22 ([`../app/README.md`](../app/README.md)).

> Este documento define **qué puede pedir y qué puede mostrar** una app sobre el motor v1 (módulos `03` a `22`). No define pantallas, tecnología ni flujo de usuario. Toda cifra que la app muestre sale del motor con su **etiqueta**; la app no calcula, no completa faltantes y no convierte un `None` en 0. Auditoría que respalda este contrato: [`auditoria_final_motor_v1.md`](auditoria_final_motor_v1.md).

---

## 1. Principios del contrato

1. **Dos universos que no se mezclan.** `EVIDENCIA` (solo datos dentro de `UMBRAL_EVIDENCIA_PUBLICACION`, default E1–E3, SUP-190) y `ESCENARIO` (inputs del usuario, rotulado `SIMULACION_HIPOTETICA_NO_VALIDADA`). La app nunca muestra un número de escenario sin su rótulo ni lo guarda como evidencia (SUP-189).
2. **Faltante ≠ 0.** Un campo vacío es `PENDIENTE`; la app lo muestra como faltante con el DPV o la DEC que lo resuelve (SUP-164, SUP-185).
3. **El motor es la única función de cálculo.** La app llama a `modelo_financiero` (21) y a `modelo_optimizador` / `motor_riesgo` (22), que consumen 03–20. No replica fórmulas.
4. **Ninguna decisión empresarial dentro de la app.** Objetivos, restricciones, pesos, umbrales y capital son inputs del usuario (DEC-097, DEC-098, DEC-099, DEC-101, DEC-102); la app no tiene defaults empresariales.
5. **USD 2 M no es un default.** El capital disponible es un input opcional; vacío = sin restricción de capital (SUP-003, SUP-221).
6. **Los ~90 supermercados no son demanda.** La app puede cargarlos como demanda `POTENCIAL` o `ESCENARIO`, pero su respaldo comercial se muestra aparte y es 0 % mientras no haya demanda `DOCUMENTADA`/`ASEGURADA` (SUP-193).

## 2. Entradas (INPUTS)

Formato: el JSON del modo escenario de 21 ([`plantilla_escenario_usuario.json`](../21_modelo_financiero/plantilla_escenario_usuario.json)) y, para el optimizador, [`escenario_optimizador.json`](../22_riesgos/escenario_optimizador.json) (`comun` + `por_alternativa` + `base_valores` + `disponibilidad`). Todo `null` = PENDIENTE.

| Input | Campo del motor | Unidad | Validación del motor | Si falta |
|---|---|---|---|---|
| **Objetivo** | `optimizador.objetivos` (MAX_VAN, MAX_TIR, MIN_PAYBACK, MIN_FONDOS_INICIALES, MIN_CAPEX, MIN_PICO_FONDOS, MAX_EBITDA, MAX_DSCR, MIN_RIESGO, MAX_ROBUSTEZ, MAX_CRECIMIENTO, BALANCEADO) | — | objetivo inexistente → error | se corren todos (`TODOS`); ninguno se declara "el" objetivo (DEC-097) |
| Pesos del objetivo balanceado | `balanceado.peso.*`, `balanceado.preset` | adimensional | se normalizan | `PESOS_NO_DEFINIDOS` (el preset IGUALES solo si el usuario lo elige, SUP-219) |
| **Capital** | `restriccion.CAPITAL_DISPONIBLE.valor/tipo`, `capital.metrica` | USD | se compara con `PICO_FONDOS` (default) o `FONDOS_INICIALES` | sin restricción de capital |
| **Demanda** | `demanda[]` {producto, canal, mercado, categoria, valor, unidad, prioridad, toma_todo}; `mix_demanda`; `categorias_demanda_usadas`; `alfa_negociada` | kg/día calendario, t/día, t/mes, t/año | producto debe existir en el balance; canal y categoría admitidos; ventas ≤ mín(producción, demanda) | `DEMANDA` faltante (bloquea ingresos) |
| **Precios** | `precios["producto\|canal\|mercado"]` = CONSTANTE o SERIE (base REAL) | USD/kg (ARS solo con TC, fecha y tipo de TC: SUP-187) | serie incompleta → faltante; no se extrapola | `PRECIOS` faltante |
| Precio hipotético sobre uno observado | `override_precios`, `override_simulacion` | USD/kg | registra observado y evaluado (SUP-211) | — |
| Condiciones comerciales | `canales.<canal>` {dias_cobro, pct_descuentos, pct_bonificaciones, pct_devoluciones, pct_comisiones, costo_logistico_usd_kg; exportación: pct_derechos_exportacion, costo_exportacion_usd_kg} | días; fracción; USD/kg | derechos de exportación solo en el canal exportación (SUP-210) | `CANALES` / `CT` faltante |
| **Arquitectura** | `configuracion` ∈ C0, C1, C2, C3, CF; `escenario_capex` = variante del mapa | — | debe existir en [`arquitecturas_maestras.csv`](arquitecturas_maestras.csv); transición entre arquitecturas → `TRANSICION_DE_ARQUITECTURA_NO_MODELADA` | — |
| **Escala** | `escalas` = [E] o trayectoria creciente (T1–T3) | aves/día operativo (2.500–20.000; intermedias admitidas) | escala fuera de rango → gate ESCALA NO_FACTIBLE; escalas no crecientes → error | — |
| Calendario | variante `C1-6dias` (300 d) o base (250 d) | días operativos/año | días arbitrarios NO_SOPORTADOS (TF-001) | 250 d (5 días/semana) |
| Tiempo | `valores.horizonte_anios`, `meses_preoperacion`, `meses_construccion`, `meses_commissioning`, `fecha_inicio` | años; meses | horizonte entero ≥ 1 | `TIEMPO` faltante |
| Tasa | `valores.tasa_descuento`, `tasa_descuento_accionista`, `tipo_tasa_descuento`, `convencion_descuento` | anual efectiva (o nominal cap. mensual declarada) | real vs nominal mezclados → error (SUP-195) | `DESCUENTO` faltante |
| CAPEX y OPEX del usuario | `etapas[].capex_usd` + `capex_meta`, `activos`, `opex_rubros[]` (cada uno con `meta`), `curva_desembolso` | USD; USD/año a escala plena | metadatos CONFIGURACION, ESCALA, VARIANTE, MODULO, UNIVERSO, ORIGEN obligatorios y compatibles con [`arquitecturas_maestras.csv`](arquitecturas_maestras.csv) y los módulos de la corrida → si no, `OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA`; OPEX debe cubrir todos los módulos de la arquitectura; Σ activos = CAPEX; curva suma 1 | se usan los de 19/20 solo si su total es publicable; si no, faltante |
| Override total | `OVERRIDE_TOTAL_ARQUITECTURA` = TRUE | — | solo TRUE / FALSE | sin flag no hay override sin control; con flag la corrida es `SIMULACION_HIPOTETICA_OVERRIDE_TOTAL` con trazabilidad parcial |
| IVA del CAPEX | `etapas[].iva_capex` {base NETA, iva_estado DECLARADO, tasa, condicion_fiscal, elegible_credito, criterio} | fracción | IVA incierto → `CREDITO_FISCAL_IVA_CAPEX = PENDIENTE` | sin crédito ni costo; flujo no publicable con IVA SIMPLIFICADO |
| Ramp-up | `plantilla` (curva ilustrativa SUP-196) o `etapas[].rampup`; `rampup_ineficiencias` | fracción por mes | — | `RAMPUP` faltante |
| CT | `dias_pago.*`, `dias_stock.*`, `dias_caja_operativa`, `inventarios` | días | propiedad del inventario según arquitectura | `CT` faltante |
| Impuestos e IVA | `impuestos.*` (incluye las reglas `iibb_aplica_domestico` / `iibb_aplica_exportacion`), `iva.*` | fracción; TRUE/FALSE | claves no admitidas → error; con IIBB > 0 y regla vacía → `NO_CALCULABLE_REGLA_FISCAL_PENDIENTE` | `IMPUESTOS_INGRESOS`, `GANANCIAS`, `IVA` faltantes |
| Financiamiento | `financiamiento` {aportes, deudas (tipo de tasa obligatorio), politica_dividendos, caja_minima_usd} | USD; meses | tasa sin tipo o ambigua → error (SUP-200) | `FINANCIAMIENTO` faltante (no bloquea el FCFF) |
| **Shocks** | one-way (`sensibilidad.variables`, `shocks_*`), 2D (`sens2d.pares`), stress (`escenarios_stress.csv` o `stress` del JSON) | relativo / días / meses | solo en ESCENARIO; en EVIDENCIA → error | sin shocks |
| Valores base para shocks absolutos | `base_valores` {mortalidad, condenas, traslado_fx} | fracción | — | esas sensibilidades = NO_CALCULABLE |
| **Restricciones** | `restriccion.<NOMBRE>.valor/tipo/penalizacion` (CAPITAL_DISPONIBLE, FONDOS_INICIALES, PICO_FONDOS, PAYBACK, VAN, TIR, DSCR, DEMANDA_ASEGURADA, UTILIZACION, SUPERFICIE_TERRENO, AGUA, POTENCIA, CAPACIDAD, DEUDA, RIESGO) | según métrica | HARD no evaluable excluye del ranking (SUP-220) | sin restricción |
| Disponibilidades físicas | `disponibilidad` (terreno_m2, agua_m3_dia, potencia_kw, capacidad_linea_aves_h, facon_faena_aves_dia, m2_galpon_integrados, pollitos_semana, alimento_t_semana, …) | m², m³/día, kW, aves/h, … | — | gate `FACTIBILIDAD_PENDIENTE` (nunca FACTIBLE) |
| Umbral de evidencia | fila `umbral_evidencia_publicacion` de `inputs_financieros.csv` | niveles E1–E5 | valor inválido → error | default E1–E3 (DEC-084 abierta) |

## 3. Salidas (OUTPUTS)

| Output | Campo / archivo del motor | Unidad | Condición para mostrar un número |
|---|---|---|---|
| **Inversión** | `CAPEX_INICIAL`, `CAPEX_EXPANSION`, `CAPEX_REPOSICION` (resultados de 21); detalle en BOQ de 19 | USD | bloque CAPEX completo; si no, `TOTAL NO DISPONIBLE` + conceptos sin precio |
| **OPEX** | serie `opex_total` (fijo, variable, semifijo) de 21; registro de 20 | USD/mes; USD/año | bloque OPEX completo (arquitectura costeable) |
| **Fondos** | `FONDOS_INICIALES`, `PICO_REQUERIMIENTO_FONDOS`, `MES_VALLE_CAJA`, `CT_INICIAL`, `CT_MAXIMO` | USD; mes | `PUBLICABLE_FLUJO` |
| **Ingresos** | `VENTA_BRUTA_ULTIMO_ANIO`, `INGRESO_NETO_ULTIMO_ANIO`; series por categoría de ingreso | USD/año | `PUBLICABLE_INGRESOS` |
| **EBITDA** | `EBITDA_ULTIMO_ANIO`, `MARGEN_EBITDA_ULTIMO_ANIO` | USD/año; fracción | `PUBLICABLE_EBITDA` |
| **VAN / TIR** | `VAN`, `TIR`, `TIR_MENSUAL`, `TIR_ESTADO`, `MIRR`; `VAN_ACCIONISTA`, `TIR_ACCIONISTA` (siempre rotuladas "del accionista") | USD; %/año | `PUBLICABLE_VAN` / `PUBLICABLE_TIR` / `PUBLICABLE_FLUJO_ACCIONISTA`; TIR NO_EXISTE / AMBIGUA / NO_CALCULADA se muestran como estado |
| **Payback** | `PAYBACK_SIMPLE_MESES/ANIOS`, `PAYBACK_DESCONTADO_*`, `PAYBACK_*_ESTADO` | meses; años | `PUBLICABLE_PAYBACK`; `NO_RECUPERADO` como estado |
| Break-even y DSCR | `BE_UTILIZACION_EBITDA`, `BE_PRECIO_MEDIO_USD_KG_EBITDA`, `DSCR_MINIMO` | fracción; USD/kg | `PUBLICABLE_BREAK_EVEN`, `PUBLICABLE_DSCR` |
| **Riesgo** | `matriz_riesgos.csv` (cualitativo), `SCORE_ORDINAL_RIESGO` (no es probabilidad), tornado, 2D, stress, quiebres, Monte Carlo | — | MC solo con distribuciones respaldadas (hoy `NO_DISPONIBLE`) |
| **Robustez** | `ROBUSTEZ`, `PCT_ESCENARIOS_VAN_NO_NEG`, `PEOR_VAN`, `P10_VAN` | fracción; USD | ≥ 3 escenarios comparables (SUP-226) |
| **Ranking** | `resultados_optimizador.csv` (RANK, SCORE, MOTIVO), `decision_optimizador.csv` (MEJOR, SEGUNDA, DECISION_ESCENARIO, REGLA_STATUS_QUO, ROBUSTEZ_DECISION), `frontera_pareto.csv`, `DOMINADA` | — | solo alternativas comparables; `PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE` con < 2 |
| Factibilidades | `FACTIBILIDAD_FISICA`, `FACTIBILIDAD_ECONOMICA`, `FACTIBILIDAD_FINANCIERA`, `RESPALDO_COMERCIAL`, `COBERTURA_EVIDENCIA` | — | siempre separadas; nunca un `FACTIBLE` único |
| Coberturas | [`cobertura_motor.csv`](cobertura_motor.csv): estructural, física, económica, evidencia | % | siempre las cuatro por separado |
| **Faltantes** | `FALTANTES` (por bloque), `PUBLICABLE_*_MOTIVO`, `prioridad_validacion.csv` | — | siempre |
| **Qué hacer ahora** | `que_hacer_ahora.csv` (ACCION, DPV_VINCULADOS, RANK_COMPARTIDO, EMPATE, `POTENCIAL_DE_CAMBIAR_DECISION`) | — | empates se muestran como empates; `POTENCIAL_DE_CAMBIAR_DECISION` = `NO_CALCULADO` en evidencia |

## 4. Etiquetas obligatorias

| Etiqueta de la app | Valores del motor que la activan | Qué significa |
|---|---|---|
| **Evidencia** | `MODO_EVIDENCIA`; `EVIDENCIA_REAL` con nivel dentro del umbral | dato observado E1–E3 (o el umbral declarado) |
| **Escenario** | `ESCENARIO_USUARIO`, `SUPUESTO_MODELO` en modo escenario, `ESCENARIO` (categoría de demanda) | hipótesis del usuario o plantilla ilustrativa |
| **Simulación** | `SIMULACION_HIPOTETICA_NO_VALIDADA`, `SIMULACION_HIPOTETICA_OVERRIDE_TOTAL` (con trazabilidad parcial), `OVERRIDE_SIMULACION`, `PROBABILIDAD_SIMULADA_NO_HISTORICA`, `SUPUESTO_INDEPENDENCIA_ESCENARIO` | resultado calculado sobre hipótesis; no es evidencia ni pronóstico |
| **Pendiente** | `PENDIENTE`, `VACIO` (bloque sin contenido), `NO_CALCULABLE_REGLA_FISCAL_PENDIENTE`, `CREDITO_FISCAL_IVA_CAPEX = PENDIENTE`, `NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE`, `NO_DISPONIBLE_FALTAN_INPUTS_DEL_ESCENARIO`, `FACTIBILIDAD_PENDIENTE`, `DESCONOCIDO` | falta un dato: mostrar qué falta y el DPV/DEC |
| **No comparable** | `OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA` (rechazado), override total frente a corridas verificadas, `COMPARABILIDAD = FALSE`, `NO_EVALUABLE`, `PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE`, `TRANSICION_DE_ARQUITECTURA_NO_MODELADA` | no entra a rankings, dominancia ni Pareto |
| **No calculado** | `NO_CALCULADA` (TIR en modo rápido), `NO_CALCULADO` (potencial de cambiar la decisión), `NO_CALCULABLE`, `NO_SOPORTADA_POR_INTERFAZ`, `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES`, `TIR_NO_DEFINIDA_MATEMATICAMENTE` | el motor no lo calculó (por diseño o por falta de método); no es 0 |
| No aplica | `NO_APLICA`, `NO_APLICA_STATUS_QUO`, `NO_REQUERIDO_POR_ARQUITECTURA` | el concepto no existe para esa alternativa (0 estructural) |
| Caso de prueba | `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO`, ámbito `ARTIFICIAL_TEST` | nunca mostrar como resultado del proyecto |

## 5. Reglas que la app debe hacer cumplir (además de las del motor)

1. **Overrides de arquitectura (TF-004, corregida en el motor):** la app envía los metadatos de cada CAPEX/OPEX del usuario y muestra el rechazo `OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA` tal cual; ofrece `OVERRIDE_TOTAL_ARQUITECTURA` solo como declaración explícita y rotula esas corridas con su etiqueta y la pérdida de trazabilidad.
2. **Canal de liquidación (`toma_todo`) (TF-006):** se muestra como "demanda supuesta ilimitada" con los kg que absorbe.
3. **NO_INVERTIR_AUN** se muestra como alternativa de decisión con su regla (SQ-1…SQ-6), nunca con VAN, TIR ni posición en un ranking (SUP-214).
4. **Probabilidades:** la app distingue probabilidad simulada, histórica (frecuencia sectorial) y del proyecto; esta última hoy es `PENDIENTE` (SUP-224).
5. **Unidades:** demanda en kg/día **calendario**; capacidad en aves/día **operativo**; CT en días calendario (365/12 por mes); la app no convierte entre bases sin mostrar la conversión.
6. **Moneda:** USD constantes de 2026-10-01 (modelo REAL); un valor en ARS exige TC, fecha y tipo de TC (SUP-187); la conversión no es una nueva cotización.

## 6. Qué NO puede hacer la app v1 (límites del motor)

- Evaluar transiciones de arquitectura (C0 → C1 → C3) ni combinaciones fuera del mapa (DEC-103, TF-074).
- Recalcular OPEX y capacidad con días operativos arbitrarios (TF-001) o parametrizar el plazo de recupero del IVA (TF-002).
- Publicar un resultado del proyecto en modo evidencia: hoy **0 de 61** corridas y **0 de 54** alternativas tienen indicadores publicables.
- Ejecutar Monte Carlo del proyecto (sin distribuciones respaldadas, DPV-180).
- Recomendar una inversión, una arquitectura, una escala o un proveedor.
