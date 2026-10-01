# Conclusiones — recursos humanos y organización

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 14A, en paralelo con 14B) · Base: [`estructura_organizacional.md`](estructura_organizacional.md), [`dotacion_por_escala.md`](dotacion_por_escala.md), [`turnos_y_productividad.md`](turnos_y_productividad.md), [`mantenimiento_y_servicios.md`](mantenimiento_y_servicios.md), [`calidad_inocuidad.md`](calidad_inocuidad.md), [`modelo_rrhh.py`](modelo_rrhh.py), [`escenarios_rrhh.csv`](escenarios_rrhh.csv), [`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv), [`guia_ramiro.md`](guia_ramiro.md)

> **Pregunta central:** ¿qué personas necesita la empresa, dónde trabajan, en qué turnos y cómo cambia la estructura al crecer de 2.500 a 20.000 aves/día?
> **No** se elige escala, automatización, turnos, modalidad de limpieza, mantenimiento ni flota; **no** se calcula OPEX laboral (la plantilla de costos está vacía). Registros centrales **no** modificados: propuestas en [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md).
> **Calidad de la evidencia:** ninguna productividad, ausentismo ni dotación proviene de plantas argentinas; dos referencias extranjeras débiles `[PVDP]` y coeficientes `[SUPUESTO]` de rango. Todas las cifras son `[ESTIMACIÓN]`.

---

## 1. Estructura organizacional

Seis bloques: **operación industrial** (recepción/colgado, faena, evisceración, enfriamiento, trozado/deshuese, empaque, cámaras/expedición, subproductos, limpieza y sanitización), **soporte industrial** (mantenimiento mecánico, eléctrico, frío, utilities, automatización; calidad, inocuidad, laboratorio; HyS; lavandería), **logística** (planificación, depósito, expedición; choferes sólo con flota propia), **producción primaria** (sólo coordinación de integrados, veterinaria, técnicos de campo, planificación; sin personal de granjas de terceros), **administración** (compras, ventas, administración, finanzas, RR. HH., sistemas) y **dirección** (general, operaciones, comercial, adm./finanzas, calidad). La inspección oficial (SENASA) es externa y su dotación queda PENDIENTE.

Tres niveles de organigrama ([`estructura_organizacional.md` §3](estructura_organizacional.md)): **asset-light** (faena a façon; 11–36 personas), **planta pequeña/media** (roles combinados; jefaturas que aparecen a 5.000 y 10.000) y **planta escalada** (gerencias de calidad y adm./finanzas, especialista en automatización, jefes de turno si hay dos cuadrillas). Dirección crece de 2 a 5 personas; no se agregan capas sin evidencia.

## 2. Dotación por escala

Escenario de referencia (1 cuadrilla, 8 h netas en turno extendido, automatización de referencia de 09A, config. B, propios), productividad alta–**media**–baja:

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Directos por turno | 22–**24**–30 | 28–**33**–44 | 29–**38**–51 | 26–**39**–52 |
| Personas en planta por turno de producción | 28–**31**–37 | 35–**41**–53 | 37–**47**–63 | 36–**51**–67 |
| Total personas internas | 57–**64**–82 | 78–**91**–118 | 92–**115**–154 | 114–**151**–215 |
| Total equivalentes internos | 42–**55**–80 | 60–**79**–117 | 72–**100**–153 | 87–**128**–204 |
| Personas por 1.000 aves/día | 25,6 | 18,2 | 11,5 | 7,5 |

Escala ×8 → personas ×2,4. Asset-light: 11 / 19 / 25 / 36 personas internas.

## 3. Directos vs indirectos

Indirecta/directa (equivalentes): **0,85 / 0,92 / 1,11 / 1,64**. El soporte es el bloque que más crece (22 → 78 personas), sobre todo limpieza post-producción (8 → 40) y mantenimiento. La relación sube con la escala y con la automatización: no es ineficiencia, es trabajo trasladado de la línea a equipos que hay que mantener, limpiar y controlar. Supervisión: 4–5 personas con una cuadrilla (12–20 directos por supervisor).

## 4. Turnos

- **8 h netas no caben en una jornada de 8 h:** la presencia de la cuadrilla es ~10 h → turno extendido con ~43 h extra/persona-mes (por encima del tope de referencia de 30 h, `[PVDP]`). En jornada normal una cuadrilla rinde **~6–7 h netas**.
- **Dos cuadrillas sin horas extra dan ~11,4–13,5 h netas, no 16 h;** a 16 h hay alerta de jornada y de la ecuación de 24 h (holgura +0,9 / −2,8 / −8,3 h). No se descarta ningún modo: son alertas con sensibilidades sin dato argentino.
- Más horas netas con la misma gente reduce personas pero no equivalentes (la mano de obra se concentra en horas extra). Dos cuadrillas de 6 h cuestan +23 % de personas a 2.500 y −1 % a 20.000 frente a una cuadrilla de 6 h.
- Tensiones registradas para la reconciliación: T-14A-1 (SUP-053, 8 h netas) y T-14A-2 (16 h = 2 × 8).

## 5. Automatización

De manual a automático (misma escala, mix y turnos): directos por turno −33 % a 2.500 y −66 % a 20.000; técnicos de mantenimiento +1,3 a +3,1 equivalentes; indirecta/directa 0,56 → 1,64 a 20.000. Total de personas: 64 → 59 (2.500), 96 → 79 (5.000), 144 → 103 (10.000), 235 → 151 (20.000). **Reduce tareas** (evisceración 35 → 8 puestos por turno a 20.000), **cambia perfiles** (operario de cuchillo → operador, repaso, control), **aumenta la necesidad técnica** (test R03: nunca reduce técnicos) y **crea dependencia de mantenimiento** (equipos críticos, repuestos y servicio técnico local no verificados). En 2.500 aves/día casi no ahorra personas.

## 6. Mantenimiento

Hasta 10.000 aves/día la dotación técnica la fija la **cobertura presencial** (un técnico en planta mientras la línea corre: 2,0 / 3,3 / 4,5 equivalentes); a 20.000 automático la fija la **carga de activos** (7,5 equivalentes; rango 3,3–17,1). Propio, tercerizado y mixto comparados sin elección: la tercerización deja siempre un coordinador interno; el mixto (cobertura propia + especialistas en frío, PLC, media tensión) es el que menos riesgo de respuesta tiene en escalas chicas, pero depende de que existan contratistas (DPV-089).

## 7. Limpieza

Función crítica (POES, APPCC, ventana de 24 h). Cuadrilla post-producción simultánea de **5–11 personas a 2.500 y 21–59 a 20.000**, con pocas horas cada una (40 personas ≈ 17 equivalentes a 20.000 en el escenario medio). Tercerizar baja la nómina interna (151 → 110 personas a 20.000) sin cambiar el trabajo; la verificación POES y la limpieza operativa en turno siguen internas. Es el **bloque más incierto**: depende de m² (proxy de 12C), complejidad de equipos y de si se limpia por sectores (DPV-14A-06).

## 8. Principales datos faltantes

1. **Dotación y productividad reales** por área en 2–3 plantas argentinas comparables (DPV-14A-04, DPV-092).
2. **Convenio colectivo aplicable**: jornada, turnos, horas extra, nocturnidad (DPV-14A-01, DPV-082).
3. **Organización real de la limpieza** (DPV-14A-06, DPV-091).
4. **Inspección oficial**: inspectores y auxiliares por línea, quién los aporta y paga (DPV-14A-05, DPV-090).
5. **Costo laboral** por categoría para completar la plantilla (DPV-14A-03).
6. **Técnicos y mano de obra por corredor** (DPV-14A-08, DPV-121).
7. **Ausentismo y rotación** (DPV-14A-02); **mantenimiento real** (DPV-14A-10); **HyS** (DPV-14A-07); **captura** (DPV-14A-09).

## 9. Tests

`python3 18_recursos_humanos/modelo_rrhh.py --solo-tests` → **15/15**; `--mutaciones` → **8/8 detectadas**.

| Test | Qué valida |
|---|---|
| R01 | Dotación nunca negativa |
| R02 | Más escala no reduce personal (total y por grupo) con el mismo nivel de automatización, mix y turnos |
| R03 / R03b | La automatización no reduce técnicos; sí reduce directos |
| R04 | Tercerizar limpieza, mantenimiento o flota retira personal interno, conserva el tamaño de la función y su responsable interno; asset-light sin directos internos pero con la función de faena externa |
| R05 | Turnos con la holgura de 09A idéntica y alertas de 24 h y de jornada siempre explícitas |
| R06 | Escenarios independientes (sin estado compartido ni mutación de entradas o parámetros) |
| R07 | Datos faltantes quedan PENDIENTE (choferes, inspección oficial, HyS, costos vacíos) |
| R08 | Entradas inválidas rechazadas |
| R09–R11 | Personas ≥ puestos × cuadrillas; agregados consistentes; KPI múltiples |
| R12 | 09A intacto (horas netas máximas 16,57 / 13,77 / 10,00) |
| R13 | Rangos ordenados (alta ≤ baja, total y por puesto) |
| R14 | Mix: sala limpia A ≤ B ≤ C |

Mutaciones detectadas: rangos invertidos, automatización que reduce mantenimiento, cobertura < 1, coeficiente negativo, mix invertido, faltantes rellenados, alertas silenciadas, tercerización que borra la función.

## 10. Archivos

**Creados** en `18_recursos_humanos/`: `estructura_organizacional.md`, `dotacion_por_escala.md`, `turnos_y_productividad.md`, `mantenimiento_y_servicios.md`, `calidad_inocuidad.md`, `modelo_rrhh.py`, `escenarios_rrhh.csv` (15.576 escenarios), `plantilla_costo_laboral.csv` (estructura de costo con columnas de costo vacías), `guia_ramiro.md`, `conclusiones_rrhh.md`, `actualizaciones_gestion_14A.md`, `fuentes_14A.csv`. **Modificado:** `18_recursos_humanos/README.md`. **Sin cambios:** `00_gestion_proyecto/`, `25_fuentes/`, archivos de 14B y todos los modelos importados (05/09A, 09/12C, 13/12B, 23).

## 11. Limitaciones

1. Ningún coeficiente es un dato argentino; el rango alta–baja (×1,4–1,9 en el total) es el resultado honesto, no un defecto.
2. La limpieza depende de m² de 12C, que son a su vez proxy; la ventana de limpieza de 09A no varía todavía con escala ni automatización (`t_limpieza` provisional).
3. El factor de cobertura no distingue días de operación (6 días/semana sólo genera alerta de horas extra).
4. Choferes de producto, inspección oficial, servicio externo de HyS y cuadrillas de captura quedan PENDIENTES (no sumados).
5. La estructura por bandas es un supuesto organizacional; ventas depende de canales y clientes, no de aves.
6. Sin costos: la conveniencia de automatizar, tercerizar o sumar un turno no puede evaluarse todavía.

## 12. Evaluación de calidad

- [x] Estructura completa sin duplicar personal de granjas de terceros; no se infla la estructura chica (roles compartidos).
- [x] Dotación por escala con personas por turno, personas físicas, equivalentes, supervisión y soporte compartido, en rango.
- [x] Turnos integrados a la ecuación de 24 h de 09A (idéntica, test R05/R12) y a la jornada; dos turnos no asumidos viables.
- [x] KPI múltiples con reglas de uso; ninguno como verdad.
- [x] Automatización, mantenimiento y limpieza con sus efectos y modalidades sin elección.
- [x] Faltantes no rellenados; costos vacíos.
- [ ] Datos de plantas argentinas, convenio y costos.

**Evaluación: MEDIA** como modelo organizacional y método (funciones completas, trazabilidad a 09A, 12B, 12C y 08, alertas de jornada y 24 h, tests y mutaciones); **BAJA** como evidencia de dotación real. Sirve para saber qué preguntar en las visitas y para alimentar con estructura (no con costos) a OPEX, layout y CAPEX.
