#!/usr/bin/env node
/*
 * PRUEBA EN NAVEGADOR REAL (opcional) — abre index.html desde file:// en Chromium sin red.
 *   NODE_PATH="$(npm root -g)" node 23_plan_expansion/simulador_html/pruebas/prueba_navegador.js [carpeta_capturas]
 * Requiere Playwright instalado (no es dependencia del simulador: solo de esta prueba).
 * Verifica: carga offline sin pedidos de red ni errores de consola; autoverificación completa;
 * todas las pestañas sin NaN/undefined/Infinity; utilización nunca > 100 %; cambiar la escala
 * actualiza los resultados; A/B/C independientes; sin scroll horizontal en celular/tablet/notebook.
 */
"use strict";
const path = require("path");
const fs = require("fs");
const { chromium } = require("playwright");

const AQUI = path.resolve(__dirname, "..");
const URL_HTML = "file://" + path.join(AQUI, "index.html");
const CAPTURAS = process.argv[2] || null;
const res = [];
const chk = (n, ok, d) => res.push([n, !!ok, d || ""]);

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 }, offline: true });
  const red = [], errores = [];
  await ctx.route("**/*", (route) => {
    const u = route.request().url();
    if (u.startsWith("file://")) return route.continue();
    red.push(u); return route.abort();
  });
  const page = await ctx.newPage();
  page.on("console", (m) => { if (m.type() === "error") errores.push(m.text()); });
  page.on("pageerror", (e) => errores.push(String(e)));
  await page.goto(URL_HTML);
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  await page.waitForSelector(".kpi");

  const pie = await page.textContent("#pie");
  const m = pie.match(/autoverificación (\d+)\/(\d+)/);
  chk("Autoverificación del motor en el navegador completa", m && m[1] === m[2] && +m[2] > 700, m ? m[0] : pie.slice(0, 80));

  const pestanas = await page.$$eval("#pestanas [data-p]", (bs) => bs.map((b) => b.dataset.p));
  const malas = [];
  for (const p of pestanas) {
    await page.click(`#pestanas [data-p="${p}"]`);
    const t = await page.textContent("#vista");
    if (/NaN|undefined|Infinity|\[object/.test(t)) malas.push(p);
    if (CAPTURAS) await page.screenshot({ path: path.join(CAPTURAS, `escritorio_${p}.png`), fullPage: true });
  }
  chk("Las " + pestanas.length + " pestañas se renderizan sin NaN / undefined / Infinity", malas.length === 0, malas.join(", "));

  // cambiar la escala actualiza los resultados (escenario A = 5.000 por defecto)
  await page.click('#pestanas [data-p="resumen"]');
  const aves = async () => (await page.textContent(".kpi .kpi-valor")).trim();
  const a5 = await aves();
  await page.click('#panel-entradas .chip[data-k="escala"][data-v="20000"]');
  const a20 = await aves();
  chk("Cambiar la escala 5.000 → 20.000 actualiza aves/año", a5 === "875.000" && a20 === "3.500.000", `${a5} → ${a20}`);

  // utilización al 100 % y demanda expansiva > capacidad: nunca > 100 %
  await page.fill('#panel-entradas input[type="number"][data-k="utilizacion"]', "100");
  await page.selectOption('#panel-entradas select[data-k="demanda_id"]', "ESC-EXP");
  await page.click('#panel-entradas .chip[data-k="escala"][data-v="2500"]');
  const util = await page.$$eval(".metrica.util .metrica-valor, .metrica.cob .metrica-valor", (els) => els.map((e) => e.textContent));
  const fac = await page.textContent(".metrica.factor .metrica-valor");
  const nums = util.map((x) => parseFloat(x.replace(/\./g, "").replace(",", ".")));
  const noAt = await page.textContent(".caja-estado.falta.activa .valor").catch(() => "");
  chk("Demanda > capacidad: utilización y cobertura ≤ 100 %, factor > 100 % y demanda no atendida visible",
    nums.every((x) => x <= 100) && parseFloat(fac.replace(/\./g, "")) > 100 && noAt.length > 0, `${util.join(" / ")} · factor ${fac} · no atendida ${noAt}`);
  const alertas = await page.textContent("#alertas");
  chk("Alertas de demanda > capacidad y demanda documentada ≈ 0 presentes", /excede la capacidad instalada/.test(alertas) && /Demanda documentada/.test(alertas));

  // A/B/C independientes en la interfaz
  const nombreB = await page.textContent('[data-slot="B"] .det');
  await page.click('[data-slot="B"]');
  const escalaB = await page.inputValue('#panel-entradas input[type="number"][data-k="escala"]');
  await page.click('[data-slot="A"]');
  const escalaA = await page.inputValue('#panel-entradas input[type="number"][data-k="escala"]');
  chk("Escenarios A/B/C independientes en la interfaz (A editado a 2.500; B conserva 10.000)", escalaA === "2500" && escalaB === "10000", `A=${escalaA} B=${escalaB} (${nombreB})`);
  await page.click('#pestanas [data-p="comparador"]');
  const comp = await page.textContent("table.comp");
  chk("El comparador muestra las tres columnas y la economía como versión futura", /Escenario A/.test(comp) && /Escenario C/.test(comp) && /versión futura/.test(comp));
  const ecoDeshab = await page.$eval('#pestanas [data-p="economia"]', (b) => b.classList.contains("deshabilitada"));
  await page.click('#pestanas [data-p="economia"]');
  const eco = await page.textContent("#vista");
  chk("Economía del proyecto deshabilitada, sin cifras", ecoDeshab && /Disponible en una versión posterior/.test(eco) && !/\d{2,}\s*(USD|US\$)/.test(eco));

  // entrada incompatible: días/año > días/semana × 52,14
  await page.click('[data-slot="C"]');
  await page.click("#avanzado summary");
  await page.fill('#panel-entradas input[data-k="dias_anio"]', "290");
  const bloq = await page.textContent("#alertas");
  chk("Entrada incompatible (290 días/año con 5 d/sem) bloquea el cálculo", /Entradas incompatibles/.test(bloq));
  await page.fill('#panel-entradas input[data-k="dias_anio"]', "250");

  // --- auditoría semántica ---
  await page.click('[data-slot="B"]');
  await page.click('#pestanas [data-p="resumen"]');
  const comoLeer = await page.textContent("details.como-leer");
  const cfg = await page.$$eval('#panel-entradas .chip[data-k="config"]', (bs) => bs.map((b) => b.textContent.trim()));
  chk("Caja «Cómo leer este simulador» visible y configuraciones sin letras A/B/C",
    /escenarios físicos, no una recomendación de inversión/.test(comoLeer) && cfg.join("|") === "Pollo entero|Trozado|Deshuesado / mayor procesamiento", cfg.join(" | "));
  // ejemplo 10.000 aves/día al 50 % con demanda que requiere 8.000 aves/día operativo (M0, trozado, 2,9 kg, 250 d)
  const D = await page.evaluate(() => 8000 * 250 / 365 * window.SimCalculo.kgPorAve(window.SIMULADOR_DATA, "B", 2.9).comestible);
  await page.fill('#panel-entradas input[type="range"][data-k="utilizacion"]', "50");
  await page.selectOption('#panel-entradas select[data-k="demanda_id"]', "MANUAL");
  await page.fill('#panel-entradas input[data-k="demanda_manual_kg"]', String(Math.round(D * 1000) / 1000));
  await page.click('#pestanas [data-p="demanda"]');
  const dem = await page.textContent("#vista");
  const cobOp = (await page.textContent(".metrica.cob .metrica-valor")).trim();
  chk("Ejemplo 10.000 al 50 % con demanda de 8.000: la interfaz muestra que la capacidad alcanza pero el escenario operativo cubre 62,5 %",
    cobOp === "62,5 %" && /sí alcanza técnicamente/.test(dem) && /Máxima posible a plena capacidad: 100 %/.test(dem) && /Capacidad ociosa operativa/.test(dem)
    && /Capacidad disponible respecto de la demanda/.test(dem), `cobertura operativa mostrada: ${cobOp}`);
  // escala fuera del rango principal (solo desde el modo avanzado)
  const simple = '#escala-simple';
  await page.fill(simple, "1000");
  const noAplicada = (await page.textContent('[data-slot="B"] .det')).startsWith("10.000");
  await page.fill('#panel-entradas fieldset:has(legend:text("Escala fuera del rango principal")) input[data-k="escala"]', "1000").catch(async () => {
    await page.click("#avanzado summary");
    await page.fill('#panel-entradas fieldset:has(legend:text("Escala fuera del rango principal")) input[data-k="escala"]', "1000");
  });
  const al = await page.textContent("#alertas") + await page.textContent(".banderas");
  chk("Modo simple no acepta escalas fuera de 2.500–20.000; el avanzado sí, con «ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO»",
    noAplicada && /ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO/.test(al));
  // solo demanda documentada + 100 %
  await page.fill('#panel-entradas input[type="range"][data-k="utilizacion"]', "100");
  await page.selectOption('#panel-entradas select[data-k="demanda_id"]', "CERO");
  const v0 = await page.textContent("#vista"), a0 = await page.textContent("#alertas");
  chk("Solo demanda documentada: «DEMANDA DOCUMENTADA ACTUAL: NO VALIDADA / PRÁCTICAMENTE NULA» y alerta de producción al 100 % sin respaldo",
    /DEMANDA DOCUMENTADA ACTUAL: NO VALIDADA \/ PRÁCTICAMENTE NULA/.test(v0) && /simula producción al 100 %, pero actualmente no existe demanda documentada/.test(a0));
  // etiqueta de certeza
  let validado = false, calculado = false;
  for (const p of pestanas) {
    await page.click(`#pestanas [data-p="${p}"]`);
    const t = await page.textContent("body");
    if (/validado por modelo/i.test(t)) validado = true;
    if (/Calculado por modelo/.test(t)) calculado = true;
  }
  chk("Etiqueta «Calculado por modelo» (nunca «Validado por modelo») en todas las pestañas", calculado && !validado);
  if (CAPTURAS) { await page.click('#pestanas [data-p="demanda"]'); }

  // responsive: sin scroll horizontal
  const anchos = [[390, 844, "celular"], [820, 1180, "tablet"], [1366, 900, "notebook"], [1920, 1080, "monitor"]];
  const desbordes = [];
  for (const [w, h, n] of anchos) {
    await page.setViewportSize({ width: w, height: h });
    for (const p of ["resumen", "demanda", "productos", "comparador"]) {
      await page.click(`#pestanas [data-p="${p}"]`);
      const sw = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
      if (sw > 1) desbordes.push(`${n}/${p}: +${sw}px`);
      if (CAPTURAS && (p === "resumen" || w === 390)) await page.screenshot({ path: path.join(CAPTURAS, `${n}_${p}.png`), fullPage: p === "resumen" });
    }
  }
  chk("Sin scroll horizontal de página en celular (390 px), tablet, notebook y monitor", desbordes.length === 0, desbordes.join("; "));

  chk("Funciona offline: ningún pedido de red; sin errores de consola", red.length === 0 && errores.length === 0,
    `pedidos bloqueados ${red.length} ${red.slice(0, 3).join(" ")}; errores ${errores.slice(0, 3).join(" | ")}`);
  await browser.close();

  console.log("\nPRUEBA EN NAVEGADOR (Chromium, file://, sin red)");
  res.forEach(([n, ok, d]) => console.log(`  [${ok ? "OK " : "FALLA"}] ${n}${d ? `\n      ${d}` : ""}`));
  const bien = res.filter((r) => r[1]).length;
  console.log(`  Resultado: ${bien}/${res.length} correctos\n`);
  process.exit(bien === res.length ? 0 : 1);
})().catch((e) => { console.error(e); process.exit(1); });
