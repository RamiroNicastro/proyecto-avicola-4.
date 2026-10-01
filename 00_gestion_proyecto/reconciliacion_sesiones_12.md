# Reconciliación de las sesiones paralelas 12A, 12B y 12C

**Fecha:** 2026-10-01 · **Tipo:** sesión administrativa de integración (no investiga temas nuevos) · **Rama:** `ccr-b6229ce7-ydckhv`

> **Qué hace este documento:** registra cómo se integraron en los registros maestros (`supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `glosario.md`, `estado_proyecto.md`, `matriz_validacion_campo.csv`, `25_fuentes/`) los resultados de tres sesiones que trabajaron en paralelo con IDs provisionales: **12A Localización**, **12B Logística** y **12C Layout y obra civil**. **No** se tomó ninguna decisión, **no** se eligió región, terreno, escala, flota, arquitectura de red ni número de líneas, **no** se modificó la lógica de ningún modelo (solo IDs en comentarios, textos y tablas de parámetros; los CSV regenerados resultaron idénticos byte a byte al reemplazo textual) y **no** se resolvieron contradicciones (§7).
> **No se iniciaron** recursos humanos, incubación, alimento balanceado, CAPEX ni OPEX.

---

## 1. Sesiones reconciliadas

| Sesión | Alcance | Carpeta | IDs provisionales | Estado tras la reconciliación |
|---|---|---|---|---|
| **12A** | Localización industrial v1.1 (metodología, matriz por corredor, gates, auditoría) | `10_localizacion` | SUP-12A-01…13, DPV-12A-01…12, DEC-12A-01…06, FTE-12A-001…017 | Integrada. `actualizaciones_gestion_12A.md` queda como **archivo histórico** |
| **12B** | Logística integral v1.1 (modelo físico de flujos) | `13_logistica` | SUP-12B-01…17, DPV-12B-01…17, DEC-12B-01…07, FTE-12B-001…004 (+ anotación de FTE-234) | Integrada. `actualizaciones_gestion_12B.md` histórico |
| **12C** | Layout y obra civil v1.0.1 (programa de áreas, superficies, terreno conceptual, expansión) | `09_layout_obra_civil` | SUP-12C-01…17, DPV-12C-01…11, DEC-12C-01…05, FTE-12C-001…010 | Integrada. `actualizaciones_gestion_12C.md` histórico |

Últimos IDs oficiales al iniciar: **SUP-077, DPV-115, DEC-049, FTE-268** (coinciden con los declarados por las tres sesiones).

**Archivos `fuentes_12A.csv`, `fuentes_12B.csv`, `fuentes_12C.csv`:** su contenido completo está en `25_fuentes/registro_fuentes.csv`. Siguiendo la práctica de la reconciliación 09 debían retirarse, pero **el borrado no fue autorizado en el entorno** de esta sesión; se conservan como **históricos no activos** (los READMEs y los `actualizaciones_gestion_12*.md` lo indican). Retirarlos queda a criterio del promotor.

## 2. Mapa de IDs provisionales → definitivos

Todos los IDs provisionales fueron reemplazados en `09_layout_obra_civil/`, `10_localizacion/` y `13_logistica/` (documentos, `matriz_localizacion.csv`, `pesos_localizacion.csv`, comentarios y tablas de parámetros de los tres modelos y CSV de salida regenerados). Solo permanecen, como historia, en los tres `actualizaciones_gestion_12*.md` (marcados **ARCHIVO HISTÓRICO**), en los tres `fuentes_12*.csv` históricos y en este documento.

### 2.1 Supuestos (47 provisionales → 46 nuevos)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| SUP-12A-01 | **SUP-078** | Alta nueva |
| SUP-12A-02 | **SUP-079** | Alta nueva |
| SUP-12A-03 | **SUP-080** | Alta nueva |
| SUP-12A-04 | **SUP-081** | Alta nueva |
| SUP-12A-05 | **SUP-082** | Alta nueva |
| SUP-12A-06 | **SUP-083** | Alta nueva |
| SUP-12A-07 | **SUP-084** | Alta nueva |
| SUP-12A-08 | **SUP-085** | Fusionado con SUP-12B-11 en SUP-085 (escenarios de red/cliente ancla) |
| SUP-12A-09 | **SUP-086** | Alta nueva |
| SUP-12A-10 | **SUP-087** | Alta nueva |
| SUP-12A-11 | **SUP-088** | Alta nueva |
| SUP-12A-12 | **SUP-089** | Alta nueva |
| SUP-12A-13 | **SUP-090** | Alta nueva |
| SUP-12B-01 | **SUP-091** | Alta nueva |
| SUP-12B-02 | **SUP-092** | Alta nueva |
| SUP-12B-03 | **SUP-093** | Alta nueva |
| SUP-12B-04 | **SUP-094** | Alta nueva |
| SUP-12B-05 | **SUP-095** | Alta nueva |
| SUP-12B-06 | **SUP-096** | Alta nueva |
| SUP-12B-07 | **SUP-097** | Alta nueva |
| SUP-12B-08 | **SUP-098** | Alta nueva |
| SUP-12B-09 | **SUP-099** | Alta nueva |
| SUP-12B-10 | **SUP-100** | Alta nueva |
| SUP-12B-11 | **SUP-085** | Fusionado con SUP-12A-08 en SUP-085 (escenarios de red/cliente ancla) |
| SUP-12B-12 | **SUP-101** | Alta nueva |
| SUP-12B-13 | **SUP-102** | Alta nueva |
| SUP-12B-14 | **SUP-103** | Alta nueva |
| SUP-12B-15 | **SUP-104** | Alta nueva |
| SUP-12B-16 | **SUP-105** | Alta nueva |
| SUP-12B-17 | **SUP-106** | Alta nueva |
| SUP-12C-01 | **SUP-107** | Alta nueva |
| SUP-12C-02 | **SUP-108** | Alta nueva |
| SUP-12C-03 | **SUP-109** | Alta nueva |
| SUP-12C-04 | **SUP-110** | Alta nueva |
| SUP-12C-05 | **SUP-111** | Alta nueva |
| SUP-12C-06 | **SUP-112** | Alta nueva |
| SUP-12C-07 | **SUP-113** | Alta nueva |
| SUP-12C-08 | **SUP-114** | Alta nueva |
| SUP-12C-09 | **SUP-115** | Alta nueva |
| SUP-12C-10 | **SUP-116** | Alta nueva |
| SUP-12C-11 | **SUP-117** | Alta nueva |
| SUP-12C-12 | **SUP-118** | Alta nueva |
| SUP-12C-13 | **SUP-119** | Alta nueva |
| SUP-12C-14 | **SUP-120** | Alta nueva |
| SUP-12C-15 | **SUP-121** | Alta nueva |
| SUP-12C-16 | **SUP-122** | Alta nueva |
| SUP-12C-17 | **SUP-123** | Alta nueva |

### 2.2 Datos por validar (40 provisionales → 30 nuevos + 7 consolidaciones en existentes)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DPV-12A-01 | **DPV-116** | Fusionado con DPV-12B-07 en DPV-116 (ruteo: distancias, tiempos, velocidades, factor de ruta) |
| DPV-12A-02 | **DPV-117** | Alta nueva |
| DPV-12A-03 | **DPV-118** | Alta nueva |
| DPV-12A-04 | **DPV-119** | Alta nueva |
| DPV-12A-05 | **DPV-120** | Fusionado con DPV-12A-12 en DPV-120 (exposición sanitaria por corredor) |
| DPV-12A-06 | **DPV-121** | Alta nueva |
| DPV-12A-07 | **DPV-122** | Alta nueva |
| DPV-12A-08 | **DPV-123** | Alta nueva |
| DPV-12A-09 | **DPV-124** | Alta nueva |
| DPV-12A-10 | **DPV-125** | Fusionado con DPV-12B-13 en DPV-125 (nodos portuarios reefer) |
| DPV-12A-11 | **DPV-126** | Alta nueva |
| DPV-12A-12 | **DPV-120** | Fusionado con DPV-12A-05 en DPV-120 |
| DPV-12B-01 | **DPV-127** | Alta nueva |
| DPV-12B-02 | **DPV-054** | Consolidado en DPV-054 (DOA real vs distancia, duración y estación) |
| DPV-12B-03 | **DPV-128** | Alta nueva |
| DPV-12B-04 | **DPV-129** | Alta nueva |
| DPV-12B-05 | **DPV-130** | Alta nueva |
| DPV-12B-06 | **DPV-131** | Alta nueva |
| DPV-12B-07 | **DPV-116** | Fusionado con DPV-12A-01 en DPV-116 |
| DPV-12B-08 | **DPV-132** | Alta nueva |
| DPV-12B-09 | **DPV-036** | Consolidado en DPV-036 (ventanas, pedido mínimo, vida útil, pallet, devoluciones de la red) |
| DPV-12B-10 | **DPV-133** | Alta nueva |
| DPV-12B-11 | **DPV-058** | Consolidado en DPV-058 (texto Res. SENASA 723/2025 por tipo de vehículo) |
| DPV-12B-12 | **DPV-098** | Consolidado en DPV-098 (Decreto 4238/68 cap. XXVIII, transporte refrigerado) |
| DPV-12B-13 | **DPV-125** | Fusionado con DPV-12A-10 en DPV-125 |
| DPV-12B-14 | **DPV-134** | Alta nueva |
| DPV-12B-15 | **DPV-047** | Consolidado en DPV-047 (capacidad de camiones de pollitos) |
| DPV-12B-16 | **DPV-135** | Alta nueva |
| DPV-12B-17 | **DPV-136** | Alta nueva |
| DPV-12C-01 | **DPV-137** | Alta nueva |
| DPV-12C-02 | **DPV-138** | Alta nueva |
| DPV-12C-03 | **DPV-139** | Alta nueva |
| DPV-12C-04 | **DPV-140** | Alta nueva |
| DPV-12C-05 | **DPV-141** | Alta nueva |
| DPV-12C-06 | **DPV-142** | Alta nueva |
| DPV-12C-07 | **DPV-143** | Alta nueva |
| DPV-12C-08 | **DPV-144** | Alta nueva |
| DPV-12C-09 | **DPV-106** | Consolidado en DPV-106 (bomberos e higiene y seguridad por sitio) |
| DPV-12C-10 | **DPV-145** | Alta nueva |
| DPV-12C-11 | **DPV-058** | Consolidado en DPV-058 (lavado y desinfección de camiones) |

### 2.3 Decisiones pendientes (18 provisionales → 17 nuevas + 1 consolidación)

| ID provisorio | ID definitivo | Tratamiento |
|---|---|---|
| DEC-12A-01 | **DEC-050** | Alta nueva |
| DEC-12A-02 | **DEC-051** | Alta nueva |
| DEC-12A-03 | **DEC-052** | Alta nueva |
| DEC-12A-04 | **DEC-053** | Alta nueva |
| DEC-12A-05 | **DEC-054** | Alta nueva |
| DEC-12A-06 | **DEC-055** | Alta nueva |
| DEC-12B-01 | **DEC-016** | Consolidada en DEC-016 (modelo de distribución: se agregan cross-dock y CD del cliente) |
| DEC-12B-02 | **DEC-056** | Alta nueva |
| DEC-12B-03 | **DEC-057** | Alta nueva |
| DEC-12B-04 | **DEC-058** | Alta nueva |
| DEC-12B-05 | **DEC-059** | Alta nueva |
| DEC-12B-06 | **DEC-060** | Alta nueva |
| DEC-12B-07 | **DEC-061** | Alta nueva |
| DEC-12C-01 | **DEC-062** | Alta nueva |
| DEC-12C-02 | **DEC-063** | Alta nueva |
| DEC-12C-03 | **DEC-064** | Alta nueva |
| DEC-12C-04 | **DEC-065** | Alta nueva |
| DEC-12C-05 | **DEC-066** | Alta nueva |

### 2.4 Fuentes (31 provisionales → 29 nuevas + 2 consolidaciones; 1 anotación)

| ID provisorio | ID definitivo | Fuente | Tratamiento |
|---|---|---|---|
| FTE-12A-001 | **FTE-269** | Estimaciones agrícolas: series de superficie y producción de maíz y so | Alta nueva |
| FTE-12A-002 | **FTE-270** | Capas de información geográfica (red vial; límites de partidos y depar | Alta nueva |
| FTE-12A-003 | **FTE-271** | Red vial nacional; tránsito medio diario anual (TMDA); tramos en autop | Alta nueva |
| FTE-12A-004 | **FTE-272** | Estadísticas y normales climatológicas por estación (temperaturas máxi | Alta nueva |
| FTE-12A-005 | **FTE-273** | Información de recursos hídricos: riesgo hídrico; acuíferos y calidad  | Alta nueva |
| FTE-12A-006 | **FTE-274** | Visor de información geoespacial agropecuaria (suelos; uso del suelo) | Alta nueva |
| FTE-12A-007 | **FTE-275** | Sistema de transporte de energía eléctrica (red de alta tensión y nodo | Alta nueva |
| FTE-12A-008 | **FTE-276** | Red de gasoductos troncales y distribuidoras de gas natural | Alta nueva |
| FTE-12A-009 | **FTE-277** | Calidad de servicio de distribuidoras eléctricas (indicadores de durac | Alta nueva |
| FTE-12A-010 | **FTE-278** | Registros georreferenciados de establecimientos avícolas (RENSPA) y co | Alta nueva |
| FTE-12A-011 | **FTE-279** | Registro de parques industriales (oferta; servicios; actividades admit | Alta nueva |
| FTE-12A-012 | **FTE-280** | Precios de pizarra de granos y referencias de fletes de cereales | Alta nueva |
| FTE-12A-013 | **FTE-281** | Autoridades hídricas y ambientales provinciales: límites de vuelco; pe | Alta nueva |
| FTE-12A-014 | **FTE-282** | Servicios de contenedores refrigerados por terminal (Zárate; Gran Rosa | Alta nueva |
| FTE-12A-015 | **FTE-283** | Faena Provincial 2024–2025 (participación provincial en la faena de av | Alta nueva |
| FTE-12A-016 | **FTE-284** | Faena Provincial 2025–2026 | Alta nueva |
| FTE-12A-017 | **FTE-285** | Publicación de SENASA del 2024-07-02 sobre la concentración de la acti | Alta nueva |
| FTE-12B-001 | **FTE-286** | Selected country circuity factors for road travel distance estimation  | Alta nueva |
| FTE-12B-002 | **FTE-287** | Convenio Colectivo de Trabajo 40/89 (choferes de camiones) - jornada y | Alta nueva |
| FTE-12B-003 | **FTE-288** | Ley 24.449 de Tránsito art. 53, Decreto 779/95 Anexo R (pesos y dimens | Alta nueva |
| FTE-12B-004 | **FTE-289** | Capacidad de jaulas para transporte de pollos: aves por jaula según pe | Alta nueva |
| FTE-12C-001 | **FTE-224** | Frigorífico Mark S.A., una planta aviar de vanguardia (Pymes exportan, | Consolidada en FTE-224 (misma URL: INTI Pymes exportan, Frigorífico MARK) |
| FTE-12C-002 | **FTE-290** | Avex inauguró su planta de faena | Alta nueva |
| FTE-12C-003 | **FTE-291** | Se inauguró la Planta de Faena de Aves en China Muerta | Alta nueva |
| FTE-12C-004 | **FTE-292** | Manual on meat cold store operation and management | Alta nueva |
| FTE-12C-005 | **FTE-293** | How to Determine the Right Cold Storage Size for Your Facility | Alta nueva |
| FTE-12C-006 | **FTE-294** | Reglas de dimensionamiento de tratamiento de efluentes (carga superfic | Alta nueva |
| FTE-12C-007 | **FTE-218** | Small-scale poultry processing (FAO); Small-Scale Poultry Processing ( | Consolidada en FTE-218 (misma URL: FAO faena en pequeña escala) |
| FTE-12C-008 | **FTE-295** | 1000BPH Compact Chicken Processing Plant | Alta nueva |
| FTE-12C-009 | **FTE-296** | Sala de faena avícola de Ayacucho (construcción) | Alta nueva |
| FTE-12C-010 | **FTE-297** | The Complete Guide to Designing a Hygienic Poultry Processing Plant (L | Alta nueva |

| Fila de `fuentes_12B.csv` | Tratamiento |
|---|---|
| FTE-234 (Res. SENASA 723/2025) | **No es fuente nueva**: anotación integrada en FTE-234 (texto oficial confirmado en revisión externa; qué respalda y qué **no** respalda) |
| (propuesta 12B en `actualizaciones_gestion_12B.md` §4) | Anotación integrada en FTE-192 (cap. XXVIII, transporte refrigerado, extracto `[PVDP]`) |

## 3. Registros nuevos

### 3.1 Supuestos (SUP-078 a SUP-123) — supuestos metodológicos y criterios de modelo

Ninguno se elevó a hecho: todos `Vigente` como hipótesis, con marca explícita (`[CRITERIO DE MODELO]`, `[SUPUESTO METODOLÓGICO]`, `[SUPUESTO DE SENSIBILIDAD]`, `[PARÁMETROS DE ESCENARIO]`, `[CAPACIDADES DE ESCENARIO]`, `[PROXY]`, `[PRINCIPIO DE DISEÑO PRELIMINAR]`).

| Módulo | Supuesto / criterio de modelo (no hecho) | Registro |
|---|---|---|
| Localización | Umbral de cobertura **75 %** (criterio de control, no estándar MCDA) con **sensibilidad 60 / 75 / 90 %** obligatoria; faltantes > 40 %; comparabilidad ≥ 2 unidades y ≥ 50 % de regiones | SUP-081 |
| Localización | **Radio sanitario de 50 km** usado en el análisis (SAN-03) y radios de levantamiento 100 / 150 / 200 / 300 km: convenciones de relevamiento, no zonas de control ni límites | SUP-086 |
| Localización | **EXP-04 ≥ 3** como condición metodológica para que la distancia a puerto (EXP-01) aporte puntaje | SUP-088 |
| Localización | Distancias viales a CABA estimadas sin medición (**factor de distancia supuesto**) | SUP-079 |
| Localización | **Perfiles de ponderación** A–D ilustrativos; reparto ECOSISTEMA / EXPOSICIÓN / CLIMA; pesos iguales por subcriterio | SUP-080, SUP-082 |
| Localización | Corredores; normalización min-max sin imputación; `PROVINCIA_NORMA` vs `PROVINCIA_AGREGADO`; no monotónicos sin normalización lineal; gates duro/condicional; envolvente por faltantes ≠ intervalo de confianza | SUP-078, SUP-083, SUP-084, SUP-087, SUP-089, SUP-090 |
| Localización + Logística | Escenarios de cliente / red ancla (S0–S2 de 12A y A/B/C de 12B) | SUP-085 (fusión) |
| Logística | **Factor de circuidad** (ruta / línea recta) 1,2 / 1,3 / 1,4; distancia media = 2/3 del radio; distancias y velocidades de sensibilidad | SUP-092, SUP-093, SUP-091, SUP-094 |
| Logística | **Ventana prefaena** de escenario 10 h y **tiempos de carga / espera** (retiro 3 h, captura 1,5 h, espera en planta 0,75 h, descarga 0,25 h, lavado 0,75 h): alcance ≈ 270 km = resultado, no límite | SUP-095 |
| Logística | **Capacidades vehiculares de escenario** (sin elección → PENDIENTE) y **payload de contenedor** 25 t | SUP-096, SUP-104 |
| Logística | **`BACKHAUL_AVES = false`**: supuesto conservador, no prohibición | SUP-103 |
| Logística | **Parámetros directo vs CD / cross-dock** (tiempo por parada, km entre paradas, paradas máximas, cross-dock a 25 km) | SUP-100 |
| Logística | **Frecuencia de despachos** (refrigerado 5/6/7 por semana; congelado 1/2/3/6; desfase 1 día); 12 h útiles y tiempo de ciclo; reducción de verano; reparto a otros canales; acumulación en cinco dimensiones; grupos G1–G4; másica ≠ volumétrica | SUP-099, SUP-098, SUP-097, SUP-102, SUP-101, SUP-105, SUP-106 |
| Layout | **Proxies de superficie** k × driver^0,8 sin footprint; **footprints pendientes** (nunca cero) | SUP-107 |
| Layout | **Buffers** (10 / 20 / 40 m, proxy) y **retiros** (5 / 10 / 15 m, supuesto) del terreno | SUP-121 |
| Layout | **Reserva de expansión** (con o sin escala objetivo; rendering) | SUP-119 |
| Layout | **Factores de circulación** (interna 15 / 22 / 30 %; pesada 25 / 35 / 50 %); envolvente 2,2 / 2,8 / 3,5 | SUP-111, SUP-117, SUP-120 |
| Layout | **Una vs dos líneas** (× 1,05–1,15 por separación) y automatización | SUP-109 |
| Layout | Recepción, enfriamiento, frío, expedición, subproductos, servicios, personas (proxy, no dotación), efluentes, nueve zonas, principio de expansión | SUP-108, SUP-110, SUP-112 a SUP-116, SUP-118, SUP-122, SUP-123 |

### 3.2 Decisiones (DEC-050 a DEC-066) — todas `Abierta`, sin resultado

| Tema que sigue abierto | Decisión |
|---|---|
| Región / corredor | DEC-003 (anotada), DEC-055 (lista corta), DEC-050 (metodología), DEC-051 (ponderación), DEC-054 (criterios de control) |
| Terreno | DEC-052 (gates y umbrales), DEC-063 (cuánto terreno asegurar) |
| Arquitectura una planta vs planta + CD | DEC-053 |
| Flota propia / tercerizada / híbrida | DEC-056 |
| Modelo de distribución | DEC-016 (ampliada) |
| Escala final para reservar terreno | DEC-063 |
| Rendering futuro | DEC-066 (reserva de terreno), DEC-027 (destino; anotada) |
| Congelado propio / tercerizado | DEC-064 |
| Una vs dos líneas | DEC-038 (anotada; sin recomendación) |
| Otras nuevas | DEC-057 (radio de abastecimiento), DEC-058 (calendario de despacho), DEC-059 (retiro de subproductos), DEC-060 (tamaño de lote), DEC-061 (lavadero), DEC-062 (forma de nave), DEC-065 (laboratorio) |

### 3.3 Glosario

21 términos nuevos (no existía ninguno): gate duro, gate condicional, criterio no monotónico, cobertura de información, envolvente por faltantes, toneladas-kilómetro, backhaul, tiempo de ciclo, capacidad másica, capacidad volumétrica, footprint, buffer, programa de áreas (pedidos) + layout, factor de envolvente, FOS / FOT, m² construidos / operativos / terreno, expansión modular (propuestos por 12C) + cross-dock, corredor y arquitectura de red R1 / R2 (términos centrales de 12A–12B sin definición). "Gate (puerta) de expansión" ya existía y no se duplicó.

## 4. Datos por validar integrados y priorizados

**30 nuevos (DPV-116 a DPV-145)**, todos `Pendiente` salvo **DPV-124 `En curso`** (existe rango conceptual de 12C, **no validado**). **Ningún DPV se marcó validado**: no hay evidencia admitida nueva en el repositorio. Cada uno tiene prioridad en *Observaciones* y fila en `matriz_validacion_campo.csv` (ahora 145 DPV; nuevos: N2 19 · N3 7 · N4 4; ninguno N1). Las prioridades de 12A y 12C se copiaron; las de 12B (que solo traía nivel N) se asignaron en la reconciliación y así se indica.

| Tema pedido | DPV | Prioridad | Nivel · ola |
|---|---|---|---|
| Terrenos: superficie requerida | DPV-124 | CRÍTICO ANTES DE ELEGIR TERRENO | N2 · O8 |
| Retiros municipales, FOS, FOT, alturas, distancias a viviendas | DPV-141 | CRÍTICO ANTES DE COMPRAR TERRENO | N2 · O8 |
| Riesgo hídrico | DPV-118 | IMPORTANTE ANTES DE ELEGIR TERRENO | N2 · O8 |
| Terrenos: parques industriales | DPV-119 | IMPORTANTE ANTES DE ELEGIR TERRENO | N2 · O8 |
| Exposición sanitaria por corredor | DPV-120 (fusión) | IMPORTANTE ANTES DE LA LISTA CORTA | N2 · O0 |
| Servicios avícolas por corredor | DPV-126 | IMPORTANTE ANTES DE LA LISTA CORTA | N2 · O4 |
| Granjas por corredor | DPV-023 (anotado: georreferenciado), DPV-048, DPV-133 (tamaño de lote) | — / CRÍTICO (N1) / IMPORTANTE ANTES DE DEFINIR ESCALA (≤ 5.000) | N2 · O4 / N1 · O4 / N2 · O4 |
| Incubadoras | DPV-047 (ampliado: camiones de pollitos), DPV-023 | CRÍTICO ANTES DE DEFINIR ESCALA | N1 · O4 |
| Agua / energía / vuelco | DPV-053, DPV-052, DPV-087, DPV-067, DPV-106 (anotados; DPV-106 ampliado con bomberos) | IMPORTANTE / CRÍTICO ANTES DE ELEGIR LOCALIZACIÓN | N2 · O8 |
| Distancias, tiempos y velocidades reales | DPV-116 (fusión) | IMPORTANTE ANTES DE LA LISTA CORTA | N2 · O0 |
| Puertos reefer | DPV-125 (fusión) | IMPORTANTE ANTES DE ESTUDIAR EXPORTACIÓN DIRECTA | N3 · O9 |
| Capacidades reales de camiones | DPV-084 (anotado), DPV-132 (pesos y dimensiones, jornada), DPV-047 | ÚTIL / IMPORTANTE ANTES DE DEFINIR LA FLOTA | N4 / N3 |
| Tiempos reales de ciclo | DPV-127, DPV-136 (disponibilidad de flota), DPV-054 (ampliado: DOA) | IMPORTANTE ANTES DE DISEÑAR / ÚTIL | N2 · O3 / N3 · O3 |
| CD de supermercados | DPV-036 (ampliado: ventanas, pedido mínimo, vida útil, pallet, devoluciones), DPV-129 (envases y pallets) | IMPORTANTE ANTES DE INVERTIR (N1) / ÚTIL | N1 · O1 / N3 · O1 |
| Densidad / volumen de subproductos | DPV-135, DPV-128 (acumulación) | IMPORTANTE ANTES DE DISEÑAR / ANTES DE INVERTIR | N2 · O5 |
| Footprints de maquinaria | DPV-137 | IMPORTANTE ANTES DE DISEÑAR (anteproyecto) | N2 · O7 |
| Dotación | DPV-138 (requerida por la planta), DPV-121 (oferta por corredor) | IMPORTANTE ANTES DE DISEÑAR / ANTES DE INVERTIR | N2 |
| Requisitos edilicios SENASA | DPV-140, DPV-090 (anotado), DPV-115 (anotado) | IMPORTANTE / CRÍTICO ANTES DE DISEÑAR | N2 · O0→O6 |
| Otros | DPV-117 (maíz y soja), DPV-122 (calor), DPV-123 (población), DPV-130 (cama), DPV-131 (combustible), DPV-134 (transportistas), DPV-139 (transporte del personal), DPV-142 (estiba), DPV-143 (superficies reales), DPV-144 (superficie de efluentes), DPV-145 (layout exportación/Halal) | ver registro | — |

## 5. Registros consolidados, anotados y correcciones cruzadas

### 5.1 Consolidaciones (sin duplicar)

| Tipo | Caso | Resultado |
|---|---|---|
| Fusión 12A + 12B | SUP-12A-08 + SUP-12B-11 → **SUP-085** | Escenarios de ancla; se conservan ambas parametrizaciones (T12-05) |
| Fusión 12A + 12B | DPV-12A-01 + DPV-12B-07 → **DPV-116** | Un solo relevamiento de ruteo (distancias, tiempos, velocidades, factor de ruta) |
| Fusión 12A + 12B | DPV-12A-10 + DPV-12B-13 → **DPV-125** | Nodos portuarios reefer (costos y fletes siguen en DPV-027) |
| Fusión interna 12A | DPV-12A-05 + DPV-12A-12 → **DPV-120** | Exposición sanitaria por corredor (mismo actor y pedido) |
| Consolidación en existente | DPV-12B-02 → DPV-054; DPV-12B-09 → DPV-036; DPV-12B-11 + DPV-12C-11 → DPV-058; DPV-12B-12 → DPV-098; DPV-12B-15 → DPV-047; DPV-12C-09 → DPV-106 | "Dato requerido" ampliado + anotación fechada; filas de la matriz anotadas |
| Consolidación en existente | DEC-12B-01 → **DEC-016** | Modelo de distribución ampliado (cross-dock, CD del cliente) |
| Fuente misma URL | FTE-12C-001 → **FTE-224**; FTE-12C-007 → **FTE-218** | Entradas maestras con URL y datos adicionales |
| Fuente existente | FTE-234 y FTE-192 | Anotaciones de 12B (no filas nuevas) |
| Límite de alcance (sin fusionar) | DPV-126 (servicios avícolas) vs DPV-134 (transportistas) | Transportistas de aves vivas solo en DPV-134 |
| Límite de alcance (sin fusionar) | DPV-121 (oferta de mano de obra) vs DPV-138 (dotación requerida) | Complementarios |
| Límite de alcance (sin fusionar) | DEC-053 (arquitectura de red) vs DEC-016 (modelo de distribución) | Ambas abiertas, referenciadas entre sí |

### 5.2 Solapamientos revisados

| Par | Tema | Resolución administrativa |
|---|---|---|
| 12A + 12C | Superficie de terreno | DPV-124 `En curso` con el rango de 12C; `terreno_ideal.md` §4 y `conclusiones_localizacion.md` §11 anotados |
| 12A + 12C | Retiros, buffers, zonificación | Retiro real = DPV-141; buffer de diseño = SUP-121; reserva sanitaria/ambiental y zonificación = DPV-106; uso de suelo = gate duro (SUP-089) |
| 12A + 12C | Expansión | Escala objetivo a reservar = DEC-063; criterio de localización en DEC-003 (anotada) |
| 12A + 12C | Servicios, riesgo hídrico, efluentes | DPV-052/053/087/106 anotados; riesgo hídrico = DPV-118 (G-C1); tecnología de efluentes ↔ terreno = DEC-043 + DPV-144 (T12-10) |
| 12A + 12B | Distancias, corredores, AMBA | SUP-079 (por corredor) ≠ SUP-091 (sensibilidad); medición única en DPV-116 |
| 12A + 12B | CD, red de supermercados | DPV-036 ampliado; SUP-085; DEC-016 y DEC-053 |
| 12A + 12B | Puerto | DPV-125; SUP-088 (EXP-04 ≥ 3); payload SUP-104 |
| 12B + 12C | Capacidades de camiones | SUP-096 (escenario 12B) vs proxies de 12C: tensión T12-06; DPV-084 |
| 12B + 12C | Docks, circulación pesada | SUP-113, SUP-117 dependen de SUP-096 y SUP-099 (D12-01) |
| 12B + 12C | Producto refrigerado / congelado | SUP-099 (frecuencia) y SUP-112 (m² de cámara); DEC-058, DEC-064 |
| 12B + 12C | Subproductos | SUP-101/105/106 ↔ SUP-114; DPV-128, DPV-135; DEC-059 |
| 12B + 12C | Recepción y lavado | SUP-095 vs SUP-108 (T12-07); DPV-058 (ampliado), DEC-061 |

### 5.3 Correcciones cruzadas

- **Río Negro (no se borró historia).** `01_mercado/mercado_avicola_argentina.md` §3.1 conserva "2,5 %" y ahora indica su **año (2025), universo (faena SENASA) y fuente (extracto de FTE-001, `[PVDP]`)**, junto al dato de 12A: **~2,41 % en 2024**, universo **faena habilitada por SENASA**, tabla oficial SAGyP "Faena Provincial 2024–2025" (**FTE-283**, *confirmado en revisión externa del proyecto; lectura directa pendiente en entorno Claude*). Se agregaron M139–M143 a `datos_mercado.csv` (2024, cinco provincias) y se anotó M083. Son años distintos: no se restan ni promedian (regla 18). La "actividad avícola ~90 % en ER y BA" (FTE-285) es otro universo.
- **Superficie.** Estado global actualizado en `estado_proyecto.md`, DPV-124, `terreno_ideal.md` §4 y `conclusiones_localizacion.md` §11: *"Existe rango conceptual preliminar de 12C; superficie real de terreno sigue pendiente de municipio, efluentes, footprints y estrategia de expansión."*
- **Logística + layout.** Dependencia futura documentada en §8 (D12-01) y en SUP-113, SUP-117 y DPV-084.

### 5.4 Registros existentes anotados (con fecha, sin borrar historia)

- **Supuestos:** SUP-004, SUP-014, SUP-021, SUP-033, SUP-055, SUP-056, SUP-057, SUP-059, SUP-064.
- **Datos por validar:** consolidados DPV-036, DPV-047, DPV-054, DPV-058, DPV-098, DPV-106; anotados DPV-009, DPV-018, DPV-023, DPV-027, DPV-048, DPV-050, DPV-052, DPV-053, DPV-065, DPV-067, DPV-084, DPV-085, DPV-087, DPV-090, DPV-095, DPV-109, DPV-114, DPV-115; leyenda en el encabezado.
- **Decisiones:** DEC-016 (ampliada), DEC-003, DEC-012, DEC-020, DEC-026, DEC-027, DEC-033, DEC-035, DEC-038, DEC-043.
- **Fuentes:** FTE-224 y FTE-218 (maestras), FTE-234, FTE-192, FTE-001, FTE-134, FTE-259.

## 6. Fuentes

**29 nuevas (FTE-269 a FTE-297)** en `25_fuentes/registro_fuentes.csv` y `25_fuentes/bibliografia.md` (por tipo, con nota de sesión): 12A FTE-269–285, 12B FTE-286–289, 12C FTE-290–297. Validación: 297 filas, 11 columnas, IDs únicos y sin huecos; ninguna URL de las sesiones 12 duplicada (queda solo el duplicado preexistente FTE-001/FTE-071, T-13 de la reconciliación 09). Tipos normalizados al registro (`prensa` → `comercial`, `organismo_internacional` → `internacional`, `conocimiento_tecnico` → `tecnica`).

| Trazabilidad | Fuentes |
|---|---|
| **Confirmado en revisión externa del proyecto; lectura directa pendiente en entorno Claude** | FTE-283 (SAGyP, Faena Provincial 2024–2025), FTE-285 (SENASA, 2024-07-02), FTE-234 (Res. SENASA 723/2025, anotación) |
| Identificada en revisión externa; no leída | FTE-284 (SAGyP, Faena Provincial 2025–2026) |
| Identificadas, no consultadas | FTE-269 a FTE-282 (fuentes oficiales y comerciales para completar la matriz de localización) |
| `[PVDP]` / `[PVDP · débil]` | FTE-286 a FTE-297 |

Las URL exactas de FTE-283 a FTE-285 no pudieron registrarse (acceso bloqueado; DPV-009). La reconciliación, por ser administrativa, no intentó lecturas nuevas.

## 7. Contradicciones / tensiones abiertas

Ninguna se resolvió. Cada una queda con el registro que la cerrará.

| ID | Tensión | Módulos | Detalle | Qué la cierra |
|---|---|---|---|---|
| **T12-01** | **Mejor ecosistema avícola vs mayor exposición sanitaria** | 12A | Las zonas con más productores, incubadoras y servicios suelen tener más densidad de granjas, movimientos y eventos de IAAP; la densidad es criterio no monotónico (TOF-01) | DEC-051 (ponderación de socios), DPV-120, DPV-126 |
| **T12-02** | **Cercanía al AMBA vs producción primaria** | 12A ↔ 12B | El AMBA minimiza distribución (DEM-01) pero la producción primaria está concentrada en ER/BA interior; el alcance de aves vivas es de escenario (≈ 270 km por ruta) | DEC-057, DEC-053, DPV-116, DPV-048 |
| **T12-03** | **Terreno barato vs servicios** | 12A ↔ 12C | Tierra rural barata puede carecer de potencia, gas, agua, vuelco y accesos; los gates condicionales (G-C4, G-C5, G-C6) lo resuelven con inversión no cuantificada | DEC-052, DPV-087, DPV-119, CAPEX (no iniciado) |
| **T12-04** | **Una planta vs planta + CD** | 12A ↔ 12B | Directo vs CD: 1.349 vs 57 km/t a 300 km; 168–291 vs 19–29 km/t a 100–150 km; sin frontera universal; R2 agrega inventario, frío y doble manipulación | DEC-053, DEC-016, DPV-036 |
| **T12-05** | Escenarios de ancla con **dos parametrizaciones** | 12A ↔ 12B | S1 = 1,0–4,5 t/día vs B = 45 locales × 25–300 kg = 1,1–13,5 t/día | Datos de la red (DPV-003, DPV-037); SUP-085 conserva ambas |
| **T12-06** | **Capacidades de camión**: escenario 12B vs proxy 12C | 12B ↔ 12C | Aves vivas 4.000 / 5.500 / 7.000 (12B) vs 3.000–6.000 (12C); despacho 3–20 t (12B) vs 5–12 t (12C) | DPV-084, DPV-132; cargar como input en ambos modelos |
| **T12-07** | **Espera en recepción** | 12B ↔ 12C | Espera en planta 0,75 h (0,5–2,0) en 12B vs 1 / 1,5 / 2 h para dimensionar bahías en 12C | DPV-127 |
| **T12-08** | **Vehículo limitado por peso vs por volumen** | 12B ↔ 12C | Subproductos ocupan 1–48 % de la capacidad **másica**; para plumas la restricción podría ser volumétrica (densidad pendiente); la playa de contenedores depende de m³ | DPV-135, SUP-106 |
| **T12-09** | **Superficie conceptual 12C vs restricciones reales municipales** | 12C ↔ 12A | Retiros, buffers y franjas **supuestos** ≈ 50–68 % del terreno medio; el FOS y los retiros reales pueden mover el terreno más que el proceso | DPV-141, DPV-106, DPV-124 |
| **T12-10** | **Tecnología de efluentes vs terreno** | 12C ↔ 11 ↔ 12A | Lagunas ~35–40 × compacto en el escenario proxy (con lagunas, hasta ~45 ha alto a 20.000 aves/día) | DEC-043, DPV-144, DEC-063 |
| **T12-11** | **Escala inicial vs reserva para expansión** | 12C ↔ 23 | Reservar para 20.000 aves/día da ~3,3 ha medio en todas las trayectorias; sin escala objetivo el terreno es 2–4,4 ha medio; comprar de más inmoviliza capital, de menos puede impedir crecer | DEC-063, DEC-033, DEC-035, DPV-083 |
| **T12-12** | Acumulación de subproductos | 12B ↔ 12C | 12C reserva cámara para 0,5–3 días; 12B considera la acumulación PENDIENTE en cinco dimensiones | DPV-128, DEC-059 |
| **T12-13** | Tres "radios" distintos | 12A ↔ 12B ↔ 03 | 50 km sanitario de levantamiento (SUP-086), radios de sensibilidad 25–300 km (SUP-091) y alcance de escenario ≈ 270 km por ruta (SUP-095); ninguno es reglamentario | DEC-057; vigilancia de nomenclatura |
| **T12-14** | Río Negro 2,5 % (2025, extracto) vs 2,41 % (2024, tabla oficial) | 01 ↔ 12A | Distinto año del mismo universo; aclarado, no conciliado | Lectura primaria de FTE-001 y FTE-283 (DPV-009) |

## 8. Dependencias entre módulos

| ID | De → a | Qué debe fluir | Estado |
|---|---|---|---|
| **D12-01** | **12B → 12C → 12A** | **camiones / frecuencia / capacidad → docks → playas → circulación → terreno**: aves por camión y t por camión (SUP-096, DPV-084), frecuencia de despacho (SUP-099), tiempos de espera y lavado (SUP-095, DPV-127) definen bahías de recepción, docks de expedición (SUP-113), playas de camiones y de contenedores de subproductos (SUP-117, DPV-135), circulación pesada (25 / 35 / 50 %, SUP-117) y, con retiros y buffers, el terreno (DPV-124) | Hoy 12C usa proxies propios (T12-06, T12-07). Al validar capacidades, cargarlas como **inputs** de `modelo_superficies.py` (`--aves-camion`, `t_por_camion_despacho`), no recalcularlas |
| D12-02 | 12A ↔ 12B | Distancias por ruta medidas, velocidades y factor de ruta reales (DPV-116) → radio, ciclo, flota, t·km; alcance de escenario de 12B → criterio de corredor | Pendiente de ruteo |
| D12-03 | 12C → 12A | Superficie requerida por escala y tecnología (rango conceptual) → comparación con la superficie disponible de la ficha de terreno | Rango existente; restricciones reales pendientes (DPV-141) |
| D12-04 | 11 → 12C → 12A | Tecnología de efluentes y permiso de vuelco → superficie de tratamiento → terreno → gates de localización | DEC-043, DPV-144, DPV-106 |
| D12-05 | 18 → 12C | Dotación por turno y zona → vestuarios, comedor, estacionamiento (hoy proxy SUP-116) | Módulo 18 no iniciado |
| D12-06 | 12A/12B/12C → 19/20 | Superficies, terreno, flota, distancias y frecuencias → CAPEX de obra y terreno; OPEX logístico (logística económica) | No iniciados |
| D12-07 | 12A/12B/12C → HTML | `salida_interfaz()` de 12C, cobertura/envolvente de 12A, flujos de 12B | Simulador no modificado |

## 9. Estado actualizado

| Módulo | Estado | Advertencia |
|---|---|---|
| Localización (`10`) | **MODELO PRELIMINAR COMPLETADO** v1.1 (28 tests) | **LOCALIZACIÓN DEFINITIVA = PENDIENTE. No existe ranking válido de regiones** (0 de 624 celdas verificadas; 0 elegibles con 60 / 75 / 90 %) |
| Logística (`13`) | **MODELO PRELIMINAR COMPLETADO** v1.1 (28 tests) | **LOGÍSTICA ECONÓMICA = PENDIENTE** (sin costos, flota, transportistas ni modelo de distribución elegido) |
| Layout y obra civil (`09`) | **MODELO PRELIMINAR COMPLETADO** v1.0.1 (22 tests, 7/7 mutaciones) | **LAYOUT CONSTRUCTIVO = NO EXISTE** (sin planos ni anteproyecto; 23 de 54 áreas PROXY). Superficie real de terreno pendiente |

Detalle en [`estado_proyecto.md`](estado_proyecto.md) (tablero, hitos, resultados, restricciones y próximos pasos).

**Próximos módulos técnicamente habilitados** (no se inician hasta que el promotor lo indique): recursos humanos (`18`), incubación y alimento balanceado (`15`, `14`), CAPEX y OPEX (`19`, `20`, incluida la logística económica). Requieren, además, trabajo de campo de las olas O0–O8.

## 10. Resultado de los tests

Ejecutados el 2026-10-01 después de la integración, con `PYTHONDONTWRITEBYTECODE=1`. Ningún modelo se modificó en su lógica: en `modelo_localizacion.py`, `modelo_logistica.py` y `modelo_superficies.py` solo cambiaron IDs en comentarios, textos de salida y tablas de parámetros. Al regenerar, `resultados_localizacion.csv` no cambió y `escenarios_logistica.csv` y `escenarios_superficies.csv` resultaron **idénticos byte a byte** al reemplazo textual de IDs sobre la versión de `HEAD` (fin de línea CRLF preservado).

| Suite | Comando | Resultado |
|---|---|---|
| Localización | `10_localizacion/modelo_localizacion.py --solo-tests` (y corrida completa) | **28/28** |
| Logística | `13_logistica/modelo_logistica.py` (pruebas + CSV) | **28/28**; pruebas con la tabla OK (18.268 filas; 2.730 PENDIENTE) |
| Layout | `09_layout_obra_civil/modelo_superficies.py` / `--mutaciones` | **22/22**; mutaciones **7/7** detectadas |
| Escala (importado) | `23_plan_expansion/modelo_escala.py --solo-tests` / `--mutaciones` | **23/23**; **22/22** |
| Proceso (importado) | `05_proceso_industrial/modelo_capacidad_proceso.py --solo-tests` / `--mutaciones` | **18/18**; **9/9** |
| Utilities (importado) | `11_agua_efluentes/modelo_utilities.py --solo-tests` / `--mutaciones` | **30/30**; **20/20** |

Los modelos de localización y logística no tienen modo de mutaciones propio.

## 11. Control de integridad

| Control | Resultado | Detalle |
|---|---|---|
| IDs SUP únicos | OK | 123 (SUP-001–SUP-123); duplicados []; huecos [] |
| IDs DPV únicos | OK | 145 (DPV-001–DPV-145); duplicados []; huecos [] |
| IDs DEC únicos | OK | 66 (DEC-001–DEC-066); duplicados []; huecos [] |
| IDs FTE únicos | OK | 297 (FTE-001–FTE-297); duplicados []; huecos [] |
| Fuentes únicas (URL) | OK | 1 URL repetida, preexistente (FTE-001/FTE-071, T-13) |
| Referencias SUP/DPV/DEC/FTE | OK | todas definidas |
| Columnas de las tablas de registros | OK | todas las filas con el número de columnas del encabezado |
| Sin IDs provisionales activos | OK | solo en `actualizaciones_gestion_*.md` y `fuentes_09*/12*` históricos y en los documentos de reconciliación |
| Enlaces relativos | OK | todos resuelven |
| Sin marcadores de merge | OK | ninguno |
| CSV válidos | OK | 23 CSV, columnas constantes |
| Glosario sin duplicados | OK | 259 términos |

## 12. Archivos modificados

- `00_gestion_proyecto/datos_por_validar.md` — modificado
- `00_gestion_proyecto/decisiones_pendientes.md` — modificado
- `00_gestion_proyecto/estado_proyecto.md` — modificado
- `00_gestion_proyecto/glosario.md` — modificado
- `00_gestion_proyecto/matriz_validacion_campo.csv` — modificado
- `00_gestion_proyecto/plan_trabajo_campo.md` — modificado
- `00_gestion_proyecto/reconciliacion_sesiones_12.md` — creado
- `00_gestion_proyecto/supuestos.md` — modificado
- `01_mercado/datos_mercado.csv` — modificado
- `01_mercado/mercado_avicola_argentina.md` — modificado
- `09_layout_obra_civil/README.md` — modificado
- `09_layout_obra_civil/actualizaciones_gestion_12C.md` — modificado
- `09_layout_obra_civil/conclusiones_layout.md` — modificado
- `09_layout_obra_civil/escenarios_superficies.csv` — modificado
- `09_layout_obra_civil/estrategia_expansion.md` — modificado
- `09_layout_obra_civil/flujos_layout.md` — modificado
- `09_layout_obra_civil/layouts_por_escala.md` — modificado
- `09_layout_obra_civil/modelo_superficies.py` — modificado
- `09_layout_obra_civil/programa_areas.md` — modificado
- `09_layout_obra_civil/requerimientos_obra_civil.md` — modificado
- `09_layout_obra_civil/zonificacion_layout.md` — modificado
- `10_localizacion/README.md` — modificado
- `10_localizacion/actualizaciones_gestion_12A.md` — modificado
- `10_localizacion/conclusiones_localizacion.md` — modificado
- `10_localizacion/criterios_localizacion.md` — modificado
- `10_localizacion/escenarios_localizacion.md` — modificado
- `10_localizacion/guia_ramiro.md` — modificado
- `10_localizacion/matriz_localizacion.csv` — modificado
- `10_localizacion/metodologia_localizacion.md` — modificado
- `10_localizacion/modelo_localizacion.py` — modificado
- `10_localizacion/pesos_localizacion.csv` — modificado
- `10_localizacion/regiones_preliminares.md` — modificado
- `10_localizacion/terreno_ideal.md` — modificado
- `13_logistica/README.md` — modificado
- `13_logistica/actualizaciones_gestion_12B.md` — modificado
- `13_logistica/conclusiones_logistica.md` — modificado
- `13_logistica/escenarios_logistica.csv` — modificado
- `13_logistica/flota_propia_vs_tercerizada.md` — modificado
- `13_logistica/kpis_logistica.md` — modificado
- `13_logistica/logistica_aves_vivas.md` — modificado
- `13_logistica/logistica_exportacion.md` — modificado
- `13_logistica/logistica_producto_terminado.md` — modificado
- `13_logistica/logistica_subproductos.md` — modificado
- `13_logistica/mapa_flujos_logisticos.md` — modificado
- `13_logistica/modelo_logistica.py` — modificado
- `25_fuentes/bibliografia.md` — modificado
- `25_fuentes/registro_fuentes.csv` — modificado

Total: 47 archivos (1 creado, 46 modificados, 0 retirados). Los CSV de salida `escenarios_logistica.csv` y `escenarios_superficies.csv` cambian solo por los IDs (regenerados). Los tres `fuentes_12*.csv` quedan sin cambios, como históricos.
