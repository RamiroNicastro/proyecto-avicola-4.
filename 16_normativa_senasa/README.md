# 16 — Normativa y SENASA

**Alcance:** normativa sanitaria (SENASA: granjas, incubación, faena, alimento, transporte), tipos de habilitación (municipal, provincial, tránsito federal, exportación), normativa ambiental, bienestar animal, seguridad e higiene, plazos y costos de habilitación.

**Regla:** citar norma (número, año, organismo) y fecha de consulta; verificar vigencia.

**Relacionado:** DPV-007, DEC-009, `17_exportacion`.

## Contenido (sesión 09B, 2026-09-30)

| Archivo | Contenido |
|---|---|
| [`conclusiones_normativa.md`](conclusiones_normativa.md) | Síntesis de la hoja de ruta regulatoria, documentos pendientes y evaluación de calidad |
| [`mapa_regulatorio.md`](mapa_regulatorio.md) | Autoridades, tipos de habilitación, temas dependientes de la ubicación, contradicciones C1–C5 |
| [`habilitacion_planta.md`](habilitacion_planta.md) | Rol e índice práctico del Decreto 4238/68, secuencia tentativa de habilitación, plantilla jurisdiccional |
| [`requisitos_sanitarios.md`](requisitos_sanitarios.md) | Edilicios, agua, inspección, BPM/POES/HACCP, bienestar, transporte, frío, rotulado, trazabilidad |
| [`exportacion_y_certificaciones.md`](exportacion_y_certificaciones.md) | Escalera exportadora, auditorías, listados, Halal |
| [`subproductos_normativa.md`](subproductos_normativa.md) | Destinos regulatorios de sangre, plumas, vísceras, huesos, grasa, CMS, pet food, decomisos |
| [`ruta_critica_habilitacion.md`](ruta_critica_habilitacion.md) | Reglas de precedencia y decisiones irreversibles |
| [`preguntas_senasa.md`](preguntas_senasa.md) | 38 preguntas técnicas para SENASA / asesor |
| [`guia_ramiro.md`](guia_ramiro.md) | Explicación en lenguaje simple |
| [`matriz_regulatoria.csv`](matriz_regulatoria.csv) | Matriz de 60 requisitos |
| [`fuentes_09B.csv`](fuentes_09B.csv) | Fuentes nuevas de la sesión (pendientes de consolidar en `25_fuentes`) |
| [`actualizaciones_gestion_09B.md`](actualizaciones_gestion_09B.md) | Propuestas para `00_gestion_proyecto` y `25_fuentes` (sesión paralela) |

**Verificación:** ninguna norma se leyó en su texto original (acceso bloqueado, DPV-009). Todo contenido normativo es `[PVDP]`.

## Documentación de `matriz_regulatoria.csv` (regla 15)

Separador de campos: coma; codificación UTF-8; una fila por requisito. No contiene fórmulas ni cifras económicas.

| Columna | Contenido |
|---|---|
| `ID` | `REG-###` |
| `TEMA` | Tema regulatorio (habilitación, edilicio, agua, inspección, programas, bienestar, frío, transporte, trazabilidad, rotulado, subproductos, residuos, exportación, etc.) |
| `REQUISITO` | Requisito o pregunta regulatoria, sin copiar texto normativo |
| `AUTORIDAD` | Organismo competente probable |
| `NORMA` | Norma identificada (número/año) o "a identificar" |
| `JURISDICCION` | Nacional / Provincial / Municipal / Extranjero / Privado |
| `ETAPA_DEL_PROYECTO` | E0 terreno/zona · E1 proyecto · E2 documentación/aprobación · E3 construcción · E4 inspección/habilitación · E5 operación · E6 exportación |
| `OBLIGATORIO_CONDICIONAL` | Obligatorio / Condicional (con la condición) / No obligatorio |
| `FUENTE` | ID de `25_fuentes/registro_fuentes.csv` (`FTE-###`) o de `fuentes_09B.csv` (`FTE-09B-##`); "—" si no hay |
| `ESTADO_VERIFICACION` | Uno de: `VERIFICADO EN PRIMARIA`, `PVDP`, `DEPENDE DE JURISDICCIÓN`, `POR CONSULTAR A SENASA` |
| `IMPACTO` | Efecto sobre diseño, trámite, costo u operación |
| `ACCION_PENDIENTE` | Próximo paso (pregunta `P-##` de `preguntas_senasa.md`, registro DPV, lectura) |

## Documentación de `fuentes_09B.csv`

Mismas columnas que `25_fuentes/registro_fuentes.csv`. IDs provisorios `FTE-09B-##` para evitar colisiones con sesiones paralelas; se renumeran al consolidar ([`actualizaciones_gestion_09B.md` §7](actualizaciones_gestion_09B.md)).
