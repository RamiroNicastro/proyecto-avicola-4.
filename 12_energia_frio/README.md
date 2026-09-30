# 12 — Energía y frío

**Alcance:** demanda eléctrica y térmica (gas, calefacción de galpones, escaldado), cadena de frío (túneles, cámaras, congelado), disponibilidad de potencia en zonas candidatas, energías alternativas.

**Relacionado:** `05_proceso_industrial`, `10_localizacion`, `20_opex`, `11_agua_efluentes` (modelo de utilities, CSV y fuentes).

## Contenido (versión 1.1, 2026-09-30 — sesión 09C con auditoría conceptual)

> Energía diaria y potencia **media** equivalente (pico PENDIENTE); MJ/día (pico térmico PENDIENTE); carga sensible del producto (carga frigorífica total PENDIENTE); kWe = kWf ÷ COP supuesto declarado; carga crítica ilustrativa (generador PENDIENTE).

| Archivo | Contenido |
|---|---|
| [`demanda_energia.md`](demanda_energia.md) | Consumidores; energía diaria → potencia media equivalente ≠ pico; MJ/día ≠ kW térmicos pico; fuentes térmicas; integración top-down/bottom-up con 09A |
| [`sistema_frio.md`](sistema_frio.md) | Carga sensible del producto ≠ carga frigorífica total; COP declarado; brecha con el benchmark; refrigerantes sin elegir |
| [`congelado_almacenamiento.md`](congelado_almacenamiento.md) | Capacidad diaria de congelación vs almacenamiento estático; toneladas por perfil P1–P3 en días de producción y días calendario; garras, menudencias, subproductos |
| [`respaldo_energia.md`](respaldo_energia.md) | Cargas críticas, carga crítica ilustrativa de escenario (proxy), qué exige dimensionar el generador, redundancia |
| [`conclusiones_energia_frio.md`](conclusiones_energia_frio.md) | Síntesis de energía, frío, congelado y respaldo |

**Modelo y datos:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) y [`../11_agua_efluentes/escenarios_utilities.csv`](../11_agua_efluentes/escenarios_utilities.csv) (documentación en [`../11_agua_efluentes/README.md`](../11_agua_efluentes/README.md)). La energía de granjas (calefacción, ventilación) queda en `03_produccion_primaria` y fuera de este modelo.
