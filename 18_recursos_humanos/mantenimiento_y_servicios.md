# Mantenimiento, limpieza y servicios de soporte

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 14A) · Fase 0

> **Alcance:** estructura conceptual de mantenimiento (preventivo, correctivo, eléctrico, mecánico, frío, automatización), comparación propio / tercerizado / mixto; limpieza y sanitización como **función crítica** con dotación propia / tercerizada / híbrida; utilities, higiene y seguridad, lavandería.
> **No** se elige modalidad (DEC-14A-01, DEC-14A-02, DEC-040), proveedor ni contratista; **no** se calculan costos.
> **Clasificación:** cantidades `[ESTIMACIÓN]` de [`modelo_rrhh.py`](modelo_rrhh.py) con coeficientes `[SUPUESTO]` (SUP-14A-06, SUP-14A-09); activos tomados de [`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv) (sin modificarla).

---

## 1. Mantenimiento

### 1.1 Estructura conceptual

| Tipo | Contenido | Quién lo hace típicamente | Cuándo |
|---|---|---|---|
| **Preventivo** | Lubricación, cambio de dedos de desplumadora, cuchillas, rodamientos, calibraciones, inspecciones | Técnicos propios o del contratista; especialistas para equipos automáticos | Ventana de mantenimiento de la ecuación de 24 h (0,5 / 1,0 / 2,0 h/día, SUP-062) y fines de semana |
| **Correctivo** | Reparar lo que se rompió durante la faena | **Técnico presente en planta** (minutos cuentan: la línea se detiene) | En producción |
| **Eléctrico** | Tableros, motores, variadores, iluminación; media tensión | Propio (baja tensión); externo matriculado (media tensión) | Ambos |
| **Mecánico** | Transportadores, grilletes, desplumadoras, evisceradoras, bombas | Propio | Ambos |
| **Frío** | Sala de máquinas, evaporadores, túneles, cámaras (24 h/365 d) | Propio con formación específica o contratista; refrigerante sin decidir (DEC-046) | Guardia fuera de turno |
| **Automatización** | PLC, sensores, balanzas de línea, visión, software de clasificación | Proveedor del equipo en escalas chicas; especialista interno en automático ≥ 10.000 | Ambos |
| **Utilities** | Caldera/agua caliente, aire comprimido, agua, tratamiento de efluentes, grupo electrógeno | Técnicos de planta; operador de PTE en escalas grandes | Más horas que la línea |

### 1.2 Cómo se dimensiona en el modelo

```
técnicos = max( cobertura presencial , carga por activos )
cobertura = días × (horas de producción × técnicos simultáneos + horas fuera de producción × 1) / horas normales × cobertura
carga     = Σ equipos presentes × horas/semana según nivel (Mc 0,75 · S 1,5 · A 3 h, media) × peso de criticidad (1,5 / 1 / 0,5)
            × unidades (equipos "duplicables": 1 cada 1.250 aves/h) / 32 h productivas por técnico
```

- **Técnicos simultáneos en producción** (SUP-14A-09): 1 (< 5.000), 2 (mecánico + electricista, ≥ 5.000), 3 (+ frío/utilities, ≥ 10.000), 4 (+ automatización, automático ≥ 10.000). Fuera de producción, 1 de guardia.
- **Nivel efectivo de cada equipo:** la opción técnica de la matriz más cercana por debajo del nivel de automatización del escenario; un equipo que no admite operación manual conserva su nivel mínimo. Así **más automatización nunca reduce técnicos** (test R03).

### 1.3 Resultados (escenario de referencia, productividad media)

| Escala | Equipos (unidades) y niveles | Carga por activos, técnicos eq. (alta–media–baja) | Cobertura presencial eq. | Propio: interno / externo | Tercerizado: interno / externo | Mixto: interno / externo |
|---|---|---|---|---|---|---|
| 2.500 (manual) | 61 (3 Mc, 15 S, 12 A) | 1,1–2,3–5,3 | 2,0 | 2,3 / 0 | 0 + 0,5 coordinación / 2,3 | 2,0 / 0,3 |
| 5.000 (mecanizado) | 63 (3 Mc, 17 S, 12 A) | 1,1–2,4–5,5 | 3,3 | 3,3 + 1 jefe / 0 | 0 + 1 coordinación / 3,3 | 3,3 + 1 jefe / 0 |
| 10.000 (semiautomático) | 65 (3 Mc, 46 S, 12 A) | 1,6–3,6–8,1 | 4,5 | 4,5 + 1 jefe / 0 | 0 + 1 coordinación / 4,5 | 4,5 + 1 jefe / 0 |
| 20.000 (automático) | 85 (7 S, 75 A) | 3,3–7,5–17,1 | 5,8 | 7,5 + 1 jefe / 0 | 0 + 1 coordinación / 7,5 | 5,8 + 1 jefe / 1,7 |

Se suma un pañolero desde 10.000 aves/día (sólo con mantenimiento propio o mixto). **Lecturas:**

1. **Hasta 10.000 aves/día manda la cobertura presencial** (tener alguien en planta cuando la línea corre), no la carga de los activos: el mantenimiento es un costo casi fijo por turno.
2. **A 20.000 automático manda la carga de activos** (7,5 vs 5,8): ahí el mixto deja afuera la parte especializada (1,7 eq.).
3. **El rango es amplio** (3,3–17,1 técnicos eq. a 20.000): las horas de mantenimiento por equipo son el supuesto menos respaldado del bloque (DPV-14A-10).
4. **Dos cuadrillas duplican la cobertura presencial** casi completa: un segundo turno sin técnico en planta no es una opción realista para una línea continua.

### 1.4 Propio vs tercerizado vs mixto (sin elección)

| Criterio | Propio | Tercerizado | Mixto (cobertura propia + especialistas externos) |
|---|---|---|---|
| Tiempo de respuesta a una falla en producción | ▲ inmediato | ▼ depende del contrato y la distancia; requiere residentes del contratista | ▲ para lo cotidiano; ● para lo especializado |
| Conocimiento de la planta | ▲ se acumula | ▼ rota con el contratista | ▲ |
| Especialidades (frío con amoníaco, PLC, media tensión) | ▼ difícil de tener todas en escalas chicas | ▲ | ▲ |
| Dependencia | De la retención de técnicos | Del contratista y del proveedor de equipos | Repartida |
| Escala chica (2.500–5.000) | ● 2–4 técnicos subutilizados en parte | ● casi siempre hace falta un residente igual | ▲ habitual |
| Escala grande / automática | ▲ con especialistas | ▼ riesgo de parada | ▲ |
| Función interna mínima que **no** se terceriza | — | Coordinador de mantenimiento y contratos; planificación del preventivo; repuestos críticos (DEC-040) | Jefe de mantenimiento |
| Datos que faltan | Disponibilidad de técnicos por corredor (DPV-14A-08) | Oferta de contratistas y servicio técnico local (DPV-089) | Ambos |

## 2. Limpieza y sanitización — función crítica

### 2.1 Por qué es crítica

- Es **condición de habilitación y de inocuidad**: POES escritos con limpieza preoperativa y operativa, responsables, frecuencias, verificación y acciones correctivas (Res. SENASA 233/1998, `[PVDP]`); su verificación es parte del APPCC obligatorio (Res. 205/2014, `[PVDP]`).
- **Ocupa la ventana de 24 h:** limpieza + sanitización = 3,0 / 4,0 / 6,0 h/día (optimista / media / conservadora, SUP-062). Si la limpieza no entra, no hay segundo turno.
- **Es el bloque de personal más incierto:** su dotación depende de m² de salas (12C, proxy), cantidad y complejidad de equipos (más automatización = más desarme) y de cómo se organiza la ventana.

### 2.2 Dos componentes

| Componente | Quién | Cuándo | Modelo |
|---|---|---|---|
| **Limpieza operativa** (pisos, derrames, recipientes, limpieza intermedia) | Siempre interna | Durante producción | 1 + 0,3 / 0,5 / 0,8 puestos por 1.000 aves/h, por cuadrilla |
| **Limpieza y sanitización post-producción** (desarme, prelavado, espuma, enjuague, desinfección, preoperacional) | Propia, tercerizada o híbrida | Ventana de limpieza + sanitización | ⌈m² de proceso × factor de automatización (1,0 / 1,0 / 1,1 / 1,25) ÷ (60 / 40 / 25 m²/persona-h) ÷ ventana⌉ |

### 2.3 Resultados (escenario de referencia, productividad media)

| Escala | m² de proceso (12C, medio) | Cuadrilla simultánea (alta–media–baja) | Propia: personas · eq. | Tercerizada: interno · eq. externos | Híbrida (30 % interna): personas · eq. int. · eq. ext. | Total empresa: propia / tercerizada / híbrida |
|---|---|---|---|---|---|---|
| 2.500 | 1.079 | 5–7–11 | 8 · 3,5 | 0 · 3,5 | 4 · 1,5 · 2,0 | 64 / 56 / 60 |
| 5.000 | 1.741 | 7–11–18 | 13 · 5,5 | 0 · 5,5 | 5 · 2,0 · 3,5 | 91 / 78 / 83 |
| 10.000 | 2.697 | 12–19–30 | 22 · 9,5 | 0 · 9,5 | 7 · 3,0 · 6,5 | 115 / 93 / 100 |
| 20.000 | 4.447 | 21–35–59 | 40 · 17,4 | 0 · 17,4 | 13 · 5,5 · 11,9 | 151 / 110 / 123 |

En las tres modalidades se mantiene **interno** el supervisor de saneamiento / verificación POES y la limpieza operativa en turno (test R04). **Lecturas:**

1. **Personas ≫ equivalentes:** una ventana de ~4 h obliga a cuadrillas grandes con pocas horas (40 personas para 17 equivalentes a 20.000). Organizar la limpieza **por sectores** a medida que cada sala termina (evisceración antes que empaque) alarga la ventana efectiva y reduce la cuadrilla; es una pregunta prioritaria de campo (DPV-091, DPV-14A-06).
2. **Tercerizar cambia el perfil de la nómina, no la cantidad de trabajo:** la función mide igual (equivalentes idénticos); lo que cambia es quién emplea, quién capacita y quién responde ante SENASA y el cliente (siempre la empresa).
3. **Jornada parcial o nocturna:** una cuadrilla post-producción que trabaja de noche cae en jornada nocturna (`[PVDP]`); el convenio puede fijar condiciones (DPV-14A-01).

### 2.4 Propia vs tercerizada vs híbrida (sin elección)

| Criterio | Propia | Tercerizada | Híbrida |
|---|---|---|---|
| Control del resultado (verificación preoperacional, hisopados) | ▲ directo | ● por contrato; la responsabilidad sigue siendo de la empresa | ▲ en equipos críticos |
| Conocimiento de equipos (desarme de evisceradoras, trozadoras) | ▲ | ▼ salvo personal estable del contratista | ▲ (la parte interna desarma) |
| Rotación y capacitación | ● la empresa la absorbe | ● la absorbe el contratista; riesgo de rotación alta | ● |
| Flexibilidad ante cambios de turno o escala | ● | ▲ | ▲ |
| Químicos y efluentes | Propios | Del contratista (compatibilidad con el tratamiento de efluentes, DPV-112) | Mixto |
| Oferta en el corredor | Mano de obra local (DPV-121) | Empresas especializadas (no relevadas) | Ambas |
| Riesgo de inocuidad | ● | ▼ si el contrato premia rapidez | ● |

## 3. Otros servicios de soporte

| Servicio | Tratamiento en el modelo | Pendiente |
|---|---|---|
| **Higiene y seguridad laboral y medicina del trabajo** | Servicio externo en todas las escalas (equivalentes **PENDIENTES**); técnico interno desde 10.000 | Horas-profesional mínimas por cantidad de trabajadores y riesgo (Ley 19.587, Decreto 1338/96, `[PVDP]`, FTE-14A-004; DPV-14A-07) |
| **Lavandería y ropería por zona** | 0,5 (2.500) → 2 (20.000) internos | Propio vs tercerizado (DEC-14A-07); 12C reservó superficie |
| **Seguridad patrimonial y portería** | No modelada (habitualmente tercerizada) | Puestos 24 h según sitio |
| **Utilities y PTE** | Incluidos en la cobertura técnica (3.er técnico simultáneo desde 10.000) | Operador de PTE según tecnología (DEC-043) |
| **Transporte del personal** | No modelado | DPV-139 |
