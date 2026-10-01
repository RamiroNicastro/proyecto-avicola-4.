# Conclusiones de incubación y pollito BB (sesión 14B)

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Base: [`modelo_incubacion.md`](modelo_incubacion.md), [`capacidad_incubacion.md`](capacidad_incubacion.md), [`compra_vs_incubacion.md`](compra_vs_incubacion.md), [`guia_ramiro.md`](guia_ramiro.md), [`../14_alimento_balanceado/integracion_upstream.md`](../14_alimento_balanceado/integracion_upstream.md), [`../14_alimento_balanceado/modelo_upstream.py`](../14_alimento_balanceado/modelo_upstream.py)

> **Modelo preliminar completado** (físico, 11/11 tests). **Sin decisión:** DEC-023 abierta; SUP-034 vigente (no se asume incubadora propia); reproductoras solo como fase futura. **Sin costos, sin fabricante, sin datos de campo.** Toda cifra externa `[PVDP]`.

---

## 1. Hallazgos

1. **Demanda de pollitos (medio, 5 d):** 13.197 / 26.395 / 52.790 / 105.580 pollitos por **semana plena** y 0,66 / 1,32 / 2,64 / 5,28 M pollitos/año para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas/día. El margen por mortalidad (granja + transporte) es 3,3 / **5,6** / 9,2 % sobre las aves faenadas (favorable / medio / desfavorable).
2. **Huevos (opción B, incubación media):** ~1,24 huevos recibidos por pollito vendible; 16.344 / 32.689 / 65.377 / 130.755 huevos/semana (−6 % / +11 % en los niveles favorable / desfavorable de incubación). Coincide con el rango de `03` (incubabilidad 80–85 %).
3. **Capacidad instalada (margen 15 %):** carga de 18.608 / 37.216 / 74.432 / 148.864 huevos/semana; 50.508 / 101.015 / 202.030 / 404.060 posiciones de incubadora; 10.580 / 21.160 / 42.320 / 84.640 posiciones de nacedora.
4. **La fertilidad es la variable más sensible** (0,85 → +8,2 % de huevos a 10.000) y en la opción B **depende del proveedor del huevo**, no de la empresa.
5. **Incubar huevo comprado traslada la dependencia** del pollito al huevo fértil; la independencia real solo llega con reproductoras (C), la opción más intensiva en capital, know-how y plazo.
6. **Conflicto de escala con el tamaño de lote de granja:** a 2.500 aves/día, una incubadora propia produce ~13.200 pollitos/semana, menos de la mitad de un lote de una granja de 30.000 plazas que debe llenarse en un día. A escala chica, comprar pollito a una incubadora de mayor tamaño o trabajar con granjas chicas aparecen como las alternativas físicamente compatibles (a validar; no es una decisión).
7. **Antelación física mínima** de 24–28 días entre la carga del huevo y el alojamiento; la expansión sostenida requiere ~6–7 meses (ciclo de reproductoras, `[ESTIMACIÓN]` 03).
8. **Escala relativa:** las demandas de 2.500–10.000 aves/día equivalen a una planta de incubación chica o a una fracción de una industrial (ejemplos de 80.000–400.000/semana citados, `[PVDP]`); la escala mínima eficiente **no se infiere** sin costos.

## 2. Qué opción modelar en cada fase (arquitectura, no recomendación)

| Fase | Pollito | Capacidad propia de incubación |
|---|---|---|
| 0 y 1 | **A. Compra** (≥ 2 proveedores, contratos) | 0 |
| 2 | A. Compra | 0 |
| 3 | **B. Huevo fértil + incubación** solo si el volumen y la oferta de huevo lo justifican | Según [`capacidad_incubacion.md`](capacidad_incubacion.md) |
| Futura | **C. Reproductoras** solo si existe justificación | B + reproductoras |

## 3. Datos faltantes críticos

| Dato | Registro |
|---|---|
| Oferta de pollito para terceros: volumen, mínimo por entrega, calidad, contrato | DPV-006, DPV-047 |
| Fertilidad e incubabilidad reales (por edad de reproductoras), descarte, pérdidas | DPV-14B-01, DPV-045 |
| Oferta de huevo fértil para terceros | DPV-14B-02 |
| Habilitación SENASA de planta de incubación | DPV-14B-06 |
| Capacidad de camiones de pollitos y huevos | DPV-14B-09, DPV-084 |
| Calendario de nacimientos compatible con lotes de granja | DPV-14B-10, DPV-133 |

## 4. Calidad

**MEDIA** como modelo físico (cadena cerrada, conservación probada, parámetros explícitos y editables); **BAJA** como evidencia (ningún parámetro de incubación verificado; referencias de pico de manual leídas en extractos).
