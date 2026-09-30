# Demanda de energía eléctrica y térmica de la planta de faena

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** principales consumidores eléctricos, **energía diaria (kWh)** por escala y **potencia media equivalente**; usos de agua caliente/vapor con **energía térmica diaria (MJ)** y equivalentes de combustible. **La potencia pico, la potencia contratada, el transformador, la caldera y el grupo electrógeno NO se calculan aquí**: quedan pendientes de una lista de cargas y de un perfil horario. No se elige fuente térmica ni se seleccionan equipos; no se calcula costo ni CAPEX. Energía de granjas: [`../03_produccion_primaria`](../03_produccion_primaria/README.md), fuera de este modelo.
> **Modelo:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) v1.1 (bloques `electricidad`, `termico`). **Fuentes:** todas `[PVDP]` ([`../11_agua_efluentes/fuentes_09C.csv`](../11_agua_efluentes/fuentes_09C.csv)); ningún dato argentino. Los indicadores kWh/ave y MJ/ave son de **sensibilidad preliminar**.

---

## 1. Energía (kWh) → potencia media equivalente (kW) ≠ potencia pico

| Magnitud | Qué es | Cómo se obtiene en este estudio | Estado |
|---|---|---|---|
| **Energía diaria** (kWh/día) | Lo que se consume en un día de faena | aves/día × kWh/ave (indicador top-down) | Calculada (sensibilidad) |
| **Potencia media equivalente bajo X horas** (kW) | Energía diaria repartida uniformemente en X horas | kWh/día ÷ X h | Calculada; el nombre de la variable declara las horas (`_bajo_14h`, `_bajo_24h`) |
| **Potencia pico / demanda máxima** (kW, kVA) | Máximo simultáneo real | Lista de cargas: equipo, kW nominal, factor de carga, simultaneidad, arranque, cos φ | **PENDIENTE** (vacía en el CSV) |
| **Potencia contratada, transformador, grupo electrógeno** | Decisiones de diseño y de contrato | Derivan de la demanda máxima y de la política de respaldo | **PENDIENTE** |

**0,8 kWh/ave no permite calcular la potencia pico.** Dos plantas con la misma energía diaria pueden tener picos muy distintos según cuántos compresores, motores y bombas arranquen a la vez. La v1.0 derivaba un "pico" multiplicando la media por un factor: **se retiró** (test **U20**, mutación M10). Toda potencia media declara sus horas (test **U21**, mutación M11). El modelo tiene la función `demanda_maxima(lista_de_cargas)` lista para cuando exista el listado de equipos (§6).

## 2. Principales consumidores eléctricos

| Consumidor | Qué incluye | Perfil horario | Reparto ilustrativo del consumo de proceso¹ |
|---|---|---|---|
| **Frío de proceso** (agua helada, hielo, chiller, salas frías) | Compresores, bombas de agua helada, condensadores, ventiladores | Faena y despiece | 35 % |
| **Motores de línea** | Transportador aéreo, desplumadoras, evisceradoras, cintas, sierras | Solo faena | 20 % |
| **Aire comprimido** | Accionamientos neumáticos, envasado, limpieza | Faena y limpieza | 10 % |
| **Bombas** | Agua (pozo, presurización), efluentes, limpieza a presión | Faena y limpieza | 10 % |
| **Climatización de salas** | Despiece y empaque a 10–12 °C | Turno | 8 % |
| **Iluminación** | Planta, puestos de inspección, exterior | Turno + seguridad | 7 % |
| **Oficinas, vestuarios, comedor, laboratorio** | | Turno | 5 % |
| **Otros** | Talleres | | 5 % |
| **Congelado** (túneles/IQF) | Compresores de baja temperatura, ventiladores, desescarche | Hasta 20 h/día | Aparte (§3) |
| **Cámaras de almacenamiento** | Refrigerado y congelado | **24 h, 365 días** | Aparte (§3) |
| **Tratamiento de efluentes** | Aireación (si es aerobio), bombas, DAF, deshidratación | 24 h | Aparte (§3) |

¹ `[SUPUESTO]` didáctico guiado por una fuente que ubica "agua helada y aire comprimido" como el mayor uso eléctrico (FTE-09C-09 `[PVDP]`). **No usar para dimensionar.**

## 3. Indicadores de energía (top-down, sensibilidad)

| Componente | Bajo | **Medio** | Alto | Base | Origen |
|---|---|---|---|---|---|
| Proceso (faena, enfriado fresco, aire, agua, servicios) | 150 | **250** | 450 kWh/t PV (0,44 · **0,73** · 1,31 kWh/ave) | t vivas/día op. | `[PVDP]`: UE 152–860 kWh/t; Brasil 165 kWh/t; ~330 kWh/t (FTE-09C-09, 09C-03) |
| Congelado | 120 | **190** | 260 kWh/t congelada | t congeladas/día | `[PVDP]` FTE-09C-10 |
| Cámaras refrigeradas / de congelado | 0,5 / 1,5 | **1,0 / 3,0** | 2,0 / 5,0 kWh/(t·día) | t en stock × días calendario | `[SUPUESTO]` sin fuente |
| Aireación (si todo el biológico fuera aerobio) | 0,7 | **1,2** | 2,0 kWh/kg DBO removida | DBO post-DAF (método A) | `[SUPUESTO]` |

Cautelas: base de los indicadores (kg vivo, carcasa, producto) no confirmada; posible doble conteo de congelado/almacenamiento en el nivel alto; un extracto de 0,36–1,3 kWh/ave parece referirse a galpones y no se usa.

## 4. Energía diaria y potencia media equivalente por escala

`[ESTIMACIÓN]` con perfil de frío P1 (3 d refrigerado / 14 d congelado, días de producción), 250 días de faena. Bajo · **medio** · alto.

| Escala | Energía kWh/día operativo | MWh/año | kWh/ave (promedio anual) | Potencia media equivalente de proceso **bajo 14 h** (kW) | Potencia media equivalente total **bajo 24 h** (kW) | Potencia pico |
|---|---|---|---|---|---|---|
| 2.500 | 1.197 · **2.046** · 3.792 | 302 · **516** · 956 | 0,48 · **0,83** · 1,53 | 78 · **129** · 233 | 50 · **85** · 158 | PENDIENTE |
| 5.000 | 2.393 · **4.092** · 7.584 | 603 · **1.033** · 1.913 | idem | 155 · **259** · 466 | 100 · **171** · 316 | PENDIENTE |
| 10.000 | 4.787 · **8.184** · 15.167 | 1.206 · **2.065** · 3.826 | idem | 311 · **518** · 932 | 199 · **341** · 632 | PENDIENTE |
| 20.000 | 9.574 · **16.368** · 30.334 | 2.412 · **4.130** · 7.652 | idem | 621 · **1.036** · 1.864 | 399 · **682** · 1.264 | PENDIENTE |

14 h = 8 h netas + 4 h de limpieza + 2 h de arranque/cierre (`[SUPUESTO]`). Desglose a 10.000 aves/día (medio): proceso 7.250 kWh/día; congelado 455; aireación 314; cámaras 165 kWh por **día calendario**.

**Lecturas:**
1. El modelo es **lineal**: kWh/ave no cambia con la escala (test U01). Las economías de escala reales no están cuantificadas.
2. **La potencia a pedir a la distribuidora no surge de esta tabla.** La potencia media es un piso: la demanda máxima real será mayor, en una proporción que depende de la lista de cargas. Lo que sí puede preguntarse ya a cada sitio es **cuánta potencia hay disponible y cuánto cuesta ampliarla** (DPV-052).
3. El **perfil de frío** cambia la energía tanto como la escala: ver [`congelado_almacenamiento.md`](congelado_almacenamiento.md).

## 5. Agua caliente y vapor

### 5.1 Usos

| Uso | Temperatura | Cantidad (medio) | Perfil | Origen |
|---|---|---|---|---|
| **Escaldado** | 51–54 °C suave o 60–66 °C fuerte; modelo 54 / **58** / 62 °C | Reposición 1,2 L/ave × factor de pérdidas 1,5 / **2** / 3 `[SUPUESTO]` | Horas de faena | FTE-09C-11 `[PVDP]` |
| **Limpieza** | 49–71 °C; modelo 50 / **55** / 60 °C | 60 % de 5 L/ave `[SUPUESTO]` | Ventana de limpieza | FTE-09C-11 `[PVDP]` |
| **Sanitización / esterilizadores** | 82 °C (82–93 °C) | 50 % de 1 L/ave `[SUPUESTO]` | Turno | FTE-09C-11 `[PVDP]` |
| **Procesos** (escaldado de patas, lavado de cajones, cocción futura) | Variable | No modelado | | — |
| Vapor para **rendering propio** | Vapor saturado | **No incluido** (SUP-049) | | [`../07_subproductos/rendering.md`](../07_subproductos/rendering.md) |

### 5.2 Energía térmica diaria (MJ) vs potencia térmica

~**1 MJ útil por ave** (0,46 · 1,0 · 2,31) es un **consumo térmico preliminar de sensibilidad**. `[ESTIMACIÓN]` física con temperaturas `[PVDP]`/`[SUPUESTO]`; rendimiento 85 / **75** / 65 % `[SUPUESTO]`.

| Escala | Calor útil MJ/día (bajo · **medio** · alto) | Combustible GJ/día (medio) | Gas natural equivalente m³/día (medio) | Potencia térmica media equivalente (medio): escaldado bajo 8 h · limpieza bajo 4 h · sanitización bajo 12 h (kW) | Potencia térmica pico |
|---|---|---|---|---|---|
| 2.500 | 1.152 · **2.501** · 5.774 | 3,3 | 86 | 35 · 81 · 8 | PENDIENTE |
| 5.000 | 2.303 · **5.002** · 11.547 | 6,7 | 171 | 70 · 161 · 16 | PENDIENTE |
| 10.000 | 4.606 · **10.005** · 23.094 | 13,3 | 343 | 140 · 323 · 31 | PENDIENTE |
| 20.000 | 9.213 · **20.009** · 46.188 | 26,7 | 686 | 279 · 645 · 62 | PENDIENTE |

- **MJ/día no define la caldera.** El consumo diario de gas no permite determinar la capacidad de generación sin conocer la **simultaneidad** y el **perfil horario** de escaldado, limpieza, sanitización y otros usos.
- La limpieza **podría** generar una demanda térmica concentrada (en el modelo, 4 h con 60 % de agua caliente); debe compararse con el escaldado y otros usos mediante un **perfil horario**. Un tanque de acumulación puede cambiar por completo esa relación. No se afirma cuál uso fija el pico.
- El valor diario es probablemente una **cota inferior**: una fuente indica que en plantas de EE.UU. el gas para vapor supera en energía al consumo eléctrico (FTE-09C-09 `[PVDP]`); aquí es ~0,45 MJ de combustible por MJ eléctrico (no incluye vapor de rendering, cocción ni lavado de cajones).

### 5.3 Comparación conceptual de fuentes térmicas (no se elige)

Equivalentes diarios a 10.000 aves/día, medio (13,3 GJ de combustible; PCI `[SUPUESTO]`). Son equivalencias de **energía**, no de potencia instalada.

| Fuente | Equivalente diario | Ventajas | Limitaciones | Condicionantes |
|---|---|---|---|---|
| **Gas natural** | ~343 m³/día (38,9 MJ/m³) | Continuo, calderas estándar, vapor y agua caliente | Requiere red y capacidad de la distribuidora | Factibilidad de conexión (DPV-052) |
| **GLP** | ~290 kg/día (46 MJ/kg) | Sin red | Logística, tanques, habilitación | Proveedor regional |
| **Electricidad** | ~2.840 kWh/día resistiva; ~950 kWh/día con bomba de calor (COP ~3) | Sin combustión; recuperación de calor del frío | Aumenta la potencia eléctrica; la bomba de calor no llega a 82 °C sin apoyo | Potencia disponible |
| **Biomasa** | ~950 kg/día de chip (14 MJ/kg, muy variable) | Recurso regional | Caldera compleja, acopio, cenizas, operador | Calidad y regularidad del recurso |
| **Biogás** (tratamiento anaerobio) | No cuantificado | Aprovecha la DQO | Solo con reactor/laguna cubierta | Decisión de tratamiento |
| **Recuperación de calor** de compresores | No cuantificado | Precalienta agua | Depende del sistema de frío | Diseño integrado |

## 6. Del top-down al bottom-up (integración con la sesión 09A)

La sesión 09A dejó en `main` un catálogo conceptual de equipos (`08_maquinaria/matriz_equipos.csv` en `main`, EQ-01 a EQ-76, con columna cualitativa de servicios). **No se modifica desde esta rama.** En la reconciliación posterior se deberá construir, para cada equipo: **EQUIPO 09A → potencia (kW nominal, factor de carga, horas, arranque, cos φ) → agua → aire comprimido → vapor/calor → frío**, a partir de cotizaciones. Con esa tabla el modelo calculará la **demanda máxima** (`demanda_maxima`) y comparará **top-down** (kWh/ave, L/ave, MJ/ave) con **bottom-up** (suma de equipos) mediante `contraste_bottom_up`; diferencias mayores que ×1,5 (`[SUPUESTO]` editable) generan alerta (test **U29**). Detalle en [`../11_agua_efluentes/conclusiones_agua_efluentes.md` §5](../11_agua_efluentes/conclusiones_agua_efluentes.md).
