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

**Modelo [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py) (v1.1, corrección conceptual final)** — regla 15

| Aspecto | Contenido |
|---|---|
| Qué calcula | Ritmo operativo (E/h netas); ritmo nominal a pedir con factores de **sensibilidad** (E/(h×R) y E/(h×D×R)); aves/día de una línea nominal (L × h programadas × D × R); **ecuación de 24 h** (faena neta + paradas + pausas + cambios de turno + arranque + cierre + limpieza intermedia + limpieza + sanitización + mantenimiento + holgura) con **alerta** si la holgura es negativa y horas netas máximas por escenario; flujos por hora y por día (config. A/B/C); carcasas en el enfriamiento; puestos manuales equivalentes; t/día a congelar (P1–P3); funciones de **jerarquía de capacidades** (teórica de equipo → cuello de botella → operativa de planta → producción real) |
| Entradas | Escalas, horas netas, perfiles de destino y kg/ave importados de `23_plan_expansion/modelo_escala.py` (v1.1) y del balance v1.1; sensibilidades SUP-09A-01 a SUP-09A-04 (D, R, ventanas, `t_limpieza` provisional, productividades, residencia); referencias de proveedores (fuente primaria del fabricante) cargadas **solo como referencia** |
| Unidades | aves, aves/h, aves/min, s, kg, kg/h, t, h, 0/1 (alerta); columna `base`; punto decimal |
| Salida | [`capacidad_proceso.csv`](capacidad_proceso.csv) (columnas: bloque, escala_aves_dia, horas_netas, parametro, variable, valor, unidad, base, fuente_modelo, clasificacion, nota) |
| Tests | 18: T01 ritmos = `escenarios_escala.csv`; T03 jerarquía de capacidades; T04 flujos = balance; T05/T13 ecuación de 24 h completa; T08 modelos anteriores intactos; T11 línea nominal ≠ escala; **T14** sensibilidades nunca `[VERIFICADO]`; **T15** capacidad efectiva ≤ nominal salvo justificación; **T16** alerta si > 24 h; **T17** Δ limpieza ⇒ −Δ holgura; **T18** capacidades de proveedores bloqueadas como diseño. `--mutaciones`: 9/9 detectadas |
| Uso | `python3 05_proceso_industrial/modelo_capacidad_proceso.py` (`--solo-tests`, `--mutaciones`) |
| Limitaciones | D, R y ventanas son sensibilidades, no datos argentinos; `t_limpieza` no depende todavía de escala, configuración ni automatización; puestos equivalentes ≠ dotación |
