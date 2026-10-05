// COMPARAR ALTERNATIVAS (#18): 2 a 5 alternativas; no se compara si COMPARABILIDAD = FALSE.
import { E, pedir } from "../estado.js";
import { h, etq, fmt, alertas, disclaimer, cargando, errorBox, bannerUniverso, semaforo, tabla, toast, vacio } from "../ui.js";

let seleccion = [];

export function etiquetaAlt(a) {
  if (!a) return "—";
  const esc = (a.escalas || []).map((x) => fmt(x, "ent")).join("→");
  return `${a.configuracion}${a.variante && a.variante !== "BASE" ? " · " + a.variante : ""}${esc ? " · " + esc + " aves/día" : ""}`;
}

const FILAS = [
  ["Configuración", (f) => f.configuracion + (f.variante && f.variante !== "BASE" ? ` (${f.variante})` : "")],
  ["Escala (aves/día)", (f) => (f.escalas || []).map((x) => fmt(x, "ent")).join(" → ")],
  ["Semáforo", (f) => semaforo(f.semaforo, E.estado?.semaforo)],
  ["Comparabilidad", (f) => f.comparabilidad === "FALSE" ? etq("NO_COMPARABLE") : f.comparabilidad],
  ["Inversión (CAPEX)", (f) => f.metricas.CAPEX, "usd"],
  ["Fondos iniciales", (f) => f.metricas.FONDOS_INICIALES, "usd"],
  ["Pico de fondos", (f) => f.metricas.PICO_FONDOS, "usd"],
  ["Capacidad (demanda necesaria para llenarla, kg/día calendario)", (f) => f.metricas.CAPACIDAD_KG_DIA, "ent"],
  ["Utilización de equilibrio (EBITDA = 0)", (f) => f.metricas.BREAK_EVEN_U, "pct"],
  ["EBITDA (año maduro)", (f) => f.metricas.EBITDA, "usd"],
  ["VAN", (f) => f.metricas.VAN, "usd"],
  ["TIR", (f) => f.metricas.TIR, "pct", (f) => f.metricas.TIR_ESTADO],
  ["Payback (años)", (f) => f.metricas.PAYBACK, "num", (f) => f.metricas.PAYBACK_ESTADO],
  ["DSCR mínimo", (f) => f.metricas.DSCR, "num"],
  ["Score ordinal de riesgo (no es probabilidad)", (f) => f.score_riesgo, "num", (f) => f.riesgo_nota],
  ["Robustez (% escenarios con VAN ≥ 0)", (f) => f.robustez, "pct"],
  ["Cobertura de evidencia", (f) => f.cobertura_evidencia, "pct"],
  ["Respaldo comercial", (f) => f.respaldo_comercial],
  ["Principales faltantes", (f) => Object.keys(f.faltantes || {}).join(", ") || "—"],
  ["Principal limitación", (f) => f.limitacion_principal],
];

function celda(v, formato, estado) {
  if (v instanceof Node) return v;
  if (formato) return v === null || v === undefined ? h("span", { class: "mut" }, estado && estado !== "UNICA" ? String(estado).split(":")[0] : "no calculable") : fmt(v, formato);
  return v ?? "—";
}

export function tablaComparacion(fichas, ganador) {
  return h("div", { class: "tabla-env" }, h("table", { class: "t", "data-tabla-comparacion": "" },
    h("thead", {}, h("tr", {}, h("th", {}, ""), fichas.map((f) => h("th", { class: f.id === ganador ? "ganador" : null }, f.id)))),
    h("tbody", {}, FILAS.map(([t, fn, fo, est]) => h("tr", {}, h("th", {}, t), fichas.map((f) => h("td", { class: fo ? "num" : null }, celda(fn(f), fo, est ? est(f) : null))))))));
}

export async function render() {
  const raiz = h("div", {}, h("h1", {}, "Comparar alternativas"), h("p", { class: "mut" }, "Elegí entre 2 y 5 alternativas del escenario actual."));
  const lista = h("div", {}, cargando("Leyendo alternativas del escenario…"));
  const res = h("div");
  raiz.append(lista, res);
  let alts;
  try { alts = await pedir("alternativas", "/api/alternativas"); } catch (e) { lista.replaceChildren(errorBox(e)); return raiz; }
  seleccion = seleccion.filter((id) => alts.alternativas.some((a) => a.id === id));
  if (!alts.alternativas.some((a) => a.completa)) {
    res.append(vacio("⇄", "Todavía no simulaste ningún escenario con datos suficientes para comparar: ninguna alternativa tiene su resultado calculable. Cargá tus datos en SIMULAR (o abrí la demo) y volvé.",
      "CREAR ESCENARIO", "#/simular", { "data-vacio-comparar": "" }));
  }
  const boton = h("button", { class: "btn btn-primario btn-grande", "data-comparar": "", onclick: correr }, "COMPARAR");
  function actualizar() { boton.disabled = seleccion.length < 2 || seleccion.length > 5; boton.textContent = `COMPARAR (${seleccion.length})`; }
  lista.replaceChildren(bannerUniverso(alts), tabla(alts.alternativas.filter((a) => a.tipo !== "NO_INVERTIR_AUN"), [
    { k: "sel", t: "✓", r: (a) => h("input", { type: "checkbox", checked: seleccion.includes(a.id), "data-alt": a.id, onclick: (e) => e.stopPropagation(), onchange: (e) => {
      if (e.target.checked) { if (seleccion.length >= 5) { e.target.checked = false; toast("Máximo 5 alternativas."); return; } seleccion.push(a.id); } else seleccion = seleccion.filter((x) => x !== a.id); actualizar(); } }) },
    { k: "configuracion", t: "Config." }, { k: "variante", t: "Variante" }, { k: "escalas", t: "Escala(s)", v: (a) => a.escalas.join("→") }, { k: "tipo", t: "Tipo" },
    { k: "completa", t: "¿Datos completos?", r: (a) => a.completa ? etq("OK", "VAN calculable") : etq("PENDIENTE", "faltan datos") },
    { k: "faltan", t: "Faltan", v: (a) => (a.faltan || []).join(", ") }], { alto: "320px", nombre: "alternativas" }), h("div", { class: "fila-btn" }, boton));
  actualizar();
  async function correr() {
    res.replaceChildren(cargando());
    try {
      const r = await pedir("comparar", "/api/comparar", { ids: [...seleccion].sort() });
      const d = r.decisiones?.MAX_VAN;
      res.replaceChildren(bannerUniverso(r), alertas(r.alertas),
        h("div", { class: r.comparable ? "ayuda" : "banner banner-pend", "data-comparable": String(r.comparable) }, r.comparable ? null : h("span", { class: "ico" }, "≠"),
          h("div", {}, r.comparable ? null : h("b", {}, "No se puede comparar (COMPARABILIDAD = FALSE)"), r.explicacion_comparabilidad)),
        tablaComparacion(r.fichas, r.comparable && d?.ESTADO === "MEJOR_EN_ESCENARIO" ? d.MEJOR : null),
        r.comparable && d ? h("p", {}, d.ESTADO === "MEJOR_EN_ESCENARIO" ? `Mayor VAN dentro de este escenario: ${d.MEJOR}. Decisión del escenario (con reglas de status quo): ${d.DECISION_ESCENARIO}.` : `MAX_VAN: ${d.ESTADO}`) : null,
        disclaimer());
    } catch (e) { res.replaceChildren(errorBox(e)); }
  }
  return raiz;
}
