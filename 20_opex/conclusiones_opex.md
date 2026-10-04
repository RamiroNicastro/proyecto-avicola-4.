# Conclusiones — Motor OPEX + capital de trabajo v1.1 (sesión 17)

**Fecha:** 2026-10-02 (v1.1, con auditoría de completitud de arquitecturas y costo laboral) · Estado: **motor construido y probado; OPEX sin costear** · Registros propuestos: [`actualizaciones_gestion_17.md`](actualizaciones_gestion_17.md)

## 1. Qué se construyó

- **Motor reproducible** ([`modelo_opex.py`](modelo_opex.py)) que arma el **registro de costos operativos** de cualquier configuración entre 2.500 y 20.000 aves/día consumiendo los modelos aprobados (03, 04, 05, 09C, 12B, 14A, 14B y CAPEX 16) y lo cruza con una **base de costos externa** de 359 conceptos ([`base_costos_opex.csv`](base_costos_opex.csv)) y **reglas laborales** ([`reglas_laborales_opex.csv`](reglas_laborales_opex.csv)).
- **Arquitecturas** (de CAPEX, sin elegir): faena propia / façon; granjas integradas / propias / mixtas (filas separadas empresa vs productor); pollito comprado / incubación / reproductoras (futuro); alimento comprado / façon B1 / façon B2 / planta propia; flota propia / tercerizada por flujo; frío A/B/C; subproductos externo / básico / rendering (futuro); cuatro métodos de mantenimiento; halal opcional.
- **Matriz de completitud** ([`completitud_arquitecturas_opex.csv`](completitud_arquitecturas_opex.csv), 166 filas): bloques operativos materiales por módulo, coberturas estructural / física / de costeo y banderas `ARQUITECTURA_OPERATIVAMENTE_COMPLETA` y `ARQUITECTURA_COSTEABLE`.
- **29 escenarios**: 4.549 filas de registro, 457 de resumen, 2.349 drivers trazados, 1.422 de costo laboral, 615 de capital de trabajo, 20 ítems de validación.
- **78 tests** + **14 mutaciones** detectadas.

## 2. Resultado central

**No existe todavía un OPEX total, un costo por ave ni un capital de trabajo para ninguna configuración, y ninguna arquitectura es costeable.** De 359 conceptos de la base, **329 no tienen precio**; los **2** con precio son E4 `[PVDP]` (pollito BB de CAPIA y maíz pizarra Rosario). El "13 meses remunerados" de la v1.0 se retiró de los precios: el SAC es una regla laboral.

| Cobertura | C0 | C1 | C2 | C3 / CF |
|---|---|---|---|---|
| **Estructural** (sé qué costos existen) | 100 % | 100 % | 100 % | 100 % |
| Física (bloques con cantidades) | 57 % | 62 % | 56 % | 43 % |
| **De costeo por bloques** (sé cuánto cuestan) | 9,5 % | 7,7 % | 4,9 % | 0 % |
| De costeo por conceptos | 1,4–1,6 % | 0,8–0,9 % | 1,3–1,4 % | 0,5 % |
| Arquitectura costeable | No | No | No | No |

## 3. Qué números pueden usarse

| Utilizable (orden de magnitud, con su clasificación) | Dónde |
|---|---|
| Qué bloques operativos tiene cada módulo de cada arquitectura y cuáles faltan dimensionar o costear | [`completitud_arquitecturas_opex.csv`](completitud_arquitecturas_opex.csv) |
| Conceptos de costo por arquitectura, aportante (empresa / productor / tercero / pendiente), naturaleza, centro, tipo, universo | [`registro_costos_operativos.csv`](registro_costos_operativos.csv) |
| Cantidades anuales por escala (alimento, materias primas ilustrativas, pollitos, huevos, kWh y agua **de la planta de faena**, kg de producto, viajes y km, subproductos) | [`mapa_drivers_opex.csv`](mapa_drivers_opex.csv) |
| FTE **industriales** (14A) por puesto y modalidad; FTE conocidos de la empresa vs terceros incluidos en tarifas; universos de RRHH pendientes | [`modelo_costo_laboral.csv`](modelo_costo_laboral.csv), [`costos_rrhh.md`](costos_rrhh.md) |
| Inventarios físicos propios vs de terceros | [`capital_trabajo_opex.csv`](capital_trabajo_opex.csv) |
| Qué precios conseguir primero | [`matriz_validacion_opex.csv`](matriz_validacion_opex.csv) |

## 4. MONTOS_PARCIALES_E4_NO_COMPARABLES — no son resultado económico

| Escenarios | Único concepto con precio | Monto parcial (USD/año, 2.500 / 5.000 / 10.000 / 20.000) |
|---|---|---|
| C0, C1 (y C2 en dos filas propia/integrada) | Pollito comprado (E4, julio 2026, flete incluido desconocido) | 0,58 / 1,17 / 2,33 / 4,66 M |
| C3, CF | Maíz a precio Rosario sobre puerto (E4; no puesto en planta) | 0,36 / 0,72 / 1,44 / 2,88 M |

## 5. Qué números NO deben usarse para decidir

| Número | Por qué no |
|---|---|
| Los montos parciales del §4 | Un concepto E4 sobre 63–217; `COMPARABILIDAD = MONTOS_PARCIALES_E4_NO_COMPARABLES` |
| Diferencias entre configuraciones (C1 "más cara" que C3) | Reflejan qué concepto tiene precio, no el costo de cada opción |
| USD 0,93 por ave (pollito) y USD 0,58 por ave (maíz) | Costos de un concepto, no costo por ave |
| Maíz en inventario USD 15.445–123.561 | Único ítem valorizado, a precio Rosario: no es capital de trabajo |
| FTE_INDUSTRIAL_14A (51,5–168,0) como dotación de C3 | 14A no dimensiona granjas, incubación ni planta de alimento: FTE_ADICIONAL_PENDIENTE |
| FTE_INDUSTRIAL_14A de C0 (35,8–124,9) como personal propio | Incluye 25,8–89,4 FTE del faenador y choferes de terceros (en tarifas) |
| kWh, agua y energía térmica de 09C como consumo de la empresa integrada | Corresponden solo a la planta de faena |
| Cobertura estructural 100 % | Dice que los costos están identificados, no que estén cuantificados ni costeados |
| Cualquier EBITDA, margen, break-even o comparación contra USD 2 M | Ingresos no modelados; ninguna arquitectura costeable |

## 6. Diferencias estructurales (sin juicio económico)

1. **C0**: pocos costos propios (24,5 FTE de la empresa a 10.000 aves/día); el resto son tarifas de terceros (façon con el personal del faenador incluido, flete, alimento) y el pago al integrado.
2. **C1 → C3**: de 119 a 216 conceptos (10.000 aves/día); se agregan módulos completos (granjas propias, incubación, planta de alimento, tratamiento de subproductos) cuya estructura está representada pero cuyo RRHH, energía y agua están **PENDIENTES**.
3. **Granjas integradas**: costo de la empresa (pollito, alimento, sanidad, coordinación, pago al integrado) separado del costo del productor (energía, agua, mano de obra: informativos); gas, cama, captura, mortalidad, limpieza y bioseguridad con aportante PENDIENTE.
4. **Capital de trabajo**: con integración, la empresa es dueña del alimento en silos de granja y de las aves en crianza; con façon B1, de los granos en el elaborador; con compra o façon B2, no del stock del proveedor.

## 7. Principales datos por validar

DPV-050 / DPV-050 (alimento), DPV-157 (granos puestos en planta y diferencial), DPV-047 (pollito y huevo), DPV-148 y DPV-148 (salarios, cargas y normativa laboral: SAC, vacaciones, horas extra), DPV-176 (dotaciones upstream), DPV-177 (consumos upstream), DPV-052 (tarifas), DPV-006 / DPV-006 (façon), DPV-170 (integración), DPV-175 (plazos) y DPV-019 (Índice de costo de producción de SAGyP).

## 8. Principales decisiones abiertas

DEC-080 (estructura del motor, incluida la regla de completitud), DEC-024, DEC-086, DEC-087, DEC-088, DEC-089, DEC-090, DEC-084. Existentes que el motor parametriza: DEC-001, 002, 003, 004, 006, 020, 023, 024, 027, 043, 045, 056, 064, 067, 068, 069, 074, 079.

## 9. Próximo paso

1. Precios de mayor impacto con lectura primaria (alimento, pollito, maíz y soja en zona, convenio laboral, tarifa eléctrica de un corredor) e Índice de costo de producción de SAGyP.
2. Modelos físicos faltantes para los módulos upstream: dotación y consumos de granjas propias, incubadora y planta de alimento (sin ellos, C3 y CF no pueden ser operativamente completas).
3. El modelo financiero (`21`) usará el registro, los repartos fijo/variable, la completitud y el capital de trabajo.
