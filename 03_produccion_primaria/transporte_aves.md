# Captura y transporte de aves vivas

**Fecha:** 2026-09-29 · **Versión:** 1 · Fase 0

> **Alcance.** Del ayuno prefaena a la recepción en el frigorífico: captura, carga, densidad, tiempo, clima, mortalidad y merma, bienestar, lavado y desinfección. La logística general (pollitos, alimento, distribución de producto) corresponde a [`../13_logistica/`](../13_logistica/README.md). Fuentes: extractos `[PVDP]`; los parámetros son `[ESTIMACIÓN]` a validar con contratistas y frigoríficos (DPV-054).

---

## 1. Secuencia y tiempos

```
Retiro del alimento (agua disponible) → Captura → Carga → Viaje → Espera en planta → Colgado
|<---------------------- AYUNO TOTAL ≈ 8–12 h (orden de magnitud) ---------------------->|
```

| Etapa | Práctica | Riesgo |
|---|---|---|
| **Ayuno** | Se retira el alimento, no el agua, para vaciar el tracto digestivo. El **ayuno total** (granja + captura + viaje + espera) se planifica en **~8–12 h** `[PVDP]` (FTE-156) | Corto: contaminación fecal en la evisceración (inocuidad). Largo: merma de peso, deshidratación, peor rendimiento y bienestar |
| **Captura manual** | Cuadrillas (contratistas) que trabajan de noche o con luz azul/tenue para calmar a las aves | Hematomas, alas y patas quebradas, rasguños: **decomisos y degradación en planta** |
| **Captura mecanizada** | Máquinas cosechadoras que cargan en módulos | Alta inversión; requiere galpones y caminos adecuados |
| **Carga** | En **cajones plásticos** apilados o en **módulos** (contenedores con cajones fijos que se cargan con autoelevador) | Sobrecarga (asfixia, calor), golpes |
| **Viaje** | Camión abierto o con cortinas laterales; en verano, de noche y sin detenciones; en invierno, protección de lluvia y viento | Estrés térmico, mortalidad en transporte (DOA) |
| **Espera en planta** | Galpón de recepción sombreado y ventilado (ventiladores, nebulización) | Esperas largas en calor = DOA y merma |

## 2. Densidad de carga

La carga se regula por **superficie por kg de ave en el cajón**, ajustada por peso, clima y duración del viaje. Como referencia exigente, el Reglamento (CE) 1/2005 de la UE fija densidades para aves en contenedores según peso y exige **alimento si el transporte supera 12 h** (FTE-159 `[PVDP]`); los valores de cm²/kg del anexo **no se pudieron leer** y quedan pendientes (DPV-054). En Argentina, la carga y el transporte se rigen por normas de SENASA y el Manual de Bienestar Animal del establecimiento (Res. 575/2018 incluye la **captura**, FTE-145); los requisitos específicos del transporte de aves vivas en Argentina **no se relevaron** (DPV-058).

**Regla práctica:** en verano se cargan **menos aves por cajón** (típicamente 1–2 aves menos) `[ESTIMACIÓN]`. Esto aumenta la cantidad de viajes en la estación de mayor riesgo.

## 3. Mortalidad y merma en el transporte

| Indicador | Rango | Clasificación |
|---|---|---|
| **DOA (llegadas muertas)** normal/excelente | ~0,1–0,5 % (se citan 0,35–0,46 % como normales o excelentes) | `[PVDP]` FTE-156 |
| DOA en condiciones adversas | > 1 % (1,63 % promedio en un estudio de Ecuador; ~1,56 % con ayuno < 12 h y 1,69 % en aves sin agua > 8 h) | `[PVDP]` FTE-156 (contexto no argentino) |
| Escenarios del proyecto | 0,2 / 0,3 / 0,5 % | `[SUPUESTO]` SUP-026 |
| **Merma de peso** (ayuno + transporte) | Del orden de **0,2–0,5 % del peso vivo por hora** de ayuno; se debe **predominantemente al ayuno** y solo en parte al transporte | `[ESTIMACIÓN]` a validar; la atribución al ayuno: FTE-156 `[PVDP]` |

**Efecto económico (sin precios):** en una planta de 10.000 aves/día con aves de 2,9 kg, **cada 0,1 % de DOA = 10 aves/día ≈ 2.500 aves/año** (5 d/semana), y **cada 1 % de merma = ~290 kg vivo/día**. Si el pollo se compra o liquida en **kg vivo en granja** vs **kg vivo en planta**, la merma cambia de dueño: debe estar en el contrato ([`modelos_integracion.md`](modelos_integracion.md)).

## 4. Tiempo y distancia máximos razonables

- **No existe un único número.** El límite práctico lo fija el **ayuno total** (≈ 8–12 h) y el clima. Si la captura y la espera ya consumen 4–6 h, el viaje debería ser de **~2–4 h** `[ESTIMACIÓN]`.
- Referencia exigente: 12 h de transporte sin alimento en la UE (FTE-159 `[PVDP]`), pero con ayuno previo en granja el tiempo útil de viaje es mucho menor.
- **Orden de magnitud:** a ~60–70 km/h medios en rutas rurales, 2–4 h equivalen a **~120–250 km** de radio `[ESTIMACIÓN]`. Los clusters integrados suelen concentrar granjas **mucho más cerca** de la planta (radio a relevar: DPV-054).

## 5. Viajes por escenario (orden de magnitud)

Supuesto: **4.000–7.000 aves por camión** según peso, clima y equipo (cajones o módulos) `[SUPUESTO]` SUP-033, a validar con contratistas (DPV-054).

| Planta (aves/día) | kg vivo/día (2,9 kg) | Camiones por día de faena | Cuadrillas de captura por noche |
|---|---|---|---|
| 2.500 | ~7,3 t | ~1 | 1 |
| 5.000 | ~14,5 t | ~1–2 | 1 |
| 10.000 | ~29 t | ~2–3 | 1–2 |
| 20.000 | ~58 t | ~3–5 | 2–3 |

`[ESTIMACIÓN]` · ESCENARIO. Cada granja de ~15.000–30.000 aves se vacía en 1–2 noches; con raleo, en dos momentos distintos.

## 6. Bienestar animal

La Res. SENASA 575/2018 incluye la **captura** entre los contenidos obligatorios del Manual de Bienestar Animal (FTE-145 `[PVDP]`). Los puntos auditables habituales: capacitación de cuadrillas, prohibición de tomar aves por el cuello o por un ala, densidad por cajón, tiempo de ayuno, protección térmica, tiempo de espera, registro de DOA y lesiones. Los importadores exigentes (UE) y los clientes privados pueden auditarlos.

## 7. Lavado y desinfección de camiones y cajones

- Los camiones y cajones **son el principal puente sanitario entre granjas** (entran a todas): se lavan y desinfectan **en la planta después de cada descarga** y antes de volver a una granja, con registro.
- La planta necesita un **área de lavado** de camiones y cajones/módulos con agua, desinfectante y tratamiento del efluente (a considerar en `09_layout_obra_civil` y `11_agua_efluentes`).
- Las cuadrillas de captura también circulan entre granjas: ropa y calzado limpios, sin haber estado en otra granja el mismo día (salvo protocolo).

## 8. Por qué la distancia granja–frigorífico condicionará la localización

1. **Bienestar y mortalidad:** a más horas, más DOA y más riesgo en verano.
2. **Merma de peso:** cada hora adicional de ayuno reduce kg vendibles.
3. **Costo de flete de aves vivas:** se transporta un producto voluminoso y de baja densidad de carga (aves en cajones), con camiones que vuelven vacíos.
4. **Bioseguridad:** rutas largas cruzan más zonas y más granjas de terceros.
5. **Operación:** cuadrillas, horarios nocturnos y coordinación con la faena son más difíciles lejos.

**Conclusión:** las granjas (propias o integradas) deben quedar dentro de un **radio acotado alrededor de la planta**; la planta, a su vez, debe estar cerca de los granos (alimento) y a una distancia manejable del mercado (AMBA) o del puerto. Como **transportar pollo vivo lejos es más difícil que transportar carne refrigerada o congelada**, la lógica sectorial es: **planta cerca de las granjas, producto terminado viaja al mercado**. Esto se evaluará en `10_localizacion` (DEC-003) sin anticipar una ubicación.
