# Plan de validación comercial — de interés verbal a demanda documentada

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Plan general: [`../00_gestion_proyecto/plan_trabajo_campo.md`](../00_gestion_proyecto/plan_trabajo_campo.md) (olas O1 y O2) · Método: [`../00_gestion_proyecto/guia_recoleccion_evidencia.md`](../00_gestion_proyecto/guia_recoleccion_evidencia.md)

> **Objetivo:** convertir la demanda de categoría C/D en demanda B/A **con evidencia**, o descubrir que no existe. Hoy la demanda documentada es ~0 ([`conclusiones_demanda.md`](conclusiones_demanda.md)).
> **Regla central:** **el interés verbal no es demanda asegurada.** Un volumen sube de categoría solo con evidencia documental nueva ([`modelo_demanda.md` §1](modelo_demanda.md)).
> Este plan **ordena** los instrumentos existentes: el cuestionario de la red ([`cuestionario_supermercados.md`](cuestionario_supermercados.md)), la ficha de otros canales ([`canales_comerciales.md` §4](canales_comerciales.md)), el pipeline ([`estrategia_comercial.md` §4](estrategia_comercial.md)) y las tareas R/I/C ([`conclusiones_demanda.md` §6](conclusiones_demanda.md)). No los reemplaza.

---

## 1. Qué se busca por actor (resumen)

| Actor | Rol en el proyecto | Entrevistas iniciales | DPV | Ola |
|---|---|---|---|---|
| Red de ~90 supermercados | Posible cliente ancla | 1 reunión con compras + 1 con logística (vía inversores) | 002, 003, 020, 036, 037, 039, 041, 078, 085 | O1 |
| Mayoristas (carnes y avícolas) | Volumen, salida de partes y excedentes, precio de referencia | 5 | 013, 040, 070 | O2 |
| Distribuidores (a comercios y gastronomía) | Llegada a canal atomizado sin flota propia | 3 | 040, 042 | O2 |
| Pollerías y carnicerías | Canal tradicional, cobro rápido, cortes y menudencias | 8–10 (incluye la carnicería familiar) | 004, 013, 040, 070 | O0–O2 |
| Gastronomía (cadenas, catering, hoteles) | Especificación estable; pechuga, porcionados | 3–5 | 040 | O2 |
| Elaboradores e industria (milanesas, hamburguesas, chacinados) | Carcasa/CMS, recortes, piel, deshuesados | 3–5 | 040, 071, 079 | O2 |
| Exportadores y traders | Piso de valor de garras, menudencias, alas; excedentes | 2–3 | 026, 032, 077, 081 | O5 / O9 |

Las cantidades son un **mínimo para aprender el patrón**, no una muestra estadística. Si las primeras entrevistas de un actor muestran respuestas muy dispersas, ampliar antes de concluir.

---

## 2. Escala de evidencia comercial

| Nivel | Nombre | Qué tiene que existir (evidencia mínima) | Qué **no** alcanza | Categoría de demanda ([`modelo_demanda.md` §1](modelo_demanda.md)) | Uso en decisiones |
|---|---|---|---|---|---|
| E0 | Sin evidencia | Cliente nombrado por terceros o identificado en un listado, sin contacto con quien decide | — | D (si es solo mercado) o C sin confirmar | Ninguno |
| **E1** | **Interés general** | Minuta de una conversación con alguien del cliente que expresa interés | "Nos interesa", "cuando tengan planta, vemos", "compramos todo lo que produzcan" | C (si hay volumen estimado de fuente identificable) | Ninguno para capacidad |
| **E2** | **Interés con volumen** | Minuta con el **decisor de compras** o con quien tiene el dato: producto, kg/semana, precio actual y plazo actual; mejor con reporte o factura | Volumen "de memoria" de alguien sin acceso al dato | C firme | Reservas de espacio y terreno; nunca capacidad inicial |
| **E3** | **Negociación** | Especificación de producto pedida o entregada, precio de referencia discutido, requisitos de alta de proveedor recibidos, cotización pedida por el cliente | Una segunda reunión "de cortesía" sin especificación | **B** | Entra parcialmente (factor α, a calibrar; DEC-014) |
| **E4** | **Prueba piloto** | Piloto **acordado** (locales, productos, volumen, duración, criterios de éxito) o **ejecutado** con compras facturadas y recompra | Muestras regaladas sin compra | B (acordado) · B con historial (ejecutado) | Calibra α y el mix real |
| **E5** | **Carta de intención** | Documento firmado con producto, volumen, precio o fórmula de referencia y plazo | LOI sin volumen ni precio (vale como E3) | **A** (con volumen y precio) | Base firme de capacidad inicial, con la cautela de que suele no ser vinculante |
| **E6** | **Contrato / orden** | Contrato de suministro u orden de compra | — | **A** | Base firme |

**Reglas de uso**

1. **Solo sube con documento.** Cada paso de nivel requiere un documento nuevo en el data room y su registro como fuente (`tipo_fuente = entrevista` o `cotizacion`).
2. **Puede bajar.** Una carta de intención vencida, un piloto sin recompra o un cambio de decisor devuelven el nivel al anterior.
3. **La cercanía no suma nivel.** Que el cliente esté vinculado al inversor **no** es evidencia de compra; aumenta el riesgo de concentración (DEC-017, DEC-019).
4. **No se suman niveles distintos.** Los kg se informan separados por categoría (A, B, C, D), como exige el modelo de demanda.
5. **Para exportación** se usa la escala de niveles 0–6 del modelo de demanda; la tabla anterior aplica al mercado interno.

---

## 3. Guías por actor

Cada guía indica qué preguntar primero (las 5–8 imprescindibles), qué evidencia se considera **fuerte** y cuál **débil**. Para la red se usa el cuestionario existente; para el resto, la ficha de [`canales_comerciales.md` §4](canales_comerciales.md) con estas prioridades.

### 3.1 Red de supermercados (O1)

**Instrumento:** [`cuestionario_supermercados.md`](cuestionario_supermercados.md) (bloque 0 ya cubierto por la reunión con inversores; bloques 1–3 con compras y logística).

| Imprescindible | Evidencia fuerte | Evidencia débil |
|---|---|---|
| Lista de locales que venden pollo (1.1–1.2) | Lista con direcciones y razón social | "Son unos 90" |
| kg/semana por producto y local (1.4–1.6) | Reporte del sistema de 12 meses | Estimación del gerente de un local |
| Proveedores actuales y contratos (1.7, 1.10) | Nombres, participación y vencimientos | "Varios" |
| Precio y plazo de pago (1.8–1.9) | Lista de precios o factura con fecha | "Pagamos a 30 más o menos" |
| CD y esquema de entrega (1.3, 2.2) | Minuta de logística + visita al CD | Suposición del comprador |
| Requisitos de alta (2.5) | Manual o requisitos escritos | "Lo normal" |
| Prueba piloto y carta de intención (1.11–1.12) | Piloto acordado por escrito | "Cuando tengan la planta" |

**Señal de alarma:** si después de la reunión con inversores no se consigue reunión con compras en 4 semanas, la red queda en E0–E1 y el hito H-A debe evaluarse sin ella.

### 3.2 Mayoristas (O2) — 5 entrevistas

**Perfil:** mayoristas de carnes y avícolas del AMBA (mercados concentradores, distribuidoras de frigoríficos, mayoristas de barrio). Incluir al menos uno que venda a pollerías y uno que venda a gastronomía.

**Qué preguntar primero**
1. ¿Qué productos de pollo venden y cuántos kg por semana de cada uno?
2. ¿A quién le compran (frigoríficos, marcas) y por qué a ellos?
3. ¿A qué precio compran y venden cada producto hoy (sin IVA, condición, plazo)?
4. ¿Qué parte del pollo **cuesta más colocar** y cuál falta? (alas, pata-muslo, menudencias, cuello, carcasa, garras)
5. ¿Compran fresco o congelado? ¿En qué presentación (cajón, granel, bandeja)?
6. ¿A cuántos días pagan y cómo?
7. ¿Qué haría que cambien o sumen un proveedor?
8. ¿Aceptarían comprar partes o excedentes de un proveedor nuevo? ¿Con qué volumen mínimo?

| Evidencia fuerte | Evidencia débil |
|---|---|
| Lista de precios con fecha; factura de compra (anonimizada); volumen semanal que coincide con lo que se observa en el depósito | Precio "de mercado" sin fecha ni condición; volumen redondo sin respaldo |

### 3.3 Distribuidores (O2) — 3 entrevistas

**Perfil:** distribuidores refrigerados que abastecen almacenes, autoservicios, rotiserías o gastronomía.

**Qué preguntar primero**
1. ¿Cuántos clientes y kg por semana de pollo distribuyen? ¿Qué productos?
2. ¿Qué margen o comisión cobran sobre el precio del proveedor?
3. ¿Qué costo tiene para ellos cada entrega (por kg, por parada)? (DPV-042)
4. ¿Qué frecuencia y pedido mínimo manejan?
5. ¿Qué exigen a un proveedor (habilitación, rótulo, vida útil, cajas)?
6. ¿Cobran a sus clientes a qué plazo y a qué plazo pagan?

| Evidencia fuerte | Evidencia débil |
|---|---|
| Tarifa o margen por escrito; lista de clientes por tipo (sin nombres) | "Llegamos a todos lados" |

### 3.4 Pollerías y carnicerías (O0–O2) — 8–10 entrevistas

**Perfil:** empezar por la **carnicería familiar** (registro de 4–8 semanas, DPV-004) y sumar pollerías y carnicerías de distintos barrios y tamaños.

**Qué preguntar primero**
1. ¿Cuántos kg de pollo venden por semana? ¿Entero, trozado, milanesas, menudencias?
2. ¿A quién le compran y cada cuánto les entregan?
3. ¿A qué precio compran (entero, pechuga, pata-muslo, alas, menudencias)?
4. ¿Pagan contado o a plazo?
5. ¿Trozan ellos o compran trozado? ¿Hacen milanesas?
6. ¿Qué problemas tienen con el proveedor actual?

| Evidencia fuerte | Evidencia débil |
|---|---|
| Factura o remito de compra; registro propio de ventas | "Vendemos mucho" |

### 3.5 Gastronomía (O2) — 3–5 entrevistas

**Perfil:** cadenas de comidas, catering de empresas o instituciones, hoteles; no restaurantes individuales pequeños como primer paso.

**Qué preguntar primero**
1. ¿Qué productos de pollo compran (pechuga porcionada, suprema, muslo deshuesado, alitas, IQF) y cuántos kg por semana?
2. ¿Qué especificación exigen (calibre, peso por porción, piel, congelado)?
3. ¿Cómo homologan a un proveedor? ¿Hay licitaciones o listas de proveedores?
4. ¿A qué precio y plazo compran?
5. ¿Compran producto importado? ¿Por qué?

| Evidencia fuerte | Evidencia débil |
|---|---|
| Ficha de especificación o pliego; precio de compra con fecha | "Siempre buscamos proveedores" |

### 3.6 Elaboradores e industria (O2) — 3–5 entrevistas

**Perfil:** fábricas de milanesas, hamburguesas, rebozados, chacinados cocidos; industrias que usan CMS, recortes, piel o muslo deshuesado. Preguntas de subproductos comestibles: ver también [`../07_subproductos/cuestionario_subproductos.md`](../07_subproductos/cuestionario_subproductos.md).

**Qué preguntar primero**
1. ¿Qué materias primas de pollo usan (CMS, recortes, pechuga, muslo, piel) y cuántas t por mes?
2. ¿De dónde viene hoy (nacional, importado de Brasil)? ¿Por qué?
3. ¿Qué especificación exigen (grasa, calcio, microbiología, temperatura, presentación)?
4. ¿A qué precio compran y a qué plazo?
5. ¿Comprarían carcasa-esqueleto para procesar ellos?
6. ¿Elaboran a façon para terceros? ¿Con qué tarifa? (DPV-079)

| Evidencia fuerte | Evidencia débil |
|---|---|
| Especificación técnica escrita; precio de la materia prima importada con fecha | "Si hay local, preferimos local" |

### 3.7 Exportadores y traders (O5 / O9) — 2–3 entrevistas

**Perfil:** frigoríficos exportadores que compran partes de terceros para completar contenedores; traders de garras, menudencias y alas. Detalle en [`../07_subproductos/cuestionario_subproductos.md`](../07_subproductos/cuestionario_subproductos.md).

**Qué preguntar primero**
1. ¿Compran partes a plantas sin habilitación de exportación propia? ¿Con qué requisitos?
2. ¿Qué especificación (grado, calibre, pelado, congelado, caja)?
3. ¿Precio en planta por grado y cómo se ajusta?
4. ¿Lote mínimo y frecuencia?
5. ¿Destinos actuales y alternativas a China?

| Evidencia fuerte | Evidencia débil |
|---|---|
| Precio en planta con fecha y especificación escrita | Precio FOB de un sitio comercial o de prensa |

---

## 4. Qué evidencia necesitamos para cada decisión

| Decisión | Qué evidencia comercial la habilita (cualitativo; los umbrales los fija el promotor) |
|---|---|
| Seguir con la red como cliente ancla (hito H-A) | Red en E2 o más con reporte de compras y acceso a compras y logística |
| Definir un rango de escala (DEC-001, DEC-014) | Volumen A + B documentado por producto; canales identificados para las partes que la red no compra |
| Etapa 0 de validación comercial (DEC-018) | Al menos un cliente en E3–E4 dispuesto a una prueba y una fuente de producto (façon o compra) |
| Portafolio inicial (DEC-005) | Mix real de la red (DPV-037) y compradores de partes en E2 o más |
| Umbrales de concentración (DEC-017) | Pipeline con varios clientes independientes en B/A |

## 5. Pipeline

Una fila por cliente potencial, en la planilla del pipeline ([`estrategia_comercial.md` §4](estrategia_comercial.md)), agregando dos columnas: **nivel de evidencia (E0–E6)** y **código del documento** en el data room. La categoría A/B/C/D se deriva del nivel (tabla §2) y nunca se asigna a mano.

| Columna | Contenido |
|---|---|
| cliente (código) | Código del actor (p. ej., `mayorista-m01`) |
| canal | Supermercado, mayorista, distribuidor, pollería/carnicería, gastronomía, industria, exportación |
| productos | Partes o productos de interés |
| kg/semana declarados | Por producto, con base y período |
| precio y plazo actuales | Con fecha y condición |
| nivel de evidencia | E0–E6 |
| categoría | A/B/C/D (derivada) |
| documento | Código del data room |
| fecha de la última evidencia | AAAA-MM-DD |
| próximo paso | Qué falta para subir de nivel |

## 6. Relevamiento de góndola (se puede empezar ya)

Sirve para DPV-013, 017, 020, 037, 068 y 070 **sin depender de ningún contacto**. Es evidencia **débil** para precios de venta del proyecto (es precio al público) pero **fuerte** para marcas presentes, formatos y definición de cortes.

**Dónde:** 10–20 locales de la red (si se conoce la lista) y 5–10 de otras cadenas y pollerías como comparación, en días y horarios parecidos.

| Campo | Qué anotar |
|---|---|
| Fecha, hora, local (código), cadena, formato | — |
| Producto | Entero (con/sin menudencias), pechuga, suprema, pata-muslo, alas, menudencias, milanesas, otros elaborados |
| Definición del corte | Qué incluye (con/sin espinazo, con/sin piel, con/sin solomillo) — foto de la etiqueta |
| Marca y proveedor | Marca visible, número de establecimiento SENASA en el rótulo |
| Fresco / congelado | — |
| Presentación | Granel, bandeja, atmósfera modificada, bolsa; peso fijo o variable |
| Precio al público | $/kg con fecha (y tipo de cambio de referencia si se convierte, regla 2) |
| Promoción | Sí/no, tipo |
| Espacio en góndola | Metros lineales aproximados o cantidad de frentes |
| Observaciones | Faltantes, calidad visible, carnicería asistida o solo autoservicio |

Guardar como `AAAA-MM-DD_gondola-gNN_precios_registro` y las fotos como `..._foto_NN` (convención en [`../00_gestion_proyecto/estructura_data_room_campo.md`](../00_gestion_proyecto/estructura_data_room_campo.md)).

## 7. Errores a evitar

| Error | Por qué es grave |
|---|---|
| Sumar el "interés" de muchos clientes y llamarlo demanda | Es E1: no dimensiona nada |
| Preguntar "¿nos compraría?" en lugar de "¿cuánto compra hoy, a quién y a qué precio?" | La respuesta hipotética casi siempre es "sí" |
| Validar solo pechuga | El ave completa tiene que venderse: la parte limitante define las aves y el resto queda como excedente |
| Olvidar el plazo de pago | Con producto perecedero, el plazo define el capital de trabajo tanto como el precio |
| Confiar en el precio de góndola como precio de venta del proyecto | Incluye margen, impuestos y promociones del comercio |
| Tratar a la red vinculada al inversor como demanda segura | La concentración conjunta capital–ventas es el principal riesgo comercial del modelo |
