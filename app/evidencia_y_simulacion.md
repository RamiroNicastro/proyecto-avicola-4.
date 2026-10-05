# Evidencia, simulación y pendiente en la app

La app muestra tres universos que **no se mezclan** y que no pueden confundirse visualmente (nunca solo por color: siempre icono + texto).

| Universo | Rótulo en la app | Origen | Qué significa |
|---|---|---|---|
| **Datos reales / evidencia** | ✔ EVIDENCIA (verde, borde continuo) | Modo EVIDENCIA del motor: solo datos E1–E3 (umbral `umbral_evidencia_publicacion`, DEC-084) | Dato observado con fuente. Hoy: 0 precios, 0 CAPEX/OPEX con evidencia; 0 de 42 corridas con VAN publicable |
| **Escenario hipotético** | ◇ SIMULACIÓN / ◇ ESCENARIO (violeta, borde punteado) | Inputs del usuario (modo ESCENARIO del motor) | `SIMULACION_HIPOTETICA_NO_VALIDADA` (o `SIMULACION_HIPOTETICA_OVERRIDE_TOTAL`). Resultado calculado sobre hipótesis; no es evidencia ni pronóstico |
| **Pendiente** | … PENDIENTE / ∅ NO CALCULABLE (gris, borde de puntos) | Falta un dato | Nunca 0: se muestra qué falta (bloque y detalle del motor, con su DPV/DEC) |
| Demo | ✱ SOLO DEMOSTRACIÓN (naranja, borde de rayas) | `DEMO_ARTIFICIAL` | Datos ficticios; universo ARTIFICIAL_TEST |
| Supuesto del modelo | ~ SUPUESTO DEL MODELO | Supuestos metodológicos del motor (p. ej. rendimientos del balance 04, curva ilustrativa) | Visibles en la traza; no son evidencia |
| No comparable / no aplica / no calculada | ≠ / – / ∅ | Estados del motor | No entran a rankings, Pareto ni dominancia |

## Reglas que la app hace cumplir

1. **Ningún número de escenario sin rótulo.** Toda pantalla económica tiene el banner del universo; cada valor de las tarjetas lleva la etiqueta ◇ SIMULACIÓN; los exports llevan la etiqueta y el disclaimer.
2. **Faltante ≠ 0.** Si el flag `PUBLICABLE_*` del motor es FALSE, la tarjeta dice NO CALCULABLE y lista qué falta; los gráficos marcan ∅ (sin dato) y no dibujan barras en 0; el CSV pone NO_CALCULABLE en ESTADO.
3. **El usuario no convierte nada en evidencia.** Marcar un precio como «Validado» en un escenario es una declaración del usuario: en la traza su origen sigue siendo ESCENARIO_USUARIO (test `test_evidencia_queda_etiquetada`).
4. **La evidencia central es de solo lectura.** La app no escribe en `base_precios_venta.csv`, `base_costos_opex.csv`, `inputs_financieros.csv`, `inputs_riesgo_optimizacion.csv`, `escenario_optimizador.json`, `datos_por_validar.md` ni `registro_fuentes.csv` (test `test_escenario_no_modifica_evidencia` compara huellas SHA-256 antes y después).
5. **Probabilidades.** Monte Carlo solo con distribuciones RESPALDADAS (proyecto) o ARTIFICIALES (demo); el resultado se rotula PROBABILIDAD SIMULADA (no histórica, no del proyecto). Sin distribuciones: NO DISPONIBLE «Faltan distribuciones de probabilidad respaldadas».
6. **Score de riesgo** = orden relativo, **no es probabilidad**. Robustez = % de escenarios determinísticos con VAN ≥ 0.
7. **Los ~90 supermercados no son demanda** y **USD 2 M no es un default**: la app no los carga en ningún escenario por defecto.

## Cargar un dato (STAGING)

VALIDACIÓN → «Cargar un dato»: concepto, valor, unidad, moneda, fecha, fuente, observaciones, tipo (cotización / factura / mercado / escenario / otro). Se guarda en `app/datos_locales/staging/cotizaciones_staging.jsonl` con estado `STAGING_SIN_CLASIFICAR`, `incorporado_a_evidencia = false` y nivel «SIN_CLASIFICAR». La app **no** asigna E1/E2/E3: la clasificación sigue [`../00_gestion_proyecto/guia_recoleccion_evidencia.md`](../00_gestion_proyecto/guia_recoleccion_evidencia.md) y la incorporación a la base corresponde a una acción explícita del analista (DEC-105).
