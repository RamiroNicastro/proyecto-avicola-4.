# Subproductos, coproductos de faena y residuos — masa

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Fase 0 (prefactibilidad)

> **Alcance.** Cuántos kg de patas/garras, plumas, sangre, cabezas, vísceras no comestibles, grasa, huesos y decomisos salen por ave y por escala, y qué destino conceptual pueden tener. **No** se asignan precios, **no** se asume un rendimiento de rendering sin fuente y **no** se diseña ningún equipo. Destino industrial detallado: [`07_subproductos`](../07_subproductos/README.md) y efluentes: [`11_agua_efluentes`](../11_agua_efluentes/README.md) (sesiones futuras).
> **Fuentes.** Extractos de buscador `[PVDP]`. Valores del modelo `[ESTIMACIÓN]`/`[SUPUESTO]` (SUP-036, SUP-040, SUP-041). Menudencias y cuello: [`balance_por_ave.md` §5](balance_por_ave.md).

---

## 1. Resumen por ave y por peso (escenario medio, condenas medias)

kg/ave. "Plumas crudas" incluye el agua de escaldado arrastrada (0,6 kg por kg de pluma biológica, SUP-040); todas las demás líneas son masa biológica.

| Salida | Clase | 2,2 kg | 2,5 kg | 2,8 kg | **2,9 kg** | 3,0 kg | 3,2 kg | 3,5 kg | % PV (2,9) |
|---|---|---|---|---|---|---|---|---|---|
| Sangre recuperada | C | 0,065 | 0,073 | 0,081 | **0,084** | 0,086 | 0,092 | 0,099 | 2,9 % |
| Sangre no recuperada | D | 0,011 | 0,013 | 0,014 | **0,015** | 0,015 | 0,016 | 0,018 | 0,5 % |
| Plumas (masa biológica) | C | 0,117 | 0,132 | 0,146 | **0,151** | 0,155 | 0,164 | 0,178 | 5,2 % |
| Plumas crudas húmedas (bio + agua) | C | 0,188 | 0,211 | 0,234 | **0,241** | 0,249 | 0,263 | 0,284 | 8,3 %* |
| Cabeza | C | 0,060 | 0,066 | 0,071 | **0,072** | 0,074 | 0,077 | 0,081 | 2,5 % |
| Garras grado A | B | 0,068 | 0,076 | 0,083 | **0,085** | 0,087 | 0,092 | 0,098 | 2,9 % |
| Garras de segunda | B | 0,013 | 0,014 | 0,016 | **0,016** | 0,016 | 0,017 | 0,018 | 0,6 % |
| Garras de descarte | C | 0,004 | 0,005 | 0,005 | **0,005** | 0,005 | 0,006 | 0,006 | 0,2 % |
| Cutícula de patas | D | 0,004 | 0,005 | 0,005 | **0,006** | 0,006 | 0,006 | 0,006 | 0,2 % |
| Tracto digestivo vacío | C | 0,070 | 0,077 | 0,085 | **0,087** | 0,089 | 0,094 | 0,100 | 3,0 % |
| Contenido gastrointestinal | D | 0,028 | 0,031 | 0,034 | **0,035** | 0,036 | 0,037 | 0,040 | 1,2 % |
| Pulmones | C | 0,014 | 0,015 | 0,017 | **0,017** | 0,018 | 0,019 | 0,020 | 0,6 % |
| Otros no comestibles | C | 0,021 | 0,024 | 0,025 | **0,026** | 0,027 | 0,028 | 0,029 | 0,9 % |

\* % sobre PV de una masa que incluye agua: solo como referencia de manejo.

Configuración C agrega, a 2,9 kg: **hueso 0,164**, **residuo óseo de CMS 0,153** (clase C) y **piel 0,110** (clase B; puede ir a rendering si no hay comprador). Decomisos (clase D): **0,040 kg/ave** en el escenario medio ([`agua_y_mermas.md` §6](agua_y_mermas.md)).

## 2. Patas y garras

### 2.1 Pata vs garra comercial

| Término | Qué es | En el modelo |
|---|---|---|
| **Pata** (cruda) | Pie + tarso (*shank*) cortado en la articulación tarsal, con cutícula amarilla, uñas y almohadilla | 3,9 % PV a 2,9 kg (0,113 kg/ave); fuentes: ~4 % (FTE-175), 5 % (FTE-163) |
| **Garra comercial** (*paw*) | Pata escaldada y **pelada** (sin cutícula externa), limpia, clasificada por grado; según el comprador puede cortarse más abajo (sin parte del tarso) o sin uñas | 95 % de la pata apta (se pierde 5 % de cutícula, `[SUPUESTO]` SUP-040) |
| Grado A | Piel blanca, sin huesos rotos, sin hematomas, sin almohadilla negra ni quemaduras de amoníaco, 35–50 g por pieza, 12–15 cm (especificaciones de ofertas comerciales, FTE-176, débil) | 80 % de las garras (escenario medio) |
| Segunda / grado B | Con lesiones leves; mercados menos exigentes | 15 % |
| Descarte | Lesiones graves, fracturas, contaminación: rendering | 5 % |

**Coherencia del modelo:** a 2,9 kg, 0,085 kg de garra grado A por ave = **~43 g por pieza**, dentro del rango comercial de 35–50 g. A 2,2 kg, ~34 g (límite inferior): **las aves livianas podrían no cumplir el calibre de algunos compradores** (a validar, DPV-064).

### 2.2 Proceso, calidad y descarte

- **Proceso:** corte de la pata (antes de la evisceración) → escaldado específico → pelado (remoción de la cutícula amarilla) → lavado → enfriado → clasificación por grado y calibre → empaque/congelado. La cutícula y el agua de escaldado van al efluente o a lodos.
- **El grado se decide en la granja:** la **pododermatitis** (lesiones plantares por cama húmeda, FTE-175 `[PVDP]`), los hematomas de captura y las quemaduras de amoníaco bajan el grado. Por eso el escenario de condenas "alto" baja el grado A a 60 % y sube el descarte a 15 % (SUP-041).

| Escenario de calidad (2,9 kg) | Garras grado A (kg/ave) | Segunda | Descarte |
|---|---|---|---|
| Bajo (pocos problemas) | 0,096 | 0,009 | 0,002 |
| **Medio** | **0,085** | **0,016** | **0,005** |
| Alto (muchos problemas) | 0,063 | 0,026 | 0,016 |

### 2.3 Potencial exportable (sin precio)

- Las garras son la parte con **mayor diferencia de valor por destino** de toda el ave, pero su mejor mercado (China) **no está disponible confirmado** (SUP-016, DPV-035). Sin China, su valor cae a destinos alternativos o a harina ([`17_exportacion/estrategia_valorizacion_ave.md` §4](../17_exportacion/estrategia_valorizacion_ave.md)). **No se asigna precio** (SUP-018).
- **Lote mínimo:** un contenedor reefer de 40' lleva ~24–27 t de congelado (`[PVDP · débil]`, `17_exportacion`). Días de faena necesarios para completar **25 t de garras grado A** (medio, con 250 días de faena/año):

| Peso vivo | Garras A (kg/ave) | 2.500 aves/día | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|---|
| 2,2 kg | 0,068 | 147 días | 73 | 37 | 18 |
| 2,9 kg | 0,085 | 118 días | 59 | 29 | 15 |
| 3,5 kg | 0,098 | 102 días | 51 | 26 | 13 |

A 2.500 aves/día se tardaría **~5–7 meses** de faena en llenar un contenedor: exportar garras exige escala, acumulación en cámara (capital de trabajo y frío) o consolidación con terceros. `[ESTIMACIÓN]`.

## 3. Plumas

| Concepto | Valor | Clasificación |
|---|---|---|
| Plumas, masa biológica | **5,2 % PV** a 2,9 kg (0,151 kg/ave); rango del modelo 5,1–5,4 % | `[ESTIMACIÓN]`; fuentes 5–7 % y 3–7 % (FTE-164, FTE-163) |
| Agua arrastrada del escaldado | 0,6 kg/kg de pluma → **pluma cruda húmeda ≈ 8,3 % PV** (0,241 kg/ave) | `[SUPUESTO]` SUP-040; coherente con "8 %" de un ejemplo de fabricante (FTE-182) y "9 %" de otra fuente |
| Humedad de la pluma hidrolizada | 45–65 % antes del secado | FTE-182 `[PVDP]` |
| Humedad de la harina de plumas | ~8–10 % | FTE-164, FTE-182 `[PVDP]` |
| Proteína | ~90 % de proteína bruta (queratina) en base seca | FTE-164 `[PVDP]` |
| Variación esperable | ±1 pp PV según peso, edad, sexo, época (muda), eficiencia del desplumado y del escurrido | `[ESTIMACIÓN]` |

**Pluma cruda ≠ harina de plumas.** La cantidad de harina depende de la **materia seca real de la pluma que entra al hidrolizador** (que varía con el escurrido, el prensado y el agua de transporte). **No se encontró una fuente confiable de rendimiento de rendering** (kg de harina por kg de pluma cruda) y **no se asume**. La relación a usar cuando haya datos es:

```
harina de plumas (kg) = pluma cruda (kg) × materia seca de la pluma cruda (fracción) / (1 − humedad final de la harina)
```

La materia seca de la pluma cruda se medirá en planta o se pedirá a plantas de rendering (DPV-065). A 10.000 aves/día de 2,9 kg salen **~1,5 t/día de pluma biológica, ~2,4 t/día de pluma húmeda** (~600 t/año): es la mayor corriente de subproducto en masa.

## 4. Sangre

| Concepto | Valor (2,9 kg, medio) | Clasificación |
|---|---|---|
| Volumen sanguíneo total del ave | 6–7,5 % PV (no toda sale) | FTE-166 `[PVDP]` |
| **Sangre drenada en el desangrado** | **3,4 % PV = 0,099 kg/ave** (fuentes 3,3–4,0 %; objetivo ~3 %, 45–50 % del volumen) | `[ESTIMACIÓN]` FTE-165, FTE-166 |
| **Sangre recuperable** (llega al tanque/canaleta de sangre) | **85 % → 0,084 kg/ave (2,9 % PV)** | `[SUPUESTO]` SUP-040 |
| Sangre no recuperada (goteo posterior, escaldado, lavados) | **15 % → 0,015 kg/ave (0,5 % PV)** → efluente | `[SUPUESTO]` |
| Sangre que queda en la carcasa | Incluida en la carcasa (no se separa) | — |

**Por qué importa:**

- **Efluentes (DBO/DQO):** la sangre es la corriente más contaminante de la faena: se reporta **~375.000 mg/L de DQO** (FTE-181 `[PVDP]`), cientos de veces la carga de un efluente de faena típico (DQO ~3.000–8.000 mg/L en los estudios leídos). Orden de magnitud `[ESTIMACIÓN]` (densidad ~1,05 kg/L): ~0,36 kg de DQO por kg de sangre. A 10.000 aves/día: la sangre no recuperada (~150 kg/día) aporta **~50 kg de DQO/día**; si toda la sangre fuera al desagüe (~990 kg/día) serían **~350 kg de DQO/día**. **Recuperar la sangre por separado es la primera medida de tratamiento de efluentes.** (Un extracto indicaba "DBO de la sangre ~100 mg/L": es incoherente y se descarta.)
- **Rendering:** la sangre recuperada puede secarse (harina de sangre) o co-procesarse; aporta proteína pero requiere coagulación y mucho secado (alto contenido de agua). Rendimiento de secado: no asumido (DPV-065).
- **Higiene y calidad:** un sangrado incompleto deja sangre en la carcasa (defectos de color, hematomas aparentes, menor vida útil) y aumenta degradaciones.
- **Bienestar y Halal:** el método de sangrado está ligado a los requisitos de aturdimiento y de sacrificio (DPV-034).

## 5. Vísceras no comestibles

| Componente | % PV (2,9 kg) | kg/ave | Destino posible | Clase |
|---|---|---|---|---|
| Tracto digestivo vacío (proventrículo, intestinos, ciegos, cloaca) | 3,0 % | 0,087 | Rendering (harina de vísceras) si está habilitado; si no, residuo | C |
| **Contenido gastrointestinal** | 1,2 % | 0,035 | Residuo / efluente; en la práctica suele viajar **dentro** del intestino hacia el rendering | D |
| Pulmones | 0,6 % | 0,017 | Rendering | C |
| Órganos no comerciales y tejidos (tráquea, esófago y buche, bazo, vesícula, gónadas, cutícula y contenido de molleja) | 0,9 % | 0,026 | Rendering | C |
| **Total** | **5,7 %** | **0,165** | | |

- **Separación conceptual:** el modelo separa el contenido digestivo (D) del tracto (C) porque no tiene valor proteico y agrega humedad y cenizas a la harina. **Físicamente** el paquete de vísceras suele ir entero (con contenido) al rendering o al residuo; en un balance medido se pesará junto.
- **Ayuno:** el contenido depende del ayuno (un ayuno de ~12 h reduce el contenido ~75 %, FTE-177 `[PVDP]`). Ayuno corto = más contenido, más contaminación fecal y más decomisos (escenario de rendimiento "bajo": 2,0 % PV).
- **Qué puede ir a rendering, a residuo o a otros procesos permitidos** (compostaje, biodigestión, alimento para mascotas): depende de la habilitación SENASA y ambiental; **no se afirma ninguna vía** hasta revisar la normativa (DPV-066). Un documento del INTA sobre compostaje de restos de faena de pollos fue identificado pero no leído.
- Fuentes: "vísceras no comestibles ~9 % PV" (FTE-163) es mayor que el 5,7 % del modelo porque probablemente incluye molleja sin limpiar u otras partes; ver [`balance_por_ave.md` §11](balance_por_ave.md).

## 6. Cabezas, grasa, huesos y decomisos

| Salida | kg/ave (2,9 kg) | Clase | Nota |
|---|---|---|---|
| Cabeza | 0,072 (2,5 % PV) | C | Rendering. Fuente: 3 % (FTE-163, débil) |
| Grasa abdominal | 0,052 (1,8 % PV) **dentro** de la carcasa | — / C si se retira | El modelo **no** la retira (SUP-043); si se retira, sale como "grasa abdominal retirada" (C) y reduce la carcasa |
| Hueso de deshuese (config. C) | 0,164 | C | Rendering (harina de carne y hueso) o caldos |
| Residuo óseo de CMS (config. C) | 0,153 | C | Rendering |
| Decomisos (medio) | 0,040 (1,4 % PV) | D | Destino según normativa (DPV-066) |

## 7. Escalado de subproductos y residuos (2,9 kg, configuración B, medio)

| Salida | Clase | kg/ave | t/día a 10.000 aves/día | t/año a 10.000 aves/día (250 d) | t/año con 1.000.000 aves/año |
|---|---|---|---|---|---|
| Plumas crudas húmedas | C | 0,241 | 2,41 | 603 | 241 |
| Tracto digestivo | C | 0,087 | 0,87 | 217 | 87 |
| Sangre recuperada | C | 0,084 | 0,84 | 210 | 84 |
| Cabezas | C | 0,072 | 0,72 | 181 | 72 |
| Otros no comestibles + pulmones | C | 0,044 | 0,44 | 109 | 44 |
| Garras de descarte | C | 0,005 | 0,05 | 13 | 5 |
| **Total subproductos C** | | **0,533** | **5,33** | **1.334** | **533** |
| Contenido gastrointestinal | D | 0,035 | 0,35 | 87 | 35 |
| Sangre no recuperada | D | 0,015 | 0,15 | 37 | 15 |
| Decomisos (total + parcial) | D | 0,040 | 0,40 | 100 | 40 |
| Cutícula de patas | D | 0,006 | 0,06 | 14 | 6 |
| Agua de goteo | D | 0,037 | 0,37 | 92 | 37 |
| **Total residuos D** | | **0,132** | **1,32** | **330** | **132** |
| Garras grado A + segunda (coproducto) | B | 0,101 | 1,01 | 253 | 101 |

Con configuración C se agregan **~3,3 t/día** de hueso y residuo de CMS a 10.000 aves/día (≈ 830 t/año). Materia prima potencial de rendering (C + decomisos + contenido): **~0,6 kg/ave en B y ~0,9 kg/ave en C**, ≈ 20–30 % del peso vivo. **Esa masa tiene valor solo si existe una salida** (rendering propio, tercerizado u otra vía permitida); si no, es un costo de disposición (DEC-027).

## 8. Qué no se asume

- Rendimiento de harina de plumas, de vísceras o de sangre por kg de materia prima (DPV-065).
- Precio de ninguna harina ni de las garras (SUP-018).
- Que el rendering deba ser propio (DEC-027; evaluar hacer / comprar / tercerizar, regla 10).
- Que un decomiso pueda ir a rendering (DPV-066).
