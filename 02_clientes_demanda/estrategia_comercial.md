# Estrategia comercial — concentración, precio y margen, marca e indicadores

**Fecha:** 2026-09-29 · **Versión:** 1 (conceptual) · Marco: [`modelo_demanda.md`](modelo_demanda.md)

> **No se elige estrategia** (marca, canal, límites de concentración) en esta fase. Se definen los conceptos, las métricas y los datos necesarios para decidir después (DEC-015, DEC-017, DEC-019). No se construye el modelo financiero (`21_modelo_financiero`).

---

## 1. Concentración de clientes

### 1.1 Fuentes de concentración a vigilar

| Tipo | Riesgo | Por qué es especialmente relevante aquí |
|---|---|---|
| **Un solo inversor** | Si el inversor es a la vez socio y dueño o decisor del principal cliente, su salida (o un conflicto) afecta capital y ventas al mismo tiempo; precios y plazos pueden no ser de mercado | La red está "vinculada al potencial inversor" (DPV-038) |
| **Una única cadena** (o grupo económico) | Poder de negociación del cliente; pérdida súbita de volumen; plazos de pago impuestos | En los tres escenarios la red pesa 57–67 % de las ventas ([`modelo_demanda.md` §6](modelo_demanda.md)) |
| **Pocos clientes** | Volatilidad de ventas; costos fijos sin cubrir si se pierde uno | Etapa inicial con cartera chica |
| **Un único país extranjero** | Cierre sanitario o político; precio | Caso China (`17_exportacion`), SUP-016 |
| **Un solo producto o parte por cliente** | Si toda la pechuga va a un cliente, su salida deja sin destino a la parte más valiosa | Balance de partes ([`supermercados.md` §2.3](supermercados.md)) |
| **Un solo operador logístico o CD** | Interrupción del abastecimiento | Depende de DPV-036 |

### 1.2 Métricas propuestas

La concentración se mide por **grupo económico o centro de decisión de compra**, no por razón social: 90 locales de varias sociedades con un mismo decisor son, a efectos de riesgo, **un cliente**.

| Métrica | Fórmula | Unidad | Frecuencia |
|---|---|---|---|
| % ventas del mayor cliente | Ventas del mayor grupo económico / ventas totales | % (en kg y en $) | Mensual |
| % top 5 y top 10 | Ventas de los 5 (10) mayores / ventas totales | % | Mensual |
| Índice Herfindahl-Hirschman (HHI) de clientes | Σ (participación_i en %)² | 0–10.000 | Trimestral |
| % ventas a partes vinculadas | Ventas a clientes vinculados al inversor / ventas totales | % | Mensual |
| % por canal | Ventas por canal (supermercados, mayoristas, tradicional, gastronomía, industria, exportación) / total | % | Mensual |
| % mercado local vs exportación | Ventas locales / exportación / total | % | Mensual |
| % exportación del mayor país destino | Exportación al mayor país / exportación total | % | Trimestral |
| % exportación a destinos que exigen país libre de IAAP | Esos destinos / exportación total (riesgo de cierre simultáneo) | % | Trimestral |
| Concentración por parte del ave | % de cada parte (pechuga, pata-muslo, etc.) vendida al mayor cliente | % | Trimestral |
| Exposición crediticia del mayor cliente | Saldo por cobrar del mayor cliente / capital de trabajo (o patrimonio) | % | Mensual |
| Prueba de estrés | Margen de contribución perdido si se va el mayor cliente / costos fijos | % | Semestral |

### 1.3 Ilustración con los escenarios de prueba

Si la red actúa como un solo decisor, el mayor cliente sería la red. El **HHI mínimo** (con el resto de las ventas totalmente atomizado) es la participación de la red al cuadrado:

| Escenario | % red en ventas | HHI mínimo (solo la red) |
|---|---|---|
| Conservador | 66,7 % | ~4.450 |
| Base | 60,0 % | ~3.600 |
| Expansivo | 57,4 % | ~3.300 |

`[ESTIMACIÓN]` sobre valores de prueba. Cualquier otro cliente grande (por ejemplo, un mayorista) suma a esos valores. **No se definen todavía límites** (DEC-017); se registra que, con la red como canal principal, la concentración en un solo decisor sería **muy alta en todos los escenarios**, y que diversificar hacia mayoristas, industria y gastronomía es una condición de robustez, no un complemento.

---

## 2. Precio y margen: qué datos se necesitan

### 2.1 De precio de lista a margen

```
PRECIO DE LISTA (sin IVA, $/kg)
  − descuentos en factura (comerciales, por volumen, por pronto pago)
  = precio facturado
  − bonificaciones fuera de factura (rebates por volumen, aniversarios, aperturas de locales,
    fee de alta de producto, fee de centro de distribución, aportes a folletos y exhibición)
  − promociones financiadas por el proveedor
  = PRECIO NETO
  − devoluciones y notas de crédito, mermas en góndola a cargo del proveedor,
    penalidades por nivel de servicio, débitos no acordados
  − costo financiero del plazo de cobro  (precio × tasa × días de cobro / 365)
  − efecto financiero de retenciones y percepciones impositivas
  = PRECIO COBRADO (efectivo recibido por kg, en valor presente)
  − costo de servir al cliente (logística, paradas, fee de CD si no se descontó antes,
    comisiones de vendedores o distribuidores, packaging específico, repositores)
  − costo del producto (parte del ave + proceso + empaque)
  = MARGEN (de contribución) por kg
```

| Concepto | Definición | Error típico que evita |
|---|---|---|
| **Precio de lista** | Precio publicado por el proveedor, sin IVA | Confundir la lista con el ingreso |
| **Precio neto** | Precio después de todos los descuentos, bonificaciones y promociones acordados | Ignorar los costos comerciales fuera de factura |
| **Precio cobrado** | Efectivo que efectivamente entra por kg, neto de devoluciones, débitos y costo financiero del plazo | Tratar como iguales a un cliente que paga a 7 días y otro a 60 |
| **Margen** | Precio cobrado − costo de servir − costo del producto | Comparar canales por precio en lugar de margen |

**Costos conjuntos:** el costo de cada parte del ave depende del método de asignación (por peso, por valor de venta relativo). Por eso: (a) la **métrica global** es el **margen por ave** (ingreso total por ave − costo por ave), coherente con SUP-013; (b) las decisiones de **a qué canal va cada parte** se toman comparando net-backs de esa parte entre canales (`17_exportacion/estrategia_valorizacion_ave.md` §1), sin necesidad de asignar costos conjuntos.

### 2.2 Datos comerciales necesarios

| Dato | Por canal y producto | Registro |
|---|---|---|
| Precio de venta (lista) sin IVA, con fecha y tipo de cambio | Sí | DPV-013, DPV-039 |
| Descuentos en factura | Sí | DPV-039 |
| Bonificaciones y fees (alta, CD, aperturas, aniversarios) | Sí | DPV-039 |
| Promociones: frecuencia, profundidad, quién las financia | Sí | DPV-039 |
| Costo logístico por kg (por modelo de entrega) | Sí | DPV-042 |
| Plazo de cobro (días desde la entrega) y medio de pago | Sí | DPV-039 |
| Devoluciones (% del volumen) y causas | Sí | DPV-039 |
| Merma (en planta, en tránsito, en góndola a cargo del proveedor) | Sí | DPV-039 |
| Comisiones (vendedores, distribuidores, brokers) | Sí | DPV-040 |
| Impuestos: alícuota de IVA de la carne aviar, ingresos brutos por jurisdicción, regímenes de retención y percepción, impuesto a los débitos y créditos | Por jurisdicción | DPV-043 |
| Tasa de costo financiero de referencia | General | DEC-006 |

Todo precio en ARS se registra con fecha, fuente y tipo de cambio (reglas 2 y 5). **Ningún precio se estima en esta sesión.**

---

## 3. Marca propia vs marca blanca vs modelo mixto

| Dimensión | **A. Marca propia** | **B. Marca blanca** (marca del supermercado o cliente) | **C. Modelo mixto** |
|---|---|---|---|
| Margen | Potencialmente mayor si la marca logra preferencia; en commodity (entero) el premio de marca puede ser bajo | Menor por kg (el cliente captura el valor de marca), pero con volumen más previsible | Intermedio; permite margen de marca donde existe y volumen donde no |
| Marketing | Requiere inversión sostenida (diseño, comunicación, degustaciones, aportes a promociones) | Casi nulo para el proyecto | Focalizado en los productos y canales donde la marca rinde |
| Fidelización | Del consumidor final hacia la empresa; activo transferible entre canales | Del consumidor hacia el supermercado; el proveedor es reemplazable | Parcial |
| Volumen | Crece lento; depende de la aceptación | Puede ser alto desde el inicio si el cliente decide | Combina ambos |
| Negociación | Mejor posición con cada cliente si la marca tiene demanda propia | **Débil**: el cliente puede licitar el mismo producto con otro proveedor | Media |
| Inversión | Mayor (marca, registros de rótulo, packaging propio, equipo comercial) | Menor en marca; el cliente puede exigir especificaciones, auditorías y packaging específicos | Intermedia |
| Riesgo | Comercial (que la marca no despegue) | **Concentración**: el producto con marca del cliente no se puede vender a otro; aumenta la dependencia de la red | Complejidad operativa (varios packagings y especificaciones) |
| Colocación de excedentes | Mayor libertad (la marca va a cualquier canal) | Los excedentes deben ir sin marca o con otra marca | Flexible |

**Observaciones sin decisión (DEC-015):**

- Con una red vinculada al inversor, la **marca blanca maximiza la dependencia** de ese cliente; la **marca propia** construye un activo que sirve para diversificar canales, a mayor costo.
- En productos commodity (entero, pata-muslo) el valor de marca es probablemente menor que en elaborados y porcionados de peso fijo (hipótesis a validar con precios de góndola, DPV-013).
- El interés de la red en marca propia o blanca es una pregunta del cuestionario (2.10).

---

## 4. Indicadores comerciales a seguir (fase operativa)

| Indicador | Fórmula / definición | Unidad | Frecuencia |
|---|---|---|---|
| kg vendidos/día | kg facturados − devoluciones, por día calendario | kg/día | Diaria / semanal |
| kg por cliente | kg vendidos por grupo económico | kg/semana | Semanal |
| kg por producto | kg por SKU y por parte del ave | kg/semana | Semanal |
| Precio promedio/kg | Precio neto (y cobrado) ponderado por kg | $/kg y USD/kg | Mensual |
| Margen/kg | Margen de contribución / kg vendidos; también **margen por ave** | $/kg; $/ave | Mensual |
| Ingreso total por ave | Σ kg de cada parte × precio neto / aves faenadas | $/ave | Mensual |
| Días de cobro (DSO) | Cuentas por cobrar / ventas diarias | días | Mensual |
| Concentración de clientes | Métricas de §1.2 | % / HHI | Mensual / trimestral |
| Devoluciones | kg devueltos / kg entregados (por cliente y causa) | % | Semanal |
| Fill rate | kg entregados / kg pedidos | % | Semanal |
| Nivel de servicio (OTIF) | Pedidos entregados completos y a tiempo / pedidos totales | % | Semanal |
| Crecimiento mensual | kg (y $ constantes) del mes / mismo indicador del mes anterior y del año anterior | % | Mensual |
| Forecast vs real | Error absoluto porcentual medio (MAPE) y sesgo del pronóstico de kg por producto | % | Mensual |
| Partes sin destino premium | kg de partes vendidas a rendering o a precio de liquidación / kg producidos | % | Mensual |
| Pipeline A/B/C | kg/día por categoría de demanda y tasa de conversión B → A (calibra el factor α, [`modelo_demanda.md` §7](modelo_demanda.md)) | kg/día; % | Mensual |

**Desde ahora (fase de validación)** conviene llevar el **pipeline A/B/C/D**: una planilla por cliente potencial con canal, productos, kg/semana estimados, fuente (FTE de la entrevista), categoría y fecha de la última evidencia. Es la base de la regla de dimensionamiento.
