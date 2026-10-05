// Markdown → HTML mínimo y seguro (sin dependencias) para «VER DETALLE TÉCNICO».
// Soporta títulos, párrafos, listas, citas, tablas, bloques de código, negrita, cursiva y código en línea.
// Los enlaces se muestran como texto (los documentos se abren desde la app, no por ruta).
const esc = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function enLinea(t) {
  let s = esc(t);
  s = s.replace(/`([^`]+)`/g, "<code>$1</code>");
  s = s.replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");
  s = s.replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
  s = s.replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, "$1<i>$2</i>");
  return s;
}

export function markdown(texto) {
  const L = String(texto || "").replace(/\r/g, "").split("\n");
  const out = [];
  let i = 0;
  while (i < L.length) {
    const l = L[i];
    if (/^```/.test(l)) {
      const buf = [];
      i++;
      while (i < L.length && !/^```/.test(L[i])) buf.push(L[i++]);
      i++;
      out.push(`<pre>${esc(buf.join("\n"))}</pre>`);
      continue;
    }
    const hd = l.match(/^(#{1,6})\s+(.*)$/);
    if (hd) { const n = Math.min(hd[1].length + 1, 4); out.push(`<h${n}>${enLinea(hd[2])}</h${n}>`); i++; continue; }
    if (/^\s*\|/.test(l)) {
      const filas = [];
      while (i < L.length && /^\s*\|/.test(L[i])) filas.push(L[i++]);
      const celdas = (f) => f.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      const cuerpo = filas.filter((f) => !/^\s*\|[\s:|-]+\|\s*$/.test(f));
      out.push("<table>" + cuerpo.map((f, k) => "<tr>" + celdas(f).map((c) => (k === 0 ? `<th>${enLinea(c)}</th>` : `<td>${enLinea(c)}</td>`)).join("") + "</tr>").join("") + "</table>");
      continue;
    }
    if (/^\s*([-*]|\d+\.)\s+/.test(l)) {
      const ord = /^\s*\d+\./.test(l);
      const items = [];
      while (i < L.length && /^\s*([-*]|\d+\.)\s+/.test(L[i])) items.push(L[i++].replace(/^\s*([-*]|\d+\.)\s+/, ""));
      out.push(`<${ord ? "ol" : "ul"}>` + items.map((x) => `<li>${enLinea(x)}</li>`).join("") + `</${ord ? "ol" : "ul"}>`);
      continue;
    }
    if (/^>\s?/.test(l)) {
      const buf = [];
      while (i < L.length && /^>\s?/.test(L[i])) buf.push(L[i++].replace(/^>\s?/, ""));
      out.push(`<blockquote class="cita">${enLinea(buf.join(" "))}</blockquote>`);
      continue;
    }
    if (/^\s*(---|\*\*\*)\s*$/.test(l)) { out.push("<hr>"); i++; continue; }
    if (!l.trim()) { i++; continue; }
    const buf = [];
    while (i < L.length && L[i].trim() && !/^(#|```|\s*\||\s*([-*]|\d+\.)\s+|>)/.test(L[i])) buf.push(L[i++]);
    out.push(`<p>${enLinea(buf.join(" "))}</p>`);
  }
  return out.join("\n");
}
