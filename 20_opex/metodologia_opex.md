# Metodología del motor OPEX + capital de trabajo

**Versión:** 1.0 · **Fecha:** 2026-10-02 · **Modelo:** [`modelo_opex.py`](modelo_opex.py) · **Sesión:** 17

> Pregunta que responde: **¿cuánto cuesta operar cada configuración del proyecto y cuánto capital queda inmovilizado en la operación?**
> El motor **no** elige escala, arquitectura, make-or-buy ni proveedor, y **no** calcula ingresos, EBITDA, VAN, TIR, payback, depreciación, impuesto a las ganancias ni IVA definitivo (van a `21_modelo_financiero`).

## 1. Principio: separar cantidades de precios

```
DRIVERS FÍSICOS consumidos de 03 · 04 · 05 · 09C · 12B · 14A · 14B · 19_capex     → cantidad anual por concepto
BASE DE COSTOS externa (base_costos_opex.csv)                                     → precio, moneda, TC, fecha, evidencia
                                    ↓
REGISTRO DE COSTOS OPERATIVOS: una fila por concepto y arquitectura (registro_costos_operativos.csv)
                                    ↓
COSTEO: solo si hay cantidad Y precio con TC; vacío ≠ 0
                                    ↓
RESUMEN por módulo: con precio / sin precio / sin cantidad / aportante pendiente, montos separados por evidencia
                                    ↓
CAPITAL DE TRABAJO: inventarios PROPIOS + CxC + caja − CxP; cualquier faltante → PENDIENTE
```

- Las **cantidades** salen de los modelos aprobados; OPEX **llama sus funciones** y no las recalcula (tests D01–D10).
- Los **precios** viven en el CSV de la base. Cargar una cotización = editar el CSV; el código no se toca.
- Un precio sin cantidad o una cantidad sin precio quedan **PENDIENTES**. Nunca se reemplazan por cero (tests C01, C01b; mutación M01).

## 2. Fuentes de las cantidades

| Driver | Origen (función) | Uso |
|---|---|---|
| Aves faenadas / cargadas, pollitos alojados, kg vivo, mortalidad, agua de bebida, ciclos, m² de galpón, inventario de aves | 03 vía 14B (`mup.produccion`) | Façon, captura, pago al integrado, sanidad, granjas propias, activo biológico |
| Pollitos a recibir, alimento t/año y composición ilustrativa de materias primas, incubación (huevos/pollito, cargas, WIP), inventario de alimento por categoría y **propietario** | 14B (`pollitos`, `alimento`, `incubacion`, `inventario_alimento`) | Pollito, alimento, materias primas, huevo fértil, capital de trabajo |
| kWh/año (incluye frío, aire, bombeo, efluentes aerobios), agua captada, efluente, energía térmica y equivalentes de combustible, subproductos segregables | 09C vía CAPEX (`D["util"]`, nivel medio; bajo/alto en el mapa) | Utilities, efluentes, subproductos |
| Decomisos | 04 (`balance()`, filas `decomiso*`) | Retiro de decomisos |
| kg comestible a empaque por ave | 05 (`kg_ave_config`) | Empaque |
| Viajes, km y t por flujo; stock medio de producto | 12B (`aves_vivas`, `producto`, `insumos`, `subproductos`, `inventario`) | Logística, capital de trabajo |
| Vehículos de flota propia por flujo | CAPEX 16 (que consume 12B) | Patentes, seguros de flota |
| Puestos, FTE interno, horas contratadas, modalidad, brecha de jornada | 14A (`modelo_rrhh.calcular`) | Costo laboral |
| Activos costeables y CAPEX por bloque | CAPEX 16 (`correr`) | Base del mantenimiento (por activo o % CAPEX) |

Cada driver queda en [`mapa_drivers_opex.csv`](mapa_drivers_opex.csv) con valor (bajo/medio/alto cuando la fuente lo da), unidad, archivo y variable de origen, escenario fuente, tipo y evidencia.

| Tipo de procedencia | Significado |
|---|---|
| `DIRECTO` | Salida del módulo fuente para un escenario publicado en su CSV (tests de reproducción) |
| `CALCULO_MODELO_FUENTE` | La misma función del módulo fuente con entradas que su CSV no publica (perfil P2, escala intermedia, laboratorio propio, capacidades de camión). No es interpolación |
| `CONSUMIDO_CAPEX` | Valor del motor CAPEX (flota, días operativos, fracción de granjas propias) |
| `DERIVADO_OPEX` | Operación declarada de OPEX sobre salidas fuente (anualización, suma de granos, huevos = huevos/pollito × pollitos) |
| `SUPUESTO_OPEX` | Parámetro propio de OPEX (composición de alimento si el usuario la carga) |
| `PENDIENTE` | El módulo fuente no lo dimensiona: el concepto queda SIN_CANTIDAD |

**Anualización** (DERIVADO_OPEX): drivers diarios × días operativos (250/300, SUP-025); drivers semanales de producto y subproductos × semanas operativas (días ÷ días/semana); viajes y km de alimento × (t/año ÷ t de la semana plena), porque las granjas consumen todo el año calendario. Los huevos se anualizan con huevos/pollito × pollitos/año (14B publica `huevos_recibidos_anio` a ritmo pleno × 52,14 semanas, que es una cota superior).

## 3. Fórmulas

| Concepto | Fórmula | Condición |
|---|---|---|
| Costo de un concepto | cantidad anual × precio USD | cantidad y precio existen; unidad del driver = unidad del precio (test S03) |
| Precio USD | precio original ÷ `TC_MONEDA_POR_USD` | moneda ≠ USD exige TC, tipo y fecha (test E05) |
| Mantenimiento % CAPEX | % × CAPEX con precio del área | base completa; si no → `BASE_SIN_PRECIO` (test A10) |
| Costo empresa por FTE | salario × meses × (1 + adicionales %) × (1 + cargas % + ART %) + beneficios × 12 + EPP + capacitación | todos los componentes cargados; si falta uno → PENDIENTE (test L02) |
| Costo laboral interno | FTE (14A) × costo empresa por FTE | **provisional por FTE**: headcount PENDIENTE |
| Costo tercerizado | horas contratadas (14A) × tarifa horaria | — |
| Ramp-up | variable × u + fijo | todos los conceptos con precio con reparto fijo/variable (tests R01–R03) |
| CTO | inventarios propios + CxC + caja − CxP | ningún componente PENDIENTE (tests K04, K05) |

## 4. Reglas contra el doble conteo

| Riesgo | Regla | Test |
|---|---|---|
| Frío con dos costos eléctricos | La energía de frío (proceso, congelación, cámaras) está **dentro** de `kwh_total_anio` de 09C: se registra como `INCLUIDO` en UT-ELE-KWH, sin costo | C06, M02 |
| Limpieza que vuelve a cobrar agua y energía | Agua y calor de limpieza ya están en 09C: fila `INCLUIDO`; FAE-QUIM son solo químicos | C07, M08 |
| Bombeo y efluentes aerobios | Incluidos en kWh de 09C | C06 |
| Choferes tercerizados + flete | Las horas de choferes de 14A con flota tercerizada quedan visibles pero `INCLUIDO` en la tarifa del flete | C09, M10 |
| Personal del faenador + tarifa de façon | En façon, 14A conserva las horas de faena como tercerizadas: quedan `INCLUIDO` en FAE-FACON | A04b, M11 |
| Captura, laboratorio externo, HyS externo | El puesto de 14A remite al concepto de servicio (PP-CAPT, CAL-ANA-MICRO, ADM-HYS) | C10 |
| Mano de obra de mantenimiento | En costo laboral (14A); el módulo de mantenimiento costea materiales y servicios | — |
| Métodos de mantenimiento | Uno por corrida (% CAPEX, por activo, horas técnicas, contrato) | A10 |
| Modelos de tarifa de flete | Uno por flujo (viaje, km, unidad, contrato) | A11 |
| Composición de alimento | "Resto" agregado de 14B **o** aceite/núcleo/otros desagregados, nunca ambos | validación |
| Pago al integrado | Por ave **o** por kg vivo, nunca ambos | validación |
| Tercerizar | Reemplaza el costo interno pero conserva la función (horas visibles y costeadas por tarifa) | C08 |
| CAPEX en OPEX | Ningún concepto usa IDs de la base CAPEX; commissioning, herramientas iniciales e insumos iniciales ya están en CAPEX (PRE-*) | S06 |

## 5. Qué se publica

Por escenario y módulo ([`escenarios_opex.csv`](escenarios_opex.csv)):

- **Montos con precio separados por evidencia** (`OPEX_E1_E2_USD_ANIO`, `OPEX_E3`, `OPEX_E4`, `OPEX_E5`) y `CALIDAD_MONTO`. No existe una columna "OPEX conocido".
- **Conteos**: costeables, con precio, sin precio, sin cantidad, aportante pendiente; informativos de terceros, incluidos en otro concepto, futuros u opcionales.
- **Cobertura por conceptos** (con precio ÷ costeables) y **cobertura por valor** solo si todos los faltantes tienen magnitud (hoy: "NO CALCULABLE").
- **Total preliminar y costos unitarios** (USD/ave, USD/kg vivo, USD/kg producto, USD/día, USD/mes) **solo con cobertura completa**; si no, "NO DISPONIBLE (cobertura X %)" (tests E03, E04).
- Monto con precio partido en **variable / fijo / sin clasificar** (base del break-even posterior).
- `CAPITAL_TRABAJO` del escenario (hoy PENDIENTE en todos).

## 6. Qué no hace (y dónde irá)

| Tema | Dónde |
|---|---|
| Ingresos, precio del pollo, ingresos por subproductos, EBITDA, VAN, TIR, payback | `21_modelo_financiero` |
| Depreciación, impuesto a las ganancias, IVA (crédito y débito), ingresos brutos, percepciones | `21_modelo_financiero` |
| Indexación por inflación (USD o ARS) | `21_modelo_financiero` (campos `INDICE_ACTUALIZACION` y `FECHA_ACTUALIZACION` preparados) |
| Elección de escala, arquitectura, make-or-buy, combustible, fuente de agua, tarifa | Decisiones (DEC-17-##) y optimizador posterior |

## 7. Ejecución

Ver [`README.md`](README.md). Los tests (62) y las mutaciones (11) están en el mismo script; si un test falla, no se escriben salidas.
