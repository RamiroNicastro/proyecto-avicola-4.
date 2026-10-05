# Guion de la presentación — Paquete ejecutivo V1

**Fecha:** 2026-10-05 · **Archivo:** [`presentacion_nicas_doipe_v1.pptx`](presentacion_nicas_doipe_v1.pptx) · **Generado por:** [`generar_presentacion.js`](generar_presentacion.js) (este guion y las notas del PPTX salen del mismo texto; no editar a mano: editar el script y regenerar).

> Estado que la presentación sostiene en todo momento: **MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO** ([`../00_gestion_proyecto/auditoria_final_motor_v1.md`](../00_gestion_proyecto/auditoria_final_motor_v1.md) §30). No contiene montos de CAPEX/OPEX, rentabilidades ni recomendación de inversión.

**Duración sugerida:** 30–35 minutos para las láminas 1–23 (≈ 1,5 min por lámina) + preguntas. El anexo (24–29) se usa solo si la audiencia es técnica.

| # | Lámina | Mensaje |
|---|---|---|
| 1 | Portada | Proyecto avícola Nicas & Doipe: Motor V1 + App V1. |
| 2 | Mensaje ejecutivo | MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO. |
| 3 | Qué estamos intentando construir | De una carnicería familiar a una posible empresa avícola integrada, por etapas. |
| 4 | Cómo funciona el negocio | La cadena va del pollito al cliente, con ramas de subproductos, efluentes, frío y exportación. |
| 5 | Qué estudiamos | Se estudió la cadena completa: de la granja a las finanzas, más una app. |
| 6 | Demanda y mercado | Los ~90 supermercados son demanda POTENCIAL; la demanda documentada hoy es ≈ 0. |
| 7 | Alternativas de negocio C0–CF | Cinco arquitecturas, de la más liviana (C0) a la más integrada (CF); ninguna elegida ni costeable hoy. |
| 8 | Escalas | 2.500 / 5.000 / 10.000 / 20.000 aves/día: tamaños de referencia; capacidad ≠ venta garantizada. |
| 9 | Planta y proceso industrial | Doce pasos simplificados de un proceso de 32 etapas; la capacidad real depende de cotizaciones y visitas. |
| 10 | Productos y subproductos | Un pollo se divide en partes con mercados distintos; las rutas entero / trozado / deshuesado / CMS son excluyentes. |
| 11 | Localización | 13 corredores en 5 provincias; sin ranking ganador (0 de 624 datos verificados). |
| 12 | Layout e infraestructura | Terreno conceptual ≈ 2 a 4,4 ha según escala; el terreno real depende del municipio, los efluentes y la expansión. |
| 13 | CAPEX | El motor de inversión está estructurado, pero no hay CAPEX total: 167 de 175 conceptos sin precio. |
| 14 | OPEX y capital de trabajo | Estructura de costos completa; precios casi inexistentes; ninguna alternativa costeable. |
| 15 | Modelo financiero | Calcula EBITDA, FCFF, VAN, TIR, payback y DSCR; hoy 0 corridas publicables con evidencia; en escenarios sí simula. |
| 16 | Riesgos y optimizador | Sensibilidad, stress, quiebres, Monte Carlo preparado y optimizador; NO_INVERTIR_AUN es una respuesta posible. |
| 17 | App V1 (1): entender | La app explica el proyecto en lenguaje simple y muestra el estado real del estudio. |
| 18 | App V1 (2): simular | Modo simple de 5 preguntas para la familia; modo experto para análisis; todo resultado es SIMULACIÓN. |
| 19 | Qué falta validar | 12 paquetes de campo; los 5 de prioridad 1 (clientes, planta, alimento, pollitos, granjas) bloquean todo resultado económico. |
| 20 | Roadmap recomendado | Validar demanda → cotizar → terreno y servicios → escenario financiero real → decisión. |
| 21 | Decisiones abiertas | Escala, arquitectura, terreno, faena, alimento, pollito, flota y financiamiento siguen abiertas (104 en el registro). |
| 22 | Qué puede decidirse hoy | Hoy no se decide la inversión; sí qué datos buscar, qué simular y qué alternativas mantener en estudio. |
| 23 | Conclusión | Motor V1 completo, App V1 lista, decisión real pendiente; próximo paso: trabajo de campo y cotizaciones. |
| 24 | Anexo técnico (portada) | Material de respaldo para una audiencia técnica. |
| 25 | A1 · Arquitectura de motores | Datos físicos → CAPEX y OPEX → financiero → riesgo/optimizador → app; evidencia y escenario separados. |
| 26 | A2 · Evidencia | Solo E1–E3 cuentan como evidencia; hoy hay 0 % de cobertura de evidencia. |
| 27 | A3 · Tests | 70/70 pruebas de integración, 15/15 mutaciones detectadas; las pruebas validan coherencia, no datos. |
| 28 | A4 · Tensiones abiertas | 76 tensiones (71 abiertas); las principales son precios, rendimientos, pico de fondos, upstream, IIBB y comparabilidad. |
| 29 | A5 · Glosario | Términos técnicos explicados en una línea. |

## 1. Portada

**Mensaje:** Proyecto avícola Nicas & Doipe: Motor V1 + App V1.

**Notas del presentador:** Buenas. Esta presentación resume dónde está el estudio del proyecto avícola Nicas & Doipe. Les adelanto el mensaje en una frase: construimos una herramienta completa para analizar el negocio (el Motor V1 y la App V1), pero todavía no tenemos los datos reales necesarios para decidir si conviene invertir. Hoy no vamos a mostrar cuánto cuesta la planta ni cuánto gana: esos números todavía no existen con respaldo. Vamos a mostrar qué se estudió, qué se puede hacer con la herramienta y qué falta conseguir. Duración sugerida: 1 minuto.

## 2. Mensaje ejecutivo

**Mensaje:** MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO.

**Notas del presentador:** Tres mensajes y nada más. Primero: el motor está completo estructuralmente; es decir, todos los modelos existen, están conectados y pasan sus pruebas. Segundo: la app está lista; cualquiera puede usarla sin saber programar. Tercero, y es el más importante: el proyecto NO está listo para una decisión real de inversión. No es un problema de la herramienta: es que todavía no hay clientes confirmados, ni precios, ni cotizaciones, ni costos reales. De 180 datos que hay que validar, hoy hay 0 validados. Abajo está la clave de colores que vamos a usar en todas las láminas: verde es evidencia real (hoy prácticamente no hay), azul es una estimación del modelo, violeta es un escenario hipotético para simular, y naranja es pendiente. Si un número no tiene etiqueta verde, no es un dato real.

## 3. Qué estamos intentando construir

**Mensaje:** De una carnicería familiar a una posible empresa avícola integrada, por etapas.

**Notas del presentador:** El punto de partida es concreto: una carnicería familiar en el AMBA. No hay granjas, ni frigorífico, ni terreno, ni máquinas. Hay un grupo inversor que mencionó unos 2 millones de dólares, pero no están comprometidos: los usamos solo como referencia. Y hay una red de unos 90 supermercados que podría ser un canal, pero no sabemos todavía cuánto compraría ni a qué precio. Lo que se estudia es si tiene sentido construir, por etapas, una empresa avícola integrada que pueda vender a varios canales y, más adelante, exportar. La idea central del negocio es sacar el mayor ingreso posible de cada pollo, vendiendo cada parte donde mejor se paga. Y nada se da por sentado: cada eslabón —granjas, alimento, faena, flota— se analiza para ver si conviene hacerlo, comprarlo, tercerizarlo o dejarlo para después.

## 4. Cómo funciona el negocio

**Mensaje:** La cadena va del pollito al cliente, con ramas de subproductos, efluentes, frío y exportación.

**Notas del presentador:** Así funciona el negocio del pollo parrillero, de izquierda a derecha. Se compra o se produce un pollito de un día. Se cría en una granja, en galpones. Lo que más se mueve en todo el sistema es el alimento: son miles de toneladas por año. Cuando el pollo llega al peso, se lo transporta vivo a la planta. En la planta se faena, se enfría, se corta en trozos y se empaca. Salen productos —pollo entero, cortes, menudencias— que van a distintos clientes. Abajo están las ramas que no se ven pero pesan mucho: los subproductos (plumas, sangre, vísceras), el agua sucia que hay que tratar, el frío, y la exportación como canal futuro. Cada uno de estos bloques es un tema que se estudió por separado y después se conectó con los demás.

## 5. Qué estudiamos

**Mensaje:** Se estudió la cadena completa: de la granja a las finanzas, más una app.

**Notas del presentador:** Esto es todo lo que se estudió. No es solo una planilla de costos: se modeló la producción en granja, qué sale de cada pollo, la planta y sus etapas, las máquinas necesarias, el agua, los efluentes, la energía, el frío, el terreno, la logística, dónde podría ubicarse la planta, el personal, el alimento y la incubación, la inversión, los costos, las finanzas, los riesgos y, al final, una app para usar todo junto. Son 25 módulos y todos están terminados como modelo. Pero ninguno está validado con datos de campo: los números físicos son estimaciones del modelo, y los números económicos directamente no existen todavía.

## 6. Demanda y mercado

**Mensaje:** Los ~90 supermercados son demanda POTENCIAL; la demanda documentada hoy es ≈ 0.

**Notas del presentador:** Esta lámina es clave. No toda la demanda vale lo mismo. De izquierda a derecha: un escenario es una hipótesis nuestra para simular. Potencial es un canal posible, sin ningún compromiso. Interesada es cuando alguien dice «me interesa», pero sin volumen firme. Negociada es cuando ya se habla de volumen y precio. Y asegurada es cuando hay un contrato o una compra documentada. Los 90 supermercados hoy están en «potencial»: no sabemos cuánto comprarían, a qué precio, ni con qué plazo de pago. Por eso la demanda documentada hoy es prácticamente cero. El motor respeta esto: cuando trabaja con datos reales, solo cuenta como venta lo asegurado. Si queremos imaginar que los supermercados compran, lo podemos simular, pero queda rotulado como escenario. Y aunque se confirmen, los supermercados no definen el tamaño de la empresa: pueden ser un cliente ancla, pero el resto del pollo tiene que ir a otros canales.

## 7. Alternativas de negocio C0–CF

**Mensaje:** Cinco arquitecturas, de la más liviana (C0) a la más integrada (CF); ninguna elegida ni costeable hoy.

**Notas del presentador:** Hay cinco formas de armar la empresa, y las llamamos C0 a CF. C0 es el arranque liviano: casi sin activos propios. Compramos pollitos, los crían productores integrados y otro frigorífico los faena por nosotros cobrando una tarifa; eso se llama façon. C1 es tener nuestra propia planta de faena, pero seguir comprando pollito y alimento y trabajar con granjas de terceros. C2 suma una parte de granjas propias. C3 integra casi todo: granjas, incubadora y planta de alimento. Y CF es una visión futura, con reproductoras y procesamiento propio de subproductos. De izquierda a derecha aumenta la inversión propia, el control y la complejidad; hacia la izquierda se depende más de terceros. Importante: ninguna está elegida, y hoy ninguna se puede costear porque faltan precios. No hay que suponer que la integración total es mejor: eso lo tienen que decir los datos.

## 8. Escalas

**Mensaje:** 2.500 / 5.000 / 10.000 / 20.000 aves/día: tamaños de referencia; capacidad ≠ venta garantizada.

**Notas del presentador:** Se estudiaron cuatro tamaños de planta de referencia, medidos en aves faenadas por día: 2.500, 5.000, 10.000 y 20.000. Para dar una idea: una planta de 10.000 aves por día faena unos 2,5 millones de pollos por año, necesita unos 52.800 pollitos por semana y unas 12.400 toneladas de alimento por año. Estos números son estimaciones del modelo, no datos de campo. El recuadro azul de cada columna dice cuánto habría que vender para llenar esa planta. Por ejemplo, 20.000 aves por día equivalen a unos 365 kilos por local y por día si todo fuera a los 90 supermercados, que es más de lo que el rango de la red parece absorber. El mensaje de fondo: tener capacidad no significa vender. Con la demanda documentada de hoy, que es casi cero, ninguna escala está justificada. La escala se elige después de validar la demanda.

## 9. Planta y proceso industrial

**Mensaje:** Doce pasos simplificados de un proceso de 32 etapas; la capacidad real depende de cotizaciones y visitas.

**Notas del presentador:** Esto es lo que pasa adentro de la planta, simplificado en doce pasos. Arriba, la zona sucia: el pollo llega vivo, se lo cuelga, se lo aturde para que no sufra, se lo desangra, se lo escalda con agua caliente y se le sacan las plumas. Después pasa a la zona limpia, separada por higiene: se lo eviscera con inspección veterinaria, se lo enfría —que es un punto crítico de inocuidad—, se lo corta, se lo empaca, se guarda en frío y se despacha. En el modelo completo son 32 etapas, más las salas de garras, menudencias y carcasa. Algo importante: lo que dice un catálogo de fabricante no es la capacidad real de la planta. Eso se conoce con una cotización formal y visitando plantas en funcionamiento. Todavía no se pidieron cotizaciones ni se eligió proveedor.

## 10. Productos y subproductos

**Mensaje:** Un pollo se divide en partes con mercados distintos; las rutas entero / trozado / deshuesado / CMS son excluyentes.

**Notas del presentador:** De un pollo vivo de 2,9 kilos, según el modelo, salen unos 780 gramos de pechuga con hueso, unos 630 de pata-muslo, casi 400 de carcasa, unos 200 de alas, y después menudencias, patas, sangre, plumas, vísceras, cuello y cabeza. Son estimaciones con rendimientos de referencia; falta medirlo en una planta argentina. A la derecha, una aclaración importante: el mismo pollo no se puede vender de todas las formas a la vez. O se vende entero, o trozado, o deshuesado. Y la carcasa o se vende, o se convierte en carne mecánicamente separada, o va a rendering. Por eso no se suman los kilos de rutas distintas. El objetivo del negocio es que cada parte vaya al mercado que más la paga: por ejemplo, garras para exportación, pechuga al supermercado. Para calcular eso hacen falta precios por producto y canal, que todavía no tenemos.

## 11. Localización

**Mensaje:** 13 corredores en 5 provincias; sin ranking ganador (0 de 624 datos verificados).

**Notas del presentador:** ¿Dónde iría la planta? Se estudiaron 13 corredores en cinco provincias: Buenos Aires, Entre Ríos, Santa Fe, Córdoba y Chaco. Están listados sin orden de preferencia. Se armó una matriz para compararlos con decenas de criterios: distancia al mercado, granjas cercanas, granos, agua, energía, rutas, costo de la tierra, riesgo sanitario. Pero de 624 casilleros de esa matriz, hoy hay cero verificados. Por eso el modelo no da un ganador, y lo dice explícitamente en lugar de inventar un orden. Hay cuatro condiciones que pueden descartar un terreno concreto: que el uso de suelo no lo permita, que no haya agua, que no se puedan tratar los efluentes o que no llegue la energía. Otras —vecinos, accesos, inundabilidad, gas, potencia, a quién se le venden los subproductos— no descartan, pero encarecen o condicionan. Y un punto de método: tener un contacto en Chaco es una ventaja, pero no es un criterio para elegir.

## 12. Layout e infraestructura

**Mensaje:** Terreno conceptual ≈ 2 a 4,4 ha según escala; el terreno real depende del municipio, los efluentes y la expansión.

**Notas del presentador:** El dibujo de la izquierda no es un plano: es un esquema de qué ocupa lugar en el terreno. La planta construida, las cámaras de frío, la planta de tratamiento de efluentes, una reserva para crecer y los accesos para camiones. El modelo estima un terreno conceptual de unas 2 hectáreas para la escala más chica y unas 4,4 para la más grande. Es un orden de magnitud. La planta se organizó en 54 áreas y 9 zonas, respetando los flujos de higiene. Pero no hay planos ni anteproyecto. ¿Por qué el terreno real puede ser distinto? Porque depende de lo que permita el municipio, de qué tecnología se use para tratar los efluentes, y de cuánto se quiera reservar para crecer. Esa última es una decisión todavía abierta.

## 13. CAPEX

**Mensaje:** El motor de inversión está estructurado, pero no hay CAPEX total: 167 de 175 conceptos sin precio.

**Notas del presentador:** CAPEX es la inversión: lo que hay que comprar o construir antes de operar. El motor ya tiene la lista: 175 conceptos de inversión, según la alternativa y la escala. Lo que no tiene son precios. 167 conceptos no tienen ningún precio, y los 8 que tienen alguna referencia son débiles: salieron de notas de prensa o páginas web, sin verificar. Por eso el motor responde «no disponible» en lugar de dar un total engañoso. Y por eso tampoco comparamos con los 2 millones: con 1 o 2 % de los precios no se puede decir ni que alcanza ni que no alcanza. Para tener un total hacen falta cotizaciones de la línea de faena, el frío, los efluentes, la obra civil, el terreno, los galpones si hubiera granjas propias, y la importación e instalación.

## 14. OPEX y capital de trabajo

**Mensaje:** Estructura de costos completa; precios casi inexistentes; ninguna alternativa costeable.

**Notas del presentador:** OPEX son los costos de operar: alimento, pollitos, sueldos, energía, fletes. El gráfico muestra tres niveles de conocimiento para cada alternativa. La barra verde oscura dice que conocemos el 100 % de los costos que existen: sabemos qué hay que pagar. La azul dice que de entre el 43 y el 62 % sabemos cuántas unidades se usan. Y la amarilla, casi invisible, dice cuánto sabemos de cuánto cuestan: menos del 10 %. Con esto no se puede calcular el costo por pollo ni el capital de trabajo. Faltan, sobre todo, precios de alimento, pollito, tarifa de façon, sueldos, servicios, fletes y los plazos de pago. El capital de trabajo es la plata que queda atada en mercadería y en lo que los clientes todavía no pagaron; en avicultura puede ser importante y por eso el modelo lo trata aparte.

## 15. Modelo financiero

**Mensaje:** Calcula EBITDA, FCFF, VAN, TIR, payback y DSCR; hoy 0 corridas publicables con evidencia; en escenarios sí simula.

**Notas del presentador:** El modelo financiero es el que junta todo y calcula los indicadores clásicos. A la izquierda, en castellano: EBITDA es lo que deja la operación; el flujo de caja es la plata que genera el proyecto después de invertir; el VAN dice cuánto valor crea por encima de lo que se le exige; la TIR es la rentabilidad implícita; el payback es cuánto tarda en recuperar la inversión; y el DSCR mide si alcanza la caja para pagar la deuda. El modelo funciona en dos modos. En modo evidencia, solo con datos reales, hoy no puede publicar ningún resultado: de las 61 corridas de referencia del modelo, 42 son en modo evidencia y ninguna es publicable (las otras 19 son plantillas de escenario sin datos cargados, tampoco publicables). Lo mismo con las 54 alternativas del optimizador. Eso es lo correcto, porque no hay precios. En modo escenario, sí puede simular: si cargamos precios y costos hipotéticos, calcula todo, pero el resultado sale marcado como simulación y nunca se guarda como si fuera real. Un hallazgo ya útil: la plata que hace falta no es solo la inversión en la planta. Hay que sumar las pérdidas del arranque y el capital de trabajo; por eso el modelo mide el pico de fondos.

## 16. Riesgos y optimizador

**Mensaje:** Sensibilidad, stress, quiebres, Monte Carlo preparado y optimizador; NO_INVERTIR_AUN es una respuesta posible.

**Notas del presentador:** Esta capa sirve para preguntar «¿y si…?». La sensibilidad mueve una variable por vez: ¿qué pasa si el alimento sube un 20 %? El stress mueve varias juntas, como en una crisis. Los puntos de quiebre buscan el límite: ¿hasta qué precio de venta el proyecto sigue en pie? El Monte Carlo está preparado, pero no lo usamos porque inventar probabilidades sería engañoso. Y el optimizador compara alternativas según el objetivo que elija el inversor: ganar más, invertir menos, recuperar rápido o arriesgar menos. Algo muy importante: el optimizador puede responder «no invertir aún». No es un error ni un fracaso; es una respuesta válida cuando los datos dicen que ninguna opción cumple las condiciones. Además hay 34 riesgos identificados —gripe aviar, precio de granos, tipo de cambio, energía— cuya probabilidad específica para este proyecto todavía no se puede estimar. Todo esto hoy funciona solo con escenarios hipotéticos, porque con datos reales no hay todavía resultados que estresar.

## 17. App V1 (1): entender

**Mensaje:** La app explica el proyecto en lenguaje simple y muestra el estado real del estudio.

**Notas del presentador:** Esta es la pantalla de inicio real de la app. Tiene cuatro botones grandes: entender el proyecto, simular un escenario, comparar u optimizar, y ver qué falta validar. Debajo está el resumen de dónde estamos parados: motor completo, datos físicos parciales, datos económicos muy incompletos, evidencia cero por ciento y decisión real no disponible. Es la misma conclusión de esta presentación, y la app la muestra siempre. Está pensada para alguien que no es ingeniero ni financista: cada tema se explica con cinco preguntas simples, y cada palabra técnica tiene un signo de pregunta con una explicación corta. Se usa en una computadora, sin internet, ejecutando un solo comando.

## 18. App V1 (2): simular

**Mensaje:** Modo simple de 5 preguntas para la familia; modo experto para análisis; todo resultado es SIMULACIÓN.

**Notas del presentador:** A la izquierda, el modo simple: cinco preguntas, una por pantalla. Qué querés lograr, cuánto capital querés simular, cuánta demanda, qué alternativa y si tenés precios. Si no se sabe algo, se responde «no sé» y la app lo deja como pendiente; nunca lo rellena con un cero, porque eso daría resultados falsos. Por ejemplo, si no se carga demanda, no hay ventas y la app no calcula rentabilidad. Y los 2 millones no se usan por defecto. A la derecha, la pantalla que explica qué se puede simular hoy y qué no se puede decidir. El modo experto permite tocar todos los datos del motor, para quien quiera analizar en detalle. Todo lo que calcula la app con datos inventados por el usuario sale con la etiqueta simulación, en violeta, arriba de la pantalla.

## 19. Qué falta validar

**Mensaje:** 12 paquetes de campo; los 5 de prioridad 1 (clientes, planta, alimento, pollitos, granjas) bloquean todo resultado económico.

**Notas del presentador:** Este es el trabajo que sigue. Todo lo que falta se agrupó en 12 paquetes, cada uno con a quién hay que pedirle, qué pedir y en qué unidad. Los cinco en rojo son prioridad uno: clientes, planta y maquinaria, alimento, pollitos y granjas. Sin ellos, ningún resultado económico se puede publicar, en ninguna alternativa. Los naranjas son prioridad dos: agua y energía, terreno, logística, personal, impuestos y financiamiento; completan los costos y el flujo de fondos. Exportación queda para una etapa futura. Dentro de cada prioridad están empatados: el modelo no inventa un orden que los datos no dan. A la derecha se ve cómo la app muestra esta lista, con casilleros que solo se marcan cuando hay evidencia. Hoy, de 180 datos, cero validados.

## 20. Roadmap recomendado

**Mensaje:** Validar demanda → cotizar → terreno y servicios → escenario financiero real → decisión.

**Notas del presentador:** Este es el camino que recomendamos para el estudio; no es un plan de inversión. Fase uno: validar la demanda. Hablar con compras de la red de supermercados y con otros canales para conseguir volúmenes por producto, precios, plazos de pago y, si se puede, cartas de intención. Fase dos: cotizar. Tarifa de faena a façon, una línea de faena, alimento, pollitos y productores que puedan integrarse. Estas dos fases son las más urgentes y pueden ir en paralelo. Fase tres: terreno y servicios, con municipios, distribuidoras de energía y de agua. Fase cuatro: cargar todo en el motor y correr escenarios con datos reales, sensibilidades y stress. Fase cinco: recién ahí, decidir. Y la decisión puede ser invertir, empezar liviano, esperar o no invertir. No ponemos fechas porque dependen de cuándo respondan los terceros.

## 21. Decisiones abiertas

**Mensaje:** Escala, arquitectura, terreno, faena, alimento, pollito, flota y financiamiento siguen abiertas (104 en el registro).

**Notas del presentador:** Estas son las grandes decisiones que siguen abiertas. El tamaño de la planta. La arquitectura, de C0 a CF. Dónde y qué terreno. Si la faena es propia o a façon. Si el alimento se compra, se encarga a façon o se fabrica. Si el pollito se compra o se incuba. Si los camiones son propios o tercerizados. Y cómo se financia. En total hay 104 decisiones registradas en el proyecto y ninguna está cerrada. Algunas no son técnicas sino del inversor: qué objetivo prioriza, cuánto capital está realmente dispuesto a poner y bajo qué condiciones. Esas respuestas son también datos que el motor necesita.

## 22. Qué puede decidirse hoy

**Mensaje:** Hoy no se decide la inversión; sí qué datos buscar, qué simular y qué alternativas mantener en estudio.

**Notas del presentador:** Para ser claros sobre qué se puede hacer con esto hoy. No se puede decidir si conviene invertir, ni cuánto, ni qué tamaño, ni qué alternativa, ni dónde, ni con qué proveedor. Cualquier respuesta a eso hoy sería una opinión, no un resultado del estudio. Lo que sí se puede decidir desde hoy: qué datos salir a buscar primero, a quién pedírselos y en qué formato; qué escenarios simular en la app para entender qué variables pesan más; mantener las cinco alternativas abiertas, sin descartar ninguna sin datos; y, del lado del inversor, definir su objetivo, cuánto capital pondría de verdad y con qué condiciones.

## 23. Conclusión

**Mensaje:** Motor V1 completo, App V1 lista, decisión real pendiente; próximo paso: trabajo de campo y cotizaciones.

**Notas del presentador:** Para cerrar, las mismas tres frases del principio. El motor está completo estructuralmente. La app está lista. Y el proyecto no está listo para una decisión real, porque faltan los datos. El próximo paso no es más modelado: es salir a la cancha. Hablar con clientes, pedir cotizaciones, conocer terrenos y proveedores. Con esos datos, el motor va a poder decir si el proyecto conviene, en qué forma y con cuánto capital. Hoy el estudio no dice si conviene; dice qué hay que conseguir para saberlo. Gracias.

## 24. Anexo técnico (portada)

**Mensaje:** Material de respaldo para una audiencia técnica.

**Notas del presentador:** Las láminas que siguen son de respaldo. No hace falta presentarlas a la familia ni a los socios; sirven para profesores o para quien quiera ver cómo está construido el motor y cómo se controló.

## 25. A1 · Arquitectura de motores

**Mensaje:** Datos físicos → CAPEX y OPEX → financiero → riesgo/optimizador → app; evidencia y escenario separados.

**Notas del presentador:** Así está armado el sistema. A la izquierda, todos los modelos físicos, que calculan cantidades: aves, kilos, metros cuadrados, kilovatios, personas. Esas cantidades alimentan dos motores económicos: el de inversión, que arma la lista de activos, y el de costos operativos y capital de trabajo. Los dos alimentan al modelo financiero mensual. Encima, la capa de riesgo y el optimizador usan el modelo financiero como función de evaluación, sin copiar fórmulas. La app no calcula nada propio: llama al motor y muestra sus resultados con sus etiquetas. Hay dos universos que no se mezclan: evidencia, con datos verificados, y escenario, con hipótesis. Y las cinco arquitecturas se definen en un solo lugar.

## 26. A2 · Evidencia

**Mensaje:** Solo E1–E3 cuentan como evidencia; hoy hay 0 % de cobertura de evidencia.

**Notas del presentador:** El motor clasifica cada precio o dato por nivel de evidencia. E1 es una cotización formal para este proyecto; E2, un precio directo de proveedor; E3, una referencia documentada que se leyó en el original. Solo esos tres cuentan para publicar resultados, y ese umbral es configurable. E4 es lo visto en prensa o en un buscador sin leer el original; E5, un supuesto de ingeniería. Esos no se usan. Y si no hay dato, queda pendiente: nunca se reemplaza por cero. A la derecha, las reglas que el motor hace cumplir. Hoy la cobertura de evidencia es cero.

## 27. A3 · Tests

**Mensaje:** 70/70 pruebas de integración, 15/15 mutaciones detectadas; las pruebas validan coherencia, no datos.

**Notas del presentador:** Cómo sabemos que el motor hace bien las cuentas. Hay 70 pruebas de integración entre módulos y todas pasan. Además se introdujeron 15 errores a propósito —por ejemplo, contar dos veces la electricidad del frío o usar un precio de prensa como si fuera verificado— y las pruebas detectaron los 15. Cada motor económico tiene su propia batería: entre 69 y 82 pruebas. La app tiene 52 pruebas de backend y 19 flujos probados en navegador. Pero ojo: las pruebas garantizan coherencia interna, no que los datos sean correctos. Eso solo lo resuelve el trabajo de campo.

## 28. A4 · Tensiones abiertas

**Mensaje:** 76 tensiones (71 abiertas); las principales son precios, rendimientos, pico de fondos, upstream, IIBB y comparabilidad.

**Notas del presentador:** Una tensión es una inconsistencia o un problema conocido que no se pudo resolver con la información disponible. La auditoría final registró 76: 71 siguen abiertas, 4 se corrigieron y 1 quedó mitigada en el motor. Las principales: no hay precios; los rendimientos del pollo no se midieron en una planta; no se puede comparar el capital necesario con los 2 millones; los módulos de granjas, incubadora y planta de alimento no tienen personal ni consumos dimensionados; falta una definición fiscal sobre ingresos brutos en exportaciones; y hoy es imposible comparar alternativas porque ninguna se puede costear. Se dejan explícitas para no esconderlas.

## 29. A5 · Glosario

**Mensaje:** Términos técnicos explicados en una línea.

**Notas del presentador:** Glosario de los términos que aparecen en la presentación, en una línea cada uno. El glosario completo del proyecto, con más de un centenar de términos, está en la carpeta de gestión del proyecto y también en el diccionario de la app.

## Preguntas probables y respuesta honesta

| Pregunta | Respuesta |
|---|---|
| ¿Cuánto cuesta la planta? | Todavía no se sabe: 167 de 175 conceptos de inversión no tienen precio. Hace falta cotizar (fase 2). |
| ¿Alcanzan los USD 2 M? | No se puede saber todavía, ni para sí ni para no. Además, la plata necesaria incluye el arranque y el capital de trabajo, no solo la planta. |
| ¿Cuánto se gana? | No hay ninguna rentabilidad calculada con datos reales. Se puede simular en la app con supuestos, pero sería una simulación, no un resultado. |
| ¿Los supermercados no alcanzan como demanda? | Hoy son un canal potencial: no hay volúmenes, precios ni condiciones confirmadas. Si se confirman, pueden ser cliente ancla. |
| ¿Qué alternativa conviene? | Ninguna está elegida. Depende de los datos y del objetivo del inversor. El optimizador puede incluso responder «no invertir aún». |
| ¿Dónde va la planta? | No hay ranking: 0 de 624 datos de la matriz verificados. Se decide terreno por terreno, con el municipio. |
| ¿Qué hacemos ahora? | Validar clientes y pedir cotizaciones (prioridad 1), siguiendo el checklist de la app. |
