#!/usr/bin/env node
/*
 * VALIDACIÓN DEL SIMULADOR HTML v0.1
 *   node 23_plan_expansion/simulador_html/validar_simulador.js
 *
 * Comprueba que el motor calculo.js reproduce los modelos aprobados:
 *   V01 cada fila numérica de escenarios_escala.csv (4 escalas × 2 calendarios, todos los bloques)
 *   V02 casos de producción primaria calculados en Python (parámetros aleatorios, mp.calcular)
 *   V03 casos de demanda vs capacidad calculados en Python (M0-M3, pesos y configuraciones aleatorias)
 *   V04 invariantes en 4.000 escenarios aleatorios: sin NaN, sin negativos, utilización y cobertura ≤ 100 %
 *   V05 entradas fuera de rango bloquean el cálculo
 *   V06 escenarios A/B/C independientes; cambiar la escala cambia los resultados
 *   V07 datos embebidos (.js) = JSON; referencia de tabla central = CSV
 *   V08 funcionamiento offline: sin URLs externas, sin fetch/XMLHttpRequest/import dinámico
 *   V09 sin cifras económicas inventadas (CAPEX, OPEX, ingresos, EBITDA, VAN, TIR, payback) en los resultados
 * Sale con código 1 si alguna verificación falla. Solo usa Node (sin dependencias).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const S = require("./calculo.js");

const AQUI = __dirname;
const RAIZ = path.resolve(AQUI, "..", "..");
const data = JSON.parse(fs.readFileSync(path.join(AQUI, "data", "simulador_data.json"), "utf8"));
const P = data.parametros;
const resultados = [];
const chk = (nombre, ok, det) => resultados.push([nombre, !!ok, det || ""]);
const cerca = (a, b, rel = 1e-9, abs = 1e-6) => Math.abs(a - b) <= Math.max(abs, rel * Math.max(Math.abs(a), Math.abs(b)));

// ------------------------------------------------------------------------------------------------
function leerCSV(ruta) {
  const txt = fs.readFileSync(ruta, "utf8").replace(/\r/g, "");
  const filas = [];
  let campo = "", fila = [], q = false;
  for (let i = 0; i < txt.length; i++) {
    const c = txt[i];
    if (q) {
      if (c === '"' && txt[i + 1] === '"') { campo += '"'; i++; } else if (c === '"') q = false; else campo += c;
    } else if (c === '"') q = true;
    else if (c === ",") { fila.push(campo); campo = ""; }
    else if (c === "\n") { fila.push(campo); filas.push(fila); fila = []; campo = ""; }
    else campo += c;
  }
  if (campo || fila.length) { fila.push(campo); filas.push(fila); }
  const cab = filas.shift();
  return filas.filter((f) => f.length === cab.length).map((f) => Object.fromEntries(cab.map((c, i) => [c, f[i]])));
}
const param = (s) => Object.fromEntries(s.split(";").map((x) => x.trim()).filter((x) => x.includes("=")).map((x) => x.split("=")));

// Mapeo variable del CSV (bloque produccion_primaria) -> clave de mp.calcular (modelo_escala.VARS_PRODUCCION)
const VARS_PROD = {
  pollitos_bb_semana_plena: "pollitos_alojados_semana_plena", pollitos_bb_semana_promedio: "pollitos_alojados_semana_promedio",
  pollitos_bb_anio: "pollitos_alojados_anio", aves_cargadas_dia_operativo: "aves_cargadas_dia", aves_cargadas_anio: "aves_cargadas_anio",
  aves_faenadas_semana_plena: "aves_faenadas_semana_plena", aves_faenadas_anio: "aves_faenadas_anio",
  plazas_simultaneas_granja: "capacidad_alojamiento_pollitos", m2_galpones: "m2_galpon",
  galpones_equivalentes_1200m2: "galpones_1200m2", galpones_equivalentes_2400m2: "galpones_2400m2",
  alimento_t_semana_plena: "alimento_t_semana_plena", alimento_t_semana_promedio: "alimento_t_semana_promedio",
  alimento_t_anio: "alimento_t_anio", alimento_un_ciclo_de_crianza_t: "alimento_ciclo_crianza_t",
  agua_bebida_m3_semana_plena: "agua_bebida_m3_semana_plena", agua_bebida_m3_anio: "agua_bebida_m3_anio",
  agua_bebida_m3_dia_calendario_promedio: "agua_bebida_m3_dia_promedio",
  aves_vivas_simultaneas_ritmo_pleno: "inventario_aves_ritmo_pleno", aves_vivas_simultaneas_promedio_anual: "inventario_aves_promedio_anual",
};

const cache = new Map();
function run(E, ds, over) {
  const e = Object.assign(S.entradasPorDefecto(data), { escala: E, dias_semana: ds, dias_anio: P.calendarios[String(ds)], utilizacion: 1 }, over || {});
  const key = JSON.stringify(e);
  if (!cache.has(key)) {
    const r = S.calcular(data, e);
    if (!r.ok) throw new Error("Cálculo bloqueado: " + r.errores.join(" | "));
    cache.set(key, r);
  }
  return cache.get(key);
}

function valorSimulador(f) {
  const E = +f.escala_aves_dia, ds = +f.dias_semana, pr = param(f.parametro), v = f.variable, per = f.periodo;
  const base = run(E, ds);
  switch (f.bloque) {
    case "capacidad":
      return { escala_aves_faenadas_dia_operativo: base.capacidad.escala, aves_faenadas_anio_plena_escala: base.capacidad.aves_anio_plena_escala,
        aves_faenadas_dia_calendario_equivalente: base.capacidad.aves_dia_cal_equivalente }[v];
    case "ritmo_linea": {
      const r = run(E, ds, { horas_netas: +pr.horas_netas });
      return v === "aves_por_hora_neta" ? r.capacidad.ritmo_aves_h : r.capacidad.ritmo_kg_vivo_h;
    }
    case "produccion_primaria": return base.produccion[VARS_PROD[v]];
    case "abastecimiento":
      if (v === "productores_necesarios") return null;              // celda vacía: DPV-048
      return base.abastecimiento.productores_ilustrativos.find((x) => x.galpones_2400 === +pr.galpones_por_productor).productores;
    case "utilizacion": {
      const r = run(E, ds, { utilizacion: +pr.utilizacion });
      const m = { aves_faenadas_dia_operativo: r.capacidad.aves_procesadas_dia_op, aves_faenadas_anio: r.capacidad.aves_anio,
        t_vivas_anio: r.central.t_vivas_anio, pollitos_bb_anio: r.produccion.pollitos_alojados_anio, alimento_t_anio: r.produccion.alimento_t_anio };
      if (v in m) return m[v];
      const c = v.replace(/_t_anio$/, "");
      return (r.agregados[c] || r.items.find((i) => i.clave === c)).t_anio;
    }
    case "balance_productos": {
      if (v === "entrada_pollo_vivo_t") return base.agregados.peso_vivo.t_dia_op;
      if (v === "entrada_agua_incorporada_t") return base.agregados.agua_incorporada.t_dia_op;
      const it = base.items.find((i) => i.clave === v.replace(/_t$/, ""));
      return per === "anio" ? it.t_anio : it.t_dia_op;
    }
    case "masa_comestible": {
      const n = { comestible_bio_t: "biologica", agua_retenida_comestible_t: "agua", comestible_t: "comercial",
        producto_principal_bio_t: "principal_biologica", producto_principal_t: "principal_comercial" }[v];
      return base.masa[n][{ dia_operativo: "t_dia_op", dia_calendario: "t_dia_cal", anio: "t_anio" }[per]];
    }
    case "configuraciones": return base.configuraciones[pr.config][v];
    case "subproductos": {
      const c = v.replace(/_t$/, "");
      return (base.subproductos[c] || { t_dia_op: base.items.find((i) => i.clave === c).t_dia_op }).t_dia_op;
    }
    case "inventario": {
      const dias = +pr.dias;
      const r = run(E, ds, { dias_inventario: dias, dias_congelado: dias, perfil_destino: pr.perfil_destino || "P1", base_inventario: pr.base_temporal });
      if (v === "subproductos_perecederos_frio_t") return r.inventario.subproductos_frio_t;
      return r.inventario.por_base[pr.base_temporal][v];
    }
    case "logistica":
      if (v === "camiones_aves_vivas_dia") return base.logistica.camiones_aves_vivas_rango[P.aves_por_camion_vivo.indexOf(+pr.aves_por_camion)];
      return base.logistica[v];
    case "exportacion": {
      const m = v.match(/^(dias_para_contenedor|contenedores_mes_si_100pct)_(.+)$/);
      return base.exportacion.find((x) => x.clave === m[2])[m[1]];
    }
    case "demanda_capacidad": {
      if (v === "utilizacion_con_demanda_documentada_A_mas_B") return data.demanda.demanda_documentada_A_mas_B_kg_dia;
      const r = run(E, ds, { demanda_id: pr.escenario, metodo: pr.metodo.slice(0, 2) });
      const s = r.demanda.sel;
      if (["factor_demanda_capacidad", "utilizacion_planta", "cobertura_demanda"].includes(v)) return 100 * s[v];
      const m = { demanda_kg_producto_dia_calendario: r.demanda.D, aves_necesarias_dia_calendario: s.res.aves_dia_cal,
        excedente_partes_kg_dia_cal: s.res.excedente_total, demanda_fuera_del_balance_kg_dia_cal: s.res.fuera_balance };
      return v in m ? m[v] : s[v];
    }
    case "tabla_central": return base.central[v];
    default: return undefined;
  }
}

// V01 — CSV maestro ---------------------------------------------------------------------------
const csv = leerCSV(path.join(RAIZ, "23_plan_expansion", "escenarios_escala.csv"));
let n = 0, malos = [], vacias = 0;
const porBloque = {};
csv.forEach((f) => {
  if (f.valor === "") { vacias++; return; }
  const esperado = parseFloat(f.valor);
  let obtenido;
  try { obtenido = valorSimulador(f); } catch (err) { obtenido = "ERROR " + err.message; }
  n++;
  porBloque[f.bloque] = (porBloque[f.bloque] || 0) + 1;
  if (typeof obtenido !== "number" || !cerca(obtenido, esperado)) malos.push(`${f.bloque}/${f.variable}/${f.escala_aves_dia}/${f.dias_semana}/${f.parametro}: CSV ${esperado} vs HTML ${obtenido}`);
});
chk("V01 el simulador reproduce cada fila numérica de escenarios_escala.csv (4 escalas × 2 calendarios)",
  malos.length === 0 && n === csv.length - vacias,
  `${n} valores comparados (${Object.entries(porBloque).map(([b, c]) => `${b} ${c}`).join(", ")}); ${vacias} celdas vacías (DPV-048); ${malos.length} diferencias` +
  (malos.length ? "\n      " + malos.slice(0, 8).join("\n      ") : ""));

// V02 — producción (Python) ---------------------------------------------------------------------
malos = [];
data.casos_prueba.produccion.forEach((c, i) => {
  const e = c.entrada;
  const r = S.produccion(P, e.aves, e.dias_semana, e.dias_anio, { edad: e.edad, peso: e.peso, fcr: e.fcr, mort: e.mort, doa: e.doa, vacio: e.vacio, kg_m2: e.kg_m2 });
  Object.keys(c.salida).forEach((k) => { if (!cerca(r[k], c.salida[k], 1e-12, 1e-9)) malos.push(`caso ${i} ${k}: ${c.salida[k]} vs ${r[k]}`); });
  if (Object.keys(r).length !== Object.keys(c.salida).length) malos.push(`caso ${i}: claves distintas`);
});
chk("V02 port de mp.calcular = Python en " + data.casos_prueba.produccion.length + " casos (37 variables, tolerancia relativa 1e-12)",
  malos.length === 0, malos.slice(0, 5).join("; "));

// V03 — demanda vs capacidad (Python) ----------------------------------------------------------
malos = [];
data.casos_prueba.demanda.forEach((c, i) => {
  const e = c.entrada;
  const k = S.kgPorAve(data, e.config, e.peso);
  const res = e.metodo === "M0" ? S.resultadoM0(e.demanda_kg_dia_cal, k)
    : S.avesPorMix(e.demanda_kg_dia_cal, data.demanda.mixes[e.metodo], data.rendimientos_mix[S.clavePeso(e.peso)], data.demanda.factor_milanesa, data.demanda.rol_mix);
  const cmp = Object.assign(S.compararDemanda(e.escala, e.dias_anio, e.demanda_kg_dia_cal, res),
    { aves_dia_cal: res.aves_dia_cal, excedente_total: res.excedente_total, limitante: res.limitante, fuera_balance: res.fuera_balance });
  Object.keys(c.salida).forEach((kk) => {
    const a = c.salida[kk], b = cmp[kk];
    if (typeof a === "string" ? a !== b : !cerca(a, b, 1e-12, 1e-9)) malos.push(`caso ${i} ${kk}: ${a} vs ${b}`);
  });
});
chk("V03 port de aves_por_mix + comparar_demanda = Python en " + data.casos_prueba.demanda.length + " casos (M0-M3, pesos 2,0-3,8 kg, configuraciones A/B/C)",
  malos.length === 0, malos.slice(0, 5).join("; "));

// V04 — invariantes en escenarios aleatorios ------------------------------------------------------
function azar(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
const rnd = azar(20260930);
const pick = (a) => a[Math.floor(rnd() * a.length)];
const ids = data.demanda.escenarios.map((d) => d.id).concat(["MANUAL", "CERO"]);
function aleatorio() {
  const ds = pick([5, 6]);
  return Object.assign(S.entradasPorDefecto(data), {
    escala: Math.round(500 + rnd() * 29500), dias_semana: ds, dias_anio: Math.round(150 + rnd() * (ds * P.semanas_anio - 151)),
    horas_netas: 4 + Math.round(rnd() * 16), peso: +(2 + Math.round(rnd() * 18) / 10).toFixed(1), edad: 35 + Math.round(rnd() * 21),
    mortalidad: rnd() * 0.15, fcr: 1.4 + rnd() * 0.8, doa: rnd() * 0.02, vacio: 8 + Math.round(rnd() * 22), kg_m2: 25 + rnd() * 20,
    utilizacion: 0.1 + rnd() * 0.9, demanda_id: pick(ids), demanda_manual_kg: rnd() * 80000, metodo: pick(["M0", "M1", "M2", "M3"]),
    config: pick(["A", "B", "C"]), dias_inventario: 1 + Math.round(rnd() * 29), dias_congelado: 1 + Math.round(rnd() * 29),
    base_inventario: pick(["dias_produccion", "dias_calendario"]), perfil_destino: pick(["P1", "P2", "P3"]), pct_propio: rnd(),
    m2_por_productor: pick([null, 2400, 5000]), aves_por_camion: pick([null, 4000, 6500]), cap_camion_frio_t: pick([null, 10]),
    cap_camion_alimento_t: pick([null, 28]), cap_camion_sub_t: pick([null, 12]),
  });
}
let nNum = 0, nan = [], neg = [], sobre100 = [], bloq = 0;
function recorrer(o, ruta) {
  if (typeof o === "number") {
    nNum++;
    if (!Number.isFinite(o)) nan.push(ruta);
    else if (o < -1e-6) neg.push(`${ruta}=${o}`);
  } else if (o && typeof o === "object") Object.keys(o).forEach((k) => recorrer(o[k], `${ruta}.${k}`));
}
for (let i = 0; i < 4000; i++) {
  const e = aleatorio();
  const r = S.calcular(data, e);
  if (!r.ok) { bloq++; continue; }
  const { alertas, entradas, ...res } = r;
  recorrer(res, "r");
  Object.values(r.demanda.metodos).forEach((m) => {
    if (m.utilizacion_planta > 1 + 1e-12 || m.cobertura_demanda > 1 + 1e-12 || m.utilizacion_planta < 0) sobre100.push(i);
    if (m.factor_demanda_capacidad > 1 + 1e-9 && !(m.kg_no_atendidos_dia_cal > 0 && m.capacidad_ociosa_aves_dia_operativo < 1e-6)) sobre100.push("AL3-" + i);
    if (m.factor_demanda_capacidad < 1 - 1e-9 && !(m.capacidad_ociosa_aves_dia_operativo > 0 && m.kg_no_atendidos_dia_cal < 1e-6)) sobre100.push("oc-" + i);
  });
  if (r.capacidad.utilizacion > 1) sobre100.push("u-" + i);
}
chk("V04 4.000 escenarios aleatorios: sin NaN/Infinito, sin negativos, utilización y cobertura ≤ 100 %, demanda no atendida ⇔ factor > 100 %",
  bloq === 0 && !nan.length && !neg.length && !sobre100.length,
  `${nNum} valores; ${bloq} bloqueados; NaN ${nan.length} ${nan.slice(0, 3)}; negativos ${neg.length} ${neg.slice(0, 3)}; métricas fuera de rango ${sobre100.length}`);

// V05 — entradas incompatibles bloquean ------------------------------------------------------------
const base = S.entradasPorDefecto(data);
const invalidas = [{ peso: 4.0 }, { peso: 1.9 }, { peso: 2.95 }, { dias_semana: 5, dias_anio: 300 }, { dias_semana: 7 }, { utilizacion: 1.2 },
  { utilizacion: 0 }, { escala: 100 }, { escala: 50000 }, { horas_netas: 24 }, { mortalidad: 0.3 }, { fcr: 3 }, { config: "Z" },
  { demanda_id: "MANUAL", demanda_manual_kg: -5 }, { m2_por_productor: -1 }, { escala: NaN }];
const noBloq = invalidas.filter((o) => S.calcular(data, Object.assign({}, base, o)).ok).map((o) => JSON.stringify(o));
chk("V05 entradas incompatibles o fuera de rango bloquean el cálculo (" + invalidas.length + " casos)", noBloq.length === 0, noBloq.join(" "));

// V06 — A/B/C independientes; la escala actualiza los resultados -------------------------------------
let est = S.estadoInicial(data);
const antes = JSON.stringify(est.escenarios.B) + JSON.stringify(est.escenarios.C);
const rB0 = JSON.stringify(S.calcular(data, est.escenarios.B).central);
est = S.conEntrada(est, "A", "escala", 2500);
est = S.conEntrada(est, "A", "peso", 3.4);
est = S.conEntrada(est, "A", "config", "C");
let ok6 = JSON.stringify(est.escenarios.B) + JSON.stringify(est.escenarios.C) === antes;
ok6 = ok6 && JSON.stringify(S.calcular(data, est.escenarios.B).central) === rB0 && est.escenarios.A.escala === 2500;
const copia = S.copiarEscenario(est, "A", "C");
copia.escenarios.C.escala = 7777;
ok6 = ok6 && copia.escenarios.A.escala === 2500 && est.escenarios.C.escala === 20000 && copia.escenarios.C.nombre === "Escenario C";
const r5 = S.calcular(data, Object.assign({}, base, { escala: 5000 })), r10 = S.calcular(data, Object.assign({}, base, { escala: 10000 }));
ok6 = ok6 && cerca(r10.central.aves_anio, 2 * r5.central.aves_anio) && cerca(r10.central.m2_galpones, 2 * r5.central.m2_galpones)
  && r10.demanda.sel.factor_demanda_capacidad < r5.demanda.sel.factor_demanda_capacidad;
const pre = { A: 5000, B: 10000, C: 20000 };
ok6 = ok6 && S.SLOTS.every((s) => S.estadoInicial(data).escenarios[s].escala === pre[s]);
chk("V06 escenarios A/B/C guardan entradas independientes (editar A no cambia B ni C; copiar no comparte referencias); cambiar la escala actualiza los resultados", ok6);

// V07 — datos embebidos y referencia ------------------------------------------------------------------
const js = fs.readFileSync(path.join(AQUI, "data", "simulador_data.js"), "utf8");
const m = js.match(/window\.SIMULADOR_DATA = (\{[\s\S]*\});\s*$/);
let ok7 = !!m && JSON.stringify(JSON.parse(m[1])) === JSON.stringify(data);
const refCSV = csv.filter((f) => f.bloque === "tabla_central");
ok7 = ok7 && refCSV.length === data.referencia_tabla_central.length
  && data.referencia_tabla_central.every((x, i) => cerca(x.valor, +refCSV[i].valor, 0, 0) && x.variable === refCSV[i].variable);
ok7 = ok7 && data.referencia_tabla_central.every((x) => {
  const r = run(x.escala, x.dias_semana);
  return cerca(r.central[x.variable], x.valor);
});
chk("V07 simulador_data.js = simulador_data.json; referencia embebida = bloque tabla_central del CSV y reproducida por el motor", ok7,
  `${data.referencia_tabla_central.length} valores de referencia`);

// V08 — offline --------------------------------------------------------------------------------------
const archivos = ["index.html", "app.js", "styles.css", "calculo.js"];
const problemas = [];
archivos.forEach((a) => {
  const t = fs.readFileSync(path.join(AQUI, a), "utf8");
  if (/https?:\/\//i.test(t)) problemas.push(`${a}: URL externa`);
  if (/\bfetch\s*\(|XMLHttpRequest|\bimport\s*\(|@import|WebSocket|EventSource/.test(t)) problemas.push(`${a}: acceso de red`);
});
const html = fs.readFileSync(path.join(AQUI, "index.html"), "utf8");
const srcs = [...html.matchAll(/(?:src|href)="([^"]+)"/g)].map((x) => x[1]).filter((s) => !s.startsWith("#"));
srcs.forEach((s) => { if (!fs.existsSync(path.join(AQUI, s))) problemas.push(`index.html referencia inexistente: ${s}`); });
chk("V08 funciona offline: sin URLs externas, sin fetch/XMLHttpRequest/import dinámico; todos los recursos son archivos locales",
  problemas.length === 0, `${srcs.length} recursos locales: ${srcs.join(", ")}` + (problemas.length ? " | " + problemas.join("; ") : ""));

// V09 — sin cifras económicas en los resultados ------------------------------------------------------
const claves = new Set();
(function col(o) { if (o && typeof o === "object") Object.keys(o).forEach((k) => { claves.add(k); col(o[k]); }); })(S.calcular(data, base));
const econ = [...claves].filter((k) => /\b(usd|ars|precio|costo|capex|opex|ebitda|van|tir|payback|margen|ingresos?)\b/i.test(k.replace(/_/g, " ")));
chk("V09 los resultados no contienen variables económicas (CAPEX, OPEX, precios, ingresos, EBITDA, VAN, TIR, payback)", econ.length === 0, econ.join(", "));

// ------------------------------------------------------------------------------------------------
console.log(`\nVALIDACIÓN — simulador HTML v${data.meta.simulador_version} (modelos: escala ${data.meta.versiones_modelos.escala}, ` +
  `producción ${data.meta.versiones_modelos.produccion}, balance ${data.meta.versiones_modelos.balance}, subproductos ${data.meta.versiones_modelos.subproductos})`);
resultados.forEach(([nom, ok, det]) => console.log(`  [${ok ? "OK " : "FALLA"}] ${nom}${det ? `\n      ${det}` : ""}`));
const bien = resultados.filter((r) => r[1]).length;
console.log(`  Resultado: ${bien}/${resultados.length} correctos\n`);
process.exit(bien === resultados.length ? 0 : 1);
