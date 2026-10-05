// OPTIMIZAR (#19–#21, #28): mejor alternativa DEL ESCENARIO, segunda, diferencia, por qué gana, qué podría hacerla perder.
import { E, editar, pedir } from "../estado.js";
import { h, etq, fmt, alertas, disclaimer, cargando, errorBox, bannerUniverso, semaforo, tabla, campo, numOrNull } from "../ui.js";
import { dispersion } from "../graficos.js";
import { tablaComparacion } from "./comparar.js";

function formulario(redibujar) {
  const s = E.escenario.simple;
  const obj = E.catalogo.objetivos_simples;
  const nombres = { GANAR_MAS: "Ganar más (MAX_VAN)", INVERTIR_MENOS: "Invertir menos", RECUPERAR_RAPIDO: "Recuperar rápido", REDUCIR_RIESGO: "Reducir riesgo", CRECER: "Crecer", BALANCEADO: "Balanceado" };
  const r = s.restricciones || {};
  const setR = (k, v) => editar((e) => { e.simple.restricciones = e.simple.restricciones || {}; if (v === null) delete e.simple.restricciones[k]; else e.simple.restricciones[k] = v; });
  const a = E.escenario.experto.analisis || {};
  return h("div", { class: "panel" }, h("div", { class: "campos" },
    campo("Objetivo", h("select", { "data-opt-objetivo": "", onchange: (e) => { editar((x) => { x.simple.objetivo = e.target.value || null; }); redibujar(); } },
      h("option", { value: "" }, "— (se muestra MAX_VAN)"), Object.keys(obj).map((k) => h("option", { value: k, selected: s.objetivo === k }, nombres[k]))),
      s.objetivo ? obj[s.objetivo].texto : "Se corren todos los objetivos; el elegido se destaca."),
    campo("Capital disponible (USD; vacío = sin restricción)", h("input", { type: "number", step: "any", "data-opt-capital": "", value: s.capital.no_se ? "" : (s.capital.valor ?? ""),
      onchange: (e) => editar((x) => { const v = numOrNull(e.target.value); x.simple.capital.no_se = v === null; x.simple.capital.valor = v; x.simple.capital.moneda = "USD"; }) })),
    campo("Demanda disponible (t/día, consulta)", h("input", { type: "number", step: "any", value: r.DEMANDA_MAXIMA_T_DIA ?? "", onchange: (e) => setR("DEMANDA_MAXIMA_T_DIA", numOrNull(e.target.value)) })),
    campo("Payback máximo (años)", h("input", { type: "number", step: "any", value: r.PAYBACK ?? "", onchange: (e) => setR("PAYBACK", numOrNull(e.target.value)) })),
    campo("VAN mínimo (USD)", h("input", { type: "number", step: "any", value: r.VAN ?? "", onchange: (e) => setR("VAN", numOrNull(e.target.value)) })),
    campo("DSCR mínimo", h("input", { type: "number", step: "any", value: r.DSCR ?? "", onchange: (e) => setR("DSCR", numOrNull(e.target.value)) })),
    campo("Riesgo máximo (score 0–1)", h("input", { type: "number", step: "any", value: r.RIESGO ?? "", onchange: (e) => setR("RIESGO", numOrNull(e.target.value)) }),
      a["riesgo.peso.VAN_NEGATIVO_ESCENARIOS"] ? "Pesos de riesgo declarados." : "Requiere pesos de riesgo (modo experto); sin pesos queda NO EVALUABLE."),
    campo("Horizonte (años)", h("input", { type: "number", step: 1, min: 1, value: s.horizonte_anios ?? E.escenario.experto.comun.valores?.horizonte_anios ?? "",
      onchange: (e) => editar((x) => { x.simple.horizonte_anios = numOrNull(e.target.value); }) }))),
    h("p", { class: "mut peq" }, "Las restricciones son obligatorias (HARD). Las SOFT con penalización se declaran en el modo experto."));
}

function bloqueDecision(r) {
  const d = r.decision_principal, x = r.explicacion;
  if (!d) return null;
  if (d.ESTADO !== "MEJOR_EN_ESCENARIO" || d.DECISION_ESCENARIO === "NO_INVERTIR_AUN") {
    const info = x?.no_invertir || {};
    const ganadora = d.ESTADO === "MEJOR_EN_ESCENARIO" ? h("p", {}, `Mejor inversión del ranking: ${d.MEJOR}; pero la regla de decisión indica NO_INVERTIR_AUN.`) : null;
    return h("div", { class: "panel", "data-decision": info.estado_app || d.DECISION_ESCENARIO || d.ESTADO }, h("h2", {}, info.titulo || d.ESTADO), ganadora, h("p", {}, info.texto),
      info.reglas?.length ? h("ul", {}, info.reglas.map((y) => h("li", {}, y))) : null, h("p", { class: "mut" }, d.POR_QUE || ""), h("p", { class: "mut peq" }, d.NOTA || ""));
  }
  return h("div", { class: "panel ganador", "data-decision": "MEJOR_EN_ESCENARIO" },
    h("h3", {}, "Mejor alternativa del escenario"), h("div", { class: "kpi-grande", "data-mejor": d.MEJOR }, d.MEJOR),
    h("div", { class: "rejilla rejilla-3" },
      h("div", {}, h("h3", {}, "Segunda alternativa"), h("b", {}, d.SEGUNDA || "—")),
      h("div", {}, h("h3", {}, "Diferencia"), h("b", {}, d.DIFERENCIA_VALOR !== undefined && d.DIFERENCIA_VALOR !== null ? fmt(d.DIFERENCIA_VALOR, ["VAN", "EBITDA", "CAPEX", "FONDOS_INICIALES", "PICO_FONDOS"].includes(d.METRICA) ? "usd" : "num") + ` en ${d.METRICA}` : "—")),
      h("div", {}, h("h3", {}, "Robustez de la decisión"), h("span", {}, d.ROBUSTEZ_DECISION || "—"))),
    h("h3", {}, "Por qué gana"), h("p", {}, x.por_que_gana), h("p", { class: "mut" }, x.diferencias),
    h("h3", {}, "Qué podría hacerla perder"), h("ul", {}, (x.que_podria_hacerla_perder || []).map((y) => h("li", {}, y))),
    h("h3", {}, "Restricciones"), h("p", {}, x.restricciones), h("h3", {}, "Datos faltantes / a validar"), h("p", {}, x.datos_faltantes),
    h("h3", {}, "¿Podría ganar NO_INVERTIR_AUN?"), h("p", {}, x.no_invertir_podria_ganar), h("p", { class: "mut peq" }, x.nota));
}

export function vistaOptimizacion(r) {
  const fs = r.fichas.filter((f) => f.tipo !== "NO_INVERTIR_AUN");
  const obj = r.objetivo_principal;
  const decs = Object.values(r.decisiones);
  const par = (r.pareto || []).filter((p) => p.PAR === "VAN×FONDOS_INICIALES");
  const pts = par.filter((p) => p.VALOR_X !== undefined && p.EN_FRONTERA !== "NO_EVALUABLE").map((p) => ({ x: p.VALOR_Y, y: p.VALOR_X, label: p.ALTERNATIVA, frontera: p.EN_FRONTERA === true }));
  const noInf = par.some((p) => String(p.EN_FRONTERA).startsWith("PARETO_NO_INFORMATIVO")) || pts.length < 2;
  const comp = fs.filter((f) => f.completa).slice().sort((a, b) => (a.ranking?.[obj]?.RANK ?? 1e9) - (b.ranking?.[obj]?.RANK ?? 1e9)).slice(0, 5);
  return h("div", { "data-resultado-optimizador": "" }, bannerUniverso(r), alertas(r.alertas),
    h("p", { class: "mut" }, `Objetivo destacado: ${obj} — ${r.objetivo_texto}. ${r.n_alternativas} alternativas evaluadas (${r.n_completas} con datos completos); ${r.evaluaciones_motor} evaluaciones del motor, ${r.aciertos_cache_motor} desde caché.`),
    bloqueDecision(r),
    h("h2", {}, "Decisión por objetivo"),
    tabla(decs, [{ k: "OBJETIVO", t: "Objetivo" }, { k: "ESTADO_APP", t: "Resultado" }, { k: "ESTADO", t: "Estado del motor" }, { k: "MEJOR", t: "Mejor" }, { k: "VALOR_MEJOR", t: "Valor", f: "num" }, { k: "SEGUNDA", t: "Segunda" },
      { k: "DECISION_ESCENARIO", t: "Decisión del escenario", r: (d) => d.DECISION_ESCENARIO === "NO_INVERTIR_AUN" ? etq("INFO", "NO_INVERTIR_AUN") : (d.DECISION_ESCENARIO || "—") },
      { k: "REGLA_STATUS_QUO", t: "Regla" }, { k: "PESOS_BALANCEADO", t: "Pesos" }], { nombre: "decisiones", buscar: false }),
    h("h2", {}, "Top 5 alternativas para el objetivo"), comp.length ? tablaComparacion(comp, r.decision_principal?.MEJOR) : h("p", { class: "mut" }, "Ninguna alternativa con datos completos."),
    h("h2", {}, "Todas las alternativas"),
    tabla(r.fichas, [{ k: "id", t: "Alternativa" }, { k: "rank", t: `Rank ${obj}`, v: (f) => f.ranking?.[obj]?.RANK ?? null, f: "ent", nulo: "—" },
      { k: "semaforo", t: "Semáforo", r: (f) => semaforo(f.semaforo, E.estado?.semaforo) }, { k: "VAN", t: "VAN", v: (f) => f.metricas.VAN, f: "usd", nulo: "no calculable" },
      { k: "FI", t: "Fondos iniciales", v: (f) => f.metricas.FONDOS_INICIALES, f: "usd", nulo: "no calculable" }, { k: "PB", t: "Payback", v: (f) => f.metricas.PAYBACK, f: "num", nulo: "—" },
      { k: "ROB", t: "Robustez", v: (f) => f.robustez, f: "pct", nulo: "—" }, { k: "comparabilidad", t: "Comparable" },
      { k: "motivo", t: "Motivo / faltantes", v: (f) => f.ranking?.[obj]?.MOTIVO || Object.keys(f.faltantes || {}).join(", ") }], { alto: "380px", nombre: "alternativas_optimizador" }),
    h("h2", {}, "Frontera de Pareto (VAN vs fondos iniciales)"),
    noInf ? h("div", { class: "banner banner-pend", "data-pareto": "no-informativo" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, "PARETO NO INFORMATIVO"), "Menos de 2 alternativas comparables con ambos ejes."))
      : dispersion(pts, { nx: "Fondos iniciales (menos es mejor)", ny: "VAN", fx: "usd", fy: "usd" }),
    r.consultas && Object.keys(r.consultas).length ? h("details", {}, h("summary", {}, "Consultas del motor (capital, demanda, payback)"),
      Object.entries(r.consultas).map(([k, filas]) => h("div", {}, h("h3", {}, k), tabla(filas, null, { alto: "240px", nombre: k })))) : null,
    h("h2", {}, "Qué hacer ahora (según la sensibilidad del escenario)"),
    r.que_hacer?.length ? tabla(r.que_hacer, [{ k: "RANK_COMPARTIDO", t: "Rank" }, { k: "QUE_HACER_AHORA", t: "Acción" }, { k: "DPV_VINCULADOS", t: "DPV" }, { k: "RAZON", t: "Razón" }, { k: "EMPATE", t: "Empate" }], { buscar: false })
      : h("p", { class: "mut" }, "Sin prioridades de escenario (no hay ganador con sensibilidad)."),
    disclaimer());
}

export async function render() {
  const raiz = h("div");
  const res = h("div");
  function dibujar() {
    raiz.replaceChildren(h("h1", {}, "◎ Buscar la mejor alternativa"), h("p", { class: "mut" }, "La «mejor» lo es DENTRO DEL ESCENARIO y para el objetivo elegido. «No invertir todavía» también es un resultado posible."),
      h("div", { class: "fila-btn" }, h("a", { class: "btn", href: "#/comparar", "data-ir": "comparar" }, "⇄ Prefiero comparar alternativas a mano")),
      formulario(dibujar), h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario btn-grande", "data-optimizar": "", onclick: correr }, "OPTIMIZAR")), res);
  }
  async function correr() {
    res.replaceChildren(cargando("El motor evalúa todas las alternativas, robustez y stress (puede tardar 10–40 s)…"));
    try { res.replaceChildren(vistaOptimizacion(await pedir("optimizar", "/api/optimizar"))); } catch (e) { res.replaceChildren(errorBox(e)); }
  }
  dibujar();
  const previo = E.res["optimizar{}"];
  if (previo) res.replaceChildren(vistaOptimizacion(previo));
  return raiz;
}
