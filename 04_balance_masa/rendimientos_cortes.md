# Rendimientos de trozado y deshuese

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance.** Cómo se reparte la carcasa en cortes (trozado) y cada corte en carne, piel, hueso y recortes (deshuese), para 6 pesos vivos, y cómo cambia el balance entre pollo entero, trozado y deshuesado. **No** se eligen productos ni se asignan precios.
> **Fuentes.** Extractos de buscador `[PVDP]` (acceso directo bloqueado, 2026-09-30). Los valores del modelo son `[ESTIMACIÓN]`/`[SUPUESTO]` (SUP-038, SUP-039). Definiciones de carcasa y peso vivo en [`balance_por_ave.md` §2](balance_por_ave.md).
> Todas las cifras de este documento salen de [`modelo_balance_masa.py`](modelo_balance_masa.py) (escenario medio, condenas medias, chiller por inmersión; kg de **masa biológica**, sin el agua retenida).

---

## 1. Rendimiento sobre peso vivo vs sobre carcasa — no sumarlos

| Base | Qué es | Ejemplo, pollo de 2,9 kg |
|---|---|---|
| **% PV** (sobre peso vivo en planta) | kg del corte / kg del ave viva | Pechuga con hueso = 0,784 kg / 2,900 kg = **27,0 % PV** |
| **% carcasa** (sobre la carcasa eviscerada, D5) | kg del corte / kg de carcasa | 0,784 / 2,073 = **37,8 % de la carcasa** |
| % carcasa apta (después de decomisos) | kg del corte / kg de carcasa que llega al trozado | 0,784 / 2,036 = **38,5 %** (parámetro del modelo) |

- **Conversión:** % PV = % carcasa × rendimiento eviscerado (0,378 × 0,715 = 0,270).
- **Errores típicos:** (a) sumar un % de carcasa con un % de PV (p. ej. "pechuga 38 % + garras 4 %" no es 42 % de nada); (b) aplicar un % de carcasa de una fuente al peso vivo (sobrestima el corte ~40 %); (c) comparar un % de carcasa de una fuente cuya carcasa incluye cuello y menudencias con otra que no.
- El CSV trae ambas columnas: `pct_peso_vivo_bio` y `pct_carcasa_bio` (esta última solo para salidas que derivan de la carcasa; base = carcasa eviscerada total antes de decomisos).

## 2. Trozado: participación de cada corte en la carcasa

### 2.1 Valores del modelo (a 2,9 kg, sobre la carcasa apta) y referencias

| Corte | Definición en el modelo | Modelo medio | Pendiente | Escenarios bajo / alto | Referencias `[PVDP]` |
|---|---|---|---|---|---|
| **Pechuga con hueso** | Pechuga entera con piel, esternón y costillar anterior | **38,5 %** | +1,2 pp/kg | 37,5 / 39,5 | 40 % del RTC (con porción de espinazo, FTE-179); filet Cobb 22,6 % PV (FTE-140) implica pechuga c/h ~38–40 % de la carcasa |
| **Pata-muslo** | Cuarto trasero (muslo + pata) **sin** porción de espinazo | **31,0 %** | −0,4 pp/kg | igual | Muslo 32 % + pata 16 % del RTC (con espinazo, FTE-179); pierna entera Cobb ~23 % PV (FTE-161) |
| **Alas** | Ala entera, 3 segmentos | **10,2 %** | −0,5 pp/kg | igual | 12 % del RTC (FTE-179); 12,4–14,2 % en estudios antiguos; Cobb ~7,6 % PV (FTE-161) ≈ 10,2 % de la carcasa |
| **Carcasa-esqueleto** | Espinazo, rabadilla, costillar remanente, grasa abdominal | **19,3 %** | −0,3 pp/kg | 20,3 / 18,3 | Espinazo 14,2–18,3 % en estudios antiguos (FTE-179) |
| Recortes de trozado | Carne y piel recortadas | 0,5 % | 0 | igual | `[SUPUESTO]` |
| Merma de trozado | Aserrín de hueso, exudado | 0,5 % | 0 | igual | `[SUPUESTO]` |
| **Total** | | **100 %** | 0 | 100 % | Test T05 |

- **Pata-muslo = muslo 58 % + pata (*drumstick*) 42 %** (SUP-038; Cobb ~13,7 % y ~9,4 % PV, FTE-161).
- **Contradicción de definiciones:** la referencia "pechuga 40 %, ala 12 %, muslo 32 %, pata 16 % del RTC" suma 100 % **sin espinazo**, porque el espinazo se reparte entre muslo y pechuga en ese corte. En Argentina, "pata-muslo" puede venderse con o sin porción de espinazo y la "pechuga" con o sin alas: **la especificación comercial cambia el rendimiento del corte varios puntos** (DPV-068).

### 2.2 Cortes por peso vivo (configuración B, escenario medio)

kg/ave · % de la carcasa eviscerada total (D5) · % PV.

| Corte | 2,2 kg | 2,5 kg | 2,8 kg | **2,9 kg** | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| Carcasa eviscerada (D5) | 1,544 | 1,768 | 1,997 | **2,073** | 2,151 | 2,306 | 2,542 |
| Carcasa apta (después de decomisos medios) | 1,516 | 1,737 | 1,961 | **2,036** | 2,112 | 2,265 | 2,497 |
| **Pechuga con hueso** | 0,571 · 37,0 % · 26,0 % | 0,660 · 37,3 % · 26,4 % | 0,753 · 37,7 % · 26,9 % | **0,784 · 37,8 % · 27,0 %** | 0,816 · 37,9 % · 27,2 % | 0,880 · 38,2 % · 27,5 % | 0,979 · 38,5 % · 28,0 % |
| **Pata-muslo** | 0,474 · 30,7 % · 21,6 % | 0,541 · 30,6 % · 21,6 % | 0,609 · 30,5 % · 21,7 % | **0,631 · 30,4 % · 21,8 %** | 0,654 · 30,4 % · 21,8 % | 0,699 · 30,3 % · 21,9 % | 0,768 · 30,2 % · 21,9 % |
| de la cual muslo | 0,275 | 0,314 | 0,353 | **0,366** | 0,379 | 0,406 | 0,445 |
| de la cual pata | 0,199 | 0,227 | 0,256 | **0,265** | 0,275 | 0,294 | 0,323 |
| **Alas** | 0,160 · 10,4 % · 7,3 % | 0,181 · 10,2 % · 7,2 % | 0,201 · 10,1 % · 7,2 % | **0,208 · 10,0 % · 7,2 %** | 0,214 · 10,0 % · 7,1 % | 0,228 · 9,9 % · 7,1 % | 0,247 · 9,7 % · 7,1 % |
| **Carcasa-esqueleto** | 0,296 · 19,2 % · 13,4 % | 0,337 · 19,1 % · 13,5 % | 0,379 · 19,0 % · 13,5 % | **0,393 · 19,0 % · 13,6 %** | 0,407 · 18,9 % · 13,6 % | 0,435 · 18,9 % · 13,6 % | 0,477 · 18,8 % · 13,6 % |
| Recortes | 0,008 | 0,009 | 0,010 | **0,010** | 0,011 | 0,011 | 0,012 |
| Merma de trozado | 0,008 | 0,009 | 0,010 | **0,010** | 0,011 | 0,011 | 0,012 |

Cuello, menudencias y garras **no** forman parte de la carcasa ni de los cortes (se separan antes; test T10). La suma de cortes = carcasa apta, nunca mayor que la carcasa (test T05).

## 3. Deshuese

### 3.1 Fracciones del corte de origen (cada fila suma 100 %)

| Corte de origen | Carne | Piel | Hueso | Recortes | Merma | Referencias `[PVDP]` y clasificación |
|---|---|---|---|---|---|---|
| **Pechuga con hueso** | **76,0 %** (suprema 61,0 % + solomillo 15,0 %) | 8,0 % | 13,0 % | 2,0 % | 1,0 % | `[SUPUESTO]` calibrado para que el filet total (suprema + solomillo) dé ~20,5 % PV a 2,9 kg, por debajo del objetivo Cobb (22,6 % a 2,8 kg, FTE-140) |
| **Muslo** | **66,0 %** | 13,0 % | 17,0 % | 3,0 % | 1,0 % | `[SUPUESTO]`; piel y grasa 8–20 % de la carcasa según peso (FTE-179) |
| **Pata** (*drumstick*) — solo si se deshuesa | **56,0 %** | 11,0 % | 30,0 % | 2,0 % | 1,0 % | Carne de pata 53,5–53,8 % (FTE-179); en el modelo base la pata se vende **con hueso** (SUP-043) |
| **Carcasa-esqueleto → CMS** | **CMS 60 %** (bajo 55 / alto 65) | — | Residuo óseo 39 % | — | 1,0 % | 60–75 % en cuellos y espinazos con separadoras tipo tornillo (FTE-180, débil) |
| Alas | No se deshuesan (venta entera) | | | | | |

- **Suprema** = filet de pechuga sin solomillo; **solomillo** (*tender*, "sassami") = músculo pectoral menor. Si el mercado vende "suprema" con solomillo, sumar ambas líneas (no contar dos veces).
- **Muslo deshuesado** = sin piel en el modelo; si se vende con piel (especificación japonesa habitual), sumar la línea "piel (muslo)" (DPV-068).
- Después del deshuese manual puede quedar 10–15 % de tejido comestible en los huesos (FTE-180): es lo que recupera la CMS; si no hay separadora, ese tejido va con el hueso a rendering.
- La **eficiencia de deshuese** (manual vs automático, habilidad del operario) no está modelada como escenario: se mantiene fija (DPV-069).

### 3.2 Deshuese por peso vivo (configuración C, escenario medio)

kg/ave · % PV.

| Salida | 2,2 kg | 2,5 kg | 2,8 kg | **2,9 kg** | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| **Suprema** | 0,348 · 15,8 % | 0,403 · 16,1 % | 0,459 · 16,4 % | **0,478 · 16,5 %** | 0,498 · 16,6 % | 0,537 · 16,8 % | 0,597 · 17,1 % |
| **Solomillo** | 0,086 · 3,9 % | 0,099 · 4,0 % | 0,113 · 4,0 % | **0,118 · 4,1 %** | 0,122 · 4,1 % | 0,132 · 4,1 % | 0,147 · 4,2 % |
| *Filet total (suprema + solomillo)* | *0,434 · 19,7 %* | *0,502 · 20,1 %* | *0,572 · 20,4 %* | ***0,596 · 20,5 %*** | *0,620 · 20,7 %* | *0,669 · 20,9 %* | *0,744 · 21,3 %* |
| **Muslo deshuesado** (sin piel) | 0,182 · 8,3 % | 0,207 · 8,3 % | 0,233 · 8,3 % | **0,242 · 8,3 %** | 0,250 · 8,3 % | 0,268 · 8,4 % | 0,294 · 8,4 % |
| Pata con hueso | 0,199 · 9,1 % | 0,227 · 9,1 % | 0,256 · 9,1 % | **0,265 · 9,1 %** | 0,275 · 9,2 % | 0,294 · 9,2 % | 0,323 · 9,2 % |
| Alas | 0,160 · 7,3 % | 0,181 · 7,2 % | 0,201 · 7,2 % | **0,208 · 7,2 %** | 0,214 · 7,1 % | 0,228 · 7,1 % | 0,247 · 7,1 % |
| Piel (pechuga + muslo) | 0,081 · 3,7 % | 0,094 · 3,7 % | 0,106 · 3,8 % | **0,110 · 3,8 %** | 0,115 · 3,8 % | 0,123 · 3,8 % | 0,136 · 3,9 % |
| Hueso (pechuga + muslo) | 0,121 · 5,5 % | 0,139 · 5,6 % | 0,158 · 5,6 % | **0,164 · 5,7 %** | 0,171 · 5,7 % | 0,183 · 5,7 % | 0,203 · 5,8 % |
| Recortes (trozado + deshuese) | 0,027 · 1,2 % | 0,031 · 1,3 % | 0,035 · 1,3 % | **0,037 · 1,3 %** | 0,038 · 1,3 % | 0,041 · 1,3 % | 0,045 · 1,3 % |
| CMS | 0,177 · 8,1 % | 0,202 · 8,1 % | 0,227 · 8,1 % | **0,236 · 8,1 %** | 0,244 · 8,1 % | 0,261 · 8,2 % | 0,286 · 8,2 % |
| Residuo óseo de CMS | 0,115 · 5,2 % | 0,132 · 5,3 % | 0,148 · 5,3 % | **0,153 · 5,3 %** | 0,159 · 5,3 % | 0,170 · 5,3 % | 0,186 · 5,3 % |
| Mermas (trozado + deshuese + CMS) | 0,019 | 0,022 | 0,025 | **0,026** | 0,027 | 0,029 | 0,031 |

**Carne recuperable** por ave de 2,9 kg (masa biológica): filet 0,596 + muslo 0,242 + CMS 0,236 + recortes 0,037 = **1,11 kg** (38 % del PV) más la carne de pata (vendida con hueso, ~0,15 kg si se deshuesara) y de alas.

## 4. Pollo entero vs trozado vs deshuesado — balance detallado (2,9 kg, medio)

kg/ave de masa biológica (entre paréntesis, agua retenida por inmersión). Faena primaria idéntica en las tres: sangre, plumas, cabeza, vísceras, menudencias, cuello y garras no cambian.

| Salida | Clase | A. Entero | B. Trozado | C. Deshuesado |
|---|---|---|---|---|
| Pollo entero | A | 1,914 (+0,080) | — | — |
| Pechuga con hueso | A | 0,047* | 0,784 (+0,033) | — |
| Pata-muslo | A | 0,038* | 0,631 (+0,027) | — |
| Suprema + solomillo | A | — | — | 0,596 (+0,025) |
| Muslo deshuesado | A | — | — | 0,242 (+0,010) |
| Pata con hueso | A | — | — | 0,265 (+0,011) |
| Alas | B | 0,012* | 0,208 (+0,009) | 0,208 (+0,009) |
| Carcasa-esqueleto | B | 0,024* | 0,393 (+0,017) | — (va a CMS) |
| CMS | B | — | — | 0,236 (+0,010) |
| Piel | B | — | — | 0,110 (+0,005) |
| Recortes | B | 0,001 | 0,010 | 0,037 (+0,002) |
| Menudencias + cuello | B | 0,184 | 0,184 | 0,184 |
| Garras (grado A + segunda) | B | 0,101 | 0,101 | 0,101 |
| **Hueso + residuo óseo de CMS** | C | 0 | 0 | **0,317** (+0,014) |
| Subproductos de faena | C | 0,443 (+0,090) | 0,443 (+0,090) | 0,443 (+0,090) |
| Residuos D | D | 0,095 (+0,037) | 0,095 (+0,037) | 0,095 (+0,037) |
| Mermas y pérdidas | P | 0,041 | 0,051 | 0,066 |
| **Total** | | **2,900 (+0,213)** | **2,900 (+0,213)** | **2,900 (+0,213)** |
| Productos principales (A) | | 1,999 | 1,415 | 1,103 |
| Comestible total (A + B) | | 2,320 | 2,311 | 1,978 |

\* En A, el 6 % de las canales no apto para venta entera (hematomas, alas rotas; escenario medio) se trocea: el "pollo entero" no puede ser el 100 % de la producción ([`agua_y_mermas.md` §6](agua_y_mermas.md)).

**Qué cambia al pasar de A → B → C:**

- **kg de productos principales:** 1,999 → 1,415 → 1,103 kg/ave.
- **kg de partes secundarias** (alas, carcasa, menudencias, garras, CMS): 0,32 → 0,89 → 0,73 kg/ave.
- **kg de hueso separado:** 0 → 0 → 0,317 kg/ave (en A y B el hueso se vende dentro del producto).
- **kg de piel separada:** 0 → 0 → 0,110 kg/ave.
- **kg de recortes:** 0,001 → 0,010 → 0,037 kg/ave.
- **kg de subproductos (C):** 0,443 → 0,443 → 0,760 kg/ave.
- **Principio (SUP-013):** los cortes son **productos conjuntos**; no se puede vender más pechuga sin producir la pata-muslo, las alas y la carcasa correspondientes. Pasar a C aumenta el valor potencial por kg de las partes principales pero multiplica las partes a colocar (piel, CMS, recortes, hueso): **cada una necesita un comprador o termina en rendering** (DEC-005).

## 5. Impacto del peso de faena sobre el mix

### 5.1 ¿Las partes crecen proporcionalmente?

**No.** La literatura de alometría indica que la pechuga crece más rápido que el resto del cuerpo en los híbridos modernos, y que cabeza, patas y órganos pierden participación (FTE-183 `[PVDP]`: rendimiento de pectoral mayor +79–85 % entre 1957 y 2005, relación alométrica simple entre pechuga y peso corporal). El modelo lo representa con fracciones que cambian con el peso (pendientes `[SUPUESTO]` en magnitud, SUP-036/038).

| Parte (config. B/C, medio) | kg a 2,2 kg | kg a 3,5 kg | Crece × (3,5 / 2,2) | vs PV (× 1,59) |
|---|---|---|---|---|
| Pechuga con hueso | 0,571 | 0,979 | **1,72** | Más que proporcional |
| Filet (suprema + solomillo) | 0,434 | 0,744 | **1,72** | Más que proporcional |
| Pata-muslo | 0,474 | 0,768 | 1,62 | ≈ proporcional |
| Carcasa-esqueleto | 0,296 | 0,477 | 1,61 | ≈ proporcional |
| Alas | 0,160 | 0,247 | 1,55 | Menos |
| Cuello | 0,058 | 0,088 | 1,51 | Menos |
| Plumas | 0,117 | 0,178 | 1,51 | Menos |
| Hígado | 0,044 | 0,063 | 1,44 | Menos |
| Garras grado A | 0,068 | 0,098 | 1,44 | Menos |
| Tracto digestivo | 0,070 | 0,100 | 1,43 | Menos |
| Cabeza | 0,060 | 0,081 | 1,36 | Menos |
| Molleja | 0,034 | 0,044 | 1,32 | Menos |

### 5.2 Aves necesarias por tonelada de producto

| Producto (medio) | 2,2 kg | 2,5 kg | 2,8 kg | 2,9 kg | 3,0 kg | 3,2 kg | 3,5 kg |
|---|---|---|---|---|---|---|---|
| Aves por t de filet (suprema + solomillo) | 2.305 | 1.993 | 1.748 | 1.678 | 1.613 | 1.495 | 1.344 |
| Aves por t de pechuga con hueso | 1.751 | 1.515 | 1.328 | 1.276 | 1.225 | 1.136 | 1.021 |

Para la misma tonelada de filet, un ave de 2,2 kg exige **72 % más aves** que una de 3,5 kg; pero genera también más garras, cabezas y menudencias por kg de filet y aves de menor edad (menos alimento por ave; ver `03_produccion_primaria`). **No se concluye qué peso conviene** (DEC-021): depende del mix de demanda, de precios por parte y del costo de crianza.

### 5.3 Advertencias

- Las pendientes son **supuestos de magnitud**: la dirección está respaldada, la cifra no. Obtener las tablas de rendimiento por peso de Cobb y Ross (DPV-059) y medir en planta (DPV-060).
- El modelo no se extrapola fuera de 2,0–3,8 kg (test T12).
- Machos y hembras tienen rendimientos distintos (las hembras más pechuga relativa, los machos más pierna según las tablas genéticas `[PVDP]`); el modelo usa lotes mixtos (*as hatched*).
- Aves pesadas tienen más riesgo de miopatías de pechuga (*white striping*, *wooden breast*; FTE-179/FTE-183 `[PVDP]`) que no cambian la masa pero sí el grado comercial: a validar.

## 6. Datos débiles de este documento

| Dato | Debilidad | Registro |
|---|---|---|
| Participación de cortes en la carcasa | Solo referencias extranjeras con definiciones distintas; ninguna medición argentina | DPV-060, DPV-068 |
| Fracciones de deshuese (carne/piel/hueso) | Mayormente supuestas; solo la pata tiene un rango leído | DPV-069 |
| Rendimiento de CMS | Fuente débil (divulgación) y dependiente de la máquina | DPV-069 |
| Pendientes con el peso | Magnitud supuesta | DPV-059 |
| Filet: 20,5 % PV (modelo) vs 22,6 % o ~26 % (extractos Cobb) | Contradicción entre extractos; el modelo queda por debajo del objetivo genético | DPV-059 |
