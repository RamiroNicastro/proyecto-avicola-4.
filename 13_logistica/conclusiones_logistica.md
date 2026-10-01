# Conclusiones — logística integral (sesión 12B)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Fase 0 · **Modelo preliminar completado; evidencia de campo pendiente**

> Modelo físico de toda la cadena (insumos, aves vivas, producto refrigerado y congelado, red ancla, inventario, exportación, subproductos, flota, KPI, backhaul). **Sin costos**, sin escala elegida, sin localización, sin transportistas. Todas las cifras son `[ESTIMACIÓN]` sobre supuestos; **ninguna capacidad de vehículo está validada** (DPV-084) y el acceso a fuentes primarias siguió bloqueado (DPV-009: argentina.gob.ar, boletinoficial.gob.ar y motivar.com.ar con `EGRESS_BLOCKED`).

---

## 1. Hallazgos principales

1. **El problema de la escala chica es la densidad, no el volumen.** A 2.500 aves/día los flujos son pequeños pero su frecuencia la fijan relojes biológicos (ayuno, vida útil, degradación): camión de aves al 46 %, retiro diario de plumas al 6 % de 10 t, congelado diario al 4 % de 12 t. A 10.000–20.000 aves/día la ocupación sube a 75–100 % en los flujos principales.
2. **Aves vivas:** 1 / 1–2 / 2–3 / 3–6 viajes por día de faena según escala, capacidad (4.000–7.000 aves) y estación; el **verano agrega un viaje**. El DOA casi no cambia viajes pero sí aves pagadas y no faenadas (30 → 166 aves/día a 10.000 entre 0,3 % y 1,63 %).
3. **Radio:** con los supuestos (ayuno 10 h, 3 h previas, 1,5 h de carga, 1 h de espera) el viaje admisible es **4,5 h**; granjas a más de **~200 km de ruta** salen de la ventana de ayuno. **No se declara radio óptimo**: tiempo, bienestar, bioseguridad, costo y disponibilidad de productores no apuntan al mismo número.
4. **Tamaño de lote vs ritmo de faena (hallazgo nuevo):** una granja de 30.000 aves tarda ~11 días de faena en vaciarse a 2.500 aves/día. La escala chica es incompatible con granjas grandes "todo dentro–todo fuera" salvo lotes chicos o alojamientos escalonados (DPV-12B-10, DEC-12B-06).
5. **Alimento** es el mayor flujo físico: 3 / 5 / 9 / 18 entregas semanales de ~28 t; cada una es un evento de bioseguridad en granja.
6. **Refrigerado vs congelado:** el refrigerado se despacha casi a diario y genera stock de fin de semana (24 → 40 → 51 t de ciclo a 10.000 aves/día con 5 / 6 / 7 despachos); el congelado **se acumula** para llenar camiones, cambiando ocupación por stock.
7. **Red de supermercados:** con planta a ≥ 300 km del AMBA, el reparto directo a locales no es razonable (≈ 2 paradas por jornada; ~1.350 km/t vs ~57 km/t vía CD). Hace falta un **punto de quiebre**: CD del cliente, cross-dock u operador. Con la planta cerca del AMBA es posible, pero son 3–12 rutas diarias con 4–29 % de ocupación si cada local compra 25–100 kg/día. La red **no define la escala** (regla 8): sus escenarios A/B/C son independientes y no sumables.
8. **Inventario:** el stock nunca cambia los viajes; lo que los cambia es el **calendario de despacho**. Días de producción y días calendario siguen siendo bases distintas (7 días = 168 t vs 115 t a 10.000 aves/día).
9. **Exportación:** a 2.500 aves/día, aun con 20 % exportado, sale **un contenedor por mes**; a 20.000, ocho. El lead time total queda PENDIENTE (espera en terminal desconocida).
10. **Subproductos:** hasta 10.000 aves/día ningún grupo llena la mitad de un vehículo de 10 t con retiro diario. Acumular requiere frío y confirmación sanitaria (PVDP); la **salida conjunta** con contenedores rotativos es la palanca más prometedora, condicionada al receptor.
11. **Flota:** casi ningún flujo usa un vehículo dedicado a pleno en escalas chicas; aves vivas (37–49 % semanal) es el más crítico. No se decide; se dejan 10 criterios ([`flota_propia_vs_tercerizada.md`](flota_propia_vs_tercerizada.md)).

## 2. Escenarios por escala (resumen físico)

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves cargadas · t vivas/día | 2.508 · 7,3 | 5.015 · 14,5 | 10.030 · 29,1 | 20.060 · 58,2 |
| Viajes de aves/día (5.500; normal · verano) | 1 · 1 | 1 · 2 | 2 · 3 | 4 · 5 |
| Granjas equivalentes (30.000 plazas) | 4 | 8 | 16 | 32 |
| Alimento t/día · entregas/semana | 8,8 · 3 | 17,7 · 5 | 35,3 · 9 | 70,6 · 18 |
| Pollitos/semana plena | 13.197 | 26.395 | 52.790 | 105.580 |
| Comestible t/día operativo (B) | 6,0 | 12,0 | 24,0 | 47,9 |
| Refrigerado · congelado (P1), t/día | 5,4 · 0,6 | 10,8 · 1,2 | 21,6 · 2,4 | 43,1 · 4,8 |
| Subproductos a retirar t/día (B · C) | 1,5 · 2,3 | 3,0 · 4,7 | 6,1 · 9,4 | 12,2 · 18,8 |
| Contenedores/mes con 20 % exportado | 1 | 2 | 4 | 8 |

## 3. Datos faltantes que más mueven el modelo

| Prioridad | Dato | Registro |
|---|---|---|
| 1 | Red de supermercados: CD, ubicación, ventanas, pedido mínimo, pallets, fee | DPV-036, DPV-039, DPV-12B-09 |
| 2 | Capacidades útiles de vehículos (aves/camión por estación, refrigerado, granelero, subproductos, pollitos) | DPV-084, SUP-033, DPV-12B-15 |
| 3 | Radio real granja–planta, productores disponibles y su tamaño de lote | DPV-054, DPV-048, DPV-12B-10 |
| 4 | Receptores de subproductos: frecuencia, vehículo, compatibilidad, tiempo máximo refrigerado | DPV-065, DPV-066, DPV-12B-03 |
| 5 | Tiempos de captura, espera, lavado; DOA vs distancia y estación | DPV-12B-01, DPV-12B-02 |
| 6 | Proporción refrigerado/congelado por canal; vida útil | DPV-085, DPV-078 |
| 7 | Normativa: Res. 723/2025, Decreto 4238 cap. XXVIII, temperaturas, jornada de choferes, pesos y dimensiones | DPV-058, DPV-098, DPV-12B-08, 11, 12 |
| 8 | Velocidades y factor de ruta reales en zonas candidatas | DPV-12B-07 (con 12A) |
| 9 | Exportación: espera en terminal, tránsitos, frecuencias | DPV-027, DPV-12B-13 |
| 10 | Envases, pallets, cama, combustible | DPV-12B-04, 05, 06 |

En el CSV hay **1.018 cifras PENDIENTES**: todas son resultados que dependen de alguno de estos datos y que el modelo se niega a completar con valores por defecto.

## 4. Pruebas del modelo

`python3 13_logistica/modelo_logistica.py` → **20/20 pruebas OK** (más las de la escala, la producción, el balance y los subproductos al importarlos):

| Test | Qué valida |
|---|---|
| L01 | Conservación de t vivas: cargado = faenable + DOA + merma |
| L02 | Conservación en planta: vivo + agua = comestible + subproductos + efluente |
| L03 | Refrigerado + congelado + exportación = comestible; despacho semanal = producción semanal |
| L04 | Corrientes y grupos de subproductos = sólidos a retirar |
| L05 | Red + canales + exportación = comestible (sin vender más que la demanda) |
| L06 | Viajes enteros = techo de equivalentes; 0 carga → 0 viajes |
| L07 | Capacidad ≤ 0 → error en todos los flujos |
| L08 | 0 < ocupación ≤ 100 % (384 casos) |
| L09 | Distancia negativa → error; km ≥ 0 |
| L10 | Inventario separado del despacho (los viajes no cambian con el stock; dos bases) |
| L11 | Refrigerado y congelado con viajes, capacidad y filas separados |
| L12 | Escenarios ancla A/B/C independientes, no sumables, A sin red |
| L13 | Datos faltantes → PENDIENTE, nunca 0 ni valor por defecto |
| L14 | Reproduce 112 cifras de `23` (t vivas, comestible, sólidos, alimento, camiones, inventario) |
| L15 | Backhaul = 0 sin evidencia; prohibido en aves vivas y subproductos |
| L16 | Sin variables ni unidades económicas; unidades válidas |
| L17 | Escalas = las aprobadas en `23` |
| L18 | Distancia por ruta ≥ geográfica |
| L19 | Monotonía: DOA → aves y viajes; radio → km |
| L20 | Ventana de ayuno coherente |

## 5. Riesgos logísticos

| Riesgo | Flujo | Efecto físico | Señal en el modelo | Mitigación conceptual (sin decisión) |
|---|---|---|---|---|
| **Accidente** de camión de aves | V1 | Mortalidad masiva, bienestar, línea sin aves, imagen | 1 de 2–4 viajes del día = 25–50 % de la faena | Protocolo de emergencia, seguro, rutas, segundo proveedor |
| **Corte de ruta** (piquete, inundación, puente) | V1, P1, I2 | Aves sin llegar dentro del ayuno; producto fresco retenido | Viaje admisible 4,5 h: poco margen en radios > 150 km | Rutas alternativas, radio con margen, stock de seguridad de producto |
| **Ola de calor** | V1 | DOA ↑, menos aves por camión (+1 viaje), merma ↑ | Barrido verano −15 % y DOA hasta 1,63 % | Viajes nocturnos, menos densidad, espera ventilada, flota de reserva |
| **Falla de frío** (equipo del camión, cámara, reefer) | P1–P3 | Producto fuera de temperatura, decomiso, reclamo | Stock de ciclo 24–100 t en riesgo | Registradores, respaldo eléctrico de cámaras (12), contratos con cláusulas |
| **Congestión** (AMBA, accesos portuarios) | P1, P3 | Ventanas incumplidas, horas extra, menos paradas por ruta | Rutas que exceden jornada | Cross-dock, horarios nocturnos, CD del cliente |
| **Demoras** (captura, carga, terminal, buque) | V1, P3 | Ayuno excedido; certificados vencidos; stock acumulado | Lead time PENDIENTE | Programación, tolerancias, colchón de stock |
| **Mortalidad** en transporte | V1 | Aves pagadas no faenadas; material de destino restringido | 0,2–1,63 % | KPI de DOA por contratista, auditoría de bienestar |
| **Restricciones sanitarias** (IAAP, cierre de zonas, cuarentenas) | V1, I1, I2, P3 | Granjas inmovilizadas; exportación suspendida; rutas prohibidas | — | Granjas dispersas, mercados diversificados, plan de contingencia |
| **Avería de camión** | Todos | Viaje perdido; con flota mínima de 1–2 camiones, 50–100 % del flujo | Flota mínima 1 a 2.500–10.000 aves/día | Reserva, contrato de respaldo, mantenimiento |
| **Dependencia de un transportista** | V1, P1, S1–S4 | Un proveedor que falla o sube precio detiene la operación | Oferta local desconocida (DPV-12B-14) | ≥ 2 proveedores por flujo crítico o híbrido |
| Receptor de subproductos que deja de retirar | S1–S4 | La planta no puede faenar (material que se pudre en horas) | Retiro diario obligatorio | Segundo receptor, frío de contingencia, contenedores |
| Falta de reefers vacíos | P3 | Producto acumulado en cámara | — | Reserva anticipada, forwarder |

## 6. Interfaces con las sesiones paralelas (sin modificar sus archivos)

- **12A Localización:** necesita de 12B el **viaje admisible** (~4,5 h; > ~200 km de ruta fuera de ventana con los supuestos), el efecto de la distancia planta–AMBA sobre el modelo de distribución (≥ 300 km ⇒ punto de quiebre), y la distancia a puerto y a receptores. 12B necesita de 12A distancias por ruta reales, factores de ruta y velocidades por zona.
- **12C Layout/Obra civil:** debe prever andén de recepción de aves con espera ventilada para 1–5 camiones por día (intervalo entre arribos 2–18 h según escala), **lavadero de camiones y cajones** (DEC-12B-07), andenes de despacho separados para refrigerado, congelado y exportación, playa de contenedores de subproductos segregados (G1–G4, cisterna de sangre) y cámaras para stock de ciclo y de seguridad.

## 7. Qué NO se hizo

No se calcularon costos, CAPEX ni OPEX; no se seleccionaron transportistas, vehículos, CD, puerto ni receptor; no se eligió escala, radio, localización ni modalidad de flota; no se modificaron `00_gestion_proyecto/`, `25_fuentes/` ni archivos de 12A/12C. Las propuestas de registros están en [`actualizaciones_gestion_12B.md`](actualizaciones_gestion_12B.md).
