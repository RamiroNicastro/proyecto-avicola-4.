// Generador de la presentación ejecutiva V1 (26_presentacion).
// Produce: presentacion_nicas_doipe_v1.pptx y guion_presentacion.md (las notas del presentador viven SOLO aquí).
// Uso:  NODE_PATH=<carpeta con node_modules> node 26_presentacion/generar_presentacion.js
// Dependencias npm: pptxgenjs, react, react-dom, react-icons, sharp. Ver README.md de esta carpeta.
// Todas las cifras salen de documentos del repo; su fuente está en fuentes_y_trazabilidad_presentacion.csv.
// No se inventan montos de CAPEX/OPEX ni resultados económicos: el deck solo muestra estructura, estados y estimaciones físicas rotuladas.

const path = require("path");
const fs = require("fs");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fa = require("react-icons/fa");
const gi = require("react-icons/gi");

const DIR = __dirname;
const SALIDA = path.join(DIR, "presentacion_nicas_doipe_v1.pptx");
const GUION = path.join(DIR, "guion_presentacion.md");
const CAP = (n) => path.join(DIR, "capturas", n);

// ---------- Paleta (verde campo + amarillo yema; estados con color propio) ----------
const K = {
  osc: "1F4D3A",   // verde oscuro principal
  txt: "1E2B24",   // texto
  gris: "5F6B66",  // texto secundario
  claro: "EAF2EC", // tinte verde claro
  linea: "C9D6CE",
  blanco: "FFFFFF",
  yema: "E3A12F",  // acento
  yemaClaro: "FBF1DC",
  evid: "2E7D4F",  // EVIDENCIA
  esti: "2F6690",  // ESTIMACIÓN
  esce: "6B4FA0",  // ESCENARIO
  pend: "C8641E",  // PENDIENTE
  rojo: "B3261E",
  rojoClaro: "F8E3E1",
  violetaClaro: "EEE9F6",
  azulClaro: "E4EEF5",
};
const THEME = {
  name: "Nicas Doipe V1",
  headFontFace: "Calibri",
  bodyFontFace: "Calibri",
  colors: {
    dk1: K.txt, lt1: K.blanco, dk2: K.gris, lt2: K.claro,
    accent1: K.osc, accent2: K.yema, accent3: K.evid, accent4: K.esce, accent5: K.pend, accent6: K.rojo,
    hlink: K.esti, folHlink: K.esce,
  },
};
const ETIQ = {
  EVIDENCIA: { fill: K.evid, desc: "dato real con fuente verificada" },
  "ESTIMACIÓN": { fill: K.esti, desc: "cálculo del modelo, sin validar en campo" },
  ESCENARIO: { fill: K.esce, desc: "hipótesis para simular; no es un dato" },
  PENDIENTE: { fill: K.pend, desc: "falta el dato o la decisión" },
};

const W = 13.333;
const FOOT = "Proyecto avícola Nicas & Doipe · Paquete ejecutivo V1 · 2026-10-05 · Documento de estudio: no es una recomendación de inversión";

// ---------- Íconos ----------
const cacheIconos = {};
async function icono(nombre, color) {
  const clave = nombre + color;
  if (cacheIconos[clave]) return cacheIconos[clave];
  const C = fa[nombre] || gi[nombre];
  if (!C) throw new Error("ícono inexistente: " + nombre);
  const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(C, { color: "#" + color, size: 256 }));
  const buf = await sharp(Buffer.from(svg)).resize(256, 256).png().toBuffer();
  return (cacheIconos[clave] = "image/png;base64," + buf.toString("base64"));
}

// ---------- Presentación ----------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.author = "Proyecto avícola Nicas y Doipe";
pres.company = "Nicas &amp; Doipe";
pres.title = "Proyecto avícola Nicas & Doipe — Paquete ejecutivo V1";
pres.subject = "Motor V1 + App V1: estado del estudio de prefactibilidad";
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };

pres.defineSlideMaster({
  title: "PORTADA",
  background: { color: K.osc },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 1.55, w: 8.4, h: 1.7, fontSize: 44, bold: true, color: K.blanco, align: "left", valign: "bottom", margin: 0 }, text: "" } },
  ],
});
pres.defineSlideMaster({
  title: "CONTENIDO",
  background: { color: K.blanco },
  margin: [0.4, 0.6, 0.6, 0.6],
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 0.38, w: 9.6, h: 0.85, fontSize: 32, bold: true, color: K.osc, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.02, w: 11.2, h: 0.3, fontSize: 10, color: K.gris, margin: 0 } } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: K.gris, align: "right" },
});
pres.defineSlideMaster({
  title: "SECCION",
  background: { color: K.osc },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 2.6, w: 11.9, h: 1.2, fontSize: 44, bold: true, color: K.blanco, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.02, w: 11.2, h: 0.3, fontSize: 10, color: "B9CCC0", margin: 0 } } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: "B9CCC0", align: "right" },
});

pres.defineSlideMaster({
  title: "CIERRE",
  background: { color: K.osc },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.7, y: 0.75, w: 8.4, h: 1.0, fontSize: 44, bold: true, color: K.blanco, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: { text: FOOT, options: { x: 0.6, y: 7.02, w: 11.2, h: 0.3, fontSize: 10, color: "B9CCC0", margin: 0 } } },
  ],
  slideNumber: { x: 12.23, y: 7.02, w: 0.5, h: 0.3, fontSize: 10, color: "B9CCC0", align: "right" },
});

const guion = []; // { n, titulo, mensaje, notas }
let nSlide = 0;
function registrar(slide, titulo, mensaje, notas) {
  nSlide += 1;
  slide.addNotes(notas);
  guion.push({ n: nSlide, titulo, mensaje, notas });
}

// ---------- Helpers de dibujo ----------
const sombra = () => ({ type: "outer", color: "000000", blur: 6, offset: 1.5, angle: 90, opacity: 0.12 });
function tarjeta(s, x, y, w, h, fill = K.blanco, conSombra = true, nombre = "tarjeta") {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: fill === K.blanco ? K.linea : fill, width: 0.75 },
    shadow: conSombra ? sombra() : undefined, objectName: nombre,
  });
}
function texto(s, t, o) { s.addText(t, Object.assign({ isTextBox: true, margin: 0, fontSize: 14, color: K.txt, valign: "top" }, o)); }
function chip(s, x, y, tipo, w) {
  const e = ETIQ[tipo];
  const ancho = w || (0.32 + tipo.length * 0.105);
  s.addText(tipo, { isTextBox: true, x, y, w: ancho, h: 0.3, fontSize: 10.5, bold: true, color: K.blanco, align: "center", valign: "middle",
    margin: 0, charSpacing: 1, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, fill: { color: e.fill }, objectName: "etiqueta " + tipo });
  return ancho;
}
function chipsArriba(s, tipos) { // alineadas a la derecha, a la altura del título
  let x = W - 0.6;
  const anchos = tipos.map((t) => 0.32 + t.length * 0.105);
  for (let i = tipos.length - 1; i >= 0; i--) { x -= anchos[i]; chip(s, x, 0.66, tipos[i]); x -= 0.1; }
}
async function circuloIcono(s, nombre, x, y, d, fondo, color) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fondo }, line: { color: fondo }, objectName: "círculo " + nombre });
  const pad = d * 0.24;
  s.addImage({ data: await icono(nombre, color), x: x + pad, y: y + pad, w: d - 2 * pad, h: d - 2 * pad, altText: nombre });
}
function flecha(s, x1, y1, x2, y2, color = K.gris, w = 1.5) {
  s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.0001, h: Math.abs(y2 - y1) || 0.0001,
    flipH: x2 < x1, flipV: y2 < y1, line: { color, width: w, endArrowType: "triangle" } });
}
function linea(s, x1, y1, x2, y2, color = K.gris, w = 1.5) {
  s.addShape(pres.shapes.LINE, { x: Math.min(x1, x2), y: Math.min(y1, y2), w: Math.abs(x2 - x1) || 0.0001, h: Math.abs(y2 - y1) || 0.0001,
    flipH: x2 < x1, flipV: y2 < y1, line: { color, width: w } });
}
function contenido(titulo, seccion) {
  const s = pres.addSlide({ masterName: "CONTENIDO", sectionTitle: seccion });
  s.addText(titulo, { placeholder: "title" });
  return s;
}
const bullets = (items, o = {}) => items.map((t, i) => ({ text: t, options: Object.assign({ bullet: { indent: 16 }, breakLine: i < items.length - 1, paraSpaceAfter: 6 }, o) }));

// =====================================================================================
async function construir() {
  // ---------------- SECCIÓN 1: mensaje ----------------
  pres.addSection({ title: "Mensaje" });

  // 1. Portada
  {
    const s = pres.addSlide({ masterName: "PORTADA", sectionTitle: "Mensaje" });
    s.addText("Proyecto avícola Nicas & Doipe", { placeholder: "title" });
    texto(s, "Motor V1 + App V1 · Paquete ejecutivo", { x: 0.7, y: 3.4, w: 8.4, h: 0.6, fontSize: 26, bold: true, color: K.yema });
    texto(s, "Estudio de prefactibilidad · Fase 0 · Argentina · 2026-10-05", { x: 0.7, y: 4.05, w: 8.4, h: 0.4, fontSize: 16, color: "D7E4DB" });
    const estados = [["MOTOR V1", "COMPLETO ESTRUCTURALMENTE", K.evid], ["APP V1", "LISTA", K.evid], ["DECISIÓN REAL", "TODAVÍA NO", K.rojo]];
    let x = 0.7;
    for (const [a, b, c] of estados) {
      const w = 0.5 + (a.length + b.length) * 0.115;
      s.addText([{ text: a + "  ", options: { bold: false, color: "D7E4DB" } }, { text: b, options: { bold: true, color: K.blanco } }],
        { isTextBox: true, x, y: 5.15, w, h: 0.42, fontSize: 13, align: "center", valign: "middle", margin: 0, shape: pres.shapes.ROUNDED_RECTANGLE,
          rectRadius: 0.2, fill: { color: c }, objectName: "estado " + a });
      x += w + 0.18;
    }
    texto(s, "Documento de estudio. No contiene una recomendación de inversión ni resultados económicos reales.", { x: 0.7, y: 6.55, w: 9, h: 0.35, fontSize: 12, color: "B9CCC0" });
    s.addShape(pres.shapes.OVAL, { x: 9.55, y: 1.45, w: 3.2, h: 3.2, fill: { color: "2C6650" }, line: { color: "2C6650" }, objectName: "círculo portada" });
    s.addImage({ data: await icono("GiChicken", K.yema), x: 10.2, y: 2.1, w: 1.9, h: 1.9, altText: "pollo" });
    registrar(s, "Portada", "Proyecto avícola Nicas & Doipe: Motor V1 + App V1.",
      "Buenas. Esta presentación resume dónde está el estudio del proyecto avícola Nicas & Doipe. " +
      "Les adelanto el mensaje en una frase: construimos una herramienta completa para analizar el negocio (el Motor V1 y la App V1), " +
      "pero todavía no tenemos los datos reales necesarios para decidir si conviene invertir. " +
      "Hoy no vamos a mostrar cuánto cuesta la planta ni cuánto gana: esos números todavía no existen con respaldo. " +
      "Vamos a mostrar qué se estudió, qué se puede hacer con la herramienta y qué falta conseguir. Duración sugerida: 1 minuto.");
  }

  // 2. Mensaje ejecutivo
  {
    const s = contenido("Mensaje ejecutivo", "Mensaje");
    const tiles = [
      ["FaCogs", "MOTOR V1", "COMPLETO ESTRUCTURALMENTE", "Los 25 módulos del estudio están construidos, conectados entre sí y probados (70 de 70 pruebas de integración).", K.evid, K.claro],
      ["FaLaptop", "APP V1", "LISTA", "Permite entender el proyecto en lenguaje simple y simular escenarios, con un modo experto para análisis.", K.evid, K.claro],
      ["FaPauseCircle", "LISTO PARA DECISIÓN REAL", "NO", "Faltan los datos reales: clientes, precios, cotizaciones y costos. 0 de 180 datos por validar están validados.", K.rojo, K.rojoClaro],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, et, val, desc, col, fondo] = tiles[i];
      const x = 0.6 + i * 4.11;
      tarjeta(s, x, 1.5, 3.89, 2.85, fondo, false);
      await circuloIcono(s, ic, x + 0.3, 1.75, 0.75, col, K.blanco);
      texto(s, et, { x: x + 1.2, y: 1.8, w: 2.55, h: 0.6, fontSize: 13, bold: true, color: K.gris, valign: "middle" });
      texto(s, val, { x: x + 0.3, y: 2.65, w: 3.35, h: 0.6, fontSize: val.length > 10 ? 20 : 28, bold: true, color: col, valign: "middle" });
      texto(s, desc, { x: x + 0.3, y: 3.3, w: 3.35, h: 0.95, fontSize: 13, color: K.txt });
    }
    texto(s, "Tenemos la calculadora. Todavía no tenemos los números reales para cargarle.", { x: 0.6, y: 4.6, w: 12.13, h: 0.7, fontSize: 22, bold: true, color: K.osc, align: "center", valign: "middle",
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, fill: { color: K.yemaClaro } });
    texto(s, "Cómo leer las etiquetas de esta presentación", { x: 0.6, y: 5.55, w: 8, h: 0.35, fontSize: 14, bold: true, color: K.gris });
    let x = 0.6;
    for (const t of ["EVIDENCIA", "ESTIMACIÓN", "ESCENARIO", "PENDIENTE"]) {
      const w = chip(s, x, 6.0, t);
      texto(s, ETIQ[t].desc, { x: x + w + 0.1, y: 5.95, w: 2.95 - w - 0.1 + 0.05, h: 0.45, fontSize: 11, color: K.gris, valign: "middle" });
      x += 3.05;
    }
    registrar(s, "Mensaje ejecutivo", "MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO.",
      "Tres mensajes y nada más. Primero: el motor está completo estructuralmente; es decir, todos los modelos existen, están conectados y pasan sus pruebas. " +
      "Segundo: la app está lista; cualquiera puede usarla sin saber programar. Tercero, y es el más importante: el proyecto NO está listo para una decisión real de inversión. " +
      "No es un problema de la herramienta: es que todavía no hay clientes confirmados, ni precios, ni cotizaciones, ni costos reales. De 180 datos que hay que validar, hoy hay 0 validados. " +
      "Abajo está la clave de colores que vamos a usar en todas las láminas: verde es evidencia real (hoy prácticamente no hay), azul es una estimación del modelo, " +
      "violeta es un escenario hipotético para simular, y naranja es pendiente. Si un número no tiene etiqueta verde, no es un dato real.");
  }

  // 3. Qué estamos intentando construir
  {
    const s = contenido("Qué estamos intentando construir", "Mensaje");
    chipsArriba(s, ["PENDIENTE"]);
    tarjeta(s, 0.6, 1.5, 5.5, 4.6, K.claro, false);
    await circuloIcono(s, "FaStore", 0.9, 1.75, 0.8, K.osc, K.blanco);
    texto(s, "HOY", { x: 1.9, y: 1.8, w: 3.9, h: 0.7, fontSize: 24, bold: true, color: K.osc, valign: "middle" });
    texto(s, bullets([
      "Una carnicería familiar en el AMBA",
      "Sin granjas, planta de faena, terreno ni maquinaria",
      "Capital de referencia: ~USD 2 M de un grupo inversor, no comprometido",
      "Canal posible: red de ~90 supermercados, demanda no validada",
    ]), { x: 0.9, y: 2.8, w: 5.0, h: 3.1, fontSize: 16 });
    s.addImage({ data: await icono("FaArrowRight", K.yema), x: 6.32, y: 3.4, w: 0.7, h: 0.7, altText: "flecha" });
    tarjeta(s, 7.23, 1.5, 5.5, 4.6, K.osc, true);
    await circuloIcono(s, "GiChicken", 7.53, 1.75, 0.8, K.yema, K.osc);
    texto(s, "LO QUE SE ESTUDIA", { x: 8.53, y: 1.8, w: 4.0, h: 0.7, fontSize: 24, bold: true, color: K.blanco, valign: "middle" });
    texto(s, bullets([
      "Una empresa avícola argentina integrada, construida por etapas",
      "Vender a supermercados, mayoristas, industria, gastronomía y, a futuro, exportar",
      "Objetivo económico: el mayor ingreso total por cada pollo",
      "Cada eslabón se evalúa: hacerlo, comprarlo, tercerizarlo o postergarlo",
    ]), { x: 7.53, y: 2.8, w: 5.0, h: 3.1, fontSize: 16, color: K.blanco });
    texto(s, "El estudio no parte de «qué entra en USD 2 M»: busca qué escala y qué forma de empezar tienen sentido, y cuánto capital requieren.",
      { x: 0.6, y: 6.3, w: 12.13, h: 0.5, fontSize: 14, italic: true, color: K.gris, align: "center", valign: "middle" });
    registrar(s, "Qué estamos intentando construir", "De una carnicería familiar a una posible empresa avícola integrada, por etapas.",
      "El punto de partida es concreto: una carnicería familiar en el AMBA. No hay granjas, ni frigorífico, ni terreno, ni máquinas. " +
      "Hay un grupo inversor que mencionó unos 2 millones de dólares, pero no están comprometidos: los usamos solo como referencia. " +
      "Y hay una red de unos 90 supermercados que podría ser un canal, pero no sabemos todavía cuánto compraría ni a qué precio. " +
      "Lo que se estudia es si tiene sentido construir, por etapas, una empresa avícola integrada que pueda vender a varios canales y, más adelante, exportar. " +
      "La idea central del negocio es sacar el mayor ingreso posible de cada pollo, vendiendo cada parte donde mejor se paga. " +
      "Y nada se da por sentado: cada eslabón —granjas, alimento, faena, flota— se analiza para ver si conviene hacerlo, comprarlo, tercerizarlo o dejarlo para después.");
  }

  // 4. Cómo funciona el negocio
  {
    const s = contenido("Cómo funciona el negocio", "Mensaje");
    const nodos = [
      ["FaEgg", "Pollito", "Pollito BB de un día, de una incubadora"],
      ["GiBarn", "Granja", "Crianza en galpones hasta el peso de faena"],
      ["GiCorn", "Alimento", "El mayor flujo físico de todo el sistema"],
      ["FaTruck", "Transporte", "Aves vivas de la granja a la planta"],
      ["GiFactory", "Planta", "Faena, enfriamiento, trozado y empaque"],
      ["GiChickenLeg", "Productos", "Entero, trozado, deshuesado, menudencias"],
      ["FaShoppingCart", "Cliente", "Supermercados, mayoristas, industria, gastronomía"],
    ];
    const d = 1.05, paso = (W - 1.2 - d) / 6;
    for (let i = 0; i < nodos.length; i++) {
      const [ic, et, desc] = nodos[i];
      const cx = 0.6 + i * paso;
      await circuloIcono(s, ic, cx, 1.6, d, i === 4 ? K.yema : K.osc, K.blanco);
      texto(s, et, { x: cx - 0.35, y: 2.75, w: d + 0.7, h: 0.4, fontSize: 17, bold: true, color: K.osc, align: "center" });
      texto(s, desc, { x: cx - 0.33, y: 3.17, w: d + 0.66, h: 0.85, fontSize: 12, color: K.gris, align: "center" });
      if (i < nodos.length - 1) flecha(s, cx + d + 0.08, 1.6 + d / 2, cx + paso - 0.08, 1.6 + d / 2, K.yema, 2);
    }
    texto(s, "Ramas que salen de la cadena", { x: 0.6, y: 4.3, w: 6, h: 0.4, fontSize: 16, bold: true, color: K.gris });
    const ramas = [
      ["FaRecycle", "Subproductos", "Plumas, sangre, vísceras y huesos: se venden, se procesan a façon o, a futuro, en un rendering propio"],
      ["FaTint", "Efluentes", "El agua de proceso se trata antes de volcarla; condiciona el terreno"],
      ["FaSnowflake", "Frío", "Cámaras de refrigerado y congelado; une planta, stock y despacho"],
      ["FaShip", "Exportación", "Canal futuro; requiere habilitaciones de SENASA y mercados abiertos"],
    ];
    for (let i = 0; i < 4; i++) {
      const [ic, et, desc] = ramas[i];
      const x = 0.6 + i * 3.08;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 4.8, w: 2.89, h: 1.95, rectRadius: 0.08, fill: { color: K.claro }, line: { color: K.osc, width: 1, dashType: "dash" }, objectName: "rama " + et });
      await circuloIcono(s, ic, x + 0.22, 5.0, 0.6, K.blanco, K.osc);
      texto(s, et, { x: x + 0.95, y: 5.0, w: 1.85, h: 0.6, fontSize: 16, bold: true, color: K.osc, valign: "middle" });
      texto(s, desc, { x: x + 0.22, y: 5.72, w: 2.5, h: 0.95, fontSize: 12, color: K.txt });
    }
    registrar(s, "Cómo funciona el negocio", "La cadena va del pollito al cliente, con ramas de subproductos, efluentes, frío y exportación.",
      "Así funciona el negocio del pollo parrillero, de izquierda a derecha. Se compra o se produce un pollito de un día. Se cría en una granja, en galpones. " +
      "Lo que más se mueve en todo el sistema es el alimento: son miles de toneladas por año. Cuando el pollo llega al peso, se lo transporta vivo a la planta. " +
      "En la planta se faena, se enfría, se corta en trozos y se empaca. Salen productos —pollo entero, cortes, menudencias— que van a distintos clientes. " +
      "Abajo están las ramas que no se ven pero pesan mucho: los subproductos (plumas, sangre, vísceras), el agua sucia que hay que tratar, el frío, y la exportación como canal futuro. " +
      "Cada uno de estos bloques es un tema que se estudió por separado y después se conectó con los demás.");
  }

  // 5. Qué estudiamos
  {
    const s = contenido("Qué estudiamos", "Mensaje");
    chipsArriba(s, ["ESTIMACIÓN", "PENDIENTE"]);
    const temas = [
      ["FaChartLine", "Mercado y demanda", "Canales y categorías de demanda"],
      ["GiBarn", "Producción en granja", "Pollitos, galpones, alimento"],
      ["GiChickenLeg", "Balance de masa", "Qué sale de cada pollo"],
      ["GiFactory", "Planta y proceso", "Etapas, capacidad, zonas"],
      ["FaTools", "Maquinaria", "Equipos conceptuales, sin proveedor"],
      ["FaWater", "Agua y efluentes", "Consumo, vuelco, tratamiento"],
      ["FaBolt", "Energía y frío", "Electricidad, gas, cámaras"],
      ["FaDraftingCompass", "Layout y terreno", "Áreas, zonas, expansión"],
      ["FaTruck", "Logística", "Aves vivas, frío, distribución"],
      ["FaMapMarkedAlt", "Localización", "Regiones y condiciones del terreno"],
      ["FaUsers", "Recursos humanos", "Puestos, turnos, dotación"],
      ["GiCorn", "Alimento e incubación", "Comprar, tercerizar o fabricar"],
      ["FaHardHat", "Inversión (CAPEX)", "Qué hay que comprar y construir"],
      ["FaFileInvoiceDollar", "Costos (OPEX)", "Qué cuesta operar; capital de trabajo"],
      ["FaCalculator", "Finanzas y riesgos", "Rentabilidad, stress, optimizador"],
      ["FaLaptop", "App V1", "Todo lo anterior, en una pantalla"],
    ];
    const tw = 2.9, th = 1.14, gx = 0.177, gy = 0.13;
    for (let i = 0; i < temas.length; i++) {
      const [ic, et, desc] = temas[i];
      const x = 0.6 + (i % 4) * (tw + gx), y = 1.45 + Math.floor(i / 4) * (th + gy);
      tarjeta(s, x, y, tw, th, i === 15 ? K.yemaClaro : K.claro, false);
      await circuloIcono(s, ic, x + 0.18, y + 0.22, 0.7, i === 15 ? K.yema : K.osc, K.blanco);
      texto(s, et, { x: x + 1.02, y: y + 0.14, w: tw - 1.12, h: 0.55, fontSize: 14, bold: true, color: K.osc, valign: "middle" });
      texto(s, desc, { x: x + 1.02, y: y + 0.67, w: tw - 1.12, h: 0.4, fontSize: 11, color: K.gris });
    }
    texto(s, "25 módulos terminados como modelo · ninguno validado todavía con datos de campo", { x: 0.6, y: 6.6, w: 12.13, h: 0.35, fontSize: 14, bold: true, color: K.gris, align: "center" });
    registrar(s, "Qué estudiamos", "Se estudió la cadena completa: de la granja a las finanzas, más una app.",
      "Esto es todo lo que se estudió. No es solo una planilla de costos: se modeló la producción en granja, qué sale de cada pollo, la planta y sus etapas, " +
      "las máquinas necesarias, el agua, los efluentes, la energía, el frío, el terreno, la logística, dónde podría ubicarse la planta, el personal, " +
      "el alimento y la incubación, la inversión, los costos, las finanzas, los riesgos y, al final, una app para usar todo junto. " +
      "Son 25 módulos y todos están terminados como modelo. Pero ninguno está validado con datos de campo: los números físicos son estimaciones del modelo, " +
      "y los números económicos directamente no existen todavía.");
  }

  // ---------------- SECCIÓN 2: el negocio ----------------
  pres.addSection({ title: "El negocio" });

  // 6. Demanda
  {
    const s = contenido("Demanda: posible no es asegurada", "El negocio");
    chipsArriba(s, ["PENDIENTE"]);
    const esc = [
      ["ESCENARIO", "Hipótesis para simular", K.esce],
      ["POTENCIAL", "Canal posible, sin compromiso", "8A6FB8"],
      ["INTERESADA", "Interés sin volumen firme", "8C8C5A"],
      ["NEGOCIADA", "Volumen y precio en conversación", "5E9470"],
      ["ASEGURADA", "Contrato o compra documentada", K.evid],
    ];
    const bw = 1.5, gap = 0.12, base = 6.55;
    for (let i = 0; i < esc.length; i++) {
      const [et, desc, col] = esc[i];
      const h = 1.3 + i * 0.62, x = 0.6 + i * (bw + gap), y = base - h;
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: bw, h, rectRadius: 0.06, fill: { color: col }, line: { color: col }, objectName: "escalón " + et });
      texto(s, et, { x: x + 0.05, y: y + 0.12, w: bw - 0.1, h: 0.35, fontSize: 13, bold: true, color: K.blanco, align: "center" });
      texto(s, desc, { x: x + 0.1, y: y + 0.5, w: bw - 0.2, h: 0.75, fontSize: 11, color: K.blanco, align: "center" });
    }
    // marcador de los 90 supermercados (sobre POTENCIAL)
    const xm = 0.6 + 1 * (bw + gap);
    texto(s, "Los ~90 supermercados están acá hoy", { x: xm - 0.35, y: 2.35, w: 2.2, h: 0.75, fontSize: 13, bold: true, color: K.osc, align: "center", valign: "middle",
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.1, fill: { color: K.yemaClaro }, line: { color: K.yema, width: 1.25 } });
    flecha(s, xm + bw / 2, 3.12, xm + bw / 2, base - (1.3 + 0.62) - 0.05, K.yema, 2);
    texto(s, "más respaldo  →", { x: 0.6, y: 6.6, w: 7.9, h: 0.3, fontSize: 11, color: K.gris, align: "right" });
    // panel derecho
    tarjeta(s, 8.85, 1.5, 3.88, 2.15, K.rojoClaro, false);
    texto(s, "≈ 0", { x: 9.1, y: 1.6, w: 3.4, h: 1.0, fontSize: 54, bold: true, color: K.rojo });
    texto(s, "demanda documentada hoy (asegurada o negociada)", { x: 9.1, y: 2.65, w: 3.4, h: 0.8, fontSize: 14, color: K.txt });
    texto(s, bullets([
      "Con datos reales, el motor solo «vende» lo ASEGURADO.",
      "Todo lo demás se puede simular, siempre rotulado ESCENARIO.",
      "Los supermercados pueden ser cliente ancla, pero no definen ni limitan la escala de la empresa.",
    ]), { x: 8.85, y: 3.9, w: 3.88, h: 2.9, fontSize: 14 });
    registrar(s, "Demanda y mercado", "Los ~90 supermercados son demanda POTENCIAL; la demanda documentada hoy es ≈ 0.",
      "Esta lámina es clave. No toda la demanda vale lo mismo. De izquierda a derecha: un escenario es una hipótesis nuestra para simular. " +
      "Potencial es un canal posible, sin ningún compromiso. Interesada es cuando alguien dice «me interesa», pero sin volumen firme. " +
      "Negociada es cuando ya se habla de volumen y precio. Y asegurada es cuando hay un contrato o una compra documentada. " +
      "Los 90 supermercados hoy están en «potencial»: no sabemos cuánto comprarían, a qué precio, ni con qué plazo de pago. Por eso la demanda documentada hoy es prácticamente cero. " +
      "El motor respeta esto: cuando trabaja con datos reales, solo cuenta como venta lo asegurado. Si queremos imaginar que los supermercados compran, lo podemos simular, pero queda rotulado como escenario. " +
      "Y aunque se confirmen, los supermercados no definen el tamaño de la empresa: pueden ser un cliente ancla, pero el resto del pollo tiene que ir a otros canales.");
  }

  // 7. Alternativas C0–CF
  {
    const s = contenido("Cinco formas de armar el negocio: C0 a CF", "El negocio");
    chipsArriba(s, ["PENDIENTE"]);
    const arq = [
      ["C0", "Arranque liviano", "Compramos pollitos; otro frigorífico faena por nosotros (façon); crían productores integrados.", [["Faena", "tercero"], ["Granjas", "integradas"], ["Pollito", "comprado"], ["Alimento", "a façon"], ["Flota y frío", "terceros"]]],
      ["C1", "Planta de faena propia", "Frigorífico propio; pollito y alimento comprados; granjas de productores integrados.", [["Faena", "propia"], ["Granjas", "integradas"], ["Pollito", "comprado"], ["Alimento", "comprado"], ["Flota", "terceros"]]],
      ["C2", "Integración selectiva", "Frigorífico propio y una parte de las granjas propias (25 % en el caso de referencia).", [["Faena", "propia"], ["Granjas", "mixtas"], ["Pollito", "comprado"], ["Alimento", "a façon"], ["Flota", "mixta"]]],
      ["C3", "Mayor integración", "Frigorífico, granjas, incubadora y planta de alimento propios.", [["Faena", "propia"], ["Granjas", "propias"], ["Pollito", "incubadora propia"], ["Alimento", "planta propia"], ["Flota", "propia"]]],
      ["CF", "Arquitectura futura", "Como C3, más reproductoras y rendering propios. Es una etapa posterior.", [["Todo lo de C3", ""], ["Reproductoras", "futuro"], ["Rendering", "futuro"]]],
    ];
    const cw = 2.3, gap = (12.13 - 5 * cw) / 4;
    for (let i = 0; i < arq.length; i++) {
      const [cod, nom, desc, filas] = arq[i];
      const x = 0.6 + i * (cw + gap), tono = ["DCEBE1", "C7DDCF", "AFCDB9", "8DB89C", "6E9F80"][i];
      tarjeta(s, x, 1.45, cw, 4.45, K.blanco, true, "alternativa " + cod);
      s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: 1.65, w: 0.8, h: 0.8, fill: { color: tono }, line: { color: tono }, objectName: "código " + cod });
      texto(s, cod, { x: x + 0.2, y: 1.65, w: 0.8, h: 0.8, fontSize: 22, bold: true, color: K.osc, align: "center", valign: "middle" });
      texto(s, nom, { x: x + 0.2, y: 2.55, w: cw - 0.4, h: 0.6, fontSize: 15, bold: true, color: K.osc, valign: "middle" });
      texto(s, desc, { x: x + 0.2, y: 3.15, w: cw - 0.4, h: 1.15, fontSize: 11.5, color: K.txt });
      texto(s, filas.map(([a, b], j) => ({ text: b ? a + ": " : a, options: { bold: true, color: K.gris, breakLine: false } })).flatMap((r, j) => {
        const b = filas[j][1];
        const arr = [r];
        if (b) arr.push({ text: b, options: { color: K.txt } });
        if (j < filas.length - 1) arr[arr.length - 1].options.breakLine = true;
        return arr;
      }), { x: x + 0.2, y: 4.35, w: cw - 0.4, h: 1.45, fontSize: 11.5, paraSpaceAfter: 2 });
    }
    // eje
    linea(s, 1.2, 6.2, 12.13, 6.2, K.gris, 1.25);
    flecha(s, 2.5, 6.2, 0.75, 6.2, K.gris, 1.25);
    flecha(s, 10.8, 6.2, 12.6, 6.2, K.gris, 1.25);
    texto(s, "menos inversión propia, más dependencia de terceros", { x: 0.6, y: 6.32, w: 5.5, h: 0.3, fontSize: 12, color: K.gris });
    texto(s, "más inversión propia, más control y complejidad", { x: 7.23, y: 6.32, w: 5.5, h: 0.3, fontSize: 12, color: K.gris, align: "right" });
    texto(s, "Ninguna está elegida · hoy ninguna es costeable: faltan precios y cotizaciones", { x: 0.6, y: 6.62, w: 12.13, h: 0.32, fontSize: 13, bold: true, color: K.pend, align: "center" });
    registrar(s, "Alternativas de negocio C0–CF", "Cinco arquitecturas, de la más liviana (C0) a la más integrada (CF); ninguna elegida ni costeable hoy.",
      "Hay cinco formas de armar la empresa, y las llamamos C0 a CF. " +
      "C0 es el arranque liviano: casi sin activos propios. Compramos pollitos, los crían productores integrados y otro frigorífico los faena por nosotros cobrando una tarifa; eso se llama façon. " +
      "C1 es tener nuestra propia planta de faena, pero seguir comprando pollito y alimento y trabajar con granjas de terceros. " +
      "C2 suma una parte de granjas propias. C3 integra casi todo: granjas, incubadora y planta de alimento. " +
      "Y CF es una visión futura, con reproductoras y procesamiento propio de subproductos. " +
      "De izquierda a derecha aumenta la inversión propia, el control y la complejidad; hacia la izquierda se depende más de terceros. " +
      "Importante: ninguna está elegida, y hoy ninguna se puede costear porque faltan precios. No hay que suponer que la integración total es mejor: eso lo tienen que decir los datos.");
  }

  // 8. Escalas
  {
    const s = contenido("Cuatro escalas de referencia", "El negocio");
    chipsArriba(s, ["ESTIMACIÓN"]);
    const esc = [
      ["2.500", "625.000", "13.200", "3.100", "4,1", "46"],
      ["5.000", "1,25 millones", "26.400", "6.200", "8,2", "91"],
      ["10.000", "2,5 millones", "52.800", "12.400", "16,4", "182"],
      ["20.000", "5 millones", "105.600", "24.700", "32,8", "365"],
    ];
    const cw = 2.86, gap = (12.13 - 4 * cw) / 3;
    for (let i = 0; i < 4; i++) {
      const [e, anio, poll, alim, dem, local] = esc[i];
      const x = 0.6 + i * (cw + gap);
      tarjeta(s, x, 1.45, cw, 3.9, K.blanco, true, "escala " + e);
      texto(s, e, { x: x + 0.25, y: 1.55, w: cw - 0.5, h: 0.75, fontSize: 36, bold: true, color: K.osc });
      texto(s, "aves por día de faena", { x: x + 0.25, y: 2.27, w: cw - 0.5, h: 0.3, fontSize: 12, color: K.gris });
      const filas = [[anio, "aves por año"], [poll, "pollitos por semana"], [alim + " t", "de alimento por año"]];
      filas.forEach(([v, et], j) => {
        texto(s, [{ text: "≈ " + v, options: { bold: true, color: K.txt, breakLine: true } }, { text: et, options: { color: K.gris, fontSize: 11 } }],
          { x: x + 0.25, y: 2.72 + j * 0.62, w: cw - 0.5, h: 0.58, fontSize: 15 });
      });
      texto(s, [{ text: "Para llenarla: ≈ " + dem + " t/día vendidas", options: { bold: true, breakLine: true } }, { text: "≈ " + local + " kg/local/día con 90 locales", options: { color: K.gris, fontSize: 11 } }],
        { x: x + 0.12, y: 4.62, w: cw - 0.24, h: 0.66, fontSize: 12, color: K.txt, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.06, fill: { color: K.azulClaro }, margin: 4 });
    }
    texto(s, [{ text: "Capacidad no es venta garantizada. ", options: { bold: true, color: K.rojo } },
      { text: "Con la demanda documentada de hoy (≈ 0), la utilización respaldada es 0 % en las cuatro escalas. Ninguna escala está elegida; también se pueden simular escalas intermedias.", options: { color: K.txt } }],
      { x: 0.6, y: 5.6, w: 12.13, h: 0.75, fontSize: 15, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.rojoClaro }, margin: 8 });
    texto(s, "Base de cálculo: 5 días de faena por semana (250 días/año), pollo de 2,9 kg vivo, demanda en día calendario y ave completa vendida (cota inferior). Con 6 días/semana el volumen anual sube ~20 %.",
      { x: 0.6, y: 6.45, w: 12.13, h: 0.45, fontSize: 11, color: K.gris });
    registrar(s, "Escalas", "2.500 / 5.000 / 10.000 / 20.000 aves/día: tamaños de referencia; capacidad ≠ venta garantizada.",
      "Se estudiaron cuatro tamaños de planta de referencia, medidos en aves faenadas por día: 2.500, 5.000, 10.000 y 20.000. " +
      "Para dar una idea: una planta de 10.000 aves por día faena unos 2,5 millones de pollos por año, necesita unos 52.800 pollitos por semana y unas 12.400 toneladas de alimento por año. " +
      "Estos números son estimaciones del modelo, no datos de campo. " +
      "El recuadro azul de cada columna dice cuánto habría que vender para llenar esa planta. Por ejemplo, 20.000 aves por día equivalen a unos 365 kilos por local y por día si todo fuera a los 90 supermercados, que es más de lo que el rango de la red parece absorber. " +
      "El mensaje de fondo: tener capacidad no significa vender. Con la demanda documentada de hoy, que es casi cero, ninguna escala está justificada. La escala se elige después de validar la demanda.");
  }

  // 9. Planta y proceso
  {
    const s = contenido("La planta por dentro: qué pasa con cada pollo", "El negocio");
    chipsArriba(s, ["ESTIMACIÓN", "PENDIENTE"]);
    const f1 = ["Recepción", "Colgado", "Aturdido", "Sangrado", "Escaldado", "Desplume"];
    const f2 = ["Eviscerado e inspección", "Enfriamiento", "Trozado", "Empaque", "Frío", "Despacho"];
    const bw = 1.85, gap = (12.13 - 6 * bw) / 5;
    texto(s, "ZONA SUCIA", { x: 0.6, y: 1.42, w: 4, h: 0.3, fontSize: 12, bold: true, color: K.pend, charSpacing: 2 });
    texto(s, "ZONA LIMPIA", { x: 1.75, y: 3.38, w: 4, h: 0.3, fontSize: 12, bold: true, color: K.evid, charSpacing: 2 });
    for (let i = 0; i < 6; i++) {
      const x = 0.6 + i * (bw + gap);
      for (const [fila, y, fondo, n0] of [[f1, 1.75, K.yemaClaro, 1], [f2, 3.7, K.claro, 7]]) {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: bw, h: 1.05, rectRadius: 0.08, fill: { color: fondo }, line: { color: fondo }, objectName: "etapa " + fila[i] });
        texto(s, String(n0 + i), { x: x + 0.15, y: y + 0.1, w: 0.5, h: 0.3, fontSize: 12, bold: true, color: K.gris });
        texto(s, fila[i], { x: x + 0.12, y: y + 0.38, w: bw - 0.24, h: 0.6, fontSize: 15, bold: true, color: K.osc, valign: "middle" });
        if (i < 5) flecha(s, x + bw + 0.03, y + 0.52, x + bw + gap - 0.03, y + 0.52, K.gris, 1.5);
      }
    }
    // transferencia sucia → limpia
    const xUlt = 0.6 + 5 * (bw + gap) + bw / 2, xPri = 0.6 + bw / 2;
    linea(s, xUlt, 2.8, xUlt, 3.2, K.gris, 1.5);
    linea(s, xPri, 3.2, xUlt, 3.2, K.gris, 1.5);
    flecha(s, xPri, 3.2, xPri, 3.68, K.gris, 1.5);
    texto(s, "transferencia de zona sucia a zona limpia", { x: 4.6, y: 3.25, w: 4.2, h: 0.3, fontSize: 11, italic: true, color: K.gris, align: "center" });
    const info = [
      ["FaLayerGroup", "32 etapas en el modelo", "Esta es la versión simple; el modelo incluye además garras, menudencias y carcasa."],
      ["FaCogs", "Capacidad del fabricante ≠ capacidad real", "Lo que una línea garantiza se sabe con una cotización y con visitas a plantas en operación."],
      ["FaClipboardCheck", "Inspección y bienestar animal", "Inspección veterinaria, zonificación higiénica y requisitos de SENASA en todo el recorrido."],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, t, d] = info[i];
      const x = 0.6 + i * 4.11;
      tarjeta(s, x, 5.1, 3.89, 1.7, K.blanco, true);
      await circuloIcono(s, ic, x + 0.2, 5.3, 0.6, K.osc, K.blanco);
      texto(s, t, { x: x + 0.95, y: 5.25, w: 2.8, h: 0.7, fontSize: 14, bold: true, color: K.osc, valign: "middle" });
      texto(s, d, { x: x + 0.2, y: 6.0, w: 3.5, h: 0.75, fontSize: 12, color: K.txt });
    }
    registrar(s, "Planta y proceso industrial", "Doce pasos simplificados de un proceso de 32 etapas; la capacidad real depende de cotizaciones y visitas.",
      "Esto es lo que pasa adentro de la planta, simplificado en doce pasos. Arriba, la zona sucia: el pollo llega vivo, se lo cuelga, se lo aturde para que no sufra, se lo desangra, se lo escalda con agua caliente y se le sacan las plumas. " +
      "Después pasa a la zona limpia, separada por higiene: se lo eviscera con inspección veterinaria, se lo enfría —que es un punto crítico de inocuidad—, se lo corta, se lo empaca, se guarda en frío y se despacha. " +
      "En el modelo completo son 32 etapas, más las salas de garras, menudencias y carcasa. " +
      "Algo importante: lo que dice un catálogo de fabricante no es la capacidad real de la planta. Eso se conoce con una cotización formal y visitando plantas en funcionamiento. Todavía no se pidieron cotizaciones ni se eligió proveedor.");
  }

  // 10. Productos y subproductos
  {
    const s = contenido("Qué sale de un pollo", "El negocio");
    chipsArriba(s, ["ESTIMACIÓN", "PENDIENTE"]);
    const partes = [
      ["Pechuga con hueso", 0.784], ["Pata-muslo", 0.631], ["Carcasa-esqueleto", 0.393], ["Alas", 0.208], ["Plumas", 0.151],
      ["Vísceras no comestibles", 0.130], ["Patas (garras)", 0.113], ["Menudencias", 0.110], ["Sangre", 0.099], ["Cuello", 0.075], ["Cabeza", 0.072],
    ].reverse();
    const fmt = (v) => v.toFixed(3).replace(".", ",");
    s.addChart(pres.charts.BAR, [{ name: "kg por ave", labels: partes.map(([n, v]) => n + "  " + fmt(v) + " kg"), values: partes.map(([, v]) => v) }], {
      x: 0.6, y: 1.45, w: 6.6, h: 5.05, barDir: "bar", chartColors: [K.osc], showLegend: false, showValue: false,
      showTitle: true, title: "kg por pollo de 2,9 kg vivo (corte en trozos)", titleFontSize: 14, titleColor: K.osc, titleFontFace: "+mn-lt",
      catAxisLabelFontSize: 12, catAxisLabelColor: K.txt, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true,
      valGridLine: { style: "none" }, catGridLine: { style: "none" }, barGapWidthPct: 45, catAxisLineShow: false,
    });
    texto(s, "Balance de masa del modelo con rendimientos de referencia; falta un ensayo en una planta argentina.", { x: 0.6, y: 6.55, w: 6.6, h: 0.35, fontSize: 11, color: K.gris });
    // rutas excluyentes
    texto(s, "Las rutas son alternativas: no se suman", { x: 7.6, y: 1.45, w: 5.13, h: 0.45, fontSize: 18, bold: true, color: K.osc });
    const rutas = [["A", "Entero", "Se vende el ave entera"], ["B", "Trozado", "Pechuga, pata-muslo, alas, carcasa"], ["C", "Deshuesado", "Suprema, muslo sin hueso, CMS"]];
    rutas.forEach(([l, t, d], i) => {
      const y = 2.0 + i * 0.95;
      tarjeta(s, 7.6, y, 4.4, 0.75, K.claro, false);
      texto(s, l, { x: 7.75, y: y + 0.12, w: 0.5, h: 0.5, fontSize: 18, bold: true, color: K.blanco, align: "center", valign: "middle", shape: pres.shapes.OVAL, fill: { color: K.osc } });
      texto(s, [{ text: t + "  ", options: { bold: true, color: K.osc } }, { text: d, options: { color: K.txt, fontSize: 12 } }], { x: 8.4, y: y + 0.05, w: 3.5, h: 0.65, fontSize: 15, valign: "middle" });
    });
    texto(s, [{ text: "La carcasa ", options: { bold: true } }, { text: "se vende, o va a CMS (pasta para elaborados), o a rendering: nunca dos a la vez." }],
      { x: 7.6, y: 4.95, w: 5.13, h: 0.75, fontSize: 14, color: K.txt, valign: "middle" });
    texto(s, [{ text: "Objetivo: ", options: { bold: true, color: K.osc } }, { text: "que cada parte vaya al mercado que mejor la paga (ingreso total por ave). Hoy no hay precios para calcularlo.", options: { color: K.txt } }],
      { x: 7.6, y: 5.8, w: 5.13, h: 1.0, fontSize: 14, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.yemaClaro }, margin: 8 });
    registrar(s, "Productos y subproductos", "Un pollo se divide en partes con mercados distintos; las rutas entero / trozado / deshuesado / CMS son excluyentes.",
      "De un pollo vivo de 2,9 kilos, según el modelo, salen unos 780 gramos de pechuga con hueso, unos 630 de pata-muslo, casi 400 de carcasa, unos 200 de alas, y después menudencias, patas, sangre, plumas, vísceras, cuello y cabeza. " +
      "Son estimaciones con rendimientos de referencia; falta medirlo en una planta argentina. " +
      "A la derecha, una aclaración importante: el mismo pollo no se puede vender de todas las formas a la vez. O se vende entero, o trozado, o deshuesado. Y la carcasa o se vende, o se convierte en carne mecánicamente separada, o va a rendering. " +
      "Por eso no se suman los kilos de rutas distintas. El objetivo del negocio es que cada parte vaya al mercado que más la paga: por ejemplo, garras para exportación, pechuga al supermercado. Para calcular eso hacen falta precios por producto y canal, que todavía no tenemos.");
  }

  // 11. Localización
  {
    const s = contenido("Dónde podría estar la planta", "El negocio");
    chipsArriba(s, ["PENDIENTE"]);
    const prov = [
      ["Buenos Aires", ["Periurbano AMBA", "Norte", "Oeste", "Interior"]],
      ["Entre Ríos", ["Sur", "Río Uruguay", "Centro"]],
      ["Santa Fe", ["Gran Rosario", "Centro"]],
      ["Córdoba", ["Sur", "Este"]],
      ["Chaco", ["Este", "Centro"]],
    ];
    texto(s, "5 provincias · 13 corredores estudiados (sin orden de preferencia)", { x: 0.6, y: 1.42, w: 6.4, h: 0.35, fontSize: 14, bold: true, color: K.gris });
    prov.forEach(([p, cs], i) => {
      const y = 1.9 + i * 0.95;
      tarjeta(s, 0.6, y, 6.4, 0.8, K.claro, false);
      texto(s, p, { x: 0.8, y, w: 1.7, h: 0.8, fontSize: 16, bold: true, color: K.osc, valign: "middle" });
      let x = 2.55;
      for (const c of cs) {
        const w = 0.3 + c.length * 0.085;
        texto(s, c, { x, y: y + 0.22, w, h: 0.36, fontSize: 12, color: K.osc, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, fill: { color: K.blanco }, line: { color: K.linea, width: 0.75 } });
        x += w + 0.1;
      }
    });
    tarjeta(s, 7.35, 1.45, 5.38, 1.4, K.rojoClaro, false);
    texto(s, "0 de 624", { x: 7.6, y: 1.5, w: 2.4, h: 0.85, fontSize: 36, bold: true, color: K.rojo, valign: "middle" });
    texto(s, "datos de la matriz de localización verificados: no hay ranking ganador", { x: 10.0, y: 1.55, w: 2.6, h: 1.2, fontSize: 13, color: K.txt, valign: "middle" });
    texto(s, "Condiciones que pueden descartar un terreno", { x: 7.35, y: 3.0, w: 5.38, h: 0.35, fontSize: 14, bold: true, color: K.osc });
    const duros = [["FaMap", "Uso de suelo"], ["FaWater", "Agua"], ["FaTint", "Efluentes"], ["FaPlug", "Energía"]];
    for (let i = 0; i < 4; i++) {
      const x = 7.35 + i * 1.36;
      await circuloIcono(s, duros[i][0], x + 0.3, 3.42, 0.62, K.osc, K.blanco);
      texto(s, duros[i][1], { x, y: 4.08, w: 1.22, h: 0.3, fontSize: 12, bold: true, color: K.txt, align: "center" });
    }
    texto(s, [{ text: "Condiciones a resolver ", options: { bold: true, color: K.osc, breakLine: true } },
      { text: "vecinos · acceso y logística · riesgo hídrico · gas · potencia eléctrica · quién recibe los subproductos", options: { color: K.txt } }],
      { x: 7.35, y: 4.55, w: 5.38, h: 1.05, fontSize: 13, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.yemaClaro }, margin: 8 });
    texto(s, "Las condiciones se verifican terreno por terreno, con el municipio. El contacto personal en Chaco es una ventaja cualitativa: no suma puntos en el análisis.",
      { x: 7.35, y: 5.75, w: 5.38, h: 0.95, fontSize: 12, italic: true, color: K.gris });
    registrar(s, "Localización", "13 corredores en 5 provincias; sin ranking ganador (0 de 624 datos verificados).",
      "¿Dónde iría la planta? Se estudiaron 13 corredores en cinco provincias: Buenos Aires, Entre Ríos, Santa Fe, Córdoba y Chaco. Están listados sin orden de preferencia. " +
      "Se armó una matriz para compararlos con decenas de criterios: distancia al mercado, granjas cercanas, granos, agua, energía, rutas, costo de la tierra, riesgo sanitario. " +
      "Pero de 624 casilleros de esa matriz, hoy hay cero verificados. Por eso el modelo no da un ganador, y lo dice explícitamente en lugar de inventar un orden. " +
      "Hay cuatro condiciones que pueden descartar un terreno concreto: que el uso de suelo no lo permita, que no haya agua, que no se puedan tratar los efluentes o que no llegue la energía. " +
      "Otras —vecinos, accesos, inundabilidad, gas, potencia, a quién se le venden los subproductos— no descartan, pero encarecen o condicionan. " +
      "Y un punto de método: tener un contacto en Chaco es una ventaja, pero no es un criterio para elegir.");
  }

  // 12. Layout e infraestructura
  {
    const s = contenido("Terreno e infraestructura: un orden de magnitud", "El negocio");
    chipsArriba(s, ["ESTIMACIÓN", "PENDIENTE"]);
    // diagrama conceptual
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.6, y: 1.5, w: 6.3, h: 5.2, rectRadius: 0.06, fill: { color: K.claro }, line: { color: K.osc, width: 1.25, dashType: "dash" }, objectName: "terreno" });
    texto(s, "Terreno (con retiros y circulación)", { x: 0.8, y: 1.58, w: 5, h: 0.35, fontSize: 13, bold: true, color: K.osc });
    const bloques = [
      [0.9, 2.05, 3.3, 2.3, K.osc, K.blanco, "Planta construida", "Faena, proceso, empaque y servicios"],
      [4.4, 2.05, 2.2, 1.1, K.esti, K.blanco, "Cámaras de frío", "Refrigerado y congelado"],
      [4.4, 3.25, 2.2, 1.1, "4F7F6A", K.blanco, "Efluentes", "Tratamiento del agua"],
      [0.9, 4.55, 5.7, 0.85, K.yemaClaro, K.osc, "Reserva de expansión", "Espacio para crecer"],
      [0.9, 5.55, 5.7, 0.9, K.blanco, K.osc, "Accesos, playa de camiones, estacionamiento", "Recepción de aves vivas y despacho"],
    ];
    for (const [x, y, w, h, f, c, t, d] of bloques) {
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.05, fill: { color: f }, line: { color: f === K.blanco ? K.linea : f }, objectName: t });
      texto(s, [{ text: t, options: { bold: true, breakLine: true } }, { text: d, options: { fontSize: 11 } }], { x: x + 0.15, y: y + 0.1, w: w - 0.3, h: h - 0.2, fontSize: 14, color: c, valign: "middle" });
    }
    // datos
    const datos = [
      ["≈ 2 a 4,4 ha", "terreno conceptual según la escala (19.868 a 43.660 m², de 2.500 a 20.000 aves/día)", K.esti],
      ["54 áreas · 9 zonas", "programa de la planta, con sus flujos higiénicos", K.esti],
      ["Sin planos", "no existe un layout constructivo ni anteproyecto", K.pend],
    ];
    datos.forEach(([v, d, c], i) => {
      const y = 1.5 + i * 1.18;
      tarjeta(s, 7.3, y, 5.43, 1.02, K.blanco, true);
      texto(s, v, { x: 7.5, y, w: 2.45, h: 1.02, fontSize: 20, bold: true, color: c, valign: "middle" });
      texto(s, d, { x: 9.95, y, w: 2.65, h: 1.02, fontSize: 12, color: K.txt, valign: "middle" });
    });
    texto(s, [{ text: "El terreno real depende de:", options: { bold: true, color: K.osc, breakLine: true } },
      { text: "lo que permita el municipio (zonificación, retiros) · la tecnología de efluentes · cuánto se decida reservar para crecer.", options: { color: K.txt } }],
      { x: 7.3, y: 5.12, w: 5.43, h: 1.55, fontSize: 14, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.yemaClaro }, margin: 10 });
    registrar(s, "Layout e infraestructura", "Terreno conceptual ≈ 2 a 4,4 ha según escala; el terreno real depende del municipio, los efluentes y la expansión.",
      "El dibujo de la izquierda no es un plano: es un esquema de qué ocupa lugar en el terreno. La planta construida, las cámaras de frío, la planta de tratamiento de efluentes, una reserva para crecer y los accesos para camiones. " +
      "El modelo estima un terreno conceptual de unas 2 hectáreas para la escala más chica y unas 4,4 para la más grande. Es un orden de magnitud. " +
      "La planta se organizó en 54 áreas y 9 zonas, respetando los flujos de higiene. Pero no hay planos ni anteproyecto. " +
      "¿Por qué el terreno real puede ser distinto? Porque depende de lo que permita el municipio, de qué tecnología se use para tratar los efluentes, y de cuánto se quiera reservar para crecer. Esa última es una decisión todavía abierta.");
  }

  // ---------------- SECCIÓN 3: economía ----------------
  pres.addSection({ title: "Economía" });

  // 13. CAPEX
  {
    const s = contenido("CAPEX: estructura lista, total no disponible", "Economía");
    chipsArriba(s, ["PENDIENTE"]);
    s.addChart(pres.charts.DOUGHNUT, [{ name: "Conceptos de inversión", labels: ["Sin precio", "Con referencia débil (sin verificar)"], values: [167, 8] }], {
      x: 0.6, y: 1.45, w: 5.0, h: 4.4, holeSize: 62, chartColors: ["C9D6CE", K.yema], showLegend: true, legendPos: "b", legendFontSize: 12, legendFontFace: "+mn-lt", legendColor: K.txt,
      showValue: true, showPercent: false, dataLabelColor: K.txt, dataLabelFontSize: 13, dataLabelFontFace: "+mn-lt", dataLabelPosition: "outEnd", showTitle: false,
    });
    texto(s, [{ text: "175", options: { fontSize: 34, bold: true, color: K.osc, breakLine: true } }, { text: "conceptos", options: { fontSize: 13, color: K.gris } }],
      { x: 2.1, y: 2.85, w: 2.0, h: 1.1, align: "center", valign: "middle" });
    texto(s, "CAPEX TOTAL: NO DISPONIBLE", { x: 6.0, y: 1.5, w: 6.73, h: 0.8, fontSize: 26, bold: true, color: K.rojo, valign: "middle",
      shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.rojoClaro }, margin: 12 });
    texto(s, bullets([
      "El motor ya sabe qué hay que comprar o construir en cada alternativa y en cada escala.",
      "Solo 8 de 175 conceptos tienen alguna referencia de precio, y todas son débiles: prensa o web, sin verificar.",
      "Cobertura de precios: 0 % a 2,3 % según la alternativa.",
      "Por eso no se compara contra USD 2 M: hoy no se puede saber si alcanza ni si no alcanza.",
    ]), { x: 6.0, y: 2.5, w: 6.73, h: 2.85, fontSize: 15 });
    texto(s, "Qué falta para tener un total", { x: 6.0, y: 5.4, w: 6.73, h: 0.35, fontSize: 14, bold: true, color: K.osc });
    const falta = ["Línea de faena", "Frío", "Efluentes", "Obra civil", "Terreno", "Galpones", "Importación e instalación"];
    let x = 6.0, y = 5.82;
    for (const f of falta) {
      const w = 0.3 + f.length * 0.09;
      if (x + w > 12.75) { x = 6.0; y += 0.45; }
      texto(s, f, { x, y, w, h: 0.36, fontSize: 12, color: K.blanco, bold: true, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, fill: { color: K.pend } });
      x += w + 0.1;
    }
    texto(s, "Ningún monto parcial se usa como total.", { x: 0.6, y: 6.1, w: 5.0, h: 0.6, fontSize: 13, italic: true, color: K.gris, align: "center" });
    registrar(s, "CAPEX", "El motor de inversión está estructurado, pero no hay CAPEX total: 167 de 175 conceptos sin precio.",
      "CAPEX es la inversión: lo que hay que comprar o construir antes de operar. El motor ya tiene la lista: 175 conceptos de inversión, según la alternativa y la escala. " +
      "Lo que no tiene son precios. 167 conceptos no tienen ningún precio, y los 8 que tienen alguna referencia son débiles: salieron de notas de prensa o páginas web, sin verificar. " +
      "Por eso el motor responde «no disponible» en lugar de dar un total engañoso. Y por eso tampoco comparamos con los 2 millones: con 1 o 2 % de los precios no se puede decir ni que alcanza ni que no alcanza. " +
      "Para tener un total hacen falta cotizaciones de la línea de faena, el frío, los efluentes, la obra civil, el terreno, los galpones si hubiera granjas propias, y la importación e instalación.");
  }

  // 14. OPEX y capital de trabajo
  {
    const s = contenido("Costos operativos y capital de trabajo", "Economía");
    chipsArriba(s, ["PENDIENTE"]);
    s.addChart(pres.charts.BAR, [
      { name: "Sabemos qué costos existen", labels: ["C0", "C1", "C2", "C3 / CF"], values: [1, 1, 1, 1] },
      { name: "Sabemos cuántas unidades se usan", labels: ["C0", "C1", "C2", "C3 / CF"], values: [0.57, 0.62, 0.56, 0.43] },
      { name: "Sabemos cuánto cuestan", labels: ["C0", "C1", "C2", "C3 / CF"], values: [0.095, 0.077, 0.049, 0] },
    ], {
      x: 0.6, y: 1.45, w: 7.0, h: 4.95, barDir: "col", barGrouping: "clustered", chartColors: [K.osc, K.esti, K.yema],
      showTitle: true, title: "Cobertura de los costos operativos por alternativa", titleFontSize: 14, titleColor: K.osc, titleFontFace: "+mn-lt",
      showValue: true, dataLabelFormatCode: "0%", dataLabelFontSize: 11, dataLabelColor: K.txt, dataLabelFontFace: "+mn-lt", dataLabelPosition: "outEnd",
      showLegend: true, legendPos: "b", legendFontSize: 12, legendColor: K.txt, legendFontFace: "+mn-lt",
      catAxisLabelFontSize: 13, catAxisLabelColor: K.txt, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valAxisMaxVal: 1.1, valAxisMinVal: 0,
      valGridLine: { style: "none" }, catGridLine: { style: "none" }, barGapWidthPct: 60,
    });
    texto(s, "Etiquetas redondeadas. «Cuánto cuestan» (costeo por bloques): C0 9,5 % · C1 7,7 % · C2 4,9 % · C3/CF 0 %.", { x: 0.6, y: 6.45, w: 7.0, h: 0.4, fontSize: 11, color: K.gris });
    texto(s, "Sabemos qué costos existen; casi no sabemos cuánto cuestan.", { x: 7.95, y: 1.5, w: 4.78, h: 1.0, fontSize: 19, bold: true, color: K.osc, valign: "middle" });
    texto(s, [{ text: "Hoy ninguna alternativa es costeable. ", options: { bold: true, color: K.rojo } }, { text: "Costo por ave, costo operativo total y capital de trabajo: PENDIENTES.", options: { color: K.txt } }],
      { x: 7.95, y: 2.6, w: 4.78, h: 1.0, fontSize: 14, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.rojoClaro }, margin: 8 });
    texto(s, "Faltan precios de", { x: 7.95, y: 3.8, w: 4.78, h: 0.35, fontSize: 14, bold: true, color: K.osc });
    texto(s, bullets(["Alimento y pollito", "Tarifa de faena a façon", "Salarios y cargas sociales", "Electricidad, gas y agua", "Fletes", "Plazos de cobro y de pago"]),
      { x: 7.95, y: 4.2, w: 4.78, h: 1.85, fontSize: 14, paraSpaceAfter: 2 });
    texto(s, "Capital de trabajo: la plata inmovilizada en stock y en lo que los clientes todavía no pagaron.", { x: 7.95, y: 6.15, w: 4.78, h: 0.65, fontSize: 12, italic: true, color: K.gris });
    registrar(s, "OPEX y capital de trabajo", "Estructura de costos completa; precios casi inexistentes; ninguna alternativa costeable.",
      "OPEX son los costos de operar: alimento, pollitos, sueldos, energía, fletes. El gráfico muestra tres niveles de conocimiento para cada alternativa. " +
      "La barra verde oscura dice que conocemos el 100 % de los costos que existen: sabemos qué hay que pagar. La azul dice que de entre el 43 y el 62 % sabemos cuántas unidades se usan. " +
      "Y la amarilla, casi invisible, dice cuánto sabemos de cuánto cuestan: menos del 10 %. " +
      "Con esto no se puede calcular el costo por pollo ni el capital de trabajo. Faltan, sobre todo, precios de alimento, pollito, tarifa de façon, sueldos, servicios, fletes y los plazos de pago. " +
      "El capital de trabajo es la plata que queda atada en mercadería y en lo que los clientes todavía no pagaron; en avicultura puede ser importante y por eso el modelo lo trata aparte.");
  }

  // 15. Modelo financiero
  {
    const s = contenido("Modelo financiero: calcula cuando haya datos", "Economía");
    chipsArriba(s, ["EVIDENCIA", "ESCENARIO"]);
    const met = [
      ["EBITDA", "Lo que deja la operación antes de intereses, impuestos y amortizaciones"],
      ["Flujo de caja (FCFF)", "La caja que genera el proyecto después de invertir"],
      ["VAN", "Cuánto valor crea por encima del rendimiento que se le exige"],
      ["TIR", "El rendimiento implícito del proyecto"],
      ["Payback", "Cuánto tarda en recuperar la plata invertida"],
      ["DSCR", "Si la caja alcanza para pagar la deuda, mes a mes"],
    ];
    texto(s, "Qué calcula", { x: 0.6, y: 1.45, w: 6, h: 0.4, fontSize: 16, bold: true, color: K.gris });
    met.forEach(([m, d], i) => {
      const y = 1.95 + i * 0.75;
      texto(s, m, { x: 0.6, y, w: 2.3, h: 0.62, fontSize: 15, bold: true, color: K.osc, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.claro }, margin: 8 });
      texto(s, d, { x: 3.05, y, w: 3.75, h: 0.62, fontSize: 13, color: K.txt, valign: "middle" });
    });
    tarjeta(s, 7.2, 1.45, 5.53, 2.35, K.blanco, true);
    chip(s, 7.45, 1.65, "EVIDENCIA");
    texto(s, "0 corridas publicables", { x: 7.45, y: 2.05, w: 5.1, h: 0.65, fontSize: 26, bold: true, color: K.rojo, valign: "middle" });
    texto(s, "Con datos reales: 0 de 42 corridas en modo evidencia y 0 de 54 alternativas del optimizador tienen resultados publicables.", { x: 7.45, y: 2.75, w: 5.1, h: 0.95, fontSize: 13, color: K.txt });
    tarjeta(s, 7.2, 4.0, 5.53, 2.0, K.blanco, true);
    chip(s, 7.45, 4.2, "ESCENARIO");
    texto(s, "Sí puede simular", { x: 7.45, y: 4.6, w: 5.1, h: 0.55, fontSize: 24, bold: true, color: K.esce, valign: "middle" });
    texto(s, "Con precios, costos y demanda hipotéticos, rotulado SIMULACIÓN. Nunca se mezcla con la evidencia.", { x: 7.45, y: 5.18, w: 5.1, h: 0.75, fontSize: 13, color: K.txt });
    texto(s, [{ text: "Hallazgo: ", options: { bold: true, color: K.osc } }, { text: "la plata necesaria no es solo la inversión. El pico de fondos suma el arranque y el capital de trabajo.", options: { color: K.txt } }],
      { x: 7.2, y: 6.15, w: 5.53, h: 0.7, fontSize: 13, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.yemaClaro }, margin: 8 });
    registrar(s, "Modelo financiero", "Calcula EBITDA, FCFF, VAN, TIR, payback y DSCR; hoy 0 corridas publicables con evidencia; en escenarios sí simula.",
      "El modelo financiero es el que junta todo y calcula los indicadores clásicos. A la izquierda, en castellano: EBITDA es lo que deja la operación; el flujo de caja es la plata que genera el proyecto después de invertir; " +
      "el VAN dice cuánto valor crea por encima de lo que se le exige; la TIR es la rentabilidad implícita; el payback es cuánto tarda en recuperar la inversión; y el DSCR mide si alcanza la caja para pagar la deuda. " +
      "El modelo funciona en dos modos. En modo evidencia, solo con datos reales, hoy no puede publicar ningún resultado: de las 61 corridas de referencia del modelo, 42 son en modo evidencia y ninguna es publicable (las otras 19 son plantillas de escenario sin datos cargados, tampoco publicables). Lo mismo con las 54 alternativas del optimizador. Eso es lo correcto, porque no hay precios. " +
      "En modo escenario, sí puede simular: si cargamos precios y costos hipotéticos, calcula todo, pero el resultado sale marcado como simulación y nunca se guarda como si fuera real. " +
      "Un hallazgo ya útil: la plata que hace falta no es solo la inversión en la planta. Hay que sumar las pérdidas del arranque y el capital de trabajo; por eso el modelo mide el pico de fondos.");
  }

  // 16. Riesgos y optimizador
  {
    const s = contenido("Riesgos y optimizador", "Economía");
    chipsArriba(s, ["ESCENARIO", "PENDIENTE"]);
    const her = [
      ["FaSlidersH", "Sensibilidad", "¿Qué pasa si sube el alimento o baja el precio?"],
      ["FaBolt", "Stress", "¿Y si varias cosas salen mal al mismo tiempo?"],
      ["FaExclamationTriangle", "Puntos de quiebre", "¿Hasta qué precio o costo aguanta el proyecto?"],
      ["FaChartBar", "Monte Carlo", "Preparado. Hoy no disponible: faltan distribuciones con respaldo."],
      ["FaBullseye", "Optimizador", "Busca la alternativa que mejor cumple el objetivo que se declare."],
    ];
    const cw = 2.3, gap = (12.13 - 5 * cw) / 4;
    for (let i = 0; i < her.length; i++) {
      const [ic, t, d] = her[i];
      const x = 0.6 + i * (cw + gap);
      tarjeta(s, x, 1.45, cw, 2.75, K.blanco, true, t);
      await circuloIcono(s, fa[ic] ? ic : "FaChartLine", x + 0.2, 1.65, 0.7, i === 4 ? K.yema : K.osc, K.blanco);
      texto(s, t, { x: x + 0.2, y: 2.45, w: cw - 0.4, h: 0.45, fontSize: 16, bold: true, color: K.osc });
      texto(s, d, { x: x + 0.2, y: 2.9, w: cw - 0.4, h: 1.2, fontSize: 12.5, color: K.txt });
    }
    tarjeta(s, 0.6, 4.5, 8.0, 2.3, K.osc, true);
    await circuloIcono(s, "FaPauseCircle", 0.9, 4.8, 0.85, K.yema, K.osc);
    texto(s, "Una respuesta válida del optimizador: NO INVERTIR AÚN", { x: 1.95, y: 4.72, w: 6.4, h: 0.95, fontSize: 21, bold: true, color: K.blanco, valign: "middle" });
    texto(s, "No es un fracaso. Aparece por reglas explícitas: ninguna alternativa cumple las condiciones, el capital no alcanza, el VAN es negativo o el riesgo es demasiado alto.",
      { x: 0.9, y: 5.75, w: 7.5, h: 0.95, fontSize: 14, color: "D7E4DB" });
    tarjeta(s, 8.9, 4.5, 3.83, 2.3, K.claro, false);
    texto(s, "34", { x: 9.15, y: 4.6, w: 3.4, h: 0.9, fontSize: 44, bold: true, color: K.osc, valign: "middle" });
    texto(s, "riesgos registrados (sanitarios, granos, tipo de cambio, energía, competencia…). Probabilidad propia del proyecto: PENDIENTE.", { x: 9.15, y: 5.5, w: 3.4, h: 1.2, fontSize: 12.5, color: K.txt });
    registrar(s, "Riesgos y optimizador", "Sensibilidad, stress, quiebres, Monte Carlo preparado y optimizador; NO_INVERTIR_AUN es una respuesta posible.",
      "Esta capa sirve para preguntar «¿y si…?». La sensibilidad mueve una variable por vez: ¿qué pasa si el alimento sube un 20 %? El stress mueve varias juntas, como en una crisis. " +
      "Los puntos de quiebre buscan el límite: ¿hasta qué precio de venta el proyecto sigue en pie? El Monte Carlo está preparado, pero no lo usamos porque inventar probabilidades sería engañoso. " +
      "Y el optimizador compara alternativas según el objetivo que elija el inversor: ganar más, invertir menos, recuperar rápido o arriesgar menos. " +
      "Algo muy importante: el optimizador puede responder «no invertir aún». No es un error ni un fracaso; es una respuesta válida cuando los datos dicen que ninguna opción cumple las condiciones. " +
      "Además hay 34 riesgos identificados —gripe aviar, precio de granos, tipo de cambio, energía— cuya probabilidad específica para este proyecto todavía no se puede estimar. " +
      "Todo esto hoy funciona solo con escenarios hipotéticos, porque con datos reales no hay todavía resultados que estresar.");
  }

  // ---------------- SECCIÓN 4: App ----------------
  pres.addSection({ title: "App V1" });

  // 17. App: entender
  {
    const s = contenido("App V1: el estudio en lenguaje simple", "App V1");
    const iw = 7.35, ih = iw * 1290 / 1815;
    s.addImage({ path: CAP("app_inicio.png"), x: 0.6, y: 1.45, w: iw, h: ih, altText: "Pantalla de inicio de la App V1",
      shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 90, opacity: 0.18 } });
    texto(s, "Captura real de la App V1: pantalla de inicio (2026-10-05)", { x: 0.6, y: 1.5 + ih, w: iw, h: 0.3, fontSize: 10.5, italic: true, color: K.gris });
    const items = [
      ["FaBook", "Entender el proyecto", "26 temas, cada uno en 5 preguntas: qué es, por qué importa, qué se modeló, qué se sabe y qué falta."],
      ["FaSearch", "Ver dónde estamos parados", "Qué está terminado, qué está pendiente, qué se puede simular y qué no se puede decidir todavía."],
      ["FaGraduationCap", "Sin saber de finanzas", "Cada término técnico tiene su «?» y hay un diccionario y un buscador."],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, t, d] = items[i];
      const y = 1.45 + i * 1.75;
      await circuloIcono(s, ic, 8.3, y + 0.05, 0.7, K.osc, K.blanco);
      texto(s, t, { x: 9.15, y, w: 3.58, h: 0.5, fontSize: 16, bold: true, color: K.osc, valign: "middle" });
      texto(s, d, { x: 9.15, y: y + 0.5, w: 3.58, h: 1.1, fontSize: 13, color: K.txt });
    }
    registrar(s, "App V1 (1): entender", "La app explica el proyecto en lenguaje simple y muestra el estado real del estudio.",
      "Esta es la pantalla de inicio real de la app. Tiene cuatro botones grandes: entender el proyecto, simular un escenario, comparar u optimizar, y ver qué falta validar. " +
      "Debajo está el resumen de dónde estamos parados: motor completo, datos físicos parciales, datos económicos muy incompletos, evidencia cero por ciento y decisión real no disponible. " +
      "Es la misma conclusión de esta presentación, y la app la muestra siempre. " +
      "Está pensada para alguien que no es ingeniero ni financista: cada tema se explica con cinco preguntas simples, y cada palabra técnica tiene un signo de pregunta con una explicación corta. " +
      "Se usa en una computadora, sin internet, ejecutando un solo comando.");
  }

  // 18. App: simular
  {
    const s = contenido("App V1: modo simple y modo experto", "App V1");
    chipsArriba(s, ["ESCENARIO"]);
    const iw = 5.6, ih = iw * 1290 / 1815;
    const caps = [["app_simular.png", "Modo simple: simular en 5 preguntas"], ["app_estado.png", "¿Dónde estamos parados? Qué se puede simular y qué no se puede decidir"]];
    caps.forEach(([f, c], i) => {
      const x = 0.6 + i * (12.13 - iw);
      s.addImage({ path: CAP(f), x, y: 1.45, w: iw, h: ih, altText: c, shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 90, opacity: 0.18 } });
      texto(s, "Captura real · " + c, { x, y: 1.5 + ih, w: iw, h: 0.3, fontSize: 10.5, italic: true, color: K.gris });
    });
    const cols = [
      ["Modo simple", "Objetivo, capital, demanda, alternativa y precios. «No sé» es una respuesta válida: nunca se completa con ceros."],
      ["Modo experto", "Todos los datos del motor, para análisis: costos por módulo, impuestos, tasa, deuda y stress."],
      ["Qué responde", "¿Qué pasa si…? ¿Qué alternativa cumple mi objetivo? ¿Cuánto capital de trabajo? ¿Qué falta validar?"],
    ];
    cols.forEach(([t, d], i) => {
      const x = 0.6 + i * 4.11;
      texto(s, [{ text: t, options: { bold: true, color: K.osc, fontSize: 15, breakLine: true } }, { text: d, options: { color: K.txt } }],
        { x, y: 5.85, w: 3.89, h: 1.05, fontSize: 12, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.claro }, margin: 8 });
    });
    registrar(s, "App V1 (2): simular", "Modo simple de 5 preguntas para la familia; modo experto para análisis; todo resultado es SIMULACIÓN.",
      "A la izquierda, el modo simple: cinco preguntas, una por pantalla. Qué querés lograr, cuánto capital querés simular, cuánta demanda, qué alternativa y si tenés precios. " +
      "Si no se sabe algo, se responde «no sé» y la app lo deja como pendiente; nunca lo rellena con un cero, porque eso daría resultados falsos. " +
      "Por ejemplo, si no se carga demanda, no hay ventas y la app no calcula rentabilidad. Y los 2 millones no se usan por defecto. " +
      "A la derecha, la pantalla que explica qué se puede simular hoy y qué no se puede decidir. " +
      "El modo experto permite tocar todos los datos del motor, para quien quiera analizar en detalle. " +
      "Todo lo que calcula la app con datos inventados por el usuario sale con la etiqueta simulación, en violeta, arriba de la pantalla.");
  }

  // ---------------- SECCIÓN 5: cómo seguir ----------------
  pres.addSection({ title: "Cómo seguir" });

  // 19. Qué falta validar
  {
    const s = contenido("Qué falta validar: 12 paquetes de trabajo de campo", "Cómo seguir");
    chipsArriba(s, ["PENDIENTE"]);
    const paq = [
      ["FaHandshake", "Clientes", "P1"], ["GiFactory", "Planta y maquinaria", "P1"], ["GiCorn", "Alimento", "P1"],
      ["FaEgg", "Pollitos", "P1"], ["GiBarn", "Granjas", "P1"], ["FaPlug", "Agua, energía y gas", "P2"],
      ["FaMap", "Terreno", "P2"], ["FaTruck", "Logística", "P2"], ["FaUsers", "Recursos humanos", "P2"],
      ["FaUniversity", "Impuestos", "P2"], ["FaMoneyBillWave", "Financiamiento", "P2"], ["FaShip", "Exportación", "P4"],
    ];
    const tw = 2.35, th = 1.08, gx = 0.17, gy = 0.15;
    for (let i = 0; i < paq.length; i++) {
      const [ic, t, p] = paq[i];
      const x = 0.6 + (i % 3) * (tw + gx), y = 1.45 + Math.floor(i / 3) * (th + gy);
      const col = p === "P1" ? K.rojo : p === "P2" ? K.pend : K.gris;
      tarjeta(s, x, y, tw, th, p === "P1" ? K.rojoClaro : K.claro, false);
      await circuloIcono(s, ic, x + 0.15, y + 0.2, 0.62, K.blanco, K.osc);
      texto(s, t, { x: x + 0.88, y: y + 0.1, w: tw - 0.98, h: 0.55, fontSize: 13, bold: true, color: K.osc, valign: "middle" });
      texto(s, p, { x: x + 0.88, y: y + 0.66, w: 0.5, h: 0.28, fontSize: 11, bold: true, color: K.blanco, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.12, fill: { color: col } });
    }
    texto(s, [{ text: "P1 ", options: { bold: true, color: K.rojo } }, { text: "sin esto, ningún resultado económico se puede publicar  ·  ", options: { color: K.gris } },
      { text: "P2 ", options: { bold: true, color: K.pend } }, { text: "para flujo, VAN y costos completos  ·  ", options: { color: K.gris } },
      { text: "P4 ", options: { bold: true, color: K.gris } }, { text: "etapa futura", options: { color: K.gris } }],
      { x: 0.6, y: 6.4, w: 7.4, h: 0.45, fontSize: 11 });
    const iw = 4.5, ih = iw * 1290 / 1815;
    s.addImage({ path: CAP("app_validacion.png"), x: 8.23, y: 1.45, w: iw, h: ih, altText: "Checklist de validación en la App V1", shadow: { type: "outer", color: "000000", blur: 8, offset: 2, angle: 90, opacity: 0.18 } });
    texto(s, "Captura real · checklist de la app: qué pedir, a quién y en qué unidad", { x: 8.23, y: 1.5 + ih, w: iw, h: 0.45, fontSize: 10.5, italic: true, color: K.gris });
    texto(s, [{ text: "0 de 180", options: { fontSize: 30, bold: true, color: K.rojo, breakLine: true } }, { text: "datos por validar están validados hoy", options: { fontSize: 13, color: K.txt } }],
      { x: 8.23, y: 5.15, w: iw, h: 1.15, valign: "middle" });
    registrar(s, "Qué falta validar", "12 paquetes de campo; los 5 de prioridad 1 (clientes, planta, alimento, pollitos, granjas) bloquean todo resultado económico.",
      "Este es el trabajo que sigue. Todo lo que falta se agrupó en 12 paquetes, cada uno con a quién hay que pedirle, qué pedir y en qué unidad. " +
      "Los cinco en rojo son prioridad uno: clientes, planta y maquinaria, alimento, pollitos y granjas. Sin ellos, ningún resultado económico se puede publicar, en ninguna alternativa. " +
      "Los naranjas son prioridad dos: agua y energía, terreno, logística, personal, impuestos y financiamiento; completan los costos y el flujo de fondos. Exportación queda para una etapa futura. " +
      "Dentro de cada prioridad están empatados: el modelo no inventa un orden que los datos no dan. " +
      "A la derecha se ve cómo la app muestra esta lista, con casilleros que solo se marcan cuando hay evidencia. Hoy, de 180 datos, cero validados.");
  }

  // 20. Roadmap
  {
    const s = contenido("Roadmap recomendado del estudio", "Cómo seguir");
    const fases = [
      ["FASE 1", "Validar demanda y clientes", ["Volumen por producto y local", "Precios y condiciones de pago", "Cartas de intención"]],
      ["FASE 2", "Cotizar", ["Faena a façon", "Línea de faena", "Alimento y pollito", "Granjas integrables"]],
      ["FASE 3", "Terreno y servicios", ["Municipio y zonificación", "Agua, energía y gas", "Efluentes y logística"]],
      ["FASE 4", "Escenario financiero real", ["Cargar los datos en el motor", "Sensibilidades y stress", "Comparar alternativas"]],
      ["FASE 5", "Decisión", ["Invertir, empezar liviano, esperar o no invertir", "Con evidencia, no con supuestos"]],
    ];
    const cw = 2.45, step = (12.13 - cw) / 4;
    for (let i = 0; i < fases.length; i++) {
      const [f, t, its] = fases[i];
      const x = 0.6 + i * step;
      const col = i < 2 ? K.osc : i < 4 ? "3F7A60" : K.yema;
      s.addShape(i === 0 ? pres.shapes.PENTAGON : pres.shapes.CHEVRON, { x, y: 1.55, w: cw, h: 0.95, fill: { color: col }, line: { color: col }, objectName: f });
      texto(s, f, { x: x + (i === 0 ? 0.2 : 0.45), y: 1.55, w: cw - 0.8, h: 0.95, fontSize: 18, bold: true, color: i === 4 ? K.osc : K.blanco, valign: "middle" });
      tarjeta(s, x + 0.05, 2.8, cw - 0.2, 3.3, K.blanco, true, "fase " + (i + 1));
      texto(s, t, { x: x + 0.22, y: 2.92, w: cw - 0.54, h: 0.8, fontSize: 15, bold: true, color: K.osc, valign: "middle" });
      texto(s, bullets(its), { x: x + 0.22, y: 3.8, w: cw - 0.54, h: 2.2, fontSize: 13, paraSpaceAfter: 4 });
    }
    texto(s, "Las fases 1 y 2 son las más urgentes (prioridad 1) y pueden avanzar en paralelo. Sin fechas: los plazos dependen de cuándo respondan clientes y proveedores.",
      { x: 0.6, y: 6.3, w: 12.13, h: 0.55, fontSize: 13, italic: true, color: K.gris, align: "center", valign: "middle" });
    registrar(s, "Roadmap recomendado", "Validar demanda → cotizar → terreno y servicios → escenario financiero real → decisión.",
      "Este es el camino que recomendamos para el estudio; no es un plan de inversión. " +
      "Fase uno: validar la demanda. Hablar con compras de la red de supermercados y con otros canales para conseguir volúmenes por producto, precios, plazos de pago y, si se puede, cartas de intención. " +
      "Fase dos: cotizar. Tarifa de faena a façon, una línea de faena, alimento, pollitos y productores que puedan integrarse. Estas dos fases son las más urgentes y pueden ir en paralelo. " +
      "Fase tres: terreno y servicios, con municipios, distribuidoras de energía y de agua. " +
      "Fase cuatro: cargar todo en el motor y correr escenarios con datos reales, sensibilidades y stress. " +
      "Fase cinco: recién ahí, decidir. Y la decisión puede ser invertir, empezar liviano, esperar o no invertir. No ponemos fechas porque dependen de cuándo respondan los terceros.");
  }

  // 21. Decisiones abiertas
  {
    const s = contenido("Decisiones abiertas", "Cómo seguir");
    chipsArriba(s, ["PENDIENTE"]);
    const dec = [
      ["FaLayerGroup", "Escala", "2.500 a 20.000 aves/día, o una intermedia"],
      ["FaSitemap", "Arquitectura", "C0, C1, C2, C3 o CF"],
      ["FaMapMarkedAlt", "Terreno y ubicación", "Región, municipio y superficie"],
      ["GiFactory", "Faena", "Planta propia o a façon"],
      ["GiCorn", "Alimento", "Comprado, a façon o planta propia"],
      ["FaEgg", "Pollito", "Comprado o incubadora propia"],
      ["FaTruck", "Flota", "Propia, tercerizada o mixta"],
      ["FaMoneyBillWave", "Financiamiento", "Aportes, deuda y etapas"],
    ];
    const tw = 2.9, th = 2.05, gx = (12.13 - 4 * tw) / 3, gy = 0.22;
    for (let i = 0; i < dec.length; i++) {
      const [ic, t, d] = dec[i];
      const x = 0.6 + (i % 4) * (tw + gx), y = 1.45 + Math.floor(i / 4) * (th + gy);
      tarjeta(s, x, y, tw, th, K.blanco, true, "decisión " + t);
      await circuloIcono(s, ic, x + 0.22, y + 0.22, 0.7, K.claro, K.osc);
      texto(s, t, { x: x + 1.05, y: y + 0.22, w: tw - 1.15, h: 0.7, fontSize: 17, bold: true, color: K.osc, valign: "middle" });
      texto(s, d, { x: x + 0.22, y: y + 1.1, w: tw - 0.44, h: 0.8, fontSize: 14, color: K.txt });
    }
    texto(s, "104 decisiones abiertas en el registro del proyecto; ninguna cerrada. Varias son del inversor: objetivo, capital real y condiciones.",
      { x: 0.6, y: 6.15, w: 12.13, h: 0.65, fontSize: 15, bold: true, color: K.osc, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.yemaClaro } });
    registrar(s, "Decisiones abiertas", "Escala, arquitectura, terreno, faena, alimento, pollito, flota y financiamiento siguen abiertas (104 en el registro).",
      "Estas son las grandes decisiones que siguen abiertas. El tamaño de la planta. La arquitectura, de C0 a CF. Dónde y qué terreno. Si la faena es propia o a façon. " +
      "Si el alimento se compra, se encarga a façon o se fabrica. Si el pollito se compra o se incuba. Si los camiones son propios o tercerizados. Y cómo se financia. " +
      "En total hay 104 decisiones registradas en el proyecto y ninguna está cerrada. " +
      "Algunas no son técnicas sino del inversor: qué objetivo prioriza, cuánto capital está realmente dispuesto a poner y bajo qué condiciones. Esas respuestas son también datos que el motor necesita.");
  }

  // 22. Qué puede decidirse hoy
  {
    const s = contenido("Qué se puede decidir hoy", "Cómo seguir");
    tarjeta(s, 0.6, 1.45, 5.9, 5.35, K.rojoClaro, false);
    await circuloIcono(s, "FaTimesCircle", 0.85, 1.65, 0.7, K.rojo, K.blanco);
    texto(s, "Todavía NO", { x: 1.75, y: 1.65, w: 4.5, h: 0.7, fontSize: 24, bold: true, color: K.rojo, valign: "middle" });
    texto(s, bullets(["Si conviene invertir", "Cuánto invertir", "Qué escala ni qué alternativa", "Dónde ubicar la planta", "Qué maquinaria o qué proveedor"]),
      { x: 0.85, y: 2.65, w: 5.4, h: 3.9, fontSize: 17, paraSpaceAfter: 10 });
    tarjeta(s, 6.83, 1.45, 5.9, 5.35, K.claro, false);
    await circuloIcono(s, "FaCheckCircle", 7.08, 1.65, 0.7, K.evid, K.blanco);
    texto(s, "SÍ, desde hoy", { x: 7.98, y: 1.65, w: 4.5, h: 0.7, fontSize: 24, bold: true, color: K.evid, valign: "middle" });
    texto(s, bullets([
      "Qué datos buscar primero: clientes y cotizaciones de prioridad 1",
      "A quién pedirlos y en qué unidad (checklist de la app)",
      "Qué escenarios simular para ver qué variables pesan más",
      "Mantener las 5 alternativas en estudio, sin descartar ninguna sin datos",
      "Que el inversor defina su objetivo, su capital real y sus condiciones",
    ]), { x: 7.08, y: 2.65, w: 5.4, h: 3.9, fontSize: 17, paraSpaceAfter: 10 });
    registrar(s, "Qué puede decidirse hoy", "Hoy no se decide la inversión; sí qué datos buscar, qué simular y qué alternativas mantener en estudio.",
      "Para ser claros sobre qué se puede hacer con esto hoy. No se puede decidir si conviene invertir, ni cuánto, ni qué tamaño, ni qué alternativa, ni dónde, ni con qué proveedor. " +
      "Cualquier respuesta a eso hoy sería una opinión, no un resultado del estudio. " +
      "Lo que sí se puede decidir desde hoy: qué datos salir a buscar primero, a quién pedírselos y en qué formato; qué escenarios simular en la app para entender qué variables pesan más; " +
      "mantener las cinco alternativas abiertas, sin descartar ninguna sin datos; y, del lado del inversor, definir su objetivo, cuánto capital pondría de verdad y con qué condiciones.");
  }

  // 23. Conclusión
  {
    const s = pres.addSlide({ masterName: "CIERRE", sectionTitle: "Cómo seguir" });
    s.addText("Conclusión", { placeholder: "title" });
    const filas = [
      ["FaCheckCircle", "MOTOR V1", "COMPLETO ESTRUCTURALMENTE", K.evid],
      ["FaCheckCircle", "APP V1", "LISTA", K.evid],
      ["FaPauseCircle", "LISTO PARA DECISIÓN REAL", "NO: faltan datos reales", K.rojo],
    ];
    for (let i = 0; i < 3; i++) {
      const [ic, a, b, c] = filas[i];
      const y = 2.2 + i * 0.9;
      await circuloIcono(s, ic, 0.7, y, 0.62, c, K.blanco);
      texto(s, [{ text: a + " = ", options: { color: "D7E4DB" } }, { text: b, options: { bold: true, color: K.blanco } }], { x: 1.55, y, w: 7.6, h: 0.62, fontSize: 22, valign: "middle" });
    }
    texto(s, "Próximo paso: trabajo de campo y cotizaciones", { x: 0.7, y: 5.1, w: 8.6, h: 0.7, fontSize: 28, bold: true, color: K.yema, valign: "middle" });
    texto(s, "El estudio todavía no dice si el proyecto conviene. Dice qué datos hacen falta para saberlo.", { x: 0.7, y: 5.85, w: 8.6, h: 0.7, fontSize: 16, color: "D7E4DB" });
    s.addShape(pres.shapes.OVAL, { x: 9.75, y: 2.0, w: 2.9, h: 2.9, fill: { color: "2C6650" }, line: { color: "2C6650" }, objectName: "círculo cierre" });
    s.addImage({ data: await icono("FaClipboardList", K.yema), x: 10.5, y: 2.75, w: 1.4, h: 1.4, altText: "lista de trabajo de campo" });
    registrar(s, "Conclusión", "Motor V1 completo, App V1 lista, decisión real pendiente; próximo paso: trabajo de campo y cotizaciones.",
      "Para cerrar, las mismas tres frases del principio. El motor está completo estructuralmente. La app está lista. Y el proyecto no está listo para una decisión real, porque faltan los datos. " +
      "El próximo paso no es más modelado: es salir a la cancha. Hablar con clientes, pedir cotizaciones, conocer terrenos y proveedores. " +
      "Con esos datos, el motor va a poder decir si el proyecto conviene, en qué forma y con cuánto capital. Hoy el estudio no dice si conviene; dice qué hay que conseguir para saberlo. Gracias.");
  }

  // ---------------- ANEXO ----------------
  pres.addSection({ title: "Anexo técnico" });
  {
    const s = pres.addSlide({ masterName: "SECCION", sectionTitle: "Anexo técnico" });
    s.addText("Anexo técnico", { placeholder: "title" });
    texto(s, "Para profesores y análisis detallado: arquitectura de motores, evidencia, pruebas, tensiones abiertas y glosario.", { x: 0.7, y: 3.85, w: 11.9, h: 0.6, fontSize: 18, color: "D7E4DB" });
    registrar(s, "Anexo técnico (portada)", "Material de respaldo para una audiencia técnica.",
      "Las láminas que siguen son de respaldo. No hace falta presentarlas a la familia ni a los socios; sirven para profesores o para quien quiera ver cómo está construido el motor y cómo se controló.");
  }

  // A1 arquitectura de motores
  {
    const s = contenido("A1 · Arquitectura de los motores", "Anexo técnico");
    const cajas = [
      [0.6, 1.6, 2.7, 3.9, K.claro, K.osc, "Datos físicos", "Producción · balance de masa · escala · proceso · agua, energía y frío · layout · logística · localización · RR. HH. · alimento e incubación"],
      [3.75, 1.6, 2.3, 1.75, K.blanco, K.osc, "CAPEX", "Lista de activos por alternativa y escala"],
      [3.75, 3.75, 2.3, 1.75, K.blanco, K.osc, "OPEX + capital de trabajo", "Registro de costos por concepto"],
      [6.5, 1.6, 2.6, 3.9, K.osc, K.blanco, "Modelo financiero", "Mes a mes: demanda → ventas → EBITDA → flujo → VAN / TIR / payback / DSCR"],
      [9.55, 1.6, 3.18, 1.75, K.yemaClaro, K.osc, "Riesgo + optimizador", "Usa el modelo financiero como función de evaluación"],
      [9.55, 3.75, 3.18, 1.75, K.blanco, K.osc, "App V1", "No calcula: llama al motor y muestra sus etiquetas"],
    ];
    for (const [x, y, w, h, f, c, t, d] of cajas) {
      tarjeta(s, x, y, w, h, f, f === K.blanco, t);
      texto(s, [{ text: t, options: { bold: true, fontSize: 16, breakLine: true } }, { text: d, options: { fontSize: 12 } }], { x: x + 0.18, y: y + 0.15, w: w - 0.36, h: h - 0.3, color: c, paraSpaceAfter: 4 });
    }
    flecha(s, 3.32, 2.47, 3.73, 2.47); flecha(s, 3.32, 4.62, 3.73, 4.62);
    flecha(s, 6.07, 2.47, 6.48, 2.9); flecha(s, 6.07, 4.62, 6.48, 4.2);
    flecha(s, 9.12, 2.9, 9.53, 2.47); flecha(s, 9.12, 4.2, 9.53, 4.62);
    texto(s, [{ text: "Dos universos que nunca se mezclan: ", options: { bold: true, color: K.osc } },
      { text: "EVIDENCIA (solo datos verificados) y ESCENARIO (hipótesis del usuario, rotuladas SIMULACIÓN). Una sola definición de C0–CF compartida por CAPEX, OPEX, finanzas, riesgo, optimizador y app.", options: { color: K.txt } }],
      { x: 0.6, y: 5.8, w: 12.13, h: 0.95, fontSize: 14, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.claro }, margin: 10 });
    registrar(s, "A1 · Arquitectura de motores", "Datos físicos → CAPEX y OPEX → financiero → riesgo/optimizador → app; evidencia y escenario separados.",
      "Así está armado el sistema. A la izquierda, todos los modelos físicos, que calculan cantidades: aves, kilos, metros cuadrados, kilovatios, personas. " +
      "Esas cantidades alimentan dos motores económicos: el de inversión, que arma la lista de activos, y el de costos operativos y capital de trabajo. " +
      "Los dos alimentan al modelo financiero mensual. Encima, la capa de riesgo y el optimizador usan el modelo financiero como función de evaluación, sin copiar fórmulas. " +
      "La app no calcula nada propio: llama al motor y muestra sus resultados con sus etiquetas. " +
      "Hay dos universos que no se mezclan: evidencia, con datos verificados, y escenario, con hipótesis. Y las cinco arquitecturas se definen en un solo lugar.");
  }

  // A2 evidencia
  {
    const s = contenido("A2 · Evidencia: qué cuenta como dato real", "Anexo técnico");
    chipsArriba(s, ["EVIDENCIA", "PENDIENTE"]);
    const niv = [
      ["E1", "Cotización formal para este proyecto", K.evid, true],
      ["E2", "Precio directo de fabricante o proveedor", K.evid, true],
      ["E3", "Referencia documentada leída en original", K.evid, true],
      ["E4", "Prensa, web o extracto sin verificar (PVDP)", K.pend, false],
      ["E5", "Supuesto de ingeniería sin precio observado", K.pend, false],
      ["—", "Sin dato: PENDIENTE, nunca cero", K.gris, false],
    ];
    niv.forEach(([c, d, col, ok], i) => {
      const y = 1.5 + i * 0.82;
      texto(s, c, { x: 0.6, y, w: 0.9, h: 0.65, fontSize: 18, bold: true, color: K.blanco, align: "center", valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: col } });
      texto(s, d, { x: 1.65, y, w: 4.6, h: 0.65, fontSize: 14, color: K.txt, valign: "middle" });
    });
    s.addShape(pres.shapes.RIGHT_BRACE, { x: 6.3, y: 1.5, w: 0.3, h: 2.29, line: { color: K.evid, width: 1.5 }, objectName: "llave umbral" });
    texto(s, "Cuenta como evidencia (umbral por defecto, configurable)", { x: 6.7, y: 2.2, w: 2.3, h: 0.9, fontSize: 12, bold: true, color: K.evid, valign: "middle" });
    s.addShape(pres.shapes.RIGHT_BRACE, { x: 6.3, y: 3.96, w: 0.3, h: 2.29, line: { color: K.pend, width: 1.5 }, objectName: "llave no usable" });
    texto(s, "No se usa para publicar resultados", { x: 6.7, y: 4.65, w: 2.3, h: 0.9, fontSize: 12, bold: true, color: K.pend, valign: "middle" });
    const reglas = [
      "Un faltante nunca se convierte en 0",
      "Una simulación nunca pasa a la base de evidencia",
      "Los ~90 supermercados no son demanda",
      "USD 2 M no es un valor por defecto",
      "Una cifra vista solo en prensa no es VERIFICADO",
    ];
    tarjeta(s, 9.25, 1.5, 3.48, 4.75, K.claro, false);
    texto(s, "Reglas del motor", { x: 9.45, y: 1.6, w: 3.1, h: 0.45, fontSize: 16, bold: true, color: K.osc });
    texto(s, bullets(reglas), { x: 9.45, y: 2.1, w: 3.1, h: 4.05, fontSize: 13, paraSpaceAfter: 8 });
    texto(s, "Hoy: 0 conceptos de CAPEX y OPEX en E1–E3 · 0 precios de venta · cobertura de evidencia del motor: 0 %", { x: 0.6, y: 6.45, w: 12.13, h: 0.4, fontSize: 13, bold: true, color: K.rojo, align: "center" });
    registrar(s, "A2 · Evidencia", "Solo E1–E3 cuentan como evidencia; hoy hay 0 % de cobertura de evidencia.",
      "El motor clasifica cada precio o dato por nivel de evidencia. E1 es una cotización formal para este proyecto; E2, un precio directo de proveedor; E3, una referencia documentada que se leyó en el original. " +
      "Solo esos tres cuentan para publicar resultados, y ese umbral es configurable. E4 es lo visto en prensa o en un buscador sin leer el original; E5, un supuesto de ingeniería. Esos no se usan. " +
      "Y si no hay dato, queda pendiente: nunca se reemplaza por cero. A la derecha, las reglas que el motor hace cumplir. Hoy la cobertura de evidencia es cero.");
  }

  // A3 tests
  {
    const s = contenido("A3 · Pruebas y controles", "Anexo técnico");
    const st = [
      ["70 / 70", "pruebas de integración entre módulos"],
      ["15 / 15", "errores introducidos a propósito que las pruebas detectaron (mutaciones)"],
      ["52 + 19", "pruebas de la App V1: backend y flujos en navegador"],
      ["0", "doble conteos detectados en la auditoría final"],
    ];
    st.forEach(([v, d], i) => {
      const x = 0.6 + i * 3.08;
      tarjeta(s, x, 1.5, 2.89, 2.3, K.blanco, true);
      texto(s, v, { x: x + 0.2, y: 1.6, w: 2.5, h: 1.0, fontSize: 38, bold: true, color: K.osc, valign: "middle" });
      texto(s, d, { x: x + 0.2, y: 2.65, w: 2.5, h: 1.05, fontSize: 13, color: K.txt });
    });
    s.addChart(pres.charts.BAR, [{ name: "pruebas", labels: ["Riesgo y optimizador", "Modelo financiero", "OPEX y capital de trabajo", "CAPEX"], values: [69, 70, 78, 82] }], {
      x: 0.6, y: 4.05, w: 7.2, h: 2.8, barDir: "bar", chartColors: [K.esti], showLegend: false, showValue: true, dataLabelFontSize: 12, dataLabelColor: K.txt, dataLabelFontFace: "+mn-lt", dataLabelPosition: "outEnd",
      showTitle: true, title: "Pruebas por motor económico (todas pasan)", titleFontSize: 14, titleColor: K.osc, titleFontFace: "+mn-lt",
      catAxisLabelFontSize: 12, catAxisLabelColor: K.txt, catAxisLabelFontFace: "+mn-lt", valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, barGapWidthPct: 50,
    });
    texto(s, [{ text: "Qué prueban y qué no", options: { bold: true, color: K.osc, fontSize: 15, breakLine: true } },
      { text: "Prueban que las cuentas son coherentes: que no se cuenta dos veces lo mismo, que un faltante no se vuelve cero y que una simulación no se vuelve evidencia. ", options: { breakLine: true } },
      { text: "No prueban que los datos sean correctos: eso solo lo resuelve el trabajo de campo.", options: { bold: true, color: K.rojo } }],
      { x: 8.1, y: 4.05, w: 4.63, h: 2.8, fontSize: 13, color: K.txt, paraSpaceAfter: 6, shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.claro }, margin: 10 });
    registrar(s, "A3 · Tests", "70/70 pruebas de integración, 15/15 mutaciones detectadas; las pruebas validan coherencia, no datos.",
      "Cómo sabemos que el motor hace bien las cuentas. Hay 70 pruebas de integración entre módulos y todas pasan. Además se introdujeron 15 errores a propósito —por ejemplo, contar dos veces la electricidad del frío o usar un precio de prensa como si fuera verificado— y las pruebas detectaron los 15. " +
      "Cada motor económico tiene su propia batería: entre 69 y 82 pruebas. La app tiene 52 pruebas de backend y 19 flujos probados en navegador. " +
      "Pero ojo: las pruebas garantizan coherencia interna, no que los datos sean correctos. Eso solo lo resuelve el trabajo de campo.");
  }

  // A4 tensiones
  {
    const s = contenido("A4 · Tensiones abiertas", "Anexo técnico");
    chipsArriba(s, ["PENDIENTE"]);
    tarjeta(s, 0.6, 1.5, 3.6, 5.3, K.osc, true);
    texto(s, "76", { x: 0.85, y: 1.7, w: 3.1, h: 1.3, fontSize: 66, bold: true, color: K.yema });
    texto(s, "tensiones registradas en la auditoría final", { x: 0.85, y: 3.0, w: 3.1, h: 0.7, fontSize: 15, color: K.blanco });
    texto(s, bullets(["71 abiertas", "4 corregidas", "1 mitigada en el motor"]), { x: 0.85, y: 3.9, w: 3.1, h: 1.6, fontSize: 15, color: "D7E4DB" });
    texto(s, "Ninguna tensión de negocio se resolvió.", { x: 0.85, y: 5.75, w: 3.1, h: 0.8, fontSize: 13, italic: true, color: "D7E4DB" });
    const ten = [
      ["Precios casi inexistentes", "en inversión y costos operativos"],
      ["Rendimientos del pollo sin ensayo", "el balance de masa usa referencias; falta medir en planta"],
      ["Pico de fondos vs CAPEX vs USD 2 M", "no se pueden comparar hasta tener costos y cronograma"],
      ["Granjas, incubadora y planta de alimento", "sin dotación ni consumos de agua y energía dimensionados"],
      ["Regla fiscal de ingresos brutos", "cómo tributan las exportaciones: pendiente de un contador"],
      ["Comparar alternativas", "hoy imposible: ninguna es costeable"],
    ];
    ten.forEach(([t, d], i) => {
      const x = 4.55 + (i % 2) * 4.18, y = 1.5 + Math.floor(i / 2) * 1.8;
      tarjeta(s, x, y, 4.0, 1.6, K.blanco, true);
      texto(s, t, { x: x + 0.2, y: y + 0.15, w: 3.6, h: 0.65, fontSize: 15, bold: true, color: K.osc, valign: "middle" });
      texto(s, d, { x: x + 0.2, y: y + 0.82, w: 3.6, h: 0.65, fontSize: 13, color: K.txt });
    });
    registrar(s, "A4 · Tensiones abiertas", "76 tensiones (71 abiertas); las principales son precios, rendimientos, pico de fondos, upstream, IIBB y comparabilidad.",
      "Una tensión es una inconsistencia o un problema conocido que no se pudo resolver con la información disponible. La auditoría final registró 76: 71 siguen abiertas, 4 se corrigieron y 1 quedó mitigada en el motor. " +
      "Las principales: no hay precios; los rendimientos del pollo no se midieron en una planta; no se puede comparar el capital necesario con los 2 millones; los módulos de granjas, incubadora y planta de alimento no tienen personal ni consumos dimensionados; " +
      "falta una definición fiscal sobre ingresos brutos en exportaciones; y hoy es imposible comparar alternativas porque ninguna se puede costear. Se dejan explícitas para no esconderlas.");
  }

  // A5 glosario
  {
    const s = contenido("A5 · Glosario", "Anexo técnico");
    const g = [
      ["Façon", "Un tercero hace el trabajo (faena o alimento) por cuenta nuestra, a cambio de una tarifa."],
      ["Asset-light", "Arrancar con pocos activos propios, apoyándose en terceros (C0)."],
      ["CAPEX", "Inversión: lo que se compra o construye antes de operar."],
      ["OPEX", "Costos de operar: alimento, pollitos, sueldos, energía, fletes."],
      ["Capital de trabajo", "Plata inmovilizada en stock y en ventas todavía no cobradas."],
      ["Ramp-up", "Arranque: meses en que la producción sube hasta la operación normal."],
      ["EBITDA", "Resultado de la operación antes de intereses, impuestos y amortizaciones."],
      ["VAN", "Valor que crea el proyecto por encima del rendimiento exigido."],
      ["TIR", "Rentabilidad implícita del proyecto."],
      ["Payback", "Tiempo para recuperar la inversión."],
      ["DSCR", "Cobertura de la deuda: caja disponible ÷ cuotas a pagar."],
      ["Rendering", "Proceso que convierte subproductos no comestibles en harinas y grasa."],
      ["CMS", "Carne mecánicamente separada: pasta de carne de carcasas para elaborados."],
      ["PVDP", "Pendiente de verificación documental primaria: visto, pero no leído en el original."],
    ];
    const half = Math.ceil(g.length / 2);
    g.forEach(([t, d], i) => {
      const col = i < half ? 0 : 1, fila = i % half;
      const x = 0.6 + col * 6.17, y = 1.45 + fila * 0.77;
      texto(s, t, { x, y, w: 1.95, h: 0.66, fontSize: 14, bold: true, color: K.osc, valign: "middle", shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.08, fill: { color: K.claro }, margin: 8 });
      texto(s, d, { x: x + 2.1, y, w: 3.85, h: 0.66, fontSize: 12.5, color: K.txt, valign: "middle" });
    });
    registrar(s, "A5 · Glosario", "Términos técnicos explicados en una línea.",
      "Glosario de los términos que aparecen en la presentación, en una línea cada uno. El glosario completo del proyecto, con más de un centenar de términos, está en la carpeta de gestión del proyecto y también en el diccionario de la app.");
  }
}

// =====================================================================================
function escribirGuion() {
  const l = [];
  l.push("# Guion de la presentación — Paquete ejecutivo V1");
  l.push("");
  l.push("**Fecha:** 2026-10-05 · **Archivo:** [`presentacion_nicas_doipe_v1.pptx`](presentacion_nicas_doipe_v1.pptx) · **Generado por:** [`generar_presentacion.js`](generar_presentacion.js) (este guion y las notas del PPTX salen del mismo texto; no editar a mano: editar el script y regenerar).");
  l.push("");
  l.push("> Estado que la presentación sostiene en todo momento: **MOTOR_V1 = COMPLETO ESTRUCTURALMENTE · APP_V1 = LISTA · LISTO_DECISION_REAL = NO** ([`../00_gestion_proyecto/auditoria_final_motor_v1.md`](../00_gestion_proyecto/auditoria_final_motor_v1.md) §30). No contiene montos de CAPEX/OPEX, rentabilidades ni recomendación de inversión.");
  l.push("");
  l.push("**Duración sugerida:** 30–35 minutos para las láminas 1–23 (≈ 1,5 min por lámina) + preguntas. El anexo (24–29) se usa solo si la audiencia es técnica.");
  l.push("");
  l.push("| # | Lámina | Mensaje |");
  l.push("|---|---|---|");
  for (const g of guion) l.push(`| ${g.n} | ${g.titulo} | ${g.mensaje} |`);
  l.push("");
  for (const g of guion) {
    l.push(`## ${g.n}. ${g.titulo}`);
    l.push("");
    l.push(`**Mensaje:** ${g.mensaje}`);
    l.push("");
    l.push(`**Notas del presentador:** ${g.notas}`);
    l.push("");
  }
  l.push("## Preguntas probables y respuesta honesta");
  l.push("");
  l.push("| Pregunta | Respuesta |");
  l.push("|---|---|");
  l.push("| ¿Cuánto cuesta la planta? | Todavía no se sabe: 167 de 175 conceptos de inversión no tienen precio. Hace falta cotizar (fase 2). |");
  l.push("| ¿Alcanzan los USD 2 M? | No se puede saber todavía, ni para sí ni para no. Además, la plata necesaria incluye el arranque y el capital de trabajo, no solo la planta. |");
  l.push("| ¿Cuánto se gana? | No hay ninguna rentabilidad calculada con datos reales. Se puede simular en la app con supuestos, pero sería una simulación, no un resultado. |");
  l.push("| ¿Los supermercados no alcanzan como demanda? | Hoy son un canal potencial: no hay volúmenes, precios ni condiciones confirmadas. Si se confirman, pueden ser cliente ancla. |");
  l.push("| ¿Qué alternativa conviene? | Ninguna está elegida. Depende de los datos y del objetivo del inversor. El optimizador puede incluso responder «no invertir aún». |");
  l.push("| ¿Dónde va la planta? | No hay ranking: 0 de 624 datos de la matriz verificados. Se decide terreno por terreno, con el municipio. |");
  l.push("| ¿Qué hacemos ahora? | Validar clientes y pedir cotizaciones (prioridad 1), siguiendo el checklist de la app. |");
  l.push("");
  fs.writeFileSync(GUION, l.join("\n"));
}

(async () => {
  await construir();
  await pres.writeFile({ fileName: SALIDA });
  const tema = process.env.APPLY_THEME;
  if (tema) { const { applyTheme } = require(tema); await applyTheme(SALIDA, THEME); }
  escribirGuion();
  console.log(`OK: ${nSlide} láminas → ${path.relative(process.cwd(), SALIDA)} · guion → ${path.relative(process.cwd(), GUION)}`);
})().catch((e) => { console.error(e); process.exit(1); });
