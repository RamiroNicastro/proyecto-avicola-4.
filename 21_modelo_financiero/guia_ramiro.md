# Guía para Ramiro — cómo leer (y no leer) el modelo financiero

**Fecha:** 2026-10-04 · Lenguaje simple, ejemplos **conceptuales**. Ninguna cifra de esta guía es del proyecto: los números de ejemplo son inventados para explicar ideas y están marcados así.

## 0. Lo primero: qué dice hoy el modelo

**Todavía no puede decir si el proyecto gana o pierde plata.** No es un problema del modelo: faltan precios de venta, volúmenes de clientes, costos cotizados, cronograma de obra, impuestos y tasa de descuento. El modelo lo dice explícitamente con `NO_PUBLICABLE_POR_EVIDENCIA_INSUFICIENTE` y lista qué falta ([`evidencia_financiera.md`](evidencia_financiera.md)). Lo que sí está listo es la **máquina**: probada con 70 controles y 25 errores sembrados a propósito, todos detectados.

Tiene **dos modos**:
- **Evidencia:** solo usa datos respaldados (cotizaciones, contratos, documentos leídos). Hoy no publica nada.
- **Escenario:** vos cargás "¿qué pasaría si…?" (precio, demanda, inversión, crédito) y el modelo calcula, pero todo sale con el sello **SIMULACIÓN HIPOTÉTICA NO VALIDADA**. Sirve para pensar, no para mostrar como rentabilidad.

## 1. Facturación ≠ ganancia

Facturar es lo que cobrás por vender. Ganar es lo que queda después de pagar todo. *Ejemplo inventado:* vender 100 y gastar 95 en alimento, pollitos, sueldos y fletes deja 5. Una planta que factura mucho puede perder plata.

## 2. EBITDA ≠ caja

El EBITDA es lo que deja la operación antes de inversiones, intereses e impuestos. Pero la caja (la plata en el banco) también se va en: comprar máquinas (CAPEX), financiar a los clientes que pagan a 30 días, tener stock, pagar el crédito y los impuestos. Un EBITDA positivo puede convivir con una cuenta bancaria vacía.

## 3. Utilidad ≠ caja

La utilidad contable descuenta la **depreciación** (el desgaste de las máquinas repartido en años), que no es una salida de plata ese año; y no descuenta lo que se compró en máquinas ese año, que sí sale de caja. Por eso el modelo calcula los dos y nunca los confunde.

## 4. CAPEX ≠ gasto operativo

CAPEX es lo que se invierte una vez (terreno, nave, línea de faena, cámaras de frío). OPEX es lo que se gasta para operar cada mes (alimento, pollito, energía, sueldos). Un galpón es CAPEX; la luz del galpón es OPEX. Reponer una máquina que se gastó es **CAPEX de reposición**, no mantenimiento.

## 5. Capital de trabajo

Es la plata "atrapada" para que la operación funcione: stock de alimento, aves en crianza, producto en cámara y lo que te deben los clientes, menos lo que vos le debés a tus proveedores. No es un gasto, pero hay que tenerla. Si vendés más, necesitás más.

## 6. Por qué crecer puede consumir caja

Cada vez que la planta vende más, antes de cobrar tenés que comprar más alimento, criar más aves y esperar el cobro. Esa plata sale antes de entrar. Una empresa que crece rápido y rentable puede quedarse sin efectivo. Por eso el modelo calcula el **pico de fondos requerido** (el punto más bajo de la caja acumulada), no solo la inversión inicial.

## 7. Por qué vender a 30 días puede generar falta de efectivo

*Ejemplo inventado:* si vendés 1.000 por día y el supermercado paga a 30 días, durante el primer mes despachaste 30.000 y no cobraste nada, pero ya pagaste el pollo, el alimento y los sueldos. Esos 30.000 son capital de trabajo que alguien tiene que poner. En los casos de prueba del modelo (artificiales, antes de impuestos), cobrar a 30 días baja el VAN de 51,6 (`CP-PRETAX-ANUAL`) a 44,2 (`CP-COBRO-30D`). **El modelo no supone que el supermercado pague contado.**

## 8. VAN (valor actual neto)

Es sumar toda la plata que entra y sale en el tiempo, pero valuando menos la plata futura que la de hoy (porque podrías invertirla en otra cosa). Si el VAN es positivo a la tasa que le pedís al proyecto, el proyecto rinde más que esa alternativa. Depende mucho de la **tasa** elegida: el modelo no la inventa, la cargás vos (y entonces es escenario).

## 9. TIR (tasa interna de retorno)

Es la tasa a la que el VAN da cero: "el rendimiento anual equivalente" del proyecto. Atención: a veces **no existe** (si el flujo nunca se vuelve positivo) o **hay dos** (si el flujo cambia de signo varias veces, por ejemplo por una expansión grande en el medio). El modelo no inventa una TIR en esos casos: lo avisa.

## 10. Payback (recupero)

Cuántos años tardás en recuperar lo que pusiste. El simple suma flujos sin descontar; el descontado usa la tasa. Si no se recupera dentro del horizonte, el modelo dice **NO RECUPERADO** y no "estira" la cuenta.

## 11. Break-even (punto de equilibrio)

Cuánto tenés que vender (o a qué utilización de la planta, o a qué precio medio) para no perder plata. Se calcula con el **margen de contribución**: lo que deja cada ave vendida después de sus costos variables, que tiene que pagar los costos fijos. *Ejemplo inventado:* si cada ave deja 0,50 y los fijos anuales son 1.000.000, necesitás 2.000.000 de aves por año. Si la planta solo puede 1.500.000, ese tamaño no llega nunca al equilibrio. Si cada ave deja margen negativo, vender más empeora todo.

## 12. Deuda

Un préstamo trae plata hoy y te obliga a devolverla con intereses en fechas fijas, haya o no ventas. El modelo arma el cronograma (francés, alemán, bullet o a medida) y nunca supone que el crédito está disponible.

## 13. DSCR

Es "cuántas veces la caja que genera la operación cubre la cuota del préstamo". Un DSCR de 1,0 significa que todo lo que genera la operación se va en la cuota; menos de 1 significa que no alcanza. Los bancos suelen exigir un mínimo (el modelo no fija cuál).

## 14. Proyecto vs accionista

- **Flujo del proyecto:** ¿el negocio, en sí mismo, vale la inversión? No importa cómo se pague (con plata propia o prestada).
- **Flujo del accionista:** ¿cuánto pone y cuánto recibe el inversor, después de pagar el crédito?
Un crédito puede mejorar el rendimiento del accionista y a la vez aumentar el riesgo. El modelo los calcula por separado y nunca los mezcla.

## 15. Por qué una TIR alta no siempre es mejor

- Un proyecto chico con TIR 40 % puede generar menos plata total que uno grande con TIR 20 %.
- La TIR supone que la plata que va saliendo se reinvierte a esa misma tasa (por eso existe la MIRR).
- Una TIR puede ser "alta" solo porque se puso poco capital y mucha deuda: más riesgo, no mejor negocio.
- Con flujos que cambian de signo, la TIR puede no significar nada.
Por eso conviene mirar juntos VAN, TIR, pico de fondos, payback, break-even y DSCR.

## 16. Por qué una planta grande puede dar mejor margen pero más riesgo

Una planta grande reparte los costos fijos (estructura, frío, mantenimiento, habilitaciones) entre más aves: si la llenás, el costo por ave baja. Pero si no la llenás, esos fijos siguen ahí, el break-even queda lejos y la inversión inicial es mayor. Con demanda documentada ≈ 0, el riesgo de no llenarla es el principal riesgo del proyecto. Crecer por fases baja ese riesgo pero puede costar más en total (ampliar una planta en operación, reemplazar equipos chicos). El modelo permite comparar ambas cosas cuando haya datos; **no supone que una sea mejor**.

## 17. Cómo usar el modo escenario

1. Copiá [`plantilla_escenario_usuario.json`](plantilla_escenario_usuario.json) y completá lo que quieras probar (todo lo que quede en `null` sigue pendiente).
2. Corré: `python3 21_modelo_financiero/modelo_financiero.py --escenario mi_escenario.json --salida mi_carpeta/`.
3. Mirá primero `PUBLICABLE_*_MOTIVO`: te dice qué te falta cargar.
4. Todo lo que salga lleva el sello **SIMULACION_HIPOTETICA_NO_VALIDADA**. No reemplaza a la evidencia ni la modifica.
