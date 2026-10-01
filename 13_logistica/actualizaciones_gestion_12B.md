# Propuestas de actualización de registros globales — sesión 12B (logística integral)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión en paralelo con 12A (Localización) y 12C (Layout/Obra civil). **No se editaron** `00_gestion_proyecto/`, `25_fuentes/` ni archivos de 12A/12C. Este archivo contiene lo que debe incorporarse al integrar la sesión.

> **IDs provisionales:** `SUP-12B-##`, `DPV-12B-##`, `DEC-12B-##`, `FTE-12B-###`. Al integrar, asignar el siguiente número libre de cada registro (al iniciar esta sesión los últimos eran **SUP-077, DPV-115, DEC-049 y FTE-268**) y reemplazar los IDs provisionales en `13_logistica/` (búsqueda de texto `12B-`), incluido `modelo_logistica.py` (comentarios y tabla `PARAMETROS_TABLA`) y `escenarios_logistica.csv` (regenerar con el modelo). Las fuentes provisionales están en [`fuentes_12B.csv`](fuentes_12B.csv), con el mismo formato que `25_fuentes/registro_fuentes.csv`.

---

## 1. `supuestos.md` — nuevos

| ID provisional | Supuesto | Área | Estado | Relacionado |
|---|---|---|---|---|
| SUP-12B-01 | **Distancias de sensibilidad** (no ubicaciones ni óptimos): radio granja–planta 25/50/100/150/200/300 km; fábrica–granja 25/75/150; incubadora–granja 150 (barrido 50–300); planta–AMBA y planta–puerto 30/150/300/600/1.000 km por ruta; planta–receptor de subproductos 10/50/150 | Logística | Vigente | DEC-003, 12A |
| SUP-12B-02 | **Factor de ruta** (km por ruta / km en línea recta) 1,2 / 1,3 / 1,4, base 1,3; valores internacionales 1,2–1,42 (FTE-12B-001 `[PVDP]`); sin dato argentino | Logística | Vigente | DPV-12B-07 |
| SUP-12B-03 | Distancia geográfica media dentro de un radio = **2/3 del radio** (granjas uniformes en un círculo; propiedad geométrica); distancia máxima = radio | Logística | Vigente | DPV-048 |
| SUP-12B-04 | Velocidades medias: troncal 70 km/h (60–80), urbana de reparto 20 km/h (15–30); aves vivas 60 km/h (de 03) — sin fuente | Logística | Vigente | DPV-12B-07 |
| SUP-12B-05 | Tiempos de aves vivas: carga en granja 1,5 h (1,0–2,5), espera y descarga en planta 1,0 h (0,5–2,0), lavado y desinfección 0,75 h (0,5–1,0), ayuno en granja antes de cargar 3 h (2–4); ayuno total máximo 10 h (8–12, FTE-156 `[PVDP]`) → **viaje admisible 4,5 h** | Aves vivas | Vigente | DPV-054, DPV-12B-01 |
| SUP-12B-06 | **Capacidades de vehículos = variables editables**, nunca estándar: aves vivas 4.000/5.500/7.000 aves (SUP-033; 5.500 = punto medio de barrido); granelero ~28 t (`[ESTIMACIÓN]` de 03); refrigerado y congelado: PENDIENTE (barrido 3/6/12/20 t); reparto 3/6 t; troncal 20 t; subproductos PENDIENTE (barrido 5/10/20 t); pollitos PENDIENTE (barrido 20/40/80 mil); contenedor 25 t (`[PVDP]` FTE-135) | Logística | Vigente | DPV-084 |
| SUP-12B-07 | Reducción de carga en verano: 15 % de las aves por camión (barrido 10–25 %), a partir de "1–2 aves menos por cajón" (03) | Aves vivas | Vigente | DPV-054 |
| SUP-12B-08 | **12 h útiles por camión-día** para calcular camión-día, flota mínima y paradas que caben en una ruta | Logística | Vigente | DPV-12B-08 |
| SUP-12B-09 | Calendario de despacho: refrigerado 5/6/7 despachos por semana; congelado 1/2/3/6 (acumulable); **desfase de 1 día** (lo faenado hoy se despacha desde mañana); la producción es de lunes a viernes (o sábado con 6 d) | Producto terminado | Vigente | DPV-078, DPV-085 |
| SUP-12B-10 | Reparto: 0,75 h por parada (0,5–1,0), 8 km entre paradas (5–15), máx. 6/10/15 paradas por ruta, 1 h de carga en andén, cross-dock a 25 km de las tiendas (15–40) — sin fuente | Distribución | Vigente | DPV-036, DPV-042 |
| SUP-12B-11 | **Escenarios de red ancla** A/B/C = fracción de locales adheridos 0 / 0,5 / 1 de los 90; volumen por local = barrido 25–300 kg/local/día (escenarios de prueba de 02). No es demanda; los escenarios son independientes y no sumables | Demanda / Distribución | Vigente | SUP-004, DPV-002 |
| SUP-12B-12 | Subproductos crudos: sin frío, **retiro dentro del día de faena**; acumulación > 1 día solo con frío y con admisibilidad sanitaria **PVDP** (no confirmada); tiempo máximo refrigerado PENDIENTE | Subproductos | Vigente | DPV-12B-03, DPV-066 |
| SUP-12B-13 | Reparto de la producción no vendida a la red entre otros canales = proporciones de ESC-BAS de 02 (mayorista 50 %, carnicerías/pollerías 33 %, gastronomía 10 %, elaborador 7 %), solo ilustrativo | Canales | Vigente | DPV-040 |
| SUP-12B-14 | **Backhaul = 0** por defecto; solo se aplica con evidencia (carga identificada o contrato). Prohibido en aves vivas y subproductos | Logística | Vigente | DPV-12B-14 |
| SUP-12B-15 | Exportación: 1 contenedor por camión portacontenedor; cada producto/destino en consolidación inmoviliza hasta 1 contenedor en cámara | Exportación | Vigente | DPV-027 |
| SUP-12B-16 | **Grupos de salida conjunta** de subproductos: G1 plumas, G2 sangre (cisterna), G3 vísceras + cabezas + huesos + otros C, G4 decomisos + contenido GI (+ DOA si se admite); compatibilidad real según receptor y normativa (`[PVDP]`) | Subproductos | Vigente | DPV-065, DPV-066 |

## 2. `datos_por_validar.md`

### 2.1 Nuevos

| ID provisional | Dato | Para qué | Fuente sugerida | Prioridad sugerida (plan de campo) |
|---|---|---|---|---|
| DPV-12B-01 | **Tiempos reales** de captura y carga por camión, espera y descarga en planta, lavado y desinfección; ayuno en granja | Ciclo del camión, flota, viaje admisible | Contratistas de captura; frigoríficos | N2 |
| DPV-12B-02 | **DOA vs distancia, duración y estación** en Argentina | Reemplazar el barrido independiente por una relación | SENASA (registros de inspección); frigoríficos | N3 |
| DPV-12B-03 | **Tiempo máximo y condiciones** de almacenamiento de sangre, vísceras y plumas (con y sin frío) aceptados por receptores y normativa; compatibilidad de corrientes en un mismo vehículo | Estrategias E2/E3/E4 | Plantas de rendering; SENASA; autoridad ambiental | N2 |
| DPV-12B-04 | **Envases y pallets**: kg de envase por kg de producto, kg por pallet, pallets por camión, tipo de pallet exigido por la red (retornable, pool) | Pallets, insumos, logística inversa | Red de supermercados; proveedores de envases | N3 |
| DPV-12B-05 | **Cama**: material disponible por zona, kg/m², reposición y retiro | Flujo de insumos y residuos de granja | Productores; proveedores | N4 |
| DPV-12B-06 | **Consumo de combustible** por tipo de vehículo (L/km cargado y vacío) y del equipo de frío | KPI económicos y huella | Transportistas; fabricantes | N4 |
| DPV-12B-07 | **Velocidades medias y factor de ruta reales** por zona candidata (caminos rurales, accesos, pasos urbanos) | Radio, ciclo, flota | 12A (rutas reales); transportistas | N2 |
| DPV-12B-08 | **Normativa de jornada y conducción** (CCT 40/89 y normativa nacional) y **pesos y dimensiones** (Ley 24.449, Dec. 779/95 Anexo R, Dec. 32/2018) — texto original | Flags de conducción y jornada; capacidades legales | Boletín Oficial; FADEEAC; Ministerio de Transporte | N3 |
| DPV-12B-09 | **Ventanas de recepción, pedido mínimo, vida útil remanente exigida, tipo de pallet y devoluciones** en la red | Rutas, ventanas, logística inversa | Red de supermercados (compras y logística) | N1 (con DPV-036) |
| DPV-12B-10 | **Tamaño de lote por galpón/granja y posibilidad de cosecha escalonada** compatible con el ritmo de faena (a 2.500 aves/día, una granja de 30.000 aves tarda ~11 días de faena en vaciarse) | Compatibilidad granja–planta en escala chica | Productores; integradoras; asesores | N2 |
| DPV-12B-11 | **Res. SENASA 723/2025** (texto): requisitos por tipo de vehículo (aves vivas, carnes, subproductos), lavado y desinfección, certificado único, DT-e | Habilitación de la flota; lavadero | Boletín Oficial; SENASA | N2 (amplía DPV-058) |
| DPV-12B-12 | **Decreto 4238/68 cap. XXVIII** (Res. ex-SENASA 745/1993): categorías A y B de transporte refrigerado, temperaturas, registro | Vehículos de producto terminado | SENASA | N2 (amplía DPV-098) |
| DPV-12B-13 | **Frecuencias de servicio reefer por destino, *cut-off*, espera en terminal** desde Buenos Aires / Dock Sud / Zárate | Lead time de exportación | Navieras; forwarders | N3 (amplía DPV-027) |
| DPV-12B-14 | **Oferta de transportistas** por tipo (jaula, refrigerado, congelado, granelero, cisterna, contenedores de subproductos) en zonas candidatas y AMBA; disposición a backhaul — **sin seleccionar** | Criterios C4/C5 de flota; backhaul | Cámaras de transporte; operadores | N3 |
| DPV-12B-15 | **Capacidad de los camiones de pollitos BB** (cajas por camión, pollitos por caja, clima) y si el transporte está incluido en el precio | Flujo I1 | Incubadoras | N3 (amplía DPV-047) |

### 2.2 Anotaciones a registros existentes

| Registro | Anotación propuesta (sesión 12B, 2026-10-01) |
|---|---|
| DPV-036 (red logística de supermercados) | Con planta a ≥ 300 km del AMBA el reparto directo cabe en ~2 paradas por jornada: 23 rutas y ~14.000 km/día para 90 locales × 100 kg (vs 1 viaje troncal vía CD). Preguntar además ventanas, pallets y devoluciones (DPV-12B-09). Ver `13_logistica/logistica_producto_terminado.md` §5 |
| DPV-054 (captura y transporte de aves) | Modelo: viajes, ocupación, ciclo y flota por radio y estación; viaje admisible ~4,5 h con los supuestos (radio > ~200 km de ruta fuera de ventana). Preguntar aves/camión con 2,9 kg por estación y tiempos de carga (DPV-12B-01) |
| DPV-084 (capacidades de vehículos) | El modelo logístico deja PENDIENTE todo resultado que dependa de una capacidad sin dato (1.018 cifras); solo SUP-033, el granelero de 03 y el contenedor tienen valor |
| DPV-048 (productores) | Agregar tamaño de lote por cosecha y posibilidad de alojamiento escalonado (DPV-12B-10) |
| DPV-065 (rendering) | Preguntar frecuencia y vehículo de retiro, contenedores rotativos, retiro conjunto de G1–G4 y retiro de viernes |
| DPV-085 (refrigerado/congelado por canal) | El congelado puede acumularse para llenar camiones (1–2 despachos/semana), intercambiando ocupación por stock (`logistica_producto_terminado.md` §3) |
| DPV-027 (exportación) | Usar la plantilla de datos para cotizar de `13_logistica/logistica_exportacion.md` §3 |
| DPV-009 (acceso a fuentes) | Sesión 12B: `EGRESS_BLOCKED` en argentina.gob.ar, boletinoficial.gob.ar y motivar.com.ar |
| SUP-033 (aves por camión) | Usado como barrido 4.000/5.500/7.000 en el modelo logístico; un extracto de foros (FTE-12B-004) indica 8–12 aves por jaula según peso, sin permitir derivar aves por camión |

## 3. `decisiones_pendientes.md`

### 3.1 Nuevas

| ID provisional | Decisión | Prioridad | Depende de | Carpeta |
|---|---|---|---|---|
| DEC-12B-01 | **Modelo de distribución a la red y a canales**: directo / CD del cliente / cross-dock propio o de operador / distribuidor (amplía DEC-016) | Alta | DPV-036, DPV-12B-09, DEC-003 (distancia al AMBA) | `13_logistica` |
| DEC-12B-02 | **Modalidad de flota por flujo** (pollitos, aves vivas, refrigerado, congelado, subproductos): propia / tercerizada / híbrida, con los criterios C1–C10 | Media | DPV-12B-14, DPV-042, DPV-054, escala | `13_logistica` |
| DEC-12B-03 | **Radio máximo admisible granja–planta** (bienestar, ayuno, estación), a fijar junto con la localización | Alta | DPV-054, DPV-12B-01/02/07, DEC-003 | `13_logistica`, `10_localizacion` |
| DEC-12B-04 | **Calendario de despacho e inventario**: despachos/semana del refrigerado, frecuencia del congelado, días de stock de seguridad y base temporal | Media | DPV-078, DPV-085, DPV-12B-09 | `13_logistica`, `12_energia_frio` |
| DEC-12B-05 | **Estrategia de retiro de subproductos por corriente** (diario / acumulación refrigerada / salida conjunta / contenedores rotativos) | Media | DPV-065, DPV-066, DPV-12B-03, DEC-027 | `13_logistica`, `07_subproductos` |
| DEC-12B-06 | **Tamaño de lote y esquema de cosecha** compatible con el ritmo de faena (lotes chicos, alojamiento escalonado o compra a terceros en escala chica) | Alta para escalas ≤ 5.000 | DPV-12B-10, DEC-020 | `03_produccion_primaria`, `13_logistica` |
| DEC-12B-07 | **Lavadero de camiones y cajones**: propio en planta vs establecimiento registrado de terceros (Res. 723/2025) | Media | DPV-12B-11, 12C (layout), 11 (efluentes) | `13_logistica`, `09_layout_obra_civil` |

### 3.2 Anotaciones

| Registro | Anotación propuesta |
|---|---|
| DEC-016 | Se amplía en DEC-12B-01 con el cross-dock y la comparación física (km/t, rutas, camión-horas) de `13_logistica/logistica_producto_terminado.md` §5.2 |
| DEC-003 | Insumos de 12B para 12A: viaje admisible ~4,5 h; ≥ 300 km al AMBA exige punto de quiebre en distribución; 600–1.000 km a puerto excede la jornada de un chofer |
| DEC-027 | La logística de subproductos (ocupación 1–48 % con retiro diario y vehículos de 5–20 t hasta 10.000 aves/día) es un argumento a pesar en rendering propio vs tercerizado |

## 4. `25_fuentes/registro_fuentes.csv`

Incorporar las 4 fuentes de [`fuentes_12B.csv`](fuentes_12B.csv) (FTE-12B-001 a 004), todas `[PVDP]`. **Fuentes existentes reutilizadas** (no se duplican): FTE-234 (Res. SENASA 723/2025), FTE-192 (Decreto 4238/68 por capítulos; agregar a `datos_extraidos`: "cap. XXVIII / Res. ex-SENASA 745/1993: transporte de carnes en vehículos habilitados; categoría A con equipo mecánico de frío, categoría B isotérmica sin equipo; lectura de temperatura visible desde el exterior — extracto 12B"), FTE-135 (reefer), FTE-156 (ayuno y DOA), FTE-147 (cama).

## 5. `estado_proyecto.md`

- Tablero: **Logística detallada (`13`)** → "**Completado** v1.0 (modelo físico, 20 tests; sin costos ni flota decidida)" · Evidencia de campo: "Pendiente — red de supermercados, contratistas, receptores, capacidades" · Síntesis: `13_logistica/conclusiones_logistica.md`.
- Hito 2026-10-01: "Logística integral (sesión 12B): mapa de flujos de insumos, aves vivas, producto refrigerado/congelado, subproductos y exportación; aves vivas por escala, radio, estación, DOA y merma; granjas abastecedoras y tamaño de lote; refrigerado vs congelado; directo vs CD vs cross-dock; red ancla A/B/C con volumen variable; inventario (días de producción vs calendario) y despacho; exportación por etapas y plantilla de cotización; subproductos con cuatro estrategias de retiro; flota propia/tercerizada/híbrida con criterios; KPI físicos y económicos; backhaul condicionado a evidencia; `modelo_logistica.py` (20/20 tests, reproduce 112 cifras de 23) → `escenarios_logistica.csv` (15.721 filas, 1.018 PENDIENTES). **Sin costos, sin escala, sin localización, sin transportistas.**"

## 6. Interfaces con 12A y 12C (para la reconciliación)

Ver [`conclusiones_logistica.md` §6](conclusiones_logistica.md). Si 12A o 12C registran supuestos sobre distancias, velocidades, lavadero o andenes, reconciliar con SUP-12B-01/04/05 y DEC-12B-07 para evitar duplicados (regla 13).
