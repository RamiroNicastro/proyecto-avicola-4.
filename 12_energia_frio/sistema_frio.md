# Sistema de frío industrial: cargas y refrigerantes (conceptual)

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Fase 0

> **Alcance:** mapa de cargas frigoríficas, diferencia entre **kW frigoríficos** y **kW eléctricos**, órdenes de magnitud por escala y comparación conceptual de refrigerantes. **No se elige sistema, refrigerante ni proveedor**, no se dimensiona sala de máquinas, no se calcula CAPEX. Congelado y cámaras en detalle: [`congelado_almacenamiento.md`](congelado_almacenamiento.md).
> **Modelo:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) (bloque `frio`). Propiedades térmicas `[PVDP]` (FTE-09C-14); temperaturas, COP y factores `[SUPUESTO]`.

---

## 1. kW frigoríficos vs kW eléctricos vs TR

| Unidad | Qué mide | Ejemplo (10.000 aves/día, medio) |
|---|---|---|
| **kW frigoríficos** (kWf) | Calor que el sistema **extrae** del producto o del recinto por unidad de tiempo | Enfriado del producto fresco: **~235 kWf** durante las 8 h de faena |
| **TR** (tonelada de refrigeración) | Unidad histórica = calor para fundir 1 t corta de hielo en 24 h = **3,517 kWf** | ~67 TR |
| **kW eléctricos** (kWe) | Potencia que consumen los compresores (y ventiladores/bombas asociados) | ~78 kWe (con COP 3) |
| **COP** | kWf / kWe: cuántos kW de frío se obtienen por kW eléctrico | ~3 para agua helada (−5/0 °C); ~1,4 para congelado (−35/−40 °C) `[SUPUESTO]` |

Un compresor que "mueve" 235 kW de calor consume ~78 kW de electricidad; **cuanto más baja la temperatura, peor el COP**: congelar cuesta, por kW de frío, ~2 veces más electricidad que enfriar. El test U10 del modelo impide confundirlos (mutación M04).

## 2. Mapa de cargas

| Carga | Qué se enfría | Temperatura típica | Perfil | Cómo la estima el modelo |
|---|---|---|---|---|
| **Chiller / enfriado de carcasas** | Carcasas de ~38 °C a ~4 °C; agua de reposición del chiller de ~18 °C a ~1 °C | Agua/hielo 0–2 °C | Horas de faena | `[ESTIMACIÓN]` kg comestible × 3,5 kJ/(kg·K) × 34 K + L de reposición × 4,186 × 17 K |
| **Menudencias y garras** | Enfriado rápido de piezas pequeñas | 0–4 °C | Faena | Incluidas en el comestible (config. B) |
| **Producto refrigerado** (mantenimiento) | Producto ya frío en cámara 0–4 °C: paredes, puertas, infiltración, respiración nula | 0–4 °C | 24 h, 365 días | kWh/(t·día) `[SUPUESTO]` |
| **Cámaras de congelado** | Producto a −18/−25 °C | −18 a −25 °C | 24 h, 365 días | kWh/(t·día) `[SUPUESTO]` |
| **Túneles de congelado / IQF** | De +4 °C a −18 °C: sensible + **latente** (el agua se congela) + sensible bajo cero | Aire −30/−40 °C | Hasta 20 h/día | `[ESTIMACIÓN]` ~296 kJ/kg × 1,3 = ~385 kJ/kg ([`congelado_almacenamiento.md`](congelado_almacenamiento.md)) |
| **Docks / antecámaras de expedición** | Aire, puertas abiertas, montacargas | 4–10 °C | Carga y despacho | Dentro de "cargas adicionales" (+25/**40**/60 % sobre el enfriado) `[SUPUESTO]` |
| **Salas climatizadas** (despiece, empaque) | Aire de sala con personas, motores, iluminación, producto | 10–12 °C | Turno | Dentro de "cargas adicionales" `[SUPUESTO]` |
| **Hielo** (si se usa en chiller o despacho) | Fabricación de hielo | < 0 °C | Faena | No separado (incluido en el enfriado) |
| Contenedores reefer en muelle | Pre-enfriado y conexión | −18 °C | Exportación | No modelado (P3: prueba de diseño) |

## 3. Órdenes de magnitud por escala

`[ESTIMACIÓN]` con parámetros `[SUPUESTO]`. Bajo · **medio** · alto. Perfil P1 (90 % refrigerado / 10 % congelado; 3 d / 14 d en días de producción).

| Escala | Enfriado fresco kWf (TR) | Enfriado fresco kWe | Congelación kWf (medio) | Cámaras kWf (medio) |
|---|---|---|---|---|
| 2.500 | 46 (13) · **59 (17)** · 84 (24) | 11 · **20** · 37 | 3 | 2 |
| 5.000 | 91 (26) · **118 (33)** · 168 (48) | 23 · **39** · 73 | 6 | 5 |
| 10.000 | 182 (52) · **235 (67)** · 336 (96) | 46 · **78** · 146 | 13 | 10 |
| 20.000 | 365 (104) · **471 (134)** · 673 (191) | 91 · **157** · 292 | 26 | 19 |

Con P2 (40 % congelado) la congelación sube a 13 / 26 / 51 / 103 kWf y con P3 (50 % congelado + exportación) a 16 / 32 / 64 / 128 kWf (medio, 20 h/día de túnel).

**Lecturas y cautelas:**
1. **El enfriado del producto fresco domina** la carga frigorífica en P1: ~680 kJ por ave (medio), de los cuales ~41 % es el agua de reposición del chiller. Enfriar con **aire** en lugar de inmersión elimina esa agua pero agrega ventiladores y tiempo (DEC-026): el modelo no lo compara todavía.
2. La carga **instalada** de túneles es mucho mayor que la media: si el producto debe congelarse en 4–8 h (lotes) en vez de repartirse en 20 h, la potencia frigorífica del túnel se multiplica ×2,5–5. El modelo reporta la media; el dimensionamiento es de un proveedor.
3. **Contraste de consistencia:** el enfriado estimado desde abajo (78 kWe × 8 h ≈ 630 kWh/día a 10.000 aves/día) es mucho menor que el 35 % del indicador de proceso asignado a "frío de proceso" (~2.540 kWh/día). La diferencia puede ser hielo, salas, docks, pérdidas de distribución, bombas y ventiladores, o que el indicador de la UE incluya almacenamiento. **No se resuelve en esta fase** (DPV propuesta: balance frigorífico de un proveedor).
4. Todo se escala linealmente (test U01); una instalación real tiene escalones (compresores discretos) y reservas.

## 4. Refrigerantes — comparación conceptual (no se elige)

| Alternativa | Uso industrial típico | Escala | Eficiencia | Seguridad | Personal | Regulación |
|---|---|---|---|---|---|---|
| **Amoníaco (R717)** directo | Estándar histórico de frigoríficos y plantas de faena grandes | Medianas y grandes; sistemas "de baja carga" y paquetizados para menores | **Alta**, sobre todo en baja temperatura | **Tóxico** (clase B2L: tóxico, baja inflamabilidad; FTE-09C-19 `[PVDP]`): sala de máquinas, detección, ventilación, plan de emergencia; riesgo para personas y vecinos | **Operadores capacitados** en amoníaco; mantenimiento especializado | Normas de seguridad argentinas de instalaciones con amoníaco **no relevadas** (DPV propuesta); no afectado por Kigali (no es HFC) |
| **CO₂ (R744)** transcrítico | Supermercados y plataformas logísticas; en expansión a industria | Pequeñas a medianas-grandes | Buena en clima templado; **menor en clima caluroso** (verano argentino) salvo con eyectores/enfriamiento adiabático | No tóxico ni inflamable (A1), pero **presiones muy altas**; asfixiante en recintos cerrados | Técnicos formados en alta presión (oferta local a verificar) | No afectado por Kigali |
| **Cascada NH₃/CO₂** | Amoníaco confinado en sala de máquinas; CO₂ en planta (congelado, cámaras) | Medianas y grandes | Alta en baja temperatura | Reduce la carga y la exposición al amoníaco | Ambas competencias | — |
| **Sistemas indirectos** (glicol/salmuera como fluido secundario) | Enfriado de salas, agua helada, cámaras con refrigerante primario confinado | Todas | Menor (doble intercambio + bombeo) | El refrigerante primario queda en la sala de máquinas | Estándar | — |
| **HFC / mezclas** (R404A, R507, R448A, etc.) | Equipos comerciales y paquetizados | Pequeñas | Media | No tóxicos; algunos A1 | Amplia oferta de técnicos | **Kigali**: Argentina vigente desde 2020-02-20, congelamiento del consumo de HFC desde 2024 y licencias de importación (FTE-09C-15 `[PVDP]`); riesgo de costo y disponibilidad futura |
| **HFO y mezclas de bajo PCG** (R1234ze, R513A, etc.) | Chillers y equipos nuevos | Pequeñas a medianas | Media | Algunos levemente inflamables (A2L) | Técnicos actualizados | Alternativa post-Kigali; costo y disponibilidad local a verificar |
| Hidrocarburos (R290, propano) | Equipos compactos, enfriadores de agua con carga limitada | Pequeñas | Alta | **Inflamable** (A3): cargas limitadas | Específico | Normas de carga máxima |

**Cómo se relaciona con la escala (sin decidir):**

- A **2.500–5.000 aves/día** (~20–40 kWe de enfriado medio más cámaras y túneles pequeños) son técnicamente posibles equipos paquetizados (HFC/HFO, CO₂ o amoníaco de baja carga); pesa la disponibilidad de **servicio técnico local**.
- A **10.000–20.000 aves/día** (del orden de 250–700 kWf en proceso, más congelado según perfil), la práctica industrial habitual se inclina por **amoníaco** o **cascada NH₃/CO₂**, y aparecen la sala de máquinas, el personal especializado y el plan de emergencia como condiciones del sitio (distancia a viviendas, bomberos).
- La **vocación exportadora** (congelado a −18 °C o menos, lotes para contenedores) aumenta la importancia de la baja temperatura, donde el COP y el refrigerante más importan.
- **Modularidad:** el frío es uno de los sistemas que la arquitectura de expansión recomienda **dejar preparado** (sala de máquinas y troncales dimensionadas para crecer) y **construir por módulos** (compresores, túneles, cámaras) ([`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md)).

## 5. Qué hace falta

Balance frigorífico de al menos dos proveedores por escala y perfil (P1/P2/P3), normativa argentina de seguridad para amoníaco y CO₂, disponibilidad de técnicos y repuestos en la zona, temperatura de diseño de verano del sitio. Lista: [`../11_agua_efluentes/conclusiones_agua_efluentes.md` §6](../11_agua_efluentes/conclusiones_agua_efluentes.md).
