# Escenarios de escala — modelo preliminar físico

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad) · Carpeta `23_plan_expansion`

> **Pregunta:** ¿qué tiene que ser verdad para que una planta de **2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día** tenga sentido?
> **Alcance:** integra por primera vez demanda → aves → producción primaria → faena → productos → subproductos → frío e inventario (conceptual) → logística (conceptual) → exportación → expansión. **No** elige la escala, **no** calcula CAPEX, OPEX, precios ni indicadores financieros, **no** selecciona maquinaria, proveedores, layout ni localización. **No** asume que USD 2 M alcanzan ni que son un tope (regla 7).
> **Modelo:** [`modelo_escala.py`](modelo_escala.py) → [`escenarios_escala.csv`](escenarios_escala.csv) (4.232 filas; archivo maestro de las cifras; versión 1.1 tras la auditoría conceptual del 2026-09-30). El modelo **importa** los modelos de producción primaria (v1.1), balance de masa (v1.1) y subproductos (v1.0) sin modificarlos, y **lee** los escenarios de demanda. Todas las cifras son `[ESTIMACIÓN]` sobre supuestos ya registrados (SUP-019 a SUP-051) y los nuevos SUP-052 a SUP-059; **ninguna proviene de datos de campo argentinos**.
> Documentos hermanos: [`arquitectura_escalable.md`](arquitectura_escalable.md) (modularidad, arquitecturas de crecimiento, matriz sin ganador) · [`gates_expansion.md`](gates_expansion.md) · [`especificacion_simulador_html.md`](especificacion_simulador_html.md) · [`guia_ramiro.md`](guia_ramiro.md) · [`conclusiones_escala.md`](conclusiones_escala.md) · ritmos de faena en [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md).

**Referencia de todas las tablas salvo indicación:** perfil y desempeño **medios** de `03_produccion_primaria` (2,9 kg vivo, 47 días, FCR de campo 1,70, mortalidad en granja 5 %, en transporte 0,3 %, 35 kg/m², 15 días entre lotes); balance **v1.1** medio (rendimiento y condenas medios, chiller por inmersión); configuración **B trozado** con carcasa-esqueleto vendida (V1, SUP-050: referencia, **no decisión**).

---

## 1. Definición de capacidad (SUP-052)

| Término | Definición en este modelo |
|---|---|
| **Escala E** | Aves **efectivamente faenadas por día operativo** cuando la planta trabaja a su capacidad operativa. "10.000 aves/día" = 10.000 aves faenadas por día de faena, no aves alojadas, ni cargadas, ni vendidas |
| Capacidad nominal | Ritmo nominal de línea × horas netas. No se calcula (sin equipos seleccionados). Nominal ≥ operativa |
| Capacidad operativa | Lo que la planta puede sostener con sus restricciones reales; en el modelo es E |
| Aves realmente faenadas | E × utilización |
| Utilización | Aves realmente faenadas / capacidad operativa |

Detalle y cuello de botella: [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md) §1–§3. **Capacidad ≠ demanda ≠ ventas**: la demanda se compara con la capacidad (§4), nunca la define (test T12).

## 2. Escenarios base y calendarios (SUP-025)

Los dos calendarios se muestran **por separado**. Semana plena = semana sin feriados (ritmo nominal); los días calendario son la unidad de la demanda (SUP-020).

| Escala (aves faenadas/día operativo) | Aves/semana plena (5 d · 6 d) | Aves/año con 5 d/sem (250 d) | Aves/año con 6 d/sem (300 d) | Equivalente por día calendario (250 d · 300 d) |
|---|---|---|---|---|
| 2.500 | 12.500 · 15.000 | 625.000 | 750.000 | 1.712 · 2.055 |
| 5.000 | 25.000 · 30.000 | 1.250.000 | 1.500.000 | 3.425 · 4.110 |
| 10.000 | 50.000 · 60.000 | 2.500.000 | 3.000.000 | 6.849 · 8.219 |
| 20.000 | 100.000 · 120.000 | 5.000.000 | 6.000.000 | 13.699 · 16.438 |

**Sexto día de faena ≠ segundo turno.** Pasar de 250 a 300 días/año aumenta ~**20 % el volumen anual potencial** (aves, productos, alimento) y, en granjas, un 20 % los pollitos y m² de la semana plena, **manteniendo la misma capacidad diaria**: no aumenta 20 % las aves por día ni el ritmo de la línea (test T19). El segundo turno, en cambio, actúa sobre las **horas netas por día** (§3). El sexto día también exige personal, frío, pollitos y abastecimiento para ese día, y reduce los días disponibles para mantenimiento y limpieza profunda.

**Tres bases temporales que no se mezclan** (test T18):

| Base | Definición | Ejemplo: comestible comercial a 10.000 aves/día |
|---|---|---|
| Por día operativo (día de faena) | Lo que sale un día en que se faena | 23,96 t/día operativo (5 d y 6 d) |
| Por día calendario (promedio) | Producción anual ÷ 365; unidad de la demanda (SUP-020) | 16,41 t/día cal (250 d) · 19,70 (300 d) |
| Anual | Por día operativo × días operativos/año | 5.991 t/año (250 d) · 7.189 (300 d) |

Conversión: `por día calendario = por día operativo × días operativos / 365` (× 0,685 con 250 días; × 0,822 con 300). En el modelo, toda comparación entre demanda y capacidad pasa por la función `convertir`, y la función `cociente` **rechaza** comparar directamente t/día de faena con t/día calendario.

## 3. Capacidad horaria

Ritmo requerido = aves faenadas/día ÷ horas **netas** de faena. A 8 h netas: **312 / 625 / 1.250 / 2.500 aves/h** para las cuatro escalas; con 6 h netas, 417 a 3.333; con 16 h netas (dos turnos de 8 h), 156 a 1.250. Tabla completa, horas de turno vs netas y cuello de botella: [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md) §2–§4. No se asume eficiencia de máquina.

**Segundo turno = capacidad teórica de la línea, no capacidad de la planta.** Que 1.250 aves/h equivalgan a 10.000 aves/día con 8 h netas o a 20.000 con 16 h netas es aritmética de la **línea**. Antes de afirmar que un segundo turno permite 20.000 aves/día hay que comprobar los demás cuellos de botella (recepción de aves, colgado, eviscerado, chilling, salas de corte, mano de obra, cámaras, congelado, expedición, agua, efluentes, energía, refrigeración, limpieza y sanitización, mantenimiento, bienestar animal y logística de granjas; [`capacidad_preliminar.md` §3](../05_proceso_industrial/capacidad_preliminar.md)). **No se afirma** que 20.000 aves/día sean posibles "sin obra nueva".

---

## 4. Demanda vs capacidad

### 4.1 Punto de partida

- **Demanda documentada (A + B) ≈ 0 kg/día** → la utilización que hoy justifica la evidencia es **0 %** en las cuatro escalas (fila `utilizacion_con_demanda_documentada_A_mas_B` del CSV).
- Los escenarios comerciales de [`../02_clientes_demanda/escenarios_demanda.csv`](../02_clientes_demanda/escenarios_demanda.csv) son **hipótesis de prueba** (SUP-021), categoría **C/D**, `sumable_a_demanda = no`: conservador **1.500**, base **7.500**, expansivo **23.500 kg de producto/día calendario**; **exportación 0** en todos (SUP-022). Los ~90 supermercados son potenciales/condicionales.

### 4.2 Cómo se convierten kg de demanda en aves (SUP-054)

La demanda está en **kg de producto por día calendario**; la planta, en **aves faenadas por día operativo**. No se usa un único rendimiento porque **el mix cambia las aves necesarias**. Se calculan dos cotas con el balance v1.1:

| Método | Supuesto | Qué da |
|---|---|---|
| **M0 — ave completa** | Toda la masa comestible del ave (A + B: pechuga, pata-muslo, alas, carcasa-esqueleto, cuello, menudencias, garras, recortes; 2,40 kg/ave comercial en B) se vende dentro de la demanda | **Cota inferior** de aves. Optimista: supone que la carcasa y las garras encuentran comprador en el mismo escenario |
| **M1 / M2 / M3 — parte limitante** | Mixes hipotéticos de [`../02_clientes_demanda/supermercados.md`](../02_clientes_demanda/supermercados.md) §2.2 (SUP-023) aplicados a toda la demanda, con los **rendimientos del balance v1.1** (pollo entero 1,995 kg; suprema + solomillo 0,621; pata-muslo 0,658; alas 0,216; menudencias 0,109 kg/ave) y 0,75 kg de pechuga por kg de milanesa | Aves fijadas por la parte más demandada (**la pechuga en los tres mixes**) y **excedentes de partes** que necesitan otros compradores |

Con los rendimientos del balance, el factor de mix frente a la fórmula simple de la demanda (kg ÷ 2,1 kg/ave) resulta **1,19 / 1,36 / 1,56** para M1 / M2 / M3 (el estudio de demanda estimaba 1,15 / 1,33 / 1,53 con rendimientos ilustrativos: la dirección se confirma). Frente a M0, las aves necesarias son **1,36 / 1,56 / 1,78 veces** mayores.

**Limitaciones:** (1) los mixes son de supermercado y se aplican a toda la demanda (los otros canales podrían absorber las partes excedentes, lo que acercaría el resultado a M0); (2) "otros elaborados" (5–13 % del kg) quedan fuera del balance (SUP-023); (3) la exportación es 0; (4) la pechuga deshuesada se toma de la configuración C y la pata-muslo de la B sobre la misma carcasa fría (combinación físicamente coherente, con diferencias de agua retenida despreciables); (5) no hay estacionalidad: la demanda es un promedio diario.

### 4.3 Tres métricas que no deben confundirse (SUP-060)

| Métrica | Fórmula | Rango | Lectura |
|---|---|---|---|
| **Factor demanda/capacidad** | aves que requiere la demanda ÷ capacidad instalada (ambas por día calendario) | 0 a ∞ | 100 % = coincide con la capacidad; **> 100 % = la escala no alcanza**; < 100 % = existe capacidad ociosa. **No es utilización** |
| **Utilización de planta** | aves efectivamente procesadas ÷ capacidad = mín(factor; 100 %) | 0–100 % | Si la demanda excede la capacidad, la planta está al 100 % y el resto es **demanda no atendida** |
| **Cobertura de demanda** | producción posible ÷ demanda requerida = mín(1 ÷ factor; 100 %) | 0–100 % | Parte de la demanda que la escala puede atender |

Además: **kg atendidos** = demanda × cobertura; **kg no atendidos** = demanda × (1 − cobertura); **capacidad ociosa** = escala × (1 − utilización), en aves/día operativo. La demanda está en kg de **peso comercial** por **día calendario**; la capacidad, en aves por **día operativo**: se comparan después de convertir la capacidad a día calendario.

**Tabla corregida — 5 d/sem (250 d).** Cada celda: **factor · utilización · cobertura** (%).

| Escenario (kg/día cal) | Método | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Conservador (1.500) | M0 | 37 · 37 · 100 | 18 · 18 · 100 | 9 · 9 · 100 | 5 · 5 · 100 |
| | M1–M3 | 50–65 · 50–65 · 100 | 25–33 · 25–33 · 100 | 12–16 · 12–16 · 100 | 6–8 · 6–8 · 100 |
| **Base (7.500)** | M0 | **183 · 100 · 55** | 91 · 91 · 100 | 46 · 46 · 100 | 23 · 23 · 100 |
| | M1–M3 | 248–326 · 100 · 31–40 | 124–163 · 100 · 61–81 | 62–81 · 62–81 · 100 | 31–41 · 31–41 · 100 |
| Expansivo (23.500) | M0 | 573 · 100 · 17 | 286 · 100 · 35 | **143 · 100 · 70** | 72 · 72 · 100 |
| | M1–M3 | 776–1.021 · 100 · 10–13 | 388–511 · 100 · 20–26 | 194–255 · 100 · 39–52 | 97–128 · 97–100 · 78–100 |

**6 d/sem (300 d)**, mismo formato:

| Escenario | Método | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Conservador | M0 | 30 · 30 · 100 | 15 · 15 · 100 | 8 · 8 · 100 | 4 · 4 · 100 |
| | M1–M3 | 41–54 · 41–54 · 100 | 21–27 · 21–27 · 100 | 10–14 · 10–14 · 100 | 5–7 · 5–7 · 100 |
| Base | M0 | 152 · 100 · 66 | 76 · 76 · 100 | 38 · 38 · 100 | 19 · 19 · 100 |
| | M1–M3 | 206–272 · 100 · 37–48 | 103–136 · 100 · 74–97 | 52–68 · 52–68 · 100 | 26–34 · 26–34 · 100 |
| Expansivo | M0 | 477 · 100 · 21 | 239 · 100 · 42 | 119 · 100 · 84 | 60 · 60 · 100 |
| | M1–M3 | 647–851 · 100 · 12–15 | 323–426 · 100 · 23–31 | 162–213 · 100 · 47–62 | 81–106 · 81–100 · 94–100 |

Aves necesarias por día operativo (5 d): conservador 914 (M0) a 1.630 (M3); base 4.569 a 8.149; expansivo 14.317 a 25.534.

### 4.4 kg atendidos, no atendidos, capacidad ociosa y kg sin destino

5 d/sem. Cada celda: **kg/día cal atendidos / no atendidos / capacidad ociosa (aves/día operativo)**. Debajo, con la planta operando a plena escala: kg/día cal **sin destino** dentro del escenario (incluye partes excedentes del mix) / **demanda adicional** (mismo mix) para llenarla.

| Escenario | Método | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Conservador | M0 | 1.500 / 0 / 1.586 | 1.500 / 0 / 4.086 | 1.500 / 0 / 9.086 | 1.500 / 0 / 19.086 |
| | — sin destino / adicional | 2.604 / 2.604 | 6.707 / 6.707 | 14.914 / 14.914 | 31.329 / 31.329 |
| | M2 | 1.500 / 0 / 1.078 | 1.500 / 0 / 3.578 | 1.500 / 0 / 8.578 | 1.500 / 0 / 18.578 |
| | — sin destino / adicional | 2.592 / 1.137 | 6.549 / 3.773 | 14.464 / 9.046 | 30.292 / 19.592 |
| Base | M0 | 4.104 / **3.396** / 0 | 7.500 / 0 / 431 | 7.500 / 0 / 5.431 | 7.500 / 0 / 15.431 |
| | — sin destino / adicional | 0 / 0 | 707 / 707 | 8.914 / 8.914 | 25.329 / 25.329 |
| | M2 | 2.637 / **4.863** / 0 | 5.273 / **2.227** / 0 | 7.500 / 0 / 2.888 | 7.500 / 0 / 12.888 |
| | — sin destino / adicional | 1.558 / 0 | 3.116 / 0 | 9.004 / 3.046 | 24.832 / 13.592 |
| Expansivo | M0 | 4.104 / **19.396** / 0 | 8.207 / **15.293** / 0 | 16.414 / **7.086** / 0 | 23.500 / 0 / 5.683 |
| | — sin destino / adicional | 0 / 0 | 0 / 0 | 0 / 0 | 9.329 / 9.329 |
| | M2 | 2.637 / **20.863** / 0 | 5.273 / **18.227** / 0 | 10.546 / **12.954** / 0 | 21.092 / **2.408** / 0 |
| | — sin destino / adicional | 1.558 / 0 | 3.116 / 0 | 6.232 / 0 | 12.463 / 0 |

Con 6 d/sem, todas las combinaciones en el CSV (bloque `demanda_capacidad`).

**Ejemplo: 10.000 aves/día (5 d/sem · 250 días)** — capacidad = 10.000 aves/día operativo = 6.849 aves/día calendario:

| Escenario | Método | Aves requeridas/día operativo | Factor | Utilización | Cobertura | kg/día cal atendidos | No atendidos | Capacidad ociosa (aves/día op.) | Partes excedentes (kg/día cal) |
|---|---|---|---|---|---|---|---|---|---|
| Conservador | M0 | 914 | 9 % | 9 % | 100 % | 1.500 | 0 | 9.086 | 0 |
| | M1–M3 | 1.238–1.630 | 12–16 % | 12–16 % | 100 % | 1.500 | 0 | 8.370–8.762 | 592–1.336 |
| Base | M0 | 4.569 | 46 % | 46 % | 100 % | 7.500 | 0 | 5.431 | 0 |
| | M1–M3 | 6.192–8.149 | 62–81 % | 62–81 % | 100 % | 7.500 | 0 | 1.851–3.808 | 2.961–6.682 |
| Expansivo | M0 | 14.317 | 143 % | **100 %** | 70 % | 16.414 | **7.086** | 0 (faltan 4.317 aves/día) | 0 |
| | M1–M3 | 19.403–25.534 | 194–255 % | **100 %** | 39–52 % | 9.203–12.112 | **11.388–14.297** | 0 (faltan 9.403–15.534) | 4.782–8.200* |

\* Partes excedentes de la fracción atendida (kg sin destino con la planta llena). Con 6 d/sem (300 días) el expansivo M0 queda en factor 119 %, utilización 100 %, cobertura 84 % y 3.803 kg/día cal no atendidos.

**Lecturas:**

1. **Con la evidencia actual, ninguna escala está justificada** (utilización documentada 0 %). Todo lo que sigue compara hipótesis.
2. **2.500 aves/día** no alcanza para el escenario base: factor 183 % con ave completa (la planta estaría al 100 % y quedarían 3,4 t/día cal sin atender); con el conservador, utilización 37–65 %.
3. **5.000** es la escala más cercana al escenario base con ave completa (utilización 91 %); con mix de supermercado la base la excede (factor 124–163 %; cobertura 61–81 %).
4. **10.000** necesita **más que el escenario base**: utilización 46 % con ave completa y 62–81 % con mix; para llenarla falta demanda por **~9 t/día calendario** (M0).
5. **20.000** solo se acerca a llenarse con el **escenario expansivo** (utilización 72 % con ave completa; factor 97–128 % con mix), que supone los 90 locales a 150 kg/día más una cartera multicanal desarrollada que hoy no existe.
6. **Aunque la escala coincida con la demanda, sobran partes:** con mix M2, aun cuando la planta está llena, quedan 1,6–12,5 t/día calendario de partes (pata-muslo, alas, carcasa, cuello, garras) que necesitan **otros canales**. Esas toneladas son el costo físico de no vender el ave completa (SUP-013).

---

## 5. Utilización de capacidad

Escala × utilización, 5 d/sem (250 d). Con 6 d/sem todo +20 % (CSV). t vivas = peso vivo en planta; producto principal = clase A (pechuga con hueso + pata-muslo); comestible = A + B con agua retenida; subproductos = clase C.

| Escala | Utilización | Aves/día | Aves/año | t vivas/año | Producto principal t/año | Comestible t/año | Subproductos C t/año | Pollitos BB/año | Alimento t/año |
|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 30 % | 750 | 187.500 | 544 | 277 | 449 | 100 | 197.962 | 927 |
| | 50 % | 1.250 | 312.500 | 906 | 461 | 749 | 167 | 329.937 | 1.545 |
| | 70 % | 1.750 | 437.500 | 1.269 | 645 | 1.048 | 233 | 461.912 | 2.163 |
| | 85 % | 2.125 | 531.250 | 1.541 | 784 | 1.273 | 283 | 560.893 | 2.627 |
| | 100 % | 2.500 | 625.000 | 1.812 | 922 | 1.498 | 333 | 659.874 | 3.091 |
| 5.000 | 30 % | 1.500 | 375.000 | 1.088 | 553 | 899 | 200 | 395.925 | 1.854 |
| | 50 % | 2.500 | 625.000 | 1.812 | 922 | 1.498 | 333 | 659.874 | 3.091 |
| | 70 % | 3.500 | 875.000 | 2.538 | 1.291 | 2.097 | 467 | 923.824 | 4.327 |
| | 85 % | 4.250 | 1.062.500 | 3.081 | 1.567 | 2.546 | 567 | 1.121.786 | 5.254 |
| | 100 % | 5.000 | 1.250.000 | 3.625 | 1.844 | 2.996 | 667 | 1.319.749 | 6.181 |
| 10.000 | 30 % | 3.000 | 750.000 | 2.175 | 1.106 | 1.797 | 400 | 791.849 | 3.709 |
| | 50 % | 5.000 | 1.250.000 | 3.625 | 1.844 | 2.996 | 667 | 1.319.749 | 6.181 |
| | 70 % | 7.000 | 1.750.000 | 5.075 | 2.581 | 4.194 | 933 | 1.847.648 | 8.653 |
| | 85 % | 8.500 | 2.125.000 | 6.162 | 3.134 | 5.093 | 1.133 | 2.243.573 | 10.508 |
| | 100 % | 10.000 | 2.500.000 | 7.250 | 3.687 | 5.991 | 1.334 | 2.639.497 | 12.362 |
| 20.000 | 30 % | 6.000 | 1.500.000 | 4.350 | 2.212 | 3.595 | 800 | 1.583.698 | 7.417 |
| | 50 % | 10.000 | 2.500.000 | 7.250 | 3.687 | 5.991 | 1.334 | 2.639.497 | 12.362 |
| | 70 % | 14.000 | 3.500.000 | 10.150 | 5.162 | 8.388 | 1.867 | 3.695.296 | 17.307 |
| | 85 % | 17.000 | 4.250.000 | 12.325 | 6.269 | 10.185 | 2.267 | 4.487.146 | 21.016 |
| | 100 % | 20.000 | 5.000.000 | 14.500 | 7.375 | 11.982 | 2.667 | 5.278.995 | 24.724 |

**Una planta de 20.000 aves/día al 50 % procesa físicamente lo mismo que una de 10.000 al 100 %** (y una de 10.000 al 50 %, lo mismo que una de 5.000 llena). La diferencia está en todo lo que se construyó y no se usa.

**Por qué una planta grande con baja utilización puede ser un problema** (conceptual; sin costos, que se calcularán después):

1. **Lo fijo no se achica con la utilización:** edificio, cámaras, equipos, sala de máquinas, tratamiento de efluentes, habilitaciones, estructura y buena parte del personal existen igual si se faena al 30 % o al 100 %. Cada ave faenada carga con una porción mayor de lo fijo.
2. **Equipos fuera de su rango:** una línea, un chiller o un túnel diseñados para un ritmo operan peor muy por debajo de él (paradas y arranques, lotes cortos, frío sobredimensionado, efluente con caudal y carga variables). El dato técnico se verificará en la fase de maquinaria.
3. **Capital inmovilizado sin producir:** el capital de la capacidad ociosa no genera producto; si además es capital de terceros, exige retorno desde el primer día.
4. **Presión para "llenar":** la capacidad ociosa empuja a vender a cualquier precio o a aceptar clientes y mixes que desbalancean el ave (§4.4 lectura 6) — el riesgo inverso al del principio de ingreso total por ave.
5. **La capacidad futura atractiva no paga el presente:** la opción de crecer se puede preservar con **terreno, servicios y diseño modular** sin construir toda la capacidad hoy ([`arquitectura_escalable.md`](arquitectura_escalable.md)).

---

## 6. Producción primaria necesaria (escenario medio, desde el modelo v1.1)

Valores **importados** de [`../03_produccion_primaria/modelo_escenarios_produccion.py`](../03_produccion_primaria/modelo_escenarios_produccion.py) (función `calcular`), sin recálculo manual; coinciden con [`../03_produccion_primaria/conclusiones_produccion.md`](../03_produccion_primaria/conclusiones_produccion.md) §3–§5 (test T10). Formato **5 d/sem (250 d) · 6 d/sem (300 d)**; utilización 100 %.

| Variable | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Pollitos BB alojados / **semana plena** | 13.197 · 15.837 | 26.395 · 31.674 | 52.790 · 63.348 | 105.580 · 126.696 |
| Pollitos BB / semana promedio anual | 12.655 · 15.186 | 25.310 · 30.372 | 50.620 · 60.745 | 101.241 · 121.489 |
| Pollitos BB / año | 659.874 · 791.849 | 1.319.749 · 1.583.698 | 2.639.497 · 3.167.397 | 5.278.995 · 6.334.794 |
| Aves cargadas en granja / año | 626.881 · 752.257 | 1.253.761 · 1.504.514 | 2.507.523 · 3.009.027 | 5.015.045 · 6.018.054 |
| Aves faenadas / año | 625.000 · 750.000 | 1.250.000 · 1.500.000 | 2.500.000 · 3.000.000 | 5.000.000 · 6.000.000 |
| **Plazas simultáneas** (capacidad de alojamiento) | 120.507 · 144.609 | 241.014 · 289.217 | 482.029 · 578.435 | 964.058 · 1.156.870 |
| **m² de galpón** | 9.486 · 11.383 | 18.971 · 22.766 | 37.943 · 45.531 | 75.885 · 91.062 |
| Galpones equivalentes de 1.200 m² | 7,9 · 9,5 | 15,8 · 19,0 | 31,6 · 37,9 | 63,2 · 75,9 |
| Galpones equivalentes de 2.400 m² | 4,0 · 4,7 | 7,9 · 9,5 | 15,8 · 19,0 | 31,6 · 37,9 |
| **Alimento t / semana plena** | 62 · 74 | 124 · 148 | 247 · 297 | 494 · 593 |
| Alimento t / año | 3.091 · 3.709 | 6.181 · 7.417 | 12.362 · 14.835 | 24.724 · 29.669 |
| Alimento de un ciclo de crianza (capital de trabajo físico, t) | 415 · 498 | 830 · 996 | 1.660 · 1.992 | 3.320 · 3.984 |
| Agua de bebida m³ / semana plena | 111 · 134 | 223 · 267 | 445 · 534 | 890 · 1.068 |
| Agua de bebida m³ / año | 5.563 · 6.676 | 11.126 · 13.351 | 22.252 · 26.702 | 44.504 · 53.404 |
| **Aves vivas simultáneas** (ritmo pleno) | 86.396 · 103.676 | 172.793 · 207.351 | 345.586 · 414.703 | 691.171 · 829.406 |

Galpones = equivalentes de superficie sin redondear ni reserva, **no una recomendación de cuántos construir** (SUP-031). El agua es solo de bebida (sin *cooling* ni lavado). Rango completo con otros perfiles y desempeños: CSV de producción (72 escenarios); los supuestos mueven los m² hasta ~3,3 veces.

## 7. Tres modelos de abastecimiento por escala (sin ganador, DEC-020)

Comparación general en [`../03_produccion_primaria/modelos_integracion.md`](../03_produccion_primaria/modelos_integracion.md). Aquí, **qué cambia con la escala**.

**Productores necesarios** = m² de galpón ÷ m² por productor. El m² por productor es **variable pendiente** (DPV-048). Aritmética ilustrativa con galpones equivalentes de 2.400 m² (5 d/sem):

| Escala | m² de galpón | Si cada productor tiene 1 galpón de 2.400 m² | 2 galpones | 4 galpones |
|---|---|---|---|---|
| 2.500 | 9.486 | 4,0 | 2,0 | 1,0 |
| 5.000 | 18.971 | 7,9 | 4,0 | 2,0 |
| 10.000 | 37.943 | 15,8 | 7,9 | 4,0 |
| 20.000 | 75.885 | 31,6 | 15,8 | 7,9 |

| Escala | A. Granjas propias | B. Productores integrados | C. Modelo mixto |
|---|---|---|---|
| 2.500 | ~9.500 m², ~121.000 plazas propias: la granja es un proyecto en sí mismo, comparable en complejidad a la planta | Pocos productores (1–4 según tamaño): alta dependencia de cada uno; un productor que se va = 25–100 % del abastecimiento | Base propia chica + 1–2 integrados + compra spot como amortiguador |
| 5.000 | ~19.000 m²; varios sitios por bioseguridad | 2–8 productores: empieza a requerir técnico de campo propio y logística de alimento y pollitos organizada | Mezcla razonable para aprender la crianza sin inmovilizar todo el capital |
| 10.000 | ~38.000 m²; ~482.000 plazas: inversión en galpones significativa (no calculada; DEC-022); la integración existe en el sector precisamente para trasladarla al productor | 4–16 productores: estructura de integración (contratos, pagos, auditorías, asistencia técnica) | Varias combinaciones; la proporción propia/integrada es una decisión de capital y riesgo |
| 20.000 | ~76.000 m²; ~964.000 plazas en muchos sitios dispersos | 8–32 productores: gestión de una red; disponibilidad real en el radio de la planta desconocida (DPV-048) | Probablemente la única forma de no concentrar riesgo sanitario ni capital, pero exige los dos know-how |

**Qué aumenta con la escala** (todo lineal con las aves, salvo lo indicado):

| Variable | 2.500 → 20.000 | Comentario |
|---|---|---|
| Capital inmovilizado en granjas (modelo A) | ×8 en m² y plazas | CAPEX no calculado |
| Capital de trabajo en alimento (modelos A y B) | 415 → 3.320 t de alimento por ciclo de crianza | Físico; sin plazos de pago/cobro |
| Coordinación | ×8 en lotes, cargas y visitas; los productores crecen con la escala y con la **dispersión** | Más productores = más contratos y más variabilidad de desempeño |
| Alimento | 62 → 494 t/semana plena | Estrategia de alimento (DEC-024) pesa más a mayor escala |
| Pollitos BB | 13.200 → 105.600 por semana plena | Oferta concentrada; ampliar reproductoras lleva ~6–7 meses (`03_produccion_primaria`) |
| Transporte | Aves vivas 7,3 → 58,2 t/día operativo; alimento 8,8 → 70,6 t/día | §12 |
| Riesgo sanitario | Más sitios y movimientos → más puntos de entrada; pero más dispersión → menos impacto de un brote en un sitio | La relación no es monótona (DEC-025) |
| Productores necesarios | Fórmula anterior; dato real DPV-048 | No se inventa |

---

## 8. Balance de productos por escala (balance v1.1, 2,9 kg, trozado V1)

t/día operativo · t/año (250 d). Masa comercial = masa biológica + agua retenida en producto; subproductos con agua adherida. Los 12 ítems pedidos más "otros" suman exactamente la entrada (pollo vivo + agua incorporada; test T06). **No se alteraron rendimientos**; rutas exclusivas respetadas (carcasa-esqueleto **vendida**, no CMS).

| Salida | kg/ave | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Pechuga con hueso | 0,817 | 2,04 · 511 | 4,09 · 1.021 | 8,17 · 2.043 | 16,34 · 4.085 |
| Pata-muslo | 0,658 | 1,64 · 411 | 3,29 · 822 | 6,58 · 1.645 | 13,16 · 3.290 |
| Alas | 0,216 | 0,54 · 135 | 1,08 · 271 | 2,16 · 541 | 4,33 · 1.082 |
| Carcasa-esqueleto | 0,410 | 1,02 · 256 | 2,05 · 512 | 4,10 · 1.024 | 8,19 · 2.048 |
| Cuello | 0,075 | 0,19 · 47 | 0,37 · 93 | 0,75 · 187 | 1,49 · 373 |
| Menudencias (hígado, corazón, molleja) | 0,109 | 0,27 · 68 | 0,55 · 136 | 1,09 · 273 | 2,18 · 545 |
| Garras (grado A + segunda) | 0,101 | 0,25 · 63 | 0,51 · 126 | 1,01 · 253 | 2,02 · 505 |
| Sangre recuperada | 0,084 | 0,21 · 52 | 0,42 · 105 | 0,84 · 210 | 1,68 · 419 |
| Plumas húmedas | 0,241 | 0,60 · 151 | 1,21 · 302 | 2,41 · 603 | 4,83 · 1.206 |
| Vísceras no comestibles | 0,131 | 0,33 · 82 | 0,65 · 163 | 1,30 · 326 | 2,61 · 652 |
| Cabezas | 0,072 | 0,18 · 45 | 0,36 · 91 | 0,72 · 181 | 1,45 · 362 |
| Residuos y efluentes (clase D) | 0,132 | 0,33 · 82 | 0,66 · 165 | 1,32 · 330 | 2,64 · 660 |
| Otros (recortes, garras de descarte, mermas y pérdidas) | 0,067 | 0,17 · 42 | 0,33 · 83 | 0,67 · 167 | 1,33 · 334 |
| **Entrada: pollo vivo** (+ agua incorporada 0,213 kg/ave) | 2,900 | 7,25 · 1.812 | 14,5 · 3.625 | 29,0 · 7.250 | 58,0 · 14.500 |

**No mezclar toneladas vivas con comerciales:** de 29,0 t vivas/día (10.000 aves) salen 24,0 t de comestible, de las cuales 14,7 t son producto principal. Con 6 d/sem, t/año +20 %.

## 9. Configuraciones comerciales (físico; sin margen)

A = mayoría pollo entero (V6), B = mayoría trozado (V1), C = mayor participación de deshuesado / valor agregado (V3: pechuga y muslo deshuesados, carcasa-esqueleto a CMS). t/día operativo a **10.000 aves/día**; el resto de las escalas es proporcional (×0,25 / ×0,5 / ×2).

| Variable física | A. Entero | B. Trozado | C. Deshuesado |
|---|---|---|---|
| Producto principal (clase A) | 20,83 | 14,75 | 11,50 |
| Partes secundarias comestibles (clase B) | 3,23 | 9,21 | 9,01 |
| Huesos separados + residuo óseo de CMS | 0 | 0 | 3,31 |
| Recortes y piel comestibles | 0,01 | 0,11 | 1,53 |
| CMS producida | 0 | 0 | 2,46 |
| CMS potencial alternativa (excluyente con vender la carcasa; **no sumable**) | 0,14 | 2,36 | — |
| Comestible total (A + B) | 24,06 | 23,96 | 20,50 |
| Subproductos C (a rendering potencial) | 5,33 | 5,33 | 8,64 |
| Masa que pasa por trozado (proxy de procesamiento) | 1,22 | 20,36 | 16,43 |
| Masa que pasa por deshuese | 0 | 0 | 11,50 |
| Materia prima que pasa por separación mecánica (CMS) | 0 | 0 | 3,93 |
| Flujos comestibles distintos (proxy de frío y canales) | 12 | 11 | 14 |
| t de coproductos por t de producto principal (necesidad de colocar coproductos) | 0,16 | 0,62 | 0,78 |

**Requerimiento relativo:**

| | A | B | C | Base física |
|---|---|---|---|---|
| Procesamiento | MENOR | MEDIO | MAYOR | Masa trozada 1,2 vs 20,4 vs 16,4 t/día + 11,5 t deshuesadas + 3,9 t a CMS |
| Frío | MEDIO | MEDIO | MAYOR | El tonelaje comestible es similar en A y B; C agrega flujos (14), CMS con 12 h refrigerada o congelado (SUP-048) y piel/recortes. La proporción congelada depende del canal, no de la configuración |
| Colocación de coproductos | MENOR | MAYOR | MAYOR | 0,16 vs 0,62 vs 0,78 t por t de producto principal; en C, además, 3,3 t/día de hueso y 1,5 t de recortes y piel |

El entero **no elimina** las partes: un 6 % de las canales no es apto para entero y se troza (SUP-041), y cuello, menudencias y garras salen igual. El deshuese **no crea masa**: resta 3,5 t/día de comestible (hueso a subproducto) y agrega corrientes que necesitan comprador. **No se decide** (DEC-005).

## 10. Subproductos y escala

t/día operativo (B trozado salvo indicación). Sin rendering propio (SUP-049).

| Material | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Plumas húmedas | 0,60 | 1,21 | 2,41 | 4,83 |
| Sangre recuperable (85 % de la drenada) | 0,21 | 0,42 | 0,84 | 1,68 |
| Sangre drenada total (no sumar con la anterior) | 0,25 | 0,49 | 0,99 | 1,97 |
| Vísceras no comestibles | 0,33 | 0,65 | 1,30 | 2,61 |
| Cabezas | 0,18 | 0,36 | 0,72 | 1,45 |
| Garras (grado A + segunda; comestible) | 0,25 | 0,51 | 1,01 | 2,02 |
| Carcasa-esqueleto (comestible, sin comprador identificado) | 1,02 | 2,05 | 4,10 | 8,19 |
| Huesos (solo config. C) | 0,83 | 1,65 | 3,31 | 6,62 |
| **Materia prima potencial de rendering** (toda la clase C), B | **1,33** | **2,67** | **5,33** | **10,67** |
| Ídem, config. C | 2,16 | 4,32 | 8,64 | 17,29 |
| Sólidos a retirar (C + decomisos + contenido GI), B | 1,52 | 3,04 | 6,08 | 12,17 |

**¿Cuándo dejan de ser "unos kilos" y pasan a ser un flujo industrial diario?**

- **En todas las escalas son flujos diarios**: sangre y vísceras se degradan en horas y la pluma húmeda no se almacena; aun 1,3 t/día a 2,5 mil aves exigen **retiro todos los días de faena**. Lo que cambia con la escala no es la frecuencia sino la **naturaleza del problema**:
  - **2.500–5.000 aves/día (1,3–3,0 t/día de C y sólidos):** el problema es **comercial y logístico**: encontrar un receptor dispuesto a retirar volúmenes chicos todos los días a una distancia viable (DPV-065, DPV-080). Sin receptor, los subproductos son un **costo** y un riesgo ambiental.
  - **10.000 aves/día (5,3 t/día de C; 2,4 t de plumas; 6,1 t de sólidos):** ya es un **flujo industrial** que ocupa su propio circuito de contenedores, frío o proceso inmediato y transporte diario, y que un receptor puede valorar como materia prima regular.
  - **20.000 aves/día (10,7–17,3 t/día de C):** es el rango que [`../07_subproductos/rendering.md`](../07_subproductos/rendering.md) toma como referencia de **alimentación continua de un proceso** (5–17 t/día); la pregunta "¿rendering propio?" pasa a ser pertinente, aunque **no se decide** (DEC-027) y el umbral técnico-económico **no está relevado**.
- La **sangre** recuperada (0,2–1,7 t/día) reduce ~7 veces la DQO que llegaría al efluente ([`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md)): a mayor escala, peor el efecto de no recuperarla.
- La **carcasa-esqueleto** (1,0–8,2 t/día) es comestible pero sin comprador identificado: a 20.000 aves/día son más de 2.000 t/año que, sin canal, bajan a subproducto (SUP-046).

## 11. Inventario y frío — modelo conceptual

**No se diseñan** cámaras, potencia frigorífica ni equipos. Dos bases temporales distintas (SUP-056; test T21):

| Concepto | Fórmula | Pregunta que responde |
|---|---|---|
| **Días de producción en stock** | producción comercial por día **operativo** × días equivalentes de producción | ¿Cuántas jornadas de faena caben en la cámara? |
| **Días calendario de cobertura** | despacho promedio por día **calendario** × días calendario | ¿Cuántos días de venta (calendario) cubre el stock? Despacho promedio = producción × días operativos / 365 |

Con 250 días de faena, **7 días calendario de cobertura** equivalen a **~4,8 días de producción** (7 × 250/365): a 10.000 aves/día son **115 t**, no 168 t. Con 300 días, 138 t. El simulador debe mostrar siempre cuál de las dos bases se usa.

**Comestible total (A + B, peso comercial, cota superior), t** — días de producción · días calendario (5 d/sem · 250 d):

| Escala | 1 día | 3 días | 7 días | 14 días |
|---|---|---|---|---|
| 2.500 | 6,0 · 4,1 | 18,0 · 12,3 | 41,9 · 28,7 | 83,9 · 57,4 |
| 5.000 | 12,0 · 8,2 | 35,9 · 24,6 | 83,9 · 57,4 | 167,8 · 114,9 |
| 10.000 | 24,0 · 16,4 | 71,9 · 49,2 | 167,8 · 114,9 | 335,5 · 229,8 |
| 20.000 | 47,9 · 32,8 | 143,8 · 98,5 | 335,5 · 229,8 | 671,0 · 459,6 |

Con 6 d/sem (300 d) los días de producción no cambian y los días calendario pasan a 4,9 / 9,8 / 19,7 / 39,4 t por día (p. ej. 7 días calendario a 10.000 aves/día = 137,9 t).

**Subproductos que requieren frío** si no se retiran en el día (clase C sin plumas: sangre, vísceras, cabezas, huesos), en **días de producción** (solo se generan en días de faena), t: 1 / 3 / 7 / 14 días = 0,7 / 2,2 / 5,1 / 10,2 (2.500) · 1,5 / 4,4 / 10,2 / 20,4 (5.000) · 2,9 / 8,8 / 20,4 / 40,9 (10.000) · 5,8 / 17,5 / 40,9 / 81,8 (20.000).

**Separación por destino** con tres perfiles **ilustrativos** (SUP-055; no son demanda): P1 mercado interno fresco (90 % refrigerado / 10 % congelado), P2 interno con congelado (60 / 40), P3 opción exportadora (50 / 30 / 20 % exportación). Refrigerado con 3 días; congelado y exportación con 14 días; t para 2.500 / 5.000 / 10.000 / 20.000:

| Base temporal | Perfil | Refrigerado (3 d) | Congelado (14 d) | Exportación (14 d) |
|---|---|---|---|---|
| Días de producción | P1 | 16,2 / 32,4 / 64,7 / 129,4 | 8,4 / 16,8 / 33,6 / 67,1 | 0 |
| | P2 | 10,8 / 21,6 / 43,1 / 86,3 | 33,6 / 67,1 / 134,2 / 268,4 | 0 |
| | P3 | 9,0 / 18,0 / 35,9 / 71,9 | 25,2 / 50,3 / 100,7 / 201,3 | 16,8 / 33,6 / 67,1 / 134,2 |
| Días calendario | P1 | 11,1 / 22,2 / 44,3 / 88,6 | 5,7 / 11,5 / 23,0 / 46,0 | 0 |
| | P2 | 7,4 / 14,8 / 29,5 / 59,1 | 23,0 / 46,0 / 91,9 / 183,8 | 0 |
| | P3 | 6,2 / 12,3 / 24,6 / 49,2 | 17,2 / 34,5 / 68,9 / 137,9 | 11,5 / 23,0 / 46,0 / 91,9 |

Todas las combinaciones (1/3/7/14 días × 2 bases × perfiles × calendarios) en el CSV (bloque `inventario`, parámetro `base_temporal`). **Lecturas:** (1) el producto refrigerado vive días (SUP-051): su inventario es corto y el frío que exige es sobre todo de **enfriamiento rápido y despacho**; (2) el congelado y la exportación **acumulan**: 14 días de producción congelada a 20.000 aves/día con el perfil P2 son ~270 t en stock; (3) el inventario es **capital de trabajo físico**, y depende más del **canal y del perfil de destino** que de la escala; (4) un fin de semana sin faena exige cubrir 2–3 días calendario de despacho con stock o con entregas previas.

## 12. Logística conceptual

t/día operativo, 5 d/sem. Sin seleccionar vehículos.

| Flujo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves vivas cargadas en granja (t/día) | 7,3 | 14,5 | 29,1 | 58,2 |
| Aves vivas faenadas en planta (t/día) | 7,2 | 14,5 | 29,0 | 58,0 |
| Producto comestible que sale (t/día) | 6,0 | 12,0 | 24,0 | 47,9 |
| Subproductos sólidos que salen (t/día) | 1,5 | 3,0 | 6,1 | 12,2 |
| Masa que va a efluente o se pierde (t/día; no se transporta; **no** es el caudal de efluente) | 0,3 | 0,5 | 1,1 | 2,2 |
| Alimento que llega a granjas (t/día en semana plena, 7 días de entrega) | 8,8 | 17,7 | 35,3 | 70,6 |
| Camiones de aves vivas/día con 4.000 · 7.000 aves por camión (SUP-033) | 0,6 · 0,4 | 1,3 · 0,7 | 2,5 · 1,4 | 5,0 · 2,9 |
| Frecuencia relativa de movimientos (2.500 = 1) | 1 | 2 | 4 | 8 |

**Fórmulas para completar cuando existan datos (DPV-084):**

```
camiones vivos/día        = aves cargadas/día ÷ aves por camión          (SUP-033: 4.000–7.000, sin fuente)
camiones refrigerados/día = t de producto/día ÷ capacidad útil del camión refrigerado   (variable)
camiones de alimento/día  = t de alimento/día ÷ capacidad útil del camión de alimento   (variable)
retiros de subproductos   = t de sólidos/día ÷ capacidad útil del contenedor/camión     (variable)
```

**Lecturas:** (1) **localización respecto de las granjas: hipótesis a estudiar, no decisión.** La relación de masas (29 t vivas que entran contra 24 t comerciales que salen a 10.000 aves/día) **no es el argumento principal**. La ubicación relativa de planta y granjas se analizará después (`10_localizacion`, DEC-003) considerando tiempo de transporte de aves vivas, bienestar, mortalidad (DOA), merma de ayuno, bioseguridad, disponibilidad de productores, costo logístico, caminos, distancia a mercados, servicios, efluentes y exportación; (2) el alimento es el **mayor flujo físico** de todo el sistema y ocurre en granjas, no en la planta; (3) en distribución, el número de viajes lo fija el **número de paradas** (90 locales vs un centro de distribución) más que las toneladas (DPV-036).

## 13. Escala y exportación

**Días de faena para completar un contenedor de 25 t** (reefer 40', carga 24–27 t `[PVDP · débil]`, FTE-135) **si el 100 % de esa parte se destinara a exportación** / contenedores por mes equivalentes. **No es demanda**: exportación = 0 en todos los escenarios (SUP-022); mercado abierto ≠ venta (regla 17).

| Parte | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Pollo entero (config. A) | 5,0 d · 4,2/mes | 2,5 d · 8,3/mes | 1,3 d · 16,6/mes | 0,6 d · 33,2/mes |
| Pechuga con hueso | 12,2 d · 1,7 | 6,1 d · 3,4 | 3,1 d · 6,8 | 1,5 d · 13,6 |
| Pata-muslo | 15,2 d · 1,4 | 7,6 d · 2,7 | 3,8 d · 5,5 | 1,9 d · 11,0 |
| Carcasa-esqueleto | 24,4 d · 0,9 | 12,2 d · 1,7 | 6,1 d · 3,4 | 3,1 d · 6,8 |
| Alas | 46,2 d · 0,5 | 23,1 d · 0,9 | 11,5 d · 1,8 | 5,8 d · 3,6 |
| Menudencias | 91,7 d · 0,2 | 45,8 d · 0,5 | 22,9 d · 0,9 | 11,5 d · 1,8 |
| Garras grado A | 117,5 d · 0,2 | 58,8 d · 0,4 | 29,4 d · 0,7 | 14,7 d · 1,4 |
| Cuello | 134,0 d · 0,2 | 67,0 d · 0,3 | 33,5 d · 0,6 | 16,7 d · 1,2 |

Días en **días de faena** (5 d/sem); en días calendario, ×1,46.

| Factor exportador | Qué cambia de 2.500 a 20.000 aves/día |
|---|---|
| Consolidar volumen | Un contenedor de garras pasa de ~6 meses calendario a ~3 semanas; de pata-muslo, de 3 semanas a menos de 2 días de faena. A escala chica, solo el entero y los cortes principales llenan lotes con regularidad |
| Frecuencia de producción | Los importadores valoran embarques regulares (mensuales o más): a 2.500 aves/día, la mayoría de las partes no alcanza un contenedor por mes |
| Congelado y stock | Acumular un lote exige congelar y almacenar: 25 t de garras a 2.500 aves/día = ~6 meses de acumulación en cámara; a 20.000, ~3 semanas. Congelado = capacidad de túnel y cámara (DEC-012) |
| Contenedores | El reefer mantiene temperatura, no congela (`17_exportacion/logistica_exportacion.md`): la planta debe congelar antes de cargar |
| Continuidad de suministro | Una sola planta chica con pocos productores es más vulnerable a interrupciones (brote, clima, pollito) que un comprador externo tolera mal |
| Diversificación de productos | A mayor escala, más partes alcanzan lote mínimo y más destinos pueden atenderse a la vez (principio de ingreso total por ave) |
| Lo que la escala **no** cambia | Habilitación SENASA y listado por destino, acceso sanitario del país, certificaciones (Halal, UE), precio de mercado y riesgo de cierre por IAAP: son condiciones **previas**, independientes del tamaño (`17_exportacion`) |

Alternativa a escala chica: vender partes a **traders o exportadores que consoliden** (DPV-081), lo que no exige lote propio pero sí especificación y habilitación compatibles.

---

## 17. Qué debe ser verdad en cada escala — tabla central

Base del futuro simulador ([`especificacion_simulador_html.md`](especificacion_simulador_html.md)). **5 d/sem (250 d) · 6 d/sem (300 d)** cuando difieren; config. B, 2,9 kg, escenario medio; utilización 100 % = punto de dimensionamiento, **no** supuesto de operación.

| Variable | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves faenadas/año | 625.000 · 750.000 | 1.250.000 · 1.500.000 | 2.500.000 · 3.000.000 | 5.000.000 · 6.000.000 |
| kg vivo/día operativo | 7.250 | 14.500 | 29.000 | 58.000 |
| t vivas/año | 1.812 · 2.175 | 3.625 · 4.350 | 7.250 · 8.700 | 14.500 · 17.400 |
| Pollitos BB/semana plena | 13.197 · 15.837 | 26.395 · 31.674 | 52.790 · 63.348 | 105.580 · 126.696 |
| Plazas de granja | 120.507 · 144.609 | 241.014 · 289.217 | 482.029 · 578.435 | 964.058 · 1.156.870 |
| m² de galpones | 9.486 · 11.383 | 18.971 · 22.766 | 37.943 · 45.531 | 75.885 · 91.062 |
| Alimento t/año | 3.091 · 3.709 | 6.181 · 7.417 | 12.362 · 14.835 | 24.724 · 29.669 |
| Comestible: **masa biológica** t/día operativo | 5,78 | 11,55 | 23,11 | 46,22 |
| Comestible: **agua retenida** en producto t/día operativo (no es carne) | 0,21 | 0,43 | 0,86 | 1,71 |
| Comestible: **peso comercial** (= biológica + agua) t/día operativo | 5,99 | 11,98 | 23,96 | 47,93 |
| Peso comercial, promedio por **día calendario** (t) | 4,1 · 4,9 | 8,2 · 9,8 | 16,4 · 19,7 | 32,8 · 39,4 |
| Peso comercial por **año** (t) | 1.498 · 1.797 | 2.996 · 3.595 | 5.991 · 7.189 | 11.982 · 14.379 |
| — de él, producto principal (A), peso comercial t/día operativo | 3,7 | 7,4 | 14,7 | 29,5 |
| Plumas húmedas t/día | 0,6 | 1,2 | 2,4 | 4,8 |
| Sangre recuperada t/día | 0,2 | 0,4 | 0,8 | 1,7 |
| Vísceras no comestibles t/día | 0,3 | 0,7 | 1,3 | 2,6 |
| Ritmo de línea a 8 h netas (aves/h) | 312 | 625 | 1.250 | 2.500 |
| Inventario: 7 **días de producción** (t) | 42 | 84 | 168 | 336 |
| Inventario: 7 **días calendario** de cobertura (t) | 29 · 34 | 57 · 69 | 115 · 138 | 230 · 276 |
| **Demanda necesaria para 100 %** (kg de peso comercial/día calendario, M0) | 4.104 · 4.924 | 8.207 · 9.849 | 16.414 · 19.697 | 32.829 · 39.394 |
| Demanda necesaria para 70 % | 2.872 · 3.447 | 5.745 · 6.894 | 11.490 · 13.788 | 22.980 · 27.576 |
| **Equivalente por local** si toda la demanda viniera de los 90 locales (kg/local/día, 100 %) | 46 · 55 | 91 · 109 | 182 · 219 | 365 · 438 |
| Frente a los escenarios (M0, 5 d): factor demanda/capacidad del escenario base | 183 % (no alcanza) | 91 % | 46 % | 23 % |
| Complejidad operativa relativa | MENOR | MEDIA | MEDIA | MAYOR |

**Masa biológica vs peso comercial:** la cifra de "producto comercial" es **peso comercial** después del enfriamiento por inmersión = masa biológica comestible (carne, piel, hueso de los cortes, menudencias, garras) + agua retenida en producto (~3,6 %; SUP-042), trazable al balance v1.1 (clases A + B). **El agua retenida nunca es carne producida** (test T20: la masa biológica es idéntica con 6 % u 8 % de absorción). La demanda se expresa en peso comercial (kg vendidos), por eso se compara con el peso comercial.

**Cómo leer la "demanda necesaria":** es la **cota inferior** (ave completa vendida), en kg de peso comercial por día calendario (producción por día operativo × días operativos / 365). Con mixes de supermercado, la demanda útil para llenar la planta es menor y aparecen partes excedentes (§4). El rango de la red por local es 25–300 kg/local/día ([`../02_clientes_demanda/supermercados.md`](../02_clientes_demanda/supermercados.md) §1): **20.000 aves/día exigirían más pollo por local que el extremo superior de ese rango**, aun vendiendo el ave completa por la red.

**Complejidad operativa relativa** (MENOR/MEDIA/MAYOR solo como orden físico): crece con el número de aves, lotes, productores, movimientos diarios y flujos de subproductos, todos ×8 entre 2.500 y 20.000. 5.000 y 10.000 comparten MEDIA porque el cambio de naturaleza (red de productores, flujo industrial de subproductos, frío con stock) aparece entre ambas sin un umbral físico claro.

**Qué debe ser verdad, en una línea por escala:**

| Escala | Debe ser verdad que… |
|---|---|
| 2.500 | …existen ≥ ~3–4 t/día calendario de demanda **A/B** propia y un receptor diario de ~1,5 t de subproductos; que una planta de este tamaño puede habilitarse y operar con costo unitario aceptable (escala mínima eficiente **desconocida**, DPV-083); y que hay 1–4 productores o granja propia para ~120.000 plazas |
| 5.000 | …la red o varios canales compran de verdad ~6–8 t/día (≈ escenario base con ave completa), con salida para pata-muslo, alas y carcasa; que hay ~26.000 pollitos BB/semana asegurados y ~19.000 m² de galpón disponibles |
| 10.000 | …existe demanda A/B de ~11–16 t/día calendario, **más del doble del escenario base**, repartida en canales que absorban todas las partes; ~53.000 pollitos/semana; ~38.000 m² de galpón (4–16 productores); un receptor o proceso para ~5–6 t/día de subproductos |
| 20.000 | …se concreta algo cercano al **escenario expansivo** (los 90 locales a más de 150 kg/día + mayoristas, industria y exportación **ya negociada**); ~106.000 pollitos/semana; ~76.000 m² de galpón en una red de productores; salida diaria para ~11–17 t de subproductos y ~8 t de carcasa; frío para cientos de toneladas |

## 19. Análisis de sensibilidad

Todas las variables son modificables en la línea de comandos (`--escenario`, §20). Ejemplo a **10.000 aves/día** (5 d, B, 100 % salvo indicación):

| Caso | Aves/año | t vivas/año | Pollitos/semana plena | m² galpón | Alimento t/año | Comestible (peso comercial) t/día operativo | Producto principal t/día operativo | Rendering potencial t/día | Días para 25 t de pata-muslo |
|---|---|---|---|---|---|---|---|---|---|
| Base (2,9 kg; FCR 1,70; mort. 5 %) | 2.500.000 | 7.250 | 52.790 | 37.943 | 12.362 | 24,0 | 14,7 | 5,33 | 3,8 |
| FCR 1,60 | = | = | = | = | 11.635 | = | = | = | = |
| FCR 1,85 | = | = | = | = | 13.453 | = | = | = | = |
| Mortalidad 3 % | = | = | 51.701 | = | = | = | = | = | = |
| Mortalidad 8 % | = | = | 54.511 | = | = | = | = | = | = |
| Liviano 2,4 kg / 38 d / FCR 1,58 | = | 6.000 | 52.790 | 26.843 | 9.509 | 19,7 | 12,0 | 4,55 | 4,6 |
| Pesado 3,4 kg / 54 d / FCR 1,82 | = | 8.500 | 52.790 | 49.507 | 15.517 | 28,3 | 17,6 | 6,06 | 3,2 |
| 6 d/sem (300 d) | 3.000.000 | 8.700 | 63.348 | 45.531 | 14.835 | 24,0 | 14,7 | 5,33 | 3,8 |
| 5 d/sem con 240 d/año | 2.400.000 | 6.960 | 52.790 | 37.943 | 11.868 | 24,0 | 14,7 | 5,33 | 3,8 |
| Config. A (entero) | = | = | = | = | = | 24,1 | 20,8 | 5,33 | 63,3* |
| Config. C (deshuesado) | = | = | = | = | = | 20,5 | 11,5 | 8,64 | 3,8** |
| Utilización 70 % | 1.750.000 | 5.075 | 36.953 | 26.560 | 8.653 | 16,8 | 10,3 | 3,73 | 5,4 |

\* En A solo se troza el 6 % de canales no aptas para entero. \*\* Pata-muslo de un ave trozada (B) para la comparación de exportación.

**Lecturas:** (1) el **peso de faena** es la variable que más mueve el sistema a igual número de aves (−17 % / +17 % de toneladas vivas y −29 % / +30 % de m² entre 2,4 y 3,4 kg); (2) el **FCR** mueve solo el alimento (+0,15 → +8,8 %); (3) la **mortalidad** mueve pollitos (+3,3 % de 5 a 8 %), no m² ni productos; (4) la **configuración** no cambia las aves ni las granjas: cambia qué sale de la planta; (5) para la **demanda**, a menor peso más aves: con el escenario base, 5.561 aves/día operativo a 2,4 kg vs 3.870 a 3,4 kg (M0).

## 20. Modelo reproducible y documentación del CSV (regla 15)

```
python3 23_plan_expansion/modelo_escala.py                 # tests + CSV
python3 23_plan_expansion/modelo_escala.py --solo-tests    # 23 pruebas (incluye las de los modelos importados)
python3 23_plan_expansion/modelo_escala.py --tablas        # tablas de este documento
python3 23_plan_expansion/modelo_escala.py --mutaciones    # 22 mutaciones que los tests deben detectar
python3 23_plan_expansion/modelo_escala.py --escenario --aves-dia 7500 --dias-semana 6 --dias-anio 290 \
    --horas-netas 8 --peso 3.1 --edad 50 --mortalidad 0.07 --fcr 1.78 --config C --utilizacion 0.6 \
    --dias-inventario 5 --demanda ESC-BAS                  # sensibilidad (no escribe CSV; emite alertas)
```

**Qué se importa y de dónde** (trazabilidad; nada copiado a mano):

| Dato | Origen |
|---|---|
| Escalas, calendarios 250/300, semanas/año, perfiles, desempeños, pollitos, plazas, m², galpones, alimento, agua, aves simultáneas | `03_produccion_primaria/modelo_escenarios_produccion.py` (`calcular`, `PERFILES`, `DESEMPENO`, `DIAS_FAENA_ANIO`) |
| kg por ave de cada salida, clases A/B/C/D/P, rutas, rendimiento de CMS, cierre | `04_balance_masa/modelo_balance_masa.py` (`balance`, `verificar_cierre`, `DESTINO`, `CMS_RENDIMIENTO`) |
| Variantes V1/V3/V6, escenario de referencia, agrupación sin doble conteo, carga de contenedor 25 t | `07_subproductos/modelo_subproductos.py` (`VARIANTES`, `agrupar`, `REND/COND/ENF`, `CARGA_CONTENEDOR_T`) |
| Escenarios comerciales, categoría, exportación, cantidad de locales | `02_clientes_demanda/escenarios_demanda.csv` |
| Mixes M1–M3 y 0,75 kg de pechuga por kg de milanesa | `02_clientes_demanda/supermercados.md` §2.2–§2.3 (leídos del texto) |
| Parámetros nuevos | Horas netas (SUP-053), perfiles de destino (SUP-055), aves por camión (SUP-033), utilizaciones y días de inventario (escenarios) |

**Columnas de `escenarios_escala.csv`** (formato largo, separador decimal punto, UTF-8):

| Columna | Contenido |
|---|---|
| `bloque` | `capacidad`, `ritmo_linea`, `produccion_primaria`, `abastecimiento`, `utilizacion`, `balance_productos`, `masa_comestible` (biológica / agua retenida / comercial por día operativo, día calendario y año), `configuraciones`, `subproductos`, `inventario`, `logistica`, `exportacion`, `demanda_capacidad`, `tabla_central` |
| `escala_aves_dia` | Escala E (aves faenadas/día operativo a utilización 100 %) |
| `dias_semana`, `dias_anio` | Calendario (5/250 o 6/300); nunca mezclados |
| `parametro` | Parámetros de la fila (`utilizacion=`, `horas_netas=`, `base_temporal=` (`dias_produccion` o `dias_calendario`) y `dias=`, `perfil_destino=`, `config=`, `peso=`, `escenario=`, `metodo=`, `aves_por_camion=`) |
| `variable` en `demanda_capacidad` | `factor_demanda_capacidad` (puede superar 100 %), `utilizacion_planta` y `cobertura_demanda` (siempre 0–100 %), `kg_atendidos_dia_cal`, `kg_no_atendidos_dia_cal`, `aves_procesadas_dia_operativo`, `aves_faltantes_dia_operativo`, `capacidad_ociosa_aves_dia_operativo`, `kg_sin_destino_plena_escala`, `demanda_adicional_para_llenar_kg_dia_cal`, `excedente_partes_kg_dia_cal` |
| `variable`, `valor`, `unidad` | Variable física, valor y unidad (aves, aves/h, pollitos, plazas, t, kg, m², m³, galpones, %, ratio, días, contenedores/mes, camiones, productores, índice). Sin unidades monetarias (test T11). Valor vacío = variable pendiente (p. ej. `productores_necesarios`, DPV-048) |
| `periodo` | `dia_operativo`, `dia_calendario`, `semana_plena`, `semana_promedio`, `anio`, `hora`, `stock`, `adimensional` |
| `base` | `vivo`, `comercial` (biológica + agua retenida), `biologica`, `biologica+agua`, `aves`, `alimento`, `agua`, `superficie`, `conteo` |
| `fuente_modelo` | Modelo del que proviene el número |
| `clasificacion` | Etiqueta de la regla 4 |
| `sumable` | `si` (partición que cierra), `no` (alternativa excluyente, agregado o entrada), `-` |
| `nota` | Advertencias |

**Tests (23) y mutaciones (22):** resultados en [`conclusiones_escala.md`](conclusiones_escala.md) §6.

**Limitaciones del modelo:** (1) todo es lineal en aves: no hay economías de escala físicas (rendimientos iguales en cualquier tamaño) ni estacionalidad; (2) peso en granja = peso en planta (la merma de ayuno queda fuera, SUP-058); (3) los días de 6 d/sem solo admiten 5 o 6 días/semana porque así lo define el modelo de producción; (4) los mixes de demanda son hipotéticos; (5) no incluye agua de proceso, efluentes, energía ni personal; (6) ningún dato es de campo argentino.
