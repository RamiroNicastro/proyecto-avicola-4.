# Plan de validación final — paquetes operativos de campo

**Fecha:** 2026-10-05 · **Origen:** sesión 21 (auditoría final del motor v1) · **Estado:** plan; **ningún** paquete iniciado, **ningún** DPV validado.

> Agrupa los DPV que hoy bloquean al motor en **12 paquetes operativos**, cada uno con un actor y un pedido concreto. No reemplaza el plan de campo de 2026-09-30 ([`plan_trabajo_campo.md`](plan_trabajo_campo.md): olas O0–O9, instrumentos y cuestionarios) ni la matriz ([`matriz_validacion_campo.csv`](matriz_validacion_campo.csv), una fila por DPV con método y evidencia requerida): los ordena según **qué bloque del motor desbloquean**. El detalle de cada DPV vive en [`datos_por_validar.md`](datos_por_validar.md).
>
> **Prioridad** (derivada del motor, no una preferencia de negocio): **P1** = sin ese paquete ningún indicador económico es publicable en ninguna arquitectura (bloquea 10 de 10 indicadores en 54/54 alternativas: [`../22_riesgos/prioridad_validacion.csv`](../22_riesgos/prioridad_validacion.csv)); **P2** = necesario para publicar flujo y VAN o para que una arquitectura sea costeable; **P3** = necesario para comparar arquitecturas o escalas; **P4** = optimización posterior. Dentro de una prioridad los paquetes están **empatados** (RANK_COMPARTIDO): no hay un orden interno, y la columna `POTENCIAL_DE_CAMBIAR_DECISION` sigue `NO_CALCULADO` hasta que exista un escenario con sensibilidades.

## 1. Mapa de paquetes

| # | Paquete | Prioridad | Actor principal | Bloques del motor que desbloquea | DPV centrales |
|---|---|---|---|---|---|
| 1 | CLIENTES | **P1** | Grupo inversor → compras de la red de supermercados; otros canales | DEMANDA, PRECIOS, CANALES, CT (cobro) | DPV-001, 002, 003, 018, 020, 036, 037, 038, 039, 040, 041, 085, 013, 070 |
| 2 | PLANTA / MAQUINARIA | **P1** (CAPEX) | Proveedores de línea, frío, efluentes y utilities (RFQ); frigoríficos en operación | CAPEX, DEPRECIACION, REPOSICION, capacidad | DPV-097, 088, 089, 095, 096, 109, 160, 162, 163, 167, 137, 083 |
| 3 | ALIMENTO | **P1** (OPEX) | Fábricas de alimento (venta y façon); acopios | OPEX:ALIMENTO_*, CT (propiedad de MP) | DPV-050, 155, 157, 117 |
| 4 | POLLITOS | **P1** (OPEX) | Incubadoras que venden a terceros | OPEX:POLLITO_COMPRADO / INCUBACION_PROPIA; gate POLLITO | DPV-006, 047, 133 |
| 5 | GRANJAS | **P1** (OPEX) | Productores integrables; integradores | OPEX:GRANJAS_*; gate PRODUCCION_PRIMARIA | DPV-019, 044, 048, 049, 051, 054, 170, 057 |
| 6 | UTILITIES | P2 | Distribuidoras de energía y gas; perforistas; laboratorios; plantas en operación | OPEX:UT-*, gates POTENCIA y AGUA, CAPEX de utilities y efluentes | DPV-052, 053, 067, 103, 108, 111, 114, 177 |
| 7 | TERRENO | P2 | Municipios; parques industriales; inmobiliarias rurales | CAPEX:TERRENO, gate TERRENO, localización | DPV-087, 106, 118, 119, 124, 141, 143, 161 |
| 8 | LOGÍSTICA | P2 | Transportistas; CD de la red; frío de terceros | OPEX:LOG-*, CANALES (costo logístico), gate TRANSPORTE | DPV-036, 042, 054, 116, 127, 135, 171 |
| 9 | RRHH | P2 | Contador laboral; cámara/sindicato; plantas en operación | OPEX:ESTRUCTURA y COSTO_LABORAL | DPV-082, 091, 092, 138, 146, 147, 148, 150, 176 |
| 10 | IMPUESTOS | P2 | Contador / estudio impositivo; ARCA; rentas provinciales; municipio | IMPUESTOS_INGRESOS, GANANCIAS, IVA | DPV-043, 169, 179 |
| 11 | FINANCIAMIENTO | P2 (flujo del accionista) | Grupo inversor; bancos; programas públicos; proveedores con financiación | FINANCIAMIENTO, DESCUENTO, CT (pago) | DPV-001, 175, 178 |
| 12 | EXPORTACIÓN | P4 (módulo futuro de mercado) | SENASA; importadores; certificadoras Halal | canal exportación; CAPEX/OPEX HAL-* | DPV-024, 026, 027, 030, 031, 032, 034, 035 |

Transversales que no son un paquete de campo: verificación documental primaria (DPV-009, normativa leída en original: DPV-046, 061, 066, 074, 090, 098, 099, 107) y ensayo de balance en planta (DPV-060, DEC-028), que define si los rendimientos del balance 04 pueden usarse en el modo evidencia.

## 2. Paquetes en detalle

Cada fila es un pedido operativo: **qué pedir**, en **qué unidad** y **qué modelo desbloquea**. Un interés verbal o un precio de prensa no completan un pedido (escala E1–E6 de [`guia_recoleccion_evidencia.md`](guia_recoleccion_evidencia.md)).

### 2.1 CLIENTES — P1

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Grupo inversor (reunión única, [`../24_inversores/cuestionario_ejecutivo_inversores.md`](../24_inversores/cuestionario_ejecutivo_inversores.md)) | Monto, forma y etapas del capital; relación con la red; rendimiento exigido y horizonte | USD; % anual; años | Restricción de capital, `TASA_DESCUENTO`, horizonte (DEC-007, DEC-010, DEC-098) |
| Compras de la red | Volumen por producto y local (12 meses), mix refrigerado/congelado, proveedor actual, CD y logística | kg/semana por producto y local | Demanda `DOCUMENTADA`/`NEGOCIADA` (categorías A/B) y mix; hoy demanda contable = 0 |
| Compras de la red | Lista de precios, descuentos, bonificaciones, fees, devoluciones, plazo de cobro, alta de proveedor | USD/kg (o ARS/kg con TC, fecha y tipo); %; días | `PRECIOS`, `CANALES`, CxC |
| Mayoristas, pollerías, gastronomía, industria | Volumen, especificación, precio y condiciones por producto (incluye coproductos y carcasa) | kg/semana; USD/kg; días | Colocación de las partes que la red no absorbe (ingreso total por ave) |
| Góndola y mayoristas | Precios observados por corte y canal (series) | USD/kg con fecha | Precio E1–E3 en `base_precios_venta.csv` |

### 2.2 PLANTA / MAQUINARIA — P1 para CAPEX

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Proveedores de línea (RFQ L1–L11, [`../19_capex/matriz_rfq_capex.csv`](../19_capex/matriz_rfq_capex.csv)) | Precio por paquete con Incoterm, alcance, instalación, commissioning, repuestos, garantía; **capacidad garantizada contractual**; lista de cargas; footprint; plazo de entrega y curva de pagos | USD; aves/h garantizadas; kW; m²; meses | `CAPEX`, `CURVA_DE_DESEMBOLSO`, gate CAPACIDAD_LINEA, POTENCIA, layout |
| Proveedores de frío y efluentes | Balance frigorífico por escala y perfil; tratamiento propuesto (superficie, energía, lodos) | kWf; m²; kWh/día; t MS/día | CAPEX de frío y efluentes; cierra la brecha ×5,7 (T16-04) |
| Frigoríficos en operación | Capacidad real vs nominal, disponibilidad, mantenimiento, arranque | aves/h sostenidas; % | Capacidad comercial ≠ nominal; ramp-up (DEC-090) |
| Fabricantes / contador | Vida útil contable y fiscal, valor residual, costo de reemplazo por clase de activo | años; USD | `DEPRECIACION`, `REPOSICION`, valor terminal (DEC-093) |

### 2.3 ALIMENTO — P1 para OPEX

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Fábricas que venden alimento | Precio por fase puesto en granja, fórmula de ajuste, plazo de pago | USD/t (o ARS/t con TC); días | OPEX:ALIMENTO_COMPRADO (C1) |
| Fábricas a façon | Tarifa de façon, quién compra la MP, dónde y cuántos días de stock, mínimo de lote, mermas | USD/t; días; t | OPEX:ALIMENTO_FACON (C0, C2); propiedad del stock (CT) |
| Acopios y molinos | Maíz y harina de soja puestos en planta, diferencial y flete | USD/t puesta en planta | OPEX:PLANTA_ALIMENTO_PROPIA (C3, CF); precio Rosario ≠ puesto planta (T17-02) |

### 2.4 POLLITOS — P1 para OPEX

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Incubadoras | Volumen disponible por semana, estacionalidad, calidad garantizada, precio y fórmula de ajuste, transporte, vacunas | pollitos/semana; USD/pollito; días | OPEX:POLLITO_COMPRADO; gate POLLITO |
| Incubadoras / genética | Huevo fértil: disponibilidad y precio (solo C3/CF) | huevos/semana; USD/huevo | OPEX:INCUBACION_PROPIA; gate HUEVO_FERTIL |
| Integradores | Sincronización incubadora–granja–faena; tamaño de lote | aves/lote; días | Chequeo de sincronización (REQUIERE VALIDACIÓN a escala chica) |

### 2.5 GRANJAS — P1 para OPEX

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Productores integrables | m² disponibles, estado y equipamiento de galpones, distancia, disposición a integrarse | m² de galpón; km | Gate PRODUCCION_PRIMARIA; logística de aves vivas |
| Productores / integradores | Contrato de integración: base de pago (por ave / kg vivo), ajustes por conversión y mortalidad, aportes de cada parte | USD/ave o USD/kg vivo | OPEX:GRANJAS_INTEGRADAS |
| Productores | Registros de 6–12 crianzas: peso, edad, FCR (con definición), mortalidad, decomisos | kg; días; kg/kg; % | Valores base de shocks (mortalidad, FCR); escenarios de 03 |
| Constructoras de galpones | Costo por tipo de galpón y equipamiento (solo C2, C3, CF) | USD/m² | CAPEX de granjas propias |

### 2.6 UTILITIES — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Distribuidora eléctrica | Potencia disponible, costo de ampliación, tarifa (energía y potencia) | kW; USD/kWh; USD/kW·mes | OPEX UT-ELE-*; gate POTENCIA |
| Distribuidora de gas / proveedor de GLP | Disponibilidad y tarifa | USD/m³ o USD/kWh térmico | OPEX UT-TER |
| Perforista / laboratorio / organismo hídrico | Caudal, calidad y permiso de agua; permiso y límites de vuelco | m³/día; mg/L | Gate AGUA; CAPEX de tratamiento |
| Plantas en operación | kWh/ave, gas/ave, agua/ave y caracterización del efluente; generación de lodos | kWh/ave; L/ave; kg DQO/día; t MS/día | Contraste del modelo top-down de 09C; lodos (TF-007) |
| Granjas, incubadoras y fábricas | Consumos de los universos upstream | kWh/año; m³/año | C3/CF operativamente completas (TF-058) |

### 2.7 TERRENO — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Municipios / parques industriales | Zonificación, retiros, FOS/FOT, distancias a viviendas, servicios disponibles, precio | m²; USD/m²; m | CAPEX:TERRENO (DEC-063); gate TERRENO; localización |
| Inmobiliarias / constructoras | USD/m² de obra civil por categoría | USD/m² con fecha y TC | CAPEX:OBRA_CIVIL |
| Organismos provinciales | Normativa ambiental, hídrica y de bomberos por sitio; riesgo hídrico | requisito por sitio | Gates condicionales de localización (sin ranking hasta tener evidencia) |

### 2.8 LOGÍSTICA — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Transportistas refrigerados | Tarifa por viaje/km/kg, capacidad real, ventanas | USD/viaje; t/vehículo | OPEX LOG-*; costo logístico por canal |
| Transportistas de aves vivas | Tarifa, capacidad (aves/camión), tiempos reales del ciclo, DOA | aves/camión; h; % | Flota de aves vivas; ventana prefaena (sensibilidad, no regla) |
| Frío de terceros | Tarifa de congelado y almacenamiento | USD/t·día | OPEX de C0 y variante congelado tercero |
| Receptores de subproductos | Densidad aparente y frecuencia de retiro | t/m³; retiros/semana | Vehículos de subproductos (límite por volumen) |

### 2.9 RRHH — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Contador laboral / convenio | Salario por categoría, cargas, ART, SAC, adicionales, beneficios, capacitación, EPP | ARS/mes con TC y fecha → USD/FTE-año | `COSTO_LABORAL` (plantilla vacía; el SAC es una regla de devengo, no un precio de mercado) |
| Plantas en operación | Factor de cobertura de nómina (ausentismo, vacaciones, francos), productividad por tarea, limpieza y mantenimiento reales | personas/puesto; aves/operario·h; h | Headcount de nómina (hoy PENDIENTE); FTE 14A ≠ dotación de la empresa integrada |
| Granjas, incubadoras, fábricas | Dotación de los universos upstream | FTE | C3/CF operativamente completas |

### 2.10 IMPUESTOS — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Estudio impositivo | IVA de ventas, compras y bienes de capital, plazo real de recupero; ganancias y quebrantos; amortización impositiva; IIBB por jurisdicción y su base (exportaciones); tasas municipales; regímenes de promoción | %; meses; años | `IMPUESTOS_INGRESOS`, `GANANCIAS`, `IVA` (TF-002, TF-005) |
| Proveedores (cada cotización) | Moneda original, fórmula de ajuste, fecha y TC | — | Exposición cambiaria (DPV-179, TF-003) |

### 2.11 FINANCIAMIENTO — P2

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| Grupo inversor | Capital comprometido (no el escenario de referencia de USD 2 M), etapas, política de dividendos y caja mínima | USD; % | Restricción de capital (DEC-098); DEC-094 |
| Bancos, programas públicos, leasing, proveedores | Monto, moneda, tasa con su tipo (efectiva/nominal y capitalización), plazo, gracia, garantías, comisiones, DSCR exigido | USD; % anual; meses | `FINANCIAMIENTO`, flujo del accionista, DSCR (DEC-092) |
| Clientes y proveedores | Días de cobro y de pago por canal y grupo de proveedor; días de stock | días | `CT` (DEC-091) |

### 2.12 EXPORTACIÓN — P4 (módulo futuro de mercado)

| Actor | Qué pedir | Unidad | Desbloquea |
|---|---|---|---|
| SENASA | Destinos habilitados por producto y requisitos para listar una planta nueva | requisito por destino | Canal exportación del motor (categorías A/B/C/D de acceso) |
| Importadores | Precio por producto y destino, volumen, condiciones | USD/t FOB | Precio de exportación E1–E3 (hoy 0) |
| Certificadoras Halal | Requisitos, costos y efectos en productividad | USD/año; % | Conceptos HAL-* de OPEX (variante C1-HALAL) y CAPEX futuro |

## 3. Qué cambia en el motor cuando llega cada paquete

- **Con CLIENTES + PLANTA + ALIMENTO + POLLITOS + GRANJAS** (todos P1) la primera arquitectura costeable podría publicar ingresos y EBITDA en modo evidencia, siempre que además se resuelva el uso de los rendimientos del balance 04 (DPV-060 o DEC-084).
- **Con UTILITIES, TERRENO, LOGÍSTICA, RRHH e IMPUESTOS** se completan OPEX y CAPEX y puede publicarse FCFF, VAN y TIR del proyecto (además de DEC-007 y DEC-093).
- **Con FINANCIAMIENTO** se publica el flujo del accionista y el DSCR.
- **Con dos o más arquitecturas o escalas costeables** el optimizador deja de ser `OPTIMIZACION_REAL_NO_DISPONIBLE` y Pareto, dominancia y robustez pasan a ser informativos (TF-010).
- Ningún paquete, por sí solo, decide la inversión: la decisión requiere además las decisiones de negocio abiertas (DEC-001, DEC-033, DEC-097, DEC-098, entre otras).
