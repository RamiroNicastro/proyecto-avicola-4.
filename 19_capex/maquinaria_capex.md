# Maquinaria de proceso, subproductos y frío — CAPEX

**Fecha:** 2026-10-02 (v1.1) · Equipos: [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv) · Lotes RFQ: [`../08_maquinaria/requerimientos_cotizacion.md`](../08_maquinaria/requerimientos_cotizacion.md) §3 · Capas de costo: [`../08_maquinaria/plan_rfq.md`](../08_maquinaria/plan_rfq.md) §5

> **Ningún equipo tiene precio.** No se seleccionó tecnología ni proveedor (DEC-049). El motor solo organiza qué hay que cotizar, en qué paquete y cómo se convertirá un precio de proveedor en costo instalado sin doble conteo.

## 1. Paquetes costeables y equipos hijos

El costo se carga **por lote RFQ** (paquete). Los EQ-01…EQ-76 entran al BOQ como **hijos informativos** (`INCLUIDO_EN_PAQUETE = Sí`): documentan nivel de automatización, etiqueta de expansión y capacidad (nominal requerida, aves/h), pero no se costean (SUP-160).

| Paquete (COSTO_ID) | Contenido | Capacidad de referencia | Método |
|---|---|---|---|
| PQ-L1 Recepción de vivo | EQ-01, 02, 04, 05, 06 (EQ-03 cajones → logística) | nominal requerido aves/h (05) | escalado (exponente PENDIENTE) |
| PQ-L2 Faena | EQ-07 a 20 (EQ-14 caldera → térmico TE-GEN) | ídem | escalado |
| PQ-L3 Evisceración | EQ-21 a 33 (incluye EQ-28 y EQ-33) | ídem | escalado |
| PQ-L4 Enfriamiento | EQ-34 a 38 (EQ-37 agua helada → frío FR-AGH) | ídem | escalado |
| PQ-L5 Clasificación, trozado, deshuese | EQ-39 a 46 (deshuese solo con config. C) | ídem | escalado |
| PQ-L6 Coproductos | EQ-47 garras (si aplica), EQ-48 CMS (opcional/tercerizar) — **sin** EQ-28/33 | ídem | escalado |
| PQ-L7 Packaging | EQ-49 a 56 (EQ-54 etiquetado → IT-ETQ) | ídem | escalado |
| PQ-L11 Línea llave en mano | L1–L5 integrados con capacidad garantizada | ídem | escalado |
| EQ-LIM Higiene | EQ-74 espuma, EQ-75 esterilizadores/lavamanos | lote | global |
| SB-L9 Subproductos | EQ-66 sangre, 67 plumas, 68 vísceras, 69 contenedores/báscula | t/d de masa segregable (09C) | escalado |
| SB-BAS Tratamiento básico propio | tecnología PENDIENTE | t/d | escalado |
| SB-REN Rendering | FUTURO | t/d | escalado |
| FR-PAQ Frío | ver [`utilities_capex.md`](utilities_capex.md) §2 | kWf (cota inferior) | escalado |

**Capacidad de línea (auditoría v1.1).** La v1.0 cargaba en los lotes el ritmo **operativo** (aves/día ÷ horas netas), que no es una capacidad comercial. La v1.1 usa el ritmo **nominal requerido** de 05 (aves/día ÷ (h × R), R = 0,95 / 0,89 / 0,82; sensibilidad `media` por defecto, input explícito) y deja en `CAPACIDAD_DETALLE`: capacidad de **planta** (aves/día), ritmo operativo, nominal (tres sensibilidades), **diseño PENDIENTE** (margen no adoptado), **garantizada PENDIENTE** (DPV-097) y número de líneas (1, de 12C). A 10.000 aves/día y 8 h: operativo 1.250, nominal 1.316 / 1.404 / 1.524 aves/h.

**Origen de la lista de equipos.** Todos los EQ del BOQ son filas de `08_maquinaria/matriz_equipos.csv` (09A); CAPEX no agrega equipos propios ni los duplica (test N17). Cada EQ tiene un solo costeador (test M05).

Equipos por escala en el BOQ de C1 (nivel de la matriz 08, `semi`): 59 (2.500), 62 (5.000), 63 (10.000), 65 (20.000). Niveles a 10.000: 47 A, 12 S, 3 M, 1 O; a 2.500: 23 M, 20 S, 12 A, 3 Mc, 1 O. Estos niveles son **hipótesis de trabajo** (SUP-065), no decisiones (DEC-037).

## 2. Duplicaciones detectadas en los lotes RFQ (no resueltas)

| Tensión | Riesgo | Tratamiento |
|---|---|---|
| T16-01: EQ-28 (mollejas) y EQ-33 (enfriador de menudencias) figuran en **L3 y L6** | Una oferta de L3 y otra de L6 podrían cotizar el mismo equipo | Asignados a L3; L6 = garras y CMS. Aclarar en el RFQ |
| T16-02: EQ-14 (caldera) está en L2 y EQ-37 (agua helada) en L4 | Duplicar con el paquete térmico y el de frío | Costeados en TE-GEN y FR-AGH; pedir a L2/L4 que los excluyan o los desglosen |
| Llave en mano (L11) vs lotes | Sumar L11 + L1–L5 | Con `modalidad_linea = llave_en_mano`, L1–L5 pasan a hijos de L11 (test A09) |

## 3. Equipo importado: de precio a costo instalado

El motor separa siempre **COSTO_EQUIPO** (precio al Incoterm), **COSTO_LANDED** y **COSTO_INSTALADO**. Sin capas, un precio EXW/FOB/CIF queda **PRECIO_PARCIAL** y **no suma** al CAPEX (test I01).

| Capa ([`plan_rfq.md`](../08_maquinaria/plan_rfq.md) §5.1) | Concepto | En el motor |
|---|---|---|
| C01 | Equipo | Precio de la base al Incoterm |
| C02–C03 | Embalaje, flete interno en origen | Landed (si el Incoterm no las incluye) |
| C04–C05 | Flete internacional, seguro | Landed |
| C06 | Gastos portuarios, despachante | Landed |
| C07 | Aranceles, tasas e impuestos **no recuperables** | Landed; si es `NC` el instalado queda PENDIENTE (**no se asume arancel cero**, test I03) |
| C08 | Impuestos **recuperables** | Aparte (efecto financiero; no es costo económico) |
| C09 | Flete puerto → sitio | Landed |
| C10 | Obra civil a cargo del comprador | **Excluida**: la obra se costea en OC-* |
| C11–C16, C18–C19 | Instalación, supervisión, puesta en marcha, capacitación, repuestos, garantía, ingeniería de integración, ajustes | Instalado |
| C17 | Servicio anual | OPEX |

Capas que incluye cada Incoterm (orientación, a confirmar con el despachante): EXW → C01; FCA/FOB → C01–C03; CFR → +C04; CIF → +C05; DAP → +C09; DDP → +C06, C07, C09. Las capas se cargan en [`capas_importacion_capex.csv`](capas_importacion_capex.csv) (hoy vacío) con estados `INC` / `INC-SV` / `EST` / `NC` / `NA`.

**Factor paramétrico** (FOB × k = instalado): solo en **modo sensibilidad** (`--sensibilidad`) y con `FACTOR_INSTALADO_SENSIBILIDAD` explícito por concepto; la fila queda marcada `INSTALADO_POR_FACTOR_SENSIBILIDAD` (test I04). No hay factor por defecto.

**Datos a validar:** fletes (DPV-162), régimen de importación, posición arancelaria, tasas y despachante (DPV-093; usados: DPV-093), alcance de instalación y puesta en marcha (DPV-163), impuestos (DPV-169).

## 4. Escala sin linealidad

Los paquetes se costean con `precio_ref × (capacidad ÷ capacidad_ref)^exponente`. El exponente **no se supone**: debe salir de dos cotizaciones del mismo proveedor a dos escalas (DPV-160). Sin exponente, un precio solo vale dentro del rango de capacidad de su referencia (SUP-167). La referencia de fabricante de planta de alimento (ALI-REF, 8–10 t/h) muestra el caso: aun cuando la escala de 10.000 aves/día cae en ese rango (8,4 t/h), el precio es de equipo con Incoterm desconocido y **no** se usa.

## 5. Referencias de contraste no usadas

- REF-RAFS (FTE-313): USD 17.401–52.501 de equipos para unidades de faena **móviles** de 350–1.200 aves/h (EE. UU., 2015). El ritmo es comparable con 2.500–10.000 aves/día, pero el alcance (unidad exenta, sin frío ni trozado, sin habilitación SENASA) no lo es. Sirve solo para recordar que una sala mínima y una planta habilitada son objetos distintos.
- REF-MAL (FTE-312): presupuesto oficial de acondicionamiento de una sala de faena aviar municipal (ARS 2022): sin m², sin alcance ni TC.
