# Respaldo eléctrico y cargas críticas (conceptual)

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** identificar cargas críticas, ordenar de qué protege el respaldo y mostrar una **carga crítica ilustrativa de escenario** (proxy preliminar de sensibilidad). **No se dimensiona el grupo electrógeno** (queda PENDIENTE de una lista de cargas críticas), ni marca ni modelo, no se elige arquitectura de redundancia ni se calcula CAPEX.
> **Modelo:** [`../11_agua_efluentes/modelo_utilities.py`](../11_agua_efluentes/modelo_utilities.py) v1.1 (bloque `respaldo`); todas las fracciones son `[SUPUESTO]`.

---

## 1. Por qué importa

- Un corte de energía en una planta de faena no es solo producción perdida: hay **aves vivas esperando** en el andén (bienestar y mortalidad), **producto a medio proceso** (carcasas en escaldador, eviscerado o chiller que deben terminar su enfriamiento), **stock en cámaras** (pérdida total si se rompe la cadena de frío) y **efluentes** (el biológico puede morir o desbordar, con consecuencias ambientales).
- Hay antecedentes en Argentina de **mortandad masiva de pollos por fallas eléctricas en granjas** (FTE-157 `[PVDP]`, prensa): el riesgo es real en zonas rurales con redes débiles (DPV-052).
- Una cámara de congelado bien aislada puede mantener temperatura bajo cero **4–8 h** tras la falla del frío (FTE-09C-17 `[PVDP · débil]`, fuente comercial); una cámara refrigerada y el producto fresco toleran mucho menos. Esa inercia define cuánto tiempo hay para arrancar el respaldo, no si hace falta.
- Destinos de exportación auditan la **integridad de la cadena de frío** y los registros de temperatura ([`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md) §3: "energía de respaldo para frío").

## 2. Cargas críticas

| Carga | Por qué es crítica | Tolerancia a un corte | Prioridad | Estimación en el modelo |
|---|---|---|---|---|
| **Ventilación y seguridad de aves** en el andén de espera | Bienestar animal; calor en verano con aves apiladas en módulos | **Minutos** en verano | 1 | 3 % de la potencia media equivalente de proceso `[SUPUESTO]` |
| **Frío de cámaras** (refrigerado y congelado) | Pérdida del stock; ruptura de cadena de frío | Horas (congelado 4–8 h; refrigerado menos) | 1 | kWh ilustrativos de almacenamiento ÷ 24 × factor de rearranque 1,3 / **1,5** / 2,0 `[SUPUESTO]` |
| **Sistemas de control, seguridad y comunicaciones** (PLC, registros de temperatura, detección de amoníaco, alarmas, CCTV) | Seguridad de personas (fugas de refrigerante), trazabilidad de temperatura | Segundos (UPS) | 1 | 3 % de la potencia media de proceso `[SUPUESTO]` |
| **Iluminación de emergencia** y salidas | Evacuación | Inmediata (baterías) | 1 | 1,5 % `[SUPUESTO]` |
| **Bombeo mínimo de agua** | Incendio, sanitización mínima, enfriado de emergencia | Minutos–horas | 2 | 4,5 % `[SUPUESTO]` |
| **Efluentes** (aireación mínima, bombas de elevación, ecualización) | Evitar desbordes y la muerte del biológico | Horas | 2 | 50 % de la potencia media de aireación `[SUPUESTO]` |
| **Línea de faena** (terminar las aves en proceso) | Producto en escaldador/eviscerado/chiller; aves colgadas | Minutos | 3 (decisión) | No estimado |
| **Túneles de congelado** | Terminar el ciclo de congelado en curso | Horas | 3 | No estimado |
| Oficinas, climatización de confort | — | Alta | 4 | No |

## 3. Carga crítica ilustrativa de escenario

`[SUPUESTO]` **proxy preliminar de sensibilidad**. En la v1.0 se expresaba en kVA como porcentaje de un "pico" de planta; ese pico se retiró (no surge de kWh/ave) y el proxy se basa ahora en la **potencia media equivalente** de proceso y en la energía ilustrativa de cámaras. Bajo · **medio** · alto, kW.

| Escala | Carga crítica ilustrativa (P1) | Carga crítica ilustrativa P2 · P3 (medio) | Grupo electrógeno |
|---|---|---|---|
| 2.500 | 11 · **20** · 40 | 24 · 26 | **PENDIENTE** |
| 5.000 | 22 · **40** · 81 | 48 · 51 | **PENDIENTE** |
| 10.000 | 43 · **79** · 162 | 97 · 102 | **PENDIENTE** |
| 20.000 | 86 · **158** · 323 | 193 · 205 | **PENDIENTE** |

Desglose a 10.000 aves/día (medio, P1): cámaras 10 kW, efluentes 7 kW, control 16 kW, iluminación de emergencia 8 kW, bombeo de agua 23 kW, andén de aves 16 kW → ~79 kW.

**No se concluye que un grupo de 25 / 49 / 99 / 198 kVA (cifras de la v1.0) sea el generador necesario.** El modelo deja `grupo_electrogeno_kva` vacío salvo que se cargue una lista de cargas críticas; nunca lo calcula como porcentaje fijo de la planta (test **U25**, mutación M18).

**El dimensionamiento real deberá considerar:** listado de cargas críticas; kW y kVA; factor de potencia; corriente de arranque; motores y compresores (el mayor arranque suele mandar); secuencia de arranque; simultaneidad; autonomía; combustible; redundancia (N+1); posibilidad de **mantener el frío sin mantener la faena**; black-start cuando corresponda. Esa lista saldrá del catálogo de equipos de la sesión 09A (en `main`) y de las cotizaciones ([`demanda_energia.md` §6](demanda_energia.md)).

**Lecturas:**
1. La decisión real es **qué se quiere seguir haciendo durante un corte** (DEC-09C-05 propuesta): solo cargas críticas, terminar el lote en proceso o planta completa.
2. Con más congelado (P2/P3) y más días de stock crece la carga crítica de cámaras.
3. Las fracciones son supuestos; el cálculo real requiere el listado de cargas del proyecto eléctrico.

## 4. Conceptos de generación y redundancia

| Concepto | Qué significa | Cuándo aplica (a evaluar) |
|---|---|---|
| **UPS** (baterías) | Energía inmediata, minutos | Control, registros, detección de gases, comunicaciones |
| **Grupo electrógeno** (diésel o gas) | Arranca en segundos–minutos; autonomía según tanque | Cargas críticas o planta completa |
| **Transferencia automática** | Conmuta red ↔ generador sin intervención | Siempre que haya cargas de prioridad 1 |
| **N+1** | Un equipo más de los necesarios (dos generadores al 100 %, o tres al 50 %) | Si la red del sitio es poco confiable o si se sostiene la línea |
| **Separación de tableros por prioridad** | Circuitos críticos alimentables por el generador; el resto se desconecta | Permite un generador chico para lo crítico |
| **Autonomía de combustible** | Horas/días de operación sin reabastecer | Zonas rurales con caminos que se cortan |
| **Segunda alimentación** de la red (otra línea/subestación) | Redundancia de red | Escalas mayores; depende de la distribuidora |
| **Inercia térmica** | Cámaras bien aisladas, cortinas de aire, no abrir puertas durante cortes | Reduce la potencia de respaldo necesaria para el frío |
| Generación propia (biogás, solar) | Complemento, no respaldo firme | Evaluación posterior |

**Relación con la localización:** la calidad de la red (frecuencia y duración de cortes, caídas de tensión) es un criterio de localización (DPV-052, DPV-087). Un sitio con red débil empuja a más respaldo y a N+1; un sitio con red robusta, a respaldo solo de cargas críticas.
