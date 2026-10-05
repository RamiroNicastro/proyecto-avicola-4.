// MODO EXPERTO (#35–#38): todos los inputs del motor agrupados por pestañas. Edita SOLO el escenario (nunca la evidencia).
import { api } from "../api.js";
import { E, editar, setEscenario, pedir } from "../estado.js";
import { h, etq, etqOrigen, fmt, cargando, errorBox, tabla, pestanas, campo, numOrNull, confirmar, toast, descargar, bannerUniverso } from "../ui.js";

let pestanaAct = "tiempo";
let altSel = null;

const X = () => E.escenario.experto;
const V = () => (X().comun.valores ||= {});

// Campo genérico sobre comun.valores (vacío = null = PENDIENTE; nunca 0)
function cv(clave, titulo, tipo = "num", opciones = null, ayuda = null) {
  const v = V()[clave];
  let input;
  const upd = (val) => editar(() => { V()[clave] = val; });
  if (tipo === "num") input = h("input", { type: "number", step: "any", value: v ?? "", placeholder: "PENDIENTE", "data-valor": clave, onchange: (e) => upd(numOrNull(e.target.value)) });
  else if (tipo === "bool") input = h("select", { "data-valor": clave, onchange: (e) => upd(e.target.value === "" ? null : e.target.value === "true") },
    [["", "PENDIENTE"], ["true", "Sí"], ["false", "No"]].map(([a, b]) => h("option", { value: a, selected: String(v ?? "") === a }, b)));
  else if (tipo === "sel") input = h("select", { "data-valor": clave, onchange: (e) => upd(e.target.value || null) },
    h("option", { value: "" }, "PENDIENTE"), opciones.map((o) => h("option", { value: o, selected: v === o }, o)));
  else input = h("input", { type: tipo === "date" ? "date" : "text", value: v ?? "", "data-valor": clave, onchange: (e) => upd(e.target.value || null) });
  return campo(h("span", {}, titulo, " ", v === null || v === undefined ? etq("PENDIENTE") : etq("ESCENARIO")), input, ayuda || clave);
}

// Campo genérico sobre experto.analisis (parámetros de análisis de 22)
function ca(clave, titulo, tipo = "num", opciones = null, ayuda = null) {
  const a = X().analisis ||= {};
  const v = a[clave];
  const upd = (val) => editar(() => { if (val === null || val === "") delete X().analisis[clave]; else X().analisis[clave] = val; });
  const input = tipo === "num" ? h("input", { type: "number", step: "any", value: v ?? "", placeholder: "vacío", "data-analisis": clave, onchange: (e) => upd(numOrNull(e.target.value)) })
    : tipo === "sel" ? h("select", { "data-analisis": clave, onchange: (e) => upd(e.target.value || null) }, h("option", { value: "" }, "—"), opciones.map((o) => h("option", { value: o, selected: v === o }, o)))
    : tipo === "bool" ? h("select", { "data-analisis": clave, onchange: (e) => upd(e.target.value === "" ? null : e.target.value === "true") }, [["", "—"], ["true", "Sí"], ["false", "No"]].map(([x, y]) => h("option", { value: x, selected: String(v ?? "") === x }, y)))
    : h("input", { value: Array.isArray(v) ? v.join("|") : (v ?? ""), "data-analisis": clave, onchange: (e) => upd(e.target.value ? (e.target.value.includes("|") ? e.target.value.split("|") : e.target.value) : null) });
  return campo(titulo, input, ayuda || clave);
}

// Editor JSON de un sub-objeto (validación de forma; la económica la hace el motor)
function editorJSON(titulo, leer, escribir, ayuda) {
  const ta = h("textarea", { rows: 10, style: { width: "100%" }, "data-json": titulo }, JSON.stringify(leer() ?? null, null, 1));
  const msg = h("div");
  return h("div", { class: "panel" }, h("h3", {}, titulo), ayuda ? h("p", { class: "mut peq" }, ayuda) : null, ta,
    h("div", { class: "fila-btn" }, h("button", { class: "btn", onclick: () => {
      try { const v = JSON.parse(ta.value); editar(() => escribir(v)); msg.replaceChildren(etq("OK", "aplicado al escenario")); }
      catch (e) { msg.replaceChildren(etq("ERROR", "JSON inválido: " + e.message)); }
    } }, "Aplicar"), msg));
}

// Tabla editable genérica
function tablaEditable(filas, cols, alCambiar, nueva) {
  const tb = h("tbody");
  function pintar() {
    tb.replaceChildren(...filas.map((f, i) => h("tr", {}, cols.map((c) => h("td", {}, c.tipo === "sel"
      ? h("select", { onchange: (e) => { const v = e.target.value || null; if (c.set) c.set(f, v); else f[c.k] = v; alCambiar(); } }, h("option", { value: "" }, "—"),
        c.op.map((o) => h("option", { value: o, selected: (c.get ? c.get(f) : f[c.k]) === o }, o)))
      : c.tipo === "bool" ? h("input", { type: "checkbox", checked: !!f[c.k], onchange: (e) => { f[c.k] = e.target.checked; alCambiar(); } })
        : h("input", { type: c.tipo === "num" ? "number" : "text", step: "any", value: c.get ? (c.get(f) ?? "") : (f[c.k] ?? ""), placeholder: c.tipo === "num" ? "PENDIENTE" : "",
          onchange: (e) => { const v = c.tipo === "num" ? numOrNull(e.target.value) : (e.target.value || null); if (c.set) c.set(f, v); else f[c.k] = v; alCambiar(); } }))),
    h("td", {}, h("button", { class: "btn", onclick: () => { filas.splice(i, 1); alCambiar(); pintar(); } }, "✕")))));
  }
  pintar();
  return h("div", {}, h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, cols.map((c) => h("th", {}, c.t)), h("th", {}, ""))), tb)),
    nueva ? h("div", { class: "fila-btn" }, h("button", { class: "btn", onclick: () => { filas.push(nueva()); alCambiar(); pintar(); } }, "+ Agregar")) : null);
}

// ------------------------------------------------------------------------------------------
function tabTiempo() {
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Tiempo"), h("div", { class: "campos" },
    cv("horizonte_anios", "Horizonte (años)"), cv("fecha_inicio", "Fecha de inicio", "date"), cv("meses_preoperacion", "Meses de preoperación"),
    cv("meses_construccion", "Meses de construcción"), cv("meses_commissioning", "Meses de commissioning"))),
  h("div", { class: "panel" }, h("h3", {}, "Tasas"), h("div", { class: "campos" },
    cv("tasa_descuento", "Tasa de descuento (anual, fracción)", "num", null, "DEC-007: no se inventa un WACC"), cv("tasa_descuento_accionista", "Tasa del accionista (fracción)"),
    cv("tipo_tasa_descuento", "Tipo de tasa", "sel", E.catalogo.tipos_tasa_descuento), cv("convencion_descuento", "Convención de descuento", "sel", ["MENSUAL", "PERIODO_REPORTE"]),
    cv("valor_terminal.metodo", "Valor terminal", "sel", E.catalogo.metodos_valor_terminal))),
  h("div", { class: "panel" }, h("h3", {}, "Ramp-up"), h("div", { class: "campos" },
    campo("Plantilla de curva ilustrativa (SUP-196)", h("select", { onchange: (e) => editar(() => { X().plantilla = e.target.value || null; }) }, h("option", { value: "" }, "ninguna (curva por alternativa)"),
      E.catalogo.plantillas_rampup.map((p) => h("option", { selected: X().plantilla === p }, p))), "Solo forma de la curva de utilización; merma, eficiencia y extras se declaran abajo."),
    ...["merma", "eficiencia", "costos_extra_usd_mes"].map((k) => campo("Ineficiencia ramp-up: " + k, h("input", { type: "number", step: "any", value: X().comun.rampup_ineficiencias?.[k] ?? "", placeholder: "PENDIENTE",
      onchange: (e) => editar(() => { X().comun.rampup_ineficiencias ||= {}; X().comun.rampup_ineficiencias[k] = numOrNull(e.target.value); }) }))))));
}

function tabImpuestos() {
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Impuestos sobre ingresos y ganancias"), h("div", { class: "campos" },
    cv("impuestos.pct_iibb", "IIBB (fracción)"), cv("impuestos.iibb_aplica_domestico", "IIBB aplica a ventas internas", "bool"), cv("impuestos.iibb_aplica_exportacion", "IIBB aplica a exportación", "bool"),
    cv("impuestos.pct_tasas_municipales", "Tasas municipales (fracción)"), cv("impuestos.otros_impuestos_usd_anio", "Otros impuestos (USD/año)"),
    cv("impuestos.tasa_ganancias", "Ganancias (fracción)"), cv("impuestos.anios_quebranto", "Años de quebranto"))),
    h("p", { class: "mut peq" }, "Con IIBB > 0 y la regla de base vacía, el motor informa NO_CALCULABLE_REGLA_FISCAL_PENDIENTE (TF-005)."),
    h("div", { class: "panel" }, h("h3", {}, "IVA"), h("div", { class: "campos" }, cv("iva.modo", "Modo de IVA", "sel", ["SIMPLIFICADO", "EXCLUIDO"]),
      cv("iva.alicuota_ventas", "Alícuota ventas"), cv("iva.alicuota_compras", "Alícuota compras"), cv("iva.alicuota_capex", "Alícuota CAPEX")),
    h("p", { class: "mut peq" }, "Crédito fiscal del IVA de CAPEX solo con declaración completa por etapa (pestaña CAPEX/OPEX): si no, CREDITO_FISCAL_IVA_CAPEX = PENDIENTE (TF-076).")));
}

function tabCT() {
  const inv = X().comun.inventarios ||= {};
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Días de pago a proveedores"), h("div", { class: "campos" }, ["alimento", "pollitos", "servicios", "packaging", "logistica", "energia"].map((g) => cv("dias_pago." + g, g)))),
    h("div", { class: "panel" }, h("h3", {}, "Días de stock y caja"), h("div", { class: "campos" }, ["producto_terminado", "activo_biologico", "alimento", "packaging", "repuestos", "otros"].map((g) => cv("dias_stock." + g, g)),
      cv("dias_caja_operativa", "Días de caja operativa"))),
    h("div", { class: "panel" }, h("h3", {}, "Propiedad de inventarios (si el motor la deja PENDIENTE)"), h("div", { class: "campos" }, E.catalogo.categorias_inventario.map((c) =>
      campo(c, h("select", { onchange: (e) => editar(() => { inv[c] ||= {}; inv[c].propiedad_empresa = e.target.value === "" ? null : e.target.value === "true"; if (inv[c].propiedad_empresa === null) delete inv[c]; }) },
        [["", "según arquitectura (20_opex)"], ["true", "de la empresa"], ["false", "de terceros"]].map(([a, b]) => h("option", { value: a, selected: String(inv[c]?.propiedad_empresa ?? "") === a }, b))))))));
}

function tabDemanda() {
  const canales = X().comun.canales ||= {};
  const cols = ["dias_cobro", "pct_descuentos", "pct_bonificaciones", "pct_devoluciones", "pct_comisiones", "costo_logistico_usd_kg", "pct_derechos_exportacion", "costo_exportacion_usd_kg"];
  const filas = Object.entries(canales).map(([k, v]) => ({ canal: k, ...v }));
  return h("div", {}, h("div", { class: "ayuda" }, "La demanda y los precios de venta se cargan en SIMULAR (pasos 3 y 4) y viven en un solo lugar del escenario. Aquí: condiciones comerciales por canal, mix y precios en serie."),
    h("div", { class: "panel" }, h("h3", {}, "Condiciones comerciales por canal"), tablaEditable(filas, [{ k: "canal", t: "Canal", tipo: "sel", op: E.catalogo.canales }, ...cols.map((c) => ({ k: c, t: c, tipo: "num" }))],
      () => editar(() => { X().comun.canales = Object.fromEntries(filas.filter((f) => f.canal).map((f) => [f.canal, Object.fromEntries(cols.map((c) => [c, f[c] ?? null]))])); }),
      () => ({ canal: "supermercados" })), h("p", { class: "mut peq" }, "Fracciones (0,03 = 3 %); días calendario; USD/kg. Derechos de exportación solo en el canal exportación (SUP-210).")),
    editorJSON("Mix de demanda (sobre la referencia de 02)", () => X().comun.mix_demanda, (v) => { X().comun.mix_demanda = v; }, "Fracciones por producto, p. ej. {\"pechuga\": 0.4}. Solo con plantilla (demanda de prueba de 02, SUPUESTO)."),
    editorJSON("Precios (incluye SERIE por año, base REAL)", () => X().comun.precios, (v) => { X().comun.precios = v; }, "Clave producto|canal|mercado. Los precios del modo simple se aplican encima de estos."),
    editorJSON("Override de precios (SOLO SIMULACIÓN)", () => X().comun.override_precios, (v) => { X().comun.override_precios = v; }, "Evalúa otro precio aunque exista uno observado; el observado queda en la traza (SUP-211)."));
}

function tabArquitectura() {
  const a = X().analisis ||= {};
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Espacio de decisiones del optimizador"), h("div", { class: "campos" },
    ca("espacio.configuraciones", "Configuraciones (C0|C1|…)", "txt"), ca("espacio.escalas", "Escalas (2500|5000|…)", "txt", null, "intermedias admitidas dentro de 2.500–20.000"),
    ca("espacio.incluir_variantes", "Incluir variantes del mapa", "bool"),
    campo("Trayectorias multietapa T1–T3", h("select", { onchange: (e) => editar(() => { X().trayectorias = e.target.value === "true"; }) }, [["false", "No"], ["true", "Sí"]].map(([x, y]) => h("option", { value: x, selected: String(!!X().trayectorias) === x }, y))),
      "Misma configuración por etapa (TRANSICION_DE_ARQUITECTURA_NO_MODELADA)")),
    h("p", { class: "mut peq" }, "La arquitectura/escala elegida en el modo simple (MANUAL) restringe este espacio.")),
  h("div", { class: "panel" }, h("h3", {}, "Mapa de arquitecturas (solo lectura)"), tabla(E.catalogo.arquitecturas, [{ k: "id", t: "ID" }, { k: "tipo", t: "Tipo" }, { k: "faena", t: "Faena" }, { k: "granjas", t: "Granjas" },
    { k: "pollito", t: "Pollito" }, { k: "alimento", t: "Alimento" }, { k: "frio", t: "Frío" }, { k: "estado_capex", t: "CAPEX" }, { k: "estado_opex", t: "OPEX" }], { nombre: "arquitecturas", alto: "320px" })));
}

function tabCapexOpex() {
  const cont = h("div", {}, cargando("Alternativas…"));
  pedir("alternativas", "/api/alternativas").then(async (al) => {
    const ids = al.alternativas.filter((a) => a.tipo !== "NO_INVERTIR_AUN").map((a) => a.id);
    altSel = ids.includes(altSel) ? altSel : (ids.find((i) => i.includes("|10000|")) || ids[0]);
    const zona = h("div");
    async function pintar() {
      zona.replaceChildren(cargando());
      let mods;
      try { mods = await api.post("/api/modulos", { alternativa: altSel }); } catch (e) { zona.replaceChildren(errorBox(e)); return; }
      const st = al.alternativas.find((a) => a.id === altSel);
      const clave = altSel;
      // Borrador: ver la pestaña NO modifica el escenario; solo una edición explícita lo escribe (guardar()).
      const ent = structuredClone(X().por_alternativa?.[clave] || {});
      ent.etapas = ent.etapas?.length ? ent.etapas : [{}];
      const et = ent.etapas[0];
      et.activos ||= []; et.opex_rubros ||= [];
      const metaBase = (mod, uni) => ({ CONFIGURACION: mods.configuracion, ESCALA: mods.escala, VARIANTE: mods.variante, MODULO: mod, UNIVERSO: uni || mod, ORIGEN: "ESCENARIO_USUARIO" });
      const limpio = () => {
        const c = structuredClone(ent);
        const e0 = c.etapas[0];
        if (!e0.activos?.length) delete e0.activos;
        if (!e0.opex_rubros?.length) delete e0.opex_rubros;
        for (const k of Object.keys(e0)) if (e0[k] === null || e0[k] === undefined) delete e0[k];
        if (!Object.keys(e0).length) delete c.etapas;
        return c;
      };
      const guardar = () => editar(() => { const c = limpio(); X().por_alternativa ||= {}; if (Object.keys(c).length) X().por_alternativa[clave] = c; else delete X().por_alternativa[clave]; });
      const activos = et.activos;
      const rubros = et.opex_rubros;
      zona.replaceChildren(
        st?.estado === "ERROR_CONSTRUCCION" ? h("div", { class: "banner banner-error", "data-override-error": "" }, h("span", { class: "ico" }, "✕"), h("div", {}, h("b", {}, "El motor rechaza esta alternativa"), (st.faltan || []).join(" "))) : null,
        h("div", { class: "ayuda" }, `Arquitectura: ${Object.entries(mods.arquitectura).map(([k, v]) => k + "=" + v).join(", ")}. Módulos CAPEX admitidos: ${mods.capex_modulos.join(", ")}. Módulos OPEX que deben cubrirse: ${mods.opex_modulos.join(", ")}.`),
        h("div", { class: "panel" }, h("h3", {}, "CAPEX de la etapa"), h("div", { class: "campos" },
          campo("CAPEX total (USD)", h("input", { type: "number", step: "any", value: et.capex_usd ?? "", placeholder: "PENDIENTE", "data-capex": "", onchange: (e) => { et.capex_usd = numOrNull(e.target.value); if (et.capex_usd !== null && !et.capex_meta) et.capex_meta = metaBase("TOTAL_ETAPA", mods.configuracion === "C0" ? "ESTRUCTURA" : "FAENA_PROPIA"); guardar(); } })),
          campo("Módulo del monto (meta)", h("select", { onchange: (e) => { et.capex_meta = { ...(et.capex_meta || metaBase("TOTAL_ETAPA")), MODULO: e.target.value }; guardar(); } }, mods.capex_modulos.map((m) => h("option", { selected: (et.capex_meta?.MODULO || "TOTAL_ETAPA") === m }, m)))),
          campo("Origen", h("select", { onchange: (e) => { et.capex_meta = { ...(et.capex_meta || metaBase("TOTAL_ETAPA")), ORIGEN: e.target.value }; guardar(); } }, ["ESCENARIO_USUARIO", "COTIZACION"].map((m) => h("option", { selected: et.capex_meta?.ORIGEN === m }, m)))),
          campo("Curva de desembolso [[mes, fracción]…] (suma 1; negativo = antes de operar)", h("input", { value: et.curva_desembolso ? JSON.stringify(et.curva_desembolso) : "", placeholder: "[[-12,0.3],[-6,0.4],[-1,0.3]]",
            onchange: (e) => { try { et.curva_desembolso = e.target.value ? JSON.parse(e.target.value) : null; guardar(); } catch (x) { toast("Curva: JSON inválido"); } } }))),
          h("h3", {}, "Activos (Σ = CAPEX; clase MODULO:nombre)"),
          tablaEditable(activos, [{ k: "clase", t: "Clase (MODULO:nombre)" }, { k: "capex_usd", t: "USD", tipo: "num" }, { k: "vida_util_anios", t: "Vida útil (años)", tipo: "num" },
            { k: "valor_residual_usd", t: "Residual USD", tipo: "num" }, { k: "costo_reemplazo_usd", t: "Reemplazo USD", tipo: "num" }, { k: "depreciable", t: "Depreciable", tipo: "bool" }], guardar,
          () => ({ clase: (mods.capex_modulos.find((m) => m !== "TOTAL_ETAPA") || "OBRA_CIVIL") + ":activo", capex_usd: null, vida_util_anios: null, valor_residual_usd: null, costo_reemplazo_usd: null, depreciable: true })),
          editorJSON("IVA del CAPEX (TF-076)", () => et.iva_capex, (v) => { et.iva_capex = v; X().por_alternativa ||= {}; X().por_alternativa[clave] = limpio(); }, "{\"base\":\"NETA\",\"iva_estado\":\"DECLARADO\",\"tasa\":x,\"condicion_fiscal\":\"…\",\"elegible_credito\":true,\"criterio\":\"…\"}")),
        h("div", { class: "panel" }, h("h3", {}, "OPEX por rubro (USD/año a escala plena; cada rubro con el módulo de la arquitectura)"),
          tablaEditable(rubros, [{ k: "rubro", t: "Rubro" }, { k: "MODULO", t: "Módulo OPEX", tipo: "sel", op: mods.opex_modulos, get: (r) => r.meta?.MODULO, set: (r, v) => { r.meta = { ...(r.meta || metaBase(v)), MODULO: v, UNIVERSO: v }; } },
            { k: "grupo_proveedor", t: "Grupo proveedor", tipo: "sel", op: E.catalogo.grupos_proveedor }, { k: "naturaleza", t: "Naturaleza", tipo: "sel", op: E.catalogo.naturalezas_opex },
            { k: "costo_pleno_usd_anio", t: "USD/año", tipo: "num" }, { k: "pct_variable", t: "% variable (semivariable)", tipo: "num" }, { k: "dias_pago", t: "Días pago", tipo: "num" },
            { k: "driver_riesgo", t: "Driver de riesgo (alimento, salarios…)" }], () => { rubros.forEach((r) => { r.es_compra = r.es_compra ?? true; r.meta ||= metaBase(mods.opex_modulos[0]); }); guardar(); },
          () => ({ rubro: "", meta: metaBase(mods.opex_modulos[0]), grupo_proveedor: "servicios", naturaleza: "fijo", costo_pleno_usd_anio: null, es_compra: true, dias_pago: null, iva_credito: false })),
          h("p", { class: "mut peq" }, "Un rubro de un módulo que la arquitectura no tiene → OVERRIDE_INCOMPATIBLE_CON_ARQUITECTURA (error claro). Falta un módulo → OPEX incompleto (no se publica).")),
        editorJSON("Curva de ramp-up de la alternativa", () => et.rampup, (v) => { et.rampup = v; X().por_alternativa ||= {}; X().por_alternativa[clave] = limpio(); }, "[{\"mes\":1,\"utilizacion\":0.5,\"merma\":0.03,\"eficiencia\":0.9,\"costos_extra_usd_mes\":0}, …]"),
        editorJSON("Financiamiento de la alternativa", () => ent.financiamiento, (v) => { ent.financiamiento = v; X().por_alternativa ||= {}; X().por_alternativa[clave] = limpio(); }, "aportes, deudas (tipo de tasa obligatorio), caja mínima, dividendos. Vacío = usa el común."),
        overrideTotal());
    }
    cont.replaceChildren(h("div", { class: "campos" }, campo("Alternativa", h("select", { "data-alt-experto": "", onchange: (e) => { altSel = e.target.value; pintar(); } },
      ids.map((i) => h("option", { value: i, selected: i === altSel }, i))))), zona);
    pintar();
  }).catch((e) => cont.replaceChildren(errorBox(e)));
  return cont;
}

function overrideTotal() {
  const activo = X().comun.OVERRIDE_TOTAL_ARQUITECTURA === true;
  return h("div", { class: "panel" }, h("h3", {}, "OVERRIDE_TOTAL_ARQUITECTURA"),
    h("p", { class: "peq" }, "Acepta CAPEX/OPEX del usuario SIN verificarlos contra la arquitectura. La corrida queda SIMULACION_HIPOTETICA_OVERRIDE_TOTAL, con trazabilidad parcial, y no es comparable con corridas verificadas."),
    h("label", {}, h("input", { type: "checkbox", checked: activo, "data-override-total": "", onchange: async (e) => {
      if (e.target.checked) {
        const ok = await confirmar("Override total de arquitectura", "Esta simulación pierde parte de la trazabilidad automática. ¿Confirmás activar OVERRIDE_TOTAL_ARQUITECTURA? No modifica evidencia.", "Activar");
        if (!ok) { e.target.checked = false; return; }
        editar(() => { X().comun.OVERRIDE_TOTAL_ARQUITECTURA = true; X().override_total_confirmado = true; });
      } else editar(() => { X().comun.OVERRIDE_TOTAL_ARQUITECTURA = false; X().override_total_confirmado = false; });
    } }), " Activar override total"), activo ? h("div", {}, etq("OVERRIDE_TOTAL")) : null);
}

function tabFinanciamiento() {
  return h("div", {}, editorJSON("Financiamiento común (todas las alternativas)", () => X().comun.financiamiento, (v) => { X().comun.financiamiento = v; },
    "{\"aportes\": [[mes, monto]], \"aporte_automatico\": false, \"caja_minima_usd\": null, \"deudas\": [{\"id\": \"D1\", \"monto\": null, \"tasa\": null, \"tipo_tasa\": \"EFECTIVA_ANUAL\", \"base_tasa\": \"REAL\", \"plazo_meses\": null, \"gracia_meses\": 0, \"metodo\": \"FRANCES\", \"frecuencia_meses\": 1, \"mes_desembolso\": null, \"comision_pct\": 0}], \"politica_dividendos\": null}. USD 2 M no es un default."),
  h("p", { class: "mut peq" }, `Métodos: ${E.catalogo.metodos_deuda.join(", ")}. Tipos de tasa: ${E.catalogo.tipos_tasa_deuda.join(", ")} (obligatorio; SUP-200).`));
}

function tabStress() {
  const st = (X().stress ||= []);
  const filas = st.flatMap((s) => Object.entries(s.shocks || {}).map(([v, x]) => ({ id: s.id, nombre: s.nombre, variable: v, valor: x })));
  return h("div", {}, h("p", {}, "Stress del escenario (vacío = se usan los de 22_riesgos/escenarios_stress.csv, ilustrativos)."),
    tablaEditable(filas, [{ k: "id", t: "ID" }, { k: "nombre", t: "Nombre" }, { k: "variable", t: "Variable", tipo: "sel", op: E.catalogo.variables_riesgo.map((v) => v.id) }, { k: "valor", t: "Magnitud", tipo: "num" }],
      () => editar(() => { const m = {}; filas.forEach((f) => { if (!f.id || !f.variable) return; m[f.id] ||= { id: f.id, nombre: f.nombre || f.id, shocks: {} }; m[f.id].shocks[f.variable] = f.valor; }); X().stress = Object.values(m); }),
      () => ({ id: "ST-U1", nombre: "", variable: "precio_venta", valor: null })),
    h("div", { class: "panel" }, h("h3", {}, "Reglas de status quo (NO_INVERTIR_AUN)"), h("div", { class: "campos" },
      ca("decision.sq_stress", "Stress que activan SQ-4 (IDs con |)", "txt"), ca("decision.sq_score_ordinal_max", "SQ-5: score de riesgo máximo"), ca("decision.sq_cobertura_min", "SQ-6: cobertura de evidencia mínima"))));
}

function tabDistribuciones() {
  const ds = (X().distribuciones ||= []);
  const cs = (X().correlaciones ||= []);
  const filas = ds.map((d) => ({ ...d, PARAMETROS: JSON.stringify(d.PARAMETROS || {}) }));
  return h("div", {}, h("div", { class: "ayuda" }, "Monte Carlo solo corre con distribuciones RESPALDADAS (con fuente) en escenarios del proyecto. ARTIFICIAL solo en la demo. Correlación vacía ≠ 0."),
    h("h3", {}, "Distribuciones"), tablaEditable(filas, [{ k: "VARIABLE", t: "Variable", tipo: "sel", op: E.catalogo.variables_riesgo.map((v) => v.id) }, { k: "DISTRIBUCION", t: "Tipo", tipo: "sel", op: E.catalogo.distribuciones },
      { k: "PARAMETROS", t: "Parámetros (JSON)" }, { k: "FUENTE", t: "Fuente" }, { k: "ESTADO", t: "Estado", tipo: "sel", op: E.catalogo.estados_distribucion }],
    () => editar(() => { X().distribuciones = filas.map((f) => { let p = {}; try { p = JSON.parse(f.PARAMETROS || "{}"); } catch (e) { p = {}; } return { ...f, PARAMETROS: p }; }); }),
    () => ({ VARIABLE: "precio_venta", DISTRIBUCION: "TRIANGULAR", PARAMETROS: "{\"min\":-0.2,\"moda\":0,\"max\":0.1}", FUENTE: "", ESTADO: "PENDIENTE" })),
    h("h3", {}, "Correlaciones"), tablaEditable(cs, [{ k: "A", t: "A" }, { k: "B", t: "B" }, { k: "RHO", t: "ρ", tipo: "num" }, { k: "ESTADO", t: "Estado", tipo: "sel", op: ["PENDIENTE", "RESPALDADA", "ARTIFICIAL"] }, { k: "FUENTE", t: "Fuente" }],
      () => editar(() => { X().correlaciones = cs; }), () => ({ A: "precio_venta", B: "alimento", RHO: null, ESTADO: "PENDIENTE", FUENTE: "" })),
    h("div", { class: "campos" }, ca("montecarlo.n", "Simulaciones"), ca("montecarlo.semilla", "Semilla"), ca("montecarlo.supuesto_independencia", "Declarar supuesto de independencia", "bool")));
}

function tabOptimizador() {
  const R = Object.keys(E.catalogo.restricciones);
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Perfil de análisis"), h("div", { class: "campos" },
    campo("Perfil", h("select", { "data-perfil": "", onchange: (e) => editar(() => { X().perfil_analisis = e.target.value; }) }, [["RAPIDO", "RÁPIDO (sensibilidad en variables de robustez)"], ["COMPLETO", "COMPLETO (todas las variables, 2D y quiebres: lento)"]].map(([a, b]) => h("option", { value: a, selected: X().perfil_analisis === a }, b))),
      "Parámetro de análisis (no cambia los resultados base)"),
    ca("decision.tolerancia_equivalencia", "Tolerancia de equivalencia (fracción)"), ca("optimizador.hard_pendiente_excluye", "Restricción no evaluable excluye", "bool"),
    ca("optimizador.exigir_fisico_confirmado", "Exigir factibilidad física confirmada", "bool"), ca("capital.metrica", "Métrica de capital", "sel", ["PICO_FONDOS", "FONDOS_INICIALES"]),
    ca("umbral.dscr_2d", "Umbral DSCR para 2D"), ca("umbral.payback_2d", "Umbral payback para 2D"))),
  h("div", { class: "panel" }, h("h3", {}, "Pesos del objetivo BALANCEADO (se normalizan; sin pesos = PESOS_NO_DEFINIDOS)"), h("div", { class: "campos" }, E.catalogo.componentes_balanceado.map((c) => ca(`balanceado.peso.${c}`, c)), ca("balanceado.preset", "Preset", "sel", ["IGUALES"]))),
  h("div", { class: "panel" }, h("h3", {}, "Pesos del score ordinal de riesgo (no es probabilidad)"), h("div", { class: "campos" }, E.catalogo.componentes_riesgo.map((c) => ca(`riesgo.peso.${c}`, c)), ca("riesgo.faltantes", "Faltantes", "sel", ["SEPARAR", "PENALIZAR"]))),
  h("div", { class: "panel" }, h("h3", {}, "Restricciones HARD / SOFT"), h("p", { class: "mut peq" }, "SOFT exige penalización declarada (no se inventa un peso). Las del modo simple se aplican como HARD encima."),
    h("div", { class: "tabla-env" }, h("table", { class: "t ed" }, h("thead", {}, h("tr", {}, ["Restricción", "Métrica", "Valor", "Tipo", "Penalización"].map((x) => h("th", {}, x)))),
      h("tbody", {}, R.map((k) => h("tr", {}, h("td", {}, k), h("td", { class: "peq" }, `${E.catalogo.restricciones[k].metrica || "capital"} ${E.catalogo.restricciones[k].sentido}`),
        h("td", {}, ca(`restriccion.${k}.valor`, "")), h("td", {}, ca(`restriccion.${k}.tipo`, "", "sel", ["HARD", "SOFT"])), h("td", {}, ca(`restriccion.${k}.penalizacion`, "")))))))));
}

function tabFisico() {
  const d = (X().disponibilidad ||= {}), b = (X().base_valores ||= {});
  const f = (obj, k) => campo(k, h("input", { value: obj[k] ?? "", placeholder: "PENDIENTE", "data-disp": k, onchange: (e) => editar(() => { const v = e.target.value; obj[k] = v === "" ? null : (v === "true" ? true : v === "false" ? false : numOrNull(v)); }) }));
  return h("div", {}, h("div", { class: "panel" }, h("h3", {}, "Disponibilidades físicas (gates; sin dato → FACTIBILIDAD_PENDIENTE, nunca FACTIBLE)"), h("div", { class: "campos" }, Object.keys(d).map((k) => f(d, k)))),
    h("div", { class: "panel" }, h("h3", {}, "Valores base para shocks absolutos"), h("div", { class: "campos" }, Object.keys(b).map((k) => f(b, k)))));
}

async function tabEvidencia() {
  const r = await api.get("/api/evidencia");
  return h("div", {}, h("div", { class: "banner banner-evi" }, h("span", { class: "ico" }, "✔"), h("div", {}, h("b", {}, "La evidencia no se edita desde la app"),
    `Umbral vigente: ${r.umbral.join(", ")} (fila umbral_evidencia_publicacion de inputs_financieros.csv; DEC-084). Para cargar evidencia: editar la base correspondiente con fuente y nivel, fuera de la app. Los datos cargados a mano van a STAGING.`)),
  h("p", {}, h("a", { href: "#/evidencia" }, "Ver evidencia del proyecto →")));
}

async function tabTrazabilidad() {
  const t = await api.get("/api/trazabilidad");
  const cont = h("div");
  let kpi = "VAN";
  const zona = h("div");
  async function pintar() {
    const filas = t.filas.filter((f) => (t.kpis[kpi] || []).includes(f.VARIABLE));
    zona.replaceChildren(h("h3", {}, "De dónde sale (cadena del motor)"), tabla(filas, [{ k: "VARIABLE", t: "Variable" }, { k: "ORIGEN", t: "Origen" }, { k: "TRANSFORMACION", t: "Transformación" },
      { k: "UNIDAD", t: "Unidad" }, { k: "EVIDENCIA", t: "Evidencia" }, { k: "ESTADO", t: "Estado" }, { k: "TEST", t: "Test" }], { nombre: "trazabilidad_" + kpi, buscar: false }));
    if (E.alternativa) {
      try {
        const tr = await pedir("traza", "/api/traza", { alternativa: E.alternativa });
        zona.append(h("h3", {}, `Mapa de drivers de la alternativa ${E.alternativa} (escenario actual)`), tabla(tr.filas, [{ k: "VARIABLE", t: "Variable" }, { k: "VALOR", t: "Valor" }, { k: "UNIDAD", t: "Unidad" },
          { k: "ORIGEN", t: "Origen", r: (f) => etqOrigen(f.ORIGEN) }, { k: "ARCHIVO", t: "Archivo" }, { k: "VARIABLE_ORIGEN", t: "Variable origen" }, { k: "EVIDENCIA", t: "Evidencia" }, { k: "OBSERVACIONES", t: "Observaciones" }],
        { nombre: "mapa_drivers", alto: "420px" }));
      } catch (e) { zona.append(errorBox(e)); }
    } else zona.append(h("p", { class: "mut" }, "Simule una alternativa para ver su mapa de drivers."));
  }
  cont.append(h("div", { class: "campos" }, campo("KPI — VER DE DÓNDE SALE", h("select", { "data-kpi": "", onchange: (e) => { kpi = e.target.value; pintar(); } }, Object.keys(t.kpis).map((k) => h("option", { selected: k === kpi }, k))))), zona);
  pintar();
  return cont;
}

function tabJSON() {
  const ta = h("textarea", { rows: 28, style: { width: "100%" }, "data-json-escenario": "" }, JSON.stringify(E.escenario, null, 1));
  const msg = h("div");
  return h("div", {}, h("p", {}, "Escenario completo (formato ESCENARIO_APP_AVICOLA, versión 1). Editar con cuidado: se valida antes de aplicar."), ta,
    h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario", onclick: async () => {
      try { const esc = await api.post("/api/validar", { escenario: JSON.parse(ta.value) }); setEscenario(esc, true); msg.replaceChildren(etq("OK", "aplicado")); }
      catch (e) { msg.replaceChildren(errorBox(e.codigo ? e : { codigo: "JSON", message: e.message })); }
    } }, "Validar y aplicar"), h("button", { class: "btn", onclick: () => descargar(`escenario_${E.escenario.id}.json`, ta.value) }, "Descargar"), msg));
}

const TABS = [["tiempo", "Tiempo, tasas y ramp-up", tabTiempo], ["demanda", "Demanda, canales y precios", tabDemanda], ["arquitectura", "Arquitectura y escala", tabArquitectura],
  ["capex", "CAPEX / OPEX por alternativa", tabCapexOpex], ["impuestos", "Impuestos e IVA", tabImpuestos], ["ct", "Capital de trabajo", tabCT], ["deuda", "Deuda y financiamiento", tabFinanciamiento],
  ["stress", "Stress y status quo", tabStress], ["dist", "Distribuciones y correlaciones", tabDistribuciones], ["optimizador", "Optimizador (pesos y restricciones)", tabOptimizador],
  ["fisico", "Factibilidad física", tabFisico], ["evidencia", "Evidencia", tabEvidencia], ["trazabilidad", "Trazabilidad", tabTrazabilidad], ["json", "JSON", tabJSON]];

export async function render() {
  return h("div", {}, h("h1", {}, "Modo experto"), h("p", { class: "mut" }, "Todos los inputs del motor. Vacío = PENDIENTE (nunca 0). Todo lo que se edita aquí es ESCENARIO: la evidencia central no se modifica."),
    E.escenario?.solo_demostracion ? h("div", { class: "banner banner-demo" }, h("span", { class: "ico" }, "✱"), h("div", {}, h("b", {}, "Demo: datos ficticios"), "Puede editarse; al guardar se crea una copia.")) : null,
    pestanas(TABS.map(([id, t]) => ({ id, t })), (id, cont) => {
      pestanaAct = id;
      const r = TABS.find((x) => x[0] === id)[2]();
      if (r instanceof Promise) { cont.append(cargando()); r.then((n) => cont.replaceChildren(n)).catch((e) => cont.replaceChildren(errorBox(e))); return; }
      return r;
    }, pestanaAct));
}
