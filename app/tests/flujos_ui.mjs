// Flujos de usuario en el NAVEGADOR (#52) con Playwright. Los lanza app/tests/correr_tests.py (que levanta la app).
//   APP_URL=http://127.0.0.1:8765/ node app/tests/flujos_ui.mjs
// Si Playwright no está instalado, el runner informa OMITIDO (los mismos flujos se prueban por HTTP en test_flujos.py).
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const URL_APP = process.env.APP_URL || "http://127.0.0.1:8765/";
let pw;
try { pw = await import(process.env.PLAYWRIGHT_MODULE || "playwright"); } catch (e) { console.log("OMITIDO: playwright no disponible"); process.exit(3); }
const { chromium } = pw.default?.chromium ? pw.default : pw;

const resultados = [];
async function flujo(nombre, fn) {
  const t = Date.now();
  try { await fn(); resultados.push([nombre, "OK", Date.now() - t]); }
  catch (e) { resultados.push([nombre, "FALLA: " + e.message.split("\n")[0], Date.now() - t]); }
}
function afirmar(c, msg) { if (!c) throw new Error(msg); }

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 }, acceptDownloads: true });
const p = await ctx.newPage();
const errores = [];
p.on("pageerror", (e) => errores.push(e.message));
p.on("dialog", (d) => d.accept(d.defaultValue() || "nombre de prueba"));
const LARGO = { timeout: 240000 };

await flujo("FLUJO 1: abrir app → crear escenario → cargar inputs → simular → ver resultado", async () => {
  await p.goto(URL_APP);
  await p.waitForSelector(".accion-home");
  await p.click("text=Empezar un escenario vacío");
  await p.waitForSelector("[data-simular]");
  await p.click('[data-objetivo="GANAR_MAS"]');
  await p.click('[data-paso="capital"]'); await p.click('[data-capital="no_se"]');
  await p.click('[data-paso="demanda"]'); await p.click("[data-agregar-demanda]");
  await p.fill("[data-linea-demanda='0'] [data-volumen]", "4"); await p.press("[data-linea-demanda='0'] [data-volumen]", "Tab");
  await p.click('[data-paso="precios"]'); await p.click("[data-precios-desde-demanda]");
  await p.selectOption("[data-linea-precio='precios_venta-0'] [data-estado-dato]", "ESCENARIO");
  await p.fill("[data-linea-precio='precios_venta-0'] [data-valor-precio]", "3.2"); await p.press("[data-linea-precio='precios_venta-0'] [data-valor-precio]", "Tab");
  await p.click('[data-paso="arquitectura"]'); await p.click('[data-arquitectura="MANUAL"]'); await p.click('[data-config="C1"]');
  await p.click('[data-paso="escala"]'); await p.click('[data-escala="10000"]');
  await p.click("[data-simular]");
  await p.waitForSelector("[data-resultado='ALTERNATIVA']", LARGO);
  afirmar(await p.locator(".banner-sim").count() > 0, "falta el rótulo de SIMULACIÓN HIPOTÉTICA");
  afirmar(await p.locator("[data-tarjeta]").count() >= 8, "faltan tarjetas de resultado");
  const nocalc = await p.locator(".item.nocalc .val").allInnerTexts();
  afirmar(nocalc.length > 0, "un escenario incompleto debe mostrar NO CALCULABLE");
  afirmar(nocalc.every((t) => !/USD|%|años/.test(t)), "un NO CALCULABLE se mostró como número");
  afirmar(await p.locator("[data-disclaimer]").count() > 0, "falta el disclaimer");
});

await flujo("FLUJO 2: comparar C0 vs C1 (demo)", async () => {
  await p.goto(URL_APP + "#/inicio");
  await p.waitForSelector("[data-abrir-demo]");
  await p.click("[data-abrir-demo]");
  await p.waitForSelector("[data-simular]");
  await p.goto(URL_APP + "#/comparar");
  await p.waitForSelector("[data-alt]", LARGO);
  await p.check('[data-alt="DEMO-C0|BASE|10000|ESCALA_UNICA"]');
  await p.check('[data-alt="DEMO-C1|BASE|10000|ESCALA_UNICA"]');
  await p.click("[data-comparar]");
  await p.waitForSelector("[data-comparable='true']", LARGO);
  afirmar(await p.locator("[data-tabla-comparacion] th:has-text('DEMO-C1|BASE|10000')").count() === 1, "falta C1 en la comparación");
  afirmar(await p.locator(".banner-demo").count() > 0, "falta el rótulo SOLO DEMOSTRACIÓN");
});

await flujo("FLUJO 3: optimizar con límite de capital", async () => {
  await p.goto(URL_APP + "#/optimizar");
  await p.waitForSelector("[data-optimizar]");
  await p.fill("[data-opt-capital]", "1200000"); await p.press("[data-opt-capital]", "Tab");
  await p.click("[data-optimizar]");
  await p.waitForSelector("[data-resultado-optimizador]", LARGO);
  afirmar(await p.locator("[data-decision]").count() === 1, "falta la decisión del escenario");
  const txt = await p.locator("[data-resultado-optimizador]").innerText();
  afirmar(txt.includes("CAPITAL_DISPONIBLE"), "la restricción de capital no aparece");
});

await flujo("FLUJO 4: ejecutar stress", async () => {
  await p.goto(URL_APP + "#/riesgos");
  await p.waitForSelector("[data-alt-riesgo]", LARGO);
  await p.click("[data-pestana='stress']");
  await p.click("[data-correr-stress]");
  await p.waitForSelector("text=VAN: base vs stress", LARGO);
  afirmar((await p.locator("table.t").last().innerText()).includes("OK"), "stress sin resultados");
});

await flujo("FLUJO 5: guardar / exportar / importar escenario", async () => {
  await p.click("#btn-guardar");
  await p.waitForFunction(() => !document.querySelector("[data-sin-guardar]"), null, LARGO);
  await p.click("#btn-escenarios");
  await p.waitForSelector("[data-accion='exportar-actual']");
  const [dl] = await Promise.all([p.waitForEvent("download"), p.click("[data-accion='exportar-actual']")]);
  const ruta = path.join(fs.mkdtempSync(path.join(os.tmpdir(), "ui-")), "esc.json");
  await dl.saveAs(ruta);
  const j = JSON.parse(fs.readFileSync(ruta, "utf8"));
  afirmar(j.formato === "ESCENARIO_APP_AVICOLA" && j.version_formato === 1 && j.sello, "exportación sin formato versionado");
  await p.setInputFiles("[data-importar]", ruta);
  await p.waitForFunction(() => document.getElementById("toast")?.textContent.includes("importado"), null, LARGO);
});

await flujo("FLUJO 6: consultar qué validar", async () => {
  await p.click("[data-cerrar]").catch(() => {});
  await p.goto(URL_APP + "#/validacion");
  await p.waitForSelector("[data-paquete]", LARGO);
  afirmar(await p.locator("[data-paquete]").count() === 12, "deben verse 12 paquetes");
  await p.click("[data-paquete='CLIENTES']");
  await p.waitForSelector("[data-detalle-paquete='CLIENTES']");
  afirmar((await p.locator("[data-detalle-paquete]").innerText()).includes("Qué pedir"), "detalle sin pedidos");
  await p.click("[data-cerrar]");
  afirmar(await p.locator("[data-dimension]").count() === 4, "el progreso debe separar 4 dimensiones");
});

await flujo("EXTRA: NO_INVERTIR_AUN se representa (demo, capital USD 50 mil, arquitectura automática)", async () => {
  await p.goto(URL_APP + "#/inicio");
  await p.click("[data-abrir-demo]");
  await p.waitForSelector("[data-simular]");
  await p.click('[data-paso="capital"]'); await p.click('[data-capital="valor"]');
  await p.fill("[data-campo='capital']", "50000"); await p.press("[data-campo='capital']", "Tab");
  await p.click("[data-simular]");
  await p.waitForSelector("[data-no-invertir='NO_INVERTIR_AUN']", LARGO);
  afirmar(!(await p.locator("[data-no-invertir]").innerText()).toLowerCase().includes("error"), "NO_INVERTIR_AUN presentado como error");
});

await flujo("EXTRA: ¿por qué me da este resultado? + móvil", async () => {
  await p.goto(URL_APP + "#/simular");
  await p.click('[data-paso="capital"]'); await p.click('[data-capital="no_se"]');
  await p.click("[data-simular]");
  await p.waitForSelector("[data-boton-por-que]", LARGO);
  await p.click("[data-boton-por-que]");
  await p.waitForSelector("[data-por-que]");
  const m = await ctx.newPage();
  await m.setViewportSize({ width: 390, height: 844 });
  await m.goto(URL_APP + "#/inicio");
  await m.waitForSelector(".accion-home");
  const ancho = await m.evaluate(() => document.documentElement.scrollWidth);
  afirmar(ancho <= 400, `scroll horizontal en móvil (${ancho}px)`);
  await m.close();
});

await browser.close();
let fallas = 0;
for (const [n, r, ms] of resultados) { console.log(`${r === "OK" ? "OK   " : "FALLA"} ${n} (${(ms / 1000).toFixed(1)} s)${r === "OK" ? "" : " — " + r}`); if (r !== "OK") fallas++; }
if (errores.length) { console.log("Errores de página:", errores.join(" | ")); fallas++; }
process.exit(fallas ? 1 : 0);
