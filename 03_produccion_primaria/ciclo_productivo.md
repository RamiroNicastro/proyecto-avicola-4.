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
| Mortalidad en granja (alojamiento → carga) | **8 %** (o más) | **5 %** | **3 %** | `[SUPUESTO]` SUP-026. Un estudio local de Entre Ríos (62 crianzas, FTE-151 `[PVDP]`) registró **7,68 %** en galpones tecnificados y **9,51 %** en convencionales: señal de riesgo a validar, no promedio argentino |
| Mortalidad en transporte (DOA) | 0,5 % | 0,3 % | 0,2 % | `[SUPUESTO]` SUP-026; FTE-156 `[PVDP]` |
| GDP (perfil medio) | ~52–55 g/d | ~58–62 g/d | ~64–68 g/d (cerca del objetivo genético) | `[ESTIMACIÓN]` |
| Uniformidad (CV del peso del lote) | > 12 % | 9–11 % | ≤ 8 % | `[ESTIMACIÓN]` de literatura técnica general; a validar (DPV-044) |
| Uniformidad (% del lote dentro de ±10 % del peso medio) | < 70 % | 70–80 % | > 80 % | `[ESTIMACIÓN]`; a validar (DPV-044) |

**Lectura crítica:**

1. **Señal de riesgo, no promedio argentino.** Se encontró un estudio local de Entre Ríos (FTE-151; 62 crianzas de 15 productores; publicación de 2015, año de los datos a confirmar) con mortalidades de **7,7–9,5 %**, superiores al supuesto medio del modelo (5 %). **Debe validarse si ese desempeño es representativo de operaciones tecnificadas actuales** (DPV-044); no se generaliza a toda Argentina. Por prudencia, el nivel "desfavorable" (8 %) no debe leerse como caso extremo y la sensibilidad incluye 12 % (§7).
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

`[ESTIMACIÓN]` (cálculo; redondeo hacia arriba). **Pasar de 3 % a 8 % de mortalidad exige ~5,4 % más pollitos** (1.086.957 vs 1.030.928 por millón) y el alimento comido por las aves que mueren se pierde. **No confundir pollitos alojados con aves faenadas:** una planta de 10.000 **aves faenadas**/día necesita alojar ~10.330–10.920 pollitos por cada día de faena según el nivel de desempeño (10.558 con 5 % de mortalidad en granja y 0,3 % en transporte).

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

> **Todo lo de esta sección es ESCENARIO, no diseño recomendado.** Las plantas de 2.500 / 5.000 / 10.000 / 20.000 **aves faenadas por día** son **hipotéticas** y sirven para entender órdenes de magnitud. No surgen de la demanda (que hoy no está documentada: `02_clientes_demanda`) ni fijan capacidad (regla 9).
>
> **Versión 1.1 (auditoría 2026-09-29):** se corrigió el cálculo semanal de pollitos y el dimensionamiento de galpones (ver §6.5).

### 6.1 Tres categorías de aves (no mezclar)

```
POLLITOS BB ALOJADOS --(mortalidad en granja, m)--> AVES CARGADAS (salen de granja) --(mortalidad en transporte, DOA)--> AVES FAENADAS
```

- **"Planta de N aves/día" = N aves efectivamente faenadas por día de faena.** Las aves recibidas vivas en planta se consideran todas faenadas; los decomisos ocurren después de la faena y no las reducen.
- Se calcula "subiendo" la cadena: **aves cargadas = aves faenadas / (1 − DOA)**; **pollitos alojados = aves cargadas / (1 − m)**. Es equivalente a aves faenadas = pollitos × (1 − m) × (1 − DOA).

### 6.2 Calendario

- **Semana plena:** semana sin feriados, con todos los días de faena (5 o 6). Es el **ritmo nominal** de la planta y la base para dimensionar galpones y contratos de pollitos.
- **Año:** 365 días = 52,14 semanas. Días de faena/año = **250** con 5 d/semana (5 × 52,14 = 260,7 − ~10,7 días sin faena por feriados) y **300** con 6 d/semana (312,9 − ~12,9) (SUP-025).
- **Promedio semanal anual** = total anual / 52,14: es menor que la semana plena porque incluye las semanas con feriados.

### 6.3 Método (detalle y pruebas en el modelo)

1. aves cargadas/día = aves faenadas/día / (1 − DOA); pollitos/día de faena = aves cargadas/día / (1 − m); × días de faena → **semana plena**;
2. aves faenadas/año = aves faenadas/día × días de faena/año; aves cargadas/año y pollitos/año con las mismas fórmulas;
3. ciclos/año = 365 / (edad + días entre lotes) × 0,97 (encaje de calendario y esperas; los feriados ya están en los días de faena);
4. **capacidad de alojamiento** (plazas de pollitos, suma de todos los galpones) = pollitos/semana plena × 52,14 / ciclos/año: la necesaria para **sostener el ritmo pleno**. En semanas con feriados se alojan menos pollitos, por lo que la **utilización anual de los galpones** es ~0,96;
5. **aves vivas simultáneas** (ley de Little): a ritmo pleno = pollitos/semana plena / 7 × edad × (1 − m/2); promedio anual = pollitos/año / 365 × edad × (1 − m/2);
6. m² de galpón = capacidad × (1 − m) × peso vivo / kg/m² máximo;
7. galpones = m² / tamaño del galpón (1.200, 1.800 y 2.400 m²; SUP-031), **sin redondear** y sin reserva.

**Capacidad de alojamiento ≠ aves simultáneas ≠ producción anual.** La capacidad es lo que cabe en los galpones el día de alojamiento; las aves simultáneas son menos porque los galpones pasan parte del año vacíos; la producción anual = capacidad × ciclos × utilización × supervivencia.

### 6.4 Prueba manual — 10.000 aves faenadas/día, 5 d/semana, perfil y desempeño medios

| Paso | Cálculo | Resultado |
|---|---|---|
| Aves faenadas por semana plena | 10.000 × 5 | **50.000** |
| Aves cargadas por semana plena (DOA 0,3 %) | 50.000 / 0,997 | **50.150** |
| Pollitos BB alojados por semana plena (m 5 %) | 50.150 / 0,95 | **52.790** |
| Control | 50.000 / 0,95 = 52.632 < 52.790 ✔ | — |
| Aves faenadas por año | 10.000 × 250 | 2.500.000 |
| Aves cargadas por año | 2.500.000 / 0,997 | 2.507.523 |
| Pollitos alojados por año | 2.507.523 / 0,95 | 2.639.497 |
| Muertes en granja / en transporte por año | 2.639.497 − 2.507.523 / 2.507.523 − 2.500.000 | 131.975 / 7.523 |
| Pollitos por semana, promedio anual | 2.639.497 / 52,14 | 50.620 |
| Ciclos/año | 365 / (47 + 15) × 0,97 | 5,71 |
| Capacidad de alojamiento | 52.790 × 52,14 / 5,71 (= 52.790 × 62/7 / 0,97) | **482.029 plazas** |
| Utilización anual de galpones | 2.639.497 / (482.029 × 5,71) | 0,959 |
| Aves vivas simultáneas (ritmo pleno / promedio anual) | 52.790/7 × 47 × 0,975 / 2.639.497/365 × 47 × 0,975 | 345.586 / 331.383 |
| m² de galpón | 482.029 × 0,95 × 2,9 / 35 | **37.943 m²** |
| Galpones equivalentes | 37.943 / 1.200 · / 1.800 · / 2.400 | 31,6 · 21,1 · 15,8 |
| Alimento por año | 2.507.523 × 2,9 × 1,70 | **12.362 t** |
| Alimento por semana plena / promedio | 50.150 × 2,9 × 1,70 / 12.362 / 52,14 | 247 t / 237 t |
| Alimento por ave faenada | 12.362 t / 2.500.000 | 4,94 kg |
| Alimento de un ciclo de crianza a ritmo pleno (capital de trabajo físico) | 247 × 47/7 | 1.660 t |
| Agua de bebida | 12.362 × 1,8 | 22.252 m³/año (61 m³/día promedio) |

### 6.5 Corrección respecto de la versión 1

En la versión 1, "pollitos BB/semana" era el total anual (con 250 días de faena) dividido por 52, lo que equivale a solo ~4,8 días de faena por semana: para 10.000 aves faenadas/día daba 50.760, **menos que los 52.632 mínimos** (50.000 / 0,95). La cadena de porcentajes estaba en el sentido correcto; el error era de calendario. Además, la capacidad de galpones se calculaba con ese promedio anual y no con el ritmo de una semana plena. Corregido:

- pollitos/semana plena: 50.760 → **52.790** (+4,0 %); promedio anual: 50.620;
- capacidad de alojamiento, m² y galpones equivalentes: **+4,3 %** (p. ej. 36.383 → 37.943 m²);
- alimento y agua **anuales sin cambio** (dependen de la faena anual); alimento semanal: 238 t → 247 t (semana plena) o 237 t (promedio);
- aves simultáneas: promedio anual sin cambio (331.383); se agrega el valor a ritmo pleno (345.586).

### 6.6 Resultados — perfil medio (47 d, 2,9 kg)

Formato: **favorable / medio / desfavorable** (SUP-026: mortalidad en granja 3/5/8 %, DOA 0,2/0,3/0,5 %, 12/15/20 días entre lotes, 39/35/30 kg/m², FCR 1,60/1,70/1,85).

**a) Flujo de aves**

| Planta (aves **faenadas**/día) | Días/sem | Aves faenadas/semana plena | Aves cargadas/semana plena | **Pollitos BB alojados/semana plena** | Pollitos BB/semana (promedio anual) | Aves faenadas/año | Pollitos BB alojados/año | Muertes en granja/año | Muertes en transporte/año |
|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 5 | 12.500 | 12.525 / 12.538 / 12.563 | 12.912 / 13.197 / 13.655 | 12.382 / 12.655 / 13.094 | 625.000 | 645.621 / 659.874 / 682.762 | 19.369 / 32.994 / 54.621 | 1.253 / 1.881 / 3.141 |
| 5.000 | 5 | 25.000 | 25.050 / 25.075 / 25.126 | 25.825 / 26.395 / 27.310 | 24.764 / 25.310 / 26.188 | 1.250.000 | 1.291.242 / 1.319.749 / 1.365.523 | 38.737 / 65.987 / 109.242 | 2.505 / 3.761 / 6.281 |
| 10.000 | 5 | 50.000 | 50.100 / 50.150 / 50.251 | 51.650 / 52.790 / 54.621 | 49.527 / 50.620 / 52.376 | 2.500.000 | 2.582.485 / 2.639.497 / 2.731.047 | 77.475 / 131.975 / 218.484 | 5.010 / 7.523 / 12.563 |
| 20.000 | 5 | 100.000 | 100.200 / 100.301 / 100.503 | 103.299 / 105.580 / 109.242 | 99.054 / 101.241 / 104.752 | 5.000.000 | 5.164.969 / 5.278.995 / 5.462.093 | 154.949 / 263.950 / 436.967 | 10.020 / 15.045 / 25.126 |
| 2.500 | 6 | 15.000 | 15.030 / 15.045 / 15.075 | 15.495 / 15.837 / 16.386 | 14.858 / 15.186 / 15.713 | 750.000 | 774.745 / 791.849 / 819.314 | 23.242 / 39.592 / 65.545 | 1.503 / 2.257 / 3.769 |
| 5.000 | 6 | 30.000 | 30.060 / 30.090 / 30.151 | 30.990 / 31.674 / 32.773 | 29.716 / 30.372 / 31.426 | 1.500.000 | 1.549.491 / 1.583.698 / 1.638.628 | 46.485 / 79.185 / 131.090 | 3.006 / 4.514 / 7.538 |
| 10.000 | 6 | 60.000 | 60.120 / 60.181 / 60.302 | 61.980 / 63.348 / 65.545 | 59.433 / 60.745 / 62.851 | 3.000.000 | 3.098.981 / 3.167.397 / 3.277.256 | 92.969 / 158.370 / 262.180 | 6.012 / 9.027 / 15.075 |
| 20.000 | 6 | 120.000 | 120.240 / 120.361 / 120.603 | 123.959 / 126.696 / 131.090 | 118.865 / 121.489 / 125.703 | 6.000.000 | 6.197.963 / 6.334.794 / 6.554.512 | 185.939 / 316.740 / 524.361 | 12.024 / 18.054 / 30.151 |

**b) Galpones y aves simultáneas**

| Planta (aves **faenadas**/día) | Días/sem | Capacidad de alojamiento (plazas de pollitos) | Aves vivas simultáneas a ritmo pleno | Aves vivas simultáneas (promedio anual) | m² de galpón | Galpones de 1.200 m² | Galpones de 1.800 m² | Galpones de 2.400 m² |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 5 | 112.199 / 120.507 / 134.742 | 85.397 / 86.396 / 88.018 | 81.888 / 82.846 / 84.401 | 8.093 / 9.486 / 11.983 | 6,7 / 7,9 / 10,0 | 4,5 / 5,3 / 6,7 | 3,4 / 4,0 / 5,0 |
| 5.000 | 5 | 224.399 / 241.014 / 269.485 | 170.794 / 172.793 / 176.035 | 163.776 / 165.692 / 168.801 | 16.185 / 18.971 / 23.966 | 13,5 / 15,8 / 20,0 | 9,0 / 10,5 / 13,3 | 6,7 / 7,9 / 10,0 |
| 10.000 | 5 | 448.797 / 482.029 / 538.969 | 341.589 / 345.586 / 352.071 | 327.551 / 331.383 / 337.602 | 32.371 / 37.943 / 47.932 | 27,0 / 31,6 / 39,9 | 18,0 / 21,1 / 26,6 | 13,5 / 15,8 / 20,0 |
| 20.000 | 5 | 897.594 / 964.058 / 1.077.939 | 683.178 / 691.171 / 704.142 | 655.102 / 662.767 / 675.204 | 64.742 / 75.885 / 95.865 | 54,0 / 63,2 / 79,9 | 36,0 / 42,2 / 53,3 | 27,0 / 31,6 / 39,9 |
| 2.500 | 6 | 134.639 / 144.609 / 161.691 | 102.477 / 103.676 / 105.621 | 98.265 / 99.415 / 101.281 | 9.711 / 11.383 / 14.380 | 8,1 / 9,5 / 12,0 | 5,4 / 6,3 / 8,0 | 4,0 / 4,7 / 6,0 |
| 5.000 | 6 | 269.278 / 289.217 / 323.382 | 204.953 / 207.351 / 211.243 | 196.531 / 198.830 / 202.561 | 19.423 / 22.766 / 28.759 | 16,2 / 19,0 / 24,0 | 10,8 / 12,6 / 16,0 | 8,1 / 9,5 / 12,0 |
| 10.000 | 6 | 538.556 / 578.435 / 646.763 | 409.907 / 414.703 / 422.485 | 393.061 / 397.660 / 405.123 | 38.845 / 45.531 / 57.519 | 32,4 / 37,9 / 47,9 | 21,6 / 25,3 / 32,0 | 16,2 / 19,0 / 24,0 |
| 20.000 | 6 | 1.077.113 / 1.156.870 / 1.293.527 | 819.813 / 829.406 / 844.970 | 786.122 / 795.320 / 810.245 | 77.690 / 91.062 / 115.038 | 64,7 / 75,9 / 95,9 | 43,2 / 50,6 / 63,9 | 32,4 / 37,9 / 47,9 |

`[ESTIMACIÓN]` · ESCENARIO. Alimento y agua por escenario en [`alimentacion.md`](alimentacion.md).

### 6.7 Rango completo (3 perfiles × 3 desempeños × 5–6 días de faena)

| Planta (aves faenadas/día) | Aves faenadas/año | Pollitos BB alojados/semana plena | Capacidad de alojamiento | m² de galpón | Galpones de 1.800 m² | Alimento (t/año) | Agua de bebida (m³/día prom.) |
|---|---|---|---|---|---|---|---|
| 2.500 | 625.000–750.000 | 12.912–16.386 | 95.084–178.584 | 5.676–18.620 | 3,2–10,3 | 2.224–5.049 | 11–25 |
| 5.000 | 1.250.000–1.500.000 | 25.825–32.773 | 190.168–357.168 | 11.352–37.241 | 6,3–20,7 | 4.449–10.097 | 22–50 |
| 10.000 | 2.500.000–3.000.000 | 51.650–65.545 | 380.336–714.336 | 22.703–74.481 | 12,6–41,4 | 8.898–20.195 | 44–100 |
| 20.000 | 5.000.000–6.000.000 | 103.299–131.090 | 760.673–1.428.671 | 45.406–148.963 | 25,2–82,8 | 17.796–40.390 | 88–199 |

**Las combinaciones de supuestos mueven la superficie hasta ~3,3 veces para una misma planta** (el perfil pesado desfavorable con 6 días frente al liviano favorable con 5 días). La cantidad de galpones no puede decidirse sin fijar antes perfil de mercado, tecnología de galpón y clima de la zona.

### 6.8 Contexto de escala

- Una planta de 10.000 aves faenadas/día (5 d/semana) necesita **~52.800 pollitos BB alojados por semana plena**, ≈ **0,26–0,29 %** de la producción nacional de pollitos parrilleros (~18–20 M/semana, FTE-071 `[PVDP]`). En el agregado el insumo existe; **la disponibilidad local, la calidad y los contratos son lo que hay que validar** (DPV-006, DPV-047).
- La granja promedio de Entre Ríos tendría ~1.400 m² (FTE-048) o ~30.500 aves de capacidad (FTE-152), ambos `[PVDP]`. Con esos tamaños, el escenario medio de 10.000 aves faenadas/día (37.943 m²; 482.029 plazas) equivaldría a **~16–27 granjas** de tamaño promedio entrerriano (~16–53 en el rango completo de supuestos). **Inconsistencia detectada:** 30.500 aves en 1.400 m² serían ~22 aves/m², muy por encima de la densidad técnica (12–14 aves/m²); los dos datos probablemente tienen años o universos distintos (regla 18, DPV-055).

---

## 7. Sensibilidad física

Base: planta de 10.000 aves faenadas/día, 5 d/semana, perfil medio (47 d, 2,9 kg), FCR 1,70, mortalidad en granja 5 %, DOA 0,3 %, 15 días entre lotes, 35 kg/m². **Se cambia un parámetro por vez.**

| Variación | Alimento (t/año) | Δ alimento | Pollitos BB alojados/semana plena | Δ pollitos | Capacidad de alojamiento | m² de galpón | Δ m² | Galpones de 1.800 m² | Ciclos/año |
|---|---|---|---|---|---|---|---|---|---|
| **Base** | 12.362 | — | 52.790 | — | 482.029 | 37.943 | — | 21,1 | 5,71 |
| FCR 1,60 | 11.635 | −5,9 % | 52.790 | 0 % | 482.029 | 37.943 | 0 % | 21,1 | 5,71 |
| FCR 1,80 | 13.089 | +5,9 % | 52.790 | 0 % | 482.029 | 37.943 | 0 % | 21,1 | 5,71 |
| FCR 1,90 | 13.816 | +11,8 % | 52.790 | 0 % | 482.029 | 37.943 | 0 % | 21,1 | 5,71 |
| Mortalidad en granja 3 % | 12.362 | 0 % | 51.701 | −2,1 % | 472.090 | 37.943 | 0 % | 21,1 | 5,71 |
| Mortalidad en granja 8 % | 12.362 | 0 % | 54.511 | +3,3 % | 497.747 | 37.943 | 0 % | 21,1 | 5,71 |
| Mortalidad en granja 12 % | 12.362 | 0 % | 56.989 | +8,0 % | 520.372 | 37.943 | 0 % | 21,1 | 5,71 |
| Peso 2,6 kg (misma edad y FCR) | 11.083 | −10,3 % | 52.790 | 0 % | 482.029 | 34.017 | −10,3 % | 18,9 | 5,71 |
| Peso 3,2 kg (misma edad y FCR) | 13.641 | +10,3 % | 52.790 | 0 % | 482.029 | 41.868 | +10,3 % | 23,3 | 5,71 |
| Edad 42 d | 12.362 | 0 % | 52.790 | 0 % | 443.156 | 34.883 | −8,1 % | 19,4 | 6,21 |
| Edad 54 d | 12.362 | 0 % | 52.790 | 0 % | 536.452 | 42.226 | +11,3 % | 23,5 | 5,13 |
| Densidad 30 kg/m² | 12.362 | 0 % | 52.790 | 0 % | 482.029 | 44.266 | +16,7 % | 24,6 | 5,71 |
| Densidad 39 kg/m² | 12.362 | 0 % | 52.790 | 0 % | 482.029 | 34.051 | −10,3 % | 18,9 | 5,71 |
| 10 días entre lotes | 12.362 | 0 % | 52.790 | 0 % | 443.156 | 34.883 | −8,1 % | 19,4 | 6,21 |
| 21 días entre lotes | 12.362 | 0 % | 52.790 | 0 % | 528.677 | 41.614 | +9,7 % | 23,1 | 5,21 |
| 6 días de faena/semana | 14.835 | +20,0 % | 63.348 | +20,0 % | 578.435 | 45.531 | +20,0 % | 25,3 | 5,71 |

`[ESTIMACIÓN]` · ESCENARIO.

**Cómo leerla:**

- **FCR** mueve solo el alimento, pero es el mayor costo: +0,1 punto = **+5,9 %** de alimento (≈ +727 t/año en este escenario).
- **Mortalidad** mueve los pollitos alojados y la capacidad de alojamiento (y el alimento perdido en aves muertas, que el FCR de campo ya incluye). En este modelo **no cambia los m²** porque la densidad está limitada por los kg al final: más mortalidad = más pollitos por m² al alojar. En la realidad, una mortalidad alta suele venir acompañada de peor FCR y peor peso.
- **Peso** mueve alimento y superficie en la misma proporción (y, en la realidad, también el FCR, que empeora con el peso).
- **Edad y días entre lotes** mueven ciclos/año y por lo tanto galpones, no alimento.
- **Densidad** mueve solo galpones: es la variable de superficie más potente (30 vs 39 kg/m² = −23 %), pero está limitada por bienestar, clima y tecnología de galpón.
- **Días de faena por semana** escalan todo linealmente: la misma planta "de 10.000 aves faenadas/día" produce 20 % más con 6 días.

---

## 8. Pruebas automáticas y balances

El modelo ejecuta pruebas en cada corrida y **se detiene si alguna falla** (`python3 modelo_escenarios_produccion.py`). Resultado de la versión 1.1: **todas correctas**.

| Prueba | Qué comprueba | Casos |
|---|---|---|
| A | Pollitos alojados > aves faenadas (semana plena y año) | 72 |
| B | Aves cargadas > aves faenadas cuando DOA > 0 | 72 |
| C | Pollitos alojados > aves cargadas cuando m > 0; y pollitos/semana plena > aves faenadas/semana / (1 − m) | 72 + 72 |
| D | Aumentar la mortalidad (granja +1 y +5 puntos; transporte +0,5 puntos) nunca reduce pollitos ni capacidad | 216 |
| E | Empeorar el FCR nunca reduce el alimento | 72 |
| F | Duplicar la faena duplica todas las variables lineales (aves, capacidad, m², galpones, alimento, agua, aves simultáneas) y no cambia las intensivas (ciclos, utilización, kg/ave) | 72 |
| G | Unidades y balances: faenadas = pollitos × (1 − m) × (1 − DOA); pollitos = cargadas + muertes; promedio semanal × 52,14 = anual; capacidad × ciclos × utilización = pollitos/año; densidad final = kg/m² declarado; alimento = kg vivo × FCR; agua = alimento × 1,8; fases = total; mes × 12 = año | 72 |
| Límite | Sin mortalidad, pollitos = aves faenadas | 1 |
| Fases | El reparto por fases suma 100 % para edades de 35 a 56 días | 22 |

Unidades: aves (cabezas), kg de peso vivo, t (1.000 kg), m² de piso, m³, días, semanas (52,14/año). Base de alimento: **alimento total entregado al lote / kg vivo cargado** (FCR de campo).
