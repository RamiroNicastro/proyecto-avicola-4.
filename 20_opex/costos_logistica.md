# Costos de logística por flujo

**Fecha:** 2026-10-02 · Drivers: 12B (capacidades de ESCENARIO de CAPEX: 5.500 aves/camión, 12 t refrigerado y congelado, 28 t granelero, 10 t subproductos; radio 100 km, mercado 300 km, fábrica–granja 75 km, receptor 50 km) y flota de CAPEX 16.

## 1. Flujos y drivers anuales (C1)

| Flujo | Driver | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| Aves vivas | viajes/año | 250 | 250 | 500 | 1.000 |
| | km/año | 43.333 | 43.333 | 86.667 | 173.333 |
| Refrigerado (troncal) | km/año | 180.000 | 180.000 | 360.000 | 540.000 |
| Alimento | viajes/año | 150 | 250 | 450 | 900 |
| | km/año | 22.500 | 37.500 | 67.500 | 135.000 |
| Subproductos (cota inferior, criterio másico) | t/año | 380 | 760 | 1.521 | 3.042 |
| Pollitos, huevos, grano | viajes y km | PENDIENTES (capacidad de camión y distancias: DPV-047, DPV-084, DPV-157) | | | |

Test D07: viajes y km de aves vivas y km de alimento reproducen el CSV de 12B. El reparto capilar del refrigerado sigue PENDIENTE (DEC-053): el km publicado es troncal planta → mercado.

## 2. Dos modelos que no se mezclan

| Flota propia (por flujo) | Tercerizado (por flujo, **un** modelo) |
|---|---|
| Gasoil: L = km × L/km (consumo PENDIENTE en 12B → SIN_CANTIDAD) | Tarifa por viaje (viajes/año) |
| Mantenimiento y neumáticos: km/año | Tarifa por km (km/año) |
| Patente: vehículos de CAPEX | Tarifa por unidad (t, pollito o huevo/año) |
| Seguros: SEG-FLOTA-<flujo> (módulo seguros) | Tarifa por contrato anual |
| Peajes, lavado y desinfección: viajes/año | |
| Equipo de frío vehicular: horas PENDIENTES (pollitos, huevos, refrigerado, congelado) | |
| Choferes: 14A (aves vivas y producto); otros flujos SIN_CANTIDAD | Chofer incluido en la tarifa: horas de 14A visibles como INCLUIDO |
| Terceros eventuales | |

Sin `modelo_tarifa_flete` el flete tercerizado figura con `MODELO_TARIFA_NO_DEFINIDO` (DEC-17-05). Variante con tarifa por unidad: `C1-10000-FLETE-POR-UNIDAD`. Tests A06 (flota tercerizada no carga costos propios; mutación M09), A07 (flota propia no carga flete) y A11 (un modelo por flujo).

## 3. Flota propia (CAPEX 16, con reserva de 1 unidad SUP-16-02) — C3

| Flujo | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves vivas | 2 | 2 | 3 | 4 |
| Refrigerado | 2 | 2 | 2 | 3 |
| Alimento | 2 | 2 | 2 | 3 |
| Subproductos | 3 | 3 | 3 | 3 |

Los costos de flota no se calculan aquí con precios (todos PENDIENTES: DPV-042, DPV-054, DPV-084, DPV-16-16). El flete del alimento y del pollito puede estar incluido en sus precios: la base marca `FLETE_INCLUIDO` y el motor alerta el posible doble conteo.
