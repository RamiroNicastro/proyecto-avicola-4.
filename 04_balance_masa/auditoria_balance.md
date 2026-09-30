# Auditoría conceptual del balance de masa

**Fecha:** 2026-09-30 · **Versión del modelo:** 1.1 · Complementa [`balance_por_ave.md`](balance_por_ave.md) y [`conclusiones_balance.md`](conclusiones_balance.md)

> **Objetivo:** demostrar que el modelo, además de cerrar matemáticamente, cierra **conceptualmente**: ninguna masa aparece dos veces bajo nombres distintos, cada kilogramo termina en **una sola** categoría final y el agua nunca se cuenta como carne.
> **Alcance:** este es un **BALANCE DE MASA DEL AVE Y SUS PRODUCTOS**. **No** es todavía un balance de agua industrial, ni de efluentes, ni energético, ni un modelo económico, ni un diseño de maquinaria; esos módulos usarán después estos resultados. **ESTE BALANCE NO DIMENSIONA EL CONSUMO INDUSTRIAL DE AGUA NI EL CAUDAL TOTAL DE EFLUENTES DE LA PLANTA.**
> Todas las cifras: pollo de **2,9 kg**, escenario medio (rendimiento y condenas medios), chiller por inmersión, rutas por defecto. Salen de [`modelo_balance_masa.py`](modelo_balance_masa.py) (`--peso 2.9 --auditoria`). Son `[ESTIMACIÓN]`, no mediciones.

---

## 1. Resultado de la auditoría

| Punto auditado | Hallazgo en la versión 1.0 | Acción en la versión 1.1 | ¿Cambian cifras? |
|---|---|---|---|
| Doble contabilización de masa | **No se encontró.** El test T10 ya verificaba que cada componente primario se asigna una sola vez | Se agregan 8 tests de exclusividad (T14–T21) | No |
| Nomenclatura del agua | **Ambigua:** "agua incorporada / agua del proceso" (0,213 kg/ave; 2,13 t/día a 10.000 aves) podía leerse como consumo de agua de la planta | Se renombra y desagrega (§2); advertencia explícita en todos los documentos | No (solo nombres) |
| Decomisos vs pérdidas no asignadas | Sin duplicación, pero la relación no estaba documentada | Documentada (§3) y test T14 | No |
| Patas → garras | Los 0,007 kg de diferencia eran decomiso de patas + cutícula, no explicitados | Identidad explícita (§4), fila renombrada "merma de acondicionamiento de patas" y test T15 | No |
| Carcasa-esqueleto vs CMS | No coexistían, pero la ruta estaba **fija** por configuración (B vende, C procesa) | **Rutas alternativas seleccionables** (esqueleto, cuello, hueso de pechuga, piel) y tests T16–T17 | No en las rutas por defecto; nuevas variantes en el CSV |
| Comparación entero / trozado / deshuesado | La diferencia de masa comestible no estaba reconciliada | Reconciliación desde la misma base (§7) y test T21 | No |

## 2. Agua: dos conceptos que no deben confundirse

| | A. Agua de proceso total utilizada por la planta | B. Agua incorporada a productos y subproductos |
|---|---|---|
| Qué es | Todo el caudal que la planta consume: lavado de aves y carcasas, escaldado, llenado y renovación del chiller, limpieza, sanitización, lavado de camiones y cajones, servicios, otros usos | Solo el agua que queda **físicamente dentro o adherida** a una masa que sale del proceso |
| Orden de magnitud | Muy superior a B (litros por ave; se estimará en `11_agua_efluentes`) | 0,213 kg/ave con inmersión |
| ¿Está en este balance? | **NO** | **Sí**, en una columna separada de la masa biológica |

**Desagregación de B (kg/ave, 2,9 kg, inmersión):**

| Concepto | kg/ave | t/día a 10.000 aves/día | Destino |
|---|---|---|---|
| **Agua absorbida por la carcasa en el chiller** | 0,122 | 1,22 | — |
| · de la cual **agua retenida en producto** (se vende dentro del pollo o de los cortes) | 0,086 | 0,86 | Productos A y B |
| · de la cual **agua de goteo del producto** (purga antes de la venta) | 0,037 | 0,37 | Efluente (D) |
| **Agua adherida a plumas** (sale con la pluma húmeda) | 0,090 | 0,90 | Subproducto C |
| **Total agua incorporada a productos y subproductos** | **0,213** | **2,13** | — |

Con enfriamiento por aire, el agua absorbida por la carcasa es 0 (la carcasa pierde 0,037 kg de humedad biológica por evaporación) y el total baja a 0,090 kg/ave (solo plumas).

## 3. Decomisos vs pérdidas no asignadas

| Pregunta | Respuesta |
|---|---|
| ¿El decomiso ya está descontado de carcasa/productos? | **Sí.** Carcasa eviscerada 2,0735 − decomiso total de carcasa 0,0207 − decomiso parcial 0,0164 = **carcasa apta 2,0363 kg**. Los cortes y el pollo entero se calculan sobre la carcasa apta. Cuello, menudencias y patas también se descuentan en la fracción de aves decomisadas |
| ¿Forma parte de residuos? | **Sí:** clase **D** (residuo), etapa "condenas". Si la normativa permitiera enviarlo a rendering pasaría a C (DPV-066), nunca a P |
| ¿Está incluido dentro de pérdidas no asignadas? | **No.** Las pérdidas no asignadas (0,0406 kg) son la diferencia de la **composición primaria del ave** (100 % − Σ componentes) y se calculan **antes** de cualquier decomiso; tienen su propio origen (`perdidas_no_asignadas`) |
| ¿Es una variable adicional? | **No agrega masa:** redistribuye masa de carcasa, cuello, menudencias y patas hacia la clase D. Es una variable de escenario (bajo / medio / alto) |
| ¿Existe doble contabilización? | **No.** Test T14: la suma de decomisos = decomiso total × (carcasa + cuello + hígado + corazón + molleja + patas) + decomiso parcial; cada origen aparece una sola vez; la fila de pérdidas no asignadas es igual a la fracción primaria y la carcasa disponible = carcasa − decomisos − grasa retirada − evaporación |

**Detalle de los 0,0401 kg de decomisos por ave:** carcasa (total) 0,0207 + carcasa (parcial) 0,0164 + patas 0,0011 + cuello 0,0007 + hígado 0,0005 + molleja 0,0004 + corazón 0,0002.

## 4. Patas → garras

| Concepto | kg/ave | Definición |
|---|---|---|
| **Pata bruta (anatómica)** | **0,1131** | Pie + tarso cortado en la articulación tarsal, obtenido en la faena |
| − Patas de aves con decomiso total | 0,0011 | Van con el decomiso (D) |
| = Patas aptas antes de acondicionar | 0,1120 | |
| − **Merma de acondicionamiento** (cutícula y suciedad removidas al escaldar y pelar) | 0,0056 | Efluente / lodos (D) |
| = Patas acondicionadas (peladas) | 0,1064 | |
| · **Garra comercial grado A** | 0,0851 | Coproducto (B) |
| · **Garra de segunda** | 0,0160 | Coproducto (B) |
| · **Descarte** (lesiones graves, fracturas) | 0,0053 | Rendering (C) |

**Identidad (test T15):**

```
PATA BRUTA 0,1131 = GARRA A 0,0851 + SEGUNDA 0,0160 + DESCARTE 0,0053 + MERMA DE ACONDICIONAMIENTO 0,0056 + DECOMISO 0,0011
```

Los **~0,007 kg** entre la pata bruta (0,113) y garras + descarte (0,106) son **0,0056 de merma de acondicionamiento + 0,0011 de decomiso**. No desaparecen: están en D.

## 5. Carcasa → cortes (configuración B)

```
CARCASA EVISCERADA 2,0735 − decomiso total 0,0207 − decomiso parcial 0,0164 = CARCASA APTA 2,0363
CARCASA APTA 2,0363 − grasa retirada 0 − evaporación 0 (inmersión) = CARCASA DISPONIBLE PARA TROZAR 2,0363
```

| Corte | kg/ave | % de la carcasa disponible | Estado |
|---|---|---|---|
| Pechuga con hueso | 0,7840 | 38,5 % | **Con piel y con hueso** |
| Pata-muslo | 0,6313 | 31,0 % | **Con piel y con hueso**, sin espinazo |
| Alas | 0,2077 | 10,2 % | **Con piel y con hueso** |
| Carcasa-esqueleto | 0,3930 | 19,3 % | Con restos de carne, piel y grasa abdominal |
| Recortes (carne y piel) | 0,0102 | 0,5 % | Coproducto comestible |
| Merma de trozado | 0,0102 | 0,5 % | Merma real (P) |
| **Total** | **2,0363** | **100,0 %** | Test T05 |

No hay porcentaje faltante. La piel no se separa en el trozado (queda en cada corte); solo se separa en el deshuese (configuración C). Las cifras de deshuese (suprema, solomillo, muslo deshuesado) son **sin piel y sin hueso**; la pata en C se vende **con hueso y con piel**.

## 6. Rutas alternativas: vender o reprocesar (exclusivas)

Un material **se vende o se reprocesa, nunca las dos cosas**. El usuario elige una ruta por material (`--ruta-esqueleto`, `--ruta-cuello`, `--ruta-hueso-pechuga`, `--ruta-piel`):

| Material | Ruta 1 | Ruta 2 | Por defecto |
|---|---|---|---|
| Carcasa-esqueleto | **venta** → carcasa-esqueleto (B) | **cms** → CMS (B) + residuo óseo (C) + merma (P) | A y B: venta · C: cms |
| Cuello | **venta** → cuello (B) | **cms** → CMS + residuo + merma | venta |
| Hueso de pechuga (solo C) | **rendering** → hueso (C) | **cms** → CMS + residuo + merma | rendering |
| Piel (solo C) | **venta** → piel (B) | **rendering** → piel a rendering (C) | venta |

Cada material enviado a CMS se procesa en una etapa propia (`CMS (esqueleto)`, `CMS (cuello)`, `CMS (hueso de pechuga)`), de modo que se verifica **CMS + residuo óseo + merma = materia prima** (test T17). Tests T16/T17: la carcasa-esqueleto vendida y la CMS obtenida de ella nunca coexisten; el hueso de pechuga nunca aparece a la vez como hueso a rendering y como materia prima de CMS; el residuo óseo post-CMS es el único hueso de ese material.

**Efecto (kg/ave, 2,9 kg, masa biológica):**

| Variante | Carcasa-esqueleto vendida | CMS | Hueso + residuo óseo (C) | Mermas P de proceso | Comestible A + B |
|---|---|---|---|---|---|
| B, esqueleto → venta (defecto) | 0,393 | 0 | 0 | 0,010 | 2,311 |
| B, esqueleto → CMS | 0 | 0,236 | 0,153 | 0,014 | 2,154 |
| C, esqueleto → CMS (defecto) | 0 | 0,236 | 0,317 | 0,026 | 1,978 |
| C, esqueleto → venta | 0,393 | 0 | 0,164 | 0,022 | 2,135 |
| C, todo a CMS (esqueleto, cuello y hueso de pechuga) y piel a rendering | 0 | 0,342 | 0,284 (+ piel 0,110 a C) | 0,027 | 1,899 |

## 7. Entero / trozado / deshuesado desde la misma base

Mismo pollo vivo (2,9 kg), misma faena, mismas condenas y mismo enfriamiento: la masa comestible **disponible después de la inspección** es idéntica en las tres configuraciones (test T21).

| kg/ave (masa biológica) | A. Entero | B. Trozado | C. Deshuesado |
|---|---|---|---|
| Carcasa disponible | 2,036 | 2,036 | 2,036 |
| + menudencias y cuello aptos | 0,184 | 0,184 | 0,184 |
| + garras grado A y de segunda | 0,101 | 0,101 | 0,101 |
| **= Masa comestible disponible** | **2,321** | **2,321** | **2,321** |
| − Merma real de trozado / deshuese / CMS (P) | 0,001 | 0,010 | 0,026 |
| − Hueso retirado (C, **subproducto, no pérdida**) | 0 | 0 | 0,164 |
| − Residuo óseo de CMS (C) | 0 | 0 | 0,153 |
| **= Productos comestibles (A + B)** | **2,320** | **2,311** | **1,978** |
| de los cuales: producto principal (A) | 1,999 | 1,415 | 1,103 |
| de los cuales: coproducto comestible (B) | 0,321 | 0,896 | 0,875 |
| · piel separada (B) | 0 | 0 | 0,110 |
| · recortes (B) | 0,001 | 0,010 | 0,037 |
| · CMS (B) | 0 | 0 | 0,236 |

**Clasificación completa (suma = 2,900 kg en las tres):**

| Clase | A. Entero | B. Trozado | C. Deshuesado |
|---|---|---|---|
| A · Producto principal | 1,999 | 1,415 | 1,103 |
| B · Coproducto comestible | 0,321 | 0,896 | 0,875 |
| C · Subproducto valorizable | 0,443 | 0,443 | 0,760 |
| D · Residuo / efluente (incluye decomisos 0,040) | 0,095 | 0,095 | 0,095 |
| P · Merma real (incluye pérdidas no asignadas 0,041) | 0,041 | 0,051 | 0,066 |
| **Total** | **2,900** | **2,900** | **2,900** |

**Lectura:**

1. **La diferencia entre A y B (0,009 kg) es solo merma real de sierra y exudado.** Todo lo demás se reclasifica: 0,58 kg/ave pasan de producto principal a coproducto (alas, carcasa-esqueleto) **sin desaparecer**.
2. **La diferencia entre B y C (0,333 kg) es 0,317 kg de hueso y residuo óseo que pasan a subproducto (C) y solo 0,016 kg de merma real adicional.** El hueso **no es una pérdida**: es un subproducto con destino (rendering, caldos) y aparece en la clase C.
3. Para el futuro cálculo del **ingreso total por ave**, cada kilogramo debe valorizarse en su clase y destino: un kilo que pasa de A a B cambia de precio, no de existencia.
4. Con peso comercial (masa biológica + agua retenida), los comestibles son 2,406 / 2,396 / 2,050 kg: la diferencia entre ambos pesos es siempre la misma agua (0,086 kg) y **no** es rendimiento biológico.

## 8. Balance manual de un pollo de 2,9 kg

### Tabla 1 — Masa biológica (sin agua)

| Salida biológica | kg/ave | % PV |
|---|---|---|
| Carcasa apta (eviscerada, después de decomisos) | 2,0363 | 70,22 % |
| Cuello (apto) | 0,0746 | 2,57 % |
| Hígado (apto) | 0,0545 | 1,88 % |
| Corazón (apto) | 0,0144 | 0,50 % |
| Molleja (apta) | 0,0402 | 1,39 % |
| Patas (aptas, antes de acondicionar) | 0,1120 | 3,86 % |
| Sangre | 0,0986 | 3,40 % |
| Plumas (masa biológica) | 0,1508 | 5,20 % |
| Cabeza | 0,0725 | 2,50 % |
| Vísceras no comestibles (tracto, pulmones, otros) | 0,1305 | 4,50 % |
| Contenido intestinal | 0,0348 | 1,20 % |
| Decomisos (total + parcial; carcasa, cuello, menudencias y patas) | 0,0401 | 1,38 % |
| Pérdidas no asignadas | 0,0406 | 1,40 % |
| **Total salidas biológicas** | **2,9000** | **100,00 %** |
| **Entrada biológica (peso vivo en planta)** | **2,9000** | |
| Error de cierre | < 1 × 10⁻¹⁵ kg | |

### Tabla 2 — Agua incorporada y peso comercial (separada; no es consumo de agua de la planta)

| Concepto (inmersión 6 %) | kg/ave |
|---|---|
| Carcasa disponible antes del chiller (masa biológica) | 2,0363 |
| + Agua absorbida por la carcasa en el chiller | 0,1222 |
| − Agua de goteo del producto antes de la venta (→ efluente) | 0,0367 |
| = Agua retenida en producto | 0,0855 |
| **Peso comercial de la carcasa** (2,0363 bio + 0,0855 agua) | **2,1219** |
| Agua adherida a plumas (sale con la pluma húmeda; no es producto) | 0,0905 |
| Con enfriamiento por aire: evaporación (masa biológica perdida, clase P) y peso comercial | −0,0367 → 1,9996 |

El agua retenida (4,0 % del peso comercial) **no aumenta el rendimiento biológico**: la carcasa sigue siendo 70,22 % del PV en masa biológica (tests T19–T20).

## 9. Tests de exclusividad agregados (versión 1.1)

| Test | Qué garantiza | Resultado |
|---|---|---|
| T14 | Decomisos una sola vez, en D, fuera de pérdidas no asignadas y ya descontados de la carcasa disponible | OK |
| T15 | Pata bruta = garras A + segunda + descarte + merma de acondicionamiento + decomiso | OK |
| T16 | Carcasa-esqueleto vendida XOR CMS de esqueleto; cuello vendido XOR CMS; piel vendida XOR a rendering | OK |
| T17 | Hueso original y residuo óseo post-CMS no se duplican; CMS + residuo + merma = materia prima | OK |
| T18 | Cada salida pertenece a una sola categoría final; Σ clases = PV | OK |
| T19 | La masa biológica es idéntica con 6 % y 8 % de absorción: cierra independientemente del agua | OK |
| T20 | El agua retenida no aumenta el rendimiento biológico (el chiller no suma masa biológica) | OK |
| T21 | La masa comestible disponible es la misma en A, B y C; disponible − merma − reclasificado a C = comestible | OK |

Los tests se ejecutan sobre **1.008 balances** (144 de la grilla del CSV + 864 combinaciones de todas las rutas × 3 configuraciones × 3 pesos × 3 rendimientos × 2 enfriamientos). **Prueba de los tests:** se introdujeron seis errores deliberados (decomiso sumado a pérdidas no asignadas, carcasa-esqueleto vendida junto con su CMS, merma de patas omitida, hueso de pechuga duplicado, agua sumada a la masa biológica, piel en dos clases); **todos fueron detectados** (T14, T16, T15, T17, T19/T20 y T18 respectivamente, además de los tests de cierre).
