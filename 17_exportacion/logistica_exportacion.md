# Logística de exportación de carne aviar

**Fecha de referencia:** 2026-09-29 · **Versión:** 1 (conceptual) · Relacionado: [`../13_logistica/README.md`](../13_logistica/README.md), [`../12_energia_frio/README.md`](../12_energia_frio/README.md), [`../10_localizacion/README.md`](../10_localizacion/README.md)

> **No se selecciona puerto ni ubicación de planta.** La comparación de puertos es conceptual (criterios). No se obtuvieron cotizaciones de flete ni costos portuarios: se registran como faltantes (DPV-027).
> **Verificación:** datos de extractos de buscador. Los parámetros técnicos de contenedores provienen en parte de sitios comerciales de exportadores brasileños `[PVDP · débil]`; deben confirmarse con navieras y operadores logísticos.

---

## 1. Flujo típico

```
Granja → Planta (faena, trozado, empaque) → Congelado (túnel / IQF) → Cámara de congelado (acumulación del lote)
       → Carga del contenedor reefer (en planta o en frigorífico de consolidación)
       → Transporte terrestre (camión portacontenedor con equipo de frío) → Terminal portuaria (conexión eléctrica del reefer)
       → Buque (tránsito marítimo; posible trasbordo) → Puerto de destino → Inspección sanitaria y aduana del importador
       → Cámara del importador → Distribución
```

| Etapa | Qué ocurre | Documentos / controles | Riesgo principal |
|---|---|---|---|
| Planta | Faena, proceso, empaque, rotulado por destino | Registros HACCP; lote identificado; certificado Halal por lote si corresponde | No conformidad de especificación |
| Congelado | El producto se congela **en planta**: el contenedor reefer **mantiene** la temperatura, no está diseñado para congelar | Registro de temperatura de producto | Producto que entra "tibio" al contenedor |
| Cámara | Acumulación hasta completar el contenedor | Control de stock por lote y fecha | Capital de trabajo inmovilizado; vencimientos |
| Carga | Pre-inspección y pre-enfriado del contenedor; carga con registradores de temperatura; precinto | Certificado sanitario SENASA; precinto oficial | Ruptura de frío durante la carga |
| Transporte terrestre | Camión con equipo de frío (*genset*) para el reefer | Documentación de tránsito | Fallas del equipo; demoras |
| Terminal | Conexión del reefer; monitoreo | Destinación de exportación en Aduana; permiso de embarque | Cortes de energía; congestión |
| Tránsito marítimo | 20–45 días según ruta (§4) | Conocimiento de embarque (B/L) | Fallas, trasbordos, demoras |
| Destino | Inspección sanitaria (puede incluir muestreo), aduana | Certificado sanitario original; certificado de origen; Halal | **Rechazo sanitario** o retención |

---

## 2. Contenedor reefer

| Parámetro | Referencia | Fuente | Estado |
|---|---|---|---|
| Tipos | 20', 40' y 40' High Cube refrigerados | FTE-135 (sitios comerciales) | [PVDP · débil] |
| **Carga típica de pollo congelado en 40'** | **~24–27 t** según producto, empaque y densidad de carga | FTE-135 | [PVDP · débil] |
| Temperatura de transporte de congelados | −18 °C o menor; los equipos alcanzan −25 °C (y "superfreezer" hasta −60 °C) | FTE-135 | [PVDP · débil] |
| Empaque | Cajas de ~10 kg (enteros en bolsa individual); cortes y menudencias en cajas o bloques de 10–20 kg | FTE-135, FTE-118 | [PVDP · débil] |
| Pallets | Carga paletizada (ej.: pallets europeos) o cajas a piso; el paletizado reduce la carga útil pero agiliza la operación | FTE-135 | [PVDP · débil] |
| Monitoreo | Registradores continuos de temperatura | FTE-135 | [PVDP · débil] |
| Disponibilidad | Argentina sufrió faltantes de reefers para exportar congelados (antecedente 2021) | Nota de prensa identificada en la búsqueda, no registrada | [PENDIENTE DE VALIDACIÓN] |

**Implicancia:** el **lote comercial mínimo es un contenedor de ~24–27 t** de un producto (o de un mix acordado con el comprador). Para partes de bajo peso por ave, completar un contenedor puede requerir semanas de acumulación según la escala (ver [`estrategia_valorizacion_ave.md` §3](estrategia_valorizacion_ave.md)).

---

## 3. Puertos — comparación conceptual

**Contexto:** en el 1S-2025 el Puerto de Buenos Aires movió 523.545 TEU y Exolgan (Dock Sud) 405.412 TEU; Zárate, 38.831 TEU hasta mayo; TecPlata (La Plata), 2.023 TEU hasta abril (FTE-134) `[PVDP]`. La carga en contenedores está **muy concentrada en Buenos Aires y Dock Sud**.

| Puerto / terminal | Fortalezas | Debilidades | Datos a relevar |
|---|---|---|---|
| **Puerto de Buenos Aires** (terminales de Puerto Nuevo) | Mayor frecuencia de servicios de línea y de navieras con reefer; mayor oferta de contenedores vacíos | Congestión urbana y accesos; costo de terminal | Servicios reefer por destino, conexiones, tarifas |
| **Dock Sud (Exolgan)** | 2° terminal del país; **~1.800 conexiones reefer**; plan de inversión de USD 150–180 M para buques mayores | Accesos del conurbano sur | Tarifas, frecuencia por destino |
| **Zárate (Terminal Zárate)** | Más cerca del corredor Entre Ríos–Buenos Aires (puente Zárate–Brazo Largo); menos congestión urbana | Volumen muy inferior (~5 % del de Buenos Aires); menor frecuencia de servicios; navegación fluvial y calado | Servicios reefer regulares, tarifas de exportación (hay tarifario público) |
| La Plata (TecPlata) | Capacidad disponible | Muy bajo movimiento actual | Servicios |
| Rosario y puertos del Paraná | Cercanía a la zona núcleo (granos) | Escasos servicios de contenedores reefer | Servicios |
| Puertos de Entre Ríos (Concepción del Uruguay, otros) | Cercanía al cluster avícola | Servicios de contenedores no relevados | Todo |
| **Camión a Chile** (paso Cristo Redentor y otros) | Sin buque; tiempo corto; mercado reabierto | Cierres de paso por nieve; costo por t | Tiempos, costos y frecuencia |

Fuentes: FTE-134 y análisis propio. **Criterios de comparación** para una fase posterior: frecuencia y cantidad de navieras con servicio reefer por destino; conexiones reefer; calado; costo total puerta–puerto (flete terrestre + terminal + flete marítimo); congestión; disponibilidad de contenedores vacíos; distancia a la planta (que depende de la localización, DEC-003).

---

## 4. Tiempos de tránsito (referencias indicativas)

| Ruta | Tiempo | Fuente | Estado |
|---|---|---|---|
| Santos (Brasil) → Jebel Ali (EAU) | 26–30 días | FTE-135 | [PVDP · débil] (referencia brasileña; Buenos Aires agrega días) |
| Shanghai → Buenos Aires (ruta inversa a Asia) | 30–45 días puerto a puerto | Sitios comerciales de logística (no registrados) | [PENDIENTE DE VALIDACIÓN] |
| Buenos Aires → Rotterdam, Japón, Corea, Vietnam, África | **No obtenidos** | — | DPV-027 |
| Argentina → Chile por camión | **No obtenido** | — | DPV-027 |

**Flete marítimo reefer:** no se obtuvieron tarifas de exportación desde Argentina. Las referencias encontradas corresponden a la ruta inversa (China → Argentina, contenedor seco) y **no son aplicables** a reefer de exportación (DPV-027).

---

## 5. Documentación típica

| Documento | Emite | Observación |
|---|---|---|
| Habilitación de planta y listado para el destino | SENASA / autoridad del importador | Condición previa (Res. SENASA 593/2026, FTE-083) |
| **Certificado sanitario internacional** | SENASA | Modelo acordado con cada país (UE: modelo oficial con atestaciones de sanidad, *Salmonella*, antimicrobianos, bienestar) |
| Destinación de exportación / permiso de embarque | Aduana (servicio aduanero de ARCA) | Registro de exportador; liquidación de divisas según el régimen vigente (a verificar, DPV-015) |
| Factura comercial y lista de empaque | Exportador | Incoterm (FOB, CFR, CIF) |
| Conocimiento de embarque (B/L) | Naviera | Documento de titularidad |
| Certificado de origen | Entidad habilitada | Necesario para preferencias (ej.: Chile; cuota UE–Mercosur) |
| **Certificado Halal** (planta y lote) | Certificadora reconocida por el destino | Arabia Saudita: por lote en plataforma SFDA (FTE-138) |
| Certificado de análisis | Laboratorio | Si lo exige el comprador o el destino |
| Póliza de seguro | Aseguradora | Si la venta es CIF o por política propia |
| Documentos de pago | Banco | Carta de crédito o cobranza documentaria; anticipos |

---

## 6. Seguros y cadena de frío

- **Seguro de transporte** (con cobertura de fallas de frío), **seguro de crédito a la exportación** (riesgo del comprador y del país; relevante en África) y eventual cobertura de rechazo en destino: **condiciones y costos no relevados** (DPV-027).
- **Puntos críticos de la cadena de frío:** entrada de producto no congelado al contenedor; tiempo de carga; corte de energía en terminal o en trasbordo; fallas del equipo en tránsito; demoras en destino. Los registros de temperatura son la prueba ante reclamos.

---

## 7. Ciclo de caja de una exportación (conceptual)

```
Faena → congelado (días) → acumulación del lote (días a semanas, según escala y producto)
      → traslado y embarque (días) → tránsito (20–45 días) → cobro (al embarque, contra documentos o a plazo)
```

- Entre la faena y el cobro pueden pasar **1 a 3 meses** `[ESTIMACIÓN conceptual]`, frente a plazos del mercado interno que dependen del canal (los supermercados suelen pagar a plazo: DPV-003). Es **capital de trabajo adicional** que debe compararse en el net-back (ver [`estrategia_valorizacion_ave.md`](estrategia_valorizacion_ave.md)).
- Las condiciones reales de pago (anticipo, carta de crédito, cobranza) deben relevarse con compradores (DPV-032).

---

## 8. Implicancias (sin seleccionar ubicación)

1. La exportación ultramarina se hace en **contenedores reefer desde Buenos Aires o Dock Sud** en su gran mayoría; la distancia planta–puerto y la frecuencia de servicios por destino son criterios de localización (DEC-003).
2. Chile (y países limítrofes) permiten **logística terrestre**, con otro perfil de costos y lotes.
3. El **lote mínimo de un contenedor** y la necesidad de congelar y acumular condicionan la escala mínima para exportar partes de bajo peso por ave.
4. Los costos logísticos son decisivos para productos de bajo precio (menudencias, cuartos, CMS): sin cotizaciones no se puede saber si conviene exportarlos (DPV-027).
