# 04 — Balance de masa

**Alcance:** modelo del flujo de huevos, pollitos, aves y kg a lo largo de la cadena (incubación → engorde → faena → productos y subproductos), con mortalidad, conversión y rendimientos. Base para dimensionar escenarios.

**Reglas específicas**
- No fijar capacidad de faena a priori: trabajar con escenarios (ver DEC-001).
- Declarar base de cálculo (por ave, por kg vivo, por kg canal) y fuente de cada coeficiente.

**Relacionado:** `03_produccion_primaria` (pollitos, aves cargadas y faenadas, alimento), `05_proceso_industrial`, `06_productos`, `07_subproductos`, `11_agua_efluentes`, `12_energia_frio`.

## Contenido (versión 1.0, 2026-09-30)

| Archivo | Contenido |
|---|---|
| [`balance_por_ave.md`](balance_por_ave.md) | Unidad base, definiciones (peso vivo, eviscerado, carcasa fría, RTC, comercial), rangos por componente, balance primario por peso, menudencias, clases A/B/C/D/P, balance global, tres configuraciones, escalado |
| [`rendimientos_cortes.md`](rendimientos_cortes.md) | Trozado y deshuese; vivo vs carcasa; entero vs trozado vs deshuesado; efecto del peso |
| [`subproductos_masa.md`](subproductos_masa.md) | Patas/garras, plumas, sangre, vísceras no comestibles, cabezas, huesos; escalado |
| [`agua_y_mermas.md`](agua_y_mermas.md) | Chiller por inmersión vs aire, límites regulatorios, masa biológica vs agua; condenas y mermas |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos en palabras simples |
| [`conclusiones_balance.md`](conclusiones_balance.md) | Síntesis, datos débiles, datos a medir en planta y protocolo de ensayo, tests, calidad |
| [`modelo_balance_masa.py`](modelo_balance_masa.py) | Modelo reproducible (Python 3, sin dependencias externas) |
| [`escenarios_balance.csv`](escenarios_balance.csv) | Salida del modelo: 126 balances, una fila por salida + filas de control |

El balance de la cadena aguas arriba (pollitos → aves cargadas → aves faenadas, alimento) está en [`03_produccion_primaria/modelo_escenarios_produccion.py`](../03_produccion_primaria/modelo_escenarios_produccion.py) y no se duplica aquí.

## Documentación del modelo (regla 15)

**Uso**

```bash
python3 04_balance_masa/modelo_balance_masa.py                 # tests + CSV + resumen a 2,9 kg
python3 04_balance_masa/modelo_balance_masa.py --solo-tests    # solo pruebas
python3 04_balance_masa/modelo_balance_masa.py --peso 3.1 --config C --rendimiento alto \
        --condenas bajo --enfriamiento aire --aves-dia 8000    # balance a medida
```

Para cambiar supuestos, editar las tablas al inicio del script (`PRIMARIOS`, `AJUSTE_RENDIMIENTO`, `CORTES`, `DESHUESE`, `CMS_RENDIMIENTO`, `CONDENAS`, `ENFRIAMIENTO`, constantes de subproductos) y volver a correrlo: los tests se ejecutan siempre antes de generar salidas y el script **se detiene (código 1)** si alguno falla.

**Unidades y bases:** kg por ave (masa biológica, agua y total en columnas separadas); `pct_peso_vivo_bio` = % del peso vivo en planta; `pct_carcasa_bio` = % de la carcasa eviscerada antes de decomisos (solo salidas derivadas de la carcasa); t/día = kg/ave × aves/día / 1.000; t/año = t/día × 250 días de faena (SUP-025, SUP-044); `t_anio_1M_aves_anio` = kg/ave × 1.000.000 / 1.000.

**Fórmulas principales**

1. Fracción de cada componente primario: `f_i(PV) = f_i(2,9) + Δescenario_i + pendiente_i × (PV − 2,9)`, en % del PV; pérdidas no asignadas = 100 − Σ f_i.
2. Condenas: decomiso total `ft` sobre carcasa, cuello, menudencias y patas; decomiso parcial `fp` sobre la carcasa restante.
3. Enfriamiento: carcasa pre-chiller `c2`; inmersión: agua absorbida = `c2 × absorción`, goteo = agua absorbida × `goteo`, retenida = absorbida − goteo; aire: evaporación = `c2 × evaporación`.
4. Trozado: corte_j = carcasa fría × fracción_j(PV); deshuese: salida_k = corte × fracción_k; CMS = carcasa-esqueleto × rendimiento.
5. Agua retenida repartida entre salidas de la carcasa proporcionalmente a su masa biológica (las pérdidas P no retienen agua).
6. Cierre: `(PV + agua incorporada) − Σ salidas`, con tolerancia 1 × 10⁻⁶ kg/ave; además Σ masa biológica = PV y Σ agua = agua incorporada.

**Supuestos:** SUP-035 a SUP-044 en [`../00_gestion_proyecto/supuestos.md`](../00_gestion_proyecto/supuestos.md). **Fuentes:** FTE-140, FTE-142, FTE-161 a FTE-184 en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (todas `[PVDP]`).

**Columnas del CSV:** `escenario_id` (BAL-001…126), `clasificacion`, `peso_vivo_kg`, `configuracion` (A entero, B trozado, C deshuesado), `escenario_rendimiento`, `escenario_condenas`, `enfriamiento` (inmersion, inmersion_limite, aire), `etapa`, `componente`, `origen` (componente primario del que proviene la masa), `clase` (A/B/C/D/P o CONTROL), `destino_conceptual`, `masa_biologica_kg_ave`, `agua_kg_ave`, `total_kg_ave`, `pct_peso_vivo_bio`, `pct_carcasa_bio`, columnas de escala. Las filas `CONTROL` muestran entradas, salidas y error de cierre de cada balance. Separador decimal: punto.

**Grilla:** 6 pesos (2,2 / 2,5 / 2,8 / 3,0 / 3,2 / 3,5 kg) × 3 configuraciones × 7 variantes: rendimiento bajo/medio/alto (condenas medias, inmersión); condenas bajo/alto (rendimiento medio, inmersión); inmersión en el límite de 8 %; aire. El peso de referencia 2,9 kg (perfil medio de `03_produccion_primaria`) se calcula con `--peso 2.9`.
