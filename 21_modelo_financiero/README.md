# 21 — Modelo financiero

**Alcance:** flujo de fondos por escenario, capital de trabajo, financiamiento, indicadores (VAN, TIR, repago, punto de equilibrio), sensibilidades y escenarios.

**Estado (2026-10-04, sesión 19):** **MODELO FINANCIERO ESTRUCTURAL COMPLETADO v1.0** — motor mensual con modos EVIDENCIA y ESCENARIO, 56 tests y 20/20 mutaciones detectadas. **RENTABILIDAD DEL PROYECTO = NO CALCULABLE**: 0 de 61 corridas publicables (faltan precios, demanda A/B, OPEX y CAPEX costeables, cronograma, fiscal, tasa y financiamiento). Sin recomendación de arquitectura, escala ni financiamiento.

**Reglas específicas**
- Documentar fórmulas, supuestos, unidades y fuentes junto al modelo.
- Declarar criterio de tipo de cambio e inflación (DEC-006) y horizonte/tasa (DEC-007).
- Dos modos que no se mezclan: EVIDENCIA (solo E1–E3; si falta un bloque: `NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE`) y ESCENARIO (inputs del usuario; todo rotulado `SIMULACION_HIPOTETICA_NO_VALIDADA`).
- Faltante = vacío, nunca 0. Proyecto (FCFF) ≠ accionista (FCFE). EBITDA ≠ caja. IVA ≠ costo.

## Uso

```
python3 21_modelo_financiero/modelo_financiero.py                 # tests + CSV de salida
python3 21_modelo_financiero/modelo_financiero.py --solo-tests
python3 21_modelo_financiero/modelo_financiero.py --mutaciones
python3 21_modelo_financiero/modelo_financiero.py --escenario mi_escenario.json --salida carpeta/
```

## Archivos

| Tipo | Archivo | Contenido |
|---|---|---|
| Modelo | [`modelo_financiero.py`](modelo_financiero.py) | Motor, adaptadores, tests y mutaciones |
| Input | [`inputs_financieros.csv`](inputs_financieros.csv) | Inputs editables con procedencia (filas EVIDENCIA y plantillas) |
| Input | [`base_precios_venta.csv`](base_precios_venta.csv) | Precios por producto × canal × mercado (todos vacíos; 2 referencias E4 no usables) |
| Input | [`curvas_rampup.csv`](curvas_rampup.csv) | Curvas ilustrativas CONSERVADOR / BASE / RÁPIDO (SUP-19-09) |
| Input | [`plantilla_escenario_usuario.json`](plantilla_escenario_usuario.json) | Plantilla del modo escenario (todo `null`) |
| Salida | [`escenarios_financieros.csv`](escenarios_financieros.csv) | Resumen por corrida + banderas `PUBLICABLE_*` con motivo |
| Salida | [`estado_resultados.csv`](estado_resultados.csv), [`flujo_caja_proyecto.csv`](flujo_caja_proyecto.csv), [`flujo_accionista.csv`](flujo_accionista.csv), [`capital_trabajo_financiero.csv`](capital_trabajo_financiero.csv), [`deuda.csv`](deuda.csv) | Series por período (hoy sin línea de tiempo: una fila con el motivo) |
| Salida | [`break_even.csv`](break_even.csv), [`completitud_financiera.csv`](completitud_financiera.csv), [`mapa_drivers_financieros.csv`](mapa_drivers_financieros.csv) | Break-even, completitud por bloque, trazabilidad |
| Salida | [`casos_prueba_motor.csv`](casos_prueba_motor.csv) | Casos artificiales de validación (no son escenarios del proyecto) |
| Doc | [`metodologia_financiera.md`](metodologia_financiera.md) · [`arquitectura_financiera.md`](arquitectura_financiera.md) | Método y arquitectura |
| Doc | [`modelo_ingresos.md`](modelo_ingresos.md) · [`modelo_ramp_up.md`](modelo_ramp_up.md) · [`estado_resultados.md`](estado_resultados.md) · [`capital_trabajo_financiero.md`](capital_trabajo_financiero.md) · [`flujo_caja.md`](flujo_caja.md) · [`financiamiento.md`](financiamiento.md) · [`break_even.md`](break_even.md) · [`van_tir_payback.md`](van_tir_payback.md) · [`expansion_financiera.md`](expansion_financiera.md) | Bloques del modelo |
| Doc | [`evidencia_financiera.md`](evidencia_financiera.md) · [`conclusiones_financieras.md`](conclusiones_financieras.md) · [`guia_ramiro.md`](guia_ramiro.md) | Estado, conclusiones y guía |
| Gestión | [`actualizaciones_gestion_19.md`](actualizaciones_gestion_19.md) | SUP-19-01…24, DPV-19-01…11, DEC-19-01…08 provisionales para reconciliar |

**Relacionado:** [`19_capex`](../19_capex/README.md), [`20_opex`](../20_opex/README.md), [`interfaz_capex_finanzas.md`](../00_gestion_proyecto/interfaz_capex_finanzas.md), [`interfaz_opex_finanzas.md`](../00_gestion_proyecto/interfaz_opex_finanzas.md), [`mapa_arquitecturas_economicas.csv`](../00_gestion_proyecto/mapa_arquitecturas_economicas.csv), `22_riesgos`.
