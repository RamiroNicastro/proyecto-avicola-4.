# Arquitectura de la App V1

## 1. Tecnología

| Capa | Elección | Por qué |
|---|---|---|
| Backend | Python 3 **biblioteca estándar** (`http.server.ThreadingHTTPServer`, `json`, `csv`) | Los motores ya son Python: se importan directamente (sin duplicar fórmulas). Cero dependencias, offline, un comando |
| Frontend | HTML + CSS + JavaScript (módulos ES nativos), **sin frameworks ni CDN** | Funciona offline, mantenible, sin build |
| Gráficos | SVG propio (`web/js/graficos.js`) | Solo los útiles (cash flow, ingresos/OPEX/EBITDA, utilización, tornado, sensibilidad, 2D, Pareto, histograma de Monte Carlo, fondos, validación); un `null` nunca se dibuja como 0 |
| Persistencia | Archivos JSON en `app/datos_locales/` (no versionado) | Separado de la evidencia; exportable / importable |
| Tests | `unittest` (Python) + Playwright (Node, opcional) | Sin dependencias para los tests de backend |

El simulador HTML previo (`23_plan_expansion/simulador_html/`) **no** se usa como lógica: la única fuente de cálculo son los motores Python actuales.

## 2. Capas

```
NAVEGADOR (web/)            vistas: inicio · simular (modo simple) · comparar · optimizar · riesgos · validación · evidencia · experto
   │  fetch JSON
SERVIDOR (backend/servidor.py)   rutas /api/* ; errores → mensaje de usuario + log ; lock para las llamadas al motor
   │
SERVICIOS (backend/servicios.py) simular · comparar · optimizar · sensibilidad · tornado · 2D · stress · quiebres · Monte Carlo
   │      └─ presentacion.py (tarjetas, lenguaje simple, alertas)  · exportar.py (CSV, resumen HTML)
TRADUCCIÓN (backend/escenario.py) escenario de la app (simple + experto) → entrada del motor (escenario_optimizador.json + inputs de 22)
   │
MOTOR (sin cambios)   21 modelo_financiero: construir_entrada / simular / resultados / agregar / completitud
                      22 motor_riesgo: Evaluador / sensibilidad_oneway / tornado / sensibilidad_2d / correr_stress / punto_quiebre / monte_carlo
                      22 modelo_optimizador: alternativas_reales / correr_universo / consultas / limitacion_principal / que_hacer_ahora
                      20 modelo_opex: correr (solo para costear precios unitarios del modo simple, sobre una copia en memoria)
LECTURA DEL PROYECTO (backend/proyecto.py, solo lectura)  plan_validacion_final.md · prioridad_validacion.csv · que_hacer_ahora.csv ·
                      datos_por_validar.md · cobertura_motor.csv · trazabilidad_end_to_end.csv · base_precios_venta.csv · …
```

## 3. Flujo de una simulación

1. La interfaz envía el escenario de la app completo (`POST /api/simular`).
2. `escenario.validar()` controla la forma (formato y versión, tipos, rango de escala, categorías, estados de dato).
3. `escenario.a_motor()` aplica la capa simple sobre la experta (demanda, precios, capital, restricciones, objetivo) y arma el `escenario_optimizador` + los `inputs` de 22. Un dato «NO SÉ» no se envía (el motor lo informa PENDIENTE).
4. Con arquitectura y escala manuales se evalúa esa alternativa; en AUTO se corre el optimizador y se detalla la mejor del objetivo (o se muestra NO_INVERTIR_AUN / NO CALCULABLE / PESOS_NO_DEFINIDOS).
5. `servicios` corre `mopt.correr_universo` sobre la alternativa + el status quo (ficha, semáforo, robustez, restricciones, cobertura) y `mf.simular` + `mf.resultados(calcular_tir=True)` para el detalle (series anuales con `mf.periodos_reporte` + `mf.agregar`, traza, completitud, faltantes).
6. `presentacion` arma tarjetas: número solo si el flag `PUBLICABLE_*` del motor es TRUE; si no, **NO CALCULABLE** + qué falta (motivo del motor).

## 4. Caché (#45)

| Nivel | Clave | Invalidación |
|---|---|---|
| Evaluador del motor **por alternativa** (`mr.Evaluador`) | huella SHA-256 de lo que define esa alternativa: `comun` (con la capa simple aplicada) + su entrada de `por_alternativa` + plantilla + valores base + universo | Cambiar un input solo invalida las alternativas cuya huella cambia (p. ej. el CAPEX de C1-10000 no invalida C0) |
| Respuesta por operación | (operación, huella del escenario completo, parámetros) | Cualquier cambio del escenario cambia la huella: **nunca** se sirve el resultado de otro escenario |
| Cachés internos del motor (`mf._CACHE`) | configuración de CAPEX/OPEX | Funciones puras de la configuración (seguro) |
| Interfaz | resultados del escenario actual | Toda edición (`editar()`) descarta los resultados y marca «Los inputs cambiaron: vuelva a simular» |

## 5. Performance (#44)

- Evaluaciones de sensibilidad, stress, robustez y Monte Carlo usan el **modo rápido** del motor (`calcular_tir=False`, interfaz explícita de la sesión 20; sin monkeypatch). La TIR se calcula en las fichas, en el detalle del resultado y cuando la métrica pedida es TIR.
- Perfil de análisis **RÁPIDO** (SUP-240) en optimizar / comparar / simular: sensibilidad interna sobre `robustez.variables`; 2D, quiebres y Monte Carlo se piden en RIESGOS. Perfil **COMPLETO** en el modo experto.
- Referencias medidas (contenedor de desarrollo, DEMO con 20 alternativas completas): evaluación rápida ≈ 15 ms; con TIR ≈ 110 ms; optimizar ≈ 20 s (≈ 960 evaluaciones); simular una alternativa < 1 s; tornado de 45 variables ≈ 4 s; quiebres ≈ 5 s.

## 6. Errores (#46)

- Error de entrada (escenario inválido, ARS sin TC, escala fuera de rango, override total sin confirmar): HTTP 400 con `{codigo, mensaje}`.
- Rechazo del motor (`ErrorFinanciero`, `ErrorRiesgo`, `ErrorCapex`, `ErrorOpex`): HTTP 422 con un mensaje de usuario (`presentacion.mensaje_error_motor`) y referencia al log.
- Error inesperado: HTTP 500 «error interno (referencia X)»; el traceback va solo a `app/datos_locales/logs/app.log`. Nunca se muestra un traceback en la interfaz.
- Una alternativa que el motor no puede construir (p. ej. `OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA`) aparece con estado `ERROR_CONSTRUCCION`, alerta visible y mensaje claro; el resto sigue funcionando.

## 7. Versionado (#47)

La barra lateral y todo export muestran: **versión de la app** (`backend/version.py`), **versión de cada motor** (constantes `VERSION` de 19, 20, 21 y 22), **commit** y **fecha** (`git`), y un aviso si los archivos del motor tienen cambios locales sin commitear. Escenarios guardados y exportados llevan ese `sello`.

## 8. Limitaciones actuales

1. Límites del motor (interfaz_app_v1.md §6): sin transiciones de arquitectura (DEC-103), días operativos solo 250/300 (TF-001), recupero de IVA no parametrizable (TF-002), Monte Carlo del proyecto NO DISPONIBLE (DPV-180).
2. Sin datos reales: hoy ningún resultado del proyecto es publicable; la app lo dice. La demo es ficticia.
3. Optimización completa de muchas alternativas completas: 10–40 s (se muestra «calculando»). Sin cálculo en segundo plano ni cancelación.
4. Un solo usuario local; sin autenticación (servir solo en `127.0.0.1`). Las llamadas al motor se serializan.
5. Los precios unitarios de costo del modo simple solo cubren alimento comprado (ALI-A-PT), pollito comprado (POL-COMPRA) y façon de faena (FAE-FACON); el resto del OPEX se carga por rubro en el modo experto.
6. El objetivo BALANCEADO sin pesos: el motor devuelve NINGUNA + SQ-1; la app lo presenta como PESOS_NO_DEFINIDOS (TF-077).
7. DSCR mínimo incluye períodos de ramp-up (TF-078): la app muestra el valor del motor con su explicación.
8. Sin PowerPoint, sin informe de inversores: el resumen imprimible (HTML listo para PDF) es la base para la presentación futura.
