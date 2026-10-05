// Estado de la interfaz: escenario actual + resultados ya pedidos (se invalidan al cambiar un input).
import { api } from "./api.js";

const CLAVE = "avicola.app.escenario_actual";
const oyentes = new Set();

export const E = {
  catalogo: null, estado: null, escenario: null, sinGuardar: false,
  res: {},              // resultados del escenario actual por operación (se descartan al editar)
  alternativa: null,    // alternativa elegida para riesgos / detalle
};

export function alCambiar(fn) { oyentes.add(fn); return () => oyentes.delete(fn); }
function avisar() { oyentes.forEach((f) => { try { f(); } catch (e) { console.error(e); } }); }

function persistir() {
  try { localStorage.setItem(CLAVE, JSON.stringify({ esc: E.escenario, sinGuardar: E.sinGuardar })); } catch (e) { /* almacenamiento no disponible */ }
}

export function setEscenario(esc, sinGuardar = false) {
  E.escenario = esc; E.sinGuardar = sinGuardar; E.res = {}; E.alternativa = null;
  persistir(); avisar();
}

// Toda edición pasa por aquí: invalida los resultados (nunca se muestran resultados de otro escenario).
export function editar(fn) {
  fn(E.escenario);
  E.escenario.modificado = new Date().toISOString().slice(0, 19);
  E.sinGuardar = true; E.res = {};
  persistir(); avisar();
}

export async function iniciar() {
  const [cat, est] = await Promise.all([api.get("/api/catalogo"), api.get("/api/estado")]);
  E.catalogo = cat; E.estado = est;
  let guardado = null;
  try { guardado = JSON.parse(localStorage.getItem(CLAVE) || "null"); } catch (e) { guardado = null; }
  if (guardado?.esc) {
    try { E.escenario = await api.post("/api/validar", { escenario: guardado.esc }); E.sinGuardar = !!guardado.sinGuardar; }
    catch (e) { E.escenario = null; }
  }
  if (!E.escenario) E.escenario = await api.post("/api/nuevo", { nombre: "Escenario nuevo" }), E.sinGuardar = true;
  avisar();
}

export async function pedir(op, ruta, extra = {}) {
  const clave = op + JSON.stringify(extra);
  if (E.res[clave]) return E.res[clave];
  const r = await api.post(ruta, { escenario: E.escenario, ...extra });
  E.res[clave] = r;
  return r;
}

export function esDemo() { return !!E.escenario?.solo_demostracion; }
export function universoTexto() { return esDemo() ? "DEMO_ARTIFICIAL" : "ESCENARIO"; }
