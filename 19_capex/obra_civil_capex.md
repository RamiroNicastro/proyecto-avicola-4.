# Obra civil y terreno — CAPEX paramétrico

**Fecha:** 2026-10-02 (v1.1, auditoría de procedencia de drivers) · Superficies: `09_layout_obra_civil/modelo_superficies.py` (12C) · Precios: [`base_costos_capex.csv`](base_costos_capex.csv) · Procedencia: [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv)

> **Superficie conceptual ≠ proyecto ejecutivo.** CAPEX **consume** las superficies de 12C (no las recalcula ni crea otra definición): para la escala y arquitectura pedidas llama a la misma función de 12C y, cuando las entradas coinciden con un escenario publicado en `escenarios_superficies.csv`, la salida es **idéntica** a ese escenario (test N01). Cada categoría tiene su propio USD/m², hoy casi todos **PENDIENTES**.

## 1. Fórmula

```
COSTO_OBRA(categoría) = m²(categoría, bajo/medio/alto de 12C) × USD/m²(categoría, bajo/medio/alto)
TERRENO              = m² ADQUIRIDOS × USD/m² (por tipo) + gastos de compra (%) + preparación (m² REQUERIDOS × USD/m²)
                       + infraestructura de acceso (lote) + conexiones extraordinarias (lote)   [o cargo de parque]
```

## 2. 12C publicado vs CAPEX (auditoría)

Valores bajo / medio / alto en m². Fuente: 12C, bloque `sensibilidad` de `escenarios_superficies.csv`; CAPEX los reproduce exactamente (test N01).

| Escala | m² construidos 12C `referencia` (P1) = CAPEX C1 | m² construidos 12C `perfil_P2` = CAPEX C2/C3 | m² operativos (12C) | Exteriores (12C) | Retiros + buffers (12C, referencia) | Reserva (12C, referencia) |
|---|---|---|---|---|---|---|
| 2.500 | 1.226 / 1.777 / 2.707 | 1.237 / 1.796 / 2.735 | 2.505 / 4.027 / 6.840 | 1.151 / 2.030 / 3.613 | 4.487 / 13.428 / 38.932 | 926 / 2.413 / 7.440 |
| 5.000 | 1.702 / 2.597 / 4.077 | 1.738 / 2.664 / 4.193 | 3.177 / 5.416 / 9.992 | 1.344 / 2.565 / 5.138 | 4.902 / 14.907 / 44.314 | 1.094 / 3.108 / 10.592 |
| 10.000 | 2.730 / 4.306 / 6.850 | 2.823 / 4.454 / 7.136 | 4.617 / 8.489 / 16.568 | 1.749 / 3.857 / 8.203 | 5.672 / 17.635 / 53.341 | 1.454 / 4.644 / 17.168 |
| 20.000 | 4.655 / 7.451 / 12.260 | 4.847 / 7.795 / 12.852 | 7.344 / 14.190 / 29.807 | 2.527 / 6.147 / 14.517 | 6.902 / 21.735 / 67.363 | 2.263 / 7.735 / 30.768 |

| Escala | Terreno 12C `referencia` (publicado; incluye reserva proxy y rendering) | Terreno REQUERIDO por la fase (función 12C, sin reserva) | Terreno ADQUIRIDO con reserva para 20.000 = 12C `objetivo_20000` |
|---|---|---|---|
| 2.500 | 7.918 / 19.868 / 53.212 | 6.470 / 15.398 / 37.510 | 14.069 / 33.345 / 82.253 |
| 5.000 | 9.173 / 23.431 / 64.897 | 7.528 / 18.029 / 44.536 | 14.069 / 33.345 / 82.253 |
| 10.000 | 11.743 / 30.768 / 87.077 | 9.678 / 23.372 / 57.569 | 14.069 / 33.345 / 82.253 |
| 20.000 | 16.509 / 43.660 / 127.938 | 13.492 / 32.379 / 80.673 | 14.069 / 33.345 / 82.253 |

### De dónde salían las cifras aproximadas de la v1.0

| Cifra citada | Origen exacto | ¿Coincide con 12C? | Corrección |
|---|---|---|---|
| ≈ 1.800 m² a 2.500 | 1.796 = m² construidos medio de 12C `perfil_P2` (CAPEX C3 usa P2) | Sí, pero de un escenario distinto de la referencia de 12C (1.777, P1) y sin decirlo | Las tablas indican ahora el escenario (P1 `referencia` o `perfil_P2`) |
| ≈ 7.800 m² a 20.000 | 7.795 = 12C `perfil_P2` medio | Ídem (referencia P1: 7.451) | Ídem |
| ≈ 15.400 m² de terreno a 2.500 | 15.398 = función de terreno de 12C con escala objetivo = escala y sin rendering | **No**: 12C no publica un terreno sin reserva (su terreno publicado incluye una reserva proxy y rendering: 19.868) | Se rotula **"terreno requerido por la fase"** = CALCULO_MODELO_FUENTE (misma fórmula de 12C, entrada no publicada); se informa al lado el terreno publicado de 12C. Tensión T16-07 |
| ≈ 32.400 m² de terreno a 20.000 | 32.379, ídem | **No** (12C publica 43.660) | Ídem |
| ≈ 33.300 m² con reserva para 20.000 | 33.345 = 12C `objetivo_20000` | **Sí, directo** | Ninguna; es el único valor de terreno que CAPEX toma tal cual de un escenario publicado |

Ninguna de esas cifras provenía de una fórmula alternativa de CAPEX, pero dos se presentaban como "terreno de 12C" cuando eran una entrada que 12C no publica, y dos no decían que correspondían al perfil P2.

## 3. Terreno requerido vs terreno adquirido

- **Requerido por la fase** (`terreno_requerido_fase`): superficie de la fase actual sin reserva. Driver de **preparación del sitio** (TER-PREP): la reserva no se prepara.
- **Adquirido / reservado** (`terreno_adquirido`): lo que se compra. `compra_fase`, `parque_industrial`, `rural_compatible` = requerido (+ reserva de rendering si la arquitectura lo pide); `compra_reserva` = 12C con escala objetivo 20.000 + rendering. Driver de **TER-COMPRA** y del **cerco** (perímetro derivado del terreno adquirido, DERIVADO_CAPEX: 12C no publica perímetro).
- **Regla verificada:** adquirido ≥ requerido en cada nivel (bajo/medio/alto) y en todas las combinaciones de configuración, escala y modalidad (test N03). Si no se cumpliera, el motor emite `TERRENO_ADQUIRIDO_MENOR_QUE_REQUERIDO` y **no corrige**.
- Reservar para 20.000 **no** es un número único: 14.069 / 33.345 / 82.253 m² según el nivel de 12C, porque retiros (5/10/15 m), buffers (10/20/40 m, PROXY) y FOS son desconocidos (DPV-106, DPV-141).

## 4. Categorías de obra y tipo de área

Cada área de 12C pertenece a una sola categoría (test M06), y la suma por tipo reproduce la superficie fuente (test N02): Σ categorías **edificio** = m² construidos; Σ **pavimento / playa-circulación / infraestructura exterior** = m² exteriores; **efluentes** = m² de efluentes.

| ID | Categoría | Tipo de área | Áreas de 12C | USD/m² | Evidencia |
|---|---|---|---|---|---|
| OC-PH | Proceso húmedo | edificio | colgado/aturdido, sangrado/escaldado/desplumado, evisceración, enfriamiento, clasificación, trozado, deshuese, CMS, coproductos, empaque, lavado de cajones, circulación de proceso, sala de subproductos | PENDIENTE | — |
| OC-RS | Recepción semicubierta | edificio | recepción y espera | PENDIENTE | — |
| OC-FR | Envolvente de frío (paneles en FR-PAN) | edificio | cámaras refrigeradas/congeladas, túnel, antecámaras, cámaras de subproductos y decomisos | PENDIENTE | — |
| OC-DK | Docks y expedición | edificio | expedición/docks | PENDIENTE | — |
| OC-DP | Depósitos y talleres secos | edificio | residuos/cartón, envases, taller, repuestos, químicos | **250 / 300 / 350** | **E4 `[PVDP]`** FTE-16-001 |
| OC-ST | Salas técnicas | edificio | máquinas de frío, caldera, aire, generador, eléctrica, tratamiento de agua | PENDIENTE | — |
| OC-LB | Laboratorio | edificio | laboratorio de calidad | PENDIENTE | — |
| OC-VC | Personal | edificio | vestuarios, comedor, lavandería | PENDIENTE | — |
| OC-OF | Administración | edificio | oficinas, oficina SENASA, enfermería, porterías, circulación de personal | PENDIENTE | — |
| OC-EP | Pavimento pesado | playa / circulación | playas de aves vivas, despacho, subproductos; circulación pesada | PENDIENTE | — |
| OC-EL | Estacionamiento | pavimento | estacionamiento | PENDIENTE | — |
| OC-LV | Lavado de camiones | pavimento (plataforma) | plataforma de lavado | PENDIENTE | — |
| OC-IP | Infraestructura pesada | infraestructura exterior | bases de tanques de agua | PENDIENTE | — |
| OC-EF | Obra de efluentes | efluentes | pretratamiento, ecualización, DAF, biológico, lodos, circulación | PENDIENTE | — |
| OC-CER | Cerco perimetral (m) | perímetro | perímetro del terreno adquirido | PENDIENTE | — |
| OC-INF | Infraestructura del predio | **lote** (corrección v1.1) | pluviales, cloaca interna, iluminación exterior | PENDIENTE | — |
| OC-ADM | Oficina asset-light | — | m² PENDIENTES (DPV-16-12) | PENDIENTE | — |

**No son obra** (no reciben ningún USD/m²): terreno, retiros y buffers, reserva de expansión, área verde (12C no la modela: PENDIENTE). La v1.0 aplicaba un USD/m² de infraestructura a **todo** el terreno (incluidos retiros, buffers y reserva); en la v1.1 OC-INF es un lote global y la preparación del sitio usa el terreno **requerido**.

**Costo de OC-DP (único con precio, E4):** USD 43.779 (2.500) · 64.186 (5.000) · 119.200 (10.000) · 222.431 (20.000) para C1. Es una **nave seca**; usar ese USD/m² para proceso húmedo o frío sería un error de categoría.

## 5. Qué falta para costear la obra

1. USD/m² por categoría con fecha, TC, IVA y alcance (DPV-16-02).
2. Footprints de proveedor para salir de PROXY (DPV-090, SUP-107).
3. Sitio: retiros, FOS, suelo, cota, accesos (DPV-106, DPV-141).
4. Que 12C publique el **terreno sin reserva** como salida propia (propuesta T16-07), para que CAPEX lo consuma en lugar de pedírselo a la función.
