# Costos de calidad, laboratorio, SENASA y módulo halal

**Fecha:** 2026-10-02 · Implementación: §CALIDAD de `generar_registro()` en [`modelo_opex.py`](modelo_opex.py)

## 1. Conceptos

| Concepto | ID | Cantidad | Estado |
|---|---|---|---|
| Análisis microbiológicos (laboratorio externo) | CAL-ANA-MICRO | análisis/año | PENDIENTE_CANTIDAD: plan de muestreo PENDIENTE (DPV-17-12) |
| Análisis de agua de proceso | CAL-ANA-AGUA | análisis/año | PENDIENTE_CANTIDAD (solo planta propia) |
| Insumos de laboratorio propio | CAL-LAB-INS | 1 año | Sin precio (solo con laboratorio propio; el equipamiento está en CAPEX) |
| Certificaciones | CAL-CERT | 1 año | Sin precio |
| Auditorías | CAL-AUD | 1 año | Sin precio |
| Documentación | CAL-DOC | 1 año | Sin precio |
| Trazabilidad (software) | CAL-TRAZ | 12 meses | Sin precio |
| Tasas y aranceles SENASA | CAL-SENASA | — | **PENDIENTE_CANTIDAD**: no se inventa el costo de inspección; estructura (por ave, por kg, fija) y montos PENDIENTES (DPV-101) |
| Análisis de alimento (planta propia) | ALI-C-ANA | — | PENDIENTE_CANTIDAD |
| Análisis de vuelco | EF-ANA | — | PENDIENTE_CANTIDAD |

El **personal** de calidad (QC, jefe de calidad, APPCC, trazabilidad, analistas de laboratorio propio, control de calidad en el façon) está en costo laboral (14A). La inspección oficial está fuera de la empresa en 14A; su eventual costo para el establecimiento es CAL-SENASA. Con laboratorio externo, el puesto de 14A remite a CAL-ANA-MICRO (sin doble conteo).

## 2. Halal / exportación — módulo opcional de mercado

No se desarrolla el módulo. Con `modulo_halal = True` el registro agrega la estructura (certificación, auditoría, supervisión/degolladores, segregación, documentación, etiquetado, logística, análisis) con `FASE = OPCIONAL_MERCADO`, **sin costos** (no hay evidencia) y contando como conceptos pendientes de ese escenario (variante `C1-10000-HALAL`: 8 conceptos más). Sin activar, no aparece (test A09). Requisitos y organismos: `17_exportacion/` (FTE-245 [PVDP]).
