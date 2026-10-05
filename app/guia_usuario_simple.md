# Guía de usuario — modo simple

Para alguien **sin conocimientos de ingeniería, finanzas ni del proyecto**. La app sirve para dos cosas: **ENTENDER EL PROYECTO** y **SIMULAR / TOMAR DECISIONES**. Todo lo que calcula es una **simulación** del escenario que se carga (o de la demo ficticia): nunca un dato real.

## 1. Empezar

1. En la terminal, desde la carpeta del proyecto: `python3 app/app.py`. Se abre el navegador en `http://127.0.0.1:8765/`.
2. La primera vez aparece **«¿QUERÉS UN RECORRIDO DE 2 MINUTOS?»**: **EMPEZAR RECORRIDO** abre la demo (datos ficticios) y guía 6 pasos (escenario → resultado → comparación → stress → optimizador → validación); **IR DIRECTO A LA APP** lo saltea. La elección se recuerda en el navegador.
3. **Inicio** («PROYECTO AVÍCOLA — NICAS & DOIPE») tiene cuatro botones grandes: **ENTENDER EL PROYECTO**, **SIMULAR UN ESCENARIO**, **COMPARAR / OPTIMIZAR** y **QUÉ FALTA VALIDAR**; debajo, **¿Dónde estamos parados?** y las preguntas clave (cómo funciona el negocio, dónde podría estar la planta, qué pasa dentro de la planta, qué sale de un pollo, las 5 arquitecturas, qué significa cada escala). El modo experto queda como enlace secundario.

## 2. Moverse por la app

| Elemento | Para qué |
|---|---|
| **Barra lateral** | Agrupada en PROYECTO (Inicio, Cómo funciona, Mercado, Producción, Planta y procesos, Productos, Localización, Logística, Infraestructura, Organización), ECONOMÍA (Inversión, Costos, Finanzas, Riesgos), DECISIÓN (Simular, Comparar, Optimizar, Qué falta validar, Para seguir avanzando), AVANZADO (Evidencia, Trazabilidad, Modo experto) y AYUDA (¿Dónde estamos?, Estudio completo, Diccionario) |
| **⌂ Inicio** | Siempre visible arriba a la izquierda |
| **Buscador** | Arriba: escribir «localización», «agua», «10.000», «faena», «CAPEX», «pollitos», «Chaco», «halal»… y Enter lleva a la sección |
| **Migas de pan** | Debajo de la barra: dónde estás (p. ej. INICIO › PROYECTO › PLANTA Y PROCESOS › PLANTA DE FAENA); cada parte es un enlace |
| **«?»** | Junto a términos técnicos (VAN, TIR, DSCR, CAPEX, OPEX, FCR, FTE, rendering, façon, ramp-up…): explicación de 1–3 frases |
| **Diccionario** | Todos los términos del glosario del proyecto, con búsqueda |

## 3. Entender el proyecto

- **Estudio completo**: los 26 temas (mercado, demanda, producción, balance de masa, productos, subproductos, proceso, maquinaria, agua, efluentes, energía, frío, normativa, exportación, localización, logística, layout, RR. HH., incubación, alimento, CAPEX, OPEX, capital de trabajo, finanzas, riesgos, optimizador).
- Cada tema responde **cinco preguntas**: ¿Qué es? · ¿Por qué importa? · ¿Qué modelamos? · ¿Qué sabemos hoy? · ¿Qué falta validar? (casilleros ☐ con los datos por validar del registro). Cada dato lleva un **chip de confianza**: ✔ Validado · ≈ Estimación · ~ Supuesto · ? Sin verificar (PVDP) · … Pendiente. Hoy ningún dato está validado en campo. **Ver fuentes** lista los documentos; **Ver detalle técnico** abre el documento original.
- **¿Cómo funciona el negocio?**: la cadena huevo/pollito → crianza → alimento → granjas → captura → transporte vivo → faena → enfriamiento → trozado → empaque → frío → logística → cliente, con las ramas subproductos, efluentes, rendering y exportación. Tocar un bloque muestra qué es y los números que ya calculó el estudio.
- **¿Dónde podría estar la planta?**: 13 regiones de 5 provincias, criterios (cercanía comercial, productores, servicios, logística, puertos…), condiciones duras y condicionales de un terreno y el estado de la información. **Todavía no existe una ubicación ganadora porque faltan datos de campo.** El esquema de distancias es un orden de magnitud no medido: no es un mapa ni un puntaje.
- **¿Qué pasa dentro de la planta?**: las etapas en orden; cada una muestra qué pasa, equipos de referencia (no son especificación ni cotización), capacidad para la escala elegida, agua y energía, riesgos y pendientes.
- **¿Qué sale de un pollo?**: cada parte en kg por ave del balance de masa. Las rutas (entero / trozado / deshuesado; carcasa vendida / CMS / rendering) son **alternativas**: no se suman.
- **Las 5 arquitecturas**: C0 Arranque asset-light, C1 Planta de faena propia, C2 Integración selectiva, C3 Mayor integración, CF Arquitectura futura, con PROPIO / TERCERIZADO / MIXTO / FUTURO para faena, granjas, pollitos, alimento, flota, frío, subproductos, rendering y reproductoras (definición exacta debajo de cada casilla).
- **¿Qué significa cada escala?**: 2.500 / 5.000 / 10.000 / 20.000 aves por día → aves por año, producto, pollitos, alimento, galpones, superficie, terreno, personal, agua, energía y demanda necesaria. **Capacidad no significa que vayamos a vender todo.**
- **¿Dónde estamos parados?**: MOTOR ✅ COMPLETO · DATOS FÍSICOS ⚠ PARCIALES · DATOS ECONÓMICOS ⚠ MUY INCOMPLETOS · EVIDENCIA 0 % · DECISIÓN REAL ⛔ NO DISPONIBLE; qué está terminado, qué falta, qué se puede simular y qué no se puede decidir todavía.

## 4. Simular un escenario (5 preguntas)

«Paso X de 5», con **ATRÁS** y **CONTINUAR** (volver atrás no borra nada).

| Paso | Pregunta | «No sé» significa |
|---|---|---|
| 1 | ¿Qué querés lograr? (Ganar más · Invertir menos · Recuperar rápido · Reducir riesgo · Crecer · Balanceado) | Se ordena por «Ganar más» solo como referencia |
| 2 | ¿Cuánto capital querés simular? | Sin límite de capital: la simulación no dice si la plata alcanza. **USD 2 M no se usa por defecto** |
| 3 | ¿Cuánta demanda querés simular? (producto, t/día y respaldo) | Sin demanda no hay ventas: no se calculan ingresos, EBITDA, VAN, TIR ni payback. **Los ~90 supermercados no son demanda por sí solos** |
| 4 | ¿Automático o una alternativa? (arquitectura y tamaño) | — («Automático» prueba todas) |
| 5 | ¿Tenés precios o costos propios? | Sin precios no se calcula rentabilidad. Costo vacío = pendiente (nunca 0) |

**Balanceado**: cada criterio lleva un % y el total tiene que dar **100 %** (botón **REPARTIR POR IGUAL**). Sin pesos **no se ejecuta** (y eso no significa «no invertir»). «Recuperar rápido» no es un criterio del balanceado del motor: si es lo más importante, elegí ese objetivo.

**⚙ Ajustar supuestos** (opcional): moneda y tipo de cambio, escala intermedia, todos los campos de demanda y precios, condiciones que la alternativa debe cumplir y horizonte. Lo demás (CAPEX, OPEX por módulo, impuestos, tasa, deuda, stress) está en el modo experto.

## 5. Leer el resultado

1. **Una frase arriba**: «Con los datos que cargaste, esta alternativa es la que mejor cumple tu objetivo dentro de la simulación.» o «Todavía faltan datos para calcular rentabilidad.» (si la regla de decisión indica no comprometer capital, lo dice y aclara que **no es un fracaso**).
2. **Hasta 6 números**: Inversión, VAN, TIR, Payback, EBITDA y DSCR mínimo del horizonte (o pico de fondos si no hay deuda), cada uno con su «?» y una frase: VAN «Cuánto valor genera el proyecto por encima de la rentabilidad mínima que le exigís.», TIR «Rentabilidad implícita estimada del escenario.», Payback «Tiempo aproximado para recuperar la inversión.», EBITDA «Resultado operativo antes de intereses, impuestos y depreciaciones.»
3. Si un número no se puede calcular se explica en castellano («No se puede calcular todavía porque falta el precio de venta.») y el **código técnico** queda debajo, en chico.
4. **DSCR mínimo del horizonte**: el período más ajustado de toda la proyección. Si cae en el arranque (ramp-up) se avisa: no significa que la deuda sea impagable; se muestra también el más bajo en operación madura.
5. Acordeones: **VER INVERSIÓN · VER RENTABILIDAD · VER RIESGOS · VER DETALLES TÉCNICOS** (tarjetas completas, semáforo, alertas, «¿por qué me da este resultado?», exportaciones y gráficos).

## 6. Decidir qué hacer

- **Qué falta validar**: checklist por tema (clientes, planta, alimento, pollitos, granjas, utilities, terreno, logística, RR. HH., impuestos, financiamiento, exportación): estado, a quién pedir, qué pedir, unidad, por qué importa y qué destraba. Ningún casillero se marca sin evidencia.
- **Para seguir avanzando**: qué hacer ahora, por prioridad del motor. Los empates se muestran como empates («PRIORIDAD 1 — EMPATE»).
- **Comparar / Optimizar / Riesgos**: si todavía no hay datos suficientes, la pantalla explica qué hacer y ofrece **CREAR ESCENARIO**.
