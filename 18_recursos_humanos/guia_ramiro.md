# Guía para Ramiro — personas, turnos y organización

**Fecha:** 2026-10-01 · Sesión 14A (v1.1, auditoría de unidades) · Lectura: 10 minutos

> Resumen práctico de [`conclusiones_rrhh.md`](conclusiones_rrhh.md). Los números son **órdenes de magnitud de un modelo con supuestos**, no datos de plantas argentinas. Sirven para saber qué preguntar.

---

## 1. Seis ideas para llevarse

1. **"Cuántas personas" son varias preguntas distintas.** ¿Cuántos puestos hay que cubrir en un turno? ¿Cuánta gente está en la planta al mismo tiempo? ¿Cuántas horas de trabajo hacen falta por día (FTE)? ¿Cuántas personas hay que tener en nómina? Las respuestas son distintas y no se suman. La última (nómina) todavía no se puede calcular: depende de francos, vacaciones, ausentismo y reemplazos.
2. **Una planta no es sólo la línea.** Mantenimiento, limpieza, calidad, logística y administración pesan cada vez más con la escala y con la automatización.
3. **Más automatización = menos operarios, más técnicos** (según los supuestos del modelo, no un ahorro probado). A 2.500 aves/día casi no ahorra trabajo.
4. **"8 horas netas de faena" no entra en una jornada de 8 horas** con paradas, pausas y limpieza intermedia: la gente de línea estaría ~10 h. Hay que organizarlo de otra forma (dos cuadrillas, relevos, escalonamiento, más personal o lo que permita el convenio). Dos cuadrillas no dan 16 h: dan ~11–13,5 h.
5. **La limpieza es un equipo grande que trabaja pocas horas:** a 20.000 aves/día, ~35 personas a la vez durante ~4 h = el trabajo de ~17,5 personas de jornada completa. Tercerizarla no hace desaparecer esas horas: se pagan como servicio.
6. **SENASA no es personal de la empresa.** Los inspectores oficiales no se cuentan en la nómina; cuántos son y si hay algún cargo está pendiente.

## 2. Órdenes de magnitud (escenario de referencia, media)

| | 2.500 aves/día | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Puestos en la planta mientras corre la línea | ~31 | ~40 | ~47 | ~50 |
| Máximo de personas en el sitio al mismo tiempo | ~41 | ~58 | ~72 | ~87 |
| Trabajo total (FTE de jornada completa) | ~55 | ~78 | ~101 | ~129 |
| Personas en nómina | **PENDIENTE** | **PENDIENTE** | **PENDIENTE** | **PENDIENTE** |
| Sin planta propia (faena a façon), FTE propios | ~10 | ~17 | ~25 | ~36 |

El vestuario se dimensiona con el **máximo de personas al mismo tiempo**, no con la nómina.

## 3. Cómo leer un organigrama chico

En 2.500 aves/día una persona hace varias cosas: el gerente general también vende y administra; el gerente de operaciones es jefe de producción; un técnico líder es el jefe de mantenimiento; contador, liquidación de sueldos y sistemas son externos. En el modelo eso aparece como "0,5" de un rol, no como una persona más.

## 4. Qué preguntar en las visitas a plantas (módulo RR. HH.)

Complementa [`../05_proceso_industrial/guia_visita_planta.md`](../05_proceso_industrial/guia_visita_planta.md) §2.1–2.4. Pedir **rangos**, nunca salarios individuales ni datos personales. **Siempre preguntar qué incluye cada número** (¿personas en nómina, presentes por turno, horas?).

| Tema | Preguntas | Para qué (ID) |
|---|---|---|
| **Dotación real** | ¿Cuántos puestos por sector y por turno? ¿Cuántas personas en nómina en total? ¿Qué parte es tercerizada? | DPV-14A-04, DPV-092 |
| **Presencia** | ¿A qué hora entra y sale cada grupo (línea, limpieza, mantenimiento, oficinas)? ¿Cuándo hay más gente en la planta? | Pico en sitio (SUP-14A-18) |
| **Productividad** | ¿Cuántas aves cuelga una persona por minuto? ¿Cuántos kg trocea o deshuesa por hora? ¿Cuántos puestos tiene la evisceración? | DPV-092 |
| **Cobertura de nómina** | ¿Cuántas personas en nómina por cada puesto a cubrir? ¿Ausentismo típico? ¿Cuántos reemplazos por turno? | FACTOR_COBERTURA_NOMINA (DPV-14A-02) |
| **Turnos y jornada** | ¿Cuántas horas netas faenan por turno? ¿Cómo cubren arranque, pausas y cierre? ¿Hacen horas extra, relevos o turnos escalonados? ¿Qué convenio aplica? | DPV-082, DPV-14A-01 |
| **Mantenimiento** | ¿Cuántos técnicos propios y por especialidad? ¿Hay un técnico en planta todo el tiempo que corre la línea? ¿Qué se terceriza? ¿Horas de preventivo por semana? | DPV-14A-10, DPV-089 |
| **Limpieza** | ¿Propia o tercerizada? ¿Cuántas personas a la vez y cuántas horas? ¿Limpian por sectores? ¿Jornada completa o parcial? | DPV-091, DPV-14A-06 |
| **Supervisión** | ¿Cuántos operarios por supervisor? ¿Hay jefe de turno? | DPV-14A-11 |
| **Inspección oficial** | ¿Cuántos inspectores oficiales por turno y por línea? ¿La planta aporta auxiliares o paga algún arancel? | DPV-14A-05 |
| **Mano de obra local** | ¿Cuesta conseguir operarios y técnicos (frigoristas, electricistas, PLC)? ¿Cuánto tarda en aprender un operario de evisceración o deshuese? | DPV-14A-08, DPV-121 |

## 5. Qué no hacer todavía

- No convertir FTE en personas de nómina ni comparar "personas" de dos fuentes sin saber qué unidad usan.
- No comprometer una estructura gerencial antes de saber la escala y el modelo (asset-light o planta propia).
- No suponer que el segundo turno duplica la capacidad ni que las horas extra resuelven la jornada.
- No cargar sueldos: la plantilla de costos ([`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv)) está vacía a propósito (DPV-14A-01, DPV-14A-03).
