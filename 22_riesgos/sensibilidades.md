# Sensibilidades: one-way, tornado y 2D

**Fecha:** 2026-10-05 · Código: `sensibilidad_oneway()`, `tornado()`, `sensibilidad_2d()` en [`motor_riesgo.py`](motor_riesgo.py) · Salidas: [`sensibilidad_oneway.csv`](sensibilidad_oneway.csv), [`sensibilidad_tornado.csv`](sensibilidad_tornado.csv), [`sensibilidad_2d.csv`](sensibilidad_2d.csv) · Variables: [`metodologia_riesgo.md`](metodologia_riesgo.md) §2

## 1. One-way

- Una variable por vez; todas las demás iguales (test SENS-01: solo cambian los campos de la variable elegida). La base nunca se modifica (SENS-02) y la evidencia no se perturba (SENS-03).
- Shocks por defecto (configurables, sin significado probabilístico): relativos −30 % … +30 %; días −30 … +30; meses −24 … +24.
- Métricas: ingresos, EBITDA, margen, FCFF total, fondos iniciales, pico de fondos, VAN, TIR (solo si se pide; si no, `NO_CALCULADA`), payback, break-even, DSCR, utilización y CT. Una métrica que la base no publica queda vacía en todas las filas.
- Monotonía verificada donde corresponde (SENS-04): VAN ↑ con precio; ↓ con CAPEX, alimento, días de cobro y tasa.

## 2. Tornado

Por métrica (`tornado.metricas`; default VAN; admite EBITDA, TIR, PAYBACK, PICO_FONDOS, DSCR). Orden por **amplitud** = máximo − mínimo entre los shocks evaluados, no por impacto con signo (SENS-05; mutación R10). Sin la métrica en la base → `NO_CALCULABLE`, sin ranking (SENS-09).

## 3. Sensibilidad 2D

Grilla completa de dos variables (`sens2d.pares`: precio × alimento, demanda × CAPEX, utilización × precio, demanda × precio, CAPEX × tasa). Conserva ambos ejes (SENS-06). Zonas de VAN y EBITDA por signo; DSCR y payback solo con umbral declarado (`SIN_UMBRAL_DECLARADO` si falta: no se elige un umbral empresarial).

## 4. Estado en el proyecto

Hoy NO_CALCULABLE: ninguna alternativa tiene inputs completos (ver [`conclusiones_riesgo_optimizacion.md`](conclusiones_riesgo_optimizacion.md)). La maquinaria funcionando está en [`casos_prueba/`](casos_prueba/) (`AMBITO = ARTIFICIAL_TEST`).
