/*
 * MOTOR DE CÁLCULO DEL SIMULADOR HTML v0.1 — funciones puras (sin DOM).
 * Se usa desde el navegador (window.SimCalculo) y desde Node (validar_simulador.js).
 *
 * Regla: el simulador NO reimplementa el balance de masa. Toma los kg por ave de cada ítem
 * (data.coeficientes[config][peso], exportados por generar_datos_simulador.py desde
 * modelo_escala.kg_por_ave) y aplica solo:
 *   (1) fórmulas lineales documentadas en 23_plan_expansion/modelo_escala.py
 *       (t/día operativo = kg/ave × aves / 1.000; t/año = t/día × días; conversión
 *        día operativo -> día calendario = × días operativos / 365; ritmo = aves / horas netas;
 *        inventario = flujo × días; productores = m² / m² por productor; camiones = t / capacidad);
 *   (2) un port 1:1 de mp.calcular (03_produccion_primaria v1.1), fórmulas cerradas, con el mismo
 *       escalado por días/año que modelo_escala.produccion;
 *   (3) un port 1:1 de modelo_escala.aves_por_mix y modelo_escala.comparar_demanda (SUP-054, SUP-060).
 * Los tres ports se verifican contra casos calculados en Python (data.casos_prueba) y contra
 * escenarios_escala.csv (validar_simulador.js). Unidades: aves, kg, t = 1.000 kg, m², m³, h.
 */
(function (raiz, fabrica) {
  if (typeof module === "object" && module.exports) module.exports = fabrica();
  else raiz.SimCalculo = fabrica();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  const DIAS_CAL = 365;

  // ---------------------------------------------------------------------------------------------
  // Rangos de entrada (especificacion_simulador_html.md §1). Fuera de rango = bloqueo (no se calcula).
  // ---------------------------------------------------------------------------------------------
  const RANGOS = {
    escala: [500, 30000, "Escala (aves/día operativo)"],
    utilizacion: [0.10, 1.0, "Utilización"],
    peso: [2.0, 3.8, "Peso vivo (kg)"],
    horas_netas: [4, 20, "Horas netas de faena"],
    edad: [35, 56, "Edad de faena (días)"],
    mortalidad: [0, 0.15, "Mortalidad en granja"],
    fcr: [1.4, 2.2, "FCR de campo"],
    doa: [0, 0.02, "Mortalidad en transporte (DOA)"],
    vacio: [8, 30, "Días entre lotes"],
    kg_m2: [25, 45, "Densidad final (kg/m²)"],
    dias_inventario: [1, 30, "Días de inventario"],
    dias_congelado: [1, 30, "Días de congelado y exportación"],
    pct_propio: [0, 1, "Proporción de granjas propias"],
  };

  // Rango PRINCIPAL ESTUDIADO (escalas de 23_plan_expansion y pesos del balance v1.1) vs rango
  // MATEMÁTICAMENTE SOPORTADO (RANGOS). Fuera del principal se calcula, pero como extrapolación.
  function rangoEstudiado(data) {
    const esc = data.parametros.escalas, pes = data.parametros.pesos_estudiados;
    return { escala: [Math.min(...esc), Math.max(...esc)], peso: [Math.min(...pes), Math.max(...pes)] };
  }

  function entradasPorDefecto(data, nombre) {
    const d = data.parametros.produccion.defaults;
    return {
      nombre: nombre || "Escenario",
      escala: 10000, dias_semana: 5, dias_anio: 250, horas_netas: 8,
      peso: data.parametros.peso_ref, edad: d.edad, mortalidad: d.mort, fcr: d.fcr,
      doa: d.doa, vacio: d.vacio, kg_m2: d.kg_m2,
      utilizacion: 0.70,
      demanda_id: "ESC-BAS", demanda_manual_kg: 7500, metodo: "M0",
      config: data.parametros.config_ref,
      dias_inventario: 3, base_inventario: "dias_produccion", dias_congelado: 14, perfil_destino: "P1",
      pct_propio: 0, m2_por_productor: null, aves_por_camion: null,
      cap_camion_frio_t: null, cap_camion_alimento_t: null, cap_camion_sub_t: null,
    };
  }

  // ---------------------------------------------------------------------------------------------
  // Estado de los escenarios A/B/C: cada uno guarda SUS PROPIAS entradas (copias independientes).
  // ---------------------------------------------------------------------------------------------
  const SLOTS = ["A", "B", "C"];

  function estadoInicial(data) {
    const esc = {};
    [["A", 5000], ["B", 10000], ["C", 20000]].forEach(([s, E]) => {
      esc[s] = Object.assign(entradasPorDefecto(data, `Escenario ${s}`), { escala: E });
    });
    return { activo: "A", escenarios: esc };
  }

  function clonar(o) { return JSON.parse(JSON.stringify(o)); }

  function conEntrada(estado, slot, clave, valor) {
    const nuevo = { activo: estado.activo, escenarios: {} };
    SLOTS.forEach((s) => { nuevo.escenarios[s] = clonar(estado.escenarios[s]); });
    nuevo.escenarios[slot][clave] = valor;
    return nuevo;
  }

  function copiarEscenario(estado, de, a) {
    const nuevo = clonar(estado);
    const nombre = nuevo.escenarios[a].nombre;
    nuevo.escenarios[a] = clonar(estado.escenarios[de]);
    nuevo.escenarios[a].nombre = nombre;
    return nuevo;
  }

  // ---------------------------------------------------------------------------------------------
  // Producción primaria: port 1:1 de mp.calcular (+ escalado por días/año de modelo_escala.produccion)
  // ---------------------------------------------------------------------------------------------
  function consumoAcumulado(edad, ref) {
    const xs = Object.keys(ref).map(Number).sort((a, b) => a - b);
    if (Object.prototype.hasOwnProperty.call(ref, String(edad))) return ref[String(edad)];
    const menores = xs.filter((x) => x < edad).length;
    const i = Math.max(1, Math.min(xs.length - 1, menores));
    const x0 = xs[i - 1], x1 = xs[i];
    const y0 = ref[String(x0)], y1 = ref[String(x1)];
    return y0 + (y1 - y0) * (edad - x0) / (x1 - x0);
  }

  function repartoFases(edad, ref) {
    const total = consumoAcumulado(edad, ref);
    const inicio = ref["10"] / total;
    const crecimiento = (ref["24"] - ref["10"]) / total;
    return [inicio, crecimiento, 1 - inicio - crecimiento];
  }

  function mpCalcular(P, aves, ds, p) {
    const SEM = P.semanas_anio;
    const dias_anio = P.calendarios[String(ds)];
    const pp = P.produccion;
    const cargadas_dia = aves / (1 - p.doa);
    const pollitos_dia = cargadas_dia / (1 - p.mort);
    const faenadas_sem = aves * ds;
    const cargadas_sem = cargadas_dia * ds;
    const pollitos_sem = pollitos_dia * ds;
    const faenadas_anio = aves * dias_anio;
    const cargadas_anio = faenadas_anio / (1 - p.doa);
    const pollitos_anio = cargadas_anio / (1 - p.mort);
    const ciclo_total = p.edad + p.vacio;
    const ciclos = 365 / ciclo_total * pp.disponibilidad;
    const capacidad = pollitos_sem * SEM / ciclos;
    const m2 = capacidad * (1 - p.mort) * p.peso / p.kg_m2;
    const alimento_anio_kg = cargadas_anio * p.peso * p.fcr;
    const alimento_sem_kg = cargadas_sem * p.peso * p.fcr;
    const [ini, cre, ter] = repartoFases(p.edad, pp.consumo_acumulado_ref);
    const r = {
      dias_faena_anio: dias_anio,
      aves_faenadas_semana_plena: faenadas_sem,
      aves_cargadas_dia: cargadas_dia,
      aves_cargadas_semana_plena: cargadas_sem,
      pollitos_alojados_por_dia_faena: pollitos_dia,
      pollitos_alojados_semana_plena: pollitos_sem,
      aves_faenadas_anio: faenadas_anio,
      aves_cargadas_anio: cargadas_anio,
      pollitos_alojados_anio: pollitos_anio,
      pollitos_alojados_semana_promedio: pollitos_anio / SEM,
      mortalidad_granja_aves_anio: pollitos_anio - cargadas_anio,
      mortalidad_transporte_aves_anio: cargadas_anio - faenadas_anio,
      ciclo_total_dias: ciclo_total,
      ciclos_anio: ciclos,
      capacidad_alojamiento_pollitos: capacidad,
      utilizacion_anual_galpones: pollitos_anio / (capacidad * ciclos),
      inventario_aves_ritmo_pleno: pollitos_sem / 7 * p.edad * (1 - p.mort / 2),
      inventario_aves_promedio_anual: pollitos_anio / 365 * p.edad * (1 - p.mort / 2),
      m2_galpon: m2,
      pollitos_m2_alojamiento: capacidad / m2,
      kg_vivo_cargado_anio: cargadas_anio * p.peso,
      alimento_por_ave_faenada_kg: alimento_anio_kg / faenadas_anio,
      alimento_por_pollito_alojado_kg: alimento_anio_kg / pollitos_anio,
      alimento_t_anio: alimento_anio_kg / 1000,
      alimento_t_mes_promedio: alimento_anio_kg / 1000 / 12,
      alimento_t_semana_promedio: alimento_anio_kg / 1000 / SEM,
      alimento_t_semana_plena: alimento_sem_kg / 1000,
      alimento_inicio_t_anio: alimento_anio_kg / 1000 * ini,
      alimento_crecimiento_t_anio: alimento_anio_kg / 1000 * cre,
      alimento_terminacion_t_anio: alimento_anio_kg / 1000 * ter,
      alimento_ciclo_crianza_t: alimento_sem_kg / 1000 * p.edad / 7,
      agua_bebida_m3_anio: alimento_anio_kg * pp.relacion_agua_alimento / 1000,
      agua_bebida_m3_dia_promedio: alimento_anio_kg * pp.relacion_agua_alimento / 1000 / 365,
      agua_bebida_m3_semana_plena: alimento_sem_kg * pp.relacion_agua_alimento / 1000,
    };
    pp.tamanos_galpon_m2.forEach((t) => { r[`galpones_${t}m2`] = m2 / t; });
    return r;
  }

  /** modelo_escala.produccion: si días/año difiere del calendario SUP-025, las variables ANUALES
   *  se escalan por días/año / días de referencia (las de semana plena no cambian). */
  function produccion(P, aves, ds, da, p) {
    const r = mpCalcular(P, aves, ds, p);
    const k = da / P.calendarios[String(ds)];
    P.produccion.claves_anuales.forEach((c) => { r[c] *= k; });
    r.dias_faena_anio = da;
    return r;
  }

  // ---------------------------------------------------------------------------------------------
  // Balance: lectura de coeficientes (kg/ave) exportados del modelo
  // ---------------------------------------------------------------------------------------------
  function clavePeso(peso) { return (Math.round(peso * 10) / 10).toFixed(1); }

  function kgPorAve(data, config, peso) {
    const c = data.coeficientes[config];
    if (!c) throw new Error(`Configuración ${config} inexistente`);
    const k = c[clavePeso(peso)];
    if (!k) throw new Error(`Peso ${peso} kg fuera del rango del balance`);
    return k;
  }

  // ---------------------------------------------------------------------------------------------
  // Demanda vs capacidad: port de modelo_escala.aves_por_mix y comparar_demanda
  // ---------------------------------------------------------------------------------------------
  function avesPorMix(D, mix, y, fMila, rolMix) {
    const kg = {};
    Object.values(rolMix).forEach((rol) => { kg[rol] = 0; });
    Object.keys(mix).forEach((prod) => { kg[rolMix[prod]] += D * mix[prod]; });
    const n_ent = kg.entero / y.entero;
    const pech_req = kg.pechuga + kg.milanesa * fMila;
    const cand = [
      ["pechuga (incluye milanesas)", pech_req / y.pechuga],
      ["pata-muslo", kg.pata_muslo / y.pata_muslo],
      ["alas", kg.alas / y.alas],
      ["menudencias", Math.max(0, kg.menudencias / y.menudencias - n_ent)],
    ];
    let lim = cand[0];
    cand.forEach((c) => { if (c[1] > lim[1]) lim = c; });           // max() de Python: primer máximo
    const n_tro = lim[1];
    const n = n_ent + n_tro;
    const exc = {
      pechuga: n_tro * y.pechuga - pech_req, pata_muslo: n_tro * y.pata_muslo - kg.pata_muslo,
      alas: n_tro * y.alas - kg.alas, menudencias: n * y.menudencias - kg.menudencias,
    };
    const otras = n_tro * (y.comestible_ave_trozada - y.pechuga - y.pata_muslo - y.alas - y.menudencias)
      + n_ent * (y.comestible_ave_entero - y.entero - y.menudencias);
    const demandada = kg.entero + pech_req + kg.pata_muslo + kg.alas + kg.menudencias;
    const producida = n_ent * y.comestible_ave_entero + n_tro * y.comestible_ave_trozada;
    const sumaExc = exc.pechuga + exc.pata_muslo + exc.alas + exc.menudencias;
    return {
      aves_dia_cal: n, aves_entero: n_ent, aves_trozado: n_tro, limitante: lim[0], excedentes: exc,
      otras_partes: otras, excedente_total: sumaExc + otras, masa_demandada_ave: demandada,
      masa_producida: producida, fuera_balance: kg.fuera_balance || 0,
      comestible_por_ave_mix: n ? producida / n : 0,
    };
  }

  function resultadoM0(D, k) {
    return { aves_dia_cal: D / k.comestible, masa_demandada_ave: D, comestible_por_ave_mix: k.comestible,
      excedente_total: 0, limitante: "ninguna (ave completa)", fuera_balance: 0, excedentes: null, otras_partes: 0 };
  }

  function convertir(valor, de, a, dias_anio) {
    const por = { dia_operativo: dias_anio, dia_calendario: DIAS_CAL, anio: 1 };
    if (!(de in por) || !(a in por)) throw new Error(`Conversión no definida: ${de} -> ${a}`);
    return valor * por[de] / por[a];
  }

  function compararDemanda(E, dias_anio, D, res) {
    const n = res.aves_dia_cal;
    const cap_cal = convertir(E, "dia_operativo", "dia_calendario", dias_anio);
    const factor = cap_cal ? n / cap_cal : Infinity;
    const utiliz = Math.min(1, factor);
    const cobertura = factor ? Math.min(1, 1 / factor) : 1;
    const com = res.comestible_por_ave_mix;
    const nOp = convertir(n, "dia_calendario", "dia_operativo", dias_anio);
    return {
      factor_demanda_capacidad: factor,
      utilizacion_planta: utiliz,
      cobertura_demanda: cobertura,
      aves_necesarias_dia_operativo: nOp,
      aves_procesadas_dia_operativo: E * utiliz,
      aves_faltantes_dia_operativo: Math.max(0, nOp - E),
      capacidad_ociosa_aves_dia_operativo: E * (1 - utiliz),
      kg_atendidos_dia_cal: D * cobertura,
      kg_no_atendidos_dia_cal: D * (1 - cobertura),
      produccion_comestible_plena_kg_dia_cal: cap_cal * com,
      kg_sin_destino_plena_escala: res.excedente_total * cobertura + Math.max(0, cap_cal - n) * com,
      demanda_adicional_para_llenar_kg_dia_cal: factor ? Math.max(0, D * (1 / factor - 1)) : 0,
    };
  }

  function demandaDeEntradas(data, e) {
    if (e.demanda_id === "MANUAL") {
      return { id: "MANUAL", nombre: "Manual", total_kg_dia: Number(e.demanda_manual_kg) || 0,
        categoria: "Ingresada por el usuario (hipótesis)", exportacion_kg_dia: 0, bloque: "manual" };
    }
    if (e.demanda_id === "CERO") {
      return { id: "CERO", nombre: "Solo demanda documentada actual", total_kg_dia: 0,
        categoria: "Demanda documentada actual: no validada / prácticamente nula (DPV-003, DPV-004)", exportacion_kg_dia: 0, bloque: "documentada" };
    }
    const d = data.demanda.escenarios.find((x) => x.id === e.demanda_id);
    if (!d) throw new Error(`Escenario de demanda ${e.demanda_id} inexistente`);
    return d;
  }

  // ---------------------------------------------------------------------------------------------
  // Validación de entradas
  // ---------------------------------------------------------------------------------------------
  function validar(data, e) {
    const err = [];
    const num = (v) => typeof v === "number" && isFinite(v);
    Object.keys(RANGOS).forEach((k) => {
      const [lo, hi, et] = RANGOS[k];
      if (!num(e[k])) err.push(`${et}: valor vacío o no numérico.`);
      else if (e[k] < lo - 1e-9 || e[k] > hi + 1e-9) err.push(`${et}: ${e[k]} fuera del rango admitido (${lo}–${hi}).`);
    });
    if (!(String(e.dias_semana) in data.parametros.calendarios))
      err.push("Días de faena por semana: el modelo de producción solo admite 5 o 6.");
    else {
      const max = e.dias_semana * data.parametros.semanas_anio;
      if (!num(e.dias_anio) || e.dias_anio <= 0 || e.dias_anio > max + 1e-9)
        err.push(`Días de faena por año (${e.dias_anio}) incompatibles con ${e.dias_semana} días/semana (máximo ${max.toFixed(1)}).`);
    }
    if (num(e.peso) && Math.abs(e.peso * 10 - Math.round(e.peso * 10)) > 1e-6)
      err.push("Peso vivo: el balance se exporta en pasos de 0,1 kg.");
    if (!data.coeficientes[e.config]) err.push("Configuración comercial inexistente.");
    if (!["M0", "M1", "M2", "M3"].includes(e.metodo)) err.push("Método de conversión de la demanda inexistente.");
    if (!["dias_produccion", "dias_calendario"].includes(e.base_inventario)) err.push("Base temporal del inventario inexistente.");
    if (!data.parametros.perfiles_destino[e.perfil_destino]) err.push("Perfil de destino inexistente.");
    if (e.demanda_id === "MANUAL" && (!num(e.demanda_manual_kg) || e.demanda_manual_kg < 0))
      err.push("Demanda manual: ingresar kg de producto por día calendario (≥ 0).");
    ["m2_por_productor", "aves_por_camion", "cap_camion_frio_t", "cap_camion_alimento_t", "cap_camion_sub_t"].forEach((k) => {
      if (e[k] !== null && e[k] !== undefined && (!num(e[k]) || e[k] <= 0)) err.push(`${k}: debe ser positivo o quedar vacío.`);
    });
    return err;
  }

  // ---------------------------------------------------------------------------------------------
  // Cálculo completo de un escenario
  // ---------------------------------------------------------------------------------------------
  function calcular(data, e) {
    const errores = validar(data, e);
    if (errores.length) return { ok: false, errores, alertas: [] };
    const P = data.parametros;
    const E = e.escala, u = e.utilizacion, ds = e.dias_semana, da = e.dias_anio;
    const aves = E * u;                                        // aves realmente faenadas / día operativo
    const pprod = { edad: e.edad, peso: e.peso, fcr: e.fcr, mort: e.mortalidad, doa: e.doa, vacio: e.vacio, kg_m2: e.kg_m2 };
    const k = kgPorAve(data, e.config, e.peso);
    const kcfg = { A: kgPorAve(data, "A", e.peso), B: kgPorAve(data, "B", e.peso), C: kgPorAve(data, "C", e.peso) };
    const t = (clave, n) => k[clave] * n / 1000;              // t/día operativo

    // 1. capacidad y ritmo (la capacidad es E; el ritmo se calcula sobre la capacidad, como el modelo)
    const capacidad = {
      escala: E, utilizacion: u, aves_procesadas_dia_op: aves, capacidad_ociosa_supuesta_dia_op: E - aves,
      aves_anio: aves * da, aves_anio_plena_escala: E * da,
      aves_dia_cal_equivalente: convertir(aves, "dia_operativo", "dia_calendario", da),
      ritmo_aves_h: E / e.horas_netas, ritmo_kg_vivo_h: E * e.peso / e.horas_netas,
      ritmo_aves_h_8h: E / 8, dias_anio: da, dias_semana: ds, horas_netas: e.horas_netas,
    };

    // 2. producción primaria a la utilización elegida y a plena escala (dimensionamiento)
    const prod = produccion(P, aves, ds, da, pprod);
    const prodPlena = produccion(P, E, ds, da, pprod);
    const m2Prop = prod.m2_galpon * e.pct_propio;
    const m2Int = prod.m2_galpon - m2Prop;
    const abastecimiento = {
      pct_propio: e.pct_propio, m2_propios: m2Prop, m2_integrados: m2Int,
      plazas_propias: prod.capacidad_alojamiento_pollitos * e.pct_propio,
      plazas_integradas: prod.capacidad_alojamiento_pollitos * (1 - e.pct_propio),
      productores: e.m2_por_productor ? m2Int / e.m2_por_productor : null,
      productores_ilustrativos: [1, 2, 4].map((n) => ({ galpones_2400: n, productores: m2Int / (n * 2400) })),
    };

    // 3. balance por ítem (t/día operativo y t/año) y agregados
    const items = P.items.map((it) => ({
      clave: it.clave, etiqueta: it.etiqueta, clase: it.clase, kg_ave: k[it.clave],
      t_dia_op: t(it.clave, aves), t_anio: t(it.clave, aves) * da,
    }));
    const agregados = {};
    ["peso_vivo", "agua_incorporada", "producto_principal", "coproductos", "comestible", "subproductos_c",
      "residuos_d", "perdidas_p", "agua_retenida_comestible", "comestible_bio", "producto_principal_bio",
      "rendering_potencial", "solidos_a_retirar", "efluente_o_perdida", "c_perecedero_sin_plumas",
      "garras_grado_a", "sangre_drenada", "plumas_bio", "cms_alternativa_no_sumable", "kg_trozado",
      "kg_deshuese", "kg_cms"].forEach((c) => {
      agregados[c] = { kg_ave: k[c], t_dia_op: t(c, aves), t_anio: t(c, aves) * da };
    });
    const masa = {};
    [["biologica", "comestible_bio"], ["agua", "agua_retenida_comestible"], ["comercial", "comestible"],
      ["principal_biologica", "producto_principal_bio"], ["principal_comercial", "producto_principal"]].forEach(([n, c]) => {
      const op = t(c, aves);
      masa[n] = { t_dia_op: op, t_dia_cal: convertir(op, "dia_operativo", "dia_calendario", da), t_anio: op * da };
    });
    const configuraciones = {};
    Object.keys(kcfg).forEach((c) => {
      const kc = kcfg[c];
      const f = (x) => kc[x] * aves / 1000;
      configuraciones[c] = {
        producto_principal_t: f("producto_principal"), coproductos_t: f("coproductos"), huesos_t: f("huesos"),
        recortes_piel_t: f("recortes_piel"), cms_t: f("cms"), cms_alternativa_no_sumable_t: f("cms_alternativa_no_sumable"),
        subproductos_c_t: f("subproductos_c"), comestible_t: f("comestible"), kg_trozado_t: f("kg_trozado"),
        kg_deshuese_t: f("kg_deshuese"), kg_cms_t: f("kg_cms"), flujos_comestibles_distintos: kc.flujos_comestibles,
        coproductos_por_t_de_producto_principal: kc.coproductos / kc.producto_principal,
      };
    });

    // 4. subproductos (t/día operativo, biológica + agua adherida)
    const subproductos = {};
    ["plumas", "sangre", "sangre_drenada", "visceras", "cabeza", "garras", "carcasa_esqueleto", "huesos",
      "rendering_potencial", "solidos_a_retirar", "plumas_bio", "otros_c"].forEach((c) => {
      subproductos[c] = { t_dia_op: t(c, aves), t_anio: t(c, aves) * da, kg_ave: k[c] };
    });

    // 5. inventario (SUP-056): dos bases temporales
    const prodCom = t("comestible", aves);
    const despCal = convertir(prodCom, "dia_operativo", "dia_calendario", da);
    const flujoBase = { dias_produccion: prodCom, dias_calendario: despCal };
    const perfil = P.perfiles_destino[e.perfil_destino];
    const inv = {};
    Object.keys(flujoBase).forEach((b) => {
      const f = flujoBase[b];
      inv[b] = {
        flujo_t_dia: f, comestible_total_t: f * e.dias_inventario,
        refrigerado_t: f * perfil.reparto.refrigerado * e.dias_inventario,
        congelado_t: f * perfil.reparto.congelado * e.dias_congelado,
        exportacion_t: f * perfil.reparto.exportacion * e.dias_congelado,
      };
    });
    const inventario = {
      base_elegida: e.base_inventario, dias: e.dias_inventario, dias_congelado: e.dias_congelado,
      perfil: e.perfil_destino, perfil_nombre: perfil.nombre, reparto: perfil.reparto,
      por_base: inv, elegido: inv[e.base_inventario],
      subproductos_frio_t: t("c_perecedero_sin_plumas", aves) * e.dias_inventario,
      equivalencia_dias_produccion_de_dias_calendario: e.dias_inventario * da / DIAS_CAL,
    };

    // 6. logística (t/día operativo)
    const logistica = {
      aves_vivas_cargadas_t_dia: prod.aves_cargadas_dia * e.peso / 1000,
      aves_vivas_recibidas_faenadas_t_dia: k.peso_vivo * aves / 1000,
      producto_comestible_sale_t_dia: prodCom,
      subproductos_solidos_salen_t_dia: t("solidos_a_retirar", aves),
      masa_a_efluente_o_perdida_t_dia: t("efluente_o_perdida", aves),
      alimento_a_granjas_t_dia_semana_plena: prod.alimento_t_semana_plena / 7,
      alimento_a_granjas_t_dia_promedio_anual: prod.alimento_t_anio / 365,
      camiones_aves_vivas_rango: P.aves_por_camion_vivo.map((c) => prod.aves_cargadas_dia / c),
      camiones_aves_vivas: e.aves_por_camion ? prod.aves_cargadas_dia / e.aves_por_camion : null,
      camiones_frio: e.cap_camion_frio_t ? prodCom / e.cap_camion_frio_t : null,
      camiones_alimento: e.cap_camion_alimento_t ? prod.alimento_t_semana_plena / 7 / e.cap_camion_alimento_t : null,
      retiros_subproductos: e.cap_camion_sub_t ? t("solidos_a_retirar", aves) / e.cap_camion_sub_t : null,
      indice_movimientos_vs_2500: aves / P.escalas[0],
    };

    // 7. exportación: días de faena para completar un contenedor (NO es demanda)
    const kB = kcfg.B;
    const exportacion = [["pollo_entero", "Pollo entero (ave entera)", kcfg.A.pollo_entero], ["pechuga", "Pechuga con hueso", kB.pechuga],
      ["pata_muslo", "Pata-muslo", kB.pata_muslo], ["alas", "Alas", kB.alas], ["garras_grado_a", "Garras grado A", kB.garras_grado_a],
      ["menudencias", "Menudencias", kB.menudencias], ["cuello", "Cuello", kB.cuello], ["carcasa_esqueleto", "Carcasa-esqueleto", kB.carcasa_esqueleto]]
      .map(([c, et, kg]) => ({ clave: c, etiqueta: et, kg_ave: kg,
        dias_para_contenedor: aves > 0 ? P.contenedor_t * 1000 / (kg * aves) : Infinity,
        contenedores_mes_si_100pct: kg * aves * da / 12 / 1000 / P.contenedor_t }));

    // 8. demanda vs capacidad (la capacidad es E; la demanda está en día calendario)
    const dem = demandaDeEntradas(data, e);
    const D = dem.total_kg_dia;
    const y = data.rendimientos_mix[clavePeso(e.peso)];
    const metodos = {};
    const resM0 = resultadoM0(D, k);
    metodos.M0 = Object.assign({ res: resM0 }, compararDemanda(E, da, D, resM0));
    ["M1", "M2", "M3"].forEach((m) => {
      const r = avesPorMix(D, data.demanda.mixes[m], y, data.demanda.factor_milanesa, data.demanda.rol_mix);
      metodos[m] = Object.assign({ res: r }, compararDemanda(E, da, D, r));
    });
    // Métricas OPERATIVAS (con la producción simulada E × u). Las del modelo (factor, utilizacion_planta,
    // cobertura_demanda, capacidad_ociosa_aves_dia_operativo) se refieren a la capacidad INSTALADA.
    Object.keys(metodos).forEach((m) => {
      const x = metodos[m], f = x.factor_demanda_capacidad;
      x.utilizacion_requerida_por_demanda = x.utilizacion_planta;             // = mín(factor; 100 %)
      x.cobertura_maxima_plena_capacidad = x.cobertura_demanda;               // = mín(1 / factor; 100 %)
      x.cobertura_operativa = D > 0 ? Math.min(1, u / f) : 1;                 // = mín(producción simulada / requerida; 100 %)
      x.kg_atendidos_operativo_dia_cal = D * x.cobertura_operativa;
      x.kg_no_atendidos_operativo_dia_cal = D * (1 - x.cobertura_operativa);
      x.aves_no_atendidas_operativo_dia_op = Math.max(0, x.aves_necesarias_dia_operativo - aves);
      x.aves_producidas_sin_demanda_dia_op = Math.max(0, aves - x.aves_necesarias_dia_operativo);
      x.capacidad_disponible_respecto_demanda = x.capacidad_ociosa_aves_dia_operativo;   // = máx(0; E − requerida)
    });
    const sel = metodos[e.metodo];
    const kgComCalPlena = k.comestible * E * da / DIAS_CAL;
    const demanda = {
      escenario: dem, D, metodo: e.metodo, metodos, sel,
      utilizacion_que_justifica: sel.utilizacion_planta,
      capacidad_kg_dia_cal_plena: kgComCalPlena,
      produccion_kg_dia_cal_a_u: kgComCalPlena * u,
      demanda_necesaria_100pct_kg_dia_cal: kgComCalPlena,
      demanda_necesaria_a_u_kg_dia_cal: kgComCalPlena * u,
      kg_por_local_dia_plena: kgComCalPlena / data.demanda.locales,
      kg_por_local_dia_a_u: kgComCalPlena * u / data.demanda.locales,
      kg_sin_destino_a_u_dia_cal: Math.max(0, kgComCalPlena * u - D),
      locales: data.demanda.locales,
      factor_conversion_op_cal: da / DIAS_CAL,
    };

    // 9. tabla central "qué debe ser verdad" (a la utilización elegida; con u = 100 % = CSV)
    const central = {
      aves_anio: aves * da,
      kg_vivo_dia: k.peso_vivo * aves,
      t_vivas_anio: k.peso_vivo * aves * da / 1000,
      pollitos_semana_plena: prod.pollitos_alojados_semana_plena,
      plazas_granja: prod.capacidad_alojamiento_pollitos,
      m2_galpones: prod.m2_galpon,
      alimento_t_anio: prod.alimento_t_anio,
      comestible_masa_biologica_t_dia_operativo: masa.biologica.t_dia_op,
      agua_retenida_en_producto_t_dia_operativo: masa.agua.t_dia_op,
      producto_comercial_t_dia_operativo: masa.comercial.t_dia_op,
      producto_comercial_t_dia_calendario_promedio: masa.comercial.t_dia_cal,
      producto_comercial_t_anio: masa.comercial.t_anio,
      producto_principal_t_dia: t("producto_principal", aves),
      plumas_t_dia: t("plumas", aves),
      sangre_recuperada_t_dia: t("sangre", aves),
      visceras_t_dia: t("visceras", aves),
      ritmo_linea_8h_aves_h: E / 8,
      inventario_7_dias_de_produccion_t: prodCom * 7,
      inventario_7_dias_calendario_t: despCal * 7,
      demanda_necesaria_100pct_kg_dia_cal: kgComCalPlena * u,
      demanda_necesaria_85pct_kg_dia_cal: 0.85 * kgComCalPlena * u,
      demanda_necesaria_70pct_kg_dia_cal: 0.70 * kgComCalPlena * u,
      kg_por_local_dia_si_todo_por_la_red_100pct: kgComCalPlena * u / data.demanda.locales,
    };

    capacidad.capacidad_ociosa_operativa = E - aves;                          // = instalada − producción simulada
    const est = rangoEstudiado(data);
    const fueraRango = { escala: E < est.escala[0] || E > est.escala[1], peso: e.peso < est.peso[0] - 1e-9 || e.peso > est.peso[1] + 1e-9,
      rango_escala: est.escala, rango_peso: est.peso };
    const g = e.peso / e.edad * 1000, [g0, g1] = UMBRALES.ganancia_diaria_ref_g;
    const fcrRef = interpFcr(P.produccion.perfiles, e.peso);
    const coherencia = { ganancia_g_dia: g, fuera_ganancia: g < g0 * 0.85 || g > g1 * 1.15, fcr_ref: fcrRef,
      fuera_fcr: Math.abs(e.fcr - fcrRef) > UMBRALES.fcr_desvio_max + 1e-9 };
    const escenario_matematico = coherencia.fuera_ganancia || coherencia.fuera_fcr;

    const r = { ok: true, entradas: clonar(e), k, kcfg, capacidad, fuera_rango: fueraRango, coherencia, escenario_matematico, produccion: prod, produccion_plena: prodPlena,
      abastecimiento, items, agregados, masa, configuraciones, subproductos, inventario, logistica, exportacion,
      demanda, central };
    r.alertas = alertas(data, e, r);
    return r;
  }

  // ---------------------------------------------------------------------------------------------
  // Alertas: informan, no recomiendan. Umbrales de interfaz documentados en observaciones_html_v01.md
  // ---------------------------------------------------------------------------------------------
  const UMBRALES = {
    utilizacion_baja: 0.50,           // interfaz: la mitad de lo construido sin uso
    subproductos_flujo_industrial_t: 5.0, // escenarios_escala.md §10: ~5,3 t/día de clase C = flujo industrial
    rendering_referencia_t: [5, 17],  // 07_subproductos/rendering.md: alimentación continua de un proceso
    inventario_alto_dias: 7,          // interfaz: una semana de producción en cámara
    ritmo_max_estudiado: 2500,        // 20.000 aves/día a 8 h netas (máximo del rango del modelo)
    kg_local_max: 300,                // extremo superior del rango de la red (AL10)
    ganancia_diaria_ref_g: [58, 62],  // guía de producción primaria (indicador 6); tolerancia de interfaz ±15 %
    fcr_desvio_max: 0.15,             // interfaz: = diferencia entre desempeño medio y desfavorable (SUP-026)
  };
  const TXT_ILUSTRATIVO = "Umbral visual ilustrativo: umbral de interfaz, pendiente de calibración económica y operativa.";

  function fmtN(x, d) {
    return Number(x).toLocaleString("es-AR", { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  }

  function alertas(data, e, r) {
    const A = [];
    const add = (id, nivel, titulo, texto, ref, ilustrativo) => A.push({ id, nivel, titulo, texto, ref, ilustrativo: !!ilustrativo });
    const dm = r.demanda, sel = dm.sel, u = e.utilizacion;
    const hayDem = dm.D > 0;
    // AL1 — siempre visible
    add("AL1", "aviso", "Demanda documentada ≈ 0",
      "La demanda documentada actual (con evidencia comercial) es prácticamente nula: no respalda ningún nivel de utilización. " +
      "Todos los escenarios de demanda son hipótesis sin evidencia comercial, no ventas.", "AL1 · SUP-021 · DPV-003 · DPV-004");
    // Demanda documentada ≈ 0 elegida: la producción simulada no tiene respaldo
    if (dm.escenario.id === "CERO")
      add("DOC0", "aviso", "Producción sin demanda documentada",
        `Este escenario simula producción al ${fmtN(u * 100)} %, pero actualmente no existe demanda documentada que respalde ese nivel de operación. ` +
        "Es válido como escenario hipotético.", "DPV-003 · DPV-004");
    // Rango principal estudiado
    const fr = r.fuera_rango;
    if (fr.escala)
      add("RANGO_E", "aviso", "ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO",
        `${fmtN(e.escala)} aves/día está fuera del rango principal estudiado (${fmtN(fr.rango_escala[0])}–${fmtN(fr.rango_escala[1])} aves/día). ` +
        "Constituye una extrapolación física del modelo y NO una escala analizada en profundidad.", "23_plan_expansion · SUP-052");
    if (fr.peso)
      add("RANGO_P", "aviso", "Peso fuera del rango principal estudiado",
        `Peso fuera del rango principal utilizado en el estudio (${fmtN(fr.rango_peso[0], 1)}–${fmtN(fr.rango_peso[1], 1)} kg); resultados deben tratarse como extrapolación. ` +
        `El motor admite ${fmtN(RANGOS.peso[0], 1)}–${fmtN(RANGOS.peso[1], 1)} kg.`, "04_balance_masa · SUP-036");
    // Coherencia peso–edad–FCR: se calcula igual, pero es un escenario matemático
    if (r.escenario_matematico) {
      const c = r.coherencia, det = [];
      if (c.fuera_ganancia) det.push(`${fmtN(e.peso, 1)} kg a ${fmtN(e.edad)} días = ${fmtN(c.ganancia_g_dia)} g/día de ganancia media (referencia ~58–62 g/día)`);
      if (c.fuera_fcr) det.push(`FCR ${fmtN(e.fcr, 2)} frente a ~${fmtN(c.fcr_ref, 2)} interpolado entre los perfiles del estudio para ${fmtN(e.peso, 1)} kg`);
      add("MAT", "aviso", "Escenario matemático",
        `Escenario matemático. La combinación peso–edad–FCR requiere validación zootécnica. ${det.join("; ")}. ` +
        "El cálculo se mantiene, pero granjas, alimento y masa no representan un escenario productivo del estudio.",
        "SUP-026 · SUP-027 · SUP-028", true);
    } else if (Math.abs(e.peso - data.parametros.peso_ref) > 1e-9 && Math.abs(e.fcr - data.parametros.produccion.defaults.fcr) < 1e-9)
      add("INC2", "info", "El FCR no cambia solo con el peso",
        `Cambiaste el peso pero el FCR sigue en ${fmtN(e.fcr, 2)}. Un ave más pesada convierte peor: ~${fmtN(r.coherencia.fcr_ref, 2)} a ${fmtN(e.peso, 1)} kg interpolando los perfiles del estudio (1,58 / 1,70 / 1,82).`,
        "SUP-028");
    // Utilización operativa asumida vs requerida por la demanda
    if (hayDem && u < sel.utilizacion_requerida_por_demanda - 1e-9)
      add("UOP", "aviso", "El escenario operativo no cubre toda la demanda",
        `Con la utilización asumida (${fmtN(u * 100)} %) se procesan ${fmtN(r.capacidad.aves_procesadas_dia_op)} aves/día operativo de las ` +
        `${fmtN(sel.aves_necesarias_dia_operativo)} que requiere la demanda (utilización requerida ${fmtN(sel.utilizacion_requerida_por_demanda * 100)} %). ` +
        `Cobertura con la producción simulada: ${fmtN(sel.cobertura_operativa * 100)} %; quedan ${fmtN(sel.kg_no_atendidos_operativo_dia_cal)} kg/día calendario sin atender` +
        (sel.factor_demanda_capacidad <= 1 + 1e-9 ? ", aunque la capacidad instalada alcanzaría técnicamente." : "."), "SUP-060");
    if (hayDem && u > sel.utilizacion_requerida_por_demanda + 1e-9)
      add("AL2", "aviso", "Más producción de la que la demanda requiere",
        `La utilización asumida (${fmtN(u * 100)} %) supera la requerida por la demanda (${fmtN(sel.utilizacion_requerida_por_demanda * 100)} %): ` +
        `${fmtN(sel.aves_producidas_sin_demanda_dia_op)} aves/día operativo producidas sin destino en el escenario (~${fmtN(dm.kg_sin_destino_a_u_dia_cal)} kg/día calendario con M0).`, "AL2");
    // AL3 — demanda > capacidad instalada
    if (sel.factor_demanda_capacidad > 1 + 1e-9)
      add("AL3", "aviso", "La demanda del escenario excede la capacidad instalada",
        `Factor demanda/capacidad instalada ${fmtN(sel.factor_demanda_capacidad * 100)} %: aun a plena capacidad la cobertura máxima sería ${fmtN(sel.cobertura_maxima_plena_capacidad * 100)} % ` +
        `y quedarían ${fmtN(sel.kg_no_atendidos_dia_cal)} kg/día calendario sin atender (faltan ${fmtN(sel.aves_faltantes_dia_operativo)} aves/día operativo de capacidad).`, "AL3 · SUP-060");
    // Utilización muy baja (umbral ilustrativo)
    if (u < UMBRALES.utilizacion_baja)
      add("UB1", "aviso", "Utilización operativa asumida baja",
        `Se asume ${fmtN(u * 100)} % de utilización: ${fmtN(r.capacidad.capacidad_ociosa_operativa)} aves/día operativo de capacidad ociosa operativa. ` +
        "Qué utilización es «baja» lo definirán CAPEX y OPEX.", `Umbral visual ilustrativo < ${UMBRALES.utilizacion_baja * 100} %`, true);
    if (hayDem && sel.utilizacion_requerida_por_demanda < UMBRALES.utilizacion_baja)
      add("UB2", "aviso", "La demanda requiere poca utilización",
        `Con el escenario «${dm.escenario.nombre}» (${e.metodo}) la demanda requiere solo ${fmtN(sel.utilizacion_requerida_por_demanda * 100)} % de la capacidad instalada: ` +
        `${fmtN(sel.capacidad_disponible_respecto_demanda)} aves/día operativo de capacidad disponible respecto de la demanda.`,
        `Umbral visual ilustrativo < ${UMBRALES.utilizacion_baja * 100} % · SUP-060`, true);
    // AL4 — excedente de partes con M1-M3
    if (e.metodo !== "M0" && sel.res.excedente_total > 0.5)
      add("AL4", "aviso", "Partes sin comprador dentro del escenario",
        `Con el mix ${e.metodo}, por la demanda atendida a plena capacidad quedan ~${fmtN(sel.res.excedente_total * sel.cobertura_demanda)} kg/día calendario ` +
        `de partes que necesitan otros compradores (parte limitante: ${sel.res.limitante}).`, "AL4 · SUP-023 · SUP-054");
    if (e.metodo !== "M0" && sel.res.fuera_balance > 0)
      add("AL4b", "info", "Otros elaborados fuera del balance",
        `${fmtN(sel.res.fuera_balance * sel.cobertura_demanda)} kg/día de «otros elaborados» del mix no se modelan (materia prima no definida).`, "SUP-023");
    if ((dm.escenario.exportacion_kg_dia || 0) > 0)
      add("AL7", "aviso", "Exportación en la demanda", "Exportación sin negociación de nivel ≥ 5 no es demanda (SUP-022).", "AL7 · SUP-022");
    const pend = [];
    if (!e.m2_por_productor) pend.push("m² por productor (DPV-048)");
    if (!e.cap_camion_frio_t || !e.cap_camion_alimento_t || !e.cap_camion_sub_t) pend.push("capacidades de camiones (DPV-084)");
    if (pend.length)
      add("AL8", "info", "Variables de campo pendientes", `Sin dato: ${pend.join("; ")}. Se muestran toneladas y m², no productores ni camiones.`, "AL8");
    if (u >= 1 - 1e-9)
      add("AL9", "info", "100 % es el punto de dimensionamiento", "100 % de utilización es el punto de dimensionamiento, no un supuesto de operación.", "AL9");
    if (dm.kg_por_local_dia_plena > UMBRALES.kg_local_max)
      add("AL10", "aviso", "Más pollo por local que el rango de la red",
        `A plena capacidad serían ${fmtN(dm.kg_por_local_dia_plena)} kg/local/día si todo pasara por los ${dm.locales} locales: ` +
        "más que el extremo superior del rango de la red (25–300 kg/local/día).", "AL10");
    const rend = r.subproductos.rendering_potencial.t_dia_op;
    if (rend >= UMBRALES.subproductos_flujo_industrial_t)
      add("SUB1", "aviso", "Alto volumen de subproductos",
        `${fmtN(rend, 1)} t/día operativo de materia prima potencial de rendering (subproductos no comestibles) y ${fmtN(r.subproductos.solidos_a_retirar.t_dia_op, 1)} t/día de sólidos a retirar: ` +
        "ya es un flujo industrial diario que necesita receptor todos los días de faena. Sin receptor, es costo y riesgo ambiental.",
        "escenarios_escala.md §10 · SUP-049 · DPV-065");
    else
      add("SUB0", "info", "Subproductos: retiro diario en cualquier escala",
        `${fmtN(rend, 2)} t/día de subproductos no comestibles: sangre y vísceras se degradan en horas; aun volúmenes chicos exigen retiro cada día de faena.`,
        "escenarios_escala.md §10");
    if (e.dias_inventario >= UMBRALES.inventario_alto_dias)
      add("INV1", "aviso", "Inventario alto",
        `${fmtN(e.dias_inventario)} días de inventario = ${fmtN(r.inventario.elegido.comestible_total_t, 1)} t (${e.base_inventario === "dias_produccion" ? "días de producción" : "días calendario"}). ` +
        "El producto refrigerado vive días (SUP-051); las cámaras y el frío no están dimensionados (12_energia_frio).",
        `Umbral visual ilustrativo ≥ ${UMBRALES.inventario_alto_dias} días · SUP-051 · SUP-056`, true);
    if (r.capacidad.ritmo_aves_h > UMBRALES.ritmo_max_estudiado)
      add("RIT1", "aviso", "Ritmo horario por encima del rango estudiado",
        `${fmtN(r.capacidad.ritmo_aves_h)} aves/h netas: supera el máximo del rango de los modelos (${fmtN(UMBRALES.ritmo_max_estudiado)} aves/h = 20.000 aves/día a 8 h netas). ` +
        "No se asume eficiencia de máquina; ningún equipo está relevado.", "05_proceso_industrial/capacidad_preliminar.md");
    if (e.horas_netas < 8)
      add("RIT2", "info", "Horas netas cortas",
        `Con ${fmtN(e.horas_netas)} h netas el ritmo es ${fmtN((8 / e.horas_netas - 1) * 100)} % mayor que con 8 h: equipos más rápidos.`, "SUP-053");
    if (e.horas_netas > 10)
      add("RIT3", "aviso", "Más de un turno",
        "Más de 10 h netas implica un segundo turno: es capacidad teórica de la LÍNEA, no de la planta (frío, efluentes, agua, energía, personal, limpieza y pollos deben acompañar).",
        "DEC-036 · SUP-053");
    if (e.dias_anio !== data.parametros.calendarios[String(e.dias_semana)])
      add("INC3", "info", "Días/año distintos del calendario de referencia",
        `${fmtN(e.dias_anio)} días/año con ${e.dias_semana} días/semana (referencia ${data.parametros.calendarios[String(e.dias_semana)]}). ` +
        "Las variables anuales se escalan; las de semana plena no cambian.", "SUP-025");
    add("PVDP", "info", "Datos todavía PVDP",
      "Los rendimientos del balance (FTE-140/142/161–184), la carga de contenedor de 25 t (FTE-135, débil), el límite de 8 % de agua retenida (FTE-168) " +
      "y los perfiles productivos (manuales genéticos) están PENDIENTES DE VERIFICACIÓN DOCUMENTAL PRIMARIA. Aves por camión (SUP-033): sin fuente.",
      "Regla 16 · SUP-036 · SUP-033");
    return A;
  }


  function interpFcr(perfiles, peso) {
    const pts = Object.values(perfiles).map((p) => [p.peso, p.fcr_base]).sort((a, b) => a[0] - b[0]);
    if (peso <= pts[0][0]) return pts[0][1] + (peso - pts[0][0]) * (pts[1][1] - pts[0][1]) / (pts[1][0] - pts[0][0]);
    for (let i = 1; i < pts.length; i++) {
      if (peso <= pts[i][0]) return pts[i - 1][1] + (peso - pts[i - 1][0]) * (pts[i][1] - pts[i - 1][1]) / (pts[i][0] - pts[i - 1][0]);
    }
    const n = pts.length;
    return pts[n - 1][1] + (peso - pts[n - 1][0]) * (pts[n - 1][1] - pts[n - 2][1]) / (pts[n - 1][0] - pts[n - 2][0]);
  }

  return {
    RANGOS, UMBRALES, SLOTS, entradasPorDefecto, estadoInicial, conEntrada, copiarEscenario, clonar,
    mpCalcular, produccion, kgPorAve, avesPorMix, resultadoM0, compararDemanda, convertir, calcular, validar,
    clavePeso, interpFcr, rangoEstudiado, TXT_ILUSTRATIVO,
  };
});
