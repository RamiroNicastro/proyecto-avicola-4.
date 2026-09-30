# Flujo del proceso industrial de faena y procesamiento

**Fecha:** 2026-09-30 · **Versión:** 1.0 (sesión 09A) · Fase 0 (prefactibilidad)

> **Alcance:** modelo **conceptual** del proceso, desde la llegada de aves vivas hasta la expedición, con los flujos laterales de sangre, plumas, vísceras, decomisos, patas/garras, menudencias y subproductos. **No** selecciona equipos, proveedores, escala, método de enfriamiento (DEC-026), aturdimiento ni layout; **no** calcula CAPEX/OPEX. Las masas por ave vienen del balance v1.1 sin cambios ([`../04_balance_masa/conclusiones_balance.md`](../04_balance_masa/conclusiones_balance.md)); los flujos por hora, de [`modelo_capacidad_proceso.py`](modelo_capacidad_proceso.py).
> **Base:** pollo de 2,9 kg vivo, rendimiento medio, inmersión, configuración B (trozado) salvo indicación. kg/ave en **masa biológica** salvo que se indique "húmeda" o "comercial" (regla 14).
> **Fuentes:** acceso directo a sitios bloqueado (`EGRESS_BLOCKED`); la descripción de etapas es conocimiento técnico general del proceso avícola y se contrasta con extractos `[PVDP]` (FTE-09A-007, FTE-09A-023, FTE-09A-024, FTE-09A-029, FTE-09A-030 en [`../08_maquinaria/fuentes_09A.csv`](../08_maquinaria/fuentes_09A.csv)). Los parámetros de proceso (temperaturas, tiempos, voltajes) **no** se fijan: quedan para la lectura del Decreto 4238/68 original y las especificaciones de proveedores (DPV-007, DPV-09A-03).

Documentos hermanos: [`zonificacion_higienica.md`](zonificacion_higienica.md) (zonas y cruces), [`cuellos_botella.md`](cuellos_botella.md), [`arquitecturas_por_escala.md`](arquitecturas_por_escala.md), [`../08_maquinaria/catalogo_equipos.md`](../08_maquinaria/catalogo_equipos.md) (equipos por etapa).

---

## 1. Diagrama general

Leyenda de zona: **[V]** vivo · **[S]** sucia (faena inicial) · **[E]** evisceración (sucia/intermedia) · **[L]** limpia refrigerada · **[F]** frío/despacho · **[X]** subproductos y residuos (fuera de las salas de producto).

```
 CAMIÓN CON AVES VIVAS (cajones o módulos)                                   → lavado de cajones/módulos y camión [V]
   │
 E01 Recepción: pesaje del camión, documentación sanitaria (RENSPA, DTe), ante mortem   [V]
 E02 Espera en andén cubierto y ventilado (control de tiempo y temperatura)             [V]  → DOA (muertas en transporte) ─→ X1
 E03 Descarga de cajones o módulos                                                       [V]
   │   (si aturdido CAS: E05 ocurre aquí, antes del colgado)
 E04 Colgado en grilletes (línea de faena) + tramo de calma (pechera, luz tenue)          [V/S]
 E05 Aturdido (eléctrico en baño de agua o atmósfera controlada) — método NO decidido      [S]
 E06 Degüello (manual, automático o automático con repaso manual)                         [S]
 E07 Sangrado en canal/túnel de sangrado (tiempo mínimo antes del escaldado)              [S]  → SANGRE ────────────→ X2
 E08 Escaldado (tanque(s) de agua caliente, temperatura según producto)                   [S]  → agua de escaldado → efluente
 E09 Desplumado (desplumadoras en serie) + repaso                                          [S]  → PLUMAS (canal de agua/tornillo) → X3
 E10 Corte de cabeza (puede ubicarse aquí o en evisceración) y de patas en el tarso         [S]  → CABEZAS → X4 ; PATAS → E30
 E11 TRANSFERENCIA a la línea de evisceración (recolgado manual o automático)  ══ LÍMITE SUCIA / EVISCERACIÓN ══
   │
 E12 Corte de cloaca (venteo) y apertura abdominal                                          [E]
 E13 Extracción del paquete visceral (queda expuesto para inspección)                       [E]
 E14 INSPECCIÓN VETERINARIA POST MORTEM (servicio oficial): carcasa + vísceras de la misma ave  [E] → decomiso total/parcial → X5
 E15 Separación de menudencias (hígado, corazón, molleja) y de vísceras no comestibles        [E]  → MENUDENCIAS → E31 ; VÍSCERAS → X6
 E16 Retiro de buche, tráquea, pulmones; corte o retiro de cuello; retiro de cabeza si no se hizo  [E]  → CUELLO → E31 ; pulmones/otros → X6
 E17 Control final (reinspección/repaso de defectos) y lavado interior/exterior de la carcasa  [E]
   │
 E18 PREENFRIADO / ENFRIADO: inmersión (prechiller + chiller), aire o mixto — DEC-026       [E→L]
 E19 Escurrido / goteo y salida del enfriamiento                                             [L]
 E20 Clasificación: peso (calibre) y calidad (grado A / con defectos → trozado)              [L]
   │
   ├─► RUTA A: POLLO ENTERO ─ (menudencias dentro o aparte) ─ embolsado / bandeja / cajón ───────┐
   ├─► RUTA B: TROZADO ─ pechuga c/hueso · pata-muslo (muslo + pata) · alas · carcasa-esqueleto ─┤
   └─► RUTA C: DESHUESADO ─ suprema, solomillo, muslo deshuesado, piel, recortes, hueso → CMS/X7 ┤
                                                                                                 │
 E24 Envasado primario (bolsa, bandeja + film, termoformado, vacío, MAP) y pesaje/etiquetado  [L] │
 E25 Detección de metales/rayos X (según cliente) · control de peso · rotulado                [L] ◄┘
 E26 Encajonado / paletizado (envase secundario; cartón fuera de la sala limpia)               [L/F]
 E27 Refrigeración en cámara (0–4 °C, a verificar) ─────┐                                       [F]
 E28 Congelado (túnel, espiral, placas; −18 °C o menos en el centro) → cámara de congelado ─┤    [F]
 E29 Almacenamiento → preparación de pedidos → EXPEDICIÓN por andén (camión refrigerado / reefer)   [F]

 FLUJOS DE COPRODUCTOS (sala propia, dentro de zona de producto):
 E30 PATAS → escaldado específico + pelado de cutícula → clasificación A / segunda / descarte → frío/congelado
 E31 MENUDENCIAS y CUELLO → limpieza de molleja (apertura, vaciado, pelado) → enfriado rápido → envasado (bolsita, bandeja, bloque)
 E32 CARCASA-ESQUELETO → venta refrigerada/congelada, o CMS (frío ≤ 12 h / congelado ≤ 6 h, FTE-185), o rendering

 FLUJOS DE SUBPRODUCTOS Y RESIDUOS (zona X, fuera de las salas de producto; retiro diario):
 X1 DOA y aves muertas en espera → contenedor cerrado → destino según norma (DPV-066)
 X2 SANGRE → canal → bomba → tanque (sin dilución con agua de lavado) → rendering / tercero
 X3 PLUMAS → canal de agua o tornillo → escurridor/tamiz → tolva/contenedor → rendering / tercero
 X4 CABEZAS → rendering
 X5 DECOMISOS (servicio oficial) → recipiente identificado y precintado → destino según norma
 X6 VÍSCERAS NO COMESTIBLES + contenido GI → canal/bomba de vacío → tamiz → contenedor → rendering / residuo
 X7 HUESO, residuo óseo de CMS, descarte de garras, piel/grasa sin comprador → rendering
 EFLUENTES: agua de escaldado, desplumado, lavado de carcasas, rebalse del chiller, limpieza → pretratamiento
            (tamiz, separación de sólidos y grasas) → tratamiento (11_agua_efluentes; no se dimensiona aquí)
```

**Orden variable:** la posición de algunas operaciones cambia según el equipo y la escala (p. ej., el corte de cabeza puede estar antes o dentro de la evisceración; el aturdido CAS ocurre antes del colgado; el trozado puede hacerse en línea colgada o en mesa). El diagrama fija **qué** debe ocurrir, no **dónde** ni **con qué equipo**.

---

## 2. Etapas: función, control y masa que pasa

Masa por ave en cada punto (2,9 kg, medio): vivo 2,900 → sin sangre drenada 2,801 → sin plumas (biológica) 2,650 → sin cabeza y patas 2,465 → carcasa eviscerada **2,073** (+ cuello 0,075 + menudencias 0,110 separados) → tras enfriamiento por inmersión +0,122 de agua absorbida → carcasa apta para trozar 2,036 (después de decomisos). Fuente: balance v1.1.

| # | Etapa | Función | Qué hay que controlar (cualitativo) | Riesgo si falla | Salida lateral (kg/ave) |
|---|---|---|---|---|---|
| E01 | Recepción | Identificar lote, documentos, peso del camión, ante mortem | Trazabilidad lote–granja; horas de ayuno y viaje | Lote sin documentación; mortalidad; decomisos | — |
| E02 | Espera | Amortiguar entre llegada y ritmo de faena | Tiempo de espera, ventilación, temperatura, densidad | Muertes por calor (DOA), estrés, hematomas | DOA (fuera del balance; 0,3 % en transporte, `03_produccion_primaria`) |
| E03 | Descarga | Sacar aves de cajones/módulos | Suavidad, altura de caída | Fracturas y hematomas (grado de alas y garras) | — |
| E04 | Colgado | Colocar aves en grilletes | Ritmo, calma, fatiga del operario | **Cuello de botella humano**; lesiones; bienestar | — |
| E05 | Aturdido | Insensibilizar antes del degüello | Parámetros eléctricos o de gas; verificación de eficacia | Bienestar (norma y exportación UE); calidad (hemorragias, fracturas) | — |
| E06 | Degüello | Cortar vasos del cuello | Precisión del corte; repaso manual | Aves que llegan vivas al escaldado (falla grave) | — |
| E07 | Sangrado | Drenar sangre | Tiempo de sangrado | Mala sangría: carcasas rojas, decomisos | Sangre 0,099 drenada (0,084 recuperada) |
| E08 | Escaldado | Aflojar plumas | Temperatura y tiempo; renovación de agua; agitación | Sobreescaldado (piel dañada) o subescaldado (plumas); contaminación cruzada | Agua de escaldado → efluente |
| E09 | Desplumado | Remover plumas | Ajuste de dedos y velocidad | Piel rota, alas quebradas, plumas residuales | Plumas 0,151 (0,241 húmedas) |
| E10 | Cabeza y patas | Separar extremidades | Corte en la articulación | Pérdida de garra o de carcasa | Cabeza 0,072; patas 0,113 |
| E11 | Transferencia | Pasar de línea de faena a evisceración | Sincronía de ritmos; recolgado | **Límite higiénico**; si es manual, cuello de botella | — |
| E12–E13 | Apertura y extracción | Abrir y sacar vísceras sin romperlas | Calibración a tamaño de ave (uniformidad del lote) | Ruptura intestinal → contaminación fecal → reproceso o decomiso | — |
| E14 | Inspección post mortem | Dictamen oficial ave por ave | Presentación carcasa + vísceras; iluminación; espacio | **Detiene o reduce la línea** si el ritmo excede la capacidad de inspección | Decomisos 0,040 |
| E15–E16 | Menudencias, vísceras, cuello | Separar comestibles de no comestibles | Identificación, enfriado rápido de menudencias | Mezclar comestible con no comestible | Menudencias 0,110; cuello 0,075; vísceras 0,130; contenido GI 0,035 |
| E17 | Lavado y control | Eliminar contaminación visible | Criterio de "cero contaminación visible" (a verificar) | Rechazos microbiológicos | Agua → efluente |
| E18 | Enfriamiento | Bajar la temperatura de la carcasa | Tiempo de residencia; temperatura final; renovación de agua; agua absorbida (límite 8 %, DPV-061) | **Punto crítico de inocuidad**; cuello de botella de capacidad | Inmersión: +0,122 agua; aire: −0,037 evaporación |
| E19 | Escurrido | Eliminar agua superficial | Tiempo | Exceso de agua (rotulado, cliente) | Goteo 0,037 |
| E20 | Clasificación | Separar por peso y calidad | Balanza de línea / criterio visual | Canales defectuosas vendidas enteras | Canales no aptas para entero → trozado (6 % medio) |
| E21–E23 | Entero / trozado / deshuese | Convertir canal en productos | Rendimiento, temperatura de sala, tiempo | Merma, temperatura, contaminación | Recortes, piel, hueso (config. C 0,317) |
| E24–E26 | Envasado, control, encajonado | Presentación comercial y trazabilidad | Peso, sellado, etiqueta, metales | Reclamos, retiros de mercado | Envases descartados |
| E27–E29 | Frío y expedición | Conservar y despachar | Temperatura de cámara y producto; FEFO | Ruptura de cadena de frío | — |
| E30 | Patas → garras | Pelar y clasificar | Escaldado específico; pelado; grado | Costo sin comprador (si no hay mercado: no pelar, DEC-031) | Garra A 0,085; segunda 0,016; descarte 0,005; cutícula 0,006 |
| E31 | Menudencias | Limpiar y enfriar | Pelado de molleja; frío inmediato | Perecibilidad (días) | — |
| E32 | Carcasa-esqueleto | Vender, CMS o rendering | CMS: 12 h refrigerada / congelada ≤ 6 h (FTE-185 `[PVDP]`) | Sin comprador → rendering (DEC-029) | 0,393 |

## 3. Flujos laterales (separados del producto)

| Flujo | Origen | kg/ave | Cómo se mueve (conceptual) | Almacenamiento temporal | Destino | Condición crítica |
|---|---|---|---|---|---|---|
| **Sangre** | E07 | 0,084 recuperada (0,099 drenada) | Canal de sangrado inclinado → bomba | Tanque cerrado; **no diluir** con agua de lavado | Rendering / tercero (SUP-049) | Recuperarla reduce ~7 veces la carga de DQO del efluente ([`../07_subproductos/conclusiones_valorizacion.md` §4](../07_subproductos/conclusiones_valorizacion.md)); retiro en horas |
| **Plumas** | E09 | 0,241 húmedas | Canal de agua bajo desplumadoras o tornillo → escurridor | Tolva o contenedor | Rendering / tercero / propio (no decidido) | Mayor subproducto en masa; volumen voluminoso; retiro diario |
| **Cabezas** | E10/E16 | 0,072 | Canal o tornillo | Contenedor | Rendering | — |
| **Vísceras no comestibles + contenido GI** | E15–E16 | 0,130 + 0,035 | Canal de agua o transporte por vacío → tamiz | Contenedor cerrado | Rendering / residuo | Muy perecederas; olor |
| **Decomisos** | E02 (DOA), E14 | 0,040 (+ DOA) | Recipientes identificados, bajo control del servicio oficial | Recipiente precintado/cerrado | Según norma (digestor, rendering, incineración; DPV-066) | No deben mezclarse con subproductos aptos |
| **Patas/garras** | E10 | 0,113 brutas | Transportador a sala de garras (zona de producto) | Frío | Garras A/segunda (B) o rendering | Coproducto comestible: **no** va con subproductos |
| **Menudencias y cuello** | E15–E16 | 0,110 + 0,075 | Canal de agua fría o bomba de menudencias → enfriador | Frío | Venta / dentro del entero / pet food | Comestibles: circuito de producto |
| **Hueso, residuo de CMS, piel/grasa sin comprador** | E22–E23, E32 | Config. C: 0,331 | Contenedores desde salas de deshuese | Frío si se valoriza | Rendering | Solo en configuración C |
| **Agua de proceso** | E08, E09, E17, E18, limpieza | No es del balance (§2 de [`../04_balance_masa/auditoria_balance.md`](../04_balance_masa/auditoria_balance.md)) | Desagües separados por zona | — | Pretratamiento → tratamiento | Se dimensiona en `11_agua_efluentes` |

**Por hora neta de faena a 8 h** (config. B, `[ESTIMACIÓN]`, [`capacidad_proceso.csv`](capacidad_proceso.csv)):

| Corriente (kg/h) | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Pollo vivo | 906 | 1.812 | 3.625 | 7.250 |
| Carcasa al enfriamiento | 648 | 1.296 | 2.592 | 5.184 |
| A trozado (config. B) | 636 | 1.273 | 2.545 | 5.091 |
| A deshuese (config. C) | 359 | 719 | 1.438 | 2.875 |
| Comestible a empaque (comercial) | 749 | 1.498 | 2.996 | 5.991 |
| Sangre recuperada | 26 | 52 | 105 | 210 |
| Plumas húmedas | 75 | 151 | 302 | 603 |
| Vísceras no comestibles | 41 | 82 | 163 | 326 |
| Cabezas | 23 | 45 | 91 | 181 |
| Garras A + segunda | 32 | 63 | 126 | 253 |
| Menudencias + cuello | 57 | 115 | 230 | 459 |

Con 6 h netas, multiplicar por 1,33; con 10 h, por 0,8; con 16 h, por 0,5. **Sólidos a retirar por día operativo** (C + decomisos + contenido GI): 1,5 / 3,0 / 6,1 / 12,2 t.

## 4. Rutas de producto (entero / trozado / deshuesado; refrigerado / congelado)

```
                ┌─ ENTERO ── (con/sin menudencias) ── bolsa · bandeja · cajón ──┬── refrigerado (días)
 CARCASA FRÍA ──┤                                                              │
 CLASIFICADA    ├─ TROZADO ── pechuga c/h · pata-muslo · alas · esqueleto ─────┼── congelado (túnel/espiral/IQF; meses)
                │                                                              │
                └─ DESHUESADO ─ suprema · solomillo · muslo desh. · piel ──────┴── exportación (congelado, rotulado por destino)
                                 └─ hueso/esqueleto → CMS (12 h / ≤ 6 h) o rendering
```

- Las tres rutas **comparten** todo el tramo E01–E20; se diferencian desde la clasificación. Qué módulos agrega cada ruta: [`arquitecturas_por_escala.md` §7](arquitecturas_por_escala.md).
- Aun en una planta de "pollo entero", entre 3 % y 12 % de las canales no son aptas para venta entera (balance v1.1, escenario de condenas) y **necesitan una sala de trozado mínima** desde el día 1.
- La proporción refrigerado / congelado es la que más cambia el frío (perfiles P1–P3, SUP-055): **comestible a congelar por día operativo** con config. B: P1 0,6 / 1,2 / 2,4 / 4,8 t; P2 2,4 / 4,8 / 9,6 / 19,2 t; P3 3,0 / 6,0 / 12,0 / 24,0 t para 2.500 / 5.000 / 10.000 / 20.000 aves/día.

## 5. Puntos de inspección y control a prever en el diseño

| Punto | Tipo | Qué exige al proceso (conceptual) | Estado |
|---|---|---|---|
| Recepción (E01–E02) | Inspección ante mortem oficial; documentos sanitarios | Espacio y luz para observar lotes; registro de tiempos | `[PVDP]` FTE-016 |
| Aturdido (E05) | Bienestar animal (verificación de eficacia) | Punto de observación antes del degüello | `[PVDP]` |
| Post mortem (E14) | Inspección oficial ave por ave | Presentación sincronizada carcasa–vísceras; iluminación; puestos cuyo número depende del ritmo (dato normativo pendiente, DPV-09A-03) | `[PENDIENTE DE VALIDACIÓN]` |
| Enfriamiento (E18) | Punto crítico candidato (HACCP): temperatura final; agua absorbida | Con aire: ≤ 7 °C en lo profundo de la pechuga antes de envasar (extracto FTE-09A-030 `[PVDP]`); parámetros de inmersión no obtenidos | `[PVDP]` |
| Salas de corte (E21–E23) | Temperatura de sala y de producto; tiempo fuera del frío | Sala refrigerada | `[PENDIENTE DE VALIDACIÓN]` |
| Envasado (E24–E25) | Detección de cuerpos extraños; rotulado | Equipos de control por línea de envasado | Exigencia de cliente |
| Congelado y cámaras (E27–E29) | Temperatura de producto y cámara | Registro continuo | `[PVDP]` |
| CMS (E32) | 12 h refrigerada o congelada ≤ 6 h | Sala y frío dedicados | `[PVDP]` FTE-185 |
