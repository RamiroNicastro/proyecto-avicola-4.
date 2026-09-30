# Reconciliación de las sesiones paralelas 09A, 09B, 09C y 09D

**Fecha:** 2026-09-30 · **Tipo:** sesión administrativa de integración (no investiga una fase nueva) · **Rama:** `ccr-1f4a228e-7pyzou`

> **Qué hace este documento:** registra cómo se integraron en los registros maestros (`supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `glosario.md`, `estado_proyecto.md`, `25_fuentes/`) los resultados de cuatro sesiones que trabajaron en paralelo con IDs provisionales. **No** se tomaron decisiones, **no** se eligió escala, proveedor ni ubicación, **no** se modificaron modelos físicos (solo referencias de IDs en comentarios y textos de salida, verificado por regeneración idéntica de los CSV) y **no** se resolvieron contradicciones: quedan en §9.
> **No se iniciaron** localización, logística, layout, CAPEX ni OPEX.

---

## 1. Sesiones reconciliadas

| Sesión | Alcance | Carpetas | IDs provisionales | Estado tras la reconciliación |
|---|---|---|---|---|
| **09A** | Proceso industrial conceptual y maquinaria (v1.1) | `05_proceso_industrial`, `08_maquinaria` | SUP-09A-01…05, DPV-09A-01…11, DEC-09A-01…05, FTE-09A-001…036 | Integrada. `actualizaciones_gestion_09A.md` queda como histórico; `fuentes_09A.csv` retirado (en `registro_fuentes.csv`) |
| **09B** | Normativa SENASA y habilitaciones (v1.0 + corrección puntual) | `16_normativa_senasa` | SUP-09B-01…03, DPV-09B-01…15, DEC-09B-01…02, FTE-09B-01…25 | Integrada. `actualizaciones_gestion_09B.md` histórico; `fuentes_09B.csv` retirado |
| **09C** | Agua, efluentes, energía y frío (v1.1) | `11_agua_efluentes`, `12_energia_frio` | SUP-09C-01…10, DPV-09C-01…08, DEC-09C-01…07, FTE-09C-01…19 | Integrada. `actualizaciones_gestion_09C.md` histórico; `fuentes_09C.csv` retirado |
| **09D** | Simulador HTML v0.1 (interfaz) | `23_plan_expansion/simulador_html` | Ninguno (observaciones en `observaciones_html_v01.md`) | Integrada: estado del HTML actualizado; umbrales de interfaz anotados en SUP-060 sin crear supuestos de proyecto |

Últimos IDs oficiales al iniciar: SUP-060, DPV-087, DEC-036, FTE-193 (coinciden con los que declararon las tres sesiones).

## 2. Mapa de IDs provisionales → definitivos

Todos los IDs provisionales fueron reemplazados en `05`, `08`, `11`, `12`, `16` (textos, CSV de salida, `matriz_regulatoria.csv`, `matriz_equipos.csv` y comentarios de los modelos). Solo permanecen, como historia, en los tres `actualizaciones_gestion_09*.md` (marcados **ARCHIVO HISTÓRICO**) y en este documento.

### 2.1 Supuestos

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| SUP-09A-01 | **SUP-061** | Alta nueva |
| SUP-09A-02 | **SUP-062** | Alta nueva |
| SUP-09A-03 | **SUP-063** | Alta nueva |
| SUP-09A-04 | **SUP-064** | Alta nueva |
| SUP-09A-05 | **SUP-065** | Alta nueva |
| SUP-09B-01 | **SUP-066** | Alta nueva |
| SUP-09B-02 | **SUP-067** | Alta nueva |
| SUP-09B-03 | **SUP-068** | Alta nueva |
| SUP-09C-01 | **SUP-069** | Alta nueva |
| SUP-09C-02 | **SUP-070** | Alta nueva |
| SUP-09C-03 | **SUP-071** | Alta nueva |
| SUP-09C-04 | **SUP-072** | Alta nueva |
| SUP-09C-05 | **SUP-073** | Alta nueva |
| SUP-09C-06 | **SUP-074** | Alta nueva |
| SUP-09C-07 | **SUP-075** | Alta nueva |
| SUP-09C-08 | **SUP-076** | Alta nueva |
| SUP-09C-09 | **SUP-055** | Consolidado en SUP-055 (misma variable: perfiles de destino P1–P3) |
| SUP-09C-10 | **SUP-077** | Alta nueva |

### 2.2 Datos por validar

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DPV-09A-01 | **DPV-088** | Alta nueva |
| DPV-09A-02 | **DPV-089** | Alta nueva |
| DPV-09A-03 | **DPV-090** | Fusionado con DPV-09B-01 en DPV-090 (Decreto 4238/68) |
| DPV-09A-04 | **DPV-091** | Alta nueva |
| DPV-09A-05 | **DPV-092** | Alta nueva |
| DPV-09A-06 | **DPV-062** | Consolidado en DPV-062 (enfriamiento en plantas argentinas) |
| DPV-09A-07 | **DPV-093** | Alta nueva |
| DPV-09A-08 | **DPV-094** | Fusionado con DPV-09B-11 en DPV-094 (aturdido y bienestar en faena) |
| DPV-09A-09 | **DPV-095** | Fusionado con DPV-09C-07 en DPV-095 (lista de cargas y servicios por equipo) |
| DPV-09A-10 | **DPV-096** | Alta nueva |
| DPV-09A-11 | **DPV-097** | Alta nueva |
| DPV-09B-01 | **DPV-090** | Fusionado con DPV-09A-03 en DPV-090 (Decreto 4238/68) |
| DPV-09B-02 | **DPV-098** | Alta nueva |
| DPV-09B-03 | **DPV-099** | Alta nueva |
| DPV-09B-04 | **DPV-100** | Alta nueva |
| DPV-09B-05 | **DPV-101** | Alta nueva |
| DPV-09B-06 | **DPV-066** | Consolidado en DPV-066 (normativa de destino de subproductos) |
| DPV-09B-07 | **DPV-102** | Alta nueva |
| DPV-09B-08 | **DPV-103** | Alta nueva |
| DPV-09B-09 | **DPV-104** | Alta nueva |
| DPV-09B-10 | **DPV-058** | Consolidado en DPV-058 (normativa de transporte de aves vivas) |
| DPV-09B-11 | **DPV-094** | Fusionado con DPV-09A-08 en DPV-094 (aturdido y bienestar en faena) |
| DPV-09B-12 | **DPV-105** | Alta nueva |
| DPV-09B-13 | **DPV-086** | Consolidado en DPV-086 (plazos, incluida la habilitación SENASA) |
| DPV-09B-14 | **DPV-106** | Alta nueva |
| DPV-09B-15 | **DPV-107** | Alta nueva |
| DPV-09C-01 | **DPV-108** | Alta nueva |
| DPV-09C-02 | **DPV-109** | Alta nueva |
| DPV-09C-03 | **DPV-110** | Alta nueva |
| DPV-09C-04 | **DPV-111** | Alta nueva |
| DPV-09C-05 | **DPV-112** | Alta nueva |
| DPV-09C-06 | **DPV-113** | Alta nueva |
| DPV-09C-07 | **DPV-095** | Fusionado con DPV-09A-09 en DPV-095 (lista de cargas y servicios por equipo) |
| DPV-09C-08 | **DPV-114** | Alta nueva |

Alta propia de la reconciliación (sin ID provisional): **DPV-115** — revisión del anteproyecto por SENASA antes de construir (las preguntas P-45 y P-27 de `16_normativa_senasa/preguntas_senasa.md` no tenían DPV).

### 2.3 Decisiones pendientes

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DEC-09A-01 | **DEC-037** | Alta nueva |
| DEC-09A-02 | **DEC-038** | Alta nueva |
| DEC-09A-03 | **DEC-039** | Alta nueva |
| DEC-09A-04 | **DEC-040** | Alta nueva |
| DEC-09A-05 | **DEC-041** | Alta nueva |
| DEC-09B-01 | **DEC-042** | Alta nueva |
| DEC-09B-02 | **DEC-030** | Consolidada en DEC-030 (elaborados: se agrega dónde se elaboran) |
| DEC-09C-01 | **DEC-043** | Alta nueva |
| DEC-09C-02 | **DEC-044** | Alta nueva |
| DEC-09C-03 | **DEC-045** | Alta nueva |
| DEC-09C-04 | **DEC-046** | Alta nueva |
| DEC-09C-05 | **DEC-047** | Alta nueva |
| DEC-09C-06 | **DEC-027** | Consolidada en DEC-027 (destino de subproductos: se agregan lodos y flotados) |
| DEC-09C-07 | **DEC-048** | Alta nueva |

Alta propia de la reconciliación (sin ID provisional): **DEC-049** — proveedor(es) de equipamiento, abierta y bloqueada por la fase (CLAUDE.md).

### 2.4 Fuentes

| ID provisorio | ID definitivo | Fuente | Tratamiento |
|---|---|---|---|
| FTE-09A-001 | **FTE-194** | Meyn LEAP Concept - Scalable Poultry Processing; Meyn Solutions | Alta nueva |
| FTE-09B-01 | **FTE-229** | Resolución SENASA 592/2026 - actualización del Reglamento de Inspecció | Alta nueva |
| FTE-09C-01 | **FTE-252** | Uso de agua por etapa en faena avícola (Poultry Processing Reuse Water | Entrada maestra FTE-252; absorbe FTE-09C-18 |
| FTE-09A-002 | **FTE-195** | Meyn to Avícola y Porcinos 2026 in Buenos Aires | Alta nueva |
| FTE-09B-02 | **FTE-230** | Habilitar y solicitar modificaciones en establecimientos de faena y el | Alta nueva |
| FTE-09C-02 | **FTE-253** | Poultry Processing: Measuring True Water Use: Converting Your Plant Fr | Alta nueva |
| FTE-09A-003 | **FTE-196** | Broiler / poultry processing solutions for all processes and capacitie | Alta nueva |
| FTE-09B-03 | **FTE-231** | Resolución SENASA 233/1998 - BPM y POES obligatorios | Alta nueva |
| FTE-09C-03 | **FTE-254** | Consumo de agua y energía en abatedouros de frangos (Avaliação do cons | Alta nueva |
| FTE-09A-004 | **FTE-197** | Calisa2 greenfield in Argentina is like an oasis (caso de cliente) | Alta nueva |
| FTE-09B-04 | **FTE-232** | Resolución SENASA 553/2002 - modificación del capítulo XX (aves) del D | Alta nueva |
| FTE-09C-04 | **FTE-255** | Slaughterhouse Water Use and Wastewater Characteristics (FAPC-240) y r | Alta nueva |
| FTE-09A-005 | **FTE-198** | Marel Buenos Aires (ficha de empresa); Success for Marel at Avícolas y | Alta nueva |
| FTE-09C-05 | **FTE-256** | Revisiones de caracterización y tratamiento de efluentes de faena avíc | Alta nueva |
| FTE-09B-05 | **FTE-083** | Resolución SENASA 593/2026 - procedimiento de habilitación de destinos | Consolidada en FTE-083 (misma norma: Res. SENASA 593/2026; otro comunicado oficial) |
| FTE-09A-006 | **FTE-199** | Automated poultry cut-up scales to 6.500 birds per hour | Alta nueva |
| FTE-09B-06 | **FTE-233** | Bienestar animal en industria aviar; Manual de bienestar animal en pla | Alta nueva |
| FTE-09C-06 | **FTE-257** | Nitrógeno, fósforo y grasas en efluentes de faena avícola; efecto de l | Alta nueva |
| FTE-09A-007 | **FTE-200** | Compact Plant 396; Designing a Reliable Poultry Processing Plant (blog | Alta nueva |
| FTE-09B-07 | **FTE-234** | Resolución SENASA 723/2025 - habilitación sanitaria de medios de trans | Alta nueva |
| FTE-09C-07 | **FTE-258** | Tratamiento de efluentes líquidos provenientes de la industria frigorí | Alta nueva |
| FTE-09A-008 | **FTE-201** | BAADER Sales & Service; After Sales | Alta nueva |
| FTE-09B-08 | **FTE-235** | Habilitar/Rehabilitar transportes de productos de origen animal y alim | Alta nueva |
| FTE-09C-08 | **FTE-259** | Resolución ADA 336/2003 (Provincia de Buenos Aires) - parámetros de ca | Alta nueva |
| FTE-09A-009 | **FTE-202** | Ingeniero Galimberti - Equipamiento para la industria avícola (product | Alta nueva |
| FTE-09B-09 | **FTE-236** | Código Alimentario Argentino art. 982 y ss. - agua potable | Entrada maestra FTE-236; absorbe FTE-09C-16 (CAA art. 982) |
| FTE-09C-09 | **FTE-260** | Energía en plantas de faena avícola (Energy and water use in poultry p | Alta nueva |
| FTE-09A-010 | **FTE-203** | Peladora de pollos D/66, escaldadora E-50, kit básico faena | Alta nueva |
| FTE-09B-10 | **FTE-237** | Ley 22.375 (Ley Federal de Carnes) y proyecto de derogación no aprobad | Alta nueva |
| FTE-09C-10 | **FTE-261** | Energy use in food refrigeration (Defra/Grimsby); Air blast freezers a | Alta nueva |
| FTE-09A-011 | **FTE-204** | Máquinas desplumadoras y artículos para faena | Alta nueva |
| FTE-09B-11 | **FTE-238** | Resolución SENASA 233/2026 - elimina la presentación de habilitaciones | Alta nueva |
| FTE-09C-11 | **FTE-262** | Temperaturas de escaldado y de limpieza/esterilización (Best practice  | Alta nueva |
| FTE-09A-012 | **FTE-205** | Poultry slaughter lines 500–5.000 birds per hour (fichas de producto) | Alta nueva |
| FTE-09B-12 | **FTE-239** | RENSPA, DT-e y registro del criador avícola (SIGSA); Res. SENASA 1699/ | Alta nueva |
| FTE-09C-12 | **FTE-263** | Tratamiento anaerobio de efluentes de faena (UASB granular; DAF-UASB;  | Alta nueva |
| FTE-09A-013 | **FTE-206** | Poultry processing equipment / automatic chicken slaughter line | Alta nueva |
| FTE-09B-13 | **FTE-240** | Certificación electrónica para exportar productos aviares (SIGCER) y a | Alta nueva |
| FTE-09C-13 | **FTE-264** | Elimination of DAF sludge disposal through resource recovery y documen | Alta nueva |
| FTE-09A-014 | **FTE-207** | 500–1.000 birds per hour poultry slaughter line | Alta nueva |
| FTE-09B-14 | **FTE-241** | Aprobación/inscripción de materias primas y productos de origen animal | Alta nueva |
| FTE-09C-14 | **FTE-265** | ASHRAE Handbook - Refrigeration, capítulo 19 'Thermal Properties of Fo | Alta nueva |
| FTE-09A-015 | **FTE-208** | BAYLE SA - French manufacturer of poultry processing equipment | Alta nueva |
| FTE-09B-15 | **FTE-242** | Rotulado de productos cárneos aviares (SENASA) y CAA cap. V; Res. GMC  | Alta nueva |
| FTE-09C-15 | **FTE-266** | Enmienda de Kigali al Protocolo de Montreal en Argentina (entrada en v | Alta nueva |
| FTE-09A-016 | **FTE-209** | Foodmate integrated line / cut-up systems | Alta nueva |
| FTE-09B-16 | **FTE-243** | Resolución SENASA 205/2014 - incorpora el APPCC/HACCP al Reglamento de | Alta nueva |
| FTE-09C-16 | **FTE-236** | Código Alimentario Argentino, artículo 982 (agua potable) | Fusionada con FTE-09B-09 en FTE-236 (mismo artículo: CAA art. 982) |
| FTE-09A-017 | **FTE-210** | Prime Equipment Group (ficha de proveedor) | Alta nueva |
| FTE-09B-17 | **FTE-244** | Temperaturas de conservación y enfriamiento de aves (extractos de busc | Alta nueva |
| FTE-09C-17 | **FTE-267** | Guías comerciales de respaldo eléctrico para cámaras frigoríficas (Col | Alta nueva |
| FTE-09A-018 | **FTE-211** | TORIDAS / YIELDAS automated deboning; Poultry World | Alta nueva |
| FTE-09B-18 | **FTE-245** | Certificación Halal en Argentina: convenio de Cancillería, capacitació | Alta nueva |
| FTE-09C-18 | **FTE-252** | Requisitos USDA de reposición de agua en chiller y escaldador (9 CFR 3 | Fusionada con FTE-09C-01 en FTE-252 (misma URL: informe NACMCF, que cita 9 CFR 381.66) |
| FTE-09A-019 | **FTE-212** | Pre-owned poultry machines (Drobtech, Use Poultry Tech, Isotek) | Alta nueva |
| FTE-09B-19 | **FTE-246** | Registros Especiales Aduaneros - inscripción de importador/exportador | Alta nueva |
| FTE-09C-19 | **FTE-268** | Refrigerantes naturales e industriales (CO2 y amoníaco: normativa y te | Alta nueva |
| FTE-09A-020 | **FTE-213** | Poultry packaging machines; Poultry packaging solutions | Alta nueva |
| FTE-09B-20 | **FTE-247** | Productos no destinados al consumo humano (subproductos, harinas de ca | Alta nueva |
| FTE-09A-021 | **FTE-214** | Traysealers; Thermoforming packaging machines | Alta nueva |
| FTE-09B-21 | **FTE-248** | Faenador (aves - industria) y ficha de documentación de establecimient | Alta nueva |
| FTE-09A-022 | **FTE-215** | Spiral freezers vs tunnel freezers (notas comerciales); JBT Frigoscand | Alta nueva |
| FTE-09B-22 | **FTE-249** | Resolución SENASA 591/2026 - derogación de 42-43 normas obsoletas | Alta nueva |
| FTE-09A-023 | **FTE-216** | Broiler stunning solutions: electrical and controlled atmosphere; Huma | Alta nueva |
| FTE-09B-23 | **FTE-016** | Decreto 4238/1968 - texto actualizado y capítulo XX (recursos de argen | Consolidada en FTE-016 (misma norma y mismo ID InfoLeg 24788) |
| FTE-09A-024 | **FTE-217** | Chillin' Chickens - Which Method Works Best; Rodrigues et al. 2014 (J. | Alta nueva |
| FTE-09B-24 | **FTE-250** | Equiparación de frigoríficos provinciales con tránsito federal (Chaco, | Alta nueva |
| FTE-09A-025 | **FTE-218** | Small-scale poultry processing (FAO); Small-Scale Poultry Processing ( | Alta nueva |
| FTE-09B-25 | **FTE-251** | Decreto 697/2026 - Código Alimentario Argentino: reorganización del Si | Alta nueva |
| FTE-09A-026 | **FTE-219** | Human health implications of live hang work (informe); Poultry line sp | Alta nueva |
| FTE-09A-027 | **FTE-220** | Animal Welfare Approved - Slaughter guidelines for poultry | Alta nueva |
| FTE-09A-028 | **FTE-221** | Meat and poultry sanitation (notas comerciales) | Alta nueva |
| FTE-09A-029 | **FTE-222** | Faena de aves: guía de buenas prácticas para el uso y construcción del | Alta nueva |
| FTE-09A-030 | **FTE-192** | Decreto 4238/68 - enfriamiento de aves por aire (extracto) | Consolidada en FTE-192 (misma URL: Decreto 4238/68, MAGyP) |
| FTE-09A-031 | **FTE-223** | Aves - Industria (SENASA) | Alta nueva |
| FTE-09A-032 | **FTE-224** | Frigorífico Mark S.A., una planta aviar de vanguardia (Pymes exportan, | Alta nueva |
| FTE-09A-033 | **FTE-225** | 40' Poultry Plant in a Box | Alta nueva |
| FTE-09A-034 | **FTE-226** | Abatedouro modular de aves | Alta nueva |
| FTE-09A-035 | **FTE-227** | Sulmaq is part of Marel | Alta nueva |
| FTE-09A-036 | **FTE-228** | Poultry processing equipment used (Isotek) - complete Meyn processing  | Alta nueva |

## 3. Supuestos integrados

**17 nuevos (SUP-061 a SUP-077)** + 1 consolidado en SUP-055. Ninguno se elevó a hecho: todos siguen `Vigente` como hipótesis.

| Grupo | Supuestos | Marca |
|---|---|---|
| Proceso: disponibilidad y factor de velocidad (η = D × R) | SUP-061 | **[SUPUESTO DE SENSIBILIDAD]** — no es desempeño demostrado ni velocidad garantizada |
| Proceso: ecuación de 24 h, tiempos de limpieza, sanitización y ventanas de mantenimiento; `t_limpieza` provisional | SUP-062 | **[SUPUESTO DE SENSIBILIDAD]** — holgura negativa = alerta, no descarte |
| Proceso: productividades manuales (puestos equivalentes, no dotación) | SUP-063 | `[PVDP · débil]` + variante prudente de sensibilidad |
| Proceso: residencia en el enfriamiento | SUP-064 | `[PVDP]` |
| Maquinaria: 76 equipos, automatización por escala, criticidad | SUP-065 | Hipótesis de trabajo |
| Capacidad nominal vs operativa | SUP-052 (anotado), SUP-053 (anotado) | Jerarquía equipo → cuello de botella → capacidad operativa → producción real; capacidades de proveedores = referencia nominal |
| Normativa: caso de referencia tránsito federal; vigencia como hipótesis; no adoptar valores reglamentarios | SUP-066, SUP-067, SUP-068 | No son decisiones |
| Utilities: L/ave por etapa | SUP-069 | **[SUPUESTO DE SENSIBILIDAD]** 15/25/38 L/ave |
| Utilities: fracción a efluente (80/88/95 %), cinco aguas, base horaria | SUP-070 | **[SUPUESTO DE SENSIBILIDAD]** |
| Utilities: DQO/ave (50/100/180 g), métodos A/B, recuperación de sangre (0,85 editable) | SUP-071 | **[SUPUESTO DE SENSIBILIDAD]** |
| Utilities: lodos | SUP-072 | **[ILUSTRATIVO — PENDIENTE]** |
| Utilities: kWh/ave (vía kWh/t PV) y potencia media | SUP-073 | **[SUPUESTO DE SENSIBILIDAD]**; pico PENDIENTE |
| Utilities: MJ/ave (agua caliente) | SUP-074 | **[SUPUESTO DE SENSIBILIDAD]**; pico térmico PENDIENTE |
| Utilities: perfiles de frío, COP 4/3/2,3 y 1,8/1,4/1,1 | SUP-075 | **[SUPUESTO DE SENSIBILIDAD]**; carga total PENDIENTE |
| Utilities: carga crítica de respaldo | SUP-076 | **[ILUSTRATIVO — PROXY]** |
| Utilities: contraste top-down/bottom-up | SUP-077 | **[CRITERIO DE CONTROL]** |
| Frío: garras y menudencias congeladas informativas | SUP-055 (consolidado) | — |
| HTML: umbrales de interfaz | SUP-060 (anotado) | Umbrales visuales ilustrativos / criterios de interfaz; **no** límites industriales |

## 4. Datos por validar integrados

**28 nuevos (DPV-088 a DPV-115)**: 27 de las sesiones + DPV-115 (alta de la reconciliación). 4 propuestas consolidadas en DPV existentes y 3 pares fusionados (§8). **Ningún DPV se perdió:** cada ID provisional tiene destino en §2.2.

El registro no tenía una columna de prioridad; se mantuvo el formato y se agregó la prioridad en *Observaciones* con la escala `CRÍTICO / IMPORTANTE / ÚTIL` (leyenda en el encabezado de `datos_por_validar.md`). Las prioridades de 09A y 09C se copiaron; las de 09B (que no las traía) se **asignaron en la reconciliación** y así se indica en cada fila.

| DPV | Dato (resumen) | Prioridad | Origen |
|---|---|---|---|
| DPV-090 | Decreto 4238/68 — texto actualizado y requisitos de faena de aves | CRÍTICO ANTES DE DISEÑAR | sesiones 09A y 09B |
| DPV-097 | Definición contractual de capacidad de cada proveedor | CRÍTICO ANTES DE ESPECIFICAR EQUIPOS | sesión 09A |
| DPV-106 | Normativa ambiental, hídrica, municipal, de bomberos y de energía por localización… | CRÍTICO ANTES DE ELEGIR LOCALIZACIÓN | sesión 09B |
| DPV-115 | Revisión del anteproyecto por SENASA antes de construir | CRÍTICO ANTES DE DISEÑAR | reconciliación |
| DPV-058 | Normativa de transporte de aves vivas (Res. SENASA 723/2025) | IMPORTANTE | consolidado 09B |
| DPV-062 | Enfriamiento en plantas argentinas (método admitido, temperaturas, inmersión) | IMPORTANTE | consolidado 09A |
| DPV-066 | Normativa de subproductos, graserías y alimentos para animales | IMPORTANTE ANTES DE INVERTIR | consolidado 09B |
| DPV-067 | Carga de efluentes por ave, L/ave, límites de vuelco | IMPORTANTE ANTES DE INVERTIR | anotado 09C |
| DPV-086 | Plazos reales de habilitación y ampliación | IMPORTANTE ANTES DE INVERTIR | consolidado 09B (existente) |
| DPV-088 | Capacidad real vs nominal de líneas avícolas en operación | IMPORTANTE ANTES DE INVERTIR | sesión 09A |
| DPV-089 | Presencia verificada y servicio técnico local de cada proveedor en Argentina | IMPORTANTE ANTES DE INVERTIR | sesión 09A |
| DPV-091 | Limpieza, sanitización y mantenimiento reales por escala, configuración y automatización | IMPORTANTE | sesión 09A |
| DPV-092 | Productividad de operarios argentinos | IMPORTANTE | sesión 09A |
| DPV-094 | Aturdido y bienestar en faena | IMPORTANTE ANTES DE DISEÑAR | sesiones 09A y 09B |
| DPV-095 | Lista de cargas y servicios por equipo (desde el catálogo EQ-01 a EQ-76 + cotizaciones) | IMPORTANTE ANTES DE INVERTIR | sesiones 09A y 09C |
| DPV-096 | Tiempo de congelado hasta −18 °C por producto y envase y capacidad (kg/h) por tipo de… | IMPORTANTE | sesión 09A |
| DPV-098 | Temperaturas vigentes de enfriamiento, conservación refrigerada, congelada y transporte… | IMPORTANTE ANTES DE DISEÑAR | sesión 09B |
| DPV-099 | Aplicación práctica actual de la Ley 22.375 (continúa en el corpus normativo oficial) y… | IMPORTANTE ANTES DE INVERTIR | sesión 09B |
| DPV-100 | Alcance de la Res. SENASA 233/2026 sobre el trámite de habilitación de plantas de faena | IMPORTANTE | sesión 09B |
| DPV-101 | Dotación, costos y tasas del servicio de inspección veterinaria (SIV); aranceles de… | IMPORTANTE ANTES DE INVERTIR | sesión 09B |
| DPV-102 | Texto de la Res. SENASA 205/2014 (Plan APPCC obligatorio), manuales complementarios y… | IMPORTANTE ANTES DE DISEÑAR | sesión 09B |
| DPV-103 | Requisitos de agua de la planta | IMPORTANTE ANTES DE INVERTIR | sesión 09B |
| DPV-107 | Texto del Decreto 697/2026 y su convivencia con el Decreto 4238/68 | IMPORTANTE | sesión 09B |
| DPV-108 | Indicadores energéticos de plantas de faena argentinas | IMPORTANTE ANTES DE INVERTIR | sesión 09C |
| DPV-109 | Balance frigorífico de proveedor por escala (2.500–20.000) y perfil (P1–P3) | IMPORTANTE ANTES DE INVERTIR | sesión 09C |
| DPV-111 | Lodos y flotados | IMPORTANTE ANTES DE INVERTIR | sesión 09C |
| DPV-114 | Sólidos que efectivamente llegan al efluente y generación de lodos (kg MS/día, % de… | IMPORTANTE ANTES DE INVERTIR | sesión 09C |
| DPV-093 | Régimen de importación de bienes usados en Argentina (requisitos, certificaciones,… | ÚTIL PARA OPTIMIZAR | sesión 09A |
| DPV-104 | Habilitación actual de la carnicería familiar (municipal/bromatología) y rubros que… | ÚTIL PARA OPTIMIZAR | sesión 09B |
| DPV-105 | Normas derogadas por la Res. SENASA 591/2026 y texto de la Res. 592/2026 | ÚTIL PARA OPTIMIZAR | sesión 09B |
| DPV-110 | Normativa argentina de seguridad de instalaciones frigoríficas con amoníaco y CO₂;… | ÚTIL PARA OPTIMIZAR | sesión 09C |
| DPV-112 | Productos de limpieza, sanitizantes y antimicrobianos admitidos en plantas de aves en… | ÚTIL PARA OPTIMIZAR | sesión 09C |
| DPV-113 | Demanda térmica real (vapor y agua caliente) en plantas argentinas y duración de la… | ÚTIL PARA OPTIMIZAR | sesión 09C |

## 5. Decisiones integradas

**13 nuevas (DEC-037 a DEC-049)**, todas `Abierta`, sin resultado. Quedan abiertas, entre otras:

| Tema | Decisión |
|---|---|
| Nivel de automatización | DEC-037 |
| Arquitectura / configuración de línea | DEC-038 (y DEC-033 arquitectura de crecimiento) |
| Equipos nuevos / usados | DEC-039 |
| Redundancia, repuestos y servicio | DEC-040 |
| Método de aturdido | DEC-041 |
| Reunión técnica con SENASA | DEC-042 |
| Tratamiento de efluentes | DEC-043 |
| Prevención en origen (sangre, transporte en seco) | DEC-044 |
| Fuente térmica | DEC-045 |
| Refrigeración y refrigerante | DEC-046 |
| Generación de respaldo | DEC-047 |
| Tabla equipo → servicios (top-down/bottom-up) | DEC-048 |
| Proveedor | DEC-049 (bloqueada por la fase) |
| Segundo turno | DEC-036 (anotada) |
| Enfriamiento | DEC-026 (anotada) |
| Rendering y destino de subproductos, lodos y flotados | DEC-027 (ampliada), DEC-029 |
| Escala | DEC-001 (anotada), DEC-033 |
| Ubicación | DEC-003 (anotada) |
| Nivel de habilitación | DEC-009 (anotada) |

## 6. Fuentes integradas

**75 nuevas (FTE-194 a FTE-268)** en `25_fuentes/registro_fuentes.csv` y en `25_fuentes/bibliografia.md` (por tipo de fuente, con nota de sesión). 80 fuentes provisionales → 78 IDs (5 consolidaciones, §8). Validación: 268 filas, 11 columnas, IDs únicos, ninguna URL de las sesiones 09 duplicada (queda un duplicado preexistente, T-13).

**Proveedores (regla 9 del encargo):**

| Evidencia | Fuentes | Uso permitido |
|---|---|---|
| **Fuerte — declaración del fabricante** (página oficial leída por el promotor; confirmada en revisión externa; **lectura primaria pendiente de reproducir en entorno Claude**) | FTE-194 Meyn LEAP (~1.300 → 15.000 aves/h), FTE-197 JBT Marel — Calisa2 (9.500 → 15.000 aves/h), FTE-200 BAADER Compact Plant 396 (~600–1.600 aves/h) | Referencia tecnológica y nominal. **No** son capacidad del proyecto, ni velocidad garantizada, ni benchmark de CAPEX, dotación o escala mínima eficiente |
| **Débil / PVDP** (extractos de buscador, portales comerciales, revendedores) | Todas las demás de FTE-195 a FTE-228: `[PVDP]`; las de categoría C (portales B2B, revendedores, blogs, prensa, directorios) son `[PVDP · débil]` | Solo existencia de oferta y rangos declarados; nunca dimensionamiento |

**Normativa (regla 7 del encargo):** se preservaron los cuatro estados de `matriz_regulatoria.csv` (`VERIFICADO EN PRIMARIA` = 0, `PVDP`, `DEPENDE DE JURISDICCIÓN`, `POR CONSULTAR A SENASA`). La relación **Decreto 697/2026 → Decreto 815/1999** figura como *"confirmado en revisión externa del proyecto; lectura primaria pendiente de reproducir en entorno Claude"* (FTE-251, DPV-107): **no** se elevó a verificado en primaria ni se degradó a extracto. La reconciliación intentó reproducir las lecturas (meyn.com, baader.com, jbtmarel.com, argentina.gob.ar, boletinoficial.gob.ar): **CONNECT 403** (DPV-009 anotado). El término quedó definido en el glosario.

## 7. Registros existentes actualizados (anotaciones con fecha, sin borrar historia)

- **Supuestos:** SUP-030, SUP-042, SUP-052, SUP-053, SUP-055, SUP-060.
- **Datos por validar:** DPV-007, DPV-009, DPV-024, DPV-031, DPV-034, DPV-052, DPV-053, DPV-058 (ampliado), DPV-061, DPV-062 (ampliado), DPV-066 (ampliado), DPV-067, DPV-072, DPV-074, DPV-078, DPV-082, DPV-083, DPV-085, DPV-086 (ampliado), DPV-087; leyenda de prioridad en el encabezado.
- **Decisiones:** DEC-001, DEC-003, DEC-004, DEC-009, DEC-012, DEC-026, DEC-027 (ampliada), DEC-030 (ampliada), DEC-033, DEC-035, DEC-036.
- **Fuentes:** FTE-016, FTE-083, FTE-192 (entradas maestras), FTE-082, FTE-146, FTE-181, FTE-135, FTE-157 (anotaciones 09B/09C).
- **Glosario:** 72 términos nuevos; actualizados "Tránsito federal", "HACCP" → "APPCC / HACCP", "PVDP", "Agua de proceso"; nuevo estado "Confirmado en revisión externa".
- **Estado del proyecto:** tablero *modelo preliminar completado* vs *evidencia de campo pendiente*, hitos 09A–09D y reconciliación, resultados por módulo, próximos pasos y módulos habilitados.
- **Módulos:** READMEs de `05`, `08`, `11`, `16`, `23` y `23/simulador_html`; conclusiones de `05`, `11`, `12`, `16` (nota de reconciliación); `cuellos_botella.md`, `especificacion_simulador_html.md` (ya no "no construido"), `escenarios_escala.md`, `gates_expansion.md`, `conclusiones_escala.md`, `observaciones_html_v01.md` (O8 resuelto); `17_exportacion/requisitos_planta_exportadora.md` (anotaciones 09B §6: APPCC obligatorio, POES Res. 233/1998, Director Técnico derogado según extractos, análisis normativo ya no "pendiente").

## 8. Duplicados eliminados / consolidados

| Tipo | Caso | Resultado |
|---|---|---|
| Consolidación en existente | SUP-09C-09 → **SUP-055** | Misma variable (perfiles P1–P3) |
| Consolidación en existente | DPV-09A-06 → **DPV-062**; DPV-09B-06 → **DPV-066**; DPV-09B-10 → **DPV-058**; DPV-09B-13 → **DPV-086** | Ampliación del "dato requerido" + anotación fechada |
| Fusión entre sesiones | DPV-09A-03 + DPV-09B-01 → **DPV-090** (Decreto 4238/68); DPV-09A-08 + DPV-09B-11 → **DPV-094** (aturdido y bienestar); DPV-09A-09 + DPV-09C-07 → **DPV-095** (servicios y cargas por equipo) | Un solo DPV con el alcance de ambos |
| Consolidación en existente | DEC-09B-02 → **DEC-030**; DEC-09C-06 → **DEC-027** | Ampliación del alcance, sin decidir |
| Fuente misma URL / misma norma | FTE-09A-030 → **FTE-192**; FTE-09B-05 → **FTE-083**; FTE-09B-23 → **FTE-016** | Entrada maestra con URLs y datos adicionales |
| Fuente misma URL / mismo artículo | FTE-09C-18 → **FTE-252**; FTE-09B-09 + FTE-09C-16 → **FTE-236** | Entrada maestra; se conserva la observación de la absorbida |
| Glosario | N+1 (09A y 09C) → una entrada; "Cuello de botella", "IQF", "Plan CREHA", "Capacidad operativa", "Chiller" ya existían → no se duplicaron; duplicados **preexistentes** "Menudencias" y "Balance de masa" unificados | Sin términos repetidos |
| Archivos | `fuentes_09A.csv`, `fuentes_09B.csv`, `fuentes_09C.csv` retirados (contenido completo en `registro_fuentes.csv`; historia en git) | Regla 13 |
| Administrativo | 9 filas de `registro_fuentes.csv` (FTE-185 a FTE-193) tenían fin de línea CRLF mezclado; quedaron en LF al reescribir el archivo (contenido sin cambios) | CSV homogéneo |

## 9. Contradicciones / tensiones abiertas

Ninguna se resolvió en esta sesión. Cada una queda con el registro que la cerrará.

| ID | Tensión | Módulos | Detalle | Qué la cierra |
|---|---|---|---|---|
| **T-01** | Demanda eléctrica **top-down vs futura suma bottom-up** de equipos | 09C ↔ 09A | ~0,8 kWh/ave y reparto ilustrativo de consumidores (SUP-073) sin contraste posible: los 76 equipos no tienen kW, agua, aire, vapor ni frío cuantificados | DPV-095, DEC-048, criterio SUP-077 (alerta fuera de [1/1,5; 1,5], sin ajustar) |
| **T-02** | **Frío físico vs benchmark energético** | 09C interno | Carga del producto ~450 kWh/día vs reparto top-down ~2.540 kWh/día a 10.000 aves/día (×5,7) | DPV-109, DPV-096 |
| **T-03** | **Tiempo de limpieza vs capacidad de dos turnos** y bases horarias distintas | 09A ↔ 23 ↔ 09C ↔ HTML | 09A: con 16 h netas la holgura es +0,9 / −2,8 / −8,3 h (limpieza 2–4 h, sanitización 1–2 h); escala (SUP-053): 16 h = capacidad teórica de la línea; utilities: caudal horario sobre 12 h (8 netas + 4 limpieza) y potencia media sobre 14 h, que es el **extremo bajo** de los 14–21 h/día de operación de 09A; HTML: alerta > 10 h sin ecuación de 24 h | DPV-091, DPV-113, DPV-082, DEC-036 |
| **T-04** | **Capacidad de línea comercial vs escala del proyecto** | 09A ↔ 23 | Ritmos requeridos 312–2.500 aves/h (8 h netas) vs ofertas declaradas: BAADER CP396 ~600–1.600, Meyn LEAP desde ~1.300, Calisa2 9.500–15.000 aves/h. A 2.500 aves/día una línea de 600 aves/h trabajaría ~4 h; nada de esto define escala mínima ni capacidad | DPV-083, DPV-088, DPV-097, DEC-038 |
| **T-05** | **Normativa de planta vs diseño conceptual** | 09B ↔ 09A/09C | SUP-068 impide adoptar valores reglamentarios, pero utilities usa 4 °C, −18 °C, chiller a 1 °C y esterilización a 82 °C como **supuestos de cálculo**; 09A zonifica y ubica puestos de inspección **sin** norma leída (puestos por velocidad de línea desconocidos) | DPV-090, DPV-098, DPV-115 |
| **T-06** | **Nombres de capacidad** | HTML ↔ SUP-052 ↔ 09A | El HTML llama "capacidad instalada" a la escala E (= capacidad operativa al 100 % según SUP-052), no a la capacidad nominal de 09A. Mismo valor, nombres distintos | Alinear nombres en HTML v0.5 (no se editó el HTML) |
| **T-07** | Efluente: **métodos A y B divergen** en los extremos | 09C interno | B/A 0,3–0,5 en el escenario bajo; SST 2,46 en el alto | DPV-067, DPV-114 |
| **T-08** | **Escalas de prioridad con nombres distintos** | 23 ↔ 09A ↔ registros | DPV: CRÍTICO / IMPORTANTE / ÚTIL; escala: "CRÍTICO ANTES DE DEFINIR ESCALA…"; equipos: CRÍTICO / IMPORTANTE / SECUNDARIO; DEC: Alta / Media / Baja | Leyenda en `datos_por_validar.md`; unificación pendiente |
| **T-09** | **Decreto 697/2026 vs Decreto 697/2024** | 16 ↔ 01/17 | Mismo número, normas distintas (CAA vs derechos de exportación, FTE-100) | Aclarado en DPV-107 y glosario |
| **T-10** | Puntos abiertos heredados de 09B | 16 | C1 (Res. 233/2026), C2 (Ley 22.375), C3 (capítulos del Decreto 4238/68), C4 (Director Técnico), C5 (temperaturas de origen dudoso), C6 (Decreto 697/2026 ↔ 4238/68) en `mapa_regulatorio.md` §5 | DPV-100, DPV-099, DPV-090, DPV-105, DPV-098, DPV-107 |
| **T-11** | Tres universos de agua | 03 ↔ 04 ↔ 09C | Agua de bebida de granja (SUP-030), agua incorporada al producto (SUP-042) y agua industrial (SUP-069): no se suman ni se restan (regla 18). Nomenclatura alineada en el glosario ("agua de proceso" = "agua utilizada"); **valores sin cambio** | — (vigilancia) |
| **T-12** | Test T08 de `modelo_capacidad_proceso.py` depende de `git status` | 05 ↔ 03/04/07/23 | Falla si hay `__pycache__/` sin versionar o cambios sin commitear en `23_plan_expansion/` (p. ej., editar su README). Se agregó `.gitignore` para `__pycache__`; el test **no** se modificó | Rediseño opcional del test en una sesión técnica |
| **T-13** | URL duplicada **preexistente** | 25 | FTE-001 y FTE-071 apuntan al mismo Anuario Avícola 2025 (SAGyP) con datos distintos; no se fusionaron para no renumerar referencias de módulos cerrados | Consolidación en una sesión de mantenimiento |
| **T-14** | Integración pendiente del HTML | HTML ↔ 09A/09C | v0.1 no muestra ecuación de 24 h, utilities, gates ni localización | Versiones v0.5 / v1.0 |

Consistencias verificadas (no son tensiones): t/día a congelar de 09A = capacidad de congelación de 09C (p. ej., 24 t/día con P3 a 20.000 aves/día); ritmos de 09A = `escenarios_escala.csv` (test T01); inventario de 09C = modelo de escala (test U07); frozen P1–P3 de 09C = SUP-055.

## 10. Dependencias entre módulos

| De → a | Qué debe fluir | Estado |
|---|---|---|
| **09A → 09C** | Cada equipo futuro (EQ-01 a EQ-76 y los que resulten del RFQ) debe alimentar: **potencia** (kW nominal, factor de carga, horas, simultaneidad, arranque, cos φ), **agua** (L/h, calidad, temperatura), **aire comprimido**, **vapor/calor**, **frío** (kWf y temperatura) y efluente | Tabla definida (`11_agua_efluentes/conclusiones_agua_efluentes.md` §5) sin datos; DPV-095, DEC-048, SUP-077 |
| **09B → layout (`09`)** | La normativa condiciona **flujos** (sucio/limpio, personas, producto, subproductos, decomisos), **zonas**, **materiales** sanitarios, **inspección** (puestos, iluminación, oficina y sala del SIV), **cámaras** (temperaturas) y **servicios** (agua potable, agua caliente, esterilizadores, vestuarios, desagües) | Requisitos `[PVDP]` en `16_normativa_senasa/requisitos_sanitarios.md` y zonificación en `05_proceso_industrial/zonificacion_higienica.md`; falta texto del reglamento (DPV-090) y revisión del anteproyecto (DPV-115) |
| **09C → localización (`10`)** | Cada zona candidata debe poder proveer: **agua** (caudal horario, calidad, permiso), **descarga** (cuerpo receptor, límites de vuelco, permiso), **electricidad** (potencia disponible y ampliable, calidad de red), **combustible** (gas natural/GLP), **terreno suficiente** (planta, tratamiento de efluentes, reserva de expansión, distancia a viviendas) | Preguntas en `12_energia_frio/conclusiones_energia_frio.md` §6 y `11_agua_efluentes/guia_ramiro.md` §10; DPV-052, DPV-053, DPV-087, DPV-106; DEC-003, DEC-043 |
| **09B → localización** | Plantilla jurisdiccional de 14 temas por candidata | `16_normativa_senasa/habilitacion_planta.md` §5; DPV-106 |
| **09A → RR. HH. (`18`)** | Puestos equivalentes (no dotación) y productividad | SUP-063, DPV-092 |
| **09A/09B/09C → CAPEX/OPEX (`19`, `20`)** | Lista de equipos, requisitos edilicios, tratamiento, frío, respaldo, tasas SENASA | RFQ no enviado; DPV-101, DPV-095 |
| **HTML** | Deberá incorporar más adelante: **utilities** (09C), capacidad de proceso y ecuación de 24 h (09A), **ubicación**, **CAPEX**, **OPEX** y **finanzas** (v1.0), gates (v0.5) | `23_plan_expansion/simulador_html/README.md` §9 |

## 11. Pendientes de trabajo de campo

1. **Demanda:** compras, mix y condiciones de la red y otros canales; carta de intención (DPV-002, 003, 020, 037, 038, 040).
2. **Plantas en operación (visitas):** capacidad real vs nominal, disponibilidad, microparadas (DPV-088); limpieza, sanitización y mantenimiento (DPV-091); productividad (DPV-092); enfriamiento (DPV-062); energía, agua y efluentes reales (DPV-108, DPV-113, DPV-114, DPV-067); decomisos (DPV-063); ensayo de balance (DPV-060).
3. **Proveedores (cuando la fase lo habilite):** definición contractual de capacidad y velocidad garantizada (DPV-097), servicio técnico y repuestos (DPV-089), lista de cargas y servicios por equipo (DPV-095), balance frigorífico (DPV-109), tiempos de congelado (DPV-096). Avícola y Porcinos 2026 (Buenos Aires, 6–8 nov 2026) como oportunidad de relevamiento.
4. **SENASA / asesor:** reunión técnica (DEC-042) con las 7 preguntas prioritarias (P-39 a P-45): Decreto 697/2026 (DPV-107), Ley 22.375 (DPV-099), Res. 233/2026 (DPV-100), APPCC (DPV-102), plazos reales (DPV-086), revisión de anteproyecto (DPV-115), dotación y tasas del SIV (DPV-101).
5. **Sitios candidatos (cuando se inicie localización):** agua, vuelco, potencia, gas, calidad de red, terreno y normativa local (DPV-052, 053, 087, 106).
6. **Documental:** lectura primaria del Decreto 4238/68 y resoluciones (DPV-090, DPV-098, DPV-105) y reproducción de las lecturas confirmadas en revisión externa (FTE-194, FTE-197, FTE-200, FTE-251) cuando el entorno tenga acceso o mediante descarga manual (DPV-009).
7. **Carnicería familiar:** habilitación actual y ventas (DPV-104, DPV-004).

## 12. Estado final de los tests

Ejecutados el 2026-09-30 **después** del commit de integración (el test T08 de proceso exige árbol limpio en `03`, `04`, `07` y `23`). Ningún modelo físico se modificó en su lógica: en `modelo_capacidad_proceso.py` y `modelo_utilities.py` solo cambiaron IDs en comentarios y textos de salida; al regenerar, `capacidad_proceso.csv` y `escenarios_utilities.csv` resultaron **idénticos byte a byte** al reemplazo textual.

| Suite | Comando | Resultado |
|---|---|---|
| Producción primaria | `03_produccion_primaria/modelo_escenarios_produccion.py` (pruebas) | 10/10 grupos OK |
| Balance de masa | `04_balance_masa/modelo_balance_masa.py --solo-tests` | **21/21** |
| Subproductos | `07_subproductos/modelo_subproductos.py --solo-tests` | **9/9** |
| Escala | `23_plan_expansion/modelo_escala.py --solo-tests` / `--mutaciones` | **23/23**; mutaciones **22/22** detectadas |
| Proceso | `05_proceso_industrial/modelo_capacidad_proceso.py --solo-tests` / `--mutaciones` | **18/18**; mutaciones **9/9** detectadas |
| Utilities | `11_agua_efluentes/modelo_utilities.py --solo-tests` / `--mutaciones` | **30/30**; mutaciones **20/20** detectadas |
| HTML (modelos ↔ simulador) | `node 23_plan_expansion/simulador_html/validar_simulador.js` | **20/20** |
| HTML (navegador, `file://`, red bloqueada) | `pruebas/prueba_navegador.js` | **16/16**; autoverificación 784/784 |

Nota: en la línea base (antes de integrar) T08 falló solo porque las corridas de otros modelos habían dejado `__pycache__/` sin versionar (tensión T-12); se agregó `.gitignore` y se corrió con `PYTHONDONTWRITEBYTECODE=1`.

## 13. Control de integridad

Script de control (reproducible, ejecutado tras la integración):

| Control | Resultado | Detalle |
|---|---|---|
| IDs SUP únicos | OK | 77 IDs (SUP-001–SUP-077); duplicados []; huecos [] |
| IDs DPV únicos | OK | 115 IDs (DPV-001–DPV-115); duplicados []; huecos [] |
| IDs DEC únicos | OK | 49 IDs (DEC-001–DEC-049); duplicados []; huecos [] |
| IDs FTE únicos | OK | 268 fuentes; duplicados [] |
| Fuentes únicas (URL) | OK | URLs repetidas: 1 (preexistente FTE-001/FTE-071, T-13) |
| Referencias SUP/DPV/DEC/FTE existentes | OK | todas definidas |
| Sin IDs provisionales activos | OK | solo en archivos históricos y en el mapa de reconciliación |
| Enlaces relativos válidos | OK | todos resuelven |
| Sin marcadores de merge | OK | ninguno |
| CSV válidos | OK | 14 CSV, columnas constantes |
| Sin 'no existe' desactualizados | OK | ninguno |

## 14. Archivos modificados

- `.gitignore` — creado
- `00_gestion_proyecto/datos_por_validar.md` — modificado
- `00_gestion_proyecto/decisiones_pendientes.md` — modificado
- `00_gestion_proyecto/estado_proyecto.md` — modificado
- `00_gestion_proyecto/glosario.md` — modificado
- `00_gestion_proyecto/reconciliacion_sesiones_09.md` — creado
- `00_gestion_proyecto/supuestos.md` — modificado
- `05_proceso_industrial/README.md` — modificado
- `05_proceso_industrial/actualizaciones_gestion_09A.md` — modificado
- `05_proceso_industrial/arquitecturas_por_escala.md` — modificado
- `05_proceso_industrial/capacidad_proceso.csv` — modificado
- `05_proceso_industrial/conclusiones_proceso.md` — modificado
- `05_proceso_industrial/cuellos_botella.md` — modificado
- `05_proceso_industrial/flujo_proceso.md` — modificado
- `05_proceso_industrial/modelo_capacidad_proceso.py` — modificado
- `05_proceso_industrial/zonificacion_higienica.md` — modificado
- `08_maquinaria/README.md` — modificado
- `08_maquinaria/automatizacion_por_escala.md` — modificado
- `08_maquinaria/catalogo_equipos.md` — modificado
- `08_maquinaria/fuentes_09A.csv` — retirado
- `08_maquinaria/matriz_equipos.csv` — modificado
- `08_maquinaria/proveedores_preliminares.md` — modificado
- `08_maquinaria/requerimientos_cotizacion.md` — modificado
- `11_agua_efluentes/README.md` — modificado
- `11_agua_efluentes/actualizaciones_gestion_09C.md` — modificado
- `11_agua_efluentes/alternativas_tratamiento.md` — modificado
- `11_agua_efluentes/balance_agua.md` — modificado
- `11_agua_efluentes/caracterizacion_efluentes.md` — modificado
- `11_agua_efluentes/conclusiones_agua_efluentes.md` — modificado
- `11_agua_efluentes/escenarios_utilities.csv` — modificado
- `11_agua_efluentes/fuentes_09C.csv` — retirado
- `11_agua_efluentes/modelo_utilities.py` — modificado
- `12_energia_frio/conclusiones_energia_frio.md` — modificado
- `12_energia_frio/congelado_almacenamiento.md` — modificado
- `12_energia_frio/demanda_energia.md` — modificado
- `12_energia_frio/respaldo_energia.md` — modificado
- `12_energia_frio/sistema_frio.md` — modificado
- `16_normativa_senasa/README.md` — modificado
- `16_normativa_senasa/actualizaciones_gestion_09B.md` — modificado
- `16_normativa_senasa/conclusiones_normativa.md` — modificado
- `16_normativa_senasa/exportacion_y_certificaciones.md` — modificado
- `16_normativa_senasa/fuentes_09B.csv` — retirado
- `16_normativa_senasa/habilitacion_planta.md` — modificado
- `16_normativa_senasa/mapa_regulatorio.md` — modificado
- `16_normativa_senasa/matriz_regulatoria.csv` — modificado
- `16_normativa_senasa/preguntas_senasa.md` — modificado
- `16_normativa_senasa/requisitos_sanitarios.md` — modificado
- `16_normativa_senasa/ruta_critica_habilitacion.md` — modificado
- `16_normativa_senasa/subproductos_normativa.md` — modificado
- `17_exportacion/requisitos_planta_exportadora.md` — modificado
- `23_plan_expansion/README.md` — modificado
- `23_plan_expansion/conclusiones_escala.md` — modificado
- `23_plan_expansion/escenarios_escala.md` — modificado
- `23_plan_expansion/especificacion_simulador_html.md` — modificado
- `23_plan_expansion/gates_expansion.md` — modificado
- `23_plan_expansion/simulador_html/README.md` — modificado
- `23_plan_expansion/simulador_html/observaciones_html_v01.md` — modificado
- `25_fuentes/bibliografia.md` — modificado
- `25_fuentes/registro_fuentes.csv` — modificado

Total: 59 archivos (2 creados, 3 retirados, 54 modificados).
