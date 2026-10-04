# Arquitectura del modelo financiero

**Fecha:** 2026-10-04 · Código: [`modelo_financiero.py`](modelo_financiero.py) · Método: [`metodologia_financiera.md`](metodologia_financiera.md)

## 1. Capas

```
┌────────────────────────── FUENTES (no se modifican; se importan) ──────────────────────────┐
│ 00_gestion_proyecto/mapa_arquitecturas_economicas.csv  → qué configuraciones se evalúan     │
│ 19_capex/modelo_capex.py   preset(), correr(), expansion(), BOQ (vida útil, residual)       │
│ 20_opex/modelo_opex.py     config_opex(), correr(): registro por concepto, CT por propiedad │
│ 04_balance_masa + 23_plan_expansion/modelo_escala.py  kg por ave (ITEMS), rutas exclusivas  │
│ 02_clientes_demanda/escenarios_demanda.csv  escenarios comerciales de PRUEBA (SUPUESTO)     │
└──────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                               │ adaptadores (§3)
┌──────────────────────────── INPUTS DEL FINANCIERO ─────────────────────────────────────────┐
│ inputs_financieros.csv (EVIDENCIA + plantillas) · base_precios_venta.csv · curvas_rampup.csv │
│ JSON del usuario (solo MODO ESCENARIO; plantilla_escenario_usuario.json)                    │
└──────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                               │ construir_entrada() → resolver() + Traza
┌──────────────────────────── MOTOR (puro, mensual) ─────────────────────────────────────────┐
│ validar_entrada() → disponibilidad() → flags_calculo() → simular() → agregar()              │
│ cronograma_deuda() · van() · tir() · mirr() · payback() · break_even_anual()                │
└──────────────────────────────────────────────┬─────────────────────────────────────────────┘
                                               │ resultados() + publicabilidad()
┌──────────────────────────── SALIDAS ───────────────────────────────────────────────────────┐
│ escenarios_financieros · estado_resultados · flujo_caja_proyecto · flujo_accionista ·        │
│ capital_trabajo_financiero · deuda · break_even · completitud_financiera ·                  │
│ mapa_drivers_financieros · casos_prueba_motor                                               │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

El **motor** no lee archivos: recibe una entrada `P` (dict con valores ya resueltos; `None` = PENDIENTE) y devuelve series. Por eso los tests usan **casos artificiales controlados** (`caso_prueba()`) y los **adaptadores** se prueban aparte contra el proyecto.

## 2. Entrada del motor (`entrada_vacia()`, `etapa_vacia()`)

| Grupo | Claves | Bloque de disponibilidad |
|---|---|---|
| Tiempo | `horizonte_anios`, `meses_detalle`, `fecha_inicio`, `meses_preoperacion/construccion/commissioning` | TIEMPO |
| Moneda | `modelo_monetario`, `inflacion_anual`, `base_tasa` | (validación) |
| Etapas | por etapa: `escala_aves_dia`, `dias_operativos_anio`, `entrada` (INICIAL / FECHA / CONDICION), `capex_usd`, `curva_desembolso`, `rampup`, `opex_rubros`, `activos` | PRODUCCION, RAMPUP, CAPEX, OPEX, DEPRECIACION, REPOSICION |
| Producto | `productos` (kg/ave por producto), `validacion_rendimientos`, `meta_productos` | PRODUCCION |
| Comercial | `demanda` (líneas), `categorias_demanda_usadas`, `alfa_negociada`, `precios`, `canales`, `inventario_max_meses` | DEMANDA, PRECIOS, CANALES |
| CT | `inventarios` (propiedad, días, base), `dias_caja_operativa`; `dias_pago` en rubros; `dias_cobro` en canales | CT |
| Fiscal | `impuestos` (IIBB, tasas, otros, ganancias, quebrantos), `iva` | IMPUESTOS_INGRESOS, GANANCIAS, IVA |
| Financiero | `financiamiento` (aportes, deudas, dividendos), `tasa_descuento`, `tasa_descuento_accionista`, `tasa_reinversion`, `valor_terminal` | FINANCIAMIENTO, DESCUENTO, VALOR_TERMINAL |
| Stress | `stress` (solo escenario) | (validación) |

`flags_calculo()` encadena los bloques: físico → bruto → neto → OPEX → EBITDA → CT → FCFF pre-tax → FCFF after-tax → FCFE. Una serie cuyo grupo no está completo se **anula** (`None`) al final de `simular()`: un faltante nunca llega a la salida como 0.

## 3. Adaptadores (consumo sin copiar fórmulas)

| Función | Consume | Devuelve | Regla |
|---|---|---|---|
| `mapa_arquitecturas()` | mapa de arquitecturas | 24 configuraciones (5 bases + 19 variantes); las M0–MF de 14B se excluyen (no son configuraciones económicas) | No redefine nada (test E09) |
| `configs()` | `escenarios_referencia()` de CAPEX y `escenarios_opex()` de OPEX | (config CAPEX, config OPEX) con la **misma arquitectura**; una variante de un solo módulo corre el otro con los mismos inputs (T18-16) | E09 |
| `capex_desde_modulo()` | `mcx.correr()` → `TOTAL_PRELIMINAR_USD`, `CAPEX_E4/E5_USD` | CAPEX total solo si existe y es E1–E3 | Monto E4 parcial → solo traza (E06, E12) |
| `activos_desde_boq()` | BOQ: `VIDA_UTIL_ANIOS`, `VALOR_RESIDUAL`, `COSTO_REEMPLAZO` | Activos para depreciación y reposición | Hoy vacíos (DPV-167) |
| `opex_desde_modulo()` | `mo.correr()` → registro por concepto (`NATURALEZA`, `PCT_VARIABLE`, `GRUPO_PROVEEDOR`) | Rubros por concepto | Solo si OPEX publica total y la arquitectura es costeable |
| `propiedad_inventarios()` | `capital_trabajo()` de OPEX (`ENTRA_EN_CT`) | Propiedad por categoría de inventario | Stock de terceros no entra |
| `capex_trayectoria()` | `mcx.expansion()` con su lógica de acciones por etiqueta | CAPEX por etapa de una trayectoria | Reemplaza `TRAYECTORIAS` del módulo solo durante la llamada y lo restaura (test N20) |
| `productos_balance()` | `mb.balance()` + `me.ITEMS` | kg comerciales por ave y producto | Reproduce `me.kg_por_ave()` (test F09); rutas exclusivas |
| `leer_precios()` | `base_precios_venta.csv` | Precios E1–E3; referencias E4 aparte | Precio vacío ≠ 0 (test E10) |
| `construir_entrada()` | todo lo anterior + inputs + JSON | Entrada `P` + `Traza` | Jerarquía de `resolver()` |

## 4. Corridas de referencia (`corridas_referencia()`)

| Modo | Corridas | Contenido |
|---|---|---|
| EVIDENCIA | 42 | C0, C1, C2, C3, CF × 2.500 / 5.000 / 10.000 / 20.000 (20); las 19 variantes del mapa a 10.000; C1 en tres trayectorias de expansión |
| ESCENARIO | 19 | Plantillas CONSERVADOR / BASE / EXPANSIVO × 5 configuraciones a 10.000 (15); plantilla BASE × 4 trayectorias de C1 |

Las plantillas **no** tienen precios, mix, cronograma, impuestos ni financiamiento (no se rellenan arbitrariamente): sirven para mostrar qué falta. Un escenario completo lo arma el usuario con el JSON ([`guia_ramiro.md`](guia_ramiro.md) §17).

## 5. Comandos

```
python3 21_modelo_financiero/modelo_financiero.py                 # 56 tests + 10 CSV de salida
python3 21_modelo_financiero/modelo_financiero.py --solo-tests
python3 21_modelo_financiero/modelo_financiero.py --mutaciones    # 20 errores sembrados, todos detectados
python3 21_modelo_financiero/modelo_financiero.py --escenario mi.json --salida carpeta/
```

El script se detiene con código 1 si falla cualquier test. No escribe en `19_capex/`, `20_opex/`, `00_gestion_proyecto/` ni `25_fuentes/`.

## 6. Diccionario de salidas

| Archivo | Una fila por | Columnas clave |
|---|---|---|
| [`escenarios_financieros.csv`](escenarios_financieros.csv) | corrida | capital requerido, ingresos, EBITDA, utilizaciones, break-even, VAN, TIR, payback, flujo del accionista, DSCR, 10 banderas `PUBLICABLE_*` con motivo, `FALTANTES` |
| [`estado_resultados.csv`](estado_resultados.csv) | corrida × período | capacidad, aves, utilizaciones, kg, venta bruta por categoría, deducciones, ingreso neto, OPEX por naturaleza, costos comerciales, impuestos, EBITDA, depreciación, EBIT, intereses, impuestos |
| [`flujo_caja_proyecto.csv`](flujo_caja_proyecto.csv) | corrida × período | EBITDA, depreciación, EBIT, impuesto operativo, CAPEX inicial/expansión/reposición, ΔCT, IVA, valor terminal, FCFF pre y after-tax |
| [`flujo_accionista.csv`](flujo_accionista.csv) | corrida × período | deuda recibida, intereses, comisiones, amortización, FCFE, aportes, dividendos, caja, CFADS, servicio de deuda |
| [`capital_trabajo_financiero.csv`](capital_trabajo_financiero.csv) | corrida × período | inventarios por categoría, CxC, caja operativa, CxP, CT, ΔCT, saldo IVA |
| [`deuda.csv`](deuda.csv) | corrida × período | saldo inicial, altas, intereses, amortización, comisiones, saldo final |
| [`break_even.csv`](break_even.csv) | corrida × base (EBITDA / EBIT) | margen de contribución, fijos, q*, u*, precio* |
| [`completitud_financiera.csv`](completitud_financiera.csv) | corrida × bloque | estado COMPLETO / PARCIAL / PENDIENTE / NO_APLICA, qué falta, registros |
| [`mapa_drivers_financieros.csv`](mapa_drivers_financieros.csv) | corrida × variable | traza completa |
| [`casos_prueba_motor.csv`](casos_prueba_motor.csv) | caso artificial | resultados de los casos de prueba (no son escenarios del proyecto) |

Sin línea de tiempo (hoy, todas las corridas del proyecto), los archivos periódicos tienen **una fila por corrida** con `FASE = SIN_LINEA_DE_TIEMPO` y el motivo.
