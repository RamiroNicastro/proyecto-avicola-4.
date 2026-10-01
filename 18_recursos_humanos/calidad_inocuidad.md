# Calidad e inocuidad — funciones y dotación

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 14A) · Fase 0

> **Alcance:** qué funciones de calidad e inocuidad necesita la empresa, quién las hace y cuánta gente implican por escala. Separa control operativo, QA, inocuidad, trazabilidad, APPCC y documentación.
> **Regla:** **no** se afirma una cantidad obligatoria de profesionales sin respaldo normativo leído. Ninguna norma pudo leerse en su original desde la sesión (DPV-009); las referencias normativas son `[PVDP]` y vienen de [`../16_normativa_senasa/`](../16_normativa_senasa/README.md).
> **Clasificación:** cantidades `[ESTIMACIÓN]` de [`modelo_rrhh.py`](modelo_rrhh.py) con coeficientes `[SUPUESTO]` (SUP-14A-08, SUP-14A-13).

---

## 1. Qué exige la norma (según 09B, todo `[PVDP]`) y qué no dice

| Tema | Lo que se sabe | Lo que **no** se sabe (y por eso no se fija dotación) |
|---|---|---|
| BPM y POES | Obligatorios (Res. SENASA 233/1998): procedimientos escritos con responsables, frecuencias, verificación y acciones correctivas | Cantidad ni perfil del personal que los ejecuta y verifica |
| Plan APPCC | Obligatorio para establecimientos SENASA que faenen, elaboren, fraccionen o depositen alimentos, salvo excepciones (Res. SENASA 205/2014, cap. XXXI del Decreto 4238/68) | Si exige un responsable con título o dedicación específicos |
| Director Técnico | **Obligación reglamentaria derogada** por Res. SENASA 592/2026 (FTE-229) | Si clientes, destinos o la autoridad local exigen igualmente un profesional responsable |
| Inspección oficial | Ante y post mortem, decomisos y dictamen a cargo del servicio veterinario oficial | Inspectores y auxiliares por velocidad de línea; si la empresa aporta auxiliares o paga aranceles (DPV-090, DPV-14A-05) |
| Exportación | Requisitos adicionales del destino sobre APPCC, microbiología, bienestar, trazabilidad por lote | Por destino; p. ej., la UE exige un responsable de bienestar animal en mataderos de su territorio (Reg. CE 1099/2009, `[PVDP]`, FTE-14A-007) — su aplicación a plantas de terceros países exportadoras está por verificar (DPV-14A-12) |

**Consecuencia:** las cantidades de abajo son **organizacionales** (lo necesario para que las funciones se cumplan con orden de magnitud razonable), no requisitos legales.

## 2. Seis funciones distintas

| Función | Qué hace | Dónde | Frecuencia | Perfil | Modalidad |
|---|---|---|---|---|---|
| **Control operativo** | Controles en recepción (lote, DOA, temperatura), línea (contaminación visible, temperatura de chiller, absorción), empaque (peso, rotulado, detector de metales), cámaras; registro de PCC | Planta, por turno | Continua | Técnico/a de calidad o operario/a capacitado/a | Interno, por cuadrilla |
| **QA (aseguramiento)** | Especificaciones de producto, liberación de lotes, reclamos, auditorías internas y de clientes, proveedores de insumos | Oficina + planta | Diaria/semanal | Profesional (ingeniería de alimentos, veterinaria, bromatología u otra) | Interno |
| **Inocuidad** | Peligros microbiológicos (*Salmonella*, *Campylobacter*), químicos (residuos, CREHA) y físicos; plan de muestreo; verificación de POES | Oficina + laboratorio | Plan anual + diario | Profesional | Interno (jefe de calidad) |
| **Trazabilidad** | Lote de granja ↔ lote de faena ↔ producto ↔ cliente; simulacros de retiro | Oficina + sistemas | Por lote | Administrativo/a técnico/a | Interno o compartido |
| **APPCC** | Diseño, validación, verificación y revisión del plan; registros de PCC | Oficina | Continua + revisión periódica | Profesional formado en APPCC | Interno |
| **Documentación** | Control de documentos y registros (BPM, POES, APPCC, capacitaciones, calibraciones) para SENASA, clientes y auditores | Oficina | Continua | Administrativo/a técnico/a | Interno o compartido |
| *Laboratorio* | Análisis de autocontrol | Laboratorio | Plan de muestreo | Analista | **Externo** como base; propio como opción (DEC-065) |

## 3. Dotación por escala (escenario de referencia, productividad media)

| Rol | 2.500 | 5.000 | 10.000 | 20.000 | Base |
|---|---|---|---|---|---|
| Control de calidad operativo (puestos por turno · personas) | 2 · 3 | 2 · 3 | 2 · 3 | 3 · 4 | 1 + 0,6 / 0,8 / 1,2 por 1.000 aves/h, por cuadrilla |
| Jefe de calidad e inocuidad | 1 | 1 | 1 | 1 | Estructura |
| Analista APPCC / documentación | 0,5 (compartido) | 1 | 1 | 2 | Estructura |
| Trazabilidad y registros | — (jefe) | 0,5 | 1 | 1 | Estructura |
| Gerente de calidad e inocuidad | — | — | — | 1 | Estructura |
| Laboratorio propio (opción, no base) | 1 | 1 | 2 | 3 | DEC-065 |
| **Total calidad (base, equivalentes)** | **~4** | **~5** | **~6** | **~9** | |

Con dos cuadrillas el control operativo se duplica. En asset-light la empresa conserva el jefe de calidad y 1–2 controladores propios en la planta del façonier ([`dotacion_por_escala.md`](dotacion_por_escala.md) §6).

## 4. Principios organizacionales

1. **Independencia:** calidad no reporta a producción. En escalas chicas reporta al gerente general; en la escalada es gerencia.
2. **El control operativo es por turno, la estructura de QA no:** un segundo turno duplica controladores, no analistas APPCC.
3. **Exportación agrega trabajo de documentación y auditoría,** no necesariamente controladores de línea: el salto llega con la primera habilitación de destino (lotes segregados, auditorías, certificados), no con las aves/día.
4. **Halal** (si se valida, DPV-034) puede exigir personal específico para el sacrificio y supervisión de la entidad certificadora: no modelado.
5. **El laboratorio propio** aporta velocidad de resultado y control; el externo, acreditación e independencia. Se compara cuando haya volumen de muestras y precios (DEC-065).
