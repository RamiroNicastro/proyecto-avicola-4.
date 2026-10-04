# Evidencia de costos OPEX — niveles, reglas y estado de la base

**Fecha:** 2026-10-02 · Base: [`base_costos_opex.csv`](base_costos_opex.csv) · Fuentes provisionales: [`fuentes_17.csv`](fuentes_17.csv)

## 1. Niveles (misma jerarquía que CAPEX)

| Nivel | Qué es | Requisito validado |
|---|---|---|
| **E1** | Cotización formal para el proyecto | `TIPO_PRECIO = cotizacion` + lectura primaria |
| **E2** | Lista o comunicación directa de proveedor | Lectura primaria |
| **E3** | Fuente oficial, tarifa publicada, convenio, benchmark técnico **leído en original** | Lectura primaria |
| **E4** | Extracto de buscador, prensa, fuente comercial secundaria `[PVDP]` | Fuente |
| **E5** | Supuesto de ingeniería | Fuente = documento del supuesto |
| **PENDIENTE** | Sin precio | Precio vacío (nunca 0) |

Reglas (`validar_base()`, tests C03, E05): sin precio ⇒ PENDIENTE; con precio ⇒ E1–E5 y fuente; E1 exige cotización; E1–E3 exigen lectura primaria; un precio en ARS u otra moneda exige TC, tipo de TC y fecha; `PRECIO_USD_EQUIVALENTE` debe coincidir con precio ÷ TC; ningún precio negativo; un rango exige `ORIGEN_RANGO`; el % variable de un semivariable debe declararse SUPUESTO. Los montos se publican **separados por evidencia** (`OPEX_E1_E2` … `OPEX_E5`, `CALIDAD_MONTO`) y E4 nunca aparece como costo validado (test E01; mutación M06).

## 2. Fecha, moneda y separación precio observado / conversión

`FECHA_BASE_OPEX = 2026-10-01` (editable). Un precio en moneda local es una **observación en ARS**; su equivalente en USD es una **conversión del modelo**, no una nueva observación de mercado. La base y el registro guardan por separado: precio original observado, moneda, fecha del precio, condición de entrega (`CONDICION_ENTREGA`), IVA, fuente, TC usado, tipo y fecha del TC, fuente del TC, USD resultante y `ORIGEN_PRECIO_USD` (`CONVERSION_MODELO` u `OBSERVADO_EN_USD`). Precios anteriores a la fecha base se marcan `PRECIO_ANTERIOR_A_FECHA_BASE` y **no** se indexan; `INDICE_ACTUALIZACION` y `FECHA_ACTUALIZACION` quedan preparados para el modelo financiero (test X09).

## 3. Estado de la base (v1.1)

| | Conceptos |
|---|---|
| Total | **359** (v1.0: 323; se agregaron bloques materiales faltantes y componentes laborales) |
| PENDIENTE (sin precio) | **329** |
| Con precio usado (`CON_PRECIO`) | **2**, ambos **E4** `[PVDP]` (v1.0: 3; se retiró "13 meses remunerados") |
| Referencias no usadas / descartadas | 2 / 1 |
| Estructura FUTURO (reproductoras, rendering) / OPCIONAL (halal) | 17 / 8 |

| ID | Precio observado (moneda original) | Conversión del modelo | Fuente | Por qué E4 / uso |
|---|---|---|---|---|
| **ALI-MP-MAIZ** | ARS 295.800/t · pizarra Cámara Arbitral de Rosario · 2026-09-29 · **SOBRE_PUERTO_ROSARIO** · IVA no informado | ÷ 1.522 ARS/USD (A3500, 2026-09-29) = USD 194,35/t | FTE-317 (TC: FTE-318) | Extracto; sitio bloqueado. **Precio Rosario ≠ costo puesto en planta**: diferencial ALI-MP-DIF-MAIZ (PENDIENTE) y flete LOG-GRA-* aparte (test X10) |
| **POL-COMPRA** | ARS 1.312,22/pollito · **sin IVA** (ARS 1.450 con IVA 10 %) · semana 2026-07-06 · entrega PENDIENTE | ÷ 1.486,50 ARS/USD (A3500, 2026-07-06) = USD 0,8828 | FTE-029 (TC: FTE-319) | Extracto de un sitio que reproduce CAPIA (bloqueado); anterior a la fecha base; flete incluido PENDIENTE |

**SAC (aguinaldo):** ya **no** figura en la base de precios. Es una regla laboral en [`reglas_laborales_opex.csv`](reglas_laborales_opex.csv) (`REGLA_LABORAL_PENDIENTE_VERIFICACION`, fuente normativa Ley 20.744 arts. 121–122 a leer en original: DPV-148), sin nivel E1–E5 (tests X07, X08).

| Referencia | Valor | Fuente | Uso |
|---|---|---|---|
| REF-SOJA-POROTO | ARS 560.000/t (2026-09-01) | FTE-320 | Soja poroto ≠ harina de soja: no se usa |
| REF-HSOJA-INT | USD 461,95/t (futuros sep-2026) | FTE-321 | Mercado internacional y punto de entrega distintos: no se usa |
| REF-POL-CONTRA | "$ 16 por unidad" (2026-09-13) | FTE-322 | **Descartado**: incompatible con ARS 1.312 de la misma cámara dos meses antes; probable página antigua mal fechada (regla 16) |

Los tipos de cambio también son extractos de prensa (A3500, `[PVDP]`).

## 4. Búsqueda realizada (2026-10-02)

Se buscaron solo referencias de alto impacto (maíz, soja, pollito BB, tipo de cambio). Los sitios primarios (Cámara Arbitral de Rosario, cadenaavicola.com) están **bloqueados por la red de la sesión**: todas las cifras quedan `[PVDP]` y no se degradó la regla de evidencia. No se buscaron tarifas eléctricas, de gas, agua ni salarios de convenio: requieren el cuadro tarifario o el convenio del sitio y la categoría, y no hay sitio elegido (DEC-003, DEC-055). Ver la matriz de validación.
