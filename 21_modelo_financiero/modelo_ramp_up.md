# Fases, puesta en marcha, ramp-up y utilización

**Fecha:** 2026-10-04 · Código: `_fila_curva()`, fases y operación en `simular()` · Curvas: [`curvas_rampup.csv`](curvas_rampup.csv)

## 1. Fases del proyecto

| Fase | Meses | Qué ocurre en el modelo |
|---|---|---|
| T0 | instante 0 | Solo desembolsos (CAPEX, aportes, deuda) |
| PREOPERACION | `meses_preoperacion` | CAPEX según curva; sin operación |
| CONSTRUCCION | `meses_construccion` | CAPEX según curva; intereses de deuda si la hay |
| COMMISSIONING | `meses_commissioning` | CAPEX (los preoperativos PRE-* de 19_capex viven en CAPEX); **OPEX = 0** para no duplicarlos (SUP-19-10) |
| RAMP_UP | desde el mes `inicio_op` hasta el último mes de la curva | Utilización técnica creciente; ineficiencias de arranque |
| OPERACION_MADURA | después | Rige el último valor de la curva |

`inicio_op = preoperación + construcción + commissioning + 1`. Las duraciones son **inputs** (hoy PENDIENTES: DPV-086 ampliado como DPV-19-03). El CAPEX no ocurre todo en T0: la **CURVA_DE_DESEMBOLSO_CAPEX** reparte el monto de cada etapa en meses relativos a su entrada en operación (`[[−12, 0,1], [−8, 0,5], [−3, 0,4]]`; test N18). Hoy está PENDIENTE (cronograma de obra, anticipos y plazos de entrega: DPV-086, DPV-167, DPV-19-01).

## 2. Tres utilizaciones (más una cuarta para decidir)

| Utilización | Definición | Puede superar 1 | Fuente |
|---|---|---|---|
| **Técnica** | aves disponibles ÷ capacidad (curva de ramp-up de cada etapa) | No | curva |
| **Comercial** | aves requeridas por la demanda (parte limitante) ÷ capacidad | **Sí** (= factor demanda/capacidad de 23) | demanda |
| **Efectiva** | aves faenadas ÷ capacidad = mín(técnica, comercial) | No | la que usa el financiero |
| **Requerida (break-even)** | utilización mínima para EBITDA = 0 | Sí (si > 1 no es alcanzable) | [`break_even.md`](break_even.md) |

`escenarios_financieros.csv` informa `U_TECNICA`, `U_COMERCIAL_REQUERIDA` y `U_EFECTIVA` del último año y `BE_UTILIZACION_EBITDA` (*required* vs *actual*). Capacidad = escala operativa de 23 (SUP-052): **no** es capacidad nominal de equipos ni demanda.

## 3. Curva de ramp-up

Formato (`curvas_rampup.csv` o JSON): `MES` (desde la entrada de la etapa, escalón), `UTILIZACION` (técnica), `MERMA` (fracción de la producción perdida por arranque), `EFICIENCIA` (≤ 1: los costos variables por ave se dividen por ella), `COSTOS_EXTRA_USD_MES` (horas extra, scrap, asistencia técnica), `OBSERVACIONES`.

| Curva (plantilla) | Utilización técnica (mes: valor) | Merma / eficiencia / extras | Origen |
|---|---|---|---|
| CONSERVADOR | 1: 0,25 · 3: 0,40 · 6: 0,55 · 9: 0,65 · 12: 0,75 · 18: 0,85 · 24: 1,0 | PENDIENTES | SUP-19-09: **ilustrativa, sin fuente** |
| BASE | 1: 0,35 · 3: 0,55 · 6: 0,70 · 9: 0,80 · 12: 0,90 · 18: 1,0 | PENDIENTES | SUP-19-09 |
| RAPIDO | 1: 0,50 · 2: 0,70 · 4: 0,85 · 6: 0,95 · 9: 1,0 | PENDIENTES | SUP-19-09 |

- Son **plantillas**, no la curva del proyecto (DEC-090 abierta). En modo evidencia no se usa ninguna.
- El 1,0 final es la capacidad **operativa** (definición de 23), no implica vender: la utilización efectiva la limita la demanda.
- Sin merma, eficiencia y extras declarados, el bloque RAMPUP queda incompleto. El usuario puede declararlos (`rampup_ineficiencias`) y quedan trazados como escenario (DPV-19-07).
- Stress `rampup_lento_factor` estira la curva en el tiempo (test N19).

## 4. Qué afecta el ramp-up

| Afecta | Cómo |
|---|---|
| Producción y ventas | aves faenadas = mín(técnica, comercial) × capacidad; merma reduce los kg vendibles |
| OPEX variable | × utilización efectiva ÷ eficiencia |
| OPEX fijo y semifijo | **No** cae con la utilización (test F08; mutación M07) |
| Costos extra | se suman antes del EBITDA |
| Capital de trabajo | CxC, CxP e inventarios siguen a ventas y costos del mes (ΔCT del arranque) |
| Caja | pérdidas del arranque + ΔCT + CAPEX → valle de caja (`PICO_REQUERIMIENTO_FONDOS`) |

## 5. Expansiones

Cada etapa de una trayectoria tiene su propia curva aplicada a su **incremento** de capacidad desde su entrada; la merma y la eficiencia se ponderan por las aves disponibles de cada incremento. Ver [`expansion_financiera.md`](expansion_financiera.md).
