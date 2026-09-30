# 05 — Proceso industrial

**Alcance:** faena y procesamiento: recepción, colgado, aturdimiento, sangrado, escaldado, desplumado, evisceración, enfriamiento, clasificación, trozado, envasado, congelado. Parámetros de proceso, calidad, inocuidad (BPM, HACCP).

**Preguntas clave**
- ¿Faena propia o a façon en la primera etapa? (DEC-004)
- ¿Qué nivel de automatización corresponde a cada escenario de escala?

**Contenido**
- [`capacidad_preliminar.md`](capacidad_preliminar.md) (2026-09-30): capacidad nominal / operativa / utilizada, horas de turno vs netas, cuello de botella y ritmo de línea requerido para 2.500–20.000 aves faenadas/día. No diseña el proceso ni selecciona equipos.
- **Sesión 09A (2026-09-30) — modelo conceptual del proceso** (sin escala, proveedor, CAPEX, layout ni localización):
  - [`flujo_proceso.md`](flujo_proceso.md): diagrama completo de 32 etapas, flujos laterales (sangre, plumas, vísceras, decomisos, patas/garras, menudencias, subproductos) con kg/ave y kg/h, rutas entero/trozado/deshuesado, puntos de control.
  - [`zonificacion_higienica.md`](zonificacion_higienica.md): zonas sucia/limpia, fronteras, cruces a evitar (personas, producto, aves, residuos, subproductos, envases, vehículos) y ciclo de limpieza y sanitización.
  - [`cuellos_botella.md`](cuellos_botella.md): capacidad de línea ≠ capacidad de planta; velocidad nominal vs operativa; ritmos a 6/8/10/16 h; ventana horaria del establecimiento; cuellos de botella por sistema.
  - [`arquitecturas_por_escala.md`](arquitecturas_por_escala.md): arquitectura conceptual de 2.500/5.000/10.000/20.000 aves/día, flexibilidad de producto y modularidad (1 vs 2 líneas).
  - [`guia_ramiro.md`](guia_ramiro.md), [`conclusiones_proceso.md`](conclusiones_proceso.md).
  - [`actualizaciones_gestion_09A.md`](actualizaciones_gestion_09A.md): supuestos, datos por validar, decisiones, glosario y fuentes con **IDs provisionales** pendientes de reconciliación central.
  - Equipos, automatización, proveedores y RFQ: [`../08_maquinaria/`](../08_maquinaria/README.md).

**Modelo [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py) (v1.0)** — regla 15

| Aspecto | Contenido |
|---|---|
| Qué calcula | Ritmo operativo (E/h) y nominal (E/h/η); aves/día de una línea nominal (L·h·η); ventana total del establecimiento y holgura contra 24 h; flujos por hora y por día de cada corriente (config. A/B/C); carcasas simultáneas en el enfriamiento; puestos manuales equivalentes; t/día a congelar por perfil P1–P3 |
| Entradas | Escalas, horas netas, perfiles de destino y kg/ave importados de `23_plan_expansion/modelo_escala.py` (v1.1), que a su vez importa el balance v1.1; parámetros de sensibilidad SUP-09A-01 a SUP-09A-04 |
| Unidades | aves, aves/h, aves/min, s, kg, kg/h, t, h; columna `base` (vivo, biologica, comercial, biologica+agua, aves, h); punto decimal |
| Salida | [`capacidad_proceso.csv`](capacidad_proceso.csv) (columnas: bloque, escala_aves_dia, horas_netas, parametro, variable, valor, unidad, base, fuente_modelo, clasificacion, nota) |
| Tests | 13 (T01 ritmos = `escenarios_escala.csv`; T04 flujos = balance; T08 modelos anteriores intactos; T11 línea de 2.500 aves/h × 8 h < 20.000 con η < 1; T13 ventana incluye sanitización y mantenimiento, etc.); `--mutaciones`: 5/5 detectadas |
| Uso | `python3 05_proceso_industrial/modelo_capacidad_proceso.py` (`--solo-tests`, `--mutaciones`) |
| Limitaciones | Sensibilidades, no datos argentinos; ventana independiente de la escala; puestos equivalentes ≠ dotación |

**Relacionado:** `08_maquinaria`, `09_layout_obra_civil`, `16_normativa_senasa`, `23_plan_expansion`.
