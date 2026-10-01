# Demanda de alimento balanceado por escala

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B · Modelo: [`modelo_upstream.py`](modelo_upstream.py) (bloques `4_alimento` y `5_materias_primas` de [`escenarios_upstream.csv`](escenarios_upstream.csv))

> El tonelaje sale de `03` (alimento = aves cargadas × peso vivo × FCR de campo; [`../03_produccion_primaria/alimentacion.md`](../03_produccion_primaria/alimentacion.md) §1–2), **importado sin recalcular** (test U09). Aquí se lo reexpresa en t/día, t/semana y t/año para dimensionar compra, façon o planta, y se separan las categorías de materias primas. **No es una fórmula** y no contiene precios. Base: alimento terminado **entregado a granja** (la base del FCR de campo). Perfil medio (47 d, 2,9 kg vivo).

---

## 1. Toneladas por escala (5 días de faena/semana; favorable / **medio** / desfavorable)

| Planta (aves faenadas/día) | t/día de entrega (semana plena / 7) | t/día promedio calendario (año / 365) | t/semana plena | t/semana (promedio anual) | **t/año** | t de un ciclo de crianza (capital de trabajo físico) |
|---|---|---|---|---|---|---|
| 2.500 | 8,3 / **8,8** / 9,6 | 8,0 / **8,5** / 9,2 | 58 / **62** / 67 | 56 / **59** / 65 | 2.906 / **3.091** / 3.370 | 390 / **415** / 453 |
| 5.000 | 16,6 / **17,7** / 19,3 | 15,9 / **16,9** / 18,5 | 116 / **124** / 135 | 111 / **119** / 129 | 5.812 / **6.181** / 6.740 | 780 / **830** / 905 |
| 10.000 | 33,2 / **35,3** / 38,5 | 31,8 / **33,9** / 36,9 | 232 / **247** / 270 | 223 / **237** / 259 | 11.623 / **12.362** / 13.480 | 1.561 / **1.660** / 1.810 |
| 20.000 | 66,4 / **70,6** / 77,0 | 63,7 / **67,7** / 73,9 | 465 / **494** / 539 | 446 / **474** / 517 | 23.246 / **24.724** / 26.960 | 3.122 / **3.320** / 3.620 |

`[ESTIMACIÓN]` · ESCENARIO. Con 6 días de faena/semana (medio): 10,6 / 21,2 / 42,4 / 84,8 t/día de entrega; 74 / 148 / 297 / 593 t por semana plena; 3.709 / 7.417 / 14.835 / 29.669 t/año. Rango completo de `03` (perfiles liviano a pesado, todos los desempeños): **2.200–40.400 t/año**.

**Por qué dos "t/día":** las granjas comen los 7 días aunque la planta faene 5. La **t/día de entrega** (semana plena / 7) dimensiona silos de granja y camiones; el **promedio calendario** (año / 365) es menor porque incluye las semanas con feriados (menos alojamientos). Para dimensionar se usa la semana plena; para volúmenes anuales de compra, el año.

**Linealidad:** el alimento escala exactamente con la faena (test U03: duplicar la faena duplica todas las toneladas; el kg por ave no cambia). Lo único no lineal son los **viajes enteros** (redondeo hacia arriba).

## 2. Reparto por fase

Perfil medio: inicio ~5 %, crecimiento ~27 %, terminación ~68 % del tonelaje ([`../03_produccion_primaria/alimentacion.md` §3](../03_produccion_primaria/alimentacion.md); SUP-032). Implicancia para el upstream: **la mayor parte del volumen es un solo tipo de alimento (terminación)**, pero la planta o el proveedor debe producir y entregar **al menos 3–4 fórmulas** (inicio en migaja, crecimiento y terminación en pellet, retiro), cada una con su silo o celda y su lote mínimo.

## 3. Categorías de materias primas (separación conceptual, NO fórmula)

> **Recetas reales = nutricionista / formulación** (DEC-14B-03). Las inclusiones son rangos de orden de magnitud de una dieta maíz–soja típica (`03` §4; FTE-160 `[PVDP]`) y dependen de precios relativos, disponibilidad regional, fase y restricciones de clientes (p. ej. harinas animales). El punto ilustrativo solo existe para maíz y harina de soja (SUP-032: 60 % / 30 %; el 10 % restante se reparte entre las otras categorías sin asignar).

| Categoría | Qué incluye | Inclusión (% del alimento) | Por qué importa en el upstream |
|---|---|---|---|
| **Maíz** | Maíz (o sorgo, trigo como sustitutos parciales) | ~55–65 % | Mayor volumen: define silos, camiones de grano y la cercanía a zonas productoras (criterio ALI-01 de `10`) |
| **Soja** | Harina de soja (y/o expeller) | ~25–35 % (más en inicio) | Segundo volumen; proviene de plantas de molienda (ALI-02); calidad variable (proteína, procesamiento) |
| **Aceite** | Aceite de soja, grasas | ~1–5 % (más en terminación) | Tanque, no silo; calefacción o agitación según producto |
| **Minerales** | Fosfato mono/dicálcico, carbonato de calcio, sal, bicarbonato | ~2,3–3,5 % | Bolsas o *big bags*; algunos a granel en plantas grandes |
| **Vitaminas** | Premezcla vitamínico-mineral | ~0,2–0,5 % | Microingrediente: dosificación precisa, almacenamiento controlado, en general importada o dolarizada |
| **Otros** | Aminoácidos sintéticos (metionina, lisina, treonina), enzimas, anticoccidianos, otros aditivos, sustitutos (DDGS, harinas de origen animal) | ~0,2–1,3 % (más sustitutos si se usan) | Microingredientes con medicación o carencia: control de retiro antes de la faena; registro y trazabilidad |

### 3.1 Toneladas por categoría (medio, 5 d; rango mín–máx, punto ilustrativo entre paréntesis)

| Planta (aves faenadas/día) | Maíz t/año | Harina de soja t/año | Aceite t/año | Minerales t/año | Vitaminas t/año | Otros t/año |
|---|---|---|---|---|---|---|
| 2.500 | 1.700–2.009 (1.854) | 773–1.082 (927) | 31–155 | 71–108 | 6–15 | 6–40 |
| 5.000 | 3.400–4.018 (3.709) | 1.545–2.163 (1.854) | 62–309 | 142–216 | 12–31 | 12–80 |
| 10.000 | 6.799–8.035 (7.417) | 3.091–4.327 (3.709) | 124–618 | 284–433 | 25–62 | 25–161 |
| 20.000 | 13.598–16.071 (14.835) | 6.181–8.653 (7.417) | 247–1.236 | 569–865 | 49–124 | 49–321 |

`[ESTIMACIÓN]`. Los rangos de cada fila **no suman** 100 % entre sí (son rangos independientes); una fórmula real elige un punto que suma 100 %. **Lectura:** maíz + harina de soja ≈ 85–95 % del tonelaje; los otros cuatro grupos suman poco volumen pero son los que más exigen en dosificación, compra en divisas y control de calidad.

## 4. Implicancias para compra vs fabricación

- **Compra de alimento:** la empresa compra ~3.100–24.700 t/año (medio) de alimento terminado en 3–4 fórmulas; su capacidad física propia es solo la de **recepción en granja** (silos de granja, propios o del integrado).
- **Façon:** la empresa compra **materias primas** (~2.800–22.250 t/año de maíz + harina de soja en el punto ilustrativo, más el 10 % restante) y las entrega a un elaborador: aparece **logística y stock de granos** propios.
- **Planta propia:** aparecen recepción y almacenamiento de granos, molienda, dosificación, mezclado, pellet y despacho ([`planta_alimento_conceptual.md`](planta_alimento_conceptual.md)).

Comparación: [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md). Almacenamiento: [`almacenamiento_silos.md`](almacenamiento_silos.md).
