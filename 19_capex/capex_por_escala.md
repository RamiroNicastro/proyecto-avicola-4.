# CAPEX por escala y configuración — resultado de la versión 1.0

**Fecha:** 2026-10-02 · **FECHA_BASE_CAPEX:** 2026-10-01 · **Moneda:** USD · Datos: [`escenarios_capex.csv`](escenarios_capex.csv) (33 escenarios × 16 filas = 528) · BOQ: [`boq_capex.csv`](boq_capex.csv)

> **No hay CAPEX total publicable.** En todos los escenarios faltan precios para casi todos los conceptos. Lo que sigue es **CAPEX con precio** (parcial, nivel E4 `[PVDP]`), **conteo de faltantes** y **cobertura**. Ningún número de esta página sirve para decidir una inversión.

## 1. Resumen por escenario

| Escenario | Filas BOQ | Conceptos costeables | Con precio | Sin precio | Alcance pendiente | CAPEX con precio USD — medio (LOW–HIGH) | Evidencia | Cobertura por conceptos | Total |
|---|---|---|---|---|---|---|---|---|---|
| C0-2.500 a C0-20.000 | 31 | 21 | 0 | 21 | 0 | — | — | 0 % | NO DISPONIBLE |
| C1-2.500 | 162 | 76 | 1 | 75 | 0 | 43.779 (25.739–73.113) | E4 | 1,3 % | NO DISPONIBLE |
| C1-5.000 | 165 | 76 | 1 | 75 | 0 | 64.186 (34.501–111.125) | E4 | 1,3 % | NO DISPONIBLE |
| C1-7.500 | 166 | 76 | 1 | 75 | 0 | 92.140 (49.295–159.583) | E4 | 1,3 % | NO DISPONIBLE |
| C1-10.000 | 166 | 76 | 1 | 75 | 0 | 119.200 (63.727–206.509) | E4 | 1,3 % | NO DISPONIBLE |
| C1-15.000 | 168 | 76 | 1 | 75 | 0 | 171.593 (91.645–297.395) | E4 | 1,3 % | NO DISPONIBLE |
| C1-20.000 | 168 | 76 | 1 | 75 | 0 | 222.431 (118.711–385.611) | E4 | 1,3 % | NO DISPONIBLE |
| C2-2.500 | 181 | 88 | 2 | 86 | 8 | 389.936 (sin rango) | E4 | 2,3 % | NO DISPONIBLE |
| C2-5.000 | 184 | 88 | 2 | 86 | 8 | 756.501 | E4 | 2,3 % | NO DISPONIBLE |
| C2-10.000 | 185 | 88 | 2 | 86 | 8 | 1.503.829 | E4 | 2,3 % | NO DISPONIBLE |
| C2-20.000 | 187 | 88 | 2 | 86 | 8 | 2.991.687 | E4 | 2,3 % | NO DISPONIBLE |
| C3-2.500 | 221 | 138 | 2 | 136 | 8 | 1.428.407 | E4 | 1,4 % | NO DISPONIBLE |
| C3-5.000 | 224 | 138 | 2 | 136 | 8 | 2.833.443 | E4 | 1,4 % | NO DISPONIBLE |
| C3-10.000 | 225 | 138 | 2 | 136 | 8 | 5.657.713 | E4 | 1,4 % | NO DISPONIBLE |
| C3-20.000 | 227 | 138 | 2 | 136 | 8 | 11.299.457 | E4 | 1,4 % | NO DISPONIBLE |
| CF-* | +3 filas FUTURO sobre C3 | 138 | 2 | 136 | 8 | igual a C3 (lo futuro no entra) | E4 | 1,4 % | NO DISPONIBLE |

**Cobertura por valor:** NO CALCULABLE en todos los escenarios (los faltantes no tienen magnitud). **Cobertura por conceptos** ≠ cobertura por valor: 1 concepto de 76 con precio no significa 1,3 % de la inversión.

## 2. Qué contiene el "CAPEX con precio" (y por qué no es comparable entre configuraciones)

| Configuración | Componente con precio | Peso en el CAPEX con precio |
|---|---|---|
| C1 | Solo **depósitos y talleres secos** (OC-DP: 146–741 m² × USD 250–350/m²) | 100 % |
| C2 | OC-DP + **25 % de galpones** a ≥ USD 11,49/plaza (cota inferior de prensa) | galpones 89–93 % |
| C3 / CF | OC-DP + **100 % de galpones** | galpones 97–98 % |

Por eso **C3 parece 33–51 veces más cara que C1**: no es una conclusión, es el efecto de que el único precio disponible de cierta magnitud es el de galpones (T16-03). La planta de faena de C1 —proceso, frío, efluentes, eléctrico, obra húmeda— está **sin precio**.

Galpones de productores integrados (informativo, **no** CAPEX de la empresa, misma cota E4): C0/C1 USD 1,38 M (2.500) a 11,08 M (20.000); C2 el 75 % de eso.

## 3. Detalle por bloque — C1 y C3 a 10.000 aves/día

| Bloque | C1: estado | C1: costeables / con precio | C3: estado | C3: costeables / con precio | C3: USD con precio |
|---|---|---|---|---|---|
| TERRENO | INCOMPLETO | 5 / 0 | INCOMPLETO | 5 / 0 | — |
| OBRA_CIVIL | INCOMPLETO | 16 / 1 | INCOMPLETO | 16 / 1 | 119.200 (E4) |
| PROCESO | INCOMPLETO | 8 / 0 | INCOMPLETO | 8 / 0 | — |
| SUBPRODUCTOS | INCOMPLETO | 1 / 0 | INCOMPLETO | 2 / 0 | — |
| FRIO | INCOMPLETO | 1 / 0 | INCOMPLETO | 1 / 0 | — |
| UTILITIES | INCOMPLETO | 15 / 0 (5 sin cantidad) | INCOMPLETO | 15 / 0 | — |
| EFLUENTES | INCOMPLETO | 1 / 0 | INCOMPLETO | 1 / 0 | — |
| SERVICIOS_GENERALES | INCOMPLETO | 11 / 0 | INCOMPLETO | 11 / 0 | — |
| LOGISTICA | SIN_CONCEPTOS (flota tercerizada) | 0 / 0 | INCOMPLETO | 26 / 0 (9 sin cantidad) | — |
| INCUBACION | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 15 / 0 (3 sin cantidad) | — |
| ALIMENTO | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 18 / 0 (2 sin cantidad) | — |
| GRANJAS | EXCLUIDO_POR_ARQUITECTURA (0) | — | INCOMPLETO | 2 / 1 (+8 alcance pendiente) | 5.538.513 (E4, cota) |
| INDIRECTOS | INCOMPLETO | 7 / 0 | INCOMPLETO | 7 / 0 | — |
| PREOPERATIVOS | INCOMPLETO | 8 / 0 | INCOMPLETO | 8 / 0 | — |
| CONTINGENCIA | INCOMPLETO | 3 / 0 | INCOMPLETO | 3 / 0 | — |

## 4. Variantes a 10.000 aves/día (C1)

Todas tienen el mismo CAPEX con precio (USD 119.200) porque **los conceptos que cambian no tienen precio**. Lo que sí cambia es **físico**:

| Variante | Cambio físico en el BOQ |
|---|---|
| Reserva de terreno para 20.000 | Terreno 23.372 → 33.345 m² (medio); cerco pasa a REUTILIZABLE |
| Parque industrial | Precio TER-02; cargo de parque en lugar de acceso y conexiones (1 concepto menos) |
| Rural compatible | Precio TER-03 |
| Congelado tercerizado | Sin túnel de congelado (3 filas menos) |
| Congelado propio (P2) | Más m² de cámaras de congelado y capacidad de túnel |
| Subproductos básicos propios | + SB-BAS |
| Llave en mano | L11 reemplaza a L1–L5 (4 conceptos costeables menos, sin doble conteo) |
| Manual / automática | Cambia el nivel de 7 EQ (los que la matriz 08 deja como "M/S" o "S/A" a esta escala; 3–15 según la escala) y el factor de superficie de 12C |
| 6 días/semana | Mismas aves/día; más aves/año (driver de OPEX, no de capacidad) |

## 5. Cantidades físicas por escala (sí utilizables como orden de magnitud)

Detalle por módulo en [`obra_civil_capex.md`](obra_civil_capex.md), [`utilities_capex.md`](utilities_capex.md), [`logistica_capex.md`](logistica_capex.md) y [`upstream_capex.md`](upstream_capex.md).

| Escala (aves/día) | m² construidos (medio) | Terreno solo fase m² (medio) | Ritmo aves/h (8 h) | Flota propia vivo / refrigerado / alimento (C3) | Setter / hatcher (posiciones) | Planta de alimento t/h | Plazas de galpón |
|---|---|---|---|---|---|---|---|
| 2.500 | 1.796 | 15.450 | 312 | 2 / 2 / 2 | 55.824 / 18.515 | 2,1 | 120.507 |
| 5.000 | 2.664 | 18.194 | 625 | 2 / 2 / 2 | 111.648 / 37.030 | 4,2 | 241.014 |
| 10.000 | 4.454 | 23.706 | 1.250 | 3 / 2 / 2 | 223.296 / 74.060 | 8,4 | 482.029 |
| 20.000 | 7.795 | 33.081 | 2.500 | 4 / 3 / 3 | 446.593 / 148.120 | 16,7 | 964.058 |

(m² y terreno de C3, perfil P2; los de C1 en `obra_civil_capex.md`). El CAPEX **no** está obligado a escalar linealmente con estas cantidades (test S02).
