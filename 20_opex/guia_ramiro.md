# Guía para Ramiro — costos de operar y capital de trabajo, sin tecnicismos

**Fecha:** 2026-10-02 · Sesión 17

## 1. CAPEX vs OPEX

- **CAPEX** es lo que se gasta **una vez** para tener el negocio: terreno, galpones, planta, cámaras, camiones. Es como comprar la carnicería con sus heladeras.
- **OPEX** es lo que cuesta **hacerlo funcionar todos los meses**: alimento, pollitos, sueldos, luz, gas, agua, envases, fletes, mantenimiento, seguros. Es como la carne que comprás, los sueldos y la luz de la carnicería.

El motor OPEX no mezcla los dos: una cámara de frío es CAPEX; la luz que consume y su mantenimiento son OPEX.

## 2. Costo fijo vs variable

- **Variable**: crece con cada pollo. Si faenás el doble, gastás el doble (alimento, pollitos, bandejas, químicos de limpieza).
- **Fijo**: lo pagás aunque produzcas poco (gerente, contador, seguros, cargo fijo de la luz).
- **Semifijo**: fijo hasta un escalón (una cuadrilla de faena cuesta lo mismo si faena 7.000 o 9.000 pollos en el turno; para 15.000 hace falta otra).

Esto importa porque cuando la planta arranca y produce poco, los fijos **no bajan**: cada pollo carga más costo fijo.

## 3. Por qué el alimento probablemente pesa mucho

Para que un pollo llegue a 2,9 kg se necesitan cerca de 4,9 kg de alimento por pollo faenado (escenario medio de 03). A 10.000 pollos por día son **unas 12.400 toneladas de alimento por año** (más de 1.000 t por mes). Cualquier diferencia de unos pocos dólares por tonelada se multiplica por miles. Por eso el precio del alimento (o del maíz y la soja si se fabrica) es el primer dato a conseguir. Hoy **no** está.

## 4. Por qué el costo por kilo puede bajar con la escala

Los costos fijos se reparten entre más pollos: el gerente, el sistema, la certificación o el laboratorio cuestan casi lo mismo a 5.000 que a 10.000 pollos por día. Pero **no todo baja**: el alimento y el pollito se pagan por unidad y siguen igual por pollo. Y una escala mayor puede pedir más turnos, más camiones o granjas más lejanas.

## 5. Por qué una planta barata puede ser cara de operar

Una planta más manual cuesta menos de construir pero necesita más gente por pollo; equipos más baratos pueden gastar más luz, romperse más y pedir más repuestos; una planta sin frío propio paga frío a terceros todos los meses. Lo que conviene se ve sumando inversión **y** operación durante años, en el modelo financiero. Hoy no se puede hacer porque faltan casi todos los precios.

## 6. Integrar vs comprar

Cada eslabón (pollito, alimento, granjas, faena, flete) se puede **hacer**, **comprar** o **tercerizar**. El motor calcula las tres formas con las mismas cantidades. Ejemplo con el alimento:

- **Comprarlo**: pagás alimento terminado por tonelada.
- **Façon**: comprás maíz y soja y pagás a una fábrica para que lo elabore.
- **Planta propia**: comprás maíz, soja y núcleo, y pagás luz, gas, gente y mantenimiento de tu fábrica (más la inversión).

Ninguna es mejor de antemano: depende de los precios reales, que hay que conseguir.

## 7. Capital de trabajo

Es la plata que queda **atrapada** en la operación: el alimento que está en los silos, los pollos que están creciendo en los galpones (unos 330.000 pollos a la vez a 10.000 por día), el producto en cámaras, lo que los clientes te deben y todavía no pagaron. Lo que vos le debés a tus proveedores te alivia.

```
capital de trabajo = stock propio + lo que te deben + caja de reserva − lo que debés
```

Solo cuenta el stock que **es tuyo**: el maíz que está en la fábrica del proveedor no es tuyo; el que compraste y dejaste en un acopio, sí.

## 8. Inventario, cuentas por cobrar y por pagar

- **Inventario**: mercadería tuya que todavía no vendiste (o insumos que todavía no usaste).
- **Cuentas por cobrar**: si un supermercado paga a 60 días, durante esos 60 días ya pagaste el pollito, el alimento y los sueldos, pero no cobraste. Cuanto más tarda en pagar, más plata necesitás.
- **Cuentas por pagar**: si al proveedor de alimento le pagás a 30 días, él te financia ese mes.

## 9. Vender mucho no es tener caja

Un supermercado grande puede comprar mucho y pagar a 60–90 días. Si crecés rápido, cada mes ponés más plata en pollitos, alimento y sueldos antes de cobrar. Muchas empresas que venden bien se quedan sin caja por eso. Por eso el capital de trabajo se calcula aparte y con cuidado.

## 10. Por qué un OPEX incompleto no debe generar EBITDA

Hoy el motor tiene precio para **1 o 2** de entre 61 y 210 conceptos según la configuración (el pollito comprado o el maíz, ambos con fuente débil). Si con eso se calculara una ganancia (EBITDA), saldría enorme y falsa, porque faltarían el alimento, los sueldos, la luz y casi todo lo demás. El motor muestra "NO DISPONIBLE" hasta tener los precios, y separa los montos por calidad de la fuente.

## 11. Qué sí se puede usar hoy

- **Cuánto se necesita** de cada cosa por escala: toneladas de alimento, pollitos, kWh, m³ de agua, km de camión, personas (en FTE), envases por kg.
- **Qué precios conseguir primero**: [`matriz_validacion_opex.csv`](matriz_validacion_opex.csv).
- **Dónde hay riesgos de contar dos veces** algo (frío y luz, choferes y flete, personal del faenador y tarifa de façon).
