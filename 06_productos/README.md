# 06 — Productos

**Alcance:** portafolio de productos (pollo entero, trozado, menudencias comercializables, elaborados), especificaciones, presentaciones, vida útil, precios de referencia por producto.

**Relacionado:** `02_clientes_demanda`, `04_balance_masa`, `07_subproductos`, `17_exportacion`, DEC-005, DEC-030.

## Contenido (2026-09-30)

| Archivo | Contenido |
|---|---|
| [`catalogo_productos.md`](catalogo_productos.md) | Productos de mercado interno, conexión parte → producto → mercado de exportación, garras, menudencias y CMS |
| [`elaborados.md`](elaborados.md) | Milanesas, hamburguesas, nuggets, medallones, marinados, cocidos, embutidos y congelados: materia prima, absorción de recortes, complejidad, canal |
| [`matriz_productos.csv`](matriz_productos.csv) | Archivo maestro de atributos de 30 productos |

Inventario completo de salidas del ave (incluye subproductos): [`../07_subproductos/mapa_subproductos.md`](../07_subproductos/mapa_subproductos.md).

## Documentación de `matriz_productos.csv` (regla 15)

- **Separador decimal:** punto. **Codificación:** UTF-8. Campos con comas entre comillas.
- **kg_ave:** masa biológica por ave de la materia prima disponible (pollo de 2,9 kg vivo en planta, rendimiento y condenas "medio", chiller por inmersión; sin el agua retenida). "-" = producto elaborado sin kg directo por ave. **Es la masa disponible, no una venta ni una demanda.**
- **ref_modelo:** de dónde sale kg_ave en el balance v1.1 (formato descripto en [`../07_subproductos/modelo_subproductos.py`](../07_subproductos/modelo_subproductos.py)); el test S08 de ese script falla si kg_ave difiere del balance en más de 0,0006 kg.
- **nivel_procesamiento:** 1 faena y enfriado · 2 trozado/bandeja/congelado simple · 3 deshuese, pelado o separación mecánica · 4 transformación en frío · 5 proceso térmico.
- **valor_agregado_relativo:** ordinal cualitativo (bajo / medio / alto / muy alto) entre productos del catálogo; **no es precio ni margen** (SUP-047).
- **vida_util:** categorías (SUP-051); refrigerado a determinar (DPV-078).
- **estado_demanda:** toda la demanda es no validada (categorías C/D del modelo de demanda) o, para exportación, nivel ≤ 2 (SUP-022).
- **Fuentes:** las citadas en cada celda (IDs de `25_fuentes/registro_fuentes.csv`); los precios mencionados son `[PVDP · débil]` y no se usan para calcular (SUP-018).
