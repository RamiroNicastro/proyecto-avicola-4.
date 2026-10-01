# Logística de subproductos — evitar camiones medio vacíos y retiros innecesarios

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 12B · Fase 0

> **Alcance:** qué corrientes salen de la planta, cuántas t/día, con qué vehículo, y cómo cambian la ocupación y la cantidad de retiros con cuatro estrategias: **retiro diario**, **cada 2 días**, **acumulación refrigerada** y **salida conjunta**. Las restricciones sanitarias y de degradación no confirmadas se marcan `[PVDP]`.
> **No** se elige receptor, rendering propio ni destino (DEC-027), **no** hay precios ni costos. Masas: balance v1.1 vía [`../07_subproductos/`](../07_subproductos/mapa_subproductos.md) (sin recálculo). Cifras: bloques `subproductos_corrientes`, `subproductos_retiro` y `coproductos_frio` de [`escenarios_logistica.csv`](escenarios_logistica.csv).

---

## 1. Corrientes y grupos logísticos

Partición exacta de los **sólidos y líquidos a retirar** (clase C + decomisos + contenido GI) del balance; la suma de corrientes reproduce `23 §12` (tests L04 y L14). t/día operativo, configuración B trozado:

| Corriente | Grupo | 2.500 | 5.000 | 10.000 | 20.000 | Estado | Vehículo típico | Vida sin frío |
|---|---|---|---|---|---|---|---|---|
| Plumas húmedas | **G1** | 0,60 | 1,21 | 2,41 | 4,83 | Sólido húmedo | Contenedor estanco / volcador | Horas a 1 día `[PVDP]` |
| Sangre recuperada | **G2** | 0,21 | 0,42 | 0,84 | 1,68 | **Líquido** | Cisterna | Horas `[PVDP]` |
| Vísceras no comestibles | **G3** | 0,33 | 0,65 | 1,31 | 2,61 | Sólido húmedo | Contenedor estanco | Horas `[PVDP]` |
| Cabezas | G3 | 0,18 | 0,36 | 0,73 | 1,45 | Sólido | Contenedor estanco | Horas `[PVDP]` |
| Otros C (garras de descarte, piel/grasa a rendering) | G3 | 0,01 | 0,03 | 0,05 | 0,11 | Sólido | Contenedor estanco | Horas `[PVDP]` |
| Decomisos + contenido GI | **G4** | 0,19 | 0,37 | 0,75 | 1,50 | Sólido húmedo | Contenedor **segregado** | Horas; destino según normativa (DPV-066) |
| **Total a retirar (B)** | | **1,52** | **3,04** | **6,08** | **12,17** | | | |
| Total con configuración C (+ huesos 0,83 / 1,65 / 3,31 / 6,62) | | 2,35 | 4,70 | 9,39 | 18,79 | | | |
| DOA (aves muertas en transporte; kg/día) | G4 | 22 | 44 | 87 | 174 | Sólido | Con G4 si se admite | Fuera del balance (SUP-035) |

**Coproductos comestibles que viajan con el producto (no se suman):** garras 0,25 / 0,51 / 1,01 / 2,02; menudencias 0,27 / 0,55 / 1,09 / 2,18; carcasa-esqueleto 1,02 / 2,05 / 4,10 / 8,19; cuello 0,19 / 0,37 / 0,75 / 1,49 t/día. Van en cadena de frío dentro del producto terminado; **si la carcasa no tiene comprador baja a rendering** (SUP-046) y el flujo G3 casi se triplica.

**Por qué cuatro grupos:** mezclar define el mercado y la habilitación. Plumas mezcladas con sangre o vísceras dejan de ser "harina de plumas" (pierden la excepción para rumiantes, [`../07_subproductos/rendering.md` §3](../07_subproductos/rendering.md)); la sangre es líquida; los decomisos tienen destino restringido. La compatibilidad real depende del **receptor** y de la normativa (DPV-065, DPV-066, DPV-12B-03): los grupos son una hipótesis de trabajo (SUP-12B-16).

## 2. El problema: ocupación de un retiro diario

Ocupación de un retiro **por día de faena** con vehículos de 5 / 10 / 20 t (**barrido**, no capacidad estándar; DPV-084):

| Grupo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| G1 plumas | 12 / 6 / 3 % | 24 / 12 / 6 % | 48 / 24 / 12 % | 97 / 48 / 24 % |
| G2 sangre | 4 / 2 / 1 % | 8 / 4 / 2 % | 17 / 8 / 4 % | 34 / 17 / 8 % |
| G3 vísceras + cabezas | 10 / 5 / 3 % | 21 / 10 / 5 % | 42 / 21 / 10 % | 83 / 42 / 21 % |
| G4 decomisos + GI | 4 / 2 / 1 % | 7 / 4 / 2 % | 15 / 7 / 4 % | 30 / 15 / 7 % |

**Días de faena que tarda en llenarse un vehículo de 10 t** (si se pudiera acumular): plumas 16,6 / 8,3 / 4,1 / 2,1; sangre 47,7 / 23,9 / 11,9 / 6,0; G3 19,2 / 9,6 / 4,8 / 2,4; G4 53,4 / 26,7 / 13,3 / 6,7.

**Lectura:** el material se degrada en **horas** pero tarda **días o semanas** en llenar un camión mediano. Hasta 10.000 aves/día, **ningún grupo llena la mitad de un vehículo de 10 t con retiro diario**. Esa es la tensión central de esta logística: o vehículos chicos, o acumulación con frío, o combinación con otros generadores, o un receptor que acepte retiros chicos.

## 3. Cuatro estrategias

| Estrategia | t por retiro | Retiros/semana (5 d faena) | Requiere frío | Admisibilidad sanitaria |
|---|---|---|---|---|
| **E1 — Retiro diario** | t/día | 5 | No (si se retira dentro del día de faena) | Referencia (`rendering.md` §4: "retiro diario") |
| **E2 — Cada 2 días de faena** | 2 × t/día | 3 | **Sí** (refrigerado; stock = 1 día) | **PVDP**: no confirmado que el receptor y la normativa lo admitan |
| **E3 — Acumulación refrigerada 3 días** | 3 × t/día | 2 | **Sí** (stock = 2 días) | **PVDP**; tiempo máximo refrigerado = PENDIENTE (DPV-12B-03) |
| **E4 — Salida conjunta** | Suma de corrientes compatibles | 5 (o según E2/E3) | Según corriente | Depende de compatibilidad del receptor (SUP-12B-16) |

El modelo deja `admisible_sanitario = PENDIENTE` para E2 y E3 (test L13): **no se asume** que acumular sea posible.

### 3.1 Efecto sobre la ocupación (vehículo de 10 t, barrido)

| Escala | Plumas E1 → E2 → E3 | G3 E1 → E2 → E3 | Stock refrigerado máximo E3 (G3), t |
|---|---|---|---|
| 2.500 | 6 → 12 → 18 % | 5 → 10 → 16 % | 1,04 |
| 5.000 | 12 → 24 → 36 % | 10 → 21 → 31 % | 2,08 |
| 10.000 | 24 → 48 → 72 % | 21 → 42 → 62 % | 4,17 |
| 20.000 | 48 → 97 % → 2 viajes (72 %) | 42 → 83 % → 2 viajes (62 %) | 8,33 |

### 3.2 Salida conjunta (E4)

Si un mismo receptor aceptara todas las corrientes en un mismo vehículo (compartimentos o contenedores separados), el total de 1,52 / 3,04 / 6,08 / 12,17 t/día ocuparía **15 / 30 / 61 / 122 %** de un vehículo de 10 t con retiro diario: a 10.000 aves/día, un solo retiro diario razonablemente cargado; a 20.000, dos. **Es la estrategia que más mejora la ocupación sin acumular**, pero exige (a) un receptor que procese todo, (b) separación física por grupo (G1 sin mezclar, G2 en cisterna, G4 segregado) y (c) confirmación normativa. En la práctica puede implicar **un camión con contenedores intercambiables**: el camión deja contenedores vacíos y retira los llenos (sistema de contenedores rotativos), lo que desacopla la frecuencia de retiro de la ocupación del camión (a validar con receptores).

### 3.3 Otras palancas (sin cuantificar)

- **Vehículo más chico** para escalas de 2.500–5.000 aves/día: mejora la ocupación sin acumular; depende de la oferta del receptor.
- **Consolidar con otros generadores** (otras plantas, carnicerías, frigoríficos de la zona): el receptor ya hace rutas; se paga por retiro, no por camión.
- **Fin de semana:** con faena de lunes a viernes y retiro diario, el viernes debe retirarse el mismo día o el material del viernes queda 3 días calendario: con E1 hace falta retiro en día de faena o frío.
- **Prevención en origen:** recuperar la sangre (85 %) cambia sangre del efluente a G2 (DEC-044); el transporte de plumas y vísceras en seco vs hidráulico modifica el agua adherida y la masa a transportar.
- **Rendering propio** (DEC-027): elimina el transporte de G1–G3 pero agrega una industria; solo se estudiaría con volumen (`07`).

## 4. Restricciones sanitarias y de degradación (estado)

| Restricción | Estado | Registro |
|---|---|---|
| Vida útil de sangre, vísceras y plumas sin frío | "Horas" — orden de magnitud de `07`, sin fuente primaria | `[PVDP]`; DPV-12B-03 |
| Tiempo máximo con refrigeración antes del rendering | **Desconocido** | DPV-12B-03 |
| Habilitación del vehículo de subproductos no aptos para consumo | Res. SENASA 723/2025 incluye transporte de subproductos (extracto) | FTE-234 `[PVDP]`; DPV-12B-11 |
| Destino de decomisos (digestor / grasería) | Decreto 4238/68 caps. XIV y XIX (extracto) | FTE-192 `[PVDP]`; DPV-066 |
| Manifiestos de transporte de residuos/subproductos provinciales | No relevado | DPV-066 |
| Olores y estanqueidad en tránsito y almacenamiento | Cualitativo | — |

## 5. Backhaul

`BACKHAUL_POSIBLE = NO` para vehículos de subproductos no aptos para consumo: no se los usa para insumos ni alimentos (Res. 723/2025, FTE-234 `[PVDP]`; DPV-066). Lo que sí puede ocurrir es el **retorno de contenedores vacíos limpios** del receptor, que no es carga paga.

## 6. Qué decidir y con qué datos

DEC-12B-05 (estrategia de retiro por corriente) depende de: receptores en las zonas candidatas, qué aceptan, con qué frecuencia y vehículo, si pagan o cobran (DPV-065); normativa (DPV-066, DPV-12B-03); escala; localización (12A); y de DEC-027 (rendering propio / tercerizado / venta directa).
