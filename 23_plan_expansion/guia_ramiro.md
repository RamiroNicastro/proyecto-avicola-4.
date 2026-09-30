# Guía para Ramiro — escala, capacidad y crecimiento por etapas

**Fecha:** 2026-09-30 · Lectura de 10 minutos. Cifras de [`escenarios_escala.md`](escenarios_escala.md) (escenario medio: pollo de 2,9 kg, 5 días de faena por semana).

El objetivo es poder responder **"¿por qué no construir directamente una planta de 20.000 pollos por día?"** con argumentos propios, no con "porque lo dijo el modelo".

---

## 1. Diez conceptos

**1. Capacidad nominal.** Lo que la planta podría hacer "en los papeles": velocidad de la línea × horas. Como la velocidad máxima de un auto: existe, pero no se maneja siempre así.

**2. Capacidad operativa y capacidad utilizada.** La operativa es lo que la planta puede sostener día tras día con su gente, su frío, sus efluentes y sus pollos disponibles. La **utilizada** es lo que efectivamente se faena. Utilización = faenado ÷ capacidad operativa. Una planta de 10.000 que faena 5.000 está al 50 %. **Capacidad no es ventas**: la planta puede faenar; vender depende de clientes.

**3. Cuello de botella.** La operación más lenta fija la capacidad de todo. Si la línea faena 1.250 pollos por hora pero la sala de deshuese solo procesa el equivalente a 800, la planta "es" de 800 para ese producto. Puede estar en la línea, en el enfriado, en el deshuese, en el túnel de congelado, en las cámaras, en el tratamiento de efluentes o… en la falta de pollos.

**4. Modularidad.** Diseñar para poder **agregar piezas** sin romper lo que funciona: dejar terreno, lugar para otra línea, potencia eléctrica reservada, espacio para más cámaras. Se prevé lo que es barato de prever y caro de corregir (terreno, caminos, permisos, flujos higiénicos); se construye por partes lo que es caro de tener parado (líneas, cámaras, salas de corte).

**5. Sobredimensionamiento.** Construir más capacidad de la que se va a usar. A 20.000 aves/día con la demanda del escenario base, la planta estaría al **23–41 %**: tres cuartos de lo construido sin uso.

**6. Subdimensionamiento.** Construir menos de lo necesario, o sin posibilidad de crecer. Riesgos: clientes que no se pueden atender, costo por pollo alto, y una planta que hay que abandonar o duplicar mal si la demanda crece. **Arrancar chico no es arrancar sin prever el crecimiento.**

**7. Escala mínima (eficiente).** El tamaño por debajo del cual el costo por pollo es demasiado alto porque lo fijo (edificio, frío, habilitaciones, personal mínimo, tratamiento de efluentes) se reparte entre pocos pollos. **No la conocemos todavía**: se calcula con CAPEX y OPEX. Por eso no se puede afirmar que 2.500 aves/día sea viable solo porque se llena más fácil.

**8. Economías de escala.** A más volumen, algunos costos por unidad bajan (lo fijo se reparte; se compra mejor; se llenan contenedores). Pero **solo si la planta está llena**. Una planta grande vacía tiene **deseconomías**: todo lo fijo sobre pocos pollos.

**9. Riesgo de demanda.** El riesgo de producir sin comprador. Hoy la demanda documentada es **prácticamente cero**: los 90 supermercados son potenciales, los escenarios comerciales son hipótesis y la exportación no tiene ni un importador identificado. Además, no alcanza con que compren "kilos": tienen que comprar **todas las partes** del pollo o hay que encontrar a quién venderle el resto.

**10. Expansión por etapas.** Crecer de a pasos, cada uno habilitado por **métricas verificables** (contratos, planta llena con clientes reales, pollitos y productores asegurados, salida para subproductos), no por entusiasmo. Hay palancas baratas antes de construir: un **sexto día** de faena da +20 %; un **segundo turno** duplica la capacidad sobre la misma línea.

---

## 2. ¿Por qué no construir directamente una planta de 20.000 pollos por día?

No es "porque lo dijo el modelo". Es porque **tiene que ser verdad todo esto a la vez**, y hoy **nada** de esto está demostrado:

| Para operar 20.000 pollos/día tiene que ser verdad que… | Cuánto es | Qué sabemos hoy |
|---|---|---|
| Alguien compra el producto | ~33 t/día calendario de producto (vendiendo **todo** el pollo); ~365 kg de pollo por local por día si todo pasara por los 90 supermercados | La red, si comprara todo su pollo a 150 kg/local, más otros canales desarrollados, es el **escenario expansivo** (23,5 t/día): llenaría el **72 %**. La demanda documentada es ~0 |
| Alguien compra **cada parte** | Con un mix de supermercado sobran hasta ~12 t/día de pata-muslo, alas, carcasa, cuello, garras aun con la planta llena | No hay compradores identificados para esas partes |
| Hay pollitos | ~105.600 pollitos BB **por semana** | Sin contratos ni proveedores relevados |
| Hay dónde criarlos | ~76.000 m² de galpones (~32 galpones de 2.400 m²), ~964.000 plazas, 8 a 32 productores | Sin productores relevados en ninguna zona |
| Hay alimento | ~494 t por semana; ~24.700 t por año | Sin estrategia de alimento |
| Hay a quién darle los subproductos todos los días | ~11–17 t/día (plumas, sangre, vísceras, cabezas…), más ~8 t/día de carcasa | Sin receptores identificados |
| Hay frío y logística | 336 t de producto por semana de inventario; ~58 t de pollo vivo entrando por día | No diseñado |
| Hay capital | CAPEX y capital de trabajo **no calculados** | USD 2 M es solo una referencia, no comprometida |

**Y si se construye grande y la demanda no llega:** una planta de 20.000 al 50 % faena lo mismo que una de 10.000 llena, pero paga (en capital, energía, mantenimiento, personal mínimo, habilitaciones) como una de 20.000. La tentación de "llenarla" lleva a vender barato o a clientes que desbalancean el pollo.

**Lo que sí conviene hacer si se aspira a 20.000:** elegir un terreno y servicios que **permitan** llegar (y no se puedan perder después), diseñar el edificio y los flujos para crecer, y ampliar cuando las métricas lo pidan ([`gates_expansion.md`](gates_expansion.md)). La aspiración define la **reserva**; la evidencia define la **construcción**.

**El argumento también vale al revés:** tampoco es obvio que haya que empezar con 2.500. Puede estar debajo de la escala mínima eficiente o no poder crecer si no se prevé. Por eso la respuesta honesta hoy es: **"no sabemos todavía cuál es la escala; sabemos qué datos la deciden"** ([`conclusiones_escala.md`](conclusiones_escala.md) §4).

---

## 3. Cinco preguntas para practicar

1. Si la red compra 7.500 kg/día y solo pechuga y milanesas, ¿qué pasa con la pata-muslo? *(Sobra: con el mix M3 quedan ~2 t/día de pata-muslo y ~6,7 t/día de partes en total sin comprador; §4 de escenarios.)*
2. ¿Qué es más barato para crecer 20 %: un sexto día de faena o una línea nueva? *(El sexto día, si hay personal, frío y pollitos para ese día.)*
3. ¿Por qué 20.000 aves/día a 8 h y 10.000 aves/día a 16 h usan la misma línea? *(Ambas necesitan 1.250 aves/h.)*
4. ¿Por qué no alcanza con decir "exportamos lo que sobra"? *(Un contenedor de garras tarda ~6 meses en llenarse a 2.500 aves/día, y sin planta habilitada ni comprador no hay exportación.)*
5. ¿Qué dato, si lo consiguiera mañana, más cambiaría la decisión de escala? *(Las compras reales de la red por producto y por semana, con precio y plazo: DPV-003 y DPV-037.)*
