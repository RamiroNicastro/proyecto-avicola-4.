# Turnos, jornada, presencia y productividad

**Fecha:** 2026-10-01 · **Versión:** 1.1 (sesión 14A; auditoría de unidades laborales) · Fase 0

> **Pregunta:** ¿cuántas horas netas de faena caben en la jornada de una cuadrilla y en las 24 h del establecimiento, quién está presente en cada momento y cómo se mide la productividad sin elegir un único KPI?
> **Integra** la ecuación de 24 h de 09A ([`../05_proceso_industrial/modelo_capacidad_proceso.py`](../05_proceso_industrial/modelo_capacidad_proceso.py), `ventana_24h`) **sin modificarla** (test R12). **No** se asume que dos turnos sean viables ni se elige organización horaria (DEC-036, DEC-14A-03).
> **v1.1:** se eliminaron las "horas extra" calculadas por el modelo y el tope de 30 h/mes como restricción. El modelo informa una **brecha de jornada**; cómo se organiza esa brecha (turnos, relevos, escalonamiento, personal adicional, horas extraordinarias u otra forma) **no** está demostrado y depende del convenio, la legislación y la forma de contratación (DPV-14A-01).
> **Clasificación:** presencia y brecha `[ESTIMACIÓN]`; jornada de referencia de 8 h `[PVDP]` (FTE-14A-001); D, pausas y limpieza intermedia `[SUPUESTO]` de sensibilidad (SUP-061, SUP-062).

---

## 1. Horas de línea funcionando ≠ horas de presencia de cada puesto

| Concepto | Qué es | Quién |
|---|---|---|
| **Horas netas de producción** | Tiempo en que la línea recibe aves (h) | La línea |
| **Presencia de la cuadrilla de línea** | h_c / D + pausas + limpieza intermedia (+ 0,25 h de traspaso con 2 cuadrillas) | Directos, supervisión de línea, QC, limpieza operativa |
| **Activos en marcha** | Preparación + producción + cierre | Técnicos de cobertura |
| **Ventana post-producción** | Limpieza + sanitización | Cuadrilla de limpieza (propia o tercerizada) |
| **Ventana de mantenimiento** | Preventivo diario | Técnico de guardia, especialistas |
| **Jornada diurna** | 8 h desde el fin de la preparación | Jefaturas, QA, logística, administración, dirección |

No toda persona está presente en todas las ventanas: la preparación, el cierre, la limpieza y el mantenimiento los cubren **otros equipos**.

## 2. Jornada de referencia: incompatibilidad, no "horas extra"

**Con la parametrización actual, una sola cuadrilla bajo una jornada de referencia de 8 h no puede cubrir 8 h netas de producción más todas las ventanas auxiliares sin una organización adicional.** La presencia requerida es ~10 h (9,97 h en el escenario medio). La diferencia (≈2 h por persona y por día) es una **brecha a organizar**, que podría resolverse con:

- dos cuadrillas o turnos escalonados;
- relevos para pausas sin detener la línea;
- personal adicional que cubra el arranque o el cierre;
- jornada extendida u horas extraordinarias, **si el convenio y la ley lo permiten** (DPV-14A-01; referencias legales `[PVDP]` FTE-14A-001/002, sin usarse como restricción del modelo);
- otra organización (horas netas menores, 6 días con menos horas, etc.).

**Horas netas que entran en la jornada de referencia sin organización adicional** (sensibilidades de 09A):

| Escenario (D) | 1 cuadrilla en 8 h | 2 cuadrillas en 8 h cada una | Ecuación de 24 h (09A) |
|---|---|---|---|
| Optimista (0,95) | **7,0 h** | **13,5 h** | 16,6 h |
| Media (0,90) | **6,4 h** | **12,4 h** | 13,8 h |
| Conservadora (0,85) | **5,9 h** | **11,4 h** | 10,0 h |

**Tensiones registradas (no resueltas):** T-14A-1 — la referencia de 8 h netas de 23/05/12B (SUP-053) implica una organización adicional para el personal de línea; T-14A-2 — "16 h = 2 × 8 h netas" choca con la jornada de referencia (presencia de 10,2 h por cuadrilla) y con la ecuación de 24 h (holgura +0,9 / −2,8 / −8,3 h). Dos cuadrillas dentro de la jornada de referencia dan ~11,4–13,5 h netas.

## 3. Matriz conceptual de presencia

Cada puesto tiene **ingreso → duración → salida** y se superpone con otros equipos. Ejemplo: 10.000 aves/día, escenario medio (horas desde el inicio de la preparación).

**Una cuadrilla, 8 h netas (escenario de referencia):**

| Puesto / equipo | Ingreso | Duración | Salida | Simultáneos | Solapamiento |
|---|---|---|---|---|---|
| Técnicos de cobertura | 0,00 | 11,47 | 11,47 | 3 | Con preparación, línea, cierre |
| Cuadrilla de línea (directos, supervisión, QC, limpieza operativa) | 0,75 | 9,97 | 10,72 | 44 | Con jornada diurna |
| Jornada diurna (jefaturas, QA, logística, administración, dirección) | 0,75 | 8,00 | 8,75 | 25 | Con línea |
| Cuadrilla de limpieza post-producción | 11,47 | 4,00 | 15,47 | 19 | Con técnico de guardia |
| Técnico de guardia (limpieza y mantenimiento) | 11,47 | 5,00 | 16,47 | 1 | Con limpieza |

Pico en sitio: **72** personas a la hora 0,75 (línea 44 + diurna 25 + técnicos 3).

**Dos cuadrillas de 6 h netas (12 h/día):** la cuadrilla 1 entra a las 0,75 y sale a las 8,48; la cuadrilla 2 entra a las 8,23 (0,25 h de traspaso) y sale a las 15,95; limpieza de 16,70 a 20,70; mantenimiento hasta 21,70. Pico en sitio: **96** a la hora 8,25 (las dos cuadrillas en el traspaso más la jornada diurna). **El pico ocurre en el cambio de turno**: es el dato que define vestuarios y circuitos de cambio.

La matriz se genera para cada escenario (`modelo_rrhh.matriz_presencia`; `--detalle 10000`). Supuestos de horario (diurna desde el fin de la preparación; limpieza sin solaparse con la línea) en SUP-14A-18; una limpieza por sectores que empiece antes cambia el pico.

## 4. Turnos por escala

Automatización de referencia de 09A, config. B, propios, productividad media.

| Escala | Modo | h netas | Cuadrillas | Presencia por cuadrilla (h) | Brecha (h/persona) | Horas-persona/día a organizar | Holgura 24 h (opt/med/cons) | Directos/turno | Simultáneos de producción | Pico en sitio | FTE totales | Alertas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 1 | 6 | 1 | 7,48 | 0 | 0 | 12,6/10,0/5,8 | 27 | 34 | 44 | 49,9 | — |
| 2.500 | extendido | 8 | 1 | 9,97 | 1,97 | 59 | 10,3/7,5/3,1 | 24 | 31 | 41 | 55,5 | JORNADA EXTENDIDA A VALIDAR |
| 2.500 | 2 | 12 | 2 | 7,73 | 0 | 0 | 5,5/2,2/−2,9 | 20 | 27 | 63 | 68,7 | — |
| 2.500 | 2 | 16 | 2 | 10,22 | 2,22 | 111 | 0,9/−2,8/−8,3 | 19 | 26 | 51 | 81,5 | 24 H; INCOMPATIBILIDAD DE JORNADA |
| 5.000 | 1 | 6 | 1 | 7,48 | 0 | 0 | 12,6/10,0/5,8 | 41 | 49 | 67 | 75,6 | — |
| 5.000 | extendido | 8 | 1 | 9,97 | 1,97 | 75 | 10,3/7,5/3,1 | 32 | 40 | 58 | 78,1 | JORNADA EXTENDIDA A VALIDAR |
| 5.000 | 2 | 12 | 2 | 7,73 | 0 | 0 | 5,5/2,2/−2,9 | 26 | 35 | 86 | 94,8 | — |
| 5.000 | 2 | 16 | 2 | 10,22 | 2,22 | 133 | 0,9/−2,8/−8,3 | 23 | 32 | 62 | 108,0 | 24 H; INCOMPATIBILIDAD DE JORNADA |
| 10.000 | 1 | 6 | 1 | 7,48 | 0 | 0 | 12,6/10,0/5,8 | 46 | 57 | 82 | 98,4 | — |
| 10.000 | extendido | 8 | 1 | 9,97 | 1,97 | 87 | 10,3/7,5/3,1 | 38 | 47 | 72 | 100,8 | JORNADA EXTENDIDA A VALIDAR |
| 10.000 | 2 | 12 | 2 | 7,73 | 0 | 0 | 5,5/2,2/−2,9 | 27 | 37 | 96 | 111,1 | — |
| 10.000 | 2 | 16 | 2 | 10,22 | 2,22 | 133 | 0,9/−2,8/−8,3 | 23 | 33 | 63 | 122,9 | 24 H; INCOMPATIBILIDAD DE JORNADA |
| 20.000 | 1 | 6 | 1 | 7,48 | 0 | 0 | 12,6/10,0/5,8 | 45 | 59 | 96 | 129,4 | — |
| 20.000 | extendido | 8 | 1 | 9,97 | 1,97 | 91 | 10,3/7,5/3,1 | 38 | 50 | 87 | 128,9 | JORNADA EXTENDIDA A VALIDAR |
| 20.000 | 2 | 12 | 2 | 7,73 | 0 | 0 | 5,5/2,2/−2,9 | 28 | 40 | 113 | 138,1 | — |
| 20.000 | 2 | 16 | 2 | 10,22 | 2,22 | 142 | 0,9/−2,8/−8,3 | 25 | 36 | 73 | 150,3 | 24 H; INCOMPATIBILIDAD DE JORNADA |

"1 turno con 8 h netas" da las mismas horas que "extendido con 8 h" (test R18): sólo cambia la alerta (INCOMPATIBILIDAD DE JORNADA vs JORNADA EXTENDIDA A VALIDAR). Todas las combinaciones están en [`escenarios_rrhh.csv`](escenarios_rrhh.csv) (`presencia_cuadrilla_h`, `brecha_jornada_h_persona`, `horas_persona_brecha_dia`, `holgura_24h`, `pico_personas_en_sitio`, `alertas`).

**Lecturas:**

1. **Más horas netas con la misma cuadrilla:** menos puestos por turno (la línea corre más lento), FTE casi iguales (la carga de trabajo no desaparece) y más horas-persona a organizar por encima de la jornada.
2. **Dos cuadrillas de 6 h netas** caben en la jornada de referencia y, salvo en el escenario conservador, en las 24 h; requieren más FTE (supervisión, jefes de turno, técnicos en ambos turnos) y **elevan el pico en sitio** por el traspaso (p. ej., 72 → 96 a 10.000).
3. **Dos cuadrillas de 8 h netas** muestran alertas de jornada y de 24 h salvo en el escenario optimista: no se descartan, pero exigen demostrar en plantas reales limpieza más corta o por sectores (DPV-091) y una organización laboral admitida (DPV-082, DPV-14A-01).

## 5. Productividad: indicadores con denominador declarado

Escenario de referencia; productividad media (entre paréntesis, alta–baja). Ningún valor es un benchmark argentino.

| Indicador | Denominador | Universo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|---|
| **Aves / hora-persona directa** (preferido) | Horas-persona/día de puestos directos | Directos (sin limpieza) | 10,4 (12,4–7,6) | 15,7 (19,5–10,7) | 26,4 (38,9–18,3) | 52,8 (87,2–35,9) |
| kg comestible / hora-persona directa | Ídem | Directos; peso comercial | 25 (30–18) | 38 (47–26) | 63 (93–44) | 127 (209–86) |
| Aves / hora-persona total | Horas-persona/día internas + tercerizadas calculadas | Toda la empresa sin PENDIENTES ni inspección oficial | 5,6 (6,8–4,1) | 8,0 (9,7–5,7) | 12,4 (16,2–8,7) | 19,4 (26,6–12,9) |
| FTE directos / 1.000 aves/día | 1.000 aves faenadas/día | FTE directos | 12,0 (10,1–16,4) | 8,0 (6,4–11,7) | 4,7 (3,2–6,8) | 2,4 (1,4–3,5) |
| FTE totales / 1.000 aves/día | Ídem | FTE internos + tercerizados | 22,2 (18,3–30,2) | 15,6 (12,9–21,9) | 10,1 (7,7–14,3) | 6,4 (4,7–9,7) |
| FTE indirectos / FTE directos | FTE directos | Internos + tercerizados; **informativo, no dimensiona** | 0,86 (0,82–0,84) | 0,96 (1,02–0,87) | 1,13 (1,40–1,10) | 1,72 (2,28–1,80) |
| Directos por supervisor | Supervisores de línea por turno | Puestos por turno | 12 (22–15) | 16 (28–14) | 19 (28–13) | 19 (25–13) |
| Equipos por FTE de mantenimiento | FTE de mantenimiento interno + tercerizado | Unidades de equipo (08) | 26 (36–11) | 18 (21–11) | 13 (15–8) | 11 (15–5) |

**Reglas:** (1) no comparar ratios con universos distintos (directos vs total; con o sin limpieza, mantenimiento o choferes tercerizados); (2) mirar al menos un indicador de línea, uno de organización y uno de estructura; (3) "personas por 1.000 aves" sólo con la unidad declarada (FTE, puestos o headcount), nunca mezcladas.

## 6. Automatización

**Resultados del modelo basados en sus supuestos, no ahorro industrial validado.** El modelo trabaja **por tarea** (colgado, descarga, faena, evisceración, enfriamiento, clasificación, trozado, deshuese, empaque, cámaras, subproductos), cada una con su coeficiente por nivel (M / Mc / S / A; SUP-14A-04/05). Dos factores son **supuestos de sensibilidad genéricos**, no tareas medidas: el factor de limpieza por automatización (1,0 / 1,0 / 1,1 / 1,25) y la fracción interna de la limpieza híbrida (30 %).

Mismo escenario (1 cuadrilla, 8 h netas, config. B, propios, media): directos/turno · FTE totales · FTE de mantenimiento · pico en sitio.

| Escala | Manual | Mecanizado | Semiautomático | Automático |
|---|---|---|---|---|
| 2.500 | 24 · 54,7 · 2,3 · 41 | 23 · 53,5 · 2,3 · 40 | 18 · 47,0 · 3,4 · 34 | 16 · 47,1 · 5,4 · 32 |
| 5.000 | 36 · 82,3 · 3,5 · 62 | 32 · 77,3 · 3,5 · 58 | 23 · 66,6 · 3,5 · 49 | 19 · 63,0 · 5,6 · 44 |
| 10.000 | 62 · 130,9 · 4,9 · 98 | 56 · 122,9 · 4,9 · 91 | 38 · 99,3 · 4,9 · 72 | 25 · 85,5 · 6,4 · 60 |
| 20.000 | 115 · 223,2 · 4,9 · 167 | 102 · 205,7 · 4,9 · 153 | 65 · 156,6 · 4,9 · 114 | 38 · 125,8 · 7,5 · 87 |

Puestos por tarea a 20.000 aves/día, manual → automático: colgado 3 → 3 (no cambia); descarga 2 → 1; faena 7 → 3; **evisceración 35 → 8**; clasificación 4 → 1; **trozado 30 → 8**; **empaque 25 → 7**; cámaras 4 → 4; subproductos 4 → 2. A 2.500: evisceración 6 → 3; trozado 5 → 2; empaque 4 → 2; el resto no cambia.

| Efecto | Dónde | En el modelo |
|---|---|---|
| **Reduce operadores** | Evisceración, trozado, empaque, clasificación, faena, descarga | Directos/turno −33 % (2.500) a −67 % (20.000), resultado de los coeficientes supuestos |
| **No reduce** | Colgado (manual en todos los niveles), cámaras, enfriamiento | Puestos iguales |
| **Aumenta mantenimiento** | Carga por activos y, en automático ≥ 10.000, un técnico más de cobertura | FTE de mantenimiento +1,5 a +3,1 (test R03: nunca baja) |
| **Aumenta automatización/control** | PLC, balanzas de línea, calibración | Especialista en automatización en la política de cobertura |
| **Cambia perfiles** | De operario de cuchillo a operador, repaso, trimming, control | Puestos fijos por tarea (operadores de máquina) |
| **Crea dependencia** | Equipos críticos, repuestos, servicio técnico local (DPV-089) | Cualitativo ([`../08_maquinaria/catalogo_equipos.md`](../08_maquinaria/catalogo_equipos.md) §2) |

En 2.500 aves/día, pasar de semiautomático a automático no reduce FTE (47,0 → 47,1): el ahorro de operadores se compensa con mantenimiento y limpieza de equipos. Nada de esto decide DEC-037.
