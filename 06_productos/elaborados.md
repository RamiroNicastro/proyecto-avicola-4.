# Elaborados de pollo — análisis conceptual

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance:** qué elaborados podrían absorber partes del ave y con qué complejidad, sin definir una línea (DEC-030), sin precios (SUP-018) ni maquinaria. La demanda de elaborados del proyecto **no está validada** (DPV-079). Atributos por producto en [`matriz_productos.csv`](matriz_productos.csv) (PRD-22 a PRD-28).
> **Restricción normativa clave (a verificar):** la CMS solo puede usarse como ingrediente de **chacinados cocidos y conservas** (Res. SENASA 368/2003, FTE-185 `[PVDP]`; SUP-048). Por eso la capacidad de un elaborado para "absorber" CMS depende de si es un producto cocido.

---

## 1. Para qué sirve un elaborado en este proyecto

1. **Absorber partes o fracciones con menor salida** (recortes, solomillo, muslo deshuesado, piel, CMS) y convertirlas en productos de mayor precio por kg.
2. **Equilibrar el mix** cuando la demanda de un corte (p. ej. pechuga para milanesas) no coincide con la proporción natural del ave ([`../02_clientes_demanda/supermercados.md` §2](../02_clientes_demanda/supermercados.md)).
3. **Diferenciar marca** y alargar vida útil (congelados).

Pero un elaborado **no crea masa**: usa la misma carne que podría venderse como corte. Solo mejora el ingreso por ave si `precio neto del elaborado × kg de carne usada − costo de ingredientes, proceso, envase y frío > precio neto de la carne vendida como corte` (ver [`../07_subproductos/guia_ramiro.md` §7](../07_subproductos/guia_ramiro.md)).

## 2. Análisis por elaborado

Materia prima por ave disponible (2,9 kg, configuración C, masa biológica): suprema 0,478 · solomillo 0,118 · muslo deshuesado 0,242 · recortes 0,037 · piel 0,110 · CMS 0,236 (si el esqueleto va a CMS).

| Elaborado | Materia prima principal | Capacidad de absorber recortes y fracciones | Valor agregado relativo | Complejidad | Inversión adicional (relativa, sin cotizar) | Canal comercial potencial | Vida útil |
|---|---|---|---|---|---|---|---|
| **Milanesas** (rebozado crudo) | Suprema fileteada; muslo deshuesado | Baja–media: requieren piezas enteras laminadas; recortes solo en milanesas "formadas" | Alto | Media–alta: rebozado, alérgenos (gluten, huevo), rotulado | Media: sala fría de elaboración, rebozadora/empanadora, envasado, congelado | Supermercados, carnicerías (incluida la familiar), gastronomía | Días (refr.) / meses (cong.) |
| **Hamburguesas** | Muslo deshuesado, recortes, piel (con límite de grasa) | **Alta** para recortes y piel; **CMS no** si el producto es crudo (SUP-048) | Medio–alto | Media: picado, mezcla, formado, congelado | Media | Supermercados, gastronomía, institucional | Meses (cong.) |
| **Nuggets / formados rebozados precocidos** | Pechuga, solomillo, recortes; CMS solo si el producto se clasifica como cocido (DPV-074) | Alta | Alto | **Muy alta**: formado, pre-enharinado, rebozado, **prefritura**, congelado IQF; control térmico | **Alta**: línea continua y escala mínima elevada | Supermercados, cadenas de comida rápida, gastronomía | Meses (cong.) |
| **Medallones** (formados, empanados o no) | Muslo, recortes, piel | Alta | Medio | Media | Media | Supermercados, institucional | Meses |
| **Marinados** (crudos, condimentados) | Pata-muslo, muslo deshuesado, alas, pechuga | Baja (usan piezas enteras); valorizan alas y pata-muslo | Medio | Media: inyección o masajeo, envasado | Baja–media | Supermercados, gastronomía | Días (según envase) |
| **Productos cocidos** (pechuga cocida, desmechado, arrollados cocidos) | Pechuga, muslo; CMS en cocidos | Media | Muy alto | **Muy alta**: cocción, enfriamiento rápido, zona de alto riesgo, *Listeria* | **Alta**: separación de zonas cruda/cocida | Supermercados, gastronomía, institucional; exportación a largo plazo (Japón, UE) | Según proceso (DPV-078) |
| **Embutidos cocidos** (salchichas de pollo) | **CMS**, piel, recortes | **Muy alta**: es el uso natural de la CMS | Medio | Alta: emulsión, embutido, cocción | Alta | Supermercados, industria | Semanas (a verificar) |
| **Congelados** (cualquiera de los anteriores, o cortes IQF) | Todas | — | Medio (estabilidad, alcance geográfico) | Media: túnel o IQF, cámara | Media–alta (frío) | Todos; exportación | Meses |

## 3. Lecturas

- Los elaborados que **mejor absorben recortes y piel** (hamburguesas, medallones) son de valor medio; los que **mejor absorben CMS** son los **cocidos** (embutidos), de mayor complejidad y escala industrial distinta a la de una planta de faena.
- **Milanesas** y **marinados** son los de **menor barrera** y se vinculan con la carnicería familiar y los supermercados, pero **no absorben** CMS y poco de los recortes: usan cortes que ya tienen salida.
- **Nuggets y cocidos** compiten con marcas establecidas e importados de Brasil (prefritos, FTE-075 `[ESTIMACIÓN]`) y requieren habilitaciones y controles específicos: se consideran **opciones de etapa posterior**.
- Una alternativa a la línea propia es la **elaboración a façon** o la **venta de insumos** (CMS, recortes, muslo deshuesado) a elaboradores: debe relevarse su disponibilidad y condiciones (DPV-079).

## 4. Qué no se decide

No se define línea, capacidad, maquinaria ni etapa de elaborados; no se afirma demanda. La decisión (propia / a façon / venta de insumos / ninguna) queda en **DEC-030**, dependiente de DEC-005, DPV-037, DPV-040 y DPV-079.
