# Auditoría final y reconciliación integral del motor v1

**Fecha:** 2026-10-05 · **Sesión:** 21 — auditoría + reconciliación final integral (cierre técnico, económico y metodológico A–Z) · **Rama:** `ccr-d71882bf-2idq1i` (desde `main` 7779a8f)

> **Qué es:** una auditoría del proyecto como **un único sistema** (datos → demanda → producción → balance → proceso → utilities → logística → localización → layout → RR. HH./upstream → CAPEX → OPEX → CT → finanzas → riesgo → optimización → decisión). **No** agrega un motor, **no** completa faltantes, **no** inventa precios ni demanda, **no** cierra decisiones de negocio y **no** recomienda una inversión. Solo se hicieron reconciliaciones, centralización de IDs, correcciones de nomenclatura e interfaz, dos correcciones inequívocas, documentación, tests y controles de integridad.

---

## 1. Objetivo

Responder si todo lo construido es internamente coherente: mismo idioma y definiciones entre módulos, ausencia de doble conteos, supuestos ocultos, universos o unidades incompatibles, faltantes convertidos en cero, simulaciones presentadas como evidencia; si C0–CF significan lo mismo en todos los módulos; si el financiero consume realmente los motores anteriores; si el optimizador compara alternativas comparables; qué está terminado, qué sigue pendiente de validación real y si el motor está listo para alimentar la app v1.

## 2. Alcance

| Incluido | Excluido (por instrucción) |
|---|---|
| Módulos 01–25 y registros de `00_gestion_proyecto/` | Nuevo motor económico; app; PowerPoint; "Biblia del pollo"; PFI; PR |
| Reconciliación de las sesiones 19 y 20 ([`reconciliacion_sesiones_19_20.md`](reconciliacion_sesiones_19_20.md)) | Completar precios, demanda, CAPEX, OPEX o financiamiento |
| Tests de integración y mutaciones entre módulos ([`tests_integracion_motor.py`](tests_integracion_motor.py)) | Cerrar decisiones (DEC) o validar DPV |
| Tablas finales: [`arquitecturas_maestras.csv`](arquitecturas_maestras.csv), [`tensiones_finales.csv`](tensiones_finales.csv), [`completitud_final_motor.csv`](completitud_final_motor.csv), [`trazabilidad_end_to_end.csv`](trazabilidad_end_to_end.csv), [`cobertura_motor.csv`](cobertura_motor.csv), [`registro_tests_final.csv`](registro_tests_final.csv) | Elevar E4/`[PVDP]` a evidencia; asumir USD 2 M o los 90 supermercados |
| Contrato de la app ([`interfaz_app_v1.md`](interfaz_app_v1.md)) y plan de validación ([`plan_validacion_final.md`](plan_validacion_final.md)) | Diseñar la app |

## 3. Arquitectura del sistema

```
02 demanda (escenarios de prueba; A+B ≈ 0) ─────────────────────────────────────────────┐
03 producción primaria → 14/15 upstream (pollitos idénticos a 03) ──┐                    │
04 balance de masa (rutas exclusivas; agua aparte) → 06/07 productos │                    │
23 escala (aves/día operativo × 250|300 d) ──────────────────────────┤                    │
05 proceso · 08 maquinaria · 11/12 utilities · 09 layout · 13 logística · 18 RR. HH. ────┤ drivers físicos
10 localización (gates; sin ranking) · 16 normativa (requisitos)                          │
                                                                                         ▼
19 CAPEX (BOQ por arquitectura y escala) ─┐   20 OPEX + CT (registro por concepto; propiedad del stock)
                                          └──────────────┬───────────────────────────────┘
                                 21 modelo financiero: construir_entrada() → simular() → resultados()
                                 (EVIDENCIA | ESCENARIO; demanda → utilización → ventas → EBITDA → ΔCT → FCFF → FCFE → VAN/TIR)
                                                         │
                                 22 riesgo (shocks sobre copia) + optimizador (Evaluador = 21)
                                                         │
                                 decisión: rankings por objetivo, Pareto, robustez, NO_INVERTIR_AUN, qué hacer ahora
```

Un solo `preset()` (19) define C0–CF; OPEX (20) lo consume vía `config_opex()`; el financiero (21) usa `configs()` que devuelve **los dos** con los mismos inputs; el optimizador (22) construye cada alternativa con `construir_entrada()` y la evalúa con `simular()` + `resultados()`. Trazabilidad variable por variable en [`trazabilidad_end_to_end.csv`](trazabilidad_end_to_end.csv).

## 4. Estado de cada módulo

Detalle en [`completitud_final_motor.csv`](completitud_final_motor.csv) (25 módulos). Síntesis: **todos** los módulos del motor están **terminados estructuralmente** y pasan sus suites; **ninguno** está validado con datos reales; `LISTO_DECISION_REAL = FALSE` en los 25. Exportación es **módulo futuro de mercado**; el simulador HTML v0.1 es físico y no es la app v1.

## 5. Reconciliación de IDs

| Registro | Antes | Después | Altas | Consolidaciones / fusiones / reclasificaciones |
|---|---|---|---|---|
| Supuestos | SUP-188 | **SUP-235** | 47 (SUP-189 a SUP-235) | 2 consolidadas (SUP-060, SUP-181); 8 propuestas fusionadas de a pares |
| Datos por validar | DPV-177 | **DPV-180** | 3 (DPV-178 a DPV-180) | 15 consolidadas en 13 DPV; 1 fusión; 2 reclasificadas (TF-001, DEC-103) |
| Decisiones | DEC-092 | **DEC-104** | 12 (DEC-093 a DEC-104) | 4 consolidadas (DEC-006, 007, 034, 084) |
| Fuentes | FTE-322 | **FTE-322** | 0 | FTE-004 y FTE-032 anotadas como referencias E4 no usables de 21 |
| Matriz de campo | 177 filas | 180 filas | 3 | — |

Mapa provisional → central en [`reconciliacion_sesiones_19_20.md`](reconciliacion_sesiones_19_20.md) §2. **0 IDs provisionales activos** (test ID01); solo permanecen en archivos históricos marcados (`actualizaciones_gestion_*.md`, `fuentes_*.csv`) y en los documentos de reconciliación. IDs centrales únicos y correlativos (ID02); toda referencia SUP/DPV/DEC/FTE/TF de los archivos activos existe en su registro (ID03); cada DPV tiene fila en la matriz de campo (ID04). Estados: 235 SUP (231 vigentes, 4 en revisión, 0 validados) · 180 DPV (0 validados) · 104 DEC (104 abiertas).

## 6. Demanda

| Categoría | Definición en el motor | Uso en EVIDENCIA | Uso en ESCENARIO |
|---|---|---|---|
| DOCUMENTADA / ASEGURADA (A) | contrato o compra documentada | se vende | se vende y cuenta como respaldo comercial |
| NEGOCIADA (B) | negociación con volumen | **no** se vende | × α declarado (DEC-014) |
| INTERESADA (B–C) | interés sin volumen firme | no | solo si el usuario la incluye |
| POTENCIAL (C/D) | canal posible (p. ej., los ~90 supermercados) | no | solo si el usuario la incluye; respaldo comercial 0 % |
| ESCENARIO | hipótesis del usuario | no | sí, rotulada `SIMULACION_HIPOTETICA_NO_VALIDADA` |

Verificado: en las 5 arquitecturas el modo evidencia no tiene **ninguna** línea de demanda contable y su faltante aclara que los ~90 supermercados son canal potencial (DM01); el modo evidencia solo vende A (DM02); en escenario la demanda hipotética no se cuenta como asegurada aunque haya VAN (DM03); las ventas nunca superan mín(producción + inventario, demanda) salvo la línea `toma_todo` declarada como canal de liquidación (TF-006). **Los 90 supermercados no se tratan como demanda asegurada en ningún módulo.**

## 7. Producción

Producción primaria (03) es la única fuente de pollitos, mortalidad, FCR, peso, ciclos, plazas, m² y alimento; 14B reproduce sus pollitos y su alimento sin recalcular (14 U09) y CAPEX (19) los consume como drivers con procedencia (19 N01–N18; mutaciones D02–D06 detectan recálculos silenciosos). Escalas: "planta de N aves/día" = N aves **faenadas por día operativo** a utilización 100 % de la capacidad operativa (SUP-052); **capacidad ≠ producción real**: el financiero separa capacidad, aves disponibles (ramp-up), aves requeridas (demanda) y aves faenadas = mín (E2E01: capacidad 1, requeridas 1,5, faenadas 1 ave/mes en el caso artificial). Capacidad mensual = escala × días operativos (250 con 5 d/semana, 300 con 6) ÷ 12 (ES01); escalas intermedias soportadas en todo el rango 2.500–20.000.

## 8. Balance de masa

Identidad completa por ruta (entero A, trozado B, deshuesado C): entrada viva + agua incorporada = Σ salidas (productos, coproductos, subproductos, residuos y pérdidas) con error ≤ 1e-9 kg/ave; cada componente físico pertenece a un solo producto (BM01). Agua agregada/retenida separada de la masa biológica (kg comerciales = biológicos + agua) (BM03). Esqueleto vendido vs CMS y hueso: rutas exclusivas; carcasa entera + sus cortes de la misma ave no se venden a la vez (en A, los cortes provienen solo de carcasas degradadas) (BM02); el validador del financiero rechaza productos que superan la masa del ave (mutación m01 detectada). Sangre, plumas, vísceras, cabezas, condenas, huesos: subproductos C con destino venta cruda / rendering propio (FUTURO) / contrato de façon, nunca dos a la vez.

## 9. Proceso

Capacidad de línea (nominal declarada del fabricante) ≠ capacidad operativa ≠ capacidad comercial: el BOQ usa el ritmo nominal **requerido** de 05, la capacidad garantizada es un dato del RFQ (DPV-097) y la real un dato de campo (DPV-088) (TF-057). Horas netas, turnos, pausas, limpieza y mantenimiento integrados en la ecuación de 24 h (05, 18). Benchmarks de fabricante quedan como nominales / `[PVDP]`.

## 10. Utilities

Universos separados (SUP-186): 09C/11/12 = solo planta de faena; incubación, planta de alimento, granjas y tratamiento de subproductos con consumos **PENDIENTES** (UT02: no se extrapola el kWh de faena a upstream). Electricidad: una sola fila costeada de energía activa por universo; la energía de frío, congelado, cámaras, efluentes y bombeo figura **INCLUIDA** en `UT-ELE-KWH` (UT01; mutación m02 detectada). Potencia pico, carga frigorífica total (brecha ×5,7 con el benchmark, TF de T16-04/T17-03) y grupo electrógeno PENDIENTES. Efluentes: carga de SST = g/ave × aves, nunca la masa de subproductos; lodos **PENDIENTES** sin dimensionar (UT03, TF-007).

## 11. Localización, layout y logística

- **Localización:** sin ranking emitido (0 de 624 celdas verificadas; todas las posiciones `NO_EMITIDO`); gates duros y condicionales documentados por separado; el contacto en Chaco tiene peso 0 en todos los perfiles (LO01; 10 T28).
- **Layout / terreno:** construido ≠ operación ≠ mínimo físico ≠ terreno conceptual ≠ escenario objetivo ≠ terreno a adquirir; el terreno conceptual de 12C **no es obligatorio** y la adquisición es DEC-063 (TF-056).
- **Logística:** flujos de pollitos, alimento, granos, aves vivas, refrigerado, congelado y subproductos con capacidades de vehículo de **escenario**; flota propia / tercerizada por arquitectura; la ventana prefaena y los radios son sensibilidades, no reglas regulatorias.

## 12. RR. HH. y upstream

Unidades separadas y nunca sumadas (puestos, simultáneos, pico, FTE, horas). El FTE de 14A es el universo **industrial + estructura + coordinación primaria**: OPEX no lo usa como dotación de la empresa integrada; granjas propias, incubadora y planta de alimento tienen RR. HH. `PENDIENTE` en C3/CF (UT02, TF-058). El personal del faenador queda `INCLUIDO_EN_TARIFA_FACON` (20 M11). SAC es una **regla laboral** de devengo, no un precio de mercado; salario, cargas, ART, adicionales, beneficios, capacitación y EPP están separados y **vacíos** (sin salario inventado). Upstream: setter y hatcher por separado con cadencia; planta de alimento en t/h; **stock físico ≠ stock propiedad**: solo el inventario propio entra al CT (CT01, TF-059).

## 13. CAPEX

BOQ por arquitectura y escala con drivers de procedencia trazable (obra, terreno, equipos, instalación, importación por capas, indirectos, contingencias, preoperativos, expansión y reposición). Precio observado separado de la conversión USD (SUP-187), niveles E1–E5 / PENDIENTE. Conceptos con precio: 0–2,3 %, todos E4 `[PVDP]`; **faltante ≠ 0** y **CAPEX total NO DISPONIBLE** en todas las arquitecturas (FA02: ningún monto E4 parcial entra como total al financiero). Expansión: crecer de escala dentro de una arquitectura está soportado (trayectorias T1–T3); cambiar de arquitectura es `TRANSICION_DE_ARQUITECTURA_NO_MODELADA` (DEC-103).

## 14. OPEX

Registro por concepto con naturaleza fija/variable/semifija y propiedad. Cobertura estructural 100 %, física 43–62 % en las bases (hasta 73 % en variantes), costeo por bloques 0–10 %; ninguna arquitectura costeable. Doble conteos auditados: electricidad de frío (UT01), agua y energía de limpieza (INCLUIDAS en UT-AGUA / UT-ELE-KWH / UT-TER), RR. HH. de façon (incluido en la tarifa), limpieza tercerizada (reemplaza la fila laboral, no la suma), choferes tercerizados (incluidos en la tarifa de flete), costos upstream (en filas de su universo, no extrapolados) (RH01). Exportación y Halal: OPEX `HAL-*` en la variante C1-HALAL sin importes; CAPEX Halal futuro como conceptos de la base; ingresos por el canal exportación del financiero; riesgos en el registro (RG-*): se incorporan **sin duplicar** módulos.

## 15. Capital de trabajo

Identidad: **CT = inventarios propios + CxC + caja operativa − CxP**, con días ÷ (365/12) por mes; el flujo usa **ΔCT** (Σ ΔCT = CT final; E2E02) y la mutación "CT total en lugar de ΔCT" se detecta (m03; 21 M04). Solo stock propiedad de la empresa (CT01). Parámetros de días `PENDIENTES` (DPV-175): `CAPITAL_TRABAJO = PENDIENTE`.

## 16. Financiero

| Identidad | Verificación |
|---|---|
| Ingreso neto = bruta − descuentos − bonificaciones − devoluciones − comisiones − derechos de exportación | E2E02 mes a mes |
| EBITDA = neto − OPEX − logística del canal − costos de exportación − IIBB/tasas − otros − extras de ramp-up | E2E02 |
| EBIT = EBITDA − depreciación; impuestos anuales con quebrantos | E2E02; 21 C02 |
| FCFF = EBITDA − impuestos operativos − CAPEX − ΔCT ± IVA + VT, **sin financiación** | E2E02; FI01 (agregar deuda no cambia FCFF ni VAN del proyecto); m04 |
| FCFE y caja = FCFF − impuestos con deuda ± deuda + aportes − dividendos | E2E02; FI01 |
| VAN, TIR, payback, break-even, DSCR | E2E03 (cálculo manual independiente); 21 R01–R05 |

**Periodicidad:** tasa anual efectiva → mensual (1 + r)^(1/12) − 1 (nunca r/12); VAN mensual; TIR mensual anualizada (1 + i)^12 − 1; payback en meses y años = meses ÷ 12; deuda con tipo de tasa obligatorio; real vs nominal no se mezclan (FI02). **Proyecto vs accionista:** la TIR del accionista se publica con su nombre y nunca como TIR del proyecto. **Valor terminal:** por defecto `SIN_VALOR_TERMINAL` (serie = 0); con método declarado la serie cierra la identidad del FCFF (FI03; corrección del §25). **Evidencia vs escenario:** ver §23.

## 17. Riesgos

Registro de 34 riesgos con **frecuencia sectorial** (con unidad, período y fuente) separada de la **probabilidad del proyecto** (PENDIENTE sin método) (RI05, SUP-224); matriz cualitativa 3×3 sin producto numérico; inherente y residual separados. Sensibilidad one-way cambia solo un driver y two-way solo dos, con la base intacta (RI01); stress multivariable = escenario determinista, no probabilidad, y nunca sobre la evidencia (RI02); puntos de quiebre por grilla + bisección, y los del caso artificial quedan en ámbito `ARTIFICIAL_TEST` (RI03). **Monte Carlo del proyecto NO_DISPONIBLE**: ninguna distribución respaldada ni correlación (una correlación PENDIENTE ≠ 0); no se inventaron normales, triangulares ni uniformes (RI04, DPV-180).

## 18. Optimizador

Consume el motor financiero como función de evaluación (E2E05: VAN del optimizador = VAN de `resultados()`); el modo rápido solo omite la TIR (`NO_CALCULADA`) y no cambia ninguna otra métrica. Con un caso artificial de solución conocida (OP01): mejor VAN, menor capital, alternativa dominada y frontera de Pareto coinciden con el cálculo manual. `NO_INVERTIR_AUN` es alternativa de decisión: sin métricas, fuera de rankings, Pareto, dominancia y robustez; gana solo por regla (capital HARD → SQ-1/SQ-2; VAN < 0 → SQ-3) (OP02; m11). Una alternativa de otro horizonte o con OPEX faltante no se rankea ni domina aunque "gane" (OP03; m10). Con < 2 comparables, `PARETO_NO_INFORMATIVO_MUESTRA_INSUFICIENTE`; robustez exige ≥ 3 escenarios (OP04). C0: `NO_REQUERIDO_POR_ARQUITECTURA` ≠ `DESCONOCIDO` (OP05; m09). Factibilidades física, económica, financiera, comercial y de evidencia separadas (OP06). Prioridades con empates como `RANK_COMPARTIDO` y columna futura `POTENCIAL_DE_CAMBIAR_DECISION = NO_CALCULADO` en evidencia (OP07). **Proyecto: `OPTIMIZACION_REAL_NO_DISPONIBLE`** (0 de 54 alternativas con VAN publicable; TF-010).

## 19. Doble conteos auditados

| Riesgo de doble conteo | Control | Resultado |
|---|---|---|
| Carcasa entera + sus cortes; esqueleto + CMS | rutas exclusivas del balance; validador de masa del financiero | sin doble conteo (BM02, m01) |
| Electricidad de frío además de la energía total | filas INCLUIDAS en UT-ELE-KWH | sin doble conteo (UT01, m02) |
| Agua de limpieza | fila INCLUIDA en UT-AGUA / UT-ELE-KWH / UT-TER | sin doble conteo (RH01) |
| RR. HH. del faenador / limpieza tercerizada / choferes tercerizados | `TERCERO_INCLUIDO_EN_TARIFA`; la tarifa reemplaza la fila laboral (20 M11) | sin doble conteo (RH01) |
| Costos upstream vs faena | universos separados (SUP-186) | sin doble conteo (UT02) |
| Paquetes RFQ (equipos en dos lotes) | SUP-160; T16-01/T16-02 | registrado (TF de T16-01/02) |
| Derechos de exportación (venta y costo) | ubicación única (SUP-210) | sin doble conteo (FI04) |
| IVA en el EBITDA | IVA solo como flujo de caja | sin doble conteo (FI04) |
| IVA de CAPEX con `IVA_INCIERTO` + crédito fiscal | — | **potencial**, hoy sin efecto (TF-076) |
| CT completo en cada período | ΔCT | sin doble conteo (E2E02, m03) |
| Deuda en el FCFF | FCFF sin financiación | sin doble conteo (FI01, m04) |

## 20. Unidades

Auditoría transversal: aves (por día **operativo**), kg y t (base declarada: peso vivo, carcasa, comercial = biológico + agua), kg/día y t/día (demanda en día **calendario**), t/año, m² y ha, m³ y m³/día, kWh (energía) vs kW (potencia) vs kWf (frío), MJ/GJ (térmico), USD/t, USD/kg, USD/ave, horas, FTE, días. No se encontraron conversiones silenciosas: la demanda se convierte con 365/12 explícito (ES02), la capacidad con días operativos explícitos (ES01) y los kWh de frío no se convierten en kWf sin COP (11 M16).

## 21. Tiempo

Día operativo (capacidad, producción, utilities) vs día calendario (demanda, inventarios, CT); 250 días/año (5 d/semana) y 300 (6 d/semana); 365 días para demanda, CT e inventario; semana plena para galpones y pollitos; mes = 365/12 días en el financiero. Denominadores no mezclados: producción en día operativo × días ÷ 12; demanda en día calendario × 365/12; inventario y CT en días calendario (ES01, ES02; 23 T21). Días operativos arbitrarios no soportados por la interfaz (TF-001).

## 22. Moneda

USD constantes de 2026-10-01 (modelo REAL, SUP-195). Moneda original, TC, fecha del TC y tipo de TC se registran por precio; un precio en ARS sin TC, fecha y tipo no se convierte (UN01); en OPEX todo precio en ARS conserva precio observado, moneda, TC y fecha (UN02). La conversión a USD no es una nueva cotización (SUP-187); no se indexa automáticamente un precio anterior a la fecha base (SUP-155). El adaptador OPEX → 21 no transporta la moneda original al motor (TF-003, DPV-179).

## 23. Evidencia

- Umbral `UMBRAL_EVIDENCIA_PUBLICACION` **configurable** sin tocar código; default actual **E1 | E2 | E3** (SUP-190); E4/E5 fuera del default; la decisión definitiva es DEC-084 (abierta) (EV02).
- **Ida y vuelta (EV01):** aplicar stress y overrides en escenario no cambia la entrada de evidencia (en memoria) ni los archivos de evidencia (hash idéntico); el universo EVIDENCIA rechaza shocks y rechaza inputs de usuario. **Nunca ocurre simulación → base de evidencia.**
- Precios E4 `[PVDP]` = `REFERENCIA_E4_NO_USABLE`; ninguno se usa (EV03; mutación m05 detectada).
- Publicabilidad: un número nunca se publica con su flag FALSE; en el proyecto, 0 indicadores publicables en las 5 arquitecturas (FI05); un faltante de CAPEX, OPEX o precio da NO PUBLICABLE con motivo, nunca 0 (FA01; m06).
- Coberturas separadas (estructural, física, económica, evidencia) en [`cobertura_motor.csv`](cobertura_motor.csv) (CV01). La cobertura de evidencia del optimizador cuenta dos bloques vacuos (TF-011).

## 24. Tensiones

[`tensiones_finales.csv`](tensiones_finales.csv): **76** (74 abiertas, 2 corregidas). TF-001 a TF-011 y TF-076 son nuevas de esta auditoría; TF-012 a TF-075 indexan las tensiones abiertas T12, T14, T16, T17, T18, T19 y T20 con su ID original. Ninguna tensión de negocio se resolvió. Principales abiertas: precios casi inexistentes en CAPEX y OPEX (TF-053, TF-054); rendimientos del balance sin ensayo (TF-069); pico de fondos vs CAPEX vs USD 2 M (TF-070); upstream sin RR. HH. ni utilities (TF-058); OPEX/CAPEX del usuario sin control de completitud de arquitectura en escenarios (TF-004); comparabilidad imposible hoy (TF-010).

## 25. Tests integrados

| Grupo | Tests | Qué prueba |
|---|---|---|
| IDs y registros | ID01–ID05 | sin IDs provisionales activos; IDs únicos y correlativos; referencias existentes; matriz de campo; mapa 19–20 completo |
| Integridad del repo | RP01–RP06 | merge markers; CSV válidos; links internos; caches/temporales; README; salida generada al día |
| Arquitecturas y variantes | AR01–AR04 | C0–CF iguales en 19, 20, 21 y 22; tabla maestra; C0/C1/C3 (punto 51); variantes |
| Escalas, tiempo, unidades, moneda | ES01–ES02, UN01–UN02 | días operativos vs calendario; FX trazable |
| Demanda | DM01–DM03 | 90 supermercados ≠ demanda; categorías; respaldo comercial separado |
| Balance y productos | BM01–BM03 | identidad de masa; rutas exclusivas (punto 9); agua separada |
| Utilities, efluentes, localización, RR. HH., CT | UT01–UT03, LO01, RH01, CT01 | electricidad única; universos; SST ≠ subproductos; lodos; sin ranking; terceros sin doble conteo; propiedad del stock |
| Caso artificial de punta a punta (punto 49) | E2E01–E2E05 | demanda → producción → ventas → CAPEX → OPEX → CT → flujo → VAN/TIR → riesgo → optimizador, verificado a mano |
| Financiero | FI01–FI05 | FCFF sin deuda; periodicidad; valor terminal; impuestos; publicabilidad |
| Faltantes (punto 50) | FA01–FA02 | sin CAPEX / OPEX / precio → NO PUBLICABLE, no 0 |
| Evidencia vs escenario (puntos 28, 29, 52) | EV01–EV03 | ida y vuelta; umbral configurable; E4 no usable |
| Riesgo | RI01–RI05 | one-way / two-way; stress; quiebres; Monte Carlo; frecuencia ≠ probabilidad |
| Optimizador (puntos 36–42, 53) | OP01–OP07 | solución conocida; status quo; comparabilidad; Pareto; robustez; C0; factibilidades; empates |
| Cobertura y tablas | CV01, TB01, MU00 | cuatro coberturas; campos de las tablas finales; detectores sin falsos positivos |

**Mutaciones de integración (punto 54): 11/11 detectadas** — m01 duplicar masa vendida · m02 duplicar electricidad · m03 CT total en lugar de ΔCT · m04 deuda en el FCFF · m05 precio E4 como validado · m06 faltante → 0 · m07 ventas > demanda · m08 arquitectura distinta en CAPEX y OPEX · m09 C0 desconocido como 0 · m10 rankear alternativa no comparable · m11 NO_INVERTIR_AUN con TIR/VAN ficticios. Resultado de todas las suites en [`registro_tests_final.csv`](registro_tests_final.csv).

**Salidas generadas vs código (punto 65):** se regeneraron las salidas de los 15 modelos y del simulador HTML después de todos los cambios: todas las salidas versionadas son **idénticas byte a byte** salvo (a) `prioridad_validacion.csv` y `que_hacer_ahora.csv` de 22 (solo la columna nueva `POTENCIAL_DE_CAMBIAR_DECISION`) y (b) los metadatos `generado` y `commit_repositorio` de `simulador_data.json/.js` (contenido idéntico; se conserva la versión versionada). `cobertura_mutaciones.csv` de 22 se reproduce exactamente en una copia limpia de `main` (una diferencia observada al correr las mutaciones mientras se editaban archivos no es del código).

**Correcciones inequívocas hechas en esta sesión:** (1) `modelo_financiero.py`: con valor terminal PERPETUIDAD + recupero de CT, la serie `valor_terminal` omitía el CT recuperado (el FCFF y el VAN eran correctos; la identidad reportada no cerraba) — TF-009; ninguna salida del proyecto cambia. (2) `mapa_arquitecturas_economicas.csv`: atributos FRIO/SUBPRODUCTOS de tres variantes repetían la base — TF-008. Interfaz: columna futura `POTENCIAL_DE_CAMBIAR_DECISION` en `prioridad_validacion.csv` y `que_hacer_ahora.csv` (sin completar en evidencia).

## 26. Completitud

| Dimensión | Estado |
|---|---|
| Motor estructural (todos los módulos, interfaces, identidades, etiquetas, tests) | **COMPLETO** |
| Cobertura física (cantidades dimensionadas) | **PARCIAL**: CAPEX 84–95 % de conceptos con cantidad; OPEX 43–62 % de bloques en las bases (hasta 73 % en variantes); upstream sin RR. HH. ni utilities |
| Cobertura económica (precios) | **CASI NULA**: CAPEX 0–2,3 % de conceptos; OPEX 0–10 % de bloques; precios de venta 0 |
| Cobertura de evidencia (E1–E3) | **NULA** en datos económicos (0 conceptos E1–E3); 15 de 17 bloques del motor sin evidencia |

Un módulo puede estar `LISTO_APP = TRUE` y `LISTO_DECISION_REAL = FALSE`: es el caso de todos los módulos del motor ([`completitud_final_motor.csv`](completitud_final_motor.csv)).

## 27. Datos pendientes

180 DPV, **ninguno validado**. Lo que bloquea **todos** los indicadores económicos (empatados, sin orden interno): demanda A/B, precios de venta, condiciones comerciales, CAPEX, OPEX costeable, ramp-up, tiempos de obra, CT, impuestos, IVA, tasa de descuento, rendimientos validados. Agrupados en 12 paquetes operativos con actor, pedido, unidad y modelo que desbloquean en [`plan_validacion_final.md`](plan_validacion_final.md).

## 28. Decisiones pendientes

104 DEC, **todas abiertas**. Metodológicas que condicionan la publicación: DEC-084 (umbral de evidencia), DEC-007 (horizonte y tasa), DEC-093 (valor terminal), DEC-096 (base de flujo y convención), DEC-006 (real/nominal, TC). De negocio que condicionan la decisión: DEC-001/DEC-033 (escala y arquitectura de crecimiento), DEC-010 (escenarios de inversión), DEC-092 (financiamiento), DEC-097/DEC-098 (objetivos y restricciones del inversor), DEC-003 (localización), DEC-020/023/024/074 (integración upstream).

## 29. Interfaz app

Contrato en [`interfaz_app_v1.md`](interfaz_app_v1.md): inputs (objetivo, capital, demanda, precios, arquitectura, escala, shocks, restricciones), outputs (inversión, OPEX, fondos, ingresos, EBITDA, VAN/TIR, payback, riesgo, robustez, ranking, faltantes, qué hacer ahora) y etiquetas obligatorias (evidencia, escenario, pendiente, no comparable, no calculado, simulación). La app debe agregar un control que el motor aún no tiene: completitud de arquitectura cuando el usuario carga su propio OPEX/CAPEX en escenarios (TF-004).

## 30. Conclusión

**¿EL MOTOR ESTÁ TERMINADO? — PARCIAL.**

| Dimensión | Estado |
|---|---|
| **MOTOR ESTRUCTURAL** | **COMPLETO**: todas las suites de módulo y de integración pasan; 11/11 mutaciones de integración detectadas; C0–CF idénticas en todos los módulos; sin doble conteos detectados; sin IDs provisionales activos |
| **DATOS REALES** | **INCOMPLETOS**: 0 DPV validados; 0 precios de venta, 0 conceptos de CAPEX y OPEX con evidencia E1–E3; demanda contable = 0; ninguna arquitectura costeable |
| **DECISIÓN DE INVERSIÓN** | **NO DISPONIBLE AÚN**: 0 de 61 corridas financieras y 0 de 54 alternativas del optimizador tienen indicadores publicables en modo evidencia (`OPTIMIZACION_REAL_NO_DISPONIBLE`) |
| **LISTO PARA LA APP v1** | **SÍ como motor de escenarios rotulados**, con el contrato de [`interfaz_app_v1.md`](interfaz_app_v1.md) y el control de completitud de TF-004 |

Esta auditoría **no** recomienda comprar o no comprar una planta, invertir un monto, ni elegir una arquitectura o escala: con los datos actuales no hay base para hacerlo.
