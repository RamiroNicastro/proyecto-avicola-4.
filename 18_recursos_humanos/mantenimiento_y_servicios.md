# Mantenimiento, limpieza y servicios de soporte

**Fecha:** 2026-10-01 · **Versión:** 1.1 (sesión 14A; auditoría de unidades laborales) · Fase 0

> **Alcance:** estructura conceptual de mantenimiento (preventivo, correctivo, eléctrico, mecánico, frío, automatización) con **cobertura operativa** y **carga de mantenimiento** separadas; comparación propio / tercerizado / mixto; limpieza y sanitización como **función crítica** con dotación simultánea, horas-persona, FTE y horas contratadas; utilities, HyS, lavandería.
> **No** se elige modalidad (DEC-067, DEC-068, DEC-040), proveedor ni contratista; **no** se calculan costos.
> **Clasificación:** cantidades `[ESTIMACIÓN]` de [`modelo_rrhh.py`](modelo_rrhh.py) v1.1 con coeficientes `[SUPUESTO]` (SUP-129, SUP-132, SUP-139); activos de [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv) (sin modificarla).

---

## 1. Mantenimiento

### 1.1 Estructura conceptual

| Tipo | Contenido | Quién lo hace típicamente | Cuándo |
|---|---|---|---|
| **Preventivo** | Lubricación, dedos de desplumadora, cuchillas, rodamientos, calibraciones, inspecciones | Técnicos propios o del contratista; especialistas para equipos automáticos | Ventana de mantenimiento (0,5 / 1,0 / 2,0 h/día, SUP-062) y fines de semana |
| **Correctivo** | Reparar lo que falla durante la faena | Técnico presente o de respuesta rápida | En producción |
| **Eléctrico** | Tableros, motores, variadores, iluminación; media tensión | Propio (baja tensión); externo matriculado (media tensión) | Ambos |
| **Mecánico** | Transportadores, grilletes, desplumadoras, evisceradoras, bombas | Propio o contratista | Ambos |
| **Frío** | Sala de máquinas, evaporadores, túneles, cámaras (24 h/365 d) | Propio con formación específica o contratista; refrigerante sin decidir (DEC-046) | Guardia |
| **Automatización** | PLC, sensores, balanzas de línea, software de clasificación | Proveedor del equipo en escalas chicas; especialista en automático ≥ 10.000 | Ambos |
| **Utilities** | Caldera/agua caliente, aire comprimido, agua, efluentes, grupo electrógeno | Técnicos de planta; operador de PTE según tecnología | Más horas que la línea |

### 1.2 Dos enfoques con supuestos distintos

| | **Cobertura operativa** | **Carga de mantenimiento** |
|---|---|---|
| Pregunta | ¿Cuántos técnicos deben estar **presentes** mientras funcionan los activos críticos? | ¿Cuántas **horas de trabajo** de mantenimiento exigen los activos? |
| Naturaleza | **Política de cobertura de referencia** (SUP-139), **no requisito técnico universal** | Estimación por activos (SUP-132) |
| Fórmula | (técnicos simultáneos × horas con activos en marcha + 1 de guardia × horas de limpieza, sanitización y mantenimiento) ÷ 8 h | Σ equipos presentes × h/semana por nivel (Mc 0,75 · S 1,5 · A 3, media) × criticidad (1,5 / 1 / 0,5) × unidades ÷ días ÷ (8 h × fracción productiva 0,8) |
| Supuestos | Técnicos simultáneos: 1; +1 desde 5.000; +1 desde 10.000; +1 si automático ≥ 10.000. Una planta puede elegir otra política (técnico de respuesta en minutos, contratista residente, operador polivalente) | Horas por equipo y criticidad sin dato argentino; equipos "duplicables" 1 cada 1.250 aves/h |
| Cambia con | Horas de operación, turnos, política de riesgo | Número de activos, nivel de automatización, criticidad |

**Dotación técnica = reconciliación máx(cobertura, carga)** (test R19). Cambiar la política de cobertura no altera la carga, y viceversa.

### 1.3 Resultados (escenario de referencia, productividad media)

| Escala | Equipos (unidades) | Cobertura: técnicos simultáneos · horas/día · FTE | Carga: h/semana · FTE (alta–media–baja) | Reconciliación (FTE) | Quién manda |
|---|---|---|---|---|---|
| 2.500 (manual) | 61 (3 Mc, 15 S, 12 A) | 1 · 16,5 · 2,1 | 75 · 1,1–2,3–5,3 | 2,3 | carga |
| 5.000 (mecanizado) | 63 (3 Mc, 17 S, 12 A) | 2 · 27,9 · 3,5 | 78 · 1,1–2,4–5,5 | 3,5 | cobertura |
| 10.000 (semiautomático) | 65 (3 Mc, 46 S, 12 A) | 3 · 39,4 · 4,9 | 114 · 1,6–3,6–8,1 | 4,9 | cobertura |
| 20.000 (automático) | 85 (7 S, 75 A) | 4 · 50,9 · 6,4 | 239 · 3,3–7,5–17,1 | 7,5 | carga |

Más jefe de mantenimiento (desde 5.000; coordinador de contratos si se terceriza) y pañolero (desde 10.000, con modalidad propia o mixta).

| Escala | Propio: FTE interno / tercerizado | Tercerizado | Mixto (cobertura propia + especialistas) |
|---|---|---|---|
| 2.500 | 2,3 / 0 | 0 / 2,3 (+0,5 coordinación interna) | 2,1 / 0,3 |
| 5.000 | 3,5 / 0 (+1 jefe) | 0 / 3,5 (+1 coordinación) | 3,5 / 0 (+1 jefe) |
| 10.000 | 4,9 / 0 (+1 jefe) | 0 / 4,9 (+1 coordinación) | 4,9 / 0 (+1 jefe) |
| 20.000 | 7,5 / 0 (+1 jefe) | 0 / 7,5 (+1 coordinación) | 6,4 / 1,1 (+1 jefe) |

Las horas de mantenimiento son las mismas en las tres modalidades (test R17): tercerizar las convierte en **horas contratadas**, no las elimina.

**Lecturas:** (1) con la política de referencia, entre 5.000 y 10.000 manda la cobertura (mantenimiento casi fijo por turno); con otra política podría mandar la carga; (2) a 20.000 automático manda la carga (7,5 vs 6,4 FTE), con un rango muy amplio (3,3–17,1) porque las horas por equipo son el supuesto menos respaldado (DPV-150); (3) dos cuadrillas extienden las horas con activos en marcha y aumentan la cobertura; (4) la automatización nunca reduce técnicos (test R03).

### 1.4 Propio vs tercerizado vs mixto (sin elección)

| Criterio | Propio | Tercerizado | Mixto |
|---|---|---|---|
| Respuesta a una falla en producción | ▲ inmediata | ▼ según contrato y distancia; requiere residentes | ▲ cotidiana; ● especializada |
| Conocimiento de la planta | ▲ | ▼ rota con el contratista | ▲ |
| Especialidades (frío con amoníaco, PLC, media tensión) | ▼ difícil en escalas chicas | ▲ | ▲ |
| Dependencia | De retener técnicos | Del contratista y del proveedor de equipos | Repartida |
| Función interna que **no** se terceriza | — | Coordinación, planificación del preventivo, repuestos críticos (DEC-040) | Jefe de mantenimiento |
| Datos faltantes | Técnicos por corredor (DPV-121) | Contratistas y servicio técnico local (DPV-089) | Ambos |

## 2. Limpieza y sanitización — función crítica

### 2.1 Por qué es crítica

- Condición de habilitación e inocuidad: POES escritos con limpieza preoperativa y operativa, responsables, verificación y acciones correctivas (Res. SENASA 233/1998, `[PVDP]`); su verificación es parte del APPCC obligatorio (Res. 205/2014, `[PVDP]`).
- Ocupa la ventana de 24 h: limpieza + sanitización = 3,0 / 4,0 / 6,0 h/día (SUP-062).
- Es el bloque de personal más incierto: m² de salas (12C, proxy), complejidad de equipos y organización de la ventana.

### 2.2 Dos componentes

| Componente | Quién | Cuándo | Modelo |
|---|---|---|---|
| **Limpieza operativa** (pisos, derrames, recipientes, limpieza intermedia) | Siempre interna | Durante producción, con la cuadrilla de línea | 1 + 0,3 / 0,5 / 0,8 puestos por 1.000 aves/h, por cuadrilla |
| **Limpieza y sanitización post-producción** | Propia, tercerizada o híbrida | Ventana post-producción | Dotación simultánea = ⌈m² de proceso × factor de automatización ÷ (60 / 40 / 25 m²/persona-h) ÷ ventana⌉ |

### 2.3 Unidades de la limpieza post-producción (escenario de referencia, media; ventana de 4,0 h)

| Escala | Modalidad | **Dotación simultánea** | **Horas-persona/día** | **FTE equivalentes** (h-p ÷ 8): internos · tercerizados | Horas contratadas/día | Puestos equivalentes internos | **Headcount contractual** |
|---|---|---|---|---|---|---|---|
| 2.500 | propia | 7 | 28 | 3,5 · 0 | 0 | 7 | PENDIENTE |
| 2.500 | tercerizada | 7 | 28 | 0 · 3,5 | 28 | 0 | PENDIENTE |
| 2.500 | híbrida | 7 | 28 | 1,5 · 2,0 | 16 | 3 | PENDIENTE |
| 5.000 | propia | 11 | 44 | 5,5 · 0 | 0 | 11 | PENDIENTE |
| 5.000 | tercerizada | 11 | 44 | 0 · 5,5 | 44 | 0 | PENDIENTE |
| 5.000 | híbrida | 11 | 44 | 2,0 · 3,5 | 28 | 4 | PENDIENTE |
| 10.000 | propia | 19 | 76 | 9,5 · 0 | 0 | 19 | PENDIENTE |
| 10.000 | tercerizada | 19 | 76 | 0 · 9,5 | 76 | 0 | PENDIENTE |
| 10.000 | híbrida | 19 | 76 | 3,0 · 6,5 | 52 | 6 | PENDIENTE |
| 20.000 | propia | 35 | 140 | 17,5 · 0 | 0 | 35 | PENDIENTE |
| 20.000 | tercerizada | 35 | 140 | 0 · 17,5 | 140 | 0 | PENDIENTE |
| 20.000 | híbrida | 35 | 140 | 5,5 · 12,0 | 96 | 11 | PENDIENTE |

Rango de dotación simultánea (alta–media–baja): 5–7–11 / 7–11–18 / 12–19–30 / 21–35–59.

**Lecturas:**

1. **35 personas durante 4 h = 140 horas-persona = 17,5 FTE**, no 35 FTE (test R16). Cuántas personas hay que contratar depende del esquema laboral (jornada parcial, jornada completa con otras tareas, limpieza por sectores que alargue la ventana): **headcount contractual PENDIENTE** (DPV-091).
2. **Tercerizar no hace desaparecer el recurso:** las 140 horas-persona pasan de FTE interno a **servicio tercerizado / horas contratadas** (test R17), y la cuadrilla sigue presente en el sitio (cuenta para vestuarios). Se mantienen internos el supervisor de saneamiento / verificación POES y la limpieza operativa en turno.
3. **Limpieza por sectores** (empezar cada sala cuando termina) alarga la ventana efectiva y reduce la dotación simultánea sin cambiar las horas-persona; cambia el pico de vestuarios. Pregunta prioritaria de campo.
4. **Nocturnidad:** una cuadrilla que trabaja de noche puede caer en régimen de jornada nocturna (`[PVDP]`); el convenio puede fijar condiciones (DPV-146).

### 2.4 Propia vs tercerizada vs híbrida (sin elección)

| Criterio | Propia | Tercerizada | Híbrida |
|---|---|---|---|
| Control del resultado | ▲ directo | ● por contrato; la responsabilidad ante SENASA y clientes sigue siendo de la empresa | ▲ en equipos críticos |
| Conocimiento de equipos (desarme) | ▲ | ▼ salvo personal estable del contratista | ▲ |
| Rotación y capacitación | La absorbe la empresa | La absorbe el contratista; riesgo de rotación | Repartida |
| Flexibilidad ante cambios | ● | ▲ | ▲ |
| Químicos y efluentes | Propios | Del contratista (compatibilidad con efluentes, DPV-112) | Mixto |
| Riesgo de inocuidad | ● | ▼ si el contrato premia rapidez | ● |

## 3. Otros servicios de soporte

| Servicio | Tratamiento en el modelo | Pendiente |
|---|---|---|
| **Higiene y seguridad laboral y medicina del trabajo** | Servicio externo en todas las escalas (horas **PENDIENTES**); técnico interno desde 10.000 | Horas-profesional por cantidad de trabajadores y riesgo (Ley 19.587, Decreto 1338/96, `[PVDP]`; DPV-149) |
| **Lavandería y ropería por zona** | 0,5 → 2 FTE internos | Propio vs tercerizado (DEC-073) |
| **Seguridad patrimonial y portería** | No modelada (habitualmente tercerizada) | Puestos según sitio |
| **Utilities y PTE** | Dentro de la cobertura técnica (3.er técnico simultáneo desde 10.000) | Operador de PTE según tecnología (DEC-043) |
| **Laboratorio de autocontrol** | Servicio externo por análisis (no por horas) | DEC-065 |
