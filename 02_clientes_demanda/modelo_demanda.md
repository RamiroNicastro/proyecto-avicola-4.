# Modelo de demanda comercial — marco, categorías y escenarios

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 (marco sin datos de campo) · **Fase:** 0 (prefactibilidad) · **Carpeta:** `02_clientes_demanda`

Documentos del modelo:

| Documento | Contenido |
|---|---|
| Este archivo | Definiciones, categorías de demanda (A/B/C/D), conversiones kg → aves, exportación como demanda (niveles 0–6), escenarios comerciales, regla de dimensionamiento y documentación del CSV |
| [`escenarios_demanda.csv`](escenarios_demanda.csv) | Datos numéricos de los escenarios (archivo maestro de las cifras) |
| [`supermercados.md`](supermercados.md) | Red de ~90 supermercados: escenarios por kg/local/día, mix de productos y logística comercial |
| [`cuestionario_supermercados.md`](cuestionario_supermercados.md) | Cuestionario para el contacto de la red y el potencial inversor |
| [`canales_comerciales.md`](canales_comerciales.md) | Otros canales locales (mayoristas, tradicional, gastronomía, industria) |
| [`estrategia_comercial.md`](estrategia_comercial.md) | Concentración de clientes, precio y margen, marca propia vs blanca, indicadores comerciales |
| [`conclusiones_demanda.md`](conclusiones_demanda.md) | Conclusiones, riesgos, tareas de campo y datos faltantes |

> **Restricciones de fase:** este modelo **no dimensiona la planta**, no fija capacidad de faena (regla 9) y no recomienda inversión. Todos los volúmenes son **escenarios de prueba de orden de magnitud**, no pronósticos ni ventas (SUP-021).
> **Situación de la evidencia (2026-09-29):** no hay ningún dato de campo de la red de supermercados ni de otros clientes. **La demanda documentada hoy es prácticamente nula** (§5).

---

## 1. Cuatro conceptos que no deben mezclarse

| Concepto (pedido de la sesión) | Categoría del modelo | Definición | Evidencia mínima para ubicar un volumen aquí | Uso en decisiones de capacidad |
|---|---|---|---|---|
| **Demanda asegurada** | **A. Demanda base** | Volumen con alta probabilidad de compra: contrato, orden de compra, carta de intención con volumen y precio, o historial de compras propio | Documento firmado o registro de ventas propio (kg/semana por producto, con precio y plazo) | **Única base firme** para la capacidad inicial y para comprometer capital |
| **Demanda probable** | **B. Demanda en desarrollo** | Clientes con interés concreto que están negociando: volumen, producto, precio o prueba piloto en discusión | Minuta de reunión con el decisor de compras, especificación de producto, cotización pedida, prueba piloto acordada | Entra **parcialmente** (factor α < 1, a calibrar) en la capacidad inicial; justifica flexibilidad de expansión |
| **Demanda potencial** | **C. Demanda potencial accesible** | Clientes identificados (nombre, ubicación, volumen estimado) con acceso razonable, pero sin negociación | Lista de clientes con contacto y volumen estimado de fuente identificable | **No** entra en la capacidad inicial. Justifica reservas de espacio, servicios y terreno para etapas futuras |
| **Mercado total** | **D. Mercado potencial** | Consumo del mercado (nacional, AMBA, canal, país importador) | Estadística de mercado | **Nunca** se usa para dimensionar. Solo verifica que el mercado no sea un techo |

**Regla de pasaje entre categorías:** un volumen sube de categoría solo con **evidencia documental nueva** (registro en `25_fuentes/registro_fuentes.csv` con tipo `entrevista` o `cotizacion`). Nunca por entusiasmo del interlocutor, por cercanía personal o por el tamaño del mercado.

**Regla de no suma:** los totales de "demanda" en decisiones se informan **separados por categoría** (A, B, C, D). Un total A+B+C+D no tiene significado.

---

## 2. Unidades y conversiones

### 2.1 Bases de cálculo (regla 14)

| Magnitud | Definición | Dónde se usa |
|---|---|---|
| **kg de producto** | kg vendidos al cliente (entero, cortes, elaborados, menudencias). Es la unidad de la demanda | Todos los escenarios de este modelo |
| **kg equivalente canal** | kg de canal eviscerada necesarios para producir los kg de producto. Si el mix tiene deshuesados o elaborados, **1 kg de producto ≠ 1 kg de canal** (§2.4) | Conversión a aves |
| **Aves (pollos) por día** | Aves faenadas necesarias para abastecer la demanda. **No** son pollos vivos alojados en granja (hay mortalidad y descartes previos) | Orden de magnitud para balance de masa |
| **kg vivo** | Peso del ave viva en la granja | Solo como base del rango de peso (§2.2) |
| **Día** | **Día calendario** (365 días/año; 30,42 días/mes = 365/12). No es día de faena (SUP-020) | Todos los escenarios |

### 2.2 Peso comercial por ave: rango, no valor único (SUP-019)

| Parámetro | Valor | Fuente / clasificación |
|---|---|---|
| Peso vivo de faena de referencia en Argentina | ~3 kg (crianza de 46–50 días) | FTE-050 `[PVDP · débil]` |
| Rango de peso vivo adoptado | 2,6 – 3,2 kg | `[SUPUESTO]` alrededor de la referencia |
| Rendimiento de canal eviscerada de referencia (Cobb 500, 2,8 kg vivo) | ~74 % del peso vivo | FTE-140 `[PVDP]` (extracto; documento original no leído) |
| Rango de rendimiento adoptado | 70 – 76 % | `[SUPUESTO]` (depende de genética, sexo, especificación de canal con o sin menudencias y cogote) |
| **Peso comercial equivalente canal por ave** | **1,8 / 2,1 / 2,4 kg** (bajo / central / alto) | `[ESTIMACIÓN]`: 2,6 × 0,70 ≈ 1,82 y 3,2 × 0,76 ≈ 2,43 |

- A **menor peso por ave, más aves** para los mismos kg: pasar de 2,4 a 1,8 kg aumenta las aves necesarias un **33 %**.
- El valor definitivo sale de `04_balance_masa` con manuales de líneas genéticas y datos de faena (DPV-008).
- **No dividir la producción nacional (t) por la faena SENASA** para obtener un peso por ave: son universos distintos (regla 18; `01_mercado/mercado_avicola_argentina.md` §0.3).

### 2.3 Fórmulas del modelo

```
kg/día (canal c)           = locales_c × kg/local/día            (supermercados)
                           = valor de prueba                      (otros canales)
Mercado interno kg/día     = supermercados + mayoristas/distribuidores + carnicerías/pollerías + gastronomía + industria
Total kg/día               = mercado interno + exportación        (exportación = 0 en los escenarios: SUP-022)
t/día                      = kg/día / 1.000
t/mes                      = kg/día × 30,42 / 1.000
t/año                      = kg/día × 365 / 1.000
Aves/día (peso p)          = kg/día / p        con p ∈ {1,8; 2,1; 2,4} kg equivalente canal por ave
% consumo nacional         = kg/día / 5.753.425 kg/día
% consumo AMBA estimado    = kg/día / 1.726.027 kg/día
```

Conversión a **días de faena** (para la fase de balance de masa, no para esta): aves/día de faena = aves/día calendario × 365 / días de faena por año. Con 250 días de faena el factor es 1,46; con 300 días, 1,22. Los días de faena no se definen aquí.

### 2.4 Por qué los kg no alcanzan: el efecto del mix

La fórmula "aves = kg / peso por ave" supone que el cliente compra **todas las partes del ave en la proporción en que el ave las produce**. Si el mix pide más de una parte (típicamente pechuga, filet o milanesas) que la proporción natural, las aves necesarias las fija **la parte limitante**, y el resto de las partes queda como **excedente que debe venderse en otros canales**. En el ejemplo ilustrativo de [`supermercados.md` §2](supermercados.md), el mismo volumen de 9.000 kg/día requiere entre **1,15× y 1,53×** las aves calculadas con la fórmula simple, y genera entre **~2,6 y ~7,2 t/día de partes excedentes** (según el mix hipotético). Por eso **conocer el mix es tan importante como conocer los kg totales**.

---

## 3. Mercado total de referencia (categoría D)

| Referencia | Valor | Base | Clasificación |
|---|---|---|---|
| Consumo aparente nacional de carne aviar | ~2,1 Mt/año (2022–2024) | `01_mercado/mercado_avicola_argentina.md` §1.4 | `[PVDP]` |
| Equivalente diario nacional | ~5.750 t/día calendario | 2,1 Mt / 365 | `[ESTIMACIÓN]` |
| Población CABA + 24 partidos / total del país (Censo 2022) | ~13,9 M / ~45,9 M ≈ 30 % | FTE-141 | `[PVDP]` (hay dos totales nacionales publicados: 45,89 M y 46,23 M; ver FTE-141) |
| Consumo AMBA estimado | ~1.730 t/día | 30 % del consumo nacional, suponiendo consumo per cápita uniforme (SUP-024) | `[ESTIMACIÓN]` (el consumo per cápita del AMBA no está verificado) |

**Lectura:** aun el escenario más alto de la red (90 locales × 300 kg/día = 27 t/día) equivaldría a ~0,5 % del consumo nacional y ~1,6 % del consumo estimado del AMBA. **El tamaño del mercado no limita la escala del proyecto; lo que la limita es el acceso comercial demostrable** (clientes que efectivamente compren a un precio que cubra costos). El proyecto, además, **desplaza** a proveedores existentes: el mercado está maduro (`01_mercado/conclusiones_mercado.md` §8).

---

## 4. La exportación como demanda: niveles 0 a 6

El tamaño del comercio mundial (~14,8 Mt en 2026, `17_exportacion`) **no es demanda del proyecto**. La demanda exportadora se clasifica por niveles acumulativos, **por producto y por destino**:

| Nivel | Definición | Situación al 2026-09-29 (desde `17_exportacion`) | Categoría de demanda | ¿Sirve para dimensionar? |
|---|---|---|---|---|
| **0** | Mercado internacional existente | Comercio mundial ~14,8 Mt; importadores relevantes: Japón, México, UE, Golfo, Vietnam, etc. | D | No |
| **1** | País legalmente accesible para Argentina (acceso sanitario a nivel país) | Comunicado de apertura posterior a feb-2026: UE, Japón, Corea del Sur, Chile, Perú. Probables por regionalización: Vietnam, Arabia Saudita, EAU, Singapur, Brasil. China: **no disponible confirmado** (DPV-035) | D | No |
| **2** | Producto argentino efectivamente exportado a ese destino | Vietnam (primer destino efectivo), Chile, Sudáfrica, RD del Congo, entre otros (`[PVDP]`) | D | No |
| **3** | Nuestra futura planta potencialmente habilitable para ese destino | **No existe planta**. Depende de DEC-009 y DEC-012 y del listado por destino (Res. SENASA 593/2026) | D (condición habilitante, no demanda) | No |
| **4** | Importador o trader identificado para un producto y destino | **Ninguno** | C | No (solo opción de diseño) |
| **5** | Negociación comercial (especificación, precio, volumen, condiciones de pago) | **Ninguna** | B | Parcialmente, con factor α y solo si el nivel 3 es alcanzable en plazo |
| **6** | Contrato u orden de compra | **Ninguno** | A | Sí |

**Consecuencias:**

1. **La exportación es hoy demanda de nivel ≤ 2 (categoría D) para todos los productos y destinos.** Por eso vale **0 kg/día** en todos los escenarios (SUP-022). La sensibilidad de [`escenarios_demanda.csv`](escenarios_demanda.csv) (`EXP-SENS-1` y `EXP-SENS-4`: 1 y 4 contenedores/mes ≈ 0,8 y 3,3 t/día) solo muestra órdenes de magnitud y **no se suma**.
2. **Problema del huevo y la gallina:** un importador rara vez firma (niveles 5–6) con una planta que no existe ni está listada (nivel 3). La exportación **no puede ser demanda base de la capacidad inicial**; entra como **opción de diseño** (congelado, cámaras, estándar higiénico, espacio), coherente con la variante "A/B preparado para C" (DEC-011, DEC-012).
3. **Función real de la exportación en la etapa inicial:** piso de valor para partes de bajo valor local (garras, menudencias) y válvula de excedentes (`17_exportacion/conclusiones_exportacion.md` §2). Esa función se modela en el balance de masa como **destino de partes**, no como demanda que justifique aves adicionales.

---

## 5. Inventario de la demanda identificada, clasificada (2026-09-29)

| Fuente de demanda | Qué se sabe | Categoría actual | Qué la haría subir |
|---|---|---|---|
| Carnicería familiar (AMBA) | Existe y vende pollo; volumen desconocido (DPV-004) | **A**, pero **sin cuantificar** (y volumen marginal frente a una planta: SUP-005) | Registro de 4–8 semanas de ventas por producto |
| Red de ~90 supermercados | Acceso potencial vía el inversor; número exacto, locales, volumen, productos, proveedor, precios, plazos y voluntad de compra **desconocidos** | **C condicionada** (entre C y D: ni siquiera los locales están identificados) | Lista de locales + datos de compra (→ C firme); reunión con compras y prueba piloto (→ B); carta de intención con volumen y precio (→ A) |
| Mayoristas, distribuidores, pollerías, carnicerías, gastronomía, hoteles, catering, industria | Ningún cliente identificado ([`canales_comerciales.md`](canales_comerciales.md)) | **D** | Relevamiento y entrevistas (DPV-040) |
| Exportación | Niveles 0–2 por destino | **D** | Importador identificado (→ C), negociación (→ B), contrato (→ A) |

**Demanda A + B documentada hoy: ~0 kg/día** (la carnicería familiar es A pero no está cuantificada). **No existe todavía base para dimensionar la planta.** Este es el hallazgo central del modelo.

---

## 6. Escenarios comerciales preliminares (no son pronósticos)

Datos en [`escenarios_demanda.csv`](escenarios_demanda.csv) (`ESC-CON`, `ESC-BAS`, `ESC-EXP`). Todos los valores son `[SUPUESTO]` de prueba (SUP-021): sirven para **probar órdenes de magnitud** (tipo de planta, logística, capital de trabajo, concentración), no para dimensionar. Todo su volumen es hoy **categoría C/D**.

| Escenario | Supermercados | Otros canales | **Mercado interno** | Exportación | **Total** | t/mes | t/año | Aves/día (1,8 kg) | Aves/día (2,1 kg) | Aves/día (2,4 kg) | % supermercados | % consumo nacional |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Conservador** | 1.000 (20 locales × 50 kg) | 500 | **1.500** | 0 | **1.500** | 45,6 | 548 | 833 | 714 | 625 | 66,7 % | 0,03 % |
| **Base** | 4.500 (45 locales × 100 kg) | 3.000 | **7.500** | 0 | **7.500** | 228,1 | 2.738 | 4.167 | 3.571 | 3.125 | 60,0 % | 0,13 % |
| **Expansivo** | 13.500 (90 locales × 150 kg) | 10.000 | **23.500** | 0 | **23.500** | 714,8 | 8.578 | 13.056 | 11.190 | 9.792 | 57,4 % | 0,41 % |

Unidades: kg de producto por día calendario, salvo indicación. Aves/día: aves faenadas por día calendario, suponiendo un mix que consume el ave completa (§2.4).

**Composición de "otros canales" (kg/día, valores de prueba):**

| Escenario | Mayoristas / distribuidores | Carnicerías / pollerías (incluye la carnicería familiar) | Gastronomía (restaurantes, hoteles, catering) | Industria | Total |
|---|---|---|---|---|---|
| Conservador | 0 | 400 | 100 | 0 | 500 |
| Base | 1.500 | 1.000 | 300 | 200 | 3.000 |
| Expansivo | 5.000 | 2.500 | 1.000 | 1.500 | 10.000 |

**Criterios de construcción:**

- **Conservador:** menos de un cuarto de la red compra, con volúmenes bajos; otros canales mínimos. Prueba si un volumen chico justifica algo más que una operación comercial con producto de terceros (DEC-018).
- **Base:** la mitad de la red compra un volumen intermedio y se abren mayoristas y canal tradicional. Prueba el rango en que la red sigue siendo más de la mitad de las ventas.
- **Expansivo:** toda la red a 150 kg/local/día y una cartera multicanal desarrollada. Prueba el extremo superior plausible sin exportación. Aun así, la red representa el 57 % de las ventas.
- **Exportación = 0** en los tres: no hay evidencia de nivel ≥ 4 (§4).

**Lecturas:**

1. El rango entre escenarios es de **~16 veces** (1,5 a 23,5 t/día; ~600 a ~13.000 aves/día). Con esa dispersión, **cualquier dimensionamiento hoy sería arbitrario**.
2. En los tres escenarios la red de supermercados pesa **57–67 % de las ventas**: el riesgo de concentración es estructural mientras la red sea el canal principal ([`estrategia_comercial.md` §1](estrategia_comercial.md)).
3. Aun el escenario expansivo es **pequeño frente a las plantas medianas del sector** (80.000 a >200.000 aves/día en empresas medianas y grandes, `01_mercado` §2.1, `[PVDP · débil]`). Esto no implica que haya que crecer para parecerse a ellas, pero sí que la **escala mínima eficiente** de una faena propia debe contrastarse con la demanda demostrable (§7) y que las alternativas de primera etapa (compraventa, faena a façon) deben evaluarse (DEC-004, DEC-018). La escala mínima eficiente no se estima en esta sesión.
4. Si el mix es de trozado o de valor agregado, las aves necesarias pueden ser **15–53 % más** que en la tabla, con excedentes de partes que requieren otros canales ([`supermercados.md` §2](supermercados.md)).

---

## 7. Regla para dimensionar la planta (metodología conceptual para la fase posterior)

**No se calcula aquí ninguna capacidad** (regla 9). Se propone el método (DEC-014).

### 7.1 Fórmula conceptual

```
Demanda de diseño de la etapa 1 (kg/día) = D_A + α × D_B
Capacidad de la etapa 1 (kg/día)         = Demanda de diseño × (1 + m) 
Aves/día de faena                        = Capacidad × f_mix × (365 / días de faena por año) / p

  D_A   = demanda base (categoría A) en kg de producto/día, por producto
  D_B   = demanda en desarrollo (categoría B), por producto
  α     = factor prudente de conversión de B en ventas (0 ≤ α < 1); se calibra con evidencia (tasa real de conversión de negociaciones)
  m     = margen de crecimiento previsto para los primeros años, respaldado por el pipeline (no por el mercado total)
  f_mix = factor de balance de partes (≥ 1): aves necesarias por la parte limitante / aves calculadas con kg totales (§2.4)
  p     = peso comercial equivalente canal por ave (SUP-019; definitivo en 04_balance_masa)
```

- **Categoría C:** no entra en la capacidad inicial; define **reservas** (terreno, espacio en el layout, potencia eléctrica, agua y efluentes) para etapas futuras.
- **Categoría D:** nunca entra; solo verifica que el mercado no sea un techo.
- **Partes excedentes** (el f_mix): cada parte debe tener **al menos dos salidas** identificadas (`17_exportacion/estrategia_valorizacion_ave.md` §5); si no, su valor es el de rendering.
- Los valores de α, m y los umbrales de expansión **no se fijan en esta fase**.

### 7.2 Cómo evitar el sobredimensionamiento

1. No contar demanda C ni D; no suponer que los 90 locales compran ni que lo hacen a 100 %.
2. No sumar demanda de una parte limitante sin canal para el resto del ave.
3. Diseñar por **módulos y etapas**: espacio reservado, equipos agregables, segundo turno como palanca de crecimiento antes que capacidad instalada ociosa.
4. **Disparadores de expansión basados en evidencia:** por ejemplo, que A + α·B supere un porcentaje de la capacidad durante varios meses consecutivos (umbral a definir).
5. **Prueba de estrés:** la capacidad debe seguir siendo viable si se pierde el mayor cliente ([`estrategia_comercial.md` §1](estrategia_comercial.md)).
6. Separar el capital de trabajo del CAPEX: un canal con plazos largos de pago consume caja aunque la planta esté bien dimensionada.
7. No dimensionar por la escala de los líderes ni por el capital disponible (reglas 7 y 8).

### 7.3 Cómo evitar el subdimensionamiento

1. Contrastar con la **escala mínima eficiente** (costo unitario de faena, frío y personal): si la demanda demostrable queda debajo, **no inflar la demanda**; evaluar compraventa, faena a façon o una etapa comercial previa (DEC-004, DEC-018).
2. Considerar los **plazos de expansión** (habilitación SENASA, obra, equipos): reservar terreno y servicios para no quedar bloqueados si la demanda se confirma rápido.
3. Dimensionar los **cuellos de botella por parte**, no solo aves/hora: deshuese, elaborados, congelado y cámaras (el mix manda).
4. Prever **capacidad de congelado y almacenamiento** para colocar excedentes y acumular lotes de exportación (un contenedor = 24–27 t, `[PVDP · débil]`).
5. Asegurar abastecimiento de **pollo vivo o pollito BB** coherente con la capacidad (DPV-006): una planta sin aves es el subdimensionamiento más caro.
6. Mantener **tercerización como amortiguador** (faena a façon, compra de producto) para picos y para la transición entre etapas.

---

## 8. Datos que cambiarían materialmente el resultado

| Dato | Efecto sobre el orden de magnitud | Registro |
|---|---|---|
| kg/semana reales de pollo de la red, por local y por producto | Hasta **×12** entre 25 y 300 kg/local/día | DPV-003, DPV-037 |
| Cantidad de locales que efectivamente comprarían (adhesión) | Hasta **×9** entre 10 y 90 locales | DPV-002 |
| Mix de productos | Aves necesarias ×1,0 a ×1,5; excedentes de 2–7 t/día por cada 9 t/día; procesos requeridos (deshuese, elaborados) | DPV-037 |
| Relación del inversor con la red y quién decide compras | Define si la red es C o puede pasar a B/A; riesgo de partes vinculadas | DPV-038 |
| Proveedor actual, contratos y exclusividades | Momento y velocidad de entrada | DPV-020 |
| Plazos de pago y condiciones comerciales | Capital de trabajo; precio cobrado | DPV-039 |
| Logística (CD vs entrega a locales) | Costo por kg y flota | DPV-036, DPV-042 |
| Peso comercial por ave | ±33 % de aves para los mismos kg | DPV-008 |
| Demanda de otros canales para las partes excedentes | Viabilidad de mixes con mucha pechuga | DPV-040 |
| Exportación en nivel ≥ 5 para algún producto | Cambia la exportación de 0 a demanda B | DPV-032 |

---

## 9. Documentación de `escenarios_demanda.csv` (regla 15)

Separador decimal: punto. Codificación UTF-8. Todas las cifras son `[SUPUESTO]` (valores de prueba) salvo las sensibilidades de exportación (`[ESTIMACIÓN]`). Las columnas derivadas se calculan con las fórmulas de §2.3.

| Columna | Unidad | Descripción |
|---|---|---|
| `id` | — | `RED-###` (red de 90 locales a ### kg/local/día), `ESC-CON/BAS/EXP` (escenarios comerciales), `EXP-SENS-n` (sensibilidad de exportación de n contenedores/mes) |
| `bloque` | — | `red_supermercados`, `escenario_comercial`, `sensibilidad_exportacion` |
| `escenario`, `descripcion` | — | Nombre y criterio de construcción |
| `locales`, `kg_local_dia` | locales; kg de producto/local/día calendario | Parámetros de la red |
| `supermercados_kg_dia` … `industria_kg_dia` | kg de producto/día calendario | Volumen por canal |
| `otros_canales_kg_dia` | kg/día | Suma de mayoristas/distribuidores, carnicerías/pollerías, gastronomía e industria |
| `mercado_interno_kg_dia` | kg/día | Supermercados + otros canales |
| `exportacion_kg_dia` | kg/día | 0 en escenarios (SUP-022); solo positivo en `EXP-SENS` (reefers de 25 t/mes ÷ 30,42) |
| `total_kg_dia`, `t_dia`, `t_mes`, `t_anio` | kg, t | Totales (30,42 días/mes; 365 días/año) |
| `aves_dia_p1_8`, `aves_dia_p2_1`, `aves_dia_p2_4` | aves faenadas/día calendario | total_kg_dia ÷ 1,8 / 2,1 / 2,4 kg equivalente canal por ave (SUP-019) |
| `pct_supermercados` | % | Participación de la red en el total |
| `pct_consumo_nacional` | % | total_kg_dia ÷ 5.753.425 kg/día (2,1 Mt/año `[PVDP]`) |
| `pct_consumo_amba_estimado` | % | total_kg_dia ÷ 1.726.027 kg/día (30 % del nacional, SUP-024) |
| `categoria_demanda_actual` | — | Categoría A/B/C/D que corresponde hoy a ese volumen |
| `clasificacion_dato` | — | Etiqueta de la regla 4 |
| `sumable_a_demanda` | — | `no` en todas las filas: ningún escenario es demanda documentada |
| `observaciones` | — | Advertencias |

---

## 10. Control de calidad

- [x] Ninguna hipótesis aparece como venta confirmada; todos los volúmenes están etiquetados `[SUPUESTO]` o `[ESTIMACIÓN]` y clasificados C/D.
- [x] Se separa demanda (A/B/C) de mercado total (D).
- [x] Se separan kg de producto, kg equivalente canal, aves faenadas y kg vivo (§2.1).
- [x] Los pesos de conversión se declaran como rango (1,8 / 2,1 / 2,4 kg) con su derivación y fuentes `[PVDP]`.
- [x] No se inventan compradores ni precios; no hay ningún precio en el modelo.
- [x] La exportación no figura como demanda asegurada (0 kg/día; niveles 0–6).
- [x] Se indica qué datos cambian materialmente el resultado (§8).
- [x] No se dimensiona la planta ni se fija capacidad (§7 es solo metodología).
