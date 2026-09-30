# Agua retenida/incorporada en producto, condenas y mermas

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual) · Fase 0 (prefactibilidad)

> **Alcance.** Cómo el enfriamiento de la carcasa (chiller por inmersión o por aire) cambia el peso vendido sin cambiar la carne, y cómo las condenas veterinarias, decomisos, degradaciones y mermas de proceso reducen la masa aprovechable. **No** se elige el sistema de enfriamiento ni se diseña equipamiento.
> **Fuentes.** Extractos de buscador `[PVDP]` (normas y estudios no leídos en su original, 2026-09-30). Valores del modelo `[ESTIMACIÓN]`/`[SUPUESTO]` (SUP-041, SUP-042).

---

## 1. Tres masas que no deben confundirse

```
MASA BIOLÓGICA  = tejidos del ave (músculo, piel, grasa, hueso). Solo entra con el peso vivo.
AGUA RETENIDA/INCORPORADA EN PRODUCTO = agua que la carcasa absorbe en el chiller por inmersión y queda en el producto vendido
                   (agua absorbida − agua de goteo del producto). El agua adherida a plumas se registra aparte (subproducto).
PESO COMERCIAL  = masa biológica + agua retenida (la que queda después del goteo) = lo que se pesa y se vende.
```

**No confundir con el agua de proceso total de la planta** (lavado, escaldado, llenado y renovación del chiller, limpieza, sanitización, otros usos): **ESTE BALANCE NO DIMENSIONA EL CONSUMO INDUSTRIAL DE AGUA NI EL CAUDAL TOTAL DE EFLUENTES DE LA PLANTA**; eso se calculará en `11_agua_efluentes`. Desagregación en [`auditoria_balance.md` §2](auditoria_balance.md).

**Regla del modelo:** el agua **nunca** se cuenta como carne producida. Cada salida del CSV tiene tres columnas: `masa_biologica_kg_ave`, `agua_kg_ave`, `total_kg_ave`; la suma de la masa biológica de todas las salidas es exactamente el peso vivo (test T08) y el agua entra y sale por una cuenta separada.

## 2. Enfriamiento: qué dicen las fuentes

### 2.1 Métodos

| Método | Cómo funciona | Efecto sobre el peso | Referencias `[PVDP]` |
|---|---|---|---|
| **Inmersión en agua** (*chiller* y *pre-chiller*) | Tanques con agua fría (y hielo) en contracorriente; ~50 min | **Gana peso:** +4 a +8 % habitual; en un estudio, 9,3 % promedio (rango 3,4–14,7 %); +5 a +10 % según extensión universitaria | FTE-171, FTE-172 |
| **Aire** (*air chilling*) | Túnel de aire frío; 90–150 min | **Pierde peso por evaporación:** −1 a −3 % (−1,6 %; −2,5 %; −2,84 % en distintos estudios) | FTE-171, FTE-172 |
| Aire con aspersión (*air-spray*) | Aire frío con rociado intermitente | Intermedio | FTE-167 |

Otros efectos (extractos): el enfriamiento por aire evita la absorción de agua y suele asociarse a mejores atributos sensoriales, pero consume más energía y tiempo; los filetes de carcasas enfriadas por inmersión mostraron **menor rendimiento en la cocción** (el agua absorbida se pierde al cocinar) (FTE-171).

### 2.2 Límites regulatorios encontrados

| Jurisdicción | Norma | Qué exige (según extractos) | Estado |
|---|---|---|---|
| **Argentina** | Decreto 4238/68, cap. XX (aves) | Regula el enfriamiento y el control de la retención de agua. Según prensa que cita a SENASA, **el pollo no puede absorber más de un 8 %** de líquido | `[PVDP]` FTE-168 (prensa). **Texto oficial no leído** (DPV-061) |
| Brasil | Portaria MAPA 210/1998 (mod. 74/2019); Res. DIPOA 4/2002 | Absorción en el pre-enfriamiento por inmersión **≤ 8 %** del peso (control interno); exceso = **fraude**; control de temperatura del agua, renovación mínima en contracorriente y tiempo máximo en el pre-chiller | `[PVDP]` FTE-170 |
| Unión Europea | Reglamento (CE) 543/2008 (normas de comercialización) | Contenido máximo de "agua extraña técnicamente inevitable": piezas (método químico) **2 % aire, 4 % aire-aspersión, 6 % inmersión**; canales enteras entre ~1,5 % y 7 % según método y ensayo (absorción, goteo o químico) | `[PVDP]` FTE-167; cifras por ensayo a verificar |
| EE.UU. | 9 CFR 441.10 (regla FSIS de 2001) | Solo se admite agua retenida si el establecimiento **demuestra con datos** que es inevitable para cumplir requisitos de inocuidad; la **etiqueta** debe declarar "hasta X % de agua retenida" | `[PVDP]` FTE-169 |

**Lectura:** el 8 % argentino y brasileño es un **tope de absorción**, no un objetivo; la UE y EE.UU. tienden a limitar el agua retenida y a exigir que se declare. Un diseño con vocación exportadora (SUP-015) debe verificar qué exige cada destino respecto del método de enfriamiento y del agua (DPV-061).

**Otra práctica distinta:** la inyección o "hidratación" con salmuera (marinado) agrega un **ingrediente** al producto (se discute en la prensa argentina, FTE-168). No es parte del balance de faena: si en el futuro se evalúan productos marinados, la solución inyectada se contabilizará como insumo y se rotulará, nunca como rendimiento de faena.

## 3. Cómo lo trata el modelo

| Parámetro | Inmersión (base) | Inmersión en el límite | Aire | Clasificación |
|---|---|---|---|---|
| Absorción (kg de agua / kg de carcasa antes del chiller) | **6,0 %** | 8,0 % | 0 | `[SUPUESTO]` SUP-042 |
| Goteo antes de la venta (escurrido + purga en bandeja), fracción del agua absorbida | **30 %** | 30 % | — | `[SUPUESTO]`, sin fuente |
| Evaporación (fracción de la masa biológica) | 0 | 0 | **1,8 %** | `[ESTIMACIÓN]` (rango de fuentes 1–3 %) |
| Reparto del agua retenida | Proporcional a la masa de cada producto derivado de la carcasa | igual | — | `[SUPUESTO]` |
| Menudencias y patas | Sin agua modelada (también se enfrían y pueden absorber) | igual | — | Simplificación (DPV-062) |
| Agua adherida a plumas (sale con la pluma húmeda) | 0,6 kg por kg de pluma | igual | igual | `[SUPUESTO]` SUP-040 |

### 3.1 Resultado por ave (configuración A, pollo de 2,9 kg, condenas medias)

| Concepto | Inmersión 6 % | Inmersión 8 % (límite) | Aire |
|---|---|---|---|
| Carcasa apta antes del chiller (masa biológica) | 2,036 kg | 2,036 kg | 2,036 kg |
| Agua absorbida por la carcasa en el chiller | +0,122 kg | +0,163 kg | 0 |
| Peso a la salida del chiller | 2,158 kg | 2,199 kg | 2,000 kg |
| Agua de goteo del producto antes de la venta (efluente) | −0,037 kg | −0,049 kg | 0 |
| Evaporación | 0 | 0 | −0,037 kg |
| **Peso comercial** (carcasa, antes de separar canales degradadas) | **2,122 kg** | **2,150 kg** | **2,000 kg** |
| de los cuales **masa biológica** | 2,036 kg | 2,036 kg | 2,000 kg |
| de los cuales **agua retenida en producto** | 0,086 kg (**4,0 %** del peso vendido) | 0,114 kg (5,3 %) | 0 |
| Rendimiento **aparente** a la salida del chiller | 74,4 % | 75,8 % | 69,0 % |
| Rendimiento **comercial** (peso comercial / PV) | 73,2 % | 74,1 % | 69,0 % |
| Rendimiento **biológico** (masa biológica vendible / PV) | 70,2 % | 70,2 % | 69,0 % |

Por peso vivo (inmersión 6 %, rendimiento comercial de la carcasa): 71,8 % (2,2 kg) · 72,4 % (2,5) · 73,0 % (2,8) · 73,2 % (2,9) · 73,4 % (3,0) · 73,8 % (3,2) · 74,3 % (3,5); con aire: 67,7 % · 68,2 % · 68,8 % · 69,0 % · 69,1 % · 69,5 % · 70,1 %.

### 3.2 Efecto sobre la economía por ave (sin precios)

- **Entre inmersión y aire, el mismo pollo "pesa" 0,122 kg más (+6,1 %) al venderse.** A 10.000 aves/día son **1,2 t/día (~305 t/año)** más de "producto". Esa diferencia es **agua**, no carne: si se usa el peso comercial con agua para calcular ingresos y el peso biológico para comparar con otra planta, el análisis queda sesgado.
- **Regla para el modelo económico futuro:** ingreso = kg **comerciales** × precio (lo que efectivamente se cobra), pero la comparación de eficiencia entre escenarios, la conversión de demanda a aves y el costo por kg de carne se hacen sobre **masa biológica**. El agua retenida debe mostrarse como línea separada.
- **El agua tiene costos:** purga en la góndola (los supermercados la reclaman como merma o devolución), menor rendimiento en cocción, riesgo reglamentario y reputacional, agua y frío del chiller, efluentes. Y el aire tiene los suyos (energía, tiempo, espacio, pérdida de peso). **No se decide el método** (DEC-026).
- **Calidad y etiquetado:** en destinos que exigen declarar el agua retenida (EE.UU.) o que fijan topes por método (UE), el método de enfriamiento condiciona la etiqueta y la especificación del producto; en Argentina el tope es de absorción (8 %, a verificar).

## 4. Condenas, decomisos y mermas — escenarios

**No hay un porcentaje único verdadero.** Los decomisos dependen de la sanidad del lote, la captura, el transporte, el ayuno y la operación de la planta. Datos leídos (Brasil; **no hay datos argentinos**):

- Mato Grosso: **9,5 %** de las carcasas con algún decomiso: **2,69 % total** y **6,8 % parcial**; causas principales: contaminación gastrointestinal (57 % de los totales, 38 % de los parciales) y celulitis (~18 %) (FTE-173 `[PVDP]`).
- Planta exportadora del sudeste: ~7 % de carcasas con decomiso total o parcial; como causas de decomiso total, celulitis 0,3–1,0 %, ascitis 0,3–0,4 % (FTE-173 `[PVDP]`).

**Relación con las pérdidas no asignadas:** los decomisos se **descuentan** de la carcasa, el cuello, las menudencias y las patas y se registran **una sola vez** como residuo (clase D). Las pérdidas no asignadas (1,4 % PV) son otra masa: la diferencia de la composición primaria del ave, calculada antes de los decomisos. No se superponen (test T14; [`auditoria_balance.md` §3](auditoria_balance.md)).

### 4.1 Parámetros del modelo (SUP-041)

| Variable | Bajo (pocos problemas) | **Medio** | Alto | Qué se pierde |
|---|---|---|---|---|
| **Decomiso total** (fracción de aves) | 0,4 % | **1,0 %** | 2,7 % (≈ Mato Grosso) | Carcasa + cuello + menudencias + patas del ave decomisada |
| **Decomiso parcial** (fracción de la masa de carcasa recortada) | 0,3 % | **0,8 %** | 1,5 % | Partes afectadas (celulitis, contaminación, lesiones) |
| **Canales no aptas para venta entera** (hematomas, alas rotas, roturas de piel) | 3 % | **6 %** | 12 % | Nada de masa: pasan a trozado (config. A) |
| Garras: grado A / segunda / descarte | 90 / 8 / 2 % | **80 / 15 / 5 %** | 60 / 25 / 15 % | Grado comercial (pododermatitis, hematomas) |

Los porcentajes de decomiso parcial en masa (0,3–1,5 %) son **estimaciones**: las fuentes informan el porcentaje de carcasas afectadas, no la masa recortada (se supuso que una carcasa con decomiso parcial pierde ~10–20 % de su masa).

### 4.2 Efecto (pollo de 2,9 kg)

| Escenario de condenas | Decomisos (kg/ave) | % PV | Pollo entero vendible (config. A, masa biológica) | Canales a trozar (config. A) | Comestible total A+B (config. B) |
|---|---|---|---|---|---|
| Bajo | 0,016 | 0,5 % | 1,997 kg | 0,062 kg | 2,338 kg |
| **Medio** | **0,040** | **1,4 %** | **1,914 kg** | **0,122 kg** | **2,311 kg** |
| Alto | 0,094 | 3,2 % | 1,749 kg | 0,238 kg | 2,247 kg |

Entre el escenario bajo y el alto se pierden **~0,09 kg comestibles por ave (−3,9 %)** y el pollo entero vendible cae **12 %** (más decomisos y más canales degradadas). A 10.000 aves/día, los decomisos van de 0,16 a 0,94 t/día.

### 4.3 Mermas de proceso

| Merma | Valor del modelo | Clase | Clasificación |
|---|---|---|---|
| Pérdidas no asignadas de la faena (humedad, tejidos al efluente, no identificado) | 1,4 % PV (medio); 1,9 % bajo; 0,7 % alto | P | `[ESTIMACIÓN]` por cierre; test 0–4 % |
| Merma de trozado (aserrín de hueso, exudado) | 0,5 % de la carcasa trozada | P | `[SUPUESTO]` |
| Merma de deshuese | 1 % del corte deshuesado | P | `[SUPUESTO]` |
| Merma de CMS | 1 % de la materia prima | P | `[SUPUESTO]` |
| Evaporación en enfriamiento por aire | 1,8 % de la carcasa | P | `[ESTIMACIÓN]` |
| Agua de goteo del producto | 30 % del agua absorbida por la carcasa | D (agua) | `[SUPUESTO]` |
| Merma de peso vivo por ayuno y transporte | 0,2–0,6 %/h de ayuno (FTE-177) | Fuera del balance | Ver `03_produccion_primaria` |

**Ninguna pérdida se oculta:** todas aparecen como filas propias (clase P o D) en el CSV.

## 5. Por qué 1 punto de rendimiento importa

- Un pollo de 2,9 kg con **1 punto** más de rendimiento eviscerado da **29 g más de carcasa**.
- A 10.000 aves/día y 250 días de faena: **72,5 t/año** más de carcasa con las **mismas aves, el mismo alimento y los mismos pollitos**. Todo el costo ya se pagó: ese kilo extra es casi margen.
- Entre los escenarios de rendimiento bajo (70,0 %) y alto (72,7 %) hay 2,7 puntos: **~196 t/año** de carcasa a 10.000 aves/día.
- Entre condenas bajas y altas: ~0,09 kg comestibles por ave → **~228 t/año** a 10.000 aves/día.
- Lo que mueve el rendimiento: ayuno correcto (contenido GI), sangrado, desplumado sin roturas, evisceración sin roturas de intestino (contaminación → decomiso), captura y transporte (hematomas), sanidad del lote (celulitis, ascitis), calibración de máquinas. Casi todo es **gestión**, no inversión.

## 6. Datos a validar

| Dato | Registro |
|---|---|
| Texto del Decreto 4238/68 cap. XX: límite de absorción, método de control, etiquetado; requisitos de destinos de exportación sobre agua y método de enfriamiento | DPV-061 |
| Método de enfriamiento predominante en Argentina; absorción, goteo y agua retenida reales en plantas; absorción de menudencias y garras | DPV-062 |
| Tasas de decomiso total y parcial y causas en plantas argentinas (SENASA, plantas, veterinarios) | DPV-063 |
| Balance medido en planta (incluye pérdidas no asignadas) | DPV-060 |
