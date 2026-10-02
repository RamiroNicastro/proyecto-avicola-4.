# Planta de alimento balanceado: modelo conceptual y capacidad requerida

**Fecha:** 2026-10-01 · **Versión:** 1.1 (capacidad horaria con sus factores explícitos) · Sesión 14B · Modelo: [`modelo_upstream.py`](modelo_upstream.py) (bloque `6_planta_alimento`)

> **Conceptual.** Describe las etapas de una planta de alimento para pollo parrillero y calcula la **capacidad de producción requerida** (t/h de alimento terminado) para cada escala. **No** elige fabricante, tecnología, número de líneas ni proveedor (regla del proyecto y DEC-049), **no** decide construir la planta (DEC-024 abierta) y **no** contiene CAPEX ni OPEX. Las descripciones de etapas son de práctica general de la industria (fuentes comerciales y técnicas `[PVDP · débil]`, FTE-309) a validar con visitas (DPV-158).

---

## 1. Flujo del proceso

```
 Camión de grano / harina de soja / aceite / microingredientes
        │
 [1] RECEPCIÓN ── balanza, calado y muestreo, análisis rápido (humedad, micotoxinas, proteína),
        │          rechazo de lotes fuera de especificación, fosa de descarga, limpieza (zaranda, imán)
 [2] ALMACENAMIENTO DE MATERIAS PRIMAS ── silos (maíz, harina de soja), tanque (aceite),
        │          depósito (bolsas / big bags de minerales, premezcla, aminoácidos, aditivos)
 [3] MOLIENDA ── molino (martillos o rodillos) del maíz; define granulometría (impacta pellet y digestión)
        │
 [4] DOSIFICACIÓN ── tolvas de dosificación sobre balanzas: macro (maíz, soja), micro (premezcla,
        │          aminoácidos, aditivos, medicados), líquidos (aceite)
 [5] MEZCLADO ── mezcladora por lote (batch); tiempo y secuencia; limpieza / secuencia de fórmulas
        │          para evitar contaminación cruzada (medicados → retiro)
 [6] PELLETIZADO (si corresponde) ── acondicionamiento con vapor, prensa peletizadora;
        │          migaja (inicio) por desmenuzado del pellet; harina sin pellet como alternativa
 [7] ENFRIADO / SECADO ── enfriador del pellet (humedad y temperatura para almacenar);
        │          tamizado de finos (retornan al proceso); aceite post-pellet si se usa
 [8] ALMACENAMIENTO DE PRODUCTO TERMINADO ── celdas/silos por fórmula (inicio, crecimiento,
        │          terminación, retiro); identificación de lote y muestra de retención
 [9] DESPACHO ── carga a granel en camión tolva (o bolsas para inicio); balanza; documentación
                   de trazabilidad (lote, fórmula, fecha) → silos de granja
```

**Servicios auxiliares** (conceptuales): generador de vapor (para pellet), aire comprimido, energía eléctrica (molienda y pellet son los mayores consumos), control de polvo (riesgo de explosión de polvos orgánicos), laboratorio de control de calidad, sistema de control y trazabilidad, lavado/desinfección de camiones (bioseguridad de granja).

### 1.1 Decisiones técnicas abiertas (no se toman aquí)

| Tema | Opciones | Depende de | Registro |
|---|---|---|---|
| Forma física | Pellet + migaja (inicio) / harina | Nutricionista, desempeño (FCR), costo de energía | DEC-076 |
| Línea | Una línea / dos líneas (redundancia) | Escala, criticidad (sin alimento no hay crianza) | DEC-075 |
| Ubicación | Junto a la planta de faena / en zona de granos / cerca de las granjas | Localización (DEC-003), flujo de granos vs alimento | DEC-077 |
| Medicados | Elaborar o no alimentos con medicación | Registro SENASA, segregación, retiro | DPV-007 |
| Elaboración para terceros | Prestar servicio con capacidad no usada por la demanda propia | Mercado regional, habilitación | No se supone |

---

## 2. Capacidad requerida por escala

**Fórmula:** t/h requerida = t/semana plena × factor de pico / (días de fabricación × horas/día × eficiencia) × (1 + margen de capacidad).

| Factor | Valores del modelo | Clasificación | Efecto sobre la t/h |
|---|---|---|---|
| **Escala** (t/semana plena de alimento) | 62 / 124 / 247 / 494 t (medio, 5 d de faena); 81 / 162 / 324 / 647 t (desfavorable, 6 d) | `[ESTIMACIÓN]` de `03` | Proporcional |
| **Días de fabricación por semana** | 3 / 5 / 6 | `[SUPUESTO]` SUP-148 (escenario) | Inverso: 3 días exigen el doble de t/h que 6 |
| **Horas por día** | 8 / 16 | `[SUPUESTO]` SUP-148 | Inverso: un turno exige el doble que dos |
| **Eficiencia** (fracción de horas programadas con producción efectiva; también llamada utilización horaria) | 0,75 / 0,85 | `[SUPUESTO]` SUP-148, sin fuente | Inverso (±13 %) |
| **Margen de capacidad** | 15 % (10–20 %) | `[SUPUESTO]` SUP-146 | ×1,15 |
| Factor de pico | 1,0 (estacionalidad PENDIENTE) | `[SUPUESTO]` | Proporcional |

### 2.1 t/h de alimento terminado requeridas (rango por eficiencia 0,85–0,75; margen 15 %)

| Escenario de producción | Planta (aves faenadas/día) | t/semana plena | 3 d × 8 h | 3 d × 16 h | 5 d × 8 h | 5 d × 16 h | 6 d × 8 h | 6 d × 16 h |
|---|---|---|---|---|---|---|---|---|
| Medio, 5 d faena | 2.500 | 62 | 3,5–3,9 | 1,7–2,0 | 2,1–2,4 | 1,0–1,2 | 1,7–2,0 | 0,9–1,0 |
| Medio, 5 d faena | 5.000 | 124 | 7,0–7,9 | 3,5–3,9 | 4,2–4,7 | 2,1–2,4 | 3,5–3,9 | 1,7–2,0 |
| Medio, 5 d faena | 10.000 | 247 | 13,9–15,8 | 7,0–7,9 | 8,4–9,5 | 4,2–4,7 | 7,0–7,9 | 3,5–3,9 |
| Medio, 5 d faena | 20.000 | 494 | 27,9–31,6 | 13,9–15,8 | 16,7–19,0 | 8,4–9,5 | 13,9–15,8 | 7,0–7,9 |
| Desfavorable, 6 d faena | 2.500 | 81 | 4,6–5,2 | 2,3–2,6 | 2,7–3,1 | 1,4–1,6 | 2,3–2,6 | 1,1–1,3 |
| Desfavorable, 6 d faena | 20.000 | 647 | 36,5–41,3 | 18,2–20,7 | 21,9–24,8 | 10,9–12,4 | 18,2–20,7 | 9,1–10,3 |

`[ESTIMACIÓN]` · ESCENARIO. Resto en el CSV (bloque `6_planta_alimento`).

**De dónde salía el rango "~1–25 t/h" de la v1.0** (con la grilla de entonces: 5–6 días × 8–16 h, eficiencia 0,75–0,85, margen 15 %):

- **mínimo ≈ 0,9 t/h** = 2.500 aves/día, desempeño medio, 5 d de faena (62 t/semana) / (6 d × 16 h × 0,85) × 1,15;
- **máximo ≈ 24,8 t/h** = 20.000 aves/día, desempeño desfavorable, 6 d de faena (647 t/semana) / (5 d × 8 h × 0,75) × 1,15.

Con la grilla v1.1, que agrega la fabricación concentrada en 3 días, el rango se amplía a **~0,9–41 t/h**. **El rango no describe una incertidumbre de la planta: es el efecto combinado de escala, desempeño, días, horas, eficiencia y margen.** Para comparar opciones se debe fijar explícitamente cada factor.

### 2.2 Horas de producción por semana para la demanda propia

Con una planta de capacidad dada, las horas de fabricación necesarias son t/semana / (t/h × eficiencia). Ejemplo con las capacidades que cada escala requeriría a 5 d × 8 h (eficiencia 0,85, margen 15 %): 2,1 / 4,2 / 8,4 / 16,7 t/h.

| Demanda propia de… | Planta de 2,1 t/h | 4,2 t/h | 8,4 t/h | 16,7 t/h |
|---|---|---|---|---|
| 2.500 aves/día (62 t/semana) | 35 h (21 % de las 168 h) | 17 h (10 %) | 9 h (5 %) | 4 h (3 %) |
| 5.000 (124 t) | 70 h (41 %) | 35 h (21 %) | 17 h (10 %) | 9 h (5 %) |
| 10.000 (247 t) | 139 h (83 %) | 70 h (41 %) | 35 h (21 %) | 17 h (10 %) |
| 20.000 (494 t) | 278 h (> 168 h: no alcanza) | 139 h (83 %) | 70 h (41 %) | 35 h (21 %) |

`[ESTIMACIÓN]` (bloque `6_planta_horas` del CSV).

**Lectura (reformulada en v1.1):** con la demanda propia de 2.500 aves/día, una planta de una capacidad determinada tendría **baja utilización si se opera todos los días bajo la cadencia asumida**. No es por sí una conclusión negativa: la misma planta podría **fabricar menos días** (p. ej. 3 d × 8 h requieren 3,5–3,9 t/h), **concentrar lotes por fórmula**, **prestar servicio a terceros** (no se supone; requiere mercado y habilitación) u operar con **capacidad ociosa estratégica** como reserva para crecer. Cuál de esas alternativas tiene sentido es una pregunta económica y de mercado (fase CAPEX/OPEX; DEC-074, DEC-075).

- Las capacidades nominales de catálogo (t/h) suelen referirse a un producto y una forma (harina vs pellet) concretos; **no son capacidad del proyecto**. Comparar siempre en t/h de **pellet terminado** con la fórmula y el diámetro reales (DPV-158).
- La fabricación concentrada en pocos días aumenta el **inventario de alimento terminado** necesario para abastecer granjas que comen los 7 días ([`almacenamiento_silos.md` §5](almacenamiento_silos.md)).

### 2.3 Consumo de servicios y personal

**PENDIENTE.** Energía (kWh/t; molienda + pellet), vapor (kg/t), agua y dotación por turno requieren datos de proveedores o plantas en operación (DPV-158). No se estiman en esta fase.

---

## 3. Capacidad física asociada (dependencias)

| Elemento | Cómo se dimensiona | Dónde se calcula |
|---|---|---|
| Recepción de granos | t/semana de maíz + harina de soja (~56 / 111 / 223 / 445 t/semana medio) y camiones/semana (2 / 4 / 8 / 16 con un barrido de 28 t, SUP-096) | [`integracion_upstream.md` §4](integracion_upstream.md) y CSV bloque `10_logistica` |
| Silos de materias primas | consumo × días de stock / densidad | [`almacenamiento_silos.md`](almacenamiento_silos.md) |
| Celdas de producto terminado | ≥ 1 por fórmula (3–4) + días de stock | [`almacenamiento_silos.md`](almacenamiento_silos.md) |
| Despacho | t/semana plena / capacidad del granelero (3 / 5 / 9 / 18 viajes/semana con 28 t de escenario, SUP-096) | CSV bloque `10_logistica` |

## 4. Requisitos regulatorios a verificar

La elaboración de alimentos para animales requiere inscripción y registro ante SENASA (establecimiento y productos), con requisitos adicionales para alimentos medicados; también habilitaciones municipales, ambientales (polvo, ruido) y de seguridad (atmósferas explosivas). **Nada de esto se leyó en el original** (DPV-009): se registra como DPV-007.
