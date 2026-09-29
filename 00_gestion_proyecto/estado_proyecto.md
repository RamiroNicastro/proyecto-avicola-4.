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
| 2026-09-29 | Estudio del mercado internacional y de exportación (`17_exportacion`): comercio mundial, productos, acceso por país (A/B/C/D), China, Halal, UE, valorización del ave, requisitos de planta, logística, riesgos y modelos A/B/C | Completado v1. **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA |
| — | Validación de demanda (`02_clientes_demanda`) | Pendiente |
| — | Balance de masa preliminar (`04_balance_masa`) | Pendiente |
| — | Escenarios CAPEX/OPEX y modelo financiero | Pendiente |
| — | Informe de prefactibilidad | Pendiente |

## Resultado del relevamiento de mercado (2026-09-29)

Síntesis en [`../01_mercado/conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md):

- Mercado grande y maduro: ~2,1–2,3 Mt (producción 2025 SAGyP ~2,3 Mt), ~47–49 kg/hab/año, faena SENASA estancada en ~740–750 M cabezas. Todas las cifras están PENDIENTES DE VERIFICACIÓN DOCUMENTAL PRIMARIA.
- El líder (Granja Tres Arroyos) está en concurso preventivo (sept-2026): es un evento de mercado, no una estrategia del proyecto.
- Riesgo sanitario recurrente (IAAP en 2023, 2025 y 2026) con cierres de exportación y sobreoferta interna.
- Exportación: UE, Japón, Chile y Perú reabiertos en 2026; China cerrada (desde ago-2025, ver estudio de exportación). El ingreso total por ave queda como principio estratégico.

## Resultado del estudio internacional y de exportación (2026-09-29)

Síntesis en [`../17_exportacion/conclusiones_exportacion.md`](../17_exportacion/conclusiones_exportacion.md):

- Comercio mundial ~14,8 Mt (2026), dominado por Brasil (~36 %). Argentina es un exportador marginal (~1–1,5 %) y precio-aceptante.
- **China cerrada desde ago-2025** (corrige el registro previo, que decía feb-2026); queda fuera del caso base (SUP-016).
- Acceso con comunicado posterior a feb-2026: UE, Japón, Corea del Sur, Chile, Perú. Regionalización reconocida: Vietnam (1° destino efectivo), Arabia Saudita, EAU, Singapur, Brasil.
- Exportar no se presume más rentable: se compara por net-back por parte del ave (SUP-017). Modelos A/B/C comparados sin ganador (DEC-011).
- Requisitos de diseño a evaluar: estándar UE y "Halal-ready" sin capacidad dedicada (SUP-015, DEC-012).

## Próximos pasos

0. **No iniciar la fase siguiente hasta que el promotor lo indique** (instrucción 2026-09-29).
1. Validación de demanda multicanal, empezando por la red de supermercados y su proveedor actual (`02_clientes_demanda`; DPV-002, DPV-003, DPV-018, DPV-020).
2. Verificación documental primaria de las cifras de mercado (requiere acceso de red o descarga manual) y completado de series (DPV-009, DPV-010, DPV-013, DPV-021).
3. Relevamiento de faena a façon y pollito BB; seguimiento del concurso de GTA sin supuestos (DPV-006, DPV-016).
4. ~~Sesión específica de estrategia exportadora~~ (realizada 2026-09-29). Pendiente: información de campo de exportación (DPV-024, DPV-026, DPV-027, DPV-032) y verificación de acceso por país (DPV-031).

Ver [`decisiones_pendientes.md`](decisiones_pendientes.md) y [`datos_por_validar.md`](datos_por_validar.md).
