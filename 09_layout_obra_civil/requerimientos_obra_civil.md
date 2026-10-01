# Requerimientos conceptuales de obra civil

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 12C) · Fase 0

> **Alcance:** qué **exigencias** debe cumplir la obra civil de cada zona (cualitativas), qué datos hacen falta para especificarla y qué cuestiones deben resolverse antes de un anteproyecto. **No** es una especificación técnica, **no** fija materiales, espesores, cotas, luxes, temperaturas ni pendientes, **no** calcula costos. Los valores reglamentarios del Decreto 4238/68 y de la Res. SENASA 592/2026 **no fueron leídos en original** (DPV-090): todo requisito normativo es `[PVDP]` o "por consultar a SENASA". Base: [`../16_normativa_senasa/requisitos_sanitarios.md` §2](../16_normativa_senasa/requisitos_sanitarios.md) y [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md).

---

## 1. Requerimientos por zona

| Zona | Pisos | Muros y cielorrasos | Desagües | Ventilación / clima | Particularidades |
|---|---|---|---|---|---|
| **1 Sucia** (recepción, faena) | Impermeables, antideslizantes, resistentes a impacto, agua caliente y químicos; pendiente a rejillas | Lavables, zócalo sanitario | Gran caudal (escaldado, desplumado); canal de plumas; sangre **separada** | Andén con ventilación forzada y nebulización (bienestar); extracción de vapor en escaldado | Altura para riel aéreo y tramo de calma; luz tenue en colgado; balanza de camiones |
| **2 Transición** (evisceración) | Idem; resistentes a grasa | Idem, color claro | Canal o vacío de vísceras; bajo caudal de sólidos al colector | Aire que **no** venga de la sucia | Puestos de inspección con iluminación diferenciada (valor a leer), lavamanos, esterilizadores; acceso del servicio oficial |
| **3 Limpia** (enfriamiento, corte, empaque) | Idem; aptos para frío y tránsito de carros/autoelevadores eléctricos | Paneles aislantes lavables; sin condensación | Pendiente **de limpio a sucio** | Refrigerada; **sobrepresión** respecto de la sucia (buena práctica) | Chiller pesado (losa, fosos); esclusa de envases; sub-zona seca de empaque |
| **3b Apoyo seco** | Industrial seco | Estándar | Mínimos | Ventilada | Racks; acceso de camión de insumos |
| **4 Fría** (cámaras, túneles) | **Aislación de piso y prevención de congelamiento del suelo** en cámaras de congelado (calefacción de contrapiso o ventilación bajo losa: a definir) | Paneles aislantes; barreras de vapor | Desagües de descongelamiento | Antecámaras; cortinas | Altura útil para racks (densidad de estiba, DPV-142); losa para cargas de racks |
| **5 Despacho** | Industrial, frío | Paneles | — | Abrigo/sello de dock | Niveladoras; altura de andén según camión (12B) |
| **6 Subproductos** | Muy resistentes, lavables | Lavables | Lavado de contenedores y tolvas; contención de derrames de sangre | Extracción; olores | Báscula; tanque de sangre cerrado; sala de decomisos con cierre |
| **7 Utilities** | Industrial; bateas de contención (químicos, combustibles) | Estándar; **sectorización contra incendio** donde corresponda | Separados | Ventilación de sala de máquinas (y detección si hay amoníaco, DPV-110) | Fundaciones de compresores, caldera, generador; acceso para recambio de equipos |
| **Efluentes** | Obras de hormigón estancas; lagunas con impermeabilización | — | Llegada por gravedad (cota baja) si el terreno lo permite | Control de olores | Distancia a viviendas; acceso de camión de lodos |
| **8 Personal** | Lavables | Lavables | Sanitarios | Ventilación | Vestuarios separados por zona y sexo; filtros sanitarios (pediluvio, lavamanos, lavabotas) |
| **9 Administrativa** | Estándar | Estándar | Sanitarios | Climatización | Oficina SENASA con sanitario propio (práctica, `[PVDP]`) |
| **Exterior** | Pavimento para camiones pesados en playas y caminos; plataforma de lavado de camiones con desagüe al pretratamiento | — | **Pluviales separados** de industriales | — | Cerco perimetral; iluminación; control de plagas (MIP) |

## 2. Requerimientos transversales

| Tema | Requerimiento conceptual | Dato o decisión que falta |
|---|---|---|
| **Estudio de suelo** | Capacidad portante (equipos pesados, racks), napa freática (fosos, lagunas), riesgo de anegamiento | Por terreno (12A, ficha de relevamiento) |
| **Cotas y escurrimiento** | El tratamiento en la cota más baja; edificio sobre el nivel de inundación | Topografía; riesgo hídrico (DPV-106) |
| **Altura libre** | Riel aéreo de faena, túnel de aire, racks de cámaras | Huellas y alturas de proveedores (DPV-137, DPV-142) |
| **Cargas sobre losa** | Chiller, túneles, compresores, racks | Pesos y cargas puntuales del RFQ |
| **Incendio** | Sectorización (paneles aislantes combustibles o no, sala de máquinas, depósito de cartón), reserva de agua, salidas | Normativa de bomberos por sitio (DPV-106) |
| **Higiene y seguridad laboral** | Vestuarios, sanitarios, iluminación, salidas de emergencia, ergonomía de puestos | Ley 19.587 y reglamentaciones (no leídas; DPV-106) |
| **Control de plagas** | Cerramientos sin huecos, mallas, cortinas de aire | Programa MIP (BPM) |
| **Exportación (UE como hipótesis, SUP-015)** | Flujos más estrictos, segregación de lotes, registros de temperatura | DPV-145, DEC-012 |
| **Halal (preservar posibilidad)** | Posible separación de aturdido/degüello y de lotes; no se construye nada específico | DPV-034 |
| **Expansión** | Muros de ampliación, vanos de montaje, troncales con derivaciones ciegas, losa prevista | [`estrategia_expansion.md` §2](estrategia_expansion.md) |
| **Aprobación previa** | Planos sometidos a SENASA antes de construir (si existe instancia) | DPV-115, DEC-042 |

## 3. Datos que la obra civil necesita y no existen

| Dato | Para qué | Quién lo da | Registro |
|---|---|---|---|
| Huella, altura, peso, fosos, vanos y servicios de cada equipo | Salas, losas, alturas | Proveedores (RFQ lote 1 y 8) | DPV-137 |
| Dotación por turno, por zona y por sexo | Vestuarios, comedor, estacionamiento | `18_recursos_humanos` | DPV-138 |
| Requisitos edilicios del servicio oficial y del Decreto 4238/68 | Oficina, puestos, sala de decomisos, iluminación, pasillos | SENASA; texto original | DPV-090, DPV-140 |
| Retiros, FOS, FOT, alturas, distancias a viviendas | Terreno mínimo y ubicación | Municipio / provincia | DPV-141, DPV-106 |
| Densidad de estiba, racks, altura útil | m² de cámara | Proveedores de frío y racks | DPV-142 |
| Tecnología y geometría del tratamiento de efluentes | Terreno de efluentes | Proveedores; límites de vuelco del sitio | DPV-144, DEC-043 |
| Reserva de incendio y sectorización | Tanques y muros | Bomberos | DPV-106 |
| Camiones: aves por camión, t por camión, frecuencia, tipo de dock | Bahías, docks, playas | 12B / transportistas | DPV-084, DPV-036 |
| Lavado y desinfección de camiones (requisitos) | Plataforma de lavado | Res. SENASA 723/2025 (`[PVDP]`) | DPV-058 |
| Superficies reales de plantas argentinas por escala | Calibrar los proxies | Visitas (guía de visita) | DPV-143 |

## 4. Qué no se hace en esta fase

No se elige sistema constructivo (hormigón, metálico, paneles), no se fija cota de piso ni altura, no se dimensionan estructuras, no se diseñan instalaciones, no se selecciona contratista ni proveedor, no se calcula costo (CAPEX en `19_capex`, no iniciado).
