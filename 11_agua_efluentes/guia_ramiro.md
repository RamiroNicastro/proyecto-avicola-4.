# Guía para Ramiro — agua, efluentes, energía y frío

**Fecha:** 2026-09-30 · Sesión 09C (v1.1, auditoría conceptual) · Lectura de 15 minutos. Los números son del escenario **medio** a **10.000 aves/día** salvo aclaración; vienen de [`modelo_utilities.py`](modelo_utilities.py) y son **rangos de sensibilidad**, no consumos esperados ni especificaciones de diseño.

---

## 1. L/ave (litros por ave)

Cuántos litros de agua usa la planta por cada pollo faenado, sumando todo: escaldado, lavados, chiller, limpieza, vestuarios.

- Rango de sensibilidad: **15–38 L/ave**; medio **25 L/ave**. **No es lo que va a consumir nuestra planta**: es el rango dentro del cual hay que preguntar y medir.
- Una planta eficiente usa menos de la mitad que una derrochadora con el **mismo pollo**.
- Segunda forma de decirlo: **m³ por tonelada de producto** (6–16 m³/t). Sirve para comparar plantas con pollos de distinto peso y detectar datos raros.

## 2. m³/día y las cinco aguas

1 m³ = 1.000 litros. m³/día = L/ave × aves ÷ 1.000 → 10.000 × 25 L = **250 m³/día** (150–380).

No es una sola agua:

| Agua | Qué es | Ejemplo |
|---|---|---|
| **Captada** | Lo que sale del pozo o se compra | 250 m³/día (más si hay que potabilizar con rechazo) |
| **Utilizada** | Lo que usan las operaciones | 250 m³/día |
| **Incorporada** | Lo que se lleva el pollo adentro (chiller) y las plumas | ~2 t/día (0,3 % queda en el producto) |
| **Evaporada o arrastrada** | Vapor del escaldador, caldera, lo que sale con lodos | ~28 m³/día |
| **Descargada (efluente)** | Lo que va al desagüe | ~220 m³/día **si** se descarga el 88 % (supuesto) |

El agua que el pollo se lleva nunca sirve para calcular cuánta agua necesita la planta. Y **cuánto de lo usado termina en el desagüe no es un número fijo**: depende de cómo se opere.

## 3. Efluente

El agua sucia que sale de la planta: lleva sangre, grasa, restos de carne y vísceras, detergentes y desinfectantes. Hay que tratarla hasta cumplir el límite **del lugar** donde se vuelca (cloaca, arroyo, pluvial).

## 4. DBO y DQO

Dos formas de medir **cuánta materia orgánica** lleva el agua:

- **DBO**: oxígeno que consumen las bacterias para "comerse" lo biodegradable en 5 días.
- **DQO**: oxígeno para oxidar químicamente **toda** la materia orgánica. Siempre ≥ DBO.
- Se miden en **mg/L**. Efluente crudo de faena: miles de mg/L.
- **Ejemplo** (no requisito): la Provincia de Buenos Aires admite 250 mg/L de DQO a un conducto pluvial (Res. ADA 336/03, a verificar). **Bajo ese ejemplo**, el escenario medio exigiría remover ~95 %. Nuestro límite real dependerá de la provincia, la autoridad del agua, dónde se vuelque y el permiso: lo fijará la localización.
- **La sangre es la peor**: ~375.000 mg/L de DQO. Por eso se junta aparte.

## 5. Carga orgánica — dos maneras de calcularla

Carga = **kilos de suciedad por día**. Es lo que dimensiona el tratamiento, más que los m³.

- **Método A:** gramos por ave × aves. 100 g DQO/ave × 10.000 = **1.000 kg DQO/día**.
- **Método B:** m³ de efluente × concentración. 220 m³ × 5.400 mg/L = **~1.200 kg DQO/día**.
- Si dan parecido (medio), vamos bien en el orden de magnitud. Si difieren más del doble (pasa en los extremos), el modelo avisa: **"DATOS DE EFLUENTE REQUIEREN VALIDACIÓN DE CAMPO"**. No se "ajusta" uno para que coincida con el otro: se mide.
- **Sangre:** si la sangre recuperada fuera al desagüe, la DQO podría subir del orden de un tercio (~300 kg/día). Es una **referencia para entender la sensibilidad**, no un resultado de nuestra planta: se valida midiendo DQO antes y después, o la sangre recuperada por ave.

## 6. Lo que sale del pollo no es "sólidos del efluente"

El balance dice que por día salen ~6 t de plumas, vísceras, cabezas, sangre recuperable y otros (10.000 aves/día). Eso es **masa que hay que capturar antes del desagüe** ("potencialmente segregable en origen"), **no** los sólidos que hay en el agua. Cuánto se escapa al desagüe depende de cómo se diseñe y opere la planta (tamices, transporte en seco, disciplina); los SST del efluente se miden en el agua.

## 7. DAF y lodos

**DAF (flotación por aire disuelto):** un tanque con burbujas finísimas que "levantan" grasa y partículas a la superficie. Pretratamiento estándar en plantas cárnicas; no saca lo disuelto (la sangre).

Después, el tratamiento **biológico**: **anaeróbico** (sin aire; poca energía, biogás) o **aeróbico** (con aire; más energía y más lodo). No se eligió ninguno.

**Lodos:** todavía **no se pueden calcular**. Dependen de los sólidos que entren, de cuánto saque el DAF, de los químicos, de la biomasa que genere el biológico y de cuán seco quede el lodo. El modelo muestra un **ejemplo ilustrativo** (~2 t/día húmedas a 10.000 aves/día) con cada supuesto a la vista, pero el número real es **pendiente de dimensionamiento**.

## 8. kW vs kWh

- **kWh** = energía (como los kilómetros recorridos). Es lo que se factura. 10.000 aves/día: **~8.200 kWh por día de faena** (~0,8 kWh/ave).
- **kW** = potencia (como la velocidad). Define la conexión, el transformador y el generador.
- Con los kWh solo se puede calcular una **potencia media equivalente**: 8.200 kWh ÷ 24 h ≈ **340 kW**; o, solo el proceso, 7.250 kWh ÷ 14 h ≈ **520 kW**. **Eso no es la potencia pico.**
- La **potencia pico** (y la potencia a contratar, el transformador, el generador) sale de una **lista de equipos**: kW de cada uno, cuánto de su potencia usa, cuáles funcionan a la vez, el golpe de arranque de los motores grandes y el factor de potencia. Esa lista vendrá del catálogo de equipos de la sesión 09A y de las cotizaciones. Hoy: **pendiente**.

## 9. Calor: MJ por día no es tamaño de caldera

- ~**1 MJ útil por ave** (sensibilidad) → ~13 GJ/día de combustible, como ~340 m³/día de gas natural.
- Saber cuánto gas se usa **en el día** no dice qué caldera hace falta: eso depende de **cuándo** se usa (escaldado todo el turno, limpieza concentrada en pocas horas, esterilizadores). La limpieza **podría** generar una demanda concentrada; hay que compararla con el escaldado en un **perfil horario**. Pico térmico: **pendiente**.

## 10. Tonelada de refrigeración y kW frigorífico

- **kW frigorífico**: cuánto calor saca el frío por segundo. **No es** lo que consume de electricidad.
- **TR**: 1 TR = 3,517 kW frigoríficos.
- **kW eléctricos ≈ kW frigoríficos ÷ COP** (COP **supuesto**: ~3 para enfriar a 0 °C; ~1,4 para congelar a −35 °C). No es un consumo garantizado.
- A 10.000 aves/día, **enfriar solo el producto** de 38 a 4 °C en 8 h pide ~**99 kW frigoríficos** (~28 TR). Enfriar el agua del chiller suma ~69 kW y las salas, docks y otros podrían sumar más. **Eso no es la planta frigorífica**: la capacidad real sale de un balance frigorífico completo (paredes, aire, puertas, personas, motores, cámaras, túneles, desescarche…).

## 11. Congelación vs almacenamiento

- **Congelación** = **túnel**: toneladas **nuevas** por día que hay que llevar de +4 °C a −18 °C.
- **Almacenamiento** = **cámara**: toneladas **ya congeladas** que se guardan.
- Una cámara que guarda 300 t **no** congela 300 t/día. Ejemplo (10.000 aves/día, perfil exportador de prueba): congelar **12 t/día**, pero guardar **168 t** con 14 días de producción.
- Dos formas de contar días: **de producción** o **calendario** (con 250 días de faena, 14 días calendario = 68 % de 14 días de producción).

## 12. Respaldo eléctrico

El modelo muestra una **carga crítica ilustrativa** (~80 kW a 10.000 aves/día: frío de cámaras, control, emergencia, agua, efluentes, ventilación de aves). **No es el generador**. El generador se dimensiona con la lista de cargas críticas, el arranque de compresores, la secuencia, la autonomía y la redundancia, y con una decisión: ¿durante un corte seguimos faenando o solo mantenemos el frío? Hoy: **pendiente**.

## 13. Por qué los servicios pueden limitar la capacidad de la planta

La capacidad real de la planta es la de su **eslabón más débil** ([`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md) §3).

| Servicio | Cómo limita | Qué hay que preguntarle al sitio |
|---|---|---|
| **Agua** | El pozo o la red no entregan el caudal por hora | ¿Cuántos m³/h sostenidos? (sensibilidad: ~20 m³/h de media en 12 h a 10.000 aves/día) |
| **Efluentes** | El permiso fija caudal o carga máxima; el tratamiento tiene capacidad fija | ¿Dónde se puede volcar y con qué límites? |
| **Energía** | La distribuidora no puede dar la potencia | ¿Cuánta potencia hay? (la necesaria sale de la lista de cargas) |
| **Frío** | Chiller o túneles no enfrían a tiempo; cámaras llenas | Balance frigorífico del proveedor |
| **Calor** | La caldera no llega en las horas de limpieza | Perfil horario de agua caliente |
| **Lodos y subproductos** | Si nadie los retira, se acumulan | ¿Quién los recibe y a qué distancia? |

**Por eso los servicios son parte de la decisión de escala y de localización**, no un detalle de ingeniería posterior.

## 14. Top-down hoy, bottom-up mañana

Todo lo anterior es **top-down**: indicadores por ave (L/ave, kWh/ave, MJ/ave). Cuando haya equipos cotizados (catálogo de la sesión 09A + proveedores), se sumarán sus consumos reales (**bottom-up**) y se compararán: si difieren mucho, el modelo avisa. Ningún número de esta guía es una especificación.
