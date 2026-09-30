# Catálogo conceptual de equipos por etapa

**Fecha:** 2026-09-30 · **Versión:** 1.1 (sesión 09A; corrección: evisceración manual sin umbral fijo, niveles como arquitectura de referencia) · Fase 0 — **solo relevamiento: no se selecciona equipo, marca, modelo ni proveedor**

> **Alcance:** qué equipos (conceptuales) necesita cada etapa del proceso ([`../05_proceso_industrial/flujo_proceso.md`](../05_proceso_industrial/flujo_proceso.md)), qué alternativas tecnológicas existen, qué servicios consumen, cuán críticos son y cómo se mantienen. **No** hay precios, CAPEX, capacidades de modelos específicos ni recomendación.
> **Archivo maestro:** [`matriz_equipos.csv`](matriz_equipos.csv) (76 equipos, `EQ-01` a `EQ-76`). Este documento es su lectura analítica; los niveles de automatización por escala se discuten en [`automatizacion_por_escala.md`](automatizacion_por_escala.md). Fuentes: [`registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (todas `[PVDP]`: extractos de buscador; acceso directo a sitios bloqueado en la sesión).
> **Clasificación:** la lista de equipos, sus alternativas y su criticidad son `[SUPUESTO]` de trabajo basados en conocimiento técnico general del proceso (SUP-065), a validar con proveedores (RFQ, [`requerimientos_cotizacion.md`](requerimientos_cotizacion.md)) y con plantas en operación.

### Diccionario de columnas de `matriz_equipos.csv`

| Columna | Contenido |
|---|---|
| `id` | EQ-## |
| `grupo`, `etapas` | Grupo de proceso y etapas de `flujo_proceso.md` (E##, X#, Z#) |
| `equipo`, `funcion`, `alternativas` | Qué es, para qué sirve y variantes tecnológicas |
| `manual_posible` | Si la operación puede hacerse a mano y hasta dónde |
| `sensibilidad_escala` | Cuánto cambia el equipo al cambiar la escala |
| `nivel_2500` … `nivel_20000` | Nivel **razonable a estudiar** (arquitectura de referencia, no obligación ni decisión): **M** manual · **Mc** mecanizado · **S** semiautomático · **A** automático · **O** opcional según producto/mercado · **T** tercerizar/postergar · **—** no aplica. "M/S" = ambas a comparar |
| `criticidad` | **CRÍTICO** detiene la faena · **IMPORTANTE** reduce capacidad o calidad · **SECUNDARIO** puede resolverse temporalmente |
| `bypass_o_redundancia` | Qué hacer si falla |
| `servicios` | elec, agua, agua_caliente, agua_helada, vapor, aire, vacío, frío, gas |
| `mantenimiento_clave`, `modularidad` | Puntos de desgaste; si se mantiene, duplica, amplía o reemplaza al crecer |
| `fuente`, `clasificacion`, `nota` | Trazabilidad |

---

## 1. Equipos por etapa (síntesis)

### 1.1 Recepción de vivo (EQ-01 a EQ-06)

| Necesidad | Equipos | Comentario |
|---|---|---|
| Pesaje | Balanza de camiones (EQ-01) | Base del balance de lote y de la liquidación a productores |
| Módulos/cajones | Cajones sueltos o módulos (EQ-03) | Los módulos reducen manipulación y lesiones; exigen autoelevador y volcador |
| Descarga | Manual, cinta o volcador (EQ-04) | A baja escala, manual; a alta, mecánica |
| Espera | Andén cubierto, ventilación forzada, nebulización, luz tenue (EQ-02) | Condición de bienestar; en verano puede limitar la faena |
| Ventilación | Ventiladores y control de temperatura (EQ-02) | — |
| Lavado | Cajones/módulos (EQ-05) y camiones (EQ-06) | Bioseguridad de las granjas integradas |

### 1.2 Faena (EQ-07 a EQ-20)

Transportador aéreo con grilletes (EQ-07, **crítico**: punto único de falla), puesto de colgado (EQ-08), **aturdido** eléctrico en baño de agua (EQ-09) o por atmósfera controlada (EQ-10; método no decidido, DEC-041), degolladora con repaso manual (EQ-11), canal de sangrado con bomba y tanque (EQ-12), **escaldadora** (EQ-13) con su generación de agua caliente (EQ-14), **desplumadoras** en serie (EQ-15) con canal de plumas (EQ-16), cortadora de patas (EQ-17), arrancador de cabezas (EQ-18), **transferencia** a evisceración (EQ-19) y lavadora de grilletes (EQ-20).

**Aturdido — comparación conceptual** (FTE-216 `[PVDP]`):

| | Eléctrico en baño de agua | Atmósfera controlada (CAS) |
|---|---|---|
| Momento | Aves colgadas conscientes, luego aturdidas | Aves aturdidas en el módulo, colgado posterior |
| Bienestar | Estándar difundido; depende de parámetros | Evita colgar aves conscientes |
| Colgado | Aleteo, más difícil | Aves inmóviles, más fácil y rápido |
| Escala | Cualquiera | Sistema grande; más natural con módulos |
| Halal | Requisitos por destino no verificados (DPV-034) | Idem |
| Decisión | **Abierta** (DEC-041) | **Abierta** |

### 1.3 Evisceración (EQ-21 a EQ-33)

Transportador de evisceración (EQ-21, crítico), cortadora de cloaca (EQ-22), abridora (EQ-23), **evisceradora** (EQ-24: la decisión de automatización más sensible a la escala; un fabricante documenta evisceración manual en línea hasta ~1.600 broilers/h, FTE-200, por lo que no hay umbral fijo), presentación de vísceras para inspección (EQ-25), **puestos de inspección oficial** (EQ-26, crítico por norma), cosecha de menudencias (EQ-27), peladora de mollejas (EQ-28), extractor de buche/cuello (EQ-29), aspirador de pulmones (EQ-30), lavadora interior/exterior (EQ-31), transporte de vísceras por canal o vacío (EQ-32) y enfriador de menudencias (EQ-33).

### 1.4 Enfriamiento (EQ-34 a EQ-38)

**Comparación** (sin decisión, DEC-026; tiempos y masas de FTE-217 `[PVDP]` y del balance v1.1):

| Criterio | Inmersión (prechiller + chiller) | Aire (air chilling) | Combinaciones (inmersión + aire; aire con aspersión) |
|---|---|---|---|
| Tiempo de residencia | ~50 min | 90–150 min | Intermedio |
| Carcasas simultáneas a 10.000 aves/día, 8 h | ~1.040 | ~1.875–3.125 (colgadas) | Intermedio |
| Masa del producto | **Absorbe agua**: +0,122 kg/ave (6 %) en el modelo; límite legal 8 % (prensa, DPV-061) | **Pierde humedad**: −0,037 kg/ave (1,8 %) | Menor pérdida que solo aire (~50 % menos según extracto) |
| Superficie y frío | Compacto; requiere agua helada/hielo | Mayor superficie (cámara con recorrido de riel) y más frío por aire | Intermedio |
| Agua y efluente | Alto consumo de agua (renovación) | Bajo consumo de agua | Intermedio |
| Contaminación cruzada | Riesgo en el agua compartida (control por renovación y temperatura) | Menor contacto entre carcasas | — |
| Mercados | Difundido en América (FTE-217) | Preferido/requerido en la UE (restricciones a la inmersión, extracto) | — |
| Rotulado y precio | El agua retenida se vende como peso; tema de rotulado | Sin agua agregada: argumento comercial "enfriado por aire" | — |
| Escalabilidad | Agregar tanque | Requiere espacio de cámara previsto | — |
| Norma argentina | Parámetros no leídos (DPV-062) | ≤ 7 °C en lo profundo de la pechuga antes de envasar (extracto FTE-192) | — |

Complementos: generación de agua helada o hielo (EQ-37, crítico con inmersión) y descargador/escurridor (EQ-38).

### 1.5 Procesamiento secundario (EQ-39 a EQ-48)

| Operación | Equipos | Manual posible | Comentario |
|---|---|---|---|
| Clasificación | Balanza de línea con distribución (EQ-39) | Sí (mesa + balanza) | Define calibres para entero y exportación |
| Trozado | Mesas con sierra (EQ-40); trozadora automática modular (EQ-41) | Sí | Sala de trozado mínima siempre necesaria (canales no aptas para entero) |
| Deshuese | Línea de conos manual (EQ-42); deshuesadora de pata-muslo (EQ-43); fileteadora de pechuga (EQ-44) | Sí (muy intensivo en mano de obra) | Referencia de equipo automático de pata-muslo: 1.000 piezas/h (FTE-211 `[PVDP]`) |
| Fileteado y porcionado | Porcionadora (EQ-46) | Sí | Solo con mercado (gastronomía, exportación) |
| Trimming | Mesas; rayos X para hueso opcional (EQ-45) | Sí | Exigencia de cliente |
| Garras | Escaldador de patas, peladora, clasificadora (EQ-47) | Sí (lento) | Sin comprador, no pelar (DEC-031) |
| Menudencias | Peladora de mollejas (EQ-28), enfriador (EQ-33) | Sí | Perecibles |
| CMS | Separadora + frío inmediato (EQ-48) | No | Ruta excluyente con venta de esqueleto (SUP-045) |

### 1.6 Packaging (EQ-49 a EQ-56)

| Formato | Equipo | Producto típico | Comentario |
|---|---|---|---|
| **Bolsa** | Embolsadora con clip o termocontracción (EQ-49) | Entero | Manual posible a baja escala |
| **Bandeja + film estirable** | Envolvedora (EQ-50) | Trozado para supermercado | Formato básico de góndola |
| **Bandeja termosellada / MAP** | Termoselladora (EQ-51) + mezclador de gases | Trozado, deshuesado, marinados | Más vida útil (a determinar, DPV-078) |
| **Termoformado** (vacío, MAP, skin) | Termoformadora (EQ-52) | Deshuesado, porciones | Mayor ritmo; más inversión |
| **Vacío** | Envasadora de cámara/campana (EQ-53) | Piezas para gastronomía y exportación | — |
| **Bloque / caja granel** | Balanza + caja (EQ-54, EQ-56) | Cortes a granel, menudencias, garras, CMS | Exportación y mayoristas |
| Control y rotulado | Balanza etiquetadora (EQ-54), detector de metales/rayos X (EQ-55) | Todos | Trazabilidad de lote |

La **atmósfera modificada** solo tiene sentido si el cliente paga la vida útil adicional. Cada formato agrega una máquina, sus moldes y sus cambios de formato: **pocos formatos al inicio** reduce el cuello de botella de empaque.

### 1.7 Congelado (EQ-57 a EQ-61) y frío (EQ-62 a EQ-65)

| Tecnología | Mejor para | Ventaja | Limitación | Fuente |
|---|---|---|---|---|
| **Túnel estático** (carros/pallets) | Producto en caja; baja escala | Simple, flexible | Congelado lento en caja; manipuleo | Conocimiento general |
| **Túnel continuo lineal / IQF** | Piezas individuales; producto plano | Menor inversión inicial que espiral para producto uniforme | Mucha superficie | FTE-215 `[PVDP · débil]` |
| **Espiral** | Producto individual o envasado, alto volumen | 60–70 % menos superficie que un túnel lineal de igual capacidad | Inversión; escala | FTE-215 `[PVDP · débil]` |
| **Placas** | Bloques (menudencias, CMS, recortes) | Congelado rápido de bloques | Solo bloques | Conocimiento general |
| **Criogénico** (N2/CO2) | Picos, productos especiales | Muy rápido, poca inversión | Costo por kg (insumo) | Conocimiento general |
| **Congelado de terceros** | Etapas iniciales o picos | Sin inversión | Logística y dependencia | [`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md) |

Carga de congelado por día (config. B): P1 0,6 → 4,8 t; P2 2,4 → 19,2 t; P3 3,0 → 24,0 t de 2.500 a 20.000 aves/día ([`../05_proceso_industrial/cuellos_botella.md` §5](../05_proceso_industrial/cuellos_botella.md)). El dimensionamiento en kW y tiempos de congelado es de `12_energia_frio` (DPV-096).

### 1.8 Subproductos (EQ-66 a EQ-70)

| Corriente | Equipos | Almacenamiento temporal | Retiro |
|---|---|---|---|
| Sangre | Canal, bomba, tanque (EQ-12, EQ-66) | Tanque cerrado, sin dilución | Horas |
| Plumas | Canal de agua o tornillo, tamiz/prensa, tolva (EQ-16, EQ-67) | Tolva o contenedor | Diario |
| Vísceras y cabezas | Canal o vacío, tamiz, tolva (EQ-32, EQ-68) | Contenedor cerrado | Diario |
| Decomisos | Recipientes identificados (EQ-69) | Bajo control oficial | Según norma |
| Efluente | Tamices y separación de sólidos (EQ-70) | — | Tratamiento (`11_agua_efluentes`) |

### 1.9 Servicios transversales (EQ-71 a EQ-76)

Aire comprimido (EQ-71), agua potable (EQ-72), grupo electrógeno (EQ-73), espuma de limpieza (EQ-74), esterilizadores y lavamanos (EQ-75), trazabilidad y registro de paradas (EQ-76). Sin ellos ningún equipo de proceso funciona; se dimensionan en `11_agua_efluentes` y `12_energia_frio`.

---

## 2. Criticidad, redundancia y mantenimiento

### 2.1 Clasificación

Criterio: **CRÍTICO** — su falla **detiene la faena** (no hay forma razonable de seguir); **IMPORTANTE** — su falla **reduce la capacidad** o la calidad (hay bypass manual o parcial); **SECUNDARIO** — puede **resolverse temporalmente** sin afectar la faena del día. Conteo en la matriz: 17 críticos + 2 condicionales (aire comprimido en líneas automáticas; evisceradora si la línea depende de evisceración automática), 36 importantes, 21 secundarios.

| Clase | Equipos (EQ) | Qué implica |
|---|---|---|
| **CRÍTICO** | Transportadores aéreos de faena y evisceración (07, 21); aturdido (09 o 10); escaldadora (13) y su agua caliente (14); desplumadoras (15) y canal de plumas (16); puestos de inspección (26); enfriamiento (34/35/36) y agua helada (37); cámaras de refrigeración (62); sala de máquinas de frío (64); agua potable (72); esterilizadores y lavamanos (75); aire comprimido en líneas automáticas (71); evisceradora cuando la línea depende de evisceración automática (24) | Repuestos en planta, mantenimiento preventivo estricto, técnico disponible en horas, redundancia N+1 donde sea posible (compresores de frío y aire, bombas, calderas) |
| **IMPORTANTE** | Espera y descarga (02–04); degolladora (11); sangrado (12); patas, cabezas y transferencia (17–19); corte de cloaca, abridora, evisceradora cuando hay bypass manual (22–24); presentación para inspección (25); lavadora de carcasas (31); vísceras y menudencias (32, 33); descargador del chiller (38); clasificación, trozado y deshuese (39–42, 44); empaque (49–52, 54, 55); congelado (57–59); cámaras de congelado (63); subproductos (66–68, 70); grupo electrógeno (73); trazabilidad (76) | Bypass manual definido y entrenado; repuestos de desgaste en planta |
| **SECUNDARIO** | Balanza de camiones (01); lavado de cajones y camiones (05, 06); puesto de colgado (08); lavadora de grilletes (20); menudencias, molleja, buche, pulmones (27–30); trimming y porcionado (45, 46); garras (47); CMS (48); vacío, cajas y paletizado (53, 56); placas y criogénico (60, 61); andenes (65); contenedores (69); espuma (74) | Se reparan en el día o se sustituyen con trabajo manual o terceros |

**La criticidad cambia con la configuración:** con evisceración manual, una evisceradora rota "no existe"; si la línea se diseña con evisceración automática, su falla la detiene (a 20.000 aves/día, reemplazarla con personas exigiría ~21–42 puestos equivalentes, [`../05_proceso_industrial/cuellos_botella.md` §5](../05_proceso_industrial/cuellos_botella.md)). **Automatizar convierte tareas manuales flexibles en equipos críticos.**

### 2.2 Repuestos

- **Críticos en planta:** cadena y grilletes, motorreductores del transportador, dedos y rodamientos de desplumadoras, resistencias/bombas de escaldado, electrodos y transformador del aturdidor, cuchillas de todas las máquinas automáticas, bombas de sangre, plumas y vísceras, componentes del chiller (motor, rodamientos), repuestos de compresores de frío y aire.
- **Criterio:** stock de repuestos de desgaste para N semanas + repuestos de falla catastrófica para equipos sin bypass. El listado lo debe entregar cada proveedor con tiempos de reposición en Argentina (RFQ).
- **Riesgo argentino:** plazos de importación y restricciones cambiarias pueden alargar la reposición; un repuesto importado con semanas de demora sobre un equipo crítico **equivale a semanas sin faena** (DPV-089).

### 2.3 Redundancia y bypass

| Estrategia | Dónde aplica | Costo conceptual |
|---|---|---|
| **N+1** (una unidad extra) | Compresores de frío y aire, bombas, calderas, evaporadores | Unidad adicional |
| **Unidades en serie** | Desplumadoras, tanques de escaldado, chiller en dos tanques | Una falla reduce calidad o ritmo, no detiene |
| **Bypass manual** | Degüello, corte de patas y cabeza, transferencia, evisceración a bajo ritmo, trozado, empaque | Personal entrenado disponible |
| **Dos líneas paralelas** | Escalas altas (10.000–20.000) | Duplicar equipos, pero una línea sigue si la otra se detiene ([`../05_proceso_industrial/arquitecturas_por_escala.md` §8.2](../05_proceso_industrial/arquitecturas_por_escala.md)) |
| **Terceros** | Congelado, cámaras, subproductos, faena a façon de emergencia | Contratos previos |

### 2.4 Mantenimiento preventivo

| Frecuencia | Tareas típicas (conceptuales) |
|---|---|
| Diaria (en la ventana de limpieza) | Inspección de cuchillas, dedos, grilletes; lubricación de grado alimentario; verificación de parámetros (aturdido, escaldado, chiller) |
| Semanal | Cambio de cuchillas y piezas de desgaste; ajustes de calibración; revisión de bombas |
| Mensual / trimestral | Rodamientos, reductores, cadenas; compresores de frío y aire |
| Anual (parada programada) | Revisión general, reemplazo de componentes mayores, recertificación de recipientes a presión |

El tiempo de mantenimiento compite con la limpieza y la faena ([`../05_proceso_industrial/cuellos_botella.md` §4](../05_proceso_industrial/cuellos_botella.md)): con dos turnos de faena, el mantenimiento preventivo diario queda sin ventana.

### 2.5 Dependencia de proveedor y técnicos

| Riesgo | Descripción | Mitigación conceptual |
|---|---|---|
| **Repuestos propietarios** | Equipos automáticos usan piezas específicas del fabricante | Contrato de repuestos; stock en planta |
| **Técnico especializado** | Calibración de evisceradoras y trozadoras exige técnicos del fabricante | Verificar técnicos residentes en Argentina (no verificado para ningún proveedor, DPV-089); capacitar personal propio |
| **Software y electrónica** | Controles, balanzas de línea, SCADA | Soporte remoto; versiones estandarizadas |
| **Mezcla de marcas** | Integrar equipos de distintos fabricantes (o nuevos con usados) complica sincronía y responsabilidad | Un integrador responsable de la línea o un proveedor principal |
| **Salida del proveedor del país** | Discontinuidad de soporte | Preferir tecnologías con repuestos genéricos donde se pueda |

Presencia verificada de proveedores: [`proveedores_preliminares.md`](proveedores_preliminares.md).
