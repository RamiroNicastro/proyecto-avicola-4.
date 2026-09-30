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
 *   V10-V20 auditoría semántica: ejemplo 10.000 aves/día al 50 %; utilización asumida vs requerida; cobertura
 *       operativa vs máxima; dos capacidades ociosas; rangos principales de escala y peso; escenario matemático;
 *       configuraciones sin A/B/C; «Calculado por modelo»; demanda documentada ≈ 0; umbrales ilustrativos
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
chk("V03 port de aves_por_mix + comparar_demanda = Python en " + data.casos_prueba.demanda.length + " casos (M0-M3, pesos 2,0-3,8 kg, tres configuraciones comerciales)",
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

// ================================================================================================
// AUDITORÍA SEMÁNTICA v0.1 (V10-V20): definiciones inequívocas para usuarios no técnicos
// ================================================================================================
const calc = (o) => S.calcular(data, Object.assign(S.entradasPorDefecto(data), o));
const idsAl = (r) => r.alertas.map((a) => a.id);

// V10 — ejemplo obligatorio: 10.000 aves/día, 50 %, demanda que requiere 8.000 aves/día operativo
{
  const k = S.kgPorAve(data, "B", 2.9);
  const D = 8000 * 250 / 365 * k.comestible;                     // kg/día calendario que requieren 8.000 aves/día op. (M0)
  const r = calc({ escala: 10000, utilizacion: 0.5, demanda_id: "MANUAL", demanda_manual_kg: D, metodo: "M0" });
  const s = r.demanda.sel;
  const ok = r.ok && cerca(r.capacidad.aves_procesadas_dia_op, 5000) && cerca(s.aves_necesarias_dia_operativo, 8000)
    && cerca(s.factor_demanda_capacidad, 0.8) && cerca(s.utilizacion_requerida_por_demanda, 0.8)
    && cerca(s.cobertura_maxima_plena_capacidad, 1) && cerca(s.cobertura_operativa, 0.625)
    && cerca(s.kg_no_atendidos_operativo_dia_cal, D * 0.375) && s.kg_no_atendidos_dia_cal < 1e-6
    && cerca(r.capacidad.capacidad_ociosa_operativa, 5000) && cerca(s.capacidad_disponible_respecto_demanda, 2000)
    && idsAl(r).includes("UOP") && !idsAl(r).includes("AL3") && /aunque la capacidad instalada alcanzaría/.test(r.alertas.find((a) => a.id === "UOP").texto);
  chk("V10 ejemplo 10.000 aves/día al 50 % con demanda de 8.000: factor 80 %, utilización requerida 80 %, cobertura operativa 62,5 %, " +
    "cobertura máxima 100 %, ociosa operativa 5.000, disponible respecto de la demanda 2.000 y alerta UOP", ok,
    `cobertura operativa ${s.cobertura_operativa}; máxima ${s.cobertura_maxima_plena_capacidad}; alertas ${idsAl(r).join(",")}`);
}

// V11-V13 — invariantes semánticas en escenarios aleatorios
let m11 = [], m12 = [], m13 = [], difieren = 0, ociosasDistintas = 0;
for (let i = 0; i < 3000; i++) {
  const e = aleatorio();
  const r = S.calcular(data, e);
  if (!r.ok) continue;
  const E = e.escala, u = e.utilizacion, sim = E * u;
  // V11: utilización elegida (entrada) ≠ utilización requerida (modelo): cambiar una no cambia la otra
  const r2 = S.calcular(data, Object.assign({}, e, { utilizacion: u > 0.5 ? u - 0.3 : u + 0.3 }));
  if (!cerca(r2.demanda.sel.utilizacion_requerida_por_demanda, r.demanda.sel.utilizacion_requerida_por_demanda)) m11.push(i);
  const r3 = S.calcular(data, Object.assign({}, e, { demanda_id: "MANUAL", demanda_manual_kg: (e.demanda_manual_kg || 1000) * 2 + 500 }));
  if (!cerca(r3.capacidad.aves_procesadas_dia_op, sim) || r3.entradas.utilizacion !== u) m11.push("d" + i);
  Object.values(r.demanda.metodos).forEach((x) => {
    const n = x.aves_necesarias_dia_operativo;
    if (Math.abs(x.utilizacion_requerida_por_demanda - u) > 1e-6) difieren++;
    // V12: cobertura operativa usa la producción simulada; la máxima, la capacidad instalada (= modelo)
    if (r.demanda.D > 0) {
      if (!cerca(x.cobertura_operativa, Math.min(1, sim / n))) m12.push(`op${i}`);
      if (!cerca(x.cobertura_maxima_plena_capacidad, Math.min(1, E / n)) || x.cobertura_maxima_plena_capacidad !== x.cobertura_demanda) m12.push(`max${i}`);
      if (x.cobertura_operativa > x.cobertura_maxima_plena_capacidad + 1e-12 || x.cobertura_operativa > 1 + 1e-12) m12.push(`ord${i}`);
      if (!cerca(x.kg_no_atendidos_operativo_dia_cal, r.demanda.D * (1 - x.cobertura_operativa))) m12.push(`kg${i}`);
    }
    // V13: capacidad ociosa operativa (instalada − simulada) ≠ disponible respecto de la demanda (instalada − requerida)
    if (!cerca(x.capacidad_disponible_respecto_demanda, Math.max(0, E - n), 1e-9, 1e-6)) m13.push(`disp${i}`);
    if (Math.abs(r.capacidad.capacidad_ociosa_operativa - x.capacidad_disponible_respecto_demanda) > 1) ociosasDistintas++;
  });
  if (!cerca(r.capacidad.capacidad_ociosa_operativa, E - sim)) m13.push(`oper${i}`);
}
chk("V11 utilización operativa asumida (entrada) y utilización requerida por demanda (modelo) son variables distintas e independientes",
  !m11.length && difieren > 1000, `${difieren} casos en que difieren; fallas ${m11.slice(0, 5)}`);
chk("V12 cobertura operativa = mín(producción simulada ÷ capacidad requerida; 100 %); cobertura máxima = mín(capacidad instalada ÷ requerida; 100 %) = modelo; operativa ≤ máxima",
  !m12.length, m12.slice(0, 5).join(" "));
chk("V13 capacidad ociosa operativa (instalada − simulada) y capacidad disponible respecto de la demanda (instalada − requerida) no se confunden",
  !m13.length && ociosasDistintas > 1000, `${ociosasDistintas} casos con valores distintos; fallas ${m13.slice(0, 5)}`);

// V14 — escala fuera del rango principal estudiado 2.500–20.000
{
  const casos = [[500, true], [2499, true], [2500, false], [7777, false], [20000, false], [20001, true], [30000, true]];
  const mal = casos.filter(([E, alerta]) => { const r = calc({ escala: E }); return !r.ok || idsAl(r).includes("RANGO_E") !== alerta || r.fuera_rango.escala !== alerta; });
  const t = calc({ escala: 1000 }).alertas.find((a) => a.id === "RANGO_E");
  chk("V14 escalas fuera de 2.500–20.000 generan «ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO» (extrapolación), sin bloquear; dentro del rango, no",
    !mal.length && t.titulo === "ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO" && /extrapolación física/.test(t.texto), mal.map((x) => x[0]).join(", "));
}
// V15 — peso fuera del rango principal 2,2–3,5 kg
{
  const casos = [[2.0, true], [2.1, true], [2.2, false], [2.9, false], [3.5, false], [3.6, true], [3.8, true]];
  const mal = casos.filter(([p, alerta]) => { const r = calc({ peso: p }); return !r.ok || idsAl(r).includes("RANGO_P") !== alerta; });
  const t = calc({ peso: 3.7 }).alertas.find((a) => a.id === "RANGO_P");
  chk("V15 pesos fuera de 2,2–3,5 kg generan advertencia de extrapolación, sin bloquear; el motor admite 2,0–3,8 kg",
    !mal.length && /Peso fuera del rango principal utilizado en el estudio; resultados deben tratarse como extrapolación/.test(t.texto.replace(/ \([^)]*\)/, "")), mal.map((x) => x[0]).join(", "));
}
// V16 — coherencia peso–edad–FCR: escenario matemático, sin relación automática
{
  const pr = P.produccion.perfiles, dm = P.produccion.desempenos.medio;
  const coherentes = [{}].concat(Object.values(pr).map((p) => ({ peso: p.peso, edad: p.edad, fcr: +(p.fcr_base + dm.d_fcr).toFixed(2) })));
  const incoherentes = [{ peso: 3.4, edad: 38 }, { fcr: 2.1 }, { peso: 2.2, edad: 56 }, { peso: 3.4, edad: 54, fcr: 1.5 }];
  const malC = coherentes.filter((o) => { const r = calc(o); return r.escenario_matematico || idsAl(r).includes("MAT"); });
  const malI = incoherentes.filter((o) => { const r = calc(o); return !r.ok || !r.escenario_matematico || !idsAl(r).includes("MAT"); });
  const r = calc({ peso: 3.4, edad: 38 });
  const sinAuto = r.entradas.fcr === S.entradasPorDefecto(data).fcr && r.entradas.edad === 38;   // no corrige las entradas
  chk("V16 combinación peso–edad–FCR incoherente: cálculo mantenido, alerta «Escenario matemático… requiere validación zootécnica», entradas sin corregir; perfiles del estudio sin alerta",
    !malC.length && !malI.length && sinAuto && /Escenario matemático\. La combinación peso–edad–FCR requiere validación zootécnica/.test(r.alertas.find((a) => a.id === "MAT").texto),
    `coherentes con alerta ${malC.length}; incoherentes sin alerta ${malI.length}`);
}
// V17 — configuraciones comerciales sin etiquetas A/B/C (reservadas a los escenarios del comparador)
{
  const app = fs.readFileSync(path.join(AQUI, "app.js"), "utf8");
  const mNom = app.match(/const NOMBRE_CONFIG = \{([^}]*)\}/);
  const nombres = mNom ? [...mNom[1].matchAll(/:\s*"([^"]+)"/g)].map((x) => x[1]) : [];
  const exp = calc({}).exportacion.map((x) => x.etiqueta);
  const prohibidos = [/"[ABC] · /, /config\. [ABC]\b/, /configuración \$\{e\.config\}/, /\(clase [ABCDP]\)/, /clase [ABC]\b/, /\((?:A|B)\)"/];
  const hallados = prohibidos.filter((re) => re.test(app)).map(String);
  const ok = nombres.length === 3 && nombres.every((n) => !/\b[ABC]\b/.test(n)) && nombres.join("|") === "Pollo entero|Trozado|Deshuesado / mayor procesamiento"
    && exp.every((t) => !/\b(config|clase) [ABC]\b/.test(t)) && !hallados.length && /chips\("config", \[\["A", NOMBRE_CONFIG\.A\]/.test(app);
  chk("V17 configuraciones comerciales = «Pollo entero», «Trozado», «Deshuesado / mayor procesamiento»; A/B/C reservadas al comparador", ok,
    `nombres: ${nombres.join(" | ")}; patrones prohibidos: ${hallados.join(" ")}`);
}
// V18 — «Calculado por modelo» (no «validado»)
{
  const txt = ["app.js", "index.html", "calculo.js"].map((a) => fs.readFileSync(path.join(AQUI, a), "utf8")).join("\n");
  const ok = /corto: "Calculado por modelo"/.test(txt) && !/validado por modelo|validado emp[ií]ricamente|validación empírica/i.test(txt)
    && /Calculado por modelo significa que la fórmula y su consistencia matemática fueron verificadas\. No significa que el valor haya sido validado en una planta real\./.test(txt);
  chk("V18 etiqueta «Calculado por modelo» con su aclaración; no aparece «validado por modelo» ni «validado empíricamente»", ok);
}
// V19 — demanda documentada ≈ 0 + utilización alta
{
  const r100 = calc({ demanda_id: "CERO", utilizacion: 1 }), r30 = calc({ demanda_id: "CERO", utilizacion: 0.3 }), rB = calc({ demanda_id: "ESC-BAS", utilizacion: 1 });
  const a = r100.alertas.find((x) => x.id === "DOC0");
  const ok = r100.ok && a && /Este escenario simula producción al 100 %, pero actualmente no existe demanda documentada que respalde ese nivel de operación\./.test(a.texto)
    && idsAl(r30).includes("DOC0") && !idsAl(rB).includes("DOC0") && /no validada \/ prácticamente nula/i.test(r100.demanda.escenario.categoria);
  chk("V19 «solo demanda documentada» + 100 % de utilización genera alerta explicativa sin bloquear; categoría «no validada / prácticamente nula»", ok);
}
// V20 — umbrales de interfaz marcados como ilustrativos
{
  const r = calc({ utilizacion: 0.3, dias_inventario: 10 });
  const il = r.alertas.filter((a) => ["UB1", "INV1"].includes(a.id));
  const ok = il.length === 2 && il.every((a) => a.ilustrativo && /Umbral visual ilustrativo/.test(a.ref))
    && /Umbral visual ilustrativo: umbral de interfaz, pendiente de calibración económica y operativa\./.test(S.TXT_ILUSTRATIVO);
  chk("V20 alertas de utilización baja e inventario alto marcadas como «umbral visual ilustrativo», pendiente de calibración económica y operativa", ok);
}

// ------------------------------------------------------------------------------------------------
console.log(`\nVALIDACIÓN — simulador HTML v${data.meta.simulador_version} (modelos: escala ${data.meta.versiones_modelos.escala}, ` +
  `producción ${data.meta.versiones_modelos.produccion}, balance ${data.meta.versiones_modelos.balance}, subproductos ${data.meta.versiones_modelos.subproductos})`);
resultados.forEach(([nom, ok, det]) => console.log(`  [${ok ? "OK " : "FALLA"}] ${nom}${det ? `\n      ${det}` : ""}`));
const bien = resultados.filter((r) => r[1]).length;
console.log(`  Resultado: ${bien}/${resultados.length} correctos\n`);
process.exit(bien === resultados.length ? 0 : 1);
