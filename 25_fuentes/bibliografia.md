# Bibliografía

Listado de referencias consultadas, agrupadas por tipo. Cada entrada debe corresponder a un ID de [`registro_fuentes.csv`](registro_fuentes.csv), que es el registro maestro (fecha de consulta, URL, confiabilidad, uso).

Formato sugerido: `FTE-### — Autor/Organismo (año). Título. Editorial/Sitio. URL. Consultado AAAA-MM-DD.`

## Organismos oficiales argentinos
_(SENASA, Secretaría de Agricultura, Ganadería y Pesca, INTA, INTI, INDEC, organismos provinciales)_

Sin entradas todavía.

## Organismos internacionales
_(FAO, USDA, OMSA/WOAH, Codex Alimentarius)_

Sin entradas todavía.

## Documentación técnica
_(manuales de líneas genéticas, fabricantes, normas, papers)_

Sin entradas todavía.

## Cámaras sectoriales y fuentes comerciales
_(uso complementario; identificar como tales)_

Sin entradas todavía.

## Cotizaciones
_(proveedor, fecha, validez; archivos en la carpeta temática correspondiente)_

Sin entradas todavía.

---

## Campos de `registro_fuentes.csv`

| Campo | Contenido |
|---|---|
| `id` | `FTE-###`, correlativo |
| `tipo_fuente` | `oficial_ar` · `internacional` · `tecnica` · `sectorial` · `comercial` · `cotizacion` · `entrevista` |
| `categoria_confiabilidad` | `A` organismo oficial o documentación técnica primaria · `B` cámara sectorial, estudio académico o consultora identificada · `C` prensa, fuente comercial o dato informal |
| `fecha_consulta` | `AAAA-MM-DD` |
| `carpetas_relacionadas` | Carpetas separadas por `;` (ej. `01_mercado;21_modelo_financiero`) |
| `datos_extraidos` | Resumen breve de las cifras tomadas de la fuente |
