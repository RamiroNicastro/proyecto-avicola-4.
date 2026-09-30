# Mapa regulatorio — autoridades y tipos de habilitación

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B (paralela) · Relacionado: [`habilitacion_planta.md`](habilitacion_planta.md), [`requisitos_sanitarios.md`](requisitos_sanitarios.md), [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md), [`subproductos_normativa.md`](subproductos_normativa.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv), [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md)

> **No es asesoramiento jurídico.** Es un mapa de trabajo para ordenar preguntas y dependencias.
> **Verificación:** el acceso directo a Infoleg, argentina.gob.ar, Boletín Oficial, digesto y biblioteca de SENASA y MAGyP estuvo **bloqueado** en esta sesión (`EGRESS_BLOCKED`, 2026-09-30; séptima sesión consecutiva, DPV-009). **Ninguna norma fue leída en su texto original.** Todo contenido normativo es `[PVDP]` (regla 16). Fuentes nuevas: [`fuentes_09B.csv`](fuentes_09B.csv) (`FTE-09B-##`); fuentes previas: `25_fuentes/registro_fuentes.csv`.
> **Sin localización:** nada de este mapa elige provincia ni municipio (DEC-003). Lo que depende del lugar se marca **[JURISDICCIÓN]**.

---

## 1. Tres ideas que ordenan todo el mapa

1. **Habilitación local ≠ habilitación federal (SENASA) ≠ habilitación para exportar a un destino ≠ planta listada por el país importador.** Son escalones sucesivos; cada uno exige el anterior y agrega requisitos propios ([`exportacion_y_certificaciones.md` §1](exportacion_y_certificaciones.md)).
2. **La habilitación sanitaria no reemplaza las habilitaciones locales** (uso de suelo, ambiental, vuelco, bomberos, comercial/industrial). La Res. SENASA 233/2026 (mar-2026) habría eliminado la **presentación** de habilitaciones municipales/provinciales en varios trámites de SENASA, pero según la prensa **no elimina la obligación de tenerlas** (FTE-09B-11, `[PVDP]`). Además, la ficha del trámite de habilitación de plantas de faena todavía lista el certificado de habilitación local y el de efluentes como requisitos (FTE-09B-02): **contradicción abierta** (§5).
3. **El régimen legal de fondo está en movimiento.** La Ley 22.375 (Ley Federal de Carnes) organizaba la convivencia de habilitaciones municipales/provinciales con el tránsito federal de SENASA. En dic-2023 se propuso derogarla (proyecto de ley "ómnibus", art. 240) para que SENASA sea el único habilitante; **no se pudo verificar si fue derogada ni por qué instrumento** (un extracto de buscador lo afirma sin citar norma; FTE-09B-10). Se trata como **vigencia no verificada**.

## 2. Mapa de autoridades

| Autoridad | Competencia posible sobre el proyecto | Nivel | ¿Depende de la ubicación? | Estado |
|---|---|---|---|---|
| **SENASA** (Dir. Nac. de Inocuidad y Calidad Agroalimentaria; Coordinación de productos de origen animal; Servicio de Inspección Veterinaria — SIV — en planta) | Habilitación e inscripción de la planta de faena, cámaras, elaboración, depósito; inspección veterinaria oficial permanente (ante y post mortem); aprobación de productos y rótulos (CAPA); certificación de exportación (SIGCER) y autorización de destinos (Res. 593/2026); habilitación de transportes (Res. 723/2025); Plan CREHA; granjas (RENSPA, Res. 1699/2019), DT-e; alimentos para animales (Res. 1415 y 1416/2024) | Nacional | No (norma nacional), pero **sí** el Centro Regional y la oficina local que interviene | `[PVDP]` FTE-016, FTE-09B-01/02/05/07/13/14 |
| **Secretaría de Agricultura, Ganadería y Pesca (SAGyP)** | Política sectorial; negociación de mercados junto con SENASA y Cancillería; programas de promoción; convenios Halal | Nacional | No | `[PVDP]` FTE-09B-18 |
| **Autoridad sanitaria/bromatológica provincial** (ministerio de producción o salud; en Santa Fe, ASSAl) | Habilitación de mataderos/frigoríficos de tránsito **provincial** (si la planta no fuera SENASA); control de comercialización y bromatología de productos no SENASA (p. ej., elaborados en comercio); convenios de equiparación con SENASA | Provincial | **Sí** | **[JURISDICCIÓN]** FTE-09B-24 |
| **Municipio** | Uso de suelo/zonificación, permiso de radicación/construcción (planos municipales), habilitación comercial/industrial, tasas, tránsito de camiones, olores y molestias; en algunos municipios, bromatología de venta minorista (carnicería) | Municipal | **Sí** | **[JURISDICCIÓN]** |
| **Autoridad ambiental provincial** (ej. en Buenos Aires el OPDS/Ministerio de Ambiente; en otras provincias, secretarías equivalentes — nombres **no verificados**) | Categorización industrial, evaluación de impacto ambiental / certificado de aptitud ambiental, residuos (especiales y no especiales), emisiones gaseosas, olores | Provincial (a veces delega en municipio) | **Sí** | **[JURISDICCIÓN]** |
| **Autoridad hídrica provincial** (ej. ADA en Buenos Aires — no verificado; organismos equivalentes en otras provincias) | Permiso de explotación de agua subterránea o superficial; permiso de vuelco de efluentes (a curso, colectora o suelo); prefactibilidad hídrica | Provincial | **Sí** | **[JURISDICCIÓN]** |
| **Prestadora de agua y cloacas** (si hay red) | Factibilidad de conexión y de vuelco a colectora; límites de vuelco propios | Local/provincial | **Sí** | **[JURISDICCIÓN]** |
| **Seguridad e higiene en el trabajo** (Ley 19.587 y Dto. 351/79 a nivel nacional —citadas de memoria, `[PVDP]`—; Superintendencia de Riesgos del Trabajo; ART; autoridad laboral provincial) | Condiciones de trabajo (ruido, frío, iluminación, amoníaco), servicio de higiene y seguridad, medicina laboral, protección contra incendio como requisito laboral | Nacional + provincial (policía del trabajo) | Parcial | `[PVDP]` — no relevado en esta sesión |
| **Bomberos / defensa civil** | Plan de protección contra incendio, certificado final de obra en materia de incendio, evacuación | Provincial/municipal | **Sí** | **[JURISDICCIÓN]** |
| **Energía eléctrica** (distribuidora; ente regulador provincial; CAMMESA solo para grandes usuarios) | Factibilidad de potencia, subestación, tarifa | Provincial | **Sí** | **[JURISDICCIÓN]** (coordinar con `12_energia_frio`) |
| **Gas** (distribuidora; ENARGAS para instalaciones) | Factibilidad, instalación de gas industrial (calderas, escaldado, chamuscado) | Nacional (ENARGAS) + distribuidora zonal | **Sí** | **[JURISDICCIÓN]** |
| **Refrigeración con amoníaco / recipientes a presión** | Habilitación de aparatos sometidos a presión (calderas, recipientes, sala de máquinas) | Provincial (en general, autoridad de trabajo o específica) | **Sí** | **[JURISDICCIÓN]** — no relevado |
| **ARCA – Dirección General de Aduanas** | Registro de importador/exportador ("Registros Especiales Aduaneros", DJ 420/R, garantía o solvencia), destinación de exportación | Nacional | No | `[PVDP]` FTE-09B-19 |
| **Cancillería / consejerías agrícolas** | Negociación de acceso, protocolos, auditorías de países importadores | Nacional | No | `[PVDP]` |
| **Autoridades del país importador** (UE DG SANTE, China GACC, Japón MAFF/MHLW, Corea MFDS/MAFRA, Arabia Saudita SFDA, EAU MoIAT) | Aceptación del sistema oficial argentino, listado de plantas, auditorías, requisitos de producto | Extranjero | No | Ver [`../17_exportacion/requisitos_planta_exportadora.md`](../17_exportacion/requisitos_planta_exportadora.md) |
| **Certificadoras privadas** (Halal, BRCGS, FSSC 22000, IFS; OAA como acreditador local) | Certificaciones voluntarias o exigidas por clientes/destinos | Privado | No | `[PVDP]` FTE-082, FTE-09B-18 |
| **INTI / laboratorios de la red SENASA** | Análisis de agua, producto, superficies (autocontrol) | Técnico | No | `[PVDP]` |

## 3. Tipos de habilitación (no son el mismo trámite)

| Actividad | Qué permite | Autoridad probable | Trámite distinto | Observaciones | Estado |
|---|---|---|---|---|---|
| **Faena con tránsito provincial / municipal** | Faenar y vender **solo dentro de la provincia** (o el municipio) | Provincia / municipio | Sí | Excluye venta al AMBA si la planta está en otra provincia; excluye exportación. Existencia y alcance del régimen dependen de la vigencia de la Ley 22.375 y de la adhesión provincial (§1) | **[JURISDICCIÓN]**; vigencia `[PVDP]` |
| **Faena con tránsito federal (SENASA)** | Faenar y vender en **todo el país** | SENASA | Sí (plantas de faena de animales terrestres "Ciclo I") | Plazo publicado 120 días hábiles (urgente hasta 30) desde la presentación completa (FTE-09B-02). **No habilita a exportar** | `[PVDP]` |
| **Elaboración** (trozado, deshuese, marinados, milanesas, chacinados, cocidos) | Producir productos con rubros específicos | SENASA si están en establecimiento SENASA; provincia/municipio en comercio minorista | Sí: se habilita **por rubro**; ampliar rubros es una **modificación** | La carnicería familiar probablemente está bajo bromatología municipal (a confirmar, DPV-09B-09) | `[PVDP]` |
| **Depósito frigorífico** (cámaras de terceros o propias fuera de la planta) | Almacenar productos de origen animal | SENASA (tránsito federal) o provincia | Sí | Relevante si se usa frío de terceros para exportación | `[PVDP]` |
| **Productos procesados / registro de producto** | Comercializar un producto con rótulo | SENASA (CAPA) vía TAD | Sí, **por producto** | Cada producto y presentación tiene número de registro (FTE-09B-14) | `[PVDP]` |
| **Subproductos no comestibles** (digestor, grasería, harinas) | Procesar sangre, plumas, vísceras | SENASA + ambiental + municipal | Sí | Ver [`subproductos_normativa.md`](subproductos_normativa.md) | `[PVDP]` |
| **Alimentos para animales** (pet food, harinas como ingrediente) | Elaborar/fraccionar/depositar alimentos para animales | SENASA (Res. 1416/2024 establecimiento; 1415/2024 producto) | Sí | Declaración jurada con inspección posterior (FTE-187) | `[PVDP]` |
| **Autorización de destino de exportación** | Exportar a un país determinado | SENASA (Res. 593/2026) | Sí, **por destino** | Requiere tránsito federal, rubros, productos CAPA, CREHA, trazabilidad y requisitos del destino | `[PVDP]` |
| **Listado por el país importador** | Que el importador acepte la planta | Autoridad extranjera, a propuesta de SENASA | Sí | Puede incluir auditoría presencial | `[PVDP]` |
| **Transporte** (aves vivas; productos; subproductos) | Circular con carga | SENASA (Res. 723/2025) | Sí, **por vehículo** | Aplica a vehículos propios y de terceros | `[PVDP]` |
| **Granjas** (si hay integración) | Criar y remitir aves a faena | SENASA (Res. 1699/2019; RENSPA) + municipio/provincia | Sí | Fuera del alcance de la planta, pero condiciona la recepción (DT-e) | `[PVDP]` FTE-146 |

## 4. Qué depende de la ubicación (aún no elegida)

| Tema | Por qué depende | Qué se necesita saber por candidata |
|---|---|---|
| Uso de suelo y zonificación | Ordenanzas municipales | Zona industrial, distancias a viviendas, factor de ocupación |
| Categoría ambiental y EIA | Leyes provinciales de radicación industrial | Categoría probable de un frigorífico avícola; plazo del certificado |
| Agua (captación) | Autoridad hídrica provincial | Permiso, caudal otorgable, calidad del acuífero |
| Vuelco de efluentes | Autoridad hídrica/ambiental; prestadora | Cuerpo receptor, límites de vuelco, canon |
| Residuos | Ley provincial de residuos especiales / sólidos | Clasificación de decomisos, lodos, contenido GI |
| Olores | Normativa municipal/provincial | Distancias, quejas, exigencias de biofiltros |
| Tránsito | Municipio y vialidad | Rutas habilitadas para camiones de aves vivas |
| Bomberos | Provincial/municipal | Certificado, reserva de agua contra incendio |
| Energía y gas | Distribuidora zonal | Potencia, gas industrial disponible, plazos de obra |
| Régimen provincial de faena | Adhesión a la ley federal; convenios con SENASA | Si existe habilitación provincial alternativa (DEC-009) |
| Incentivos | Leyes provinciales de promoción | No se analizan en esta sesión |

**Plantilla para comparar candidatas:** [`habilitacion_planta.md` §5](habilitacion_planta.md). No se completa: no hay candidatas (DEC-003).

## 5. Contradicciones y vacíos detectados

| # | Tema | Contradicción / vacío | Tratamiento |
|---|---|---|---|
| C1 | Habilitación local como requisito del trámite SENASA | Ficha del trámite (FTE-09B-02) y ficha "Faenador" (FTE-09B-21) exigen certificado local, efluentes y uso de suelo; la Res. 233/2026 (FTE-09B-11) eliminaría la presentación en "varios trámites" | Pendiente: confirmar si el trámite de plantas de faena está alcanzado. **En cualquier caso, la habilitación local sigue siendo obligación del operador** |
| C2 | Vigencia de la Ley 22.375 | Extracto: "ha sido derogada"; otras fuentes: solo **proyecto** de derogación (dic-2023) | **No se afirma derogación.** Consultar SENASA/asesor (P-01 de [`preguntas_senasa.md`](preguntas_senasa.md)) |
| C3 | Cantidad de capítulos del Decreto 4238/68 | Extracto: "30 capítulos"; otro extracto cita un "capítulo XXXII" de bienestar animal | Se usa solo lo confirmado por dos extractos (cap. XX aves; cap. XXXII bienestar); índice completo pendiente |
| C4 | Director Técnico | Referencias previas y la bibliografía técnica lo describen como obligatorio; Res. 592/2026 (jul-2026) derogó los numerales 1.7 y 9.2 | Prevalece la norma posterior (extracto oficial): **ya no obligatorio**, sí voluntario |
| C5 | Temperaturas de conservación de aves | Extractos con −2 a 2 °C (±2) refrigerado, "no superior a −4 °C" congelado y 7 °C en pechuga para enfriado por aire; la búsqueda devolvió también normativa brasileña | **No se adoptan**; posible confusión de origen ([`requisitos_sanitarios.md` §8](requisitos_sanitarios.md)) |
