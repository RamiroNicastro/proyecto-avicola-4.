# Costos de alimento — tres arquitecturas

**Fecha:** 2026-10-02 · Implementación: `generar_registro()` §ALIMENTO en [`modelo_opex.py`](modelo_opex.py) · Drivers: 14B (`alimento`, `inventario_alimento`), que consume 03.

> Probablemente el bloque más pesado del OPEX (en la integración avícola el alimento suele ser la mayor partida del costo del pollo vivo; dato a confirmar con precios: DPV-050). El motor **no** formula dietas: la composición es un parámetro.

## 1. Cantidades (iguales en las tres arquitecturas)

| Escala (aves/día) | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Alimento terminado (t/año, 14B) | 3.091 | 6.181 | 12.362 | 24.724 |
| Maíz ilustrativo 60 % (t/año) | 1.854 | 3.709 | 7.417 | 14.835 |
| Harina de soja ilustrativa 30 % (t/año) | 927 | 1.854 | 3.709 | 7.417 |
| Resto agregado 10 % (t/año) | 309 | 618 | 1.236 | 2.472 |
| Viajes de granelero a granjas (por año; 28 t, 75 km) | 150 | 250 | 450 | 900 |

`[ESTIMACIÓN]` perfil medio (2,9 kg, FCR de 03); composición = puntos ilustrativos de 14B (SUP-032), **no** una dieta. Las t de 14B son alimento entregado en granja: las mermas de materias primas se agregan aparte (ALI-MERMA, cantidad PENDIENTE).

## 2. Arquitecturas

| | A. Compra | B1. Façon con MP de la empresa | B2. Façon con MP del elaborador | C. Planta propia |
|---|---|---|---|---|
| Alimento | ALI-A-PT (t × USD/t) | — | ALI-B-PTE (t × precio integral) | — |
| Materias primas | — | ALI-MP-* (t × USD/t) | — | ALI-MP-* |
| Servicio | — | ALI-B-SRV (t × USD/t) | (incluido en el precio) | — |
| Almacenamiento | — | ALI-B-ALM (t·mes de MP propias en el elaborador) | — | ALI-C-ALM (PENDIENTE) |
| Mermas | (del proveedor) | ALI-MERMA (PENDIENTE) | (del elaborador) | ALI-MERMA (PENDIENTE) |
| Energía, vapor, agua | — | — | — | ALI-C-ENE, ALI-C-TER, ALI-C-AGUA (PENDIENTES: kWh/t, vapor y agua sin dimensionar, DPV-158; **no** se usa el kWh ni el agua de la planta de faena de 09C) |
| Diferencial a puesto en planta | — | ALI-MP-DIF-* | — | ALI-MP-DIF-* (PENDIENTE) |
| Movimientos internos | — | — | — | ALI-C-MOV (PENDIENTE) |
| Análisis | — | — | — | ALI-C-ANA (PENDIENTE) |
| Personal | — | — | — | 14A no lo dimensiona → FTE PENDIENTE |
| Mantenimiento | — | — | — | MAN-ALI-* |
| Flete de alimento a granja | LOG-ALI-* | LOG-ALI-* | LOG-ALI-* | LOG-ALI-* |
| Flete de grano | — | LOG-GRA-* | — | LOG-GRA-* |
| Descarga | ALI-A-DES (puede estar en el flete) | — | — | — |
| Inventario propio (CT) | Alimento en silos de granja | MP + alimento hasta despacho (en el elaborador) | Solo alimento en silos de granja | Todo (granos, MP, alimento) |

Si la variante del façon no se define (`alimento_facon_mp = None`, caso C0 y C2), el registro muestra una sola fila PENDIENTE y el capital de trabajo marca la propiedad de las MP como **PENDIENTE** (no se asume). Variantes calculadas: `C0-10000-FACON-MP-EMPRESA`, `C0-10000-FACON-MP-ELABORADOR`, `C2-10000-FACON-MP-EMPRESA`.

Tests: compra no carga costos internos de fábrica (A01, mutación M03); planta propia no carga el precio del alimento terminado (A02); la t usada es la de 14B (D02, D03, mutación D01).

## 3. Precios disponibles

| ID | Valor | Evidencia | Uso |
|---|---|---|---|
| ALI-MP-MAIZ | **Precio observado:** ARS 295.800/t, pizarra Cámara Arbitral de Rosario, 2026-09-29, condición SOBRE_PUERTO_ROSARIO, IVA no informado (FTE-17-001). **Conversión del modelo:** ÷ 1.522 ARS/USD (A3500 del mismo día, FTE-17-003) = USD 194,35/t (`ORIGEN_PRECIO_USD = CONVERSION_MODELO`) | **E4** `[PVDP]` (extracto; sitio bloqueado) | C3, CF, variantes B1. **Precio Rosario ≠ costo puesto en planta**: el diferencial (zona, acondicionamiento, secado, comisiones) es ALI-MP-DIF-MAIZ, PENDIENTE; el flete es LOG-GRA-* |
| ALI-A-PT, ALI-B-*, ALI-MP-SOJA, aceite, núcleo, otros | — | PENDIENTE | DPV-050, DPV-155, DPV-157 |

Monto con precio (E4): maíz C3/CF = USD 0,36 / 0,72 / 1,44 / 2,88 M/año (2.500 / 5.000 / 10.000 / 20.000) ≈ USD 0,58 por ave faenada **solo por el maíz**. No es costo de alimento: faltan soja, núcleo, aceite, flete, mermas, energía, personal y mantenimiento.

## 4. Composición parametrizable

`composicion_alimento` acepta fracciones que suman 1 (`maiz`, `harina_soja`, `aceite`, `nucleo`, `otros` **o** `resto`). Si se carga, los drivers pasan a `DERIVADO_OPEX` con evidencia `[SUPUESTO]`. Sin input se usan los puntos de 14B; aceite, núcleo y otros quedan `INCLUIDO` en "resto" porque 14B solo da rangos (1–5 %, 2,5–4 %, 0,2–1,3 %).

## 5. Completitud (auditoría v1.1)

Planta propia: 12 bloques materiales representados (materias primas con filas explícitas de maíz, soja, aceite, núcleo y otros —estas tres `INCLUIDO` en "resto" hasta tener fórmula—, diferencial a planta, RRHH, electricidad, vapor, agua, mantenimiento, laboratorio, mermas, almacenamiento, movimientos internos, transporte). C3-10000: cobertura estructural 100 %, física 17 %, de costeo 0 % (el maíz con precio no completa el bloque de materias primas). Façon sin variante: fila explícita de alimento/materias primas con cantidad y sin precio aplicable (antes faltaba el bloque). Tests X03, X10.
