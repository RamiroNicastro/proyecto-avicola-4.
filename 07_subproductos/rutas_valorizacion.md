# Rutas alternativas de valorización

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Objetivo:** mostrar, para cada material con más de un destino, qué rutas existen, cuáles son **incompatibles** entre sí y qué información decide la elección. **No se elige ganador** (DEC-005, DEC-027, DEC-029, DEC-031).
> **Regla de oro:** un kilogramo sigue **una sola ruta** en cada escenario. Dos rutas incompatibles **nunca** se suman económicamente (SUP-045). El modelo lo garantiza para las rutas modeladas (tests T16–T17 del balance y S04 de [`modelo_subproductos.py`](modelo_subproductos.py)); para las rutas no modeladas (pet food, compost, harina propia) la regla es la misma y se aplicará en el modelo económico.

---

## 1. Carcasa-esqueleto: vender / CMS / rendering

0,393 kg/ave (13,6 % del PV) en configuración B; a 10.000 aves/día, **4,1 t/día**: después de pechuga y pata-muslo es la **mayor masa comestible** del ave.

| | **Ruta A — vender carcasa-esqueleto** | **Ruta B — procesar a CMS** | **Ruta C — rendering** |
|---|---|---|---|
| Producto obtenido | Carcasa para caldo/sopa (0,393 kg/ave) | CMS 0,236 + residuo óseo 0,153 (a rendering) + merma 0,004 | Harina y grasa (rendimiento no asumido, DPV-065) |
| Clase | B | B (CMS) + C (residuo) | C |
| Complejidad | Baja | Media–alta: separadora, enfriado o congelado inmediato, microbiología | Baja para la faena (la complejidad está en el rendering) |
| Regulación | Venta como menudencia/coproducto | Res. SENASA 368/2003: CMS **solo** para chacinados cocidos y conservas; −2 a 2 °C y uso en 12 h o congelado −18 °C (FTE-185 `[PVDP]`, SUP-048) | Decreto 4238 (digestor), Res. 1416/2024; harina prohibida para rumiantes |
| Frío | Refrigerado o congelado | **Crítico** (12 h refrigerada) | No, si se retira en horas |
| Necesidad de comprador | Mayorista, carnicería, pet food, industria de caldos | Industria de chacinados cocidos (hoy importa CMS de Brasil) | Rendering habilitado |
| Valor agregado relativo | Bajo | Bajo por kg de CMS; sustituye importaciones | Mínimo (piso) |
| Cuándo tendría sentido | Si hay comprador de carcasa a precio > CMS neta de proceso | Si hay comprador industrial estable y la carcasa no se vende | Solo si A y B no tienen comprador |

**Por qué no se elige:** A y B dependen de compradores no identificados (DPV-070, DPV-071); la comparación exige `k_carcasa × NB_carcasa` vs `k_CMS × NB_CMS + k_residuo × NB_rendering − costo de CMS` (fórmula de SUP-017). Decisión: **DEC-029**.

## 2. Árboles de decisión por material

Notación: `├─` ruta posible · **[X]** incompatible con las demás ramas del mismo nodo · `(?)` requiere validar normativa o comprador.

```
CARCASA-ESQUELETO (0,393 kg/ave)                           [rutas excluyentes]
├─ Vender (caldos, mayoristas, pet food)          → B
├─ Separar CMS → CMS 60 % (B) + residuo óseo 39 % (C) + merma 1 %
│               └─ residuo óseo → rendering (no volver a contarlo como hueso)
└─ Rendering                                      → C (si A y B no tienen comprador)

CUELLO (0,075)                                             [excluyentes]
├─ Vender como menudencia / pet food              → B
├─ CMS (0,045) + residuo óseo                     → B + C
└─ Rendering                                      → C

PECHUGA CON HUESO (0,784)                                  [excluyentes]
├─ Vender con hueso                               → A
└─ Deshuesar → suprema 0,478 + solomillo 0,118 (A) + piel 0,063 + recortes 0,016 (B) + hueso 0,102
                 ├─ hueso → rendering (defecto)   → C
                 └─ hueso → CMS (0,061)           → B + residuo C        [hueso: rendering XOR CMS]

PATA-MUSLO (0,631)                                         [excluyentes]
├─ Vender entera                                  → A
├─ Separar muslo (0,366) + pata (0,265)           → A
│   └─ Deshuesar muslo → carne 0,242 (A) + piel 0,048 + recortes 0,011 (B) + hueso 0,062 (C)
└─ Congelar como cuarto trasero (exportación)     → A (?) comprador

PATAS (0,113 brutas)                                        [excluyentes]
├─ Escaldar + pelar + clasificar → garras A 0,085 / segunda 0,016 (B) + descarte 0,005 (C) + cutícula 0,006 (D)
│   ├─ Exportar congeladas (China (?) / Vietnam / Hong Kong / Medio Oriente)
│   └─ Mercado interno / pet food (?)
├─ Vender sin pelar (pet food, procesador)        → B (?) comprador
└─ Rendering                                      → C

MENUDENCIAS (hígado 0,055 · corazón 0,014 · molleja 0,040)   [excluyentes]
├─ Dentro del pollo entero (bolsita)              → B
├─ Venta separada refrigerada / congelada         → B
├─ Pet food (materia prima apta)                  → B (?)
├─ Exportación congelada (África / Asia)          → B (?)
└─ Rendering (sin comprador)                      → C

PIEL (0,110; solo con deshuese)                             [excluyentes]
├─ Industria (embutidos, emulsiones)              → B (?)
├─ Elaborados propios (hamburguesas, medallones)  → B (DEC-030)
└─ Rendering (grasa + harina)                     → C

GRASA ABDOMINAL (0,052)                                     [excluyentes]
├─ Queda en la carcasa (defecto)                  → se vende con el producto
├─ Se retira → grasería (grasa alimentaria)       → B (?)
└─ Se retira → rendering                          → C
   (si se retira, sale de la carcasa: no se suma dos veces)

PLUMAS (0,241 húmedas)                                      [excluyentes]
├─ Vender/entregar cruda a rendering externo      → C (ingreso, cero o costo)
├─ Planta propia → harina de plumas hidrolizada   → C (DEC-027; no se asume)
├─ Compostaje / enmienda                          → C/D (?) normativa
└─ Disposición                                    → D (costo)

SANGRE (0,099 drenada)
├─ Recuperar por separado (0,084) ────────────────┐       [recuperada: excluyentes]
│   ├─ Vender/entregar a rendering (co-proceso)   → C
│   ├─ Harina de sangre propia                    → C (no se asume)
│   └─ Sin receptor → disposición                 → D
├─ No recuperada (0,015)                          → D efluente (inevitable)
└─ No recuperar nada → todo al efluente           → D (≈ 7 veces más DQO; no recomendable)

VÍSCERAS NO COMESTIBLES (0,130 + contenido GI 0,035)        [excluyentes]
├─ Rendering (harina de vísceras)                 → C
├─ Biodigestión (biogás)                          → C/D (?) teórica
├─ Compostaje                                     → C/D (?)
└─ Disposición                                    → D

CABEZAS (0,072)                                             [excluyentes]
├─ Rendering                                      → C
├─ Pet food                                       → C (?) comprador y normativa
└─ Disposición                                    → D

DECOMISOS (0,040)
├─ Digestor / rendering (si la causa y la norma lo permiten) → C (?) DPV-066
└─ Incineración / disposición                     → D (defecto prudencial)
```

## 3. Incompatibilidades que el modelo económico debe respetar

| # | No sumar | Por qué |
|---|---|---|
| 1 | Carcasa-esqueleto vendida **+** CMS del esqueleto | Misma masa (tests T16, S04) |
| 2 | Hueso de pechuga a rendering **+** CMS de hueso de pechuga | Misma masa (T17) |
| 3 | Hueso original **+** residuo óseo post-CMS del mismo material | El residuo **es** el hueso después de la separación (T17) |
| 4 | Pechuga con hueso **+** suprema/solomillo | Presentaciones alternativas de la misma pechuga |
| 5 | Pata-muslo **+** muslo o pata por separado | Idem |
| 6 | Pollo entero **+** cortes del mismo pollo | Configuración A vs B/C (salvo el 3–12 % de canales no aptas para entero, que se trozan) |
| 7 | Piel vendida **+** piel a rendering | T16, S04 |
| 8 | Grasa en la carcasa **+** grasa retirada | Si se retira, se descuenta de la carcasa |
| 9 | Menudencias dentro del entero **+** menudencias vendidas aparte | Misma masa |
| 10 | Cuellos/carcasas/menudencias a **pet food** **+** mismos a mercado alimentario o CMS | Pet food es ruta **alternativa**, no adicional |
| 11 | Plumas entregadas a tercero **+** harina de plumas propia | Misma masa |
| 12 | Sangre a rendering **+** carga de esa sangre al efluente | La sangre recuperada no llega al efluente |
| 13 | Garras exportadas **+** patas a pet food o rendering | Misma masa (salvo descarte y cutícula, ya separados) |
| 14 | Masa biológica **+** agua retenida contadas como "carne" | El agua se vende pero no es carne (SUP-042) |
| 15 | Decomisos en D **+** decomisos en rendering | Uno u otro según normativa (T14) |

## 4. Valorización técnica vs económica

| Etapa | Pregunta | Resultado |
|---|---|---|
| 1. **Técnica** | ¿Existe un proceso capaz de transformar la salida en algo útil y permitido? | Rutas de §2 (este documento) |
| 2. **Normativa** | ¿Está permitido para ese uso y ese destino? | DPV-066, DPV-073, DPV-074 |
| 3. **Comercial** | ¿Hay un comprador identificado, con volumen, especificación y frecuencia compatibles? | Tareas de campo ([`conclusiones_valorizacion.md` §6](conclusiones_valorizacion.md)) |
| 4. **Económica** | ¿El net-back (precio − flete − frío − proceso − costo financiero − mermas) es positivo y mayor que el de la ruta alternativa? | Modelo económico (fase posterior; SUP-017) |

Solo una salida que supera las **cuatro** etapas se cuenta como ingreso. Hasta entonces, cada corriente C se trata en los escenarios como **costo de disposición a cotizar** (SUP-046, SUP-049). La fórmula de asignación por parte está en [`../17_exportacion/estrategia_valorizacion_ave.md` §1](../17_exportacion/estrategia_valorizacion_ave.md):

```
Ingreso total por ave = Σ_i  k_i × max_r ( NB_i,r )     con una sola ruta r por material i
NB_i,r puede ser negativo (costo de retiro o disposición)
```
