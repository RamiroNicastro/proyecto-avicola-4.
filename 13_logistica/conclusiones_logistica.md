# Conclusiones — logística integral (sesión 12B)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría final de interpretación) · Fase 0 · **Modelo preliminar completado; evidencia de campo pendiente**

> Modelo físico de toda la cadena (insumos, aves vivas, producto refrigerado y congelado, red ancla, inventario, exportación, subproductos, flota, KPI, backhaul). **Sin costos**, sin escala elegida, sin localización, sin transportistas. Todas las cifras son `[ESTIMACIÓN]` sobre supuestos de **escenario**; **ninguna capacidad de vehículo está validada ni cotizada** (DPV-084). El acceso directo a fuentes primarias siguió bloqueado desde la sesión (DPV-009).
> **v1.1:** la ventana prefaena se desagrega y sus resultados (tiempo de transporte disponible, alcance) se presentan como **resultados de escenario**, no como límites; la Res. SENASA 723/2025 queda trazada como confirmada en revisión externa y **sin** usarse para respaldar tiempos, distancias ni retorno vacío; el retorno de aves se describe como "sin carga comercial (con jaulas)"; la utilización sale del tiempo de ciclo; cada cifra de viajes indica su capacidad de escenario; los subproductos separan capacidad másica y volumétrica; la acumulación se evalúa en cinco dimensiones; la exportación es una sensibilidad.

---

## 1. Hallazgos principales (todos condicionados a los supuestos del escenario)

1. **El problema de la escala chica es la densidad, no el volumen.** Con las capacidades de escenario, a 2.500 aves/día los flujos son pequeños pero su frecuencia la fijan relojes biológicos: camión de aves de 5.500 al 46 %, retiro diario de plumas al 6 % de la capacidad **másica** de 10 t (volumétrica pendiente), congelado diario al 4 % de 12 t.
2. **Aves vivas:** con 4.000–7.000 aves por camión (escenario), 1 / 1–2 / 2–3 / 3–6 viajes por día de faena según escala y estación. Sin capacidad elegida, los viajes son PENDIENTE. El DOA casi no cambia viajes pero sí aves pagadas y no faenadas.
3. **Ventana prefaena ≠ tiempo de viaje.** La secuencia retiro de alimento → captura y carga → espera en granja → transporte → espera en planta → descarga se modela tramo por tramo. Con una **ventana de escenario de 10 h** (8–12 h citadas como práctica, sin norma primaria que fije un máximo) y los tramos supuestos, queda un **tiempo de transporte disponible de 4,5 h bajo la parametrización actual**, equivalente a un **alcance de ≈ 270 km por ruta (≈ 208 km de radio geográfico)** con 60 km/h y factor de ruta 1,3. Es un resultado del escenario, **no un radio reglamentario ni óptimo**: con ventana de 8 h el alcance baja a ~150 km por ruta; con 12 h o captura más rápida, sube a 300–390 km.
4. **Granjas grandes vs escala chica:** si un lote de 30.000 aves se retirara con la cadencia de una planta de 2.500 aves/día, tardaría ~11 días de faena (referencia de 03: 1–2 noches). Es una **incompatibilidad operativa potencial bajo el supuesto de esa cadencia**, no una conclusión: falta validar retiros parciales, all-in/all-out, tamaño real de lotes y programación entre granjas (DPV-133, DEC-060).
5. **Alimento** es el mayor flujo físico: 3 / 5 / 9 / 18 entregas semanales con un granelero de escenario de ~28 t.
6. **Refrigerado vs congelado:** el refrigerado se despacha casi a diario y genera stock de fin de semana (24 → 40 → 51 t de ciclo a 10.000 aves/día con 5 / 6 / 7 despachos); el congelado se puede acumular para llenar camiones, cambiando ocupación por stock.
7. **Directo vs CD:** con la parametrización actual (100 kg/local, 0,75 h por parada, 10 paradas máx., 12 h útiles, camiones de escenario de 6/20 t), **la distribución directa resulta mucho menos eficiente que la consolidación vía CD** cuando la planta está lejos del AMBA: a 300 km, 1.349 vs 57 km/t. La brecha se reduce mucho a 100–150 km (168–291 vs 19–29 km/t) y depende de kg/local, tiempo por parada y horas disponibles. **No hay frontera universal ni ganador declarado.**
8. **Inventario:** el stock no cambia los viajes; lo que los cambia es el calendario de despacho. Días de producción y días calendario siguen siendo bases distintas.
9. **Exportación (sensibilidad):** con 20 % exportado y 25 t por contenedor saldrían 1 / 2 / 4 / 8 contenedores por mes; el 20 % **no** es una estrategia prevista (demanda de exportación = 0). El lead time total queda PENDIENTE.
10. **Subproductos:** en masa, hasta 10.000 aves/día ningún grupo alcanza la mitad de la capacidad másica de un vehículo de 10 t con retiro diario; **para las plumas la restricción podría ser volumétrica** y no está medida (densidad aparente PENDIENTE). Acumular es posible solo si se confirman cinco condiciones (física, sanitaria, receptor, frío/recipiente, olores).
11. **Flota:** la utilización sale del tiempo de ciclo. El 37–49 % semanal de los camiones de aves (radio 100 km) es un resultado del escenario (5 días de faena, 1 ciclo de 6,1 h por jornada, pocos viajes), no de una prohibición; con 25 km caben 3 ciclos por jornada y con 300 km la utilización semanal llega a 71 %.

## 2. Escenarios por escala (resumen físico)

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves cargadas · t vivas/día | 2.508 · 7,3 | 5.015 · 14,5 | 10.030 · 29,1 | 20.060 · 58,2 |
| Viajes de aves/día **con 5.500 aves/camión (escenario)**; normal · verano | 1 · 1 | 1 · 2 | 2 · 3 | 4 · 5 |
| Granjas equivalentes (30.000 plazas) | 4 | 8 | 16 | 32 |
| Alimento t/día · entregas/semana (**granelero de escenario 28 t**) | 8,8 · 3 | 17,7 · 5 | 35,3 · 9 | 70,6 · 18 |
| Pollitos/semana plena | 13.197 | 26.395 | 52.790 | 105.580 |
| Comestible t/día operativo (B) | 6,0 | 12,0 | 24,0 | 47,9 |
| Refrigerado · congelado (P1), t/día | 5,4 · 0,6 | 10,8 · 1,2 | 21,6 · 2,4 | 43,1 · 4,8 |
| Subproductos a retirar t/día (B · C) | 1,5 · 2,3 | 3,0 · 4,7 | 6,1 · 9,4 | 12,2 · 18,8 |
| Contenedores/mes — **sensibilidad** 20 % exportado, 25 t | 1 | 2 | 4 | 8 |

## 3. Res. SENASA 723/2025: qué verifica y qué no

| | Contenido |
|---|---|
| **Trazabilidad** | La sesión 12B **no pudo abrir** el texto oficial (`EGRESS_BLOCKED` en argentina.gob.ar y boletinoficial.gob.ar). El texto oficial fue **confirmado en revisión externa del proyecto** (FTE-234; anotación integrada en `25_fuentes/registro_fuentes.csv` en la reconciliación de las sesiones 12 (2026-10-01)) |
| **Confirma** | Habilitación sanitaria de los vehículos alcanzados; requisitos de bienestar animal; ventilación/protección para aves; facilidad de lavado y desinfección; lavado/desinfección de superficies externas e internas a cada viaje; documentación sanitaria correspondiente |
| **NO respalda** | Un máximo general de 4,5 h de viaje; un máximo general de 200–270 km; una obligación general de retorno vacío. Esos puntos son **supuestos o resultados de modelización** (SUP-095, SUP-103) o **DPV** (DPV-127, DPV-058) |

## 4. Datos faltantes que más mueven el modelo

| Prioridad | Dato | Registro |
|---|---|---|
| 1 | Red de supermercados: CD, ubicación, ventanas, pedido mínimo, pallets, fee | DPV-036, DPV-039 |
| 2 | Capacidades útiles **validadas o cotizadas** (aves/camión por estación, refrigerado, granelero, subproductos en t y m³, pollitos) | DPV-084, SUP-033, DPV-047, DPV-135 |
| 3 | Tiempos reales de cada tramo prefaena y del ciclo (captura, esperas, descarga, lavado) | DPV-127 |
| 4 | Radio real granja–planta, productores, tamaño de lote y cadencia de retiro | DPV-054, DPV-048, DPV-133 |
| 5 | Receptores de subproductos: frecuencia, vehículo, m³, compatibilidad, acumulación aceptada | DPV-065, DPV-066, DPV-128 |
| 6 | **Densidad aparente** y volumen útil por corriente de subproducto | DPV-135 |
| 7 | Proporción refrigerado/congelado por canal; vida útil | DPV-085, DPV-078 |
| 8 | Normativa: requisitos detallados de la Res. 723/2025 por vehículo, Decreto 4238 cap. XXVIII, temperaturas, jornada, pesos y dimensiones | DPV-058, DPV-098, DPV-132 |
| 9 | Velocidades y factor de ruta reales; disponibilidad de flota y mantenimiento | DPV-116, DPV-136 |
| 10 | Exportación: espera en terminal, tránsitos, frecuencias; envases, pallets, cama, combustible | DPV-027, DPV-125, DPV-129, DPV-130, DPV-131 |

El CSV marca como **PENDIENTE** todo resultado que depende de alguno de estos datos; el modelo no los completa con valores por defecto.

## 5. Pruebas del modelo

`python3 13_logistica/modelo_logistica.py` → **28/28 pruebas OK** (los 20 originales y 8 controles de la auditoría), además de las pruebas de escala, producción, balance y subproductos al importarlos.

| Test | Qué valida |
|---|---|
| L01 | Conservación de t vivas: cargado = faenable + DOA + merma |
| L02 | Conservación en planta: vivo + agua = comestible + subproductos + efluente |
| L03 | Refrigerado + congelado + exportación = comestible; despacho semanal = producción semanal |
| L04 | Corrientes y grupos de subproductos = sólidos a retirar |
| L05 | Red + canales + exportación = comestible (sin vender más que la demanda) |
| L06 | Viajes enteros = techo de equivalentes; 0 carga → 0 viajes |
| L07 | Capacidad ≤ 0 → error en todos los flujos |
| L08 | 0 < ocupación ≤ 100 % |
| L09 | Distancia negativa → error; km ≥ 0 |
| L10 | Inventario separado del despacho (los viajes no cambian con el stock; dos bases) |
| L11 | Refrigerado y congelado con viajes, capacidad y filas separados |
| L12 | Escenarios ancla A/B/C independientes, no sumables, A sin red |
| L13 | Datos faltantes → PENDIENTE (incluye camión de aves sin capacidad elegida) |
| L14 | Reproduce 112 cifras de `23` |
| L15 | Backhaul = 0 sin evidencia; aves y subproductos deshabilitados por defecto; el estado "NO" queda reservado a prohibición con fuente |
| L16 | Sin variables ni unidades económicas; unidades válidas |
| L17 | Escalas = las aprobadas en `23` |
| L18 | Distancia por ruta ≥ geográfica |
| L19 | Monotonía: DOA → aves y viajes; radio → km |
| L20 | Ventana prefaena desagregada; alerta coherente; sin ventana → PENDIENTE |
| **L21** | Alcance/radio resultante nunca etiquetado como reglamentario, admisible u óptimo |
| **L22** | Cambiar tiempos de captura, esperas, retiro o descarga cambia el tiempo de transporte disponible y el alcance |
| **L23** | `BACKHAUL_AVES = false` por defecto, sin figurar como prohibición; retorno con jaulas ≠ vacío |
| **L24** | Utilización de flota = f(tiempo de ciclo con sus componentes) |
| **L25** | Toda fila de viajes/ocupación declara la capacidad usada y su tipo (ESCENARIO / PENDIENTE) |
| **L26** | Ocupación másica ≠ volumétrica; sin densidad aparente la volumétrica es PENDIENTE |
| **L27** | Exportación como SENSIBILIDAD con % exportado, payload y utilización explícitos |
| **L28** | Acumulación de subproductos: físico / sanitario / receptor / frío / olores separados y PENDIENTES sin evidencia |

## 6. Riesgos logísticos

| Riesgo | Flujo | Efecto físico | Señal en el modelo | Mitigación conceptual (sin decisión) |
|---|---|---|---|---|
| **Accidente** de camión de aves | V1 | Mortalidad masiva, bienestar, línea sin aves, imagen | Con 5.500 aves/camión, 1 de 2–4 viajes del día = 25–50 % de la faena | Protocolo de emergencia, seguro, rutas, segundo proveedor |
| **Corte de ruta** (piquete, inundación, puente) | V1, P1, I2 | Aves fuera de la ventana prefaena; producto fresco retenido | Tiempo de transporte disponible de escenario 4,5 h: poco margen en radios amplios | Rutas alternativas, margen en la programación, stock de seguridad de producto |
| **Ola de calor** | V1 | DOA ↑, menos aves por camión (+1 viaje), merma ↑ | Barrido verano −15 % y DOA hasta 1,63 % | Viajes nocturnos, menos densidad, espera ventilada, flota de reserva |
| **Falla de frío** (camión, cámara, reefer) | P1–P3 | Producto fuera de temperatura, decomiso, reclamo | Stock de ciclo 24–100 t en riesgo | Registradores, respaldo eléctrico de cámaras (12), contratos |
| **Congestión** (AMBA, accesos portuarios) | P1, P3 | Ventanas incumplidas, menos paradas por ruta | Rutas que exceden jornada | Cross-dock, horarios nocturnos, CD del cliente |
| **Demoras** (captura, carga, terminal, buque) | V1, P3 | Ventana prefaena excedida (alerta); certificados vencidos | `alerta_prefaena_excede_ventana`; lead time PENDIENTE | Programación, tolerancias, colchón de stock |
| **Mortalidad** en transporte | V1 | Aves pagadas no faenadas; material de destino restringido | 0,2–1,63 % | KPI de DOA por contratista, auditoría de bienestar |
| **Restricciones sanitarias** (IAAP, cierre de zonas) | V1, I1, I2, P3 | Granjas inmovilizadas; exportación suspendida | — | Granjas dispersas, mercados diversificados, plan de contingencia |
| **Avería de camión** | Todos | Viaje perdido; con flota mínima de 1–2 camiones, 50–100 % del flujo | Flota mínima de escenario | Reserva, contrato de respaldo, mantenimiento (DPV-136) |
| **Dependencia de un transportista** | V1, P1, S1–S4 | Un proveedor que falla detiene la operación | Oferta local desconocida (DPV-134) | ≥ 2 proveedores por flujo crítico o híbrido |
| Receptor de subproductos que deja de retirar | S1–S4 | La planta no puede sostener la faena (material que se degrada en horas) | Retiro diario como referencia | Segundo receptor, frío de contingencia, contenedores |
| Falta de reefers vacíos | P3 | Producto acumulado en cámara | — | Reserva anticipada, forwarder |

## 7. Interfaces con las sesiones paralelas (sin modificar sus archivos)

- **12A Localización:** 12B aporta el **tiempo de transporte disponible y el alcance de escenario** (4,5 h y ≈ 270 km por ruta con la parametrización actual; recalculables con `--ventana-prefaena`, `--t-captura-carga`, `--t-espera-planta`, etc.), la sensibilidad directo/CD/cross-dock por distancia planta–AMBA y las distancias a puerto y receptores. 12B necesita de 12A distancias por ruta reales, factores de ruta y velocidades por zona. **Ningún valor de 12B debe usarse como radio reglamentario.**
- **12C Layout/Obra civil:** andén de recepción de aves con espera ventilada para 1–5 camiones por día (capacidades de escenario), lavadero de camiones y cajones (DEC-061), andenes separados para refrigerado, congelado y exportación, playa de contenedores de subproductos segregados (G1–G4, cisterna de sangre; **dimensionar en m³ cuando haya densidades**) y cámaras para stock de ciclo y de seguridad.

## 8. Qué NO se hizo

No se calcularon costos, CAPEX ni OPEX; no se seleccionaron transportistas, vehículos, CD, puerto ni receptor; no se eligió escala, radio, localización ni modalidad de flota; no se modificaron `00_gestion_proyecto/`, `25_fuentes/` ni archivos de 12A/12C. Las propuestas de registros están en [`actualizaciones_gestion_12B.md`](actualizaciones_gestion_12B.md).
