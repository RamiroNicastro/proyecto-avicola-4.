# 01 — Mercado

**Alcance:** mercado avícola argentino e internacional: producción, faena, consumo per cápita, exportaciones, precios (mayoristas, minoristas, al productor), estructura de la oferta y principales competidores.

**Preguntas clave**
- ¿Cuál es la evolución de la producción y el consumo de carne aviar en Argentina?
- ¿Cómo se forman los precios a lo largo de la cadena y cuál es su volatilidad?
- ¿Qué concentración tiene la oferta y qué espacio existe para un nuevo actor?

**Relacionado:** `02_clientes_demanda`, `17_exportacion`.

**Contenido**

| Archivo | Contenido |
|---|---|
| [`mercado_avicola_argentina.md`](mercado_avicola_argentina.md) | Radiografía del mercado 2026: tamaño, cadena de valor, geografía, productos, canales, precios, competencia, oportunidades, amenazas y control de calidad |
| [`datos_mercado.csv`](datos_mercado.csv) | Indicadores numéricos con fuente y clasificación (IDs `M###`) |
| [`competidores.md`](competidores.md) | Estructura competitiva y fichas de empresas |
| [`exportaciones.md`](exportaciones.md) | Serie de exportación, destinos, productos, estado de acceso a mercados e importaciones |
| [`conclusiones_mercado.md`](conclusiones_mercado.md) | Implicancias para el proyecto |

**Notas sobre `datos_mercado.csv`**

- Separador decimal: punto. Codificación UTF-8.
- Columnas: `id`, `categoria`, `indicador`, `anio`, `periodo`, `valor`, `unidad`, `base_definicion`, `ambito`, `fuente` (IDs `FTE-###` separados por `;`), `clasificacion` (`PENDIENTE DE VERIFICACIÓN DOCUMENTAL PRIMARIA` o `ESTIMACIÓN`; ninguna fila es `VERIFICADO` en la v2), `verificacion_documental`, `solidez` (media = fuente A/B coherente; baja = débil, parcial o contradictoria; derivada = estimación), `notas`.
- Excepciones: `valor` puede contener rangos (`700-800`) o listas separadas por `|` (M100, M102). En las filas `ESTIMACIÓN`, la fórmula está en `base_definicion`.
