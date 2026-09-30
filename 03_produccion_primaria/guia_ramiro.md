# Guía de producción primaria para el responsable del proyecto

**Fecha:** 2026-09-29 · Para: Ramiro (responsable del proyecto) · Nivel: dirigir y evaluar el negocio, no hacer veterinaria.

> Idea central: **la granja es una fábrica biológica de kg vivo.** Su "materia prima" es el pollito y el alimento; su "máquina" es el galpón; su "rendimiento" es el FCR; su "scrap" es la mortalidad; su "capacidad" depende de densidad y ciclos; y su "falla catastrófica" es sanitaria o eléctrica. Todo se puede pensar con herramientas de Ingeniería Industrial (balances, capacidad, cuellos de botella, variabilidad, confiabilidad).

---

## 1. Los 10 conceptos que tenés que poder defender

1. **Pollitos alojados ≠ aves faenadas.** Entre ambos están la mortalidad en granja (3–8 % o más) y la del transporte (0,2–0,5 %). Para faenar 10.000 aves hay que alojar ~10.330–10.920 pollitos (10.558 en el escenario medio); para una semana plena de 5 días de faena, ~52.800 pollitos, no 50.000. Siempre aclarar si un número son pollitos alojados, aves cargadas o aves faenadas.
2. **El alimento es el costo principal y el FCR lo gobierna.** Alimento = kg vivo × FCR. Empeorar 0,1 punto el FCR = **+5,9 % de alimento** (+290 t por millón de aves de 2,9 kg).
3. **El FCR depende del peso:** un ave más pesada siempre convierte peor. Nunca compares FCR de lotes con pesos distintos sin corregir.
4. **Capacidad de galpón ≠ producción anual.** Producción = capacidad × ciclos/año × supervivencia. Un galpón de 1.800 m² aloja ~23.000 pollitos pero entrega hasta ~124.000 aves cargadas/año (~119.000 si en las semanas con feriados se aloja menos).
5. **Ciclos/año ≠ 365/edad.** Hay que sumar captura, limpieza, desinfección, vacío sanitario y preparación (10–21 días): con 47 días de crianza salen **~5,7 ciclos**, no 7,8.
6. **La densidad se mide en kg/m² al final, no en pollitos/m² al inicio.** Es la variable de superficie más potente (30 vs 39 kg/m² = −23 % de m²), pero la limitan el bienestar, el clima y la tecnología del galpón.
7. **El peso de faena es una decisión comercial**, no técnica: sale del mix de productos (entero, trozado, deshuese) y del principio de ingreso total por ave. Cambia alimento, m² y FCR.
8. **Bioseguridad = acceso a mercados.** Un brote de influenza aviar no solo mata aves: cierra exportaciones y hunde el precio interno. Regionalización y compartimentación son activos comerciales.
9. **Un galpón cerrado depende 100 % de la electricidad.** En galpones intensivos/climatizados, una falla de ventilación durante períodos de calor puede provocar rápidamente estrés térmico y mortalidad significativa; por eso generación de respaldo, alarmas y procedimientos de emergencia no son opcionales.
10. **Granjas propias, integrados o compra no es una decisión técnica sino de capital, control y riesgo.** Integrar a productores es el modelo dominante porque traslada el CAPEX de galpones, pero exige capital de trabajo (alimento y pollitos del ciclo completo) y know-how. La compra spot es flexible pero inestable y débil en bioseguridad.

## 2. Los 10 indicadores que tenés que entender

| # | Indicador | En una frase | Valor de referencia (perfil medio, a validar) |
|---|---|---|---|
| 1 | **Mortalidad (%)** | Cuántos pollitos no llegan a la carga | 3 / 5 / 8 % (un estudio de Entre Ríos: 7,7–9,5 %, a validar) |
| 2 | **Mortalidad de 7 días** | Calidad del pollito y de la recepción | ≤ 1 % |
| 3 | **FCR** | kg de alimento por kg vivo | 1,60 / 1,70 / 1,85 |
| 4 | **Peso vivo final** | Lo que se vende (y define el ingreso) | 2,7–3,0 kg |
| 5 | **Edad de faena** | Cuánto ocupa el galpón | 45–50 d |
| 6 | **Ganancia diaria** | Velocidad de crecimiento | ~58–62 g/d |
| 7 | **Uniformidad** | Qué tan parejo es el lote (importa para la planta) | CV ≤ 8–10 % |
| 8 | **kg/m² y kg/m²/año** | Uso del activo galpón | 30–39 kg/m²; ~155–235 kg/m²/año |
| 9 | **IEP** | Resumen de desempeño para comparar lotes e integrados | ~300–375 |
| 10 | **Costo por kg vivo** | Competitividad y decisión hacer/comprar | Sin valor aún (sin precios) |

Complementarios: consumo de agua (alerta temprana), decomisos en planta, DOA y merma de transporte, pododermatitis (bienestar y grado de garras). Detalle: [`kpis_productivos.md`](kpis_productivos.md).

## 3. Preguntas para hacerle a un productor avícola (o integrado)

> Versión de campo con registro y planilla de 6–12 crianzas: [`cuestionario_productores.md`](cuestionario_productores.md). Incubadoras: [`../15_incubacion/cuestionario_incubadoras.md`](../15_incubacion/cuestionario_incubadoras.md).

**Sus números (pedir registros de los últimos 6–12 lotes, no promedios de memoria):**
1. ¿Cuántos m² de galpón tiene, de qué tipo (abierto, blackout, túnel) y de qué año?
2. ¿Cuántos pollitos aloja por galpón y cuántas aves salen? ¿Cuántos kg/m² al final, en invierno y en verano?
3. ¿Edad y peso de faena, FCR y mortalidad por lote? ¿Con qué definición de FCR (kg en granja o en planta)?
4. ¿Cuántos días pasan entre la salida de un lote y la entrada del siguiente? ¿Cuántos lotes hizo el último año?
5. ¿Cuál fue su peor lote y por qué (calor, enfermedad, pollito, corte de luz)?

**Su instalación y sus riesgos:**
6. ¿Tiene generador con arranque automático? ¿Alarma remota? ¿Cuántos cortes o caídas de tensión tuvo en el último verano?
7. ¿De dónde sale el agua? ¿Tiene análisis? ¿Cuántos días de reserva tiene?
8. ¿Cómo maneja la cama y la mortalidad? ¿Cada cuánto retira la cama completa?
9. ¿Qué medidas de bioseguridad aplica (cerco, ducha, ropa, arco de desinfección, malla antipájaros)? ¿Tuvo inspecciones de SENASA? ¿Está habilitado y con RENSPA?
10. ¿A qué distancia está la granja avícola más cercana y a cuántos km de la planta de faena?

**Su relación comercial:**
11. ¿Con quién trabaja hoy? ¿Tiene contrato escrito? ¿Por cuánto tiempo y con qué preaviso de salida?
12. ¿Cómo le pagan (por ave, por kg, con premios/castigos por FCR y mortalidad)? ¿A cuántos días?
13. ¿Qué aporta el integrador (pollito, alimento, gas, veterinario, captura) y qué aporta usted?
14. ¿Qué le haría cambiar de integrador? ¿Qué problema tuvo con su integrador actual o anterior?
15. ¿Estaría dispuesto a invertir en mejorar el galpón si el contrato lo justificara?

**Preguntas clave a una incubadora:** volumen semanal disponible y estacionalidad; genética; edad de las reproductoras; mortalidad de 7 días garantizada y reposición; vacunación en incubadora; transporte; precio y su fórmula de ajuste; plazo de pago; prioridad ante escasez.

**Preguntas clave a un integrador o frigorífico establecido (si hay acceso):** radio de sus granjas; costo por kg vivo y su estructura (sin pedir secretos, órdenes de magnitud); problemas de abastecimiento de pollito; experiencia con compra spot; cómo manejaron los brotes de IAAP.

## 4. Errores de razonamiento que conviene evitar

- Dimensionar galpones con 365/edad o con la capacidad de alojamiento como si fuera producción.
- Tomar la tabla del manual genético como resultado de campo.
- Usar un único FCR, un único peso o una única mortalidad.
- Confundir kg vivo en granja, kg vivo en planta y kg de canal.
- Suponer que integrados "sobran" por la crisis de otro integrador.
- Elegir una zona por cercanía personal sin mirar clima, energía, agua, granos, densidad avícola y distancia a la planta y al mercado.
