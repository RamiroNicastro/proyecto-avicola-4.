# Demanda de energía eléctrica y térmica de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Fase 0

> **Alcance:** principales consumidores eléctricos, rangos de kWh/ave, separación entre **potencia (kW)** y **energía (kWh)**, y usos de agua caliente/vapor con equivalentes de combustible. **No** se elige fuente térmica, **no** se seleccionan equipos, **no** se calcula costo ni CAPEX. Energía de granjas (calefacción, ventilación): [`../03_produccion_primaria`](../03_produccion_primaria/README.md), fuera de este modelo.
> **Modelo:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) (bloques `electricidad`, `termico`). **Fuentes:** todas `[PVDP]` ([`../11_agua_efluentes/fuentes_09C.csv`](../11_agua_efluentes/fuentes_09C.csv)); ningún dato argentino.

---

## 1. Potencia (kW) vs energía (kWh)

- **kW = potencia**: cuánta energía se usa **en un instante**. Define el tamaño de la conexión, del transformador y del generador. Se contrata como "potencia" con la distribuidora.
- **kWh = energía**: potencia × horas. Define el consumo que se factura y el combustible.
- Una planta que consume 8.000 kWh en un día de faena no necesita 8.000 kW: si esa energía se reparte en ~14 h, la **potencia media** es ~560 kW y el **pico** puede ser ~800 kW (arranques simultáneos de motores, compresores y bombas).
- Por eso el modelo reporta **siempre las dos** y el test U11 verifica que pico ≥ media y que no se confundan.

## 2. Principales consumidores eléctricos

| Consumidor | Qué incluye | Perfil horario | Reparto ilustrativo del consumo de proceso¹ |
|---|---|---|---|
| **Frío de proceso** (agua helada, hielo, chiller, túneles de enfriado, salas frías) | Compresores, bombas de agua helada, condensadores, ventiladores | Durante la faena y el despiece | **35 %** |
| **Motores de línea** | Noria/transportador aéreo, desplumadoras, evisceradoras, cintas, sierras | Solo horas de faena | 20 % |
| **Aire comprimido** | Accionamientos neumáticos, envasado, limpieza | Faena y limpieza | 10 % |
| **Bombas** | Agua (pozo, presurización), transporte de efluentes, limpieza a presión | Faena y limpieza | 10 % |
| **Climatización de salas** | Despiece y empaque a 10–12 °C, ventilación | Turno | 8 % |
| **Iluminación** | Planta, inspección (niveles altos en puestos veterinarios), exterior | Turno + seguridad | 7 % |
| **Oficinas, vestuarios, comedor, laboratorio** | | Turno | 5 % |
| **Otros** | Talleres, etc. | | 5 % |
| **Congelado** (túneles/IQF) | Compresores de baja temperatura, ventiladores, deshielo | Hasta 20 h/día | Aparte (§3) |
| **Cámaras de almacenamiento** | Refrigerado 0–4 °C y congelado −18/−25 °C | **24 h, 365 días** | Aparte (§3) |
| **Tratamiento de efluentes** | Aireación (si es aerobio), bombas, DAF, deshidratación de lodos | 24 h | Aparte (§3) |

¹ `[SUPUESTO]` didáctico guiado por una fuente que ubica "agua helada y aire comprimido" como el mayor uso eléctrico (FTE-09C-09 `[PVDP]`). **No usar para dimensionar.**

## 3. Rangos y método

| Componente | Bajo | **Medio** | Alto | Base | Origen |
|---|---|---|---|---|---|
| Proceso (faena, enfriado fresco, aire, agua, servicios) | 150 | **250** | 450 kWh/t de peso vivo | t vivas por día operativo | Indicador de referencia `[PVDP]`: UE 152–860 kWh/t faenada; Brasil 165 kWh/t; 1,19 MJ/kg ≈ 330 kWh/t (FTE-09C-09, 09C-03) |
| Congelado | 120 | **190** | 260 kWh/t congelada | t congeladas por día | `[PVDP]` 120–260 kWh/t de ave (FTE-09C-10) |
| Cámaras refrigeradas | 0,5 | **1,0** | 2,0 kWh/(t·día) | t en stock × días calendario | `[SUPUESTO]` sin fuente |
| Cámaras de congelado | 1,5 | **3,0** | 5,0 kWh/(t·día) | idem | `[SUPUESTO]` sin fuente |
| Aireación (si todo el biológico fuera aerobio) | 0,7 | **1,2** | 2,0 kWh/kg DBO removida | DBO que llega al biológico (post-DAF) | `[SUPUESTO]` |

Cautelas: (1) la base del indicador de la UE ("kg de ave faenada") y del brasileño ("tonelada") no está confirmada; (2) el rango alto de la UE (860 kWh/t) probablemente incluye procesados y congelado: el modelo usa 450 como alto y suma congelado aparte, con riesgo de **doble conteo** en el nivel alto (conservador); (3) un extracto de 0,36–1,3 kWh/ave parece referirse a **galpones**, no a plantas, y no se usa.

## 4. Electricidad por escala

`[ESTIMACIÓN]`, perfil de frío P1 (90 % refrigerado, 10 % congelado; 3 días refrigerado y 14 días congelado en días de producción), 250 días de faena. Bajo · **medio** · alto.

| Escala | kWh/día operativo | MWh/año | kWh/ave (promedio anual) | Potencia media / pico kW |
|---|---|---|---|---|
| 2.500 | 1.197 · **2.046** · 3.792 | 302 · **516** · 956 | 0,48 · **0,83** · 1,53 | 83/106 · **140/205** · 256/443 |
| 5.000 | 2.393 · **4.092** · 7.584 | 603 · **1.033** · 1.913 | 0,48 · **0,83** · 1,53 | 166/212 · **280/410** · 513/886 |
| 10.000 | 4.787 · **8.184** · 15.167 | 1.206 · **2.065** · 3.826 | 0,48 · **0,83** · 1,53 | 331/425 · **561/820** · 1.026/1.771 |
| 20.000 | 9.574 · **16.368** · 30.334 | 2.412 · **4.130** · 7.652 | 0,48 · **0,83** · 1,53 | 663/849 · **1.121/1.639** · 2.051/3.543 |

Desglose a 10.000 aves/día (medio): proceso 7.250 kWh/día; congelado 455; aireación 314; cámaras 165 kWh por **día calendario** (funcionan también sin faena). Potencia media = proceso sobre 14 h (8 h netas + 4 h limpieza + 2 h arranque/cierre, `[SUPUESTO]`) + túneles + cámaras + efluentes; pico = media de proceso × 1,5 (`[SUPUESTO]` 1,3–1,8) + cargas continuas.

**Lecturas:**
1. El modelo es **lineal**: kWh/ave no cambia con la escala (test U01). En la realidad una planta más grande suele ser algo más eficiente por ave (economías de escala en compresores, iluminación, servicios): la diferencia **no está cuantificada** y no se supone.
2. **Potencia a pedir a la distribuidora** (orden de magnitud, medio): ~0,2 MW a 2.500 aves/día, ~0,4 MW a 5.000, ~0,8 MW a 10.000, ~1,6 MW a 20.000. Con nivel alto, el doble. En zonas rurales, **1–2 MW** pueden requerir línea de media tensión dedicada o subestación: la potencia disponible puede limitar la escala o la localización (DPV-052).
3. El **perfil de frío** (cuánto se congela y cuántos días se almacena) cambia la energía más que el paso de escala dentro de un mismo perfil: ver [`congelado_almacenamiento.md`](congelado_almacenamiento.md).

## 5. Agua caliente y vapor

### 5.1 Usos

| Uso | Temperatura | Cantidad (medio) | Perfil | Origen de la temperatura |
|---|---|---|---|---|
| **Escaldado** | 51–54 °C (suave) o 60–66 °C (fuerte); modelo 54 / **58** / 62 °C | Reposición 1,2 L/ave + pérdidas (calor que se llevan las aves, evaporación): factor 1,5 / **2** / 3 `[SUPUESTO]` | Horas de faena | FTE-09C-11 `[PVDP]` |
| **Limpieza** | 49–71 °C; modelo 50 / **55** / 60 °C | 60 % del agua de limpieza (5 L/ave) `[SUPUESTO]` | Ventana de limpieza (4 h): **pico térmico** | FTE-09C-11 `[PVDP]` |
| **Sanitización / esterilizadores de cuchillos** | 82 °C (82–93 °C) | 50 % del agua de sanitización (1 L/ave) `[SUPUESTO]` | Turno | FTE-09C-11 `[PVDP]` |
| **Procesos** (escaldado de patas para garras, lavado de cajones, eventual cocción futura) | Variable | No modelado por separado | | — |
| Vapor para **rendering propio** | Vapor saturado | **No incluido**: el caso de referencia no tiene rendering propio (SUP-049) | | [`../07_subproductos/rendering.md`](../07_subproductos/rendering.md) |

### 5.2 Demanda térmica por escala

`[ESTIMACIÓN]` física: calor útil = L × 4,186 kJ/(kg·K) × (T − 18 °C) × factores; combustible = útil / rendimiento de generación y distribución (0,85 / **0,75** / 0,65 `[SUPUESTO]`). Agua de red a 18 °C `[SUPUESTO]` (en invierno más fría → más calor).

| Escala | Calor útil MJ/ave | Energía de combustible GJ/día (bajo · **medio** · alto) | kWh térmicos/día (medio) | Potencia térmica útil pico (medio) |
|---|---|---|---|---|
| 2.500 | 0,46 · **1,00** · 2,31 | 1,4 · **3,3** · 8,9 | 926 | ~90 kW |
| 5.000 | idem | 2,7 · **6,7** · 17,8 | 1.853 | ~180 kW |
| 10.000 | idem | 5,4 · **13,3** · 35,5 | 3.705 | ~350 kW (limpieza 323 + sanitización 31) |
| 20.000 | idem | 10,8 · **26,7** · 71,1 | 7.411 | ~710 kW |

A 10.000 aves/día (medio), el calor útil se reparte: escaldado 4,0 GJ/día (~140 kW térmicos durante 8 h), limpieza 4,6 GJ/día (~320 kW térmicos durante 4 h), sanitización 1,3 GJ/día. **La limpieza, no el escaldado, fija el pico térmico** en este modelo, porque se concentra en pocas horas: un tanque de acumulación de agua caliente desplaza ese pico (decisión de diseño futura).

Contraste: una fuente indica que en plantas de EE.UU. el gas para vapor **supera** en energía al consumo eléctrico (FTE-09C-09 `[PVDP]`); este modelo da ~0,45 MJ de combustible por MJ eléctrico (13,3 GJ vs 29,5 GJ eléctricos a 10.000 aves/día). La diferencia puede deberse a que esas plantas usan vapor para rendering, cocción, lavado de cajones y calefacción, que aquí no se incluyen. **El valor térmico del modelo es probablemente una cota inferior** (DPV propuesta).

### 5.3 Comparación conceptual de fuentes térmicas (no se elige)

Equivalentes diarios a 10.000 aves/día, medio (13,3 GJ de combustible; PCI `[SUPUESTO]`):

| Fuente | Equivalente | Ventajas | Limitaciones | Condicionantes |
|---|---|---|---|---|
| **Gas natural** (red) | ~343 m³/día (PCI 38,9 MJ/m³) | Continuo, limpio, calderas estándar, apto para vapor y agua caliente | Requiere red de gas y capacidad de la distribuidora en el sitio | Factibilidad de conexión (DPV-052) |
| **GLP** | ~290 kg/día (46 MJ/kg) | Disponible sin red | Logística de cisternas, almacenamiento en tanques (normativa de seguridad), mayor dependencia de proveedor | Tanques, habilitación |
| **Electricidad** (resistiva) | ~2.840 kWh/día (98 %); con **bomba de calor** (COP ~3) ~950 kWh/día | Sin combustión; la bomba de calor puede recuperar calor de los condensadores de frío | Aumenta la **potencia** contratada; bomba de calor limitada a ~60–70 °C (no alcanza 82 °C de esterilización sin apoyo) | Potencia disponible |
| **Biomasa** (chip, cáscara, pellet) | ~950 kg/día de chip (14 MJ/kg, muy variable) | Recurso regional (NEA/Litoral) | Caldera más compleja, acopio, cenizas, operador, emisiones; no apta para arranques rápidos | Disponibilidad y calidad del recurso regional |
| **Biogás** del tratamiento anaerobio | No cuantificado | Aprovecha la DQO del efluente | Solo si hay reactor/laguna cubierta; cantidad variable | Decisión de tratamiento |
| **Recuperación de calor** de compresores de frío | No cuantificado | Precalienta agua de limpieza | Depende del sistema de frío | Diseño integrado |

**Técnicamente**, todas pueden producir agua a 60–85 °C; el vapor requiere caldera (gas, GLP o biomasa). La elección depende del sitio (red de gas, potencia, biomasa regional) y del costo, que no se calcula en esta fase.
