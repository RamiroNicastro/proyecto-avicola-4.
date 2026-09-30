# Conclusiones — energía, frío, congelado y respaldo

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Base: [`demanda_energia.md`](demanda_energia.md), [`sistema_frio.md`](sistema_frio.md), [`congelado_almacenamiento.md`](congelado_almacenamiento.md), [`respaldo_energia.md`](respaldo_energia.md); modelo [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) v1.1 y CSV [`../11_agua_efluentes/escenarios_utilities.csv`](../11_agua_efluentes/escenarios_utilities.csv)

> **Modelo top-down de sensibilidad.** Ninguna cifra es especificación de diseño. **No** se eligen fuente térmica, refrigerante, sistema de frío, generador ni proveedores; **no** se calculan CAPEX, OPEX ni m² de cámara; **no** se elige sitio. Toda cifra externa es `[PVDP]`; ninguna es argentina medida.
> Tabla física por escala, auditoría v1.1, integración con 09A, incertidumbres, qué medir/cotizar, tests y calidad: [`../11_agua_efluentes/conclusiones_agua_efluentes.md`](../11_agua_efluentes/conclusiones_agua_efluentes.md) (no se duplican aquí).

---

## 1. Energía eléctrica: energía → potencia media; pico PENDIENTE

- **Energía diaria** (sensibilidad): ~0,8 kWh/ave (0,5–1,5) → **2.046 / 4.092 / 8.184 / 16.368 kWh por día operativo** (medio).
- **Potencia media equivalente** (no pico): proceso **bajo 14 h** 129 / 259 / 518 / 1.036 kW; total **bajo 24 h** 85 / 171 / 341 / 682 kW (medio).
- **Potencia pico, potencia contratada, transformador y grupo electrógeno: PENDIENTES.** Surgirán de una lista de cargas (equipo, kW nominal, factor de carga, simultaneidad, arranque, cos φ, demanda máxima). kWh/ave no los determina.

## 2. Energía térmica: MJ/día ≠ kW pico

- ~1 MJ útil/ave (sensibilidad) → 3,3 / 6,7 / 13,3 / 26,7 GJ/día de combustible (medio); ~86 / 171 / 343 / 686 m³/día de gas natural **equivalente**.
- Potencia térmica **media** equivalente (10.000 aves/día, medio): escaldado bajo 8 h ~140 kW; limpieza bajo 4 h ~323 kW; sanitización bajo 12 h ~31 kW. La limpieza **podría** concentrar demanda; debe compararse con el escaldado mediante un **perfil horario**. **Pico térmico y caldera: PENDIENTES.**

## 3. Frío: carga sensible del producto ≠ carga frigorífica total

- **Carga sensible preliminar asociada al enfriamiento del producto:** 25 / 50 / 99 / 198 kWf (7 / 14 / 28 / 56 TR) en 8 h. **No es la capacidad frigorífica de planta.**
- Filas separadas: agua de reposición del chiller (69 kWf medio a 10.000 aves/día), cargas adicionales ilustrativas (67 kWf), congelación del producto (10 / 39 / 49 kWf con P1 / P2 / P3).
- **Carga frigorífica total: PENDIENTE** (balance frigorífico: producto, latente, transmisión, infiltración, puertas, personas, iluminación, motores, docks, salas, cámaras, túneles, desescarche).
- **kW eléctricos aproximados = kWf ÷ COP supuesto** (3 enfriado; 1,4 congelado, medio), con el COP declarado en cada fila; no es consumo garantizado.
- **Brecha no cerrada:** cálculo físico ~450 kWh/día vs ~2.540 kWh/día del reparto top-down (×5,7). Se resolverá con balance de proveedor y suma bottom-up.
- **Refrigerantes:** amoníaco, CO₂, cascada, indirectos, HFC (Kigali) y HFO comparados sin elegir.

## 4. Congelado y almacenamiento

- **Capacidad de congelación** = t **nuevas** que atraviesan la congelación por día: P1 0,6 / 1,2 / 2,4 / 4,8; P2 2,4 / 4,8 / 9,6 / 19,2; P3 3,0 / 6,0 / 12,0 / 24,0 t/día.
- **Capacidad de almacenamiento** = t **ya congeladas** guardadas: P3 a 20.000 aves/día y 14 días, 336 t (días de producción) o 230 t (días calendario).
- Una cámara de 300 t **no** congela 300 t/día. El **perfil** pesa más que la escala (×5 entre P1 y P3).

## 5. Respaldo

- **Carga crítica ilustrativa de escenario** (proxy): 20 / 40 / 79 / 158 kW (P1, medio). **No es el generador.**
- **Grupo electrógeno: PENDIENTE** (lista de cargas críticas, kVA, cos φ, arranque, secuencia, simultaneidad, autonomía, combustible, redundancia, frío sin faena, black-start).

## 6. Qué debe ser verdad en un sitio (preguntas, no especificaciones)

| Pregunta al sitio | Por qué | Referencia de sensibilidad (10.000 aves/día, medio) |
|---|---|---|
| ¿Cuánta potencia eléctrica hay disponible y ampliable? | La demanda máxima real saldrá de la lista de cargas; la media ya es ~0,5 MW de proceso | Media equivalente 518 kW bajo 14 h |
| ¿Hay gas natural? ¿Con qué caudal horario? | La caldera se dimensiona por perfil horario, no por m³/día | 343 m³/día equivalentes |
| ¿Qué temperatura de verano de diseño? | Define COP y capacidad de condensación | — |
| ¿Qué calidad de red (cortes)? | Define la política de respaldo | — |

## 7. Archivos de esta carpeta

`demanda_energia.md`, `sistema_frio.md`, `congelado_almacenamiento.md`, `respaldo_energia.md`, `conclusiones_energia_frio.md`, `README.md` (v1.1). Modelo, CSV, fuentes y propuestas de gestión en `../11_agua_efluentes/`.

## 8. Calidad

**MEDIA** como método (separación energía/potencia media/pico, MJ/kW térmicos, carga del producto/carga total, kWf/kWe con COP declarado, congelación/almacenamiento, pendientes explícitos y tests); **BAJA** como evidencia (indicadores `[PVDP]` de base incierta, COP y temperaturas supuestos, sin lista de cargas, sin balance frigorífico de proveedor ni datos argentinos).
