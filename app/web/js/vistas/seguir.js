// PARA SEGUIR AVANZANDO: qué hacer ahora, por prioridad del motor (empates conservados: «PRIORIDAD 1 — EMPATE»).
import { api } from "../api.js";
import { h, sinRutas } from "../ui.js";

export async function render() {
  const S = await api.get("/api/seguir");
  const grupo = (g, abierto) => h("details", { class: "acordeon", open: abierto, "data-prioridad": g.rank }, h("summary", {}, g.titulo),
    g.empate ? h("p", { class: "peq mut" }, "Estos pedidos están empatados: el motor no puede decir cuál conviene primero, así que se muestran juntos y sin orden.") : null,
    h("ul", { class: "check" }, g.items.map((x) => h("li", {}, h("span", { class: "caja", "aria-hidden": "true" }, "☐"),
      h("div", {}, h("b", {}, sinRutas(x.accion)), h("div", { class: "peq mut" }, "Qué falta: ", sinRutas(x.item)), h("div", { class: "peq mut" }, "Por qué: ", x.razon, x.dpv.length ? " · " + x.dpv.join(", ") : ""))))));
  return h("div", { "data-seguir": "" }, h("h1", {}, "→ Para seguir avanzando"),
    h("p", { class: "mut", style: { fontSize: "15px" } }, "Qué hacer ahora para pasar de simulaciones a decisiones reales. Primero, lo que destraba más resultados."),
    S.grupos.map((g, i) => grupo(g, i < 2)),
    h("p", { class: "mut peq" }, sinRutas(S.nota)),
    h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario btn-grande", href: "#/validacion" }, "Ver el checklist por tema (a quién pedir qué)")));
}
