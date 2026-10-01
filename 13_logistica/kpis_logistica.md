# KPI logísticos — definiciones y valores de referencia

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de interpretación) · Sesión 12B · Fase 0

> Se separan **KPI físicos** (calculables hoy con el modelo, sin precios) de **KPI económicos** (definidos, **no calculados**: requieren cotizaciones). Los valores de referencia son de un **caso de sensibilidad**, no de un escenario recomendado (bloque `kpi_resumen` de [`escenarios_logistica.csv`](escenarios_logistica.csv)).

---

## 1. KPI físicos

| KPI | Fórmula | Unidad | Uso | Flujo |
|---|---|---|---|---|
| **km por ave** | km totales del flujo / aves faenadas | km/ave | Compara radios y escalas | Aves vivas |
| **km por tonelada** | km totales / t transportadas | km/t | Densidad logística de un circuito | Todos |
| **t·km** | t × km cargado | t·km | Esfuerzo de transporte (base de costo futuro) | Todos |
| **Ocupación másica** | t / (viajes × capacidad másica de escenario) | % | Detecta camiones con poca carga en peso (≤ 100 %, test L08) | Todos |
| **Ocupación volumétrica** | m³ / (viajes × m³ útiles); m³ = t / densidad aparente | % | Restricción de materiales de baja densidad (plumas). **PENDIENTE** sin densidad (L26) | Subproductos |
| **Viajes/día** | techo(carga / capacidad) | viajes | Tamaño de la operación (test L06) | Todos |
| **t por camión** (t por viaje) | t / viajes | t/viaje | Aprovechamiento real | Todos |
| **Entregas** | paradas por día de despacho | paradas | Complejidad de la distribución | Red / canales |
| **kg por parada** | kg/local/día × 7 / entregas por semana | kg/parada | Costo por parada (inverso) | Red |
| **% de km sin carga comercial** | km de retorno sin carga comercial / km totales | % | 50 % en circuitos ida y vuelta sin backhaul comercial (supuesto conservador). El vehículo puede volver con envases/jaulas: no está físicamente vacío | Todos (calculado en aves vivas) |
| **Tiempo de ciclo** | ida + captura/carga + espera en granja + espera en planta + descarga + regreso + lavado/desinfección | h | Camiones necesarios, coordinación, utilización (L24) | Todos |
| **Ciclos posibles por camión y jornada** | piso(horas útiles / ciclo) | índice | Múltiples ciclos diarios con radios cortos | Aves vivas |
| **Camión-día** | camión-horas / horas útiles por camión-día | camión-día | Flota equivalente | Todos |
| **Utilización de flota** (diaria y semanal) | viajes × ciclo / (flota × horas útiles); semanal × días de faena / 7 | % | Criterio C1 de flota; resultado del ciclo, no de una prohibición de otros usos | Todos |
| **Flota mínima** | max(horas, alimentación continua de la línea) | camiones | Orden de magnitud de vehículos | Aves vivas |
| **Intervalo entre arribos** | aves por camión / aves por hora de línea | h | Coordinación captura–faena | Aves vivas |
| **Ave·hora en tránsito** | aves cargadas × h de viaje | ave·h | Exposición (bienestar), no daño | Aves vivas |
| **DOA** | aves muertas al llegar / aves cargadas | % | Calidad de la logística de vivo | Aves vivas |
| **Merma de viaje** | kg perdidos en viaje y espera / kg cargados | % | Contrato granja–planta | Aves vivas |
| **Tiempo total prefaena** | retiro de alimento + captura/carga + espera en granja + transporte + espera en planta + descarga | h | Bienestar e inocuidad | Aves vivas |
| **Tiempo de transporte disponible (escenario)** | ventana prefaena configurada − tramos que no son transporte | h | Resultado del escenario, **no límite sanitario** | Aves vivas |
| **Alcance de escenario** | tiempo disponible × velocidad supuesta (÷ factor de ruta para el radio geográfico) | km | **No es radio reglamentario ni óptimo** | Aves vivas |
| **Alerta prefaena** | tiempo total prefaena > ventana configurada | flag | Señal, no infracción | Aves vivas |
| **Días para llenar un vehículo/contenedor** | capacidad / t por día | d | Acumulación vs degradación | Subproductos, congelado, exportación |
| **Stock de ciclo y t·día inmovilizadas** | ciclo semanal producción–despacho | t, t·d | Cámara y capital de trabajo **físico** | Producto terminado |
| **Contenedores/mes** | t exportadas/mes / carga | contenedores | Regularidad de embarques | Exportación |
| **Rutas inviables en jornada** | paradas que no caben en las horas útiles | flag | Necesidad de CD / cross-dock | Red |

## 2. Valores de referencia (caso de sensibilidad)

Radio 100 km (factor de ruta 1,3), perfil P1, refrigerado 6 y congelado 2 despachos/semana. **Capacidades de escenario** (no validadas ni cotizadas): 5.500 aves/camión, 12 t refrigerado/congelado, granelero ~28 t, 10 t másicas para subproductos (m³ PENDIENTE). Cada fila del CSV `kpi_resumen` lleva la capacidad en `capacidad_vehiculo`.

| KPI | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves vivas: viajes/día | 1 | 1 | 2 | 4 |
| Aves vivas: ocupación | **46 %** | 91 % | 91 % | 91 % |
| Aves vivas: km por ave | 0,069 | 0,035 | 0,035 | 0,035 |
| Aves vivas: km por t viva | 23,8 | 11,9 | 11,9 | 11,9 |
| Aves vivas: % km sin carga comercial (retorno con jaulas) | 50 % | 50 % | 50 % | 50 % |
| Aves vivas: tiempo de ciclo | 6,1 h | 6,1 h | 6,1 h | 6,1 h |
| Aves vivas: flota mínima · utilización diaria · semanal | 1 · 51 · 37 % | 1 · 51 · 37 % | 2 · 51 · 37 % | 3 · 68 · 49 % |
| Refrigerado: viajes/día de despacho (ocupación) | 1 (37 %) | 1 (75 %) | 2 (75 %) | 3 (100 %) |
| Congelado: viajes por despacho (ocupación) | 1 (12 %) | 1 (25 %) | 1 (50 %) | 1 (100 %) |
| Alimento: entregas/semana | 3 | 5 | 9 | 18 |
| Vísceras + cabezas (G3): % de capacidad másica, retiro diario | 5 % | 10 % | 21 % | 42 % |
| Plumas: % de capacidad másica, retiro diario | 6 % | 12 % | 24 % | 48 % |
| Plumas: ocupación volumétrica | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |

La **ocupación** es el KPI que mejor resume el problema de escala: con estas capacidades de escenario, a 2.500 aves/día casi todos los vehículos salen con menos de la mitad de su capacidad másica (la volumétrica, relevante para plumas, está pendiente).

## 3. KPI económicos (definidos, NO calculados)

| KPI | Fórmula | Requiere |
|---|---|---|
| Costo logístico por ave | USD de todos los fletes / aves faenadas | Tarifas (DPV-027, 042, 054) |
| Costo por kg entregado, por canal | USD de distribución del canal / kg entregados | DPV-042, fee de CD (DPV-039) |
| Costo por parada | USD de la ruta / paradas | DPV-042 |
| Costo por t·km | USD / t·km | Tarifas |
| Costo del km sin carga comercial | km sin carga comercial × USD/km | Tarifas, consumo (DPV-12B-06) |
| Costo de la merma y del DOA | kg × precio del kg vivo | Precios (DPV-013) |
| Capital de trabajo inmovilizado | t·día en stock × costo por t × días | Costos de producción (`20`) |
| Costo de retiro de subproductos | USD por retiro o por t (positivo, cero o negativo) | DPV-065 |
| Net-back de exportación | precio FOB/CFR − logística − certificaciones | DPV-027, `17` |
| Costo de flota propia vs tercerizada | Costo total de propiedad vs tarifa | `19`, `20` |

Ningún KPI económico se estima en esta fase (instrucción de la sesión 12B y regla 3).
