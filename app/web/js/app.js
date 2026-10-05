// Arranque, navegación (barra lateral agrupada + migas de pan), buscador global y barra superior.
import { api } from "./api.js";
import { E, iniciar, alCambiar, setEscenario } from "./estado.js";
import { h, etq, errorBox, toast, cargando, cargarTextos } from "./ui.js";
import { abrirGestor } from "./vistas/escenarios.js";
import { primerUso, bannerDemo, refrescarTour } from "./tour.js";
import * as inicio from "./vistas/inicio.js";
import * as simular from "./vistas/simular.js";
import * as comparar from "./vistas/comparar.js";
import * as optimizar from "./vistas/optimizar.js";
import * as riesgos from "./vistas/riesgos.js";
import * as validacion from "./vistas/validacion.js";
import * as evidencia from "./vistas/evidencia.js";
import * as experto from "./vistas/experto.js";
import * as estudio from "./vistas/estudio.js";
import * as cadena from "./vistas/cadena.js";
import * as localizacion from "./vistas/localizacion.js";
import * as proceso from "./vistas/proceso.js";
import * as productos from "./vistas/productos.js";
import * as arquitecturas from "./vistas/arquitecturas.js";
import * as escalas from "./vistas/escalas.js";
import * as diccionario from "./vistas/diccionario.js";
import * as estado from "./vistas/estado.js";
import * as seguir from "./vistas/seguir.js";
import * as buscar from "./vistas/buscar.js";

// ruta → [vista, migas]. Las migas son [texto, ruta|null]; «params» = segmentos después de la ruta.
const G = (id) => (E.estudio?.grupos || []).find((g) => g.id === id);
const SECCION = { PROYECTO: ["Proyecto", "estudio"], ECONOMIA: ["Economía", "estudio"] };
function migasGrupo(id) {
  const g = G(id);
  return g ? [SECCION[g.seccion], [g.titulo, "grupo/" + g.id]] : [["Proyecto", "estudio"]];
}
function migasModulo(mid) {
  for (const g of E.estudio?.grupos || []) {
    const m = g.modulos.find((x) => x.id === mid);
    if (m) return [...migasGrupo(g.id).filter(([t]) => t !== m.titulo), [m.titulo, null]];
  }
  return [["Estudio completo", "estudio"], [mid, null]];
}
const RUTAS = {
  inicio: [inicio, () => [["Inicio", null]]],
  "como-funciona": [cadena, () => [["Proyecto", "estudio"], ["Cómo funciona el negocio", null]]],
  estudio: [estudio, (p) => (p[0] ? migasModulo(p[0]) : [["Proyecto", null], ["Estudio completo", null]])],
  grupo: [estudio, (p) => migasGrupo(p[0])],
  localizacion: [localizacion, () => [["Proyecto", "estudio"], ["Localización", "estudio/localizacion"], ["¿Dónde podría estar la planta?", null]]],
  proceso: [proceso, () => [["Proyecto", "estudio"], ["Planta y procesos", "grupo/planta"], ["¿Qué pasa dentro de la planta?", null]]],
  productos: [productos, () => [["Proyecto", "estudio"], ["Productos", "grupo/productos"], ["¿Qué sale de un pollo?", null]]],
  arquitecturas: [arquitecturas, () => [["Economía", "estudio"], ["Inversión", "grupo/inversion"], ["Las 5 arquitecturas", null]]],
  escalas: [escalas, () => [["Economía", "estudio"], ["Inversión", "grupo/inversion"], ["¿Qué significa cada escala?", null]]],
  diccionario: [diccionario, () => [["Ayuda", null], ["Diccionario", null]]],
  estado: [estado, () => [["Proyecto", "estudio"], ["¿Dónde estamos parados?", null]]],
  seguir: [seguir, () => [["Decisión", null], ["Para seguir avanzando", null]]],
  buscar: [buscar, () => [["Búsqueda", null]]],
  simular: [simular, () => [["Decisión", null], ["Simular un escenario", null]]],
  comparar: [comparar, () => [["Decisión", null], ["Comparar", null]]],
  optimizar: [optimizar, () => [["Decisión", null], ["Optimizar", null]]],
  riesgos: [riesgos, () => [["Decisión", null], ["Probar riesgos", null]]],
  validacion: [validacion, () => [["Decisión", null], ["Qué falta validar", null]]],
  evidencia: [evidencia, () => [["Avanzado", null], ["Evidencia", null]]],
  experto: [experto, () => [["Avanzado", null], ["Modo experto", null]]],
  trazabilidad: [experto, () => [["Avanzado", null], ["Trazabilidad", null]]],
};

export function rutaActual() {
  const [camino, qs] = (location.hash || "#/inicio").replace(/^#\//, "").split("?");
  const partes = camino.split("/").filter(Boolean).map(decodeURIComponent);
  const r = RUTAS[partes[0]] ? partes[0] : "inicio";
  return { r, params: partes.slice(1), query: Object.fromEntries(new URLSearchParams(qs || "")) };
}

function pintarMigas(m) {
  const n = document.getElementById("migas");
  const items = [["Inicio", "inicio"], ...m.filter(([t]) => t !== "Inicio")];
  n.replaceChildren(...items.flatMap(([t, ruta], i) => {
    const ult = i === items.length - 1;
    const nodo = ult || !ruta ? h("span", { class: ult ? "actual" : null }, t) : h("a", { href: "#/" + ruta }, t);
    return i ? [h("span", { class: "sep", "aria-hidden": "true" }, "›"), nodo] : [nodo];
  }));
  n.dataset.migas = items.map(([t]) => t.toUpperCase()).join(" > ");
}

let pintando = 0;
async function render() {
  const { r, params, query } = rutaActual();
  const id = ++pintando;
  const clave = r === "grupo" ? "grupo/" + params[0] : (r === "estudio" && params[0] ? null : r);
  document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("activo", a.dataset.ruta === clave));
  document.getElementById("sidebar").classList.remove("abierta");
  document.getElementById("buscar-res").hidden = true;
  const [vista, migas] = RUTAS[r];
  pintarMigas(migas(params));
  const cont = document.getElementById("vista");
  cont.replaceChildren(cargando("Cargando…"));
  globales();
  try {
    const nodo = await vista.render(params, query, r);
    if (id === pintando) { cont.replaceChildren(nodo); window.scrollTo(0, 0); }
  } catch (e) {
    if (id === pintando) cont.replaceChildren(errorBox(e));
  }
  cont.dataset.vista = r;
  refrescarTour();
}

function globales() {
  document.getElementById("alertas-globales").replaceChildren(bannerDemo());
}

function barra() {
  const c = document.getElementById("escenario-actual");
  const esc = E.escenario;
  if (!esc) { c.replaceChildren(); return; }
  c.replaceChildren(
    h("span", { class: "mut peq" }, "Escenario:"), h("span", { class: "nombre", "data-nombre-escenario": "" }, esc.nombre),
    esc.solo_demostracion ? etq("DEMO") : etq("SIMULACION", esc.tipo === "PRESET" ? "Preset" : "Simulación"),
    E.sinGuardar ? h("span", { class: "etq etq-pend", "data-sin-guardar": "" }, "● sin guardar") : null);
  globales();
}

function pie() {
  const v = E.estado?.version;
  if (!v) return;
  document.getElementById("version-pie").replaceChildren(
    h("div", {}, `App ${v.version_app} · ${v.fecha_app}`), h("div", {}, `Motor 21 v${v.version_motor["modelo_financiero (21)"]} · 22 v${v.version_motor["motor_riesgo (22)"]}`),
    h("div", {}, `Versión ${v.commit} (${v.fecha_commit})`), v.motor_con_cambios_locales ? h("div", { class: "etq etq-error" }, "motor con cambios locales") : null);
}

async function guardar() {
  try {
    const esc = await api.post("/api/escenarios", { escenario: E.escenario });
    setEscenario(esc, false);
    toast("Escenario guardado en esta computadora (separado de los datos reales).");
  } catch (e) {
    if (e.status === 400 && /solo lectura/.test(e.message)) {
      toast("Los ejemplos y la demo no se modifican: se guarda una copia.");
      const copia = structuredClone(E.escenario);
      copia.id = Math.random().toString(16).slice(2, 14);
      copia.tipo = copia.tipo === "PRESET" ? "USUARIO" : copia.tipo;
      copia.nombre = copia.nombre + " (copia)";
      try { setEscenario(await api.post("/api/escenarios", { escenario: copia }), false); } catch (e2) { toast(e2.message, 6000); }
    } else toast(e.message, 6000);
  }
}

// ---------- buscador global ----------
export function destinoBusqueda(x) {
  return x.tipo === "TERMINO" ? "#/diccionario?q=" + encodeURIComponent(x.q) : "#/" + x.ruta;
}
function buscador() {
  const inp = document.getElementById("buscar");
  const caja = document.getElementById("buscar-res");
  let t, res = [], sel = 0;
  const pintar = () => {
    caja.replaceChildren(...res.slice(0, 8).map((x, i) => h("button", { class: "res-busq" + (i === sel ? " act" : ""), "data-resultado-busqueda": x.ruta,
      onclick: () => ir(x) }, h("span", { class: "tipo" }, { VISTA: "pantalla", MODULO: "tema", REGION: "región", TERMINO: "diccionario" }[x.tipo] || ""),
      h("span", { class: "t" }, x.titulo), h("span", { class: "d" }, x.texto))),
    res.length ? h("a", { class: "res-busq", href: "#/buscar?q=" + encodeURIComponent(inp.value) }, h("span", { class: "d" }, "Ver todos los resultados →"))
      : h("div", { class: "res-busq" }, h("span", { class: "d" }, "Sin resultados. Probá con otra palabra (por ejemplo: agua, faena, CAPEX).")));
    caja.hidden = false;
  };
  const ir = (x) => { caja.hidden = true; inp.blur(); location.hash = destinoBusqueda(x); };
  inp.addEventListener("input", () => {
    clearTimeout(t);
    if (!inp.value.trim()) { caja.hidden = true; return; }
    t = setTimeout(async () => { try { res = (await api.get("/api/buscar?q=" + encodeURIComponent(inp.value))).resultados; sel = 0; pintar(); } catch (e) { /* sin búsqueda */ } }, 180);
  });
  inp.addEventListener("keydown", async (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      clearTimeout(t);
      res = (await api.get("/api/buscar?q=" + encodeURIComponent(inp.value))).resultados;
      if (res[0]) ir(res[Math.min(sel, res.length - 1)]); else location.hash = "#/buscar?q=" + encodeURIComponent(inp.value);
    } else if (e.key === "ArrowDown") { sel = Math.min(sel + 1, Math.min(res.length, 8) - 1); pintar(); e.preventDefault(); }
    else if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); pintar(); e.preventDefault(); }
    else if (e.key === "Escape") caja.hidden = true;
  });
  document.addEventListener("click", (e) => { if (!document.getElementById("buscador").contains(e.target)) caja.hidden = true; });
}

window.addEventListener("hashchange", render);
document.getElementById("btn-menu").addEventListener("click", () => document.getElementById("sidebar").classList.toggle("abierta"));
document.getElementById("btn-escenarios").addEventListener("click", () => abrirGestor());
document.getElementById("btn-guardar").addEventListener("click", guardar);
alCambiar(barra);
buscador();

(async () => {
  try {
    const [, est, txt] = await Promise.all([iniciar(), api.get("/api/estudio"), api.get("/api/textos")]);
    E.estudio = est;
    cargarTextos(txt);
    pie(); barra(); render();
    primerUso();
  } catch (e) {
    document.getElementById("vista").replaceChildren(errorBox(e));
  }
})();

export function irA(ruta) { if (location.hash === "#/" + ruta) render(); else location.hash = "#/" + ruta; }
window.__app = { E, irA, render };
