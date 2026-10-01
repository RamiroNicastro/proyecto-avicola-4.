# Alimento: compra vs façon vs planta propia

**Fecha:** 2026-10-01 · **Versión:** 1.1 (façon con dos variantes de propiedad; capacidad horaria e inventarios corregidos) · Sesión 14B · Marco general del upstream: [`integracion_upstream.md` §2](integracion_upstream.md)

> **Marco de comparación, sin costos ni decisión.** DEC-024 (estrategia de alimento) sigue **abierta**. Las tres opciones son **escenarios de comparación** con el mismo estatus; la compra es solo el **benchmark de comparación**, no una preferencia. No se elige fabricante ni proveedor. La comparación económica (precio del alimento comprado vs costo de materias primas + elaboración + capital) requiere datos de campo (DPV-050, DPV-14B-03, DPV-14B-05) y corresponde a la fase de CAPEX/OPEX.

---

## 1. Las tres opciones

| | **A. Compra de alimento** (benchmark de comparación) | **B. Façon** (integración parcial; variantes B1 / B2) | **C. Planta propia** (integración total del eslabón) |
|---|---|---|---|
| Qué hace la empresa | Compra alimento terminado por fase, puesto en granja | Define la **fórmula** con su nutricionista y paga a un tercero por elaborar; **B1:** además compra las materias primas; **B2:** las compra el elaborador | Compra materias primas y elabora en su planta |
| Qué hace el tercero | Fórmula, compras, elaboración, entrega | Elaboración, almacenamiento (y a veces flete); en B2 también compra y mantiene las materias primas | — |
| Capacidad física propia | Recepción en granja (silos de granja) | Recepción en granja; en B1, stock **propio** de materias primas ubicado en el elaborador o acopio (sin silos propios) | Recepción y silos de granos, molienda, dosificación, mezcla, pellet, enfriado, celdas, despacho (~0,9–41 t/h según escala, desempeño, días, horas, eficiencia y margen, [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md)) |
| Flujos logísticos propios | Ninguno (lo entrega el proveedor) o retiro | B1: granos → elaborador (si la empresa contrata el flete); alimento → granjas | Granos → planta; alimento → granjas |
| t/año involucradas (medio, 5 d) | 3.091 / 6.181 / 12.362 / 24.724 t de alimento | Las mismas t de alimento; en B1, además ~2.780–22.250 t/año de maíz y harina de soja compradas por la empresa | Ídem façon |

## 2. Comparación por criterio

| Criterio | A. Compra | B. Façon | C. Planta propia |
|---|---|---|---|
| **Volumen** | Cualquier volumen si el proveedor tiene capacidad; a escala chica puede ser la única opción razonable | Requiere que el elaborador acepte el lote mínimo por fórmula | Requiere volumen estable; a 2.500 aves/día la demanda propia ocupa ~35 h/semana de una planta de 2,1 t/h: baja utilización **si se opera todos los días bajo la cadencia asumida**; podría fabricar menos días, concentrar lotes o servir a terceros ([`planta_alimento_conceptual.md` §2.2](planta_alimento_conceptual.md)) |
| **Calidad** | Fórmula y materias primas del proveedor; la empresa controla solo por resultado (FCR) y análisis | Fórmula propia; materias primas propias o controladas; proceso del tercero (pellet, limpieza) | Control total (y responsabilidad total) |
| **Dependencia** | Alta de un proveedor que puede ser **competidor** (integradoras con planta propia) | Media: elaborador + mercado de granos | Baja en elaboración; queda la de granos e insumos importados (premezcla, aminoácidos) |
| **Capital** | Ninguno en planta; capital de trabajo según plazo de pago | B1: capital de trabajo en materias primas propias (maíz + soja 15 d ≈ 119–954 t, micros aparte); B2: solo el alimento en granja ([`almacenamiento_silos.md` §5](almacenamiento_silos.md)) | CAPEX de planta + silos + capital de trabajo en granos y repuestos (no cuantificado) |
| **Flexibilidad** | Alta | Media | Baja (capacidad fija; ociosidad si cae la faena) |
| **Bioseguridad** | Camión del proveedor entra a las granjas; protocolos del proveedor | Ídem, o camión propio | Protocolos propios (lavado y desinfección de camiones, rutas) |
| **Know-how** | Compras y control de recepción | Nutrición (formulador), compra de granos, control de calidad | Todo lo anterior + operación y mantenimiento de planta, seguridad (polvo), registros SENASA |
| **Riesgo de suministro** | Ante escasez o conflicto, el cliente chico queda último | Riesgo de capacidad del elaborador | Riesgo de falla de equipo crítico (pellet, molino): sin alimento no hay crianza → redundancia |
| **Capacidad ociosa** | Ninguna | Ninguna | Depende de la cadencia de fabricación y de la rampa; puede ser estratégica (reserva) o usarse para terceros (no se supone) |
| **Trazabilidad / exportación** | Depende del proveedor | Buena | Plena |

## 3. Qué hace falta para comparar económicamente (no se hace aquí)

| Dato | Para qué | Registro |
|---|---|---|
| Precio del alimento por fase puesto en granja (fecha, moneda, IVA, flete) | Costo de A | DPV-050 |
| Tarifa de façon, lote mínimo, plazo y capacidad libre de elaboradores; **quién compra las materias primas y quién mantiene stocks**; servicio nutricional; mermas; frecuencia de producción | Costo de B, variante B1/B2 y viabilidad | DPV-14B-03 |
| Precio y flete de maíz, harina de soja, aceite, premezcla, aminoácidos; condiciones de contrato | Costo de B y C | DPV-050, DPV-14B-05 |
| Capacidad real, consumo de energía y vapor, dotación y eficiencia de plantas en operación | Costo operativo de C | DPV-14B-07 |
| CAPEX de planta por escala (fase CAPEX) | Inversión de C | Fase posterior (sin RFQ en esta fase) |
| Diferencia de desempeño (FCR) atribuible a la calidad del alimento | Beneficio de controlar la fórmula | DPV-044 |

**Regla de comparación propuesta** (para la fase económica): comparar **costo por kg de pollo vivo producido** (alimento × FCR), no costo por tonelada de alimento, porque una fórmula más cara puede mejorar el FCR. +0,1 de FCR = +5,9 % de alimento ([`../03_produccion_primaria/alimentacion.md` §1.4](../03_produccion_primaria/alimentacion.md)).

## 4. Señales a observar (sin umbrales numéricos todavía)

- **Señales hacia comprar:** escala chica, demanda no validada, proveedor confiable con capacidad libre que no compite en el mismo canal, falta de nutricionista y de capital.
- **Señales hacia façon:** se quiere controlar fórmula y compra de granos sin CAPEX; existe un elaborador con capacidad libre en el radio; volumen intermedio.
- **Señales hacia planta propia:** volumen estable que llena al menos un turno, localización en zona de granos, capital disponible, know-how incorporado, proveedores de alimento que son competidores o poco confiables.

Umbral de volumen a partir del cual conviene cada opción: **PENDIENTE** (requiere costos; DEC-14B-01).
