# Mapa de productos, coproductos y subproductos del ave

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Pregunta central:** ¿qué sale de cada pollo, qué puede venderse, procesarse, exportarse o valorizarse, y qué termina como residuo? Criterio: **maximizar el ingreso total por ave** (SUP-013) **sin duplicar masas ni suponer que todo tiene comprador**.
> **Base física:** balance de masa v1.1 ([`../04_balance_masa/`](../04_balance_masa/README.md)), **sin modificarlo**. Pollo de **2,9 kg vivo en planta**, rendimiento y condenas "medio", chiller por inmersión. Todas las cifras de kg/ave salen del balance a través de [`modelo_subproductos.py`](modelo_subproductos.py), que verifica que las matrices coincidan con el modelo (test S08) y que ninguna ruta incompatible se sume (tests S04, S05). Variantes de ruta V1–V6: §7.
> **Qué no se hace:** no se asignan precios (SUP-018), no se elige ruta, no se diseña maquinaria ni se fija capacidad (reglas 7–9). La clase y el nivel de valor son **cualitativos y condicionales** (SUP-046, SUP-047).
> **Fuentes:** acceso directo a documentos otra vez bloqueado (`EGRESS_BLOCKED` en argentina.gob.ar e infoleg, 2026-09-30; DPV-009). Normativa leída solo en extractos de buscador: `[PVDP]` (FTE-185 a FTE-193).
> Documentos hermanos: rutas y árboles de decisión en [`rutas_valorizacion.md`](rutas_valorizacion.md); rendering en [`rendering.md`](rendering.md); productos comestibles en [`../06_productos/catalogo_productos.md`](../06_productos/catalogo_productos.md) y elaborados en [`../06_productos/elaborados.md`](../06_productos/elaborados.md); matriz en [`matriz_valorizacion.csv`](matriz_valorizacion.csv); síntesis en [`conclusiones_valorizacion.md`](conclusiones_valorizacion.md).

---

## 1. Inventario completo de salidas

kg/ave de **masa biológica** (salvo plumas húmedas y agua de goteo, que incluyen agua) y % del peso vivo (PV = 2,9 kg). Las filas marcadas "alternativa" **no se suman** entre sí: son formas distintas de presentar la misma masa (p. ej. la pechuga con hueso **o** la suprema + solomillo + piel + hueso). ID = fila de [`matriz_valorizacion.csv`](matriz_valorizacion.csv).

**Vida útil:** en esta fase se expresa en **categorías** (horas / días refrigerado / meses congelado). No se encontró una fuente de vida útil comercial argentina; la guía de almacenamiento de la FDA (FTE-189 `[PVDP]`: pollo crudo 1–2 días en heladera doméstica; congelado: entero hasta 12 meses, trozos 9, menudencias 3–4) es **doméstica** y solo sirve de orden de magnitud. La vida útil de cada presentación se determinará con estudios propios y exigencias del cliente (DPV-078, SUP-051).

### 1.1 Productos principales y cortes (derivan de la carcasa: presentaciones alternativas)

| ID | Salida | kg/ave | % PV | Clase de referencia | Potencial de venta | Frío | Vida útil | Posibles destinos |
|---|---|---|---|---|---|---|---|---|
| MAT-01 | **Pollo entero** (configuración A, sin menudencias) | 1,914 | 66,0 | A | Alto (producto masivo) — demanda del proyecto **no validada** | Refrigerado 0–4 °C o congelado | Días (refr.) / meses (cong.) | Supermercados, carnicerías, pollerías, mayoristas; congelado a Golfo (Halal), Irak, Chile |
| MAT-02 | **Pechuga con hueso** (config. B) | 0,784 | 27,0 | A | Alto | Refr. o cong. | Días / meses | Supermercados, carnicerías, gastronomía |
| MAT-03 | **Suprema** (filet sin solomillo; config. C) | 0,478 | 16,5 | A | Alto | Refr. o cong. (IQF) | Días / meses | Supermercados, gastronomía, industria; UE (cuota), Medio Oriente |
| MAT-04 | **Solomillo** (config. C) | 0,118 | 4,1 | A | Medio–alto (requiere comprador que lo pague separado) | Refr. o cong. | Días / meses | Gastronomía, supermercados, rebozados |
| MAT-05 | **Pata-muslo** (config. B) | 0,631 | 21,8 | A | Alto (volumen) | Refr. o cong. | Días / meses | Supermercados, carnicerías, mayoristas, catering; congelado a Vietnam, Chile, África |
| MAT-06 | **Muslo** con hueso (58 % de la pata-muslo) | 0,366 | 12,6 | A (si se separa) | Medio | Refr. o cong. | Días / meses | Supermercados, gastronomía |
| MAT-07 | **Muslo deshuesado** sin piel (config. C) | 0,242 | 8,3 | A | Medio–alto | Refr. o cong. (IQF) | Días / meses | Gastronomía, industria; Japón, Corea |
| MAT-08 | **Pata** (*drumstick*) con hueso | 0,265 | 9,1 | A | Medio | Refr. o cong. | Días / meses | Supermercados, carnicerías |
| MAT-09 | **Alas** | 0,208 | 7,2 | B | Medio (volátil) | Refr. o cong. | Días / meses | Gastronomía, mayoristas; Asia (China no disponible) |
| MAT-10 | **Carcasa-esqueleto** (ruta venta) | 0,393 | 13,6 | B | Bajo–medio: **comprador no identificado** | Refr. o cong. | Días / meses | Caldos/sopas, mayoristas, pet food; **o** CMS; **o** rendering |

### 1.2 Coproductos de faena comestibles (no forman parte de la carcasa)

| ID | Salida | kg/ave | % PV | Clase | Potencial de venta | Frío | Vida útil | Posibles destinos |
|---|---|---|---|---|---|---|---|---|
| MAT-11 | **Cuello** | 0,075 | 2,6 | B | Medio (menudencia tradicional) | Refr. o cong. | Días cortos / meses | Carnicerías, mayoristas, pet food; **o** CMS |
| MAT-12 | **Hígado** | 0,055 | 1,9 | B | Medio | Refr. (muy perecedero) o cong. | Días cortos / 3–4 meses (orientativo) | Carnicerías, pollerías, industria (paté), pet food, África |
| MAT-13 | **Corazón** | 0,014 | 0,5 | B | Bajo en masa | Refr. o cong. | Días cortos / meses | Menudencias, gastronomía (brochetas), pet food |
| MAT-14 | **Molleja** limpia | 0,040 | 1,4 | B | Medio | Refr. o cong. | Días cortos / meses | Carnicerías, mayoristas, pet food, exportación |
| MAT-15 | **Patas brutas** (antes de acondicionar) | 0,113 | 3,9 | — | Depende de la ruta (§1.3) | — | — | → garras, pata sin pelar o rendering |
| MAT-16 | **Garras grado A** (peladas) | 0,085 | 2,9 | B | **Alto solo con mercado asiático**; bajo sin él | Congelado | Meses | China (no disponible confirmado), Vietnam, Hong Kong; mercado interno reducido |
| MAT-17 | **Garras de segunda** | 0,016 | 0,6 | B | Bajo–medio | Congelado | Meses | Medio Oriente (débil), mercado interno, pet food |

### 1.3 Subproductos no comestibles, huesos, piel, grasa y CMS

| ID | Salida | kg/ave | % PV | Clase | Potencial de venta | Frío | Deterioro / vida útil | Posibles destinos |
|---|---|---|---|---|---|---|---|---|
| MAT-18 | Garras de descarte | 0,005 | 0,2 | C | Bajo | No, si se procesa en horas | Horas | Rendering |
| MAT-19 | **Cabeza** | 0,072 | 2,5 | C | Bajo | No, si se retira en horas | Horas | Rendering; pet food (a verificar) |
| MAT-20 | **Piel** (solo si se deshuesa) | 0,110 | 3,8 | B o C | Bajo; comprador industrial no identificado | Refr. o cong. | Días / meses | Industria de embutidos; rendering |
| MAT-21 | **Grasa abdominal** (queda **dentro** de la carcasa por defecto) | 0,052 | 1,8 | — (en el producto) / C si se retira | Bajo | Refr. si es alimentaria | Días | Queda en la carcasa; o grasería; o rendering |
| MAT-22 | **Recortes** (config. C; en B 0,010) | 0,037 | 1,3 | B | Medio si hay elaborados o comprador | Refr. o cong. | Días / meses | Elaborados propios, industria |
| MAT-23 | **CMS** (del esqueleto, 60 %; **alternativa** a MAT-10 vendida) | 0,236 | 8,1 | B | Bajo; uso restringido | −2 a 2 °C y uso en 12 h, o congelado (Res. 368/2003 `[PVDP]`) | **Horas** refrigerada | Chacinados cocidos y conservas; exportación (Filipinas, Sudáfrica) |
| MAT-24 | CMS máxima (esqueleto + cuello + hueso de pechuga) | 0,342 | 11,8 | B | Idem | Idem | Idem | Techo físico, no recomendación |
| MAT-25 | **Huesos** de deshuese (pechuga + muslo; config. C) | 0,164 | 5,7 | C | Bajo | No, si se procesa en horas | Horas | Rendering; CMS (hueso de pechuga) |
| MAT-26 | Residuo óseo de CMS | 0,153 | 5,3 | C | Bajo | Idem | Horas | Rendering |
| MAT-27 | **Sangre recuperada** | 0,084 | 2,9 | C | Bajo | Retiro diario o refrigeración | **Horas** (coagula y fermenta) | Rendering (co-proceso con plumas o harina de sangre) |
| MAT-29 | **Plumas** crudas húmedas (bio 0,151 + agua 0,090) | 0,241 | 8,3* | C | Bajo | No, si se procesan en el día | Horas a 1 día | Rendering (harina de plumas hidrolizada); fertilizante; compost |
| MAT-30 | **Tracto digestivo** vacío | 0,087 | 3,0 | C | Bajo | Retiro diario | Horas | Rendering (harina de vísceras); biodigestión |
| MAT-31 | Pulmones y otros no comestibles | 0,043 | 1,5 | C | Bajo | Idem | Horas | Rendering |

### 1.4 Residuos, efluentes y pérdidas

| ID | Salida | kg/ave | % PV | Clase | Destino |
|---|---|---|---|---|---|
| MAT-28 | Sangre no recuperada | 0,015 | 0,5 | D | Efluente (DQO muy alta) |
| MAT-32 | **Contenido gastrointestinal** | 0,035 | 1,2 | D | Viaja con las vísceras si el rendering lo acepta; si no, residuo |
| MAT-33 | **Decomisos** (total + parcial) | 0,040 | 1,4 | D (C si se permite el digestor) | Digestor/rendering según causa y normativa (FTE-192 `[PVDP]`, DPV-066); si no, disposición |
| MAT-34 | Cutícula de patas (merma de acondicionamiento) | 0,006 | 0,2 | D | Efluente / lodos |
| MAT-35 | Agua de goteo del producto (agua, no carne) | 0,037 | 1,3* | D | Efluente |
| MAT-36 | Pérdidas no asignadas + mermas de proceso (B) | 0,041 + 0,010 | 1,8 | P | A medir en planta (DPV-060) |

\* % sobre PV de una masa que incluye agua: solo referencia de manejo.

### 1.5 Salidas fuera del balance de planta (se listan para que nada quede sin destino)

| ID | Salida | Dónde se trata | Destino conceptual |
|---|---|---|---|
| MAT-37 | Aves muertas en granja y en transporte (DOA) | `03_produccion_primaria` | Disposición en granja (compost/fosa) o rendering si se permite; en la UE es categoría 2, prohibida en pet food (FTE-193 `[PVDP]`) |
| MAT-38 | Cama de pollo | `03_produccion_primaria` | Abono/enmienda (registro Ley 20.466 y Res. SENASA 264/2011, FTE-188 `[PVDP]`), compost, biodigestión |
| MAT-39 | Lodos y grasas del tratamiento de efluentes | `11_agua_efluentes` | Disposición, compost o biodigestión (a evaluar) |
| — | Envases, cartón, film, pallets | `20_opex` | Residuos asimilables / reciclaje |

**Comprobación:** las 36 salidas de planta (MAT-01 a MAT-36) cubren todos los componentes del balance; cada componente pertenece a un solo grupo (test S03) y los grupos suman exactamente el PV + agua incorporada en las seis variantes (test S02, error ≤ 2 × 10⁻¹⁵ kg/ave).

---

## 2. Clasificación económica — condicional al comprador

| Clase | Definición | Ejemplos (referencia) |
|---|---|---|
| **A. Producto principal** | Define el negocio; mayor valor por kg | Entero; pechuga; suprema; solomillo; pata-muslo; muslo deshuesado; pata |
| **B. Coproducto comestible** | Comestible, producido en forma conjunta con A, de menor valor por kg | Alas; menudencias; cuello; garras A y de segunda; carcasa-esqueleto; CMS; piel; recortes |
| **C. Subproducto valorizable** | No destinado a consumo humano, con valor **si** existe un proceso y un comprador | Plumas; sangre recuperada; cabezas; vísceras; huesos; garras de descarte |
| **D. Residuo / efluente** | Sin valor o con costo de tratamiento o disposición | Contenido GI; sangre no recuperada; cutícula; agua de goteo; decomisos (por prudencia) |

**Regla (SUP-046):** la clase de referencia supone que **existe un comprador o un proceso habilitado**. Sin comprador, la salida **baja de clase**: un coproducto B sin cliente comestible pasa a C (se envía a rendering) y un subproducto C sin rendering ni comprador pasa a D (costo de disposición). Una misma masa puede **subir** de clase si aparece un mercado (garras con China abierta; decomisos si la normativa permite el digestor).

| Material | Con comprador / proceso | Sin comprador | Qué lo decide |
|---|---|---|---|
| Plumas | C — ingreso (venta a rendering o harina propia) | **D — costo** (retiro y disposición) | Rendering a distancia viable y que pague o retire sin cargo (DPV-065) |
| Sangre | C — valor bajo, sobre todo evita carga al efluente | **D — carga contaminante** | Recuperación separada + receptor (DPV-080) |
| Garras grado A | B — alto valor con mercado asiático habilitado | B de bajo precio en mercado interno, o **C** (harina) | Acceso a China/Asia y registro de planta (DPV-035, DPV-077) |
| Carcasa-esqueleto | B — caldos o CMS | **C** (rendering) | Comprador de esqueleto o industria de CMS (DPV-070, DPV-071) |
| Piel | B — industria | **C** (rendering) | Industria de embutidos (DPV-071) |
| Menudencias, cuello | B — mercado tradicional | **C** (rendering) | Canal tradicional, pet food (DPV-070, DPV-073) |
| Cabezas, vísceras, huesos | C — rendering o pet food apto | **D** (disposición) | Rendering o fabricante habilitado (DPV-065, DPV-073) |
| Decomisos | C — solo si la normativa permite digestor | **D** | Normativa (DPV-066) |

**Valorización técnica ≠ valorización económica.** Que exista un proceso capaz de transformar una salida (técnica) no significa que alguien la compre a un precio que cubra el proceso, el flete y el frío (económica). Este documento clasifica la **técnica**; la económica exige precios netos (net-back) y compradores reales (§6 y [`rutas_valorizacion.md` §4](rutas_valorizacion.md)).

---

## 3. Piel y grasa

| Uso | Tipo | Material | Requisitos / comentario | Estado |
|---|---|---|---|---|
| Piel como ingrediente de embutidos y emulsiones cocidas | **Alimentario** | Piel de deshuese (0,110 kg/ave, solo config. C) | Establecimiento habilitado; límites de piel y grasa según producto (CAA, a verificar); frío | Posible; comprador no identificado (DPV-071) |
| Piel en rebozados/formados propios | **Alimentario** | Idem | Línea de elaborados ([`elaborados.md`](../06_productos/elaborados.md)) | Condicionado a DEC-030 |
| Grasa de pollo fundida para uso alimentario | **Alimentario** | Grasa abdominal retirada (hasta 0,052 kg/ave) y piel | Grasería habilitada (Decreto 4238, cap. XIV, FTE-192 `[PVDP]`) | Teórica a esta escala; mercado a relevar |
| Grasa abdominal dentro de la carcasa | **Alimentario** (en el producto) | 0,052 kg/ave | Opción por defecto del modelo (SUP-043) | Referencia |
| Rendering → grasa avícola y harina | **Industrial** | Piel sin comprador, grasa retirada | Grasa para alimento balanceado (no rumiantes, FTE-186 `[PVDP]`) | Posible vía terceros |
| Pet food (ingrediente) | **Industrial / mascotas** | Piel, grasa | Solo material apto de establecimiento habilitado (§8) | A verificar (DPV-073) |
| Oleoquímica, biocombustibles | **Industrial** | Grasa de rendering | Mercado de grasas animales | Teórica; no evaluada |

**Ruta exclusiva:** la piel se **vende** o va a **rendering** (test S04); la grasa **queda** en la carcasa o se **retira** (si se retira, sale de la carcasa y no se suma dos veces). Retirar grasa **reduce kg vendidos** de carcasa: solo conviene si el cliente penaliza la grasa o si la grasa separada vale más que en el producto.

## 4. Sangre

0,099 kg/ave drenada (3,4 % PV): **0,084 recuperable** (85 %, SUP-040) + 0,015 al efluente. A 10.000 aves/día: 0,99 t/día drenada, 0,84 t/día recuperable.

| Alternativa | Qué implica | Requisitos | Comentario |
|---|---|---|---|
| **A. Recuperación y venta/procesamiento por terceros** | Canaleta y tanque de sangre separados; retiro frecuente | Evitar dilución con agua de lavado; tanque cerrado; retiro diario o refrigeración; receptor habilitado | Es la opción de menor inversión **si existe receptor**. El uso de sangre avícola para plasma/hemoderivados requiere colecta higiénica con anticoagulante: **teórico** para el proyecto (DPV-080) |
| **B. Harina de sangre** (propia o de terceros) | Coagulación y secado | Mucha energía térmica: la sangre es mayoritariamente agua (materia seca a medir, DPV-065); habilitación como elaborador de alimentos para animales (Res. SENASA 1416/2024, FTE-187 `[PVDP]`) | **No se asume planta propia** (SUP-049): a escalas de 0,2–1,7 t/día de sangre es una línea pequeña y energéticamente cara |
| **C. Incorporación a rendering** (co-procesada con plumas u otros) | Se agrega a la hidrólisis de plumas o a la cocción de vísceras | Un extracto técnico menciona agregar ~500 L de sangre por cada 3 t de pluma cruda antes de la hidrólisis (FTE-190 `[PVDP · débil]`) | Frecuente en rendering integral; depende del receptor |
| **D. Tratamiento como carga contaminante** | La sangre va al efluente | Planta de tratamiento dimensionada para esa carga; límites de vuelco provinciales (DPV-067) | **Peor opción:** DQO de la sangre ~375.000 mg/L (FTE-181 `[PVDP]`); a 10.000 aves/día toda la sangre al efluente ≈ **350 kg DQO/día** vs ≈ 50 kg DQO/día si solo va la fracción no recuperada ([`../04_balance_masa/subproductos_masa.md` §4](../04_balance_masa/subproductos_masa.md)) |

- **Separación:** necesaria en cualquier alternativa A–C (canaleta de sangrado independiente del agua de proceso).
- **Deterioro:** horas; sin retiro diario genera olores y pierde valor.
- **Regulación:** la harina de sangre está **prohibida para rumiantes** (Res. SAGPyA 1389/2004, FTE-186 `[PVDP]`): su mercado es alimento de aves, cerdos, peces y mascotas.
- **Conclusión conceptual:** recuperar la sangre por separado se justifica **aunque no genere ingreso**, porque reduce el costo de tratamiento de efluentes. Su destino (A o C) depende de un receptor; B propia no se estudia en esta fase.

## 5. Plumas

0,151 kg/ave de pluma biológica; **0,241 kg/ave de pluma cruda húmeda** (con 0,090 kg de agua de escaldado adherida, SUP-040). A 10.000 aves/día: **2,41 t/día húmedas** (≈ 600 t/año): la mayor corriente de subproducto en masa.

| Forma / ruta | Descripción | Requisitos | Estado |
|---|---|---|---|
| **Pluma cruda** | Sale del desplumado arrastrada por agua (canaleta) | Separar del agua (tamiz, prensa) | Punto de partida |
| **Pluma húmeda** | Pluma escurrida con agua adherida (0,6 kg de agua por kg de pluma, SUP-040) | Retiro diario (se deteriora) | Lo que se entrega a un tercero |
| **Harina de plumas hidrolizada** | Hidrólisis a presión con vapor (rompe la queratina) y secado a ~8–10 % de humedad; ~90 % de proteína bruta (FTE-164, FTE-182 `[PVDP]`) | Hidrolizador, secador, caldera, tratamiento de olores y condensados; habilitación (Res. 1416/2024) | Proceso estándar de rendering |
| Hidrólisis enzimática / química | Alternativas para mejorar digestibilidad | Tecnología específica | Teórica para el proyecto |
| **Venta a rendering de terceros** | El tercero retira la pluma húmeda | Contrato, frecuencia, distancia; puede pagar, retirar sin cargo o **cobrar** | Opción de referencia (SUP-049); condiciones desconocidas (DPV-065) |
| Uso como fertilizante / enmienda | Harina de plumas o compost | Registro de fertilizantes (Ley 20.466, Res. SENASA 264/2011, FTE-188 `[PVDP]`) | Posible; mercado a relevar |
| Compostaje de pluma cruda | Con cama o residuos vegetales | Habilitación ambiental; lenta degradación de la queratina | Alternativa de disposición, no de ingreso |
| Otros (queratina, fibras) | Industriales | — | Teóricos |

**Regulación del mercado:** la Res. 1389/2004 prohíbe proteínas animales para rumiantes, pero **exceptúa la harina de plumas** si se garantiza con análisis la ausencia de otras proteínas (FTE-186 `[PVDP]`). Si la pluma se co-procesa con sangre o vísceras, la harina resultante pierde esa excepción: **mezclar define el mercado**.

**Vender a un tercero vs procesar internamente:**

| | Vender/entregar a tercero | Planta propia de harina de plumas |
|---|---|---|
| CAPEX | Nulo (contenedores) | Alto (hidrolizador, secador, caldera, olores, efluentes) |
| Riesgo | Dependencia de un receptor; precio o costo de retiro | Operación industrial adicional; energía; permisos |
| Ingreso | Precio de pluma húmeda (o costo) | Precio de harina − energía − mano de obra − mantenimiento |

**Qué escala podría justificar estudiar una planta propia** (sin fijar umbral): (a) **volumen** de plumas + otros subproductos suficiente para operar el equipo varias horas al día (a 10.000 aves/día: 2,4 t/día de pluma y 5,3 t/día de toda la clase C; a 20.000: 4,8 y 10,7 t/día); (b) **ausencia de receptor** a distancia económica o receptor que cobra; (c) posibilidad de **integrar** con otras corrientes (sangre, vísceras) y con la planta de efluentes; (d) **uso cautivo** de la harina (fábrica de alimento propia, DEC-024) o comprador estable. Un fabricante ilustra una planta de 30 t/día de pollo vivo con 2,4 t/día de plumas (FTE-182 `[PVDP]`), equivalente a ~10.000 aves/día de 2,9 kg: indica que **existe equipo para esa escala, no que sea rentable**. La comparación se hace en [`rendering.md`](rendering.md).

## 6. Vísceras no comestibles

0,130 kg/ave (tracto 0,087 + pulmones 0,017 + otros 0,026) más 0,035 kg/ave de contenido gastrointestinal que en la práctica viaja dentro del intestino. A 10.000 aves/día: **1,30 t/día + 0,35 t/día de contenido**.

| Destino | Estado | Comentario |
|---|---|---|
| **Rendering → harina de vísceras** ("harina de subproductos avícolas", con grasa) | **Permitido** con habilitación (Decreto 4238, digestor; Res. 1416/2024) `[PVDP]` | Destino habitual; prohibida para rumiantes (FTE-186) |
| Pet food (materia prima cruda) | **A verificar**: solo material apto de establecimiento habilitado (§8); el tubo digestivo con contenido difícilmente sea aceptado | No asumir |
| Compostaje | **Posible con habilitación** (Res. 264/2011 si se comercializa como enmienda; normativa provincial) | Documento INTA sobre compostaje de restos de faena identificado, no leído (DPV-066) |
| Biodigestión (biogás) | **Técnicamente posible**; permisos y economía no evaluados | Alternativa teórica; podría combinarse con lodos y contenido GI |
| Residuo (relleno / disposición) | Permitido con operador habilitado | **Costo** (DPV-072) |
| Alimentación directa de animales (cerdos, peces) con vísceras crudas | **No considerada**: riesgo sanitario; se presume no permitida (a verificar, DPV-066) | Descartada |

## 7. Cabeza y huesos

| Material | kg/ave | Rendering | CMS | Harinas | Pet food | Otros |
|---|---|---|---|---|---|---|
| Cabeza | 0,072 | Sí (destino habitual) | **No se considera** (la Res. 368/2003 define la CMS a partir de carcasas y partes de carcasas, FTE-185 `[PVDP]`; a verificar, DPV-074) | Harina de subproductos | A verificar | — |
| Carcasa-esqueleto | 0,393 | Sí (si no se vende) | Sí (0,236 de CMS + 0,153 de residuo) | — | Posible (materia prima apta) | Caldos |
| Cuello | 0,075 | Sí (si no se vende) | Sí (0,045 de CMS) | — | Posible | — |
| Hueso de pechuga (config. C) | 0,102 | Sí (defecto) | Sí (0,061 de CMS) | Harina de carne y hueso | Posible | Caldos |
| Hueso de muslo (config. C) | 0,062 | Sí | No modelado | Idem | Posible | — |
| Residuo óseo de CMS | 0,153–0,222 | Sí | **Ya fue procesado** | Idem | A verificar | — |

**Rutas incompatibles (no se suman):** carcasa-esqueleto **vendida XOR procesada a CMS XOR a rendering**; cuello **vendido XOR a CMS**; hueso de pechuga **a rendering XOR a CMS**; cabeza **a rendering XOR a pet food**; el residuo óseo de CMS es el **único** hueso de ese material (no se cuenta además el hueso original, test T17 del balance). En pollo entero y trozado **no hay corriente de hueso**: el hueso se vende dentro del producto.

**Variantes calculadas** (kg/ave; t/día a 10.000 aves/día en [`escenarios_subproductos.csv`](escenarios_subproductos.csv)):

| Variante | Descripción | Carcasa vendida | CMS | Huesos + residuo óseo | Piel vendida | Clase C total (bio + agua) |
|---|---|---|---|---|---|---|
| **V1** | Trozado, esqueleto vendido (**referencia**) | 0,410 | 0 | 0 | 0 | 0,533 |
| V2 | Trozado, esqueleto a CMS | 0 | 0,246 | 0,160 | 0 | 0,693 |
| V3 | Deshuesado, esqueleto a CMS | 0 | 0,246 | 0,331 | 0,115 | 0,864 |
| V4 | Deshuesado, esqueleto vendido | 0,410 | 0 | 0,171 | 0,115 | 0,705 |
| V5 | Deshuesado, todo a CMS, piel a rendering | 0 | 0,354 | 0,295 | 0 | 0,944 |
| V6 | Pollo entero | 0,025 | 0 | 0 | 0 | 0,533 |

(kg incluyen el agua retenida del chiller en los productos derivados de la carcasa.)

## 8. Pet food

| | Ingrediente apto y regulado | Residuo no apto |
|---|---|---|
| Qué es | Material de aves **faenadas con inspección**, apto para consumo humano pero no destinado a él por razones comerciales, o subproducto procesado habilitado | Material de riesgo: aves muertas fuera de la faena, decomisos por enfermedad, contenido digestivo, material contaminado |
| Marco argentino | Registro de productos para alimentación animal (Res. SENASA 1415/2024) y habilitación de establecimientos elaboradores (Res. 1416/2024) (FTE-187 `[PVDP]`); texto no leído (DPV-073) | Destino según Decreto 4238 y normativa ambiental (DPV-066) |
| Referencia internacional | UE, Reg. (CE) 1069/2009: categoría 3 utilizable en pet food; categoría 2 (p. ej. animales muertos fuera del matadero) **prohibida** en pet food; una mezcla adopta la categoría de mayor riesgo (FTE-193 `[PVDP]`) | Idem |
| Ejemplos del proyecto | Cuellos, carcasas, menudencias, patas/garras, piel, CMS; harinas avícolas habilitadas | Decomisos (MAT-33), contenido GI (MAT-32), aves muertas (MAT-37) |

**Salidas posibles:** (a) **fabricantes de alimento para mascotas** que compran materias primas crudas congeladas (cuellos, carcasas, menudencias) o harinas; (b) **treats** (patas, cuellos o corazones deshidratados): producto observable en el mercado, demanda **no validada**; (c) venta de harinas a pet food a través del rendering. **No se asume que el pet food acepte cualquier material**: exige especificación, habilitación, cadena de frío para crudos y trazabilidad (DPV-073). Pet food **compite por la misma masa** que el mercado alimentario (cuellos, menudencias, carcasas): es una ruta alternativa, no adicional.

---

## 9. Índice de aprovechamiento del ave (IAA) — KPI conceptual

**Definición:** porcentaje del peso vivo recibido que sale de la planta con una salida comercial o valorizable.

```
IAA = kg valorizados (masa biológica) / kg vivos ingresados en planta
```

Se mide sobre **masa biológica**: el agua retenida del chiller **no** cuenta como aprovechamiento (SUP-042). Se desagrega en:

| Subíndice | Qué mide | V1 trozado (2,9 kg) | V3 deshuesado | V6 entero |
|---|---|---|---|---|
| IAA-A | Producto alimentario principal vendido | 48,8 % | 38,0 % | 68,9 % |
| IAA-B | Coproductos comestibles vendidos | 30,9 % | 30,2 % | 11,1 % |
| **IAA alimentario (A + B)** | | **79,7 %** | **68,2 %** | **80,0 %** |
| IAA-C | Subproductos valorizados (con comprador o proceso) | 15,3 % | 26,2 % | 15,3 % |
| **IAA técnico (A + B + C)** | Techo físico si **todo** tiene salida | **95,0 %** | **94,4 %** | **95,3 %** |
| Residuos (D) | Con costo | 3,3 % | 3,3 % | 3,3 % |
| Mermas y pérdidas (P) | Sin corriente | 1,8 % | 2,3 % | 1,4 % |

Valores del balance v1.1 `[ESTIMACIÓN]` (clases del CSV del balance; suma = 100 %). **No son objetivos.**

**Dos versiones que no deben confundirse:**

- **IAA técnico:** masas con un destino técnicamente posible (cifras de la tabla).
- **IAA económico:** masas efectivamente **vendidas con net-back ≥ 0** (ingreso neto de flete, frío y proceso). Si hoy ningún subproducto C tuviera comprador, el IAA económico de V1 sería ≤ 79,7 %, y si además la carcasa no tuviera comprador, ≤ 66,1 %. La brecha **IAA técnico − IAA económico** mide cuánta masa del ave está sin mercado: es el indicador de gestión.

**Cómo medirlo después (fase operativa):**

1. Denominador: kg vivos por balanza de recepción (camión lleno − vacío), por día o por lote.
2. Numerador: kg despachados por corriente (remitos/facturas de producto, coproducto y subproducto), **ajustados por variación de stock** en cámaras y **descontada el agua retenida** estimada por ensayo de absorción (o bien informar en paralelo un IAA sobre peso comercial, rotulado como tal).
3. Clasificar cada kg despachado en: vendido con ingreso neto > 0 · entregado sin cargo · entregado **pagando** retiro · residuo dispuesto.
4. Informar mensualmente IAA técnico, IAA económico y la brecha; reconciliar con el balance de masa (DEC-028).

La adopción del KPI y su método quedan como decisión (DEC-032).

---

## 10. Escalado físico — 2,9 kg, escenario medio

t/día por día de faena (masa biológica + agua incorporada cuando corresponde). Fuente: [`escenarios_subproductos.csv`](escenarios_subproductos.csv) (variante V1 salvo indicación). **Escenarios, no capacidad** (regla 9); t/año = t/día × 250 (SUP-044).

| Material | kg/ave | 2.500 aves/día | 5.000 | **10.000** | 20.000 |
|---|---|---|---|---|---|
| **Producto principal** (pechuga c/h + pata-muslo; V1) | 1,475 | 3,69 | 7,37 | **14,75** | 29,50 |
| Alas | 0,217 | 0,54 | 1,08 | **2,16** | 4,33 |
| Carcasa-esqueleto (ruta venta) | 0,410 | 1,02 | 2,05 | **4,10** | 8,19 |
| **Menudencias** (hígado + corazón + molleja) | 0,109 | 0,27 | 0,55 | **1,09** | 2,18 |
| Cuello | 0,075 | 0,19 | 0,37 | **0,75** | 1,49 |
| **Garras** grado A + segunda | 0,101 | 0,25 | 0,51 | **1,01** | 2,02 |
| — de las cuales grado A | 0,085 | 0,21 | 0,43 | 0,85 | 1,70 |
| **Plumas** crudas húmedas | 0,241 | 0,60 | 1,21 | **2,41** | 4,83 |
| — masa biológica de pluma | 0,151 | 0,38 | 0,75 | 1,51 | 3,02 |
| **Sangre** recuperada | 0,084 | 0,21 | 0,42 | **0,84** | 1,68 |
| **Vísceras** no comestibles | 0,130 | 0,33 | 0,65 | **1,30** | 2,61 |
| Contenido GI | 0,035 | 0,09 | 0,17 | 0,35 | 0,70 |
| Cabezas | 0,072 | 0,18 | 0,36 | **0,72** | 1,45 |
| **Huesos** + residuo óseo (solo con deshuese, V3) | 0,331 | 0,83 | 1,65 | **3,31** | 6,62 |
| **CMS potencial** (esqueleto a CMS; **alternativa** a vender la carcasa) | 0,236 | 0,59 | 1,18 | **2,36** | 4,72 |
| Piel (solo con deshuese, V3) | 0,115 | 0,29 | 0,58 | 1,15 | 2,30 |
| Decomisos | 0,040 | 0,10 | 0,20 | 0,40 | 0,80 |
| **Materia prima potencial de rendering** (clase C, V1) | 0,533 | 1,33 | 2,67 | **5,33** | 10,67 |
| — ampliada con decomisos y contenido GI (si se permite) | 0,608 | 1,52 | 3,04 | 6,08 | 12,17 |
| — con deshuese y CMS (V3) | 0,864 | 2,16 | 4,32 | 8,64 | 17,29 |
| Días de faena para llenar un reefer de 25 t de garras grado A | — | 118 | 59 | **29** | 15 |

**Lectura:** a 2.500 aves/día ninguna corriente de subproducto supera ~0,6 t/día y un contenedor de garras tarda ~6 meses: a esa escala la valorización pasa por **terceros o consolidadores**. A 10.000–20.000 aves/día, la clase C suma 5–11 t/día (hasta 17 t/día con deshuese completo): recién ahí tiene sentido **estudiar** procesamiento propio ([`rendering.md` §5](rendering.md)).
