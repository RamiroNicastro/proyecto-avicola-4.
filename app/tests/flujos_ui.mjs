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
  catch (e) {
    resultados.push([nombre, "FALLA: " + e.message.split("\n")[0], Date.now() - t]);
    if (process.env.UI_CAPTURAS && globalThis.__pagina) await globalThis.__pagina.screenshot({ path: path.join(process.env.UI_CAPTURAS, `falla_${resultados.length}.png`) }).catch(() => {});
  }
}
function afirmar(c, msg) { if (!c) throw new Error(msg); }

const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
const ctx = await browser.newContext({ viewport: { width: 1360, height: 900 }, acceptDownloads: true });
await ctx.addInitScript(() => { try { if (!sessionStorage.getItem("t")) { localStorage.setItem("avicola.app.primer_uso", "directo"); sessionStorage.setItem("t", "1"); } } catch (e) { /* */ } });
const p = await ctx.newPage();
globalThis.__pagina = p;
const errores = [];
p.on("pageerror", (e) => errores.push(e.message));
p.on("dialog", (d) => d.accept(d.defaultValue() || "nombre de prueba"));
const LARGO = { timeout: 240000 };
const ir = async (r) => { await p.goto(URL_APP + "#/" + r); await p.waitForTimeout(150); };
const vista = (r) => p.waitForFunction((x) => document.getElementById("vista")?.dataset.vista === x && !document.querySelector("#vista [data-cargando]"), r, LARGO);

// Texto VISIBLE de una zona, sin los códigos técnicos (.codigo-tecnico) ni el contenido de acordeones cerrados.
async function textoVisible(sel) {
  return p.evaluate((s) => {
    const raiz = document.querySelector(s);
    if (!raiz) return "";
    const out = [];
    const w = document.createTreeWalker(raiz, NodeFilter.SHOW_TEXT);
    while (w.nextNode()) {
      const el = w.currentNode.parentElement;
      if (el.closest(".codigo-tecnico")) continue;
      const det = el.closest("details");
      if (det && !det.open && !el.closest("summary")) continue;
      if (!el.offsetParent) continue;
      out.push(w.currentNode.textContent);
    }
    return out.join(" ");
  }, sel);
}
const CODIGO = /\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b/;
const RUTA_ARCHIVO = /[\w-]+\.(csv|md|py|json)\b/;

// Asistente de 5 pasos: escenario vacío → C1 · 10.000 → precio de escenario → SIMULAR.
async function asistenteBasico() {
  await ir("inicio"); await p.click("[data-escenario-vacio]"); await p.waitForSelector("[data-continuar]");
  afirmar((await p.locator("[data-paso-n]").innerText()).includes("Paso 1 de 5"), "falta «Paso 1 de 5»");
  await p.click('[data-objetivo="GANAR_MAS"]'); await p.click("[data-continuar]");
  afirmar((await p.locator("[data-paso-n]").innerText()).includes("Paso 2 de 5"), "CONTINUAR no avanzó");
  await p.click('[data-capital="no_se"]');
  afirmar(await p.locator("[data-no-se-explica]").count() === 1, "«No sé» del capital no explica qué no se calcula");
  await p.click("[data-continuar]");
  await p.click('[data-demanda="cargar"]');
  await p.fill("[data-linea-demanda='0'] [data-volumen]", "4"); await p.press("[data-linea-demanda='0'] [data-volumen]", "Tab");
  await p.click("[data-continuar]");
  await p.click('[data-arquitectura="MANUAL"]'); await p.click('[data-config="C1"]'); await p.click('[data-escala="10000"]');
  await p.click("[data-continuar]");
  await p.click('[data-precios="cargar"]');
  await p.fill("[data-linea-precio='precios_venta-0'] [data-valor-precio]", "3.2"); await p.press("[data-linea-precio='precios_venta-0'] [data-valor-precio]", "Tab");
}

await flujo("FLUJO 1: crear escenario con el asistente de 5 pasos → simular → resultado simple", async () => {
  await asistenteBasico();
  await p.click("[data-atras]"); await p.click("[data-atras]");
  afirmar(await p.inputValue("[data-linea-demanda='0'] [data-volumen]") === "4", "ATRÁS perdió los datos cargados");
  await p.click('[data-paso="precios"]');
  await p.click("[data-simular]");
  await p.waitForSelector("[data-resultado='ALTERNATIVA']", LARGO);
  afirmar(await p.locator(".banner-sim").count() > 0, "falta el rótulo de SIMULACIÓN");
  const n = await p.locator("[data-kpis] [data-kpi]").count();
  afirmar(n >= 1 && n <= 6, `el resultado simple debe tener 1–6 números clave (tiene ${n})`);
  afirmar((await p.locator("[data-titular]").innerText()).includes("Todavía faltan datos para calcular rentabilidad"), "frase superior incorrecta para un escenario incompleto");
  const nd = await p.locator("[data-kpi-nd]").allInnerTexts();
  afirmar(nd.length > 0 && nd.every((t) => !/USD|%|años/.test(t)), "un NO CALCULABLE se mostró como número");
  afirmar(nd.some((t) => t.startsWith("No se puede calcular todavía porque")), "el faltante no está explicado en castellano");
  for (const a of ["inversion", "rentabilidad", "riesgos", "tecnico"]) afirmar(await p.locator(`[data-acordeon='${a}']`).count() === 1, "falta el acordeón " + a);
  afirmar(await p.locator("[data-disclaimer]").count() > 0, "falta el disclaimer");
});

await flujo("FLUJO 2: comparar C0 vs C1 (demo)", async () => {
  await ir("inicio"); await p.click("[data-abrir-demo]"); await p.waitForSelector("[data-continuar]");
  await ir("comparar");
  await p.waitForSelector("[data-alt]", LARGO);
  await p.check('[data-alt="DEMO-C0|BASE|10000|ESCALA_UNICA"]');
  await p.check('[data-alt="DEMO-C1|BASE|10000|ESCALA_UNICA"]');
  await p.click("[data-comparar]");
  await p.waitForSelector("[data-comparable='true']", LARGO);
  afirmar(await p.locator("[data-tabla-comparacion] th:has-text('DEMO-C1|BASE|10000')").count() === 1, "falta C1 en la comparación");
  afirmar(await p.locator(".banner-demo").count() > 0, "falta el rótulo SOLO DEMOSTRACIÓN");
});

await flujo("FLUJO 3: optimizar con límite de capital", async () => {
  await ir("optimizar");
  await p.waitForSelector("[data-optimizar]");
  await p.fill("[data-opt-capital]", "1200000"); await p.press("[data-opt-capital]", "Tab");
  await p.click("[data-optimizar]");
  await p.waitForSelector("[data-resultado-optimizador]", LARGO);
  afirmar(await p.locator("[data-decision]").count() === 1, "falta la decisión del escenario");
  afirmar((await p.locator("[data-resultado-optimizador]").innerText()).includes("CAPITAL_DISPONIBLE"), "la restricción de capital no aparece");
});

await flujo("FLUJO 4: ejecutar stress", async () => {
  await ir("riesgos?tab=stress");
  await p.waitForSelector("[data-correr-stress]", LARGO);
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
  await p.click("[data-cerrar]").catch(() => {});
});

await flujo("FLUJO 6: qué validar (checklist por paquete)", async () => {
  await ir("validacion");
  await p.waitForSelector("[data-paquete]", LARGO);
  afirmar(await p.locator("[data-paquete]").count() === 12, "deben verse 12 paquetes");
  await p.click("[data-paquete='PLANTA'] > summary");
  const t = (await p.locator("[data-detalle-paquete='PLANTA']").innerText()).toLowerCase();
  for (const x of ["estado", "qué pedir", "a quién", "unidad", "desbloquea", "por qué importa"]) afirmar(t.includes(x), "checklist incompleto: falta " + x);
  afirmar(await p.locator("[data-pedido] .caja:has-text('☑')").count() === 0, "un pedido aparece marcado sin evidencia");
  afirmar(await p.locator("[data-dimension]").count() === 4, "el progreso debe separar 4 dimensiones");
});

await flujo("EXTRA: NO_INVERTIR_AUN se representa (demo, capital USD 50 mil, automático)", async () => {
  await ir("inicio"); await p.click("[data-abrir-demo]"); await p.waitForSelector("[data-continuar]");
  await p.click('[data-paso="capital"]'); await p.click('[data-capital="valor"]');
  await p.fill("[data-campo='capital']", "50000"); await p.press("[data-campo='capital']", "Tab");
  await p.click('[data-paso="precios"]'); await p.click("[data-simular]");
  await p.waitForSelector("[data-no-invertir='NO_INVERTIR_AUN']", LARGO);
  const t = await p.locator("[data-no-invertir]").innerText();
  afirmar(!t.toLowerCase().includes("error") && t.includes("NO es un fracaso"), "NO_INVERTIR_AUN presentado como error");
});

await flujo("EXTRA: DSCR mínimo del horizonte con aviso de ramp-up + ¿por qué? + móvil", async () => {
  await ir("inicio"); await p.click("[data-abrir-demo]"); await p.waitForSelector("[data-continuar]");
  await p.click('[data-paso="alternativa"]'); await p.click('[data-arquitectura="MANUAL"]'); await p.click('[data-config="C1"]'); await p.click('[data-escala="10000"]');
  await p.click('[data-paso="precios"]'); await p.click("[data-simular]");
  await p.waitForSelector("[data-resultado='ALTERNATIVA']", LARGO);
  afirmar((await p.locator("[data-kpi='DSCR MÍNIMO']").innerText()).toUpperCase().includes("DSCR MÍNIMO DEL HORIZONTE"), "falta «DSCR mínimo del horizonte»");
  const av = await p.locator("[data-aviso-rampa]").innerText();
  afirmar(av.includes("arranque") && av.includes("No significa que la deuda sea impagable"), "falta el aviso de ramp-up del DSCR");
  afirmar((await p.locator("[data-titular]").innerText()).startsWith("Con los datos que cargaste"), "frase superior incorrecta");
  await p.click("[data-kpi='DSCR MÍNIMO'] [data-ayuda]");
  afirmar(!(await p.locator("#popover").isHidden()), "la ayuda «?» del DSCR no se abre");
  await p.click("[data-acordeon='tecnico'] > summary");
  await p.click("[data-boton-por-que]");
  await p.waitForSelector("[data-por-que]");
  const m = await ctx.newPage();
  await m.setViewportSize({ width: 390, height: 844 });
  for (const r of ["inicio", "localizacion", "proceso", "simular"]) {
    await m.goto(URL_APP + "#/" + r); await m.waitForTimeout(900);
    const ancho = await m.evaluate(() => document.documentElement.scrollWidth);
    afirmar(ancho <= 400, `scroll horizontal en móvil en ${r} (${ancho}px)`);
  }
  await m.close();
});

// ------------------------------------------------------------------ usuario no técnico (#35–#36)
async function clicsDesdeInicio(pasos, final) {
  await ir("inicio"); await p.waitForSelector("[data-home]");
  for (const s of pasos) { await p.click(s); await p.waitForTimeout(250); }
  await p.waitForSelector(final, LARGO);
  return pasos.length;
}

await flujo("NAV: localización ≤ 3 clics desde el inicio", async () => {
  afirmar(await clicsDesdeInicio(["[data-ir='localizacion']"], "[data-sin-ganadora]") <= 3, "más de 3 clics");
  afirmar((await p.locator("[data-sin-ganadora]").innerText()).includes("Todavía no existe una ubicación ganadora porque faltan datos de campo."), "falta el aviso sin ranking");
  afirmar(await clicsDesdeInicio(["#nav a[data-ruta='localizacion']"], "[data-localizacion]") <= 3, "más de 3 clics por la barra lateral");
  afirmar((await p.getAttribute("#migas", "data-migas")).includes("PROYECTO > LOCALIZACIÓN"), "migas de pan incorrectas");
});

await flujo("NAV: proceso industrial ≤ 3 clics", async () => {
  afirmar(await clicsDesdeInicio(["#nav a[data-ruta='grupo/planta']", "[data-ir='proceso']"], "[data-etapas]") <= 3, "más de 3 clics");
  await p.click("[data-etapa='E18']");
  const t = (await p.locator("[data-detalle-etapa]").innerText()).toLowerCase();
  for (const x of ["enfriamiento", "qué pasa", "riesgos", "capacidad", "equipos de referencia", "agua y energía", "pendiente"]) afirmar(t.includes(x), "la etapa no muestra: " + x);
  afirmar(await p.locator("[data-aviso-benchmark]").count() === 1, "falta el aviso de que los equipos no son especificación");
  afirmar((await p.getAttribute("#migas", "data-migas")).includes("PROYECTO > PLANTA Y PROCESOS"), "migas de pan del proceso");
});

await flujo("NAV: estado del proyecto ≤ 2 clics", async () => {
  afirmar(await clicsDesdeInicio(["[data-ir='estado']"], "[data-estado-proyecto]") <= 2, "más de 2 clics");
  const t = await p.locator("[data-semaforo-estado]").innerText();
  for (const x of ["COMPLETO", "PARCIALES", "MUY INCOMPLETOS", "0 %", "NO DISPONIBLE"]) afirmar(t.includes(x), "falta " + x);
});

await flujo("NAV: productos, faena y CAPEX ≤ 3 clics; volver al inicio siempre visible", async () => {
  await clicsDesdeInicio(["#nav a[data-ruta='grupo/productos']", "[data-ir='productos']"], "[data-aviso-rutas]");
  await clicsDesdeInicio(["#nav a[data-ruta='grupo/planta']", "[data-modulo='faena']"], "[data-ficha-modulo='faena']");
  afirmar((await p.getAttribute("#migas", "data-migas")) === "INICIO > PROYECTO > PLANTA Y PROCESOS > PLANTA DE FAENA", "migas de pan del módulo faena");
  await clicsDesdeInicio(["#nav a[data-ruta='grupo/inversion']", "[data-modulo='capex']"], "[data-ficha-modulo='capex']");
  for (const q of ["que_es", "por_que", "que_modelamos", "que_sabemos", "que_falta"]) afirmar(await p.locator(`[data-pregunta='${q}']`).count() === 1, "falta la pregunta " + q);
  afirmar(await p.locator("[data-ver-fuentes]").count() === 1 && await p.locator("[data-conf]").count() > 0, "faltan chips de confianza o VER FUENTES");
  await p.click("[data-detalle-tecnico] > summary"); await p.waitForSelector("[data-detalle-tecnico] .md h2, [data-detalle-tecnico] .md h3, [data-detalle-tecnico] .md p", LARGO);
  afirmar(await p.locator("[data-volver-inicio]").isVisible(), "el botón Volver al inicio no está visible");
  await p.click("[data-volver-inicio]"); await p.waitForSelector("[data-home]");
});

await flujo("BÚSQUEDA: «localización» → localización; «faena» → proceso", async () => {
  await ir("inicio");
  for (const [q, destino] of [["localización", "#/localizacion"], ["faena", "#/proceso"], ["CAPEX", "#/estudio/capex"]]) {
    await p.fill("[data-buscar-global]", q); await p.press("[data-buscar-global]", "Enter");
    await p.waitForFunction((d) => location.hash === d, destino, LARGO);
  }
});

await flujo("DICCIONARIO buscable", async () => {
  await ir("diccionario"); await p.waitForSelector("[data-buscar-glosario]");
  await p.fill("[data-buscar-glosario]", "FCR");
  await p.waitForTimeout(200);
  afirmar((await p.locator("[data-termino]").first().innerText()).includes("FCR"), "el diccionario no encuentra FCR");
  await p.fill("[data-buscar-glosario]", "zzzz-inexistente");
  afirmar(await p.locator("[data-vacio] [data-cta]").count() === 1, "diccionario vacío sin explicación/acción");
});

await flujo("BALANCEADO: sin pesos no se ejecuta; repartir por igual = 100 %; PESOS_NO_DEFINIDOS ≠ NO_INVERTIR_AUN", async () => {
  await ir("inicio"); await p.click("[data-abrir-demo]"); await p.waitForSelector("[data-continuar]");
  await p.click('[data-objetivo="BALANCEADO"]');
  afirmar(await p.getAttribute("[data-total-pesos]", "data-total-pesos") === "0", "la demo no debería traer pesos");
  await p.click('[data-paso="precios"]');
  afirmar(await p.locator("[data-simular]").isDisabled(), "SIMULAR habilitado sin pesos");
  afirmar(await p.locator("[data-bloqueo-pesos]").count() === 1, "falta el aviso de pesos no definidos");
  afirmar(await p.locator("[data-no-invertir]").count() === 0, "PESOS_NO_DEFINIDOS se mostró como no invertir");
  const r = await p.evaluate(async () => { const e = structuredClone(window.__app.E.escenario);
    const x = await fetch("/api/simular", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ escenario: e }) }); return [x.status, (await x.json()).error.codigo]; });
  afirmar(r[0] === 400 && r[1] === "PESOS_NO_DEFINIDOS", "el backend no bloquea BALANCEADO sin pesos: " + r);
  await p.click('[data-paso="objetivo"]'); await p.click("[data-repartir]");
  afirmar(await p.getAttribute("[data-total-pesos]", "data-total-pesos") === "100", "repartir por igual no suma 100 %");
  await p.click('[data-paso="precios"]');
  afirmar(!(await p.locator("[data-simular]").isDisabled()), "SIMULAR sigue bloqueado con pesos al 100 %");
});

await flujo("USUARIO SIMPLE: sin códigos técnicos ni rutas de archivos como texto principal", async () => {
  for (const r of ["inicio", "estudio/localizacion", "localizacion", "proceso", "productos", "escalas", "estado", "seguir", "validacion"]) {
    await ir(r); await vista(r.split("/")[0]);
    const t = await textoVisible("#vista");
    afirmar(!RUTA_ARCHIVO.test(t), `ruta de archivo visible en ${r}: ${t.match(RUTA_ARCHIVO)?.[0]}`);
    afirmar(!CODIGO.test(t), `código técnico visible en ${r}: ${t.match(CODIGO)?.[0]}`);
  }
  await ir("simular"); await p.click('[data-paso="precios"]'); await p.click("[data-simular]");
  await p.waitForSelector("[data-resultado-simple]", LARGO);
  const t = await textoVisible("[data-resultado-simple]");
  afirmar(!CODIGO.test(t), "código técnico visible en el resultado simple: " + t.match(CODIGO)?.[0]);
  afirmar(await p.locator("[data-resultado-simple] .codigo-tecnico").count() > 0, "el código técnico debe quedar como dato secundario");
});

await flujo("ESTADOS VACÍOS con explicación y acción", async () => {
  await ir("inicio"); await p.click("[data-escenario-vacio]"); await p.waitForSelector("[data-continuar]");
  afirmar(await p.locator("[data-vacio-simular] [data-cta]").count() === 1, "simular sin resultado: falta explicación/acción");
  afirmar((await p.locator("[data-vacio-simular]").innerText()).includes("Todavía no simulaste ningún escenario"), "texto del estado vacío");
  for (const r of ["comparar", "riesgos"]) { await ir(r); await vista(r); afirmar(await p.locator("[data-vacio] [data-cta]").count() >= 1, "estado vacío sin acción en " + r); }
  await ir("validacion"); await p.waitForSelector("[data-vacio] [data-cta]", LARGO);
});

await flujo("ESTUDIO COMPLETO lista todos los módulos", async () => {
  await ir("estudio"); await p.waitForSelector("[data-estudio-completo]");
  const temas = (await p.locator("[data-tema]").allInnerTexts()).join(" ").toLowerCase();
  for (const t of ["mercado", "demanda", "producción", "balance", "productos", "subproductos", "proceso", "maquinaria", "agua", "efluentes", "energía", "frío",
    "normativa", "exportación", "localización", "logística", "layout", "rrhh", "incubación", "alimento", "capex", "opex", "capital de trabajo", "finanzas", "riesgos", "optimizador"])
    afirmar(temas.includes(t), "falta en ESTUDIO COMPLETO: " + t);
  await ir("como-funciona"); await p.waitForSelector("[data-cadena]");
  await p.click("[data-eslabon='alimento']");
  afirmar((await p.getAttribute("[data-detalle-eslabon]", "data-eslabon")) === "alimento", "el bloque de la cadena no responde al clic");
});

await flujo("RECORRIDO: primer uso ofrece el recorrido y la demo guiada se completa", async () => {
  const c2 = await browser.newContext({ viewport: { width: 1280, height: 860 } });
  const q = await c2.newPage();
  await q.goto(URL_APP);
  await q.waitForSelector("[data-primer-uso]");
  afirmar((await q.locator("[data-primer-uso]").innerText()).includes("¿QUERÉS UN RECORRIDO DE 2 MINUTOS?"), "texto del primer uso");
  await q.click("[data-ir-directo]");
  await q.reload(); await q.waitForSelector("[data-home]"); await q.waitForTimeout(400);
  afirmar(await q.locator("[data-primer-uso]").count() === 0, "la elección del primer uso no se guardó");
  await q.click("[data-abrir-demo]"); await q.waitForSelector("[data-guiarme]");
  await q.click("[data-guiarme]");
  for (let i = 0; i < 6; i++) { await q.waitForSelector("[data-tour-siguiente]"); await q.click("[data-tour-siguiente]"); await q.waitForTimeout(300); }
  await q.waitForSelector("[data-tour-fin]");
  afirmar(q.url().includes("#/validacion"), "el recorrido no terminó en validación");
  await q.click("[data-tour-cerrar]");
  await c2.close();
  const c3 = await browser.newContext(); const w = await c3.newPage();
  await w.goto(URL_APP); await w.waitForSelector("[data-empezar-recorrido]"); await w.click("[data-empezar-recorrido]");
  await w.waitForSelector("[data-tour-paso='escenario']"); await c3.close();
});

await browser.close();
let fallas = 0;
for (const [n, r, ms] of resultados) { console.log(`${r === "OK" ? "OK   " : "FALLA"} ${n} (${(ms / 1000).toFixed(1)} s)${r === "OK" ? "" : " — " + r}`); if (r !== "OK") fallas++; }
if (errores.length) { console.log("Errores de página:", errores.join(" | ")); fallas++; }
process.exit(fallas ? 1 : 0);
