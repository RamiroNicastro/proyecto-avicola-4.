// ¿CÓMO FUNCIONA EL NEGOCIO?: la cadena avícola clicable, con sus ramas (subproductos, efluentes, rendering, exportación).
import { api } from "../api.js";
import { h, conf } from "../ui.js";

export async function render() {
  const c = await api.get("/api/cadena");
  const detalle = h("div", { class: "panel", "data-detalle-eslabon": "" });
  let sel = null;
  const botones = new Map();
  function mostrar(n) {
    sel = n.id;
    botones.forEach((b, id) => b.classList.toggle("sel", id === sel));
    detalle.dataset.eslabon = n.id;
    detalle.replaceChildren(h("h2", {}, n.icono, " ", n.titulo), h("p", { style: { fontSize: "15px" } }, n.texto),
      n.numeros.length ? h("div", {}, h("h3", {}, "Números del estudio"), h("ul", { class: "sabemos" }, n.numeros.map((x) => h("li", {}, conf(x.etiqueta), " ", x.texto))))
        : h("p", { class: "mut" }, "Todavía no hay números para este bloque."),
      h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/estudio/" + n.modulo }, "Entender «" + n.modulo_titulo + "» →"),
        n.id === "faena" || n.id === "enfriamiento" || n.id === "empaque" ? h("a", { class: "btn", href: "#/proceso" }, "Ver las etapas de la planta") : null,
        n.id === "trozado" ? h("a", { class: "btn", href: "#/productos" }, "¿Qué sale de un pollo?") : null));
  }
  const boton = (n, rama) => {
    const b = h("button", { class: "eslabon" + (rama ? " rama" : ""), "data-eslabon": n.id, onclick: () => mostrar(n) }, h("span", { class: "i" }, n.icono), h("span", { class: "t" }, n.titulo));
    botones.set(n.id, b);
    return b;
  };
  const fila = [];
  c.nodos.forEach((n, i) => { if (i) fila.push(h("span", { class: "flecha", "aria-hidden": "true" }, "→")); fila.push(boton(n)); });
  mostrar(c.nodos.find((n) => n.id === "faena") || c.nodos[0]);
  return h("div", {}, h("h1", {}, "🔗 ¿Cómo funciona el negocio?"),
    h("p", { class: "mut", style: { fontSize: "15px" } }, "Del huevo al cliente. Tocá cada bloque para ver qué es y qué números tiene el estudio."),
    h("div", { class: "panel" }, h("div", { class: "cadena", "data-cadena": "" }, fila)),
    h("div", { class: "panel" }, h("h3", {}, "Ramas que salen de la cadena"),
      h("div", { class: "cadena" }, c.ramas.map((r) => [h("span", { class: "peq mut", style: { alignSelf: "center" } }, "desde " + (c.nodos.find((n) => n.id === r.padre)?.titulo || r.padre) + " ↘"), boton(r, true)]))),
    detalle, h("p", { class: "mut peq" }, c.nota));
}
