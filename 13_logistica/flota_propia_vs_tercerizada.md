# Flota propia vs tercerizada vs híbrida — comparación conceptual

**Fecha:** 2026-10-01 · **Versión:** 1.0 · Sesión 12B · Fase 0

> **No se decide** flota propia ni tercerizada, **no** se selecciona transportista ni se cotiza (DEC-12B-02, abierta). Se comparan conceptualmente las tres modalidades para cada tipo de flujo y se definen los **criterios** con los que se decidirá cuando existan datos de costo, oferta y escala.

---

## 1. Definiciones

| Modalidad | Qué es | Variantes |
|---|---|---|
| **OWN (propia)** | La empresa compra o arrienda los vehículos y emplea a los choferes (o contrata choferes con vehículo dedicado bajo su control operativo) | Compra; leasing; alquiler de largo plazo sin chofer |
| **OUTSOURCE (tercerizada)** | Un transportista u operador logístico presta el servicio con sus vehículos y personal | Por viaje (spot); por contrato con tarifa; dedicado exclusivo; servicio incluido por el proveedor (p. ej. incubadora que entrega pollitos, fábrica que entrega alimento, receptor que retira subproductos) |
| **HYBRID (híbrida)** | Núcleo propio para la carga base o crítica + terceros para picos, estacionalidad o rutas específicas | Propia para aves vivas + tercerizada para distribución; dedicada contratada + spot |

## 2. Uso de flota que muestra el modelo (sin costos)

Caso de **sensibilidad** (radio 100 km, 5.500 aves/camión, refrigerado P1 6 despachos/semana con 12 t y troncal a 300 km, congelado 2 despachos/semana; capacidades = barrido):

| Flujo | 2.500 | 5.000 | 10.000 | 20.000 | Comentario |
|---|---|---|---|---|---|
| Aves vivas: camiones · uso de la jornada en día de faena · uso semanal (7 × 12 h) | 1 · 51 % · 37 % | 1 · 51 % · 37 % | 2 · 51 % · 37 % | 3 · 68 % · 49 % | Dedicado por bioseguridad: no puede hacer otra carga; trabaja solo los días de faena |
| Refrigerado troncal: camión-día por día de despacho | 0,88 | 0,88 | 1,76 | 2,64 | Ciclo de 10,6 h a 300 km |
| Congelado troncal: camión-día por despacho (2/sem) | 0,88 | 0,88 | 0,88 | 0,88 | Semanal y programable: buen candidato a tercero |
| Alimento: entregas/semana (~28 t) | 3 | 5 | 9 | 18 | Usualmente incluido por la fábrica (si es de terceros) |
| Subproductos: ocupación del retiro diario de plumas (10 t) | 6 % | 12 % | 24 % | 48 % | Habitualmente el receptor retira con su vehículo |

**Lectura:** a escalas de 2.500–5.000 aves/día casi ningún flujo llena un vehículo dedicado una jornada completa todos los días. Una flota propia **inmovilizada y subutilizada** es un riesgo económico (a cuantificar en `19`/`20`); al mismo tiempo, los flujos críticos (aves vivas, refrigerado) son los que más dependen del **control operativo**.

## 3. Comparación por tipo de flujo

| Flujo | OWN | OUTSOURCE | HYBRID | Sesgo conceptual (no decisión) |
|---|---|---|---|---|
| **Pollitos BB** | Vehículo climatizado especializado, uso semanal o por lote: muy baja utilización | Normalmente lo provee la **incubadora** (precio puesto en granja; DPV-047). Control de clima y horario en manos del proveedor | Propio solo si la incubadora es propia | Tercerizado / incluido en la compra mientras no haya incubadora propia (SUP-034) |
| **Aves vivas** | Control total de horarios, carga, bienestar y lavado; dedicación por bioseguridad; equipo especial (jaulas/módulos) y cuadrillas; utilización 37–49 % semanal | Contratistas de captura y transporte existentes en polos avícolas (DPV-054); riesgo de dependencia y de calidad de bienestar variable; menor inversión | Núcleo propio o contratado dedicado + contratista para picos (verano, +1 viaje) | **El flujo más crítico**: bienestar, DOA y coordinación con la línea. La decisión depende de la oferta de contratistas en la zona (12A) y de la escala |
| **Alimento a granel** | Solo con fábrica propia (DEC-024) | Incluido por la fábrica de terceros | — | Sigue a la decisión de fábrica de alimento |
| **Refrigerado — troncal** | Camiones grandes, ciclo diario, buena utilización si hay carga completa; marca visible | Transportistas refrigerados con habilitación SENASA; tarifa por viaje o por kg | Propio para la carga base + tercero para picos o rutas largas | Depende del modelo de distribución (DEC-016, DEC-12B-01) |
| **Refrigerado — reparto a tiendas** | Muchas rutas con baja carga por parada: **operación de distribución en sí misma** | Operadores de última milla refrigerada en el AMBA; distribuidores | Cross-dock de un operador + reparto tercerizado | Si no hay CD del cliente, la última milla propia es una segunda empresa (02 §3.2) |
| **Congelado** | Baja frecuencia (1–3 despachos/semana): utilización baja | Muy compatible con tercero (programable, carga completa) | — | Tercerizado salvo integración con el refrigerado |
| **Exportación** | No aplica (portacontenedor del forwarder/naviera) | Forwarder + transporte de contenedores | — | Tercerizado |
| **Subproductos** | Contenedores estancos, cisterna, volcador; habilitación específica; olores | El **receptor** suele retirar (DPV-065); su frecuencia y condiciones definen la logística | Contenedores propios + retiro del receptor (contenedor rotativo) | Tercerizado / del receptor, salvo rendering propio |

## 4. Criterios para decidir después (DEC-12B-02)

| # | Criterio | Indicador | Favorece OWN si… | Favorece OUTSOURCE si… |
|---|---|---|---|---|
| C1 | **Utilización** | Camión-día por semana / días disponibles | Uso > ~70 % de la jornada todos los días (umbral a definir con costos) | Uso bajo, irregular o estacional |
| C2 | **Criticidad para el producto o el animal** | Impacto de una falla (DOA, ruptura de frío, línea parada) | La falla detiene la planta o afecta bienestar | La falla es recuperable con stock o reprogramación |
| C3 | **Especialización y habilitación** | Equipos y permisos específicos (jaulas, frío, SENASA, subproductos) | Nadie en la zona los ofrece con calidad suficiente | Existe oferta habilitada y competitiva |
| C4 | **Oferta local** | Cantidad de transportistas por tipo en la zona (DPV-12B-14) | Mercado con 0–1 oferentes (dependencia) | Mercado con varios oferentes |
| C5 | **Riesgo de dependencia** | % del flujo en un solo proveedor | — | Se contratan ≥ 2 proveedores o un híbrido |
| C6 | **Capital** | Inversión inmovilizada vs capital disponible (regla 7) | Hay capital y uso alto | Capital escaso o prioridades en planta/granjas |
| C7 | **Control comercial y marca** | Visibilidad, servicio, datos de entrega | La entrega es parte de la propuesta de valor | El cliente recibe en CD y no valora la marca en el transporte |
| C8 | **Escalabilidad** | Facilidad para sumar viajes al crecer o en verano | Crecimiento previsible y continuo | Crecimiento por etapas inciertas |
| C9 | **Bioseguridad** | Exclusividad del vehículo y protocolo de lavado | Se requiere exclusividad que el mercado no garantiza | El contratista certifica lavado y exclusividad |
| C10 | **Costo total por t y por parada** (fase económica) | USD/t, USD/km, USD/parada (no calculados) | Menor costo total con utilización real | Menor costo total o costo variable deseado |

**Regla de trabajo:** la decisión se toma **por flujo**, no para toda la empresa; la integración vertical del transporte no se presume conveniente (regla 10).

## 5. Datos necesarios

Oferta de transportistas por tipo y zona (DPV-12B-14), tarifas de distribución (DPV-042), de captura y transporte de aves (DPV-054), de exportación (DPV-027); costos de vehículos, choferes (CCT 40/89), seguros, combustible (DPV-12B-06) y mantenimiento (fase `19`/`20`).
