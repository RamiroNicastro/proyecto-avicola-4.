# KPI logísticos — definiciones y valores de referencia

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 12B · Fase 0

> Se separan **KPI físicos** (calculables hoy con el modelo, sin precios) de **KPI económicos** (definidos, **no calculados**: requieren cotizaciones). Los valores de referencia son de un **caso de sensibilidad**, no de un escenario recomendado (bloque `kpi_resumen` de [`escenarios_logistica.csv`](escenarios_logistica.csv)).

---

## 1. KPI físicos

| KPI | Fórmula | Unidad | Uso | Flujo |
|---|---|---|---|---|
| **km por ave** | km totales del flujo / aves faenadas | km/ave | Compara radios y escalas | Aves vivas |
| **km por tonelada** | km totales / t transportadas | km/t | Densidad logística de un circuito | Todos |
| **t·km** | t × km cargado | t·km | Esfuerzo de transporte (base de costo futuro) | Todos |
| **Ocupación** | carga / (viajes × capacidad) | % | Detecta camiones medio vacíos (≤ 100 %, test L08) | Todos |
| **Viajes/día** | techo(carga / capacidad) | viajes | Tamaño de la operación (test L06) | Todos |
| **t por camión** (t por viaje) | t / viajes | t/viaje | Aprovechamiento real | Todos |
| **Entregas** | paradas por día de despacho | paradas | Complejidad de la distribución | Red / canales |
| **kg por parada** | kg/local/día × 7 / entregas por semana | kg/parada | Costo por parada (inverso) | Red |
| **% de km vacíos** | km de retorno vacío / km totales | % | Sin backhaul = 50 % en circuitos ida y vuelta | Todos (calculado en aves vivas) |
| **Tiempo de ciclo** | carga + ida + espera/descarga + vuelta + lavado | h | Camiones necesarios, coordinación | Todos |
| **Camión-día** | camión-horas / horas útiles por camión-día | camión-día | Flota equivalente | Todos |
| **Utilización de flota** | camión-horas / (flota × horas útiles) | % | Criterio C1 de flota (propia vs tercero) | Todos |
| **Flota mínima** | max(horas, alimentación continua de la línea) | camiones | Orden de magnitud de vehículos | Aves vivas |
| **Intervalo entre arribos** | aves por camión / aves por hora de línea | h | Coordinación captura–faena | Aves vivas |
| **Ave·hora en tránsito** | aves cargadas × h de viaje | ave·h | Exposición (bienestar), no daño | Aves vivas |
| **DOA** | aves muertas al llegar / aves cargadas | % | Calidad de la logística de vivo | Aves vivas |
| **Merma de viaje** | kg perdidos en viaje y espera / kg cargados | % | Contrato granja–planta | Aves vivas |
| **Dentro de la ventana de ayuno** | h de viaje ≤ viaje admisible | flag | Bienestar e inocuidad | Aves vivas |
| **Días para llenar un vehículo/contenedor** | capacidad / t por día | d | Acumulación vs degradación | Subproductos, congelado, exportación |
| **Stock de ciclo y t·día inmovilizadas** | ciclo semanal producción–despacho | t, t·d | Cámara y capital de trabajo **físico** | Producto terminado |
| **Contenedores/mes** | t exportadas/mes / carga | contenedores | Regularidad de embarques | Exportación |
| **Rutas inviables en jornada** | paradas que no caben en las horas útiles | flag | Necesidad de CD / cross-dock | Red |

## 2. Valores de referencia (caso de sensibilidad)

Radio 100 km (factor de ruta 1,3), 5.500 aves/camión, perfil P1, refrigerado 6 y congelado 2 despachos/semana con camiones de 12 t, alimento con granelero de ~28 t, retiro diario de subproductos con 10 t (todas las capacidades son **barrido**):

| KPI | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves vivas: viajes/día | 1 | 1 | 2 | 4 |
| Aves vivas: ocupación | **46 %** | 91 % | 91 % | 91 % |
| Aves vivas: km por ave | 0,069 | 0,035 | 0,035 | 0,035 |
| Aves vivas: km por t viva | 23,8 | 11,9 | 11,9 | 11,9 |
| Aves vivas: % km vacíos | 50 % | 50 % | 50 % | 50 % |
| Aves vivas: tiempo de ciclo | 6,1 h | 6,1 h | 6,1 h | 6,1 h |
| Aves vivas: flota mínima · utilización | 1 · 51 % | 1 · 51 % | 2 · 51 % | 3 · 68 % |
| Refrigerado: viajes/día de despacho (ocupación) | 1 (37 %) | 1 (75 %) | 2 (75 %) | 3 (100 %) |
| Congelado: viajes por despacho (ocupación) | 1 (12 %) | 1 (25 %) | 1 (50 %) | 1 (100 %) |
| Alimento: entregas/semana | 3 | 5 | 9 | 18 |
| Vísceras + cabezas (G3): ocupación del retiro diario | 5 % | 10 % | 21 % | 42 % |
| Plumas: ocupación del retiro diario | 6 % | 12 % | 24 % | 48 % |

La **ocupación** es el KPI que mejor resume el problema de escala: a 2.500 aves/día, casi todos los vehículos salen con menos de la mitad de su capacidad.

## 3. KPI económicos (definidos, NO calculados)

| KPI | Fórmula | Requiere |
|---|---|---|
| Costo logístico por ave | USD de todos los fletes / aves faenadas | Tarifas (DPV-027, 042, 054) |
| Costo por kg entregado, por canal | USD de distribución del canal / kg entregados | DPV-042, fee de CD (DPV-039) |
| Costo por parada | USD de la ruta / paradas | DPV-042 |
| Costo por t·km | USD / t·km | Tarifas |
| Costo del km vacío | km vacíos × USD/km | Tarifas, consumo (DPV-12B-06) |
| Costo de la merma y del DOA | kg × precio del kg vivo | Precios (DPV-013) |
| Capital de trabajo inmovilizado | t·día en stock × costo por t × días | Costos de producción (`20`) |
| Costo de retiro de subproductos | USD por retiro o por t (positivo, cero o negativo) | DPV-065 |
| Net-back de exportación | precio FOB/CFR − logística − certificaciones | DPV-027, `17` |
| Costo de flota propia vs tercerizada | Costo total de propiedad vs tarifa | `19`, `20` |

Ningún KPI económico se estima en esta fase (instrucción de la sesión 12B y regla 3).
