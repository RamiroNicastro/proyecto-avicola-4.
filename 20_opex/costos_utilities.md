# Costos de utilities, frío y efluentes

**Fecha:** 2026-10-02 · Drivers: 09C (vía CAPEX, nivel medio; bajo/alto en el mapa) · Solo planta de faena propia.

## 1. Cantidades (C1, perfil P1, 8 h netas, configuración B)

| Escala | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Electricidad (kWh/año, total 09C) | 516.266 | 1.032.532 | 2.065.063 | 4.130.127 |
| …de ellos frío de proceso (informativo, incluido) | 158.594 | 317.188 | 634.375 | 1.268.750 |
| Agua captada (m³/año) | 15.625 | 31.250 | 62.500 | 125.000 |
| Efluente (m³/año) | 13.750 | 27.500 | 55.000 | 110.000 |
| Energía de combustible (kWh térmicos/año) | 231.587 | 463.173 | 926.346 | 1.852.692 |
| …equivalente gas natural (m³/año, PCI [SUPUESTO]) | 21.432 | 42.864 | 85.729 | 171.457 |

C3/CF (perfil P2, más congelado): 627.226 / 1.254.452 / 2.508.904 / 5.017.808 kWh/año (`CALCULO_MODELO_FUENTE`). Test D06: C1 reproduce el CSV de 09C.

## 2. Electricidad

| Concepto | ID | Driver | Estado |
|---|---|---|---|
| Energía activa | UT-ELE-KWH | kWh/año (09C) | Tarifa industrial **no asumida** (DPV-17-05) |
| Potencia / demanda contratada | UT-ELE-POT | kW·mes | **SIN_CANTIDAD**: el pico no está dimensionado (DPV-095). Nunca se multiplican kW por la tarifa de kWh |
| Cargo fijo | UT-ELE-FIJO | 12 meses | Sin precio |

## 3. Térmico

El combustible **no está elegido** (DEC-045): sin elección, la fila es UT-TER-NS en kWh térmicos y no puede tener precio. Con `combustible_termico = gas_natural | glp | biomasa` se usa el equivalente de 09C (m³ o kg) y su precio (UT-TER-GN / GLP / BIO). Variante: `C1-10000-GN-RED`.

## 4. Agua

`fuente_agua = red` → UT-AGUA-RED (m³); `pozo` → UT-AGUA-CANON (m³; jurisdicción PENDIENTE); en ambos casos UT-AGUA-TRAT (químicos de potabilización). Sin elección → UT-AGUA-NS (sin precio posible). La **energía de bombeo** ya está en los kWh de 09C (fila INCLUIDO).

## 5. Frío — sin doble conteo

El sistema de frío consume electricidad y mantenimiento. Su electricidad (frío de proceso, congelación, cámaras) **ya está** en `kwh_total_anio` de 09C: se muestra como filas `INCLUIDO` en UT-ELE-KWH, sin costo (test C06, mutación M02). El mantenimiento del frío va en MAN-FRIO-* y la reposición de refrigerante dentro de ese mantenimiento. La contradicción ×5,7 entre la carga física y el reparto top-down de 09C sigue **abierta** (DPV-109): el kWh total de 09C es el benchmark top-down, no un balance frigorífico.

Arquitectura de frío C (congelado tercerizado, y C0): UT-FRIO-TER = t congeladas/año (12B) × tarifa PENDIENTE (DPV-17-06).

## 6. Efluentes

| Concepto | ID | Driver | Estado |
|---|---|---|---|
| Químicos | EF-QUIM | m³ de efluente | Sin precio; tecnología PENDIENTE (DEC-043) |
| Energía | — | incluida en kWh (tratamiento aerobio de 09C) | INCLUIDO |
| Personal | COSTO_LABORAL | — | 14A no tiene operador de efluentes → FTE PENDIENTE (puede estar cubierto por mantenimiento) |
| Análisis de vuelco | EF-ANA | análisis | SIN_CANTIDAD (frecuencia de la autoridad) |
| Lodos | EF-LODO | t | SIN_CANTIDAD: lodos no dimensionados en 09C (DPV-072) |
| Canon de vuelco | EF-CANON | m³ | Sin precio (jurisdicción) |
| Mantenimiento | MAN-UTIL-* | — | Método PENDIENTE |
