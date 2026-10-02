# 14 — Alimento balanceado

**Alcance:** requerimientos de alimento por etapa, formulación de referencia, insumos (maíz, harina de soja, núcleos), precios y disponibilidad regional; alternativa planta propia vs. compra a terceros. Desde la sesión 14B aloja también el **modelo físico del upstream** (pollitos, incubación, alimento, silos, logística de insumos), que comparte con [`../15_incubacion/`](../15_incubacion/README.md).

**Relacionado:** `03_produccion_primaria`, `04_balance_masa`, `13_logistica`, `15_incubacion`, `20_opex`, `23_plan_expansion`.

**Reconciliación (2026-10-02):** los IDs provisionales de esta carpeta se reemplazaron por los definitivos de los registros centrales (mapa en [`../00_gestion_proyecto/reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2); ninguna decisión se cerró y la lógica del modelo no cambió.

## Contenido (v1.1, 2026-10-01; sesión 14B con auditoría de sincronización e inventarios)

| Archivo | Contenido |
|---|---|
| [`conclusiones_alimento.md`](conclusiones_alimento.md) | **Síntesis**: hallazgos, escenarios de comparación (benchmark ≠ preferencia), arquitecturas de referencia, faltantes, tests |
| [`integracion_upstream.md`](integracion_upstream.md) | Demanda de pollitos por escala; marco *make or buy* (pollito, alimento, granjas) con 9 criterios; arquitecturas de referencia (sin orden obligatorio); **sincronización huevo → nacimiento → colocación → faena (granja ≠ galpón)**; dependencias; datos de campo por actor |
| [`demanda_alimento.md`](demanda_alimento.md) | t/día, t/semana, t/año por escala; fases; categorías de materias primas (sin fórmula) |
| [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md) | Proceso recepción → despacho; capacidad requerida (t/h) con sus cinco factores; horas de producción por semana; sin fabricante |
| [`almacenamiento_silos.md`](almacenamiento_silos.md) | Silos desde variables (consumo, días de stock, densidad, n.º de materias primas); **inventarios por categoría y por propiedad** (propio / en tercero / cadena) |
| [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md) | Compra / façon (B1 materias primas propias, B2 del elaborador) / planta propia, sin costos |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin jerga y preguntas para fábricas y proveedores de grano |
| [`modelo_upstream.py`](modelo_upstream.py) | Modelo físico (importa `03` v1.1): `python3 modelo_upstream.py [--tablas]`; 21 tests U01–U21 |
| [`escenarios_upstream.csv`](escenarios_upstream.csv) | Salidas en formato largo (15.998 filas; 1.054 PENDIENTES con valor vacío). **Sin precios** |
| [`actualizaciones_gestion_14B.md`](actualizaciones_gestion_14B.md) | **Archivo histórico**: propuestas de la sesión 14B, ya integradas en `00_gestion_proyecto` (mapa de IDs en [`../00_gestion_proyecto/reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2) |
| [`fuentes_14B.csv`](fuentes_14B.csv) | **Histórico, no activo** desde la reconciliación de las sesiones 14 (2026-10-02): las 5 fuentes están en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (FTE-305 a FTE-309, todas `[PVDP]`) |

### Columnas de `escenarios_upstream.csv`

`bloque` (1_pollitos, 1_pollitos_entregas, 2_cadena_temporal, 2_incubacion, 2_incubacion_cadencia, 2_incubacion_expedicion, 2_incubacion_almacen, 2_incubacion_logistica, 2_incubacion_elasticidad, 2_reproductoras_fase_futura, 3_sincronizacion, 4_alimento, 5_materias_primas, 6_planta_alimento, 6_planta_horas, 7_silos, 7_inventarios, 8_opcion_pollito, 8_opcion_alimento, 8_opcion_granjas, 9_arquitecturas_referencia, 10_logistica) · `escala_aves_faenadas_dia` · `dias_faena_semana` (5 / 6) · `nivel_produccion` (favorable / medio / desfavorable de `03`) · `opcion` (A / B / C por eslabón —todas escenarios de comparación—, arquitectura de inventario o de referencia) · `parametros` (supuestos usados en la fila) · `variable` · `valor` (vacío si PENDIENTE) · `unidad` · `periodo` (semana plena / promedio anual / año / día / por lote o nacimiento / capacidad) · `clasificacion` · `estado` (CALCULADO / PENDIENTE) · `fuente` · `nota`. Separador decimal: punto.

**Estado:** modelo preliminar; **sin decisión de integración** (DEC-020, DEC-023, DEC-024 abiertas), sin CAPEX/OPEX, sin datos de campo.
