# 08 — Maquinaria

**Alcance:** relevamiento de equipos y proveedores (nacionales e importados) para faena, procesamiento, frío, incubación, planta de alimento y granjas. Fichas técnicas y cotizaciones.

**Restricción Fase 0:** solo relevamiento; **no** se selecciona maquinaria ni proveedores. Toda cotización se etiqueta `[COTIZACIÓN]` con proveedor, fecha, validez y condiciones.

**Relacionado:** `05_proceso_industrial`, `19_capex`.

**Contenido (sesión 09A, 2026-09-30 — relevamiento conceptual, sin selección):**
- [`catalogo_equipos.md`](catalogo_equipos.md): equipos por etapa, comparaciones (aturdido, enfriamiento, packaging, congelado), criticidad (CRÍTICO / IMPORTANTE / SECUNDARIO), repuestos, redundancia, mantenimiento y dependencia de proveedor. Incluye el diccionario de columnas de la matriz.
- [`matriz_equipos.csv`](matriz_equipos.csv): 76 equipos conceptuales (EQ-01 a EQ-76) con alternativas, nivel de automatización a estudiar por escala, criticidad, bypass, servicios, mantenimiento y modularidad. Tabla curada (no generada por modelo); clasificación `[SUPUESTO]` SUP-09A-05.
- [`automatizacion_por_escala.md`](automatizacion_por_escala.md): manual vs mecanizado vs semiautomático vs automático por operación y por escala (arquitectura de referencia, sin umbral fijo de evisceración manual); cuándo automatizar no conviene.
- [`proveedores_preliminares.md`](proveedores_preliminares.md): fabricantes y revendedores nacionales e internacionales (BAADER CP396, Meyn LEAP y JBT Marel/Calisa2 como fuente primaria del fabricante; resto `[PVDP]`), nuevo vs usado vs reacondicionado; Calisa2 no es benchmark económico.
- [`requerimientos_cotizacion.md`](requerimientos_cotizacion.md): base de diseño común, **definición contractual de capacidad y condiciones de garantía** (dato crítico), 31 campos por equipo y 11 lotes de RFQ futuro (no enviado).
- [`fuentes_09A.csv`](fuentes_09A.csv): 36 fuentes nuevas con IDs provisionales (FTE-09A-001 a 036), mismo esquema que `25_fuentes/registro_fuentes.csv`, pendientes de reconciliación ([`../05_proceso_industrial/actualizaciones_gestion_09A.md`](../05_proceso_industrial/actualizaciones_gestion_09A.md)).
