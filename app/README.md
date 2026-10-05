# App V1 del proyecto avícola

**Versión:** 1.1.0 (corrección de UX profunda) · **Fecha:** 2026-10-05 · **Sesión:** 22 · **Estado:** APP_V1_FUNCIONAL = SÍ · APP_V1_INTUITIVA = SÍ · MOTOR_MODIFICADO = NO · RESULTADOS_REALES_PUBLICABLES = NO

Aplicación local para **entender el proyecto** (los 26 temas del estudio explicados en lenguaje simple) y **simular / tomar decisiones** con el Motor V1 (módulos `03`–`22`) sin editar CSV, JSON ni correr Python a mano. Pensada para alguien sin conocimientos de ingeniería, finanzas ni del proyecto; el **modo experto** (todos los inputs del motor) queda como opción avanzada. Consume el contrato [`../00_gestion_proyecto/interfaz_app_v1.md`](../00_gestion_proyecto/interfaz_app_v1.md): la app **no calcula** (no tiene fórmulas de CAPEX, OPEX, finanzas ni riesgo), **no inventa datos** y **no modifica la evidencia**.

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

Primera vez: la app ofrece **un recorrido de 2 minutos** sobre la demo `DEMO_ARTIFICIAL` (datos **completamente ficticios**, rotulados SOLO DEMOSTRACIÓN). En INICIO también están **Abrir la demo** y **Empezar un escenario vacío**.

## Qué permite responder

| Pregunta | Dónde |
|---|---|
| «¿Qué es este proyecto y cómo funciona el negocio?» | INICIO → ENTENDER EL PROYECTO (26 temas, 5 preguntas cada uno) y ¿Cómo funciona el negocio? (cadena clicable) |
| «¿Dónde podría estar la planta? ¿Qué pasa adentro? ¿Qué sale de un pollo?» | Pantallas visuales de localización, proceso y productos (sin ranking ni cifras inventadas) |
| «¿Dónde estamos parados?» | ¿Dónde estamos? (terminado / pendiente / simulable / no decidible) y Para seguir avanzando |
| «Tengo X capital, ¿qué alternativas puedo evaluar?» | SIMULAR pregunta 2 / OPTIMIZAR (capital → restricción HARD; vacío = sin restricción) |
| «Tengo X t/día de demanda, ¿qué escala tiene sentido simular?» | SIMULAR pregunta 3 (demanda y respaldo) + OPTIMIZAR (consulta de demanda del motor) |
| «¿Qué pasa si el alimento sube / el precio baja?» | RIESGOS → ¿Qué pasa si…?, stress, 2D |
| «¿Qué configuración requiere menos inversión / tiene mayor VAN / menor riesgo?» | OPTIMIZAR (decisión por objetivo) y COMPARAR |
| «¿Cuánto capital de trabajo necesito?» | Tarjeta INVERSIÓN del resultado |
| «¿Qué tengo que validar antes de invertir?» | QUÉ FALTA VALIDAR (checklist de 12 paquetes) y PARA SEGUIR AVANZANDO (prioridad del motor con empates) |
| «¿Por qué el sistema elige esta alternativa en este escenario?» | Resultado → VER DETALLES TÉCNICOS → «¿Por qué me da este resultado?» y explicación del optimizador |

## Documentación

| Documento | Contenido |
|---|---|
| [`arquitectura_app.md`](arquitectura_app.md) | Tecnología, capas, caché, performance, errores, versionado |
| [`guia_usuario_simple.md`](guia_usuario_simple.md) | Navegación, «Entender el proyecto», las 5 preguntas de la simulación, cómo leer el resultado |
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
                          estudio.py + estudio_contenido.py («Entender el proyecto»: módulos, cadena, localización,
                          proceso, productos, arquitecturas, escalas, glosario, estado, búsqueda; solo lectura),
                          servicios.py (simular, comparar, optimizar, riesgo), presentacion.py (lenguaje simple),
                          proyecto.py (evidencia, validación, trazabilidad: solo lectura), almacen.py (escenarios y staging),
                          exportar.py (CSV y resumen imprimible), version.py, demo.py, generar_base.py, servidor.py
  web/                    index.html, css/, js/ (router con migas de pan, buscador, recorrido guiado, vistas por pantalla,
                          markdown y gráficos SVG propios)
  escenarios_base/        presets estructurales (sin valores económicos) y DEMO_ARTIFICIAL
  tests/                  test_backend.py, test_flujos.py, test_ux.py, flujos_ui.mjs, correr_tests.py
  datos_locales/          (no versionado) escenarios guardados, staging de cotizaciones, logs
```

## Límites actuales

Ver [`arquitectura_app.md`](arquitectura_app.md) §8. En síntesis: los límites del motor siguen vigentes (sin transiciones de arquitectura, sin días operativos arbitrarios, sin Monte Carlo del proyecto, sin resultados publicables en evidencia); la optimización completa de la demo tarda ~20 s; no hay PowerPoint ni usuarios múltiples.
