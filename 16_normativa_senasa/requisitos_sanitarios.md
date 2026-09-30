# Requisitos sanitarios de una planta de faena y procesamiento avícola

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B · Relacionado: [`habilitacion_planta.md`](habilitacion_planta.md), [`mapa_regulatorio.md`](mapa_regulatorio.md), [`subproductos_normativa.md`](subproductos_normativa.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv), [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md), [`../04_balance_masa/conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md)

> **Alcance:** identifica **requisitos y principios** que condicionan el diseño y la operación. **No** dimensiona layout, **no** selecciona equipos, **no** fija dotación de inspección.
> **Verificación:** todo contenido normativo es `[PVDP]` (acceso primario bloqueado, DPV-009). Se distingue **obligatorio (norma)**, **esperable (práctica exigida en inspección)** y **buena práctica**; cuando no se pudo confirmar la base legal se dice.

---

## 1. Marco SENASA aplicable (visión de conjunto)

| Tema | Norma(s) identificada(s) | Qué regula | Estado |
|---|---|---|---|
| Establecimientos faenadores avícolas | Decreto 4238/68 cap. XX (mod. Res. 553/2002) | Definición de matadero de aves, ubicación, construcción, equipos, tecnología, inspección | `[PVDP]` FTE-016, FTE-09B-04 |
| Habilitación y registro | Procedimiento SENASA (SIGTrámites); Res. 233/2026 (documentación local) | Trámite, documentación, rubros, plazos | `[PVDP]` FTE-09B-02, FTE-09B-11 |
| Condiciones edilicias | Decreto 4238/68 (capítulos generales + cap. XX) | Materiales, desagües, iluminación, vestuarios, flujos | `[PVDP]` |
| Higiene | Res. SENASA 233/1998 (POES); BPM (reglamento y CAA) | Saneamiento diario y buenas prácticas | `[PVDP]` FTE-09B-03 |
| Inspección veterinaria | Decreto 4238/68; SIV en planta | Ante/post mortem, dictamen, decomisos | `[PVDP]` |
| Agua potable | CAA arts. 982 y ss.; Decreto 4238/68 | Potabilidad, análisis | `[PVDP]` FTE-09B-09 |
| Efluentes | Nacional: requisito documental en habilitación SENASA; fondo: **provincial** | Tratamiento y vuelco | **[JURISDICCIÓN]** |
| Decomisos | Decreto 4238/68 | Destino de lo no apto | `[PVDP]` |
| Cámaras y temperaturas | Decreto 4238/68 (cap. a identificar) | Refrigeración, congelación | `[PVDP]` — contradicción C5 |
| Trazabilidad | RENSPA, DT-e, SIGSA, Res. 1699/2019 (granjas); rotulado y registros de planta; Res. 593/2026 exige trazabilidad documentada para exportar | Lote granja → planta → producto | `[PVDP]` FTE-09B-12 |
| Transporte | Res. SENASA 723/2025 (derogó 503/2022, 735/2022, 557/2024) | Vehículos de animales vivos, productos, subproductos | `[PVDP]` FTE-09B-07 |
| Bienestar animal | Decreto 4238/68 cap. XXXII; manual SENASA de faena de aves y lagomorfos; Res. 575/2018 (granja) | Espera, manejo, insensibilización, sacrificio | `[PVDP]` FTE-09B-06, FTE-145 |
| Residuos veterinarios y contaminantes | Plan CREHA; Res. 445/2024 (antimicrobianos promotores) | Muestreo oficial; proveedores | `[PVDP]` FTE-110, FTE-109 |
| Subproductos | Ver [`subproductos_normativa.md`](subproductos_normativa.md) | | |

## 2. Condiciones edilicias (principios, sin dimensionar)

Base: principios de diseño higiénico recogidos por el Decreto 4238/68 y por guías internacionales (Codex CXC 58-2005, citado de memoria, `[PVDP]`). **Los valores numéricos (lux, alturas, pendientes, temperaturas de agua) no se transcriben porque no se leyó el texto.**

| Elemento | Principio sanitario | Tipo | Impacto en diseño | Estado |
|---|---|---|---|---|
| Pisos | Impermeables, antideslizantes, resistentes a golpes y químicos, con pendiente a desagües | Obligatorio (reglamento) | Obra civil; costo de revestimientos | `[PVDP]` |
| Paredes | Lisas, impermeables, lavables, de color claro, con zócalo sanitario y ángulos redondeados | Obligatorio | Tipo de panel o revestimiento | `[PVDP]` |
| Techos / cielorrasos | Lisos, sin condensación ni desprendimientos; altura suficiente en faena | Obligatorio | Aislación y ventilación | `[PVDP]` |
| Drenajes | Rejillas sifonadas, tapas, pendientes; nunca de zona sucia a limpia; separación de pluviales | Obligatorio | Trazado de desagües **antes** del layout definitivo | `[PVDP]` |
| Iluminación | Intensidad mínima diferenciada, mayor en **puestos de inspección**; luminarias protegidas | Obligatorio (valores a leer) | Eléctrica | `[PVDP]` |
| Ventilación | Evitar condensación, olores y vapores; presión positiva en zonas limpias (buena práctica) | Obligatorio / buena práctica | Climatización | `[PVDP]` |
| Lavamanos | De accionamiento no manual, con agua caliente, jabón y secado; en accesos y puestos | Obligatorio | Cantidad y ubicación | `[PVDP]` |
| Esterilizadores de utensilios | Agua caliente a temperatura reglamentaria en puestos de corte e inspección | Obligatorio (valor a leer) | Agua caliente y energía | `[PVDP]` |
| Vestuarios y sanitarios | Separados de salas de proceso, por sexo, dimensionados por personal; separación zona sucia/limpia | Obligatorio | Superficie y flujos de personal | `[PVDP]` |
| Barreras sanitarias | Lavabotas / pediluvios y lavamanos en ingresos a salas | Esperable | Accesos | `[PVDP]` |
| **Separación sucio / limpio** | Recepción, colgado, aturdimiento, sangrado, escaldado, desplumado (**sucia**) separados físicamente de evisceración, enfriamiento, trozado, empaque (**limpia**) | Obligatorio | **Condiciona todo el layout** | `[PVDP]` |
| Circulación | Producto avanza sin retroceder; personal, residuos, envases y subproductos con flujos que no crucen al producto | Obligatorio / buena práctica | Layout | `[PVDP]` |
| Cámaras | Materiales lavables, termómetros/registradores, antecámaras; separación de producto crudo, terminado, decomisado | Obligatorio | Frío (`12_energia_frio`) | `[PVDP]` |
| Depósitos | Envases y materiales separados de químicos; químicos bajo llave | Obligatorio / BPM | Superficies | `[PVDP]` |
| Docks | Andén de recepción de aves cubierto y ventilado; dock de expedición con sello/abrigo para mantener frío | Obligatorio (recepción) / buena práctica (sellos) | Obra civil | `[PVDP]` |
| Control de plagas | Programa MIP, cerramientos, mallas, cortinas de aire, sin huecos | Obligatorio (BPM) | Cerramientos | `[PVDP]` |
| Oficina SIV | Espacio para la inspección oficial | Obligatorio (práctica SENASA) | Superficie | `[PVDP]` |
| Sala/contenedores de decomisos | Identificados, con cierre, circuito propio | Obligatorio | Layout de residuos | `[PVDP]` |

## 3. Agua

| Aspecto | Qué se sabe | Tipo | Estado |
|---|---|---|---|
| Potabilidad | Toda agua en contacto con el producto o superficies debe ser **potable** según el CAA (art. 982 y ss.) | Obligatorio | `[PVDP]` FTE-09B-09 |
| Análisis | Análisis microbiológico y fisicoquímico en laboratorio habilitado, con registros; parámetros típicos: *E. coli*, coliformes, pH, turbiedad, nitratos, cloro residual | Obligatorio (frecuencia a confirmar) | `[PVDP]` |
| Frecuencia | Un extracto de un sitio comercial menciona bacteriológico semestral y fisicoquímico anual como práctica general; **no es la norma de frigoríficos** | Desconocido | `[PVDP · débil]` — **no se adopta** |
| Agua caliente | Necesaria para lavamanos, esterilizadores y limpieza; temperaturas reglamentarias **no leídas** | Obligatorio | `[PVDP]` |
| Agua no potable | En general solo admitida para usos sin contacto (incendio, refrigeración de condensadores, algunos lavados de patio), con **cañerías separadas e identificadas**; admisibilidad exacta en el reglamento argentino **no verificada** | Condicional | POR CONSULTAR A SENASA |
| Reúso de agua (p. ej., de chiller a escaldado) | Posible en otros países con condiciones; en Argentina **no verificado** | Condicional | POR CONSULTAR A SENASA |
| Cloración y control | Cloro residual en red y en chiller; registros | Esperable | `[PVDP]` |
| Tanques y red | Limpieza periódica documentada, plano de red con puntos de muestreo | Esperable | `[PVDP]` |
| Registros | Planilla de cloro, análisis, limpieza de tanques, mantenimiento | Obligatorio (BPM/POES) | `[PVDP]` |

**Coordinación con el futuro módulo de agua (`11_agua_efluentes`):** este archivo define **calidad y controles**; el caudal, el origen (red/perforación), el tratamiento y el balance hídrico se calculan allá. El balance de masa **no** dimensiona el consumo de agua de la planta ([`../04_balance_masa/conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md)).

## 4. Inspección veterinaria oficial

| Etapa | Qué es | Quién | Registros | Estado |
|---|---|---|---|---|
| Documentación de ingreso | Verificar DT-e, RENSPA de origen y registro del criador (mortandad, tratamientos) antes de faenar | SIV (SENASA) y operador | DT-e; registro del criador | `[PVDP]` FTE-09B-12 |
| **Ante mortem** | Examen del lote vivo en recepción: estado, mortalidad en transporte (DOA), signos de enfermedad; puede ordenar faena separada o rechazo | Veterinario oficial | Acta/planilla por lote | `[PVDP]` |
| **Post mortem** | Examen de carcasas y vísceras en la línea (puestos de inspección con iluminación y espacio); dictamen de aptitud | Veterinario oficial y auxiliares | Planillas de hallazgos por causa | `[PVDP]` |
| **Decomisos** | Total (carcasa entera) o parcial (partes); el veterinario oficial determina eliminación o retiro | SIV decide; operador ejecuta destino | Registro de decomisos por lote y causa | `[PVDP]` |
| Dictamen final | Aptitud para consumo humano; marca/sello sanitario | SIV | — | `[PVDP]` |
| Muestreos oficiales | Plan CREHA (residuos), microbiología oficial | SIV | Actas | `[PVDP]` FTE-110 |
| Responsabilidad del operador | Autocontroles (POES, BPM, HACCP donde aplique), trazabilidad, destino de decomisos, bienestar | Empresa | Programas escritos y registros | `[PVDP]` |

**Dotación:** no se especula; es pregunta a SENASA (P-12). Costo de inspección y tasas: no relevado (DPV-09B-05).
**Vínculo con el balance de masa:** los registros de decomisos del SIV son la fuente para calibrar la condena del modelo (DPV-063).

## 5. BPM, POES, HACCP y certificaciones voluntarias (no son equivalentes)

| Programa | Qué es | Obligatoriedad en Argentina | Para exportar | Estado |
|---|---|---|---|---|
| **BPM / BPF** (Buenas Prácticas de Manufactura) | Condiciones básicas de higiene del personal, edificio, equipos, materias primas, plagas, agua, capacitación | **Obligatorias** para establecimientos que faenen, elaboren, fraccionen o depositen alimentos (Res. SENASA 233/1998; CAA) | Base de todo | `[PVDP]` FTE-09B-03 |
| **POES / SSOP** (Procedimientos Operativos Estandarizados de Saneamiento) | Procedimientos **escritos** de limpieza y desinfección diaria (pre-operativa y operativa), con responsables, frecuencias, verificación y acciones correctivas | **Obligatorios** (Res. SENASA 233/1998): firmados por un responsable con autoridad y presentados ante SENASA; se actualizan ante cambios | Exigidos | `[PVDP]` FTE-09B-03 |
| **HACCP / APPCC** | Análisis de peligros y control de puntos críticos (p. ej., enfriamiento, temperatura de cámaras, contaminación fecal) | **No verificado** con carácter general para faena aviar de mercado interno. Un extracto (FAOLEX) indica HACCP obligatorio para carne picada y alimentos listos para consumo y luego para otros alimentos, **sin identificar la norma**; la Res. Conj. 87/2008-340/2008 del CAA lo haría obligatorio "para los productos que el Código indique" | **Exigido por la mayoría de los destinos** y por grandes compradores | `[PVDP]` FTE-09B-16 — POR CONSULTAR A SENASA |
| **MIP** (Manejo Integrado de Plagas) | Programa de plagas | Parte de BPM | Exigido | `[PVDP]` |
| **ISO 22000** | Sistema de gestión de inocuidad (norma ISO) | Voluntaria | Diferencial comercial | — |
| **FSSC 22000** | ISO 22000 + prerrequisitos (ISO/TS 22002-1) + requisitos adicionales; reconocida por GFSI | Voluntaria | Exigida por algunos compradores/retailers | — |
| **BRCGS / IFS** | Normas privadas de retail (Reino Unido / Europa continental), reconocidas por GFSI | Voluntarias | Exigidas por retailers de UE/UK | — |
| **Halal** | Certificación religiosa por organismo reconocido por el destino | Voluntaria salvo para exportar a destinos que la exigen | Obligatoria para el Golfo y otros | `[PVDP]` FTE-082 |
| **Bienestar animal privado** (auditorías de clientes, estándares tipo NAMI/OIE-OMSA) | Auditorías de segunda parte | Voluntarias | Exigidas por algunos compradores | — |

**Lectura:** BPM y POES son **piso legal**; HACCP es **esperable** para una planta que aspire a exportar y probablemente necesario en la práctica aun para supermercados grandes; ISO/FSSC/BRCGS/IFS son **decisiones comerciales** posteriores. Los supermercados de la red podrían exigir auditorías propias (DPV-041).

## 6. Bienestar animal (planta)

**Normativa argentina** (`[PVDP]`, FTE-09B-06):

| Etapa | Qué se sabe | Estado |
|---|---|---|
| Definición y alcance | Decreto 4238/68 cap. XXXII: bienestar = necesidades satisfechas, alojamiento adecuado, trato responsable y **sacrificio humanitario**; alcanza carga, transporte, descarga, degüello y procesado | `[PVDP]` |
| Ayuno | Un extracto indica que los pollos **no deben ayunar más de 12 h** entre la captura y la insensibilización; no se identificó si es norma o guía | `[PVDP]` — norma vs guía a confirmar |
| Transporte | Vehículos habilitados (Res. 723/2025); densidad y condiciones de jaulas: no leídas | `[PVDP]` |
| Descarga y espera | Espera en planta **30 min a 3 h** según el manual de SENASA (guía); andén cubierto y ventilado | `[PVDP]` guía, no necesariamente norma |
| Manejo y colgado | Manual SENASA de bienestar en plantas de faena de aves y lagomorfos (recepción, pesaje, espera, colgado, insensibilización, degüello) | `[PVDP]` FTE-09B-06 |
| Aturdido (insensibilización) | Obligatorio previo al degüello según el enfoque de "sacrificio humanitario"; **parámetros eléctricos y verificación de inconsciencia no leídos** | `[PVDP]` |
| Sacrificio | Sección de grandes vasos del cuello; tiempo hasta escaldado a verificar | `[PVDP]` |
| Granja | Res. SENASA 575/2018 (engorde) | `[PVDP]` FTE-145 |

**Exigencias de clientes y mercados externos (separadas de la norma argentina):** UE — Reg. (CE) 1099/2009 (atestación de equivalencia; operarios con certificado de competencia; procedimientos operativos estándar; monitoreo del aturdido), `[PVDP]`; destinos Halal — posibles restricciones al aturdimiento o exigencia de aturdimiento reversible (**no verificadas**, DPV-034); compradores privados — auditorías propias. **No se diseña** ninguna línea sin aturdimiento.

## 7. Transporte

| Carga | Requisito identificado | Vehículo propio | Vehículo de tercero | Estado |
|---|---|---|---|---|
| **Aves vivas** | Habilitación sanitaria del vehículo (Res. 723/2025): número pintado en ambos laterales y trasera ("HABILITACIÓN SENASA N°…", letras ≥ 8 cm según norma anterior), lavado y desinfección, DT-e firmado por el transportista como DJ | La empresa habilita cada unidad y es responsable del lavado/desinfección y del bienestar | Exigir habilitación vigente y constancia de lavado; el remitente/receptor sigue siendo responsable de recibir solo aves con DT-e | `[PVDP]` FTE-09B-07 |
| **Producto refrigerado / congelado** | Habilitación del vehículo por categoría según caja (isotermo, con equipo de frío = categoría A), termómetro, hermeticidad, bandejas colectoras; condiciones higiénicas | Idem, más registros de temperatura | Exigir habilitación y registros; cláusula contractual de cadena de frío | `[PVDP]` FTE-09B-08 |
| **Subproductos** (plumas, sangre, vísceras) | Vehículo habilitado para subproductos no aptos para consumo humano; estanco | Idem | Habitual: lo retira el receptor (rendering) con su vehículo habilitado | `[PVDP]` FTE-09B-07 |
| **Residuos** (lodos, contenido GI, decomisos no valorizables) | Transportista y operador habilitados por la autoridad ambiental; manifiesto si son residuos especiales | Raro | Habitual | **[JURISDICCIÓN]** |

La Res. 723/2025 también creó un programa de certificación de diseños de vehículos 0 km (validez 5 años). Detalle logístico: `13_logistica` (pendiente) y DPV-058.

## 8. Cadena de frío

| Aspecto | Qué se sabe | Tipo | Estado |
|---|---|---|---|
| Enfriamiento de carcasas | Obligatorio tras la evisceración, por inmersión (con control de absorción de agua) o por aire; temperatura objetivo y tiempo **no leídos** | Obligatorio | `[PVDP]` DPV-061 |
| Conservación refrigerada | Extracto: −2 a 2 °C con tolerancia ±2 °C | A confirmar | `[PVDP · contradictorio]` C5 |
| Congelado | Extracto: "no superior a −4 °C" (valor atípico; los destinos de exportación suelen exigir ≤ −18 °C) | A confirmar | `[PVDP · contradictorio]` C5 |
| Enfriamiento por aire | Extracto: pechuga ≤ 7 °C; **posible origen en normativa brasileña** (la búsqueda devolvió un documento de Brasil) | A confirmar | `[PVDP · origen dudoso]` |
| Almacenamiento | Cámaras con termómetro y registro; separación por tipo de producto | Obligatorio | `[PVDP]` |
| Transporte | Vehículos categoría con equipo de frío y termómetro (Res. 723/2025) | Obligatorio | `[PVDP]` |
| Registros de temperatura | Continuos en cámaras y túneles (registradores), en recepción y despacho; parte del HACCP | Esperable / exigido por destinos | `[PVDP]` |

**No se adopta ningún valor de temperatura** hasta leer el reglamento (DPV-09B-02).

## 9. Rotulado y productos (impacto regulatorio, sin diseñar etiquetas)

| Producto | Cómo impacta la regulación | Estado |
|---|---|---|
| Pollo entero | Rótulo con número de establecimiento SENASA, producto registrado (CAPA), fechas; declaración de menudencias si las incluye | `[PVDP]` FTE-09B-14/15 |
| Cortes | Cada corte y presentación se registra; denominaciones reglamentarias | `[PVDP]` |
| Menudencias | Productos propios con registro; alta perecibilidad | `[PVDP]` |
| **CMS** | Uso restringido (chacinados cocidos y conservas, según extracto); temperatura y plazo específicos; rotulado a verificar | `[PVDP]` FTE-185, DPV-074 |
| Elaborados (marinados, milanesas, chacinados, cocidos) | Rubros de habilitación adicionales; aditivos según CAA/reglamento; rotulado nutricional (CAA cap. V, Res. GMC 26/03) y eventual sellos de advertencia (Ley 27.642, citada de memoria) | `[PVDP]` |
| **Agua retenida** | Límite de absorción en enfriamiento por inmersión (~8 % según prensa) y método de control; posible declaración en rótulo | `[PVDP]` DPV-061 |
| Productos congelados | Denominación "congelado", temperatura de conservación, vida útil, eventual prohibición de recongelar | `[PVDP]` |
| Exportación | Idioma, número de planta, marca sanitaria, logos (Halal), requisitos por destino | [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md) |

El registro es **por producto y presentación** ante CAPA, por TAD, con **monografía de proceso**: cada nuevo producto implica trámite (FTE-09B-14).

## 10. Trazabilidad (granja → despacho)

Requerimientos identificados: RENSPA y DT-e para mover aves (sin RENSPA vigente no se emite DT-e); registro del criador por lote con mortandad cargada en SIGSA antes del primer DT-e a faena (Res. 1699/2019); la Res. 593/2026 exige **trazabilidad documentada** para autorizar destinos de exportación; la UE exige atestación de no uso de antimicrobianos prohibidos (art. 118) (FTE-09B-12, FTE-09B-05, FTE-107; `[PVDP]`).

| Eslabón | Datos que deberían capturarse | Base |
|---|---|---|
| Granja | RENSPA, galpón, lote SIGSA, genética, fecha de alojamiento, origen del pollito (planta de incubación), alimento (fábrica, lote), medicamentos y vacunas con períodos de retiro, mortalidad, programa *Salmonella* | Obligatorio (RENSPA/registro del criador) + exigencia de destinos |
| Lote de faena | Fecha y hora de retiro de alimento (ayuno), captura, carga | Bienestar; buena práctica |
| Transporte | DT-e, vehículo habilitado, chofer, horarios de salida y llegada, DOA | Obligatorio (DT-e) |
| Recepción | Peso bruto/tara, conteo, espera, resultado ante mortem | Obligatorio (SIV) / buena práctica |
| Faena | Lote de faena ↔ lote de granja, hora, línea, decomisos por causa, temperatura de chiller, absorción | Obligatorio (SIV) / HACCP |
| Producción | Lote de producción por producto y fecha, rendimiento, operarios/sector | Buena práctica / rótulo |
| Cámara | Ubicación, fecha/hora de ingreso, temperatura, congelado (túnel, tiempo) | HACCP / exportación |
| Despacho | Cliente, remito, vehículo habilitado, temperatura de carga, precinto, certificado sanitario (exportación: SIGCER, contenedor) | Obligatorio (exportación) / buena práctica |

Recomendación de principio (no de sistema): **identificar el lote de faena con el lote SIGSA de la granja** desde el día 1; un sistema digital facilita la exportación ([`../17_exportacion/requisitos_planta_exportadora.md` §3](../17_exportacion/requisitos_planta_exportadora.md)).
