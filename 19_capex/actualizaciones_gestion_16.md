# Actualizaciones de gestión — sesión 16 (Motor CAPEX integral)

**Fecha:** 2026-10-02 · **Rama:** `claude/relaxed-pasteur-p3cg45` (desde `main` actualizado, commit `14d411a`, posterior a la reconciliación 14A–14B)
**Estado:** PROPUESTA para la próxima reconciliación. Esta sesión **no** modificó `00_gestion_proyecto/` ni `25_fuentes/`. Todos los IDs son **provisionales** (`SUP-16-##`, `DPV-16-##`, `DEC-16-##`, `FTE-16-###`, `T16-##`).

Últimos IDs oficiales al iniciar: **SUP-154, DPV-159, DEC-079, FTE-309**.

---

## 1. Supuestos propuestos (`supuestos.md`)

| ID provisional | Supuesto | Tipo | Dónde se usa | Relación |
|---|---|---|---|---|
| SUP-16-01 | **FECHA_BASE_CAPEX = 2026-10-01** (editable). Moneda de comparación **USD**. Precios con fecha anterior se marcan `PRECIO_ANTERIOR_A_FECHA_BASE`; **no** se escalan automáticamente (índice PENDIENTE: DPV-16-09) | Criterio de modelo | `modelo_capex.py` §1 | Regla 2 de CLAUDE.md |
| SUP-16-02 | **Reserva de flota:** +1 unidad por flujo con flota propia y base > 0 (barrido 0 / 1). No es estándar | [SUPUESTO] | `drivers()` | DEC-056, SUP-098 |
| SUP-16-03 | **Ciclo de vehículos** de alimento, pollitos y subproductos: 2 × distancia ÷ 70 km/h + 2 h de carga/descarga; 12 h útiles por camión-día (SUP-098); 6 días de entrega/semana (alimento, pollitos) | [SUPUESTO] sin fuente | `_vehiculos()` | SUP-094, SUP-098 |
| SUP-16-04 | **Arquitectura de frío → perfil de 09C:** A = P1 con congelado propio mínimo; B = P2 con congelado propio; C = P1 **sin** túnel ni congelado propio (congelado tercerizado) | Criterio de modelo | `FRIO_A_PERFIL` | SUP-055, DEC-064 |
| SUP-16-05 | **Nivel de automatización en escalas intermedias:** el de la escala de referencia más cercana (empate hacia arriba); opciones "M/S" según el input (manual → la primera, auto → la última, semi → S) | Criterio de modelo | `nivel_eq()` | SUP-065, DEC-037 |
| SUP-16-06 | **Paquetes sin doble conteo:** los componentes de un lote RFQ (EQ-xx, FR-*, EF-*) se consideran **incluidos** en el precio del paquete; se costean aparte solo si la cotización viene desglosada. Reasignaciones: EQ-03 → logística (cajones); EQ-14 → térmico; EQ-37 → frío (agua helada); EQ-54/EQ-76 → IT; EQ-70 → efluentes; EQ-71/72/73 → aire/agua/respaldo; EQ-74/75 → higiene | Criterio de modelo | `padre_de_eq()` | T16-01, T16-02 |
| SUP-16-07 | **Indirectos, preoperativos y contingencias** por porcentaje sobre bases declaradas (directo **sin terreno**; equipos; equipos sin puesta en marcha incluida; directo + indirecto sin conceptos que ya incluyen contingencia). **Porcentajes NO adoptados** (vacíos); todo valor que se cargue es SUPUESTO DE ESTIMACIÓN (E5) | Criterio de modelo | `_base_pct()` | DPV-16-08, DPV-16-09 |
| SUP-16-08 | **LOW / HIGH** = cantidad baja × precio bajo / cantidad alta × precio alto (envolvente con correlación perfecta, **no** intervalo de confianza); solo si el precio declara `ORIGEN_RANGO` | Criterio de modelo | `costear()` | SUP-107 (rangos de 12C) |
| SUP-16-09 | **Configuraciones de referencia C0–C3 y CF** con parámetros ilustrativos (C2: 25 % de granjas propias; flota propia en aves vivas, refrigerado y servicio; C3: granjas 100 % propias, flota propia en todos los flujos, subproductos con tratamiento básico propio). **No** son recomendación ni secuencia obligatoria | [SUPUESTO] de escenario | `preset()` | SUP-152, DEC-074 |
| SUP-16-10 | **Total preliminar** solo si el 100 % de los conceptos costeables tiene precio y cantidad y no hay alcance pendiente; si no, se publica "NO DISPONIBLE" + CAPEX con precio + cobertura | Criterio de modelo | `resumir()` | DEC-16-05 |
| SUP-16-11 | **Etiquetas de expansión** desde la modularidad de `08_maquinaria/matriz_equipos.csv` (Mantener → REUTILIZABLE; Ampliar → ESCALABLE; Duplicar/Agregar → DUPLICABLE; Reemplazar → REEMPLAZABLE) y por módulo para el resto; un cambio del nivel de automatización entre etapas = REEMPLAZA. Costo de ampliación = Δ × precio unitario de obra nueva; **prima/penalidad de ampliación PENDIENTE** | Criterio de modelo | `accion_expansion()` | DEC-035, DPV-16-14 |
| SUP-16-12 | **IVA:** `pendiente` → se incluye con alerta IVA_INCIERTO; `con_iva` sin alícuota → fuera del costo económico; no se resuelven IVA recuperable ni aranceles | Criterio de modelo | `costear()` | DPV-16-05, DPV-16-17 |
| SUP-16-13 | **Método escalado:** sin exponente explícito, el precio de referencia solo vale **dentro** del rango de capacidad de la referencia; con exponente es sensibilidad declarada | Criterio de modelo | `costear()` | DPV-16-01 |
| SUP-16-14 | **Subproductos:** A = lote L9 (sangre, plumas, vísceras, contenedores) + retiro externo; B = A + acondicionamiento básico propio (tecnología PENDIENTE); C rendering = solo futuro/sensibilidad | Criterio de modelo | `generar_boq()` | DEC-027, DEC-059 |
| SUP-16-15 | **Agua:** almacenamiento = agua captada × 0,5 / 1 / 2 días; tratamiento y bombeo con el caudal horario máximo ilustrativo de 09C. (v1.1: la ecualización ya **no** usa el volumen diario; queda PENDIENTE de tiempo de retención) | [SUPUESTO] | `generar_boq()` | SUP-070 (09C) |
| SUP-16-16 | **Terreno (v1.2):** la modalidad declara la **necesidad** de la arquitectura (`terreno_requerido_arquitectura`): `compra_fase`, `parque_industrial`, `rural_compatible` = mínimo físico (+ rendering si se declara); `compra_reserva` o `escala_objetivo` = superficie del escenario objetivo de 12C (crecer hasta X + rendering). Parque y rural cambian el **tipo de precio**. El terreno **a adquirir** es una decisión aparte (SUP-16-25) | Criterio de modelo | `entradas_superficie()` | DEC-063, SUP-119 |
| SUP-16-17 | **Alerta de planta de alimento subutilizada** < 50 % de utilización (alerta, no criterio de diseño) | Criterio de control | `drivers()` | SUP-148 |
| SUP-16-18 | Una báscula de camiones en la planta de alimento | [SUPUESTO] | BOQ ALI-BAS | — |
| SUP-16-19 | **Rango del motor:** 2.500–20.000 aves/día, intermedias permitidas, sin extrapolación | Criterio de modelo | `validar_config()` | SUP-052 |
| SUP-16-21 | **Capacidad nominal de línea** = ritmo nominal requerido de 05 con sensibilidad `media` (R = 0,89) y 8 h netas: **escenario etiquetado** (input `sensibilidad_rendimiento_linea`); diseño y garantizada PENDIENTES | Escenario | `drivers()` | SUP-061, DPV-097 |
| SUP-16-22 | **CADENCIA_NACIMIENTOS** = 2 cargas/semana y margen 15 %: **escenario etiquetado** de 14B (input `cadencia_nacimientos`, `margen_capacidad_incubacion`) | Escenario | `drivers()` | SUP-146, SUP-147, DEC-060, DEC-078 |
| SUP-16-23 | **Perfil de fabricación de alimento** = 5 d × 8 h, eficiencia 0,85, margen 15 %: **escenario etiquetado** de 14B (inputs `dias_op_planta_alimento`, `horas_dia_planta_alimento`, `eficiencia_planta_alimento`, `margen_planta_alimento`) | Escenario | `drivers()` | SUP-148 |
| SUP-16-24 | **TERRENO_MINIMO_FISICO_DERIVADO** = función de terreno de 12C con escala objetivo = escala y sin rendering (huella + exteriores + efluentes + retiros/buffers); 12C no lo publica (T16-07) |
| SUP-16-25 | **Terreno a adquirir = DECISIÓN** (`criterio_terreno`: mínimo físico / conceptual 12C / objetivo 12C / requerido por la arquitectura / valor de usuario). Sin criterio: dimensionamiento PROVISIONAL con el requerido por la arquitectura, costo no definitivo, bloque TERRENO nunca COMPLETO. Nunca un max() entre definiciones | Criterio de modelo | `drivers()` | SUP-121 |
| SUP-16-20 | **Capacidades de vehículos** = escenarios de 12B (5.500 aves/camión; 12 t refrigerado y congelado; 28 t granelero; 10 t subproductos; pollitos PENDIENTE). No son capacidades validadas | [SUPUESTO] heredado | `config_por_defecto()` | SUP-033, SUP-096, DPV-084 |

## 2. Datos por validar propuestos (`datos_por_validar.md`)

Agrupados por tema (no uno por tornillo). Ninguno se resolvió en esta sesión.

| ID provisional | Dato | Para qué | Bloques del BOQ | Relación |
|---|---|---|---|---|
| DPV-16-01 | **Precio de equipos de proceso** por lote RFQ (L1–L7, L11) y por escala, con Incoterm, alcance y **exponente de escala** observado entre dos escalas cotizadas | Sacar PROCESO de PENDIENTE | PQ-L1…L11, SB-L9 | DPV-097, DPV-095, DEC-049 |
| DPV-16-02 | **USD/m² de obra civil por categoría** (14 categorías de `obra_civil_capex.md`) en Argentina, con fecha, TC, IVA, alcance y región | Obra civil | OC-* | DEC-062, SUP-107 |
| DPV-16-03 | **Precio de terreno por tipo y corredor** (industrial, parque, rural compatible) + gastos de compra + cargos de parque + accesos | Terreno | TER-* | DEC-055, DEC-063, DPV-141 |
| DPV-16-04 | **Fletes y logística de importación:** flete marítimo, seguro, gastos portuarios, despachante, flete puerto → sitio (capas C04–C09) | Equipo importado → landed | capas | `08_maquinaria/plan_rfq.md` §5 |
| DPV-16-05 | **Importación:** clasificación arancelaria, derechos, tasas, régimen aplicable (bienes de capital nuevos y usados), despachante | Capa C07 (no se asume arancel cero) | capas | DPV-093 |
| DPV-16-06 | **Alcance de paquetes e instalación:** montaje electromecánico, supervisión, commissioning, puesta en marcha, capacitación, repuestos, garantía; qué incluye cada oferta (columnas `INSTALACION_INCLUIDA`, `PUESTA_EN_MARCHA_INCLUIDA`) | Equipo → instalado sin doble conteo | todos los paquetes; PRE-* | T16-01, T16-02 |
| DPV-16-07 | **Galpones:** precio por plaza o por m² en Argentina y alcance (equipamiento, silos, terreno); leer en original el índice SAGyP (FTE-16-002) y el documento INTA (FTE-16-007) | Reemplazar la cota de prensa E4 (FTE-081) | GRA-* | DEC-022, T16-03 |
| DPV-16-08 | **Indirectos:** referencias documentadas de ingeniería, dirección de obra, PM, permisos y estudios para plantas alimentarias en Argentina | Cargar IND-* con evidencia | IND-* | SUP-16-07 |
| DPV-16-09 | **Contingencia y escalación:** clase de estimación por bloque (madurez de ingeniería), criterio de contingencia, índice de escalación aplicable (USD o ARS) | CON-* | CON-* | DEC-16-04 |
| DPV-16-10 | **Cajones, módulos y contenedores:** aves por cajón, juegos por camión, titularidad con transporte tercerizado; volumen útil de contenedores de subproductos | Cantidades de JAU-*/CNT-* | JAU-VIVO, CNT-* | DPV-084, DPV-135, DEC-16-06 |
| DPV-16-11 | **Conexiones:** costo y plazo de acometida de MT, gas, agua y cloaca por sitio; demanda máxima (kVA) a solicitar | Terreno y utilities | TER-07, EL-ACO, EL-TRA | DPV-095, DPV-106 |
| DPV-16-12 | **Programa de áreas asset-light** (oficina, eventual cross-dock/CD) | Cantidad de OC-ADM | OC-ADM | DEC-053 |
| DPV-16-13 | **Programa de áreas de incubadora y planta de alimento** (m² y terreno) | Cantidad de INC-EDI, ALI-OBR, INC-TER, ALI-TER | INC-*, ALI-* | DPV-153, DPV-158 |
| DPV-16-14 | **Prima/penalidad de ampliación** por etapas (obra en operación, interferencias, demoliciones) y alcance real de la "previsión de ampliación" | Comparar trayectorias de expansión | `expansion_capex.csv` | DEC-035, DEC-033 |
| DPV-16-15 | **Vida útil y tiempo de entrega** por clase de activo y paquete | Campos `VIDA_UTIL_ANIOS`, `REEMPLAZO_ANIO` (para el modelo financiero) y cronograma | todos | DPV-086 |
| DPV-16-16 | **Vehículos:** precio de chasis, carrocería, equipo de frío y equipo auxiliar por flujo en Argentina | Logística propia | VEH-*, CAR-*, FRI-*, AUX-* | DEC-056 |
| DPV-16-17 | **Impuestos sobre la inversión:** IVA de bienes de capital, percepciones, recupero y efecto financiero (costo económico vs desembolso) | Modelo financiero | todos | SUP-16-12 |

Capacidades reales que quedan PENDIENTES en el BOQ (kWf total, kVA máximo, kWt pico, caudal de aire, posiciones de dock, puestos de etiquetado) **no** generan DPV nuevos: dependen de **DPV-095**, **DPV-109**, **DPV-097** y de la dependencia D12-01, ya registrados.

## 3. Decisiones pendientes propuestas (`decisiones_pendientes.md`)

| ID provisional | Decisión | Tipo | Prioridad | Depende de | Relación |
|---|---|---|---|---|---|
| DEC-16-01 | **[DECISIÓN METODOLÓGICA — no es decisión de inversión]** **Adoptar la estructura del motor CAPEX:** bloques, niveles de evidencia E1–E5, separación directo / indirecto / preoperativo / contingencia / capital de trabajo, regla de total (SUP-16-10), registro de procedencia de drivers | **METODOLÓGICA** | Media | — | DEC-002 (solo como insumo; no la decide) |
| DEC-16-02 | **Modalidad de contratación de la línea:** por lotes (L1–L7) vs llave en mano (L11), o ambas cotizaciones | Contratación (negocio) | Media | DEC-049, DPV-16-01 | DEC-038 |
| DEC-16-03 | **RFQ de frío y efluentes:** paquete integral vs desglosado por componente (define si FR-*/EF-* se costean aparte) | Alcance de RFQ | Media | DPV-109, DEC-043, DEC-046 | SUP-16-06 |
| DEC-16-04 | **Criterio de contingencia** por bloque cuando existan cotizaciones (clase de estimación) y tratamiento de la escalación | **METODOLÓGICA** | Media | DPV-16-09 | SUP-16-07 |
| DEC-16-05 | **Umbral de cobertura** para publicar un CAPEX preliminar total (el motor propone 100 %) y si se acepta publicar con faltantes no críticos | **METODOLÓGICA** | Media | DEC-16-01 | SUP-16-10 |
| DEC-16-06 | **Titularidad de cajones/módulos** de aves vivas con transporte tercerizado | Negocio / operativa | Baja | DPV-16-10 | DEC-056 |

Las decisiones **METODOLÓGICAS** (DEC-16-01, 04, 05) definen cómo se calcula y publica el CAPEX; no deben mezclarse en la reconciliación con decisiones de negocio o inversión.

Decisiones existentes que el motor deja **parametrizadas, no tomadas**: DEC-001 (escala), DEC-002 (eslabones), DEC-020 (abastecimiento de pollo vivo), DEC-023, DEC-024, DEC-027, DEC-033, DEC-035, DEC-037, DEC-038, DEC-043, DEC-046, DEC-047, DEC-049, DEC-053, DEC-056, DEC-063, DEC-064, DEC-065, DEC-074.

## 4. Fuentes propuestas (`25_fuentes/registro_fuentes.csv`)

Detalle en [`fuentes_16.csv`](fuentes_16.csv). **Todas `[PVDP]`**: la red de la sesión bloqueó los sitios (EGRESS_BLOCKED); ninguna se leyó en original.

| ID provisional | Fuente | Uso en el motor |
|---|---|---|
| FTE-16-001 | EDICI Ingeniería, blog (jun-2026), USD/m² de naves | OC-DP (E4); REF-EDI (no usada) |
| FTE-16-002 | SAGyP, Índice de costo de producción de pollos parrilleros (may-2026) | Ninguno (no leída); prioritaria para DPV-16-07 |
| FTE-16-003 | Municipalidad de Malargüe, pliego de sala de faena aviar (2022) | REF-MAL (no usada) |
| FTE-16-004 | RAFS 2015, unidades de faena móviles (EE. UU.) | REF-RAFS (no usada) |
| FTE-16-005 | UGA Extension B1214, galpones de reproductoras (EE. UU.) | REP-GAL (FUTURO, E4) |
| FTE-16-006 | Fabricantes asiáticos de plantas de alimento | ALI-REF (no usada; precio de equipo, no instalado) |
| FTE-16-007 | INTA EEA Famaillá, rentabilidad del pollo parrillero | Ninguno (no leída) |

Fuentes **existentes** reutilizadas: FTE-081 (Las Camelias, galpones; E4 en GRA-GAL), FTE-043 (Soychú, USD 300.000 por galpón; REF-SOY no usada).

## 5. Tensiones registradas (sin resolver)

| ID | Tensión | Tratamiento en el motor |
|---|---|---|
| T16-01 | `08_maquinaria/requerimientos_cotizacion.md` §3 incluye **EQ-28 y EQ-33** en L3 **y** en L6 | Asignados solo a L3; el RFQ debe aclararlo (DPV-16-06) |
| T16-02 | EQ-14 (caldera) figura en L2 y EQ-37 (agua helada) en L4, pero son servicios | Costeados en TE-GEN y FR-AGH; L2/L4 deben excluirlos o desglosarlos |
| T16-03 | El precio de galpón (FTE-081) es **cota inferior de prensa** y de alcance desconocido, y explica el 89–93 % (C2) y el 97–98 % (C3) del monto con precio (`MONTO_CON_REFERENCIAS_DEBILES_E4`) | No comparar C2/C3 con C1 por ese número (`capex_por_escala.md`) |
| T16-04 | Carga frigorífica: el cálculo físico parcial de 09C y el benchmark global difieren ×5,7 (5,2–6,2) | v1.1: FR-PAQ **sin capacidad**; se informan base, benchmark, contradicción abierta, diseño y margen PENDIENTES; no se cotiza con una sola cifra (DPV-109) |
| T16-07 | 12C no publica el **terreno sin reserva**; su terreno publicado incluye una reserva proxy (SUP-119) y rendering | CAPEX obtiene el terreno requerido con la función de 12C (CALCULO_MODELO_FUENTE, no fórmula propia) y lo rotula. **Propuesta:** que 12C publique `terreno_sin_reserva` |
| T16-08 | 09C publica dos métodos de DQO (A y B) que difieren ~19 % | CAPEX informa ambos y no elige (EF-BIO PENDIENTE) |
| T16-10 | `objetivo_20000` de 12C (33.345 m² medio) < terreno conceptual que 12C publica para 20.000 (43.660 m²) | Universos distintos: el conceptual suma una reserva PROXY fraccional para crecer más allá de 20.000 (SUP-119); el objetivo no. Alerta explicativa `SUPERFICIE_OBJETIVO_MENOR_QUE_CONCEPTUAL_12C_X`; no se usa max() (§8) |
| T16-09 | La matriz 08 define niveles de automatización solo en 4 escalas | Escalas intermedias usan la escala de referencia más cercana (SUP-16-05): es una asignación, no un dato |
| T16-05 | La flota de subproductos suma cuatro corrientes con vehículos distintos (cisterna, contenedores) por criterio **másico** | Cantidad = cota inferior; tipo de vehículo por corriente PENDIENTE (DPV-135) |
| T16-06 | Las acciones REEMPLAZA de la expansión salen de los niveles de automatización por escala de la matriz 08, que son hipótesis (SUP-065) | Resultado condicional, no conclusión |

## 6. Para `estado_proyecto.md` (al reconciliar)

- Hito: **motor CAPEX v1.1 construido y auditado en procedencia de drivers** (`19_capex/`), 82 tests + 10 mutaciones detectadas (v1.2); [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv) registra el origen de cada driver. **Sin CAPEX total publicable**: cobertura por conceptos 0–2,3 % según configuración; cobertura por valor no calculable.
- El motor queda listo para recibir cotizaciones (base de costos y capas de importación externas) sin tocar el código.
- **Cambio de alcance de `19_capex/README.md`:** el README original incluía "capital de trabajo inicial" dentro del CAPEX; por instrucción de la sesión 16 (no mezclar capital de trabajo con CAPEX) se trasladó a `20_opex` / `21_modelo_financiero`. Confirmar en la reconciliación y, si corresponde, actualizar el README de `20_opex`.
- Siguiente: RFQ cuando la fase lo habilite (DEC-049, hito H-B); OPEX (`20_opex`) puede iniciarse en paralelo con la misma lógica de evidencia.

## 7. Auditoría final de procedencia de drivers (cierre de la sesión 16)

Principio: CAPEX **consume** outputs de los modelos anteriores y no los recalcula. Resultado de la auditoría (todas las correcciones son de CAPEX; **no** se modificó la lógica de ningún modelo fuente):

| # | Inconsistencia encontrada en la v1.0 | Corrección (v1.1) | Test |
|---|---|---|---|
| 1 | Terreno "solo fase" (15.398–32.379 m²) presentado como terreno de 12C; 12C no publica terreno sin reserva | Separado en **mínimo físico** (CALCULO_MODELO_FUENTE) y terreno a adquirir (v1.2: decisión, §8); terreno publicado de 12C informado al lado; adquirido ≥ requerido | N01, N03 |
| 2 | m² construidos de P2 (1.796 / 7.795) en tablas sin indicar el perfil | Escenario de 12C explícito (`referencia` / `perfil_P2`) | N01 |
| 3 | OC-INF (USD/m²) aplicado a **todo** el terreno (incl. retiros, buffers, reserva); TER-PREP sobre todo el terreno | OC-INF = lote global; TER-PREP = mínimo físico; tipo de área por categoría | N02, N04 |
| 4 | Frío: "≥ X kWf" = suma CAPEX de cargas de 09C incluida una SUPUESTA ilustrativa, usada como capacidad del RFQ | FR-PAQ sin capacidad; detalle con base, benchmark, contradicción ×5,7, diseño y margen PENDIENTES | N15 |
| 5 | FR-AGH con la carga parcial de reposición como capacidad | PENDIENTE | N15 |
| 6 | EF-ECU = volumen diario (24 h de retención implícitas); EF-BIO = máximo de métodos A/B (elección) | Ambos PENDIENTES; valores de 09C en el texto | N16 |
| 7 | SB-L9 = suma propia de 4 corrientes de 09C | Variable de 09C `masa_biologica_potencialmente_segregable_en_origen_t_dia` | N16 |
| 8 | Capacidad de los lotes = aves/día ÷ horas (operativa) | Nominal requerido de 05; planta, operativa, diseño, garantizada y líneas separadas | N17 |
| 9 | Cadencia de nacimientos y perfil de planta de alimento fijados sin declararlos | Inputs explícitos y escenarios etiquetados | N07, N08 |
| 10 | "CAPEX conocido / estimado" mezclaban grupos de evidencia | `CAPEX_E1_E2/E3/E4/E5_USD`, `CALIDAD_MONTO`, cobertura por evidencia | N12, N14 |
| 11 | Sin registro de procedencia ni alerta de escala intermedia | `mapa_drivers_capex.csv`; alerta `ESCALA_INTERMEDIA`; verificación de consistencia sin corrección | N11, N13, N18 |

Verificado sin cambios: agua 15/25/38 L/ave y efluente = agua × fracción (09C, N16, N19); kWh nunca tratado como kW, transformador y grupo PENDIENTES (N05, N06); setters y hatchers separados y = 14B (N07); t/h y silos = 14B (N08); plazas, m² y galpones conceptuales = 03, granjas PENDIENTE (N09); flota de aves vivas = 12B (N10); lista de equipos = matriz 08 sin duplicados (N17).

Mutaciones nuevas (detectadas): D01 kWh → kVA (N05, N13), D02 cadencia cambiada en silencio (N07), D04 terreno recalculado fuera de 12C (N01), D05 área de 12C recalculada en CAPEX (N02).

## 8. Semántica del terreno (cierre final de la sesión 16, v1.2)

**Problema:** la v1.1 presentaba como terreno comprado con reserva (driver `terreno_adquirido`) al escenario `objetivo_20000` de 12C (33.345 m² medio), menor que el terreno que 12C publica para la configuración de 20.000 (43.660 m²).

**Semántica en 12C (sin modificar 12C):** `objetivo_20000` = escenario con `escala_objetivo = 20.000`: huella + exteriores + efluentes de la escala actual + Σ max(0, áreas(20.000) − áreas actuales) por categoría + rendering + retiros/buffers. A 20.000 (medio): 7.451 + 6.147 + 592 + 0 + 640 = 14.830 de área interna + 18.515 de retiros/buffers = 33.345. El terreno publicado sin objetivo a 20.000 suma en cambio una reserva PROXY de 50 % del operativo (7.095, SUP-119) para crecer **más allá** de 20.000: 21.925 + 21.735 = 43.660. El mínimo físico (sin reserva ni rendering) es 14.190 + 18.189 = 32.379.

**Corrección:** cuatro drivers separados — `terreno_minimo_fisico`, `terreno_conceptual_12c`, `superficie_escenario_objetivo_12c` (SUPERFICIE_ESCENARIO_OBJETIVO_X_12C), `terreno_requerido_arquitectura` — y `terreno_a_adquirir` como decisión (`criterio_terreno`, SUP-16-25). Alertas: `TERRENO_CRITERIO_NO_SELECCIONADO`, `TERRENO_ADQUIRIDO_MENOR_QUE_REQUERIDO_ARQUITECTURA`, `SUPERFICIE_OBJETIVO_MENOR_QUE_CONCEPTUAL_12C_X` (diferencia de universo, explicada) y `SUPERFICIE_OBJETIVO_NO_CUBRE_MINIMO_FISICO_X`. Tests N20–N24; mutación D06 (max silencioso). Decisión asociada: **DEC-16-07** (abajo).

| ID provisional | Decisión | Tipo | Prioridad | Depende de | Relación |
|---|---|---|---|---|---|
| DEC-16-07 | **Criterio de terreno a adquirir** (mínimo físico / conceptual 12C / escenario objetivo / requerido por la arquitectura / superficie de un lote concreto) | Negocio / arquitectura | Alta (antes de costear terreno) | DEC-063, DPV-16-03, DPV-141 | SUP-16-25 |
