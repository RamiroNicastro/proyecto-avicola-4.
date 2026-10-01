# Conclusiones de alimento balanceado e integración upstream (sesión 14B)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría final de sincronización productiva e inventarios) · Base: [`integracion_upstream.md`](integracion_upstream.md), [`demanda_alimento.md`](demanda_alimento.md), [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md), [`almacenamiento_silos.md`](almacenamiento_silos.md), [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_upstream.py`](modelo_upstream.py), [`escenarios_upstream.csv`](escenarios_upstream.csv). Incubación: [`../15_incubacion/conclusiones_incubacion.md`](../15_incubacion/conclusiones_incubacion.md).

> **MODELO PRELIMINAR COMPLETADO** (físico; 21/21 tests). **Sin decisión de integración:** DEC-020, DEC-023 y DEC-024 siguen abiertas. **Sin CAPEX/OPEX, sin precios, sin fabricante, sin cadencia elegida, sin datos de campo.** Toda cifra externa `[PVDP]` (DPV-009).

---

## 1. Hallazgos

1. **El alimento es el mayor flujo físico del sistema:** 8,8 / 17,7 / 35,3 / 70,6 t/día de entrega y 3.091 / 6.181 / 12.362 / 24.724 t/año (medio, 5 d) para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas/día. Escala **linealmente** con la faena (test U03); lo único no lineal son los viajes enteros (3 / 5 / 9 / 18 entregas de 28 t por semana).
2. **Maíz + harina de soja ≈ 85–95 % del tonelaje.** No hay fórmula: eso es del nutricionista.
3. **Capacidad de una planta propia (corregido en v1.1):** la t/h requerida es el producto de cinco factores explícitos: escala, días de fabricación, horas por día, eficiencia y margen. El rango "~1–25 t/h" de la v1.0 iba de 2.500 aves/día con 6 d × 16 h (0,9 t/h) a 20.000 desfavorable con 5 d × 8 h y eficiencia 0,75 (24,8 t/h); con fabricación concentrada en 3 días llega a ~41 t/h. Con la demanda propia de 2.500 aves/día, una planta de 2,1 t/h trabajaría ~35 h por semana: **baja utilización si se opera todos los días bajo la cadencia asumida**, lo que podría resolverse fabricando menos días, concentrando lotes, sirviendo a terceros o manteniendo capacidad estratégica (decisión económica, no tomada).
4. **Silos ≠ inventario (corregido en v1.1):** los silos dependen de días de stock, densidad y número de materias primas (los días mueven el volumen más de 3 veces); no hay silo estándar. El **inventario** se separa por categoría (alimento terminado en granja y en planta, maíz, soja, micros-aceite-otros, material en proceso) y por propiedad. Con los mismos días, **el stock físico de la cadena es igual en todas las arquitecturas**: integrar cambia quién lo posee y dónde está. La comparación v1.0 "106 / 583 / 653 t" sumaba categorías y universos distintos y se retira.
5. **Façon tiene dos variantes** que deben distinguirse: materias primas de la empresa (B1: stock propio en casa del elaborador) o del elaborador (B2: stock propio solo en granja). Quién compra y quién mantiene stocks es un dato contractual a relevar (DPV-14B-03).
6. **La demanda física es idéntica en compra, integración parcial o total** (test U05).
7. **Pollito:** incubar huevo comprado **sustituye** la dependencia de proveedores de pollito por la de proveedores de huevo fértil; la concentración real de esa oferta es DPV-14B-02 ([`../15_incubacion/compra_vs_incubacion.md`](../15_incubacion/compra_vs_incubacion.md)).
8. **Sincronización (nuevo en v1.1):** existe un **posible problema de sincronización entre tamaño de lote de nacimiento, capacidad de galpones y cadencia de faena**, más visible a escala chica (a 2.500 aves/día, cosechar un galpón equivalente de 15.000–30.000 aves lleva ~6–12 días de faena). No demuestra incompatibilidad: debe validarse con la arquitectura real de las granjas ([`integracion_upstream.md` §4](integracion_upstream.md)).
9. **Acoplamiento operativo:** integrar granjas obliga a proveer pollito y alimento; comprar pollo vivo vuelve irrelevantes las otras dos decisiones.

## 2. Escenarios a llevar a la comparación económica (sin preferencia)

> Todas las opciones son **escenarios de comparación** con el mismo estatus. La columna "benchmark de comparación" indica solo contra qué opción se medirán las diferencias de CAPEX/OPEX; **no es un caso base ni una recomendación** (test U20). El modelo financiero debe poder comparar todas las opciones sin favorecer ninguna por diseño.

| Eslabón | Benchmark de comparación | Escenarios de comparación (mismo estatus) | Condición para modelarlo | Capacidad física a modelar |
|---|---|---|---|---|
| **Pollito BB** | A. Compra | A. Compra · B. Huevo fértil + incubación · C. Reproductoras | C: solo como arquitectura futura / sensibilidad (test U07) | B: setter 55.824–446.593 y hatcher 12.343–148.120 posiciones según escala y cadencia |
| **Alimento** | A. Compra | A. Compra · B1. Façon con MP propias · B2. Façon con MP del elaborador · C. Planta propia | C: fijar explícitamente días, horas, eficiencia y margen de fabricación | C: 0,9–41 t/h según factores; silos según días de stock |
| **Granjas** | A. Pollo vivo de terceros | A. Pollo vivo · B. Integrados · C. Propias · Mixto | Arquitectura real de granjas para el chequeo de sincronización | Plazas y m² de `03` (9.500–75.900 m² medio) |

## 3. Arquitecturas de madurez de referencia (sin orden obligatorio)

Arquitectura 0: pollito y alimento comprados, granjas de terceros, faena a façon posible · 1: planta de faena propia, upstream comprado o parcialmente integrado · 2: más granjas e integración · 3: alimento y/o incubación propios · futura: reproductoras/genética solo con justificación. **Son referencias, no un recorrido**: si existieran demanda, capital y ventaja económica suficientes, una función podría integrarse antes. Detalle: [`integracion_upstream.md` §3](integracion_upstream.md).

## 4. Datos faltantes principales

| Dato | Registro |
|---|---|
| Precio y condiciones del alimento por fase puesto en granja | DPV-050 |
| Façon: quién compra materias primas, quién mantiene inventario, mínimo de lote, servicio nutricional, mermas, almacenamiento, frecuencia de producción, capacidad disponible | DPV-14B-03, DPV-14B-04 |
| Proveedores de grano: volumen anual, calidad, contratos, estacionalidad | DPV-14B-05, DPV-117 |
| Plantas de alimento en operación: t/h reales, eficiencia, turnos, días de fabricación, energía, dotación | DPV-14B-07 |
| Densidades y días de stock reales; silos de granja | DPV-14B-04 |
| Incubadoras: días de nacimiento, lote mínimo, mínimos contractuales, flexibilidad, uniformidad, ventana de entrega, estacionalidad, capacidad futura | DPV-047, DPV-14B-10 |
| Arquitectura real de granjas (galpones por granja, plazas por galpón, llenado y cosecha) | DPV-048, DPV-133 |
| Registro SENASA de fábricas de alimento y medicados | DPV-14B-06 |
| Integradores: condiciones para un tercero y prácticas de sincronización | DPV-14B-08 |

## 5. Tests (21/21 correctos)

| Test | Qué valida |
|---|---|
| U01 | Conservación de pollitos y huevos (hacia adelante recupera la demanda; cadena recibidos > cargados > fértiles > nacidos > vendibles ≥ alojados > cargadas > faenadas) |
| U02 | Capacidad instalada ≥ requerida (setter, hatcher, almacén de huevo, planta de alimento) — **adaptado en v1.1** a setter/hatcher con cadencia |
| U03 | Alimento lineal con la escala; viajes enteros no lineales por redondeo (explicado y acotado) |
| U04 | Silos e inventarios ∝ días de stock, ∝ 1/densidad; n.º de silos PENDIENTE sin volumen unitario |
| U05 | Opciones calculadas por separado, con la misma demanda física |
| U06 | Faltantes PENDIENTES con valor vacío (lead time de entrega, lote de proveedor, galpones reales, material en proceso, capacidades de camión…); parámetros inválidos se rechazan |
| U07 | Reproductoras = 0 en las arquitecturas 0 y 1 |
| U08 | Sin precios ni variables económicas en el CSV |
| U09 | Pollitos y alimento idénticos a `03` |
| U10 | Monotonía (incubación, margen, mortalidad; ovoscopia reduce el hatcher) |
| U11 | Unidades válidas |
| **U12** | Setter y hatcher dimensionados por separado (permanencias y flujos propios; cambiar uno no cambia el otro) |
| **U13** | Conservación temporal: ocupación media simulada = ley de Little; cargas en régimen = demanda; ocupación máxima ≤ posiciones de diseño para cada cadencia |
| **U14** | Recepción, carga, transferencia, nacimiento y entrega son eventos distintos; incubación = 21 d con cualquier almacenamiento |
| **U15** | Lote de nacimiento = demanda / cadencia ≠ demanda media semanal; sin cadencia → PENDIENTE |
| **U16** | Granja ≠ galpón (unidad de colocación explícita; identidad de capacidad con `03`) |
| **U17** | Elasticidad de huevos = −1 para fertilidad y para incubabilidad; diferencias de variación solo por rango |
| **U18** | Alimento terminado y materias primas en categorías separadas, sin totales mezclados |
| **U19** | Stock propio vs en tercero separados; stock de la cadena por categoría igual en todas las arquitecturas |
| **U20** | Todas las opciones = escenario de comparación; benchmark ≠ preferencia; sin "caso base" ni orden obligatorio de arquitecturas |
| **U21** | Banderas de sincronización coherentes; sin dato → PENDIENTE; cosecha × aves por unidad = faena diaria |

## 6. Calidad

**MEDIA** como marco y modelo físico reproducible; **BAJA** como evidencia para decidir integrar (sin oferta, precios, capacidades ni arquitectura de granjas relevadas). Ningún parámetro de planta, silos, cadencia o incubación está verificado.
