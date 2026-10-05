// LAS 5 ARQUITECTURAS en lenguaje humano: qué es PROPIO / TERCERIZADO / MIXTO / FUTURO (definiciones exactas debajo).
import { api } from "../api.js";
import { h, ayuda } from "../ui.js";

const ICONO = { PROPIO: "■ Propio", TERCERIZADO: "□ Tercerizado", MIXTO: "◧ Mixto", FUTURO: "◌ Futuro", "NO TIENE": "– No tiene" };

export async function render() {
  const A = await api.get("/api/arquitecturas");
  const dims = A.arquitecturas[0].dimensiones.map((d) => [d.id, d.titulo]);
  return h("div", { "data-arquitecturas": "" },
    h("h1", {}, "🧩 Las 5 arquitecturas"),
    h("p", { class: "mut", style: { fontSize: "15px" } }, "Una arquitectura dice qué partes del negocio hace la empresa con activos propios y cuáles contrata a terceros. ", ayuda("ASSET-LIGHT"), " ", ayuda("FAÇON")),
    h("div", { class: "cards" }, A.arquitecturas.map((a) => h("div", { class: "card", style: { cursor: "default" }, "data-arq": a.id },
      h("span", { class: "peq mut" }, a.id), h("span", { class: "t" }, a.nombre), h("span", { class: "d" }, a.explicacion),
      h("ul", { class: "sabemos peq" }, a.dimensiones.map((d) => h("li", { "data-dim": d.id }, h("b", {}, d.titulo, ": "), ICONO[d.clase] || d.clase,
        h("details", { style: { display: "inline-block", border: "none", padding: "0 4px", margin: 0 } }, h("summary", { class: "peq mut", style: { fontWeight: 400 } }, "definición"), h("span", { class: "peq" }, d.definicion)))))))),
    h("h2", {}, "Comparación rápida"),
    h("div", { class: "tabla-env" }, h("table", { class: "t arq-tabla" }, h("thead", {}, h("tr", {}, h("th", {}, ""), A.arquitecturas.map((a) => h("th", {}, a.id, h("div", { class: "peq" }, a.nombre))))),
      h("tbody", {}, dims.map(([id, t]) => h("tr", {}, h("td", {}, h("b", {}, t)), A.arquitecturas.map((a) => {
        const d = a.dimensiones.find((x) => x.id === id);
        return h("td", { class: d.clase.replace(" ", "_"), title: d.definicion }, ICONO[d.clase] || d.clase);
      })))))),
    h("div", { class: "fila-btn" }, Object.entries(A.leyenda).map(([k, v]) => h("span", { class: "chip" }, h("b", {}, ICONO[k], ": "), v))),
    h("div", { class: "titular pend" }, "Ninguna arquitectura está recomendada ni se puede costear todavía: faltan precios y cotizaciones."),
    h("p", { class: "mut peq" }, "Las definiciones exactas son las del mapa de arquitecturas del estudio (se ven al desplegar «definición»)."),
    h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/simular" }, "Probar una arquitectura en una simulación"), h("a", { class: "btn", href: "#/escalas" }, "¿Qué significa cada escala?")));
}
