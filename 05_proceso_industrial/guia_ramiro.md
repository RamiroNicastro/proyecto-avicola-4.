# Guía para Ramiro — cómo funciona una planta de faena y por qué la velocidad de la máquina no es la capacidad

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A)

> Explicación en lenguaje simple de los conceptos de esta etapa. Los detalles y números están en [`flujo_proceso.md`](flujo_proceso.md), [`cuellos_botella.md`](cuellos_botella.md) y [`arquitecturas_por_escala.md`](arquitecturas_por_escala.md). Ningún número de esta guía es un dato medido en una planta argentina: son cálculos y supuestos para entender órdenes de magnitud.

---

## 1. Qué es una línea de faena

Imaginá una **cinta colgante** (un riel con una cadena y ganchos llamados **grilletes**) que da vueltas por la planta sin parar. En un extremo, una persona cuelga cada pollo vivo de las patas. La cadena lo lleva, uno detrás de otro, por estaciones fijas: lo aturde (lo deja inconsciente), lo degüella, lo desangra, lo sumerge en agua caliente (escaldado) para aflojar las plumas, lo pasa por máquinas con dedos de goma que le sacan las plumas, le corta patas y cabeza. Después lo cuelga en **otra** cadena (la de evisceración), donde se lo abre, se le sacan las vísceras, lo revisa el veterinario de SENASA, se lava y entra al **chiller** para enfriarse.

Eso es la **línea**: una sucesión de puestos que trabajan todos **al mismo ritmo**, porque la cadena no espera. Después vienen las **salas** (clasificación, trozado, deshuese, envasado), las **cámaras de frío** y la **expedición**, que ya no dependen de la cadena pero sí de lo que ella entrega.

## 2. Qué significa "aves por hora"

Es la cantidad de pollos que pasan por la línea en una hora **mientras está funcionando**.

| Si la planta faena por día… | …y la línea trabaja 8 horas netas | …pasa por la línea |
|---|---|---|
| 2.500 aves | 312 aves/h | ~5 pollos por minuto (uno cada 11,5 segundos) |
| 5.000 | 625 aves/h | ~10 por minuto |
| 10.000 | 1.250 aves/h | ~21 por minuto (uno cada 3 segundos) |
| 20.000 | 2.500 aves/h | ~42 por minuto (casi uno por segundo y medio) |

**Horas netas** = horas en que realmente entran aves a la línea. No es lo mismo que el horario del turno (ver §5).

## 3. Qué es un cuello de botella

Una planta es como una cañería con tramos de distinto diámetro: **el agua sale al ritmo del tramo más angosto**, no del más ancho. Si la línea de faena puede procesar 2.500 aves/h pero la sala de trozado solo alcanza para 1.800 aves/h, la planta produce 1.800 (o se acumulan pollos que se echan a perder).

Posibles cuellos de botella: la gente que cuelga los pollos, la evisceración, cuántos pollos puede revisar el veterinario, el chiller (cada pollo tiene que estar ~50 minutos adentro), la sala de trozado o de deshuese, las máquinas de envasado, el túnel de congelado, el tamaño de las cámaras, los camiones y andenes de despacho, el agua, el tratamiento de efluentes, el frío, la mano de obra, las horas de limpieza y hasta el camión que retira las plumas: si no viene, no hay dónde ponerlas y la faena para.

**Regla:** capacidad de la planta = capacidad de su etapa más lenta.

## 4. Qué es la disponibilidad (y por qué la máquina nunca rinde lo que dice)

La **velocidad nominal** es lo que dice el folleto: "esta máquina procesa 2.500 aves/h". Pero en un día real:

- la línea para 15 minutos porque se trabó un grillete (**parada**);
- hay decenas de interrupciones de segundos que nadie anota (**microparadas**);
- algunos ganchos pasan vacíos porque el colgador no llegó (**pérdida de velocidad**);
- se para para cambiar el programa de corte o el tipo de bandeja (**cambio de producto**).

La **disponibilidad** es el porcentaje del tiempo en que la línea efectivamente anda. Sumando todo, una planta produce entre el 70 % y el 90 % de lo que diría la cuenta "velocidad × horas" (es un rango que usamos para pensar; el dato real hay que medirlo en plantas argentinas).

## 5. Horas de faena ≠ horas de la planta

Para faenar 8 horas, la planta trabaja muchas más: preparar y revisar todo antes de arrancar, pausas del personal, limpieza intermedia, vaciar la línea al terminar, y sobre todo **limpiar y desinfectar** todo (prelavado, espuma, enjuague, desinfección, inspección) y hacer **mantenimiento**. Con nuestros supuestos, 8 horas de faena ocupan **13 a 20 horas** del establecimiento.

Por eso "hago dos turnos y duplico la producción" es engañoso: dos turnos de 8 horas netas más la limpieza y el mantenimiento necesitan **22 a 29 horas**… y el día tiene 24.

## 6. Automatización

**Manual:** una persona con cuchillo eviscera unos 2 pollos por minuto (referencia de FAO, no argentina). **Semiautomático:** una máquina ayuda y la persona guía. **Automático:** la máquina lo hace sola y las personas controlan y reparan.

Automatizar **no siempre es mejor**:

| A favor | En contra |
|---|---|
| Menos gente por pollo | La máquina cuesta mucho y hay que usarla mucho para que se pague |
| Cortes más parejos | Si el lote tiene pollos de pesos muy distintos, la máquina funciona mal; la persona se adapta |
| Menos dependencia de conseguir personal | Si se rompe y el técnico está en otro país, se para todo |
| Más ritmo | Menos flexibilidad para cambiar de producto |

Hay operaciones que son automáticas en cualquier escala (aturdido, escaldado, desplumado, chiller), otras que siguen siendo manuales en casi todas las plantas (**colgar los pollos**, el trimming, la inspección veterinaria) y otras donde el salto depende de la escala: la **evisceración** manual deja de ser práctica por encima de ~1.000 aves/h, es decir, entre 5.000 y 10.000 aves/día.

## 7. Redundancia

Tener un **repuesto o una segunda unidad** para que una falla no pare la planta. Ejemplos: dos compresores de frío donde alcanzaría con uno; varias desplumadoras en fila (si una falla, las otras siguen, peor pero siguen); dos líneas de faena chicas en lugar de una grande (si una se rompe, la otra sigue al 50 %).

Clasificamos los equipos en tres grupos: **CRÍTICO** (si falla, se para la faena: la cadena, el aturdidor, la escaldadora, el chiller, el frío, la inspección), **IMPORTANTE** (si falla, se produce menos o peor, pero se puede seguir a mano) y **SECUNDARIO** (se arregla después). Detalle: [`../08_maquinaria/catalogo_equipos.md` §2](../08_maquinaria/catalogo_equipos.md).

**Ojo:** automatizar convierte tareas manuales (que "no se rompen") en equipos críticos (que sí).

## 8. Mantenimiento

Las máquinas de una planta de pollos trabajan mojadas, con grasa, sangre y lavados diarios con químicos. Se gastan cuchillas, dedos de goma, grilletes, rodamientos. El **mantenimiento preventivo** (cambiar piezas antes de que fallen) es más barato que la parada. Necesita: tiempo en el día (compite con la limpieza y con un eventual segundo turno), **repuestos en planta** (un repuesto importado que tarda semanas = semanas sin faena) y **técnicos** que conozcan el equipo.

## 9. Por qué comprar una línea de 2.500 aves/h no significa poder producir 20.000 aves/día

La cuenta ingenua es 2.500 aves/h × 8 h = 20.000 aves/día. Es falsa por cinco razones:

1. **La línea no rinde el 100 %:** con 80 % de eficiencia, 2.500 × 8 × 0,8 = **16.000 aves/día**. Para llegar a 20.000 con 8 horas netas habría que comprar una línea de ~2.800–3.600 aves/h nominales, o trabajar más horas netas.
2. **Las otras etapas tienen que acompañar:** evisceración, inspección, chiller, trozado, envasado, congelado, cámaras y despacho deben procesar lo mismo. Si una no llega, manda ella.
3. **Los servicios tienen que alcanzar:** agua, efluentes, frío, energía, vapor, aire comprimido.
4. **La gente tiene que alcanzar:** colgadores, evisceradores, operarios de sala, en cada turno.
5. **Tienen que llegar 20.000 pollos por día** (granjas, pollitos, camiones) **y alguien tiene que comprarlos** (hoy la demanda documentada es cero, [`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md)).

Y al revés: una línea de 2.500 aves/h puede servir para una planta de 10.000 aves/día con menos horas, o para crecer; pero eso depende de todo lo anterior, no de la línea.

## 10. Tres preguntas para hacer en cualquier visita a una planta o a un proveedor

1. "¿Cuántos pollos **realmente** faenan por día, y en cuántas horas netas?" (no la velocidad de la máquina).
2. "¿Qué es lo que más les frena la producción?" (su cuello de botella real).
3. "Si se rompe [la evisceradora / el chiller / el compresor], ¿quién viene a arreglarlo y en cuánto tiempo?"
