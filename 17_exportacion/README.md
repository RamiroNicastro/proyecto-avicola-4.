# 17 — Exportación

**Alcance:** mercado internacional de carne aviar, mercados destino y acceso real para Argentina, requisitos sanitarios y comerciales por mercado, habilitaciones, productos exportables (incluidas garras y otras partes de baja demanda local), precios, logística y estrategia de valorización del ave.

**Relacionado:** `01_mercado`, `04_balance_masa`, `13_logistica`, `16_normativa_senasa`, `22_riesgos`, `23_plan_expansion`.

**Antecedentes:** serie de exportación argentina e importaciones en [`../01_mercado/exportaciones.md`](../01_mercado/exportaciones.md). La clasificación de acceso por país de ese documento queda **reemplazada** por [`mercados_por_pais.md`](mercados_por_pais.md) (2026-09-29).

## Contenido (v1, 2026-09-29)

| Archivo | Contenido |
|---|---|
| [`mercado_internacional.md`](mercado_internacional.md) | Producción y comercio mundial, productores, exportadores, importadores, evolución reciente, tendencias y ventajas de los líderes |
| [`mercados_por_pais.md`](mercados_por_pais.md) | Matriz de acceso para Argentina (A habilitado / B exportación efectiva / C potencial / D cerrado); secciones de China, mercados Halal y Unión Europea |
| [`productos_exportables.md`](productos_exportables.md) | Productos comercializados (mercados, formato, frío, requisitos) y precios internacionales de referencia |
| [`estrategia_valorizacion_ave.md`](estrategia_valorizacion_ave.md) | Ingreso total por ave: fórmula de net-back, restricciones, matriz producto–mercado, mapa conceptual de asignación |
| [`requisitos_planta_exportadora.md`](requisitos_planta_exportadora.md) | Requisitos obligatorios, por mercado y convenientes para la expansión |
| [`logistica_exportacion.md`](logistica_exportacion.md) | Flujo planta–importador, contenedor reefer, puertos (comparación conceptual), documentación, seguros, ciclo de caja |
| [`datos_exportacion.csv`](datos_exportacion.csv) | Indicadores numéricos con fuente y clasificación (IDs `E###`) |
| [`conclusiones_exportacion.md`](conclusiones_exportacion.md) | Respuestas, exportar vs local, riesgos, modelos A/B/C, información de campo, control de calidad |

## Notas sobre `datos_exportacion.csv`

- Separador decimal: punto. Codificación UTF-8. Delimitador: coma (campos con comas entre comillas).
- Columnas: `id`, `categoria`, `indicador`, `producto`, `origen`, `destino`, `anio`, `periodo`, `valor`, `unidad`, `base_definicion` (base del precio: FOB, CIF, mayorista interno; o fórmula si es estimación), `fuente` (IDs `FTE-###` separados por `;`), `clasificacion` (`PENDIENTE DE VERIFICACIÓN DOCUMENTAL PRIMARIA` o `ESTIMACIÓN`; ninguna fila es `VERIFICADO`), `verificacion_documental`, `solidez` (`media` = fuente A/B coherente; `baja` = débil, comercial o contradictoria; `derivada` = estimación), `notas`.
- Excepciones: `valor` puede contener rangos (`24-27`), desigualdades (`>10000`) o listas separadas por `;` cuando `periodo` u `origen` también lo están (ej.: E038, E065, E075).
- Unidades: t, Mt (millones de t), USD/t, EUR/100 kg, JPY/kg, %, días, TEU. Los valores en EUR y JPY no se convierten a USD (no se documentó tipo de cambio).
- **Los precios con solidez `baja` no deben usarse para modelar** (ver `productos_exportables.md` §2).
