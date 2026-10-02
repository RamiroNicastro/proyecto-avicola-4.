# Dotación por escala — 2.500 / 5.000 / 10.000 / 20.000 aves/día

**Fecha:** 2026-10-01 · **Versión:** 1.1 (sesión 14A; auditoría de unidades laborales) · Fase 0

> **Qué es:** órdenes de magnitud de puestos, presencia simultánea, FTE y horas contratadas por escala, con rangos de productividad alta–media–baja. Fuente: [`modelo_rrhh.py`](modelo_rrhh.py) v1.1 y [`escenarios_rrhh.csv`](escenarios_rrhh.csv) (15.576 escenarios).
> **Qué no es:** una dotación validada, un headcount de nómina ni un plan de contratación. **Ninguna productividad es un dato argentino medido**: coeficientes `[SUPUESTO]` de rango (SUP-127 a SUP-141) y dos referencias extranjeras débiles `[PVDP]` (colgado FTE-219; eviscerado manual FTE-218). Todas las cifras son `[ESTIMACIÓN]`.
> **v1.1:** la v1.0 usaba una sola variable "personas" para conceptos distintos. Esta versión separa las unidades y deja el **headcount de nómina como PENDIENTE**.

---

## 1. Unidades (no se suman entre sí)

| Unidad | Definición | Para qué sirve | Estado |
|---|---|---|---|
| **Puestos por turno** | Posiciones que deben cubrirse durante un turno, por cuadrilla | Diseño de línea, supervisión | Calculado |
| **Dotación simultánea** | Personas presentes al mismo tiempo durante una operación (p. ej., cuadrilla de limpieza) | Organización de franjas | Calculado |
| **Puestos simultáneos de producción** | Suma de puestos presentes mientras corre la línea: directos + supervisión de línea + QC + limpieza operativa + técnicos de cobertura | Personal de planta en producción | Calculado |
| **Pico de personas en sitio** | Máximo de personas presentes a la vez en el establecimiento (internas y terceros en sitio), según la matriz de presencia ([`turnos_y_productividad.md`](turnos_y_productividad.md) §3) | **Vestuarios, comedor, estacionamiento (12C)** | Calculado; excluye inspección oficial (PENDIENTE) |
| **Puestos equivalentes internos** | Posiciones distintas a cubrir con personal propio: puestos × cuadrillas; integrantes de la cuadrilla de limpieza propia; dedicación de roles de estructura (0,5 = rol combinado) | **Base** del headcount | Calculado |
| **Headcount de nómina** | Puestos equivalentes × FACTOR_COBERTURA_NOMINA (francos, vacaciones, licencias, ausentismo, capacitación, reemplazos) | Nómina y OPEX | **PENDIENTE** (factor no validado, DPV-147). **No se deriva del FTE** |
| **FTE** | Horas-persona por día operativo ÷ jornada de referencia de 8 h `[PVDP]`. 2 personas × 4 h = 1 FTE | Comparar cargas de trabajo; OPEX por hora | Calculado |
| **FTE tercerizados / horas contratadas** | Horas-persona de funciones tercerizadas (limpieza, mantenimiento, flota) | Servicios tercerizados en OPEX | Calculado (salvo funciones PENDIENTES) |
| **Funciones cubiertas** | Funciones con carga interna, tercerizada o PENDIENTE | Verificar que tercerizar no borre funciones | Calculado |

## 2. Tabla de dotación corregida

**Escenario de referencia (no es decisión, SUP-138):** 1 cuadrilla con 8 h netas en turno extendido (alerta de jornada, [`turnos_y_productividad.md`](turnos_y_productividad.md) §2), automatización de referencia de 09A por escala (manual / mecanizado / semiautomático / automático; DEC-037 abierta), config. B (trozado), limpieza y mantenimiento propios, flota de aves de terceros con 5.500 aves/camión **de escenario** (SUP-033), integración, laboratorio externo, 5 días/semana. Rango: productividad alta–**media**–baja.

| Unidad | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Puestos directos por turno | 22–**24**–30 | 28–**32**–43 | 28–**38**–50 | 25–**38**–51 |
| Puestos simultáneos de producción | 28–**31**–37 | 35–**40**–52 | 36–**47**–62 | 35–**50**–66 |
| Cuadrilla de limpieza simultánea (otra franja) | 5–**7**–11 | 7–**11**–18 | 12–**19**–30 | 21–**35**–59 |
| **Pico de personas en sitio** | 37–**41**–47 | 52–**58**–70 | 61–**72**–88 | 71–**87**–104 |
| Puestos equivalentes internos (base de headcount) | 44–**51**–64 | 64–**74**–95 | 78–**98**–128 | 100–**132**–184 |
| **Headcount de nómina** | **PENDIENTE** | **PENDIENTE** | **PENDIENTE** | **PENDIENTE** |
| *Headcount — sólo sensibilidad, factor 1,08–1,18 (media)* | *55–60* | *79–87* | *106–116* | *143–156* |
| **FTE internos** | 45–**55**–75 | 64–**77**–109 | 76–**99**–142 | 91–**126**–191 |
| **FTE tercerizados** (choferes de aves de terceros) | 0,8 | 0,8 | 1,5 | 3,1 |
| Horas-persona por día (internas + tercerizadas) | 366–**444**–604 | 518–**625**–876 | 617–**806**–1.145 | 752–**1.031**–1.556 |
| Funciones cubiertas: internas / tercerizadas / PENDIENTES / total (media) | 31 / 2 / 3 / 36 | 37 / 2 / 3 / 42 | 41 / 2 / 3 / 46 | 42 / 2 / 3 / 47 |

Las funciones PENDIENTES (inspección oficial, servicio externo de HyS, captura; además los choferes de producto) **no se suman**: sus horas no se conocen. La inspección oficial no es personal de la empresa ([`calidad_inocuidad.md`](calidad_inocuidad.md) §1).

FTE por grupo (internos + tercerizados, productividad media) y puestos equivalentes internos:

| Grupo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Directos (FTE) | 29,9 | 39,9 | 47,4 | 47,4 |
| Supervisión (FTE) | 3,5 | 3,5 | 4,5 | 4,5 |
| Soporte (FTE) | 16,6 | 25,2 | 35,9 | 57,5 |
| Administración (FTE) | 3,5 | 6,5 | 9,0 | 14,5 |
| Dirección (FTE) | 2,0 | 3,0 | 4,0 | 5,0 |
| Puestos equivalentes internos: directos / supervisión / soporte / adm. / dirección | 24 / 3 / 18 / 3,5 / 2 | 32 / 3 / 29 / 6,5 / 3 | 38 / 4 / 43 / 9 / 4 | 38 / 4 / 71 / 14,5 / 5 |

**Lecturas:**

1. **Las unidades divergen donde importan.** A 20.000 aves/día: 50 puestos simultáneos en producción, 87 personas en sitio en el pico, 132 puestos equivalentes, 126 FTE internos. Ninguna de estas cifras es "la dotación": cada una responde a otra pregunta.
2. **Puestos equivalentes > FTE cuando hay trabajo parcial** (limpieza: 35 puestos y 17,5 FTE a 20.000) y **FTE > puestos cuando la presencia supera la jornada** (línea: ~10 h de presencia sobre 8 h → 1,25 FTE por puesto). Por eso el headcount no puede derivarse del FTE.
3. **El rango de productividad pesa más que el punto medio** (FTE internos ×1,7–2,1 entre alta y baja). Ninguna cifra central debe usarse como dotación hasta tener datos de plantas (DPV-092).
4. **La escala diluye la estructura:** de 2.500 a 20.000 aves/día (×8), los FTE totales crecen ×2,3 (media). FTE por 1.000 aves/día: 22,2 → 6,4.
5. **Los directos se estancan entre 10.000 y 20.000** sólo porque la referencia pasa de semiautomático a automático; con el mismo nivel de automatización los directos siempre crecen con la escala (test R02).

## 3. Puestos por tarea (escenario de referencia, media; puestos por turno)

| Tarea | 2.500 (M) | 5.000 (Mc) | 10.000 (S) | 20.000 (A) |
|---|---|---|---|---|
| Colgado | 1 | 1 | 2 | 3 |
| Descarga, cajones y andén | 1 | 1 | 1 | 1 |
| Faena | 2 | 2 | 3 | 3 |
| Evisceración (sin inspección oficial) | 6 | 10 | 9 | 8 |
| Enfriamiento | 1 | 1 | 1 | 1 |
| Clasificación | 1 | 1 | 1 | 1 |
| Trozado (config. B) | 5 | 7 | 9 | 8 |
| Empaque | 4 | 6 | 7 | 7 |
| Cámaras y expedición | 2 | 2 | 3 | 4 |
| Subproductos | 1 | 1 | 2 | 2 |
| **Directos por turno** | **24** | **32** | **38** | **38** |
| Limpieza operativa en turno | 2 | 2 | 2 | 3 |
| Supervisores de línea | 2 | 2 | 2 | 2 |
| Control de calidad (QC) | 2 | 2 | 2 | 3 |
| Técnicos presentes (política de cobertura) | 1 | 2 | 3 | 4 |
| **Puestos simultáneos de producción** | **31** | **40** | **47** | **50** |

Puestos por zona en producción (circuitos de cambio y vestuarios por zona): sucia 4 / 4 / 6 / 7; evisceración 6 / 10 / 9 / 8; limpia 11 / 15 / 18 / 17; frío y expedición 2 / 2 / 3 / 4; subproductos 1 / 1 / 2 / 2; transversal 7 / 8 / 9 / 12.

## 4. Asset-light (faena a façon) — escenario organizacional de referencia

**No** se asume que cada incremento de aves requiera esta estructura: las cifras son una configuración posible, por bloque, con roles que dependen del volumen y roles casi fijos.

FTE internos por bloque (media):

| Bloque | 2.500 | 5.000 | 10.000 | 20.000 | ¿Depende del volumen? |
|---|---|---|---|---|---|
| Comercial (ventas, gerente comercial) | 1 | 3 | 4 | 5 | Depende de **canales y clientes** más que de aves |
| Administración (adm., finanzas, compras, RR. HH., sistemas) | 2,5 | 4,0 | 6,5 | 10,5 | Escalonado; casi fijo en el piso |
| Coordinación productiva (integrados, veterinaria, técnicos de campo, planificación) | 2,0 | 3,5 | 5,0 | 7,0 | **Sí** (técnicos ∝ granjas) |
| Calidad (jefe, APPCC, trazabilidad) | 1,5 | 2,5 | 3,0 | 4,0 | Casi fijo, escalonado |
| Supervisión de terceros (QC propio en la planta del façonier) | 1 | 1 | 2 | 2 | Poco (por planta y turno del façonier) |
| Logística (planificación, depósito, expedición) | 1,0 | 2,5 | 3,0 | 6,0 | Sí (por despachos) |
| Dirección | 1 | 1 | 1 | 1 | Fijo |
| **Total FTE internos** | **10,0** | **17,5** | **24,5** | **35,5** | |
| Pico en sitio (oficinas propias) | 7 | 13 | 18 | 27 | |
| FTE tercerizados conocidos (dotación industrial del façonier + choferes) | 23 | 29 | 49 | 84 | Del façonier, no de la empresa |

Su viabilidad depende de que exista un façonier con capacidad, habilitación y condiciones (DEC-004, DEC-018; sin investigar).

## 5. Sensibilidades

- **Mix:** deshuesar (config. C) agrega trabajo casi todo en sala limpia (test R14); ver `escenarios_rrhh.csv` filtrando `config`.
- **Flota propia:** convierte las horas de choferes de aves de tercerizadas en internas (0,8–3,1 FTE); los choferes de producto siguen PENDIENTES.
- **Dos cuadrillas o turno extendido:** cambian puestos, FTE y pico de manera distinta ([`turnos_y_productividad.md`](turnos_y_productividad.md) §4).
- **Factor de cobertura de nómina:** sólo cambia el headcount (hoy PENDIENTE), nunca los puestos, el FTE ni el pico.

## 6. Qué falta para que estas cifras sirvan para decidir

Dotación real por sector, productividad, organización de turnos y limpieza de 2–3 plantas argentinas comparables ([`guia_ramiro.md`](guia_ramiro.md) §4); convenio aplicable (DPV-146); factor de cobertura de nómina (DPV-147); inspección oficial (DPV-101); servicio de HyS (DPV-149); oferta de mano de obra y técnicos por corredor (DPV-121). Lista completa en [`../00_gestion_proyecto/datos_por_validar.md`](../00_gestion_proyecto/datos_por_validar.md) (DPV-146 a DPV-152 y consolidados; mapa en [`reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2).
