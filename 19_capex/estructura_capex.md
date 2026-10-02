# Estructura del CAPEX — bloques, conceptos e identificadores

**Fecha:** 2026-10-02 · Fuente de verdad de los conceptos: [`base_costos_capex.csv`](base_costos_capex.csv) (175 filas). Fórmulas: [`metodologia_capex.md`](metodologia_capex.md).

## 1. Bloques de resumen

| Bloque | Categoría | Contenido | Activo si… |
|---|---|---|---|
| TERRENO | Directo | Compra (TER-01/02/03), gastos de compra (TER-04, %), preparación (TER-05), acceso (TER-06), conexiones extraordinarias (TER-07), cargo de parque industrial (TER-08) | Planta de faena propia |
| OBRA_CIVIL | Directo | 14 categorías de obra + cerco + infraestructura del predio ([`obra_civil_capex.md`](obra_civil_capex.md)); oficina asset-light (OC-ADM) | Siempre (asset-light: solo OC-ADM) |
| PROCESO | Directo | Lotes RFQ L1–L7 o L11 + higiene (EQ-LIM); EQ-01…EQ-76 como hijos | Planta propia |
| SUBPRODUCTOS | Directo | Lote L9 (SB-L9); tratamiento básico propio (SB-BAS); rendering FUTURO (SB-REN) | Planta propia |
| FRIO | Directo | Paquete de frío FR-PAQ con hijos: paneles, compresores, condensación, evaporadores, piping, refrigerante, controles, agua helada, docks, túnel | Planta propia |
| UTILITIES | Directo | Agua (AG-*), electricidad (EL-*), térmico (TE-*), aire comprimido (AC-COM) | Planta propia |
| EFLUENTES | Directo | Paquete EF-PAQ con hijos: pretratamiento, ecualización, fisicoquímico, biológico, lodos, infraestructura | Planta propia |
| SERVICIOS_GENERALES | Directo | IT y trazabilidad (IT-*), laboratorio (LAB-EQ), seguridad e incendio (SI-*), equipamiento de personal y mobiliario | Siempre |
| LOGISTICA | Directo | Por flujo: vehículo, carrocería, equipo de frío, equipo auxiliar; cajones, cajas y contenedores | Algún flujo con flota propia |
| INCUBACION | Directo | INC-* (15 conceptos, setter y hatcher separados); reproductoras REP-* FUTURO | Pollito = incubación |
| ALIMENTO | Directo | ALI-* (18 conceptos) | Alimento = planta propia |
| GRANJAS | Directo | GRA-* (galpón + 8 componentes) | Fracción de granjas propias > 0 |
| INDIRECTOS | Indirecto | Ingeniería, arquitectura, proyecto ejecutivo, dirección de obra, PM, permisos, estudios | Siempre |
| PREOPERATIVOS | Preoperativo | Commissioning, puesta en marcha, capacitación, pruebas FAT/SAT, repuestos y herramientas iniciales, insumos iniciales de laboratorio, implementación IT | Siempre |
| CONTINGENCIA | Contingencia | CON-DIS (diseño/cantidades), CON-COS (costo), CON-ESC (escalación) | Siempre |

Un bloque inactivo se publica como **EXCLUIDO_POR_ARQUITECTURA** con valor 0: es una exclusión de diseño, no un dato faltante (test A01).

## 2. Qué NO entra (y por qué)

| Concepto | Va a |
|---|---|
| Alimento, pollitos, huevo fértil e insumos de operación normal | Capital de trabajo / OPEX |
| Inventarios comerciales, cuentas por cobrar | Capital de trabajo |
| Alquileres, suscripciones de software, contratos de servicio (capa C17) | OPEX |
| Reemplazo de activos en años futuros | Modelo financiero (campos preparados) |
| Valor residual | Modelo financiero (campo preparado) |
| IVA recuperable, créditos fiscales, beneficios promocionales, depreciación | Modelo financiero (DPV-16-17) |
| Galpones de productores integrados | Informativo (`CAPEX_TERCEROS_INFORMATIVO_USD`), no CAPEX de la empresa |
| Reproductoras y rendering | `FASE = FUTURO`, fuera del CAPEX inicial |

## 3. Columnas de la base de costos

| Grupo | Columnas |
|---|---|
| Identificación | `ID_COSTO`, `MODULO`, `SUBMODULO`, `CONCEPTO`, `DESCRIPCION` |
| Cantidad de referencia | `CAPACIDAD_REFERENCIA` (admite rango "8-10"), `UNIDAD_CAPACIDAD`, `CANTIDAD`, `UNIDAD` |
| Precio | `METODO_COSTEO`, `PRECIO_UNITARIO`, `PRECIO_BAJO`, `PRECIO_ALTO`, `ORIGEN_RANGO`, `EXPONENTE_ESCALA`, `BASE_PORCENTAJE` |
| Moneda y fecha | `MONEDA_ORIGINAL`, `TC_MONEDA_POR_USD`, `TIPO_TC`, `FECHA_TC`, `FECHA_PRECIO`, `PAIS` |
| Condición comercial | `TIPO_PRECIO`, `INCOTERM`, `ORIGEN_EQUIPO`, `FLETE_INCLUIDO`, `IMPUESTOS_INCLUIDOS`, `IVA_TRATAMIENTO`, `ALICUOTA_IVA`, `INSTALACION_INCLUIDA`, `PUESTA_EN_MARCHA_INCLUIDA`, `CONTINGENCIA_INCLUIDA`, `COSTO_INSTALADO`, `FACTOR_INSTALADO_SENSIBILIDAD` |
| Evidencia | `NIVEL_EVIDENCIA`, `LECTURA_PRIMARIA`, `FUENTE`, `ESTADO` |
| Para el modelo financiero | `VIDA_UTIL_ANIOS`, `REEMPLAZO_ANIO`, `COSTO_REEMPLAZO`, `VALOR_RESIDUAL` (vacíos) |
| Texto | `OBSERVACIONES` |

**Vacío = desconocido. 0 = costo cero real** (test M10).

## 4. Columnas del BOQ ([`boq_capex.csv`](boq_capex.csv))

`ESCENARIO`, `ACTIVO_ID`, `ARQUITECTURA`, `MODULO`, `SUBMODULO`, `BLOQUE`, `CATEGORIA_CAPEX`, `ACTIVO`, `CAPACIDAD`, `UNIDAD_CAPACIDAD`, `CANTIDAD_BAJO`, `CANTIDAD`, `CANTIDAD_ALTO`, `UNIDAD`, `ORIGEN_DIMENSIONAMIENTO`, `COSTO_ID`, `INCLUIDO_EN_PAQUETE`, `ACTIVO_PADRE`, `COSTEA`, `ETIQUETA_EXPANSION`, `REUTILIZABLE`, `ESCALABLE`, `FASE`, `TITULAR`, `NIVEL_AUTOMATIZACION`, `ESTADO_DIMENSION`, `ESTADO_COSTO`, `NIVEL_EVIDENCIA`, `MONEDA_ORIGINAL`, `PRECIO_UNITARIO_USD`, `COSTO_EQUIPO_USD`, `COSTO_LANDED_USD`, `COSTO_INSTALADO_LOW_USD`, `COSTO_INSTALADO_USD`, `COSTO_INSTALADO_HIGH_USD`, `ORIGEN_RANGO`, `VIDA_UTIL_ANIOS`, `REEMPLAZO_ANIO`, `COSTO_REEMPLAZO`, `VALOR_RESIDUAL`, `ALERTAS`.

| Campo | Valores |
|---|---|
| `ESTADO_DIMENSION` | DIMENSIONADO · COTA_INFERIOR · PENDIENTE · INFORMATIVO (EQ hijos) |
| `ESTADO_COSTO` | CON_PRECIO · SIN_PRECIO · SIN_CANTIDAD · SIN_TIPO_DE_CAMBIO · PRECIO_PARCIAL · IVA_NO_SEPARADO · FUERA_DE_RANGO_REFERENCIA · BASE_SIN_PRECIO · INCLUIDO_EN_PAQUETE · ALCANCE_PENDIENTE |
| `TITULAR` | EMPRESA · PRODUCTOR_INTEGRADO · PENDIENTE |
| `FASE` | INICIAL · FUTURO |
| `ETIQUETA_EXPANSION` | REUTILIZABLE · ESCALABLE · DUPLICABLE · REEMPLAZABLE · ESPECIFICO_DE_FASE · MIXTA (paquete: se resuelve en los hijos) |

## 5. Conteo por configuración (10.000 aves/día)

| Config. | Filas BOQ | Filas que costean | EQ informativos | Titular ≠ empresa | Futuro | Conceptos costeables de la empresa |
|---|---|---|---|---|---|---|
| C0 | 31 | 23 | 0 | 10 | 0 | 21 |
| C1 | 166 | 79 | 63 | 11 | 0 | 76 |
| C2 | 185 | 90 | 63 | 10 | 0 | 88 |
| C3 | 225 | 138 | 63 | 0 | 0 | 138 |
| CF | 228 | 141 | 63 | 0 | 3 | 138 |

Salida de `modelo_capex.py` (2026-10-02). La diferencia entre "filas que costean" y "conceptos de la empresa" son galpones de integrados, cajones de titularidad pendiente y conceptos futuros.
