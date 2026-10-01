# Actualizaciones de gestión pendientes de reconciliación — sesión 14A (RR. HH. y organización)

**Fecha:** 2026-10-01 · Sesión ejecutada **en paralelo** con 14B.

> **Por qué existe este archivo:** por instrucción del promotor, esta sesión **no modificó** `00_gestion_proyecto/` ni `25_fuentes/`, ni archivos de 14B. Lo que normalmente se registraría en `supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `estado_proyecto.md` y `registro_fuentes.csv` se propone aquí con **IDs provisionales** (`SUP-14A-##`, `DPV-14A-##`, `DEC-14A-##`, `FTE-14A-###`) para la reconciliación.
> Últimos IDs vistos en los registros centrales al iniciar la sesión: **SUP-123, DPV-145, DEC-066, FTE-297**.
> Fuentes provisionales: [`fuentes_14A.csv`](fuentes_14A.csv) (mismas columnas que `25_fuentes/registro_fuentes.csv`).
> **Posibles solapamientos con 14B** a revisar en la reconciliación: cualquier registro de 14B sobre costos laborales, OPEX o CAPEX de vestuarios/oficinas debe usar la dotación de este módulo (sin costos) y no un proxy propio.

---

## 1. Supuestos nuevos → `00_gestion_proyecto/supuestos.md`

| ID provisional | Supuesto | Ámbito | Estado |
|---|---|---|---|
| SUP-14A-01 | **Clasificación de la dotación:** directos = operación industrial de recepción a expedición y subproductos; supervisión = supervisores, jefes de turno y de producción, supervisor de saneamiento; soporte = limpieza y sanitización, calidad, mantenimiento, logística, producción primaria (sólo coordinación), HyS, lavandería; indirectos = todo lo que no es directo. Personal de granjas de terceros **no** se cuenta | RR. HH. | Vigente |
| SUP-14A-02 | **[SUPUESTO DE SENSIBILIDAD]** **Jornada:** jornada normal 8 h `[PVDP]` (FTE-14A-001); turno extendido con tope de trabajo de 10 h; traspaso entre cuadrillas 0,25 h; presencia de la cuadrilla de línea = h_c/D + pausas + limpieza intermedia (D, pausas y limpieza intermedia de SUP-061/SUP-062); tope de referencia de horas extra 30 h/mes `[PVDP]` (FTE-14A-002) usado sólo como alerta | RR. HH. / proceso | Vigente |
| SUP-14A-03 | **[SUPUESTO DE SENSIBILIDAD]** **Factor de cobertura** (ausentismo + vacaciones + licencias) 1,08 / 1,12 / 1,18; **horas normales semanales** 48 / 45 / 44 (ley vs convenio por confirmar) | RR. HH. | Vigente |
| SUP-14A-04 | **[SUPUESTO DE SENSIBILIDAD — sin dato argentino]** **Puestos por 1.000 aves/h por área y nivel** (alta / media / baja): colgado 0,72 / 1,0 / 1,45 (FTE-219 `[PVDP · débil]`, prudente SUP-063); descarga M 0,6 / 0,8 / 1,0 · S 0,4 / 0,5 / 0,7 · A 0,2 / 0,3 / 0,4; faena M 1,6 / 2,2 / 3,0 · Mc 1,2 / 1,6 / 2,2 · S 0,6 / 0,9 / 1,3 · A 0,2 / 0,5 / 0,8; evisceración M 9,8 / 13,6 / 20,1 (FTE-218 `[PVDP · débil]` + menudencias) · S 4 / 6 / 9 · A 1,0 / 2,2 / 3,5; clasificación M 1,0 / 1,5 / 2,0 · S 0,5 / 0,8 / 1,0 · A 0,2 / 0,3 / 0,5; limpieza operativa 0,3 / 0,5 / 0,8; más 1 puesto fijo por área (2 en evisceración automática). Todo redondeado hacia arriba por área | RR. HH. / proceso | Vigente |
| SUP-14A-05 | **[SUPUESTO DE SENSIBILIDAD — sin fuente]** **Productividades por masa:** trozado M 250 / 180 / 120 · Mc 300 / 220 / 150 · S 450 / 320 / 220 · A 1.500 / 800 / 500 kg/persona-h; deshuese M 70 / 50 / 35 · S 100 / 75 / 55 · A 350 / 250 / 180; empaque M 350 / 250 / 170 · Mc 450 / 330 / 230 · S 700 / 500 / 350 · A 2.000 / 1.100 / 700; cámaras 25 / 18 / 12 t por persona-turno; subproductos M 6 / 4 / 3 · S 8 / 6 / 4 · A 15 / 10 / 8 t por persona-turno (kg/ave del balance v1.1 vía 09A) | RR. HH. | Vigente |
| SUP-14A-06 | **[SUPUESTO DE SENSIBILIDAD]** **Limpieza post-producción:** m² de proceso de 12C (bajo / medio / alto) × factor de automatización 1,0 / 1,0 / 1,1 / 1,25 ÷ 60 / 40 / 25 m²/persona-h ÷ ventana (limpieza + sanitización de SUP-062); esquema híbrido = 30 % interno; supervisor de saneamiento interno en toda modalidad | RR. HH. / limpieza | Vigente |
| SUP-14A-07 | **Supervisión:** 1 supervisor de línea cada 30 / 22 / 15 directos por cuadrilla (mínimo 1); jefe de turno por cuadrilla sólo con 2 cuadrillas; jefe de producción desde 10.000 aves/día | RR. HH. | Vigente |
| SUP-14A-08 | **Control de calidad operativo:** 1 + 0,6 / 0,8 / 1,2 puestos por 1.000 aves/h por cuadrilla; estructura de QA por banda de escala (§ estructura) | Calidad | Vigente |
| SUP-14A-09 | **[SUPUESTO DE SENSIBILIDAD]** **Mantenimiento:** técnicos = max(cobertura presencial, carga por activos); h/semana por equipo M 0 · Mc 0,5 / 0,75 / 1,5 · S 0,75 / 1,5 / 3 · A 1,5 / 3 / 6; peso por criticidad 1,5 / 1 / 0,5; equipos "Duplicar" = 1 unidad cada 1.250 aves/h; 36 / 32 / 28 h productivas por técnico; técnicos simultáneos en producción 1 / 2 / 3 / 4 según escala y automatización; 1 de guardia fuera de producción. Activos de `08_maquinaria/matriz_equipos.csv` | Mantenimiento | Vigente |
| SUP-14A-10 | **Producción primaria (sólo coordinación):** técnicos de campo 1 cada 20 / 15 / 10 granjas equivalentes de 30.000 plazas (12B/03); coordinador, veterinario y planificación por banda de escala; sin personal de granjas | Producción primaria | Vigente |
| SUP-14A-11 | **Choferes:** sólo con flota propia; aves vivas = flota mínima de 12B con capacidad de **escenario** 5.500 aves/camión (SUP-033) y radio 100 km × factor de cobertura; producto terminado PENDIENTE salvo capacidad y distancia explícitas | Logística | Vigente |
| SUP-14A-12 | **RR. HH.:** 1 persona cada 150 / 120 / 90 personas internas (mínimo 0,5) | Administración | Vigente |
| SUP-14A-13 | **Estructura por banda** (S < 4.000 · M < 8.000 · L < 15.000 · XL ≥ 15.000 aves/día): tabla de roles de estructura de `modelo_rrhh.py` (dirección, jefaturas, QA, logística, administración); las fracciones se suman por bloque y se redondean una vez ("roles compartidos") | Organización | Vigente |
| SUP-14A-14 | **Automatización por área:** los cuatro escenarios (manual / mecanizado / semiautomático / automático) se traducen a M / Mc / S / A por área; aturdido–desplumado continuo Mc/A en todos los casos (arquitectura de referencia de 09A); para mantenimiento, cada equipo toma la opción de la matriz más cercana por debajo del objetivo | RR. HH. / maquinaria | Vigente |
| SUP-14A-15 | **Escenario de referencia de documentación** (no decisión): 1 cuadrilla, 8 h netas en turno extendido, automatización de referencia de 09A por escala, config. B, limpieza y mantenimiento propios, flota de aves de terceros, integración, laboratorio externo, 5 días | RR. HH. | Vigente |

**Notas a supuestos existentes:**

- **SUP-053** (horas netas 6 / 8 / 10 / 16; 16 = 2 × 8): agregar "14A: con jornada de 8 h `[PVDP]` y las sensibilidades de SUP-061/062, 8 h netas implican ~10 h de presencia (turno extendido, ~43 h extra/persona-mes) y dos cuadrillas sin horas extra dan ~11,4–13,5 h netas, no 16 (`18_recursos_humanos/turnos_y_productividad.md` §2)".
- **SUP-063** (productividades manuales): agregar "14A: usadas como extremo alto (referencia) y bajo (prudente) de los rangos de colgado y eviscerado; el valor medio es un supuesto intermedio (SUP-14A-04)".
- **SUP-116** (proxy de dotación de 12C): agregar "14A: el modelo de dotación da 31 / 41 / 47 / 51 personas por turno de producción (referencia media) vs 49 / 82 / 115 / 165 del proxy; para vestuarios usar máximo simultáneo por zona y sexo (`dotacion_por_escala.md` §5). Reemplazo a decidir en la reconciliación".

## 2. Datos por validar nuevos → `00_gestion_proyecto/datos_por_validar.md`

| ID provisional | Dato | Para qué | Fuente esperada | Prioridad (nivel del plan de campo) |
|---|---|---|---|---|
| DPV-14A-01 | **Convenio colectivo aplicable** a faena y procesamiento avícola en cada corredor: jornada, turnos, horas extra, nocturnidad, sábados, categorías, adicionales | Alertas de jornada y horas extra; costo laboral; viabilidad del segundo turno | Sindicato, cámara, plantas, asesor laboral (FTE-14A-006) | IMPORTANTE ANTES DE DISEÑAR (N2). Complementa DPV-082 |
| DPV-14A-02 | **Ausentismo, rotación, vacaciones y licencias** reales en plantas avícolas | Factor de cobertura (SUP-14A-03) | Visitas; consultoras de RR. HH. | ÚTIL PARA OPTIMIZAR (N3) |
| DPV-14A-03 | **Costo laboral por categoría** (salario de convenio, cargas sociales, ART, adicionales, ropa, comedor, transporte), con tipo de cambio, fecha y fuente | Completar `plantilla_costo_laboral.csv`; OPEX (`20_opex`) | Convenio, estudio contable, plantas | IMPORTANTE ANTES DE INVERTIR (N2) |
| DPV-14A-04 | **Productividad real por área:** colgado, faena, evisceración por nivel de automatización, trozado, deshuese, empaque, cámaras, subproductos | Reemplazar SUP-14A-04/05 | Visitas; ensayo en planta (DEC-028) | IMPORTANTE ANTES DE DISEÑAR (N2). Complementa DPV-092 |
| DPV-14A-05 | **Inspección oficial:** inspectores y auxiliares por línea y turno; si la empresa aporta auxiliares, espacios o aranceles | Dotación y costo de la función oficial (hoy PENDIENTE) | SENASA; plantas | IMPORTANTE ANTES DE DISEÑAR (N2). Complementa DPV-090 y DPV-140 |
| DPV-14A-06 | **Organización real de la limpieza:** dotación, duración, por sectores o en bloque, jornada completa o parcial, propia o tercerizada, quién desarma equipos | Cuadrilla de limpieza (el bloque más incierto) | Visitas; empresas de limpieza industrial | IMPORTANTE ANTES DE DISEÑAR (N2). Complementa DPV-091 |
| DPV-14A-07 | **Horas mínimas de los servicios de higiene y seguridad y de medicina del trabajo** por cantidad de trabajadores y riesgo | Servicio externo de HyS (hoy PENDIENTE) | Ley 19.587, Decretos 351/79 y 1338/96 (FTE-14A-004); asesor de HyS | ÚTIL PARA OPTIMIZAR (N3) |
| DPV-14A-08 | **Disponibilidad de técnicos** (mecánicos, electricistas, frigoristas con amoníaco, PLC) y de operarios con experiencia frigorífica por corredor; tiempo de formación | Viabilidad de automatización y de mantenimiento propio | Plantas, escuelas técnicas, municipios | IMPORTANTE ANTES DE INVERTIR (N2). Complementa DPV-121 |
| DPV-14A-09 | **Cuadrillas de captura:** quién las provee (integrado, contratista, empresa) y su dotación | Logística de aves vivas (hoy PENDIENTE) | Integradores, contratistas | ÚTIL PARA OPTIMIZAR (N3) |
| DPV-14A-10 | **Mantenimiento real:** técnicos por especialidad, horas de preventivo, cobertura en turno, qué se terceriza | Reemplazar SUP-14A-09 | Visitas; proveedores de equipos | IMPORTANTE ANTES DE DISEÑAR (N2). Complementa DPV-089 |
| DPV-14A-11 | **Supervisión real:** operarios por supervisor, jefes de turno, origen de los supervisores | SUP-14A-07 | Visitas | ÚTIL PARA OPTIMIZAR (N3) |
| DPV-14A-12 | **Requisitos de personal para exportación:** responsable de bienestar animal (UE, FTE-14A-007), certificados de competencia, personal Halal, auditorías | Estructura de calidad del nivel escalado | SENASA; importadores; certificadoras | ÚTIL PARA OPTIMIZAR (N3). Complementa DPV-034 |

## 3. Decisiones pendientes nuevas → `00_gestion_proyecto/decisiones_pendientes.md`

| ID provisional | Decisión | Opciones | Insumos | Relacionada con |
|---|---|---|---|---|
| DEC-14A-01 | **Modalidad de limpieza y sanitización** | Propia / tercerizada / híbrida (siempre con supervisión y verificación POES internas) | DPV-14A-06, DPV-091, costo laboral y de contratistas | DEC-036, DEC-043 (químicos y efluentes) |
| DEC-14A-02 | **Modalidad de mantenimiento** | Propio / tercerizado / mixto (cobertura propia + especialistas) | DPV-14A-10, DPV-14A-08, DPV-089 | DEC-040, DEC-037, DEC-046 |
| DEC-14A-03 | **Organización de la jornada de producción** | 1 cuadrilla en jornada normal (~6–7 h netas) / turno extendido con horas extra / 2 cuadrillas / cuadrillas solapadas / 6 días | DPV-082, DPV-14A-01, DPV-091 | Sub-decisión de DEC-036; DEC-033 |
| DEC-14A-04 | **Estructura de dirección inicial** y momento de incorporación de cada gerencia | Roles combinados (GG + comercial + adm.) / gerencias separadas desde el inicio | Escala y modelo (DEC-004, DEC-018), costo laboral | DEC-008 |
| DEC-14A-05 | **Polivalencia y rotación** entre puestos y zonas | Polivalencia dentro de cada zona / rotación entre zonas con circuito de cambio / especialización | Zonificación higiénica (09A), ergonomía, ausentismo | DEC-012 |
| DEC-14A-06 | **Higiene y seguridad laboral y medicina del trabajo** | Servicio externo / interno / mixto | DPV-14A-07 | — |
| DEC-14A-07 | **Lavandería y ropería** | Propia / tercerizada | Costo, superficie (12C), logística de ropa por zona | DEC-062 |

**Notas a decisiones existentes:** DEC-036 y DEC-037 (agregar los hallazgos de jornada y automatización de `turnos_y_productividad.md`); DEC-056 (choferes de aves calculables sólo con capacidad de escenario; producto PENDIENTE); DEC-065 (laboratorio propio: +1 / +1 / +2 / +3 personas).

## 4. Tensiones abiertas (no resueltas por esta sesión)

| # | Tensión | Módulos | Propuesta para la reconciliación |
|---|---|---|---|
| T-14A-1 | "8 h netas" (SUP-053, referencia de 23/05/12B) implica ~10 h de presencia por persona: es turno extendido con ~43 h extra/mes, no un turno de 8 h | 23, 05, 12B, 18 | Mantener 8 h netas como sensibilidad de capacidad, pero etiquetar "requiere turno extendido u organización solapada" |
| T-14A-2 | "16 h = 2 × 8 h netas" choca con la jornada (presencia 10,2 h) y con la ecuación de 24 h; dos cuadrillas sin horas extra dan ~11,4–13,5 h | 23, 05, 18 | Agregar a DEC-036 una variante de 12 h netas (2 × 6) |
| T-14A-3 | Proxy de dotación de 12C (SUP-116) 1,6–3,2 veces la dotación por turno de este modelo | 09, 18 | Recalcular vestuarios y comedor con máximo simultáneo por zona y sexo cuando 12C se actualice |
| T-14A-4 | La cuadrilla de limpieza en ventana de ~4 h produce muchas personas con pocas horas (personas ≫ equivalentes) | 05, 18 | Validar limpieza por sectores en visitas (DPV-14A-06) antes de usar personas físicas en OPEX |

## 5. Fuentes → `25_fuentes/registro_fuentes.csv`

Siete fuentes provisionales en [`fuentes_14A.csv`](fuentes_14A.csv) (FTE-14A-001 a FTE-14A-007), **todas `[PVDP]`** (ninguna leída en original). Además se usaron, sin cambios, FTE-200, FTE-218, FTE-219, FTE-229 y FTE-287 del registro central.

## 6. Propuesta de fila del tablero → `00_gestion_proyecto/estado_proyecto.md`

| Módulo | Modelo preliminar | Evidencia de campo | Síntesis |
|---|---|---|---|
| Recursos humanos y organización (`18`) | **MODELO PRELIMINAR COMPLETADO** v1.0 (estructura funcional, organigramas en tres niveles, dotación por escala y por zona, tres modos de turno integrados a la ecuación de 24 h y a la jornada, KPI múltiples, automatización, mantenimiento propio/tercerizado/mixto, limpieza propia/tercerizada/híbrida, calidad e inocuidad; `modelo_rrhh.py` con 15 tests y 8/8 mutaciones; 15.576 escenarios; plantilla de costo laboral **vacía**). **OPEX laboral = PENDIENTE**; sin escala ni modalidades elegidas | Pendiente — dotación real, productividad, convenio, ausentismo, limpieza, mantenimiento, inspección oficial | [`conclusiones_rrhh.md`](conclusiones_rrhh.md) |

Hito propuesto: *2026-10-01 — Recursos humanos y organización (`18_recursos_humanos`; sesión 14A, en paralelo con 14B) — Modelo preliminar completado v1.0; evidencia de campo pendiente; costos no calculados.*
