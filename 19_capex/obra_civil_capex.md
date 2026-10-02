# Obra civil y terreno — CAPEX paramétrico

**Fecha:** 2026-10-02 · Superficies: `09_layout_obra_civil/modelo_superficies.py` (12C) · Precios: [`base_costos_capex.csv`](base_costos_capex.csv)

> **Superficie conceptual ≠ proyecto ejecutivo.** Los m² son rangos de 12C (muchos en estado PROXY, sin footprint de proveedor). No hay un USD/m² único para la planta: cada categoría tiene su precio, hoy casi todos **PENDIENTES**.

## 1. Fórmula

```
COSTO_OBRA(categoría) = m²(categoría, bajo/medio/alto de 12C) × USD/m²(categoría, bajo/medio/alto)
TERRENO              = m² necesarios × USD/m² (por tipo) + gastos de compra (%) + preparación (m² × USD/m²)
                       + infraestructura de acceso (lote) + conexiones extraordinarias (lote)   [o cargo de parque]
```

## 2. Categorías de obra (mapeo de áreas de 12C, cada área en una sola categoría)

| ID | Categoría | Áreas de 12C | USD/m² | Evidencia |
|---|---|---|---|---|
| OC-PH | Proceso húmedo | colgado/aturdido, sangrado/escaldado/desplumado, evisceración, enfriamiento, clasificación, trozado, deshuese, CMS, coproductos, empaque, lavado de cajones, circulación de proceso, sala de subproductos | PENDIENTE | — |
| OC-RS | Recepción semicubierta | recepción y espera | PENDIENTE | — |
| OC-FR | Envolvente de frío (losa, estructura; paneles en FR-PAN) | cámaras refrigeradas/congeladas, túnel, antecámaras, cámaras de subproductos y decomisos | PENDIENTE | — |
| OC-DK | Docks y expedición | expedición/docks | PENDIENTE | — |
| OC-DP | Depósitos y talleres secos | residuos/cartón, envases, taller, repuestos, químicos | **250 / 300 / 350** | **E4 `[PVDP]`** FTE-16-001 |
| OC-ST | Salas técnicas | máquinas de frío, caldera, aire, generador, eléctrica, tratamiento de agua | PENDIENTE | — |
| OC-LB | Laboratorio | laboratorio de calidad (si es propio) | PENDIENTE | — |
| OC-VC | Personal | vestuarios, comedor, lavandería | PENDIENTE | — |
| OC-OF | Administración | oficinas, oficina SENASA, enfermería, porterías, circulación de personal | PENDIENTE | — |
| OC-EP | Pavimento pesado | playas de aves vivas, despacho, subproductos; circulación pesada | PENDIENTE | — |
| OC-EL | Estacionamiento | estacionamiento | PENDIENTE | — |
| OC-LV | Lavado de camiones | plataforma de lavado | PENDIENTE | — |
| OC-IP | Infraestructura pesada | bases de tanques de agua | PENDIENTE | — |
| OC-EF | Obra de efluentes | pretratamiento, ecualización, DAF, biológico, lodos, circulación | PENDIENTE | — |
| OC-CER | Cerco perimetral (m) | perímetro del terreno conceptual | PENDIENTE | — |
| OC-INF | Infraestructura del predio | m² de terreno (pluviales, cloaca interna, iluminación exterior) | PENDIENTE | — |
| OC-ADM | Oficina asset-light | m² PENDIENTES (DPV-16-12) | PENDIENTE | — |

La reserva de expansión de 12C es **terreno**, no obra (no se construye). Los paneles aislantes están en el paquete de frío (FR-PAN), no en OC-FR, para no contarlos dos veces (confirmar alcance en el RFQ: DPV-16-06).

## 3. Superficies por categoría — C1 (perfil P1, semi, 8 h netas), m² medio (bajo–alto)

| Categoría | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| OC-RS | 180 (140–240) | 180 (140–240) | 180 (140–240) | 180 (140–360) |
| OC-PH | 859 (573–1.302) | 1.477 (979–2.245) | 2.609 (1.725–3.979) | 4.647 (3.060–7.155) |
| OC-FR | 98 (68–157) | 137 (89–225) | 241 (144–421) | 466 (274–829) |
| OC-DK | 45 (35–60) | 45 (35–120) | 90 (35–240) | 135 (35–480) |
| OC-DP | 146 (103–209) | 214 (138–317) | 397 (255–590) | 741 (475–1.102) |
| OC-ST | 155 (115–215) | 182 (127–258) | 267 (177–399) | 432 (276–716) |
| OC-LB | 15 (12–20) | 17 (12–27) | 30 (18–48) | 52 (31–83) |
| OC-VC | 96 (70–175) | 154 (71–288) | 272 (116–516) | 508 (217–971) |
| OC-OF | 182 (110–330) | 192 (111–355) | 220 (120–417) | 290 (147–564) |
| OC-EP | 1.384 (864–2.322) | 1.683 (991–3.275) | 2.506 (1.263–5.198) | 3.855 (1.774–9.226) |
| OC-EL | 500 (182–1.085) | 719 (245–1.610) | 1.156 (370–2.660) | 2.031 (620–4.760) |
| OC-LV | 130 (100–160) | 130 (100–160) | 130 (100–160) | 130 (100–160) |
| OC-IP | 16 (4–46) | 32 (8–93) | 65 (16–185) | 130 (32–370) |
| OC-EF | 220 (128–519) | 254 (132–777) | 326 (138–1.515) | 592 (163–3.030) |
| OC-CER (m) | 507 (328–791) | 548 (354–862) | 624 (402–980) | 735 (474–1.160) |

El rango de OC-EF depende de la tecnología de efluentes, todavía abierta (DEC-043; el biológico con lagunas ocupa mucho más: DPV-144).

**Costo de OC-DP (único con precio, E4):** USD 43.779 (2.500) · 64.186 (5.000) · 119.200 (10.000) · 222.431 (20.000), con envolvente LOW–HIGH en [`capex_por_escala.md`](capex_por_escala.md). Es una **nave seca**; usar ese USD/m² para proceso húmedo o frío sería un error de categoría.

## 4. Terreno (sin elegir sitio)

| Modalidad | Superficie (m² medio; bajo–alto) | Precio |
|---|---|---|
| Solo la fase (`compra_fase`) | 15.398 (6.470–37.510) a 2.500 · 18.029 (7.528–44.536) a 5.000 · 23.372 (9.678–57.569) a 10.000 · 32.379 (13.492–80.673) a 20.000 | TER-01 PENDIENTE |
| Con reserva para 20.000 + rendering (`compra_reserva`) | 33.345 (14.069–82.253) en **todas** las escalas | TER-01 PENDIENTE |
| Parque industrial | Igual superficie; cargo de parque (TER-08) en lugar de acceso y conexiones | TER-02 PENDIENTE |
| Rural / industrial compatible | Igual superficie | TER-03 PENDIENTE |

El rango de terreno es amplio porque retiros (5/10/15 m), buffers (10/20/40 m, PROXY) y FOS son desconocidos (DPV-106, DPV-141). Gastos de compra: % PENDIENTE (TER-04). Preparación del sitio, acceso y conexiones: PENDIENTES (DPV-16-03, DPV-16-11). **No hay ninguna referencia válida de precio de suelo por corredor**: no se asigna precio.

## 5. Qué falta para costear la obra

1. USD/m² por categoría con fecha, TC, IVA y alcance (DPV-16-02): constructoras con antecedentes en plantas alimentarias o licitaciones públicas con cómputo y presupuesto leídos en original.
2. Programa de áreas de proveedor (footprints) para salir de PROXY (DPV-090, SUP-107).
3. Sitio: retiros, FOS, suelo, cota, accesos (DPV-106, DPV-141).
