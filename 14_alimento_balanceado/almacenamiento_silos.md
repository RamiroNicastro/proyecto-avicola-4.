# Almacenamiento: silos de materias primas, alimento terminado y granja

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B · Modelo: [`modelo_upstream.py`](modelo_upstream.py) (función `almacenamiento`, bloque `7_silos` del CSV)

> **Solo desde variables.** El almacenamiento se calcula a partir de **consumo diario, días de stock, densidad aparente y número de materias primas**. **No hay "silo estándar"**: el número de silos queda PENDIENTE mientras no se fije un volumen unitario (`VOLUMEN_UNITARIO_SILO_M3 = None`; test U06). Todos los parámetros son variables o supuestos editables.

---

## 1. Fórmulas

```
t almacenadas_i      = consumo_t_día_i × días_de_stock_i
m³ útiles_i          = t almacenadas_i / densidad aparente_i (t/m³)
m³ brutos_i          = m³ útiles_i / factor de llenado (0,90; SUP-14B-09)
silos mínimos        = n.º de materias primas a granel + n.º de tipos de alimento terminado
                       (segregación: una celda por producto, independiente del volumen)
n.º de silos_i       = techo(m³ brutos_i / volumen unitario)  → PENDIENTE (sin volumen unitario)
```

- **Consumo diario:** alimento entregado (semana plena / 7) de [`demanda_alimento.md`](demanda_alimento.md); materias primas = alimento × inclusión ilustrativa (maíz 60 %, harina de soja 30 %; SUP-032).
- **Días de stock** (SUP-14B-10; días calendario de consumo): maíz 7 / 15 / 30; harina de soja 7 / 15; alimento terminado en planta 1 / 2 / 3; silos de granja 2 / 3 / 5. Son **decisiones de diseño y de compra** (cosecha, precio, continuidad, riesgo de corte de rutas), no datos.
- **Densidad aparente** (SUP-14B-09): maíz ~0,72 t/m³; harina de soja 0,56–0,67 t/m³; alimento terminado 0,55 / 0,60 / 0,65 t/m³ (barrido). Fuente: extractos de tablas técnicas (FTE-14B-003 `[PVDP]`); varía con humedad, granulometría, pellet vs harina y compactación (DPV-14B-04).

## 2. Qué se almacena según la opción de alimento

| Opción | Silos de granja | Granos (maíz, harina de soja) | Alimento terminado en planta |
|---|---|---|---|
| **A. Compra de alimento** | Sí (propios o del integrado) | No | No (lo tiene el proveedor) |
| **B. Façon** | Sí | **Sí, como stock propio**, aunque esté físicamente en la planta del elaborador o en un acopio (capital de trabajo) | No |
| **C. Planta propia** | Sí | Sí, en silos propios | Sí, celdas por fórmula |

## 3. Resultados (perfil y desempeño medios, 5 d; maíz 15 d, soja 15 d, alimento en planta 2 d, granja 3 d; densidades 0,72 / 0,60 / 0,60)

| Planta | Opción | Granja: t / m³ brutos | Maíz: t / m³ | Harina de soja: t / m³ | Alimento en planta: t / m³ | **Stock total (t)** | Silos mínimos por segregación (planta) | N.º de silos |
|---|---|---|---|---|---|---|---|---|
| 2.500 | A compra | 26 / 49 | 0 | 0 | 0 | **26** | 0 | — |
| 2.500 | B façon | 26 / 49 | 79 / 123 | 40 / 74 | 0 | **146** | 0 (silos del elaborador) | — |
| 2.500 | C planta | 26 / 49 | 79 / 123 | 40 / 74 | 18 / 33 | **163** | 5 | PENDIENTE |
| 5.000 | A compra | 53 / 98 | 0 | 0 | 0 | **53** | 0 | — |
| 5.000 | B façon | 53 / 98 | 159 / 245 | 79 / 147 | 0 | **291** | 0 | — |
| 5.000 | C planta | 53 / 98 | 159 / 245 | 79 / 147 | 35 / 65 | **327** | 5 | PENDIENTE |
| 10.000 | A compra | 106 / 196 | 0 | 0 | 0 | **106** | 0 | — |
| 10.000 | B façon | 106 / 196 | 318 / 491 | 159 / 294 | 0 | **583** | 0 | — |
| 10.000 | C planta | 106 / 196 | 318 / 491 | 159 / 294 | 71 / 131 | **653** | 5 | PENDIENTE |
| 20.000 | A compra | 212 / 392 | 0 | 0 | 0 | **212** | 0 | — |
| 20.000 | B façon | 212 / 392 | 636 / 981 | 318 / 589 | 0 | **1.166** | 0 | — |
| 20.000 | C planta | 212 / 392 | 636 / 981 | 318 / 589 | 141 / 262 | **1.307** | 5 | PENDIENTE |

`[ESTIMACIÓN]` · ESCENARIO. Silos mínimos = 2 materias primas a granel + 3 fórmulas; con 3–4 materias primas a granel y 4 fórmulas, 6–8 celdas (barrido `N_MP_GRANEL`, `N_TIPOS_ALIMENTO`).

**Silos de granja:** los 49–392 m³ son el **total agregado** de todas las granjas. Cada granja necesita su propio silo (o más de uno por galpón) dimensionado para su consumo **pico** del final del lote, que es mayor que el promedio; ese dimensionamiento por granja requiere la curva diaria de consumo y el tamaño de cada granja (DPV-045, DPV-048). Hoy no se calcula.

## 4. Sensibilidad a los días de stock (planta propia, 10.000 aves faenadas/día)

| Maíz (d) | Harina de soja (d) | Alimento en planta (d) | m³ brutos en planta (maíz + soja + alimento) |
|---|---|---|---|
| 7 | 7 | 1 | 432 |
| 7 | 7 | 2 | 497 |
| 7 | 7 | 3 | 563 |
| 15 | 15 | 1 | 850 |
| 15 | 15 | 2 | 916 |
| 15 | 15 | 3 | 981 |
| 30 | 15 | 1 | 1.341 |
| 30 | 15 | 2 | 1.406 |
| 30 | 15 | 3 | 1.472 |

**Lectura:** los días de stock mueven el volumen **más de 3 veces** para la misma escala (432 → 1.472 m³); el volumen es proporcional a los días (test U04). Guardar maíz de cosecha (meses, no días) es una **estrategia comercial de compra de granos** que cambiaría el almacenamiento en otro orden de magnitud (p. ej. 6 meses —182,5 d— de maíz a 10.000 aves/día ≈ 3.870 t ≈ 5.970 m³ brutos `[ESTIMACIÓN]` con las mismas variables); no se supone.

## 5. Inventario físico total del upstream (medio, 5 d)

| Planta | Alimento en un ciclo de crianza (t, de 03) | Granos en planta / façon (15 d, t) | Alimento en silos (t, granja 3 d + planta 2 d) | Huevos fértiles en almacén (5 d, opción B) | Aves vivas simultáneas (ritmo pleno, de 03) |
|---|---|---|---|---|---|
| 2.500 | 415 | 119 | 44 | 13.426 | 86.396 |
| 5.000 | 830 | 238 | 88 | 26.851 | 172.793 |
| 10.000 | 1.660 | 477 | 177 | 53.703 | 345.586 |
| 20.000 | 3.320 | 954 | 353 | 107.406 | 691.171 |

`[ESTIMACIÓN]`. Huevos en almacén con margen de capacidad de 15 % ([`../15_incubacion/capacidad_incubacion.md`](../15_incubacion/capacidad_incubacion.md)). Todo escala linealmente para días de stock fijos. **Sin valorización** (no hay precios en esta fase).
