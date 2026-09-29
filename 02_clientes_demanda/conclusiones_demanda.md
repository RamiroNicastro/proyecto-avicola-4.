# Conclusiones del modelo de demanda comercial

**Fecha:** 2026-09-29 · **Versión:** 1 · Base: [`modelo_demanda.md`](modelo_demanda.md), [`supermercados.md`](supermercados.md), [`canales_comerciales.md`](canales_comerciales.md), [`estrategia_comercial.md`](estrategia_comercial.md), [`escenarios_demanda.csv`](escenarios_demanda.csv)

> **No se dimensiona la planta** ni se fija capacidad (regla 9). **Ningún volumen de este estudio es una venta confirmada.** Todos los escenarios son pruebas de orden de magnitud (SUP-021). No se inventan compradores ni precios.

---

## 1. Hallazgos principales

1. **La demanda documentada hoy (categorías A + B) es prácticamente nula.** Solo la carnicería familiar es demanda base, y no está cuantificada (DPV-004). La red de supermercados es categoría **C condicionada** (ni siquiera la lista de locales está disponible). Otros canales y exportación son **D**. **No hay todavía base para dimensionar la planta.**
2. **Escenarios de prueba** (kg de producto por día calendario; exportación 0 en todos):

   | Escenario | Supermercados | Otros canales | Total | Aves/día (2,4 – 1,8 kg por ave) |
   |---|---|---|---|---|
   | Conservador | 1.000 | 500 | 1.500 | 625 – 833 |
   | Base | 4.500 | 3.000 | 7.500 | 3.125 – 4.167 |
   | Expansivo | 13.500 | 10.000 | 23.500 | 9.792 – 13.056 |

   El rango entre escenarios es de **~16 veces**: cualquier dimensionamiento hoy sería arbitrario.
3. **Los 90 supermercados**, si todos compraran todo su pollo al proyecto, representarían de **2,25 t/día (25 kg/local) a 27 t/día (300 kg/local)**, es decir, de ~940 a ~15.000 aves/día según el peso por ave. Con adhesión parcial, el rango va de **0,25 a 27 t/día** (dos órdenes de magnitud) ([`supermercados.md` §1](supermercados.md)).
4. **El mercado no es el límite:** aun 27 t/día serían ~0,5 % del consumo nacional y ~1,6 % del consumo estimado del AMBA. El límite es el **acceso comercial demostrable** y el desplazamiento de proveedores existentes en un mercado maduro.
5. **El mix importa tanto como los kg:** con los mismos 9.000 kg/día, un mix orientado a pechuga y milanesas puede requerir **hasta ~1,5 veces más aves** y generar **hasta ~7 t/día de partes excedentes** que necesitan otros canales (ejemplo ilustrativo con rendimientos supuestos). La red **no puede ser el único canal** aunque compre mucho.
6. **Concentración estructural:** en los tres escenarios la red pesa **57–67 %** de las ventas; si actúa como un solo decisor, el HHI mínimo sería de ~3.300 a ~4.450. Sumado al vínculo con el inversor, es el principal riesgo comercial del modelo.
7. **La logística de la red puede cambiar el costo por kg más que el precio:** entregar a 90 locales con 58 kg por parada cuesta por kg ~12 veces más que con 700 kg por parada; un CD cambia la ecuación. **Conocer la red logística es prioritario** (DPV-036).
8. **La exportación no es demanda hoy** (niveles 0–2 para todos los productos y destinos). Un importador difícilmente firme con una planta inexistente: la exportación entra como **opción de diseño y piso de valor de partes**, no como base de capacidad.

---

## 2. Los 10 datos más importantes a conseguir del contacto

Detalle y formulación en [`cuestionario_supermercados.md`](cuestionario_supermercados.md).

| # | Dato | Registro | Impacto |
|---|---|---|---|
| 1 | Cantidad exacta de locales que venden pollo y su ubicación | DPV-002, DPV-018 | Tamaño del canal (hasta ×9); habilitación |
| 2 | kg de pollo comprados por semana (reporte de 12 meses) | DPV-003 | Tamaño del canal (hasta ×12) |
| 3 | kg por producto (mix) y refrigerado vs congelado | DPV-037 | Aves necesarias (×1,0–1,5), procesos, excedentes |
| 4 | Proveedor(es) actual(es) y participación | DPV-020 | Competencia directa y ventana de entrada |
| 5 | Contratos, exclusividades y vencimientos | DPV-020 | Momento de entrada |
| 6 | Centros de distribución y esquema de entrega | DPV-036 | Costo por kg, flota |
| 7 | Precios de compra por producto y plazo de pago | DPV-013, DPV-039 | Margen y capital de trabajo |
| 8 | Quién decide la compra y relación del inversor con la red | DPV-038 | Si la red puede pasar a B/A; partes vinculadas |
| 9 | Voluntad concreta de compra (productos, % del volumen) | DPV-002 | Paso de C a B |
| 10 | Volumen mínimo de prueba y posibilidad de carta de intención | DPV-002 | Paso de B a A |

---

## 3. Canales comerciales más relevantes para investigar

1. **Red de supermercados** (cliente ancla potencial).
2. **Mayoristas y distribuidores del AMBA** (volumen, baja complejidad logística, salida para partes y excedentes, diversificación).
3. **Industria alimenticia y fábricas de elaborados** (CMS, recortes, deshuesados; sustitución de importaciones de Brasil).
4. **Gastronomía de cadena y catering** (especificación estable; valoriza pechuga y porcionados).
5. **Pollerías y carnicerías**, empezando por la carnicería familiar (aprendizaje, cobro rápido a validar).

Fichas y matriz parte–canal en [`canales_comerciales.md`](canales_comerciales.md).

---

## 4. Principales riesgos comerciales

| Riesgo | Descripción | Probabilidad | Impacto | Mitigación conceptual |
|---|---|---|---|---|
| **Demanda inexistente o menor a la esperada** | La red no compra, o compra poco, o solo algunos productos | Desconocida (sin datos) | Muy alto | No invertir en capacidad antes de A/B documentada; validar con prueba piloto |
| **Concentración en un cliente vinculado al inversor** | Pérdida conjunta de capital y ventas; precios no de mercado | Alta si la red es el canal principal | Muy alto | Métricas de concentración; reglas escritas para partes vinculadas (DEC-019); diversificación |
| **Desbalance de partes** | Mix con mucha pechuga y sin canal para el resto del ave | Media–alta | Alto | Canales para cada parte antes de dimensionar; ingreso total por ave |
| **Costos comerciales y logísticos ocultos** | Bonificaciones, fees, devoluciones, entregas atomizadas | Alta | Alto | Relevar el "waterfall" completo de precio (DPV-039, DPV-042) |
| **Plazos de pago largos** | Capital de trabajo con producto perecedero | Alta | Alto | Dato de plazo por canal; mezcla de canales con cobro rápido |
| **Proveedor actual atrincherado** | Contratos, exclusividades o relación de largo plazo | Desconocida | Alto | Pregunta 1.10 del cuestionario |
| **Precio gancho y sobreoferta sectorial** | Promociones del supermercado y caídas de precio por cierres de exportación del sector | Alta | Alto | Mix de mayor valor; diversificación de canales |
| **Requisitos de alta de proveedor** | Habilitación federal, auditorías, codificación, trazabilidad | Alta | Medio–alto | DPV-041, DEC-009 |
| **Competencia importada** | Pechuga y elaborados de Brasil | Media–alta | Medio | Precios de referencia de importados |
| **Exportación tomada como demanda** | Dimensionar con demanda externa de nivel ≤ 3 | Evitable | Muy alto | Regla de niveles 0–6 |

---

## 5. Información que falta antes de dimensionar la planta

| Prioridad | Información | Registro |
|---|---|---|
| Crítica | Volumen y mix reales de la red (kg/semana por producto y por local, 12 meses) | DPV-003, DPV-037 |
| Crítica | Lista de locales, CD y esquema logístico | DPV-002, DPV-018, DPV-036 |
| Crítica | Proveedor actual, contratos y exclusividades | DPV-020 |
| Crítica | Relación inversor–red y decisor de compras | DPV-038 |
| Crítica | Evidencia de compromiso (reunión con compras, prueba piloto, carta de intención) | DPV-002 |
| Alta | Condiciones comerciales completas (precios, bonificaciones, plazos, devoluciones) | DPV-039 |
| Alta | Demanda de otros canales para las partes que la red no absorbe | DPV-040 |
| Alta | Rendimientos por parte y peso de faena (factor de mix y conversión a aves) | DPV-008 |
| Alta | Precios por corte y por canal | DPV-013 |
| Alta | Requisitos de alta de proveedor y habilitación exigida | DPV-041, DEC-009 |
| Media | Costos de distribución refrigerada en AMBA | DPV-042 |
| Media | Tratamiento impositivo de las ventas | DPV-043 |
| Media | Ventas de la carnicería familiar | DPV-004 |
| Media | Disponibilidad de faena a façon y de producto de terceros para una etapa de validación comercial | DPV-006, DEC-018 |
| Baja (para la etapa 1) | Importadores identificados (nivel ≥ 4) | DPV-032 |

---

## 6. Tareas de campo

**Prioridad:** 🔴 puede cambiar el tamaño de la planta · 🟠 cambia diseño, costos o capital de trabajo · 🟢 afina el modelo.

### 6.1 Tareas de Ramiro / familia

| # | Tarea | Prioridad | Plazo sugerido | Registro |
|---|---|---|---|---|
| R1 | Pedir al inversor la **lista de locales** (dirección, formato) y armar un mapa | 🔴 | 2 semanas | DPV-018 |
| R2 | Enviar al inversor el **bloque 0** del cuestionario y coordinar la reunión con compras y logística | 🔴 | 2 semanas | DPV-038 |
| R3 | **Relevar en góndola 10–20 locales de la red**: productos de pollo exhibidos, marcas, precios, refrigerado/congelado, packaging, marca propia del supermercado (se puede hacer sin el contacto) | 🔴 | 3 semanas | DPV-020, DPV-037 |
| R4 | Registrar **4–8 semanas de ventas de pollo de la carnicería familiar** por producto, con precio de compra y venta, proveedor y plazo | 🟠 | 4–8 semanas | DPV-004 |
| R5 | Entrevistar a **3–5 distribuidores o mayoristas** y **5–10 pollerías/carnicerías** del AMBA (ficha de [`canales_comerciales.md` §4](canales_comerciales.md)) | 🟠 | 6 semanas | DPV-040 |
| R6 | Registrar cada entrevista como fuente (`entrevista`) y llevar el **pipeline A/B/C/D** | 🟢 | Continuo | [`estrategia_comercial.md` §4](estrategia_comercial.md) |

### 6.2 Tareas para el potencial inversor

| # | Tarea | Prioridad | Registro |
|---|---|---|---|
| I1 | Aclarar su **relación con la red** y **quién decide** la compra de pollo | 🔴 | DPV-038 |
| I2 | Facilitar un **reporte de compras de pollo** (kg y $ por producto, por local y por semana, 12 meses) | 🔴 | DPV-003, DPV-037 |
| I3 | Facilitar reunión con el **gerente de compras de perecederos** y el **responsable de logística/CD** | 🔴 | DPV-002, DPV-036 |
| I4 | Informar **proveedor actual, contratos, exclusividades** y condiciones | 🔴 | DPV-020, DPV-039 |
| I5 | Indicar si la red aceptaría una **prueba piloto** (volumen mínimo) y una **carta de intención** no vinculante | 🔴 | DPV-002 |
| I6 | Explicitar sus expectativas como **inversor y cliente a la vez** (precios, plazos, reglas para partes vinculadas) | 🟠 | DEC-019 |
| I7 | Informar los **requisitos de alta de proveedor** de la red | 🟠 | DPV-041 |

### 6.3 Tareas para el futuro equipo comercial (fases siguientes)

| # | Tarea | Prioridad | Registro |
|---|---|---|---|
| C1 | Mapear y entrevistar **≥10 mayoristas y distribuidores** del AMBA | 🔴 | DPV-040 |
| C2 | Relevar **industria alimenticia y fábricas de elaborados** (CMS, recortes, deshuesados): especificaciones, volúmenes, precios de referencia del importado | 🟠 | DPV-040 |
| C3 | Relevar **cadenas gastronómicas y catering** (homologación, calibres, licitaciones) | 🟠 | DPV-040 |
| C4 | Cotizar **distribución refrigerada** en AMBA (propia vs tercerizada; por kg y por parada) | 🟠 | DPV-042 |
| C5 | Evaluar una **etapa de validación comercial** con producto de terceros o faena a façon para convertir demanda C en B/A antes de invertir en planta | 🔴 | DEC-018, DPV-006 |
| C6 | Contactar **traders e importadores** para subir la exportación a nivel 4 en productos concretos (garras, pata-muslo, menudencias) | 🟢 (para la etapa 1) | DPV-032 |
| C7 | Implementar el tablero de **indicadores comerciales** y el pipeline | 🟢 | [`estrategia_comercial.md` §4](estrategia_comercial.md) |

---

## 7. Control de calidad

- [x] Ninguna hipótesis aparece como venta confirmada; todos los volúmenes están etiquetados y clasificados C/D.
- [x] Se separa demanda (A/B/C) de mercado total (D); la exportación se clasifica por niveles 0–6.
- [x] Se separan kg de producto, kg equivalente canal, aves faenadas y kg vivo.
- [x] Pesos de conversión declarados como rango: 1,8 / 2,1 / 2,4 kg equivalente canal por ave (SUP-019).
- [x] No se inventan compradores ni precios (no hay ningún precio en los escenarios).
- [x] Exportación = 0 en todos los escenarios; sensibilidad separada y no sumable.
- [x] Se señalan los datos que cambian materialmente el resultado ([`modelo_demanda.md` §8](modelo_demanda.md)).
- [x] No se dimensiona la planta; la regla de dimensionamiento es solo metodológica.
- [ ] Verificación documental primaria de FTE-140 y FTE-141 (extractos de buscador; acceso directo bloqueado).

## 8. Evaluación de calidad

**MEDIA** como marco metodológico; **BAJA** como evidencia cuantitativa de demanda.

- **Fortalezas:** categorías de demanda con reglas de pasaje y uso en capacidad; niveles de exportación; conversiones con bases explícitas y sensibilidad de peso; efecto del mix cuantificado con un ejemplo; logística, concentración, precio-margen y marca conceptualizados; cuestionario y tareas priorizados por impacto en la escala.
- **Debilidades:** **cero datos de campo** (ningún volumen, precio, cliente ni condición real); valores de escenarios y mixes son supuestos de prueba; rendimientos por parte ilustrativos; las dos fuentes nuevas son extractos no verificados en su original. El modelo sirve para **ordenar la validación**, no para dimensionar.
