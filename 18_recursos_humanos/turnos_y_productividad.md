# Turnos, jornada y productividad

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 14A) · Fase 0

> **Pregunta:** ¿cuántas horas netas de faena caben en la jornada de una cuadrilla y en las 24 h del establecimiento, y cómo se mide la productividad sin elegir un único KPI?
> **Integra** la ecuación de 24 h de 09A ([`../05_proceso_industrial/modelo_capacidad_proceso.py`](../05_proceso_industrial/modelo_capacidad_proceso.py), `ventana_24h`) **sin modificarla** (test R12). **No** se asume que dos turnos son viables ni se elige organización horaria (DEC-036, DEC-14A-03).
> **Clasificación:** presencia, horas extra y alertas `[ESTIMACIÓN]`; jornada de 8 h y tope de horas extra de referencia `[PVDP]` (FTE-14A-001, FTE-14A-002; convenio aplicable no identificado, DPV-14A-01); disponibilidad D, pausas y limpieza intermedia `[SUPUESTO]` de sensibilidad (SUP-061, SUP-062).

---

## 1. Tres modos de turno

| Modo | Cuadrillas | Horas netas por cuadrilla | Qué exige | Riesgo |
|---|---|---|---|---|
| **1 turno** | 1 | h | Que la presencia quepa en una jornada normal (8 h `[PVDP]`) | Si no cabe: horas extra sistemáticas → se vuelve turno extendido |
| **Turno extendido** | 1 | h | Horas extra diarias (tope de trabajo 10 h, SUP-14A-02) | Horas extra/mes por encima del tope de referencia (30 h/mes `[PVDP]`); fatiga, accidentes, ausentismo |
| **2 turnos** | 2 | h / 2 | Dos cuadrillas completas con mando y técnico; solapamiento de 0,25 h; ventana de 24 h suficiente para limpieza, sanitización y mantenimiento | Ecuación de 24 h negativa; segundo turno parcialmente nocturno (jornada nocturna de 7 h, Ley 11.544 `[PVDP]`, no modelada); duplicar personal calificado |

## 2. Horas netas ≠ horas de presencia

Para una cuadrilla de línea:

```
presencia = h_c / D  +  pausas(h_c)  +  limpieza intermedia(h_c)  [+ 0,25 h de traspaso si hay 2 cuadrillas]
```

con h_c = horas netas por cuadrilla, D = disponibilidad (0,95 / 0,90 / 0,85) y pausas y limpieza intermedia proporcionales a las de 09A (SUP-062). Arranque, cierre, limpieza post-producción, sanitización y mantenimiento los cubren **otros equipos** (técnicos, cuadrilla de limpieza), no la cuadrilla de línea.

**Horas netas máximas** (sin horas extra) según las sensibilidades de 09A:

| Escenario (D) | 1 cuadrilla en 8 h | Turno extendido a 10 h | 2 cuadrillas en 8 h cada una | Ecuación de 24 h (09A) |
|---|---|---|---|---|
| Optimista (0,95) | **7,0 h** | 8,7 h | **13,5 h** | 16,6 h |
| Media (0,90) | **6,4 h** | 8,0 h | **12,4 h** | 13,8 h |
| Conservadora (0,85) | **5,9 h** | 7,3 h | **11,4 h** | 10,0 h |

**Hallazgos (tensión registrada, no resuelta):**

1. **"8 h netas en un turno" no entra en una jornada de 8 h** con estos supuestos: la presencia resulta ~10 h (9,97 h en el escenario medio) y genera ~43 h extra por persona y mes, por encima del tope de referencia de 30 h. La referencia de 8 h netas usada en 23, 05 y 12B (SUP-053) es, en términos de personal, un **turno extendido** o una organización con solapamiento, no un turno simple. Con jornada normal, una cuadrilla rinde ~6–7 h netas.
2. **"16 h = 2 × 8 h netas" choca dos veces:** con la jornada (presencia de 10,2 h por cuadrilla) y con la ecuación de 24 h (holgura +0,9 / −2,8 / −8,3 h). Dos cuadrillas sin horas extra dan **~11–13,5 h netas/día**, es decir ~1,9 veces una cuadrilla en jornada normal (~1,7 en el escenario conservador, limitado por las 24 h), **no 2 veces 8 h**. En el escenario conservador la ecuación de 24 h (10 h) es más restrictiva que la jornada.
3. Estas restricciones dependen de D, pausas y limpieza intermedia, que son **sensibilidades sin dato argentino** (DPV-082, DPV-091). Se informan como alertas; **no** se descarta ningún modo.

## 3. Turnos por escala

Automatización de referencia de 09A, config. B, propios, productividad media. Holgura de 24 h en los escenarios optimista / medio / conservador.

| Escala | Modo | h netas/día | Cuadrillas | Presencia por cuadrilla (h) | Horas extra/persona-mes | Holgura 24 h (h) | Directos/turno | Total personas | Equivalentes | Alertas |
|---|---|---|---|---|---|---|---|---|---|---|
| 2.500 | 1 | 6 | 1 | 7,48 | 0 | 12,6 / 10,0 / 5,8 | 27 | 71 | 50,0 | — |
| 2.500 | 1 | 8 | 1 | 9,97 | 43 | 10,3 / 7,5 / 3,1 | 24 | 64 | 55,0 | JORNADA |
| 2.500 | extendido | 8 | 1 | 9,97 | 43 | 10,3 / 7,5 / 3,1 | 24 | 64 | 55,0 | HORAS EXTRA |
| 2.500 | extendido | 10 | 1 | 12,46 | 97 | 8,0 / 5,0 / 0,4 | 22 | 60 | 59,2 | JORNADA EXTENDIDA; HORAS EXTRA |
| 2.500 | 2 | 12 | 2 | 7,73 | 0 | 5,5 / 2,2 / −2,9 | 20 | 87 | 68,2 | — (24 h negativa sólo en conservador) |
| 2.500 | 2 | 16 | 2 | 10,22 | 48 | 0,9 / −2,8 / −8,3 | 19 | 84 | 80,9 | 24 H; JORNADA |
| 5.000 | 1 | 6 | 1 | 7,48 | 0 | 12,6 / 10,0 / 5,8 | 42 | 103 | 75,8 | — |
| 5.000 | extendido | 8 | 1 | 9,97 | 43 | 10,3 / 7,5 / 3,1 | 33 | 91 | 78,6 | HORAS EXTRA |
| 5.000 | 2 | 12 | 2 | 7,73 | 0 | 5,5 / 2,2 / −2,9 | 26 | 121 | 94,5 | — |
| 5.000 | 2 | 16 | 2 | 10,22 | 48 | 0,9 / −2,8 / −8,3 | 23 | 111 | 107,6 | 24 H; JORNADA |
| 10.000 | 1 | 6 | 1 | 7,48 | 0 | 12,6 / 10,0 / 5,8 | 47 | 132 | 98,5 | — |
| 10.000 | extendido | 8 | 1 | 9,97 | 43 | 10,3 / 7,5 / 3,1 | 38 | 115 | 99,6 | HORAS EXTRA |
| 10.000 | 2 | 12 | 2 | 7,73 | 0 | 5,5 / 2,2 / −2,9 | 28 | 140 | 112,3 | — |
| 10.000 | 2 | 16 | 2 | 10,22 | 48 | 0,9 / −2,8 / −8,3 | 23 | 128 | 121,6 | 24 H; JORNADA |
| 20.000 | 1 | 6 | 1 | 7,48 | 0 | 12,6 / 10,0 / 5,8 | 46 | 175 | 128,4 | — |
| 20.000 | extendido | 8 | 1 | 9,97 | 43 | 10,3 / 7,5 / 3,1 | 39 | 151 | 127,7 | HORAS EXTRA |
| 20.000 | 2 | 12 | 2 | 7,73 | 0 | 5,5 / 2,2 / −2,9 | 29 | 173 | 137,0 | — |
| 20.000 | 2 | 16 | 2 | 10,22 | 48 | 0,9 / −2,8 / −8,3 | 25 | 158 | 147,2 | 24 H; JORNADA |

Todas las combinaciones (incluidos "1 turno 8 h" y "extendido 10 h" en todas las escalas, y las cuatro automatizaciones) están en [`escenarios_rrhh.csv`](escenarios_rrhh.csv), columnas `presencia_cuadrilla_h`, `horas_extra_mes_persona`, `holgura_24h`, `alertas`.

**Lecturas:**

1. **Más horas netas con la misma cuadrilla = menos personas, más horas extra.** Pasar de 6 a 8 h netas en 20.000 aves/día baja de 175 a 151 personas (la línea corre más lento, hacen falta menos puestos), pero cada persona hace ~43 h extra/mes. Los equivalentes casi no cambian (128 → 128): **la mano de obra no se ahorra, se concentra en menos personas**.
2. **Dos cuadrillas de 6 h netas** (12 h/día) caben en la jornada y, salvo en el escenario conservador, en las 24 h; frente a una cuadrilla de 6 h para las mismas aves cuestan +23 % de personas en 2.500, +17 % en 5.000, +6 % en 10.000 y −1 % en 20.000 (más supervisión, técnicos y jefes de turno, compensados a gran escala porque una sola cuadrilla de 6 h exige una línea de 3.333 aves/h con más puestos); a cambio, la línea es la mitad de rápida.
3. **Dos cuadrillas de 8 h netas** muestran alerta en todos los escenarios salvo el optimista: no se descartan, pero requieren demostrar en plantas reales limpieza más corta o simultánea por sectores (DPV-091) y un esquema de jornada admitido por el convenio (DPV-082, DPV-14A-01).
4. **Seis días por semana** con una cuadrilla lleva las horas extra a ~64 h/persona-mes: en la práctica exige más personas o rotación de francos (no modelado; alerta).

## 4. Productividad: indicadores (ninguno es "la verdad")

Escenario de referencia; productividad media (entre paréntesis, alta–baja).

| Indicador | Qué mide | Qué oculta | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|---|
| Aves / persona-hora directa | Rendimiento de la línea | Limpieza, mantenimiento, mix | 10,4 (12,4–7,6) | 15,2 (19,5–10,4) | 26,4 (37,6–18,0) | 51,4 (83,9–35,2) |
| kg comestible / persona-hora directa | Rendimiento ajustado por peso | Valor del producto (entero ≠ deshuesado) | 25 (30–18) | 36 (47–25) | 63 (90–43) | 123 (201–84) |
| Aves / persona-hora total interna | Productividad de la empresa | Tercerizaciones (bajan el denominador) | 5,0 (6,2–3,6) | 7,1 (8,7–4,9) | 11,2 (14,4–7,4) | 17,4 (23,9–11,1) |
| Personas internas / 1.000 aves/día | Tamaño relativo de la organización | Horas extra, turnos, tercerizados | 25,6 (22,8–32,8) | 18,2 (15,6–23,6) | 11,5 (9,2–15,4) | 7,5 (5,7–10,8) |
| Directos / 1.000 aves/día | Intensidad de mano de obra en línea | Automatización trasladada a soporte | 12,8 (12,0–16,4) | 8,4 (7,2–11,2) | 4,8 (3,7–6,4) | 2,4 (1,7–3,2) |
| Dotación indirecta / directa (eq.) | Peso de la estructura y del soporte | Si sube por automatización, no es ineficiencia | 0,85 (0,85–0,82) | 0,92 (1,08–0,82) | 1,11 (1,41–1,04) | 1,64 (2,25–1,68) |
| Directos por supervisor de línea | Span de control | Calidad del mando, rotación | 12,0 (22,0–15,0) | 16,5 (28,0–14,7) | 19,0 (29,0–12,8) | 19,5 (26,0–13,0) |
| Equipos (unidades) por técnico | Carga de mantenimiento por persona | Complejidad del equipo (un automático ≠ una bomba) | 26,2 (39,7–11,4) | 19,1 (24,5–11,4) | 14,3 (18,0–8,0) | 11,4 (18,3–5,0) |

**Reglas de uso:**

1. Comparar plantas **sólo** con el mismo mix, nivel de automatización, alcance (¿incluye limpieza, mantenimiento, choferes, granjas?) y base horaria. Un indicador de una planta que terceriza limpieza no es comparable con uno de una planta que la hace propia.
2. Mirar **al menos tres** indicadores juntos: uno de línea (aves o kg por persona-hora directa), uno de organización (personas por 1.000 aves) y uno de estructura (indirecta/directa).
3. Ningún valor de esta tabla es un benchmark argentino: son resultados de coeficientes supuestos. Sirven para **ordenar preguntas** en las visitas, no para fijar metas.

## 5. Automatización y dotación

Mismo escenario (1 cuadrilla, 8 h netas en turno extendido, config. B, propios, media): directos/turno · total personas · técnicos de mantenimiento (eq.) · indirecta/directa.

| Escala | Manual | Mecanizado | Semiautomático | Automático |
|---|---|---|---|---|
| 2.500 | 24 · 64 · 2,3 · 0,85 | 23 · 63 · 2,3 · 0,89 | 18 · 58 · 3,4 · 1,12 | 16 · 59 · 5,4 · 1,39 |
| 5.000 | 37 · 96 · 3,3 · 0,82 | 33 · 91 · 3,3 · 0,92 | 23 · 81 · 3,5 · 1,35 | 19 · 79 · 5,6 · 1,69 |
| 10.000 | 63 · 144 · 4,5 · 0,69 | 57 · 138 · 4,5 · 0,77 | 38 · 115 · 4,5 · 1,11 | 25 · 103 · 5,8 · 1,75 |
| 20.000 | 116 · 235 · 4,5 · 0,56 | 103 · 220 · 4,5 · 0,62 | 65 · 175 · 4,7 · 0,95 | 39 · 151 · 7,5 · 1,64 |

Puestos por turno en evisceración / trozado / empaque:

| Escala | Manual | Mecanizado | Semiautomático | Automático |
|---|---|---|---|---|
| 2.500 | 6 / 5 / 4 | 6 / 4 / 4 | 3 / 3 / 3 | 3 / 2 / 2 |
| 5.000 | 10 / 9 / 7 | 10 / 7 / 6 | 5 / 5 / 4 | 4 / 3 / 3 |
| 10.000 | 18 / 16 / 13 | 18 / 13 / 11 | 9 / 9 / 7 | 5 / 5 / 4 |
| 20.000 | 35 / 30 / 25 | 35 / 25 / 20 | 16 / 17 / 13 | 8 / 8 / 7 |

**Dónde la automatización…**

| Efecto | Dónde | Evidencia en el modelo |
|---|---|---|
| **Reduce tareas** | Evisceración (35 → 8 puestos/turno a 20.000), trozado, empaque, descarga, clasificación, transporte de subproductos | Directos/turno −66 % (20.000) y −33 % (2.500) de manual a automático |
| **Cambia perfiles** | Del operario de cuchillo al operador de máquina, al de repaso/trimming y al de control de parámetros; del electricista al técnico de automatización | Los puestos que quedan son de repaso, inspección de calidad y ajuste (fijos por área en el modelo) |
| **Aumenta la necesidad técnica** | Mantenimiento: técnicos +1,3 a +3,1 eq. de manual a automático según escala; especialista en automatización en automático ≥ 10.000 | Test R03: la automatización nunca reduce técnicos |
| **Crea dependencia de mantenimiento** | Equipos críticos que detienen la línea (evisceradora automática, transferencia, balanza de línea; [`../08_maquinaria/catalogo_equipos.md`](../08_maquinaria/catalogo_equipos.md) §2); repuestos y servicio técnico local no verificados (DPV-089) | En 2.500 la automatización completa **aumenta** el total (58 → 59): el ahorro de directos no compensa técnicos y limpieza de equipos |

**Lecturas:** la automatización baja el total de personas poco en 2.500 (64 → 59; de semiautomático a automático no ahorra), algo en 5.000 (96 → 79) y mucho en 10.000–20.000 (144 → 103; 235 → 151), pero sube la proporción de indirectos y la exigencia técnica. Ninguna de estas cifras decide DEC-037: falta costo laboral, CAPEX, disponibilidad de técnicos por corredor (DPV-14A-08) y productividad real (DPV-092).
