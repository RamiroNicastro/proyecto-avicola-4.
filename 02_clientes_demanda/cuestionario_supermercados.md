# Cuestionario para la red de supermercados y el potencial inversor

**Fecha:** 2026-09-29 · **Versión:** 1 · Uso: entrevista con el potencial inversor y con los responsables de compras y logística de la red. Contexto: [`supermercados.md`](supermercados.md).

**Objetivo:** pasar la red de categoría C condicionada a C firme, B o A ([`modelo_demanda.md` §1](modelo_demanda.md)) con datos verificables. **No** es una negociación comercial ni implica compromiso de ninguna de las partes.

---

## Instrucciones de uso

1. **Primero al inversor, después a compras.** El bloque 0 se trata solo con el potencial inversor. Los bloques 1–3 van, idealmente, al gerente de compras de perecederos (carnes/pollo) y al responsable de logística.
2. **Pedir datos, no opiniones.** Siempre que se pueda, pedir un **reporte del sistema** (kg y $ por producto, por local y por semana, últimos 12 meses) en lugar de estimaciones de memoria. Si solo hay estimaciones, anotarlas como tales.
3. **Confidencialidad:** ofrecer un acuerdo de confidencialidad si la red lo requiere. Los datos se usan solo para el estudio.
4. **Registro:** cada entrevista se registra en `25_fuentes/registro_fuentes.csv` como `tipo_fuente = entrevista` (fecha, persona, cargo, empresa) y las respuestas actualizan DPV-002, 003, 018, 020 y 036 a 043.
5. **Duración objetivo:** 45–60 minutos para las preguntas imprescindibles. Las importantes y deseables pueden enviarse por escrito después.

**Presentación sugerida (30 segundos):**
> "Estamos evaluando un proyecto avícola en Argentina y queremos entender cómo compra pollo la red: volúmenes, productos, proveedores y condiciones. No venimos a vender todavía: necesitamos datos reales para decidir si el proyecto tiene sentido y cómo diseñarlo. Cualquier información es confidencial."

---

## Bloque 0 — Solo con el potencial inversor (imprescindible)

| # | Pregunta | Para qué |
|---|---|---|
| 0.1 | ¿Cuál es su relación con la red: propietario, socio, directivo, proveedor, contacto personal? ¿Es una sola empresa o varias sociedades? | Partes vinculadas y poder real de decisión (DPV-038) |
| 0.2 | ¿Quién decide la compra de pollo? ¿Se decide centralmente o cada local/sociedad por separado? | Saber con quién validar (DPV-002) |
| 0.3 | ¿Estaría dispuesto a facilitar datos de compras de pollo y una reunión con compras y logística? | Viabilidad de la validación |
| 0.4 | Si fuera a la vez inversor y cliente, ¿cómo imagina los precios y plazos: de mercado, preferenciales? ¿Aceptaría reglas escritas para operar entre partes vinculadas? | Gobierno y concentración (DEC-019) |
| 0.5 | ¿Su interés en invertir depende de que el proyecto abastezca a la red, o son decisiones independientes? | Separar la decisión de inversión de la comercial |

---

## Bloque 1 — IMPRESCINDIBLES (cambian el tamaño de la planta o la viabilidad del canal)

| # | Tema | Pregunta | Dato esperado | Registro |
|---|---|---|---|---|
| 1.1 | Locales | ¿Cuántos locales tiene la red hoy? ¿Cuántos venden pollo fresco? Lista con dirección, formato (hiper / super / autoservicio / mayorista) y superficie aproximada | Lista de locales | DPV-002, DPV-018 |
| 1.2 | Ubicación | ¿En qué municipios y provincias están? ¿Hay locales fuera del AMBA? | Mapa | DPV-018 |
| 1.3 | Centros de distribución | ¿Tienen CD? ¿Reciben perecederos refrigerados en el CD o cada proveedor entrega en cada local? ¿Ubicación, horarios, cobran fee de CD? | Esquema logístico | DPV-036 |
| 1.4 | Volumen total | ¿Cuántos kg de pollo (todos los productos) compran por semana en toda la red? Idealmente, reporte de 12 meses | kg/semana | DPV-003 |
| 1.5 | Volumen por local | ¿Cuántos kg por semana compra un local chico, uno mediano y uno grande? | kg/local/semana por formato | DPV-003 |
| 1.6 | Productos | ¿Qué productos compran y en qué proporción: entero, pechuga/suprema, pata-muslo, alas, milanesas, menudencias, otros elaborados? | kg/semana por producto | DPV-037 |
| 1.7 | Proveedores | ¿Quiénes son sus proveedores actuales de pollo (marcas, empresas)? ¿Qué participación tiene cada uno? | Lista y % | DPV-020 |
| 1.8 | Precios | ¿A qué precio compran cada producto (sin IVA, puesto en local o en CD)? ¿Con qué descuentos y bonificaciones? | $/kg por producto, fecha | DPV-013, DPV-039 |
| 1.9 | Plazo de pago | ¿A cuántos días pagan a los proveedores de pollo? ¿Desde la factura o desde la entrega? ¿Medio de pago? | Días y medio | DPV-039 |
| 1.10 | Contratos y exclusividades | ¿Tienen contratos, acuerdos de exclusividad o de volumen mínimo con los proveedores actuales? ¿Hasta cuándo? | Sí/no, vencimiento | DPV-020 |
| 1.11 | Voluntad de compra | ¿Evaluarían incorporar un proveedor nuevo? ¿Para qué productos y qué parte del volumen? ¿Qué tendría que ofrecer? | Interés concreto | DPV-002 |
| 1.12 | Prueba y carta de intención | ¿Aceptarían una prueba piloto (qué volumen mínimo, en cuántos locales)? ¿Firmarían una carta de intención no vinculante con volumen y condiciones de referencia? | Volumen de prueba; sí/no LOI | DPV-002 |

## Bloque 2 — IMPORTANTES (cambian el diseño, los costos o el capital de trabajo)

| # | Tema | Pregunta | Registro |
|---|---|---|---|
| 2.1 | Estacionalidad | ¿Cómo varían las compras a lo largo del año (meses altos y bajos, fiestas, vacaciones, promociones)? | DPV-037 |
| 2.2 | Frecuencia de entrega | ¿Cuántas veces por semana reciben pollo? ¿En qué horarios? ¿Pedido mínimo por entrega? | DPV-036 |
| 2.3 | Refrigerado vs congelado | ¿Qué proporción compran refrigerada y qué proporción congelada? ¿En qué productos? | DPV-037 |
| 2.4 | Packaging | ¿Compran a granel (cajón) y fraccionan en el local, o en bandeja lista para góndola? ¿Atmósfera modificada? ¿Peso fijo o variable? | DPV-037 |
| 2.5 | Requisitos sanitarios y de alta | ¿Qué habilitación exigen (SENASA tránsito federal, provincial)? ¿Auditorías, certificaciones, seguros, vida útil mínima en recepción, códigos EAN/GS1, trazabilidad por lote, facturación electrónica o EDI? | DPV-041 |
| 2.6 | Problemas actuales | ¿Qué problemas tienen con los proveedores actuales: faltantes, calidad, precio, cumplimiento de horarios, devoluciones, crisis de algún proveedor? | DPV-020 |
| 2.7 | Devoluciones y mermas | ¿Qué productos devuelven y en qué casos? ¿Quién absorbe la merma en góndola? | DPV-039 |
| 2.8 | Costos comerciales | ¿Qué bonificaciones, aportes a promociones y folletos, fees de alta de producto, de apertura de locales o de CD cobran a los proveedores? | DPV-039 |
| 2.9 | Promociones | ¿Con qué frecuencia hacen promociones de pollo? ¿Quién financia el descuento? | DPV-039 |
| 2.10 | Marca propia / marca blanca | ¿Venden pollo con marca propia del supermercado? ¿Les interesaría? ¿O prefieren marca del proveedor? | DEC-015 |

## Bloque 3 — DESEABLES (afinan el modelo)

| # | Tema | Pregunta |
|---|---|---|
| 3.1 | Crecimiento | ¿Planean abrir o cerrar locales en los próximos 2–3 años? |
| 3.2 | Precio de venta al público | ¿A qué precio venden cada producto? ¿Qué margen buscan en pollo? |
| 3.3 | Rotación y quiebres | ¿Cuántos días de stock tienen? ¿Con qué frecuencia se quedan sin producto? |
| 3.4 | Elaborados | ¿Qué elaborados de pollo venden (nuggets, hamburguesas, marinados, prefritos)? ¿Son importados? ¿De quién? |
| 3.5 | Especificaciones | ¿Calibres de peso preferidos del pollo entero y de los cortes? ¿Con o sin menudencias? ¿Con o sin piel? |
| 3.6 | Exhibición | ¿Tienen carnicería asistida en los locales o solo autoservicio? |
| 3.7 | Otras proteínas | ¿Les interesaría el mismo proveedor para otros productos (huevos, cerdo)? *(solo informativo; fuera del alcance, SUP-006)* |
| 3.8 | Contactos | ¿Pueden recomendar otros compradores (mayoristas, gastronomía, otras cadenas)? |

---

## Tabla para completar (volumen por producto)

| Producto | kg/semana (red total) | kg/semana (local típico) | Refrigerado / congelado | Packaging | Proveedor principal | Precio sin IVA ($/kg, fecha) | Plazo de pago (días) |
|---|---|---|---|---|---|---|---|
| Pollo entero | | | | | | | |
| Pechuga / suprema / filet | | | | | | | |
| Pata-muslo | | | | | | | |
| Alas | | | | | | | |
| Milanesas | | | | | | | |
| Menudencias | | | | | | | |
| Otros elaborados | | | | | | | |
| **Total** | | | | | | | |

Todo valor en ARS debe registrarse con fecha y tipo de cambio (regla 2).

---

## Los 10 datos más importantes (si hay una sola reunión)

1. **Cantidad exacta de locales** que venden pollo y su **ubicación** (lista).
2. **kg de pollo comprados por semana** en toda la red (reporte de 12 meses, si es posible).
3. **kg por producto** (mix) y refrigerado vs congelado.
4. **Proveedor(es) actual(es)** y su participación.
5. **Contratos, exclusividades** y su vencimiento.
6. **Centros de distribución** y esquema logístico (entrega en CD o en cada local; frecuencia).
7. **Precios de compra** por producto (sin IVA, con descuentos) y **plazo de pago**.
8. **Quién decide** la compra y cuál es la **relación del inversor** con la red.
9. **Voluntad concreta de compra**: qué productos y qué parte del volumen.
10. **Volumen mínimo de prueba** y posibilidad de **carta de intención**.
