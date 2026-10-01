# Plan de trabajo de campo — de datos pendientes a validación real

**Fecha:** 2026-09-30 · **Versión:** 1.0 · **Fase:** 0 (prefactibilidad) · Matriz: [`matriz_validacion_campo.csv`](matriz_validacion_campo.csv) · Guía de método: [`guia_recoleccion_evidencia.md`](guia_recoleccion_evidencia.md) · Data room: [`estructura_data_room_campo.md`](estructura_data_room_campo.md)

> **Pregunta central:** ¿qué información tenemos que conseguir **fuera de Internet** para pasar de prefactibilidad a una decisión de inversión?
> **Qué es este plan:** la priorización de los 115 datos por validar (DPV-001 a DPV-115, sin cambiar su numeración), los instrumentos para salir a buscarlos y el orden de trabajo.
> **Qué no es:** no investiga tecnologías nuevas, no construye modelos, no elige escala, localización, proveedor ni maquinaria, no solicita cotizaciones, no calcula CAPEX ni OPEX. **Ningún DPV se marca validado** y **ninguna decisión se cierra**.
> **Actualización (reconciliación de las sesiones 12, 2026-10-01):** se agregaron DPV-116 a DPV-145 (localización, logística y layout) a la matriz con nivel y ola (N2: 19, N3: 7, N4: 4); la matriz tiene ahora 145 DPV. Ninguno es N1: no cambian los hitos H-A / H-B, pero varios se suman a las olas O0 (escritorio), O3, O5, O7 y O8. Detalle en [`reconciliacion_sesiones_12.md`](reconciliacion_sesiones_12.md) §4.

---

## 1. Cómo leer la priorización

### 1.1 Niveles

| Nivel | Nombre | Criterio | Cantidad |
|---|---|---|---|
| **N1** | **Bloquea la escala o la inversión** | Sin este dato no se puede decidir si se invierte ni en qué rango de escala: capital real, demanda real, precios, abastecimiento, escala mínima | **18** |
| **N2** | **Necesario antes de diseñar o cotizar** | Hace falta antes del anteproyecto, del RFQ, de la localización y del CAPEX/OPEX que sostendrían una decisión de inversión | **53** |
| **N3** | **Necesario antes de operar** | No cambia la decisión de invertir, pero sí la ingeniería de detalle, los trámites, los contratos operativos o el arranque | **11** |
| **N4** | **Optimización posterior** | Mejora el modelo o abre opciones (exportación, rutas alternativas de subproductos); no condiciona la primera decisión | **33** |

**Relación con la etiqueta previa** (`CRÍTICO / IMPORTANTE / ÚTIL` en [`datos_por_validar.md`](datos_por_validar.md)): los niveles no la reemplazan; la etiqueta previa se conserva y se copia en la columna `OBSERVACIONES` de la matriz. Diferencias deliberadas:

- **Suben a N1** cuatro datos marcados "IMPORTANTE ANTES DE INVERTIR" — capital (DPV-001), precios (DPV-013), logística de la red (DPV-036) y condiciones comerciales (DPV-039) — porque sin ellos no se puede evaluar la inversión aunque la escala estuviera clara. También dos sin etiqueta: ubicación de los locales (DPV-018) y costo del pollo vivo (DPV-019).
- **Suben a N2** dos datos marcados "ÚTIL": desempeño productivo (DPV-044; +0,1 de FCR = +5,9 % de alimento, el principal costo) y horas netas por turno (DPV-082; fija el ritmo nominal a especificar).
- Los datos de **exportación** quedan en N4 (la exportación no forma parte del caso base, SUP-022), salvo los que condicionan el diseño: requisitos para listar una planta (DPV-024) y sacrificio Halal (DPV-034), en N2.

### 1.2 Tipos de evidencia (columna `TIPO_EVIDENCIA`)

`documento` (texto, reporte, lista de precios, norma) · `reunión` (entrevista con minuta) · `llamada` (relevamiento telefónico con registro) · `visita` (observación en sitio con hoja de visita) · `cotización` (precio ofrecido con condiciones) · `medición` (registro propio: góndola, ventas, pesadas, análisis). En la matriz, 69 DPV requieren algún documento, 60 una reunión, 26 una visita, 14 una medición, 13 una cotización y 11 una llamada (un DPV puede requerir varios tipos).

### 1.3 Qué indica cada columna de la matriz por DPV

Quién puede responderlo (`ACTOR`), cómo conseguirlo (`MÉTODO`), qué evidencia cuenta (`EVIDENCIA_REQUERIDA`), qué decisión desbloquea (`DECISIÓN_QUE_DESBLOQUEA`), qué pasa si no se consigue (`CONSECUENCIA_SI_NO_SE_OBTIENE`), con qué instrumento (`INSTRUMENTO`) y en qué ola del plan (`OLA`). Documentación completa en §9.

---

## 2. Qué bloquea hoy la decisión (los 18 datos N1)

Hoy la **demanda documentada es ~0**, el **capital no está comprometido** y **ningún costo ni precio proviene de campo**. Estos son los datos sin los cuales no hay decisión de inversión posible:

| Bloque | DPV | Dato | Quién lo tiene | Desbloquea |
|---|---|---|---|---|
| **Capital y gobierno** | DPV-001 | Monto, forma, etapas, plazo y retorno esperado del capital | Grupo inversor | DEC-010, DEC-007, DEC-008 |
| | DPV-038 | Relación inversor–red y reglas entre partes vinculadas | Grupo inversor | DEC-019, DEC-017 |
| **Red de supermercados** | DPV-002 | Acceso real y quién decide la compra | Inversor → compras de la red | DEC-001, DEC-014, DEC-018 |
| | DPV-018 | Lista y ubicación de los locales, CD y razones sociales | Inversor / red | DEC-009, DEC-016 |
| | DPV-003 | kg/semana comprados por producto y local (12 meses) | Compras de la red | DEC-001, DEC-014 |
| | DPV-037 | Mix, formato y estacionalidad | Compras de la red; góndola | DEC-005, DEC-014 |
| | DPV-085 | Refrigerado vs congelado | Compras de la red | Congelado y cámaras (×5) |
| | DPV-020 | Proveedor actual, contratos y problemas | Compras de la red; góndola | Ventana de entrada |
| | DPV-036 | Logística (CD o local, frecuencia, fee) | Logística de la red | DEC-016; costo de servir (×12) |
| | DPV-039 | Condiciones comerciales completas y plazo de pago | Compras de la red | Precio neto; capital de trabajo |
| **Otros canales y precios** | DPV-040 | Demanda de mayoristas, distribuidores, pollerías, gastronomía e industria | Esos actores | Partes excedentes; concentración |
| | DPV-013 | Precios por corte y canal | Mayoristas, red, góndola | Ingreso por ave |
| | DPV-070 | Precios de coproductos (alas, menudencias, cuello, carcasa) | Mayoristas, frigoríficos, industria | Ingreso total por ave |
| **Abastecimiento** | DPV-006 | Faena a façon y pollito disponibles | Frigoríficos; incubadoras | DEC-004, DEC-018 |
| | DPV-047 | Pollito BB: volumen, precio, calidad, contrato | Incubadoras | DEC-023; techo de escala |
| | DPV-048 | Productores integrables | Productores, técnicos, municipios | DEC-020 |
| | DPV-019 | Costo del pollo vivo y su estructura | Productores, asesores, integradores | DEC-020; margen |
| **Escala** | DPV-083 | Escala mínima eficiente en Argentina | Plantas existentes de distinto tamaño | DEC-001, DEC-033 |

**Lectura crítica:** 10 de los 18 datos N1 dependen, directa o indirectamente, de **una sola relación** (grupo inversor → red de supermercados). Si esa relación no abre la puerta a compras y logística, el proyecto pierde su hipótesis de cliente ancla y debe replantearse como una empresa que sale a competir en el mercado abierto (§5.3, hito H-A). DPV-083 solo es obtenible en parte en el campo: el umbral económico requiere CAPEX y OPEX, que no se calculan en esta fase.

---

## 3. Resumen de N2, N3 y N4

Detalle por DPV en la matriz. Agrupados por tema:

| Nivel | Tema | DPV |
|---|---|---|
| N2 | Demanda y comercial | 017, 041, 042, 043, 068, 071 |
| N2 | Producción primaria | 008, 023, 044, 046, 049, 050, 051, 054, 057, 059 |
| N2 | Planta y proceso (visitas) | 062, 067, 082, 088, 091, 092, 108, 114 |
| N2 | Proveedores (RFQ futuro) | 089, 095, 096, 097, 109 |
| N2 | Normativa y SENASA | 007, 024, 034, 061, 066, 074, 086, 090, 094, 098, 099, 101, 103, 107, 115 |
| N2 | Subproductos | 065, 072, 080, 111 |
| N2 | Sitio y servicios | 052, 053, 087, 106 |
| N2 | Documental de base | 009 |
| N3 | Antes de operar | 004, 056, 058, 060, 078, 100, 102, 104, 110, 112, 113 |
| N4 | Exportación | 015, 022, 025, 026, 027, 028, 029, 030, 031, 032, 033, 035 |
| N4 | Subproductos y partes (rutas alternativas) | 064, 073, 075, 076, 077, 079, 081 |
| N4 | Contexto estadístico y documental | 005, 010, 011, 012, 014, 021, 045, 055, 105 |
| N4 | Proceso y logística (afinar) | 063, 069, 084, 093 |
| N4 | Evento de mercado | 016 |

Condicionales: DPV-049 (pollo vivo spot) **sube a N1** si la etapa 0 elegida es faena a façon con aves compradas; DPV-051 y DPV-057 solo importan mientras se evalúe el modelo de granjas propias.

---

## 4. Actores a contactar

| Actor | Cantidad inicial | Instrumento | DPV principales | Ola |
|---|---|---|---|---|
| **Padre de Ramiro y grupo inversor** | 1 reunión (difícil de repetir) | [`cuestionario_maestro_inversores.md`](../24_inversores/cuestionario_maestro_inversores.md) · [`cuestionario_ejecutivo_inversores.md`](../24_inversores/cuestionario_ejecutivo_inversores.md) · [`minuta_reunion_inversores.md`](../24_inversores/minuta_reunion_inversores.md) | 001, 002, 018, 038 | O1 |
| **Compras y logística de la red** | 1–2 reuniones | [`cuestionario_supermercados.md`](../02_clientes_demanda/cuestionario_supermercados.md) | 003, 020, 036, 037, 039, 041, 078, 085 | O1 |
| Mayoristas y distribuidores | 5–8 | [`plan_validacion_comercial.md`](../02_clientes_demanda/plan_validacion_comercial.md) | 013, 040, 070 | O2 |
| Pollerías y carnicerías | 8–10 | idem | 013, 040, 070 | O2 |
| Gastronomía y catering | 3–5 | idem | 040 | O2 |
| Elaboradores e industria de chacinados | 3–5 | idem · [`cuestionario_subproductos.md`](../07_subproductos/cuestionario_subproductos.md) | 040, 071, 079 | O2 |
| **Frigoríficos avícolas** (incluye posibles plantas a façon, de distinto tamaño) | 3–5 visitas | [`guia_visita_planta.md`](../05_proceso_industrial/guia_visita_planta.md) | 006, 083, 054, 062, 067, 082, 088, 091, 092, 108, 114 | O3 |
| **Productores avícolas** (integrados e independientes) | 6–10 en 2 zonas | [`cuestionario_productores.md`](../03_produccion_primaria/cuestionario_productores.md) | 019, 044, 048, 049, 050 | O4 |
| Asesores técnicos y veterinarios avícolas | 2–3 | idem | 019, 056 | O4 |
| **Incubadoras** | 3–4 | [`cuestionario_incubadoras.md`](../15_incubacion/cuestionario_incubadoras.md) | 006, 047 | O4 |
| Rendering, graserías y operadores de residuos | 2–4 | [`cuestionario_subproductos.md`](../07_subproductos/cuestionario_subproductos.md) | 065, 072, 080, 111 | O5 |
| Pet food, traders y exportadores de partes | 3–5 | idem | 064, 073, 077, 081 | O5 |
| **SENASA** (regional o central) y asesor de habilitaciones | 1 reunión + 1 consulta | [`preguntas_senasa_ejecutivas.md`](../16_normativa_senasa/preguntas_senasa_ejecutivas.md) | 007, 024, 034, 086, 094, 099, 101, 107, 115 | O6 |
| Contador | 1 consulta | — | 043 | O2 |
| Proveedores de equipos y frío (sin pedir cotización) | exposición + consultas | [`plan_rfq.md`](../08_maquinaria/plan_rfq.md) | 089 (y luego 095–097, 109) | O7 |
| Municipios, distribuidoras, organismos hídricos y ambientales | por terreno | [`ficha_relevamiento_terreno.md`](../10_localizacion/ficha_relevamiento_terreno.md) | 052, 053, 087, 106 | O8 |

Las cantidades son **mínimos de arranque para aprender**, no muestras estadísticas. Un patrón se considera confirmado cuando se repite en fuentes independientes (§4 de la guía de evidencia).

---

## 5. Orden de trabajo

### 5.1 Criterio

El orden se fijó por **cuántas decisiones desbloquea cada ola** y por **dependencias**: una ola va antes si su resultado cambia qué hay que preguntar en las siguientes. No se valida todo a la vez.

| Ola | Qué | DPV en la ola | N1 que resuelve | Por qué en este lugar |
|---|---|---|---|---|
| **O0** | Preparación y trabajo sin contactos | 21 | — (adelanta 013, 020, 037, 070 por góndola) | No depende de nadie: data room, descargas de normas y manuales, relevamiento de góndola, ventas de la carnicería |
| **O1** | Inversores y red de supermercados | 12 | **10** (001, 002, 003, 018, 020, 036, 037, 038, 039, 085) | Es la ola que más decisiones desbloquea y la que puede cambiar el proyecto entero (capital y cliente ancla) |
| **O2** | Otros canales, precios y coproductos | 9 | 3 (013, 040, 070) | Diversifica la demanda y da el ingreso total por ave; **puede empezar en paralelo con O1** porque no depende del inversor |
| **O3** | Frigoríficos y plantas en operación | 18 | 2 (006, 083) | Define si existe una etapa 0 a façon y da los datos reales de proceso; las plantas son también la puerta a productores e incubadoras |
| **O4** | Producción primaria e incubación | 11 | 3 (019, 047, 048) | Cuántos pollitos y productores hacen falta depende del rango de demanda de O1–O2; las llamadas a incubadoras pueden adelantarse |
| **O5** | Subproductos no comestibles | 10 | — | Son regionales: conviene hacerlas con zonas preseleccionadas por O3–O4 |
| **O6** | SENASA y asesor de habilitaciones | 11 | — | La reunión rinde más si se lleva rango de escala, productos y alcance territorial del canal (de O1–O3) |
| **O7** | Proveedores de maquinaria y frío | 7 | — | El RFQ no se envía hasta tener rango de escala (hito H-B); antes, solo relevamiento sin cotizar |
| **O8** | Terrenos y servicios | 5 | — | Solo al iniciar el módulo de localización (DEC-003) |
| **O9** | Exportación | 11 | — | Posterior: la exportación no es parte del caso base |

El orden coincide en lo grueso con "primero demanda e inversores; después producción y frigoríficos; después subproductos; después SENASA; después maquinaria; después terrenos", con dos ajustes: **frigoríficos antes que productores** (la faena a façon habilita una etapa 0 sin planta propia y las plantas dan acceso a productores e incubadoras) y **otros canales en paralelo con la red** (no dependen del inversor y reducen la concentración).

### 5.2 Calendario orientativo

Semanas desde el inicio del trabajo de campo; es una **propuesta de ritmo**, no un compromiso. Supone una persona (Ramiro) con apoyo del padre para O1.

| Semana | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| O0 Preparación | ■ | ■ | ▪ | ▪ | ▪ | ▪ | ▪ | ▪ | | | | | | |
| O1 Inversores y red | ■ | ■ | ■ | ■ | ▪ | ▪ | | | | | | | | |
| O2 Otros canales | | ■ | ■ | ■ | ■ | ■ | ■ | ■ | | | | | | |
| O3 Frigoríficos | | | | ■ | ■ | ■ | ■ | ■ | ■ | ■ | | | | |
| O4 Producción e incubación | | | ▪ | ▪ | | ■ | ■ | ■ | ■ | ■ | ■ | ■ | | |
| O5 Subproductos | | | ▪ | | | | | ■ | ■ | ■ | ■ | ■ | ■ | ■ |
| O6 SENASA | | | | | | | | ■ | ■ | ■ | ■ | ■ | ■ | ■ |
| O7 Maquinaria (solo relevamiento) | | | | | | ▪ | ▪ | | | | | | | |

■ trabajo principal · ▪ tareas livianas (góndola continua, llamadas iniciales). La exposición **Avícola y Porcinos 2026** (Buenos Aires, 6–8 nov 2026; FTE-195) cae hacia la semana 6 si se empieza a principios de octubre: sirve para relevar presencia y servicio técnico de proveedores (DPV-089) y hacer contactos con plantas, **sin pedir cotizaciones** (DEC-049 sigue bloqueada por la fase).

### 5.3 Hitos de decisión del trabajo de campo

No son los *gates* de expansión G0–G3 de [`gates_expansion.md`](../23_plan_expansion/gates_expansion.md) (que se aplican entre etapas de una empresa en marcha); son puntos para decidir cómo sigue la validación. **No tienen umbrales numéricos**: los fija el promotor con la información de cada ola (igual que DEC-034).

| Hito | Cuándo | Preguntas que se contestan | Resultados posibles |
|---|---|---|---|
| **H-A — Capital y ancla** | Al cerrar O1 | ¿Hay capital con monto, forma y condiciones declarados por escrito? ¿La red abrió compras y logística y entregó datos? ¿En qué nivel de la escala de evidencia comercial quedó (E1–E6)? | Seguir con el plan · Reencuadrar (proyecto sin cliente ancla: O2 pasa a ser la validación principal) · Pausar hasta tener capital o acceso |
| **H-B — Rango de escala y abastecimiento** | Al cerrar O2–O4 | ¿Hay demanda documentada (categoría A o B) para algún rango? ¿Hay pollito, productores o façon para ese rango? ¿El costo del pollo vivo y los precios dejan margen? ¿Existe una etapa 0 posible (DEC-018)? | Habilitar la reunión con SENASA con anteproyecto, el RFQ (O7) y la localización (O8) · Volver a O1–O2 · Recomendar etapa 0 antes de planta |
| **H-C — Insumos para decidir invertir** | Al cerrar O5–O8 | ¿Están los N2 necesarios para CAPEX, OPEX y modelo financiero? | Iniciar los módulos 19–21 (no en esta sesión) |

### 5.4 Qué puede empezar inmediatamente

Sin esperar a nadie (37 DPV marcados `INICIO_INMEDIATO = Sí` en la matriz; los principales):

1. **Coordinar la reunión con el padre de Ramiro y el grupo inversor** con el cuestionario ejecutivo (DPV-001, 002, 018, 038).
2. **Relevamiento de góndola** en 10–20 locales de la red y de la competencia: productos, marcas, precios al público, refrigerado/congelado, packaging, definición de cortes (DPV-013, 017, 020, 037, 068, 070). Planilla en [`plan_validacion_comercial.md` §6](../02_clientes_demanda/plan_validacion_comercial.md).
3. **Registro de ventas de pollo de la carnicería familiar** durante 4–8 semanas y copia de su habilitación (DPV-004, 104).
4. **Primeras llamadas** a mayoristas y pollerías del AMBA (DPV-040), a incubadoras (DPV-006, 047) y a plantas de rendering (DPV-065, 080).
5. **Descarga manual de documentos** que el entorno de análisis no puede abrir (DPV-009): Decreto 4238/68 actualizado, cap. XX y XXXII, Res. SENASA 205/2014, 368/2003, 723/2025, 591–593/2026, normativa de granjas, manuales Cobb y Ross, Anuario Avícola (DPV-005, 010, 045, 046, 058, 059, 061, 066, 074, 090, 098, 102, 105).
6. **Consulta al contador** sobre el tratamiento impositivo de la carne aviar (DPV-043).
7. **Armar el data room** con la convención de nombres ([`estructura_data_room_campo.md`](estructura_data_room_campo.md)).

---

## 6. Instrumentos

| Archivo | Uso |
|---|---|
| [`guia_recoleccion_evidencia.md`](guia_recoleccion_evidencia.md) | Qué es validar, jerarquía de evidencia, cómo tomar notas, qué no prometer (leer antes de cualquier contacto) |
| [`../24_inversores/cuestionario_maestro_inversores.md`](../24_inversores/cuestionario_maestro_inversores.md) | Preparación completa de la reunión con inversores |
| [`../24_inversores/cuestionario_ejecutivo_inversores.md`](../24_inversores/cuestionario_ejecutivo_inversores.md) | 20 preguntas para llevar a la reunión |
| [`../24_inversores/minuta_reunion_inversores.md`](../24_inversores/minuta_reunion_inversores.md) | Plantilla para registrar la reunión |
| [`../02_clientes_demanda/cuestionario_supermercados.md`](../02_clientes_demanda/cuestionario_supermercados.md) | Reunión con compras y logística de la red (existente) |
| [`../02_clientes_demanda/plan_validacion_comercial.md`](../02_clientes_demanda/plan_validacion_comercial.md) | Validación de demanda por actor y escala de evidencia comercial E1–E6 |
| [`../03_produccion_primaria/cuestionario_productores.md`](../03_produccion_primaria/cuestionario_productores.md) | Productores y registro de 6–12 crianzas |
| [`../15_incubacion/cuestionario_incubadoras.md`](../15_incubacion/cuestionario_incubadoras.md) | Incubadoras y proveedores de pollito BB |
| [`../05_proceso_industrial/guia_visita_planta.md`](../05_proceso_industrial/guia_visita_planta.md) | Visitas a frigoríficos y hoja de observaciones |
| [`../07_subproductos/cuestionario_subproductos.md`](../07_subproductos/cuestionario_subproductos.md) | Rendering, pet food, traders, compradores de carcasa y menudencias |
| [`../16_normativa_senasa/preguntas_senasa_ejecutivas.md`](../16_normativa_senasa/preguntas_senasa_ejecutivas.md) | Primera reunión con SENASA (versión corta) |
| [`../08_maquinaria/plan_rfq.md`](../08_maquinaria/plan_rfq.md) | Secuencia futura de RFQ y plantilla de comparación de ofertas (no se envía) |
| [`../10_localizacion/ficha_relevamiento_terreno.md`](../10_localizacion/ficha_relevamiento_terreno.md) | Ficha por terreno para el futuro módulo de localización |
| [`estructura_data_room_campo.md`](estructura_data_room_campo.md) | Dónde y cómo guardar la evidencia |

---

## 7. Cómo se registra el avance

1. **Antes del contacto:** buscar en la matriz los DPV que cubre el actor; llevar el instrumento correspondiente.
2. **Dentro de las 24 h:** completar la minuta u hoja de visita, guardarla en el data room con su código y registrar el contacto como fuente en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (`tipo_fuente = entrevista` para reuniones, llamadas y visitas; `cotizacion` para precios ofrecidos; valores admitidos en [`../25_fuentes/bibliografia.md`](../25_fuentes/bibliografia.md); sin datos personales sensibles, ver data room §5).
3. **Actualizar la matriz:** `ESTADO`, `FECHA` (del cambio de estado), `RESULTADO` (una línea con el dato y su clasificación `[VERIFICADO]` / `[ESTIMACIÓN]` / `[SUPUESTO]` / `[COTIZACIÓN]`), `FUENTE_DOCUMENTAL` (código del documento en el data room y FTE).
4. **Actualizar los registros centrales** solo cuando el estado cambia: [`datos_por_validar.md`](datos_por_validar.md) (estado y FTE), [`supuestos.md`](supuestos.md) si un supuesto se confirma o cae, [`decisiones_pendientes.md`](decisiones_pendientes.md) si una decisión queda habilitada.

**Estados de la matriz:** `NO INICIADO` → `CONTACTADO` → `REUNIÓN AGENDADA` → `EN VALIDACIÓN` → `VALIDADO` / `NO CONSEGUIDO` / `CONTRADICTORIO`.

| Estado | Cuándo usarlo |
|---|---|
| NO INICIADO | Nadie fue contactado para este dato |
| CONTACTADO | Hubo un primer contacto (llamada, mensaje) sin reunión fijada |
| REUNIÓN AGENDADA | Hay fecha de reunión, visita o entrega de documento |
| EN VALIDACIÓN | Hay información parcial o de una sola fuente; falta la evidencia requerida |
| VALIDADO | Se obtuvo la `EVIDENCIA_REQUERIDA` completa y está en el data room. Solo entonces el registro central pasa a `Validado` |
| NO CONSEGUIDO | Se agotaron los actores razonables; queda como supuesto explícito y riesgo |
| CONTRADICTORIO | Dos fuentes confiables dicen cosas incompatibles; se registra la contradicción y se busca una tercera |

`VALIDADO` exige la evidencia de la columna `EVIDENCIA_REQUERIDA`; una respuesta verbal favorable **no** alcanza (guía de evidencia §3).

---

## 8. Riesgos del propio trabajo de campo

| Riesgo | Cómo se ve | Contramedida |
|---|---|---|
| Sesgo de confirmación | Anotar solo lo que favorece al proyecto | Registrar también las respuestas negativas; la matriz tiene `NO CONSEGUIDO` y `CONTRADICTORIO` |
| Confundir cercanía con evidencia | "Nos conocen, van a comprar" | Escala E1–E6; el vínculo con el inversor aumenta el riesgo de concentración, no la certeza |
| Una sola reunión con inversores | Salir sin respuestas clave | Cuestionario ejecutivo ordenado por prioridad; pedidos concretos al final |
| Promesas implícitas | Un productor o proveedor entiende que hay compromiso | Presentación estándar y lista de "qué no prometer" (guía §6) |
| Confidencialidad | Datos de la red o de plantas que circulan | Data room fuera del repositorio público; NDA si lo piden (data room §5) |
| Pedir secretos comerciales | Una planta corta la relación | Guía de visita: órdenes de magnitud, no números internos |
| Anclarse en una zona por contactos | El contacto en Chaco o en otra región define la ubicación | Regla de localización del proyecto: los contactos son ventaja cualitativa, no criterio |
| Validar demasiado a la vez | Muchos contactos, pocas minutas completas | Olas y cantidades iniciales acotadas |

---

## 9. Documentación de `matriz_validacion_campo.csv` (regla 15)

Tabla **curada** (no generada por un modelo). Una fila por DPV (115 filas, DPV-001 a DPV-115, numeración sin cambios). Codificación UTF-8; separador de campos coma; los valores múltiples dentro de una celda se separan con punto y coma; no contiene cifras ni fórmulas.

| Columna | Contenido | Valores |
|---|---|---|
| `ID_DPV` | ID del registro central | DPV-001 … DPV-115 |
| `DATO` | Resumen del dato (el texto completo sigue en `datos_por_validar.md`) | Texto |
| `PRIORIDAD` | Nivel de este plan | N1, N2, N3, N4 (§1.1) |
| `ACTOR` | Quién puede responderlo | Texto; varios con `;` |
| `MÉTODO` | Cómo conseguirlo | Texto |
| `TIPO_EVIDENCIA` | Tipo de obtención | documento, reunión, llamada, visita, cotización, medición |
| `EVIDENCIA_REQUERIDA` | Qué debe existir para marcarlo `VALIDADO` | Texto |
| `DECISIÓN_QUE_DESBLOQUEA` | DEC, SUP o módulo que habilita | Texto con IDs |
| `CONSECUENCIA_SI_NO_SE_OBTIENE` | Qué pasa si no se consigue | Texto |
| `INSTRUMENTO` | Cuestionario o guía a usar | Ruta relativa a la raíz del repositorio |
| `OLA` | Ola del plan (§5.1) | O0 … O9 |
| `INICIO_INMEDIATO` | Si puede empezar sin depender de otra ola | Sí / No |
| `ESTADO` | Estado del trabajo de campo | Siete estados de §7; hoy todos `NO INICIADO` |
| `FECHA` | Fecha del último cambio de estado (AAAA-MM-DD) | Alta: 2026-09-30 |
| `RESPONSABLE` | Quién lo lleva | Padre de Ramiro + Ramiro · Ramiro · Analista · otros |
| `RESULTADO` | Dato obtenido con su clasificación (regla 4) | Vacío hasta obtenerlo |
| `FUENTE_DOCUMENTAL` | Código del documento en el data room y FTE | Vacío hasta obtenerlo |
| `OBSERVACIONES` | Etiqueta previa de prioridad y notas | Texto |

**Estado de registro vs estado de campo:** los DPV con estado `En curso` en el registro central (DPV-005, 008, 015, 018, 022) lo están por trabajo de escritorio; en la matriz figuran `NO INICIADO` porque ningún actor de campo fue contactado todavía.

**Control:** 115 filas, 18 columnas constantes, IDs únicos y consecutivos, estados dentro de los siete admitidos.
