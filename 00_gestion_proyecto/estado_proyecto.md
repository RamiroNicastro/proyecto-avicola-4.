# Estado del proyecto

**Fase actual:** FASE 0 — DEFINICIÓN Y PREFACTIBILIDAD
**Última actualización:** 2026-09-29

## Situación de partida

- Activo existente: una carnicería familiar.
- Sin granjas, frigorífico, terreno, maquinaria ni infraestructura industrial.
- Capital potencial: ~USD 2.000.000 de un grupo inversor — **no comprometido** y **sin validar suficiencia**.
- Canal comercial potencial: ~90 supermercados — **demanda no validada**.

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
| 2026-09-29 | Relevamiento de mercado (`01_mercado`): radiografía 2026, competidores, exportaciones y conclusiones | Completado v1 (verificación documental pendiente: DPV-009) |
| — | Validación de demanda (`02_clientes_demanda`) | Pendiente |
| — | Balance de masa preliminar (`04_balance_masa`) | Pendiente |
| — | Escenarios CAPEX/OPEX y modelo financiero | Pendiente |
| — | Informe de prefactibilidad | Pendiente |

## Resultado del relevamiento de mercado (2026-09-29)

Síntesis en [`../01_mercado/conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md):

- Mercado grande y maduro: ~2,1–2,2 Mt de consumo aparente, ~47–49 kg/hab/año, faena SENASA estancada en ~740–750 M cabezas.
- El líder (Granja Tres Arroyos) está en concurso preventivo (sept-2026). La oferta está en reconfiguración.
- Riesgo sanitario recurrente (IAAP en 2023, 2025 y 2026) con cierres de exportación y sobreoferta interna.
- La validación del canal supermercados pasa a ser el cuello de botella del estudio.

## Próximos pasos

1. Validación de demanda de la red de supermercados y ubicación de la red (`02_clientes_demanda`; DPV-002, DPV-003, DPV-018).
2. Verificación documental de las cifras de mercado y completado de series (DPV-009, DPV-010, DPV-013).
3. Relevamiento de faena a façon, pollito BB y activos liberados por la crisis de GTA (DPV-006, DPV-016).

Ver [`decisiones_pendientes.md`](decisiones_pendientes.md) y [`datos_por_validar.md`](datos_por_validar.md).
