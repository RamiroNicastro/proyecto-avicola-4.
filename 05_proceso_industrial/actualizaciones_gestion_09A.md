# Actualizaciones de gestión pendientes de reconciliación — sesión 09A (proceso industrial y maquinaria)

**Fecha:** 2026-09-30 · Sesión ejecutada **en paralelo** con otras sesiones.

> **Por qué existe este archivo:** por instrucción del promotor, esta sesión **no modificó** `00_gestion_proyecto/` ni `25_fuentes/registro_fuentes.csv` / `25_fuentes/bibliografia.md`. Todo lo que normalmente se registraría allí está aquí para la **reconciliación central**. Los IDs son **provisionales** (`SUP-09A-##`, `DPV-09A-##`, `DEC-09A-##`, `FTE-09A-###`) para evitar colisiones con otras sesiones; al reconciliar se reasignan al siguiente número libre y se reemplazan en los archivos de `05_proceso_industrial/` y `08_maquinaria/` (búsqueda de texto de cada ID provisional).
> Últimos IDs vistos en los registros centrales al iniciar la sesión: SUP-060, DPV-087, DEC-036, FTE-193.

---

## 1. Supuestos nuevos → `00_gestion_proyecto/supuestos.md`

| ID provisional | Supuesto | Ámbito | Responsable | Fecha | Estado |
|---|---|---|---|---|---|
| SUP-09A-01 | **Eficiencia global de línea** η = producción real / (ritmo nominal × horas netas) de **0,70 / 0,80 / 0,90** como sensibilidad; agrupa disponibilidad, microparadas, pérdidas de velocidad y reprocesos. No es dato de ningún equipo ni de plantas argentinas | Proceso industrial / maquinaria | Analista | 2026-09-30 | Vigente (sensibilidad) |
| SUP-09A-02 | **Ventana no productiva diaria** (h) baja / media / alta: preoperativo 0,5 / 0,75 / 1,0; pausas 0,5 / 0,75 / 1,0 y limpieza intermedia 0,25 / 0,33 / 0,5 por cada 8 h netas; cierre y vaciado 0,5 / 0,75 / 1,0; **sanitización final 3 / 4 / 6**; mantenimiento no solapado 0,5 / 1 / 2. Independiente de la escala (simplificación) | Proceso industrial | Analista | 2026-09-30 | Vigente (sensibilidad) |
| SUP-09A-03 | **Productividades manuales de referencia** `[PVDP · débil]`: colgado 23 aves/min por operario (líneas de EE.UU. de alta velocidad, FTE-09A-026); eviscerado manual 2 aves/min por operario (FAO, FTE-09A-025); variante **prudente** = 50 %. Se usan solo para "puestos equivalentes"; **no son dotación** | Proceso industrial / RR. HH. | Analista | 2026-09-30 | Vigente |
| SUP-09A-04 | **Tiempo de residencia en el enfriamiento**: inmersión 50 min; aire 90–150 min (FTE-09A-024 `[PVDP]`). Coherente con SUP-042 (absorción 6 %, evaporación 1,8 %), que no cambia | Proceso industrial | Analista | 2026-09-30 | Vigente |
| SUP-09A-05 | **Lista conceptual de equipos, niveles de automatización por escala y criticidad** (CRÍTICO / IMPORTANTE / SECUNDARIO) de [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv) como hipótesis de trabajo basada en conocimiento técnico general, a validar con proveedores (RFQ) y plantas en operación | Maquinaria | Analista | 2026-09-30 | Vigente |

**Notas a supuestos existentes:**

- **SUP-052** (definición de capacidad): agregar "2026-09-30 (09A): capacidad nominal requerida = ritmo operativo ÷ η (SUP-09A-01); capacidad de planta = mínimo de las etapas (`05_proceso_industrial/cuellos_botella.md` §1)".
- **SUP-053** (horas netas 6/8/10/16): agregar "2026-09-30 (09A): 16 h netas + ventana no productiva = 22–29 h/día (SUP-09A-02): con tiempos medios o altos no entran en 24 h".
- **SUP-042** (enfriamiento): sin cambio; tiempos de residencia en SUP-09A-04.

## 2. Datos por validar nuevos → `00_gestion_proyecto/datos_por_validar.md`

| ID provisional | Dato | Por qué importa | Dónde buscar | Prioridad |
|---|---|---|---|---|
| DPV-09A-01 | **Capacidad real vs nominal** de líneas avícolas en operación (aves/h reales sostenidas, disponibilidad, microparadas), por proveedor y rango de ritmo, preferentemente en plantas argentinas | Define el ritmo nominal a especificar (η) y la capacidad real de cada escala | Visitas a plantas; referencias de proveedores (RFQ campo 2 y 25) | Importante antes de invertir |
| DPV-09A-02 | **Presencia verificada y servicio técnico local** de cada proveedor en Argentina: filial o representante, técnicos residentes, stock de repuestos, tiempos de respuesta; qué equipos y proveedores usan las ~60 plantas habilitadas | Riesgo de parada de equipos críticos; dependencia de proveedor | Consultas directas; visitas; Avícola y Porcinos 2026 (Buenos Aires, 6–8 nov 2026) | Importante antes de invertir |
| DPV-09A-03 | **Requisitos normativos de faena de aves** en el texto original del Decreto 4238/68 (capítulo de aves) y Res. SENASA 592/2026: puestos/inspectores por velocidad de línea, iluminación, temperaturas de chiller, salas y producto, separación de zonas y de subproductos | Fija cuellos de botella regulatorios (inspección) y parámetros de diseño | Texto original (SENASA, InfoLeg); consulta al servicio oficial | Crítico antes de diseñar (complementa DPV-007) |
| DPV-09A-04 | **Tiempo real de limpieza y sanitización** y de mantenimiento diario en plantas argentinas, por escala; organización de turnos de sanitización | Ventana horaria y factibilidad del segundo turno | Visitas; proveedores de químicos; convenio (DPV-082) | Importante |
| DPV-09A-05 | **Productividad de operarios argentinos**: colgado (aves/min), eviscerado manual (aves/h), trozado y deshuese manual (kg/h), rotación de puestos | Puestos equivalentes, umbral de automatización | Visitas; `18_recursos_humanos`; ensayo en planta (DEC-028) | Importante |
| DPV-09A-06 | **Método de enfriamiento** usual y admitido en Argentina; temperaturas objetivo; parámetros de inmersión (renovación de agua, temperatura) | Elección de enfriamiento (DEC-026) | Decreto 4238/68 original (extracto de aire en FTE-09A-030); plantas | Importante (complementa DPV-061) |
| DPV-09A-07 | **Régimen de importación de bienes usados** en Argentina (requisitos, certificaciones, aranceles) y disponibilidad real de líneas usadas/reacondicionadas | Viabilidad de la opción usada/reacondicionada | Normativa aduanera; despachantes; revendedores | Útil para optimizar |
| DPV-09A-08 | **Métodos de aturdido** admitidos por SENASA y por destinos (UE, Halal); experiencia de CAS en Argentina | DEC-09A-05 | Decreto 4238/68; destinos (complementa DPV-034) | Importante antes de diseñar |
| DPV-09A-09 | **Consumos de servicios por equipo** (kW, agua, vapor, aire, frío, efluente) | Dimensionamiento de servicios (`11_agua_efluentes`, `12_energia_frio`) | RFQ campos 5–10 | Importante antes de invertir |
| DPV-09A-10 | **Tiempo de congelado** hasta −18 °C por producto y envase y capacidad (kg/h) por tipo de congelador | Dimensionar congelado y cámaras según perfil P1–P3 | RFQ lote L8; `12_energia_frio` | Importante |

**Notas a datos existentes:**

- **DPV-082** (horas netas y turnos): agregar "09A: la factibilidad del segundo turno depende también de la ventana de sanitización y mantenimiento (DPV-09A-04; `cuellos_botella.md` §4)".
- **DPV-083** (escala mínima eficiente): agregar "09A: arquitecturas por escala en `arquitecturas_por_escala.md`; el salto de automatización de la evisceración (~1.000 aves/h, FTE-09A-025) cae entre 5.000 y 10.000 aves/día a 8 h netas; no se concluye escala mínima".
- **DPV-086** (plazos): agregar "09A: lead time de equipos se pedirá en RFQ (campo 20)".
- **DPV-007** (normativa): vincular con DPV-09A-03 y DPV-09A-08.
- **DPV-034** (Halal): vincular con DPV-09A-08.
- **DPV-009** (verificación documental): una sesión más con acceso directo bloqueado (WebFetch `EGRESS_BLOCKED` en meyn.com; curl 403 en marel.com y meyn.com); WebSearch sí funcionó.

## 3. Decisiones pendientes nuevas → `00_gestion_proyecto/decisiones_pendientes.md`

| ID provisional | Decisión | Prioridad | Depende de | Carpeta | Nota |
|---|---|---|---|---|---|
| DEC-09A-01 | Definir el **nivel de automatización por operación** (manual / semiautomático / automático) para la escala o etapa elegida | Media | DEC-001, DEC-005, DPV-09A-02, DPV-09A-05, `18_recursos_humanos`, `19_capex`, `20_opex` | `08_maquinaria` | Matriz sin decisión en `automatizacion_por_escala.md`; no se presume que más automatización sea mejor |
| DEC-09A-02 | Definir la **configuración de líneas**: una línea rápida, dos líneas, o línea ampliable (y su ritmo nominal) | Media | DEC-001, DEC-033, DEC-035, DEC-036, DPV-09A-01 | `05_proceso_industrial` | Comparación conceptual en `arquitecturas_por_escala.md` §8.2 |
| DEC-09A-03 | Definir la política de **equipos nuevos / usados / reacondicionados** (por grupo de equipos) | Media | DPV-09A-07, DPV-09A-02, `19_capex` | `08_maquinaria` | `proveedores_preliminares.md` §4 |
| DEC-09A-04 | Definir la **estrategia de redundancia, repuestos críticos y contrato de servicio** | Media | DEC-09A-01, DPV-09A-02 | `08_maquinaria` | `catalogo_equipos.md` §2 |
| DEC-09A-05 | Definir el **método de aturdido** a estudiar (eléctrico en baño de agua, CAS) | Media | DPV-09A-08, DPV-034, DEC-012 | `05_proceso_industrial` / `16_normativa_senasa` | `catalogo_equipos.md` §1.2 |

**Notas a decisiones existentes:**

- **DEC-004** (faena propia o a façon): agregar "09A: la faena a façon también sirve para medir capacidad real, cuellos de botella y productividad antes de especificar equipos (DPV-09A-01, DPV-09A-05)".
- **DEC-026** (método de enfriamiento): agregar "09A: comparación inmersión / aire / mixto en `08_maquinaria/catalogo_equipos.md` §1.4; carcasas simultáneas en `cuellos_botella.md` §5".
- **DEC-036** (organización horaria): agregar "09A: con la ventana de sensibilidad (SUP-09A-02), 16 h netas requieren 22–29 h/día; el segundo turno no se asume sin resolver sanitización y mantenimiento (`cuellos_botella.md` §4 y §7)".
- **DEC-012** (estándar UE / Halal): agregar "09A: zonificación conceptual en `05_proceso_industrial/zonificacion_higienica.md`".
- **DEC-035** (sobredimensionar vs módulos): agregar "09A: acción por equipo (mantener / duplicar / ampliar / reemplazar) en `matriz_equipos.csv` y `arquitecturas_por_escala.md` §8".

## 4. Glosario → `00_gestion_proyecto/glosario.md`

| Término | Definición propuesta |
|---|---|
| **Aves/h (bph, *birds per hour*)** | Aves que pasan por la línea en una hora de funcionamiento |
| **Velocidad nominal / operativa** | Nominal: la especificada para el equipo sin interrupciones; operativa: la real mientras la línea funciona |
| **Disponibilidad** | Fracción de las horas netas programadas en que la línea está en marcha |
| **Microparada** | Interrupción de segundos a pocos minutos que no se registra como parada |
| **Eficiencia global (η; análoga a OEE, *overall equipment effectiveness*)** | Producción real / (velocidad nominal × horas netas) |
| **Cuello de botella** | Etapa de menor capacidad; fija la capacidad de la planta |
| **Grillete (*shackle*)** | Gancho del transportador aéreo del que cuelgan las aves |
| **Línea de faena (*kill line*) / línea de evisceración** | Tramo del transportador desde colgado hasta desplumado / desde la transferencia hasta el enfriamiento |
| **Transferencia (recolgado, *rehang*)** | Paso de la carcasa de la línea de faena a la de evisceración; límite higiénico sucia/evisceración |
| **CAS (*controlled atmosphere stunning*)** | Aturdido por atmósfera controlada (gases) antes del colgado |
| **Chiller por inmersión / *air chilling*** | Enfriamiento de carcasas en agua helada / en aire frío forzado |
| **IQF (*individually quick frozen*)** | Congelado individual rápido de piezas |
| **MAP (*modified atmosphere packaging*)** | Envase con atmósfera modificada |
| **Termoformado / *skin pack*** | Envase formado en línea a partir de film; film que se adhiere al producto |
| **Bypass** | Forma alternativa (generalmente manual) de seguir operando si falla un equipo |
| **N+1** | Una unidad adicional a las necesarias, como reserva |
| **RFQ (*request for quotation*)** | Solicitud formal de cotización |
| **Incoterm** | Regla de comercio internacional que define entrega, costos y riesgos (EXW, FOB, CIF, DAP, DDP) |
| **Lead time** | Plazo desde el pedido hasta el equipo instalado |
| **FAT / SAT** | Pruebas de aceptación en fábrica / en sitio |
| **Ventana horaria del establecimiento** | Horas netas de faena + preoperativo + pausas + limpieza intermedia + cierre + sanitización + mantenimiento |

## 5. Estado del proyecto → `00_gestion_proyecto/estado_proyecto.md`

Propuesta de entrada: "2026-09-30 — **Modelo conceptual del proceso industrial y equipamiento por escala (sesión 09A)**: flujo de proceso con flujos laterales, zonificación higiénica, capacidad horaria y ventana del establecimiento, cuellos de botella, 76 equipos conceptuales con automatización por escala y criticidad, proveedores preliminares (todos `[PVDP]`), nuevo vs usado, RFQ futuro y guía. Modelo `05_proceso_industrial/modelo_capacidad_proceso.py` (13/13 tests; 5/5 mutaciones). Sin escala, proveedor, CAPEX, layout ni localización. Evaluación: MEDIA como método; BAJA como evidencia de capacidad real."

## 6. Fuentes nuevas → `25_fuentes/registro_fuentes.csv` y `bibliografia.md`

36 fuentes con IDs provisionales **FTE-09A-001 a FTE-09A-036** en [`../08_maquinaria/fuentes_09A.csv`](../08_maquinaria/fuentes_09A.csv), con el mismo esquema de columnas que el registro central. Todas `PENDIENTE DE VERIFICACIÓN DOCUMENTAL PRIMARIA` (extractos de buscador). Categorías: fabricantes (Meyn, JBT Marel, BAADER/Linco, Foodmate, Prime, Mayekawa, Bayle, ULMA, Multivac, GEA/JBT Frigoscandia), fabricantes argentinos (Ing. Galimberti, Rosarossa, Rovi), chinos (Raniche, Xinbaiyun/Eruis, Henger), revendedores de usados (Drobtech, Use Poultry Tech, Isotek), técnicas (FAO, INTA, Decreto 4238/68 extracto, SENASA, INTI) y comerciales débiles. FTE-09A-030 complementa FTE-016 y FTE-192 (mismo decreto): al reconciliar, decidir si se fusiona como nueva fila o como anotación de FTE-016.

## 7. Archivos de otros módulos

No se modificó ningún archivo fuera de `05_proceso_industrial/` y `08_maquinaria/`. Los modelos anteriores (`03`, `04`, `07`, `23`) se **importan** sin cambios (test T08 de `modelo_capacidad_proceso.py`).
