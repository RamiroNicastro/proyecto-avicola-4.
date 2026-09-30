# Alternativas de tratamiento de efluentes y manejo de lodos (conceptual)

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09C) · Fase 0

> **Alcance:** comparación **conceptual** de pretratamientos, tratamientos biológicos y manejo de lodos. **No se elige tecnología**, no se dimensionan unidades, no se selecciona proveedor ni se calcula CAPEX/OPEX. Las eficiencias citadas son `[PVDP]` (FTE-09C-05, 09C-12, 09C-13). Cargas por escala: [`caracterizacion_efluentes.md` §4](caracterizacion_efluentes.md).

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
| **DAF** (flotación por aire disuelto, a menudo con coagulante/floculante) | Burbujas finas flotan grasas y sólidos finos | DBO 30–90 %, DQO 70–80 %, SST 38–70 %, grasas 63–95 % (FTE-09C-05 `[PVDP]`) | Estándar en plantas cárnicas; reduce mucho la carga al biológico | Genera **flotado** (lodo) con 10–15 % de sólidos (FTE-09C-13); consumo de químicos y energía; la **DQO soluble** (sangre) no se remueve |
| Otros: coagulación química, electrocoagulación, membranas (UF/ósmosis) | Remoción avanzada / reúso | Alta | Aparecen en revisiones recientes (FTE-09C-05); membranas orientadas a **reúso** | Costo, ensuciamiento; no se evalúan en esta fase |

## 3. Tratamiento biológico — comparación conceptual

| Criterio | **Lagunas anaerobias** (abiertas o cubiertas) | **Reactores anaerobios** (UASB, EGSB, filtros) | **Lagunas aireadas / facultativas** | **Lodos activados / SBR** (reactores aerobios) | **Combinación anaerobio + aerobio** |
|---|---|---|---|---|---|
| Terreno | **Muy alto** (grandes superficies) | Bajo | Alto | Bajo–medio | Medio |
| Carga que tolera | Alta; robustas a variaciones | Alta (hasta 7–11 kg DQO/m³·día a 20–30 °C en ensayos, FTE-09C-12); sensibles a grasas y SST (necesitan buen DAF) | Media | Media; sensibles a picos (necesitan ecualización) | Alta |
| Calidad de salida | Insuficiente sola para vuelco estricto | Remoción parcial (55 % DQO total en un ensayo con efluente sin sedimentar); necesita postratamiento | Media | Alta; puede nitrificar/desnitrificar | Alta |
| Nitrógeno | No lo remueve (lo convierte en amonio) | No lo remueve | Parcial | **Sí** (con diseño específico) | Sí (etapa aerobia) |
| Olor | **Alto** si son abiertas (sulfhídrico); cubiertas lo controlan | Bajo (cerrado) | Medio | Bajo | Bajo–medio |
| Energía | Muy baja; **genera biogás** (cubiertas) | Baja; **genera biogás** | Media (aireación) | **Alta** (aireación: 0,7–2 kWh/kg DBO removida en el modelo, `[SUPUESTO]`) | Menor que aerobio solo |
| Lodos | Muy pocos; acumulación y retiro periódico | Pocos | Medios | **Muchos** (0,3–0,5 kg MS/kg DBO, `[SUPUESTO]`) | Menos que aerobio solo |
| Operación | Simple; arranque lento; estacional (temperatura) | Técnica; arranque de semanas a meses | Simple–media | **Técnica** (operador calificado, laboratorio) | Técnica |
| Emisiones | CH₄, CO₂, N₂O si abiertas (FTE-09C-12) | Biogás captado | CO₂ | CO₂, lodos | Biogás captado |
| Escalabilidad por módulos | Por celdas (requiere terreno reservado) | Por reactores | Por celdas | Por trenes | Por trenes |

**Cómo se relaciona la elección con el proyecto** (no se decide aquí; DEC propuesta):

| Factor | Cómo empuja la elección |
|---|---|
| **Terreno** | Mucho terreno barato y alejado → lagunas posibles; terreno escaso o periurbano → reactores compactos |
| **Carga** (escala × gestión) | A 2.500–5.000 aves/día (125–900 kg DQO/día) conviene la simplicidad; a 10.000–20.000 (500–3.600 kg DQO/día) la recuperación de biogás y la compacidad pesan más |
| **Normativa** | Vuelco a cloaca (prestador fija límites y tarifa por carga) vs pluvial/curso (límites estrictos: 50 mg/L DBO, 250 mg/L DQO en PBA `[PVDP]`) vs suelo (restringido; inyección prohibida en PBA) → define el grado de tratamiento y si hace falta remover N y P |
| **Olor y vecindad** | Lagunas abiertas y acopio de lodos cerca de poblaciones son un riesgo de conflicto y de habilitación ([`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md) §10) |
| **Energía** | Red débil (zona rural) → penaliza aeración intensiva; biogás puede cubrir parte del calor (caldera) |
| **Operación** | Personal técnico disponible en la zona; laboratorio; turnos (el biológico funciona 365 días aunque la planta faene 250) |
| **Expansión** | Reservar terreno y trazas para duplicar el tratamiento cuando crezca la escala (principio de [`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md): sobredimensionar lo barato de prever) |
| **Exportación** | Auditorías de importadores revisan gestión ambiental y de subproductos; no fija tecnología pero sí registros y cumplimiento |

**Vuelco a colectora cloacal:** si el sitio tiene cloaca con capacidad, el prestador puede aceptar un efluente pretratado (tamiz + grasas + DAF) con límites y canon; el biológico lo haría la planta municipal. Depende 100 % del sitio: **no se supone**.

## 4. Lodos

| Tipo | Generación (10.000 aves/día, medio; orden de magnitud `[ESTIMACIÓN]`) | Características | Manejo | Disposición / valorización posible |
|---|---|---|---|---|
| **Tamizado y sólidos gruesos** | Parte de los 6,1 t/día de sólidos a retirar (si no se retiraron antes) | Plumas finas, recortes, vísceras | Contenedor, retiro diario | Rendering con el resto de la clase C ([`../07_subproductos/rendering.md`](../07_subproductos/rendering.md)) |
| **Flotado de DAF** | ~320 kg MS/día → **~2,7 t/día húmedo** (12 % sólidos) | 30–40 % proteína y ~40 % grasa en base seca (FTE-09C-13 `[PVDP]`); putrescible; con químicos si se usan coagulantes | Espesado, deshidratación (centrífuga, prensa), retiro diario | **Rendering** (si el receptor acepta químicos), biodigestión, compost; disposición como último recurso |
| **Lodo biológico aerobio** | ~105 kg MS/día (si todo el biológico fuera aerobio) | Biomasa; estabilizable | Espesado, deshidratación, estabilización | Compost, uso agronómico (sujeto a normativa: registro de enmiendas, FTE-188), relleno |
| **Lodo anaerobio** | Mucho menor | Estabilizado | Retiro periódico (lagunas: años) | Uso agronómico / relleno |
| **Total deshidratado** (DAF + biológico) | **~2,4 t/día** (1,0–5,8 según nivel) | | | |

Por escala (t/día deshidratadas, bajo · medio · alto): 2.500 → 0,2 · 0,6 · 1,5; 5.000 → 0,5 · 1,2 · 2,9; 10.000 → 1,0 · 2,4 · 5,8; 20.000 → 2,0 · 4,7 · 11,7.

**Lecturas:**
1. Los lodos son **otro flujo diario de subproductos** que hay que sacar de la planta, del orden de un 40 % adicional sobre los 6,1 t/día de sólidos del balance (medio, 10.000 aves/día). Se suma al problema logístico de [`../07_subproductos`](../07_subproductos/README.md).
2. El flotado de DAF es rico en grasa y proteína: puede ir a rendering (mejor destino) o a biodigestión (biogás). Es un argumento para **integrar** el diseño de efluentes con la decisión de rendering (DEC-027).
3. Toda cifra de lodos es orden de magnitud: depende de químicos, de la tecnología y de la edad de lodo, ninguno decidido.

## 5. Qué no se decide y qué hace falta para decidir

- **No se decide:** tecnología, número de etapas, vuelco a cloaca o a cuerpo receptor, destino de lodos, biogás.
- **Hace falta:** límites de vuelco del sitio y cuerpo receptor; terreno disponible y distancia a viviendas; caracterización medida (DPV-067); receptor de flotados y lodos; potencia eléctrica disponible; cotizaciones de tratamiento llave en mano por escala (fase posterior, `19_capex`). Lista completa: [`conclusiones_agua_efluentes.md` §6](conclusiones_agua_efluentes.md).
