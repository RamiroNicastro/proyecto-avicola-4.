# Tests de la app

```
python3 app/tests/correr_tests.py            # backend + flujos HTTP + flujos en navegador (si hay Playwright)
python3 app/tests/correr_tests.py --sin-ui   # solo Python
```

Los tests usan una carpeta temporal para datos locales (`APP_AVICOLA_DATOS`) y nunca escriben en la evidencia. Resultado de la sesión 22: **33/33 tests Python OK** (≈ 50 s) y **8/8 flujos de navegador OK** (Chromium headless).

## 1. Backend (`tests/test_backend.py`, 27 tests)

| # pedido | Test | Qué verifica |
|---|---|---|
| Escenario no modifica evidencia | `T01.test_escenario_no_modifica_evidencia`, `test_staging_no_es_evidencia` | SHA-256 de 10 archivos de evidencia iguales tras simular, stress, sensibilidad, guardar, importar y staging; staging sin nivel E |
| Pendientes no se muestran como 0 | `T02.*` | Escenario vacío: todo lo no calculable tiene `valor = None` y lista de faltantes; precio «No sé» no se envía y el VAN dice qué precio falta; el CSV marca NO_CALCULABLE |
| Simple = experto | `T03.test_modo_simple_igual_a_experto` | Mismos inputs por la capa simple o directamente en `comun`/`analisis` → métricas, tarjetas y restricciones idénticas |
| Override incompatible se rechaza | `T04.test_override_incompatible_se_rechaza`, `test_override_total_requiere_confirmacion` | Rubro de planta de alimento propia en C1 → OVERRIDE_INCOMPATIBLE (mensaje y alerta); override total sin confirmar → error; confirmado → SIMULACION_HIPOTETICA_OVERRIDE_TOTAL |
| NO_INVERTIR_AUN | `T05.*` | Capital USD 50 mil en la demo → SIN_INVERSION con SQ-1 y SQ-2, sin métricas ni ranking del status quo, texto «no un fracaso»; BALANCEADO sin pesos → PESOS_NO_DEFINIDOS (no NO_INVERTIR_AUN) |
| Comparabilidad | `T06.test_comparabilidad_se_respeta` | C0 vs variante incompleta → `comparable = FALSE`, sin decisiones ni Pareto; C0 vs C1 → comparable |
| Exportado / importado reproduce | `T07.*` | Exportar → importar → simular (con caché limpia) da lo mismo; versión de formato desconocida → rechazo |
| Simulación etiquetada | `T08.test_simulacion_queda_etiquetada` | Etiquetas del motor, alertas SIMULACION / SOLO_DEMOSTRACION, disclaimer en resultado y resumen HTML |
| Evidencia etiquetada | `T08.test_evidencia_queda_etiquetada` | Umbral E1–E3, 0 VAN publicables, precio «Validado» del usuario sigue siendo ESCENARIO_USUARIO en la traza |
| TIR rápida / completa | `T09.test_tir_rapida_y_completa_consistentes` | `calcular_tir=False` vs `True`: todas las métricas iguales salvo TIR (NO_CALCULADA en el modo rápido) |
| Errores manejables | `T10.*` | Escenario inválido → 400 con mensaje; excepción interna → 500 con referencia y sin traceback; ARS sin TC → 400; escala fuera de rango |
| Extras | `T11.*` | Capital vacío sin restricción (no USD 2 M); POTENCIAL no se vuelve ASEGURADA; presets sin valores; demo base = generador; caché no sirve otro escenario; costo unitario vía módulo 20 (NO_APLICA en C3); Monte Carlo simulado vs NO DISPONIBLE; tornado no calculable sin VAN |

## 2. Flujos HTTP (`tests/test_flujos.py`, 6 tests, servidor real en un hilo)

| Flujo | Recorrido |
|---|---|
| 1 | `GET /` → nuevo escenario → cargar objetivo, arquitectura, escala, demanda POTENCIAL y precio ESCENARIO → simular → tarjetas, qué hacer, disclaimer |
| 2 | demo → alternativas → comparar C0 vs C1 (comparable, VAN de ambas) |
| 3 | optimizar con capital USD 1,2 M: la restricción aparece, la mejor cumple el capital y hay alternativas excluidas por CAPITAL_DISPONIBLE |
| 4 | stress editable: alimento +25 % baja el VAN; magnitud vacía → NO_EJECUTADO_VALORES_PENDIENTES |
| 5 | guardar (la demo base es de solo lectura) → duplicar → renombrar → exportar JSON → importar → mismos resultados → CSV y resumen → eliminar |
| 6 | validación: 12 paquetes con pedidos, empates de prioridad conservados, progreso en 4 dimensiones |

## 3. Flujos en navegador (`tests/flujos_ui.mjs`, Playwright)

FLUJO 1 a 6 sobre la interfaz real (clics en el asistente, comparación, optimización con capital, stress, guardar/exportar/importar con descarga y carga de archivo, paquetes de validación) + NO_INVERTIR_AUN en pantalla + «¿Por qué?» + móvil (390 px sin scroll horizontal). Verifica además que ningún NO CALCULABLE se muestre como número y que no haya errores de JavaScript. Si Playwright no está instalado el runner informa OMITIDO (los flujos siguen cubiertos por HTTP).

## 4. Motor

La app no modifica el motor; sus suites propias se corren como siempre (`python3 00_gestion_proyecto/correr_suites_motor.py`, `21_modelo_financiero/modelo_financiero.py --solo-tests`, `22_riesgos/modelo_optimizador.py --solo-tests`).
