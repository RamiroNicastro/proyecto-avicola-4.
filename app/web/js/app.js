// Arranque, navegación y barra superior.
import { api } from "./api.js";
import { E, iniciar, alCambiar, setEscenario } from "./estado.js";
import { h, etq, errorBox, toast, cargando } from "./ui.js";
import { abrirGestor } from "./vistas/escenarios.js";
import * as inicio from "./vistas/inicio.js";
import * as simular from "./vistas/simular.js";
import * as comparar from "./vistas/comparar.js";
import * as optimizar from "./vistas/optimizar.js";
import * as riesgos from "./vistas/riesgos.js";
import * as validacion from "./vistas/validacion.js";
import * as evidencia from "./vistas/evidencia.js";
import * as experto from "./vistas/experto.js";

const VISTAS = { inicio, simular, comparar, optimizar, riesgos, validacion, evidencia, experto };

function rutaActual() {
  const r = (location.hash || "#/inicio").replace(/^#\//, "").split("?")[0];
  return VISTAS[r] ? r : "inicio";
}

let pintando = 0;
async function render() {
  const r = rutaActual();
  const id = ++pintando;
  document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("activo", a.dataset.ruta === r));
  document.getElementById("sidebar").classList.remove("abierta");
  const vista = document.getElementById("vista");
  vista.replaceChildren(cargando("Cargando…"));
  try {
    const nodo = await VISTAS[r].render();
    if (id === pintando) vista.replaceChildren(nodo);
  } catch (e) {
    if (id === pintando) vista.replaceChildren(errorBox(e));
  }
  vista.dataset.vista = r;
}

function barra() {
  const c = document.getElementById("escenario-actual");
  const esc = E.escenario;
  if (!esc) { c.replaceChildren(); return; }
  c.replaceChildren(
    h("span", { class: "mut peq" }, "Escenario:"), h("span", { class: "nombre", "data-nombre-escenario": "" }, esc.nombre),
    esc.solo_demostracion ? etq("DEMO") : null, etq("SIMULACION", esc.tipo === "PRESET" ? "Preset estructural" : "Escenario hipotético"),
    E.sinGuardar ? h("span", { class: "etq etq-pend", "data-sin-guardar": "" }, "● sin guardar") : null);
}

function pie() {
  const v = E.estado?.version;
  if (!v) return;
  document.getElementById("version-pie").replaceChildren(
    h("div", {}, `App ${v.version_app} · ${v.fecha_app}`), h("div", {}, `Motor 21 v${v.version_motor["modelo_financiero (21)"]} · 22 v${v.version_motor["motor_riesgo (22)"]}`),
    h("div", {}, `Commit ${v.commit} (${v.fecha_commit})`), v.motor_con_cambios_locales ? h("div", { class: "etq etq-error" }, "motor con cambios locales") : null);
}

async function guardar() {
  try {
    const esc = await api.post("/api/escenarios", { escenario: E.escenario });
    setEscenario(esc, false);
    toast("Escenario guardado (datos locales, separado de la evidencia).");
  } catch (e) {
    if (e.status === 400 && /solo lectura/.test(e.message)) {
      toast("Los presets y la demo son de solo lectura: se guarda una copia.");
      const copia = structuredClone(E.escenario);
      copia.id = Math.random().toString(16).slice(2, 14);
      copia.tipo = copia.tipo === "PRESET" ? "USUARIO" : copia.tipo;
      copia.nombre = copia.nombre + " (copia)";
      try { setEscenario(await api.post("/api/escenarios", { escenario: copia }), false); } catch (e2) { toast(e2.message, 6000); }
    } else toast(e.message, 6000);
  }
}

window.addEventListener("hashchange", render);
document.getElementById("btn-menu").addEventListener("click", () => document.getElementById("sidebar").classList.toggle("abierta"));
document.getElementById("btn-escenarios").addEventListener("click", () => abrirGestor());
document.getElementById("btn-guardar").addEventListener("click", guardar);
alCambiar(barra);

(async () => {
  try {
    await iniciar();
    pie(); barra(); render();
  } catch (e) {
    document.getElementById("vista").replaceChildren(errorBox(e));
  }
})();

export function irA(ruta) { if (rutaActual() === ruta) render(); else location.hash = "#/" + ruta; }
window.__app = { E, irA, render };
