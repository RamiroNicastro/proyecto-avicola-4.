# Modelo de ingresos — demanda, producción vendible, mix, canales y precios

**Fecha:** 2026-10-04 · Código: `productos_balance()`, `_lineas_contables()`, bloque "producción, ventas, inventario" de `simular()` en [`modelo_financiero.py`](modelo_financiero.py) · Precios: [`base_precios_venta.csv`](base_precios_venta.csv)

## 1. Demanda: seis categorías que no se suman

Usa el marco de [`02_clientes_demanda/modelo_demanda.md`](../02_clientes_demanda/modelo_demanda.md) §1 (A/B/C/D). Correspondencia (SUP-19-05):

| Categoría del financiero | Equivale en 02 | Evidencia mínima | ¿Vende en MODO EVIDENCIA? | ¿Vende en MODO ESCENARIO? |
|---|---|---|---|---|
| `DOCUMENTADA` | A (historial propio) | Registro de ventas propio | Sí | Sí |
| `ASEGURADA` | A (contrato, OC, carta de intención con volumen y precio) | Documento firmado | Sí | Sí |
| `NEGOCIADA` | B | Minuta con decisor, piloto | No | Sí, × α (`alfa_negociada`, DEC-014); sin α no cuenta |
| `INTERESADA` | entre B y C | Interés expresado sin negociación | No | Sí, si el usuario la incluye |
| `POTENCIAL` | C / D | Cliente identificado o mercado | No | Sí, si el usuario la incluye |
| `ESCENARIO` | — | Ninguna: hipótesis del usuario | No | Sí |

- Las líneas se reportan **separadas por categoría**. El motor nunca arma un "total A+B+C+D" para decidir.
- **Los ~90 supermercados no son demanda**: los escenarios `RED-*` de 02 son `SUPUESTO` y "no sumables"; en modo evidencia no hay ninguna línea (test E08). Hoy la demanda A+B documentada es ≈ 0 y no está cuantificada (la carnicería familiar es A sin cuantificar: DPV-004).
- Las plantillas de escenario referencian `ESC-CON` / `ESC-BAS` / `ESC-EXP` de 02 (kg/día calendario por canal), pero **sin mix por producto** no generan ventas (DPV-037).

**Unidades aceptadas** (`convertir_demanda()`, test F10): `kg/dia`, `t/dia`, `t/mes`, `t/anio`, `kg/mes`, `kg/anio` (día **calendario**, convención de 02) y `kg/dia_operativo` (con días operativos declarados). Internamente: kg por mes.

## 2. Producción vendible

```
capacidad_aves_mes   = escala (aves/día operativo, capacidad operativa de 23) × días operativos ÷ 12
aves_disponibles     = Σ etapas Δescala × días ÷ 12 × u_técnica(etapa)
aves_requeridas      = máx_producto (demanda_kg − inventario_kg) ÷ (kg_por_ave × (1 − merma))   ← parte limitante
aves_faenadas        = mín(aves_disponibles, aves_requeridas)
producción_kg(p)     = aves_faenadas × kg_por_ave(p) × (1 − merma)
ventas_kg(línea)     ≤ mín(producción + inventario, demanda)
```

- **Parte limitante** (mismo criterio que 23, `aves_por_mix`): se faenan las aves que necesita el producto más exigido; las demás partes generan **excedente**.
- **Inventario** (FIFO por producto): el excedente puede guardarse hasta `inventario_max_meses` meses; por defecto **0** (SUP-19-16): lo no vendido en el mes se informa como `kg_excedente_sin_venta` y **no** se monetiza. El inventario desplaza ventas entre meses pero nunca crea producto (tests F03, F03b; mutación M16).
- **Asignación entre canales:** por `prioridad` de la línea; prorrata dentro de la misma prioridad; las líneas `toma_todo` (p. ej. un comprador de subproductos) reciben solo lo que sobra (SUP-19-17).
- Un producto con 0 kg/ave en la ruta elegida no se produce: su demanda no se atiende y se anota.

## 3. Productos y mix (balance 04, sin copiar fórmulas)

Los kg por ave salen de `mb.balance()` agrupados con `ITEMS` de 23 (una sola agrupación del balance). La función reproduce exactamente `me.kg_por_ave()` (test F09). Peso de referencia 2,9 kg (único que publican 03/14B). Ejemplo, configuración B (trozado), kg **comerciales** por ave (masa biológica + agua retenida; modelo físico **sin** ensayo en planta, DPV-060):

| Producto | kg/ave | Categoría de ingreso |
|---|---|---|
| Pechuga con hueso | 0,8171 | PRODUCTO_PRINCIPAL |
| Pata-muslo | 0,6579 | PRODUCTO_PRINCIPAL |
| Alas | 0,2165 | OTROS |
| Carcasa-esqueleto (ruta venta) | 0,4096 | OTROS |
| CMS (ruta CMS) | 0 en esta ruta | OTROS |
| Menudencias (hígado, corazón, molleja) | 0,1091 | MENUDENCIAS |
| Cuello | 0,0746 | MENUDENCIAS |
| Garras (grado A + segunda) | 0,1011 | PATAS_GARRAS |
| Recortes y piel | 0,0106 | OTROS |
| Sangre, plumas, vísceras, cabeza, otros C | 0,0838 / 0,2413 / 0,1305 / 0,0725 / 0,0053 | SUBPRODUCTOS |
| Harinas de rendering propio | 0 (o PENDIENTE si se activa: DPV-065) | RENDERING |

**Alternativas mutuamente excluyentes** (test F05; mutación M11):

| Material | Opción 1 | Opción 2 | Cómo se garantiza |
|---|---|---|---|
| Carcasa-esqueleto, cuello, hueso de pechuga, piel | venta | CMS / rendering | Ruta única del balance 04 (`rutas`); la otra queda en 0 |
| Masa clase C (sangre, plumas, vísceras, cabeza, huesos) | venta cruda | rendering propio | `destino_c`: con rendering, los C crudos valen 0 kg y las harinas quedan PENDIENTES |
| `cms_alternativa_no_sumable` de 23 | — | — | Nunca se usa |

Además, `validar_entrada()` rechaza cualquier conjunto de productos cuya masa supere peso vivo + agua incorporada (test F04).

**Arquitectura y propiedad del producto:** en C0 (faena a façon) el destino y la propiedad de los subproductos dependen del contrato (FAE-FACON-SUB): sus kg quedan **PENDIENTES**. En CF el rendering es FUTURO: en la etapa inicial los C se venden crudos (SUP-19-21).

## 4. Precios de venta

[`base_precios_venta.csv`](base_precios_venta.csv): `ID_PRECIO, PRODUCTO, CANAL, MERCADO, PRESENTACION, UNIDAD, PRECIO, MONEDA, FECHA, IVA, CONDICION_COMERCIAL, NIVEL_EVIDENCIA, FUENTE, ESTADO, OBSERVACIONES` (+ `TC_USADO, TIPO_TC, FECHA_TC, DPV`).

| Estado | Filas | Uso |
|---|---|---|
| `PENDIENTE` (precio vacío) | 42 combinaciones producto × canal × mercado | Ninguno. Vacío ≠ 0 (test E10) |
| `REFERENCIA_E4_NO_USABLE` | 2: mayorista eviscerado ARS (FTE-004) y FOB promedio país (FTE-032), ambos `[PVDP]` | Solo traza; el motor nunca las usa |
| `CON_PRECIO` | 0 | Requiere precio > 0, nivel, fuente y TC si no es USD |

Precio **constante real** o **serie por año** (`{"tipo": "SERIE", "base": "REAL", "por_anio": {...}}`); sin crecimiento automático; una serie incompleta es faltante (test N21).

## 5. Canales y condiciones comerciales

Canales: `supermercados`, `mayoristas`, `carnicerias_pollerias`, `gastronomia`, `industria`, `exportacion`, `otros`. Cada canal declara (todo PENDIENTE hoy, DPV-039 ampliado a todos los canales: DPV-19-02):

| Campo | Efecto |
|---|---|
| `pct_descuentos`, `pct_bonificaciones`, `pct_devoluciones`, `pct_comisiones` | Deducciones de la venta bruta |
| `costo_logistico_usd_kg` | Costo comercial del canal **adicional** al OPEX logístico de 20 (fees de CD, entrega específica); antes del EBITDA. 0 solo si se declara |
| `dias_cobro` | Cuentas por cobrar (0 = contado; no se supone que el supermercado pague contado) |

No se asumen porcentajes: un canal con un campo vacío deja el ingreso neto como NO CALCULABLE.

## 6. Ingresos

```
VENTA BRUTA            = Σ kg vendidos × precio
− DESCUENTOS − BONIFICACIONES − DEVOLUCIONES − COMISIONES − DERECHOS DE EXPORTACIÓN
= INGRESO NETO                                              (test I01)
```

Separados por categoría: `VENTA_PRODUCTO_PRINCIPAL`, `VENTA_MENUDENCIAS`, `VENTA_PATAS_GARRAS`, `VENTA_SUBPRODUCTOS`, `VENTA_RENDERING`, `VENTA_OTROS`. Los subproductos **no se netean** contra costos: si un subproducto tiene costo de retiro, va al OPEX (DPV-072); si tiene precio, a ingresos (DPV-19-11).

## 7. Exportación (arquitectura preparada, sin valores)

Una línea con `mercado ≠ INTERNO` exige además, en el canal `exportacion`: `pct_derechos_exportacion` (deducción sobre FOB; DPV-015; **ubicación única**: no se carga en el módulo de impuestos ni en otro canal, test X01), `costo_exportacion_usd_kg` (logística a puerto, despacho, certificación, puerto, contenedor, seguro y, si aplica, halal; DPV-026, DPV-145) e `incoterm` (FOB / CIF; con CIF el flete y el seguro van en el costo). Sin débito de IVA. El mercado se identifica por destino y debe respetar las categorías A–D de la regla 17 (DPV-024). Corte de exportación: stress `corte_exportacion_desde_mes`. **No** se desarrolla halal ni se carga ningún precio FOB.
