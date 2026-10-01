# Terreno ideal para una planta avícola: requisitos conceptuales

**Fecha:** 2026-10-01 · **Versión:** 1.0 · **Sesión:** 12A · Relevamiento de cada terreno: [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md) · Filtros eliminatorios: [`criterios_localizacion.md`](criterios_localizacion.md) §4

> Este documento explica **qué debería tener** un terreno para una planta de faena y procesamiento avícola que pueda crecer por etapas. **No define cantidad de hectáreas**, no selecciona terreno y no reemplaza el layout del módulo 12C (`09_layout_obra_civil`, no modificado por esta sesión). El terreno de las **granjas** es otro problema (densidad, distancias sanitarias, DPV-057) y no se trata aquí.

---

## 1. Principio rector

El terreno es de lo **más barato de prever y más caro de corregir** ([`../23_plan_expansion/arquitectura_escalable.md`](../23_plan_expansion/arquitectura_escalable.md) §1): ampliar un edificio sin lugar obliga a mudarse; comprar el lote vecino después puede ser imposible. Por eso el terreno se piensa para la **escala final posible** aunque la obra arranque chica, siempre que la diferencia de precio lo justifique (decisión con CAPEX, DEC-035).

## 2. Qué debe contener el terreno (por función)

| Función | Qué ocupa | Qué la dimensiona | Fuente del dato |
|---|---|---|---|
| **Edificio de planta** | Recepción y colgado, faena, evisceración, enfriamiento, trozado, empaque, cámaras, expedición, vestuarios, oficinas, sala del SIV | Escala (aves/día), configuración (entero / trozado / deshuese, DEC-005), perfil refrigerado/congelado (P1–P3) | 12C (`09_layout_obra_civil`), `05_proceso_industrial` |
| **Zona sucia separada de zona limpia** | Flujos sin cruces de aves vivas, subproductos y producto terminado | Zonificación higiénica | [`../05_proceso_industrial/zonificacion_higienica.md`](../05_proceso_industrial/zonificacion_higienica.md) |
| **Playa de camiones de aves vivas** | Espera ventilada y sombreada, maniobra, ingreso por acceso propio | Camiones por día y por hora de llegada (0,4–5 camiones/día entre 2.500 y 20.000 aves/día, SUP-033) | [`../23_plan_expansion/escenarios_escala.md`](../23_plan_expansion/escenarios_escala.md) §12 |
| **Lavado y desinfección de camiones y cajones** | Playa con drenaje al tratamiento | Camiones por día; bioseguridad | [`../03_produccion_primaria/transporte_aves.md`](../03_produccion_primaria/transporte_aves.md) §7 |
| **Playa de expedición refrigerada** | Andenes con abrigo, maniobra de semirremolques y reefers | t/día de producto (6–48 t/día) y número de despachos | 12B, `12_energia_frio` |
| **Subproductos** | Carga de plumas, vísceras, sangre en contenedores; acceso separado | 1,5–12,2 t/día de subproductos sólidos que salen (trozado, escenario medio) | [`../07_subproductos/conclusiones_valorizacion.md`](../07_subproductos/conclusiones_valorizacion.md) |
| **Tratamiento de efluentes** | Pretratamiento, DAF, biológico (lagunas o reactores), lodos, punto de vuelco | Caudal (62–500 m³/día, sensibilidad) y carga; **la tecnología cambia la superficie en órdenes de magnitud** (lagunas: superficie "muy alta"; reactores: "baja") | [`../11_agua_efluentes/alternativas_tratamiento.md`](../11_agua_efluentes/alternativas_tratamiento.md) |
| **Servicios** | Sala de máquinas de frío, calderas, subestación y transformador, grupo electrógeno, tanques y potabilización de agua, aire comprimido, reserva de incendio | Lista de cargas y balance frigorífico (pendientes, DPV-095, DPV-109) | `12_energia_frio`, `11_agua_efluentes` |
| **Circulación interna** | Calles perimetrales, radios de giro, accesos separados (vivos / producto / subproductos / personal) | Tipo de camión y frecuencia | 12B, 12C |
| **Personal y visitas** | Estacionamiento, ingreso con barrera sanitaria | Dotación (pendiente, `18_recursos_humanos`) | — |
| **Barreras sanitarias** | Cerco perimetral, arco o vado de desinfección, ingreso único controlado | Bioseguridad y requisitos de habilitación | `16_normativa_senasa` |
| **Retiros y franja verde** | Distancia a linderos y a la calle; cortina forestal | Norma municipal y provincial (DPV-106) | Municipio |
| **Reserva de expansión** | Lugar para duplicar líneas, cámaras, tratamiento y playas | Arquitectura de crecimiento (DEC-033, DEC-035) | `23_plan_expansion` |

## 3. Atributos físicos deseables

| Atributo | Deseable | Por qué |
|---|---|---|
| **Forma** | Regular, con frente suficiente para accesos separados | Permite un flujo lineal (sucio → limpio) y crecer sin cruzar flujos |
| **Topografía** | Plana o con pendiente suave y conocida | Drenaje por gravedad hacia el tratamiento; menos movimiento de suelos |
| **Cota** | Por encima de su entorno, fuera de zonas inundables | Riesgo hídrico es filtro eliminatorio; el acceso también debe ser transitable con lluvia |
| **Drenaje** | Pluviales separados de efluentes industriales | Evita que una lluvia sobrecargue el tratamiento |
| **Suelo y napa** | Estudio de suelos; napa no superficial | Fundaciones de cámaras (cargas, congelamiento del suelo bajo cámaras de congelado), lagunas impermeabilizadas |
| **Accesos** | Pavimento hasta el predio; acceso directo a ruta sin atravesar zonas urbanas | Camiones de aves vivas de madrugada y reefers; seguridad vial y vecinal |
| **Servicios en el lindero** | Media tensión, gas natural, agua o acuífero apto, cuerpo receptor o colectora | Cada servicio ausente es una obra, un plazo y un riesgo (filtros eliminatorios) |
| **Vecinos** | Uso rural o industrial; viviendas lejos y a sotavento de los vientos predominantes | Olores, ruido, tránsito y amoníaco son la principal fuente de conflicto |
| **Linderos** | Terrenos vecinos disponibles o con opción de compra | Seguro de expansión |
| **Situación dominial** | Clara y verificada por profesional | Sin esto, nada de lo anterior sirve |

## 4. Superficie: qué se puede decir hoy y qué no

**No hay base suficiente para dar hectáreas** (`[PVDP]`, DPV-12A-09):

- No existe todavía la superficie del edificio por escala (módulo 12C en curso, sin modificar desde esta sesión).
- La superficie del tratamiento de efluentes depende de la tecnología (lagunas vs reactores, DEC-043), del tiempo de retención y de los límites de vuelco del sitio: puede ser la mayor superficie del predio o una fracción menor.
- La reserva de expansión depende de la arquitectura de crecimiento (DEC-033), que no está decidida.

**Cómo se calculará** (cuando existan los insumos):

```
superficie del terreno = edificio de planta (12C, por escala y configuración)
                       + playas y circulación (12B/12C: camiones/día, radios de giro)
                       + tratamiento de efluentes (11: tecnología, caudal, retención, módulos)
                       + servicios (12: sala de máquinas, subestación, calderas, generador, agua)
                       + subproductos y lavado de camiones
                       + estacionamiento y barreras sanitarias
                       + retiros y franja verde (norma local)
                       + reserva de expansión (23: arquitectura elegida)
```

**Qué sí se puede decir en términos relativos** (sin hectáreas): entre 2.500 y 20.000 aves/día se multiplican por ~8 los camiones de aves vivas, el producto despachado, los subproductos y el caudal de efluentes de sensibilidad (flujos lineales con la escala en los modelos de `23` y `11`). El edificio y los servicios **no** necesariamente crecen ×8 (hay elementos fijos y economías de escala), pero las playas y el tratamiento por lagunas tienden a crecer con el volumen. Por eso **la tecnología de efluentes y la escala final esperada son las dos variables que más mueven la superficie necesaria**.

**Escenarios de rango de superficie:** quedan **PENDIENTES** hasta tener la superficie por escala de 12C y una tecnología de tratamiento de referencia. Para no inventar cifras, la ficha de terreno pide la superficie **disponible** (dato del sitio) y la decisión se toma comparándola con la necesaria cuando esta exista.

## 5. Por qué un terreno barato puede ser caro

Un terreno de bajo precio puede requerir: extender la línea de media tensión varios kilómetros; perforar y potabilizar agua con arsénico; construir un acceso pavimentado; tratar efluentes a un nivel más exigente por falta de cuerpo receptor; rellenar por cota baja; enfrentar un conflicto vecinal que demore la habilitación; o quedar lejos de granjas, personal y servicios técnicos durante toda la vida de la planta. **El precio de la tierra se paga una vez; la mala localización se paga todos los días.** Por eso TER-02 (precio) se registra solo como DPV hasta tener cotizaciones y nunca se evalúa aislado.

## 6. Datos de terreno a levantar en campo

Los campos de la [`ficha_relevamiento_terreno.md`](ficha_relevamiento_terreno.md) cubren lo necesario. Prioridad para la lista corta (los primeros son eliminatorios):

1. Uso de suelo admitido y posibilidad de ampliación (por escrito).
2. Agua: caudal sostenible (ensayo de bombeo) y análisis de calidad.
3. Vuelco: cuerpo receptor, organismo, límites y permiso viable.
4. Energía: potencia disponible y ampliable (factibilidad escrita), calidad de red; gas natural.
5. Riesgo hídrico: cota, antecedentes de anegamiento, acceso con lluvia.
6. Vecinos: viviendas en radio, vientos predominantes, conflictos previos, postura municipal.
7. Superficie, forma, topografía, napa, linderos disponibles.
8. Distancias medidas a granjas, incubadoras, fábricas de alimento, rendering, SENASA, rutas y puertos.
9. Precio como `[COTIZACIÓN]` (moneda, fecha, condiciones; tipo de cambio si está en ARS, regla 2).
