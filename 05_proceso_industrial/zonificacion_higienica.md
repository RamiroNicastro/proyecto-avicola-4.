# Zonificación higiénica conceptual (zonas sucia y limpia)

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A) · Fase 0

> **Alcance:** principios de separación sanitaria entre zonas y cruces de flujo que el diseño debe evitar. **No** es un layout: no hay metros, superficies ni ubicación de salas (eso corresponde a `09_layout_obra_civil`, fase posterior). Los requisitos normativos concretos (Decreto 4238/68, Res. SENASA 592/2026, estándar UE) están **sin leer en su texto original** (DPV-007, DPV-09A-03).
> **Base:** principio de "marcha hacia adelante" de zona sucia a zona limpia, sin retrocesos ni cruces (guía INTA de faena de aves, FTE-09A-029 `[PVDP]`); requisitos de flujos separados para habilitación SENASA y exportación ([`../17_exportacion/requisitos_planta_exportadora.md` §1 y §3](../17_exportacion/requisitos_planta_exportadora.md)). Flujo de etapas: [`flujo_proceso.md`](flujo_proceso.md).

---

## 1. Principios

1. **Marcha hacia adelante:** el producto avanza siempre de lo más contaminado a lo más limpio y de lo caliente a lo frío; nunca vuelve atrás (FTE-09A-029 `[PVDP]`).
2. **Barrera en cada cambio de zona:** paredes o separaciones físicas, con aberturas solo para el paso del producto (transportador aéreo, cinta, ventana de traspaso).
3. **Personas y utensilios asignados a una zona:** el personal, los equipos y los utensilios de la zona sucia no circulan en la zona limpia (FTE-09A-029 `[PVDP]`); vestimenta de color distinto por zona, vestuarios y accesos separados, pediluvios y lavamanos en cada acceso.
4. **Aire y agua de lo limpio a lo sucio:** el aire no debe ir de la zona sucia a la limpia (sobrepresión en la zona limpia; tomas de aire con filtro, FTE-09A-029 `[PVDP]`); los desagües corren desde la zona limpia hacia la sucia, nunca al revés.
5. **Subproductos y residuos salen por su propio camino:** nunca atraviesan salas de producto terminado ni comparten puertas con él.
6. **Envases y materiales entran limpios y por separado:** el cartón y los pallets (sucios por definición) no entran a las salas de proceso; el envase primario entra por un pasaplatos o esclusa.
7. **Temperatura como barrera:** a partir del enfriamiento, todo el producto permanece en salas refrigeradas hasta la expedición.
8. **Inspección oficial con espacio propio:** oficina, puestos en línea y sala de decomisos accesibles sin cruzar zonas limpias con indumentaria de zona sucia.

## 2. Zonas y su nivel sanitario

| Zona | Operaciones ([`flujo_proceso.md`](flujo_proceso.md)) | Nivel sanitario | Temperatura (cualitativa) | Personal | Límite con la zona siguiente |
|---|---|---|---|---|---|
| **Z0 Exterior y vehículos** | Circulación de camiones de aves, lavado de camiones, cajones y módulos | Sucio (bioseguridad) | Ambiente | Choferes, lavado | Cerco perimetral; circuitos separados para vivo, producto, subproductos |
| **Z1 Recepción de vivo** | E01–E04: recepción, espera, descarga, colgado | **Sucio** (polvo, plumas, heces) | Ambiente, ventilado | Colgadores, recepción | Pared con abertura para la línea de grilletes |
| **Z2 Faena inicial** | E05–E10: aturdido, degüello, sangrado, escaldado, desplumado, patas/cabeza | **Sucio** (húmedo, vapor) | Caliente/húmedo | Operarios de faena | **Transferencia E11**: pared con paso de la carcasa sin pluma a la línea de evisceración |
| **Z3 Evisceración** | E11–E17: apertura, extracción, inspección, menudencias, lavado | **Intermedio** (riesgo fecal) | Ambiente controlado | Evisceradores, inspección oficial | Entrada al enfriamiento |
| **Z4 Enfriamiento** | E18–E19 | **Limpio** (inicio) | Frío | Operación del chiller | Salida a clasificación |
| **Z5 Área limpia refrigerada** | E20–E25: clasificación, entero, trozado, deshuese, garras, menudencias, envasado primario | **Limpio** | Refrigerada | Operarios de sala limpia | Envase secundario |
| **Z6 Empaque secundario** | E26: encajonado, paletizado, cartón | **Limpio seco** (producto ya envasado) | Refrigerada | Empaque | Cámaras |
| **Z7 Cámaras y congelado** | E27–E28 | Producto envasado | Frío / congelado | Cámaras | Andén |
| **Z8 Expedición** | E29: preparación de pedidos, andenes de carga | Producto envasado | Frío (andén con sello) | Expedición, choferes | Camión refrigerado / reefer |
| **ZX Subproductos y residuos** | X1–X7: sangre, plumas, vísceras, cabezas, decomisos, hueso | **Sucio** | Ambiente; algunos con frío | Personal exclusivo | Salida propia de camiones de retiro |
| **ZS Servicios** | Sala de máquinas de frío, calderas/agua caliente, aire comprimido, tratamiento de efluentes, talleres | Técnico | — | Mantenimiento | Acceso a zonas solo con cambio de indumentaria |
| **ZP Personal e inspección** | Vestuarios por zona, comedor, oficina del servicio oficial, laboratorio de autocontrol | Social / técnico | — | Todo el personal | Barreras sanitarias por zona |

**Frontera principal:** la transferencia de la línea de faena a la de evisceración (E11) separa lo que tuvo plumas de lo que se abre. La segunda frontera es la salida del enfriamiento: desde ahí el producto está en zona limpia y fría.

## 3. Cruces de flujo que deben evitarse

| Flujo | Cruce a evitar | Por qué | Cómo se resuelve conceptualmente (no es diseño) |
|---|---|---|---|
| **Personas** | Operario de colgado, faena o subproductos que entra a sala limpia sin cambio | Contaminación microbiológica y de plumas | Vestuarios y accesos por zona; colores de ropa; pediluvio y lavamanos obligatorios; comedor sin cruce de zonas |
| **Personas** | Mantenimiento que pasa de zona sucia a limpia con la misma ropa y herramientas | Contaminación | Herramientas por zona o sanitización; cambio de ropa |
| **Producto** | Carcasa limpia que vuelve a una zona anterior (reproceso) | Recontaminación | Estación de reproceso dentro de la misma zona o descarte |
| **Producto** | Producto crudo que comparte sala con cocido (si hubiera elaborados) | Contaminación de producto listo para consumo | Sala y personal separados (espacio para futuros cocidos, [`../17_exportacion/requisitos_planta_exportadora.md` §3](../17_exportacion/requisitos_planta_exportadora.md)) |
| **Aves vivas** | Camión de aves vivas que circula junto al andén de expedición | Bioseguridad y contaminación de producto | Accesos y playas separados |
| **Aves vivas** | Polvo y plumas de la recepción que llegan a zonas limpias por el aire | Contaminación aérea | Presión de aire y separación física |
| **Residuos** | Contenedores de vísceras, plumas o decomisos que atraviesan salas de producto | Contaminación grave | Canales, bombas o tornillos hacia ZX; salida propia |
| **Subproductos** | Mezclar decomisos con subproductos aptos para rendering o pet food | Incumplimiento normativo y pérdida de valor | Recipientes identificados; decomisos bajo control oficial |
| **Subproductos** | Garras y menudencias (comestibles) tratadas como subproductos | Pérdida de condición de alimento | Circuito de producto hasta su sala |
| **Envases** | Cartón y pallets que ingresan a salas de proceso | Suciedad, humedad, plagas | Depósito de envases separado; envase primario por esclusa; cartón solo en Z6 |
| **Envases retornables** | Cajones de aves vivas lavados que vuelven a zona de producto | Contaminación | Lavadero de cajones en Z0/Z1; nunca en zona de producto |
| **Vehículos** | Camión de aves vivas, de subproductos y de producto terminado por el mismo acceso o andén | Contaminación cruzada y bioseguridad | Tres circuitos: vivo, subproductos, producto; lavado y desinfección de camiones de vivo |
| **Agua** | Desagüe de zona sucia que pasa por zona limpia | Contaminación por reflujo | Pendientes desde zona limpia hacia sucia; rejillas y sifones |
| **Aire** | Condensados y aire de escaldado que llegan a evisceración o sala limpia | Contaminación | Extracción de vapor; presión escalonada |

## 4. Diferencias conceptuales por escala

| Escala | Separación física | Riesgo típico |
|---|---|---|
| **2.500 aves/día** | Mismas zonas y principios; salas más pequeñas. La tentación es compartir salas (p. ej., evisceración y trozado en un mismo ambiente) o personal entre zonas | **Personal polivalente** que cambia de zona durante el día: exige procedimientos de cambio muy estrictos |
| **5.000** | Zonas claramente separadas; sala de garras y menudencias puede compartir ambiente con trozado (dentro de zona limpia) | Crecer por agregado sin respetar la marcha hacia adelante |
| **10.000** | Salas dedicadas por operación (trozado, deshuese, garras, menudencias, empaque); circuitos de subproductos por canal/bomba | Volumen de subproductos exige retiro continuo |
| **20.000** | Igual que 10.000 con más capacidad; posibles dos líneas paralelas | Coordinación de flujos de dos líneas sin cruces |

**La zonificación no se simplifica por ser chica la planta:** una planta de 2.500 aves/día con habilitación SENASA necesita la misma secuencia de zonas que una de 20.000; lo que cambia es el tamaño de cada zona y el grado de mecanización de los traspasos. Prever desde el inicio el **orden** de las zonas para que la ampliación se haga "hacia adelante" sin invertir flujos ([`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md), DEC-035).

## 5. Limpieza y sanitización: horas netas de faena vs tiempo total del establecimiento

La **hora neta de faena** es la hora en que la línea recibe aves. El **tiempo total del establecimiento** agrega todo lo que la planta necesita para poder volver a faenar al día siguiente. La cuantificación de sensibilidad está en [`cuellos_botella.md` §4](cuellos_botella.md) (8 h netas → 13–20 h de establecimiento; 16 h netas → 22–29 h, es decir, **no entran en un día** salvo con tiempos bajos). No se dimensionan todavía consumos de agua, químicos ni personal de limpieza.

Secuencia conceptual del ciclo de limpieza y sanitización (POES; orden típico descrito en FTE-09A-028 `[PVDP · débil]`):

| Paso | Qué se hace | Por qué importa para la capacidad | Dependencia de diseño |
|---|---|---|---|
| 0. Fin de producción y vaciado | Últimas aves terminan el proceso; producto retirado o protegido | Cierre y vaciado de línea (0,5–1 h) | Longitud del proceso, chiller y cámaras intermedias |
| 1. Bloqueo y desarme | Bloqueo eléctrico de equipos; desarme de partes que se lavan aparte (cuchillas, guardas, bandejas) | Equipos difíciles de desarmar alargan la ventana | **Diseño higiénico** de equipos: accesibilidad, desarme sin herramientas |
| 2. Retiro de sólidos en seco | Recolección de restos, plumas, vísceras | Reduce agua y carga del efluente | Canales y bandejas de recolección |
| 3. Prelavado | Agua (tibia) para retirar suciedad gruesa | Consumo de agua; tiempo | Presión y puntos de agua por zona |
| 4. Espuma / químicos | Aplicación de detergente (alcalino o ácido según suciedad), tiempo de contacto | Tiempo de contacto es fijo | Sistema de espuma centralizado o móvil; compatibilidad de materiales (acero inoxidable) |
| 5. Fregado manual | Donde la espuma no alcanza | Mano de obra | Superficies lisas y accesibles |
| 6. Enjuague | Retiro del detergente | Agua | — |
| 7. Desinfección | Aplicación de sanitizante y tiempo de contacto | Tiempo | — |
| 8. Inspección | Verificación visual y, según plan, microbiológica (hisopados); registro POES | Si falla, se repite la limpieza | Registro y responsables |
| 9. Rearmado y preparación | Montaje, lubricación de grado alimentario, arranque de frío, inspección preoperacional (con el servicio oficial) | Preoperativo 0,5–1 h | Mantenimiento programado en esta ventana |

**Reglas de zonificación durante la limpieza:** se limpia de la zona limpia hacia la sucia (y de arriba hacia abajo), con equipos y personal de limpieza asignados por zona; las mangueras y útiles de la zona sucia no entran a la zona limpia; el agua corre hacia los desagües de zona sucia.

**Implicancias para la escala:** con un turno de faena la limpieza completa entra en la noche; con dos turnos queda comprimida entre turnos o se hace por sectores. En plantas de dos turnos el diseño higiénico (tiempo de limpieza por equipo) y la redundancia (limpiar un equipo mientras otro trabaja) pasan a ser **parte de la capacidad**.

## 6. Pendientes

- Leer el texto original del Decreto 4238/68 (capítulo de aves) y de la Res. SENASA 592/2026 sobre zonas, iluminación de puestos de inspección, temperaturas de salas y separación de subproductos (DPV-007, DPV-09A-03).
- Requisitos adicionales del estándar UE (listado de planta) y de certificaciones privadas (BRCGS, IFS) sobre zonificación (DEC-012).
- Traducción a superficies y ubicación: `09_layout_obra_civil` (no iniciado).
