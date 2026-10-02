# Estructura organizacional — funciones, ubicación y organigramas por nivel

**Fecha:** 2026-10-01 · **Versión:** 1.1 (sesión 14A, en paralelo con 14B; auditoría de unidades) · Fase 0

> **Pregunta:** ¿qué funciones necesita la empresa, quién las cubre (interno, externo, compartido), dónde trabaja cada persona y cómo cambia la estructura al crecer?
> **No** se elige escala, automatización, turnos, modalidad de limpieza, mantenimiento ni flota; **no** se calculan salarios ni OPEX. Las cantidades salen de [`modelo_rrhh.py`](modelo_rrhh.py) y se analizan en [`dotacion_por_escala.md`](dotacion_por_escala.md).
> **Clasificación:** estructura y asignación de funciones `[SUPUESTO]` de trabajo (SUP-124, SUP-136); ninguna es recomendación.

---

## 1. Principios de diseño

1. **Función ≠ persona ≠ puesto de tiempo completo.** Toda función necesaria existe en todas las escalas; lo que cambia es si la cubre una persona dedicada, una persona que acumula roles (rol compartido) o un tercero. Tercerizar **retira personal interno pero no borra la función**: queda un responsable interno que la contrata y la verifica (test R04 del modelo).
2. **No inflar la estructura chica.** En 2.500 aves/día un gerente general cubre también lo comercial y lo administrativo-financiero; el gerente de operaciones cubre la jefatura de producción; un técnico líder cubre la jefatura de mantenimiento. Un rol combinado se expresa como **dedicación en FTE** (0,5 de un rol), no como una persona más; el número de personas de nómina que resulta queda PENDIENTE hasta validar el factor de cobertura (v1.1).
3. **Calidad independiente de producción.** El responsable de calidad e inocuidad no reporta a quien es medido por volumen; en escalas chicas reporta al gerente general, en la escalada se vuelve gerencia.
4. **Producción primaria: sólo coordinación.** No se cuenta personal de granjas de terceros (integrados o proveedores de pollo vivo); se cuentan coordinación, veterinaria, técnicos de campo y planificación ([`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md)).
5. **Zonas higiénicas mandan sobre la polivalencia.** Una persona de zona sucia no pasa a zona limpia dentro de la jornada sin el circuito de cambio previsto ([`../05_proceso_industrial/zonificacion_higienica.md`](../05_proceso_industrial/zonificacion_higienica.md)); la polivalencia se diseña **dentro** de cada zona (DEC-071).
6. **La inspección oficial no es dotación de la empresa.** El servicio veterinario oficial (SENASA) realiza ante y post mortem; cuántos inspectores y eventuales auxiliares requiere cada línea y quién los provee y paga **no está leído en la norma** (DPV-090, DPV-101): queda PENDIENTE, no se rellena.

## 2. Mapa de funciones

Códigos de modalidad: **I** interno · **C** rol compartido · **E** externo/tercerizable · **P** PENDIENTE (dato faltante). Zonas: S sucia · EV evisceración · L limpia · F frío/expedición · SP subproductos · T transversal (recorre zonas con circuito de cambio) · O oficinas · R ruta · G granja/campo.

### 2.1 Operación industrial (personal directo, por turno)

| Función | Qué hace | Zona | Driver de dotación | Modalidad | Cambia con automatización |
|---|---|---|---|---|---|
| Recepción, descarga y colgado | Pesaje, descarga de cajones o módulos, colgado, lavado de cajones | S | aves/h (colgado manual en todas las escalas, 09A) | I | Descarga: sí (módulos); colgado: casi no |
| Faena | Control de aturdido, degüello y repaso, escaldado, desplumado, corte de patas/cabeza, transferencia | S | aves/h | I | Mucho (degüello, patas, transferencia) |
| Evisceración | Apertura, extracción, menudencias, lavado, presentación para inspección | EV | aves/h | I | **Muy alto** (manual → automático) |
| Enfriamiento y clasificación | Operación del chiller/túnel de aire, escurrido, calibrado | L | aves/h | I | Clasificación: sí |
| Trozado y deshuese | Cortes, deshuese, trimming | L | kg/h según mix (config. A/B/C) | I | Sí, pero el trimming sigue siendo humano |
| Empaque | Embolsado, bandeja, rotulado, control de peso | L | kg/h comestible | I | Sí |
| Cámaras, congelado y expedición | Ingreso a cámaras, túneles, preparación de pedidos, carga | F | t/día | I | Poco |
| Subproductos y decomisos | Manejo, contenedores, despacho a receptores | SP | t/día de sólidos | I | Sí (vacío/bombas) |
| Limpieza operativa en turno | Pisos, derrames, recipientes, limpieza intermedia | T | aves/h | I (siempre) | Poco |
| Limpieza y sanitización post-producción | Desarme, lavado, espuma, desinfección, preoperacional | T | m² de salas de proceso (12C) × complejidad de equipos | I / E / híbrida (DEC-067) | **Aumenta** (más equipos que desarmar) |

### 2.2 Soporte industrial

| Función | Qué hace | Zona | Modalidad | Nota |
|---|---|---|---|---|
| Mantenimiento mecánico | Preventivo y correctivo de línea, transportadores, desplumadoras, evisceradoras | T | I / E / mixto (DEC-068) | Ver [`mantenimiento_y_servicios.md`](mantenimiento_y_servicios.md) |
| Electricidad | Tableros, motores, iluminación, media tensión | T | I / E | Media tensión casi siempre externa |
| Frío | Sala de máquinas, cámaras, túneles | T | I / E | Refrigerante sin decidir (DEC-046); con amoníaco la competencia técnica es específica (DPV-121) |
| Utilities | Caldera/agua caliente, aire comprimido, agua, tratamiento de efluentes | T | I / E | Operan más horas que la línea |
| Automatización / PLC | Programación, sensores, balanzas de línea | T | E en escalas chicas; I en automático ≥ 10.000 | Crece con la automatización |
| Control de calidad operativo | Controles en recepción, línea, temperaturas, empaque; registros del APPCC | T | I (por turno) | Ver [`calidad_inocuidad.md`](calidad_inocuidad.md) |
| QA / inocuidad / APPCC / documentación | Plan APPCC, POES, BPM, auditorías, reclamos, documentación | O | I | APPCC obligatorio (Res. SENASA 205/2014, `[PVDP]`) |
| Trazabilidad | Lote de granja ↔ lote de faena ↔ producto ↔ cliente | O | I / C | |
| Laboratorio | Autocontrol microbiológico y fisicoquímico | O | E (base) / I (opción) | DEC-065 |
| Inspección oficial | Ante/post mortem, decomisos, dictamen | EV | **Externo oficial — P** | DPV-090, DPV-101 |
| Higiene y seguridad laboral, medicina laboral | Programa HyS, ART, exámenes, capacitación | T | E en chicas; I + E en grandes | Horas mínimas por norma PENDIENTE (DPV-149) |
| Lavandería y ropería | Ropa por color de zona | personal | I / E | 12C dejó abierto propio vs tercerizado |

### 2.3 Logística

| Función | Modalidad | Nota |
|---|---|---|
| Planificación y tráfico (programación de cosecha, despacho, viajes) | I / C | |
| Recepción de insumos y depósito (envases, químicos, repuestos de consumo) | I / C | |
| Administración de expedición (remitos, DT-e, documentación sanitaria) | I / C | |
| Carga física y cámaras | I | Contada en operación industrial (directos) |
| Choferes de aves vivas | **Sólo si la flota es propia** (DEC-056) | Flota mínima de 12B con capacidad de **escenario** |
| Choferes de producto terminado | Sólo si la flota es propia | **PENDIENTE**: capacidad de camión, distancia y modelo de distribución no definidos (DPV-084, DPV-036, DEC-016) |
| Cuadrillas de captura en granja | Integrado o contratista | **PENDIENTE** (DPV-054); no se cuenta |

### 2.4 Producción primaria (sólo coordinación)

| Función | Integración (DEC-020 B) | Compra de pollo vivo (DEC-020 C) |
|---|---|---|
| Coordinación de integrados / abastecimiento | I (C en 2.500) | I (C en 2.500) |
| Veterinaria | I (C en 2.500) | I parcial (recepción, bienestar, sanidad de proveedores) |
| Técnicos de campo | 1 cada 10–20 granjas equivalentes (SUP-133) | No |
| Planificación de crianza (pollito BB, alimento, cosecha) | I desde 5.000 | No |
| Personal de granjas | **No se cuenta** (terceros) | **No se cuenta** |

### 2.5 Administración

Compras · ventas / ejecutivos de cuenta · administración (facturación, cobranzas, pagos) · finanzas, contabilidad y tesorería · recursos humanos (liquidación, selección, capacitación) · sistemas y datos. En 2.500 aves/día varias son roles compartidos o servicios externos (contador, liquidación de sueldos, sistemas). **Ventas no escala con las aves** sino con canales y clientes ([`../02_clientes_demanda/`](../02_clientes_demanda/README.md)): la tabla del modelo es un piso de trabajo.

### 2.6 Dirección

| Rol | Startup / asset-light | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Gerente general | ✔ (+ comercial, adm./fin.) | ✔ (+ comercial, adm./fin.) | ✔ | ✔ | ✔ |
| Operaciones / planta | — (control del façonier) | ✔ (+ jefe de producción) | ✔ (+ jefe de producción) | ✔ | ✔ |
| Comercial | GG | GG | ✔ | ✔ | ✔ |
| Administración y finanzas | GG + contador | GG + contador | Jefe adm. | ✔ | ✔ |
| Calidad e inocuidad | Jefe de calidad | Jefe (reporta al GG) | Jefe (reporta al GG) | Jefe (reporta al GG) | ✔ gerencia |

La Res. SENASA 592/2026 derogó la **obligación reglamentaria** del Director Técnico (FTE-229, `[PVDP]`); eso no implica que no se necesiten profesionales responsables de calidad e inocuidad por operación, clientes o destinos de exportación ([`../16_normativa_senasa/habilitacion_planta.md`](../16_normativa_senasa/habilitacion_planta.md)).

## 3. Organigramas por nivel

Los tres niveles son **configuraciones organizacionales**, no escalas elegidas. Cantidades en FTE o puestos, nunca headcount de nómina (PENDIENTE): escenario de referencia del modelo (productividad media; [`dotacion_por_escala.md`](dotacion_por_escala.md) §2).

### 3.1 Nivel 1 — Startup / asset-light (faena a façon, DEC-004 / DEC-018)

La empresa compra pollo vivo o integra productores, hace faenar a un tercero habilitado y vende. Conserva: especificación de producto, control de calidad en la planta del façonier, abastecimiento, logística y comercial. **Escenario organizacional de referencia:** 10–36 FTE internos según volumen (2.500–20.000 aves/día equivalentes), desagregados por bloque y por dependencia del volumen en [`dotacion_por_escala.md`](dotacion_por_escala.md) §4; no se asume que cada incremento de aves requiera automáticamente esa estructura. Las horas industriales (23–84 FTE) son del façonier.

```
Gerente general (+ comercial + adm./fin. en volúmenes chicos)
├── Calidad e inocuidad
│   ├── Jefe de calidad (especificaciones, auditoría al façonier, reclamos)
│   └── Control de calidad propio en la planta del façonier (1–2)
├── Abastecimiento / producción primaria
│   ├── Coordinador de integrados o de compra de pollo vivo
│   ├── Veterinario (compartido o externo)
│   └── Técnicos de campo (sólo con integración)
├── Logística (planificación, depósito, expedición — roles compartidos)
└── Administración (ventas, administración, compras, RR. HH. — roles compartidos)
```

### 3.2 Nivel 2 — Planta pequeña / media (referencia 2.500–10.000 aves/día)

```
Gerente general
├── Gerente comercial (desde 5.000; antes, el GG)
│   └── Ventas / ejecutivos de cuenta
├── Gerente de operaciones / planta
│   ├── Jefe de producción (desde 10.000; antes, el gerente de operaciones)
│   │   ├── Supervisores de línea (1 cada ~15–30 directos)
│   │   │   ├── Zona sucia: recepción, colgado, faena
│   │   │   ├── Evisceración
│   │   │   ├── Zona limpia: enfriamiento, clasificación, trozado, empaque
│   │   │   └── Cámaras, expedición, subproductos
│   │   └── Supervisor de saneamiento → cuadrilla de limpieza (propia, tercerizada o híbrida)
│   ├── Jefe de mantenimiento (desde 5.000; antes, técnico líder)
│   │   └── Técnicos (mecánica, electricidad, frío/utilities); pañol desde 10.000
│   ├── Logística: planificación y tráfico, depósito, expedición
│   └── Producción primaria: coordinador, veterinario, técnicos de campo, planificación
├── Jefe de calidad e inocuidad (reporta al GG, no a producción)
│   ├── Control de calidad operativo (por turno)
│   ├── Analista APPCC / documentación; trazabilidad
│   └── Laboratorio externo (toma de muestras interna)
└── Administración y finanzas (jefe; gerencia desde 10.000)
    ├── Administración, compras, finanzas, sistemas
    └── RR. HH. (+ HyS y medicina laboral externos)
```

### 3.3 Nivel 3 — Planta escalada (referencia 20.000 aves/día; con dos cuadrillas si la ecuación de 24 h y la jornada lo permiten)

Cambios respecto del nivel 2: gerencia de calidad e inocuidad; gerencia de administración y finanzas; jefes de turno si hay dos cuadrillas; especialista en automatización si la línea es automática; HyS interno además del servicio externo; sistemas y datos con 2 personas; técnicos de campo para ~32 granjas equivalentes. **No** se agregan capas intermedias (subgerencias, coordinadores de área) sin evidencia de que hagan falta.

```
Gerente general
├── Gerencia comercial ── ventas, atención de cuentas, exportación (cuando exista)
├── Gerencia de operaciones
│   ├── Jefe de producción ── jefes de turno (si 2 cuadrillas) ── supervisores por zona
│   ├── Supervisor de saneamiento ── cuadrilla de limpieza (o contratista)
│   ├── Jefe de mantenimiento ── técnicos por especialidad (mecánica, eléctrica, frío/utilities, automatización) + pañol
│   ├── Logística ── planificación, depósito, expedición, (choferes si flota propia)
│   └── Producción primaria ── coordinador, veterinarios, técnicos de campo, planificación de crianza
├── Gerencia de calidad e inocuidad ── jefe de calidad, control operativo, APPCC, trazabilidad, (laboratorio propio, opción)
└── Gerencia de administración y finanzas ── administración, compras, finanzas, sistemas y datos, RR. HH., HyS
```

## 4. Cómo cambia la estructura al crecer

| Al pasar de… | Se separa / agrega | Por qué |
|---|---|---|
| Asset-light → planta propia | Toda la operación industrial, mantenimiento, limpieza, control operativo, gerente de operaciones | La empresa pasa a operar activos |
| 2.500 → 5.000 | Gerente comercial, jefe de mantenimiento, analista APPCC dedicado, planificación y depósito dedicados | Los roles compartidos superan la capacidad de una persona |
| 5.000 → 10.000 | Jefe de producción, gerente adm./fin., pañol, HyS interno, sistemas, trazabilidad dedicada | Volumen, cantidad de puestos (> ~100 equivalentes) y de equipos |
| 10.000 → 20.000 | Gerencia de calidad, especialista en automatización (si automático), duplicación de logística y administración | Exportación potencial, auditorías, activos automáticos |
| 1 → 2 cuadrillas | Jefes de turno, segunda línea de supervisores, cobertura técnica en ambos turnos | Cada turno necesita mando y técnico presentes |

Lo que **no** crece proporcionalmente (FTE): dirección (2 → 5), supervisión (3,5 → 4,5 con una cuadrilla), administración (3,5 → 14,5). Lo que crece más que proporcionalmente con la automatización: mantenimiento y la relación indirecta/directa ([`turnos_y_productividad.md`](turnos_y_productividad.md) §4).

## 5. Decisiones abiertas que esta estructura no toma

DEC-067 (limpieza), DEC-068 (mantenimiento), DEC-069 (organización de la jornada), DEC-070 (estructura de dirección inicial), DEC-071 (polivalencia entre zonas), DEC-072 (HyS y medicina laboral), DEC-073 (lavandería); y las existentes DEC-004, DEC-018, DEC-020, DEC-036, DEC-037, DEC-056, DEC-065. Detalle en [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md).
