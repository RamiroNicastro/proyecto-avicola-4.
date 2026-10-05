# Tests de la app

```
python3 app/tests/correr_tests.py            # backend + flujos HTTP + flujos en navegador (si hay Playwright)
python3 app/tests/correr_tests.py --sin-ui   # solo Python
```

Los tests usan una carpeta temporal para datos locales (`APP_AVICOLA_DATOS`) y nunca escriben en la evidencia. Resultado de la sesión 22 (v1.1, corrección de UX): **52/52 tests Python OK** (≈ 50 s) y **19/19 flujos de navegador OK** (Chromium headless). Suites del motor: todas OK (INT 70/70, 15/15 mutaciones), sin cambios en el motor.

## 1. Backend (`tests/test_backend.py`, 27 tests)

| # pedido | Test | Qué verifica |
|---|---|---|
| Escenario no modifica evidencia | `T01.test_escenario_no_modifica_evidencia`, `test_staging_no_es_evidencia` | SHA-256 de 10 archivos de evidencia iguales tras simular, stress, sensibilidad, guardar, importar y staging; staging sin nivel E |
| Pendientes no se muestran como 0 | `T02.*` | Escenario vacío: todo lo no calculable tiene `valor = None` y lista de faltantes; precio «No sé» no se envía y el VAN dice qué precio falta; el CSV marca NO_CALCULABLE |
| Simple = experto | `T03.test_modo_simple_igual_a_experto` | Mismos inputs por la capa simple o directamente en `comun`/`analisis` → métricas, tarjetas y restricciones idénticas |
| Override incompatible se rechaza | `T04.test_override_incompatible_se_rechaza`, `test_override_total_requiere_confirmacion` | Rubro de planta de alimento propia en C1 → OVERRIDE_INCOMPATIBLE (mensaje y alerta); override total sin confirmar → error; confirmado → SIMULACION_HIPOTETICA_OVERRIDE_TOTAL |
| NO_INVERTIR_AUN | `T05.*` | Capital USD 50 mil en la demo → SIN_INVERSION con SQ-1 y SQ-2, sin métricas ni ranking del status quo, texto «no un fracaso»; BALANCEADO sin pesos → simular y optimizar **no se ejecutan** (400 PESOS_NO_DEFINIDOS, nunca NO_INVERTIR_AUN); con pesos declarados sí |
| Comparabilidad | `T06.test_comparabilidad_se_respeta` | C0 vs variante incompleta → `comparable = FALSE`, sin decisiones ni Pareto; C0 vs C1 → comparable |
| Exportado / importado reproduce | `T07.*` | Exportar → importar → simular (con caché limpia) da lo mismo; versión de formato desconocida → rechazo |
| Simulación etiquetada | `T08.test_simulacion_queda_etiquetada` | Etiquetas del motor, alertas SIMULACION / SOLO_DEMOSTRACION, disclaimer en resultado y resumen HTML |
| Evidencia etiquetada | `T08.test_evidencia_queda_etiquetada` | Umbral E1–E3, 0 VAN publicables, precio «Validado» del usuario sigue siendo ESCENARIO_USUARIO en la traza |
| TIR rápida / completa | `T09.test_tir_rapida_y_completa_consistentes` | `calcular_tir=False` vs `True`: todas las métricas iguales salvo TIR (NO_CALCULADA en el modo rápido) |
| Errores manejables | `T10.*` | Escenario inválido → 400 con mensaje; excepción interna → 500 con referencia y sin traceback; ARS sin TC → 400; escala fuera de rango |
| Extras | `T11.*` | Capital vacío sin restricción (no USD 2 M); POTENCIAL no se vuelve ASEGURADA; presets sin valores; demo base = generador; caché no sirve otro escenario; costo unitario vía módulo 20 (NO_APLICA en C3); Monte Carlo simulado vs NO DISPONIBLE; tornado no calculable sin VAN |

## 1 bis. Corrección de UX (`tests/test_ux.py`, 19 tests)

| Grupo | Qué verifica |
|---|---|
| U01 Estudio | «Estudio completo» con los 26 temas; las 24 secciones de «Entender el proyecto»; cada módulo con 5 preguntas, etiquetas válidas, DPV existentes en el registro y documentos existentes; ningún dato rotulado VERIFICADO; cadena con 4 ramas; detalle técnico solo en lista blanca |
| U02 Localización | Mensaje «Todavía no existe una ubicación ganadora…», ranking NO_EMITIDO, 0 celdas verificadas, 13 regiones sin coordenadas ni puntajes, 11 gates duros/condicionales |
| U03 Proceso, productos, escalas, arquitecturas | Etapas en orden con equipos y capacidad y aviso de benchmark; kg/ave = balance del motor y aviso «no se suman»; escalas solo modeladas con «Capacidad no significa que vayamos a vender todo.»; C0–CF con nombres pedidos y definición exacta del CSV maestro |
| U04 Búsqueda y glosario | localización → localización, faena → proceso, agua, 10.000, CAPEX, pollitos, Chaco, halal; glosario > 300 términos con VAN…ramp-up; textos de KPI; estados en castellano sin códigos; PESOS_NO_DEFINIDOS ≠ NO_INVERTIR_AUN |
| U05 Estado y seguir | Semáforo MOTOR / FÍSICOS / ECONÓMICOS / EVIDENCIA 0 % / DECISIÓN; PRIORIDAD 1 — EMPATE con los mismos ítems que `prioridad_validacion.csv` |
| U06 BALANCEADO y DSCR | Bloqueo sin pesos y RIESGO_SIN_PESOS; DSCR del período mínimo = DSCR_MINIMO del motor, en ramp-up y sin afirmar impagabilidad; rutas nuevas responden |

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

19 flujos sobre la interfaz real; no puede haber errores de JavaScript. Si Playwright no está instalado el runner informa OMITIDO (los flujos de datos siguen cubiertos por HTTP). Con `UI_CAPTURAS=<carpeta>` guarda una captura de cada falla.

| Flujo | Criterio |
|---|---|
| FLUJO 1–6 | Asistente de 5 pasos («Paso X de 5», ATRÁS sin perder datos, «No sé» explicado) → resultado simple (frase, 1–6 números, faltantes en castellano y nunca como número, 4 acordeones); comparar; optimizar con capital; stress; guardar/exportar/importar; checklist de 12 paquetes (estado, a quién, qué pedir, unidad, por qué importa, qué desbloquea; nada marcado sin evidencia) |
| EXTRA | NO_INVERTIR_AUN («NO es un fracaso»); «DSCR mínimo del horizonte» con aviso de ramp-up y «?»; «¿Por qué?»; móvil 390 px sin scroll horizontal en inicio, localización, proceso y simular |
| NAV | Localización en 1 clic desde el inicio (≤ 3); proceso en 2 (≤ 3); estado en 1 (≤ 2); productos, faena y CAPEX en 2; migas de pan; «Volver al inicio» visible |
| BÚSQUEDA / DICCIONARIO | «localización» → localización, «faena» → proceso, «CAPEX» → CAPEX; diccionario buscable con estado vacío |
| BALANCEADO | Sin pesos SIMULAR deshabilitado + aviso; backend 400 PESOS_NO_DEFINIDOS; nunca se muestra NO_INVERTIR_AUN; REPARTIR POR IGUAL = 100 % habilita SIMULAR |
| USUARIO SIMPLE | En inicio, ficha de módulo, localización, proceso, productos, escalas, estado, seguir, validación y resultado simple: sin códigos técnicos ni rutas de archivo como texto principal (el código queda como dato secundario) |
| ESTADOS VACÍOS | Simular, comparar, riesgos y staging explican qué hacer y ofrecen una acción |
| ESTUDIO COMPLETO | Los 26 temas; la cadena responde al clic |
| RECORRIDO | Primer uso ofrece «¿QUERÉS UN RECORRIDO DE 2 MINUTOS?», la elección se recuerda; GUIARME recorre 6 pasos y termina en validación; EMPEZAR RECORRIDO abre la demo guiada |

### Criterios de usuario no técnico (#35)

| Sin modo experto, el usuario puede… | Cómo lo verifican los tests |
|---|---|
| explicar el proyecto | Inicio con la descripción + ENTENDER EL PROYECTO (U01, ESTUDIO COMPLETO) |
| encontrar localización / faena / productos / CAPEX | NAV (≤ 3 clics) y BÚSQUEDA |
| crear un escenario | FLUJO 1 (asistente de 5 pasos) |
| saber qué validar | FLUJO 6 (checklist) y U05 (para seguir avanzando) |
| distinguir real de simulado | Rótulos SIMULACIÓN / SOLO DEMOSTRACIÓN en cada resultado (FLUJO 1–2), semáforo «Decisión real NO DISPONIBLE» (NAV estado) |

## 4. Motor

La app no modifica el motor; sus suites propias se corren como siempre (`python3 00_gestion_proyecto/correr_suites_motor.py`, `21_modelo_financiero/modelo_financiero.py --solo-tests`, `22_riesgos/modelo_optimizador.py --solo-tests`).
