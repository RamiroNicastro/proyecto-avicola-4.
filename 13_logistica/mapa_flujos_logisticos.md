# Mapa de flujos logísticos — cadena avícola completa

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Fase 0 (prefactibilidad) · Sesión **12B** (en paralelo con 12A Localización y 12C Layout/Obra civil)

> **Pregunta:** ¿qué se mueve, cuánto, desde dónde, hacia dónde, con qué frecuencia y bajo qué restricciones?
> **No responde** cuánto cuesta: no hay fletes, tarifas, CAPEX ni OPEX (fase posterior). **No** se elige escala, localización, radio, transportista ni flota.
> **Cifras:** [`modelo_logistica.py`](modelo_logistica.py) → [`escenarios_logistica.csv`](escenarios_logistica.csv). Todas son `[ESTIMACIÓN]` sobre supuestos ya registrados (SUP-019 a SUP-077) y los provisionales SUP-12B-01 a 16 ([`actualizaciones_gestion_12B.md`](actualizaciones_gestion_12B.md)). Referencia de las tablas: perfil y desempeño **medios** (2,9 kg vivo, DOA 0,3 %), balance v1.1, configuración **B trozado**, **5 días de faena por semana (250 d/año)**. Ninguna cifra proviene de datos de campo argentinos.

---

## 1. Esquema general

```
                         INSUMOS A GRANJAS                                  INSUMOS A PLANTA
  Incubadora ──pollitos BB (clima)──┐                       Envases, cajas, film, etiquetas ──┐
  Fábrica de alimento ──granel──────┤                       Pallets ──────────────────────────┤
  Cama (viruta / cáscara) ──────────┤                       Limpieza y sanitizantes ──────────┤
  Vacunas y medicamentos (frío) ────┤                       Repuestos, gas, combustible ──────┤
  Gas / combustible ────────────────┘                                                         │
                                   ▼                                                          ▼
                          GRANJAS (N, radio R) ══ AVES VIVAS (camión jaula, noche) ══► PLANTA DE FAENA
                                   │  ▲                                                       │
       aves muertas en granja,     │  └── camión vacío + lavado y desinfección ◄──────────────┤
       cama usada (salen de granja)▼                                                          │
                                                                                              │
     ┌────────────────────────────── PRODUCTO TERMINADO ──────────────────────────────────────┤
     │  REFRIGERADO (días)                          CONGELADO (meses)                          │
     │   ├─► CD del cliente ──► tiendas (cliente)    ├─► mayorista / industria                 │
     │   ├─► cross-dock (AMBA) ──► tiendas           ├─► depósito / consolidación ──► puerto   │
     │   ├─► tiendas directo                         │        ──► contenedor reefer ──► buque  │
     │   ├─► mayorista / distribuidor               │                                         │
     │   ├─► carnicerías / pollerías (vía distrib.) │                                         │
     │   ├─► gastronomía                             │                                         │
     │   └─► elaborador / industria                  │                                         │
     └──────────────────────────────────────────────────────────────────────────────────────────┤
                                                                                              │
     SUBPRODUCTOS (horas) ── plumas (G1) · sangre (G2, cisterna) · vísceras + cabezas (G3) ·   │
                             decomisos + contenido GI (G4) · DOA ─► rendering / receptor ◄─────┘
     COPRODUCTOS COMESTIBLES (frío) ── garras · menudencias · carcasa · cuello ─► canales / export / rendering si no hay comprador
     RESIDUOS ── lodos (PENDIENTE, 11) · residuos generales · envases de insumos
```

**Tres "relojes" distintos** gobiernan la logística: **horas** para aves vivas y subproductos crudos (ayuno, bienestar, degradación), **días** para el refrigerado (vida útil corta, SUP-051), **semanas a meses** para el congelado y la exportación (acumulación de lotes). Mezclarlos en un mismo plan de transporte es el error más caro.

## 2. Tabla maestra de flujos (t/día operativo salvo indicación)

| # | Flujo | Desde → hacia | 2.500 | 5.000 | 10.000 | 20.000 | Frecuencia | Restricción dominante | Vehículo | Dato faltante |
|---|---|---|---|---|---|---|---|---|---|---|
| I1 | **Pollitos BB** (pollitos/semana plena) | Incubadora → granjas | 13.197 | 26.395 | 52.790 | 105.580 | Por lote de granja (todo dentro-todo fuera) | Clima interior del camión, horas de viaje, calidad del pollito | Camión climatizado de la incubadora | Capacidad (DPV-12B-15), distancia (sin incubadora identificada, DPV-047) |
| I2 | **Alimento balanceado** (t/día, 7 d de entrega) | Fábrica → silos de granja | 8,8 | 17,7 | 35,3 | 70,6 | ~3 / 5 / 9 / 18 entregas/semana (granelero de ~28 t, `[ESTIMACIÓN]`) | **Mayor flujo físico del sistema**; bioseguridad en cada entrada | Granelero (tolva) | Capacidad real (DPV-084), ubicación de fábrica (DEC-024) |
| I3 | Cama (viruta, cáscara de arroz) | Proveedor → granjas | PENDIENTE | | | | Por lote o reutilización (retiro total 1/año o cada 5 crianzas, `[PVDP]` FTE-147) | Material disponible en la zona | Volcador / jaula | kg/m² y material (DPV-12B-05) |
| I4 | Vacunas y medicamentos | Laboratorio/distribuidor → granjas | Masa baja | | | | Por lote / plan sanitario | **Cadena de frío** (rango a confirmar con el laboratorio) | Utilitario refrigerado | — (no dimensiona flota) |
| I5 | Envases, film, cajas, etiquetas | Proveedores → planta | PENDIENTE | | | | Semanal (stock de insumos) | Espacio de depósito (12C) | Camión de carga general | kg de envase/kg de producto (DPV-12B-04) |
| I6 | Pallets | Proveedor / pool → planta; retorno desde clientes | 12 · 8 · 6 pallets/día con 500 · 750 · 1.000 kg/pallet (barrido) a 2.500; ×2 / ×4 / ×8 | | | | Diaria (salida); retorno según cliente | Pallet retornable o exigido por el supermercado | — | kg/pallet y estándar de la red (DPV-12B-04, DPV-12B-09) |
| I7 | Insumos de limpieza y sanitizantes | Proveedor → planta | PENDIENTE | | | | Semanal | Almacenamiento de químicos (12C) | Carga general / peligrosa | DPV-112 (químicos admitidos) |
| I8 | Repuestos | Proveedores → planta | Masa baja | | | | Bajo demanda | **Tiempo de reposición** de críticos (cuchillas, motores, compresores) | Courier / flete | Stock crítico (08) |
| I9 | Combustible y gas | Distribuidor → planta, granjas, flota | PENDIENTE | | | | Según consumo | Disponibilidad de gas natural (DPV-052) | Cisterna | Consumo L/km por vehículo (DPV-12B-06) |
| V1 | **Aves vivas** (t vivas cargadas/día) | Granjas → planta | 7,3 | 14,5 | 29,1 | 58,2 | Cada noche/mañana de faena | **Ayuno 8–12 h, bienestar, calor, DOA** | Camión jaula (cajones o módulos) | Aves/camión (SUP-033, DPV-084), radio real (DPV-054) |
| V2 | Camiones vacíos + cajones | Planta → granjas | = V1 en viajes | | | | Tras cada descarga | **Lavado y desinfección antes de nueva carga** (Res. SENASA 723/2025, FTE-234 `[PVDP]`) | Ídem | Tiempo de lavado (DPV-12B-01) |
| P1 | **Producto refrigerado** | Planta → CD / cross-dock / tiendas / mayorista / gastronomía | Según perfil P1–P3: 3,0–5,4 | 6,0–10,8 | 12,0–21,6 | 24,0–43,1 | 5–7 despachos/semana | **Vida útil corta**, ventanas de recepción, temperatura | Furgón refrigerado (troncal o reparto) | Capacidad (DPV-084), ventanas (DPV-036) |
| P2 | **Producto congelado** | Planta → mayorista / industria / depósito | 0,6–2,4 | 1,2–4,8 | 2,4–9,6 | 4,8–19,2 | **Acumulable**: 1–6 despachos/semana | Llenar camión vs stock en cámara | Furgón de congelado | Proporción por canal (DPV-085) |
| P3 | **Exportación** (congelado; P3 = 20 %) | Planta → consolidación → puerto → reefer | 1,2 | 2,4 | 4,8 | 9,6 | 1 / 2 / 4 / 8 contenedores/mes | Lote = contenedor de ~25 t `[PVDP]`; habilitación por destino | Portacontenedor + reefer con genset | Todo el costo y tránsito (DPV-027) |
| S1 | **Plumas húmedas** (G1) | Planta → rendering / receptor | 0,60 | 1,21 | 2,41 | 4,83 | **Diaria** (cada día de faena) | Se deteriora en horas a 1 día `[PVDP]` | Contenedor estanco / volcador | Receptor y distancia (DPV-065) |
| S2 | **Sangre recuperada** (G2) | Planta → rendering | 0,21 | 0,42 | 0,84 | 1,68 | Diaria o refrigerada | Líquido; coagula y fermenta en horas `[PVDP]` | Cisterna | Receptor (DPV-065) |
| S3 | **Vísceras + cabezas + otros C** (G3) | Planta → rendering | 0,52 | 1,04 | 2,08 | 4,17 | Diaria | Horas `[PVDP]`; olores; categoría sanitaria | Contenedor estanco | DPV-065/066 |
| S4 | **Decomisos + contenido GI** (G4) | Planta → digestor / receptor habilitado | 0,19 | 0,37 | 0,75 | 1,50 | Diaria | **Destino restringido por normativa** (DPV-066) | Contenedor segregado | DPV-066 |
| S5 | DOA (aves muertas en transporte; kg/día) | Planta → destino restringido | 22 | 44 | 87 | 174 | Diaria | Fuera del balance (SUP-035) | Con G4 si se admite | DPV-066 |
| S6 | Coproductos comestibles: garras · menudencias · carcasa · cuello | Planta → canales (dentro de P1/P2) | 0,25 · 0,27 · 1,02 · 0,19 | ×2 | ×4 | ×8 | Con el producto (frío) | Sin comprador, la carcasa (1,0–8,2 t/día) baja a rendering (SUP-046) | Refrigerado / congelado | Compradores (DEC-029, DEC-031) |
| S7 | Huesos (solo config. C deshuesado) | Planta → rendering | 0,83 | 1,65 | 3,31 | 6,62 | Diaria | Horas | Contenedor estanco | — |
| R1 | Lodos y flotados | Planta (efluentes) → receptor | PENDIENTE (11_agua_efluentes) | | | | | | | DPV-111, DPV-114 |
| R2 | Mortalidad en granja y cama usada | Granjas → compostaje / disposición | Aves: 5 % de los pollitos (131.975 aves/año a 10.000); kg PENDIENTE | | | | Diaria (aves) / por ciclo (cama) | **Bioseguridad**: no deben salir de la granja sin tratamiento | En granja (compostaje) | DPV-066, DPV-12B-05 |

**Conservación (tests L01–L05):** a 10.000 aves/día entran 29,1 t vivas cargadas (= 29,0 t faenables + 0,09 t de DOA + merma, si se considera); salen 24,0 t de producto comestible (peso comercial, incluye 0,2 kg/ave de agua retenida), 6,1 t de subproductos sólidos y líquidos a retirar y 1,1 t que van al efluente o se pierden (no se transporta). Los coproductos S6 **ya están dentro** de P1/P2: no se suman.

## 3. Flujos por escala: qué cambia

| Indicador físico (referencia: radio 100 km, 5.500 aves/camión, P1, capacidades de barrido) | 2.500 | 5.000 | 10.000 | 20.000 |
|---|---|---|---|---|
| Viajes de aves vivas/día (normal · verano −15 % de carga) | 1 · 1 | 1 · 2 | 2 · 3 | 4 · 5 |
| Ocupación de esos viajes (normal) | **46 %** | 91 % | 91 % | 91 % |
| Entregas de alimento/semana (granelero ~28 t) | 3 | 5 | 9 | 18 |
| Viajes troncales refrigerados/día de despacho (12 t, barrido; 6 d) | 1 (37 %) | 1 (75 %) | 2 (75 %) | 3 (100 %) |
| Contenedores de exportación/mes (si 20 % se exportara) | 1,0 | 2,0 | 4,0 | 8,0 |
| Ocupación de un retiro diario de plumas en vehículo de 10 t (barrido) | **6 %** | 12 % | 24 % | 48 % |

**Lectura:** a escala chica, el problema logístico no es la cantidad de toneladas sino la **falta de densidad**: camiones de aves, de producto y de subproductos salen con poca carga porque los flujos son pequeños pero su frecuencia está fijada por restricciones biológicas (ayuno, vida útil, degradación). A escala grande aparecen otros problemas: coordinación de 3–5 camiones de aves por día con la línea, 18 entregas semanales de alimento y la gestión de una red de 16–64 granjas.

## 4. Restricciones transversales

| Restricción | Afecta a | Estado |
|---|---|---|
| Ayuno total 8–12 h (granja + captura + viaje + espera) | V1 | `[PVDP]` FTE-156; define el viaje admisible (≈ 4,5 h con los supuestos SUP-12B-05) |
| Lavado y desinfección del camión antes de cada nueva carga de animales | V1, V2 | Res. SENASA 723/2025 (FTE-234 `[PVDP]`); texto original no leído (DPV-058, DPV-12B-11) |
| Habilitación sanitaria del vehículo por tipo de carga (animales vivos, carnes, subproductos) | V1, P1–P3, S1–S5 | Res. 723/2025 y Decreto 4238/68 cap. XXVIII (FTE-192 `[PVDP]`); categorías A (equipo de frío) y B (isotérmico) según extracto |
| Temperaturas de transporte refrigerado y congelado | P1–P3 | **No verificadas** (DPV-098); reefer de congelados ≤ −18 °C `[PVDP · débil]` (FTE-135) |
| Pesos y dimensiones de vehículos | Todos | Ley 24.449 art. 53 y Dec. 779/95 Anexo R; Dec. 32/2018 (configuraciones > 45 t) — FTE-12B-003 `[PVDP]` |
| Tiempos de conducción y descanso | P1 (troncal largo), P3 | CCT 40/89: 8 h urbano, 10 h media y larga distancia según extracto (FTE-12B-002 `[PVDP]`) |
| Tránsito federal si la planta y los clientes están en provincias distintas | P1, P2 | Habilitación SENASA (DPV-041, DEC-009) |
| Bioseguridad entre granjas (vehículos, cuadrillas, alimento) | I1, I2, V1, R2 | 03 [`bioseguridad.md`](../03_produccion_primaria/bioseguridad.md) |
| Ventanas de recepción de supermercados / CD | P1 | **Desconocidas** (DPV-036, DPV-12B-09) |

## 5. Documentos de detalle

| Tema | Archivo |
|---|---|
| Aves vivas: viajes, radios, ayuno, DOA, merma, granjas, flota | [`logistica_aves_vivas.md`](logistica_aves_vivas.md) |
| Producto terminado: refrigerado vs congelado, CD vs directo, red ancla A/B/C, inventario | [`logistica_producto_terminado.md`](logistica_producto_terminado.md) |
| Subproductos: retiro diario, cada 2 días, acumulación refrigerada, salida conjunta | [`logistica_subproductos.md`](logistica_subproductos.md) |
| Exportación: etapas y datos para cotizar | [`logistica_exportacion.md`](logistica_exportacion.md) (puertos y documentos: [`../17_exportacion/logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md)) |
| Flota propia / tercerizada / híbrida | [`flota_propia_vs_tercerizada.md`](flota_propia_vs_tercerizada.md) |
| KPI físicos y económicos | [`kpis_logistica.md`](kpis_logistica.md) |
| Riesgos, faltantes y conclusiones | [`conclusiones_logistica.md`](conclusiones_logistica.md) |
| Explicación para el responsable del proyecto | [`guia_ramiro.md`](guia_ramiro.md) |
