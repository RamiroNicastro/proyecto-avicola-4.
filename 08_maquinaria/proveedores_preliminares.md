# Proveedores y tecnologías — relevamiento preliminar

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A) · Fase 0 — **no se recomienda proveedor ni se ordena por preferencia**

> **Alcance:** fabricantes y revendedores de equipos de faena y procesamiento avícola (nacionales e internacionales) identificados en esta sesión, con país, líneas o equipos, rango de capacidad publicado, presencia en Argentina y servicio técnico **si pudo verificarse**. También el análisis conceptual de maquinaria nueva, usada y reacondicionada (§4). **No** hay precios ni CAPEX.
> **Verificación:** WebFetch y curl bloqueados (`EGRESS_BLOCKED`/403) en todos los sitios de fabricantes; **toda la información proviene de extractos de buscador** y queda `[PVDP]` (regla 16). Las capacidades son **nominales declaradas por el vendedor**, no capacidades reales (ver [`../05_proceso_industrial/cuellos_botella.md` §2](../05_proceso_industrial/cuellos_botella.md)). Fuentes: [`fuentes_09A.csv`](fuentes_09A.csv) (IDs provisionales FTE-09A-###).
> **Orden:** por categoría y alfabético dentro de cada una. El orden **no** implica preferencia.

---

## 1. Proveedores de líneas completas (internacionales)

| Proveedor | País (sede) | Líneas o equipos | Rango de capacidad publicado | Presencia en Argentina | Servicio técnico | Fuente | Estado |
|---|---|---|---|---|---|---|---|
| **BAADER** (incluye Linco) | Alemania / Dinamarca | Faena, evisceración, enfriamiento, trozado, deshuese; *Compact Plant* para plantas chicas; software de planta | Compact Plant: 600–1.600 aves/h; modelo 396: 1.600 aves/h preparado para 3.700 | **No verificada**; los extractos mencionan oficinas en México y Chile | Paquetes de servicio y repuestos (declarado); local **no verificado** | FTE-09A-007, FTE-09A-008 | `[PVDP]` |
| **Foodmate** (grupo Duravant; incluye Systemate) | Países Bajos / EE.UU. | Abridoras, evisceración, trozado, deshuese | Trozado hasta 6.000–7.200 aves/h; abridora hasta 9.000 aves/h; línea compacta de trozado de 3.000 aves/h (usada) | No verificada | No verificado | FTE-09A-016 | `[PVDP]` |
| **JBT Marel** (Marel, incluye Stork; fusión con JBT) | Islandia / Países Bajos / EE.UU. | Líneas completas: recepción, aturdido eléctrico y CAS, faena, evisceración, enfriamiento, clasificación, trozado (incl. compacto ACM-NT), deshuese, elaborados, congelado (Frigoscandia), software | Líneas desde ~500–1.000 aves/h iniciales hasta 15.000 aves/h | **Oficina de representación en Buenos Aires** (Maipú 267, CABA) según directorio de terceros; participación en ferias argentinas; **caso de cliente en Argentina** (Calisa2, Racedo, 9.500 → 15.000 aves/h) | Repuestos y servicio gestionados desde sucursales regionales (declarado); técnicos residentes **no verificados** | FTE-09A-003, FTE-09A-004, FTE-09A-005, FTE-09A-006, FTE-09A-023 | `[PVDP · débil]` para la oficina |
| **Meyn** | Países Bajos | Líneas completas; concepto modular *LEAP*; balanzas de línea | ~500 a > 8.000 aves/h; *LEAP* ampliable de 1.300 a 15.000 aves/h | Participación en **Avícola y Porcinos 2026** (Buenos Aires, nov-2026); oficina o representante **no verificado** | No verificado | FTE-09A-001, FTE-09A-002 | `[PVDP]` |
| **Prime Equipment Group** | EE.UU. | Máquinas individuales y sistemas para casi todas las etapas | No publicado en el extracto | No verificada | No verificado | FTE-09A-017 | `[PVDP · débil]` |
| **Sulmaq** (parte de Marel desde 2017) | Brasil | Principalmente bovinos y porcinos | — | — | — | FTE-09A-035 | `[PVDP · débil]`; sin línea avícola identificada |

**Contexto argentino:** una planta argentina difundida por el INTI declara tecnología holandesa y alemana (FTE-09A-032 `[PVDP]`), y SENASA informa ~60 plantas habilitadas de faena aviar (FTE-09A-031 `[PVDP]`, fecha del dato no identificada). **No se relevó** qué equipos usan esas plantas ni qué proveedor les da servicio: es la pregunta más útil para las visitas de campo (DPV-09A-02).

## 2. Proveedores de pequeña escala y especialistas

| Proveedor | País | Líneas o equipos | Capacidad publicada | Presencia en Argentina | Servicio técnico | Fuente | Estado |
|---|---|---|---|---|---|---|---|
| **BAYLE SA** | Francia | Líneas compactas de faena; evisceración semiautomática y automática (pollos, patos, pavos) | 150–1.500 aves/h | No verificada | No verificado | FTE-09A-015 | `[PVDP]` |
| **Cantrell-Gainco** | EE.UU. | Deshuese y trimming; distribuye TORIDAS en EE.UU. | — | No verificada | — | FTE-09A-018 | `[PVDP]` |
| **Engmaq** | Brasil | Abatederos modulares para cooperativas | ~40 aves/h | No verificada | — | FTE-09A-034 | `[PVDP · débil]`; muy por debajo de las escalas estudiadas |
| **Mayekawa (MYCOM)** | Japón | Deshuese automático: TORIDAS (pata-muslo entera), YIELDAS (pechuga); refrigeración industrial | TORIDAS Mark II: 1.000 piezas/h; Mark III anunciada: 1.500 piezas/h | No verificada (tiene red en América) | No verificado | FTE-09A-018 | `[PVDP]` |
| **Plant in a Box** | EE.UU. | Planta de faena en contenedor de 40' | ~500 aves/h (8–9 aves/min) | No verificada | — | FTE-09A-033 | `[PVDP · débil]` |

## 3. Packaging, congelado, fabricantes nacionales, China y usados

### 3.1 Packaging y congelado

| Proveedor | País | Equipos | Presencia en Argentina | Fuente | Estado |
|---|---|---|---|---|---|
| **GEA** | Alemania | Túneles de congelado (citado como fabricante difundido) | No verificada en esta sesión | FTE-09A-022 | `[PVDP · débil]` |
| **JBT Frigoscandia** (JBT Marel) | Suecia / EE.UU. | Espirales (GYRoCOMPACT), túneles | Ver JBT Marel | FTE-09A-022 | `[PVDP · débil]` |
| **MULTIVAC** | Alemania | Termoselladoras de bandejas, termoformadoras | No verificada en esta sesión | FTE-09A-021 | `[PVDP]` |
| **ULMA Packaging / Harpak-ULMA** | España (Harpak-ULMA en EE.UU.) | Film estirable, flow-pack horizontal y vertical, termoformado (MAP, vacío, skin), termoselladoras | Filial **no verificada** | FTE-09A-020 | `[PVDP]` |

### 3.2 Fabricantes argentinos

| Proveedor | Localidad | Equipos | Capacidad publicada | Servicio técnico | Fuente | Estado |
|---|---|---|---|---|---|---|
| **Ing. Galimberti y Cía.** | Argentina (localidad no verificada) | Descarga y lavado de jaulas, conteo, aturdido, degüello, canal de sangrado, escaldador automático (AISI 304, largo y vueltas según aves/h), desplumadoras, transportador aéreo, enfriadora, clasificadora, cinta de trozado; asesoramiento para plantas nuevas y ampliaciones | **No publicada** en el extracto (escaldador dimensionado a pedido) | Local (fabricante nacional); alcance no verificado | FTE-09A-009 | `[PVDP]` |
| **Avícola Rosarossa** | Argentina | Desplumadoras y artículos de faena de pequeña escala | Artesanal | — | FTE-09A-011 | `[PVDP]` |
| **Avícola Rovi** | Argentina | Peladora de 28 dedos (~60 pollos/h), escaldadora de 50 L | ~60 aves/h | — | FTE-09A-010 | `[PVDP]`; referencia de piso, fuera de escala |

**Brecha:** no se identificó en esta sesión un fabricante argentino con **evisceración automática**, trozado automático o deshuese automático; tampoco se descartó. La búsqueda debe continuar (cámaras sectoriales, ferias Avícola y Porcinos 2026, plantas en operación).

### 3.3 Fabricantes chinos (portales B2B)

| Proveedor | Líneas | Capacidad publicada | Posventa declarada | Fuente | Estado |
|---|---|---|---|---|---|
| **Henger Manufacturing (Shandong)** | Líneas de faena multiespecie | 500–1.000 aves/h | — | FTE-09A-014 | `[PVDP · débil]` |
| **Qingdao Raniche Machinery** | Líneas completas de faena y procesamiento | 500–1.000; 3.000; 5.000 aves/h | Instalación y posventa con ingenieros enviados; >60 países (declarado) | FTE-09A-012 | `[PVDP · débil]` |
| **XINBAIYUN / Eruis** | Líneas de faena y evisceración a pedido | 200–10.000 aves/h | Ingenieros para servicio en el exterior (declarado) | FTE-09A-013 | `[PVDP · débil]` |

Declaraciones de vendedores en portales B2B: **no** verificadas (referencias de clientes, cumplimiento de diseño higiénico, materiales, certificaciones eléctricas, repuestos en Argentina).

### 3.4 Revendedores de equipos usados y reacondicionados

| Proveedor | País | Oferta | Ejemplos publicados | Fuente | Estado |
|---|---|---|---|---|---|
| **Drobtech** | Polonia | Equipos usados de Meyn, Foodmate, Baader, Marel; restaurados o en estado actual; líneas modulares semiautomáticas | Línea de evisceración Linco de 4.000 aves/h; línea modular 500–2.000 aves/h | FTE-09A-019 | `[PVDP · débil]` |
| **Isotek** | Países Bajos | Equipos reacondicionados Stork, Linco, Meyn | Planta Meyn completa de hasta 3.000 aves/h ampliable a 6.000 | FTE-09A-036 | `[PVDP · débil]` |
| **Use Poultry Tech** | Países Bajos | Equipos usados y reacondicionados; depósito de 6.000 m² | Línea Linco preparada para 2.000–2.500 aves/h que operaba a 4.000–4.500 | FTE-09A-019 | `[PVDP · débil]` |

## 4. Maquinaria nueva vs usada vs reacondicionada (conceptual)

**No se ponen precios.** Valoración relativa `[SUPUESTO]` (SUP-09A-05): ▲ ventaja · ● intermedio · ▼ desventaja.

| Criterio | Nueva | Usada (en estado) | Reacondicionada (overhaul por revendedor o fabricante) |
|---|---|---|---|
| **CAPEX** (relativo) | ▼ mayor | ▲ menor | ● intermedio |
| **Repuestos** | ▲ disponibles del fabricante durante la vida del modelo | ▼ modelos discontinuados; piezas escasas; estado de desgaste desconocido | ● depende de la marca y del modelo; mejor si la marca sigue vigente |
| **Garantía** | ▲ del fabricante | ▼ ninguna o mínima | ● limitada del revendedor |
| **Integración** (sincronía entre equipos, controles, software) | ▲ una línea diseñada para el caso | ▼ equipos de distintas plantas, velocidades y pasos de grillete distintos | ● mejor si se compra una línea completa y probada |
| **Automatización y actualización tecnológica** | ▲ última generación (bienestar, higiene, datos) | ▼ tecnología de hace años; posibles brechas con requisitos UE | ● igual que usada, con componentes renovados |
| **Vida útil remanente** | ▲ completa | ▼ incierta | ● parcial |
| **Riesgo de parada** | ▲ menor (con curva de puesta en marcha) | ▼ mayor | ● intermedio |
| **Disponibilidad local de técnicos** | ● depende de la presencia del fabricante en Argentina | ▼ el fabricante puede no dar soporte a equipos no comprados a él | ● el revendedor suele estar en Europa |
| **Plazo de entrega** | ▼ fabricación a pedido (lead time a cotizar) | ▲ inmediato si está en stock | ● semanas de reacondicionamiento |
| **Importación a Argentina** | ● régimen general | **Régimen de bienes usados con requisitos específicos: no verificado** (DPV-09A-07) | Idem usados |
| **Ajuste a la escala** | ▲ se especifica | ▼ se adapta la planta al equipo disponible (p. ej., línea de 3.000 aves/h para una planta de 2.500 aves/día) | ● |
| **Habilitación SENASA / exportación** | ▲ diseño higiénico vigente | ▼ riesgo de materiales o diseños no aceptados | ● |

**Lecturas:**

1. **Lo usado es más atractivo** en equipos **simples y robustos** (tanques, escaldadoras, desplumadoras, transportadores, túneles estáticos, cámaras) y en **líneas completas probadas** de una misma marca vigente; **más riesgoso** en equipos **automáticos complejos** (evisceradoras, trozadoras, deshuesadoras, balanzas de línea), donde repuestos, calibración y técnicos definen la disponibilidad.
2. **Una línea usada "sobredimensionada"** (p. ej., 3.000 aves/h) puede cubrir varias escalas si los demás sistemas acompañan, pero condiciona el diseño del edificio al equipo y no a la estrategia.
3. **Mezclar nuevo y usado, o marcas distintas,** traslada al proyecto la responsabilidad de integración (sincronía, controles, garantía cruzada): exige un integrador técnico responsable.
4. **Ninguna de las tres opciones se descarta ni se elige** (DEC-09A-03). Se necesita: régimen de importación de bienes usados, tiempos de reposición de repuestos en Argentina, disponibilidad de técnicos y precios (`19_capex`).

## 5. Qué hay que verificar de cada proveedor (antes de cualquier comparación)

1. Representante o filial en Argentina: razón social, domicilio, técnicos residentes (cuántos, dónde), stock de repuestos en el país y tiempos de respuesta.
2. Plantas argentinas o de la región con sus equipos (referencias visitables).
3. Capacidad **real** sostenida en esas plantas (no la nominal).
4. Cumplimiento de requisitos de diseño higiénico y de bienestar (UE como referencia, DEC-012).
5. Condiciones de garantía, capacitación y contratos de servicio.
6. Formulario de datos: [`requerimientos_cotizacion.md`](requerimientos_cotizacion.md).
