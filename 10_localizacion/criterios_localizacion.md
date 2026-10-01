# Criterios de localización

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría metodológica final de 12A) · **Sesión:** 12A · Método en [`metodologia_localizacion.md`](metodologia_localizacion.md) · Datos en [`matriz_localizacion.csv`](matriz_localizacion.csv)

> Los criterios describen **qué se mide** y **por qué importa**. No contienen valores: los valores viven solo en la matriz (regla 13). Ningún criterio, solo, define una ubicación.
>
> **Cambios v1.1:** (1) la densidad avícola dejó de ser un criterio "menor es mejor": se separó en **ECOSISTEMA_AVICOLA** y **EXPOSICION_SANITARIA**, con variables distintas, y la densidad de granjas quedó como **trade-off no monotónico**; (2) además de `MAYOR_MEJOR` y `MENOR_MEJOR` existen `NO_MONOTONICO` y `GATE_DURO` / `GATE_CONDICIONAL`; (3) los filtros eliminatorios se separaron en **gates duros** y **condicionales**, aplicables a municipio o terreno; (4) los datos provinciales se dividen en **norma** (rige en todo el territorio) y **agregado estadístico** (no puntúa corredores); (5) la distancia al puerto solo puntúa si el nodo tiene servicio reefer verificado.

---

## 1. Estructura

- **14 grupos ponderables** (los que llevan peso en [`pesos_localizacion.csv`](pesos_localizacion.csv)) y **45 subcriterios monotónicos**; de ellos, 44 puntúan por defecto (ECO-01 es un agregado provincial y no puntúa salvo autorización explícita).
- **Categorías sin peso:** `TRADE_OFF` (3 criterios no monotónicos, análisis cualitativo), `NETWORK` (contacto en Chaco) y `GATE` (se aplican a municipio o terreno). La matriz tiene 13 regiones × 48 subcriterios = 624 celdas, más 2 filas NETWORK.
- **Sentido del criterio** (columna `SENTIDO`):

| Sentido | Significado | Tratamiento en el modelo |
|---|---|---|
| `MAYOR_MEJOR` | Más es mejor dentro de **esa** dimensión | Normalización min-max o rango fijo |
| `MENOR_MEJOR` | Menos es mejor dentro de **esa** dimensión | Ídem, invertida |
| `NO_MONOTONICO` (trade-off) | El mismo valor tiene efectos opuestos o un óptimo intermedio | **Nunca** min-max lineal. Solo `NORMALIZACION = ninguna` (análisis cualitativo) o una función registrada y justificada (hoy no hay ninguna). Si no hay función defendible, el criterio se **divide en componentes monotónicos** |
| `GATE_DURO` / `GATE_CONDICIONAL` | Condición de viabilidad, no de preferencia | No puntúa; se evalúa a nivel municipio o terreno (§4) |

- **Nivel del dato** (`NIVEL_DATO`): `CORREDOR` (medido para el corredor); `PROVINCIA_NORMA` (regla provincial que rige en todo el territorio, p. ej., un límite de vuelco: se aplica a cada corredor de la provincia); `PROVINCIA_AGREGADO` (estadística provincial, p. ej., participación en la faena: **no se usa para puntuar corredores**, porque no distingue entre corredores de la misma provincia).
- **Radios de análisis** (SUP-12A-09): 50 km (mano de obra, IAAP), 100 km (granjas), 150 km (maíz, fábricas de alimento), 200 km (incubadoras, façon), 300 km (mercado regional). Son convenciones para levantar datos, no distancias reglamentarias ni límites de transporte. Para aves vivas, el orden de magnitud del proyecto es ~2–4 h de viaje (~120–250 km `[ESTIMACIÓN]`, [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §4).

## 2. Densidad avícola: dos dimensiones distintas y un trade-off

La concentración de granjas **no es monotónica**: la misma cifra significa cosas opuestas según qué se mire. Por eso no se usa una sola variable para ambas cosas.

| Dimensión | Qué captura | Sentido | Variables (distintas entre sí) |
|---|---|---|---|
| **ECOSISTEMA_AVICOLA** | Disponibilidad de productores, incubadoras, veterinarios, técnicos, mantenimiento, transportistas de aves vivas, proveedores especializados (la experiencia laboral está en RRHH, RRH-02; las fábricas de alimento en ALI-03) | Mayor presencia favorable | ECO-01 (agregado provincial, no puntúa), ECO-02, ECO-03, ECO-04 |
| **EXPOSICION_SANITARIA** | Proximidad entre establecimientos, tránsito avícola, exposición epidemiológica, dificultad de aislamiento, impacto potencial de eventos sanitarios | Mayor exposición desfavorable | SAN-01, SAN-02, SAN-03, SAN-04 |
| **TRADE_OFF** (no puntúa) | La densidad de granjas como tal: es la variable que alimenta a las dos dimensiones a la vez | No monotónica | TOF-01 |

Hoy no hay datos por corredor para ninguna de estas variables: quedan vacías (ECO-01 tiene valores provinciales `[PVDP]` que no puntúan).

## 3. Subcriterios

### 3.1 Monotónicos (puntúan)

| Código | Grupo | Subcriterio | Unidad | Sentido | Nivel | Por qué importa | Fuente sugerida · registro |
|---|---|---|---|---|---|---|---|
| DEM-01 | Demanda | Distancia vial del centro de referencia del corredor a CABA | km | Menor | Corredor | Proxy de costo y tiempo hacia el mayor mercado (AMBA ≈ 30 % del consumo, SUP-024) | Ruteo; 12B · DPV-12A-01 |
| DEM-02 | Demanda | Tiempo de tránsito en camión a CABA | h | Menor | Corredor | La vida útil del fresco se mide en días | Ruteo; transportistas · DPV-12A-01 |
| DEM-03 | Demanda | Distancia media ponderada a locales o CD de la red | km | Menor | Corredor | Solo si la red existe y se conoce su mapa; **no se asume** que compre | Promotor · DPV-018, DPV-036 |
| DEM-04 | Demanda | Población en radio de 300 km | hab | Mayor | Corredor | Mercado regional propio | INDEC · DPV-12A-08 |
| DEM-05 | Demanda | Acceso a mayoristas, gastronomía y elaboradores | 1–5 | Mayor | Corredor | Canales para partes que la red no compra (SUP-013) | Relevamiento comercial · DPV-040 |
| ECO-01 | Ecosistema avícola | Participación provincial en la faena habilitada por SENASA, **año 2024** | % | Mayor | **Provincia — agregado** | Contexto del cluster. **No puntúa corredores** por defecto | SAGyP "Faena Provincial 2024–2025" (FTE-12A-015, confirmado en revisión externa; lectura directa pendiente) |
| ECO-02 | Ecosistema avícola | Productores integrables disponibles | m² de galpón | Mayor | Corredor | Lo que se puede contratar, no lo que existe | Productores, cámaras, municipios · DPV-048 |
| ECO-03 | Ecosistema avícola | Incubadoras que venden pollito BB a terceros en radio de 200 km | n | Mayor | Corredor | Sin pollito no hay crianza | Incubadoras · DPV-047 |
| ECO-04 | Ecosistema avícola | Servicios avícolas especializados (veterinarios y técnicos avícolas, contratistas de captura, transportistas de aves vivas, proveedores y mantenimiento de equipos de galpón) | 1–5 | Mayor | Corredor | El ecosistema que una zona nueva tendría que construir | Productores, proveedores · DPV-12A-11 |
| SAN-01 | Exposición sanitaria | Distancia mediana al establecimiento avícola comercial más cercano | km | **Mayor** | Corredor | Más distancia entre establecimientos = menos exposición y más facilidad de aislamiento | SENASA (RENSPA georreferenciado) · DPV-023 |
| SAN-02 | Exposición sanitaria | Movimientos de tránsito de aves (DT-e) con origen o destino en el departamento o partido | n/año | Menor | Corredor | Tránsito avícola = puente sanitario entre establecimientos | SENASA · DPV-12A-12 |
| SAN-03 | Exposición sanitaria | Eventos de IAAP en aves comerciales en radio de 50 km (2023–2026) | n | Menor | Corredor | Impacto potencial: zonas de control y cierres de exportación | SENASA · DPV-12A-05 |
| SAN-04 | Exposición sanitaria | Lejanía de humedales y concentraciones de aves silvestres (5 = lejos) | 1–5 | Mayor | Corredor | Riesgo de introducción por aves silvestres ([`../03_produccion_primaria/bioseguridad.md`](../03_produccion_primaria/bioseguridad.md)) | INTA, organismos ambientales · DPV-12A-12 |
| CLI-01 | Clima | Días/año con temperatura máxima ≥ 35 °C | d/año | Menor | Corredor | Tecnología de galpón, energía de cooling, mortalidad por calor | SMN · DPV-12A-07 |
| ALI-01 | Alimento | Producción de maíz en radio de 150 km | t/año | Mayor | Corredor | El alimento es el mayor flujo físico del sistema | SAGyP · DPV-12A-02 |
| ALI-02 | Alimento | Distancia a planta de molienda de soja | km | Menor | Corredor | Harina de soja ≈ 30 % de la dieta ilustrativa (SUP-032) | Industria aceitera · DPV-12A-02 |
| ALI-03 | Alimento | Fábricas de alimento balanceado que venden a terceros o a façon en radio de 150 km | n | Mayor | Corredor | Permite no invertir en fábrica propia al inicio (DEC-024) | Fábricas, SENASA · DPV-050 |
| ALI-04 | Alimento | Diferencia de precio del maíz puesto en zona vs pizarra Rosario | USD/t | Menor | Corredor | Maíz más barato en origen lejos del puerto (validar) | BCR, acopios · DPV-050 |
| IND-02 | Faena / industria | Capacidad de faena a façon disponible en radio de 200 km | aves/día | Mayor | Corredor | Habilita una etapa sin planta propia (DEC-004, DEC-018) | Frigoríficos · DPV-006 |
| IND-03 | Faena / industria | Servicios industriales: talleres, frío industrial, repuestos | 1–5 | Mayor | Corredor | Tiempo de reparación = horas de faena perdidas | Proveedores · DPV-089 |
| AGU-01 | Agua | Caudal sostenible típico de perforaciones | m³/h | Mayor | Corredor | Sensibilidad: ~5–42 m³/h medios entre 2.500 y 20.000 aves/día | Perforistas, organismos hídricos · DPV-053 |
| AGU-02 | Agua | Calidad del acuífero (As, F, sales) | 1–5 | Mayor | Corredor | Potabilizar cuesta y genera rechazo (SUP-070) | Laboratorios, INA · DPV-053 |
| AGU-03 | Agua | Claridad y plazo del régimen de permisos de explotación | 1–5 | Mayor | Corredor | Un permiso incierto es un riesgo de calendario | Autoridad hídrica · DPV-106 |
| EFL-01 | Efluentes | Límite de DQO para vuelco a pluvial o cuerpo superficial | mg/L | Mayor | **Provincia — norma** | Mide **costo de tratamiento**; no es un objetivo buscar límites laxos | ADA 336/2003 PBA (FTE-259 `[PVDP]`); resto sin relevar · DPV-067 |
| EFL-02 | Efluentes | Disponibilidad de cuerpo receptor o colectora apta | 1–5 | Mayor | Corredor | Insumo regional del gate de efluentes (§4) | Municipios, autoridad hídrica · DPV-106 |
| EFL-03 | Efluentes | Sensibilidad ambiental del entorno (5 = baja) | 1–5 | Mayor | Corredor | Humedales, delta, ríos recreativos y áreas protegidas elevan exigencias | Organismos ambientales · DPV-106 |
| ENE-01 | Energía | Disponibilidad de potencia en media tensión ampliable | 1–5 | Mayor | Corredor | Potencia media ~0,13–1,04 MW (pico pendiente, DPV-095) | Distribuidoras · DPV-052, DPV-087 |
| ENE-02 | Energía | Acceso a gas natural por red para uso industrial | 1–5 | Mayor | Corredor | Escaldado, limpieza, agua caliente (DEC-045) | Distribuidoras, ENARGAS · DPV-087 |
| ENE-03 | Energía | Duración de interrupciones (SAIDI de la distribuidora) | h/año | Menor | Corredor | Cortes = mortandad en granjas y pérdida de frío (FTE-157 `[PVDP]`) | Entes reguladores · DPV-052 |
| LOG-01 | Logística | Proporción del trayecto a CABA en autopista o autovía | % | Mayor | Corredor | Seguridad, tiempo, previsibilidad | Vialidad, 12B · DPV-12A-01 |
| LOG-02 | Logística | Congestión y restricciones urbanas en accesos (5 = baja) | 1–5 | Mayor | Corredor | Camiones nocturnos de aves vivas, reefers, horarios | Municipios, 12B |
| LOG-03 | Logística | Disponibilidad de transportistas refrigerados (aves vivas: ECO-04) | 1–5 | Mayor | Corredor | Sin contratistas, la flota es propia | Transportistas · DPV-042 |
| EXP-01 | Exportación | Distancia vial al nodo portuario de contenedores de referencia | km | Menor | Corredor | **Solo usable si EXP-04 ≥ 3** (dependencia en el modelo) | Ruteo, 12B · DPV-12A-01 |
| EXP-02 | Exportación | Plantas avícolas exportadoras o traders operando en el corredor | n | Mayor | Corredor | Ecosistema exportador (DPV-081) | SENASA, CEPA · DPV-024 |
| EXP-03 | Exportación | Distancia a oficina SENASA con certificación de exportación | km | Menor | Corredor | Certificación e inspección | SENASA · DPV-101 |
| EXP-04 | Exportación | Servicio reefer verificado en el nodo de referencia (terminal, enchufes, frecuencia, destinos, cut-off) | 1–5 | Mayor | Corredor | Lo que de verdad habilita la salida en contenedor refrigerado | Terminales, navieras · DPV-12A-10 |
| TER-01 | Terreno | Parques o áreas industriales que admiten frigorífico avícola | n | Mayor | Corredor | Uso de suelo resuelto y servicios compartidos | Registro de parques, municipios · DPV-12A-04 |
| TER-02 | Terreno | Precio de tierra apta para planta | USD/ha | Menor | Corredor | **Solo como DPV** hasta tener cotizaciones ([`guia_ramiro.md`](guia_ramiro.md) §6) | `[COTIZACIÓN]` · DPV-087 |
| TER-03 | Terreno | Superficie inundable del partido o departamento | % | Menor | Corredor | Insumo regional del gate de riesgo hídrico | INA · DPV-12A-03 |
| TER-04 | Terreno | Densidad poblacional del partido o departamento | hab/km² | Menor | Corredor | Presión urbana sobre el sitio (la mano de obra se mide aparte, RRH-01) | INDEC · DPV-12A-08 |
| NOR-01 | Normativa | Plazo típico de aptitud o evaluación ambiental | meses | Menor | Corredor | Calendario de habilitación (DPV-086) | Organismos ambientales · DPV-106 |
| NOR-02 | Normativa | Claridad del régimen de uso de suelo industrial | 1–5 | Mayor | Corredor | Previsibilidad, no "facilidad" negociada | Municipios · DPV-106 |
| RRH-01 | RRHH | Población de 18 a 64 años en radio de 50 km | hab | Mayor | Corredor | Base de reclutamiento | INDEC · DPV-12A-06 |
| RRH-02 | RRHH | Experiencia local en industria frigorífica o avícola | 1–5 | Mayor | Corredor | Curva de aprendizaje (DPV-092) | Gremios, plantas · DPV-12A-06 |
| RRH-03 | RRHH | Oferta de técnicos y profesionales | 1–5 | Mayor | Corredor | Mantenimiento, frío, calidad, veterinarios | Escuelas técnicas, universidades · DPV-12A-06 |

### 3.2 No monotónicos (TRADE_OFF: no puntúan; análisis cualitativo)

| Código | Variable | Nivel | Por qué no es monotónica | Cómo se trata |
|---|---|---|---|---|
| TOF-01 | Granjas avícolas comerciales: cantidad en radio de 100 km y densidad | Corredor | Más granjas = más ecosistema **y** más exposición sanitaria | Se describe por corredor; lo puntuable se mide con ECO-xx y SAN-xx |
| TOF-02 | Plantas de faena de aves con habilitación SENASA en la provincia (concentración industrial) | Provincia — agregado | Ecosistema industrial y, a la vez, competencia por personal y productores | Contexto; valores `[PVDP]` de FTE-072 (ER 23, SF 6, Cba 4) |
| TOF-03 | Distancia al borde urbano consolidado más cercano | Corredor | Muy cerca: vecinos, olores, tránsito; muy lejos: sin personal ni servicios | Contexto; sin función de óptimo definida |

Otros candidatos a no monotónicos (no incluidos como fila, documentados): la cercanía a ciertos nodos cuando existen compensaciones (p. ej., estar muy cerca de un cluster ajeno). DEM-01 se mantiene monotónico porque mide **solo** la dimensión de distribución; las compensaciones (granjas, tierra, sanidad) están en otros criterios.

## 4. Gates: duros vs condicionales (nivel municipio / terreno)

Los gates **no se suman** en la matriz y **nunca eliminan una región completa**: se aplican a un municipio o a un terreno concreto. Un terreno descartado no descarta su corredor. Catálogo en `GATES` de [`modelo_localizacion.py`](modelo_localizacion.py); evaluación con `evaluar_gates` (test T23).

| ID | Tipo | Gate | Cuándo es duro / cómo se resuelve si es condicional |
|---|---|---|---|
| G-D1 | **Duro** | Uso de suelo incompatible con frigorífico avícola | Solo si no existe vía legal de cambio (zonificación, excepción) |
| G-D2 | **Duro** | Imposibilidad demostrada de abastecer el agua mínima | Ni pozo, ni red, ni tratamiento técnicamente viable |
| G-D3 | **Duro** | Imposibilidad legal de gestionar efluentes | Ni vuelco, ni reúso, ni retiro autorizado |
| G-D4 | **Duro** | Imposibilidad física de conexión o abastecimiento energético indispensable | Ni red, ni generación propia viable |
| G-C1 | Condicional | Riesgo hídrico | Cota, relleno, drenaje, acceso alternativo |
| G-C2 | Condicional | Vecinos y usos sensibles | Retiros, diseño, barreras, tecnología de tratamiento y de olores |
| G-C3 | Condicional | Receptor de subproductos lejano o inexistente | Tercerización, transporte, proceso propio |
| G-C4 | Condicional | Falta inicial de gas natural | GLP, electricidad, biomasa |
| G-C5 | Condicional | Potencia limitada pero ampliable | Obra de la distribuidora, generación, crecimiento por etapas |
| G-C6 | Condicional | Agua con calidad que requiere tratamiento | Potabilización (costo, rechazo) |
| G-C7 | Condicional | Acceso no pavimentado o restringido | Obra vial, acceso alternativo |

Reglas:

1. Un gate duro solo descarta un terreno con **imposibilidad demostrada por escrito** (factibilidad negativa, norma, dictamen). Una afirmación verbal o un `[PVDP]` deja el terreno **CONDICIONADO**, no descartado.
2. Un gate condicional nunca descarta: marca el terreno como **CONDICIONADO** (requiere inversión, mitigación, tercerización o cambio de diseño, que se evaluarán con CAPEX/OPEX en su momento).
3. Un condicional pasa a duro solo si la mitigación se demuestra inviable.
4. Los umbrales concretos (caudal mínimo, potencia, distancia a viviendas) quedan **sin definir** (DEC-12A-03): dependen de la escala y de la normativa del sitio.

Regla de la ruta crítica ([`../16_normativa_senasa/ruta_critica_habilitacion.md`](../16_normativa_senasa/ruta_critica_habilitacion.md)): **no comprar ni comprometer un terreno sin verificar uso de suelo, agua y vuelco por escrito.**

## 5. Correlaciones declaradas (riesgo de doble conteo)

| Par | Relación | Cómo tratarla |
|---|---|---|
| DEM-01 / EXP-01 | Buenos Aires y Dock Sud son nodos logísticos de referencia y están en el AMBA: si el nodo de referencia es uno de ellos, ambas distancias son casi la misma | Revisar el peso conjunto de DEMANDA y EXPORTACION; comparar otros nodos (Zárate, Gran Rosario, Concepción del Uruguay) cuando EXP-04 esté verificado |
| ECO-xx / SAN-xx | Ambas dimensiones se correlacionan con la densidad de granjas (TOF-01), pero se miden con variables distintas | Mantener ambas: es el trade-off central de una zona avícola fuerte (§2) |
| ECO-04 / RRH-02 | Servicios avícolas vs experiencia laboral local | ECO-04 excluye la experiencia laboral para no duplicar |
| ECO-01 / TOF-02 / EXP-02 | Todas miden el tamaño del cluster | ECO-01 y TOF-02 no puntúan; solo EXP-02 (por corredor) |
| DEM-01 / TER-04 / LOG-02 | Cerca del AMBA = más presión urbana y más congestión | Trade-off documentado en [`escenarios_localizacion.md`](escenarios_localizacion.md) §1 |
| ALI-01 / ALI-04 | Más maíz cerca suele implicar menor precio en origen | Si hay precios reales, ALI-04 puede reemplazar a ALI-01 |

## 6. Rúbricas de las escalas 1–5

Una celda 1–5 solo se completa con evidencia citada en `OBSERVACIONES`. **Sin evidencia la celda queda vacía**; nunca se pone "3" por defecto.

| Subcriterio | 1 | 3 | 5 |
|---|---|---|---|
| DEM-05 Mayoristas, gastronomía, elaboradores | Sin compradores identificados en 300 km | Algunos identificados, sin contacto | Contactados con interés documentado (E3+ de la escala comercial) |
| ECO-04 Servicios avícolas especializados | Veterinarios, contratistas y proveedores a > 1 día | Algunos servicios en la provincia | Veterinarios avícolas, contratistas de captura, transportistas de aves vivas y proveedores de equipos en el corredor |
| SAN-04 Lejanía de humedales y aves silvestres | Humedal o concentración de aves silvestres en el corredor | A distancia intermedia, sin registro de concentraciones | Sin humedales ni concentraciones conocidas en el radio |
| IND-03 Servicios industriales | Repuestos y técnicos a > 1 día | Talleres generales; frío industrial a pocas horas | Frío, refrigeración y equipos con técnicos residentes |
| AGU-02 Calidad del acuífero | No apta sin tratamiento complejo (p. ej., As alto) | Apta con tratamiento convencional | Apta sin tratamiento, con análisis |
| AGU-03 / NOR-02 Permisos / uso de suelo | Norma inexistente o contradictoria | Norma clara, plazo desconocido | Norma clara con plazo y requisitos publicados |
| EFL-02 Cuerpo receptor | Ninguno practicable | Disponible con obra o restricciones | Colectora o cuerpo receptor con capacidad declarada |
| EFL-03 Sensibilidad ambiental | Humedal, área protegida o curso recreativo cercano | Curso sin uso sensible conocido | Entorno rural sin cuerpos sensibles |
| ENE-01 Potencia en MT | Sin red de MT cercana | Red de MT con ampliación necesaria | Potencia disponible por escrito con margen |
| ENE-02 Gas natural | Sin red; solo GLP | Red a distancia con obra | Red con factibilidad de caudal industrial |
| LOG-02 Congestión | Accesos congestionados y restricciones horarias | Paso por localidades sin restricción | Acceso directo a ruta sin cruzar áreas urbanas |
| LOG-03 Transportistas refrigerados | Sin oferta local | Oferta a distancia | Varias empresas locales |
| EXP-04 Servicio reefer del nodo | Sin terminal de contenedores o sin enchufes reefer | **Servicio reefer regular verificado** (umbral de uso de EXP-01) a pocos destinos | Servicio regular a múltiples destinos, capacidad de enchufes y cut-off documentados |
| RRH-02 / RRH-03 Experiencia y técnicos | Sin antecedentes industriales | Industria alimentaria no cárnica | Frigoríficos avícolas, escuelas técnicas y universidad cercanos |

## 7. Bioseguridad y localización (análisis conceptual)

Base técnica en [`../03_produccion_primaria/bioseguridad.md`](../03_produccion_primaria/bioseguridad.md) y [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md). **No se usan distancias reglamentarias**: la distancia de 1.000 m entre granjas aparece solo en extractos de la Res. SENASA 1699/2019 y no se usa hasta verificar alcance, excepciones y forma de medición (DPV-046).

| Factor | Cómo lo afecta la localización | Lado ECOSISTEMA (favorable) | Lado EXPOSICIÓN (desfavorable) |
|---|---|---|---|
| **Concentración de granjas** | Cuántos productores hay y cuán cerca están unos de otros | Productores, contratistas, técnicos, veterinarios (ECO-02, ECO-04) | Un brote se propaga más fácil; menor distancia entre establecimientos (SAN-01) |
| **Distancia planta–granja** | Horas de viaje, DOA, merma de ayuno, bienestar | Granjas cerca de la planta | Granjas de terceros intercaladas con las propias |
| **Tránsito de aves y vehículos** | Camiones, cajones y cuadrillas son el principal puente sanitario | Logística de captura establecida | Más movimientos (SAN-02) y rutas compartidas |
| **Planta como nodo** | La planta concentra camiones de todas las granjas | Servicios de lavado y desinfección conocidos | Dentro del cluster, su tránsito pasa cerca de granjas de terceros |
| **Riesgo sanitario de exportación** | Una zona de control por IAAP puede suspender certificaciones (regionalización reconocida solo por algunos destinos, FTE-097 `[PVDP]`) | Experiencia de organismos y sector en manejo de brotes | Más probabilidad de quedar dentro de una zona afectada (SAN-03) |
| **Expansión** | Crecer exige granjas nuevas a distancia sanitaria | Productores dispuestos a ampliar | Tierra apta para granjas nuevas escasa y competida |
| **Compartimentación futura** | Un compartimento reconocido (Res. 484/2017 `[PVDP]`) es independiente de la geografía | — | La compra spot de pollo vivo es incompatible con compartimentación (DEC-025) |

**Lectura:** una zona de baja densidad ofrece mejor exposición sanitaria **inicial** pero obliga a construir el ecosistema y no garantiza baja densidad futura si el propio proyecto crece; una zona de alta densidad ofrece ecosistema inmediato a cambio de mayor exposición. Ninguna es mejor en abstracto: depende del modelo de abastecimiento (DEC-020), de la vocación exportadora (DEC-011), del nivel de bioseguridad objetivo (DEC-025) y de los pesos que los socios asignen a ECOSISTEMA_AVICOLA y EXPOSICION_SANITARIA (DEC-12A-02).

## 8. Exportación: cuatro cosas distintas

**Cercanía a puerto ≠ disponibilidad reefer ≠ servicio marítimo adecuado ≠ exportación habilitada.**

1. **Cercanía a puerto:** km y horas al nodo (EXP-01). Reduce un costo.
2. **Disponibilidad reefer:** terminal de contenedores con enchufes y capacidad reefer (EXP-04).
3. **Servicio marítimo adecuado:** frecuencia, destinos, cut-off y costos del servicio (EXP-04, DPV-12A-10).
4. **Exportación habilitada:** país abierto (categoría A, regla 17), planta habilitada y listada, producto autorizado, comprador con contrato, volumen y congelado ([`../16_normativa_senasa/exportacion_y_certificaciones.md`](../16_normativa_senasa/exportacion_y_certificaciones.md), [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md)). **Ninguna localización la otorga.**

Buenos Aires / Dock Sud son **nodos logísticos de referencia** para contenedores (FTE-134 `[PVDP]`) y deben compararse con otras alternativas portuarias (Zárate, Gran Rosario, Concepción del Uruguay u otras) cuando se releve cada nodo; no se afirma que sean los únicos nodos reefer porque no hay un inventario nacional de terminales reefer verificado. El modelo **no da puntaje exportador por kilómetros**: EXP-01 solo es usable si el nodo tiene EXP-04 ≥ 3 (test T27).

## 9. Criterios que existen solo a nivel de terreno

Se relevan con la [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md): superficie y forma, cota y drenaje, vecinos inmediatos y vientos, accesos separados, dominio, napa, contaminación previa, servicios en el lindero, precio cotizado, linderos para expansión. Requisitos en [`terreno_ideal.md`](terreno_ideal.md).

## 10. Factor cualitativo NO puntuable: network / acceso

El contacto familiar, político o social del promotor en Chaco (SUP-014) figura en la matriz como fila **NETWORK** (NET-01) solo en CH-ESTE y CH-CENTRO, **separada de los criterios físicos**: ventaja cualitativa de acceso a información e interlocutores. No es beneficio económico, facilidad regulatoria, reducción de plazos ni recomendación de ubicación, y tiene **peso cero** en todos los perfiles (el modelo rechaza un peso > 0; tests T08 y T28). Tratamiento en [`regiones_preliminares.md`](regiones_preliminares.md) §6.
