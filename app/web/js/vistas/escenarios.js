// Gestor de escenarios guardados (#33): guardar, duplicar, renombrar, eliminar, exportar, importar (JSON versionado).
import { api } from "../api.js";
import { E, setEscenario } from "../estado.js";
import { h, etq, modal, toast, descargar, confirmar, errorBox } from "../ui.js";

export async function abrirGestor() {
  const cont = h("div", {}, h("h2", {}, "Escenarios"), h("p", { class: "mut" },
    "Los escenarios se guardan en app/datos_locales/ (JSON versionado), separados de la evidencia del proyecto. Los presets y la demo son de solo lectura."));
  const lista = h("div");
  const cerrar = modal(h("div", {}, cont, lista));
  async function pintar() {
    let filas;
    try { filas = await api.get("/api/escenarios"); } catch (e) { lista.replaceChildren(errorBox(e)); return; }
    const acciones = h("div", { class: "fila-btn" },
      h("button", { class: "btn btn-primario", "data-accion": "nuevo", onclick: async () => {
        const nombre = prompt("Nombre del escenario nuevo:", "Mi escenario");
        if (nombre === null) return;
        setEscenario(await api.post("/api/nuevo", { nombre }), true); cerrar(); location.hash = "#/simular";
      } }, "Nuevo escenario"),
      h("label", { class: "btn" }, "Importar JSON…", h("input", { type: "file", accept: ".json,application/json", class: "oculto", "data-importar": "",
        onchange: async (ev) => {
          const f = ev.target.files[0]; if (!f) return;
          try {
            const obj = JSON.parse(await f.text());
            const esc = await api.post("/api/escenarios/importar", { escenario: obj });
            setEscenario(esc, false); toast("Escenario importado: " + esc.nombre); pintar();
          } catch (e) { toast("No se pudo importar: " + e.message, 7000); }
        } })),
      h("button", { class: "btn", "data-accion": "exportar-actual", onclick: async () => {
        const j = await api.post("/api/exportar/json", { escenario: E.escenario });
        descargar(`escenario_${(E.escenario.nombre || "sin_nombre").replace(/[^\w-]+/g, "_")}.json`, JSON.stringify(j, null, 1));
      } }, "Exportar el actual (JSON)"));
    lista.replaceChildren(acciones, h("div", { class: "tabla-env" }, h("table", { class: "t" },
      h("thead", {}, h("tr", {}, ["Nombre", "Tipo", "Origen", "Modificado", ""].map((x) => h("th", {}, x)))),
      h("tbody", {}, filas.map((f) => h("tr", { "data-escenario": f.id },
        h("td", {}, h("b", {}, f.nombre), f.descripcion ? h("div", { class: "mut peq" }, f.descripcion) : null),
        h("td", {}, f.solo_demostracion ? etq("DEMO") : etq("INFO", f.tipo)), h("td", {}, f.origen), h("td", { class: "peq" }, f.modificado || ""),
        h("td", {}, h("div", { class: "fila-btn" },
          h("button", { class: "btn", "data-accion": "abrir", onclick: async () => { setEscenario(await api.get("/api/escenarios/" + f.id), false); cerrar(); toast("Abierto: " + f.nombre); location.hash = "#/inicio"; } }, "Abrir"),
          h("button", { class: "btn", "data-accion": "duplicar", onclick: async () => {
            const n = prompt("Nombre de la copia:", f.nombre + " (copia)"); if (n === null) return;
            const c = await api.post(`/api/escenarios/${f.id}/duplicar`, { nombre: n }); toast("Duplicado: " + c.nombre); pintar(); } }, "Duplicar"),
          f.origen === "GUARDADO" ? h("button", { class: "btn", "data-accion": "renombrar", onclick: async () => {
            const n = prompt("Nuevo nombre:", f.nombre); if (!n) return;
            const c = await api.post(`/api/escenarios/${f.id}/renombrar`, { nombre: n }); if (E.escenario.id === f.id) setEscenario(c, false); pintar(); } }, "Renombrar") : null,
          h("button", { class: "btn", "data-accion": "exportar", onclick: async () => {
            const esc = await api.get("/api/escenarios/" + f.id); const j = await api.post("/api/exportar/json", { escenario: esc });
            descargar(`escenario_${f.id}.json`, JSON.stringify(j, null, 1)); } }, "Exportar"),
          f.origen === "GUARDADO" ? h("button", { class: "btn btn-peligro", "data-accion": "eliminar", onclick: async () => {
            if (!(await confirmar("Eliminar escenario", `¿Eliminar «${f.nombre}»? No afecta la evidencia del proyecto.`, "Eliminar"))) { abrirGestor(); return; }
            await api.borrar("/api/escenarios/" + f.id); toast("Eliminado."); abrirGestor(); } }, "Eliminar") : null))))))));
  }
  pintar();
}
