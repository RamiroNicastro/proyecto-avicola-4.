# Balance de agua industrial de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Fase 0 (prefactibilidad)

> **Alcance:** agua **industrial** de la planta de faena y proceso (no la de bebida de las granjas, que está en [`../03_produccion_primaria`](../03_produccion_primaria/README.md)). Rangos bajo/medio/alto en L/ave y m³/día para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo. **No** se diseña captación, tratamiento de agua ni tanques; **no** se elige ubicación; **no** se calcula CAPEX.
> **Modelo:** [`modelo_utilities.py`](modelo_utilities.py) → [`escenarios_utilities.csv`](escenarios_utilities.csv) (bloques `agua` y `agua_retenida`). **Fuentes:** acceso directo bloqueado (`EGRESS_BLOCKED`, séptima sesión consecutiva; DPV-009): **toda cifra externa es `[PVDP]`** (IDs `FTE-09C-xx` en [`fuentes_09C.csv`](fuentes_09C.csv)). Ninguna cifra es una medición argentina.

---

## 1. Tres aguas que no se mezclan

| Concepto | Qué es | Cómo se calcula | Orden de magnitud (10.000 aves/día, medio) |
|---|---|---|---|
| **Agua utilizada** (consumo industrial) | Toda el agua que entra a la planta: escaldado, lavados, chiller, limpieza, sanitización, servicios | Σ L/ave por etapa × aves / 1.000 | **250 m³/día** (25 L/ave) |
| **Agua descargada** (efluente) | Lo que sale por el desagüe de proceso hacia el tratamiento | Agua utilizada × fracción a efluente (80–95 %) | **220 m³/día** (22 L/ave) |
| **Agua retenida en producto/subproductos** | Agua absorbida por la carcasa en el chiller que queda en el producto vendido (y la adherida a las plumas) | Balance de masa v1.1 (SUP-042, SUP-040) | **0,86 t/día** en producto; 2,13 t/día incorporada a producto y subproductos |

- El agua retenida en producto es **~0,34 %** del agua utilizada. Por eso **nunca** sirve para estimar consumo: es otro universo (regla 18). El modelo lo garantiza con el test **U03** (triplicar el agua retenida no cambia ni el agua utilizada ni la descargada) y la mutación **M01**.
- **Cierre** (test U04): agua utilizada = agua descargada + agua no descargada. La no descargada incluye evaporación (escaldador, caldera, condensadores evaporativos), agua retenida en producto, agua que sale con plumas y lodos, y pérdidas. El agua retenida siempre es menor que la no descargada.
- Ejemplo del chiller: por cada ave la reposición de agua del chiller es **~2,8 L** (1,9–4,5 L), mientras que la carcasa **absorbe ~0,12 L** y retiene ~0,09 L. El chiller es un consumidor de agua **30 veces** mayor que lo que el producto se lleva.

## 2. Consumo por etapa (L/ave faenada)

| Etapa | Bajo | **Medio** | Alto | Origen | Referencia |
|---|---|---|---|---|---|
| Recepción (lavado de jaulas/módulos, camiones, andén) | 0,5 | **1,0** | 2,0 | `[SUPUESTO]` | Sin dato por ave |
| Escaldado (llenado, reposición, desborde) | 0,9 | **1,2** | 2,0 | FUENTE `[PVDP]` | ~1 cuarto de galón (0,95 L)/ave (FTE-09C-11, FTE-09C-18) |
| Desplumado (duchas, transporte de plumas) | 1,0 | **2,0** | 3,5 | `[SUPUESTO]` | Dentro de los totales de FTE-09C-01/02 |
| Evisceración (lavados interior/exterior, transporte hidráulico de vísceras) | 4,0 | **6,0** | 8,0 | FUENTE `[PVDP]` | 7,57 L/ave (FTE-09C-01) |
| Lavado final de carcasas | 1,5 | **3,0** | 4,5 | FUENTE `[PVDP]` | 4,25–4,35 L/ave (FTE-09C-01) |
| Chiller (reposición en contracorriente) | 1,9 | **2,8** | 4,5 | FUENTE `[PVDP]` | Mín. 0,5 gal = 1,9 L; típico 2,8–5,7 L (FTE-09C-18); 2,12 L (FTE-09C-01) |
| Despiece y deshuese | 0,5 | **1,0** | 2,0 | FUENTE `[PVDP]` | 3,03 L/ave (FTE-09C-01) |
| Limpieza de equipos y salas | 3,0 | **5,0** | 7,5 | FUENTE `[PVDP]` | 5,7–11,4 L saneamiento + 0,9–3,8 L equipos (FTE-09C-01) |
| Sanitización (esterilizadores, lavamanos, pediluvios, enjuagues) | 0,7 | **1,0** | 1,5 | `[SUPUESTO]` | Sin dato separado |
| Servicios auxiliares (caldera, condensadores, vestuarios, comedor) | 1,0 | **2,0** | 2,5 | `[SUPUESTO]` | Sin dato separado |
| **Total** | **15,0** | **25,0** | **38,0** | `[ESTIMACIÓN]` | Calibrado a los totales de fuentes (§3) |

**Cómo leer la tabla:** los **totales** están calibrados contra rangos publicados; el **reparto** por etapa es un supuesto guiado por un único desglose de EE.UU. y **no debe usarse para diseñar** ninguna etapa. "Bajo" = planta eficiente (reutilización, boquillas, limpieza en seco previa); "alto" = planta con prácticas de uso intensivo.

## 3. Contraste con fuentes (todas `[PVDP]`)

| Fuente | Dato | Equivalente | Dentro del rango del modelo |
|---|---|---|---|
| Georgia, 2009 (FTE-09C-02) | 7 gal (26 L) por carcasa | 26 L/ave | Sí (medio 25) |
| Carolina del Norte (FTE-09C-02) | 13,2–37,8 L/ave | — | Sí (15–38) |
| Planta que optimizó (FTE-09C-02) | 5,67 → 3,94 gal/ave | 21,5 → 14,9 L/ave | Sí (bajo ≈ 15) |
| EE.UU., ave de 2,3 kg (FTE-09C-01) | 26,5 L/ave | ~33 L/ave escalado a 2,9 kg (proporcional, **no verificado**) | Sí (medio–alto) |
| Brasil (FTE-09C-03) | 30 L/ave (dimensionamiento); 22 L/ave (caso) | — | Sí |
| Revisión mataderos (FTE-09C-04) | 3,8–17,9 kL/t de carcasa | ~8–38 L/ave con ~2,1 kg de carcasa | Rango más amplio abajo |

**Contradicciones y cautelas:** (1) un extracto da "escaldado 5–15 gal/ave", incompatible con el mínimo de ~1 cuarto de galón: se interpreta como el total de la planta y no se usa por etapa; (2) otro extracto da lavados de carcasa de 2–6 gal/ave (7,6–22,7 L), muy superior a 4,25 L: se registra como inconsistencia; (3) todas las cifras son de EE.UU. o Brasil, con normas de chiller distintas (el mínimo de 0,5 gal/ave es norma de EE.UU., no argentina); (4) ninguna distingue claramente si incluye el despiece ni el lavado de camiones. **Dato argentino faltante: DPV-067** (y propuesta de DPV nueva en [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md)).

## 4. Agua por escala

`[ESTIMACIÓN]` = L/ave × aves / 1.000. Día **operativo** (día de faena). Año con 250 días de faena.

| Escala (aves/día op.) | Agua utilizada m³/día (bajo · **medio** · alto) | Agua descargada m³/día | m³/año (medio, 250 d) | Caudal medio / pico m³/h (medio)¹ | Agua retenida en producto t/día |
|---|---|---|---|---|---|
| 2.500 | 38 · **62** · 95 | 30 · **55** · 90 | 15.600 | 5,2 / 9,4 | 0,21 |
| 5.000 | 75 · **125** · 190 | 60 · **110** · 180 | 31.300 | 10,4 / 18,8 | 0,43 |
| 10.000 | 150 · **250** · 380 | 120 · **220** · 361 | 62.500 | 20,8 / 37,5 | 0,86 |
| 20.000 | 300 · **500** · 760 | 240 · **440** · 722 | 125.000 | 41,7 / 75,0 | 1,71 |

¹ Caudal medio sobre 12 h (8 h netas de faena + 4 h de limpieza, `[SUPUESTO]`); pico = medio × 1,8 (`[SUPUESTO]`; 1,5–2,2). Con 300 días/año el consumo **diario** no cambia; el **anual** sube 20 %.

**Lecturas:**
1. **Una planta de 10.000 aves/día usa del orden de 150–380 m³/día**, como una localidad de unos pocos miles de habitantes (comparación didáctica, no dato). A 20.000 aves/día son 300–760 m³/día.
2. La **incertidumbre** (bajo vs alto, ×2,5) es mayor que el efecto de pasar de 5.000 a 10.000 aves/día (×2). La gestión del agua pesa tanto como la escala.
3. El caudal **horario** (no el diario) dimensiona la captación, el bombeo y la reserva: 10.000 aves/día pueden requerir ~38 m³/h en pico (≈ 10 L/s).
4. **El agua puede limitar la capacidad:** si la perforación o la red de un sitio entregan, por ejemplo, 20 m³/h durante 12 h (240 m³/día), una planta de 10.000 aves/día en nivel alto (380 m³/día) no puede operar sin reserva, reúso o una segunda fuente. El dato del sitio es crítico (DPV-053, DPV-087).

## 5. Calidad del agua — necesidades conceptuales

**No se diseña ninguna planta de tratamiento.** Se listan las preguntas que el sitio debe responder.

| Tema | Por qué importa en una planta de faena | Qué se necesita saber | Estado |
|---|---|---|---|
| **Potabilidad** | El agua en contacto con el producto y las superficies debe ser potable (Decreto 4238/68 para habilitación SENASA; CAA art. 982 define agua potable) | Análisis físico-químico y microbiológico completo según CAA art. 982 | Norma leída solo en extractos `[PVDP]` (FTE-016, FTE-09C-16) |
| **Perforación vs red** | Determina caudal disponible, costo, riesgo de corte y permisos | Caudal sostenido (ensayo de bombeo), profundidad, acuífero, permiso de explotación (autoridad del agua provincial); red: caudal y presión garantizados por el prestador | DPV-053 |
| **Arsénico, flúor, nitratos** | En parte de la llanura chaco-pampeana el agua subterránea puede superar límites de potabilidad (CAA: As ≤ 0,01 mg/L `[PVDP]`) | Análisis en el sitio; si excede, la potabilización (p. ej. ósmosis) cambia la ecuación de agua y genera rechazo salino | Sin dato por sitio (DPV-053) |
| **Dureza** | Incrustaciones en caldera, intercambiadores, escaldador, boquillas; más consumo de químicos de limpieza | Dureza total y alcalinidad | Sin dato |
| **Hierro y manganeso** | Manchas, depósitos, sabor; obstrucción de boquillas y filtros | Fe, Mn | Sin dato |
| **Tratamiento** | Según el análisis: filtración, ablandamiento (caldera), remoción de As/Fe, desinfección | Qué parámetros exceden y en cuánto | No se diseña |
| **Cloración** | Desinfección y **cloro residual** en red interna; algunas plantas usan agua clorada o antimicrobianos en chiller y lavados | Demanda de cloro del agua; norma de cloro residual y de antimicrobianos permitidos en carne aviar (a relevar en `16_normativa_senasa`) | Pendiente |
| **Almacenamiento** | Autonomía frente a cortes de suministro y para absorber el pico horario (el pozo entrega caudal constante; la planta consume en picos) | Autonomía deseada (horas o días de uso), exigencia de reserva contra incendio | Referencia conceptual: **1 día de uso = 62 / 125 / 250 / 500 m³** (medio); no es diseño |
| **Presión** | Lavados de carcasa, limpieza y esterilizadores requieren presión estable; limpieza a alta presión localizada | Presión de red o necesidad de presurización | Sin dato |
| **Temperatura del agua** | Agua de red más fría reduce frío del chiller pero aumenta calor del escaldador y la limpieza | Temperatura estacional del pozo/red | Modelo usa 18 °C `[SUPUESTO]` |
| **Agua para exportación** | Destinos exigentes auditan la potabilidad y el control del agua (plan de muestreo, registros) | Requisitos por destino ([`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md)) | Pendiente |

## 6. Reúso de agua (conceptual)

Las fuentes de EE.UU. (FTE-09C-01) describen reúso del agua del chiller para escaldado o transporte de vísceras bajo reglas sanitarias específicas. En Argentina **no se relevó** qué admite el Decreto 4238/68 (DPV-061). Se registra como **opción a estudiar**, no como supuesto: reduciría el nivel "alto" hacia el "bajo" y es un argumento de escalabilidad (la misma perforación alcanza para más aves).

## 7. Qué medir

Consolidado en [`conclusiones_agua_efluentes.md` §6](conclusiones_agua_efluentes.md).
