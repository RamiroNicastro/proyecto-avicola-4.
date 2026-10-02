# Metodología del motor CAPEX

**Versión:** 1.1 (auditoría de procedencia de drivers) · **Fecha:** 2026-10-02 · **Modelo:** [`modelo_capex.py`](modelo_capex.py) · **Sesión:** 16

> Pregunta que responde: **¿cuánto capital requiere construir y poner operativa cada configuración del proyecto?**
> El motor **no** elige escala, arquitectura, tecnología ni proveedor, y **no** calcula OPEX, ingresos, EBITDA, VAN/TIR/payback ni capital de trabajo.

## 1. Principio: separar cantidades de precios

```
DRIVERS FÍSICOS (módulos 03, 09/12C, 11/09C, 13/12B, 14B, 08)   →  BOQ (qué se compra/construye, cuánto)
BASE DE COSTOS externa (base_costos_capex.csv)                  →  precio, moneda, Incoterm, evidencia
CAPAS DE IMPORTACIÓN (capas_importacion_capex.csv)              →  flete, seguro, aduana, montaje, PEM…
                                    ↓
COSTEO por fila (solo si hay precio Y cantidad; vacío ≠ 0)
                                    ↓
RESUMEN por bloque: con precio / sin precio / sin cantidad / alcance pendiente, por nivel de evidencia
```

- Las **cantidades** vienen de los modelos aprobados; el motor **no** las recalcula (las importa llamando a sus funciones).
- Los **precios** viven fuera del código. Cambiar un precio o agregar una cotización = editar el CSV; el motor no se toca.
- Un **precio sin cantidad** o una **cantidad sin precio** quedan PENDIENTES. Nunca se reemplazan por cero.

## 2. Fuentes de las cantidades (drivers)

| Driver | Origen | Uso en el BOQ |
|---|---|---|
| m² por área (bajo/medio/alto) y terreno conceptual | `09_layout_obra_civil/modelo_superficies.py` (12C) | Obra civil por categoría, terreno, cerco, infraestructura del predio |
| Agua captada/descargada, caudal máximo ilustrativo, DQO, kW medios, cargas de frío preliminares, térmico, cargas críticas | `11_agua_efluentes/modelo_utilities.py` (09C) vía 12C | Agua, efluentes, frío (cota inferior), eléctrico y térmico (cotas) |
| Viajes y flota mínima por flujo | `13_logistica/modelo_logistica.py` (12B) | Vehículos por flujo (solo si la flota es propia) |
| Pollitos, setters y hatchers por cadencia, almacén de huevo, t/h de planta de alimento, silos, plazas de galpón | `14_alimento_balanceado/modelo_upstream.py` (14B) | Incubación, planta de alimento, granjas |
| Equipos EQ-01…EQ-76, nivel de automatización por escala, modularidad | `08_maquinaria/matriz_equipos.csv` (09A) | Hijos de los lotes RFQ, etiquetas de expansión |

**Superficie conceptual ≠ proyecto ejecutivo.** Los m² de 12C son órdenes de magnitud (muchos en estado PROXY); el costo de obra hereda esa incertidumbre.

## 2 bis. Procedencia de los drivers: consumir, no recalcular

Regla: CAPEX **consume** salidas de los módulos anteriores; no produce una versión alternativa del mismo dimensionamiento. Cada driver queda registrado en [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv) con valor (bajo/medio/alto), unidad, archivo y variable de origen, escenario fuente, tipo y estado de evidencia.

| Tipo | Significado | Ejemplos |
|---|---|---|
| `DIRECTO` | Salida del módulo fuente para un escenario **publicado** en su CSV; un test lo verifica contra el CSV | m² construidos (12C `referencia` / `perfil_P2`), terreno con reserva (12C `objetivo_20000`), setters y hatchers (14B), plazas (03), flota de aves vivas (12B), agua y energía (09C) |
| `CALCULO_MODELO_FUENTE` | La **misma función** del módulo fuente con entradas que su CSV no publica (escala intermedia, perfil o modalidad no publicados). **No es interpolación** | todo driver a 7.500 o 15.000 aves/día; terreno requerido por la fase (12C no publica terreno sin reserva) |
| `DERIVADO_CAPEX` | Operación declarada de CAPEX sobre salidas fuente | ⌈camión-día⌉, perímetro del terreno, suma de áreas por categoría, silos de maíz + soja |
| `SUPUESTO_CAPEX` | Parámetro propio (SUP-16-##) | reserva de flota, ciclo de vehículos de alimento, días de reserva de agua |
| `PENDIENTE` | El módulo fuente no lo dimensiona; CAPEX no lo inventa | carga frigorífica total, pico eléctrico, transformador, grupo, caldera, lodos, granjas |
| `INTERPOLADO` | No se usa en ningún driver | — |

Escenarios **etiquetados** (inputs explícitos, no verdades): horas netas (8), sensibilidad de rendimiento de línea (`media` de 05), cadencia de nacimientos (2/semana), margen de incubación (15 %), perfil de fabricación de alimento (5 d × 8 h, η 0,85, margen 15 %), días de stock y densidades de silos (14B), capacidades de vehículos (12B). Se listan en `escenarios_referencia` y en el mapa de drivers.

Consistencias entre fuentes que dos módulos calculan por separado (efluente 12C vs 09C, plazas 14B vs 03, ritmo 05 vs 23) se verifican en cada corrida: una diferencia genera `DRIVER_INCONSISTENTE` y **no se corrige** (test N13).

Escala intermedia: alerta `ESCALA_INTERMEDIA`; todos los drivers son `CALCULO_MODELO_FUENTE`; los niveles de automatización de los equipos (matriz 08, solo en 4 escalas) se toman de la escala de referencia más cercana (SUP-16-05).

## 2 ter. Capacidad de planta ≠ capacidad de línea

| Magnitud | Fuente | Uso |
|---|---|---|
| Capacidad de **planta** (aves/día) | input de escala (SUP-052) | escala del escenario |
| Ritmo **operativo** requerido (aves/h) = aves/día ÷ horas netas | 05 `ritmo_operativo_requerido` | referencia; **no** es capacidad comercial |
| Ritmo **nominal** requerido (aves/h) = aves/día ÷ (h × R) | 05, R = 0,95 / 0,89 / 0,82 (SUP-061) | capacidad de los lotes de línea en el BOQ (sensibilidad `media` por defecto, input) |
| Capacidad de **diseño** | — | PENDIENTE (margen no adoptado) |
| Capacidad **garantizada** | cotización | PENDIENTE (DPV-097) |
| Líneas | 12C (1) | capacidad por línea = nominal ÷ líneas |

La v1.0 usaba el ritmo operativo (aves/día ÷ horas) como capacidad de los lotes; la v1.1 usa el nominal de 05 y muestra todas las capas en `CAPACIDAD_DETALLE`.

## 3. Fórmulas

| Método (`METODO_COSTEO`) | Fórmula | Condición |
|---|---|---|
| `unitario` | costo = cantidad × precio unitario (USD) | unidad del BOQ = unidad del precio |
| `global` | costo = precio del lote | cantidad = 1 lote |
| `escalado` | costo = precio_ref × (capacidad ÷ capacidad_ref)^exponente | exponente **explícito**; sin exponente, solo dentro del rango de la referencia (SUP-16-13) |
| `porcentaje` | costo = % × base declarada | base sin precio → PENDIENTE (no 0); base parcial → alerta `BASE_INCOMPLETA` |

**Moneda.** `precio_USD = precio_original ÷ TC_MONEDA_POR_USD`. Un precio en ARS u otra moneda **sin** tipo de cambio, fecha y tipo de TC no entra (error de validación si se marca `CON_PRECIO`; estado `SIN_TIPO_DE_CAMBIO` si no). La fecha base es editable (`FECHA_BASE_CAPEX`, SUP-16-01).

**Equipo → instalado** (detalle en [`maquinaria_capex.md`](maquinaria_capex.md) §3):
1. Si la base trae `COSTO_INSTALADO`, se usa.
2. Si el precio ya es instalado (`INSTALACION_INCLUIDA = Sí`, flete incluido o no aplica, Incoterm `NA`/`INSTALADO`), se usa el precio.
3. Si hay capas de importación/instalación cargadas, se apilan: Incoterm → landed → instalado.
4. Solo en **modo sensibilidad** se acepta `precio × FACTOR_INSTALADO_SENSIBILIDAD` (marcado).
5. Si no, la fila queda **PRECIO_PARCIAL**: el equipo tiene precio pero **no** suma al CAPEX.

**Rangos.** LOW/HIGH solo donde el precio declara `ORIGEN_RANGO`; se combinan cantidad baja × precio bajo y alta × alta (SUP-16-08). No hay ±20 % automático.

## 4. Separaciones obligatorias

| Se separa | De | Cómo |
|---|---|---|
| CAPEX directo | Indirectos, preoperativos, contingencia | `CATEGORIA_CAPEX` y bloques propios ([`estructura_capex.md`](estructura_capex.md)) |
| Terreno | Obra civil | Bloque TERRENO; además, el terreno no integra la base de los porcentajes |
| Tres contingencias | Entre sí | CON-DIS (diseño/cantidades), CON-COS (costo), CON-ESC (escalación) |
| CAPEX de la empresa | CAPEX de productores integrados | `TITULAR`; los galpones de integrados se informan aparte |
| CAPEX inicial | Arquitectura futura | `FASE = FUTURO` (reproductoras, rendering) |
| CAPEX | Capital de trabajo | No hay alimento, pollitos, inventarios ni cuentas por cobrar en el BOQ (test P05) |
| CAPEX inicial | Reemplazos y valor residual | Campos `VIDA_UTIL_ANIOS`, `REEMPLAZO_ANIO`, `COSTO_REEMPLAZO`, `VALOR_RESIDUAL` vacíos, para el modelo financiero |
| Costo económico | IVA recuperable | SUP-16-12; no se resuelve la fiscalidad |

## 5. Reglas contra el doble conteo

1. Cada área de 12C pertenece a **una** categoría de obra (test M06).
2. Cada EQ tiene **un** costeador (test M05). EQ-28/EQ-33 figuran en dos lotes RFQ: se asignan a L3 (T16-01).
3. Las filas `INCLUIDO_EN_PAQUETE = Sí` (hijas de un paquete) **no** se costean; `PENDIENTE` = alcance a confirmar, tampoco se costean y se cuentan aparte (test M04).
4. Modalidad llave en mano: L1–L5 pasan a ser hijos de L11 (test A09).
5. La obra civil se costea en `OC-*`: la capa C10 de las ofertas (obra a cargo del comprador) se excluye del instalado.
6. Puesta en marcha, capacitación y repuestos: si el paquete los incluye (`PUESTA_EN_MARCHA_INCLUIDA = Sí`) se excluye de la base del porcentaje; si es `PENDIENTE`, alerta `POSIBLE_DOBLE_CONTEO`.
7. La contingencia no se aplica sobre conceptos con `CONTINGENCIA_INCLUIDA = Sí` (test P03).

## 6. Qué se publica

Por escenario y por bloque ([`escenarios_capex.csv`](escenarios_capex.csv)):

- **Monto con precio** (USD), siempre **separado por evidencia**: `CAPEX_E1_E2_USD`, `CAPEX_E3_USD`, `CAPEX_E4_USD`, `CAPEX_E5_USD`; los faltantes como conteo (`CAPEX_PENDIENTE_CONCEPTOS`). `CALIDAD_MONTO` dice qué es ese número (`MONTO_CON_REFERENCIAS_DEBILES_E4` cuando solo hay E4). No existe una columna "CAPEX conocido".
- **Cobertura por nivel de evidencia** (conteos, no %): `N_CONCEPTOS_E1_E2`, `N_CONCEPTOS_E3`, `N_CONCEPTOS_E4`, `N_CONCEPTOS_E5`, `N_CONCEPTOS_PENDIENTES`.
- **Conceptos** costeables, con precio, sin precio, sin cantidad, con precio parcial y con alcance pendiente.
- **Cobertura por conceptos** = con precio ÷ costeables.
- **Cobertura por valor**: solo si todos los faltantes tienen una magnitud estimada; si no, "NO CALCULABLE" (hoy, en todos los escenarios).
- **Total preliminar**: solo con cobertura completa (SUP-16-10). Si no, "NO DISPONIBLE: N conceptos sin costo".

## 7. Qué no hace (y dónde irá)

| Tema | Dónde |
|---|---|
| OPEX, costo por ave, capital de trabajo | `20_opex` |
| VAN, TIR, payback, financiación, depreciación, IVA, valor residual | `21_modelo_financiero` |
| Elección de escala, arquitectura o trayectoria | Optimizador posterior al modelo financiero (`23_plan_expansion`) |
| Selección de proveedores | Bloqueada por la fase (DEC-049) |

## 8. Ejecución

Ver [`README.md`](README.md). Las pruebas (77) y las mutaciones (9) están en el mismo script; si una prueba falla, el script se detiene sin escribir CSV.
