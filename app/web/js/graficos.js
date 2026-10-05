// Gráficos SVG mínimos (sin librerías; funcionan offline). Un valor null NUNCA se dibuja como 0: se marca "sin dato".
import { h, fmt } from "./ui.js";

const NS = "http://www.w3.org/2000/svg";
function s(tag, attrs = {}, ...hijos) {
  const el = document.createElementNS(NS, tag);
  for (const [k, v] of Object.entries(attrs)) if (v !== null && v !== undefined) el.setAttribute(k, v);
  for (const c of hijos.flat()) if (c !== null && c !== undefined) el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  return el;
}
const COLORES = ["var(--c1)", "var(--c2)", "var(--c3)", "var(--c4)", "var(--c5)", "var(--c6)"];
const titulo = (t) => s("title", {}, t);

function escala(min, max, a, b) {
  if (max === min) { max = min + 1; }
  return (v) => a + (v - min) * (b - a) / (max - min);
}
function rango(vals) {
  const xs = vals.filter((v) => v !== null && v !== undefined && Number.isFinite(v));
  if (!xs.length) return null;
  let lo = Math.min(0, ...xs), hi = Math.max(0, ...xs);
  if (lo === hi) hi = lo + 1;
  return [lo, hi];
}
function ticks(lo, hi, n = 4) { const out = []; for (let i = 0; i <= n; i++) out.push(lo + (hi - lo) * i / n); return out; }

function leyenda(series) {
  return h("div", { class: "leyenda" }, series.map((se, i) => h("span", {}, h("i", { style: { background: se.color || COLORES[i % 6] } }), se.nombre)));
}

export function sinDatos(texto) {
  return h("div", { class: "banner banner-pend" }, h("span", { class: "ico" }, "∅"), h("div", {}, h("b", {}, "Gráfico no disponible"), texto));
}

// Barras agrupadas por período
export function barras(series, etiquetas, opciones = {}) {
  const todas = series.flatMap((x) => x.valores || []);
  const r = rango(todas);
  if (!r) return sinDatos(opciones.vacio || "No hay valores publicables para graficar.");
  const W = Math.max(560, etiquetas.length * (series.length * 12 + 18) + 90), H = opciones.alto || 240, ml = 88, mb = 28, mt = 10;
  const y = escala(r[0], r[1], H - mb, mt);
  const bw = (W - ml - 10) / etiquetas.length;
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": opciones.titulo || "gráfico de barras" });
  for (const t of ticks(r[0], r[1])) {
    g.append(s("line", { x1: ml, x2: W - 6, y1: y(t), y2: y(t), class: "grid" }), s("text", { x: ml - 6, y: y(t) + 4, "text-anchor": "end" }, fmt(t, opciones.formato || "usd")));
  }
  g.append(s("line", { x1: ml, x2: W - 6, y1: y(0), y2: y(0), class: "eje" }));
  etiquetas.forEach((e, i) => {
    const x0 = ml + i * bw + 4, ancho = (bw - 8) / series.length;
    series.forEach((se, j) => {
      const v = (se.valores || [])[i];
      const x = x0 + j * ancho;
      if (v === null || v === undefined) {
        g.append(s("text", { x: x + ancho / 2, y: y(0) - 3, "text-anchor": "middle", "font-size": 9 }, "∅", titulo(`${se.nombre} · ${e}: sin dato (no publicable)`)));
        return;
      }
      g.append(s("rect", { x, y: Math.min(y(v), y(0)), width: Math.max(1, ancho - 1), height: Math.abs(y(v) - y(0)), fill: se.color || COLORES[j % 6], rx: 1 },
        titulo(`${se.nombre} · ${e}: ${fmt(v, opciones.formato || "usd")}`)));
    });
    if (etiquetas.length <= 24 || i % 2 === 0) g.append(s("text", { x: x0 + (bw - 8) / 2, y: H - 10, "text-anchor": "middle" }, e));
  });
  return h("div", { class: "grafico" }, g, leyenda(series));
}

export function lineas(series, etiquetas, opciones = {}) {
  const todas = series.flatMap((x) => x.valores || []);
  const r = opciones.rango || rango(todas);
  if (!r) return sinDatos(opciones.vacio || "No hay valores publicables para graficar.");
  const W = Math.max(560, etiquetas.length * 36 + 90), H = opciones.alto || 220, ml = 88, mb = 28, mt = 10;
  const y = escala(r[0], r[1], H - mb, mt), x = (i) => ml + 10 + i * (W - ml - 30) / Math.max(1, etiquetas.length - 1);
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  for (const t of ticks(r[0], r[1])) g.append(s("line", { x1: ml, x2: W - 6, y1: y(t), y2: y(t), class: "grid" }), s("text", { x: ml - 6, y: y(t) + 4, "text-anchor": "end" }, fmt(t, opciones.formato || "usd")));
  if (r[0] < 0 && r[1] > 0) g.append(s("line", { x1: ml, x2: W - 6, y1: y(0), y2: y(0), class: "eje" }));
  series.forEach((se, j) => {
    let d = "", abierto = false;
    (se.valores || []).forEach((v, i) => {
      if (v === null || v === undefined) { abierto = false; return; }
      d += (abierto ? "L" : "M") + x(i) + " " + y(v) + " "; abierto = true;
      g.append(s("circle", { cx: x(i), cy: y(v), r: 2.5, fill: se.color || COLORES[j % 6] }, titulo(`${se.nombre} · ${etiquetas[i]}: ${fmt(v, opciones.formato || "usd")}`)));
    });
    g.append(s("path", { d, fill: "none", stroke: se.color || COLORES[j % 6], "stroke-width": 2 }));
  });
  etiquetas.forEach((e, i) => { if (etiquetas.length <= 16 || i % 2 === 0) g.append(s("text", { x: x(i), y: H - 10, "text-anchor": "middle" }, e)); });
  return h("div", { class: "grafico" }, g, leyenda(series));
}

// Tornado: barras horizontales alrededor del valor base (solo filas con SWING)
export function tornado(filas, opciones = {}) {
  const fs = filas.filter((f) => f.SWING !== null && f.SWING !== undefined);
  if (!fs.length) return sinDatos(opciones.vacio || "Sin tornado: la métrica no es publicable en la base.");
  const base = fs[0].BASE;
  const vals = fs.flatMap((f) => [f.VALOR_MIN, f.VALOR_MAX, base]);
  let lo = Math.min(...vals), hi = Math.max(...vals); if (lo === hi) hi = lo + 1;
  const W = 720, fila = 24, ml = 170, H = fs.length * fila + 40;
  const x = escala(lo, hi, ml, W - 20);
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img", "aria-label": "tornado" });
  fs.forEach((f, i) => {
    const yy = 10 + i * fila;
    const a = Math.min(f.VALOR_MIN, f.VALOR_MAX), b = Math.max(f.VALOR_MIN, f.VALOR_MAX);
    g.append(s("text", { x: ml - 8, y: yy + 14, "text-anchor": "end" }, f.VARIABLE));
    const tip = `${f.VARIABLE}\nshock ${f.SHOCK_MIN} → ${fmt(f.VALOR_MIN, opciones.formato || "usd")}\nshock ${f.SHOCK_MAX} → ${fmt(f.VALOR_MAX, opciones.formato || "usd")}\nimpacto (amplitud): ${fmt(f.SWING, opciones.formato || "usd")}`;
    g.append(s("rect", { x: x(a), y: yy + 2, width: Math.max(1, x(Math.min(b, base)) - x(a)), height: fila - 8, fill: "var(--c2)" }, titulo(tip)));
    if (b > base) g.append(s("rect", { x: x(Math.max(a, base)), y: yy + 2, width: Math.max(1, x(b) - x(Math.max(a, base))), height: fila - 8, fill: "var(--c1)" }, titulo(tip)));
  });
  g.append(s("line", { x1: x(base), x2: x(base), y1: 4, y2: H - 26, stroke: "var(--texto)", "stroke-dasharray": "3 2" }));
  g.append(s("text", { x: x(base), y: H - 10, "text-anchor": "middle" }, "base " + fmt(base, opciones.formato || "usd")));
  return h("div", { class: "grafico" }, g, h("div", { class: "leyenda" }, h("span", {}, h("i", { style: { background: "var(--c2)" } }), "por debajo de la base"),
    h("span", {}, h("i", { style: { background: "var(--c1)" } }), "por encima de la base"), h("span", {}, "Pase el cursor: variable, shock e impacto.")));
}

// Heatmap (sensibilidad 2D). Colores divergentes por signo; sin umbrales inventados.
export function heatmap(xs, ys, valor, opciones = {}) {
  const vals = []; ys.forEach((yv) => xs.forEach((xv) => { const v = valor(xv, yv); if (v !== null && v !== undefined) vals.push(v); }));
  if (!vals.length) return sinDatos(opciones.vacio || "Sin valores calculables.");
  const mx = Math.max(...vals.map(Math.abs)) || 1;
  const cw = 92, ch = 34, ml = 96, mt = 30;
  const W = ml + xs.length * cw + 10, H = mt + ys.length * ch + 30;
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  xs.forEach((xv, i) => g.append(s("text", { x: ml + i * cw + cw / 2, y: 18, "text-anchor": "middle" }, opciones.fx ? opciones.fx(xv) : xv)));
  ys.forEach((yv, j) => {
    g.append(s("text", { x: ml - 8, y: mt + j * ch + ch / 2 + 4, "text-anchor": "end" }, opciones.fy ? opciones.fy(yv) : yv));
    xs.forEach((xv, i) => {
      const v = valor(xv, yv);
      const t = v === null || v === undefined ? 0 : Math.min(1, Math.abs(v) / mx);
      const color = v === null || v === undefined ? "var(--gris-suave)" : (v >= 0 ? `rgba(26,127,55,${0.12 + 0.6 * t})` : `rgba(198,40,40,${0.12 + 0.6 * t})`);
      g.append(s("rect", { x: ml + i * cw + 1, y: mt + j * ch + 1, width: cw - 2, height: ch - 2, fill: color, rx: 3 },
        titulo(`${opciones.nx || "x"} ${opciones.fx ? opciones.fx(xv) : xv} × ${opciones.ny || "y"} ${opciones.fy ? opciones.fy(yv) : yv}: ${v === null || v === undefined ? "no calculable" : fmt(v, opciones.formato || "usd")}`)));
      g.append(s("text", { x: ml + i * cw + cw / 2, y: mt + j * ch + ch / 2 + 4, "text-anchor": "middle", style: "font-weight:600" },
        v === null || v === undefined ? "∅" : fmt(v, opciones.formato || "usd")));
    });
  });
  g.append(s("text", { x: ml, y: H - 6 }, `${opciones.nx || "x"} → columnas · ${opciones.ny || "y"} → filas`));
  return h("div", { class: "grafico" }, g);
}

export function dispersion(puntos, opciones = {}) {
  const ps = puntos.filter((p) => p.x !== null && p.y !== null && p.x !== undefined && p.y !== undefined);
  if (ps.length < 2) return sinDatos(opciones.vacio || "PARETO NO INFORMATIVO: menos de 2 alternativas comparables.");
  const W = 640, H = 320, ml = 84, mb = 40, mt = 12;
  let [x0, x1] = [Math.min(...ps.map((p) => p.x)), Math.max(...ps.map((p) => p.x))];
  let [y0, y1] = [Math.min(...ps.map((p) => p.y)), Math.max(...ps.map((p) => p.y))];
  const dx = (x1 - x0) * 0.08 || 1, dy = (y1 - y0) * 0.08 || 1; x0 -= dx; x1 += dx; y0 -= dy; y1 += dy;
  const X = escala(x0, x1, ml, W - 14), Y = escala(y0, y1, H - mb, mt);
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  for (const t of ticks(y0, y1)) g.append(s("line", { x1: ml, x2: W - 10, y1: Y(t), y2: Y(t), class: "grid" }), s("text", { x: ml - 6, y: Y(t) + 4, "text-anchor": "end" }, fmt(t, opciones.fy || "usd")));
  for (const t of ticks(x0, x1)) g.append(s("text", { x: X(t), y: H - mb + 16, "text-anchor": "middle" }, fmt(t, opciones.fx || "usd")));
  const fr = ps.filter((p) => p.frontera).sort((a, b) => a.x - b.x);
  if (fr.length > 1) g.append(s("path", { d: fr.map((p, i) => (i ? "L" : "M") + X(p.x) + " " + Y(p.y)).join(" "), fill: "none", stroke: "var(--acento)", "stroke-dasharray": "4 3" }));
  ps.forEach((p) => g.append(s("circle", { cx: X(p.x), cy: Y(p.y), r: p.frontera ? 6 : 4, fill: p.frontera ? "var(--acento)" : "var(--gris)", opacity: .85 },
    titulo(`${p.label}\n${opciones.nx}: ${fmt(p.x, opciones.fx || "usd")}\n${opciones.ny}: ${fmt(p.y, opciones.fy || "usd")}${p.frontera ? "\nEN FRONTERA" : ""}`))));
  g.append(s("text", { x: (ml + W) / 2, y: H - 6, "text-anchor": "middle" }, opciones.nx), s("text", { x: 12, y: mt + 8 }, opciones.ny));
  return h("div", { class: "grafico" }, g, h("div", { class: "leyenda" }, h("span", {}, h("i", { style: { background: "var(--acento)" } }), "en la frontera"),
    h("span", {}, h("i", { style: { background: "var(--gris)" } }), "dominada en este par"), h("span", {}, "La frontera no es un ranking.")));
}

export function histograma(valores, opciones = {}) {
  if (!valores || valores.length < 2) return sinDatos("Sin muestras.");
  const n = opciones.bins || 20, lo = Math.min(...valores), hi = Math.max(...valores), w = (hi - lo) / n || 1;
  const cuentas = Array(n).fill(0);
  valores.forEach((v) => { cuentas[Math.min(n - 1, Math.floor((v - lo) / w))]++; });
  const W = 640, H = 220, ml = 40, mb = 32, mt = 10, mx = Math.max(...cuentas);
  const g = s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: "img" });
  const bw = (W - ml - 10) / n;
  cuentas.forEach((c, i) => {
    const a = lo + i * w;
    g.append(s("rect", { x: ml + i * bw + 1, y: H - mb - (H - mb - mt) * c / mx, width: bw - 2, height: (H - mb - mt) * c / mx,
      fill: a + w <= 0 ? "var(--mal)" : "var(--c1)" }, titulo(`${fmt(a, "usd")} a ${fmt(a + w, "usd")}: ${c} simulaciones`)));
  });
  [[lo, "start"], [(lo + hi) / 2, "middle"], [hi, "end"]].forEach(([t, a]) => g.append(s("text", { x: ml + (t - lo) / (hi - lo || 1) * (W - ml - 10), y: H - 10, "text-anchor": a }, fmt(t, "usd"))));
  return h("div", { class: "grafico" }, g, h("div", { class: "leyenda" }, h("span", {}, "Distribución SIMULADA del VAN (no es probabilidad real ni histórica)")));
}

export function barraProgreso(pct) {
  return h("div", { class: "barra-p", role: "progressbar", "aria-valuenow": pct ?? 0, "aria-valuemin": 0, "aria-valuemax": 100 },
    h("span", { style: { width: `${Math.max(0, Math.min(100, pct || 0))}%` } }));
}
