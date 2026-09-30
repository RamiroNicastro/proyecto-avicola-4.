# 03 — Producción primaria

**Alcance:** granjas de engorde y, eventualmente, de reproductoras. Genética, parámetros productivos, galpones (convencionales / ambiente controlado), sanidad, bioseguridad, bienestar animal, esquemas propio vs. integrados.

**Preguntas clave**
- ¿Granjas propias, productores integrados, compra de pollo vivo o combinación? (DEC-020, sin decidir)
- ¿Qué parámetros productivos de referencia usar y con qué fuente? (rangos en `ciclo_productivo.md`; validación en DPV-044)

## Contenido (v1.1, 2026-09-29; auditoría del modelo físico)

| Archivo | Contenido |
|---|---|
| [`conclusiones_produccion.md`](conclusiones_produccion.md) | **Síntesis**: hallazgos, rangos, escenarios, riesgos, información de campo, calidad |
| [`ciclo_productivo.md`](ciclo_productivo.md) | Proceso de pollito BB a frigorífico; rangos de edad, peso, FCR, mortalidad y uniformidad; densidad y bienestar; ciclos/año; dimensionamiento por escenarios; sensibilidad física |
| [`alimentacion.md`](alimentacion.md) | FCR en profundidad; alimento por escenario y por fase; composición y materias primas; agua (consumo, calidad, almacenamiento, tratamiento) |
| [`galpones.md`](galpones.md) | Tipos de galpón y comparación; energía, clima, riesgo eléctrico; implicancias regionales |
| [`bioseguridad.md`](bioseguridad.md) | Normativa SENASA identificada, medidas por componente, enfermedades, regionalización y compartimentación |
| [`transporte_aves.md`](transporte_aves.md) | Ayuno, captura, carga, transporte, DOA, merma, bienestar, lavado; distancia y localización |
| [`modelos_integracion.md`](modelos_integracion.md) | Granjas propias vs integrados vs compra vs mixto; pollito BB, incubadoras, contratos y riesgos |
| [`kpis_productivos.md`](kpis_productivos.md) | Indicadores, fórmulas, rangos orientativos y uso gerencial |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos, indicadores y preguntas para el responsable del proyecto |
| [`cuestionario_productores.md`](cuestionario_productores.md) | (2026-09-30) Cuestionario de campo para productores: capacidad, desempeño, insumos, bioseguridad, contratos, reparto de costos productor/integrador y registro de 6–12 crianzas |
| [`escenarios_produccion.csv`](escenarios_produccion.csv) | 72 escenarios físicos (4 plantas de 2.500–20.000 aves faenadas/día × 2 regímenes de faena × 3 perfiles × 3 desempeños). **ESCENARIOS, no diseño** |
| [`modelo_escenarios_produccion.py`](modelo_escenarios_produccion.py) | Modelo que genera el CSV: fórmulas, parámetros, fuentes y verificación de balances (`python3 modelo_escenarios_produccion.py --tablas`) |

### Columnas principales del CSV (versión 1.1)

Unidades: aves (cabezas), kg de peso vivo, t (1.000 kg), m², m³, días, semanas (52,14/año); separador decimal: punto. Tres categorías de aves: **`pollitos_alojados_*`** (pollitos BB que entran al galpón) → **`aves_cargadas_*`** (salen vivas de la granja) → **`aves_faenadas_*`** (llegan vivas y se faenan). `aves_faenadas_dia` = escala hipotética de la planta. Sufijos: `_semana_plena` = semana sin feriados (ritmo nominal); `_semana_promedio` = total anual / 52,14; `_anio` = anual (250 o 300 días de faena). `capacidad_alojamiento_pollitos` = plazas para sostener la semana plena; `utilizacion_anual_galpones` ≈ 0,96; `inventario_aves_ritmo_pleno` / `inventario_aves_promedio_anual` = aves vivas simultáneas; `mortalidad_granja_aves_anio` / `mortalidad_transporte_aves_anio` = muertes por etapa; `fcr_campo` = alimento entregado / kg vivo cargado; `alimento_ciclo_crianza_t` = alimento de un ciclo de crianza a ritmo pleno (capital de trabajo físico); `galpones_<N>m2` = m² / N sin redondear ni reserva; `agua_bebida_*` = solo bebida (1,8 L/kg de alimento). Supuestos: SUP-025 a SUP-034.

**Pruebas automáticas:** el script verifica en cada corrida (A) pollitos > faenadas, (B) cargadas > faenadas, (C) pollitos > cargadas, (D) monotonía de la mortalidad, (E) monotonía del FCR, (F) linealidad al duplicar la faena, (G) unidades y balances, más casos límite; si alguna falla, se detiene.

**Relacionado:** `04_balance_masa`, `10_localizacion`, `13_logistica`, `14_alimento_balanceado`, `15_incubacion`, `16_normativa_senasa`, `22_riesgos`.
