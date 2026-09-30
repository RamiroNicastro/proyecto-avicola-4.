# Plan de RFQ — secuencia de cotizaciones y plantilla uniforme de comparación

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Ola O7 de [`../00_gestion_proyecto/plan_trabajo_campo.md`](../00_gestion_proyecto/plan_trabajo_campo.md) · Contenido técnico del pedido: [`requerimientos_cotizacion.md`](requerimientos_cotizacion.md) (base de diseño, 31 campos, 11 lotes; no se repite aquí)

> **Estado: NO se solicita ninguna cotización todavía.** La elección de proveedor (DEC-049) sigue bloqueada por la fase y la escala no está definida. Este plan define **qué pedir primero, cuándo y cómo comparar** las ofertas cuando la fase lo habilite.
> **Regla que este plan protege:** nunca comparar una línea **FOB China** contra una línea **instalada y puesta en marcha en Argentina** como si fueran el mismo precio. Toda oferta se lleva a la misma base (§5) antes de compararla.

---

## 1. Cuándo se puede enviar un RFQ

| Condición | Por qué | Fuente |
|---|---|---|
| Hito **H-B** superado: rango de escala acotado con demanda documentada y abastecimiento posible | Sin rango de escala, las ofertas no son comparables ni útiles | [`plan_trabajo_campo.md` §5.3](../00_gestion_proyecto/plan_trabajo_campo.md) |
| Mix y perfil fresco/congelado aproximados (DPV-037, DPV-085) | Definen trozado, deshuese, packaging y congelado | Matriz de validación |
| Horas netas y organización horaria de referencia (DPV-082, DEC-036) | Definen el ritmo nominal a pedir | [`../05_proceso_industrial/cuellos_botella.md`](../05_proceso_industrial/cuellos_botella.md) |
| Promotor habilita la fase de cotizaciones | CLAUDE.md: no seleccionar maquinaria ni proveedores antes | `estado_proyecto.md` |

**Antes de eso sí se puede** (sin pedir precios): relevar catálogos, presencia en Argentina, servicio técnico, stock de repuestos y plantas de referencia (DPV-089), por ejemplo en **Avícola y Porcinos 2026** (Buenos Aires, 6–8 nov 2026; FTE-195), y preguntar en las visitas a plantas qué equipos usan y cómo funciona su servicio técnico ([`../05_proceso_industrial/guia_visita_planta.md`](../05_proceso_industrial/guia_visita_planta.md) §2.4).

## 2. Qué cotizaciones pedir primero

Criterio: primero lo que (a) pesa más en la inversión, (b) tiene más incertidumbre y (c) condiciona el diseño del resto (layout, servicios, dotación).

| Orden | RFQ | Lotes de [`requerimientos_cotizacion.md` §3](requerimientos_cotizacion.md) | Por qué primero | DPV que responde | Precondición adicional |
|---|---|---|---|---|---|
| **1** | **Línea de faena, evisceración y enfriamiento** (por módulos y como línea completa con responsable único) | L1–L4 y L11 | Fija ritmo real, **definición contractual de capacidad**, dotación, superficie y servicios del núcleo de la planta | 097, 088 (referencias), 095, 086 (lead time), 089 | Pedir **dos escalas** del rango y cómo se pasa de una a otra; inmersión y aire por separado; aturdido eléctrico y, si lo ofrecen, CAS |
| **2** | **Frío**: cámaras, túneles de congelado, sala de máquinas y balance frigorífico | L8 (y agua helada de L4) | Incertidumbre ×5 por perfil fresco/congelado; brecha ×5,7 sin cerrar entre cálculo físico y benchmark | 109, 096, 095 | Perfil P1–P3 y temperatura de verano de diseño (depende de la zona) |
| **3** | **Pretratamiento y tratamiento de efluentes** | L9 + proveedores de tratamiento | Puede limitar el sitio y la escala; condiciona terreno | 114, 111, 095 | Límites de vuelco del sitio o de las zonas candidatas (DPV-106); si no hay sitio, cotizar por escenario de carga con rangos |
| **4** | **Trozado, deshuese y packaging** | L5, L7 | Dependen del mix real | 095 | Mix de la red y de otros canales (DPV-037, DPV-040) |
| **5** | **Servicios**: generación de respaldo, calderas, compresores, agua | L10 | Se dimensionan con la lista de cargas de los RFQ 1–4 | 095 | Lista de cargas consolidada (DEC-048) |
| **6** | **Coproductos**: garras, CMS, menudencias | L6 | Solo si la ruta tiene comprador | — | Comprador identificado (DEC-029, DEC-031) |
| Alt. | **Usados o reacondicionados** (en paralelo al RFQ 1) | L11 | Alternativa de menor inversión inicial a evaluar, no a presumir | 093 | Régimen de importación de usados (DPV-093) |

**Cuántos proveedores por RFQ:** tres como mínimo, de perfiles distintos para no comparar solo un tipo de oferta: un proveedor integral internacional, uno regional o nacional, y una alternativa (fabricante asiático, pequeña escala o usado). **Sin preferencia ni selección** (DEC-049); el listado de candidatos está en [`proveedores_preliminares.md`](proveedores_preliminares.md).

## 3. Cómo se envía (cuando corresponda)

1. La misma **base de diseño** a todos ([`requerimientos_cotizacion.md` §1](requerimientos_cotizacion.md)).
2. Los **31 campos** por equipo y la **definición contractual de capacidad** (§2 y §2.1 del mismo archivo).
3. Pedir explícitamente el **desglose de costos** por capas (§5.1): una oferta con un único precio global no es comparable.
4. Pedir **Incoterm**, **moneda**, **validez**, **fórmula de ajuste**, **condiciones de pago** y **garantías bancarias** exigidas.
5. Pedir **plantas de referencia visitables**, idealmente en Argentina o la región.
6. Registrar cada respuesta como `[COTIZACIÓN]` con proveedor, fecha, validez, moneda, IVA, flete, instalación y condiciones (regla 4); valores en ARS con tipo de cambio, fecha y fuente (regla 2).

## 4. El problema que hay que evitar

Dos ofertas del "mismo" equipo pueden cubrir alcances muy distintos:

| | Oferta X (ejemplo de formato) | Oferta Y (ejemplo de formato) |
|---|---|---|
| Incoterm | FOB puerto de origen | Instalada y en marcha en planta en Argentina |
| Incluye | Solo equipo embalado a bordo | Equipo, fletes, seguro, importación, montaje, puesta en marcha, capacitación, repuestos de 1 año, garantía |
| No incluye | Flete marítimo, seguro, aranceles e impuestos de importación, despachante, flete interno, montaje, supervisión, puesta en marcha, capacitación, repuestos, servicio local | Obra civil y servicios hasta el pie del equipo |

Comparar el número de X con el de Y es comparar **cosas distintas**: X parece más barata porque le faltan capas que alguien tendrá que pagar. La plantilla de §5 obliga a completar todas las capas antes de comparar.

## 5. Plantilla uniforme de comparación

### 5.1 Capas de costo (una columna por oferta)

**Base de comparación única:** **costo total instalado y en marcha en el sitio, en Argentina** (CTIM), en una sola moneda, con tipo de cambio y fecha declarados. El CTIM **no** es CAPEX del proyecto: es una herramienta de comparación entre ofertas; el CAPEX se arma después en `19_capex`.

| Capa | Concepto | Oferta 1 | Oferta 2 | Oferta 3 |
|---|---|---|---|---|
| C01 | **Equipo** (precio en fábrica, sin embalaje) | | | |
| C02 | Embalaje de exportación | | | |
| C03 | Flete interno en origen y despacho de exportación | | | |
| C04 | **Flete internacional** | | | |
| C05 | **Seguro** de transporte | | | |
| C06 | Gastos portuarios y de terminal en destino; despachante | | | |
| C07 | **Aranceles, tasas e impuestos de importación no recuperables**, cuando correspondan (confirmar con despachante; **no se asume alícuota**) | | | |
| C08 | Impuestos de importación **recuperables** (efecto financiero, se informa aparte) | | | |
| C09 | Flete puerto → sitio | | | |
| C10 | **Obra civil** y bases a cargo del comprador (indicada por el proveedor) | | | |
| C11 | **Instalación**: montaje mecánico, eléctrico, cañerías, tableros | | | |
| C12 | Supervisión de montaje del proveedor (viajes, viáticos) | | | |
| C13 | **Puesta en marcha** y **prueba de aceptación** (FAT/SAT, desempeño) | | | |
| C14 | **Capacitación** de operación y mantenimiento | | | |
| C15 | **Repuestos** iniciales (1–2 años) y críticos | | | |
| C16 | **Garantía** extendida, si se cotiza aparte | | | |
| C17 | **Servicio** técnico o contrato de mantenimiento (costo anual; se informa aparte del CTIM) | | | |
| C18 | Ingeniería de integración y documentación en español | | | |
| C19 | Ajustes de precio y riesgo cambiario previstos en la oferta | | | |
| **CTIM** | **Suma C01–C16 y C18–C19** (C08 y C17 se informan aparte) | | | |

**Cómo se completa cada celda** (obligatorio, nunca en blanco ni en cero por omisión):

| Código | Significado |
|---|---|
| `INC: monto` | Incluido y valorizado por el proveedor (`[COTIZACIÓN]`) |
| `INC-SV` | Incluido en el precio, sin valor separado |
| `EST: monto` | No incluido; estimado por el proyecto (`[ESTIMACIÓN]` con método y fuente) |
| `NC` | No cotizado y sin estimación: **la oferta no es comparable** hasta resolverlo |
| `NA` | No aplica (p. ej., C04–C08 para un proveedor nacional) |

### 5.2 Qué capas incluye cada Incoterm (orientación general)

Referencia para detectar lo que falta; **cada oferta debe confirmarse con su texto y con el despachante**.

| Incoterm | Normalmente incluye | Normalmente **no** incluye |
|---|---|---|
| EXW | C01 | C02–C19 |
| FCA / FOB | C01–C03 | C04–C19 |
| CFR | C01–C04 | C05–C19 |
| CIF | C01–C05 | C06–C19 |
| DAP (en sitio) | C01–C05, C09 | C06–C08 (importación), C10–C19 |
| DDP (en sitio) | C01–C09 | C10–C19 |
| "Llave en mano" / instalada y en marcha | Según contrato: verificar C10–C19 una por una | Lo que el contrato excluya (habitualmente C10) |

### 5.3 Comparación técnica (mismas ofertas)

| Aspecto | Oferta 1 | Oferta 2 | Oferta 3 |
|---|---|---|---|
| Velocidad **garantizada** y sus condiciones (peso, producto, dotación, disponibilidad) | | | |
| Velocidad nominal declarada | | | |
| Rango de peso sin ajuste | | | |
| Dotación supuesta | | | |
| Servicios: kW, agua, aire, vapor, frío, efluente | | | |
| Tiempo de lavado y de sanitización | | | |
| Lead time total (fabricación + transporte + montaje + puesta en marcha) | | | |
| Técnicos en Argentina y tiempo de respuesta garantizado | | | |
| Stock de repuestos críticos en Argentina | | | |
| Garantía (plazo, alcance, condiciones) | | | |
| Ampliación: hasta qué capacidad, qué se reemplaza, parada necesaria | | | |
| Plantas de referencia visitables | | | |
| Campos de los 31 respondidos | /31 | /31 | /31 |
| Validez de la oferta y fórmula de ajuste | | | |
| Condiciones de pago y garantías exigidas | | | |

### 5.4 Reglas de comparación

1. **No se compara** ninguna oferta con celdas `NC` en §5.1.
2. Los montos se llevan a **una sola moneda** con el **mismo tipo de cambio y fecha** para todas.
3. Las ofertas se comparan a **igual capacidad garantizada** y con la **misma definición de capacidad**; si difieren, se ajusta el alcance (más módulos, más personal) antes de comparar, y se documenta.
4. Una capacidad solo **nominal** o sin referencia de planta no se usa como capacidad del proyecto (SUP-061).
5. El costo anual de servicio (C17) y la dotación se comparan aparte: una línea más barata puede requerir más personal o más servicio.
6. La comparación económica completa (CAPEX, OPEX, costo por ave) se hace en `19_capex` y `20_opex`, no aquí.

## 6. Registro

- Ofertas → data room `07_proveedores/` con código `AAAA-MM-DD_prov-equipos-eNN_linea_cotizacion` ([`../00_gestion_proyecto/estructura_data_room_campo.md`](../00_gestion_proyecto/estructura_data_room_campo.md)).
- Planilla de comparación (§5) → data room, una por RFQ.
- Resultado → matriz de validación (DPV-089, 095, 096, 097, 109) y `25_fuentes/registro_fuentes.csv` con `tipo_fuente = cotizacion`.
