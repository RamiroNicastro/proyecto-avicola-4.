# Indicadores productivos (KPIs) de la producción primaria

**Fecha:** 2026-09-29 · **Versión:** 1 · Fase 0

> Indicadores que una empresa avícola debería seguir **por lote, por galpón, por granja, por integrado y por proveedor de pollitos**. Las fórmulas son estándar del sector; los rangos orientativos remiten a [`ciclo_productivo.md` §2](ciclo_productivo.md) y son `[ESTIMACIÓN]`/`[SUPUESTO]` hasta tener datos argentinos (DPV-044). **Regla:** todo KPI se informa con su **base** (por ave alojada o faenada, por kg vivo en granja o en planta) y con el **peso y la edad** del lote.

---

## 1. Tabla de KPIs

| # | KPI | Fórmula | Unidad | Qué indica | Rango orientativo (perfil medio) | Frecuencia |
|---|---|---|---|---|---|---|
| 1 | **Mortalidad acumulada** | (aves muertas + descartadas) / pollitos alojados | % | Salud, calidad del pollito, manejo, clima | 3 % (favorable) – 5 % (medio) – 8 %+ (desfavorable); un estudio local de Entre Ríos registró 7,7–9,5 % (FTE-151 `[PVDP]`; señal de riesgo a validar, no promedio argentino) | Diaria y por lote |
| 1a | Mortalidad de 7 días | muertes 0–7 d / alojados | % | **Calidad del pollito y de la recepción** (se usa para reclamar a la incubadora) | ≤ 1 % como objetivo habitual `[PVDP]` | Semana 1 |
| 1b | Mortalidad diaria acumulada vs umbral UE | 1 % + 0,06 % × edad (Dir. 2007/43/CE) | % | Referencia de bienestar para densidades altas | 3,8 % a 47 d | Por lote |
| 2 | **FCR (conversión alimenticia)** | alimento entregado / kg vivo cargado (de campo) | kg/kg | **Eficiencia económica principal** (alimento ≈ mayor costo) | 1,60 – 1,70 – 1,85 | Por lote |
| 2a | FCR corregido | FCR ajustado a un peso estándar | kg/kg | Comparar lotes de distinto peso | — | Por lote |
| 3 | **Peso vivo final** | kg vivo cargado / aves cargadas (o balanza de planta) | kg/ave | Cumplimiento del perfil de mercado; ingreso | 2,7–3,0 kg (perfil medio) | Por lote |
| 4 | **Edad de faena** | días desde el alojamiento a la captura | días | Uso del galpón (ciclos/año) | 45–50 d (medio) | Por lote |
| 5 | **Ganancia diaria (GDP)** | (peso final − peso inicial) / edad | g/ave/día | Velocidad de crecimiento | ~58–62 g/d (medio) | Semanal (pesajes) y por lote |
| 6 | **Uniformidad** | CV del peso = desvío / media; o % de aves dentro de ±10 % del peso medio | % | Homogeneidad: afecta rendimiento en planta (máquinas calibradas), calibres y especificaciones de cliente | CV ≤ 8–10 %; > 75–80 % en ±10 % | Semanal (muestras) |
| 7 | **Consumo de alimento** | kg entregados / aves vivas / día | g/ave/día | Apetito; una caída anticipa problemas | Según curva de la genética | Diaria |
| 8 | **Consumo de agua** | L / aves vivas / día; **relación agua/alimento** | mL/ave/día; L/kg | **Alerta temprana** (12–24 h antes de síntomas); detecta fallas de bebederos o calor | Relación 1,6–2,0 a ~21 °C (FTE-155 `[PVDP]`) | Diaria (medidor por galpón) |
| 9 | **Densidad final** | kg vivo cargado / m² de galpón | kg/m² | Uso del activo; bienestar | 30–39 kg/m² según galpón | Por lote |
| 9a | **Productividad del galpón** | kg vivo producido / m² / año | kg/m²/año | Rinde del activo (combina densidad y ciclos) | ~155–235 kg/m²/año `[ESTIMACIÓN]` (30 × 5,2 ≈ 156; 35 × 5,7 ≈ 200; 39 × 6,0 ≈ 234) | Anual |
| 10 | **IEP / FEP** (índice de eficiencia productiva) | (supervivencia % × peso kg) / (edad d × FCR) × 100 | índice | Resume peso, velocidad, conversión y mortalidad en un número; muy usado para **ranking de integrados** | Medio: (95 × 2,9)/(47 × 1,70) × 100 ≈ **345**; favorable (97 × 2,9)/(47 × 1,60) × 100 ≈ 374; desfavorable (92 × 2,9)/(47 × 1,85) × 100 ≈ 307 `[ESTIMACIÓN]` | Por lote |
| 11 | **Costo por kg vivo** | (pollito + alimento + sanidad + energía + mano de obra + amortización + otros) / kg vivo | USD/kg vivo | Competitividad y decisión hacer/comprar | **Sin valor en esta fase** (sin precios; DPV-019) | Por lote y mensual |
| 12 | **Condenas/decomisos en frigorífico** | aves o kg decomisados (total o parcial) / aves o kg recibidos, por causa | % | Salud y manejo en granja (celulitis, ascitis, aerosaculitis, hematomas, fracturas) y en captura | A relevar (DPV-044) | Por lote |
| 13 | **Mortalidad en transporte (DOA)** | aves muertas al llegar / aves cargadas | % | Captura, carga, clima, tiempo | 0,2–0,5 % (SUP-026) | Por viaje |
| 14 | **Merma de peso** | (kg en granja − kg en planta) / kg en granja | % | Ayuno y transporte; define quién pierde kg en el contrato | ~0,2–0,5 %/h de ayuno `[ESTIMACIÓN]` | Por viaje |
| 15 | **Pododermatitis** (lesiones plantares) | puntaje en planta sobre muestra de patas | índice o % | **Calidad de cama y bienestar**; también el **grado de las garras** para exportación (ingreso por ave) | A relevar | Por lote |

## 2. Cómo se relacionan (árbol de valor)

```
Costo por kg vivo
 ├── Alimento  = kg vivo × FCR × precio del alimento   ← FCR (2), peso (3)
 ├── Pollito   = pollitos alojados × precio / kg vivo  ← mortalidad (1), peso (3)
 ├── Galpón    = amortización / (kg/m²/año)            ← densidad (9), ciclos (edad 4 + vacío)
 └── Otros     = energía, sanidad, mano de obra

Ingreso por ave (planta) ← peso (3), uniformidad (6), decomisos (12), DOA (13), merma (14), pododermatitis (15)
```

## 3. Uso gerencial

- **Tablero por lote** con los KPIs 1–10, 12–15 y comparación contra objetivo, contra el lote anterior del mismo galpón y contra el promedio de la empresa.
- **Ranking de integrados** por IEP y costo por kg (base de pagos por desempeño).
- **Ranking de proveedores de pollito** por mortalidad de 7 días y uniformidad.
- **Alertas diarias:** consumo de agua, mortalidad diaria, temperatura, corte de energía.
- **Cierre de lote en 7–15 días** con liquidación y análisis de causas.
