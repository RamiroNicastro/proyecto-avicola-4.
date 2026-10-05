# Stress tests

**Fecha:** 2026-10-05 · Input: [`escenarios_stress.csv`](escenarios_stress.csv) · Código: `leer_stress()`, `correr_stress()` en [`motor_riesgo.py`](motor_riesgo.py) · Salida: [`resultados_stress.csv`](resultados_stress.csv)

- Un stress cambia **varias** variables a la vez (independiente de la sensibilidad one-way). Plantillas: STRESS_DEMANDA, STRESS_ALIMENTO, STRESS_PRECIO, STRESS_CAPEX, STRESS_RAMP_UP, STRESS_FINANCIERO, STRESS_COMBINADO y STRESS_EXPORTACION_CERRADA (desactivado: variable discreta, se evalúa con `stress.corte_exportacion_desde_mes` del motor cuando el escenario tenga exportación).
- **Magnitudes:** las de demanda (−30 %), alimento (+20 %), precio (−10 %), CAPEX (+25 %) y ramp-up (×2) son las plantillas `STRESS_PREDEFINIDOS` de 21, rotuladas `ILUSTRATIVO_EDITABLE` (SUP-223). No son pronósticos ni probabilidades. El stress financiero queda `NO_EJECUTADO_VALORES_PENDIENTES` hasta que el usuario declare sus magnitudes (DEC-102).
- Salida por alternativa y stress: estado, métricas (EBITDA, VAN, TIR si se pide, payback, pico, fondos, DSCR, caja mínima) y deltas contra la base.
- Los stress alimentan la robustez ([`robustez.md`](robustez.md)), la estabilidad del ganador ([`objetivos_optimizacion.md`](objetivos_optimizacion.md) §4) y la regla SQ-4 de NO_INVERTIR_AUN ([`metodologia_optimizador.md`](metodologia_optimizador.md) §5).
