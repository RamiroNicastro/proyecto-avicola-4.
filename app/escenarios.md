# Escenarios de la app

## 1. Formato (JSON versionado)

```json
{
  "formato": "ESCENARIO_APP_AVICOLA", "version_formato": 1,
  "id": "…", "nombre": "…", "descripcion": "", "tipo": "USUARIO | PRESET | DEMO_ARTIFICIAL",
  "solo_demostracion": false, "creado": "AAAA-MM-DDThh:mm:ss", "modificado": "…",
  "simple": {
    "objetivo": "GANAR_MAS | INVERTIR_MENOS | RECUPERAR_RAPIDO | REDUCIR_RIESGO | CRECER | BALANCEADO | null",
    "capital": {"no_se": true, "valor": null, "moneda": "USD | ARS", "tc": null, "tipo_tc": null, "fecha_tc": null, "fuente_tc": null, "metrica": "PICO_FONDOS"},
    "demanda": [{"producto", "canal", "mercado", "categoria", "valor", "unidad", "toma_todo", "fuente", "estado"}],
    "categorias_vendibles": ["DOCUMENTADA", "ASEGURADA", "NEGOCIADA", "INTERESADA", "POTENCIAL", "ESCENARIO"], "alfa_negociada": null,
    "precios_venta": [{"producto", "canal", "mercado", "valor", "moneda", "unidad", "fuente", "estado": "VALIDADO | COTIZACION | ESCENARIO | NO_SE"}],
    "costos_unitarios": [{"concepto": "alimento | pollito | facon_faena", "valor", "moneda", "fuente", "estado"}],
    "arquitectura": {"modo": "AUTO | MANUAL", "configuracion": "C0…CF", "variante": null},
    "escala": {"modo": "AUTO | VALOR", "valor": 10000},
    "restricciones": {"FONDOS_INICIALES": …, "PAYBACK": …, "VAN": …, "TIR": …, "DSCR": …, "RIESGO": …, "SUPERFICIE_TERRENO": …, "DEMANDA_MAXIMA_T_DIA": …},
    "horizonte_anios": null
  },
  "experto": {
    "comun": { …misma estructura que 21_modelo_financiero/plantilla_escenario_usuario.json… },
    "por_alternativa": {"C1|BASE|10000|ESCALA_UNICA": {"etapas": [{…}], "financiamiento": {…}}},
    "base_valores": {…}, "disponibilidad": {…}, "plantilla": null,
    "analisis": {"<parámetro de inputs_riesgo_optimizacion.csv>": valor},
    "perfil_analisis": "RAPIDO | COMPLETO", "trayectorias": false,
    "stress": [{"id", "nombre", "shocks": {"variable": valor}}], "distribuciones": […], "correlaciones": […],
    "override_total_confirmado": false
  },
  "procedencia": {},
  "sello": {"version_app", "version_motor", "commit", "fecha_commit"}
}
```

- `null` = PENDIENTE. La capa **simple** se aplica sobre la **experta** (demanda, precios, capital, restricciones, horizonte); el resto vive solo en `experto`.
- Un archivo con otro `formato` o `version_formato` se rechaza con un mensaje claro (no se adivina).
- Los IDs de alternativa son los del optimizador: `CONFIG|VARIANTE|ESCALAS|TRAYECTORIA` (en la demo, con prefijo `DEMO-`).

## 2. Operaciones

| Acción | Dónde | Detalle |
|---|---|---|
| Guardar | botón **Guardar** | `app/datos_locales/escenarios/<id>.json` con el `sello` de versión. Presets y demo se guardan como copia |
| Duplicar · Renombrar · Eliminar | **Escenarios** | Eliminar solo afecta escenarios guardados (nunca evidencia ni escenarios base) |
| Exportar | **Escenarios** o resultado | JSON con sello; CSV y resumen imprimible del resultado |
| Importar | **Escenarios → Importar JSON…** | Valida formato y versión; recibe un id nuevo |

Un escenario guardado **nunca se mezcla con la evidencia**: está en otra carpeta, se rotula ESCENARIO/SIMULACIÓN y no lo lee ningún modo evidencia del motor. `app/datos_locales/` está en `.gitignore`; para compartir un escenario se exporta.

## 3. Presets (estructurales, sin valores económicos)

| Preset | Contenido |
|---|---|
| `preset_conservador` | objetivo REDUCIR_RIESGO; plantilla de curva PLANTILLA_CONSERVADOR (forma ilustrativa SUP-196) |
| `preset_base` | objetivo GANAR_MAS; plantilla PLANTILLA_BASE |
| `preset_expansivo` | objetivo CRECER; plantilla PLANTILLA_EXPANSIVO; trayectorias multietapa habilitadas |

No tienen precios, costos, demanda, capital, tasas ni impuestos (test `test_presets_sin_valores_economicos`).

## 4. DEMO_ARTIFICIAL (SOLO_DEMOSTRACION)

`escenarios_base/demo_artificial.json`, generado por [`backend/demo.py`](backend/demo.py) (`python3 app/backend/generar_base.py`).

- **Todos los números son ficticios** (reglas redondas por escala: CAPEX = fijo + USD/ave·día; OPEX por módulo en USD/ave o USD/año; precios, demanda —incluida una línea ASEGURADA ficticia—, tasas, impuestos, deuda, disponibilidades físicas, stress y distribuciones ARTIFICIALES). No son datos, estimaciones ni supuestos del proyecto (SUP-242).
- Corre en el universo **ARTIFICIAL_TEST** del motor (etiqueta `CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO`); las alternativas llevan prefijo `DEMO-`; la app muestra ✱ SOLO DEMOSTRACIÓN en cada pantalla y en los exports.
- Cubre C0–CF × 2.500 / 5.000 / 10.000 / 20.000 con CAPEX/OPEX que respetan los módulos de cada arquitectura (pasan la defensa TF-004). Variantes y trayectorias quedan incompletas a propósito (muestran NO CALCULABLE y COMPARABILIDAD = FALSE).
- Sirve para ver: resultado completo, NO_INVERTIR_AUN (con capital bajo), ROJO por gate físico (C0-20000: façon disponible < escala), TIR ambigua, comparación, Pareto, tornado, 2D, stress, quiebres y Monte Carlo simulado.
