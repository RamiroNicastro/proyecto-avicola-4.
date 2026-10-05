// QUÉ ME FALTA VALIDAR (#29–#32): paquetes, prioridad (empates compartidos), progreso por dimensión, carga a staging.
import { api } from "../api.js";
import { h, etq, fmt, cargando, errorBox, tabla, campo, numOrNull, toast, modal, sinRutas, vacio } from "../ui.js";
import { barraProgreso } from "../graficos.js";

function prioridadEtq(p) {
  const n = (p || "").slice(0, 2);
  return h("span", { class: "etq " + ({ P1: "etq-error", P2: "etq-info", P3: "etq-pend", P4: "etq-na" }[n] || "etq-pend") }, p);
}

export function progreso(p) {
  return h("div", { class: "panel", "data-progreso": "" }, h("h2", {}, "Validación del proyecto"),
    h("div", { class: "progreso" }, p.dimensiones.map((d) => h("div", { class: "dim", "data-dimension": d.id }, h("div", {}, h("b", {}, d.titulo), h("div", { class: "peq mut" }, sinRutas(d.texto))),
      barraProgreso(d.pct), h("span", {}, d.pct === null || d.pct === undefined ? "—" : fmt(d.pct / 100, "pct", 0), " ", h("span", { class: "peq mut" }, d.estado))))),
    h("p", { class: "peq mut" }, sinRutas(p.nota), ` DPV registrados: ${p.dpv.total} (pendientes: ${p.dpv.pendientes}).`),
    h("div", { class: "fila-btn" }, Object.entries(p.estado_general).map(([k, v]) => h("span", { class: "chip" }, sinRutas(`${k} = ${v}`)))));
}

function formularioStaging(alGuardar) {
  const d = { concepto: "", valor: "", unidad: "", moneda: "USD", fecha: new Date().toISOString().slice(0, 10), fuente: "", observaciones: "", tipo: "cotizacion" };
  const msg = h("div");
  const inp = (k, attrs = {}) => h("input", { value: d[k], "data-staging": k, oninput: (e) => { d[k] = e.target.value; }, ...attrs });
  return h("div", { class: "panel", "data-form-staging": "" }, h("h2", {}, "Cargar un dato (cotización, factura, mercado…)"),
    h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "⧗"), h("div", {}, h("b", {}, "Va a STAGING, no a la evidencia"),
      "Se guarda en esta computadora SIN clasificar. La app no lo convierte en dato real ni lo usa en el motor: el analista lo revisa con la guía de recolección de evidencia y lo incorpora a la base que corresponda.")),
    h("div", { class: "campos" }, campo("Concepto", inp("concepto", { placeholder: "p. ej. alimento terminado fase 1" })), campo("Valor (punto decimal)", inp("valor", { type: "number", step: "any" })),
      campo("Unidad", inp("unidad", { placeholder: "USD/t, ARS/kg…" })), campo("Moneda", h("select", { onchange: (e) => { d.moneda = e.target.value; } }, ["USD", "ARS", "otra"].map((m) => h("option", {}, m)))),
      campo("Fecha", inp("fecha", { type: "date" })), campo("Fuente", inp("fuente", { placeholder: "proveedor / documento" })),
      campo("Tipo", h("select", { "data-staging": "tipo", onchange: (e) => { d.tipo = e.target.value; } }, ["cotizacion", "factura", "mercado", "escenario", "otro"].map((t) => h("option", {}, t)))),
      campo("Observaciones (IVA, flete, validez, TC…)", inp("observaciones"))),
    h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario", "data-guardar-staging": "", onclick: async () => {
      try { await api.post("/api/staging", { dato: d }); toast("Guardado en STAGING (sin clasificar)."); msg.replaceChildren(etq("STAGING", "guardado en staging")); alGuardar(); }
      catch (e) { msg.replaceChildren(errorBox(e)); }
    } }, "Guardar en staging")), msg);
}

function checklistPaquete(p, abierto) {
  const porQue = [...new Set(p.dpv.map((d) => d.por_que).filter(Boolean))].slice(0, 3);
  const validados = p.dpv.filter((d) => /^validad/i.test(d.estado || "")).length;
  return h("details", { class: "acordeon", open: abierto, "data-paquete": p.clave },
    h("summary", {}, p.paquete, " ", prioridadEtq(p.prioridad), h("span", { class: "peq mut", style: { fontWeight: 400 } }, ` · ${validados} de ${p.dpv.length} datos validados`)),
    h("div", { "data-detalle-paquete": p.clave },
      h("p", {}, h("b", {}, "Estado: "), validados ? `${validados} validado(s)` : "☐ nada validado todavía", " · ", h("b", {}, "A quién pedir: "), p.actor),
      h("p", {}, h("b", {}, "Qué destraba: "), sinRutas(p.desbloquea)),
      porQue.length ? h("p", {}, h("b", {}, "Por qué importa: "), porQue.map(sinRutas).join(" · ")) : null,
      h("h3", {}, "Qué pedir"),
      h("ul", { class: "check" }, p.pedidos.map((x) => h("li", { "data-pedido": "" }, h("span", { class: "caja", "aria-hidden": "true", title: "Pendiente: se marca solo con evidencia" }, "☐"),
        h("div", {}, h("b", {}, sinRutas(x.que_pedir)), h("div", { class: "peq mut" }, "A quién: ", sinRutas(x.actor) || p.actor, " · Unidad: ", sinRutas(x.unidad) || "—"),
          h("div", { class: "peq" }, "Desbloquea: ", sinRutas(x.desbloquea) || "—"))))),
      h("details", {}, h("summary", {}, `Datos por validar de este paquete (${p.dpv.length})`),
        h("ul", { class: "check" }, p.dpv.map((d) => h("li", {}, h("span", { class: "caja" }, /^validad/i.test(d.estado || "") ? "☑" : "☐"),
          h("div", {}, sinRutas(d.dato), h("div", { class: "peq mut" }, d.id, " · ", d.estado))))))));
}

export async function render() {
  const raiz = h("div", {}, h("h1", {}, "☐ Qué falta validar"), h("p", { class: "mut", style: { fontSize: "15px" } }, "Antes de invertir: qué datos pedir, a quién, en qué unidad y qué resultado destraba cada uno. Ningún casillero se marca sin evidencia."), cargando());
  let r;
  try { r = await api.get("/api/validacion"); } catch (e) { raiz.lastChild.replaceWith(errorBox(e)); return raiz; }
  raiz.lastChild.remove();
  const plan = r.plan, pr = r.prioridad;
  raiz.append(h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/seguir" }, "→ Ver por dónde empezar (prioridades)")),
    h("h2", {}, "Checklist por tema"), h("p", { class: "mut peq" }, sinRutas(plan.criterio_prioridad)),
    h("div", { "data-checklist": "" }, plan.paquetes.map((p, i) => checklistPaquete(p, i === 0))),
    progreso(r.progreso));
  const paqDe = (bloque) => plan.paquetes.filter((p) => (p.desbloquea || "").toUpperCase().includes(String(bloque).split(":")[0].toUpperCase())).map((p) => p.clave);
  raiz.append(h("details", { class: "acordeon" }, h("summary", {}, "🔧 Ver detalle técnico de la prioridad"),
    h("p", { class: "mut peq" }, pr.nota),
    tabla(pr.prioridad, [{ k: "RANK_COMPARTIDO", t: "Prioridad", v: (f) => Number(f.RANK_COMPARTIDO) }, { k: "ACCION", t: "Qué pedir" },
      { k: "paq", t: "A quién (paquete)", v: (f) => paqDe(f.BLOQUE).join(", ") || "—" }, { k: "BLOQUE", t: "Bloque / unidad del motor" },
      { k: "INDICADORES_BLOQUEADOS", t: "Indicadores que desbloquea", v: (f) => Number(f.INDICADORES_BLOQUEADOS) },
      { k: "N_ALTERNATIVAS_BLOQUEADAS", t: "Alternativas bloqueadas", v: (f) => `${f.N_ALTERNATIVAS_BLOQUEADAS}/${f.N_ALTERNATIVAS}` },
      { k: "EMPATE", t: "Empate", r: (f) => f.EMPATE ? h("span", { title: f.EMPATE }, etq("INFO", `empate (${f.N_EMPATADOS})`)) : "—" },
      { k: "DPV_VINCULADOS", t: "DPV" }], { nombre: "prioridad_validacion", alto: "420px" }),
    h("h3", {}, "Qué cambia en el motor con cada paquete"), h("ul", {}, plan.que_cambia.map((x) => h("li", {}, sinRutas(x))))));
  const lista = h("div");
  async function pintarStaging() {
    try { const s = await api.get("/api/staging"); if (!s.filas.length) { lista.replaceChildren(vacio("⧗", "Todavía no cargaste ningún dato. Cuando consigas una cotización, factura o precio de mercado, cargalo arriba: queda guardado aparte, sin mezclarse con los datos reales.", "CARGAR UN DATO", () => document.querySelector("[data-staging='concepto']")?.focus())); return; }
      lista.replaceChildren(h("h3", {}, "Datos en staging"), h("p", { class: "mut peq" }, s.nota), tabla(s.filas, [{ k: "registrado", t: "Registrado" }, { k: "concepto", t: "Concepto" }, { k: "valor", t: "Valor" },
      { k: "unidad", t: "Unidad" }, { k: "moneda", t: "Moneda" }, { k: "fecha", t: "Fecha" }, { k: "fuente", t: "Fuente" }, { k: "tipo", t: "Tipo" }, { k: "estado_staging", t: "Estado", r: () => etq("STAGING") }], { nombre: "staging" })); }
    catch (e) { lista.replaceChildren(errorBox(e)); }
  }
  raiz.append(formularioStaging(pintarStaging), lista);
  pintarStaging();
  return raiz;
}
