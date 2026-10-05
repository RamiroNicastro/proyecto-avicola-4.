# Proyecto avícola integrado — Argentina

Repositorio documental y analítico para el estudio de **prefactibilidad** de una empresa avícola (pollo parrillero) verticalmente integrada en Argentina.

## Objetivo

Centralizar la investigación, los supuestos, las fuentes y los modelos que permitan evaluar de manera objetiva:

- si existe un negocio viable a partir de una carnicería familiar, un capital potencial de ~USD 2 millones y un canal comercial potencial (~90 supermercados, demanda no validada);
- qué eslabones de la cadena conviene desarrollar, comprar, tercerizar o postergar;
- una secuencia de inversión escalable, con miras a una eventual exportación.

Fase actual y avances: [`00_gestion_proyecto/estado_proyecto.md`](00_gestion_proyecto/estado_proyecto.md).
Reglas de trabajo (fuentes, clasificación de datos, unidades): [`CLAUDE.md`](CLAUDE.md).

## Estructura

| Carpeta | Contenido |
|---|---|
| `00_gestion_proyecto` | Estado, supuestos, decisiones pendientes, datos por validar, glosario |
| `01_mercado` | Mercado avícola argentino e internacional: producción, consumo, precios, competidores |
| `02_clientes_demanda` | Canal supermercados, carnicería, otros clientes; validación de demanda |
| `03_produccion_primaria` | Granjas de engorde, reproductoras, genética, sanidad, bienestar animal |
| `04_balance_masa` | Flujo de aves y kg a lo largo de la cadena; rendimientos |
| `05_proceso_industrial` | Faena y procesamiento: etapas, parámetros, calidad |
| `06_productos` | Portafolio: pollo entero, trozado, elaborados; especificaciones |
| `07_subproductos` | Menudencias, plumas, sangre, vísceras, harinas, cama de pollo |
| `08_maquinaria` | Relevamiento de equipos y proveedores (sin selección en Fase 0) |
| `09_layout_obra_civil` | Layouts, superficies, obra civil |
| `10_localizacion` | Criterios y alternativas de localización |
| `11_agua_efluentes` | Consumo de agua, tratamiento de efluentes, residuos |
| `12_energia_frio` | Energía eléctrica, gas, cadena de frío, refrigeración |
| `13_logistica` | Transporte de aves vivas, distribución, flota |
| `14_alimento_balanceado` | Formulación, insumos (maíz, soja), planta propia vs. compra |
| `15_incubacion` | Planta de incubación, huevo fértil, pollito BB |
| `16_normativa_senasa` | Habilitaciones, normativa sanitaria, ambiental, municipal |
| `17_exportacion` | Mercados destino, requisitos, habilitaciones |
| `18_recursos_humanos` | Dotación, perfiles, convenios, costos laborales |
| `19_capex` | Inversiones por etapa y eslabón |
| `20_opex` | Costos operativos |
| `21_modelo_financiero` | Flujo de fondos, escenarios, indicadores |
| `22_riesgos` | Matriz de riesgos y mitigaciones |
| `23_plan_expansion` | Etapas de crecimiento e integración |
| `24_inversores` | Material para el grupo inversor |
| `25_fuentes` | Bibliografía y registro de fuentes |
| `26_presentacion` | **Paquete ejecutivo V1**: presentación (PPTX/PDF), guion, resumen de 1 página y trazabilidad — ver [`26_presentacion/README.md`](26_presentacion/README.md) |
| `app` | **App V1** local sobre el motor (modo simple + experto): `python3 app/app.py` — ver [`app/README.md`](app/README.md) |

Cada carpeta temática (`01`–`24`) contiene un `README.md` con su alcance y preguntas clave.
