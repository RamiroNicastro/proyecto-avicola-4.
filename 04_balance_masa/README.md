# 04 — Balance de masa

**Alcance:** modelo del flujo de huevos, pollitos, aves y kg a lo largo de la cadena (incubación → engorde → faena → productos y subproductos), con mortalidad, conversión y rendimientos. Base para dimensionar escenarios.

**Reglas específicas**
- No fijar capacidad de faena a priori: trabajar con escenarios (ver DEC-001).
- Declarar base de cálculo (por ave, por kg vivo, por kg canal) y fuente de cada coeficiente.

**Relacionado:** `03_produccion_primaria` (pollitos, aves cargadas y faenadas, alimento), `05_proceso_industrial`, `06_productos`, `07_subproductos`, `11_agua_efluentes`, `12_energia_frio`.

## Alcance del módulo

Este es un **BALANCE DE MASA DEL AVE Y SUS PRODUCTOS**. **No** es todavía:

- un balance completo de agua industrial;
- un balance de efluentes;
- un balance energético;
- un modelo económico;
- un diseño de maquinaria.

Esos módulos usarán después estos resultados. **ESTE BALANCE NO DIMENSIONA EL CONSUMO INDUSTRIAL DE AGUA NI EL CAUDAL TOTAL DE EFLUENTES DE LA PLANTA.** El "agua" del modelo es solo el **agua incorporada a productos y subproductos** (agua absorbida por la carcasa en el chiller —retenida en producto o goteo del producto— y agua adherida a plumas).

## Contenido (versión 1.1, 2026-09-30)

| Archivo | Contenido |
|---|---|
| [`balance_por_ave.md`](balance_por_ave.md) | Unidad base, definiciones (peso vivo, eviscerado, carcasa fría, RTC, comercial), rangos por componente, balance primario por peso, menudencias, clases A/B/C/D/P, balance global, tres configuraciones, escalado |
| [`rendimientos_cortes.md`](rendimientos_cortes.md) | Trozado y deshuese; vivo vs carcasa; entero vs trozado vs deshuesado; efecto del peso |
| [`subproductos_masa.md`](subproductos_masa.md) | Patas/garras, plumas, sangre, vísceras no comestibles, cabezas, huesos; escalado |
| [`agua_y_mermas.md`](agua_y_mermas.md) | Chiller por inmersión vs aire, límites regulatorios, masa biológica vs agua; condenas y mermas |
| [`guia_ramiro.md`](guia_ramiro.md) | Conceptos en palabras simples |
| [`auditoria_balance.md`](auditoria_balance.md) | Auditoría conceptual v1.1: agua, decomisos vs pérdidas, patas → garras, carcasa → cortes, rutas alternativas (esqueleto/CMS), comparación desde la misma base, balance manual de 2,9 kg, tests de exclusividad |
| [`conclusiones_balance.md`](conclusiones_balance.md) | Síntesis, datos débiles, datos a medir en planta y protocolo de ensayo, tests, calidad |
| [`modelo_balance_masa.py`](modelo_balance_masa.py) | Modelo reproducible (Python 3, sin dependencias externas) |
| [`escenarios_balance.csv`](escenarios_balance.csv) | Salida del modelo: 144 balances, una fila por salida + filas de control |

El balance de la cadena aguas arriba (pollitos → aves cargadas → aves faenadas, alimento) está en [`03_produccion_primaria/modelo_escenarios_produccion.py`](../03_produccion_primaria/modelo_escenarios_produccion.py) y no se duplica aquí.

## Documentación del modelo (regla 15)

**Uso**

```bash
python3 04_balance_masa/modelo_balance_masa.py                 # tests + CSV + resumen a 2,9 kg
python3 04_balance_masa/modelo_balance_masa.py --solo-tests    # solo pruebas
python3 04_balance_masa/modelo_balance_masa.py --peso 3.1 --config C --rendimiento alto \
        --condenas bajo --enfriamiento aire --ruta-esqueleto venta --aves-dia 8000   # balance a medida
python3 04_balance_masa/modelo_balance_masa.py --peso 2.9 --auditoria  # tabla biológica y tabla de agua separadas
```

Para cambiar supuestos, editar las tablas al inicio del script (`PRIMARIOS`, `AJUSTE_RENDIMIENTO`, `CORTES`, `DESHUESE`, `CMS_RENDIMIENTO`, `CONDENAS`, `ENFRIAMIENTO`, constantes de subproductos) y volver a correrlo: los tests se ejecutan siempre antes de generar salidas y el script **se detiene (código 1)** si alguno falla.

**Rutas alternativas (exclusivas, SUP-045):** cada material se vende **o** se reprocesa, nunca ambas: `--ruta-esqueleto venta|cms` (por defecto venta en A/B, cms en C), `--ruta-cuello venta|cms` (venta), `--ruta-hueso-pechuga rendering|cms` (rendering; solo C), `--ruta-piel venta|rendering` (venta; solo C). Cada material enviado a CMS tiene su propia etapa (`CMS (esqueleto)`, `CMS (cuello)`, `CMS (hueso de pechuga)`).

**Unidades y bases:** kg por ave (masa biológica, agua y total en columnas separadas); `pct_peso_vivo_bio` = % del peso vivo en planta; `pct_carcasa_bio` = % de la carcasa eviscerada antes de decomisos (solo salidas derivadas de la carcasa); t/día = kg/ave × aves/día / 1.000; t/año = t/día × 250 días de faena (SUP-025, SUP-044); `t_anio_1M_aves_anio` = kg/ave × 1.000.000 / 1.000.

**Fórmulas principales**

1. Fracción de cada componente primario: `f_i(PV) = f_i(2,9) + Δescenario_i + pendiente_i × (PV − 2,9)`, en % del PV; pérdidas no asignadas = 100 − Σ f_i.
2. Condenas: decomiso total `ft` sobre carcasa, cuello, menudencias y patas; decomiso parcial `fp` sobre la carcasa restante.
3. Enfriamiento: carcasa pre-chiller `c2`; inmersión: agua absorbida = `c2 × absorción`, goteo = agua absorbida × `goteo`, retenida = absorbida − goteo; aire: evaporación = `c2 × evaporación`.
4. Trozado (cortes con piel y con hueso): corte_j = carcasa fría × fracción_j(PV); deshuese: salida_k = corte × fracción_k; CMS = materia prima de la ruta `cms` × rendimiento; residuo óseo = materia prima × (1 − rendimiento − merma).
5. Agua retenida repartida entre salidas de la carcasa proporcionalmente a su masa biológica (las pérdidas P no retienen agua).
6. Cierre: `(PV + agua incorporada a productos y subproductos) − Σ salidas`, con tolerancia 1 × 10⁻⁶ kg/ave; además Σ masa biológica = PV y Σ agua = agua incorporada. Identidades adicionales: pata bruta = garras + descarte + merma de acondicionamiento + decomiso; masa comestible disponible − merma real − reclasificado a C = comestible (A + B).

**Supuestos:** SUP-035 a SUP-045 en [`../00_gestion_proyecto/supuestos.md`](../00_gestion_proyecto/supuestos.md). **Fuentes:** FTE-140, FTE-142, FTE-161 a FTE-184 en [`../25_fuentes/registro_fuentes.csv`](../25_fuentes/registro_fuentes.csv) (todas `[PVDP]`).

**Columnas del CSV:** `escenario_id` (BAL-001…144), `clasificacion`, `peso_vivo_kg`, `configuracion` (A entero, B trozado, C deshuesado), `escenario_rendimiento`, `escenario_condenas`, `enfriamiento` (inmersion, inmersion_limite, aire), `ruta_esqueleto`, `ruta_cuello`, `ruta_hueso_pechuga`, `ruta_piel`, `etapa`, `componente`, `origen` (componente primario del que proviene la masa), `clase` (A/B/C/D/P o CONTROL), `destino_conceptual`, `masa_biologica_kg_ave`, `agua_kg_ave`, `total_kg_ave`, `pct_peso_vivo_bio`, `pct_carcasa_bio`, columnas de escala. Las filas `CONTROL` muestran, por separado, masa biológica (entrada/salidas), agua incorporada a productos y subproductos desagregada (absorbida en el chiller, retenida en producto, goteo del producto, adherida a plumas) y error de cierre. Separador decimal: punto.

**Grilla:** 6 pesos (2,2 / 2,5 / 2,8 / 3,0 / 3,2 / 3,5 kg) × 3 configuraciones × 7 variantes: rendimiento bajo/medio/alto (condenas medias, inmersión); condenas bajo/alto (rendimiento medio, inmersión); inmersión en el límite de 8 %; aire; más 3 variantes de ruta por peso (B con esqueleto a CMS; C con esqueleto vendido; C con esqueleto, cuello y hueso de pechuga a CMS y piel a rendering). Tests: 21 (ver [`auditoria_balance.md` §9](auditoria_balance.md)). El peso de referencia 2,9 kg (perfil medio de `03_produccion_primaria`) se calcula con `--peso 2.9`.
