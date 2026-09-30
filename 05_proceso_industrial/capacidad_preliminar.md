# Capacidad preliminar de faena — definiciones y ritmos físicos

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance:** solo define términos de capacidad y calcula qué **ritmo de línea** implicaría cada escala de 2.500–20.000 aves faenadas/día según las horas netas de faena. **No** diseña el proceso industrial, **no** selecciona maquinaria ni proveedores, **no** asume la eficiencia real de ningún equipo, **no** fija la capacidad de la planta (regla 9) ni el número de turnos (DEC-036).
> Modelo: [`../23_plan_expansion/modelo_escala.py`](../23_plan_expansion/modelo_escala.py) (bloque `ritmo_linea` de [`escenarios_escala.csv`](../23_plan_expansion/escenarios_escala.csv)). Escenarios de escala: [`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md).

---

## 1. Cuatro conceptos que no deben mezclarse (SUP-052)

| Concepto | Definición | Cómo se mide | En este estudio |
|---|---|---|---|
| **Capacidad nominal** | Aves/día que la instalación podría procesar a su **ritmo nominal** durante las horas netas previstas: ritmo nominal (aves/h) × horas netas | Especificación de equipos + organización del trabajo | **No se calcula**: depende de equipos no seleccionados |
| **Capacidad operativa** | Aves/día que la planta puede **sostener** con sus restricciones reales: personal, frío, efluentes, abastecimiento de aves, retiro de subproductos y el **cuello de botella** (§3). Siempre ≤ nominal | Registro de producción sostenida (semanas) | Es la **escala** del modelo: "planta de 10.000 aves/día" = 10.000 aves faenadas por día operativo a utilización 100 % |
| **Aves realmente faenadas** | Aves que efectivamente entran a la línea y se faenan en el día | Conteo en planta | Escala × utilización |
| **Utilización** | Aves realmente faenadas / capacidad operativa | Promedio de un período | Escenarios de 30, 50, 70, 85 y 100 % |

**Capacidad no es ventas.** La capacidad es lo que la planta *podría* hacer; las ventas dependen de compradores (hoy la demanda documentada es ~0, [`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md) §1).

## 2. Horas de turno vs horas netas de faena

```
horas netas de faena = horas de turno − arranque y cierre − pausas del personal − limpieza intermedia
                       − cambios de producto − paradas no programadas
aves/hora necesarias = aves faenadas/día ÷ horas netas de faena/día
```

- Las **horas de turno** las fija la organización del trabajo y el convenio laboral; las **horas netas** son las que la línea recibe aves. La relación entre ambas en plantas argentinas **no está relevada** (DPV-082): no se adopta ningún valor.
- La capacidad nominal que habría que especificar a un equipo sería mayor que el ritmo requerido, porque ningún equipo opera el 100 % de las horas netas a su ritmo nominal (eficiencia, microparadas). Ese factor **no se asume** hasta relevar equipos (`08_maquinaria`, fase posterior).

## 3. Cuello de botella

La capacidad operativa de la planta es la de su **operación más lenta** (cuello de botella), no la de la línea de faena. Candidatos a verificar en fases posteriores: recepción y espera de aves vivas (andén, ventilación), colgado, escaldado/desplumado, evisceración e inspección, **enfriamiento** (tiempo de residencia), clasificación, **trozado y deshuese** (mano de obra), empaque, **túnel de congelado**, **cámaras**, docks de despacho, **tratamiento de efluentes** (caudal y carga diaria) y **retiro de subproductos**. El mix comercial cambia el cuello de botella: una planta de entero y una de deshuesado con las mismas aves/hora tienen cuellos distintos ([`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §9).

## 4. Ritmo de línea requerido (aves faenadas/hora neta)

`[ESTIMACIÓN]` aritmética; horas netas como sensibilidad (SUP-053). 16 h = dos turnos de 8 h netas.

| Escala (aves faenadas/día operativo) | 6 h netas | 8 h netas | 10 h netas | 16 h netas (2 × 8) | Aves/minuto a 8 h | kg vivo/h a 8 h (2,9 kg) |
|---|---|---|---|---|---|---|
| 2.500 | 417 | 312 | 250 | 156 | 5,2 | 906 |
| 5.000 | 833 | 625 | 500 | 312 | 10,4 | 1.812 |
| 10.000 | 1.667 | 1.250 | 1.000 | 625 | 20,8 | 3.625 |
| 20.000 | 3.333 | 2.500 | 2.000 | 1.250 | 41,7 | 7.250 |

**Lecturas:**

1. **Las mismas aves/hora sirven para escalas distintas según las horas:** 1.250 aves/h son 10.000 aves/día con 8 h netas o 20.000 con 16 h (dos turnos). El segundo turno es una **palanca de crecimiento sin nueva línea**, a costa de personal, limpieza y frío que también deben duplicarse (DEC-036).
2. **Horas netas cortas exigen equipos más rápidos:** 10.000 aves/día en 6 h netas requieren 1.667 aves/h, un 67 % más que en 10 h.
3. **El ritmo no dice nada de la escala mínima eficiente:** que un equipo pueda procesar 300 aves/h no implica que una planta de 2.500 aves/día sea viable. Contexto: el relevamiento de mercado ubica a las plantas medianas del sector en 80.000–200.000 aves/día y a un modelo regional en ~27.000 aves/día ([`../01_mercado/competidores.md`](../01_mercado/competidores.md), `[PVDP · débil]`); la escala mayor estudiada aquí (20.000) está por debajo de todas ellas. La escala mínima eficiente se estima con CAPEX y OPEX (DPV-083), no aquí.
4. Las aves/hora son **aves faenadas**: la llegada de aves vivas debe cubrir además la mortalidad en transporte (0,3 % en el escenario medio, `03_produccion_primaria`) y la programación de la espera en planta.

## 5. Datos faltantes

| Dato | Registro |
|---|---|
| Horas netas por turno y paradas típicas en plantas argentinas; turnos admitidos por convenio | DPV-082 |
| Escala mínima eficiente y tamaños/ritmos de plantas existentes en Argentina | DPV-083 |
| Capacidad y eficiencia de equipos por rango de aves/hora (sin seleccionar proveedores) | Fase de maquinaria (`08_maquinaria`) |
