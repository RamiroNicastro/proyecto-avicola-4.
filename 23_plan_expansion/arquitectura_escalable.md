# Arquitectura escalable — modularidad, arquitecturas de crecimiento y matriz sin ganador

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance:** análisis **conceptual** de qué conviene dimensionar para la primera etapa, qué dejar preparado y qué sobredimensionar desde la obra inicial; alternativas de secuencia de crecimiento; comparación de las cuatro escalas **sin elegir ganador**. **No** fija dimensiones, **no** diseña layout, **no** selecciona maquinaria, terreno ni localización, **no** calcula CAPEX (DEC-033, DEC-035).
> Cifras físicas: [`escenarios_escala.md`](escenarios_escala.md) y [`escenarios_escala.csv`](escenarios_escala.csv). Gates para pasar de una etapa a otra: [`gates_expansion.md`](gates_expansion.md).

**Idea central:** la **opción de crecer** se preserva con terreno, accesos, servicios y un diseño que admite módulos; **no** construyendo 20.000 aves/día desde el día uno porque algún día se quiera llegar a 20.000.

---

## 1. Modularidad: qué dimensionar, qué preparar, qué sobredimensionar (§14)

Categorías: **A** dimensionar para la primera etapa · **B** dejar preparado para expansión (espacio, conexiones, previsiones) · **C** posiblemente sobredimensionar desde la obra inicial si técnicamente tiene sentido. La clasificación es una **hipótesis de trabajo** (SUP-059) que se valida con ingeniería y CAPEX.

| Elemento | Criterio físico | Clasificación conceptual | Por qué | Riesgo si se equivoca |
|---|---|---|---|---|
| **Terreno** | Superficie para la planta final + retiros, efluentes, estacionamiento de camiones, bioseguridad | **C** | Comprar terreno después es caro o imposible (vecinos, zonificación); ampliar un edificio sin lugar obliga a mudarse | Terreno chico = techo físico definitivo |
| **Accesos** (camino, portones, radios de giro) | Tránsito de camiones de aves vivas, alimento, producto y subproductos (×8 entre 2.500 y 20.000) | **C** para trazado y derechos de paso; **A** para el pavimento | La traza no se cambia; el pavimento se amplía | Cruces de circulación sucio/limpio imposibles de corregir |
| **Servicios**: energía (potencia contratada, subestación), agua (perforaciones, reserva), gas | Crecen casi linealmente con la faena y el frío | **B/C**: reservar potencia, lugar de subestación y derechos de agua; instalar lo de la etapa | La factibilidad de potencia y agua en zona rural es un cuello de botella que tarda (DPV-052, DPV-053, DPV-087) | Sin potencia o agua suficientes, la ampliación se frena aunque haya demanda |
| **Tratamiento de efluentes** | Caudal y carga diaria (no dimensionados: `11_agua_efluentes`) | **B** con previsión de terreno y módulos (lagunas/reactores en paralelo); **C** en lo que no se puede ampliar (cañerías troncales, punto de vuelco, permiso) | El permiso de vuelco y el terreno de tratamiento son difíciles de ampliar; los módulos de proceso sí se agregan | Un efluente subdimensionado puede **cerrar** la planta; uno sobredimensionado trabaja mal con poca carga |
| **Frío** (enfriamiento, túneles, cámaras, sala de máquinas) | Inventario ×8 entre escalas; depende del perfil refrigerado/congelado (§11 de escenarios) | **A** en evaporadores y cámaras; **B** en sala de máquinas y espacio para compresores y cámaras adicionales; **C** posible en cañerías principales y estructura | La sala de máquinas y sus troncales son costosas de rehacer; las cámaras se agregan por módulos | Frío insuficiente limita el congelado y la exportación; frío ocioso consume energía sin producto |
| **Edificio** (zona limpia/sucia, cerramientos, pisos, desagües) | Flujos higiénicos (estándar UE como hipótesis, SUP-015) | **B**: diseñar el edificio final y construir por etapas con **muros de ampliación** previstos; **C** en la zona de faena si el flujo higiénico lo exige | Ampliar sin cortar la operación ni romper el flujo sucio→limpio exige preverlo | Ampliaciones que cruzan flujos comprometen habilitaciones de exportación |
| **Corrales / recepción de aves vivas** | Aves por hora de llegada, espera ventilada (bienestar) | **A** con espacio **B** | Crece con el ritmo, no con la superficie total | Espera en camión con calor = mortalidad (DOA) |
| **Línea de faena** | Ritmo (aves/h) × horas netas × turnos | **A**, con la opción de **segundo turno** y, más adelante, una **segunda línea** en espacio reservado | El segundo turno duplica la capacidad sin nueva línea ([`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md)); una línea sobredimensionada trabaja fuera de su rango | Línea chica sin espacio para la segunda = techo |
| **Salas de corte y deshuese** | Masa trozada/deshuesada (1,2 t/día en A vs 20,4 en B a 10.000 aves/día) | **A** y **B**: módulos de mesas/equipos agregables | El mix real de la demanda es desconocido (DPV-037) | Invertir en deshuese sin compradores de suprema y sin destino para el hueso |
| **Depósitos** (envases, insumos, químicos) | Rotación y compras | **A** con espacio **B** | Bajo costo relativo de ampliar | Menor |
| **Oficinas y servicios al personal** (vestuarios, comedor) | Dotación por turno | **A**; vestuarios **B** (el segundo turno los comparte en horario; más línea, más gente) | Los vestuarios son parte del flujo higiénico | Vestuarios chicos limitan la dotación por turno |
| **Docks de despacho y recepción** | Camiones/día y número de paradas (DPV-036) | **B**: reservar posiciones; construir las de la etapa | Frente de docks depende del canal (CD vs locales) | Cuello de botella logístico con producto perecedero |
| **Caminos internos y playas de maniobra** | Circulaciones separadas (aves vivas y subproductos vs producto terminado) | **C** en trazado; **A** en construcción | La separación de circulaciones es condición sanitaria | Cruces que ningún módulo posterior corrige |
| **Subproductos** (sala de sangre, playa de contenedores de plumas y vísceras) | 1,3–17 t/día según escala y configuración | **A** con espacio **B** para un eventual proceso propio | El rendering propio **no se decide** (DEC-027, SUP-049) | Sin espacio, la opción de proceso propio desaparece |

**Regla práctica que surge:** sobredimensionar lo **barato de prever y caro de corregir** (terreno, trazas, permisos, troncales, flujos higiénicos); construir por módulos lo **caro de tener ocioso y fácil de agregar** (líneas, cámaras, salas de corte, compresores, docks).

---

## 2. Arquitecturas de crecimiento (§15)

Secuencias posibles; **ninguna es la elegida** (DEC-033). "Etapa 0" = validación comercial previa sin planta propia (compraventa de producto de terceros o faena a façon, DEC-018).

| Arquitectura | Secuencia |
|---|---|
| **A. Escalonada completa** | 2.500 → 5.000 → 10.000 → 20.000 |
| **B. Arranque intermedio** | 5.000 → 10.000 → 20.000 |
| **C. Arranque grande** | 10.000 → 20.000 |
| **D. Validación comercial + turnos** | Etapa 0 (façon/compraventa) → línea de ritmo intermedio a 1 turno (p. ej. 5.000 aves/día en 8 h netas = 625 aves/h) → 2.º turno (10.000) → 2.ª línea en espacio reservado (20.000) |
| **E. Planta diseñada grande, equipada por etapas** | Obra civil, servicios y flujos para la escala final; equipamiento y frío para la etapa 1; se equipa por módulos |

### 2.1 Análisis de cada arquitectura

| | Ventajas | Limitaciones | Cuándo ampliar (ver gates) | Qué debe ser modular | Riesgo de sobredimensionamiento | Riesgo de arrancar demasiado chico |
|---|---|---|---|---|---|---|
| **A** 2.500→20.000 | Menor exposición inicial; aprendizaje operativo y comercial con poco volumen; coherente con la demanda base (2.500 se llena con el escenario base) | Tres ampliaciones = tres obras con la planta operando; la escala 2.500 podría estar **debajo de la escala mínima eficiente** (DPV-083); habilitaciones y equipos quizás no escalables | Cuando la utilización sostenida y la demanda A/B cubran la etapa siguiente (G1–G3) | Casi todo: línea, frío, corte, efluentes, docks | **Menor** | **Mayor**: costo unitario alto, planta que no se puede ampliar si no se previó, clientes perdidos por falta de capacidad |
| **B** 5.000→20.000 | Escala cercana al escenario base con ave completa (91 %); dos ampliaciones | Necesita ~6–8 t/día de demanda real desde el inicio; con mix de supermercado la base ya la excede (124–163 %) | Idem | Línea (segundo turno), frío, corte, efluentes | Medio | Medio |
| **C** 10.000→20.000 | Menos obras; mejores condiciones para consolidar lotes de exportación y atraer receptores de subproductos | Exige **más del doble** del escenario base (46 % de utilización con ave completa); ~38.000 m² de galpones y ~53.000 pollitos/semana desde el inicio | Idem | Segunda línea o segundo turno | **Mayor**: capacidad ociosa inicial alta con la demanda actual | Menor |
| **D** façon → turnos → 2.ª línea | Convierte demanda C en A/B **antes** de construir (DEC-018); usa el segundo turno como palanca antes de la segunda línea; la misma línea sirve dos escalas | Depende de encontrar faena a façon o producto de terceros (DPV-006); el segundo turno exige personal y limpieza nocturna; margen de intermediación en la etapa 0 | Etapa 0 → planta: cuando la demanda A/B y la especificación estén probadas (G0); 1 → 2 turnos: G2; 2.ª línea: G3 | Personal por turno, frío, efluentes, docks; espacio para la 2.ª línea | Medio | Menor que A, porque la etapa 0 no inmoviliza planta |
| **E** obra grande, equipos por etapas | Evita obras con la planta operando; flujos higiénicos y servicios correctos desde el inicio | Inmoviliza capital en obra civil y servicios ociosos; si la demanda no llega, el edificio sobra | Cuando cada módulo de equipamiento se justifique (G1–G3) | Equipos, frío, corte, dotación | **Mayor** en obra civil; menor en equipos | Menor |

### 2.2 Lecturas

1. **No hay arquitectura "segura":** arrancar chico arriesga quedar bajo la escala mínima eficiente o sin capacidad cuando llega la demanda; arrancar grande arriesga capacidad ociosa con la demanda actual (C/D).
2. **La escala mínima eficiente es el dato que falta** para descartar A (2.500) o B (5.000) como primera etapa. Se estima con CAPEX y OPEX (fases posteriores; DPV-083).
3. **Las palancas baratas de crecimiento** (6.º día semanal: +20 %; segundo turno: ×2 sobre la misma línea) permiten que una planta pequeña o intermedia crezca **sin obra**, si se prevé personal, frío y efluentes. Por eso D y E combinan bien.
4. **La secuencia la debe fijar la evidencia**, no el capital disponible ni la capacidad de los líderes (reglas 7 y 8): cada ampliación pasa por un gate con métricas ([`gates_expansion.md`](gates_expansion.md)).
5. **La producción primaria tiene su propio ritmo de expansión:** ampliar requiere pollitos (reproductoras: ~6–7 meses), productores o galpones y alimento. La planta no puede crecer más rápido que su abastecimiento.

---

## 3. Matriz de decisión sin ganador (§18)

MENOR / MEDIA / MAYOR se usa **solo cuando la comparación es físicamente evidente**; si no, se indica la dirección y por qué no se ordena. **No hay puntuación ni recomendación.**

| Criterio | 2.500 | 5.000 | 10.000 | 20.000 | Base física / por qué |
|---|---|---|---|---|---|
| **Riesgo de demanda** (volumen a colocar frente a los escenarios actuales) | MENOR | MEDIA | MAYOR | MAYOR | Demanda necesaria para 100 %: 4,1 / 8,2 / 16,4 / 32,8 t/día calendario (M0) frente a escenarios de 1,5 / 7,5 / 23,5 t/día, todos C/D. 10.000 y 20.000 exceden el escenario base |
| **Facilidad de abastecimiento de aves** | MAYOR | MEDIA | MEDIA | MENOR | 13.200 → 105.600 pollitos/semana plena; 9.500 → 75.900 m² de galpón; 1–4 vs 8–32 productores equivalentes. La disponibilidad real en el radio de la planta es desconocida (DPV-047, DPV-048) |
| **Complejidad operativa** | MENOR | MEDIA | MEDIA | MAYOR | Aves, lotes, movimientos y flujos de subproductos ×8; ver tabla central |
| **Facilidad para valorizar subproductos** | Dirección: **aumenta con la escala** (sin ordinal) | | | | Más volumen regular interesa más a un receptor y habilita procesos propios (1,3 → 10,7 t/día de clase C), pero el umbral de interés de receptores y de un rendering propio **no está relevado** (DPV-065): no es evidente dónde cambia de categoría |
| **Posibilidad exportadora** (capacidad física de consolidar lotes) | MENOR | MEDIA | MEDIA | MAYOR | Días de faena para 25 t de pata-muslo: 15,2 / 7,6 / 3,8 / 1,9; de garras: 118 / 59 / 29 / 15. **No** incluye acceso sanitario, habilitación ni compradores, que no dependen de la escala |
| **Modularidad** (margen para crecer por módulos desde esa escala) | Dirección: **mayor al arrancar chico si se previó terreno y servicios** | | | | Depende del diseño (§1), no de la escala: una planta de 2.500 sin terreno no es modular; una de 10.000 con espacio para 2.º turno y 2.ª línea sí |
| **Dependencia de capital** (capital de trabajo físico: alimento de un ciclo e inventario de 7 días) | MENOR | MEDIA | MEDIA | MAYOR | 415 → 3.320 t de alimento por ciclo; 42 → 336 t de comestible en 7 días. **CAPEX no calculado**: el orden entre escalas es evidente en lo físico, no su magnitud monetaria |
| **Capacidad de crecer sin ampliar** (demanda adicional que puede absorber) | MENOR | MEDIA | MEDIA | MAYOR | Es la contracara del riesgo de demanda: la capacidad ociosa es margen de crecimiento **y** capital sin producir |

**Lectura:** cada criterio favorece a una escala distinta. Las escalas chicas minimizan riesgo de demanda, de abastecimiento y de capital; las grandes favorecen lotes de exportación, valorización de subproductos y margen de crecimiento. **La decisión depende de datos que no existen todavía** (demanda A/B, escala mínima eficiente, productores y pollitos disponibles, receptores de subproductos): ver [`conclusiones_escala.md`](conclusiones_escala.md) §4.
