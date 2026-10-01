# Actualizaciones de gestión pendientes de reconciliación — sesión 12C (layout y obra civil)

**Fecha:** 2026-10-01 · Sesión ejecutada **en paralelo** con 12A (localización) y 12B (logística).

> **Por qué existe este archivo:** por instrucción del promotor, esta sesión **no modificó** `00_gestion_proyecto/` ni `25_fuentes/`, ni archivos de 12A o 12B. Todo lo que normalmente se registraría allí está aquí para la **reconciliación central**. Los IDs son **provisionales** (`SUP-12C-##`, `DPV-12C-##`, `DEC-12C-##`, `FTE-12C-###`); al reconciliar se reasignan al siguiente número libre y se reemplazan por búsqueda de texto en `09_layout_obra_civil/` (incluido `modelo_superficies.py`, que cita los IDs en sus parámetros).
> Últimos IDs vistos en los registros centrales al iniciar la sesión: **SUP-077, DPV-115, DEC-049, FTE-268**.
> Fuentes provisionales: [`fuentes_12C.csv`](fuentes_12C.csv) (mismas columnas que `25_fuentes/registro_fuentes.csv`).
> **Posibles solapamientos con 12A/12B** a revisar en la reconciliación: DPV-12C-05 (retiros, FOS) con localización; DPV-12C-03 (transporte del personal) y los proxies de camiones (DPV-084) con logística.

---

## 1. Supuestos nuevos → `00_gestion_proyecto/supuestos.md`

| ID provisional | Supuesto | Ámbito | Estado |
|---|---|---|---|
| SUP-12C-01 | **[SUPUESTO DE ORDEN DE MAGNITUD — PROXY]** Áreas dominadas por equipos sin huella conocida: m² = k × (driver/1.000)^0,8 con mínimo funcional; k y mínimos por área en `modelo_superficies.py` (`K`), **sin fuente**. Se reemplazan por huella × envolvente cuando haya layouts de proveedores | Layout | Vigente (proxy) |
| SUP-12C-02 | **Recepción:** espera de 1 / 1,5 / 2 h; bahías = ⌈ritmo × espera ÷ aves por camión⌉ + 1; 70 / 90 / 120 m² por bahía cubierta y ventilada | Layout | Vigente |
| SUP-12C-03 | **Líneas y automatización:** dos líneas = cada una a la mitad del ritmo, × 1,05 / 1,10 / 1,15 por pasillo de separación; factor de superficie por automatización en salas con puestos: manual 1,20 · semi 1,00 · auto 0,90 (débil) | Layout | Vigente |
| SUP-12C-04 | **Enfriamiento:** m² por carcasa simultánea: inmersión 0,15 / 0,20 / 0,28; aire 0,10 / 0,14 / 0,20 (residencias de SUP-09A-04 → reconciliado); **sin método decidido se reserva el mayor** | Layout | Vigente |
| SUP-12C-05 | **Circulación interna de proceso** 15 / 22 / 30 % de las salas; **depósito de envases** 5 / 8 / 12 m² por t/día de comestible | Layout | Vigente |
| SUP-12C-06 | **Frío (conversión t → m²):** factor de pico de stock 1,15 / 1,3 / 1,5; densidad de piso refrigerado 1,0 / 0,7 / 0,5 t/m² y congelado 1,75 / 1,25 / 0,9 t/m² (de 4–7 m³ brutos/t × 3,5–7 m útiles, `[PVDP]`); antecámaras 20–40 %; túnel 6 / 9 / 14 m² por t/día (proxy). Las t provienen de 09C sin cambios | Layout / frío | Vigente |
| SUP-12C-07 | **Expedición:** pico de despacho 1,0 / 1,2 / 1,5; 4 / 3 / 2 cargas por dock y día; 35 / 45 / 60 m² por dock interior; 150 / 200 / 250 m² de maniobra por dock | Layout / logística | Vigente (revisar con 12B) |
| SUP-12C-08 | **Subproductos:** cámara de subproductos perecederos 0,5 / 1 / 3 días a 0,7 / 0,5 / 0,35 t/m²; decomisos 6–12 m²; sala de subproductos 10 / 15 / 22 m² por t/día de sólidos | Layout | Vigente |
| SUP-12C-09 | **Servicios:** proxies de sala de máquinas de frío (12–25 % de m² de frío, mín. 40–80), caldera, aire, sala eléctrica, generador, mantenimiento, repuestos, químicos, laboratorio, lavandería; reserva de agua 0,5–1,5 días | Layout | Vigente (proxy) |
| SUP-12C-10 | **[PROXY]** **Dotación solo para superficies:** 10–20 + 0,05–0,12 × ritmo (aves/h) × automatización (1,35 / 1,0 / 0,75) × configuración (A 0,9 / B 1,0 / C 1,3) personas por turno; vestuarios 1,0–1,7 m²/persona (+40–80 % de lockers por 2.º turno); comedor 33–50 % simultáneo × 1,2–1,8 m². **No es dotación** | Layout / RR. HH. | Vigente (proxy hasta `18_recursos_humanos`) |
| SUP-12C-11 | **Exteriores:** 150–250 m² por camión en playa; lavado 100–160 m² por plataforma (8–12 camiones/plataforma/día); estacionamiento: 20–50 % del personal motorizado × 20–28 m²; circulación pesada 25 / 35 / 50 % de los m² cubiertos | Layout | Vigente |
| SUP-12C-12 | **Efluentes (sin elegir tecnología):** pretratamiento, ecualización (30–70 % del caudal diario), DAF (4–6 m³/m²·h), biológico por tecnología (FTE-12C-006 `[PVDP]`), lodos proxy (09C pendiente); DBO/DQO = el **mayor** de los dos métodos de 09C | Layout / efluentes | Vigente |
| SUP-12C-13 | **Reserva de expansión:** con escala objetivo = Σ max(0, área objetivo − actual) por categoría; sin objetivo = 25 / 50 / 100 % de lo operativo (con alerta); reserva de rendering 40–90 m² por t/día de rendering potencial (mín. 300–600 m²), solo terreno | Layout / expansión | Vigente |
| SUP-12C-14 | **Factor de envolvente** de sala sobre huella de equipos: 2,2 / 2,8 / 3,5 | Layout | Vigente |
| SUP-12C-15 | **Terreno:** rectángulo de relación 1,5; margen perimetral = retiro (5 / 10 / 15 m, supuesto) + buffer (10 / 20 / 40 m, proxy); si se conoce el FOS, terreno ≥ huella ÷ FOS | Layout / localización | Vigente (revisar con 12A) |
| SUP-12C-16 | Las **nueve zonas de layout** (sucia, transición, limpia, fría, despacho, subproductos, utilities, personal, administrativa) son **categorías de trabajo**, no categorías regulatorias | Layout / normativa | Vigente |
| SUP-12C-17 | **Expansión "a lo ancho":** las ampliaciones se ubican en paralelo o lateralmente a cada zona, nunca intercaladas en la secuencia sucia → limpia → fría → despacho; clasificación S/P/M/D de [`estrategia_expansion.md` §2](estrategia_expansion.md) como hipótesis | Layout / expansión | Vigente |

**Notas a supuestos existentes:**

- **SUP-055 / SUP-056** (perfiles e inventario): agregar "12C: convertidos a m² de cámara en `09_layout_obra_civil/modelo_superficies.py` sin cambiar las t (test T11)".
- **SUP-059** (modularidad A/B/C de 23): agregar "12C: traducida a reglas de layout (S/P/M/D) y al resultado de que el terreno de la escala final es el mismo en todas las trayectorias (`estrategia_expansion.md` §1)".

## 2. Datos por validar nuevos → `00_gestion_proyecto/datos_por_validar.md`

| ID provisional | Dato | Por qué importa | Dónde buscar | Prioridad (escala del plan de campo) |
|---|---|---|---|---|
| DPV-12C-01 | **Huellas de equipos por área** (layout con cotas, altura libre, peso, fosos, vano de montaje, servicios por punto), por escala y para la ampliación | Reemplaza los proxies de 23 áreas (estado PROXY) | RFQ lote 1 y 8 (`08_maquinaria/plan_rfq.md`); tabla en `programa_areas.md` §4 | N2 (antes de anteproyecto) |
| DPV-12C-02 | **Dotación por turno, por zona (sucia/limpia) y por sexo** | Vestuarios, comedor, lavandería, estacionamiento | `18_recursos_humanos`; visitas a plantas | N2 |
| DPV-12C-03 | **Modo de transporte del personal** (colectivo propio, transporte público, autos, motos) en zonas candidatas | Estacionamiento (hasta ~2.000 m² medio a 20.000 aves/día) | Encuestas locales; 12B | N3 |
| DPV-12C-04 | **Requisitos edilicios del servicio oficial** (oficina, vestuario, sanitario, sala de decomisos, puestos de inspección, iluminación) | Áreas obligatorias de la zona administrativa y de transición | SENASA; Decreto 4238/68 original (complementa DPV-090) | N2 |
| DPV-12C-05 | **Retiros, FOS, FOT, alturas máximas y distancias a viviendas** por sitio candidato | Retiros y buffers son ~55 % del terreno medio en el modelo | Municipios (código de planeamiento); ficha de terreno (complementa DPV-106, DPV-087; **posible solapamiento con 12A**) | N2 (antes de comprar terreno) |
| DPV-12C-06 | **Densidad de estiba, sistema de racks y altura útil** de cámaras para el formato de caja/pallet del proyecto | Convierte t en m² de cámara | Proveedores de frío y racks (complementa DPV-109) | N3 |
| DPV-12C-07 | **Superficie cubierta y de terreno real de plantas argentinas** por escala, con qué incluye cada m² | Calibrar o descartar los proxies; leer en original FTE-12C-001 a 003 y 009 | Visitas (`05_proceso_industrial/guia_visita_planta.md`); documentos originales | N2 |
| DPV-12C-08 | **Superficie y geometría del tratamiento de efluentes** propuesto por proveedores para cada tecnología y escala | El terreno de efluentes varía ~35–40 veces entre compacto y lagunas | Proveedores (RFQ de tratamiento); complementa DPV-114 y DEC-043 | N2 |
| DPV-12C-09 | **Requisitos de bomberos e higiene y seguridad**: reserva de incendio, sectorización, salidas, materiales de paneles | Tanques, muros cortafuego, superficies | Bomberos y normativa provincial (complementa DPV-106) | N3 |
| DPV-12C-10 | **Requisitos de layout para exportación (UE) y Halal**: segregación de lotes, salas dedicadas, aturdido | Espacio adicional a reservar | SENASA; auditorías de destino (complementa DPV-034, DEC-012) | N4 |
| DPV-12C-11 | **Requisitos de lavado y desinfección de camiones** de aves vivas (Res. SENASA 723/2025, `[PVDP]`) | Plataforma de lavado y su efluente | Texto original de la resolución | N3 |

**Notas a datos existentes:**

- **DPV-084** (capacidades de vehículos): agregar "12C: aves por camión y t por camión definen bahías de recepción, docks y playas; hoy proxies (alertas `AVES_POR_CAMION`, `T_POR_CAMION`)".
- **DPV-087** (terreno y servicios): agregar "12C: terreno conceptual 0,8–5,3 / 0,9–6,5 / 1,2–8,7 / 1,7–12,8 ha (2.500 / 5.000 / 10.000 / 20.000 aves/día, sin objetivo); ~1,4 / 3,3 / 8,2 ha si se reserva para 20.000 desde cualquier etapa; lagunas: hasta ~45 ha (rango alto a 20.000)".
- **DPV-090** (Decreto 4238/68): agregar "12C: lista de requisitos edilicios a leer en `09_layout_obra_civil/requerimientos_obra_civil.md` §1–§3".
- **DPV-109** (balance frigorífico): agregar "12C: la sala de máquinas de frío es proxy hasta tener carga y equipos".
- **DPV-114** (lodos): agregar "12C: área de lodos y flotados en proxy (`efl_lodos`)".
- **DPV-115** (revisión del anteproyecto por SENASA): agregar "12C: la matriz de cruces de `flujos_layout.md` §10 es la lista de control previa".
- **DPV-009** (verificación documental): una sesión más con acceso directo bloqueado (WebFetch `EGRESS_BLOCKED` en meridianmachine.com); WebSearch funcionó.

## 3. Decisiones pendientes nuevas → `00_gestion_proyecto/decisiones_pendientes.md`

| ID provisional | Decisión | Prioridad | Depende de | Carpeta | Nota |
|---|---|---|---|---|---|
| DEC-12C-01 | Definir la **forma conceptual de la nave** (lineal, U, L, peine) y el lado de cada frente de ampliación | Media | DEC-033, DEC-038, terreno (DEC-003) | `09_layout_obra_civil` | Solo con escala y terreno; no en Fase 0 |
| DEC-12C-02 | Definir la **escala objetivo para la que se reserva el terreno** (independiente de la escala de arranque) | **Alta** (antes de comprar terreno) | DEC-033, DEC-035, DPV-083, DPV-087 | `09_layout_obra_civil` / `23_plan_expansion` | Con objetivo 20.000, el terreno es ~3,3 ha medio en todas las trayectorias |
| DEC-12C-03 | Definir si el **congelado** de la etapa inicial es **propio o tercerizado** | Media | Perfil de destino (SUP-055, DPV-085), DEC-046 | `12_energia_frio` / `09_layout_obra_civil` | Si es tercerizado, reservar espacio para internalizarlo |
| DEC-12C-04 | Definir **laboratorio de autocontrol propio o tercerizado** | Baja | DEC-009, exigencias de clientes | `09_layout_obra_civil` / `16_normativa_senasa` | Cambia poco la superficie |
| DEC-12C-05 | Definir si se **reserva terreno para rendering** futuro y dónde | Media | DEC-027, DPV-065, distancias a vecinos | `09_layout_obra_civil` / `07_subproductos` | Reservar es barato; sin reserva la opción desaparece |

**Notas a decisiones existentes:**

- **DEC-003** (localización): agregar "12C: el terreno necesario es criterio de localización: ver rangos en `09_layout_obra_civil/layouts_por_escala.md` §1 y §4".
- **DEC-035** (sobredimensionar vs modular): agregar "12C: traducción espacial en `estrategia_expansion.md` §2 (S/P/M/D) y lista de 12 puntos difíciles de modificar (§5)".
- **DEC-038** (líneas): agregar "12C: comparación espacial una vs dos líneas (+~21 % en salas de línea) en `layouts_por_escala.md` §6; sin recomendación".
- **DEC-043** (efluentes): agregar "12C: el tren de tratamiento cambia el terreno hasta ~35–40 veces en el biológico (lagunas vs compacto); no puede decidirse separado del terreno".
- **DEC-026** (enfriamiento): agregar "12C: mientras no se decida, el layout reserva el espacio del método más extenso (aire)".

## 4. Glosario → `00_gestion_proyecto/glosario.md`

| Término | Definición propuesta |
|---|---|
| Layout | Disposición de áreas, flujos y circulaciones de una planta y su terreno |
| Footprint (huella) | Superficie de piso que ocupa un equipo |
| Factor de envolvente | Relación entre la superficie de la sala y la huella de los equipos que contiene |
| Buffer | Espacio de amortiguación de proceso (stock, espera) o de terreno (franja libre) |
| FOS / FOT | Factor de ocupación del suelo (fracción edificable en planta) / total (m² edificables totales ÷ terreno) |
| m² construidos / operativos / terreno | Ver `09_layout_obra_civil/programa_areas.md` §1 |
| Expansión modular | Crecimiento por bloques que se agregan sin desarmar los existentes |

## 5. Estado del proyecto → `00_gestion_proyecto/estado_proyecto.md`

Propuesta de fila del tablero: **Layout y obra civil (`09`)** — Modelo preliminar **completado** v1.0 (programa de 54 áreas, nueve zonas, nueve flujos, superficies en rango para cuatro escalas, terreno conceptual, estrategia de expansión; `modelo_superficies.py` con 19 tests y 7/7 mutaciones detectadas) · Evidencia de campo **pendiente** (huellas, dotación, retiros, plantas reales) · Síntesis: [`../09_layout_obra_civil/conclusiones_layout.md`](conclusiones_layout.md). **Sin planos, sin CAPEX, sin terreno ni escala elegidos.**
