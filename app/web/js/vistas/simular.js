// SIMULAR (modo simple, #4–#17): asistente guiado + resultado en tarjetas con lenguaje simple.
import { api } from "../api.js";
import { E, editar, pedir, alCambiar } from "../estado.js";
import { h, etq, etqEstadoDato, fmt, tarjetas, alertas, disclaimer, cargando, errorBox, bannerUniverso, campo, numOrNull,
  modal, descargar, semaforo, leyendaSemaforo, tabla, toast } from "../ui.js";
import { barras, lineas } from "../graficos.js";

const PASOS = [["objetivo", "1 · Objetivo"], ["capital", "2 · Capital"], ["demanda", "3 · Demanda"], ["precios", "4 · Precios"],
  ["arquitectura", "5 · Arquitectura"], ["escala", "6 · Escala"], ["restricciones", "7 · Restricciones"]];
let pasoAct = "objetivo";
let ultimoResultado = null;

const S = () => E.escenario.simple;
const set = (fn) => editar((e) => fn(e.simple, e));

function opcion(sel, titulo, desc, onclick, attrs = {}) {
  return h("button", { class: "opcion" + (sel ? " sel" : ""), onclick, "aria-pressed": sel ? "true" : "false", ...attrs }, h("span", { class: "t" }, titulo),
    desc ? h("span", { class: "d" }, desc) : null);
}

// ---------- pasos ----------
function pasoObjetivo(redibujar) {
  const obj = E.catalogo.objetivos_simples;
  const nombres = { GANAR_MAS: "Ganar más", INVERTIR_MENOS: "Invertir menos", RECUPERAR_RAPIDO: "Recuperar rápido", REDUCIR_RIESGO: "Reducir riesgo",
    CRECER: "Crecer", BALANCEADO: "Balanceado" };
  const pesos = E.escenario.experto.analisis || {};
  return h("div", {}, h("p", {}, "¿Qué es lo más importante para vos? Se traduce a un objetivo del optimizador (se muestra cuál)."),
    h("div", { class: "opciones" }, Object.entries(obj).map(([k, v]) => opcion(S().objetivo === k, nombres[k], `${v.objetivo}: ${v.texto}`,
      () => { set((s) => { s.objetivo = k; }); redibujar(); }, { "data-objetivo": k }))),
    S().objetivo === "BALANCEADO" ? h("div", { class: "panel" }, h("h3", {}, "Pesos del objetivo balanceado (visibles, los define usted)"),
      h("div", { class: "campos" }, E.catalogo.componentes_balanceado.map((c) => campo(c, h("input", { type: "number", min: 0, step: "any", value: pesos[`balanceado.peso.${c}`] ?? "",
        "data-peso": c, onchange: (e) => editar((x) => { const v = numOrNull(e.target.value); if (v === null) delete x.experto.analisis[`balanceado.peso.${c}`]; else x.experto.analisis[`balanceado.peso.${c}`] = v; }) })))),
      h("div", { class: "fila-btn" }, h("button", { class: "btn", onclick: () => { editar((x) => { E.catalogo.componentes_balanceado.forEach((c) => { x.experto.analisis[`balanceado.peso.${c}`] = 1; }); }); redibujar(); } },
        "Usar pesos IGUALES (SUP-219: supuesto explícito)")),
      h("p", { class: "mut peq" }, "Sin pesos, el balanceado queda PESOS_NO_DEFINIDOS: la app no inventa pesos.")) : null);
}

function pasoCapital(redibujar) {
  const c = S().capital;
  const upd = (k, v) => set((s) => { s.capital[k] = v; });
  return h("div", {}, h("p", {}, "¿Cuánto capital tenés disponible? Si no lo sabés, no se usa restricción de capital (USD 2 M NO es un valor por defecto)."),
    h("div", { class: "opciones" }, opcion(c.no_se, "No sé", "Sin restricción de capital", () => { upd("no_se", true); redibujar(); }, { "data-capital": "no_se" }),
      opcion(!c.no_se, "Lo sé", "Cargar un monto", () => { upd("no_se", false); redibujar(); }, { "data-capital": "valor" })),
    c.no_se ? null : h("div", { class: "campos", style: { marginTop: "10px" } },
      campo("Capital disponible", h("input", { type: "number", step: "any", min: 0, value: c.valor ?? "", "data-campo": "capital", onchange: (e) => upd("valor", numOrNull(e.target.value)) })),
      campo("Moneda", h("select", { onchange: (e) => { upd("moneda", e.target.value); redibujar(); } }, ["USD", "ARS"].map((m) => h("option", { selected: c.moneda === m }, m)))),
      campo("Se compara con", h("select", { onchange: (e) => upd("metrica", e.target.value) },
        [["PICO_FONDOS", "Pico de fondos (default del motor)"], ["FONDOS_INICIALES", "Fondos iniciales"]].map(([v, t]) => h("option", { value: v, selected: c.metrica === v }, t)))),
      c.moneda === "ARS" ? [
        campo("Tipo de cambio (ARS/USD)", h("input", { type: "number", step: "any", value: c.tc ?? "", onchange: (e) => upd("tc", numOrNull(e.target.value)) })),
        campo("Tipo de TC", h("select", { onchange: (e) => upd("tipo_tc", e.target.value) }, ["", "oficial", "MEP", "otro"].map((t) => h("option", { selected: c.tipo_tc === t, value: t }, t || "—")))),
        campo("Fecha del TC", h("input", { type: "date", value: c.fecha_tc ?? "", onchange: (e) => upd("fecha_tc", e.target.value) })),
        campo("Fuente del TC", h("input", { value: c.fuente_tc ?? "", onchange: (e) => upd("fuente_tc", e.target.value) }))] : null),
    c.moneda === "ARS" && !c.no_se ? h("p", { class: "mut peq" }, "Regla 2 del proyecto: un valor en ARS exige TC, tipo y fecha. La conversión no es una nueva cotización.") : null);
}

function filaDemanda(l, i, redibujar) {
  const prods = E.catalogo.productos;
  const upd = (k, v) => set((s) => { s.demanda[i][k] = v; });
  const kg = prods.find((p) => p.producto === l.producto)?.kg_ave;
  return h("tr", { "data-linea-demanda": i },
    h("td", {}, h("select", { onchange: (e) => { upd("producto", e.target.value); redibujar(); } }, prods.map((p) => h("option", { value: p.producto, selected: p.producto === l.producto },
      `${p.producto}${p.kg_ave === 0 ? " (0 kg/ave en conf. B)" : ""}`))), kg === 0 ? h("div", { class: "peq mut" }, "La configuración de producto del balance (B, trozado) no produce este producto.") : null),
    h("td", {}, h("select", { onchange: (e) => upd("canal", e.target.value) }, E.catalogo.canales.map((c) => h("option", { selected: c === l.canal }, c)))),
    h("td", {}, h("select", { "data-categoria": "", onchange: (e) => upd("categoria", e.target.value) }, E.catalogo.categorias_demanda.map((c) => h("option", { selected: c === l.categoria }, c)))),
    h("td", {}, h("input", { type: "number", step: "any", min: 0, value: l.valor ?? "", style: { width: "90px" }, "data-volumen": "", onchange: (e) => upd("valor", numOrNull(e.target.value)) })),
    h("td", {}, h("select", { onchange: (e) => upd("unidad", e.target.value) }, E.catalogo.unidades_demanda.map((u) => h("option", { selected: u === l.unidad }, u)))),
    h("td", {}, h("input", { type: "checkbox", checked: !!l.toma_todo, title: "Canal de liquidación: demanda supuesta ilimitada", onchange: (e) => upd("toma_todo", e.target.checked) })),
    h("td", {}, h("input", { value: l.fuente ?? "", placeholder: "fuente", onchange: (e) => upd("fuente", e.target.value) })),
    h("td", {}, h("button", { class: "btn", title: "Quitar", onclick: () => { set((s) => { s.demanda.splice(i, 1); }); redibujar(); } }, "✕")));
}

function pasoDemanda(redibujar) {
  const d = S().demanda;
  const tot = {};
  d.forEach((l) => { tot[l.categoria] = (tot[l.categoria] || 0) + 1; });
  return h("div", {}, h("p", {}, h("b", {}, "¿Cuánto tenés realmente vendido o respaldado?")),
    h("div", { class: "cita" }, "Que un cliente pueda comprar no significa que la demanda esté asegurada. ASEGURADA y DOCUMENTADA requieren respaldo (contrato, orden, carta de intención con volumen); ",
      "POTENCIAL y ESCENARIO son hipótesis. La app NO convierte potencial en asegurada; los ~90 supermercados no son demanda por sí mismos."),
    h("div", { class: "tabla-env", style: { marginTop: "10px" } }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Producto", "Canal", "Categoría", "Volumen", "Unidad", "Toma todo", "Fuente", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, d.map((l, i) => filaDemanda(l, i, redibujar))))),
    h("div", { class: "fila-btn" }, h("button", { class: "btn", "data-agregar-demanda": "", onclick: () => {
      set((s) => s.demanda.push({ producto: "pechuga", canal: "supermercados", mercado: "INTERNO", categoria: "POTENCIAL", valor: null, unidad: "t/dia", fuente: "", estado: "ESCENARIO" })); redibujar();
    } }, "+ Agregar línea de demanda"), h("span", { class: "mut peq" }, "Unidades: kg/día y t/día son días CALENDARIO; t/mes, t/año."),
    Object.entries(tot).map(([k, n]) => h("span", { class: "chip" }, `${k}: ${n} línea(s)`))),
    h("details", {}, h("summary", {}, "¿Qué categorías se venden en la simulación?"),
      h("div", { class: "opciones" }, E.catalogo.categorias_demanda.map((c) => h("label", { class: "chip" }, h("input", { type: "checkbox", checked: S().categorias_vendibles.includes(c),
        onchange: (e) => set((s) => { s.categorias_vendibles = e.target.checked ? [...new Set([...s.categorias_vendibles, c])] : s.categorias_vendibles.filter((x) => x !== c); }) }), " ", c))),
      campo("Fracción de la demanda NEGOCIADA que se cuenta (alfa)", h("input", { type: "number", step: "any", min: 0, max: 1, value: S().alfa_negociada ?? "", onchange: (e) => set((s) => { s.alfa_negociada = numOrNull(e.target.value); }) }),
        "Sin alfa, la demanda NEGOCIADA no se vende (no se asume 100 %)."),
      h("p", { class: "mut peq" }, "El respaldo comercial de cada alternativa se calcula solo con DOCUMENTADA / ASEGURADA.")));
}

function filaPrecio(p, i, lista, redibujar) {
  const upd = (k, v) => set((s) => { s[lista][i][k] = v; });
  const esVenta = lista === "precios_venta";
  return h("tr", { "data-linea-precio": `${lista}-${i}` },
    esVenta ? h("td", {}, h("select", { onchange: (e) => upd("producto", e.target.value) }, E.catalogo.productos.map((x) => h("option", { selected: x.producto === p.producto }, x.producto))),
      h("select", { onchange: (e) => upd("canal", e.target.value) }, E.catalogo.canales.map((c) => h("option", { selected: c === p.canal }, c))))
      : h("td", {}, E.catalogo.costos_unitarios[p.concepto]?.texto || p.concepto),
    h("td", {}, h("input", { type: "number", step: "any", value: p.valor ?? "", style: { width: "100px" }, "data-valor-precio": "", disabled: p.estado === "NO_SE",
      onchange: (e) => upd("valor", numOrNull(e.target.value)) })),
    h("td", {}, h("select", { onchange: (e) => { upd("moneda", e.target.value); redibujar(); } }, ["USD", "ARS"].map((m) => h("option", { selected: (p.moneda || "USD") === m }, m))),
      p.moneda === "ARS" ? h("div", { class: "campos" }, h("input", { type: "number", placeholder: "TC ARS/USD", value: p.tc ?? "", onchange: (e) => upd("tc", numOrNull(e.target.value)) }),
        h("select", { onchange: (e) => upd("tipo_tc", e.target.value) }, ["", "oficial", "MEP", "otro"].map((t) => h("option", { value: t, selected: p.tipo_tc === t }, t || "tipo TC"))),
        h("input", { type: "date", value: p.fecha_tc ?? "", onchange: (e) => upd("fecha_tc", e.target.value) })) : null),
    h("td", {}, esVenta ? "por kg" : E.catalogo.costos_unitarios[p.concepto]?.unidad),
    h("td", {}, h("input", { value: p.fuente ?? "", placeholder: "fuente (proveedor, fecha…)", onchange: (e) => upd("fuente", e.target.value) })),
    h("td", {}, h("select", { "data-estado-dato": "", onchange: (e) => { upd("estado", e.target.value); redibujar(); } }, ["VALIDADO", "COTIZACION", "ESCENARIO", "NO_SE"].map((x) => h("option", { selected: p.estado === x, value: x },
      { VALIDADO: "Validado", COTIZACION: "Cotización", ESCENARIO: "Escenario", NO_SE: "No sé" }[x]))), " ", etqEstadoDato(p.estado),
      p.estado === "ESCENARIO" ? h("div", { class: "peq mut" }, "marcado como simulación") : null),
    h("td", {}, h("button", { class: "btn", onclick: () => { set((s) => { s[lista].splice(i, 1); }); redibujar(); } }, "✕")));
}

function pasoPrecios(redibujar) {
  const pv = S().precios_venta, cu = S().costos_unitarios;
  const faltan = S().demanda.filter((l) => !pv.some((p) => p.producto === l.producto && p.canal === l.canal));
  return h("div", {}, h("p", {}, "Precios principales. Cada valor lleva UNIDAD, FUENTE y ESTADO. «No sé» deja el precio PENDIENTE (nunca 0)."),
    h("h3", {}, "Precios de venta (USD/kg; ARS con TC)"),
    h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Producto · canal", "Valor", "Moneda", "Unidad", "Fuente", "Estado", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, pv.map((p, i) => filaPrecio(p, i, "precios_venta", redibujar))))),
    h("div", { class: "fila-btn" },
      faltan.length ? h("button", { class: "btn", "data-precios-desde-demanda": "", onclick: () => { set((s) => faltan.forEach((l) => s.precios_venta.push({ producto: l.producto, canal: l.canal, mercado: l.mercado || "INTERNO", valor: null, moneda: "USD", unidad: "USD/kg", fuente: "", estado: "NO_SE" }))); redibujar(); } },
        `+ Agregar precios para las ${faltan.length} líneas de demanda sin precio`) : null,
      h("button", { class: "btn", onclick: () => { set((s) => s.precios_venta.push({ producto: "pechuga", canal: "supermercados", mercado: "INTERNO", valor: null, moneda: "USD", unidad: "USD/kg", fuente: "", estado: "NO_SE" })); redibujar(); } }, "+ Precio")),
    h("p", { class: "mut peq" }, "El balance de masa (04) en la configuración de producto B produce cortes; el pollo entero tiene 0 kg/ave: su precio no se usa."),
    h("h3", {}, "Costos principales (precio unitario)"),
    h("p", { class: "mut peq" }, "Se costean con la CANTIDAD que calcula el módulo 20 para cada alternativa (cantidad × precio). Si la arquitectura no usa ese concepto, NO APLICA."),
    h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Concepto", "Valor", "Moneda", "Unidad", "Fuente", "Estado", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, cu.map((p, i) => filaPrecio(p, i, "costos_unitarios", redibujar))))),
    h("div", { class: "fila-btn" }, Object.keys(E.catalogo.costos_unitarios).filter((k) => !cu.some((c) => c.concepto === k)).map((k) =>
      h("button", { class: "btn", onclick: () => { set((s) => s.costos_unitarios.push({ concepto: k, valor: null, moneda: "USD", fuente: "", estado: "NO_SE" })); redibujar(); } }, "+ " + E.catalogo.costos_unitarios[k].texto))),
    h("p", { class: "mut peq" }, "Otros costos (OPEX por módulo), CAPEX, impuestos, tasas y financiamiento: MODO EXPERTO."));
}

function explicarArquitecturas() {
  modal(h("div", {}, h("h2", {}, "¿Qué significa cada configuración?"),
    E.catalogo.arquitecturas.filter((a) => a.tipo === "CONFIGURACION_BASE").map((a) => h("div", { class: "panel" }, h("b", {}, `${a.id} — ${a.titulo}`), h("p", {}, a.explicacion),
      h("details", {}, h("summary", {}, "Definición técnica (arquitecturas_maestras / mapa)"), h("ul", { class: "peq" },
        ["faena", "granjas", "pollito", "alimento", "flota", "frio", "subproductos", "rendering"].map((k) => h("li", {}, `${k}: ${a[k]}`)), h("li", {}, "Estado CAPEX: " + a.estado_capex), h("li", {}, "Estado OPEX: " + a.estado_opex))))),
    h("p", { class: "mut" }, "Ninguna configuración es una recomendación. La integración vertical total no se presume conveniente.")));
}

function pasoArquitectura(redibujar) {
  const a = S().arquitectura;
  return h("div", {}, h("div", { class: "opciones" },
    opcion(a.modo === "AUTO", "Automática", "El optimizador evalúa todas las alternativas válidas del mapa", () => { set((s) => { s.arquitectura = { modo: "AUTO", configuracion: null, variante: null }; }); redibujar(); }, { "data-arquitectura": "AUTO" }),
    opcion(a.modo === "MANUAL", "Quiero probar una configuración", "Elegís C0, C1, C2, C3 o CF", () => { set((s) => { s.arquitectura.modo = "MANUAL"; s.arquitectura.configuracion ||= "C1"; }); redibujar(); }, { "data-arquitectura": "MANUAL" })),
    a.modo === "MANUAL" ? h("div", { class: "opciones", style: { marginTop: "10px" } }, E.catalogo.arquitecturas.filter((x) => x.tipo === "CONFIGURACION_BASE").map((x) =>
      opcion(a.configuracion === x.id, x.id, x.titulo, () => { set((s) => { s.arquitectura.configuracion = x.id; }); redibujar(); }, { "data-config": x.id }))) : null,
    h("div", { class: "fila-btn" }, h("button", { class: "btn-link", onclick: explicarArquitecturas, "data-que-significa": "" }, "¿Qué significa esto?")));
}

function pasoEscala(redibujar) {
  const e = S().escala, esc = E.catalogo.escalas;
  const val = e.modo === "VALOR" ? e.valor : null;
  return h("div", {}, h("p", {}, "Escala de faena en aves por día OPERATIVO. Fuera del rango evaluable por el motor (", fmt(esc.rango_min, "ent"), "–", fmt(esc.rango_max, "ent"), ") no se ofrece."),
    h("div", { class: "opciones" }, opcion(e.modo === "AUTO", "AUTO", "El optimizador prueba las escalas de referencia", () => { set((s) => { s.escala = { modo: "AUTO", valor: null }; }); redibujar(); }, { "data-escala": "AUTO" }),
      esc.referencia.map((v) => opcion(val === v, fmt(v, "ent"), "aves/día", () => { set((s) => { s.escala = { modo: "VALOR", valor: v }; }); redibujar(); }, { "data-escala": v }))),
    h("div", { class: "campos", style: { marginTop: "10px" } }, campo("Otra escala intermedia (el motor de CAPEX la admite)", h("input", { type: "number", min: esc.rango_min, max: esc.rango_max, step: 100,
      value: val && !esc.referencia.includes(val) ? val : "", onchange: (ev) => { const v = numOrNull(ev.target.value); if (v === null) return;
        if (v < esc.rango_min || v > esc.rango_max) { toast(`Fuera del rango evaluable (${esc.rango_min}–${esc.rango_max}).`, 5000); return; }
        set((s) => { s.escala = { modo: "VALOR", valor: Math.round(v) }; }); redibujar(); } }))),
    h("p", { class: "mut peq" }, esc.nota));
}

function pasoRestricciones(redibujar) {
  const r = S().restricciones || {};
  const def = [["FONDOS_INICIALES", "Máximo capital (fondos iniciales, USD)"], ["PAYBACK", "Máximo payback (años)"], ["VAN", "Mínimo VAN (USD)"], ["TIR", "Mínima TIR (fracción, 0,15 = 15 %)"],
    ["DSCR", "Mínimo DSCR (veces)"], ["RIESGO", "Máximo score ordinal de riesgo (0–1; requiere pesos de riesgo)"], ["SUPERFICIE_TERRENO", "Máximo terreno (m²)"],
    ["DEMANDA_MAXIMA_T_DIA", "Demanda disponible a evaluar (t/día; consulta del motor)"]];
  return h("div", {}, h("p", {}, "Todas opcionales. Se aplican como restricciones obligatorias (HARD) del optimizador. Vacío = sin restricción."),
    h("div", { class: "campos" }, def.map(([k, t]) => campo(t, h("input", { type: "number", step: "any", value: r[k] ?? "", "data-restriccion": k,
      onchange: (e) => set((s) => { s.restricciones = s.restricciones || {}; const v = numOrNull(e.target.value); if (v === null) delete s.restricciones[k]; else s.restricciones[k] = v; }) }))),
      campo("Horizonte de evaluación (años)", h("input", { type: "number", min: 1, step: 1, value: S().horizonte_anios ?? "", "data-campo": "horizonte",
        onchange: (e) => set((s) => { s.horizonte_anios = numOrNull(e.target.value); }) }), "DEC-007 abierta: 10 / 15 / 20 como escenarios.")));
}

const RENDER_PASO = { objetivo: pasoObjetivo, capital: pasoCapital, demanda: pasoDemanda, precios: pasoPrecios, arquitectura: pasoArquitectura, escala: pasoEscala, restricciones: pasoRestricciones };

// ---------- resultado ----------
function graficosResultado(det) {
  const se = det?.series;
  if (!se) return h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, "Sin línea de tiempo"), "Falta horizonte o cronograma: no hay series para graficar."));
  const per = se.periodos, S_ = se.series;
  const acum = []; let a = 0;
  (S_.fcff || S_.fcff_pre || []).forEach((v) => { a = v === null ? a : a + v; acum.push(S_.fcff || S_.fcff_pre ? a : null); });
  const nopub = Object.entries(se.no_publicadas || {});
  return h("div", { class: "rejilla rejilla-2" },
    h("div", { class: "panel" }, h("h3", {}, "Ingresos, OPEX y EBITDA (por año)"), barras([{ nombre: "Ingreso neto", valores: S_.ingreso_neto }, { nombre: "OPEX", valores: S_.opex_total }, { nombre: "EBITDA", valores: S_.ebitda }], per)),
    h("div", { class: "panel" }, h("h3", {}, "Flujo de caja del proyecto (FCFF) y acumulado"), barras([{ nombre: "FCFF", valores: S_.fcff || S_.fcff_pre }], per),
      (S_.fcff || S_.fcff_pre) ? lineas([{ nombre: "Acumulado (suma de FCFF del motor; su mínimo = pico de fondos)", valores: acum, color: "var(--c4)" }], per) : null),
    h("div", { class: "panel" }, h("h3", {}, "Utilización"), lineas([{ nombre: "Efectiva", valores: S_.u_efectiva }, { nombre: "Técnica", valores: S_.u_tecnica }, { nombre: "Comercial requerida", valores: S_.u_comercial }], per, { formato: "pct" })),
    h("div", { class: "panel" }, h("h3", {}, "CAPEX y capital de trabajo"), barras([{ nombre: "CAPEX", valores: S_.capex_total }, { nombre: "Δ capital de trabajo", valores: S_.delta_ct }], per),
      nopub.length ? h("details", {}, h("summary", {}, "Series no publicadas"), nopub.map(([k, v]) => h("div", { class: "peq mut" }, `${k}: ${v}`))) : null));
}

function panelPorQue(r) {
  const p = r.por_que || {};
  return h("div", { class: "panel", "data-por-que": "" }, h("h2", {}, "¿Por qué me da este resultado?"),
    h("h3", {}, "Principales drivers (amplitud del VAN en la sensibilidad)"),
    p.drivers?.length ? tabla(p.drivers, [{ k: "variable", t: "Variable" }, { k: "swing_van", t: "Amplitud VAN", f: "usd" }, { k: "min", t: "VAN mín.", f: "usd" }, { k: "max", t: "VAN máx.", f: "usd" }], { buscar: false, csv: false })
      : h("p", { class: "mut" }, "No calculado: el VAN no es publicable o no hubo sensibilidad."),
    h("h3", {}, "Restricciones"), p.restricciones?.length ? tabla(p.restricciones, [{ k: "NOMBRE", t: "Restricción" }, { k: "TIPO", t: "Tipo" }, { k: "VALOR", t: "Límite", f: "num" }, { k: "VALOR_ALTERNATIVA", t: "Valor", f: "num" }, { k: "ESTADO", t: "Estado" }], { buscar: false, csv: false })
      : h("p", { class: "mut" }, "Sin restricciones declaradas."),
    h("h3", {}, "Qué cambiaría la decisión"), p.que_cambiaria?.length ? h("ul", {}, p.que_cambiaria.map((x) => h("li", {}, x))) : h("p", { class: "mut" }, "—"),
    p.segunda ? h("p", {}, "Segunda mejor alternativa del escenario: ", h("b", {}, p.segunda)) : null,
    h("h3", {}, "Sensibilidades evaluadas"), p.sensibilidades?.length ? tabla(p.sensibilidades, [{ k: "variable", t: "Variable" }, { k: "shock", t: "Shock", f: "num" }, { k: "VAN", t: "VAN", f: "usd", nulo: "no calculable" }, { k: "DELTA_VAN", t: "Δ VAN", f: "usd" }, { k: "estado", t: "Estado" }], { alto: "260px", nombre: "sensibilidades" }) : h("p", { class: "mut" }, "—"),
    h("details", {}, h("summary", {}, `Datos de ESCENARIO usados (${p.datos_escenario?.length || 0})`), tabla(p.datos_escenario || [], [{ k: "variable", t: "Variable" }, { k: "valor", t: "Valor" }, { k: "unidad", t: "Unidad" }, { k: "origen", t: "Origen", r: () => etq("ESCENARIO") }, { k: "obs", t: "Obs." }], { alto: "300px", nombre: "datos_escenario" })),
    h("details", {}, h("summary", {}, `Datos del motor (supuestos / evidencia) (${p.datos_motor?.length || 0})`), tabla(p.datos_motor || [], [{ k: "variable", t: "Variable" }, { k: "valor", t: "Valor" }, { k: "unidad", t: "Unidad" }, { k: "origen", t: "Origen" }, { k: "archivo", t: "Archivo" }, { k: "obs", t: "Obs." }], { alto: "300px", nombre: "datos_motor" })),
    h("details", {}, h("summary", {}, `Datos PENDIENTES (${p.datos_pendientes?.length || 0})`), tabla(p.datos_pendientes || [], [{ k: "variable", t: "Variable" }, { k: "unidad", t: "Unidad" }, { k: "obs", t: "Qué falta" }], { alto: "300px", nombre: "datos_pendientes" })),
    h("p", { class: "mut peq" }, p.nota));
}

function bloqueNoInvertir(r) {
  const ni = r.no_invertir || {};
  return h("div", { class: "panel", "data-no-invertir": ni.estado_app || "" }, h("h2", {}, ni.titulo),
    h("p", {}, ni.texto), ni.reglas?.length ? h("div", {}, h("h3", {}, "Reglas del motor que se cumplen"), h("ul", {}, ni.reglas.map((x) => h("li", {}, x)))) : null,
    ni.por_que ? h("p", { class: "mut" }, "Detalle: ", ni.por_que) : null,
    ni.por_que_no_invertir_podria_ganar ? h("p", { class: "mut" }, ni.por_que_no_invertir_podria_ganar) : null);
}

export function vistaResultado(r) {
  const cont = h("div", { "data-resultado": r.resultado });
  cont.append(bannerUniverso(r), alertas(r.alertas));
  if (r.resultado !== "ALTERNATIVA") {
    cont.append(bloqueNoInvertir(r));
    if (r.optimizacion) cont.append(h("p", { class: "mut" }, `Se evaluaron ${r.optimizacion.n_alternativas} alternativas (${r.optimizacion.n_completas} con datos completos). Objetivo: ${r.optimizacion.objetivo}.`),
      h("div", { class: "fila-btn" }, h("a", { class: "btn", href: "#/optimizar" }, "Ver detalle en OPTIMIZAR"), h("a", { class: "btn", href: "#/validacion" }, "Qué me falta validar")));
    cont.append(disclaimer(r.disclaimer));
    return cont;
  }
  const fj = r.alternativa;
  E.alternativa = fj.id;
  if (r.modo === "AUTOMATICO" && r.optimizacion) cont.append(h("div", { class: "ayuda" }, `Arquitectura AUTOMÁTICA: el optimizador eligió ${fj.id} como mejor alternativa DEL ESCENARIO para el objetivo ${r.optimizacion.objetivo}`,
    r.optimizacion.segunda && r.optimizacion.segunda !== "—" ? ` (segunda: ${r.optimizacion.segunda}).` : "."));
  if (r.detalle?.error_construccion) cont.append(errorBox({ codigo: r.detalle.error_construccion.codigo, message: r.detalle.error_construccion.mensaje }));
  cont.append(h("div", { class: "fila-btn" }, h("span", {}, "Semáforo: "), semaforo(fj.semaforo, E.estado?.semaforo),
    h("button", { class: "btn-link", onclick: () => modal(h("div", {}, h("h2", {}, "Leyenda del semáforo"), leyendaSemaforo(E.estado?.semaforo), h("p", { class: "mut peq" }, "Cortes del optimizador (no son cortes económicos nuevos)."))) }, "leyenda")));
  cont.append(tarjetas(r.tarjetas));
  const qh = r.que_hacer || [];
  cont.append(h("div", { class: "panel", "data-que-hacer": "" }, h("h3", {}, "Qué hacer ahora"), h("ol", {}, qh.map((a) => h("li", {}, a.accion, a.dpv ? h("span", { class: "mut peq" }, ` (${a.dpv})`) : null,
    a.empate ? h("span", { class: "etq etq-info" }, "empate") : null)))));
  const porQue = h("div");
  cont.append(h("div", { class: "fila-btn" },
    h("button", { class: "btn btn-primario", "data-boton-por-que": "", onclick: () => { porQue.firstChild ? porQue.replaceChildren() : porQue.replaceChildren(panelPorQue(r)); } }, "¿Por qué me da este resultado?"),
    h("button", { class: "btn", onclick: () => { E.alternativa = fj.id; location.hash = "#/riesgos"; } }, "¿Qué pasa si…? (riesgos)"),
    h("button", { class: "btn", "data-exportar": "json", onclick: async () => { const j = await api.post("/api/exportar/json", { escenario: E.escenario }); descargar(`escenario_${E.escenario.id}.json`, JSON.stringify(j, null, 1)); } }, "Exportar JSON"),
    h("button", { class: "btn", "data-exportar": "csv", onclick: async () => { try { descargar(`resultado_${E.escenario.id}.csv`, await api.texto("/api/exportar/csv", { escenario: E.escenario, alternativa: fj.id }), "text/csv"); } catch (e) { toast(e.message, 6000); } } }, "Exportar CSV"),
    h("button", { class: "btn", "data-exportar": "resumen", onclick: async () => { try { const t = await api.texto("/api/exportar/resumen", { escenario: E.escenario, alternativa: fj.id });
      const w = window.open(URL.createObjectURL(new Blob([t], { type: "text/html" })), "_blank"); if (!w) descargar(`resumen_${E.escenario.id}.html`, t, "text/html"); } catch (e) { toast(e.message, 6000); } } }, "Resumen imprimible")), porQue);
  cont.append(h("h2", {}, "Gráficos"), graficosResultado(r.detalle));
  cont.append(disclaimer(r.disclaimer));
  return cont;
}

export async function render() {
  const raiz = h("div");
  const resultado = h("div", { id: "resultado-simulacion" });
  function dibujar() {
    const cuerpo = RENDER_PASO[pasoAct](dibujar);
    raiz.replaceChildren(
      h("h1", {}, "Simular un negocio"), h("p", { class: "mut" }, "Modo simple: pocos datos, resultados explicados. El modo experto sigue disponible para todo lo demás."),
      h("div", { class: "pasos" }, PASOS.map(([id, t]) => h("button", { class: "paso" + (id === pasoAct ? " act" : ""), "data-paso": id, onclick: () => { pasoAct = id; dibujar(); } }, t))),
      h("div", { class: "panel" }, h("h2", {}, PASOS.find((p) => p[0] === pasoAct)[1]), cuerpo,
        h("div", { class: "fila-btn" },
          pasoAct !== "objetivo" ? h("button", { class: "btn", onclick: () => { pasoAct = PASOS[PASOS.findIndex((p) => p[0] === pasoAct) - 1][0]; dibujar(); } }, "← Anterior") : null,
          pasoAct !== "restricciones" ? h("button", { class: "btn", "data-siguiente": "", onclick: () => { pasoAct = PASOS[PASOS.findIndex((p) => p[0] === pasoAct) + 1][0]; dibujar(); } }, "Siguiente →") : null,
          h("button", { class: "btn btn-primario btn-grande", "data-simular": "", onclick: correr }, "SIMULAR"))),
      resultado);
  }
  async function correr() {
    resultado.replaceChildren(cargando(S().arquitectura.modo === "AUTO" || S().escala.modo === "AUTO" ? "El motor evalúa todas las alternativas del escenario (puede tardar varios segundos)…" : "Calculando con el motor…"));
    try {
      const r = await pedir("simular", "/api/simular");
      ultimoResultado = r;
      resultado.replaceChildren(h("h1", {}, "Resultado"), vistaResultado(r));
      resultado.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) { resultado.replaceChildren(errorBox(e)); }
  }
  dibujar();
  const off = alCambiar(() => {
    if (!document.body.contains(resultado)) { off(); return; }
    if (resultado.querySelector("[data-resultado]") && !Object.keys(E.res).some((k) => k.startsWith("simular"))) {
      resultado.replaceChildren(h("div", { class: "banner banner-pend", "data-desactualizado": "" }, h("span", { class: "ico" }, "↻"),
        h("div", {}, h("b", {}, "Los inputs cambiaron"), "El resultado anterior ya no corresponde a este escenario. Presioná SIMULAR de nuevo.")));
    }
  });
  const previo = Object.entries(E.res).find(([k]) => k.startsWith("simular"));
  if (previo) resultado.replaceChildren(h("h1", {}, "Resultado"), vistaResultado(previo[1]));
  return raiz;
}
