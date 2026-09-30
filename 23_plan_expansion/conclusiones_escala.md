# Conclusiones — modelo preliminar de escala

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Base: [`escenarios_escala.md`](escenarios_escala.md), [`arquitectura_escalable.md`](arquitectura_escalable.md), [`gates_expansion.md`](gates_expansion.md), [`especificacion_simulador_html.md`](especificacion_simulador_html.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_escala.py`](modelo_escala.py), [`escenarios_escala.csv`](escenarios_escala.csv), [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md)

> **No se elige la escala.** No se calcula CAPEX, OPEX, precios ni indicadores financieros; no se selecciona maquinaria, proveedores, layout ni localización; no se construye el HTML. USD 2 M no se trata como suficiente ni como tope (regla 7).
> **Fuentes:** no se incorporaron fuentes externas nuevas. Todas las cifras derivan de los modelos existentes (producción v1.1, balance v1.1, subproductos v1.0) y de supuestos registrados; **ninguna es un dato de campo argentino**.

---

## 1. Hallazgos principales

1. **Con la evidencia actual ninguna escala está justificada:** la demanda documentada (A + B) es ~0, así que la utilización que respalda la evidencia es **0 %** en las cuatro escalas. Todo lo demás compara hipótesis C/D.
2. **Contra los escenarios de prueba**, la escala que "se llena" depende del escenario y del mix: el **conservador** (1,5 t/día) no llena ni 2.500 (37–65 %); el **base** (7,5 t/día) excede 2.500, ronda **5.000** (91 % con ave completa; 124–163 % con mix de supermercado) y deja 10.000 al **46–81 %**; el **expansivo** (23,5 t/día) recién acerca **20.000** (72 % con ave completa; 97–128 % con mix).
3. **Demanda necesaria para llenar cada escala** (cota inferior, vendiendo el ave completa): **4,1 / 8,2 / 16,4 / 32,8 t de producto por día calendario** (5 d/sem); con 6 d/sem, +20 %. Si todo pasara por los 90 locales: **46 / 91 / 182 / 365 kg/local/día**; 20.000 supera el extremo del rango de la red (300).
4. **El mix vale tanto como los kilos:** con los rendimientos del balance v1.1, los mixes de supermercado exigen **1,19–1,56 veces** las aves de la fórmula simple (1,36–1,78 frente al ave completa) y dejan **3,0–6,7 t/día de partes sin comprador** con el escenario base; aun con la planta "llena" sobran partes. La **pechuga** es la parte limitante en los tres mixes.
5. **Producción primaria (medio, 5 d):** 13.200 / 26.400 / 52.800 / 105.600 pollitos BB por semana plena; 9.500 / 19.000 / 37.900 / 75.900 m² de galpón (4 / 8 / 16 / 32 galpones de 2.400 m²); 3.100 / 6.200 / 12.400 / 24.700 t de alimento por año. El alimento es el mayor flujo físico del sistema y ocurre en las granjas.
6. **Ritmo de línea a 8 h netas:** 312 / 625 / 1.250 / 2.500 aves/h. La misma línea de 1.250 aves/h sirve 10.000 aves/día a un turno y 20.000 a dos: el **segundo turno** y el **sexto día** (+20 %) son palancas de crecimiento sin obra.
7. **Subproductos:** en todas las escalas son flujos **diarios** (perecederos). Lo que cambia es la naturaleza del problema: a 2.500–5.000 aves/día (1,3–3,0 t/día) es **conseguir un receptor** para volúmenes chicos; a 10.000 (5,3–8,6 t/día) es un **flujo industrial**; a 20.000 (10,7–17,3 t/día) la pregunta del rendering propio se vuelve pertinente (no decidida).
8. **Exportación:** la escala cambia la **capacidad de consolidar lotes**, no el acceso. Un contenedor de garras tarda ~118 días de faena a 2.500 aves/día y ~15 a 20.000; de pata-muslo, 15 y 2 días. Exportación = 0 en la demanda (SUP-022).
9. **Inventario y frío:** 7 días de comestible son 42 / 84 / 168 / 336 t; lo que más cambia el frío no es la escala sino el **perfil refrigerado/congelado/exportación** (P2 a 20.000 aves/día: ~270 t congeladas con 14 días).
10. **Arquitectura:** sobredimensionar lo barato de prever y caro de corregir (terreno, accesos, trazas, permisos, flujos higiénicos, troncales de servicios) y construir por módulos lo caro de tener ocioso (líneas, cámaras, salas de corte). Cinco arquitecturas comparadas **sin ganador**; la **escala mínima eficiente** es el dato que falta para descartar arranques chicos.

## 2. Tabla comparativa

Tabla central completa en [`escenarios_escala.md` §17](escenarios_escala.md). Síntesis (5 d/sem; config. B; 2,9 kg; utilización 100 % = punto de dimensionamiento):

| Variable | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves/año (5 d · 6 d) | 625.000 · 750.000 | 1,25 M · 1,5 M | 2,5 M · 3,0 M | 5,0 M · 6,0 M |
| t vivas/día | 7,3 | 14,5 | 29,0 | 58,0 |
| Pollitos BB/semana plena | 13.197 | 26.395 | 52.790 | 105.580 |
| m² de galpón | 9.486 | 18.971 | 37.943 | 75.885 |
| Alimento t/año | 3.091 | 6.181 | 12.362 | 24.724 |
| Producto comercial t/día | 6,0 | 12,0 | 24,0 | 47,9 |
| Rendering potencial t/día (B · C) | 1,3 · 2,2 | 2,7 · 4,3 | 5,3 · 8,6 | 10,7 · 17,3 |
| Ritmo a 8 h (aves/h) | 312 | 625 | 1.250 | 2.500 |
| Inventario 7 días (t) | 42 | 84 | 168 | 336 |
| Demanda para 100 % (t/día cal) | 4,1 | 8,2 | 16,4 | 32,8 |
| Utilización con escenario base (M0 · M1–M3) | 183 % · 248–326 % | 91 % · 124–163 % | 46 % · 62–81 % | 23 % · 31–41 % |

## 3. Qué debe ser verdad en cada escala

Ver [`escenarios_escala.md` §17](escenarios_escala.md) (tabla "debe ser verdad que…") y la matriz sin ganador en [`arquitectura_escalable.md` §3](arquitectura_escalable.md).

## 4. Información que nos falta (priorizada)

Acumulada en [`../00_gestion_proyecto/datos_por_validar.md`](../00_gestion_proyecto/datos_por_validar.md) (anotación "escala 2026-09-30" en cada registro). **No** se prepara todavía el cuestionario maestro de inversores.

### 4.1 CRÍTICO ANTES DE DEFINIR ESCALA

| # | Dato | Por qué cambia la escala | Registro |
|---|---|---|---|
| 1 | **Compras reales de los supermercados** (kg/semana por local, 12 meses) | Mueve la demanda ×12 (25–300 kg/local/día): de "2.500 sobra" a "20.000 no alcanza" | DPV-003 |
| 2 | **Mix real** por producto (entero, pechuga, pata-muslo, alas, milanesas, menudencias; refrigerado/congelado) | Aves necesarias ×1,2–1,8 y excedentes de partes | DPV-037, DPV-085 |
| 3 | **Contratos / evidencia de compromiso** (reunión con compras, piloto, carta de intención) y proveedor actual | Única forma de pasar de C a B/A | DPV-002, DPV-020, DPV-038 |
| 4 | **Demanda de otros canales** para las partes que la red no compra (pata-muslo, alas, carcasa, garras, menudencias) | Sin ellos, el excedente de partes limita la escala útil | DPV-040, DPV-070 |
| 5 | **Escala mínima eficiente** de una planta de faena en Argentina | Decide si 2.500 o 5.000 son arranques posibles | DPV-083 |
| 6 | **Productores integrables** y **pollitos BB** disponibles en zonas candidatas | La planta no puede crecer más rápido que su abastecimiento | DPV-048, DPV-047 |
| 7 | **Faena a façon / producto de terceros** para una etapa 0 | Permite validar demanda sin planta (arquitectura D) | DPV-006 |

### 4.2 IMPORTANTE ANTES DE INVERTIR

| # | Dato | Registro |
|---|---|---|
| 8 | **Precio** por producto y canal y **condiciones de pago** (capital de trabajo) | DPV-013, DPV-039 |
| 9 | **Alimento** en zonas candidatas (precio, fábricas, logística) | DPV-050 |
| 10 | **Compradores de carcasa-esqueleto** y CMS | DPV-071 |
| 11 | **Rendering** y receptores de sangre y subproductos (volumen mínimo, distancia, condiciones) | DPV-065, DPV-080 |
| 12 | **Terreno** con reserva para expansión y **disponibilidad de servicios** (potencia, agua, gas, permiso de vuelco) | DPV-087, DPV-052, DPV-053 |
| 13 | **Plazos** de obra, equipos y habilitación SENASA para cada ampliación | DPV-086 |
| 14 | Monto y condiciones reales del capital | DPV-001 |
| 15 | Requisitos de alta de proveedor y habilitación exigida por clientes | DPV-041 |
| 16 | Logística de la red (CD vs locales) y costos de distribución | DPV-036, DPV-042 |

### 4.3 ÚTIL PARA OPTIMIZAR

| # | Dato | Registro |
|---|---|---|
| 17 | **Exportadores / traders** que consoliden partes (garras, menudencias, alas) | DPV-081, DPV-032 |
| 18 | Horas netas por turno y convenio (segundo turno) | DPV-082 |
| 19 | Capacidades útiles de vehículos (vivo, refrigerado, alimento, subproductos) | DPV-084 |
| 20 | Desempeño productivo de campo (mortalidad, FCR, peso) | DPV-044 |
| 21 | Ensayo de balance de masa en planta argentina | DPV-060 |
| 22 | Vida útil comercial por producto y envase (define días de inventario refrigerado) | DPV-078 |

## 5. Qué quedó preparado para el HTML v0.1

[`especificacion_simulador_html.md`](especificacion_simulador_html.md): 17 inputs (escala, días/semana, días/año, horas netas, peso, edad, mortalidad, FCR, utilización, escenario y método de demanda, configuración, días de inventario, perfil de destino, abastecimiento, m² por productor, capacidades de vehículos), 11 grupos de outputs, 4 vistas, 11 alertas de inconsistencia, comparador de escenarios A/B/C lado a lado y campos CAPEX/OPEX/EBITDA/VAN/TIR/payback **previstos y deshabilitados**. La fuente de verdad es `escenarios_escala.csv` (bloque `tabla_central` como núcleo); se propone exportar un archivo de coeficientes desde el modelo para que el HTML no duplique fórmulas.

## 6. Resultado de tests

`python3 23_plan_expansion/modelo_escala.py --solo-tests` → **17/17 correctos**. Los modelos importados siguen intactos: producción 10/10 grupos de pruebas, balance v1.1 21/21, subproductos 9/9; sus CSV no se reescriben ni cambian.

| Test | Qué verifica | Resultado |
|---|---|---|
| T00 / T00b | Modelos importados intactos; escalas, peso y calendarios coherentes entre modelos | OK |
| T01 | Duplicar aves/día duplica toda variable física lineal (2.272 variables; días de contenedor a la mitad) | OK |
| T02 | 100 % de utilización nunca procesa menos que 50 % (120 series monótonas y proporcionales) | OK |
| T03 | 6 días/semana > 5 días/semana en volúmenes anuales, semanales y diarios calendario (428 variables) | OK |
| T04 | Pollitos alojados > aves cargadas > aves faenadas con mortalidad | OK |
| T05 | Masas de productos y subproductos = balance v1.1 (recalculado) = CSV de 07_subproductos | OK |
| T06 | Subproductos no duplicados: cada componente en un ítem y una clase; Σ = PV + agua; alternativas y agregados no sumables | OK |
| T07 | Inventario = producción diaria × días; perfiles suman 100 % | OK |
| T08 | Ninguna variable física negativa ni no finita (3.360 valores) | OK |
| T09 | Unidades consistentes (t, t/año, vivo > comercial, unidades válidas) | OK |
| T10 | Semana plena y promedio anual no se mezclan; días/año no alteran la semana plena; envoltorio = modelo de producción | OK |
| T11 | Ninguna cifra económica (precio, costo, CAPEX, OPEX, margen, moneda) | OK |
| T12 | Capacidad ≠ demanda: triplicar la demanda no cambia ninguna variable de capacidad; demanda C/D y exportación 0 | OK |
| T13 | Mixes leídos de `supermercados.md`; masa producida = demandada + excedentes; parte limitante ≥ ave completa; cierre a plena escala | OK |
| T14 | La utilización es variable (30–100 %), no un supuesto de 100 % | OK |
| T15 | Entradas inválidas detienen el modelo | OK |

**Pruebas de mutación** (`--mutaciones`): **14/14 detectadas** — escalado no lineal (T01, T05, T06), utilización invertida (T02), 6 días con 250 días/año (T03, T10), pollitos sin mortalidad (T04), pechuga no tomada del balance (T05, T06), vísceras duplicadas en dos ítems (T06), inventario × (días + 1) (T07), demanda insatisfecha negativa (T08), kg ↔ t mal convertidos (T09), semana plena reemplazada por promedio (T04, T10), cifra económica agregada (T01, T03, T11), capacidad igualada a la demanda (T12, T14), CMS alternativa sumada como producto (T06), días/año que alteran la semana plena (T10). Durante la construcción, la mutación económica reveló un defecto real del test T11 (el guion bajo impedía detectar `precio_usd`), que se corrigió.

## 7. Control de calidad

- [x] Demanda potencial ≠ demanda asegurada: utilización documentada 0 %; escenarios C/D, `sumable = no`, exportación 0.
- [x] Capacidad ≠ ventas: la demanda se compara, nunca define la capacidad (T12).
- [x] Ningún escenario supone automáticamente 100 % de utilización (T14; 100 % rotulado como punto de dimensionamiento).
- [x] Sin precios, sin CAPEX, sin OPEX (T11).
- [x] Sin maquinaria, sin ubicación, sin layout.
- [x] Modelos anteriores intactos (T00; CSV previos sin cambios en git).
- [x] Balance v1.1 sin modificar; rendimientos importados (T05).
- [x] Toneladas vivas y comerciales en columnas `base` distintas; nunca sumadas.
- [x] Rutas incompatibles no sumadas (CMS alternativa y agregados no sumables; T06).
- [x] Trazabilidad: columna `fuente_modelo` en cada fila; tabla de origen en `escenarios_escala.md` §20.
- [x] Contenedor de 25 t marcado `[PVDP · débil]` (FTE-135).
- [ ] Datos de campo argentinos (ninguno disponible).

## 8. Archivos

**Creados:** `23_plan_expansion/escenarios_escala.md`, `arquitectura_escalable.md`, `gates_expansion.md`, `modelo_escala.py`, `escenarios_escala.csv`, `especificacion_simulador_html.md`, `guia_ramiro.md`, `conclusiones_escala.md`; `05_proceso_industrial/capacidad_preliminar.md`.
**Modificados:** `23_plan_expansion/README.md`, `05_proceso_industrial/README.md`; `00_gestion_proyecto/supuestos.md` (SUP-052 a SUP-059), `datos_por_validar.md` (DPV-082 a DPV-087 y anotaciones de prioridad), `decisiones_pendientes.md` (DEC-033 a DEC-036 y notas en DEC-001, DEC-002, DEC-004, DEC-014, DEC-018, DEC-020), `estado_proyecto.md`, `glosario.md`. `25_fuentes/` sin cambios (no hubo fuentes externas nuevas).

## 9. Evaluación de calidad

**MEDIA** como modelo integrador y método (reproducible, trazable a los tres modelos previos sin duplicar fórmulas, 17 tests y 14 mutaciones detectadas, separación estricta de capacidad/demanda, vivo/comercial y semana plena/promedio); **BAJA** como evidencia para decidir la escala (cero datos de campo; demanda hipotética; escala mínima eficiente, productores, pollitos y receptores desconocidos). Sirve para **saber qué preguntar y qué tiene que ser verdad**, no para elegir la escala.
