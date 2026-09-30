# Gates de expansión — puertas medibles entre etapas

**Fecha:** 2026-09-30 · **Versión:** 1.0 (estructura; **sin umbrales definitivos**) · Fase 0

> **Alcance:** define las **variables medibles** que deberían cumplirse antes de pasar de una etapa (o escala) a la siguiente, cómo medirlas y qué evidencia las respalda. **No se fijan umbrales numéricos definitivos**: no existen datos para calibrarlos (DEC-034). Donde se muestra un valor, es la **forma** del criterio o una referencia física del modelo, no una meta.
> Relacionado: [`arquitectura_escalable.md`](arquitectura_escalable.md) (secuencias), [`escenarios_escala.md`](escenarios_escala.md) (cifras), [`../02_clientes_demanda/modelo_demanda.md`](../02_clientes_demanda/modelo_demanda.md) §7 (regla de dimensionamiento D_A + α·D_B, DEC-014).

**Principio:** **no ampliar únicamente porque "hay interés"**. Cada ampliación se vincula a métricas **verificables y documentadas** (registro en `25_fuentes/registro_fuentes.csv` como `entrevista`, `cotizacion` o documento), sostenidas en el tiempo, y a un plazo de ejecución conocido.

---

## 1. Puertas

| Gate | Paso | Pregunta que responde |
|---|---|---|
| **G0** | Etapa 0 (validación comercial, sin planta) → primera planta | ¿Existe demanda A/B suficiente, abastecimiento y receptores para que una planta propia tenga sentido frente a seguir con façon/compraventa? |
| **G1** | Primera escala → siguiente (p. ej. 2.500 → 5.000) | ¿La planta actual está llena **con clientes reales** y la demanda firme ya cubre buena parte de la siguiente? |
| **G2** | Escala intermedia → 10.000 (o 1 → 2 turnos) | ¿Hay una red de productores, pollitos, frío y salida de subproductos para duplicar? |
| **G3** | 10.000 → 20.000 (o 2.ª línea) | ¿La diversificación comercial (canales, exportación negociada) justifica otra línea sin concentrar el riesgo? |

## 2. Variables medibles

Cada variable tiene fórmula, fuente de evidencia y **umbral a definir** (UAD). Las variables se evalúan **sostenidas** (p. ej., promedio de varios meses consecutivos: el período también es UAD) y **antes** de que la capacidad se agote, descontando el plazo de ampliación (§3).

| # | Variable | Fórmula / medición | Evidencia aceptada | Umbral | Gates |
|---|---|---|---|---|---|
| V1 | **Demanda asegurada** (A) | kg de producto/día calendario con contrato, orden de compra, carta de intención con volumen y precio, o historial propio; **por producto** | Documentos firmados; registro de ventas | UAD: A ≥ x % de la capacidad de la **etapa siguiente** | G0–G3 |
| V2 | **Demanda en negociación** (B) | kg/día con negociación activa (especificación, precio, prueba piloto) × factor de conversión α | Minutas con el decisor de compras; cotizaciones pedidas | UAD: A + α·B ≥ y % de la capacidad siguiente; α calibrado con la tasa real de conversión | G0–G3 |
| V3 | **Utilización de planta** | Aves faenadas / capacidad operativa, promedio del período | Registro de producción | UAD: u ≥ z % sostenido (el modelo muestra que 70–85 % es el rango donde la planta está "cerca de llena"; no es meta) | G1–G3 |
| V4 | **Balance de partes** | Excedente de partes sin comprador (kg/día) / producción comestible; cada parte con **≥ 2 salidas** identificadas | Pedidos por parte; compradores de pata-muslo, alas, carcasa, garras, menudencias | UAD; regla cualitativa: ninguna parte relevante sin comprador | G0–G3 |
| V5 | **Concentración** | Participación del mayor cliente; top 5; partes vinculadas; HHI | Ventas por cliente | UAD (DEC-017); prueba de estrés: la etapa siguiente debe resistir la pérdida del mayor cliente | G1–G3 |
| V6 | **Contratos comerciales** | Cantidad, plazo y volumen de contratos vigentes; condiciones de pago | Contratos | UAD | G0–G3 |
| V7 | **Disponibilidad de pollitos BB** | Pollitos/semana contratados para la etapa siguiente vs necesarios (13.200 / 26.400 / 52.800 / 105.600 por semana plena, medio) | Contratos con incubadoras; dos proveedores | UAD: cobertura ≥ 100 % de la semana plena siguiente + margen | G0–G3 |
| V8 | **Productores integrados disponibles** | m² de galpón comprometidos vs necesarios (9.500 / 19.000 / 37.900 / 75.900 m², medio) | Relevamiento y contratos de integración (DPV-048) | UAD | G0–G3 |
| V9 | **Alimento** | t/semana plena comprometidas (62 / 124 / 247 / 494 t, medio) y capacidad de entrega | Acuerdos con fábricas o plan propio (DEC-024) | UAD | G1–G3 |
| V10 | **Desempeño productivo real** | Mortalidad, FCR, peso y decomisos medidos vs supuestos del modelo | Registros de lotes y de faena | UAD: los supuestos del modelo se reemplazan por los medidos antes de dimensionar la etapa siguiente | G1–G3 |
| V11 | **Capacidad de frío** | Inventario proyectado (t) vs capacidad de cámaras y túneles para el perfil refrigerado/congelado real | Registro de stocks | UAD | G1–G3 |
| V12 | **Salida de subproductos** | t/día de clase C retiradas vs generadas; contrato con receptor; distancia | Contrato de retiro; remitos | UAD: 100 % retirado a diario con contrato vigente para el volumen siguiente | G0–G3 |
| V13 | **Efluentes** | Caudal y carga tratables vs proyectados; cumplimiento de límites de vuelco | Análisis de laboratorio; permiso | UAD (`11_agua_efluentes`) | G1–G3 |
| V14 | **Capital disponible** | Capital comprometido (no declarado) para CAPEX + capital de trabajo de la etapa siguiente | Compromiso documentado del inversor (DPV-001) | UAD (DEC-010) | G0–G3 |
| V15 | **Habilitación sanitaria** | Habilitación vigente para el nivel requerido por los clientes de la etapa siguiente (provincial / SENASA tránsito federal / listado de exportación) | Resoluciones SENASA | Sí / no (DEC-009) | G0–G3 |
| V16 | **Compradores de exportación** | Importadores o traders en nivel ≥ 5 (negociación) por producto y destino | Minutas, ofertas firmes; nivel 6 = contrato | UAD; la exportación entra en la capacidad solo en nivel ≥ 5 (SUP-022) | G2–G3 |
| V17 | **Servicios y terreno** | Potencia, agua, permiso de vuelco y superficie disponibles vs necesarios para la etapa siguiente | Factibilidades de las prestadoras; plano | Sí / no | G1–G3 |
| V18 | **Plazo de ampliación** | Meses desde la decisión hasta operar la etapa siguiente (obra, equipos, habilitación, pollitos) | Cronograma con proveedores (DPV-086) | Se usa para anticipar el disparo (§3) | G1–G3 |

## 3. Cuándo disparar una ampliación

La capacidad debe estar disponible **cuando** llega la demanda, no después. Forma del criterio (sin valores):

```
Disparar la ampliación en el mes t si:
    (A + α·B) proyectada al mes t + plazo_de_ampliación  ≥  u_umbral × capacidad_actual
    y se cumplen V7, V8, V12, V14, V15 y V17 para la escala siguiente
```

- La **proyección** se basa en el pipeline documentado, nunca en el mercado total (categoría D).
- Si la demanda aparece antes de que la ampliación esté lista, los **amortiguadores** son: sexto día de faena (+20 %), segundo turno (×2 sobre la misma línea), faena a façon o compra de producto de terceros (DEC-018).

## 4. Señales que **no** habilitan una ampliación

| Señal | Por qué no alcanza |
|---|---|
| "Hay interés" de un cliente o del inversor | Es demanda C; no tiene volumen, precio ni plazo |
| El mercado es grande | Es demanda D (regla 8; el mercado nunca fue el límite) |
| Un país abrió su mercado | País abierto ≠ planta habilitada ≠ producto autorizado ≠ comprador (regla 17) |
| Hay capital disponible | El capital no es demanda (regla 7) |
| Un competidor tiene problemas (p. ej. concurso de GTA) | Oportunidad a investigar, no hecho (principios estratégicos de `CLAUDE.md`) |
| La planta está llena **con un solo cliente** o con partes vendidas bajo costo | Llenar no es lo mismo que valorizar el ave (V4, V5) |
| Utilización alta durante pocas semanas | Puede ser estacional o una promoción; el período de medición es parte del gate |

## 5. Pendiente

- Calibrar umbrales x, y, z, α, período de medición y márgenes (DEC-034) cuando haya: datos de la red (DPV-003, DPV-037), escala mínima eficiente (DPV-083), plazos de ampliación (DPV-086) y modelo financiero.
- Integrar los gates al futuro simulador como **alertas**, no como decisiones automáticas ([`especificacion_simulador_html.md`](especificacion_simulador_html.md) §4).
