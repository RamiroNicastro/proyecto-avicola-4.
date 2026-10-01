# 09 — Layout y obra civil

**Alcance:** layouts conceptuales de planta y granjas, superficies por sector, separación de zonas limpia/sucia, flujos, obra civil e instalaciones, previsión de ampliaciones.

**Relacionado:** `05_proceso_industrial`, `10_localizacion`, `19_capex`.

**Estado (2026-10-01, sesión 12C):** modelo preliminar **completado** v1.0 para la **planta de faena** (las granjas no se trataron). Programa de áreas, zonificación, flujos, superficies en rango para 2.500–20.000 aves/día, terreno conceptual y estrategia de expansión. **Sin planos constructivos, sin CAPEX, sin terreno, escala, tecnología de efluentes, enfriamiento ni número de líneas elegidos.** Evidencia de campo pendiente (huellas de equipos, dotación, retiros y FOS, plantas reales).

## Contenido

| Archivo | Qué responde |
|---|---|
| [`conclusiones_layout.md`](conclusiones_layout.md) | **Síntesis**: áreas, zonas, flujos, superficies, terreno, expansión, puntos difíciles de modificar, datos faltantes, tests e interfaz futura del HTML |
| [`programa_areas.md`](programa_areas.md) | Las 54 áreas: zona, categoría, método de dimensionamiento, driver y dato faltante; huellas a pedir en el RFQ |
| [`zonificacion_layout.md`](zonificacion_layout.md) | Nueve zonas de layout (categorías de trabajo, no regulatorias), fronteras críticas y orden espacial |
| [`flujos_layout.md`](flujos_layout.md) | Nueve flujos por separado (vivo, producto, personal, subproductos, residuos, envases, mantenimiento, camiones, agua/efluentes) y matriz de cruces |
| [`layouts_por_escala.md`](layouts_por_escala.md) | m² por categoría y área (bajo/medio/alto), frío por perfil, efluentes por tecnología, sensibilidad, una vs dos líneas, esquemas de bloques |
| [`estrategia_expansion.md`](estrategia_expansion.md) | Trayectorias 2.500→20.000, 5.000→20.000, 10.000→20.000; qué sobredimensionar, preparar, modular o duplicar; puntos difíciles de modificar |
| [`requerimientos_obra_civil.md`](requerimientos_obra_civil.md) | Exigencias cualitativas por zona, requerimientos transversales y datos que faltan |
| [`guia_ramiro.md`](guia_ramiro.md) | Layout, flujo, zoning, buffer, footprint, expansión modular, m² de edificio vs de terreno, por qué una máquina nueva puede romper media planta |
| [`modelo_superficies.py`](modelo_superficies.py) | Modelo reproducible (ver abajo) |
| [`escenarios_superficies.csv`](escenarios_superficies.csv) | Salida del modelo: bloques `detalle` (área por área, 4 escalas × 4 tecnologías de efluentes), `sensibilidad` (totales, 22 variantes × 4 escalas) y `expansion` (3 trayectorias) |
| [`actualizaciones_gestion_12C.md`](actualizaciones_gestion_12C.md) | **Archivo histórico**: SUP/DPV/DEC provisionales y notas de la sesión 12C, ya integrados en `00_gestion_proyecto/` (mapa de IDs en [`../00_gestion_proyecto/reconciliacion_sesiones_12.md`](../00_gestion_proyecto/reconciliacion_sesiones_12.md)) |
| [`fuentes_12C.csv`](fuentes_12C.csv) | **Histórico, no activo** desde la reconciliación de las sesiones 12 (2026-10-01): las 10 fuentes están en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (FTE-290 a FTE-297; dos consolidadas en FTE-224 y FTE-218), todas `[PVDP]` |

## Modelo de superficies

```
python3 09_layout_obra_civil/modelo_superficies.py               # 22 tests + regenera el CSV
python3 09_layout_obra_civil/modelo_superficies.py --mutaciones  # 7/7 errores sembrados detectados
python3 09_layout_obra_civil/modelo_superficies.py --tablas      # tablas de los .md
python3 09_layout_obra_civil/modelo_superficies.py --escenario --aves-dia 7500 --config C --perfil P3 \
        --dias-congelado 28 --lineas 2 --efluentes lagunas --objetivo 20000 [--estricto]
```

- **Inputs:** escala, horas netas, configuración A/B/C (mix del balance v1.1), perfil P1–P3 y días de inventario, automatización, líneas, enfriamiento, tecnología de efluentes, escala objetivo, reserva de rendering, dotación, aves y t por camión, huellas de equipos por área, retiro, buffer, FOS, modo estricto.
- **Insumos importados (no recalculados):** `05_proceso_industrial/modelo_capacidad_proceso.py` (kg/ave por configuración, residencias de enfriamiento) y `11_agua_efluentes/modelo_utilities.py` (stock refrigerado y congelado, congelación t/día, caudales y cargas de efluente).
- **Outputs:** rango bajo/medio/alto por área; m² por categoría; m² construidos, operativos y de reserva; terreno conceptual; alertas; `salida_interfaz()` para el futuro HTML.
- **Unidades:** m², t, m³, h, ha; separador decimal del CSV: punto. Fórmulas y supuestos en el encabezado del script y en `programa_areas.md` §2.
- **Calidad de cada superficie:** tipo de origen A (modelo existente) · B (factor de diseño) · C (proxy) · D (footprint pendiente) · E (requisito regulatorio pendiente), en `programa_areas.md` §2 bis y en la columna `origen_superficie` del CSV. El terreno depende de retiro y buffer **variables** (supuesto/proxy hasta tener datos del sitio).
- **Uso:** las superficies sirven para comparar escalas y reservar órdenes de magnitud; no son anteproyecto ni superficie habilitable.
- **Factores no validados:** todos (SUP-107 a SUP-123). Los que sustituyen datos faltantes se marcan **PROXY** y generan alertas; una huella desconocida **nunca** se convierte en cero.
