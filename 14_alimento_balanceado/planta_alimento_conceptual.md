# Planta de alimento balanceado: modelo conceptual y capacidad requerida

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B · Modelo: [`modelo_upstream.py`](modelo_upstream.py) (bloque `6_planta_alimento`)

> **Conceptual.** Describe las etapas de una planta de alimento para pollo parrillero y calcula la **capacidad de producción requerida** (t/h de alimento terminado) para cada escala. **No** elige fabricante, tecnología, número de líneas ni proveedor (regla del proyecto y DEC-049), **no** decide construir la planta (DEC-024 abierta) y **no** contiene CAPEX ni OPEX. Las descripciones de etapas son de práctica general de la industria (fuentes comerciales y técnicas `[PVDP · débil]`, FTE-14B-005) a validar con visitas (DPV-14B-07).

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
| Forma física | Pellet + migaja (inicio) / harina | Nutricionista, desempeño (FCR), costo de energía | DEC-14B-03 |
| Línea | Una línea / dos líneas (redundancia) | Escala, criticidad (sin alimento no hay crianza) | DEC-14B-02 |
| Ubicación | Junto a la planta de faena / en zona de granos / cerca de las granjas | Localización (DEC-003), flujo de granos vs alimento | DEC-14B-04 |
| Medicados | Elaborar o no alimentos con medicación | Registro SENASA, segregación, retiro | DPV-14B-06 |
| Elaboración para terceros | Vender capacidad ociosa | Mercado regional, habilitación | No se supone |

---

## 2. Capacidad requerida por escala

**Fórmula:** t/h requerida = t/semana plena × factor de pico / (días de operación × horas/día × eficiencia) × (1 + margen de capacidad).

- **t/semana plena:** de `03` (alimento entregado a granja; [`demanda_alimento.md`](demanda_alimento.md)).
- **Días y horas de operación:** 5 o 6 días × 8 o 16 h (SUP-14B-07; **escenario**, no turno elegido).
- **Eficiencia:** 0,75–0,85 = fracción de las horas programadas con producción efectiva (cambios de fórmula, limpiezas, arranques, mantenimiento menor; SUP-14B-07, sin fuente).
- **Margen de capacidad:** 15 % (SUP-14B-05; barrido 10–20 %): reserva de diseño, no óptimo.
- **Factor de pico:** 1,0 (la semana plena ya es el ritmo nominal); estacionalidad del consumo (verano/invierno) **PENDIENTE**.

### 2.1 t/h de alimento terminado requeridas (perfil y desempeño medios, 5 d de faena; rango por eficiencia 0,85–0,75)

| Planta (aves faenadas/día) | t/semana plena | 5 d × 8 h | 5 d × 16 h | 6 d × 8 h | 6 d × 16 h |
|---|---|---|---|---|---|
| 2.500 | 62 | 2,1–2,4 | 1,0–1,2 | 1,7–2,0 | 0,9–1,0 |
| 5.000 | 124 | 4,2–4,7 | 2,1–2,4 | 3,5–3,9 | 1,7–2,0 |
| 10.000 | 247 | 8,4–9,5 | 4,2–4,7 | 7,0–7,9 | 3,5–3,9 |
| 20.000 | 494 | 16,7–19,0 | 8,4–9,5 | 13,9–15,8 | 7,0–7,9 |

`[ESTIMACIÓN]` · ESCENARIO. **Cota alta** (desempeño desfavorable y 6 días de faena: 81 / 162 / 324 / 647 t/semana): 3,1 / 6,2 / 12,4 / 24,8 t/h con 5 d × 8 h y eficiencia 0,75; 1,1 / 2,3 / 4,6 / 9,1 t/h con 6 d × 16 h y 0,85.

**Lectura:**
- El rango de capacidad requerida va de **~1 t/h** (2.500 aves/día, dos turnos) a **~25 t/h** (20.000, desfavorable, un turno): **más de un orden de magnitud**. La elección de turnos mueve la capacidad tanto como duplicar la escala.
- Las capacidades nominales que publican los fabricantes (t/h "de catálogo") suelen referirse a un producto y una forma (harina vs pellet) concretos; **no son capacidad del proyecto**. Comparar siempre en t/h de **pellet terminado** con la fórmula y el diámetro reales (DPV-14B-07).
- **Capacidad ociosa:** con margen de 15 % la utilización de diseño es 1 / 1,15 ≈ 87 % de las horas programadas; si la faena arranca por debajo del ritmo nominal (rampa, demanda no validada), la utilización real de la planta de alimento cae en la misma proporción. A escala chica, una planta propia con un turno tendría la mayor parte del día ociosa.

### 2.2 Consumo de servicios y personal

**PENDIENTE.** Energía (kWh/t; molienda + pellet), vapor (kg/t), agua y dotación por turno requieren datos de proveedores o plantas en operación (DPV-14B-07). No se estiman en esta fase.

---

## 3. Capacidad física asociada (dependencias)

| Elemento | Cómo se dimensiona | Dónde se calcula |
|---|---|---|
| Recepción de granos | t/semana de maíz + harina de soja (~56 / 111 / 223 / 445 t/semana medio) y camiones/semana (2 / 4 / 8 / 16 con un barrido de 28 t, SUP-14B-13) | [`integracion_upstream.md` §4](integracion_upstream.md) y CSV bloque `10_logistica` |
| Silos de materias primas | consumo × días de stock / densidad | [`almacenamiento_silos.md`](almacenamiento_silos.md) |
| Celdas de producto terminado | ≥ 1 por fórmula (3–4) + días de stock | [`almacenamiento_silos.md`](almacenamiento_silos.md) |
| Despacho | t/semana plena / capacidad del granelero (3 / 5 / 9 / 18 viajes/semana con 28 t de escenario, SUP-096) | CSV bloque `10_logistica` |

## 4. Requisitos regulatorios a verificar

La elaboración de alimentos para animales requiere inscripción y registro ante SENASA (establecimiento y productos), con requisitos adicionales para alimentos medicados; también habilitaciones municipales, ambientales (polvo, ruido) y de seguridad (atmósferas explosivas). **Nada de esto se leyó en el original** (DPV-009): se registra como DPV-14B-06.
