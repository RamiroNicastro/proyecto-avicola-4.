// VER DATOS / EVIDENCIA (#15): universo EVIDENCIA del proyecto, en solo lectura.
import { api } from "../api.js";
import { h, etq, etqOrigen, cargando, errorBox, tabla, bannerUniverso } from "../ui.js";
import { progreso } from "./validacion.js";
import { semaforoEstado } from "./estado.js";

export async function render() {
  const raiz = h("div", {}, h("h1", {}, "Datos reales / evidencia"), cargando());
  let r, est;
  try { [r, est] = await Promise.all([api.get("/api/evidencia"), api.get("/api/estado_proyecto")]); } catch (e) { raiz.lastChild.replaceWith(errorBox(e)); return raiz; }
  raiz.lastChild.remove();
  raiz.append(h("div", { class: "titular", "data-intro-evidencia": "" }, est.intro), semaforoEstado(est));
  const pub = Object.entries(r.publicables);
  raiz.append(bannerUniverso({ universo: "EVIDENCIA" }),
    h("div", { class: "panel" }, h("h2", {}, "¿Qué resultados del proyecto son publicables hoy?"),
      h("p", {}, `Umbral de evidencia: ${r.umbral.join(", ")} (DEC-084 abierta). Corridas del modo evidencia: ${r.corridas_evidencia}.`),
      h("div", { class: "rejilla rejilla-auto" }, pub.map(([k, n]) => h("div", { class: "tarjeta", "data-flag": k }, h("div", { class: "peq mut" }, k.replace("PUBLICABLE_", "")),
        h("div", { style: { fontSize: "20px", fontWeight: 700 } }, `${n} / ${r.corridas_evidencia}`), n ? etq("EVIDENCIA") : etq("NO_CALCULABLE", "sin evidencia suficiente")))),
      h("p", { class: "mut" }, r.optimizador_evidencia?.[0] ? `Optimizador en evidencia: ${r.optimizador_evidencia[0].ESTADO} — ${r.optimizador_evidencia[0].POR_QUE || ""}` : "")),
    progreso(r.progreso),
    h("h2", {}, "Precios de venta (base_precios_venta.csv)"),
    tabla(r.precios, [{ k: "ID_PRECIO", t: "ID" }, { k: "PRODUCTO", t: "Producto" }, { k: "CANAL", t: "Canal" }, { k: "MERCADO", t: "Mercado" },
      { k: "PRECIO", t: "Precio", r: (f) => f.PRECIO ? `${f.PRECIO} ${f.MONEDA} / ${f.UNIDAD}` : etq("PENDIENTE") }, { k: "NIVEL_EVIDENCIA", t: "Nivel" },
      { k: "ESTADO", t: "Estado" }, { k: "FUENTE", t: "Fuente" }, { k: "DPV", t: "DPV" }], { nombre: "precios_evidencia", alto: "380px" }),
    h("h2", {}, "Inputs financieros del modo evidencia"), h("p", { class: "mut peq" }, Object.entries(r.inputs_resumen).map(([k, v]) => `${k}: ${v}`).join(" · ")),
    tabla(r.inputs, [{ k: "ID_INPUT", t: "ID" }, { k: "BLOQUE", t: "Bloque" }, { k: "VARIABLE", t: "Variable" }, { k: "VALOR", t: "Valor", r: (f) => f.VALOR || etq("PENDIENTE") },
      { k: "UNIDAD", t: "Unidad" }, { k: "ORIGEN", t: "Origen", r: (f) => etqOrigen(f.ORIGEN) }, { k: "NIVEL_EVIDENCIA", t: "Nivel" }, { k: "OBSERVACIONES", t: "Observaciones" }],
    { nombre: "inputs_evidencia", alto: "420px" }),
    h("p", { class: "mut" }, r.nota),
    h("p", {}, "Datos cargados a mano: ", h("a", { href: "#/validacion" }, "STAGING (en Validación)"), " — ", etq("STAGING"), "."));
  return raiz;
}
