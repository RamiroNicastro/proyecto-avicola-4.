# Conclusiones — energía, frío, congelado y respaldo

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Base: [`demanda_energia.md`](demanda_energia.md), [`sistema_frio.md`](sistema_frio.md), [`congelado_almacenamiento.md`](congelado_almacenamiento.md), [`respaldo_energia.md`](respaldo_energia.md); modelo [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) y CSV [`../11_agua_efluentes/escenarios_utilities.csv`](../11_agua_efluentes/escenarios_utilities.csv)

> **No se eligen** fuente térmica, refrigerante, sistema de frío, generador ni proveedores; **no** se calculan CAPEX, OPEX ni m² de cámara; **no** se elige sitio. Toda cifra externa es `[PVDP]`; ninguna es argentina medida.
> Tabla física completa por escala (agua, efluentes, energía, calor, frío, congelado, inventario, respaldo), incertidumbres, lista de qué medir/cotizar, tests y calidad: [`../11_agua_efluentes/conclusiones_agua_efluentes.md`](../11_agua_efluentes/conclusiones_agua_efluentes.md) §2, §4, §6, §7 y §9 (no se duplican aquí).

---

## 1. Energía eléctrica

- **~0,8 kWh/ave** (0,5–1,5), lineal con la escala en el modelo: **2.046 / 4.092 / 8.184 / 16.368 kWh por día operativo** (medio) y **0,5 / 1,0 / 2,1 / 4,1 GWh/año** (250 días).
- **Potencia ≠ energía:** pico estimado **~0,2 / 0,4 / 0,8 / 1,6 MW** (medio; el doble en alto). En zonas rurales, 1–2 MW puede requerir obra de media tensión: la potencia disponible es un criterio de localización (DPV-052).
- Mayores consumidores: frío de proceso, motores de línea, aire comprimido y bombas; congelado, cámaras (365 días) y aireación se suman aparte.

## 2. Agua caliente / vapor

- ~**1,0 MJ útil por ave** (0,5–2,3) para escaldado, limpieza y sanitización → ~3,3 / 6,7 / 13,3 / 26,7 GJ/día de combustible (medio), equivalente a ~86 / 171 / 343 / 686 m³/día de gas natural.
- La **limpieza** (pocas horas, mucha agua caliente) fija el pico térmico (~320 kW térmicos a 10.000 aves/día, medio); acumular agua caliente lo aplana.
- Es probablemente una **cota inferior** (sin vapor de rendering, cocción ni lavado de cajones). Gas natural, GLP, electricidad/bomba de calor, biomasa y biogás son técnicamente aplicables; **no se elige** (DEC-09C-03 propuesta).

## 3. Frío

- **kW frigoríficos ≠ kW eléctricos:** enfriar el producto fresco a 10.000 aves/día pide ~235 kWf (~67 TR) y consume ~78 kWe (COP ~3). Congelar tiene COP ~1,4.
- Enfriado fresco (medio): 59 / 118 / 235 / 471 kWf por escala; el agua de reposición del chiller es ~41 % de esa carga.
- **Brecha no resuelta:** el cálculo físico del enfriado (~630 kWh/día a 10.000 aves/día) es mucho menor que el 35 % del indicador de proceso atribuido a frío (~2.540 kWh/día): falta un balance frigorífico de proveedor (DPV-09C-02 propuesta).
- **Refrigerantes:** amoníaco (eficiente, tóxico, exige personal y sala de máquinas), CO₂ transcrítico (no tóxico, alta presión, menos eficiente en verano caluroso), cascada NH₃/CO₂, sistemas indirectos, HFC en reducción por Kigali (vigente en Argentina desde 2020, congelamiento desde 2024 `[PVDP]`), HFO. A 10.000–20.000 aves/día la práctica industrial tiende a amoníaco o cascada; **no se elige** (DEC-09C-04 propuesta).

## 4. Congelado y almacenamiento

- **Capacidad diaria de congelación** (t/día, túneles) ≠ **capacidad estática** (t, cámaras). Más días de stock agrandan la cámara, no el túnel.
- Congelación diaria (P1 / P2 / P3): 0,6/2,4/3,0 · 1,2/4,8/6,0 · 2,4/9,6/12,0 · 4,8/19,2/24,0 t por día de faena.
- Stock congelado de 14 días (días de producción · días calendario): P3 a 20.000 aves/día **336 · 230 t**; P1 a 10.000 **34 · 23 t**. Reproduce el modelo de escala (640/640 filas).
- **El perfil de destino pesa más que la escala** (×5 entre P1 y P3 a igual escala). Garras (siempre congeladas si se exportan; hasta ~118 días de faena para llenar un contenedor a 2.500 aves/día) y menudencias son los subproductos comestibles que más empujan el congelado.

## 5. Respaldo

- Cargas críticas (andén de aves, cámaras, control y seguridad, iluminación de emergencia, agua mínima, efluentes): **~25 / 49 / 99 / 198 kVA** (P1, medio), ~10 % de la potencia de la planta; sostener toda la planta: ~0,26 / 0,51 / 1,0 / 2,0 MVA.
- La decisión es **qué seguir haciendo durante un corte**, no el generador (DEC-09C-05 propuesta). La calidad de la red del sitio define si hace falta N+1.

## 6. Qué debe ser verdad en un sitio (energía y frío)

| Requisito | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Potencia eléctrica disponible (pico, medio · alto) | 0,2 · 0,45 MW | 0,4 · 0,9 MW | 0,8 · 1,8 MW | 1,6 · 3,5 MW |
| Energía térmica (combustible, medio) | 3,3 GJ/día | 6,7 GJ/día | 13,3 GJ/día | 26,7 GJ/día |
| Frío de enfriado fresco (medio) | 17 TR | 33 TR | 67 TR | 134 TR |
| Respaldo crítico (P1, medio) | 25 kVA | 49 kVA | 99 kVA | 198 kVA |

## 7. Archivos de esta carpeta

`demanda_energia.md`, `sistema_frio.md`, `congelado_almacenamiento.md`, `respaldo_energia.md`, `conclusiones_energia_frio.md` (creados); `README.md` (actualizado). Modelo, CSV, fuentes y propuestas de gestión en `../11_agua_efluentes/`.

## 8. Calidad

**MEDIA** como método (física explícita, separación potencia/energía y frío/electricidad, congelación/almacenamiento con dos bases temporales, tests de unidades y escalabilidad); **BAJA** como evidencia (indicadores energéticos `[PVDP]` de base incierta, COP y temperaturas supuestos, ningún balance frigorífico de proveedor ni dato argentino).
