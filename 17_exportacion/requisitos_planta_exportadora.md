# Requisitos de una planta de faena avícola con orientación exportadora

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 · Relacionado: [`../16_normativa_senasa/README.md`](../16_normativa_senasa/README.md) (análisis normativo detallado realizado el 2026-09-30 en la sesión 09B; todo `[PVDP]`), [`mercados_por_pais.md`](mercados_por_pais.md), [`logistica_exportacion.md`](logistica_exportacion.md)

> **Alcance:** lista de requisitos que **pueden afectar el diseño desde el día 1**. No se selecciona maquinaria, proveedor, capacidad ni ubicación (fase 0). No se estima CAPEX.
> **Verificación:** las normas se identificaron por extractos de buscador; **ninguna fue leída en su texto original** en esta sesión. Donde se cita una norma "conocida pero no leída", se indica. El análisis normativo completo corresponde a `16_normativa_senasa` (DPV-007).
> **Nivel de habilitación objetivo:** es una decisión abierta (DEC-009). La columna "Categoría A" supone una planta con **habilitación SENASA** (tránsito federal), que es condición necesaria para exportar.

---

## 1. Categoría A — Requisitos obligatorios desde el inicio (planta con habilitación SENASA)

| Requisito | Contenido | Cómo afecta el diseño | Base | Estado |
|---|---|---|---|---|
| Habilitación SENASA del establecimiento | Reglamento de inspección de productos de origen animal; actualización por Res. SENASA 592/2026 (según 09B, deroga la **obligatoriedad reglamentaria del Director Técnico** —numerales 1.7 y 9.2—, sin perjuicio de profesionales responsables exigidos por otras normas, la operación o los clientes; `[PVDP]`, DPV-105) | Layout con flujos separados (zona sucia / limpia), materiales sanitarios, agua potable, vestuarios y barreras sanitarias, desagües, iluminación en puestos de inspección | Decreto 4238/68 (FTE-016) | [PVDP] |
| Tránsito federal | Permite vender entre provincias (probable necesidad si la planta abastece al AMBA desde otra provincia) | Mismo estándar que la habilitación SENASA | Glosario; DEC-009 | [PVDP] |
| Inspección veterinaria oficial | Inspección ante y post mortem por SENASA | Oficina y espacios para el servicio oficial; puestos de inspección en línea con iluminación y espacio; sala de decomisos | FTE-016 | [PVDP] |
| BPM y POES | Buenas prácticas y procedimientos operativos estandarizados de saneamiento | Superficies lavables, lavamanos, esterilizadores, circuitos de limpieza | Norma específica a verificar (DPV-007). **Actualización 2026-09-30 (09B):** BPM y POES obligatorios por Res. SENASA 233/1998 (FTE-231, `[PVDP]`) | [PVDP] |
| HACCP | Plan de análisis de peligros y puntos críticos de control | Puntos de control de temperatura (enfriado, cámaras), registros | Exigido por mercados de exportación; obligatoriedad nacional a verificar (DPV-007). **Actualización 2026-09-30 (09B):** el Plan APPCC es **obligatorio regulatorio** para establecimientos SENASA según la Res. SENASA 205/2014 (FTE-243, `[PVDP]`); los destinos agregan exigencias; excepciones en DPV-102 | [PVDP] |
| Bienestar animal en faena | Recepción, espera, descarga, colgado, aturdimiento y degüello | Andén de recepción cubierto y ventilado, zona de espera, diseño del colgado y del aturdimiento | Capítulo de bienestar animal del Decreto 4238/68 (FTE-016) | [PVDP] |
| Prohibición de antimicrobianos promotores de crecimiento | Aplica a toda la producción nacional | Afecta la granja y el alimento, no la planta; exige trazabilidad de medicamentos (Sigtrazavet) | Res. SENASA 445/2024 (FTE-109) | [PVDP] |
| Control de residuos (Plan CREHA) | Muestreo oficial de residuos y contaminantes | Toma de muestras en planta; registros de proveedores (granjas) | FTE-110 | [PVDP] |
| Trazabilidad | Lote de faena vinculado a granja de origen (RENSPA) y documentos de tránsito | Sistema de identificación de lotes desde la recepción hasta el despacho | FTE-107, FTE-109 | [PVDP] |
| Sanidad aviar de origen | Granjas registradas, programas de *Salmonella* y micoplasma, vigilancia de IAAP y ENC | Recepción solo de lotes con documentación sanitaria | FTE-015 | [PVDP] |
| Autocontrol microbiológico | Análisis de producto y superficies (laboratorio propio o tercero) | Sala de toma de muestras; decisión sobre laboratorio propio | Norma a verificar | [PENDIENTE DE VALIDACIÓN] |
| Cadena de frío | Enfriado de canales y conservación refrigerada a temperatura reglamentaria | Capacidad de enfriado (*chiller*) y cámaras dimensionadas para la producción | FTE-016 (parámetros no leídos) | [PENDIENTE DE VALIDACIÓN] |
| Ambiental, agua y efluentes | Habilitación provincial y municipal; tratamiento de efluentes | Planta de tratamiento; disponibilidad de agua | `11_agua_efluentes` | [PENDIENTE DE VALIDACIÓN] |

---

## 2. Categoría B — Requisitos necesarios solo para determinados mercados

| Requisito | Mercados | Contenido | Cómo afecta el diseño | Base | Estado |
|---|---|---|---|---|---|
| **Listado de la planta por destino** | Todos los de exportación | SENASA propone la planta según la Res. 593/2026 (BO 2026-07-08); el importador la acepta (UE: lista oficial; China: GACC; Japón: MAFF; Corea: MAFRA; Arabia Saudita: SFDA) | Cumplir el estándar del destino más exigente al que se aspire | FTE-083 | [PVDP] |
| Atestación de antimicrobianos (art. 118) | UE (desde 2026-09-03) | Garantía de que las aves nunca recibieron promotores ni antimicrobianos reservados a humanos | Trazabilidad completa granja–alimento–medicamentos | FTE-107 | [PVDP] |
| Control de *Salmonella* en origen y microbiología del producto | UE (Reg. (CE) 2160/2003 y 2073/2005); otros destinos con criterios propios | Programas en granja; muestreo de producto | Laboratorio y registros; posible necesidad de intervenciones en línea | Extractos (FTE-107) y normas conocidas no leídas | [PVDP] |
| Bienestar animal equivalente al Reg. (CE) 1099/2009 | UE | Atestación en el certificado | Aturdimiento, monitoreo y capacitación | Norma conocida, no leída | [PVDP] |
| Registro GACC y protocolo sanitario | China (cerrada) | Registro de la planta; etiquetado con número de registro; requisitos por producto (garras) | Sala de proceso y clasificación de garras; etiquetado | FTE-014, DPV-029 | [PVDP · débil] |
| **Certificación Halal** | Arabia Saudita, EAU, Qatar, Kuwait, Omán, Irak, Egipto, Malasia, Indonesia | Certificación emitida por un organismo reconocido por el país importador (sujeto a la normativa vigente); otros requisitos (matarifes, certificado por lote en Arabia Saudita) reportados por fuentes secundarias | Solo preservar la posibilidad de incorporarla (§3); no se diseña todavía | FTE-082, FTE-113, FTE-116, FTE-138 | [PVDP]; detalle pendiente (DPV-034) |
| Requisitos de sacrificio de aves para destinos Halal (aturdimiento, métodos admitidos) | Arabia Saudita, EAU y otros del Golfo | Fuentes secundarias reportan restricciones al aturdimiento en Arabia Saudita desde 2018; **no se verificó normativa oficial vigente** ni si se admite aturdimiento reversible | **Ninguno por ahora:** no se diseña una línea sin aturdimiento ni otra adaptación hasta validar requisitos | FTE-113, FTE-114, FTE-115 | [PENDIENTE DE VALIDACIÓN] (DPV-034) |
| Especificaciones de producto | Japón (deshuese de muslo), Medio Oriente (griller calibrado), China (grados de garras) | Calibres, pesos, presentación | Salas de deshuese y clasificación; balanzas de calibración | FTE-127, FTE-118, FTE-136 | [PVDP · débil] |
| Congelado y almacenamiento a −18 °C o menos | Toda exportación de ultramar | Túnel de congelado o IQF; cámaras de congelado | Capacidad de congelado y de almacenamiento para completar contenedores | FTE-135 | [PVDP · débil] |
| Empaque y rotulado por destino | Todos | Idioma, marca sanitaria, número de planta, fechas, logos Halal | Diseño de empaque; espacio de etiquetado | Práctica comercial | [PVDP · débil] |
| Certificaciones privadas (BRCGS, IFS, FSSC 22000) | Retail de UE, Reino Unido, Japón; grandes compradores | Norma privada auditada | Diseño higiénico, documentación | Práctica comercial; **no verificada por destino** | [PENDIENTE DE VALIDACIÓN] |
| Auditorías del país importador | UE (DG SANTE), China (GACC), Japón, Corea, Arabia Saudita | Visitas al sistema oficial y a plantas | Planta "auditable" en todo momento | FTE-108 (caso Brasil) | [PVDP] |
| Criterios de residuos propios | Japón, Corea, China | LMR distintos a los de la UE | Control de proveedores de alimento y medicamentos | No relevado | [PENDIENTE DE VALIDACIÓN] |

---

## 3. Categoría C — Requisitos convenientes para facilitar la expansión

| Recomendación de diseño (a evaluar, no decidida) | Por qué | Costo si se posterga | Estado |
|---|---|---|---|
| Diseño higiénico y de flujos al **estándar del destino más exigente previsible** (UE) desde el día 1 | Evita reformas para listar la planta; la UE está legalmente abierta | Reformas con la planta en operación | Hipótesis a validar (SUP-015) |
| Espacio reservado para **congelado (túnel/IQF) y cámaras de congelado ampliables** | La exportación y la valorización de partes exigen congelar y acumular lotes | Falta de espacio en el terreno o en la nave | Hipótesis |
| **Muelle de expedición para contenedores reefer** (andén con sello, pre-enfriado, conexiones) | Cargar el contenedor en planta evita reprocesos y rupturas de frío | Consolidación en frigoríficos de terceros | Hipótesis |
| **Diseño que preserve la posibilidad de incorporar procesos y certificaciones Halal** una vez definidos los mercados objetivo y sus requisitos específicos (por ejemplo, no bloquear con el layout la segregación de cámaras ni la trazabilidad por lote) | Mantiene abierta la opción del bloque del Golfo e Irak sin invertir sobre requisitos no validados | Posibles reformas si el layout la impide | DEC-012, DPV-034 |
| Salas separadas y ampliables para **deshuese, clasificación de garras y CMS** | Son las operaciones que más cambian el ingreso por ave | Pérdida de flexibilidad de asignación | Hipótesis |
| Espacio para una futura **línea de cocidos/elaborados** con separación crudo–cocido | Opción de largo plazo (Japón, UK, UE; mercado interno) | Nave nueva | Hipótesis |
| **Compartimento libre de IAAP** en granjas propias o integradas (Res. SENASA 484/2017) | Algunos importadores reconocen compartimentos y zonas: permite seguir exportando durante brotes | Imposible de aplicar retroactivamente sin reorganizar la base de granjas | FTE-015, FTE-097 [PVDP] |
| Trazabilidad **digital** por lote (granja → contenedor) | Exigida por la UE (antimicrobianos) y por Arabia Saudita (certificado por lote) | Sistemas en papel incompatibles | Hipótesis |
| Laboratorio de autocontrol propio o convenio con laboratorios de la red SENASA | Rapidez de liberación de lotes y respuesta a auditorías | Demoras y costos | Hipótesis |
| Energía de respaldo para frío | Evita pérdidas de producto congelado | Pérdida de stock | Hipótesis |
| Salida para subproductos (rendering propio o contratado) | Piso de valor y cumplimiento ambiental | Costo de disposición | Hipótesis |
| Oficinas para inspección oficial y auditores externos | Requisito práctico de las auditorías | Menor | Hipótesis |

---

## 4. Requisitos que más pueden condicionar el diseño desde el día 1

1. **Nivel de habilitación** (municipal/provincial vs SENASA): sin SENASA no hay exportación ni venta interprovincial (DEC-009).
2. **Estándar de diseño higiénico** (nacional vs UE).
3. **Capacidad de congelado y almacenamiento** (define si se pueden acumular lotes de exportación).
4. **Preservar la posibilidad de incorporar procesos y certificaciones Halal** una vez definidos los mercados objetivo y validados sus requisitos (DPV-034); no se diseña todavía ninguna línea especial.
5. **Salas de proceso para valorización** (deshuese, garras, CMS) y espacio para cocidos.
6. **Trazabilidad granja–planta–contenedor** y control de antimicrobianos en la base de granjas.
7. **Bioseguridad y compartimentación** de granjas propias o integradas.
8. **Logística de contenedores** (muelle, pre-frío, acceso de camiones).

Cada uno se traduce en CAPEX y OPEX que **se estimarán en fases posteriores** (`19_capex`, `20_opex`); aquí solo se identifican.
