# 11 — Agua y efluentes

**Alcance:** requerimiento y calidad de agua (granjas, faena), fuentes de abastecimiento, tratamiento de efluentes líquidos, residuos sólidos, permisos ambientales.

**Relacionado:** `07_subproductos`, `10_localizacion`, `16_normativa_senasa`, `12_energia_frio` (energía, frío, congelado y respaldo del mismo modelo de utilities).

## Contenido (versión 1.1, 2026-09-30 — sesión 09C con auditoría conceptual)

> Modelo **top-down de sensibilidad**: los rangos bajo/medio/alto no son consumos esperados ni especificaciones. Potencia pico, pico térmico, carga frigorífica total, lodos y grupo electrógeno quedan **PENDIENTES** (valor vacío en el CSV) hasta tener lista de cargas, perfil horario, balance frigorífico y caracterización medida.

| Archivo | Contenido |
|---|---|
| [`balance_agua.md`](balance_agua.md) | Cinco aguas (captada, utilizada, incorporada, evaporada/arrastrada, descargada); L/ave y m³/t como rango de sensibilidad; m³/día por escala; calidad del agua (conceptual) |
| [`caracterizacion_efluentes.md`](caracterizacion_efluentes.md) | Corrientes; rangos citados; carga por **método A (g/ave) y método B (m³ × mg/L)** con alerta de divergencia; límite ADA 336/03 solo como ejemplo; masa segregable en origen ≠ SST; sangre |
| [`alternativas_tratamiento.md`](alternativas_tratamiento.md) | Pretratamiento (rejas, grasas, ecualización, DAF), biológico (anaerobio, aerobio, lagunas, reactores, combinaciones) — sin elegir; lodos PENDIENTES con cadena explícita y escenario ilustrativo |
| [`guia_ramiro.md`](guia_ramiro.md) | L/ave, m³/día, DBO/DQO, efluente, DAF, carga orgánica, kW vs kWh, TR, congelación vs almacenamiento, por qué los servicios limitan la capacidad |
| [`conclusiones_agua_efluentes.md`](conclusiones_agua_efluentes.md) | Auditoría v1.1, síntesis, **tabla física por escala**, incertidumbres, **integración top-down/bottom-up con 09A**, **qué medir/cotizar**, tests, archivos, calidad |
| [`modelo_utilities.py`](modelo_utilities.py) | Modelo reproducible de utilities (Python 3, sin dependencias externas) |
| [`escenarios_utilities.csv`](escenarios_utilities.csv) | Salida del modelo (4.995 filas) |
| [`fuentes_09C.csv`](fuentes_09C.csv) | 19 fuentes nuevas (`FTE-09C-xx`, todas `[PVDP]`) pendientes de integrar a `25_fuentes/` |
| [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md) | Propuestas para `00_gestion_proyecto/` y `25_fuentes/` (sesión en paralelo: no se editaron) |

## Documentación del modelo (regla 15)

- **Qué hace:** para cualquier escala y nivel bajo/medio/alto calcula cinco aguas y m³/t; carga del efluente por método A y método B con relación B/A y alertas; remoción bajo límites de **ejemplo** (con jurisdicción y tipo de descarga); masa segregable en origen; lodos (PENDIENTE o ilustrativo con cadena explícita); energía diaria y potencia **media** equivalente (pico solo desde `demanda_maxima(lista_de_cargas)`); calor en MJ/día y potencia térmica media (pico PENDIENTE); carga sensible del producto, agua de chiller, adicionales y congelación en kWf con kWe = kWf ÷ COP declarado (carga total PENDIENTE); capacidad de congelación (t/día) y de almacenamiento (t); carga crítica ilustrativa (generador PENDIENTE); contraste top-down/bottom-up (`contraste_bottom_up`).
- **Entradas de masa:** lee `23_plan_expansion/escenarios_escala.csv` (fuente de verdad; modelo de escala v1.1 ← balance v1.1 ← subproductos v1.0). **No modifica** ningún modelo previo ni su CSV.
- **Parámetros:** sección 1 del script, cada uno con valores bajo/medio/alto, origen (FUENTE `[PVDP]` / ESTIMACIÓN / SUPUESTO) y referencia; resumen en `actualizaciones_gestion_09C.md` §1 (SUP-09C-01 a 09).
- **Fórmulas y unidades:** docstring del script (L, m³, kg, t, kWh, kW, kJ, MJ, TR, mg/L, h; decimal con punto en el CSV).
- **Parámetros modificables** (`--escenario`): `--aves-dia`, `--dias-anio`, `--nivel`, `--l-ave` (reparte por etapa en proporción), `--frac-efluente` (SUPUESTO editable), `--dqo-g-ave` (método A), `--dqo-mg-l` (método B), `--frac-sangre`, `--lodos-ilustrativo`, `--perfil refrigerado,congelado,exportacion`, `--dias-refrigerado`, `--dias-congelado`, `--base-inventario`, `--horas-netas`.
- **Uso:** `python3 11_agua_efluentes/modelo_utilities.py` (tests + CSV) · `--solo-tests` · `--tablas` · `--mutaciones` · `--escenario ...`. Se detiene con código 1 si falla un test.
- **Columnas del CSV:** `bloque, escala_aves_dia, dias_semana, dias_anio, nivel, parametro, variable, valor, unidad, periodo, base, origen, clasificacion, referencia, nota`. Bloques: `entrada`, `agua`, `agua_incorporada`, `efluente`, `masa_segregable`, `lodos`, `lodos_ilustrativo`, `electricidad`, `inventario`, `congelado`, `frio`, `termico`, `respaldo`, `perfil_frio` (P2/P3), `alertas`, `parametros` (incluye límites de ejemplo con jurisdicción y tipo de descarga). `origen` = FUENTE / ESTIMACIÓN / SUPUESTO / PENDIENTE (valor vacío).
- **Tests:** U00–U29 (unidades, escalabilidad, cinco aguas y cierre, inventario = modelo de escala, congelación vs almacenamiento, COP declarado, kWh ≠ pico, horas de la potencia media, subproductos ≠ SST, lodos pendientes, carga del producto ≠ capacidad frigorífica, generador pendiente, límites con jurisdicción, métodos A/B independientes, m³/t, contraste bottom-up); mutaciones M01–M20.
- **Limitaciones:** lineal (sin economías de escala); todas las fuentes externas `[PVDP]`; ningún dato argentino; no incluye rendering propio, cocción ni granjas.
