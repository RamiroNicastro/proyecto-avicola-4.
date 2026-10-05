# App V1 del proyecto avícola

**Versión:** 1.0.0 · **Fecha:** 2026-10-05 · **Sesión:** 22 · **Estado:** APP_V1_FUNCIONAL = SÍ · MOTOR_MODIFICADO = NO · RESULTADOS_REALES_PUBLICABLES = NO

Aplicación local para usar el Motor V1 (módulos `03`–`22`) sin editar CSV, JSON ni correr Python a mano. Tiene un **modo simple** (dueño, inversor, gerente) y un **modo experto** (todos los inputs del motor). Consume el contrato [`../00_gestion_proyecto/interfaz_app_v1.md`](../00_gestion_proyecto/interfaz_app_v1.md): la app **no calcula** (no tiene fórmulas de CAPEX, OPEX, finanzas ni riesgo), **no inventa datos** y **no modifica la evidencia**.

> Todo resultado depende de los datos y supuestos ingresados. No constituye una recomendación de inversión ni reemplaza validaciones técnicas, comerciales, fiscales o financieras. Hoy **0 de 42** corridas del modo evidencia tienen VAN publicable: todo número económico que muestre la app es una **simulación** (o la **demo ficticia**).

## Inicio rápido (un comando)

```
python3 app/app.py
```

Abre `http://127.0.0.1:8765/` en el navegador (o indica la URL). Requisitos: **Python 3.9+** y un navegador. **Sin dependencias externas** (biblioteca estándar; funciona offline).

| Acción | Cómo |
|---|---|
| Instalar | Nada que instalar: clonar / actualizar el repo |
| Ejecutar | `python3 app/app.py` (opciones: `--puerto 9000`, `--no-abrir`, `--host 127.0.0.1`) |
| Detener | `Ctrl+C` en la terminal |
| Actualizar | `git pull` en la raíz del repo y volver a ejecutar (la app lee los motores del repo en cada arranque) |
| Probar | `python3 app/tests/correr_tests.py` (`--sin-ui` para omitir el navegador) |
| Regenerar presets y demo | `python3 app/backend/generar_base.py` |

Primera vez: en INICIO, **Abrir demo** carga el escenario `DEMO_ARTIFICIAL` (datos **completamente ficticios**, rotulados SOLO_DEMOSTRACIÓN) para ver todas las funciones.

## Qué permite responder

| Pregunta | Dónde |
|---|---|
| «Tengo X capital, ¿qué alternativas puedo evaluar?» | SIMULAR paso 2 / OPTIMIZAR (capital → restricción HARD; vacío = sin restricción) |
| «Tengo X t/día de demanda, ¿qué escala tiene sentido simular?» | SIMULAR paso 3 (demanda por categoría) + OPTIMIZAR (consulta de demanda del motor) |
| «¿Qué pasa si el alimento sube / el precio baja?» | RIESGOS → ¿Qué pasa si…?, stress, 2D |
| «¿Qué configuración requiere menos inversión / tiene mayor VAN / menor riesgo?» | OPTIMIZAR (decisión por objetivo) y COMPARAR |
| «¿Cuánto capital de trabajo necesito?» | Tarjeta INVERSIÓN del resultado |
| «¿Qué tengo que validar antes de invertir?» | VALIDACIÓN (12 paquetes, prioridad del motor con empates) |
| «¿Por qué el sistema elige esta alternativa en este escenario?» | Botón «¿Por qué me da este resultado?» y explicación del optimizador |

## Documentación

| Documento | Contenido |
|---|---|
| [`arquitectura_app.md`](arquitectura_app.md) | Tecnología, capas, caché, performance, errores, versionado |
| [`guia_usuario_simple.md`](guia_usuario_simple.md) | Uso del modo simple paso a paso |
| [`guia_usuario_experto.md`](guia_usuario_experto.md) | Pestañas del modo experto, overrides, trazabilidad |
| [`contrato_backend.md`](contrato_backend.md) | API HTTP local (rutas, entradas, salidas, errores) |
| [`escenarios.md`](escenarios.md) | Formato JSON versionado, presets, demo, guardar / exportar / importar |
| [`evidencia_y_simulacion.md`](evidencia_y_simulacion.md) | Cómo se distinguen evidencia, simulación y pendiente; staging |
| [`tests_app.md`](tests_app.md) | Tests de backend, de flujo y de navegador |

## Estructura

```
app/
  app.py                  punto de entrada (servidor local)
  backend/                motor.py (carga de 19–22), escenario.py (formato y traducción simple→motor),
                          servicios.py (simular, comparar, optimizar, riesgo), presentacion.py (lenguaje simple),
                          proyecto.py (evidencia, validación, trazabilidad: solo lectura), almacen.py (escenarios y staging),
                          exportar.py (CSV y resumen imprimible), version.py, demo.py, generar_base.py, servidor.py
  web/                    index.html, css/, js/ (vistas por pantalla, gráficos SVG propios)
  escenarios_base/        presets estructurales (sin valores económicos) y DEMO_ARTIFICIAL
  tests/                  test_backend.py, test_flujos.py, flujos_ui.mjs, correr_tests.py
  datos_locales/          (no versionado) escenarios guardados, staging de cotizaciones, logs
```

## Límites actuales

Ver [`arquitectura_app.md`](arquitectura_app.md) §8. En síntesis: los límites del motor siguen vigentes (sin transiciones de arquitectura, sin días operativos arbitrarios, sin Monte Carlo del proyecto, sin resultados publicables en evidencia); la optimización completa de la demo tarda ~20 s; no hay PowerPoint ni usuarios múltiples.
