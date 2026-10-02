# CAPEX por escala y configuración — resultado de la versión 1.1

**Fecha:** 2026-10-02 (v1.1, auditoría de procedencia) · **FECHA_BASE_CAPEX:** 2026-10-01 · **Moneda:** USD · Datos: [`escenarios_capex.csv`](escenarios_capex.csv) (33 escenarios × 16 filas = 528) · BOQ: [`boq_capex.csv`](boq_capex.csv) · Drivers: [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv)

> **No hay CAPEX total publicable.** En todos los escenarios faltan precios para casi todos los conceptos. Lo que sigue es un **monto con referencias débiles E4** (`[PVDP]`), el **conteo de faltantes** y la **cobertura**. Ningún número en USD de esta página sirve para decidir una inversión.

## 1. Resumen por escenario

| Escenario | Conceptos costeables | Con precio (E1_E2 / E3 / E4 / E5) | Pendientes | Alcance pendiente | Monto con precio USD — medio (LOW–HIGH) | Calidad del monto | Cobertura por conceptos | Total |
|---|---|---|---|---|---|---|---|---|
| C0-2.500 a C0-20.000 | 21 | 0 / 0 / 0 / 0 | 21 | 0 | — | SIN_MONTO | 0 % | NO DISPONIBLE |
| C1-2.500 | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 43.779 (25.739–73.113) | MONTO_CON_REFERENCIAS_DEBILES_E4 | 1,3 % | NO DISPONIBLE |
| C1-5.000 | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 64.186 (34.501–111.125) | ídem | 1,3 % | NO DISPONIBLE |
| C1-7.500 (intermedia) | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 92.140 (49.295–159.583) | ídem | 1,3 % | NO DISPONIBLE |
| C1-10.000 | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 119.200 (63.727–206.509) | ídem | 1,3 % | NO DISPONIBLE |
| C1-15.000 (intermedia) | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 171.593 (91.645–297.395) | ídem | 1,3 % | NO DISPONIBLE |
| C1-20.000 | 76 | 0 / 0 / 1 / 0 | 75 | 0 | 222.431 (118.711–385.611) | ídem | 1,3 % | NO DISPONIBLE |
| C2-2.500 | 88 | 0 / 0 / 2 / 0 | 86 | 8 | 389.936 (sin rango) | ídem | 2,3 % | NO DISPONIBLE |
| C2-5.000 | 88 | 0 / 0 / 2 / 0 | 86 | 8 | 756.501 | ídem | 2,3 % | NO DISPONIBLE |
| C2-10.000 | 88 | 0 / 0 / 2 / 0 | 86 | 8 | 1.503.829 | ídem | 2,3 % | NO DISPONIBLE |
| C2-20.000 | 88 | 0 / 0 / 2 / 0 | 86 | 8 | 2.991.687 | ídem | 2,3 % | NO DISPONIBLE |
| C3-2.500 | 138 | 0 / 0 / 2 / 0 | 136 | 8 | 1.428.407 | ídem | 1,4 % | NO DISPONIBLE |
| C3-5.000 | 138 | 0 / 0 / 2 / 0 | 136 | 8 | 2.833.443 | ídem | 1,4 % | NO DISPONIBLE |
| C3-10.000 | 138 | 0 / 0 / 2 / 0 | 136 | 8 | 5.657.713 | ídem | 1,4 % | NO DISPONIBLE |
| C3-20.000 | 138 | 0 / 0 / 2 / 0 | 136 | 8 | 11.299.457 | ídem | 1,4 % | NO DISPONIBLE |
| CF-* | 138 (+3 filas FUTURO) | 0 / 0 / 2 / 0 | 136 | 8 | igual a C3 (lo futuro no entra) | ídem | 1,4 % | NO DISPONIBLE |

**Cobertura por valor:** NO CALCULABLE en todos los escenarios (los faltantes no tienen magnitud). **Cobertura por conceptos** ≠ cobertura por valor: 1 concepto de 76 con precio no significa 1,3 % de la inversión. La columna "con precio" es un **conteo por nivel de evidencia**, no un porcentaje económico.

## 2. Qué contiene el monto con precio (y por qué no es comparable entre configuraciones)

| Configuración | Componente con precio | Peso en el monto |
|---|---|---|
| C1 | Solo **depósitos y talleres secos** (OC-DP: 146–741 m² × USD 250–350/m², E4) | 100 % |
| C2 | OC-DP + **25 % de galpones** a ≥ USD 11,49/plaza (cota inferior de prensa, E4) | galpones 89–93 % |
| C3 / CF | OC-DP + **100 % de galpones** | galpones 97–98 % |

Por eso **C3 parece 33–51 veces más cara que C1**: no es una conclusión, es el efecto de que el único precio de cierta magnitud es el de galpones (T16-03). La planta de faena de C1 —proceso, frío, efluentes, eléctrico, obra húmeda— está **sin precio**.

Galpones de productores integrados (informativo, **no** CAPEX de la empresa, misma cota E4): C0/C1 USD 1,38 M (2.500) a 11,08 M (20.000); C2 el 75 % de eso.

## 3. Detalle por bloque — C1 y C3 a 10.000 aves/día

| Bloque | C1: estado | C1: costeables / con precio | C3: estado | C3: costeables / con precio | C3: USD con precio (E4) |
|---|---|---|---|---|---|
| TERRENO | INCOMPLETO | 5 / 0 | INCOMPLETO | 5 / 0 | — |
| OBRA_CIVIL | INCOMPLETO | 16 / 1 | INCOMPLETO | 16 / 1 | 119.200 |
| PROCESO | INCOMPLETO | 8 / 0 | INCOMPLETO | 8 / 0 | — |
| SUBPRODUCTOS | INCOMPLETO | 1 / 0 | INCOMPLETO | 2 / 0 | — |
| FRIO | INCOMPLETO | 1 / 0 (capacidad de diseño PENDIENTE) | INCOMPLETO | 1 / 0 | — |
| UTILITIES | INCOMPLETO | 15 / 0 | INCOMPLETO | 15 / 0 | — |
| EFLUENTES | INCOMPLETO | 1 / 0 | INCOMPLETO | 1 / 0 | — |
| SERVICIOS_GENERALES | INCOMPLETO | 11 / 0 | INCOMPLETO | 11 / 0 | — |
| LOGISTICA | SIN_CONCEPTOS (flota tercerizada) | 0 / 0 | INCOMPLETO | 26 / 0 | — |
| INCUBACION | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 15 / 0 | — |
| ALIMENTO | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 18 / 0 | — |
| GRANJAS | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 2 / 1 (+8 alcance pendiente) | 5.538.513 (cota) |
| INDIRECTOS | INCOMPLETO | 7 / 0 | INCOMPLETO | 7 / 0 | — |
| PREOPERATIVOS | INCOMPLETO | 8 / 0 | INCOMPLETO | 8 / 0 | — |
| CONTINGENCIA | INCOMPLETO | 3 / 0 | INCOMPLETO | 3 / 0 | — |

## 4. Variantes a 10.000 aves/día (C1)

Todas tienen el mismo monto con precio (USD 119.200, E4) porque **los conceptos que cambian no tienen precio**. Lo que cambia es físico:

| Variante | Cambio físico en el BOQ |
|---|---|
| Escala objetivo 20.000 (`compra_reserva`) | Terreno requerido por la arquitectura 23.372 → 33.345 m² (medio; = SUPERFICIE_ESCENARIO_OBJETIVO_20000_12C); el mínimo físico sigue en 23.372 m²; terreno a adquirir PROVISIONAL hasta elegir criterio |
| Parque industrial | Precio TER-02; cargo de parque en lugar de acceso y conexiones (1 concepto menos) |
| Rural compatible | Precio TER-03 |
| Congelado tercerizado | Sin túnel de congelado (3 filas menos); áreas no publicadas por 12C (alerta) |
| Congelado propio (P2) | Áreas = 12C `perfil_P2` |
| Subproductos básicos propios | + SB-BAS |
| Llave en mano | L11 reemplaza a L1–L5 (4 conceptos costeables menos, sin doble conteo) |
| Manual / automática | Cambia el nivel de 7 EQ (3–15 según la escala) y las áreas (12C `automatizacion_manual` / `_auto`) |
| 6 días/semana | Mismas aves/día; áreas de 12C con 300 días/año (no publicadas por 12C: alerta); 09C publica también 6 días |

## 5. Cantidades físicas por escala (utilizables como orden de magnitud, con su procedencia)

| Escala (aves/día) | m² construidos 12C `referencia` (C1, P1) | m² construidos 12C `perfil_P2` (C2/C3) | Terreno mínimo físico derivado (C1) | Terreno conceptual 12C (`referencia`) | SUPERFICIE_ESCENARIO_OBJETIVO_20000_12C | Ritmo operativo / nominal requerido (aves/h, 05) | Flota propia vivo / refrig. / alim. (C3) | Setter / hatcher (cadencia 2) | Planta de alimento t/h (5 × 8, η 0,85) | Plazas de galpón |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 1.777 | 1.796 | 15.398 | 19.868 | 33.345 | 312 / 351 | 2 / 2 / 2 | 55.824 / 18.515 | 2,1 | 120.507 |
| 5.000 | 2.597 | 2.664 | 18.029 | 23.431 | 33.345 | 625 / 702 | 2 / 2 / 2 | 111.648 / 37.030 | 4,2 | 241.014 |
| 10.000 | 4.306 | 4.454 | 23.372 | 30.768 | 33.345 | 1.250 / 1.404 | 3 / 2 / 2 | 223.296 / 74.060 | 8,4 | 482.029 |
| 20.000 | 7.451 | 7.795 | 32.379 | 43.660 | 33.345 | 2.500 / 2.809 | 4 / 3 / 3 | 446.593 / 148.120 | 16,7 | 964.058 |

Valores medios; bajo/alto en [`obra_civil_capex.md`](obra_civil_capex.md) §2 y en el mapa de drivers. Procedencia: m², terreno conceptual, superficie objetivo y plazas, setters, hatchers, t/h, flota de aves vivas = **DIRECTO**; mínimo físico = **CALCULO_MODELO_FUENTE** (12C no lo publica); el terreno a adquirir es una **decisión** (`criterio_terreno`, ver `obra_civil_capex.md` §3); flota refrigerada y de alimento = **DERIVADO_CAPEX**. La v1.0 mostraba en esta tabla los m² de P2 y el terreno sin reserva sin indicarlo (ver `obra_civil_capex.md` §2). El CAPEX **no** está obligado a escalar linealmente con estas cantidades (test S02).
