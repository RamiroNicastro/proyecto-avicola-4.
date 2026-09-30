# Requisitos sanitarios de una planta de faena y procesamiento avícola

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B · Relacionado: [`habilitacion_planta.md`](habilitacion_planta.md), [`mapa_regulatorio.md`](mapa_regulatorio.md), [`subproductos_normativa.md`](subproductos_normativa.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv), [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md), [`../04_balance_masa/conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md)

> **Alcance:** identifica **requisitos y principios** que condicionan el diseño y la operación. **No** dimensiona layout, **no** selecciona equipos, **no** fija dotación de inspección.
> **Verificación:** todo contenido normativo es `[PVDP]` (acceso primario bloqueado, DPV-009). Se distingue **obligatorio (norma)**, **esperable (práctica exigida en inspección)** y **buena práctica**; cuando no se pudo confirmar la base legal se dice.

---

## 1. Marco SENASA aplicable (visión de conjunto)

| Tema | Norma(s) identificada(s) | Qué regula | Estado |
|---|---|---|---|
| Establecimientos faenadores avícolas | Decreto 4238/68 cap. XX (mod. Res. 553/2002) | Definición de matadero de aves, ubicación, construcción, equipos, tecnología, inspección | `[PVDP]` FTE-016, FTE-232 |
| Habilitación y registro | Procedimiento SENASA (SIGTrámites); Res. 233/2026 (documentación local) | Trámite, documentación, rubros, plazos | `[PVDP]` FTE-230, FTE-238 |
| Condiciones edilicias | Decreto 4238/68 (capítulos generales + cap. XX) | Materiales, desagües, iluminación, vestuarios, flujos | `[PVDP]` |
| Higiene e inocuidad | Res. SENASA 233/1998 (POES); BPM (reglamento y CAA); **Res. SENASA 205/2014 (Plan APPCC obligatorio; cap. XXXI del Decreto 4238/68)** | Saneamiento diario, buenas prácticas y análisis de peligros | `[PVDP]` FTE-231, FTE-243 |
| Sistema Nacional de Control de Alimentos | **Decreto 697/2026** (BO 2026-08-03) | Reorganiza el sistema alimentario general (CAA): SENASA concentra registro, control y fiscalización; registro único y base única de datos. **Convivencia con el Decreto 4238/68 por confirmar** ([`mapa_regulatorio.md` §6](mapa_regulatorio.md)) | `[PVDP]` FTE-251 |
| Inspección veterinaria | Decreto 4238/68; SIV en planta | Ante/post mortem, dictamen, decomisos | `[PVDP]` |
| Agua potable | CAA arts. 982 y ss.; Decreto 4238/68 | Potabilidad, análisis | `[PVDP]` FTE-236 |
| Efluentes | Nacional: requisito documental en habilitación SENASA; fondo: **provincial** | Tratamiento y vuelco | **[JURISDICCIÓN]** |
| Decomisos | Decreto 4238/68 | Destino de lo no apto | `[PVDP]` |
| Cámaras y temperaturas | Decreto 4238/68 (cap. a identificar) | Refrigeración, congelación | `[PVDP]` — contradicción C5 |
| Trazabilidad | RENSPA, DT-e, SIGSA, Res. 1699/2019 (granjas); rotulado y registros de planta; Res. 593/2026 exige trazabilidad documentada para exportar | Lote granja → planta → producto | `[PVDP]` FTE-239 |
| Transporte | Res. SENASA 723/2025 (derogó 503/2022, 735/2022, 557/2024) | Vehículos de animales vivos, productos, subproductos | `[PVDP]` FTE-234 |
| Bienestar animal | Decreto 4238/68 cap. XXXII; manual SENASA de faena de aves y lagomorfos; Res. 575/2018 (granja) | Espera, manejo, insensibilización, sacrificio | `[PVDP]` FTE-233, FTE-145 |
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
| Potabilidad | Toda agua en contacto con el producto o superficies debe ser **potable** según el CAA (art. 982 y ss.) | Obligatorio | `[PVDP]` FTE-236 |
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
| Documentación de ingreso | Verificar DT-e, RENSPA de origen y registro del criador (mortandad, tratamientos) antes de faenar | SIV (SENASA) y operador | DT-e; registro del criador | `[PVDP]` FTE-239 |
| **Ante mortem** | Examen del lote vivo en recepción: estado, mortalidad en transporte (DOA), signos de enfermedad; puede ordenar faena separada o rechazo | Veterinario oficial | Acta/planilla por lote | `[PVDP]` |
| **Post mortem** | Examen de carcasas y vísceras en la línea (puestos de inspección con iluminación y espacio); dictamen de aptitud | Veterinario oficial y auxiliares | Planillas de hallazgos por causa | `[PVDP]` |
| **Decomisos** | Total (carcasa entera) o parcial (partes); el veterinario oficial determina eliminación o retiro | SIV decide; operador ejecuta destino | Registro de decomisos por lote y causa | `[PVDP]` |
| Dictamen final | Aptitud para consumo humano; marca/sello sanitario | SIV | — | `[PVDP]` |
| Muestreos oficiales | Plan CREHA (residuos), microbiología oficial | SIV | Actas | `[PVDP]` FTE-110 |
| Responsabilidad del operador | Autocontroles (BPM, POES y Plan APPCC —Res. 205/2014—), trazabilidad, destino de decomisos, bienestar | Empresa | Programas escritos y registros | `[PVDP]` |

**Dotación:** no se especula; es pregunta a SENASA (P-12). Costo de inspección y tasas: no relevado (DPV-101).
**Vínculo con el balance de masa:** los registros de decomisos del SIV son la fuente para calibrar la condena del modelo (DPV-063).

## 5. BPM, POES, APPCC/HACCP y certificaciones voluntarias (no son equivalentes)

| Programa | Qué es | Obligatoriedad en Argentina | Para exportar | Estado |
|---|---|---|---|---|
| **BPM / BPF** (Buenas Prácticas de Manufactura) | Condiciones básicas de higiene del personal, edificio, equipos, materias primas, plagas, agua, capacitación | **Obligatorias** para establecimientos que faenen, elaboren, fraccionen o depositen alimentos (Res. SENASA 233/1998; CAA) | Base de todo | `[PVDP]` FTE-231 |
| **POES / SSOP** (Procedimientos Operativos Estandarizados de Saneamiento) | Procedimientos **escritos** de limpieza y desinfección diaria (pre-operativa y operativa), con responsables, frecuencias, verificación y acciones correctivas | **Obligatorios** (Res. SENASA 233/1998): firmados por un responsable con autoridad y presentados ante SENASA; se actualizan ante cambios | Exigidos | `[PVDP]` FTE-231 |
| **APPCC / HACCP regulatorio SENASA** | Análisis de peligros y control de puntos críticos (p. ej., enfriamiento, temperatura de cámaras, contaminación fecal) | **Obligatorio (regulatorio, no solo exportador).** La **Res. SENASA 205/2014** (BO 2014-05-20) incorporó el APPCC al Reglamento del Decreto 4238/68 (cap. XXXI, renombrado "BPF, POES y APPCC"): los establecimientos **bajo jurisdicción SENASA** donde se faenen animales, elaboren, fraccionen y/o depositen alimentos deben **desarrollar, implementar y mantener un Plan APPCC**, con las **excepciones** que establezca SENASA según tecnología o actividad (los extractos citan como exentos a establecimientos de clasificación de huevos). Implementación escalonada: 180 días para carne picada/molida y alimentos listos para consumo; 365 días para el resto | Base común; los destinos agregan exigencias propias (fila siguiente) | `[PVDP]` FTE-243 (el extracto FAOLEX antes "sin norma identificada" corresponde a esta resolución). Excepciones aplicables a una planta avícola: POR CONSULTAR A SENASA (P-43) |
| **Exigencias APPCC adicionales de destinos de exportación** | Requisitos del país importador sobre el plan (p. ej., criterios microbiológicos, controles de *Salmonella*, verificación oficial, formato de auditoría) | No aplica en mercado interno | **Adicionales** al APPCC regulatorio; se verifican en la autorización de destino y en auditorías | `[PVDP]` — ver [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md) |
| **MIP** (Manejo Integrado de Plagas) | Programa de plagas | Parte de BPM | Exigido | `[PVDP]` |
| **ISO 22000** | Sistema de gestión de inocuidad (norma ISO) | Voluntaria | Diferencial comercial | — |
| **FSSC 22000** | ISO 22000 + prerrequisitos (ISO/TS 22002-1) + requisitos adicionales; reconocida por GFSI | Voluntaria | Exigida por algunos compradores/retailers | — |
| **BRCGS / IFS** | Normas privadas de retail (Reino Unido / Europa continental), reconocidas por GFSI | Voluntarias | Exigidas por retailers de UE/UK | — |
| **Halal** | Certificación religiosa por organismo reconocido por el destino | Voluntaria salvo para exportar a destinos que la exigen | Obligatoria para el Golfo y otros | `[PVDP]` FTE-082 |
| **Bienestar animal privado** (auditorías de clientes, estándares tipo NAMI/OIE-OMSA) | Auditorías de segunda parte | Voluntarias | Exigidas por algunos compradores | — |

**Lectura (tres capas que no deben mezclarse):**
1. **Regulatorio SENASA (piso legal, mercado interno incluido):** BPM, POES y **Plan APPCC** (Res. 233/1998 y Res. 205/2014, cap. XXXI del Decreto 4238/68), salvo excepción expresa de SENASA.
2. **Exigencias adicionales de mercados de exportación:** requisitos del destino sobre el APPCC, microbiología, bienestar, antimicrobianos, Halal, verificadas en la autorización de destino y en auditorías.
3. **Certificaciones privadas de clientes:** ISO 22000, FSSC 22000, BRCGS, IFS, auditorías de supermercados (DPV-041): **decisiones comerciales**, no requisitos legales.

El texto de la Res. 205/2014 no se leyó en original (acceso bloqueado): el contenido proviene de extractos coincidentes del Boletín Oficial, Infoleg (cap. XXXI) y FAOLEX `[PVDP]`.

## 6. Bienestar animal (planta)

**Normativa argentina** (`[PVDP]`, FTE-233):

| Etapa | Qué se sabe | Estado |
|---|---|---|
| Definición y alcance | Decreto 4238/68 cap. XXXII: bienestar = necesidades satisfechas, alojamiento adecuado, trato responsable y **sacrificio humanitario**; alcanza carga, transporte, descarga, degüello y procesado | `[PVDP]` |
| Ayuno | Un extracto indica que los pollos **no deben ayunar más de 12 h** entre la captura y la insensibilización; no se identificó si es norma o guía | `[PVDP]` — norma vs guía a confirmar |
| Transporte | Vehículos habilitados (Res. 723/2025); densidad y condiciones de jaulas: no leídas | `[PVDP]` |
| Descarga y espera | Espera en planta **30 min a 3 h** según el manual de SENASA (guía); andén cubierto y ventilado | `[PVDP]` guía, no necesariamente norma |
| Manejo y colgado | Manual SENASA de bienestar en plantas de faena de aves y lagomorfos (recepción, pesaje, espera, colgado, insensibilización, degüello) | `[PVDP]` FTE-233 |
| Aturdido (insensibilización) | Obligatorio previo al degüello según el enfoque de "sacrificio humanitario"; **parámetros eléctricos y verificación de inconsciencia no leídos** | `[PVDP]` |
| Sacrificio | Sección de grandes vasos del cuello; tiempo hasta escaldado a verificar | `[PVDP]` |
| Granja | Res. SENASA 575/2018 (engorde) | `[PVDP]` FTE-145 |

**Exigencias de clientes y mercados externos (separadas de la norma argentina):** UE — Reg. (CE) 1099/2009 (atestación de equivalencia; operarios con certificado de competencia; procedimientos operativos estándar; monitoreo del aturdido), `[PVDP]`; destinos Halal — posibles restricciones al aturdimiento o exigencia de aturdimiento reversible (**no verificadas**, DPV-034); compradores privados — auditorías propias. **No se diseña** ninguna línea sin aturdimiento.

## 7. Transporte

| Carga | Requisito identificado | Vehículo propio | Vehículo de tercero | Estado |
|---|---|---|---|---|
| **Aves vivas** | Habilitación sanitaria del vehículo (Res. 723/2025): número pintado en ambos laterales y trasera ("HABILITACIÓN SENASA N°…", letras ≥ 8 cm según norma anterior), lavado y desinfección, DT-e firmado por el transportista como DJ | La empresa habilita cada unidad y es responsable del lavado/desinfección y del bienestar | Exigir habilitación vigente y constancia de lavado; el remitente/receptor sigue siendo responsable de recibir solo aves con DT-e | `[PVDP]` FTE-234 |
| **Producto refrigerado / congelado** | Habilitación del vehículo por categoría según caja (isotermo, con equipo de frío = categoría A), termómetro, hermeticidad, bandejas colectoras; condiciones higiénicas | Idem, más registros de temperatura | Exigir habilitación y registros; cláusula contractual de cadena de frío | `[PVDP]` FTE-235 |
| **Subproductos** (plumas, sangre, vísceras) | Vehículo habilitado para subproductos no aptos para consumo humano; estanco | Idem | Habitual: lo retira el receptor (rendering) con su vehículo habilitado | `[PVDP]` FTE-234 |
| **Residuos** (lodos, contenido GI, decomisos no valorizables) | Transportista y operador habilitados por la autoridad ambiental; manifiesto si son residuos especiales | Raro | Habitual | **[JURISDICCIÓN]** |

La **Res. SENASA 723/2025** se toma como el **marco consolidado** de habilitación sanitaria de medios de transporte de animales vivos y mercancías de origen animal (reemplazó a las Res. 503/2022, 735/2022 y 557/2024). **No se asume que todos los vehículos tengan requisitos idénticos:** la norma distingue tipos de unidad y carga y tiene **anexos y excepciones** que deben revisarse al desarrollar el módulo logístico (`13_logistica`, DPV-058, DPV-058). También creó un programa de certificación de diseños de vehículos 0 km (validez 5 años). El **Decreto 697/2026** asigna a SENASA la fiscalización alimentaria general; si eso modifica el control del transporte de alimentos fuera del ámbito de la Res. 723/2025 queda por confirmar (P-39).

## 8. Cadena de frío

| Aspecto | Qué se sabe | Tipo | Estado |
|---|---|---|---|
| Enfriamiento de carcasas | Obligatorio tras la evisceración, por inmersión (con control de absorción de agua) o por aire; temperatura objetivo y tiempo **no leídos** | Obligatorio | `[PVDP]` DPV-061 |
| Conservación refrigerada | Extracto: −2 a 2 °C con tolerancia ±2 °C | A confirmar | `[PVDP · contradictorio]` C5 |
| Congelado | Extracto: "no superior a −4 °C" (valor atípico; los destinos de exportación suelen exigir ≤ −18 °C) | A confirmar | `[PVDP · contradictorio]` C5 |
| Enfriamiento por aire | Extracto: pechuga ≤ 7 °C; **posible origen en normativa brasileña** (la búsqueda devolvió un documento de Brasil) | A confirmar | `[PVDP · origen dudoso]` |
| Almacenamiento | Cámaras con termómetro y registro; separación por tipo de producto | Obligatorio | `[PVDP]` |
| Transporte | Vehículos categoría con equipo de frío y termómetro (Res. 723/2025) | Obligatorio | `[PVDP]` |
| Registros de temperatura | Continuos en cámaras y túneles (registradores), en recepción y despacho; registros del Plan APPCC | Obligatorio como parte del APPCC regulatorio (Res. 205/2014); destinos pueden exigir más | `[PVDP]` |

**No se adopta ningún valor de temperatura** hasta leer el reglamento (DPV-098).

## 9. Rotulado y productos (impacto regulatorio, sin diseñar etiquetas)

| Producto | Cómo impacta la regulación | Estado |
|---|---|---|
| Pollo entero | Rótulo con número de establecimiento SENASA, producto registrado (CAPA), fechas; declaración de menudencias si las incluye | `[PVDP]` FTE-241/FTE-242 |
| Cortes | Cada corte y presentación se registra; denominaciones reglamentarias | `[PVDP]` |
| Menudencias | Productos propios con registro; alta perecibilidad | `[PVDP]` |
| **CMS** | Uso restringido (chacinados cocidos y conservas, según extracto); temperatura y plazo específicos; rotulado a verificar | `[PVDP]` FTE-185, DPV-074 |
| Elaborados (marinados, milanesas, chacinados, cocidos) | Rubros de habilitación adicionales; aditivos según CAA/reglamento; rotulado nutricional (CAA cap. V, Res. GMC 26/03) y eventual sellos de advertencia (Ley 27.642, citada de memoria) | `[PVDP]` |
| **Agua retenida** | Límite de absorción en enfriamiento por inmersión (~8 % según prensa) y método de control; posible declaración en rótulo | `[PVDP]` DPV-061 |
| Productos congelados | Denominación "congelado", temperatura de conservación, vida útil, eventual prohibición de recongelar | `[PVDP]` |
| Exportación | Idioma, número de planta, marca sanitaria, logos (Halal), requisitos por destino | [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md) |

El registro es **por producto y presentación** ante CAPA, por TAD, con **monografía de proceso**: cada nuevo producto implica trámite (FTE-241).

## 10. Trazabilidad (granja → despacho)

Requerimientos identificados: RENSPA y DT-e para mover aves (sin RENSPA vigente no se emite DT-e); registro del criador por lote con mortandad cargada en SIGSA antes del primer DT-e a faena (Res. 1699/2019); la Res. 593/2026 exige **trazabilidad documentada** para autorizar destinos de exportación; la UE exige atestación de no uso de antimicrobianos prohibidos (art. 118) (FTE-239, FTE-083, FTE-107; `[PVDP]`).

| Eslabón | Datos que deberían capturarse | Base |
|---|---|---|
| Granja | RENSPA, galpón, lote SIGSA, genética, fecha de alojamiento, origen del pollito (planta de incubación), alimento (fábrica, lote), medicamentos y vacunas con períodos de retiro, mortalidad, programa *Salmonella* | Obligatorio (RENSPA/registro del criador) + exigencia de destinos |
| Lote de faena | Fecha y hora de retiro de alimento (ayuno), captura, carga | Bienestar; buena práctica |
| Transporte | DT-e, vehículo habilitado, chofer, horarios de salida y llegada, DOA | Obligatorio (DT-e) |
| Recepción | Peso bruto/tara, conteo, espera, resultado ante mortem | Obligatorio (SIV) / buena práctica |
| Faena | Lote de faena ↔ lote de granja, hora, línea, decomisos por causa, temperatura de chiller, absorción | Obligatorio (SIV) / Plan APPCC |
| Producción | Lote de producción por producto y fecha, rendimiento, operarios/sector | Buena práctica / rótulo |
| Cámara | Ubicación, fecha/hora de ingreso, temperatura, congelado (túnel, tiempo) | Plan APPCC / exportación |
| Despacho | Cliente, remito, vehículo habilitado, temperatura de carga, precinto, certificado sanitario (exportación: SIGCER, contenedor) | Obligatorio (exportación) / buena práctica |

Recomendación de principio (no de sistema): **identificar el lote de faena con el lote SIGSA de la granja** desde el día 1; un sistema digital facilita la exportación ([`../17_exportacion/requisitos_planta_exportadora.md` §3](../17_exportacion/requisitos_planta_exportadora.md)).
