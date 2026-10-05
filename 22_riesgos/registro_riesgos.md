# Registro y matriz de riesgos

**Fecha:** 2026-10-05 · Datos: [`registro_riesgos.csv`](registro_riesgos.csv) (input) → [`matriz_riesgos.csv`](matriz_riesgos.csv) (salida) · Código: `leer_registro_riesgos()`, `matriz_riesgos()` en [`motor_riesgo.py`](motor_riesgo.py)

## 1. Campos

34 riesgos (comerciales, operativos, costos, inversión, financieros, estratégicos) con: `ID_RIESGO`, `CATEGORIA`, `RIESGO`, `DRIVER_AFECTADO` (variables del registro de variables), `PROBABILIDAD`, `METODO_PROBABILIDAD`, `FRECUENCIA_SECTORIAL_REFERENCIA`, `UNIDAD_FRECUENCIA`, `PERIODO_REFERENCIA`, `FUENTE`, `IMPACTO`, `VELOCIDAD`, `CONTROLABILIDAD`, `DETECTABILIDAD`, `INTERDEPENDENCIAS`, `MITIGACION`, `ESTADO_MITIGACION`, `PROBABILIDAD_RESIDUAL`, `IMPACTO_RESIDUAL`, `INDICADOR_ALERTA`, `UMBRAL_ALERTA` (UAD, DEC-20-04), `EVIDENCIA`, `ESTADO`, `OBSERVACIONES`.

## 2. Frecuencia sectorial ≠ probabilidad del proyecto

- `PROBABILIDAD` es la probabilidad **específica del proyecto**, en escala cualitativa. Solo puede ser BAJA / MEDIA / ALTA si `METODO_PROBABILIDAD` describe un método propio del proyecto; si no, la lectura del registro falla. **Hoy los 34 riesgos tienen `PROBABILIDAD = PENDIENTE`.**
- La frecuencia o antecedente **del sector** (p. ej. influenza aviar: eventos 2023, ago-2025 y feb-2026; maíz y soja; tipo de cambio; barreras sanitarias; conflictividad; competencia; capital de trabajo; energía; inflación) se registra aparte, en `FRECUENCIA_SECTORIAL_REFERENCIA`, con unidad, período y fuente ([`../01_mercado/mercado_avicola_argentina.md`](../01_mercado/mercado_avicola_argentina.md) §11, fuentes de sector y prensa, parte `[PVDP]`). Es la mejor referencia disponible, no una probabilidad futura: convertirla exigiría una metodología explícita (pendiente).
- La versión inicial de la sesión cargaba esas frecuencias en `PROBABILIDAD`; la auditoría las movió (anotado en `OBSERVACIONES` de cada riesgo afectado). Test AUD-06; mutación R23.
- **No se calcula riesgo esperado** (P × I): `RIESGO_ESPERADO` vacío con estado `NO_CALCULADO: no existe probabilidad específica del proyecto`.

## 3. Escala cualitativa

- BAJA / MEDIA / ALTA / PENDIENTE son **etiquetas**. No se mapean a 1/2/3 ni a probabilidades (`PROB_NUMERICA` siempre vacío; test RIE-01, AUD-07; mutación R18).
- **Impacto:** clasificación de 01 §11 cuando existe; en el resto, `[ESTIMACIÓN]` cualitativa según el bloque del motor que el driver bloquea o mueve. VELOCIDAD, CONTROLABILIDAD y DETECTABILIDAD son estimaciones cualitativas revisables (SUP-20-18).
- **Matriz:** celda `P×I` y clase por tabla 3×3 de etiquetas (BAJO / MODERADO / ALTO / CRÍTICO; SUP-20-14), sin producto numérico. Con probabilidad PENDIENTE la clase es PENDIENTE (hoy, los 34). `IMPACTO_USD` y `EXPOSICION_USD` vacíos: cuantificación futura con distribución respaldada.

## 4. Inherente vs residual

El residual solo difiere del inherente si `ESTADO_MITIGACION = IMPLEMENTADA_CON_EVIDENCIA`; una mitigación PROPUESTA o EN_CURSO deja residual = inherente. El inherente nunca se modifica (RIE-03; mutación R19). Hoy ninguna mitigación está implementada con evidencia.

## 5. Vínculo con la simulación

`SWING_VAN_SIMULADO`: cuando exista un escenario completo, la amplitud del VAN (tornado) de los drivers del riesgo se agrega como referencia **simulada** (no es probabilidad ni impacto observado).
