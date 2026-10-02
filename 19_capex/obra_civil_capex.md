# Obra civil y terreno — CAPEX paramétrico

**Fecha:** 2026-10-02 (v1.2, semántica de terreno) · Superficies: `09_layout_obra_civil/modelo_superficies.py` (12C) · Precios: [`base_costos_capex.csv`](base_costos_capex.csv) · Procedencia: [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv)

> **Superficie conceptual ≠ proyecto ejecutivo.** CAPEX **consume** las superficies de 12C (no las recalcula ni crea otra definición): para la escala y arquitectura pedidas llama a la misma función de 12C y, cuando las entradas coinciden con un escenario publicado en `escenarios_superficies.csv`, la salida es **idéntica** a ese escenario (test N01). Cada categoría tiene su propio USD/m², hoy casi todos **PENDIENTES**.

## 1. Fórmula

```
COSTO_OBRA(categoría) = m²(categoría, bajo/medio/alto de 12C) × USD/m²(categoría, bajo/medio/alto)
TERRENO              = m² A ADQUIRIR (decisión: criterio_terreno) × USD/m² (por tipo) + gastos de compra (%)
                       + preparación (m² del MÍNIMO FÍSICO × USD/m²)
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

| Escala | TERRENO_MINIMO_FISICO_DERIVADO (función 12C, sin reserva ni rendering) | TERRENO_CONCEPTUAL_12C (publicado, `referencia`) | SUPERFICIE_ESCENARIO_OBJETIVO_20000_12C (publicado, `objetivo_20000`) |
|---|---|---|---|
| 2.500 | 6.470 / 15.398 / 37.510 | 7.918 / 19.868 / 53.212 | 14.069 / 33.345 / 82.253 |
| 5.000 | 7.528 / 18.029 / 44.536 | 9.173 / 23.431 / 64.897 | 14.069 / 33.345 / 82.253 |
| 10.000 | 9.678 / 23.372 / 57.569 | 11.743 / 30.768 / 87.077 | 14.069 / 33.345 / 82.253 |
| 20.000 | 13.492 / 32.379 / 80.673 | 16.509 / 43.660 / 127.938 | 14.069 / 33.345 / 82.253 |

### De dónde salían las cifras aproximadas de la v1.0

| Cifra citada | Origen exacto | ¿Coincide con 12C? | Corrección |
|---|---|---|---|
| ≈ 1.800 m² a 2.500 | 1.796 = m² construidos medio de 12C `perfil_P2` (CAPEX C3 usa P2) | Sí, pero de un escenario distinto de la referencia de 12C (1.777, P1) y sin decirlo | Las tablas indican ahora el escenario (P1 `referencia` o `perfil_P2`) |
| ≈ 7.800 m² a 20.000 | 7.795 = 12C `perfil_P2` medio | Ídem (referencia P1: 7.451) | Ídem |
| ≈ 15.400 m² de terreno a 2.500 | 15.398 = función de terreno de 12C con escala objetivo = escala y sin rendering | **No**: 12C no publica un terreno sin reserva (su terreno publicado incluye una reserva proxy y rendering: 19.868) | Se rotula **TERRENO_MINIMO_FISICO_DERIVADO** = CALCULO_MODELO_FUENTE (misma fórmula de 12C, entrada no publicada); se informa al lado el terreno publicado de 12C. Tensión T16-07 |
| ≈ 32.400 m² de terreno a 20.000 | 32.379, ídem | **No** (12C publica 43.660) | Ídem |
| ≈ 33.300 m² rotulado en la v1.1 como terreno comprado para 20.000 | 33.345 = 12C `objetivo_20000` | Sí, directo, pero **con otra semántica** (ver §3) | Renombrado `SUPERFICIE_ESCENARIO_OBJETIVO_20000_12C`; ya no se presenta como terreno a comprar |

Ninguna de esas cifras provenía de una fórmula alternativa de CAPEX, pero dos se presentaban como "terreno de 12C" cuando eran una entrada que 12C no publica, y dos no decían que correspondían al perfil P2.

## 3. Cuatro magnitudes de terreno (cierre de la sesión 16)

### 3.1 Qué contiene cada cifra (20.000 aves/día, nivel medio, m²)

| Componente | Mínimo físico derivado | Escenario `objetivo_20000` (12C) | Conceptual 12C `referencia` a 20.000 |
|---|---|---|---|
| Construido (huella de edificios) | 7.451 | 7.451 | 7.451 |
| Exteriores (playas, circulación, estacionamiento, plataformas) | 6.147 | 6.147 | 6.147 |
| Efluentes | 592 | 592 | 592 |
| Reserva de expansión **hasta** la escala objetivo (Σ max(0, áreas(20.000) − áreas actuales)) | — | 0 (a 20.000 ya se llegó; desde 5.000 serían 8.774) | — |
| Reserva de expansión **más allá** de la escala (sin objetivo: 25 / 50 / 100 % del operativo, SUP-119, PROXY) | — | — | 7.095 |
| Reserva de rendering futuro | — | 640 | 640 |
| Área interna | 14.190 | 14.830 | 21.925 |
| Retiros + buffers (margen perimetral 30 m; rectángulo 1,5) | 18.189 | 18.515 | 21.735 |
| **Terreno total** | **32.379** | **33.345** | **43.660** |

- **`objetivo_20000` en 12C** = el terreno de un escenario con escala objetivo 20.000: la planta de la escala actual + la diferencia de áreas hasta 20.000 por categoría + rendering + retiros y buffers. Por eso da 33.345 m² desde **cualquier** escala de partida. **Cubre** el mínimo físico de 20.000 (32.379) más el rendering, pero **no** incluye reserva para crecer **más allá** de 20.000.
- **El 43.660 de 12C a 20.000** no es "el terreno necesario para 20.000": es el escenario **sin escala objetivo**, en el que 12C agrega una reserva proxy fraccional (50 % del operativo en el nivel medio) para una expansión **indefinida** posterior. La diferencia 33.345 vs 43.660 (≈ 10.300 m²) es esa reserva (7.095) más los retiros/buffers que crecen con el área (3.220).
- Son **universos distintos**; no hay incompatibilidad. El 33.345 no es menor que lo que necesita una planta de 20.000; es menor que una planta de 20.000 **con reserva para seguir creciendo**.

### 3.2 Qué usa CAPEX

| Driver | Definición | Uso |
|---|---|---|
| `terreno_minimo_fisico` (TERRENO_MINIMO_FISICO_DERIVADO) | huella + exteriores + efluentes + retiros/buffers de la escala actual (función de 12C; 12C no lo publica, T16-07) | preparación del sitio (TER-PREP) |
| `terreno_conceptual_12c` (TERRENO_CONCEPTUAL_12C) | lo que 12C publica para la escala, sin objetivo | contexto y opción de criterio |
| `superficie_escenario_objetivo_12c` (SUPERFICIE_ESCENARIO_OBJETIVO_X_12C) | 12C con escala objetivo X (20.000 por defecto) | contexto y opción de criterio |
| `terreno_requerido_arquitectura` | lo que la arquitectura declara necesitar: mínimo físico; + rendering si lo declara; = superficie objetivo X si declara reserva hasta X (`compra_reserva` o `escala_objetivo`) | umbral de alerta |
| `terreno_a_adquirir` | **DECISIÓN** (`criterio_terreno`: `minimo_fisico` · `conceptual_12c` · `objetivo_12c` · `requerido_arquitectura` · `usuario` con `terreno_adquirido_m2`) | TER-COMPRA y cerco |

**CAPEX no supone que ninguna de las tres cifras de 12C sea el terreno que se compra.** Sin criterio seleccionado (valor por defecto), TER-COMPRA se dimensiona **provisionalmente** con `terreno_requerido_arquitectura`, la fila queda `PROVISIONAL_CRITERIO_NO_SELECCIONADO`, cualquier costo lleva la alerta `COSTO_PROVISIONAL` con el driver costeado y el bloque TERRENO no puede quedar COMPLETO (test N22). No hay `max()` implícito entre definiciones (test N23).

### 3.3 Alertas

| Alerta | Cuándo | Significado |
|---|---|---|
| `TERRENO_CRITERIO_NO_SELECCIONADO` | criterio vacío | el terreno es provisional |
| `TERRENO_ADQUIRIDO_MENOR_QUE_REQUERIDO_ARQUITECTURA` | terreno a adquirir < requerido por la arquitectura (por nivel) | terreno insuficiente para lo que la arquitectura declara; no se corrige (test N21) |
| `SUPERFICIE_OBJETIVO_MENOR_QUE_CONCEPTUAL_12C_X` | superficie objetivo X < conceptual 12C publicado para X | **diferencia de universo**, explicada en el texto de la alerta; no es incompatibilidad (test N24) |
| `SUPERFICIE_OBJETIVO_NO_CUBRE_MINIMO_FISICO_X` | superficie objetivo X < mínimo físico de X | sería una inconsistencia real; hoy no ocurre en ninguna combinación |

El rango de terreno sigue siendo amplio (por ejemplo, 14.069 / 33.345 / 82.253 m² para el escenario objetivo) porque retiros (5/10/15 m), buffers (10/20/40 m, PROXY) y FOS son desconocidos (DPV-106, DPV-141).

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
| OC-CER | Cerco perimetral (m) | perímetro | perímetro del terreno a adquirir | PENDIENTE | — |
| OC-INF | Infraestructura del predio | **lote** (corrección v1.1) | pluviales, cloaca interna, iluminación exterior | PENDIENTE | — |
| OC-ADM | Oficina asset-light | — | m² PENDIENTES (DPV-16-12) | PENDIENTE | — |

**No son obra** (no reciben ningún USD/m²): terreno, retiros y buffers, reserva de expansión, área verde (12C no la modela: PENDIENTE). La v1.0 aplicaba un USD/m² de infraestructura a **todo** el terreno (incluidos retiros, buffers y reserva); en la v1.1 OC-INF es un lote global y la preparación del sitio usa el **mínimo físico**.

**Costo de OC-DP (único con precio, E4):** USD 43.779 (2.500) · 64.186 (5.000) · 119.200 (10.000) · 222.431 (20.000) para C1. Es una **nave seca**; usar ese USD/m² para proceso húmedo o frío sería un error de categoría.

## 5. Qué falta para costear la obra

1. USD/m² por categoría con fecha, TC, IVA y alcance (DPV-16-02).
2. Footprints de proveedor para salir de PROXY (DPV-090, SUP-107).
3. Sitio: retiros, FOS, suelo, cota, accesos (DPV-106, DPV-141).
4. Que 12C publique el **terreno sin reserva** como salida propia (propuesta T16-07), para que CAPEX lo consuma en lugar de pedírselo a la función.
