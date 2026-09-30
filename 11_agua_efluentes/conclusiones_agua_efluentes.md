# Conclusiones — modelo preliminar de utilities (agua, efluentes, energía, frío, congelado, respaldo)

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C, en paralelo) · Base: [`balance_agua.md`](balance_agua.md), [`caracterizacion_efluentes.md`](caracterizacion_efluentes.md), [`alternativas_tratamiento.md`](alternativas_tratamiento.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_utilities.py`](modelo_utilities.py), [`escenarios_utilities.csv`](escenarios_utilities.csv); energía y frío en [`../12_energia_frio/conclusiones_energia_frio.md`](../12_energia_frio/conclusiones_energia_frio.md)

> **No se seleccionan equipos, tecnología de tratamiento, refrigerante, fuente térmica ni generador. No se calcula CAPEX ni OPEX. No se elige ubicación.** Las escalas son escenarios (regla 9).
> **Fuentes:** acceso directo bloqueado (`EGRESS_BLOCKED` en todos los dominios intentados: aidic.it, frontiersin.org, thepoultrysite.com, sedici.unlp.edu.ar, fieldreport.caes.uga.edu, extension.okstate.edu, ina.gov.ar; DPV-009). **Toda cifra externa es `[PVDP]`** (19 fuentes nuevas `FTE-09C-01` a `FTE-09C-19` en [`fuentes_09C.csv`](fuentes_09C.csv), más FTE-181, FTE-135, FTE-157, FTE-016 ya registradas). **Ninguna cifra es una medición argentina.**
> **Sesión en paralelo:** no se modificaron `00_gestion_proyecto/` ni `25_fuentes/`; las propuestas para los registros globales están en [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md).

---

## 1. Hallazgos principales

1. **Agua:** 15 / **25** / 38 L/ave (bajo/medio/alto) → **62 / 125 / 250 / 500 m³/día** (medio) a 2.500 / 5.000 / 10.000 / 20.000 aves/día; rango total 38–760 m³/día. La diferencia entre una planta eficiente y una derrochadora (×2,5) es mayor que duplicar la escala. El **caudal horario de pico** (~38 m³/h a 10.000 aves/día) es lo que el sitio debe poder entregar.
2. **Tres aguas separadas:** utilizada (250 m³/día), descargada (220 m³/día) y retenida en producto (0,86 t/día = **0,34 %** del agua utilizada). El agua retenida nunca calcula consumo (test U03).
3. **Efluentes:** carga específica 50 / **100** / 180 g DQO/ave → **~1.000 kg DQO/día y ~500 kg DBO/día** a 10.000 aves/día (medio), con ~4.500 mg/L de DQO (dentro del rango publicado 1.223–9.695). Con un límite ilustrativo de 250 mg/L (ADA 336/03, pluvial, PBA, `[PVDP]`), la remoción requerida sería **~95 %**: el tratamiento es un sistema principal de la planta.
4. **Sangre y sólidos:** el balance permite retirar en seco ~0,61 kg/ave (**6,1 t/día** a 10.000 aves/día) frente a ~0,11 kg/ave que ya va a efluente o pérdida. Recuperar la sangre evita del orden de **+30 % de DQO** (~300 kg/día); la cifra depende de un único dato `[PVDP]` y no se presenta como reducción medida.
5. **Lodos:** ~2,4 t/día deshidratados a 10.000 aves/día (1,0–5,8): otro flujo diario a retirar, del orden de 40 % adicional sobre los sólidos del balance; el flotado de DAF es rico en grasa y proteína (rendering o biodigestión).
6. **Energía eléctrica:** **~0,8 kWh/ave** (0,5–1,5); a 10.000 aves/día ~8.200 kWh/día operativo, **~2,1 GWh/año**, potencia media ~560 kW y pico **~820 kW** (medio). Potencia a pedir: ~0,2 / 0,4 / 0,8 / 1,6 MW según escala (medio; el doble en alto).
7. **Calor:** ~1,0 MJ útil/ave (0,5–2,3) → ~13 GJ/día de combustible (~340 m³ de gas natural equivalente) a 10.000 aves/día; la **limpieza**, concentrada en pocas horas, fija el pico térmico. Probable **cota inferior** (no incluye vapor de rendering ni lavado de cajones).
8. **Frío:** enfriar el producto fresco pide **~235 kW frigoríficos (~67 TR)** y ~78 kW eléctricos a 10.000 aves/día; ~41 % de esa carga es el agua de reposición del chiller.
9. **Congelado:** lo que más mueve el frío es el **perfil** (qué % se congela y cuántos días se guarda), no la escala: a 10.000 aves/día, de P1 a P3 la congelación diaria pasa de 2,4 a 12 t/día y el stock congelado de 14 días de producción de 34 a 168 t (336 t a 20.000).
10. **Respaldo:** las cargas críticas (cámaras, control, emergencia, efluentes, agua mínima, andén de aves) son **~10 %** de la potencia de la planta (~100 kVA a 10.000 aves/día, P1, medio); sostener toda la planta exige ~1 MVA.
11. **Los servicios pueden fijar la capacidad:** agua por hora, permiso de vuelco, potencia disponible, frío y retiro de subproductos son candidatos a cuello de botella tanto como la línea ([`guia_ramiro.md` §10](guia_ramiro.md)). Son criterios de **localización y escala**, no detalles de ingeniería posterior.

## 2. Escenarios físicos por escala (§16 del encargo)

Base: config. B, 2,9 kg, medio, inmersión, perfil P1, 5 días/semana y 250 días de faena; días **operativos** salvo indicación. Bajo · **medio** · alto. Con 300 días/año los valores diarios no cambian y los anuales suben 20 % (agua medio: 18.750 / 37.500 / 75.000 / 150.000 m³/año; electricidad: 617 / 1.233 / 2.466 / 4.932 MWh/año).

| Variable | 2.500 | 5.000 | 10.000 | 20.000 | Origen |
|---|---|---|---|---|---|
| Agua utilizada m³/día | 38 · **62** · 95 | 75 · **125** · 190 | 150 · **250** · 380 | 300 · **500** · 760 | ESTIMACIÓN (L/ave calibrados a FUENTE `[PVDP]`; reparto SUPUESTO) |
| Caudal pico m³/h (medio) | 9,4 | 18,8 | 37,5 | 75,0 | ESTIMACIÓN con SUPUESTO (12 h, factor 1,8) |
| Agua descargada (efluente) m³/día | 30 · **55** · 90 | 60 · **110** · 180 | 120 · **220** · 361 | 240 · **440** · 722 | ESTIMACIÓN con SUPUESTO (80–95 % a efluente) |
| Agua retenida en producto t/día | 0,21 | 0,43 | 0,86 | 1,71 | ESTIMACIÓN (balance v1.1; SUP-042) |
| DQO kg/día | 125 · **250** · 450 | 250 · **500** · 900 | 500 · **1.000** · 1.800 | 1.000 · **2.000** · 3.600 | ESTIMACIÓN con rangos FUENTE `[PVDP]` |
| DBO₅ kg/día | 62 · **125** · 225 | 125 · **250** · 450 | 250 · **500** · 900 | 500 · **1.000** · 1.800 | idem |
| SST · GyA · NTK kg/día (medio) | 88 · 28 · 12 | 175 · 55 · 25 | 350 · 110 · 50 | 700 · 220 · 100 | idem |
| Sólidos a retirar en seco t/día | 1,5 | 3,0 | 6,1 | 12,2 | ESTIMACIÓN (balance v1.1) |
| DQO evitada por recuperar sangre kg/día | 75 | 150 | 299 | 599 | ESTIMACIÓN con FUENTE `[PVDP]` (FTE-181) |
| Lodos deshidratados t/día | 0,2 · **0,6** · 1,5 | 0,5 · **1,2** · 2,9 | 1,0 · **2,4** · 5,8 | 2,0 · **4,7** · 11,7 | ESTIMACIÓN con SUPUESTO |
| Electricidad kWh/día operativo | 1.197 · **2.046** · 3.792 | 2.393 · **4.092** · 7.584 | 4.787 · **8.184** · 15.167 | 9.574 · **16.368** · 30.334 | ESTIMACIÓN con indicadores FUENTE `[PVDP]` y SUPUESTO |
| Electricidad MWh/año | 302 · **516** · 956 | 603 · **1.033** · 1.913 | 1.206 · **2.065** · 3.826 | 2.412 · **4.130** · 7.652 | idem |
| Potencia media / pico kW (medio) | 140 / 205 | 280 / 410 | 561 / 820 | 1.121 / 1.639 | ESTIMACIÓN con SUPUESTO (factor de pico) |
| Calor: combustible GJ/día | 1,4 · **3,3** · 8,9 | 2,7 · **6,7** · 17,8 | 5,4 · **13,3** · 35,5 | 10,8 · **26,7** · 71,1 | ESTIMACIÓN física con temperaturas FUENTE `[PVDP]` y SUPUESTO |
| Gas natural equivalente m³/día | 35 · **86** · 228 | 70 · **171** · 457 | 139 · **343** · 913 | 279 · **686** · 1.827 | ESTIMACIÓN con PCI SUPUESTO |
| Frío enfriado fresco kWf (TR) | 46 (13) · **59 (17)** · 84 (24) | 91 · **118 (33)** · 168 | 182 · **235 (67)** · 336 | 365 · **471 (134)** · 673 | ESTIMACIÓN con SUPUESTO |
| Producto comestible t/día (peso comercial) | 6,0 | 12,0 | 24,0 | 47,9 | ESTIMACIÓN (balance v1.1) |
| Congelación t/día · P1 / P2 / P3 | 0,6 / 2,4 / 3,0 | 1,2 / 4,8 / 6,0 | 2,4 / 9,6 / 12,0 | 4,8 / 19,2 / 24,0 | ESTIMACIÓN con perfiles SUPUESTO (SUP-055) |
| Stock congelado 14 d (prod · cal) P1 t | 8 · 6 | 17 · 11 | 34 · 23 | 67 · 46 | ESTIMACIÓN (= escenarios_escala.csv) |
| Stock congelado 14 d (prod · cal) P3 t | 42 · 29 | 84 · 57 | 168 · 115 | 336 · 230 | idem |
| Stock refrigerado 3 d (prod · cal) P1 t | 16 · 11 | 32 · 22 | 65 · 44 | 129 · 89 | idem |
| Respaldo cargas críticas kVA (P1) | 12 · **25** · 57 | 24 · **49** · 115 | 48 · **99** · 230 | 95 · **198** · 460 | ESTIMACIÓN con SUPUESTO |

**Separación FUENTE / ESTIMACIÓN / SUPUESTO:** el CSV tiene una columna `origen` con uno de esos tres valores en cada fila y una columna `clasificacion` con la etiqueta completa (`[PVDP]` cuando proviene de una fuente no leída en su original); el bloque `parametros` lista cada parámetro con su referencia.

## 3. Tratamiento conceptual

Prevención en origen (sangre, transporte en seco) → pretratamiento (rejas/tamices, grasas, **ecualización**, **DAF**) → biológico (anaerobio, aerobio o combinación) → pulido según vuelco → lodos a rendering/compost/biodigestión/disposición. La elección depende de **terreno, carga, normativa del sitio, olor/vecindad, energía disponible y operación** ([`alternativas_tratamiento.md`](alternativas_tratamiento.md) §3). **No se elige.**

## 4. Principales incertidumbres

| # | Incertidumbre | Efecto | Registro |
|---|---|---|---|
| 1 | **Agua por ave** en plantas argentinas (15–38 L/ave es un rango de EE.UU./Brasil) | ×2,5 en agua, efluente y tratamiento | DPV-067 |
| 2 | **Carga específica** (g DQO/ave) y su relación con la recuperación de sangre | ×3,6 en carga orgánica | DPV-067 |
| 3 | **Límites de vuelco** del sitio y cuerpo receptor | Define el grado de tratamiento (del pretratamiento a la remoción de N y P) | DPV-067; nueva DPV |
| 4 | **Disponibilidad y calidad del agua** (caudal, As, dureza, Fe) | Puede limitar la escala o exigir potabilización | DPV-053 |
| 5 | **Potencia eléctrica** disponible y calidad de red | Puede limitar la escala o la localización | DPV-052 |
| 6 | Indicadores de kWh/t (base y alcance no confirmados; posible doble conteo en el nivel alto) | ×3 en electricidad | Nueva DPV |
| 7 | Demanda térmica (el modelo es probable cota inferior) | Tamaño de caldera y combustible | Nueva DPV |
| 8 | Balance frigorífico (bottom-up vs indicador: 630 vs ~2.540 kWh/día de frío de proceso) | Tamaño de sala de máquinas | Nueva DPV |
| 9 | **Perfil refrigerado/congelado y días de stock** | ×5 en congelado y cámaras | DPV-085, DPV-078 |
| 10 | Reúso de agua admitido por SENASA | Baja el nivel de consumo | DPV-061 |
| 11 | Lodos: tecnología y receptor | Logística diaria de lodos | Nueva DPV |

## 5. Qué no se hizo

No se eligió tecnología ni proveedor, no se dimensionaron unidades (tanques, DAF, reactores, calderas, compresores, cámaras en m²/m³, generadores), no se calcularon costos, no se eligió sitio. No se leyó ningún documento original (bloqueo de red).

## 6. Qué medir y qué cotizar (lista para campo y proveedores)

### 6.1 Sitio (por cada terreno candidato)

| Tema | Qué pedir / medir | A quién |
|---|---|---|
| **Disponibilidad de agua** | Caudal sostenido de perforación (ensayo de bombeo de 24–72 h), profundidad, acuífero, pozos vecinos; o caudal y presión garantizados por la red | Hidrogeólogo; prestador; autoridad del agua provincial (permiso de explotación) |
| **Análisis de agua** | Físico-químico completo según CAA art. 982 (As, F, nitratos, dureza, Fe, Mn, sales) + microbiológico; temperatura en verano e invierno | Laboratorio habilitado |
| **Caudal de efluente admitido** | ¿Hay colectora cloacal con capacidad? ¿Cuerpo receptor (arroyo, canal, pluvial)? Caudal máximo | Prestador cloacal; autoridad del agua; municipio |
| **Límites de vuelco** | Tabla vigente (DBO, DQO, SST, SSEE, N, P, pH, T, coliformes) por destino (cloaca, pluvial, curso, suelo); canon; plazos del permiso | Autoridad del agua provincial (ADA en PBA, equivalentes en Santa Fe, Córdoba, Entre Ríos, Chaco) |
| **Energía disponible** | Potencia disponible en baja/media tensión, distancia a la línea y a la subestación, obra necesaria, plazos | Distribuidora eléctrica |
| **Potencia** | Factibilidad para 0,2–2 MW según escala y posibilidad de ampliar | Distribuidora |
| **Calidad de red** | Historial de cortes y caídas de tensión (frecuencia, duración) | Distribuidora; vecinos industriales |
| **Gas** | Red de gas natural, caudal (m³/h) y presión disponibles, factibilidad; alternativa GLP (logística, tanques) | Distribuidora de gas; proveedores de GLP |
| **Biomasa** | Disponibilidad regional, calidad, precio y regularidad de chip/cáscara | Proveedores regionales |
| **Terreno para tratamiento** | Superficie disponible para lagunas o planta compacta, distancia a viviendas, vientos dominantes | Relevamiento propio |

### 6.2 Plantas de faena existentes (referencia argentina)

L/ave medidos, caracterización del efluente (crudo, post-DAF, salida), tecnología de tratamiento y su desempeño, kWh/ave y m³ de gas/ave, TR instaladas, refrigerante, horas de limpieza, tamaño del generador. Fuente: visitas técnicas, cámaras sectoriales, INTI, autoridades del agua (declaraciones juradas de efluentes si son públicas).

### 6.3 Cotizaciones de proveedores (fase posterior; sin seleccionar)

| Sistema | Qué pedir, por escala (2.500 / 5.000 / 10.000 / 20.000) y perfil (P1 / P2 / P3) |
|---|---|
| **Frío** | Balance frigorífico (kWf y kWe por carga), alternativa de refrigerante (NH₃, CO₂, cascada, indirecto), COP de diseño con la temperatura de verano del sitio, modularidad, personal requerido |
| **Congelado** | Túneles/IQF: t/día y tiempo de congelación; cámaras: t estáticas, densidad de estiba, kWh/(t·día) |
| **Tratamiento de efluentes** | Tren propuesto (pretratamiento + biológico), superficie, kWh/día, químicos, lodos (t/día y % sólidos), garantía de salida contra el límite del sitio, operación |
| **Agua** | Potabilización según análisis (si hace falta), reserva, presurización |
| **Térmica** | Caldera o calentadores (gas/GLP/biomasa/bomba de calor), acumulación de agua caliente, recuperación de calor del frío |
| **Generador** | Listado de cargas críticas y de planta completa, kVA, autonomía, transferencia automática, N+1 |

## 7. Tests

`python3 11_agua_efluentes/modelo_utilities.py` → **20/20 correctos**; `--mutaciones` → **9/9 detectadas**.

| Test | Qué verifica | Resultado |
|---|---|---|
| U00 | Las masas por ave leídas de `escenarios_escala.csv` son idénticas en las 4 escalas y 2 calendarios | OK |
| U01 | **Escalabilidad:** duplicar aves duplica todo flujo y potencia; los indicadores por ave y % no cambian (369 variables × 3 niveles) | OK |
| U02 | **Unidades:** L↔m³, día↔año, kW↔TR, MJ↔kWh, g/ave↔kg/día, mg/L; L/ave en rango físico | OK |
| U03 | Agua retenida separada: triplicarla no cambia agua utilizada ni descargada | OK |
| U04 | Cierre: utilizada = descargada + no descargada; retenida ≤ no descargada | OK |
| U05 | Orden bajo < medio < alto en agua, efluente, cargas, energía, calor, frío y lodos | OK |
| U06 | Σ etapas = agua utilizada | OK |
| U07 | Inventario = bloque `inventario` de `escenarios_escala.csv` (640/640 filas) | OK |
| U08 | Días calendario = días de producción × días op./365 < días de producción | OK |
| U09 | Capacidad diaria de congelación independiente de los días de stock | OK |
| U10 | kW eléctricos = kW frigoríficos / COP < kW frigoríficos | OK |
| U11 | Potencia pico ≥ media; energía diaria > potencia | OK |
| U12 | Ningún valor negativo ni no finito (4.072 filas) | OK |
| U13 | Ninguna variable económica | OK |
| U14 | 11 entradas inválidas rechazadas (fracción a efluente > 1, L/ave negativo o en m³, perfil que no suma 100 %, etc.) | OK |
| U15 | DQO extra = sangre no recuperada × DQO de la sangre; recuperación de referencia 85 % | OK |
| U16 | Masa que evita el efluente = balance/escala | OK |
| U17 | Perfiles = 100 %; DQO media resultante dentro del rango de fuentes | OK |
| U18 | Sexto día: +50 días de proceso; cámaras sin cambio (365 días) | OK |
| U19 | Cambiar el L/ave total mantiene el reparto por etapa | OK |

| Mutación | Detectada por |
|---|---|
| M01 agua retenida sumada al consumo | U03, U06, U19 |
| M02 escalado no lineal | U01, U02, U08, U16 |
| M03 se descarga más agua de la utilizada | U04, U12 |
| M04 kW eléctrico = kW frigorífico | U10 |
| M05 inventario calendario sin conversión | U07, U08 |
| M06 almacenamiento = capacidad diaria | U08, U09 |
| M07 sangre no recuperada sin DQO | U15 |
| M08 L/ave leídos como m³/ave | U02 |
| M09 potencia pico < media | U11 |

Los modelos previos no se modificaron (el de utilities solo **lee** `escenarios_escala.csv`).

## 8. Archivos

**Creados:** `11_agua_efluentes/balance_agua.md`, `caracterizacion_efluentes.md`, `alternativas_tratamiento.md`, `modelo_utilities.py`, `escenarios_utilities.csv` (4.072 filas), `guia_ramiro.md`, `conclusiones_agua_efluentes.md`, `actualizaciones_gestion_09C.md`, `fuentes_09C.csv`; `12_energia_frio/demanda_energia.md`, `sistema_frio.md`, `congelado_almacenamiento.md`, `respaldo_energia.md`, `conclusiones_energia_frio.md`.
**Modificados:** `11_agua_efluentes/README.md`, `12_energia_frio/README.md` (alcance y documentación del modelo, locales a cada carpeta).
**No modificados:** `00_gestion_proyecto/`, `25_fuentes/registro_fuentes.csv`, `25_fuentes/bibliografia.md`, modelos y CSV de 03, 04, 07 y 23.

## 9. Control de calidad y evaluación

- [x] Agua utilizada, descargada y retenida separadas (U03, U04, M01).
- [x] Toda cifra externa trazada a `FTE-09C-xx` o FTE existente y marcada `[PVDP]`.
- [x] Ningún valor presentado como universal: rangos bajo/medio/alto y contradicciones registradas.
- [x] kW vs kWh y kW frigoríficos vs eléctricos separados (U10, U11).
- [x] Congelación diaria vs almacenamiento estático (U09); dos bases temporales (U07, U08).
- [x] Sin equipos, sin CAPEX/OPEX, sin ubicación (U13).
- [x] Modelo reproducible con parámetros modificables (aves/día, L/ave, % a efluente, carga, % refrigerado/congelado, días y base de inventario) y tests de unidades y escalabilidad.
- [ ] Lectura de documentos originales (bloqueada).
- [ ] Datos argentinos medidos (ninguno).

**Evaluación: MEDIA** como modelo y método (reproducible, trazable, lineal verificado, separación estricta de conceptos, 20 tests y 9 mutaciones); **BAJA** como evidencia numérica (todas las fuentes externas `[PVDP]`, ninguna argentina, varios parámetros supuestos, indicadores energéticos de base incierta). Sirve para **dimensionar órdenes de magnitud, detectar qué servicio puede limitar la escala y saber qué preguntar en cada sitio**, no para diseñar ni presupuestar.
