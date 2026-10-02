# Ramp-up — estructura sin curva definitiva

**Fecha:** 2026-10-02 · Implementación: `aplicar_utilizacion()`, `rampup()`, `ETAPAS_RAMPUP` en [`modelo_opex.py`](modelo_opex.py)

## 1. Qué hace

El registro de costos se arma a la **escala plena** del escenario (capacidad de faena de la configuración = producción madura). Para una etapa con utilización `u` (fracción de esa producción):

```
costo(u) = Σ costo_concepto × (PCT_VARIABLE × u + PCT_FIJO)
```

- **Variables** (alimento, pollito, químicos, empaque, kWh, fletes por unidad): acompañan el volumen (× u).
- **Fijos y semifijos** (administración, seguros, personal de estructura y cuadrillas de línea, cargos fijos): se mantienen.
- **Semivariables**: según su `PCT_VARIABLE`; si no está declarado (hoy, ninguno), el ajuste devuelve **PENDIENTE** (test R03).

## 2. Etapas

| Etapa | Utilización | Estado |
|---|---|---|
| Arranque | `None` | PENDIENTE (no se inventa la curva) |
| Estabilización | `None` | PENDIENTE |
| Operación madura | 1,0 de la escala del escenario | Es la que publica `escenarios_opex.csv` |

Finanzas carga la curva (`rampup(filas, {"arranque": u1, "estabilizacion": u2, "madura": 1.0})`) cuando haya evidencia.

## 3. Límites declarados

1. **Escalamiento lineal** de los drivers variables (DERIVADO_OPEX): no se vuelven a correr los modelos fuente a `u × escala` (podría quedar fuera del rango 2.500–20.000 y los viajes enteros no escalan linealmente).
2. **Ineficiencias del arranque** (mayor mortalidad, peor conversión, rendimiento de línea bajo, mermas, horas extra, scrap de empaque) no están modeladas: requieren parámetros propios del ramp-up (DEC-17-08).
3. **Preoperativos** (commissioning, capacitación, insumos iniciales) están en CAPEX y no se repiten aquí; el OPEX empieza con la operación normal.
4. Con utilización < 1 en la configuración, el motor emite una alerta y sigue publicando la escala plena.

Tests: R01 (u = 0,5 → fijo + 0,5 × variable), R02 (etapas sin factor → PENDIENTE), R03 (semivariable sin reparto → PENDIENTE).
