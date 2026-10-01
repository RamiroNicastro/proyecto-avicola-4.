# Superficies y layouts conceptuales por escala

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 12C) · Fase 0

> **Alcance:** superficies en **rango bajo / medio / alto** para 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día operativo, separadas en m² de proceso, frío, servicios, personal/admin, exteriores, efluentes y reserva; esquema de bloques por escala; comparación espacial **una línea vs dos líneas** sin elegir. **No** fija escala (DEC-001, DEC-033), **no** es un plano, **no** es CAPEX.
> **No fingir precisión:** los totales se redondean en el texto; las cifras con unidades salen de [`modelo_superficies.py`](modelo_superficies.py) v1.0 (`--tablas`) y están completas en [`escenarios_superficies.csv`](escenarios_superficies.csv). Todo es `[ESTIMACIÓN]` con factores `[SUPUESTO]`; 23 de 54 áreas están en estado **PROXY** porque faltan huellas de equipos, dotación y capacidades de camión (alertas listadas en §7). El rango alto/bajo es **~2–3 veces** en construido y **~5–7 veces** en terreno: esa amplitud es el resultado, no un defecto.

**Escenario de referencia (no es decisión):** config. B (trozado), 2,9 kg, 8 h netas, 250 días; perfil P1 (90 % refrigerado / 10 % congelado) con 3 días de refrigerado y 14 de congelado (base días de producción, 09C); automatización "semi"; una línea; enfriamiento **sin definir** (se reserva el mayor, aire); efluentes **sin definir** (el total usa anaerobio + aerobio como reserva; las demás tecnologías en §4); sin escala objetivo (reserva = 25 / 50 / 100 % de lo operativo); reserva de rendering incluida.

---

## 1. Totales por categoría (m², bajo / medio / alto)

| Categoría | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| **Proceso** | 690 / 1.000 / 1.490 | 1.090 / 1.610 / 2.420 | 1.800 / 2.700 / 4.090 | 3.080 / 4.640 / 7.250 |
| **Frío** | 100 / 140 / 220 | 120 / 180 / 350 | 180 / 330 / 660 | 310 / 600 / 1.310 |
| **Servicios** | 270 / 360 / 510 | 320 / 470 / 700 | 520 / 810 / 1.220 | 920 / 1.450 / 2.260 |
| **Personal / admin** | 170 / 270 / 490 | 170 / 330 / 620 | 230 / 470 / 880 | 340 / 760 / 1.440 |
| **= m² construidos** | **1.230 / 1.780 / 2.710** | **1.700 / 2.600 / 4.080** | **2.730 / 4.310 / 6.850** | **4.660 / 7.450 / 12.260** |
| Exteriores | 1.150 / 2.030 / 3.610 | 1.340 / 2.570 / 5.140 | 1.750 / 3.860 / 8.200 | 2.530 / 6.150 / 14.520 |
| Efluentes (anaerobio + aerobio) | 130 / 220 / 520 | 130 / 250 / 780 | 140 / 330 / 1.520 | 160 / 590 / 3.030 |
| **= m² operativos** | **2.500 / 4.030 / 6.840** | **3.170 / 5.420 / 9.990** | **4.620 / 8.490 / 16.570** | **7.340 / 14.190 / 29.810** |
| Reserva (sin objetivo + rendering) | 920 / 2.410 / 7.440 | 1.090 / 3.110 / 10.590 | 1.450 / 4.640 / 17.170 | 2.260 / 7.740 / 30.770 |
| **Terreno conceptual (ha)** | **0,8 / 2,0 / 5,3** | **0,9 / 2,3 / 6,5** | **1,2 / 3,1 / 8,7** | **1,7 / 4,4 / 12,8** |
| Huella de edificios / terreno | 16 / 9 / 5 % | 19 / 11 / 6 % | 23 / 14 / 8 % | 28 / 17 / 10 % |
| m² cubiertos por ave/día | 0,49 / 0,71 / 1,08 | 0,34 / 0,52 / 0,82 | 0,27 / 0,43 / 0,68 | 0,23 / 0,37 / 0,61 |

**Lecturas:**

1. **Duplicar la escala no duplica el edificio:** de 2.500 a 20.000 (×8) los m² construidos medios crecen ×4,2 (1.780 → 7.450). Hay mínimos funcionales (vestuarios, oficina SENASA, salas técnicas, andén de recepción) que existen igual en una planta chica; por eso los m² por ave/día bajan de ~0,7 a ~0,4. **Esto es física de superficies, no economía de escala en costos**: no se concluye nada sobre escala mínima eficiente (DPV-083).
2. **El proceso es ~55–62 % de lo construido**; el frío solo ~8 % con perfil P1. Cambia mucho con el perfil (§3).
3. **El edificio es una parte chica del terreno:** con márgenes perimetrales medios de 30 m (retiro 10 m + buffer 20 m, ambos supuestos), la huella ocupa ~10–17 % del terreno medio. En el escenario medio del modelo actual, los factores reservados para retiros, buffers y franjas representan aproximadamente **50–68 % del terreno conceptual** según la escala (57 % a 10.000 aves/día; 56 % si se reserva para 20.000). **No** es lo que exige ningún municipio: separa tres cosas distintas — el **retiro reglamentario real** (lo fija el municipio, DPV-12C-05; aquí 5 / 10 / 15 m supuestos), el **buffer de diseño** (supuesto/proxy 10 / 20 / 40 m, SUP-12C-15) y la eventual **reserva sanitaria o ambiental** (supuesto o requisito según jurisdicción, DPV-106). Con márgenes 0 el terreno medio a 10.000 sería ~1,3 ha; con solo 10 m de retiro, ~1,8 ha (test T21: cambiar retiro o buffer cambia el terreno y no el edificio). Ver [`guia_ramiro.md` §6](guia_ramiro.md). Coincide en orden de magnitud con la regla general de que los edificios ocupen ~20 % del predio en mataderos pequeños (FTE-12C-007, `[PVDP]`).
4. **Contraste con plantas argentinas (`[PVDP]`, extractos de prensa/INTI, nunca leídos en original):** Frigorífico MARK ~12.000–15.000 m² cubiertos para 70.000–80.000 aves/día (0,15–0,21 m²/(ave/día)); Avex >13.000 m² para ~120.000/día (~0,11); salas municipales de 181 m² para 1.000 aves/día (0,18, China Muerta) y 290 m² para 200–300 aves/día (~1,0–1,45, Ayacucho). Los valores del modelo (0,23–1,08) caen **dentro** de esa banda y bajan con la escala como las referencias, pero **no se sabe qué incluye cada m² declarado** (cámaras, oficinas, elaborados): es contraste de orden de magnitud, no calibración (regla 18, DPV-12C-07).

## 2. Áreas principales por escala (m², medio; rango completo en el CSV)

| Área | Zona | 2.500 | 5.000 | 10.000 | 20.000 | Estado |
|---|---|---|---|---|---|---|
| Recepción y andén de espera (bahías) | Sucia | 180 (2) | 180 (2) | 180 (2) | 180 (2) | PROXY (aves/camión) |
| Colgado y aturdido | Sucia | 45 | 75 | 130 | 230 | PROXY |
| Sangrado, escaldado, desplumado | Sucia | 90 | 160 | 275 | 480 | PROXY |
| Evisceración e inspección | Transición | 105 | 185 | 325 | 560 | PROXY |
| Enfriamiento (reserva aire) | Limpia | 90 | 175 | 350 | 700 | ESTIMACION |
| Trozado | Limpia | 105 | 180 | 315 | 550 | PROXY |
| Garras y menudencias | Limpia | 65 | 115 | 195 | 345 | PROXY |
| Envasado y empaque | Limpia | 95 | 165 | 290 | 505 | PROXY |
| Circulación de proceso | — | 180 | 290 | 485 | 835 | ESTIMACION |
| Cámaras (refrig. + cong.) | Fría | 50 | 80 | 155 | 310 | ESTIMACION |
| Docks de expedición | Despacho | 45 (1) | 45 (1) | 90 (2) | 135 (3) | PROXY (t/camión) |
| Sala de subproductos | Subproductos | 35 | 45 | 90 | 185 | ESTIMACION |
| Sala de máquinas de frío | Utilities | 60 | 60 | 60 | 65 | PROXY |
| Vestuarios | Personal | 50 | 85 | 150 | 280 | PROXY (dotación) |
| Comedor | Personal | 35 | 55 | 100 | 185 | PROXY (dotación) |
| Oficina SENASA | Admin. | 30 | 30 | 35 | 45 | ESTIMACION |
| Circulación pesada | Exterior | 620 | 910 | 1.510 | 2.610 | ESTIMACION |
| Estacionamiento | Exterior | 500 | 720 | 1.160 | 2.030 | PROXY (dotación) |
| Dotación proxy por turno (personas) | — | 40 | 65 | 115 | 215 | PROXY |

## 3. Frío: perfil e inventario (m² de frío medio · t congeladas en stock, de 09C)

| Perfil / días refrig.–cong. | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| P1 3/14 | 140 · 8 t | 180 · 17 t | 330 · 34 t | 600 · 67 t |
| P1 7/28 | 200 · 17 t | 310 · 34 t | 590 · 67 t | 1.110 · 134 t |
| P2 3/14 | 160 · 34 t | 250 · 67 t | 480 · 134 t | 900 · 268 t |
| P2 7/28 | 240 · 67 t | 410 · 134 t | 800 · 268 t | 1.540 · 537 t |
| P3 3/14 | 180 · 42 t | 270 · 84 t | 530 · 168 t | 1.000 · 336 t |
| P3 7/28 | 250 · 84 t | 450 · 168 t | 870 · 336 t | 1.680 · 671 t |

**Lecturas:** (1) el **perfil y los días de stock** mueven el frío tanto como la escala: a 10.000 aves/día, pasar de P1 3/14 a P3 7/28 multiplica ×2,6 los m² de frío; (2) duplicar los días agranda las **cámaras** pero no el **túnel** (test T04; congelar ≠ almacenar, 09C); (3) el frío es **barato de agregar en módulos** si hay lugar y troncales previstas ([`estrategia_expansion.md`](estrategia_expansion.md)), y **caro** si la sala de máquinas o la fachada de cámaras quedaron encerradas; (4) los m² son de **planta**: las cámaras son altas (densidad de estiba con 3,5–7 m de altura útil, `[PVDP]`, DPV-12C-06).

## 4. Efluentes: cómo la tecnología (no elegida) cambia el terreno

m² de efluentes (medio) · terreno total medio en ha (rango bajo–alto):

| Tecnología | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Vuelco a colectora (si el prestador lo acepta) | 130 · 2,0 (0,8–5,2) | 140 · 2,3 (0,9–6,3) | 160 · 3,0 (1,2–8,4) | 290 · 4,3 (1,6–12,2) |
| Aerobio compacto | 260 · 2,0 (0,8–5,4) | 330 · 2,4 (0,9–6,6) | 480 · 3,1 (1,2–9,0) | 910 · 4,4 (1,7–13,3) |
| Anaerobio + aerobio | 220 · 2,0 (0,8–5,3) | 250 · 2,3 (0,9–6,5) | 330 · 3,1 (1,2–8,7) | 590 · 4,4 (1,7–12,8) |
| **Lagunas** | **2.630 · 2,6 (0,9–10,7)** | **5.090 · 3,5 (1,1–16,2)** | **9.990 · 5,2 (1,5–26,5)** | **19.920 · 8,2 (2,2–45,6)** |

**Lecturas:** en el escenario de superficies actual, las tecnologías compactas cambian poco el terreno total (el edificio, las playas y los márgenes supuestos dominan) y **las lagunas lo cambian mucho**: el biológico con lagunas resulta ~35–40 veces el compacto — **RESULTADO DEL ESCENARIO DE SUPERFICIES ACTUAL / PROXY, no una relación general de ingeniería**; la relación real depende de tecnología, carga, clima, tiempo de retención, profundidad, calidad de efluente, terreno y normativa. En el escenario, el tratamiento pasa a ser el área más grande del predio y el rango alto llega a decenas de hectáreas, además de exigir distancia a viviendas (alerta `LAGUNAS_DISTANCIA`). Por eso la elección del tren de tratamiento (DEC-043) y la del terreno (DEC-003) **no pueden hacerse por separado**: un terreno chico periurbano **elimina** la opción lagunas; un terreno rural grande la mantiene. Lodos: PROXY (09C pendiente).

## 5. Sensibilidad a 10.000 aves/día (m² construidos medio · terreno medio)

| Variante | m² construidos | Terreno | Comentario |
|---|---|---|---|
| Referencia | 4.310 | 3,1 ha | — |
| Config. A (entero) | 3.940 | 2,9 ha | Sala de trozado mínima igual existe (6 % de canales no aptas) |
| Config. C (deshuesado) | 4.820 | 3,3 ha | Salas de deshuese y CMS; más personal |
| P3 con 7/28 días | 4.900 | 3,3 ha | Cámaras para lotes de exportación |
| Automatización manual | 4.630 | 3,3 ha | Más puestos y más vestuarios |
| Automatización alta | 4.130 | 3,0 ha | Factores débiles (SUP-12C-03) |
| Dos líneas | 4.580 | 3,2 ha | §6 |
| Enfriamiento por inmersión | 4.130 | 3,0 ha | Aire: +170 m² (la referencia ya reserva aire) |
| 16 h netas (2 turnos) | 2.970 | 2,6 ha | Línea más lenta = salas más chicas, **pero** ecuación de 24 h en alerta (09A); no es ahorro garantizado |
| Escala objetivo 20.000 | 4.310 | 3,3 ha | Igual edificio hoy; más terreno reservado |
| Sin reserva de rendering | 4.310 | 3,0 ha | −0,06 ha |

## 6. Una línea vs dos líneas (comparación espacial, sin elegir; DEC-038)

Superficie de las salas de línea (colgado → enfriamiento), medio:

| Escala | 1 línea | 2 líneas | Diferencia |
|---|---|---|---|
| 2.500 | 330 m² | 400 m² | +22 % |
| 5.000 | 590 m² | 720 m² | +22 % |
| 10.000 | 1.080 m² | 1.310 m² | +21 % |
| 20.000 | 1.970 m² | 2.370 m² | +21 % |

El **+21–22 %** vale **en la parametrización actual del modelo**, no como regla general: sale de que dos líneas a la mitad del ritmo ocupan 2 × (1/2)^0,8 ≈ 1,15 veces una línea, más 5–15 % de pasillo de separación (SUP-12C-01, SUP-12C-03), todo con proxies. Puede cambiar —incluso de signo en algún área— con el **proveedor**, el **footprint** real de cada línea, los **buffers**, el espacio de **mantenimiento**, la **automatización** y la **disposición física** (equipos compartidos, chiller común, nave en U).

| Criterio | Una línea | Dos líneas |
|---|---|---|
| **Espacio** | Menor en la parametrización actual (~−18 % en salas de línea) | Mayor en la parametrización actual; nave más ancha |
| **Redundancia** | Ninguna: una falla detiene toda la faena | Una línea sigue (~50 %); el resto de la planta (chiller compartido, frío, efluentes) puede seguir siendo punto único |
| **Mantenimiento** | Un solo parque; parada total para intervenir | Se puede mantener una mientras la otra produce, **si** el layout permite aislar cada línea (pasillo técnico entre ambas) |
| **Expansión** | Se compra para el ritmo final o se reemplaza; requiere que la nave tenga el **largo** del ritmo final | La 2.ª línea se instala en **espacio reservado paralelo**: requiere prever el **ancho** y las troncales desde el día 1 |
| **Flujos** | Un único eje sucia → limpia: simple | Dos ejes paralelos que convergen en la zona limpia; riesgo de cruces en la transferencia y en la salida del chiller; dos frentes de colgado |
| **Limpieza** | Toda la línea en la misma ventana | Limpieza por sectores posible (útil con dos turnos, 09A §5) |
| **Inspección oficial** | Puestos concentrados | Puestos duplicados (DPV-090) |

```
UNA LÍNEA (nave larga)                       DOS LÍNEAS (nave ancha; la 2.ª puede quedar como reserva)
┌────────┬─────────┬─────────┬──────────┐    ┌────────┬─────────┬─────────┬──────────┐
│SUCIA 1 │ TRANS 2 │ LIMPIA 3│  FRÍA 4  │    │SUCIA L1│ TRANS L1│         │          │
│ ═══════╪═════════╪═══▶     │          │    │ ═══════╪═════════╪══▶ LIMPIA 3  FRÍA 4 │
│        │         │         │          │    │- - - - - - - - - - (pasillo técnico)   │
└────────┴─────────┴─────────┴──────────┘    │SUCIA L2│ TRANS L2│══▶      │          │
  ampliar = alargar o reemplazar             └────────┴─────────┴─────────┴──────────┘
                                               ampliar = ocupar la franja reservada
```

## 7. Esquemas de bloques por escala (no son planos)

Los cuatro tamaños comparten **la misma secuencia de zonas**; cambian el tamaño de cada bloque, el número de bahías/docks y lo que se reserva.

```
2.500 aves/día — ~1.800 m² construidos (1.200–2.700) · terreno ~2 ha (0,8–5,3)
  [Playa vivo]→[Andén 2 bahías]→[SUCIA ~140]→[TRANS ~105]→[LIMPIA ~370: enfriam.+trozado mín.+garras+empaque]→[FRÍA ~100]→[1 dock]
                                     │ personal polivalente: vestuario intermedio crítico (09A §4)
  [SUBPRODUCTOS ~50 + playa]   [UTILITIES ~300]   [PERSONAL/ADMIN ~270]   [EFLUENTES]   [RESERVA: líneas/salas/cámaras/rendering]

5.000 — ~2.600 m² (1.700–4.100) · ~2,3 ha (0,9–6,5)
  igual secuencia; garras y menudencias pueden compartir ambiente con trozado (09A §4); túnel estático

10.000 — ~4.300 m² (2.700–6.900) · ~3,1 ha (1,2–8,7)
  salas dedicadas (trozado, garras, menudencias, empaque); 2 docks; subproductos por canal/bomba con retiro continuo

20.000 — ~7.500 m² (4.700–12.300) · ~4,4 ha (1,7–12,8)
  una línea rápida o dos líneas (§6); 3 docks; ~12 t/día de sólidos; congelado continuo si el perfil lo exige
```

## 8. Alertas activas en la referencia (por qué hay PROXY)

`FOOTPRINT_DESCONOCIDO` (DPV-12C-01) · `DOTACION_PROXY` (DPV-12C-02) · `AVES_POR_CAMION` y `T_POR_CAMION` (DPV-084, DPV-036) · `ENFRIAMIENTO_NO_DEFINIDO` (DEC-026) · `TECNOLOGIA_EFLUENTES_NO_DEFINIDA` (DEC-043) · `CLOACA_DEPENDE_DEL_SITIO` · `LODOS_PENDIENTE` (DPV-114) · `CARGA_FRIGORIFICA_PENDIENTE` (DPV-109) · `GENERADOR_PENDIENTE` (DEC-047) · `OBJETIVO_EXPANSION_NO_DEFINIDO` (DEC-12C-02) · `RENDERING_RESERVA` (DEC-027) · `RETIRO_PENDIENTE`, `BUFFER_PROXY`, `FOS_PENDIENTE` (DPV-12C-05). En modo estricto (`estricto=True`), 21 áreas quedan PENDIENTE y los totales no se calculan: es la forma de ver **cuánto del resultado depende de proxies**.
