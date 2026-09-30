# 12 — Energía y frío

**Alcance:** demanda eléctrica y térmica (gas, calefacción de galpones, escaldado), cadena de frío (túneles, cámaras, congelado), disponibilidad de potencia en zonas candidatas, energías alternativas.

**Relacionado:** `05_proceso_industrial`, `10_localizacion`, `20_opex`, `11_agua_efluentes` (modelo de utilities, CSV y fuentes).

## Contenido (versión 1.0, 2026-09-30 — sesión 09C)

| Archivo | Contenido |
|---|---|
| [`demanda_energia.md`](demanda_energia.md) | Consumidores eléctricos, kW vs kWh, kWh/ave por escala; agua caliente/vapor y comparación conceptual de fuentes térmicas |
| [`sistema_frio.md`](sistema_frio.md) | Mapa de cargas frigoríficas, kW frigoríficos vs eléctricos, TR, órdenes de magnitud; refrigerantes (NH₃, CO₂, cascada, indirectos, HFC/HFO) sin elegir |
| [`congelado_almacenamiento.md`](congelado_almacenamiento.md) | Capacidad diaria de congelación vs almacenamiento estático; toneladas por perfil P1–P3 en días de producción y días calendario; garras, menudencias, subproductos |
| [`respaldo_energia.md`](respaldo_energia.md) | Cargas críticas, orden de magnitud del respaldo, conceptos de redundancia |
| [`conclusiones_energia_frio.md`](conclusiones_energia_frio.md) | Síntesis de energía, frío, congelado y respaldo |

**Modelo y datos:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) y [`../11_agua_efluentes/escenarios_utilities.csv`](../11_agua_efluentes/escenarios_utilities.csv) (documentación en [`../11_agua_efluentes/README.md`](../11_agua_efluentes/README.md)). La energía de granjas (calefacción, ventilación) queda en `03_produccion_primaria` y fuera de este modelo.
