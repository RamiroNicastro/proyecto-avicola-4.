# Logística de exportación — modelo físico y datos para cotizar

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría de interpretación) · Sesión 12B · Fase 0

> **Alcance:** cadena física **planta → depósito/consolidación → puerto → contenedor reefer → buque**, separada en etapas, con toneladas, contenedores, frecuencia y tiempos por escala; y la **lista de datos** que hace falta para pedir cotizaciones. Puertos, documentos, seguros y ciclo de caja ya están en [`../17_exportacion/logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md) y **no se repiten**.
> **No** hay fletes, tarifas ni costos portuarios (DPV-027). La exportación **no es demanda**: es 0 en todos los escenarios comerciales (SUP-022); aquí se usa una **cuota de barrido** (10 / 20 / 50 % del comestible; P3 = 20 %) para dimensionar físicamente la opción. País abierto ≠ planta habilitada ≠ producto autorizado ≠ comprador (regla 17).
> Cifras: bloques `exportacion` y `exportacion_ruta` de [`escenarios_logistica.csv`](escenarios_logistica.csv).

---

## 1. Cadena y etapas

```
Planta: faena → empaque → CONGELADO (túnel; el reefer mantiene, no congela) → cámara
   │  [consolidación: días hasta completar un contenedor por producto/destino]
   ▼
Carga del reefer (en planta o en frigorífico/depósito de consolidación; precinto, registrador)
   │  [TRANSPORTE TERRESTRE: camión portacontenedor con genset]
   ▼
Terminal portuaria (conexión reefer; espera de buque; inspección)
   │  [ESPERA EN TERMINAL: PENDIENTE]
   ▼
Buque (tránsito marítimo; posibles trasbordos)  [MARÍTIMO: 20–45 d, PVDP débil]
   ▼
Puerto de destino → inspección sanitaria y aduana → importador
```

| Etapa | Qué determina su duración | Valor en el modelo | Estado |
|---|---|---|---|
| **Consolidación** | t exportadas por día × carga del contenedor | Días de faena = 25 t / t exportadas por día operativo | `[ESTIMACIÓN]`; carga 25 t `[PVDP · débil]` FTE-135 |
| **Transporte terrestre** | Distancia planta–puerto (12A) | h = km / 70 km/h (barrido 30 / 150 / 300 / 600 / 1.000 km → 0,4 / 2,1 / 4,3 / 8,6 / 14,3 h) | `[SUPUESTO]` SUP-091/094 |
| **Espera** (en planta antes de la carga y en terminal) | Frecuencia de buques por destino, *cut-off*, inspección | **PENDIENTE** | DPV-027, DPV-125 |
| **Terminal** | Operación del puerto, disponibilidad de conexiones reefer | **PENDIENTE** | DPV-027 |
| **Marítimo** | Ruta y trasbordos | 20–45 días (referencia brasileña y ruta inversa) | `[PVDP · débil]` (17 §4) |

El **lead time total** (faena → arribo) queda **PENDIENTE** en el modelo porque falta la espera en terminal: no se completa con un valor por defecto (test L13).

## 2. SENSIBILIDAD: toneladas, contenedores y frecuencia por escala

**Esto es una sensibilidad física, no una estrategia comercial prevista.** El porcentaje exportado es un parámetro de barrido (10 / 20 / 50 % del comestible); el 20 % coincide con el perfil ilustrativo P3 de `23` pero **no** es un objetivo. La demanda de exportación del proyecto es 0 (SUP-022). Supuestos explícitos de cada fila: **payload = 25 t por contenedor reefer 40'** (capacidad de escenario, `[PVDP · débil]` FTE-135, rango citado 24–27 t), 5 días de faena por semana (250 días/año), configuración B, un solo producto/destino.

| Escala | % exportado (sensibilidad) | t exportadas/día operativo | Payload asumido | Días de faena (producción) para 1 contenedor | Días calendario | Contenedores/mes | Contenedores/año | Utilización del payload |
|---|---|---|---|---|---|---|---|---|
| 2.500 | 10 · 20 · 50 % | 0,60 · 1,20 · 3,00 | 25 t | 41,7 · 20,9 · 8,3 | 60,9 · 30,5 · 12,2 | 0,5 · 1,0 · 2,5 | 6 · 12 · 30 | ~100 % |
| 5.000 | 10 · 20 · 50 % | 1,20 · 2,40 · 5,99 | 25 t | 20,9 · 10,4 · 4,2 | 30,5 · 15,2 · 6,1 | 1,0 · 2,0 · 5,0 | 12 · 24 · 60 | ~100 % |
| 10.000 | 10 · 20 · 50 % | 2,40 · 4,79 · 11,98 | 25 t | 10,4 · 5,2 · 2,1 | 15,2 · 7,6 · 3,0 | 2,0 · 4,0 · 10,0 | 24 · 48 · 120 | ~100 % |
| 20.000 | 10 · 20 · 50 % | 4,79 · 9,59 · 23,96 | 25 t | 5,2 · 2,6 · 1,0 | 7,6 · 3,8 · 1,5 | 4,0 · 8,0 · 20,0 | 48 · 96 · 240 | ~100 % |

**Utilización del payload** = t exportadas/año ÷ (contenedores enteros × 25 t). Es ~100 % **por construcción**, porque el modelo espera a completar cada contenedor: el costo físico de llenarlo no aparece como camión vacío sino como **días de consolidación y stock congelado**. Si el comprador exigiera embarques en fecha fija con menos de 25 t, la utilización bajaría (dato del comprador, DPV-032).

Estas cifras suponen **un solo producto/destino** con toda la cuota. Para partes específicas (garras, menudencias, pata-muslo) el tiempo de llenado por parte ya está en [`../23_plan_expansion/escenarios_escala.md` §13](../23_plan_expansion/escenarios_escala.md) (p. ej. garras grado A: ~118 días de faena a 2.500 aves/día). Cada producto/destino en consolidación inmoviliza hasta ~1 contenedor (25 t) en cámara de congelado: con 3 lotes en paralelo, ~75 t.

**Transporte terrestre:** 1 contenedor por camión portacontenedor (`[SUPUESTO]` SUP-104, a validar) → viajes terrestres/año = contenedores/año. km/año = 2 × contenedores × distancia (el portacontenedor vuelve con el contenedor vacío o sin carga: backhaul **REQUIERE_EVIDENCIA**).

**Lecturas:**
1. En la sensibilidad, **a 2.500 aves/día con 20 % exportado sale un contenedor por mes** (con 25 t de payload): embarques más frecuentes requerirían porcentajes mayores o consolidar con un trader (DPV-081). No es una proyección de ventas.
2. Con 600–1.000 km a puerto, el tramo terrestre (8,6–14,3 h) excede la jornada de un chofer (CCT 40/89, FTE-287 `[PVDP]`): relevo o pernocte con genset encendido.
3. La exportación **suma congelado y cámara**, no camiones refrigerados diarios: su logística se parece a la del congelado acumulable ([`logistica_producto_terminado.md` §3](logistica_producto_terminado.md)).

## 3. Datos requeridos para una futura cotización (plantilla)

Completar uno por combinación producto–destino. Los campos marcados ★ dependen de decisiones abiertas.

| Campo | Contenido | Hoy | Fuente / registro |
|---|---|---|---|
| **Origen** ★ | Localidad de la planta o del depósito de consolidación; dónde se carga el contenedor | **PENDIENTE** (12A, DEC-003) | — |
| **Puerto de embarque** | Buenos Aires / Dock Sud / Zárate / otro | Sin elegir (17 §3) | DPV-027 |
| **Destino** ★ | País y puerto; categoría A/B/C/D (regla 17) | Sin comprador; China fuera del caso base (SUP-016) | `17_exportacion/mercados_por_pais.md` |
| **Incoterm** | FOB / CFR / CIF (define quién contrata flete y seguro) | Sin definir | DPV-032 |
| **Equipo** | Reefer 40' (o 40' HC / 20'); con genset para el tramo terrestre | 40' como referencia | FTE-135 `[PVDP · débil]` |
| **Tonelaje por contenedor** | Neto de producto, según empaque y paletizado | 24–27 t (referencia 25 t) | FTE-135 `[PVDP · débil]` |
| **Producto y empaque** | Entero, cortes, garras; caja de ~10 kg, bloque, IQF; pallets o a piso | Sin definir | `17/productos_exportables.md` |
| **Frecuencia** | Contenedores por mes por destino | Tabla §2 (según escala y cuota; **no es demanda**) | Este documento |
| **Temperatura** | Consigna de transporte de congelados | −18 °C o menor `[PVDP · débil]`; norma argentina no verificada | DPV-098 |
| **Tránsito** | Días puerto a puerto, trasbordos, tiempo total | 20–45 d `[PVDP · débil]`; por destino PENDIENTE | DPV-027, DPV-125 |
| **Tramo terrestre** | km planta–puerto, horario de recepción de la terminal, *cut-off* | Barrido 30–1.000 km | 12A |
| **Requisitos documentales** | Certificado sanitario por destino, Halal, origen | `17 §5` | DPV-034 |
| **Servicios adicionales** | Conexión en terminal, monitoreo, inspección, seguro con cobertura de frío | No relevados | DPV-027 |

Con esta plantilla se pide a **navieras, forwarders y despachantes** (sin seleccionar proveedor): tarifa por contenedor, recargos (BAF, reefer, THC), días libres, frecuencia y tiempos. Esa información alimenta el net-back por parte del ave (SUP-017), fuera de esta fase.

## 4. Riesgos propios de la cadena de exportación

Producto que entra "tibio" al contenedor (debe congelarse en planta), corte de energía en terminal o trasbordo, falta de contenedores reefer vacíos (antecedente 2021 sin validar), demoras de buque que vencen certificados, rechazo sanitario en destino y cierre de mercados por IAAP. Detalle y mitigaciones: [`conclusiones_logistica.md` §5](conclusiones_logistica.md) y `17_exportacion`.
