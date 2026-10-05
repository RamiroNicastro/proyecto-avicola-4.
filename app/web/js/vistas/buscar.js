// Resultados de la búsqueda global (índice de temas, pantallas, regiones y términos).
import { api } from "../api.js";
import { h, vacio } from "../ui.js";

export async function render(params, query) {
  const q = query?.q || "";
  const R = q ? await api.get("/api/buscar?q=" + encodeURIComponent(q)) : { resultados: [] };
  const destino = (x) => (x.tipo === "TERMINO" ? "#/diccionario?q=" + encodeURIComponent(x.q) : "#/" + x.ruta);
  return h("div", { "data-busqueda": q }, h("h1", {}, "🔎 Resultados para «", q, "»"),
    R.resultados.length ? h("div", { class: "cards" }, R.resultados.map((x) => h("a", { class: "card", href: destino(x), "data-resultado-busqueda": x.ruta },
      h("span", { class: "peq mut" }, { VISTA: "Pantalla", MODULO: "Tema del estudio", REGION: "Región", TERMINO: "Diccionario" }[x.tipo]), h("span", { class: "t" }, x.titulo), h("span", { class: "d" }, x.texto))))
      : vacio("🔎", "No encontramos resultados. Probá con palabras como: localización, agua, faena, 10.000, CAPEX, pollitos, Chaco o halal.", "VER EL ESTUDIO COMPLETO", "#/estudio"));
}
