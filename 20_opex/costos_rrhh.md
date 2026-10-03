# Costo laboral — RRHH industrial vs universos upstream

**Fecha:** 2026-10-02 (v1.1, auditoría de completitud y costo laboral) · Drivers: 14A (`modelo_rrhh.calcular`) · Salida: [`modelo_costo_laboral.csv`](modelo_costo_laboral.csv) · Reglas: [`reglas_laborales_opex.csv`](reglas_laborales_opex.csv) · Implementación: `lineas_laborales()`, `fte_universos()`, `costo_empresa_fte()`, `filas_costo_laboral()`

> 14A dimensiona la **organización de la planta industrial** (más estructura y coordinación de la producción primaria). Sus FTE **no** son el FTE total de una empresa verticalmente integrada. Granjas propias, incubación, planta de alimento, reproductoras y rendering son **universos de RRHH distintos**, hoy **sin dimensionar**: aparecen como filas PENDIENTE (o FUTURO), nunca con FTE fabricados ni reutilizando los de 14A. **No hay salarios cargados**: `COSTO_LABORAL_TOTAL = PENDIENTE` en todos los escenarios.

## 1. Universos de RRHH (`UNIVERSO_RRHH`)

| Universo | Origen | Estado |
|---|---|---|
| `INDUSTRIAL_14A` | 14A: operación, soporte industrial (calidad, mantenimiento, limpieza, HyS, lavandería), logística interna | FTE dimensionados (costo PENDIENTE) |
| `ESTRUCTURA_14A` | 14A: administración, comercial, dirección | FTE dimensionados |
| `COORDINACION_PRIMARIA_14A` | 14A: coordinador, veterinario, planificación de crianza, técnicos de campo | FTE dimensionados (no son operarios de granja) |
| `TERCERO_INCLUIDO_EN_TARIFA` | 14A: personal del faenador (façon) y choferes con flete tercerizado | **Recurso físico de tercero**: horas visibles, costo `INCLUIDO_EN_TARIFA_FACON` / `INCLUIDO_EN_TARIFA_FLETE` |
| `TERCERO_INCLUIDO_EN_SERVICIO` | Captura, laboratorio externo, HyS externo | Se costea en el servicio (PP-CAPT, CAL-ANA-MICRO, ADM-HYS) |
| `RRHH_GRANJAS_PROPIAS_PENDIENTE` | — (03 no tiene modelo de dotación de granja) | **PENDIENTE** |
| `RRHH_INCUBACION_PENDIENTE` | — | **PENDIENTE** |
| `RRHH_PLANTA_ALIMENTO_PENDIENTE` | — | **PENDIENTE** |
| `RRHH_INDUSTRIAL_NO_DIMENSIONADO_14A` | Operación de efluentes, tratamiento básico de subproductos | **PENDIENTE** |
| `RRHH_LOGISTICA_NO_DIMENSIONADO_14A` | Choferes de pollitos, huevos, alimento, grano y subproductos con flota propia | **PENDIENTE** |
| `RRHH_REPRODUCTORAS_FUTURO`, `RRHH_RENDERING_FUTURO` | — | **FUTURO** (estructura sin dotación) |

## 2. FTE por escenario (columnas del resumen y filas de `modelo_costo_laboral.csv`)

| | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| **FTE_INDUSTRIAL_14A** — planta propia (C1–C3, CF) | 51,5 | 71,0 | 106,8 | 168,0 |
| …FTE_TOTAL_CONOCIDO (empresa) — C1 | 48,0 | 67,6 | 101,3 | 159,6 |
| …FTE_TERCEROS_INCLUIDOS_EN_TARIFAS — C1 (choferes) | 3,4 | 3,4 | 5,5 | 8,4 |
| **FTE_INDUSTRIAL_14A** — C0 asset-light | 35,8 | 49,6 | 77,4 | 124,9 |
| …FTE_TOTAL_CONOCIDO (empresa) — C0 | 10,0 | 17,5 | 24,5 | 35,5 |
| …FTE_TERCEROS_INCLUIDOS_EN_TARIFAS — C0 (faenador + choferes) | 25,8 | 32,1 | 52,9 | 89,4 |

| Configuración | FTE_ADICIONAL_PENDIENTE |
|---|---|
| C0 | ninguno identificado |
| C1 | operación de efluentes |
| C2 | granjas propias, operación de efluentes |
| C3, CF | granjas propias, incubación, planta de alimento, operación de efluentes, tratamiento de subproductos (CF: + reproductoras y rendering como FUTURO) |

C2 y C3 tienen flota propia de aves vivas y producto: sus choferes son internos (FTE_TERCEROS = 0). **El FTE de C3 no es mayor que el de C1** porque los universos upstream no están dimensionados: no debe leerse como dotación de una empresa integrada (test X05).

## 3. Costo empresa por FTE — componentes separados

`remuneración mensual = salario base × (1 + adicionales % + vacaciones %)`
`remuneración anual = remuneración mensual × (12 + SAC)`
`costo empresa/FTE·año = remuneración anual × (1 + cargas % + ART %) + beneficios × 12 + uniforme/EPP + capacitación + otros`

| Componente | Dónde | Estado |
|---|---|---|
| Remuneración base mensual | base `LAB-<CAT>-SAL` | PENDIENTE (DPV-148) |
| Adicionales (presentismo, antigüedad, nocturnidad) | `LAB-<CAT>-ADI` (%) | PENDIENTE |
| Vacaciones (plus vacacional) | `LAB-<CAT>-VAC` (%) | PENDIENTE (convenio, DPV-148) |
| **SAC / aguinaldo** | **regla** en `reglas_laborales_opex.csv` (1 sueldo adicional/año) | `REGLA_LABORAL_PENDIENTE_VERIFICACION` — **no es precio ni E4** |
| Cargas / contribuciones | `LAB-<CAT>-CAR` (%) | PENDIENTE |
| ART | `LAB-<CAT>-ART` (%) | PENDIENTE |
| Beneficios | `LAB-<CAT>-BEN` (USD/mes) | PENDIENTE |
| Horas extra | `LAB-<CAT>-HEX` (USD/hora) + regla de recargo | **No automáticas**: la brecha de jornada de 14A es informativa; solo si se organizan horas extra (DEC-069) |
| Uniforme y EPP, capacitación, otros | `LAB-<CAT>-EPP/CAP/OTR` (USD/FTE·año) | PENDIENTE |

Corrección v1.1: la v1.0 contaba "13 meses remunerados" como un **concepto con precio E4**. Se retiró de la base: el SAC es una regla laboral con fuente normativa a verificar (DPV-148), sin nivel de evidencia de precio. Los conceptos con precio pasaron de 3 a **2** (test X07, X08).

Categorías: CONV_DIR, CONV_SOP, FC_SUP, FC_PRO, FC_ADM, DIR, CHOF; tercerizados LAB-TER-LIMP/MANT/LOG/OTR (USD/hora). Si falta un componente, la categoría queda PENDIENTE (no se costea parcialmente).

## 4. Unidades y advertencias

FTE (horas operativas ÷ 8 h) ≠ headcount de nómina (PENDIENTE: factor de cobertura no validado). El costeo por FTE es **provisional**: subestima si el costo empresa no incluye la cobertura de francos y licencias. Naturaleza (SUP-179): producción, activos y estrategia → semifijo; casi fijo → fijo; horas tercerizadas → variable.
