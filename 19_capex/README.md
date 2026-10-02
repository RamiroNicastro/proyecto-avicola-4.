# 19 — CAPEX

**Alcance:** inversión inicial y por etapa, desagregada por eslabón (terreno, obra civil, maquinaria, frío, utilities, efluentes, logística, incubación, alimento, granjas, indirectos, preoperativos, contingencia), con clasificación de evidencia de cada precio (E1 cotización … E5 supuesto; PENDIENTE). El **capital de trabajo inicial se calcula aparte** (`20_opex` / `21_modelo_financiero`): no se mezcla con el CAPEX (cambio de alcance de la sesión 16, ver [`actualizaciones_gestion_16.md`](actualizaciones_gestion_16.md) §6).

**Regla:** no asumir que USD 2 millones alcanza; la suficiencia es un resultado. Vacío = desconocido; 0 = costo cero real.

**Estado (2026-10-02, sesión 16):** motor v1.1 construido, auditado en procedencia de drivers y probado (77 tests, 9 mutaciones detectadas). **Sin CAPEX total publicable**: 167 de 175 conceptos sin precio; cobertura por conceptos 0–2,3 %. Ver [`conclusiones_capex.md`](conclusiones_capex.md).

## Archivos

| Archivo | Contenido |
|---|---|
| [`modelo_capex.py`](modelo_capex.py) | Motor: drivers → BOQ → costeo → resumen → expansión → RFQ; tests y mutaciones |
| [`base_costos_capex.csv`](base_costos_capex.csv) | **Input**: 175 conceptos con precio, moneda, Incoterm, inclusiones y evidencia (editable sin tocar el código) |
| [`capas_importacion_capex.csv`](capas_importacion_capex.csv) | **Input** (vacío): capas C02–C19 por concepto importado |
| [`boq_capex.csv`](boq_capex.csv) | Salida: registro de activos de 33 escenarios (5.485 filas) |
| [`escenarios_capex.csv`](escenarios_capex.csv) | Salida: resumen por escenario y bloque (528 filas) |
| [`expansion_capex.csv`](expansion_capex.csv) | Salida: trayectorias 20.000 directo / 5.000 → 20.000 / 5.000 → 10.000 → 20.000 / 10.000 → 20.000 (2.508 filas) |
| [`matriz_rfq_capex.csv`](matriz_rfq_capex.csv) | Salida: 13 cotizaciones necesarias |
| [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv) | Salida: procedencia de cada driver físico (valor, unidad, archivo y variable de origen, escenario, tipo, evidencia) |
| [`fuentes_16.csv`](fuentes_16.csv) | Fuentes provisionales FTE-16-001…007 (todas `[PVDP]`) |
| [`metodologia_capex.md`](metodologia_capex.md) | Método, fórmulas, separaciones, reglas contra el doble conteo |
| [`estructura_capex.md`](estructura_capex.md) | Bloques, conceptos, columnas, qué entra y qué no |
| [`arquitecturas_inversion.md`](arquitecturas_inversion.md) | Opciones por eslabón y configuraciones C0–C3/CF |
| [`capex_por_escala.md`](capex_por_escala.md) | Resultados por escenario y cantidades físicas por escala |
| [`obra_civil_capex.md`](obra_civil_capex.md) | Obra paramétrica por categoría y terreno |
| [`maquinaria_capex.md`](maquinaria_capex.md) | Paquetes RFQ, equipos hijos, equipo vs instalado, importados |
| [`utilities_capex.md`](utilities_capex.md) | Frío, agua, efluentes, electricidad, térmico, aire, servicios generales |
| [`upstream_capex.md`](upstream_capex.md) | Incubación, planta de alimento, granjas, reproductoras |
| [`logistica_capex.md`](logistica_capex.md) | Flota por flujo |
| [`expansion_capex.md`](expansion_capex.md) | CAPEX inicial / de expansión / acumulado; activos reutilizables |
| [`evidencia_costos.md`](evidencia_costos.md) | Niveles E1–E5 y estado de la base |
| [`plan_cotizaciones.md`](plan_cotizaciones.md) | Qué cotizar, especificación mínima y cómo cargar una cotización |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin tecnicismos |
| [`conclusiones_capex.md`](conclusiones_capex.md) | Qué números usar y cuáles no |
| [`actualizaciones_gestion_16.md`](actualizaciones_gestion_16.md) | SUP/DPV/DEC/FTE provisionales para la reconciliación |

## Uso

```bash
python3 19_capex/modelo_capex.py                 # tests + regenera los 5 CSV de salida
python3 19_capex/modelo_capex.py --solo-tests
python3 19_capex/modelo_capex.py --mutaciones
python3 19_capex/modelo_capex.py --tablas
python3 19_capex/modelo_capex.py --escenario --config C3 --aves-dia 7500 --terreno compra_reserva
python3 19_capex/modelo_capex.py --escenario --config C1 --costos mi_base.csv --sensibilidad
```

Requiere Python 3 estándar (sin paquetes externos) y los modelos de `09_layout_obra_civil`, `11_agua_efluentes`, `13_logistica`, `14_alimento_balanceado`, `05_proceso_industrial`, `23_plan_expansion` y `03_produccion_primaria`. Separador decimal de los CSV: punto. Moneda del modelo: USD; `FECHA_BASE_CAPEX` = 2026-10-01 (editable con `--fecha-base`).

**Relacionado:** `08_maquinaria`, `09_layout_obra_civil`, `11_agua_efluentes`, `12_energia_frio`, `13_logistica`, `14_alimento_balanceado`, `15_incubacion`, `20_opex`, `21_modelo_financiero`, `23_plan_expansion`.
