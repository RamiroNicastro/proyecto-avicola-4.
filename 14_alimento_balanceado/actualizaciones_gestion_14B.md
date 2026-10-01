# Propuestas de actualización de registros globales — sesión 14B (integración upstream)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión en paralelo con 14A. **No se editaron** `00_gestion_proyecto/`, `25_fuentes/` ni archivos de otras sesiones (`03`, `13`, `23` solo se leyeron; `03` se importa desde el modelo sin modificarlo). Este archivo contiene lo que debe incorporarse al reconciliar la sesión.

> **IDs provisionales:** `SUP-14B-##`, `DPV-14B-##`, `DEC-14B-##`, `FTE-14B-###`. Al integrar, asignar el siguiente número libre de cada registro (al iniciar esta sesión los últimos eran **SUP-123, DPV-145, DEC-066 y FTE-297**; la sesión 14A puede haber tomado números en paralelo) y reemplazar los IDs provisionales en `14_alimento_balanceado/` y `15_incubacion/` (búsqueda de texto `14B-`), incluidos los comentarios de `modelo_upstream.py` y la columna `fuente`/`parametros` de `escenarios_upstream.csv` (regenerar con `python3 modelo_upstream.py`).

---

## 1. `supuestos.md` — nuevos

| ID provisional | Supuesto | Área | Estado | Relacionado |
|---|---|---|---|---|
| SUP-14B-01 | **Margen de pedido de pollitos** (pollitos pedidos por encima de los alojados: reposición, conteo, mortalidad de llegada) = **0 en la base**, barrido 1–2 %; es distinto del margen por mortalidad (que sale de `03`). No se supone excedente sin cargo del proveedor | Pollito BB | Vigente | DPV-047 |
| SUP-14B-02 | **Parámetros de incubación** (supuestos, no datos): fertilidad 0,95 / **0,92** / 0,88 e incubabilidad de fértiles 0,92 / **0,90** / 0,87 (favorable / medio / desfavorable); incubabilidad sobre cargados resultante 87,1 / **82,4** / 75,8 %. Referencia: 96,7 % y 93,5 % **en pico** (FTE-14B-001 `[PVDP]`) | Incubación | Vigente | DPV-14B-01, DPV-045 |
| SUP-14B-03 | **Pérdidas y descartes de incubación:** recepción/almacenamiento 0,5 / 1 / 2 %; transferencia 0,3 / 0,5 / 1 %; descarte en selección 0,5 / 1 / 2 % — sin fuente | Incubación | Vigente | DPV-14B-01 |
| SUP-14B-04 | **Tiempos de incubación:** 18 d de incubadora + 3 d de nacedora (21 d), 1 d de limpieza por carga en cada máquina, almacenamiento de huevo 3 / 5 / 7 d (óptimo 3–6 d citado, FTE-14B-001 `[PVDP]`); ovoscopia en la transferencia: no (base) | Incubación | Vigente | DEC-14B-05 |
| SUP-14B-05 | **Margen de capacidad instalada** 10 / **15** / 20 % para incubación y planta de alimento: reserva de diseño, no óptimo | Upstream | Vigente | DEC-14B-01 |
| SUP-14B-06 | **Expedición:** 1–4 nacimientos por semana y 6 / 10 h de ventana para selección, vacunación y carga por nacimiento — barrido operativo, sin fuente | Incubación | Vigente | DPV-14B-10 |
| SUP-14B-07 | **Planta de alimento (escenario):** 5 / 6 días × 8 / 16 h de operación; eficiencia 0,75 / 0,85 (fracción de horas programadas con producción efectiva); factor de pico 1,0 (estacionalidad PENDIENTE) | Alimento | Vigente | DPV-14B-07 |
| SUP-14B-08 | **Categorías de materias primas** (no fórmula): maíz 55–65 %, harina de soja 25–35 %, aceite 1–5 %, minerales 2,3–3,5 %, vitaminas (premezcla) 0,2–0,5 %, otros 0,2–1,3 % (rangos de `03` §4); punto ilustrativo solo para maíz/soja (SUP-032). Recetas reales = nutricionista | Alimento | Vigente | SUP-032, DEC-14B-03 |
| SUP-14B-09 | **Densidades aparentes** (variables): maíz 0,72 t/m³; harina de soja 0,56 / 0,60 / 0,67; alimento terminado 0,55 / 0,60 / 0,65 (barrido, sin dato propio); **factor de llenado 0,90** (FTE-14B-003 `[PVDP]`) | Almacenamiento | Vigente | DPV-14B-04 |
| SUP-14B-10 | **Días de stock** (días calendario de consumo; decisiones de diseño y compra, no datos): maíz 7 / 15 / 30; harina de soja 7 / 15; alimento terminado en planta 1 / 2 / 3; silos de granja 2 / 3 / 5. **No hay volumen unitario de silo** (n.º de silos PENDIENTE) | Almacenamiento | Vigente | DPV-14B-04 |
| SUP-14B-11 | **Reproductoras equivalentes** (opción C, solo fase futura) = pollitos/semana / 3,6 pollitos por reproductora por semana (ESTIMACIÓN de `03` §4.2); sin recría, machos ni reposición | Incubación | Vigente | DPV-045, SUP-034 |
| SUP-14B-12 | **Fases upstream 0 / 1 / 2 / 3 / futura** = arquitectura conceptual de análisis, **no** secuencia recomendada; reproductoras = 0 en Fases 0 y 1 | Estrategia | Vigente | DEC-14B-01, DEC-018, DEC-020 |
| SUP-14B-13 | **Capacidad de camión de grano** 25 / 28 / 30 t: barrido ilustrativo, no capacidad legal ni elegida (sin elección → PENDIENTE) | Logística | Vigente | DPV-084 |

### 1.1 Anotaciones a supuestos existentes

| Registro | Anotación propuesta (sesión 14B, 2026-10-01) |
|---|---|
| SUP-034 (no se asume granja ni incubadora propia) | **Se mantiene.** 14B modela la incubación propia (huevo fértil comprado) solo como alternativa de Fase 3 y las reproductoras solo como fase futura; test U07 garantiza 0 reproductoras en Fases 0 y 1 |
| SUP-032 (reparto por fase y 60 / 30 maíz–soja) | Reutilizado como punto ilustrativo; el resto de categorías se trata como rango (SUP-14B-08) |
| SUP-096 (capacidades de escenario de vehículos) | Reutilizado: granelero 28 t (viajes de alimento) y barrido de pollitos 20 / 40 / 80 mil; sin capacidad de camión de pollitos ni de huevos el resultado es PENDIENTE |

## 2. `datos_por_validar.md`

### 2.1 Nuevos

| ID provisional | Dato | Para qué | Fuente sugerida | Prioridad sugerida (plan de campo) |
|---|---|---|---|---|
| DPV-14B-01 | **Parámetros reales de incubación**: fertilidad e incubabilidad por edad de reproductoras, descarte, pérdidas de recepción y transferencia, efecto de los días de almacenamiento | Reemplazar SUP-14B-02/03 | Incubadoras; manuales de reproductoras (DPV-045) | N3 |
| DPV-14B-02 | **Oferta de huevo fértil para terceros**: quién vende, volumen, calidad, edad de reproductoras, sanidad, contrato | Viabilidad de la opción B de pollito | Incubadoras, empresas de genética, integradoras (pregunta E5 del cuestionario) | N3 |
| DPV-14B-03 | **Fábricas de alimento con capacidad libre**: t/mes disponibles, pellet, **disposición a façon**, lote mínimo por fórmula, entrega en granja, registro SENASA | Opciones A y B de alimento | Fábricas de alimento balanceado (cuestionario pendiente) | N2 |
| DPV-14B-04 | **Densidades aparentes y días de stock reales**; silos de granja (t y m³ por galpón) | Reemplazar SUP-14B-09/10 | Fábricas; productores; fabricantes de silos (sin selección) | N4 |
| DPV-14B-05 | **Proveedores de grano**: volumen anual en el radio, contratos (a término/forward), calidad (humedad, micotoxinas, proteína), estacionalidad, logística | Opciones B y C de alimento | Acopios, cooperativas, corredores, plantas de molienda de soja | N3 (con DPV-117) |
| DPV-14B-06 | **Habilitaciones**: planta de incubación, fábrica de alimentos para animales (inscripción y registro SENASA; medicados), granjas de reproductoras — texto original | Requisitos de las opciones B/C | SENASA; Boletín Oficial | N3 |
| DPV-14B-07 | **Plantas de alimento en operación**: capacidad real en t/h de pellet, eficiencia, turnos, energía y vapor por t, dotación | Reemplazar SUP-14B-07 | Visitas a fábricas; proveedores (sin selección) | N3 |
| DPV-14B-08 | **Integradores existentes**: si ofrecerían pollito, alimento o crianza a un tercero; a qué volumen integraron alimento e incubación | Escala mínima de integración (cualitativa) | Integradoras; cámaras | N3 |
| DPV-14B-09 | **Capacidad de camiones de huevo fértil y de pollitos** y si el transporte está incluido | Viajes de insumos (hoy PENDIENTES) | Incubadoras; transportistas | N4 (amplía DPV-047 / DPV-084) |
| DPV-14B-10 | **Calendario de nacimientos y tamaño de entrega** compatible con el llenado de granjas (lote completo vs escalonado) | Compatibilidad incubadora–granja a escala chica | Incubadoras; productores; integradoras | N2 (con DPV-133) |

### 2.2 Anotaciones a registros existentes

| Registro | Anotación propuesta |
|---|---|
| DPV-006 / DPV-047 (pollito BB) | Demanda por semana plena 13.197 / 26.395 / 52.790 / 105.580 (medio, 5 d) ya en `03`; 14B agrega: **mínimo por entrega** (un lote de granja de 15–60 mil pollitos) puede ser mayor que la demanda semanal a escala chica; preguntar huevo fértil (DPV-14B-02) |
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

### 3.2 Anotaciones a decisiones existentes (siguen **abiertas**)

| Registro | Anotación |
|---|---|
| DEC-020 (abastecimiento de pollo vivo) | 14B muestra que la decisión de granjas arrastra las de pollito y alimento (integrar granjas obliga a proveer insumos). Sin ganador |
| DEC-023 (pollito BB) | Marco A/B/C en `15_incubacion/compra_vs_incubacion.md`; B traslada la dependencia al huevo fértil; C solo fase futura |
| DEC-024 (alimento) | Marco compra / façon / planta propia en `14_alimento_balanceado/compra_vs_fabricacion.md`; capacidad requerida 1–25 t/h |

## 4. `25_fuentes/registro_fuentes.csv`

Agregar las 5 filas de [`fuentes_14B.csv`](fuentes_14B.csv) (FTE-14B-001 a FTE-14B-005), todas `[PVDP]`; FTE-14B-004 y FTE-14B-005 de confiabilidad débil (sectorial/comercial).

## 5. `estado_proyecto.md` — propuesta

**Tablero:** agregar fila "Upstream: alimento e incubación (`14`, `15`) — **MODELO PRELIMINAR COMPLETADO** v1.0 (modelo físico, 11 tests; pollitos, huevos, capacidad de incubación, alimento, planta conceptual, silos desde variables, make-or-buy sin ganador, fases conceptuales). **INTEGRACIÓN = NO DECIDIDA** (DEC-020/023/024 abiertas); sin costos | Pendiente — incubadoras, fábricas, proveedores de grano, integradores | [`conclusiones_alimento.md`](conclusiones_alimento.md), [`conclusiones_incubacion.md`](../15_incubacion/conclusiones_incubacion.md)".

**Hito:** "2026-10-01 · Integración upstream (sesión 14B) · Modelo preliminar completado; sin decisión de integración".

## 6. Plan de trabajo de campo — propuesta

- Ola O4 (producción e incubación): agregar **fábricas de alimento** (3–4) y **proveedores de grano** (2–3) con las preguntas de [`integracion_upstream.md` §5](integracion_upstream.md); crear un cuestionario breve de fábricas de alimento en `14_alimento_balanceado/` al reconciliar (no se creó en esta sesión para no duplicar formatos del plan de campo).
- Añadir a la pregunta E5 del cuestionario de incubadoras: volumen y calidad de huevo fértil, y **mínimo por entrega de pollitos** (lote de granja).

## 7. Tensiones registradas (sin resolver)

| Tensión | Dónde |
|---|---|
| Incubación propia a escala chica vs tamaño de lote de granja (una incubadora de ~13.200 pollitos/semana no llena una granja de 30.000 en un día) | `15_incubacion/capacidad_incubacion.md` §2.3 |
| Planta de alimento propia a escala chica: ~1–2,4 t/h → capacidad mayormente ociosa | `planta_alimento_conceptual.md` §2 |
| Silos: el mínimo por segregación (5–8 celdas) no escala con el volumen | `almacenamiento_silos.md` §3 |
