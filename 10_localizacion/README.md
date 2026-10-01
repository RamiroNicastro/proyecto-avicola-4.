# 10 — Localización

**Alcance:** criterios de localización (distancia a granjas y mercado, disponibilidad de granos, agua, energía, efluentes, mano de obra, zonificación, incentivos provinciales/municipales) y evaluación de alternativas.

**Relacionado:** DEC-003, `11_agua_efluentes`, `12_energia_frio`, `13_logistica` (módulo paralelo 12B), `09_layout_obra_civil` (módulo paralelo 12C), `16_normativa_senasa`, `17_exportacion`, `23_plan_expansion`.

**Estado (2026-10-01, sesión 12A):** metodología y modelo multicriterio **completos y auditados (v1.1)**: 13 corredores en Buenos Aires, Entre Ríos, Santa Fe, Córdoba y Chaco; 45 subcriterios monotónicos en 14 grupos + 3 trade-offs no monotónicos; gates duros/condicionales; 4 perfiles de ponderación; 28 tests. **No hay ubicación seleccionada (DEC-003) ni ranking**: de 624 celdas, 0 verificadas, 35 `[PVDP]`, 589 pendientes; ninguna región elegible con umbrales de cobertura de 60, 75 ni 90 %. Síntesis en [`conclusiones_localizacion.md`](conclusiones_localizacion.md).

## Contenido

| Archivo | Contenido |
|---|---|
| [`conclusiones_localizacion.md`](conclusiones_localizacion.md) | Resultado del módulo: metodología, regiones, criterios, faltantes, sensibilidad, trade-offs, zonas a investigar, datos de campo, tests, archivos |
| [`metodologia_localizacion.md`](metodologia_localizacion.md) | Niveles país → terreno, embudo E0–E5, matriz, sentidos (monotónico / no monotónico / gate), envolvente por faltantes y cobertura de información, sensibilidad 60/75/90 %, arquitecturas de red, interfaces con 12B y 12C |
| [`criterios_localizacion.md`](criterios_localizacion.md) | Ecosistema avícola vs exposición sanitaria, subcriterios y trade-offs, gates duros y condicionales, correlaciones, rúbricas 1–5, bioseguridad, exportación por nodo, factor NETWORK no puntuable |
| [`regiones_preliminares.md`](regiones_preliminares.md) | 13 corredores, cuatro lógicas de Buenos Aires, fichas por provincia, eventos de GTA, contacto en Chaco |
| [`escenarios_localizacion.md`](escenarios_localizacion.md) | Distancia ≠ costo, arquetipos L1–L4, arquitecturas R1/R2, red de supermercados (sin ancla / parcial / fuerte) con parámetros t·km explícitos, exportación por nodo, escala, trade-offs |
| [`terreno_ideal.md`](terreno_ideal.md) | Qué debe tener un terreno (funciones, atributos, superficie pendiente, datos de campo) |
| [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md) | Ficha uniforme para relevar cada terreno candidato (2026-09-30) |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos: por qué no hay "mejor provincia", matriz multicriterio, pesos, zona vs terreno |
| [`matriz_localizacion.csv`](matriz_localizacion.csv) | Datos: una fila por región × subcriterio (valores vacíos o `[PVDP]`; no rellenar para calcular) |
| [`pesos_localizacion.csv`](pesos_localizacion.csv) | Perfiles A MERCADO, B PRODUCCIÓN, C EQUILIBRADO, D EXPORTADOR (ninguno es el correcto) |
| [`modelo_localizacion.py`](modelo_localizacion.py) | Modelo reproducible (fórmulas, supuestos y unidades en su docstring) |
| `resultados_localizacion.csv` | Salida generada por el modelo (no editar a mano) |
| [`actualizaciones_gestion_12A.md`](actualizaciones_gestion_12A.md) | Registros provisionales SUP-12A, DPV-12A, DEC-12A a consolidar en `00_gestion_proyecto` |
| [`fuentes_12A.csv`](fuentes_12A.csv) | Fuentes provisionales FTE-12A (identificadas, no consultadas) a consolidar en `25_fuentes` |

## Uso del modelo

```
python3 10_localizacion/modelo_localizacion.py                     # tests + resultados (estricto y exploratorio)
python3 10_localizacion/modelo_localizacion.py --solo-tests        # 28 pruebas
python3 10_localizacion/modelo_localizacion.py --umbrales-cobertura 0.6,0.75,0.9   # criterio de control
python3 10_localizacion/modelo_localizacion.py --demo --sensibilidad 0.5   # mecánica con datos FICTICIOS
python3 10_localizacion/modelo_localizacion.py --modo exploratorio --perfil C --detalle
python3 10_localizacion/modelo_localizacion.py --peso DEMANDA=20 --peso ECOSISTEMA_AVICOLA=8 --peso RRHH=0 ...
```

Columnas de la matriz: `REGION`, `PROVINCIA`, `CORREDOR`, `CRITERIO` (grupo), `SUBCRITERIO`, `NOMBRE_SUBCRITERIO`, `UNIDAD`, `SENTIDO` (`MAYOR_MEJOR`/`MENOR_MEJOR`/`NO_MONOTONICO`/`GATE_DURO`/`GATE_CONDICIONAL`), `NIVEL_DATO` (`CORREDOR`/`PROVINCIA_NORMA`/`PROVINCIA_AGREGADO`), `VALOR` (decimal con punto), `TIPO_EVIDENCIA` (`VERIFICADO`/`ESTIMACION`/`SUPUESTO`/`COTIZACION`/`PVDP`), `FUENTE` (FTE o SUP), `ESTADO` (`DISPONIBLE`/`PVDP`/`PENDIENTE`/`NO_APLICA`), `NORMALIZACION` (`minmax` o `rango_fijo:a:b`; `ninguna` para trade-offs, gates y NETWORK), `PESO` y `PUNTAJE` (vacíos: los pesos viven en `pesos_localizacion.csv` y los puntajes en `resultados_localizacion.csv`, que informa siempre la envolvente por faltantes —no es intervalo de confianza— junto con la `COBERTURA_DE_INFORMACION`), `OBSERVACIONES`.
