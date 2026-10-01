# Guía para Ramiro — localización

**Fecha:** 2026-10-01 · **Sesión:** 12A · Para leer antes de hablar de "dónde poner la planta" con inversores, municipios o vendedores de terrenos.

---

## 1. No existe "la mejor provincia" en abstracto

"¿Cuál es la mejor provincia para un frigorífico avícola?" no tiene respuesta, porque **"mejor" depende de para qué**:

- Si el negocio vive de abastecer supermercados del AMBA con fresco, lo mejor es estar cerca del AMBA.
- Si vive de producir pollo vivo barato y sano, lo mejor es estar cerca de las granjas, del maíz y lejos de otras granjas.
- Si vive de exportar, importa la habilitación, el listado por destino y la escala para llenar contenedores; el puerto es lo último.

Además, cada provincia tiene **varias zonas muy distintas**: el periurbano de Pilar y el centro de la provincia de Buenos Aires comparten gobernador pero no comparten nada más. Por eso el estudio trabaja con **corredores** (13 en total), no con provincias enteras.

## 2. Qué es una matriz multicriterio

Es una tabla que:

1. **Divide** la pregunta grande en preguntas medibles (distancia a CABA, granjas en 100 km, calidad del agua, límites de vuelco, potencia eléctrica…): son los **criterios** (43 subcriterios en 12 grupos).
2. **Convierte** cada medida a una escala común de 0 a 1 (1 = mejor). Si "menos es mejor" (distancia, precio de la tierra, densidad de granjas), la escala se invierte.
3. **Pondera**: le da a cada grupo un peso según lo que importa para quien decide (los pesos suman 100).
4. **Suma**: puntaje = Σ peso × valor normalizado.

Su utilidad no es dar "la respuesta", sino **obligar a decir en voz alta** qué se midió, con qué evidencia y cuánto importa cada cosa. Si alguien no está de acuerdo con el resultado, se puede ver exactamente si discrepa en un dato o en un peso.

## 3. Por qué el resultado cambia con los pesos

Ejemplo con datos **ficticios** (`python3 10_localizacion/modelo_localizacion.py --demo`): tres zonas inventadas — Z-CERCA (cerca del mercado, pocas granjas, tierra cara), Z-CLUSTER (zona avícola fuerte, densa) y Z-GRANOS (lejos, mucho maíz, pocas granjas, tierra barata).

| Perfil de pesos | Primero | Segundo | Tercero |
|---|---|---|---|
| A — Mercado (demanda 30, logística 12) | Z-CERCA (0,550) | Z-CLUSTER (0,527) | Z-GRANOS (0,344) |
| B — Producción (producción primaria 25, alimento 15) | Z-CLUSTER (0,491) | Z-GRANOS (0,482) | Z-CERCA (0,415) |
| C — Equilibrado | Z-CLUSTER (0,512) | Z-CERCA (0,460) | Z-GRANOS (0,418) |

**Con los mismos datos**, la zona "ganadora" cambia según el perfil. Y en el perfil B, Z-CLUSTER y Z-GRANOS están a 0,009 de distancia: si el peso del alimento sube un 50 %, gana Z-GRANOS. Lección: **cuando el resultado depende de los pesos, la decisión es de valores (estrategia), no técnica**. Por eso el estudio **no declara cuál perfil es el correcto**: eso lo deciden los socios con la estrategia clara (DEC-12A-02).

## 4. Con los datos reales, hoy no hay ranking — y está bien

De 559 celdas de la matriz real, **0 están verificadas**, 35 tienen un dato visto solo en extractos o estimado sin medir (`[PVDP]`) y 524 están vacías. El modelo:

- en modo **estricto** (solo datos verificados) da puntaje 0 a todas y **no emite ranking**;
- en modo **exploratorio** (aceptando extractos) muestra intervalos del tipo "entre 0,07 y 0,99": significa "no sabemos". Tampoco emite ranking.

El modelo nunca rellena celdas vacías para poder calcular. **Un ranking hecho con datos inventados sería peor que no tener ranking**, porque parecería una conclusión.

## 5. Zona no es terreno

- La **zona** (corredor) se elige por condiciones de contexto: granjas, granos, mercado, rutas, acuíferos, normativa provincial, mano de obra.
- El **terreno** se elige por condiciones del lote: uso de suelo, cota, vecinos, acceso, servicios en el lindero, superficie, precio.

Una buena zona puede no tener ningún terreno apto (todo inundable, o sin vuelco posible), y un terreno excelente puede estar en una zona sin productores. **Primero zona, después municipio, después terreno.** Si alguien ofrece "un terreno buenísimo", la primera pregunta es en qué zona está y si esa zona sirve para el modelo de abastecimiento.

## 6. Un terreno barato puede ser caro de operar

El precio de la tierra se paga una vez. Lo que se paga **todos los días** es: kilómetros de aves vivas, de alimento y de producto; agua que hay que potabilizar; efluentes que hay que tratar más porque no hay dónde volcar; cortes de luz; personal que no hay; técnicos que vienen de lejos. Extender una línea de media tensión, hacer un acceso pavimentado o rellenar un terreno bajo puede costar más que la diferencia de precio con un terreno caro con servicios. Detalle en [`terreno_ideal.md`](terreno_ideal.md) §5.

## 7. Estar cerca del cliente puede ser malo para producir

Una planta en el periurbano del AMBA queda cerca de los supermercados, pero:

- las granjas tienen que estar lejos (no hay lugar ni conviene criar pollos entre barrios), así que las **aves vivas viajan muchas horas**: más mortalidad en el camión, más pérdida de peso, peor bienestar;
- los camiones de aves vivas cruzan zonas pobladas y otras granjas: **peor bioseguridad**;
- el suelo es caro, los vecinos están cerca (olores, ruido, tránsito de madrugada) y **crecer es difícil**.

Por eso la lógica habitual del sector es "planta cerca de las granjas; el producto refrigerado viaja al mercado". Una alternativa a estudiar es separar: faena en zona productiva y un centro de trozado o distribución en el AMBA (DEC-12A-04).

## 8. Una zona avícola fuerte tiene ventajas y riesgos

Entre Ríos concentra la mitad de la faena del país (dato de extractos, `[PVDP]`). Eso significa:

| Ventajas | Riesgos |
|---|---|
| Productores, incubadoras, fábricas de alimento, contratistas y veterinarios cerca | Si hay un brote, se propaga más fácil y la zona de control abarca más granjas |
| Personal con experiencia | Competencia con empresas grandes por productores y personal |
| Organismos y proveedores acostumbrados a la actividad | Menos tierra disponible para granjas nuevas a distancia sanitaria |
| Plantas que podrían faenar a façon | Que exista capacidad no significa que la vendan (hay que preguntar) |

Una zona de baja densidad (como partes de Chaco o del interior bonaerense) es al revés: mejor sanidad de partida, pero todo el ecosistema hay que construirlo.

## 9. El contacto en Chaco

Es una ventaja **para conseguir información y reuniones** en Chaco. No es un ahorro, no acorta trámites, no hace más fácil una habilitación y no suma puntos en la matriz. Si Chaco entra en la lista corta por sus condiciones físicas, el contacto ayudará a relevarla más rápido. Si no entra, el contacto no la mete.

## 10. Estar cerca del puerto no te hace exportador

Para exportar hace falta, en este orden: que el país destino esté abierto, que la planta esté habilitada y listada para ese destino, que el producto esté autorizado, un comprador con contrato, volumen para llenar contenedores y congelado. El puerto solo resuelve el último paso del camino. Rosario está cerca de los granos pero tiene pocos servicios de contenedores refrigerados; casi todo sale por Buenos Aires y Dock Sud.

## 11. Cómo usar el modelo

```
python3 10_localizacion/modelo_localizacion.py                       # pruebas + resultados reales
python3 10_localizacion/modelo_localizacion.py --demo                # ejemplo ficticio para entender
python3 10_localizacion/modelo_localizacion.py --demo --sensibilidad 0.5
python3 10_localizacion/modelo_localizacion.py --peso DEMANDA=20 --peso PRODUCCION_PRIMARIA=20 ...
```

Para cargar un dato: completar la fila en `matriz_localizacion.csv` con valor, tipo de evidencia, fuente y estado (`DISPONIBLE` solo si se leyó el documento original o es una medición o cotización). Para cambiar prioridades: editar `pesos_localizacion.csv` (cada perfil debe sumar 100).

## 12. Preguntas que conviene llevar a campo

- ¿Dónde están los locales y el centro de distribución de la red? ¿Recibe perecederos? (DPV-018, DPV-036)
- ¿Cuántos productores con galpones libres hay a menos de 2–3 h de cada corredor y en qué condiciones? (DPV-048)
- ¿Quién vende pollito BB a terceros y desde dónde? (DPV-047)
- En cada municipio candidato: ¿admite un frigorífico avícola?, ¿dónde se puede volcar?, ¿qué potencia hay?, ¿hay gas?, ¿qué pasó con otras industrias y sus vecinos? (DPV-106, DPV-087)
- ¿Qué plantas faenarían a façon y a qué distancia? (DPV-006)
