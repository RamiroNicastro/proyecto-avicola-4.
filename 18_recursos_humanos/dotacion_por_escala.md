# Dotación por escala — 2.500 / 5.000 / 10.000 / 20.000 aves/día

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 14A) · Fase 0

> **Qué es:** órdenes de magnitud de personas por turno, personas físicas y equivalentes (FTE por horas) por escala, separados en directos, supervisión, soporte, administración y dirección, con rangos de productividad alta–media–baja. Fuente: [`modelo_rrhh.py`](modelo_rrhh.py) v1.0 y [`escenarios_rrhh.csv`](escenarios_rrhh.csv) (15.576 escenarios).
> **Qué no es:** una dotación validada ni un plan de contratación. **Ninguna productividad es un dato argentino medido**: los coeficientes son `[SUPUESTO]` de rango (SUP-14A-04 a SUP-14A-13) y dos referencias extranjeras débiles `[PVDP]` (colgado FTE-219; eviscerado manual FTE-218). Todas las cifras son `[ESTIMACIÓN]`.
> **No** se elige escala, automatización, turnos ni modalidades; **no** se calculan costos.

---

## 1. Definiciones

| Término | Definición |
|---|---|
| **Puesto por turno** | Posición ocupada simultáneamente en una cuadrilla de producción |
| **Cuadrilla** | Equipo que cubre un turno de producción (1 en "1 turno" y "turno extendido"; 2 en "2 turnos") |
| **Personas (físicas)** | ⌈puestos × cuadrillas × factor de cobertura⌉; el factor (1,08 / 1,12 / 1,18, SUP-14A-03) cubre ausentismo, vacaciones y licencias |
| **Equivalentes (FTE)** | Horas trabajadas ÷ horas normales semanales (48 / 45 / 44, `[PVDP]` / SUP-14A-03) × cobertura: incluye las horas extra como fracción de persona |
| **Directos** | Operación industrial de recepción a expedición y subproductos (no incluye limpieza) |
| **Supervisión** | Supervisores de línea, jefes de turno, jefe de producción, supervisor de saneamiento |
| **Soporte** | Limpieza y sanitización, calidad, mantenimiento, logística, producción primaria, HyS, lavandería |
| **Indirectos** | Supervisión + soporte + administración + dirección |
| **Rol compartido** | Fracción de un rol (p. ej. 0,5) que se acumula con otra fracción en una misma persona |
| **PENDIENTE** | Dato faltante que el modelo **no rellena**: inspección oficial, servicio externo de HyS, choferes de producto, cuadrillas de captura |

## 2. Escenario de referencia por escala

**Escenario de referencia (no es decisión):** 1 cuadrilla con 8 h netas de faena en **turno extendido** (la presencia resultante, ~10 h, no entra en una jornada normal de 8 h; ver [`turnos_y_productividad.md`](turnos_y_productividad.md) §2), automatización de referencia de 09A por escala (manual / mecanizado / semiautomático / automático; DEC-037 abierta), configuración B (trozado), limpieza y mantenimiento propios, flota de aves de terceros con 5.500 aves/camión **de escenario** (SUP-033), abastecimiento por integración, laboratorio externo, 5 días/semana. Rango: productividad alta–**media**–baja.

| Concepto | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Automatización de referencia (09A, no decisión) | manual | mecanizado | semiautomático | automático |
| Ritmo de línea (aves/h) | 312 | 625 | 1.250 | 2.500 |
| Directos por turno | 22–**24**–30 | 28–**33**–44 | 29–**38**–51 | 26–**39**–52 |
| Personas en planta por turno de producción (directos + supervisión de línea + calidad operativa + limpieza operativa + técnicos de guardia) | 28–**31**–37 | 35–**41**–53 | 37–**47**–63 | 36–**51**–67 |
| Cuadrilla de limpieza post-producción (simultánea, en otra franja) | 5–**7**–11 | 7–**11**–18 | 12–**19**–30 | 21–**35**–59 |
| Directos (personas) | 30–**32**–41 | 36–**42**–56 | 37–**48**–64 | 34–**47**–65 |
| Supervisión | 2–**4**–4 | 3–**4**–5 | 4–**5**–7 | 4–**5**–7 |
| Soporte | 19–**22**–30 | 29–**35**–46 | 37–**48**–67 | 56–**78**–120 |
| Administración | 4–**4**–5 | 7–**7**–8 | 10–**10**–12 | 15–**16**–18 |
| Dirección | 2–**2**–2 | 3–**3**–3 | 4–**4**–4 | 5–**5**–5 |
| **Total personas internas** | 57–**64**–82 | 78–**91**–118 | 92–**115**–154 | 114–**151**–215 |
| **Total equivalentes internos** | 42–**55**–80 | 60–**79**–117 | 72–**100**–153 | 87–**128**–204 |
| Externos equivalentes conocidos (choferes de aves de terceros) | 1,1 | 1,1 | 2,2 | 3,4 |
| Funciones PENDIENTES (no sumadas) | 4 | 4 | 4 | 4 |

**Lecturas:**

1. **El rango importa más que el punto medio:** entre productividad alta y baja la dotación total varía ~1,4–1,9 veces. Ninguna cifra central debe usarse como "la dotación" hasta tener datos de plantas (DPV-092, DPV-14A-04).
2. **La escala diluye la estructura:** de 2.500 a 20.000 aves/día (×8) la dotación total crece ~×2,4 (media). Personas por 1.000 aves/día: 25,6 → 7,5.
3. **Los directos casi se estancan entre 10.000 y 20.000** porque la referencia pasa de semiautomático a automático; con el **mismo** nivel de automatización los directos siempre crecen con la escala (test R02). La caída de 48 a 47 directos no es economía de escala: es automatización.
4. **El soporte es el bloque que más crece** (22 → 78): limpieza post-producción (8 → 40 personas), mantenimiento (3 → 8), logística, calidad y producción primaria. En 20.000 aves/día automático el soporte supera a los directos.
5. **Personas ≠ equivalentes:** la diferencia (64 vs 55 en 2.500; 151 vs 128 en 20.000) viene de la cuadrilla de limpieza, que trabaja una ventana de ~4 h (muchas personas, pocas horas), y de los roles compartidos. Si la limpieza se organiza por sectores o con jornada completa, las personas bajan y los equivalentes no (DPV-091, DPV-14A-06).
6. **La cuadrilla de limpieza es el dato más incierto** (5–59 personas simultáneas según escala y productividad): depende de m² de salas (12C, a su vez proxy), complejidad de equipos y duración de la ventana.

## 3. Personal por área (escenario de referencia, productividad media; puestos por turno · personas)

| Área | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Recepción, descarga y colgado | 2 · 3 | 3 · 4 | 3 · 4 | 5 · 6 |
| Faena | 2 · 3 | 2 · 3 | 3 · 4 | 3 · 4 |
| Evisceración (sin inspección oficial) | 6 · 7 | 10 · 12 | 9 · 11 | 8 · 9 |
| Enfriamiento y clasificación | 2 · 3 | 2 · 3 | 2 · 3 | 2 · 3 |
| Trozado (config. B) | 5 · 6 | 7 · 8 | 9 · 11 | 8 · 9 |
| Deshuese (config. B: no hay) | 0 | 0 | 0 | 0 |
| Empaque | 4 · 5 | 6 · 7 | 7 · 8 | 7 · 8 |
| Cámaras, congelado y expedición | 2 · 3 | 2 · 3 | 3 · 4 | 4 · 5 |
| Subproductos y decomisos | 1 · 2 | 1 · 2 | 2 · 3 | 2 · 3 |
| Limpieza operativa en turno | 2 · 3 | 2 · 3 | 2 · 3 | 3 · 4 |
| Limpieza y sanitización post-producción | 7 · 8 | 11 · 13 | 19 · 22 | 35 · 40 |
| Supervisores de línea + jefe de producción + saneamiento | 2 · 4 | 2 · 4 | 2 · 5 | 2 · 5 |
| Control de calidad operativo | 2 · 3 | 2 · 3 | 2 · 3 | 3 · 4 |
| QA/APPCC, trazabilidad, jefe de calidad (equivalentes) | 1,5 | 2,5 | 3 | 4 + gerente |
| Técnicos de mantenimiento (equivalentes) + jefe + pañol | 2,3 | 3,3 + 1 | 4,5 + 1 + 1 | 7,5 + 1 + 1 |
| Logística (planificación, depósito, expedición; eq.) | 1,0 | 2,5 | 3 | 6 |
| Producción primaria (coordinación, veterinaria, técnicos, planificación; eq.) | 2 | 3,5 | 5 | 7 |
| Administración (eq.) | 4 | 7 | 10 | 15,5 |
| Dirección | 2 | 3 | 4 | 5 |

Los cambios de 5.000 a 10.000 en evisceración y trozado (10 → 9; 7 → 9) reflejan el paso de mecanizado a semiautomático en la referencia. La tabla con el mismo nivel de automatización está en [`turnos_y_productividad.md`](turnos_y_productividad.md) §4.

## 4. Directos vs indirectos

Equivalentes, productividad media, escenario de referencia.

| Escala | Directos eq. | Indirectos eq. | Supervisión | Soporte | Administración | Dirección | Indirecta / directa |
|---|---|---|---|---|---|---|---|
| 2.500 | 29,8 | 25,3 | 3,5 | 15,8 | 4,0 | 2,0 | 0,85 |
| 5.000 | 40,9 | 37,7 | 3,5 | 24,2 | 7,0 | 3,0 | 0,92 |
| 10.000 | 47,1 | 52,4 | 4,5 | 34,0 | 10,0 | 4,0 | 1,11 |
| 20.000 | 48,4 | 79,3 | 4,5 | 54,3 | 15,5 | 5,0 | 1,64 |

Por bloque organizacional (equivalentes):

| Bloque | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Operación industrial (incluye limpieza y supervisión de línea) | 39,2 | 52,4 | 63,6 | 74,0 |
| Soporte industrial (calidad, mantenimiento, HyS, lavandería) | 6,8 | 10,3 | 14,0 | 20,2 |
| Logística | 1,0 | 2,5 | 3,0 | 6,0 |
| Producción primaria (coordinación) | 2,0 | 3,5 | 5,0 | 7,0 |
| Administración | 4,0 | 7,0 | 10,0 | 15,5 |
| Dirección | 2,0 | 3,0 | 4,0 | 5,0 |

**La relación indirecta/directa sube con la escala y con la automatización** (0,85 → 1,64). No es ineficiencia: es el efecto de reemplazar puestos de línea por equipos que hay que mantener, limpiar y controlar. Un indicador de "personas por ave" que sólo mire directos sobrestima el ahorro de automatizar.

## 5. Dónde trabajan: personas por turno por zona

Puestos simultáneos por turno de producción (productividad media; escenario de referencia). Insumo para vestuarios y circuitos de cambio de 12C (DPV-138).

| Zona | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Sucia (recepción, colgado, faena) | 4 | 5 | 6 | 8 |
| Evisceración | 6 | 10 | 9 | 8 |
| Limpia (enfriamiento, clasificación, trozado, empaque) | 11 | 15 | 18 | 17 |
| Frío y expedición | 2 | 2 | 3 | 4 |
| Subproductos | 1 | 1 | 2 | 2 |
| Transversal (supervisión, calidad, limpieza operativa, técnicos de guardia) | 7 | 8 | 9 | 12 |
| **Total por turno de producción** | **31** | **41** | **47** | **51** |
| Cuadrilla de limpieza post-producción (otra franja; usa los mismos vestuarios) | 7 | 11 | 19 | 35 |
| Roles de estructura en jornada diurna (jefaturas, QA, logística, campo, administración, dirección; personas) | 12 | 23 | 31 | 45 |
| *Proxy de 12C por turno (SUP-116, valor medio) — sólo comparación* | *49* | *82* | *115* | *165* |

**Tensión con 12C (registrada, no resuelta):** el proxy de dotación que 12C usó para vestuarios y comedor (SUP-116) da 1,6–3,2 veces las personas por turno de producción de este modelo. Para dimensionar vestuarios habría que usar el **máximo simultáneo por zona y por sexo** (turno de producción + solapamiento con limpieza + oficinas), no un proxy único. La reconciliación decide si se reemplaza el proxy; esta sesión **no modifica** 12C.

## 6. Asset-light (faena a façon)

| Escala equivalente | Personas internas (alta–media–baja) | Equivalentes internos | Externos eq. (incluye la dotación industrial del façonier) |
|---|---|---|---|
| 2.500 | 11 | 10,0 | 23 |
| 5.000 | 19 | 17,5 | 30 |
| 10.000 | 24–**25**–25 | 24,5 | 49 |
| 20.000 | 35–**36**–37 | 35,5 | 84 |

La empresa conserva comercial, abastecimiento (coordinación de integrados o compra), control de calidad propio en la planta del façonier, logística y administración. Ningún directo industrial es interno; la función de faena **existe** como externa (test R04). Su viabilidad depende de que exista un façonier con capacidad, habilitación y condiciones (DEC-004, DEC-018; sin investigar).

## 7. Sensibilidades principales (escenario de referencia, media)

| Escala | Mix A / B / C (total personas) | Choferes de aves con flota propia | Laboratorio propio | Compra de pollo vivo (sin integración) | 6 días/semana (personas · eq. · h extra/persona-mes) |
|---|---|---|---|---|---|
| 2.500 | 61 / 64 / 76 | 2 | 65 | 63 | 64 · 63,3 · 64 |
| 5.000 | 85 / 91 / 111 | 2 | 92 | 89 | 91 · 90,1 · 64 |
| 10.000 | 106 / 115 / 142 | 3 | 117 | 112 | 116 · 113,3 · 64 |
| 20.000 | 139 / 151 / 171 | 4 | 154 | 146 | 151 · 142,9 · 64 |

- **El mix pesa:** deshuesar (config. C) agrega 13–23 % de personas respecto de B, casi todas en sala limpia (test R14). La asignación de cada parte al mejor mercado (principio de ingreso total por ave) tiene costo de personal que deberá compararse con su ingreso.
- **Flota propia:** sólo choferes de aves vivas son calculables (2–4 con capacidad de escenario); choferes de producto quedan PENDIENTES. Con 12 t y 150 km **de escenario** serían 3–4 más (ilustrativo, no se usa).
- **Seis días con una cuadrilla** no agrega personas en el modelo pero eleva las horas extra a ~64 h/persona-mes: en la práctica exige más personas o rotación; queda como alerta.

## 8. Qué falta para que estas cifras sirvan para decidir

Dotación real por sector, productividad, ausentismo, turnos y horas extra, limpieza y mantenimiento de 2–3 plantas argentinas de escala comparable (guía en [`guia_ramiro.md`](guia_ramiro.md) §4 y [`../05_proceso_industrial/guia_visita_planta.md`](../05_proceso_industrial/guia_visita_planta.md)); convenio aplicable (DPV-14A-01); inspección oficial (DPV-14A-05); servicio de HyS (DPV-14A-07); oferta de mano de obra y técnicos por corredor (DPV-121, DPV-14A-08). Lista completa en [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md) §2.
