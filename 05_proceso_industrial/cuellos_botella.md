# Capacidad horaria y cuellos de botella

**Fecha:** 2026-09-30 · **Versión:** 1.1 (corrección conceptual final de la sesión 09A; ver §0) · Fase 0

> **Alcance:** por qué la velocidad de la línea principal **no** es la capacidad de la planta; jerarquía de capacidades; definiciones de velocidad (nominal, de diseño, garantizada, operativa), disponibilidad, eficiencia, OEE, microparadas y paradas planificadas; ritmos a 6 / 8 / 10 / 16 h netas; ecuación de 24 h del establecimiento; cuellos de botella por sistema. **No** elige escala, turnos (DEC-036), equipos ni método de enfriamiento.
> **Modelo:** [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py) v1.1 → [`capacidad_proceso.csv`](capacidad_proceso.csv) (18 tests; 9 mutaciones detectadas). Definiciones de capacidad nominal / operativa / utilización de la escala: [`capacidad_preliminar.md` §1](capacidad_preliminar.md) (SUP-052).
> **Clasificación:** los ritmos operativos son `[ESTIMACIÓN]` aritmética. Disponibilidad, factor de velocidad, eficiencia global, tiempos de ventana, residencia en el enfriamiento y productividades manuales son **`[SUPUESTO]` de sensibilidad del modelo** (SUP-061 a SUP-064) o extractos `[PVDP]`: **no son desempeño industrial demostrado** (test T14). **Ninguna cifra es un dato medido en una planta argentina.**

---

## 0. Corrección conceptual v1.1

| # | Afirmación v1.0 | Corrección v1.1 |
|---|---|---|
| 1 | "Una línea con eficiencia real 0,70–0,90…" | 0,70–0,90 es solo un **rango de sensibilidad del modelo**, descompuesto en disponibilidad (D) y factor de velocidad (R); no es una eficiencia universal ni un dato de fabricantes (§2) |
| 2 | "Por encima de ~1.000 aves/h la evisceración manual deja de ser práctica" | **Sin umbral fijo.** Un fabricante documenta una planta compacta con **evisceración manual hasta ~1.600 broilers/h** (BAADER Compact Plant 396, FTE-200). El umbral económico para Argentina se determina con cotizaciones y productividad real (§5) |
| 3 | "16 h netas no entran en un día" | Con los supuestos actuales, 16 h netas generan una **restricción severa de calendario** y **pueden** resultar inviables en 24 h; **debe validarse** con proveedores y plantas antes de descartarlo (§4) |
| 4 | Una sola "capacidad de planta" | Jerarquía: capacidad teórica de equipo → capacidad del cuello de botella → capacidad operativa de planta → producción real (§1) |
| 5 | Tiempo de limpieza fijo | `t_limpieza(escala, configuración, automatización)` **provisional**: hoy no cambia con la escala; no se usa para descartar arquitecturas (§4.3) |

## 1. Capacidad de línea ≠ capacidad de planta: la jerarquía

```
CAPACIDAD TEÓRICA DE EQUIPO        = velocidad nominal × horas                     (cada equipo por separado)
CAPACIDAD EFECTIVA DE SUBSISTEMA   = velocidad nominal × horas programadas × D × R (≤ teórica, salvo justificación)
CAPACIDAD DEL CUELLO DE BOTELLA    = mínimo de las capacidades efectivas de los subsistemas modelados
CAPACIDAD OPERATIVA DE PLANTA      = mínimo(cuello de botella; restricciones externas: abastecimiento de aves,
                                     retiro de subproductos, frío, efluentes, personal, calendario)
PRODUCCIÓN REAL (período)          = capacidad operativa diaria × (días de faena − paradas planificadas de día completo)
                                     × utilización (≤ 100 %, depende de la demanda)
```

Funciones `capacidad_teorica_equipo`, `capacidad_efectiva`, `capacidad_cuello`, `capacidad_operativa_planta` y `produccion_real` del modelo (tests T03, T15, T18). La producción real es el **mínimo de las capacidades efectivas de los subsistemas relevantes, ajustado por disponibilidad y calendario**.

**Ejemplo didáctico** (números hipotéticos, **no** son datos ni una recomendación):

| Nivel | Valor hipotético (aves/día) |
|---|---|
| Capacidad efectiva: línea de faena | 20.000 |
| Capacidad efectiva: evisceración + inspección | 18.000 |
| Capacidad efectiva: enfriamiento | 19.000 |
| Capacidad efectiva: sala de trozado | **15.000** ← cuello de botella |
| Capacidad efectiva: cámaras | 17.000 |
| **Capacidad del cuello de botella** | **15.000** |
| Restricción externa: retiro de subproductos | **14.000** |
| **Capacidad operativa de planta** | **14.000** |
| Producción real anual con 250 días, 5 días de parada planificada y 90 % de utilización | 14.000 × 245 × 0,9 ≈ 3,09 M aves |

Comprar una línea de faena más rápida no mueve ninguno de los niveles inferiores.

## 2. Definiciones de velocidad, disponibilidad y eficiencia

| Concepto | Definición | Quién la fija / cómo se mide | En este estudio |
|---|---|---|---|
| **Velocidad nominal declarada** | Aves/h que el fabricante publica para un equipo o línea | Catálogo o página del fabricante. **Cada fabricante puede definir "aves/h" de forma distinta** (peso de ave, producto, con o sin repaso manual, grilletes ocupados, paso de grillete) | Solo **referencia**; nunca capacidad de diseño (T18) |
| **Velocidad de diseño** | Velocidad para la que se especifica y dimensiona la línea del proyecto, con margen sobre la operativa requerida | Ingeniería del proyecto + proveedor | No definida (fase posterior) |
| **Velocidad contractual / garantizada** | Velocidad que el proveedor se compromete a alcanzar en condiciones definidas en contrato, verificada con una **prueba de aceptación** | Contrato; prueba de aceptación en sitio | **Dato crítico de RFQ** ([`../08_maquinaria/requerimientos_cotizacion.md` §2.1](../08_maquinaria/requerimientos_cotizacion.md)) |
| **Velocidad operativa** | Aves/h reales mientras la línea está en marcha | Registro en planta | = nominal × R |
| **Factor de velocidad (R)** | Velocidad operativa / nominal: microparadas, grilletes vacíos, velocidad reducida por aves fuera de rango | Registro en planta | Sensibilidad 0,82 / 0,89 / 0,95 (SUP-061) |
| **Microparadas** | Interrupciones de segundos a pocos minutos que no se registran como parada | Sistemas de registro de línea | Dentro de R |
| **Disponibilidad (D)** | Tiempo en marcha / tiempo programado de producción: paradas no planificadas y cambios de producto | Registro de paradas | Sensibilidad 0,85 / 0,90 / 0,95 (SUP-061) |
| **Paradas planificadas** | Limpieza, sanitización, mantenimiento preventivo, arranque, pausas, cambios de turno; días de parada programada | Plan de producción | Fuera del tiempo programado: componentes de la ecuación de 24 h (§4) y días de parada en `produccion_real` |
| **Eficiencia de línea (η)** | Producción real / (nominal × tiempo programado) = D × R | Registro | Sensibilidad ≈ 0,70 / 0,80 / 0,90 |
| **OEE** (*overall equipment effectiveness*) | D × R × Q, con Q = fracción de aves conformes sin reproceso | Estándar de la industria de manufactura | Q no se modela (se supone incluido en R); aplicable cuando haya registros de planta |

**Horas netas** (h) = tiempo en que la línea está en marcha recibiendo aves (misma definición que [`capacidad_preliminar.md` §2](capacidad_preliminar.md)); las paradas no planificadas son tiempo **adicional**: `horas programadas = h / D`.

**Los factores D, R y η son un rango de sensibilidad del modelo, no desempeño industrial demostrado.** Ninguna fuente leída en esta sesión (fabricantes, FAO, prensa) da disponibilidades o eficiencias de líneas avícolas argentinas (DPV-088).

## 3. Capacidad horaria requerida

`[ESTIMACIÓN]` para el ritmo operativo (= aves/día ÷ horas netas; idéntico a [`../23_plan_expansion/escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv), test T01); `[SUPUESTO]` de sensibilidad para las columnas nominales.

| Escala (aves/día) | h netas | Ritmo operativo (aves/h) | Nominal con h netas en marcha: R 0,95 · 0,89 · 0,82 | Nominal si h incluyera las paradas: η 0,90 · 0,80 · 0,70 | Segundos por ave |
|---|---|---|---|---|---|
| 2.500 | 6 | 417 | 439 · 468 · 508 | 462 · 520 · 598 | 8,6 |
| 2.500 | **8** | **312** | 329 · 351 · 381 | 346 · 390 · 448 | 11,5 |
| 2.500 | 10 | 250 | 263 · 281 · 305 | 277 · 312 · 359 | 14,4 |
| 2.500 | 16 | 156 | 164 · 176 · 191 | 173 · 195 · 224 | 23,0 |
| 5.000 | 6 | 833 | 877 · 936 · 1.016 | 923 · 1.040 · 1.196 | 4,3 |
| 5.000 | **8** | **625** | 658 · 702 · 762 | 693 · 780 · 897 | 5,8 |
| 5.000 | 10 | 500 | 526 · 562 · 610 | 554 · 624 · 717 | 7,2 |
| 5.000 | 16 | 312 | 329 · 351 · 381 | 346 · 390 · 448 | 11,5 |
| 10.000 | 6 | 1.667 | 1.754 · 1.873 · 2.033 | 1.847 · 2.081 · 2.391 | 2,2 |
| 10.000 | **8** | **1.250** | 1.316 · 1.404 · 1.524 | 1.385 · 1.561 · 1.793 | 2,9 |
| 10.000 | 10 | 1.000 | 1.053 · 1.124 · 1.220 | 1.108 · 1.248 · 1.435 | 3,6 |
| 10.000 | 16 | 625 | 658 · 702 · 762 | 693 · 780 · 897 | 5,8 |
| 20.000 | 6 | 3.333 | 3.509 · 3.745 · 4.065 | 3.693 · 4.161 · 4.782 | 1,1 |
| 20.000 | **8** | **2.500** | 2.632 · 2.809 · 3.049 | 2.770 · 3.121 · 3.587 | 1,4 |
| 20.000 | 10 | 2.000 | 2.105 · 2.247 · 2.439 | 2.216 · 2.497 · 2.869 | 1,8 |
| 20.000 | 16 | 1.250 | 1.316 · 1.404 · 1.524 | 1.385 · 1.561 · 1.793 | 2,9 |

**Aves/día de una línea de nominal L con 8 h programadas** (L × 8 × D × R; líneas ilustrativas, no modelos de proveedor; sensibilidad):

| L nominal (aves/h) | η 0,90 | η 0,80 | η 0,70 |
|---|---|---|---|
| 312 | 2.256 | 2.002 | 1.742 |
| 625 | 4.512 | 4.005 | 3.485 |
| 1.250 | 9.025 | 8.010 | 6.970 |
| **2.500** | 18.050 | **16.020** | 13.940 |
| 3.125 | 22.562 | 20.025 | 17.425 |

**Lectura:** **si** una línea de 2.500 aves/h nominales tuviera una eficiencia de 0,80 en 8 h programadas, produciría ~16.000 aves/día, no 20.000 (T11). Es una **ilustración con parámetros de sensibilidad**: la cifra real depende de cómo el proveedor define su nominal, de la velocidad **garantizada** en contrato y de la disponibilidad medida. Lo que no cambia es el principio: ritmo × horas = escala solo si todo funciona al 100 % del tiempo, y eso no ocurre.

## 4. Modelo de 24 horas

### 4.1 Ecuación

```
24 h = faena neta
     + paradas durante la producción        (= h × (1/D − 1))
     + pausas del personal
     + cambios de turno
     + preparación / arranque (preoperativo)
     + cierre y vaciado de línea
     + limpieza intermedia
     + limpieza                             (t_limpieza: PROVISIONAL)
     + sanitización (desinfección + inspección)
     + mantenimiento no solapable
     + HOLGURA
```

Si la holgura es negativa, el modelo emite una **alerta de calendario** (no un descarte; T16). Cambiar el tiempo de limpieza cambia la holgura en la misma magnitud (T17). El simulador HTML (v0.1 ya construido en `23_plan_expansion/simulador_html/`, que **todavía no incorpora** la ecuación de 24 h) deberá mostrar cada componente y la holgura en una versión futura.

### 4.2 Resultados con tres escenarios de sensibilidad (SUP-062; h/día)

| Componente | Optimista | Media | Conservadora |
|---|---|---|---|
| Disponibilidad D asociada | 0,95 | 0,90 | 0,85 |
| Preparación / arranque | 0,50 | 0,75 | 1,00 |
| Pausas, por cada 8 h netas | 0,50 | 0,75 | 1,00 |
| Cambio de turno (por turno adicional; 10 h = un turno extendido) | 0,25 | 0,33 | 0,50 |
| Cierre y vaciado | 0,50 | 0,75 | 1,00 |
| Limpieza intermedia, por cada 8 h netas | 0,25 | 0,33 | 0,50 |
| Limpieza | 2,00 | 2,75 | 4,00 |
| Sanitización | 1,00 | 1,25 | 2,00 |
| Mantenimiento no solapable | 0,50 | 1,00 | 2,00 |

| h netas | Optimista: total · holgura | Media: total · holgura | Conservadora: total · holgura |
|---|---|---|---|
| 6 | 11,4 · 12,6 | 14,0 · 10,0 | 18,2 · 5,8 |
| 8 | 13,7 · 10,3 | 16,5 · 7,5 | 20,9 · 3,1 |
| 10 | 16,0 · 8,0 | 19,0 · 5,0 | 23,6 · 0,4 |
| **16 (2 × 8)** | 23,1 · **0,9** | 26,8 · **−2,8 ALERTA** | 32,3 · **−8,3 ALERTA** |
| Horas netas máximas con holgura ≥ 0 | 16,6 | 13,8 | 10,0 |

**Lecturas:**

1. Con 8 h netas, el establecimiento opera ~14–21 h/día según el escenario.
2. **Con los supuestos actuales de ventanas de limpieza, sanitización y mantenimiento, un escenario de 16 horas NETAS de faena genera una restricción severa de calendario y puede resultar inviable dentro de 24 horas. Debe validarse con proveedores y plantas reales antes de descartarlo.** Solo el escenario optimista deja una holgura (~0,9 h). Referencia `[PVDP · débil]`: plantas de EE.UU. operan jornadas de 16–20 h con un turno de sanitización de ~8 h (FTE-221), lo que indica que **existen organizaciones de dos turnos**; cómo lo logran (limpieza por sectores, equipos redundantes, dotación de limpieza, diseño higiénico) es justamente lo que hay que relevar.
3. **Dos turnos no se declaran imposibles.** Alternativas a evaluar: 10–13 h netas en turno extendido, sanitización por sectores o simultánea, equipos redundantes, sexto día, mayor ritmo nominal con un turno.

### 4.3 Limpieza: relación provisional

`t_limpieza(escala, configuración, automatización)` devuelve hoy el mismo valor para todas las escalas (factor 1; `LIMPIEZA_PROVISIONAL = True`). En la realidad, una planta más grande tiene más equipos que limpiar pero también más personal y, quizás, sistemas de limpieza centralizados; una planta más automatizada puede tener equipos más complejos de desarmar. **Datos de campo pendientes** (DPV-091): duración por sector, dotación de limpieza, simultaneidad (limpiar un sector mientras otro produce), CIP / limpieza manual / espuma, tiempos preoperacionales e inspección. **No se usa un único tiempo fijo para descartar arquitecturas.**

## 5. Cuellos de botella por sistema

Cada fila: por qué limita, qué indicador usar, cómo varía con la escala y qué dato falta. Cifras de carga del modelo (config. B, 8 h netas).

| Sistema | Por qué puede limitar | Indicador de carga | 2.500 → 20.000 aves/día (8 h) | Mitigación conceptual | Dato faltante |
|---|---|---|---|---|---|
| **Abastecimiento y espera de aves** | Si no llegan aves al ritmo, la línea para; si esperan demasiado, mueren o pierden calidad | Aves/h que deben llegar; camiones/día | 312 → 2.500 aves/h vivas | Programación de carga en granja; andén ventilado | Capacidad de camión (DPV-084); tiempos de viaje (DEC-003) |
| **Colgado** | Operación manual repetitiva y exigente; el ritmo por persona es limitado y la rotación es alta | Aves/min por colgador | 5,2 → 41,7 aves/min. Puestos equivalentes: 1 → 2 (ritmo de referencia de líneas de EE.UU., 23 aves/min) o 1 → 4 (prudente, 50 %) | Rotación de puestos; más puestos; ritmo por debajo del máximo (bienestar: estándar privado de 35 aves/min de línea, FTE-220) | Productividad y rotación reales en Argentina (DPV-092). Los puestos del modelo **no son dotación**: no incluyen rotación, pausas ni ausentismo |
| **Evisceración** | Manual: mucha mano de obra; automática: la calibración depende de la uniformidad del lote y cualquier falla detiene la línea | Aves/h por operario o por máquina | Manual: 3 → 21 puestos equivalentes (referencia 2 aves/min por operario, FTE-218 `[PVDP]`) o 6 → 42 (prudente). Hay equipos comerciales con **evisceración manual hasta ~1.600 aves/h** (BAADER Compact Plant 396, FTE-200) | Manual, semiautomática o automática según velocidad, costo y disponibilidad de mano de obra, ergonomía, inspección, uniformidad, calidad, higiene y escala; puestos de repaso en todos los casos | **Umbral económico argentino sin determinar**: cotizaciones y productividad real (DPV-092); tolerancia de equipos a pesos variables |
| **Inspección veterinaria** | El servicio oficial inspecciona ave por ave; si el ritmo excede lo que los inspectores pueden examinar, la línea debe bajar | Aves/min por puesto de inspección | 5 → 42 aves/min | Presentación automática de vísceras; puestos suficientes; acuerdo con SENASA | **Norma sobre puestos/inspectores por velocidad de línea** (DPV-090) |
| **Enfriamiento (chiller)** | Tiempo de residencia fijo: la capacidad depende del volumen o de la longitud del recorrido | Carcasas simultáneas dentro del sistema | Inmersión (50 min): 260 → 2.083 carcasas; aire (90–150 min): 469–781 → 3.750–6.250 carcasas | Dimensionar por la escala final o modularizar (segundo tanque, más recorrido); DEC-026 | Tiempos y temperaturas objetivo por norma (FTE-192 `[PVDP]`) y por equipo |
| **Clasificación** | Si es manual, depende de personas; si es automática, de la balanza de línea | Aves/h | 312 → 2.500 | Balanza de línea con distribución | — |
| **Trozado** | Manual: mano de obra y temperatura de la sala; automático: un equipo de alto costo que puede ser el cuello si se para | kg/h a trozar | 636 → 5.091 kg/h | Mesas manuales en escalas bajas; trozado automático en altas; sala ampliable | Productividad manual (kg/h/operario) |
| **Deshuese** | Muy intensivo en mano de obra; el equipo automático es específico por pieza | kg/h a deshuesar (config. C) | 359 → 2.875 kg/h; piezas de pata-muslo: 625 → 5.000/h. Referencia de un equipo automático de pata-muslo: 1.000 piezas/h (FTE-211 `[PVDP]`) | Deshuese manual en conos; automatizar primero la pieza de mayor volumen | Productividad manual; mix real (DPV-037) |
| **Packaging** | Cada formato (bolsa, bandeja, termoformado, vacío, MAP) es una máquina distinta con su ritmo y sus cambios | Envases/min por formato; cambios de formato por día | Comestible a empaque 749 → 5.991 kg/h | Pocos formatos al inicio; máquinas por familia de producto | Mix de formatos por cliente (DPV-041) |
| **Congelado** | El producto debe llegar a −18 °C en el centro; el tiempo de congelado fija la capacidad del túnel o espiral | t/día a congelar | P1 0,6 → 4,8; P2 2,4 → 19,2; P3 3,0 → 24,0 t/día | Congelado de terceros al inicio; túnel modular | Tiempo de congelado por producto y envase (DPV-096) |
| **Cámaras** | Stock para completar pedidos y contenedores | t en stock | 7 días de producción: 42 → 336 t ([`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) §2) | Cámaras modulares; frío de terceros | Días de stock según clientes y exportación |
| **Expedición** | Andenes, tiempo de carga y ventanas horarias de clientes | t/día a despachar; camiones/día | 6,0 → 47,9 t peso comercial por día operativo | Andenes con sello; turnos de carga desfasados de la faena | Capacidad de camión y ventanas de entrega (DPV-084, DPV-036) |
| **Limpieza y sanitización** | Consume la ventana horaria (§4) | h/día | Limpieza 2–4 h + sanitización 1–2 h (sensibilidad; relación con la escala provisional) | Diseño higiénico (fácil de limpiar); equipos de limpieza centralizados | Tiempos reales (DPV-091) |
| **Agua** | Escaldado, lavado, chiller, limpieza: litros por ave (no dimensionado) | m³/día | Proporcional a aves (a calcular en `11_agua_efluentes`) | Recirculación donde la norma lo permita | Consumo por ave (`11_agua_efluentes`) |
| **Efluentes** | Caudal y carga orgánica diarios; permiso de vuelco | m³/día y kg DQO/día | Proporcional; la sangre no recuperada es la mayor carga evitable | Recuperar sangre; separar sólidos | `11_agua_efluentes` |
| **Frío** | Carga térmica del enfriamiento de carcasas, salas, túneles y cámaras | kW de frío | Proporcional a kg/h y a perfil de congelado | Sala de máquinas ampliable | `12_energia_frio` |
| **Mano de obra** | Colgado, evisceración, trozado, deshuese y empaque son intensivos; disponibilidad local limitada | Personas por turno | Crece casi linealmente sin automatización | Automatizar donde la mano de obra es el límite | `18_recursos_humanos` |
| **Subproductos** | Si el receptor no retira, la faena se detiene (no hay dónde poner plumas y vísceras) | t/día a retirar | Sólidos: 1,5 → 12,2 t/día; sangre 0,2 → 1,7 t/día | Dos receptores o almacenamiento de contingencia ([`../07_subproductos/conclusiones_valorizacion.md` §10](../07_subproductos/conclusiones_valorizacion.md)) | DPV-065, DPV-080 |

## 6. Por qué la línea principal no es la capacidad real

1. **Disponibilidad y velocidad < 100 %:** paradas, microparadas y huecos reducen la producción real (§2–§3; magnitud a medir).
2. **Otras etapas más lentas:** evisceración manual, inspección, trozado o deshuese manual, envasado con muchos formatos (§5).
3. **Etapas con tiempo de residencia:** enfriamiento y congelado no se aceleran subiendo la velocidad; dependen del volumen instalado.
4. **Servicios:** sin agua, frío, efluentes o energía suficientes, la línea no puede ir a su ritmo.
5. **Ventana horaria:** la limpieza y el mantenimiento compiten con las horas de faena (§4).
6. **Mano de obra:** en escalas chicas y medianas la capacidad la marca la gente, no la máquina.
7. **Mix de productos:** el cuello de botella cambia con el producto. Una planta de pollo entero tiene su cuello en faena/enfriamiento/embolsado; una de trozado, en la sala de trozado; una de deshuesado, en el deshuese (misma cantidad de aves, [`../23_plan_expansion/escenarios_escala.md` §9](../23_plan_expansion/escenarios_escala.md)).
8. **Subproductos:** si no se retiran, la planta se detiene.

## 7. Qué verificar antes de usar un segundo turno como palanca

Condición necesaria, no suficiente (DEC-036). El segundo turno **no se descarta ni se asume**: (1) ventana de limpieza, sanitización y mantenimiento compatible, medida en plantas reales (§4; hoy solo sensibilidad); (2) mano de obra para dos turnos (convenio, DPV-082); (3) abastecimiento de aves 16 h por día y espera nocturna; (4) enfriamiento, frío, cámaras y congelado para el doble de producción diaria; (5) agua y permiso de vuelco para el doble de caudal diario; (6) retiro de subproductos dos veces por día; (7) inspección oficial en ambos turnos; (8) expedición y clientes que absorban el doble.
