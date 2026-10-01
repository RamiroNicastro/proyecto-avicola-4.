# Logística de subproductos — evitar camiones medio vacíos y retiros innecesarios

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de interpretación) · Sesión 12B · Fase 0

> **Alcance:** qué corrientes salen de la planta, cuántas t/día, con qué vehículo, y cómo cambian la carga por retiro y la cantidad de retiros con cuatro estrategias: **retiro diario**, **cada 2 días**, **acumulación refrigerada** y **salida conjunta**. Las restricciones sanitarias y de degradación no confirmadas se marcan `[PVDP]` o PENDIENTE.
> **No** se elige receptor, rendering propio ni destino (DEC-027), **no** hay precios ni costos. Masas: balance v1.1 vía [`../07_subproductos/`](../07_subproductos/mapa_subproductos.md). Cifras: bloques `subproductos_corrientes`, `subproductos_retiro` y `coproductos_frio` de [`escenarios_logistica.csv`](escenarios_logistica.csv).
> **v1.1:** se separan **capacidad másica (t)** y **capacidad volumétrica (m³)**. Sin densidad aparente validada, la ocupación volumétrica queda PENDIENTE y los porcentajes de este documento se expresan como **fracción de la capacidad másica del vehículo supuesto**. La acumulación se evalúa en cinco dimensiones separadas.

---

## 1. Corrientes y grupos logísticos

Partición exacta de los **sólidos y líquidos a retirar** (clase C + decomisos + contenido GI) del balance; la suma reproduce `23 §12` (tests L04 y L14). t/día operativo, configuración B trozado:

| Corriente | Grupo | 2.500 | 5.000 | 10.000 | 20.000 | Estado | Vehículo típico | Vida sin frío |
|---|---|---|---|---|---|---|---|---|
| Plumas húmedas | **G1** | 0,60 | 1,21 | 2,41 | 4,83 | Sólido húmedo, **baja densidad aparente** | Contenedor estanco / volcador | Horas a 1 día `[PVDP]` |
| Sangre recuperada | **G2** | 0,21 | 0,42 | 0,84 | 1,68 | **Líquido** | Cisterna | Horas `[PVDP]` |
| Vísceras no comestibles | **G3** | 0,33 | 0,65 | 1,31 | 2,61 | Sólido húmedo | Contenedor estanco | Horas `[PVDP]` |
| Cabezas | G3 | 0,18 | 0,36 | 0,73 | 1,45 | Sólido | Contenedor estanco | Horas `[PVDP]` |
| Otros C (garras de descarte, piel/grasa a rendering) | G3 | 0,01 | 0,03 | 0,05 | 0,11 | Sólido | Contenedor estanco | Horas `[PVDP]` |
| Decomisos + contenido GI | **G4** | 0,19 | 0,37 | 0,75 | 1,50 | Sólido húmedo | Contenedor **segregado** | Horas; destino según normativa (DPV-066) |
| **Total a retirar (B)** | | **1,52** | **3,04** | **6,08** | **12,17** | | | |
| Total con configuración C (+ huesos 0,83 / 1,65 / 3,31 / 6,62) | | 2,35 | 4,70 | 9,39 | 18,79 | | | |
| DOA (aves muertas en transporte; kg/día) | G4 | 22 | 44 | 87 | 174 | Sólido | Con G4 si se admite | Fuera del balance (SUP-035) |

**Coproductos comestibles que viajan con el producto (no se suman):** garras 0,25 / 0,51 / 1,01 / 2,02; menudencias 0,27 / 0,55 / 1,09 / 2,18; carcasa-esqueleto 1,02 / 2,05 / 4,10 / 8,19; cuello 0,19 / 0,37 / 0,75 / 1,49 t/día. Si la carcasa no tiene comprador baja a rendering (SUP-046) y G3 casi se triplica.

**Por qué cuatro grupos:** mezclar define el mercado y la habilitación (plumas mezcladas pierden la condición de "harina de plumas", [`../07_subproductos/rendering.md` §3](../07_subproductos/rendering.md); la sangre es líquida; los decomisos tienen destino restringido). La compatibilidad real depende del receptor y de la normativa (DPV-065, DPV-066, DPV-12B-03): los grupos son hipótesis de trabajo (SUP-12B-16).

## 2. Capacidad másica vs capacidad volumétrica

| Concepto | Unidad | Qué limita | Estado en el modelo |
|---|---|---|---|
| **Capacidad másica** | t (o kg) | Peso legal y estructural del vehículo/contenedor | Barrido de escenario 5 / 10 / 20 t (no estándar; DPV-084) |
| **Capacidad volumétrica** | m³ útiles | Volumen del contenedor/caja/cisterna, grado de llenado | **PENDIENTE** (`cap_m3`, DPV-12B-16) |
| **Densidad aparente** por corriente | t/m³ | Convierte t en m³ en el estado real de transporte (temperatura, humedad, escurrido, compactación) | **PENDIENTE** para todas las corrientes (`DENSIDAD_APARENTE_T_M3`, DPV-12B-16) |

Para materiales de baja densidad —**en especial plumas húmedas**, y eventualmente vísceras o residuos en contenedores específicos— la restricción puede ser **volumétrica antes que de peso**: un contenedor puede llenarse en volumen con mucho menos de su capacidad en toneladas. Por eso el modelo calcula por separado:

```
ocupación másica      = t por retiro / (viajes por masa × capacidad másica)
ocupación volumétrica = m³ por retiro / (viajes por volumen × capacidad volumétrica)   ← solo si hay densidad y m³
m³ por retiro         = Σ (t de cada corriente / densidad aparente de esa corriente)
viajes vinculantes    = max(viajes por masa, viajes por volumen)                      ← PENDIENTE si falta uno
```

Si falta la densidad aparente de cualquier corriente del grupo, la ocupación volumétrica y los viajes vinculantes quedan **PENDIENTES** (tests L26 y L13). Los viajes que se informan hoy son **viajes por criterio de masa**: pueden subestimar los reales si el volumen es la restricción.

Datos a relevar por corriente (DPV-12B-16): densidad aparente (t/m³) en el estado de transporte, temperatura, acondicionamiento (escurrido, compactación, triturado), capacidad útil en m³ del contenedor o cisterna y grado de llenado admitido.

## 3. Fracción de la capacidad másica con retiro diario

**Equivale a X % de la capacidad másica del vehículo supuesto (5 / 10 / 20 t, barrido); la ocupación volumétrica está pendiente:**

| Grupo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| G1 plumas | 12 / 6 / 3 % | 24 / 12 / 6 % | 48 / 24 / 12 % | 97 / 48 / 24 % |
| G2 sangre | 4 / 2 / 1 % | 8 / 4 / 2 % | 17 / 8 / 4 % | 34 / 17 / 8 % |
| G3 vísceras + cabezas | 10 / 5 / 3 % | 21 / 10 / 5 % | 42 / 21 / 10 % | 83 / 42 / 21 % |
| G4 decomisos + GI | 4 / 2 / 1 % | 7 / 4 / 2 % | 15 / 7 / 4 % | 30 / 15 / 7 % |

**Días de faena para alcanzar la capacidad másica de 10 t** (si se pudiera acumular): plumas 16,6 / 8,3 / 4,1 / 2,1; sangre 47,7 / 23,9 / 11,9 / 6,0; G3 19,2 / 9,6 / 4,8 / 2,4; G4 53,4 / 26,7 / 13,3 / 6,7. Para las plumas, el volumen podría llenarse antes (PENDIENTE).

**Lectura:** el material se degrada en horas (`[PVDP]`) mientras que, **en masa**, tarda días en completar un vehículo mediano. Esa es la tensión central: vehículos o contenedores chicos, acumulación con condiciones validadas, combinación con otros generadores, o un receptor que acepte retiros chicos.

## 4. Cuatro estrategias

| Estrategia | t por retiro | Retiros/semana (5 d faena) | Requiere frío o recipiente específico |
|---|---|---|---|
| **E1 — Retiro diario** | t/día | 5 | No para la espera dentro del día (sí contenedor estanco) |
| **E2 — Cada 2 días de faena** | 2 × t/día | 3 | **Sí** (stock = 1 día) |
| **E3 — Acumulación refrigerada 3 días** | 3 × t/día | 2 | **Sí** (stock = 2 días) |
| **E4 — Salida conjunta** | Suma de corrientes compatibles | 5 (o según E2/E3) | Según corriente |

### 4.1 Acumulación: cinco preguntas distintas

Consolidar retiros **puede** mejorar la ocupación, pero no se asume que acumular sea posible. El modelo separa (test L28):

| Dimensión | Variable | E1 (diario) | E2 / E3 (acumulación) | Qué la valida |
|---|---|---|---|---|
| **Físicamente posible** (espacio, recipientes, cámara) | `fisicamente_posible` | Sí | **PENDIENTE** | Layout y frío (12C, 12) |
| **Sanitariamente permitido** | `sanitariamente_permitido` | **PENDIENTE** | **PENDIENTE** | Normativa aplicable (DPV-066, DPV-12B-03) |
| **Aceptado por el receptor** (frescura, calidad de la harina, horario) | `aceptado_por_receptor` | **PENDIENTE** | **PENDIENTE** | Requisitos del comprador (DPV-065) |
| **Necesidad de refrigeración / recipiente** | `requiere_frio` | No | Sí | Diseño (12) |
| **Olores y degradación** | `riesgo_olores_degradacion_aumentado` | Base | Aumentado | Ambiental; receptor |

Ninguna dimensión se da por cumplida sin evidencia: todas quedan como DPV hasta conocer los requisitos reales del comprador y la normativa aplicable.

### 4.2 Efecto sobre la fracción de capacidad másica (vehículo de 10 t, barrido)

| Escala | Plumas E1 → E2 → E3 | G3 E1 → E2 → E3 | Stock a mantener en E3 (G3), t |
|---|---|---|---|
| 2.500 | 6 → 12 → 18 % | 5 → 10 → 16 % | 1,04 |
| 5.000 | 12 → 24 → 36 % | 10 → 21 → 31 % | 2,08 |
| 10.000 | 24 → 48 → 72 % | 21 → 42 → 62 % | 4,17 |
| 20.000 | 48 → 97 % → 2 viajes (72 %) | 42 → 83 % → 2 viajes (62 %) | 8,33 |

### 4.3 Salida conjunta (E4)

Si un mismo receptor aceptara todas las corrientes en un mismo vehículo (compartimentos o contenedores separados), el total de 1,52 / 3,04 / 6,08 / 12,17 t/día equivaldría a **15 / 30 / 61 / 122 % de la capacidad másica** de un vehículo de 10 t con retiro diario (volumen pendiente). Exige un receptor que procese todo, separación física por grupo (G1 sin mezclar, G2 en cisterna, G4 segregado) y confirmación normativa. Una variante es el sistema de **contenedores rotativos** (el camión deja vacíos y retira llenos), que desacopla la frecuencia de retiro de la ocupación del camión (a validar con receptores).

### 4.4 Otras palancas (sin cuantificar)

Vehículo o contenedor más chico en escalas de 2.500–5.000 aves/día; consolidar con otros generadores de la zona; resolver el retiro del viernes (o el material queda 3 días calendario); prevención en origen (sangre recuperada, transporte en seco vs hidráulico, DEC-044); rendering propio (DEC-027), que elimina el transporte de G1–G3 pero agrega una industria.

## 5. Restricciones sanitarias y de degradación (estado)

| Restricción | Estado | Registro |
|---|---|---|
| Vida útil de sangre, vísceras y plumas sin frío | "Horas" — orden de magnitud de `07`, sin fuente primaria | `[PVDP]`; DPV-12B-03 |
| Tiempo máximo con refrigeración antes del rendering | Desconocido | DPV-12B-03 |
| Habilitación del vehículo de subproductos no aptos para consumo | La Res. SENASA 723/2025 regula la habilitación sanitaria de los vehículos alcanzados (FTE-234, confirmada en revisión externa); requisitos específicos para cada tipo de subproducto: a precisar | DPV-066 |
| Destino de decomisos (digestor / grasería) | Decreto 4238/68 caps. XIV y XIX (extracto) | FTE-192 `[PVDP]`; DPV-066 |
| Manifiestos provinciales de transporte de residuos/subproductos | No relevado | DPV-066 |
| Densidad aparente y volumen útil | No relevado | DPV-12B-16 |

## 6. Retorno y backhaul

Retorno **con contenedores vacíos (rotativos), sin carga comercial**. `BACKHAUL_POSIBLE = DESHABILITADO_POR_DEFECTO`: supuesto conservador mientras no se verifiquen habilitación y compatibilidad sanitaria (DPV-066); no se afirma una prohibición normativa general.

## 7. Qué decidir y con qué datos

DEC-12B-05 (estrategia de retiro por corriente) depende de: receptores en las zonas candidatas, qué aceptan, con qué frecuencia, vehículo y volumen, si pagan o cobran (DPV-065); normativa (DPV-066, DPV-12B-03); densidad y volumen (DPV-12B-16); escala; localización (12A); y DEC-027.
