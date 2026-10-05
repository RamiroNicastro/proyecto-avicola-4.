// ¿DÓNDE ESTAMOS PARADOS?: qué está terminado, qué falta, qué se puede simular y qué no se puede decidir todavía.
import { api } from "../api.js";
import { h, sinRutas } from "../ui.js";

export function semaforoEstado(S) {
  return h("div", { class: "semaforo-estado", "data-semaforo-estado": "" }, S.semaforo.map((s) => h("div", { class: "sem-item", "data-sem": s.id },
    h("div", { class: "peq mut" }, s.titulo.toUpperCase()), h("div", { class: "e" }, s.icono, " ", s.estado), h("div", { class: "peq" }, s.texto))));
}

export async function render() {
  const S = await api.get("/api/estado_proyecto");
  const lista = (titulo, icono, xs, attr) => h("div", { class: "panel", [attr]: "" }, h("h2", {}, icono, " ", titulo), h("ul", { class: "sabemos" }, xs.map((x) => h("li", {}, x))));
  return h("div", { "data-estado-proyecto": "" }, h("h1", {}, "📊 ¿Dónde estamos parados?"),
    h("div", { class: "titular" }, S.intro), semaforoEstado(S),
    h("div", { class: "rejilla rejilla-2", style: { marginTop: "14px" } },
      lista("Lo que se puede simular hoy", "▶", S.se_puede_simular, "data-se-puede"),
      lista("Lo que todavía NO se puede decidir", "⛔", S.no_se_puede_decidir, "data-no-se-puede")),
    h("div", { class: "rejilla rejilla-2" },
      h("div", { class: "panel", "data-terminado": "" }, h("h2", {}, "✅ Terminado (como modelo, sin datos de campo)"),
        h("ul", { class: "sabemos" }, S.terminado.map((t) => h("li", {}, h("b", {}, sinRutas(t.modulo)), h("div", { class: "peq mut" }, sinRutas(t.texto).slice(0, 220)))))),
      h("div", { class: "panel", "data-pendiente": "" }, h("h2", {}, "⏳ Pendiente"),
        h("ul", { class: "sabemos" }, S.pendiente.map((t) => h("li", {}, h("b", {}, sinRutas(t.modulo)), h("div", { class: "peq mut" }, sinRutas(t.texto).slice(0, 220))))))),
    h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario btn-grande", href: "#/seguir" }, "Para seguir avanzando →"), h("a", { class: "btn btn-grande", href: "#/validacion" }, "Qué falta validar")));
}
