# Criterios de localización

**Fecha:** 2026-10-01 · **Versión:** 1.0 · **Sesión:** 12A · Método en [`metodologia_localizacion.md`](metodologia_localizacion.md) · Datos en [`matriz_localizacion.csv`](matriz_localizacion.csv)

> Los criterios describen **qué se mide** y **por qué importa**. No contienen valores: los valores viven solo en la matriz (regla 13). Ningún criterio, solo, define una ubicación.

---

## 1. Estructura

- **12 grupos** (los que llevan peso en [`pesos_localizacion.csv`](pesos_localizacion.csv)) y **43 subcriterios** regionales (los que tienen valor por corredor).
- **Sentido:** `MAYOR_MEJOR` o `MENOR_MEJOR` (el modelo invierte los segundos).
- **Nivel del dato:** `CORREDOR` (se mide para el corredor) o `PROVINCIA` (dato provincial usado como proxy; no discrimina dentro de la provincia).
- **Radios de análisis** (SUP-12A-09): 50 km (mano de obra, IAAP), 100 km (granjas), 150 km (maíz, fábricas de alimento), 200 km (incubadoras, façon), 300 km (mercado regional). Son **convenciones para levantar datos de forma homogénea**, no distancias reglamentarias ni límites de transporte. Para aves vivas, el orden de magnitud del proyecto es ~2–4 h de viaje (~120–250 km `[ESTIMACIÓN]`, [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §4).

## 2. Subcriterios regionales

| Código | Grupo | Subcriterio | Unidad | Sentido | Nivel | Por qué importa | Fuente sugerida · registro |
|---|---|---|---|---|---|---|---|
| DEM-01 | Demanda | Distancia vial del centro de referencia del corredor a CABA | km | Menor | Corredor | Proxy del costo y tiempo de llevar producto al mayor mercado (AMBA ≈ 30 % del consumo, SUP-024) | Ruteo; 12B · DPV-12A-01 |
| DEM-02 | Demanda | Tiempo de tránsito en camión a CABA | h | Menor | Corredor | La vida útil del fresco se mide en días; el tiempo pesa más que los km | Ruteo; transportistas · DPV-12A-01 |
| DEM-03 | Demanda | Distancia media ponderada a locales o CD de la red | km | Menor | Corredor | Solo si la red existe y se conoce su mapa; **no se asume** que compre | Promotor · DPV-018, DPV-036 |
| DEM-04 | Demanda | Población en radio de 300 km | hab | Mayor | Corredor | Mercado regional propio, independiente de la red | INDEC Censo 2022 por partido · DPV-12A-08 |
| DEM-05 | Demanda | Acceso a mayoristas, gastronomía y elaboradores | 1–5 | Mayor | Corredor | Canales para partes que la red no compra (ingreso total por ave, SUP-013) | Relevamiento comercial · DPV-040 |
| PRI-01 | Producción primaria | Participación de la provincia en la faena SENASA | % | Mayor | Provincia | Proxy de tradición avícola y de ecosistema de servicios | SAGyP Anuario (FTE-001 `[PVDP]`) · DPV-009 |
| PRI-02 | Producción primaria | Granjas de parrilleros habilitadas en radio de 100 km | n | Mayor | Corredor | Base de integración o compra de pollo vivo | SENASA (RENSPA), SAGyP · DPV-023 |
| PRI-03 | Producción primaria | Productores integrables disponibles | m² de galpón | Mayor | Corredor | Lo que de verdad se puede contratar, no lo que existe | Productores, cámaras, municipios · DPV-048 |
| PRI-04 | Producción primaria | Incubadoras que venden pollito BB a terceros en radio de 200 km | n | Mayor | Corredor | Sin pollito no hay crianza; hoy concentrado en pocos actores | Incubadoras · DPV-047 |
| PRI-05 | Producción primaria | Densidad de granjas avícolas comerciales | granjas/1.000 km² | **Menor** | Corredor | Presión sanitaria (§6). Es la otra cara de PRI-02 | SENASA, SAGyP · DPV-023 |
| PRI-06 | Producción primaria | Eventos de IAAP en aves comerciales en radio de 50 km (2023–2026) | n | Menor | Corredor | Riesgo de zonas de control y cierres de exportación | SENASA (comunicados georreferenciados) · DPV-12A-05 |
| PRI-07 | Producción primaria | Días/año con temperatura máxima ≥ 35 °C | d/año | Menor | Corredor | Tecnología de galpón, energía de cooling, mortalidad por calor | SMN · DPV-12A-07 |
| ALI-01 | Alimento | Producción de maíz en radio de 150 km | t/año | Mayor | Corredor | El alimento es el mayor flujo físico del sistema ([`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §12) | SAGyP estimaciones agrícolas · DPV-12A-02 |
| ALI-02 | Alimento | Distancia a planta de molienda de soja | km | Menor | Corredor | Harina de soja ≈ 30 % de la dieta ilustrativa (SUP-032) | Cámaras de la industria aceitera · DPV-12A-02 |
| ALI-03 | Alimento | Fábricas de alimento balanceado que venden a terceros o a façon en radio de 150 km | n | Mayor | Corredor | Permite no invertir en fábrica propia al inicio (DEC-024) | Fábricas, SENASA · DPV-050 |
| ALI-04 | Alimento | Diferencia de precio del maíz puesto en zona vs pizarra Rosario | USD/t | Menor | Corredor | Zonas lejos del puerto suelen tener maíz más barato en origen; validar | BCR, acopios · DPV-050 |
| IND-01 | Faena / industria | Plantas de faena de aves con habilitación SENASA en la provincia | n | Mayor | Provincia | Ecosistema industrial (y también competencia por personal) | FTE-072 `[PVDP]`, SENASA · DPV-023 |
| IND-02 | Faena / industria | Capacidad de faena a façon disponible en radio de 200 km | aves/día | Mayor | Corredor | Habilita una etapa sin planta propia (DEC-004, DEC-018) | Frigoríficos · DPV-006 |
| IND-03 | Faena / industria | Servicios industriales: talleres, frío industrial, repuestos | 1–5 | Mayor | Corredor | Tiempo de reparación = horas de faena perdidas | Proveedores · DPV-089 |
| AGU-01 | Agua | Caudal sostenible típico de perforaciones | m³/h | Mayor | Corredor | Referencia de sensibilidad: ~5–42 m³/h medios entre 2.500 y 20.000 aves/día (DPV-053) | Perforistas, organismos hídricos · DPV-053 |
| AGU-02 | Agua | Calidad del acuífero (As, F, sales) | 1–5 | Mayor | Corredor | Potabilizar cuesta y genera rechazo (agua captada > utilizada, SUP-070) | Laboratorios, INA, organismos provinciales · DPV-053 |
| AGU-03 | Agua | Claridad y plazo del régimen de permisos de explotación | 1–5 | Mayor | Provincia | Un permiso incierto es un riesgo de calendario | Autoridad hídrica provincial · DPV-106 |
| EFL-01 | Efluentes | Límite de DQO para vuelco a pluvial o cuerpo superficial | mg/L | Mayor | Provincia | Mide **costo de tratamiento**; no es un objetivo buscar límites laxos (la planta debe cumplir y prever el estándar más exigente) | ADA 336/2003 PBA (FTE-259 `[PVDP]`); otras provincias sin relevar · DPV-067 |
| EFL-02 | Efluentes | Disponibilidad de cuerpo receptor o colectora apta | 1–5 | Mayor | Corredor | Sin vuelco no hay planta (también es filtro eliminatorio en terreno, §4) | Municipios, autoridad hídrica · DPV-106 |
| EFL-03 | Efluentes | Sensibilidad ambiental del entorno | 1–5 (5 = baja) | Mayor | Corredor | Humedales, delta, ríos recreativos y áreas protegidas elevan exigencias y conflictos | Organismos ambientales · DPV-106 |
| ENE-01 | Energía | Disponibilidad de potencia en media tensión ampliable | 1–5 | Mayor | Corredor | Potencia media de proceso ~0,13–1,04 MW (pico pendiente, DPV-095) | Distribuidoras · DPV-052, DPV-087 |
| ENE-02 | Energía | Acceso a gas natural por red para uso industrial | 1–5 | Mayor | Corredor | Escaldado, limpieza y agua caliente; alternativa GLP más cara (DEC-045) | Distribuidoras de gas, ENARGAS · DPV-087 |
| ENE-03 | Energía | Duración de interrupciones (SAIDI de la distribuidora) | h/año | Menor | Corredor | Cortes = mortandad en granjas y pérdida de frío en planta (FTE-157 `[PVDP]`) | Entes reguladores · DPV-052 |
| LOG-01 | Logística | Proporción del trayecto a CABA en autopista o autovía | % | Mayor | Corredor | Seguridad, tiempo y previsibilidad del refrigerado | Vialidad Nacional, 12B · DPV-12A-01 |
| LOG-02 | Logística | Congestión y restricciones urbanas en accesos | 1–5 (5 = baja) | Mayor | Corredor | Camiones de aves vivas de noche, reefers, horarios municipales | Municipios, 12B |
| LOG-03 | Logística | Disponibilidad de transportistas refrigerados y de aves vivas | 1–5 | Mayor | Corredor | Sin contratistas, la flota es propia (capital y gestión) | Transportistas · DPV-054, DPV-042 |
| EXP-01 | Exportación | Distancia vial a terminal de contenedores con servicio reefer regular | km | Menor | Corredor | Costo y tiempo del flete planta–puerto; **no** equivale a poder exportar (§7) | Terminales, navieras, 12B · DPV-027 |
| EXP-02 | Exportación | Plantas avícolas exportadoras o traders operando en el corredor | n | Mayor | Corredor | Ecosistema exportador: despachantes, consolidación, traders (DPV-081) | SENASA, CEPA · DPV-024 |
| EXP-03 | Exportación | Distancia a oficina SENASA con certificación de exportación | km | Menor | Corredor | Certificación y presencia de inspección | SENASA · DPV-101 |
| TER-01 | Terreno | Parques o áreas industriales que admiten frigorífico avícola | n | Mayor | Corredor | Uso de suelo resuelto y servicios compartidos | Registro de parques industriales, municipios · DPV-12A-04 |
| TER-02 | Terreno | Precio de tierra apta para planta | USD/ha | Menor | Corredor | **Solo como DPV** hasta tener cotizaciones; un terreno barato puede ser caro de operar ([`guia_ramiro.md`](guia_ramiro.md) §5) | Inmobiliarias, `[COTIZACIÓN]` · DPV-087 |
| TER-03 | Terreno | Superficie inundable del partido o departamento | % | Menor | Corredor | Riesgo de acceso y de daños; también filtro en terreno | INA, mapas provinciales · DPV-12A-03 |
| TER-04 | Terreno | Densidad poblacional del partido o departamento | hab/km² | Menor | Corredor | Presión urbana: vecinos, olores, tránsito, expansión | INDEC Censo 2022 · DPV-12A-08 |
| NOR-01 | Normativa | Plazo típico de aptitud o evaluación ambiental | meses | Menor | Provincia | Calendario de habilitación (DPV-086) | Organismos ambientales · DPV-106 |
| NOR-02 | Normativa | Claridad del régimen de uso de suelo industrial | 1–5 | Mayor | Corredor | Previsibilidad; no confundir con "facilidad" negociada | Municipios · DPV-106 |
| RRH-01 | RRHH | Población de 18 a 64 años en radio de 50 km | hab | Mayor | Corredor | Base de reclutamiento de operarios (dotación pendiente en `18_recursos_humanos`) | INDEC · DPV-12A-06 |
| RRH-02 | RRHH | Experiencia local en industria frigorífica o avícola | 1–5 | Mayor | Corredor | Curva de aprendizaje y productividad (DPV-092) | Gremios, municipios, plantas · DPV-12A-06 |
| RRH-03 | RRHH | Oferta de técnicos y profesionales | 1–5 | Mayor | Corredor | Mantenimiento, frío, calidad, veterinarios | Escuelas técnicas, universidades · DPV-12A-06 |

## 3. Correlaciones declaradas (riesgo de doble conteo)

| Par | Relación | Cómo tratarla |
|---|---|---|
| DEM-01 / EXP-01 | Las terminales reefer principales están en CABA y Dock Sud: ambas distancias son casi la misma | Al subir el peso de EXPORTACION, revisar si no se está duplicando el peso de la cercanía al AMBA |
| PRI-02 / PRI-05 | Más granjas cerca = más abastecimiento **y** más presión sanitaria | Mantener ambos: es el trade-off central de una zona avícola fuerte (§6) |
| PRI-01 / IND-01 / EXP-02 | Todas miden el tamaño del cluster | El grupo PRODUCCION_PRIMARIA + FAENA_INDUSTRIA puede sobrerrepresentar a la provincia líder |
| DEM-01 / TER-04 / LOG-02 | Cerca del AMBA = más presión urbana y más congestión | Trade-off, no error: documentado en [`escenarios_localizacion.md`](escenarios_localizacion.md) §2 |
| ALI-01 / ALI-04 | Más maíz cerca suele implicar menor precio en origen | Si hay precios reales, ALI-04 puede reemplazar a ALI-01 |

## 4. Filtros eliminatorios (nivel terreno, no ponderables)

No se suman en la matriz: si un terreno los incumple, se descarta aunque su puntaje regional sea alto. Los umbrales concretos quedan **sin definir** (DEC-12A-03) porque dependen de la escala y de la normativa del sitio.

| Filtro | Pregunta que debe contestarse por escrito | Relacionado |
|---|---|---|
| Uso de suelo | ¿La parcela admite frigorífico avícola (o industria equivalente) y su ampliación? | DPV-106 |
| Agua | ¿Caudal sostenible y calidad suficiente para la escala considerada (o tratable a costo razonable)? | DPV-053 |
| Vuelco | ¿Existe cuerpo receptor o colectora y un permiso de vuelco viable? | DPV-067, DEC-043 |
| Energía | ¿Potencia ampliable en un plazo compatible con el proyecto? | DPV-052, DPV-087 |
| Riesgo hídrico | ¿El terreno y su acceso quedan fuera de zonas inundables? | DPV-12A-03 |
| Vecinos | ¿Distancia y vientos respecto de viviendas y usos sensibles sin conflicto previsible? | DPV-087 |
| Subproductos | ¿Receptor de subproductos y lodos a distancia viable? | DPV-065, DPV-111 |

Regla de la ruta crítica ([`../16_normativa_senasa/ruta_critica_habilitacion.md`](../16_normativa_senasa/ruta_critica_habilitacion.md)): **no comprar ni comprometer un terreno sin verificar uso de suelo, agua y vuelco por escrito.**

## 5. Rúbricas de las escalas 1–5

Una celda 1–5 solo se completa con evidencia citada en `OBSERVACIONES`. **Sin evidencia la celda queda vacía**; nunca se pone "3" por defecto.

| Subcriterio | 1 | 3 | 5 |
|---|---|---|---|
| DEM-05 Mayoristas, gastronomía, elaboradores | Sin compradores identificados en 300 km | Algunos compradores identificados, sin contacto | Compradores contactados con interés documentado (E3+ de la escala comercial) |
| IND-03 Servicios industriales | Repuestos y técnicos a > 1 día | Talleres generales; frío industrial a pocas horas | Proveedores de frío, refrigeración y equipos avícolas con técnicos residentes |
| AGU-02 Calidad del acuífero | No apta sin tratamiento complejo (p. ej., As alto) | Apta con tratamiento convencional | Apta sin tratamiento, con análisis |
| AGU-03 / NOR-02 Régimen de permisos / uso de suelo | Norma inexistente o contradictoria | Norma clara, plazo desconocido | Norma clara con plazo y requisitos publicados |
| EFL-02 Cuerpo receptor | Ninguno practicable | Disponible con obra o restricciones | Colectora o cuerpo receptor con capacidad declarada |
| EFL-03 Sensibilidad ambiental | Humedal, área protegida o curso de uso recreativo cercano | Curso de agua sin uso sensible conocido | Entorno rural sin cuerpos sensibles |
| ENE-01 Potencia en MT | Sin red de MT cercana | Red de MT con ampliación necesaria | Potencia disponible por escrito con margen |
| ENE-02 Gas natural | Sin red; solo GLP | Red a distancia con obra | Red con factibilidad de caudal industrial |
| LOG-02 Congestión | Accesos urbanos congestionados y restricciones horarias | Paso por localidades sin restricción | Acceso directo a ruta sin cruzar áreas urbanas |
| LOG-03 Transportistas | Sin oferta local | Oferta a distancia | Varias empresas locales de aves vivas y refrigerado |
| RRH-02 / RRH-03 Experiencia y técnicos | Sin antecedentes industriales | Industria alimentaria no cárnica | Frigoríficos avícolas, escuelas técnicas y universidad cercanos |

## 6. Bioseguridad y localización (análisis conceptual)

Base técnica en [`../03_produccion_primaria/bioseguridad.md`](../03_produccion_primaria/bioseguridad.md) y [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md). **No se usan distancias reglamentarias**: la distancia de 1.000 m entre granjas aparece solo en extractos de la Res. SENASA 1699/2019 y no se usa como criterio hasta verificar alcance, excepciones y forma de medición (DPV-046).

| Factor | Cómo lo afecta la localización | Ventaja de una zona avícola fuerte | Riesgo de una zona avícola fuerte |
|---|---|---|---|
| **Concentración de granjas** | Determina cuántos productores hay para integrar y cuán cerca están unos de otros | Abastecimiento, contratistas, técnicos, veterinarios | Un brote se propaga más fácil; zonas de control abarcan más granjas propias |
| **Distancia planta–granja** | Define horas de viaje, DOA, merma de ayuno y bienestar | Granjas cerca de la planta (viajes cortos) | Granjas de terceros intercaladas con las propias |
| **Tránsito de aves y vehículos** | Camiones, cajones y cuadrillas son el principal puente sanitario entre granjas | Logística de captura establecida | Rutas compartidas con camiones de otras empresas; más cruces |
| **Zonas avícolas y planta** | La planta concentra camiones de todas las granjas: es un nodo de riesgo | Servicios de lavado y desinfección conocidos | Si la planta está dentro del cluster, su tránsito pasa cerca de granjas de terceros |
| **Riesgo sanitario de exportación** | Una zona de control por IAAP puede suspender certificaciones regionales (regionalización reconocida solo por algunos destinos, FTE-097 `[PVDP]`) | Experiencia de los organismos y del sector en manejo de brotes | La concentración aumenta la probabilidad de quedar dentro de una zona afectada |
| **Expansión** | Para crecer hacen falta nuevas granjas a distancia sanitaria entre sí | Hay productores dispuestos a ampliar | Tierra apta para granjas nuevas escasa y competida |
| **Compartimentación futura** | Un compartimento reconocido (Res. 484/2017 `[PVDP]`) es independiente de la geografía pero exige control total | — | Compra spot de pollo vivo incompatible con compartimentación (DEC-025) |

**Lectura:** una zona de **baja densidad** (p. ej., partes de Chaco, del interior bonaerense o de Córdoba) ofrece mejores condiciones sanitarias **iniciales**, pero obliga a construir el ecosistema (productores, incubadora, servicios) y no garantiza baja densidad futura si el propio proyecto crece. Una zona de **alta densidad** (el corredor del río Uruguay en Entre Ríos) ofrece ecosistema inmediato a cambio de mayor exposición. Ninguna es mejor en abstracto: depende del modelo de abastecimiento (DEC-020), de la vocación exportadora (DEC-011) y del nivel de bioseguridad objetivo (DEC-025).

## 7. Exportación: distancia al puerto ≠ posibilidad de exportar

Una planta cerca del puerto **no** se vuelve exportadora. Exportar requiere, en este orden ([`../16_normativa_senasa/exportacion_y_certificaciones.md`](../16_normativa_senasa/exportacion_y_certificaciones.md), [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md)): (1) país destino abierto (categoría A, regla 17); (2) planta habilitada y listada para ese destino; (3) producto autorizado; (4) comprador con contrato; (5) volumen para lotes y congelado; (6) logística reefer. La distancia al puerto solo actúa en el punto 6, y su peso es pequeño frente a los anteriores. Por eso EXP-01 tiene peso bajo en todos los perfiles salvo el D, y aun en D se combina con EXP-02 (ecosistema exportador) y EXP-03 (certificación).

## 8. Criterios que existen solo a nivel de terreno

No están en la matriz regional; se relevan con la [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md): superficie y forma, cota y drenaje, vecinos inmediatos y vientos, accesos separados, dominio, napa, contaminación previa, servicios en el lindero, precio cotizado, terrenos linderos para expansión. Requisitos del terreno en [`terreno_ideal.md`](terreno_ideal.md).

## 9. Factor cualitativo NO puntuable: network / acceso

El contacto familiar, político o social del promotor en Chaco (SUP-014) se registra **solo** como ventaja cualitativa de **acceso a información y a interlocutores** para relevar esa zona. No se convierte en beneficio económico, facilidad regulatoria, reducción de plazos ni recomendación de ubicación, y **no tiene peso** en ningún perfil (el modelo rechaza un peso > 0 en NETWORK; test T08). Tratamiento en [`regiones_preliminares.md`](regiones_preliminares.md) §6.
