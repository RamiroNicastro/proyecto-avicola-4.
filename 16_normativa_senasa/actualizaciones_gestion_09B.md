# Propuestas de actualización de registros globales — sesión 09B

**Fecha:** 2026-09-30 · Sesión 09B (normativa y habilitaciones), **paralela** a otras sesiones.

> Esta sesión **no modificó** `00_gestion_proyecto/`, `25_fuentes/registro_fuentes.csv` ni `25_fuentes/bibliografia.md`. Las altas y anotaciones se proponen aquí para consolidarlas después.
> **Numeración provisoria:** para evitar colisiones con sesiones paralelas se usan IDs con sufijo `09B` (`SUP-09B-##`, `DEC-09B-##`, `DPV-09B-##`, `FTE-09B-##`). Al consolidar, asignar el siguiente número libre de cada registro (últimos vistos al iniciar: SUP-060, DEC-036, DPV-087, FTE-193) y **reemplazar** los IDs provisorios en todos los archivos de `16_normativa_senasa/` (búsqueda global de `-09B-`).

---

## 1. Supuestos (`supuestos.md`) — altas propuestas

| ID provisorio | Supuesto | Categoría | Origen | Estado | Relacionado | Notas |
|---|---|---|---|---|---|---|
| SUP-09B-01 | El análisis normativo toma como **caso de referencia** una planta con **habilitación SENASA de tránsito federal**, porque es condición para vender fuera de la provincia de radicación y para exportar. **No es una decisión** | Normativa | Analista | Vigente | DEC-009, SUP-015 | La alternativa provincial se mantiene abierta hasta verificar la Ley 22.375 (DPV-09B-03) |
| SUP-09B-02 | Ninguna norma citada se considera **vigente** hasta leer su texto actualizado; las derogaciones y reemplazos detectados en prensa (Res. 592/2026, 593/2026, 723/2025, 233/2026) se usan como hipótesis de vigencia | Normativa | Analista | Vigente | DPV-009 | Regla 16 |
| SUP-09B-03 | No se adopta ningún valor técnico reglamentario (temperaturas, lux, temperatura de esterilizadores, frecuencia de análisis) hasta leer el reglamento | Normativa / Industrial | Analista | Vigente | DPV-09B-01, DPV-09B-02 | Extractos contradictorios (C5) |

## 2. Decisiones pendientes (`decisiones_pendientes.md`)

### 2.1 Altas propuestas

| ID provisorio | Decisión | Prioridad | Depende de | Carpeta | Estado | Notas |
|---|---|---|---|---|---|---|
| DEC-09B-01 | Definir **cuándo y con quién** hacer la reunión técnica de habilitación (SENASA regional/central y/o asesor de habilitaciones) y con qué material (anteproyecto conceptual, escenarios de escala, lista de productos) | Alta | DEC-003 (región), DEC-009 | `16_normativa_senasa` | Abierta | Preguntas listas en `16_normativa_senasa/preguntas_senasa.md`; no seleccionar asesor en Fase 0, solo relevar |
| DEC-09B-02 | Definir si los **elaborados** se producen en la planta SENASA (rubros propios) o si la carnicería familiar funciona como canal/elaboradora bajo habilitación local | Media | DPV-09B-09, DEC-005 | `16_normativa_senasa` / `06_productos` | Abierta | Afecta rubros a solicitar (P-03) y alcance comercial (venta interprovincial) |

### 2.2 Notas a decisiones existentes

- **DEC-009** (nivel de habilitación): agregar "2026-09-30 (09B): mapa de habilitaciones y escalera exportadora en `16_normativa_senasa/`. Vigencia de la Ley 22.375 y del régimen provincial **no verificada** (DPV-09B-03). Res. 233/2026 cambia la documentación del trámite, no la obligación local."
- **DEC-012** (estándar UE / Halal): agregar "Ruta crítica R4 (`16_normativa_senasa/ruta_critica_habilitacion.md`): el estándar de obra civil es decisión irreversible; P-27 pregunta si SENASA evalúa proyectos contra requisitos de destino antes de construir."
- **DEC-003** (localización): agregar "Plantilla jurisdiccional de 14 temas en `16_normativa_senasa/habilitacion_planta.md` §5; completar por candidata."
- **DEC-027** (destino de subproductos): agregar "Marco normativo en `16_normativa_senasa/subproductos_normativa.md`; decomisos como residuo hasta verificar (P-30)."

## 3. Datos por validar (`datos_por_validar.md`)

### 3.1 Altas propuestas

| ID provisorio | Dato | Impacto | Fuente posible | Responsable | Estado | Fuentes | Notas |
|---|---|---|---|---|---|---|---|
| DPV-09B-01 | **Decreto 4238/68 texto actualizado**: índice oficial por capítulos, cap. XX completo (con Res. 553/2002), capítulos generales de construcción, inspección, cámaras, graserías, transporte y rotulado; cap. XXXII | Base de diseño sanitario de la planta | argentina.gob.ar/normativa (texto actualizado); digesto SENASA | Analista (descarga manual si la red sigue bloqueada) | Pendiente | FTE-016, FTE-192, FTE-09B-04, FTE-09B-23 | Contradicción C3 (30 capítulos vs cap. XXXII) |
| DPV-09B-02 | **Temperaturas vigentes** de enfriamiento, conservación refrigerada, congelada y transporte de carne aviar | Dimensionamiento de frío | Reglamento; SENASA | Analista | Pendiente | FTE-09B-17 | Extractos contradictorios y de origen dudoso (C5) |
| DPV-09B-03 | **Vigencia de la Ley 22.375** y existencia de régimen provincial de faena en regiones candidatas | Alternativa de planta provincial (DEC-009) | Infoleg; SENASA; asesor legal | Analista / asesor | Pendiente | FTE-09B-10, FTE-09B-24 | Contradicción C2 |
| DPV-09B-04 | **Alcance de la Res. SENASA 233/2026** sobre el trámite de habilitación de plantas de faena | Orden de trámites | Boletín Oficial; SENASA | Analista | Pendiente | FTE-09B-02, FTE-09B-11, FTE-09B-21 | Contradicción C1 |
| DPV-09B-05 | **Dotación, costos y tasas** del servicio de inspección veterinaria; aranceles de habilitación, modificación, registro de productos y certificación | OPEX/CAPEX; turnos | SENASA | Analista | Pendiente | — | P-12, P-36 |
| DPV-09B-06 | Normativa de **graserías/digestores**, requisitos para proveedores de materia prima de alimentos para animales (Res. 1415/1416/2024) y excepciones de la Res. 1389/2004 | Rutas de subproductos | SENASA | Analista | Pendiente | FTE-186, FTE-187, FTE-09B-20 | Complementa DPV-066 y DPV-074 |
| DPV-09B-07 | **Obligatoriedad del HACCP** para faena aviar de mercado interno (norma) | Programas obligatorios vs esperables | SENASA; CAA | Analista | Pendiente | FTE-09B-16 | P-16 |
| DPV-09B-08 | **Requisitos de agua**: parámetros, frecuencia de análisis, agua caliente, admisibilidad de agua no potable y reúso | Módulo de agua | Reglamento; CAA; SENASA | Analista | Pendiente | FTE-09B-09 | Coordinar con `11_agua_efluentes`; P-18 |
| DPV-09B-09 | **Habilitación actual de la carnicería familiar** (municipal/bromatología) y rubros que podría sumar | Canal de elaborados (DEC-09B-02) | Promotor; municipio | Promotor | Pendiente | — | — |
| DPV-09B-10 | **Texto de la Res. SENASA 723/2025** (transporte): requisitos por tipo de vehículo, lavado y desinfección, bienestar | Logística | Boletín Oficial | Analista | Pendiente | FTE-09B-07, FTE-09B-08 | Complementa DPV-058 (la Res. 503/2022 que podría figurar en otros archivos está derogada) |
| DPV-09B-11 | **Bienestar en faena**: ayuno, espera, parámetros de aturdimiento y verificación de inconsciencia; carácter de norma o guía | Recepción y aturdimiento | Manual SENASA; reglamento | Analista | Pendiente | FTE-09B-06 | P-22 |
| DPV-09B-12 | **Normas derogadas por la Res. SENASA 591/2026** y texto de la 592/2026 | Evitar citar normas derogadas | Boletín Oficial | Analista | Pendiente | FTE-09B-01, FTE-09B-22 | 42 vs 43 normas según fuente |
| DPV-09B-13 | **Plazos reales** de habilitación federal, modificaciones y autorización de destinos (casos recientes) | Gates y cronograma | SENASA; plantas habilitadas recientemente; asesores | Analista | Pendiente | FTE-09B-02 | Complementa DPV-086; P-35 |
| DPV-09B-14 | **Normativa ambiental, hídrica, municipal, bomberos y energía** por localización candidata (plantilla de 14 temas) | Selección de terreno | Organismos provinciales y municipales | Analista | Pendiente (requiere DEC-003) | — | `16_normativa_senasa/habilitacion_planta.md` §5 |

### 3.2 Notas a registros existentes

- **DPV-007** (normativa de habilitación): "2026-09-30 (09B): planta de faena **parcialmente abordada** en `16_normativa_senasa/` (mapa, matriz de 60 requisitos, secuencia, preguntas); todo `[PVDP]`. Pendientes: granjas (ver `03_produccion_primaria`), incubación, alimento balanceado."
- **DPV-009**: "Séptima sesión con acceso bloqueado (Infoleg, argentina.gob.ar, BO, digesto y biblioteca SENASA, MAGyP, ecofield, agrolex: `EGRESS_BLOCKED` 2026-09-30)."
- **DPV-058** (transporte de aves vivas): "Marco vigente identificado: Res. SENASA 723/2025 (reemplazó 503/2022, 735/2022, 557/2024). Ver DPV-09B-10."
- **DPV-061** (agua en carne aviar): "Cap. XX modificado por Res. 553/2002; P-19 en `preguntas_senasa.md`."
- **DPV-066**, **DPV-074**: "Marco en `16_normativa_senasa/subproductos_normativa.md`; preguntas P-30 a P-34."
- **DPV-086** (plazos de ampliación): "Plazo publicado de habilitación de plantas Ciclo I: 120 días hábiles (urgente ≤ 30) `[PVDP]`, FTE-09B-02; modificaciones con trámite propio. Ver DPV-09B-13."
- **DPV-024 / DPV-031** (listados y destinos): "Procedimiento Res. 593/2026 detallado en `16_normativa_senasa/exportacion_y_certificaciones.md` §1 (FTE-09B-05)."

## 4. Glosario (`glosario.md`) — términos a agregar si no existen

| Término | Definición propuesta |
|---|---|
| SIV | Servicio de Inspección Veterinaria de SENASA destacado en un establecimiento; realiza la inspección ante y post mortem y dictamina la aptitud. |
| Ante mortem / post mortem | Inspección oficial de los animales vivos antes de la faena / de carcasas y vísceras después de la faena. |
| Rubro (habilitación) | Actividad específica autorizada a un establecimiento (faena, trozado, deshuese, elaboración, depósito, congelado); agregar rubros es una modificación. |
| Tránsito federal | Habilitación de SENASA que permite comercializar productos en todo el país (y es condición previa para exportar). |
| Ciclo I | Categoría de SENASA para plantas de faena de animales terrestres (incluye aves) en el trámite de habilitación. `[PVDP]` |
| SIGTrámites / TAD | Plataformas digitales de trámites de SENASA / Trámites a Distancia del Estado nacional. |
| CAPA | Coordinación General de Aprobación de Productos Alimenticios de SENASA: registra productos y rótulos de origen animal. |
| SIGCER | Sistema de Gestión de Certificaciones de SENASA para certificados sanitarios de exportación. |
| DT-e | Documento de Tránsito electrónico de SENASA, obligatorio para mover animales (incluidas aves a faena). |
| SIGSA | Sistema Integrado de Gestión de Sanidad Animal de SENASA (lotes, existencias, DT-e). |
| POES (SSOP) | Procedimientos Operativos Estandarizados de Saneamiento: procedimientos escritos de limpieza y desinfección, obligatorios (Res. SENASA 233/1998). |
| MIP | Manejo Integrado de Plagas. |
| Plan CREHA | Plan Nacional de Control de Residuos e Higiene en Alimentos de SENASA. |
| FSSC 22000 / BRCGS / IFS | Certificaciones privadas de inocuidad reconocidas por GFSI, voluntarias, exigidas por algunos compradores. |
| OAA | Organismo Argentino de Acreditación. |

## 5. Estado del proyecto (`estado_proyecto.md`) — hito propuesto

| Fecha | Hito | Estado |
|---|---|---|
| 2026-09-30 | Hoja de ruta regulatoria (`16_normativa_senasa`): mapa de autoridades y tipos de habilitación, rol e índice práctico del Decreto 4238/68, secuencia tentativa de habilitación, condiciones edilicias, agua, inspección veterinaria, BPM/POES/HACCP, bienestar animal, frío, rotulado, trazabilidad, transporte, subproductos, escalera exportadora, plantilla jurisdiccional, matriz regulatoria (60 requisitos), ruta crítica (14 reglas), 38 preguntas para SENASA y guía | Completado v1.0 (sesión 09B). **Ninguna norma leída en original (acceso bloqueado, DPV-009)**. Detectados cambios 2025–2026 (Res. 592, 593, 591 y 233/2026; Res. 723/2025) y 5 contradicciones. Calidad: MEDIA como estructura, BAJA como evidencia normativa |

## 6. Anotaciones propuestas en otras carpetas (no modificadas en esta sesión)

- `17_exportacion/requisitos_planta_exportadora.md` §1: la "actualización por Res. SENASA 592/2026" consiste en la **derogación de la obligatoriedad del Director Técnico** (numerales 1.7 y 9.2); el análisis detallado ya no está "pendiente": ver `16_normativa_senasa/`.
- `16_normativa_senasa/README.md`: actualizado en esta sesión (dentro de la carpeta asignada).

## 7. Fuentes (`registro_fuentes.csv` y `bibliografia.md`)

Las 24 fuentes nuevas están en [`fuentes_09B.csv`](fuentes_09B.csv) con las mismas columnas que `registro_fuentes.csv` (IDs `FTE-09B-01` a `FTE-09B-24`). Al consolidar: renumerar como FTE-194 en adelante (o el siguiente libre), copiar las filas al registro y agregar a `bibliografia.md` bajo "Normativa". Anotaciones a fuentes existentes: **FTE-016** y **FTE-192** ("texto actualizado identificado; ver FTE-09B-23"), **FTE-083** ("detalle de requisitos en FTE-09B-05"), **FTE-082** ("complemento FTE-09B-18"), **FTE-146** ("complemento FTE-09B-12").
