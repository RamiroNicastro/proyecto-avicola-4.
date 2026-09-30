# Estado del proyecto

**Fase actual:** FASE 0 — DEFINICIÓN Y PREFACTIBILIDAD
**Última actualización:** 2026-09-30 (plan de validación de campo: [`plan_trabajo_campo.md`](plan_trabajo_campo.md); antes, reconciliación de las sesiones 09A–09D: [`reconciliacion_sesiones_09.md`](reconciliacion_sesiones_09.md))

## Situación de partida

- Activo existente: una carnicería familiar.
- Sin granjas, frigorífico, terreno, maquinaria ni infraestructura industrial.
- Capital potencial: ~USD 2.000.000 de un grupo inversor — **no comprometido**. Es solo un **escenario inicial de referencia**, no un límite (SUP-003, DEC-010).
- Canal comercial potencial: ~90 supermercados, aparentemente concentrados en AMBA — **demanda no validada**; proveedor actual desconocido (SUP-004, DPV-020). La carnicería está en el AMBA.
- Visión: empresa avícola integrada, escalable y con vocación exportadora (SUP-011). Principio: ingreso total por ave (SUP-013). Sin localización seleccionada (DEC-003).

Detalle de premisas: [`supuestos.md`](supuestos.md).

## Tablero de estado (2026-09-30)

**Cómo leerlo:** *Modelo preliminar completado* = el método, el documento y (si corresponde) el modelo reproducible existen y pasan sus pruebas. **No** significa validado en campo. *Evidencia de campo pendiente* = sus cifras todavía no fueron contrastadas con datos reales (plantas argentinas, compradores, proveedores, organismos, sitios). En toda la Fase 0 **ninguna** cifra externa pudo leerse en su documento original desde el entorno de análisis (DPV-009).

| Módulo | Modelo preliminar | Evidencia de campo | Síntesis |
|---|---|---|---|
| Mercado (`01`) | **Completado** v2 | Pendiente (verificación documental primaria) | [`conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md) |
| Exportación (`17`) | **Completado** v1.1 | Pendiente | [`conclusiones_exportacion.md`](../17_exportacion/conclusiones_exportacion.md) |
| Demanda (`02`) | **Completado** v1 (marco y escenarios de prueba) | Pendiente — demanda documentada ≈ 0 | [`conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md) |
| Producción primaria (`03`) | **Completado** v1.1 (modelo y 72 escenarios) | Pendiente | [`conclusiones_produccion.md`](../03_produccion_primaria/conclusiones_produccion.md) |
| Balance de masa (`04`) | **Completado** v1.1 (modelo, 21 tests) | Pendiente — ensayo en planta (DEC-028) | [`conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md) |
| Productos y subproductos (`06`, `07`) | **Completado** v1.0 (mapa, 9 tests) | Pendiente — sin precios ni compradores | [`conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md) |
| Escala preliminar (`23`) | **Completado** v1.1 (modelo, 23 tests; **sin escala elegida**) | Pendiente | [`conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md) |
| Proceso industrial conceptual (`05`) | **Completado** v1.1 (modelo, 18 tests) | Pendiente — capacidad real, limpieza, productividad | [`conclusiones_proceso.md`](../05_proceso_industrial/conclusiones_proceso.md) |
| Maquinaria conceptual (`08`) | **Completado** (76 equipos, RFQ no enviado; **sin proveedor**) | Pendiente — cotizaciones, servicio técnico | [`08_maquinaria/README.md`](../08_maquinaria/README.md) |
| Normativa preliminar (`16`) | **Completado** v1.0 (hoja de ruta, 64 requisitos) | Pendiente — 0 normas leídas en original; consulta a SENASA | [`conclusiones_normativa.md`](../16_normativa_senasa/conclusiones_normativa.md) |
| Agua y efluentes (`11`) | **Completado** v1.1 (modelo de utilities, 30 tests) | Pendiente — agua, vuelco, DQO/DBO/SST, lodos | [`conclusiones_agua_efluentes.md`](../11_agua_efluentes/conclusiones_agua_efluentes.md) |
| Energía y frío (`12`) | **Completado** v1.1 (mismo modelo; pico, carga frigorífica total y generador PENDIENTES) | Pendiente — lista de cargas, balance frigorífico | [`conclusiones_energia_frio.md`](../12_energia_frio/conclusiones_energia_frio.md) |
| Simulador HTML v0.1 (`23/simulador_html`) | **Construido** v0.1 (20/20 validaciones; sin economía) | No aplica (interfaz de modelos) | [`simulador_html/README.md`](../23_plan_expansion/simulador_html/README.md) |
| Trabajo de campo (demanda, plantas, proveedores, SENASA, sitios) | **Plan completado** v1.0 (115 DPV priorizados N1–N4, instrumentos, orden de trabajo; sin evidencia recolectada) | **Pendiente** — ningún actor contactado | [`plan_trabajo_campo.md`](plan_trabajo_campo.md) |
| Localización (`10`) | **Pendiente** (no iniciado) | Pendiente | — |
| Logística detallada (`13`) | **Pendiente** (no iniciado) | Pendiente | — |
| Layout y obra civil (`09`) | **Pendiente** (no iniciado) | Pendiente | — |
| Recursos humanos (`18`) | **Pendiente** (no iniciado) | Pendiente | — |
| CAPEX (`19`) / OPEX (`20`) | **Pendiente** (no iniciado) | Pendiente | — |
| Modelo financiero (`21`) y riesgo financiero (`22`) | **Pendiente** (no iniciado) | Pendiente | — |
| Decisión de escala (DEC-001, DEC-033) | **Pendiente** (no tomada) | Pendiente | — |
| Documentación final para inversores (`24`) | **Pendiente** | — | — |

## Alcance de la Fase 0

1. Estructurar el repositorio y las reglas de trabajo. ✅
2. Relevar información de mercado, normativa y tecnología con fuentes trazables. ✅ como modelo preliminar (mercado, exportación, normativa, proceso, maquinaria, utilities); verificación documental primaria pendiente (DPV-009).
3. Validar (o descartar) la demanda del canal supermercados. ⏳ Marco listo; trabajo de campo pendiente.
4. Construir el balance de masa y escenarios de escala sin fijar capacidad a priori. ✅ como modelo preliminar (sin escala elegida).
5. Evaluar cada eslabón de la cadena: hacer / comprar / tercerizar / postergar. ⏳ Parcial (producción primaria, subproductos, faena a façon como opciones sin decisión).
6. Estimar CAPEX y OPEX por escenario y construir el modelo financiero. ⏳ No iniciado.
7. Emitir conclusión de prefactibilidad (viable / viable con condiciones / no viable) y definir si se pasa a Fase 1 (factibilidad). ⏳ No iniciado.

## Restricciones vigentes en esta fase

- **No** se realizan recomendaciones de inversión.
- **No** se selecciona maquinaria ni proveedores (solo relevamiento; DEC-049 abierta). Las capacidades de fabricantes son nominales declaradas, nunca capacidad del proyecto.
- **No** se eligen automatización, arquitectura de línea, segundo turno, enfriamiento, aturdido, tratamiento de efluentes, refrigerante, fuente térmica, respaldo, rendering ni ubicación (DEC-003, DEC-026, DEC-027, DEC-036 a DEC-049).
- **No** se fija capacidad de faena (el modelo de escala de 2026-09-30 compara escenarios; no elige escala).

## Hitos

| Fecha | Hito | Estado |
|---|---|---|
| 2026-09-29 | Estructura del repositorio y reglas (`CLAUDE.md`) | Completado |
| 2026-09-29 | Relevamiento de mercado (`01_mercado`): radiografía 2026, competidores, exportaciones y conclusiones | Completado v2 (segunda pasada de control y triangulación). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)** |
| 2026-09-29 | Estudio del mercado internacional y de exportación (`17_exportacion`): comercio mundial, productos, acceso por país (A/B/C/D), China, Halal, UE, valorización del ave, requisitos de planta, logística, riesgos y modelos A/B/C | Completado v1.1 (con corrección prudencial sobre China, Halal, niveles de acceso y precios). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA |
| 2026-09-29 | Modelo de demanda comercial (`02_clientes_demanda`): categorías A/B/C/D, niveles de exportación 0–6, escenarios de la red (25–300 kg/local/día), mix, logística, concentración, precio-margen, marca, indicadores, cuestionario y tareas de campo | Completado v1 (marco, **sin datos de campo**). Calidad: MEDIA como método, BAJA como evidencia cuantitativa |
| 2026-09-29 | Estudio de producción primaria (`03_produccion_primaria`): ciclo productivo, rangos de edad/peso/FCR/mortalidad, densidad y bienestar, galpones, energía y clima, alimento y agua, bioseguridad, transporte de aves vivas, modelos propio/integrado/compra/mixto, pollito BB, KPIs, escenarios físicos (72) con modelo documentado y guía para el responsable | Completado v1.1 (marco y escenarios, **sin datos de campo**; auditoría del modelo físico con corrección de pollitos/semana y galpones +4,3 % y pruebas automáticas). **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA como marco y modelo físico, BAJA como evidencia de campo argentina |
| — | Validación de demanda con datos de campo (red de supermercados y otros canales) | Pendiente: requiere el cuestionario y las tareas de `02_clientes_demanda/conclusiones_demanda.md` §6 |
| 2026-09-30 | Balance de masa (`04_balance_masa`): definiciones (vivo, eviscerado, carcasa fría, RTC, comercial), balance por ave para 6 pesos, cortes y deshuese, menudencias, garras, plumas, sangre, vísceras, agua del chiller separada de la masa biológica, condenas y mermas, 3 configuraciones (entero / trozado / deshuesado), escalado 1 ave–20.000 aves/día y 1 M aves/año, clases A/B/C/D, modelo reproducible con 13 tests y protocolo de ensayo en planta | Completado v1.1 (**sin datos de planta argentinos**). Auditoría conceptual v1.1: sin doble contabilización; nomenclatura del agua corregida (agua incorporada a productos y subproductos ≠ agua de proceso de la planta); rutas alternativas exclusivas esqueleto/CMS; 21 tests sobre 1.008 balances con error ≤ 2 × 10⁻¹⁵ kg/ave. **Verificación documental primaria no realizada: acceso bloqueado (DPV-009)**. Calidad: MEDIA como modelo, BAJA como evidencia numérica |
| 2026-09-30 | Mapa de productos, coproductos y subproductos (`06_productos`, `07_subproductos`): inventario de 39 salidas con kg/ave trazables al balance v1.1, clasificación económica condicional al comprador, productos de mercado interno y exportación, garras, menudencias, carcasa/CMS, piel y grasa, sangre, plumas, vísceras, cabeza y huesos, rendering (propio / tercerizado / venta directa), pet food, elaborados, matriz de valorización, índice de aprovechamiento del ave, árboles de rutas con 15 incompatibilidades, escalado 2.500–20.000 aves/día, lista maestra de precios y tareas de campo; generador con 9 tests | Completado v1.0 (**sin precios ni compradores**; normativa solo en extractos, DPV-009). Calidad: MEDIA como mapa y método, BAJA como evidencia comercial y normativa |
| 2026-09-30 | Modelo preliminar de escala (`23_plan_expansion`, `05_proceso_industrial/capacidad_preliminar.md`): definición de capacidad (nominal / operativa / faenada / utilización), calendarios 250 y 300 días, ritmo de línea por horas netas, demanda vs capacidad con dos métodos (ave completa y parte limitante con balance v1.1), utilización 30–100 %, producción primaria importada, modelos de abastecimiento, balance de productos, configuraciones A/B/C, subproductos, inventario y logística conceptuales, exportación (lotes), modularidad, arquitecturas de crecimiento A–E, gates G0–G3, matriz sin ganador, especificación del simulador HTML v0.1 y guía; modelo reproducible que importa los modelos previos; auditoría conceptual v1.1 (utilización ≤ 100 % separada de factor demanda/capacidad y cobertura; día operativo vs calendario; inventario con dos bases; masa biológica vs peso comercial; segundo turno y sexto día; localización como hipótesis), 23 tests y 22 mutaciones detectadas | Completado v1.1 (**sin escala elegida, sin CAPEX/OPEX, sin datos de campo**). Calidad: MEDIA como modelo integrador, BAJA como evidencia para decidir la escala |
| 2026-09-30 | Proceso industrial y maquinaria conceptual (`05_proceso_industrial`, `08_maquinaria`; sesión 09A): flujo de 32 etapas con flujos laterales, zonificación higiénica, capacidad horaria y ventana del establecimiento (ecuación de 24 h), cuellos de botella, arquitecturas por escala, 76 equipos conceptuales con automatización por escala y criticidad, proveedores preliminares, nuevo vs usado, RFQ futuro; `modelo_capacidad_proceso.py` v1.1 | **Modelo preliminar completado** v1.1 (18/18 tests; 9/9 mutaciones). **Evidencia de campo pendiente.** Sin escala, proveedor, CAPEX, layout ni localización. Tres fuentes de fabricante confirmadas en revisión externa (lectura primaria pendiente de reproducir). Calidad: MEDIA como método, BAJA como evidencia de capacidad real |
| 2026-09-30 | Normativa preliminar (`16_normativa_senasa`; sesión 09B): mapa de autoridades y habilitaciones, rol del Decreto 4238/68, secuencia tentativa, requisitos sanitarios, APPCC obligatorio (Res. 205/2014), Decreto 697/2026, Ley 22.375, escalera exportadora, subproductos, matriz de 64 requisitos, ruta crítica (14 reglas), 7 preguntas prioritarias a SENASA | **Modelo preliminar completado** v1.0. **Ninguna norma leída en original** (DPV-009): 37 requisitos `[PVDP]`, 15 por consultar a SENASA, 12 dependientes de jurisdicción, 0 verificados en primaria. Calidad: MEDIA como estructura, BAJA como evidencia normativa |
| 2026-09-30 | Agua, efluentes, energía y frío (`11_agua_efluentes`, `12_energia_frio`; sesión 09C): modelo **top-down de sensibilidad** de cinco aguas, efluente por dos métodos, lodos (pendiente), energía, térmico, frío, congelado y respaldo; `modelo_utilities.py` v1.1 | **Modelo preliminar completado** v1.1 (30 tests; 20 mutaciones). Potencia pico, pico térmico, carga frigorífica total, lodos y grupo electrógeno **PENDIENTES**. **Evidencia de campo pendiente.** Calidad: MEDIA como método, BAJA como evidencia |
| 2026-09-30 | Simulador HTML v0.1 (`23_plan_expansion/simulador_html`; sesión 09D) | **Construido.** Reproduce los modelos físicos aprobados (4.224 cifras de `escenarios_escala.csv` sin diferencias; 20/20 validaciones; prueba en navegador 16/16); funciona offline (`file://`, sin CDN); comparador A/B/C; **sin economía** (CAPEX, OPEX, EBITDA, VAN, TIR y payback pendientes); no integra todavía proceso (09A) ni utilities (09C) |
| 2026-09-30 | Reconciliación de las sesiones 09A–09D en los registros maestros | Completada: 17 SUP, 28 DPV, 13 DEC y 75 FTE nuevos; 15 IDs provisionales consolidados en registros existentes o fusionados entre sí (ninguno duplicado); tensiones abiertas registradas sin resolver. Ver [`reconciliacion_sesiones_09.md`](reconciliacion_sesiones_09.md) |
| 2026-09-30 | Plan de validación de campo (`00_gestion_proyecto`, `24_inversores` y cuestionarios por carpeta): 115 DPV clasificados en N1–N4 (18 / 53 / 11 / 33) con actor, método, evidencia requerida, decisión que desbloquea y consecuencia; matriz de validación; cuestionario maestro y ejecutivo (20 preguntas) para inversores y minuta; plan de validación comercial con escala de evidencia E1–E6; cuestionarios de productores, incubadoras y subproductos; guía de visita a plantas; plan de RFQ con plantilla de comparación por capas de costo; preguntas ejecutivas a SENASA; ficha de terreno; data room; guía de recolección de evidencia; orden de trabajo en olas O0–O9 con hitos H-A / H-B / H-C | **Plan completado.** Ningún DPV validado, ninguna decisión cerrada, ninguna cotización pedida. Trabajo de campo **no iniciado** |
| — | Escenarios CAPEX/OPEX y modelo financiero | Pendiente |
| — | Informe de prefactibilidad | Pendiente |

## Resultado del relevamiento de mercado (2026-09-29)

Síntesis en [`../01_mercado/conclusiones_mercado.md`](../01_mercado/conclusiones_mercado.md):

- Mercado grande y maduro: ~2,1–2,3 Mt (producción 2025 SAGyP ~2,3 Mt), ~47–49 kg/hab/año, faena SENASA estancada en ~740–750 M cabezas. Todas las cifras están PENDIENTES DE VERIFICACIÓN DOCUMENTAL PRIMARIA.
- El líder (Granja Tres Arroyos) está en concurso preventivo (sept-2026): es un evento de mercado, no una estrategia del proyecto.
- Riesgo sanitario recurrente (IAAP en 2023, 2025 y 2026) con cierres de exportación y sobreoferta interna.
- Exportación: UE, Japón, Chile y Perú reabiertos en 2026; China no disponible confirmada (fecha y alcance de la suspensión pendientes de verificación, DPV-035). El ingreso total por ave queda como principio estratégico.

## Resultado del estudio internacional y de exportación (2026-09-29)

Síntesis en [`../17_exportacion/conclusiones_exportacion.md`](../17_exportacion/conclusiones_exportacion.md):

- Comercio mundial ~14,8 Mt (2026), dominado por Brasil (~36 %). Argentina es un exportador marginal (~1–1,5 %) y precio-aceptante.
- **China no se considera un mercado disponible confirmado**; fecha y alcance de la suspensión pendientes de verificación primaria (DPV-035). Queda fuera del caso base (SUP-016).
- Países con comunicado de apertura posterior a feb-2026 (país abierto ≠ planta habilitada ≠ producto autorizado ≠ comprador): UE, Japón, Corea del Sur, Chile, Perú. Regionalización reconocida: Vietnam (1° destino efectivo), Arabia Saudita, EAU, Singapur, Brasil.
- Exportar no se presume más rentable: se compara por net-back por parte del ave (SUP-017). Modelos A/B/C comparados sin ganador (DEC-011).
- Requisitos de diseño a evaluar: estándar UE (SUP-015) y un diseño que preserve la posibilidad de incorporar procesos y certificaciones Halal una vez validados los requisitos (DEC-012, DPV-034). Los precios internacionales son preliminares y no se usan para calcular rentabilidad (SUP-018).

## Resultado del modelo de demanda comercial (2026-09-29)

Síntesis en [`../02_clientes_demanda/conclusiones_demanda.md`](../02_clientes_demanda/conclusiones_demanda.md):

- **Demanda documentada (A + B) ≈ 0 kg/día:** la carnicería familiar no está cuantificada; la red de ~90 supermercados es categoría C condicionada; otros canales y exportación son D. **No hay base para dimensionar la planta.**
- La red, si todos los locales compraran todo su pollo al proyecto, representaría 2,25–27 t/día (25–300 kg/local/día), ~940–15.000 aves/día según el peso por ave (1,8–2,4 kg equivalente canal, SUP-019). Con adhesión parcial, 0,25–27 t/día.
- Escenarios de prueba (no pronósticos): conservador 1,5 t/día, base 7,5 t/día, expansivo 23,5 t/día; exportación 0 en todos (SUP-022). La red pesa 57–67 % de las ventas: concentración estructural.
- El mix puede multiplicar las aves necesarias por hasta ~1,5 y generar excedentes de partes que requieren otros canales; la logística de la red (CD o entrega a locales) es prioritaria (DPV-036).
- Metodología de dimensionamiento propuesta (DEC-014), sin parámetros ni capacidad calculada.

## Resultado del estudio de producción primaria (2026-09-29)

Síntesis en [`../03_produccion_primaria/conclusiones_produccion.md`](../03_produccion_primaria/conclusiones_produccion.md):

- Rangos (escenarios, no datos de campo): edad 38 / 47 / 54 d; peso vivo 2,4 / 2,9 / 3,4 kg; FCR de campo 1,60–1,85 a 2,9 kg; mortalidad en granja 3 / 5 / 8 % (un estudio de Entre Ríos registró 7,7–9,5 %: señal de riesgo a validar, DPV-044); ~5–7 ciclos/año (no 365/edad).
- Escenarios físicos hipotéticos de 2.500 / 5.000 / 10.000 / 20.000 **aves faenadas**/día (5 d/semana, perfil y desempeño medios): ~13.200 / 26.400 / 52.800 / 105.600 pollitos BB alojados por semana plena; ~3.100 / 6.200 / 12.400 / 24.700 t de alimento/año; ~9.500 / 19.000 / 37.900 / 75.900 m² de galpón (versión 1.1, tras la auditoría del modelo). Los supuestos mueven los m² hasta ~3,3 veces. **No son escala ni diseño.**
- +0,1 de FCR = +5,9 % de alimento. La superficie depende sobre todo de densidad, peso y ciclos.
- Riesgos críticos: IAAP, golpe de calor y fallas eléctricas, pollito BB concentrado, disponibilidad de integrados.
- Modelos de abastecimiento (propio / integrado / compra / mixto) comparados **sin ganador** (DEC-020). No se asume granja ni incubadora propia (SUP-034).

## Resultado del balance de masa (2026-09-30)

Síntesis en [`../04_balance_masa/conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md):

- Pollo de 2,9 kg (medio): carcasa eviscerada sin cuello ni menudencias **2,07 kg (71,5 %)**; rango 70,0–72,7 % según escenario y 70,2–72,6 % entre 2,2 y 3,5 kg. Con cuello y menudencias 77,9 %: **el "rendimiento" siempre debe declararse con su definición**.
- Cortes (medio, % de la carcasa apta): pechuga con hueso 38,5 %, pata-muslo 31,0 %, alas 10,2 %, carcasa-esqueleto 19,3 %; filet (suprema + solomillo) 20,5 % del peso vivo.
- Subproductos por ave: plumas 0,151 kg (0,241 kg húmedas), sangre 0,099 kg (85 % recuperable), cabeza 0,072 kg, vísceras no comestibles 0,165 kg, garras vendibles 0,101 kg, menudencias + cuello 0,185 kg.
- **Agua:** el chiller por inmersión agrega ~0,086 kg vendidos por ave (4 % del peso comercial); entre inmersión y aire hay 0,122 kg/ave (6 %) de diferencia. El agua se contabiliza aparte y nunca como carne (SUP-042).
- Entero / trozado / deshuesado: comestible 2,32 / 2,31 / 1,98 kg por ave; **sin ganador** (DEC-005). El peso cambia el mix de forma no lineal (DEC-021).
- 10.000 aves/día de 2,9 kg: 29 t/día de pollo vivo → 14,8 t/día de productos principales trozados, 9,2 t/día de coproductos, 5,3 t/día de subproductos, 1,3 t/día de residuos (masa del ave; no incluye el agua de proceso de la planta). **Escenario, no escala.**
- Nuevas decisiones: método de enfriamiento (DEC-026), destino de subproductos (DEC-027), ensayo de balance en planta (DEC-028).
- **Alcance:** es un balance de masa del ave y sus productos; **no dimensiona el consumo industrial de agua ni el caudal de efluentes**, ni energía, ni economía, ni maquinaria. Auditoría conceptual en [`../04_balance_masa/auditoria_balance.md`](../04_balance_masa/auditoria_balance.md).

## Resultado del mapa de productos y subproductos (2026-09-30)

Síntesis en [`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md):

- Pollo de 2,9 kg (trozado, V1): ~80 % del PV es comestible (A 48,8 % + B 30,9 %), 15,3 % subproductos C, 3,3 % residuos y 1,8 % pérdidas. **IAA técnico 95 %**; el IAA económico depende de compradores que hoy no están identificados (DEC-032).
- La **carcasa-esqueleto** (13,6 % PV; 4,1 t/día a 10.000 aves/día) es la tercera masa comestible y no tiene comprador identificado: vender / CMS / rendering sin ganador (DEC-029). La CMS, según extracto de la Res. SENASA 368/2003, solo puede usarse en chacinados cocidos y conservas (SUP-048).
- **Garras:** valor alto solo con Asia abierta; China no disponible confirmada. A 2.500 aves/día un contenedor tarda ~6 meses (DEC-031).
- **Subproductos C:** 5,3 t/día (trozado) a 8,6 t/día (deshuesado) a 10.000 aves/día; plumas 2,4 t/día. Sin comprador son costo (SUP-046). Rendering propio / tercerizado / venta directa comparados sin decisión; caso de referencia sin rendering propio (SUP-049).
- **Sangre:** recuperarla por separado reduce ~7 veces la DQO que llega al efluente, aunque no genere ingreso.
- Lista maestra de 44 precios a obtener (interno, exportación, subproductos, servicios) y 10 tareas de campo por actor; DPV-070 a DPV-081.
- **Alcance:** no se asignaron precios, no se eligió portafolio ni ruta, no se diseñó maquinaria ni se fijó escala.

## Resultado del modelo preliminar de escala (2026-09-30)

Síntesis en [`../23_plan_expansion/conclusiones_escala.md`](../23_plan_expansion/conclusiones_escala.md):

- **Con la demanda documentada (~0) ninguna escala está justificada:** la utilización respaldada por evidencia es 0 %. Demanda necesaria para llenar 2.500 / 5.000 / 10.000 / 20.000 aves faenadas/día: **4,1 / 8,2 / 16,4 / 32,8 t de peso comercial por día calendario** (ave completa, 5 d/sem; +20 % con 6 d; = 6,0 / 12,0 / 24,0 / 47,9 t por día de faena × 250/365); equivalente a 46 / 91 / 182 / 365 kg/local/día si todo pasara por los 90 locales.
- Contra los escenarios de prueba (factor demanda/capacidad; la utilización nunca supera 100 %): el **base** (7,5 t/día) excede 2.500 (factor 183–326 %, cobertura 31–55 %), ronda **5.000** (factor 91 % con ave completa; 124–163 % con mix de supermercado) y deja 10.000 con utilización 46–81 %; el **expansivo** (23,5 t/día) excede 10.000 (cobertura 39–70 %) y recién acerca 20.000 (factor 72–128 %). Aun con la planta llena, el mix deja **partes sin comprador** (3,0–6,7 t/día en el escenario base).
- Físico (medio, 5 d): 13.200 / 26.400 / 52.800 / 105.600 pollitos BB por semana plena; 9.500–75.900 m² de galpón; 3.100–24.700 t de alimento/año; 312–2.500 aves/h a 8 h netas; 1,3–10,7 t/día de subproductos C (hasta 17,3 con deshuese); 42–336 t de comestible en 7 días de producción (29–230 t en 7 días calendario de cobertura).
- El segundo turno es **capacidad teórica de la línea** (16 h netas) sujeta a verificar los demás cuellos de botella; el sexto día agrega ~20 % de **volumen anual** con la misma capacidad diaria; ninguno se afirma como crecimiento sin obra. La **escala mínima eficiente** (DPV-083) es un dato crítico pendiente: no se concluye que 2.500 sea chico ni 20.000 grande. La cercanía a granjas es una hipótesis a estudiar (DEC-003). Cinco arquitecturas de crecimiento y una matriz de ocho criterios **sin ganador** (DEC-033); gates con 18 variables medibles **sin umbrales** (DEC-034).
- **Alcance:** no se eligió escala; no se calcularon CAPEX, OPEX ni precios; no se seleccionaron maquinaria, proveedores, layout ni localización; el HTML solo se especificó (se construyó después como v0.1, ver más abajo).

## Resultado del proceso industrial y la maquinaria conceptual (2026-09-30, sesión 09A)

Síntesis en [`../05_proceso_industrial/conclusiones_proceso.md`](../05_proceso_industrial/conclusiones_proceso.md):

- Ritmo operativo a 8 h netas: 312 / 625 / 1.250 / 2.500 aves/h para 2.500–20.000 aves/día. **Capacidad de línea ≠ capacidad de planta** (equipo → cuello de botella → capacidad operativa → producción real). Disponibilidad y factor de velocidad solo como sensibilidad (SUP-061).
- Ecuación de 24 h (SUP-062): con 8 h netas la planta opera ~14–21 h/día; con 16 h netas la holgura es +0,9 / −2,8 / −8,3 h: **restricción severa, a validar; segundo turno ni asumido ni descartado** (DEC-036).
- 76 equipos conceptuales; evisceración manual **sin umbral fijo**; más automatización no es siempre mejor (DEC-037). Una vs dos líneas sin recomendación (DEC-038). Aturdido y enfriamiento sin elegir (DEC-041, DEC-026).
- Proveedores: BAADER CP396, Meyn LEAP y JBT Marel/Calisa2 como **declaración del fabricante** (evidencia fuerte, confirmada en revisión externa); sus capacidades son **nominales declaradas, no capacidad del proyecto**; el resto `[PVDP]`. Dato crítico: definición contractual de capacidad (DPV-097). **Sin proveedor elegido** (DEC-049).

## Resultado de la normativa preliminar (2026-09-30, sesión 09B)

Síntesis en [`../16_normativa_senasa/conclusiones_normativa.md`](../16_normativa_senasa/conclusiones_normativa.md):

- Cadena de cuatro niveles: habilitaciones locales → SENASA tránsito federal → autorización SENASA por destino → listado/aceptación del importador. Caso de referencia del análisis: tránsito federal (SUP-066), **no decidido** (DEC-009).
- Cambios 2025–2026 detectados solo en extractos (hipótesis de vigencia, SUP-067): Res. SENASA 592, 593, 591 y 233/2026; Res. 723/2025; Decreto 697/2026. El Plan APPCC es obligatorio regulatorio (Res. 205/2014, `[PVDP]`). La Ley 22.375 sigue en el corpus oficial.
- Estados de verificación preservados: `VERIFICADO EN PRIMARIA` (0), `PVDP`, `DEPENDE DE JURISDICCIÓN`, `POR CONSULTAR A SENASA`. Que el Decreto 697/2026 modifica/complementa el Decreto 815/1999 está **confirmado en revisión externa**; la lectura primaria queda pendiente de reproducir (DPV-107).
- Pendientes prioritarios: texto del Decreto 4238/68 (DPV-090), revisión del anteproyecto por SENASA (DPV-115), plazos reales (DPV-086), Decreto 697/2026 (DPV-107), Ley 22.375 (DPV-099), APPCC (DPV-102), Res. 233/2026 (DPV-100) y normativa por sitio (DPV-106).

## Resultado de agua, efluentes, energía y frío (2026-09-30, sesión 09C)

Síntesis en [`../11_agua_efluentes/conclusiones_agua_efluentes.md`](../11_agua_efluentes/conclusiones_agua_efluentes.md) y [`../12_energia_frio/conclusiones_energia_frio.md`](../12_energia_frio/conclusiones_energia_frio.md) (todo **sensibilidad top-down**, fuentes `[PVDP]`):

- Agua 15 / 25 / 38 L/ave (62–500 m³/día medio entre 2.500 y 20.000 aves/día); cinco aguas separadas; efluente ~1.000–1.200 kg DQO/día a 10.000 aves/día (medio) por dos métodos que **divergen en los extremos** → validación de campo. Lodos **PENDIENTES**.
- ~0,8 kWh/ave y potencia **media** equivalente (pico PENDIENTE de lista de cargas); ~1 MJ/ave (pico térmico PENDIENTE); carga sensible del producto ~99 kWf a 10.000 aves/día (carga frigorífica total PENDIENTE; brecha ×5,7 con el benchmark sin cerrar); congelado dominado por el perfil P1–P3; grupo electrógeno PENDIENTE.
- Agua, vuelco, potencia, gas y calidad de red son **criterios de localización** que pueden limitar la escala del sitio (DEC-003, DEC-043).

## Simulador HTML v0.1 (2026-09-30, sesión 09D)

Documentación en [`../23_plan_expansion/simulador_html/README.md`](../23_plan_expansion/simulador_html/README.md):

- **Ya existe** y funciona offline (abrir `index.html`; sin servidor ni Internet). Reproduce los modelos físicos aprobados (producción, balance, subproductos, escala) sin reimplementar el balance; comparador de escenarios A/B/C; etiquetas de certeza por cifra ("Calculado por modelo" ≠ validado en planta).
- **Sin economía:** CAPEX, OPEX, EBITDA, VAN, TIR y payback **pendientes** (pestaña deshabilitada). No integra todavía la capacidad de proceso (09A), utilities (09C), gates ni localización.
- Umbrales de alerta de interfaz — **no son límites industriales validados**: utilización < 50 % (umbral visual ilustrativo), inventario ≥ 7 días (umbral visual ilustrativo), FCR ±0,15 (criterio de interfaz), ganancia diaria ±15 % (criterio de interfaz). Registrados en la anotación de SUP-060.

## Plan de validación de campo (2026-09-30)

Síntesis en [`plan_trabajo_campo.md`](plan_trabajo_campo.md); matriz en [`matriz_validacion_campo.csv`](matriz_validacion_campo.csv):

- **Qué bloquea hoy la decisión (N1, 18 DPV):** capital y relación inversor–red (DPV-001, 038); acceso, locales, volumen, mix, fresco/congelado, proveedor actual, logística y condiciones de la red (DPV-002, 018, 003, 037, 085, 020, 036, 039); otros canales y precios de cortes y coproductos (DPV-040, 013, 070); façon, pollito, productores y costo del pollo vivo (DPV-006, 047, 048, 019); escala mínima eficiente (DPV-083). Diez de ellos dependen de la relación grupo inversor → red.
- **Orden de trabajo:** O0 preparación (góndola, carnicería, descargas) → **O1 inversores y red** (resuelve 10 N1) → O2 otros canales y precios (en paralelo) → O3 frigoríficos (façon y datos reales de proceso) → O4 productores e incubadoras → O5 subproductos → O6 SENASA → O7 maquinaria (sin cotizar hasta el hito H-B) → O8 terrenos. Exportación (O9) posterior.
- **Hitos de decisión del campo** (sin umbrales numéricos): H-A capital y ancla; H-B rango de escala y abastecimiento; H-C insumos para CAPEX/OPEX.
- **Instrumentos:** reunión única con inversores (maestro + 20 preguntas ejecutivas + minuta), plan comercial con escala E1–E6 (el interés verbal no es demanda), cuestionarios de productores (registro de 6–12 crianzas), incubadoras y subproductos, guía y hoja de visita a plantas, plan de RFQ con comparación por capas de costo (EXW/FOB ≠ instalado y en marcha), 12 preguntas a SENASA, ficha de terreno, data room fuera del repositorio.
- **Alcance:** no se investigaron tecnologías nuevas ni se construyeron modelos; no se inició localización, logística, layout, CAPEX ni OPEX.

## Próximos pasos

0. **No iniciar la fase siguiente hasta que el promotor lo indique** (instrucción 2026-09-29).
1. Validación de demanda de campo: aplicar el cuestionario a la red y al potencial inversor y ejecutar las tareas priorizadas de `02_clientes_demanda/conclusiones_demanda.md` §6 (DPV-002, DPV-003, DPV-018, DPV-020, DPV-036 a DPV-040). Evaluar una etapa de validación comercial previa a la inversión (DEC-018). *Actualización 2026-09-30:* el trabajo de campo completo quedó ordenado en [`plan_trabajo_campo.md`](plan_trabajo_campo.md); **primer paso: la reunión con el padre de Ramiro y los inversores** ([`../24_inversores/cuestionario_ejecutivo_inversores.md`](../24_inversores/cuestionario_ejecutivo_inversores.md)) y, en paralelo, las tareas de inicio inmediato (§5.4 del plan).
2. Verificación documental primaria de las cifras de mercado (requiere acceso de red o descarga manual) y completado de series (DPV-009, DPV-010, DPV-013, DPV-021).
3. Relevamiento de faena a façon y pollito BB; seguimiento del concurso de GTA sin supuestos (DPV-006, DPV-016).
4. ~~Sesión específica de estrategia exportadora~~ (realizada 2026-09-29). Pendiente: información de campo de exportación (DPV-024, DPV-026, DPV-027, DPV-032) y verificación de acceso por país (DPV-031).
5. Producción primaria (realizada 2026-09-29). Pendiente: datos de campo de desempeño (DPV-044), productores integrables (DPV-048), pollito BB (DPV-047), normativa completa (DPV-046) y manuales genéticos (DPV-045); preguntas en `03_produccion_primaria/guia_ramiro.md`. El balance de masa se realizó el 2026-09-30 (punto 6).
6. Balance de masa (realizado 2026-09-30). Pendiente: tablas genéticas de rendimiento (DPV-059), **ensayo en planta argentina** (DPV-060, DEC-028), normativa de agua y subproductos (DPV-061, DPV-066), decomisos (DPV-063), garras (DPV-064), rendering (DPV-065) y convenciones comerciales (DPV-068). El mapa de productos y subproductos se realizó el 2026-09-30 (punto 7). **No se iniciaron** maquinaria, layout ni escala óptima.
7. Mapa de productos y subproductos (realizado 2026-09-30). Pendiente: precios y compradores reales por parte y subproducto (tareas F1–F10 de `07_subproductos/conclusiones_valorizacion.md` §9; DPV-070 a DPV-081), receptores de rendering en zonas candidatas (DPV-065) y verificación de normativa de CMS, harinas, pet food y decomisos (DPV-066, DPV-073, DPV-074). **No se iniciaron** modelo financiero, maquinaria, escala óptima ni layout.

8. Modelo preliminar de escala (realizado 2026-09-30). Pendiente: datos **críticos antes de definir escala** — compras reales y mix de la red (DPV-003, DPV-037, DPV-085), evidencia de compromiso (DPV-002, DPV-020, DPV-038), canales para las partes excedentes (DPV-040, DPV-070), escala mínima eficiente (DPV-083), productores y pollitos (DPV-048, DPV-047) y faena a façon (DPV-006) — y calibración de gates (DEC-034). Lista priorizada en `23_plan_expansion/conclusiones_escala.md` §4. **No se iniciaron** CAPEX, OPEX, modelo financiero, maquinaria, layout, localización ni el HTML.

   *Actualización (reconciliación 2026-09-30):* después de ese punto se hicieron, en sesiones paralelas, proceso industrial y maquinaria conceptual (09A), normativa preliminar (09B), utilities (09C) y el simulador HTML v0.1 (09D); ver los resultados arriba.

9. Proceso, maquinaria, normativa y utilities (realizados 2026-09-30, modelos preliminares). Pendiente de **campo**: capacidad real y definición contractual de capacidad (DPV-088, DPV-097), servicio técnico y repuestos (DPV-089), limpieza y sanitización reales (DPV-091), productividad (DPV-092), texto del Decreto 4238/68 y revisión de anteproyecto con SENASA (DPV-090, DPV-115, DEC-042), agua, vuelco y efluentes reales (DPV-053, DPV-067, DPV-106, DPV-114), lista de cargas y balance frigorífico de proveedores (DPV-095, DPV-109). Lista completa en [`reconciliacion_sesiones_09.md`](reconciliacion_sesiones_09.md) §11.
10. Simulador HTML: v0.5 (variantes del balance, gates, datos de campo) y v1.0 (economía) **solo cuando existan** los módulos correspondientes.
11. **Próximos módulos técnicamente habilitados** (tienen insumos preliminares, pero **no se inician hasta que el promotor lo indique**): localización (`10`; criterios de 09B y 09C), logística detallada (`13`), layout y obra civil (`09`; zonificación de 09A y requisitos de 09B), recursos humanos (`18`; puestos equivalentes de 09A), CAPEX y OPEX (`19`, `20`; requieren cotizaciones y definición de alcance). Modelo financiero, riesgo financiero, decisión de escala y documentación para inversores dependen de los anteriores y del trabajo de campo.

Ver [`decisiones_pendientes.md`](decisiones_pendientes.md) y [`datos_por_validar.md`](datos_por_validar.md).
