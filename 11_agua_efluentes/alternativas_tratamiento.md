# Alternativas de tratamiento de efluentes y manejo de lodos (conceptual)

**Fecha:** 2026-09-30 · **Versión:** 1.1 (auditoría conceptual, sesión 09C) · Fase 0

> **Alcance:** comparación **conceptual** de pretratamientos, tratamientos biológicos y manejo de lodos. **No se elige tecnología**, no se dimensionan unidades, no se selecciona proveedor ni se calcula CAPEX/OPEX. Las eficiencias citadas son `[PVDP]` (FTE-256, FTE-263, FTE-264). Cargas por escala: [`caracterizacion_efluentes.md` §4](caracterizacion_efluentes.md).

---

## 1. Secuencia típica (a validar)

```
PREVENCIÓN EN ORIGEN     recuperar sangre · transporte en seco de plumas y vísceras · limpieza en seco previa
        ↓
PRETRATAMIENTO           rejas / tamices → separación de sólidos → trampa/recuperación de grasas → ecualización
                         (+ ajuste de pH) → DAF (flotación por aire disuelto, con o sin químicos)
        ↓
TRATAMIENTO BIOLÓGICO    anaerobio (lagunas cubiertas / reactores)  y/o  aerobio (lodos activados, SBR, lagunas aireadas)
        ↓                (a menudo combinados: anaerobio para la carga, aerobio para pulir y nitrificar)
PULIDO / DESINFECCIÓN    según cuerpo receptor y límites (nitrógeno, fósforo, coliformes)
        ↓
VUELCO                   colectora cloacal · conducto pluvial · curso de agua · suelo (según permiso)
LODOS Y FLOTADOS  →      espesado → deshidratación → rendering / compost / biodigestión / disposición
```

La primera "etapa de tratamiento" es **no ensuciar el agua**: cada kg de sangre, grasa o víscera retirado en seco es carga que no hay que tratar ([`caracterizacion_efluentes.md` §5](caracterizacion_efluentes.md)).

## 2. Pretratamiento

| Unidad | Qué hace | Qué remueve (orden de magnitud) | Relevancia para faena avícola | Condicionantes |
|---|---|---|---|---|
| **Rejas y tamices** (estáticos, rotativos) | Retienen sólidos gruesos y finos (plumas, recortes, vísceras) | Sólidos gruesos; parte de la DQO particulada | Imprescindible; cuanto antes se tamiza, menos se disuelve | Retirar el tamizado diariamente (va a rendering o disposición) |
| **Separación de sólidos** (sedimentador, hidrociclón) | Separa arena y sólidos sedimentables | SST sedimentables | Útil si hay transporte hidráulico o lavado de camiones | Genera lodo primario |
| **Recuperación de grasas** (trampa, desnatador) | Separa grasa libre flotante | Grasas libres | Protege cañerías y el biológico; la grasa puede ir a rendering | Mantenimiento frecuente; olor |
| **Ecualización** (tanque homogeneizador) | Amortigua picos de caudal, carga, pH y temperatura (vaciado del escaldador, limpieza con químicos) | Nada por sí sola: **estabiliza** | Muy relevante: la planta descarga en ~12 h y con pulsos; el biológico prefiere caudal y carga constantes | Volumen ≈ fracción del caudal diario (no se dimensiona); aireación/mezcla para evitar olores |
| **DAF** (flotación por aire disuelto, a menudo con coagulante/floculante) | Burbujas finas flotan grasas y sólidos finos | DBO 30–90 %, DQO 70–80 %, SST 38–70 %, grasas 63–95 % (FTE-256 `[PVDP]`) | Estándar en plantas cárnicas; reduce mucho la carga al biológico | Genera **flotado** (lodo) con 10–15 % de sólidos (FTE-264); consumo de químicos y energía; la **DQO soluble** (sangre) no se remueve |
| Otros: coagulación química, electrocoagulación, membranas (UF/ósmosis) | Remoción avanzada / reúso | Alta | Aparecen en revisiones recientes (FTE-256); membranas orientadas a **reúso** | Costo, ensuciamiento; no se evalúan en esta fase |

## 3. Tratamiento biológico — comparación conceptual

| Criterio | **Lagunas anaerobias** (abiertas o cubiertas) | **Reactores anaerobios** (UASB, EGSB, filtros) | **Lagunas aireadas / facultativas** | **Lodos activados / SBR** (reactores aerobios) | **Combinación anaerobio + aerobio** |
|---|---|---|---|---|---|
| Terreno | **Muy alto** (grandes superficies) | Bajo | Alto | Bajo–medio | Medio |
| Carga que tolera | Alta; robustas a variaciones | Alta (hasta 7–11 kg DQO/m³·día a 20–30 °C en ensayos, FTE-263); sensibles a grasas y SST (necesitan buen DAF) | Media | Media; sensibles a picos (necesitan ecualización) | Alta |
| Calidad de salida | Insuficiente sola para vuelco estricto | Remoción parcial (55 % DQO total en un ensayo con efluente sin sedimentar); necesita postratamiento | Media | Alta; puede nitrificar/desnitrificar | Alta |
| Nitrógeno | No lo remueve (lo convierte en amonio) | No lo remueve | Parcial | **Sí** (con diseño específico) | Sí (etapa aerobia) |
| Olor | **Alto** si son abiertas (sulfhídrico); cubiertas lo controlan | Bajo (cerrado) | Medio | Bajo | Bajo–medio |
| Energía | Muy baja; **genera biogás** (cubiertas) | Baja; **genera biogás** | Media (aireación) | **Alta** (aireación: 0,7–2 kWh/kg DBO removida en el modelo, `[SUPUESTO]`) | Menor que aerobio solo |
| Lodos | Muy pocos; acumulación y retiro periódico | Pocos | Medios | **Muchos** (0,3–0,5 kg MS/kg DBO, `[SUPUESTO]`) | Menos que aerobio solo |
| Operación | Simple; arranque lento; estacional (temperatura) | Técnica; arranque de semanas a meses | Simple–media | **Técnica** (operador calificado, laboratorio) | Técnica |
| Emisiones | CH₄, CO₂, N₂O si abiertas (FTE-263) | Biogás captado | CO₂ | CO₂, lodos | Biogás captado |
| Escalabilidad por módulos | Por celdas (requiere terreno reservado) | Por reactores | Por celdas | Por trenes | Por trenes |

**Cómo se relaciona la elección con el proyecto** (no se decide aquí; DEC propuesta):

| Factor | Cómo empuja la elección |
|---|---|
| **Terreno** | Mucho terreno barato y alejado → lagunas posibles; terreno escaso o periurbano → reactores compactos |
| **Carga** (escala × gestión) | A 2.500–5.000 aves/día (del orden de 60–1.750 kg DQO/día según método y nivel; ver [`caracterizacion_efluentes.md` §4](caracterizacion_efluentes.md)) conviene la simplicidad; a 10.000–20.000 (240–7.000 kg DQO/día) la recuperación de biogás y la compacidad pesan más |
| **Normativa** | Vuelco a cloaca (prestador fija límites y tarifa por carga) vs pluvial/curso (ejemplo de referencia: 50 mg/L DBO y 250 mg/L DQO a conducto pluvial en PBA, Res. ADA 336/03 `[PVDP]`; el límite real lo fijará el sitio) vs suelo (restringido; inyección prohibida en PBA) → define el grado de tratamiento y si hace falta remover N y P |
| **Olor y vecindad** | Lagunas abiertas y acopio de lodos cerca de poblaciones son un riesgo de conflicto y de habilitación ([`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md) §10) |
| **Energía** | Red débil (zona rural) → penaliza aeración intensiva; biogás puede cubrir parte del calor (caldera) |
| **Operación** | Personal técnico disponible en la zona; laboratorio; turnos (el biológico funciona 365 días aunque la planta faene 250) |
| **Expansión** | Reservar terreno y trazas para duplicar el tratamiento cuando crezca la escala (principio de [`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md): sobredimensionar lo barato de prever) |
| **Exportación** | Auditorías de importadores revisan gestión ambiental y de subproductos; no fija tecnología pero sí registros y cumplimiento |

**Vuelco a colectora cloacal:** si el sitio tiene cloaca con capacidad, el prestador puede aceptar un efluente pretratado (tamiz + grasas + DAF) con límites y canon; el biológico lo haría la planta municipal. Depende 100 % del sitio: **no se supone**.

## 4. Lodos — PENDIENTE DE DIMENSIONAMIENTO

La v1.0 daba "~2,4 t/día de lodo deshidratado" a 10.000 aves/día. **Se retira como salida física**: la generación de lodos depende de los SST que entran, de lo separado mecánicamente, de la eficiencia del DAF, de la dosificación química, de la biomasa generada (tecnología biológica y purga), de la concentración de sólidos y de la deshidratación, y **ninguno de esos parámetros existe todavía para nuestra planta**. En el modelo, **LODO = PENDIENTE DE DIMENSIONAMIENTO** por defecto (test **U23**; mutaciones M13 y M14).

### 4.1 Cadena explícita que exige el modelo

```
kg SST removidos/día        = SST del efluente (método A o B, NO subproductos del balance) × remoción mecánica + DAF
+ kg grasas flotadas/día    = grasas y aceites × remoción del DAF
+ kg sólidos químicos/día   = m³ de efluente × dosis de coagulante/floculante (g/m³) ÷ 1.000
+ kg biomasa/día            = DBO que llega al biológico × remoción × rendimiento de biomasa (depende de la tecnología)
= kg SÓLIDOS SECOS/día
÷ fracción de sólidos de la torta (tras deshidratación)
= t de LODO HÚMEDO/día
```

Si falta cualquier eslabón, el sólido seco queda vacío; si falta el % de sólidos de torta, el lodo húmedo queda vacío.

### 4.2 Escenario ilustrativo (cada supuesto visible y editable)

Solo para mostrar el orden de magnitud y qué parámetros mandan (bloque `lodos_ilustrativo` del CSV; `--lodos-ilustrativo` en la línea de comandos). 10.000 aves/día, método A, nivel medio:

| Eslabón | Parámetro (bajo · **medio** · alto) | Origen | kg/día (medio) |
|---|---|---|---|
| SST removidos | remoción 70 · **54** · 38 % de 350 kg SST | FUENTE `[PVDP]` (DAF 38–70 %, FTE-256) | 189 |
| Grasas flotadas | remoción 95 · **80** · 63 % de 110 kg GyA | FUENTE `[PVDP]` (DAF 63–95 %) | 88 |
| Sólidos químicos | dosis 50 · **100** · 200 g/m³ × 220 m³ | `[SUPUESTO]` sin fuente | 22 |
| Biomasa (si fuera aerobio) | DBO al biológico (1 − 45 %) × 95 % × 0,3 · **0,4** · 0,5 kg MS/kg DBO | FUENTE `[PVDP]` + `[SUPUESTO]` | 105 |
| **Sólidos secos** | | `[ESTIMACIÓN ILUSTRATIVA]` | **~400** |
| Fracción de sólidos de torta | 20 · **18** · 15 % | `[SUPUESTO]` | — |
| **Lodo húmedo** | | `[ESTIMACIÓN ILUSTRATIVA]` | **~2,2 t/día** |

Rango ilustrativo por escala (t/día húmedas, bajo · medio · alto): 2.500 → 0,2 · 0,6 · 1,4; 5.000 → 0,5 · 1,1 · 2,8; 10.000 → 0,9 · 2,2 · 5,6; 20.000 → 1,9 · 4,5 · 11,1. **No son salidas físicas establecidas.**

### 4.3 Tipos de lodo (cualitativo)

| Tipo | Características | Manejo | Disposición / valorización posible |
|---|---|---|---|
| **Tamizado y sólidos gruesos** | Plumas finas, recortes, restos de vísceras que escaparon a la segregación en origen | Contenedor, retiro diario | Rendering con la clase C ([`../07_subproductos/rendering.md`](../07_subproductos/rendering.md)) |
| **Flotado de DAF** | 5–30 % de sólidos (habitual 10–15 %); en base seca 30–40 % proteína y ~40 % grasa (FTE-264 `[PVDP]`); putrescible; con químicos si se usan coagulantes | Espesado, deshidratación, retiro diario | **Rendering** (si el receptor acepta químicos), biodigestión, compost; disposición como último recurso |
| **Lodo biológico aerobio** | Biomasa; estabilizable | Espesado, deshidratación, estabilización | Compost, uso agronómico (registro de enmiendas, FTE-188), relleno |
| **Lodo anaerobio** | Mucho menor y estabilizado | Retiro periódico (lagunas: años) | Uso agronómico / relleno |

**Lecturas:** (1) los lodos serán **otro flujo diario** a retirar, que se suma a la logística de [`../07_subproductos`](../07_subproductos/README.md); su magnitud se conocerá con el tren de tratamiento y la caracterización medida; (2) el flotado de DAF es rico en grasa y proteína: argumento para **integrar** efluentes y rendering (DEC-027); (3) los sólidos del lodo **no se derivan** de la masa de subproductos del balance, sino de los SST del efluente (ver [`caracterizacion_efluentes.md` §6](caracterizacion_efluentes.md)).

## 5. Qué no se decide y qué hace falta para decidir

- **No se decide:** tecnología, número de etapas, vuelco a cloaca o a cuerpo receptor, destino de lodos, biogás.
- **Hace falta:** límites de vuelco del sitio y cuerpo receptor; terreno disponible y distancia a viviendas; caracterización medida (DPV-067); receptor de flotados y lodos; potencia eléctrica disponible; cotizaciones de tratamiento llave en mano por escala (fase posterior, `19_capex`). Lista completa: [`conclusiones_agua_efluentes.md` §7](conclusiones_agua_efluentes.md).
