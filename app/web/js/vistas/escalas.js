// ¿QUÉ SIGNIFICA 2.500 / 5.000 / 10.000 / 20.000 AVES POR DÍA?: solo datos ya modelados.
import { api } from "../api.js";
import { h, conf, num, ayuda } from "../ui.js";

const dec = (v) => (v === null || v === undefined ? 0 : Math.abs(v) < 10 ? 1 : 0);

export async function render() {
  const S = await api.get("/api/escalas");
  return h("div", { "data-escalas": "" },
    h("h1", {}, "📏 ¿Qué significa 2.500 / 5.000 / 10.000 / 20.000 aves por día?"),
    h("div", { class: "titular", "data-aviso-capacidad": "" }, "⚠ ", S.aviso),
    h("p", { class: "mut", style: { fontSize: "15px" } }, "La escala es cuántas aves puede faenar la planta en un día de trabajo. ", ayuda("ESCALA"), " ", S.nota),
    h("div", { class: "cards", style: { margin: "12px 0" } }, S.escalas.map((e, i) => h("div", { class: "card", style: { cursor: "default" }, "data-escala-card": e },
      h("span", { class: "t", style: { fontSize: "22px" } }, num(e)), h("span", { class: "d" }, "aves por día de planta"),
      ["aves_anio", "comestible_dia", "pollitos_semana", "galpones_eq", "demanda_t_dia"].map((id) => {
        const f = S.filas.find((x) => x.id === id);
        return f ? h("span", { class: "d" }, h("b", {}, num(f.valores[i], dec(f.valores[i])), " ", f.unidad), " — ", f.texto.toLowerCase()) : null;
      })))),
    h("div", { class: "tabla-env" }, h("table", { class: "t", "data-tabla-escalas": "" },
      h("thead", {}, h("tr", {}, h("th", {}, "Qué"), S.escalas.map((e) => h("th", { style: { textAlign: "right" } }, num(e))), h("th", {}, "Unidad"), h("th", {}, "Confianza"))),
      h("tbody", {}, S.filas.map((f) => h("tr", {}, h("td", {}, f.texto), f.valores.map((v) => h("td", { class: "num" }, num(v, dec(v)))), h("td", {}, f.unidad), h("td", {}, conf(f.etiqueta))))))),
    h("p", { class: "mut peq" }, S.base),
    h("div", { class: "panel" }, h("h3", {}, "Camiones de aves vivas por día"), h("p", { class: "peq" }, "Depende de cuántas aves entran en un camión, que todavía no está validado:"),
      h("ul", {}, S.camiones.map((cs, i) => h("li", {}, h("b", {}, num(S.escalas[i]), " aves/día: "), cs.map((c) => `${num(c.valor, 1)} camiones (${c.parametro.replace("aves_por_camion=", "")} aves por camión)`).join(" · "))))),
    h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/estudio/crecimiento" }, "Estrategia de crecimiento"), h("a", { class: "btn", href: "#/proceso" }, "Ver la planta por dentro"),
      h("a", { class: "btn", href: "#/estudio/demanda" }, "¿Hay demanda para eso?")));
}
