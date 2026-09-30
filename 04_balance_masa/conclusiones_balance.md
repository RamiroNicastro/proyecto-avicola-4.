# Conclusiones del balance de masa

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual) · Base: [`auditoria_balance.md`](auditoria_balance.md), [`balance_por_ave.md`](balance_por_ave.md), [`rendimientos_cortes.md`](rendimientos_cortes.md), [`subproductos_masa.md`](subproductos_masa.md), [`agua_y_mermas.md`](agua_y_mermas.md), [`guia_ramiro.md`](guia_ramiro.md), [`modelo_balance_masa.py`](modelo_balance_masa.py), [`escenarios_balance.csv`](escenarios_balance.csv)

> **ALCANCE:** este es un **balance de masa del ave y sus productos**. **No** es todavía un balance de agua industrial, ni de efluentes, ni energético, ni un modelo económico, ni un diseño de maquinaria. **ESTE BALANCE NO DIMENSIONA EL CONSUMO INDUSTRIAL DE AGUA NI EL CAUDAL TOTAL DE EFLUENTES DE LA PLANTA.**
> **No** se calcula rentabilidad, **no** se seleccionan productos comerciales, **no** se diseña maquinaria ni layout y **no** se fija capacidad. Las escalas de 2.500–20.000 aves/día y 1.000.000 aves/año son **escenarios** para ordenar magnitudes.
> **Fuentes:** acceso directo bloqueado (quinta sesión consecutiva; WebFetch y curl con `EGRESS_BLOCKED`/403, DPV-009). Toda cifra externa es `[PVDP]`; los parámetros del modelo son `[ESTIMACIÓN]`/`[SUPUESTO]` (SUP-035 a SUP-045). **Ningún rendimiento proviene de una planta argentina.**

---

## 1. Balance medio de un pollo de 2,8–3,0 kg vivo

Escenario medio, masa biológica, kg/ave y % del peso vivo en planta. Suma = PV (error de cierre < 2 × 10⁻¹⁵ kg).

| Destino | 2,8 kg | **2,9 kg** | 3,0 kg | Clase |
|---|---|---|---|---|
| **Carcasa eviscerada** (sin cuello ni menudencias) | 1,997 (71,3 %) | **2,073 (71,5 %)** | 2,151 (71,7 %) | A/B según configuración |
| Cuello | 0,073 (2,6 %) | 0,075 (2,6 %) | 0,078 (2,6 %) | B |
| Menudencias (hígado + corazón + molleja) | 0,108 (3,9 %) | 0,110 (3,8 %) | 0,113 (3,8 %) | B |
| Patas (→ garras) | 0,110 (3,9 %) | 0,113 (3,9 %) | 0,116 (3,9 %) | B/C/D |
| Sangre | 0,095 (3,4 %) | 0,099 (3,4 %) | 0,102 (3,4 %) | C/D |
| Plumas (masa biológica) | 0,146 (5,2 %) | 0,151 (5,2 %) | 0,155 (5,2 %) | C |
| Cabeza | 0,071 (2,5 %) | 0,072 (2,5 %) | 0,074 (2,5 %) | C |
| Vísceras no comestibles (sin contenido) | 0,127 (4,5 %) | 0,130 (4,5 %) | 0,134 (4,5 %) | C |
| Contenido gastrointestinal | 0,034 (1,2 %) | 0,035 (1,2 %) | 0,036 (1,2 %) | D |
| Pérdidas no asignadas | 0,039 (1,4 %) | 0,041 (1,4 %) | 0,042 (1,4 %) | P |
| **Total** | **2,800** | **2,900** | **3,000** | |

Después: decomisos (medio 1,4 % PV), enfriamiento (+0,122 kg de agua absorbida por inmersión o −0,037 kg de evaporación por aire a 2,9 kg) y trozado/deshuese según la configuración.

## 2. Rendimiento eviscerado

| Escenario | 2,2 kg | 2,5 kg | 2,8 kg | 2,9 kg | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| Bajo | 68,7 % | 69,2 % | 69,8 % | 70,0 % | 70,2 % | 70,6 % | 71,1 % |
| **Medio** | **70,2 %** | **70,7 %** | **71,3 %** | **71,5 %** | **71,7 %** | **72,1 %** | **72,6 %** |
| Alto | 71,4 % | 71,9 % | 72,5 % | 72,7 % | 72,9 % | 73,3 % | 73,8 % |

Definición: carcasa caliente sin cabeza, patas, cuello ni menudencias, sin agua. Con cuello: +2,6 pp; con cuello y menudencias: +6,4 pp (77,9 % a 2,9 kg). Objetivo genético Cobb ~74–76 % (definición no confirmada, contradicción entre extractos, DPV-059).

## 3. Rendimientos por corte (2,9 kg, medio)

| Corte | % de la carcasa apta | % de la carcasa eviscerada | % PV | kg/ave |
|---|---|---|---|---|
| Pechuga con hueso | 38,5 % | 37,8 % | 27,0 % | 0,784 |
| — suprema / solomillo (deshuese) | 23,5 % / 5,8 % | 23,1 % / 5,7 % | 16,5 % / 4,1 % | 0,478 / 0,118 |
| Pata-muslo | 31,0 % | 30,4 % | 21,8 % | 0,631 |
| — muslo / pata | 18,0 % / 13,0 % | 17,7 % / 12,8 % | 12,6 % / 9,1 % | 0,366 / 0,265 |
| — muslo deshuesado sin piel | 11,9 % | 11,7 % | 8,3 % | 0,242 |
| Alas | 10,2 % | 10,0 % | 7,2 % | 0,208 |
| Carcasa-esqueleto | 19,3 % | 19,0 % | 13,6 % | 0,393 |
| — CMS (60 %) | 11,6 % | 11,4 % | 8,1 % | 0,236 |
| Piel separada (config. C) | 5,4 % | 5,3 % | 3,8 % | 0,110 |
| Recortes + mermas | 1,0 % | 1,0 % | 0,7 % | 0,020 |

Detalle por peso: [`rendimientos_cortes.md`](rendimientos_cortes.md).

## 4. kg de cada subproducto por ave (2,9 kg, medio)

| Salida | kg/ave | Clase |
|---|---|---|
| Plumas: biológica / húmeda (con agua de escaldado) | 0,151 / 0,241 | C |
| Sangre recuperada / no recuperada | 0,084 / 0,015 | C / D |
| Cabeza | 0,072 | C |
| Tracto digestivo / pulmones / otros no comestibles | 0,087 / 0,017 / 0,026 | C |
| Contenido gastrointestinal | 0,035 | D |
| Garras grado A / segunda / descarte | 0,085 / 0,016 / 0,005 | B / B / C |
| Merma de acondicionamiento de patas (cutícula) | 0,006 | D |
| Decomisos (total + parcial) | 0,040 | D |
| Agua de goteo del producto | 0,037 (agua) | D |
| Hueso / residuo óseo de CMS (solo config. C) | 0,164 / 0,153 | C |
| Piel (solo config. C) | 0,110 | B (o C) |

## 5. Balance para 10.000 aves/día (2,9 kg, configuración B, medio, inmersión)

Entrada: **29,0 t/día de pollo vivo** (masa biológica) + 2,13 t/día de **agua incorporada a productos y subproductos** (agua absorbida por la carcasa en el chiller 1,22, de la cual 0,86 queda retenida en producto y 0,37 gotea; agua adherida a plumas 0,90). **Esto no es el consumo de agua de la planta ni el caudal de efluentes**, que se calcularán en `11_agua_efluentes`. t/año con 250 días de faena.

| Clase | Salida | t/día | t/año |
|---|---|---|---|
| A | Pechuga con hueso | 8,17 | 2.043 |
| A | Pata-muslo | 6,58 | 1.645 |
| B | Carcasa-esqueleto | 4,10 | 1.024 |
| B | Alas | 2,16 | 541 |
| B | Cuello | 0,75 | 187 |
| B | Hígado / corazón / molleja | 0,55 / 0,14 / 0,40 | 136 / 36 / 100 |
| B | Garras grado A / segunda | 0,85 / 0,16 | 213 / 40 |
| B | Recortes | 0,11 | 27 |
| C | Plumas crudas húmedas | 2,41 | 603 |
| C | Tracto digestivo | 0,87 | 217 |
| C | Sangre recuperada | 0,84 | 210 |
| C | Cabezas | 0,72 | 181 |
| C | Otros no comestibles + pulmones + garras de descarte | 0,49 | 122 |
| D | Decomisos | 0,40 | 100 |
| D | Agua de goteo del producto | 0,37 | 92 |
| D | Contenido GI | 0,35 | 87 |
| D | Sangre no recuperada + merma de acondicionamiento de patas | 0,20 | 51 |
| P | Pérdidas no asignadas + merma de trozado | 0,51 | 127 |
| | **Total salidas** | **31,13** | **7.782** |

Productos A = 14,75 t/día; comestible A + B = 23,96 t/día (de los cuales ~0,86 t/día es agua retenida). Con 2,8 kg / 3,0 kg: A = 14,19 / 15,32 t/día. Configuraciones A y C, otros pesos y escenarios: CSV (columnas `t_dia_10000_aves_dia`, `t_anio_10000_aves_dia`).

## 6. Efecto del peso vivo

- **No es lineal.** Entre 2,2 y 3,5 kg (×1,59), la pechuga crece ×1,72, la pata-muslo ×1,62, las alas ×1,55, la cabeza ×1,36 y la molleja ×1,32. El rendimiento eviscerado sube ~1,9 pp por kg.
- Aves por tonelada de filet: **2.305** (2,2 kg) → **1.678** (2,9 kg) → **1.344** (3,5 kg).
- A 2,2 kg la garra grado A pesa ~34 g/pieza (límite inferior del calibre comercial de 35–50 g).
- Las pendientes son **supuestos de magnitud** con dirección respaldada por la literatura (DPV-059). **No se concluye qué peso conviene** (DEC-021).

## 7. Entero / trozado / deshuesado (2,9 kg, medio)

| kg/ave (masa biológica) | A. Entero | B. Trozado | C. Deshuesado |
|---|---|---|---|
| Productos principales | 1,999 | 1,415 | 1,103 |
| Partes secundarias comestibles | 0,320 | 0,886 | 0,728 |
| Hueso separado | 0 | 0 | 0,317 |
| Piel separada | 0 | 0 | 0,110 |
| Recortes | 0,001 | 0,010 | 0,037 |
| Subproductos (C) | 0,443 | 0,443 | 0,760 |
| **Comestible total** | **2,320** | **2,311** | **1,978** |

Desde la misma masa comestible disponible (2,321 kg/ave en las tres): A pierde 0,001 kg de merma real, B 0,010 y C 0,026; C además **reclasifica** 0,317 kg de hueso y residuo óseo a subproducto (C), que **no es pérdida** ([`auditoria_balance.md` §7](auditoria_balance.md)). Trozar reordena la masa (≈ 0,58 kg/ave pasan de producto principal a coproducto) sin perderla; deshuesar saca ~0,33 kg/ave de hueso y residuo (−14 % comestible) y crea piel, recortes y CMS que necesitan compradores. Aun en A, un 3–12 % de las canales no es apto para venta entera. **No se decide cuál conviene** (DEC-005): depende de precios netos por parte (SUP-013, SUP-017).

## 8. Datos débiles o contradictorios

| # | Tema | Problema | Registro |
|---|---|---|---|
| 1 | **Todo el modelo** | Ningún documento original leído; ninguna medición argentina | DPV-009, DPV-060 |
| 2 | Rendimiento Cobb 500 a 2,8 kg | 74,03 % vs 75,55–75,85 % entre extractos; definición de "carcass" sin confirmar | DPV-059 |
| 3 | Filet Cobb | 22,57 % vs 26,05–26,50 % PV entre extractos | DPV-059 |
| 4 | Suma de subproductos de la literatura | Supera el 100 % con la carcasa: definiciones incompatibles (pluma húmeda/seca, molleja sucia/limpia) | §3 de `balance_por_ave.md` |
| 5 | Participación de cortes | Referencias con espinazo repartido (40/12/32/16 % del RTC) vs cortes argentinos sin especificación | DPV-068 |
| 6 | Deshuese (carne/piel/hueso), CMS | Mayormente supuestos; CMS de fuente débil | DPV-069 |
| 7 | Tracto, pulmones, otros no comestibles, contenido GI | Sin datos individuales: supuestos | DPV-060 |
| 8 | Límite de agua en Argentina (8 %) | Solo prensa que cita a SENASA; decreto no leído | DPV-061 |
| 9 | Goteo del agua absorbida (30 %) | Sin fuente | DPV-062 |
| 10 | Decomisos | Solo Brasil; masa recortada en decomisos parciales estimada | DPV-063 |
| 11 | Garras: definición y grados | Especificaciones de ofertas comerciales (débil); pata vs garra según comprador | DPV-064 |
| 12 | Rendering | Sin rendimiento de harinas por kg de materia prima | DPV-065 |
| 13 | DQO de la sangre | Un extracto con "DBO ~100 mg/L" (incoherente, descartado) vs 375.000 mg/L de DQO | DPV-067 |
| 14 | Pendientes con el peso | Magnitud supuesta | DPV-059 |
| 15 | Pérdidas no asignadas (1,4 %) | Surgen por cierre; podrían esconder errores de otros parámetros | DPV-060 |

## 9. Información a medir en una planta real

### 9.1 Datos

| Dato | Cómo medirlo | Precisión objetivo |
|---|---|---|
| **Peso vivo real** en granja y en planta | Balanza de camión (lleno/vacío) + conteo; muestra individual de 50–100 aves con balanza de 1 g | Lote y ave |
| Horas de ayuno, captura, viaje y espera; DOA | Registro de tiempos | — |
| **Sangre** | Pesar aves identificadas antes y después del desangrado (bandeja tarada); volumen del tanque de sangre por lote | g/ave; % recuperada |
| **Plumas** | Peso después del desangrado y después del desplumado (incluye agua de escaldado); muestra de pluma para **materia seca** en laboratorio | kg húmedo y seco/ave |
| Cabeza y **patas** | Pesaje de muestra; garras después del pelado; **clasificación de grado** (A/segunda/descarte) y calibre por pieza; pododermatitis | g/ave; % por grado |
| **Menudencias** y cuello | Pesaje por separado (hígado, corazón, molleja limpia, cuello con/sin piel) | g/ave |
| Vísceras no comestibles y **contenido GI** | Pesar el paquete completo de muestra; vaciar y pesar el contenido | g/ave |
| **Peso eviscerado** (carcasa caliente) | Pesaje individual de aves identificadas (anillo en ala/pata) antes del chiller | g/ave |
| **Absorción de agua** | Mismas carcasas pesadas antes y después del chiller y a las 24 h (goteo en bandeja) | % absorbido y retenido |
| **Carcasa fría y cortes** | Despiece de la muestra por un operario entrenado: pechuga, pata-muslo (muslo, pata), alas, carcasa, recortes | g y % de carcasa |
| **Deshuese** | Deshuese de la muestra: suprema, solomillo, muslo, piel, hueso, recortes | % del corte |
| **Condenas** | Registros del servicio de inspección (total y parcial, por causa) de al menos 4–8 semanas; masa recortada en una muestra | % aves; % masa |
| **Mermas y pérdidas** | Por diferencia en cada etapa del ensayo individual | % PV |
| Grasa abdominal | Pesaje en la muestra (y si la planta la retira) | g/ave |

### 9.2 Protocolo de ensayo de balance de masa (propuesta)

1. **Acuerdo con una planta** (propia en el futuro, a façon o colaboradora; DEC-028) y con el servicio de inspección; balanzas verificadas con pesas patrón (1 g para carcasas y cortes; 0,1 g para menudencias).
2. **Diseño:** al menos **3 lotes de 3 productores distintos** y, si es posible, **2 estaciones** (verano/invierno); separar machos y hembras si el lote lo permite; registrar genética, edad, peso y horas de ayuno.
3. **Tamaño de muestra:** para estimar el rendimiento medio con ±0,5 puntos al 95 % con un desvío de ~1,5 puntos hacen falta ~35 aves por grupo: tomar **50 aves identificadas por lote** (para absorber pérdidas de identificación).
4. **Secuencia de pesajes por ave:** vivo → desangrado → desplumado → sin cabeza y patas → eviscerado (menudencias y cuello aparte) → antes del chiller → después del chiller → 24 h (goteo) → cortes → deshuese.
5. **Balance de lote en paralelo:** peso vivo total del lote vs kg de cada corriente (tanque de sangre, contenedores de plumas y vísceras, producto terminado) para validar la muestra a escala.
6. **Laboratorio:** materia seca de plumas, sangre y vísceras (para rendering) y agua/proteína en carcasas (para el control de agua).
7. **Cierre:** para cada ave, peso vivo − Σ partes = pérdidas; el ensayo es aceptable si la pérdida no explicada es < 2 % y se documenta su origen.
8. **Carga al modelo:** reemplazar los parámetros de `modelo_balance_masa.py` (tablas `PRIMARIOS`, `CORTES`, `DESHUESE`, `CONDENAS`, `ENFRIAMIENTO`), volver a correr los tests y registrar las fuentes como mediciones propias.

## 10. Lo que Ramiro debe aprender

Resumen en [`guia_ramiro.md`](guia_ramiro.md): (1) rendimiento de faena = carcasa / peso vivo, **siempre con su definición**; (2) rendimiento de corte = corte / carcasa; (3) **no sumar % sobre vivo con % sobre carcasa**; (4) producto ≠ coproducto ≠ subproducto ≠ residuo, y una parte cambia de clase si no tiene comprador; (5) balance de masa = cada kilo tiene un destino y la suma cierra; (6) **el agua del chiller no es carne** (0,122 kg por ave de diferencia entre inmersión y aire); (7) las mermas existen y hay que medirlas; (8) las condenas se originan en gran parte en la granja, la captura y el ayuno; (9) **1 punto de rendimiento = 29 g/ave = 72,5 t/año a 10.000 aves/día**, sin costo adicional de crianza.

## 11. Resultado de los tests

`python3 04_balance_masa/modelo_balance_masa.py` (versión 1.1) — **21/21 correctos** sobre **1.008 balances**: los 144 del CSV (6 pesos × [3 configuraciones × 7 variantes de rendimiento, condenas y enfriamiento + 3 variantes de ruta]) y 864 combinaciones de todas las rutas alternativas:

| Test | Resultado |
|---|---|
| T01 Cierre por ave (total, masa biológica y agua por separado) | OK — error máximo 1,8 × 10⁻¹⁵ kg/ave (tolerancia 1 × 10⁻⁶ kg = 1 mg) |
| T02 Cierre por 1.000 aves | OK |
| T03 Ningún componente negativo | OK |
| T04 Porcentajes dentro de las bandas de fuentes (incluye agua retenida ≤ 8 % y pérdidas no asignadas 0–4 %) | OK |
| T05 Suma de cortes ≤ carcasa (igual a la carcasa apta asignada) | OK |
| T06 Suma de deshuesados ≤ corte de origen | OK |
| T07 Escalado lineal (1 ave → 1.000 → t/día → t/año) | OK |
| T08 Agua separada de la masa biológica | OK |
| T09 Unidades consistentes (fracciones suman 1; kg primarios = PV) | OK |
| T10 Sin doble conteo (cada componente primario asignado una sola vez) | OK |
| T11 No linealidad con el peso (pechuga crece más que el PV; cabeza y patas menos) | OK |
| T12 Rechazo de pesos fuera de 2,0–3,8 kg (el script se detiene) | OK |
| T13 Toda salida clasificada A/B/C/D/P | OK |
| T14 Decomisos no duplicados (una vez, en D, fuera de pérdidas no asignadas y ya descontados de la carcasa) | OK |
| T15 Pata bruta = garras A + segunda + descarte + merma de acondicionamiento + decomiso | OK |
| T16 Rutas exclusivas: carcasa-esqueleto vendida XOR CMS; cuello XOR CMS; piel venta XOR rendering | OK |
| T17 Hueso original y residuo óseo post-CMS no se duplican (CMS + residuo + merma = materia prima) | OK |
| T18 Cada salida en una sola categoría final (Σ clases = PV) | OK |
| T19 Masa biológica idéntica con 6 % y 8 % de absorción (cierra sin depender del agua) | OK |
| T20 El agua retenida no aumenta el rendimiento biológico | OK |
| T21 Misma masa comestible disponible en A/B/C y reconciliación disponible − merma − reclasificado = comestible | OK |

**Prueba de los tests (mutaciones):** se alteró deliberadamente el modelo (cortes que suman más que la carcasa; agua sumada a la masa biológica del pollo entero; deshuese con más carne que el corte; absorción de 15 %): en todos los casos fallaron los tests correspondientes y el script se detiene con código de salida 1. En la auditoría v1.1 se agregaron seis mutaciones más (decomiso sumado a pérdidas, carcasa-esqueleto vendida junto con su CMS, merma de patas omitida, hueso de pechuga duplicado, agua como carne, piel en dos clases): todas detectadas ([`auditoria_balance.md` §9](auditoria_balance.md)).

## 12. Archivos creados y modificados

**Creados:** `04_balance_masa/auditoria_balance.md` (v1.1), `balance_por_ave.md`, `rendimientos_cortes.md`, `subproductos_masa.md`, `agua_y_mermas.md`, `escenarios_balance.csv`, `modelo_balance_masa.py`, `guia_ramiro.md`, `conclusiones_balance.md`.
**Modificados:** `04_balance_masa/README.md` (documentación del modelo); `00_gestion_proyecto/supuestos.md` (SUP-035 a SUP-045; SUP-019 y SUP-023 anotados), `datos_por_validar.md` (DPV-059 a DPV-069; DPV-008 actualizado), `decisiones_pendientes.md` (DEC-026 a DEC-028; notas en DEC-001, DEC-005, DEC-014, DEC-021), `estado_proyecto.md`, `glosario.md`; `25_fuentes/registro_fuentes.csv` (FTE-161 a FTE-184; FTE-140 y FTE-142 anotados), `25_fuentes/bibliografia.md`.

## 13. Control de calidad y evaluación

- [x] Base vivo y base carcasa separadas en todas las tablas y en dos columnas del CSV.
- [x] Agua no contada como carne: columnas separadas y tests T08, T19, T20; nomenclatura inequívoca (agua incorporada a productos y subproductos ≠ agua de proceso de la planta).
- [x] Auditoría conceptual v1.1: sin doble contabilización; decomisos, patas, cortes, rutas CMS y comparación de configuraciones reconciliados ([`auditoria_balance.md`](auditoria_balance.md)).
- [x] Patas y menudencias fuera de la carcasa y de los cortes; ningún kg en dos productos (test T10).
- [x] Rendimientos de fuente débil señalados (§8) y pérdidas visibles como filas propias (clase P).
- [x] Contradicciones identificadas (Cobb, suma de la literatura, definiciones de cortes, DQO de la sangre).
- [x] Balances verificados numéricamente (1.008 balances; error ≤ 1,8 × 10⁻¹⁵ kg/ave).
- [x] Sin precios, sin selección de productos, maquinaria ni layout.
- [ ] Verificación documental primaria (bloqueada; DPV-009, DPV-059, DPV-061).
- [ ] Mediciones en planta argentina (DPV-060).

**Evaluación de calidad: MEDIA** como modelo y método (reproducible, trazable, con tests y separación explícita de bases, agua y clases); **BAJA** como evidencia numérica (ningún original leído, ningún dato argentino, varios componentes supuestos). Sirve para **dimensionar órdenes de magnitud y ordenar preguntas**, no para diseñar la planta ni para calcular ingresos definitivos.
