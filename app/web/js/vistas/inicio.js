// Pantalla inicial (#3): ¿QUÉ QUERÉS HACER?
import { api } from "../api.js";
import { E, setEscenario } from "../estado.js";
import { h, etq, toast } from "../ui.js";
import { barraProgreso } from "../graficos.js";

const ACCIONES = [
  ["simular", "▶", "Simular un negocio", "Cargá capital, demanda y precios; el motor calcula el resultado del escenario."],
  ["comparar", "⇄", "Comparar alternativas", "Poné 2 a 5 configuraciones y escalas lado a lado."],
  ["optimizar", "◎", "Optimizar", "Buscá la mejor alternativa del escenario según tu objetivo y restricciones."],
  ["riesgos", "⚠", "Ver riesgos", "¿Qué pasa si sube el alimento o baja el precio? Stress, quiebres, Monte Carlo."],
  ["validacion", "✓", "Qué me falta validar", "Paquetes de validación, a quién pedir qué y qué desbloquea."],
  ["evidencia", "▤", "Ver datos / evidencia", "Qué datos reales hay hoy (y cuáles faltan)."],
  ["experto", "⚙", "Modo experto", "Todos los inputs del motor por pestañas, trazabilidad y JSON."],
];

export async function render() {
  const p = E.estado?.progreso;
  const demo = h("div", { class: "panel" }, h("h3", {}, "¿Primera vez?"),
    h("p", {}, "Abrí el escenario ", h("b", {}, "DEMO_ARTIFICIAL"), " para ver todas las funciones con datos ", h("b", {}, "completamente ficticios"), " ", etq("DEMO"), "."),
    h("div", { class: "fila-btn" }, h("button", { class: "btn", "data-abrir-demo": "", onclick: async () => {
      setEscenario(await api.get("/api/escenarios/demo_artificial"), false); toast("Demo abierta: datos ficticios (SOLO_DEMOSTRACION)."); location.hash = "#/simular";
    } }, "Abrir demo"), h("button", { class: "btn", onclick: async () => {
      setEscenario(await api.post("/api/nuevo", { nombre: "Escenario nuevo" }), true); location.hash = "#/simular";
    } }, "Empezar un escenario vacío")));
  return h("div", {},
    h("div", { class: "home-pregunta" }, "¿Qué querés hacer?"),
    h("div", { class: "acciones-home" }, ACCIONES.map(([r, i, t, d]) => h("button", { class: "accion-home", "data-ir": r, onclick: () => { location.hash = "#/" + r; } },
      h("span", { class: "i", "aria-hidden": "true" }, i), h("span", { class: "t" }, t), h("span", { class: "d" }, d)))),
    h("div", { class: "rejilla rejilla-2", style: { marginTop: "18px" } }, demo,
      p ? h("div", { class: "panel" }, h("h3", {}, "Estado del proyecto"),
        h("div", { class: "progreso" }, p.dimensiones.map((d) => h("div", { class: "dim" }, h("span", {}, h("b", {}, d.titulo)), barraProgreso(d.pct),
          h("span", { class: "peq" }, d.estado)))),
        h("p", { class: "peq mut" }, "Cada dimensión se mide por separado; no hay una barra única. Detalle en VALIDACIÓN."),
        h("div", { class: "fila-btn" }, Object.entries(p.estado_general).map(([k, v]) => h("span", { class: "chip" }, `${k} = ${v}`)))) : null));
}
