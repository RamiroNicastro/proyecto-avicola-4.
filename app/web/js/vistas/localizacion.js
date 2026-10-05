// ¿DÓNDE PODRÍA ESTAR LA PLANTA?: regiones en estudio, criterios, gates y estado de la información. Sin ranking inventado.
import { api } from "../api.js";
import { h, conf, num, modal } from "../ui.js";

export async function render() {
  const L = await api.get("/api/localizacion");
  const maxKm = Math.max(...L.regiones.map((r) => r.km_caba_orden || 0), 1);
  const fichaRegion = (r) => modal(h("div", { "data-ficha-region": r.codigo }, h("h2", {}, `📍 ${r.centro} — ${r.provincia}`), h("p", { class: "mut" }, r.corredor),
    h("p", {}, h("b", {}, "Lógica: "), r.logica),
    r.que_gana ? h("p", {}, h("b", {}, "Qué gana: "), r.que_gana) : null, r.que_arriesga ? h("p", {}, h("b", {}, "Qué arriesga: "), r.que_arriesga) : null,
    r.preguntas ? h("p", {}, h("b", {}, "Preguntas que la decidirían: "), r.preguntas) : null,
    h("p", {}, h("b", {}, "Información cargada: "), `${r.con_dato} de ${r.celdas} criterios con algún dato (ninguno verificado).`),
    h("p", { class: "mut peq" }, "Distancia a CABA ≈ ", num(r.km_caba_orden), " km: orden de magnitud no medido.")));
  return h("div", { "data-localizacion": "" },
    h("h1", {}, "📍 ¿Dónde podría estar la planta?"),
    h("div", { class: "titular pend", "data-sin-ganadora": "" }, "⛔ ", L.mensaje),
    h("p", { class: "mut", style: { fontSize: "15px" } }, `Se estudian ${L.regiones.length} regiones de Buenos Aires, Entre Ríos, Santa Fe, Córdoba y Chaco. Ninguna está descartada ni preferida. `,
      `De ${L.celdas.total} datos necesarios para comparar regiones, ${L.celdas.verificadas} están verificados y ${L.celdas.por_estado.SIN_DATO || 0} están vacíos.`),
    h("div", { class: "rejilla rejilla-2" },
      h("div", { class: "panel" }, h("h2", {}, "Regiones en estudio"), h("p", { class: "mut peq" }, "Esquema de distancia aproximada a la Ciudad de Buenos Aires (no es un mapa ni un puntaje). Tocá una región."),
        L.regiones.map((r) => h("div", { class: "km-fila", "data-region": r.codigo, onclick: () => fichaRegion(r), role: "button", tabindex: 0 },
          h("span", {}, h("b", {}, r.centro), h("span", { class: "peq mut" }, " · " + r.provincia)),
          h("div", { class: "km-barra" }, h("span", { style: { width: `${Math.round(100 * (r.km_caba_orden || 0) / maxKm)}%` } })),
          h("span", { class: "peq" }, "~", num(r.km_caba_orden), " km"))),
        h("p", { class: "mut peq" }, conf("SUPUESTO"), " ", L.nota_km)),
      h("div", { class: "panel" }, h("h2", {}, "¿Con qué criterios se compararían?"),
        h("ul", { class: "sabemos" }, L.criterios.map((c) => h("li", { "data-criterio": c.id }, h("b", {}, c.titulo), " — ", c.texto,
          h("span", { class: "peq mut" }, ` (${c.con_dato} de ${c.celdas} datos cargados)`)))),
        h("p", { class: "mut peq" }, "Incluye acceso a productores, logística, servicios (agua, energía, efluentes), cercanía comercial y puertos."))),
    h("div", { class: "panel" }, h("h2", {}, "Condiciones que puede tener un terreno («gates»)"), h("p", {}, L.nota_gates),
      h("div", { class: "rejilla rejilla-2" },
        h("div", {}, h("h3", {}, "Duras: descartan ese terreno"), L.gates.filter((g) => g.tipo === "DURO").map((g) => h("div", { class: "gate duro", "data-gate": g.id, style: { margin: "6px 0" } }, h("b", {}, g.gate), h("div", { class: "peq mut" }, g.detalle)))),
        h("div", {}, h("h3", {}, "Condicionales: se pueden resolver con inversión o diseño"), L.gates.filter((g) => g.tipo === "CONDICIONAL").map((g) => h("div", { class: "gate cond", "data-gate": g.id, style: { margin: "6px 0" } }, h("b", {}, g.gate), h("div", { class: "peq mut" }, g.detalle)))))),
    h("div", { class: "panel" }, h("h2", {}, "Puertos y exportación"), h("p", {}, L.puertos)),
    h("div", { class: "panel" }, h("h2", {}, "Formas de ponderar (ilustrativas)"), h("p", { class: "mut" }, L.nota_perfiles),
      h("div", { class: "cards" }, L.perfiles.map((p) => h("div", { class: "card", style: { cursor: "default" } }, h("span", { class: "t" }, `Perfil ${p.id} — ${p.nombre.toLowerCase()}`),
        h("span", { class: "d" }, p.pesos.filter((w) => w.peso).sort((a, b) => b.peso - a.peso).slice(0, 4).map((w) => `${w.criterio} ${num(w.peso)}`).join(" · ")))))),
    h("div", { class: "panel" }, h("h2", {}, "Estado de la evidencia"),
      h("p", {}, `Ranking de regiones: `, h("b", {}, L.ranking.estado === "NO_EMITIDO" ? "no emitido" : "emitido"), ` (${L.ranking.emitidos} de ${L.ranking.filas} combinaciones). `,
        `Cobertura máxima de información: ${num((L.ranking.cobertura_max || 0) * 100)} %.`),
      h("div", { class: "chips" }, Object.entries(L.celdas.por_tipo).map(([k, n]) => k === "SIN_DATO" ? conf("PENDIENTE", n) : conf(k === "ESTIMACION" ? "ESTIMACION" : k === "SUPUESTO" ? "SUPUESTO" : "PVDP", n))),
      h("div", { class: "fila-btn" }, h("a", { class: "btn btn-primario", href: "#/estudio/localizacion" }, "Entender la localización (5 preguntas)"),
        h("a", { class: "btn", href: "#/validacion" }, "Qué datos de campo faltan"))));
}
