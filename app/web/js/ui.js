// Componentes de interfaz reutilizables (sin frameworks).
import { ErrorApp } from "./api.js";

// Los métodos DOM convierten null en el texto "null": se filtran null / undefined / false en toda la app.
for (const proto of [Element.prototype, DocumentFragment.prototype]) {
  for (const m of ["append", "replaceChildren", "prepend"]) {
    const orig = proto[m];
    if (orig.__filtrado) continue;
    const f = function (...xs) { return orig.apply(this, xs.flat().filter((x) => x !== null && x !== undefined && x !== false)); };
    f.__filtrado = true;
    proto[m] = f;
  }
}

export function h(tag, attrs = {}, ...hijos) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "html") el.innerHTML = v;
    else if (k.startsWith("on") && typeof v === "function") el.addEventListener(k.slice(2), v);
    else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const hijo of hijos.flat(Infinity)) {
    if (hijo === null || hijo === undefined || hijo === false) continue;
    el.append(hijo instanceof Node ? hijo : document.createTextNode(String(hijo)));
  }
  return el;
}

// ---------- formato (es-AR: separador decimal coma) ----------
const nf = (d) => new Intl.NumberFormat("es-AR", { minimumFractionDigits: d, maximumFractionDigits: d });
export function fmt(v, formato, dec) {
  if (v === null || v === undefined || Number.isNaN(v)) return "—";
  switch (formato) {
    case "usd": {
      const a = Math.abs(v);
      if (a >= 1e6) return "USD " + nf(2).format(v / 1e6) + " M";
      if (a >= 1e4) return "USD " + nf(0).format(v / 1e3) + " mil";
      return "USD " + nf(0).format(v);
    }
    case "usd0": return "USD " + nf(0).format(v);
    case "pct": return nf(dec ?? 1).format(v * 100) + " %";
    case "anios": return nf(1).format(v) + " años";
    case "veces": return nf(2).format(v) + " ×";
    case "t": return nf(0).format(v) + " t";
    case "num": return nf(dec ?? 2).format(v);
    case "ent": return nf(0).format(v);
    default: return String(v);
  }
}
export const fmtShock = (s, tipo) => tipo === "ABSOLUTO_DIAS" ? `${s > 0 ? "+" : ""}${s} días`
  : tipo === "ABSOLUTO_MESES" ? `${s > 0 ? "+" : ""}${s} meses` : (s === 0 ? "BASE" : `${s > 0 ? "+" : ""}${Math.round(s * 100)} %`);

// ---------- etiquetas de procedencia (icono + texto, nunca solo color) ----------
const ETQ = {
  EVIDENCIA: ["etq-evi", "✔", "Evidencia"], SIMULACION: ["etq-sim", "◇", "Simulación"], ESCENARIO: ["etq-sim", "◇", "Escenario"],
  PENDIENTE: ["etq-pend", "…", "Pendiente"], DEMO: ["etq-demo", "✱", "Solo demostración"], NO_COMPARABLE: ["etq-nocomp", "≠", "No comparable"],
  NO_CALCULABLE: ["etq-nocalc", "∅", "No calculable"], NO_CALCULADA: ["etq-nocalc", "∅", "No calculada"], NO_APLICA: ["etq-na", "–", "No aplica"],
  ERROR: ["etq-error", "✕", "Error"], STAGING: ["etq-pend", "⧗", "Staging (no es evidencia)"], SUPUESTO: ["etq-pend", "~", "Supuesto del modelo"],
  OVERRIDE_TOTAL: ["etq-error", "⚠", "Override total"], OK: ["etq-ok", "✔", "OK"], INFO: ["etq-info", "i", "Info"],
};
export function etq(clave, texto) {
  const [c, i, t] = ETQ[clave] || ["etq-info", "i", clave];
  return h("span", { class: "etq " + c, title: texto || t }, h("span", { "aria-hidden": "true" }, i), texto || t);
}
export function etqOrigen(origen) {
  return { EVIDENCIA_REAL: etq("EVIDENCIA"), ESCENARIO_USUARIO: etq("ESCENARIO"), SUPUESTO_MODELO: etq("SUPUESTO"), PENDIENTE: etq("PENDIENTE") }[origen]
    || etq("INFO", origen);
}
export function etqEstadoDato(e) {
  return { VALIDADO: etq("OK", "Validado (declarado)"), COTIZACION: etq("INFO", "Cotización"), ESCENARIO: etq("ESCENARIO"), NO_SE: etq("PENDIENTE", "No sé") }[e] || etq("PENDIENTE");
}

export function bannerUniverso(r) {
  if (!r) return null;
  if (r.solo_demostracion) {
    return h("div", { class: "banner banner-demo", role: "note" }, h("span", { class: "ico" }, "✱"),
      h("div", {}, h("b", {}, "Solo demostración — datos ficticios"),
        "DEMO_ARTIFICIAL: números inventados para mostrar la app. Universo ARTIFICIAL_TEST del motor (CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO). No es información del proyecto."));
  }
  if (r.universo === "EVIDENCIA") {
    return h("div", { class: "banner banner-evi" }, h("span", { class: "ico" }, "✔"),
      h("div", {}, h("b", {}, "Datos reales / evidencia"), "Solo datos con evidencia E1–E3 (umbral configurable, DEC-084)."));
  }
  return h("div", { class: "banner banner-sim", role: "note" }, h("span", { class: "ico" }, "◇"),
    h("div", {}, h("b", {}, "Simulación hipotética"), "Resultado calculado por el motor sobre los datos y supuestos de ESTE escenario (",
      h("code", {}, r.etiqueta || "SIMULACION_HIPOTETICA_NO_VALIDADA"), "). No es evidencia ni pronóstico."));
}

export function semaforo(color, leyendas) {
  const c = color || "GRIS";
  return h("span", { class: "semaforo", title: leyendas?.[c] || "" }, h("span", { class: "luz luz-" + c, "aria-hidden": "true" }), c);
}
export function leyendaSemaforo(leyendas) {
  return h("div", { class: "leyenda-sem" }, Object.entries(leyendas || {}).map(([k, v]) => h("div", {}, semaforo(k), " ", h("span", { class: "mut" }, v))));
}

// ---------- valor con NO CALCULABLE (#16) ----------
export function itemValor(it) {
  if (it.estado === "TEXTO") return h("div", { class: "item" }, it.etiqueta ? h("div", { class: "lab" }, it.etiqueta) : null, h("div", { class: "val txt" }, it.texto));
  if (it.estado === "SEMAFORO") return h("div", { class: "item" }, h("div", { class: "lab" }, it.etiqueta), h("div", { class: "val txt" }, semaforo(it.texto)),
    h("div", { class: "exp" }, it.explicacion));
  if (it.estado === "VALOR") {
    return h("div", { class: "item" }, h("div", { class: "lab" }, it.etiqueta, etq("SIMULACION")),
      h("div", { class: "val" }, fmt(it.valor, it.formato)), it.explicacion ? h("div", { class: "exp" }, it.explicacion) : null,
      it.nota ? h("div", { class: "exp mut" }, it.nota) : null);
  }
  const titulo = { NO_CALCULABLE: "No calculable", NO_APLICA: "No aplica", NO_CALCULADA: "No calculada", NO_RECUPERADO: "No se recupera",
    NO_DEFINIDA: "TIR no definida", PENDIENTE: "Pendiente" }[it.estado] || it.estado;
  const clave = it.estado === "NO_APLICA" ? "NO_APLICA" : (it.estado === "PENDIENTE" ? "PENDIENTE" : "NO_CALCULABLE");
  return h("div", { class: "item nocalc" }, h("div", { class: "lab" }, it.etiqueta, etq(clave, titulo)),
    h("div", { class: "val" }, titulo),
    (it.faltan && it.faltan.length) ? h("div", { class: "faltan" },
      h("ul", { class: "lista-faltan" }, it.faltan.slice(0, 3).map((f) => h("li", {}, f.texto + "."))),
      it.faltan.length > 3 ? h("div", { class: "peq mut" }, `y ${it.faltan.length - 3} bloque(s) más`) : null,
      h("details", { class: "peq" }, h("summary", {}, "ver qué falta en detalle"),
        h("ul", {}, it.faltan.map((f) => h("li", {}, h("b", {}, f.texto), f.detalles?.length ? ": " + f.detalles.join(" · ") : ""))))) : null,
    it.explicacion ? h("div", { class: "exp" }, it.explicacion) : null, it.nota ? h("div", { class: "exp mut" }, it.nota) : null);
}

export function tarjetas(cards) {
  return h("div", { class: "tarjetas" }, cards.map((c) => h("section", { class: "tarjeta", "data-tarjeta": c.id }, h("h3", {}, c.titulo), c.items.map(itemValor))));
}

// ---------- alertas (#37) ----------
export function alertas(lista) {
  if (!lista || !lista.length) return null;
  const mapa = { SOLO_DEMOSTRACION: "DEMO", SIMULACION: "SIMULACION", DATO_PENDIENTE: "PENDIENTE", EVIDENCIA_BAJA: "PENDIENTE",
    NO_COMPARABLE: "NO_COMPARABLE", OVERRIDE_TOTAL: "OVERRIDE_TOTAL", OVERRIDE_INCOMPATIBLE: "ERROR", REGLA_FISCAL_PENDIENTE: "PENDIENTE",
    NO_CALCULADA: "NO_CALCULADA", NO_APLICA: "NO_APLICA", ERROR: "ERROR" };
  const max = 6;
  const vis = lista.slice(0, max);
  const resto = lista.slice(max);
  return h("div", { class: "alertas", "data-alertas": "" }, vis.map((a) => h("div", { class: "alerta", "data-codigo": a.codigo }, etq(mapa[a.codigo] || "INFO", a.codigo), h("span", {}, a.texto))),
    resto.length ? h("details", {}, h("summary", {}, `${resto.length} alertas más`), resto.map((a) => h("div", { class: "alerta", "data-codigo": a.codigo }, etq(mapa[a.codigo] || "INFO", a.codigo), h("span", {}, a.texto)))) : null);
}

export function disclaimer(texto) {
  return h("div", { class: "disclaimer", "data-disclaimer": "" }, h("b", {}, "Aviso. "), texto ||
    "Este resultado depende de los datos y supuestos ingresados. No constituye una recomendación de inversión ni reemplaza validaciones técnicas, comerciales, fiscales o financieras.");
}

export function cargando(texto = "Calculando con el motor…") {
  return h("div", { class: "cargando", "data-cargando": "" }, h("span", { class: "spin" }), texto);
}

export function errorBox(e) {
  const msg = e?.message || "Error inesperado en la interfaz.";
  if (!(e instanceof ErrorApp) && !e?.codigo) console.error(e);
  return h("div", { class: "banner banner-error", role: "alert", "data-error": e?.codigo || "ERROR" }, h("span", { class: "ico" }, "✕"),
    h("div", {}, h("b", {}, e?.codigo || "Error"), msg, e?.ref ? h("div", { class: "peq mut" }, "Referencia para el log: " + e.ref) : null));
}

// ---------- tabla: ordenar / filtrar / buscar / exportar CSV (#43) ----------
export function tabla(filas, columnas, opciones = {}) {
  const cols = columnas || (filas[0] ? Object.keys(filas[0]).map((k) => ({ k, t: k })) : []);
  let orden = opciones.orden || null, asc = true, filtro = "";
  const cuerpo = h("tbody");
  const thead = h("thead", {}, h("tr", {}, cols.map((c) => h("th", { onclick: () => { asc = orden === c.k ? !asc : true; orden = c.k; pintar(); }, title: "Ordenar" }, c.t))));
  const tbl = h("table", { class: "t" }, thead, cuerpo);
  const info = h("span", { class: "mut peq" });
  function valorCelda(f, c) { const v = c.v ? c.v(f) : f[c.k]; return v; }
  function pintar() {
    let fs = filas.filter((f) => !filtro || cols.some((c) => String(valorCelda(f, c) ?? "").toLowerCase().includes(filtro)));
    if (orden) {
      const c = cols.find((x) => x.k === orden);
      fs = [...fs].sort((a, b) => {
        const x = valorCelda(a, c), y = valorCelda(b, c);
        if (x === y) return 0; if (x === null || x === undefined || x === "") return 1; if (y === null || y === undefined || y === "") return -1;
        return (typeof x === "number" && typeof y === "number" ? x - y : String(x).localeCompare(String(y), "es")) * (asc ? 1 : -1);
      });
    }
    cuerpo.replaceChildren(...fs.map((f) => h("tr", { class: opciones.claseFila ? opciones.claseFila(f) : null, onclick: opciones.alClic ? () => opciones.alClic(f) : null },
      cols.map((c) => {
        const v = valorCelda(f, c);
        const contenido = c.r ? c.r(f) : (c.f ? (v === null || v === undefined ? h("span", { class: "mut" }, c.nulo || "—") : fmt(v, c.f, c.d)) : (v ?? ""));
        return h("td", { class: c.f ? "num" : null }, contenido);
      }))));
    info.textContent = `${fs.length} de ${filas.length} filas`;
  }
  function csv() {
    const esc = (x) => { const s = x === null || x === undefined ? "" : (typeof x === "object" ? JSON.stringify(x) : String(x)); return /[",\n;]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s; };
    const txt = [cols.map((c) => esc(c.t)).join(","), ...filas.map((f) => cols.map((c) => esc(valorCelda(f, c))).join(","))].join("\n");
    descargar((opciones.nombre || "tabla") + ".csv", txt, "text/csv");
  }
  pintar();
  return h("div", {}, h("div", { class: "tabla-herr" },
    opciones.buscar === false ? null : h("input", { type: "search", placeholder: "Buscar / filtrar…", oninput: (e) => { filtro = e.target.value.toLowerCase(); pintar(); } }),
    opciones.csv === false ? null : h("button", { class: "btn", onclick: csv }, "Exportar CSV"), info), h("div", { class: "tabla-env", style: opciones.alto ? { maxHeight: opciones.alto, overflowY: "auto" } : null }, tbl));
}

export function descargar(nombre, contenido, tipo = "application/json") {
  const blob = new Blob([contenido], { type: tipo + ";charset=utf-8" });
  const a = h("a", { href: URL.createObjectURL(blob), download: nombre });
  document.body.append(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}

// ---------- modal / toast ----------
export function modal(contenido, opciones = {}) {
  const m = document.getElementById("modal");
  const cerrar = () => { m.hidden = true; m.replaceChildren(); };
  const caja = h("div", { class: "modal-caja", role: "dialog", "aria-modal": "true" }, contenido,
    opciones.sinCerrar ? null : h("div", { class: "fila-btn" }, h("button", { class: "btn", onclick: cerrar, "data-cerrar": "" }, opciones.textoCerrar || "Cerrar")));
  m.replaceChildren(caja); m.hidden = false;
  m.onclick = (e) => { if (e.target === m && !opciones.sinCerrar) cerrar(); };
  return cerrar;
}
export function confirmar(titulo, texto, aceptar = "Confirmar") {
  return new Promise((res) => {
    let cerrar;
    const fin = (v) => { cerrar(); res(v); };
    cerrar = modal(h("div", {}, h("h2", {}, titulo), h("p", {}, texto), h("div", { class: "fila-btn" },
      h("button", { class: "btn btn-primario", onclick: () => fin(true), "data-confirmar": "" }, aceptar), h("button", { class: "btn", onclick: () => fin(false) }, "Cancelar"))), { sinCerrar: true });
  });
}
let tt;
export function toast(texto, ms = 3200) {
  const t = document.getElementById("toast");
  t.textContent = texto; t.hidden = false; clearTimeout(tt); tt = setTimeout(() => { t.hidden = true; }, ms);
}

export function pestanas(defs, alCambiar, inicial) {
  const cont = h("div");
  const barra = h("div", { class: "pestanas", role: "tablist" });
  let act = inicial || defs[0].id;
  function pintar() {
    barra.replaceChildren(...defs.map((d) => h("button", { class: "pestana" + (d.id === act ? " act" : ""), role: "tab", "data-pestana": d.id,
      onclick: () => { act = d.id; pintar(); } }, d.t)));
    cont.replaceChildren();
    const r = alCambiar(act, cont);
    if (r instanceof Node) cont.append(r);
  }
  pintar();
  return h("div", {}, barra, cont);
}

export function campo(etiqueta, input, ayuda) {
  return h("label", { class: "campo" }, etiqueta, input, ayuda ? h("span", { class: "mut peq" }, ayuda) : null);
}

export function numOrNull(v) {
  if (v === "" || v === null || v === undefined) return null;
  const n = Number(String(v).replace(",", "."));
  return Number.isFinite(n) ? n : null;
}
