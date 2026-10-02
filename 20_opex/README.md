# 20 — OPEX y capital de trabajo

**Alcance:** costos operativos por escala, arquitectura e integración (alimento, pollito BB / huevo fértil, producción primaria, faena, empaque, utilities, frío, efluentes, subproductos, logística, mantenimiento, calidad, administración, comercial, seguros, costo laboral) y **capital de trabajo operativo** (inventarios propios, cuentas por cobrar y por pagar, caja). Cada costo se clasifica por naturaleza (variable / fijo / semifijo / semivariable), centro de costo, tipo y aportante. Los impuestos operativos (ingresos brutos, tasas sobre ventas) y el IVA se tratan en `21_modelo_financiero`.

**Regla:** costo = driver físico consumido × precio de una base externa. Vacío = desconocido, nunca 0. Sin cobertura completa no hay OPEX total, costo por ave ni capital de trabajo. **No** se calculan ingresos, EBITDA, VAN, TIR, payback, depreciación, impuestos ni IVA definitivo.

**Estado (2026-10-02, sesión 17):** motor v1.0 construido (62 tests, 11/11 mutaciones). **Sin OPEX total ni capital de trabajo**: 3 de 323 conceptos con precio, todos E4 `[PVDP]`; cobertura por conceptos 0,5–2,7 %. Ver [`conclusiones_opex.md`](conclusiones_opex.md).

## Archivos

| Archivo | Contenido |
|---|---|
| [`modelo_opex.py`](modelo_opex.py) | Motor: drivers → registro → costeo → resumen → capital de trabajo → ramp-up; tests y mutaciones |
| [`base_costos_opex.csv`](base_costos_opex.csv) | **Input**: 323 conceptos con unidad, precio, moneda, TC, fecha, evidencia, naturaleza, centro, tipo y grupo de proveedor (editable sin tocar el código) |
| [`registro_costos_operativos.csv`](registro_costos_operativos.csv) | Salida: una fila por concepto y escenario (29 escenarios, 4.401 filas) |
| [`escenarios_opex.csv`](escenarios_opex.csv) | Salida: resumen por escenario y módulo (montos por evidencia, conteos, coberturas, total, KPI unitarios, CT) |
| [`mapa_drivers_opex.csv`](mapa_drivers_opex.csv) | Salida: procedencia de cada driver (valor bajo/medio/alto, unidad, archivo y variable de origen, tipo, evidencia) |
| [`modelo_costo_laboral.csv`](modelo_costo_laboral.csv) | Salida: puesto × modalidad × FTE/horas × componentes del costo empresa (desde 14A; salarios vacíos) |
| [`capital_trabajo_opex.csv`](capital_trabajo_opex.csv) | Salida: inventarios (propietario, ubicación, si entra), CxC, CxP por proveedor, caja y CTO por escenario |
| [`matriz_validacion_opex.csv`](matriz_validacion_opex.csv) | Salida: 20 ítems a cotizar / validar con driver, magnitud física, actor, prioridad e impacto |
| [`fuentes_17.csv`](fuentes_17.csv) | Fuentes provisionales FTE-17-001…008 (todas `[PVDP]`) |
| [`metodologia_opex.md`](metodologia_opex.md) | Método, fórmulas, procedencia, reglas contra el doble conteo |
| [`estructura_opex.md`](estructura_opex.md) | Módulos, clasificación, columnas, administración, comercial y seguros |
| [`costos_alimento.md`](costos_alimento.md) | Compra / façon B1 y B2 / planta propia |
| [`costos_incubacion.md`](costos_incubacion.md) | Pollito comprado, incubación propia, reproductoras (futuro) |
| [`costos_produccion_primaria.md`](costos_produccion_primaria.md) | Granja integrada (aportes empresa vs integrado) y propia |
| [`costos_faena.md`](costos_faena.md) | Façon vs planta propia, empaque, subproductos |
| [`costos_utilities.md`](costos_utilities.md) | Electricidad, térmico, agua, frío, efluentes |
| [`costos_rrhh.md`](costos_rrhh.md) | Costo laboral desde 14A |
| [`costos_logistica.md`](costos_logistica.md) | Flota propia vs tercerizada por flujo |
| [`costos_mantenimiento.md`](costos_mantenimiento.md) | Métodos alternativos por área |
| [`costos_calidad.md`](costos_calidad.md) | Calidad, laboratorio, SENASA, halal opcional |
| [`capital_trabajo.md`](capital_trabajo.md) | Stock propio ≠ stock de la cadena; CxC, CxP, caja |
| [`ramp_up.md`](ramp_up.md) | Utilización por etapa sin curva definitiva |
| [`evidencia_costos_opex.md`](evidencia_costos_opex.md) | Niveles E1–E5 y estado de la base |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin tecnicismos |
| [`conclusiones_opex.md`](conclusiones_opex.md) | Qué números usar y cuáles no |
| [`actualizaciones_gestion_17.md`](actualizaciones_gestion_17.md) | SUP/DPV/DEC/FTE provisionales para la reconciliación |

## Uso

```bash
python3 20_opex/modelo_opex.py                     # tests + regenera los 6 CSV de salida
python3 20_opex/modelo_opex.py --solo-tests
python3 20_opex/modelo_opex.py --mutaciones
python3 20_opex/modelo_opex.py --escenario --config C3 --aves-dia 10000
python3 20_opex/modelo_opex.py --escenario --config C1 --aves-dia 7500 --costos mi_base.csv
```

Desde Python: `correr(config_opex("C1", aves_dia=10000, combustible_termico="gas_natural", fuente_agua="red", ...))`; otros parámetros: `alimento_facon_mp`, `mantenimiento_metodo`, `modelo_tarifa_flete`, `base_pago_integrado`, `aportes_integracion`, `composicion_alimento`, `ventas_anuales_usd`, `dias_cobro`, `dias_pago`, `dias_caja_operativa`. Ramp-up: `aplicar_utilizacion(filas, u)`.

Requiere Python 3 estándar (sin paquetes externos) y los modelos de `19_capex`, `18_recursos_humanos`, `14_alimento_balanceado`, `13_logistica`, `11_agua_efluentes`, `09_layout_obra_civil`, `05_proceso_industrial`, `04_balance_masa`, `03_produccion_primaria` y `23_plan_expansion` (solo lectura; no se modifican). Separador decimal de los CSV: punto. Moneda: USD; `FECHA_BASE_OPEX` = 2026-10-01 (`--fecha-base`).

**Relacionado:** `03_produccion_primaria`, `04_balance_masa`, `11_agua_efluentes`, `12_energia_frio`, `13_logistica`, `14_alimento_balanceado`, `15_incubacion`, `18_recursos_humanos`, `19_capex`, `21_modelo_financiero`.
