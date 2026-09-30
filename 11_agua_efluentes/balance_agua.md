# Balance de agua industrial de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0 (prefactibilidad)

> **Alcance:** agua **industrial** de la planta de faena y proceso (no la de bebida de las granjas, que está en [`../03_produccion_primaria`](../03_produccion_primaria/README.md)). **Los escenarios de 15 / 25 / 38 L por ave son un RANGO DE SENSIBILIDAD PRELIMINAR, no el consumo esperado de nuestra futura planta ni una especificación de diseño.** No se diseña captación, tratamiento de agua ni tanques; no se elige ubicación; no se calcula CAPEX.
> **Modelo:** [`modelo_utilities.py`](modelo_utilities.py) v1.1 → [`escenarios_utilities.csv`](escenarios_utilities.csv) (bloques `agua` y `agua_incorporada`). **Fuentes:** acceso directo bloqueado (`EGRESS_BLOCKED`; DPV-009): **toda cifra externa es `[PVDP]`** (IDs `FTE-09C-xx` en [`fuentes_09C.csv`](fuentes_09C.csv)). Ninguna cifra es una medición argentina.

---

## 1. Cinco conceptos de agua que no se mezclan

| Concepto | Qué es | Cómo se calcula | 10.000 aves/día, escenario medio |
|---|---|---|---|
| **Agua captada/comprada** | Lo que se extrae del pozo o se compra a la red | Agua utilizada ÷ (1 − fracción de rechazo de potabilización) | 250 m³/día con rechazo 0 (`[SUPUESTO]` editable: si el agua exige ósmosis por arsénico, la captada supera a la utilizada) |
| **Agua utilizada en proceso** | Toda el agua que entra a las operaciones: escaldado, lavados, chiller, limpieza, sanitización, servicios | Σ L/ave por etapa × aves / 1.000 | **250 m³/día** (25 L/ave, rango de sensibilidad) |
| **Agua incorporada al producto y subproductos** | Agua absorbida por la carcasa en el chiller (retenida en producto + goteo) y agua adherida a las plumas | Balance de masa v1.1 (SUP-040, SUP-042) | 2,13 t/día (de las cuales **0,86 t/día** quedan retenidas en el producto vendido) |
| **Agua evaporada o arrastrada** | Evaporación (escaldador, caldera, condensadores), arrastre con lodos y sólidos, pérdidas | Por diferencia: utilizada − descargada − incorporada | ~28 m³/día (resultado, no dato) |
| **Agua descargada como efluente** | Lo que sale por el desagüe de proceso hacia el tratamiento | Utilizada × **fracción a efluente** | **220 m³/día** con 0,88 |

Reglas del modelo:

1. **El agua incorporada nunca calcula el consumo:** es ~0,34 % del agua utilizada (retenida en producto). Test **U03**: triplicarla no cambia ni el agua utilizada ni la descargada (mutación M01).
2. **La relación entre agua utilizada y efluente NO es fija.** Depende de evaporación, arrastre con subproductos y lodos, reúso interno y fugas. La fracción a efluente (80 / 88 / 95 %) es un **`[SUPUESTO]` editable** (`--frac-efluente`), registrado en el CSV como `fraccion_agua_a_efluente_supuesta`.
3. **Cierre** (test **U04**): captada ≥ utilizada = descargada + incorporada + evaporada/arrastrada. Si la fracción supuesta deja una evaporación negativa, el modelo emite la alerta `AGUA_CIERRE` en lugar de forzar el cierre (mutación M09).
4. Ejemplo del chiller: la reposición es **~2,8 L/ave** mientras la carcasa absorbe ~0,12 L y retiene ~0,09 L.

## 2. Consumo por etapa — rango de sensibilidad (L/ave faenada)

| Etapa | Bajo | **Medio** | Alto | Origen | Referencia |
|---|---|---|---|---|---|
| Recepción (lavado de jaulas/módulos, camiones, andén) | 0,5 | **1,0** | 2,0 | `[SUPUESTO]` | Sin dato por ave |
| Escaldado (llenado, reposición, desborde) | 0,9 | **1,2** | 2,0 | FUENTE `[PVDP]` | ~1 cuarto de galón (0,95 L)/ave (FTE-09C-11, FTE-09C-18) |
| Desplumado (duchas, transporte de plumas) | 1,0 | **2,0** | 3,5 | `[SUPUESTO]` | Dentro de los totales de FTE-09C-01/02 |
| Evisceración (lavados, transporte hidráulico de vísceras) | 4,0 | **6,0** | 8,0 | FUENTE `[PVDP]` | 7,57 L/ave (FTE-09C-01) |
| Lavado final de carcasas | 1,5 | **3,0** | 4,5 | FUENTE `[PVDP]` | 4,25–4,35 L/ave (FTE-09C-01) |
| Chiller (reposición en contracorriente) | 1,9 | **2,8** | 4,5 | FUENTE `[PVDP]` | Mín. 0,5 gal = 1,9 L; típico 2,8–5,7 L (FTE-09C-18); 2,12 L (FTE-09C-01) |
| Despiece y deshuese | 0,5 | **1,0** | 2,0 | FUENTE `[PVDP]` | 3,03 L/ave (FTE-09C-01) |
| Limpieza de equipos y salas | 3,0 | **5,0** | 7,5 | FUENTE `[PVDP]` | 5,7–11,4 L saneamiento + 0,9–3,8 L equipos (FTE-09C-01) |
| Sanitización | 0,7 | **1,0** | 1,5 | `[SUPUESTO]` | Sin dato separado |
| Servicios auxiliares | 1,0 | **2,0** | 2,5 | `[SUPUESTO]` | Sin dato separado |
| **Total** | **15,0** | **25,0** | **38,0** | `[ESTIMACIÓN]` | Calibrado a totales de fuentes (§3) |

Los **totales** están calibrados contra rangos publicados; el **reparto** por etapa es un supuesto guiado por un único desglose de EE.UU. y **no debe usarse para diseñar** ninguna etapa. El nivel alto (38 L/ave) queda en el borde superior del rango citado (37,8): el modelo lo marca con la alerta `AGUA_L_AVE`.

## 3. Dos unidades para contrastar: L/ave y m³/t de producto

| Nivel | L/ave | m³/t de producto comestible (peso comercial, 2,40 kg/ave) | m³/t de peso vivo |
|---|---|---|---|
| Bajo | 15 | **6,3** | 5,2 |
| Medio | 25 | **10,4** | 8,6 |
| Alto | 38 | **15,9** | 13,1 |

Contraste con fuentes (`[PVDP]`):

| Fuente | Dato | En L/ave | En m³/t | ¿Compatible? |
|---|---|---|---|---|
| Georgia, 2009 (FTE-09C-02) | 7 gal/carcasa | 26 | ~10,8 (con 2,40 kg/ave) | Sí |
| Carolina del Norte (FTE-09C-02) | 13,2–37,8 L/ave | 13–38 | ~5,5–15,8 | Sí |
| Revisión de mataderos (FTE-09C-04) | 3,8–17,9 kL/t de **carcasa** | ~8–38 (con ~2,1 kg de carcasa) | 3,8–17,9 | Sí (base distinta: carcasa vs producto) |
| Brasil (FTE-09C-03) | 22–30 L/ave | 22–30 | ~9–12,5 | Sí |

Expresar el consumo **en las dos unidades** sirve para detectar inconsistencias: un dato en L/ave de aves livianas (2,3 kg en EE.UU.) no es comparable directamente con uno de aves de 2,9 kg; el m³/t corrige el tamaño del ave pero depende de la base (carcasa, producto, peso vivo). El modelo emite la alerta `AGUA_M3_T` si el m³/t de producto sale del rango 3,8–17,9 (test **U28**).

**Cautelas:** (1) un extracto da "escaldado 5–15 gal/ave", incompatible con el mínimo de ~1 cuarto de galón: se interpreta como total de la planta y no se usa por etapa; (2) otro da lavados de carcasa de 2–6 gal/ave (7,6–22,7 L), muy superior a 4,25 L: inconsistencia registrada; (3) todas las cifras son de EE.UU. o Brasil; (4) ninguna aclara si incluye despiece o lavado de camiones. **Dato argentino faltante: DPV-067.**

## 4. Agua por escala (sensibilidad)

`[ESTIMACIÓN]` = L/ave × aves / 1.000. Día **operativo**. Año con 250 días de faena.

| Escala (aves/día op.) | Agua utilizada m³/día (bajo · **medio** · alto) | Agua descargada m³/día¹ | Evaporada/arrastrada m³/día (medio) | Agua incorporada t/día | m³/año (medio) | Caudal horario medio m³/h bajo 12 h (medio)² |
|---|---|---|---|---|---|---|
| 2.500 | 38 · **62** · 95 | 30 · **55** · 90 | 7 | 0,53 | 15.600 | 5,2 |
| 5.000 | 75 · **125** · 190 | 60 · **110** · 180 | 14 | 1,06 | 31.300 | 10,4 |
| 10.000 | 150 · **250** · 380 | 120 · **220** · 361 | 28 | 2,13 | 62.500 | 20,8 |
| 20.000 | 300 · **500** · 760 | 240 · **440** · 722 | 56 | 4,25 | 125.000 | 41,7 |

¹ Con la fracción a efluente **supuesta** (80 / 88 / 95 %). ² Sobre 12 h (8 h netas + 4 h de limpieza, `[SUPUESTO]`); el CSV agrega un caudal horario máximo **ilustrativo** (× 1,8, `[SUPUESTO]`) que no es dato de diseño: el caudal de diseño surgirá del perfil horario real.

**Lecturas:**
1. Una planta de 10.000 aves/día **podría** usar del orden de 150–380 m³/día según su eficiencia. No es un consumo esperado: es el rango dentro del cual hay que preguntar a cada sitio.
2. La incertidumbre (bajo vs alto, ×2,5) es mayor que duplicar la escala: la gestión del agua pesa tanto como la escala.
3. **El agua puede limitar la capacidad:** si un sitio entrega, por ejemplo, 20 m³/h durante 12 h (240 m³/día), el nivel alto a 10.000 aves/día no entra sin reserva, reúso o una segunda fuente (DPV-053, DPV-087).

## 5. Calidad del agua — necesidades conceptuales

**No se diseña ninguna planta de tratamiento.**

| Tema | Por qué importa | Qué se necesita saber | Estado |
|---|---|---|---|
| **Potabilidad** | El agua en contacto con producto y superficies debe ser potable (Decreto 4238/68; CAA art. 982) | Análisis físico-químico y microbiológico completo | Normas leídas solo en extractos `[PVDP]` (FTE-016, FTE-09C-16) |
| **Perforación vs red** | Caudal disponible, riesgo de corte, permisos | Ensayo de bombeo, acuífero, permiso de explotación; caudal y presión garantizados por la red | DPV-053 |
| **Arsénico, flúor, nitratos** | Parte de la llanura chaco-pampeana puede superar límites (CAA: As ≤ 0,01 mg/L `[PVDP]`) | Análisis en el sitio; la potabilización con rechazo hace que **agua captada > agua utilizada** | DPV-053 |
| **Dureza** | Incrustaciones en caldera, escaldador, intercambiadores | Dureza y alcalinidad | Sin dato |
| **Hierro y manganeso** | Depósitos, obstrucción de boquillas | Fe, Mn | Sin dato |
| **Tratamiento** | Filtración, ablandamiento, remoción de As/Fe, desinfección según análisis | Parámetros que exceden | No se diseña |
| **Cloración** | Desinfección y cloro residual; antimicrobianos en chiller y lavados | Demanda de cloro; normativa de antimicrobianos (`16_normativa_senasa`) | Pendiente |
| **Almacenamiento** | Autonomía frente a cortes y absorción del pico horario | Autonomía deseada, reserva contra incendio | Referencia conceptual: 1 día de uso = 62 / 125 / 250 / 500 m³ (medio); no es diseño |
| **Presión** | Lavados de carcasa, limpieza, esterilizadores | Presión de red o presurización | Sin dato |
| **Temperatura** | Agua fría ahorra frío en el chiller pero pide más calor | Temperatura estacional | Modelo: 18 °C `[SUPUESTO]` |
| **Agua para exportación** | Auditorías de importadores revisan potabilidad y registros | Requisitos por destino ([`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md)) | Pendiente |

## 6. Reúso de agua (conceptual)

Las fuentes de EE.UU. describen reúso del agua del chiller para escaldado o transporte de vísceras bajo reglas sanitarias específicas (FTE-09C-01). En Argentina **no se relevó** qué admite el Decreto 4238/68 (DPV-061). Opción a estudiar: acercaría el nivel alto al bajo y **cambiaría la relación entre agua utilizada y efluente**.

## 7. Qué medir

Consolidado en [`conclusiones_agua_efluentes.md` §7](conclusiones_agua_efluentes.md).
