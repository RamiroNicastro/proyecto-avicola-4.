# 23 — Plan de expansión

**Alcance:** secuencia de etapas de crecimiento e integración vertical, evaluando para cada eslabón hacer / comprar / tercerizar / postergar, con condiciones de disparo para cada etapa.

**Relacionado:** DEC-002, DEC-033 a DEC-036, `19_capex`, `17_exportacion`.

## Contenido (modelo preliminar de escala, 2026-09-30)

| Archivo | Contenido |
|---|---|
| [`escenarios_escala.md`](escenarios_escala.md) | Definición de capacidad, calendarios, demanda vs capacidad, utilización, producción primaria, abastecimiento, balance de productos, configuraciones, subproductos, inventario, logística, exportación, tabla central "qué debe ser verdad", sensibilidad y documentación del modelo y del CSV |
| [`arquitectura_escalable.md`](arquitectura_escalable.md) | Modularidad (dimensionar / preparar / sobredimensionar), arquitecturas de crecimiento A–E y matriz de decisión sin ganador |
| [`gates_expansion.md`](gates_expansion.md) | Puertas G0–G3 y 18 variables medibles para ampliar (sin umbrales definitivos) |
| [`especificacion_simulador_html.md`](especificacion_simulador_html.md) | Especificación del futuro simulador HTML v0.1 (no construido) |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos de capacidad y escala; "¿por qué no construir directamente 20.000 aves/día?" |
| [`conclusiones_escala.md`](conclusiones_escala.md) | Hallazgos, información faltante priorizada, tests, calidad |
| [`modelo_escala.py`](modelo_escala.py) | Modelo reproducible: importa producción primaria v1.1, balance de masa v1.1 y subproductos v1.0 sin modificarlos; lee la demanda |
| [`escenarios_escala.csv`](escenarios_escala.csv) | Resultados en formato largo (archivo maestro de las cifras de escala) |

## Uso

```
python3 23_plan_expansion/modelo_escala.py                # tests + CSV
python3 23_plan_expansion/modelo_escala.py --solo-tests   # 17 pruebas
python3 23_plan_expansion/modelo_escala.py --tablas       # tablas de los .md
python3 23_plan_expansion/modelo_escala.py --mutaciones   # prueba de mutación (14)
python3 23_plan_expansion/modelo_escala.py --escenario --aves-dia 7500 --dias-semana 6 --utilizacion 0.6 --demanda ESC-BAS
```

Fórmulas, unidades, supuestos y columnas del CSV: docstring del script y [`escenarios_escala.md` §20](escenarios_escala.md). **Escenarios, no escala elegida**; sin CAPEX, OPEX ni precios.
