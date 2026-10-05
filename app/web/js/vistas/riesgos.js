// RIESGOS (#22–#27): ¿qué pasa si…?, tornado, 2D, stress, puntos de quiebre, Monte Carlo y matriz cualitativa.
import { api } from "../api.js";
import { E, pedir } from "../estado.js";
import { h, etq, fmt, fmtShock, disclaimer, cargando, errorBox, bannerUniverso, tabla, pestanas, campo, numOrNull } from "../ui.js";
import { tornado as gTornado, heatmap, lineas, barras, histograma, sinDatos } from "../graficos.js";

const SHOCKS_REL = [-0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3];
const SHOCKS_DIAS = [-30, -20, -10, 0, 10, 20, 30];
const SHOCKS_MESES = [-24, -12, 0, 12, 24];
const SIMPLES = ["precio_venta", "precio_pollo_entero", "precio_cortes", "alimento", "demanda", "capex", "utilizacion", "fx", "salarios", "electricidad",
  "pollito", "facon", "dias_cobro", "tasa_descuento", "rampup", "mortalidad", "fcr", "logistica", "gas"];
let pestanaAct = "quepasa";

const vars = () => E.catalogo.variables_riesgo;
const varInfo = (id) => vars().find((v) => v.id === id) || {};
const shocksDe = (id) => ({ ABSOLUTO_DIAS: SHOCKS_DIAS, ABSOLUTO_MESES: SHOCKS_MESES }[varInfo(id).tipo_shock] || SHOCKS_REL);

// El rótulo del universo (simulación / demo) ya está arriba de la pantalla: dentro de cada pestaña solo se repite si cambia.
function etiquetaUniverso(r) { return null; }

function quePasa(alt) {
  const cont = h("div");
  const soportadas = vars().filter((v) => !["DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"].includes(v.soporte));
  let variable = "alimento";
  const sel = h("select", { "data-variable": "", onchange: (e) => { variable = e.target.value; correr(); } },
    h("optgroup", { label: "Principales" }, SIMPLES.filter((v) => soportadas.some((s) => s.id === v)).map((v) => h("option", { value: v, selected: v === variable }, `${v} — ${varInfo(v).descripcion}`))),
    h("optgroup", { label: "Otras soportadas por el motor" }, soportadas.filter((v) => !SIMPLES.includes(v.id)).map((v) => h("option", { value: v.id }, `${v.id} — ${v.descripcion}`))));
  const out = h("div");
  async function correr() {
    out.replaceChildren(cargando());
    try {
      const r = await pedir("sens", "/api/riesgo/sensibilidad", { alternativa: alt, variables: [variable], shocks: shocksDe(variable) });
      const filas = r.filas.filter((f) => f.SHOCK !== null && f.SHOCK !== undefined);
      if (!filas.length) { out.replaceChildren(h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "–"), h("div", {}, h("b", {}, r.filas[0]?.ESTADO), r.filas[0]?.MOTIVO))); return; }
      const v = varInfo(variable);
      const fxs = filas.map((f) => fmtShock(f.SHOCK, v.tipo_shock));
      const algunoNA = filas.find((f) => f.ESTADO !== "OK");
      out.replaceChildren(etiquetaUniverso(r),
        algunoNA ? h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, algunoNA.ESTADO), algunoNA.MOTIVO)) : null,
        h("div", { class: "rejilla rejilla-2" },
          h("div", { class: "panel" }, h("h3", {}, "VAN según el cambio"), lineas([{ nombre: "VAN", valores: filas.map((f) => f.VAN) }], fxs)),
          h("div", { class: "panel" }, h("h3", {}, "EBITDA y pico de fondos"), lineas([{ nombre: "EBITDA", valores: filas.map((f) => f.EBITDA) }, { nombre: "Pico de fondos", valores: filas.map((f) => f.PICO_FONDOS) }], fxs))),
        tabla(filas, [{ k: "SHOCK", t: "Cambio", r: (f) => h("b", {}, fmtShock(f.SHOCK, v.tipo_shock)) }, { k: "VAN", t: "VAN", f: "usd", nulo: "no calculable" },
          { k: "DELTA_VAN", t: "Δ VAN", f: "usd" }, { k: "EBITDA", t: "EBITDA", f: "usd", nulo: "no calculable" }, { k: "PAYBACK", t: "Payback (años)", f: "num", nulo: "no recupera / n.c." },
          { k: "PICO_FONDOS", t: "Pico de fondos", f: "usd", nulo: "no calculable" }, { k: "ESTADO", t: "Estado" }, { k: "FLAGS", t: "Avisos" }], { nombre: "que_pasa_si_" + variable, buscar: false }),
        h("p", { class: "mut peq" }, `${v.descripcion}. Campo del motor: ${v.campo_motor}. ${v.nota || ""} DPV: ${v.dpv || "—"}. ${r.nota}`));
    } catch (e) { out.replaceChildren(errorBox(e)); }
  }
  cont.append(h("div", { class: "campos" }, campo("¿Qué pasa si cambia…?", sel)), h("p", { class: "mut peq" }, "Cambios de −30 % a +30 % (días o meses para plazos). No son probabilidades."), out);
  correr();
  return cont;
}

function tornado(alt) {
  const out = h("div", {}, cargando("Sensibilidad de todas las variables soportadas…"));
  let met = "VAN";
  const sel = h("select", { onchange: (e) => { met = e.target.value; correr(); } }, ["VAN", "EBITDA", "PICO_FONDOS", "PAYBACK", "DSCR"].map((m) => h("option", {}, m)));
  async function correr() {
    out.replaceChildren(cargando("Sensibilidad de todas las variables soportadas…"));
    try {
      const r = await pedir("tornado", "/api/riesgo/tornado", { alternativa: alt, metrica: met });
      out.replaceChildren(etiquetaUniverso(r), r.calculable ? gTornado(r.tornado, { formato: ["PAYBACK", "DSCR"].includes(met) ? "num" : "usd" })
        : h("div", { class: "banner banner-pend", "data-tornado": "no-calculable" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, "Tornado no disponible"), r.nota)),
      h("details", {}, h("summary", {}, "Tabla"), tabla(r.tornado, [{ k: "RANK", t: "#" }, { k: "VARIABLE", t: "Variable" }, { k: "SWING", t: "Amplitud", f: "num" }, { k: "VALOR_MIN", t: "Mín.", f: "num" },
        { k: "SHOCK_MIN", t: "Shock mín." }, { k: "VALOR_MAX", t: "Máx.", f: "num" }, { k: "SHOCK_MAX", t: "Shock máx." }, { k: "ESTADO", t: "Estado" }, { k: "NOTA", t: "Nota" }], { nombre: "tornado_" + met })));
    } catch (e) { out.replaceChildren(errorBox(e)); }
  }
  correr();
  return h("div", {}, h("div", { class: "campos" }, campo("Métrica", sel)), out);
}

function dosD(alt) {
  const soportadas = vars().filter((v) => !["DISCRETA", "NO_SOPORTADA_POR_INTERFAZ"].includes(v.soporte) && v.tipo_shock === "RELATIVO");
  let vx = "precio_venta", vy = "alimento", met = "VAN";
  const out = h("div");
  const mk = (val, fn) => h("select", { onchange: (e) => { fn(e.target.value); correr(); } }, soportadas.map((v) => h("option", { value: v.id, selected: v.id === val }, v.id)));
  async function correr() {
    out.replaceChildren(cargando());
    try {
      const sh = [-0.2, -0.1, 0, 0.1, 0.2];
      const r = await pedir("s2d", "/api/riesgo/sens2d", { alternativa: alt, vx, vy, shocks: sh });
      const val = (x, y) => r.filas.find((f) => f.SHOCK_X === x && f.SHOCK_Y === y)?.[met] ?? null;
      out.replaceChildren(etiquetaUniverso(r), heatmap(sh, sh, val, { nx: vx, ny: vy, fx: (s) => fmtShock(s), fy: (s) => fmtShock(s), formato: met === "PAYBACK" || met === "DSCR" ? "num" : "usd" }),
        h("p", { class: "mut peq" }, `Verde = ${met} positivo; rojo = negativo (signo, no umbral). ${r.nota} Umbral DSCR: ${r.umbral_dscr ?? "no declarado"}; payback: ${r.umbral_payback ?? "no declarado"}.`));
    } catch (e) { out.replaceChildren(errorBox(e)); }
  }
  correr();
  return h("div", {}, h("div", { class: "campos" }, campo("Variable X (columnas)", mk(vx, (v) => { vx = v; })), campo("Variable Y (filas)", mk(vy, (v) => { vy = v; })),
    campo("Métrica", h("select", { onchange: (e) => { met = e.target.value; correr(); } }, ["VAN", "EBITDA", "PAYBACK", "DSCR"].map((m) => h("option", {}, m))))), out);
}

function stress(alt) {
  const base = (E.escenario.experto.stress?.length ? E.escenario.experto.stress : E.catalogo.stress_motor.map((s) => ({ id: s.id, nombre: s.nombre, shocks: { ...s.shocks, ...Object.fromEntries(s.pendientes.map((p) => [p, null])) }, activo: s.activo })));
  const st = structuredClone(base);
  const out = h("div");
  const editor = h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Stress", "Variable", "Magnitud (fracción o días)"].map((x) => h("th", {}, x)))),
    h("tbody", {}, st.flatMap((s) => Object.entries(s.shocks).map(([v, x]) => h("tr", {}, h("td", {}, s.nombre || s.id), h("td", {}, v),
      h("td", {}, h("input", { type: "number", step: "any", value: x ?? "", placeholder: "PENDIENTE", "data-stress": `${s.id}:${v}`, onchange: (e) => { s.shocks[v] = numOrNull(e.target.value); } }))))))));
  async function correr() {
    out.replaceChildren(cargando());
    try {
      const r = await pedir("stress", "/api/riesgo/stress", { alternativa: alt, stresses: st });
      const ok = r.filas.filter((f) => f.ESTADO === "OK");
      out.replaceChildren(etiquetaUniverso(r),
        h("div", { class: "panel" }, h("h3", {}, "VAN: base vs stress"), barras([{ nombre: "Base", valores: ok.map(() => r.base.VAN) }, { nombre: "Stress", valores: ok.map((f) => f.VAN) }], ok.map((f) => f.NOMBRE || f.ID_STRESS))),
        tabla(r.filas, [{ k: "NOMBRE", t: "Stress" }, { k: "ESTADO", t: "Estado" }, { k: "VAN", t: "VAN stress", f: "usd", nulo: "—" }, { k: "DELTA_VAN", t: "Δ VAN", f: "usd" },
          { k: "EBITDA", t: "EBITDA", f: "usd", nulo: "—" }, { k: "PAYBACK", t: "Payback", f: "num", nulo: "—" }, { k: "PICO_FONDOS", t: "Pico fondos", f: "usd", nulo: "—" },
          { k: "DSCR", t: "DSCR", f: "num", nulo: "—" }, { k: "MOTIVO", t: "Motivo" }], { nombre: "stress", buscar: false }),
        h("p", { class: "mut peq" }, r.nota));
    } catch (e) { out.replaceChildren(errorBox(e)); }
  }
  return h("div", {}, h("p", {}, "Magnitudes editables (relativas: −0,30 = −30 %; plazos en días). Un valor vacío deja el stress NO EJECUTADO (pendiente)."), editor,
    h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario", "data-correr-stress": "", onclick: correr }, "Ejecutar stress")), out);
}

function quiebres(alt) {
  const out = h("div", {}, cargando("Buscando puntos de quiebre (grilla + bisección)…"));
  pedir("quiebres", "/api/riesgo/quiebres", { alternativa: alt }).then((r) => {
    out.replaceChildren(etiquetaUniverso(r), h("h3", {}, "¿Hasta dónde aguanta el negocio?"),
      h("div", { class: "rejilla rejilla-auto" }, r.filas.map((q) => h("div", { class: "tarjeta" }, h("h3", {}, q.PREGUNTA),
        q.MOSTRAR ? h("div", { class: "val", style: { fontSize: "20px", fontWeight: 700 } }, q.TIPO_SHOCK === "RELATIVO" ? fmt(q.SHOCK_QUIEBRE, "pct") : fmt(q.SHOCK_QUIEBRE, "num") + " días")
          : etq(q.ESTADO === "VARIABLE_NO_APLICA" ? "NO_APLICA" : "NO_CALCULABLE", q.ESTADO), h("p", { class: "peq" }, q.TEXTO),
        q.VALOR_ABSOLUTO_QUIEBRE !== undefined ? h("p", { class: "peq mut" }, `valor absoluto: ${fmt(q.VALOR_ABSOLUTO_QUIEBRE, "num")}`) : null))),
      h("p", { class: "mut peq" }, r.nota));
  }).catch((e) => out.replaceChildren(errorBox(e)));
  return out;
}

function montecarlo(alt) {
  const out = h("div");
  let n = 500, semilla = 20261005;
  async function correr() {
    out.replaceChildren(cargando("Monte Carlo…"));
    try {
      const r = await pedir("mc", "/api/riesgo/montecarlo", { alternativa: alt, n, semilla });
      if (!r.disponible) {
        out.replaceChildren(h("div", { class: "banner banner-pend", "data-mc": "no-disponible" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, "NO DISPONIBLE"), r.explicacion,
          h("div", { class: "peq mut" }, `${r.estado}: ${(r.notas || []).join(" · ")}`))),
        h("p", {}, "Para ejecutarlo, cargue en el modo experto distribuciones RESPALDADAS (con fuente) en este escenario."));
        return;
      }
      const R = r.resumen;
      out.replaceChildren(etiquetaUniverso(r), h("div", { class: "banner banner-sim", "data-mc": "ejecutado" }, h("span", { class: "ico" }, "◇"), h("div", {}, h("b", {}, "Probabilidad simulada"),
        "Proporciones dentro de la simulación con las distribuciones declaradas. NO es probabilidad real, histórica ni del proyecto.")),
        h("div", { class: "rejilla rejilla-3" },
          h("div", { class: "panel" }, h("h3", {}, "VAN negativo (simulado)"), h("div", { class: "kpi-grande" }, fmt(R.PROB_VAN_NEGATIVO, "pct"))),
          h("div", { class: "panel" }, h("h3", {}, "Déficit (simulado)"), h("div", { class: "kpi-grande" }, fmt(R.PROB_DEFICIT, "pct")), h("p", { class: "peq mut" }, R.DEFINICION_DEFICIT)),
          h("div", { class: "panel" }, h("h3", {}, "No recupera en el horizonte"), h("div", { class: "kpi-grande" }, fmt(R.PROB_NO_RECUPERO, "pct")))),
        histograma(r.van_muestras),
        tabla(["VAN", "PICO_FONDOS", "DSCR", "PAYBACK"].map((m) => ({ metrica: m, ...(R[m] || {}) })), [{ k: "metrica", t: "Métrica" }, { k: "N_VALIDOS", t: "N" }, { k: "P10", t: "P10", f: "num" },
          { k: "P50", t: "P50", f: "num" }, { k: "P90", t: "P90", f: "num" }, { k: "MEDIA", t: "Media", f: "num" }], { buscar: false, nombre: "montecarlo" }),
        h("p", { class: "mut peq" }, `N = ${R.N}, semilla ${R.SEMILLA}. Correlaciones: ${R.CORRELACIONES}. Variables: ${(R.VARIABLES || []).join(", ")}.`));
    } catch (e) { out.replaceChildren(errorBox(e)); }
  }
  correr();
  return h("div", {}, h("div", { class: "campos" }, campo("Simulaciones", h("input", { type: "number", value: n, min: 50, max: 5000, onchange: (e) => { n = numOrNull(e.target.value) || 500; } })),
    campo("Semilla (reproducible)", h("input", { type: "number", value: semilla, onchange: (e) => { semilla = numOrNull(e.target.value) || 20261005; } }))),
  h("div", { class: "fila-btn" }, h("button", { class: "btn", onclick: correr }, "Ejecutar de nuevo")), out);
}

async function matriz() {
  const r = await api.get("/api/riesgos_cualitativos");
  return h("div", {}, h("div", { class: "banner banner-evi" }, h("span", { class: "ico" }, "▤"), h("div", {}, h("b", {}, "Registro del proyecto (cualitativo)"), r.nota)),
    tabla(r.matriz, [{ k: "ID_RIESGO", t: "ID" }, { k: "CATEGORIA", t: "Categoría" }, { k: "RIESGO", t: "Riesgo" }, { k: "PROBABILIDAD_INHERENTE", t: "Prob." }, { k: "IMPACTO_INHERENTE", t: "Impacto" },
      { k: "CLASE_INHERENTE", t: "Clase" }, { k: "ESTADO_MITIGACION", t: "Mitigación" }, { k: "DRIVERS", t: "Drivers" }], { nombre: "matriz_riesgos", alto: "460px" }));
}

export async function render() {
  const raiz = h("div", {}, h("h1", {}, "Riesgos"), h("p", { class: "mut" }, "Sensibilidades y stress sobre el escenario actual (simulación). La matriz cualitativa es del proyecto."));
  let alts;
  try { alts = await pedir("alternativas", "/api/alternativas"); } catch (e) { raiz.append(errorBox(e)); return raiz; }
  const completas = alts.alternativas.filter((a) => a.completa);
  let alt = completas.some((a) => a.id === E.alternativa) ? E.alternativa : completas[0]?.id;
  const zona = h("div");
  function dibujar() {
    E.alternativa = alt;
    zona.replaceChildren(pestanas([{ id: "quepasa", t: "¿Qué pasa si…?" }, { id: "tornado", t: "Tornado" }, { id: "2d", t: "Sensibilidad 2D" }, { id: "stress", t: "Stress" },
      { id: "quiebres", t: "Puntos de quiebre" }, { id: "mc", t: "Monte Carlo" }, { id: "matriz", t: "Matriz cualitativa" }], (id, cont) => {
      pestanaAct = id;
      if (id === "matriz") { cont.append(cargando()); matriz().then((n) => cont.replaceChildren(n)).catch((e) => cont.replaceChildren(errorBox(e))); return; }
      if (!alt) { cont.append(sinDatos("Ninguna alternativa del escenario tiene datos completos (VAN calculable): no hay sensibilidades que mostrar. Revise qué falta en COMPARAR o SIMULAR.")); return; }
      return { quepasa: quePasa, tornado, "2d": dosD, stress, quiebres, mc: montecarlo }[id](alt);
    }, pestanaAct));
  }
  raiz.append(bannerUniverso(alts), h("div", { class: "campos" }, campo("Alternativa analizada", h("select", { "data-alt-riesgo": "", onchange: (e) => { alt = e.target.value; dibujar(); } },
    completas.length ? completas.map((a) => h("option", { value: a.id, selected: a.id === alt }, a.id)) : h("option", {}, "— ninguna con datos completos —")))), zona);
  dibujar();
  raiz.append(disclaimer());
  return raiz;
}
