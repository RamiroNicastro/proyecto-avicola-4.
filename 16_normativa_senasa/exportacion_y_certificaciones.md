# Exportación y certificaciones — escalera regulatoria

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B · Relacionado: [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md) (requisitos de diseño por destino — **no se duplican aquí**), [`../17_exportacion/mercados_por_pais.md`](../17_exportacion/mercados_por_pais.md) (acceso por país, categorías A/B/C/D), [`mapa_regulatorio.md`](mapa_regulatorio.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv)

> Este archivo agrega el **procedimiento argentino** (SENASA, Aduana) y ordena la escalera. Todo es `[PVDP]` (acceso primario bloqueado, DPV-009).
> **Regla:** mercado abierto ≠ planta habilitada ≠ producto autorizado ≠ planta listada ≠ comprador ≠ operación (regla 17; [`../17_exportacion/conclusiones_exportacion.md`](../17_exportacion/conclusiones_exportacion.md)).

---

## 1. La escalera (cada peldaño exige el anterior)

| # | Peldaño | Qué significa | Quién decide | Qué se sabe | Estado |
|---|---|---|---|---|---|
| 1 | **Planta habilitada SENASA con tránsito federal** | Número de establecimiento, rubros habilitados, inspección oficial permanente | SENASA | Condición previa explícita del trámite de autorización de destino (FTE-09B-13) | `[PVDP]` |
| 2 | **País/mercado abierto** para carne aviar argentina | Protocolo o certificado sanitario acordado; estatus IAAP reconocido (país libre o regionalización) | País importador + SENASA/SAGyP | Situación por país en [`mercados_por_pais.md`](../17_exportacion/mercados_por_pais.md) | Nivel país |
| 3 | **Producto autorizado** para ese destino | El protocolo cubre ese producto (p. ej., garras, CMS, menudencias, cocidos); el producto está registrado en CAPA y dentro de los rubros de la planta | Importador + SENASA | Productos a exportar deben estar dentro de los rubros habilitados y registrados en CAPA (FTE-09B-13) | `[PVDP]` |
| 4 | **Establecimiento autorizado para el destino (SENASA)** y **listado por el importador** cuando corresponda | SENASA autoriza el destino (Res. 593/2026: procedimiento único digital; requisitos: sin deuda con SENASA, cumplimiento higiénico-sanitario y del destino, trazabilidad documentada, sin incumplimientos del Plan CREHA, proveedores con habilitación equivalente); el país importador puede exigir su propia lista (UE, China GACC, Japón, Corea, Arabia Saudita) | SENASA; autoridad extranjera | Res. 593/2026 reemplazó el sistema de 2010; las plantas ya autorizadas no deben re-solicitar; SENASA puede **suspender de inmediato** ante incumplimiento (FTE-083, FTE-09B-05) | `[PVDP]` |
| 5 | **Certificaciones adicionales** | Halal (organismo reconocido por el destino), atestaciones UE (antimicrobianos art. 118, bienestar), requisitos microbiológicos, BRCGS/IFS/FSSC si el comprador lo exige | Certificadoras; SENASA para atestaciones oficiales | Ver §3 | `[PVDP]` |
| 6 | **Comprador / importador** | Cliente con licencia de importación en destino, especificación y contrato | Mercado | No hay compradores identificados (DPV-032) | Sin evidencia |
| 7 | **Operación comercial** | Exportador inscripto en Aduana; certificado sanitario por embarque (SIGCER, firma electrónica con QR); despacho, flete reefer, cobro | ARCA/Aduana; SENASA; despachante | SIGCER para carne fresca aviar desde 2019-01-02; eliminación del "talón de exportación" en papel (FTE-09B-13); registro de importador/exportador con DJ 420/R y garantía/solvencia (FTE-09B-19) | `[PVDP]` |

**Tres errores a evitar:**
1. "Argentina recuperó la UE" **no** significa que la planta del proyecto pueda exportar a la UE: faltan los peldaños 3–7 para esa planta concreta.
2. "Tenemos tránsito federal" **no** es habilitación exportadora: es solo el peldaño 1.
3. "Tenemos Halal" **no** abre el Golfo: se necesita el país abierto (2), el producto (3), la autorización/listado (4) y un comprador (6).

## 2. Auditorías y listados

| Tipo | Quién audita | Cuándo | Impacto |
|---|---|---|---|
| Auditoría de SENASA para autorizar destino | SENASA (coordinación de exportaciones / regional) | Antes de autorizar y periódicamente | Planta "auditable" en todo momento; registros al día |
| Auditoría del país importador al sistema oficial | UE (DG SANTE), China (GACC), Japón, Corea, etc. | Periódicas o por reapertura; pueden visitar plantas seleccionadas | Una no conformidad puede afectar a la planta o a todo el país |
| Auditoría de certificadora Halal | Certificadora reconocida por el destino | Inicial y periódica; supervisión en faena | Personal y procedimientos específicos (DPV-034) |
| Auditoría de segunda parte (comprador) | Importador, retailer | Antes de contratar | Especificaciones, bienestar, HACCP |
| Certificación privada (BRCGS/IFS/FSSC) | Organismo de certificación acreditado | Anual | Costo y sistema de gestión |

## 3. Halal (cuando corresponda)

- La certificación debe emitirla un **organismo reconocido por el país importador** (p. ej., CIRA declara acreditación del GCC Accreditation Center); el **OAA** sería la autoridad técnica local reconocida por el IHAF; existe un **convenio de Cancillería** sobre certificaciones Halal y capacitaciones oficiales sobre un "nuevo sistema de acreditación Halal" (FTE-082, FTE-09B-18; `[PVDP]`). **No se identificó** la norma argentina que crea ese sistema.
- Requisitos de faena (aturdimiento, matarifes, oraciones, segregación): **no verificados en normativa oficial del destino** (DPV-034). Solo preservar la posibilidad (DEC-012).

## 4. Requisitos específicos por destino

No se repiten: ver [`../17_exportacion/requisitos_planta_exportadora.md` §2](../17_exportacion/requisitos_planta_exportadora.md). Novedad de esta sesión que **modifica** la lectura de ese archivo: el procedimiento de autorización de destinos ahora es el de la **Res. 593/2026** (ya citado allí) y la **Res. 592/2026** eliminó el Director Técnico obligatorio (ese archivo la citaba como "actualización" sin detalle). Se propone anotarlo en `17_exportacion` en la consolidación ([`actualizaciones_gestion_09B.md`](actualizaciones_gestion_09B.md) §6).

## 5. Qué hay que preguntar (resumen)

Lista completa en [`preguntas_senasa.md`](preguntas_senasa.md) §E. Principales: requisitos exactos de la Res. 593/2026 para una planta nueva; si SENASA puede evaluar el proyecto contra requisitos de un destino **antes** de construir; qué destinos exigen listado propio y auditoría previa; qué productos (garras, CMS, menudencias) están cubiertos por cada protocolo vigente; plazos típicos desde la habilitación federal hasta el primer certificado.
