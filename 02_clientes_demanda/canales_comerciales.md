# Canales comerciales locales — análisis conceptual

**Fecha:** 2026-09-29 · **Versión:** 1 (conceptual) · Marco: [`modelo_demanda.md`](modelo_demanda.md) · Red de supermercados: [`supermercados.md`](supermercados.md) · Exportación como demanda: [`modelo_demanda.md` §4](modelo_demanda.md)

> **Alcance y límites:** descripción cualitativa de cada canal para orientar el relevamiento de campo. **No se asigna volumen propio a ningún canal** (no hay evidencia). Las características son **hipótesis de trabajo a validar con entrevistas** (DPV-040), no datos. No existe una serie pública de ventas de pollo por canal en Argentina (DPV-012); la única referencia es de consumo masivo en general (FTE-054 `[PVDP]`: cadenas 40 %, comercio tradicional 32 %, autoservicios independientes 16 % del volumen de consumo masivo, no específico de pollo).
> Los volúmenes de "otros canales" de [`escenarios_demanda.csv`](escenarios_demanda.csv) son valores de prueba, no estimaciones de mercado.

---

## 1. Ficha por canal

Escala cualitativa de volumen **por cliente individual**: bajo / medio / alto / muy alto (no se asignan kg).

| Canal | Productos típicos | Volumen por cliente | Frecuencia | Sensibilidad al precio | Condiciones de pago (a validar) | Complejidad logística | Estabilidad | Barreras de entrada |
|---|---|---|---|---|---|---|---|---|
| **Mayoristas** (de carnes o generalistas, con venta a comercios) | Entero en cajón, pata-muslo, alas, menudencias; congelado para acopio | Alto a muy alto | Varias veces por semana o por camión completo | **Muy alta**: compran por precio, cambian de proveedor rápido | Probablemente más cortas que las de supermercados; variables | **Baja**: pocas entregas grandes o retiro en planta | Media–baja (lealtad al precio) | Bajas en lo comercial; exigen habilitación y volumen continuo; compiten con los integradores |
| **Distribuidores** (reparten a pollerías, carnicerías, gastronomía) | Entero, trozado, menudencias, elaborados; a veces multimarca | Alto | Diaria o varias por semana | Alta (su margen está en la diferencia) | A validar; pueden pedir consignación o plazos | **Baja para el proyecto** (el distribuidor hace la última milla) | Media; depende de la relación y de la exclusividad zonal | Relación comercial y exclusividades con proveedores actuales |
| **Pollerías** | Entero, trozado, pechuga, pata-muslo, alas, menudencias, milanesas caseras | Bajo a medio | Diaria (producto fresco) | Alta | Frecuentemente contado o plazos cortos (a validar) | **Alta** si es directa (muchos puntos chicos); baja vía distribuidor | Media–alta si hay buen servicio | Bajas; el acceso suele ser vía distribuidor |
| **Carnicerías** (incluida la carnicería familiar) | Entero, pata-muslo, pechuga, milanesas; el pollo es complemento de la carne vacuna | Bajo | 2–6 veces por semana | Alta | Contado o plazos cortos (a validar) | Alta si es directa | Media | Bajas; la carnicería familiar es un canal propio de aprendizaje (SUP-005) |
| **Restaurantes** (incluye parrillas, rotiserías, cadenas de comida rápida) | Pechuga/filet, suprema porcionada, pata-muslo deshuesado, alas, milanesas, elaborados listos | Bajo (independientes) a alto (cadenas) | 2–6 veces por semana | Media (valoran calibre y porcionado estable) | Variables; cadenas con plazos más largos (a validar) | Media; cadenas con CD, independientes dispersos | Media–alta en cadenas con especificación y contrato | Especificación técnica, homologación de proveedor en cadenas |
| **Hoteles** | Pechuga, porcionados, congelado IQF | Bajo a medio | Semanal | Media–baja | Plazos a validar | Media | Media (estacionalidad turística) | Homologación; suelen comprar vía distribuidores gastronómicos |
| **Catering** (comedores de empresas, escuelas, hospitales, eventos) | Pata-muslo, pechuga, porcionados de peso fijo, congelado | Medio a alto | Semanal o por contrato | **Alta** (licitaciones y contratos por precio) | Contratos; en el sector público, plazos largos y riesgo de cobro (a validar) | Media | **Alta** mientras dura el contrato | Licitaciones, especificación, antecedentes |
| **Industria alimenticia** (fabricantes que usan pollo como insumo: empanadas, tartas, comidas listas, pastas) | Pechuga industrial, pata-muslo deshuesado, recortes, **CMS**, congelado en bloque | Medio a alto | Semanal a mensual | Alta (insumo de costo) | Plazos comerciales de industria (a validar) | Baja (entregas grandes y programadas) | **Alta** con especificación y contrato | Especificación microbiológica, continuidad, habilitación; hoy se importa CMS de Brasil (`01_mercado` §1.6) |
| **Fábricas de elaborados** (nuggets, hamburguesas, rebozados, embutidos) | CMS, recortes, piel, pata-muslo deshuesado, pechuga | Medio a alto | Semanal | Alta | A validar | Baja | Alta con contrato | Especificación; competencia de importados de Brasil |

**Exportación:** se analiza como demanda por niveles en [`modelo_demanda.md` §4](modelo_demanda.md) y como estrategia en `17_exportacion`. Hoy es categoría D.

---

## 2. Qué parte del ave absorbe cada canal

Relevante para el **ingreso total por ave** (SUP-013) y para colocar los excedentes del mix de supermercados ([`supermercados.md` §2.3](supermercados.md)).

| Parte | Supermercados | Mayoristas / distribuidores | Pollerías / carnicerías | Gastronomía / hoteles / catering | Industria / elaborados | Exportación (hoy nivel ≤ 2) |
|---|---|---|---|---|---|---|
| Entero | ● | ● | ● | ○ | — | ○ (Chile, Golfo con Halal) |
| Pechuga / filet | ● | ○ | ● | ● | ○ | ○ (UE, Medio Oriente) |
| Pata-muslo | ● | ● | ● | ● (catering) | ○ (deshuesado) | ○ (Vietnam, Chile, Japón deshuesado) |
| Alas | ○ | ● | ● | ● | — | ○ (Asia) |
| Menudencias | ○ | ● | ● | — | ○ | ○ (África) |
| Garras | — | ○ | ○ | — | — | ● (China no disponible confirmado; Vietnam, Hong Kong a verificar) |
| Carcasa, recortes, piel, CMS | — | — | — | — | ● | ○ (Filipinas, Sudáfrica) |
| Elaborados | ● | ○ | ○ | ● | — | — |

● salida principal probable · ○ salida secundaria posible · — poco relevante. Clasificación `[SUPUESTO]` cualitativo, a validar en campo (DPV-040).

**Lectura:** los supermercados absorben sobre todo entero, cortes nobles y elaborados; **las partes de menor valor (menudencias, alas en exceso, carcasa, CMS, garras) dependen de mayoristas, canal tradicional, industria y exportación**. Una estrategia apoyada solo en supermercados deja partes del ave sin mejor destino.

---

## 3. Canales más relevantes para investigar (priorización)

| Prioridad | Canal | Por qué | Qué averiguar primero |
|---|---|---|---|
| 1 | **Red de supermercados** | Único canal con acceso potencial identificado; puede ser cliente ancla | Cuestionario completo ([`cuestionario_supermercados.md`](cuestionario_supermercados.md)) |
| 2 | **Mayoristas y distribuidores del AMBA** | Mayor volumen por cliente, baja complejidad logística, salida para partes y excedentes; diversifican la concentración | Volumen por cliente, productos, precios de compra, plazos, proveedores actuales, requisitos |
| 3 | **Industria alimenticia y fábricas de elaborados** | Destino de CMS, recortes y deshuesados (partes que el supermercado no absorbe); sustitución de importaciones | Especificaciones, volúmenes, precios de referencia (incluido el importado), contratos |
| 4 | **Gastronomía de cadena y catering** | Especificación estable, volumen programable, valoriza pechuga y porcionados | Homologación de proveedores, calibres, plazos, licitaciones |
| 5 | **Pollerías y carnicerías** (incluida la familiar) | Canal fresco clásico, cobro rápido (a validar); aprendizaje propio | Datos de la carnicería familiar (DPV-004); relevamiento de 5–10 comercios |
| 6 | **Hoteles y restaurantes independientes** | Volumen por cliente bajo y disperso; mejor vía distribuidores gastronómicos | Qué distribuidores los abastecen |
| — | Exportación | Opción de diseño y piso de valor de partes; no es demanda hoy | Ver `17_exportacion/conclusiones_exportacion.md` §7 |

---

## 4. Información a relevar por canal (común a todos)

Para cada cliente entrevistado: nombre y tipo; ubicación; kg/semana por producto; refrigerado o congelado; especificaciones (calibre, packaging, piel, hueso); proveedor actual; precio de compra sin IVA con fecha; plazo y medio de pago; frecuencia y horario de entrega; requisitos sanitarios y de alta; problemas con proveedores actuales; interés en un proveedor nuevo; volumen de prueba. Registro como `entrevista` en `25_fuentes/registro_fuentes.csv` y clasificación A/B/C/D en el pipeline ([`estrategia_comercial.md` §4](estrategia_comercial.md)).
