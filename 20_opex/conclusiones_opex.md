# Conclusiones — Motor OPEX + capital de trabajo v1.0 (sesión 17)

**Fecha:** 2026-10-02 · Estado: **motor construido y probado; OPEX sin costear** · Registros propuestos: [`actualizaciones_gestion_17.md`](actualizaciones_gestion_17.md)

## 1. Qué se construyó

- **Motor reproducible** ([`modelo_opex.py`](modelo_opex.py)) que arma el **registro de costos operativos** de cualquier configuración entre 2.500 y 20.000 aves/día consumiendo los modelos aprobados (03, 04, 05, 09C, 12B, 14A, 14B y el CAPEX de 16) y lo cruza con una **base de costos externa** de 323 conceptos ([`base_costos_opex.csv`](base_costos_opex.csv)).
- **Arquitecturas** (de CAPEX, sin elegir): faena propia / façon; granjas integradas / propias / mixtas con aportes empresa vs integrado; pollito comprado / incubación / reproductoras (futuro); alimento comprado / façon con MP de la empresa / façon con MP del elaborador / planta propia; flota propia / tercerizada por flujo con modelo de tarifa; frío A/B/C; subproductos externo / básico / rendering (futuro); mantenimiento por cuatro métodos alternativos; halal como módulo opcional.
- **29 escenarios** (C0–C3 y CF × 2.500 / 5.000 / 10.000 / 20.000 + 9 variantes a 10.000): 4.401 filas de registro, 457 filas de resumen, 2.175 drivers trazados, 1.238 filas de costo laboral, 615 filas de capital de trabajo, 20 ítems de validación.
- **62 tests** + **11 mutaciones** detectadas.

## 2. Resultado central

**No existe todavía un OPEX total ni un costo por ave para ninguna configuración, y el capital de trabajo es PENDIENTE en todas.** De 323 conceptos de la base, **301 no tienen precio**; los 3 con precio son **E4 `[PVDP]`** (pollito BB de CAPIA, maíz pizarra Rosario, 13 meses remunerados). Cobertura por conceptos: **1,5–2,7 % (C0), 0,8–0,9 % (C1), 0,7 % (C2), 0,5 % (C3/CF)**. Cobertura por valor: **no calculable**. El motor responde "NO DISPONIBLE" en lugar de un total engañoso.

## 3. Qué números pueden usarse

| Utilizable (orden de magnitud, con su clasificación) | Dónde |
|---|---|
| Qué conceptos de costo tiene cada arquitectura, quién los aporta (empresa / integrado / pendiente), su naturaleza (variable / fijo / semifijo / semivariable), centro de costo y tipo | [`registro_costos_operativos.csv`](registro_costos_operativos.csv), [`estructura_opex.md`](estructura_opex.md) |
| Cantidades anuales por escala: alimento (3.091–24.724 t), materias primas ilustrativas, pollitos (0,66–5,28 M), huevos (0,82–6,54 M), kWh (0,52–4,13 M en C1), agua (15.625–125.000 m³), efluente, energía térmica, kg de producto (1.498–11.982 t), viajes y km por flujo, subproductos y decomisos | [`mapa_drivers_opex.csv`](mapa_drivers_opex.csv), documentos `costos_*.md` |
| Dotación en FTE y horas por puesto y modalidad (14A) y la estructura del costo empresa por FTE | [`modelo_costo_laboral.csv`](modelo_costo_laboral.csv), [`costos_rrhh.md`](costos_rrhh.md) |
| Inventarios físicos **propios** vs de terceros por arquitectura (alimento, granos, huevos, aves en crianza, producto) | [`capital_trabajo_opex.csv`](capital_trabajo_opex.csv), [`capital_trabajo.md`](capital_trabajo.md) |
| Dónde hay riesgo de doble conteo y cómo se evita | [`metodologia_opex.md`](metodologia_opex.md) §4 |
| Qué precios y parámetros conseguir primero | [`matriz_validacion_opex.csv`](matriz_validacion_opex.csv) |

## 4. Qué números NO deben usarse para decidir

| Número | Por qué no |
|---|---|
| Monto con precio de C0–C2 (USD 0,58 / 1,17 / 2,33 / 4,66 M/año) | Es **solo el pollito comprado** (E4, julio 2026, sin saber si incluye flete): 1 de 61–147 conceptos |
| Monto con precio de C3/CF (USD 0,36 / 0,72 / 1,44 / 2,88 M/año) | Es **solo el maíz** (E4, precio sobre puerto): 1 de 199–210 conceptos |
| Diferencia de montos entre configuraciones (C1 "cuesta más" que C3) | Refleja **qué concepto tiene precio**, no cuánto cuesta cada opción: C1 tiene el pollito y C3 el maíz |
| USD 0,93 por ave (pollito) y USD 0,58 por ave (maíz) | Costos **de un concepto**, no costo por ave |
| Maíz en inventario USD 15.445–123.561 | Único ítem de inventario valorizado (E4): no es capital de trabajo |
| FTE de C3 iguales a C1 | 14A no dimensiona granjas, incubadora ni planta de alimento: esas funciones son SIN_CANTIDAD |
| Cualquier EBITDA, margen o break-even | Ingresos no modelados y OPEX con < 3 % de cobertura (§8 de la guía) |
| Cualquier comparación contra USD 2 M | El capital no es límite (regla 7); OPEX y CT no están completos |

## 5. Diferencias estructurales (sin juicio económico)

1. **C0 (asset-light)** tiene pocos conceptos propios (67 a 10.000 aves/día): su costo se concentra en **tarifas de terceros** (façon, flete, alimento) y en el pago al integrado; el personal del faenador está dentro de la tarifa de façon (las horas de 14A siguen visibles).
2. **C1 → C3** pasa de 118 a 209 conceptos (10.000 aves/día): aparecen materias primas, incubadora, granjas propias, flota propia en ocho flujos, mantenimiento de más áreas y funciones de personal que 14A no dimensiona.
3. **Granjas integradas**: la energía, el agua y la mano de obra de la granja son del integrado (informativos); cama, gas, captura, mortalidad, limpieza y bioseguridad quedan con **aportante PENDIENTE** hasta tener contrato.
4. **Capital de trabajo**: con integración, la empresa es dueña del alimento en los silos de granja y de las aves en crianza (~331.000 a 10.000 aves/día); con façon B1, también de los granos en el elaborador; con compra o façon B2, no del stock del proveedor.
5. **Variable vs fijo**: los costos de mayor volumen (alimento, pollito, empaque, energía) son variables por definición; personal y estructura son fijos o semifijos. Ningún semivariable tiene todavía reparto declarado: el ramp-up y el break-even quedan PENDIENTES.

## 6. Principales datos por validar

DPV-050 / DPV-17-01 (alimento), DPV-17-02 (granos y MP puestos en planta), DPV-17-03 (pollito y huevo), DPV-148 (salarios y cargas), DPV-17-05 (tarifa eléctrica, gas, agua), DPV-006 / DPV-17-07 (façon), DPV-17-04 (contrato de integración), DPV-17-14 (plazos y días de stock) y DPV-17-17 (lectura primaria del Índice de costo de producción de pollos parrilleros de SAGyP, FTE-16-002).

## 7. Principales decisiones abiertas

DEC-17-01 (adoptar la estructura del motor), DEC-17-02 (variante del façon de alimento), DEC-17-04 (base de pago al integrado), DEC-17-05 (modelo de tarifa de flete), DEC-17-06 (método de mantenimiento), DEC-17-07 (valuación de inventarios), DEC-17-08 (curva de ramp-up), DEC-17-10 (umbral de cobertura). Existentes que el motor solo parametriza: DEC-001, DEC-002, DEC-003, DEC-004, DEC-006, DEC-020, DEC-023, DEC-024, DEC-027, DEC-043, DEC-045, DEC-056, DEC-064, DEC-067, DEC-068, DEC-074, DEC-079.

## 8. Próximo paso

1. Conseguir los precios de mayor impacto con lectura primaria (alimento, pollito, maíz y soja en zona, salario de convenio, tarifa eléctrica de un corredor candidato) y leer el Índice de costo de producción de SAGyP: con 6–8 precios E2/E3 la cobertura por valor empieza a ser calculable.
2. Definir los parámetros que hoy bloquean cantidades (consumo L/km, kWh de granja e incubadora, lodos, plan de muestreo, dotaciones upstream).
3. El modelo financiero (`21`) usará este registro, los repartos fijo/variable y el capital de trabajo; ingresos, EBITDA y VAN se calculan allí.
