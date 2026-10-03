# Estructura del OPEX — módulos, clasificación y columnas

**Fecha:** 2026-10-02 · Fuente de verdad de los conceptos: [`base_costos_opex.csv`](base_costos_opex.csv) (359 filas, v1.1). Reglas laborales: [`reglas_laborales_opex.csv`](reglas_laborales_opex.csv). Método: [`metodologia_opex.md`](metodologia_opex.md).

## 1. Módulos

| Módulo | Contenido | Activo si… | Detalle |
|---|---|---|---|
| ALIMENTO | Compra (alimento terminado, descarga), façon (servicio, precio integral, almacenamiento), materias primas (maíz, soja, aceite, núcleo, otros o "resto"), mermas, planta propia (energía, vapor, análisis, almacenamiento) | Siempre (según arquitectura) | [`costos_alimento.md`](costos_alimento.md) |
| POLLITOS / INCUBACION / REPRODUCTORAS | Pollito comprado; huevo fértil, vacunas, insumos, limpieza por carga, descartes, energía y agua de incubadora; reproductoras **FUTURO** | Pollito = compra / incubación | [`costos_incubacion.md`](costos_incubacion.md) |
| PRODUCCION_PRIMARIA | Sanidad, cama, gas, captura, mortalidad, limpieza de galpones, bioseguridad, energía y agua de granja, pago al integrado, asistencia externa | Siempre; reparto empresa / integrado | [`costos_produccion_primaria.md`](costos_produccion_primaria.md) |
| FAENA | Façon (tarifa, frío, subproductos) o planta propia (químicos, elementos, cuchillería, servicios) | Siempre | [`costos_faena.md`](costos_faena.md) |
| EMPAQUE | Bolsas, bandejas, film, cajas, etiquetas, separadores, pallets, flejes, otros (por kg de producto) | Siempre (aportante PENDIENTE en façon) | [`costos_faena.md`](costos_faena.md) §3 |
| UTILITIES / EFLUENTES | Electricidad (kWh, potencia, cargo fijo), térmico (por combustible), agua (red / pozo / tratamiento), congelado en tercero; químicos, análisis, lodos y canon de efluentes | Faena propia (congelado en tercero también en frío C) | [`costos_utilities.md`](costos_utilities.md) |
| SUBPRODUCTOS | Retiro de sangre, plumas, vísceras, cabezas y decomisos; contenedores; tratamiento básico; rendering **FUTURO** | Faena propia | [`costos_faena.md`](costos_faena.md) §4 |
| LOGISTICA | Por flujo (pollitos, huevos, alimento, grano, vivo, refrigerado, congelado, subproductos): flota propia **o** flete tercerizado | Flujos activos de la arquitectura | [`costos_logistica.md`](costos_logistica.md) |
| MANTENIMIENTO | Por área (proceso, frío, eléctrico/automatización, utilities/efluentes, edificios, incubadora, planta de alimento, granjas) y tipo (preventivo, correctivo, repuestos, lubricantes, servicios técnicos, contratos) | Áreas con activos propios | [`costos_mantenimiento.md`](costos_mantenimiento.md) |
| CALIDAD / HALAL | Análisis, laboratorio, certificaciones, auditorías, documentación, trazabilidad, tasas SENASA; halal = **módulo opcional de mercado** | Siempre / opcional | [`costos_calidad.md`](costos_calidad.md) |
| ADMINISTRACION / COMERCIAL | Contabilidad, legales, sistemas, comunicaciones, seguridad, limpieza administrativa, HyS externo, otros; marketing, viajes | Siempre | §4 |
| SEGUROS | Planta, incendio, RC, mercadería, interrupción, granjas, flota por flujo | Según activos | §5 |
| COSTO_LABORAL | Puestos de 14A (FTE interno y horas contratadas) + funciones que 14A no dimensiona | Siempre | [`costos_rrhh.md`](costos_rrhh.md) |

## 2. Clasificación obligatoria de cada costo

| Campo | Valores | Uso posterior |
|---|---|---|
| `NATURALEZA` | variable · fijo · semifijo · semivariable | Break-even, ramp-up |
| `PCT_VARIABLE` / `PCT_FIJO` | 100/0 por **definición** si el driver es volumen (variable) o período (fijo; semifijo dentro del escalón de capacidad). Semivariable: vacío = PENDIENTE; si se carga, debe declararse SUPUESTO (validación) | Break-even |
| `CENTRO_COSTO` | producción primaria · incubación · alimento · faena · frío · mantenimiento · calidad · logística · administración · comercial · servicios generales · terceros | Costeo por eslabón |
| `TIPO` | interno · tercerizado · comprado · propio | Make-or-buy posterior |
| `APORTANTE` | EMPRESA · PRODUCTOR_INTEGRADO (informativo) · TERCERO (informativo) · PENDIENTE (cuenta como faltante) | Separar costo de la empresa del de terceros |
| `FASE` | OPERACION · FUTURO (no cuenta) · OPCIONAL_MERCADO (cuenta solo si se activa el módulo) | — |
| `GRUPO_PROVEEDOR` | alimento · pollitos · granos · servicios · packaging · logística · energía · personal | Cuentas por pagar por proveedor |

Costo laboral por driver de 14A (SUP-179): `produccion`, `activos` y `estrategia` → semifijo (se mueven por escalones de cuadrillas y turnos); `casi_fijo` → fijo; horas tercerizadas → variable.

## 3. Columnas

**Base de costos** ([`base_costos_opex.csv`](base_costos_opex.csv)): `ID_COSTO`, `MODULO`, `SUBMODULO`, `CONCEPTO`, `UNIDAD`, `PRECIO_UNITARIO`, `PRECIO_BAJO`, `PRECIO_ALTO`, `ORIGEN_RANGO`, `MONEDA_ORIGINAL`, `TC_MONEDA_POR_USD`, `TIPO_TC`, `FECHA_TC`, `FUENTE_TC`, `PRECIO_USD_EQUIVALENTE`, `FECHA_PRECIO`, `PAIS`, `TIPO_PRECIO`, `IVA_TRATAMIENTO`, `FLETE_INCLUIDO`, `CONDICION_ENTREGA`, `ORIGEN_PRECIO_USD`, `NIVEL_EVIDENCIA`, `LECTURA_PRIMARIA`, `FUENTE`, `ESTADO`, `NATURALEZA`, `PCT_VARIABLE`, `ORIGEN_PCT_VARIABLE`, `CENTRO_COSTO`, `TIPO`, `GRUPO_PROVEEDOR`, `INDICE_ACTUALIZACION`, `FECHA_ACTUALIZACION`, `OBSERVACIONES`.

**Registro** ([`registro_costos_operativos.csv`](registro_costos_operativos.csv)): `ESCENARIO`, `CONFIGURACION`, `ESCALA_AVES_DIA`, `MODULO`, `SUBMODULO`, `CONCEPTO`, `COSTO_ID`, `FLUJO`, `CENTRO_COSTO`, `NATURALEZA`, `TIPO`, `APORTANTE`, `FASE`, `DRIVER`, `CANTIDAD`, `UNIDAD`, `ESTADO_DIMENSION`, `INCLUIDO_EN`, `MOTIVO`, `COSTEA`, `PRECIO_USD`, `COSTO_CALCULADO_USD_ANIO`, `COSTO_CONCEPTO_USD_AVE`, `EVIDENCIA`, `PCT_VARIABLE`, `PCT_FIJO`, `FIJO_VARIABLE`, `ESTADO`, `GRUPO_PROVEEDOR`, `MODULO_ARQ`, `BLOQUE`, `AMBITO_GRANJA`, `UNIVERSO_RRHH`, `UNIVERSO_UTILITIES`, `PRECIO_ORIGINAL_OBSERVADO`, `MONEDA_ORIGINAL`, `FECHA_PRECIO`, `CONDICION_ENTREGA`, `IVA_PRECIO`, `TC_USADO`, `FECHA_TC`, `ORIGEN_PRECIO_USD`, `ALERTAS`.

| Campo | Valores |
|---|---|
| `ESTADO_DIMENSION` | DIMENSIONADO · PENDIENTE · INCLUIDO (lo cubre otro concepto: `INCLUIDO_EN`) · INFORMATIVO (aporte de terceros, brecha de jornada) |
| `ESTADO` | CON_PRECIO · PENDIENTE_PRECIO · SIN_TIPO_DE_CAMBIO · PENDIENTE_CANTIDAD · APORTANTE_PENDIENTE · INCLUIDO_EN_OTRO_CONCEPTO · INCLUIDO_EN_TARIFA_FACON · INCLUIDO_EN_TARIFA_FLETE · INFORMATIVO · FUTURO |
| `MODULO_ARQ` / `BLOQUE` | Módulo de la arquitectura y bloque operativo material (completitud, [`metodologia_opex.md`](metodologia_opex.md) §8) |
| `AMBITO_GRANJA` | PROPIA (costo de la empresa) / INTEGRADA (según aportante; costo del productor informativo) |
| `COSTO_CONCEPTO_USD_AVE` | Costo **de ese concepto** por ave faenada (solo filas con precio). **No** es un costo total por ave |

## 4. Administración y comercial

Estructura por mes (12 meses/año, fijo): contabilidad, legales, sistemas, comunicaciones, seguridad/vigilancia, limpieza administrativa, otros; HyS externo solo si 14A lo prevé como servicio; marketing y viajes comerciales. El **personal** de estas áreas está en costo laboral (14A): no se infla una estructura chica con conceptos duplicados. Fees comerciales de canal (alta, CD, aportes, rebates) dependen de las ventas y de condiciones no validadas (DPV-039): se tratarán en el modelo financiero como deducción o gasto comercial, no aquí.

## 5. Seguros

Prima anual por póliza (planta todo riesgo, incendio, RC con producto, mercadería en stock y tránsito, interrupción de negocio, granjas propias) y por vehículo de flota propia y flujo. **No** se usa un porcentaje global sin evidencia. ART va en costo laboral. Todos PENDIENTES (DPV-173).

## 6. Qué no entra

| Concepto | Va a |
|---|---|
| Commissioning, puesta en marcha, capacitación inicial, repuestos y herramientas iniciales, insumos iniciales de laboratorio | CAPEX (bloque PREOPERATIVOS de 19) |
| Depreciación, reemplazos | Modelo financiero (campos en el BOQ de 19) |
| Impuestos a las ganancias, IVA, ingresos brutos, tasas municipales sobre ventas | Modelo financiero |
| Ingresos por subproductos o créditos de façon | Modelo financiero (no se netean: precio ≥ 0, test C02, mutación M07) |
| Costos de productores integrados | Informativos (`APORTANTE = PRODUCTOR_INTEGRADO`) |
