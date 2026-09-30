# Estado del proyecto

**Fase actual:** FASE 0 — DEFINICIÓN Y PREFACTIBILIDAD
**Última actualización:** 2026-09-29

## Situación de partida

- Activo existente: una carnicería familiar.
- Sin granjas, frigorífico, terreno, maquinaria ni infraestructura industrial.
- Capital potencial: ~USD 2.000.000 de un grupo inversor — **no comprometido**. Es solo un **escenario inicial de referencia**, no un límite (SUP-003, DEC-010).
- Canal comercial potencial: ~90 supermercados, aparentemente concentrados en AMBA — **demanda no validada**; proveedor actual desconocido (SUP-004, DPV-020). La carnicería está en el AMBA.
- Visión: empresa avícola integrada, escalable y con vocación exportadora (SUP-011). Principio: ingreso total por ave (SUP-013). Sin localización seleccionada (DEC-003).

Detalle de premisas: [`supuestos.md`](supuestos.md).

## Alcance de la Fase 0

1. Estructurar el repositorio y las reglas de trabajo. ✅
2. Relevar información de mercado, normativa y tecnología con fuentes trazables.
3. Validar (o descartar) la demanda del canal supermercados.
4. Construir el balance de masa y escenarios de escala sin fijar capacidad a priori.
5. Evaluar cada eslabón de la cadena: hacer / comprar / tercerizar / postergar.
6. Estimar CAPEX y OPEX por escenario y construir el modelo financiero.
7. Emitir conclusión de prefactibilidad (viable / viable con condiciones / no viable) y definir si se pasa a Fase 1 (factibilidad).

## Restricciones vigentes en esta fase

- **No** se realizan recomendaciones de inversión.
- **No** se selecciona maquinaria ni proveedores (solo relevamiento).
- **No** se fija capacidad de faena.

## Hitos

| Fecha | Hito | Estado |
|---|---|---|
| 2026-09-29 | Estructura del repositorio y reglas (`CLAUDE.md`) | Completado |
| 2026-09-29 | Relevamiento de mercado (`01_mercado`): radiografía 2026, competidores, exportaciones y conclusiones | Completado v2 (segunda pasada de control y triangulación). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)** |
| 2026-09-29 | Estudio del mercado internacional y de exportación (`17_exportacion`): comercio mundial, productos, acceso por país (A/B/C/D), China, Halal, UE, valorización del ave, requisitos de planta, logística, riesgos y modelos A/B/C | Completado v1.1 (con corrección prudencial sobre China, Halal, niveles de acceso y precios). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA |
| 2026-09-29 | Modelo de demanda comercial (`02_clientes_demanda`): categorías A/B/C/D, niveles de exportación 0–6, escenarios de la red (25–300 kg/local/día), mix, logística, concentración, precio-margen, marca, indicadores, cuestionario y tareas de campo | Completado v1 (marco, **sin datos de campo**). Calidad: MEDIA como método, BAJA como evidencia cuantitativa |
| 2026-09-29 | Estudio de producción primaria (`03_produccion_primaria`): ciclo productivo, rangos de edad/peso/FCR/mortalidad, densidad y bienestar, galpones, energía y clima, alimento y agua, bioseguridad, transporte de aves vivas, modelos propio/integrado/compra/mixto, pollito BB, KPIs, escenarios físicos (72) con modelo documentado y guía para el responsable | Completado v1.1 (marco y escenarios, **sin datos de campo**; auditoría del modelo físico con corrección de pollitos/semana y galpones +4,3 % y pruebas automáticas). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA como marco y modelo físico, BAJA como evidencia de campo argentina |
| — | Validación de demanda con datos de campo (red de supermercados y otros canales) | Pendiente: requiere el cuestionario y las tareas de `02_clientes_demanda/conclusiones_demanda.md` §6 |
| — | Balance de masa preliminar (`04_balance_masa`) | Pendiente |
| — | Escenarios CAPEX/OPEX y modelo financiero | Pendiente |
| — | Informe de prefactibilidad | Pendiente |

## Resultado del relevamiento de mercado (2026-09-29)

Síntesis en [`../01_mercado/conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md):

- Mercado grande y maduro: ~2,1–2,3 Mt (producción 2025 SAGyP ~2,3 Mt), ~47–49 kg/hab/año, faena SENASA estancada en ~740–750 M cabezas. Todas las cifras están PENDIENTES DE VERIFICACIÓN DOCUMENTAL PRIMARIA.
- El líder (Granja Tres Arroyos) está en concurso preventivo (sept-2026): es un evento de mercado, no una estrategia del proyecto.
- Riesgo sanitario recurrente (IAAP en 2023, 2025 y 2026) con cierres de exportación y sobreoferta interna.
- Exportación: UE, Japón, Chile y Perú reabiertos en 2026; China no disponible confirmada (fecha y alcance de la suspensión pendientes de verificación, DPV-035). El ingreso total por ave queda como principio estratégico.

## Resultado del estudio internacional y de exportación (2026-09-29)

Síntesis en [`../17_exportacion/conclusiones_exportacion.md`](../17_exportacion/conclusiones_exportacion.md):

- Comercio mundial ~14,8 Mt (2026), dominado por Brasil (~36 %). Argentina es un exportador marginal (~1–1,5 %) y precio-aceptante.
- **China no se considera un mercado disponible confirmado**; fecha y alcance de la suspensión pendientes de verificación primaria (DPV-035). Queda fuera del caso base (SUP-016).
- Países con comunicado de apertura posterior a feb-2026 (país abierto ≠ planta habilitada ≠ producto autorizado ≠ comprador): UE, Japón, Corea del Sur, Chile, Perú. Regionalización reconocida: Vietnam (1° destino efectivo), Arabia Saudita, EAU, Singapur, Brasil.
- Exportar no se presume más rentable: se compara por net-back por parte del ave (SUP-017). Modelos A/B/C comparados sin ganador (DEC-011).
- Requisitos de diseño a evaluar: estándar UE (SUP-015) y un diseño que preserve la posibilidad de incorporar procesos y certificaciones Halal una vez validados los requisitos (DEC-012, DPV-034). Los precios internacionales son preliminares y no se usan para calcular rentabilidad (SUP-018).

## Resultado del modelo de demanda comercial (2026-09-29)

Síntesis en [`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md):

- **Demanda documentada (A + B) ≈ 0 kg/día:** la carnicería familiar no está cuantificada; la red de ~90 supermercados es categoría C condicionada; otros canales y exportación son D. **No hay base para dimensionar la planta.**
- La red, si todos los locales compraran todo su pollo al proyecto, representaría 2,25–27 t/día (25–300 kg/local/día), ~940–15.000 aves/día según el peso por ave (1,8–2,4 kg equivalente canal, SUP-019). Con adhesión parcial, 0,25–27 t/día.
- Escenarios de prueba (no pronósticos): conservador 1,5 t/día, base 7,5 t/día, expansivo 23,5 t/día; exportación 0 en todos (SUP-022). La red pesa 57–67 % de las ventas: concentración estructural.
- El mix puede multiplicar las aves necesarias por hasta ~1,5 y generar excedentes de partes que requieren otros canales; la logística de la red (CD o entrega a locales) es prioritaria (DPV-036).
- Metodología de dimensionamiento propuesta (DEC-014), sin parámetros ni capacidad calculada.

## Resultado del estudio de producción primaria (2026-09-29)

Síntesis en [`../03_produccion_primaria/conclusiones_produccion.md`](../03_produccion_primaria/conclusiones_produccion.md):

- Rangos (escenarios, no datos de campo): edad 38 / 47 / 54 d; peso vivo 2,4 / 2,9 / 3,4 kg; FCR de campo 1,60–1,85 a 2,9 kg; mortalidad en granja 3 / 5 / 8 % (un estudio de Entre Ríos registró 7,7–9,5 %: señal de riesgo a validar, DPV-044); ~5–7 ciclos/año (no 365/edad).
- Escenarios físicos hipotéticos de 2.500 / 5.000 / 10.000 / 20.000 **aves faenadas**/día (5 d/semana, perfil y desempeño medios): ~13.200 / 26.400 / 52.800 / 105.600 pollitos BB alojados por semana plena; ~3.100 / 6.200 / 12.400 / 24.700 t de alimento/año; ~9.500 / 19.000 / 37.900 / 75.900 m² de galpón (versión 1.1, tras la auditoría del modelo). Los supuestos mueven los m² hasta ~3,3 veces. **No son escala ni diseño.**
- +0,1 de FCR = +5,9 % de alimento. La superficie depende sobre todo de densidad, peso y ciclos.
- Riesgos críticos: IAAP, golpe de calor y fallas eléctricas, pollito BB concentrado, disponibilidad de integrados.
- Modelos de abastecimiento (propio / integrado / compra / mixto) comparados **sin ganador** (DEC-020). No se asume granja ni incubadora propia (SUP-034).

## Próximos pasos

0. **No iniciar la fase siguiente hasta que el promotor lo indique** (instrucción 2026-09-29).
1. Validación de demanda de campo: aplicar el cuestionario a la red y al potencial inversor y ejecutar las tareas priorizadas de `02_clientes_demanda/conclusiones_demanda.md` §6 (DPV-002, DPV-003, DPV-018, DPV-020, DPV-036 a DPV-040). Evaluar una etapa de validación comercial previa a la inversión (DEC-018).
2. Verificación documental primaria de las cifras de mercado (requiere acceso de red o descarga manual) y completado de series (DPV-009, DPV-010, DPV-013, DPV-021).
3. Relevamiento de faena a façon y pollito BB; seguimiento del concurso de GTA sin supuestos (DPV-006, DPV-016).
4. ~~Sesión específica de estrategia exportadora~~ (realizada 2026-09-29). Pendiente: información de campo de exportación (DPV-024, DPV-026, DPV-027, DPV-032) y verificación de acceso por país (DPV-031).
5. Producción primaria (realizada 2026-09-29). Pendiente: datos de campo de desempeño (DPV-044), productores integrables (DPV-048), pollito BB (DPV-047), normativa completa (DPV-046) y manuales genéticos (DPV-045); preguntas en `03_produccion_primaria/guia_ramiro.md`. **No se inició** el balance de masa, el dimensionamiento del frigorífico ni la maquinaria.

Ver [`decisiones_pendientes.md`](decisiones_pendientes.md) y [`datos_por_validar.md`](datos_por_validar.md).
