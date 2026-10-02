# Reconciliación de las sesiones paralelas 14A y 14B — RR. HH., organización y upstream

**Fecha:** 2026-10-02 · **Tipo:** sesión administrativa de integración (no investiga temas nuevos) · **Rama:** `claude/laughing-wright-fu8rtg` (desde `main` actualizado, commit `dda7ba7`)

> **Qué hace este documento:** registra cómo se integraron en los registros maestros (`supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `glosario.md`, `estado_proyecto.md`, `matriz_validacion_campo.csv`, `plan_trabajo_campo.md`, `25_fuentes/`) los resultados de dos sesiones que trabajaron en paralelo con IDs provisionales: **14A Recursos humanos y organización** (`18_recursos_humanos/`) y **14B Integración upstream** (`14_alimento_balanceado/` + `15_incubacion/`).
> **No** se tomó ninguna decisión; **no** se eligió escala, arquitectura de integración, modalidad de limpieza o mantenimiento, organización de turnos, planta de alimento propia ni incubación propia; **no** se cargaron precios ni salarios; **no** se inició CAPEX ni OPEX; **no** se modificó la lógica matemática de `modelo_rrhh.py` ni de `modelo_upstream.py` (solo IDs en comentarios, textos y etiquetas; los CSV regenerados son **idénticos byte a byte** al reemplazo textual de IDs sobre `HEAD`, §13); **no** se resolvieron contradicciones (§9) ni se transformaron supuestos en hechos.

---

## 1. Objetivo

1. Consolidar los registros globales con las propuestas de 14A y 14B.
2. Eliminar los IDs provisionales activos (`SUP-14A-##`, `DPV-14B-##`, `DEC-14A-##`, `FTE-14B-###`, `T-14A-#`).
3. Reconciliar dependencias con módulos anteriores (03, 05/09A, 09C/11–12, 09/12C, 13/12B, 23).
4. Registrar contradicciones y tensiones sin resolverlas.
5. Dejar el proyecto preparado para CAPEX y, después, OPEX (§10–11), **sin calcularlos**.

| Sesión | Alcance | Carpeta | IDs provisionales | Estado tras la reconciliación |
|---|---|---|---|---|
| **14A** | RR. HH. y organización v1.1 (auditoría de unidades laborales) | `18_recursos_humanos` | SUP-14A-01…18, DPV-14A-01…12, DEC-14A-01…07, FTE-14A-001…007, T-14A-1…4 | Integrada. `actualizaciones_gestion_14A.md` y `fuentes_14A.csv` quedan como **archivos históricos** |
| **14B** | Upstream v1.1 (auditoría de sincronización productiva e inventarios) | `14_alimento_balanceado`, `15_incubacion` | SUP-14B-01…15, DPV-14B-01…10, DEC-14B-01…07, FTE-14B-001…005 | Integrada. `actualizaciones_gestion_14B.md` y `fuentes_14B.csv` históricos |

Últimos IDs oficiales al iniciar: **SUP-123, DPV-145, DEC-066, FTE-297** (coinciden con los declarados por ambas sesiones; ninguna tomó números en paralelo).

## 2. IDs consolidados (mapa provisional → definitivo)

Todos los IDs provisionales se reemplazaron en `18_recursos_humanos/`, `14_alimento_balanceado/` y `15_incubacion/` (documentos, comentarios y etiquetas de `modelo_rrhh.py` y `modelo_upstream.py`, y CSV de salida regenerados). Las formas abreviadas se convirtieron con la convención del registro (p. ej. `SUP-14A-04/05` → `SUP-127/128`). Solo permanecen, como historia, en los dos `actualizaciones_gestion_14*.md` (marcados **ARCHIVO HISTÓRICO**), en los dos `fuentes_14*.csv` históricos y en este documento. Las tensiones `T-14A-1…4` pasan a `T14-02`, `T14-03`, `T14-01` y `T14-11` (§9).

### 2.1 Supuestos (33 provisionales → 31 nuevos + 2 consolidaciones)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| SUP-14A-01 | **SUP-124** | Alta nueva |
| SUP-14A-02 | **SUP-125** | Alta nueva |
| SUP-14A-03 | **SUP-126** | Alta nueva |
| SUP-14A-04 | **SUP-127** | Alta nueva |
| SUP-14A-05 | **SUP-128** | Alta nueva |
| SUP-14A-06 | **SUP-129** | Alta nueva |
| SUP-14A-07 | **SUP-130** | Alta nueva |
| SUP-14A-08 | **SUP-131** | Alta nueva |
| SUP-14A-09 | **SUP-132** | Alta nueva |
| SUP-14A-10 | **SUP-133** | Alta nueva |
| SUP-14A-11 | **SUP-134** | Alta nueva |
| SUP-14A-12 | **SUP-135** | Alta nueva |
| SUP-14A-13 | **SUP-136** | Alta nueva |
| SUP-14A-14 | **SUP-137** | Alta nueva |
| SUP-14A-15 | **SUP-138** | Alta nueva |
| SUP-14A-16 | **SUP-139** | Alta nueva |
| SUP-14A-17 | **SUP-140** | Alta nueva |
| SUP-14A-18 | **SUP-141** | Alta nueva |
| SUP-14B-01 | **SUP-142** | Alta nueva |
| SUP-14B-02 | **SUP-143** | Alta nueva |
| SUP-14B-03 | **SUP-144** | Alta nueva |
| SUP-14B-04 | **SUP-145** | Alta nueva |
| SUP-14B-05 | **SUP-146** | Alta nueva |
| SUP-14B-06 | **SUP-147** | Alta nueva |
| SUP-14B-07 | **SUP-148** | Alta nueva |
| SUP-14B-08 | **SUP-032** | Consolidado en SUP-032 (categorías de materias primas como rangos; el 60 / 30 sigue ilustrativo) |
| SUP-14B-09 | **SUP-149** | Alta nueva |
| SUP-14B-10 | **SUP-150** | Alta nueva |
| SUP-14B-11 | **SUP-151** | Alta nueva |
| SUP-14B-12 | **SUP-152** | Alta nueva |
| SUP-14B-13 | **SUP-096** | Consolidado en SUP-096 (granelero de grano 25 / 28 / 30 t de escenario) |
| SUP-14B-14 | **SUP-153** | Alta nueva |
| SUP-14B-15 | **SUP-154** | Alta nueva |

### 2.2 Datos por validar (22 provisionales → 14 nuevos + 8 consolidaciones)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DPV-14A-01 | **DPV-146** | Alta nueva |
| DPV-14A-02 | **DPV-147** | Alta nueva |
| DPV-14A-03 | **DPV-148** | Alta nueva |
| DPV-14A-04 | **DPV-092** | Consolidado en DPV-092 (productividad real por área y automatización) |
| DPV-14A-05 | **DPV-101** | Consolidado en DPV-101 (inspección oficial: dotación, auxiliares, tasas) |
| DPV-14A-06 | **DPV-091** | Consolidado en DPV-091 (organización real de la limpieza) |
| DPV-14A-07 | **DPV-149** | Alta nueva |
| DPV-14A-08 | **DPV-121** | Consolidado en DPV-121 (disponibilidad de técnicos por corredor) |
| DPV-14A-09 | **DPV-054** | Consolidado en DPV-054 (cuadrillas de captura) |
| DPV-14A-10 | **DPV-150** | Alta nueva |
| DPV-14A-11 | **DPV-151** | Alta nueva |
| DPV-14A-12 | **DPV-152** | Alta nueva |
| DPV-14B-01 | **DPV-153** | Alta nueva |
| DPV-14B-02 | **DPV-154** | Alta nueva |
| DPV-14B-03 | **DPV-155** | Alta nueva |
| DPV-14B-04 | **DPV-156** | Alta nueva |
| DPV-14B-05 | **DPV-157** | Alta nueva |
| DPV-14B-06 | **DPV-007** | Consolidado en DPV-007 (habilitaciones de fábricas de alimento, incubación y reproductoras) |
| DPV-14B-07 | **DPV-158** | Alta nueva |
| DPV-14B-08 | **DPV-159** | Alta nueva |
| DPV-14B-09 | **DPV-047** | Consolidado en DPV-047 (camiones y horas nacimiento → granja; programación del proveedor) |
| DPV-14B-10 | **DPV-133** | Consolidado en DPV-133 (sincronización incubadora–granja–faena) |

### 2.3 Decisiones pendientes (14 provisionales → 12 nuevas + 2 consolidaciones; + 1 alta derivada)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DEC-14A-01 | **DEC-067** | Alta nueva |
| DEC-14A-02 | **DEC-068** | Alta nueva |
| DEC-14A-03 | **DEC-069** | Alta nueva |
| DEC-14A-04 | **DEC-070** | Alta nueva |
| DEC-14A-05 | **DEC-071** | Alta nueva |
| DEC-14A-06 | **DEC-072** | Alta nueva |
| DEC-14A-07 | **DEC-073** | Alta nueva |
| DEC-14B-01 | **DEC-074** | Alta nueva |
| DEC-14B-02 | **DEC-075** | Alta nueva |
| DEC-14B-03 | **DEC-076** | Alta nueva |
| DEC-14B-04 | **DEC-077** | Alta nueva |
| DEC-14B-05 | **DEC-078** | Alta nueva |
| DEC-14B-06 | **DEC-060** | Consolidada en DEC-060 (cadencia de nacimientos y unidad de colocación) |
| DEC-14B-07 | **DEC-024** | Consolidada en DEC-024 (variantes de façon B1 / B2) |
| — (sin ID provisional) | **DEC-079** | **Alta derivada de la reconciliación**: días de stock e inventario upstream y estrategia de silos (14B los declaró "decisiones de diseño y compra" en SUP-14B-10 sin registrarlos como decisión) |

### 2.4 Fuentes (12 provisionales → 12 nuevas)

| ID provisorio | ID definitivo | Fuente | Tratamiento |
|---|---|---|---|
| FTE-14A-001 | **FTE-298** | Ley 11.544 - Jornada de trabajo | Alta nueva `[PVDP]` |
| FTE-14A-002 | **FTE-299** | Decreto 484/2000 - Horas suplementarias | Alta nueva `[PVDP]` |
| FTE-14A-003 | **FTE-300** | Ley 20.744 - Régimen de Contrato de Trabajo | Alta nueva `[PVDP]` |
| FTE-14A-004 | **FTE-301** | Ley 19.587 de Higiene y Seguridad en el Trabajo; Decreto 351/79; Decre | Alta nueva `[PVDP]` |
| FTE-14A-005 | **FTE-302** | Ley 24.557 de Riesgos del Trabajo | Alta nueva `[PVDP]` |
| FTE-14A-006 | **FTE-303** | Convenio colectivo de trabajo aplicable a la faena y procesamiento aví | Alta nueva `[PVDP]` |
| FTE-14A-007 | **FTE-304** | Reglamento (CE) 1099/2009 relativo a la protección de los animales en  | Alta nueva `[PVDP]` |
| FTE-14B-001 | **FTE-305** | Cobb Breeder Management Guide (egg storage; egg handling) y Cobb Hatch | Alta nueva `[PVDP]` |
| FTE-14B-002 | **FTE-306** | Vacunación en incubadora: in ovo en la transferencia (Marek; Gumboro)  | Alta nueva `[PVDP]` |
| FTE-14B-003 | **FTE-307** | Densidad aparente de ingredientes para alimentos balanceados (FAO Appe | Alta nueva `[PVDP]` |
| FTE-14B-004 | **FTE-308** | Planta de incubación de pollitos bebé (tesis/proyecto de grado) y refe | Alta nueva `[PVDP]` |
| FTE-14B-005 | **FTE-309** | Descripciones comerciales de plantas de alimento para aves (etapas de  | Alta nueva `[PVDP]` |

## 3. Supuestos

**31 nuevos (SUP-124 a SUP-154)**, todos `Vigente`, con marca explícita de su naturaleza. Ninguno se elevó a hecho. Se distinguen cuatro estatus en todo el registro:

| Estatus | Qué es | Ejemplos |
|---|---|---|
| **HECHO** | Dato con fuente verificada en original | **Ninguno** en 14A/14B |
| **PVDP** | Visto solo en extractos o referencias de conocimiento general | Jornada de 8 h (FTE-298), fertilidad 96,7 % / incubabilidad 93,5 % **en pico** (FTE-305), densidades (FTE-307) |
| **SUPUESTO / CRITERIO DE MODELO** | Hipótesis o regla de cálculo adoptada | Coeficientes de puestos y productividad (SUP-127, SUP-128), cobertura de mantenimiento (SUP-139), cadencias (SUP-147), días de stock (SUP-150), arquitecturas sin orden (SUP-152) |
| **RESULTADO DEL MODELO** | Cifra calculada desde supuestos | FTE, pico en sitio, dotación técnica = máx(cobertura, carga), posiciones de setter/hatcher, t/h de planta, inventarios por categoría, plazas por galpón |

### 3.1 Revisión de solapamientos (pedida explícitamente)

| Tema | Registro existente | Tratamiento |
|---|---|---|
| Productividad | SUP-063 (colgado y eviscerado de referencia) | SUP-127/128 nuevos (todas las áreas); SUP-063 **anotado** (extremos de rango) |
| Turnos / jornada | SUP-053 (horas netas), SUP-062 (ecuación de 24 h) | SUP-125 nuevo (jornada laboral ≠ horas netas); SUP-053 y SUP-062 **anotados** |
| Automatización | SUP-065 (matriz de equipos y niveles) | SUP-137 nuevo (traducción por área); SUP-065 **anotado** sin modificar |
| Limpieza | SUP-062 (ventanas) | SUP-129 nuevo (dotación); usa las ventanas sin cambiarlas |
| Mantenimiento | SUP-062 (ventana), SUP-065 (activos) | SUP-132 (carga) y SUP-139 (cobertura) nuevos: **dos mecanismos distintos** |
| Flota propia / tercerizada | SUP-033, SUP-096 | SUP-134 nuevo (choferes); SUP-033 **anotado** |
| Granjas propias / integradas | SUP-034 | SUP-034 **anotado** (se mantiene); SUP-133 (coordinación) nuevo |
| Alimentación | SUP-032 (60 / 30 ilustrativo) | **SUP-14B-08 consolidado en SUP-032** (rangos por categoría; no fórmula) |
| Mortalidad / FCR | SUP-026, SUP-028 | Sin cambios: 14B los **importa** de `03` (test U09) |
| Días de stock | SUP-056 (inventario de producto) | SUP-150 nuevo (insumos upstream); SUP-056 **anotado**: universos distintos |
| Incubación, fertilidad, incubabilidad | — | SUP-143 a SUP-145 nuevos (referencia de pico `[PVDP]`, no promedio) |
| Márgenes de diseño | — | SUP-146 nuevo (reserva de diseño, no óptimo) |
| Tamaño / capacidad de galpones | SUP-031 (1.200 / 1.800 / 2.400 m²) | SUP-153 nuevo (granja ≠ galpón ≠ lote); SUP-031 **anotado** (plazas = equivalencias) |
| Camión de grano | SUP-096 (granelero ~28 t) | **SUP-14B-13 consolidado en SUP-096** (barrido 25 / 28 / 30 t) |
| Integración por etapas | SUP-007 | SUP-152 nuevo (sin orden obligatorio); SUP-007 **anotado** (compatibles) |
| Proxy de personas de 12C | SUP-116 | **Anotado con la contradicción T14-01**; no se reemplaza |

### 3.2 Puntos de RR. HH. y upstream verificados

- **RR. HH.:** jornada de referencia (SUP-125, `[PVDP]`, base de cálculo, no límite legal); **FTE = horas-persona ÷ jornada equivalente** (unidad de cálculo, glosario); **factor de cobertura de nómina PENDIENTE** (SUP-126, DPV-147); productividad por tarea (SUP-127/128); automatización por puesto (SUP-137); política de cobertura de mantenimiento (SUP-139); limpieza (SUP-129); roles combinados (SUP-136); presencia simultánea (SUP-141).
- **Upstream:** fertilidad e incubabilidad (SUP-143); almacenamiento previo del huevo, setter 18 d, hatcher 3 d (SUP-145); margen de capacidad (SUP-146); cadencia de nacimientos (SUP-147); días de stock (SUP-150); densidades (SUP-149); eficiencia, días y horas de la planta de alimento (SUP-148); tamaños de galpón **solo como escenario** (SUP-031, SUP-153).

## 4. Datos por validar

**14 nuevos (DPV-146 a DPV-159)**, todos `Pendiente`; **ninguno N1** (N2: 5 · N3: 8 · N4: 1) y ninguno validado. Ocho propuestas se consolidaron en DPV existentes (§2.2), cuyas filas de la matriz se anotaron. `matriz_validacion_campo.csv` tiene **159 filas** (18 columnas, CRLF preservado, ninguna columna ni estado existente modificado; solo OBSERVACIONES de las filas consolidadas se amplió). Las prioridades de 14A se copiaron; las de 14B (que solo traía nivel N) se asignaron en esta reconciliación y así se indica.

| Tema pedido | DPV | Prioridad | Nivel · ola |
|---|---|---|---|
| Dotación real por sector en plantas argentinas (y pico simultáneo) | DPV-138 (ampliado) | IMPORTANTE ANTES DE DISEÑAR | N2 · O3 |
| Productividad real por tarea | DPV-092 (consolida DPV-14A-04) | IMPORTANTE | N2 · O3 |
| Turnos reales | DPV-082 (anotado) | ÚTIL / N2 | N2 · O3 |
| Convenio colectivo aplicable | **DPV-146** | IMPORTANTE ANTES DE DISEÑAR | N2 · O3 |
| Salarios / costo empresa | **DPV-148** | IMPORTANTE ANTES DE INVERTIR | N2 · O3 |
| Ausentismo, vacaciones, francos, reemplazos, factor de cobertura | **DPV-147** | IMPORTANTE ANTES DE INVERTIR | N2 · O3 |
| Limpieza propia / tercerizada | DPV-091 (consolida DPV-14A-06) | IMPORTANTE | N2 · O3 |
| Mantenimiento | **DPV-150** | IMPORTANTE ANTES DE DISEÑAR | N2 · O3 |
| Disponibilidad de técnicos | DPV-121 (consolida DPV-14A-08) | IMPORTANTE ANTES DE INVERTIR | N2 · O8 |
| Organización real QC / QA / inocuidad | **DPV-151** (supervisión + calidad; ampliado en esta reconciliación) | ÚTIL PARA OPTIMIZAR | N3 · O3 |
| Inspección oficial / SENASA, costos o tasas | DPV-101 (consolida DPV-14A-05) | IMPORTANTE ANTES DE INVERTIR | N2 · O6 |
| HyS y medicina laboral | **DPV-149** | ÚTIL PARA OPTIMIZAR | N3 · O0 |
| Personal para exportación | **DPV-152** | ÚTIL PARA OPTIMIZAR | N3 · O9 |
| Proveedores reales de pollito BB, precios y contratos, mínimos de lote, días de nacimiento, flexibilidad, capacidad disponible, estacionalidad, tiempo de entrega | DPV-047 (consolida DPV-14B-09 + anotación 14B), DPV-006 | CRÍTICO ANTES DE DEFINIR ESCALA | N1 · O4 (sin cambio) |
| Disponibilidad y concentración de huevo fértil | **DPV-154** | IMPORTANTE ANTES DE EVALUAR INCUBACIÓN PROPIA | N3 · O4 |
| Fertilidad / incubabilidad reales | **DPV-153** | ídem | N3 · O4 |
| Tamaño real de galpones; galpones por granja; esquema de llenado; noches de cosecha | DPV-048 (anotado), DPV-133 (consolida DPV-14B-10) | CRÍTICO (N1) / IMPORTANTE ANTES DE DEFINIR ESCALA (≤ 5.000) | N1 · O4 / N2 · O4 |
| Proveedores de alimento; façon; quién compra MP; quién mantiene inventario; mínimos; formulación; mermas; capacidad disponible | DPV-050 (anotado), **DPV-155** | IMPORTANTE ANTES DE INVERTIR / ANTES DE COMPARAR ALTERNATIVAS DE ALIMENTO | N2 · O4 |
| Proveedores de grano, precios, condiciones | **DPV-157**, DPV-117, DPV-050 | IMPORTANTE ANTES DE EVALUAR FAÇON B1 O PLANTA PROPIA | N3 · O4 |
| Plantas de alimento en operación (t/h reales, mermas, energía) | **DPV-158** | IMPORTANTE ANTES DE EVALUAR PLANTA PROPIA | N3 · O4 |
| Densidades y días de stock reales | **DPV-156** | ÚTIL PARA OPTIMIZAR | N4 · O4 |
| Integradores existentes | **DPV-159** | IMPORTANTE ANTES DE FIJAR GATES DE INTEGRACIÓN | N3 · O4 |
| Habilitaciones (fábrica de alimento, incubación, reproductoras) | DPV-007 (consolida DPV-14B-06) | — / N2 | N2 · O6 |

**Coherencia de prioridades:** ningún DPV nuevo es N1; los N1 que ya bloqueaban la escala por abastecimiento (DPV-047, DPV-048, DPV-006) se mantienen y concentran las preguntas de 14B que afectan la escala. Los DPV que solo importan si se evalúa integrar (huevo fértil, incubación, granos, planta de alimento) quedan N3: no bloquean la escala ni la inversión inicial de referencia.

## 5. Decisiones

**12 nuevas de 14A/14B (DEC-067 a DEC-078) + 1 alta derivada (DEC-079)**, todas `Abierta`, sin resultado; **2 consolidaciones** (DEC-060, DEC-024 ampliadas). Los "benchmarks de comparación" de 14B **no** se registraron como decisiones.

| Tema que sigue abierto | Decisión |
|---|---|
| Limpieza propia / tercerizada / híbrida | **DEC-067** |
| Mantenimiento propio / tercerizado / mixto | **DEC-068** (y DEC-040, anotada) |
| Flota propia / tercero (efecto en choferes) | DEC-056 (anotada) |
| Organización por turnos | **DEC-069** (sub-decisión de DEC-036, anotada; incluye variante 12 h netas = 2 × 6) |
| Nivel de automatización | DEC-037 (anotada con los resultados de 14A, no validados) |
| Laboratorio propio | DEC-065 (anotada: +1 / +1 / +2 / +3 FTE) |
| Estructura organizacional por fase | **DEC-070** |
| Polivalencia, HyS, lavandería | **DEC-071**, **DEC-072**, **DEC-073** |
| Comprar pollito vs incubar; reproductoras futuras | DEC-023 (anotada; reproductoras solo arquitectura futura) y **DEC-078** (tecnología, si se incuba) |
| Alimento comprado vs façon vs planta propia | DEC-024 (ampliada con B1 / B2), **DEC-075**, **DEC-076**, **DEC-077** |
| Granjas propias vs integradas vs mixtas | DEC-020 (anotada; arquitecturas distintas) |
| Días de stock y estrategia de silos | **DEC-079** (alta derivada) |
| Cadencia de nacimientos (y unidad de colocación) | DEC-060 (ampliada) |
| Integración vertical por fase | **DEC-074** (gates upstream) y DEC-002 (anotada) |

## 6. Fuentes

**12 nuevas (FTE-298 a FTE-309)** en `25_fuentes/registro_fuentes.csv` (309 filas, 11 columnas, IDs únicos y sin huecos) y en `bibliografia.md` por tipo, con nota de sesión. **Todas siguen `[PVDP]`**: 14A usó referencias legales de conocimiento general (no leídas) y 14B extractos de buscador; no se mejoró el nivel de evidencia. Ajustes administrativos (no de contenido):

- **Tipos normalizados** al registro: `oficial_int` → `internacional` (FTE-304).
- **URL marcadoras** de 14A (`https://servicios.infoleg.gob.ar (texto a ubicar)`, repetida cinco veces) se hicieron distintas indicando qué texto falta ubicar; **no se inventaron URLs**. Ninguna URL nueva duplica una existente (queda solo el duplicado preexistente FTE-001/FTE-071 y el marcador de portal de FTE-283/284 de la reconciliación 12).
- **FTE-303** (convenio colectivo) es un **registro de búsqueda**: convenio no identificado, URL `PENDIENTE` y confiabilidad **"—"** (excepción declarada a la escala A/B/C: no hay documento que calificar).
- FTE-308 y FTE-309 quedan `[PVDP · débil]` (sectorial / comercial). Fuentes centrales reutilizadas sin cambios: FTE-071, FTE-149, FTE-151, FTE-187, FTE-200, FTE-218, FTE-219, FTE-229, FTE-287.

## 7. Reconciliación RR. HH.

### 7.1 Con 12C (layout): servicios al personal

**Contradicción registrada, no resuelta (T14-01).** 12C usó un proxy de personas por turno (SUP-116) de **49 / 82 / 115 / 165** para vestuarios a 2.500 / 5.000 / 10.000 / 20.000 aves/día; 14A obtiene un **pico de personas en sitio** de **41 / 58 / 72 / 87** (puestos simultáneos de producción 31 / 40 / 47 / 50; cuadrilla de limpieza 7 / 11 / 19 / 35 en otra franja). No se decide cuál es correcto: el proxy no tiene matriz de presencia y 14A no tiene dato real; ambas cifras son estimaciones.

Para dimensionar **vestuarios, comedor y servicios al personal**, la variable relevante será el **pico de personas simultáneas que realmente requieren ese servicio**, más:

- margen;
- cambios de turno (con dos cuadrillas el pico ocurre en el traspaso: 72 → 96 a 10.000 aves/día);
- composición por sexo cuando corresponda;
- separación sanitaria por zona (sucia / limpia; circuitos de cambio);
- requisitos normativos (DPV-090, DPV-140);
- terceros en sitio (limpieza, mantenimiento, choferes si usan instalaciones);
- inspección oficial si usa las instalaciones (DPV-101, DPV-140);
- expansión.

**No** se usan automáticamente FTE anuales, headcount total ni total de funciones. **La superficie definitiva sigue PENDIENTE** (DPV-138, DPV-140). 12C no se recalculó; cuando se valide la dotación, el pico debe cargarse como **input** de `modelo_superficies.py` (dependencia D14-01).

### 7.2 Con 09A (proceso)

| Aspecto | Coherencia verificada | Observación |
|---|---|---|
| Puestos por operación | Coherente con los rangos de 09A: colgado 1 / 1 / 2 / 3 (09A: 1 → 2 referencia, 1 → 4 prudente); evisceración manual 6 a 2.500 y 35 a 20.000 (09A: 3 → 21 referencia, 6 → 42 prudente) | 14A agrega menudencias, puestos fijos y áreas que 09A no tenía |
| Automatización | 14A usa la arquitectura de referencia de 09A por escala (SUP-137) sin modificarla | Los ahorros son resultado de los coeficientes |
| Horas netas | 14A importa D, pausas y limpieza intermedia de `modelo_capacidad_proceso.py` (test R12: 09A intacto) | — |
| Turnos | 1 cuadrilla / extendido / 2 cuadrillas evaluados contra la ecuación de 24 h y la jornada de referencia | Brecha ~2 h/persona con 8 h netas (T14-02) |
| Limpieza | Usa las ventanas de SUP-062 y los m² proxy de 12C | `t_limpieza` sigue provisional (no depende de la escala) |
| Mantenimiento | Ventana de mantenimiento de SUP-062 para el técnico de guardia | — |

**14A no se usa para resolver la tensión de 09A** "16 h netas vs ecuación completa de 24 h" (T-03 de la reconciliación 09): 14A agrega una restricción **laboral** distinta (jornada), no una evidencia sobre las ventanas de limpieza, sanitización y mantenimiento. Dependencia registrada (D14-02):

**CAPACIDAD OPERATIVA ↔ HORAS NETAS ↔ TURNOS ↔ DOTACIÓN ↔ LIMPIEZA ↔ MANTENIMIENTO.** Cambiar cualquiera mueve las otras: más horas netas con la misma cuadrilla abren la brecha de jornada; dos cuadrillas suben FTE y pico en sitio; una limpieza más larga reduce la ventana disponible para producir y cambia la cuadrilla; más automatización reduce directos y aumenta mantenimiento. Ninguna se fija sin datos de campo (DPV-082, DPV-091, DPV-146, DPV-150).

### 7.3 Con 09C (utilities: agua, energía, frío)

Mayor automatización y mayor escala pueden implicar **más técnicos** (frío, electricidad, PLC, utilities, PTE), más **energía** y **frío** (09C), y más **mantenimiento**. **No** se convierte número de equipos en dotación validada: el conteo de `08_maquinaria/matriz_equipos.csv` es un insumo de la **carga por activos** (SUP-132), con rango 1,1–17,1 FTE a 20.000 aves/día. El modelo de mantenimiento conserva **dos mecanismos distintos**:

| Mecanismo | Pregunta | Registro | Resultado (media) 2.500 / 5.000 / 10.000 / 20.000 |
|---|---|---|---|
| **Cobertura operativa** | ¿Cuántos técnicos deben estar presentes mientras funcionan los activos? | SUP-139 (política de referencia, no requisito universal) | 2,1 / 3,5 / 4,9 / 6,4 FTE |
| **Carga por activos** | ¿Cuántas horas de trabajo exigen los activos? | SUP-132 | 2,3 / 2,4 / 3,6 / 7,5 FTE |
| Reconciliación | máx(cobertura, carga) — **resultado del modelo** | — | 2,3 / 3,5 / 4,9 / 7,5 FTE |

La lista de cargas por equipo (DPV-095) y el balance frigorífico (DPV-109) siguen pendientes; cuando existan, podrán afinar la carga de mantenimiento de frío y utilities sin mezclar los dos mecanismos.

## 8. Reconciliación upstream

### 8.1 Con 03 (producción primaria): reproducción exacta

`modelo_upstream.py` **importa** `03_produccion_primaria/modelo_escenarios_produccion.py` sin recalcularlo (test U09). Verificado en esta sesión contra `03_produccion_primaria/escenarios_produccion.csv` (perfil y desempeño medios, 5 d):

| Planta (aves faenadas/día) | Pollitos alojados / semana plena (03 · 14B) | Pollitos / año (03 · 14B) | Alimento t/año (03 · 14B) |
|---|---|---|---|
| 2.500 | 13.197 · 13.197,5 | 659.874 · 659.874,4 | 3.091 · 3.090,5 |
| 5.000 | 26.395 · 26.395,0 | 1.319.749 · 1.319.748,7 | 6.181 · 6.181,0 |
| **10.000** | **52.790 · 52.789,9** | **2.639.497 · 2.639.497,4 (≈ 2,639 M)** | **12.362 · 12.362,1** |
| 20.000 | 105.580 · 105.579,9 | 5.278.995 · 5.278.994,9 | 24.724 · 24.724,2 |

Las diferencias son solo de redondeo de presentación (el CSV de 03 redondea a enteros). `03` **no** se recalculó.

**Cadena física registrada (D14-03):** **POLLITO → GALPÓN → ENGORDE → RETIRO → FAENA** — pollitos alojados −(mortalidad en granja, SUP-026)→ aves cargadas −(mortalidad en transporte)→ aves faenadas; con incubación propia se antepone huevo recibido → cargado → transferido → nacido → vendible (SUP-143 a SUP-145). Cadena temporal: carga día 0 → nacimiento día 21 → colocación (21 + horas PENDIENTES) → retiro ≥ día 68 → faena ≥ 68,4 → siguiente colocación de la misma unidad a los 62 días (47 d de engorde + 15 d entre lotes, SUP-029).

### 8.2 Incubación con galpones y faena

- **Demanda media semanal de pollitos ≠ tamaño de cada nacimiento:** lote = demanda / nacimientos por semana (a 10.000 aves/día: 52.790 / 26.395 / 17.597 / 10.558 con 1 / 2 / 3 / 5 nacimientos; test U15). Con pollito comprado, el lote lo fija el proveedor (PENDIENTE, DPV-047).
- **GRANJA ≠ GALPÓN ≠ LOTE:** la unidad de colocación es variable (galpón o granja); plazas por galpón = equivalencias derivadas de SUP-031 (no galpones reales); galpones por granja reales PENDIENTES (DPV-048, DPV-133).
- **Lo que existe es un CHEQUEO DE SINCRONIZACIÓN, no un optimizador** (SUP-153; tests U16, U21). Detecta tensiones entre cadencia de nacimientos, tamaño de galpón/lote, capacidad de alojamiento, duración de cosecha (> 2 días de faena por unidad) y cadencia de faena, y marca **REQUIERE VALIDACIÓN**. **No se declara incompatibilidad definitiva** (T14-06, T14-07).

### 8.3 Setter / hatcher

Los registros globales **no** conservan las cifras v1.0 de "posiciones de incubadora" (50.508 / 101.015 / 202.030 / 404.060): se verificó que no aparecen en `00_gestion_proyecto/` ni en `25_fuentes/`; en los módulos solo figuran como **corrección retirada** (`capacidad_incubacion.md` §1). La capacidad queda separada conceptualmente:

| Concepto | Registro | Valor del modelo (margen 15 %) |
|---|---|---|
| **Setter** (18 d + 1 d de limpieza por lote) | SUP-145, SUP-147 | 55.824 / 111.648 / 223.296 / 446.593 posiciones (igual para las cinco cadencias) |
| **Hatcher** (3 d + 1 d) | SUP-145, SUP-147 | 12.343–148.120 posiciones según escala y cadencia (1–2 nacimientos/semana: +50 % frente a 3) |
| **Frecuencia de carga** = nacimientos por semana | SUP-147 (ilustrativa, no elegida) | 1 a 5 |
| **Tamaño de lote** | test U15 | demanda / cadencia |
| **Margen de capacidad** | SUP-146 | 10 / 15 / 20 % (reserva de diseño, no óptimo) |

Si en algún documento futuro se informa una cifra física total, debe indicarse como **suma de posiciones físicas instaladas (inventario de máquinas)**, **no** como una capacidad operativa única e intercambiable entre setter y hatcher.

### 8.4 Alimento e inventarios

La comparación v1.0 **"106 t vs 583 t vs 653 t"** (compra / façon / planta propia a 10.000 aves/día) **no aparece** en los registros globales y en los módulos solo figura como retirada. Quedan separados (SUP-154; tests U18, U19):

| Categoría (10.000 aves/día, medio, días de parámetro) | t | Propio en A / B1 / B2 / C |
|---|---|---|
| Alimento terminado en granja (3 d) | 106 | Propio en todas (si hay integrados o granjas propias; 0 si se compra pollo vivo) |
| Alimento terminado en planta / elaborador (2 d) | 71 | Tercero / propio / tercero / propio |
| Maíz (15 d) | 318 | Tercero / propio (en elaborador o acopio) / tercero / propio |
| Harina de soja (15 d) | 159 | ídem |
| Micros, aceite y otros (30 d) | 106 | ídem |
| Material en proceso | PENDIENTE | — |

**No se suman categorías.** Stock propio ≠ stock en tercero ≠ stock total de la cadena. **Integrar puede cambiar PROPIEDAD, UBICACIÓN y CAPITAL DE TRABAJO aunque el requerimiento físico de la cadena sea similar** (con los mismos días de stock, idéntico). Es **dependencia directa de OPEX / capital de trabajo** (D14-04; DEC-079, DPV-155, DPV-156).

## 9. Contradicciones y tensiones (ninguna resuelta)

| ID | Tensión | Módulos | Detalle | Qué la cierra |
|---|---|---|---|---|
| **T14-01** | **Dotación de 12C vs pico de 14A** (ex T-14A-3) | 09/12C ↔ 18 | Proxy 49 / 82 / 115 / 165 (SUP-116) vs pico en sitio 41 / 58 / 72 / 87; el proxy es 1,2–1,9 × el pico. Probable causa parcial: el proxy mezcla dotación de turno con un factor por ritmo, sin matriz de presencia. No se decide cuál es correcto | DPV-138, DPV-140, DPV-101; dimensionar con pico simultáneo + margen y requisitos (§7.1) |
| **T14-02** | **8 h netas vs organización laboral** (ex T-14A-1) | 23 / 05 / 12B ↔ 18 | Con la jornada de referencia de 8 h, una cuadrilla no cubre 8 h netas + ventanas auxiliares (presencia ~10 h; brecha ~2 h/persona; 59–91 horas-persona/día). La organización (turnos, relevos, escalonamiento, personal adicional, horas extra si el convenio lo permite) no está demostrada. 8 h netas sigue como sensibilidad de capacidad, etiquetada "requiere organización laboral adicional" | DPV-146, DPV-082, DEC-069 |
| **T14-03** | **16 h netas vs dos cuadrillas** (ex T-14A-2) | 23 / 05 ↔ 18 | "16 h = 2 × 8 h netas" choca con la jornada (presencia 10,2 h por cuadrilla) y con la ecuación de 24 h (holgura +0,9 / −2,8 / −8,3 h); dos cuadrillas dentro de la jornada dan ~11,4–13,5 h netas. Variante 12 h netas (2 × 6) agregada a DEC-036/069 como opción a estudiar, no recomendación. **No se usa para cerrar T-03 de 09A** | DPV-091, DPV-082, DPV-146, DEC-036, DEC-069 |
| **T14-04** | **Automatización vs reducción de operarios vs aumento técnico** | 08 / 09A ↔ 18 | De manual a automático: directos −33 % (2.500) a −67 % (20.000) y mantenimiento +1,5 a +3,1 FTE; a 2.500, semiautomático → automático no reduce FTE (47,0 → 47,1). Cambia perfiles y crea dependencia de servicio técnico. Resultado de coeficientes supuestos | DPV-092, DPV-150, DPV-121, DPV-089, DEC-037 (costos en OPEX) |
| **T14-05** | **Cobertura de mantenimiento vs carga por activos** | 18 ↔ 08 / 09C | Manda la carga a 2.500 y 20.000 y la cobertura a 5.000–10.000; la cobertura es una **política**, la carga un supuesto por equipo (rango 1,1–17,1 FTE a 20.000) | DPV-150, DEC-068 |
| **T14-06** | **Cadencia de nacimiento vs tamaño de galpón** | 15 ↔ 03 ↔ 13 | A 2.500 aves/día un galpón equivalente de 1.800 m² necesita ~1,7–8,7 nacimientos para llenarse según la cadencia → edades distintas en un lote; tolerancia de edad PENDIENTE | DPV-047, DPV-133, DEC-060 |
| **T14-07** | **Producción semanal de pollitos vs llenado de unidades** | 14B ↔ 03 ↔ 12B | La demanda media semanal no llena unidades grandes a escala chica; cosechar una unidad de 15.000–30.000 aves lleva ~6–12 días de faena a 2.500 aves/día (referencia de cosecha 2 días). Requiere validación, no demuestra incompatibilidad (continúa DEC-060 / DPV-133 de 12B) | DPV-048, DPV-133, DEC-060 |
| **T14-08** | **Fábrica de alimento propia vs utilización** | 14 | A 2.500 aves/día una planta de 2,1 t/h trabajaría ~35 h/semana (21 % de 168 h) operando todos los días bajo la cadencia asumida; alternativas: menos días, lotes concentrados, terceros, reserva estratégica. Decisión económica no tomada | DPV-158, DEC-024, DEC-074, DEC-075 |
| **T14-09** | **Stock físico vs propiedad / capital de trabajo** | 14 ↔ 20 / 21 | Mismo stock físico de la cadena en A, B1, B2 y C; cambia quién lo posee y dónde está; los días del tercero son PENDIENTES; en la realidad los días no serán iguales | DPV-155, DPV-156, DEC-079 |
| **T14-10** | **Integración upstream vs flexibilidad / capital** | 14 / 15 ↔ 23 | Integrar da control (calidad, programación, bioseguridad) a cambio de capital, capacidad fija y ociosidad (setter 79 %, hatcher 50–75 % de utilización media de diseño); incubar sustituye la dependencia de pollito por la de huevo fértil. Sin costos no hay conclusión | DEC-074, DEC-020, DEC-023, DEC-024; CAPEX/OPEX |
| T14-11 | Limpieza en ventana de ~4 h (ex T-14A-4) | 05 ↔ 18 | Dotación simultánea alta con pocas horas (35 personas = 17,5 FTE a 20.000); limpieza por sectores cambiaría dotación y pico | DPV-091, DEC-067 |
| T14-12 | Silos: celdas mínimas por segregación | 14 | 5–8 celdas mínimas no escalan con el volumen; pesan a escala chica | DPV-156, DEC-079 |
| T14-13 | "Granja equivalente de 30.000 plazas" (14A, técnicos de campo) vs granja ≠ galpón (14B) | 18 ↔ 14B ↔ 12B | 14A usa la granja equivalente de 12B como driver; 14B deja galpones por granja PENDIENTES. Nomenclatura, no contradicción numérica | DPV-048, DPV-133 |

## 10. Dependencias para CAPEX (sin calcular, sin precios)

Conceptos de 14A/14B que deberán entrar en `19_capex` **cuando se habilite**. Ninguno tiene monto; ninguna alternativa está elegida.

| Bloque | Conceptos | Driver físico disponible (resultado de modelo, no validado) | Condición |
|---|---|---|---|
| **RR. HH. / edificio** | Vestuarios (por zona y sexo), comedor, oficinas, laboratorio si corresponde (DEC-065), talleres, mantenimiento y pañol, lavandería y ropería (DEC-073), instalaciones del personal, servicios para inspección oficial (DPV-140) | Pico de personas en sitio y simultáneos por zona (SUP-141; `modelo_rrhh.salida_layout`); superficies proxy de 12C | Contradicción T14-01 abierta; superficie definitiva PENDIENTE |
| **Incubación** (solo si se modela la opción B o C) | Terreno / edificio; almacenamiento de huevo (sala climatizada); **setters**; **hatchers**; vacunación; clasificación/selección; HVAC; energía; respaldo; lavado; expedición (camiones climatizados); bioseguridad | Setter y hatcher por separado según cadencia (§8.3); huevos en almacén 13.426–107.406 | DEC-023, DEC-074, DEC-078; DPV-153, DPV-154; habilitación DPV-007 |
| **Alimento** (solo si se modela planta propia) | Recepción (balanza, calado, fosa); silos de materias primas; molienda; dosificación; mezclado; pellet / enfriado si corresponde (DEC-076); almacenamiento de producto terminado; expedición; laboratorio / calidad; control de polvo y explosión; utilities (vapor, aire, energía) | t/h requerida 0,9–41 según factores (SUP-148); silos por días de stock y densidad (SUP-149/150) | DEC-024, DEC-075, DEC-077, DEC-079; DPV-155, DPV-158 |
| **Granjas** | **Propias e integradas son arquitecturas distintas**: propias → galpones, equipamiento, silos de granja, terreno; integradas → sin activos de galpón propios, pero con capital de trabajo (alimento por ciclo 415–3.320 t) y asistencia técnica | m² de `03` (9.500–75.900 m² medio) | DEC-020, DEC-022; DPV-048, DPV-051 |

## 11. Dependencias para OPEX y capital de trabajo (sin importes)

| Bloque | Variables que alimentarán OPEX | Fuente en el modelo | Dato faltante |
|---|---|---|---|
| **RR. HH.** | FTE (internos, tercerizados), **headcount** (PENDIENTE), horas-persona y horas contratadas, tercerización (limpieza, mantenimiento, flota), factor de cobertura, adicionales (nocturnidad, horas extra si el convenio lo permite), turnos y cuadrillas | `escenarios_rrhh.csv`, `plantilla_costo_laboral.csv` (costos **vacíos**) | DPV-146, DPV-147, DPV-148 |
| **Incubación** | Huevo fértil (cantidad por semana), energía, vacunas, personal, limpieza, descartes, logística de pollitos y de huevo | `escenarios_upstream.csv` bloques `2_*` | DPV-153, DPV-154, DPV-047, DPV-056 |
| **Alimento** | **Alimento comprado** (t por fase) **o** materias primas (maíz, soja, micros) + molienda + energía + mantenimiento + personal + almacenamiento + transporte + **tarifa de façon** | Bloques `4_alimento`, `5_materias_primas`, `6_planta_*`, `8_opcion_alimento`, `10_logistica` | DPV-050, DPV-155, DPV-157, DPV-158 |
| **Capital de trabajo** | Inventarios de alimento por categoría y propiedad, granos, huevo fértil, pollitos y aves en crianza (con integrados), plazos de pago y cobro | Bloque `7_inventarios`; `almacenamiento_silos.md` §5 | DPV-155, DPV-156, DEC-079; condiciones de pago (DPV-039, DPV-047) |

**Dependencias registradas:** D14-01 (18 → 09: pico simultáneo → vestuarios, comedor, estacionamiento; reemplaza la D12-05 pendiente); D14-02 (05 ↔ 18: capacidad ↔ horas netas ↔ turnos ↔ dotación ↔ limpieza ↔ mantenimiento); D14-03 (03 → 14/15: cadena pollito → faena, importada sin recálculo); D14-04 (14 → 20/21: propiedad del inventario → capital de trabajo); D14-05 (18, 14, 15 → 19/20: conceptos de §10–11).

## 12. Estado final

| Módulo | Estado | Pendiente |
|---|---|---|
| Recursos humanos (`18`) | **MODELO PRELIMINAR DE ORGANIZACIÓN Y DOTACIÓN COMPLETADO** v1.1 (24 tests, 13/13 mutaciones) | Validación de productividad real, convenio, costos, cobertura, dotación real y organización definitiva |
| Upstream (`14`, `15`) | **MODELO PRELIMINAR DE INCUBACIÓN / ALIMENTO / INTEGRACIÓN COMPLETADO** v1.1 (21 tests) | Proveedores, precios, contratos, oferta, capacidades reales, decisión make-or-buy y economía de la integración. **Ninguna arquitectura recomendada** |
| CAPEX / OPEX (`19`, `20`) | No iniciados | Preparados conceptualmente (§10–11) |

Detalle en [`estado_proyecto.md`](estado_proyecto.md). **Glosario:** 11 términos nuevos (FTE, headcount de nómina, dotación simultánea, pico de personas en sitio, factor de cobertura de nómina, setter, hatcher, hatch / lote de nacimiento, alimento a façon, make-or-buy, stock propio / en tercero); "huevo fértil" ya existía y no se duplicó.

## 13. Tests

Ejecutados el 2026-10-02 después de la integración, con `PYTHONDONTWRITEBYTECODE=1`. En `modelo_rrhh.py` y `modelo_upstream.py` solo cambiaron IDs en comentarios, docstrings, etiquetas `ref=`/`parametros` y textos de salida. Al regenerar, `escenarios_upstream.csv` y `plantilla_costo_laboral.csv` resultaron **idénticos byte a byte** al reemplazo textual de IDs sobre la versión de `HEAD` (CRLF preservado en la plantilla); `escenarios_rrhh.csv` no cambió. Los CSV regenerados por las suites importadas (03, 09, 13) no cambiaron.

| Suite | Comando | Resultado |
|---|---|---|
| **RR. HH. (14A)** | `18_recursos_humanos/modelo_rrhh.py --solo-tests` / `--mutaciones` | **24/24**; mutaciones **13/13** detectadas |
| **Upstream (14B)** | `14_alimento_balanceado/modelo_upstream.py` (pruebas + CSV) | **21/21** (U01–U21; 15.998 filas, 1.054 PENDIENTES) |
| Producción primaria | `03_produccion_primaria/modelo_escenarios_produccion.py` | 10/10 bloques OK (sin fallas) |
| Balance de masa | `04_balance_masa/modelo_balance_masa.py --solo-tests` | 21/21 |
| Escala | `23_plan_expansion/modelo_escala.py --solo-tests` | 23/23 |
| Proceso (09A) | `05_proceso_industrial/modelo_capacidad_proceso.py --solo-tests` | 18/18 |
| Layout (12C) | `09_layout_obra_civil/modelo_superficies.py` | 22/22 |
| Logística (12B) | `13_logistica/modelo_logistica.py` | 28/28; pruebas con la tabla OK (18.268 filas) |

No se ejecutaron utilities (09C) ni localización (12A): no intervienen en esta reconciliación y sus modelos no cambiaron.

**Control de integridad**

| Control | Resultado | Detalle |
|---|---|---|
| IDs SUP únicos y consecutivos | OK | 154 (SUP-001–SUP-154); duplicados []; huecos [] |
| IDs DPV únicos y consecutivos | OK | 159 (DPV-001–DPV-159); duplicados []; huecos [] |
| IDs DEC únicos y consecutivos | OK | 79 (DEC-001–DEC-079); duplicados []; huecos []; ninguna `Tomada` ni `Descartada` |
| IDs FTE únicos y consecutivos | OK | 309 (FTE-001–FTE-309); duplicados []; huecos [] |
| Sin SUP/DPV/DEC/FTE/T provisionales activos | OK | solo en `actualizaciones_gestion_14*.md`, `fuentes_14*.csv` (históricos) y este documento |
| CSV válidos | OK | 28 CSV, columnas constantes, sin filas duplicadas en los registros |
| URLs nuevas duplicadas | OK | ninguna; persisten 2 repeticiones preexistentes (FTE-001/FTE-071; marcador de portal FTE-283/284) |
| `matriz_validacion_campo.csv` ↔ `datos_por_validar.md` | OK | 159 = 159 IDs; nivel N1–N4 idéntico en ambos; filas existentes intactas salvo OBSERVACIONES de las 9 ampliadas |
| Referencias SUP/DPV/DEC/FTE | OK | todas definidas |
| Enlaces relativos | OK | todos resuelven |
| Marcadores de merge | OK | ninguno |
| Glosario sin duplicados | OK | 270 términos |
| Filas de tablas de registros | OK | todas con el número de columnas del encabezado |

**Archivos modificados (36):**

- `00_gestion_proyecto/datos_por_validar.md` — modificado
- `00_gestion_proyecto/decisiones_pendientes.md` — modificado
- `00_gestion_proyecto/estado_proyecto.md` — modificado
- `00_gestion_proyecto/glosario.md` — modificado
- `00_gestion_proyecto/matriz_validacion_campo.csv` — modificado
- `00_gestion_proyecto/plan_trabajo_campo.md` — modificado
- `00_gestion_proyecto/supuestos.md` — modificado
- `14_alimento_balanceado/README.md` — modificado
- `14_alimento_balanceado/actualizaciones_gestion_14B.md` — modificado
- `14_alimento_balanceado/almacenamiento_silos.md` — modificado
- `14_alimento_balanceado/compra_vs_fabricacion.md` — modificado
- `14_alimento_balanceado/conclusiones_alimento.md` — modificado
- `14_alimento_balanceado/demanda_alimento.md` — modificado
- `14_alimento_balanceado/escenarios_upstream.csv` — modificado
- `14_alimento_balanceado/integracion_upstream.md` — modificado
- `14_alimento_balanceado/modelo_upstream.py` — modificado
- `14_alimento_balanceado/planta_alimento_conceptual.md` — modificado
- `15_incubacion/README.md` — modificado
- `15_incubacion/capacidad_incubacion.md` — modificado
- `15_incubacion/compra_vs_incubacion.md` — modificado
- `15_incubacion/conclusiones_incubacion.md` — modificado
- `15_incubacion/modelo_incubacion.md` — modificado
- `18_recursos_humanos/README.md` — modificado
- `18_recursos_humanos/actualizaciones_gestion_14A.md` — modificado
- `18_recursos_humanos/calidad_inocuidad.md` — modificado
- `18_recursos_humanos/conclusiones_rrhh.md` — modificado
- `18_recursos_humanos/dotacion_por_escala.md` — modificado
- `18_recursos_humanos/estructura_organizacional.md` — modificado
- `18_recursos_humanos/guia_ramiro.md` — modificado
- `18_recursos_humanos/mantenimiento_y_servicios.md` — modificado
- `18_recursos_humanos/modelo_rrhh.py` — modificado
- `18_recursos_humanos/plantilla_costo_laboral.csv` — modificado
- `18_recursos_humanos/turnos_y_productividad.md` — modificado
- `25_fuentes/bibliografia.md` — modificado
- `25_fuentes/registro_fuentes.csv` — modificado
- `00_gestion_proyecto/reconciliacion_sesiones_14.md` — creado

Los `actualizaciones_gestion_14*.md` solo recibieron el encabezado de ARCHIVO HISTÓRICO; los `fuentes_14*.csv` quedan sin cambios, como históricos.

## 14. Próximos pasos

1. **Revisión de Ramiro** de esta rama antes de abrir un PR (no se creó PR).
2. Trabajo de campo prioritario para estos módulos (sin cuestionario nuevo): en las visitas a plantas (O3) relevar dotación por sector, pico en cambio de turno, limpieza, mantenimiento, supervisión y calidad (DPV-138, 091, 092, 147, 150, 151); identificar el convenio y el costo laboral (DPV-146, 148); en O4 sumar fábricas de alimento / façon, proveedores de grano e integradores (DPV-155 a 159) y las preguntas de sincronización a incubadoras y productores (DPV-047, DPV-133).
3. Incorporar a `cuestionario_incubadoras.md` y `cuestionario_productores.md` las preguntas ya registradas en DPV-047 y DPV-133 (pendiente; no se hizo en esta reconciliación).
4. Cuando el promotor lo habilite: CAPEX (§10) y luego OPEX y capital de trabajo (§11), comparando todas las arquitecturas upstream sin caso base.
5. Al validar la dotación: cargar el pico simultáneo como input de `09_layout_obra_civil/modelo_superficies.py` y cerrar T14-01; no antes.
6. Retirar los archivos históricos `actualizaciones_gestion_14*.md` y `fuentes_14*.csv` queda a criterio del promotor (se conservan, como en las reconciliaciones 09 y 12).
