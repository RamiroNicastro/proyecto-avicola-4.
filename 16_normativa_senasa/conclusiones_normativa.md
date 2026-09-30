# Conclusiones — hoja de ruta regulatoria (terreno → exportación)

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B (paralela) · Base: [`mapa_regulatorio.md`](mapa_regulatorio.md), [`habilitacion_planta.md`](habilitacion_planta.md), [`requisitos_sanitarios.md`](requisitos_sanitarios.md), [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md), [`subproductos_normativa.md`](subproductos_normativa.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv), [`ruta_critica_habilitacion.md`](ruta_critica_habilitacion.md), [`preguntas_senasa.md`](preguntas_senasa.md), [`guia_ramiro.md`](guia_ramiro.md), [`fuentes_09B.csv`](fuentes_09B.csv), [`actualizaciones_gestion_09B.md`](actualizaciones_gestion_09B.md)

> **Pregunta central:** ¿qué habilitaciones, registros, condiciones sanitarias y controles necesita el proyecto desde el terreno hasta exportar?
> **Respuesta corta:** una cadena de **cuatro niveles** (local → SENASA tránsito federal → autorización SENASA por destino → listado/aceptación del importador), más **habilitaciones locales** que dependen de la ubicación, **registros por producto y por vehículo**, **programas sanitarios** (BPM, POES y **Plan APPCC/HACCP obligatorios** por norma SENASA, también para mercado interno; los destinos agregan exigencias) y **certificaciones de destino** (Halal, atestaciones UE). Nada de esto está verificado en texto primario.
> **No es asesoramiento jurídico. No se selecciona localización, maquinaria ni proveedores.** Acceso primario bloqueado (séptima sesión, DPV-009): **ninguna norma leída en original; 0 datos `[VERIFICADO]`.**

---

## 1. Mapa de autoridades

| Nivel | Autoridades | Competencia central para el proyecto |
|---|---|---|
| Nacional | **SENASA** (habilitación, SIV, CAPA, transporte, exportación, alimentos para animales; desde el Decreto 697/2026, registro y fiscalización del sistema alimentario general), Ministerio de Salud (criterios y CAA), SAGyP, ARCA-Aduana, Cancillería, SRT/ENARGAS | Norma sanitaria única del establecimiento (Decreto 4238/68) |
| Provincial **[JURISDICCIÓN]** | Sanidad/bromatología (habilitación provincial alternativa), ambiente, recursos hídricos, bomberos, trabajo/aparatos a presión, energía | Radicación, agua, vuelco, residuos |
| Municipal **[JURISDICCIÓN]** | Uso de suelo, construcción, habilitación comercial/industrial, tránsito, olores | Terreno y convivencia urbana |
| Extranjero / privado | Autoridades de destino, certificadoras (Halal, BRCGS, FSSC), OAA | Listados, auditorías, certificados |

Detalle: [`mapa_regulatorio.md` §2](mapa_regulatorio.md).

## 2. Ruta de habilitación

Nivel objetivo (DEC-009) → terreno apto **[JURISDICCIÓN]** → anteproyecto y consulta a SENASA → proyecto ejecutivo → aprobaciones locales y ambientales → solicitud SIGTrámites (planos, DJ de capacidad en kg, documentación) → obra → inspección → **número de establecimiento con rubros** (**plazo real: dato a consultar** con SENASA y plantas habilitadas recientemente; no se adopta ningún plazo de fichas) → registro de productos en CAPA → operación con SIV → autorización de destinos (Res. 593/2026) → listados. Detalle: [`habilitacion_planta.md` §3](habilitacion_planta.md).

## 3. Principales requisitos SENASA

1. **Decreto 4238/68, cap. XX (aves, mod. Res. 553/2002):** norma de diseño del matadero avícola; hay que leer el **texto actualizado**.
2. **Condiciones edilicias:** materiales sanitarios, desagües, iluminación de inspección, lavamanos y esterilizadores, vestuarios, **separación sucio/limpio** y flujos sin cruce; oficina del SIV; sala de decomisos.
3. **Inspección veterinaria oficial permanente:** ante mortem por lote, post mortem en línea, decomisos, dictamen; el operador ejecuta el destino.
4. **Agua potable** (CAA art. 982 y ss.) con análisis y registros; agua caliente; uso de agua no potable/reúso **por consultar**.
5. **Enfriamiento** con control de **absorción de agua** (~8 % según prensa) y **temperaturas** de conservación **no verificadas** (extractos contradictorios: no se adoptan).
6. **Trazabilidad:** RENSPA + DT-e + lote SIGSA en origen; lote de faena → producción → cámara → despacho.
7. **Transporte:** Res. 723/2025 (reemplazó 503/2022, 735/2022 y 557/2024): vehículos propios **y** de terceros habilitados.
8. **Registro de cada producto y rótulo** en CAPA (TAD).
9. **Bienestar animal:** cap. XXXII; manual SENASA (espera 30 min–3 h; ayuno ≤ 12 h —carácter normativo por confirmar—); aturdimiento previo.
10. **APPCC/HACCP:** Plan APPCC **obligatorio** para establecimientos SENASA que faenen, elaboren, fraccionen o depositen alimentos, salvo excepciones de SENASA (Res. 205/2014, cap. XXXI del Decreto 4238/68, `[PVDP]`). No es un requisito exclusivamente exportador.
11. **Novedades 2025–2026:**
    - **Decreto 697/2026** (BO 2026-08-03): reorganiza el Sistema Nacional de Control de Alimentos; SENASA concentra registro, control y fiscalización; registro único y base única de datos. **No se concluye** que derogue o reemplace el régimen de frigoríficos del Decreto 4238/68; convivencia probable, a confirmar (P-39; [`mapa_regulatorio.md` §6](mapa_regulatorio.md)).
    - **Res. 592/2026:** eliminó la **obligación reglamentaria** de Director Técnico; eso no implica que el proyecto no requiera profesionales responsables o de calidad/inocuidad por operación, otras normas o clientes.
    - **Res. 233/2026:** elimina en diversos trámites la exigencia de **presentar** habilitaciones locales ante SENASA; **no** elimina uso de suelo, habilitación municipal ni requisitos ambientales: la empresa sigue obligada ante provincia y municipio.
    - **Res. 593/2026:** procedimiento único de autorización de destinos; las autorizaciones ya no vencen automáticamente a los dos años mientras se mantengan las condiciones y siguen dependiendo del país importador; no es habilitación automática de la futura planta.
    - **Res. 723/2025:** marco consolidado de habilitación de transporte; requisitos distintos por tipo de vehículo, con anexos y excepciones a revisar en el módulo logístico.
    - **Ley 22.375:** continúa figurando en el corpus normativo oficial; su interacción con las reformas 2025–2026 y con el Decreto 697/2026 se verifica con SENASA (P-42).

## 4. Programas sanitarios

| Programa | Condición |
|---|---|
| BPM | **Obligatorio** (Res. 233/1998; CAA) |
| POES | **Obligatorio**, escrito, firmado y presentado a SENASA (Res. 233/1998) |
| **APPCC/HACCP regulatorio** | **Obligatorio** (Res. SENASA 205/2014), incluido mercado interno, salvo excepciones de SENASA (P-43) |
| Exigencias APPCC de destinos | **Adicionales** para exportar (microbiología, verificación, auditorías) |
| ISO 22000 / FSSC 22000 / BRCGS / IFS | **Certificaciones privadas voluntarias**, según comprador |
| Halal | Voluntario; **obligatorio para destinos que lo exigen** |

## 5. Exportación

Escalera de siete peldaños: planta SENASA → país abierto → producto autorizado → planta autorizada para el destino (Res. 593/2026) y listada si corresponde → certificaciones adicionales → comprador → operación (SIGCER, Aduana). **Mercado abierto ≠ planta habilitada.** Detalle: [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md).

## 6. Subproductos

Cuatro destinos regulatorios (alimentario, alimentación animal, industrial/fertilizante, residuo). CMS solo para cocidos (Res. 368/2003); harinas y pet food con habilitación de alimentos para animales (Res. 1415/1416/2024); prohibición para rumiantes (Res. 1389/2004); **decomisos como residuo hasta verificar**. Detalle: [`subproductos_normativa.md`](subproductos_normativa.md).

## 7. Puntos que dependen de provincia / municipio

Uso de suelo; categoría y aptitud ambiental; permiso de agua; permiso de vuelco y límites; residuos y operadores; olores; tránsito de camiones; habilitación comercial/industrial; bomberos; energía y gas; aparatos a presión; **existencia de un régimen provincial de faena** (depende de la aplicación actual de la Ley 22.375, de la provincia y del reparto de competencias del Decreto 697/2026). La Res. 233/2026 no suprime ninguno de estos requisitos locales. Plantilla comparativa: [`habilitacion_planta.md` §5](habilitacion_planta.md). **No se completó ninguna provincia** (sin candidatas, DEC-003).

## 8. Ruta crítica

14 reglas de precedencia en [`ruta_critica_habilitacion.md` §1](ruta_critica_habilitacion.md). Las tres más costosas de ignorar: **no comprar terreno sin verificar uso de suelo, agua y vuelco**; **no cerrar el layout sin leer el reglamento y consultar a SENASA**; **no asumir exportación sin conocer, por destino, producto autorizado y listado**. Decisiones irreversibles: terreno, nivel de habilitación, estándar higiénico de la obra, separación de zonas, reserva de espacio, método de enfriamiento, planta de efluentes.

## 9. Preguntas para SENASA

45 preguntas (41 vigentes; 4 reemplazadas por las prioritarias) en un bloque prioritario y 7 temáticos + guía para asesores locales: [`preguntas_senasa.md`](preguntas_senasa.md). **Prioritarias (§0):** P-39 (Decreto 697/2026 ↔ Decreto 4238/68), P-40 (organismo que habilita cada rubro), P-41 (documentación local que ya no se presenta vs. que sigue siendo obligatoria), P-42 (aplicación actual de la Ley 22.375), P-43 (excepciones al APPCC), P-44 (plazo real anteproyecto → habilitación operativa), P-45 (revisión de anteproyecto). Siguen siendo importantes P-12 (SIV), P-19/P-20 (agua retenida y temperaturas), P-24 (Res. 593/2026), P-30 (decomisos).

## 10. Principales documentos primarios pendientes

| # | Documento | Para qué | Registro propuesto |
|---|---|---|---|
| 1 | **Decreto 4238/68 — texto actualizado**: índice oficial, cap. XX completo, capítulos generales de construcción, inspección, cámaras, graserías, transporte, rotulado; cap. XXXII | Base de diseño | DPV-09B-01 (FTE-016, FTE-192, FTE-09B-23) |
| 2 | Res. SENASA 553/2002 | Modificaciones del cap. XX | DPV-09B-01 |
| 3 | Aplicación actual de la **Ley 22.375** | Régimen provincial alternativo | DPV-09B-03 |
| 3b | **Decreto 697/2026** (texto completo) | Convivencia con el Decreto 4238/68; registro único; base única | DPV-09B-15 |
| 4 | **Res. SENASA 233/2026** (anexo de trámites alcanzados) | Documentación local en el trámite de faena | DPV-09B-04 |
| 5 | Res. SENASA 592/2026 y 591/2026 | Cambios 2026 y normas derogadas | DPV-09B-12 |
| 6 | **Res. SENASA 593/2026** | Requisitos de autorización de destinos | DPV-024 / DPV-031 (existentes) |
| 7 | **Res. SENASA 233/1998** | BPM y POES | DPV-007 |
| 8 | **Res. SENASA 205/2014** (APPCC) y manuales complementarios | Contenido del Plan APPCC y excepciones | DPV-09B-07 |
| 9 | **Res. SENASA 723/2025** | Transporte | DPV-09B-10 / DPV-058 |
| 10 | CAA arts. 982 y ss. + requisitos de agua del reglamento | Agua | DPV-09B-08 |
| 11 | Numeral de enfriamiento/absorción de agua y temperaturas | Frío y rótulo | DPV-061 / DPV-09B-02 |
| 12 | Manual SENASA de bienestar en faena de aves y lagomorfos | Recepción y aturdimiento | DPV-09B-11 |
| 13 | Res. 368/2003 (CMS), 1415/1416/2024, 1389/2004 | Subproductos | DPV-066 / DPV-074 / DPV-09B-06 |
| 14 | Normativa ambiental, hídrica y municipal por candidata | Terreno | DPV-09B-14 |

## 11. Qué debe aprender Ramiro

Resumen simple en [`guia_ramiro.md`](guia_ramiro.md): qué es SENASA; tránsito federal; habilitación del establecimiento (por rubros); habilitación para exportar (escalera); inspección veterinaria (ante/post mortem, decomisos); BPM; POES; HACCP; trazabilidad; por qué la normativa va **antes** del diseño.

## 12. Archivos creados y modificados

**Creados (`16_normativa_senasa/`):** `mapa_regulatorio.md`, `habilitacion_planta.md`, `requisitos_sanitarios.md`, `exportacion_y_certificaciones.md`, `subproductos_normativa.md`, `matriz_regulatoria.csv` (64 requisitos), `ruta_critica_habilitacion.md`, `preguntas_senasa.md`, `guia_ramiro.md`, `conclusiones_normativa.md`, `actualizaciones_gestion_09B.md`, `fuentes_09B.csv` (25 fuentes).
**Modificado:** `16_normativa_senasa/README.md` (índice y documentación de los CSV, regla 15).
**No modificados (sesión paralela):** `00_gestion_proyecto/`, `25_fuentes/registro_fuentes.csv`, `25_fuentes/bibliografia.md`. Las propuestas de actualización están en [`actualizaciones_gestion_09B.md`](actualizaciones_gestion_09B.md).

## 13. Control de calidad y evaluación

| Control | Resultado |
|---|---|
| Fuente primaria antes que prensa | Se buscó primero SENASA/Infoleg/BO/digesto: **todos bloqueados**; se usaron fichas oficiales vía extracto y prensa como complemento identificado (FTE-09B-11 y FTE-09B-22 son prensa, categoría C) |
| Extracto de buscador = PVDP | Sí: 37 requisitos PVDP, 15 por consultar a SENASA, 12 dependientes de jurisdicción; **0 "VERIFICADO EN PRIMARIA"** |
| Vigencia normativa comprobada | **No** (imposible sin texto): se registraron 6 puntos abiertos (C1–C6) y se detectaron normas **reemplazadas** (Res. 503/2022 → 723/2025; sistema de destinos 2010 → 593/2026; Director Técnico derogado) |
| Habilitación local ≠ federal ≠ exportadora | Explícito en todos los archivos |
| Mercado abierto ≠ planta habilitada | Escalera de 7 peldaños |
| Obligatorio vs buena práctica | Columna propia en la matriz y en tablas de requisitos |
| Nación / provincia / municipio | Columna "JURISDICCION"; marca **[JURISDICCIÓN]** |
| Sin selección de localización, maquinaria ni proveedores | Cumplido |
| Sin valores numéricos no verificados adoptados | Temperaturas, frecuencias de análisis y **plazos de habilitación no adoptados** (corrección 2026-09-30: el plazo de la ficha de trámite ya no se usa como referencia) |
| Sin modificar registros globales | Cumplido |

**Corrección normativa puntual (2026-09-30, misma sesión):** APPCC reclasificado como obligatorio regulatorio (Res. 205/2014); incorporado el Decreto 697/2026; Ley 22.375 reformulada como vigente en el corpus oficial; aclaraciones sobre Res. 233, 592 y 593/2026 y 723/2025; plazos retirados; 7 preguntas prioritarias.

**Evaluación: MEDIA como estructura, BAJA como evidencia normativa.** El mapa, la escalera, la matriz, la ruta crítica y las preguntas son completos y accionables, y la sesión detectó cambios normativos de 2025–2026 que afectan el diseño y los trámites. Pero **ningún texto normativo fue leído**, siguen abiertas la convivencia entre el Decreto 697/2026 y el Decreto 4238/68, la aplicación práctica de la Ley 22.375 y la documentación local del trámite, y los valores técnicos (temperaturas, iluminación, agua caliente, frecuencias) siguen sin conocerse. **Sirve para preparar la reunión con SENASA y ordenar la selección de terreno; no sirve para diseñar la planta ni para estimar plazos o costos de habilitación.**
