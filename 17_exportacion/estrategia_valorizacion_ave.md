# Estrategia de valorización por parte del ave — ingreso total por ave

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 (conceptual) · Base: [`productos_exportables.md`](productos_exportables.md), [`mercados_por_pais.md`](mercados_por_pais.md)
Antecedente: [`01_mercado/exportaciones.md` §7](../01_mercado/exportaciones.md) (introducción conceptual; este documento la desarrolla y la reemplaza como referencia).

> **Principio estratégico** (`CLAUDE.md`, SUP-013): maximizar el **ingreso total por ave**, asignando cada parte al mercado que mejor la paga **en términos netos**.
> **Alcance:** conceptual. No se usan rendimientos por parte (dependen de genética, peso de faena y especificación: DPV-008, `04_balance_masa`) ni se fija capacidad (regla 9). Los precios citados son `[PVDP]` o `[PVDP · débil]`: sirven para ordenar, no para calcular.
> **Precios:** todos los precios de este documento son **preliminares** (fuentes comerciales, estimaciones o mercados distintos). **No se usan para calcular rentabilidad** (SUP-018); en particular, no los ~3.500 USD/t de garras. La cuantificación se hará con precios FOB reales y cotizaciones comerciales (DPV-026, DPV-032).
> **No se elige** un destino por parte; se describen los mercados que suelen valorizar mejor cada parte y las condiciones para acceder.

---

## 1. Fórmula

```
Ingreso total por ave = Σ_i  k_i × max_j ( NB_ij )     sujeto a restricciones (§3)

  k_i   = kg de la parte i por ave (rendimiento; se obtendrá en 04_balance_masa)
  NB_ij = precio neto ("net-back") de la parte i en el mercado j, en USD/kg, puesto en planta
```

**Net-back de exportación** (por kg, puesto en planta):

```
NB_exp = Precio FOB
         − derechos de exportación (hoy 5 % sobre FOB según prensa: FTE-056; a verificar, DPV-015)
         − transporte refrigerado planta → puerto, gastos de terminal, despachante, certificados (SENASA, Halal)
         − costo incremental de proceso, empaque de exportación y congelado vs. el producto local
         − costo financiero: (días desde faena hasta cobro) × tasa × precio
         − mermas, reclamos y descuentos por calidad (provisión)
Si el precio es CIF/CFR: restar además flete marítimo y seguro.
```

**Net-back local** (por kg, puesto en planta):

```
NB_loc = Precio al cliente sin IVA
         − distribución refrigerada, bonificaciones y promociones del canal
         − costo financiero del plazo de pago del cliente (ej.: supermercados)
         − mermas y devoluciones
```

**Regla de asignación:** una parte va a exportación solo si `NB_exp > NB_loc` **de manera sostenida** y ajustada por riesgo (cierres sanitarios, cobro). No alcanza con que el precio FOB en USD/t sea mayor que el precio local.

---

## 2. Qué cambia respecto de "vender el pollo entero"

1. **Productos conjuntos:** cada ave da una cantidad fija de pechuga, pata-muslo, alas, garras y menudencias. No se puede producir más garras sin producir más pechuga. La empresa no elige *cuánto* de cada parte, sino *a qué mercado* va cada una y **si troza o no**.
2. **Decisión entero vs trozado** (por ave): trozar conviene si `Σ_i k_i × NB_i − costo de trozado y empaque > k_entero × NB_entero`.
3. **Partes que más ganan con la exportación:** las que valen poco en el mercado interno (garras, alas en ciertos momentos, menudencias, pata-muslo en sobreoferta). **Partes que pueden valer más en el mercado interno:** la pechuga (Argentina la importa de Brasil a ~2.660 USD/t promedio de importación, ago-2025, FTE-075 `[ESTIMACIÓN]`) y los elaborados.
4. **Sin salida, una parte no vale cero: vale lo que pague el rendering** (harina) o incluso cuesta disponerla. La exportación sube el "piso" de esas partes.

---

## 3. Restricciones que condicionan la asignación

| Restricción | Efecto | Documento |
|---|---|---|
| **Habilitación sanitaria del destino** (país y planta listada) | Sin listado, el net-back de ese destino no existe | [`mercados_por_pais.md`](mercados_por_pais.md), [`requisitos_planta_exportadora.md`](requisitos_planta_exportadora.md) |
| **Lote mínimo = contenedor** (~24–27 t de congelado por reefer de 40', `[PVDP · débil]`) | Días para completar un contenedor de la parte i: `D_i = carga del contenedor / (k_i × aves faenadas por día)`. Las partes de bajo peso por ave (garras, menudencias) requieren **mucha escala o mucha acumulación** en cámara (capital de trabajo, espacio de frío) | [`logistica_exportacion.md`](logistica_exportacion.md); se cuantificará en `04_balance_masa` |
| Especificación del comprador | Calibre, pelado y clasificación de garras, deshuese japonés, piel, grasa, peso del "griller" | [`productos_exportables.md`](productos_exportables.md) |
| Halal | Para Golfo e Irak se requiere certificación Halal reconocida; requisitos de faena (aturdimiento, métodos) por verificar (DPV-034) | [`mercados_por_pais.md` §4](mercados_por_pais.md) |
| Capacidad de congelado y almacenamiento | Exportar exige congelar (túnel/IQF) y estoquear hasta completar lotes | [`requisitos_planta_exportadora.md`](requisitos_planta_exportadora.md) |
| Cuotas y aranceles | UE fuera de cuota: prohibitivo; Sudáfrica: 62 % para cortes con hueso | [`mercados_por_pais.md` §5](mercados_por_pais.md) |
| Riesgo sanitario | Un brote cierra los destinos que exigen país libre; la parte debe tener **salida alternativa** | [`conclusiones_exportacion.md` §5](conclusiones_exportacion.md) |
| Capital de trabajo | Exportación: faena → embarque → tránsito (20–45 días) → cobro | [`logistica_exportacion.md`](logistica_exportacion.md) |

---

## 4. Matriz de valorización por producto

Rangos de precio **preliminares**: ver [`productos_exportables.md` §2](productos_exportables.md) (bases y fechas distintas; **no comparables entre filas como si fueran equivalentes**). "Volumen potencial" = profundidad del mercado para un proveedor nuevo (no escala del proyecto).

| Producto | Mercados relevantes | Rango de precio disponible (referencia) | Requisitos | Riesgo | Volumen potencial | Comentarios |
|---|---|---|---|---|---|---|
| **Pechuga / filet** | Mercado interno (supermercados, gastronomía, industria; sustitución de importaciones de Brasil); UE (cuota); Medio Oriente (shawarma); Reino Unido; Chile | CIF Medio Oriente 2.700 USD/t (mínimo, may-2025); mayorista UE 6,26 €/kg (jul-2026); importación argentina ~2.660 USD/t | Deshuese, calibrado, IQF; UE: listado, antimicrobianos, cuota; Golfo: Halal | Medio: competencia de Brasil en todos los destinos, incluido el mercado argentino | Alto (mercado interno y UE) | **El mercado interno puede ser su mejor destino.** Exportarla tiene sentido si la cuota UE o Medio Oriente dan un net-back mayor |
| **Pata-muslo con hueso** | Mercado interno; Vietnam; Chile; África; China (cerrada) | Referencia de cuartos de EE.UU. ~1.100–1.200 USD/t (2024) | Congelado; especificación simple | Alto en precio: EE.UU. fija un techo bajo | Alto | Parte "de volumen": exportarla sirve para descomprimir el mercado interno en sobreoferta, no para ganar margen |
| **Muslo deshuesado** | **Japón**, Corea; gastronomía local | ¥370–650/kg mayorista en Japón (2025–2026) | Especificación japonesa; mano de obra de deshuese; listado MAFF | Medio: exigencia de calidad; competencia de Brasil y Tailandia | Medio | Transforma una parte de valor medio en una de mayor valor; requiere proceso adicional |
| **Cuartos traseros** | México, Angola, Vietnam, Filipinas, Cuba, África | ~1.100–1.200 USD/t (EE.UU., 2024) | Congelado | Alto en precio y cobro (África) | Alto | Alternativa al trozado fino cuando no hay mejor salida |
| **Alas** | Mercado interno (gastronomía); China y Hong Kong; Vietnam | Sin dato confiable | Clasificación por tamaño | Alto: el mejor destino (China) está cerrado | Medio | Revisar net-back local vs Asia caso por caso |
| **Garras** | **China** (no disponible confirmado; DPV-035); Hong Kong; Vietnam; 2ª calidad a Medio Oriente | Preliminar: China ~3.100–3.500 USD/t CIF (2025); cotizaciones argentinas 1.050–2.800 USD/t (débiles) | Pelado, sin callos, clasificación por grado; registro GACC; calidad de cama y bienestar en granja (lesiones plantares) | **Muy alto:** dependencia de un solo país; cierre prolongado | Bajo en kg por ave; alto en valor por kg si China abre | Mayor diferencia de valor por destino de toda el ave. **Sin China, su valor cae a destinos alternativos o a harina** |
| **Menudencias** | Mercado interno (carnicerías); África; China | 300–800 USD/t (ofertas comerciales, débiles) | Congelado en bloque | Medio: flete pesa mucho sobre un precio bajo; cobro en África | Medio | Exportar solo si el mercado interno no absorbe o paga menos que el net-back africano |
| **Pollo entero** | Mercado interno (supermercados, carnicería, "producto gancho"); Chile; Golfo (Halal); Irak; África | Brasil FOB 1.569–2.316 USD/t según destino (mar-2025) | Calibración de peso; Halal para Golfo | Medio: commodity; Brasil fija precio | Alto | Es la forma de venta que **menos** valoriza las partes; útil como regulador de volumen y para clientes que lo exigen |
| **CMS / recortes** | Industria local de elaborados (hoy se importa CMS de Brasil); Filipinas; Sudáfrica | Brasil FOB 400–600 USD/t (débil) | Separadora mecánica; microbiología | Bajo en precio | Medio | Probablemente mejor destino local (sustitución de importaciones), a validar |
| **Cocidos / procesados** | Mercado interno; Japón, UK, UE (a largo plazo) | Tailandia ~3.270 USD/t promedio (2025, débil) | Planta de proceso y listados específicos | Medio–alto: otra escala industrial y competencia de Tailandia y China | Bajo al inicio | Opción de largo plazo. Pueden tener menos restricciones sanitarias por IAAP (a verificar) |
| **Subproductos (harinas de plumas y vísceras, grasa)** | Alimento balanceado local; acuicultura (Chile, Asia) | 350–650 USD/t (débil) | Planta de rendering habilitada | Bajo | Medio | Piso de valor de toda parte sin mejor destino; también resuelve efluentes y residuos |

---

## 5. Mapa conceptual de asignación (ilustrativo, no es una selección)

```
                                   ┌─ Mercado interno (supermercados, gastronomía, industria)  ← sustitución de importaciones
PECHUGA ───────────────────────────┼─ UE (cuota UE–Mercosur)          [acceso legal vigente; competitividad a demostrar]
                                   └─ Medio Oriente (Halal)            [precio volátil]

PATA-MUSLO ────────────────────────┬─ Mercado interno
                                   ├─ Vietnam / Chile / África          [precio techo EE.UU.]
                                   └─ Japón (deshuesado)               [reabierto 2026-09-08; especificación]

ALAS ──────────────────────────────┬─ Mercado interno (gastronomía)
                                   └─ Asia (Hong Kong, Vietnam; China cerrada)

GARRAS ────────────────────────────┬─ China                             [NO DISPONIBLE CONFIRMADO: opción, no base]
                                   ├─ Vietnam / Hong Kong               [a verificar precio y acceso]
                                   └─ Harina (piso)

MENUDENCIAS ───────────────────────┬─ Mercado interno (carnicerías)
                                   └─ África                            [riesgo de cobro]

POLLO ENTERO ──────────────────────┬─ Mercado interno (supermercados, carnicería familiar)
                                   └─ Chile / Golfo (Halal) / Irak

CMS / RECORTES ────────────────────── Industria local de elaborados     [hoy importa CMS de Brasil]

SUBPRODUCTOS ──────────────────────── Harinas (alimento balanceado, acuicultura)
```

**Cada parte necesita al menos dos salidas** (una principal y una alternativa) para que un cierre sanitario no destruya su valor.

---

## 6. Sensibilidad conceptual a eventos

| Evento | Partes afectadas | Efecto sobre el ingreso por ave |
|---|---|---|
| Cierre de China | Garras, alas, pata-muslo | `Δ ingreso = k_garras × (NB_China − NB_alternativo)` + efectos en alas; es el mayor riesgo por kg |
| Brote de IAAP en Argentina (cierre de destinos que exigen país libre) | Todas las que se exportan a UE, Chile, Japón, Corea (y China si estuviera abierta) | Las partes vuelven al mercado interno, que a la vez recibe la sobreoferta de todo el sector (en 2025 hubo ventas ~40 % bajo costo durante ~40 días, FTE-052) |
| Brasil fuera de un mercado (ej.: UE desde 2026-09-03) | Pechuga | Ventana de precio **temporal** |
| Apreciación del peso | Todas | Reduce el net-back en pesos y abarata las importaciones que compiten con la pechuga local |
| Suba del flete reefer | Partes de bajo precio (menudencias, cuartos, CMS) | El flete es una proporción mayor de su precio: pueden dejar de convenir |

---

## 7. Implicancias para el diseño (sin dimensionar)

1. **La flexibilidad vale más que la especialización:** poder reasignar partes entre mercado interno y exportación (trozado, deshuese, congelado, cámaras) protege el ingreso por ave frente a cierres.
2. **Capacidades que habilitan la valorización:** trozado y deshuese; clasificación y proceso de garras; congelado (túnel/IQF) y almacenamiento a −18 °C o menos; separación de CMS; rendering (propio o tercerizado); empaque y etiquetado por destino; trazabilidad por lote. **Cuáles se hacen en planta propia y cuáles se tercerizan se decide en fases posteriores** (DEC-002).
3. **La escala condiciona la exportación de partes de bajo peso:** completar contenedores de garras o menudencias con regularidad requiere volumen diario o acumulación; se cuantificará con el balance de masa.
4. **La calidad empieza en la granja:** el grado de las garras depende de lesiones plantares (cama, manejo); el grado de pechuga y alas depende de hematomas (captura, transporte, aturdimiento).

## 8. Datos necesarios para cuantificar

| Dato | Registro |
|---|---|
| Rendimientos por parte según peso de faena y especificación | DPV-008 (`04_balance_masa`) |
| Precios locales por corte (mayorista, supermercado, gastronomía, industria) | DPV-013 |
| Precios FOB argentinos por producto y destino; referencias internacionales | DPV-026 |
| Costos logísticos, portuarios y de certificación por destino | DPV-027 |
| Alícuota vigente de derechos de exportación | DPV-015 |
| Condiciones de pago y lotes mínimos de compradores reales | DPV-032 |
