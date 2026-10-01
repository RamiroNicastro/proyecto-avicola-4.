# Conclusiones de alimento balanceado e integración upstream (sesión 14B)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Base: [`integracion_upstream.md`](integracion_upstream.md), [`demanda_alimento.md`](demanda_alimento.md), [`planta_alimento_conceptual.md`](planta_alimento_conceptual.md), [`almacenamiento_silos.md`](almacenamiento_silos.md), [`compra_vs_fabricacion.md`](compra_vs_fabricacion.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_upstream.py`](modelo_upstream.py), [`escenarios_upstream.csv`](escenarios_upstream.csv). Incubación: [`../15_incubacion/conclusiones_incubacion.md`](../15_incubacion/conclusiones_incubacion.md).

> **MODELO PRELIMINAR COMPLETADO** (físico; 11/11 tests). **Sin decisión de integración:** DEC-020, DEC-023 y DEC-024 siguen abiertas. **Sin CAPEX/OPEX, sin precios, sin fabricante, sin datos de campo.** Toda cifra externa `[PVDP]` (DPV-009).

---

## 1. Hallazgos

1. **El alimento es el mayor flujo físico del sistema:** 8,8 / 17,7 / 35,3 / 70,6 t/día de entrega y 3.091 / 6.181 / 12.362 / 24.724 t/año (medio, 5 d) para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas/día. Escala **linealmente** con la faena (test U03); lo único no lineal son los viajes enteros (3 / 5 / 9 / 18 entregas de 28 t por semana).
2. **Maíz + harina de soja ≈ 85–95 % del tonelaje** (punto ilustrativo: ~1.850–14.800 t/año de maíz y ~930–7.400 t/año de harina de soja). Aceite, minerales, vitaminas y otros pesan poco en t pero concentran exigencias de dosificación, importación y control. **No hay fórmula**: eso es del nutricionista.
3. **Una planta propia requeriría ~1 a ~25 t/h** de alimento terminado según escala, turnos y desempeño; los turnos mueven la capacidad tanto como duplicar la escala. A 2.500 aves/día, ~1–2,4 t/h: una planta propia estaría mayormente ociosa.
4. **El almacenamiento depende de decisiones, no solo de la escala:** con los mismos consumos, los días de stock mueven los m³ de la planta más de 3 veces (432 → 1.472 m³ a 10.000 aves/día). No existe "silo estándar"; el número de silos queda PENDIENTE hasta fijar volumen unitario. Hay un mínimo de 5–8 celdas por segregación que **no escala**.
5. **Façon** es la forma de controlar fórmula y compra de granos sin CAPEX de planta, pero introduce stock y logística de granos propios (~119–954 t a 15 días) y depende de que exista un elaborador dispuesto.
6. **La demanda física es idéntica en compra, integración parcial o total** (test U05): la decisión de integrar no cambia cuántos pollitos ni cuánto alimento hacen falta, sino qué capacidad física, capital, know-how y riesgo asume la empresa.
7. **Integrar pollito incubando huevo comprado traslada la dependencia**, no la elimina ([`../15_incubacion/compra_vs_incubacion.md`](../15_incubacion/compra_vs_incubacion.md)).
8. **Las decisiones están acopladas operativamente:** integrar granjas obliga a proveer pollito y alimento; comprar pollo vivo vuelve irrelevantes las otras dos.

## 2. Qué conviene **modelar** como compra, integración parcial o total (para la fase económica)

> Es una propuesta de **qué escenarios llevar al modelo económico**, no una recomendación de integración (regla 10; DEC-14B-01).

| Eslabón | Modelar como caso base | Modelar como alternativa | Modelar solo como sensibilidad / fase futura | Capacidad física a modelar |
|---|---|---|---|---|
| **Pollito BB** | **Compra** (todas las escalas) | Huevo fértil + incubación (10.000–20.000, si hay oferta de huevo) | Reproductoras (fase futura) | B: 74.000–149.000 huevos/semana de carga (10.000–20.000) |
| **Alimento** | **Compra** (escalas chicas) y **façon** | **Planta propia** (desde la escala en que un turno quede razonablemente lleno — umbral PENDIENTE) | — | C: 1–25 t/h + silos según días de stock |
| **Granjas** | **Integrados** (+ pollo vivo como amortiguador) | Granjas propias modelo / mixto | 100 % propias | Plazas y m² de `03` (9.500–75.900 m² medio) |

## 3. Fases (arquitectura conceptual, NO secuencia recomendada)

Fase 0: compra de pollito + alimento + granjas de terceros + faena a façon posible → Fase 1: planta propia con upstream comprado o parcialmente integrado → Fase 2: más granjas e integración → Fase 3: alimento y/o incubación si el volumen lo justifica → Fase futura: reproductoras/genética solo con justificación. Detalle y gates conceptuales: [`integracion_upstream.md` §3](integracion_upstream.md).

## 4. Datos faltantes principales

| Dato | Registro |
|---|---|
| Precio y condiciones del alimento por fase puesto en granja | DPV-050 |
| Fábricas con capacidad libre y disposición a façon; lote mínimo; tarifa | DPV-14B-03 |
| Proveedores de grano: volumen anual, calidad, contratos, estacionalidad | DPV-14B-05, DPV-117 |
| Capacidad real, eficiencia, energía y dotación de plantas de alimento en operación | DPV-14B-07 |
| Densidades aparentes y días de stock usados en Argentina; silos de granja | DPV-14B-04 |
| Registro SENASA de fábricas de alimento y medicados | DPV-14B-06 |
| Condiciones que ofrecerían integradores existentes a un tercero | DPV-14B-08 |
| Capacidad útil de graneleros y camiones de grano | DPV-084 |
| Costo del pollo vivo y peso del alimento en él | DPV-019 |

## 5. Tests (11/11 correctos)

| Test | Qué valida |
|---|---|
| U01 | Conservación de pollitos y huevos (hacia adelante recupera la demanda; cadena estrictamente decreciente) |
| U02 | Capacidad instalada ≥ requerida (incubadora, nacedora, almacén de huevo, planta de alimento) |
| U03 | Alimento lineal con la escala; viajes enteros no lineales por redondeo (explicado y acotado) |
| U04 | Silos ∝ días de stock, ∝ 1/densidad, 0 sin stock; n.º de silos PENDIENTE sin volumen unitario |
| U05 | Compra / integración parcial / total calculadas por separado, con la misma demanda física |
| U06 | Faltantes quedan PENDIENTES con valor vacío (240 filas del CSV); parámetros inválidos se rechazan |
| U07 | Reproductoras = 0 en Fase 0 y 1; solo en la fase futura |
| U08 | Sin precios ni variables económicas en el CSV |
| U09 | Pollitos y alimento idénticos a `03` (importado, no recalculado) |
| U10 | Monotonía: peor incubación → más huevos; más margen → más capacidad; más mortalidad → más pollitos |
| U11 | Toda variable tiene unidad válida |

## 6. Calidad

**MEDIA** como marco y modelo físico reproducible; **BAJA** como evidencia para decidir integrar (sin oferta, precios ni capacidades reales relevadas). Ningún parámetro de planta, silos o incubación está verificado.
