# Simulador HTML v0.1 — escala física del proyecto

**Fecha:** 2026-09-30 · **Estado:** v0.1 interna (Ramiro y familia). **No es una web pública ni el modelo financiero.**

Interfaz visual de los modelos ya aprobados para mover las variables de escala y ver qué tiene que ser verdad: aves, granjas, alimento, productos, subproductos, inventario y demanda. **Solo física**: no muestra ni estima CAPEX, OPEX, precios, ingresos, EBITDA, VAN, TIR ni payback. Especificación de origen: [`../especificacion_simulador_html.md`](../especificacion_simulador_html.md). Observaciones de esta versión: [`observaciones_html_v01.md`](observaciones_html_v01.md).

## 1. Cómo abrir el simulador

1. Abrir **`index.html`** con doble clic (Chrome, Edge, Firefox o Safari). No necesita servidor, instalación ni Internet.
2. Elegir el escenario (A / B / C) en la barra superior y mover los parámetros del panel izquierdo. En celular, el panel se abre con el botón **Parámetros**.

**Por qué funciona desde `file://`:** los navegadores bloquean `fetch()` de un JSON local, así que el generador escribe los mismos datos dos veces: `data/simulador_data.json` (para herramientas y validación) y `data/simulador_data.js` (`window.SIMULADOR_DATA = {...}`), que `index.html` carga con una etiqueta `<script>`. No hay CDN, fuentes web ni librerías externas; los gráficos son HTML/CSS/SVG propios.

Los parámetros de los tres escenarios se guardan en el navegador (`localStorage`) si está disponible; si no, el simulador funciona igual con los valores por defecto. «Exportar A/B/C» descarga un JSON para compartir o archivar; «Importar» lo vuelve a cargar.

## 2. Cómo regenerar los datos

Cada vez que cambie un modelo aprobado (producción, balance, subproductos, escala) o la demanda:

```
python3 23_plan_expansion/simulador_html/generar_datos_simulador.py   # ejecuta los tests de los modelos y escribe data/
node    23_plan_expansion/simulador_html/validar_simulador.js         # comprueba que el HTML reproduce los modelos (9 verificaciones)
```

Opcional, prueba en un navegador real sin red (requiere Playwright, que **no** es dependencia del simulador):

```
NODE_PATH="$(npm root -g)" node 23_plan_expansion/simulador_html/pruebas/prueba_navegador.js [carpeta_para_capturas]
```

El generador se **detiene** sin escribir datos si falla alguna prueba de los modelos (`modelo_escala.ejecutar_tests`: 23 pruebas propias que incluyen las de producción, balance y subproductos).

## 3. Archivos

| Archivo | Qué es | ¿Editar a mano? |
|---|---|---|
| `index.html` | Estructura de la página | Sí (interfaz) |
| `styles.css` | Estilos; tema claro/oscuro; responsive | Sí (interfaz) |
| `app.js` | Interfaz: panel, pestañas, gráficos, alertas visibles, explicaciones «¿Qué significa esto?», autoverificación | Sí (interfaz) |
| `calculo.js` | Motor de cálculo puro (sin DOM), usado por el navegador y por Node | Solo con validación (ver §5) |
| `generar_datos_simulador.py` | Toma los modelos aprobados y exporta coeficientes + casos de prueba | Sí (herramienta) |
| `validar_simulador.js` | Validación HTML ↔ modelos ↔ CSV | Sí (herramienta) |
| `pruebas/prueba_navegador.js` | Prueba opcional en Chromium sin red | Sí (herramienta) |
| **`data/simulador_data.json`** | Datos generados | **NO: se regenera** |
| **`data/simulador_data.js`** | Mismos datos embebidos para `file://` | **NO: se regenera** |
| `observaciones_html_v01.md` | Observaciones, decisiones de interfaz y limitaciones de esta versión | Sí |

## 4. Versión de los modelos que usa

| Modelo | Versión | Qué aporta |
|---|---|---|
| [`../modelo_escala.py`](../modelo_escala.py) | 1.1 (2026-09-30) | kg/ave por ítem (`kg_por_ave`), rendimientos del mix, mixes y demanda, perfiles de destino, fórmulas de escala |
| [`../../03_produccion_primaria/modelo_escenarios_produccion.py`](../../03_produccion_primaria/modelo_escenarios_produccion.py) | 1.1 | Parámetros y fórmulas de pollitos, plazas, m², alimento y agua (`mp.calcular`) |
| [`../../04_balance_masa/modelo_balance_masa.py`](../../04_balance_masa/modelo_balance_masa.py) | 1.1 | Balance por ave (vía `modelo_escala`) |
| [`../../07_subproductos/modelo_subproductos.py`](../../07_subproductos/modelo_subproductos.py) | 1.0 | Variantes V1/V3/V6 y agrupación (vía `modelo_escala`) |
| [`../escenarios_escala.csv`](../escenarios_escala.csv) | generado por escala 1.1 | Referencia de validación |
| `02_clientes_demanda/escenarios_demanda.csv`, `supermercados.md` §2.2 | — | Escenarios de demanda y mixes M1–M3 |

La versión exacta, el último commit y el SHA-256 de cada archivo quedan en `meta` del JSON y se muestran en la pestaña **Supuestos** y en el pie de página.

## 5. Cómo se conectan los modelos

```
modelos aprobados (Python, sin modificar)
  └─ generar_datos_simulador.py
       ├─ corre modelo_escala.ejecutar_tests()  → si falla, se detiene
       ├─ exporta COEFICIENTES:
       │    kg/ave de los 20 ítems del balance y sus agregados × config A/B/C × peso 2,0–3,8 kg (paso 0,1)   ← modelo_escala.kg_por_ave
       │    rendimientos por parte para los mixes, por peso                                   ← modelo_escala.rendimientos_mix
       │    parámetros de producción (perfiles, desempeños, calendario, constantes)           ← mp.*
       │    demanda (escenarios, locales, mixes, factor milanesa), perfiles de destino, contenedor, camiones
       ├─ exporta CASOS DE PRUEBA calculados en Python: 300 de producción, 300 de demanda vs capacidad
       └─ copia la tabla central del CSV como referencia (184 valores)
  → data/simulador_data.json  y  data/simulador_data.js
       └─ calculo.js aplica:
            (1) fórmulas lineales documentadas en modelo_escala.py (× aves, × días, ÷ horas, ÷ capacidad,
                conversión día operativo ↔ día calendario, inventario = flujo × días);
            (2) port 1:1 de mp.calcular (fórmulas cerradas) con el escalado por días/año de modelo_escala.produccion;
            (3) port 1:1 de modelo_escala.aves_por_mix y comparar_demanda.
       └─ app.js presenta los resultados; al cargar, autoverifica 784 valores contra los modelos.
```

**El simulador no reimplementa el balance de masa**: lee los kg/ave del modelo. Todo cambio de fórmula en `calculo.js` debe mantener `validar_simulador.js` en 9/9.

## 6. Entradas y salidas

**Modo simple (panel «Lo esencial»):** escala (2.500 / 5.000 / 10.000 / 20.000 o valor propio 500–30.000), utilización (10–100 %), peso vivo (2,0–3,8 kg), días de faena por año (250 / 300), escenario de demanda (conservador, base, expansivo, red de 90 locales × 25–300 kg, solo demanda documentada ≈ 0, manual), configuración comercial (A entero / B trozado / C deshuesado), días de inventario y su base temporal.

**Modo avanzado (desplegable):** días/semana, días/año, horas netas, perfil de mercado y nivel de desempeño (atajos de SUP-026/027/028), edad, mortalidad en granja, FCR, mortalidad en transporte, días entre lotes, densidad, método de conversión de la demanda (M0 ave completa / M1–M3 mix), perfil de destino, días de congelado/exportación, % de granjas propias, m² por productor, capacidades de vehículos.

**Pestañas:** RESUMEN · DEMANDA · PRODUCCIÓN · PLANTA · PRODUCTOS · SUBPRODUCTOS · INVENTARIO · COMPARADOR · SUPUESTOS · ECONOMÍA DEL PROYECTO (deshabilitada: «Disponible en una versión posterior»). Cada módulo tiene un botón **«¿Qué significa esto?»** con contenido de las guías de Ramiro y cada cifra una etiqueta de estado: **Validado por modelo · Supuesto · PVDP · Dato de campo pendiente**.

## 7. Pruebas realizadas (2026-09-30)

| Prueba | Resultado |
|---|---|
| V01 · el HTML reproduce **cada fila numérica** de `escenarios_escala.csv` (4 escalas × 2 calendarios, 14 bloques) | 4.224 / 4.224, diferencia 0 (tolerancia 1e-6) |
| V02 · port de `mp.calcular` vs Python, parámetros aleatorios | 300 casos × 37 variables, tolerancia relativa 1e-12 |
| V03 · demanda vs capacidad M0–M3 vs Python, pesos y configuraciones aleatorios | 300 casos |
| V04 · 4.000 escenarios aleatorios: sin NaN, sin negativos, utilización y cobertura ≤ 100 %, demanda no atendida ⇔ factor > 100 % | 0 fallas en 2,8 millones de valores |
| V05 · 16 entradas incompatibles bloquean el cálculo | OK |
| V06 · A/B/C independientes; cambiar la escala actualiza resultados | OK |
| V07 · `.js` = `.json`; referencia embebida = CSV | OK |
| V08 · offline: sin URLs externas ni accesos de red | OK |
| V09 · sin variables económicas | OK |
| Navegador (Chromium, `file://`, red bloqueada): 10 pestañas sin NaN, cambio de escala, demanda > capacidad, A/B/C, bloqueo de entradas, sin scroll horizontal a 390 / 820 / 1.366 / 1.920 px, 0 pedidos de red, 0 errores de consola | 11 / 11 |

## 8. Limitaciones actuales

- **Sin economía**: ninguna cifra de CAPEX, OPEX, precios, ingresos ni indicadores (módulos 19–21 no construidos).
- Balance fijo en rendimiento y condenas **medios** y chiller por **inmersión** (SUP-050); rutas de CMS por defecto de cada configuración. No se exponen las variantes bajo/alto ni el enfriamiento por aire.
- Peso en pasos de 0,1 kg (el balance se exporta en esa grilla); el modelo no vincula peso con edad ni con FCR: el simulador **avisa** pero no corrige.
- Días/semana solo 5 o 6 (lo que admite el modelo de producción).
- Demanda: escenarios de prueba categoría C/D; la exportación de la demanda es 0 (SUP-022). Sin perfil de destino «manual».
- Productores y camiones solo con dato ingresado por el usuario (DPV-048, DPV-084); por defecto se muestran m² y toneladas.
- Umbrales de alertas de interfaz (no son datos del proyecto): ver `observaciones_html_v01.md` §3.
- No hay gates de expansión (AL11) ni localización, agua industrial, efluentes, energía o frío dimensionados.

## 9. Próximas versiones (propuesta, sujeta a las fases del proyecto)

**v0.5** — variantes del balance (rendimiento/condenas bajo-alto, chiller por aire o al límite, rutas de CMS) exportadas como coeficientes; sensibilidad tornado de las variables físicas; perfil de destino manual; panel de gates G0–G3 con las variables V1–V18 que tengan evidencia cargada (AL11); datos de campo reales a medida que se completen DPV-003/037/048/084; exportar el escenario a PDF para reuniones.

**v1.0** — sección **Economía del proyecto** conectada a los módulos aprobados de CAPEX, OPEX y modelo financiero (cuando existan), con los mismos escenarios A/B/C; precios por parte y destino para el «ingreso total por ave»; capital de trabajo; comparación de escalas y fases de inversión sin declarar ganador automático.
