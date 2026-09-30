# Congelado y almacenamiento frigorífico: toneladas a enfriar, congelar y guardar

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** toneladas que habría que **congelar por día** y que habría que **almacenar** (refrigerado y congelado) por escala y perfil de destino, con las **dos bases temporales** del modelo de escala v1.1 (días de producción y días calendario de cobertura). **No** se calculan m² ni m³ de cámara, no se dimensionan túneles ni se eligen equipos.
> **Fuente de verdad:** [`../23_plan_expansion/escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv) (bloque `inventario`); el modelo de utilities lo reproduce fila por fila (test **U07**: 640/640 filas) y agrega la capacidad diaria de congelación. Perfiles P1–P3 ilustrativos (SUP-055): **no son demanda**; la exportación de la demanda sigue en 0 (SUP-022).

---

## 1. Capacidad de congelación ≠ capacidad de almacenamiento

- **CAPACIDAD DE CONGELACIÓN** = toneladas **nuevas** que deben **atravesar el proceso de congelación** por unidad de tiempo (t/día operativo; variable `capacidad_congelacion_t_dia`).
- **CAPACIDAD DE ALMACENAMIENTO** = toneladas **ya congeladas** que **permanecen guardadas** (t; variable `capacidad_almacenamiento_congelado_t`).
- **Una cámara capaz de guardar 300 t NO significa poder congelar 300 t/día.**

| | Capacidad de congelación | Capacidad de almacenamiento |
|---|---|---|
| Qué es | t nuevas que los túneles/IQF llevan de +4 °C a −18 °C **cada día de faena** | t ya congeladas que las cámaras **guardan** al mismo tiempo |
| Unidad | **t/día** operativo | **t** (stock) |
| Depende de | Escala × % que se congela | Escala × % que se congela × **días de stock** × base temporal |
| Equipo | Túneles, IQF, placas (potencia frigorífica alta, baja temperatura, tiempo de congelación) | Cámaras (aislamiento, volumen, racks; potencia menor, 24 h) |
| Error típico | Creer que una cámara grande congela: una cámara **mantiene**, no congela | Creer que un túnel grande almacena |

Ejemplo (10.000 aves/día, perfil P3, medio): hay que **congelar 12 t por día de faena**, pero con 14 días de producción en stock hay que **guardar 168 t**. Duplicar los días de stock duplica la cámara y **no cambia** el túnel. Test **U09**: son variables distintas, con unidades distintas, y la de congelación no cambia con los días de stock (mutaciones M06 y M17).

## 2. Toneladas por día (base de todo lo demás)

Producto comestible en **peso comercial** (masa biológica + agua retenida; config. B, 2,9 kg, medio): **6,0 / 12,0 / 24,0 / 47,9 t por día operativo** (4,1 / 8,2 / 16,4 / 32,8 t por día calendario con 250 días de faena).

### 2.1 Capacidad diaria de congelación por perfil (t/día operativo)

| Perfil | Refrig. / congelado / exportación | 2.500 | 5.000 | 10.000 | 20.000 | Calor del producto repartido en 20 h (kWf) |
|---|---|---|---|---|---|---|
| **P1** Mercado interno fresco | 90 / 10 / 0 % | 0,6 | 1,2 | 2,4 | 4,8 | 2 / 5 / 10 / 20 |
| **P2** Interno con congelado | 60 / 40 / 0 % | 2,4 | 4,8 | 9,6 | 19,2 | 10 / 20 / 39 / 79 |
| **P3** Opción exportadora (prueba de diseño) | 50 / 30 / 20 % | 3,0 | 6,0 | 12,0 | 24,0 | 12 / 25 / 49 / 99 |

Calor a extraer: sensible de +4 a −1,5 °C (3,5 kJ/(kg·K)) + latente (74 % de agua × 334 kJ/kg ≈ 247 kJ/kg, método de ASHRAE, FTE-09C-14 `[PVDP]`) + sensible de −1,5 a −18 °C (1,8 kJ/(kg·K)) ≈ **296 kJ/kg de producto**. El **calor latente es ~83 %** del total: congelar es sobre todo congelar el agua del producto. Los envases, ventiladores, desescarche y pérdidas del túnel **no se suman aquí**: pertenecen al balance frigorífico pendiente ([`sistema_frio.md` §2](sistema_frio.md)). La columna de kWf es solo el calor del producto repartido en 20 h; la **potencia instalada** del túnel depende del tiempo de congelación de cada lote (×2,5–5 si se congela en 4–8 h) y queda PENDIENTE. Conversión a kW eléctricos solo con COP declarado (`[SUPUESTO]` 1,4 medio). Energía eléctrica de referencia: 120–260 kWh/t (FTE-09C-10 `[PVDP]`).

## 3. Toneladas a almacenar — dos bases temporales

- **Días de producción en stock:** stock = producción por día **operativo** × días. Responde "¿cuántos días de faena puedo guardar?".
- **Días calendario de cobertura:** stock = despacho promedio por día **calendario** × días = producción por día operativo × (días de faena/365) × días. Responde "¿cuántos días de ventas cubre el stock?". Con 250 días de faena es **68 %** del anterior (82 % con 300).

### 3.1 Congelado (incluye exportación) — 14 días

t (días de producción · días calendario de cobertura, 250 días de faena):

| Perfil | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| P1 | 8 · 6 | 17 · 11 | 34 · 23 | 67 · 46 |
| P2 | 34 · 23 | 67 · 46 | 134 · 92 | **268** · 184 |
| P3 | 42 · 29 | 84 · 57 | 168 · 115 | **336** · 230 |

### 3.2 Refrigerado — 3 días

| Perfil | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| P1 | 16 · 11 | 32 · 22 | 65 · 44 | 129 · 89 |
| P2 | 11 · 7 | 22 · 15 | 43 · 30 | 86 · 59 |
| P3 | 9 · 6 | 18 · 12 | 36 · 25 | 72 · 49 |

### 3.3 Cota superior: todo el comestible, 7 días

7 días de producción · 7 días calendario (250 d): **42 · 29 / 84 · 57 / 168 · 115 / 336 · 230 t** (= [`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) §1, punto 9). Otras combinaciones (1, 3, 7, 14 días × perfiles × bases × 250/300 días): bloque `inventario` de [`../11_agua_efluentes/escenarios_utilities.csv`](../11_agua_efluentes/escenarios_utilities.csv).

**Lecturas:**
1. **El perfil pesa más que la escala:** a 10.000 aves/día, pasar de P1 a P3 multiplica ×5 la congelación diaria y el stock congelado; pasar de 10.000 a 20.000 con el mismo perfil, ×2.
2. El stock congelado de un perfil exportador (P3) a 20.000 aves/día y 14 días (**336 t**) equivale a ~13 contenedores de 25 t (carga de referencia `[PVDP · débil]`, FTE-135). Consolidar lotes de exportación exige almacenamiento, no solo congelación.
3. Los días de stock **no** están validados: dependen de vida útil (DPV-078), frecuencia de despacho, mix de clientes y lotes de exportación (DPV-085). **No se calculan m² de cámara** hasta tener esos datos, densidad de estiba y sistema de racks.

## 4. Qué se congela: producto exportable, subproductos, garras, menudencias

| Material | t/día operativo (2.500 / 5.000 / 10.000 / 20.000) | Frío necesario | Observación |
|---|---|---|---|
| **Producto exportable** (entero, pata-muslo, pechuga, alas) | Según perfil: exportación P3 = 20 % del comestible → 1,2 / 2,4 / 4,8 / 9,6 | Congelado ≤ −18 °C (FTE-135 `[PVDP]`) y almacenamiento hasta completar contenedor | Exportación = 0 en la demanda (SUP-022); P3 es una **prueba de diseño** |
| **Garras** (A + segunda) | 0,25 / 0,51 / 1,01 / 2,02 | Si se exportan, **siempre congeladas**; mercado interno puede ser refrigerado | Llenar 25 t de garras grado A toma ~118 días de faena a 2.500 aves/día y ~15 a 20.000 ([`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) §1, punto 8): **stock largo** |
| **Menudencias** (hígado, corazón, molleja) | 0,27 / 0,55 / 1,09 / 2,18 | Muy perecederas: refrigerado corto o congelado | Parte puede congelarse para pet food o exportación (África) |
| **Subproductos perecederos para rendering** (sangre, vísceras, cabezas; sin plumas) | 0,73 / 1,46 / 2,92 / 5,84 | **Refrigerado** si no se retiran en el día (no congelado) | Stock de 3 días = 2,2 / 4,4 / 8,8 / 17,5 t (SUP-056); requiere cámara separada del producto (SANDACH/categorías) |

Garras y menudencias **ya están dentro del comestible** (clase B): el modelo las muestra como información (`*_informativo`) y **no las suma** al perfil para no duplicar (ver `modelo_utilities.py`, bloque `congelado`). Si se decide congelar el 100 % de garras y 50 % de menudencias sin cambiar el perfil del resto, la congelación diaria sube ~1,6 t/día a 10.000 aves/día.

## 5. Energía de almacenamiento

`[SUPUESTO]` 1,0 kWh/(t·día) refrigerado y 3,0 kWh/(t·día) congelado (medio; 0,5–2 y 1,5–5). A 10.000 aves/día: P1 → 165 kWh/día calendario; P2 → 305; P3 → 369. Las cámaras funcionan **365 días**, aunque la planta faene 250 (test U18). Son energía **ilustrativa** (kWh), no potencia de cámara; son las cargas que **no pueden cortarse** ([`respaldo_energia.md`](respaldo_energia.md)).
