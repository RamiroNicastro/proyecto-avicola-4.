# Conclusiones — proceso industrial y equipamiento conceptual por escala

**Fecha:** 2026-09-30 · **Versión:** 1.1 (sesión 09A, en paralelo con otras sesiones; corrección conceptual final en §0) · Base: [`flujo_proceso.md`](flujo_proceso.md), [`zonificacion_higienica.md`](zonificacion_higienica.md), [`cuellos_botella.md`](cuellos_botella.md), [`arquitecturas_por_escala.md`](arquitecturas_por_escala.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py), [`capacidad_proceso.csv`](capacidad_proceso.csv), [`../08_maquinaria/catalogo_equipos.md`](../08_maquinaria/catalogo_equipos.md), [`../08_maquinaria/automatizacion_por_escala.md`](../08_maquinaria/automatizacion_por_escala.md), [`../08_maquinaria/proveedores_preliminares.md`](../08_maquinaria/proveedores_preliminares.md), [`../08_maquinaria/requerimientos_cotizacion.md`](../08_maquinaria/requerimientos_cotizacion.md), [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv), [`../08_maquinaria/fuentes_09A.csv`](../08_maquinaria/fuentes_09A.csv)

> **Pregunta central:** ¿qué procesos, equipos y cuellos de botella tiene que resolver una planta para procesar 2.500, 5.000, 10.000 o 20.000 aves/día?
> **No** se elige escala, proveedor, equipo, método de enfriamiento ni de aturdido, turnos, layout ni localización; **no** se calcula CAPEX ni OPEX. Modelos físicos anteriores sin cambios (test T08). Registros globales **no** modificados: las actualizaciones están en [`actualizaciones_gestion_09A.md`](actualizaciones_gestion_09A.md) con IDs provisionales.

---

## 0. Corrección conceptual final (v1.1)

| Tema | v1.0 | v1.1 |
|---|---|---|
| Eficiencia 0,70–0,90 | Presentada como eficiencia real de línea | **Solo rango de sensibilidad del modelo**, descompuesto en disponibilidad (D) y factor de velocidad (R); se distinguen velocidad nominal declarada, de diseño, garantizada y operativa, disponibilidad, eficiencia, OEE, microparadas y paradas planificadas ([`cuellos_botella.md` §2](cuellos_botella.md)) |
| Evisceración manual | "Deja de ser práctica por encima de ~1.000 aves/h" | **Sin umbral fijo.** Un fabricante documenta evisceración manual hasta ~1.600 broilers/h (BAADER Compact Plant 396). El umbral económico argentino se determina con cotizaciones y productividad real |
| Automático en todas las escalas | Aturdido, escaldado, desplumado y enfriamiento "automáticos" | **Arquitectura de referencia a estudiar** (mecanizado o automático), no obligación universal |
| 16 h netas | "No entran en un día" | **Restricción severa de calendario** con los supuestos actuales; puede resultar inviable; **validar antes de descartar**. Ecuación de 24 h con holgura y alerta |
| Capacidad de planta | Un solo concepto | Capacidad teórica de equipo → cuello de botella → capacidad operativa de planta → producción real |
| Limpieza | Tiempo fijo | `t_limpieza(escala, configuración, automatización)` provisional; no se usa para descartar arquitecturas |
| Proveedores | Todo `[PVDP]` | BAADER CP396, Meyn LEAP y JBT Marel/Calisa2 elevados a **fuente primaria del fabricante** (lectura del promotor); Calisa2 **no** es benchmark económico |
| RFQ | Capacidad nominal y real | **Definición contractual de capacidad y condiciones de garantía** como dato crítico; 31 campos |
| Modelo | 13 tests, 5 mutaciones | **18 tests, 9 mutaciones** detectadas |

## 1. Flujo industrial completo

Recepción (pesaje, documentación, ante mortem) → espera ventilada → descarga → colgado → aturdido → degüello → sangrado → escaldado → desplumado → corte de patas (y cabeza) → **transferencia** (límite zona sucia / evisceración) → venteo y apertura → extracción de vísceras → **inspección veterinaria** → menudencias, cuello y vísceras no comestibles por separado → lavado → **enfriamiento** (inmersión, aire o mixto) → escurrido → clasificación → **entero / trozado / deshuesado** → envasado → control y rotulado → encajonado → refrigeración o **congelado** → cámaras → expedición. Flujos separados: sangre, plumas, cabezas, vísceras + contenido, decomisos (bajo control oficial), patas → garras, menudencias + cuello, carcasa → venta/CMS/rendering, hueso y piel (config. C), efluentes. Detalle con 32 etapas y kg/ave de cada salida: [`flujo_proceso.md`](flujo_proceso.md). Zonas: vivo → faena sucia → evisceración → limpia refrigerada → empaque → cámaras → expedición, más zona de subproductos con salida propia y tres circuitos de vehículos: [`zonificacion_higienica.md`](zonificacion_higienica.md).

## 2. Principales equipos

76 equipos conceptuales en 9 grupos ([`matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv)): recepción (balanza, cajones o módulos, descarga, andén ventilado, lavado); faena (transportador aéreo con grilletes, aturdidor eléctrico o CAS, degolladora, canal de sangrado, escaldadora, desplumadoras, canal de plumas, cortadoras, transferencia); evisceración (transportador, venteo, abridora, evisceradora, presentación para inspección, puestos de inspección, menudencias, lavadora); enfriamiento (inmersión, aire, mixto; agua helada); procesamiento secundario (clasificadora, trozado manual o automático, deshuese en conos o automático, fileteado, trimming, garras, CMS); packaging (bolsa, bandeja + film, termosellado/MAP, termoformado, vacío, balanza etiquetadora, detector de metales); congelado (túnel estático, continuo, espiral, placas, criogénico); frío y cámaras; subproductos (bombas, tanques, tamices, tolvas, vacío); servicios (aire, agua, grupo electrógeno, espuma, esterilizadores, trazabilidad).

## 3. Capacidades horarias

Ritmo operativo `[ESTIMACIÓN]` (T01: idéntico a `23_plan_expansion`); columnas nominales `[SUPUESTO]` de **sensibilidad**, no desempeño demostrado.

| Escala | 6 h netas | **8 h** | 10 h | 16 h | Nominal a pedir a 8 h netas en marcha (R 0,95–0,82) |
|---|---|---|---|---|---|
| 2.500 | 417 | **312** | 250 | 156 | 329–381 |
| 5.000 | 833 | **625** | 500 | 312 | 658–762 |
| 10.000 | 1.667 | **1.250** | 1.000 | 625 | 1.316–1.524 |
| 20.000 | 3.333 | **2.500** | 2.000 | 1.250 | 2.632–3.049 |

- **Nominal ≠ garantizada ≠ operativa ≠ real:** si una línea de 2.500 aves/h nominales rindiera η 0,70–0,90 (sensibilidad) en 8 h programadas, produciría ~14.000–18.000 aves/día (T11). El valor real depende de la definición de "aves/h" de cada fabricante, de la velocidad **garantizada** y de la disponibilidad medida.
- **Ecuación de 24 h:** 24 = faena neta + paradas + pausas + cambios de turno + arranque + cierre + limpieza intermedia + limpieza + sanitización + mantenimiento + holgura. Con 8 h netas el establecimiento opera ~14–21 h/día. **Con 16 h netas, la holgura es +0,9 / −2,8 / −8,3 h** (escenarios optimista / medio / conservador): **restricción severa de calendario que puede resultar inviable; debe validarse con proveedores y plantas reales antes de descartarla** (SUP-09A-02; DEC-036). Horas netas máximas con holgura ≥ 0: 16,6 / 13,8 / 10,0.

## 4. Manual vs automático por escala

| Operación | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aturdido–escaldado–desplumado–enfriamiento (arquitectura de referencia) | Mc/A | A | A | A |
| Colgado | M | M | M | M |
| **Evisceración** | M | M/S | M/S/A a comparar | S/A (manual a comparar) |
| Clasificación | M | M/S | A | A |
| Trozado | M | M/S | S/A | A |
| Deshuese | M | M | M/S | S + A por pieza (opcional) |
| Envasado | M/S | S | A | A |
| Congelado | Terceros o túnel estático | S | S/A | A |

**Evisceración sin umbral fijo:** la transición manual → semiautomática → automática depende de velocidad, costo y disponibilidad de mano de obra, ergonomía, inspección, uniformidad, calidad, higiene y economía de escala; un fabricante documenta evisceración manual hasta ~1.600 aves/h (BAADER Compact Plant 396); el umbral argentino se determinará con cotizaciones y productividad real (21–42 puestos equivalentes a 20.000 aves/día muestran el tamaño del problema de personal, no un límite técnico). Los niveles son **arquitectura de referencia a estudiar**, no obligación. **Más automatización no es siempre mejor:** mejora consistencia y mano de obra por ave, empeora mantenimiento, dependencia de técnicos y flexibilidad; con lotes de peso desparejo, baja utilización o técnicos lejanos, lo manual puede convenir ([`automatizacion_por_escala.md` §4](../08_maquinaria/automatizacion_por_escala.md)). Nada decidido (DEC-09A-01).

## 5. Principales cuellos de botella

1. **Colgado** — manual en todas las escalas; límite humano (5 → 42 aves/min).
2. **Evisceración + inspección** — puestos manuales o equipos según la comparación del §4; puestos de inspección por velocidad de línea **sin norma leída** (DPV-09A-03).
3. **Enfriamiento** — tiempo de residencia fijo: 260 → 2.083 carcasas en inmersión; 469–781 → 3.750–6.250 en aire.
4. **Trozado y deshuese** — dependen del mix: 636 → 5.091 kg/h a trozar; 359 → 2.875 kg/h a deshuesar (config. C).
5. **Congelado y cámaras** — hasta 24 t/día a congelar (P3) y 336 t en 7 días de producción a 20.000.
6. **Ventana horaria** (limpieza + mantenimiento), **subproductos** (1,5 → 12,2 t/día de sólidos), **agua, efluentes, frío** y **mano de obra**.

**La línea principal no es la capacidad de la planta** (capacidad teórica de equipo → cuello de botella → capacidad operativa de planta → producción real): disponibilidad y velocidad < 100 %, etapas más lentas, tiempos de residencia, servicios, ventana horaria, personal, mix de productos y retiro de subproductos ([`cuellos_botella.md` §6](cuellos_botella.md)).

## 6. Equipos críticos

**CRÍTICO — detiene la faena:** transportadores aéreos, aturdido, escaldadora y su agua caliente, desplumadoras y canal de plumas, puestos de inspección, enfriamiento y agua helada, cámaras de refrigeración, sala de máquinas de frío, agua potable, esterilizadores/lavamanos, aire comprimido (líneas automáticas), evisceradora (si la línea depende de evisceración automática). **IMPORTANTE — reduce capacidad:** 36 equipos con bypass manual o parcial. **SECUNDARIO:** 21 equipos resolubles en el día. **Automatizar convierte tareas manuales en equipos críticos.** Repuestos, N+1, bypass, preventivo y dependencia de técnicos: [`catalogo_equipos.md` §2](../08_maquinaria/catalogo_equipos.md).

## 7. Modularidad

Mantener (balanza, aturdidor si su rango lo cubre), duplicar (calderas, compresores, puestos, túneles estáticos, envasadoras), ampliar (transportador, escaldadora, desplumadoras en serie, chiller, trozado modular, cámaras) y reemplazar (evisceración manual → automática, descarga, transferencia, embolsado, clasificación). Una línea rápida (sin redundancia) vs dos líneas (una sigue si la otra falla; crecimiento por etapas; más personal y superficie): comparada **sin recomendación** ([`arquitecturas_por_escala.md` §8](arquitecturas_por_escala.md); DEC-09A-02). **Flexibilidad:** todo hasta la clasificación es común; entero, trozado, deshuesado, congelado y exportación se diferencian en salas refrigeradas, empaque, congelado, cámaras y estándar higiénico — lo difícil de agregar después es el espacio refrigerado y el frío, no las máquinas (§7 del mismo archivo).

## 8. Proveedores encontrados

**Fuente primaria del fabricante** (páginas oficiales; lectura del promotor, la sesión no pudo abrirlas): **BAADER Compact Plant 396** (~600–1.600 broilers/h con evisceración manual; expansión prevista), **Meyn LEAP** (concepto modular ~1.300 → 15.000 aves/h; no implica que la inversión inicial llegue a 15.000), **JBT Marel — Calisa2** (Argentina, 9.500 → 15.000 aves/h, evisceración automatizada; **referencia tecnológica, no benchmark de CAPEX, dotación, costo por ave, escala mínima eficiente ni automatización**). El resto `[PVDP]`: **Integrales:** JBT Marel (500/1.000–15.000 aves/h; oficina de representación en CABA según directorio de terceros), Meyn (~500 a > 8.000; en Avícola y Porcinos 2026), BAADER/Linco, Foodmate/Systemate (trozado hasta 6.000–7.200), Prime Equipment Group. **Pequeña escala/especialistas:** Bayle (150–1.500), Mayekawa (deshuese 1.000–1.500 piezas/h), Cantrell-Gainco, Plant in a Box (~500), Engmaq (~40). **Packaging/congelado:** ULMA/Harpak-ULMA, Multivac, GEA, JBT Frigoscandia. **Argentinos:** Ing. Galimberti (línea de faena, escaldador a pedido; capacidad no publicada), Rosarossa y Rovi (artesanal). **China:** Raniche (500–5.000), Xinbaiyun/Eruis (200–10.000), Henger (500–1.000). **Usados:** Drobtech, Use Poultry Tech, Isotek. **Servicio técnico local no verificado para ninguno.** Nuevo vs usado vs reacondicionado: usado atractivo en equipos simples o líneas completas probadas; riesgoso en automáticos complejos; sin decisión (DEC-09A-03).

## 9. Información a cotizar

Base de diseño común (escalas, 8 h netas con sensibilidad, 2,9 kg con rango 2,2–3,5, productos, inmersión y aire, eléctrico y CAS, estándar SENASA/UE); **dato crítico: definición contractual de capacidad y condiciones de garantía** (peso/rango, producto, dotación, disponibilidad, alimentación, mantenimiento, tolerancia a variabilidad, rechazos/paradas máximos, velocidad garantizada, prueba de aceptación); y 31 campos por equipo: capacidad nominal y **real con referencias**, rango de producto, dimensiones, potencia, agua, aire, vapor, frío, efluente, personal, precio, Incoterm, instalación, puesta en marcha con capacidad garantizada, capacitación, repuestos (stock en Argentina), garantía, mantenimiento, lead time, servicio técnico local, tiempo de limpieza, ampliabilidad, materiales, referencias y validez. 11 lotes de cotización con preguntas específicas ([`requerimientos_cotizacion.md`](../08_maquinaria/requerimientos_cotizacion.md)). **No se envía todavía.**

## 10. Qué debe aprender Ramiro

[`guia_ramiro.md`](guia_ramiro.md): qué es una línea de faena; qué significa aves/h (312 aves/h = un pollo cada 11,5 s; 2.500 = uno cada 1,4 s); cuello de botella (la cañería sale al ritmo del tramo más angosto); disponibilidad y microparadas; horas de faena ≠ horas de planta; automatización con sus pros y contras; redundancia; mantenimiento; y **por qué una línea de 2.500 aves/h no produce 20.000 aves/día** (η < 1 → ~16.000; las demás etapas, servicios, personal, abastecimiento y demanda tienen que acompañar). Tres preguntas para cada visita.

## 11. Archivos

**Creados:** `05_proceso_industrial/flujo_proceso.md`, `zonificacion_higienica.md`, `cuellos_botella.md`, `arquitecturas_por_escala.md`, `guia_ramiro.md`, `conclusiones_proceso.md`, `actualizaciones_gestion_09A.md`, `modelo_capacidad_proceso.py`, `capacidad_proceso.csv`; `08_maquinaria/catalogo_equipos.md`, `automatizacion_por_escala.md`, `proveedores_preliminares.md`, `requerimientos_cotizacion.md`, `matriz_equipos.csv`, `fuentes_09A.csv`.
**Modificados:** `05_proceso_industrial/README.md` y `08_maquinaria/README.md` (contenido y documentación del modelo y de la matriz, regla 15). **Sin cambios:** `00_gestion_proyecto/`, `25_fuentes/`, modelos y CSV de `03`, `04`, `07`, `23`, y `capacidad_preliminar.md`.

## 12. Limitaciones

1. **La sesión no pudo leer ninguna fuente primaria** (WebFetch/curl bloqueados). Tres páginas oficiales de fabricantes fueron leídas por el promotor y se elevaron; normativa y demás referencias quedan `[PVDP]`.
2. **Ningún dato de planta argentina:** disponibilidad, factor de velocidad y eficiencia (solo sensibilidad), ventana horaria, productividades manuales y tiempos de limpieza son sensibilidades o referencias extranjeras.
3. **Normativa de faena sin leer** (puestos de inspección por velocidad, temperaturas, zonas): puede introducir cuellos de botella regulatorios no modelados.
4. **Capacidades de proveedores = nominales declaradas** (incluso las de fuente primaria), no garantizadas ni reales; cada fabricante puede definir "aves/h" distinto; presencia y servicio técnico en Argentina no verificados (salvo indicios para JBT Marel y Meyn, débiles).
5. **Matriz de equipos, criticidad y niveles de automatización** son hipótesis de trabajo (SUP-09A-05).
6. `t_limpieza` **no escala** todavía con tamaño, configuración ni automatización (relación provisional; no se usa para descartar arquitecturas).
7. **No se dimensionan** agua, efluentes, frío, energía, superficies ni dotación (otros módulos).
8. Configuración B (trozado) como referencia de carga; el mix real (DPV-037) cambia el cuello de botella.
9. IDs provisionales pendientes de reconciliación.

## 13. Evaluación de calidad

- [x] Capacidad de línea ≠ capacidad de planta (T03, T11; §1 de `cuellos_botella.md`).
- [x] Sin precios, sin CAPEX/OPEX (T07).
- [x] Sin proveedor elegido; orden alfabético por categoría y advertencia explícita.
- [x] Sin escala elegida; las cuatro escalas analizadas en paralelo.
- [x] Proceso limpio y sucio separados: zonas, fronteras, 14 cruces a evitar.
- [x] Sin automatización total asumida; operaciones manuales en todas las escalas y casos donde lo manual conviene.
- [x] Segundo turno ni asumido ni descartado: ecuación de 24 h con alerta, holgura +0,9 / −2,8 / −8,3 h a 16 h netas, a validar; 8 condiciones a verificar.
- [x] Factores de eficiencia/disponibilidad solo como sensibilidad (T14); capacidad efectiva ≤ nominal salvo justificación (T15); capacidades de proveedores bloqueadas como diseño (T18).
- [x] Trazabilidad: ritmos = `escenarios_escala.csv` (T01); flujos = balance v1.1 (T04); modelos anteriores intactos (T08); fuentes con ID; supuestos registrados.
- [x] Modelo reproducible v1.1: 18/18 tests, 9/9 mutaciones detectadas.
- [ ] Verificación documental primaria por la sesión (bloqueada; tres fuentes de fabricante leídas por el promotor).
- [ ] Datos de plantas argentinas y respuestas de proveedores.

**Evaluación: MEDIA** como modelo conceptual y método (flujo completo, zonificación, cargas por etapa trazables al balance, ventana horaria, criticidad, modularidad, RFQ accionable, tests y mutaciones); **BAJA** como evidencia de capacidad real, costos o proveedores (sin fuentes primarias, sin datos argentinos, sin cotizaciones). Sirve para **saber qué preguntar a proveedores y plantas y dónde mirar los cuellos de botella**, no para especificar equipos ni elegir escala.
