# Arquitecturas conceptuales de planta por escala, flexibilidad y modularidad

**Fecha:** 2026-09-30 · **Versión:** 1.1 (sesión 09A; corrección: factores de eficiencia solo como sensibilidad, evisceración manual sin umbral fijo, niveles como arquitectura de referencia) · Fase 0

> **Alcance:** para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo: ritmo de línea, nivel de automatización razonable **a estudiar**, operaciones que pueden ser manuales, operaciones que probablemente requieran automatización, cuellos de botella principales y módulos para crecer. Además: flexibilidad entre productos (§7) y modularidad (§8). **No** se elige escala, número de líneas, turnos, modelos de equipo, proveedor, layout ni localización; **no** se calcula CAPEX/OPEX.
> **Relación con otros módulos:** las arquitecturas de **crecimiento** (A escalonada, B arranque intermedio, C arranque grande, D validación comercial + turnos, E obra grande equipada por etapas) y la clasificación "sobredimensionar / preparar / construir por módulos" están en [`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md) y no se repiten; este documento describe **qué hay adentro de la planta** en cada escala. Cargas: [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py) y [`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md). Niveles por equipo: [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv).
> **Clasificación:** cargas `[ESTIMACIÓN]`; niveles de automatización y arquitecturas `[SUPUESTO]` de trabajo (SUP-09A-05). Ninguna es recomendación.

---

## 1. Base común a todas las escalas

Toda planta con habilitación SENASA, de cualquier escala, necesita: recepción con espera ventilada; aturdido–sangrado–escaldado–desplumado (la **arquitectura de referencia a estudiar** es una línea continua mecanizada o automática; no se afirma que otra configuración sea imposible sin respaldo normativo, DPV-09A-03); separación física faena / evisceración / zona limpia ([`zonificacion_higienica.md`](zonificacion_higienica.md)); puestos de inspección oficial; enfriamiento continuo; sala de clasificación y trozado mínima (canales no aptas para entero); empaque; cámaras; circuitos separados de sangre, plumas, vísceras y decomisos; agua potable, agua caliente, frío, aire comprimido, tratamiento de efluentes; vestuarios por zona y oficina del servicio oficial. **Lo que cambia con la escala es el tamaño, el grado de automatización y la cantidad de personas, no la lista de sistemas.**

## 2. Tabla resumen

`[ESTIMACIÓN]` config. B (trozado), 2,9 kg, inmersión, 5 d/sem.

| Variable | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Ritmo operativo 6 / 8 / 10 / 16 h netas (aves/h) | 417 / **312** / 250 / 156 | 833 / **625** / 500 / 312 | 1.667 / **1.250** / 1.000 / 625 | 3.333 / **2.500** / 2.000 / 1.250 |
| Nominal a pedir a 8 h netas en marcha (R 0,95–0,82, **sensibilidad**) | 329–381 | 658–762 | 1.316–1.524 | 2.632–3.049 |
| Nominal si las 8 h incluyeran paradas (η 0,90–0,70, **sensibilidad**) | 346–448 | 693–897 | 1.385–1.793 | 2.770–3.587 |
| Aves por minuto a 8 h | 5,2 | 10,4 | 20,8 | 41,7 |
| Pollo vivo t/día | 7,3 | 14,5 | 29,0 | 58,0 |
| Comestible (peso comercial) t/día operativo | 6,0 | 12,0 | 24,0 | 47,9 |
| Sólidos a retirar t/día (subproductos C + decomisos + contenido GI) | 1,5 | 3,0 | 6,1 | 12,2 |
| Carcasas en el enfriamiento a 8 h (inmersión 50 min · aire 90–150 min) | 260 · 469–781 | 521 · 938–1.562 | 1.042 · 1.875–3.125 | 2.083 · 3.750–6.250 |
| A congelar t/día (P1 · P2 · P3) | 0,6 · 2,4 · 3,0 | 1,2 · 4,8 · 6,0 | 2,4 · 9,6 · 12,0 | 4,8 · 19,2 · 24,0 |
| Stock de 7 días de producción (t) | 42 | 84 | 168 | 336 |
| Eviscerado manual: puestos equivalentes a 8 h (ref. · prudente) | 3 · 6 | 6 · 11 | 11 · 21 | 21 · 42 |

## 3. Escala 2.500 aves/día

| Aspecto | Contenido |
|---|---|
| **Ritmo** | 312 aves/h a 8 h netas (5,2 aves/min; 11,5 s por ave). Equipos de línea continua en su rango más bajo; existen líneas compactas de 150–1.500 aves/h (FTE-09A-015 `[PVDP]`) y plantas compactas de ~600–1.600 broilers/h con evisceración manual (FTE-09A-007, fuente primaria del fabricante) — capacidades **nominales declaradas**, no de diseño |
| **Automatización razonable a estudiar** | Línea continua solo en aturdido → desplumado y enfriamiento; resto **manual o semiautomático** |
| **Operaciones manuales posibles** | Descarga, colgado, degüello (con repaso), corte de patas y cabeza, transferencia, **evisceración completa**, menudencias, clasificación, trozado, deshuese, embolsado, encajonado |
| **Probablemente mecanizadas o automáticas (arquitectura de referencia)** | Aturdido, escaldado, desplumado, transportador aéreo, enfriamiento |
| **Cuellos de botella principales** | **Mano de obra** (casi todo es manual); personal polivalente que cambia de zona (riesgo higiénico); **subproductos**: 1,5 t/día es poco para interesar a un receptor ([`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md)); escala mínima eficiente desconocida (DPV-083); congelado probablemente de terceros |
| **Módulos para crecer** | Más puestos manuales; segundo turno (156 aves/h a 16 h); para pasar a 5.000: la línea continua debe haberse especificado con margen (aturdidor, escaldadora y desplumadoras dimensionados para ≥ 625–900 aves/h) o se reemplaza |
| **Riesgo de diseño** | Comprar equipos "justos" de 300–400 aves/h que luego no se amplían (reemplazo total al crecer) |

## 4. Escala 5.000 aves/día

| Aspecto | Contenido |
|---|---|
| **Ritmo** | 625 aves/h a 8 h (10,4 aves/min; 5,8 s por ave); 833 aves/h si solo hay 6 h netas |
| **Automatización razonable a estudiar** | Faena continua; **evisceración manual o semiautomática** (625–833 aves/h según horas netas: dentro del rango en que un fabricante documenta evisceración manual, hasta ~1.600 aves/h); clasificación y trozado semiautomáticos |
| **Operaciones manuales posibles** | Colgado, transferencia, evisceración (6–11 puestos equivalentes), menudencias, trozado en mesa con sierras, deshuese en conos, trimming |
| **Probablemente mecanizadas o automáticas** | Descarga asistida, degüello con repaso, escaldado, desplumado, enfriamiento, lavado de carcasas, balanza de línea, envasado de bandeja |
| **Cuellos de botella principales** | **Evisceración e inspección** (ritmo de puestos manuales); **sala de trozado** si el mix es trozado; empaque si hay muchos formatos; ventana de limpieza si se pretende un segundo turno |
| **Módulos para crecer** | Evisceración semiautomática → automática; trozadora compacta; segundo tanque de enfriamiento; túnel de congelado estático; segundo turno (312 aves/h a 16 h) |
| **Riesgo de diseño** | Quedar "en el medio": demasiado grande para lo manual y demasiado chica para diluir la automatización |

## 5. Escala 10.000 aves/día

| Aspecto | Contenido |
|---|---|
| **Ritmo** | 1.250 aves/h a 8 h (20,8 aves/min; 2,9 s por ave); 1.667 aves/h con 6 h |
| **Automatización razonable a estudiar** | **Evisceración manual, semiautomática o automática a comparar** (1.250 aves/h a 8 h: dentro del rango con evisceración manual documentado por un fabricante; la decisión depende de costo y disponibilidad de mano de obra, ergonomía, inspección, uniformidad e higiene, DEC-09A-01); clasificación por balanza de línea; trozado semiautomático o automático según mix; envasado automático; subproductos por canal/vacío |
| **Operaciones manuales posibles** | Colgado (con rotación), repaso de degüello, inspección (humana por definición), trimming, deshuese en conos, garras (si hay mercado), trozado de canales defectuosas |
| **Probablemente mecanizadas o automáticas** | Tramo faena → enfriamiento, transferencia, presentación para inspección, clasificación, envasado principal; evisceración y menudencias según la comparación anterior |
| **Cuellos de botella principales** | **Enfriamiento** (~1.000 carcasas en inmersión o ~1.900–3.100 en aire); **inspección** (puestos por velocidad, DPV-09A-03); **deshuese** si el mix lo exige (1.438 kg/h en config. C); **congelado** (hasta 12 t/día con P3); **subproductos** (6,1 t/día: flujo industrial que requiere receptor confiable) |
| **Módulos para crecer** | Segundo turno (625 aves/h a 16 h, sujeto a la ventana horaria, [`cuellos_botella.md` §4](cuellos_botella.md)) **o** segunda línea en espacio reservado; módulos de trozado; deshuese automático por pieza; túnel continuo o espiral; cámaras modulares |
| **Riesgo de diseño** | Asumir que 1.250 aves/h × 16 h = 20.000 aves/día sin revisar limpieza, mantenimiento, frío, efluentes y personal |

## 6. Escala 20.000 aves/día

| Aspecto | Contenido |
|---|---|
| **Ritmo** | 2.500 aves/h a 8 h (41,7 aves/min; 1,4 s por ave); nominal a pedir ~2.600–3.600 aves/h según los factores de **sensibilidad** (la cifra real sale de la velocidad **garantizada** en RFQ). Referencia tecnológica argentina: Calisa2 arrancó a 9.500 aves/h, preparada para 15.000 (FTE-09A-004, fuente primaria del fabricante), ~3,8 veces este ritmo — **no es benchmark** de CAPEX, dotación, costo por ave, escala mínima eficiente ni automatización ([`../08_maquinaria/proveedores_preliminares.md` §1.1](../08_maquinaria/proveedores_preliminares.md)) |
| **Automatización razonable a estudiar** | Automatización amplia en faena, evisceración, clasificación, trozado, envasado y congelado continuo; evaluar descarga por módulos y aturdido CAS |
| **Operaciones manuales posibles** | Colgado (más puestos y rotación; 2–4 puestos equivalentes solo en ritmo), inspección, repaso, trimming, clasificación de defectos, parte del deshuese |
| **Probablemente mecanizadas o automáticas** | Casi todas las demás; la evisceración manual no se descarta, pero implicaría 21–42 puestos equivalentes (tamaño del problema de personal, no límite técnico) |
| **Cuellos de botella principales** | **Colgado** (ritmo humano), **enfriamiento** (~2.100 carcasas en inmersión; 3.750–6.250 en aire), **congelado** (hasta 24 t/día con P3), **cámaras** (336 t en 7 días de producción), **expedición** (~48 t/día), **agua y efluentes**, **frío**, **subproductos** (12,2 t/día: aquí el rendering propio se vuelve pregunta pertinente, no decidida), **mano de obra** de salas de corte |
| **Módulos para crecer** | Más allá de 20.000 queda fuera del estudio; la pregunta es cómo **llegar** (§8) |
| **Riesgo de diseño** | Una sola línea de alta velocidad sin redundancia: cualquier falla crítica detiene 20.000 aves/día |

## 7. Flexibilidad de producto

¿Qué necesita la planta para pasar entre productos? `C` = operación común a todos; `+` = módulo adicional.

| Producto | Operaciones comunes (E01–E20) | Módulos adicionales | Qué cambia en frío y empaque | Tiempo de cambio |
|---|---|---|---|---|
| **Pollo entero** | C | Embolsadora; menudencias en bolsita (si van dentro); calibrado por peso | Refrigerado o congelado en caja | Bajo |
| **Trozado** | C | Sala de trozado (mesas o trozadora); bandejas | Bandeja + film; más superficie de sala limpia | Medio (programa de corte, formato) |
| **Deshuesado** | C | Línea de conos o deshuesadoras; trimming; rayos X opcional; destino para hueso y piel | Envasado al vacío/MAP; sala refrigerada más grande | Alto (personal especializado) |
| **Refrigerado** | C | Cámaras 0–4 °C (a verificar); despacho diario | Vida útil de días (DPV-078) | — |
| **Congelado** | C | Túnel/espiral/placas; cámara −18 °C | Envase apto para congelado; rotulado | Medio |
| **Exportación** | C + **estándar del destino** (listado de planta, bienestar, trazabilidad por lote) | Calibración, congelado, cámaras para completar contenedores, andén reefer, rotulado por destino; eventual Halal (DPV-034) | Congelado; lotes segregados | Alto (lotes, auditorías, documentación) |
| **Mercado interno** | C | Formatos de góndola y mayorista | Refrigerado mayormente | — |

**Lecturas:**

1. **Todo lo que está antes de la clasificación es común.** La flexibilidad se decide **después** del enfriamiento: salas de corte, empaque, congelado y cámaras.
2. **Lo difícil de agregar después** no son las máquinas sino el **espacio refrigerado** contiguo a la salida del chiller (salas de corte y deshuese), la **capacidad de frío** y el **estándar higiénico** de exportación ([`../17_exportacion/requisitos_planta_exportadora.md` §3](../17_exportacion/requisitos_planta_exportadora.md)).
3. **Cambiar de producto tiene costo en tiempo:** cada cambio de programa de trozado, formato de envase o lote de exportación consume minutos u horas de la ventana ([`cuellos_botella.md` §2](cuellos_botella.md)). Una planta flexible con muchos productos **produce menos aves por día** que una planta de pocos productos con los mismos equipos.
4. **La asignación de cada parte al mejor mercado** (principio de ingreso total por ave) exige al menos: trozado, congelado, clasificación por calibre y salas de coproductos (garras, menudencias). Deshuese y CMS son módulos que se agregan con mercado probado.

## 8. Modularidad

### 8.1 Qué hacer con cada equipo al crecer

Columna `modularidad` de [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv). Resumen:

| Acción al crecer | Equipos típicos | Condición para que funcione |
|---|---|---|
| **Mantener** | Balanza de camiones, aturdidor (si su rango lo cubre), lavado de camiones, lavadora de grilletes | Haber especificado el rango final desde el inicio |
| **Duplicar** | Calderas, compresores de frío y aire, puestos de inspección, puestos manuales, esterilizadores, túneles estáticos, balanzas etiquetadoras, envasadoras, deshuesadoras por pieza | Espacio y troncales de servicios previstos |
| **Ampliar** | Transportador aéreo (más grilletes y velocidad), escaldadora modular, desplumadoras en serie, chiller (tanque adicional), trozadora modular, cámaras modulares, andén de espera, canales de subproductos | Recorrido, espacio y estructura previstos en la obra inicial |
| **Reemplazar** | Evisceración manual → automática; descarga manual → módulos; transferencia manual → automática; embolsado manual → automático; clasificación manual → balanza de línea | Aceptar que el equipo de la etapa anterior se vende o se reubica (p. ej., como línea de reserva) |

### 8.2 Una línea rápida vs dos líneas

Ejemplo conceptual para 20.000 aves/día a 8 h netas (2.500 aves/h operativas):

| Criterio | 1 línea × ~2.600–3.600 aves/h nominales (sensibilidad) | 2 líneas × ~1.300–1.800 aves/h nominales (sensibilidad) |
|---|---|---|
| Equipos | Menos unidades, más grandes | Duplicados (dos evisceradoras, dos chillers o uno compartido) |
| Redundancia | **Ninguna**: una falla crítica detiene todo | Una línea sigue si la otra se detiene (la planta cae a ~50 %) |
| Crecimiento | Se compra de una vez (o se amplía una línea prevista) | Se puede instalar la primera línea y agregar la segunda en espacio reservado (arquitecturas D y E) |
| Flexibilidad | Un solo calibre/producto a la vez | Cada línea puede trabajar pesos o productos distintos |
| Personal | Menos supervisión por ave | Más puestos de colgado, inspección y supervisión |
| Superficie | Menor | Mayor |
| Mantenimiento | Un solo parque de repuestos | Dos parques (si son iguales, se comparten repuestos) |
| Inspección oficial | Puestos concentrados | Puestos en ambas líneas |
| Costo | No se calcula (CAPEX pendiente) | No se calcula |

**Otras combinaciones** (conceptuales, no recomendadas): 1 línea de ~1.300–1.800 aves/h nominales para 10.000 aves/día con 8 h, ampliada a 20.000 con segundo turno **si** la ecuación de 24 h (hoy con alerta en escenarios medio y conservador, [`cuellos_botella.md` §4](cuellos_botella.md); a validar) y los demás sistemas lo permiten; o una línea especificada para el ritmo final pero equipada al inicio con menos módulos (concepto "línea ampliable" que documentan fabricantes: p. ej. Meyn LEAP, disposición inicial ~1.300 aves/h ampliable hasta ~15.000, FTE-09A-001, fuente primaria del fabricante; BAADER Compact Plant 396 con expansión prevista, FTE-09A-007). Esto prueba que **existen arquitecturas escalables**, **no** que una misma inversión inicial llegue automáticamente a la capacidad máxima: la ampliación exige equipos, espacio, servicios y obra previstos, y qué componentes se reemplazan debe preguntarse en el RFQ.

### 8.3 Trayectorias de crecimiento dentro de la planta

| Paso | Qué se mantiene | Qué se amplía | Qué se reemplaza | Qué se agrega |
|---|---|---|---|---|
| 2.500 → 5.000 | Edificio y zonas si se previeron; aturdidor | Transportador, escaldado, desplumado, chiller (si modulares); puestos manuales | Descarga manual (opcional) | Clasificadora; túnel estático; cámaras |
| 5.000 → 10.000 | Idem + clasificadora | Chiller, cámaras, frío, efluentes | **Evisceración manual → automática**; transferencia | Trozado semiautomático/automático; congelado continuo |
| 10.000 → 20.000 | Idem | Todo el tramo de faena (o segunda línea) | Posiblemente la línea completa si no se especificó ampliable | Segunda línea o segundo turno; salas de corte; espiral; cámaras |

**Regla de fondo** (coherente con [`../23_plan_expansion/arquitectura_escalable.md` §1](../23_plan_expansion/arquitectura_escalable.md)): conviene **prever** lo barato de dejar previsto y caro de corregir (recorrido del transportador, espacio para chiller y salas de corte, troncales de frío y agua, flujos higiénicos) y **construir por módulos** lo caro de tener ocioso (equipos automáticos, frío, cámaras). La configuración final **no** se recomienda en esta fase (DEC-09A-02).
