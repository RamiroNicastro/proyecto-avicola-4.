# Observaciones — simulador HTML v0.1

**Fecha:** 2026-09-30 · Sesión de interfaz (paralela a las sesiones técnicas). **No se modificaron** modelos científicos, `00_gestion_proyecto/` ni `25_fuentes/`. Las observaciones que afectan registros vivos (supuestos, decisiones, datos por validar) quedan aquí para que las incorpore la sesión responsable.

## 1. Errores técnicos en los modelos

**No se detectó ningún error técnico imprescindible.** Los modelos pasan sus pruebas (escala 23/23, que incluye producción, balance 21 y subproductos 9) y el motor del simulador reproduce las 4.224 celdas numéricas de `escenarios_escala.csv` sin diferencias, más 600 casos calculados en Python con parámetros aleatorios. No se detuvo ninguna parte del trabajo.

## 2. Observaciones sobre los modelos (no son errores; para las sesiones técnicas)

| # | Observación | Tratamiento en v0.1 |
|---|---|---|
| O1 | `modelo_escala.produccion()` solo permite cambiar peso, edad, FCR y mortalidad; DOA, días entre lotes y densidad quedan fijos en el desempeño medio, aunque `mp.calcular` los admite. | El simulador llama a la misma lógica (port 1:1 de `mp.calcular` + el mismo escalado por días/año) con los siete parámetros; se valida contra Python con esos parámetros variando. |
| O2 | El modelo no vincula **peso con edad** ni **peso con FCR** (perfiles SUP-027/028 son puntos aislados). Un usuario puede pedir 3,4 kg a 38 días con FCR 1,70. | Atajos «perfil de mercado» y «nivel de desempeño» fijan combinaciones coherentes; alertas INC1 (ganancia diaria fuera de ~58–62 g/día ±15 %) e INC2 (peso cambiado con FCR de referencia; muestra el FCR interpolado entre perfiles). Candidato a modelar en producción primaria. |
| O3 | El balance usado por `modelo_escala` está fijo en rendimiento y condenas «medio» y chiller por inmersión; `rendimientos_mix` también. | No se exponen variantes en v0.1 (propuesta v0.5). |
| O4 | La tabla central del CSV calcula `demanda_necesaria_*` y `kg_por_local_dia` a plena escala; `comparar_demanda` usa la capacidad E, independiente de la utilización supuesta. | El simulador muestra dos utilizaciones rotuladas: **supuesta** (entrada) y **la que justifica la demanda** (modelo). La tabla central se calcula a la utilización supuesta y coincide con el CSV a 100 %. La demanda necesaria se muestra a la utilización supuesta y a 100 %. |
| O5 | `excedente_partes_kg_dia_cal` del CSV es el excedente del mix para **toda** la demanda; `kg_sin_destino_plena_escala` lo escala por la cobertura. | En la tabla de métodos y en la alerta AL4 se muestra excedente × cobertura (partes producidas para la demanda efectivamente atendida), coherente con `kg_sin_destino_plena_escala`. |
| O6 | El CSV aplica los mismos días a refrigerado, congelado y exportación; la especificación propone 3 d refrigerado / 14 d congelado. | Dos entradas: días de inventario (total y refrigerado) y días de congelado/exportación (avanzado, 14 por defecto). Con días iguales reproduce el CSV. |
| O7 | «Producción sin destino» a la utilización supuesta (M0) = producción comestible por día calendario a esa utilización − demanda. No es una variable del CSV. | Aritmética lineal sobre variables del modelo; se rotula como M0 y como cota. |
| O8 | Registros: la sesión responsable podría registrar como supuestos de interfaz los umbrales de §3 si se adoptan fuera del simulador, y actualizar el estado de `especificacion_simulador_html.md` («no construido») y el índice de `23_plan_expansion/README.md` (no se editaron para no interferir con las sesiones técnicas en curso). | Pendiente de la sesión técnica. **Resuelto en la reconciliación 09 (2026-09-30):** especificación y README de `23_plan_expansion/` actualizados; los umbrales de §3 se registraron como criterios de interfaz en la anotación de SUP-060, **sin** crear supuestos de proyecto (no se adoptan fuera del simulador). |

## 3. Decisiones de interfaz (no son datos del proyecto)

| Tema | Decisión | Motivo |
|---|---|---|
| Umbral «utilización muy baja» | < 50 % | Convención de interfaz: la mitad de lo construido sin uso. |
| Umbral «alto volumen de subproductos» | ≥ 5 t/día operativo de clase C | `escenarios_escala.md` §10: ~5,3 t/día ya es un flujo industrial diario. Debajo se muestra una nota: el retiro es diario en cualquier escala. |
| Umbral «inventario alto» | ≥ 7 días | Convención de interfaz (una semana); el refrigerado vive días (SUP-051). |
| Umbral «ritmo por encima del rango estudiado» | > 2.500 aves/h | Máximo del rango de los modelos (20.000 aves/día a 8 h netas). Notas adicionales: horas netas < 8 (equipos más rápidos) y > 10 (segundo turno = capacidad de la línea, DEC-036). |
| «Pollo por local» | > 300 kg/local/día a plena escala | AL10 de la especificación. |
| Peso en pasos de 0,1 kg | Grilla 2,0–3,8 kg | La especificación (§5) propone esa grilla; el balance no extrapola fuera de 2,0–3,8 kg. |
| Escala personalizada | 500–30.000 aves/día | Rango I1 de la especificación. |
| Precarga A/B/C | 5.000 / 10.000 / 20.000, resto igual (5 d, B, base, 70 %) | Ejemplo pedido en el encargo; la especificación sugería otra combinación, que el usuario puede armar. |
| Escenarios de demanda | Comerciales C/D + red 90 × 25–300 kg + «solo demanda documentada (≈ 0)» + manual | Se excluyen las filas `sensibilidad_exportacion` porque el CSV indica que no se suman a la demanda. |
| Estado del dato por cifra | Una etiqueta por fila: la dependencia más débil (producción → Supuesto; balance → PVDP; demanda real, productores, vehículos → Dato de campo pendiente; aritmética de entradas → Validado por modelo) | Regla 4 y 16 de CLAUDE.md. «Validado por modelo» = cálculo verificado, no dato comprobado en la realidad. |
| Visualización del pollo | Sankey simplificado SVG propio, 7 colores de la paleta categórica validada + gris para residuos; tabla al lado (vista accesible) | Sin librerías externas. |
| Tres métricas | Colores, íconos, rótulo «de la planta / demanda ÷ capacidad / de la demanda» y forma de medidor distintos; el factor tiene marca de 100 % | Punto 6 del encargo; SUP-060. |

## 4. Elementos de la especificación no incluidos en v0.1

- AL11 (gates V1–V18): requiere cargar evidencia; queda para v0.5.
- Perfil de destino «manual» (I14) y productores/camiones con valores por defecto (sin dato: DPV-048, DPV-084).
- Días de faena para contenedor se calculan con la carga de 25 t `[PVDP · débil]`; no se ofrece otra carga.
- Economía del proyecto: solo la estructura, deshabilitada.

## 5. Riesgos de uso a comunicar a la familia

1. El simulador es **aritmética de escenarios**: la exactitud del cálculo (verificada) no convierte los supuestos en datos.
2. La demanda documentada es ≈ 0: toda utilización que la demanda «justifica» sale de hipótesis C/D.
3. Masa disponible no es producto vendido; subproducto sin receptor es costo.
4. Ninguna escala es «la recomendada»; el comparador no declara ganador.

## 6. Auditoría semántica final (2026-09-30)

Cambios de **presentación y definiciones**; ningún modelo científico cambia. `validar_simulador.js` V01 confirma que las 4.224 cifras de `escenarios_escala.csv` siguen reproduciéndose sin diferencias.

| Tema | Antes | Ahora |
|---|---|---|
| Utilización | Una «utilización» de entrada y otra «que justifica la demanda» | **Utilización operativa asumida** (entrada) vs **utilización requerida por demanda** = mín(factor; 100 %) (modelo), en tarjetas distintas |
| Cobertura | Solo la del modelo (a capacidad instalada): mostraba 100 % aunque se asumiera 50 % | **Cobertura con la producción simulada** = mín(capacidad instalada × utilización asumida ÷ capacidad requerida; 100 %) y **cobertura máxima a plena capacidad** (= `cobertura_demanda` del modelo), siempre por separado |
| Capacidad ociosa | Una cifra | **Capacidad ociosa operativa** (instalada − producción simulada) y **capacidad disponible respecto de la demanda** (instalada − requerida; = `capacidad_ociosa_aves_dia_operativo` del modelo) |
| Etiqueta de certeza | «Validado por modelo» | **«Calculado por modelo»**, con la aclaración de que no es validación en planta real |
| Escala | 500–30.000 en el modo simple | Simple: 2.500–20.000 (rango principal estudiado). Avanzado: 500–30.000 con «ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO» |
| Peso | 2,0–3,8 kg sin distinción | Rango principal 2,2–3,5 kg (pesos del balance v1.1, exportados como `pesos_estudiados`); fuera de él, advertencia de extrapolación sin bloqueo |
| Peso–edad–FCR | Avisos informativos | Si es incoherente: alerta «Escenario matemático. La combinación peso–edad–FCR requiere validación zootécnica.» y etiqueta en las salidas de granja y alimento. No se corrige ni se inventa una relación. Umbral de FCR ±0,15 (= diferencia medio–desfavorable de SUP-026), de interfaz |
| Configuraciones | «A · entero / B · trozado / C · deshuesado» | **Pollo entero / Trozado / Deshuesado / mayor procesamiento**; A/B/C solo para los escenarios del comparador. También se quitaron las letras de clase (A/B/C/D/P) y de categoría de demanda (A+B, C/D) de los textos visibles |
| Demanda documentada ≈ 0 | Opción «Solo demanda documentada (≈ 0)» | Recuadro «DEMANDA DOCUMENTADA ACTUAL: NO VALIDADA / PRÁCTICAMENTE NULA» y alerta «Este escenario simula producción al X %, pero actualmente no existe demanda documentada que respalde ese nivel de operación» |
| Umbrales de interfaz | «Convención de interfaz» | **Umbral visual ilustrativo**, con el texto «Umbral de interfaz, pendiente de calibración económica y operativa» en las alertas y en la pestaña Supuestos |
| Resumen | — | Caja «Cómo leer este simulador» |

Nota de la sesión: un pedido previo referido a la sesión 09A (capacidad de línea, evisceración, 24 h, RFQ) se descartó a pedido del usuario antes de publicarse; ese trabajo ya está en `main` (PR #10) y este simulador no lo incorpora en v0.1.
