# 18 — Recursos humanos

**Alcance:** dotación por escenario y eslabón, perfiles, convenios colectivos aplicables, costos laborales, capacitación, disponibilidad de mano de obra en zonas candidatas.

**Relacionado:** `10_localizacion`, `20_opex`.

**Estado (2026-10-01, sesión 14A):** modelo preliminar **completado** v1.1 (auditoría de unidades laborales) de organización y dotación para 2.500 / 5.000 / 10.000 / 20.000 aves/día. **Sin escala, automatización, turnos ni modalidades elegidas; sin costos (OPEX laboral pendiente).** Evidencia de campo pendiente (dotación real, productividad, convenio, ausentismo, limpieza, mantenimiento, inspección oficial).

**Reconciliación (2026-10-02):** los IDs provisionales de esta carpeta se reemplazaron por los definitivos de los registros centrales (mapa en [`../00_gestion_proyecto/reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2); ninguna decisión se cerró y la lógica del modelo no cambió.

## Contenido

| Archivo | Contenido |
|---|---|
| [`conclusiones_rrhh.md`](conclusiones_rrhh.md) | Síntesis: estructura, dotación, directos/indirectos, turnos, automatización, mantenimiento, limpieza, faltantes, tests |
| [`estructura_organizacional.md`](estructura_organizacional.md) | Mapa de funciones por bloque, zona y modalidad; organigramas en tres niveles (asset-light, planta pequeña/media, planta escalada) |
| [`dotacion_por_escala.md`](dotacion_por_escala.md) | Unidades laborales separadas (puestos, simultáneos, pico en sitio, puestos equivalentes, headcount PENDIENTE, FTE, horas contratadas) por escala; puestos por tarea y zona; asset-light por bloque |
| [`turnos_y_productividad.md`](turnos_y_productividad.md) | Horas de línea vs presencia; brecha de jornada (sin horas extra automáticas); matriz de presencia y pico; 1 turno / extendido / 2 turnos con la ecuación de 24 h de 09A; KPI con denominador; automatización por tarea |
| [`mantenimiento_y_servicios.md`](mantenimiento_y_servicios.md) | Mantenimiento por activos y cobertura (propio / tercerizado / mixto); limpieza y sanitización (propia / tercerizada / híbrida); HyS, lavandería, utilities |
| [`calidad_inocuidad.md`](calidad_inocuidad.md) | Control operativo, QA, inocuidad, trazabilidad, APPCC, documentación, laboratorio; qué dice y qué no dice la norma |
| [`guia_ramiro.md`](guia_ramiro.md) | Resumen práctico y **preguntas de campo** de RR. HH. para visitas a plantas |
| [`actualizaciones_gestion_14A.md`](actualizaciones_gestion_14A.md) | **Archivo histórico**: registros provisionales de la sesión 14A, ya integrados en `00_gestion_proyecto` (mapa de IDs en [`../00_gestion_proyecto/reconciliacion_sesiones_14.md`](../00_gestion_proyecto/reconciliacion_sesiones_14.md) §2) |
| [`fuentes_14A.csv`](fuentes_14A.csv) | **Histórico, no activo** desde la reconciliación de las sesiones 14 (2026-10-02): las 7 fuentes están en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (FTE-298 a FTE-304, todas `[PVDP]`) |
| [`modelo_rrhh.py`](modelo_rrhh.py) | Modelo reproducible (abajo) |
| [`escenarios_rrhh.csv`](escenarios_rrhh.csv) | 15.576 escenarios (una fila por escenario) |
| [`plantilla_costo_laboral.csv`](plantilla_costo_laboral.csv) | Estructura de costo futuro por puesto y modalidad (PUESTO, ÁREA, HEADCOUNT = PENDIENTE, FTE, HORAS_MES, TURNOS, TIPO_CONTRATACIÓN, SUELDO_BASE, CARGAS, ADICIONALES, HORAS_EXTRA, BENEFICIOS, COSTO_EMPRESA_MENSUAL/ANUAL, FUENTE, ESTADO) para los 4 escenarios de referencia — **costos vacíos** |

## Modelo [`modelo_rrhh.py`](modelo_rrhh.py) (v1.1, auditoría de unidades laborales) — regla 15

| Aspecto | Contenido |
|---|---|
| Unidades (no se suman entre sí) | **Puestos por turno**, **dotación simultánea**, **puestos simultáneos de producción**, **pico de personas en sitio** (matriz de presencia), **puestos equivalentes internos** (base de headcount), **headcount de nómina** (= puestos equivalentes × FACTOR_COBERTURA_NOMINA; **PENDIENTE** sin factor validado; nunca desde FTE), **FTE** (horas-persona/día ÷ jornada de referencia de 8 h), **FTE tercerizados / horas contratadas**, **funciones cubiertas** |
| Qué calcula | Lista de puestos por tarea y función con las unidades anteriores, zona, franja, grupo, driver de escala y modalidad (interno / tercerizado / externo por servicio / PENDIENTE); matriz de presencia (ingreso, duración, salida) y pico en sitio; brecha de jornada y alertas de 24 h (sin horas extra automáticas); mantenimiento con cobertura (política) y carga (activos) separadas; KPI con denominador y universo declarados; insumo para layout (`salida_layout`: pico simultáneo, nunca FTE) |
| Entradas | `aves_dia`, `horas_netas`, `turnos` (1 / extendido / 2), `automatizacion` (manual / mecanizado / semiautomatico / automatico), `config` (A / B / C), `flota_propia`, `limpieza` (propia / tercerizada / hibrida), `mantenimiento` (propio / tercerizado / mixto), `productividad` (alta / media / baja), `ventana`, `dias_semana`, `planta_propia` (False = asset-light), `abastecimiento` (integracion / compra), `laboratorio`, `factor_cobertura_nomina` (None = PENDIENTE), `aves_camion`, `cap_camion_producto_t`, `dist_producto_km` (None = PENDIENTE) |
| Importa (sin modificar) | `05_proceso_industrial/modelo_capacidad_proceso.py` (ecuación de 24 h, D, pausas, kg/ave del balance v1.1); `09_layout_obra_civil/modelo_superficies.py` (m² de proceso para limpieza; proxy SUP-116 sólo para comparar); `13_logistica/modelo_logistica.py` (flota y horas-camión de aves vivas, granjas equivalentes, camión-día de producto); `08_maquinaria/matriz_equipos.csv` (activos) |
| Fórmulas | En el encabezado del archivo: puestos por tarea = ⌈fijo + coeficiente × driver⌉; FTE línea = puestos × cuadrillas × presencia ÷ 8; limpieza = dotación simultánea × ventana ÷ 8; mantenimiento = máx(cobertura, carga); pico = máximo de la matriz de presencia; brecha = máx(0, presencia − 8) |
| Supuestos | SUP-124 a SUP-141 (reconciliación 14) más SUP-033, SUP-061, SUP-062, SUP-063 del registro central |
| Unidades de salida | puestos, personas simultáneas, FTE, h, h-persona/día, aves/h, kg/h, t/día, m²; punto decimal en CSV |
| Salidas | `escenarios_rrhh.csv` (15.576 escenarios; columnas por unidad: `puestos_simultaneos_produccion`, `pico_personas_en_sitio`, `puestos_equivalentes_internos`, `headcount_nomina` = PENDIENTE, `headcount_sensibilidad_f108/_f118`, `fte_internos`, `fte_tercerizados`, `horas_contratadas_dia`, FTE por grupo y por driver, mantenimiento cobertura/carga, funciones, KPI, brecha de jornada, alertas); `plantilla_costo_laboral.csv` (costos vacíos) |
| Tests | 24 (R01–R14 adaptados; R15–R23 de unidades: variables distintas, cuadrilla parcial ≠ FTE, tercerización conserva horas, sin horas extra automáticas, cobertura vs carga, layout recibe pico, KPI con denominador, plantilla sin salarios, SENASA fuera de la empresa). `--mutaciones`: 13/13 detectadas |
| Uso | `python3 18_recursos_humanos/modelo_rrhh.py` (tests + CSV + tablas); `--solo-tests`; `--tablas`; `--detalle 10000` (puestos y matriz de presencia); `--mutaciones` |
| Limitaciones | Coeficientes sin dato argentino (rangos); FACTOR_COBERTURA_NOMINA sin valor; limpieza sobre m² proxy de 12C y ventana fija; horario de la matriz de presencia supuesto (SUP-141); choferes de producto, inspección oficial, HyS externo y captura PENDIENTES; sin costos |
