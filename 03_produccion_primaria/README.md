# 03 — Producción primaria

**Alcance:** granjas de engorde y, eventualmente, de reproductoras. Genética, parámetros productivos, galpones (convencionales / ambiente controlado), sanidad, bioseguridad, bienestar animal, esquemas propio vs. integrados.

**Preguntas clave**
- ¿Granjas propias, productores integrados, compra de pollo vivo o combinación? (DEC-020, sin decidir)
- ¿Qué parámetros productivos de referencia usar y con qué fuente? (rangos en `ciclo_productivo.md`; validación en DPV-044)

## Contenido (v1, 2026-09-29)

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
| [`escenarios_produccion.csv`](escenarios_produccion.csv) | 72 escenarios físicos (4 plantas × 2 regímenes de faena × 3 perfiles × 3 desempeños). **ESCENARIOS, no diseño** |
| [`modelo_escenarios_produccion.py`](modelo_escenarios_produccion.py) | Modelo que genera el CSV: fórmulas, parámetros, fuentes y verificación de balances (`python3 modelo_escenarios_produccion.py --tablas`) |

### Columnas principales del CSV

Unidades: aves (cabezas), kg de peso vivo, t (1.000 kg), m², m³, días; separador decimal: punto. `aves_faena_dia` = aves vivas que llegan a planta por día de faena; `capacidad_alojamiento_aves` = pollitos que caben al alojar (suma de galpones); `inventario_promedio_aves` = aves vivas presentes en promedio; `fcr_campo` = alimento entregado / kg vivo cargado; `galpones_<N>m2` = m² / N sin redondear ni reserva; `agua_bebida_*` = solo bebida (1,8 L/kg de alimento). Supuestos: SUP-025 a SUP-034.

**Relacionado:** `04_balance_masa`, `10_localizacion`, `13_logistica`, `14_alimento_balanceado`, `15_incubacion`, `16_normativa_senasa`, `22_riesgos`.
