# 11 — Agua y efluentes

**Alcance:** requerimiento y calidad de agua (granjas, faena), fuentes de abastecimiento, tratamiento de efluentes líquidos, residuos sólidos, permisos ambientales.

**Relacionado:** `07_subproductos`, `10_localizacion`, `16_normativa_senasa`, `12_energia_frio` (energía, frío, congelado y respaldo del mismo modelo de utilities).

## Contenido (versión 1.0, 2026-09-30 — sesión 09C)

| Archivo | Contenido |
|---|---|
| [`balance_agua.md`](balance_agua.md) | Agua utilizada vs descargada vs retenida; L/ave por etapa (bajo/medio/alto); m³/día por escala; calidad del agua (conceptual) |
| [`caracterizacion_efluentes.md`](caracterizacion_efluentes.md) | Corrientes del efluente; rangos de DBO, DQO, SST, grasas, NTK, PT; carga por escala; valor de recuperar sangre y sólidos |
| [`alternativas_tratamiento.md`](alternativas_tratamiento.md) | Pretratamiento (rejas, grasas, ecualización, DAF), biológico (anaerobio, aerobio, lagunas, reactores, combinaciones) y lodos — sin elegir |
| [`guia_ramiro.md`](guia_ramiro.md) | L/ave, m³/día, DBO/DQO, efluente, DAF, carga orgánica, kW vs kWh, TR, congelación vs almacenamiento, por qué los servicios limitan la capacidad |
| [`conclusiones_agua_efluentes.md`](conclusiones_agua_efluentes.md) | Síntesis, **tabla física de utilities por escala**, incertidumbres, **qué medir/cotizar**, tests, archivos, calidad |
| [`modelo_utilities.py`](modelo_utilities.py) | Modelo reproducible de utilities (Python 3, sin dependencias externas) |
| [`escenarios_utilities.csv`](escenarios_utilities.csv) | Salida del modelo (4.072 filas) |
| [`fuentes_09C.csv`](fuentes_09C.csv) | 19 fuentes nuevas (`FTE-09C-xx`, todas `[PVDP]`) pendientes de integrar a `25_fuentes/` |
| [`actualizaciones_gestion_09C.md`](actualizaciones_gestion_09C.md) | Propuestas para `00_gestion_proyecto/` y `25_fuentes/` (sesión en paralelo: no se editaron) |

## Documentación del modelo (regla 15)

- **Qué hace:** para cualquier escala (aves faenadas por día operativo) y nivel bajo/medio/alto calcula agua (por etapa, total, descargada, caudal horario), agua retenida (del balance), carga del efluente (DQO, DBO₅, SST, GyA, NTK, PT) y concentraciones, masa que evita el efluente, lodos, electricidad (kWh y kW), calor (MJ, kW térmicos, equivalentes de combustible), frío (kWf, TR, kWe), congelado (t/día), inventario (t, dos bases temporales) y respaldo (kW, kVA).
- **Entradas de masa:** lee `23_plan_expansion/escenarios_escala.csv` (fuente de verdad; modelo de escala v1.1 ← balance v1.1 ← subproductos v1.0). **No modifica** ningún modelo previo ni su CSV.
- **Parámetros:** sección 1 del script, cada uno con valores bajo/medio/alto, origen (FUENTE `[PVDP]` / ESTIMACIÓN / SUPUESTO) y referencia; resumen en `actualizaciones_gestion_09C.md` §1 (SUP-09C-01 a 09).
- **Fórmulas y unidades:** docstring del script (L, m³, kg, t, kWh, kW, kJ, MJ, TR, mg/L, h; decimal con punto en el CSV).
- **Parámetros modificables** (`--escenario`): `--aves-dia`, `--dias-anio`, `--nivel`, `--l-ave` (reparte por etapa en proporción), `--frac-efluente`, `--dqo-g-ave` (DBO, SST, GyA, NTK, PT en proporción), `--frac-sangre`, `--perfil refrigerado,congelado,exportacion`, `--dias-refrigerado`, `--dias-congelado`, `--base-inventario`, `--horas-netas`.
- **Uso:** `python3 11_agua_efluentes/modelo_utilities.py` (tests + CSV) · `--solo-tests` · `--tablas` · `--mutaciones` · `--escenario ...`. Se detiene con código 1 si falla un test.
- **Columnas del CSV:** `bloque, escala_aves_dia, dias_semana, dias_anio, nivel, parametro, variable, valor, unidad, periodo, base, origen, clasificacion, referencia, nota`. Bloques: `entrada`, `agua`, `agua_retenida`, `efluente`, `masa_evitable`, `lodos`, `electricidad`, `inventario`, `congelado`, `frio`, `termico`, `respaldo`, `perfil_frio` (P2/P3), `parametros`.
- **Tests:** U00–U19 (unidades, escalabilidad, separación de aguas, cierre, inventario = modelo de escala, congelación vs almacenamiento, kW frigorífico vs eléctrico, potencia vs energía, no negativos, sin economía, entradas inválidas, sangre); mutaciones M01–M09.
- **Limitaciones:** lineal (sin economías de escala); todas las fuentes externas `[PVDP]`; ningún dato argentino; no incluye rendering propio, cocción ni granjas.
