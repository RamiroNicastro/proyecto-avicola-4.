# Propuestas de actualización de registros globales — sesión 12A (localización)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (incluye la auditoría metodológica final, §6) · Sesión en paralelo con 12B (Logística, `13_logistica`) y 12C (Layout/Obra civil, `09_layout_obra_civil`): **no se editaron** `00_gestion_proyecto/`, `25_fuentes/`, `13_logistica/` ni `09_layout_obra_civil/`. Este archivo contiene lo que debe incorporarse al consolidar las sesiones 12A–12C.

> **IDs provisionales:** `SUP-12A-##`, `DPV-12A-##`, `DEC-12A-##`, `FTE-12A-###`. Al consolidar, asignar el siguiente número libre de cada registro (al cierre de esta sesión los últimos eran **SUP-077, DPV-115, DEC-049 y FTE-268**) y reemplazar los IDs provisionales en `10_localizacion/` (búsqueda de texto `12A-`). Las fuentes provisionales están en [`fuentes_12A.csv`](fuentes_12A.csv) (mismas columnas que `25_fuentes/registro_fuentes.csv`). Si 12B o 12C proponen registros equivalentes (p. ej., distancias medidas o superficie por escala), **fusionar** en lugar de duplicar (regla 13).

---

## 1. `supuestos.md` — nuevos

| ID provisional | Supuesto | Área | Origen | Estado | Vinculado a | Observaciones |
|---|---|---|---|---|---|---|
| SUP-12A-01 | **Unidad de análisis regional:** 13 corredores (BA-AMBA, BA-NORTE, BA-OESTE, BA-INTERIOR, ER-SUR, ER-URUGUAY, ER-CENTRO, SF-SUR, SF-CENTRO, CBA-SUR, CBA-ESTE, CH-ESTE, CH-CENTRO), cada uno definido por un eje vial y un ecosistema, con un **centro de referencia** usado solo para medir distancias. Un corredor **no** es un sitio ni una recomendación | Localización | Analista | Vigente | DEC-003 | `10_localizacion/regiones_preliminares.md` §2. Río Negro como referencia secundaria fuera de la matriz |
| SUP-12A-02 | **Distancias viales a CABA de orden de magnitud** (centro de referencia → CABA): ~55 / 165 / 160 / 300 / 230 / 320 / 470 / 300 / 490 / 600 / 560 / 1.020 / 1.170 km (orden de la lista de SUP-12A-01). `[ESTIMACIÓN]` del analista **sin medición ni fuente**; estado `[PVDP]` en la matriz; el modelo **no** las usa en modo estricto | Localización / Logística | Analista | Vigente | DPV-12A-01 | Reemplazar por ruteo medido (coordinar con 12B). Solo para órdenes de magnitud y para la aritmética de t·km de `escenarios_localizacion.md` §3 |
| SUP-12A-03 | **Perfiles de ponderación ilustrativos** (peso por grupo, suma 100): A MERCADO (demanda 30, logística 12, …), B PRODUCCIÓN (producción primaria 25, alimento 15, …), C EQUILIBRADO, D EXPORTADOR (exportación 18, …). **Ninguno es el correcto**; sirven para mostrar sensibilidad | Localización | Analista | Vigente | DEC-12A-02 | `10_localizacion/pesos_localizacion.csv` (fuente única de los pesos) |
| SUP-12A-04 | **Umbrales del modelo:** cobertura mínima de peso para informar puntaje y entrar al orden = 75 %; alerta de faltantes si > 40 % de subcriterios sin dato; un subcriterio compara solo si tiene datos de ≥ 2 unidades de observación distintas (provincias o corredores según su nivel) y de ≥ 50 % de las regiones | Localización / Modelo | Analista | Vigente | DEC-12A-05 | Editables por línea de comandos; tests T04, T10, T11 |
| SUP-12A-05 | **Reparto del peso del grupo** en partes iguales entre sus subcriterios presentes en la matriz | Localización / Modelo | Analista | Vigente | SUP-12A-03 | Alternativa futura: pesos por subcriterio |
| SUP-12A-06 | **Normalización min-max** por defecto (1 = mejor; inversión para "menor es mejor"; empate = 1); `rango_fijo:a:b` opcional para evitar inversión de ranking. **Sin imputación**: un faltante aporta 0 a la cota inferior y 1 a la cota superior del puntaje | Localización / Modelo | Analista | Vigente | — | `10_localizacion/metodologia_localizacion.md` §5 |
| SUP-12A-07 | **Datos provinciales como proxy de corredor** (participación en la faena SENASA, plantas por provincia, límites de vuelco provinciales): se asignan a todos los corredores de la provincia con `NIVEL_DATO = PROVINCIA` y se advierte que no discriminan dentro de ella | Localización | Analista | Vigente | DPV-023 | Regla 18: no comparar universos distintos |
| SUP-12A-08 | **Escenarios de cliente ancla para sensibilidad logística:** S0 sin ancla (0 t/día), S1 ancla parcial (1,0–4,5 t/día; ESC-CON a ESC-BAS), S2 ancla fuerte (13,5–27 t/día; ESC-EXP a RED-300). Solo sensibilidad; **no** dimensionan ubicación ni planta | Localización / Demanda | Analista | Vigente | SUP-004, SUP-021, DPV-036 | `escenarios_localizacion.md` §3 |
| SUP-12A-09 | **Radios de levantamiento de datos:** 50 km (mano de obra, IAAP), 100 km (granjas), 150 km (maíz, fábricas de alimento), 200 km (incubadoras, façon), 300 km (mercado regional). Convenciones para relevar de forma homogénea; **no** son distancias reglamentarias ni límites de transporte | Localización | Analista | Vigente | DPV-046, DPV-054 | El orden de magnitud de viaje de aves vivas sigue siendo ~2–4 h (`03_produccion_primaria/transporte_aves.md` §4) |

## 2. `datos_por_validar.md`

### 2.1 Nuevos

| ID provisional | Dato requerido | Por qué importa | Fuente sugerida | Responsable | Prioridad / nivel |
|---|---|---|---|---|---|
| DPV-12A-01 | **Distancias y tiempos viales medidos** de cada centro de referencia a CABA, a los nodos portuarios de contenedores (Buenos Aires, Dock Sud, Zárate, Gran Rosario, Concepción del Uruguay u otros), a los CD de la red (cuando se conozcan) y proporción del trayecto en autopista/autovía | Reemplazar SUP-12A-02 (DEM-01, DEM-02, EXP-01, LOG-01) | Ruteo (IGN, Vialidad, FTE-12A-002/003); **módulo 12B** | Analista | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O8 |
| DPV-12A-02 | **Producción de maíz y soja por departamento/partido** y ubicación de plantas de molienda de soja | ALI-01, ALI-02 | SAGyP estimaciones (FTE-12A-001); cámaras de la industria aceitera | Analista | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O0 (escritorio) |
| DPV-12A-03 | **Riesgo hídrico regional** (superficie inundable, antecedentes de anegamiento) por partido/departamento | TER-03; insumo del gate condicional de riesgo hídrico (G-C1) | INA (FTE-12A-005), organismos provinciales | Analista | IMPORTANTE ANTES DE ELEGIR TERRENO · N2 · ola O8 |
| DPV-12A-04 | **Parques o áreas industriales que admiten frigorífico avícola** por corredor, con servicios (energía, gas, agua, vuelco) y lotes disponibles | TER-01; reduce riesgo de uso de suelo | Registro de parques industriales (FTE-12A-011), municipios | Promotor / Analista | IMPORTANTE ANTES DE ELEGIR TERRENO · N2 · ola O8 |
| DPV-12A-05 | **Eventos de IAAP georreferenciados 2023–2026** y zonas de control asociadas, por corredor | SAN-03 (exposición sanitaria); riesgo sanitario y de exportación | SENASA (FTE-12A-010) | Analista | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O0 |
| DPV-12A-06 | **Recursos humanos por corredor:** población de 18–64 años en 50 km, experiencia frigorífica/avícola local, escuelas técnicas y universidades, convenio y conflictividad laboral de referencia | RRH-01 a RRH-03; insumo de `18_recursos_humanos` | INDEC, municipios, gremios, plantas | Analista | IMPORTANTE ANTES DE INVERTIR · N2 · ola O8 |
| DPV-12A-07 | **Días/año con temperatura máxima ≥ 35 °C** (y humedad) por corredor | CLI-01; tecnología de galpón y energía de cooling | SMN (FTE-12A-004) | Analista | ÚTIL PARA OPTIMIZAR · N4 · ola O0 |
| DPV-12A-08 | **Población y densidad por partido/departamento** (Censo 2022) y población en radio de 300 km | DEM-04, TER-04 | INDEC (ampliar FTE-141 a nivel partido) | Analista | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O0 |
| DPV-12A-09 | **Superficie de terreno requerida por escala** (edificio, playas, tratamiento de efluentes por tecnología, servicios, retiros, reserva de expansión) | Comparar superficie disponible vs necesaria; hoy sin base (`terreno_ideal.md` §4) | **Módulo 12C**; `11_agua_efluentes` (tecnología de tratamiento); plantas de referencia | Analista | CRÍTICO ANTES DE ELEGIR TERRENO · N2 · ola O8 |

### 2.2 Anotaciones a registros existentes (sin borrar historia)

| Registro | Anotación propuesta (sesión 12A, 2026-10-01) |
|---|---|
| DPV-009 (acceso a fuentes) | Octava sesión con egress bloqueado: magyp.gob.ar, indec.gob.ar y un servicio de ruteo devolvieron `CONNECT 403` el 2026-10-01. Ningún dato de la matriz de localización pudo verificarse en primaria |
| DPV-018 (ubicación de la red) | Insumo de DEM-03 de la matriz de localización; sin el mapa de locales y CD, la cercanía a la red no se puntúa (SUP-12A-08) |
| DPV-023 (establecimientos por provincia) | Pedir los datos **georreferenciados** para contar granjas, incubadoras, fábricas y plantas por radio (TOF-01, ECO-03, SAN-01, ALI-03, TOF-02; códigos v1.1); faltan Buenos Aires y Chaco |
| DPV-027 (costos logísticos de exportación) | Agregar frecuencia de servicios reefer regulares por terminal (Zárate, Gran Rosario, Concepción del Uruguay) para EXP-01 (FTE-12A-014) |
| DPV-036 (logística de la red) | La arquitectura de distribución (CD vs 90 locales vs cross-dock) puede pesar más que la ubicación de la planta (`escenarios_localizacion.md` §3) |
| DPV-050 (alimento en zonas candidatas) | Insumo de ALI-03 y ALI-04 por corredor |
| DPV-052 / DPV-087 (energía; terreno y servicios) | Insumo de ENE-01 a ENE-03 por corredor; agregar indicadores de calidad de servicio de la distribuidora (FTE-12A-009) y precio de tierra apta como `[COTIZACIÓN]` (TER-02) |
| DPV-053 (agua en zonas candidatas) | Insumo de AGU-01 y AGU-02 por corredor (rúbrica en `criterios_localizacion.md` §5) |
| DPV-067 / DPV-106 (vuelco; normativa por candidata) | Límites de vuelco de ER, SF, Cba y Chaco para EFL-01 (hoy solo BA, FTE-259): sin al menos otra provincia el subcriterio es NO_COMPARABLE |
| SUP-014 (contacto en Chaco) | Tratado como factor NETWORK **no puntuable**, separado de los criterios físicos (`regiones_preliminares.md` §6; test T08) |

## 3. `decisiones_pendientes.md`

### 3.1 Nuevas

| ID provisional | Decisión | Prioridad | Depende de | Carpeta |
|---|---|---|---|---|
| DEC-12A-01 | **Adoptar la metodología de localización** en embudo (E0–E5) con matriz multicriterio por corredor, envolvente por faltantes sin imputación (no es intervalo de confianza) y sin ranking hasta cobertura suficiente | Media | DEC-003 | `10_localizacion` |
| DEC-12A-02 | **Definir el perfil de ponderación** (o rango de pesos) que reflejará la estrategia; decisión de los socios, no técnica | Alta (al llegar a E2) | Hitos H-A y H-B del plan de campo; DEC-011, DEC-020 | `10_localizacion` |
| DEC-12A-03 | **Definir los gates duros y condicionales de municipio/terreno** y sus umbrales (duros: uso de suelo, agua mínima, gestión legal de efluentes, energía indispensable; condicionales: riesgo hídrico, vecinos, subproductos, gas, potencia, calidad de agua, acceso) | Alta (antes de E4) | Escala (DEC-001), DEC-043, DPV-106 | `10_localizacion` |
| DEC-12A-04 | **Elegir la arquitectura de red**: R1 planta única vs R2 faena en zona productiva + CD/cross-dock/trozado en el AMBA. Son **arquitecturas**, no criterios de localización; comparar inversión, inventario, frío, doble manipulación, transporte primario, distribución secundaria y nivel de servicio (sin costos en esta fase) | Media | DEC-016, DEC-018, 12B | `10_localizacion` / `13_logistica` |
| DEC-12A-05 | **Adoptar los criterios de control del modelo** (cobertura 75 % con sensibilidad 60/75/90 %, faltantes 40 %, comparabilidad por criterio, umbral de nodo reefer EXP-04 ≥ 3) o modificarlos | Baja | SUP-12A-04 | `10_localizacion` |
| DEC-12A-06 | **Definir la lista corta de corredores** (2–4) para relevamiento dirigido en la ola O8 | Alta (después de H-A/H-B) | DEC-12A-02, DPV-018, DPV-048, DPV-047 | `10_localizacion` |

### 3.2 Anotación a DEC-003

> 2026-10-01 (12A, v1.1): metodología, 45 subcriterios monotónicos + 3 trade-offs, 13 corredores, gates duros/condicionales y modelo reproducible creados (`10_localizacion/`). **Sigue abierta**: con 0 de 624 celdas verificadas, el modelo no emite ranking en ningún perfil. Próximo paso: completar los DPV-12A de escritorio (ola O0) y, después de H-A/H-B, definir la lista corta (DEC-12A-06).

## 4. Fuentes

14 fuentes **identificadas y no consultadas** (FTE-12A-001 a FTE-12A-014) y, desde la v1.1, 3 fuentes oficiales **confirmadas o identificadas en revisión externa del proyecto, con lectura directa pendiente en este entorno** (FTE-12A-015 a FTE-12A-017, §6.4) en [`fuentes_12A.csv`](fuentes_12A.csv). Las fuentes usadas en la matriz son registros existentes: FTE-001, FTE-072 y FTE-259 (todas `[PVDP]`); el documento también cita FTE-035, FTE-040, FTE-047, FTE-057, FTE-081, FTE-097, FTE-099, FTE-134, FTE-157 y FTE-250. **No se agregaron cifras nuevas de fuentes externas.**

## 5. `estado_proyecto.md` — propuesta de fila y hito

- Tablero: Localización (`10`) → **Completado v1.0 como metodología y modelo** (13 corredores, 45 subcriterios monotónicos + 3 trade-offs, 14 grupos, 4 perfiles, 28 tests; **sin ubicación elegida; sin ranking por falta de datos en ningún umbral 60/75/90 %**) · Evidencia de campo: Pendiente · Síntesis: [`conclusiones_localizacion.md`](conclusiones_localizacion.md).
- Hito 2026-10-01: "Metodología de localización industrial (sesión 12A, en paralelo con 12B y 12C)".

---

## 6. Auditoría metodológica final (v1.1, 2026-10-01)

Cambios metodológicos sin rehacer el modelo, sin elegir ubicación y sin CAPEX/OPEX. Se mantienen la matriz, el principio de no completar faltantes y la decisión de no emitir ranking con evidencia insuficiente.

### 6.1 Supuestos nuevos o revisados

| ID provisional | Supuesto | Estado | Observaciones |
|---|---|---|---|
| SUP-12A-03 (revisado) | El peso del antiguo grupo PRODUCCION_PRIMARIA se reparte en **ECOSISTEMA_AVICOLA / EXPOSICION_SANITARIA / CLIMA**: A 4/3/1, B 13/9/3, C 6/4/2, D 6/6/2 (misma suma por perfil). Sigue siendo ilustrativo | Vigente | `pesos_localizacion.csv` |
| SUP-12A-04 (revisado) | El umbral de cobertura de 75 % es un **criterio de control del modelo / supuesto metodológico**, no un estándar de análisis multicriterio; se informa siempre la sensibilidad 60 / 75 / 90 % | Vigente | Test T24 |
| SUP-12A-07 (revisado) | Datos provinciales en dos tipos: `PROVINCIA_NORMA` (regla que rige en todo el territorio; se aplica a cada corredor) y `PROVINCIA_AGREGADO` (estadística; **no se usa para puntuar corredores** salvo autorización explícita y rotulada) | Vigente | Tests T18, T26 |
| SUP-12A-10 | Un criterio `NO_MONOTONICO` (trade-off) **nunca** recibe normalización lineal; sin función defendible registrada, se divide en componentes monotónicos o se analiza cualitativamente. Aplicado a la densidad de granjas (TOF-01), la concentración industrial (TOF-02) y la cercanía al borde urbano (TOF-03) | Vigente | Test T21 |
| SUP-12A-11 | La distancia al nodo portuario (EXP-01) solo es usable si ese nodo tiene **servicio reefer regular verificado** (EXP-04 ≥ 3 en la rúbrica 1–5) | Vigente | Test T27 |
| SUP-12A-12 | **Gates:** duro = incumplirlo vuelve el terreno legal o técnicamente inviable, y solo descarta con imposibilidad demostrada por escrito; condicional = resoluble con infraestructura, tratamiento, inversión, tercerización, mitigación o diseño. Se aplican a municipio/terreno; **nunca eliminan una región** | Vigente | Test T23; `criterios_localizacion.md` §4 |
| SUP-12A-13 | El rango [faltantes = 0; faltantes = 1] es una **envolvente de peor/mejor caso producida exclusivamente por la información faltante**; no es intervalo de confianza, probabilidad ni error estadístico; se informa siempre junto con la cobertura de información | Vigente | Test T25 |

### 6.2 Datos por validar nuevos y anotaciones

| ID | Dato / anotación | Para qué | Prioridad / nivel |
|---|---|---|---|
| DPV-12A-10 (nuevo) | **Por nodo portuario** (Buenos Aires, Dock Sud, Zárate, Gran Rosario, Concepción del Uruguay u otros): terminal de contenedores; enchufes y capacidad reefer; frecuencia de servicios; destinos; cut-off; costos; disponibilidad real | EXP-04 (y, a través de él, EXP-01) | IMPORTANTE ANTES DE ESTUDIAR EXPORTACIÓN DIRECTA · N3 · ola O9 (con 12B) |
| DPV-12A-11 (nuevo) | **Servicios avícolas especializados por corredor:** veterinarios y técnicos avícolas, contratistas de captura, transportistas de aves vivas, proveedores y mantenimiento de equipos de galpón | ECO-04 | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O4 |
| DPV-12A-12 (nuevo) | **Exposición sanitaria por corredor:** distancia mediana entre establecimientos avícolas comerciales (RENSPA georreferenciado), movimientos de tránsito de aves (DT-e) por departamento, humedales y concentraciones de aves silvestres | SAN-01, SAN-02, SAN-04 | IMPORTANTE ANTES DE LA LISTA CORTA · N2 · ola O0 (pedido a SENASA) |
| DPV-12A-09 (anotación) | 12C está generando una estimación conceptual de superficie en su rama (no leída desde 12A). En la reconciliación 12A–12C, reemplazar el estado genérico por el **rango conceptual de 12C + restricciones reales municipales y de terreno** | Superficie de terreno | — |
| DPV-009 (anotación) | Nueva prueba 2026-10-01: magyp.gob.ar y argentina.gob.ar/senasa sin respuesta desde el entorno; las fuentes FTE-12A-015 a 017 quedan "confirmadas en revisión externa; lectura directa pendiente" | — | — |

### 6.3 Decisiones

DEC-12A-03 y DEC-12A-04 fueron reformuladas en §3.1 (gates duros/condicionales; arquitecturas de red R1/R2). DEC-12A-02 incluye ahora el peso relativo entre ECOSISTEMA_AVICOLA y EXPOSICION_SANITARIA, que es una decisión estratégica (cuánto ecosistema se está dispuesto a cambiar por exposición sanitaria). DEC-12A-05 incluye el umbral del nodo reefer. Sin decisiones nuevas.

### 6.4 Fuentes oficiales incorporadas (en [`fuentes_12A.csv`](fuentes_12A.csv))

| ID provisional | Fuente | Universo y dato | Estado |
|---|---|---|---|
| FTE-12A-015 | SAGyP, "Faena Provincial 2024–2025" | **Faena habilitada por SENASA, 2024:** ER ~50,90 %; BA ~34,89 %; SF ~5,09 %; Cba ~4,49 %; RN ~2,41 % | Confirmado en revisión externa del proyecto; lectura directa pendiente en este entorno |
| FTE-12A-016 | SAGyP, "Faena Provincial 2025–2026" (portal actual) | Faena habilitada por SENASA, 2025–2026 | Identificada en revisión externa; no leída |
| FTE-12A-017 | SENASA, publicación del 2024-07-02 | **Actividad avícola:** casi 90 % en Entre Ríos y Buenos Aires (no es participación de faena) | Confirmado en revisión externa del proyecto; lectura directa pendiente en este entorno |

**Para la consolidación:** no mezclar FTE-12A-015 (2024) con FTE-001 (extracto 2025: ER 50,2; BA 35,4; SF 5,1; Cba 4,1; RN 2,5) sin verificar año y universo (regla 18). Otros documentos fuera de 12A (p. ej., `01_mercado/mercado_avicola_argentina.md` §3.1, que cita "Río Negro 2,5 %" del extracto 2025) quedan como están; al consolidar, conviene fecharlos y agregar la cifra oficial 2024 con su universo.
