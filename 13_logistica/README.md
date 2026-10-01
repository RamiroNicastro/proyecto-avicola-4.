# 13 — Logística

**Alcance:** transporte de pollitos BB, alimento, insumos y aves vivas; distribución refrigerada y congelada a clientes; exportación; retiro de subproductos; flota propia vs tercerizada; rutas, frecuencias y KPI. **Modelo físico**: qué se mueve, cuánto, desde dónde, hacia dónde, con qué frecuencia y bajo qué restricciones. **Sin costos** en esta fase.

**Relacionado:** `02_clientes_demanda`, `03_produccion_primaria` (captura y transporte de aves: [`transporte_aves.md`](../03_produccion_primaria/transporte_aves.md)), `04_balance_masa`, `07_subproductos`, `10_localizacion`, `12_energia_frio`, `17_exportacion` (puertos y documentos: [`logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md)), `23_plan_expansion`.

**Estado (2026-10-01, sesión 12B):** modelo preliminar **completado** v1.0 (20/20 tests). Evidencia de campo **pendiente**. No se eligió escala, radio, localización, modelo de distribución, transportista ni modalidad de flota.

## Contenido

| Archivo | Qué contiene |
|---|---|
| [`mapa_flujos_logisticos.md`](mapa_flujos_logisticos.md) | Mapa completo de flujos (insumos, vivo, producto, subproductos, residuos) con t/día por escala, frecuencia, restricción y dato faltante |
| [`logistica_aves_vivas.md`](logistica_aves_vivas.md) | Aves y t vivas, viajes, ocupación, radios (geográfico vs ruta), ventana de ayuno, DOA, merma, granjas abastecedoras, tamaño de lote vs ritmo de faena |
| [`logistica_producto_terminado.md`](logistica_producto_terminado.md) | Refrigerado vs congelado, despacho, pallets, ventanas, directo vs CD vs cross-dock, red ancla A/B/C, asignación por canal, inventario (días de producción vs calendario) |
| [`logistica_subproductos.md`](logistica_subproductos.md) | Corrientes y grupos G1–G4; retiro diario, cada 2 días, acumulación refrigerada, salida conjunta |
| [`logistica_exportacion.md`](logistica_exportacion.md) | Etapas planta → consolidación → puerto → reefer; contenedores por escala; plantilla de datos para cotizar |
| [`flota_propia_vs_tercerizada.md`](flota_propia_vs_tercerizada.md) | OWN / OUTSOURCE / HYBRID por flujo y criterios C1–C10 para decidir |
| [`kpis_logistica.md`](kpis_logistica.md) | KPI físicos (calculados) y económicos (definidos, no calculados) |
| [`conclusiones_logistica.md`](conclusiones_logistica.md) | Hallazgos, escenarios por escala, faltantes, tests, **riesgos**, interfaces con 12A y 12C |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación sin jerga: flete vs logística, camión vacío, densidad, backhaul, vivo vs refrigerado, red, CD |
| [`actualizaciones_gestion_12B.md`](actualizaciones_gestion_12B.md) | Propuestas para `00_gestion_proyecto/` y `25_fuentes/` (SUP/DPV/DEC/FTE provisionales `12B`) |
| [`fuentes_12B.csv`](fuentes_12B.csv) | Fuentes nuevas provisionales (FTE-12B-001 a 004, todas `[PVDP]`) |
| [`modelo_logistica.py`](modelo_logistica.py) | Modelo reproducible (fórmulas y supuestos documentados en el encabezado) |
| [`escenarios_logistica.csv`](escenarios_logistica.csv) | Salida del modelo (formato largo) |

## Modelo reproducible

```
python3 13_logistica/modelo_logistica.py                 # 20 tests + escribe escenarios_logistica.csv
python3 13_logistica/modelo_logistica.py --solo-tests
python3 13_logistica/modelo_logistica.py --resumen       # tablas de resumen por escala
python3 13_logistica/modelo_logistica.py --escenario --aves-dia 7500 --radio-km 120 --aves-camion 6000 \
    --cap-refrigerado 8 --dias-despacho 6 --perfil P2 --ancla B --kg-local-dia 100 --modo crossdock
```

- **Lee** las escalas aprobadas y los calendarios de [`../23_plan_expansion/modelo_escala.py`](../23_plan_expansion/modelo_escala.py) (que a su vez importa producción 03, balance 04 y subproductos 07) y los escenarios de demanda de `02`. No modifica ningún modelo previo.
- **Inputs:** aves/día, peso, DOA, distancias (radio, factor de ruta, planta–mercado, planta–puerto, receptor), capacidades de vehículos, estación, días/año, configuración y perfil de destino (mix), días de despacho, inventario, frecuencia de retiro, escenario ancla y kg/local/día.
- **Outputs:** toneladas, viajes, km, t·km, camión-horas, camión-día, flota mínima, frecuencia, ocupación, stock de ciclo y de seguridad, contenedores, flags de ayuno, jornada y conducción.
- **Datos faltantes:** toda capacidad o dato sin validar vale `None`; los resultados que dependen de él se escriben **`PENDIENTE`** (nunca 0). `NO_APLICA` = variable inexistente en el escenario (p. ej. ocupación sin viajes).

### Columnas de `escenarios_logistica.csv`

`bloque` (parametros, backhaul, aves_vivas_flujo, aves_vivas, aves_vivas_ruta, aves_vivas_doa, aves_vivas_merma, granjas, insumos_*, producto_terminado, producto_config, asignacion_canales, inventario_ciclo, inventario_seguridad, exportacion, exportacion_ruta, subproductos_corrientes, coproductos_frio, subproductos_retiro, red_ancla, kpi_resumen) · `escala_aves_dia` · `dias_semana` · `dias_anio` · `escenario` (estación, perfil, base temporal, escenario ancla, configuración o estrategia) · `parametros` (valores de barrido usados) · `variable` · `valor` (punto decimal; `PENDIENTE` / `NO_APLICA`) · `unidad` (% = ×100) · `periodo` (dia_operativo, dia_despacho, dia_calendario, semana, semana_plena, anio, mes, viaje, ruta, retiro, lote, cosecha, embarque, stock) · `base` (vivo, comercial, biologica+agua, alimento) · `cadena` (refrigerado, congelado, exportacion, subproducto) · `clasificacion` · `tipo_kpi` (todos físicos) · `sumable` · `fuente` · `nota`.

**Reglas de lectura:** no sumar filas de distintos `escenario`, `periodo` o `parametros`; los escenarios ancla A/B/C no son sumables; las filas de `stock` no son flujos; los coproductos de `coproductos_frio` ya están dentro del producto terminado.

## Preguntas clave pendientes

1. ¿La red de supermercados tiene CD que reciba perecederos? ¿Ventanas, pedido mínimo, pallets, fee? (DPV-036, DPV-12B-09)
2. ¿Cuántas aves por camión, con qué tiempos y a qué distancia real trabajan los contratistas de la zona? (DPV-054, DPV-12B-01)
3. ¿Qué receptor retira subproductos, con qué frecuencia y vehículo, y qué acepta juntos? (DPV-065, DPV-12B-03)
4. ¿Qué proporción refrigerado/congelado pide cada canal? (DPV-085)
