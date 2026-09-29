# Galpones, energía y clima

**Fecha:** 2026-09-29 · **Versión:** 1 · Fase 0

> **Alcance.** Tipos de galpón de engorde, sus sistemas y su lógica técnico-económica; necesidades de energía y control ambiental; implicancias regionales. **No se cotiza ninguna inversión** ni se selecciona tecnología, proveedor o cantidad de galpones (fase no habilitada; DEC-022). Los CAPEX se expresan **solo en términos relativos y cualitativos** hasta contar con cotizaciones (DPV-051). Fuentes: extractos `[PVDP]`.

---

## 1. Tipos de galpón

Los nombres no son estándar; en Argentina se habla de galpón **convencional** (abierto con cortinas), **tecnificado**, **climatizado**, **blackout** o **túnel**. Se usan estas categorías:

| Tipo | Descripción | Ventilación | Luz |
|---|---|---|---|
| **Convencional (abierto)** | Galpón con laterales de cortina (manual o semiautomática), a veces ventiladores de recirculación | Natural (apertura de cortinas) + ventiladores de apoyo | Natural + artificial |
| **Climatizado / tecnificado** | Cerramientos más estancos, cortinas automáticas, extractores, control electrónico de temperatura | Presión negativa (extractores) con modos mínimo/transición | Natural reducida + artificial |
| **Túnel de ventilación** | Galpón cerrado; extractores concentrados en un extremo y entrada de aire (con **paneles evaporativos**) en el otro; el aire recorre el galpón a alta velocidad | Mínima → transición → **túnel** (enfriamiento por velocidad del aire + evaporación) | Artificial predominante |
| **Dark house** (usado en Brasil) | Túnel con cerramiento que **bloquea la luz natural** (cortinas/paredes oscuras) y control total del programa de luz | Túnel con paneles evaporativos | **Solo artificial** (programa de luz controlado) |
| **Automatizado** (transversal a los anteriores) | Controlador ambiental integrado, sensores (temperatura, humedad, CO₂, NH₃, presión estática), balanzas automáticas de aves, medición de agua y alimento por galpón, alarmas remotas | — | — |

En Argentina un estudio con 15 productores de Entre Ríos que operaban **ambos sistemas** comparó convencionales (cortinas manuales y ventiladores) con tecnificados (**blackout**, cerrados con chapa y extractores) en 62 crianzas: los tecnificados fueron mejores en **mortalidad (7,68 % vs 9,51 %), conversión, kg de carne/m² y relación peso/conversión** (FTE-151 `[PVDP]`).

---

## 2. Comparación por dimensión

Escala cualitativa: **+** bajo · **++** medio · **+++** alto. Sin cotizaciones: **no usar como costos**.

| Dimensión | Convencional | Climatizado / tecnificado | Túnel | Dark house | Automatización (adicional) |
|---|---|---|---|---|---|
| **Capacidad típica por galpón** | ~10.000–18.000 pollitos | ~15.000–25.000 | ~20.000–40.000 | ~25.000–40.000+ | — |
| **Dimensiones típicas** | ~12 m × 100–125 m (≈1.200–1.500 m²) | ~12–15 m × 100–150 m | ~14–20 m × 120–150 m (≈1.700–3.000 m²) | Similar a túnel | — |
| **Densidad técnicamente razonable** | ~25–33 kg/m² (menos en verano) | ~33–37 kg/m² | ~35–42 kg/m² | ~35–42 kg/m² | Permite sostener el máximo con menor riesgo |
| **Ventilación** | Natural; depende del viento y del operario | Mecánica parcial | Mecánica total; alta velocidad de aire | Mecánica total | Control automático por sensores |
| **Calefacción** | Criadoras a gas (campanas), calefactores; pérdidas altas | Criadoras + calefactores; mejor aislación | Calefactores de aire; buena aislación | Idem túnel | Control por temperatura/edad |
| **Cooling** | Ventiladores de recirculación, eventualmente nebulización | Nebulización | **Paneles evaporativos** + túnel | Paneles evaporativos + túnel | Control por temperatura y humedad |
| **Comederos** | Tolvas o líneas automáticas de platos | Líneas automáticas | Líneas automáticas | Líneas automáticas | Balanzas de silo, consumo por galpón |
| **Bebederos** | Campana o niple | Niple | Niple con regulación de presión | Niple | Medidor de agua por galpón |
| **Iluminación** | Natural + lámparas | Natural reducida + LED | LED con programa | LED con programa y **oscuridad total** | Programa automático, dimmer |
| **Mano de obra** | +++ (manejo manual de cortinas, más recorridas) | ++ | + a ++ | + a ++ | Reduce tareas manuales; exige personal más calificado |
| **Control ambiental** | + | ++ | +++ | +++ | +++ |
| **CAPEX relativo por m²** | + | ++ | +++ | +++ | + adicional |
| **Consumo eléctrico** | + | ++ | +++ (extractores, bombas) | +++ | + |
| **Productividad** (kg/m²/año, FCR, mortalidad) | + | ++ | +++ | +++ | Mejora la consistencia |
| **Riesgos principales** | Golpe de calor, frío, dependencia del operario y del clima | Fallas de extractores | **Dependencia total de la energía**: un corte en verano puede matar el lote en minutos | Idem túnel | Fallas de sensores/controlador; ciberseguridad y conectividad rural |

Capacidades y dimensiones: `[ESTIMACIÓN]` a partir de la densidad (§4 de [`ciclo_productivo.md`](ciclo_productivo.md)) y de referencias de dimensión `[PVDP]`: galpones de ~12 m de ancho y 100–150 m de largo (FTE-150); promedio de ~1.400 m² por granja en Entre Ríos (FTE-048). Densidades: FTE-143 y FTE-144 `[PVDP]`.

### 2.1 Capacidad por galpón según densidad (perfil medio, 2,9 kg)

| Superficie del galpón | 30 kg/m² | 35 kg/m² | 39 kg/m² |
|---|---|---|---|
| 1.200 m² | ~12.400 aves a faena (~13.000 pollitos alojados con 5 % de mortalidad) | ~14.500 (~15.200) | ~16.100 (~17.000) |
| 1.800 m² | ~18.600 (~19.600) | ~21.700 (~22.900) | ~24.200 (~25.500) |
| 2.400 m² | ~24.800 (~26.100) | ~29.000 (~30.500) | ~32.300 (~34.000) |

`[ESTIMACIÓN]`. La **capacidad de un galpón no es su producción anual**: un galpón de 1.800 m² a 35 kg/m² con 5,7 ciclos/año produce ~124.000 aves/año, no 22.900.

### 2.2 Lógica económica (sin cifras)

- Un galpón más tecnificado cuesta más por m², pero **produce más kg por m² y por año** (más densidad, mejor FCR, menor mortalidad, menos riesgo de calor). La comparación correcta es **CAPEX + OPEX por kg vivo producido**, no CAPEX por m².
- En climas cálidos la tecnificación deja de ser opcional: sin enfriamiento, la densidad de verano cae y la mortalidad por calor sube.
- Para un **integrador**, la tecnología del galpón la paga el productor; el integrador la incentiva con el pago por desempeño o exigiéndola por contrato ([`modelos_integracion.md`](modelos_integracion.md)).
- **Exportación:** los mercados exigentes auditan bienestar (densidad, calidad de cama, pododermatitis). Galpones con mejor control ambiental facilitan cumplirlos.

---

## 3. Energía y clima

### 3.1 Necesidades

| Necesidad | Qué es | Fuente de energía | Orden de magnitud / referencia |
|---|---|---|---|
| **Calefacción inicial** | Mantener el ambiente de cría (~30–33 °C a nivel del pollito el día 1, bajando con la edad `[PVDP]`) | Gas natural o GLP (criadoras, calefactores de aire); leña/biomasa en algunos casos | Una criadora típica para ~1.000 pollitos consume **~360 g/h de GLP** a potencia máxima (FTE-158 `[PVDP]`, ficha comercial). Muy estacional: casi nula en verano, alta en invierno. En Entre Ríos, el integrador suele aportar el gas (FTE-153 `[PVDP]`) |
| **Ventilación mínima** | Renovar aire para retirar humedad, CO₂ y amoníaco aun con frío | Electricidad (extractores) | Continua durante todo el ciclo |
| **Ventilación de transición y túnel** | Retirar el calor producido por las aves | Electricidad | **Principal consumo eléctrico** de la granja (FTE-158 `[PVDP]`) |
| **Cooling** | Enfriamiento evaporativo (paneles, nebulización) | Electricidad (bombas) + agua | Estacional (verano) |
| **Iluminación** | Programa de luz | Electricidad (LED) | Bajo con LED |
| **Comederos, bebederos, bombas de agua** | Motores de líneas, sinfines, bombas | Electricidad | Bajo–medio |
| **Consumo eléctrico anual (referencia externa)** | — | — | **8,7–23,6 kWh/m²/año** según tamaño de ave (estudio extranjero, FTE-158 `[PVDP · débil]`). Para 36.000 m² (escenario medio de 10.000 aves/día): ~0,3–0,85 GWh/año `[ESTIMACIÓN]`, a validar con datos argentinos (DPV-052) |
| **Potencia instalada (planificación)** | — | — | Sin dato utilizable. Un extracto indica "0,08–0,12 kW por ave" (FTE-158 `[PVDP · débil]`), que implicaría 2.000–3.000 kW para un galpón de 25.000 aves: **inconsistente, descartado** (ver nota). A dimensionar con proveedores y datos argentinos (DPV-052) |
| **Generador de emergencia** | Respaldo del 100 % de la carga crítica (ventilación, agua, alarmas, controlador) con **transferencia automática** | Gasoil / gas | Obligatorio de hecho en galpones cerrados; la prensa registra mortandades por caídas de tensión (FTE-157) |
| **Alarmas** | Temperatura alta/baja, corte de energía, falla de agua, puerta abierta; aviso remoto (SMS/app) | Batería / red | Requiere conectividad rural confiable |

> **Nota de control de calidad:** el extracto "0,08–0,12 kW por ave" implicaría 2.000–3.000 kW para 25.000 aves, incompatible con 8,7–23,6 kWh/m²/año (para 1.800 m²: ~16.000–42.000 kWh/año, es decir **~2–5 kW de potencia media**; la potencia instalada es mayor por los picos de ventilación de verano, pero no en ese orden). Se descarta hasta verificar la fuente (DPV-052).

### 3.2 Por qué una falla eléctrica puede matar un lote en minutos

**Estimación de orden de magnitud** (galpón cerrado, perfil medio, final de crianza, verano) `[ESTIMACIÓN]`:

1. Un pollo de ~2,9 kg come ~0,2 kg/día de alimento con ~3.100 kcal/kg → ~620 kcal/día ≈ **30 W** de energía ingerida; la mayor parte termina como **calor**: del orden de **~15–20 W por ave**.
2. A 12 aves/m² → **~180–240 W/m²**. Un galpón de 1.800 m² genera **~330–430 kW** de calor, como decenas de estufas encendidas.
3. El aire del galpón (1.800 m² × ~3 m de altura media ≈ 5.400 m³) tiene una capacidad calorífica de ~6,5 MJ/°C. Sin ventilación, aunque solo la mitad del calor fuera sensible, **la temperatura subiría del orden de 1–2 °C por minuto**.
4. Con temperatura y humedad altas el ave no puede disipar calor (jadeo), y en **10–30 minutos** pueden producirse muertes masivas.

En galpones abiertos el riesgo es menor pero existe (días sin viento). En **galpones túnel y dark house**, sin ventanas que abrir, la dependencia es total. Mitigaciones: generador con arranque y transferencia automáticos probado semanalmente, alarmas remotas, cortinas o paneles de apertura de emergencia (*drop curtains*), presencia de personal de guardia, contrato de suministro y calidad de red (caídas de tensión, no solo cortes). La prensa registra casos en Entre Ríos (2026-03, caída de tensión con calor extremo, granja de un integrador) y Santa Fe (FTE-157 `[PVDP]`).

### 3.3 Implicancias regionales (cualitativas)

| Región | Clima (desafío principal) | Energía | Granos | Distancia al AMBA | Otros |
|---|---|---|---|---|---|
| **Buenos Aires (norte y centro)** | Invierno frío (calefacción) y olas de calor | Red eléctrica más densa; gas natural en algunas zonas | Zona núcleo maicera y sojera | **Baja** | ~35 % de la faena nacional (FTE-001 `[PVDP]`); presión urbana y ambiental cerca del AMBA |
| **Entre Ríos** | Veranos húmedos y calurosos; inviernos moderados | Calidad de red rural a relevar (casos de caídas de tensión, FTE-157) | Maíz y soja en la provincia | Media (~200–400 km) | **Principal cluster avícola** (~50 % de la faena, FTE-001; mayoría de granjas, FTE-048): servicios, integrados y contratistas disponibles, pero **mayor densidad de granjas = mayor presión sanitaria** y competencia por productores |
| **Santa Fe / Córdoba** | Continental; olas de calor | Buena en zonas productivas | **Excedentes de maíz y soja** (menor costo de flete de granos) | Media–alta | Cluster avícola menor (SF ~5 %, Cba ~4 % de la faena, FTE-001) |
| **Chaco (NEA)** | **Calor y humedad intensos**: exige túnel/cooling y reduce la densidad de verano; poca calefacción | Red rural a verificar; costo eléctrico del cooling | Soja y maíz regionales (a verificar) | **Alta (~1.000 km)**: el producto terminado viaja lejos del principal mercado | Baja densidad avícola (ventaja sanitaria); contacto personal = ventaja cualitativa, no criterio (SUP-014) |

La localización se decidirá con criterios técnicos (DEC-003). Desde la producción primaria, las variables clave son: **clima (tecnología de galpón necesaria), calidad y costo de la energía, disponibilidad de agua, cercanía a granos y a la fábrica de alimento, distancia granja–planta, densidad avícola de la zona y disponibilidad de productores y mano de obra**.
