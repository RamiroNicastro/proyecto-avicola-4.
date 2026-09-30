# Especificación del simulador HTML — versión 0.1

**Fecha:** 2026-09-30 · **Estado original:** especificación; el HTML no se construyó en la sesión de escala.

> **Estado actualizado (reconciliación 2026-09-30):** la v0.1 **fue construida** en [`simulador_html/`](simulador_html/README.md) (sesión 09D). Diferencias entre esta especificación y lo construido: [`simulador_html/observaciones_html_v01.md`](simulador_html/observaciones_html_v01.md) §3–4. Este documento se conserva como especificación de origen.

> **Propósito:** que Ramiro y el grupo inversor puedan mover las variables físicas de escala y ver, en una sola pantalla, qué tiene que ser verdad (aves, granjas, alimento, productos, subproductos, inventario, logística, demanda). **Solo física**: la v0.1 **no** muestra CAPEX, OPEX, EBITDA, VAN, TIR ni payback (no están construidos); esos campos quedan **previstos y deshabilitados**.
> **Fuente de verdad:** [`modelo_escala.py`](modelo_escala.py) y [`escenarios_escala.csv`](escenarios_escala.csv) (bloque `tabla_central` como núcleo). El simulador **no debe reimplementar fórmulas distintas** de las del modelo (§5).

---

## 1. Inputs previstos

| # | Input | Tipo / rango | Valor por defecto | Origen del valor por defecto |
|---|---|---|---|---|
| I1 | Escala (aves faenadas/día operativo) | Numérico, 500–30.000; atajos 2.500 / 5.000 / 10.000 / 20.000 | 10.000 | Escenarios de escala (SUP-052) |
| I2 | Días de faena por semana | 5 / 6 | 5 | SUP-025 |
| I3 | Días de operación por año | Numérico ≤ días/semana × 52,14 | 250 (5 d) / 300 (6 d) | SUP-025 |
| I4 | Horas netas de faena por día | 4–20 | 8 | SUP-053 |
| I5 | Peso vivo (kg) | 2,0–3,8 (fuera de rango: bloqueo) | 2,9 | SUP-027; rango válido del balance (SUP-036) |
| I6 | Edad de faena (días) | 35–56 | 47 | SUP-027 |
| I7 | Mortalidad en granja (%) | 0–15 | 5 | SUP-026 |
| I8 | FCR de campo | 1,4–2,2 | 1,70 | SUP-028 |
| I9 | Utilización de capacidad (%) | 10–100 | 70 (nunca 100 por defecto) | SUP-052 |
| I10 | Escenario de demanda | Conservador / Base / Expansivo / Manual (kg/día calendario) | Base | `02_clientes_demanda/escenarios_demanda.csv` (C/D) |
| I11 | Método de conversión de la demanda | M0 ave completa / M1 / M2 / M3 | M0 y M2 lado a lado | SUP-054 |
| I12 | Configuración comercial | A entero / B trozado / C deshuesado | B | SUP-050 (referencia, no decisión) |
| I13 | Días de inventario **y su base temporal** | 1–30 + selector: días de producción / días calendario de cobertura | 3 refrigerado / 14 congelado; base = días de producción | SUP-056 |
| I14 | Perfil de destino | P1 / P2 / P3 / Manual (% refrigerado, congelado, exportación) | P1 | SUP-055 (ilustrativo) |
| I15 | Modelo de abastecimiento | Propias / Integrados / Mixto (% propio) | Mixto 0 % propio | DEC-020 (sin ganador) |
| I16 | m² por productor integrado | Numérico o vacío | **Vacío** (DPV-048) | Si está vacío, el output "productores" muestra "dato pendiente" |
| I17 | Capacidades de vehículos (aves/camión vivo; t por camión refrigerado, de alimento, de subproductos) | Numérico o vacío | Aves/camión 4.000–7.000 (SUP-033); resto **vacío** (DPV-084) | Si está vacío, se muestran toneladas y no camiones |

## 2. Outputs previstos

| Grupo | Outputs | Bloque del CSV / función |
|---|---|---|
| Aves | Aves faenadas/día y /año; aves cargadas; pollitos BB por **semana plena** y **promedio anual** (rotulados por separado); aves vivas simultáneas | `produccion_primaria` / `mp.calcular` |
| Granjas | Plazas; m² de galpón; galpones equivalentes (1.200 / 2.400 m²); productores (si I16) | `produccion_primaria`, `abastecimiento` |
| Alimento y agua | t/semana plena, t/año, alimento de un ciclo de crianza; agua de bebida | `produccion_primaria` |
| Kg vivos | t vivas/día operativo y /año; ritmo de línea (aves/h y kg vivo/h) | `tabla_central`, `ritmo_linea` |
| Productos | Producto principal, coproductos, comestible, **siempre con su base de masa** (biológica / agua retenida / peso comercial); detalle por parte (12 ítems + otros) | `balance_productos`, `masa_comestible`, `configuraciones` |
| Subproductos | Plumas, sangre, vísceras, cabezas, huesos, rendering potencial, sólidos a retirar | `subproductos` |
| Demanda vs capacidad | Tres indicadores separados: **factor demanda/capacidad** (puede superar 100 %), **utilización de capacidad** (0–100 %), **cobertura de demanda** (0–100 %) | `demanda_capacidad` |
| Demanda no atendida / capacidad ociosa | kg/día cal atendidos y **no atendidos**; aves faltantes; **capacidad ociosa** (aves/día operativo); kg sin destino a plena escala; demanda adicional para llenar; excedente de partes | `demanda_capacidad` |
| Inventario | t por categoría (refrigerado, congelado, exportación, subproductos con frío), **en días de producción y en días calendario de cobertura** (dos números rotulados) | `inventario` |
| Logística física | t/día de aves vivas, producto, subproductos, alimento; camiones (si I17) | `logistica` |
| Exportación | Días de faena para 25 t por parte `[PVDP · débil]`; aviso "no es demanda" | `exportacion` |

### 2.1 Variables que la interfaz nunca debe confundir

Cada una se muestra como output **distinto**, con nombre, unidad y base temporal explícitos:

| Output | Definición | Rango / unidad |
|---|---|---|
| **Utilización de capacidad** | aves procesadas / capacidad operativa | 0–100 % (nunca más) |
| **Factor demanda/capacidad** | capacidad que requiere la demanda / capacidad instalada | 0 % a más de 100 % (>100 % = la escala no alcanza; <100 % = capacidad ociosa) |
| **Cobertura de demanda** | producción posible / demanda requerida | 0–100 % |
| **Demanda no atendida** | demanda × (1 − cobertura) | kg/día calendario |
| **Capacidad ociosa** | capacidad × (1 − utilización) | aves/día operativo |
| **Producción por día operativo** | lo que sale en un día de faena | t/día operativo |
| **Producción promedio por día calendario** | producción anual / 365 | t/día calendario |
| **Inventario en días de producción** | producción por día operativo × días | t (base: días de producción) |
| **Inventario en días calendario** | despacho promedio por día calendario × días | t (base: días calendario) |
| **Masa biológica** | carne y tejidos comestibles, sin agua | t |
| **Agua incorporada** | agua retenida en producto (chiller); **no es carne** | t |
| **Peso comercial** | masa biológica + agua retenida (lo que se vende) | t |

Reglas de interfaz: (1) nunca rotular "utilización" a un valor mayor que 100 %; (2) toda cifra diaria lleva "por día operativo" o "por día calendario"; (3) la demanda (día calendario) y la producción (día operativo) solo se comparan convertidas, y la interfaz muestra la conversión (× días operativos / 365); (4) toda cifra de producto dice si es masa biológica o peso comercial; (5) todo inventario muestra su base temporal.

## 3. Pantallas / vistas

1. **Tablero de escala:** inputs a la izquierda; tabla central "qué debe ser verdad" a la derecha ([`escenarios_escala.md`](escenarios_escala.md) §17).
2. **Demanda vs capacidad:** barra de capacidad (100 %) con la utilización elegida y la que justifica cada escenario (M0 y M2); kg sin destino.
3. **Del pollito al producto:** diagrama de flujo con cantidades (pollitos → cargadas → faenadas → kg vivo → comestible / subproductos / residuos).
4. **Comparador A / B / C** (§6).

## 4. Alertas de inconsistencia (obligatorias)

| # | Condición | Mensaje |
|---|---|---|
| AL1 | Demanda documentada A + B = 0 | "La utilización que justifica la evidencia actual es 0 %. Los escenarios son hipótesis C/D." (siempre visible) |
| AL2 | Utilización elegida > utilización que permite la demanda (mín(factor; 100 %)) | "Estás suponiendo más producción de la que la demanda del escenario justifica: habría kg sin destino." |
| AL3 | Factor demanda/capacidad > 100 % | "La demanda del escenario excede la escala: utilización 100 %, cobertura X %, Y kg/día calendario no atendidos (faltan Z aves/día operativo)." |
| AL4 | Excedente de partes > 0 con método M1–M3 | "Aun con la planta llena, X kg/día de partes necesitan otros compradores." |
| AL5 | Peso fuera de 2,0–3,8 kg | Bloqueo: el balance no extrapola (SUP-036) |
| AL6 | Días/año > días/semana × 52,14 | Bloqueo |
| AL7 | Exportación > 0 en la demanda | "Exportación sin negociación de nivel ≥ 5 no es demanda (SUP-022)." |
| AL8 | Productores o camiones sin dato | "Variable pendiente (DPV-048 / DPV-084): se muestran toneladas." |
| AL9 | Utilización = 100 % | "100 % es el punto de dimensionamiento, no un supuesto de operación." |
| AL10 | Kg/local/día equivalente > 300 | "La escala exige más pollo por local que el extremo superior del rango de la red (25–300 kg/local/día)." |
| AL11 | Gates (futuro) | Mostrar qué variables V1–V18 de [`gates_expansion.md`](gates_expansion.md) no tienen evidencia cargada |

## 5. Datos y cálculo

- **v0.1 (propuesta):** el HTML lee un archivo de **coeficientes** exportado por `modelo_escala.py` (a construir: p. ej. `coeficientes_simulador.json` con kg/ave por ítem, configuración y peso en pasos de 0,1 kg; parámetros de producción; mixes) y aplica solo **fórmulas lineales documentadas** (× aves, × días, ÷ horas, ÷ capacidad). Así el HTML no duplica el balance ni el modelo de producción.
- **Prueba de consistencia:** para las 4 escalas × 2 calendarios, el HTML debe reproducir `escenarios_escala.csv` (tolerancia 0,1 %).
- Unidades y bases rotuladas en cada número (vivo / comercial / subproducto; día operativo / día calendario / semana plena / promedio anual).

## 6. Tabla de escenarios A / B / C (comparación lado a lado)

Plantilla para que el usuario compare tres configuraciones completas (no confundir con las configuraciones comerciales A/B/C del balance: aquí A/B/C son **escenarios del usuario**).

| Campo | Escenario A | Escenario B | Escenario C |
|---|---|---|---|
| Nombre | (editable) | (editable) | (editable) |
| Escala (aves/día) | | | |
| Días/semana · días/año | | | |
| Horas netas | | | |
| Peso · edad · mortalidad · FCR | | | |
| Utilización | | | |
| Escenario y método de demanda | | | |
| Configuración comercial | | | |
| Días de inventario · perfil de destino | | | |
| Modelo de abastecimiento | | | |
| → Aves/año · t vivas/año | | | |
| → Pollitos/semana plena · plazas · m² | | | |
| → Alimento t/año | | | |
| → Producto principal · comestible (t/día) | | | |
| → Rendering potencial (t/día) | | | |
| → Factor demanda/capacidad · utilización · cobertura | | | |
| → kg/día cal no atendidos · capacidad ociosa (aves/día op.) · kg sin destino | | | |
| → Comestible: masa biológica · agua retenida · peso comercial | | | |
| → Inventario (t): días de producción · días calendario | | | |
| → t/día que entran y salen | | | |
| → Alertas activas | | | |
| CAPEX (USD) | *versión futura* | *versión futura* | *versión futura* |
| OPEX (USD/año) | *versión futura* | *versión futura* | *versión futura* |
| EBITDA | *versión futura* | *versión futura* | *versión futura* |
| VAN · TIR · payback | *versión futura* | *versión futura* | *versión futura* |

Ejemplo precargado sugerido (solo para demostrar la vista): A = 2.500 · 5 d · B · base; B = 5.000 · 5 d · B · base; C = 10.000 · 6 d · C · expansivo.

## 7. Fuera de alcance de la v0.1

CAPEX, OPEX, precios, ingresos, EBITDA, VAN, TIR, payback, capital de trabajo monetario, maquinaria, layout, localización, efluentes y energía (módulos no construidos al especificar; agua, efluentes, energía y frío existen desde la sesión 09C como modelo preliminar en `11_agua_efluentes/`, pero **no** están integrados al HTML v0.1). Los campos existen en la interfaz como **"versión futura"**, deshabilitados, para que la estructura no cambie cuando se incorporen.
