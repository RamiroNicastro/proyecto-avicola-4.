# Requerimientos de información para cotización (RFQ futuro)

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A) · Fase 0 — **plantilla; no se envía todavía**

> **Alcance:** qué datos habrá que pedir a cada proveedor, para cada equipo o módulo, cuando la fase del proyecto habilite solicitar cotizaciones. Define una **base de diseño común** (para que las ofertas sean comparables), los **campos obligatorios** por equipo, los **lotes** (paquetes) de cotización y las **preguntas específicas** por grupo. **No** se envía ninguna solicitud, **no** se elige proveedor, **no** se fija escala.
> Toda respuesta se registrará como `[COTIZACIÓN]` con proveedor, fecha, validez, moneda, IVA, flete, instalación y condiciones (regla 4); los valores en ARS con tipo de cambio, fecha y fuente (regla 2).
> Equipos de referencia: [`matriz_equipos.csv`](matriz_equipos.csv). Proveedores relevados: [`proveedores_preliminares.md`](proveedores_preliminares.md).

---

## 1. Base de diseño a entregar a los proveedores (común a todos)

Para que las ofertas sean comparables, todos deben cotizar sobre la misma base. Valores **de escenario**, no decisiones:

| Parámetro | Valor para el RFQ | Origen |
|---|---|---|
| Escalas a cotizar | 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo (pedir la oferta para **al menos dos**, y cómo se amplía de una a la siguiente) | [`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) |
| Horas netas de faena | 8 h (sensibilidad 6 y 10 h); preguntar qué cambia con 16 h (dos turnos) | SUP-053; DEC-036 |
| Ritmo operativo requerido | 312 / 625 / 1.250 / 2.500 aves/h a 8 h | [`../05_proceso_industrial/cuellos_botella.md` §3](../05_proceso_industrial/cuellos_botella.md) |
| Peso vivo | Referencia 2,9 kg (escenarios 2,4 / 2,9 / 3,4 kg, SUP-027); **rango modelado en el balance: 2,2–3,5 kg** (el equipo debe declarar qué rango tolera sin ajuste) | SUP-027; balance v1.1 |
| Uniformidad de lotes | Desconocida: lotes de varios productores (pedir tolerancia a dispersión de peso) | DPV-044 |
| Productos | Entero, trozado (pechuga, pata-muslo, alas, esqueleto), deshuesado (suprema, solomillo, muslo), garras, menudencias; refrigerado y congelado; opción exportación | [`../06_productos/catalogo_productos.md`](../06_productos/catalogo_productos.md) |
| Enfriamiento | Cotizar **inmersión** y **aire** (y mixto si lo ofrecen) por separado | DEC-026 |
| Aturdido | Cotizar **eléctrico** y, si lo ofrecen, **CAS** | DEC-09A-05 |
| Estándar higiénico | Habilitación SENASA; indicar si el diseño cumple estándar UE | DEC-009, DEC-012 |
| Servicios disponibles | **Desconocidos** (sin localización): pedir consumos, no suponer disponibilidad | DEC-003 |
| Energía eléctrica | 380 V / 50 Hz trifásico (norma argentina) | Conocimiento general |

## 2. Campos obligatorios por equipo o módulo

Cada línea de la oferta debe completar:

| # | Campo | Unidad / detalle | Por qué se necesita |
|---|---|---|---|
| 1 | **Capacidad nominal** | aves/h, kg/h, piezas/h, envases/min | Comparación básica |
| 2 | **Capacidad real esperable** | Misma unidad, con la eficiencia o disponibilidad supuesta y **referencias de plantas** donde se midió | La nominal no es la real (SUP-09A-01) |
| 3 | Rango de producto | Peso mínimo/máximo, calibres, tipos de corte | Pesos variables en lotes argentinos |
| 4 | **Dimensiones** | Largo × ancho × alto (m), peso (kg), espacio de mantenimiento, cargas a piso/estructura | Layout futuro (no ahora) |
| 5 | **Potencia** | kW instalados y kW de consumo medio; tensión | Energía (`12_energia_frio`) |
| 6 | **Agua** | L/h o L/ave; temperatura; calidad; recirculación posible | `11_agua_efluentes` |
| 7 | **Aire comprimido** | Nm³/h y presión (bar); calidad | Compresores |
| 8 | **Vapor / agua caliente** | kg/h de vapor o kW térmicos; temperatura | Caldera |
| 9 | **Frío** | kW frigoríficos; temperatura de evaporación; refrigerante; agua helada/hielo | Sala de máquinas |
| 10 | **Efluente generado** | m³/h y carga orgánica estimada | Tratamiento |
| 11 | **Personal** | Operarios por turno para operar y para repaso; perfil de calificación | Dotación (`18_recursos_humanos`) |
| 12 | **Precio** | Por equipo y total; **moneda**; IVA; qué incluye | `19_capex` (no ahora) |
| 13 | **Incoterm** | EXW, FOB, CIF, DAP, DDP; puerto/lugar | Costo de importación |
| 14 | **Instalación** | Incluida o no; supervisión; obras civiles y servicios a cargo del comprador | Alcance real |
| 15 | **Puesta en marcha** | Duración, personal del proveedor, pruebas de aceptación (FAT/SAT) y criterio de capacidad garantizada | Responsabilidad de desempeño |
| 16 | **Capacitación** | Operadores y mantenimiento; duración; idioma | Operación |
| 17 | **Repuestos** | Lista recomendada para 1 y 2 años; repuestos críticos; **stock en Argentina**; tiempos de reposición | Riesgo de parada (§2.2 de [`catalogo_equipos.md`](catalogo_equipos.md)) |
| 18 | **Garantía** | Plazo, alcance, condiciones (uso de repuestos originales) | Riesgo |
| 19 | **Mantenimiento** | Plan preventivo, horas/semana, consumibles, contrato de servicio, soporte remoto | OPEX y ventana horaria |
| 20 | **Lead time** | Semanas de fabricación + transporte + montaje + puesta en marcha | Plan de etapas (DPV-086) |
| 21 | Servicio técnico local | Técnicos residentes en Argentina (cuántos, dónde), tiempo de respuesta garantizado | DPV-09A-02 |
| 22 | Tiempo de limpieza | Horas-persona y tiempo de desarme/limpieza por día; diseño higiénico | Ventana horaria (SUP-09A-02) |
| 23 | Ampliabilidad | Cómo se amplía a la escala siguiente: qué se mantiene, qué se agrega, qué se reemplaza | Modularidad ([`../05_proceso_industrial/arquitecturas_por_escala.md` §8](../05_proceso_industrial/arquitecturas_por_escala.md)) |
| 24 | Materiales y certificaciones | Acero inoxidable (tipo), plásticos aptos, seguridad eléctrica y de máquinas | Habilitación |
| 25 | Referencias | Plantas en Argentina o la región con el mismo equipo, visitables | Validación |
| 26 | Validez de la oferta | Fecha; ajuste de precio | Regla 4 |

## 3. Lotes de cotización (paquetes)

| Lote | Contenido (EQ de la matriz) | Proveedores candidatos a consultar (sin preferencia) |
|---|---|---|
| **L1 Recepción de vivo** | EQ-01 a EQ-06 | Integrales; fabricantes nacionales |
| **L2 Faena** | EQ-07 a EQ-20 (incluye aturdido eléctrico y CAS por separado) | Integrales; pequeña escala; nacionales; China; usados |
| **L3 Evisceración** | EQ-21 a EQ-33 (manual asistida, semiautomática y automática como alternativas) | Integrales; pequeña escala; China; usados |
| **L4 Enfriamiento** | EQ-34 a EQ-38 (inmersión, aire, mixto) | Integrales; nacionales |
| **L5 Clasificación, trozado y deshuese** | EQ-39 a EQ-46 | Integrales; especialistas de deshuese; usados |
| **L6 Coproductos** | EQ-47 (garras), EQ-48 (CMS), EQ-28 y EQ-33 (menudencias) | Integrales; especialistas |
| **L7 Packaging** | EQ-49 a EQ-56 | Fabricantes de packaging |
| **L8 Congelado y cámaras** | EQ-57 a EQ-65 | Fabricantes de congelado y frío industrial (`12_energia_frio`) |
| **L9 Subproductos y pretratamiento** | EQ-66 a EQ-70 | Integrales; proveedores de efluentes (`11_agua_efluentes`) |
| **L10 Servicios** | EQ-71 a EQ-76 | Proveedores de servicios industriales |
| **L11 Línea completa llave en mano** | L1–L5 integrados, con capacidad garantizada de la línea | Integrales; revendedores de líneas completas usadas |

## 4. Preguntas específicas por lote

| Lote | Preguntas adicionales |
|---|---|
| L1 | ¿Cajones o módulos? ¿Qué capacidad de camión supone? ¿Ventilación del andén para verano argentino? |
| L2 | Longitud de sangrado y escaldado para cada ritmo; parámetros de aturdido y cómo se verifica su eficacia; ¿cumple requisitos de bienestar de la UE? ¿Aptitud para requisitos Halal (métodos admitidos)? Recuperación de sangre sin dilución |
| L3 | Rango de peso sin recalibrar; % de rotura de vísceras esperado; presentación para inspección y **cuántos puestos de inspección** prevé para cada ritmo; bypass manual |
| L4 | Tiempo de residencia; temperatura final de carcasa; agua absorbida (%) en inmersión; pérdida (%) en aire; consumo de agua y frío por ave; cómo se amplía |
| L5 | Programas de corte disponibles; rendimiento de deshuese (% carne/hueso) medido; productividad manual equivalente; tiempo de cambio de programa |
| L6 | Rendimiento y grado de garras; capacidad de pelado; CMS: temperatura de salida y tiempo hasta congelado |
| L7 | Formatos (bolsa, bandeja, termosellado, termoformado, vacío, MAP); envases/min; tiempo de cambio de formato; vida útil lograda en aves por formato (referencias) |
| L8 | Tiempo de congelado hasta −18 °C en el centro por producto y envase; kg/h; kW frigoríficos; espacio; ampliación |
| L9 | Capacidad de bombas y tanques; tamices; almacenamiento por 24 h |
| L10 | Consumos simultáneos; redundancia N+1 |
| L11 | **Capacidad garantizada** de la línea en aves/h reales con pesos de 2,2–3,5 kg, penalidades, pruebas de aceptación, responsable único de integración |

## 5. Formato de comparación (neutral)

Las respuestas se cargarán en una tabla con **una fila por equipo y por proveedor**, con las columnas del §2 y una columna de "campos no respondidos". La comparación económica (CAPEX, OPEX, costo por ave) se hará en `19_capex` y `20_opex` **después** de validar demanda y escala, no en esta fase. Ninguna oferta debe usarse como dato `[VERIFICADO]` de capacidad real sin referencia de planta.
