# Registro de supuestos

Hipótesis de trabajo adoptadas. Un supuesto **no es un dato verificado**: debe revisarse cuando se obtenga evidencia. Al validarse o descartarse, actualizar el estado (no borrar la fila).

**Estados:** `Vigente` · `En revisión` · `Validado` · `Descartado`
**Origen:** `Promotor` (información aportada por el equipo del proyecto) · `Analista` (adoptado para modelar)

| ID | Supuesto | Área | Origen | Fecha | Estado | Vinculado a | Observaciones |
|---|---|---|---|---|---|---|---|
| SUP-001 | El proyecto se localiza en Argentina | General | Promotor | 2026-09-29 | Vigente | — | Provincia/localidad a definir (ver DEC-003) |
| SUP-002 | La moneda de evaluación de la inversión es USD | Financiero | Promotor | 2026-09-29 | Vigente | — | Tratamiento de ARS y tipo de cambio a definir (ver DEC-006) |
| SUP-003 | Existe un grupo inversor que podría aportar ~USD 2.000.000 | Financiero | Promotor | 2026-09-29 | En revisión | DPV-001 | No comprometido. Suficiencia no asumida (regla 7 de `CLAUDE.md`) |
| SUP-004 | Existe acceso potencial a una red de ~90 supermercados como canal inicial | Comercial | Promotor | 2026-09-29 | En revisión | DPV-002, DPV-003 | Demanda no validada (regla 8 de `CLAUDE.md`) |
| SUP-005 | La carnicería familiar existente puede servir como canal y aprendizaje comercial | Comercial | Promotor | 2026-09-29 | En revisión | DPV-004 | Volumen actual y rol futuro a relevar |
| SUP-006 | El producto principal es pollo parrillero (carne de pollo) | Producto | Analista | 2026-09-29 | Vigente | — | Otras especies/huevo fuera de alcance salvo decisión en contrario |
| SUP-007 | La integración vertical se desarrollará por etapas, no en simultáneo | Estrategia | Analista | 2026-09-29 | Vigente | DEC-002 | Cada eslabón se evalúa por separado |
| SUP-008 | La serie de referencia de consumo per cápita de carne aviar es la de SAGyP (consumo aparente). CEPA se usa como cota superior y BCR/SSPM como cota inferior | Mercado | Analista | 2026-09-29 | Vigente | DPV-010 | 2025: SAGyP 47,68; rango 46,8–49,4 kg/hab/año (ver `01_mercado/mercado_avicola_argentina.md` §13) |
| SUP-009 | Las conversiones ARS→USD de precios de mercado se hacen con el tipo de cambio mayorista del día o semana del dato, a título ilustrativo | Financiero | Analista | 2026-09-29 | Vigente | DEC-006 | Provisorio hasta definir el criterio del modelo (DEC-006). Fuente primaria a usar: BCRA Com. A3500 |
| SUP-010 | Para escenarios de demanda de mercado no se supone crecimiento del consumo per cápita de pollo superior al observado en 2020–2025 | Mercado | Analista | 2026-09-29 | Vigente | DPV-010 | Base: faena estancada (~740 M cab/año) y consumo cercano al techo según el sector. Revisar con series completas |
