# Sistema de frío industrial: cargas y refrigerantes (conceptual)

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** mapa de cargas frigoríficas, diferencia entre **kW frigoríficos** y **kW eléctricos** (con COP declarado), **carga sensible preliminar del producto** por escala y comparación conceptual de refrigerantes. **No se calcula la capacidad frigorífica de la planta** (queda PENDIENTE del balance frigorífico), no se elige sistema, refrigerante ni proveedor, no se dimensiona sala de máquinas, no se calcula CAPEX. Congelado y cámaras: [`congelado_almacenamiento.md`](congelado_almacenamiento.md).
> **Modelo:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) v1.1 (bloque `frio`). Propiedades térmicas `[PVDP]` (FTE-09C-14); temperaturas, COP y factores `[SUPUESTO]`.

---

## 1. kW frigoríficos, TR, COP y kW eléctricos

| Unidad | Qué mide | Ejemplo (10.000 aves/día, medio) |
|---|---|---|
| **kW frigoríficos** (kWf) | Calor que el sistema **extrae** por unidad de tiempo | Carga sensible preliminar del producto: **~99 kWf** durante 8 h |
| **TR** | 1 TR = **3,517 kWf** | ~28 TR |
| **COP** (o EER) | kWf ÷ kWe | **Supuesto:** 4 · **3** · 2,3 para agua helada/hielo (−5/0 °C); 1,8 · **1,4** · 1,1 para congelado (−35/−40 °C) |
| **kW eléctricos aproximados** | kWf ÷ **COP supuesto** | ~33 kWe para el producto con COP 3 |

Toda conversión frigorífico → eléctrico del modelo se llama `kw_electricos_aprox_*`, tiene una fila `cop_supuesto_*` con el COP usado y **no es un consumo garantizado** (test **U10**; mutaciones M04 y M16). El COP real depende del refrigerante, del ciclo, de las temperaturas de evaporación y condensación y del clima del sitio (verano).

## 2. Carga sensible del producto ≠ carga frigorífica total

La v1.0 llamaba "~235 kWf" a la suma de producto + agua del chiller + 40 % de cargas adicionales, y podía leerse como la capacidad de la planta. **Se corrige**: el modelo separa lo que calcula y deja la carga total **PENDIENTE**.

| Componente | Qué calcula el modelo | 10.000 aves/día (bajo · **medio** · alto) | Estado |
|---|---|---|---|
| **Carga sensible preliminar asociada al enfriamiento del producto** | kg comestible × 3,5 kJ/(kg·K) × (38 − 4 °C), repartido en 8 h netas | **99** kWf (igual en los tres niveles) | `[ESTIMACIÓN]` con `[SUPUESTO]` |
| Enfriamiento del agua de reposición del chiller | L/ave × 4,186 × (18 − 1 °C), en 8 h | 47 · **69** · 111 kWf | `[ESTIMACIÓN]`, fila separada |
| Cargas adicionales ilustrativas (salas, docks, infiltración, motores, iluminación) | +25 · **40** · 60 % sobre las dos anteriores | 36 · **67** · 126 kWf | `[SUPUESTO]` ilustrativo, **no es un balance** |
| Congelación del producto (sensible + latente + sensible) | 296 kJ/kg × t/día congeladas, repartido en 20 h | 10 kWf (P1) · 39 (P2) · 49 (P3), medio | `[ESTIMACIÓN]` (solo producto) |
| **Carga frigorífica total de la planta** | — | **PENDIENTE** | Balance frigorífico posterior |

**El balance frigorífico posterior deberá sumar, según corresponda:** enfriamiento sensible del producto; congelación sensible; calor latente de congelación; transmisión por paredes, techos y pisos; infiltración de aire; apertura de puertas; personas; iluminación; motores y equipos; docks; salas de proceso climatizadas; cámaras; túneles (potencia instalada según tiempo de congelación, no media diaria); desescarche; otras cargas. Test **U24**: ninguna variable se denomina "capacidad frigorífica" y la carga total queda vacía (mutación M15).

## 3. Mapa de cargas

| Carga | Qué se enfría | Temperatura típica | Perfil | En el modelo v1.1 |
|---|---|---|---|---|
| **Chiller / enfriado de carcasas** | Carcasas ~38 → ~4 °C | Agua/hielo 0–2 °C | Faena | Carga sensible del producto |
| **Agua de reposición del chiller** | ~18 → ~1 °C | | Faena | Fila separada |
| **Menudencias y garras** | Enfriado rápido | 0–4 °C | Faena | Dentro del comestible |
| **Cámaras refrigeradas** | Producto ya frío: paredes, puertas, infiltración | 0–4 °C | 24 h, 365 días | Solo energía ilustrativa kWh/(t·día) `[SUPUESTO]`; potencia PENDIENTE |
| **Cámaras de congelado** | Producto a −18/−25 °C | −18/−25 °C | 24 h, 365 días | Idem |
| **Túneles / IQF** | +4 → −18 °C | Aire −30/−40 °C | Hasta 20 h/día (lotes) | Calor del producto; potencia instalada PENDIENTE |
| **Docks / antecámaras** | Aire, puertas, montacargas | 4–10 °C | Carga y despacho | Dentro de "adicionales ilustrativas" |
| **Salas climatizadas** | Personas, motores, iluminación, producto | 10–12 °C | Turno | Idem |
| **Hielo** | Fabricación de hielo | < 0 °C | Faena | No separado |
| Contenedores reefer en muelle | Pre-enfriado y conexión | −18 °C | Exportación | No modelado |

## 4. Carga sensible del producto por escala

`[ESTIMACIÓN]`; 8 h netas; COP `[SUPUESTO]`. Medio salvo indicación.

| Escala | Carga sensible preliminar del producto kWf (TR) | kWe aprox. con COP 3 | Agua de chiller kWf (bajo · medio · alto) | Congelación del producto kWf, P1 · P2 · P3 (20 h) |
|---|---|---|---|---|
| 2.500 | 25 (7) | 8 | 12 · 17 · 28 | 2 · 10 · 12 |
| 5.000 | 50 (14) | 17 | 23 · 35 · 56 | 5 · 20 · 25 |
| 10.000 | 99 (28) | 33 | 47 · 69 · 111 | 10 · 39 · 49 |
| 20.000 | 198 (56) | 66 | 94 · 138 · 222 | 20 · 79 · 99 |

**Lecturas:**
1. La carga sensible del producto es **física del producto**, no depende del nivel; lo que cambia entre niveles son el agua del chiller, las cargas adicionales y el COP.
2. En enfriado por **inmersión**, enfriar el agua de reposición del chiller puede pesar tanto como el producto (69 vs 99 kWf, medio): el método de enfriamiento (DEC-026) es también una decisión de frío.
3. Los túneles se dimensionan por **tiempo de congelación** de cada lote: si se congela en 4–8 h en vez de repartir en 20 h, la potencia instalada se multiplica ×2,5–5. El modelo solo da la media diaria del producto.

### 4.1 Brecha no cerrada: física del producto vs benchmark global

| | kWh eléctricos/día de frío de proceso (10.000 aves/día, medio) |
|---|---|
| Cálculo físico (producto + agua del chiller, con COP 3, 8 h) | ~450 |
| 35 % del indicador global de proceso asignado a "frío" (reparto `[SUPUESTO]` didáctico) | ~2.540 |
| **Relación** | **~5,7×** (5,2–6,2 según nivel) |

La brecha puede deberse a salas, docks, infiltración, hielo, bombas y ventiladores, pérdidas de distribución, a que el indicador de la UE incluya almacenamiento o congelado, o a que el reparto del 35 % no aplique. **No se cierra arbitrariamente** (ni ajustando el COP ni el reparto): se resolverá con un balance frigorífico de proveedor y con la suma bottom-up de equipos (DPV-09C-02 propuesta; [`demanda_energia.md` §6](demanda_energia.md)).

## 5. Refrigerantes — comparación conceptual (no se elige)

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

- A **2.500–5.000 aves/día** (cargas sensibles del producto de ~25–50 kWf, más agua de chiller, cámaras y túneles pequeños) son técnicamente posibles equipos paquetizados (HFC/HFO, CO₂ o amoníaco de baja carga); pesa la disponibilidad de **servicio técnico local**.
- A **10.000–20.000 aves/día** (carga sensible del producto ~100–200 kWf, más agua de chiller, salas, cámaras y túneles según perfil; total PENDIENTE), la práctica industrial habitual se inclina por **amoníaco** o **cascada NH₃/CO₂**, y aparecen la sala de máquinas, el personal especializado y el plan de emergencia como condiciones del sitio (distancia a viviendas, bomberos).
- La **vocación exportadora** (congelado a −18 °C o menos, lotes para contenedores) aumenta la importancia de la baja temperatura, donde el COP y el refrigerante más importan.
- **Modularidad:** el frío es uno de los sistemas que la arquitectura de expansión recomienda **dejar preparado** (sala de máquinas y troncales dimensionadas para crecer) y **construir por módulos** (compresores, túneles, cámaras) ([`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md)).

## 6. Qué hace falta

Balance frigorífico de al menos dos proveedores por escala y perfil (P1/P2/P3), normativa argentina de seguridad para amoníaco y CO₂, disponibilidad de técnicos y repuestos en la zona, temperatura de diseño de verano del sitio. Lista: [`../11_agua_efluentes/conclusiones_agua_efluentes.md` §7](../11_agua_efluentes/conclusiones_agua_efluentes.md).
