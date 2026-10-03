# Arquitecturas de inversión configurables

**Fecha:** 2026-10-02 · Implementación: `config_por_defecto()`, `preset()` y `validar_config()` en [`modelo_capex.py`](modelo_capex.py)

> Ninguna arquitectura se declara "mejor". Las configuraciones C0–C3 y CF son **referencias de comparación** (SUP-163, SUP-152), no una recomendación ni una secuencia obligatoria. El motor solo dice **qué se construye, qué se compra, qué se terceriza y qué cantidad física implica**.

## 1. Opciones por eslabón (inputs del motor)

| Eslabón | Input | Opciones | Efecto en el BOQ |
|---|---|---|---|
| Faena | `faena` | `propia` · `facon` | `facon`: sin terreno, obra de planta, proceso, frío, utilities, efluentes ni subproductos (test A06); queda oficina asset-light (OC-ADM) |
| Producción primaria | `granjas` + `fraccion_granjas_propias` | `integradas` (0) · `propias` (1) · `mixto` (0–1) | Galpones propios = CAPEX de la empresa; galpones de integrados = `TITULAR = PRODUCTOR_INTEGRADO`, **informativo** (test A05) |
| Pollito BB | `pollito` (+ `reproductoras`) | `compra` · `incubacion` · reproductoras propias solo como **FUTURO** (exige incubación, test A08) | Incubación: 15 conceptos con setter y hatcher separados; reproductoras: `FASE = FUTURO` |
| Alimento | `alimento` | `compra` · `facon` · `propia` | `propia`: 18 conceptos ALI-* con la t/h de 14B; `compra` y `facon`: sin activos de planta (test A02) |
| Logística | `flota` (+ `flota_por_flujo`) | `tercero` · `propia` · `mixto` (por flujo) | Vehículos solo en flujos propios (tests A03, A04); flujos: pollitos, alimento/granos, aves vivas, refrigerado, congelado, subproductos, servicio |
| Frío / producto | `frio` | `A_refrigerado` · `B_refrigerado_congelado` · `C_congelado_tercero` | A → perfil P1 con congelado propio mínimo; B → P2; C → P1 sin túnel propio (SUP-158, test A10) |
| Subproductos | `subproductos` (+ `rendering`) | `A_externo` · `B_basico_propio` · rendering **FUTURO** | B agrega SB-BAS; rendering = `FASE = FUTURO` (SUP-168) |
| Terreno | `terreno` (+ `escala_objetivo`) | `compra_fase` · `compra_reserva` · `parque_industrial` · `rural_compatible` | Necesidad de terreno de la arquitectura (fase, o crecimiento hasta la escala objetivo + rendering) y tipo de precio (SUP-170); la superficie a comprar se elige con `criterio_terreno` |
| Línea | `modalidad_linea` | `lotes` · `llave_en_mano` | Llave en mano: L1–L5 hijos de L11 (test A09) |
| Automatización | `automatizacion` | `manual` · `semi` · `auto` | Nivel de cada EQ donde la matriz 08 deja "M/S" (SUP-159) y superficie de 12C |
| Otros | `dias_semana`, `horas_netas`, `laboratorio_propio`, `tecnologia_efluentes`, `config_producto` (A/B/C), `fecha_base`, capacidades de vehículos, distancias | — | Pasan a los módulos de origen |

Combinaciones inválidas que el motor rechaza: reproductoras sin incubación; rendering sin planta propia; flota mixta sin definir cada flujo; fracción de granjas incompatible con la opción; escala fuera de 2.500–20.000; moneda distinta de USD.

## 2. Configuraciones de referencia

| | C0 asset-light | C1 planta de faena | C2 faena + activos selectivos | C3 mayor integración | CF futura |
|---|---|---|---|---|---|
| Faena | façon | propia | propia | propia | propia |
| Granjas | integradas | integradas | mixto 25 % propias | 100 % propias | 100 % propias |
| Pollito | compra | compra | compra | incubación (huevo comprado) | incubación + reproductoras (FUTURO) |
| Alimento | façon | compra | façon | planta propia | planta propia |
| Flota | tercero | tercero | propia: aves vivas, refrigerado, servicio | propia en todos los flujos | propia |
| Frío | congelado tercero | A refrigerado | B refrigerado + congelado | B | B |
| Subproductos | externo | externo | externo | básico propio | básico propio + rendering (FUTURO) |
| Terreno | — | compra de la fase | compra de la fase | compra de la fase | compra de la fase |

Variantes calculadas sobre C1 a 10.000 aves/día: escala objetivo de terreno 20.000, parque industrial, rural compatible, congelado tercerizado, congelado propio, subproductos básicos, línea llave en mano, automatización manual y automática, 6 días/semana; y C1 a 5.000 con escala objetivo de terreno 20.000. Resultados en [`capex_por_escala.md`](capex_por_escala.md).

## 3. Qué se construye, qué se compra, qué se terceriza

| Config. | Se construye / instala (empresa) | Se compra como servicio o insumo | Activos de terceros (informativos) |
|---|---|---|---|
| C0 | Oficina, IT, mobiliario | Faena a façon, pollito, alimento a façon, transporte, congelado | Galpones de integrados (100 %) |
| C1 | Planta de faena completa: terreno, obra, proceso, frío, utilities, efluentes, subproductos (L9), IT, laboratorio | Pollito, alimento, transporte | Galpones de integrados (100 %); cajones con titularidad PENDIENTE |
| C2 | C1 + túnel/cámaras de congelado + flota de aves vivas, refrigerado y servicio + 25 % de galpones | Pollito, alimento a façon, resto del transporte | Galpones de integrados (75 %) |
| C3 | C2 + incubadora + planta de alimento + 100 % de galpones + flota completa + subproductos básicos | Huevo fértil | — |
| CF | C3 + reproductoras y rendering (FUTURO, fuera del CAPEX inicial) | — | — |

## 4. Lo que el motor no decide

Escala (DEC-001), eslabones de la primera etapa (DEC-002), modelo de abastecimiento (DEC-020), pollito (DEC-023), alimento (DEC-024), subproductos (DEC-027), arquitectura de crecimiento (DEC-033), sobredimensionamiento (DEC-035), automatización (DEC-037), líneas (DEC-038), efluentes (DEC-043), frío (DEC-046), respaldo (DEC-047), proveedores (DEC-049), red R1/R2 (DEC-053), flota (DEC-056), terreno (DEC-063), congelado (DEC-064), laboratorio (DEC-065), gates upstream (DEC-074).
