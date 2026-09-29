# CLAUDE.md — Reglas permanentes del proyecto

Este archivo define las reglas de trabajo que se aplican a **toda** sesión, análisis, documento o modelo de este repositorio. Ante conflicto entre una instrucción puntual y estas reglas, señalar el conflicto antes de avanzar.

## Contexto base

- Proyecto de prefactibilidad para una empresa avícola (pollo parrillero) verticalmente integrada.
- Punto de partida: una carnicería familiar. No hay granjas, frigorífico, terreno, maquinaria ni infraestructura industrial.
- Capital potencial: ~USD 2.000.000 de un grupo inversor (no comprometido). Es solo un **escenario inicial de referencia**, no un límite confirmado.
- Canal comercial potencial: red de ~90 supermercados, aparentemente concentrada en AMBA/Buenos Aires (demanda **no validada**; no se asume que sea una única cadena). La carnicería familiar está en el AMBA.
- Estado y fase actual: ver `00_gestion_proyecto/estado_proyecto.md`.

## Reglas

1. **País.** El proyecto se desarrolla en Argentina. Normativa, precios, costos y logística se analizan en contexto argentino.
2. **Moneda.** La moneda principal de inversión es el **USD**. Todo valor en ARS debe indicar tipo de cambio utilizado (oficial / MEP / otro), fecha y fuente.
3. **No inventar datos.** Si un dato no está disponible, se declara como faltante y se registra en `00_gestion_proyecto/datos_por_validar.md`.
4. **Clasificación obligatoria de cada dato.** Toda cifra se etiqueta como:
   - `[VERIFICADO]` — proviene de fuente identificable y confiable (ver regla 6).
   - `[ESTIMACIÓN]` — cálculo o inferencia propia a partir de datos; se documenta el método.
   - `[SUPUESTO]` — hipótesis de trabajo adoptada; se registra en `00_gestion_proyecto/supuestos.md`.
   - `[COTIZACIÓN]` — precio ofrecido por un proveedor; se indica proveedor, fecha, validez, moneda y condiciones (IVA, flete, instalación).
5. **Trazabilidad.** Toda cifra relevante indica su fuente (ID de `25_fuentes/registro_fuentes.csv`) o queda marcada `[PENDIENTE DE VALIDACIÓN]`.
6. **Jerarquía de fuentes.** Priorizar: SENASA, Secretaría de Agricultura, Ganadería y Pesca, INTA, INTI, INDEC, organismos provinciales, FAO, USDA y documentación técnica (manuales de líneas genéticas, fabricantes, normas). Cámaras sectoriales, prensa y fuentes comerciales se usan como complemento y se identifican como tales.
7. **Capital.** No asumir que USD 2 millones alcanza ni que es el tope. Es un escenario de referencia. El estudio debe determinar la inversión mínima viable, la recomendable, las escalas, las fases, el capital de trabajo y las necesidades adicionales. No diseñar el proyecto artificialmente para que entre en USD 2 millones.
8. **Demanda.** No asumir que los 90 supermercados son clientes confirmados. Se tratan como canal potencial hasta contar con evidencia (volúmenes, precios, condiciones de pago, cartas de intención). Pueden funcionar como cliente ancla, canal para ciertos cortes, fuente de volumen o reductor de riesgo comercial, pero **no definen ni limitan la escala final** de la empresa.
9. **Capacidad.** No asumir una capacidad de faena (aves/hora o aves/día) antes de realizar el estudio de demanda, balance de masa y escenarios.
10. **Objetividad.** Analizar la factibilidad de forma crítica. Señalar explícitamente cuando una hipótesis sea poco realista, riesgosa o no esté sustentada. La integración vertical total no se presume conveniente: cada eslabón se evalúa (hacer / comprar / tercerizar / postergar).
11. **Escalabilidad y exportación.** Diseñar pensando en crecimiento por etapas y en requisitos de futura exportación (habilitaciones SENASA, bienestar animal, trazabilidad, mercados destino).
12. **Registros vivos.** Mantener actualizados `supuestos.md`, `decisiones_pendientes.md` y `datos_por_validar.md` en `00_gestion_proyecto/` en cada sesión que los afecte, y actualizar `estado_proyecto.md` al cerrar hitos.
13. **Sin duplicación.** Cada información vive en un solo archivo; los demás la referencian con un enlace relativo. Antes de crear un archivo, verificar si el tema ya existe.
14. **Unidades métricas.** Sistema métrico (kg, t, m², m³, kWh, °C, km). Densidades en kg/m² o aves/m². Declarar base de cálculo (peso vivo, peso canal, por ave, por kg).
15. **Modelos documentados.** Todo modelo (Excel, CSV, Python, etc.) documenta sus fórmulas, supuestos, unidades y fuentes, ya sea en el propio archivo o en un README junto al modelo.

16. **Verificación documental.** Una cifra vista solo en un extracto de buscador o en prensa, sin lectura del documento original, no se etiqueta `[VERIFICADO]`. Se marca **PENDIENTE DE VERIFICACIÓN DOCUMENTAL PRIMARIA** (`[PVDP]`). Si el documento original contradice al extracto, prevalece el original y la contradicción se registra.
17. **Mercados de exportación.** Distinguir siempre cuatro categorías: (A) país habilitado sanitariamente; (B) país al que efectivamente se exporta; (C) país potencial; (D) país cerrado o suspendido. No afirmar acceso vigente sin evidencia posterior al último evento sanitario.
18. **Universos estadísticos.** No restar ni comparar cifras de distinto universo (faena SENASA vs faena total, pollitos nacidos vs aves faenadas, producción vs faena, definiciones de exportación) sin verificar período, categoría de aves, variable medida y metodología. Si no se puede verificar, se registra como inconsistencia pendiente.

## Principios estratégicos (vigentes desde 2026-09-29)

- **Visión:** estudiar la construcción progresiva de una **empresa avícola argentina integrada, escalable y con vocación exportadora**, capaz de competir en mercado interno, supermercados, mayoristas, industria, gastronomía, elaborados y exportación. La red de ~90 supermercados es una posible ventaja inicial, no el objetivo final.
- **Ingreso total por ave:** el objetivo económico es maximizar el ingreso total por ave, asignando cada parte del pollo (pechuga, pata-muslo, alas, garras, menudencias, recortes, subproductos) al mercado que mejor la paga. No se busca simplemente vender la mayor cantidad posible de pollo entero.
- **Localización:** no hay ubicación seleccionada. Se evalúan objetivamente Buenos Aires, Entre Ríos, Santa Fe, Córdoba, Chaco y cualquier otra región competitiva. Los contactos personales (ej.: un contacto en Chaco) son solo una ventaja cualitativa y nunca un criterio suficiente.
- **Eventos de mercado (ej.: crisis de Granja Tres Arroyos):** separar hechos verificados de posibles oportunidades. No asumir disponibilidad de activos, productores, capacidad a façon ni clientes sin investigación específica.

## Convenciones de trabajo

- Idioma de trabajo: español (Argentina). Términos técnicos en inglés se definen en `00_gestion_proyecto/glosario.md`.
- Nombres de archivo: minúsculas, sin acentos ni espacios, con guion bajo (`ejemplo_archivo.md`).
- Fechas: formato ISO `AAAA-MM-DD`.
- Separador decimal en documentos: coma; en CSV y modelos: punto. Declarar cualquier excepción.
- IDs de registros: supuestos `SUP-###`, decisiones `DEC-###`, datos por validar `DPV-###`, fuentes `FTE-###`.
- Cada carpeta temática tiene un `README.md` con su alcance; agregar contenido dentro de la carpeta correspondiente.
- No realizar recomendaciones de inversión ni selección de maquinaria o proveedores hasta que la fase del proyecto lo habilite (ver `estado_proyecto.md`).
