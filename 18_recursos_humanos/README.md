# 18 — Recursos humanos

**Alcance:** dotación por escenario y eslabón, perfiles, convenios colectivos aplicables, costos laborales, capacitación, disponibilidad de mano de obra en zonas candidatas.

**Relacionado:** `10_localizacion`, `20_opex`.

**Estado (2026-10-01, sesión 14A):** modelo preliminar **completado** v1.0 de organización y dotación para 2.500 / 5.000 / 10.000 / 20.000 aves/día. **Sin escala, automatización, turnos ni modalidades elegidas; sin costos (OPEX laboral pendiente).** Evidencia de campo pendiente (dotación real, productividad, convenio, ausentismo, limpieza, mantenimiento, inspección oficial).

## Contenido

| Archivo | Contenido |
|---|---|
| [`conclusiones_rrhh.md`](conclusiones_rrhh.md) | Síntesis: estructura, dotación, directos/indirectos, turnos, automatización, mantenimiento, limpieza, faltantes, tests |
| [`estructura_organizacional.md`](estructura_organizacional.md) | Mapa de funciones por bloque, zona y modalidad; organigramas en tres niveles (asset-light, planta pequeña/media, planta escalada) |
| [`dotacion_por_escala.md`](dotacion_por_escala.md) | Personas por turno, personas físicas y equivalentes por escala; por área y por zona; asset-light; sensibilidades; comparación con el proxy de 12C |
| [`turnos_y_productividad.md`](turnos_y_productividad.md) | 1 turno / turno extendido / 2 turnos; horas netas vs presencia; integración con la ecuación de 24 h de 09A; KPI; automatización |
| [`mantenimiento_y_servicios.md`](mantenimiento_y_servicios.md) | Mantenimiento por activos y cobertura (propio / tercerizado / mixto); limpieza y sanitización (propia / tercerizada / híbrida); HyS, lavandería, utilities |
| [`calidad_inocuidad.md`](calidad_inocuidad.md) | Control operativo, QA, inocuidad, trazabilidad, APPCC, documentación, laboratorio; qué dice y qué no dice la norma |
| [`guia_ramiro.md`](guia_ramiro.md) | Resumen práctico y **preguntas de campo** de RR. HH. para visitas a plantas |
| [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md) | SUP-14A, DPV-14A, DEC-14A, tensiones y fila del tablero, pendientes de reconciliación |
| [`fuentes_14A.csv`](fuentes_14A.csv) | Fuentes provisionales FTE-14A-001 a 007 (todas `[PVDP]`) |
| [`modelo_rrhh.py`](modelo_rrhh.py) | Modelo reproducible (abajo) |
| [`escenarios_rrhh.csv`](escenarios_rrhh.csv) | 15.576 escenarios (una fila por escenario) |
| [`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv) | Estructura de costo futuro por puesto (PUESTO, CANTIDAD, HORAS, TIPO_CONTRATO, COSTO_EMPRESA_MENSUAL, COSTO_ANUAL) para los 4 escenarios de referencia — **costos vacíos** |

## Modelo [`modelo_rrhh.py`](modelo_rrhh.py) (v1.0) — regla 15

| Aspecto | Contenido |
|---|---|
| Qué calcula | Lista de puestos por escenario con puestos por turno, cuadrillas, personas físicas, equivalentes (FTE por horas), zona, grupo (directo / supervisión / soporte / administración / dirección), modalidad (interno / externo / PENDIENTE); agregados; externos equivalentes; alertas de jornada, horas extra y ecuación de 24 h; KPI (aves y kg por persona-hora, personas por 1.000 aves, indirecta/directa, directos por supervisor, equipos por técnico) |
| Entradas | `aves_dia`, `horas_netas`, `turnos` (1 / extendido / 2), `automatizacion` (manual / mecanizado / semiautomatico / automatico), `config` (A / B / C), `flota_propia`, `limpieza` (propia / tercerizada / hibrida), `mantenimiento` (propio / tercerizado / mixto), `productividad` (alta / media / baja), `ventana`, `dias_semana`, `planta_propia` (False = asset-light), `abastecimiento` (integracion / compra), `laboratorio`, `aves_camion`, `cap_camion_producto_t`, `dist_producto_km` (None = PENDIENTE) |
| Importa (sin modificar) | `05_proceso_industrial/modelo_capacidad_proceso.py` (ecuación de 24 h, D, pausas, kg/ave del balance v1.1); `09_layout_obra_civil/modelo_superficies.py` (m² de proceso para limpieza; proxy SUP-116 sólo para comparar); `13_logistica/modelo_logistica.py` (flota mínima de aves vivas, granjas equivalentes, camión-día de producto); `08_maquinaria/matriz_equipos.csv` (activos para mantenimiento) |
| Fórmulas | Documentadas en el encabezado del archivo: puestos por área = ⌈fijo + coeficiente × driver⌉ (aves/h, kg/h o t/día); personas = ⌈puestos × cuadrillas × cobertura⌉; equivalentes = puestos × cuadrillas × presencia × días ÷ horas normales × cobertura; limpieza = m² × factor ÷ productividad ÷ ventana; mantenimiento = max(cobertura presencial, carga por activos); supervisión = ⌈directos ÷ span⌉ |
| Supuestos | SUP-14A-01 a SUP-14A-15 (provisionales) más SUP-033, SUP-061, SUP-062, SUP-063 del registro central |
| Unidades | personas, personas/turno, FTE, h, h/semana, aves/h, kg/h, t/día, m²; punto decimal en CSV |
| Salidas | `escenarios_rrhh.csv` (identificación del escenario, ritmo, presencia, horas extra, holgura 24 h, alertas, directos por turno, personas por turno y por zona, personas y equivalentes por grupo y bloque, externos, mantenimiento, KPI, proxy de 12C, pendientes, estado, clasificación `[ESTIMACIÓN]`); `plantilla_costo_laboral.csv` |
| Tests | 15 (R01–R14 y R03b): dotación no negativa; escala no reduce personal; automatización no reduce técnicos; tercerización conserva la función; 24 h y jornada explícitas; independencia de escenarios; faltantes no rellenados; entradas inválidas; consistencia; KPI; 09A intacto; rangos ordenados; mix. `--mutaciones`: 8/8 detectadas |
| Uso | `python3 18_recursos_humanos/modelo_rrhh.py` (tests + CSV + tablas); `--solo-tests`; `--tablas`; `--detalle 10000`; `--mutaciones` |
| Limitaciones | Coeficientes sin dato argentino (rangos); limpieza sobre m² proxy de 12C; choferes de producto, inspección oficial, HyS externo y captura PENDIENTES; sin costos |
