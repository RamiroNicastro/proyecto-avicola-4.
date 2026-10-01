# Regiones preliminares (provincia + corredor)

**Fecha:** 2026-10-01 · **Versión:** 1.1 (auditoría metodológica) · **Sesión:** 12A · Criterios en [`criterios_localizacion.md`](criterios_localizacion.md) · Datos en [`matriz_localizacion.csv`](matriz_localizacion.csv)

> **Ninguna región está elegida ni descartada.** Las 13 regiones son **ámbitos de búsqueda** definidos por un eje vial y un ecosistema (SUP-12A-01). El "centro de referencia" sirve solo para medir distancias de orden de magnitud; no indica dónde iría la planta. Las cifras provienen de registros ya existentes del proyecto y están `[PVDP]` (acceso a fuentes primarias bloqueado, DPV-009; reconfirmado el 2026-10-01).

---

## 1. Universo y criterio de inclusión

- **Provincias pedidas:** Buenos Aires, Entre Ríos, Santa Fe, Córdoba y Chaco (DEC-003).
- **Por qué estas cinco tienen sustento** (no solo intuición): en **2024**, dentro del universo **faena habilitada por SENASA**, Entre Ríos representó ~50,90 %, Buenos Aires ~34,89 %, Santa Fe ~5,09 % y Córdoba ~4,49 % (≈ 95,4 % entre las cuatro; tabla oficial de SAGyP "Faena Provincial 2024–2025", FTE-12A-015: **confirmado en revisión externa del proyecto; lectura directa pendiente en este entorno**). Son además núcleo de granos. Chaco se incluye por pedido del promotor y por su producción de granos y baja densidad avícola (hipótesis), **no** por el contacto personal (§6). *No mezclar universos:* la publicación de SENASA del 2024-07-02 indica que casi el 90 % de la **actividad avícola** se concentra en Entre Ríos y Buenos Aires (FTE-12A-017): es otro universo, no la participación en la faena; y ninguno de los dos es producción primaria. El extracto de FTE-001 (2025) es otro año y no se suma ni se compara sin verificar (regla 18). Estos porcentajes son **provinciales**: no se usan para puntuar corredores (ECO-01, agregado provincial).
- **Referencia secundaria (fuera de la matriz):** **Río Negro** representó aproximadamente **2,4 % de la faena nacional habilitada por SENASA en 2024**, según la tabla oficial de la Secretaría de Agricultura (FTE-12A-015; confirmado en revisión externa del proyecto, lectura directa pendiente en este entorno). Eso justifica mantenerla como **referencia secundaria**, pero **no** implica descartarla ni incorporarla automáticamente a la matriz principal: está lejos de la zona núcleo de granos y del AMBA y su lógica conocida es el abastecimiento patagónico ([`../01_mercado/mercado_avicola_argentina.md`](../01_mercado/mercado_avicola_argentina.md) §3.1). Se incorporaría si el proyecto considerara un mercado regional patagónico o si la evidencia de corredor lo justificara.
- **No incluidas:** Salta, Mendoza, La Rioja, Jujuy (~2,7 % de la faena en conjunto, mercados regionales); Corrientes, Santiago del Estero, Tucumán, Uruguay u otras: **sin evidencia** en el proyecto que justifique agregarlas. Agregar una región exige al menos una fuente registrada que muestre actividad avícola, granos o logística relevante.

## 2. Tabla de regiones

Distancia a CABA = **orden de magnitud no medido** (SUP-12A-02, `[ESTIMACIÓN]` con estado `[PVDP]`); el modelo no la usa en modo estricto. Medición con ruteo pendiente (DPV-12A-01, coordinar con 12B).

| Código | Provincia | Corredor | Centro de referencia | km a CABA (orden) | Lógica de la región |
|---|---|---|---|---|---|
| BA-AMBA | Buenos Aires | Periurbano AMBA (2.ª–3.ª corona; Pilar, Escobar, Cañuelas, Luján) | Pilar | ~55 | Cercanía máxima al mercado y a la carnicería |
| BA-NORTE | Buenos Aires | Norte bonaerense (RN9/RN8: Zárate–Baradero–San Pedro–Arrecifes–Pergamino) | San Pedro | ~165 | Rutas principales, granos, nodo portuario de Zárate (servicios reefer a verificar), conexión con Entre Ríos |
| BA-OESTE | Buenos Aires | Oeste bonaerense (RN5/RN7: Mercedes–Chivilcoy–Bragado–Junín) | Chivilcoy | ~160 | Zona agrícola con rutas troncales y menor presión urbana que el AMBA |
| BA-INTERIOR | Buenos Aires | Centro y sur de menor presión urbana (RN3/RN205/RN226: Saladillo–Las Flores–Azul–Olavarría) | Azul | ~300 | Tierra y baja densidad; más lejos de puertos y granos de zona núcleo |
| ER-SUR | Entre Ríos | Sur entrerriano (RN14/RN12: Gualeguaychú–Gualeguay) | Gualeguaychú | ~230 | Puente entre el cluster entrerriano y el AMBA (Zárate–Brazo Largo) |
| ER-URUGUAY | Entre Ríos | Corredor del río Uruguay (RN14: C. del Uruguay–San José–Colón–Villa Elisa) | Concepción del Uruguay | ~320 | Cluster avícola principal del país |
| ER-CENTRO | Entre Ríos | Centro y oeste (RN12/RN18: Paraná–Crespo–Nogoyá–Villaguay) | Paraná | ~470 | Segunda área avícola entrerriana; vínculo con Santa Fe |
| SF-SUR | Santa Fe | Gran Rosario y corredor del Paraná (RN9/RN33/RN34/A008) | Rosario | ~300 | Molienda de soja, granos, puertos del Gran Rosario (servicio de contenedores reefer a verificar por nodo), gran mercado regional |
| SF-CENTRO | Santa Fe | Centro santafesino (RN19/RN34: Santa Fe–Esperanza–Rafaela) | Esperanza | ~490 | Agroindustria y un caso de integración avícola hasta el minorista |
| CBA-SUR | Córdoba | Sur cordobés (RN8/RN35/RN36: Río Cuarto) | Río Cuarto | ~600 | Maíz abundante; complejo avícola integrado existente |
| CBA-ESTE | Córdoba | Este cordobés (RN9/RN158: Marcos Juárez–Villa María–San Francisco) | Villa María | ~560 | Granos y agroindustria sobre corredores troncales |
| CH-ESTE | Chaco | Este chaqueño (RN11/RN16: Gran Resistencia) | Resistencia | ~1.020 | Mercado regional NEA; baja densidad avícola (hipótesis) |
| CH-CENTRO | Chaco | Centro chaqueño (RN16/RN95: Pcia. Roque Sáenz Peña) | Pcia. Roque Sáenz Peña | ~1.170 | Granos regionales; muy lejos del AMBA y de los nodos portuarios de contenedores de referencia |

## 3. Buenos Aires: cuatro lógicas distintas en una provincia

Buenos Aires no es una sola opción: comparte normativa provincial (p. ej., Autoridad del Agua, Res. ADA 336/2003, FTE-259 `[PVDP]`) pero no realidades.

| Lógica | Región | Qué gana | Qué arriesga | Preguntas que la decidirían |
|---|---|---|---|---|
| **Cercanía AMBA** | BA-AMBA | Distribución diaria corta; frescura; cercanía a la carnicería, a la red (si se valida) y a mayoristas | Suelo caro, presión urbana y vecinal, congestión, bioseguridad (granjas lejos o dispersas; tránsito de aves vivas por zonas pobladas), expansión limitada; antecedentes de plantas de GTA paralizadas en Pilar y Esteban Echeverría (FTE-035 `[PVDP]`: evento de mercado, no oportunidad asumida) | ¿Admite el municipio un frigorífico con ampliación? ¿Hay granjas a menos de ~2–4 h? ¿Conviene aquí la planta de faena, o este corredor sería el segundo nodo (CD o trozado) de una arquitectura de dos nodos? Son arquitecturas de red distintas, no se comparan en la matriz (DEC-12A-04) |
| **Norte bonaerense** | BA-NORTE | Rutas troncales (RN9), granos de zona núcleo, puerto de Zárate, conexión con el cluster entrerriano | Presión de usos industriales y logísticos en el tramo Zárate–Campana; antecedentes de planta de GTA en Capitán Sarmiento (FTE-035 `[PVDP]`) | ¿Productores disponibles a ambos lados del río? ¿Servicios reefer regulares en Zárate? |
| **Oeste** | BA-OESTE | Agricultura y rutas (RN5/RN7) a 2–3 h del AMBA; menor presión urbana | Ecosistema avícola a relevar; acuíferos con calidad a verificar (DPV-053) | ¿Hay granjas e incubadoras en radio? ¿Calidad de agua? |
| **Interior de menor presión urbana** | BA-INTERIOR | Tierra disponible, baja densidad (sanitaria y urbana), espacio para granjas propias | Distancia a granos de zona núcleo, a puertos y al AMBA; IAAP 2025–2026 en Ranchos (01_mercado §3.1, `[PVDP]`), cuya relación con este corredor no está georreferenciada | ¿Cuánto cuesta construir el ecosistema desde cero? ¿Logística de alimento? |

**Acceso a rutas principales** no se trata como región aparte: es una condición que debe cumplir cualquier corredor (LOG-01, LOG-02) y se verifica en cada municipio y terreno.

## 4. Fichas breves por provincia

Lo que se sabe proviene de registros existentes; todo `[PVDP]`. Lo que no se sabe es la mayor parte.

### Entre Ríos (ER-SUR, ER-URUGUAY, ER-CENTRO)

- **Sabido:** ~50,90 % de la faena habilitada por SENASA en 2024 (FTE-12A-015, confirmado en revisión externa; lectura directa pendiente) — dato provincial, no de corredor. `[PVDP]`: 23 plantas nacionales de faena de aves (FTE-072, año no identificado); 54–62,9 % de las granjas de parrilleros del país (fuentes en conflicto, DPV-023/DPV-055); mayor concentración industrial en los departamentos Colón, Uruguay y Gualeguaychú (FTE-072); cierre de la planta La China de GTA en Concepción del Uruguay (may-2026, FTE-081) e inversión de Las Camelias en granjas en Villaguay (FTE-081).
- **Implicancias:** ecosistema completo (genética, incubación, alimento, integrados, contratistas) **y** la mayor presión sanitaria y competencia por productores y personal. El cierre de La China **no** implica productores, personal o activos disponibles: debe relevarse (DPV-016).
- **No sabido:** productores integrables con capacidad ociosa, incubadoras con venta a terceros, límites de vuelco provinciales, calidad de red rural (casos de caídas de tensión, FTE-157 `[PVDP]`), servicios reefer en puertos entrerrianos.

### Buenos Aires (BA-AMBA, BA-NORTE, BA-OESTE, BA-INTERIOR)

- **Sabido:** ~34,89 % de la faena habilitada por SENASA en 2024 (FTE-12A-015, confirmado en revisión externa; lectura directa pendiente). `[PVDP]`: plantas de GTA paralizadas en Pilar, Capitán Sarmiento y Esteban Echeverría (FTE-035); casos de IAAP 2025–2026 (FTE-057, FTE-099); límite de vuelco a pluvial DQO ≤ 250 mg/L y prohibición de inyección a napa (Res. ADA 336/2003, FTE-259, extracto); Buenos Aires y Dock Sud como nodos logísticos de referencia para contenedores (FTE-134), a comparar con otras alternativas portuarias.
- **No sabido:** cantidad de plantas habilitadas y de granjas por partido; productores disponibles; calidad de acuíferos por corredor; disponibilidad de parques industriales que admitan frigoríficos.

### Santa Fe (SF-SUR, SF-CENTRO)

- **Sabido:** ~5,09 % de la faena habilitada por SENASA en 2024 (FTE-12A-015, revisión externa). `[PVDP]`: 6 plantas nacionales (FTE-072); caso de integración del grano al consumidor en Esperanza/Humboldt (Grupo Cem, FTE-047); casos de mortandad por calor y fallas eléctricas (FTE-157); el Gran Rosario tiene puertos de granos; su servicio de contenedores reefer aparece como escaso en un análisis preliminar del proyecto ([`../17_exportacion/logistica_exportacion.md`](../17_exportacion/logistica_exportacion.md) §3), **a verificar por nodo** (terminal, enchufes, frecuencia, destinos, cut-off, costos; DPV-12A-10): cercanía a puerto ≠ disponibilidad reefer ≠ servicio marítimo adecuado ≠ exportación habilitada; plan de equiparación de frigoríficos provinciales con SENASA (FTE-250).
- **No sabido:** granjas por radio, incubadoras, límites de vuelco provinciales, precio de maíz puesto en zona.

### Córdoba (CBA-SUR, CBA-ESTE)

- **Sabido:** ~4,49 % de la faena habilitada por SENASA en 2024 (FTE-12A-015, revisión externa). `[PVDP]`: 4 plantas nacionales (FTE-072); complejo Avex en Río Cuarto (incubación, alimento, granjas, faena), cedido a ACA e incluido en el concurso de GTA (FTE-040); IAAP 2026 en ponedoras (FTE-057).
- **Implicancias:** maíz abundante y lejos de los nodos portuarios de contenedores de referencia. La situación de Avex es un **evento de mercado**: no se asume disponibilidad de activos, capacidad a façon ni productores (CLAUDE.md, principios estratégicos).
- **No sabido:** casi todo lo regional (granjas, incubadoras, agua, vuelco).

### Chaco (CH-ESTE, CH-CENTRO)

- **Sabido `[PVDP]`:** no figura con participación propia en la faena habilitada por SENASA de la tabla 2024 recibida (FTE-12A-015); hay un relevamiento SENASA–provincia para equiparar frigoríficos con habilitación provincial (FTE-250); calor y humedad intensos que exigen galpones túnel y cooling ([`../03_produccion_primaria/galpones.md`](../03_produccion_primaria/galpones.md) §3.3, cualitativo).
- **Implicancias:** baja densidad avícola (ventaja sanitaria **hipotética**) y mercado regional NEA; a la vez, ecosistema avícola a construir (pollito, alimento, servicios), producto terminado a ~1.000 km del AMBA (orden de magnitud no medido) y lejos de los nodos portuarios de contenedores de referencia.
- **No sabido:** prácticamente todo. **Requiere relevamiento específico** antes de poder compararse (cobertura de información actual: 2–6 % del peso según el perfil, en modo exploratorio; [`conclusiones_localizacion.md`](conclusiones_localizacion.md) §5).

## 5. Granja Tres Arroyos y otros eventos de mercado

La crisis de GTA (concurso, plantas paralizadas en BA, La China cerrada en ER, Avex cedida en Córdoba) toca seis de las trece regiones. Separación obligatoria:

| Hecho registrado `[PVDP]` | Posible oportunidad (no asumida) | Qué habría que verificar |
|---|---|---|
| Plantas paralizadas o cerradas | Instalaciones existentes, personal con experiencia | Estado legal en el concurso, habilitaciones, estado técnico, deudas, conflictos gremiales (FTE-081) |
| Productores integrados sin integrador | Galpones con capacidad ociosa | Cuántos, dónde, en qué estado, con qué contratos (DPV-016, DPV-048) |
| Faena reasignada a otras empresas | Capacidad a façon o competidores más fuertes | Quién absorbió la faena (DPV-016) |

Ninguno de estos eventos suma puntos a una región en la matriz.

## 6. Factor cualitativo no puntuable: el contacto en Chaco

| Qué es | Qué **no** es |
|---|---|
| Ventaja cualitativa de **acceso / network**: facilita conseguir reuniones, información local y presentaciones con actores de la zona (SUP-014) | Beneficio económico; facilidad regulatoria; reducción de plazos; recomendación de ubicación; criterio físico |

- Se registra **separado de los criterios físicos** y no tiene peso en ningún perfil (el modelo rechaza un peso > 0 en NETWORK; test T08).
- Uso correcto: priorizar, **si Chaco entra en la lista corta**, que el relevamiento de campo allí sea más rápido y barato. Uso incorrecto: inclinar la matriz a favor de Chaco o suponer que habilitaciones, terrenos o incentivos serán más fáciles.
- La misma regla vale para cualquier otro contacto en otra provincia.

## 7. Qué faltaría para pasar de región a municipio

Para cada región que entre a la lista corta (DEC-12A-06): mapa de granjas, incubadoras, fábricas de alimento y plantas en radio (DPV-023, DPV-047, DPV-050); productores integrables (DPV-048); distancias y tiempos medidos (DPV-12A-01); autoridad hídrica y límites de vuelco (DPV-067, DPV-106); distribuidoras eléctrica y de gas (DPV-052, DPV-087); parques industriales que admitan frigorífico (DPV-12A-04); riesgo hídrico (DPV-12A-03). Recién con eso se completa la plantilla jurisdiccional de 14 temas por municipio ([`../16_normativa_senasa/habilitacion_planta.md`](../16_normativa_senasa/habilitacion_planta.md) §5).
