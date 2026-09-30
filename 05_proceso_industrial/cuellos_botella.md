# Capacidad horaria y cuellos de botella

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A) · Fase 0

> **Alcance:** por qué la velocidad de la línea principal **no** es la capacidad de la planta; capacidad horaria en 6 / 8 / 10 / 16 h netas; diferencia entre velocidad nominal, operativa, disponibilidad, paradas, limpieza, cambios de producto, mantenimiento y microparadas; ventana horaria total del establecimiento; y cuellos de botella por sistema. **No** elige escala, turnos (DEC-036), equipos ni método de enfriamiento.
> **Modelo:** [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py) → [`capacidad_proceso.csv`](capacidad_proceso.csv) (13 tests, 5 mutaciones detectadas). Definiciones de capacidad nominal / operativa / utilización: [`capacidad_preliminar.md` §1](capacidad_preliminar.md) (SUP-052, no se repiten).
> **Clasificación:** los ritmos son `[ESTIMACIÓN]` aritmética; la eficiencia global, los tiempos no productivos, la residencia en el enfriamiento y las productividades manuales son **sensibilidades** `[SUPUESTO]` (SUP-09A-01 a SUP-09A-04) o extractos `[PVDP]`. **Ninguna cifra es un dato medido en una planta argentina.**

---

## 1. La regla central

```
capacidad de la planta = capacidad de su etapa más lenta (cuello de botella)
                       ≠ velocidad nominal de la línea de faena
```

Una planta es una **cadena**: recepción → colgado → faena → evisceración + inspección → enfriamiento → clasificación → trozado/deshuese → envasado → congelado → cámaras → expedición, más los **servicios** (agua, efluentes, frío, energía, vapor, aire), la **organización** (personal, limpieza, mantenimiento) y los **flujos laterales** (sangre, plumas, vísceras). Si cualquiera de esos eslabones procesa menos, la planta procesa menos, aunque la línea de faena pueda ir más rápido. Test T03 del modelo.

**Ejemplo didáctico** (números hipotéticos, **no** son datos ni una recomendación):

| Etapa | Capacidad hipotética (aves/día) |
|---|---|
| Línea de faena (nominal × horas × eficiencia) | 20.000 |
| Evisceración + inspección | 18.000 |
| Enfriamiento | 19.000 |
| **Sala de trozado** | **15.000** ← cuello de botella |
| Cámaras (días de stock) | 17.000 |
| **Capacidad de la planta** | **15.000** |

Comprar una línea de faena más rápida no mueve la capacidad: hay que ampliar la sala de trozado, y después aparecerá el siguiente cuello (cámaras, 17.000).

## 2. Seis conceptos de velocidad y tiempo

| Concepto | Definición | Ejemplo de lo que la reduce |
|---|---|---|
| **Velocidad nominal** | Aves/h que el equipo procesa según su especificación, funcionando sin interrupciones | — (la declara el fabricante; FTE-09A-001, FTE-09A-003, FTE-09A-007 publican rangos nominales) |
| **Velocidad operativa** | Aves/h reales **mientras** la línea está en marcha | Grilletes vacíos (colgado incompleto), aves fuera de calibre que obligan a bajar la velocidad, operarios que no llegan al ritmo |
| **Disponibilidad** | Fracción de las horas netas programadas en que la línea está efectivamente en marcha | Paradas por fallas, esperas de aves, trabas, cortes de energía o agua |
| **Paradas** | Interrupciones de minutos a horas | Avería de un equipo crítico, falta de camión de aves, rotura de grillete |
| **Microparadas** | Interrupciones de segundos a pocos minutos, que no se registran como parada pero suman | Atascos en transferencias, ajustes, aves mal colgadas |
| **Limpieza intermedia** | Limpieza parcial durante el turno | Pausa de almuerzo con lavado de equipos, cambio de lote |
| **Cambio de producto** | Tiempo para pasar de un producto o calibre a otro | Cambio de programa de trozado, de envase o de etiqueta; lotes de exportación (Halal, destino) |
| **Mantenimiento** | Tiempo reservado para mantener equipos | Preventivo diario (lubricación, cuchillas, dedos de desplumadora) y semanal |

**Eficiencia global η** (concepto análogo al OEE de la industria): `producción real = velocidad nominal × horas netas × η`, con η = disponibilidad × (velocidad operativa / nominal) × fracción de aves que no se reprocesan. **No hay dato argentino de η** (DPV-09A-01); se usa 0,70 / 0,80 / 0,90 como sensibilidad (SUP-09A-01). Ejemplo de descomposición ilustrativa: disponibilidad 0,92 × rendimiento de velocidad 0,90 ≈ 0,83.

## 3. Capacidad horaria requerida

`[ESTIMACIÓN]`. Ritmo operativo = aves/día ÷ horas netas (idéntico a [`../23_plan_expansion/escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv), test T01). Ritmo **nominal** que habría que pedir a un equipo = operativo ÷ η.

| Escala (aves/día) | h netas | Ritmo operativo (aves/h) | Nominal η 0,90 | Nominal η 0,80 | Nominal η 0,70 | Segundos por ave |
|---|---|---|---|---|---|---|
| 2.500 | 6 | 417 | 463 | 521 | 595 | 8,6 |
| 2.500 | **8** | **312** | 347 | 391 | 446 | 11,5 |
| 2.500 | 10 | 250 | 278 | 312 | 357 | 14,4 |
| 2.500 | 16 | 156 | 174 | 195 | 223 | 23,0 |
| 5.000 | 6 | 833 | 926 | 1.042 | 1.190 | 4,3 |
| 5.000 | **8** | **625** | 694 | 781 | 893 | 5,8 |
| 5.000 | 10 | 500 | 556 | 625 | 714 | 7,2 |
| 5.000 | 16 | 312 | 347 | 391 | 446 | 11,5 |
| 10.000 | 6 | 1.667 | 1.852 | 2.083 | 2.381 | 2,2 |
| 10.000 | **8** | **1.250** | 1.389 | 1.562 | 1.786 | 2,9 |
| 10.000 | 10 | 1.000 | 1.111 | 1.250 | 1.429 | 3,6 |
| 10.000 | 16 | 625 | 694 | 781 | 893 | 5,8 |
| 20.000 | 6 | 3.333 | 3.704 | 4.167 | 4.762 | 1,1 |
| 20.000 | **8** | **2.500** | 2.778 | 3.125 | 3.571 | 1,4 |
| 20.000 | 10 | 2.000 | 2.222 | 2.500 | 2.857 | 1,8 |
| 20.000 | 16 | 1.250 | 1.389 | 1.562 | 1.786 | 2,9 |

**Lo que produce una línea de ritmo nominal dado** (aves/día = L × h × η; líneas ilustrativas, no modelos de proveedor):

| Línea nominal (aves/h) | 8 h · η 0,90 | 8 h · η 0,80 | 8 h · η 0,70 | 10 h · η 0,80 | 16 h · η 0,80 |
|---|---|---|---|---|---|
| 312 | 2.250 | 2.000 | 1.750 | 2.500 | 4.000 |
| 625 | 4.500 | 4.000 | 3.500 | 5.000 | 8.000 |
| 1.250 | 9.000 | 8.000 | 7.000 | 10.000 | 16.000 |
| **2.500** | 18.000 | **16.000** | 14.000 | 20.000 | 32.000* |
| 3.125 | 22.500 | 20.000 | 17.500 | 25.000 | 40.000* |

\* Solo si existen 16 h netas, lo que la §4 muestra como difícil o inviable.

**Lectura:** una línea de 2.500 aves/h **nominales** con 8 h netas y η = 0,80 produce ~16.000 aves/día, no 20.000 (test T11). Para 20.000 aves/día con 8 h netas habría que especificar ~2.800–3.600 aves/h nominales **en todas las etapas**, o más horas netas. Lo mismo vale en cada escala: la cifra "8 h × ritmo = escala" supone η = 1, que no existe.

## 4. Horas netas de faena ≠ tiempo total del establecimiento

La planta funciona muchas más horas que las que la línea recibe aves. `[ESTIMACIÓN]` con tiempos de sensibilidad (SUP-09A-02; ningún dato argentino, DPV-082, DPV-09A-04):

| Componente (h/día) | Baja | Media | Alta |
|---|---|---|---|
| Preoperativo (inspección preoperacional, arranque de equipos y frío) | 0,50 | 0,75 | 1,00 |
| Pausas del personal, por cada 8 h netas | 0,50 | 0,75 | 1,00 |
| Limpieza intermedia, por cada 8 h netas | 0,25 | 0,33 | 0,50 |
| Cierre y vaciado de línea (últimas aves hasta el final del proceso) | 0,50 | 0,75 | 1,00 |
| **Limpieza y sanitización final** (prelavado, espuma, enjuague, desinfección, inspección) | 3,0 | 4,0 | 6,0 |
| Mantenimiento no solapable con la limpieza | 0,5 | 1,0 | 2,0 |

| h netas | Ventana total baja · holgura | Media · holgura | Alta · holgura |
|---|---|---|---|
| 6 | 11,1 · 12,9 | 13,3 · 10,7 | 17,1 · 6,9 |
| 8 | 13,2 · 10,8 | 15,6 · 8,4 | 19,5 · 4,5 |
| 10 | 15,4 · 8,6 | 17,9 · 6,1 | 21,9 · 2,1 |
| **16 (2 × 8)** | 22,0 · **2,0** | 24,7 · **−0,7** | 29,0 · **−5,0** |

**Lecturas:**

1. Con 8 h netas, el establecimiento opera **13–20 h/día** (faena + preparación + limpieza + mantenimiento).
2. **16 h netas (dos turnos de faena) no entran en 24 h** con tiempos medios o altos y dejan solo ~2 h con tiempos bajos: el segundo turno **come la ventana de sanitización y de mantenimiento**. Por eso no se asume un segundo turno sin estudiar estos tiempos (DEC-036). Referencia `[PVDP · débil]`: plantas de EE.UU. reservan un turno de ~8 h para sanitización después de jornadas de 16–20 h (FTE-09A-028), lo que es compatible con el orden de magnitud de esta tabla.
3. Alternativas conceptuales que se deben evaluar (no decididas): 10 h netas en un turno extendido; 6.° día; sanitización parcial por zonas con equipos redundantes; o capacidad nominal mayor con un solo turno.
4. La ventana del modelo **no depende de la escala** (test T06): es una simplificación. En la realidad, una planta más grande tiene más equipos que limpiar, pero también más personal de limpieza; se registra como dato a relevar (DPV-09A-04).

## 5. Cuellos de botella por sistema

Cada fila: por qué limita, qué indicador usar, cómo varía con la escala y qué dato falta. Cifras de carga del modelo (config. B, 8 h netas).

| Sistema | Por qué puede limitar | Indicador de carga | 2.500 → 20.000 aves/día (8 h) | Mitigación conceptual | Dato faltante |
|---|---|---|---|---|---|
| **Abastecimiento y espera de aves** | Si no llegan aves al ritmo, la línea para; si esperan demasiado, mueren o pierden calidad | Aves/h que deben llegar; camiones/día | 312 → 2.500 aves/h vivas | Programación de carga en granja; andén ventilado | Capacidad de camión (DPV-084); tiempos de viaje (DEC-003) |
| **Colgado** | Operación manual repetitiva y exigente; el ritmo por persona es limitado y la rotación es alta | Aves/min por colgador | 5,2 → 41,7 aves/min. Puestos equivalentes: 1 → 2 (ritmo de referencia de líneas de EE.UU., 23 aves/min) o 1 → 4 (prudente, 50 %) | Rotación de puestos; más puestos; ritmo por debajo del máximo (bienestar: estándar privado de 35 aves/min de línea, FTE-09A-027) | Productividad y rotación reales en Argentina (DPV-09A-05). Los puestos del modelo **no son dotación**: no incluyen rotación, pausas ni ausentismo |
| **Evisceración** | Manual: mucha mano de obra; automática: la calibración depende de la uniformidad del lote y cualquier falla detiene la línea | Aves/h por operario o por máquina | Manual: 3 → 21 puestos equivalentes (referencia 2 aves/min por operario, FTE-09A-025) o 6 → 42 (prudente). Por encima de ~1.000 aves/h la evisceración manual deja de ser práctica (FTE-09A-025 `[PVDP]`) | Semiautomática en escalas bajas; automática en altas; puestos de repaso | Productividad argentina; tolerancia de equipos a pesos variables |
| **Inspección veterinaria** | El servicio oficial inspecciona ave por ave; si el ritmo excede lo que los inspectores pueden examinar, la línea debe bajar | Aves/min por puesto de inspección | 5 → 42 aves/min | Presentación automática de vísceras; puestos suficientes; acuerdo con SENASA | **Norma sobre puestos/inspectores por velocidad de línea** (DPV-09A-03) |
| **Enfriamiento (chiller)** | Tiempo de residencia fijo: la capacidad depende del volumen o de la longitud del recorrido | Carcasas simultáneas dentro del sistema | Inmersión (50 min): 260 → 2.083 carcasas; aire (90–150 min): 469–781 → 3.750–6.250 carcasas | Dimensionar por la escala final o modularizar (segundo tanque, más recorrido); DEC-026 | Tiempos y temperaturas objetivo por norma (FTE-09A-030 `[PVDP]`) y por equipo |
| **Clasificación** | Si es manual, depende de personas; si es automática, de la balanza de línea | Aves/h | 312 → 2.500 | Balanza de línea con distribución | — |
| **Trozado** | Manual: mano de obra y temperatura de la sala; automático: un equipo de alto costo que puede ser el cuello si se para | kg/h a trozar | 636 → 5.091 kg/h | Mesas manuales en escalas bajas; trozado automático en altas; sala ampliable | Productividad manual (kg/h/operario) |
| **Deshuese** | Muy intensivo en mano de obra; el equipo automático es específico por pieza | kg/h a deshuesar (config. C) | 359 → 2.875 kg/h; piezas de pata-muslo: 625 → 5.000/h. Referencia de un equipo automático de pata-muslo: 1.000 piezas/h (FTE-09A-018 `[PVDP]`) | Deshuese manual en conos; automatizar primero la pieza de mayor volumen | Productividad manual; mix real (DPV-037) |
| **Packaging** | Cada formato (bolsa, bandeja, termoformado, vacío, MAP) es una máquina distinta con su ritmo y sus cambios | Envases/min por formato; cambios de formato por día | Comestible a empaque 749 → 5.991 kg/h | Pocos formatos al inicio; máquinas por familia de producto | Mix de formatos por cliente (DPV-041) |
| **Congelado** | El producto debe llegar a −18 °C en el centro; el tiempo de congelado fija la capacidad del túnel o espiral | t/día a congelar | P1 0,6 → 4,8; P2 2,4 → 19,2; P3 3,0 → 24,0 t/día | Congelado de terceros al inicio; túnel modular | Tiempo de congelado por producto y envase (DPV-09A-10) |
| **Cámaras** | Stock para completar pedidos y contenedores | t en stock | 7 días de producción: 42 → 336 t ([`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) §2) | Cámaras modulares; frío de terceros | Días de stock según clientes y exportación |
| **Expedición** | Andenes, tiempo de carga y ventanas horarias de clientes | t/día a despachar; camiones/día | 6,0 → 47,9 t peso comercial por día operativo | Andenes con sello; turnos de carga desfasados de la faena | Capacidad de camión y ventanas de entrega (DPV-084, DPV-036) |
| **Limpieza y sanitización** | Consume la ventana horaria (§4) | h/día | 3–6 h/día sensibilidad | Diseño higiénico (fácil de limpiar); equipos de limpieza centralizados | Tiempos reales (DPV-09A-04) |
| **Agua** | Escaldado, lavado, chiller, limpieza: litros por ave (no dimensionado) | m³/día | Proporcional a aves (a calcular en `11_agua_efluentes`) | Recirculación donde la norma lo permita | Consumo por ave (`11_agua_efluentes`) |
| **Efluentes** | Caudal y carga orgánica diarios; permiso de vuelco | m³/día y kg DQO/día | Proporcional; la sangre no recuperada es la mayor carga evitable | Recuperar sangre; separar sólidos | `11_agua_efluentes` |
| **Frío** | Carga térmica del enfriamiento de carcasas, salas, túneles y cámaras | kW de frío | Proporcional a kg/h y a perfil de congelado | Sala de máquinas ampliable | `12_energia_frio` |
| **Mano de obra** | Colgado, evisceración, trozado, deshuese y empaque son intensivos; disponibilidad local limitada | Personas por turno | Crece casi linealmente sin automatización | Automatizar donde la mano de obra es el límite | `18_recursos_humanos` |
| **Subproductos** | Si el receptor no retira, la faena se detiene (no hay dónde poner plumas y vísceras) | t/día a retirar | Sólidos: 1,5 → 12,2 t/día; sangre 0,2 → 1,7 t/día | Dos receptores o almacenamiento de contingencia ([`../07_subproductos/conclusiones_valorizacion.md` §10](../07_subproductos/conclusiones_valorizacion.md)) | DPV-065, DPV-080 |

## 6. Por qué la línea principal no es la capacidad real

1. **η < 1:** paradas, microparadas y huecos reducen la producción real (§3).
2. **Otras etapas más lentas:** evisceración manual, inspección, trozado o deshuese manual, envasado con muchos formatos (§5).
3. **Etapas con tiempo de residencia:** enfriamiento y congelado no se aceleran subiendo la velocidad; dependen del volumen instalado.
4. **Servicios:** sin agua, frío, efluentes o energía suficientes, la línea no puede ir a su ritmo.
5. **Ventana horaria:** la limpieza y el mantenimiento compiten con las horas de faena (§4).
6. **Mano de obra:** en escalas chicas y medianas la capacidad la marca la gente, no la máquina.
7. **Mix de productos:** el cuello de botella cambia con el producto. Una planta de pollo entero tiene su cuello en faena/enfriamiento/embolsado; una de trozado, en la sala de trozado; una de deshuesado, en el deshuese (misma cantidad de aves, [`../23_plan_expansion/escenarios_escala.md` §9](../23_plan_expansion/escenarios_escala.md)).
8. **Subproductos:** si no se retiran, la planta se detiene.

## 7. Qué verificar antes de usar un segundo turno como palanca

Condición necesaria, no suficiente (DEC-036): (1) ventana de sanitización y mantenimiento compatible (§4); (2) mano de obra para dos turnos (convenio, DPV-082); (3) abastecimiento de aves 16 h por día y espera nocturna; (4) enfriamiento, frío, cámaras y congelado para el doble de producción diaria; (5) agua y permiso de vuelco para el doble de caudal diario; (6) retiro de subproductos dos veces por día; (7) inspección oficial en ambos turnos; (8) expedición y clientes que absorban el doble.
