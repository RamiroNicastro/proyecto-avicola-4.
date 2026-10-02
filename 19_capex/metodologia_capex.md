# Metodología del motor CAPEX

**Versión:** 1.0 · **Fecha:** 2026-10-02 · **Modelo:** [`modelo_capex.py`](modelo_capex.py) · **Sesión:** 16

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

- **CAPEX con precio** (USD), desagregado por nivel de evidencia E1…E5; **conocido** = E1 + E2; **estimado** = E3 + E4 + E5.
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

Ver [`README.md`](README.md). Las pruebas (58) y las mutaciones (5) están en el mismo script; si una prueba falla, el script se detiene sin escribir CSV.
