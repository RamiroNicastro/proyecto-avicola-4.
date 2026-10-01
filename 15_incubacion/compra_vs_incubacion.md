# Pollito BB: compra vs incubación propia vs reproductoras

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de sincronización) · Sesión 14B · Marco general y criterios del upstream: [`../14_alimento_balanceado/integracion_upstream.md` §2](../14_alimento_balanceado/integracion_upstream.md)

> **Sin decisión y sin costos.** DEC-023 (estrategia de pollito BB) sigue **abierta**; SUP-034 (no se asume incubadora propia) sigue **vigente**. Las tres opciones son **escenarios de comparación** con el mismo estatus; la compra de pollito es solo el **benchmark de comparación** (punto contra el que se miden las demás), no una preferencia. Las reproductoras no se suponen en las arquitecturas de referencia 0 y 1 (test U07); son una opción de la arquitectura futura condicionada a una justificación.

---

## 1. Las tres opciones

| | **A. Comprar pollitos** | **B. Incubar huevo fértil comprado** | **C. Reproductoras propias** (arquitectura futura) |
|---|---|---|---|
| Qué compra la empresa | Pollito BB vacunado, puesto en granja | Huevo fértil | Pollitas reproductoras de un día (o abuelas) y su alimento |
| Qué capacidad física propia necesita | Ninguna (recepción en granja) | Planta de incubación: almacén de huevo, incubadoras, nacedoras, sala de pollitos, vacunación, expedición, camiones climatizados ([`capacidad_incubacion.md`](capacidad_incubacion.md)) | Todo lo de B + granjas de recría y de reproductoras (~3.700–29.300 hembras en postura equivalentes, sin recría ni machos) |
| De quién depende | Incubadoras que venden a terceros | **Vendedores de huevo fértil** (reproductoras de terceros) | Empresas de genética |
| Plazo para ampliar | El del proveedor (ciclo de reproductoras: ~6–7 meses, `[ESTIMACIÓN]` 03, DPV-045) | Igual que A para el huevo; más la obra de incubación | ~6–7 meses + plazo de pedido de genética + granjas de reproductoras |
| Huevos o pollitos/semana (medio, 5 d) | 13.197 / 26.395 / 52.790 / 105.580 pollitos | 16.344 / 32.689 / 65.377 / 130.755 huevos | Mismos huevos, producidos por las reproductoras propias |

## 2. Comparación por criterio

| Criterio | A. Comprar pollitos | B. Incubar huevo comprado | C. Reproductoras |
|---|---|---|---|
| **Volumen** | Sirve a cualquier escala si hay oferta; el **lote de nacimiento** lo fija el proveedor (PENDIENTE) | Necesita volumen estable; el **lote de nacimiento** = demanda / cadencia y puede ser menor que la unidad de colocación (galpón o granja): posible problema de sincronización a validar ([`capacidad_incubacion.md` §4](capacidad_incubacion.md)) | Necesita volumen y horizonte largos |
| **Calidad** | Por contrato: peso, uniformidad, mortalidad 7 d, vacunas | Control del proceso de incubación; **la fertilidad y la calidad del huevo siguen dependiendo del proveedor** | Control completo |
| **Dependencia** | Alta (oferta concentrada; integradoras se autoabastecen) | **Se sustituye** la dependencia de proveedores de pollito por dependencia de proveedores de huevo fértil; la concentración y disponibilidad real de esa oferta es **DPV-14B-02** (sin evidencia) | Solo de la genética |
| **Capital** | Nulo | Planta de incubación + equipos + capital de trabajo en huevo | B + granjas de recría y reproductoras + alimento de reproductoras |
| **Flexibilidad** | Alta (si hay oferta) | Baja: capacidad fija; ociosa si la faena no la llena | Muy baja (ciclos de ~1 año de los lotes de reproductoras) |
| **Bioseguridad** | Riesgo compartido con los otros clientes del proveedor | Controlada en la planta; el huevo sigue siendo una entrada de riesgo | Máxima posible (compatible con compartimentos, Res. 484/2017, FTE-149 `[PVDP]`) |
| **Know-how** | Compras y control de recepción | Incubación, sanidad del huevo, vacunación, mantenimiento de equipos | Manejo de reproductoras (iluminación, restricción alimentaria, sanidad) |
| **Riesgo de suministro** | El cliente chico queda último ante escasez | Ídem para el huevo fértil | Menor, pero un evento sanitario en reproductoras corta todo |
| **Capacidad ociosa** | Ninguna | Alta en la rampa | Muy alta en la rampa |

## 3. Lectura crítica

1. **B sustituye una dependencia por otra y agrega control del proceso de incubación.** Incubar huevo fértil comprado sustituye la dependencia de proveedores de pollito por dependencia de proveedores de huevo fértil; **la concentración y disponibilidad real de esa oferta es un dato por validar** (DPV-14B-02, pregunta E5 del [cuestionario](cuestionario_incubadoras.md)). No hay evidencia de que haya más o menos vendedores de huevo que de pollito.
2. **El argumento para B es más de calidad, programación y costo que de seguridad de suministro**, y ninguno de los tres puede evaluarse sin datos de campo (calidad del pollito comprado vs propio, precio pollito vs huevo + costo de incubar).
3. **Posible problema de sincronización a escala chica:** a 2.500–5.000 aves/día la planta de incubación sería pequeña frente a los ejemplos citados (80.000–400.000 por semana, FTE-14B-004 `[PVDP]`) y sus lotes de nacimiento (≈ 2.600–26.400 pollitos según cadencia) pueden ser menores que la unidad de colocación (un galpón de ~15.000–30.000 plazas equivalentes). Eso **no demuestra incompatibilidad**: depende de la arquitectura real de las granjas (galpones por granja, plazas por galpón, tolerancia de edad en un mismo lote) y debe validarse ([`../14_alimento_balanceado/integracion_upstream.md` §4](../14_alimento_balanceado/integracion_upstream.md)).
4. **C es una decisión de otra naturaleza** (negocio de genética/reproductoras) y **no se supone en las arquitecturas de referencia 0 y 1**.
5. **Mitigaciones dentro de A** (sin integrar): contratos anuales con volumen asegurado, **al menos dos proveedores**, especificaciones con reposición, seguimiento de la 1.ª semana por proveedor ([`../03_produccion_primaria/modelos_integracion.md` §4.4](../03_produccion_primaria/modelos_integracion.md)), y posibilidad contractual de compra de huevo fértil como respaldo.

## 4. Qué haría falta para pasar de A a B (señales, sin umbrales)

- Oferta de huevo fértil para terceros, escrita, de ≥ 2 proveedores (DPV-14B-02).
- Volumen de faena estable que llene la planta de incubación en el tamaño evaluado, con una cadencia de nacimientos compatible con galpones y faena (chequeo de sincronización).
- Evidencia de que el pollito comprado tiene problemas de calidad, programación o disponibilidad que la incubación propia resolvería.
- Comparación económica: precio del pollito vs (huevo + incubación + capital) — **fase posterior**.
- Habilitación SENASA y sitio con distancias de bioseguridad (DPV-14B-06).

**Umbral de volumen para B o C: PENDIENTE** (DEC-14B-01).
