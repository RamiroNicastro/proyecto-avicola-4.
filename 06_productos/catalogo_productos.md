# Catálogo conceptual de productos comestibles

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance:** qué productos comestibles pueden obtenerse del ave, con qué nivel de proceso, frío, vida útil y canal potencial, y cómo se conecta cada parte con los mercados de exportación. **No** se define el portafolio (DEC-005), **no** se asignan precios (SUP-018), **no** se afirma demanda: toda demanda del proyecto es **no validada** (categorías C/D, [`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md)).
> **Archivo maestro de atributos:** [`matriz_productos.csv`](matriz_productos.csv) (30 productos; kg/ave verificados contra el balance v1.1 por el test S08 de [`../07_subproductos/modelo_subproductos.py`](../07_subproductos/modelo_subproductos.py)). Este documento es la lectura analítica. Inventario completo de salidas (incluye subproductos): [`../07_subproductos/mapa_subproductos.md` §1](../07_subproductos/mapa_subproductos.md). Elaborados: [`elaborados.md`](elaborados.md).
> **Base:** pollo de 2,9 kg vivo, rendimiento medio, inmersión (masa biológica; el agua retenida se vende con el producto pero no es carne, SUP-042).

**Escala de nivel de procesamiento** (usada en la matriz): **1** faena, enfriado y empaque a granel · **2** trozado, bandeja o congelado simple · **3** deshuese, pelado/clasificación o separación mecánica · **4** transformación en frío (rebozado crudo, formado, armado) · **5** proceso térmico (cocción, prefritura).

**Vida útil:** categorías cualitativas (SUP-051). Refrigerado = **días**, a determinar por estudio de vida útil según envase (bandeja, atmósfera modificada, vacío) y exigencia de vida útil remanente del cliente (DPV-078, DPV-041). Congelado = **meses** (orientativo: entero hasta 12, trozos hasta 9, menudencias 3–4, guía doméstica FTE-189 `[PVDP]`). CMS refrigerada = **12 horas** (Res. SENASA 368/2003, FTE-185 `[PVDP]`).

---

## 1. Productos para el mercado interno

"Valor agregado relativo" ordena productos **entre sí** por transformación incorporada, **no** por margen: un producto con más proceso puede ganar menos si el proceso cuesta más que la diferencia de precio ([`../07_subproductos/guia_ramiro.md` §7](../07_subproductos/guia_ramiro.md)).

| Producto | Nivel | Mano de obra | Frío | Packaging | Vida útil | Complejidad | Valor agregado relativo | Canales potenciales (no validados) |
|---|---|---|---|---|---|---|---|---|
| **Pollo entero** | 1–2 | Baja | Refr. / cong. | Bolsa, bandeja o cajón | Días / meses | Baja | Bajo | Supermercados, carnicerías, pollerías, mayoristas |
| **Pollo trozado** (cuartos, bandeja mixta) | 2 | Baja–media | Refr. | Bandeja con film | Días | Media | Bajo–medio | Supermercados, carnicerías |
| **Pechuga** con hueso | 2 | Media | Refr. / cong. | Bandeja o granel | Días / meses | Media | Medio | Supermercados, carnicerías, gastronomía |
| **Suprema** | 3 | Alta (deshuese) | Refr. / IQF | Bandeja; IQF | Días / meses | Media–alta | Alto | Supermercados, gastronomía, industria |
| **Pata-muslo** | 2 | Baja | Refr. / cong. | Bandeja o granel | Días / meses | Baja | Bajo | Supermercados, carnicerías, mayoristas, catering |
| **Alas** | 2 | Baja–media | Refr. / cong. | Bandeja; IQF | Días / meses | Media (clasificación) | Medio | Gastronomía, mayoristas |
| **Menudencias** (hígado, corazón, molleja; cuello aparte) | 1–2 | Baja (molleja: media) | Refr. (muy perecederas) / cong. | Bolsita, bandeja, bloque | Días cortos / 3–4 meses | Baja–media | Bajo | Carnicerías, pollerías, mayoristas, pet food |
| **Milanesas** | 4 | Alta | Refr. / cong. | Bandeja; bolsa | Días / meses | Alta | Alto | Supermercados, carnicerías, gastronomía |
| **Hamburguesas / medallones** | 4 | Media–alta | Cong. | Caja, estuche | Meses | Alta | Medio–alto | Supermercados, gastronomía, institucional |
| **Nuggets / rebozados precocidos** | 5 | Alta | Cong. | Bolsa, estuche | Meses | Muy alta | Alto | Supermercados, gastronomía, cadenas |
| **Marinados** | 3 | Media | Refr. / cong. | Bandeja sellada, vacío | Días (según envase) | Media | Medio | Supermercados, gastronomía |
| **Listos para cocinar** (brochetas, arrollados, rellenos) | 4 | Alta | Refr. | Bandeja sellada | Días | Alta | Alto | Supermercados, carnicería propia |
| Otros: carcasa para caldo, cuello, garras (mercado interno), recortes, CMS, piel | 1–3 | Baja | Refr. / cong. | Granel, bloque | Días / meses (CMS: horas) | Baja–media | Bajo | Mayoristas, industria, pet food |

**Lecturas:**

1. Los productos de **nivel 1–2** (entero, trozado, pata-muslo) son de baja complejidad pero compiten en precio en un mercado maduro con sobreoferta periódica ([`../01_mercado/conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md)).
2. Los de **nivel 3–5** agregan transformación pero exigen mano de obra, frío, envases y habilitaciones adicionales; su demanda por el proyecto es **desconocida** (DPV-037, DPV-040, DPV-079).
3. **Pechuga y suprema** pueden tener su mejor destino en el mercado interno (Argentina importa pechuga de Brasil, FTE-075 `[ESTIMACIÓN]`); la **pata-muslo**, las **alas** y las **menudencias** son las partes con mayor riesgo de excedente si el canal principal es el supermercado ([`../02_clientes_demanda/canales_comerciales.md` §2](../02_clientes_demanda/canales_comerciales.md)).

---

## 2. Parte del ave → producto → mercado de exportación

Resumen para **conectar** partes con mercados; la investigación está en [`../17_exportacion/`](../17_exportacion/README.md) y no se repite. Categorías de acceso A/B/C/D (regla 17): ningún destino es hoy una venta del proyecto (exportación = 0 kg/día en los escenarios, SUP-022).

| Parte (kg/ave) | Producto exportable | Mercados potenciales | Congelado / refrigerado | Requisitos y certificación | Dependencia | Riesgos |
|---|---|---|---|---|---|---|
| Carcasa entera (1,914) | **Entero congelado** (griller calibrado) | Golfo (Arabia Saudita, EAU, Qatar), Irak, Egipto, África, Chile | Congelado | Listado SENASA por destino; calibración de peso; **Halal** reconocido para Golfo (requisitos de faena por verificar, DPV-034) | Media (Golfo exige Halal) | Brasil fija precio (FOB 1.569–2.316 USD/t según destino, FTE-119 `[PVDP · débil]`); IAAP |
| Pechuga (0,784) → suprema (0,478) + solomillo (0,118) | **Pechuga/filet** IQF o bloque | UE (cuota UE–Mercosur), Reino Unido, Medio Oriente (shawarma), Chile | Congelado (refrigerado solo regional) | UE: listado, antimicrobianos, *Salmonella*, bienestar, cuota (DPV-028); Golfo: Halal | Media | Precio volátil (mínimo 2.700 USD/t CIF may-2025, FTE-118 `[PVDP]`) |
| Pata-muslo (0,631) | **Pata-muslo / cuartos traseros** | Vietnam, Chile, África, México, Filipinas; China (no disponible) | Congelado | Listado; aranceles (Sudáfrica 62 % a cortes con hueso, FTE-128 `[PVDP]`) | Baja–media | Techo bajo (cuartos EE.UU. ~1.100–1.200 USD/t, FTE-120 `[PVDP]`); cobro en África |
| Muslo (0,366) → deshuesado (0,242) | **Muslo deshuesado** calibrado | **Japón** (reabierto 2026), Corea | Congelado | Especificación japonesa (≥ 200 g, piel); listado MAFF | **Alta** (Japón) | Exigencia de calidad; competencia de Brasil/Tailandia |
| Alas (0,208) | **Alas** enteras o trozadas | Hong Kong, Vietnam, Filipinas; China (no disponible) | Congelado | Clasificación por tamaño | **Alta** (Asia) | Mejor destino cerrado |
| Patas (0,113) → garras (0,101) | **Garras** grado A / segunda | China (**no disponible confirmado**, SUP-016), Vietnam, Hong Kong; segunda a Medio Oriente | Congelado | Registro GACC para China; pelado y clasificación | **Muy alta** (China) | Ver §3 |
| Hígado, corazón, molleja, cuello (0,184) | **Menudencias** en bloque | Sudáfrica, RD Congo, Angola, Ghana; China | Congelado | Listado | Media | Flete alto sobre precio bajo (300–800 USD/t, FTE-137 `[PVDP · débil]`); cobro |
| Carcasa-esqueleto → CMS (0,236) | **CMS** en bloque | Filipinas, Sudáfrica, México | Congelado | Microbiología; listado | Media | Precio bajo (Brasil FOB 400–600 USD/t, FTE-137 `[PVDP · débil]`) |
| Cualquier parte | **Halal** (variante de certificación) | Golfo, Malasia, Indonesia | Congelado | Certificadora reconocida por destino (DPV-030, DPV-034) | Alta | No se diseña línea sin aturdimiento (DEC-012) |
| Pechuga, muslo, recortes | **Cocidos / marinados** | Japón, UE, Reino Unido (largo plazo) | Congelado | Registro de planta de proceso; pueden tener menos restricciones por IAAP (a verificar) | Media | Otra escala industrial; competencia de Tailandia/China |

**Regla de asignación:** una parte va a exportación solo si su net-back sostenido y ajustado por riesgo supera al del mercado interno (SUP-017; fórmula en [`../17_exportacion/estrategia_valorizacion_ave.md` §1](../17_exportacion/estrategia_valorizacion_ave.md)). **Cada parte necesita al menos dos salidas.**

---

## 3. Garras / patas

### 3.1 De la pata a la garra (2,9 kg, medio)

```
PATA BRUTA 0,113 kg/ave
 ├─ decomiso (patas de aves decomisadas) ........ 0,001  → D
 ├─ cutícula y suciedad (escaldado y pelado) ..... 0,006  → D (efluente/lodos)
 └─ patas peladas 0,106
      ├─ GRADO A .................................. 0,085  → B (≈ 43 g por pieza)
      ├─ SEGUNDA .................................. 0,016  → B
      └─ DESCARTE ................................. 0,005  → C (rendering)
```

Identidad verificada por el test T15 del balance ([`../04_balance_masa/auditoria_balance.md` §4](../04_balance_masa/auditoria_balance.md)). Grados según escenario de calidad: A 60–90 %, segunda 8–25 %, descarte 2–15 % (SUP-041).

### 3.2 Especificación y proceso

| Aspecto | Contenido | Fuente / estado |
|---|---|---|
| **Grado A** | Piel blanca, sin huesos rotos, sin hematomas, sin cutícula amarilla, sin almohadilla negra ni quemaduras de amoníaco | Ofertas comerciales (FTE-176 `[PVDP · débil]`); especificación real del comprador pendiente (DPV-064) |
| **Segunda** | Lesiones leves; mercados menos exigentes | Idem |
| **Descarte** | Fracturas, lesiones graves, contaminación → rendering | Modelo |
| **Calibre** | 35–50 g por pieza, 12–15 cm (FTE-176, débil). Modelo: ~43 g a 2,9 kg; **~34 g a 2,2 kg** (límite inferior: aves livianas pueden no cumplir) | DEC-021 |
| **Limpieza / escaldado / pelado** | Escaldado específico y pelado mecánico de la cutícula; sin uñas según comprador | Proceso a relevar; rendimiento de pelado supuesto (5 % de merma, SUP-040) |
| **Lavado y enfriado** | Lavado, enfriado rápido | — |
| **Congelado** | Túnel o IQF; −18 °C o menos | Exportación exige congelado |
| **Packaging** | Caja de 10–20 kg, bloque o IQF en bolsa; rotulado por destino | [`../17_exportacion/productos_exportables.md` §1](../17_exportacion/productos_exportables.md) |
| **Calidad en granja** | La **pododermatitis** (cama húmeda), las quemaduras de amoníaco y los golpes de captura definen el grado **antes** de la planta | FTE-175 `[PVDP]`; DPV-044 |

### 3.3 Mercados y dependencia de China

| Destino | Estado | Comentario |
|---|---|---|
| **China** | **No disponible confirmado** (SUP-016, DPV-035). Reapertura por anuncio GACC 38/2025 del 2025-03-17, que incluía subproductos; eventos posteriores de IAAP; en jul-2026 el sector reclamaba la reapertura plena (FTE-014, FTE-191 `[PVDP]`) | Históricamente el mejor pagador: China representaba ~45 % de las exportaciones del sector, con garras y alas como productos destacados (FTE-191, prensa) |
| Vietnam, Hong Kong | Acceso y precio a verificar (DPV-031) | Hong Kong puede actuar como reexportador a China: riesgo regulatorio |
| Medio Oriente (segunda) | Cotización argentina de ~1.500 USD/t, fecha incierta (FTE-136 `[PVDP · débil]`) | No usar como base |
| Mercado interno | Demanda no relevada (sopas, gastronomía asiática, treats para mascotas) | Probablemente pequeño y de bajo precio (DPV-077) |
| Harina (rendering) | Piso de valor | Garra = harina de subproductos |

**Precios:** los ~3.100–3.500 USD/t CIF de importación china (FTE-089) y las cotizaciones argentinas de 1.050–2.800 USD/t (FTE-136, débiles) **no se usan** como base de rentabilidad (SUP-018).

### 3.4 Si China está cerrada

1. **No pelar ni clasificar para exportación** sin comprador: el pelado agrega costo (agua caliente, equipo, mano de obra) que solo se recupera con un precio de garra pelada.
2. Alternativas en orden de valor potencial (a validar): Vietnam/Hong Kong vía trader → mercado interno → pet food (patas crudas o deshidratadas) → rendering.
3. **Escala:** a 10.000 aves/día se llena un reefer de 25 t de garras grado A cada ~29 días de faena; a 2.500 aves/día, cada ~118 días (≈ 6 meses) ([`../07_subproductos/escenarios_subproductos.csv`](../07_subproductos/escenarios_subproductos.csv), fila D07). A baja escala la exportación de garras requiere **consolidar con terceros** (trader o frigorífico exportador) o acumular stock congelado (capital de trabajo y cámara).
4. La **opción** vale: diseñar para poder pelar, clasificar y congelar garras más adelante sin comprometer esa inversión hoy (DEC-031).

---

## 4. Menudencias

| | Hígado (0,055 kg/ave) | Corazón (0,014) | Molleja (0,040) | Cuello (0,075) |
|---|---|---|---|---|
| **Mercado interno** | Carnicerías, pollerías, mayoristas; vendido suelto o en bolsita de menudencias | Con menudencias; brochetas (gastronomía) | Carnicerías, mayoristas | Carnicerías, mayoristas; "cogote" para caldo |
| **Industria** | Paté, embutidos (a relevar) | Marginal | Marginal | CMS (ruta excluyente con venta) |
| **Pet food** | Materia prima apta cruda o congelada (si proviene de faena inspeccionada; DPV-073) | Idem; treats | Idem | Idem; treats deshidratados |
| **Exportación** | África, China (bloque congelado) | Con menudencias | África, Asia | África (con menudencias) |
| **Frío** | Refrigerado de vida muy corta o congelado rápido | Idem | Idem | Refrigerado o congelado |
| **Packaging** | Bolsita (dentro o fuera del entero), bandeja, bloque 10–15 kg | Idem | Idem | Granel, bloque |
| **Proceso** | Separación, recorte de vesícula, lavado | Separación | Apertura, vaciado y pelado de cutícula (mano de obra o equipo) | Corte |
| **Nivel de valor (relativo)** | BAJO | BAJO (masa mínima) | BAJO | BAJO |

- **Definir siempre si "menudencias" incluye el cuello** (0,110 vs 0,185 kg/ave; DPV-068).
- En el pollo entero, las menudencias pueden venderse **dentro** del ave o aparte: el modelo las vende aparte (SUP-043).
- Son partes de **bajo precio por kg y alta perecibilidad**: si no hay canal diario, conviene congelarlas y el flete pesa mucho sobre su precio.

---

## 5. CMS (carne mecánicamente separada)

| Aspecto | Contenido |
|---|---|
| **Definición** | Producto de la separación y remoción por medios mecánicos del músculo esquelético y otros tejidos adheridos a carcasas y partes de carcasas de aves (Res. SENASA 368/2003, incorporada al Decreto 4238/68, FTE-185 `[PVDP]`) |
| **Diferencia con carne deshuesada convencional** | La **carne deshuesada** (suprema, muslo deshuesado, recortes) se obtiene con cuchillo o máquina de deshuese que **conserva la estructura muscular**; es un corte vendible al consumidor. La **CMS** es una **pasta** obtenida presionando huesos con carne adherida contra un tamiz: estructura muscular destruida, más contenido de médula, calcio y fragmentos óseos microscópicos, más grasa y mayor carga microbiana potencial. **No es un corte** y tiene uso restringido |
| **Aplicaciones permitidas** | **Solo como ingrediente de chacinados cocidos y conservas** según el extracto de la Res. 368/2003 (FTE-185 `[PVDP]`) — p. ej. salchichas, fiambres cocidos. SUP-048: hasta verificar el texto, no se asume su uso en hamburguesas crudas, milanesas ni venta directa al consumidor |
| **Restricciones** | Uso restringido por norma; posible límite de calcio/hueso y rotulado (a verificar, DPV-074); no para productos crudos |
| **Requisitos sanitarios y frío** | Si no se usa de inmediato: refrigerada entre **−2 y 2 °C y utilizada dentro de las 12 horas** de producida, o **congelada a −18 °C** en el centro en un proceso de **no más de 6 horas**, y mantenida a esa temperatura (FTE-185 `[PVDP]`) |
| **Vida útil** | Horas (refrigerada); meses (congelada) |
| **Materia prima** | Carcasa-esqueleto (0,393 kg/ave → 0,236 de CMS al 60 %), cuello (0,075 → 0,045), hueso de pechuga en config. C (0,102 → 0,061). Rendimiento 55–65 % supuesto (SUP-039; fuente débil FTE-180) |
| **Mercados** | Industria cárnica local (hoy se importa CMS de Brasil, [`../17_exportacion/estrategia_valorizacion_ave.md` §5](../17_exportacion/estrategia_valorizacion_ave.md)); exportación a Filipinas, Sudáfrica, México (potencial) |
| **Valor relativo** | BAJO por kg; su interés es dar salida a la carcasa-esqueleto si no se vende como tal |
| **Ruta** | **Excluyente** con vender la carcasa-esqueleto o el cuello (SUP-045; tests T16–T17 del balance y S04) |

Comparación de rutas de la carcasa en [`../07_subproductos/rutas_valorizacion.md` §1](../07_subproductos/rutas_valorizacion.md).
