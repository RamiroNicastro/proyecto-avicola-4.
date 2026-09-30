# Caracterización de efluentes de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** corrientes que llegan al efluente, rangos de DBO, DQO, SST, grasas y aceites, nitrógeno y fósforo, carga orgánica por escala con **dos métodos independientes** y masa **potencialmente segregable en origen** según el balance de masa (que **no** es SST del efluente). **Ningún valor es universal** ni medido en Argentina; todas las concentraciones externas son `[PVDP]`. No se diseña tratamiento (ver [`alternativas_tratamiento.md`](alternativas_tratamiento.md)).
> **Modelo:** [`modelo_utilities.py`](modelo_utilities.py) v1.1 (bloques `efluente`, `masa_segregable`, `alertas`). Masa: [`../23_plan_expansion/escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv) (balance v1.1, config. B, 2,9 kg, inmersión).

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

**No se adopta un valor único.** Desde la v1.1 el modelo estima la carga por **dos métodos independientes** y los compara; ninguno se calibra con el otro.

## 3. Dos métodos independientes para estimar la carga

| | **Método A — carga específica** | **Método B — caudal × concentración** |
|---|---|---|
| Fórmula | kg/día = aves/día × g/ave ÷ 1.000 | kg/día = m³ de efluente/día × mg/L ÷ 1.000 |
| Parámetros | g DQO / DBO₅ / SST / GyA / NTK / PT por ave | mg/L de DQO / DBO₅ / SST (solo donde hay rangos citados) |
| Depende del agua | **No** | **Sí** (del caudal descargado y de la fracción a efluente supuesta) |
| Valores (bajo · medio · alto) | DQO 50 · **100** · 180; DBO₅ 25 · **50** · 90; SST 15 · **35** · 80; GyA 5 · 11 · 25; NTK 3 · 5 · 8; PT 0,3 · 0,5 · 1 g/ave | DQO 2.000 · **5.400** · 9.695; DBO₅ 970 · **1.600** · 2.900; SST 378 · **1.410** · 5.462 mg/L |
| Estado | **Escenarios `[PVDP]`**, no mediciones | **Valores citados `[PVDP]`** (promedio, centro de un rango, extremo) |
| Qué valida en campo | Masa de DQO por ave (DQO × caudal medido ÷ aves) | Concentración del efluente crudo compuesto |

**Regla de compatibilidad** (`[SUPUESTO]` editable: `TOLERANCIA_METODOS = 2` en el script): si la relación B/A cae fuera de [0,5; 2], el modelo emite la alerta **"DATOS DE EFLUENTE REQUIEREN VALIDACIÓN DE CAMPO"**. Test **U27**: cambiar la concentración no mueve el método A; cambiar la carga por ave no mueve el método B (mutación M20: calibrar B con A es detectada).

## 4. Reconciliación DQO por ave vs concentración

A 10.000 aves/día (lineal: las demás escalas escalan igual; las relaciones B/A no cambian con la escala):

| Parámetro | Nivel | Método A kg/día | Método B kg/día | B/A | Concentración implícita de A (mg/L) | ¿Compatibles? |
|---|---|---|---|---|---|---|
| DQO | bajo | 500 | 240 | 0,48 | 4.167 | **No → alerta** |
| DQO | **medio** | **1.000** | **1.188** | **1,19** | 4.545 | Sí |
| DQO | alto | 1.800 | 3.500 | 1,94 | 4.986 | Sí (en el límite) |
| DBO₅ | bajo | 250 | 116 | 0,47 | 2.083 | **No → alerta** |
| DBO₅ | **medio** | **500** | **352** | **0,70** | 2.273 | Sí |
| DBO₅ | alto | 900 | 1.047 | 1,16 | 2.493 | Sí |
| SST | bajo | 150 | 45 | 0,30 | 1.250 | **No → alerta** |
| SST | **medio** | **350** | **310** | **0,89** | 1.591 | Sí |
| SST | alto | 800 | 1.972 | 2,46 | 2.216 | **No → alerta** |

**Lectura:** en el escenario medio ambos métodos dan el **mismo orden de magnitud** (~1.000–1.200 kg DQO/día a 10.000 aves/día). En los extremos divergen porque combinan supuestos que no tienen por qué ir juntos: poca agua con baja concentración (bajo) o mucha agua con concentración máxima (alto). Una planta que ahorra agua **concentra** su efluente; por eso la concentración sola no alcanza para dimensionar. **La divergencia no se corrige ajustando parámetros: se resuelve midiendo** caudal y concentración en una planta real (DPV-067).

Por escala (kg/día, método A · método B, medio): DQO 250 · 297 / 500 · 594 / 1.000 · 1.188 / 2.000 · 2.376; DBO₅ 125 · 88 / 250 · 176 / 500 · 352 / 1.000 · 704; SST 88 · 78 / 175 · 155 / 350 · 310 / 700 · 620 (2.500 / 5.000 / 10.000 / 20.000 aves/día). Grasas, NTK y PT solo por método A (medio, 10.000 aves/día: 110 / 50 / 5 kg/día).

## 5. Límite de vuelco: solo ejemplo regulatorio

El modelo usa como **EJEMPLO REGULATORIO DE REFERENCIA** la Res. ADA 336/2003 de la Provincia de Buenos Aires para vuelco a **conducto pluvial** (DQO 250 mg/L, DBO 50 mg/L; FTE-09C-08 `[PVDP]`). Cada límite del modelo lleva jurisdicción, autoridad, norma y tipo de descarga; un límite sin esos datos detiene el modelo (test **U26**, mutación M19).

> **Bajo el ejemplo de límite utilizado, el escenario medio exigiría aproximadamente 94,5 % (método A) a 95,4 % (método B) de remoción de DQO** (rango de todos los escenarios: 87,5–97,4 %).

**No es un requisito del proyecto.** La remoción necesaria dependerá de la provincia, la autoridad hídrica, el cuerpo receptor, la red cloacal o pluvial cuando corresponda, las condiciones particulares del permiso y la normativa vigente al momento del proyecto. **La localización futura reemplazará este benchmark por el límite regulatorio real** (DPV-067).

## 6. Subproductos del balance ≠ sólidos del efluente ≠ SST

La v1.0 decía "se pueden retirar en seco 6,1 t/día". Se corrige: que un material no sea producto comercial **no** significa que esté presente como sólido suspendido en el efluente.

| Concepto | Qué es | Cómo se obtiene | 10.000 aves/día |
|---|---|---|---|
| **A. Masa biológica potencialmente segregable en origen** | Materiales del balance que **deberían capturarse antes de llegar a los drenajes**: sangre recuperable, plumas, vísceras, cabezas, contenido GI, decomisos | Balance de masa v1.1 (clase C + decomisos + contenido GI) | **6,1 t/día** (0,61 kg/ave) |
| **B. Sólidos que efectivamente entran al efluente** | Lo que se escapa al drenaje por diseño del proceso, pérdidas, lavado, tamizado, manejo de subproductos y disciplina operativa | **PENDIENTE** (medición en planta) | Sin valor |
| **C. SST del efluente** | Sólidos suspendidos medidos en el agua | Método A (g/ave) o método B (mg/L), **independientes del balance** | 350 (A) · 310 (B) kg/día (medio) |

Masa segregable en origen por escala (t/día, del balance; no son reducciones medidas ni SST):

| Material | kg/ave | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Sangre recuperable (85 % de la drenada, SUP-040) | 0,084 | 0,21 | 0,42 | 0,84 | 1,68 |
| Plumas húmedas | 0,241 | 0,60 | 1,21 | 2,41 | 4,83 |
| Vísceras no comestibles | 0,131 | 0,33 | 0,65 | 1,31 | 2,61 |
| Cabezas | 0,073 | 0,18 | 0,36 | 0,73 | 1,45 |
| **Masa biológica potencialmente segregable en origen** (no sumar con las filas anteriores) | 0,608 | **1,52** | **3,04** | **6,08** | **12,17** |
| Masa que el balance asigna a efluente o pérdida (sangre no recuperada, cutícula, goteo, pérdidas no asignadas) — **no equivale a SST** | 0,108 | 0,27 | 0,54 | 1,08 | 2,16 |

Test **U22**: triplicar la masa de subproductos del balance no cambia los SST de ningún método, y la variable "sólidos que entran efectivamente al efluente" queda vacía (mutación M12). Si esos materiales se transportan con agua (canales de plumas y vísceras), parte se disuelve y ya no puede separarse: el **transporte en seco vs hidráulico** es una decisión de efluentes (DEC-09C-02 propuesta).

## 7. Sangre: principio firme, magnitud como referencia

- **Principio:** recuperar la sangre antes de que llegue al drenaje reduce fuertemente la carga orgánica, y su nitrógeno y fósforo solubles no se retiran con tamiz ni DAF (FTE-09C-06 `[PVDP]`).
- **Magnitud (referencia `[PVDP]` de sensibilidad, no resultado de la planta):** con DQO de la sangre ~0,357 kg/kg (FTE-181), la sangre recuperada aportaría ~299 kg DQO/día a 10.000 aves/día (75 / 150 / 299 / 599 por escala), del orden de **30 % de la carga del método A medio**.
- **Variable editable:** `fraccion_sangre_recuperada` (0,85 por defecto, SUP-040; `--frac-sangre`). El test U15 verifica que la DQO adicional sea exactamente sangre no recuperada × DQO de la sangre.
- **Validación:** medir DQO del efluente **antes y después** de mejorar la recolección, o medir **masa recuperada por ave** y carga específica.

## 8. Qué falta

| Dato | Registro |
|---|---|
| Caudal y caracterización medida (DBO, DQO, SST, GyA, NTK, PT, pH, T) de efluente de faena avícola **argentina**, por punto y por período (faena vs limpieza): resuelve la divergencia entre métodos | DPV-067 |
| Límite regulatorio real del sitio (provincia, autoridad, cuerpo receptor, permiso) | DPV-067 |
| DQO/DBO/N de la sangre de pollo (original de FTE-181) y masa de sangre recuperada por ave | DPV-067, DPV-080 |
| Sólidos que efectivamente llegan al drenaje en plantas con y sin transporte en seco | Nueva DPV propuesta |
| Productos de limpieza y sanitizantes admitidos y su efecto en el tratamiento | DPV-09C-05 propuesta |
