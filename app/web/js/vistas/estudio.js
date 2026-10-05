// ENTENDER EL PROYECTO: índice «Estudio completo», páginas de grupo y ficha de cada módulo (5 preguntas).
import { api } from "../api.js";
import { E } from "../estado.js";
import { h, cargando, errorBox, conf, modal, sinRutas, ayuda } from "../ui.js";
import { markdown } from "../md.js";

// Pantallas visuales que amplían cada grupo (botón destacado).
const DESTACADAS = {
  mercado: [["como-funciona", "🔗", "¿Cómo funciona el negocio?", "La cadena del huevo al cliente, bloque por bloque."]],
  produccion: [["como-funciona", "🔗", "¿Cómo funciona el negocio?", "Pollito → crianza → alimento → granjas → transporte."],
    ["escalas", "📏", "¿Qué significa cada escala?", "Pollitos, alimento y galpones para 2.500 a 20.000 aves/día."]],
  planta: [["proceso", "🏭", "¿Qué pasa dentro de la planta?", "Las etapas de la faena en orden, con equipos, capacidad y riesgos."]],
  productos: [["productos", "🍗", "¿Qué sale de un pollo?", "Cada parte en kg por ave y a dónde puede ir."]],
  localizacion: [["localizacion", "📍", "¿Dónde podría estar la planta?", "Regiones, criterios y qué falta saber."]],
  infraestructura: [["escalas", "📏", "¿Qué significa cada escala?", "Agua, energía, superficie y terreno por escala."]],
  inversion: [["arquitecturas", "🧩", "Las 5 arquitecturas", "Qué es propio y qué tercerizado en C0, C1, C2, C3 y CF."],
    ["escalas", "📏", "¿Qué significa cada escala?", "2.500 / 5.000 / 10.000 / 20.000 aves por día."]],
  finanzas: [["simular", "▶", "Simular un escenario", "Cargá tus datos y mirá un resultado (rotulado como simulación)."]],
  riesgos: [["riesgos", "⚠", "Probar riesgos", "¿Qué pasa si sube el alimento o baja el precio?"], ["optimizar", "◎", "Optimizar", "Buscar la alternativa que mejor cumple tu objetivo."]],
  logistica: [["como-funciona", "🔗", "¿Cómo funciona el negocio?", "Dónde entra la logística en la cadena."]],
  organizacion: [["estado", "📊", "¿Dónde estamos parados?", "Qué está terminado y qué falta."]],
  costos: [["simular", "▶", "Simular un escenario", "Probá con tus propios precios de alimento y pollitos."]],
};

export function tarjetaDestacada([ruta, i, t, d]) {
  return h("a", { class: "card destacada", href: "#/" + ruta, "data-ir": ruta }, h("span", { class: "i" }, i), h("span", { class: "t" }, t), h("span", { class: "d" }, d));
}
export function tarjetaModulo(m) {
  return h("a", { class: "card", href: "#/estudio/" + m.id, "data-modulo": m.id }, h("span", { class: "i" }, m.icono), h("span", { class: "t" }, m.titulo),
    h("span", { class: "d" }, m.resumen), h("span", { class: "chips" }, m.chips.map((c) => conf(c.etiqueta, c.n))));
}

function leyendaConfianza() {
  return h("div", { class: "chips", "data-leyenda-confianza": "" }, ["VERIFICADO", "ESTIMACION", "SUPUESTO", "PVDP", "PENDIENTE"].map((k) => conf(k)),
    h("span", { class: "peq mut" }, " — cómo de seguro es cada dato. Hoy ningún dato del proyecto está validado en campo."));
}

async function indice() {
  const ix = E.estudio || await api.get("/api/estudio");
  return h("div", {}, h("h1", {}, "📚 Estudio completo"),
    h("p", { class: "mut" }, "Todos los temas del estudio, explicados en lenguaje simple. Elegí uno para ver qué es, por qué importa, qué se modeló, qué se sabe hoy y qué falta validar."),
    leyendaConfianza(),
    h("div", { class: "cards", "data-estudio-completo": "", style: { marginTop: "14px" } }, ix.estudio_completo.map((x) =>
      h("a", { class: "card", href: "#/estudio/" + x.modulo, "data-tema": x.tema }, h("span", { class: "i" }, x.icono), h("span", { class: "t" }, x.tema),
        x.tema !== x.titulo ? h("span", { class: "d" }, "en: " + x.titulo) : null))),
    ["PROYECTO", "ECONOMIA"].map((sec) => h("div", {}, h("h2", {}, sec === "PROYECTO" ? "Proyecto" : "Economía"),
      h("div", { class: "cards" }, ix.grupos.filter((g) => g.seccion === sec).map((g) => h("a", { class: "card", href: "#/grupo/" + g.id, "data-grupo": g.id },
        h("span", { class: "t" }, g.titulo), h("span", { class: "d" }, g.texto), h("span", { class: "d" }, `${g.modulos.length} tema(s)`)))))));
}

async function grupo(id) {
  const ix = E.estudio || await api.get("/api/estudio");
  const g = ix.grupos.find((x) => x.id === id);
  if (!g) return h("div", {}, h("h1", {}, "Tema no encontrado"), h("a", { class: "btn", href: "#/estudio" }, "Ver el estudio completo"));
  return h("div", { "data-pagina-grupo": id }, h("h1", {}, g.titulo), h("p", { class: "mut", style: { fontSize: "15px" } }, g.texto),
    (DESTACADAS[id] || []).length ? h("div", { class: "cards", style: { margin: "14px 0" } }, DESTACADAS[id].map(tarjetaDestacada)) : null,
    h("h2", {}, "Temas"), h("div", { class: "cards" }, g.modulos.map(tarjetaModulo)), h("div", { style: { marginTop: "12px" } }, leyendaConfianza()));
}

function verFuentes(m) {
  modal(h("div", { "data-fuentes": m.id }, h("h2", {}, "Fuentes de «" + m.titulo + "»"),
    h("p", {}, "Este resumen sale de los documentos del estudio:"), h("ul", {}, m.detalle_tecnico.documentos.map((d) => h("li", {}, d.titulo))),
    h("h3", {}, "Qué tan seguro es cada dato"), h("ul", { class: "sabemos" }, Object.entries(E.estudio?.confianza || {}).map(([k, v]) => h("li", {}, conf(k), " ", v))),
    h("p", { class: "mut peq" }, "Las fuentes externas (organismos, prensa, fabricantes) están registradas con su identificador en el registro de fuentes del proyecto; se ven en el modo experto.")));
}

function detalleTecnico(m) {
  const zona = h("div", { class: "md" });
  let cargado = false;
  const cargar = async (ruta) => {
    zona.replaceChildren(cargando("Abriendo el documento…"));
    try { const d = await api.get("/api/doc_estudio?ruta=" + encodeURIComponent(ruta)); zona.innerHTML = markdown(d.texto); }
    catch (e) { zona.replaceChildren(errorBox(e)); }
  };
  const docs = m.detalle_tecnico.documentos;
  return h("details", { class: "acordeon", "data-detalle-tecnico": "", ontoggle: (e) => { if (e.target.open && !cargado) { cargado = true; cargar(docs[0].ruta); } } },
    h("summary", {}, "🔧 Ver detalle técnico"),
    h("p", { class: "mut peq" }, "Documento original del estudio (lenguaje técnico)."),
    docs.length > 1 ? h("div", { class: "fila-btn" }, docs.map((d) => h("button", { class: "btn", onclick: () => cargar(d.ruta) }, d.titulo))) : null, zona);
}

const LISTO = { TRUE: "Sí", FALSE: "No" };
async function ficha(mid) {
  let m;
  try { m = await api.get("/api/estudio/" + encodeURIComponent(mid)); } catch (e) { return h("div", {}, errorBox(e), h("a", { class: "btn", href: "#/estudio" }, "Ver el estudio completo")); }
  const p = Object.fromEntries(m.preguntas.map((x) => [x.id, x]));
  const pregunta = (id, contenido, attrs = {}) => h("section", { class: "pregunta", "data-pregunta": id, ...attrs }, contenido);
  return h("div", { "data-ficha-modulo": m.id },
    h("div", { class: "hero" }, h("div", { style: { fontSize: "40px" } }, m.icono), h("h1", {}, m.titulo), h("p", {}, m.resumen),
      h("div", { class: "chips" }, m.chips.map((c) => conf(c.etiqueta, c.n))),
      h("div", { class: "fila-btn" }, m.vista ? h("a", { class: "btn btn-primario btn-grande", href: "#/" + m.vista.ruta, "data-ir-vista": m.vista.ruta }, m.vista.texto + " →") : null,
        h("button", { class: "btn", "data-ver-fuentes": "", onclick: () => verFuentes(m) }, "📎 Ver fuentes"))),
    h("div", { class: "preguntas" },
      pregunta("que_es", [h("h2", {}, "¿Qué es?"), h("p", {}, p.que_es.texto)]),
      pregunta("por_que", [h("h2", {}, "¿Por qué importa?"), h("p", {}, p.por_que.texto)]),
      pregunta("que_modelamos", [h("h2", {}, "¿Qué modelamos?"), h("p", {}, p.que_modelamos.texto)])),
    h("div", { class: "preguntas", style: { marginTop: "12px" } },
      pregunta("que_sabemos", [h("h2", {}, "¿Qué sabemos hoy?"), h("ul", { class: "sabemos" }, m.que_sabemos.map((x) => h("li", {}, conf(x.etiqueta), " ", x.texto))),
        h("p", { class: "mut peq" }, "Ningún dato está validado en campo todavía.")]),
      pregunta("que_falta", [h("h2", {}, "¿Qué falta validar?"),
        m.que_falta.length ? h("ul", { class: "check" }, m.que_falta.map((d) => h("li", { "data-dpv": d.id }, h("span", { class: "caja", "aria-hidden": "true" }, /^validad/i.test(d.estado) ? "☑" : "☐"),
          h("div", {}, h("div", {}, sinRutas(d.dato)), h("div", { class: "peq mut" }, d.por_que ? "Por qué importa: " + sinRutas(d.por_que) + " · " : "", "Estado: ", d.estado, " · ", d.id)))))
          : h("p", { class: "mut" }, "Sin datos registrados para este tema."),
        m.decisiones.length ? h("div", {}, h("h3", {}, "Decisiones abiertas"), h("ul", {}, m.decisiones.map((d) => h("li", {}, sinRutas(d.decision), h("span", { class: "peq mut" }, ` (${d.estado} · ${d.id})`))))) : null,
        h("a", { class: "btn", href: "#/validacion" }, "Ver el checklist completo de validación")])),
    m.completitud ? h("div", { class: "panel" }, h("h3", {}, "Estado de este módulo en el motor"),
      h("p", {}, "Modelo: ", h("b", {}, m.completitud.estado_motor.replace(/_/g, " ").toLowerCase()), " · ¿Sirve para decidir con datos reales? ", h("b", {}, LISTO[m.completitud.listo_decision_real] || m.completitud.listo_decision_real),
        " ", ayuda("EVIDENCIA"))) : null,
    detalleTecnico(m));
}

export async function render(params, query, r) {
  if (r === "grupo") return grupo(params[0]);
  if (params[0]) return ficha(params[0]);
  return indice();
}
