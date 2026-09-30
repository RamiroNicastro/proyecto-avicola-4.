# Conclusiones — modelo preliminar de utilities (agua, efluentes, energía, frío, congelado, respaldo)

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C, en paralelo) · Base: [`balance_agua.md`](balance_agua.md), [`caracterizacion_efluentes.md`](caracterizacion_efluentes.md), [`alternativas_tratamiento.md`](alternativas_tratamiento.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_utilities.py`](modelo_utilities.py), [`escenarios_utilities.csv`](escenarios_utilities.csv); energía y frío en [`../12_energia_frio/conclusiones_energia_frio.md`](../12_energia_frio/conclusiones_energia_frio.md)

> **Reconciliación 2026-09-30:** los IDs provisionales de esta sesión fueron reemplazados por definitivos y sus supuestos, datos por validar, decisiones y fuentes se integraron en los registros centrales ([`../00_gestion_proyecto/reconciliacion_sesiones_09.md`](../00_gestion_proyecto/reconciliacion_sesiones_09.md)). Donde este documento dice que los registros centrales no se modificaron, describe el estado de la sesión original.
> **Modelo TOP-DOWN de sensibilidad.** Los rangos bajo/medio/alto son órdenes de magnitud preliminares: **no son consumos esperados de nuestra planta ni especificaciones de diseño**. No se seleccionan equipos, tecnología de tratamiento, refrigerante, fuente térmica ni generador; no se calcula CAPEX ni OPEX; no se elige ubicación.
> **Fuentes:** acceso directo bloqueado (`EGRESS_BLOCKED`; DPV-009). **Toda cifra externa es `[PVDP]`** (19 fuentes de la sesión, integradas en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) como FTE-252 a FTE-268 y FTE-236, más FTE-181, FTE-135, FTE-157, FTE-016). **Ninguna cifra es una medición argentina.**
> **Sesión en paralelo:** no se modificaron `00_gestion_proyecto/`, `25_fuentes/` ni el catálogo de equipos de la sesión 09A; las propuestas están en [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md).

---

## 0. Auditoría conceptual v1.1 (2026-09-30)

Correcciones de **definiciones** para que los órdenes de magnitud no se conviertan en especificaciones. El modelo general se mantiene.

| # | Problema en v1.0 | Corrección v1.1 | Test / mutación |
|---|---|---|---|
| 1 | 15/25/38 L/ave podían leerse como consumo esperado; tres aguas | **Rango de sensibilidad preliminar**; cinco aguas (captada, utilizada, incorporada, evaporada/arrastrada, descargada); fracción a efluente = `[SUPUESTO]` editable (relación no fija); segunda unidad **m³/t de producto** con contraste y alerta | U03, U04, U28 · M01, M09 |
| 2 | Una sola estimación de carga (g/ave) | **Método A** (g/ave) y **método B** (m³ × mg/L) independientes; sin calibración cruzada; alerta "DATOS DE EFLUENTE REQUIEREN VALIDACIÓN DE CAMPO" si B/A sale de [0,5; 2] | U27 · M20 |
| 3 | "Hay que remover ~95 %" | ADA 336/03 = **ejemplo regulatorio de referencia** con jurisdicción y tipo de descarga; "bajo el ejemplo de límite utilizado, el escenario exigiría aproximadamente X %" | U26 · M19 |
| 4 | "Se pueden retirar en seco 6,1 t/día" | **Masa biológica potencialmente segregable en origen** (A) ≠ sólidos que entran al efluente (B, PENDIENTE) ≠ SST (C, métodos A/B) | U22 · M12 |
| 5 | "Recuperar sangre reduce la DQO ~30 %" | Principio firme; magnitud como **referencia `[PVDP]` de sensibilidad**; variable `fraccion_sangre_recuperada` editable; validación por medición | U15 · M07 |
| 6 | "~2,4 t/día de lodo deshidratado" | **LODO = PENDIENTE DE DIMENSIONAMIENTO**; cadena explícita SST removidos + grasas + químicos + biomasa → sólidos secos → % torta → t húmedas; escenario ilustrativo separado | U23 · M13, M14 |
| 7 | "Pico ~820 kW" derivado de kWh/ave | **Potencia media equivalente bajo X horas**; potencia pico, contratada, transformador y generador **PENDIENTES** (lista de cargas) | U20, U21 · M10, M11 |
| 8 | "El pico térmico lo fija la limpieza" | MJ/día y potencia térmica **media**; pico térmico **PENDIENTE** (perfil horario) | U20 |
| 9 | "~235 kWf" como frío de planta | **Carga sensible preliminar asociada al enfriamiento del producto** (99 kWf a 10.000 aves/día); agua de chiller y adicionales en filas separadas; carga frigorífica total **PENDIENTE**; brecha con el benchmark **no cerrada** | U24 · M15 |
| 10 | Conversión kWf → kWe sin COP visible | `kw_electricos_aprox_*` = kWf ÷ COP supuesto, con fila `cop_supuesto_*` | U10 · M04, M16 |
| 11 | — | Definiciones explícitas: congelación = t **nuevas**/día; almacenamiento = t **ya congeladas** guardadas | U09 · M06, M17 |
| 12 | "25/49/99/198 kVA" como respaldo | **Carga crítica ilustrativa de escenario** (proxy, kW); grupo electrógeno **PENDIENTE**; nunca % fijo de la planta | U25 · M18 |
| 13 | — | Integración futura **top-down vs bottom-up** con el catálogo de equipos de 09A (§5); alerta ante diferencias | U29 |

Cifras que **cambiaron**: la carga frigorífica ya no se agrega (99 + 69 + 67 kWf en filas separadas en vez de 235); el calor de congelación es solo del producto (296 kJ/kg; antes 385 con pérdidas de túnel); el respaldo pasa a kW ilustrativos (79 kW en vez de 99 kVA a 10.000 aves/día); lodos y potencias pico quedan vacíos. **No cambiaron** agua, cargas del método A, energía diaria, calor diario ni toneladas de congelado y stock.

## 1. Hallazgos principales (sensibilidad)

1. **Agua utilizada:** 15 / **25** / 38 L/ave (= 6,3 / **10,4** / 15,9 m³/t de producto) → 62 / 125 / 250 / 500 m³/día (medio) a 2.500 / 5.000 / 10.000 / 20.000 aves/día; ambas unidades caen dentro de los rangos citados.
2. **Cinco aguas:** a 10.000 aves/día (medio) captada ≈ utilizada 250 m³/día (sin potabilización con rechazo), incorporada 2,1 t/día, evaporada/arrastrada ~28 m³/día, descargada ~220 m³/día **con una fracción supuesta de 88 %**.
3. **Carga orgánica:** los dos métodos coinciden en orden de magnitud en el escenario medio (DQO 1.000 vs 1.188 kg/día a 10.000 aves/día; B/A = 1,19) y **divergen en los extremos** (bajo: B/A 0,3–0,5 en DQO, DBO y SST; alto: SST 2,46) → alerta de validación de campo.
4. **Ejemplo regulatorio:** bajo el límite de 250 mg/L de DQO (PBA, ADA 336/03, pluvial), el escenario medio exigiría ~95 % de remoción (87–97 % en todos los escenarios). No es requisito del proyecto.
5. **Masa segregable en origen:** 1,5 / 3,0 / 6,1 / 12,2 t/día de materiales que deben capturarse antes de los drenajes. Los sólidos que efectivamente llegan al efluente y los lodos están **pendientes**.
6. **Energía eléctrica:** ~0,8 kWh/ave → 8.184 kWh/día a 10.000 aves/día (medio); potencia media equivalente 518 kW (proceso, bajo 14 h) o 341 kW (total, bajo 24 h). **Pico pendiente.**
7. **Calor:** ~1 MJ útil/ave → ~13 GJ/día de combustible (~343 m³ de gas equivalente) a 10.000 aves/día; **pico térmico pendiente**.
8. **Frío:** carga sensible del producto 99 kWf (28 TR) a 10.000 aves/día; carga total pendiente; brecha ×5,7 con el benchmark sin cerrar.
9. **Congelado:** el perfil manda (P1→P3: ×5); congelación y almacenamiento separados.
10. **Respaldo:** carga crítica ilustrativa ~79 kW a 10.000 aves/día (P1, medio); generador pendiente.
11. **Los servicios pueden fijar la capacidad** (agua por hora, permiso de vuelco, potencia, frío, retiro de subproductos): son criterios de localización y escala.

## 2. Escenarios físicos por escala (sensibilidad)

Base: config. B, 2,9 kg, medio, inmersión, perfil P1, 5 d/sem, 250 días de faena; días **operativos**. Bajo · **medio** · alto. Con 300 días/año los valores diarios no cambian y los anuales suben 20 %.

| Variable | 2.500 | 5.000 | 10.000 | 20.000 | Origen |
|---|---|---|---|---|---|
| Agua utilizada m³/día | 38 · **62** · 95 | 75 · **125** · 190 | 150 · **250** · 380 | 300 · **500** · 760 | ESTIMACIÓN (L/ave de sensibilidad calibrados a FUENTE `[PVDP]`) |
| Agua utilizada m³/t de producto | 6,3 · **10,4** · 15,9 | idem | idem | idem | ESTIMACIÓN |
| Agua descargada m³/día | 30 · **55** · 90 | 60 · **110** · 180 | 120 · **220** · 361 | 240 · **440** · 722 | ESTIMACIÓN con fracción SUPUESTO (editable) |
| Agua incorporada t/día | 0,53 | 1,06 | 2,13 | 4,25 | ESTIMACIÓN (balance v1.1) |
| DQO método A · método B kg/día (medio) | 250 · 297 | 500 · 594 | 1.000 · 1.188 | 2.000 · 2.376 | A: escenario `[PVDP]`; B: conc. `[PVDP]` × caudal |
| DBO₅ A · B kg/día (medio) | 125 · 88 | 250 · 176 | 500 · 352 | 1.000 · 704 | idem |
| SST A · B kg/día (medio) | 88 · 78 | 175 · 155 | 350 · 310 | 700 · 620 | idem (independientes del balance) |
| Alerta de validación de efluente | bajo (DQO, DBO, SST) y alto (SST) en todas las escalas | | | | ESTIMACIÓN |
| Masa biológica potencialmente segregable en origen t/día | 1,5 | 3,0 | 6,1 | 12,2 | ESTIMACIÓN (balance v1.1); **no es SST** |
| Sólidos que entran efectivamente al efluente | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Medición |
| Lodos | PENDIENTE (ilustrativo 0,6 t/día húm.) | PENDIENTE (1,1) | PENDIENTE (2,2) | PENDIENTE (4,5) | Ilustrativo con SUPUESTO visibles |
| Energía eléctrica kWh/día operativo | 1.197 · **2.046** · 3.792 | 2.393 · **4.092** · 7.584 | 4.787 · **8.184** · 15.167 | 9.574 · **16.368** · 30.334 | ESTIMACIÓN con indicadores FUENTE `[PVDP]` y SUPUESTO |
| Potencia media equivalente de proceso bajo 14 h kW (medio) | 129 | 259 | 518 | 1.036 | ESTIMACIÓN |
| Potencia pico / demanda máxima | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Lista de cargas |
| Calor útil MJ/día | 1.152 · **2.501** · 5.774 | 2.303 · **5.002** · 11.547 | 4.606 · **10.005** · 23.094 | 9.213 · **20.009** · 46.188 | ESTIMACIÓN física |
| Potencia térmica pico | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Perfil horario |
| Carga sensible preliminar del producto kWf (TR) | 25 (7) | 50 (14) | 99 (28) | 198 (56) | ESTIMACIÓN con SUPUESTO |
| Carga frigorífica total | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Balance frigorífico |
| Producto comestible t/día (peso comercial) | 6,0 | 12,0 | 24,0 | 47,9 | ESTIMACIÓN (balance v1.1) |
| Capacidad de congelación t/día · P1 / P2 / P3 | 0,6 / 2,4 / 3,0 | 1,2 / 4,8 / 6,0 | 2,4 / 9,6 / 12,0 | 4,8 / 19,2 / 24,0 | ESTIMACIÓN con perfiles SUPUESTO |
| Capacidad de almacenamiento congelado 14 d (prod · cal) P3 t | 42 · 29 | 84 · 57 | 168 · 115 | 336 · 230 | ESTIMACIÓN (= escenarios_escala.csv) |
| Carga crítica ilustrativa kW (P1) | 11 · **20** · 40 | 22 · **40** · 81 | 43 · **79** · 162 | 86 · **158** · 323 | SUPUESTO (proxy) |
| Grupo electrógeno | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Lista de cargas críticas |

El CSV separa en la columna `origen` FUENTE / ESTIMACIÓN / SUPUESTO / **PENDIENTE** (valor vacío) y agrega los bloques `alertas`, `lodos_ilustrativo` y `parametros` (este último con los límites de ejemplo, su jurisdicción y tipo de descarga).

## 3. Tratamiento conceptual

Prevención en origen (sangre, transporte en seco) → pretratamiento (rejas/tamices, grasas, ecualización, DAF) → biológico (anaerobio, aerobio o combinación) → pulido según el límite real del sitio → lodos. La elección depende de terreno, carga (a medir), normativa del sitio, olor/vecindad, energía y operación ([`alternativas_tratamiento.md`](alternativas_tratamiento.md)). **No se elige.**

## 4. Principales incertidumbres

| # | Incertidumbre | Efecto | Registro |
|---|---|---|---|
| 1 | Agua por ave y fracción a efluente en plantas argentinas | ×2,5 en agua y efluente | DPV-067 |
| 2 | **Divergencia entre métodos A y B** en los extremos | Carga orgánica incierta hasta ×3 | DPV-067 |
| 3 | Límite de vuelco real (provincia, autoridad, cuerpo receptor, permiso) | Grado de tratamiento | DPV-067 |
| 4 | Sólidos que llegan efectivamente al efluente; lodos | Pretratamiento y logística de lodos | Nuevas DPV propuestas |
| 5 | Disponibilidad y calidad del agua; potencia eléctrica | Pueden limitar la escala o el sitio | DPV-053, DPV-052 |
| 6 | **Lista de cargas** (demanda máxima, cos φ, arranques) | Potencia contratada, transformador, generador | DPV-095 propuesta |
| 7 | Perfil horario térmico | Caldera | DPV-113 propuesta |
| 8 | Balance frigorífico; brecha ×5,7 con el benchmark | Sala de máquinas | DPV-109 propuesta |
| 9 | Perfil refrigerado/congelado y días de stock | ×5 en congelado y cámaras | DPV-085, DPV-078 |
| 10 | Indicadores kWh/t (base y alcance) | ×3 en energía | DPV-108 propuesta |

## 5. Integración futura con la sesión 09A: de top-down a bottom-up

La sesión 09A creó un catálogo conceptual de equipos (`08_maquinaria/matriz_equipos.csv` en `main`, EQ-01 a EQ-76, con una columna **cualitativa** `servicios`: elec, agua, agua caliente, agua helada, vapor, aire, vacío, frío, gas). **No se modifica desde esta rama.**

En la reconciliación posterior se deberá construir, para cada equipo:

```
EQUIPO 09A (EQ-xx) → potencia (kW nominal, factor de carga, horas/día, simultaneidad, arranque, cos φ)
                   → agua (m³/día o L/ave)
                   → aire comprimido (Nm³/h)
                   → vapor / calor (MJ/día, kW térmicos, horario)
                   → frío (kWf, temperatura de evaporación)
```

Con esa tabla (valores `[COTIZACIÓN]` de proveedores) el diseño futuro comparará:

| TOP-DOWN (este modelo) | BOTTOM-UP (equipos cotizados) |
|---|---|
| kWh/ave, L/ave, MJ/ave, carga sensible del producto | Σ consumos reales de equipos; demanda máxima desde la lista de cargas |

El modelo ya incluye `demanda_maxima(lista_de_cargas)` (potencia pico y kVA) y `contraste_bottom_up(r, equipos)`, que **no ajusta** ningún valor: si la relación bottom-up/top-down sale de [1/1,5; 1,5] (`[SUPUESTO]` editable) emite una alerta por variable (test **U29**). Propuesta: DEC-048 y DPV-095 en [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md).

## 6. Qué no se hizo

No se eligió tecnología ni proveedor; no se dimensionaron tanques, DAF, reactores, calderas, compresores, cámaras, transformadores ni generadores; no se calcularon potencias pico, carga frigorífica total ni lodos; no hay costos; no se eligió sitio; no se leyó ningún original.

## 7. Qué medir y qué cotizar

### 7.1 Sitio (por cada terreno candidato)

| Tema | Qué pedir / medir | A quién |
|---|---|---|
| **Disponibilidad de agua** | Caudal sostenido (ensayo de bombeo 24–72 h), acuífero, pozos vecinos; o caudal y presión de red | Hidrogeólogo; prestador; autoridad del agua (permiso) |
| **Análisis de agua** | Físico-químico completo (CAA art. 982: As, F, nitratos, dureza, Fe, Mn, sales) + microbiológico; temperatura estacional; rechazo si hay que potabilizar | Laboratorio habilitado |
| **Caudal de efluente admitido** | Colectora cloacal con capacidad; cuerpo receptor; caudal máximo | Prestador; autoridad del agua; municipio |
| **Límites de vuelco reales** | Tabla vigente por tipo de descarga, canon, condiciones del permiso | Autoridad del agua de cada provincia candidata |
| **Energía y potencia** | Potencia disponible y ampliable (BT/MT), obra y plazos | Distribuidora |
| **Calidad de red** | Historial de cortes y caídas de tensión | Distribuidora; vecinos industriales |
| **Gas** | Red, caudal horario (m³/h) y presión; alternativa GLP | Distribuidora de gas; proveedores de GLP |
| **Biomasa** | Disponibilidad, calidad, regularidad | Proveedores regionales |
| **Terreno para tratamiento** | Superficie, distancia a viviendas, vientos | Relevamiento propio |

### 7.2 Plantas de faena existentes (referencia argentina)

L/ave y m³/t medidos; fracción del agua que va a efluente; **caudal y concentración** del efluente crudo (para reconciliar métodos A y B); DQO antes/después de recuperar sangre y masa de sangre recuperada por ave; sólidos que llegan al drenaje; lodos (kg MS/día, % sólidos); kWh/ave, **demanda máxima** y potencia contratada; m³ de gas/ave y perfil horario térmico; TR instaladas y refrigerante; tamaño y lógica del generador.

### 7.3 Proveedores (fase posterior; sin seleccionar)

| Sistema | Qué pedir por escala (2.500–20.000) y perfil (P1–P3) |
|---|---|
| **Equipos de proceso (catálogo 09A)** | Por equipo: kW nominal, factor de carga, horas, arranque, cos φ, agua, aire, vapor/calor, frío (tabla bottom-up de §5) |
| **Frío** | Balance frigorífico completo (todas las cargas de [`../12_energia_frio/sistema_frio.md` §2](../12_energia_frio/sistema_frio.md)), refrigerante, COP de diseño con verano del sitio |
| **Congelado** | Túneles/IQF: t/día y tiempo de congelación; cámaras: t estáticas, estiba, kWh/(t·día) |
| **Tratamiento de efluentes** | Tren propuesto, superficie, kWh/día, químicos, **lodos (kg MS/día y % sólidos)**, garantía contra el límite real |
| **Agua** | Potabilización según análisis (rechazo), reserva, presurización |
| **Térmica** | Perfil horario, caldera o calentadores, acumulación, recuperación de calor |
| **Generador** | Lista de cargas críticas, kVA, arranques, secuencia, autonomía, N+1, black-start |

## 8. Tests

`python3 11_agua_efluentes/modelo_utilities.py` → **30/30 correctos**; `--mutaciones` → **20/20 detectadas**.

| Test | Qué verifica |
|---|---|
| U00 | Masas por ave de `escenarios_escala.csv` idénticas en 4 escalas y 2 calendarios |
| U01 | Escalabilidad lineal (462 variables; pendientes siguen pendientes) |
| U02 | Unidades: L↔m³, día↔año, kW↔TR, MJ↔kWh, g/ave↔kg/día, m³×mg/L↔kg/día |
| U03 | Agua incorporada separada del consumo |
| U04 | Cierre: captada ≥ utilizada = descargada + incorporada + evaporada (≥ 0); fracción editable; alerta si no cierra |
| U05 | Bajo < medio < alto |
| U06 | Σ etapas = agua utilizada |
| U07 | Inventario = modelo de escala (640/640 filas) |
| U08 | Días calendario = días de producción × días op./365 |
| U09 | **Congelación (t/día nuevas) y almacenamiento (t guardadas): variables y unidades distintas, independientes** |
| U10 | **kW eléctricos aprox. = kWf ÷ COP supuesto declarado** |
| U11 | kWh/día = aves × kWh/ave |
| U12 | Sin negativos ni no finitos (PENDIENTE = vacío; 4.995 filas) |
| U13 | Sin variables económicas |
| U14 | 13 entradas inválidas rechazadas |
| U15 | Fracción de sangre editable; efecto como referencia `[PVDP]` |
| U16 | Masa segregable = balance/escala |
| U17 | Perfiles = 100 %; concentraciones del método B dentro del rango de fuentes |
| U18 | Sexto día: +50 días de proceso; cámaras sin cambio |
| U19 | L/ave total mantiene el reparto |
| **U20** | **kWh/ave nunca produce una "potencia pico"; pico solo desde lista de cargas e independiente de kWh/ave** |
| **U21** | **Toda potencia media declara las horas usadas** |
| **U22** | **Subproductos del balance no se contabilizan como SST ni como sólidos del efluente** |
| **U23** | **Lodos PENDIENTES por defecto; sin % de sólidos no hay lodo húmedo; sin modelo de generación no hay lodo seco** |
| **U24** | **La carga sensible del producto no se denomina capacidad frigorífica; carga total PENDIENTE** |
| **U25** | **Grupo electrógeno PENDIENTE sin lista de cargas críticas; nunca % fijo de la planta** |
| **U26** | **Límites regulatorios asociados a jurisdicción y tipo de descarga; solo ejemplo** |
| **U27** | **Métodos A y B independientes; divergencia → alerta de validación de campo** |
| **U28** | **m³/t de producto coherente con L/ave; fuera de rango → alerta** |
| **U29** | **Contraste top-down vs bottom-up: diferencias → alerta, sin ajuste** |

| Mutación | Detectada por |
|---|---|
| M01 agua retenida sumada al consumo | U03, U06, U19 |
| M02 escalado no lineal | U01, U02, U08, U11, U16 |
| M03 se descarga más de lo utilizado | U04, U12 |
| M04 kWe = kWf (sin COP) | U05, U10 |
| M05 inventario calendario sin conversión | U07, U08 |
| M06 almacenamiento = capacidad diaria | U08, U09 |
| M07 sangre no recuperada sin DQO | U15 |
| M08 L/ave leídos como m³/ave | U02, U04, U27, U28 |
| M09 cierre del agua forzado | U01, U04 |
| **M10** potencia pico derivada de kWh/ave | U20 |
| **M11** potencia media sin horas | U21 |
| **M12** SST = subproductos del balance | U01, U22 |
| **M13** lodo húmedo con % de sólidos por defecto | U23 |
| **M14** lodo seco fijo sin modelo | U01, U23 |
| **M15** carga sensible llamada capacidad frigorífica total | el modelo se detiene (variable requerida inexistente) |
| **M16** kWe sin COP declarado | el modelo se detiene (COP ausente) |
| **M17** congelación y almacenamiento en la misma variable/unidad | el modelo se detiene (variable de almacenamiento inexistente) |
| **M18** generador = % fijo de la planta | U25 |
| **M19** límite sin jurisdicción ni tipo de descarga | U26 |
| **M20** método B calibrado con el A | U27 |

## 9. Archivos

**v1.0 (creados):** `11_agua_efluentes/balance_agua.md`, `caracterizacion_efluentes.md`, `alternativas_tratamiento.md`, `modelo_utilities.py`, `escenarios_utilities.csv`, `guia_ramiro.md`, `conclusiones_agua_efluentes.md`, `actualizaciones_gestion_09C.md`, `fuentes_09C.csv` (integrado y retirado en la reconciliación 09); `12_energia_frio/demanda_energia.md`, `sistema_frio.md`, `congelado_almacenamiento.md`, `respaldo_energia.md`, `conclusiones_energia_frio.md`; READMEs de ambas carpetas.
**v1.1 (modificados en la auditoría):** `modelo_utilities.py` (v1.1), `escenarios_utilities.csv` (regenerado, 4.995 filas), `balance_agua.md`, `caracterizacion_efluentes.md`, `alternativas_tratamiento.md`, `guia_ramiro.md`, `conclusiones_agua_efluentes.md`, `actualizaciones_gestion_09C.md`, `README.md`; `12_energia_frio/demanda_energia.md`, `sistema_frio.md`, `congelado_almacenamiento.md`, `respaldo_energia.md`, `conclusiones_energia_frio.md`, `README.md`. `fuentes_09C.csv` sin cambios (integrado a `25_fuentes/` y retirado en la reconciliación 09).
**No modificados:** `00_gestion_proyecto/`, `25_fuentes/`, modelos y CSV de 03, 04, 07 y 23, catálogo de 09A.

## 10. Control de calidad y evaluación

- [x] Rangos de agua rotulados como sensibilidad; cinco aguas; fracción a efluente editable; m³/t.
- [x] Dos métodos de carga independientes con alerta de divergencia.
- [x] Límite regulatorio solo como ejemplo, con jurisdicción y tipo de descarga.
- [x] Subproductos del balance ≠ sólidos del efluente ≠ SST.
- [x] Sangre: principio firme, magnitud como referencia `[PVDP]`.
- [x] Lodos, potencia pico, pico térmico, carga frigorífica total y generador: PENDIENTES explícitos.
- [x] kWf → kWe siempre con COP declarado; congelación ≠ almacenamiento.
- [x] Contraste top-down vs bottom-up preparado para 09A, sin modificar 09A.
- [x] Sin equipos, sin CAPEX/OPEX, sin ubicación.
- [ ] Lectura de originales (bloqueada). [ ] Datos argentinos medidos.

**Evaluación: MEDIA** como modelo y método (30 tests, 20 mutaciones, pendientes explícitos en lugar de cifras inventadas); **BAJA** como evidencia (fuentes `[PVDP]`, ninguna argentina, métodos de efluente divergentes en los extremos). Sirve para **saber qué preguntar a cada sitio y a cada proveedor**, no para diseñar ni presupuestar.
