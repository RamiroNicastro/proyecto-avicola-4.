# Guía para Ramiro — cómo usar (y no usar) la capa de riesgos y el optimizador

**Fecha:** 2026-10-05 · Lenguaje simple. Los números de ejemplo son **inventados** y están marcados así; ninguno es del proyecto.

## 0. Lo primero

**Hoy el optimizador no puede recomendar nada para el proyecto**, y lo dice: `OPTIMIZACION_REAL_NO_DISPONIBLE`. Faltan precios, clientes, costos cotizados, cronograma, impuestos y tasa. Lo que sí hace hoy es decir **qué dato conseguir primero** ([`que_hacer_ahora.csv`](que_hacer_ahora.csv)) y mostrar, con un caso inventado ([`casos_prueba/`](casos_prueba/)), cómo va a razonar cuando los datos lleguen.

## 1. Sensibilidad: "¿qué pasa si…?"

Se mueve **una sola** cosa (por ejemplo el precio del pollo −10 %) y se deja todo lo demás igual. *Ejemplo inventado:* si el VAN pasa de 100 a 40, el precio es una variable crítica. El **tornado** ordena las variables por cuánto mueven el resultado. Un −10 % **no** es una predicción: es una prueba.

## 2. Stress: "¿y si vienen varias malas juntas?"

Precio −10 %, alimento +20 % y demanda −30 % al mismo tiempo. Los porcentajes del archivo [`escenarios_stress.csv`](escenarios_stress.csv) son ejemplos editables, no pronósticos.

## 3. Punto de quiebre: "¿hasta dónde aguanta?"

Busca el valor exacto en el que el negocio deja de ganar (VAN = 0). *Ejemplo inventado:* "con precio 14 % más bajo, el VAN llega a cero". Si en el rango buscado no cruza, dice `NO_ENCONTRADO_EN_RANGO`; si no hay datos para calcularlo, `NO_CALCULABLE`. Son cosas distintas.

## 4. Monte Carlo: "¿qué tan probable es perder?"

Corre el modelo cientos de veces sorteando precios y costos. **Solo vale si las "loterías" (distribuciones) salen de datos reales** (series de precios, varias cotizaciones). Hoy no hay, así que el proyecto dice `NO_DISPONIBLE_POR_FALTA_DE_DISTRIBUCIONES`. Aunque se corra, el resultado es una probabilidad **simulada**, no una estadística histórica.

## 5. El optimizador: no hay "mejor" sin criterio

Hay que elegir qué se busca: más VAN, menos capital, recuperar antes, menos riesgo… *En el caso inventado* la planta grande gana en VAN y el modelo asset-light (façon) gana en capital y en payback. Por eso el modelo hace **un ranking por objetivo** y no elige uno por vos. El objetivo **balanceado** necesita que vos pongas los pesos.

## 6. No construir todavía es una opción

`NO_INVERTIR_AUN` siempre está en la lista: es seguir como hoy, pilotear con façon y validar demanda. Si ninguna planta tiene VAN positivo, gana esa opción. Si ninguna configuración cumple tus condiciones, el modelo dice `NINGUNA_CONFIGURACION_FACTIBLE` y **no** elige "la menos mala".

## 7. Restricciones: duras y blandas

- **Dura:** "tengo como máximo X de capital" → lo que necesita más, queda afuera.
- **Blanda:** "prefiero recuperar en menos de 5 años" → lo que tarda más pierde puntos pero sigue en la lista.

Nada viene cargado: el modelo **no** supone que hay USD 2 M. El capital se compara contra el **pico de fondos** (lo máximo que hay que poner, incluyendo el arranque y la plata que queda en la calle por cobrar), no solo contra el CAPEX.

## 8. Ganar en el escenario ≠ estar seguro

Cada alternativa tiene dos notas separadas: **rentabilidad** (VAN, TIR) y **confianza** (`COBERTURA_EVIDENCIA`: cuánto del cálculo se apoya en datos verificados). Un VAN alto con confianza baja es una hipótesis, no un resultado. El **semáforo**: verde = cumple todo y con evidencia; amarillo = atractivo pero con datos pendientes; rojo = no cumple una condición; gris = no se puede evaluar.

## 9. ¿Qué tan firme es la elección?

El modelo siempre muestra la **segunda mejor** y la diferencia. Si el ganador cambia cuando se mueve la demanda o el precio, marca `DECISION_NO_ROBUSTA`: en ese caso conviene conseguir el dato que la define antes de decidir.

## 10. Cómo cargar un escenario

1. Copiar [`escenario_optimizador.json`](escenario_optimizador.json).
2. En `comun`: precios por producto y canal, demanda, plazos, impuestos, horizonte, tasa (igual que la plantilla del modelo financiero).
3. En `por_alternativa`: CAPEX, cronograma y OPEX de cada configuración que quieras comparar (por ejemplo `C0|BASE|5000|ESCALA_UNICA` y `C1|BASE|5000|ESCALA_UNICA`).
4. En `disponibilidad`: terreno, potencia, agua, integrados, pollito y façon que tengas confirmados.
5. Restricciones y objetivo en [`inputs_riesgo_optimizacion.csv`](inputs_riesgo_optimizacion.csv).
6. `python3 22_riesgos/modelo_optimizador.py --escenario mi.json --salida mi_carpeta/`

Todo lo que salga dirá **SIMULACIÓN HIPOTÉTICA NO VALIDADA**.
