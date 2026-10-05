// QUÉ ME FALTA VALIDAR (#29–#32): paquetes, prioridad (empates compartidos), progreso por dimensión, carga a staging.
import { api } from "../api.js";
import { h, etq, fmt, cargando, errorBox, tabla, campo, numOrNull, toast, modal } from "../ui.js";
import { barraProgreso } from "../graficos.js";

function prioridadEtq(p) {
  const n = (p || "").slice(0, 2);
  return h("span", { class: "etq " + ({ P1: "etq-error", P2: "etq-info", P3: "etq-pend", P4: "etq-na" }[n] || "etq-pend") }, p);
}

export function progreso(p) {
  return h("div", { class: "panel", "data-progreso": "" }, h("h2", {}, "Validación del proyecto"),
    h("div", { class: "progreso" }, p.dimensiones.map((d) => h("div", { class: "dim", "data-dimension": d.id }, h("div", {}, h("b", {}, d.titulo), h("div", { class: "peq mut" }, d.texto)),
      barraProgreso(d.pct), h("span", {}, d.pct === null || d.pct === undefined ? "—" : fmt(d.pct / 100, "pct", 0), " ", h("span", { class: "peq mut" }, d.estado))))),
    h("p", { class: "peq mut" }, p.nota, ` DPV registrados: ${p.dpv.total} (pendientes: ${p.dpv.pendientes}).`),
    h("div", { class: "fila-btn" }, Object.entries(p.estado_general).map(([k, v]) => h("span", { class: "chip" }, `${k} = ${v}`))));
}

function formularioStaging(alGuardar) {
  const d = { concepto: "", valor: "", unidad: "", moneda: "USD", fecha: new Date().toISOString().slice(0, 10), fuente: "", observaciones: "", tipo: "cotizacion" };
  const msg = h("div");
  const inp = (k, attrs = {}) => h("input", { value: d[k], "data-staging": k, oninput: (e) => { d[k] = e.target.value; }, ...attrs });
  return h("div", { class: "panel", "data-form-staging": "" }, h("h2", {}, "Cargar un dato (cotización, factura, mercado…)"),
    h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "⧗"), h("div", {}, h("b", {}, "Va a STAGING, no a la evidencia"),
      "Se guarda en app/datos_locales/staging/ SIN clasificar. La app no lo convierte en E1/E2/E3 ni lo usa en el motor: el analista lo clasifica según guia_recoleccion_evidencia.md y lo incorpora a la base que corresponda.")),
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

export async function render() {
  const raiz = h("div", {}, h("h1", {}, "Qué me falta validar"), h("p", { class: "mut" }, "Antes de invertir: qué datos pedir, a quién, en qué unidad y qué resultado desbloquea cada uno."), cargando());
  let r;
  try { r = await api.get("/api/validacion"); } catch (e) { raiz.lastChild.replaceWith(errorBox(e)); return raiz; }
  raiz.lastChild.remove();
  const plan = r.plan, pr = r.prioridad;
  raiz.append(progreso(r.progreso));
  raiz.append(h("h2", {}, "Paquetes de validación"), h("p", { class: "mut peq" }, plan.criterio_prioridad),
    h("div", { class: "rejilla rejilla-auto" }, plan.paquetes.map((p) => h("button", { class: "accion-home", "data-paquete": p.clave, onclick: () => detalle(p) },
      h("span", { class: "t" }, p.paquete), prioridadEtq(p.prioridad), h("span", { class: "d" }, "A quién: " + p.actor), h("span", { class: "d" }, "Desbloquea: " + p.desbloquea),
      h("span", { class: "d" }, `${p.dpv.length} DPV · ${p.pedidos.length} pedidos`)))));
  function detalle(p) {
    modal(h("div", { "data-detalle-paquete": p.clave }, h("h2", {}, p.paquete, " ", prioridadEtq(p.prioridad)), h("p", {}, h("b", {}, "Actor principal: "), p.actor), h("p", {}, h("b", {}, "Desbloquea: "), p.desbloquea),
      h("h3", {}, "Pedidos"), tabla(p.pedidos, [{ k: "que_pedir", t: "Qué pedir" }, { k: "actor", t: "A quién" }, { k: "unidad", t: "Unidad" }, { k: "desbloquea", t: "Qué resultado desbloquea" }], { nombre: "pedidos_" + p.clave, buscar: false }),
      h("h3", {}, "DPV centrales"), tabla(p.dpv, [{ k: "id", t: "ID" }, { k: "dato", t: "Dato requerido" }, { k: "estado", t: "Estado" }, { k: "fuente_sugerida", t: "Fuente sugerida" }], { nombre: "dpv_" + p.clave })));
  }
  const paqDe = (bloque) => plan.paquetes.filter((p) => (p.desbloquea || "").toUpperCase().includes(String(bloque).split(":")[0].toUpperCase())).map((p) => p.clave);
  raiz.append(h("h2", {}, "Prioridad de validación (derivada del motor)"), h("p", { class: "mut peq" }, pr.nota),
    tabla(pr.prioridad, [{ k: "RANK_COMPARTIDO", t: "Prioridad", v: (f) => Number(f.RANK_COMPARTIDO) }, { k: "ACCION", t: "Qué pedir" },
      { k: "paq", t: "A quién (paquete)", v: (f) => paqDe(f.BLOQUE).join(", ") || "—" }, { k: "BLOQUE", t: "Bloque / unidad del motor" },
      { k: "INDICADORES_BLOQUEADOS", t: "Indicadores que desbloquea", v: (f) => Number(f.INDICADORES_BLOQUEADOS) },
      { k: "N_ALTERNATIVAS_BLOQUEADAS", t: "Alternativas bloqueadas", v: (f) => `${f.N_ALTERNATIVAS_BLOQUEADAS}/${f.N_ALTERNATIVAS}` },
      { k: "EMPATE", t: "Empate", r: (f) => f.EMPATE ? h("span", { title: f.EMPATE }, etq("INFO", `empate (${f.N_EMPATADOS})`)) : "—" },
      { k: "DPV_VINCULADOS", t: "DPV" }], { nombre: "prioridad_validacion", alto: "420px" }),
    h("h2", {}, "Qué hacer ahora"), tabla(pr.que_hacer_ahora, [{ k: "RANK_COMPARTIDO", t: "Rank", v: (f) => Number(f.RANK_COMPARTIDO) }, { k: "QUE_HACER_AHORA", t: "Acción" }, { k: "DPV_VINCULADOS", t: "DPV" },
      { k: "RAZON", t: "Razón" }, { k: "EMPATE", t: "Empate", r: (f) => f.EMPATE ? etq("INFO", "empate") : "—" }, { k: "POTENCIAL_DE_CAMBIAR_DECISION", t: "¿Cambia la decisión?" }], { nombre: "que_hacer_ahora" }),
    h("p", { class: "mut peq" }, "Los empates se muestran como empates: la app no inventa desempates."),
    h("h2", {}, "Qué cambia en el motor con cada paquete"), h("ul", {}, plan.que_cambia.map((x) => h("li", {}, x))));
  const lista = h("div");
  async function pintarStaging() {
    try { const s = await api.get("/api/staging"); lista.replaceChildren(h("h3", {}, "Datos en staging"), h("p", { class: "mut peq" }, s.nota), tabla(s.filas, [{ k: "registrado", t: "Registrado" }, { k: "concepto", t: "Concepto" }, { k: "valor", t: "Valor" },
      { k: "unidad", t: "Unidad" }, { k: "moneda", t: "Moneda" }, { k: "fecha", t: "Fecha" }, { k: "fuente", t: "Fuente" }, { k: "tipo", t: "Tipo" }, { k: "estado_staging", t: "Estado", r: () => etq("STAGING") }], { nombre: "staging" })); }
    catch (e) { lista.replaceChildren(errorBox(e)); }
  }
  raiz.append(formularioStaging(pintarStaging), lista);
  pintarStaging();
  return raiz;
}
