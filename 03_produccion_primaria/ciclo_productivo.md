# Ciclo productivo del pollo parrillero

**Fecha:** 2026-09-29 · **Versión:** 1 · Fase 0 (prefactibilidad)

> **Alcance.** Cómo funciona la crianza del pollo parrillero y qué rangos físicos (edad, peso, conversión, mortalidad, densidad, ciclos) sirven para dimensionar **escenarios**. **No** se fija capacidad de faena, **no** se decide cantidad de galpones y **no** se asume que habrá granjas propias.
> **Fuentes.** La lectura directa de documentos volvió a estar bloqueada por la red del entorno (manuales Cobb/Ross, SENASA, INTA, SAGyP: 2026-09-29). Todo lo tomado de fuentes externas proviene de extractos de buscador y se marca `[PVDP]` (regla 16). Los valores de trabajo de los escenarios son `[ESTIMACIÓN]` o `[SUPUESTO]` y están registrados en [`../00_gestion_proyecto/supuestos.md`](../00_gestion_proyecto/supuestos.md) (SUP-025 a SUP-033).
> **Modelo.** Fórmulas y parámetros en [`modelo_escenarios_produccion.py`](modelo_escenarios_produccion.py); resultados en [`escenarios_produccion.csv`](escenarios_produccion.csv).

---

## 1. El proceso completo, de pollito BB a frigorífico

```
Reproductoras → huevo fértil → INCUBADORA (21 días) → pollito BB (día 0, ~40–45 g)
   → [1] Recepción en granja → [2] Crianza inicial (0–10/14 d) → [3] Crecimiento (≈11–24/28 d)
   → [4] Terminación (≈25 d – faena) → [5] Ayuno prefaena (≈8–12 h totales)
   → [6] Captura → [7] Carga → [8] Transporte → [9] Espera y recepción en frigorífico
   → (granja vacía) limpieza, retiro/tratamiento de cama, desinfección, VACÍO SANITARIO, preparación → nuevo lote
```

| Etapa | Qué ocurre | Qué se controla | Qué puede salir mal |
|---|---|---|---|
| **0. Preparación del galpón** | Cama nueva o tratada (viruta, cáscara de arroz, etc.), desinfección terminada, **precalentamiento** del piso y del aire 24–48 h antes, líneas de agua lavadas y cargadas, alimento en comederos | Temperatura de piso y aire, humedad, calidad de agua | Piso frío: pollitos que no comen ni toman; mortalidad temprana |
| **1. Recepción del pollito BB** | Descarga rápida desde el camión climatizado de la incubadora; distribución en zona de cría (*brooding*) | Temperatura corporal (cloacal), llenado de buche a las 24 h, calidad del pollito (ombligo, deshidratación) | Pollitos de mala calidad o deshidratados: mortalidad de 1.ª semana y lote desparejo |
| **2. Crianza inicial (0–10/14 d)** | Calefacción (criadoras a gas, calefactores), iluminación intensa para estimular consumo, alimento de inicio (migaja), apertura progresiva del galpón | Mortalidad de 7 días, peso a 7 días (objetivo típico: ~4–5 veces el peso inicial `[PVDP]`), uniformidad | Frío, falta de agua, amoníaco, enfermedades inmunosupresoras |
| **3. Crecimiento (≈11–24/28 d)** | Ampliación del espacio, cambio a alimento de crecimiento (pellet), vacunaciones según plan, ventilación creciente | Ganancia diaria, consumo de agua/alimento, calidad de cama | Cama húmeda (pododermatitis), coccidiosis, enteritis |
| **4. Terminación (≈25 d – faena)** | Máxima biomasa por m²; alimento de terminación y, si corresponde, de **retiro** (sin aditivos con período de carencia); máxima ventilación/enfriamiento en verano | Densidad en kg/m², temperatura, consumo, mortalidad diaria | **Golpe de calor** y fallas eléctricas (mortalidad masiva en horas), problemas de patas, ascitis, muerte súbita |
| **5. Ayuno prefaena** | Retiro del alimento (no del agua) antes de la captura para vaciar el intestino | Horas totales sin alimento (granja + captura + transporte + espera): **≈8–12 h** como orden de magnitud `[PVDP]` (FTE-156) | Ayuno corto: contaminación fecal en la faena; largo: merma de peso y deshidratación |
| **6. Captura** | Manual (cuadrillas, de noche o con luz tenue) o mecanizada | Golpes, alas quebradas, tiempo | Hematomas y fracturas que se decomisan o degradan en planta |
| **7. Carga** | En cajones plásticos o módulos | Aves por cajón según peso y clima | Sobrecarga: asfixia y calor |
| **8. Transporte** | Camión abierto o con cortinas; preferentemente de noche en verano | Tiempo de viaje, temperatura, ventilación | Mortalidad en transporte (DOA), merma de peso ([`transporte_aves.md`](transporte_aves.md)) |
| **9. Recepción en frigorífico** | Espera en galpón de recepción ventilado; colgado | Tiempo de espera, DOA, decomisos | Esperas largas en calor |

**Principio de manejo "todo adentro – todo afuera" (*all-in, all-out*):** cada granja aloja aves de **una sola edad** y se vacía por completo antes del próximo lote. Es la base del vacío sanitario y de la bioseguridad ([`bioseguridad.md`](bioseguridad.md)).

---

## 2. Rangos de referencia

Se separan dos cosas que a menudo se mezclan:

- **Perfil de mercado (qué ave se quiere):** peso y edad de faena. Es una **decisión comercial** (DEC-021) ligada al mix (entero, trozado, deshuese; `02_clientes_demanda`).
- **Nivel de desempeño (qué tan bien se produce):** conversión, mortalidad, uniformidad, ganancia diaria **a igual peso**. Es un resultado de genética, manejo, galpón, clima y sanidad.

### 2.1 Perfiles de mercado (peso vivo y edad)

| Perfil | Edad de faena | Peso vivo | Ganancia diaria media (GDP)* | Uso típico | Clasificación |
|---|---|---|---|---|---|
| **Liviano** | 35–40 d (escenarios: **38 d**) | 2,2–2,5 kg (**2,4 kg**) | ~58–63 g/d | Pollo entero chico, rotisería, *griller* de exportación | `[ESTIMACIÓN]` |
| **Medio** | 45–50 d (**47 d**) | 2,7–3,0 kg (**2,9 kg**) | ~55–62 g/d | Pollo entero y trozado del mercado interno argentino | `[ESTIMACIÓN]` con referencias de campo `[PVDP]` |
| **Pesado** | 52–56 d (**54 d**) | 3,2–3,6 kg (**3,4 kg**) | ~58–63 g/d | Deshuese (pechuga, muslo), elaborados, CMS | `[ESTIMACIÓN]` |

\* GDP = (peso vivo − peso del pollito BB) / edad. Con 2,9 kg a 47 d: (2,9 − 0,042) / 47 ≈ 61 g/d.

**Referencias que respaldan los rangos** (todas `[PVDP]`):

- Productor integrado argentino: crianza de **46–50 días hasta ~3 kg** (FTE-050, prensa sectorial).
- Referencia técnica argentina: **~2,7 kg en ~50 días con conversión ~1,6** (FTE-154, fuente comercial).
- Manual genético Cobb 500 (objetivo en condiciones ideales, mixto): **~2,86 kg a 42 días**, GDP ~64 g/d (FTE-140). Los objetivos de los manuales **no son resultados de campo**: el campo argentino faena más tarde y con peor conversión que la tabla genética.
- La demanda usó un rango de **2,6–3,2 kg vivo** (SUP-019). El rango productivo es más amplio (2,2–3,6 kg) porque incluye perfiles liviano y pesado; ambos son compatibles.

### 2.2 Desempeño productivo (a igual perfil)

| Indicador | BAJO desempeño (desfavorable) | MEDIO | ALTO desempeño (favorable) | Clasificación y referencia |
|---|---|---|---|---|
| FCR de campo, perfil liviano (2,4 kg) | 1,73 | 1,58 | 1,48 | `[ESTIMACIÓN]` SUP-028 |
| FCR de campo, perfil medio (2,9 kg) | **1,85** | **1,70** | **1,60** | `[ESTIMACIÓN]` SUP-028; campo AR ~1,6 a 2,7 kg (FTE-154 `[PVDP]`) |
| FCR de campo, perfil pesado (3,4 kg) | 1,97 | 1,82 | 1,72 | `[ESTIMACIÓN]` SUP-028 |
| Consumo acumulado de alimento por ave (medio) | 5,4 kg | 4,9 kg | 4,6 kg | `[ESTIMACIÓN]` = peso × FCR |
| Mortalidad en granja (alojamiento → carga) | **8 %** (o más) | **5 %** | **3 %** | `[SUPUESTO]` SUP-026. Estudio en Entre Ríos: **7,68 %** en galpones tecnificados y **9,51 %** en convencionales (62 crianzas, FTE-151 `[PVDP]`) |
| Mortalidad en transporte (DOA) | 0,5 % | 0,3 % | 0,2 % | `[SUPUESTO]` SUP-026; FTE-156 `[PVDP]` |
| GDP (perfil medio) | ~52–55 g/d | ~58–62 g/d | ~64–68 g/d (cerca del objetivo genético) | `[ESTIMACIÓN]` |
| Uniformidad (CV del peso del lote) | > 12 % | 9–11 % | ≤ 8 % | `[ESTIMACIÓN]` de literatura técnica general; a validar (DPV-044) |
| Uniformidad (% del lote dentro de ±10 % del peso medio) | < 70 % | 70–80 % | > 80 % | `[ESTIMACIÓN]`; a validar (DPV-044) |

**Lectura crítica:**

1. **La mortalidad "media" de 5 % podría ser optimista para Argentina.** El único dato local obtenido (FTE-151, Entre Ríos, fecha a confirmar) muestra 7,7–9,5 %. Por eso el nivel "desfavorable" (8 %) no debe leerse como caso extremo, y la sensibilidad incluye 12 % (§8). Es el dato productivo a validar con mayor prioridad (DPV-044).
2. **Los FCR de campo son supuestos, no datos.** No se obtuvo ningún registro argentino de FCR por zona y tipo de galpón. La diferencia entre el manual genético y el campo puede ser de 0,1–0,3 puntos.
3. Un peor desempeño normalmente **alarga la edad** para llegar al mismo peso. El modelo mantiene la edad fija por perfil para aislar efectos; la sensibilidad a la edad se muestra aparte.

---

## 3. Mortalidad

### 3.1 Tipos de mortalidad

| Tipo | Período | Orden de magnitud | Causas principales | Qué la reduce |
|---|---|---|---|---|
| **Temprana (1.ª semana)** | 0–7 d | 0,5–1,5 % del lote `[ESTIMACIÓN]`; objetivo habitual ≤ 1 % `[PVDP]` | Calidad del pollito (reproductoras jóvenes o viejas, incubación, transporte), onfalitis, frío, deshidratación, falta de acceso a agua/alimento | Contrato con la incubadora con especificación de calidad; precalentamiento; recepción rápida |
| **Durante el crecimiento** | 8–28 d | 1–2 % `[ESTIMACIÓN]` | Enfermedades (Gumboro, bronquitis, coccidiosis, enteritis necrótica, colibacilosis), cama húmeda, amoníaco | Plan sanitario, bioseguridad, ventilación mínima |
| **En terminación** | 29 d – faena | 1–3 % `[ESTIMACIÓN]` | Metabólicas (ascitis, muerte súbita), problemas de patas, calor | Programa de luz, control de ritmo de crecimiento, ventilación y enfriamiento |
| **Por calor (eventos)** | Días de ola de calor, sobre todo con aves pesadas | De cero a **pérdidas de miles de aves en horas** (casos de prensa: 5.000 pollos en Santa Fe; "miles" por caída de tensión con calor extremo en Entre Ríos, 2026-03, FTE-157 `[PVDP]`) | Temperatura y humedad altas + densidad alta + ventilación insuficiente o **corte eléctrico** | Galpón con ventilación túnel y paneles evaporativos, generador con transferencia automática, alarmas, bajar densidad en verano |
| **Por enfermedades exóticas o de notificación** | Cualquiera | IAAP: **eliminación total** del lote y de la granja afectada | Influenza aviar altamente patógena; Newcastle (Argentina libre) | Bioseguridad ([`bioseguridad.md`](bioseguridad.md)) |
| **Por manejo** | Cualquiera | Muy variable | Falla de agua, error de calefacción, CO por combustión, amontonamiento, captura brusca | Procedimientos, capacitación, alarmas, supervisión |
| **En transporte (DOA)** | Captura → planta | 0,1–0,5 % en condiciones normales; > 1 % en condiciones adversas (1,63 % en un estudio de Ecuador, FTE-156 `[PVDP]`) | Calor, sobrecarga, tiempo, lesiones | [`transporte_aves.md`](transporte_aves.md) |

**Referencia de bienestar exigente (UE):** la Directiva 2007/43/CE solo permite densidades de 39–42 kg/m² si la mortalidad diaria acumulada de al menos 7 lotes consecutivos es menor a **1 % + 0,06 % × edad** (FTE-144 `[PVDP]`): 3,5 % a 42 d, 3,8 % a 47 d, 4,2 % a 54 d. Es un buen umbral de "alto desempeño" y muestra que **densidad y mortalidad están ligadas**.

### 3.2 Pollitos a alojar para obtener N aves en la carga

Fórmula: **pollitos alojados = aves a cargar / (1 − mortalidad en granja)**. Para aves llegadas a la planta, dividir además por (1 − DOA).

| Aves a faena (cargadas) | 2 % | 3 % | 5 % | 8 % | 10 % | 15 % |
|---|---|---|---|---|---|---|
| 1.000 | 1.021 | 1.031 | 1.053 | 1.087 | 1.112 | 1.177 |
| 5.000 | 5.103 | 5.155 | 5.264 | 5.435 | 5.556 | 5.883 |
| 10.000 | 10.205 | 10.310 | 10.527 | 10.870 | 11.112 | 11.765 |
| 20.000 | 20.409 | 20.619 | 21.053 | 21.740 | 22.223 | 23.530 |
| 100.000 | 102.041 | 103.093 | 105.264 | 108.696 | 111.112 | 117.648 |
| 1.000.000 | 1.020.409 | 1.030.928 | 1.052.632 | 1.086.957 | 1.111.112 | 1.176.471 |

`[ESTIMACIÓN]` (cálculo; redondeo hacia arriba). **Pasar de 3 % a 8 % de mortalidad exige ~5,4 % más pollitos** (1.086.957 vs 1.030.928 por millón) y el alimento comido por las aves que mueren se pierde. **No confundir pollitos alojados con aves faenadas:** una planta de 10.000 aves/día necesita alojar ~10.500–11.000 pollitos por cada día de faena.

---

## 4. Densidad y bienestar animal

### 4.1 Cómo se expresa la densidad

- **aves/m²** al alojamiento (pollitos por m²) o al final;
- **kg vivo/m²** al final de la crianza, justo antes de la captura. **Es la medida relevante** porque la carga térmica, la calidad de cama y el bienestar dependen de la biomasa, no del número de aves.

Relación: **aves finales/m² = kg/m² máximo / peso vivo final**; aves alojadas/m² = aves finales/m² / (1 − mortalidad).

### 4.2 Referencias

| Referencia | Densidad | Clasificación |
|---|---|---|
| SENASA Res. 575/2018 (bienestar animal en pollos de engorde) | **No fija un número único** según los extractos: exige un Manual de Bienestar Animal por establecimiento que describa el método y la densidad, considerando sistema productivo, calidad de cama, ventilación, bioseguridad, línea genética, edad y peso de comercialización; veterinario responsable (Res. 542/2010) | `[PVDP]` FTE-145. Texto completo pendiente (DPV-046) |
| UE, Directiva 2007/43/CE | **33 kg/m²** general; **39 kg/m²** con requisitos ambientales (anexo II); **42 kg/m²** excepcional con mortalidad baja y controles sin deficiencias | `[PVDP]` FTE-144 |
| Aviagen (manual Ross) | De **~30 kg/m²** (galpón abierto, ventilación natural) a **~42 kg/m²** (paredes sólidas, túnel y enfriamiento evaporativo) | `[PVDP]` FTE-143 |
| Relevamiento SAGyP de granjas (extracto) | **~12 aves/m²** convencional; **~14 aves/m²** automatizado | `[PVDP]` FTE-150 |
| Ensayos argentinos de bienestar | 10–16 aves/m²; "estándar" 14 y "reducida" 12 aves/m² | `[PVDP]` (extractos INTA/UNLu/UNNE; sin registrar como FTE individual) |

Con 2,9 kg, 12–14 aves/m² equivalen a **~35–41 kg/m²**: coherente con el rango técnico.

### 4.3 Diferencias según clima y ventilación

- **Clima cálido (NEA, norte de Santa Fe y Córdoba) o galpón abierto:** menor densidad en verano (≈25–30 kg/m²) o aves más livianas; la alternativa es invertir en túnel y enfriamiento.
- **Clima templado con galpón climatizado/túnel:** 35–39 kg/m² son técnicamente razonables todo el año, sujetos al manual de bienestar y al cliente.
- **Mercados exportadores:** la UE fija máximos; compradores privados (cadenas, UE, Reino Unido) pueden exigir densidades menores, enriquecimiento, luz natural o auditorías de bienestar. Hoy no hay un requisito de exportación identificado que obligue a una densidad concreta para Argentina (DPV-046).

**No se selecciona una densidad.** Los escenarios usan **30 / 35 / 39 kg/m²** (SUP-026).

### 4.4 Superficie necesaria por cada 10.000 aves cargadas por ciclo

| kg/m² máx. | Ave de 2,4 kg | Ave de 2,9 kg | Ave de 3,4 kg |
|---|---|---|---|
| 25 | 960 m² (10,4 av/m²) | 1.160 m² (8,6) | 1.360 m² (7,4) |
| 30 | 800 m² (12,5) | 967 m² (10,3) | 1.133 m² (8,8) |
| 33 | 727 m² (13,8) | 879 m² (11,4) | 1.030 m² (9,7) |
| 35 | 686 m² (14,6) | 829 m² (12,1) | 971 m² (10,3) |
| 39 | 615 m² (16,2) | 744 m² (13,4) | 872 m² (11,5) |
| 42 | 571 m² (17,5) | 690 m² (14,5) | 810 m² (12,4) |

`[ESTIMACIÓN]`. Pasar de 30 a 39 kg/m² reduce la superficie un **23 %**; aves más pesadas necesitan más m² por ave pero menos m² por kg (no hay diferencia por kg a igual kg/m²).

---

## 5. Ciclos por año

### 5.1 Componentes del ciclo de un galpón

| Componente | Días (orden de magnitud) | Observación |
|---|---|---|
| Crianza (alojamiento → captura) | 35–56 | = edad de faena |
| Captura y salida del lote | 1–3 | Más si hay **raleo** (se retiran aves livianas antes y las pesadas días después) |
| Retiro o tratamiento de la cama | 2–5 | Cama reutilizada: compostaje en el galpón; retiro total **una vez por año o cada 5 crianzas** (Res. SENASA 546/2010 y 106/2013, FTE-147 `[PVDP]`) |
| Lavado, desinfección, control de plagas, mantenimiento | 3–6 | |
| **Vacío sanitario** (galpón limpio y vacío) | 5–10 | Mínimo sanitario; más largo tras un problema sanitario |
| Preparación: cama nueva, precalentamiento, llenado de líneas | 1–3 | |
| **Total entre lotes** | **≈10–21** (escenarios: **12 / 15 / 20**) | Referencia: "~2 semanas" de limpieza en Argentina (FTE-152 `[PVDP]`, atribución a confirmar) |

### 5.2 Por qué 365 / edad de faena **no** son los ciclos por año

`365 / 47 = 7,8` supone que el galpón recibe pollitos el mismo día en que salen las aves, sin limpieza ni vacío. En la realidad:

1. hay que sumar el intervalo entre lotes (10–21 días): **365 / (47 + 15) = 5,9**;
2. el calendario no encaja perfecto (feriados, disponibilidad de pollitos de la incubadora, turnos de faena, retiro total de cama anual, arreglos): se aplica una **disponibilidad de 0,97** (SUP-029) → **5,7 ciclos/año**;
3. los ciclos son enteros por galpón en un año dado; el promedio fraccionario vale para un conjunto grande de galpones escalonados.

### 5.3 Ciclos por año según edad y días entre lotes (× 0,97)

| Edad de faena | 10 d | 12 d | 15 d | 18 d | 21 d | 365/edad (incorrecto) |
|---|---|---|---|---|---|---|
| 35 | 7,87 | 7,53 | 7,08 | 6,68 | 6,32 | 10,43 |
| 38 | 7,38 | 7,08 | 6,68 | 6,32 | 6,00 | 9,61 |
| 42 | 6,81 | 6,56 | 6,21 | 5,90 | 5,62 | 8,69 |
| 47 | 6,21 | 6,00 | 5,71 | 5,45 | 5,21 | 7,77 |
| 50 | 5,90 | 5,71 | 5,45 | 5,21 | 4,99 | 7,30 |
| 54 | 5,53 | 5,36 | 5,13 | 4,92 | 4,72 | 6,76 |
| 56 | 5,36 | 5,21 | 4,99 | 4,78 | 4,60 | 6,52 |

**Rango razonable: ~5 a ~7 ciclos/año** (perfil medio: 5,2–6,2). Referencia sectorial: "~6 crianzas anuales" (FTE-152 `[PVDP]`). Usar 365/edad **sobreestima la capacidad de un galpón en 25–40 %**.

---

## 6. Dimensionamiento físico con escenarios

> **Todo lo de esta sección es ESCENARIO, no diseño recomendado.** Las plantas de 2.500 / 5.000 / 10.000 / 20.000 aves/día son **hipotéticas** y sirven para entender órdenes de magnitud. No surgen de la demanda (que hoy no está documentada: `02_clientes_demanda`) ni fijan capacidad (regla 9).

### 6.1 Método (resumen; detalle en el modelo)

1. aves a faena/año = aves/día × días de faena/año (**250** con 5 d/semana; **300** con 6 d/semana; SUP-025);
2. aves cargadas = aves a faena / (1 − DOA); pollitos alojados = aves cargadas / (1 − mortalidad en granja);
3. ciclos/año = 365 / (edad + días entre lotes) × 0,97;
4. **capacidad de alojamiento** (plazas, suma de todos los galpones) = pollitos/año / ciclos/año;
5. **inventario promedio de aves vivas** (aves "en producción simultánea" en promedio) = pollitos/año × edad / 365 × (1 − mortalidad/2);
6. m² de galpón = capacidad × (1 − mortalidad) × peso vivo / kg/m² máximo;
7. galpones = m² / tamaño del galpón (1.200, 1.800 y 2.400 m²; SUP-031), **sin redondear** y sin reserva.

**Capacidad de alojamiento ≠ inventario promedio ≠ producción anual.** La capacidad es lo que cabe en los galpones el día de alojamiento; el inventario promedio es menor porque los galpones pasan parte del año vacíos; la producción anual es la capacidad × ciclos × supervivencia.

### 6.2 Resultados — perfil medio (47 d, 2,9 kg)

Formato: **favorable / medio / desfavorable** (parámetros de SUP-026: mortalidad 3/5/8 %, DOA 0,2/0,3/0,5 %, 12/15/20 días entre lotes, 39/35/30 kg/m², FCR 1,60/1,70/1,85).

| Planta (aves/día) | Días/sem | Aves a faena/año | Pollitos BB/semana | Pollitos BB/año (M) | Capacidad de alojamiento (plazas) | Inventario promedio de aves vivas | m² de galpón | Galpones de 1.200 m² | Galpones de 2.400 m² |
|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 5 | 625.000 | 12.416 / 12.690 / 13.130 | 0,65 / 0,66 / 0,68 | 107.588 / 115.555 / 129.205 | 81.888 / 82.846 / 84.401 | 7.760 / 9.096 / 11.491 | 6,5 / 7,6 / 9,6 | 3,2 / 3,8 / 4,8 |
| 2.500 | 6 | 750.000 | 14.899 / 15.228 / 15.756 | 0,77 / 0,79 / 0,82 | 129.106 / 138.666 / 155.046 | 98.265 / 99.415 / 101.281 | 9.312 / 10.915 / 13.789 | 7,8 / 9,1 / 11,5 | 3,9 / 4,5 / 5,8 |
| 5.000 | 5 | 1.250.000 | 24.832 / 25.380 / 26.260 | 1,29 / 1,32 / 1,37 | 215.177 / 231.110 / 258.410 | 163.776 / 165.692 / 168.801 | 15.520 / 18.192 / 22.981 | 12,9 / 15,2 / 19,1 | 6,5 / 7,6 / 9,6 |
| 5.000 | 6 | 1.500.000 | 29.798 / 30.456 / 31.512 | 1,55 / 1,58 / 1,64 | 258.212 / 277.332 / 310.092 | 196.531 / 198.830 / 202.561 | 18.624 / 21.830 / 27.578 | 15,5 / 18,2 / 23,0 | 7,8 / 9,1 / 11,5 |
| 10.000 | 5 | 2.500.000 | 49.663 / 50.760 / 52.520 | 2,58 / 2,64 / 2,73 | 430.353 / 462.220 / 516.820 | 327.551 / 331.383 / 337.602 | 31.041 / 36.383 / 45.963 | 25,9 / 30,3 / 38,3 | 12,9 / 15,2 / 19,1 |
| 10.000 | 6 | 3.000.000 | 59.596 / 60.911 / 63.024 | 3,10 / 3,17 / 3,28 | 516.424 / 554.663 / 620.184 | 393.061 / 397.660 / 405.123 | 37.249 / 43.660 / 55.155 | 31,0 / 36,4 / 46,0 | 15,5 / 18,2 / 23,0 |
| 20.000 | 5 | 5.000.000 | 99.326 / 101.519 / 105.040 | 5,16 / 5,28 / 5,46 | 860.707 / 924.439 / 1.033.640 | 655.102 / 662.767 / 675.204 | 62.081 / 72.767 / 91.925 | 51,7 / 60,6 / 76,6 | 25,9 / 30,3 / 38,3 |
| 20.000 | 6 | 6.000.000 | 119.192 / 121.823 / 126.048 | 6,20 / 6,33 / 6,55 | 1.032.848 / 1.109.327 / 1.240.368 | 786.122 / 795.320 / 810.245 | 74.497 / 87.320 / 110.310 | 62,1 / 72,8 / 91,9 | 31,0 / 36,4 / 46,0 |

`[ESTIMACIÓN]` · ESCENARIO. Galpones de 1.800 m²: ver CSV.

### 6.3 Rango completo (3 perfiles × 3 desempeños × 5–6 días de faena)

| Planta (aves/día) | Aves a faena/año | Pollitos BB/semana | Capacidad de alojamiento | m² de galpón | Galpones de 1.800 m² | Alimento (t/año) | Agua de bebida (m³/día prom.) |
|---|---|---|---|---|---|---|---|
| 2.500 | 0,63–0,75 M | 12.400–15.800 | 91.000–171.000 | 5.400–17.900 | 3,0–9,9 | 2.200–5.000 | 11–25 |
| 5.000 | 1,25–1,5 M | 24.800–31.500 | 182.000–342.000 | 10.900–35.700 | 6,0–19,8 | 4.400–10.100 | 22–50 |
| 10.000 | 2,5–3,0 M | 49.700–63.000 | 365.000–685.000 | 21.800–71.400 | 12,1–39,7 | 8.900–20.200 | 44–100 |
| 20.000 | 5,0–6,0 M | 99.300–126.000 | 729.000–1.370.000 | 43.500–142.800 | 24,2–79,4 | 17.800–40.400 | 88–199 |

**Las combinaciones de supuestos mueven la superficie hasta ~3,3 veces para una misma planta** (el perfil pesado desfavorable con 6 días frente al liviano favorable con 5 días). La cantidad de galpones no puede decidirse sin fijar antes perfil de mercado, tecnología de galpón y clima de la zona.

### 6.4 Contexto de escala

- Una planta de 10.000 aves/día (5 d/semana) necesita **~50.000 pollitos BB por semana**, ≈ **0,25 %** de la producción nacional de pollitos parrilleros (~18–20 M/semana, FTE-071 `[PVDP]`). En el agregado el insumo existe; **la disponibilidad local, la calidad y los contratos son lo que hay que validar** (DPV-006, DPV-047).
- La granja promedio de Entre Ríos tendría ~1.400 m² (FTE-048) o ~30.500 aves de capacidad (FTE-152), ambos `[PVDP]`. Con esos tamaños, el escenario medio de 10.000 aves/día (36.383 m²; 462.220 plazas) equivaldría a **~15–26 granjas** de tamaño promedio entrerriano (~16–51 en el rango completo de supuestos). **Inconsistencia detectada:** 30.500 aves en 1.400 m² serían ~22 aves/m², muy por encima de la densidad técnica (12–14 aves/m²); los dos datos probablemente tienen años o universos distintos (regla 18, DPV-055).

---

## 7. Sensibilidad física

Base: planta de 10.000 aves/día, 5 d/semana, perfil medio (47 d, 2,9 kg), FCR 1,70, mortalidad 5 %, DOA 0,3 %, 15 días entre lotes, 35 kg/m². **Se cambia un parámetro por vez.**

| Variación | Alimento (t/año) | Δ alimento | Pollitos (M/año) | Δ pollitos | Capacidad de alojamiento | m² de galpón | Δ m² | Galpones de 1.800 m² | Ciclos/año |
|---|---|---|---|---|---|---|---|---|---|
| **Base** | 12.362 | — | 2,64 | — | 462.220 | 36.383 | — | 20,2 | 5,71 |
| FCR 1,60 | 11.635 | −5,9 % | 2,64 | 0 | 462.220 | 36.383 | 0 | 20,2 | 5,71 |
| FCR 1,80 | 13.089 | +5,9 % | 2,64 | 0 | 462.220 | 36.383 | 0 | 20,2 | 5,71 |
| FCR 1,90 | 13.816 | +11,8 % | 2,64 | 0 | 462.220 | 36.383 | 0 | 20,2 | 5,71 |
| Mortalidad 3 % | 12.362 | 0 | 2,59 | −2,1 % | 452.689 | 36.383 | 0 | 20,2 | 5,71 |
| Mortalidad 8 % | 12.362 | 0 | 2,73 | +3,3 % | 477.292 | 36.383 | 0 | 20,2 | 5,71 |
| Mortalidad 12 % | 12.362 | 0 | 2,85 | +8,0 % | 498.987 | 36.383 | 0 | 20,2 | 5,71 |
| Peso 2,6 kg (misma edad y FCR) | 11.083 | −10,3 % | 2,64 | 0 | 462.220 | 32.619 | −10,3 % | 18,1 | 5,71 |
| Peso 3,2 kg (misma edad y FCR) | 13.641 | +10,3 % | 2,64 | 0 | 462.220 | 40.147 | +10,3 % | 22,3 | 5,71 |
| Edad 42 d | 12.362 | 0 | 2,64 | 0 | 424.944 | 33.449 | −8,1 % | 18,6 | 6,21 |
| Edad 54 d | 12.362 | 0 | 2,64 | 0 | 514.406 | 40.491 | +11,3 % | 22,5 | 5,13 |
| Densidad 30 kg/m² | 12.362 | 0 | 2,64 | 0 | 462.220 | 42.447 | +16,7 % | 23,6 | 5,71 |
| Densidad 39 kg/m² | 12.362 | 0 | 2,64 | 0 | 462.220 | 32.652 | −10,3 % | 18,1 | 5,71 |
| 10 días entre lotes | 12.362 | 0 | 2,64 | 0 | 424.944 | 33.449 | −8,1 % | 18,6 | 6,21 |
| 21 días entre lotes | 12.362 | 0 | 2,64 | 0 | 506.951 | 39.904 | +9,7 % | 22,2 | 5,21 |
| 6 días de faena/semana | 14.835 | +20,0 % | 3,17 | +20,0 % | 554.663 | 43.660 | +20,0 % | 24,3 | 5,71 |

`[ESTIMACIÓN]` · ESCENARIO.

**Cómo leerla:**

- **FCR** mueve solo el alimento, pero es el mayor costo: +0,1 punto = **+5,9 %** de alimento (≈ +727 t/año en este escenario).
- **Mortalidad** mueve los pollitos (y el alimento perdido en aves muertas, que el FCR de campo ya incluye). En este modelo **no cambia los m²** porque la densidad está limitada por los kg al final: más mortalidad = más pollitos por m² al alojar. En la realidad, una mortalidad alta suele venir acompañada de peor FCR y peor peso.
- **Peso** mueve alimento y superficie en la misma proporción (y, en la realidad, también el FCR, que empeora con el peso).
- **Edad y días entre lotes** mueven ciclos/año y por lo tanto galpones, no alimento.
- **Densidad** mueve solo galpones: es la variable de superficie más potente (30 vs 39 kg/m² = −23 %), pero está limitada por bienestar, clima y tecnología de galpón.
- **Días de faena por semana** escalan todo linealmente: la misma planta "de 10.000 aves/día" produce 20 % más con 6 días.

---

## 8. Balances verificados

El modelo verifica automáticamente en los 72 escenarios (`verificar_balances`):

1. pollitos alojados ≥ aves cargadas ≥ aves faenadas;
2. capacidad × ciclos/año = pollitos/año (±1 %);
3. densidad final resultante = densidad máxima declarada (kg/m²);
4. alimento = kg vivo cargado × FCR;
5. inicio + crecimiento + terminación = alimento total.

Unidades: aves (cabezas), kg de peso vivo, t (1.000 kg), m² de piso, días. Base de alimento: **alimento total entregado al lote / kg vivo cargado** (FCR de campo).
