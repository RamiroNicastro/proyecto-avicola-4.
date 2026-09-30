# Guía para Ramiro — agua, efluentes, energía y frío

**Fecha:** 2026-09-30 · Sesión 09C · Lectura de 15 minutos. Los números son del escenario **medio** a **10.000 aves/día** salvo aclaración; vienen de [`modelo_utilities.py`](modelo_utilities.py) y son **órdenes de magnitud**, no datos medidos.

---

## 1. L/ave (litros por ave)

Cuántos litros de agua usa la planta por cada pollo faenado, sumando todo: escaldado, lavados, chiller, limpieza, vestuarios. Es el indicador que usan todas las plantas para compararse.

- Rango de referencia: **15–38 L/ave**; medio **25 L/ave**.
- Una planta eficiente usa menos de la mitad que una derrochadora con el **mismo pollo**: el agua depende más de la gestión que de la escala.

## 2. m³/día (metros cúbicos por día)

1 m³ = 1.000 litros. m³/día = L/ave × aves ÷ 1.000.

- 10.000 aves × 25 L = 250.000 L = **250 m³/día** (entre 150 y 380).
- Lo que importa para elegir un terreno no es solo el total diario sino **cuántos m³ por hora** entrega el pozo o la red: en pico, ~38 m³/h.
- **No confundir** con el agua que el pollo se lleva adentro del chiller (~0,09 kg/ave). Esa agua es **0,3 %** del consumo: nunca sirve para calcular cuánta agua necesita la planta.

## 3. Efluente

El agua sucia que sale de la planta: ~88 % del agua que entra (el resto se evapora o se va con el producto y los subproductos). Lleva sangre, grasa, restos de carne y vísceras, detergentes y desinfectantes. **No se puede tirar así**: hay que tratarla hasta cumplir los límites del lugar donde se vuelca (cloaca, arroyo, pluvial). A 10.000 aves/día: **~220 m³/día**.

## 4. DBO y DQO

Dos formas de medir **cuánta materia orgánica** (suciedad que se pudre) lleva el agua:

- **DBO** (demanda bioquímica de oxígeno): cuánto oxígeno consumen las bacterias para "comerse" la suciedad en 5 días. Mide lo biodegradable.
- **DQO** (demanda química de oxígeno): cuánto oxígeno hace falta para oxidar **toda** la materia orgánica con un químico fuerte. Siempre es mayor que la DBO (en faena, la DBO suele ser ~la mitad de la DQO).
- Se expresan en **mg/L** (concentración). Efluente crudo de faena: miles de mg/L (≈ 4.500 mg/L de DQO en el modelo). Un límite de vuelco a pluvial en la Provincia de Buenos Aires: **250 mg/L de DQO** y **50 mg/L de DBO** (a verificar). Hay que remover ~95 %.
- **La sangre es la peor**: ~375.000 mg/L de DQO. Por eso se junta aparte y nunca va al desagüe.

## 5. Carga orgánica

Concentración × caudal = **kilos de suciedad por día**. Es lo que dimensiona el tratamiento, más que los m³.

- 10.000 aves/día: **~1.000 kg de DQO/día** y **~500 kg de DBO/día** (medio). Es del orden de lo que genera una población de varios miles de personas.
- Si se perdiera toda la sangre recuperable al desagüe, la DQO subiría ~30 % (~300 kg/día más).
- Por eso **cada kg retirado en seco** (sangre, plumas, vísceras, cabezas: ~6 t/día) es tratamiento que no hay que pagar.

## 6. DAF

**Flotación por aire disuelto.** Un tanque donde se inyectan burbujas finísimas que "levantan" grasa y partículas a la superficie, donde se barren. Es el pretratamiento estándar de plantas cárnicas: saca buena parte de las grasas y sólidos (y algo de DBO), pero **no** lo disuelto (por ejemplo, la sangre). Genera un **lodo flotado** (~2,7 t/día húmedo a 10.000 aves/día) rico en grasa y proteína, que puede ir a rendering.

Después del DAF viene el tratamiento **biológico** (bacterias que se comen la materia orgánica): **anaeróbico** (sin aire; lagunas o reactores; poca energía, produce biogás, necesita pulido) o **aeróbico** (con aire; más energía y más lodo, mejor calidad de salida). Muchas plantas combinan los dos. **No se eligió ninguno.**

## 7. kW vs kWh

- **kW** = potencia = **cuán fuerte** se consume en un momento (como la velocidad de un auto). Define el tamaño de la conexión eléctrica, del transformador y del generador.
- **kWh** = energía = potencia × horas (como los kilómetros recorridos). Es lo que se factura.
- 10.000 aves/día: **~8.200 kWh por día de faena**, pero la potencia media es **~560 kW** y el pico **~820 kW**. A la distribuidora hay que pedirle **potencia** (~0,8 MW), y en el campo eso puede no estar disponible.
- Consumo por ave: **~0,8 kWh** (0,5–1,5).

## 8. Tonelada de refrigeración y kW frigorífico

- **kW frigorífico**: cuánto calor saca el sistema de frío por segundo. **No es** lo que consume de electricidad.
- **TR** (tonelada de refrigeración): unidad vieja, 1 TR = 3,517 kW frigoríficos (el frío de derretir una tonelada de hielo en un día).
- Relación: **kW eléctricos = kW frigoríficos ÷ COP**. El COP es ~3 para enfriar a 0 °C (3 kW de frío por cada kW eléctrico) y ~1,4 para congelar a −35 °C: **congelar cuesta el doble** por cada kW de frío.
- 10.000 aves/día: enfriar el producto fresco pide **~235 kW frigoríficos (~67 TR)** y consume ~78 kW eléctricos durante la faena.

## 9. Congelación vs almacenamiento

- **Congelación** = **túnel**: cuántas toneladas por día hay que llevar de +4 °C a −18 °C. Es potencia frigorífica grande y rápida.
- **Almacenamiento** = **cámara**: cuántas toneladas hay que **guardar** a la vez. Es volumen y aislamiento; mantiene, **no congela**.
- Ejemplo (10.000 aves/día con perfil exportador de prueba): congelar **12 t por día**, pero guardar **168 t** si se juntan 14 días de producción. Más días de stock = más cámara, **mismo túnel**.
- Y dos formas de contar días: **días de producción** (lo que sale en N días de faena) o **días calendario** (N días de ventas): con 250 días de faena al año, 14 días calendario son solo 68 % de 14 días de producción.

## 10. Por qué los servicios pueden limitar la capacidad de la planta

La capacidad real de la planta es la de su **eslabón más débil** ([`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md) §3). Una línea capaz de 1.250 aves/h no sirve si:

| Servicio | Cómo limita | Ejemplo (10.000 aves/día, medio) |
|---|---|---|
| **Agua** | El pozo o la red no entregan el caudal horario | Hacen falta ~38 m³/h en pico; si el pozo da 20 m³/h, no alcanza sin reserva |
| **Efluentes** | El permiso de vuelco fija un caudal o una carga máxima; el tratamiento tiene capacidad fija | 1.000 kg DQO/día; si la planta de tratamiento se diseñó para 5.000 aves, no se puede duplicar la faena |
| **Energía** | La distribuidora no puede dar más potencia | ~0,8 MW de pico; en zona rural puede requerir obra de línea |
| **Frío** | El chiller o los túneles no enfrían a tiempo; las cámaras se llenan | Si no se congela lo del día, la faena del día siguiente no tiene lugar |
| **Calor** | La caldera no da agua caliente para limpiar a tiempo | La limpieza pide ~320 kW térmicos en 4 h |
| **Lodos y subproductos** | Si nadie los retira, se acumulan | ~6 t/día de sólidos + ~2,4 t/día de lodos |

**Por eso los servicios son parte de la decisión de escala y de localización**, no un detalle de ingeniería posterior.

## 11. Qué no está hecho

No se eligió tecnología de tratamiento, refrigerante, fuente de calor ni generador; no hay costos; ningún número es de una planta argentina medida. Lo que hay que medir y cotizar: [`conclusiones_agua_efluentes.md` §6](conclusiones_agua_efluentes.md).
