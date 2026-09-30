# Caracterización de efluentes de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Fase 0

> **Alcance:** corrientes que llegan al efluente, rangos de DBO, DQO, SST, grasas y aceites, nitrógeno y fósforo, carga orgánica por escala y cuánto material puede **evitar** llegar al efluente según el balance de masa. **Ningún valor es universal** ni medido en Argentina; todas las concentraciones externas son `[PVDP]`. No se diseña tratamiento (ver [`alternativas_tratamiento.md`](alternativas_tratamiento.md)).
> **Modelo:** [`modelo_utilities.py`](modelo_utilities.py) (bloques `efluente`, `masa_evitable`). Masa: [`../23_plan_expansion/escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv) (balance v1.1, config. B, 2,9 kg, inmersión).

---

## 1. Corrientes que forman el efluente

| Corriente | Origen | Qué aporta | Controlable en origen | Observación |
|---|---|---|---|---|
| **Sangre** | Desangrado (no recuperada), escaldado, lavados | La mayor carga específica: DQO ~375.000 mg/L en la sangre pura (FTE-181 `[PVDP]`); nitrógeno y fósforo solubles | **Sí**: canaleta y tanque separados, tiempo de desangrado | La fracción no recuperada del modelo es 15 % (SUP-040); lo soluble no se retira con tamiz ni DAF (FTE-09C-06) |
| **Grasas** | Evisceración, lavados, despiece (piel, grasa abdominal), limpieza | Grasas y aceites (origen animal, no mineral: FTE-09C-03), taponamiento, DQO | Parcial: retiro en seco, trampas, DAF | Condiciona el pretratamiento y el biológico |
| **Sólidos** | Recortes, restos de vísceras, plumas finas, contenido GI, cutícula de patas | SST, DQO particulada, materia sedimentable | **Sí**: transporte en seco, rejas y tamices | El balance manda 0,006 kg/ave de cutícula al efluente/lodos |
| **Plumas** | Desplumado; transporte hidráulico en canal (si se usa) | Sólidos gruesos; lixiviado orgánico si se transportan con agua | **Sí**: transporte en seco o tamizado inmediato | 0,241 kg/ave húmedas; deben retirarse, no tratarse |
| **Materia orgánica disuelta** | Todas las etapas en contacto con carne y vísceras; escaldado | DBO/DQO soluble, NTK | Parcial (menos contacto, menos agua caliente) | Es lo que llega al biológico |
| **Detergentes** | Limpieza (alcalinos, ácidos, espumantes) | pH extremo, tensioactivos, fósforo (algunos), espuma | **Sí**: selección de químicos, dosificación | Descarga concentrada en la ventana de limpieza: pico de pH y caudal |
| **Sanitizantes** | Cloro, ácido peracético, amonios cuaternarios, antimicrobianos de chiller | Oxidantes/biocidas que pueden inhibir el biológico | **Sí**: neutralización, ecualización | Uso de antimicrobianos en carne aviar a verificar en normativa argentina |
| **Aguas de proceso** | Escaldador (vaciado diario, alta carga y temperatura), chiller (desborde), lavados | Caudal y temperatura; el vaciado del escaldador es un pulso de alta carga | Parcial | La ecualización absorbe pulsos |
| **Agua de goteo del producto** | Purga del producto antes de la venta | 0,037 kg/ave (agua con proteína soluble) | No | Del balance (clase D) |
| **Aguas cloacales y pluviales** | Vestuarios, comedor; techos y playas | Carga doméstica; pluviales limpias | Separar pluviales | No mezclar pluviales con proceso (caudal) |

## 2. Rangos de concentración publicados (efluente crudo de faena avícola)

Todas `[PVDP]` (extractos de buscador; originales no leídos). **Rango amplio porque depende de recolección de sangre, agua por ave, transporte hidráulico de vísceras/plumas y punto de muestreo.**

| Parámetro | Rango/valor citado | Fuente |
|---|---|---|
| DQO | 1.223–9.695 mg/L; promedio de plantas ~2.000 mg/L; un estudio 3.154–7.719 mg/L; ~2.900–7.700 mg/L; caso de baja carga 155 mg/L; caso venezolano 820 mg/L | FTE-09C-05, FTE-181, FTE-09C-07 |
| DBO₅ | Promedio 2.375 mg/L; 1.341–1.821 mg/L; ~970–2.900 mg/L; caso 784 mg/L | FTE-09C-05, FTE-181, FTE-09C-07 |
| SST | 378–5.462 mg/L; caso 1.410 mg/L | FTE-09C-05, FTE-09C-07 |
| Grasas y aceites | ~500 mg/L (efluente tamizado) | FTE-09C-06 `[débil]` |
| NTK | ~150 mg/L (tamizado); 296 ± 53 mg/L (una planta de EE.UU.) | FTE-09C-06 |
| Fósforo total | ~18,5 mg/L (tamizado); −60 % al mejorar la recolección de sangre | FTE-09C-06 |
| Relación DBO/DQO | ~0,4–0,6 en la mayoría; ~0,95 en un caso | Calculada de las anteriores `[ESTIMACIÓN]` |

**No se adopta un valor único.** El modelo usa **carga específica por ave** (g/ave), que es físicamente más estable que la concentración: una planta que usa menos agua tiene el mismo kg de DQO pero más concentrado. La concentración es un **resultado** (carga / caudal).

## 3. Carga específica adoptada (efluente crudo, sangre recuperada al 85 %)

`[ESTIMACIÓN]` = rangos de concentración × rangos de caudal (§2 y [`balance_agua.md`](balance_agua.md) §3), redondeados.

| Parámetro | Bajo | **Medio** | Alto | Concentración resultante con el caudal medio (22 L/ave descargados) |
|---|---|---|---|---|
| DQO | 50 | **100** | 180 g/ave | 4.545 mg/L (dentro del rango 1.223–9.695) |
| DBO₅ | 25 | **50** | 90 g/ave | 2.273 mg/L |
| SST | 15 | **35** | 80 g/ave | 1.591 mg/L |
| Grasas y aceites | 5 | **11** | 25 g/ave | 500 mg/L |
| NTK | 3 | **5** | 8 g/ave | 227 mg/L |
| Fósforo total | 0,3 | **0,5** | 1,0 g/ave | 23 mg/L |

Cautelas: (1) el "bajo" con caudal bajo o el "alto" con caudal alto no son combinaciones obligadas: la carga y el caudal se eligen por separado en el modelo (`--dqo-g-ave`, `--l-ave`); (2) el test U17 verifica que la DQO media resultante quede dentro del rango de fuentes; (3) la carga depende fuertemente de la **recuperación de sangre** (§5).

## 4. Carga orgánica por escala

`[ESTIMACIÓN]` kg por día operativo (bajo · **medio** · alto). Remoción ilustrativa: con el límite de 250 mg/L de DQO para vuelco a conducto pluvial de la Res. ADA 336/2003 (PBA, `[PVDP]`, FTE-09C-08), el efluente medio exigiría **~94,5 %** de remoción de DQO. Otras provincias y cuerpos receptores: sin relevar (propuesta de DPV en [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md)).

| Escala (aves/día op.) | Efluente m³/día | DQO kg/día | DBO₅ kg/día | SST kg/día | GyA kg/día | NTK kg/día |
|---|---|---|---|---|---|---|
| 2.500 | 30 · **55** · 90 | 125 · **250** · 450 | 62 · **125** · 225 | 38 · **88** · 200 | 12 · **28** · 62 | 8 · **12** · 20 |
| 5.000 | 60 · **110** · 180 | 250 · **500** · 900 | 125 · **250** · 450 | 75 · **175** · 400 | 25 · **55** · 125 | 15 · **25** · 40 |
| 10.000 | 120 · **220** · 361 | 500 · **1.000** · 1.800 | 250 · **500** · 900 | 150 · **350** · 800 | 50 · **110** · 250 | 30 · **50** · 80 |
| 20.000 | 240 · **440** · 722 | 1.000 · **2.000** · 3.600 | 500 · **1.000** · 1.800 | 300 · **700** · 1.600 | 100 · **220** · 500 | 60 · **100** · 160 |

**Lectura:** ~500 kg de DBO/día (10.000 aves/día, medio) es una carga del orden de la de una población de varios miles de habitantes (a razón de ~50–60 g DBO/hab·día, dato de ingeniería sanitaria no verificado en esta sesión). Es la razón por la que la planta de efluentes es un **sistema de primera línea**, no un accesorio, y por la que **los límites de vuelco del sitio** pueden decidir la escala o la localización.

## 5. Valor de recuperar sangre y sólidos (usa el balance de masa)

### 5.1 Masa que puede evitar llegar al efluente

Del balance v1.1 (config. B, 2,9 kg, medio), t por día operativo. **Son masas que se retiran en seco; no son reducciones medidas de DQO.**

| Material | kg/ave | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Sangre recuperada (85 % de la drenada, SUP-040) | 0,084 | 0,21 | 0,42 | 0,84 | 1,68 |
| Plumas húmedas | 0,241 | 0,60 | 1,21 | 2,41 | 4,83 |
| Vísceras no comestibles | 0,131 | 0,33 | 0,65 | 1,31 | 2,61 |
| Cabezas | 0,073 | 0,18 | 0,36 | 0,73 | 1,45 |
| **Total de sólidos a retirar** (clase C + decomisos + contenido GI; no sumar con las filas anteriores) | 0,608 | **1,52** | **3,04** | **6,08** | **12,17** |
| Masa que el balance ya envía a efluente o pérdida (sangre no recuperada, cutícula, goteo, pérdidas no asignadas) | 0,108 | 0,27 | 0,54 | 1,08 | 2,16 |

**Lectura:** por cada kg que el balance ya manda al efluente o a pérdida, hay ~5,6 kg de sólidos que **deben** retirarse en seco. Si esos sólidos se transportan con agua (canales de plumas y vísceras), parte de su materia orgánica se disuelve y ya no puede separarse con rejas: el diseño del **transporte** (seco vs hidráulico) es una decisión de efluentes, no solo de proceso (DEC propuesta).

### 5.2 Orden de magnitud del efecto de la sangre

`[ESTIMACIÓN]` con DQO de la sangre ~0,357 kg/kg (375.000 mg/L ÷ 1,05 kg/L; FTE-181 `[PVDP]`):

| Escala | DQO de la sangre recuperada (si fuera al efluente) kg/día | Comparación con la DQO media del efluente |
|---|---|---|
| 2.500 | 75 | +30 % |
| 5.000 | 150 | +30 % |
| 10.000 | 299 | +30 % |
| 20.000 | 599 | +30 % |

- La sangre **no recuperada** (15 %) ya está dentro de la carga base: ~5,3 g DQO/ave (~5 % de la DQO media).
- **No se afirma una reducción exacta:** la cifra depende de un único dato `[PVDP]` de DQO de la sangre y de que la carga base (100 g/ave) corresponda efectivamente a plantas con recuperación de sangre, lo que las fuentes no aclaran. Lo robusto es la **dirección y el orden de magnitud**: perder la sangre puede aumentar la carga de DQO del orden de un tercio, y su nitrógeno y fósforo solubles no se retiran con pretratamiento físico (FTE-09C-06). Coherente con [`../07_subproductos/mapa_subproductos.md`](../07_subproductos/mapa_subproductos.md) §4 (sangre al efluente ≈ 350 kg DQO/día a 10.000 aves/día).
- El modelo permite cambiar la recuperación (`--frac-sangre`); el test U15 verifica que la DQO adicional sea exactamente sangre no recuperada × DQO de la sangre.

## 6. Qué falta

| Dato | Registro |
|---|---|
| Caracterización medida (DBO, DQO, SST, GyA, NTK, PT, pH, T, sedimentables) de efluente de faena avícola **argentina**, por punto (crudo, post-tamiz, post-DAF) y por día (faena vs limpieza) | DPV-067 |
| Límites de vuelco por provincia y cuerpo receptor en zonas candidatas (PBA, Santa Fe, Córdoba, Entre Ríos, Chaco) y canon/permiso | DPV-067; nueva DPV propuesta |
| DQO/DBO/N de la sangre de pollo (original de FTE-181) | DPV-067 |
| Productos de limpieza y sanitizantes admitidos y su efecto en el tratamiento | Nueva DPV propuesta |
