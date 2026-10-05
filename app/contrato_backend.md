# Contrato del backend (API HTTP local)

Servidor: `python3 app/app.py` → `http://127.0.0.1:8765`. Todas las rutas `/api/*` responden JSON `{"ok": true, "datos": …}` o `{"ok": false, "error": {"codigo", "mensaje", "ref"?}}` (salvo las de exportación CSV/HTML). El escenario viaja completo en cada petición (`"escenario": {…}`): el servidor no guarda estado de sesión.

## Lectura

| Método y ruta | Devuelve |
|---|---|
| `GET /api/estado` | versión (app, motores, commit, fecha), progreso por dimensión, estadísticas de caché, leyenda del semáforo, disclaimer |
| `GET /api/catalogo` | arquitecturas (mapa + explicación), escalas (rango, referencia, trayectorias), productos (kg/ave), canales, categorías y unidades de demanda, objetivos (y su traducción simple), restricciones, reglas de status quo, variables de riesgo (soporte, tipo de shock, DPV), stress del repo, distribuciones admitidas, inputs de 22, métodos de deuda, etiquetas |
| `GET /api/escenarios` · `GET /api/escenarios/<id>` | lista (base + guardados) · un escenario |
| `GET /api/validacion` | paquetes de `plan_validacion_final.md` (con pedidos y DPV centrales), `prioridad_validacion.csv`, `que_hacer_ahora.csv`, progreso |
| `GET /api/evidencia` | precios de `base_precios_venta.csv`, inputs EVIDENCIA, publicables por flag (0/42), umbral, progreso |
| `GET /api/trazabilidad` · `GET /api/riesgos_cualitativos` | `trazabilidad_end_to_end.csv` + KPI → variables · `matriz_riesgos.csv` |
| `GET /api/staging` | datos cargados a mano (sin clasificar) |
| `GET /api/documento/<nombre>` | `interfaz_app_v1`, `plan_validacion_final`, `estado_proyecto` (texto) |

## Cálculo (POST, cuerpo `{"escenario": …, …}`)

| Ruta | Parámetros extra | Devuelve | Motor |
|---|---|---|---|
| `/api/nuevo` | `nombre` | escenario vacío (todo PENDIENTE) | — |
| `/api/validar` | — | escenario normalizado | — |
| `/api/alternativas` | — | alternativas del escenario con evaluación rápida (¿VAN calculable?, bloques faltantes) | `Evaluador.evaluar(tir=False)` |
| `/api/simular` | `alternativa` (opcional) | `resultado` (ALTERNATIVA · SIN_INVERSION · NO_CALCULABLE · PESOS_NO_DEFINIDOS), ficha, detalle (resultados, faltantes, estado de bloques, completitud, series anuales, traza), tarjetas, por_que, que_hacer, alertas, disclaimer | `correr_universo` + `simular`/`resultados(calcular_tir=True)` |
| `/api/comparar` | `ids` (2–5) | fichas, `comparable`, no comparables con motivo, decisiones y Pareto solo si comparable | `correr_universo` |
| `/api/optimizar` | — | decisión principal y por objetivo (`ESTADO_APP`), explicación, fichas con ranking, Pareto, consultas (capital, demanda, payback), prioridad de escenario, qué hacer | `correr_universo`, `consultas`, `que_hacer_ahora` |
| `/api/riesgo/sensibilidad` | `alternativa`, `variables`, `shocks` | filas one-way (VAN, EBITDA, payback, pico, Δ) | `sensibilidad_oneway` |
| `/api/riesgo/tornado` | `alternativa`, `metrica`, `variables` | tornado ordenado; `calculable` = FALSE si la métrica base no es publicable | `tornado` |
| `/api/riesgo/sens2d` | `alternativa`, `vx`, `vy`, `shocks` | grilla 2D con zonas (umbrales solo declarados) | `sensibilidad_2d` |
| `/api/riesgo/stress` | `alternativa`, `stresses` [{id, nombre, shocks}] | base vs stress; vacío → NO_EJECUTADO_VALORES_PENDIENTES | `correr_stress` |
| `/api/riesgo/quiebres` | `alternativa` | precio mínimo, alimento máximo, CAPEX máximo, demanda mínima, utilización mínima, días de cobro máximos (VAN = 0) y precio mínimo (EBITDA = 0); estado por quiebre | `punto_quiebre` |
| `/api/riesgo/montecarlo` | `alternativa`, `n`, `semilla` | `disponible`, resumen (P10/P50/P90, PROB_VAN_NEGATIVO simulada), muestras de VAN; o NO_DISPONIBLE con explicación | `monte_carlo` |
| `/api/modulos` | `alternativa` | módulos CAPEX/OPEX admitidos por la arquitectura (para overrides TF-004) | `contexto_override` |
| `/api/traza` | `alternativa` | mapa de drivers (traza del motor) | `construir_entrada` |
| `/api/costo_unitario` | `alternativa`, `concepto`, `precio` | rubro costeado por el módulo 20 o NO_APLICA | `modelo_opex.correr` (copia en memoria) |

## Escenarios y exportación

| Ruta | Efecto |
|---|---|
| `POST /api/escenarios` | guardar (los base son de solo lectura → 400) |
| `POST /api/escenarios/<id>/duplicar` · `/renombrar` | `{nombre}` |
| `DELETE /api/escenarios/<id>` | eliminar (solo guardados) |
| `POST /api/escenarios/importar` | importa un JSON versionado (nuevo id) |
| `POST /api/exportar/json` | escenario + `sello` (versión app, motor, commit) |
| `POST /api/exportar/csv` | `text/csv`: SECCION, CAMPO, VALOR, UNIDAD_O_FORMATO, ESTADO, ETIQUETA (NO_CALCULABLE como estado, nunca 0) |
| `POST /api/exportar/resumen` | `text/html`: resumen ejecutivo imprimible (inputs, arquitectura, resultados, sensibilidad, stress, evidencia, faltantes, qué hacer, alertas, disclaimer) |
| `POST /api/staging` | `{dato: {concepto, valor, unidad, moneda, fecha, fuente, observaciones, tipo}}` → staging sin clasificar |

## Códigos de error

| HTTP | `codigo` | Cuándo |
|---|---|---|
| 400 | `ENTRADA_INVALIDA`, `OVERRIDE_TOTAL_SIN_CONFIRMAR`, … | escenario inválido, ARS sin TC, escala fuera de rango, comparación con < 2 o > 5, alternativa inexistente |
| 422 | `OVERRIDE_INCOMPATIBLE`, `MOTOR_RECHAZO_LA_ENTRADA` | el motor rechaza la entrada (mensaje de usuario + `ref` al log) |
| 500 | `ERROR_INTERNO` | error inesperado (sin traceback en la respuesta; detalle en `app/datos_locales/logs/app.log`) |
| 404 | `NO_ENCONTRADO` | ruta inexistente |

`servidor.manejar(metodo, ruta, cuerpo)` permite usar el mismo despacho sin HTTP (tests).
