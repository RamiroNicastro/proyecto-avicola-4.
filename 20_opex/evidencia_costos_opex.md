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

## 2. Fecha y moneda

`FECHA_BASE_OPEX = 2026-10-01` (editable). Cada precio guarda moneda original, fecha, TC (moneda por USD), tipo de TC, fecha y fuente del TC y equivalente USD. Precios anteriores a la fecha base se marcan `PRECIO_ANTERIOR_A_FECHA_BASE` y **no** se indexan; las columnas `INDICE_ACTUALIZACION` y `FECHA_ACTUALIZACION` quedan preparadas para el modelo financiero.

## 3. Estado de la base

| | Conceptos |
|---|---|
| Total | **323** |
| PENDIENTE (sin precio) | **301** |
| Con precio usado (`CON_PRECIO`) | **3**, todos **E4** `[PVDP]` |
| Referencias no usadas / descartadas | 2 / 1 |
| Estructura FUTURO (reproductoras, rendering) / OPCIONAL (halal) | 8 / 8 |

| ID | Valor | Fuente | Por qué E4 / uso |
|---|---|---|---|
| **ALI-MP-MAIZ** | ARS 295.800/t (pizarra Rosario, 2026-09-29) ÷ 1.522 = **USD 194,35/t** | FTE-17-001 (TC: FTE-17-003) | Extracto de buscador; sitio de la Cámara Arbitral bloqueado. Precio sobre puerto (no puesto en planta); IVA no resuelto |
| **POL-COMPRA** | ARS 1.312,22/pollito sin IVA (CAPIA, semana 2026-07-06) ÷ 1.486,50 = **USD 0,8828** | FTE-17-002 (TC: FTE-17-004) | Extracto de un sitio que reproduce precios de CAPIA (bloqueado); lugar de entrega PENDIENTE; anterior a la fecha base |
| **LAB-PARAM-MESES** | 13 meses remunerados (12 + SAC) | FTE-17-008 | Parámetro legal (Ley 20.744) no leído en original; no es un salario |
| REF-SOJA-POROTO | ARS 560.000/t (2026-09-01) | FTE-17-005 | Soja poroto ≠ harina de soja: no se usa |
| REF-HSOJA-INT | USD 461,95/t (futuros sep-2026) | FTE-17-006 | Mercado internacional y punto de entrega distintos: no se usa |
| REF-POL-CONTRA | "$ 16 por unidad" (2026-09-13) | FTE-17-007 | **Descartado**: incompatible con ARS 1.312 de la misma cámara dos meses antes; probable página antigua mal fechada (regla 16) |

Los tipos de cambio también son extractos de prensa (A3500, `[PVDP]`).

## 4. Búsqueda realizada (2026-10-02)

Se buscaron solo referencias de alto impacto (maíz, soja, pollito BB, tipo de cambio). Los sitios primarios (Cámara Arbitral de Rosario, cadenaavicola.com) están **bloqueados por la red de la sesión**: todas las cifras quedan `[PVDP]` y no se degradó la regla de evidencia. No se buscaron tarifas eléctricas, de gas, agua ni salarios de convenio: requieren el cuadro tarifario o el convenio del sitio y la categoría, y no hay sitio elegido (DEC-003, DEC-055). Ver la matriz de validación.
