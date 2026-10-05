# Break-even (punto de equilibrio)

**Fecha:** 2026-10-04 · Código: `break_even_anual()`, `break_even_simple()` · Salida: [`break_even.csv`](break_even.csv)

## 1. Método: margen de contribución del año maduro

Sobre el **último año del horizonte** (año maduro), con el **mismo mix y los mismos precios** de la corrida (SUP-206):

```
Ingreso neto (∝ precio)              R
Impuestos ∝ precio (IIBB + tasas)    I
Costos variables                     CV = OPEX variable + parte variable de semivariables + logística del canal
                                          + costos de exportación + extras de ramp-up
Costos fijos                         CF = OPEX fijo + semifijo + parte fija de semivariables + otros impuestos fijos
                                          (+ depreciación en la versión EBIT)
Margen de contribución               MC = R − I − CV ;  MC por ave = MC ÷ aves del año

BREAK-EVEN EN VOLUMEN       q* = CF ÷ (MC por ave)                 [aves/año y kg vendidos]
BREAK-EVEN EN UTILIZACIÓN   u* = q* ÷ capacidad de aves del año
BREAK-EVEN EN PRECIO        k* = (CV + CF) ÷ (R − I)  → precio medio* = k* × precio medio bruto actual
```

## 2. Estados posibles

| Estado | Significado |
|---|---|
| `CALCULADO` | q* existe y es alcanzable |
| `CALCULADO; q* SUPERA LA DEMANDA CONTABLE DEL AÑO` | Habría que vender más de lo que la demanda cargada permite |
| `NO_ALCANZABLE_CON_LA_CAPACIDAD (q* > capacidad)` | u* > 100 %: ninguna utilización de esa planta cubre los fijos |
| `NO_EXISTE (margen de contribución ≤ 0)` | Cada ave vendida pierde dinero: más volumen agrava la pérdida |
| `NO_CALCULABLE` | Faltan costos variables o precios: **no se calcula** |

Se publican dos versiones: base **EBITDA** (equilibrio operativo) y base **EBIT** (incluye depreciación).

## 3. Validación

- Test N07: caso simple p = 10, cv = 6, CF = 400, capacidad 200 → q* = 100, u* = 50 %; con p ≤ cv → `NO_EXISTE`.
- En el motor (test N07: caso de prueba pre-tax con ingresos 100/año, OPEX variable 24/año y fijo 60/año): u* = 60 ÷ 76 = 78,9 % y precio* = 84 ÷ 12 por kg.

## 4. Límites

- Supone que el mix y el precio medio no cambian con el volumen, y que la demanda acompaña (si no, lo indica el estado).
- Los semifijos son fijos **dentro de la etapa**: el break-even de una planta mayor no es el de una menor.
- No se calcula hoy para el proyecto: costos variables y precios están materialmente incompletos (`PUBLICABLE_BREAK_EVEN = FALSE` en las 61 corridas).
