# Estructura del data room de campo

**Fecha:** 2026-09-30 · **Versión:** 1.0 · Plan: [`plan_trabajo_campo.md`](plan_trabajo_campo.md) · Guía: [`guia_recoleccion_evidencia.md`](guia_recoleccion_evidencia.md)

> **Estructura conceptual.** No contiene documentos todavía ni datos de ejemplo inventados. Define dónde se guarda la evidencia de campo, cómo se nombra y cómo se vincula con la matriz de validación.

---

## 1. Dónde vive el data room

| Contenido | Dónde | Por qué |
|---|---|---|
| **Documentos de campo** (minutas, cotizaciones, fotos, planos, audios, contactos, cartas de intención, contratos, reportes de clientes) | **Carpeta privada fuera de este repositorio** (almacenamiento en la nube con acceso restringido a quienes el promotor autorice) | Incluyen datos confidenciales de terceros y datos personales. Un repositorio Git conserva el historial aunque después se borre un archivo |
| **Índice y resultados** (estado, dato obtenido, clasificación, código del documento) | Este repositorio: [`matriz_validacion_campo.csv`](matriz_validacion_campo.csv), registros de `00_gestion_proyecto` y `25_fuentes/registro_fuentes.csv` | Trazabilidad del estudio sin exponer el documento |

**Regla:** en el repositorio se cita el **código** del documento (§3), nunca se copia su contenido confidencial. Un dato que se usa en el estudio se transcribe como cifra con su clasificación y fuente; el documento queda en el data room.

## 2. Estructura de carpetas

```
DATA_ROOM_CAMPO/
├── 00_indice/                  índice maestro (planilla: código, fecha, actor, tema, tipo, DPV, confidencialidad, ubicación)
├── 01_inversores/              minutas de la reunión con inversores, confirmaciones escritas, documentación societaria
├── 02_demanda/
│   ├── red_supermercados/      minutas con compras y logística, reportes de compras, lista de locales, condiciones de alta
│   ├── otros_canales/          mayoristas, distribuidores, pollerías, gastronomía, elaboradores
│   ├── gondola/                planillas y fotos de relevamiento de góndola
│   ├── carniceria_familiar/    registros de ventas y habilitación
│   └── cartas_intencion/       LOI, pruebas piloto, órdenes de compra
├── 03_produccion/
│   ├── productores/            fichas, registros de crianzas, liquidaciones (anonimizadas)
│   ├── incubadoras/
│   └── alimento/
├── 04_plantas/                 hojas de visita, fotos autorizadas, datos compartidos por plantas
├── 05_subproductos/            rendering, pet food, traders, compradores de carcasa y menudencias
├── 06_normativa/
│   ├── senasa/                 minutas, respuestas escritas
│   └── textos_oficiales/       normas descargadas (original, con fecha de descarga)
├── 07_proveedores/             catálogos, fichas técnicas; cotizaciones solo cuando la fase lo habilite
├── 08_terrenos/                fichas de relevamiento, planos catastrales, factibilidades de servicios, análisis de agua
├── 09_contactos/               agenda de contactos (acceso restringido, ver §5)
└── 10_contratos_nda/           acuerdos de confidencialidad firmados, contratos
```

Cada carpeta temática corresponde a una ola del plan: 01–02 (O1–O2), 03 (O4), 04 (O3), 05 (O5), 06 (O6), 07 (O7), 08 (O8).

## 3. Convención de nombres

```
AAAA-MM-DD_actor_tema_tipo-documento[_vNN].ext
```

| Campo | Regla | Ejemplos de valores |
|---|---|---|
| `AAAA-MM-DD` | Fecha del hecho (reunión, visita, emisión del documento), no la de archivo | `2026-10-14` |
| `actor` | **Tipo de actor + código corto**, en minúsculas, sin espacios ni acentos. El nombre real de una persona **no** va en el nombre del archivo; la empresa puede ir abreviada si no es confidencial, si no se usa un código del índice | `inversores`, `red-compras`, `red-logistica`, `mayorista-m01`, `polleria-p03`, `frigorifico-f02`, `productor-pr05`, `incubadora-i01`, `rendering-r01`, `senasa-regional`, `prov-equipos-e01`, `terreno-t01` |
| `tema` | Tema principal, una o dos palabras con guion | `capital`, `volumen-mix`, `logistica`, `precios`, `facon`, `pollito`, `crianzas`, `efluentes`, `habilitacion`, `rendering` |
| `tipo-documento` | Uno de la lista siguiente | ver tabla |
| `_vNN` | Versión, solo si el documento se corrige | `_v02` |

| `tipo-documento` | Uso |
|---|---|
| `minuta` | Resumen escrito de reunión o llamada |
| `hoja-visita` | Hoja de observación de una visita a planta, granja o terreno |
| `ficha` | Ficha estructurada (productor, terreno) |
| `registro` | Planilla de datos (crianzas, góndola, ventas) |
| `cotizacion` | Precio ofrecido con condiciones |
| `lista-precios` | Lista de precios general (no personalizada) |
| `reporte` | Reporte de sistema entregado por un tercero |
| `foto` | Fotografía (con autorización si es dentro de un establecimiento) |
| `plano` | Plano, croquis, catastro |
| `audio` / `transcripcion` | Grabación con consentimiento y su transcripción |
| `norma` | Texto oficial descargado |
| `respuesta-oficial` | Respuesta escrita de un organismo |
| `loi` | Carta de intención |
| `orden` / `contrato` | Orden de compra o contrato |
| `nda` | Acuerdo de confidencialidad |
| `analisis` | Protocolo de laboratorio (agua, efluente) |

**Ejemplos (hipotéticos, solo para mostrar el formato):**

- `2026-10-14_inversores_capital_minuta.pdf`
- `2026-10-21_red-compras_volumen-mix_reporte.xlsx`
- `2026-11-04_frigorifico-f02_facon_hoja-visita.pdf`
- `2026-11-04_frigorifico-f02_facon_cotizacion.pdf`
- `2026-11-18_productor-pr05_crianzas_registro.xlsx`
- `2026-12-02_senasa-regional_habilitacion_minuta.pdf`

Fotos de una misma visita: `2026-11-04_frigorifico-f02_recepcion_foto_01.jpg`, `_02`, …

## 4. Índice maestro (`00_indice`)

Una fila por documento:

| Columna | Contenido |
|---|---|
| `codigo` | Nombre del archivo sin extensión |
| `fecha` | AAAA-MM-DD |
| `actor_tipo` / `actor_codigo` | Tipo y código del actor |
| `organizacion` | Nombre de la empresa u organismo (restringido si es confidencial) |
| `tema` | Tema |
| `tipo_documento` | Tipo |
| `dpv` | DPV que respalda (uno o varios) |
| `fte` | ID en `25_fuentes/registro_fuentes.csv`, si se registró |
| `nivel_evidencia` | Para demanda: E1–E6 ([`plan_validacion_comercial.md` §2](../02_clientes_demanda/plan_validacion_comercial.md)); para el resto: documento / cotización / declaración / observación |
| `confidencialidad` | `publica` · `interna` · `confidencial` · `bajo NDA` |
| `vence` | Fecha de validez (cotizaciones, NDA) |
| `responsable` | Quién lo cargó |

## 5. Datos sensibles y confidencialidad

1. **Datos personales** (nombres, teléfonos, correos de contactos) solo en `09_contactos/`, con acceso restringido. En minutas, matriz y registro de fuentes se usan **cargo y organización** o el código del actor.
2. **Información bajo NDA**: se marca `bajo NDA` en el índice, no se copia al repositorio y se respeta el plazo y el uso pactados.
3. **Fotos y audios**: solo con autorización explícita; si la planta no permite fotos, se describe en la hoja de visita.
4. **Liquidaciones, reportes y facturas de terceros**: se guardan anonimizados cuando es posible (sin CUIT, nombres ni montos individuales que no hagan falta).
5. **No se guardan datos inventados** ni "de ejemplo" en el data room: si un campo no se obtuvo, queda vacío y el DPV sigue abierto.
6. Las cartas de intención, contratos y documentos societarios deben ser revisados por un profesional antes de firmarse; el data room solo los archiva.

## 6. Vínculo con la matriz

`matriz_validacion_campo.csv` → columna `FUENTE_DOCUMENTAL` = `código del data room; FTE-xxx`. Ejemplo de formato: `2026-10-21_red-compras_volumen-mix_reporte; FTE-3xx`. Así cualquier cifra del estudio lleva a su documento sin exponerlo.
