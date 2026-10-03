# Costo de expansión — construir 20.000 de entrada vs crecer por etapas

**Fecha:** 2026-10-02 (v1.1) · Datos: [`expansion_capex.csv`](expansion_capex.csv) (2.508 filas) · Función: `expansion()` en [`modelo_capex.py`](modelo_capex.py) · Configuración: C1 (planta de faena; upstream externo)

> **El motor no dice que construir por etapas sea más barato ni más caro.** Con la base actual, casi todo el costo de ampliar está PENDIENTE. Lo que sí entrega es el mapa físico de qué se reutiliza, qué se amplía, qué se duplica y qué se reemplaza en cada trayectoria.

## 1. Trayectorias comparadas

| ID | Etapas (aves/día) | Terreno |
|---|---|---|
| A_20000_directo | 20.000 | `compra_fase` y `compra_reserva` |
| B_5000_a_20000 | 5.000 → 20.000 | ídem |
| B2_5000_10000_20000 | 5.000 → 10.000 → 20.000 | ídem |
| C_10000_a_20000 | 10.000 → 20.000 | ídem |

Se separan: **CAPEX inicial** (etapa 1), **CAPEX de expansión** (cada etapa siguiente) y **CAPEX acumulado**.

## 2. Etiquetas y acciones (SUP-165)

| Etiqueta | Significado | Acción al crecer | Δ a adquirir |
|---|---|---|---|
| REUTILIZABLE | Sirve tal cual a la escala mayor si se dimensionó para ella (terreno reservado, acometida, software, laboratorio) | REUTILIZA o AMPLIA_REUTILIZABLE | max(0, q₁ − q₀) |
| ESCALABLE | Se reutiliza y se amplía por módulos (edificios, frío, efluentes, agua) | AMPLIA | max(0, q₁ − q₀) |
| DUPLICABLE | Se agrega otra unidad igual (vehículos, túneles, setters, transformadores, generadores) | DUPLICA | max(0, q₁ − q₀) |
| REEMPLAZABLE | Se reemplaza por uno mayor o de otro nivel de automatización | REEMPLAZA | q₁ completo (valor residual del anterior PENDIENTE) |
| ESPECIFICO_DE_FASE | Se incurre en cada fase (indirectos, preoperativos, contingencias) | NUEVO_POR_FASE | PENDIENTE |
| MIXTA | Paquete de línea: se resuelve en sus EQ hijos | PENDIENTE | — |

Los lotes y paquetes se comparan por **capacidad** (aves/h, kWf, m³/d, t/d), no por "1 lote". Un concepto "lote" sin capacidad queda PENDIENTE: no se puede saber si se reutiliza. Un cambio del nivel de automatización de un EQ entre etapas (p. ej., S → A) se registra como REEMPLAZA; esos niveles son hipótesis de la matriz 08 (SUP-065, T16-06).

## 3. Resultado físico (C1, etapa de crecimiento hacia 20.000)

| Trayectoria / terreno | REUTILIZA | AMPLIA (incl. reutilizable) | DUPLICA | REEMPLAZA | NUEVO | Por fase | PENDIENTE |
|---|---|---|---|---|---|---|---|
| B 5.000 → 20.000, solo fase | 2 | 40 | 10 | 39 | 3 | 19 | 44 |
| B 5.000 → 20.000, con reserva | 4 | 38 | 10 | 39 | 3 | 19 | 44 |
| C 10.000 → 20.000, solo fase | 2 | 51 | 19 | 20 | 2 | 19 | 44 |
| C 10.000 → 20.000, con reserva | 4 | 49 | 19 | 20 | 2 | 19 | 44 |
| B2 (dos expansiones), solo fase | 4 | 92 | 31 | 56 | 3 | 38 | 88 |

Conteos v1.1 (tras la auditoría de drivers: frío y algunos componentes pasaron a PENDIENTE). Lectura (física, no económica):
- **Terreno.** Sin reserva, crecer de 5.000 a 20.000 exige comprar ≈ 14.350 m² adicionales (medio; diferencia de mínimos físicos, función de 12C sin reserva) **contiguos**: riesgo si no hay lote vecino (DEC-063). Con reserva para 20.000 desde el inicio, el terreno se **reutiliza** (Δ = 0; test X02), a cambio de comprar ≈ 33.345 m² en la etapa 1.
- **Obra.** Proceso húmedo +3.170 m², pavimentos +2.172 m², etc. (B, medio): se amplía; la prima de ampliar con la planta operando es PENDIENTE (DPV-086).
- **Equipos.** Partiendo de 5.000, 39 EQ cambian de nivel de automatización al llegar a 20.000 (reemplazo); partiendo de 10.000, 20. Es la mayor diferencia física entre trayectorias, y depende de una hipótesis.
- **Utilities.** Efluente +330 m³/d, agua +375 m³/d (B): ampliables si se reservó espacio. Frío, transformación, respaldo y térmico quedan PENDIENTES (v1.1: el paquete de frío ya no tiene una capacidad propia de CAPEX; la carga de diseño es PENDIENTE, contradicción ×5,7 abierta).

## 4. Resultado económico: lo poco que hay

| Trayectoria (C1, solo fase) | CAPEX inicial con precio | Expansión con precio | Acumulado con precio | Conceptos sin costo (acumulados) |
|---|---|---|---|---|
| A 20.000 directo | 222.431 | — | 222.431 | 75 |
| B 5.000 → 20.000 | 64.186 | 158.244 | 222.431 | 148 |
| B2 5.000 → 10.000 → 20.000 | 64.186 | 55.014 + 103.230 | 222.431 | 221 |
| C 10.000 → 20.000 | 119.200 | 103.230 | 222.431 | 148 |

USD, solo depósitos y talleres (OC-DP, E4). **El acumulado es idéntico en todas las trayectorias por construcción** (precio unitario lineal por m² de obra nueva), no porque etapas y planta única cuesten lo mismo. Faltan: prima de ampliación, duplicación de servicios, valor residual de lo reemplazado, costo financiero del tiempo y todos los precios de equipos.

## 5. Para el optimizador futuro

`expansion_capex.csv` deja por activo: trayectoria, etapa, escala, etiqueta, acción, cantidad anterior/nueva, Δ a adquirir, unidad y costo de la etapa (vacío si no hay precio). Con cotizaciones a dos escalas (exponentes, DPV-160) y la prima de ampliación (DPV-086), el mismo motor podrá comparar trayectorias en valor. Decisiones relacionadas: DEC-033, DEC-034, DEC-035, DEC-063.
