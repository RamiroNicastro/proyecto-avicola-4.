# Modelo conceptual de incubación

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 14B · Modelo: [`../14_alimento_balanceado/modelo_upstream.py`](../14_alimento_balanceado/modelo_upstream.py) (función `incubacion`; bloques `2_incubacion*` de [`escenarios_upstream.csv`](../14_alimento_balanceado/escenarios_upstream.csv))

> **Conceptual.** Describe el proceso de una planta de incubación de pollito parrillero y la cadena de cálculo de huevos a pollitos. **No** supone incubadora propia (SUP-034 sigue vigente), **no** modela genética ni reproductoras como obligatorias (solo como opción de fase futura), **no** elige tecnología ni fabricante y **no** tiene costos. Las descripciones de proceso son de práctica general y de manuales de genética leídos solo en extractos (FTE-14B-001, FTE-14B-002 `[PVDP]`).

---

## 1. Dónde está la incubación en la cadena

```
Genética (bisabuelas/abuelas) → REPRODUCTORAS (padres) → HUEVO FÉRTIL → INCUBACIÓN (21 d) → POLLITO BB → granja (engorde)
         [fase futura, opción C]          [opción C]       [compra: opción B]   [opción B y C]   [compra: opción A]
```

La demanda de pollitos por escala está en [`../14_alimento_balanceado/integracion_upstream.md` §1](../14_alimento_balanceado/integracion_upstream.md).

## 2. Proceso: huevo fértil → expedición

| Etapa | Qué pasa | Variables del modelo | Notas y riesgos |
|---|---|---|---|
| **1. Recepción de huevo fértil** | Llega de reproductoras (propias o de terceros) en bandejas/carros; se registra origen, edad del lote, fecha de postura; se descartan rotos, sucios, deformes o fuera de peso | `perdida_recepcion_almacen` (0,5 / 1 / 2 %, SUP-14B-03) | Bioseguridad: el huevo es una vía de entrada sanitaria (desinfección/fumigación a la recepción) |
| **2. Almacenamiento** | Sala climatizada (temperatura y humedad controladas) hasta completar la carga | `dias_almacen` 3 / 5 / 7 (óptimo 3–6 d citado; FTE-14B-001 `[PVDP]`) | El almacenamiento prolongado reduce la incubabilidad y la calidad del pollito (efecto no modelado: PENDIENTE) |
| **3. Incubadora (*setter*)** | ~18 días a temperatura, humedad, ventilación y volteo controlados; carga única (*single-stage*) o múltiple (*multi-stage*) | `D_INCUBADORA` 18 d + `D_LIMPIEZA_INC` 1 d (SUP-14B-04) | Tecnología no elegida (DEC-14B-05); la carga única facilita limpieza y bioseguridad |
| **4. Transferencia** (y vacunación *in ovo* si se usa) | A los ~18–19 días los huevos pasan a la nacedora; puede hacerse ovoscopia (retirar infértiles y embriones muertos) y vacunación *in ovo* (p. ej. Marek) | `perdida_transferencia` 0,3 / 0,5 / 1 %; `ovoscopia` (base: no) | Ventana de vacunación *in ovo* citada 17,5–19,2 d (FTE-14B-002 `[PVDP]`) |
| **5. Nacedora (*hatcher*)** | ~3 días hasta el nacimiento | `D_NACEDORA` 3 d + `D_LIMPIEZA_NAC` 1 d | Momento de mayor carga microbiológica (pelusa); zona sucia |
| **6. Selección** | Se separan pollitos aptos de los de descarte (débiles, ombligo mal cerrado, malformados); conteo | `descarte_seleccion` 0,5 / 1 / 2 % (SUP-14B-03) | Peso y uniformidad dependen de la edad de las reproductoras (DPV-14B-01) |
| **7. Vacunación** | Spray o inyección al día de nacimiento según plan sanitario (o ya hecha *in ovo*) | `pollitos_h_seleccion_vacunacion` = pollitos por nacimiento / horas de ventana (SUP-14B-06) | Plan vacunal: veterinario (DPV-056) |
| **8. Expedición** | Sala de pollitos climatizada; carga en cajas; camión climatizado a granja | `nacimientos_semana` 1–4; capacidad del camión PENDIENTE (DPV-047) | Horas de viaje y clima del camión afectan la mortalidad de la 1.ª semana |

## 3. Cadena de cálculo (inversa, desde la demanda)

```
pollitos vendibles/semana     = pollitos a recibir en granja (semana plena; de 03, con margen de pedido)
pollitos nacidos/semana       = vendibles / (1 − descarte de selección)
huevos incubados/semana       = nacidos / (fertilidad × incubabilidad de fértiles × (1 − pérdida en transferencia))
huevos fértiles/semana        = incubados × fertilidad
huevos a nacedora/semana      = incubados × (1 − pérdida en transferencia) × (fertilidad, solo si hay ovoscopia)
huevos recibidos/semana       = incubados / (1 − pérdida en recepción y almacenamiento)
incubabilidad sobre cargados  = fertilidad × incubabilidad de fértiles × (1 − pérdida en transferencia)
```

**Conservación (test U01):** recalculando hacia adelante (recibidos × (1 − pérdida) × fertilidad × incubabilidad × (1 − transferencia) × (1 − descarte)) se recupera exactamente la demanda (error ≤ 10⁻⁹), y la cadena es estrictamente decreciente: huevos recibidos > incubados > fértiles > nacidos > vendibles ≥ alojados > cargadas > faenadas.

## 4. Parámetros (todos SUPUESTOS editables)

| Parámetro | Favorable | **Medio** | Desfavorable | Clasificación |
|---|---|---|---|---|
| Fertilidad (huevos fértiles / incubados) | 0,95 | **0,92** | 0,88 | `[SUPUESTO]` SUP-14B-02. Referencia: ≥ 96,7 % **en pico** de postura (FTE-14B-001 `[PVDP]`); el promedio de vida del lote es menor |
| Incubabilidad de fértiles (nacidos / fértiles) | 0,92 | **0,90** | 0,87 | `[SUPUESTO]` SUP-14B-02. Referencia: 93,5 % **en pico** (FTE-14B-001 `[PVDP]`) |
| Pérdida en recepción y almacenamiento | 0,5 % | **1 %** | 2 % | `[SUPUESTO]` SUP-14B-03, sin fuente |
| Pérdida en transferencia (rotura) | 0,3 % | **0,5 %** | 1 % | `[SUPUESTO]` SUP-14B-03, sin fuente |
| Descarte en selección | 0,5 % | **1 %** | 2 % | `[SUPUESTO]` SUP-14B-03, sin fuente |
| **Incubabilidad sobre cargados (resultado)** | 87,1 % | **82,4 %** | 75,8 % | Coherente con el 80–85 % usado en `03` ([`modelos_integracion.md` §4.2](../03_produccion_primaria/modelos_integracion.md)) |
| Días en incubadora / nacedora / limpieza | 18 / 3 / 1 + 1 | | | `[SUPUESTO]` SUP-14B-04 (21 d de incubación: práctica general) |
| Margen de capacidad | 10 % | **15 %** | 20 % | `[SUPUESTO]` SUP-14B-05 (reserva de diseño) |

**Lo que el modelo NO captura** (registrado como faltante, no rellenado): efecto de la edad de las reproductoras sobre fertilidad, incubabilidad y peso del pollito; efecto de los días de almacenamiento sobre la incubabilidad; estacionalidad; huevos de doble yema o de piso; separación por sexo; mortalidad de la 1.ª semana atribuible a la incubación (DPV-14B-01).

## 5. Habilitación y bioseguridad (a verificar)

Una planta de incubación requiere habilitación SENASA como establecimiento avícola, flujo unidireccional limpio → sucio (huevo → pollito), separación de las granjas, manejo de residuos de incubación (cáscaras, huevos no nacidos, descarte de pollitos) y control de *Salmonella* en reproductoras proveedoras (Res. SENASA 86/2016 y 882/2002, FTE-148 `[PVDP]`). **Ninguna norma leída en original** (DPV-009, DPV-14B-06).

Capacidad por escala: [`capacidad_incubacion.md`](capacidad_incubacion.md). Comparación de opciones: [`compra_vs_incubacion.md`](compra_vs_incubacion.md).
