# Reconciliación de las sesiones 16 y 17 — CAPEX + OPEX + capital de trabajo

**Fecha:** 2026-10-03 · **Tipo:** sesión administrativa de integración (sesión 18; no investiga temas nuevos) · **Rama:** `ccr-9ff1ac94-0vqhoq` (desde `main` actualizado, commit `7ac9732`, posterior al merge de las sesiones 16 y 17)

> **Qué hace este documento:** integra en los registros maestros (`supuestos.md`, `datos_por_validar.md`, `decisiones_pendientes.md`, `glosario.md`, `estado_proyecto.md`, `matriz_validacion_campo.csv`, `25_fuentes/`) las propuestas con IDs provisionales de **16 Motor CAPEX** (`19_capex/`) y **17 Motor OPEX + capital de trabajo** (`20_opex/`), y deja una **interfaz coherente** para el futuro modelo financiero integral.
> **No** se construyó el modelo financiero; **no** se completaron precios ni salarios; **no** se calcularon ingresos, EBITDA, VAN, TIR ni payback; **no** se eligió escala ni arquitectura; **no** se compararon económicamente arquitecturas; **no** se elevó ninguna evidencia E4/`[PVDP]`; **no** se cerró ninguna decisión; USD 2 M **no** se trata como límite. **No** se modificó la lógica matemática de `modelo_capex.py` ni de `modelo_opex.py`: solo IDs en comentarios, docstrings y textos de salida; los 12 CSV regenerados son **idénticos byte a byte** al reemplazo textual de IDs sobre `HEAD` (§14).

---

## 1. Objetivo

1. Consolidar CAPEX y OPEX en los registros centrales (supuestos, DPV, decisiones, fuentes) eliminando los IDs provisionales activos (`SUP-16/17-##`, `DPV-16/17-##`, `DEC-16/17-##`, `FTE-16/17-###`).
2. Dejar explícito el **estado de la evidencia económica** (§7–8) y del **capital de trabajo** (§9).
3. Garantizar que **C0–CF signifiquen lo mismo** en CAPEX, OPEX y capital de trabajo (§10).
4. Definir la **interfaz al modelo financiero** (§11): qué entrega CAPEX, qué entrega OPEX, cómo se consume por período, frontera fiscal, categorías de ingreso sin precio.
5. Registrar tensiones sin resolverlas (§12) y mostrar por qué hoy **no puede calcularse rentabilidad real** (§13).

| Sesión | Alcance | Carpeta | IDs provisionales | Estado tras la reconciliación |
|---|---|---|---|---|
| **16** | Motor CAPEX v1.2 (procedencia de drivers; semántica de terreno) | `19_capex` | SUP-16-01…25, DPV-16-01…17, DEC-16-01…07, FTE-16-001…007, T16-01…10 | Integrada. `actualizaciones_gestion_16.md` y `fuentes_16.csv` quedan como **archivos históricos** |
| **17** | Motor OPEX + capital de trabajo v1.1 (completitud de arquitecturas; costo laboral) | `20_opex` | SUP-17-01…20, DPV-17-01…19, DEC-17-01…10, FTE-17-001…008, T17-01…04, D17-01…03 | Integrada. `actualizaciones_gestion_17.md` y `fuentes_17.csv` históricos |

Últimos IDs oficiales al iniciar: **SUP-154, DPV-159, DEC-079, FTE-309** (coinciden con los declarados por ambas sesiones). Las tensiones `T16-##`, `T17-##` y dependencias `D17-##` ya tenían formato definitivo y se conservan; las nuevas de esta reconciliación son `T18-##` (§12).

## 2. IDs consolidados (mapa provisional → definitivo)

Todos los IDs provisionales se reemplazaron en `19_capex/` y `20_opex/` (documentos, comentarios y textos de `modelo_capex.py` y `modelo_opex.py`, bases de costos, reglas laborales y CSV de salida regenerados) y en las filas nuevas de `25_fuentes/`. Formas abreviadas convertidas: `DPV-16-04/05` → `DPV-162 / DPV-093`; `FTE-16-001…007` → `FTE-310…316`; `FTE-17-001…008` → `FTE-317…322, FTE-029 y FTE-300`. Solo permanecen, como historia, en los dos `actualizaciones_gestion_1*.md` (marcados **ARCHIVO HISTÓRICO**), en los dos `fuentes_1*.csv` y en este documento.

**Resumen:** 45 SUP → 34 nuevos (SUP-155 a SUP-188) + 3 fusiones entre propuestas + 8 consolidaciones en existentes · 36 DPV → 18 nuevos (DPV-160 a DPV-177) + 3 fusiones + 15 consolidaciones (en 14 DPV) · 17 DEC → 12 nuevas (DEC-080 a DEC-091) + 2 fusiones + 3 consolidaciones, **+ 1 alta derivada** (DEC-092) · 15 FTE → 13 nuevas (FTE-310 a FTE-322) + 2 consolidaciones (FTE-029, misma URL; FTE-300, mismo documento).

#### Supuestos

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| SUP-16-01 | **SUP-155** | Alta nueva | FECHA_BASE_CAPEX = 2026-10-01 (editable). Moneda de comparación USD. P… |
| SUP-16-02 | **SUP-156** | Alta nueva | Reserva de flota: +1 unidad por flujo con flota propia y base > 0 (bar… |
| SUP-16-03 | **SUP-157** | Alta nueva | Ciclo de vehículos de alimento, pollitos y subproductos: 2 × distancia… |
| SUP-16-04 | **SUP-158** | Alta nueva | Arquitectura de frío → perfil de 09C: A = P1 con congelado propio míni… |
| SUP-16-05 | **SUP-159** | Alta nueva | Nivel de automatización en escalas intermedias: el de la escala de ref… |
| SUP-16-06 | **SUP-160** | Alta nueva | Paquetes sin doble conteo: los componentes de un lote RFQ (EQ-xx, FR-*… |
| SUP-16-07 | **SUP-161** | Alta nueva | Indirectos, preoperativos y contingencias por porcentaje sobre bases d… |
| SUP-16-08 | **SUP-162** | Alta nueva | LOW / HIGH = cantidad baja × precio bajo / cantidad alta × precio alto… |
| SUP-16-09 | **SUP-163** | Alta nueva | Configuraciones de referencia C0–C3 y CF con parámetros ilustrativos (… |
| SUP-16-10 | **SUP-164** | Alta nueva | Total preliminar solo si el 100 % de los conceptos costeables tiene pr… |
| SUP-16-11 | **SUP-165** | Alta nueva | Etiquetas de expansión desde la modularidad de 08_maquinaria/matriz_eq… |
| SUP-16-12 | **SUP-166** | Alta nueva | IVA: pendiente → se incluye con alerta IVA_INCIERTO; con_iva sin alícu… |
| SUP-16-13 | **SUP-167** | Alta nueva | Método escalado: sin exponente explícito, el precio de referencia solo… |
| SUP-16-14 | **SUP-168** | Alta nueva | Subproductos: A = lote L9 (sangre, plumas, vísceras, contenedores) + r… |
| SUP-16-15 | **SUP-169** | Alta nueva | Agua: almacenamiento = agua captada × 0,5 / 1 / 2 días; tratamiento y … |
| SUP-16-16 | **SUP-170** | Alta nueva | Terreno (v1.2): la modalidad declara la necesidad de la arquitectura (… |
| SUP-16-17 | **SUP-171** | Alta nueva | Alerta de planta de alimento subutilizada < 50 % de utilización (alert… |
| SUP-16-18 | **SUP-172** | Alta nueva | Una báscula de camiones en la planta de alimento |
| SUP-16-19 | **SUP-173** | Alta nueva | Rango del motor: 2.500–20.000 aves/día, intermedias permitidas, sin ex… |
| SUP-16-20 | **SUP-096** | Consolidado en SUP-096 (existente) | Capacidades de vehículos = escenarios de 12B (5.500 aves/camión; 12 t … |
| SUP-16-21 | **SUP-061** | Consolidado en SUP-061 (existente) | Capacidad nominal de línea = ritmo nominal requerido de 05 con sensibi… |
| SUP-16-22 | **SUP-147** | Consolidado en SUP-147 (existente) | CADENCIA_NACIMIENTOS = 2 cargas/semana y margen 15 %: escenario etique… |
| SUP-16-23 | **SUP-148** | Consolidado en SUP-148 (existente) | Perfil de fabricación de alimento = 5 d × 8 h, eficiencia 0,85, margen… |
| SUP-16-24 | **SUP-174** | Alta nueva | TERRENO_MINIMO_FISICO_DERIVADO = función de terreno de 12C con escala … |
| SUP-16-25 | **SUP-175** | Alta nueva | Terreno a adquirir = DECISIÓN (criterio_terreno: mínimo físico / conce… |
| SUP-17-01 | **SUP-155** | Fusionado con SUP-16-01 en SUP-155 | FECHA_BASE_OPEX = 2026-10-01 (editable). Moneda del modelo USD. Precio… |
| SUP-17-02 | **SUP-176** | Alta nueva | Anualización: drivers diarios × días operativos (250/300); drivers sem… |
| SUP-17-03 | **SUP-163** | Fusionado con SUP-16-09 en SUP-163 | Configuraciones de referencia = presets de CAPEX (SUP-16-09) + parámet… |
| SUP-17-04 | **SUP-177** | Alta nueva | Aportes en granja integrada según el esquema descripto en 03 (modelos_… |
| SUP-17-05 | **SUP-032** | Consolidado en SUP-032 (existente) | Composición del alimento = puntos ilustrativos de 14B (60 % maíz, 30 %… |
| SUP-17-06 | **SUP-178** | Alta nueva | Mantenimiento: cuatro métodos alternativos (% CAPEX, por activo, horas… |
| SUP-17-07 | **SUP-179** | Alta nueva | Naturaleza del costo laboral por driver de 14A: producción, activos y … |
| SUP-17-08 | **SUP-180** | Alta nueva | % variable por definición: driver de volumen → 100 % variable; driver … |
| SUP-17-09 | **SUP-181** | Alta nueva | Ramp-up: variables × u, fijos y semifijos constantes, escalamiento lin… |
| SUP-17-10 | **SUP-096** | Consolidado en SUP-096 (existente) | Capacidades y distancias logísticas = escenarios de CAPEX/12B (5.500 a… |
| SUP-17-11 | **SUP-099** | Consolidado en SUP-099 (existente) | Stock medio de producto terminado = inventario() de 12B con 6 despacho… |
| SUP-17-12 | **SUP-182** | Alta nueva | Costeo laboral provisional por FTE (v1.1): costo empresa/FTE = salario… |
| SUP-17-13 | **SUP-183** | Alta nueva | Tercerizar conserva la función: las horas de 14A siguen visibles; si e… |
| SUP-17-14 | **SUP-009** | Consolidado en SUP-009 (existente) | Tipo de cambio de precios en ARS = A3500 (oficial mayorista) del día d… |
| SUP-17-15 | **SUP-164** | Fusionado con SUP-16-10 en SUP-164 | Total preliminar y costos unitarios solo con cobertura 100 % de los co… |
| SUP-17-16 | **SUP-184** | Alta nueva | Huevos en incubación (WIP) valuados al costo del huevo como cota infer… |
| SUP-17-17 | **SUP-185** | Alta nueva | Completitud de arquitecturas (v1.1): cada módulo propio o contratado t… |
| SUP-17-18 | **SUP-186** | Alta nueva | Universos que no se mezclan (v1.1): utilities por universo (09C = solo… |
| SUP-17-19 | **SUP-187** | Alta nueva | Precio observado ≠ conversión (v1.1): el precio en ARS es la observaci… |
| SUP-17-20 | **SUP-188** | Alta nueva | Granjas mixtas (v1.1): cada concepto de producción primaria se registr… |

#### Datos por validar

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| DPV-16-01 | **DPV-160** | Alta nueva | Precio de equipos de proceso por lote RFQ (L1–L7, L11) y por escala, c… |
| DPV-16-02 | **DPV-161** | Alta nueva | USD/m² de obra civil por categoría (14 categorías de obra_civil_capex.… |
| DPV-16-03 | **DPV-087** | Consolidado en DPV-087 (existente) | Precio de terreno por tipo y corredor (industrial, parque, rural compa… |
| DPV-16-04 | **DPV-162** | Alta nueva | Fletes y logística de importación: flete marítimo, seguro, gastos port… |
| DPV-16-05 | **DPV-093** | Consolidado en DPV-093 (existente) | Importación: clasificación arancelaria, derechos, tasas, régimen aplic… |
| DPV-16-06 | **DPV-163** | Alta nueva | Alcance de paquetes e instalación: montaje electromecánico, supervisió… |
| DPV-16-07 | **DPV-051** | Consolidado en DPV-051 (existente) | Galpones: precio por plaza o por m² en Argentina y alcance (equipamien… |
| DPV-16-08 | **DPV-164** | Alta nueva | Indirectos: referencias documentadas de ingeniería, dirección de obra,… |
| DPV-16-09 | **DPV-165** | Alta nueva | Contingencia y escalación: clase de estimación por bloque (madurez de … |
| DPV-16-10 | **DPV-054** | Consolidado en DPV-054 (existente) | Cajones, módulos y contenedores: aves por cajón, juegos por camión, ti… |
| DPV-16-11 | **DPV-087** | Consolidado en DPV-087 (existente) | Conexiones: costo y plazo de acometida de MT, gas, agua y cloaca por s… |
| DPV-16-12 | **DPV-166** | Alta nueva | Programa de áreas asset-light (oficina, eventual cross-dock/CD) |
| DPV-16-13 | **DPV-166** | Fusionado con DPV-16-12 en DPV-166 | Programa de áreas de incubadora y planta de alimento (m² y terreno) |
| DPV-16-14 | **DPV-086** | Consolidado en DPV-086 (existente) | Prima/penalidad de ampliación por etapas (obra en operación, interfere… |
| DPV-16-15 | **DPV-167** | Alta nueva | Vida útil y tiempo de entrega por clase de activo y paquete |
| DPV-16-16 | **DPV-168** | Alta nueva | Vehículos: precio de chasis, carrocería, equipo de frío y equipo auxil… |
| DPV-16-17 | **DPV-169** | Alta nueva | Impuestos sobre la inversión: IVA de bienes de capital, percepciones, … |
| DPV-17-01 | **DPV-050** | Consolidado en DPV-050 (existente) | Alimento comprado: si el precio es puesto en granja o en fábrica, si i… |
| DPV-17-02 | **DPV-157** | Consolidado en DPV-157 (existente) | Granos y materias primas puestos en planta por corredor (maíz y harina… |
| DPV-17-03 | **DPV-047** | Consolidado en DPV-047 (existente) | Pollito BB y huevo fértil: precio, IVA, vacunas incluidas, lugar de en… |
| DPV-17-04 | **DPV-170** | Alta nueva | Contrato de integración: base de pago (ave / kg), ajustes por conversi… |
| DPV-17-05 | **DPV-052** | Consolidado en DPV-052 (existente) | Tarifas de energía y agua del sitio: electricidad industrial (cargo va… |
| DPV-17-06 | **DPV-171** | Alta nueva | Congelado y almacenamiento en frío de terceros: tarifa por t o t·mes, … |
| DPV-17-07 | **DPV-006** | Consolidado en DPV-006 (existente) | Faena a façon: tarifa por ave y alcance (empaque, frío, subproductos, … |
| DPV-17-08 | **DPV-172** | Alta nueva | Químicos de limpieza y sanitización (USD/ave o USD/m²), de potabilizac… |
| DPV-17-09 | **DPV-172** | Fusionado con DPV-17-08 en DPV-172 | Packaging por kg de producto según mix y formato (bolsa, bandeja, film… |
| DPV-17-10 | **DPV-150** | Consolidado en DPV-150 (existente) | Mantenimiento: plan y costo anual por área (por activo o contrato), re… |
| DPV-17-11 | **DPV-173** | Alta nueva | Primas de seguros por póliza (planta, incendio, RC, mercadería, interr… |
| DPV-17-12 | **DPV-174** | Alta nueva | Plan de autocontrol y precio por análisis (microbiología, agua, alimen… |
| DPV-17-13 | **DPV-174** | Fusionado con DPV-17-12 en DPV-174 | Certificaciones y auditorías (BPM/HACCP/ISO, clientes) y su costo anua… |
| DPV-17-14 | **DPV-175** | Alta nueva | Parámetros de capital de trabajo: días de cobro por canal, días de pag… |
| DPV-17-15 | **DPV-176** | Alta nueva | Dotaciones no dimensionadas por 14A: granjas propias, incubadora, plan… |
| DPV-17-16 | **DPV-177** | Alta nueva | Consumos no dimensionados: energía y gas de granja, cama (kg/m²), ener… |
| DPV-17-17 | **DPV-019** | Consolidado en DPV-019 (existente) | Lectura primaria del Índice de costo de producción de pollos parriller… |
| DPV-17-18 | **DPV-009** | Consolidado en DPV-009 (existente) | Lectura primaria del A3500 (BCRA) para las fechas de los precios usado… |
| DPV-17-19 | **DPV-148** | Consolidado en DPV-148 (existente) | Normativa laboral en original: SAC (Ley 20.744 arts. 121–122), vacacio… |

#### Decisiones

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| DEC-16-01 | **DEC-080** | Alta nueva | Adoptar la estructura del motor CAPEX: bloques, niveles de evidencia E… |
| DEC-16-02 | **DEC-081** | Alta nueva | Modalidad de contratación de la línea: por lotes (L1–L7) vs llave en m… |
| DEC-16-03 | **DEC-082** | Alta nueva | RFQ de frío y efluentes: paquete integral vs desglosado por componente… |
| DEC-16-04 | **DEC-083** | Alta nueva | Criterio de contingencia por bloque cuando existan cotizaciones (clase… |
| DEC-16-05 | **DEC-084** | Alta nueva | Umbral de cobertura para publicar un CAPEX preliminar total (el motor … |
| DEC-16-06 | **DEC-056** | Consolidado en DEC-056 (existente) | Titularidad de cajones/módulos de aves vivas con transporte tercerizad… |
| DEC-16-07 | **DEC-063** | Consolidado en DEC-063 (existente) | Criterio de terreno a adquirir (mínimo físico / conceptual 12C / escen… |
| DEC-17-01 | **DEC-080** | Fusionado con DEC-16-01 en DEC-080 | Adoptar la estructura del motor OPEX: registro por concepto, niveles E… |
| DEC-17-02 | **DEC-024** | Consolidado en DEC-024 (existente) | Variante del façon de alimento: materias primas de la empresa (B1) o d… |
| DEC-17-03 | **DEC-085** | Alta nueva | Fuente de agua de la planta: red / pozo / mixta |
| DEC-17-04 | **DEC-086** | Alta nueva | Base de pago y reparto de aportes con los integrados (por ave / por kg… |
| DEC-17-05 | **DEC-087** | Alta nueva | Modelo de tarifa del flete tercerizado por flujo (viaje / km / unidad … |
| DEC-17-06 | **DEC-088** | Alta nueva | Método de estimación del mantenimiento (por activo / contrato / horas … |
| DEC-17-07 | **DEC-089** | Alta nueva | Método de valuación de inventarios para el capital de trabajo: activo … |
| DEC-17-08 | **DEC-090** | Alta nueva | Curva de ramp-up y parámetros de ineficiencia del arranque (para el mo… |
| DEC-17-09 | **DEC-091** | Alta nueva | Política de cobro, pago y caja operativa (días por canal y proveedor; … |
| DEC-17-10 | **DEC-084** | Fusionado con DEC-16-05 en DEC-084 | Umbral de cobertura para publicar un OPEX preliminar y costos unitario… |

#### Fuentes

| ID provisorio | ID definitivo | Tratamiento | Tema |
|---|---|---|---|
| FTE-16-001 | **FTE-310** | Alta nueva | Cuánto cuesta construir un galpón o nave industrial en Argentina 2026  |
| FTE-16-002 | **FTE-311** | Alta nueva | Índice del Costo de Producción de pollos parrilleros - Mayo 2026 |
| FTE-16-003 | **FTE-312** | Alta nueva | Pliego de licitación: acondicionamiento de instalaciones de sala de fa |
| FTE-16-004 | **FTE-313** | Alta nueva | Economic Feasibility of Mobile Processing Units for Small Poultry Prod |
| FTE-16-005 | **FTE-314** | Alta nueva | Guidelines for Prospective Contract Hatching Egg Producers (B 1214) |
| FTE-16-006 | **FTE-315** | Alta nueva | Poultry feed manufacturing plant cost (1–20 t/h) |
| FTE-16-007 | **FTE-316** | Alta nueva | Rentabilidad del pollo parrillero (EEA Famaillá) |
| FTE-17-001 | **FTE-317** | Alta nueva | Precios de pizarra de la Cámara Arbitral de Cereales de Rosario - maíz |
| FTE-17-002 | **FTE-029** | Consolidado en FTE-029 (existente) | Precios del huevo y productos avícolas - semana del 06/07/2026 (precio |
| FTE-17-003 | **FTE-318** | Alta nueva | Cotización del dólar oficial y mayorista - martes 29 de septiembre de  |
| FTE-17-004 | **FTE-319** | Alta nueva | Dólar oficial: cierre del lunes 6 de julio de 2026 (A3500) |
| FTE-17-005 | **FTE-320** | Alta nueva | Soja Rosario (septiembre 2026) |
| FTE-17-006 | **FTE-321** | Alta nueva | Precios internacionales - harina y pellets de soja (contrato septiembr |
| FTE-17-007 | **FTE-322** | Alta nueva | CAPIA - Precios de referencia (extracto con fecha 2026-09-13) |
| FTE-17-008 | **FTE-300** | Consolidado en FTE-300 (existente) | Ley 20.744 de Contrato de Trabajo - sueldo anual complementario (arts. |

**Alta derivada (sin ID provisional):** **DEC-092** — estructura de financiamiento futura (las sesiones 16 y 17 la dejaron implícita en "modelo financiero"; se registra como decisión de negocio).

## 3. Supuestos

**34 nuevos (SUP-155 a SUP-188)**, todos `Vigente`, con su clasificación explícita en el texto. Ninguno se elevó a hecho y ninguno contiene precios ni salarios.

| Estatus | Qué es | Ejemplos en CAPEX/OPEX |
|---|---|---|
| **HECHO** | Dato con fuente verificada en original | **Ninguno** en 16/17 (ninguna fuente pudo leerse en original; DPV-009) |
| **PVDP** | Visto solo en extractos de buscador | Pollito ARS 1.312,22 sin IVA (FTE-029), maíz Rosario ARS 295.800/t (FTE-317), TC (FTE-318/319), USD/m² de naves (FTE-310), cota de galpones (FTE-081), SAC (FTE-300) |
| **SUPUESTO / CRITERIO DE MODELO / ESCENARIO** | Hipótesis o regla adoptada | Fecha base y moneda (SUP-155), configuraciones C0–CF (SUP-163), regla de totales (SUP-164), aportes en granja integrada (SUP-177), % variable por definición (SUP-180), ramp-up (SUP-181), costeo por FTE (SUP-182), precio observado ≠ conversión (SUP-187) |
| **RESULTADO DEL MODELO** | Cifra calculada desde supuestos | BOQ y cantidades por arquitectura, terreno mínimo físico, coberturas estructural / física / de costeo, inventarios físicos por propiedad, FTE industriales de 14A consumidos por OPEX |

### 3.1 Revisión de solapamientos (pedida explícitamente)

| Tema | Propuestas | Registro existente | Tratamiento |
|---|---|---|---|
| Fecha base | SUP-16-01, SUP-17-01 | — | **Fusionadas en SUP-155** (una sola fecha base 2026-10-01 para ambos motores; sin indexación automática) |
| Moneda | SUP-16-01, SUP-17-01 | SUP-002 | SUP-155 (USD); SUP-002 sin cambios |
| Tipo de cambio | SUP-17-14 | SUP-009 (mayorista del día; A3500) | **Consolidado en SUP-009** (anotado: A3500 del día del precio) |
| Precio observado vs conversión | SUP-17-19 | SUP-009 | SUP-187 nuevo (observación ARS ≠ conversión USD; Rosario ≠ puesto planta) |
| Terreno | SUP-16-16, 24, 25 | SUP-119, SUP-121; DEC-063 | SUP-170 (necesidad), SUP-174 (mínimo físico), SUP-175 (a adquirir = decisión); el criterio es **DEC-063** (consolida DEC-16-07) |
| Obra | — (las cantidades vienen de 12C) | SUP-107 a SUP-121 | Sin cambios; superficie conceptual ≠ proyecto ejecutivo (T18-03) |
| Contingencias / indirectos / preoperativos | SUP-16-07 | — | SUP-161 (porcentajes **no adoptados**) |
| Instalación / paquetes | SUP-16-06 | — | SUP-160 (sin doble conteo) |
| Expansión | SUP-16-11 | SUP-059, SUP-119, SUP-123 | SUP-165 (etiquetas); prima de ampliación en DPV-086 |
| Importación / IVA | SUP-16-12 | — | SUP-166 (IVA en CAPEX antes de tratamiento fiscal); importación en DPV-162, DPV-093 |
| Mantenimiento | SUP-17-06 | SUP-132, SUP-139 (dotación) | SUP-178 (costo; un método por corrida); dotación sigue en SUP-132/139 |
| Utilización / ramp-up | SUP-17-09 | SUP-052 (100 % de capacidad operativa = definición de escala) | SUP-181 (utilización y ramp-up = **inputs**; no 100 % automático) |
| Días de stock | SUP-17-11 | SUP-056, SUP-099, SUP-150 | **Consolidado en SUP-099** (stock de producto de 12B); upstream sigue en SUP-150 |
| Plazos de cobro / pago | — (inputs vacíos) | — | Sin supuesto: DPV-175 y DEC-091 (no se inventan días) |
| Fijo / variable | SUP-17-07, SUP-17-08 | SUP-140 (driver de 14A) | SUP-179, SUP-180 |
| Composición de alimento | SUP-17-05 | SUP-032 | **Consolidado en SUP-032** |
| Propiedad de inventarios | — | SUP-154 | SUP-154 anotado (regla aplicada por OPEX); SUP-184 (WIP de huevo, cota inferior) |
| Tratamiento laboral | SUP-17-12, SUP-17-13 | SUP-125, SUP-126 | SUP-182 (costeo por FTE; SAC = regla, no precio; **no se cargan salarios**), SUP-183 |
| Configuraciones | SUP-16-09, SUP-17-03 | SUP-152 | **Fusionadas en SUP-163**; SUP-152 anotado (M0–MF ≠ C0–CF, §10) |
| Totales | SUP-16-10, SUP-17-15 | — | **Fusionadas en SUP-164**; umbral definitivo en DEC-084 |
| Capacidades / distancias logísticas | SUP-16-20, SUP-17-10 | SUP-096, SUP-091 | **Consolidados en SUP-096** (y SUP-091 anotado) |
| Escenarios etiquetados heredados | SUP-16-21, 22, 23 | SUP-061, SUP-147, SUP-148 | **Consolidados** en los existentes (son elecciones de escenario de un rango ya registrado) |

## 4. Datos por validar

**18 nuevos (DPV-160 a DPV-177)**, todos `Pendiente`; **ninguno N1** (N2: 11 · N3: 7), por lo que no cambian los hitos H-A / H-B; se concentran en H-C (insumos para CAPEX/OPEX). 15 propuestas se consolidaron en 14 DPV existentes, cuyas OBSERVACIONES en la matriz se ampliaron. **DPV-093** (régimen de importación) se amplió a bienes de capital nuevos y su nivel se **elevó de N4 a N2** porque condiciona el CAPEX landed de equipos importados (único cambio de nivel; registrado en ambos archivos). `matriz_validacion_campo.csv`: **177 filas**, 18 columnas, CRLF preservado, todas `NO INICIADO`; ninguna columna ni estado existente modificado.

### 4.1 CAPEX — cobertura de los temas pedidos

| Tema | DPV |
|---|---|
| Cotización de líneas (y exponente de escala) | **DPV-160** (+ DPV-097 capacidad garantizada) |
| Precios por m² de obra | **DPV-161** |
| Terreno (precio por tipo y corredor) | DPV-087 (consolida) |
| Frío, efluentes, electricidad, agua (equipos) | **DPV-160** (paquetes FR-PAQ, EF-*, utilities); capacidades en DPV-095, DPV-109 |
| Conexiones (MT, gas, agua, cloaca, kVA) | DPV-087 (consolida) |
| Incubación y planta de alimento (equipos) | **DPV-160**; programas de áreas en **DPV-166** |
| Granjas (galpones) | DPV-051 (consolida; SAGyP FTE-311, INTA FTE-316) |
| Vehículos | **DPV-168** |
| Montaje, instalación, commissioning | **DPV-163** |
| Ingeniería e indirectos | **DPV-164** |
| Importación (EXW/FOB → landed) | **DPV-162** |
| Aranceles y régimen | DPV-093 (consolida, N4 → N2) |
| Impuestos (IVA de bienes de capital, amortización impositiva, Ganancias, regímenes) | **DPV-169** (+ DPV-043 ventas) |
| Contingencia y escalación | **DPV-165** |
| Vidas útiles, reemplazo, valor residual, plazo de entrega | **DPV-167** |
| Expansión por etapas (prima de ampliación) | DPV-086 (consolida) |

### 4.2 OPEX — cobertura de los temas pedidos

| Tema | DPV |
|---|---|
| Alimento terminado | DPV-050 (consolida) |
| Maíz / soja / micros | DPV-157 (consolida; FTE-317) |
| Pollitos | DPV-047 (consolida) |
| Huevo fértil | DPV-154 (anotado: precio) |
| Contratos de integración | **DPV-170** |
| Salarios, cargas, convenio | DPV-148 (consolida normativa laboral), DPV-146 (anotado) |
| Electricidad, gas | DPV-052 (consolida tarifas) |
| Agua | DPV-053 (anotado: tarifa / canon) |
| Químicos y packaging | **DPV-172** (DPV-112, DPV-129 anotados) |
| Mantenimiento | DPV-150 (consolida costo por área) |
| Façon (faena) | DPV-006 (consolida tarifa y alcance) |
| Frío de terceros | **DPV-171** |
| Logística (tarifas por flujo, flota propia) | DPV-134 (anotado), DPV-042, DPV-054 |
| Seguros | **DPV-173** |
| Laboratorio y certificaciones | **DPV-174** (DPV-101 anotado) |
| Halal / exportación | DPV-022, DPV-030 (anotado: módulo futuro de mercado), DPV-024 |
| Plazos comerciales, stock, capital de trabajo | **DPV-175** (DPV-039 anotado) |
| Dotaciones y consumos upstream | **DPV-176**, **DPV-177** (cama → DPV-130 y L/km → DPV-131, no duplicados) |
| Índice SAGyP y A3500 (lectura primaria) | DPV-019, DPV-009 (consolidan) |

## 5. Decisiones

**12 nuevas de 16/17 (DEC-080 a DEC-091) + 1 alta derivada (DEC-092)**, todas `Abierta`, sin resultado. **3 consolidaciones:** titularidad de cajones → **DEC-056**; criterio de terreno a adquirir → **DEC-063**; variante del façon B1/B2 → **DEC-024**. Ninguna decisión se cerró. Las dos categorías **no se mezclan** (cada fila nueva lleva su etiqueta).

### 5.1 Decisiones metodológicas (cómo se calcula y publica)

| Decisión | Tema |
|---|---|
| **DEC-080** | Estructura de los motores CAPEX y OPEX (fusiona las dos propuestas) |
| **DEC-083** | Criterio de contingencia, escalación y % de indirectos/preoperativos |
| **DEC-084** | **Umbral de publicación** de CAPEX total, OPEX total, costo por ave/kg, capital de trabajo, EBITDA, VAN, TIR y payback (fusiona las dos propuestas y amplía a los indicadores financieros). **Hasta decidirlo: NO PUBLICABLE si falta un bloque material** |
| **DEC-088** | Método de estimación del mantenimiento |
| **DEC-089** | Método de valuación de inventarios del capital de trabajo |

### 5.2 Decisiones de negocio (qué hace la empresa)

| Tema | Decisión |
|---|---|
| Terreno a adquirir | DEC-063 (consolida el criterio de terreno) |
| Faena propia / façon | DEC-004 |
| Alimento comprado / façon (B1/B2) / propio | DEC-024 (consolida la variante B1/B2), DEC-075 a DEC-077 |
| Pollito comprado / incubación | DEC-023, DEC-078 |
| Granjas propias / integradas; base de pago y aportes | DEC-020, **DEC-086** |
| Flota (y titularidad de cajones); tarifa del flete | DEC-056 (consolida), **DEC-087** |
| Frío / congelado | DEC-046, DEC-064 |
| Subproductos / rendering | DEC-027, DEC-059, DEC-066 |
| Contratación de la línea; alcance de RFQ de frío y efluentes | **DEC-081**, **DEC-082** |
| Fuente de agua | **DEC-085** |
| Ramp-up y utilización | **DEC-090** |
| Política comercial: cobro, pago, stock, caja | **DEC-091** (con DEC-079 stock upstream y DEC-058 stock de producto) |
| Financiamiento futuro | **DEC-092** (alta derivada) |

Decisiones existentes anotadas sin cambiar su estado: DEC-002, DEC-006, DEC-010, DEC-013.

## 6. Fuentes

**13 nuevas (FTE-310 a FTE-322)** en `25_fuentes/registro_fuentes.csv` (322 filas, 11 columnas, IDs consecutivos) y en `bibliografia.md` por tipo, con nota de sesión. **Todas siguen `[PVDP]`** (extractos de buscador; sitios bloqueados con `EGRESS_BLOCKED`); no se subió ningún nivel de evidencia. Ajustes administrativos:

- **Consolidaciones:** la fuente provisional de precios CAPIA de la sesión 17 tenía **la misma URL** que **FTE-029** (precio del pollo vivo, misma semana): se consolidó en FTE-029 agregando el dato de pollito BB; la Ley 20.744 de la sesión 17 es **el mismo documento** que **FTE-300**: se consolidó agregando la regla SAC y la ubicación sugerida (no leída).
- **FTE-322** queda registrada como **DESCARTADA** (contradicción con FTE-029, regla 16).
- **FTE-311** (Índice de costo SAGyP, may-2026, PDF) es distinta de **FTE-006** (dataset ICPP): se registra aparte y se cita junto a ella en DPV-019 y DPV-051.
- Tipo normalizado: `academico` → `academica` (FTE-313, FTE-314).
- Ninguna URL nueva duplica una existente (persisten las 2 repeticiones preexistentes).

## 7. Estado de la evidencia económica — CAPEX

| Indicador | Valor (CSV finales) |
|---|---|
| Conceptos en la base | **175** |
| Con referencia monetaria | **8**, todas **E4 `[PVDP]`**: 2 con precio aplicado (OC-DP depósitos secos, GRA-GAL galpones), 5 referencias no usadas, 1 futura (reproductoras) |
| Sin precio | 167 |
| Cobertura por conceptos | C0 0 % · C1 1,3 % · C2 2,3 % · C3/CF 1,4 % |
| Cobertura por valor | **NO CALCULABLE** en los 33 escenarios |
| Montos E1–E3 | **0** en todos los escenarios |
| CAPEX total | **NO DISPONIBLE** en los 33 escenarios: **no existe CAPEX total publicable** |
| Calidad del monto con precio | `MONTO_CON_REFERENCIAS_DEBILES_E4` (C1–CF) / `SIN_MONTO` (C0); 89–98 % del monto de C2/C3 es una cota de prensa de galpones (T16-03) |

## 8. Estado de la evidencia económica — OPEX

| Indicador | Valor (CSV finales) |
|---|---|
| Conceptos en la base | **359** (ampliada en la v1.1) |
| Con precio | **2**, ambos **E4 `[PVDP]`**: pollito BB (POL-COMPRA) y maíz pizarra Rosario (ALI-MP-MAIZ); además 2 referencias no usadas y 1 descartada |
| Sin precio | 329 `PENDIENTE` (+ 17 FUTURO, 8 OPCIONAL) |
| Cobertura estructural / física / de costeo por bloques | 100 % / 43–73 % / 0–10 % |
| Cobertura de costeo por conceptos | 0,46–2,63 % |
| Arquitecturas operativamente completas / costeables | **Ninguna / ninguna** |
| OPEX total, costo por ave, por kg vivo, por kg de producto | **NO DISPONIBLE** en los 29 escenarios: **no existe OPEX total ni costo por ave/kg confiable** |
| Comparabilidad | `MONTOS_PARCIALES_E4_NO_COMPARABLES` en los 29 escenarios |

Los montos con precio de ambos motores **no son comparables** entre arquitecturas ni escalas: reflejan qué concepto tiene precio, no el costo de cada opción.

## 9. Capital de trabajo

```
CAPITAL_TRABAJO_OPERATIVO = INVENTARIOS_PROPIOS + CUENTAS_POR_COBRAR + CAJA_OPERATIVA − CUENTAS_POR_PAGAR
```

| Componente | Regla reconciliada | Estado |
|---|---|---|
| **Inventario** | Entra **solo si `PROPIEDAD_EMPRESA = TRUE`** (también stock propio en un tercero: MP en façon B1, producto en frío del faenador). Stock de terceros (fábrica proveedora, MP del elaborador en B2) y propiedad PENDIENTE (façon sin variante) **no** entran | Verificado: 305 filas propias, 55 de terceros y 8 pendientes excluidas (§14). Valores PENDIENTES |
| **Cuentas por cobrar** | ventas × días de cobro ÷ 365, por canal | PENDIENTE: no hay ventas ni plazos (DPV-175, DPV-039) |
| **Cuentas por pagar** | compras × días de pago ÷ 365, por grupo de proveedor | PENDIENTE: compras sin precio, plazos sin dato |
| **Caja operativa** | según la política que se elija (DEC-091); sin política = `NO_ASIGNADA` | Sin política |
| **CAPITAL_TRABAJO_TOTAL** | — | **PENDIENTE** en los 29 escenarios, hasta contar con precios, ventas y plazos |

El **maíz valorizado** (USD 15.445–123.561, E4 sobre puerto) es el único ítem con valor y **no** se usa como proxy del CT total.

**CAPEX ≠ CAPITAL DE TRABAJO.** El BOQ no contiene inventarios ni cuentas por cobrar (test P05) y el capital de trabajo inicial no está en CAPEX (cambio de alcance del README de `19_capex` confirmado; `20_opex` ya lo incluye en su alcance). La inversión total futura será **conceptualmente** `FONDOS_INICIALES = CAPEX + CAPITAL_TRABAJO_INICIAL + otros requerimientos financieros pertinentes` ([`interfaz_capex_finanzas.md`](interfaz_capex_finanzas.md) §1). **No se calcula.**

## 10. Arquitectura económica (C0–CF)

Puente: [`mapa_arquitecturas_economicas.csv`](mapa_arquitecturas_economicas.csv) (29 filas: 5 configuraciones base, 19 variantes, 5 referencias de madurez de 14B).

**Verificación:** las configuraciones C0–CF se definen **una sola vez** en `preset()` de `modelo_capex.py`; OPEX las importa con `config_opex()` (no las redefine). Comprobado en esta sesión: la configuración CAPEX contenida en la configuración OPEX es **idéntica** al preset en las 5 configuraciones, y la cadena `ARQUITECTURA` de los 20 escenarios comunes coincide en ambos CSV. El capital de trabajo usa la misma corrida. **C3 en CAPEX = C3 en OPEX = C3 en CT.**

| Config. | Interpretación común (CAPEX = OPEX = CT) | Diferencias documentadas |
|---|---|---|
| **C0** asset-light | Faena a façon, granjas integradas, pollito comprado, alimento a façon, flota y congelado de terceros | CAPEX no distingue B1/B2 (sin activos); OPEX deja la propiedad de MP PENDIENTE y corre B1 y B2 como variantes. CAPEX corre C0 con `subprod = A_externo` (sin activos); en OPEX el destino de subproductos es parte del contrato de façon (FAE-FACON-SUB) |
| **C1** planta de faena | Faena propia; integrados; pollito y alimento comprados; flota tercera; frío A | Variantes distintas por módulo: CAPEX (frío, subproductos, línea, automatización, días, terreno) y OPEX (combustible y agua, limpieza, mantenimiento, flete, pago al integrado, halal). **No** son arquitecturas nuevas; cada una se corrió solo donde cambia algo |
| **C2** faena + activos selectivos | 25 % granjas propias, alimento a façon, flota propia en aves vivas, refrigerado y servicio, frío B | OPEX separa granjas PROPIA / INTEGRADA en dos filas (SUP-188) |
| **C3** mayor integración | Granjas 100 % propias, incubación con huevo comprado, planta de alimento, flota propia, subproductos básicos | OPEX: RRHH y utilities upstream PENDIENTES (14A y 09C solo cubren faena) |
| **CF** futura | C3 + reproductoras + rendering (FUTURO) | En ambos motores lo FUTURO no suma: montos iniciales = C3 por construcción |

**Diferencia de nomenclatura corregida (sin tocar modelos):** las "arquitecturas de madurez de referencia 0 / 1 / 2 / 3 / futura" de 14B (SUP-152) **no** son C0–C3/CF: p. ej. la 3 de 14B tiene granjas integradas + propias y C3 tiene 100 % propias; la 0 de 14B compra el alimento y C0 lo hace a façon. Se renombran **M0–M3/MF** (nota en `14_alimento_balanceado/integracion_upstream.md` §3 y SUP-152 anotado). Otros "C" del repositorio que **no** son configuraciones: criterios de flota C1–C10 (`13_logistica`), puntos normativos C1–C6 (`16_normativa_senasa`), capas de importación C01–C10 (CAPEX).

No se decide cuál configuración es mejor.

## 11. Interfaz al modelo financiero

| Documento | Contenido |
|---|---|
| [`interfaz_capex_finanzas.md`](interfaz_capex_finanzas.md) | CAPEX directo, indirecto, preoperativo, contingencia, terreno, inversión por fase y acumulada, inversiones futuras, reposiciones, vida útil, valor residual, fecha/desembolso (casi todo PENDIENTE); `FONDOS_INICIALES` conceptual; capas de importación; mantenimiento vs reposición; preoperativos; halal; frontera fiscal |
| [`interfaz_opex_finanzas.md`](interfaz_opex_finanzas.md) | OPEX **por período** (`variable × u(t) + fijo`), fijo / variable / semifijo / semivariable, centros de costo, costo laboral, servicios, inventarios, CxP, días, ramp-up, propiedad del stock; capital de trabajo; precio observado vs conversión; frontera fiscal; **categorías de ingreso sin precio** |
| [`matriz_completitud_economica.csv`](matriz_completitud_economica.csv) | Estado por configuración y bloque (§13) |

**Cadena obligatoria:** DEMANDA → UTILIZACIÓN → PRODUCCIÓN → VENTAS → OPEX VARIABLE → CAPITAL DE TRABAJO → FLUJO. El financiero **no** asumirá 100 % de utilización: ramp-up y utilización son inputs (DEC-090).

**Verificaciones de frontera pedidas:**

| Punto | Resultado |
|---|---|
| Preoperativos (commissioning, ingeniería, herramientas, capacitación, repuestos iniciales) | Solo en CAPEX (PRE-*, IND-ING). En OPEX: `NO_APLICA_EN_OPERACION_NORMAL` (estructura §6, ramp-up §3, test S06). Los conceptos OPEX parecidos (FAE-CUCH, LAB-*-CAP, MAN-*-REP) son **recurrentes**, no iniciales. Ningún PRE-* en el registro OPEX |
| Mantenimiento | CAPEX = activos; OPEX = mantenimiento, repuestos, contratos, horas técnicas; reemplazos mayores = **CAPEX de reposición** del financiero |
| Importación | CAPEX conserva EXW / FOB / CIF / landed / instalado; OPEX no tiene ningún concepto de importación ni arancel (sus "aranceles" son solo tasas SENASA, CAL-SENASA) |
| Impuestos | Frontera: CAPEX/OPEX actuales = costos antes de tratamiento fiscal; el financiero tratará IVA, Ganancias, depreciaciones, créditos fiscales, importación, tasas y regímenes (DPV-169, DPV-043). No se calculó nada |
| Halal / exportación | CAPEX puede incorporar inversión específica como conceptos nuevos de la base (hoy sin bloque); OPEX tiene HAL-* opcional sin importes; ingresos separan mercado de exportación. **Módulo futuro de mercado**, sin importes |
| Registros de precios | Precio observado (ARS) separado de la conversión USD en pollito y maíz; precio Rosario ≠ puesto planta; ambos siguen E4 |

## 12. Tensiones (ninguna resuelta)

Se conservan T16-01…10, T17-01…04 y D17-01…03 de las sesiones (ver sus archivos históricos). Nuevas de esta reconciliación:

| ID | Tensión | Detalle | Qué la cierra |
|---|---|---|---|
| **T18-01** | **CAPEX con precios casi inexistentes** | 8 de 175 conceptos con referencia, todas E4 `[PVDP]`; cobertura por conceptos 0–2,3 %; por valor no calculable | DPV-160 a DPV-169, DPV-087, DPV-051, DPV-093 |
| **T18-02** | **OPEX con precios casi inexistentes** | 2 de 359 con precio (E4); costeo por bloques 0–10 %; ninguna arquitectura costeable | DPV-047, 050, 052, 148, 157, 170–177 |
| **T18-03** | **Obra conceptual vs proyecto ejecutivo** | Los m² de 12C son órdenes de magnitud (muchos PROXY); un USD/m² sobre ellos hereda esa incertidumbre | DPV-161, DPV-143, DPV-137; proyecto ejecutivo (IND-PEJ) |
| **T18-04** | **Terreno conceptual vs terreno adquirido** | Cuatro definiciones (mínimo físico, conceptual 12C, objetivo, requerido); el adquirido es decisión (DEC-063); sin criterio, bloque TERRENO PROVISIONAL | DEC-063, DPV-087, DPV-141 |
| **T18-05** | **Capacidad física vs capacidad comercial de equipos** | El BOQ usa el ritmo nominal requerido de 05 (escenario R = 0,89); diseño y garantizada PENDIENTES; la capacidad no es demanda | DPV-097, DPV-088, DEC-001 |
| **T18-06** | **Upstream propio sin dimensionamiento completo de RRHH y utilities** | C3/CF tienen la estructura de costos de granjas, incubación y planta de alimento pero sin dotación ni consumos (14A y 09C solo cubren faena); C3/CF no pueden ser operativamente completas | DPV-176, DPV-177 |
| **T18-07** | **Stock físico vs propiedad** | El requerimiento físico de la cadena es igual en A/B1/B2/C; cambia quién lo posee; en la realidad los días del tercero no serán iguales (continúa T14-09) | DPV-155, DPV-156, DPV-175, DEC-024, DEC-079 |
| **T18-08** | **Consumo de faena vs utilities upstream** | kWh, agua y térmico de 09C son de la planta de faena; extenderlos a la empresa integrada subestimaría (universos separados, SUP-186) | DPV-177, DPV-052, DPV-053 |
| **T18-09** | **Precio Rosario vs puesto planta** | Maíz E4 es pizarra **sobre puerto**; el diferencial y el flete a planta son PENDIENTES (continúa T17-02) | DPV-157 |
| **T18-10** | **Pollito observado en ARS vs conversión USD** | ARS 1.312,22 sin IVA de julio 2026 convertido con A3500 de esa fecha; anterior a la fecha base y sin indexar; entrega y vacunas desconocidas; extracto contradictorio descartado (continúa T17-01) | DPV-047, DPV-009, DEC-006 |
| **T18-11** | **Utilización madura vs ramp-up** | Los motores publican escala plena (u = 1); el arranque no tiene factores ni ineficiencias modeladas | DEC-090, DPV-088, demanda validada |
| **T18-12** | **Inversión por fases vs inversión inicial** | CAPEX separa INICIAL / FUTURO y trayectorias de expansión, pero sin cronograma de desembolsos ni prima de ampliación; el "acumulado igual entre trayectorias" es artefacto | DPV-086, DPV-167, DEC-033, DEC-035 |
| **T18-13** | **Expansibilidad vs reemplazo** | Partir de 5.000 implica reemplazar ≈ 39 equipos al llegar a 20.000 (10.000: ≈ 20) según niveles de automatización hipotéticos (continúa T16-06); el costo de reemplazo y el valor residual están vacíos | DPV-167, DEC-037, DEC-033 |
| **T18-14** | **Costos E4 no comparables** | Montos `MONTO_CON_REFERENCIAS_DEBILES_E4` (CAPEX) y `MONTOS_PARCIALES_E4_NO_COMPARABLES` (OPEX) reflejan qué concepto tiene precio: no permiten comparar C0–CF ni escalas, ni contra USD 2 M | DEC-084 |
| **T18-15** | **Nomenclatura de arquitecturas** | "Arquitectura 3" (14B) ≠ C3 (CAPEX/OPEX). Corregido solo en nomenclatura (M0–MF); 14B no tiene preset económico, de modo que M3 (integrados + propias) solo puede aproximarse corriendo C3 con granjas mixtas | Uso del mapa; DEC-074 |
| **T18-16** | **Variantes no cruzadas** | Las variantes de CAPEX (frío, línea, automatización, terreno) no se corrieron en OPEX y viceversa; el financiero debe correr ambos módulos con los mismos inputs para cada variante que use | Interfaz (§11) |

## 13. Completitud económica

[`matriz_completitud_economica.csv`](matriz_completitud_economica.csv): 60 filas (5 configuraciones × 12 bloques), estados COMPLETO / PARCIAL / PENDIENTE / NO_APLICA.

| Bloque | C0 | C1 | C2 | C3 | CF | Bloquea rentabilidad |
|---|---|---|---|---|---|---|
| Demanda | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Cantidades vendibles (balance de masa, mix) | PARCIAL | PARCIAL | PARCIAL | PARCIAL | PARCIAL | Sí |
| Utilización / ramp-up | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Precio de venta | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| CAPEX | PARCIAL | PARCIAL | PARCIAL | PARCIAL | PARCIAL | Sí |
| OPEX | PARCIAL | PARCIAL | PARCIAL | PARCIAL | PARCIAL | Sí |
| Capital de trabajo | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Impuestos | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Financiamiento | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Evidencia | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | Sí |
| Exportación / halal | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | PENDIENTE | No (base sin exportación) |
| Módulos futuros | NO_APLICA | NO_APLICA | NO_APLICA | NO_APLICA | PENDIENTE | No |

**Ningún bloque está COMPLETO en ninguna configuración.** Por eso hoy **no puede calcularse rentabilidad real**: faltan a la vez ingresos (demanda, precio, utilización) y costos (CAPEX, OPEX, CT) y su tratamiento fiscal y financiero. EBITDA, VAN, TIR y payback quedan **NO PUBLICABLES** (DEC-084).

## 14. Tests

Ejecutados el 2026-10-03 después de la integración, con `PYTHONDONTWRITEBYTECODE=1`.

| Suite | Comando | Resultado |
|---|---|---|
| **CAPEX (16)** | `python3 19_capex/modelo_capex.py` | **82/82**; 5.485 filas BOQ, 528 de escenarios, 2.508 de expansión |
| CAPEX — mutaciones | `python3 19_capex/modelo_capex.py --mutaciones` | **10/10** detectadas |
| **OPEX (17)** | `python3 20_opex/modelo_opex.py` | **78/78**; 4.549 filas de registro, 457 de escenarios, 2.349 de mapa, 1.422 laborales, 615 de CT, 166 de completitud |
| OPEX — mutaciones | `python3 20_opex/modelo_opex.py --mutaciones` | **14/14** detectadas |
| Reproducción de salidas | regenerar y comparar con `reemplazo_de_IDs(HEAD)` | **12/12 CSV idénticos byte a byte** (`boq`, `escenarios`, `expansion`, `mapa_drivers`, `matriz_rfq` de CAPEX; `registro`, `escenarios`, `mapa_drivers`, `modelo_costo_laboral`, `capital_trabajo`, `completitud`, `matriz_validacion` de OPEX) |
| Lógica de los modelos | diff de `modelo_capex.py` / `modelo_opex.py` contra `HEAD` normalizando IDs | Solo cambian IDs en comentarios/textos y la línea de "IDs provisionales" |

Línea base previa (HEAD sin cambios): las dos suites pasaban y regeneraban los CSV idénticos al commit. No se ejecutaron los módulos históricos (03, 04, 05, 09C, 12A–C, 14A/B, 23): no se modificaron (salvo una nota de nomenclatura en `14_alimento_balanceado/integracion_upstream.md`, sin cambio de modelo); CAPEX y OPEX los importan y sus tests de reproducción (D01–D10, N01–N19) pasaron.

**Control de integridad**

| Control | Resultado | Detalle |
|---|---|---|
| IDs SUP únicos y consecutivos | OK | 188 (SUP-001–SUP-188) |
| IDs DPV únicos y consecutivos | OK | 177 (DPV-001–DPV-177) |
| IDs DEC únicos y consecutivos | OK | 92 (DEC-001–DEC-092) |
| IDs FTE únicos y consecutivos | OK | 322 |
| Ninguna DEC Tomada/Descartada | OK |  |
| Sin SUP/DPV/DEC/FTE provisionales activos (16/17) | OK | [] |
| Sin marcadores de merge | OK | [] |
| CSV válidos (columnas constantes) | OK | 48 CSV; [] |
| matriz_validacion_campo.csv = DPV central (IDs) | OK | 177 = 177 |
| Nivel N1–N4 idéntico en matriz y registro | OK | [] |
| Matriz: CRLF preservado y 18 columnas | OK |  |
| Matriz: estados sin cambio (todas NO INICIADO) | OK |  |
| URLs nuevas no duplicadas | OK | duplicados preexistentes: 2 |
| FTE nuevas siguen [PVDP] | OK |  |
| Referencias SUP/DPV/DEC/FTE en 00_gestion definidas | OK | [] |
| Enlaces relativos resuelven (00, 14, 19, 20, 25) | OK | [] |
| C0–CF: preset CAPEX == configuración CAPEX dentro de OPEX | OK |  |
| C0–CF: misma cadena ARQUITECTURA en CAPEX y OPEX por escenario común | OK | 20 escenarios comunes |
| Mapa de arquitecturas: 5 bases + variantes + M0–MF, ninguna COSTEABLE | OK | 29 filas |
| CAPEX/OPEX no duplican preoperativos (ningún PRE-* ni ID de la base CAPEX en OPEX) | OK |  |
| OPEX no recarga aranceles de importación (solo tasas SENASA, CAL-SENASA) | OK |  |
| Capital de trabajo no contiene stock ajeno ni con propiedad PENDIENTE | OK | 368 filas de inventario; 63 ajenas/pendientes excluidas |
| CAPITAL_TRABAJO = PENDIENTE en todos los escenarios | OK | 29 escenarios |
| Montos E4 siguen no comparables (OPEX) | OK |  |
| CAPEX: ningún monto con evidencia E1–E3 y sin total | OK |  |
| OPEX: sin total ni costo unitario | OK |  |
| Faltante no se vuelve cero (BOQ y registro OPEX) | OK | 0/0 |
| Precio observado separado de conversión (pollito, maíz) | OK |  |

### 14.1 Archivos modificados (60)

- `00_gestion_proyecto/interfaz_capex_finanzas.md` — creado
- `00_gestion_proyecto/interfaz_opex_finanzas.md` — creado
- `00_gestion_proyecto/mapa_arquitecturas_economicas.csv` — creado
- `00_gestion_proyecto/matriz_completitud_economica.csv` — creado
- `00_gestion_proyecto/reconciliacion_sesiones_16_17.md` — creado
- `00_gestion_proyecto/datos_por_validar.md` — modificado
- `00_gestion_proyecto/decisiones_pendientes.md` — modificado
- `00_gestion_proyecto/estado_proyecto.md` — modificado
- `00_gestion_proyecto/glosario.md` — modificado
- `00_gestion_proyecto/matriz_validacion_campo.csv` — modificado
- `00_gestion_proyecto/supuestos.md` — modificado
- `14_alimento_balanceado/integracion_upstream.md` — modificado
- `19_capex/README.md` — modificado
- `19_capex/actualizaciones_gestion_16.md` — modificado
- `19_capex/arquitecturas_inversion.md` — modificado
- `19_capex/base_costos_capex.csv` — modificado
- `19_capex/boq_capex.csv` — modificado
- `19_capex/conclusiones_capex.md` — modificado
- `19_capex/escenarios_capex.csv` — modificado
- `19_capex/estructura_capex.md` — modificado
- `19_capex/evidencia_costos.md` — modificado
- `19_capex/expansion_capex.csv` — modificado
- `19_capex/expansion_capex.md` — modificado
- `19_capex/logistica_capex.md` — modificado
- `19_capex/mapa_drivers_capex.csv` — modificado
- `19_capex/maquinaria_capex.md` — modificado
- `19_capex/matriz_rfq_capex.csv` — modificado
- `19_capex/metodologia_capex.md` — modificado
- `19_capex/modelo_capex.py` — modificado
- `19_capex/obra_civil_capex.md` — modificado
- `19_capex/plan_cotizaciones.md` — modificado
- `19_capex/upstream_capex.md` — modificado
- `19_capex/utilities_capex.md` — modificado
- `20_opex/README.md` — modificado
- `20_opex/actualizaciones_gestion_17.md` — modificado
- `20_opex/base_costos_opex.csv` — modificado
- `20_opex/capital_trabajo.md` — modificado
- `20_opex/capital_trabajo_opex.csv` — modificado
- `20_opex/conclusiones_opex.md` — modificado
- `20_opex/costos_alimento.md` — modificado
- `20_opex/costos_calidad.md` — modificado
- `20_opex/costos_faena.md` — modificado
- `20_opex/costos_incubacion.md` — modificado
- `20_opex/costos_logistica.md` — modificado
- `20_opex/costos_mantenimiento.md` — modificado
- `20_opex/costos_produccion_primaria.md` — modificado
- `20_opex/costos_rrhh.md` — modificado
- `20_opex/costos_utilities.md` — modificado
- `20_opex/estructura_opex.md` — modificado
- `20_opex/evidencia_costos_opex.md` — modificado
- `20_opex/mapa_drivers_opex.csv` — modificado
- `20_opex/matriz_validacion_opex.csv` — modificado
- `20_opex/metodologia_opex.md` — modificado
- `20_opex/modelo_costo_laboral.csv` — modificado
- `20_opex/modelo_opex.py` — modificado
- `20_opex/ramp_up.md` — modificado
- `20_opex/registro_costos_operativos.csv` — modificado
- `20_opex/reglas_laborales_opex.csv` — modificado
- `25_fuentes/bibliografia.md` — modificado
- `25_fuentes/registro_fuentes.csv` — modificado

Los `actualizaciones_gestion_16/17.md` solo recibieron el encabezado de ARCHIVO HISTÓRICO; los `fuentes_16/17.csv` quedan sin cambios, como históricos. Los CSV de salida de `19_capex` y `20_opex` cambian solo por el reemplazo de IDs (regenerados por los modelos).


## 15. Próximos pasos

1. **Revisión de Ramiro** de esta rama (no se creó PR).
2. **Modelo financiero integral** (`21`), solo cuando el promotor lo indique: consumir las dos interfaces por período, con utilización y ramp-up como inputs, sin completar faltantes con cero; decidir antes el umbral de publicación (DEC-084) y el método de valuación de inventarios (DEC-089). Con la evidencia actual será un modelo **estructural** (EBITDA, VAN, TIR, payback NO PUBLICABLES).
3. **Evidencia económica prioritaria (sin cotizaciones formales todavía):** lectura primaria del Índice de costo SAGyP (FTE-311) y del A3500; USD/m² de obra por categoría (DPV-161); precio de terreno y conexiones en 2–4 corredores (DPV-087); alimento, pollito y granos puestos en planta (DPV-050, 047, 157); convenio y costo laboral (DPV-146, 148); tarifas eléctricas (DPV-052); contrato de integración (DPV-170); plazos comerciales (DPV-175).
4. **Cuando la fase lo habilite (H-B):** RFQ de paquetes con alcance de instalación e importación desglosados (DPV-160, 162, 163; DEC-081, 082).
5. **Modelos físicos faltantes** para upstream propio (dotación y consumos de granjas, incubadora y planta de alimento: DPV-176, 177) antes de que C3/CF puedan ser operativamente completas.
6. Retirar los archivos históricos `actualizaciones_gestion_16/17.md` y `fuentes_16/17.csv` queda a criterio del promotor (se conservan, como en las reconciliaciones 09, 12 y 14).
