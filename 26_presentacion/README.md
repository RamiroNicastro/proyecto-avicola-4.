# 26 — Presentación / paquete ejecutivo V1

**Fecha:** 2026-10-05 · **Sesión:** 23 · **Estado:** paquete ejecutivo V1 construido. No crea motor, no agrega datos, no recomienda inversión.

**Alcance:** comunicar en lenguaje simple el estado del estudio (Motor V1 + App V1) a Ramiro, su familia, socios/inversores y, eventualmente, profesores. Toda cifra sale de documentos ya existentes del repositorio; esta carpeta **no es fuente primaria de ningún dato** (regla 13): la fuente de cada afirmación está en [`fuentes_y_trazabilidad_presentacion.csv`](fuentes_y_trazabilidad_presentacion.csv).

Mensaje que el paquete sostiene en todas sus piezas ([`../00_gestion_proyecto/auditoria_final_motor_v1.md`](../00_gestion_proyecto/auditoria_final_motor_v1.md) §30):

**MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO**

## Archivos

| Archivo | Qué es |
|---|---|
| [`presentacion_nicas_doipe_v1.pptx`](presentacion_nicas_doipe_v1.pptx) | Presentación de 29 láminas: 23 principales + anexo técnico (portada + 5 láminas). Notas del presentador en cada lámina |
| [`presentacion_nicas_doipe_v1.pdf`](presentacion_nicas_doipe_v1.pdf) | La misma presentación en PDF (exportada con LibreOffice; las notas no se incluyen) |
| [`guion_presentacion.md`](guion_presentacion.md) | Mensaje y notas del presentador de cada lámina + preguntas probables |
| [`resumen_ejecutivo_1_pagina.md`](resumen_ejecutivo_1_pagina.md) | Resumen de una página para leer o imprimir |
| [`fuentes_y_trazabilidad_presentacion.csv`](fuentes_y_trazabilidad_presentacion.csv) | Una fila por afirmación o cifra: lámina, valor mostrado, etiqueta, documento fuente, sección e IDs de registro |
| [`generar_presentacion.js`](generar_presentacion.js) | Generador del PPTX y del guion (contenido, diseño y notas en un solo lugar) |
| [`verificar_presentacion.py`](verificar_presentacion.py) | Verificación (solo biblioteca estándar): PPTX íntegro, notas en cada lámina, mensajes clave, sin placeholders ni rutas técnicas, sin montos ni rentabilidades, consistencia con la auditoría final y fuentes del CSV existentes. `python3 26_presentacion/verificar_presentacion.py` |
| [`capturas/`](capturas/) | 4 capturas reales de la App V1 v1.1.0 (inicio, simular, ¿dónde estamos?, qué falta validar), tomadas con Playwright sobre la app local |

## Estructura de la presentación

| Sección | Láminas |
|---|---|
| Mensaje | 1 Portada · 2 Mensaje ejecutivo · 3 Qué estamos intentando construir · 4 Cómo funciona el negocio · 5 Qué estudiamos |
| El negocio | 6 Demanda · 7 Alternativas C0–CF · 8 Escalas · 9 Planta y proceso · 10 Qué sale de un pollo · 11 Localización · 12 Terreno e infraestructura |
| Economía | 13 CAPEX · 14 OPEX y capital de trabajo · 15 Modelo financiero · 16 Riesgos y optimizador |
| App V1 | 17 Entender · 18 Modo simple y modo experto |
| Cómo seguir | 19 Qué falta validar · 20 Roadmap · 21 Decisiones abiertas · 22 Qué se puede decidir hoy · 23 Conclusión |
| Anexo técnico | 24 Portada · A1 Arquitectura de motores · A2 Evidencia · A3 Pruebas · A4 Tensiones · A5 Glosario |

## Etiquetas usadas en las láminas

| Etiqueta | Significado | Relación con las reglas del proyecto |
|---|---|---|
| EVIDENCIA | dato real con fuente verificada (E1–E3) | `[VERIFICADO]` / `[COTIZACIÓN]`; hoy prácticamente no hay |
| ESTIMACIÓN | cálculo del modelo, sin validar en campo | `[ESTIMACIÓN]` |
| ESCENARIO | hipótesis para simular; no es un dato | escenario del usuario / `SIMULACION_HIPOTETICA_NO_VALIDADA` |
| PENDIENTE | falta el dato o la decisión | `[PENDIENTE DE VALIDACIÓN]`, DPV o DEC abiertos |

En el CSV de trazabilidad, `ESTADO` identifica afirmaciones sobre el estado del proyecto (no son cifras de mercado) y `SUPUESTO` remite a `supuestos.md`.

## Controles aplicados

- Ningún monto total de CAPEX u OPEX: no se muestran ni siquiera los montos parciales E4 de [`../19_capex/`](../19_capex/conclusiones_capex.md) y [`../20_opex/`](../20_opex/conclusiones_opex.md).
- Ninguna rentabilidad (VAN, TIR, payback, EBITDA) publicada; las capturas de la app no muestran la demo ficticia ni resultados simulados.
- Ningún dato `[PVDP]` presentado como validado; las cifras físicas se rotulan ESTIMACIÓN.
- Los ~90 supermercados se presentan como demanda **potencial**; USD 2 M como capital de referencia **no comprometido**, nunca comparado contra un CAPEX.
- No se afirma que el proyecto convenga ni se recomienda inversión, arquitectura, escala, ubicación ni proveedor (fase 0, `estado_proyecto.md`).
- Se explica que el motor permite simular cuando se carguen datos (láminas 15–18).
- Gates de localización: el pedido de la sesión listaba «vecinos» y «logística» entre los gates duros; en el estudio son **condicionales** ([`../10_localizacion/conclusiones_localizacion.md`](../10_localizacion/conclusiones_localizacion.md) §4) y la lámina 11 sigue al estudio.
- «0 de 42» (app) y «0 de 61» (auditoría) no se contradicen: 61 corridas de referencia = 42 en modo evidencia + 19 plantillas de escenario, ninguna publicable (fila PR-036 del CSV).

## Cómo regenerar

Requisitos: Node 18+ con `pptxgenjs`, `react`, `react-dom`, `react-icons` y `sharp` instalados en alguna carpeta (no se versionan dependencias).

```
npm install --prefix /ruta/temporal pptxgenjs react react-dom react-icons sharp
NODE_PATH=/ruta/temporal/node_modules node 26_presentacion/generar_presentacion.js
```

Opcional: `APPLY_THEME=<ruta a apply_theme.js>` escribe los colores de la paleta en el tema del PPTX. PDF: `soffice --headless --convert-to pdf presentacion_nicas_doipe_v1.pptx` (requiere LibreOffice Impress; para que las medidas coincidan con Calibri, instalar la fuente métrica-compatible Carlito).

Las notas del presentador y [`guion_presentacion.md`](guion_presentacion.md) se generan del mismo texto: para cambiarlas, editar el script y regenerar. Si cambia el estado del motor o de la app, actualizar primero los documentos fuente y luego las filas del CSV de trazabilidad.

Las etiquetas de valores de los gráficos nativos usan el separador decimal de la configuración regional de PowerPoint.

**Capturas:** `python3 app/app.py --no-abrir`, luego Playwright (Chromium) a 1440×860 con escala 1,5 sobre `#/inicio`, `#/simular`, `#/estado` y `#/validacion`; se recortó la barra lateral.
