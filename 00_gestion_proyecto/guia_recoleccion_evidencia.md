# Guía de recolección de evidencia — qué tiene que aprender Ramiro antes de salir al campo

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Plan general: [`plan_trabajo_campo.md`](plan_trabajo_campo.md) · Matriz: [`matriz_validacion_campo.csv`](matriz_validacion_campo.csv)

> Leer antes de cualquier reunión, llamada o visita. Es corta a propósito. Las guías temáticas (`guia_ramiro.md` de cada carpeta) explican **el tema**; esta explica **cómo conseguir y registrar evidencia**.

---

## 1. Qué es validar una hipótesis

Una **hipótesis** es algo que creemos pero no sabemos: "la red compra mucho pollo", "hay productores dispuestos a integrarse", "el rendering nos retira las plumas gratis".

**Validar** es buscar a propósito la información que podría demostrar que la hipótesis es **falsa**, y ver si resiste. No es juntar opiniones a favor.

Tres reglas prácticas:

1. **Antes de la reunión, escribí qué respuesta te haría cambiar de idea.** Si ninguna respuesta posible cambiaría algo, la pregunta no sirve.
2. **Una hipótesis puede terminar validada, rechazada o sin resolver.** Las tres son resultados útiles. Un "no" temprano ahorra plata.
3. **Validar no es convencer.** Si terminás la reunión explicando por qué el proyecto es bueno, no validaste nada.

## 2. Dato, supuesto y evidencia

| Concepto | Qué es | Ejemplo | Cómo se registra |
|---|---|---|---|
| **Dato** | Un hecho con fuente identificable | "La red compró 12.400 kg de pollo en la semana 32 según su reporte de compras" | Con su fuente y la etiqueta `[VERIFICADO]` solo si se vio el documento original (reglas 4, 5 y 16 de `CLAUDE.md`) |
| **Estimación** | Un cálculo propio o del interlocutor a partir de datos | "El gerente estima unos 50 kg por local por día" | `[ESTIMACIÓN]`, indicando quién estimó y cómo |
| **Supuesto** | Una hipótesis de trabajo adoptada para poder avanzar | "Suponemos 2,9 kg de peso vivo" | `[SUPUESTO]` y en [`supuestos.md`](supuestos.md) |
| **Cotización** | Un precio ofrecido por un proveedor | "Tarifa de façon: $X por ave, sin frío, válida 30 días" | `[COTIZACIÓN]` con proveedor, fecha, validez, moneda y condiciones |
| **Evidencia** | El **documento o registro** que respalda un dato | El reporte de compras, la minuta firmada, la lista de precios, la foto de la góndola | Archivado en el data room con su código |

Una frase dicha en una reunión es un **dato del interlocutor**, no un dato verificado. Se anota tal cual, con quién lo dijo y con qué respaldo.

## 3. Qué vale más: opinión, cotización, carta de intención o contrato

De menor a mayor fuerza:

| Fuerza | Tipo | Qué prueba | Qué **no** prueba |
|---|---|---|---|
| 1 (muy débil) | **Opinión o entusiasmo** ("les va a encantar", "seguro compran") | Que alguien tiene buena disposición | Volumen, precio, fecha ni decisión |
| 2 | **Estimación verbal con números** ("compramos unos 300 kg por semana") | Orden de magnitud según esa persona | Que el número sea correcto |
| 3 | **Documento del interlocutor** (reporte de compras, lista de precios, factura) | Que el número existe en un sistema | Que vayan a comprarnos a nosotros |
| 4 | **Cotización escrita** (precio con condiciones y validez) | Precio y condiciones ofrecidas hoy | Que se mantenga al momento de invertir |
| 5 | **Prueba piloto ejecutada** con compras facturadas | Que el producto se vende y cómo | Volumen futuro a escala |
| 6 | **Carta de intención** con volumen, producto y precio de referencia | Intención formal de comprar | Obligación (normalmente no es vinculante) |
| 7 (más fuerte) | **Contrato u orden de compra** | Obligación de compra en las condiciones pactadas | Que el cliente no quiebre o no incumpla |

La escala comercial completa (E1 interés general → E6 contrato/orden) y su relación con las categorías de demanda A/B/C/D está en [`../02_clientes_demanda/plan_validacion_comercial.md` §2](../02_clientes_demanda/plan_validacion_comercial.md). **El interés verbal nunca es demanda asegurada.**

## 4. Cuándo algo está confirmado

- **Una fuente** = dato del interlocutor (`EN VALIDACIÓN` en la matriz).
- **Dos fuentes independientes que coinciden** (por ejemplo, dos mayoristas que no se conocen) = patrón razonable.
- **Documento original** (reporte, norma, factura, cotización) = evidencia; habilita `VALIDADO` solo si cumple la columna `EVIDENCIA_REQUERIDA` de la matriz.
- **Dos fuentes que se contradicen** = `CONTRADICTORIO`: se anotan ambas y se busca una tercera. No se promedia ni se elige la que conviene.

## 5. Cómo tomar notas en una reunión o visita

**Antes**
1. Identificar en la matriz qué DPV cubre ese actor y llevar el instrumento (cuestionario u hoja de visita).
2. Elegir las **5 preguntas imprescindibles**. Si la reunión se corta, que estén hechas.
3. Preparar la presentación de 30 segundos (sección 6) y la lista de documentos a pedir.

**Durante**
1. Pedir permiso para tomar notas; grabar audio **solo** con consentimiento explícito.
2. Anotar **números con unidad, base y fecha**: "kg de producto por semana, promedio de agosto", no "bastante".
3. Separar en la hoja lo que **dijo** el interlocutor de lo que **vos interpretás** (dos columnas, o comillas para lo textual).
4. Preguntar siempre: **"¿de dónde sale ese número?"** y **"¿me lo podría compartir por escrito?"**
5. Cerrar con: "¿a quién más me recomienda consultar?" y "¿puedo volver a escribirle si me queda una duda?"

**Después (dentro de las 24 h)**
1. Pasar las notas a la minuta u hoja de visita del tema.
2. Clasificar cada dato: `[VERIFICADO]` / `[ESTIMACIÓN]` / `[SUPUESTO]` / `[COTIZACIÓN]` (regla 4).
3. Guardar en el data room con el código `AAAA-MM-DD_actor_tema_tipo-documento` ([`estructura_data_room_campo.md`](estructura_data_room_campo.md)).
4. Actualizar la matriz (estado, fecha, resultado, fuente) y registrar la fuente en `25_fuentes/registro_fuentes.csv`.
5. Enviar un agradecimiento breve; si hubo pedidos, recordarlos por escrito.

## 6. Qué decir y qué no prometer

**Presentación estándar (30 segundos):**
> "Estamos estudiando la factibilidad de un proyecto avícola en Argentina. Todavía no hay decisión de inversión, ni escala, ni ubicación, ni proveedores elegidos. Queremos entender cómo funciona su parte de la cadena con datos reales. La información es confidencial y se usa solo para el estudio."

**No prometer ni dar a entender:**

| No decir | Por qué | Decir en cambio |
|---|---|---|
| "Vamos a comprarle / contratarlo" | No hay decisión de inversión ni proveedor elegido (fase 0) | "Estamos relevando; si el proyecto avanza, volveremos a consultar" |
| "Vamos a poner una planta de X aves/día" | La escala no está definida (regla 9) | "Estudiamos varios escenarios de escala" |
| "La planta va a estar en tal lugar" | No hay localización (DEC-003) | "Todavía no elegimos ubicación" |
| "Tenemos USD 2 millones" | El capital no está comprometido (SUP-003) | "Estamos en etapa de estudio" |
| "Los supermercados ya nos compran" | La demanda no está validada (regla 8) | "Estamos validando la demanda" |
| Precios o volúmenes propios | Anclan la negociación futura | Preguntar primero por los de ellos |
| Nombres o datos de otros entrevistados | Rompe la confianza y puede violar una confidencialidad | "Hablamos con varios actores del sector" |

Si alguien pide exclusividad, adelanto o compromiso: **no responder en el momento**; anotar el pedido y consultarlo.

## 7. Preguntas que sirven casi siempre

1. "¿Cómo lo hacen hoy?" (antes de "¿qué harían si…?").
2. "¿Cuánto, cada cuánto y a qué precio, en la última semana o el último mes?" (hechos recientes, no promedios de memoria).
3. "¿De dónde sale ese número? ¿Me lo puede compartir?"
4. "¿Cuál fue el peor mes o el peor lote, y por qué?"
5. "¿Qué problema tienen hoy con su proveedor o cliente actual?"
6. "¿Qué tendría que pasar para que cambien de proveedor?"
7. "¿Qué me estoy olvidando de preguntar?"
8. "¿Con quién más debería hablar?"

Evitar preguntas que inducen la respuesta ("¿no le parece que…?") y preguntas hipotéticas sin ancla ("¿compraría si…?"): la respuesta casi siempre es "sí" y no vale nada.

## 8. Por qué no adaptar los números para que el proyecto "dé bien"

- **El dinero es real y los números no.** Si se ajusta un precio, un volumen o un FCR para que el proyecto cierre, el error aparece después, cuando la planta está construida y el capital gastado.
- **Los inversores van a comparar con la realidad.** Una cifra acomodada que se descubre destruye la credibilidad de todo el estudio, incluso de lo que estaba bien.
- **Un "no da" temprano es un buen resultado.** Permite cambiar la escala, las etapas, el modelo de abastecimiento o el canal antes de invertir. Para eso existe la prefactibilidad (regla 10).
- **Cómo se ve la tentación:** usar el mejor precio escuchado, el menor FCR, el volumen del día de más ventas, la opinión del contacto más entusiasta, o descartar una respuesta negativa "porque esa persona no entiende".
- **Qué hacer en cambio:** registrar todas las respuestas, usar rangos (bajo / medio / alto), marcar lo débil como débil y dejar que el modelo muestre el resultado, sea el que sea.

## 9. Lista de control para cada contacto

- [ ] Sé qué DPV cubre este actor y qué evidencia necesito.
- [ ] Llevo el instrumento y la lista de documentos a pedir.
- [ ] Usé la presentación estándar y no prometí nada.
- [ ] Anoté números con unidad, base, fecha y fuente.
- [ ] Separé lo dicho de lo interpretado.
- [ ] Pedí el respaldo por escrito.
- [ ] Guardé la minuta en el data room con su código dentro de las 24 h.
- [ ] Actualicé la matriz y el registro de fuentes.
