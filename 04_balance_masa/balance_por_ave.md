# Balance de masa por ave

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Pregunta central:** si entran X kg de pollo vivo, ¿dónde termina cada kilogramo?
> **Alcance.** Balance físico de la faena y del procesamiento de 1 pollo vivo, para 6 pesos vivos (2,2 / 2,5 / 2,8 / 3,0 / 3,2 / 3,5 kg; más 2,9 kg de referencia), 3 configuraciones comerciales y escenarios de rendimiento, condenas y enfriamiento. **No** calcula rentabilidad, **no** selecciona productos, **no** diseña maquinaria ni fija capacidad (reglas 7–9 de [`CLAUDE.md`](../CLAUDE.md)).
> **Fuentes.** La lectura directa de documentos volvió a estar bloqueada por la red del entorno (WebFetch y curl: `EGRESS_BLOCKED` / 403 en cobbgenetics.com, aviagen.com, eur-lex, fsis, SENASA, FAO; 2026-09-30). Solo se usaron **extractos de buscador**: toda cifra externa es `[PVDP]` (regla 16). Los parámetros del modelo son `[ESTIMACIÓN]` o `[SUPUESTO]` (SUP-035 a SUP-044).
> **Modelo:** [`modelo_balance_masa.py`](modelo_balance_masa.py) · **Resultados:** [`escenarios_balance.csv`](escenarios_balance.csv) (126 balances, 4.956 filas) · Documentación del modelo: [`README.md`](README.md).
> Documentos hermanos: cortes y deshuese en [`rendimientos_cortes.md`](rendimientos_cortes.md); subproductos en [`subproductos_masa.md`](subproductos_masa.md); agua, condenas y mermas en [`agua_y_mermas.md`](agua_y_mermas.md); guía en [`guia_ramiro.md`](guia_ramiro.md); síntesis en [`conclusiones_balance.md`](conclusiones_balance.md).

---

## 1. Unidad base y límites del sistema

- **Unidad:** 1 pollo vivo **recibido en planta** (después del ayuno y del transporte). El balance empieza en la balanza de recepción, no en la granja.
- **Fuera del balance** (ya tratados en `03_produccion_primaria`): aves muertas en granja y en transporte (DOA) y la **merma de peso por ayuno y transporte** (≈0,2–0,6 % del peso vivo por hora de ayuno según extractos, FTE-177 `[PVDP]`). Un ave que pesó 2,9 kg en la granja puede llegar con ~2,85 kg. Por eso **peso vivo en granja ≠ peso vivo en planta** (SUP-035).
- **Dos flujos que no se mezclan** (regla del modelo): la **masa biológica** del ave (entra solo con el peso vivo) y el **agua incorporada en el proceso** (chiller por inmersión, agua arrastrada por las plumas), que entra y sale por separado. Ver [`agua_y_mermas.md`](agua_y_mermas.md).
- **Base de cálculo de cada porcentaje:** siempre declarada — `% PV` (sobre peso vivo en planta, masa biológica) o `% carcasa` (sobre la carcasa eviscerada caliente, definición D5).

## 2. Definiciones (no mezclar)

Las fuentes usan "canal", "carcasa", "eviscerado", "dressed", "ready-to-cook" con contenidos distintos: una diferencia de definición mueve el "rendimiento" 3–8 puntos. En este proyecto:

| ID | Término | Qué incluye | Qué excluye | Momento |
|---|---|---|---|---|
| D1 | **Peso vivo en granja** | Ave viva con contenido digestivo | — | Antes de la carga |
| D2 | **Peso vivo (PV) en planta** | Ave viva al llegar, después de ayuno y transporte | Merma de ayuno/transporte | Recepción. **Base del balance** |
| D3 | Peso sangrado / desplumado | Ave sin sangre / sin sangre ni plumas | — | Etapas intermedias (no se usan como rendimiento) |
| D4 | **"Peso canal"** | Término **ambiguo** en Argentina y en las fuentes: puede incluir o no cuello, menudencias, patas o grasa | — | **No se usa sin calificador** |
| D5 | **Peso eviscerado (carcasa caliente)** — "carcasa" en el modelo | Carcasa con piel, grasa abdominal y riñones | Sangre, plumas, cabeza, patas (corte en el tarso), vísceras, **cuello y menudencias** | Salida de evisceración, antes del chiller. **Masa biológica** |
| D6 | Carcasa con cuello y menudencias ("canal con menudencias") | D5 + cuello + hígado + corazón + molleja | — | Referencia de comparación con fuentes que la usan |
| D7 | **Carcasa fría** | D5 después del enfriamiento: **masa biológica** (menos evaporación si es por aire) **+ agua absorbida** (si es por inmersión) | — | Salida del chiller |
| D8 | **Ready-to-cook (RTC)** | Carcasa fría lista para cocinar. En EE.UU. puede incluir cuello y menudencias; en este proyecto = D7 **sin** cuello ni menudencias salvo que se indique | — | Empaque |
| D9 | **Peso comercial** | Peso que se vende: masa biológica + **agua retenida** (agua absorbida − goteo/purga) | Envase | Venta |

**Rendimientos derivados** (siempre con su definición):

- **Rendimiento eviscerado** = D5 / D2 (masa biológica, sin agua). Es el que usa el modelo como "rendimiento de faena".
- Rendimiento con cuello y menudencias = D6 / D2.
- **Rendimiento aparente** = peso a la salida del chiller / D2: **incluye agua** y no debe confundirse con carne producida.
- Rendimiento comercial = D9 / D2.
- Las tablas de las genéticas son "*dry yield*": según el extracto del objetivo Ross 308 no incluyen humedad retenida en el enfriamiento (FTE-142 `[PVDP]`). Comparar un rendimiento de planta con inmersión contra una tabla genética sin corregir el agua es un error frecuente.

## 3. Rangos de rendimiento de faena por componente

`% PV` (masa biológica). "Fuentes" = rangos leídos en extractos `[PVDP]`; "Modelo" = valor medio adoptado a 2,9 kg y su escenario bajo/alto. **Los rangos de fuentes no suman 100 %** entre sí (definiciones y épocas distintas): ver §11.

| Componente | Fuentes (% PV) | Modelo medio 2,9 kg (% PV) | Escenarios / pendiente | Fuente | Clasificación |
|---|---|---|---|---|---|
| **Carcasa eviscerada** (D5) | 72–75 "dressing" (UW-Madison, FTE-172); Cobb 500 ~74,0 a 2,8 kg (FTE-140) o 75,6–75,9 (FTE-161), definición no confirmada | **71,5** | bajo 70,0 / alto 72,7; +1,9 pp/kg | FTE-140, FTE-161, FTE-172 | `[ESTIMACIÓN]` SUP-036/037 |
| Sangre drenada | 3,3–4,0; 3,8 (corte yugular); objetivo ~3 (45–50 % del volumen sanguíneo de 6–7,5 % PV); 3,5 | **3,4** | −0,1 pp/kg | FTE-163, FTE-165, FTE-166 | `[ESTIMACIÓN]` |
| Plumas (masa biológica) | 5–7; 3–7; 6; "9" y "8" (probablemente pluma húmeda) | **5,2** (+ 3,1 de agua de escaldado = 8,3 húmeda) | bajo 5,4; −0,2 pp/kg | FTE-163, FTE-164, FTE-182 | `[ESTIMACIÓN]` |
| Cabeza | 3 | **2,5** | −0,3 pp/kg | FTE-163 | `[ESTIMACIÓN]` débil |
| Patas (corte en el tarso) | ~4; 5 | **3,9** | −0,3 pp/kg | FTE-163, FTE-175 | `[ESTIMACIÓN]` |
| Hígado | 2,0 (7 semanas) | **1,9** | −0,15 pp/kg | FTE-174 | `[ESTIMACIÓN]` |
| Corazón | 0,6 (7 semanas) | **0,5** | −0,05 pp/kg | FTE-174 | `[ESTIMACIÓN]` |
| Molleja limpia | 3,0 (7 semanas, probablemente sin limpiar) | **1,4** | −0,2 pp/kg | FTE-174 | `[ESTIMACIÓN]` débil |
| Cuello | 3,6 (7 semanas); 4,98 (definición dudosa) | **2,6** | −0,1 pp/kg | FTE-174 | `[ESTIMACIÓN]` débil |
| Tracto digestivo vacío | Sin dato individual (vísceras no comestibles totales ~9, FTE-163) | **3,0** | −0,25 pp/kg | FTE-163 | `[SUPUESTO]` |
| Contenido gastrointestinal | Ayuno de ~12 h reduce el contenido ~75 % (FTE-177) | **1,2** | bajo 2,0 / alto 0,7 | FTE-177 | `[SUPUESTO]` |
| Pulmones | Sin dato | **0,6** | −0,05 pp/kg | — | `[SUPUESTO]` |
| Otros no comestibles (tráquea, esófago y buche, bazo, vesícula, gónadas, cutícula y contenido de molleja) | Sin dato | **0,9** | −0,1 pp/kg | — | `[SUPUESTO]` |
| Grasa abdominal (**dentro** de la carcasa) | 1,55–3,3 (según edad, sexo y época) | **1,8** | +0,3 pp/kg | FTE-178 | `[ESTIMACIÓN]`; queda en la carcasa (SUP-043) |
| **Pérdidas no asignadas** (humedad, tejidos al efluente, no identificado) | — | **1,4** (cierre) | bajo 1,9 / alto 0,7; constante con el peso | Cálculo | `[ESTIMACIÓN]` por diferencia; test: 0–4 % |

**Método del cierre.** La carcasa y cada subproducto se fijan con rangos de fuentes; la diferencia hasta el 100 % se muestra como **pérdidas no asignadas** (no se esconde dentro de otra línea). El test T04 exige que esté entre 0 y 4 % del PV: si un cambio de parámetros la vuelve negativa (se "asignaron" más kg de los que tiene el ave) el modelo se detiene.

## 4. Balance primario por peso vivo (escenario medio)

kg/ave (masa biológica) y `% PV`. Suma = PV en todas las columnas (tests T01, T09). Fuente: modelo, `[ESTIMACIÓN]`.

| Componente | 2,2 kg | 2,5 kg | 2,8 kg | **2,9 kg** | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| **Carcasa eviscerada (D5)** | 1,544 (70,2 %) | 1,768 (70,7 %) | 1,997 (71,3 %) | **2,073 (71,5 %)** | 2,151 (71,7 %) | 2,306 (72,1 %) | 2,542 (72,6 %) |
| Sangre | 0,076 (3,5 %) | 0,086 (3,4 %) | 0,095 (3,4 %) | **0,099 (3,4 %)** | 0,102 (3,4 %) | 0,108 (3,4 %) | 0,117 (3,3 %) |
| Plumas (biológica) | 0,117 (5,3 %) | 0,132 (5,3 %) | 0,146 (5,2 %) | **0,151 (5,2 %)** | 0,155 (5,2 %) | 0,164 (5,1 %) | 0,178 (5,1 %) |
| Cabeza | 0,060 (2,7 %) | 0,066 (2,6 %) | 0,071 (2,5 %) | **0,072 (2,5 %)** | 0,074 (2,5 %) | 0,077 (2,4 %) | 0,081 (2,3 %) |
| Patas | 0,090 (4,1 %) | 0,100 (4,0 %) | 0,110 (3,9 %) | **0,113 (3,9 %)** | 0,116 (3,9 %) | 0,122 (3,8 %) | 0,130 (3,7 %) |
| Hígado | 0,044 (2,0 %) | 0,049 (2,0 %) | 0,054 (1,9 %) | **0,055 (1,9 %)** | 0,057 (1,9 %) | 0,059 (1,9 %) | 0,063 (1,8 %) |
| Corazón | 0,012 (0,5 %) | 0,013 (0,5 %) | 0,014 (0,5 %) | **0,015 (0,5 %)** | 0,015 (0,5 %) | 0,016 (0,5 %) | 0,016 (0,5 %) |
| Molleja limpia | 0,034 (1,5 %) | 0,037 (1,5 %) | 0,040 (1,4 %) | **0,041 (1,4 %)** | 0,041 (1,4 %) | 0,043 (1,3 %) | 0,045 (1,3 %) |
| Cuello | 0,059 (2,7 %) | 0,066 (2,6 %) | 0,073 (2,6 %) | **0,075 (2,6 %)** | 0,078 (2,6 %) | 0,082 (2,6 %) | 0,089 (2,5 %) |
| Tracto digestivo vacío | 0,070 (3,2 %) | 0,077 (3,1 %) | 0,085 (3,0 %) | **0,087 (3,0 %)** | 0,089 (3,0 %) | 0,094 (2,9 %) | 0,100 (2,9 %) |
| Contenido gastrointestinal | 0,028 (1,3 %) | 0,031 (1,2 %) | 0,034 (1,2 %) | **0,035 (1,2 %)** | 0,036 (1,2 %) | 0,037 (1,2 %) | 0,040 (1,1 %) |
| Pulmones | 0,014 (0,6 %) | 0,015 (0,6 %) | 0,017 (0,6 %) | **0,017 (0,6 %)** | 0,018 (0,6 %) | 0,019 (0,6 %) | 0,020 (0,6 %) |
| Otros no comestibles | 0,021 (1,0 %) | 0,024 (0,9 %) | 0,025 (0,9 %) | **0,026 (0,9 %)** | 0,027 (0,9 %) | 0,028 (0,9 %) | 0,029 (0,8 %) |
| Pérdidas no asignadas | 0,031 (1,4 %) | 0,035 (1,4 %) | 0,039 (1,4 %) | **0,041 (1,4 %)** | 0,042 (1,4 %) | 0,045 (1,4 %) | 0,049 (1,4 %) |
| **Total = PV** | **2,200** | **2,500** | **2,800** | **2,900** | **3,000** | **3,200** | **3,500** |
| *de la carcasa: grasa abdominal* | *0,035* | *0,042* | *0,050* | *0,052* | *0,055* | *0,060* | *0,069* |

### 4.1 Rendimiento eviscerado (D5 / PV, masa biológica) por escenario

| Escenario | 2,2 kg | 2,5 kg | 2,8 kg | 2,9 kg | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| Bajo (ayuno deficiente, lote pobre) | 68,7 % | 69,2 % | 69,8 % | 70,0 % | 70,2 % | 70,6 % | 71,1 % |
| **Medio** | **70,2 %** | **70,7 %** | **71,3 %** | **71,5 %** | **71,7 %** | **72,1 %** | **72,6 %** |
| Alto (cerca del objetivo genético) | 71,4 % | 71,9 % | 72,5 % | 72,7 % | 72,9 % | 73,3 % | 73,8 % |

### 4.2 El mismo pollo de 2,9 kg según la definición de "rendimiento"

| Definición | kg/ave | % PV | ¿Incluye agua? |
|---|---|---|---|
| Eviscerado caliente (D5) | 2,073 | 71,5 % | No |
| Con cuello (D5 + cuello) | 2,149 | 74,1 % | No |
| Con cuello y menudencias (D6) | 2,259 | 77,9 % | No |
| Carcasa apta después de condenas (medio) | 2,036 | 70,2 % | No |
| Salida de chiller por inmersión (6 % de absorción) | 2,158 | 74,4 % | **Sí** (0,122 kg) |
| Peso comercial con inmersión (después del goteo) | 2,122 | 73,2 % | **Sí** (0,086 kg) |
| Peso comercial con enfriamiento por aire (1,8 % de evaporación) | 2,000 | 69,0 % | No (perdió 0,037 kg de humedad) |

Un mismo ave puede presentarse con "rendimientos" de **69 % a 78 %** según qué se cuente. Ninguno es falso; lo incorrecto es compararlos entre sí. Detalle del agua en [`agua_y_mermas.md`](agua_y_mermas.md).

## 5. Menudencias (vísceras comestibles) y cuello

Escenario medio, **antes** del decomiso total (con decomiso medio de 1 % se venden 0,99 veces estos valores). `% carcasa` = sobre D5.

| Parte | 2,2 kg | 2,5 kg | 2,8 kg | 2,9 kg | 3,0 kg | 3,2 kg | 3,5 kg | % PV (2,9) | % carcasa (2,9) |
|---|---|---|---|---|---|---|---|---|---|
| Hígado | 0,044 | 0,049 | 0,054 | 0,055 | 0,057 | 0,059 | 0,063 | 1,9 % | 2,7 % |
| Corazón | 0,012 | 0,013 | 0,014 | 0,015 | 0,015 | 0,016 | 0,016 | 0,5 % | 0,7 % |
| Molleja limpia | 0,034 | 0,037 | 0,040 | 0,041 | 0,041 | 0,043 | 0,045 | 1,4 % | 2,0 % |
| **Menudencias (3)** | **0,090** | **0,099** | **0,108** | **0,110** | **0,113** | **0,118** | **0,124** | **3,8 %** | **5,3 %** |
| Cuello | 0,059 | 0,066 | 0,073 | 0,075 | 0,078 | 0,082 | 0,089 | 2,6 % | 3,6 % |
| **Menudencias + cuello** | 0,149 | 0,165 | 0,181 | **0,185** | 0,191 | 0,200 | 0,213 | 6,4 % | 8,9 % |

- **Otras partes comestibles** posibles (no modeladas como producto): riñones (quedan en la carcasa), piel del cuello, grasa abdominal, crestas/testículos (irrelevantes en parrillero). Las **patas/garras** se tratan en [`subproductos_masa.md` §2](subproductos_masa.md) y **no** se suman aquí (sin doble conteo, test T10).
- Las menudencias pierden peso relativo al crecer el ave (hígado ×1,44 y molleja ×1,32 entre 2,2 y 3,5 kg, contra ×1,59 del PV).
- El ejemplo ilustrativo de la demanda (0,12 kg de menudencias por ave, SUP-023) es coherente con 0,110 kg (hígado + corazón + molleja) o 0,185 kg si incluye cuello: **definir siempre si "menudencias" incluye el cuello** (DPV-068).
- En la configuración A, el modelo vende el pollo entero **sin** menudencias adentro (parámetro `MENUDENCIAS_CON_ENTERO`, SUP-043); la práctica argentina (entero "con menudencias" o "sin menudencias") debe validarse (DPV-068).

## 6. Clasificación conceptual de las salidas

| Clase | Significado | Salidas del modelo | Destino conceptual |
|---|---|---|---|
| **A. Producto principal** | Lo que define el negocio; mayor valor por kg | Pollo entero; pechuga con hueso; pata-muslo; suprema; solomillo; muslo deshuesado; pata con hueso | Venta de carne |
| **B. Coproducto comestible** | Parte comestible de menor valor, conjunta con A | Alas; hígado; corazón; molleja; cuello; garras grado A y de segunda; carcasa-esqueleto; piel; recortes; CMS | Venta de carne o insumo industrial |
| **C. Subproducto valorizable** | No comestible (o no destinado a consumo) pero con valor si se procesa | Sangre recuperada; plumas; cabezas; tracto digestivo; pulmones; otros no comestibles; huesos; residuo óseo de CMS; garras de descarte; grasa retirada | Rendering (harinas, grasa) u otro uso permitido |
| **D. Residuo / efluente** | Sin valor o con costo de tratamiento | Contenido gastrointestinal; sangre no recuperada; cutícula de patas; agua de goteo; decomisos* | Tratamiento de efluentes, residuos sólidos |
| **P. Pérdida** | Masa que sale sin corriente identificable | Evaporación (aire); mermas de trozado, deshuese y CMS; pérdidas no asignadas | Vapor, efluente difuso (a medir) |

\* Los decomisos se clasifican D por prudencia; si la normativa permite enviarlos a rendering serían C (DPV-066).

**Subproducto ≠ residuo.** Las plumas o la sangre tienen valor si existe rendering (propio o de terceros) y un comprador de harina; sin rendering, pasan a ser un residuo con costo de disposición. El contenido intestinal es residuo en cualquier caso. Una misma parte puede cambiar de clase según el mercado: las garras son B si hay comprador y C si no lo hay (ver [`17_exportacion/estrategia_valorizacion_ave.md` §2](../17_exportacion/estrategia_valorizacion_ave.md)). **La clase no es un precio.**

## 7. Balance de masa total

```
ENTRADAS                                   SALIDAS
Peso vivo (masa biológica)          =  A productos + B coproductos + C subproductos + D residuos + P pérdidas   (masa biológica)
Agua incorporada (chiller + plumas) =  agua retenida en A/B/C + agua en plumas húmedas + agua de goteo           (agua)
Error de cierre = (PV + agua incorporada) − Σ salidas      Tolerancia: 1 mg por ave (1e-6 kg); el modelo se detiene si se supera
```

**Ejemplo — pollo de 2,9 kg, configuración B (trozado), escenario medio, chiller por inmersión:**

| | Masa biológica (kg/ave) | Agua (kg/ave) | Total (kg/ave) | % PV (bio) |
|---|---|---|---|---|
| **Entradas:** peso vivo | 2,900 | — | 2,900 | 100,0 % |
| **Entradas:** agua incorporada (chiller 0,122 + plumas 0,090) | — | 0,213 | 0,213 | — |
| A. Productos principales (pechuga con hueso, pata-muslo) | 1,415 | 0,060 | 1,475 | 48,8 % |
| B. Coproductos comestibles | 0,896 | 0,026 | 0,921 | 30,9 % |
| C. Subproductos valorizables | 0,443 | 0,090 | 0,533 | 15,3 % |
| D. Residuos y efluentes (incluye decomisos 0,040) | 0,095 | 0,037 | 0,132 | 3,3 % |
| P. Pérdidas | 0,051 | 0 | 0,051 | 1,8 % |
| **Total salidas** | **2,900** | **0,213** | **3,113** | **100,0 %** |
| **Error de cierre** | | | **1,8 × 10⁻¹⁵ kg** | |

Detalle por componente y para las tres configuraciones: §8 y [`escenarios_balance.csv`](escenarios_balance.csv) (filas `CONTROL` de cada balance).

## 8. Tres configuraciones comerciales (pollo de 2,9 kg, escenario medio, inmersión)

Resumen; detalle de cortes y deshuese en [`rendimientos_cortes.md` §5](rendimientos_cortes.md). kg/ave de **masa biológica** (el agua retenida se muestra aparte). **No se decide cuál conviene.**

| Concepto | A. Pollo entero | B. Trozado | C. Deshuesado / mayor valor |
|---|---|---|---|
| Productos principales (A) | 1,999 (entero 1,914 + trozado de canales no aptas 0,085) | 1,415 (pechuga c/h 0,784; pata-muslo 0,631) | 1,103 (suprema 0,478; solomillo 0,118; muslo deshuesado 0,242; pata c/h 0,265) |
| Partes secundarias comestibles (alas, carcasa, menudencias, cuello, garras) | 0,320 | 0,886 | 0,728 (incluye CMS 0,236) |
| Hueso separado (C) | 0 (dentro del producto) | 0 (dentro de los cortes) | **0,317** (hueso 0,164 + residuo de CMS 0,153) |
| Piel separada (B) | 0 | 0 | 0,110 |
| Recortes (B) | 0,001 | 0,010 | 0,037 |
| Subproductos de faena (C: sangre, plumas, cabeza, vísceras, garras descarte) | 0,443 | 0,443 | 0,443 |
| Residuos D + pérdidas P | 0,136 | 0,146 | 0,161 |
| **Comestible total (A + B)** | **2,320** | **2,311** | **1,978** |
| Agua retenida en productos (inmersión) | 0,086 | 0,086 | 0,086 |

**Lectura:** trozar casi no cambia la masa comestible (−0,4 %: merma de sierra y exudado), pero **mueve ~0,58 kg por ave de "producto principal" a "coproducto"** (alas, carcasa-esqueleto). Deshuesar **saca ~0,33 kg de hueso y residuo por ave (−14 % de masa comestible)** y genera piel, recortes y CMS que necesitan un comprador (industria de elaborados). El deshuese solo tiene sentido si el valor de la carne sin hueso compensa la masa perdida más el costo del proceso: se evaluará con precios (no en esta sesión).

## 9. Escalado

Pollo de **2,9 kg**, configuración **B**, escenario medio, inmersión. Totales por clase = masa biológica + agua. t/año con **250 días de faena** (SUP-025, SUP-044); 1.000.000 aves/año ≡ 4.000 aves por día de faena.

| Clase | 1 ave (kg) | 1.000 aves (kg) | 2.500 aves/día (t/día) | 5.000 (t/día) | **10.000 (t/día)** | 20.000 (t/día) | 10.000 aves/día (t/año) | 1.000.000 aves/año (t/año) |
|---|---|---|---|---|---|---|---|---|
| **Entrada: pollo vivo** | 2,900 | 2.900 | 7,25 | 14,50 | **29,00** | 58,00 | 7.250 | 2.900 |
| Entrada: agua incorporada | 0,213 | 213 | 0,53 | 1,06 | **2,13** | 4,25 | 532 | 213 |
| A. Productos principales | 1,475 | 1.475 | 3,69 | 7,37 | **14,75** | 29,50 | 3.687 | 1.475 |
| B. Coproductos comestibles | 0,921 | 921 | 2,30 | 4,61 | **9,21** | 18,43 | 2.304 | 921 |
| C. Subproductos | 0,533 | 533 | 1,33 | 2,67 | **5,33** | 10,67 | 1.334 | 533 |
| D. Residuos y efluentes | 0,132 | 132 | 0,33 | 0,66 | **1,32** | 2,64 | 330 | 132 |
| P. Pérdidas | 0,051 | 51 | 0,13 | 0,25 | **0,51** | 1,02 | 127 | 51 |

Con 2,8 kg y 3,0 kg (misma configuración): A = 1,419 / 1,532 kg/ave; B = 0,892 / 0,951; C = 0,518 / 0,548; a 10.000 aves/día, A = 14,19 / 15,32 t/día. Todas las combinaciones de peso, configuración y escenario están en el CSV (columnas `kg_1000_aves`, `t_dia_*`, `t_anio_*`). El balance de 10.000 aves/día por componente está en [`conclusiones_balance.md` §5](conclusiones_balance.md).

**Escalar no es lineal en aves cuando cambia el peso**: para la misma tonelada de producto, aves más livianas exigen más aves (ver [`rendimientos_cortes.md` §6](rendimientos_cortes.md)). A peso fijo, el escalado es exactamente lineal (test T07).

## 10. Implicancias para etapas posteriores (sin calcular todavía)

| Uso posterior | Qué toma del balance |
|---|---|
| Ingreso potencial por ave (`17_exportacion/estrategia_valorizacion_ave.md`) | `k_i` = kg por parte por ave, por peso y configuración (columna `total_kg_ave`, clases A y B) |
| Frío y almacenamiento (`12_energia_frio`) | t/día de producto refrigerado (A + B ≈ 24 t/día a 10.000 aves de 2,9 kg); carcasa a enfriar ≈ 20,4 t/día; agua absorbida en el chiller ≈ 1,2 t/día |
| Efluentes (`11_agua_efluentes`) | Sangre no recuperada, contenido GI, goteo, cutícula, mermas (≈ 1,3 t/día de corrientes D a 10.000 aves/día) |
| Subproductos y rendering (`07_subproductos`) | ≈ 5,3 t/día de corrientes C (plumas húmedas 2,4; tracto 0,9; sangre 0,8; cabezas 0,7) |
| Productos (`06_productos`) | Mezcla de partes por configuración y peso |

## 11. Contradicciones y debilidades de las fuentes

| Tema | Contradicción o debilidad | Tratamiento | Registro |
|---|---|---|---|
| Rendimiento de carcasa Cobb 500 a ~2,8 kg | Un extracto da **74,03 %** (FTE-140) y otro **75,55–75,85 %** (FTE-161, calculadora de terceros); definición de "carcass" (con o sin cuello y menudencias) no confirmada | El modelo usa 71,5 % sin cuello (≈ 74,1 % con cuello) como campo medio, por debajo del objetivo genético | DPV-059 |
| Filet de pechuga Cobb a ~2,8 kg | **22,57 % PV** (FTE-140) vs **26,05–26,50 %** "boneless breast" (FTE-161) | Modelo: 20,5 % PV (campo medio); alto 21,1 % | DPV-059 |
| Suma de subproductos de la literatura | Plumas 6 + sangre 3,5 + cabeza 3 + patas 5 + vísceras no comestibles 9 = 26,5 %, más menudencias y cuello (~7 %) y carcasa (~72 %) = **~105 %** | Las fuentes mezclan pluma húmeda con seca, molleja sucia con limpia y otras definiciones; el modelo usa un conjunto coherente que cierra con 1,4 % de pérdidas no asignadas | §3; DPV-060 |
| Plumas: 5–7 % vs 8–9 % | Probablemente seca/biológica vs húmeda (con agua de escaldado) | Se separan masa biológica (5,2 %) y agua arrastrada (0,6 kg/kg) | SUP-040 |
| Molleja: 3,0 % PV | Probablemente molleja entera (con cutícula y contenido) en aves de 7 semanas | Modelo: 1,4 % limpia; cutícula y contenido en "otros no comestibles" | DPV-060 |
| Datos argentinos | Ningún rendimiento de faena argentino leído; hay estudios de la UNNE y de Formosa identificados pero no leídos (FTE-184) | Todo el modelo depende de literatura extranjera y supuestos | DPV-060 |
| Tablas genéticas vs campo | Las tablas son objetivos genéticos "dry yield" en condiciones ideales, no rendimientos de planta | Escenario "alto" ≈ tabla genética; "medio" 1–3 pp por debajo | SUP-037 |
