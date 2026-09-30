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

La capacidad operativa de la planta es la de su **operación más lenta** (cuello de botella), no la de la línea de faena. Sistemas a verificar en fases posteriores, todos candidatos a cuello de botella:

| Grupo | Sistemas |
|---|---|
| Entrada de aves | Recepción y espera de aves vivas (andén ventilado), **bienestar animal**, logística de granjas (captura, carga y programación de camiones) |
| Faena | Colgado, aturdimiento, escaldado y desplumado, **eviscerado** e inspección |
| Enfriamiento y proceso | **Chilling** (tiempo de residencia), clasificación, **salas de corte y deshuese**, empaque |
| Frío y despacho | **Túneles de congelado**, **cámaras**, docks de **expedición** |
| Servicios | **Agua**, **efluentes** (caudal y carga diaria), **energía**, **refrigeración** (sala de máquinas) |
| Organización | **Mano de obra** por turno, **limpieza y sanitización** entre turnos y diaria, **mantenimiento** |
| Subproductos | Retiro diario de sangre, plumas y vísceras |

El mix comercial cambia el cuello de botella: una planta de entero y una de deshuesado con las mismas aves/hora tienen cuellos distintos ([`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §9).

## 4. Ritmo de línea requerido (aves faenadas/hora neta)

`[ESTIMACIÓN]` aritmética; horas netas como sensibilidad (SUP-053). 16 h = dos turnos de 8 h netas.

| Escala (aves faenadas/día operativo) | 6 h netas | 8 h netas | 10 h netas | 16 h netas (2 × 8) | Aves/minuto a 8 h | kg vivo/h a 8 h (2,9 kg) |
|---|---|---|---|---|---|---|
| 2.500 | 417 | 312 | 250 | 156 | 5,2 | 906 |
| 5.000 | 833 | 625 | 500 | 312 | 10,4 | 1.812 |
| 10.000 | 1.667 | 1.250 | 1.000 | 625 | 20,8 | 3.625 |
| 20.000 | 3.333 | 2.500 | 2.000 | 1.250 | 41,7 | 7.250 |

**Lecturas:**

1. **Segundo turno = capacidad teórica de la LÍNEA:** 1.250 aves/h son 10.000 aves/día con 8 h netas y, **solo si existen 16 h netas de faena**, 20.000 con dos turnos. Eso no es la capacidad de la **planta**: antes deben comprobarse todos los sistemas de §3 (recepción de aves, colgado, eviscerado, chilling, salas de corte, mano de obra, cámaras, congelado, expedición, agua, efluentes, energía, refrigeración, limpieza y sanitización —que además necesita su propia ventana horaria—, mantenimiento, bienestar animal y logística de granjas). **No se afirma** que un segundo turno permita 20.000 aves/día sin obra nueva (DEC-036).
2. **Sexto día ≠ segundo turno:** pasar de 250 a 300 días de faena por año aumenta ~20 % el **volumen anual** potencial con la **misma capacidad diaria**; no cambia las aves por día ni el ritmo de la línea. El segundo turno actúa sobre las horas por día; el sexto día, sobre los días por año.
3. **Horas netas cortas exigen equipos más rápidos:** 10.000 aves/día en 6 h netas requieren 1.667 aves/h, un 67 % más que en 10 h.
4. **El ritmo no dice nada de la escala mínima eficiente:** que un equipo pueda procesar 300 aves/h no implica que una planta de 2.500 aves/día sea viable, ni lo contrario. **No se concluye** que 2.500 sea demasiado chico ni que 20.000 sea demasiado grande: la escala mínima eficiente surgirá después de estudiar maquinaria, turnos, dotación, CAPEX, OPEX, servicios y utilización (DPV-083). Contexto: el relevamiento de mercado ubica a las plantas medianas del sector en 80.000–200.000 aves/día y a un modelo regional en ~27.000 aves/día ([`../01_mercado/competidores.md`](../01_mercado/competidores.md), `[PVDP · débil]`); la escala mayor estudiada aquí (20.000) está por debajo de todas ellas. La escala mínima eficiente se estima con CAPEX y OPEX (DPV-083), no aquí.
5. Las aves/hora son **aves faenadas**: la llegada de aves vivas debe cubrir además la mortalidad en transporte (0,3 % en el escenario medio, `03_produccion_primaria`) y la programación de la espera en planta.

## 5. Datos faltantes

| Dato | Registro |
|---|---|
| Horas netas por turno y paradas típicas en plantas argentinas; turnos admitidos por convenio | DPV-082 |
| Escala mínima eficiente y tamaños/ritmos de plantas existentes en Argentina | DPV-083 |
| Capacidad y eficiencia de equipos por rango de aves/hora (sin seleccionar proveedores) | Fase de maquinaria (`08_maquinaria`) |
