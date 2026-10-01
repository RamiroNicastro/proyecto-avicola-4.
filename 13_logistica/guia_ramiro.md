# Guía para Ramiro — logística, explicada sin jerga

**Fecha:** 2026-10-01 · v1.1 · Sesión 12B · Para leer en 10 minutos. Los números son de **escenarios** (supuestos editables), no de datos de campo ni de normas.

---

## 1. Por qué logística no es solo "flete"

"Flete" es lo que se paga por mover un camión de A a B. La **logística** es todo lo que decide **cuántos** camiones, **cuándo**, **llenos o con poca carga**, **esperando o andando**, y **qué pasa si fallan**. En este proyecto se mueven cosas muy distintas:

- **Pollitos** recién nacidos que no aguantan frío ni calor.
- **Alimento**: el flujo más pesado de todo el sistema (35 t por día a 10.000 aves/día).
- **Aves vivas**, con un reloj de horas: entre el retiro del alimento y la faena pasan captura, carga, viaje y esperas.
- **Carne refrigerada**, con un reloj de días.
- **Carne congelada**, con un reloj de meses.
- **Subproductos** (plumas, sangre, vísceras) que se degradan en horas.

Cada uno tiene su vehículo, su temperatura, su habilitación y su frecuencia.

## 2. Por qué un camión con poca carga destruye eficiencia

Un camión cuesta casi lo mismo por día si va lleno o con poca carga: chofer, combustible, seguro, peajes, amortización. Si va al 25 %, **cada kilo cuesta cuatro veces más**.

Con los camiones que **supone** el modelo (no son camiones elegidos ni cotizados), a 2.500 aves/día:

- un camión de 5.500 aves va al **46 %**;
- el congelado despachado a diario usaría el **4 %** de un camión de 12 t;
- el retiro diario de plumas equivale al **6 % del peso** que admite un vehículo de 10 t. Ojo: las plumas son livianas y voluminosas, así que el **volumen** podría llenarse antes que el peso; eso todavía no está medido.

## 3. Qué es la densidad logística

Es **cuánta carga hay por parada, por kilómetro o por viaje**. Si cada local compra 25 kg por día y recibe 3 veces por semana, cada parada entrega **58 kg**; si compra 300 kg, **700 kg**. Estacionar, descargar y firmar tarda casi lo mismo en los dos casos: el segundo es **12 veces** más eficiente por kilo. En distribución, **las paradas pesan más que las toneladas**.

## 4. Qué es el backhaul (y por qué "volver sin carga" no es "volver vacío")

Hay tres formas de volver:

1. **Sin carga comercial**: no trae nada que se venda o que reemplace otro flete.
2. **Con envases**: trae jaulas, cajones, pallets o contenedores vacíos. **No está físicamente vacío**, pero tampoco genera ingreso.
3. **Backhaul comercial**: trae otra carga con valor (por ejemplo, insumos o carga de un tercero).

El modelo, por prudencia, **no aplica backhaul comercial en ningún flujo sin evidencia**. Para el camión de aves usa `BACKHAUL_AVES = false` como **supuesto conservador**: vuelve con sus jaulas, sin carga comercial. **No es que esté prohibido en todos los casos**; es que para usarlo en otra cosa habría que validar habilitación, lavado y desinfección (la Res. SENASA 723/2025 exige lavarlo y desinfectarlo a cada viaje), tiempos, tipo de vehículo y compatibilidad sanitaria.

## 5. Qué cambia entre vivo y refrigerado

| | Aves vivas | Producto refrigerado |
|---|---|---|
| Reloj | **Horas**: la ventana total entre retiro de alimento y faena (8–12 h citadas como práctica) incluye captura, carga, esperas y viaje | **Días** (vida útil) |
| Qué se cuida | Bienestar, calor, mortalidad, peso | Temperatura, higiene, vida útil remanente |
| Cuándo se mueve | De noche o madrugada, coordinado con la línea | Según ventanas de los clientes |
| Retorno | Con jaulas, sin carga comercial (supuesto) | Sin carga comercial o con pallets, salvo backhaul probado |
| Densidad | Baja: aves en jaulas | Alta: cajas y pallets |

**Cuánto tiempo queda para viajar:** con una ventana de 10 h y los tiempos supuestos (3 h desde el retiro de alimento, 1,5 h de captura y carga, 1 h de espera y descarga en planta) quedan **≈ 4,5 h** para el viaje; a 60 km/h son **≈ 270 km por ruta**. Eso **no es un límite legal ni el radio ideal**: si la captura se hace en 1 h o la espera en planta baja, el alcance sube; si la ventana real es 8 h, baja a ~150 km. Hay que medirlo con contratistas y frigoríficos.

## 6. Por qué una red de supermercados puede simplificar… o complicar

**Simplifica** si la red tiene **centro de distribución (CD)**: un camión lleno por día a un solo lugar.

**Complica** si hay que entregar en **cada local**. Con los supuestos del modelo (planta a 300 km, 0,75 h por parada, 12 h por camión, 100 kg por local), en una jornada solo caben ~2 paradas por camión y el reparto a 90 locales llega a **23 rutas y ~14.000 km por día**. Con la planta a 100 km, la diferencia con el CD es mucho menor. **No hay una distancia mágica**: depende de paradas, tiempos, kg por local y horas disponibles.

También puede **complicar el resto del negocio**: si la red compra sobre todo pechuga y pollo entero, el resto del ave necesita otros clientes. La red es un posible cliente ancla, **no el destino de toda la producción**.

## 7. Por qué un CD puede ser mejor que repartir tienda por tienda

| (Escenario: 90 locales, 100 kg, 300 km) | Tienda por tienda | Vía CD del cliente | Cross-dock propio/operador |
|---|---|---|---|
| Viajes desde la planta | 23 rutas chicas | 1 troncal lleno | 1 troncal + 7 rutas cortas |
| km por tonelada | ~1.350 | ~57 | ~125 |
| Camión-horas por día | ~270 | ~11 | ~87 |
| Riesgo de frío | Muchas aperturas | Pocas | Intermedio |
| Control de góndola | Alto | Menor | Medio |
| Costo extra | Flota de reparto | Fee del CD | Operador / cross-dock |

No hay ganador definido: falta saber si la red tiene CD, dónde, con qué horarios y qué cobra (DPV-036, DPV-039).

## 8. Granjas grandes y planta chica

Si una planta de 2.500 aves/día tuviera que retirar de una vez el lote de una granja de 30.000 aves, tardaría ~11 días de faena. Es una **incompatibilidad posible**, no un veredicto: se puede resolver con lotes más chicos, retiros parciales o programando varias granjas. Hay que preguntarlo a los productores.

## 9. Tres preguntas para las primeras reuniones

1. **A la red de supermercados:** ¿tienen CD que reciba perecederos refrigerados? ¿Dónde, en qué horario, con qué pedido mínimo y qué cobran?
2. **A contratistas de captura y transporte:** ¿cuántas aves de 2,9 kg llevan por camión en verano e invierno? ¿Cuánto tardan en capturar y cargar? ¿Cuánto esperan en planta? ¿Dónde lavan?
3. **A plantas de rendering:** ¿retiran todos los días? ¿Con qué vehículo y contenedor (m³)? ¿Aceptan plumas, sangre y vísceras juntas? ¿Aceptan material de 2 días? ¿Pagan o cobran?
