# Almacenamiento e inventarios: silos de instalaciones y stock de material por categoría

**Fecha:** 2026-10-01 · **Versión:** 1.1 (inventarios separados por categoría y por propiedad) · Sesión 14B · Modelo: [`modelo_upstream.py`](modelo_upstream.py) (funciones `almacenamiento` e `inventario_alimento`; bloques `7_silos` y `7_inventarios` del CSV)

> **Dos preguntas distintas, dos secciones distintas.** (1) **Silos:** qué volumen de almacenamiento debe **tener instalado** la empresa en cada arquitectura (§1–4). (2) **Inventarios:** cuánto **material** hay en la cadena, de qué categoría, **de quién es** y **dónde está** (§5). La v1.0 presentaba juntos 106 / 583 / 653 t (compra / façon / planta propia a 10.000 aves/día) como "stock total": eran sumas de categorías distintas (alimento terminado + granos) y de universos distintos (propiedad de la empresa, sin el stock que mantiene el tercero). **Esa comparación se retira.**
>
> **Solo desde variables.** Consumo diario, días de stock, densidad aparente y número de materias primas. **No hay "silo estándar"**: el número de silos queda PENDIENTE (test U06). **Todos los días de stock son supuestos hasta validación** (SUP-14B-10).

---

## 1. Fórmulas

```
t almacenadas_i      = consumo_t_día_i × días_de_stock_i
m³ útiles_i          = t almacenadas_i / densidad aparente_i (t/m³)
m³ brutos_i          = m³ útiles_i / factor de llenado (0,90; SUP-14B-09)
silos mínimos        = n.º de materias primas a granel + n.º de tipos de alimento terminado
n.º de silos_i       = techo(m³ brutos_i / volumen unitario)  → PENDIENTE (sin volumen unitario)
```

- **Consumo diario:** alimento entregado (semana plena / 7) de [`demanda_alimento.md`](demanda_alimento.md); por categoría: maíz 60 %, harina de soja 30 % (SUP-032), micros-aceite-otros 10 % (resto ilustrativo).
- **Días de stock (supuestos):** maíz 7 / **15** / 30; harina de soja 7 / **15**; micros-aceite-otros 15 / **30** / 60; alimento terminado en planta 1 / **2** / 3; silos de granja 2 / **3** / 5 (en negrita, el valor de parámetro usado en las tablas). Son decisiones de diseño y de compra, no datos.
- **Densidad aparente:** maíz ~0,72 t/m³; harina de soja 0,56–0,67; alimento terminado 0,55 / 0,60 / 0,65 (FTE-14B-003 `[PVDP]`; DPV-14B-04). Los micros, aceite y otros se almacenan en bolsas, *big bags* o tanques: m³ no calculados.

## 2. Silos que cada arquitectura obliga a tener instalados

| Arquitectura | Silos de granja | Silos de granos | Celdas de alimento terminado |
|---|---|---|---|
| **A. Compra de alimento** | Sí (en granjas integradas o propias) | No | No |
| **B. Façon** | Sí | **No propios** (los granos están en el elaborador o en un acopio; si fueran de la empresa, el stock es propio pero el silo no) | No |
| **C. Planta propia** | Sí | Sí | Sí (≥ 1 por fórmula) |

## 3. Volumen de silos (perfil y desempeño medios, 5 d; maíz 15 d, soja 15 d, alimento en planta 2 d, granja 3 d; densidades 0,72 / 0,60 / 0,60)

| Planta | Silos de granja (todas las arquitecturas): t / m³ brutos | **Solo C**: maíz t / m³ | **Solo C**: harina de soja t / m³ | **Solo C**: alimento terminado t / m³ | **Solo C**: celdas mínimas por segregación | N.º de silos |
|---|---|---|---|---|---|---|
| 2.500 | 26 / 49 | 79 / 123 | 40 / 74 | 18 / 33 | 5 | PENDIENTE |
| 5.000 | 53 / 98 | 159 / 245 | 79 / 147 | 35 / 65 | 5 | PENDIENTE |
| 10.000 | 106 / 196 | 318 / 491 | 159 / 294 | 71 / 131 | 5 | PENDIENTE |
| 20.000 | 212 / 392 | 636 / 981 | 318 / 589 | 141 / 262 | 5 | PENDIENTE |

`[ESTIMACIÓN]` · ESCENARIO. Celdas mínimas = 2 materias primas a granel + 3 fórmulas; con 3–4 materias primas y 4 fórmulas, 6–8. Los m³ de granja son el **total agregado**; cada granja necesita su silo dimensionado para su consumo pico (curva diaria y tamaño de granja: DPV-045, DPV-048).

## 4. Sensibilidad a los días de stock (planta propia, 10.000 aves faenadas/día)

| Maíz (d) | Harina de soja (d) | Alimento en planta (d) | m³ brutos de silos en planta (maíz + soja + alimento) |
|---|---|---|---|
| 7 | 7 | 1 | 432 |
| 7 | 7 | 3 | 563 |
| 15 | 15 | 2 | 916 |
| 30 | 15 | 1 | 1.341 |
| 30 | 15 | 3 | 1.472 |

Los días de stock mueven el volumen **más de 3 veces** para la misma escala (test U04). Guardar maíz de cosecha (meses) es una estrategia comercial que cambiaría el almacenamiento en otro orden de magnitud (6 meses a 10.000 aves/día ≈ 3.870 t ≈ 5.970 m³ brutos `[ESTIMACIÓN]`); no se supone.

---

## 5. Inventarios de alimento por categoría y por propiedad

### 5.1 Reglas

- **Categorías separadas** (test U18): alimento terminado en granja, alimento terminado en planta/elaborador, maíz, harina de soja, micros-aceite-otros, material en proceso. **No se suman categorías distintas**: una tonelada de maíz no es una tonelada de alimento terminado (etapa, valor, riesgo y lugar distintos).
- **Propiedad y ubicación separadas** (test U19): **stock propio** = material de la empresa (esté donde esté); **stock en tercero** = material del proveedor o elaborador que la cadena necesita.
- **Stock de la cadena** (por categoría) = propio + en tercero. Con los mismos días de stock, **es igual en todas las arquitecturas**: integrar no cambia cuánto material físico hay en la cadena, cambia **quién lo posee** (test U19).
- **Los días que mantiene un tercero no los decide la empresa y son PENDIENTES**: el stock en tercero se informa como **referencial**, calculado con los mismos días supuestos.
- **Material en proceso** (tolvas, mezcladora, pellet, enfriador): **PENDIENTE** en todas las arquitecturas (depende del equipo y la operación).
- El alimento de granja es **propio** cuando las granjas son integradas o propias (la empresa entrega el alimento). Si se compra **pollo vivo**, la empresa no tiene ningún inventario de alimento.

### 5.2 Quién posee qué en cada arquitectura

| Categoría | A. Compra de alimento | B1. Façon con materias primas **de la empresa** | B2. Façon con materias primas **del elaborador** | C. Planta propia |
|---|---|---|---|---|
| Alimento terminado en granja | Propio (silos de granja) | Propio | Propio | Propio |
| Alimento terminado en planta | Tercero (fábrica) | Propio, en el elaborador hasta el despacho | Tercero | Propio |
| Maíz | Tercero | **Propio, en el elaborador o en un acopio** | Tercero | Propio |
| Harina de soja | Tercero | Propio, en el elaborador o acopio | Tercero | Propio |
| Micros, aceite, otros | Tercero | Propio, en el elaborador | Tercero | Propio |
| Material en proceso | Tercero (PENDIENTE) | Propio, en el elaborador (PENDIENTE) | Tercero (PENDIENTE) | Propio (PENDIENTE) |
| **Qué queda físicamente en la operación de la empresa** | Solo el alimento en silos de granja | Solo el alimento en silos de granja (el resto está en el elaborador o acopio) | Solo el alimento en silos de granja | Todo |

Quién compra las materias primas en el façon y quién mantiene los stocks es una **condición contractual a relevar** (DPV-14B-03): el modelo mantiene B1 y B2 como variantes separadas.

### 5.3 Tabla de inventario: stock propio / stock en tercero (referencial), t (medio, 5 d; días de parámetro)

| Planta | Arquitectura | Alimento terminado en granja (3 d) | Alimento terminado en planta (2 d) | Maíz (15 d) | Harina de soja (15 d) | Micros-aceite-otros (30 d) |
|---|---|---|---|---|---|---|
| 2.500 | A compra | 26 / 0 | 0 / 18 | 0 / 79 | 0 / 40 | 0 / 26 |
| 2.500 | B1 façon, MP de la empresa | 26 / 0 | 18 / 0 | 79 / 0 | 40 / 0 | 26 / 0 |
| 2.500 | B2 façon, MP del elaborador | 26 / 0 | 0 / 18 | 0 / 79 | 0 / 40 | 0 / 26 |
| 2.500 | C planta propia | 26 / 0 | 18 / 0 | 79 / 0 | 40 / 0 | 26 / 0 |
| 10.000 | A compra | 106 / 0 | 0 / 71 | 0 / 318 | 0 / 159 | 0 / 106 |
| 10.000 | B1 façon, MP de la empresa | 106 / 0 | 71 / 0 | 318 / 0 | 159 / 0 | 106 / 0 |
| 10.000 | B2 façon, MP del elaborador | 106 / 0 | 0 / 71 | 0 / 318 | 0 / 159 | 0 / 106 |
| 10.000 | C planta propia | 106 / 0 | 71 / 0 | 318 / 0 | 159 / 0 | 106 / 0 |
| 20.000 | A compra | 212 / 0 | 0 / 141 | 0 / 636 | 0 / 318 | 0 / 212 |
| 20.000 | C planta propia | 212 / 0 | 141 / 0 | 636 / 0 | 318 / 0 | 212 / 0 |

`[SUPUESTO]` (días) · `[ESTIMACIÓN]` (t). 5.000 aves/día y las demás combinaciones: CSV, bloque `7_inventarios`. Material en proceso: PENDIENTE en todas.

### 5.4 Resumen por arquitectura (10.000 aves faenadas/día)

| Arquitectura | Stock propio | Stock en tercero (referencial; días del tercero PENDIENTES) | Stock total de la cadena (por categoría) | Días de cobertura (supuestos) |
|---|---|---|---|---|
| **A. Compra** | Alimento terminado en granja 106 t | Alimento terminado 71 t; maíz 318 t; soja 159 t; micros 106 t | Alimento terminado 106 + 71 t; maíz 318 t; soja 159 t; micros 106 t | Granja 3 d; planta 2 d; maíz 15 d; soja 15 d; micros 30 d |
| **B1. Façon, MP de la empresa** | Alimento terminado 106 + 71 t; maíz 318 t; soja 159 t; micros 106 t | 0 | Igual que A | Igual que A |
| **B2. Façon, MP del elaborador** | Alimento terminado en granja 106 t | Igual que A | Igual que A | Igual que A |
| **C. Planta propia** | Todo: 106 + 71 t; 318 t; 159 t; 106 t | 0 | Igual que A | Igual que A |

**Lectura:** con los mismos días de stock, el material de la cadena es el mismo en todas las arquitecturas; lo que cambia es la **propiedad** (capital de trabajo de la empresa) y la **ubicación** (qué silos debe tener). A y B2 tienen el mismo stock propio (solo granja); B1 y C también son iguales entre sí en propiedad, pero en B1 el material está en casa del elaborador y en C en silos propios. En la realidad los días **no** serán iguales: un tercero puede mantener más o menos stock, y una planta propia que fabrica pocos días por semana necesita más alimento terminado acumulado ([`planta_alimento_conceptual.md` §2.2](planta_alimento_conceptual.md)). Ejemplo: 4 días de alimento terminado en planta a 10.000 aves/día = 141 t en lugar de 71 t.

### 5.5 Otros inventarios físicos del upstream (medio, 5 d)

| Planta | Alimento en un ciclo de crianza (t, de 03; propio si hay integrados o granjas propias) | Huevos en almacén (opción B, 5 d, +15 %) | Huevos en proceso en setter + hatcher (opción B, media) | Aves vivas simultáneas (ritmo pleno, de 03) |
|---|---|---|---|---|
| 2.500 | 415 | 13.426 | 48.508 | 86.396 |
| 5.000 | 830 | 26.851 | 97.016 | 172.793 |
| 10.000 | 1.660 | 53.703 | 194.032 | 345.586 |
| 20.000 | 3.320 | 107.406 | 388.064 | 691.171 |

`[ESTIMACIÓN]`. Unidades distintas (t, huevos, aves): **no se suman**. Sin valorización (no hay precios en esta fase).
