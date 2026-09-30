# Conclusiones — modelo preliminar de escala

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual final: ver §0) · Base: [`escenarios_escala.md`](escenarios_escala.md), [`arquitectura_escalable.md`](arquitectura_escalable.md), [`gates_expansion.md`](gates_expansion.md), [`especificacion_simulador_html.md`](especificacion_simulador_html.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_escala.py`](modelo_escala.py), [`escenarios_escala.csv`](escenarios_escala.csv), [`../05_proceso_industrial/capacidad_preliminar.md`](../05_proceso_industrial/capacidad_preliminar.md)

> **No se elige la escala.** No se calcula CAPEX, OPEX, precios ni indicadores financieros; no se selecciona maquinaria, proveedores, layout ni localización; no se construye el HTML (se construyó después como v0.1 en `simulador_html/`, sesión 09D). USD 2 M no se trata como suficiente ni como tope (regla 7).
> **Fuentes:** no se incorporaron fuentes externas nuevas. Todas las cifras derivan de los modelos existentes (producción v1.1, balance v1.1, subproductos v1.0) y de supuestos registrados; **ninguna es un dato de campo argentino**.

---

## 0. Auditoría conceptual v1.1 (2026-09-30)

Correcciones de **definiciones** antes de usar el modelo como base del simulador. Ninguna cifra física (aves, pollitos, m², alimento, productos, subproductos) cambió; cambiaron los nombres, las métricas de demanda/capacidad y las bases temporales del inventario.

| # | Problema | Corrección |
|---|---|---|
| 1 | Se llamaba "utilización" a valores como 183 %, 326 %, 573 % o 1.021 % | Tres métricas separadas (SUP-060): **factor demanda/capacidad** (puede superar 100 %), **utilización de planta** (0–100 %; si la demanda excede, 100 % y el resto es **demanda no atendida**) y **cobertura de demanda** (0–100 %); más kg atendidos, kg no atendidos y capacidad ociosa |
| 2 | Riesgo de comparar t/día de faena con t/día calendario | Funciones `convertir` y `cociente`: la comparación sin conversión se **rechaza** (test T18, mutaciones M17–M18). Producción mostrada por día operativo, por día calendario promedio y por año |
| 3 | "7 días = 168 t" podía leerse como 7 días calendario | Dos bases: **días de producción** (168 t a 10.000 aves/día) y **días calendario de cobertura** (115 t con 250 días; 138 t con 300) |
| 4 | "Producto comestible t/día" sin decir qué contiene | Es **peso comercial** = masa biológica (23,11 t a 10.000 aves/día) + agua retenida (0,86 t); ambas se muestran; el agua nunca es carne (test T20) |
| 5 | "Segundo turno = 20.000 sin obra" | Es **capacidad teórica de la línea** con 16 h netas; la de la planta depende de 17 sistemas a verificar |
| 6 | Sexto día confundido con capacidad diaria | +20 % de **volumen anual** con la **misma capacidad diaria** (test T19) |
| 7 | "Entran 29 t y salen 24 t → cerca de las granjas" | Reformulado como **hipótesis a estudiar** con criterios de transporte de aves vivas, bienestar, mortalidad, merma, bioseguridad, productores, costos, caminos, mercados, servicios, efluentes y exportación (DEC-003) |
| 8 | Escala mínima eficiente usada para "descartar arranques chicos" | Dato crítico **pendiente** (DPV-083); no se concluye que 2.500 sea chico ni 20.000 grande |

## 1. Hallazgos principales

1. **Con la evidencia actual ninguna escala está justificada:** la demanda documentada (A + B) es ~0, así que la utilización que respalda la evidencia es **0 %** en las cuatro escalas. Todo lo demás compara hipótesis C/D.
2. **Contra los escenarios de prueba** (factor demanda/capacidad, 5 d/sem): el **conservador** (1,5 t/día) deja todas las escalas con capacidad ociosa (utilización de 2.500: 37–65 %); el **base** (7,5 t/día) **excede** 2.500 (factor 183–326 %: utilización 100 %, cobertura 31–55 %), ronda **5.000** (factor 91 % con ave completa; 124–163 % con mix) y deja 10.000 con **utilización 46–81 %**; el **expansivo** (23,5 t/día) excede 10.000 (factor 143–255 %; cobertura 39–70 %) y recién acerca **20.000** (utilización 72 % con ave completa; factor 97–128 % con mix).
3. **Demanda necesaria para llenar cada escala** (cota inferior, vendiendo el ave completa): **4,1 / 8,2 / 16,4 / 32,8 t de peso comercial por día calendario** (= 6,0 / 12,0 / 24,0 / 47,9 t por día de faena × 250/365); con 6 d/sem, +20 %. Si todo pasara por los 90 locales: **46 / 91 / 182 / 365 kg/local/día**; 20.000 supera el extremo del rango de la red (300).
4. **El mix vale tanto como los kilos:** con los rendimientos del balance v1.1, los mixes de supermercado exigen **1,19–1,56 veces** las aves de la fórmula simple (1,36–1,78 frente al ave completa) y dejan **3,0–6,7 t/día de partes sin comprador** con el escenario base; aun con la planta "llena" sobran partes. La **pechuga** es la parte limitante en los tres mixes.
5. **Producción primaria (medio, 5 d):** 13.200 / 26.400 / 52.800 / 105.600 pollitos BB por semana plena; 9.500 / 19.000 / 37.900 / 75.900 m² de galpón (4 / 8 / 16 / 32 galpones de 2.400 m²); 3.100 / 6.200 / 12.400 / 24.700 t de alimento por año. El alimento es el mayor flujo físico del sistema y ocurre en las granjas.
6. **Ritmo de línea a 8 h netas:** 312 / 625 / 1.250 / 2.500 aves/h. Una línea de 1.250 aves/h equivale a 10.000 aves/día con 8 h netas y, **en teoría**, a 20.000 con 16 h netas (dos turnos): es **capacidad teórica de la línea**, sujeta a verificar recepción, colgado, eviscerado, chilling, corte, mano de obra, cámaras, congelado, expedición, agua, efluentes, energía, refrigeración, limpieza, mantenimiento, bienestar y logística de granjas. El **sexto día** (250 → 300 días/año) agrega ~20 % de **volumen anual** con la **misma capacidad diaria**. Ninguna de las dos se afirma como crecimiento "sin obra".
7. **Subproductos:** en todas las escalas son flujos **diarios** (perecederos). Lo que cambia es la naturaleza del problema: a 2.500–5.000 aves/día (1,3–3,0 t/día) es **conseguir un receptor** para volúmenes chicos; a 10.000 (5,3–8,6 t/día) es un **flujo industrial**; a 20.000 (10,7–17,3 t/día) la pregunta del rendering propio se vuelve pertinente (no decidida).
8. **Exportación:** la escala cambia la **capacidad de consolidar lotes**, no el acceso. Un contenedor de garras tarda ~118 días de faena a 2.500 aves/día y ~15 a 20.000; de pata-muslo, 15 y 2 días. Exportación = 0 en la demanda (SUP-022).
9. **Inventario y frío:** 7 **días de producción** en stock son 42 / 84 / 168 / 336 t; 7 **días calendario** de cobertura, 29 / 57 / 115 / 230 t con 250 días de faena (34 / 69 / 138 / 276 con 300); lo que más cambia el frío no es la escala sino el **perfil refrigerado/congelado/exportación** (P2 a 20.000 aves/día: ~270 t congeladas con 14 días).
10. **Arquitectura:** sobredimensionar lo barato de prever y caro de corregir (terreno, accesos, trazas, permisos, flujos higiénicos, troncales de servicios) y construir por módulos lo caro de tener ocioso (líneas, cámaras, salas de corte). Cinco arquitecturas comparadas **sin ganador**. La **escala mínima eficiente** es un dato crítico pendiente (DPV-083): no se concluye que 2.500 sea demasiado chico ni que 20.000 sea demasiado grande; surgirá de maquinaria, turnos, dotación, CAPEX, OPEX, servicios y utilización.
11. **Localización respecto de las granjas: hipótesis a estudiar.** No se usa la relación de masas (29 t vivas entran, 24 t comerciales salen) como argumento; se analizará con tiempo de transporte de aves vivas, bienestar, mortalidad, merma, bioseguridad, productores, costo logístico, caminos, mercados, servicios, efluentes y exportación (DEC-003).

## 2. Tabla comparativa

Tabla central completa en [`escenarios_escala.md` §17](escenarios_escala.md). Síntesis (5 d/sem; config. B; 2,9 kg; utilización 100 % = punto de dimensionamiento):

| Variable | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Aves/año (5 d · 6 d) | 625.000 · 750.000 | 1,25 M · 1,5 M | 2,5 M · 3,0 M | 5,0 M · 6,0 M |
| t vivas/día | 7,3 | 14,5 | 29,0 | 58,0 |
| Pollitos BB/semana plena | 13.197 | 26.395 | 52.790 | 105.580 |
| m² de galpón | 9.486 | 18.971 | 37.943 | 75.885 |
| Alimento t/año | 3.091 | 6.181 | 12.362 | 24.724 |
| Comestible: masa biológica t/día operativo | 5,8 | 11,6 | 23,1 | 46,2 |
| Comestible: agua retenida t/día operativo (no es carne) | 0,2 | 0,4 | 0,9 | 1,7 |
| Comestible: peso comercial t/día operativo | 6,0 | 12,0 | 24,0 | 47,9 |
| Peso comercial t/día calendario (250 d · 300 d) | 4,1 · 4,9 | 8,2 · 9,8 | 16,4 · 19,7 | 32,8 · 39,4 |
| Rendering potencial t/día (B · C) | 1,3 · 2,2 | 2,7 · 4,3 | 5,3 · 8,6 | 10,7 · 17,3 |
| Ritmo a 8 h (aves/h) | 312 | 625 | 1.250 | 2.500 |
| Inventario 7 días de producción · 7 días calendario (t, 250 d) | 42 · 29 | 84 · 57 | 168 · 115 | 336 · 230 |
| Demanda para 100 % (t peso comercial/día cal) | 4,1 | 8,2 | 16,4 | 32,8 |
| Escenario base M0: factor · utilización · cobertura | 183 · 100 · 55 % | 91 · 91 · 100 % | 46 · 46 · 100 % | 23 · 23 · 100 % |
| Escenario base M1–M3: factor · utilización · cobertura | 248–326 · 100 · 31–40 % | 124–163 · 100 · 61–81 % | 62–81 · 62–81 · 100 % | 31–41 · 31–41 · 100 % |
| Escenario base M0: kg/día cal no atendidos · capacidad ociosa (aves/día op.) | 3.396 · 0 | 0 · 431 | 0 · 5.431 | 0 · 15.431 |

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
| 5 | **Escala mínima eficiente** de una planta de faena en Argentina (requiere maquinaria, turnos, dotación, CAPEX, OPEX, servicios y utilización) | Permite evaluar si cada escala es un arranque posible; hoy no se concluye nada sobre 2.500 ni sobre 20.000 | DPV-083 |
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

[`especificacion_simulador_html.md`](especificacion_simulador_html.md): 17 inputs (escala, días/semana, días/año, horas netas, peso, edad, mortalidad, FCR, utilización, escenario y método de demanda, configuración, días de inventario **con su base temporal**, perfil de destino, abastecimiento, m² por productor, capacidades de vehículos), grupos de outputs, 4 vistas, 11 alertas de inconsistencia, comparador de escenarios A/B/C lado a lado y campos CAPEX/OPEX/EBITDA/VAN/TIR/payback **previstos y deshabilitados**. Tras la auditoría v1.1 se agregó una tabla (§2.1) de **12 outputs que la interfaz nunca debe confundir**: utilización de capacidad (0–100 %), factor demanda/capacidad (puede superar 100 %), cobertura de demanda (0–100 %), demanda no atendida, capacidad ociosa, producción por día operativo, producción promedio por día calendario, inventario en días de producción, inventario en días calendario, masa biológica, agua incorporada y peso comercial. La fuente de verdad es `escenarios_escala.csv`.

## 6. Resultado de tests

`python3 23_plan_expansion/modelo_escala.py --solo-tests` → **23/23 correctos**. Los modelos importados siguen intactos: producción 10/10 grupos de pruebas, balance v1.1 21/21, subproductos 9/9; sus CSV no se reescriben ni cambian.

| Test | Qué verifica | Resultado |
|---|---|---|
| T00 / T00b | Modelos importados intactos; escalas, peso y calendarios coherentes entre modelos | OK |
| T01 | Duplicar aves/día duplica toda variable física lineal (2.752 variables; días de contenedor a la mitad) | OK |
| T02 | 100 % de utilización nunca procesa menos que 50 % (120 series monótonas y proporcionales) | OK |
| T03 | 6 días/semana > 5 días/semana en volúmenes anuales, semanales y diarios calendario (436 variables) | OK |
| T04 | Pollitos alojados > aves cargadas > aves faenadas con mortalidad | OK |
| T05 | Masas de productos y subproductos = balance v1.1 (recalculado) = CSV de 07_subproductos | OK |
| T06 | Subproductos no duplicados: cada componente en un ítem y una clase; Σ = PV + agua; alternativas y agregados no sumables | OK |
| T07 | Inventario = flujo diario de su base temporal × días; perfiles suman 100 % | OK |
| T08 | Ninguna variable física negativa ni no finita (4.224 valores) | OK |
| T09 | Unidades consistentes (t, t/año, vivo > comercial, unidades válidas) | OK |
| T10 | Semana plena y promedio anual no se mezclan; días/año no alteran la semana plena; envoltorio = modelo de producción | OK |
| T11 | Ninguna cifra económica (precio, costo, CAPEX, OPEX, margen, moneda) | OK |
| T12 | Capacidad ≠ demanda: triplicar la demanda no cambia ninguna variable de capacidad; demanda C/D y exportación 0 | OK |
| T13 | Mixes leídos de `supermercados.md`; masa producida = demandada + excedentes; parte limitante ≥ ave completa; cierre con cobertura | OK |
| T14 | La utilización es variable (30–100 %), no un supuesto de 100 % | OK |
| T15 | Entradas inválidas detienen el modelo | OK |
| **T16** | Utilización de planta y cobertura de demanda nunca > 100 %; utilización = mín(factor; 100 %); el factor demanda/capacidad sí supera 100 % (96 casos; máx. 1.021 %) y ninguna otra variable en % lo hace | OK |
| **T17** | Si demanda > capacidad: kg no atendidos > 0, aves faltantes > 0, utilización 100 %, sin capacidad ociosa (41 casos); si capacidad > demanda: capacidad ociosa > 0, cobertura 100 %, nada sin atender (55 casos); atendidos + no atendidos = demanda | OK |
| **T18** | Comparar t/día de faena con t/día calendario sin convertir **se rechaza** (`cociente`); factor = aves requeridas ÷ (escala × días/365); producción día calendario = día operativo × días/365 y anual = día operativo × días = día calendario × 365; etiquetas de período coherentes | OK |
| **T19** | 300 días/año = +20 % de volumen anual que 250 con las mismas aves/día; cambiar los días/año (250 ↔ 300 con 6 d/sem) no cambia ninguna variable por día operativo ni por hora | OK |
| **T20** | Masa biológica comestible idéntica con 6 % u 8 % de absorción de agua; peso comercial = masa biológica + agua retenida | OK |
| **T21** | Todo inventario declara su base temporal (672 filas); 7 días calendario = 7 días de producción × días/365 < 7 días de producción | OK |

**Pruebas de mutación** (`--mutaciones`): **22/22 detectadas.**

| Mutación introducida | Detectada por |
|---|---|
| M01 escalado no lineal | T01, T05, T06 |
| M02 utilización invertida (E / u) | T02 |
| M03 6 días/semana con 250 días/año | T03, T10, T19 |
| M04 pollitos sin mortalidad | T04 |
| M05 pechuga no tomada del balance | T05, T06 |
| M06 vísceras duplicadas en dos ítems | T06 |
| M07 inventario × (días + 1) | T07 |
| M08 demanda no atendida negativa | T08, T17 |
| M09 kg ↔ t mal convertidos | T09 |
| M10 semana plena reemplazada por promedio | T04, T10 |
| M11 cifra económica agregada | T01, T03, T11 |
| M12 capacidad igualada a la demanda | T12, T14, T16, T17, T18 |
| M13 CMS alternativa sumada como producto | T06 |
| M14 días/año que alteran la semana plena | T10 |
| **M15** utilización sin tope de 100 % | T08, T16, T17 |
| **M16** cobertura sin tope de 100 % | T08, T13, T16, T17 |
| **M17** capacidad por día de faena comparada con demanda calendario sin convertir | T18 |
| **M18** comparación directa de períodos distintos | El modelo se detiene (`cociente`: "dia_calendario contra dia_operativo sin conversión") |
| **M19** inventario calendario sin conversión | T07, T21 |
| **M20** inventario sin base temporal (todo rotulado como días de producción) | El modelo se detiene (filas ambiguas) |
| **M21** el sexto día aumenta la capacidad diaria | T09, T19 |
| **M22** agua retenida contada como masa biológica | T20 |

En la versión 1.0, la mutación económica reveló un defecto real del test T11 (el guion bajo impedía detectar `precio_usd`), que se corrigió.

## 7. Control de calidad

- [x] Demanda potencial ≠ demanda asegurada: utilización documentada 0 %; escenarios C/D, `sumable = no`, exportación 0.
- [x] Capacidad ≠ ventas: la demanda se compara, nunca define la capacidad (T12).
- [x] Ningún escenario supone automáticamente 100 % de utilización (T14; 100 % rotulado como punto de dimensionamiento).
- [x] La utilización nunca supera 100 %; el exceso de demanda aparece como factor demanda/capacidad y demanda no atendida (T16, T17).
- [x] Día operativo, día calendario y año separados; comparación sin conversión rechazada (T18); sexto día ≠ capacidad diaria (T19).
- [x] Inventario con base temporal explícita (T21); masa biológica separada del agua retenida y del peso comercial (T20).
- [x] Segundo turno presentado solo como capacidad teórica de la línea; localización cerca de granjas como hipótesis; escala mínima eficiente sin conclusión.
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

**Creados (v1.0):** `23_plan_expansion/escenarios_escala.md`, `arquitectura_escalable.md`, `gates_expansion.md`, `modelo_escala.py`, `escenarios_escala.csv`, `especificacion_simulador_html.md`, `guia_ramiro.md`, `conclusiones_escala.md`; `05_proceso_industrial/capacidad_preliminar.md`.
**Modificados (v1.0):** `23_plan_expansion/README.md`, `05_proceso_industrial/README.md`; `00_gestion_proyecto/supuestos.md` (SUP-052 a SUP-059), `datos_por_validar.md` (DPV-082 a DPV-087 y anotaciones de prioridad), `decisiones_pendientes.md` (DEC-033 a DEC-036 y notas en DEC-001, DEC-002, DEC-004, DEC-014, DEC-018, DEC-020), `estado_proyecto.md`, `glosario.md`.
**Modificados en la auditoría v1.1:** `modelo_escala.py` (v1.1), `escenarios_escala.csv` (regenerado: 4.232 filas), `escenarios_escala.md`, `arquitectura_escalable.md`, `gates_expansion.md`, `especificacion_simulador_html.md`, `guia_ramiro.md`, `conclusiones_escala.md`, `README.md` de la carpeta; `05_proceso_industrial/capacidad_preliminar.md`; `00_gestion_proyecto/supuestos.md` (SUP-060; notas en SUP-052, SUP-053, SUP-056), `decisiones_pendientes.md` (notas en DEC-001, DEC-003, DEC-036), `datos_por_validar.md` (DPV-083), `glosario.md`, `estado_proyecto.md`. `25_fuentes/` sin cambios.

## 9. Evaluación de calidad

**MEDIA** como modelo integrador y método (reproducible, trazable a los tres modelos previos sin duplicar fórmulas, 23 tests y 22 mutaciones detectadas, separación estricta de capacidad/demanda, utilización/factor/cobertura, día operativo/día calendario, masa biológica/peso comercial y semana plena/promedio); **BAJA** como evidencia para decidir la escala (cero datos de campo; demanda hipotética; escala mínima eficiente, productores, pollitos y receptores desconocidos). Sirve para **saber qué preguntar y qué tiene que ser verdad**, no para elegir la escala.
