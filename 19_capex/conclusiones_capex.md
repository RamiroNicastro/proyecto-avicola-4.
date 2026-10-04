# Conclusiones — Motor CAPEX v1.0 (sesión 16)

**Fecha:** 2026-10-02 (v1.1, con auditoría de procedencia de drivers) · Estado: **motor construido y probado; CAPEX sin costear** · Registros propuestos: [`actualizaciones_gestion_16.md`](actualizaciones_gestion_16.md)

## 1. Qué se construyó

- **Motor reproducible** ([`modelo_capex.py`](modelo_capex.py)) que arma el registro de activos (BOQ) de cualquier configuración entre 2.500 y 20.000 aves/día a partir de los modelos aprobados (12C, 09C, 12B, 14B, 09A) y lo cruza con una **base de costos externa** (175 conceptos) y una tabla de **capas de importación/instalación**.
- **11 ejes de arquitectura** configurables (faena, granjas, pollito, reproductoras, alimento, flota por flujo, frío, subproductos, rendering, terreno, línea) + automatización, días/semana, fecha base y capacidades.
- **5 configuraciones de referencia** (C0, C1, C2, C3, CF) × 4 escalas + 2 escalas intermedias + 11 variantes = **33 escenarios** en [`escenarios_capex.csv`](escenarios_capex.csv); **5.485 filas** de BOQ (243 activos distintos); **2.508 filas** de expansión; **13 RFQ**.
- **82 tests** + **10 mutaciones** detectadas (v1.2).
- **Mapa de procedencia** de cada driver físico ([`mapa_drivers_capex.csv`](mapa_drivers_capex.csv), 1.030 filas): directo / cálculo del modelo fuente / derivado CAPEX / supuesto CAPEX / pendiente.

## 2. Resultado central

**No existe todavía un CAPEX total para ninguna configuración.** De 175 conceptos de la base, **167 no tienen precio**; los 8 con precio son E4 `[PVDP]` (extractos de prensa o web, ninguno leído en original). Cobertura por conceptos: **0 % (C0), 1,3 % (C1), 2,3 % (C2), 1,4 % (C3/CF)**. Cobertura por valor: **no calculable**. El motor responde "NO DISPONIBLE" en lugar de un total engañoso.

## 3. Qué números pueden usarse

| Utilizable (orden de magnitud, con su clasificación) | Dónde |
|---|---|
| Qué activos requiere cada arquitectura y en qué paquete se cotizan (sin doble conteo) | [`boq_capex.csv`](boq_capex.csv), [`maquinaria_capex.md`](maquinaria_capex.md) |
| Superficies por categoría de obra y terreno (con y sin reserva) | [`obra_civil_capex.md`](obra_civil_capex.md) |
| Agua, efluente, DQO, potencia media, cotas de frío y térmico | [`utilities_capex.md`](utilities_capex.md) |
| Flota por flujo (con supuestos de capacidad) | [`logistica_capex.md`](logistica_capex.md) |
| Posiciones de setter y hatcher, t/h y silos de planta de alimento, plazas de galpón | [`upstream_capex.md`](upstream_capex.md) |
| Mapa físico de expansión (qué se reutiliza, amplía, duplica o reemplaza) | [`expansion_capex.md`](expansion_capex.md) |
| Lista de cotizaciones necesarias y su especificación mínima | [`plan_cotizaciones.md`](plan_cotizaciones.md) |

## 4. Qué números NO deben usarse para decidir una inversión

| Número | Por qué no |
|---|---|
| Monto con precio de C1 (USD 43.779–222.431; `MONTO_CON_REFERENCIAS_DEBILES_E4`) | Cubre solo depósitos y talleres secos (1 de 76 conceptos), con un USD/m² de blog comercial (E4) |
| Monto con precio de C2/C3 (USD 0,39–11,3 M; `MONTO_CON_REFERENCIAS_DEBILES_E4`) | 89–98 % es una **cota inferior de prensa** para galpones de alcance desconocido (T16-03); la planta, la incubadora y la fábrica de alimento no tienen precio |
| Diferencias de CAPEX entre configuraciones o entre escalas | Reflejan qué conceptos tienen precio, no cuánto cuesta cada opción |
| Acumulado igual entre trayectorias de expansión | Artefacto del precio unitario lineal; la prima de ampliación es PENDIENTE |
| Cualquier comparación contra USD 2 M | El capital del grupo inversor no es límite ni referencia de suficiencia (SUP-003, DEC-010); con 1–2 % de cobertura no puede afirmarse ni que alcanza ni que no alcanza |

## 4 bis. Auditoría de procedencia de drivers (cierre de la sesión 16)

Se verificó que CAPEX **consume** las salidas de 12C, 09C, 12B, 14B, 03, 05 y 08 y no recalcula dimensionamientos. Hallazgos y correcciones (detalle en [`actualizaciones_gestion_16.md`](actualizaciones_gestion_16.md) §7):

| Hallazgo v1.0 | Corrección v1.1 |
|---|---|
| Terreno "solo fase" (15.398 / 32.379 m²) presentado como terreno de 12C; 12C no lo publica | Rotulado como terreno **requerido** (CALCULO_MODELO_FUENTE); se informa al lado el terreno publicado por 12C; adquirido ≥ requerido verificado |
| m² de P2 (1.796 / 7.795) presentados sin indicar el perfil | Tablas con escenario de 12C explícito (`referencia` P1 o `perfil_P2`) |
| Infraestructura del predio y preparación del sitio sobre **todo** el terreno (incl. retiros, buffers, reserva) | OC-INF = lote; preparación = terreno requerido |
| Frío: "cota" = suma de cargas de 09C incluida una ilustrativa, usada como capacidad del RFQ | Sin capacidad; base física, benchmark, contradicción ×5,7, diseño y margen PENDIENTES |
| Ecualización = volumen diario (24 h implícitas); biológico = máximo de dos métodos | Ambos PENDIENTES con los valores de 09C informados |
| Subproductos: suma propia de 4 corrientes | Variable de 09C `masa_biologica_potencialmente_segregable_en_origen_t_dia` |
| Capacidad de línea = aves/día ÷ horas | Nominal requerido de 05; planta, operativa, diseño y garantizada separadas |
| Cadencia de nacimientos y perfil de planta de alimento fijos sin declarar | Inputs explícitos, escenarios etiquetados |
| "CAPEX conocido / estimado" | Montos separados E1_E2 / E3 / E4 / E5 + `CALIDAD_MONTO` + cobertura por evidencia |

Sin cambios necesarios: agua (15/25/38 L/ave) y efluente reproducen 09C; kWh nunca se usó como kW; setters/hatchers, t/h, silos, plazas y flota de aves vivas ya reproducían 14B, 03 y 12B (ahora con test).

## 5. Diferencias físicas preliminares (sin juicio económico)

1. **C0 casi no tiene activos propios** (21 conceptos de oficina, IT, indirectos); su costo será OPEX (tarifa de façon, fletes).
2. **C1 → C3** pasa de 76 a 138 conceptos de la empresa: incubadora (setter y hatcher por separado), planta de alimento (2,1–16,7 t/h), flota en 7 flujos y granjas (120.000–964.000 plazas).
3. **Granjas** son, por volumen físico, el activo upstream más grande: el único precio disponible (cota de prensa) ya ubica los galpones propios en ≥ USD 1,4–11,1 M según escala.
4. **Terreno:** tres magnitudes distintas (medio): mínimo físico derivado 15.398–32.379 m² (2.500–20.000); conceptual publicado por 12C 19.868–43.660 m² (incluye una reserva proxy para crecer más allá de la escala); escenario `objetivo_20000` de 12C 33.345 m² (14.069 / 33.345 / 82.253) en cualquier escala: cubre crecer hasta 20.000 + rendering, **sin** reserva más allá de 20.000. El terreno a comprar es una **decisión** (`criterio_terreno`); hasta elegirla, su costo es provisional.
5. **Expansión:** partir de 5.000 implica reemplazar ≈ 39 equipos al llegar a 20.000 (partir de 10.000: ≈ 20), según los niveles de automatización hipotéticos de la matriz 08.

## 6. Principales datos por validar

DPV-160 (precios de línea a dos escalas y exponente), DPV-161 (USD/m² por categoría), DPV-087 (terreno), DPV-162 / DPV-093 (fletes e importación), DPV-163 (alcance de paquetes e instalación), DPV-051 (galpones con fuente oficial), DPV-086 (prima de ampliación). Capacidades reales pendientes: DPV-095, DPV-097, DPV-109.

## 7. Principales decisiones abiertas

DEC-080 (adoptar la estructura del motor), DEC-081 (lotes vs llave en mano), DEC-082 (frío y efluentes en paquete o desglosados), DEC-083 (criterio de contingencia), DEC-084 (umbral de cobertura para publicar un total), DEC-056 (titularidad de cajones). Y las existentes que el motor solo parametriza: DEC-001, DEC-002, DEC-020, DEC-024, DEC-035, DEC-049, DEC-063, DEC-074.

## 8. Próximo paso

1. Conseguir precios sin pedir cotizaciones formales todavía (constructoras, inmobiliarias, despachante, fuentes oficiales SAGyP/INTA en original) para subir obra, terreno y galpones a E2/E3.
2. Cuando la fase lo habilite (H-B), RFQ 1–5 de [`plan_cotizaciones.md`](plan_cotizaciones.md).
3. OPEX (`20_opex`) puede empezar con la misma lógica de evidencia; el optimizador de escala y arquitectura va después del modelo financiero.
