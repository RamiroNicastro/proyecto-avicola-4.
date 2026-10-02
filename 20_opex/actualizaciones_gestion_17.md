# Actualizaciones de gestión — sesión 17 (Motor OPEX + capital de trabajo)

**Fecha:** 2026-10-02 · **Rama:** `ccr-8751505c-jibesg` (desde `main` actualizado, commit `c5e0eb6`, posterior al merge de la sesión 16)
**Estado:** PROPUESTA para la próxima reconciliación. Esta sesión **no** modificó `00_gestion_proyecto/` ni `25_fuentes/` ni los modelos fuente aprobados. Todos los IDs son **provisionales** (`SUP-17-##`, `DPV-17-##`, `DEC-17-##`, `FTE-17-###`).

Últimos IDs oficiales al iniciar: **SUP-154, DPV-159, DEC-079, FTE-309**. Los IDs provisionales de la sesión 16 (`SUP-16-##`, `DPV-16-##`, `DEC-16-##`, `FTE-16-###`) tampoco están reconciliados: conviene reconciliar 16 y 17 juntas.

---

## 1. Supuestos propuestos (`supuestos.md`)

| ID provisional | Supuesto | Tipo | Dónde se usa | Relación |
|---|---|---|---|---|
| SUP-17-01 | **FECHA_BASE_OPEX = 2026-10-01** (editable). Moneda del modelo USD. Precios anteriores se marcan `PRECIO_ANTERIOR_A_FECHA_BASE` y **no** se indexan; campos `INDICE_ACTUALIZACION` / `FECHA_ACTUALIZACION` preparados | Criterio de modelo | `costear()` | SUP-16-01, DEC-006 |
| SUP-17-02 | **Anualización:** drivers diarios × días operativos (250/300); drivers semanales de producto y subproductos × semanas operativas (días ÷ días/semana); viajes y km de alimento × (t/año ÷ t de semana plena); huevos/año = huevos por pollito (14B) × pollitos/año (14B publica ritmo pleno × 52,14 = cota superior) | Criterio de modelo | `drivers_opex()` | SUP-025 |
| SUP-17-03 | **Configuraciones de referencia** = presets de CAPEX (SUP-16-09) + parámetros OPEX por defecto: 14A con turno extendido de 8 h netas, productividad media, limpieza y mantenimiento propios, automatización mapeada (semi → semiautomático), laboratorio y flota según CAPEX. No son decisión | [SUPUESTO] de escenario | `config_opex()`, `entradas_rrhh()` | SUP-152, DEC-067, DEC-068, DEC-069 |
| SUP-17-04 | **Aportes en granja integrada** según el esquema descripto en 03 (`modelos_integracion.md`): empresa = pollito, alimento, sanidad, asistencia técnica, logística de insumos; integrado = mano de obra, electricidad, agua (informativos); gas, cama, captura, mortalidad, limpieza y bioseguridad = **PENDIENTE** (según contrato). Editable; no es un contrato | [SUPUESTO] de escenario | `APORTES_03`, `Registro.split()` | DEC-020, DEC-17-04 |
| SUP-17-05 | **Composición del alimento** = puntos ilustrativos de 14B (60 % maíz, 30 % harina de soja, 10 % resto); aceite, núcleo y otros quedan incluidos en "resto" hasta tener fórmula. No es una dieta | [SUPUESTO] heredado | `drivers_opex()` | SUP-032, DEC-076 |
| SUP-17-06 | **Mantenimiento:** cuatro métodos alternativos (% CAPEX, por activo, horas técnicas, contrato), uno por corrida; el % CAPEX es solo benchmark (todo valor = SUPUESTO/[PVDP]); sin método = PENDIENTE | Criterio de modelo | §MANTENIMIENTO | DEC-040, DEC-068, DEC-17-06 |
| SUP-17-07 | **Naturaleza del costo laboral** por driver de 14A: producción, activos y estrategia → semifijo; casi fijo → fijo; horas tercerizadas → variable | Criterio de modelo | `NATURALEZA_DRIVER_14A` | SUP-140 |
| SUP-17-08 | **% variable por definición**: driver de volumen → 100 % variable; driver por período → 0 % (semifijo: dentro del escalón de capacidad). Semivariables sin reparto (PENDIENTE) hasta que se declare un SUPUESTO | Criterio de modelo | base, `costear()` | — |
| SUP-17-09 | **Ramp-up:** variables × u, fijos y semifijos constantes, escalamiento lineal de drivers; etapas arranque y estabilización sin factor (PENDIENTE); ineficiencias del arranque no modeladas | Criterio de modelo | `aplicar_utilizacion()` | DEC-17-08 |
| SUP-17-10 | **Capacidades y distancias logísticas** = escenarios de CAPEX/12B (5.500 aves/camión; 12 t; 28 t; 10 t; radio 100 km; mercado 300 km; fábrica–granja 75 km; receptor 50 km) | [SUPUESTO] heredado | `drivers_opex()` | SUP-16-20, SUP-033, SUP-091, SUP-096 |
| SUP-17-11 | **Stock medio de producto terminado** = `inventario()` de 12B con 6 despachos/semana de refrigerado y 2 de congelado, sin stock de seguridad | [SUPUESTO] heredado | capital de trabajo | SUP-099, DEC-058 |
| SUP-17-12 | **Costeo laboral provisional por FTE (v1.1)**: costo empresa/FTE = salario × (1 + adicionales % + vacaciones %) × (12 + SAC) × (1 + cargas % + ART %) + beneficios × 12 + EPP + capacitación + otros. El **SAC es una regla laboral** (`reglas_laborales_opex.csv`, [PVDP], DPV-17-19), **no** un precio E4 (la v1.0 lo contaba como concepto con precio: corregido). Headcount PENDIENTE; horas extra no automáticas | Criterio de modelo | `costo_empresa_fte()` | SUP-125, SUP-126, DPV-146, DPV-148 |
| SUP-17-13 | **Tercerizar conserva la función**: las horas de 14A siguen visibles; si el servicio ya las cobra (choferes en flete tercerizado, personal del faenador en façon, captura, laboratorio externo, HyS externo) quedan `INCLUIDO` en ese concepto; si no, se costean con tarifa horaria | Criterio de modelo | `lineas_laborales()` | SUP-129, SUP-134 |
| SUP-17-14 | **Tipo de cambio de precios en ARS** = A3500 (oficial mayorista) del día del precio, como criterio provisional | Criterio de modelo | base | DEC-006 |
| SUP-17-15 | **Total preliminar y costos unitarios** solo con cobertura 100 % de los conceptos costeables (incluye aportantes resueltos) **y** `ARQUITECTURA_COSTEABLE = TRUE` (v1.1); si no, "NO DISPONIBLE" + montos rotulados `MONTOS_PARCIALES_E4_NO_COMPARABLES` | Criterio de modelo | `resumir()` | SUP-16-10, DEC-17-10 |
| SUP-17-16 | **Huevos en incubación (WIP)** valuados al costo del huevo como **cota inferior** | Criterio de modelo | capital de trabajo | DEC-17-07 |
| SUP-17-17 | **Completitud de arquitecturas (v1.1)**: cada módulo propio o contratado tiene una lista de **bloques operativos materiales** (`BLOQUES_REQUERIDOS`); un bloque sin cantidad o precio queda PENDIENTE, nunca 0 ni ausente; un bloque ausente es error de modelo. `ARQUITECTURA_OPERATIVAMENTE_COMPLETA` = todos los bloques con cantidades; `ARQUITECTURA_COSTEABLE` = además con precio y sin aportantes pendientes. Los módulos FUTUROS deben estar estructurados pero no bloquean la etapa inicial | Criterio de modelo | `completitud()` | DEC-17-01 |
| SUP-17-18 | **Universos que no se mezclan (v1.1)**: utilities por universo (09C = solo planta de faena; incubación, alimento, granjas, tratamiento, rendering y reproductoras con consumos propios PENDIENTES) y RRHH por universo (14A = industrial + estructura + coordinación primaria; granjas propias, incubación, planta de alimento, efluentes, tratamiento y choferes de otros flujos PENDIENTES; reproductoras y rendering FUTURO). `FTE_TOTAL_CONOCIDO` excluye terceros incluidos en tarifas | Criterio de modelo | `clasificar_filas()`, `fte_universos()` | SUP-140, D17-02 |
| SUP-17-19 | **Precio observado ≠ conversión (v1.1)**: el precio en ARS es la observación; el USD es `CONVERSION_MODELO` (TC A3500 de la fecha del precio) y no una nueva observación. Precio de pizarra Rosario ≠ costo puesto en planta (diferencial `ALI-MP-DIF-*` aparte; flete en `LOG-GRA-*`) | Criterio de modelo | base, `costear()` | SUP-17-14 |
| SUP-17-20 | **Granjas mixtas (v1.1)**: cada concepto de producción primaria se registra en dos filas (`AMBITO_GRANJA` PROPIA / INTEGRADA); la integrada sigue al aportante y el aporte del productor es informativo ("costo del productor") | Criterio de modelo | `Registro.split()` | SUP-17-04 |

## 2. Datos por validar propuestos (`datos_por_validar.md`)

| ID provisional | Dato | Para qué | Conceptos | Relación |
|---|---|---|---|---|
| DPV-17-01 | **Alimento comprado:** si el precio es puesto en granja o en fábrica, si incluye flete y descarga, precio por fase | Separar alimento, flete y descarga sin doble conteo | ALI-A-PT, ALI-A-DES, LOG-ALI-* | **ampliar DPV-050** |
| DPV-17-02 | **Granos y materias primas puestos en planta** por corredor (maíz y harina de soja: pizarra + flete; núcleo, aceite, aminoácidos); lectura primaria de la Cámara Arbitral | Planta propia y façon B1 | ALI-MP-*, LOG-GRA-* | DPV-157 |
| DPV-17-03 | **Pollito BB y huevo fértil:** precio, IVA, vacunas incluidas, lugar de entrega, flete; lectura primaria de CAPIA | Pollito e incubación | POL-COMPRA, INC-OP-HUEVO, LOG-POL/HUE | DPV-006, DPV-153 |
| DPV-17-04 | **Contrato de integración:** base de pago (ave / kg), ajustes por conversión y mortalidad, aportes de cada parte (gas, cama, captura, mortalidad, limpieza, bioseguridad), plazo de pago al integrado | Producción primaria y CxP | PP-* | DEC-020, FTE-050 |
| DPV-17-05 | **Tarifas de energía y agua del sitio:** electricidad industrial (cargo variable, potencia, fijo, nivel de tensión), gas natural / GLP / biomasa, agua de red o canon | Utilities | UT-* | **ampliar DPV-052, DPV-053**; DPV-095 |
| DPV-17-06 | **Congelado y almacenamiento en frío de terceros:** tarifa por t o t·mes, condiciones | Frío C y façon | UT-FRIO-TER, FAE-FACON-FRIO | DPV-085, DEC-064 |
| DPV-17-07 | **Faena a façon:** tarifa por ave y alcance (empaque, frío, subproductos, rendimiento garantizado, control de calidad) | C0 | FAE-FACON* | **ampliar DPV-006** |
| DPV-17-08 | **Químicos** de limpieza y sanitización (USD/ave o USD/m²), de potabilización y de tratamiento de efluentes | Faena, utilities, efluentes | FAE-QUIM, UT-AGUA-TRAT, EF-QUIM, INC-OP-LIM, PP-LIMP | DEC-043 |
| DPV-17-09 | **Packaging por kg de producto** según mix y formato (bolsa, bandeja, film, caja, etiqueta, pallet, fleje) | Empaque | EMP-* | DEC-005 |
| DPV-17-10 | **Mantenimiento:** plan y costo anual por área (por activo o contrato), repuestos críticos, refrigerante; pedirlo con los RFQ de equipos | Mantenimiento | MAN-* | DEC-040, DPV-089 |
| DPV-17-11 | **Primas de seguros** por póliza (planta, incendio, RC, mercadería, interrupción, flota, granjas) | Seguros | SEG-* | — |
| DPV-17-12 | **Plan de autocontrol y precio por análisis** (microbiología, agua, alimento, vuelco) | Calidad | CAL-ANA-*, ALI-C-ANA, EF-ANA | DPV-041, DEC-065 |
| DPV-17-13 | **Certificaciones y auditorías** (BPM/HACCP/ISO, clientes) y su costo anual | Calidad | CAL-CERT, CAL-AUD | DPV-101 (tasas SENASA) |
| DPV-17-14 | **Parámetros de capital de trabajo:** días de cobro por canal, días de pago por proveedor, días de stock de envases, repuestos e insumos | Capital de trabajo | CT | DPV-039, DEC-079 |
| DPV-17-15 | **Dotaciones no dimensionadas por 14A:** granjas propias, incubadora, planta de alimento, operación de efluentes, tratamiento de subproductos, choferes de pollitos / alimento / grano / subproductos con flota propia | Costo laboral | COSTO_LABORAL (PENDIENTE_CANTIDAD) | DPV-153, DPV-158 |
| DPV-17-16 | **Consumos no dimensionados:** energía y gas de granja, cama (kg/m²), energía y agua de incubadora, kWh/t y vapor de planta de alimento, consumo L/km por tipo de camión, horas de equipo de frío vehicular, lodos | Cantidades hoy PENDIENTE_CANTIDAD | PP-ENE/GAS/CAMA, INC-OP-ENE/AGUA, ALI-C-*, LOG-COMB, LOG-*-FRIO, EF-LODO | **ampliar DPV-052, DPV-158, DPV-072, DPV-084** |
| DPV-17-17 | **Lectura primaria del Índice de costo de producción de pollos parrilleros (SAGyP)** (FTE-16-002): estructura y valores de costos de crianza | Benchmark oficial OPEX (E3) para alimento, pollito, sanidad, energía y mano de obra de granja | PP-*, ALI-*, POL-* | DPV-16-07 |
| DPV-17-18 | **Lectura primaria del A3500 (BCRA)** para las fechas de los precios usados | Validar los TC | base | DEC-006 |
| DPV-17-19 | **Normativa laboral en original**: SAC (Ley 20.744 arts. 121–122), vacaciones y plus vacacional (arts. 150–155), recargo de horas extra (art. 201), contribuciones patronales y alícuotas de ART vigentes; convenio colectivo aplicable por categoría | Reglas y componentes del costo empresa por FTE | `reglas_laborales_opex.csv`, LAB-<CAT>-* | **ampliar DPV-146, DPV-148** |

## 3. Decisiones pendientes propuestas (`decisiones_pendientes.md`)

| ID provisional | Decisión | Tipo | Prioridad | Depende de | Relación |
|---|---|---|---|---|---|
| DEC-17-01 | **[DECISIÓN METODOLÓGICA — no es decisión de inversión]** Adoptar la estructura del motor OPEX: registro por concepto, niveles E1–E5, clasificación (naturaleza, centro, tipo, aportante), regla de total y costos unitarios, separación OPEX / CAPEX / capital de trabajo, procedencia de drivers | METODOLÓGICA | Media | — | DEC-16-01 |
| DEC-17-02 | **Variante del façon de alimento:** materias primas de la empresa (B1) o del elaborador (B2); define precio, propiedad del inventario y capital de trabajo | Negocio (sub-decisión de DEC-024) | Media | DPV-155, DPV-17-02 | DEC-024, DEC-079 |
| DEC-17-03 | **Fuente de agua de la planta:** red / pozo / mixta | Negocio / sitio | Media | DEC-003, DPV-053 | DEC-043 |
| DEC-17-04 | **Base de pago y reparto de aportes con los integrados** (por ave / por kg; quién aporta gas, cama, captura, mortalidad, limpieza, bioseguridad) | Negocio (sub-decisión de DEC-020) | Alta (antes de costear C0–C2) | DPV-17-04 | DEC-020 |
| DEC-17-05 | **Modelo de tarifa del flete tercerizado** por flujo (viaje / km / unidad / contrato) | Negocio | Media | DPV-042, DPV-054 | DEC-056 |
| DEC-17-06 | **Método de estimación del mantenimiento** (por activo / contrato / horas / % CAPEX como benchmark) | METODOLÓGICA | Media | DPV-17-10 | DEC-040, DEC-068 |
| DEC-17-07 | **Método de valuación de inventarios** para el capital de trabajo: activo biológico (costo acumulado medio), producto terminado (costo de producción por kg), alimento propio (MP + conversión) | METODOLÓGICA | Media | DEC-17-01 | — |
| DEC-17-08 | **Curva de ramp-up** y parámetros de ineficiencia del arranque (para el modelo financiero) | METODOLÓGICA / negocio | Media | DPV-088 | DEC-033 |
| DEC-17-09 | **Política de cobro, pago y caja operativa** (días por canal y proveedor; buffer opcional) | Negocio | Media | DPV-039, DPV-17-14 | DEC-079 |
| DEC-17-10 | **Umbral de cobertura** para publicar un OPEX preliminar y costos unitarios (el motor propone 100 %) | METODOLÓGICA | Media | DEC-17-01 | DEC-16-05 |

Las decisiones **METODOLÓGICAS** (DEC-17-01, 06, 07, 10) definen cómo se calcula y publica el OPEX; no deben mezclarse con decisiones de negocio o inversión. El combustible térmico **no** genera una DEC nueva: es **DEC-045** (fuente térmica).

Decisiones existentes que el motor deja **parametrizadas, no tomadas**: DEC-001, DEC-002, DEC-003, DEC-004, DEC-006, DEC-016, DEC-020, DEC-023, DEC-024, DEC-027, DEC-043, DEC-045, DEC-053, DEC-056, DEC-064, DEC-065, DEC-067, DEC-068, DEC-072, DEC-073, DEC-074, DEC-079.

## 4. Fuentes provisionales (`registro_fuentes.csv`)

8 fuentes en [`fuentes_17.csv`](fuentes_17.csv) (FTE-17-001…008), **todas `[PVDP]`** (extractos de buscador; sitios primarios bloqueados por la red de la sesión). FTE-17-007 queda registrada como **descartada** por contradicción (regla 16).

## 5. Glosario (`glosario.md`) — términos a agregar si no existen

OPEX; costo variable / fijo / semifijo / semivariable; centro de costo; capital de trabajo operativo (CTO); cuentas por cobrar / por pagar; activo biológico; ramp-up; cobertura por conceptos vs por valor; aportante (empresa / integrado); tarifa de façon. Verificar duplicados antes de agregar ("capital de trabajo" y "façon" pueden existir).

## 6. Estado del proyecto (`estado_proyecto.md`) — al reconciliar

| Módulo | Estado propuesto |
|---|---|
| OPEX (`20`) | **MOTOR OPEX + CAPITAL DE TRABAJO CONSTRUIDO** v1.1 (78 tests, 14/14 mutaciones; auditado en completitud de arquitecturas y costo laboral). **Sin OPEX total ni capital de trabajo y ninguna arquitectura costeable**: 2 de 359 conceptos con precio (ambos E4); cobertura estructural 100 %, física 43–73 %, de costeo por bloques 0–10 % |

Hito sugerido: "2026-10-02 — Motor OPEX + capital de trabajo (sesión 17)".

## 7. Dependencias y tensiones abiertas

| ID | Dependencia / tensión | Estado |
|---|---|---|
| D17-01 | 20 → 21: el registro, el reparto fijo/variable y el capital de trabajo alimentan el modelo financiero; ingresos, IVA, depreciación e impuestos se calculan allí | Abierta |
| D17-02 | 18 (14A) → 20: 14A no dimensiona personal upstream (granjas, incubadora, planta de alimento), operación de efluentes ni choferes de algunos flujos; OPEX los deja PENDIENTE_CANTIDAD | Abierta (DPV-17-15) |
| D17-03 | 19 → 20: el mantenimiento por % CAPEX o por activo depende del BOQ y de los precios de CAPEX | Abierta |
| T17-01 | Contradicción de precios de pollito BB en extractos de CAPIA (ARS 1.312 vs "$ 16") | Registrada; prevalece la lectura del original cuando se obtenga |
| T17-02 | Maíz: precio sobre puerto vs puesto en planta (paridad por zona) | Abierta (DPV-17-02) |
| T17-03 | La energía de frío del OPEX hereda la contradicción ×5,7 de 09C (benchmark top-down vs carga física) | Abierta (DPV-109) |
| T17-04 | El costeo por FTE subestima si el costo empresa no incluye la cobertura de francos y licencias | Abierta (headcount PENDIENTE) |

## 8. Archivos de esta sesión

`20_opex/`: `modelo_opex.py`, `base_costos_opex.csv` y `reglas_laborales_opex.csv` (inputs), `completitud_arquitecturas_opex.csv`, `registro_costos_operativos.csv`, `escenarios_opex.csv`, `mapa_drivers_opex.csv`, `modelo_costo_laboral.csv`, `capital_trabajo_opex.csv`, `matriz_validacion_opex.csv`, `fuentes_17.csv`, 17 documentos `.md` y `README.md`. Ningún archivo fuera de `20_opex/` fue modificado.

## 9. Auditoría de cierre v1.1 — completitud de arquitecturas y costo laboral

| Hallazgo v1.0 | Corrección v1.1 | Test |
|---|---|---|
| Façon de alimento sin variante (C0, C2): el bloque de materias primas no existía (solo el servicio) | Fila explícita de alimento/MP con cantidad y sin precio aplicable | X15 |
| Incubación propia sin calidad/bioseguridad; energía sin mención de HVAC | INC-OP-CAL; INC-OP-ENE incluye HVAC; universo de utilities INCUBACION | X02 |
| Planta de alimento sin agua, movimientos internos ni diferencial a puesto en planta | ALI-C-AGUA, ALI-C-MOV, ALI-MP-DIF-MAIZ/SOJA | X03, X10 |
| Granjas propias sin análisis/veterinaria; mixtas en una sola fila | PP-VET; filas PROPIA / INTEGRADA separadas | X01 |
| Tratamiento básico de subproductos sin energía | SUB-TRAT-ENE | — |
| Rendering (CF) solo con energía, insumos y mantenimiento | + RRHH, térmico, agua, tratamiento, residuos, logística (FUTURO) | X14 |
| Reproductoras (CF) sin RRHH, agua, mantenimiento, residuos ni logística | REP-AGUA/MAN/RES/LOG + RRHH FUTURO | X14 |
| FTE de 14A presentado como dotación (C3 "igual a C1") | `fte_industrial_14a`; universos de RRHH; FTE_TOTAL_CONOCIDO, FTE_TERCEROS_INCLUIDOS_EN_TARIFAS, FTE_ADICIONAL_PENDIENTE | X05 |
| Utilities sin universo (riesgo de extender 09C a la empresa integrada) | `UNIVERSO_UTILITIES`; drivers de 09C solo en FAENA_PROPIA | X04 (mutación M12) |
| "13 meses remunerados" contado como precio E4 | Retirado de la base; SAC = regla laboral; componentes VAC, HEX, OTR agregados | X07, X08 |
| USD del pollito y del maíz sin distinguir de la observación en ARS | Columnas de precio observado, condición, IVA, TC, fecha y `ORIGEN_PRECIO_USD` | X09 |
| Totales bloqueados solo por conceptos faltantes | Además por `ARQUITECTURA_COSTEABLE`; montos `MONTOS_PARCIALES_E4_NO_COMPARABLES` | X06, X13 (mutación M17) |
| Horas del faenador "INCLUIDO" genérico | Recurso físico de tercero, `INCLUIDO_EN_TARIFA_FACON` | X11 |

Tests adaptados con justificación: C05 (la clave incluye el ámbito propia/integrada, porque las granjas mixtas generan dos filas a propósito), E04 (verifica la aritmética del total forzando una arquitectura costeable; el bloqueo real lo prueba X06) y L02 (nueva fórmula con vacaciones, SAC como regla y otros).

