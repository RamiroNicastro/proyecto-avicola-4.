# Logística propia — CAPEX de flota

**Fecha:** 2026-10-02 (v1.1, auditoría de procedencia) · Drivers: `13_logistica/modelo_logistica.py` (12B) · Decisión abierta: DEC-056 (modalidad de flota por flujo)

> Con flota **tercerizada** no hay CAPEX de vehículos (test A03); el costo del transporte será OPEX. Con flota **propia** o **mixta**, el motor calcula unidades por flujo desde el volumen; **no fija cantidades arbitrarias**. Ningún vehículo tiene precio.

## 1. Regla de dimensionamiento

```
unidades = ⌈ VIAJES (volumen ÷ capacidad del vehículo) ÷ CICLOS DISPONIBLES ⌉ + RESERVA
```

| Flujo | Volumen y viajes (12B) | Capacidad de escenario | Ciclos | Estado |
|---|---|---|---|---|
| Aves vivas | `aves_vivas()`: flota mínima con ventana prefaena, radio 100 km | 5.500 aves/camión (SUP-033) | del modelo 12B | ESTIMACIÓN con SUPUESTOS |
| Refrigerado | `producto()`: camión-día, troncal 300 km, 6 despachos/semana | 12 t (DPV-084) | del modelo 12B | ídem; reparto capilar a la red **no** modelado (DEC-053) |
| Congelado | `producto()`: 2 despachos/semana | 12 t | del modelo 12B | ídem |
| Alimento / granos | `insumos()`: viajes/semana a 75 km | 28 t granelero (SUP-096) | 2 × 75 km ÷ 70 km/h + 2 h; 12 h/día; 6 d/sem (SUP-16-03) | ídem |
| Pollitos | `insumos()` | **PENDIENTE** (DPV-047, DPV-084) | — | **cantidad PENDIENTE** |
| Subproductos | `subproductos()`: 4 corrientes, retiro diario, criterio **másico** | 10 t | 2 × 50 km ÷ 70 km/h + 2 h | **cota inferior** (volumétrico PENDIENTE, DPV-135; T16-05) |
| Servicio | sin driver físico | — | — | **PENDIENTE** |

Reserva: +1 unidad por flujo propio (SUP-16-02, barrido 0/1). Las capacidades son de **escenario** (SUP-16-20), no validadas.

### Procedencia por tipo de vehículo (auditoría v1.1; detalle en [`mapa_drivers_capex.csv`](mapa_drivers_capex.csv))

| Flujo | Volumen | Payload | Ciclo y frecuencia | Unidades base | Tipo de procedencia |
|---|---|---|---|---|---|
| Aves vivas | aves/día (12B) | 5.500 aves/camión (escenario SUP-033) | ventana prefaena, radio 100 km, horas útiles (12B) | `flota_minima` de 12B, sin cambios | **DIRECTO** (reproduce `escenarios_logistica.csv`, test N10) |
| Refrigerado | t/día por perfil (12B) | 12 t (escenario DPV-084) | 6 despachos/sem, troncal 300 km (12B) | ⌈`refrigerado_camion_dia`⌉ | **DERIVADO_CAPEX** (redondeo hacia arriba de una salida de 12B) |
| Congelado | ídem | 12 t | 2 despachos/sem | ⌈`congelado_camion_dia`⌉ | DERIVADO_CAPEX |
| Alimento / granos | t/sem (12B) | 28 t (SUP-096) | ciclo CAPEX: 2 × 75 km ÷ 70 km/h + 2 h; 12 h/día; 6 d/sem | viajes/sem ÷ ciclos | DERIVADO_CAPEX + SUPUESTO_CAPEX (SUP-16-03) |
| Subproductos | t/día por corriente (12B) | 10 t másica (volumétrica PENDIENTE) | retiro diario; ciclo CAPEX a 50 km | Σ viajes de 4 grupos ÷ ciclos | DERIVADO_CAPEX, **cota inferior** |
| Pollitos | pollitos/sem (14B) | **PENDIENTE** | — | — | PENDIENTE |
| Servicio | sin driver | — | — | — | PENDIENTE |
| Reserva | — | — | — | +1 por flujo | SUPUESTO_CAPEX (SUP-16-02) |

Ningún payload ni tiempo de ciclo se trata como capacidad validada: todos son escenarios de 12B o supuestos de CAPEX.

## 2. Unidades por escala (C3, flota propia en todos los flujos, perfil P2)

| Flujo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves vivas | 2 | 2 | 3 | 4 |
| Refrigerado | 2 | 2 | 2 | 3 |
| Congelado | 2 | 2 | 3 | 5 |
| Alimento / granos | 2 | 2 | 2 | 3 |
| Subproductos (cota inferior) | 3 | 3 | 3 | 3 |
| Pollitos | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |
| Servicio | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE |

Incluye la reserva. En escalas chicas la reserva pesa tanto como la flota base: es un efecto del supuesto, no una conclusión sobre flota propia.

## 3. Desagregación por vehículo (cada uno con su COSTO_ID)

| Componente | Flujos | ID |
|---|---|---|
| Vehículo (chasis / tractor) | todos | VEH-<FLUJO> |
| Carrocería / semirremolque (caja, tolva, cisterna) | todos salvo servicio | CAR-<FLUJO> |
| Equipo de frío / climatización | pollitos, refrigerado, congelado | FRI-<FLUJO> |
| Equipo auxiliar (rastreo, registro de temperatura, seguridad) | todos | AUX-<FLUJO> |
| Jaulas / cajones / módulos (EQ-03) | aves vivas | JAU-VIVO (cantidad PENDIENTE: aves por cajón y juegos por camión) |
| Cajas / carros de pollitos | pollitos | JAU-POLLITOS (PENDIENTE) |
| Contenedores rotativos | subproductos | CNT-SUBPRODUCTOS (PENDIENTE) |

Con transporte de aves vivas **tercerizado** y planta propia, los cajones aparecen con `TITULAR = PENDIENTE` (no se cargan a la empresa ni se omiten: DEC-16-06, DPV-16-10).

## 4. Qué falta

Capacidades útiles validadas por flujo (DPV-084, DPV-135), capacidad de camión de pollitos (DPV-047), reparto capilar a la red (DEC-053), precios de chasis, carrocería y equipo de frío en Argentina (DPV-16-16), tipo de vehículo por corriente de subproductos (cisterna para sangre, contenedores estancos para el resto).
