# Conclusiones — recursos humanos y organización

**Fecha:** 2026-10-01 · **Versión:** 1.1 (sesión 14A, en paralelo con 14B; auditoría final de unidades laborales) · Base: [`estructura_organizacional.md`](estructura_organizacional.md), [`dotacion_por_escala.md`](dotacion_por_escala.md), [`turnos_y_productividad.md`](turnos_y_productividad.md), [`mantenimiento_y_servicios.md`](mantenimiento_y_servicios.md), [`calidad_inocuidad.md`](calidad_inocuidad.md), [`modelo_rrhh.py`](modelo_rrhh.py), [`escenarios_rrhh.csv`](escenarios_rrhh.csv), [`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv), [`guia_ramiro.md`](guia_ramiro.md)

> **Pregunta central:** ¿qué personas necesita la empresa, dónde trabajan, en qué turnos y cómo cambia la estructura al crecer de 2.500 a 20.000 aves/día?
> **No** se elige escala, automatización, turnos, modalidad de limpieza, mantenimiento ni flota; **no** se inicia OPEX ni se cargan salarios (plantilla de costos vacía). Registros centrales **no** modificados: propuestas en [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md).
> **Evidencia:** ninguna productividad, ausentismo ni dotación proviene de plantas argentinas. Todas las cifras son `[ESTIMACIÓN]` con coeficientes `[SUPUESTO]` de rango.

---

## 0. Auditoría de unidades (v1.1)

| v1.0 | v1.1 |
|---|---|
| Una variable "personas" para todo | **Puestos por turno, dotación simultánea, pico en sitio, puestos equivalentes, headcount de nómina, FTE y horas contratadas** separados y nunca sumados entre sí |
| "Personas" = puestos × cobertura 1,08–1,18 | **Headcount de nómina PENDIENTE** (FACTOR_COBERTURA_NOMINA no validado); sólo un rango de sensibilidad; nunca derivado del FTE |
| FTE con factor de cobertura y semana de 45 h | **FTE = horas-persona por día operativo ÷ jornada de referencia de 8 h** (2 personas × 4 h = 1 FTE) |
| "43 h extra por persona al mes" y tope de 30 h como restricción | **Brecha de jornada** sin forma organizativa asumida; límites legales/CCT como DPV |
| Limpieza tercerizada: interna 0, externos | **Horas contratadas** iguales a las internas que reemplaza; presencia en sitio conservada |
| "Hasta 10.000 manda tener un técnico presente" | **Política de cobertura de referencia** separada de la **carga por activos**; dotación = reconciliación |
| Proxy de 12C comparado con "personas por turno" | Layout recibe el **pico de personas simultáneas**, nunca FTE ni headcount |
| 15 tests, 8 mutaciones | **24 tests, 13 mutaciones** |

## 1. Headcount vs FTE vs simultáneos

A 20.000 aves/día (referencia, media): **50** puestos simultáneos de producción · **87** personas en sitio en el pico · **35** personas simultáneas en la cuadrilla de limpieza (en otra franja) · **132** puestos equivalentes internos · **126** FTE internos + **3,1** FTE tercerizados · headcount de nómina **PENDIENTE** (sensibilidad 143–156 con factor 1,08–1,18). Puestos equivalentes > FTE donde hay trabajo parcial (limpieza: 35 puestos = 17,5 FTE); FTE > puestos donde la presencia supera la jornada (línea: ~10 h = 1,25 FTE por puesto).

## 2. Dotación (referencia; alta–**media**–baja)

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Puestos simultáneos de producción | 28–**31**–37 | 35–**40**–52 | 36–**47**–62 | 35–**50**–66 |
| Pico de personas en sitio | 37–**41**–47 | 52–**58**–70 | 61–**72**–88 | 71–**87**–104 |
| Puestos equivalentes internos | 44–**51**–64 | 64–**74**–95 | 78–**98**–128 | 100–**132**–184 |
| Headcount de nómina | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |
| FTE internos | 45–**55**–75 | 64–**77**–109 | 76–**99**–142 | 91–**126**–191 |
| FTE tercerizados | 0,8 | 0,8 | 1,5 | 3,1 |
| Funciones int. / terc. / PENDIENTES / total | 31 / 2 / 3 / 36 | 37 / 2 / 3 / 42 | 41 / 2 / 3 / 46 | 42 / 2 / 3 / 47 |

Asset-light (escenario organizacional de referencia): 10 / 17,5 / 24,5 / 35,5 FTE internos, desagregados en comercial, administración, coordinación productiva, calidad, supervisión de terceros, logística y dirección ([`dotacion_por_escala.md`](dotacion_por_escala.md) §4).

## 3. Limpieza

Dotación simultánea 7 / 11 / 19 / 35 (rango 5–59) durante una ventana de 4 h → horas-persona 28 / 44 / 76 / 140 por día → **FTE 3,5 / 5,5 / 9,5 / 17,5**. **Headcount contractual PENDIENTE** según esquema laboral. Tercerizada: las mismas horas pasan a **servicio tercerizado / horas contratadas**; la cuadrilla sigue en el sitio; supervisión POES y limpieza operativa siguen internas.

## 4. Turnos y jornada

**Con la parametrización actual, una sola cuadrilla bajo una jornada de referencia de 8 h no puede cubrir 8 h netas de producción más todas las ventanas auxiliares sin una organización adicional** (presencia ~10 h; brecha ~2 h/persona; 59–91 horas-persona/día a organizar según escala). La forma de resolverlo (turnos, relevos, escalonamiento, personal adicional, horas extraordinarias u otra) no está demostrada (DPV-14A-01). Sin organización adicional caben ~6–7 h netas con una cuadrilla y ~11,4–13,5 h con dos. Dos cuadrillas de 8 h netas tienen alertas de jornada y de 24 h. Matriz de presencia: el pico en sitio ocurre al inicio con la jornada diurna o, con dos cuadrillas, en el traspaso (10.000: 72 → 96).

## 5. Automatización

Resultados del modelo basados en sus supuestos **por tarea**, no ahorro validado: de manual a automático, directos por turno −33 % (2.500) a −67 % (20.000) (evisceración 35 → 8, trozado 30 → 8, empaque 25 → 7 a 20.000; colgado sin cambio); FTE de mantenimiento +1,5 a +3,1; en 2.500, de semiautomático a automático no se reducen FTE (47,0 → 47,1). Genéricos etiquetados como sensibilidad: factor de limpieza por automatización y fracción interna de la limpieza híbrida.

## 6. Mantenimiento

**Cobertura operativa** (política de referencia, no requisito universal): 2,1 / 3,5 / 4,9 / 6,4 FTE. **Carga por activos**: 2,3 / 2,4 / 3,6 / 7,5 FTE (rango 1,1–17,1). **Reconciliación** (máximo): 2,3 / 3,5 / 4,9 / 7,5. Manda la carga en 2.500 y 20.000, la cobertura en 5.000–10.000. Propio, tercerizado y mixto conservan las mismas horas; cambia quién las emplea.

## 7. Indirectos y soporte

El ratio FTE indirecto/directo (0,86 → 1,72) es **informativo y no dimensiona**. Sube en la referencia sobre todo por **automatización**: con el mismo nivel semiautomático en todas las escalas vale 1,13 / 1,35 / 1,13 / 0,97 (baja a gran escala). FTE no directos por cómo escalan:

| Driver | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Escala con la producción (limpieza, QC, supervisión, expedición, logística, técnicos de campo, lavandería) | 13,5 | 18,0 | 24,0 | 39,5 |
| Escala por activos (mantenimiento, jefe, pañol) | 2,3 | 4,5 | 6,9 | 9,5 |
| Casi fijo (dirección, jefaturas, QA/APPCC, administración mínima, coordinación primaria, HyS) | 8,0 | 13,0 | 18,0 | 25,5 |
| Depende de la estrategia (ventas, choferes, laboratorio, QC en façon, captura) | 1,8 | 2,8 | 4,5 | 7,1 |

Lo casi fijo explica la dilución por escala; lo que escala por activos explica el salto con la automatización.

## 8. Tensión con 12C

12C usó un proxy de dotación por turno (SUP-116) de 49 / 82 / 115 / 165 para vestuarios. El modelo da **pico en sitio de 41 / 58 / 72 / 87** (puestos simultáneos de producción 31 / 40 / 47 / 50; cuadrilla de limpieza 7 / 11 / 19 / 35 en otra franja). **No se corrige 12C desde esta rama.** Para la reconciliación: layout debe dimensionar vestuarios, comedor y estacionamiento con el **pico de personas simultáneas** (`modelo_rrhh.salida_layout`: pico, simultáneos por zona, cuadrilla de limpieza) **más margen y requisitos** por zona y sexo, **no** con FTE anuales ni headcount total. Esto probablemente explica parte de la diferencia.

## 9. Preparación para OPEX

[`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv) (175 filas, 4 escenarios de referencia): PUESTO, AREA, GRUPO, ZONA, FRANJA, MODALIDAD (interno / tercerizado (horas contratadas) / servicio externo por unidad / PENDIENTE), PUESTOS_TURNO, SIMULTANEOS, PUESTOS_EQUIVALENTES, HEADCOUNT (PENDIENTE), FTE, HORAS_MES, TURNOS, TIPO_CONTRATACION, SUELDO_BASE, CARGAS, ADICIONALES, HORAS_EXTRA, BENEFICIOS, COSTO_EMPRESA_MENSUAL, COSTO_EMPRESA_ANUAL, MONEDA, TIPO_CAMBIO_FECHA_FUENTE, FUENTE, ESTADO. **Todas las columnas de costo vacías** (test R22). FACTOR_COBERTURA_NOMINA es una entrada del modelo (`factor_cobertura_nomina`, None = PENDIENTE).

## 10. Tests

`python3 18_recursos_humanos/modelo_rrhh.py --solo-tests` → **24/24**; `--mutaciones` → **13/13 detectadas**.

| Test | Qué valida |
|---|---|
| R01–R14 (adaptados) | Unidades no negativas; más escala no reduce FTE, puestos, simultáneos ni pico; automatización no reduce técnicos y sí directos; tercerización conserva función, responsable y presencia; 24 h y jornada con alerta; independencia; faltantes PENDIENTES; entradas inválidas; puestos equivalentes = puestos × cuadrillas; FTE = horas-persona ÷ 8; KPI; 09A intacto; rangos ordenados (R13 ya no exige ordenar el pico, que depende del horario del traspaso); mix |
| R15 | Headcount, FTE, simultáneos y puestos son variables distintas; headcount PENDIENTE sin factor y nunca desde FTE |
| R16 | Una cuadrilla parcial no cuenta como igual número de FTE |
| R17 | Tercerizar no elimina horas de trabajo |
| R18 | Sin horas extra automáticas ("1" y "extendido" = mismas horas; sólo cambia la alerta) |
| R19 | Mantenimiento separa cobertura y carga; dotación = máximo |
| R20 | Layout recibe el pico simultáneo de la matriz de presencia, no FTE |
| R21 | Cada KPI declara denominador y universo |
| R22 | Plantilla de costos sin salarios ni headcount numérico |
| R23 | SENASA fuera de nómina, FTE, puestos y pico |

## 11. Limitaciones

1. Coeficientes sin dato argentino (rangos); el factor de cobertura de nómina no está validado.
2. La limpieza depende de m² proxy de 12C y de una ventana fija; la limpieza por sectores no está modelada.
3. El horario de la matriz de presencia (diurna desde el fin de la preparación; limpieza sin solapamiento) es un supuesto (SUP-14A-18).
4. Choferes de producto, inspección oficial, servicio externo de HyS y captura PENDIENTES.
5. Sin costos: no puede evaluarse todavía la conveniencia de automatizar, tercerizar o sumar una cuadrilla.

**Evaluación: MEDIA** como modelo organizacional y de unidades laborales; **BAJA** como evidencia de dotación real.
