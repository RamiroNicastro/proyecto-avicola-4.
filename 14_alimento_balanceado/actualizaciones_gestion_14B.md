# Propuestas de actualización de registros globales — sesión 14B (integración upstream)

> **ARCHIVO HISTÓRICO — RECONCILIADO el 2026-10-02.** Todo lo propuesto aquí ya fue integrado en `00_gestion_proyecto/` y `25_fuentes/`. Los IDs provisionales `14B` que aparecen abajo **ya no están activos**: sus equivalentes definitivos (y los casos consolidados en registros existentes) están en [`../00_gestion_proyecto/reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2. El CSV de fuentes provisional [`fuentes_14B.csv`](fuentes_14B.csv) se conserva **solo como histórico** (no es registro activo): las fuentes vigentes están en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv).

**Fecha:** 2026-10-01 · **Versión:** 1.1 (incluye la auditoría final de sincronización productiva e inventarios; ver §8) · Sesión en paralelo con 14A. **No se editaron** `00_gestion_proyecto/`, `25_fuentes/` ni archivos de otras sesiones (`03`, `13`, `23` solo se leyeron; `03` se importa desde el modelo sin modificarlo). Este archivo contiene lo que debe incorporarse al reconciliar la sesión.

> **IDs provisionales:** `SUP-14B-##`, `DPV-14B-##`, `DEC-14B-##`, `FTE-14B-###`. Al integrar, asignar el siguiente número libre de cada registro (al iniciar esta sesión los últimos eran **SUP-123, DPV-145, DEC-066 y FTE-297**; la sesión 14A puede haber tomado números en paralelo) y reemplazar los IDs provisionales en `14_alimento_balanceado/` y `15_incubacion/` (búsqueda de texto `14B-`), incluidos los comentarios de `modelo_upstream.py` y la columna `fuente`/`parametros` de `escenarios_upstream.csv` (regenerar con `python3 modelo_upstream.py`).

---

## 1. `supuestos.md` — nuevos

| ID provisional | Supuesto | Área | Estado | Relacionado |
|---|---|---|---|---|
| SUP-14B-01 | **Margen de pedido de pollitos** (pollitos pedidos por encima de los alojados: reposición, conteo, mortalidad de llegada) = **0 en la base**, barrido 1–2 %; es distinto del margen por mortalidad (que sale de `03`). No se supone excedente sin cargo del proveedor | Pollito BB | Vigente | DPV-047 |
| SUP-14B-02 | **Parámetros de incubación** (supuestos, no datos): fertilidad 0,95 / **0,92** / 0,88 e incubabilidad de fértiles 0,92 / **0,90** / 0,87 (favorable / medio / desfavorable); incubabilidad sobre cargados resultante 87,1 / **82,4** / 75,8 %. Referencia: 96,7 % y 93,5 % **en pico** (FTE-14B-001 `[PVDP]`) | Incubación | Vigente | DPV-14B-01, DPV-045 |
| SUP-14B-03 | **Pérdidas y descartes de incubación:** recepción/almacenamiento 0,5 / 1 / 2 %; transferencia 0,3 / 0,5 / 1 %; descarte en selección 0,5 / 1 / 2 % — sin fuente | Incubación | Vigente | DPV-14B-01 |
| SUP-14B-04 | **Tiempos de incubación:** 18 d de setter + 3 d de hatcher = **21 d de incubación (carga → nacimiento)**, 1 d de limpieza por carga en cada máquina; almacenamiento previo del huevo 3 / 5 / 7 d (óptimo 3–6 d citado, FTE-14B-001 `[PVDP]`); horas nacimiento → llegada a granja PENDIENTES; **el lead time recepción → pollito entregado (≥ 24–28 d) no es incubación**; ovoscopia: no (valor de parámetro) | Incubación | Vigente | DEC-14B-05 |
| SUP-14B-05 | **Margen de capacidad instalada** 10 / **15** / 20 % para incubación y planta de alimento: reserva de diseño, no óptimo | Upstream | Vigente | DEC-14B-01 |
| SUP-14B-06 | **Cadencia de cargas = nacimientos** (ilustrativa, no seleccionada): 1 (lunes), 2 (lunes y jueves), 3 (lunes, miércoles, viernes), 4 (lunes, martes, jueves, viernes), 5 (lunes a viernes); lotes iguales; posiciones de setter y hatcher = ocupación máxima simulada × (1 + margen); 6 / 10 h de ventana de selección, vacunación y carga por nacimiento — sin fuente | Incubación | Vigente | DPV-14B-10 |
| SUP-14B-07 | **Planta de alimento (escenario):** 5 / 6 días × 8 / 16 h de operación; eficiencia 0,75 / 0,85 (fracción de horas programadas con producción efectiva); factor de pico 1,0 (estacionalidad PENDIENTE) | Alimento | Vigente | DPV-14B-07 |
| SUP-14B-08 | **Categorías de materias primas** (no fórmula): maíz 55–65 %, harina de soja 25–35 %, aceite 1–5 %, minerales 2,3–3,5 %, vitaminas (premezcla) 0,2–0,5 %, otros 0,2–1,3 % (rangos de `03` §4); punto ilustrativo solo para maíz/soja (SUP-032). Recetas reales = nutricionista | Alimento | Vigente | SUP-032, DEC-14B-03 |
| SUP-14B-09 | **Densidades aparentes** (variables): maíz 0,72 t/m³; harina de soja 0,56 / 0,60 / 0,67; alimento terminado 0,55 / 0,60 / 0,65 (barrido, sin dato propio); **factor de llenado 0,90** (FTE-14B-003 `[PVDP]`) | Almacenamiento | Vigente | DPV-14B-04 |
| SUP-14B-10 | **Días de stock** (días calendario de consumo; decisiones de diseño y compra, no datos): maíz 7 / 15 / 30; harina de soja 7 / 15; **micros-aceite-otros 15 / 30 / 60**; alimento terminado en planta 1 / 2 / 3; silos de granja 2 / 3 / 5. **No hay volumen unitario de silo** (n.º de silos PENDIENTE); material en proceso PENDIENTE | Almacenamiento | Vigente | DPV-14B-04 |
| SUP-14B-11 | **Reproductoras equivalentes** (opción C, solo arquitectura futura) = pollitos/semana / 3,6 pollitos por reproductora por semana (ESTIMACIÓN de `03` §4.2); sin recría, machos ni reposición | Incubación | Vigente | DPV-045, SUP-034 |
| SUP-14B-12 | **Arquitecturas de madurez de referencia 0 / 1 / 2 / 3 / futura** = referencias de análisis **sin orden obligatorio** (una función puede integrarse antes si hay demanda, capital y ventaja económica); reproductoras = 0 en las arquitecturas 0 y 1. Todas las opciones make-or-buy son **escenarios de comparación**; la compra es solo **benchmark de comparación**, no caso base | Estrategia | Vigente | DEC-14B-01, DEC-018, DEC-020 |
| SUP-14B-13 | **Capacidad de camión de grano** 25 / 28 / 30 t: barrido ilustrativo, no capacidad legal ni elegida (sin elección → PENDIENTE) | Logística | Vigente | DPV-084 |
| SUP-14B-14 | **Granja ≠ galpón:** la unidad de colocación es variable (galpón o granja completa); plazas por galpón = pollitos/m² de `03` × m² de SUP-031 (~15.200 / 22.900 / 30.500 plazas equivalentes); galpones por granja reales PENDIENTES; **referencia de cosecha de 2 días de faena por unidad** (03/13 `[ESTIMACIÓN]`) y tolerancia de edad en una colocación PENDIENTE; el chequeo de sincronización marca REQUIERE VALIDACIÓN, no incompatibilidad | Sincronización | Vigente | DPV-048, DPV-133, DPV-14B-10 |
| SUP-14B-15 | **Inventarios por categoría y propiedad:** stock de la cadena = consumo de la categoría × días supuestos, igual en todas las arquitecturas; propio vs en tercero según la tabla de propiedad (A compra, B1 façon con materias primas propias, B2 façon con materias primas del elaborador, C planta propia); el stock en tercero es **referencial** (días del tercero PENDIENTES); no se suman categorías distintas | Inventarios | Vigente | DPV-14B-03, DPV-14B-04 |

### 1.1 Anotaciones a supuestos existentes

| Registro | Anotación propuesta (sesión 14B, 2026-10-01) |
|---|---|
| SUP-034 (no se asume granja ni incubadora propia) | **Se mantiene.** 14B modela la incubación propia (huevo fértil comprado) solo como alternativa de la arquitectura de referencia 3 y las reproductoras solo como arquitectura futura; test U07 garantiza 0 reproductoras en arquitecturas 0 y 1 |
| SUP-032 (reparto por fase y 60 / 30 maíz–soja) | Reutilizado como punto ilustrativo; el resto de categorías se trata como rango (SUP-14B-08) |
| SUP-096 (capacidades de escenario de vehículos) | Reutilizado: granelero 28 t (viajes de alimento) y barrido de pollitos 20 / 40 / 80 mil; sin capacidad de camión de pollitos ni de huevos el resultado es PENDIENTE |

## 2. `datos_por_validar.md`

### 2.1 Nuevos

| ID provisional | Dato | Para qué | Fuente sugerida | Prioridad sugerida (plan de campo) |
|---|---|---|---|---|
| DPV-14B-01 | **Parámetros reales de incubación**: fertilidad e incubabilidad por edad de reproductoras, descarte, pérdidas de recepción y transferencia, efecto de los días de almacenamiento | Reemplazar SUP-14B-02/03 | Incubadoras; manuales de reproductoras (DPV-045) | N3 |
| DPV-14B-02 | **Oferta de huevo fértil para terceros**: quién vende, volumen, calidad, edad de reproductoras, sanidad, contrato | Viabilidad de la opción B de pollito | Incubadoras, empresas de genética, integradoras (pregunta E5 del cuestionario) | N3 |
| DPV-14B-03 | **Fábricas de alimento y façon**: t/mes disponibles, pellet, **disposición a façon**, **quién compra las materias primas**, **quién mantiene el inventario** (dónde y cuántos días), **mínimo de lote** por fórmula, **fórmula / servicio nutricional**, **mermas**, **almacenamiento** disponible para el cliente, **frecuencia de producción**, **capacidad disponible**, entrega en granja, registro SENASA | Opciones A, B1, B2 de alimento; inventario propio vs en tercero | Fábricas de alimento balanceado (preguntas propuestas en §6; sin cuestionario nuevo) | N2 |
| DPV-14B-04 | **Densidades aparentes y días de stock reales**; silos de granja (t y m³ por galpón) | Reemplazar SUP-14B-09/10 | Fábricas; productores; fabricantes de silos (sin selección) | N4 |
| DPV-14B-05 | **Proveedores de grano**: volumen anual en el radio, contratos (a término/forward), calidad (humedad, micotoxinas, proteína), estacionalidad, logística | Opciones B y C de alimento | Acopios, cooperativas, corredores, plantas de molienda de soja | N3 (con DPV-117) |
| DPV-14B-06 | **Habilitaciones**: planta de incubación, fábrica de alimentos para animales (inscripción y registro SENASA; medicados), granjas de reproductoras — texto original | Requisitos de las opciones B/C | SENASA; Boletín Oficial | N3 |
| DPV-14B-07 | **Plantas de alimento en operación**: capacidad real en t/h de pellet, eficiencia, turnos, energía y vapor por t, dotación | Reemplazar SUP-14B-07 | Visitas a fábricas; proveedores (sin selección) | N3 |
| DPV-14B-08 | **Integradores existentes**: si ofrecerían pollito, alimento o crianza a un tercero; a qué volumen integraron alimento e incubación | Escala mínima de integración (cualitativa) | Integradoras; cámaras | N3 |
| DPV-14B-09 | **Capacidad de camiones de huevo fértil y de pollitos**, si el transporte está incluido, y **horas reales nacimiento → selección → vacunación → expedición → llegada a granja** | Viajes de insumos y lead time de entrega (hoy PENDIENTES) | Incubadoras; transportistas | N3 (amplía DPV-047 / DPV-084) |
| DPV-14B-10 | **Sincronización real incubadora–granja–faena**: días de nacimiento y tamaño de lote del proveedor; mínimo contractual semanal/mensual; flexibilidad de programación; ventana de entrega; **galpones por granja y plazas por galpón**; llenado por galpón o por granja; **tolerancia de edad** en una colocación; cosecha en cuántas noches o escalonada | Chequeo de sincronización (hoy REQUIERE VALIDACIÓN en escalas chicas) | Incubadoras; productores; integradoras | N2 (con DPV-133) |

### 2.2 Anotaciones a registros existentes

| Registro | Anotación propuesta |
|---|---|
| DPV-006 / DPV-047 (pollito BB) | Demanda media por semana plena 13.197 / 26.395 / 52.790 / 105.580 (medio, 5 d) ya en `03`; 14B agrega: **días de nacimiento, tamaño mínimo de lote, mínimo contractual semanal/mensual, flexibilidad de programación, uniformidad, ventana de entrega, disponibilidad estacional y capacidad disponible futura**; preguntar huevo fértil (DPV-14B-02) |
| DPV-045 (manuales) | Agregar manual de **incubación** y de reproductoras (fertilidad e incubabilidad por edad, almacenamiento) |
| DPV-050 (alimento) | Agregar disposición a **façon** y capacidad libre (DPV-14B-03) |
| DPV-084 (vehículos) | Agregar camiones de huevo fértil y de grano |
| DPV-133 (tamaño de lote) | Ver DPV-14B-10: el mismo problema aparece en la incubación propia |

## 3. `decisiones_pendientes.md`

### 3.1 Nuevas

| ID provisional | Decisión | Prioridad | Depende de | Carpeta |
|---|---|---|---|---|
| DEC-14B-01 | **Umbrales de volumen y condiciones (gates) para pasar de compra a integración parcial o total** en pollito, alimento y granjas, por fase | Media | Costos (fase CAPEX/OPEX), DPV-14B-02/03/05/07, DEC-001 | `14` / `15` / `23` |
| DEC-14B-02 | Planta de alimento (si se hace): una o dos líneas (redundancia), turnos | Baja (futura) | DEC-14B-01, escala | `14` |
| DEC-14B-03 | Forma física del alimento (pellet + migaja vs harina) y responsable de formulación | Media | Nutricionista; DPV-044 | `14` |
| DEC-14B-04 | Ubicación de una eventual planta de alimento (junto a faena / zona de granos / cerca de granjas) | Baja (futura) | DEC-003, ALI-01/02 de `10` | `14` / `10` |
| DEC-14B-05 | Tecnología de incubación (carga única vs múltiple; ovoscopia; vacunación in ovo) | Baja (futura) | DEC-023, DEC-14B-01 | `15` |
| DEC-14B-06 | **Cadencia de nacimientos y unidad de colocación** a modelar en la fase económica (si hay incubación propia o integrados): nacimientos por semana, llenado por galpón o granja, cosecha escalonada | Media | DPV-14B-10, DPV-048, DEC-020 | `15` / `03` / `14` |
| DEC-14B-07 | **Variante de façon** a comparar (B1 materias primas de la empresa / B2 del elaborador) | Media | DPV-14B-03 | `14` |

### 3.2 Anotaciones a decisiones existentes (siguen **abiertas**)

| Registro | Anotación |
|---|---|
| DEC-020 (abastecimiento de pollo vivo) | 14B muestra que la decisión de granjas arrastra las de pollito y alimento (integrar granjas obliga a proveer insumos). Sin ganador |
| DEC-023 (pollito BB) | Marco A/B/C en `15_incubacion/compra_vs_incubacion.md`; B sustituye la dependencia de proveedores de pollito por la de proveedores de huevo fértil (concentración: DPV-14B-02); C solo arquitectura futura |
| DEC-024 (alimento) | Marco compra / façon (B1, B2) / planta propia en `14_alimento_balanceado/compra_vs_fabricacion.md`; capacidad requerida 0,9–41 t/h según escala, desempeño, días, horas, eficiencia y margen |

## 4. `25_fuentes/registro_fuentes.csv`

Agregar las 5 filas de [`fuentes_14B.csv`](fuentes_14B.csv) (FTE-14B-001 a FTE-14B-005), todas `[PVDP]`; FTE-14B-004 y FTE-14B-005 de confiabilidad débil (sectorial/comercial).

## 5. `estado_proyecto.md` — propuesta

**Tablero:** agregar fila "Upstream: alimento e incubación (`14`, `15`) — **MODELO PRELIMINAR COMPLETADO** v1.1 (modelo físico, 21 tests; pollitos, cadena temporal, huevos, setter y hatcher con cadencia, sincronización granja/galpón–faena, alimento, planta conceptual, silos desde variables, inventarios por categoría y propiedad, make-or-buy como escenarios de comparación, arquitecturas de referencia). **INTEGRACIÓN = NO DECIDIDA** (DEC-020/023/024 abiertas); sin costos | Pendiente — incubadoras, fábricas, proveedores de grano, integradores | [`conclusiones_alimento.md`](conclusiones_alimento.md), [`conclusiones_incubacion.md`](../15_incubacion/conclusiones_incubacion.md)".

**Hito:** "2026-10-01 · Integración upstream (sesión 14B) · Modelo preliminar completado; sin decisión de integración".

## 6. Plan de trabajo de campo — propuesta

- Ola O4 (producción e incubación): agregar **fábricas de alimento / façon** (3–4) y **proveedores de grano** (2–3) con las preguntas de [`integracion_upstream.md` §6](integracion_upstream.md). **No se crea un cuestionario nuevo** en esta sesión para no duplicar el plan de campo; al reconciliar, decidir si se agregan como bloque a un instrumento existente.
- **Cuestionario de incubadoras** — agregar: días de nacimiento; tamaño mínimo de lote; mínimo contractual semanal/mensual; flexibilidad de programación; uniformidad; ventana de entrega (horas nacimiento → granja); disponibilidad estacional; capacidad disponible futura; huevo fértil (volumen, calidad, contrato).
- **Preguntas de alimento / façon** — quién compra las materias primas; quién mantiene el inventario (dónde, cuántos días); mínimo de lote por fórmula; fórmula / servicio nutricional; mermas; almacenamiento disponible; frecuencia de producción; capacidad disponible.
- **Cuestionario de productores** — agregar: galpones por granja y plazas por galpón; llenado por galpón o por granja; diferencia de edad aceptada en un mismo lote; noches de cosecha por galpón y cosecha escalonada.

## 7. Tensiones registradas (sin resolver)

| Tensión | Dónde |
|---|---|
| **Posible problema de sincronización** entre lote de nacimiento, capacidad de galpones y cadencia de faena (más visible a escala chica; no demuestra incompatibilidad) | `14_alimento_balanceado/integracion_upstream.md` §4 |
| Planta de alimento propia a escala chica: baja utilización si opera todos los días bajo la cadencia asumida (alternativas: menos días, lotes concentrados, terceros, reserva) | `planta_alimento_conceptual.md` §2.2 |
| Silos: el mínimo por segregación (5–8 celdas) no escala con el volumen | `almacenamiento_silos.md` §3 |

## 8. Auditoría final de sincronización productiva e inventarios (v1.1, 2026-10-01)

| Punto | Corrección | Dónde |
|---|---|---|
| Lead time | "24–28 días" ya no se llama incubación: incubación (carga → nacimiento) = 21 d; lead time recepción del huevo → pollito entregado = almacenamiento + 21 d + expedición (PENDIENTE) | `15_incubacion/modelo_incubacion.md` §2.1; test U14 |
| Setter / hatcher | Las "posiciones de incubadora" v1.0 (50.508 / 101.015 / 202.030 / 404.060) eran solo setter en flujo continuo × margen: se retiran. Setter y hatcher por separado con cadencia simulada: setter 55.824 / 111.648 / 223.296 / 446.593; hatcher 12.343–148.120 según cadencia | `15_incubacion/capacidad_incubacion.md`; tests U12, U13 |
| Cadencia | Lote de nacimiento = demanda / nacimientos por semana ≠ demanda media; cadencias ilustrativas, ninguna elegida | ídem §4; test U15 |
| Granja ≠ galpón | Se retira "la granja se llena de una sola vez"; unidad de colocación variable; chequeo de sincronización (multi-nacimiento, cosecha > 2 días) que marca REQUIERE VALIDACIÓN, no incompatibilidad | `integracion_upstream.md` §4; tests U16, U21 |
| Fertilidad vs incubabilidad | Elasticidad −1 para ambas; la diferencia de variación viene solo del rango supuesto | `capacidad_incubacion.md` §5; test U17 |
| Huevo fértil | Se retira "mercado más estrecho / menos vendedores": sustitución de dependencia; concentración = DPV-14B-02 | `compra_vs_incubacion.md`; `integracion_upstream.md` §2 |
| Planta de alimento | t/h con sus cinco factores; origen del rango "1–25 t/h"; "parada la mayor parte del día" reformulado como baja utilización bajo la cadencia asumida | `planta_alimento_conceptual.md` §2 |
| Inventarios | Se retira "106 / 583 / 653 t"; inventario por categoría y propiedad (propio / en tercero / cadena), façon B1/B2 | `almacenamiento_silos.md` §5; tests U18, U19 |
| Make or buy | "Caso base" reemplazado por **benchmark de comparación**; todas las opciones con el mismo estatus | `conclusiones_alimento.md` §2; test U20 |
| Fases | Arquitecturas de madurez de referencia sin orden obligatorio | `integracion_upstream.md` §3; test U20 |
| Datos de campo | Incubadoras y alimento/façon ampliados; propuestas para la reconciliación (§6), sin cuestionario nuevo | `integracion_upstream.md` §6 |
| Tests | 11 → 21; U02 adaptado (setter/hatcher con cadencia), U04 amplía a inventarios, U06/U07/U10 actualizados; los demás sin cambios de criterio | `modelo_upstream.py` |
