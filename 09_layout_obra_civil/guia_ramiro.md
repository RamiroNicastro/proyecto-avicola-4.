# Guía para Ramiro — layout y obra civil explicados sin jerga

**Fecha:** 2026-10-01 · Sesión 12C · Para leer antes de hablar con arquitectos, proveedores, municipios o dueños de terrenos.

---

## 1. Layout

Es **cómo se ordenan las salas y los caminos** dentro de la planta y del terreno. No es el dibujo lindo del edificio: es la respuesta a "¿por dónde entra el pollo vivo, por dónde sale el producto, por dónde salen las plumas y por dónde camina la gente?". Un buen layout se puede dibujar con cajas y flechas; si las flechas se cruzan donde no deben, el layout está mal aunque el edificio sea hermoso.

## 2. Flujo

Es el **camino** que recorre algo: el ave, el producto, el personal, los subproductos, los residuos, los envases, los camiones, el agua. En una planta de faena hay **nueve flujos** ([`flujos_layout.md`](flujos_layout.md)) y la regla de oro es que **lo sucio nunca cruce lo limpio**. El pollo avanza siempre hacia adelante, de lo más sucio (pluma, sangre) a lo más limpio (producto envasado y frío), y nunca vuelve.

## 3. Zoning (zonificación)

Es **dividir la planta en zonas** según qué tan limpias tienen que estar, y poner **barreras** entre ellas (paredes, cambio de ropa, lavamanos). En este estudio usamos nueve zonas: sucia, de transición, limpia, fría, de despacho, de subproductos, de utilities, de personal y administrativa ([`zonificacion_layout.md`](zonificacion_layout.md)). **Ojo:** esos nombres son nuestros; SENASA puede usar otros. Lo que sí exige (en lo que pudimos ver en extractos) es separar físicamente la parte con plumas de la parte donde se abre el pollo, y que los caminos no se crucen.

Un ejemplo concreto: el operario que cuelga pollos vivos **no puede** entrar a la sala de trozado con la misma ropa. Necesita ir a su vestuario, y la sala de trozado tiene **otro** vestuario. Eso, que parece un detalle de procedimiento, define dónde van los vestuarios, los pasillos y las puertas de todo el edificio.

## 4. Buffer

Es un **espacio de amortiguación**. Hay de dos tipos:

- **Buffer de proceso:** un lugar donde se acumula algo para que el resto no se frene. Ejemplo: el andén donde esperan los camiones de pollo vivo; la cámara donde espera el producto antes de cargarse. Si no existe, cualquier demora en un punto para toda la planta.
- **Buffer de terreno:** una franja libre alrededor de la planta (o entre zonas) por bioseguridad, olores, ruido o vecinos. No produce nada, pero sin ella el municipio puede no habilitar o los vecinos pueden hacer cerrar.

## 5. Footprint (huella)

Es la **superficie que ocupa una máquina apoyada en el piso**. Una desplumadora puede ocupar, digamos, unos metros cuadrados; pero la sala que la contiene es mucho más grande, porque hay que **caminar alrededor, desarmarla para limpiarla, sacar una pieza para repararla** y dejar pasar carros. Por eso en el modelo la sala es "huella × factor de envolvente" (entre 2,2 y 3,5 veces, un supuesto).

**Hoy no tenemos ninguna huella real**: dependen del proveedor y del modelo de máquina. Por eso las superficies de proceso son estimaciones de orden de magnitud (estado PROXY) y el modelo lo avisa con una alerta. Cuando lleguen los layouts de proveedores, se cargan y la estimación mejora sola. Lo que **no** hacemos es poner "cero" donde no sabemos: un dato que falta no es un dato que vale cero.

## 6. Por qué m² de edificio no es lo mismo que m² de terreno

Para 10.000 aves/día el modelo da, en el escenario medio, ~**4.300 m² construidos**, pero ~**3,1 hectáreas (31.000 m²) de terreno**. ¿Por qué siete veces más?

| Concepto | m² aprox. (medio, 10.000 aves/día) |
|---|---|
| Edificio (proceso, frío, servicios, personal) | 4.300 |
| Playas de camiones, lavado, caminos internos, estacionamiento, tanques | 3.900 |
| Tratamiento de efluentes (reserva anaerobio + aerobio) | 300 |
| Reserva para crecer y para un rendering futuro | 4.600 |
| Retiros municipales y franja de buffer alrededor | 17.600 |
| **Terreno** | **~31.000** |

Los camiones no giran en una baldosa, el municipio exige retiros, los vecinos necesitan distancia y el futuro necesita lugar. Con lagunas para el efluente, el terreno puede duplicarse. Y estas cifras tienen un rango enorme (1,2 a 8,7 ha) porque retiros, buffers y reserva son datos del sitio que todavía no existen. **Al mirar un terreno, la pregunta no es "¿entra el galpón?", sino "¿entra todo lo de la tabla, para la escala final?"**

## 7. Por qué agregar una máquina después puede requerir romper media planta

Porque una máquina no es solo una máquina:

1. **Tiene que entrar:** si no se dejó un portón o un panel desmontable del tamaño del bulto más grande, hay que romper una pared.
2. **Tiene que apoyarse:** un chiller o un túnel lleno pesa mucho; si la losa no estaba preparada, hay que romper el piso.
3. **Tiene que conectarse:** agua, vapor, aire, frío y electricidad. Si las cañerías principales no tenían "salidas de reserva", hay que cortar servicios de toda la planta.
4. **Tiene que lavarse:** necesita desagüe con la pendiente correcta. Mover un desagüe en una sala limpia es romper el piso de la sala limpia.
5. **Tiene que ir en su lugar del flujo:** si la única ubicación posible está en medio del recorrido del pollo (por ejemplo, entre la evisceración y el chiller), hay que **parar la producción** y romper la barrera sanitaria. Y eso puede exigir volver a presentar planos a SENASA.

Por eso el principio aprobado es **anticipar lo barato de prever y caro de corregir** (terreno, accesos, desagües, cañerías principales, espacio al costado de cada zona) y **comprar por módulos lo caro de tener parado** (máquinas, cámaras, túneles).

## 8. Expansión modular

Es diseñar la planta como un conjunto de **bloques que se agregan** sin desarmar los existentes: una segunda línea al lado de la primera, más cámaras al costado de las cámaras, más docks a lo largo de la fachada, otro módulo de tratamiento de efluentes. La regla del layout es **crecer a lo ancho, nunca intercalar**: una sala nueva no puede quedar en el medio de la secuencia sucia → limpia → fría ([`estrategia_expansion.md`](estrategia_expansion.md)).

## 9. Planificar la expansión no significa construir todo hoy

El modelo muestra algo útil: si la meta final fueran 20.000 aves/día, **el terreno necesario es el mismo (~3,3 ha medio) arrancando con 2.500, con 5.000 o con 10.000**. Lo que cambia es cuánto se construye en cada etapa: ~1.800 m² en la primera etapa de la trayectoria chica contra ~7.500 m² al final.

Es decir:

- **Hoy** se decide (y se paga) el **terreno**, la **traza** de accesos y caminos, los **desagües y cañerías principales**, la **dirección del flujo** y **dónde va a crecer** cada zona.
- **Después**, y solo si la demanda lo justifica (los gates de [`../23_plan_expansion/gates_expansion.md`](../23_plan_expansion/gates_expansion.md)), se construyen las salas, se compran las máquinas y se agregan cámaras.

Construir hoy el edificio de 20.000 para operar 2.500 inmovilizaría ~4 veces más obra que la necesaria. Comprar hoy un terreno que solo sirve para 2.500 pone un techo que después no se puede romper.

## 10. Qué preguntar (y qué no prometer)

- **A un dueño de terreno o al municipio:** superficie útil, retiros, FOS (cuánto del lote se puede edificar), distancia a viviendas, si admite frigorífico y tratamiento de efluentes, por dónde se vuelca el efluente, si hay potencia eléctrica y gas, si el lote se inunda ([`../10_localizacion/ficha_relevamiento_terreno.md`](../10_localizacion/ficha_relevamiento_terreno.md)).
- **A un proveedor de equipos:** el **layout con cotas** de lo que ofrece, la huella, la altura libre, el peso, los fosos, el tamaño del bulto más grande para montaje y cómo se amplía después.
- **En una visita a una planta:** cuántos m² cubiertos tiene, cuántas aves faena, cuánta gente trabaja por turno, qué haría distinto si la construyera de nuevo.
- **No prometer:** ninguna superficie de este estudio es un plano ni un presupuesto. Son rangos para saber **qué tamaño de terreno buscar** y **qué preguntar**.
