// ¿QUÉ PASA DENTRO DE LA PLANTA?: etapas en orden, clicables; equipos de referencia, capacidad, servicios, riesgos y pendientes.
import { api } from "../api.js";
import { h, conf, num, ayuda } from "../ui.js";

let escalaSel = 10000;
let etapaSel = null;

export async function render(params, query) {
  if (query?.escala) escalaSel = Number(query.escala);
  const raiz = h("div", { "data-proceso": "" });
  async function dibujar() {
    const P = await api.get("/api/proceso?escala=" + escalaSel);
    const detalle = h("div", { class: "panel", "data-detalle-etapa": "" });
    const botones = [];
    function mostrar(e) {
      etapaSel = e.codigo;
      botones.forEach(([c, b]) => b.classList.toggle("sel", c === e.codigo));
      detalle.dataset.etapa = e.codigo;
      detalle.replaceChildren(h("div", { class: "peq mut" }, e.codigo), h("h2", { style: { marginTop: "2px" } }, e.nombre),
        h("div", { class: "preguntas" },
          h("div", { class: "pregunta" }, h("h2", {}, "Qué pasa"), h("p", {}, e.que_pasa), h("p", { class: "peq" }, h("b", {}, "Qué hay que controlar: "), e.controlar)),
          h("div", { class: "pregunta" }, h("h2", {}, "Riesgos"), h("p", {}, e.riesgo), e.salida_lateral && e.salida_lateral !== "—" ? h("p", { class: "peq" }, h("b", {}, "Qué sale aparte (kg por ave): "), e.salida_lateral) : null),
          h("div", { class: "pregunta" }, h("h2", {}, "Capacidad a ", num(escalaSel), " aves/día"),
            e.capacidad.length ? h("ul", { class: "sabemos" }, e.capacidad.map((c) => h("li", {}, conf(c.etiqueta), " ", c.texto, ": ", h("b", {}, num(c.valor, c.valor < 10 ? 1 : 0), " ", c.unidad))))
              : h("p", { class: "mut" }, "Sin cálculo de capacidad específico para esta etapa."),
            h("p", { class: "peq mut" }, "Es lo que la línea tiene que procesar, no la capacidad de una máquina.")),
          h("div", { class: "pregunta" }, h("h2", {}, "Agua y energía"), e.servicios.length ? h("div", { class: "chips" }, e.servicios.map((s) => h("span", { class: "chip" }, s))) : h("p", { class: "mut" }, "—"),
            h("p", { class: "peq mut" }, "Servicios que usan los equipos de referencia de esta etapa."))),
        h("h3", {}, "Equipos de referencia (", e.equipos.length, ")"),
        e.equipos.length ? h("ul", { class: "sabemos" }, e.equipos.map((q) => h("li", {}, conf(q.clasificacion), " ", h("b", {}, q.equipo), " — ", q.funcion,
          h("span", { class: "peq mut" }, ` · nivel a esta escala: ${P.niveles[q.nivel?.split("/")[0]] || q.nivel || "—"}${q.alternativas ? " · alternativas: " + q.alternativas : ""}`))))
          : h("p", { class: "mut" }, "Sin equipo específico."),
        h("div", { class: "aviso-rampa", "data-aviso-benchmark": "" }, P.aviso),
        h("h3", {}, "¿Qué está pendiente?"), e.pendiente.length ? h("p", {}, "Datos y decisiones abiertas: ", e.pendiente.join(", "), ". ", h("a", { href: "#/validacion" }, "Ver qué hay que validar")) : h("p", { class: "mut" }, "Sin pendientes específicos de esta etapa (además de las cotizaciones de equipos)."));
    }
    const lista = P.etapas.map((e) => {
      const b = h("button", { class: "etapa", "data-etapa": e.codigo, onclick: () => mostrar(e) }, h("span", { class: "c" }, e.codigo), h("div", { class: "t" }, e.nombre),
        h("div", { class: "peq mut" }, e.que_pasa));
      botones.push([e.codigo, b]);
      return b;
    });
    mostrar(P.etapas.find((e) => e.codigo === etapaSel) || P.etapas[0]);
    raiz.replaceChildren(h("h1", {}, "🏭 ¿Qué pasa dentro de la planta?"),
      h("p", { class: "mut", style: { fontSize: "15px" } }, "El pollo vivo entra por un lado y sale como carne refrigerada o congelada por el otro, pasando de zona «sucia» a zona «limpia» y a frío. Tocá cada etapa."),
      h("div", { class: "fila-btn" }, h("span", {}, "Escala:"), P.escalas.map((x) => h("button", { class: "btn" + (x === escalaSel ? " btn-primario" : ""), "data-escala-proceso": x,
        onclick: async () => { escalaSel = x; await dibujar(); } }, num(x) + " aves/día")), ayuda("ESCALA")),
      h("div", { class: "etapas", "data-etapas": "" }, lista), detalle,
      h("div", { class: "rejilla rejilla-2" },
        h("div", { class: "panel" }, h("h3", {}, "Lo que sale aparte por hora (", num(escalaSel), " aves/día, 8 h)"),
          h("ul", { class: "sabemos" }, P.laterales.map((l) => h("li", {}, conf(l.etiqueta), " ", l.variable, ": ", h("b", {}, num(l.valor), " kg/h")))),
          h("a", { class: "btn", href: "#/productos" }, "¿Qué sale de un pollo?")),
        h("div", { class: "panel" }, h("h3", {}, "Agua y energía de toda la planta"),
          h("ul", { class: "sabemos" }, P.utilities_planta.map((u) => h("li", {}, conf(u.etiqueta), " ", u.texto, ": ", h("b", {}, num(u.valor), " ", u.unidad)))),
          h("a", { class: "btn", href: "#/estudio/agua" }, "Agua y efluentes"), " ", h("a", { class: "btn", href: "#/estudio/energia" }, "Energía"))),
      h("p", { class: "mut peq" }, P.base, " ", P.niveles.nota));
  }
  await dibujar();
  return raiz;
}
