# Guía de usuario — modo simple

Para dueño, inversor o gerente. No hace falta saber de modelos: la app pregunta poco y explica los resultados en lenguaje claro. **Todo lo que calcula es una simulación del escenario que usted carga** (o de la demo ficticia).

## 1. Empezar

1. En la terminal, desde la carpeta del proyecto: `python3 app/app.py`. Se abre el navegador en `http://127.0.0.1:8765/`.
2. Pantalla **¿QUÉ QUERÉS HACER?**: Simular un negocio · Comparar alternativas · Optimizar · Ver riesgos · Qué me falta validar · Ver datos / evidencia · Modo experto.
3. ¿Primera vez? **Abrir demo** (datos inventados, rótulo ✱ SOLO DEMOSTRACIÓN) o **Empezar un escenario vacío**.
4. Arriba se ve siempre el escenario actual, su tipo y si hay cambios sin guardar. **Guardar** lo guarda en su computadora (los presets y la demo se guardan como copia).

## 2. Simular un negocio (7 pasos)

| Paso | Qué carga | Cómo lo usa el motor |
|---|---|---|
| 1 · Objetivo | Ganar más · Invertir menos · Recuperar rápido · Reducir riesgo · Crecer · Balanceado | Se traduce a un objetivo del optimizador y se muestra cuál (MAX_VAN, MIN_FONDOS_INICIALES, MIN_PAYBACK, MAX_ROBUSTEZ, MAX_CRECIMIENTO, BALANCEADO). Balanceado pide **sus** pesos; sin pesos no ordena (PESOS_NO_DEFINIDOS) |
| 2 · Capital | Monto en USD o ARS, o **No sé** | «No sé» = sin restricción de capital. **USD 2 M no es un valor por defecto.** ARS exige tipo de cambio, tipo de TC y fecha |
| 3 · Demanda | Líneas producto · canal · categoría · volumen (kg/día, t/día, t/mes, t/año) | **Que un cliente pueda comprar no significa que la demanda esté asegurada.** ASEGURADA / DOCUMENTADA necesitan respaldo; POTENCIAL / ESCENARIO son hipótesis. La app no convierte potencial en asegurada. «Toma todo» = canal de liquidación (demanda supuesta ilimitada) |
| 4 · Precios | Venta por producto y canal; costos de alimento, pollito y façon | Cada valor lleva unidad, fuente y estado: **Validado** (declarado por usted), **Cotización**, **Escenario** (simulación) o **No sé** (queda PENDIENTE, nunca 0). Los costos unitarios se convierten a costo anual con la cantidad que calcula el módulo de costos para cada alternativa |
| 5 · Arquitectura | **Automática** (el optimizador prueba las válidas) o **Quiero probar** C0, C1, C2, C3, CF | «¿Qué significa esto?» explica cada una en simple, con su definición técnica |
| 6 · Escala | 2.500 · 5.000 · 10.000 · 20.000 aves/día, intermedia (2.500–20.000) o AUTO | Fuera del rango que el motor puede evaluar no se ofrece |
| 7 · Restricciones | Máximo capital, payback máximo, VAN mínimo, TIR mínima, DSCR mínimo, riesgo máximo, terreno máximo, demanda disponible; horizonte | Todas opcionales; se aplican como obligatorias (HARD). La «demanda disponible» se usa en la consulta de demanda del motor |

Luego **SIMULAR**.

> Lo que no está en estos pasos (CAPEX, OPEX por módulo, impuestos, tasas, financiamiento, ramp-up) se carga en el **modo experto**. Si falta, el resultado lo dice.

## 3. Leer el resultado

- **Rótulo** arriba: ◇ SIMULACIÓN HIPOTÉTICA (o ✱ SOLO DEMOSTRACIÓN). Nunca es un dato real.
- **Tarjetas**: Alternativa · Inversión (CAPEX, capital de trabajo, fondos iniciales, pico de fondos) · Negocio (ventas, facturación, EBITDA, margen) · Retorno (VAN, TIR, payback) · Deuda (DSCR) · Riesgo (semáforo, robustez, score ordinal) · Evidencia (cobertura, respaldo comercial) · Principal limitación · Qué hacer ahora.
- Cada número viene con una frase: p. ej. «En este escenario el proyecto crearía valor por encima de la tasa de descuento usada (12 %)», o «El flujo cubriría 1,45 veces el servicio de deuda en el período más ajustado».
- **NO CALCULABLE**: si falta un dato no se muestra USD 0, 0 % ni 0 años; se muestra NO CALCULABLE y debajo qué falta («Falta precio de venta», «Falta CAPEX completo»…).
- **Semáforo**: 🟢 VERDE evaluable, cumple todo, físico confirmado y 100 % evidencia · 🟡 AMARILLO evaluable con evidencia o físico pendiente · 🔴 ROJO incumple una restricción obligatoria o un requisito físico · ⚪ GRIS no evaluable. Siempre con texto (botón «leyenda»).
- **¿Por qué me da este resultado?**: drivers principales, restricciones, datos usados (motor / escenario / pendientes), sensibilidades, qué cambiaría la decisión y la segunda alternativa.
- **NO_INVERTIR_AUN**: si gana, no es un fracaso. Significa que, con las restricciones y datos cargados, ninguna inversión productiva cumple los criterios; se muestran las reglas reales del motor (SQ-1…SQ-6) y caminos posibles (asset-light o validar más información).
- **Exportar**: JSON (escenario), CSV (resultado con etiquetas) y **Resumen imprimible** (HTML para imprimir o guardar como PDF).

## 4. Otras pantallas

- **Comparar**: elegir 2 a 5 alternativas. Si una no es comparable (faltan datos u otra base), la app lo explica y no la ordena.
- **Optimizar**: objetivo, capital, demanda, restricciones, riesgo y horizonte → mejor alternativa **del escenario**, segunda, diferencia, por qué gana, qué podría hacerla perder, restricciones y datos faltantes.
- **Riesgos**: ¿Qué pasa si…? (−30 % a +30 %), tornado, 2D, stress editable, puntos de quiebre («¿hasta dónde aguanta?») y Monte Carlo (NO DISPONIBLE si no hay distribuciones respaldadas; si corre, es probabilidad **simulada**).
- **Validación**: los 12 paquetes (clientes, planta, alimento, pollitos, granjas, utilities, terreno, logística, RR. HH., impuestos, financiamiento, exportación), a quién pedir qué, en qué unidad y qué desbloquea; prioridad del motor con empates; progreso separado en estructura / física / económica / evidencia; carga de cotizaciones a STAGING.
- **Evidencia**: qué datos reales hay hoy (solo lectura).
