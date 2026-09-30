# 07 — Subproductos

**Alcance:** aprovechamiento de subproductos: plumas, sangre, vísceras no comestibles, patas, cabezas, grasa, cama de pollo, huevos no incubables. Alternativas: venta a terceros, rendering propio, compostaje, biogás. Mercados y precios.

**Relacionado:** `04_balance_masa`, `06_productos`, `11_agua_efluentes`, DEC-027, DEC-029, DEC-031, DEC-032.

## Contenido (2026-09-30)

| Archivo | Contenido |
|---|---|
| [`mapa_subproductos.md`](mapa_subproductos.md) | **Mapa completo de salidas del ave**: inventario (kg/ave, % PV, clase, frío, vida útil, destinos), clasificación económica condicional, piel y grasa, sangre, plumas, vísceras, cabeza y huesos, pet food, índice de aprovechamiento (IAA) y escalado físico |
| [`rutas_valorizacion.md`](rutas_valorizacion.md) | Rutas de la carcasa (vender / CMS / rendering), árboles de decisión por material, 15 incompatibilidades, valorización técnica vs económica |
| [`rendering.md`](rendering.md) | Qué es el rendering, qué recibe, productos, comparación propio / tercerizado / venta directa |
| [`matriz_valorizacion.csv`](matriz_valorizacion.csv) | Matriz de 39 materiales: kg/ave, rutas, mercado, proceso, frío, regulación, nivel de valor relativo, riesgo, precio pendiente |
| [`escenarios_subproductos.csv`](escenarios_subproductos.csv) | t/día por material para 2.500–20.000 aves/día en 6 variantes de ruta (generado) |
| [`modelo_subproductos.py`](modelo_subproductos.py) | Generador del CSV y tests de trazabilidad |
| [`guia_ramiro.md`](guia_ramiro.md) | Guía breve para explicar el tema |
| [`conclusiones_valorizacion.md`](conclusiones_valorizacion.md) | Síntesis, lista maestra de precios, tareas de campo, riesgos y evaluación |
| [`cuestionario_subproductos.md`](cuestionario_subproductos.md) | (2026-09-30) Preguntas para rendering, pet food, traders de garras y compradores de carcasa, CMS y menudencias; grilla por material (compra / gratis / cobra, precio, volumen, frecuencia, presentación, temperatura, calidad, transporte, contrato) |

## Documentación del modelo (regla 15)

**Ejecución:** `python3 07_subproductos/modelo_subproductos.py` (tests + CSV) · `--solo-tests` · `--imprimir` (tabla por variante). Requiere Python 3.10+ y **solo** la biblioteca estándar; importa `04_balance_masa/modelo_balance_masa.py` (v1.1) **sin modificarlo**.

**Supuestos fijos:** 2,9 kg vivo en planta; rendimiento y condenas "medio"; chiller por inmersión; 250 días de faena/año (SUP-025, SUP-044); reefer de 25 t (`[PVDP · débil]`). Ningún parámetro físico nuevo: todo sale del balance.

**Variantes:** V1 trozado con carcasa-esqueleto vendida (referencia, SUP-050) · V2 trozado con esqueleto a CMS · V3 deshuesado con esqueleto a CMS · V4 deshuesado con esqueleto vendido · V5 deshuesado con esqueleto, cuello y hueso de pechuga a CMS y piel a rendering · V6 pollo entero.

**Fórmulas:**

```
grupo_g (kg/ave) = Σ componentes del balance asignados al grupo g   (cada componente en un solo grupo)
t/día(N)         = total_kg_ave × N / 1000        N = 2.500, 5.000, 10.000, 20.000 aves faenadas/día
t/año(10.000)    = t/día × 250
D01 rendering    = Σ clase C (bio + agua)                       [no sumable]
D02 ampliada     = D01 + decomisos + contenido GI                [no sumable; solo si la norma lo permite]
D06 CMS potencial= carcasa-esqueleto vendida × rendimiento de CMS (0,60)   [no sumable; alternativa a G03]
D07 días garras  = 25.000 kg / (garras grado A kg/ave × N)       [columnas t_dia_* contienen DÍAS]
```

**Columnas de `escenarios_subproductos.csv`:** `variante`, `descripcion_variante`, `configuracion`, rutas (`ruta_esqueleto`, `ruta_cuello`, `ruta_hueso_pechuga`, `ruta_piel`), `grupo_id` (G01–G24 grupos; D01–D07 derivadas; CTRL control), `material`, `familia`, `clase_balance` (A/B/C/D/P del balance), `tipo_fila`, `sumable` (si/no), `masa_biologica_kg_ave`, `agua_kg_ave`, `total_kg_ave`, `pct_peso_vivo_bio`, `t_dia_2500` … `t_dia_20000`, `t_anio_10000`, `nota`. Separador decimal: punto.

**Columnas de `matriz_valorizacion.csv`:** `kg_ave` (3 decimales; base en `base_kg`: masa biológica salvo plumas húmedas y agua de goteo), `ref_modelo` (origen en el balance), `clase_con_comprador` / `clase_sin_comprador` (SUP-046), rutas 1–3 y `rutas_incompatibles`, `nivel_valor_con_comprador` / `nivel_valor_sin_comprador` (VALOR ALTO / MEDIO / BAJO / COSTO, ordinal y argumentado, SUP-047), `dato_precio_pendiente` (DPV). Los precios mencionados son referencias débiles ya registradas: **no** se usan para calcular.

**Tests (9):** S01 balance v1.1 intacto (21/21) · S02 cierre Σ grupos = PV + agua por variante · S03 cada componente en un solo grupo y clase · S04 rutas exclusivas (esqueleto vendido XOR CMS; piel vendida XOR rendering) · S05 filas derivadas no sumables · S06 sin masas negativas · S07 escalado lineal · S08 kg/ave de ambas matrices = balance (tolerancia 0,0006 kg) · S09 CMS potencial = CMS calculada por el balance en V2. Si un test falla, el script se detiene sin escribir el CSV.

**Limitaciones:** hereda todas las del balance v1.1 (ningún dato de planta argentina; DPV-060). No contiene precios, rendimientos de rendering, ni energía, agua de proceso o efluentes.
