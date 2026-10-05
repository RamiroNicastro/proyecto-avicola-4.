// Primer uso («¿Querés un recorrido de 2 minutos?») y RECORRIDO DE DEMOSTRACIÓN sobre DEMO_ARTIFICIAL.
// Es solo un tutorial: navega y explica; no carga datos ni cambia el escenario salvo abrir la demo cuando se pide.
import { api } from "./api.js";
import { E, setEscenario } from "./estado.js";
import { h, modal } from "./ui.js";

const CLAVE_PRIMER_USO = "avicola.app.primer_uso";
const CLAVE_TOUR = "avicola.app.tour_paso";

export const PASOS_TOUR = [
  { id: "escenario", ruta: "simular", titulo: "1 · El escenario",
    texto: "Esto es un escenario: las respuestas a 5 preguntas (objetivo, capital, demanda, alternativa y precios). En la demo ya están cargadas con datos FICTICIOS. Recorré los pasos con CONTINUAR." },
  { id: "resultado", ruta: "simular", titulo: "2 · El resultado",
    texto: "En el último paso tocá SIMULAR. Arriba vas a ver una frase con la conclusión y hasta 6 números clave. Cada número tiene un «?» que explica qué significa." },
  { id: "comparacion", ruta: "comparar", titulo: "3 · Comparar",
    texto: "Elegí dos alternativas (por ejemplo C0 y C1 a 10.000 aves/día) y tocá COMPARAR para verlas lado a lado." },
  { id: "stress", ruta: "riesgos?tab=stress", titulo: "4 · ¿Y si algo sale mal?",
    texto: "Ahora probemos qué pasa si sube el alimento. Tocá EJECUTAR STRESS: el motor recalcula el resultado con el alimento más caro." },
  { id: "optimizador", ruta: "optimizar", titulo: "5 · Buscar la mejor alternativa",
    texto: "El optimizador prueba todas las arquitecturas y escalas y te dice cuál cumple mejor tu objetivo DENTRO de la simulación. «No invertir todavía» también es un resultado posible." },
  { id: "validacion", ruta: "validacion", titulo: "6 · Qué falta para decidir de verdad",
    texto: "Con datos reales, esto es lo que habría que conseguir: una lista de pedidos por tema (clientes, planta, alimento…). Ninguno está validado todavía." },
];

function leer(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function escribir(k, v) { try { if (v === null) localStorage.removeItem(k); else localStorage.setItem(k, v); } catch (e) { /* sin almacenamiento */ } }

let paso = (() => { const v = leer(CLAVE_TOUR); return v === null ? null : Number(v); })();

export function primerUso() {
  if (leer(CLAVE_PRIMER_USO)) return;
  const cerrar = modal(h("div", { "data-primer-uso": "" }, h("div", { style: { fontSize: "40px" } }, "🐔"),
    h("h2", {}, "¿QUERÉS UN RECORRIDO DE 2 MINUTOS?"),
    h("p", {}, "Te mostramos cómo funciona la app con un ejemplo de datos ficticios: cómo se arma un escenario, cómo leer el resultado y qué falta validar."),
    h("div", { class: "fila-btn" },
      h("button", { class: "btn btn-primario btn-grande", "data-empezar-recorrido": "", onclick: async () => { escribir(CLAVE_PRIMER_USO, "recorrido"); cerrar(); await empezarTour(); } }, "EMPEZAR RECORRIDO"),
      h("button", { class: "btn btn-grande", "data-ir-directo": "", onclick: () => { escribir(CLAVE_PRIMER_USO, "directo"); cerrar(); } }, "IR DIRECTO A LA APP"))),
  { sinCerrar: true });
}

export async function empezarTour() {
  if (!E.escenario?.solo_demostracion) setEscenario(await api.get("/api/escenarios/demo_artificial"), false);
  irPaso(0);
}

function irPaso(n) {
  paso = n;
  escribir(CLAVE_TOUR, n === null ? null : String(n));
  if (n !== null && n < PASOS_TOUR.length) {
    const destino = "#/" + PASOS_TOUR[n].ruta;
    if (location.hash !== destino) location.hash = destino; else refrescarTour();
  } else refrescarTour();
}

export function refrescarTour() {
  const t = document.getElementById("tour");
  if (!t) return;
  if (paso === null || Number.isNaN(paso)) { t.hidden = true; t.replaceChildren(); return; }
  if (paso >= PASOS_TOUR.length) {
    t.hidden = false;
    t.replaceChildren(h("div", { "data-tour-fin": "" }, h("h3", {}, "¡Recorrido completo!"),
      h("p", {}, "Ya viste el ciclo: escenario → resultado → comparación → riesgo → optimizador → validación. Recordá: todo lo de la demo es ficticio."),
      h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario", "data-tour-cerrar": "", onclick: () => irPaso(null) }, "Cerrar"),
        h("a", { class: "btn", href: "#/inicio", onclick: () => irPaso(null) }, "Ir al inicio"))));
    return;
  }
  const p = PASOS_TOUR[paso];
  t.hidden = false;
  t.replaceChildren(h("div", { "data-tour-paso": p.id },
    h("div", { class: "peq mut" }, `RECORRIDO DE DEMOSTRACIÓN · paso ${paso + 1} de ${PASOS_TOUR.length}`), h("h3", {}, p.titulo), h("p", {}, p.texto),
    h("div", { class: "fila-btn" },
      paso > 0 ? h("button", { class: "btn", onclick: () => irPaso(paso - 1) }, "← Atrás") : null,
      h("button", { class: "btn btn-primario", "data-tour-siguiente": "", onclick: () => irPaso(paso + 1) }, paso === PASOS_TOUR.length - 1 ? "Terminar" : "Siguiente →"),
      h("button", { class: "btn-link", onclick: () => irPaso(null) }, "Salir del recorrido"))));
}

// Banner que aparece cuando está abierta la demo (y no hay un recorrido en curso).
export function bannerDemo() {
  if (!E.escenario?.solo_demostracion || (paso !== null && !Number.isNaN(paso))) return null;
  return h("div", { class: "banner banner-demo banner-tour", "data-banner-recorrido": "" },
    h("div", {}, h("b", {}, "✱ Recorrido de demostración"), "Estás viendo la DEMO: todos los números son ficticios. ¿Querés que te guiemos paso a paso?"),
    h("div", { class: "fila-btn" }, h("button", { class: "btn btn-primario", "data-guiarme": "", onclick: () => irPaso(0) }, "GUIARME")));
}
