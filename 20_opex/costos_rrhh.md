# Costo laboral — puesto × modalidad × horas/FTE × costo empresa

**Fecha:** 2026-10-02 · Drivers: 14A (`modelo_rrhh.calcular`) · Salida: [`modelo_costo_laboral.csv`](modelo_costo_laboral.csv) (1.238 filas, una por puesto y modalidad en cada escenario) · Implementación: `lineas_laborales()` y `filas_costo_laboral()`

> **No** se usa "X personas × salario". El costo se construye desde cada puesto de 14A, su modalidad (interno / tercerizado / servicio externo), su FTE u horas contratadas y el costo empresa de su categoría. **No hay ningún salario cargado** (DPV-148): `COSTO_LABORAL_TOTAL = PENDIENTE` en todos los escenarios.

## 1. Unidades (no se mezclan)

| Unidad | Uso en OPEX |
|---|---|
| FTE interno (14A) | Base del costeo **provisional** de puestos internos |
| Headcount de nómina | **PENDIENTE** (factor de cobertura no validado); no se deriva del FTE |
| Horas-persona/día y horas/año | Informativas por puesto |
| Horas contratadas (tercerizado) | Base del costeo de servicios tercerizados (tarifa horaria) |
| Simultáneos / puestos por turno | Informativos (layout, 14A) |
| Brecha de jornada | Horas-persona a organizar (turnos, relevos, personal adicional u horas extra): **INFORMATIVA**, no horas extra automáticas (DPV-146) |

Advertencia del costeo por FTE: el FTE mide horas operativas; los francos, vacaciones y licencias hacen que el headcount sea mayor. Hasta validar el factor de cobertura, el costo por FTE debe entenderse como **costo por FTE efectivo** (incluir la cobertura en el costo empresa) o subestima el costo.

## 2. Estructura del costo empresa por FTE (por categoría)

`costo empresa/FTE·año = salario básico × meses remunerados × (1 + adicionales %) × (1 + cargas % + ART %) + beneficios × 12 + uniforme/EPP + capacitación`

| Componente | ID en la base (`LAB-<CAT>-*`) | Estado |
|---|---|---|
| Salario básico mensual | SAL | PENDIENTE |
| Meses remunerados (12 + SAC) | LAB-PARAM-MESES = 13 | E4 `[PVDP]` (Ley 20.744 arts. 121–122, no leída en original) |
| Adicionales (presentismo, antigüedad, nocturnidad) | ADI (%) | PENDIENTE |
| Cargas sociales | CAR (%) | PENDIENTE |
| ART | ART (%) | PENDIENTE |
| Beneficios (comedor, transporte) | BEN (USD/mes) | PENDIENTE |
| Uniforme y EPP | EPP (USD/FTE·año) | PENDIENTE |
| Capacitación | CAP (USD/FTE·año) | PENDIENTE |
| Horas extra | — | **No automáticas** (brecha informada) |

Categorías: CONV_DIR (directos de convenio), CONV_SOP (soporte de convenio: limpieza, mantenimiento, depósito, QC, laboratorio), FC_SUP (supervisión), FC_PRO (profesionales y jefes), FC_ADM (administración y ventas), DIR (dirección), CHOF (choferes, CCT 40/89 [PVDP]). Tercerizados: LAB-TER-LIMP / MANT / LOG / OTR (USD/hora). Si falta un componente, el costo de la categoría es PENDIENTE (no se costea parcialmente).

## 3. Dotación por escala (14A, FTE totales internos + tercerizados)

| Configuración | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| C1–C3, CF (planta propia) | 51,5 | 71,0 | 106,8 | 168,0 |
| C0 (asset-light) | 35,8 | 49,6 | 77,4 | 124,9 |

En C0, 14A conserva las horas del personal del faenador como tercerizadas (la función no desaparece): esas horas quedan **incluidas en la tarifa de façon** (no se cobran dos veces; test A04b). Lo mismo con los choferes cuando la flota es tercerizada (test C09).

**14A no dimensiona** personal de granjas propias, incubadora, planta de alimento, operación de efluentes, tratamiento básico de subproductos ni choferes de los flujos de pollitos, alimento, grano y subproductos con flota propia: esas funciones aparecen como filas **SIN_CANTIDAD** (test L03). C3 tiene así los mismos FTE de 14A que C1 más esas funciones pendientes; el número de C3 **no** debe leerse como la dotación de una empresa integrada.

## 4. Naturaleza del costo laboral (SUP-17-07)

Producción, activos y estrategia → **semifijo** (cambia por escalones de cuadrillas y turnos, no por ave); casi fijo → **fijo**; horas tercerizadas → **variable**. En ramp-up, el personal de línea no baja proporcionalmente al volumen.
