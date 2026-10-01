# Guía para Ramiro — logística, explicada sin jerga

**Fecha:** 2026-10-01 · Sesión 12B · Para leer en 10 minutos. Los números son de escenarios, no de datos de campo.

---

## 1. Por qué logística no es solo "flete"

"Flete" es lo que se paga por mover un camión de A a B. La **logística** es todo lo que decide **cuántos** camiones, **cuándo**, **llenos o vacíos**, **esperando o andando**, y **qué pasa si fallan**. En este proyecto se mueven cosas muy distintas:

- **Pollitos** recién nacidos que no aguantan frío ni calor.
- **Alimento**: el flujo más pesado de todo el sistema (35 t por día a 10.000 aves/día).
- **Aves vivas**, que tienen un reloj de horas: el ayuno, el calor y el bienestar animal ponen el límite.
- **Carne refrigerada**, con un reloj de días.
- **Carne congelada**, con un reloj de meses.
- **Subproductos** (plumas, sangre, vísceras) que se pudren en horas y casi no valen nada.

Cada uno tiene su vehículo, su temperatura, su habilitación SENASA y su frecuencia. Pensar la logística solo como "cuánto cuesta el flete" es como pensar una planta solo por el precio de la máquina.

## 2. Por qué un camión vacío destruye eficiencia

Un camión cuesta casi lo mismo por día si va lleno o vacío: chofer, combustible, seguro, peajes, amortización. Si va al 25 %, **cada kilo cuesta cuatro veces más**.

El modelo muestra que, a 2.500 aves/día, eso pasa en casi todos los flujos:

- el camión de aves vivas va al **46 %**;
- el congelado despachado a diario iría al **4 %** de un camión de 12 t;
- el retiro diario de plumas ocupa el **6 %** de un vehículo de 10 t.

Y hay vacíos que no se pueden evitar: el camión de aves **vuelve vacío siempre** (por bioseguridad no puede traer otra cosa), así que la mitad de sus kilómetros son vacíos por diseño.

## 3. Qué es la densidad logística

Es **cuánta carga hay por parada, por kilómetro o por viaje**. Con alta densidad, cada parada entrega mucho y el camión trabaja lleno. Con baja densidad, el camión hace muchas paradas chicas.

Ejemplo de la red de supermercados: si cada local compra 25 kg por día y recibe 3 veces por semana, cada parada entrega **58 kg**. Si compra 300 kg, cada parada entrega **700 kg**. El camión tarda casi lo mismo en estacionar, descargar y firmar en los dos casos: el segundo es **12 veces** más eficiente por kilo. Por eso, en distribución, **las paradas pesan más que las toneladas**.

## 4. Qué es el backhaul

Es **volver con carga** en lugar de volver vacío. Ejemplo: un camión que lleva pollo al AMBA y vuelve con cajas, envases o carga refrigerada de otra empresa.

Suena bien, pero en este negocio tiene límites duros:
- El camión de aves vivas **no puede** (bioseguridad; lavado obligatorio antes de cargar animales).
- El de subproductos **no puede** llevar alimentos.
- El refrigerado **podría**, pero solo si existe esa carga, en ese horario, compatible con la temperatura y la habilitación del vehículo.

Por eso el modelo tiene un campo `BACKHAUL_POSIBLE` y **no aplica ningún backhaul sin evidencia** (un contrato o una carga concreta).

## 5. Qué cambia entre vivo y refrigerado

| | Aves vivas | Producto refrigerado |
|---|---|---|
| Reloj | **Horas** (ayuno total 8–12 h) | **Días** (vida útil) |
| Qué se cuida | Bienestar, calor, mortalidad, peso | Temperatura, higiene, vida útil remanente |
| Cuándo se mueve | De noche o madrugada, coordinado con la línea | Según ventanas de los clientes |
| Retorno | Vacío y a lavar | Vacío, salvo backhaul probado |
| Densidad | Baja: aves en jaulas | Alta: cajas y pallets |
| Distancia razonable | Corta: con los supuestos, más de ~200 km de ruta compromete el ayuno | Larga: cientos de km |

Conclusión sectorial (no de este proyecto todavía): **la planta va cerca de las granjas y la carne viaja al mercado**. Dónde, lo estudia 12A.

## 6. Por qué una red de supermercados puede simplificar… o complicar

**Simplifica** si la red tiene **centro de distribución (CD)**: un camión lleno por día a un solo lugar. A 300 km del AMBA eso son ~600 km/día.

**Complica** si hay que entregar en **cada local**: con la planta a 300 km, en una jornada solo caben ~2 paradas por camión, y el reparto a 90 locales llega a **23 rutas y ~14.000 km por día**. Es otra empresa, de distribución urbana.

También puede **complicar el resto del negocio**: si la red compra sobre todo pechuga y pollo entero, el resto del ave (pata-muslo, alas, carcasa, menudencias) necesita otros clientes. Y si la red se va, se va el canal. Por eso la red se trata como posible cliente ancla, **no como el destino de toda la producción**.

## 7. Por qué un CD puede ser mejor que repartir tienda por tienda

| | Tienda por tienda | Vía CD (del cliente o un cross-dock) |
|---|---|---|
| Viajes desde la planta | Muchos y chicos | Uno o dos, llenos |
| km por tonelada (C, 300 km) | ~1.350 | ~57 (CD) / ~125 (cross-dock) |
| Choferes y horas | ~270 camión-horas por día | ~11 (CD) / ~87 (cross-dock) |
| Riesgo de frío | Muchas aperturas de puerta | Pocas |
| Control de góndola | Alto | Menor |
| Costo extra | Flota de reparto | Fee del CD o del operador |

La decisión depende de datos que todavía no tenemos: si la red tiene CD, dónde, con qué horarios y qué cobra (DPV-036, DPV-039).

## 8. Tres preguntas para las primeras reuniones

1. **A la red de supermercados:** ¿tienen CD que reciba perecederos refrigerados? ¿Dónde, en qué horario, con qué pedido mínimo y qué cobran por recibir?
2. **A contratistas de captura y transporte:** ¿cuántas aves por camión llevan con aves de 2,9 kg, en verano e invierno? ¿Cuánto tardan en cargar? ¿Dónde lavan?
3. **A plantas de rendering de la zona:** ¿retiran todos los días? ¿Con qué vehículo? ¿Aceptan sangre, plumas y vísceras juntas? ¿Pagan o cobran?
