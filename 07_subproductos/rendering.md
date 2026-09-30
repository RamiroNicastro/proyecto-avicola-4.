# Rendering — qué es, qué recibe y cómo compararlo

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance:** explicar el rendering y comparar conceptualmente **rendering propio / tercerizado / venta directa de subproductos**. **No se decide** construir rendering propio (DEC-027), **no** se asume rendimiento de harinas (DPV-065) ni se cotiza equipo.
> **Fuentes:** extractos `[PVDP]` (FTE-164, FTE-181, FTE-182, FTE-186, FTE-187, FTE-190, FTE-192, FTE-193). Masas: [`mapa_subproductos.md` §10](mapa_subproductos.md) y [`escenarios_subproductos.csv`](escenarios_subproductos.csv).

---

## 1. Qué es una planta de rendering

Una planta de **rendering** transforma subproductos animales no destinados a consumo humano en **harinas proteicas** y **grasas** mediante **cocción/esterilización con calor y presión, separación de la grasa y secado**. En la normativa argentina de inspección, las instalaciones equivalentes aparecen como **digestor** (destino de decomisos y desperdicios) y **grasería** (Decreto 4238/68, caps. XIV y XIX, FTE-192 `[PVDP]`).

Procesos típicos (conceptuales):

| Corriente | Proceso | Producto |
|---|---|---|
| Plumas | **Hidrólisis** a presión con vapor (rompe la queratina) → secado a ~8–10 % de humedad | Harina de plumas hidrolizada (~90 % de proteína bruta, FTE-164 `[PVDP]`) |
| Vísceras, cabezas, huesos, garras de descarte, piel | Cocción (continua o por lotes) → **prensado** (separa grasa) → secado → molienda | Harina de subproductos avícolas / de vísceras; **grasa avícola** |
| Sangre | Coagulación → deshidratación → secado; o incorporación a la hidrólisis de plumas | Harina de sangre; harina de plumas y sangre |
| Huesos (con carne) | Cocción y secado | Harina de carne y hueso |

Todo el proceso **evapora agua**: el costo principal es **energía térmica** (caldera) y el principal problema ambiental son los **olores** y los **condensados**.

## 2. Qué puede recibir

| Material | kg/ave (2,9 kg) | ¿Rendering? | Condición |
|---|---|---|---|
| Plumas (húmedas) | 0,241 | Sí | Proceso específico de hidrólisis; mezclar con otras corrientes cambia el mercado de la harina (§3) |
| Sangre recuperada | 0,084 | Sí | Colecta separada y retiro rápido |
| Vísceras no comestibles (+ contenido GI) | 0,130 (+ 0,035) | Sí | Retiro diario; el contenido GI agrega humedad y cenizas |
| Cabezas | 0,072 | Sí | — |
| Huesos y residuo óseo de CMS (solo con deshuese/CMS) | 0,160–0,331 | Sí | — |
| Garras de descarte | 0,005 | Sí | — |
| Piel y grasa sin comprador alimentario | hasta 0,110 + 0,052 | Sí | Pasa de B a C |
| Carcasa, cuello, menudencias **sin comprador** | hasta 0,58 | Sí | Pérdida de valor: son comestibles (B → C) |
| **Decomisos** | 0,040 | **Según normativa y causa** | El Decreto 4238 prevé el digestor como destino de decomisos (FTE-192 `[PVDP]`); verificar qué causas y usos del producto (DPV-066). En la UE, el material de riesgo se clasifica en categorías 1/2 con usos restringidos (FTE-193 `[PVDP]`) |
| Aves muertas en granja / DOA | fuera del balance | Restringido | En la UE, categoría 2 (prohibida en pet food) |

## 3. Productos posibles y su mercado

| Producto | Mercado | Restricción |
|---|---|---|
| Harina de plumas hidrolizada | Alimento balanceado de aves, cerdos, peces; pet food; fertilizante orgánico | **Exceptuada** de la prohibición para rumiantes si se garantiza analíticamente la ausencia de otras proteínas (Res. SAGPyA 1389/2004, FTE-186 `[PVDP]`) |
| Harina de sangre | Aves, cerdos, peces, mascotas | **Prohibida para rumiantes** (FTE-186) |
| Harina de vísceras / de subproductos avícolas | Aves, cerdos, peces, pet food | Prohibida para rumiantes |
| Harina de carne y hueso (avícola) | Idem | Prohibida para rumiantes |
| Grasa avícola | Alimento balanceado; pet food; usos industriales | Calidad (acidez) según frescura de la materia prima |

**Mezclar define el mercado:** si las plumas se procesan junto con sangre o vísceras, la harina deja de ser "harina de plumas" pura y pierde la excepción para rumiantes. Precio de referencia de harina de plumas: 350–650 USD/t a granel (FTE-137 `[PVDP · débil]`, **no usar para calcular**). Habilitación de elaboradores de alimentos para animales: Res. SENASA 1416/2024 (FTE-187 `[PVDP]`).

## 4. Tres opciones

| Criterio | **A. Rendering propio** | **B. Rendering tercerizado** | **C. Venta directa de subproductos** |
|---|---|---|---|
| Qué es | La empresa procesa sus subproductos en una planta propia (en el predio o separada) | Un rendering de terceros retira las corrientes y las procesa (compra, retira sin cargo o **cobra**) | Se venden materias primas crudas a usuarios distintos del rendering (p. ej. fabricantes de pet food, industria), sin procesarlas |
| Materiales | Todas las corrientes C (y decomisos si se permite) | Las que el tercero acepte | Solo las **aptas y con comprador** (cuellos, carcasas, menudencias, patas, piel; no vísceras ni decomisos) |
| **CAPEX relativo** | **Alto**: cocinadores/hidrolizador, prensa, secadores, caldera, molienda, silos, tratamiento de olores y condensados, obra civil | **Bajo**: contenedores estancos, zona de carga, eventual refrigeración | **Bajo–medio**: frío (congelado), envasado, cámara |
| **Escala** | Requiere volumen continuo; a 2.500 aves/día la clase C es ~1,3 t/día; a 20.000, ~10,7 t/día (hasta ~17 con deshuese) | Cualquier escala si existe receptor a distancia viable | Cualquier escala; lotes mínimos del comprador |
| **Complejidad** | Alta: operación industrial distinta de la faena, personal, mantenimiento, calidad de harina | Baja: logística y contrato | Media: especificación, frío, trazabilidad |
| **Olores** | **Altos** en el propio predio (tratamiento obligatorio: biofiltros, lavadores de gases) | Se trasladan al tercero; quedan olores de almacenamiento transitorio | Bajos |
| **Energía** | **Alta** (vapor para cocción e hidrólisis y secado: evaporación del agua de plumas, sangre y vísceras) | Nula (salvo frío transitorio) | Frío de congelado |
| **Efluentes** | Condensados y aguas de lavado de alta carga orgánica; gases no condensables | Menores (lavado de contenedores) | Menores |
| **Permisos** | SENASA (elaborador de alimentos para animales, Res. 1416/2024; digestor/grasería, Decreto 4238); ambiental provincial (categoría industrial, emisiones, olores); municipal (zonificación) | Contrato con un receptor **habilitado**; manifiestos de transporte de residuos/subproductos según provincia | Habilitación del comprador (pet food: Res. 1415/1416-2024) |
| **Logística** | Interna (sin transporte) | **Retiro diario** (plumas, sangre y vísceras se deterioran en horas); distancia crítica | Cadena de frío hasta el comprador |
| **Riesgo principal** | Inversión y operación de una segunda industria; mercado de harinas | **Dependencia de un receptor** (precio, continuidad, cierre); si deja de retirar, la planta de faena no puede operar | Comprador de nicho; volumen pequeño |
| **Ingreso** | Precio de harinas y grasa − energía − mano de obra − mantenimiento | Precio de las corrientes crudas (positivo, cero o negativo) | Precio de materia prima apta (puede superar al de rendering) |

**Las opciones no son excluyentes por material:** p. ej. C para cuellos y carcasas aptas, B para plumas, sangre y vísceras. Lo que sí es excluyente es enviar **la misma masa** a dos destinos (rutas en [`rutas_valorizacion.md`](rutas_valorizacion.md)).

## 5. Cuándo tendría sentido estudiar un rendering propio (sin umbral)

1. **Volumen:** a 10.000 aves/día la clase C suma ~5,3 t/día (V1) a ~8,6 t/día (V3); a 20.000, ~10,7 a ~17,3 t/día ([`escenarios_subproductos.csv`](escenarios_subproductos.csv), filas D01). Un fabricante ilustra equipos para una planta de 30 t/día de pollo vivo (≈ 10.000 aves/día; FTE-182 `[PVDP]`): **existe tecnología para esa escala; su rentabilidad no está demostrada**.
2. **Mercado de terceros:** si no hay rendering habilitado a distancia de retiro diario, o si cobra por retirar, el propio pasa de "opción" a "necesidad" (regla 10: hacer / comprar / tercerizar / postergar).
3. **Localización:** en polos avícolas (Entre Ríos, Buenos Aires) es más probable encontrar receptores; en zonas nuevas, menos (DEC-003).
4. **Integración:** si existe fábrica de alimento propia (DEC-024) o un comprador estable de harinas, y si el rendering se integra con el tratamiento de efluentes y la caldera.
5. **Permisos y vecindad:** olores y categoría ambiental pueden condicionar la localización de la planta de faena entera.

**Información necesaria antes de cualquier decisión:** plantas de rendering en zonas candidatas, qué reciben, a qué precio o costo, frecuencia y distancia (DPV-065); rendimientos y materia seca (DPV-065); normativa (DPV-066); costos de disposición si nadie retira (DPV-072); mercado de harinas (DPV-076).
