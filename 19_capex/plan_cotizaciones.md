# Plan de cotizaciones para el CAPEX

**Fecha:** 2026-10-02 · Matriz: [`matriz_rfq_capex.csv`](matriz_rfq_capex.csv) (13 ítems) · Secuencia y plantilla de comparación: [`../08_maquinaria/plan_rfq.md`](../08_maquinaria/plan_rfq.md) (no se duplica aquí)

> **No se solicitó ninguna cotización.** La fase no lo habilita (DEC-049; hito H-B del plan de campo). Este plan dice qué pedir, con qué especificación mínima y cómo se carga la respuesta en el motor. No se inventan proveedores: donde no hay candidatos relevados dice "No identificados".

## 1. Qué cotizar (resumen de la matriz)

| RFQ | Categoría | Capacidad a pedir | Conceptos del motor | Cotizaciones |
|---|---|---|---|---|
| RFQ-16-01 | Línea de faena, evisceración y enfriamiento (L1–L4, L11) | operativo 312–2.500 aves/h; **nominal requerido** 329–3.049 aves/h (05, R 0,95–0,82); diseño y garantizada PENDIENTES — **dos escalas** del rango | PQ-L1…L4, PQ-L11 | ≥ 3 |
| RFQ-16-02 | Trozado, deshuese, packaging (L5, L7) | ídem, por configuración de producto | PQ-L5, PQ-L7 | ≥ 3 |
| RFQ-16-03 | Coproductos (L6) y subproductos (L9) | 1,5–12,2 t/d de masa biológica segregable (09C; no son sólidos de efluente) | PQ-L6, SB-L9, SB-BAS | ≥ 3 |
| RFQ-16-04 | Paquete de frío | **sin capacidad única**: BASE física parcial de 09C (p. ej. 99 + 69 + 10 kWf a 10.000), BENCHMARK 634–5.075 kWh/d, CONTRADICCIÓN ABIERTA ×5,7, diseño y margen PENDIENTES; pedir balance frigorífico (DPV-109) | FR-PAQ y componentes | ≥ 3 |
| RFQ-16-05 | Efluentes | 55–440 m³/d | EF-PAQ, EF-*, OC-EF | ≥ 3 |
| RFQ-16-06 | Acometida, transformación, tableros, respaldo | demanda máxima PENDIENTE (lista de cargas) | EL-* | ≥ 3 |
| RFQ-16-07 | Caldera, aire comprimido, agua | pico PENDIENTE | TE-*, AC-COM, AG-* | ≥ 3 |
| RFQ-16-08 | Obra civil: USD/m² por categoría | 1.796–7.795 m² construidos | OC-* | ≥ 3 |
| RFQ-16-09 | Terreno por corredor | mínimo físico 15.398–32.379 m² (medio, función 12C); conceptual 12C 19.868–43.660 m²; SUPERFICIE_ESCENARIO_OBJETIVO_20000_12C 14.069 / 33.345 / 82.253 m²; superficie a cotizar = criterio de terreno elegido (decisión) | TER-* | por corredor |
| RFQ-16-10 | Incubación | posiciones de setter y hatcher de 14B | INC-* | ≥ 3 |
| RFQ-16-11 | Planta de alimento | 2,1–16,7 t/h (14B) | ALI-* | ≥ 3 |
| RFQ-16-12 | Vehículos por flujo | unidades de `logistica_capex.md` | VEH/CAR/FRI/AUX/JAU | ≥ 3 |
| RFQ-16-13 | Galpones y equipamiento | 9.500–75.900 m² de galpón | GRA-* | ≥ 3 |

Los valores exactos de capacidad por escala salen del CSV (columna `CAPACIDAD`).

## 2. Requisitos de cada cotización (para que entre al motor como E1)

1. **Desglose por capas** C01–C19 ([`../08_maquinaria/plan_rfq.md`](../08_maquinaria/plan_rfq.md) §5.1); un precio global único no es comparable.
2. **Incoterm**, **moneda**, **fecha**, **validez**, fórmula de ajuste, condiciones de pago.
3. **IVA** y otros impuestos: incluidos o no, alícuota.
4. **Flete, instalación, puesta en marcha, capacitación, repuestos**: incluidos o no (columnas `FLETE_INCLUIDO`, `INSTALACION_INCLUIDA`, `PUESTA_EN_MARCHA_INCLUIDA`).
5. **Capacidad garantizada** y su definición (DPV-097); precio a **dos escalas** para estimar el exponente (DPV-16-01).
6. Alcance explícito para evitar duplicaciones: EQ-28/EQ-33 (L3 vs L6), EQ-14 (L2 vs térmico), EQ-37 (L4 vs frío) (T16-01, T16-02).
7. Plazo de entrega y vida útil esperada (DPV-16-15).

## 3. Cómo se carga una cotización

1. En [`base_costos_capex.csv`](base_costos_capex.csv), fila del `ID_COSTO`: `PRECIO_UNITARIO` (y `PRECIO_BAJO`/`PRECIO_ALTO` solo si la oferta da un rango, con `ORIGEN_RANGO`), `MONEDA_ORIGINAL` (+ `TC_MONEDA_POR_USD`, `TIPO_TC`, `FECHA_TC` si no es USD), `FECHA_PRECIO`, `TIPO_PRECIO = cotizacion`, `INCOTERM`, flags de inclusión, `NIVEL_EVIDENCIA = E1`, `LECTURA_PRIMARIA = Sí`, `FUENTE` (ID del registro de fuentes con `tipo_fuente = cotizacion`), `ESTADO = CON_PRECIO`.
2. Si es importado y no instalado: capas en [`capas_importacion_capex.csv`](capas_importacion_capex.csv) (`ID_COSTO, CAPA, ESTADO, MONTO_USD, NIVEL_EVIDENCIA, FUENTE`).
3. Si la oferta es desglosada (frío, efluentes): cambiar `INCLUIDO_EN_PAQUETE` a "No" en los componentes (DEC-16-03).
4. Correr `python3 19_capex/modelo_capex.py`: si la fila viola una regla de evidencia, el script se detiene y dice cuál.

## 4. Antes de cotizar (sin pedir precios)

Relevar presencia local, servicio técnico y plantas de referencia (DPV-089), y en la feria Avícola y Porcinos 2026 (FTE-195) preguntar alcance típico de ofertas, plazos y si cotizan a dos escalas. Leer en original las fuentes oficiales bloqueadas en esta sesión (FTE-16-002 SAGyP, FTE-16-007 INTA, FTE-16-003 pliego municipal).
