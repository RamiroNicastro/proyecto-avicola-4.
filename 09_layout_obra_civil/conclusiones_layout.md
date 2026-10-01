# Conclusiones — layout y obra civil (sesión 12C)

**Fecha:** 2026-10-01 · **Versión:** 1.0.1 (corrección final de interpretación) · Fase 0 (prefactibilidad) · En paralelo con 12A (localización) y 12B (logística)

> **Pregunta central:** ¿qué áreas necesita la planta, cómo deben relacionarse y cómo puede crecer?
> **Respuesta corta:** necesita **54 áreas** en **nueve zonas** que se ordenan en una sola secuencia (sucia → transición → limpia → fría → despacho) con subproductos, utilities y personal **a los costados**; ocupa del orden de **1.800 / 2.600 / 4.300 / 7.500 m² construidos** (medio) para 2.500 / 5.000 / 10.000 / 20.000 aves/día, con rangos de ~2–3 veces; y el **terreno** del modelo resulta **~2 / 2,3 / 3,1 / 4,4 ha** medio sin escala objetivo, o **~3,3 ha** si desde el inicio se supone reservada toda la superficie para 20.000 aves/día. Todo es orden de magnitud: **23 de 54 áreas son PROXY**, ningún factor está validado y **no hay planos, CAPEX, terreno ni escala elegidos**.

> ⚠️ **Advertencia de uso.** Las superficies obtenidas sirven para comparar escalas y reservar órdenes de magnitud. No constituyen un anteproyecto arquitectónico ni una superficie habilitable. Deben recalcularse cuando existan footprints de proveedores, dotación, logística, normativa municipal y solución de efluentes.

---

## 1. Programa de áreas

54 áreas + reserva, cada una con zona, categoría, método, driver, dato faltante y **tipo de origen** (A derivada de modelo existente · B factor de diseño · C proxy preliminar · D footprint pendiente de proveedor · E requisito regulatorio pendiente; por código principal: 14 A, 16 B, 24 C): [`programa_areas.md` §2 bis](programa_areas.md). Categorías: proceso, frío, servicios, personal/admin (= **construidos**); + exteriores y efluentes (= **operativos**); + reserva, retiros y buffers (= **terreno**). Método: huella de equipos × envolvente cuando exista; driver físico + densidad (cámaras, andenes, vestuarios, tratamiento); proxy de intensidad con alerta cuando falta la huella; `NO_APLICA` explícito; modo estricto que deja `None` en lugar de inventar.

## 2. Zonificación

Nueve zonas de layout ([`zonificacion_layout.md`](zonificacion_layout.md)) mapeadas a las zonas higiénicas Z0–Z8/ZX/ZS/ZP de 09A. **No son categorías regulatorias** (SUP-12C-16). Siete fronteras críticas (F1 transferencia, F2 chiller, F3 frío/despacho, F4 producto/subproductos, F5 vivo/producto, F6 personal, F7 aire y agua). La zonificación **no se simplifica en la planta chica**: 2.500 aves/día exige la misma secuencia que 20.000.

## 3. Flujos

Nueve flujos por separado con diagramas y matriz de cruces ([`flujos_layout.md`](flujos_layout.md)). Reglas que definen el layout: tres circuitos de camiones que no se tocan (vivo, producto, subproductos); subproductos que salen **lateralmente** por canal/bomba/tornillo; personal que llega a cada zona solo desde su vestuario; envases por esclusa; desagües de limpio a sucio y pluviales separados. La matriz de cruces (§10) es la lista de control para cualquier esquema que se muestre a SENASA (DPV-115).

## 4. Superficies por escala (m², bajo / medio / alto)

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Proceso | 690 / 1.000 / 1.490 | 1.090 / 1.610 / 2.420 | 1.800 / 2.700 / 4.090 | 3.080 / 4.640 / 7.250 |
| Frío (P1, 3/14 d) | 100 / 140 / 220 | 120 / 180 / 350 | 180 / 330 / 660 | 310 / 600 / 1.310 |
| Servicios | 270 / 360 / 510 | 320 / 470 / 700 | 520 / 810 / 1.220 | 920 / 1.450 / 2.260 |
| Personal / admin | 170 / 270 / 490 | 170 / 330 / 620 | 230 / 470 / 880 | 340 / 760 / 1.440 |
| **Construidos** | **1.230 / 1.780 / 2.710** | **1.700 / 2.600 / 4.080** | **2.730 / 4.310 / 6.850** | **4.660 / 7.450 / 12.260** |
| Exteriores | 1.150 / 2.030 / 3.610 | 1.340 / 2.570 / 5.140 | 1.750 / 3.860 / 8.200 | 2.530 / 6.150 / 14.520 |
| Efluentes (reserva anaerobio + aerobio) | 130 / 220 / 520 | 130 / 250 / 780 | 140 / 330 / 1.520 | 160 / 590 / 3.030 |
| **Operativos** | **2.500 / 4.030 / 6.840** | **3.170 / 5.420 / 9.990** | **4.620 / 8.490 / 16.570** | **7.340 / 14.190 / 29.810** |

Lecturas: (1) ×8 en aves = ×4,2 en m² construidos (mínimos funcionales y exponente 0,8, un supuesto); (2) el frío depende más del **perfil y los días de stock** que de la escala (P3 7/28 ≈ 2,6 × P1 3/14 a 10.000 aves/día); (3) los m² por ave/día del modelo (0,23–1,08) caen dentro de la banda de referencias argentinas `[PVDP]` (0,11–1,45), lo que **no valida** el modelo pero descarta errores groseros. Detalle, frío por perfil, efluentes por tecnología y sensibilidad: [`layouts_por_escala.md`](layouts_por_escala.md).

## 5. Terreno conceptual

```
TERRENO = (huella de edificios + circulación + estacionamiento + playas + tratamiento + reserva de expansión)
          ampliado por retiros y buffers perimetrales;   ≥ huella ÷ FOS si el FOS se conoce
```

| Terreno (ha) | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Sin escala objetivo (reserva = fracción) | 0,8 / 2,0 / 5,3 | 0,9 / 2,3 / 6,5 | 1,2 / 3,1 / 8,7 | 1,7 / 4,4 / 12,8 |
| Reservando para 20.000 | 1,4 / 3,3 / 8,2 | 1,4 / 3,3 / 8,2 | 1,4 / 3,3 / 8,2 | 1,4 / 3,3 / 8,2 |
| Con lagunas (medio, sin objetivo) | 2,6 | 3,5 | 5,2 | 8,2 |

- **El edificio ocupa ~10–17 % del terreno medio.** En el escenario medio del modelo actual, los factores reservados para retiros, buffers y franjas representan aproximadamente **57 % del terreno conceptual a 10.000 aves/día** (50–68 % según la escala; 56 % reservando para 20.000). No es una exigencia conocida: hay que separar el **retiro reglamentario real** (municipio, DPV-12C-05; hoy 5 / 10 / 15 m supuestos), el **buffer de diseño** (supuesto/proxy 10 / 20 / 40 m, SUP-12C-15) y la **reserva sanitaria o ambiental** (supuesto o requisito según jurisdicción, DPV-106). Son variables: sin márgenes el terreno medio a 10.000 sería ~1,3 ha; con 10 m de retiro y sin buffer, ~1,8 ha (test T21). Por eso los datos del sitio pueden mover el terreno más que cualquier factor de proceso.
- **Lagunas:** en el escenario de superficies actual, el biológico con lagunas ocupa ~35–40 veces el compacto — **resultado del escenario actual / proxy, no relación general de ingeniería**; la relación real depende de tecnología, carga, clima, tiempo de retención, profundidad, calidad de efluente, terreno y normativa. Aun así, la dirección es clara: la tecnología de efluentes (DEC-043) y el terreno (DEC-003) deben evaluarse juntos.
- Insumo para 12A (localización): buscar terrenos con **capacidad de alojar la escala objetivo**, no la de arranque.

## 6. Estrategia de expansión

[`estrategia_expansion.md`](estrategia_expansion.md): dentro del modelo actual, **si se supone que desde el inicio se adquiere y reserva toda la superficie necesaria para la escala final de 20.000 aves/día**, las trayectorias 2.500→20.000, 5.000→20.000 y 10.000→20.000 convergen al mismo requerimiento conceptual de terreno (test T18) y difieren en cuánto se construye y cuándo (1.780 → 7.450 m² en la trayectoria A). Esto **no** implica que todas las estrategias de inversión requieran comprar el mismo terreno desde el día 1, ni que no pueda adquirirse superficie adicional, ni que no puedan tercerizarse funciones, ni que el terreno no cambie con la tecnología de efluentes, el congelado, el rendering, los accesos o la normativa. **Sobredimensionar** terreno, accesos, traza de circulación, orden de zonas, colector y troncales, permiso de vuelco; **dejar preparado** largo o ancho de nave, espacio junto al chiller, sala de máquinas, subestación, fachadas de docks y cámaras, terreno de efluentes y rendering; **modular/duplicar** línea, salas de corte, cámaras, túneles, compresores, calderas, docks, módulos de tratamiento. Principio de diseño preliminar (no regla arquitectónica universal): **preferir expansiones que prolonguen o dupliquen secuencias funcionales sin introducir cruces ni romper la zonificación higiénica**.

**Una línea vs dos:** en la parametrización actual del modelo, dos líneas ocupan ~21–22 % más en las salas de línea (resultado que puede cambiar con proveedor, footprint, buffers, mantenimiento, automatización y disposición física); dan redundancia parcial, permiten mantener y limpiar por sectores y crecer ocupando una franja reservada; una línea es más compacta pero sin redundancia y exige prever el largo final. **No se elige** (DEC-038).

## 7. Puntos difíciles de modificar

Terreno y accesos; portones y traza de circulación; dirección del flujo y fronteras F1/F2; pisos, pendientes, colector y pluviales; losas y fosos de equipos pesados; altura de naves; sala de máquinas, subestación y caldera con sus troncales; tratamiento de efluentes y permiso de vuelco; vestuarios y filtros sanitarios; fachadas de docks y recepción; posición del servicio oficial; retiros y distancias a vecinos ([`estrategia_expansion.md` §5](estrategia_expansion.md)). Agregar una máquina sin haberlos previsto puede requerir **romper pisos, muros y barreras sanitarias con la planta parada** ([`guia_ramiro.md` §7](guia_ramiro.md)).

## 8. Interfaz futura (simulador HTML) — **no se modificó el HTML**

Variables que el simulador debería recibir de `modelo_superficies.salida_interfaz(R)` (cada una como triple bajo / medio / alto y con su estado):

| Variable | Contenido | Nota para la interfaz |
|---|---|---|
| `m2_construidos` | Proceso + frío + servicios + personal/admin | Nunca rotularlo "terreno" |
| `m2_operativos` | Construidos + exteriores + efluentes | — |
| `m2_terreno` | Terreno conceptual con retiros y buffers | Mostrar siempre junto a `supuestos_terreno` (retiro, buffer, FOS y si son INPUT, SUPUESTO o PROXY) |
| `supuestos_terreno` | Retiro, buffer, FOS y su origen | Rotular "terreno variable con retiro, buffer y FOS" |
| `m2_por_categoria` | Siete categorías | Barra apilada por categoría |
| `m2_reserva_expansion` | Reserva hacia la escala objetivo + rendering | Input: escala objetivo (vacío = alerta) |
| `camaras` | Cámaras refrigeradas, congeladas, túnel, cámara de subproductos (m²) | Junto a `t_stock_refrigerado` / `t_stock_congelado` de 09C; **congelar ≠ almacenar** |
| `areas_por_funcion` | 54 áreas con nombre, zona, categoría, estado, **origen A–E** y rango | Etiquetas visibles: estado (PROXY / ESTIMACION / FOOTPRINT / NO_APLICA / PENDIENTE) y origen (A modelo existente · B factor de diseño · C proxy · D footprint pendiente · E requisito regulatorio pendiente) |
| `efluentes_por_tecnologia` | m² de efluentes con cloaca, compacto, anaerobio+aerobio, lagunas | Comparador; **sin ganador** |
| `alertas` | Códigos de alerta | Mostrar todas; nunca ocultarlas |
| `estado_global` | `RANGO` o `INCOMPLETO` (modo estricto) | Si `INCOMPLETO`, no mostrar totales |

Inputs a exponer: escala, horas netas, configuración A/B/C, perfil P1–P3 y días de inventario (con base temporal), automatización, líneas, enfriamiento, tecnología de efluentes, escala objetivo, reserva de rendering, dotación, aves y t por camión, retiro, buffer, FOS, modo estricto. La fuente de verdad sería `escenarios_superficies.csv`, como en v0.1 con `escenarios_escala.csv`.

## 9. Datos faltantes (prioridad para el layout)

1. **Huellas de equipos** por área (DPV-12C-01) — 23 áreas en proxy.
2. **Retiros, FOS y distancias** por sitio (DPV-12C-05) — dominan el terreno.
3. **Dotación** por turno y zona (DPV-12C-02) — vestuarios, comedor, estacionamiento.
4. **Requisitos edilicios del servicio oficial y del Decreto 4238/68** (DPV-12C-04, DPV-090).
5. **Tecnología y superficie de efluentes** (DPV-12C-08, DEC-043) y **lodos** (DPV-114).
6. **Capacidad de camiones y canal de despacho** (DPV-084, DPV-036; 12B).
7. **Densidad de estiba de cámaras** (DPV-12C-06) y **balance frigorífico** (DPV-109).
8. **Superficies reales de plantas argentinas** (DPV-12C-07).
9. Bomberos, exportación/Halal, lavado de camiones (DPV-12C-09 a 11).

Registro completo con IDs provisionales: [`actualizaciones_gestion_12C.md`](actualizaciones_gestion_12C.md); fuentes: [`fuentes_12C.csv`](fuentes_12C.csv) (10 fuentes, todas `[PVDP]`; ninguna leída en original).

## 10. Tests del modelo

`python3 09_layout_obra_civil/modelo_superficies.py` → **22/22 tests OK** (los 19 originales + 3 de integridad agregados en v1.0.1); `--mutaciones` → **7/7 mutaciones detectadas**. La v1.0.1 no cambia ninguna cifra: agrega el tipo de origen A–E por área, la columna `origen_superficie` del CSV, `supuestos_terreno` en la salida de interfaz y la fila `margen_perimetral_m`.

| Test | Qué prueba |
|---|---|
| T01 | Ninguna superficie negativa (100 escenarios) |
| T02 | Total = suma de áreas (categorías, construido, operativo, reserva, terreno) |
| T03 | Aumentar la escala (2.000–24.000) no reduce ningún área ni el terreno |
| T03b | Más horas netas reducen solo la línea, con alerta explícita (explicación documentada) |
| T04 | Más días de inventario no reducen el frío; duplicar días agranda cámaras, no el túnel |
| T05 | Mayor escala objetivo ⇒ mayor reserva y terreno; objetivo = actual ⇒ reserva 0 |
| T06 | Cada variable faltante genera alerta; al informarla, desaparece |
| T07 | Footprint desconocido ≠ 0: PROXY con alerta o, en modo estricto, `None` y totales `None`; footprint 0 rechazado |
| T08 | Escenarios independientes: el orden no altera resultados y no se modifican las entradas |
| T09 | Rango ordenado bajo ≤ medio ≤ alto |
| T10 | Terreno ≥ operativos ≥ construidos > 0 |
| T11 | Frío y efluentes tomados de 09C sin recalcular |
| T12 | Deshuese/CMS solo en config. C (NO_APLICA explícito); sala mínima de trozado en A |
| T13 | Dos líneas ocupan más que una |
| T14 | Cloaca < compacto < lagunas en área y terreno |
| T15 | CSV sin variables económicas y finito |
| T16 | Entradas inválidas rechazadas |
| T17 | Enfriamiento sin decidir reserva el mayor |
| T18 | En cada trayectoria con reserva total para la escala final, construido ≤ final y terreno = terreno final (propiedad aritmética del supuesto de reserva) |
| T19 | Ninguna superficie ni fila del CSV se etiqueta como verificada; toda área PROXY lleva origen C |
| T20 | Las salidas de terreno indican que retiro y buffer son variables (supuesto/proxy o input) |
| T21 | Cambiar retiro o buffer cambia el terreno y no los m² construidos |

## 11. Límites y advertencias

- **Orden de magnitud, no arquitectura:** ningún m² es una medida de sala; los rangos son amplios a propósito.
- **Proxies sin fuente:** los factores de intensidad (SUP-12C-01) y la dotación (SUP-12C-10) son del analista; su efecto puede verse con el modo estricto.
- **Benchmarks no comparables en alcance** (regla 18): se desconoce qué incluye cada m² declarado por las plantas citadas.
- **No se eligió** escala, terreno, tecnología de efluentes, método de enfriamiento, número de líneas, forma de nave ni proveedor; **no se calculó** CAPEX.
- **Coordinación con 12A y 12B:** los retiros/buffers/FOS (12A) y las capacidades y frecuencias de camiones (12B) reemplazan proxies de este modelo; sus resultados deben cargarse como inputs, no recalcularse aquí.
