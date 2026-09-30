# Propuestas de actualización de registros globales — sesión 09C (utilities)

**Fecha:** 2026-09-30 · Sesión en paralelo: **no se editaron** `00_gestion_proyecto/`, `25_fuentes/registro_fuentes.csv` ni `25_fuentes/bibliografia.md`. Este archivo contiene lo que debe incorporarse al integrar la sesión.

> **IDs provisionales:** para evitar colisiones con otras sesiones paralelas, los registros nuevos usan IDs `SUP-09C-xx`, `DPV-09C-xx`, `DEC-09C-xx` y `FTE-09C-xx`. Al integrar, asignar el siguiente número libre de cada registro (al cierre de esta sesión los últimos eran SUP-060, DPV-087, DEC-036 y FTE-193) y reemplazar los IDs provisionales en `11_agua_efluentes/` y `12_energia_frio/` (búsqueda de texto `09C-`).

---

## 1. `supuestos.md` — nuevos

| ID provisional | Supuesto | Área | Estado | Relacionado |
|---|---|---|---|---|
| SUP-09C-01 | **Agua industrial por etapa** (L/ave faenada; bajo/medio/alto): recepción 0,5/1/2; escaldado 0,9/1,2/2; desplumado 1/2/3,5; evisceración 4/6/8; lavado final 1,5/3/4,5; chiller 1,9/2,8/4,5; despiece 0,5/1/2; limpieza 3/5/7,5; sanitización 0,7/1/1,5; auxiliares 1/2/2,5 → **15/25/38 L/ave**. Totales calibrados a rangos de EE.UU./Brasil `[PVDP]` (FTE-09C-01 a 04); reparto por etapa sin fuente argentina. **No se usa el agua retenida en producto para calcular consumo** | Agua | Vigente | DPV-067 |
| SUP-09C-02 | **Agua descargada** = 80/88/95 % del agua utilizada; caudal horario sobre 12 h (8 h netas + 4 h de limpieza) con factor de pico 1,5/1,8/2,2; agua de red a 18 °C | Agua / Efluentes | Vigente | DPV-053, DPV-067 |
| SUP-09C-03 | **Carga específica del efluente crudo** (g/ave, con sangre recuperada al 85 % y sólidos gruesos retirados): DQO 50/100/180; DBO₅ 25/50/90; SST 15/35/80; grasas y aceites 5/11/25; NTK 3/5/8; PT 0,3/0,5/1. DQO de la sangre 0,357 kg/kg (375.000 mg/L ÷ 1,05; FTE-181 `[PVDP]`). La concentración es resultado (carga/caudal), no parámetro | Efluentes | Vigente | DPV-067 |
| SUP-09C-04 | **Pretratamiento y lodos:** remociones de DAF (DBO 60/45/30 %, SST 70/54/38 %, grasas 95/80/63 %, FTE-09C-05 `[PVDP]`), químicos +10/15/25 % sobre la materia seca, flotado al 15/12/10 % de sólidos; lodo aerobio 0,3/0,4/0,5 kg MS/kg DBO removida (95 % de remoción); deshidratado al 20/18/15 % | Efluentes / Lodos | Vigente | DPV-09C-04 |
| SUP-09C-05 | **Electricidad:** indicador de proceso 150/250/450 kWh/t de peso vivo (incluye enfriado de producto fresco; `[PVDP]` FTE-09C-09, 09C-03); congelado 120/190/260 kWh/t (FTE-09C-10 `[PVDP]`); cámaras 0,5/1/2 kWh/(t·día) refrigerado y 1,5/3/5 congelado (sin fuente); aireación 0,7/1,2/2 kWh/kg DBO removida; factor de pico 1,3/1,5/1,8 sobre la media de proceso en 14 h; reparto ilustrativo de consumidores (35 % frío de proceso, 20 % motores, 10 % aire, 10 % bombas, 8 % climatización, 7 % iluminación, 5 % servicios, 5 % otros) solo didáctico | Energía | Vigente | DPV-09C-01 |
| SUP-09C-06 | **Agua caliente:** escaldado a 54/58/62 °C (FTE-09C-11 `[PVDP]`) con factor de pérdidas 1,5/2/3 sobre la reposición; 50/60/70 % del agua de limpieza a 50/55/60 °C; 30/50/70 % del agua de sanitización a 82 °C; rendimiento de generación y distribución 85/75/65 %; PCI gas natural 38,9 MJ/m³, GLP 46 MJ/kg, chip 14 MJ/kg. No incluye vapor de rendering, lavado de cajones ni cocción (cota inferior probable) | Energía térmica | Vigente | DPV-09C-07 |
| SUP-09C-07 | **Frío:** carcasa de 38 °C a 4 °C con cp 3,5 kJ/(kg·K); agua de chiller a 1 °C; cargas adicionales (salas, docks, infiltración) +25/40/60 %; congelado de +4 a −18 °C con cp 1,8 bajo cero, 74 % de agua, latente 334 kJ/kg (FTE-09C-14 `[PVDP]`), factor de túnel 1,2/1,3/1,5 y 20 h/día; COP 4/3/2,3 enfriado y 1,8/1,4/1,1 congelado; kW eléctricos = kW frigoríficos / COP | Frío | Vigente | DPV-09C-02 |
| SUP-09C-08 | **Respaldo:** cargas críticas = cámaras × factor de rearranque 1,3/1,5/2 + 50 % de la aireación media + control 2 %, iluminación de emergencia 1 %, bombeo mínimo 3 % y andén de aves 2 % de la potencia pico de proceso; kVA = kW / 0,8 | Energía | Vigente | DEC-09C-05 |
| SUP-09C-09 | Garras (0/100/100 %) y menudencias (0/50/100 %) congeladas se muestran como **informativas** dentro del comestible: **no se suman** al perfil P1–P3 (SUP-055) para no duplicar | Frío | Vigente | DEC-031, DPV-085 |

## 2. `datos_por_validar.md`

### 2.1 Nuevos

| ID provisional | Dato | Para qué | Fuente sugerida | Prioridad |
|---|---|---|---|---|
| DPV-09C-01 | **Indicadores energéticos de plantas de faena argentinas:** kWh/ave, kWh/t (base declarada), m³ de gas/ave, desglose por uso, potencia contratada | Reemplazar SUP-09C-05 y 09C-06 | Plantas existentes, INTI, distribuidoras, cámaras | Importante antes de invertir |
| DPV-09C-02 | **Balance frigorífico de proveedor** por escala (2.500–20.000) y perfil (P1–P3): kWf y kWe por carga, COP con temperatura de verano del sitio | Reemplazar SUP-09C-07; resolver la brecha bottom-up vs indicador | Dos o más proveedores de refrigeración industrial | Importante antes de invertir |
| DPV-09C-03 | **Normativa argentina de seguridad** de instalaciones frigoríficas con amoníaco y CO₂; cronograma nacional de reducción de HFC (Kigali, ley aprobatoria y resoluciones); disponibilidad de técnicos y repuestos por zona | Evaluar refrigerantes (DEC-09C-04) | Ministerio de Ambiente, SRT, normas IRAM, cámaras de frío | Útil para optimizar |
| DPV-09C-04 | **Lodos y flotados:** receptores (rendering, compostaje, biodigestión), condiciones de aceptación (químicos, % de sólidos), normativa de uso agronómico y disposición | Cerrar el destino del ~40 % adicional de sólidos | Rendering (DPV-065), autoridades ambientales, SENASA (FTE-188) | Importante antes de invertir |
| DPV-09C-05 | **Productos de limpieza, sanitizantes y antimicrobianos** admitidos en plantas de aves en Argentina y su efecto sobre el tratamiento biológico | Caracterización del efluente y compatibilidad con el biológico | SENASA, proveedores de químicos | Útil para optimizar |
| DPV-09C-06 | **Demanda térmica real** (vapor y agua caliente) y **duración de la ventana de limpieza** en plantas argentinas | Reemplazar SUP-09C-06; pico térmico | Plantas existentes, proveedores de calderas | Útil para optimizar |

### 2.2 Anotaciones a registros existentes

| Registro | Anotación propuesta (sesión 09C, 2026-09-30) |
|---|---|
| DPV-052 (energía en zonas rurales) | Potencia de referencia por escala (medio): ~0,2 / 0,4 / 0,8 / 1,6 MW de pico a 2.500 / 5.000 / 10.000 / 20.000 aves/día (el doble en nivel alto); pedir también historial de cortes y factibilidad de gas natural. Ver `11_agua_efluentes/conclusiones_agua_efluentes.md` §6 |
| DPV-053 (agua en zonas candidatas) | Caudal de referencia: 62 / 125 / 250 / 500 m³/día (medio) y ~9 / 19 / 38 / 75 m³/h de pico; análisis según CAA art. 982 (As ≤ 0,01 mg/L `[PVDP]`, FTE-09C-16) |
| DPV-061 (normativa de agua en carne aviar) | Agregar: reúso de agua admitido (chiller → escaldado, transporte de vísceras) y reposición mínima exigida en chiller/escaldador en Argentina (EE.UU.: 0,5 gal/ave en chiller, FTE-09C-18 `[PVDP]`) |
| DPV-067 (carga de efluentes por ave) | Rango de trabajo 50/100/180 g DQO/ave y 15–38 L/ave (SUP-09C-01, 09C-03); límite ilustrativo ADA 336/03 PBA: DBO 50 y DQO 250 mg/L a pluvial, SSEE 50 mg/L a cloaca (FTE-09C-08 `[PVDP]`); faltan Santa Fe, Córdoba, Entre Ríos y Chaco; única fuente argentina hallada: FTE-09C-07 (SEDICI-UNLP), prioridad de lectura |
| DPV-078 / DPV-085 (vida útil; refrigerado/congelado) | El perfil multiplica ×5 la congelación diaria y el stock congelado a igual escala (`12_energia_frio/congelado_almacenamiento.md`) |
| DPV-087 (terreno y servicios) | Agregar superficie para tratamiento de efluentes (lagunas vs compacto) y distancia a viviendas (olor, amoníaco) |
| DPV-009 (acceso a fuentes) | Séptima sesión con `EGRESS_BLOCKED` (aidic.it, frontiersin.org, thepoultrysite.com, sedici.unlp.edu.ar, fieldreport.caes.uga.edu, extension.okstate.edu, ina.gov.ar) |

## 3. `decisiones_pendientes.md`

### 3.1 Nuevas

| ID provisional | Decisión | Prioridad | Depende de | Carpeta |
|---|---|---|---|---|
| DEC-09C-01 | **Estrategia de efluentes:** destino del vuelco (cloaca / pluvial / curso / suelo) y tren de tratamiento (pretratamiento + anaerobio / aerobio / combinado); reserva de terreno para ampliar | Alta (condiciona localización) | DPV-067, DPV-087, DEC-003, escala | `11_agua_efluentes` |
| DEC-09C-02 | **Prevención en origen:** meta de recuperación de sangre y transporte de plumas y vísceras en seco vs hidráulico | Media | DEC-027, DPV-080 | `11_agua_efluentes`, `05_proceso_industrial` |
| DEC-09C-03 | **Fuente térmica** (gas natural, GLP, electricidad/bomba de calor, biomasa, biogás, recuperación de calor) y acumulación de agua caliente | Media | DPV-052, DPV-09C-06 | `12_energia_frio` |
| DEC-09C-04 | **Sistema de refrigeración y refrigerante** (NH₃, CO₂, cascada, indirecto, HFO) y su modularidad | Media | DPV-09C-02, DPV-09C-03, perfil de frío (DPV-085) | `12_energia_frio` |
| DEC-09C-05 | **Política de respaldo:** qué operaciones deben seguir durante un corte (solo cargas críticas / terminar lote / planta completa), N+1, autonomía | Media | DPV-052 | `12_energia_frio` |
| DEC-09C-06 | **Destino de lodos y flotados** (rendering, compost, biodigestión, disposición), integrado con el destino de subproductos | Media | DEC-027, DPV-09C-04 | `11_agua_efluentes`, `07_subproductos` |

### 3.2 Anotaciones

| Registro | Anotación propuesta |
|---|---|
| DEC-003 (localización) | Agua (caudal horario y calidad), permiso y límites de vuelco, potencia eléctrica, gas y calidad de red son **criterios de localización**: pueden limitar la escala del sitio (`11_agua_efluentes/guia_ramiro.md` §10) |
| DEC-026 (método de enfriamiento) | El agua de reposición del chiller por inmersión es ~2,8 L/ave (~11 % del agua de la planta) y ~41 % de la carga frigorífica del enfriado fresco en el modelo; el aire elimina esa agua pero agrega ventiladores y tiempo (no comparado todavía) |
| DEC-035 (sobredimensionar vs módulos) | Candidatos a **dejar preparado**: captación y reserva de agua, troncales de efluentes, terreno del tratamiento, sala de máquinas de frío, acometida eléctrica y de gas; **por módulos**: trenes de tratamiento, compresores, túneles, cámaras, generadores |
| DEC-033 (arquitectura de crecimiento) | Verificar en cada etapa que agua, efluentes, potencia y frío del sitio acompañen la escala |

## 4. `glosario.md` — términos nuevos

| Término | Definición propuesta |
|---|---|
| L/ave | Litros de agua utilizada por ave faenada; indicador de eficiencia hídrica de la planta. No incluye el agua retenida en producto |
| Agua utilizada / descargada / retenida | Utilizada: toda el agua que entra a la planta. Descargada: la que sale como efluente. Retenida: la que queda en el producto o subproducto (balance de masa). No se suman ni se sustituyen |
| DBO₅ | Demanda bioquímica de oxígeno a 5 días: oxígeno que consumen microorganismos para degradar la materia orgánica biodegradable (mg/L) |
| DQO | Demanda química de oxígeno: oxígeno necesario para oxidar químicamente toda la materia orgánica (mg/L); siempre ≥ DBO |
| SST | Sólidos suspendidos totales (mg/L) |
| Grasas y aceites / SSEE | Sustancias solubles en éter etílico: medida de grasas en el efluente |
| NTK | Nitrógeno total Kjeldahl: nitrógeno orgánico + amoniacal |
| Carga orgánica | Masa de DBO o DQO por día (kg/día) = concentración × caudal; dimensiona el tratamiento |
| Carga específica | Carga por ave faenada (g/ave) |
| DAF | Flotación por aire disuelto: pretratamiento que separa grasas y sólidos finos con microburbujas; genera un flotado (lodo) |
| Ecualización | Tanque que amortigua variaciones de caudal, carga, pH y temperatura del efluente |
| Tratamiento anaerobio / aerobio | Degradación biológica sin oxígeno (lagunas, UASB; produce biogás, poco lodo) o con oxígeno (lodos activados, SBR; más energía y lodo, mejor salida) |
| UASB | Reactor anaerobio de manto de lodo de flujo ascendente |
| kW / kWh | Potencia (tasa instantánea) / energía (potencia × horas) |
| kW frigorífico (kWf) / kW eléctrico (kWe) / COP | Calor extraído por el sistema de frío / potencia consumida por los compresores / kWf ÷ kWe |
| TR (tonelada de refrigeración) | 3,517 kW frigoríficos |
| Capacidad de congelación vs capacidad de almacenamiento | t/día que túneles/IQF llevan a −18 °C vs t que las cámaras guardan al mismo tiempo |
| Cargas críticas | Consumos eléctricos que deben mantenerse durante un corte (frío de cámaras, control y seguridad, emergencia, efluentes, agua mínima, ventilación de aves) |
| N+1 | Redundancia con un equipo más de los necesarios |
| PCI | Poder calorífico inferior de un combustible (MJ/m³ o MJ/kg) |

## 5. `estado_proyecto.md` — propuesta de hito

> **2026-09-30 — Sesión 09C: modelo preliminar de utilities** (`11_agua_efluentes`, `12_energia_frio`). Agua 15/25/38 L/ave; efluente ~1.000 kg DQO/día a 10.000 aves/día (medio); ~0,8 kWh/ave; ~0,8 MW de pico; ~235 kWf de enfriado; congelado dominado por el perfil (P1–P3), no por la escala; respaldo crítico ~10 % de la potencia. Modelo `modelo_utilities.py` (20 tests, 9 mutaciones) que lee `escenarios_escala.csv`. Todas las fuentes `[PVDP]`. Sin equipos, sin CAPEX, sin ubicación. Calidad: MEDIA como método, BAJA como evidencia.

## 6. `25_fuentes/`

- Incorporar `FTE-09C-01` a `FTE-09C-19` de [`fuentes_09C.csv`](fuentes_09C.csv) a `registro_fuentes.csv` con numeración definitiva (mismas columnas) y agregar sus entradas a `bibliografia.md` en la sección de agua/efluentes/energía/frío.
- Anotar en **FTE-181** (efluentes de faena) que se usó para la carga específica y la DQO de la sangre en `11_agua_efluentes` (sin cambiar su estado `[PVDP]`).
- Anotar en **FTE-135** que la exigencia de ≤ −18 °C se usa como temperatura final de congelado en `12_energia_frio`.
- Anotar en **FTE-157** (mortandades por fallas eléctricas) su uso en `12_energia_frio/respaldo_energia.md`.
