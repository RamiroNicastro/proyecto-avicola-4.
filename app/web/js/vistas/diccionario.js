// DICCIONARIO: glosario del proyecto (00_gestion_proyecto/glosario.md) + ayudas breves, con búsqueda.
import { api } from "../api.js";
import { h } from "../ui.js";

const norm = (s) => String(s || "").toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

export async function render(params, query) {
  const G = await api.get("/api/glosario");
  const lista = h("div", { "data-terminos": "" });
  const info = h("p", { class: "mut peq" });
  const inp = h("input", { type: "search", placeholder: "Buscá un término: VAN, FCR, façon, rendering…", value: query?.q || "", "data-buscar-glosario": "",
    style: { width: "100%", maxWidth: "520px", fontSize: "15px", padding: "10px 14px", borderRadius: "999px" }, oninput: () => pintar() });
  function pintar() {
    const q = norm(inp.value.trim());
    const fs = G.terminos.filter((t) => !q || norm(t.termino).includes(q) || norm(t.definicion).includes(q))
      .sort((a, b) => (q ? (norm(b.termino).includes(q) - norm(a.termino).includes(q)) : 0));
    info.textContent = `${fs.length} de ${G.terminos.length} términos`;
    lista.replaceChildren(...fs.slice(0, 200).map((t) => h("div", { class: "panel", "data-termino": t.termino, style: { margin: "8px 0" } },
      h("b", { style: { fontSize: "15px" } }, t.termino), h("p", {}, t.definicion))),
    fs.length ? null : h("div", { class: "vacio", "data-vacio": "" }, h("div", { class: "i" }, "📖"), h("p", {}, "No encontramos ese término. Probá con otra palabra o buscalo en todo el proyecto."),
      h("a", { class: "btn btn-primario", href: "#/buscar?q=" + encodeURIComponent(inp.value), "data-cta": "" }, "BUSCAR EN TODO EL PROYECTO")));
  }
  pintar();
  return h("div", {}, h("h1", {}, "📖 Diccionario"), h("p", { class: "mut" }, "Los términos técnicos del proyecto explicados en pocas palabras."), inp, info, lista);
}
