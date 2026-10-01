# Programa de áreas conceptual

**Fecha:** 2026-10-01 · **Versión:** 1.0 (sesión 12C) · Fase 0

> **Pregunta:** ¿qué áreas necesita la planta, con qué lógica se dimensiona cada una y qué dato falta para hacerlo bien?
> **Alcance:** lista completa de áreas funcionales (54 en el modelo + la reserva de expansión), su zona ([`zonificacion_layout.md`](zonificacion_layout.md)), su categoría de superficie, el **método** de dimensionamiento y el **dato faltante**. Las superficies por escala están en [`layouts_por_escala.md`](layouts_por_escala.md) y, completas, en [`escenarios_superficies.csv`](escenarios_superficies.csv) (bloque `detalle`). **No** es un programa arquitectónico ejecutivo: no hay alturas, terminaciones, vanos ni posiciones.
> **Clasificación:** todas las superficies son `[ESTIMACIÓN]` construidas con factores `[SUPUESTO]` (SUP-12C-01 a SUP-12C-15), algunos `[PVDP]` (densidades de cámara, cargas de tratamiento) y algunos **PROXY** (sustitutos de datos faltantes que generan alerta). **Ningún** factor está validado en planta argentina.

---

## 1. Categorías de superficie y totales

| Categoría | Qué incluye | ¿Construido (cubierto)? |
|---|---|---|
| **m² de proceso** | Salas desde la recepción de aves hasta el empaque, más su circulación interna, esclusas y barreras sanitarias | Sí |
| **m² de frío** | Túneles de congelado, cámaras refrigeradas y congeladas, antecámaras, docks de expedición, cámara de subproductos, sala de decomisos | Sí |
| **m² de servicios** | Subproductos, residuos, envases, salas técnicas (frío, caldera, aire, electricidad, generador, agua), mantenimiento, repuestos, químicos, laboratorio, lavandería | Sí |
| **m² de personal/admin** | Vestuarios, comedor, oficinas, oficina SENASA, enfermería/capacitación, porterías, circulación de personal | Sí |
| **m² exteriores** | Playas de vivo, despacho y subproductos, lavado de camiones, estacionamiento, tanques, circulación pesada | No |
| **m² de efluentes** | Pretratamiento, ecualización, DAF, biológico, lodos, circulación | No (mayormente a cielo abierto o en tinglado) |
| **m² de reserva para expansión** | Diferencia entre la escala objetivo y la actual por categoría + reserva de rendering futuro | No (es terreno libre) |

```
m² CONSTRUIDOS  = proceso + frío + servicios + personal/admin
m² OPERATIVOS   = construidos + exteriores + efluentes
TERRENO         = (huella de edificios + exteriores + efluentes + reserva) ampliado por retiros y buffers
```

Por qué tres totales distintos: [`guia_ramiro.md` §6](guia_ramiro.md).

## 2. Método de dimensionamiento (resumen; código en [`modelo_superficies.py`](modelo_superficies.py))

| Método | Cuándo se usa | Fórmula | Estado que muestra |
|---|---|---|---|
| **F — Footprint** | Cuando el proveedor entregue la huella de equipos del área (layout de RFQ) | m² = huella de equipos × **factor de envolvente** 2,2 / 2,8 / 3,5 (pasillos, acceso de mantenimiento, buffers, higiene; SUP-12C-14) | `FOOTPRINT` |
| **D — Driver físico + densidad** | Cuando la superficie depende de un stock o de un conteo que sí existe | cámaras = t (09C) × pico ÷ t/m²; andenes = posiciones × m²; vestuarios = personas × m²/persona; tratamiento = volumen ÷ profundidad | `ESTIMACION` |
| **P — Proxy de intensidad** | Cuando falta la huella de equipos (hoy: todas) | m² = k × (driver/1.000)^0,8, con mínimo funcional; k y mínimos **sin fuente** (SUP-12C-01) | `PROXY` + alerta `FOOTPRINT_DESCONOCIDO` |
| **N — No aplica** | El área no existe en la configuración | 0 declarado explícitamente | `NO_APLICA` |
| **Estricto** | `estricto=True`: no se aceptan proxies de huella ni de dotación | El área queda `None` y todo total que la contiene también | `PENDIENTE` (estado global `INCOMPLETO`) |

**Regla clave:** una huella desconocida **nunca** se convierte en cero. O se usa un proxy visible (con alerta) o el resultado queda incompleto. Una huella informada igual a 0 se rechaza como error (test T07).

**Exponente 0,8 (SUP-12C-01):** expresa que al duplicar el ritmo una sala crece menos del doble (pasillos, puestos fijos y mínimos se comparten). Es un supuesto de orden de magnitud; la curva real sale de layouts de proveedores (DPV-12C-01) y de plantas existentes (DPV-12C-07).

## 2 bis. Calidad de las superficies: tipo de origen (A–E)

**Por qué importa:** en el escenario de referencia **23 de 54 áreas están en estado PROXY**. Para no leer todas las cifras con la misma confianza, cada área lleva un **tipo de origen** (columna `origen_superficie` del CSV y campo `origen` en `salida_interfaz()`; metadato agregado en v1.0.1 sin cambiar ningún cálculo):

| Código | Tipo de origen | Qué significa | Áreas que lo incluyen |
|---|---|---|---|
| **A** | DERIVADA DE MODELO EXISTENTE | El driver sale de 09A/09C (t de stock, t/día, kg/h, caudales, residencias); la conversión a m² igual usa factores | 14 |
| **B** | CALCULADA CON FACTOR DE DISEÑO | Densidad, m²/persona, m²/bahía, fracción de circulación: `[SUPUESTO]` explícito | 37 |
| **C** | PROXY PRELIMINAR | Sustituto de un dato faltante (huella, dotación, camión, lodos, potencia); genera alerta | 25 |
| **D** | FOOTPRINT PENDIENTE DE PROVEEDOR | La sala depende de la huella de equipos aún no recibida (RFQ, §4) | 16 |
| **E** | REQUISITO REGULATORIO PENDIENTE | Hay una exigencia normativa no leída en original o dependiente de la jurisdicción | 11 |

El **primer código** es el que domina la calidad del resultado: por código principal, **14 áreas A, 16 B y 24 C** (las 23 en estado PROXY + deshuese y CMS, que no aplican en config. B pero son proxy en C). **Ninguna superficie es `[VERIFICADO]`** (test T19).

| Grupo | Área | Origen | Estado (referencia 10.000) |
|---|---|---|---|
| Proceso | Recepción, andén de espera ventilado y descarga | **C·B·E** | PROXY |
| Proceso | Colgado y aturdido | **C·D** | PROXY |
| Proceso | Sangrado, escaldado, desplumado, patas y cabeza | **C·D·E** | PROXY |
| Proceso | Evisceración, inspección oficial post mortem, menudencias en línea | **C·D·E** | PROXY |
| Proceso | Enfriamiento (inmersión, aire o mixto) y escurrido | **A·B·D** | ESTIMACION |
| Proceso | Clasificación por peso y calidad | **C·D** | PROXY |
| Proceso | Trozado (incluye sala mínima en config. A) | **C·D** | PROXY |
| Proceso | Deshuese, fileteado y trimming | **C·D** | NO_APLICA en A/B; PROXY en C |
| Proceso | Sala de CMS (carne separada mecánicamente) | **C·D·E** | NO_APLICA en A/B; PROXY en C |
| Proceso | Coproductos comestibles: garras y menudencias | **C·D** | PROXY |
| Proceso | Envasado primario, control, encajonado y paletizado | **C·D** | PROXY |
| Proceso | Lavado de cajones/módulos de aves vivas | **C·D** | PROXY |
| Proceso | Circulación interna de proceso, esclusas y barreras sanitarias | **B·E** | ESTIMACION |
| Frío | Cámaras de producto refrigerado | **A·B** | ESTIMACION |
| Frío | Cámaras de producto congelado (incluye lotes de exportación) | **A·B** | ESTIMACION |
| Frío | Congelado (túnel/espiral/placas) | **A·C·D** | PROXY |
| Frío | Antecámaras, pasillo frío y preparación de pedidos | **B** | ESTIMACION |
| Frío | Expedición: andenes refrigerados con sello | **C·B** | PROXY |
| Frío | Cámara de subproductos perecederos (separada del producto) | **A·B** | ESTIMACION |
| Frío | Sala/cámara de decomisos bajo control oficial | **B·E** | ESTIMACION |
| Servicios | Subproductos no comestibles: sangre, plumas, vísceras, cabezas (tanques, tolvas, contenedores, báscula) | **A·B** | ESTIMACION |
| Servicios | Residuos, cartón y compactación | **B** | ESTIMACION |
| Servicios | Depósito de envases, cartón e insumos secos (fuera de salas de proceso) | **A·B** | ESTIMACION |
| Servicios | Sala de máquinas de frío (compresores, condensadores) | **C·D** | PROXY |
| Servicios | Caldera / agua caliente / vapor | **C·D** | PROXY |
| Servicios | Compresores de aire comprimido | **C·D** | PROXY |
| Servicios | Grupo electrógeno de respaldo | **C·D** | PROXY |
| Servicios | Sala eléctrica, tableros y transformador | **C** | PROXY |
| Servicios | Tratamiento de agua potable (cloración, filtros, bombeo) | **A·B** | ESTIMACION |
| Servicios | Mantenimiento y taller | **B** | ESTIMACION |
| Servicios | Pañol de repuestos | **B** | ESTIMACION |
| Servicios | Depósito de químicos (bajo llave) | **B** | ESTIMACION |
| Servicios | Laboratorio de autocontrol / calidad | **B** | ESTIMACION |
| Servicios | Lavandería / ropería de indumentaria por color de zona | **C·B** | PROXY |
| Personal / admin | Vestuarios y sanitarios separados por zona (sucia / limpia) y por sexo | **C·B·E** | PROXY |
| Personal / admin | Comedor y office | **C·B** | PROXY |
| Personal / admin | Oficinas de administración | **B** | ESTIMACION |
| Personal / admin | Oficina del servicio de inspección oficial (SENASA) con sanitario propio | **B·E** | ESTIMACION |
| Personal / admin | Enfermería, sala de capacitación | **B** | ESTIMACION |
| Personal / admin | Porterías y seguridad (accesos separados) | **B** | ESTIMACION |
| Personal / admin | Circulación de personal y filtros sanitarios | **B** | ESTIMACION |
| Exteriores | Playa de camiones de aves vivas (espera exterior y maniobra) | **C·B** | PROXY |
| Exteriores | Lavado y desinfección de camiones de vivo | **B·E** | ESTIMACION |
| Exteriores | Playa de maniobra de despacho (frente a docks) | **C·B** | PROXY |
| Exteriores | Playa de contenedores y retiro de subproductos | **A·B** | ESTIMACION |
| Exteriores | Estacionamiento de personal y visitas | **C·B** | PROXY |
| Exteriores | Tanques de reserva de agua (incluye incendio a definir) | **A·B·E** | ESTIMACION |
| Exteriores | Circulación pesada interna (vivo / producto / subproductos separados) | **B** | ESTIMACION |
| Efluentes | Pretratamiento: rejas, tamiz, desengrasador, bombeo | **A·B** | ESTIMACION |
| Efluentes | Ecualización | **A·B** | ESTIMACION |
| Efluentes | DAF (flotación por aire disuelto) y química | **A·B** | ESTIMACION |
| Efluentes | Tratamiento biológico (anaerobio_aerobio) | **A·B·E** | ESTIMACION |
| Efluentes | Manejo de lodos y flotados (espesado, deshidratación, acopio) | **C** | PROXY |
| Efluentes | Circulación, laboratorio y operación de efluentes | **B** | ESTIMACION |
| Reserva | Reserva de terreno para expansión (incluye rendering futuro si se pide) | **B·C** | PROXY |


## 3. Programa de áreas

Columnas: **Zona** (1 sucia · 2 transición · 3 limpia · 3b apoyo seco · 4 fría · 5 despacho · 6 subproductos · 7 utilities · 8 personal · 9 administrativa · EXT) · **Cat.** (P proceso · F frío · S servicios · PA personal/admin · E exteriores · EF efluentes · R reserva) · **Método** (§2) · **Driver** (variable que la hace crecer) · **Dato faltante**.

### 3.1 Acceso, seguridad, estacionamiento y circulación

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Porterías y seguridad (≥ 2 accesos separados) | 9 | PA | D | Número de porterías × m² | Política de seguridad; accesos reales del terreno (12A) |
| Estacionamiento de personal y visitas | 8/EXT | E | D (PROXY de dotación) | Personas por turno × fracción motorizada | Dotación (DPV-12C-02); transporte del personal (DPV-12C-03) |
| Circulación pesada (vivo / producto / subproductos separados) | EXT | E | D | 25–50 % de los m² cubiertos | Geometría del terreno y radios de giro (12A, 12B) |

### 3.2 Recepción y faena (zona sucia)

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Recepción, andén de espera ventilado y descarga | 1 | P | D (PROXY de camión) | **Bahías** = ⌈ritmo × horas de espera ÷ aves por camión⌉ + 1 | Aves por camión (DPV-084); horas de espera admitidas (bienestar, DPV-090) |
| Colgado y aturdido (eléctrico o CAS) | 1 | P | P / F | Ritmo por línea | Huella de EQ-04, 07–10 (DPV-12C-01); método de aturdido (DEC-041: CAS ocupa más) |
| Sangrado, escaldado, desplumado, patas y cabeza | 1 | P | P / F | Ritmo por línea | Huella de EQ-11 a 18 y 20; tiempos de sangrado y escaldado (DPV-090) |
| Lavado de cajones/módulos | 1 | P | P / F | Ritmo | Huella de EQ-05; cajones vs módulos (EQ-03) |
| Playa de camiones de vivo | EXT | E | D | Bahías × m²/camión | DPV-084 |
| Lavado y desinfección de camiones de vivo | EXT | E | D | Camiones/día ÷ camiones por plataforma | Requisitos de Res. SENASA 723/2025 (`[PVDP]`, DPV-12C-11) |

### 3.3 Evisceración e inspección (transición)

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Evisceración, **inspección oficial post mortem**, separación de menudencias y vísceras, lavado de carcasas | 2 | P | P / F (× automatización: manual 1,20 · semi 1,00 · auto 0,90) | Ritmo por línea | **Puestos de inspección por velocidad de línea, iluminación y espacio** (DPV-090, DPV-12C-04); huella EQ-19, 21–33 |

### 3.4 Enfriamiento y zona limpia

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Enfriamiento y escurrido | 3 | P | D | Carcasas simultáneas = ritmo × residencia (inmersión 50 min; aire 90–150 min, 09A) × m²/carcasa | Método (DEC-026). **Sin decidir se reserva el mayor** (aire) — test T17 |
| Clasificación por peso y calidad | 3 | P | P / F | Ritmo | Huella EQ-39 |
| Trozado (sala mínima aun en config. A) | 3 | P | P / F (× automatización) | kg/h a trozado (09A) | Mix real (DEC-005); huella EQ-40/41 |
| Deshuese, fileteado y trimming | 3 | P | P / F; **NO_APLICA** en A y B | kg/h a deshuese (09A) | Compradores de suprema y destino del hueso (DEC-005, DEC-029) |
| Sala de CMS | 3 | P | P / F; **NO_APLICA** en A y B | kg/h a CMS | Norma de uso de CMS (SUP-048) y comprador (DEC-029) |
| Coproductos comestibles: garras y menudencias | 3 | P | P / F | kg/h de garras + menudencias | Estrategia de garras (DEC-031) |
| Envasado primario, control, encajonado, paletizado (sub-zona limpia seca) | 3 | P | P / F (× automatización) | kg/h comestible | Formatos (06_productos); huella EQ-49 a 56 |
| Circulación interna de proceso, esclusas y barreras sanitarias | — | P | D | 15–30 % de las salas | Normativa de pasillos y filtros (DPV-090) |
| Depósito de envases, cartón e insumos secos | 3b | S | D | t/día comestible × 5–12 m²/(t/día) | Rotación de compras de envases |

### 3.5 Frío y expedición

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Congelado (túnel estático, lineal, espiral, placas) | 4 | F | P / F | **Capacidad de congelación t/día (09C)** × 6–14 m²/(t/día); espiral ×0,35 (FTE-215 `[PVDP · débil]`) | Huella de EQ-57 a 61 y tiempo de congelado (DPV-12C-01) |
| Cámaras refrigeradas | 4 | F | D | **Stock refrigerado t (09C)** × pico 1,15–1,5 ÷ 0,5–1,0 t/m² | Densidad de estiba, racks, altura (DPV-12C-06); días de stock (DPV-078) |
| Cámaras congeladas (incluye lotes de exportación) | 4 | F | D | **Stock congelado t (09C)** × pico ÷ 0,9–1,75 t/m² | Idem; lotes de exportación (SUP-055 P3) |
| Antecámaras, pasillo frío, preparación de pedidos | 4/5 | F | D | 20–40 % de cámaras | Sistema de picking (12B) |
| Expedición: andenes refrigerados con sello | 5 | F | D (PROXY de camión) | Docks = ⌈t/día × pico ÷ (t por camión × cargas por dock)⌉ | t por camión (DPV-084), canal CD vs locales (DPV-036, 12B) |
| Playa de maniobra de despacho | EXT | E | D | Docks × 150–250 m² | Idem |

**Frío: qué se toma de 09C y qué se agrega acá.** De 09C se importan **toneladas** (stock refrigerado, stock congelado, congelación por día) con la misma base temporal y los mismos perfiles P1–P3 (test T11). Aquí solo se convierten t en m² con densidad de estiba y factor de pico. **No** se recalcula carga frigorífica, potencia ni equipos de frío (la carga frigorífica total sigue PENDIENTE en 09C, DPV-109).

### 3.6 Subproductos y residuos

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Sala de subproductos no comestibles (sangre, plumas, vísceras, cabezas; tanques, tolvas, contenedores, báscula) | 6 | S | D | t/día de sólidos a retirar (09A) × 10–22 m²/(t/día) | Frecuencia de retiro y receptor (DEC-027, DPV-065) |
| Cámara de subproductos perecederos (separada del producto) | 6 | F | D | t/día de C perecederos × 0,5–3 días ÷ densidad | Retiro diario o no (SUP-056) |
| Sala/cámara de decomisos bajo control oficial | 6 | F | D | Mínimo 6–12 m² | Requisito SENASA (DPV-090) |
| Residuos, cartón y compactación | 6 | S | D | Ritmo | — |
| Playa de contenedores y retiro de subproductos | EXT | E | D | Base + t/día | — |
| **Rendering futuro / tercerizado** | 6/R | R | PROXY | t/día de rendering potencial × 40–90 m² (mín. 300–600) | **Solo reserva de terreno**, no se construye (DEC-027, SUP-049, DEC-12C-05) |

### 3.7 Utilities

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Sala de máquinas de frío | 7 | S | PROXY | 12–25 % de los m² de frío (mín. 40–80) | Carga frigorífica total PENDIENTE (09C, DPV-109); refrigerante (DEC-046) |
| Caldera / agua caliente / vapor | 7 | S | P / F | Ritmo | Pico térmico PENDIENTE (09C, DPV-113); fuente térmica (DEC-045) |
| Compresores de aire | 7 | S | P / F | Ritmo | Consumo por equipo (DPV-095) |
| Sala eléctrica, tableros, transformador | 7 | S | PROXY | Ritmo | Potencia pico PENDIENTE (DPV-095); si el transformador va a la intemperie cambia la superficie |
| Grupo electrógeno | 7 | S | PROXY + alerta | Ritmo | Generador PENDIENTE en 09C (DEC-047) |
| Tratamiento de agua potable | 7 | S | D | m³/día (09C) | Calidad de la fuente (DPV-053) |
| Tanques de reserva (incluye incendio a definir) | EXT | E | D | m³/día × días ÷ altura | Reserva de incendio (DPV-12C-09, DPV-106) |
| Mantenimiento y taller | 7 | S | D | Ritmo | Política de mantenimiento propio vs tercerizado |
| Pañol de repuestos | 7 | S | D | Ritmo | Stock de repuestos críticos (DPV-089) |
| Depósito de químicos (bajo llave) | 7 | S | D | Ritmo | — |
| Lavandería / ropería por color de zona | 8 | S | D (PROXY de dotación) | Personas × turnos | Lavado propio vs tercerizado |

### 3.8 Efluentes (la tecnología **no** se elige)

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Pretratamiento (rejas, tamiz, desengrasador, bombeo) | 7 | EF | D | Caudal horario máximo (09C) | DPV-114 |
| Ecualización | 7 | EF | D | 30–70 % del caudal diario ÷ 3,5–4,5 m | Perfil horario de vuelco |
| DAF | 7 | EF | D | Caudal máx ÷ 4–6 m³/(m²·h) × 3–5 | Proveedor (DPV-12C-08) |
| Tratamiento biológico | 7 | EF | D según tecnología (§3.8.1) | DBO/DQO (09C, el **mayor** de los dos métodos) | Límite de vuelco del sitio (DPV-106); tecnología (DEC-043) |
| Lodos y flotados | 7 | EF | PROXY | DBO que llega al biológico | Lodos PENDIENTES (09C, DPV-114) |
| Circulación, laboratorio y operación | 7 | EF | D | 25–40 % de lo anterior | — |

#### 3.8.1 Cómo cambia el terreno según la tecnología (sin elegir)

| Tecnología | Lógica de superficie en el modelo | Consecuencia |
|---|---|---|
| **Vuelco a colectora (cloaca)** | Solo pretratamiento + ecualización + DAF; biológico y lodos `NO_APLICA` | Mínimo terreno, **solo si el prestador lo acepta** (no se supone) |
| **Aerobio compacto** (lodos activados/SBR) | Volumen = DBO tras DAF ÷ 0,3–0,8 kg/(m³·d); profundidad 4–5 m; ×1,4–1,9 | Poco terreno, más energía y lodos |
| **Anaerobio + aerobio** | Reactor: DQO tras DAF ÷ 3–8 kg/(m³·d) (FTE-263: 7–11 en ensayos); pulido aerobio del 20–40 % | Terreno intermedio; biogás |
| **Lagunas** | Anaerobia: DBO ÷ 0,15–0,35 kg/(m³·d), 3–5 m; facultativa: 150–350 kg DBO/(ha·d); taludes ×1,2–1,5 | ~35–40 veces la superficie del biológico compacto — **RESULTADO DEL ESCENARIO DE SUPERFICIES ACTUAL / PROXY**, no relación general de ingeniería; más distancia a vecinos |

La relación real entre tecnologías **depende de tecnología, carga, clima, tiempo de retención, profundidad, calidad de efluente, terreno y normativa**. Las cargas de diseño de §3.8.1 son reglas de manual de ingeniería sanitaria **no leídas en esta sesión** (FTE-12C-006, `[PVDP]`); sirven para el **orden de magnitud** del terreno, no para diseñar.

### 3.9 Personal y administración

| Área | Zona | Cat. | Método | Driver | Dato faltante / referencia |
|---|---|---|---|---|---|
| Vestuarios y sanitarios **separados por zona (sucia/limpia) y por sexo** | 8 | PA | D (PROXY de dotación) | Personas por turno × 1,0–1,7 m² (+ lockers del 2.º turno) | **Dotación** (DPV-12C-02, `18_recursos_humanos` no iniciado); requisitos de vestuarios (DPV-090) |
| Comedor y office | 8 | PA | D | Personas simultáneas × 1,2–1,8 m² | Turnos de comida |
| Oficinas de administración | 9 | PA | D | Puestos × 8–12 m² | Organigrama |
| Oficina del servicio oficial (SENASA) con sanitario | 9 | PA | D | Superficie base | **Requisito edilicio del SIV** (DPV-12C-04) |
| Laboratorio de autocontrol / calidad | 9 | S | D | Ritmo; si es tercerizado: sala de muestras | Propio vs tercero (DEC-12C-04) |
| Enfermería y capacitación | 8 | PA | D | Superficie base | Higiene y seguridad (DPV-106) |
| Circulación de personal y filtros sanitarios | 8 | PA | D | 10–20 % de personal/admin | — |

**Dotación proxy (SUP-12C-10, solo para superficies):** personas por turno = 10–20 + 0,05–0,12 × ritmo (aves/h) × factor de automatización (manual 1,35 · semi 1,0 · auto 0,75) × factor de configuración (A 0,9 · B 1,0 · C 1,3). Da ~40 / 65 / 115 / 215 personas por turno (medio) para 2.500 / 5.000 / 10.000 / 20.000 aves/día a 8 h netas. **No es dotación**: es un sustituto para que vestuarios, comedor y estacionamiento no queden en cero; se reemplaza con `18_recursos_humanos`.

### 3.10 Reserva

| Área | Cat. | Método | Referencia |
|---|---|---|---|
| Reserva de terreno para expansión | R | Σ max(0, área a escala objetivo − área actual) por categoría; sin objetivo: 25 / 50 / 100 % de lo operativo (alerta) | SUP-12C-13; DEC-035; [`estrategia_expansion.md`](estrategia_expansion.md) |
| Reserva de rendering futuro | R | Ver §3.6 | DEC-027 |

## 4. Huellas de equipos a pedir en el RFQ (DPV-12C-01)

El plan de RFQ ([`../08_maquinaria/plan_rfq.md`](../08_maquinaria/plan_rfq.md)) ya pide "dotación, superficie y servicios del núcleo de la planta" para el lote 1. Para que el método F reemplace los proxies, cada respuesta debería incluir **layout de equipos con cotas** y la huella por área:

| Área del modelo (`footprints`) | Equipos ([`../08_maquinaria/matriz_equipos.csv`](../08_maquinaria/matriz_equipos.csv)) |
|---|---|
| `colgado_aturdido` | EQ-04, EQ-07, EQ-08, EQ-09/EQ-10 |
| `sangrado_escaldado_desplumado` | EQ-11 a EQ-18, EQ-20 |
| `evisceracion_inspeccion` | EQ-19, EQ-21 a EQ-33 |
| `enfriamiento` | EQ-34/35/36, EQ-37, EQ-38 |
| `clasificacion` | EQ-39 |
| `trozado` | EQ-40, EQ-41 |
| `deshuese` · `cms` | EQ-42 a EQ-46 · EQ-48 |
| `coproductos` | EQ-28, EQ-33, EQ-47 |
| `empaque` | EQ-49 a EQ-56 |
| `lavado_cajones` | EQ-05 |
| `tunel_congelado` | EQ-57 a EQ-61 |
| `sala_maquinas_frio` | EQ-64 |
| `caldera_agua_caliente` · `aire_comprimido` · `generador` | EQ-14 · EQ-71 · EQ-73 |
| `sala_subproductos` | EQ-66 a EQ-69 |

Además de la huella: **altura libre** requerida, **zona de mantenimiento** (desmontaje de ejes, tanques), **peso y cargas puntuales** sobre losa, **fosos y canales** en piso, **vano de montaje** (dimensiones del bulto más grande) y **servicios por punto** (agua, vapor, aire, desagüe). Sin estos datos, las superficies de proceso siguen siendo PROXY.
