# Ruta crítica de habilitación — dependencias conceptuales

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Sesión 09B · Relacionado: [`habilitacion_planta.md`](habilitacion_planta.md) §3, [`../23_plan_expansion/gates_expansion.md`](../23_plan_expansion/gates_expansion.md), [`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md), [`matriz_regulatoria.csv`](matriz_regulatoria.csv)

> Dependencias **conceptuales**, sin plazos ni costos (no hay datos jurisdiccionales ni respuestas de SENASA). No es un cronograma.

---

## 1. Reglas de precedencia ("no hacer X sin Y")

| # | No… | …sin antes | Por qué | Referencia |
|---|---|---|---|---|
| R1 | Comprar o alquilar terreno | Comprobar uso de suelo industrial, aptitud ambiental probable, agua (permiso), vuelco (cuerpo receptor), energía/gas y distancias a viviendas | Un terreno inapto es la decisión más cara e irreversible | [`habilitacion_planta.md` §5](habilitacion_planta.md) |
| R2 | Elegir el nivel de habilitación "por defecto" | Decidir DEC-009 (provincial vs federal vs federal preparada para exportar) con la ubicación de la demanda, el organismo que habilita cada rubro (P-40) y la aplicación actual de la Ley 22.375 y del Decreto 697/2026 (P-39, P-42) | Planta provincial fuera de Buenos Aires **no puede vender al AMBA**; subir de nivel después implica reformas | DEC-009 |
| R3 | Cerrar el layout | Leer el cap. XX y los capítulos generales del Decreto 4238/68 **y** obtener observaciones de SENASA sobre el anteproyecto | Flujos sucio/limpio, desagües, iluminación de inspección y espacios del SIV se fijan en obra civil | [`requisitos_sanitarios.md` §2](requisitos_sanitarios.md) |
| R4 | Diseñar la obra civil al estándar nacional mínimo | Evaluar el CAPEX incremental del estándar del destino más exigente previsible | Reformar una planta en operación para listarse es caro y detiene la faena | SUP-015, DEC-012 |
| R5 | Asumir exportación en el modelo de negocio | Conocer, por destino: país abierto, producto autorizado, exigencia de listado/auditoría y compradores | Mercado abierto ≠ planta habilitada | [`exportacion_y_certificaciones.md` §1](exportacion_y_certificaciones.md) |
| R6 | Fijar el método de enfriamiento (inmersión / aire) | Verificar límite de absorción de agua (Argentina) y exigencias de destinos | Cambia equipos, balance de masa, rótulo y compatibilidad exportadora | DPV-061 |
| R7 | Planificar rendering propio o dar por sentado un receptor | Verificar receptores habilitados y normativa de decomisos | Sin receptor habilitado, la faena se detiene o los subproductos son costo | [`subproductos_normativa.md`](subproductos_normativa.md) |
| R8 | Dimensionar la planta de efluentes | Conocer límites de vuelco del cuerpo receptor de la candidata | Los límites definen la tecnología de tratamiento | `11_agua_efluentes` |
| R9 | Contratar el proyecto ejecutivo | Tener la lista vigente de documentación y formato de planos que exige SENASA | Evita rehacer planos | P-07 de [`preguntas_senasa.md`](preguntas_senasa.md) |
| R10 | Iniciar obra | Tener aprobaciones locales (radicación, ambiental, construcción) **y** conformidad de SENASA al proyecto (si existe esa instancia) | Obra sin aprobación = riesgo de clausura o reforma. La Res. 233/2026 no elimina las aprobaciones locales | P-45, P-41 |
| R11 | Comprar equipos de faena | Validar requisitos sanitarios del equipo (materiales, higiene) y de bienestar (aturdimiento) | Equipos no conformes no se habilitan | Fase de maquinaria (no habilitada) |
| R12 | Lanzar productos con marca | Registrar productos y rótulos en CAPA | Sin registro no se comercializa con rótulo | FTE-241 |
| R13 | Integrar granjas | Verificar RENSPA, habilitación (Res. 1699/2019) y trazabilidad por lote | La planta no puede recibir aves sin DT-e | FTE-146 |
| R14 | Contratar transporte | Verificar habilitación SENASA de los vehículos (Res. 723/2025) | Aplica a propios y terceros | FTE-234 |

## 2. Cadena crítica (simplificada)

```
Demanda por jurisdicción (AMBA / otras) ─► DEC-009 nivel de habilitación
                                              │
Candidatas de localización (DEC-003) ─► Plantilla jurisdiccional ─► Terreno (R1)
                                              │
Lectura Decreto 4238 (cap. XX + generales) ─► Anteproyecto ─► Consulta SENASA (R3)
                                              │
Decisión estándar exportador (DEC-012) ───────┤
Método de enfriamiento (R6) ──────────────────┤
Receptores de subproductos (R7) ──────────────┤
Límites de vuelco (R8) ───────────────────────┘
                                              ▼
                         Proyecto ejecutivo (R9) ─► Aprobaciones locales + SENASA (R10)
                                              ▼
                         Obra y montaje (R11) ─► Inspección y habilitación federal
                                              ▼
                         Registro de productos (R12) ─► Operación con SIV
                                              ▼
                         Autorización de destinos (Res. 593/2026) ─► Listados/auditorías ─► Compradores ─► Exportación
```

## 3. Decisiones irreversibles o caras de corregir

| Decisión | Por qué es cara de corregir | Qué la desbloquea |
|---|---|---|
| **Terreno** | Inamovible; condiciona agua, vuelco, olores, tránsito, ampliación | Plantilla jurisdiccional completa por candidata |
| **Nivel de habilitación** | Pasar de provincial a federal o a exportador exige reformas y nuevo trámite | DEC-009 con demanda por jurisdicción |
| **Estándar higiénico de la obra civil** | Pisos, desagües, paneles y flujos no se cambian con la planta operando | Lectura del reglamento + CAPEX incremental (DEC-012) |
| **Separación de zonas y flujos** | Redibujar flujos obliga a demoler | Anteproyecto observado por SENASA |
| **Reserva de espacio** para congelado, deshuese, CMS, elaborados (crudo/cocido separados), rendering | Sin espacio en el terreno o la nave, se necesita otra planta | Arquitectura escalable (`23_plan_expansion`) |
| **Método de enfriamiento** | Equipos y rótulos | DPV-061 |
| **Planta de efluentes** | Obra civil grande; límites de vuelco | Datos de la candidata |
| **Sala de aturdimiento / recepción** | Bienestar y eventual Halal | DPV-034; requisitos UE |

## 4. Qué se puede hacer ya, sin ubicación

1. Conseguir y leer los textos primarios (lista en [`conclusiones_normativa.md` §10](conclusiones_normativa.md)).
2. Reunión técnica con SENASA / asesor de habilitaciones ([`preguntas_senasa.md`](preguntas_senasa.md)).
3. Definir DEC-009 con la información de demanda por jurisdicción.
4. Preparar la plantilla jurisdiccional para las regiones candidatas (DEC-003).
5. Relevar receptores de subproductos habilitados por región (F5 de `07_subproductos`).
