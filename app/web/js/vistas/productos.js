// ¿QUÉ SALE DE UN POLLO?: partes en kg por ave del balance existente; las rutas alternativas no se suman.
import { api } from "../api.js";
import { h, conf, num } from "../ui.js";

const nombre = (p) => p.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());
const CLASE_COLOR = { A: "var(--c1)", B: "var(--c3)", C: "var(--c2)", D: "var(--gris)", P: "var(--gris)" };

export async function render() {
  const P = await api.get("/api/productos_ave");
  const motor = P.balance_motor.filter((x) => x.kg_ave > 0).sort((a, b) => b.kg_ave - a.kg_ave);
  const max = Math.max(...motor.map((x) => x.kg_ave), 0.001);
  const porRuta = (r) => P.materiales.filter((m) => (m.configuracion || "").split(/[ /(]/).includes(r) || (r === "A" && /^A/.test(m.configuracion)));
  const fila = (m) => h("div", { class: "km-fila", style: { cursor: "default" }, "data-material": m.id },
    h("span", {}, m.material), h("div", { class: "km-barra" }, h("span", { style: { width: `${Math.min(100, Math.round(100 * m.kg_ave / 2))}%`, background: CLASE_COLOR[m.clase?.[0]] || "var(--acento)" } })),
    h("span", { class: "peq" }, num(m.kg_ave, 3), " kg"));
  return h("div", { "data-productos": "" },
    h("h1", {}, "🍗 ¿Qué sale de un pollo?"),
    h("p", { class: "mut", style: { fontSize: "15px" } }, "Un pollo vivo de 2,9 kg se convierte en varias partes. Cada parte puede ir a un mercado distinto: el objetivo es que el ingreso TOTAL por ave sea el mayor posible."),
    h("div", { class: "titular pend", "data-aviso-rutas": "" }, "⚠ ", P.aviso_rutas),
    h("div", { class: "panel" }, h("h2", {}, "Lo que vende el modelo (mix «trozado»)"), h("p", { class: "mut peq" }, "kg vendibles por ave en la configuración de productos que usa el motor financiero."),
      motor.map((x) => h("div", { class: "km-fila", style: { cursor: "default" }, "data-producto-motor": x.producto },
        h("span", {}, nombre(x.producto)), h("div", { class: "km-barra" }, h("span", { style: { width: `${Math.round(100 * x.kg_ave / max)}%` } })),
        h("span", { class: "peq" }, num(x.kg_ave, 3), " kg"))),
      h("p", { class: "peq mut" }, conf("ESTIMACION"), " Balance de masa del estudio (rendimientos de referencia; falta ensayo en una planta argentina).")),
    h("h2", {}, "Tres maneras de vender el mismo pollo"),
    h("div", { class: "rejilla rejilla-3" }, P.rutas.map((r) => h("div", { class: "panel", "data-ruta-producto": r.id }, h("h3", {}, r.titulo), h("p", { class: "peq" }, r.texto),
      porRuta(r.id).filter((m) => ["A", "B"].includes(m.clase?.[0])).map(fila)))),
    h("div", { class: "panel" }, h("h2", {}, "Coproductos y subproductos (salen en todas las rutas)"),
      P.materiales.filter((m) => /todas/.test(m.configuracion) && m.kg_ave).map(fila),
      h("p", { class: "peq mut" }, P.aviso_clase)),
    h("div", { class: "panel" }, h("h2", {}, "¿Qué no se puede sumar?"), h("ul", {}, P.materiales.filter((m) => m.incompatible).slice(0, 12).map((m) => h("li", {}, h("b", {}, m.material), ": ", m.incompatible)))),
    h("div", { class: "panel" }, h("h2", {}, "Clases de cada salida"), h("ul", { class: "sabemos" }, Object.entries(P.clases).map(([k, v]) => h("li", {}, h("span", { class: "chip", style: { borderLeft: `4px solid ${CLASE_COLOR[k]}` } }, k), " ", v)))),
    h("p", { class: "mut peq" }, P.base),
    h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/estudio/productos" }, "Entender los productos"), h("a", { class: "btn", href: "#/estudio/subproductos" }, "Subproductos y rendering"),
      h("a", { class: "btn", href: "#/estudio/exportacion" }, "Exportación")));
}
