# Valor de la información y QUE_HACER_AHORA

**Fecha:** 2026-10-05 · Código: `prioridad_evidencia()`, `prioridad_escenario()`, `asignar_rank_compartido()`, `que_hacer_ahora()` en [`modelo_optimizador.py`](modelo_optimizador.py) · Salidas: [`prioridad_validacion.csv`](prioridad_validacion.csv), [`que_hacer_ahora.csv`](que_hacer_ahora.csv)

## 1. Universo evidencia (hoy)

Cada faltante de `disponibilidad()` del motor (desagregado por módulo de OPEX y por gate físico pendiente) se agrega en todas las alternativas. Clave de prioridad derivada del modelo: (indicadores publicables que bloquea según `DEPENDENCIAS_FLAG` de 21 ↓, alternativas que bloquea ↓). No es una lista fija.

## 2. Universo escenario

Variables ordenadas por (¿pueden invertir el orden mejor/segunda o llevar el VAN de la mejor bajo 0? → amplitud del VAN de la mejor). Se informa la cercanía entre alternativas (diferencia ÷ amplitud). Sin distribuciones no es VOI bayesiano.

## 3. Empates: RANK_COMPARTIDO

- `RANK_COMPARTIDO` = 1 + número de ítems estrictamente mejores. Los ítems con la misma clave comparten rango y llevan `EMPATE` (cuántos y por qué criterio) y `ORDEN_DENTRO_DEL_EMPATE = NO_SIGNIFICATIVO`.
- **No se desempata** por orden de archivo, ID, posición en el código ni nombre. Hoy 9 faltantes empatan en el primer lugar (bloquean los 10 indicadores en las 54 alternativas): cronograma (3 duraciones), horizonte, curva de ramp-up, rendimientos, demanda A/B, precios y condiciones de canal.
- El desempate corresponde a una etapa futura: sensibilidad (con un escenario cargado), magnitud económica, capacidad de cambiar la decisión y costo/facilidad de obtener el dato. No se inventa ahora.
- Tests COMP-05, AUD-13; mutación R25.

## 4. QUE_HACER_AHORA

Acción por ítem (tabla de correspondencia ítem → acción), con DPV/DEC vinculados verificados contra `datos_por_validar.md` y `decisiones_pendientes.md`; ítems sin registro → `NUEVA`. Se listan acciones hasta `que_hacer.n` (10), pero **un grupo de empate nunca se corta**: si el límite cae dentro de un empate, entra el grupo completo. Cada fila lleva su `RANK_COMPARTIDO`; no hay numeración secuencial que sugiera un orden inexistente.

## 5. Columna futura `POTENCIAL_DE_CAMBIAR_DECISION` (auditoría final 21)

`prioridad_validacion.csv` y `que_hacer_ahora.csv` llevan la columna `POTENCIAL_DE_CAMBIAR_DECISION`, preparada para el desempate futuro del §3. En el universo **EVIDENCIA** vale `NO_CALCULADO` (constante `POTENCIAL_NO_CALC`): sin un escenario no hay sensibilidad que medir y no se completa con un orden inventado. En **ESCENARIO** y en el caso artificial repite el resultado one-way de `prioridad_escenario()` (`SÍ` / `NO`, "dentro del escenario; no es VOI"). Los empates siguen siendo empates (test de integración OP07).
