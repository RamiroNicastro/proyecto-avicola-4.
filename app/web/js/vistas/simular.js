// SIMULAR (modo simple): 5 preguntas guiadas («Paso X de 5»), «Ajustar supuestos» para lo avanzado y un resultado simple
// (una frase + hasta 6 números + acordeones). Todo el cálculo lo hace el motor vía /api/simular.
import { api } from "../api.js";
import { E, editar, pedir, alCambiar } from "../estado.js";
import { h, etq, etqEstadoDato, fmt, tarjetas, alertas, disclaimer, cargando, errorBox, bannerUniverso, campo, numOrNull,
  descargar, semaforo, leyendaSemaforo, tabla, toast, ayuda, porQueFalta, vacio, confirmar, modal } from "../ui.js";
import { barras, lineas, barraProgreso } from "../graficos.js";

const PASOS = [["objetivo", "¿Qué querés lograr?"], ["capital", "¿Cuánto capital querés simular?"], ["demanda", "¿Cuánta demanda querés simular?"],
  ["alternativa", "¿Automático o una alternativa?"], ["precios", "¿Tenés precios o costos propios?"]];
let pasoAct = "objetivo";
let escenarioDelAsistente = null;   // al abrir otro escenario el asistente vuelve al paso 1

const S = () => E.escenario.simple;
const set = (fn) => editar((e) => fn(e.simple, e));

export const NOMBRE_ARQ = { C0: "Arranque asset-light", C1: "Planta de faena propia", C2: "Integración selectiva", C3: "Mayor integración", CF: "Arquitectura futura" };
export const nombreProducto = (p) => String(p || "").replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());
export function nombreAlternativa(fj) {
  if (!fj) return "—";
  const esc = (fj.escalas || []).map((x) => fmt(x, "ent")).join(" → ");
  return `${NOMBRE_ARQ[fj.configuracion] || fj.configuracion} (${fj.configuracion})${fj.variante && fj.variante !== "BASE" ? " · variante" : ""}${esc ? " · " + esc + " aves/día" : ""}`;
}

function opcion(sel, titulo, desc, onclick, attrs = {}, codigo = null) {
  return h("button", { class: "opcion" + (sel ? " sel" : ""), onclick, "aria-pressed": sel ? "true" : "false", ...attrs }, h("span", { class: "t" }, titulo),
    desc ? h("span", { class: "d" }, desc) : null, codigo ? h("span", { class: "codigo-tecnico" }, codigo) : null);
}
const noSeTexto = (t) => h("div", { class: "cita no-se", "data-no-se-explica": "" }, h("b", {}, "Si elegís «No sé»: "), t);

// ---------------------------------------------------------------- paso 1: objetivo (+ pesos BALANCEADO al 100 %)
const OBJ_SIMPLE = {
  GANAR_MAS: ["Ganar más", "Elegir lo que más valor genera."], INVERTIR_MENOS: ["Invertir menos", "Lo que necesita menos plata al inicio."],
  RECUPERAR_RAPIDO: ["Recuperar rápido", "Recuperar la inversión en el menor tiempo."], REDUCIR_RIESGO: ["Reducir riesgo", "Lo que mejor aguanta si las cosas salen mal."],
  CRECER: ["Crecer", "Llegar a la mayor capacidad."], BALANCEADO: ["Balanceado", "Combinar varios criterios con el peso que vos elijas."],
};
export const COMP_NOMBRE = { rentabilidad: "Rentabilidad (que gane más)", capital: "Menor inversión inicial", liquidez: "Menor necesidad de caja (liquidez)",
  robustez: "Robustez (que aguante los imprevistos)", riesgo: "Menor riesgo (puntaje de riesgo)", crecimiento: "Crecimiento (más capacidad)" };
const pesosDe = () => E.escenario.experto.analisis || {};
export const tienePesosRiesgo = () => Object.keys(pesosDe()).some((k) => k.startsWith("riesgo.peso.") && Number(pesosDe()[k]));
export function totalPesos() {
  return (E.catalogo.componentes_balanceado || []).reduce((t, c) => t + (Number(pesosDe()[`balanceado.peso.${c}`]) || 0), 0);
}
// Bloquea la ejecución: BALANCEADO sin pesos (o que no suman 100 %) NO se simula; nunca se convierte en «no invertir».
export function bloqueoPesos() {
  if (S().objetivo !== "BALANCEADO") return null;
  const t = totalPesos();
  if (t === 0) return "Falta definir cuánto pesa cada criterio del objetivo balanceado. Sin pesos no se puede simular (y eso NO significa «no invertir»).";
  if (Math.abs(t - 100) > 0.001) return `Los pesos suman ${fmt(t, "num", 0)} %: tienen que sumar 100 %.`;
  if (Number(pesosDe()["balanceado.peso.riesgo"]) && !tienePesosRiesgo()) return "Le diste peso al riesgo, pero el puntaje de riesgo necesita sus propios pesos (Modo experto). Poné 0 % en riesgo.";
  return null;
}
export function repartirPorIgual(x) {
  const comps = (E.catalogo.componentes_balanceado || []).filter((c) => c !== "riesgo" || tienePesosRiesgo());
  const base = Math.floor(100 / comps.length);
  let resto = 100 - base * comps.length;
  (E.catalogo.componentes_balanceado || []).forEach((c) => { delete x.experto.analisis[`balanceado.peso.${c}`]; });
  comps.forEach((c) => { x.experto.analisis[`balanceado.peso.${c}`] = base + (resto-- > 0 ? 1 : 0); });
}

function panelPesos(redibujar) {
  const total = totalPesos();
  const bloqueo = bloqueoPesos();
  return h("div", { class: "panel", "data-pesos-balanceado": "" }, h("h3", {}, "¿Cuánto pesa cada criterio? (en %, tienen que sumar 100)"),
    h("div", { class: "pesos" }, (E.catalogo.componentes_balanceado || []).map((c) => h("label", { class: "peso-fila" }, h("span", {}, COMP_NOMBRE[c] || c,
      c === "riesgo" && !tienePesosRiesgo() ? h("span", { class: "peq mut" }, " — requiere los pesos del puntaje de riesgo (modo experto)") : null),
      h("input", { type: "number", min: 0, max: 100, step: 1, value: pesosDe()[`balanceado.peso.${c}`] ?? "", "data-peso": c, placeholder: "0",
        onchange: (e) => { editar((x) => { const v = numOrNull(e.target.value); if (!v) delete x.experto.analisis[`balanceado.peso.${c}`]; else x.experto.analisis[`balanceado.peso.${c}`] = v; }); redibujar(); } })))),
    h("div", { class: "fila-btn" }, h("span", { class: "total-pesos " + (Math.abs(total - 100) < 0.001 ? "ok" : "mal"), "data-total-pesos": String(total) }, `Total: ${fmt(total, "num", 0)} %`),
      h("button", { class: "btn", "data-repartir": "", onclick: () => { editar((x) => repartirPorIgual(x)); redibujar(); } }, "REPARTIR POR IGUAL")),
    bloqueo ? h("div", { class: "banner banner-pend", "data-bloqueo-pesos": "" }, h("span", { class: "ico" }, "⚖"), h("div", {}, bloqueo,
      h("span", { class: "codigo-tecnico" }, "Código técnico: PESOS_NO_DEFINIDOS"))) : null,
    h("p", { class: "mut peq" }, "«Recuperar rápido» (payback) no es un criterio del objetivo balanceado del motor: si es lo más importante para vos, elegí el objetivo «Recuperar rápido». ",
      "Repartir por igual es una elección tuya (supuesto explícito), no una recomendación."));
}

function pasoObjetivo(redibujar) {
  const obj = E.catalogo.objetivos_simples;
  return h("div", {}, h("p", {}, "Elegí qué es lo más importante para vos. La app busca la alternativa que mejor lo cumple dentro de la simulación."),
    h("div", { class: "opciones" }, Object.keys(obj).map((k) => opcion(S().objetivo === k, OBJ_SIMPLE[k]?.[0] || k, OBJ_SIMPLE[k]?.[1],
      () => { set((s) => { s.objetivo = k; }); redibujar(); }, { "data-objetivo": k }, "Código técnico: " + obj[k].objetivo)),
      opcion(!S().objetivo, "No sé", "Mostrar como referencia lo que más valor genera.", () => { set((s) => { s.objetivo = null; }); redibujar(); }, { "data-objetivo": "NO_SE" })),
    !S().objetivo ? noSeTexto("se usa «Ganar más» solo como referencia para ordenar; no se calcula nada distinto.") : null,
    S().objetivo === "BALANCEADO" ? panelPesos(redibujar) : null);
}

// ---------------------------------------------------------------- paso 2: capital
function pasoCapital(redibujar) {
  const c = S().capital;
  const upd = (k, v) => set((s) => { s.capital[k] = v; });
  return h("div", {}, h("p", {}, "¿Con cuánta plata querés probar? Sirve para descartar las alternativas que no entran. USD 2 millones NO se usa por defecto."),
    h("div", { class: "opciones" }, opcion(c.no_se, "No sé", "Probar sin límite de capital", () => { upd("no_se", true); redibujar(); }, { "data-capital": "no_se" }),
      opcion(!c.no_se, "Quiero poner un monto", "Ej.: 1.500.000 dólares", () => { upd("no_se", false); upd("moneda", c.moneda || "USD"); redibujar(); }, { "data-capital": "valor" })),
    c.no_se ? noSeTexto("no se aplica un límite de capital: la simulación NO te va a decir si la plata alcanza.")
      : h("div", { class: "campos", style: { marginTop: "10px" } },
        campo("Capital disponible (" + (c.moneda || "USD") + ")", h("input", { type: "number", step: "any", min: 0, value: c.valor ?? "", "data-campo": "capital", style: { fontSize: "16px" },
          onchange: (e) => upd("valor", numOrNull(e.target.value)) })), h("span", { class: "mut peq", style: { alignSelf: "end" } }, "En pesos o con otra medida: «Ajustar supuestos» más abajo.")));
}

// ---------------------------------------------------------------- paso 3: demanda
const RESPALDO = { ASEGURADA: "Tengo contrato u orden de compra", DOCUMENTADA: "Tengo carta de intención con volumen", NEGOCIADA: "Lo estoy negociando",
  INTERESADA: "Mostró interés", POTENCIAL: "Podría comprar", ESCENARIO: "Es una prueba (supuesto)" };
function pasoDemanda(redibujar) {
  const d = S().demanda;
  const prods = E.catalogo.productos.filter((p) => p.kg_ave > 0);
  const upd = (i, k, v) => set((s) => { s.demanda[i][k] = v; });
  const noSe = d.length === 0;
  return h("div", {}, h("p", {}, "¿Cuánto producto creés que podrías vender? Podés probar distintas cantidades."),
    h("div", { class: "cita" }, "Que un cliente pueda comprar no significa que la venta esté asegurada. Los ~90 supermercados NO cuentan como demanda por sí solos: cargá solo lo que quieras simular y decí qué respaldo tiene."),
    h("div", { class: "opciones", style: { marginTop: "10px" } },
      opcion(noSe, "No sé", "Simular sin demanda", async () => { if (d.length && !(await confirmar("¿Quitar la demanda cargada?", "Se borran las líneas de demanda de este escenario.", "Quitar"))) return; set((s) => { s.demanda = []; }); redibujar(); }, { "data-demanda": "no_se" }),
      opcion(!noSe, "Quiero cargar demanda", "Producto, toneladas por día y respaldo", () => { if (!d.length) set((s) => s.demanda.push({ producto: "pechuga", canal: "supermercados", mercado: "INTERNO", categoria: "ESCENARIO", valor: null, unidad: "t/dia", fuente: "", estado: "ESCENARIO" })); redibujar(); }, { "data-demanda": "cargar" })),
    noSe ? noSeTexto("sin demanda no hay ventas: no se pueden calcular ingresos, EBITDA, VAN, TIR ni payback. Igual vas a ver qué falta.") :
      h("div", { style: { marginTop: "10px" } }, d.map((l, i) => h("div", { class: "campos panel", "data-linea-demanda": i, style: { margin: "6px 0" } },
        campo("Producto", h("select", { onchange: (e) => { upd(i, "producto", e.target.value); redibujar(); } }, prods.map((p) => h("option", { value: p.producto, selected: p.producto === l.producto }, nombreProducto(p.producto))))),
        campo("Cantidad (toneladas por día)", h("input", { type: "number", step: "any", min: 0, value: l.valor ?? "", "data-volumen": "", onchange: (e) => { upd(i, "valor", numOrNull(e.target.value)); upd(i, "unidad", "t/dia"); } })),
        campo("¿Qué respaldo tiene?", h("select", { "data-categoria": "", onchange: (e) => upd(i, "categoria", e.target.value) }, E.catalogo.categorias_demanda.map((c) => h("option", { value: c, selected: c === l.categoria }, RESPALDO[c] || c)))),
        h("button", { class: "btn", style: { alignSelf: "end" }, onclick: () => { set((s) => { s.demanda.splice(i, 1); }); redibujar(); } }, "Quitar"))),
        h("div", { class: "fila-btn" }, h("button", { class: "btn", "data-agregar-demanda": "", onclick: () => {
          set((s) => s.demanda.push({ producto: "pechuga", canal: "supermercados", mercado: "INTERNO", categoria: "ESCENARIO", valor: null, unidad: "t/dia", fuente: "", estado: "ESCENARIO" })); redibujar(); } }, "+ Otro producto"),
          h("span", { class: "mut peq" }, "Canal, fuente y otras unidades: «Ajustar supuestos»."))));
}

// ---------------------------------------------------------------- paso 4: alternativa (arquitectura + escala)
function pasoAlternativa(redibujar) {
  const a = S().arquitectura, e = S().escala, esc = E.catalogo.escalas;
  const val = e.modo === "VALOR" ? e.valor : null;
  return h("div", {}, h("p", {}, "¿Querés que la app pruebe todas las alternativas o tenés una en mente?"),
    h("div", { class: "opciones" },
      opcion(a.modo === "AUTO", "Automático", "La app prueba todas las arquitecturas y elige la que mejor cumple tu objetivo", () => { set((s) => { s.arquitectura = { modo: "AUTO", configuracion: null, variante: null }; }); redibujar(); }, { "data-arquitectura": "AUTO" }),
      opcion(a.modo === "MANUAL", "Quiero probar una", "Elegís cómo se arma la empresa", () => { set((s) => { s.arquitectura.modo = "MANUAL"; s.arquitectura.configuracion ||= "C1"; }); redibujar(); }, { "data-arquitectura": "MANUAL" })),
    a.modo === "MANUAL" ? h("div", { class: "opciones", style: { marginTop: "10px" } }, E.catalogo.arquitecturas.filter((x) => x.tipo === "CONFIGURACION_BASE").map((x) =>
      opcion(a.configuracion === x.id, `${x.id} · ${NOMBRE_ARQ[x.id] || x.titulo}`, x.titulo, () => { set((s) => { s.arquitectura.configuracion = x.id; }); redibujar(); }, { "data-config": x.id }))) : null,
    h("p", {}, h("a", { href: "#/arquitecturas", "data-que-significa": "" }, "¿Qué significa cada arquitectura?")),
    h("h3", {}, "Tamaño de la planta ", ayuda("ESCALA")),
    h("div", { class: "opciones" }, opcion(e.modo === "AUTO", "Automático", "Probar 2.500 / 5.000 / 10.000 / 20.000", () => { set((s) => { s.escala = { modo: "AUTO", valor: null }; }); redibujar(); }, { "data-escala": "AUTO" }),
      esc.referencia.map((v) => opcion(val === v, fmt(v, "ent"), "aves por día", () => { set((s) => { s.escala = { modo: "VALOR", valor: v }; }); redibujar(); }, { "data-escala": v }))),
    h("p", { class: "mut peq" }, "Capacidad no significa que se venda todo. ", h("a", { href: "#/escalas" }, "¿Qué significa cada escala?"), " Otra escala intermedia: «Ajustar supuestos»."));
}

// ---------------------------------------------------------------- paso 5: precios y costos
const ORIGEN = { COTIZACION: "Me lo cotizaron", VALIDADO: "Lo tengo validado", ESCENARIO: "Es una prueba (supuesto)", NO_SE: "No sé" };
function pasoPrecios(redibujar) {
  const pv = S().precios_venta, cu = S().costos_unitarios;
  const prodsDemanda = [...new Set(S().demanda.map((l) => l.producto))];
  const tiene = pv.some((p) => p.estado !== "NO_SE");
  const updPv = (i, k, v) => set((s) => { s.precios_venta[i][k] = v; });
  const asegurarPrecios = () => set((s) => prodsDemanda.forEach((pr) => {
    if (!s.precios_venta.some((p) => p.producto === pr)) {
      const canal = s.demanda.find((l) => l.producto === pr)?.canal || "supermercados";
      s.precios_venta.push({ producto: pr, canal, mercado: "INTERNO", valor: null, moneda: "USD", unidad: "USD/kg", fuente: "", estado: "ESCENARIO" });
    }
  }));
  const costo = (k) => cu.find((c) => c.concepto === k);
  const setCosto = (k, campoC, v) => set((s) => { let c = s.costos_unitarios.find((x) => x.concepto === k); if (!c) { c = { concepto: k, valor: null, moneda: "USD", fuente: "", estado: "ESCENARIO" }; s.costos_unitarios.push(c); } c[campoC] = v; });
  return h("div", {}, h("p", {}, "Con precios de venta y algunos costos, el motor puede calcular la rentabilidad del escenario. Todo lo que cargues queda marcado como simulación."),
    h("div", { class: "opciones" },
      opcion(!tiene && !cu.some((c) => c.valor !== null && c.estado !== "NO_SE"), "No sé", "Simular sin precios", () => { set((s) => { s.precios_venta.forEach((p) => { p.estado = "NO_SE"; }); s.costos_unitarios.forEach((c) => { c.estado = "NO_SE"; }); }); redibujar(); }, { "data-precios": "no_se" }),
      opcion(tiene, "Tengo precios de venta", prodsDemanda.length ? "Para los productos de tu demanda" : "Primero cargá demanda (paso 3)", () => { asegurarPrecios(); set((s) => s.precios_venta.forEach((p) => { if (p.estado === "NO_SE") p.estado = "ESCENARIO"; })); redibujar(); }, { "data-precios": "cargar" })),
    !tiene ? noSeTexto("sin precios de venta no se pueden calcular ingresos ni rentabilidad: el resultado va a decir «Todavía faltan datos para calcular rentabilidad».") : null,
    pv.length && tiene ? h("div", { style: { marginTop: "10px" } }, pv.map((p, i) => p.estado === "NO_SE" ? null : h("div", { class: "campos panel", "data-linea-precio": `precios_venta-${i}`, style: { margin: "6px 0" } },
      h("div", {}, h("b", {}, nombreProducto(p.producto)), h("div", { class: "peq mut" }, p.canal)),
      campo("Precio (dólares por kg)", h("input", { type: "number", step: "any", value: p.valor ?? "", "data-valor-precio": "", onchange: (e) => updPv(i, "valor", numOrNull(e.target.value)) })),
      campo("¿De dónde sale?", h("select", { "data-estado-dato": "", onchange: (e) => { updPv(i, "estado", e.target.value); redibujar(); } }, Object.entries(ORIGEN).map(([k, t]) => h("option", { value: k, selected: p.estado === k }, t)))),
      campo("Fuente (opcional)", h("input", { value: p.fuente ?? "", placeholder: "quién, cuándo", onchange: (e) => updPv(i, "fuente", e.target.value) }))))) : null,
    h("h3", {}, "Costos principales (opcional)"),
    h("div", { class: "campos" }, Object.entries(E.catalogo.costos_unitarios).map(([k, v]) => campo(`${v.texto} (${v.unidad.replace("USD", "dólares")})`,
      h("input", { type: "number", step: "any", placeholder: "No sé", value: costo(k)?.estado === "NO_SE" ? "" : (costo(k)?.valor ?? ""), "data-costo": k,
        onchange: (e) => { const x = numOrNull(e.target.value); setCosto(k, "valor", x); setCosto(k, "estado", x === null ? "NO_SE" : "ESCENARIO"); } })))),
    h("p", { class: "mut peq" }, "Vacío = «No sé»: ese costo queda pendiente (nunca 0). El costo se multiplica por la cantidad que calcula el estudio para cada arquitectura. CAPEX, impuestos, tasa y financiamiento: modo experto."));
}

const RENDER_PASO = { objetivo: pasoObjetivo, capital: pasoCapital, demanda: pasoDemanda, alternativa: pasoAlternativa, precios: pasoPrecios };

// ---------------------------------------------------------------- AJUSTAR SUPUESTOS (avanzado, opcional)
function ajustarSupuestos(redibujar) {
  const c = S().capital, r = S().restricciones || {}, esc = E.catalogo.escalas, e = S().escala;
  const upd = (k, v) => set((s) => { s.capital[k] = v; });
  const def = [["FONDOS_INICIALES", "Máximo capital (fondos iniciales, USD)"], ["PAYBACK", "Máximo payback (años)"], ["VAN", "Mínimo VAN (USD)"], ["TIR", "Mínima TIR (0,15 = 15 %)"],
    ["DSCR", "Mínimo DSCR (veces)"], ["SUPERFICIE_TERRENO", "Máximo terreno (m²)"], ["DEMANDA_MAXIMA_T_DIA", "Demanda disponible a evaluar (t/día)"]];
  return h("details", { class: "acordeon", "data-ajustar-supuestos": "" }, h("summary", {}, "⚙ Ajustar supuestos (opcional)"),
    h("h3", {}, "Capital"), h("div", { class: "campos" },
      campo("Moneda", h("select", { onchange: (ev) => { upd("moneda", ev.target.value); redibujar(); } }, ["USD", "ARS"].map((m) => h("option", { selected: c.moneda === m }, m)))),
      campo("Se compara con", h("select", { onchange: (ev) => upd("metrica", ev.target.value) }, [["PICO_FONDOS", "Pico de fondos"], ["FONDOS_INICIALES", "Fondos iniciales"]].map(([v, t]) => h("option", { value: v, selected: c.metrica === v }, t)))),
      c.moneda === "ARS" ? [
        campo("Tipo de cambio (ARS por USD)", h("input", { type: "number", step: "any", value: c.tc ?? "", onchange: (ev) => upd("tc", numOrNull(ev.target.value)) })),
        campo("Tipo de cambio usado", h("select", { onchange: (ev) => upd("tipo_tc", ev.target.value) }, ["", "oficial", "MEP", "otro"].map((t) => h("option", { selected: c.tipo_tc === t, value: t }, t || "—")))),
        campo("Fecha", h("input", { type: "date", value: c.fecha_tc ?? "", onchange: (ev) => upd("fecha_tc", ev.target.value) })),
        campo("Fuente", h("input", { value: c.fuente_tc ?? "", onchange: (ev) => upd("fuente_tc", ev.target.value) }))] : null),
    h("h3", {}, "Escala intermedia"), campo(`Aves por día (${fmt(esc.rango_min, "ent")}–${fmt(esc.rango_max, "ent")})`, h("input", { type: "number", min: esc.rango_min, max: esc.rango_max, step: 100,
      value: e.modo === "VALOR" && !esc.referencia.includes(e.valor) ? e.valor : "", onchange: (ev) => { const v = numOrNull(ev.target.value); if (v === null) return;
        if (v < esc.rango_min || v > esc.rango_max) { toast(`Fuera del rango que puede evaluar el motor (${esc.rango_min}–${esc.rango_max}).`, 5000); return; }
        set((s) => { s.escala = { modo: "VALOR", valor: Math.round(v) }; }); redibujar(); } })),
    h("h3", {}, "Demanda: todos los campos"),
    h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Producto", "Canal", "Respaldo", "Volumen", "Unidad", "Toma todo", "Fuente", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, S().demanda.map((l, i) => filaDemanda(l, i, redibujar))))),
    h("details", {}, h("summary", {}, "¿Qué respaldos se cuentan como venta en la simulación?"),
      h("div", { class: "opciones" }, E.catalogo.categorias_demanda.map((cat) => h("label", { class: "chip" }, h("input", { type: "checkbox", checked: S().categorias_vendibles.includes(cat),
        onchange: (ev) => set((s) => { s.categorias_vendibles = ev.target.checked ? [...new Set([...s.categorias_vendibles, cat])] : s.categorias_vendibles.filter((x) => x !== cat); }) }), " ", RESPALDO[cat] || cat))),
      campo("Fracción de lo «negociado» que se cuenta (0 a 1)", h("input", { type: "number", step: "any", min: 0, max: 1, value: S().alfa_negociada ?? "", onchange: (ev) => set((s) => { s.alfa_negociada = numOrNull(ev.target.value); }) }),
        "Vacío: lo negociado no se vende (no se asume 100 %).")),
    h("h3", {}, "Precios: todos los campos"),
    h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Producto · canal", "Valor", "Moneda", "Unidad", "Fuente", "Estado", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, S().precios_venta.map((p, i) => filaPrecio(p, i, "precios_venta", redibujar))))),
    h("h3", {}, "Condiciones que la alternativa tiene que cumplir"),
    h("div", { class: "campos" }, def.map(([k, t]) => campo(t, h("input", { type: "number", step: "any", value: r[k] ?? "", "data-restriccion": k,
      onchange: (ev) => set((s) => { s.restricciones = s.restricciones || {}; const v = numOrNull(ev.target.value); if (v === null) delete s.restricciones[k]; else s.restricciones[k] = v; }) }))),
      campo("Horizonte de evaluación (años)", h("input", { type: "number", min: 1, step: 1, value: S().horizonte_anios ?? "", "data-campo": "horizonte",
        onchange: (ev) => set((s) => { s.horizonte_anios = numOrNull(ev.target.value); }) }), "Decisión abierta: 10 / 15 / 20 años como escenarios.")),
    h("p", { class: "mut peq" }, "Todo lo demás (CAPEX, OPEX por módulo, impuestos, tasa, deuda, stress): ", h("a", { href: "#/experto" }, "modo experto"), "."));
}

// ---------------------------------------------------------------- tablas completas (Ajustar supuestos) y gráficos
function filaDemanda(l, i, redibujar) {
  const prods = E.catalogo.productos;
  const upd = (k, v) => set((s) => { s.demanda[i][k] = v; });
  const kg = prods.find((p) => p.producto === l.producto)?.kg_ave;
  return h("tr", { "data-linea-demanda-full": i },
    h("td", {}, h("select", { onchange: (e) => { upd("producto", e.target.value); redibujar(); } }, prods.map((p) => h("option", { value: p.producto, selected: p.producto === l.producto },
      `${p.producto}${p.kg_ave === 0 ? " (0 kg/ave en conf. B)" : ""}`))), kg === 0 ? h("div", { class: "peq mut" }, "La configuración de producto del balance (B, trozado) no produce este producto.") : null),
    h("td", {}, h("select", { onchange: (e) => upd("canal", e.target.value) }, E.catalogo.canales.map((c) => h("option", { selected: c === l.canal }, c)))),
    h("td", {}, h("select", { "data-categoria-full": "", onchange: (e) => upd("categoria", e.target.value) }, E.catalogo.categorias_demanda.map((c) => h("option", { selected: c === l.categoria }, c)))),
    h("td", {}, h("input", { type: "number", step: "any", min: 0, value: l.valor ?? "", style: { width: "90px" }, "data-volumen-full": "", onchange: (e) => upd("valor", numOrNull(e.target.value)) })),
    h("td", {}, h("select", { onchange: (e) => upd("unidad", e.target.value) }, E.catalogo.unidades_demanda.map((u) => h("option", { selected: u === l.unidad }, u)))),
    h("td", {}, h("input", { type: "checkbox", checked: !!l.toma_todo, title: "Canal de liquidación: demanda supuesta ilimitada", onchange: (e) => upd("toma_todo", e.target.checked) })),
    h("td", {}, h("input", { value: l.fuente ?? "", placeholder: "fuente", onchange: (e) => upd("fuente", e.target.value) })),
    h("td", {}, h("button", { class: "btn", title: "Quitar", onclick: () => { set((s) => { s.demanda.splice(i, 1); }); redibujar(); } }, "✕")));
}

function filaPrecio(p, i, lista, redibujar) {
  const upd = (k, v) => set((s) => { s[lista][i][k] = v; });
  const esVenta = lista === "precios_venta";
  return h("tr", { "data-linea-precio-full": `${lista}-${i}` },
    esVenta ? h("td", {}, h("select", { onchange: (e) => upd("producto", e.target.value) }, E.catalogo.productos.map((x) => h("option", { selected: x.producto === p.producto }, x.producto))),
      h("select", { onchange: (e) => upd("canal", e.target.value) }, E.catalogo.canales.map((c) => h("option", { selected: c === p.canal }, c))))
      : h("td", {}, E.catalogo.costos_unitarios[p.concepto]?.texto || p.concepto),
    h("td", {}, h("input", { type: "number", step: "any", value: p.valor ?? "", style: { width: "100px" }, "data-valor-precio-full": "", disabled: p.estado === "NO_SE",
      onchange: (e) => upd("valor", numOrNull(e.target.value)) })),
    h("td", {}, h("select", { onchange: (e) => { upd("moneda", e.target.value); redibujar(); } }, ["USD", "ARS"].map((m) => h("option", { selected: (p.moneda || "USD") === m }, m))),
      p.moneda === "ARS" ? h("div", { class: "campos" }, h("input", { type: "number", placeholder: "TC ARS/USD", value: p.tc ?? "", onchange: (e) => upd("tc", numOrNull(e.target.value)) }),
        h("select", { onchange: (e) => upd("tipo_tc", e.target.value) }, ["", "oficial", "MEP", "otro"].map((t) => h("option", { value: t, selected: p.tipo_tc === t }, t || "tipo TC"))),
        h("input", { type: "date", value: p.fecha_tc ?? "", onchange: (e) => upd("fecha_tc", e.target.value) })) : null),
    h("td", {}, esVenta ? "por kg" : E.catalogo.costos_unitarios[p.concepto]?.unidad),
    h("td", {}, h("input", { value: p.fuente ?? "", placeholder: "fuente (proveedor, fecha…)", onchange: (e) => upd("fuente", e.target.value) })),
    h("td", {}, h("select", { "data-estado-dato-full": "", onchange: (e) => { upd("estado", e.target.value); redibujar(); } }, ["VALIDADO", "COTIZACION", "ESCENARIO", "NO_SE"].map((x) => h("option", { selected: p.estado === x, value: x },
      { VALIDADO: "Validado", COTIZACION: "Cotización", ESCENARIO: "Escenario", NO_SE: "No sé" }[x]))), " ", etqEstadoDato(p.estado),
      p.estado === "ESCENARIO" ? h("div", { class: "peq mut" }, "marcado como simulación") : null),
    h("td", {}, h("button", { class: "btn", onclick: () => { set((s) => { s[lista].splice(i, 1); }); redibujar(); } }, "✕")));
}

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


// ---------------------------------------------------------------- RESULTADO SIMPLE
const KPI_AYUDA = {
  VAN: "Cuánto valor genera el proyecto por encima de la rentabilidad mínima que le exigís.",
  TIR: "Rentabilidad implícita estimada del escenario.",
  PAYBACK: "Tiempo aproximado para recuperar la inversión.",
  EBITDA: "Resultado operativo antes de intereses, impuestos y depreciaciones.",
  CAPEX: "Lo que habría que invertir en activos (edificio, máquinas, frío…) en este escenario.",
  "DSCR MÍNIMO": "Cuántas veces el flujo del período más ajustado cubre la cuota de la deuda.",
  "PICO DE FONDOS": "La mayor cantidad de plata que el proyecto llega a necesitar acumulada.",
};
const ESTADO_KPI = { NO_APLICA: "No aplica a este escenario.", NO_RECUPERADO: "La inversión no se recupera dentro del horizonte.",
  NO_DEFINIDA: "La TIR no es única para este flujo de caja.", NO_CALCULADA: "No se calculó en esta vista.", PENDIENTE: "Pendiente: todavía no hay dato." };

function buscarItem(r, etiqueta) {
  for (const c of r.tarjetas || []) for (const it of c.items) if (it.etiqueta === etiqueta) return it;
  return null;
}
function kpi(titulo, termino, it, extra = null, attrs = {}) {
  let cuerpo;
  if (!it) cuerpo = [h("div", { class: "val nd" }, "Pendiente: todavía no hay dato.")];
  else if (it.estado === "VALOR") cuerpo = [h("div", { class: "val" }, fmt(it.valor, it.formato))];
  else {
    const txt = it.estado === "NO_CALCULABLE" ? porQueFalta(it.faltan) : (ESTADO_KPI[it.estado] || it.estado);
    cuerpo = [h("div", { class: "val nd", "data-kpi-nd": it.estado }, txt), h("span", { class: "codigo-tecnico" }, "Código técnico: " + it.estado + ((it.faltan || []).length ? " · " + it.faltan.map((f) => f.bloque).join(", ") : ""))];
  }
  return h("div", { class: "kpi", "data-kpi": termino, ...attrs }, h("div", { class: "lab" }, titulo, ayuda(termino, KPI_AYUDA[termino])), cuerpo,
    h("div", { class: "ayu" }, KPI_AYUDA[termino]), extra);
}

function avisoDscr(det) {
  const d = det?.dscr;
  if (!d) return null;
  return h("div", {}, d.incluye_rampa ? h("div", { class: "aviso-rampa", "data-aviso-rampa": "" },
    "Este mínimo cae en el arranque (período ", d.periodo, ", fase ", d.fase.replace(/_/g, "-").toLowerCase(), "), cuando la planta todavía no produce a pleno. ",
    "No significa que la deuda sea impagable.", d.dscr_minimo_operacion_madura !== null ? [" En operación madura, el DSCR más bajo es ", h("b", {}, fmt(d.dscr_minimo_operacion_madura, "veces")), "."] : null) : null);
}

export function vistaResultadoSimple(r) {
  const cont = h("div", { "data-resultado": r.resultado, "data-resultado-simple": "" });
  cont.append(bannerUniverso(r));
  if (r.resultado !== "ALTERNATIVA") {
    const ni = r.no_invertir || {};
    const sinInv = r.resultado === "SIN_INVERSION";
    cont.append(h("div", { class: "titular pend", "data-titular": "" }, sinInv ? "Con los datos que cargaste, la regla de decisión indica no comprometer capital todavía." : "Todavía faltan datos para calcular rentabilidad."),
      h("div", { class: "panel", "data-no-invertir": ni.estado_app || r.resultado }, h("p", { style: { fontSize: "15px" } }, ni.texto),
        sinInv ? h("p", {}, "Esto NO es un fracaso: es una decisión válida (mantener opciones abiertas y validar más información).") : null,
        h("span", { class: "codigo-tecnico" }, "Código técnico: " + (ni.estado_app || r.resultado)),
        h("details", {}, h("summary", {}, "Ver detalles técnicos"), ni.reglas?.length ? h("ul", {}, ni.reglas.map((x) => h("li", {}, x))) : null,
          ni.por_que ? h("p", { class: "mut" }, ni.por_que) : null, r.optimizacion ? h("p", { class: "mut" }, `Se evaluaron ${r.optimizacion.n_alternativas} alternativas (${r.optimizacion.n_completas} con datos completos).`) : null,
          alertas(r.alertas))),
      h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/validacion" }, "Qué falta validar"), h("a", { class: "btn", href: "#/optimizar" }, "Ver todas las alternativas")),
      disclaimer(r.disclaimer));
    return cont;
  }
  const fj = r.alternativa, det = r.detalle || {};
  E.alternativa = fj.id;
  const van = buscarItem(r, "VAN");
  const calculable = van?.estado === "VALOR";
  const frase = !calculable ? "Todavía faltan datos para calcular rentabilidad."
    : r.modo === "AUTOMATICO" ? "Con los datos que cargaste, esta alternativa es la que mejor cumple tu objetivo dentro de la simulación."
      : "Con los datos que cargaste, este es el resultado de la alternativa que elegiste, dentro de la simulación.";
  const dscr = buscarItem(r, "DSCR mínimo");
  const sexto = dscr && dscr.estado !== "NO_APLICA" ? kpi("DSCR mínimo del horizonte", "DSCR MÍNIMO", dscr, avisoDscr(det)) : kpi("Pico de fondos", "PICO DE FONDOS", buscarItem(r, "Pico de fondos"));
  cont.append(h("div", { class: "titular" + (calculable ? "" : " pend"), "data-titular": "" }, frase),
    h("p", { style: { fontSize: "15px" } }, "Alternativa: ", h("b", { "data-alternativa-nombre": "" }, nombreAlternativa(fj)), h("span", { class: "codigo-tecnico" }, "Código técnico: " + fj.id)),
    h("div", { class: "kpis", "data-kpis": "" },
      kpi("Inversión", "CAPEX", buscarItem(r, "CAPEX")), kpi("VAN", "VAN", van), kpi("TIR", "TIR", buscarItem(r, "TIR")),
      kpi("Payback", "PAYBACK", buscarItem(r, "Payback")), kpi("EBITDA (último año)", "EBITDA", buscarItem(r, "EBITDA")), sexto));
  const card = (id) => (r.tarjetas || []).filter((c) => c.id === id);
  const S_ = det.series?.series || {};
  const per = det.series?.periodos;
  cont.append(
    h("details", { class: "acordeon", "data-acordeon": "inversion" }, h("summary", {}, "Ver inversión"), tarjetas(card("inversion")),
      per ? h("div", { class: "panel" }, h("h3", {}, "Inversión y capital de trabajo por año"), barras([{ nombre: "CAPEX", valores: S_.capex_total }, { nombre: "Capital de trabajo", valores: S_.delta_ct }], per)) : null),
    h("details", { class: "acordeon", "data-acordeon": "rentabilidad" }, h("summary", {}, "Ver rentabilidad"), tarjetas([...card("negocio"), ...card("retorno"), ...card("deuda")]),
      per ? h("div", { class: "panel" }, h("h3", {}, "Ingresos, costos y EBITDA por año"), barras([{ nombre: "Ingreso neto", valores: S_.ingreso_neto }, { nombre: "OPEX", valores: S_.opex_total }, { nombre: "EBITDA", valores: S_.ebitda }], per)) : null),
    h("details", { class: "acordeon", "data-acordeon": "riesgos" }, h("summary", {}, "Ver riesgos"), tarjetas([...card("riesgo"), ...card("evidencia"), ...card("limitacion")]),
      h("div", { class: "fila-btn" }, h("a", { class: "btn", href: "#/riesgos?tab=stress", onclick: () => { E.alternativa = fj.id; } }, "¿Qué pasa si sube el alimento? (stress)"))),
    detallesTecnicos(r, fj),
    disclaimer(r.disclaimer));
  return cont;
}

function detallesTecnicos(r, fj) {
  const porQue = h("div");
  const qh = r.que_hacer || [];
  return h("details", { class: "acordeon", "data-acordeon": "tecnico" }, h("summary", {}, "Ver detalles técnicos"),
    alertas(r.alertas),
    h("div", { class: "fila-btn" }, h("span", {}, "Semáforo: "), semaforo(fj.semaforo, E.estado?.semaforo), leyendaSemaforo(E.estado?.semaforo)),
    r.detalle?.error_construccion ? errorBox({ codigo: r.detalle.error_construccion.codigo, message: r.detalle.error_construccion.mensaje }) : null,
    tarjetas(r.tarjetas),
    h("div", { class: "panel", "data-que-hacer": "" }, h("h3", {}, "Qué hacer ahora"), h("ol", {}, qh.map((a) => h("li", {}, a.accion, a.dpv ? h("span", { class: "mut peq" }, ` (${a.dpv})`) : null,
      a.empate ? h("span", { class: "etq etq-info" }, "empate") : null)))),
    h("div", { class: "fila-btn" },
      h("button", { class: "btn btn-primario", "data-boton-por-que": "", onclick: () => { porQue.firstChild ? porQue.replaceChildren() : porQue.replaceChildren(panelPorQue(r)); } }, "¿Por qué me da este resultado?"),
      h("button", { class: "btn", "data-exportar": "json", onclick: async () => { const j = await api.post("/api/exportar/json", { escenario: E.escenario }); descargar(`escenario_${E.escenario.id}.json`, JSON.stringify(j, null, 1)); } }, "Exportar JSON"),
      h("button", { class: "btn", "data-exportar": "csv", onclick: async () => { try { descargar(`resultado_${E.escenario.id}.csv`, await api.texto("/api/exportar/csv", { escenario: E.escenario, alternativa: fj.id }), "text/csv"); } catch (e) { toast(e.message, 6000); } } }, "Exportar CSV"),
      h("button", { class: "btn", "data-exportar": "resumen", onclick: async () => { try { const t = await api.texto("/api/exportar/resumen", { escenario: E.escenario, alternativa: fj.id });
        const w = window.open(URL.createObjectURL(new Blob([t], { type: "text/html" })), "_blank"); if (!w) descargar(`resumen_${E.escenario.id}.html`, t, "text/html"); } catch (e) { toast(e.message, 6000); } } }, "Resumen imprimible")),
    porQue, h("h3", {}, "Gráficos"), graficosResultado(r.detalle));
}

// compatibilidad: otras vistas pueden seguir llamando vistaResultado
export const vistaResultado = vistaResultadoSimple;

// ---------------------------------------------------------------- render
export async function render() {
  if (escenarioDelAsistente !== E.cargas) { pasoAct = "objetivo"; escenarioDelAsistente = E.cargas; }
  const raiz = h("div");
  const resultado = h("div", { id: "resultado-simulacion" });
  const idx = () => PASOS.findIndex((p) => p[0] === pasoAct);
  function dibujar() {
    const i = idx();
    const bloqueo = bloqueoPesos();
    const ultimo = i === PASOS.length - 1;
    raiz.replaceChildren(
      h("h1", {}, "▶ Simular un escenario"), h("p", { class: "mut" }, "Respondé 5 preguntas. Podés volver atrás sin perder lo cargado. Todo resultado es una simulación, no un dato real."),
      h("div", { class: "progreso-pasos" }, h("b", { "data-paso-n": String(i + 1) }, `Paso ${i + 1} de ${PASOS.length}`), barraProgreso(100 * (i + 1) / PASOS.length)),
      h("div", { class: "pasos" }, PASOS.map(([id, t], k) => h("button", { class: "paso" + (id === pasoAct ? " act" : k < i ? " hecho" : ""), "data-paso": id, onclick: () => { pasoAct = id; dibujar(); } }, `${k + 1}. ${t}`))),
      h("div", { class: "panel" }, h("div", { class: "paso-titulo" }, PASOS[i][1]), RENDER_PASO[pasoAct](dibujar),
        h("div", { class: "fila-btn", style: { marginTop: "16px" } },
          i > 0 ? h("button", { class: "btn btn-grande", "data-atras": "", onclick: () => { pasoAct = PASOS[i - 1][0]; dibujar(); } }, "← ATRÁS") : null,
          !ultimo ? h("button", { class: "btn btn-primario btn-grande", "data-continuar": "", onclick: () => { pasoAct = PASOS[i + 1][0]; dibujar(); } }, "CONTINUAR →") : null,
          ultimo ? h("button", { class: "btn btn-primario btn-grande", "data-simular": "", disabled: !!bloqueo, title: bloqueo || "", onclick: correr }, "SIMULAR") : null),
        ultimo && bloqueo ? h("div", { class: "banner banner-pend", "data-bloqueo-pesos": "" }, h("span", { class: "ico" }, "⚖"),
          h("div", {}, h("b", {}, "No se puede simular todavía"), bloqueo, " Volvé al paso 1 para definir los pesos.", h("span", { class: "codigo-tecnico" }, "Código técnico: PESOS_NO_DEFINIDOS"))) : null),
      ajustarSupuestos(dibujar), resultado);
  }
  async function correr() {
    if (bloqueoPesos()) { dibujar(); return; }
    resultado.replaceChildren(cargando(S().arquitectura.modo === "AUTO" || S().escala.modo === "AUTO" ? "El motor prueba todas las alternativas (puede tardar unos segundos)…" : "Calculando con el motor…"));
    try {
      const r = await pedir("simular", "/api/simular");
      resultado.replaceChildren(h("h1", {}, "Resultado"), vistaResultadoSimple(r));
      resultado.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (e) { resultado.replaceChildren(errorBox(e)); }
  }
  dibujar();
  const off = alCambiar(() => {
    if (!document.body.contains(resultado)) { off(); return; }
    if (resultado.querySelector("[data-resultado]") && !Object.keys(E.res).some((k) => k.startsWith("simular"))) {
      resultado.replaceChildren(h("div", { class: "banner banner-pend", "data-desactualizado": "" }, h("span", { class: "ico" }, "↻"),
        h("div", {}, h("b", {}, "Cambiaste datos"), "El resultado anterior ya no corresponde a este escenario. Tocá SIMULAR de nuevo.")));
    }
  });
  const previo = Object.entries(E.res).find(([k]) => k.startsWith("simular"));
  if (previo) resultado.replaceChildren(h("h1", {}, "Resultado"), vistaResultadoSimple(previo[1]));
  else resultado.replaceChildren(vacio("▶", "Todavía no simulaste ningún escenario. Respondé las 5 preguntas de arriba y tocá SIMULAR en el último paso.",
    "CREAR ESCENARIO", () => { pasoAct = "objetivo"; dibujar(); window.scrollTo(0, 0); }, { "data-vacio-simular": "" }));
  return raiz;
}
