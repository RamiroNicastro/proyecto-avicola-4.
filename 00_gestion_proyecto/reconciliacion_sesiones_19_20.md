# Reconciliación de las sesiones 19 y 20 — modelo financiero, riesgo y optimizador

**Fecha:** 2026-10-05 · **Tipo:** parte administrativa de la sesión 21 (auditoría + reconciliación final integral del motor) · **Rama:** `ccr-d71882bf-2idq1i` (desde `main` actualizado, commit `7779a8f`, posterior al merge de las sesiones 19 y 20)

> **Qué hace este documento:** integra en los registros maestros (`supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `matriz_validacion_campo.csv`, `glosario.md`, `estado_proyecto.md`, `25_fuentes/`) las propuestas con IDs provisionales de **19 Modelo financiero integral** (`21_modelo_financiero/`) y **20 Riesgos + sensibilidades + optimizador** (`22_riesgos/`), y deja el mapa ID provisional → ID central. La auditoría A–Z del motor está en [`auditoria_final_motor_v1.md`](auditoria_final_motor_v1.md).
> **No** se completaron precios, demanda, CAPEX, OPEX ni financiamiento; **no** se cerró ninguna decisión; **no** se elevó ninguna evidencia E4/`[PVDP]`; USD 2 M **no** se trata como capital confirmado. Los IDs provisionales solo permanecen en este documento y en los dos archivos históricos (`actualizaciones_gestion_19.md`, `actualizaciones_gestion_20.md`, marcados **ARCHIVO HISTÓRICO**). Test de integración ID01: ningún ID provisional activo en modelos, CSV, interfaces, README ni documentación vigente.

---

## 1. Resumen

| Sesión | Alcance | Carpeta | IDs provisionales | Resultado |
|---|---|---|---|---|
| **19** | Modelo financiero integral v1.1 | `21_modelo_financiero` | SUP-19-01…29, DPV-19-01…11, DEC-19-01…08, T19-01…04 (sin FTE) | 23 SUP nuevos (SUP-189 a SUP-211) + 2 consolidados (SUP-060, SUP-181) + 4 fusiones de a pares · 1 DPV nuevo (DPV-178) + 10 consolidados · 4 DEC nuevas (DEC-093 a DEC-096) + 4 consolidadas (DEC-006, 007, 034, 084) |
| **20** | Riesgo, sensibilidades y optimizador v1.1 | `22_riesgos` | SUP-20-01…24, DPV-20-01…10, DEC-20-01…08, T20-01…04 (sin FTE) | 24 SUP nuevos (SUP-212 a SUP-235) · 2 DPV nuevos (DPV-179, DPV-180; el segundo fusiona dos propuestas) + 5 consolidados + 2 reclasificados (TF-001, DEC-103) · 8 DEC nuevas (DEC-097 a DEC-104) |

Últimos IDs oficiales al iniciar: **SUP-188, DPV-177, DEC-092, FTE-322** (coinciden con los declarados por ambas sesiones). Al cerrar: **SUP-235, DPV-180, DEC-104, FTE-322**.

**Totales:** 53 propuestas SUP → 47 IDs nuevos + 2 consolidaciones (8 propuestas fusionadas de a pares en SUP-192, 200, 208, 210) · 21 propuestas DPV → 3 nuevos + 15 consolidaciones (en 13 DPV) + 2 reclasificaciones (+ 1 fusión) · 16 propuestas DEC → 12 nuevas + 4 consolidaciones · 0 FTE (FTE-004 y FTE-032 se anotan como usadas en `21_modelo_financiero`). Las tensiones T19-01…04 y T20-01…04 se indexan en [`tensiones_finales.csv`](tensiones_finales.csv) (T20-03 = TF-003).

## 2. IDs consolidados (mapa provisional → definitivo)

Todos los IDs provisionales se reemplazaron en `21_modelo_financiero/` y `22_riesgos/` (documentos, comentarios y textos de `modelo_financiero.py`, `motor_riesgo.py`, `modelo_optimizador.py`, inputs y CSV de salida). En los archivos activos, la propuesta reclasificada de recupero de IVA se cita como **TF-002** (limitación de interfaz) y el dato real queda en DPV-169. Las salidas de 21 y 22 regeneradas después del reemplazo son **idénticas byte a byte** al reemplazo textual (verificación del §8).

#### Supuestos

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| SUP-19-01 | **SUP-189** | Alta nueva | Jerarquía de inputs: EVIDENCIA_REAL > ESCENARIO_USUARIO > SUPUESTO_MODELO > PENDIENTE; el escen… |
| SUP-19-02 | **SUP-190** | Alta nueva | UMBRAL_EVIDENCIA_PUBLICACION configurable (fila umbral_evidencia_publicacion de inputs_financie… |
| SUP-19-03 | **SUP-191** | Alta nueva | Supuestos metodológicos admitidos en modo evidencia: modelo real, base de la tasa, meses de det… |
| SUP-19-04 | **SUP-192** | Fusionado con SUP-19-25 en SUP-192 | Tiempo: motor mensual (k = 0 es T0); descuento a fin de período con tasa anual efectiva y t = k… |
| SUP-19-05 | **SUP-193** | Alta nueva | Categorías de demanda: DOCUMENTADA y ASEGURADA = A; NEGOCIADA = B (× α, DEC-014); INTERESADA en… |
| SUP-19-06 | **SUP-194** | Alta nueva | Reporte: mensual los primeros 24 meses, anual después (editable; múltiplo de 12) |
| SUP-19-07 | **SUP-195** | Alta nueva | Modelo REAL en USD constantes de 2026-10-01, sin inflación; tasa en la misma base que los flujo… |
| SUP-19-08 | **SUP-060** | Consolidado en SUP-060 (existente) | Utilización: técnica (curva) · comercial (parte limitante, criterio de 23; puede > 1) · efectiv… |
| SUP-19-09 | **SUP-196** | Alta nueva | Curvas de ramp-up CONSERVADOR / BASE / RÁPIDO: ilustrativas, sin fuente, solo utilización técni… |
| SUP-19-10 | **SUP-181** | Consolidado en SUP-181 (existente) | OPEX por período: rubros de 20_opex a escala plena de la etapa activa; variable × u ÷ eficienci… |
| SUP-19-11 | **SUP-197** | Alta nueva | Capital de trabajo por días sobre DIAS_MES = 365 ÷ 12: inventario = días × costo de la base; Cx… |
| SUP-19-12 | **SUP-198** | Alta nueva | Valor terminal por defecto = SIN_VALOR_TERMINAL; sin recupero de CT; la deuda remanente al cier… |
| SUP-19-13 | **SUP-199** | Alta nueva | Ganancias anual al cierre de cada año del proyecto, sin anticipos; quebrantos con vencimiento; … |
| SUP-19-14 | **SUP-200** | Fusionado con SUP-19-26 en SUP-200 | Deuda: interés = saldo × tasa del período de servicio según tipo_tasa declarado (ver (prov.)); … |
| SUP-19-15 | **SUP-201** | Alta nueva | IVA simplificado: débito sobre venta interna neta de descuentos, bonificaciones y devoluciones;… |
| SUP-19-16 | **SUP-202** | Alta nueva | Inventario de producto: FIFO; por defecto sin arrastre (inventario_max_meses = 0): el excedente… |
| SUP-19-17 | **SUP-203** | Alta nueva | Asignación de ventas: por prioridad de la línea; prorrata dentro de la misma prioridad; toma_to… |
| SUP-19-18 | **SUP-204** | Alta nueva | Depreciación lineal contable desde la entrada en operación; terreno no depreciable; reposición … |
| SUP-19-19 | **SUP-205** | Alta nueva | Fondos iniciales: CT inicial = máximo CT hasta el fin del ramp-up inicial; otros = máximo saldo… |
| SUP-19-20 | **SUP-206** | Alta nueva | Break-even sobre el último año del horizonte con el mismo mix y precios; IIBB y tasas proporcio… |
| SUP-19-21 | **SUP-207** | Alta nueva | Subproductos por arquitectura: C0 (façon) = kg PENDIENTES según contrato (FAE-FACON-SUB); CF = … |
| SUP-19-22 | **SUP-208** | Fusionado con SUP-19-29 en SUP-208 | Trayectorias solo para configuraciones base (expansion() de CAPEX parte de preset()); las varia… |
| SUP-19-23 | **SUP-209** | Alta nueva | Stress: devaluación = valor USD × (1 + traslado × d) ÷ (1 + d) solo en ítems ARS con traslado d… |
| SUP-19-24 | **SUP-210** | Fusionado con SUP-19-28 en SUP-210 | Costos comerciales: logística del canal (adicional al OPEX de 20) y costos de exportación = OPE… |
| SUP-19-25 | **SUP-192** | Fusionado con SUP-19-04 en SUP-192 | Tasas y descuento: TASA_DESCUENTO anual efectiva (o nominal anual cap. mensual declarada y conv… |
| SUP-19-26 | **SUP-200** | Fusionado con SUP-19-14 en SUP-200 | Tasa de deuda con tipo obligatorio: EFECTIVA_ANUAL → (1 + TEA)^(f/12) − 1; NOMINAL_ANUAL → TNA … |
| SUP-19-27 | **SUP-211** | Alta nueva | Capa OVERRIDE_SIMULACION (solo escenario): permite evaluar un valor distinto del observado (pre… |
| SUP-19-28 | **SUP-210** | Fusionado con SUP-19-24 en SUP-210 | Derechos de exportación: ubicación única = deducción de la venta de exportación (canales.export… |
| SUP-19-29 | **SUP-208** | Fusionado con SUP-19-22 en SUP-208 | Corridas con ID_CORRIDA único MODO\|CONFIGURACION\|VARIANTE\|ESCALAS\|TRAYECTORIA\|ESCENARIO; s… |
| SUP-20-01 | **SUP-212** | Alta nueva | Shocks one-way relativos (−30 % … +30 %), en días (−30 … +30) y en meses (−24 … +24): grillas d… |
| SUP-20-02 | **SUP-213** | Alta nueva | Evaluación rápida por interfaz explícita resultados(R, calcular_tir=False): TIR y TIR del accio… |
| SUP-20-03 | **SUP-214** | Alta nueva | NO_INVERTIR_AUN = alternativa de decisión (status quo), no proyecto productivo: sin métricas fi… |
| SUP-20-04 | **SUP-215** | Alta nueva | Peso vivo (aproximación): kg comerciales por ave y costo de alimento proporcionales al peso viv… |
| SUP-20-05 | **SUP-216** | Alta nueva | FCR (aproximación): costo de alimento proporcional al FCR a precio y peso constantes |
| SUP-20-06 | **SUP-217** | Alta nueva | Rendimiento de faena (aproximación): más rendimiento comestible = más kg de productos comestibl… |
| SUP-20-07 | **SUP-218** | Alta nueva | Parámetros técnicos: grilla de quiebre 24 puntos + bisección (tol 1e-7); Monte Carlo 1.000 simu… |
| SUP-20-08 | **SUP-219** | Alta nueva | Preset de pesos IGUALES para el objetivo balanceado (solo si el usuario lo elige; rotulado SUPU… |
| SUP-20-09 | **SUP-220** | Alta nueva | Restricción HARD no evaluable excluye del ranking (FACTIBILIDAD_PENDIENTE ≠ FACTIBLE); exigir g… |
| SUP-20-10 | **SUP-221** | Alta nueva | CAPITAL_DISPONIBLE se compara contra el PICO_FONDOS por defecto (incluye pérdidas del ramp-up y… |
| SUP-20-11 | **SUP-222** | Alta nueva | Componentes faltantes en scores (riesgo, balanceado): SEPARAR por defecto (score PENDIENTE); PE… |
| SUP-20-12 | **SUP-223** | Alta nueva | Magnitudes de stress ilustrativas tomadas de STRESS_PREDEFINIDOS de 21 (demanda −30 %, alimento… |
| SUP-20-13 | **SUP-224** | Alta nueva | Frecuencia sectorial ≠ probabilidad del proyecto: PROBABILIDAD exige método específico del proy… |
| SUP-20-14 | **SUP-225** | Alta nueva | Matriz cualitativa 3×3 con clases BAJO / MODERADO / ALTO / CRÍTICO; sin producto numérico P × I |
| SUP-20-15 | **SUP-226** | Alta nueva | Robustez = comportamiento en escenarios deterministas (stress activos + extremos one-way de rob… |
| SUP-20-16 | **SUP-227** | Alta nueva | 0 estructural ≠ desconocido: un requerimiento físico es 0 solo si la arquitectura no tiene el a… |
| SUP-20-17 | **SUP-228** | Alta nueva | COBERTURA_EVIDENCIA = bloques del motor completos en modo EVIDENCIA ÷ 17 para la misma configur… |
| SUP-20-18 | **SUP-229** | Alta nueva | VELOCIDAD, CONTROLABILIDAD, DETECTABILIDAD del registro de riesgos: estimaciones cualitativas r… |
| SUP-20-19 | **SUP-230** | Alta nueva | Clasificación de rubros por driver por prefijo de COSTO_ID de 20 (ALI-, POL-, UT-ELE-, LAB-, EM… |
| SUP-20-20 | **SUP-231** | Alta nueva | SCORE_ORDINAL_RIESGO: el score de orden del optimizador se llama así y NO ES PROBABILIDAD; BAJA… |
| SUP-20-21 | **SUP-232** | Alta nueva | Correlación pendiente ≠ 0: un par relacionado con correlación PENDIENTE impide el Monte Carlo s… |
| SUP-20-22 | **SUP-233** | Alta nueva | RANK_COMPARTIDO: los empates de prioridad no se desempatan por orden, ID ni nombre |
| SUP-20-23 | **SUP-234** | Alta nueva | Pareto y dominancia solo entre comparables: COMPARABILIDAD FALSE → NO_EVALUABLE; menos de 2 pun… |
| SUP-20-24 | **SUP-235** | Alta nueva | AMBITO en toda salida: PROYECTO (evidencia o escenario) vs ARTIFICIAL_TEST (casos de prueba; lo… |

#### Datos por validar

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| DPV-19-01 | **DPV-167** | Consolidado en DPV-167 (existente) | Curva de desembolso del CAPEX: hitos de pago y anticipos por paquete (línea, frío, obra, efluen… |
| DPV-19-02 | **DPV-040** | Consolidado en DPV-040 (existente) | Condiciones comerciales de todos los canales (mayoristas, carnicerías/pollerías, gastronomía, i… |
| DPV-19-03 | **DPV-086** | Consolidado en DPV-086 (existente) | Duración de preoperación, construcción y commissioning (permisos, habilitación SENASA, obra, mo… |
| DPV-19-04 | **DPV-001** | Consolidado en DPV-001 (existente) | Costo de capital del grupo inversor (rendimiento exigido, horizonte) |
| DPV-19-05 | **DPV-178** | Alta nueva | Financiamiento disponible: bancos, programas públicos, leasing, financiación de proveedores: mo… |
| DPV-19-06 | **DPV-169** | Consolidado en DPV-169 (existente) | Reglas fiscales completas: alícuota de ganancias, quebrantos, IIBB por jurisdicción, tasas muni… |
| DPV-19-07 | **DPV-088** | Consolidado en DPV-088 (existente) | Ineficiencias del arranque en plantas avícolas argentinas: merma, conversión, rendimiento de lí… |
| DPV-19-08 | **DPV-167** | Consolidado en DPV-167 (existente) | Vida útil contable y fiscal por clase de activo |
| DPV-19-09 | **DPV-175** | Consolidado en DPV-175 (existente) | Días de inventario de producto terminado, packaging, repuestos e insumos y su método de valuaci… |
| DPV-19-10 | **DPV-078** | Consolidado en DPV-078 (existente) | Vida comercial del producto refrigerado y congelado (cuánto puede guardarse un excedente) y cap… |
| DPV-19-11 | **DPV-072** | Consolidado en DPV-072 (existente) | Signo del ingreso por subproductos crudos: precio de venta vs costo de retiro por material y re… |
| DPV-20-01 | **TF-001** | Reclasificado: limitación de interfaz del motor, no dato de campo → tensión TF-001 | Interfaz de días operativos: recalcular OPEX y capacidad con días distintos de 250/300 sin romp… |
| DPV-20-02 | **DPV-169** | Consolidado en DPV-169 (dato: regla y plazo reales); la parametrización del motor es la tensión TF-002 | Plazo de recupero del IVA (saldo técnico, bienes de capital) parametrizable en el motor |
| DPV-20-03 | **DEC-103** | Reclasificado: ampliar el mapa es una decisión de alcance del modelo → DEC-103 | Ampliar el mapa de arquitecturas con combinaciones físicamente válidas relevantes (1.450 no map… |
| DPV-20-04 | **DPV-179** | Alta nueva | Moneda original por rubro de OPEX y precio (ARS / USD) transportada hasta la entrada del motor |
| DPV-20-05 | **DPV-180** | Fusionado con DPV-20-06 en DPV-180 | Distribuciones respaldadas: series históricas (precio de pollo y cortes, maíz, harina de soja, … |
| DPV-20-06 | **DPV-180** | Fusionado con DPV-20-05 en DPV-180 | Coeficientes de correlación con fuente (pollo/alimento, maíz/soja, FX/costos, demanda/precio, u… |
| DPV-20-07 | **DPV-087** | Consolidado en DPV-087 (existente) | Disponibilidades físicas confirmadas por sitio: terreno, potencia, agua, m² de galpón de integr… |
| DPV-20-08 | **DPV-044** | Consolidado en DPV-044 (existente) | Valores base de mortalidad, condenas, FCR y traslado de una devaluación a precios en ARS |
| DPV-20-09 | **DPV-160** | Consolidado en DPV-160 (existente) | CAPEX desglosado por clase de activo (equipos, obra, frío, efluentes, terreno, instalación, imp… |
| DPV-20-10 | **DPV-006** | Consolidado en DPV-006 (existente) | Capacidad de façon (faena y alimento) disponible y su estabilidad |

#### Decisiones

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| DEC-19-01 | **DEC-084** | Consolidado en DEC-084 (existente) | Umbral de publicación del modo evidencia (ampliación de DEC-084): ¿se acepta E4 en algún bloque… |
| DEC-19-02 | **DEC-007** | Consolidado en DEC-007 (existente) | Horizonte de evaluación (10 / 15 / 20 años) y tasa de descuento de referencia del proyecto y de… |
| DEC-19-03 | **DEC-093** | Alta nueva | Método de valor residual / terminal (sin valor, valor libro, explícito, perpetuidad) |
| DEC-19-04 | **DEC-006** | Consolidado en DEC-006 (existente) | Modelo real vs nominal y criterio de TC para reportar en ARS |
| DEC-19-05 | **DEC-034** | Consolidado en DEC-034 (existente) | Gatillos de expansión: por fecha o por condición (utilización, demanda asegurada, caja, DSCR, a… |
| DEC-19-06 | **DEC-094** | Alta nueva | Política de dividendos y caja mínima |
| DEC-19-07 | **DEC-095** | Alta nueva | Política de excedentes de producto (vender fresco, congelar, canal de liquidación) |
| DEC-19-08 | **DEC-096** | Alta nueva | Base de flujo para publicar indicadores (¿solo after-tax?), si el break-even oficial es EBITDA … |
| DEC-20-01 | **DEC-097** | Alta nueva | Objetivo(s) de optimización y pesos del objetivo balanceado |
| DEC-20-02 | **DEC-098** | Alta nueva | Restricciones duras y blandas (capital real comprometido, pico máximo, payback máximo, DSCR mín… |
| DEC-20-03 | **DEC-099** | Alta nueva | Pesos del score de riesgo y tratamiento de faltantes |
| DEC-20-04 | **DEC-100** | Alta nueva | Umbrales de alerta del registro de riesgos (UAD) |
| DEC-20-05 | **DEC-101** | Alta nueva | Tolerancia de equivalencia entre mejor y segunda alternativa |
| DEC-20-06 | **DEC-102** | Alta nueva | Criterio de robustez y magnitudes de stress |
| DEC-20-07 | **DEC-103** | Alta nueva | Extender la interfaz financiera a transiciones de arquitectura (C0 → C1 → …) y combinaciones fu… |
| DEC-20-08 | **DEC-104** | Alta nueva | Reglas opcionales de status quo y desempate de prioridades: stress que obligan a no invertir (S… |

## 3. Supuestos

Todos son **criterios de modelo** (cómo calcula o compara el motor), no datos económicos ni precios. 19 → SUP-189 a SUP-211 (motor financiero: jerarquía de inputs, umbral, tiempo y tasas, demanda, utilización, ramp-up, CT, valor terminal, ganancias, deuda, IVA, inventario, ventas, depreciación, fondos, break-even, subproductos, corridas, stress, deducciones, override). 20 → SUP-212 a SUP-235 (shocks, evaluación rápida, status quo, aproximaciones técnicas, parámetros, restricciones, scores, stress, frecuencia ≠ probabilidad, robustez, 0 estructural ≠ desconocido, cobertura de evidencia, clasificación de rubros, correlaciones, empates, Pareto, ámbito).

Solapamientos revisados (no se duplicó ningún concepto):

| Propuesta | Concepto existente | Tratamiento |
|---|---|---|
| Utilización técnica / comercial / efectiva (19) | SUP-060 (factor demanda/capacidad, utilización, cobertura) | Consolidada: la comercial = factor demanda/capacidad; la efectiva = utilización de planta |
| OPEX por período (19) | SUP-181 (ramp-up OPEX) | Consolidada como anotación |
| Tiempo (19-04) y tasas (19-25) | — | Fusión en SUP-192 (eran el mismo criterio antes y después de la auditoría de 19) |
| Deuda (19-14) y tipo de tasa (19-26) | — | Fusión en SUP-200 |
| Trayectorias (19-22) y corridas (19-29) | — | Fusión en SUP-208 |
| Costos comerciales (19-24) y derechos de exportación (19-28) | — | Fusión en SUP-210 |
| Modelo real (19-07) | SUP-155 (fecha base y moneda de CAPEX/OPEX) | Alta (SUP-195): agrega la regla real vs nominal y su verificación; referencia SUP-155 |
| 0 estructural ≠ desconocido (20-16) | SUP-185 (completitud de arquitecturas) | Alta (SUP-227): agrega la distinción NO_REQUERIDO / DESCONOCIDO en gates |

## 4. Datos por validar

Altas (con fila en [`matriz_validacion_campo.csv`](matriz_validacion_campo.csv)): **DPV-178** financiamiento disponible (N2), **DPV-179** moneda original por rubro y traslado de devaluación (N2), **DPV-180** distribuciones y correlaciones respaldadas (N4). Consolidaciones (anotadas en el DPV existente con la fecha 2026-10-05): DPV-001 (costo de capital), 006 (capacidad de façon), 040 (condiciones de todos los canales), 044 (valores base de mortalidad y FCR), 072 (signo del ingreso por subproductos), 078 (vida comercial del excedente), 086 (duración de preoperación, obra y commissioning), 087 (disponibilidades físicas por sitio), 088 (ineficiencias del arranque), 160 (CAPEX por clase de activo), 167 (curva de desembolso y vida útil contable/fiscal), 169 (reglas fiscales completas y recupero de IVA), 175 (días de inventario y valuación). Reclasificaciones: la interfaz de días operativos → **TF-001**; la ampliación del mapa de arquitecturas → **DEC-103**. Paquetes operativos de validación en [`plan_validacion_final.md`](plan_validacion_final.md). **Ningún DPV cambió a Validado.**

## 5. Decisiones

**[METODOLÓGICA]:** DEC-093 (valor terminal), DEC-096 (base de flujo, break-even oficial y convención de descuento para publicar), DEC-099 (pesos del score de riesgo), DEC-101 (tolerancia de equivalencia), DEC-102 (criterio de robustez y magnitudes de stress), DEC-103 (extender la interfaz a transiciones de arquitectura y combinaciones fuera del mapa). **[NEGOCIO]:** DEC-094 (dividendos y caja mínima), DEC-095 (excedentes de producto), DEC-097 (objetivos de optimización y pesos), DEC-098 (restricciones duras y blandas, incluido el capital real), DEC-100 (umbrales de alerta del registro de riesgos), DEC-104 (reglas opcionales de status quo y desempate de prioridades). Consolidaciones: umbral de publicación → DEC-084; horizonte y tasa (proyecto y accionista) → DEC-007; real vs nominal → DEC-006; gatillos de expansión → DEC-034. **Todas `Abierta`.**

## 6. Fuentes

Ninguna fuente nueva (no se asignó ningún FTE provisional). FTE-004 y FTE-032 agregan `21_modelo_financiero` a `carpetas_relacionadas` y una observación: se usan solo como `REFERENCIA_E4_NO_USABLE`. Nota en [`../25_fuentes/bibliografia.md`](../25_fuentes/bibliografia.md).

## 7. Tensiones

Ninguna se resolvió por decisión de negocio. Registro único en [`tensiones_finales.csv`](tensiones_finales.csv): TF-001 a TF-010 son nuevas de la auditoría (dos de ellas ya CORREGIDAS por ser errores inequívocos de documentación o reporte); TF-011 en adelante indexan las abiertas de las reconciliaciones 12, 14, 16–17 y de las sesiones 16, 17, 19 y 20 (con su ID original).

## 8. Verificación y archivos

| Verificación | Resultado |
|---|---|
| Reemplazo de IDs | 1.709 ocurrencias en 37 archivos activos + 4 líneas con marcadores genéricos reescritas a mano |
| Salidas de 21 regeneradas después del reemplazo | 13 CSV **idénticos byte a byte** al reemplazo textual |
| Salidas de 22 regeneradas después del reemplazo | **idénticas byte a byte** (antes de agregar la columna `POTENCIAL_DE_CAMBIAR_DECISION` de la auditoría) |
| Registros centrales | columnas por fila = encabezado en los tres registros; IDs únicos y correlativos (test ID02) |
| IDs provisionales activos | 0 (test ID01) |
| Mapa completo | cada propuesta de 19 y 20 tiene ID central existente (test ID05) |
