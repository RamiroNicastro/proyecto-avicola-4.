# Conclusiones — mapa de productos, coproductos y subproductos

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Base: [`mapa_subproductos.md`](mapa_subproductos.md), [`rutas_valorizacion.md`](rutas_valorizacion.md), [`rendering.md`](rendering.md), [`matriz_valorizacion.csv`](matriz_valorizacion.csv), [`escenarios_subproductos.csv`](escenarios_subproductos.csv), [`modelo_subproductos.py`](modelo_subproductos.py), [`guia_ramiro.md`](guia_ramiro.md), [`../06_productos/catalogo_productos.md`](../06_productos/catalogo_productos.md), [`../06_productos/elaborados.md`](../06_productos/elaborados.md), [`../06_productos/matriz_productos.csv`](../06_productos/matriz_productos.csv)

> **Alcance:** mapa físico y conceptual de todas las salidas del ave, sus rutas y su potencial de valorización. **No** es un modelo financiero, **no** asigna precios, **no** elige rutas ni productos, **no** diseña maquinaria, escala ni layout.
> **Base física:** balance de masa v1.1 **sin cambios** (sus 21 tests siguen pasando, test S01). Pollo de 2,9 kg, medio, inmersión.
> **Fuentes:** acceso directo bloqueado otra vez (sexta sesión, DPV-009); normativa nueva leída solo en extractos `[PVDP]` (FTE-185 a FTE-193).

---

## 1. Principales salidas comerciales del pollo (2,9 kg, trozado V1)

| Salida | kg/ave | % PV | Clase | Lectura |
|---|---|---|---|---|
| Pechuga con hueso (→ suprema 0,478 + solomillo 0,118 si se deshuesa) | 0,784 | 27,0 | A | Parte de mayor valor potencial en el mercado interno |
| Pata-muslo (→ muslo 0,366 + pata 0,265) | 0,631 | 21,8 | A | Parte de volumen; riesgo de excedente |
| Carcasa-esqueleto | 0,393 | 13,6 | B | **Tercera masa comestible del ave**; comprador no identificado |
| Alas | 0,208 | 7,2 | B | Valor volátil; mejor destino externo cerrado |
| Menudencias + cuello | 0,184 | 6,4 | B | Bajo precio, muy perecederas |
| Garras A + segunda | 0,101 | 3,5 | B | Valor alto **solo** con Asia abierta |
| Plumas húmedas | 0,241 | 8,3* | C | Mayor subproducto en masa |
| Vísceras no comestibles + contenido | 0,165 | 5,7 | C/D | Rendering o costo |
| Sangre recuperada | 0,084 | 2,9 | C | Sobre todo reduce carga del efluente |
| Cabeza | 0,072 | 2,5 | C | Rendering |

\* incluye agua de escaldado.

## 2. Mapa de utilización de cada parte (síntesis)

| Parte | Venta directa | Procesar | Frío | Exportable | Mercado interno | Mayor valor posible | Rendering | Residuo |
|---|---|---|---|---|---|---|---|---|
| Entero | ● | — | Refr./cong. | ○ Golfo (Halal), Chile | ● | Trozado | — | — |
| Pechuga | ● | Deshuese | Refr./cong. | ○ UE, Medio Oriente | ● | Suprema, milanesas | — | — |
| Pata-muslo | ● | Separar/deshuesar | Refr./cong. | ○ Vietnam, Chile, Japón (deshuesado) | ● | Muslo deshuesado, marinados | — | — |
| Alas | ● | Trozar | Refr./cong. | ○ Asia | ● | Marinados | — | — |
| Carcasa | ○ | CMS | Refr./cong.; CMS 12 h | ○ CMS | ○ | Embutidos cocidos | ○ | — |
| Cuello | ● | CMS | Refr./cong. | ○ África | ● | — | ○ | — |
| Menudencias | ● | Limpieza (molleja) | Refr. corta/cong. | ○ África | ● | Pet food, paté | ○ | — |
| Garras | ○ | Pelar, clasificar | Congelado | ○ China (?), Vietnam, HK | ○ | — | ○ | Cutícula |
| Piel / grasa | — | Separar | Refr./cong. | — | ○ industria | Embutidos | ● | — |
| Sangre | — | Recuperar | Horas | — | — | Harina | ● | No recuperada |
| Plumas | — | Hidrólisis | — | Harina (?) | — | Harina | ● | Si no hay receptor |
| Vísceras, cabeza, huesos | — | — | Horas | — | — | Pet food (?) | ● | Contenido GI |
| Decomisos | — | — | — | — | — | — | (?) | ● |

● ruta principal probable · ○ posible/condicionada · (?) a verificar. Detalle: [`matriz_valorizacion.csv`](matriz_valorizacion.csv).

## 3. Productos de mayor valor agregado potencial

(Ordenados por transformación y precio relativo esperado, **no** por margen, que no se calcula.)

1. **Suprema y solomillo** (deshuese de pechuga): mayor valor por kg de carne en el mercado interno; sustituyen pechuga importada.
2. **Muslo deshuesado**: convierte una parte de volumen en una de mayor valor; Japón como opción de largo plazo.
3. **Milanesas y listos para cocinar**: menor barrera de entrada entre los elaborados; vinculables a la carnicería familiar.
4. **Nuggets y cocidos**: el mayor valor agregado, pero otra industria (escala, habilitaciones, competencia importada).
5. **Garras grado A**: mayor salto de valor por destino de todo el ave, **condicionado a China/Asia**.
6. **Embutidos cocidos con CMS**: el único uso habilitado de la CMS (según extracto): dan salida a la carcasa, con valor por kg bajo.

## 4. Opciones por material (resumen)

| Material | Opciones | Condición crítica |
|---|---|---|
| **Garras** | Exportar peladas (China si reabre; Vietnam/HK) · mercado interno · pet food · rendering | Acceso a Asia y registro de planta; calidad de pata en granja; escala para llenar contenedores |
| **Menudencias** | Venta refrigerada/congelada · dentro del entero · pet food · exportación (África) · rendering | Canal diario (perecederas); definir si incluyen cuello |
| **Carcasa / CMS** | Vender carcasa · CMS para chacinados cocidos · rendering | Comprador industrial; uso restringido de la CMS (Res. 368/2003 `[PVDP]`) |
| **Piel / grasa** | Industria alimentaria · grasería · rendering · pet food | Solo existe separada si se deshuesa; comprador no identificado |
| **Sangre** | Recuperar y entregar a rendering · co-proceso con plumas · harina propia (no se asume) · efluente (peor opción) | Receptor y retiro diario; recuperar reduce la carga de DQO ~7 veces |
| **Plumas** | Tercero (paga / gratis / cobra) · harina propia · compost | Receptor a distancia viable (DPV-065) |
| **Vísceras** | Rendering · biodigestión/compost (teóricas) · disposición | Normativa y receptor |

## 5. Rendering propio vs tercerizado vs venta directa

| | Propio | Tercerizado | Venta directa |
|---|---|---|---|
| CAPEX | Alto | Bajo | Bajo–medio (frío) |
| Escala | Requiere volumen continuo (~5–17 t/día de clase C a 10.000–20.000 aves/día) | Cualquiera | Cualquiera (lotes del comprador) |
| Complejidad | Alta (otra industria) | Baja | Media |
| Olores / energía / efluentes | Altos | Trasladados al tercero | Bajos |
| Permisos | SENASA + ambiental + municipal | Receptor habilitado | Comprador habilitado |
| Riesgo | Inversión y mercado de harinas | **Dependencia de un receptor** | Nicho |

**No se decide.** Caso de referencia para escenarios: **sin rendering propio** (SUP-049). Detalle: [`rendering.md` §4–§5](rendering.md).

## 6. Toneladas/día a 10.000 aves/día (2,9 kg, V1 salvo indicación)

| Material | t/día | t/año (250 d) |
|---|---|---|
| Producto principal (pechuga c/h + pata-muslo) | 14,75 | 3.687 |
| Carcasa-esqueleto | 4,10 | 1.024 |
| Alas | 2,16 | 541 |
| Menudencias (hígado + corazón + molleja) | 1,09 | 273 |
| Cuello | 0,75 | 187 |
| Garras A + segunda (grado A: 0,85) | 1,01 | 253 |
| **Plumas húmedas** | **2,41** | 603 |
| **Vísceras no comestibles** (+ contenido GI 0,35) | **1,30** | 326 |
| **Sangre recuperada** (drenada 0,99) | **0,84** | 210 |
| **Cabezas** | **0,72** | 181 |
| Huesos + residuo óseo (solo con deshuese y CMS, V3) | 3,31 | 827 |
| CMS potencial (alternativa a vender la carcasa) | 2,36 | 590 |
| Decomisos | 0,40 | 100 |
| **Materia prima potencial de rendering** (clase C) | **5,33** (V1) · 6,08 ampliada · 8,64 (V3) | 1.334 · 1.521 · 2.161 |

Otras escalas (2.500 / 5.000 / 20.000): [`mapa_subproductos.md` §10](mapa_subproductos.md) y [`escenarios_subproductos.csv`](escenarios_subproductos.csv).

## 7. Árboles de rutas alternativas

Completos en [`rutas_valorizacion.md` §2](rutas_valorizacion.md). Resumen:

```
CARCASA ─┬─ vender                 PLUMAS ─┬─ vender cruda / rendering externo      SANGRE ─┬─ recuperar ─┬─ rendering externo
         ├─ CMS (+ residuo óseo)           ├─ planta propia (harina)                        │             ├─ harina propia (no se asume)
         └─ rendering                      └─ compost / disposición                         │             └─ sin receptor → costo
                                                                                            └─ no recuperar → efluente (evitar)
GARRAS ──┬─ pelar → exportar / mercado interno          PIEL ─┬─ industria      MENUDENCIAS ─┬─ venta / dentro del entero
         ├─ sin pelar → pet food                              ├─ elaborados                  ├─ pet food / exportación
         └─ rendering                                         └─ rendering                   └─ rendering
```

15 incompatibilidades que el modelo económico debe respetar: [`rutas_valorizacion.md` §3](rutas_valorizacion.md).

---

## 8. Precios que necesitaremos (lista maestra)

Ningún precio se estima en esta sesión. Para cada uno: **unidad** · **calidad/especificación** · **presentación** · **condición de venta** (sin IVA, puesto en planta o entregado, plazo de pago, flete) · **frecuencia de actualización**. Registrar con fecha, fuente y tipo de cambio (regla 2); cotizaciones como `[COTIZACIÓN]`.

### 8.1 Mercado interno

| # | Producto | Unidad | Calidad | Presentación | Condición | Frecuencia | Registro |
|---|---|---|---|---|---|---|---|
| P01 | Pollo entero (con y sin menudencias) | ARS/kg | Calibre de peso | Cajón 20 kg; bolsa; bandeja | Mayorista y a supermercado, sin IVA, entregado AMBA, plazo | Semanal | DPV-013 |
| P02 | Pechuga con hueso | ARS/kg | Con/sin alas | Granel; bandeja | Idem | Semanal | DPV-013 |
| P03 | Suprema / filet | ARS/kg | Con/sin solomillo; calibre | Granel; bandeja; IQF | Idem | Semanal | DPV-013 |
| P04 | Solomillo | ARS/kg | — | Granel; IQF | Idem | Mensual | DPV-070 |
| P05 | Pata-muslo | ARS/kg | Con/sin espinazo | Granel; bandeja | Idem | Semanal | DPV-013 |
| P06 | Muslo con hueso y deshuesado | ARS/kg | Con/sin piel | Granel; IQF | Idem | Mensual | DPV-013 |
| P07 | Alas | ARS/kg | Enteras/trozadas | Granel; bandeja | Idem | Quincenal | DPV-070 |
| P08 | Hígado | ARS/kg | — | Granel; bandeja; congelado | Idem | Mensual | DPV-070 |
| P09 | Corazón | ARS/kg | — | Idem | Idem | Mensual | DPV-070 |
| P10 | Molleja | ARS/kg | Limpia | Idem | Idem | Mensual | DPV-070 |
| P11 | Cuello | ARS/kg | Con/sin piel | Granel; congelado | Idem | Mensual | DPV-070 |
| P12 | Menudencias en bolsita | ARS/kg o ARS/unidad | Con/sin cuello | Bolsita | Idem | Mensual | DPV-070 |
| P13 | Garras (mercado interno) | ARS/kg | Pelada/sin pelar; grado | Granel; congelado | Idem | Trimestral | DPV-077 |
| P14 | Carcasa-esqueleto | ARS/kg | Con/sin grasa | Granel; congelado | Idem | Mensual | DPV-070 |
| P15 | CMS (nacional e importada de Brasil) | ARS/kg o USD/t | Grasa, calcio, microbiología | Bloque congelado | Puesto en fábrica | Trimestral | DPV-071 |
| P16 | Recortes / carne industrial | ARS/kg | % grasa | Bloque | Idem | Trimestral | DPV-071 |
| P17 | Piel | ARS/kg | — | Bloque | Idem | Trimestral | DPV-071 |
| P18 | Grasa de pollo (alimentaria) | ARS/kg | — | Granel | Idem | Trimestral | DPV-075 |
| P19 | Milanesas, hamburguesas, nuggets, marinados (góndola y mayorista) | ARS/kg | Marca, formato | Envase de consumo | Precio de góndola y precio al proveedor | Mensual | DPV-079 |
| P20 | Materias primas para pet food (cuellos, carcasas, menudencias, patas) | ARS/kg | Apta / especificación | Congelado | Puesto en fábrica | Trimestral | DPV-073 |

### 8.2 Exportación

| # | Producto | Unidad | Calidad | Presentación | Condición | Frecuencia | Registro |
|---|---|---|---|---|---|---|---|
| X01 | Entero congelado (convencional y Halal) por destino | USD/t | Calibre | Caja 10 aves | FOB y CIF; plazo; derechos de exportación | Mensual | DPV-026 |
| X02 | Pechuga / filet IQF por destino (UE, Medio Oriente) | USD/t | Calibre, con/sin piel | IQF; bloque | FOB; cuota UE | Mensual | DPV-026, DPV-028 |
| X03 | Pata-muslo / cuartos traseros | USD/t | Con/sin espinazo | Bloque 15 kg; IQF | FOB | Mensual | DPV-026 |
| X04 | Muslo deshuesado (Japón) | USD/t o ¥/kg | ≥ 200 g, con piel | IQF | FOB/CIF | Mensual | DPV-026 |
| X05 | Alas por destino | USD/t | Tamaño | IQF | FOB | Mensual | DPV-026 |
| X06 | Garras grado A y segunda por destino (China, Vietnam, HK, Medio Oriente) | USD/t | Grado, calibre, pelado | Caja 10–20 kg | FOB / precio en planta de un trader | Mensual | DPV-026, DPV-077 |
| X07 | Menudencias (hígado, molleja, corazón, cuello) | USD/t | — | Bloque 10–15 kg | FOB | Trimestral | DPV-026 |
| X08 | CMS | USD/t | — | Bloque | FOB | Trimestral | DPV-026 |
| X09 | Costos de exportación (flete reefer, puerto, certificados, despachante, seguro) | USD/contenedor | — | Reefer 40' | Por ruta | Trimestral | DPV-027 |

### 8.3 Subproductos

| # | Producto | Unidad | Calidad | Presentación | Condición | Frecuencia | Registro |
|---|---|---|---|---|---|---|---|
| S01 | Pluma cruda húmeda | ARS/t (positivo, cero o negativo) | Frescura; humedad | Contenedor a granel | Retirada en planta; frecuencia | Trimestral | DPV-065 |
| S02 | Sangre cruda | ARS/t | Sin dilución; tiempo desde faena | Tanque | Retirada | Trimestral | DPV-080 |
| S03 | Vísceras (con contenido) | ARS/t | Frescura | Contenedor | Retirada | Trimestral | DPV-065 |
| S04 | Cabezas, huesos, residuo óseo, garras de descarte | ARS/t | — | Contenedor | Retirada | Trimestral | DPV-065 |
| S05 | Harina de plumas hidrolizada | ARS/t o USD/t | % proteína; digestibilidad | Granel; big-bag | Puesto en fábrica de alimento | Mensual | DPV-076 |
| S06 | Harina de subproductos avícolas / de vísceras | Idem | % proteína, grasa, ceniza | Idem | Idem | Mensual | DPV-076 |
| S07 | Harina de sangre | Idem | — | Idem | Idem | Trimestral | DPV-076 |
| S08 | Grasa avícola (rendering) | ARS/t | Acidez | Granel | Idem | Mensual | DPV-076 |
| S09 | Enmiendas / compost / harina de plumas como fertilizante | ARS/t | Registro | Granel | — | Semestral | DPV-066 |

### 8.4 Servicios y disposición

| # | Servicio | Unidad | Condición | Frecuencia | Registro |
|---|---|---|---|---|---|
| R01 | Retiro de subproductos por rendering (si cobra) | ARS/t o ARS/viaje | Distancia, frecuencia, contenedor | Trimestral | DPV-065 |
| R02 | Retiro y disposición de residuos no valorizables (contenido GI, decomisos, lodos) | ARS/t | Operador habilitado; manifiesto | Trimestral | DPV-072 |
| R03 | Incineración de decomisos (si corresponde) | ARS/t | — | Semestral | DPV-072 |
| R04 | Faena, trozado, deshuese o elaboración a façon | ARS/ave o ARS/kg | Qué incluye (subproductos, frío) | Trimestral | DPV-006, DPV-079 |
| R05 | Congelado y almacenamiento en frío de terceros | ARS/t/día | Temperatura | Trimestral | DPV-027 |
| R06 | Transporte refrigerado AMBA y planta–puerto | ARS/kg, ARS/viaje | — | Trimestral | DPV-042, DPV-027 |

---

## 9. Tareas de campo

Se agregan al listado maestro de información a obtener ([`../00_gestion_proyecto/datos_por_validar.md`](../00_gestion_proyecto/datos_por_validar.md), DPV-070 a DPV-081). **No** es el cuestionario final para inversores.

| # | Actor | Qué preguntar | Registro |
|---|---|---|---|
| F1 | **Mayoristas y distribuidores** (3–5) | Precio y volumen semanal por parte (alas, menudencias, cuello, carcasa, garras); qué parte cuesta más colocar; presentación y frío; plazo de pago; proveedores actuales | DPV-070, DPV-040 |
| F2 | **Frigoríficos avícolas** (2–3; incluye posibles plantas a façon) | Destino real de cada parte (carcasa, CMS, piel, garras, plumas, sangre, vísceras); quién retira sus subproductos y en qué condiciones; si pelan y exportan garras; rendimientos reales | DPV-065, DPV-060, DPV-006 |
| F3 | **Exportadores** | Qué partes exportan y a dónde; si compran producto de terceros para completar contenedores; especificación de garras y menudencias; lote mínimo | DPV-081, DPV-032 |
| F4 | **Traders** (garras, menudencias, CMS) | Precio en planta o FOB por grado; calibre; si compran volúmenes chicos; destinos alternativos a China; plazo y forma de pago | DPV-077, DPV-081 |
| F5 | **Plantas de rendering** (zonas candidatas) | Qué materiales reciben; pagan/retiran gratis/cobran; frecuencia y distancia máxima; contenedores; requisitos de frescura y separación (sangre sin agua, plumas escurridas); si aceptan decomisos y contenido; qué harinas venden y a qué precio | DPV-065, DPV-076 |
| F6 | **Fabricantes de pet food** | Qué materias primas avícolas compran (crudas congeladas, harinas); especificación; requisitos de habilitación del proveedor; volumen y precio; treats | DPV-073 |
| F7 | **Supermercados** (red y otros) | Qué menudencias y cortes secundarios venden; con o sin menudencias en el entero; elaborados de pollo que venden y de quién; vida útil remanente exigida | DPV-037, DPV-041, DPV-078 |
| F8 | **Industria de elaborados y chacinados** | Uso de CMS (origen, precio, especificación, temperatura); compra de recortes, piel, muslo deshuesado; interés en proveedor local; elaboración a façon | DPV-071, DPV-079 |
| F9 | **SENASA / organismos provinciales** | Texto vigente de Res. 368/2003, 1389/2004, 1415/2024, 1416/2024, Decreto 4238 (digestor, grasería); destino permitido de decomisos; compostaje y biodigestión | DPV-066, DPV-074 |
| F10 | **Operadores de residuos** | Tarifas de retiro y disposición de residuos orgánicos no valorizables; habilitaciones | DPV-072 |

---

## 10. Riesgos de valorización

| Riesgo | Efecto | Mitigación conceptual |
|---|---|---|
| **Subproductos sin comprador** | 15–26 % del PV pasa de ingreso a costo | Relevar receptores antes de elegir localización (DEC-003, DEC-027) |
| **Dependencia de un único receptor de rendering** | Si deja de retirar, la faena se detiene | Dos receptores o plan de contingencia (almacenamiento, compost) |
| **China cerrada** | Las garras y alas pierden su mejor destino | No invertir en pelado/clasificación sin comprador; diseño que preserve la opción (DEC-031) |
| **Carcasa sin salida** | 13,6 % del PV (4,1 t/día a 10.000 aves) a rendering | Validar compradores de carcasa y CMS (DEC-029) |
| **CMS de uso restringido** | Mercado limitado a chacinados cocidos | Verificar normativa (DPV-074); no asumir usos en productos crudos |
| **Desbalance de partes** | Excedentes de pata-muslo, alas, menudencias si el canal principal es el supermercado | Canales para cada parte antes de dimensionar |
| **Perecibilidad** | Menudencias, sangre, vísceras y CMS se deterioran en horas o días | Frío, retiro diario, congelado |
| **Escala insuficiente** | Contenedores de garras o menudencias tardan meses; rendering propio inviable | Consolidar con terceros |
| **Precios débiles** | Decisiones sobre precios de sitios comerciales | Solo precios de compradores reales (SUP-018) |
| **Doble conteo** | Sumar rutas incompatibles infla el ingreso por ave | 15 incompatibilidades ([`rutas_valorizacion.md` §3](rutas_valorizacion.md)); tests S04–S05 |
| **Normativa no verificada** | Rutas que parecen posibles pueden no estar permitidas (decomisos, pet food, compost) | Verificación documental primaria (DPV-009, DPV-066) |
| **Olores y vecindad** | Rendering o acopio de subproductos condicionan la localización | Evaluar en `10_localizacion` y `11_agua_efluentes` |

---

## 11. Archivos creados y modificados

**Creados:** `06_productos/catalogo_productos.md`, `06_productos/elaborados.md`, `06_productos/matriz_productos.csv`, `07_subproductos/mapa_subproductos.md`, `07_subproductos/rendering.md`, `07_subproductos/rutas_valorizacion.md`, `07_subproductos/matriz_valorizacion.csv`, `07_subproductos/escenarios_subproductos.csv`, `07_subproductos/modelo_subproductos.py`, `07_subproductos/guia_ramiro.md`, `07_subproductos/conclusiones_valorizacion.md`.
**Modificados:** `06_productos/README.md`, `07_subproductos/README.md` (documentación de modelo y CSV, regla 15); `00_gestion_proyecto/supuestos.md` (SUP-046 a SUP-051), `datos_por_validar.md` (DPV-070 a DPV-081; notas en DPV-013, DPV-064, DPV-065, DPV-066, DPV-067), `decisiones_pendientes.md` (DEC-029 a DEC-032; notas en DEC-005 y DEC-027), `estado_proyecto.md`, `glosario.md`; `25_fuentes/registro_fuentes.csv` (FTE-185 a FTE-193), `25_fuentes/bibliografia.md`. **Sin cambios:** `04_balance_masa/` (balance v1.1).

## 12. Control de calidad

- [x] Base: balance de masa v1.1, **sin modificar** (test S01: 21/21).
- [x] kg/ave trazables al modelo: 59 valores de las dos matrices verificados contra el balance (test S08).
- [x] Cierre por variante: Σ grupos = PV + agua incorporada (S02, error ≤ 2 × 10⁻¹⁵ kg/ave); cada componente en un solo grupo (S03).
- [x] Rutas incompatibles no sumadas (S04, S05, S09) y 15 incompatibilidades documentadas.
- [x] Sin precios definitivos; los precios citados son referencias `[PVDP · débil]` ya registradas y marcadas "no usar para calcular".
- [x] Mercado potencial no tratado como venta; subproducto no tratado como ingreso sin comprador (SUP-046).
- [x] Valorización técnica separada de la económica (IAA técnico vs económico; cuatro etapas en `rutas_valorizacion.md` §4).
- [x] Todo material con destino conceptual, incluidas salidas fuera del balance (MAT-37 a MAT-39).
- [x] Datos débiles marcados: normativa en extractos, vida útil sin fuente comercial, rendimiento de CMS, garras, rendering.
- [ ] Verificación documental primaria de la normativa (bloqueada, DPV-009).
- [ ] Precios y compradores reales (tareas de campo §9).

## 13. Evaluación de calidad

**MEDIA** como mapa y método: inventario completo, clasificación condicional, rutas exclusivas verificadas por código, escalado trazable al balance y lista de precios y tareas accionable. **BAJA** como evidencia comercial y normativa: ningún comprador identificado, ningún precio utilizable, normativa leída solo en extractos y vida útil sin datos propios. Sirve para **ordenar la investigación de campo y las decisiones**, no para calcular ingresos ni elegir rutas.
