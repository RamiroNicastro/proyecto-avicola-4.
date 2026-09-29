# Red de ~90 supermercados — escenarios de volumen, mix y logística comercial

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 · Marco general: [`modelo_demanda.md`](modelo_demanda.md) · Datos: [`escenarios_demanda.csv`](escenarios_demanda.csv) (bloque `red_supermercados`)

> **La red NO es un cliente confirmado** (regla 8, SUP-004). Todo lo que sigue son **escenarios hipotéticos para entender órdenes de magnitud**. Hoy la red es demanda de **categoría C condicionada** ([`modelo_demanda.md` §5](modelo_demanda.md)).

---

## 0. Qué se sabe y qué no

| Tema | Estado | Registro |
|---|---|---|
| Acceso potencial a ~90 supermercados vinculados al potencial inversor | Declarado por el promotor; no verificado | SUP-004, DPV-002 |
| Ubicación principalmente en AMBA | "Aparentemente"; sin lista de locales | DPV-018 |
| Cantidad exacta de locales, formato (hiper, super, autoservicio), superficie | Desconocido | DPV-002, DPV-018 |
| Una cadena o varias sociedades; centros de distribución | Desconocido | DPV-018, DPV-036 |
| Volumen de pollo, productos, proveedores, precios, plazos | Desconocido | DPV-003, DPV-020, DPV-037, DPV-039 |
| Relación del inversor con la red y quién decide las compras | Desconocido | DPV-038 |
| Voluntad real de compra | Desconocida | DPV-002 |

---

## 1. Escenarios por kg/local/día (90 locales)

### 1.1 Tabla principal

Supuesto de cada fila: **los 90 locales compran todo su pollo al proyecto** (adhesión 100 % y proveedor único). Es un **techo hipotético** del canal, no una expectativa.

| kg/local/día | kg/día (90 locales) | t/día | t/mes | t/año | Aves/día a 1,8 kg | Aves/día a 2,1 kg | Aves/día a 2,4 kg | % consumo nacional | % consumo AMBA estimado |
|---|---|---|---|---|---|---|---|---|---|
| 25 | 2.250 | 2,25 | 68,4 | 821 | 1.250 | 1.071 | 938 | 0,04 % | 0,13 % |
| 50 | 4.500 | 4,50 | 136,9 | 1.642 | 2.500 | 2.143 | 1.875 | 0,08 % | 0,26 % |
| 75 | 6.750 | 6,75 | 205,3 | 2.464 | 3.750 | 3.214 | 2.812 | 0,12 % | 0,39 % |
| 100 | 9.000 | 9,00 | 273,8 | 3.285 | 5.000 | 4.286 | 3.750 | 0,16 % | 0,52 % |
| 150 | 13.500 | 13,50 | 410,6 | 4.928 | 7.500 | 6.429 | 5.625 | 0,23 % | 0,78 % |
| 200 | 18.000 | 18,00 | 547,5 | 6.570 | 10.000 | 8.571 | 7.500 | 0,31 % | 1,04 % |
| 300 | 27.000 | 27,00 | 821,2 | 9.855 | 15.000 | 12.857 | 11.250 | 0,47 % | 1,56 % |

Bases: kg de producto por **día calendario**; 30,42 días/mes; 365 días/año. Aves/día = kg/día ÷ peso comercial equivalente canal por ave (1,8 / 2,1 / 2,4 kg; SUP-019, [`modelo_demanda.md` §2.2](modelo_demanda.md)). Las aves suponen un mix que consume el ave completa (§2). Porcentajes de consumo: [`modelo_demanda.md` §3](modelo_demanda.md). Clasificación: `[SUPUESTO]` (kg/local) y `[ESTIMACIÓN]` (derivados).

### 1.2 Lo mismo visto desde un local

| kg/local/día | kg/local/semana | Pollos/local/día (1,8 / 2,1 / 2,4 kg) |
|---|---|---|
| 25 | 175 | 13,9 / 11,9 / 10,4 |
| 50 | 350 | 27,8 / 23,8 / 20,8 |
| 75 | 525 | 41,7 / 35,7 / 31,3 |
| 100 | 700 | 55,6 / 47,6 / 41,7 |
| 150 | 1.050 | 83,3 / 71,4 / 62,5 |
| 200 | 1.400 | 111,1 / 95,2 / 83,3 |
| 300 | 2.100 | 166,7 / 142,9 / 125,0 |

**Uso:** es la forma de chequear cada escenario con el comprador ("¿venden unos 50 pollos equivalentes por día en un local típico?"). **No hay dato público de ventas de pollo por local de supermercado en Argentina**; el volumen depende del formato (un hipermercado y un autoservicio de barrio pueden diferir en un orden de magnitud). No se afirma que ningún valor de la tabla sea típico.

### 1.3 Sensibilidad a la adhesión (kg/día)

La adhesión real puede ser parcial: algunos locales pueden no comprar, comprar solo ciertos cortes o mantener a su proveedor actual.

| Locales que compran | 25 kg | 50 kg | 75 kg | 100 kg | 150 kg | 200 kg | 300 kg |
|---|---|---|---|---|---|---|---|
| 10 | 250 | 500 | 750 | 1.000 | 1.500 | 2.000 | 3.000 |
| 20 | 500 | 1.000 | 1.500 | 2.000 | 3.000 | 4.000 | 6.000 |
| 30 | 750 | 1.500 | 2.250 | 3.000 | 4.500 | 6.000 | 9.000 |
| 45 | 1.125 | 2.250 | 3.375 | 4.500 | 6.750 | 9.000 | 13.500 |
| 60 | 1.500 | 3.000 | 4.500 | 6.000 | 9.000 | 12.000 | 18.000 |
| 90 | 2.250 | 4.500 | 6.750 | 9.000 | 13.500 | 18.000 | 27.000 |

**Lectura:** la combinación de adhesión y kg/local cubre **dos órdenes de magnitud** (de 250 a 27.000 kg/día). Sin datos de la red, cualquier valor de este rango es igualmente defendible, y por eso ninguno lo es.

---

## 2. Mix de productos de supermercado

### 2.1 Por qué el mix importa tanto como los kg

1. **El ave es un conjunto fijo de partes** (`17_exportacion/estrategia_valorizacion_ave.md` §2). Si la red pide mucha pechuga y milanesas, hay que faenar más aves para obtenerla, y la pata-muslo, las alas y la carcasa sobrantes necesitan otros compradores.
2. **Define los procesos de planta:** entero (faena y enfriado) vs trozado vs deshuese vs elaborados (rebozado, formado, cocción) son equipos, personal, habilitaciones y frío distintos.
3. **Define el ingreso y el margen:** cada producto tiene precio, costo de proceso, vida útil y merma distintos. El pollo entero suele usarse como producto gancho con margen mínimo (FTE-052 `[PVDP · débil]`).
4. **Define el packaging y la logística:** granel en cajón, bandeja con film, bandeja con atmósfera modificada, congelado IQF; cada uno cambia vida útil, frecuencia de entrega y devoluciones.
5. **Define la competencia:** en pechuga y elaborados compite la importación de Brasil (`01_mercado` §1.6); en entero, los integradores nacionales.

### 2.2 Mixes hipotéticos (no son datos)

`[SUPUESTO]` (SUP-023). Porcentajes del kg vendido por la red. **No representan el mix real de ningún supermercado**; son tres formas contrastantes para ver el efecto del mix. El único dato disponible sobre el mix nacional es periodístico y no validado ("~70 % se troza", DPV-017).

| Producto | M1 — Entero dominante | M2 — Trozado | M3 — Valor agregado |
|---|---|---|---|
| Pollo entero | 55 % | 30 % | 20 % |
| Pechuga / suprema / filet | 12 % | 22 % | 25 % |
| Pata-muslo | 15 % | 22 % | 15 % |
| Alas | 3 % | 5 % | 5 % |
| Milanesas (de pechuga) | 8 % | 12 % | 20 % |
| Menudencias | 2 % | 3 % | 2 % |
| Otros elaborados (hamburguesas, nuggets, marinados) | 5 % | 6 % | 13 % |
| **Total** | 100 % | 100 % | 100 % |

**Aplicado a 9.000 kg/día** (90 locales × 100 kg; kg de producto por día):

| Producto | M1 | M2 | M3 |
|---|---|---|---|
| Pollo entero | 4.950 | 2.700 | 1.800 |
| Pechuga / suprema | 1.080 | 1.980 | 2.250 |
| Pata-muslo | 1.350 | 1.980 | 1.350 |
| Alas | 270 | 450 | 450 |
| Milanesas | 720 | 1.080 | 1.800 |
| Menudencias | 180 | 270 | 180 |
| Otros elaborados | 450 | 540 | 1.170 |

### 2.3 Ejemplo ilustrativo del balance de partes

**Rendimientos ilustrativos** `[SUPUESTO]` (SUP-023), a reemplazar por los de `04_balance_masa` (DPV-008): de una canal de 2,1 kg se obtienen 30 % de pechuga deshuesada (coherente con el extracto de Cobb: filet ≈ 22,6 % del peso vivo ≈ 30 % de la canal, FTE-140 `[PVDP]`), 30 % de pata-muslo, 10 % de alas y 30 % de carcasa, cogote, piel y recortes; 1 kg de milanesa requiere 0,75 kg de pechuga; 0,12 kg de menudencias por ave. Los "otros elaborados" se suponen hechos con recortes y no entran en el balance.

| Concepto (9.000 kg/día) | M1 | M2 | M3 |
|---|---|---|---|
| Aves para el pollo entero | 2.357 | 1.286 | 857 |
| Aves para trozar (fijadas por la parte limitante) | 2.571 | 4.429 | 5.714 |
| Parte limitante | Pechuga (incluye milanesas) | Pechuga (incluye milanesas) | Pechuga (incluye milanesas) |
| **Aves totales/día** | **4.929** | **5.714** | **6.571** |
| Aves según la fórmula simple (9.000 ÷ 2,1) | 4.286 | 4.286 | 4.286 |
| **Factor de mix (f_mix)** | **1,15** | **1,33** | **1,53** |
| Excedente de pata-muslo (kg/día) | 270 | 810 | 2.250 |
| Excedente de alas (kg/día) | 270 | 480 | 750 |
| Carcasa, cogote, piel y recortes (kg/día) | 1.620 | 2.790 | 3.600 |
| Excedente de menudencias (kg/día) | 411 | 416 | 609 |
| **Excedentes a colocar en otros canales (kg/día)** | **~2.570** | **~4.500** | **~7.210** |

**Conclusiones del ejemplo** (válidas en su dirección, no en sus cifras):

- Con los mismos 9.000 kg/día, un mix orientado a pechuga y milanesas puede exigir **hasta ~50 % más aves** y generar **tantos kg de excedente como un 80 % de lo que compra la red**.
- Esos excedentes necesitan canales propios (mayoristas, pollerías, industria de elaborados y CMS, exportación de pata-muslo, rendering para la carcasa): la red de supermercados **no puede ser el único canal** aunque compre mucho.
- Si el mix de la red se parece a M1 (mucho entero), el volumen es más fácil de balancear pero el margen probablemente sea menor (producto gancho). Si se parece a M3, el valor por kg puede ser mayor pero el negocio depende de colocar los excedentes: **el ingreso total por ave** es lo que decide (SUP-013).

---

## 3. Logística comercial: entregar a 90 locales, a centros de distribución o a un distribuidor

**Conocer la red logística de los supermercados es prioritario** (DPV-036, DEC-016): puede cambiar el costo por kg más que cualquier otra variable comercial, además del tipo de flota, del capital de trabajo y de la habilitación.

### 3.1 Aritmética de las entregas directas

Paradas por semana con entrega directa a los 90 locales: **270** con 3 entregas semanales por local y **540** con 6.

| kg/local/día | kg por entrega con 3 entregas/semana | kg por entrega con 6 entregas/semana |
|---|---|---|
| 25 | 58 | 29 |
| 50 | 117 | 58 |
| 100 | 233 | 117 |
| 150 | 350 | 175 |
| 300 | 700 | 350 |

`[ESTIMACIÓN]`: kg/local/día × 7 ÷ entregas por semana. Si cada parada tiene un costo aproximadamente fijo (tiempo de chofer, espera en recepción, tránsito urbano), **el costo logístico por kg es inversamente proporcional a los kg por parada**: con 58 kg por parada cuesta, por kg, ~4 veces más que con 233 kg y ~12 veces más que con 700 kg. Con producto fresco de vida útil corta, la frecuencia no puede bajarse mucho.

### 3.2 Comparación cualitativa

| Dimensión | **A. Entrega directa a 90 locales** | **B. Entrega a uno o varios centros de distribución (CD)** | **C. Venta a un mayorista / distribuidor** |
|---|---|---|---|
| Camiones | Varios camiones de reparto urbano refrigerados, muchas rutas diarias | Pocos camiones de mayor porte; viajes consolidados | Mínimo propio (retiro en planta o entrega a un punto) |
| Combustible | Alto por kg (kilómetros urbanos, paradas) | Bajo por kg | Muy bajo o nulo |
| Choferes y auxiliares | Muchos (rutas + descarga en cada local) | Pocos | Mínimo |
| Tiempos | Ventanas horarias de recepción por local, esperas, tránsito del AMBA | Una ventana en el CD; el CD redistribuye | Según acuerdo |
| Cadena de frío | Muchas aperturas de puerta; mayor riesgo de corte de frío | Menos aperturas; depende de la cadena de frío del CD | Transferida al distribuidor (riesgo reputacional si hay marca propia) |
| Inventario | Stock en planta y en camiones; reposición fina por local | Stock consolidado; el CD puede exigir vida útil remanente mínima | Stock mínimo propio; el distribuidor absorbe |
| Devoluciones | Muchas y dispersas (producto próximo a vencer, faltantes de calidad); logística inversa costosa | Concentradas; reglas del CD | Menores o negociadas en el precio |
| Costo por kg | **El más alto**; muy sensible a los kg por parada (§3.1) | Intermedio; el supermercado puede cobrar un **fee de CD** (a validar, DPV-039) | Bajo para el proyecto, pero el distribuidor retiene un margen |
| Control comercial | Máximo (reposición, exhibición, datos por local) | Medio (datos del CD; menos visibilidad de góndola) | Bajo (el cliente final es del distribuidor) |
| Capital de trabajo | Flota propia o flete; plazos del supermercado | Plazos del supermercado | Plazos del distribuidor (a validar) |

**Implicancias:**

- Si la red tiene CD con recepción de perecederos, el costo logístico del canal cae y la red se parece más a un "gran cliente único" (mejor logística, **mayor concentración**).
- Si no tiene CD, la entrega directa a 90 locales exige una operación de distribución urbana que puede ser **un negocio en sí mismo**; la opción de un distribuidor tercerizado debe compararse (DEC-016, DPV-042).
- Los datos se completan en `13_logistica` en la fase correspondiente.

---

## 4. Riesgos específicos del canal

| Riesgo | Por qué | Referencia |
|---|---|---|
| Voluntad de compra no demostrada | No hay reunión con compras ni carta de intención | DPV-002 |
| Concentración | La red pesaría 57–67 % de las ventas en los tres escenarios | [`estrategia_comercial.md` §1](estrategia_comercial.md) |
| Partes vinculadas | Si el inversor controla la red, precio y plazo pueden no ser de mercado; si el inversor se retira, se va el cliente | DPV-038 |
| Poder de negociación y producto gancho | El supermercado fija promociones sobre el pollo entero | FTE-052 `[PVDP · débil]` |
| Plazos de pago | Producto perecedero, pagado a plazo: capital de trabajo | DPV-039 |
| Costos comerciales ocultos | Bonificaciones, fees de alta y de CD, aportes promocionales, devoluciones, penalidades | [`estrategia_comercial.md` §2](estrategia_comercial.md) |
| Proveedor actual con contrato o exclusividad | Retrasa o impide la entrada | DPV-020 |
| Requisitos de alta de proveedor | Habilitación (probablemente tránsito federal si la planta está fuera de la provincia de los locales), auditorías, codificación, trazabilidad | DPV-041, DEC-009 |

## 5. Cómo validar

Cuestionario en [`cuestionario_supermercados.md`](cuestionario_supermercados.md). Tareas en [`conclusiones_demanda.md` §6](conclusiones_demanda.md).
