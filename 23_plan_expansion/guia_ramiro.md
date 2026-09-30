# Guía para Ramiro — escala, capacidad y crecimiento por etapas

**Fecha:** 2026-09-30 · Lectura de 10 minutos. Cifras de [`escenarios_escala.md`](escenarios_escala.md) (escenario medio: pollo de 2,9 kg, 5 días de faena por semana).

El objetivo es poder responder **"¿por qué no construir directamente una planta de 20.000 pollos por día?"** con argumentos propios, no con "porque lo dijo el modelo".

---

## 1. Doce conceptos

**1. Capacidad nominal.** Lo que la planta podría hacer "en los papeles": velocidad de la línea × horas. Como la velocidad máxima de un auto: existe, pero no se maneja siempre así.

**2. Capacidad operativa, utilización, factor demanda/capacidad y cobertura.** La operativa es lo que la planta puede sostener día tras día con su gente, su frío, sus efluentes y sus pollos disponibles. Tres números distintos que **no hay que confundir**:
- **Utilización** = lo que efectivamente se faena ÷ capacidad. Va de 0 a 100 %, **nunca más**: una planta de 10.000 que faena 5.000 está al 50 %; si le piden 14.000, sigue al 100 %.
- **Factor demanda/capacidad** = lo que pide la demanda ÷ capacidad. Sí puede pasar de 100 %: 143 % quiere decir que la planta no alcanza y queda **demanda sin atender**; 46 % quiere decir que sobra **capacidad ociosa**.
- **Cobertura** = lo que la planta puede producir ÷ lo que pide la demanda, hasta 100 %. Con factor 143 %, la cobertura es 70 %: se atiende el 70 % y el 30 % queda afuera.

**Capacidad no es ventas**: la planta puede faenar; vender depende de clientes.

**3. Cuello de botella.** La operación más lenta fija la capacidad de todo. Si la línea faena 1.250 pollos por hora pero la sala de deshuese solo procesa el equivalente a 800, la planta "es" de 800 para ese producto. Puede estar en la línea, en el enfriado, en el deshuese, en el túnel de congelado, en las cámaras, en el tratamiento de efluentes o… en la falta de pollos.

**4. Modularidad.** Diseñar para poder **agregar piezas** sin romper lo que funciona: dejar terreno, lugar para otra línea, potencia eléctrica reservada, espacio para más cámaras. Se prevé lo que es barato de prever y caro de corregir (terreno, caminos, permisos, flujos higiénicos); se construye por partes lo que es caro de tener parado (líneas, cámaras, salas de corte).

**5. Sobredimensionamiento.** Construir más capacidad de la que se va a usar. A 20.000 aves/día con la demanda del escenario base, la **utilización** sería del **23–41 %**: tres cuartos de lo construido sin uso.

**6. Subdimensionamiento.** Construir menos de lo necesario, o sin posibilidad de crecer. Riesgos: clientes que no se pueden atender, costo por pollo alto, y una planta que hay que abandonar o duplicar mal si la demanda crece. **Arrancar chico no es arrancar sin prever el crecimiento.**

**7. Escala mínima (eficiente).** El tamaño por debajo del cual el costo por pollo es demasiado alto porque lo fijo (edificio, frío, habilitaciones, personal mínimo, tratamiento de efluentes) se reparte entre pocos pollos. **No la conocemos todavía** y **no se puede concluir** que 2.500 sea demasiado chico ni que 20.000 sea demasiado grande: saldrá después de estudiar maquinaria, turnos, dotación, CAPEX, OPEX, servicios y utilización. Por ahora: se calcula con CAPEX y OPEX. Por eso no se puede afirmar que 2.500 aves/día sea viable solo porque se llena más fácil.

**8. Economías de escala.** A más volumen, algunos costos por unidad bajan (lo fijo se reparte; se compra mejor; se llenan contenedores). Pero **solo si la planta está llena**. Una planta grande vacía tiene **deseconomías**: todo lo fijo sobre pocos pollos.

**9. Riesgo de demanda.** El riesgo de producir sin comprador. Hoy la demanda documentada es **prácticamente cero**: los 90 supermercados son potenciales, los escenarios comerciales son hipótesis y la exportación no tiene ni un importador identificado. Además, no alcanza con que compren "kilos": tienen que comprar **todas las partes** del pollo o hay que encontrar a quién venderle el resto.

**10. Expansión por etapas.** Crecer de a pasos, cada uno habilitado por **métricas verificables** (contratos, planta llena con clientes reales, pollitos y productores asegurados, salida para subproductos), no por entusiasmo. Dos palancas que **no** son lo mismo: el **sexto día** de faena (250 → 300 días/año) da ~20 % más de **volumen anual** con la **misma capacidad por día**; el **segundo turno** puede hasta duplicar la **capacidad teórica de la línea** por día, pero solo si el resto de la planta acompaña (frío, congelado, efluentes, agua, energía, personal, limpieza, mantenimiento, bienestar animal, pollos). Ninguna de las dos es "crecer sin obra" hasta estudiarlo.

**11. Día de faena vs día calendario.** La planta produce en **días de faena** (250 o 300 por año); la gente come y los supermercados venden todos los **días del calendario** (365). A 10.000 aves/día y 250 días, salen 24 t de producto por día de faena, pero en promedio son 16,4 t por día calendario. **La demanda se compara con la producción en la misma base**, siempre convirtiendo (× 250 / 365). Lo mismo con el stock: 7 días de faena en cámara (168 t) no son 7 días calendario de ventas (115 t).

**12. Carne no es lo mismo que peso vendido.** El pollo enfriado en agua absorbe un poco: de las 24 t/día que se venden a 10.000 aves/día, ~23,1 t son carne y tejidos (**masa biológica**) y ~0,9 t son **agua retenida**. Se vende el **peso comercial** (las dos cosas juntas), pero el agua **nunca** es carne producida.

---

## 2. ¿Por qué no construir directamente una planta de 20.000 pollos por día?

No es "porque lo dijo el modelo". Es porque **tiene que ser verdad todo esto a la vez**, y hoy **nada** de esto está demostrado:

| Para operar 20.000 pollos/día tiene que ser verdad que… | Cuánto es | Qué sabemos hoy |
|---|---|---|
| Alguien compra el producto | ~33 t/día calendario de producto (vendiendo **todo** el pollo); ~365 kg de pollo por local por día si todo pasara por los 90 supermercados | La red, si comprara todo su pollo a 150 kg/local, más otros canales desarrollados, es el **escenario expansivo** (23,5 t/día): **utilización 72 %** (28 % de capacidad ociosa). La demanda documentada es ~0 |
| Alguien compra **cada parte** | Con un mix de supermercado sobran hasta ~12 t/día de pata-muslo, alas, carcasa, cuello, garras aun con la planta llena | No hay compradores identificados para esas partes |
| Hay pollitos | ~105.600 pollitos BB **por semana** | Sin contratos ni proveedores relevados |
| Hay dónde criarlos | ~76.000 m² de galpones (~32 galpones de 2.400 m²), ~964.000 plazas, 8 a 32 productores | Sin productores relevados en ninguna zona |
| Hay alimento | ~494 t por semana; ~24.700 t por año | Sin estrategia de alimento |
| Hay a quién darle los subproductos todos los días | ~11–17 t/día (plumas, sangre, vísceras, cabezas…), más ~8 t/día de carcasa | Sin receptores identificados |
| Hay frío y logística | 336 t en 7 días de **producción** en stock (230 t si se cuentan 7 días **calendario** de ventas); ~58 t de pollo vivo entrando por día | No diseñado |
| Hay capital | CAPEX y capital de trabajo **no calculados** | USD 2 M es solo una referencia, no comprometida |

**Y si se construye grande y la demanda no llega:** una planta de 20.000 al 50 % faena lo mismo que una de 10.000 llena, pero paga (en capital, energía, mantenimiento, personal mínimo, habilitaciones) como una de 20.000. La tentación de "llenarla" lleva a vender barato o a clientes que desbalancean el pollo.

**Lo que sí conviene hacer si se aspira a 20.000:** elegir un terreno y servicios que **permitan** llegar (y no se puedan perder después), diseñar el edificio y los flujos para crecer, y ampliar cuando las métricas lo pidan ([`gates_expansion.md`](gates_expansion.md)). La aspiración define la **reserva**; la evidencia define la **construcción**.

**El argumento también vale al revés:** tampoco es obvio que haya que empezar con 2.500. Con el escenario base no alcanzaría (factor demanda/capacidad 183 %: quedarían 3,4 t/día sin atender), no sabemos si está por encima o por debajo de la escala mínima eficiente, y podría no poder crecer si no se prevé. Por eso la respuesta honesta hoy es: **"no sabemos todavía cuál es la escala; sabemos qué datos la deciden"** ([`conclusiones_escala.md`](conclusiones_escala.md) §4).

---

## 3. Seis preguntas para practicar

1. Si la red compra 7.500 kg/día con un mix cargado de pechuga y milanesas (M3), ¿qué pasa con la pata-muslo? *(Sobra: con el mix M3 quedan ~2 t/día de pata-muslo y ~6,7 t/día de partes en total sin comprador; §4 de escenarios.)*
2. ¿Un sexto día de faena aumenta 20 % la capacidad por día? *(No: aumenta ~20 % el volumen **anual** con la misma capacidad diaria, y solo si hay personal, frío y pollitos para ese día.)*
3. ¿Por qué 10.000 aves/día con 8 h netas y 20.000 con 16 h netas piden la misma línea, y por qué eso no alcanza para decir que la planta llega a 20.000? *(Ambas necesitan 1.250 aves/h; pero el segundo turno también necesita frío, efluentes, agua, energía, personal, limpieza y pollos para el doble: es capacidad teórica de la línea, no de la planta.)*
4. ¿Por qué no alcanza con decir "exportamos lo que sobra"? *(Un contenedor de garras tarda ~6 meses en llenarse a 2.500 aves/día, y sin planta habilitada ni comprador no hay exportación.)*
5. Si el factor demanda/capacidad da 143 %, ¿a qué utilización trabaja la planta? *(100 %; el 30 % de la demanda queda sin atender: cobertura 70 %.)*
6. ¿Qué dato, si lo consiguiera mañana, más cambiaría la decisión de escala? *(Las compras reales de la red por producto y por semana, con precio y plazo: DPV-003 y DPV-037.)*
