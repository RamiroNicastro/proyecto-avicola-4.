// INICIO: qué es la herramienta, cuatro acciones grandes, dónde estamos y accesos a las preguntas clave.
import { api } from "../api.js";
import { setEscenario } from "../estado.js";
import { h, toast } from "../ui.js";
import { semaforoEstado } from "./estado.js";
import { empezarTour } from "../tour.js";

const ACCIONES = [
  ["estudio", "📚", "Entender el proyecto", "Qué es cada parte del negocio, qué se estudió y qué se sabe hoy. En lenguaje simple."],
  ["simular", "▶", "Simular un escenario", "Respondé 5 preguntas y mirá qué pasaría con esos datos (es una simulación, no un dato real)."],
  ["optimizar", "◎", "Comparar / optimizar", "Poné alternativas lado a lado o buscá la que mejor cumple tu objetivo."],
  ["validacion", "☐", "Qué falta validar", "La lista de datos que hay que conseguir, a quién pedírselos y qué destraban."],
];
const PREGUNTAS = [
  ["como-funciona", "🔗", "¿Cómo funciona el negocio?", "Del huevo al cliente, bloque por bloque."],
  ["localizacion", "📍", "¿Dónde podría estar la planta?", "Regiones, criterios y qué falta saber."],
  ["proceso", "🏭", "¿Qué pasa dentro de la planta?", "Las etapas de la faena, una por una."],
  ["productos", "🍗", "¿Qué sale de un pollo?", "Cada parte en kg por ave."],
  ["arquitecturas", "🧩", "Las 5 arquitecturas", "Qué es propio y qué se terceriza."],
  ["escalas", "📏", "¿Qué significa cada escala?", "2.500 a 20.000 aves por día."],
];

export async function render() {
  let estado = null;
  try { estado = await api.get("/api/estado_proyecto"); } catch (e) { estado = null; }
  return h("div", { "data-home": "" },
    h("div", { class: "hero" }, h("h1", { "data-titulo-home": "" }, "PROYECTO AVÍCOLA — NICAS & DOIPE"),
      h("p", {}, "Esta herramienta reúne el estudio completo para analizar una cadena avícola: producción, planta, logística, inversiones, costos, rentabilidad y riesgos.")),
    h("div", { class: "acciones-grandes" }, ACCIONES.map(([r, i, t, d]) => h("a", { class: "accion-grande", href: "#/" + r, "data-accion": r },
      h("span", { class: "i", "aria-hidden": "true" }, i), h("span", { class: "t" }, t), h("span", { class: "d" }, d)))),
    estado ? h("div", { class: "panel", "data-home-estado": "" }, h("h2", {}, "¿Dónde estamos parados?"), h("p", {}, estado.intro), semaforoEstado(estado),
      h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/estado", "data-ir": "estado" }, "Ver el estado completo →"), h("a", { class: "btn", href: "#/seguir" }, "Para seguir avanzando"))) : null,
    h("h2", {}, "Preguntas para entender el proyecto"),
    h("div", { class: "cards" }, PREGUNTAS.map(([r, i, t, d]) => h("a", { class: "card", href: "#/" + r, "data-ir": r }, h("span", { class: "i" }, i), h("span", { class: "t" }, t), h("span", { class: "d" }, d)))),
    h("div", { class: "panel", style: { marginTop: "18px" } }, h("h2", {}, "¿Primera vez?"),
      h("p", {}, "Hacé el recorrido de 2 minutos con la DEMO (datos completamente ficticios) o empezá un escenario propio desde cero."),
      h("div", { class: "fila-btn" },
        h("button", { class: "btn btn-primario", "data-recorrido": "", onclick: () => empezarTour() }, "Recorrido de 2 minutos"),
        h("button", { class: "btn", "data-abrir-demo": "", onclick: async () => { setEscenario(await api.get("/api/escenarios/demo_artificial"), false); toast("Demo abierta: datos ficticios."); location.hash = "#/simular"; } }, "Abrir la demo"),
        h("button", { class: "btn", "data-escenario-vacio": "", onclick: async () => { setEscenario(await api.post("/api/nuevo", { nombre: "Escenario nuevo" }), true); location.hash = "#/simular"; } }, "Empezar un escenario vacío"))),
    h("div", { class: "secundarias", style: { marginTop: "14px" } }, h("span", { class: "mut peq" }, "Avanzado:"),
      h("a", { class: "btn-link peq", href: "#/experto" }, "Modo experto"), h("a", { class: "btn-link peq", href: "#/evidencia" }, "Evidencia"), h("a", { class: "btn-link peq", href: "#/diccionario" }, "Diccionario")));
}
