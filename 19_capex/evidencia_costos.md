# Evidencia de costos — niveles, reglas y estado de la base

**Fecha:** 2026-10-02 · Base: [`base_costos_capex.csv`](base_costos_capex.csv) · Fuentes nuevas: [`fuentes_16.csv`](fuentes_16.csv)

## 1. Niveles de evidencia (`NIVEL_EVIDENCIA`)

| Nivel | Nombre | Qué es | Requisito que el motor exige |
|---|---|---|---|
| **E1** | Cotización formal | Oferta vigente identificable de un proveedor para este proyecto | `TIPO_PRECIO = cotizacion`, fecha, fuente, lectura primaria del documento |
| **E2** | Precio directo de fabricante/proveedor | Lista o comunicación directa, no específica del proyecto | Fuente y lectura primaria |
| **E3** | Benchmark documentado | Proyecto comparable, paper, estudio, licitación, presupuesto público, fuente técnica **leída en original** | Fuente y lectura primaria |
| **E4** | Benchmark secundario / `[PVDP]` | Extracto de buscador, prensa, fuente comercial secundaria, referencia incompleta | Fuente |
| **E5** | Supuesto de ingeniería | Factor paramétrico sin precio observado (p. ej., un % de indirectos) | Fuente = documento del supuesto |
| **PENDIENTE** | Sin base | Sin precio | Precio vacío (nunca 0) |

Reglas verificadas por `validar_base()` y los tests E01–E08:

1. Sin precio ⇒ nivel PENDIENTE; con precio ⇒ E1–E5 (nunca PENDIENTE).
2. **Una página web nunca es E1** (E1 exige `TIPO_PRECIO = cotizacion`).
3. E1, E2 y E3 exigen `LECTURA_PRIMARIA = Sí`; un extracto o una URL bloqueada queda en E4 `[PVDP]` (regla 16 de CLAUDE.md).
4. Un rango (bajo/alto) exige `ORIGEN_RANGO`: no hay ±20 % automático.
5. Un precio en ARS u otra moneda exige tipo de cambio, fecha y tipo de TC.
6. Los niveles **no se mezclan**: cada fila conserva el suyo y el resumen informa montos separados `CAPEX_E1_E2_USD`, `CAPEX_E3_USD`, `CAPEX_E4_USD`, `CAPEX_E5_USD` (tests E03, N12). La v1.0 publicaba "CAPEX conocido" (E1+E2) y "CAPEX estimado" (E3+E4+E5); se eliminaron para no presentar referencias E4 como parte de un CAPEX económico.
7. `CALIDAD_MONTO` etiqueta el monto con precio: `SIN_MONTO`, `MONTO_COTIZADO_E1_E2`, `MONTO_MIXTO_CON_COTIZACIONES`, `MONTO_MIXTO_SIN_COTIZACIONES`, `MONTO_CON_REFERENCIAS_DEBILES_E4`, `MONTO_SOLO_SUPUESTOS_E5`. Hoy todos los escenarios con monto son **`MONTO_CON_REFERENCIAS_DEBILES_E4`**.
8. **Cobertura por nivel de evidencia** = conteo de conceptos E1/E2, E3, E4, E5 y pendientes (test N14). Es un conteo de conceptos, **no** un porcentaje económico.

## 2. Estado de la base (2026-10-02)

| | Cantidad |
|---|---|
| Conceptos en la base | **175** |
| PENDIENTE (sin precio) | **167** |
| Con precio | **8**, todos **E4** `[PVDP]` |
| …de ellos usados en el CAPEX inicial | **2** (OC-DP, GRA-GAL) |
| …usados solo en arquitectura FUTURA | 1 (REP-GAL) |
| …registrados como REFERENCIA no usada | 5 (ALI-REF, REF-MAL, REF-RAFS, REF-SOY, REF-EDI) |
| E1 / E2 / E3 / E5 | 0 / 0 / 0 / 0 |

## 3. Las 8 referencias con precio

| ID_COSTO | Valor | Fuente | Por qué ese nivel / uso |
|---|---|---|---|
| **OC-DP** | USD 250 / 300 / 350 por m² (nave industrial llave en mano, jun-2026, TC oficial) | FTE-310 | E4: blog comercial leído solo como extracto (sitio bloqueado). Usado **solo** para depósitos y talleres secos; IVA desconocido (alerta IVA_INCIERTO) |
| **GRA-GAL** | ≥ USD 11,49 por plaza (6.000.000 ÷ 522.000 aves/ciclo) | FTE-081 | E4: prensa ("más de USD 6 M"). **Cota inferior**, alcance desconocido; los 8 componentes de equipamiento quedan con alcance PENDIENTE para no contarlos dos veces |
| REP-GAL | ≥ USD 25,45–28,00 por plaza de reproductora (EE. UU.) | FTE-314 | E4; solo arquitectura futura |
| ALI-REF | USD 150.000–300.000 equipos de planta de alimento de 8–10 t/h | FTE-315 | E4; precio de **equipo** de fabricante, Incoterm desconocido: no es instalado. No se usa |
| REF-MAL | ARS 101.471.771 + IVA (2022), acondicionamiento de sala de faena aviar | FTE-312 | E4; sin TC, sin m², alcance desconocido: no convertible |
| REF-RAFS | USD 17.401–52.501 equipos de unidades móviles de 350–1.200 aves/h (EE. UU., 2015) | FTE-313 | E4; no comparable con una planta SENASA |
| REF-SOY | ~USD 300.000 por galpón | FTE-043 | E4; sin m² ni plazas |
| REF-EDI | USD 90–130/m² galpón cerrado estándar | FTE-310 | E4; no aplicable a áreas sanitarias ni de frío |

## 3 bis. Cobertura por nivel de evidencia (conteo de conceptos costeables de la empresa)

| Configuración (cualquier escala) | E1/E2 | E3 | E4 | E5 | Pendientes | Calidad del monto |
|---|---|---|---|---|---|---|
| C0 | 0 | 0 | 0 | 0 | 21 | SIN_MONTO |
| C1 | 0 | 0 | 1 (OC-DP) | 0 | 75 | MONTO_CON_REFERENCIAS_DEBILES_E4 |
| C2 | 0 | 0 | 2 (OC-DP, GRA-GAL) | 0 | 86 | MONTO_CON_REFERENCIAS_DEBILES_E4 |
| C3 / CF | 0 | 0 | 2 | 0 | 136 | MONTO_CON_REFERENCIAS_DEBILES_E4 |

Cuando entren cotizaciones, el mismo resumen mostrará cuánto del monto es E1/E2 sin mezclarlo con E4.

## 4. Por qué hay tan pocos precios

1. **No hay cotizaciones**: la fase no habilita RFQ (DEC-049, hito H-B).
2. **La red de la sesión bloqueó** todas las fuentes consultadas (oficiales y comerciales): ninguna pudo leerse en original. Se privilegiaron 7 referencias útiles frente a decenas de extractos débiles.
3. **No se inventan precios argentinos** (regla 3). Un precio de internet no se convierte en cotización ni en costo instalado.

## 5. Fuentes prioritarias para subir de nivel

| Prioridad | Fuente | Concepto | Nivel alcanzable |
|---|---|---|---|
| 1 | Cotizaciones RFQ (cuando la fase lo habilite) | Línea, frío, efluentes, eléctrico | E1 |
| 2 | Índice de costo de producción de pollo parrillero, SAGyP (FTE-311), leído en original | Galpones y equipamiento de granja | E3 |
| 3 | Licitaciones públicas de salas de faena y cámaras con pliego y cómputo (p. ej., FTE-312 leído) | Obra civil sanitaria y de frío | E3 |
| 4 | Listas de precios de concesionarios y carroceros | Vehículos | E2 |
| 5 | Consulta a constructoras con antecedentes en plantas alimentarias | USD/m² por categoría | E2 |
| 6 | Inmobiliarias y parques industriales de la lista corta de corredores | Terreno | E2 |
