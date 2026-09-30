/*
 * SIMULADOR DE ESCALA v0.1 — interfaz (DOM). Los cálculos viven en calculo.js; los datos en
 * data/simulador_data.js (generado por generar_datos_simulador.py). Este archivo solo presenta.
 * Sin dependencias externas; funciona abriendo index.html directamente (file://).
 */
(function () {
  "use strict";
  const DATA = window.SIMULADOR_DATA;
  const S = window.SimCalculo;
  if (!DATA || !S) {
    document.getElementById("sin-datos").hidden = false;
    document.querySelector(".disposicion").hidden = true;
    return;
  }
  const P = DATA.parametros;
  const $ = (sel) => document.querySelector(sel);

  // ============================================================================================
  // Formato (es-AR: miles con punto, decimales con coma)
  // ============================================================================================
  const NF = {};
  function fmt(x, d) {
    d = d || 0;
    if (x === null || x === undefined || Number.isNaN(x)) return "—";
    if (!Number.isFinite(x)) return "∞";
    if (!NF[d]) NF[d] = new Intl.NumberFormat("es-AR", { minimumFractionDigits: d, maximumFractionDigits: d });
    return NF[d].format(Math.abs(x) < 1e-9 ? 0 : x);
  }
  const fmtT = (x) => fmt(x, Math.abs(x) < 10 ? 2 : Math.abs(x) < 100 ? 1 : 0);
  const pct = (x, d) => `${fmt(x * 100, d || 0)} %`;
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const CANALES = { supermercados: "Supermercados", mayoristas_distribuidores: "Mayoristas y distribuidores", carnicerias_pollerias: "Carnicerías y pollerías", gastronomia: "Gastronomía", industria: "Industria", exportacion: "Exportación" };
  const NOMBRE_CONFIG = { A: "Pollo entero", B: "Trozado", C: "Deshuesado / mayor procesamiento" };  // claves internas; nunca se muestran las letras

  // ============================================================================================
  // Estado de los datos (regla 4 y 16 de CLAUDE.md)
  // ============================================================================================
  const ESTADOS = {
    modelo: { corto: "Calculado por modelo", tip: "Calculado por modelo significa que la fórmula y su consistencia matemática fueron verificadas. No significa que el valor haya sido validado en una planta real." },
    supuesto: { corto: "Supuesto", tip: "Depende principalmente de un supuesto de trabajo registrado (SUP-###): parámetros productivos de escenario medio, perfiles ilustrativos o escenarios de demanda de prueba." },
    pvdp: { corto: "PVDP", tip: "Depende de rendimientos o parámetros construidos con fuentes PENDIENTES DE VERIFICACIÓN DOCUMENTAL PRIMARIA (manuales genéticos, bibliografía, prensa). No es una medición de una planta argentina." },
    campo: { corto: "Dato de campo pendiente", tip: "Requiere un dato que todavía no existe y debe relevarse en campo (DPV-###): demanda real, productores, vehículos, receptores de subproductos." },
  };
  let ESC_MAT = false;   // se fija en renderVista: la combinación peso–edad–FCR del escenario activo es incoherente
  const TAG_MAT = '<span class="estado matematico" tabindex="0" title="Escenario matemático. La combinación peso–edad–FCR requiere validación zootécnica.">Escenario matemático</span>';
  const badgeProd = (ref) => badge("supuesto", ref) + (ESC_MAT ? " " + TAG_MAT : "");
  const badge = (tipo, ref) => tipo === "prod" ? badgeProd(ref) : `<span class="estado ${tipo}" tabindex="0" title="${esc(ESTADOS[tipo].tip + (ref ? " — " + ref : ""))}">${ESTADOS[tipo].corto}</span>`;
  const PER = {
    op: '<span class="periodo op" title="Día con faena (250 o 300 por año)">por día operativo</span>',
    cal: '<span class="periodo cal" title="Cualquier día del año (365). La demanda se expresa así.">por día calendario</span>',
    anio: '<span class="periodo">por año</span>',
    semp: '<span class="periodo" title="Semana sin feriados, con todos los días de faena: dimensiona granjas y pollitos">semana plena</span>',
    semprom: '<span class="periodo" title="Total anual ÷ 52,14 (incluye feriados)">semana promedio</span>',
    stock: '<span class="periodo" title="Cantidad simultánea (no es un flujo)">en simultáneo</span>',
    hora: '<span class="periodo">por hora neta</span>',
    ave: '<span class="periodo">por ave</span>',
  };
  const tip = (t) => `<span class="tip" tabindex="0" role="note" aria-label="${esc(t)}" data-tip="${esc(t)}">i</span>`;

  // ============================================================================================
  // Explicaciones "¿Qué significa esto?" (contenido de las guías de Ramiro)
  // ============================================================================================
  const EXPLICA = {
    resumen: {
      titulo: "¿Qué muestra este resumen?",
      cuerpo: `<p>El simulador responde <strong>«¿qué tiene que ser verdad para que esta escala tenga sentido?»</strong>: cuántos pollitos, cuántos m² de galpón, cuánto alimento, cuánto producto y cuántos subproductos salen, y cuánta demanda haría falta para colocarlos.</p>
        <ul><li><strong>Escala</strong> = aves que la planta puede faenar por día de faena a su capacidad operativa (100 %).</li>
        <li><strong>Aves procesadas</strong> = escala × utilización supuesta. Todos los volúmenes se calculan con esta cifra.</li>
        <li>Todo es <strong>física</strong>: no hay precios, costos ni rentabilidad. <strong>Capacidad no es ventas.</strong></li></ul>
        <p>La respuesta honesta hoy es: <em>«no sabemos todavía cuál es la escala; sabemos qué datos la deciden»</em>.</p>`,
      fuente: "23_plan_expansion/guia_ramiro.md §1–§2",
    },
    metricas: {
      titulo: "Capacidad instalada, utilización asumida, utilización requerida y cobertura",
      cuerpo: `<ul><li><strong>Capacidad instalada</strong> = aves/día máximas del escenario (la escala).</li>
        <li><strong>Utilización operativa asumida</strong> = el porcentaje que <em>vos</em> elegís para simular cuánto se procesa realmente. <strong>Producción simulada</strong> = capacidad instalada × utilización asumida.</li>
        <li><strong>Factor demanda/capacidad instalada</strong> = capacidad requerida por la demanda ÷ capacidad instalada. <strong>Puede</strong> pasar de 100 %: 143 % quiere decir que la planta no alcanza.</li>
        <li><strong>Utilización requerida por demanda</strong> = mínimo entre ese factor y 100 %. La calcula el modelo; no se elige.</li>
        <li><strong>Cobertura con la producción simulada</strong> = producción simulada ÷ capacidad requerida (hasta 100 %). <strong>Cobertura máxima a plena capacidad</strong> = capacidad instalada ÷ capacidad requerida (hasta 100 %). Son dos números distintos y no se mezclan.</li>
        <li><strong>Capacidad ociosa operativa</strong> = capacidad instalada − producción simulada. <strong>Capacidad disponible respecto de la demanda</strong> = capacidad instalada − capacidad requerida por la demanda.</li></ul>
        <p><strong>Ejemplo:</strong> planta de 10.000 aves/día, utilización asumida 50 % → producción simulada 5.000. Si la demanda requiere 8.000 aves/día, la capacidad instalada sí alcanza (factor 80 %, utilización requerida 80 %), pero con 50 % se cubre solo el 62,5 % de la demanda. Capacidad ociosa operativa: 5.000; capacidad disponible respecto de la demanda: 2.000.</p>
        <p>La demanda está en <strong>kg por día calendario</strong>; la capacidad en <strong>aves por día operativo</strong>. Solo se comparan después de convertir (× días de faena / 365).</p>`,
      fuente: "23_plan_expansion/guia_ramiro.md concepto 2 · escenarios_escala.md §4.3 · SUP-060 · auditoría semántica v0.1",
    },
    dias: {
      titulo: "Día de faena (operativo) vs día calendario",
      cuerpo: `<p>La planta produce en <strong>días de faena</strong> (250 o 300 por año); la gente come y los supermercados venden los <strong>365 días del calendario</strong>. A 10.000 aves/día y 250 días salen 24 t de producto por día de faena, pero en promedio son 16,4 t por día calendario.</p>
        <p><strong>La demanda se compara con la producción en la misma base</strong>, siempre convirtiendo (× 250 / 365). Lo mismo con el stock: 7 días de faena en cámara (168 t) no son 7 días calendario de ventas (115 t).</p>
        <p>El <strong>sexto día</strong> (250 → 300 días/año) da ~20 % más de volumen <em>anual</em> con la <em>misma</em> capacidad por día. El <strong>segundo turno</strong> actúa sobre las horas por día y solo sirve si el resto de la planta acompaña.</p>`,
      fuente: "23_plan_expansion/guia_ramiro.md conceptos 10–11",
    },
    masa: {
      titulo: "Masa biológica, agua retenida y peso comercial",
      cuerpo: `<p>El pollo enfriado en agua (chiller por inmersión) absorbe un poco: de las 24 t/día que se venden a 10.000 aves/día, ~23,1 t son carne y tejidos (<strong>masa biológica</strong>) y ~0,9 t son <strong>agua retenida</strong>. Se vende el <strong>peso comercial</strong> (las dos cosas juntas), pero el agua <strong>nunca</strong> es carne producida.</p>
        <p>En Argentina la absorción tendría un tope de <strong>8 %</strong> (según prensa y normas a verificar: PVDP). Para comparar plantas o proveedores, <strong>comparar siempre sin agua</strong>. Esta agua no es el agua que consume la planta para lavar, escaldar y limpiar, que se calculará aparte.</p>`,
      fuente: "04_balance_masa/guia_ramiro.md §6 · 23_plan_expansion/guia_ramiro.md concepto 12 · SUP-042",
    },
    demanda: {
      titulo: "¿Cómo se lee la demanda?",
      cuerpo: `<p>Hoy la demanda documentada es <strong>prácticamente cero</strong>: los 90 supermercados son potenciales, los escenarios comerciales son hipótesis de orden de magnitud, sin evidencia comercial y la exportación no tiene ni un importador identificado.</p>
        <p>No alcanza con que compren «kilos»: tienen que comprar <strong>todas las partes</strong> del pollo o hay que encontrar a quién venderle el resto. Por eso hay dos formas de convertir kg en aves:</p>
        <ul><li><strong>M0 · ave completa</strong>: se supone que toda la masa comestible del ave se vende dentro de la demanda. Da el <em>mínimo</em> de aves.</li>
        <li><strong>M1–M3 · parte limitante</strong>: con un mix de supermercado (entero dominante / trozado / valor agregado) la parte más pedida (casi siempre la pechuga) fija las aves, y <strong>sobran</strong> pata-muslo, alas, carcasa, cuello y garras.</li></ul>
        <p>El dato que más cambiaría la decisión de escala: las compras reales de la red por producto y por semana, con precio y plazo (DPV-003, DPV-037).</p>`,
      fuente: "23_plan_expansion/guia_ramiro.md concepto 9 y pregunta 6 · escenarios_escala.md §4.2 · SUP-054",
    },
    produccion: {
      titulo: "La granja: una fábrica biológica de kg vivo",
      cuerpo: `<ul><li><strong>Pollitos alojados ≠ aves faenadas.</strong> Entre ambos están la mortalidad en granja (3–8 %) y la del transporte (0,2–0,5 %). Para faenar 10.000 aves hay que alojar ~10.558 pollitos (escenario medio).</li>
        <li><strong>El alimento lo gobierna el FCR:</strong> alimento = kg vivo × FCR. Empeorar 0,1 el FCR = +5,9 % de alimento. Un ave más pesada siempre convierte peor.</li>
        <li><strong>Plazas ≠ producción anual:</strong> producción = plazas × ciclos/año × supervivencia. Con 47 días de crianza + vacío sanitario salen ~5,7 ciclos por año, no 7,8.</li>
        <li><strong>La densidad se mide en kg/m² al final</strong>: 30 vs 39 kg/m² cambia 23 % los m² necesarios, pero la limitan el bienestar, el clima y el galpón.</li>
        <li><strong>Semana plena vs promedio:</strong> las granjas se dimensionan para la semana sin feriados.</li>
        <li><strong>Propias, integrados o compra</strong> no es una decisión técnica sino de capital, control y riesgo (DEC-020, sin ganador).</li></ul>`,
      fuente: "03_produccion_primaria/guia_ramiro.md §1 · SUP-026 · SUP-028",
    },
    planta: {
      titulo: "Capacidad, ritmo de línea y cuello de botella",
      cuerpo: `<ul><li><strong>Capacidad nominal</strong>: lo que la planta podría hacer «en los papeles» (velocidad de la línea × horas). <strong>Capacidad operativa</strong>: lo que puede sostener día tras día con su gente, su frío, sus efluentes y sus pollos. La escala del simulador es la operativa.</li>
        <li><strong>Ritmo de línea</strong> = aves por día ÷ horas <em>netas</em> de faena. No incluye eficiencia de máquina (ningún equipo está relevado).</li>
        <li><strong>Cuello de botella</strong>: la operación más lenta fija la capacidad de todo (línea, enfriado, deshuese, túnel, cámaras, efluentes… o falta de pollos).</li>
        <li><strong>Segundo turno = capacidad teórica de la línea, no de la planta</strong>: 1.250 aves/h son 10.000 aves/día con 8 h netas o 20.000 con 16 h, solo si frío, efluentes, agua, energía, personal, limpieza y pollos acompañan.</li></ul>`,
      fuente: "23_plan_expansion/guia_ramiro.md conceptos 1, 3, 10 · 05_proceso_industrial/capacidad_preliminar.md",
    },
    productos: {
      titulo: "Producto, coproducto, subproducto y residuo",
      cuerpo: `<p>Un pollo se «desarma» y cada kilo tiene un destino. De un pollo de 2,9 kg salen ~2,3 kg comestibles (≈ 80 %), ~0,44 kg de subproductos no comestibles (≈ 15 %) y ~0,14 kg de residuos y pérdidas (≈ 5 %).</p>
        <ul><li><strong>Producto principal</strong>: lo que define el negocio (entero, pechuga, pata-muslo, suprema).</li>
        <li><strong>Coproducto</strong>: comestible, sale sí o sí junto con el principal y vale menos por kg (alas, menudencias, cuello, garras, carcasa).</li>
        <li><strong>Subproducto</strong>: no se come pero puede valer si alguien lo procesa (plumas, sangre, vísceras, huesos).</li>
        <li><strong>Residuo</strong>: no vale o cuesta tratarlo.</li></ul>
        <p><strong>La categoría depende de que haya comprador.</strong> Todas las partes salen juntas: si vendés más pechuga, igual vas a tener que colocar las patas-muslo, alas, carcasas y menudencias de esos pollos. <strong>Una parte sin comprador baja el ingreso de todo el pollo.</strong></p>
        <p>Cuidado con los porcentajes: la pechuga con hueso es ~38 % de la <em>carcasa</em> pero ~27 % del <em>peso vivo</em>. Siempre preguntar «¿rendimiento de qué, sobre qué?».</p>`,
      fuente: "07_subproductos/guia_ramiro.md §1 y §6 · 04_balance_masa/guia_ramiro.md §2–§5",
    },
    subproductos: {
      titulo: "Rendering, plumas, sangre y garras",
      cuerpo: `<ul><li><strong>Rendering</strong>: una «fábrica de harinas» que cocina, esteriliza y seca lo que no se come y lo convierte en harinas proteicas y grasa para alimento animal. Tener uno propio es <strong>otra industria</strong> (caldera, olores, permisos). Primero hay que saber si hay uno cerca que retire los subproductos y cuánto paga o cobra.</li>
        <li><strong>Plumas</strong>: el subproducto más pesado (~240 g húmedas por pollo). Si un rendering las compra, son ingreso; si las retira gratis, cero; si hay que pagar para disponerlas, costo. Por eso <strong>dónde se instala la planta</strong> importa.</li>
        <li><strong>Sangre y vísceras</strong> se degradan en horas: hay que retirarlas todos los días de faena, en cualquier escala. Recuperar la sangre reduce mucho la carga del efluente.</li>
        <li><strong>Garras</strong>: en Argentina casi no se comen; en China se pagaron como un corte, pero China no está confirmada como abierta. A 2.500 pollos/día un contenedor de garras tarda ~6 meses en llenarse.</li></ul>`,
      fuente: "07_subproductos/guia_ramiro.md §2, §4, §5 · escenarios_escala.md §10",
    },
    inventario: {
      titulo: "Días de producción en stock vs días calendario de cobertura",
      cuerpo: `<ul><li><strong>Días de producción en stock</strong> = producción por día <em>operativo</em> × días. Responde «¿cuántas jornadas de faena caben en la cámara?».</li>
        <li><strong>Días calendario de cobertura</strong> = despacho promedio por día <em>calendario</em> × días. Responde «¿cuántos días de venta cubre el stock?».</li></ul>
        <p>Con 250 días de faena, 7 días calendario de cobertura equivalen a ~4,8 días de producción. El producto refrigerado vive <strong>días</strong>: su inventario es corto. El congelado y la exportación <strong>acumulan</strong>. El inventario es capital de trabajo físico y depende más del <strong>canal y el perfil de destino</strong> que de la escala. Un fin de semana sin faena exige cubrir 2–3 días calendario de despacho.</p>`,
      fuente: "escenarios_escala.md §11 · SUP-051 · SUP-055 · SUP-056",
    },
    comparador: {
      titulo: "¿Por qué no construir directamente 20.000 pollos por día?",
      cuerpo: `<p>No es «porque lo dijo el modelo». Para operar una escala grande tiene que ser verdad <strong>todo esto a la vez</strong>: alguien compra el producto; alguien compra <strong>cada parte</strong>; hay pollitos; hay dónde criarlos; hay alimento; hay a quién darle los subproductos todos los días; hay frío y logística; hay capital. Hoy nada de eso está demostrado.</p>
        <p>Una planta de 20.000 al 50 % faena lo mismo que una de 10.000 llena, pero paga como una de 20.000. <strong>El argumento también vale al revés</strong>: tampoco es obvio empezar con 2.500 (podría no alcanzar para la demanda base y no sabemos si está por encima de la escala mínima eficiente).</p>
        <p><strong>La aspiración define la reserva; la evidencia define la construcción.</strong> El comparador no declara ganador: muestra qué cambia físicamente.</p>`,
      fuente: "23_plan_expansion/guia_ramiro.md §2",
    },
    estados: {
      titulo: "¿Por qué los datos tienen distinto color?",
      cuerpo: `<p>No todos los números tienen la misma certeza. Cada cifra lleva una etiqueta:</p>
        <ul><li>${badge("modelo")} fórmula verificada contra los modelos aprobados; no es una medición real.</li>
        <li>${badge("supuesto")} depende de un supuesto de trabajo registrado (SUP-###).</li>
        <li>${badge("pvdp")} depende de fuentes que todavía no se leyeron en su documento original.</li>
        <li>${badge("campo")} falta un dato que solo se consigue en campo (DPV-###).</li></ul>
        <p><strong>Calculado por modelo significa que la fórmula y su consistencia matemática fueron verificadas. No significa que el valor haya sido validado en una planta real.</strong></p>`,
      fuente: "CLAUDE.md reglas 4, 5 y 16",
    },
  };
  const explica = (k) => {
    const e = EXPLICA[k];
    return `<details class="explica"><summary>¿Qué significa esto?</summary><div class="explica-cuerpo"><strong>${e.titulo}</strong>${e.cuerpo}<div class="fuente">Fuente: ${esc(e.fuente)}</div></div></details>`;
  };

  // ============================================================================================
  // Estado de la aplicación (escenarios A/B/C independientes; persistencia local opcional)
  // ============================================================================================
  const CLAVE_LS = "simulador_avicola_v01";
  const PESTANAS = [["resumen", "Resumen"], ["demanda", "Demanda"], ["produccion", "Producción"], ["planta", "Planta"],
    ["productos", "Productos"], ["subproductos", "Subproductos"], ["inventario", "Inventario"], ["comparador", "Comparador"],
    ["supuestos", "Supuestos"], ["economia", "Economía del proyecto"]];
  let estado = S.estadoInicial(DATA);
  let ui = { pestana: "resumen", tema: "auto", panel: false };

  function normalizar(guardado) {
    const est = S.estadoInicial(DATA);
    if (!guardado || !guardado.escenarios) return est;
    S.SLOTS.forEach((s) => {
      if (guardado.escenarios[s] && typeof guardado.escenarios[s] === "object") {
        const base = S.entradasPorDefecto(DATA, `Escenario ${s}`);
        Object.keys(base).forEach((k) => { if (k in guardado.escenarios[s]) base[k] = guardado.escenarios[s][k]; });
        est.escenarios[s] = base;
      }
    });
    if (S.SLOTS.includes(guardado.activo)) est.activo = guardado.activo;
    return est;
  }
  function cargar() {
    try {
      const t = localStorage.getItem(CLAVE_LS);
      if (!t) return;
      const g = JSON.parse(t);
      estado = normalizar(g.estado);
      if (g.ui && PESTANAS.some((p) => p[0] === g.ui.pestana) && g.ui.pestana !== "economia") ui.pestana = g.ui.pestana;
      if (g.ui && ["auto", "light", "dark"].includes(g.ui.tema)) ui.tema = g.ui.tema;
    } catch (e) { /* almacenamiento no disponible: se usan los valores por defecto */ }
  }
  function guardar() {
    try { localStorage.setItem(CLAVE_LS, JSON.stringify({ estado, ui: { pestana: ui.pestana, tema: ui.tema } })); } catch (e) { /* sin persistencia */ }
  }

  const act = () => estado.escenarios[estado.activo];
  const resultados = {};
  function recalcular() { S.SLOTS.forEach((s) => { resultados[s] = S.calcular(DATA, estado.escenarios[s]); }); }

  // ============================================================================================
  // Panel de entradas
  // ============================================================================================
  function opcionesPeso(v) {
    const [lo, hi] = P.rango_peso;
    let h = "";
    for (let i = 0; i <= Math.round((hi - lo) / P.paso_peso); i++) {
      const p = +(lo + i * P.paso_peso).toFixed(1);
      const fuera = p < Math.min(...P.pesos_estudiados) - 1e-9 || p > Math.max(...P.pesos_estudiados) + 1e-9;
      h += `<option value="${p}"${Math.abs(p - v) < 1e-9 ? " selected" : ""}>${fmt(p, 1)} kg${Math.abs(p - P.peso_ref) < 1e-9 ? " (referencia)" : ""}${fuera ? " · extrapolación" : ""}</option>`;
    }
    return h;
  }
  function opcionesDemanda() {
    const com = DATA.demanda.escenarios.filter((d) => d.bloque === "escenario_comercial");
    const red = DATA.demanda.escenarios.filter((d) => d.bloque === "red_supermercados");
    return `<optgroup label="Escenarios comerciales (hipótesis)">${com.map((d) => `<option value="${d.id}">${esc(d.nombre)} · ${fmt(d.total_kg_dia)} kg/día cal.</option>`).join("")}</optgroup>
      <optgroup label="Red de ${DATA.demanda.locales} supermercados (hipótesis)">${red.map((d) => `<option value="${d.id}">${esc(d.nombre)} · ${fmt(d.total_kg_dia)} kg/día</option>`).join("")}</optgroup>
      <optgroup label="Otros"><option value="CERO">Solo demanda documentada actual (≈ 0: no validada)</option><option value="MANUAL">Manual (ingresar kg/día calendario)</option></optgroup>`;
  }
  function descMix(m) {
    const mix = DATA.demanda.mixes[m];
    return Object.keys(mix).map((k) => `${k.split(" (")[0]} ${fmt(mix[k] * 100)} %`).join(" · ");
  }
  const campo = (rotulo, control, ayuda, tipTxt) =>
    `<div class="campo"><div class="rotulo"><span>${rotulo}</span>${tipTxt ? tip(tipTxt) : ""}</div>${control}${ayuda ? `<div class="ayuda">${ayuda}</div>` : ""}</div>`;
  const num = (k, min, max, step, extra) => `<input type="number" data-k="${k}" min="${min}" max="${max}" step="${step}" ${extra || ""}>`;
  const chips = (k, pares, numerico) => `<div class="chips">${pares.map(([v, t]) => `<button type="button" class="chip" data-accion="set" data-k="${k}" data-v="${v}"${numerico ? ' data-num="1"' : ""}>${t}</button>`).join("")}</div>`;

  function formHTML() {
    const e = act();
    return `
    <div class="campo"><label for="nombre-esc">Nombre del escenario ${estado.activo}</label><input type="text" id="nombre-esc" data-k="nombre" maxlength="40"></div>
    <fieldset class="grupo"><legend>Lo esencial</legend>
      ${campo("Escala (aves faenadas por día operativo)", chips("escala", P.escalas.map((x) => [x, fmt(x)]), true) +
        `<div class="en-linea" style="margin-top:6px"><span class="pequeno muted">Otra:</span>${num("escala", 2500, 20000, 100, 'data-rango="2500,20000" id="escala-simple"')}<span class="pequeno muted">2.500–20.000</span></div>
        <div class="ayuda" id="aviso-escala-simple" hidden>Fuera del rango principal estudiado: usar «Parámetros avanzados».</div>`,
        "Rango principal estudiado: 2.500–20.000.", "CAPACIDAD INSTALADA: aves máximas por día de faena del escenario (capacidad operativa al 100 %). No es una recomendación (SUP-052).")}
      ${campo("Utilización operativa asumida", `<div class="en-linea"><input type="range" data-k="utilizacion" data-escala="100" min="10" max="100" step="5">${num("utilizacion", 10, 100, 1, 'data-escala="100"')}<span>%</span></div>`,
        "La elegís vos: producción simulada = capacidad instalada × este %. No es la utilización requerida por la demanda.", "UTILIZACIÓN OPERATIVA ASUMIDA: porcentaje elegido manualmente para simular cuánto se procesa realmente. La utilización REQUERIDA por la demanda la calcula el modelo y se muestra aparte. 100 % es el punto de dimensionamiento, no un supuesto de operación.")}
      ${campo("Peso vivo del pollo", `<select data-k="peso" data-num="1">${opcionesPeso(e.peso)}</select>`, "Rango principal estudiado: 2,2–3,5 kg. El motor admite 2,0–3,8 kg (fuera del principal = extrapolación).", "Peso vivo en granja = en planta (SUP-058). Cambia rendimientos, alimento y m². Perfil medio: 2,9 kg a 47 días (SUP-027).")}
      ${campo("Días de faena por año", `<div class="chips"><button type="button" class="chip" data-accion="calendario" data-ds="5">250 días · 5 d/sem</button><button type="button" class="chip" data-accion="calendario" data-ds="6">300 días · 6 d/sem</button></div><div class="ayuda" id="dias-actual"></div>`,
        "", "Días OPERATIVOS (con faena) por año, descontados feriados (SUP-025). Otro valor: en «Parámetros avanzados».")}
      ${campo("Escenario de demanda", `<select data-k="demanda_id">${opcionesDemanda()}</select>`, "Hipótesis de prueba, no ventas (SUP-021).", "Demanda en kg de producto comercial por DÍA CALENDARIO. Ningún escenario tiene evidencia comercial.")}
      <div id="campo-manual">${campo("Demanda manual (kg de producto por día calendario)", num("demanda_manual_kg", 0, 200000, 100))}</div>
      ${campo("Configuración comercial", chips("config", [["A", NOMBRE_CONFIG.A], ["B", NOMBRE_CONFIG.B], ["C", NOMBRE_CONFIG.C]]),
        "Referencia: trozado (SUP-050); no es una decisión.", "Cómo se vende la carcasa: entera, en cortes con hueso (trozado) o deshuesada con separación mecánica (CMS). Cambia productos, coproductos y subproductos. No confundir con los escenarios A/B/C del comparador.")}
      ${campo("Inventario", `<div class="en-linea">${num("dias_inventario", 1, 30, 1)}<span>días de</span></div>` +
        `<div class="chips" style="margin-top:6px"><button type="button" class="chip" data-accion="set" data-k="base_inventario" data-v="dias_produccion">producción en stock</button><button type="button" class="chip" data-accion="set" data-k="base_inventario" data-v="dias_calendario">calendario de cobertura</button></div>`,
        "", "Días de PRODUCCIÓN en stock (jornadas de faena en cámara) o días CALENDARIO de cobertura (días de venta). Son cantidades distintas (SUP-056).")}
    </fieldset>
    <details class="avanzado" id="avanzado"${ui.avanzado ? " open" : ""}><summary>Parámetros avanzados</summary>
      <fieldset class="grupo"><legend>Escala fuera del rango principal</legend>
        ${campo("Capacidad instalada (aves/día operativo)", num("escala", 500, 30000, 100), "500–30.000. Fuera de 2.500–20.000: ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO (extrapolación física, no escala analizada en profundidad).")}
      </fieldset>
      <fieldset class="grupo"><legend>Calendario y línea</legend>
        <div class="fila-2">
          ${campo("Días/semana", `<select data-k="dias_semana" data-num="1"><option value="5">5</option><option value="6">6</option></select>`)}
          ${campo("Días/año", num("dias_anio", 1, 313, 1), "", "Días de faena por año; máximo = días/semana × 52,14. Al cambiar días/semana se repone el calendario de referencia (250/300).")}
        </div>
        ${campo("Horas netas de faena por día", chips("horas_netas", [[6, "6 h"], [8, "8 h"], [10, "10 h"], [16, "16 h (2 turnos)"]], true) +
          `<div class="en-linea" style="margin-top:6px">${num("horas_netas", 4, 20, 0.5)}<span class="pequeno muted">h netas (4–20)</span></div>`, "", "Horas efectivas de faena (no horas de turno). Solo cambia el ritmo de línea (SUP-053).")}
      </fieldset>
      <fieldset class="grupo"><legend>Producción primaria</legend>
        <div class="fila-2">
          ${campo("Perfil de mercado", `<select data-accion="perfil"><option value="">personalizado</option>${Object.keys(P.produccion.perfiles).map((k) => `<option value="${k}">${k} (${fmt(P.produccion.perfiles[k].peso, 1)} kg · ${P.produccion.perfiles[k].edad} d)</option>`).join("")}</select>`, "", "Fija peso, edad y FCR base (SUP-027, SUP-028).")}
          ${campo("Nivel de desempeño", `<select data-accion="desempeno"><option value="">personalizado</option>${Object.keys(P.produccion.desempenos).map((k) => `<option value="${k}">${k}</option>`).join("")}</select>`, "", "Fija mortalidad, DOA, días entre lotes, densidad y ajuste de FCR (SUP-026).")}
        </div>
        <div class="fila-2">
          ${campo("Edad de faena (d)", num("edad", 35, 56, 1))}
          ${campo("Mortalidad granja (%)", num("mortalidad", 0, 15, 0.1, 'data-escala="100"'))}
          ${campo("FCR de campo", num("fcr", 1.4, 2.2, 0.01), "", "kg de alimento por kg vivo cargado; incluye el alimento de las aves muertas (SUP-028).")}
          ${campo("Mortalidad transporte (%)", num("doa", 0, 2, 0.05, 'data-escala="100"'))}
          ${campo("Días entre lotes", num("vacio", 8, 30, 1), "", "Captura, limpieza, desinfección, vacío sanitario y preparación.")}
          ${campo("Densidad final (kg/m²)", num("kg_m2", 25, 45, 0.5))}
        </div>
      </fieldset>
      <fieldset class="grupo"><legend>Demanda y mix comercial</legend>
        ${campo("Conversión de la demanda en aves", `<select data-k="metodo"><option value="M0">M0 · ave completa (mínimo de aves)</option><option value="M1">M1 · mix entero dominante</option><option value="M2">M2 · mix trozado</option><option value="M3">M3 · mix valor agregado</option></select>`,
          `<span id="desc-mix"></span>`, "M0 supone que se vende toda el ave. M1–M3 usan mixes hipotéticos de supermercado (SUP-023): la parte más pedida fija las aves y sobran otras partes (SUP-054).")}
      </fieldset>
      <fieldset class="grupo"><legend>Inventario</legend>
        ${campo("Perfil de destino", `<select data-k="perfil_destino">${Object.keys(P.perfiles_destino).map((k) => `<option value="${k}">${k} · ${esc(P.perfiles_destino[k].nombre)}</option>`).join("")}</select>`, "Ilustrativo (SUP-055); la exportación de la demanda es 0.")}
        ${campo("Días de congelado y exportación", num("dias_congelado", 1, 30, 1), "El refrigerado usa los días de inventario de arriba.")}
      </fieldset>
      <fieldset class="grupo"><legend>Abastecimiento de aves</legend>
        ${campo("Granjas propias (% de los m²)", chips("pct_propio", [[0, "Integrados"], [0.5, "Mixto 50 %"], [1, "Propias"]], true) +
          `<div class="en-linea" style="margin-top:6px">${num("pct_propio", 0, 100, 5, 'data-escala="100"')}<span>% propio</span></div>`, "Sin ganador (DEC-020).")}
        ${campo("m² de galpón por productor integrado", num("m2_por_productor", 100, 200000, 100, 'data-nullable="1" placeholder="vacío = dato pendiente"'), "Vacío: dato de campo pendiente (DPV-048).")}
      </fieldset>
      <fieldset class="grupo"><legend>Vehículos (vacío = sin dato)</legend>
        <div class="fila-2">
          ${campo("Aves por camión", num("aves_por_camion", 500, 20000, 100, 'data-nullable="1" placeholder="4.000–7.000"'), "", "SUP-033: 4.000–7.000, sin fuente.")}
          ${campo("t por camión refrigerado", num("cap_camion_frio_t", 0.5, 60, 0.5, 'data-nullable="1" placeholder="DPV-084"'))}
          ${campo("t por camión de alimento", num("cap_camion_alimento_t", 1, 60, 0.5, 'data-nullable="1" placeholder="DPV-084"'))}
          ${campo("t por retiro de subproductos", num("cap_camion_sub_t", 0.5, 60, 0.5, 'data-nullable="1" placeholder="DPV-084"'))}
        </div>
      </fieldset>
    </details>
    <fieldset class="grupo"><legend>Escenario ${estado.activo}</legend>
      <div class="acciones-escenario">
        ${S.SLOTS.filter((s) => s !== estado.activo).map((s) => `<button type="button" class="btn-sec" data-accion="copiar" data-a="${s}">Copiar a ${s}</button>`).join("")}
        <button type="button" class="btn-sec" data-accion="restablecer">Restablecer</button>
      </div>
      <div class="acciones-escenario">
        <button type="button" class="btn-sec" data-accion="exportar">Exportar A/B/C</button>
        <label class="btn-sec" style="display:inline-flex;align-items:center">Importar<input type="file" accept="application/json,.json" data-accion="importar" hidden></label>
      </div>
      <p class="nota-entrada">Cada escenario guarda sus propios parámetros en este navegador. «Exportar» descarga un archivo para compartir o guardar.</p>
    </fieldset>`;
  }

  function perfilActual(e) {
    const pr = P.produccion.perfiles;
    return Object.keys(pr).find((k) => Math.abs(pr[k].peso - e.peso) < 1e-9 && pr[k].edad === e.edad) || "";
  }
  function desempenoActual(e) {
    const d = P.produccion.desempenos;
    return Object.keys(d).find((k) => Math.abs(d[k].mort - e.mortalidad) < 1e-9 && Math.abs(d[k].doa - e.doa) < 1e-9 && d[k].vacio === e.vacio && d[k].kg_m2 === e.kg_m2) || "";
  }

  function syncForm(excepto) {
    const e = act();
    document.querySelectorAll("#panel-entradas [data-k]").forEach((el) => {
      if (el === excepto) return;
      const k = el.dataset.k, v = e[k];
      if (el.classList.contains("chip")) {
        const cv = el.dataset.num ? Number(el.dataset.v) : el.dataset.v;
        el.setAttribute("aria-pressed", String(cv === v || (typeof v === "number" && Math.abs(cv - v) < 1e-9)));
        return;
      }
      const esc100 = Number(el.dataset.escala || 1);
      if (v === null || v === undefined) el.value = "";
      else if (typeof v === "number") el.value = Number.isFinite(v) ? String(+(v * esc100).toFixed(4)) : "";
      else el.value = v;
    });
    document.querySelectorAll('#panel-entradas [data-accion="calendario"]').forEach((b) => {
      const ds = Number(b.dataset.ds);
      b.setAttribute("aria-pressed", String(e.dias_semana === ds && e.dias_anio === P.calendarios[String(ds)]));
    });
    const sp = document.querySelector('[data-accion="perfil"]'); if (sp) sp.value = perfilActual(e);
    const sd = document.querySelector('[data-accion="desempeno"]'); if (sd) sd.value = desempenoActual(e);
    const da = $("#dias-actual");
    if (da) da.textContent = `Actual: ${fmt(e.dias_anio)} días/año con ${e.dias_semana} días/semana` + (e.dias_anio !== P.calendarios[String(e.dias_semana)] ? " (personalizado)" : "");
    const cm = $("#campo-manual"); if (cm) cm.hidden = e.demanda_id !== "MANUAL";
    const dm = $("#desc-mix"); if (dm) dm.textContent = e.metodo === "M0" ? "Toda la masa comestible del ave se vende dentro de la demanda." : descMix(e.metodo);
  }

  function renderPanel() {
    $("#panel-entradas").innerHTML = formHTML();
    syncForm();
  }

  function cambiar(k, v, excepto) {
    estado = S.conEntrada(estado, estado.activo, k, v);
    if (k === "dias_semana" && P.calendarios[String(v)]) estado = S.conEntrada(estado, estado.activo, "dias_anio", P.calendarios[String(v)]);
    actualizar(excepto);
  }
  function cambiarVarios(obj) {
    Object.keys(obj).forEach((k) => { estado = S.conEntrada(estado, estado.activo, k, obj[k]); });
    actualizar();
  }

  function leerValor(el) {
    if (el.tagName === "SELECT") return el.dataset.num ? Number(el.value) : el.value;
    if (el.type === "number" || el.type === "range") {
      if (el.value.trim() === "") return el.dataset.nullable ? null : NaN;
      return Number(el.value.replace(",", ".")) / Number(el.dataset.escala || 1);
    }
    return el.value;
  }

  function enlazarPanel() {
    const panel = $("#panel-entradas");
    panel.addEventListener("input", (ev) => {
      const el = ev.target;
      if (!el.dataset.k || el.tagName === "SELECT") return;
      if (el.dataset.rango) {
        const [lo, hi] = el.dataset.rango.split(",").map(Number), v = leerValor(el);
        const fuera = !(v >= lo && v <= hi);
        $("#aviso-escala-simple").hidden = !fuera;
        el.setCustomValidity(fuera ? "Fuera del rango principal estudiado" : "");
        if (fuera) return;
      }
      cambiar(el.dataset.k, leerValor(el), el);
    });
    panel.addEventListener("change", (ev) => {
      const el = ev.target;
      if (el.dataset.accion === "perfil" && el.value) {
        const pr = P.produccion.perfiles[el.value], d = P.produccion.desempenos[desempenoActual(act()) || "medio"];
        cambiarVarios({ peso: pr.peso, edad: pr.edad, fcr: +(pr.fcr_base + d.d_fcr).toFixed(2) });
      } else if (el.dataset.accion === "desempeno" && el.value) {
        const d = P.produccion.desempenos[el.value], pr = P.produccion.perfiles[perfilActual(act()) || "medio"];
        cambiarVarios({ mortalidad: d.mort, doa: d.doa, vacio: d.vacio, kg_m2: d.kg_m2, fcr: +(pr.fcr_base + d.d_fcr).toFixed(2) });
      } else if (el.dataset.accion === "importar" && el.files && el.files[0]) {
        const fr = new FileReader();
        fr.onload = () => {
          try { estado = normalizar(JSON.parse(fr.result)); renderTodo(); } catch (e) { alert("El archivo no es un conjunto de escenarios válido."); }
        };
        fr.readAsText(el.files[0]);
      } else if (el.tagName === "SELECT" && el.dataset.k) cambiar(el.dataset.k, leerValor(el));
    });
    panel.addEventListener("click", (ev) => {
      const b = ev.target.closest("[data-accion]");
      if (!b || b.tagName === "SELECT" || b.tagName === "INPUT") return;
      const a = b.dataset.accion;
      if (a === "set") cambiar(b.dataset.k, b.dataset.num ? Number(b.dataset.v) : b.dataset.v);
      else if (a === "calendario") { const ds = Number(b.dataset.ds); cambiarVarios({ dias_semana: ds, dias_anio: P.calendarios[String(ds)] }); }
      else if (a === "copiar") {
        if (confirm(`¿Reemplazar los parámetros del escenario ${b.dataset.a} por los de ${estado.activo}?`)) { estado = S.copiarEscenario(estado, estado.activo, b.dataset.a); renderTodo(); }
      } else if (a === "restablecer") {
        if (confirm(`¿Restablecer el escenario ${estado.activo} a los valores por defecto?`)) {
          const def = S.estadoInicial(DATA).escenarios[estado.activo];
          estado = S.clonar(estado); estado.escenarios[estado.activo] = def; renderTodo();
        }
      } else if (a === "exportar") {
        const blob = new Blob([JSON.stringify({ simulador: "v" + DATA.meta.simulador_version, fecha: new Date().toISOString().slice(0, 10), activo: estado.activo, escenarios: estado.escenarios }, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const lnk = document.createElement("a");
        lnk.href = url; lnk.download = "escenarios_simulador_avicola.json"; document.body.appendChild(lnk); lnk.click(); lnk.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
      }
    });
    panel.addEventListener("toggle", (ev) => { if (ev.target.id === "avanzado") ui.avanzado = ev.target.open; }, true);
  }

  // ============================================================================================
  // Selector de escenarios, pestañas, alertas
  // ============================================================================================
  function renderSelector() {
    $("#selector-escenarios").innerHTML = S.SLOTS.map((s) => {
      const e = estado.escenarios[s], r = resultados[s];
      const av = r.ok ? r.alertas.filter((a) => a.nivel === "aviso").length : 0;
      return `<button type="button" role="tab" class="tab-escenario" data-slot="${s}" aria-selected="${s === estado.activo}">
        <span class="letra">${s}</span><span>${esc(e.nombre)}</span>
        <span class="det">${Number.isFinite(e.escala) ? fmt(e.escala) : "—"} aves/día · ${r.ok ? `${av} aviso${av === 1 ? "" : "s"}` : "entradas inválidas"}</span></button>`;
    }).join("");
  }
  function renderPestanas() {
    $("#pestanas").innerHTML = PESTANAS.map(([k, t]) =>
      `<button type="button" role="tab" data-p="${k}" aria-selected="${ui.pestana === k}"${k === "economia" ? ' class="deshabilitada" title="Disponible en una versión posterior"' : ""}>${t.toUpperCase()}</button>`).join("");
  }
  function renderAlertas(r) {
    const cont = $("#alertas");
    if (!r.ok) {
      cont.innerHTML = `<div class="error-bloqueo" role="alert"><strong>Entradas incompatibles: no se calcula este escenario.</strong><ul>${r.errores.map((x) => `<li>${esc(x)}</li>`).join("")}</ul></div>`;
      return;
    }
    const av = r.alertas.filter((a) => a.nivel === "aviso"), inf = r.alertas.filter((a) => a.nivel === "info");
    const li = (a) => `<li class="alerta ${a.nivel}"${a.ilustrativo ? ` title="${esc(S.TXT_ILUSTRATIVO)}"` : ""}><strong>${esc(a.titulo)}</strong>${esc(a.texto)} <span class="ref">(${esc(a.ref)})</span>` +
      (a.ilustrativo ? ` ${tip(S.TXT_ILUSTRATIVO)} <span class="ref"><em>Umbral visual ilustrativo: no es una regla industrial.</em></span>` : "") + `</li>`;
    cont.innerHTML = `<details${ui.alertasAbiertas ? " open" : ""} id="det-alertas"><summary>Alertas del escenario ${estado.activo}
      <span class="cuenta aviso">${av.length} aviso${av.length === 1 ? "" : "s"}</span><span class="cuenta info">${inf.length} nota${inf.length === 1 ? "" : "s"}</span>
      <span class="muted pequeno">Informan; no recomiendan inversión.</span></summary><ul>${av.map(li).join("")}${inf.map(li).join("")}</ul></details>`;
    $("#det-alertas").addEventListener("toggle", (ev) => { ui.alertasAbiertas = ev.target.open; });
  }

  // ============================================================================================
  // Piezas reutilizables
  // ============================================================================================
  const tarjeta = (titulo, cuerpo, extra) => `<article class="tarjeta">${titulo ? `<div class="tarjeta-cab"><h2>${titulo}</h2>${extra || ""}</div>` : ""}${cuerpo}</article>`;
  const kpi = (rotulo, valor, unidad, sec, est, ref, tipTxt) => `<div class="kpi"><div class="kpi-rotulo"><span>${rotulo}</span>${tipTxt ? tip(tipTxt) : ""}</div>
    <div class="kpi-valor num">${valor}</div><div class="kpi-unidad">${unidad}</div>${sec ? `<div class="kpi-sec">${sec}</div>` : ""}<div style="margin-top:4px">${badge(est, ref)}</div></div>`;

  const bandera = (t, tipTxt) => `<span class="bandera" tabindex="0" title="${esc(tipTxt)}">${t}</span>`;
  function banderas(r) {
    const b = [];
    if (r.fuera_rango.escala) b.push(bandera("ESCENARIO FUERA DEL RANGO PRINCIPAL ESTUDIADO", "Extrapolación física del modelo; no es una escala analizada en profundidad (rango principal 2.500–20.000 aves/día)."));
    if (r.fuera_rango.peso) b.push(bandera("PESO FUERA DEL RANGO PRINCIPAL · EXTRAPOLACIÓN", "Peso fuera del rango principal utilizado en el estudio (2,2–3,5 kg); resultados deben tratarse como extrapolación."));
    if (r.escenario_matematico) b.push(bandera("ESCENARIO MATEMÁTICO", "La combinación peso–edad–FCR requiere validación zootécnica."));
    if (r.demanda.escenario.id === "CERO") b.push(bandera("DEMANDA DOCUMENTADA ≈ 0", "Demanda documentada actual: no validada / prácticamente nula."));
    return b.length ? `<div class="banderas">${b.join("")}</div>` : "";
  }
  function baseCalculo(r) {
    const e = r.entradas, dm = r.demanda;
    return `<div class="base-calculo">Capacidad instalada <strong>${fmt(e.escala)}</strong> aves/día operativo × utilización operativa asumida <strong>${pct(e.utilizacion)}</strong> =
      <strong>producción simulada de ${fmt(r.capacidad.aves_procesadas_dia_op)} aves por día operativo</strong> · ${fmt(e.dias_anio)} días de faena/año (${e.dias_semana} d/sem) ·
      pollo de <strong>${fmt(e.peso, 1)} kg</strong> · configuración <strong>${NOMBRE_CONFIG[e.config]}</strong> · demanda <strong>${esc(dm.escenario.nombre)}</strong> (${e.metodo})</div>`;
  }

  function filaTabla(etq, valor, unidad, per, est, ref, clase) {
    return `<tr${clase ? ` class="${clase}"` : ""}><td>${etq}</td><td class="n">${valor}</td><td>${unidad}${per ? " " + per : ""}</td><td>${est ? badge(est, ref) : ""}</td></tr>`;
  }
  const tabla = (cab, filas) => `<div class="tabla-envoltura"><table><thead><tr>${cab.map((c, i) => `<th${i === 1 ? ' class="n"' : ""}>${c}</th>`).join("")}</tr></thead><tbody>${filas}</tbody></table></div>`;

  function lecturaDemanda(r) {
    const s = r.demanda.sel, e = r.entradas, c = r.capacidad;
    if (!(r.demanda.D > 0)) return "No hay demanda en el escenario: toda la producción simulada queda sin comprador identificado.";
    if (s.factor_demanda_capacidad > 1 + 1e-9)
      return `La capacidad instalada <strong>no alcanza</strong>: la demanda requiere ${fmt(s.aves_necesarias_dia_operativo)} aves/día operativo. Aun a plena capacidad se cubriría ${pct(s.cobertura_maxima_plena_capacidad)}; con la utilización asumida (${pct(e.utilizacion)}) se cubre <strong>${pct(s.cobertura_operativa)}</strong>.`;
    if (e.utilizacion < s.utilizacion_requerida_por_demanda - 1e-9)
      return `La capacidad instalada <strong>sí alcanza técnicamente</strong> (factor ${pct(s.factor_demanda_capacidad)}), pero con la utilización asumida (${pct(e.utilizacion)}) se producen ${fmt(c.aves_procesadas_dia_op)} de las ${fmt(s.aves_necesarias_dia_operativo)} aves/día operativo requeridas: <strong>el escenario operativo cubre ${pct(s.cobertura_operativa, 1)} de la demanda</strong>, no el 100 %.`;
    if (e.utilizacion > s.utilizacion_requerida_por_demanda + 1e-9)
      return `La producción simulada (${fmt(c.aves_procesadas_dia_op)} aves/día operativo) <strong>supera</strong> lo que requiere la demanda (${fmt(s.aves_necesarias_dia_operativo)}): se cubre el 100 % y sobran ${fmt(s.aves_producidas_sin_demanda_dia_op)} aves/día operativo producidas sin destino.`;
    return "La producción simulada coincide con la capacidad requerida por la demanda.";
  }

  function metricasHTML(r) {
    const s = r.demanda.sel, e = r.entradas, c = r.capacidad;
    const f = s.factor_demanda_capacidad, maxF = Math.max(2, f * 1.1);
    const hayDem = r.demanda.D > 0;
    const medidor = (v, extra) => `<div class="medidor" role="img" aria-label="${pct(v)}"><span style="width:${Math.min(100, v * 100)}%"></span>${extra || ""}</div>`;
    const cadena = `<div class="cadena">
      <div class="eslabon"><div class="pequeno muted">Capacidad instalada</div><div class="valor">${fmt(c.escala)}</div><div class="pequeno">aves ${PER.op} (máximo del escenario)</div></div><span class="flecha">×</span>
      <div class="eslabon"><div class="pequeno muted">Utilización operativa asumida</div><div class="valor">${pct(e.utilizacion)}</div><div class="pequeno">elegida por el usuario</div></div><span class="flecha">=</span>
      <div class="eslabon"><div class="pequeno muted">Producción simulada</div><div class="valor">${fmt(c.aves_procesadas_dia_op)}</div><div class="pequeno">aves procesadas ${PER.op}</div></div>
      <div class="eslabon" style="border-color:var(--m-cob)"><div class="pequeno muted">Capacidad requerida por la demanda</div><div class="valor">${hayDem ? fmt(s.aves_necesarias_dia_operativo) : "0"}</div><div class="pequeno">aves ${PER.op} (${esc(r.demanda.escenario.nombre)}, ${e.metodo})</div></div></div>`;
    const tarjetas = `<div class="metricas metricas-4">
      <div class="metrica util"><div class="metrica-cab"><span class="metrica-icono" aria-hidden="true">U</span><div><div class="metrica-de">elegida por el usuario</div><div class="metrica-nombre">Utilización operativa asumida</div></div>
        ${tip("Porcentaje elegido manualmente para simular cuánto se procesa realmente. Producción simulada = capacidad instalada × utilización operativa asumida. Siempre 0–100 %.")}</div>
        <div class="metrica-valor">${pct(e.utilizacion)}</div>${medidor(e.utilizacion)}
        <div class="medidor-escala"><span>0 %</span><span>100 % (máximo)</span></div>
        <div class="metrica-def">Producción simulada: ${fmt(c.aves_procesadas_dia_op)} aves/día operativo.</div></div>
      <div class="metrica req"><div class="metrica-cab"><span class="metrica-icono" aria-hidden="true">R</span><div><div class="metrica-de">exigida por la demanda</div><div class="metrica-nombre">Utilización requerida por demanda</div></div>
        ${tip("Mínimo entre (capacidad requerida por la demanda ÷ capacidad instalada) y 100 %. La calcula el modelo; no la elige el usuario.")}</div>
        <div class="metrica-valor">${hayDem ? pct(s.utilizacion_requerida_por_demanda) : "0 %"}</div>${medidor(s.utilizacion_requerida_por_demanda)}
        <div class="medidor-escala"><span>0 %</span><span>100 % (máximo)</span></div>
        <div class="metrica-def">${!hayDem ? "Sin demanda en el escenario." : Math.abs(e.utilizacion - s.utilizacion_requerida_por_demanda) < 1e-9 ? "Igual a la asumida." : e.utilizacion < s.utilizacion_requerida_por_demanda ? "<strong>Mayor que la asumida</strong>: falta producción." : "<strong>Menor que la asumida</strong>: sobra producción."}</div></div>
      <div class="metrica factor"><div class="metrica-cab"><span class="metrica-icono" aria-hidden="true">÷</span><div><div class="metrica-de">demanda ÷ capacidad instalada</div><div class="metrica-nombre">Factor demanda/capacidad</div></div>
        ${tip("Capacidad requerida por la demanda ÷ capacidad instalada. PUEDE superar 100 %: más de 100 % = la capacidad instalada no alcanza. NO es una utilización.")}</div>
        <div class="metrica-valor">${hayDem ? pct(f) : "0 %"}</div>
        <div class="medidor-factor" role="img" aria-label="Factor ${pct(f)}; la marca indica 100 %"><span style="width:${Math.min(100, f / maxF * 100)}%"></span><i style="left:${1 / maxF * 100}%"></i></div>
        <div class="medidor-escala"><span>0 %</span><span>marca = 100 % de la capacidad</span></div>
        <div class="metrica-def">${!hayDem ? "Sin demanda." : f > 1 + 1e-9 ? "<strong>La demanda excede la capacidad instalada.</strong>" : "La capacidad instalada alcanza técnicamente."}</div></div>
      <div class="metrica cob"><div class="metrica-cab"><span class="metrica-icono" aria-hidden="true">✓</span><div><div class="metrica-de">de la demanda</div><div class="metrica-nombre">Cobertura de demanda</div></div>
        ${tip("Con la producción simulada: producción simulada ÷ capacidad requerida (hasta 100 %). Máxima a plena capacidad: capacidad instalada ÷ capacidad requerida (hasta 100 %). Son dos números distintos.")}</div>
        <div class="pequeno"><strong>Con la producción simulada</strong></div>
        <div class="metrica-valor">${hayDem ? pct(s.cobertura_operativa, s.cobertura_operativa < 1 ? 1 : 0) : "—"}</div>${medidor(hayDem ? s.cobertura_operativa : 0)}
        <div class="pequeno" style="margin-top:6px">Máxima posible a plena capacidad: <strong>${hayDem ? pct(s.cobertura_maxima_plena_capacidad, s.cobertura_maxima_plena_capacidad < 1 ? 1 : 0) : "—"}</strong></div></div>
    </div>`;
    const caja = (activa, clase, titulo, valor, detalle) => `<div class="caja-estado ${clase} ${activa ? "activa" : ""}"><div class="pequeno muted">${titulo}</div><div class="valor">${valor}</div><div class="pequeno">${detalle}</div></div>`;
    const cajas = `<div class="resultado-demanda resultado-4">
      ${caja(hayDem && s.kg_no_atendidos_operativo_dia_cal > 0.5, "falta", `Demanda no atendida con la producción simulada ${PER.cal}`, `${fmt(s.kg_no_atendidos_operativo_dia_cal)} kg`, `faltan ${fmt(s.aves_no_atendidas_operativo_dia_op)} aves ${PER.op} de producción`)}
      ${caja(hayDem && s.kg_no_atendidos_dia_cal > 0.5, "falta", `Demanda no atendida aun a plena capacidad ${PER.cal}`, `${fmt(s.kg_no_atendidos_dia_cal)} kg`, `faltan ${fmt(s.aves_faltantes_dia_operativo)} aves ${PER.op} de capacidad instalada`)}
      ${caja(c.capacidad_ociosa_operativa > 0.5, "sobra", `Capacidad ociosa operativa ${PER.op}`, `${fmt(c.capacidad_ociosa_operativa)} aves`, "= capacidad instalada − producción simulada")}
      ${caja(s.capacidad_disponible_respecto_demanda > 0.5, "sobra", `Capacidad disponible respecto de la demanda ${PER.op}`, `${fmt(s.capacidad_disponible_respecto_demanda)} aves`, "= capacidad instalada − capacidad requerida por la demanda (mínimo 0)")}
    </div>`;
    return cadena + `<p class="nota-caja" style="margin-top:12px">${lecturaDemanda(r)}</p>` + tarjetas + cajas;
  }

  // ---------- visualización del pollo (Sankey simplificado, SVG propio) ----------
  function gruposPollo(k) {
    return [
      { n: "Productos principales", d: "entero, pechuga, pata-muslo, suprema", v: k.producto_principal, c: "var(--s1)" },
      { n: "Otros cortes y carne comestible", d: "alas, carcasa-esqueleto, CMS, recortes y piel", v: k.alas + k.carcasa_esqueleto + k.cms + k.recortes_piel, c: "var(--s7)" },
      { n: "Menudencias y cuello", d: "hígado, corazón, molleja, cuello", v: k.menudencias + k.cuello, c: "var(--s3)" },
      { n: "Garras", d: "grado A + segunda (comestible)", v: k.garras, c: "var(--s4)" },
      { n: "Sangre recuperada", d: "85 % de la sangre drenada", v: k.sangre, c: "var(--s8)" },
      { n: "Plumas (húmedas)", d: "incluye agua de escaldado adherida", v: k.plumas, c: "var(--s2)" },
      { n: "Vísceras, cabezas, huesos y otros", d: "no comestibles (subproductos)", v: k.visceras + k.cabeza + k.huesos + k.otros_c, c: "var(--s5)" },
      { n: "Residuos, efluentes y pérdidas", d: "contenido intestinal, decomisos, sangre no recuperada, goteo, mermas", v: k.residuos + k.perdidas, c: "var(--gris-serie)" },
    ];
  }
  function polloHTML(r) {
    const k = r.k, e = r.entradas, g = gruposPollo(k);
    const total = k.peso_vivo + k.agua_incorporada;
    const W = 470, H = 300, gap = 6, x0 = 96, w0 = 24, x1 = 392, w1 = 24;
    const s = (H - gap * (g.length - 1)) / total;
    let yl = (H - total * s) / 2, yr = 0, svg = "";
    const hBio = k.peso_vivo * s, hAgua = k.agua_incorporada * s;
    const yTop = yl;
    g.forEach((it) => {
      const h = it.v * s;
      const xm = (x0 + w0 + x1) / 2;
      svg += `<path d="M${x0 + w0},${yl} C${xm},${yl} ${xm},${yr} ${x1},${yr} L${x1},${yr + h} C${xm},${yr + h} ${xm},${yl + h} ${x0 + w0},${yl + h} Z" fill="${it.c}" fill-opacity=".28"><title>${esc(it.n)}: ${fmt(it.v, 3)} kg por ave</title></path>`;
      svg += `<rect x="${x1}" y="${yr}" width="${w1}" height="${Math.max(1, h)}" rx="3" fill="${it.c}"><title>${esc(it.n)}: ${fmt(it.v, 3)} kg por ave (${pct(it.v / total, 1)})</title></rect>`;
      if (h >= 13) svg += `<text x="${x1 + w1 + 6}" y="${yr + h / 2 + 4}" font-size="14">${pct(it.v / total)}</text>`;
      yl += h; yr += h + gap;
    });
    svg = `<rect x="${x0}" y="${yTop}" width="${w0}" height="${hBio}" rx="3" fill="var(--texto)"><title>Pollo vivo ${fmt(k.peso_vivo, 2)} kg</title></rect>
      <rect x="${x0}" y="${yTop + hBio + 1}" width="${w0}" height="${Math.max(2, hAgua - 1)}" fill="var(--s1)" fill-opacity=".55"><title>Agua incorporada ${fmt(k.agua_incorporada, 3)} kg</title></rect>
      <text x="${x0 - 8}" y="${yTop + hBio / 2}" text-anchor="end" font-size="16" font-weight="700" style="fill:var(--texto)">Pollo vivo</text>
      <text x="${x0 - 8}" y="${yTop + hBio / 2 + 18}" text-anchor="end" font-size="15">${fmt(k.peso_vivo, 1)} kg</text>
      <text x="${x0 - 8}" y="${yTop + hBio + hAgua / 2 + 4}" text-anchor="end" font-size="12">+${fmt(k.agua_incorporada, 2)} agua</text>` + svg;
    const aves = r.capacidad.aves_procesadas_dia_op;
    const ley = g.map((it) => `<li><span class="sw" style="background:${it.c}"></span><span><strong>${it.n}</strong><br><span class="muted pequeno">${it.d}</span></span>
      <span class="num">${fmt(it.v, 3)} kg</span><span class="num muted">${fmtT(it.v * aves / 1000)} t/día</span></li>`).join("");
    return `<div class="pollo-flujo"><div><svg class="grafico" viewBox="0 0 ${W} ${H}" role="img" aria-label="Destino de la masa de un pollo vivo de ${fmt(e.peso, 1)} kg en la configuración ${esc(NOMBRE_CONFIG[e.config])}">${svg}</svg>
      <p class="pequeno muted">Cada kilo tiene un destino y la suma cierra: ${fmt(k.peso_vivo, 2)} kg vivos + ${fmt(k.agua_incorporada, 3)} kg de agua incorporada (chiller y plumas mojadas) = ${fmt(total, 3)} kg de salidas. Las cantidades de la derecha incluyen esa agua.</p></div>
      <div><ul class="leyenda" aria-label="Tabla de destinos por ave">${ley}</ul>
      <p class="pequeno muted" style="margin-top:6px">kg por ave (configuración ${NOMBRE_CONFIG[e.config]}) y t/día operativo a ${fmt(aves)} aves procesadas. ${badge("pvdp", "balance de masa v1.1, rendimientos de fuentes PVDP")}</p></div></div>`;
  }

  function barrasHTML(filas, unidad) {
    const max = Math.max(...filas.map((f) => f.v), 1e-9);
    return `<div class="barras">${filas.map((f) => `<div class="barra-fila"><span>${f.n}</span><span class="pista" title="${esc(f.n)}: ${fmtT(f.v)} ${unidad}"><span style="width:${Math.max(0.4, f.v / max * 100)}%${f.c ? `;background:${f.c}` : ""}"></span></span><span class="v">${fmtT(f.v)}</span></div>`).join("")}</div>
      <p class="pequeno muted" style="margin-top:4px">Valores en ${unidad}.</p>`;
  }

  // ============================================================================================
  // Pestañas
  // ============================================================================================
  function vResumen(r) {
    const c = r.capacidad, p = r.produccion, m = r.masa, e = r.entradas;
    const kp = `<div class="kpis">
      ${kpi("Aves faenadas por año", fmt(r.central.aves_anio), "aves por año", `${fmt(c.aves_procesadas_dia_op)} ${PER.op}`, "modelo", "", "Aves procesadas por día operativo × días de faena por año.")}
      ${kpi("Masa viva procesada", fmtT(r.central.t_vivas_anio), "t por año (peso vivo)", `${fmtT(r.central.kg_vivo_dia / 1000)} t ${PER.op}`, "supuesto", "peso vivo SUP-027 / SUP-058")}
      ${kpi("Producto comercial", fmtT(m.comercial.t_dia_op), "t por día operativo", `${fmtT(m.comercial.t_dia_cal)} t ${PER.cal}`, "pvdp", "balance v1.1", "Masa comestible (productos + coproductos) con el agua retenida del chiller. Ver pestaña Productos.")}
      ${kpi("Pollitos BB", fmt(p.pollitos_alojados_semana_plena), "por semana plena", `${fmt(p.pollitos_alojados_semana_promedio)} en semana promedio`, "prod", "mortalidad y DOA SUP-026")}
      ${kpi("Galpones", fmt(p.m2_galpon), "m² de galpón", `≈ ${fmt(p.galpones_2400m2, 1)} galpones de 2.400 m² · ${fmt(p.capacidad_alojamiento_pollitos)} plazas`, "prod", "densidad SUP-026")}
      ${kpi("Alimento", fmt(p.alimento_t_anio), "t por año", `${fmt(p.alimento_t_semana_plena)} t por semana plena`, "prod", "FCR SUP-028")}
      ${kpi("Ritmo de línea necesario", fmt(c.ritmo_aves_h), "aves por hora neta", `con ${fmt(e.horas_netas, 1)} h netas · a capacidad`, "modelo", "SUP-053", "Escala ÷ horas netas de faena. Sin eficiencia de máquina.")}
      ${kpi("Subproductos a rendering", fmtT(r.subproductos.rendering_potencial.t_dia_op), "t por día operativo", "materia prima potencial (subproductos no comestibles)", "pvdp", "balance v1.1")}
      ${kpi("Inventario", fmtT(r.inventario.elegido.comestible_total_t), "t de producto en stock", `${fmt(e.dias_inventario)} días de ${e.base_inventario === "dias_produccion" ? "producción" : "calendario"}`, "supuesto", "SUP-056")}
    </div>`;
    const comoLeer = `<details class="como-leer" open><summary>Cómo leer este simulador</summary><p>El simulador muestra escenarios físicos, no una recomendación de inversión. Los cálculos pueden ser matemáticamente consistentes y aun depender de supuestos o datos pendientes de campo. Antes de decidir capacidad, inversión o rentabilidad deben incorporarse demanda validada, cotizaciones, CAPEX, OPEX y datos reales de operación.</p></details>`;
    return comoLeer + tarjeta(`Resumen · ${esc(e.nombre)}`, cajaDocumentada(r) + baseCalculo(r) + `<div style="margin-top:12px">${kp}</div>` + explica("resumen")) +
      tarjeta("Planta vs demanda: tres métricas que no se confunden", metricasHTML(r) + explica("metricas")) +
      tarjeta(`¿Qué pasa con cada pollo de ${fmt(e.peso, 1)} kg?`, polloHTML(r) + explica("productos")) +
      tarjeta("Qué tiene que ser verdad en este escenario", tablaCentral(r) + explica("dias"));
  }

  function tablaCentral(r) {
    const c = r.central;
    const f = (etq, v, u, per, est, ref) => filaTabla(etq, v, u, per, est, ref);
    return tabla(["Variable", "Valor", "Unidad y período", "Estado del dato"],
      f("Aves faenadas", fmt(c.aves_anio), "aves", PER.anio, "modelo") +
      f("Masa viva procesada", fmtT(c.kg_vivo_dia / 1000), "t vivas", PER.op, "supuesto", "SUP-027") +
      f("Masa viva procesada", fmt(c.t_vivas_anio), "t vivas", PER.anio, "supuesto", "SUP-027") +
      f("Pollitos BB alojados", fmt(c.pollitos_semana_plena), "pollitos", PER.semp, "prod", "SUP-026") +
      f("Plazas de granja", fmt(c.plazas_granja), "plazas", PER.stock, "prod", "SUP-026") +
      f("Superficie de galpones", fmt(c.m2_galpones), "m²", "", "prod", "SUP-026") +
      f("Alimento", fmt(c.alimento_t_anio), "t", PER.anio, "prod", "SUP-028") +
      f("Comestible: masa biológica", fmtT(c.comestible_masa_biologica_t_dia_operativo), "t", PER.op, "pvdp", "balance v1.1") +
      f("Comestible: agua retenida (no es carne)", fmtT(c.agua_retenida_en_producto_t_dia_operativo), "t", PER.op, "pvdp", "SUP-042") +
      f("Comestible: peso comercial", fmtT(c.producto_comercial_t_dia_operativo), "t", PER.op, "pvdp") +
      f("Peso comercial promedio", fmtT(c.producto_comercial_t_dia_calendario_promedio), "t", PER.cal, "pvdp") +
      f("Peso comercial", fmt(c.producto_comercial_t_anio), "t", PER.anio, "pvdp") +
      f("Producto principal", fmtT(c.producto_principal_t_dia), "t", PER.op, "pvdp") +
      f("Plumas húmedas", fmtT(c.plumas_t_dia), "t", PER.op, "pvdp") +
      f("Sangre recuperada", fmtT(c.sangre_recuperada_t_dia), "t", PER.op, "pvdp") +
      f("Vísceras no comestibles", fmtT(c.visceras_t_dia), "t", PER.op, "pvdp") +
      f("Ritmo de línea a 8 h netas", fmt(c.ritmo_linea_8h_aves_h), "aves/h", "", "modelo") +
      f("Inventario de 7 días de producción", fmtT(c.inventario_7_dias_de_produccion_t), "t", PER.stock, "supuesto", "SUP-056") +
      f("Inventario de 7 días calendario", fmtT(c.inventario_7_dias_calendario_t), "t", PER.stock, "supuesto", "SUP-056") +
      f("Demanda necesaria para vender lo producido (M0, a la utilización supuesta)", fmt(c.demanda_necesaria_100pct_kg_dia_cal), "kg", PER.cal, "campo", "cota inferior; demanda real DPV-003") +
      f(`kg por local y día si todo pasara por los ${r.demanda.locales} locales (a la utilización supuesta)`, fmt(c.kg_por_local_dia_si_todo_por_la_red_100pct), "kg", PER.cal, "campo", "rango de la red 25–300 kg/local/día; DPV-037"));
  }

  function cajaDocumentada(r) {
    return r.demanda.escenario.id === "CERO"
      ? `<div class="aviso-caja" role="note" style="margin-bottom:10px"><strong>DEMANDA DOCUMENTADA ACTUAL: NO VALIDADA / PRÁCTICAMENTE NULA.</strong> ` +
        `Este escenario simula producción al ${pct(r.entradas.utilizacion)}, pero actualmente no existe demanda documentada que respalde ese nivel de operación. Es válido solo como escenario hipotético.</div>`
      : "";
  }

  function vDemanda(r) {
    const dm = r.demanda, s = dm.sel, e = r.entradas, esq = dm.escenario;
    const canales = esq.canales ? Object.keys(esq.canales).filter((k) => esq.canales[k] > 0) : [];
    const esCero = esq.id === "CERO";
    const desc = cajaDocumentada(r) + `<p><strong>${esc(esq.nombre)}</strong> — ${esc(esq.descripcion || esq.categoria || "")}</p>
      <div class="kpis">${kpi("Demanda del escenario", fmt(dm.D), "kg de producto comercial", PER.cal, esCero ? "campo" : "supuesto", esCero ? "DPV-003 · DPV-004" : "SUP-021")}
      ${kpi("Tipo de demanda", esCero ? "Documentada" : "Hipótesis", esCero ? "no validada / prácticamente nula" : "sin evidencia comercial", esCero ? "carnicería familiar sin cuantificar" : "valores de prueba, no pronóstico", "campo", "DPV-003 · DPV-037")}
      ${kpi("Demanda documentada actual", "≈ 0", "kg por día", "no validada; la carnicería familiar no está cuantificada", "campo", "DPV-004")}</div>
      ${canales.length ? `<h3 style="margin-top:12px">Composición por canal</h3>` + barrasHTML(canales.map((k) => ({ n: CANALES[k] || k, v: esq.canales[k] })), "kg por día calendario") : ""}
      ${esCero ? "" : `<div class="aviso-caja" style="margin-top:10px"><strong>No es venta.</strong> ${esc(esq.observaciones || "Hipótesis ingresada para explorar; no es un pronóstico.")}</div>`}`;
    // gráfico: tres barras en aves por día operativo, misma escala
    const E = e.escala, sim = r.capacidad.aves_procesadas_dia_op, nOp = s.aves_necesarias_dia_operativo;
    const max = Math.max(E, nOp, 1) * 1.1;
    const w = (x) => `${Math.max(0, x / max * 100)}%`;
    const fila = (titulo, sub, v, estilo, etiqueta, claro) => `<div class="cap-dem-fila"><span><strong>${titulo}</strong><br><span class="pequeno muted">${sub}</span></span>
      <div class="cap-dem-pista"><span style="left:0;width:${w(v)};${estilo}" title="${esc(titulo)}: ${fmt(v)} aves"></span><em style="left:${w(v)}${v / max > 0.6 ? `;transform:translateX(-100%)${claro ? ";color:#fff" : ""}` : ""}">${etiqueta}</em>
      ${nOp > 0 ? `<i style="left:${w(nOp)}" title="Capacidad requerida por la demanda"></i>` : ""}</div></div>`;
    const grafico = `<div class="cap-dem" role="img" aria-label="Capacidad instalada ${fmt(E)}, producción simulada ${fmt(sim)} y capacidad requerida por la demanda ${fmt(nOp)} aves por día operativo">
      ${fila("Capacidad instalada", `aves ${PER.op}`, E, "background:var(--superficie-2);outline:1px solid var(--borde-fuerte)", fmt(E))}
      ${fila("Producción simulada", `instalada × ${pct(e.utilizacion)}`, sim, "background:var(--s1)", fmt(sim), true)}
      ${fila("Capacidad requerida por la demanda", `${e.metodo}, aves ${PER.op}`, nOp, "background:var(--s3)", nOp > 0 ? fmt(nOp) : "sin demanda", true)}
      <p class="pequeno muted">Misma escala para las tres barras. La línea vertical marca la capacidad requerida por la demanda: si la producción simulada no la alcanza, falta producción; si la capacidad instalada no la alcanza, falta planta.</p></div>`;
    const conv = dm.D > 0 ? `<div class="nota-caja"><strong>Conversión (misma base temporal):</strong> ${fmt(dm.D)} kg ${PER.cal} ÷ ${fmt(s.res.comestible_por_ave_mix, 3)} kg comestibles por ave ${e.metodo === "M0" ? "(ave completa)" : "(mix, parte limitante: " + esc(s.res.limitante) + ")"} =
      ${fmt(s.res.aves_dia_cal)} aves ${PER.cal} × 365 / ${fmt(e.dias_anio)} = <strong>${fmt(nOp)} aves ${PER.op}</strong> requeridas.</div>` : "";
    const filas = ["M0", "M1", "M2", "M3"].map((m) => {
      const x = dm.metodos[m];
      return `<tr${m === e.metodo ? ' class="sel"' : ""}><td><strong>${m}</strong> ${m === "M0" ? "ave completa" : "mix " + { M1: "entero dominante", M2: "trozado", M3: "valor agregado" }[m]}</td>
        <td class="n">${fmt(x.aves_necesarias_dia_operativo)}</td><td class="n">${pct(x.factor_demanda_capacidad)}</td><td class="n">${pct(x.utilizacion_requerida_por_demanda)}</td>
        <td class="n">${pct(x.cobertura_operativa)}</td><td class="n">${pct(x.cobertura_maxima_plena_capacidad)}</td>
        <td class="n">${fmt(x.kg_no_atendidos_operativo_dia_cal)}</td><td class="n">${fmt(x.capacidad_disponible_respecto_demanda)}</td><td class="n">${fmt(x.res.excedente_total * x.cobertura_demanda)}</td><td>${esc(x.res.limitante)}</td></tr>`;
    }).join("");
    const tabM = `<p class="pequeno">Utilización operativa asumida en todos los métodos: <strong>${pct(e.utilizacion)}</strong> (${fmt(sim)} aves/día operativo).</p>
      <div class="tabla-envoltura"><table><thead><tr><th>Método</th><th class="n">Capacidad requerida (aves/día op.)</th><th class="n">Factor dem./cap. instalada</th><th class="n">Utilización requerida</th><th class="n">Cobertura con producción simulada</th><th class="n">Cobertura máxima a plena capacidad</th><th class="n">No atendido con producción simulada (kg/día cal)</th><th class="n">Capacidad disponible respecto de la demanda (aves/día op.)</th><th class="n">Partes sin comprador (kg/día cal)</th><th>Parte limitante</th></tr></thead><tbody>${filas}</tbody></table></div>
      <p class="pequeno muted">Fila resaltada = método elegido (Parámetros avanzados). Partes sin comprador = partes producidas que el mix no pide, a plena capacidad. ${badge("supuesto", "mixes SUP-023, conversión SUP-054")} ${badge("pvdp", "rendimientos del balance")}</p>`;
    const vender = `<div class="kpis">
      ${kpi("Para vender la producción simulada (M0)", fmt(dm.demanda_necesaria_a_u_kg_dia_cal), "kg por día calendario", `a ${pct(e.utilizacion)} · ${fmt(dm.demanda_necesaria_100pct_kg_dia_cal)} a plena capacidad`, "campo", "DPV-003")}
      ${kpi("Producción simulada sin destino (M0)", fmt(dm.kg_sin_destino_a_u_dia_cal), "kg por día calendario", "producción simulada − demanda", "campo", "AL2")}
      ${kpi("Pollo por local si todo va a la red", fmt(dm.kg_por_local_dia_plena), "kg por local por día", `${dm.locales} locales · a plena capacidad · rango de la red 25–300`, "campo", "DPV-037")}
    </div>`;
    return tarjeta("Escenario de demanda", desc + explica("demanda")) +
      tarjeta("Capacidad instalada, producción simulada y demanda", grafico + conv + `<div style="margin-top:12px">${metricasHTML(r)}</div>` + explica("metricas")) +
      tarjeta("Los cuatro métodos de conversión, lado a lado", tabM) +
      tarjeta("¿Cuánta demanda haría falta?", vender + explica("dias"));
  }

  function vProduccion(r) {
    const p = r.produccion, q = r.produccion_plena, a = r.abastecimiento, e = r.entradas;
    const aviso = (r.escenario_matematico ? `<div class="aviso-caja" style="margin-bottom:8px"><strong>Escenario matemático.</strong> La combinación peso–edad–FCR requiere validación zootécnica: estas cifras de granja y alimento no representan un escenario productivo del estudio.</div>` : "") + `<div class="aviso-caja"><strong>Escenarios físicos, no diseño definitivo.</strong> No hay galpones, productores, incubadoras ni proveedores de alimento relevados. Cifras de orden de magnitud con el desempeño elegido.</div>`;
    const cadena = `<div class="cadena" style="margin-top:12px">
      <div class="eslabon"><div class="pequeno muted">Pollitos BB alojados</div><div class="valor">${fmt(p.pollitos_alojados_por_dia_faena)}</div><div class="pequeno">por día de faena</div></div><span class="flecha">→</span>
      <div class="eslabon"><div class="pequeno muted">Mueren en granja (${pct(e.mortalidad, 1)})</div><div class="valor">−${fmt(p.pollitos_alojados_por_dia_faena - p.aves_cargadas_dia)}</div></div><span class="flecha">→</span>
      <div class="eslabon"><div class="pequeno muted">Aves cargadas</div><div class="valor">${fmt(p.aves_cargadas_dia)}</div></div><span class="flecha">→</span>
      <div class="eslabon"><div class="pequeno muted">Mueren en transporte (${pct(e.doa, 2)})</div><div class="valor">−${fmt(p.aves_cargadas_dia - r.capacidad.aves_procesadas_dia_op)}</div></div><span class="flecha">→</span>
      <div class="eslabon"><div class="pequeno muted">Aves faenadas</div><div class="valor">${fmt(r.capacidad.aves_procesadas_dia_op)}</div><div class="pequeno">por día operativo</div></div></div>`;
    const fila = (etq, x, y, u, per, est, ref, d) => `<tr><td>${etq}</td><td class="n">${fmt(x, d || 0)}</td><td class="n">${fmt(y, d || 0)}</td><td>${u} ${per || ""}</td><td>${badge(est === "supuesto" ? "prod" : est, ref)}</td></tr>`;
    const tab = `<div class="tabla-envoltura"><table><thead><tr><th>Variable</th><th class="n">A la utilización supuesta (${pct(e.utilizacion)})</th><th class="n">A plena escala (100 %)</th><th>Unidad</th><th>Estado</th></tr></thead><tbody>
      ${fila("Pollitos BB alojados", p.pollitos_alojados_semana_plena, q.pollitos_alojados_semana_plena, "pollitos", PER.semp, "supuesto", "SUP-026")}
      ${fila("Pollitos BB alojados", p.pollitos_alojados_semana_promedio, q.pollitos_alojados_semana_promedio, "pollitos", PER.semprom, "supuesto", "SUP-026")}
      ${fila("Pollitos BB alojados", p.pollitos_alojados_anio, q.pollitos_alojados_anio, "pollitos", PER.anio, "supuesto", "SUP-026")}
      ${fila("Aves cargadas en granja", p.aves_cargadas_dia, q.aves_cargadas_dia, "aves", PER.op, "supuesto", "SUP-026")}
      ${fila("Plazas de granja (capacidad de alojamiento)", p.capacidad_alojamiento_pollitos, q.capacidad_alojamiento_pollitos, "plazas", PER.stock, "supuesto", "SUP-026")}
      ${fila("Aves vivas en crianza (ritmo pleno)", p.inventario_aves_ritmo_pleno, q.inventario_aves_ritmo_pleno, "aves", PER.stock, "supuesto", "")}
      ${fila("Superficie de galpón", p.m2_galpon, q.m2_galpon, "m²", "", "prod", "densidad SUP-026")}
      ${fila("Galpones equivalentes de 1.200 m²", p.galpones_1200m2, q.galpones_1200m2, "galpones", "", "supuesto", "tamaño ilustrativo", 1)}
      ${fila("Galpones equivalentes de 2.400 m²", p.galpones_2400m2, q.galpones_2400m2, "galpones", "", "supuesto", "tamaño ilustrativo", 1)}
      ${fila("Ciclos de crianza por año", p.ciclos_anio, q.ciclos_anio, "ciclos", "", "supuesto", "edad + días entre lotes", 2)}
      ${fila("Alimento", p.alimento_t_semana_plena, q.alimento_t_semana_plena, "t", PER.semp, "prod", "FCR SUP-028")}
      ${fila("Alimento", p.alimento_t_anio, q.alimento_t_anio, "t", PER.anio, "prod", "FCR SUP-028")}
      ${fila("Alimento de un ciclo de crianza", p.alimento_ciclo_crianza_t, q.alimento_ciclo_crianza_t, "t", PER.stock, "supuesto", "capital de trabajo físico")}
      ${fila("Alimento por ave faenada", p.alimento_por_ave_faenada_kg, q.alimento_por_ave_faenada_kg, "kg", PER.ave, "supuesto", "SUP-028", 2)}
      ${fila("Agua de bebida (solo bebida)", p.agua_bebida_m3_anio, q.agua_bebida_m3_anio, "m³", PER.anio, "supuesto", "1,8 L por kg de alimento")}
      </tbody></table></div><p class="pequeno muted">Las granjas se dimensionan para la <strong>semana plena</strong> (sin feriados); el promedio anual incluye feriados. La columna «plena escala» sirve para dimensionar; la de utilización supuesta, para operar.</p>`;
    const ab = `<p>Granjas propias: <strong>${pct(a.pct_propio)}</strong> de los m² · integrados: <strong>${pct(1 - a.pct_propio)}</strong> (sin ganador, DEC-020).</p>
      ${tabla(["Abastecimiento", "Valor", "Unidad", "Estado"],
        filaTabla("m² de galpón propios", fmt(a.m2_propios), "m²", "", "supuesto") +
        filaTabla("m² de galpón de productores integrados", fmt(a.m2_integrados), "m²", "", "supuesto") +
        filaTabla("Plazas propias", fmt(a.plazas_propias), "plazas", "", "supuesto") +
        filaTabla("Productores integrados necesarios", a.productores === null ? "dato pendiente" : fmt(a.productores, 1), "productores", "", "campo", "m² por productor: DPV-048") +
        a.productores_ilustrativos.map((x) => filaTabla(`<span class="muted">Ilustrativo: si cada productor tuviera ${x.galpones_2400} galpón${x.galpones_2400 > 1 ? "es" : ""} de 2.400 m²</span>`, fmt(x.productores, 1), "productores", "", "supuesto", "aritmética; el dato real es DPV-048", "sub")).join(""))}`;
    return tarjeta("Producción primaria: granjas, pollitos y alimento", aviso + cadena + explica("produccion")) +
      tarjeta("Qué necesitan las granjas", tab) + tarjeta("Modelo de abastecimiento", ab);
  }

  function vPlanta(r) {
    const c = r.capacidad, e = r.entradas, L = r.logistica, m = r.masa;
    const ritmos = [6, 8, 10, 16].concat([e.horas_netas]).filter((h, i, arr) => arr.indexOf(h) === i).sort((a, b) => a - b);
    const cap = `<div class="kpis">
      ${kpi("Capacidad instalada", fmt(c.escala), "aves por día operativo", "capacidad operativa al 100 %", "supuesto", "SUP-052")}
      ${kpi("Producción simulada", fmt(c.aves_procesadas_dia_op), "aves procesadas por día operativo", `utilización operativa asumida ${pct(c.utilizacion)}`, "supuesto")}
      ${kpi("Capacidad ociosa operativa", fmt(c.capacidad_ociosa_operativa), "aves por día operativo", "capacidad instalada − producción simulada", "modelo")}
      ${kpi("Ritmo de línea necesario", fmt(c.ritmo_aves_h), "aves por hora neta", `${fmt(c.ritmo_kg_vivo_h / 1000, 1)} t vivas por hora`, "modelo", "SUP-053")}
    </div>
    <h3 style="margin-top:14px">Ritmo según horas netas de faena (a capacidad)</h3>
    ${tabla(["Horas netas por día", "Aves por hora", "kg vivos por hora", ""],
      ritmos.map((h) => `<tr${h === e.horas_netas ? ' class="sel"' : ""}><td>${fmt(h, 1)} h${h === 16 ? " (dos turnos de 8 h)" : ""}${h === e.horas_netas ? " · elegida" : ""}</td><td class="n">${fmt(c.escala / h)}</td><td>${fmt(c.escala * e.peso / h)}</td><td>${badge("modelo")}</td></tr>`).join(""))}
    <p class="pequeno muted">No se asume eficiencia de máquina ni se selecciona equipo: el ritmo nominal que habría que especificar sería mayor.</p>`;
    const opcal = `<div class="grilla-2">
      <div><h3>Por día operativo (día con faena)</h3>${tabla(["", "Valor", "Unidad", ""],
        filaTabla("Aves procesadas", fmt(c.aves_procesadas_dia_op), "aves", "", "modelo") +
        filaTabla("Producto comercial", fmtT(m.comercial.t_dia_op), "t", "", "pvdp"))}</div>
      <div><h3>Por día calendario (promedio de 365)</h3>${tabla(["", "Valor", "Unidad", ""],
        filaTabla("Aves procesadas equivalentes", fmt(c.aves_dia_cal_equivalente), "aves", "", "modelo") +
        filaTabla("Producto comercial despachado", fmtT(m.comercial.t_dia_cal), "t", "", "pvdp"))}</div></div>
      <p class="nota-caja" style="margin-top:10px">Factor de conversión: ${fmt(e.dias_anio)} días de faena / 365 = <strong>${fmt(e.dias_anio / 365, 3)}</strong>. Lo que sale en un día de faena no es lo que se vende en un día cualquiera.</p>`;
    const cam = (v, alt) => v === null ? `<span class="muted">${alt}</span>` : fmt(v, 1);
    const log = tabla(["Flujo físico", "Valor", "Unidad y período", "Estado"],
      filaTabla("Aves vivas cargadas en granja", fmtT(L.aves_vivas_cargadas_t_dia), "t", PER.op, "supuesto") +
      filaTabla("Aves vivas recibidas y faenadas", fmtT(L.aves_vivas_recibidas_faenadas_t_dia), "t", PER.op, "supuesto") +
      filaTabla("Producto comestible que sale", fmtT(L.producto_comestible_sale_t_dia), "t", PER.op, "pvdp") +
      filaTabla("Subproductos sólidos que salen", fmtT(L.subproductos_solidos_salen_t_dia), "t", PER.op, "pvdp") +
      filaTabla("Masa a efluente o pérdida (no se transporta; no es el caudal de efluentes)", fmtT(L.masa_a_efluente_o_perdida_t_dia), "t", PER.op, "pvdp") +
      filaTabla("Alimento que llega a granjas (semana plena, 7 días de entrega)", fmtT(L.alimento_a_granjas_t_dia_semana_plena), "t", PER.cal, "supuesto") +
      filaTabla("Camiones de aves vivas", L.camiones_aves_vivas === null ? `${fmt(L.camiones_aves_vivas_rango[1], 1)}–${fmt(L.camiones_aves_vivas_rango[0], 1)}` : fmt(L.camiones_aves_vivas, 1), "camiones", PER.op, "supuesto", "SUP-033 (4.000–7.000 aves/camión, sin fuente)") +
      filaTabla("Camiones refrigerados", cam(L.camiones_frio, "dato pendiente"), "camiones", PER.op, "campo", "DPV-084") +
      filaTabla("Camiones de alimento", cam(L.camiones_alimento, "dato pendiente"), "camiones", PER.cal, "campo", "DPV-084") +
      filaTabla("Retiros de subproductos", cam(L.retiros_subproductos, "dato pendiente"), "retiros", PER.op, "campo", "DPV-084"));
    return tarjeta("Capacidad y ritmo de línea", cap + explica("planta")) +
      tarjeta("Día operativo vs día calendario", opcal + explica("dias")) +
      tarjeta("Logística física (t que entran y salen)", log + `<p class="pequeno muted">La localización respecto de granjas y mercados es hipótesis a estudiar (10_localizacion), no decisión. Sin vehículos seleccionados.</p>`);
  }

  function vProductos(r) {
    const m = r.masa, e = r.entradas, aves = r.capacidad.aves_procesadas_dia_op;
    const tot = m.comercial.t_dia_op;
    const masa = `<div class="barra-apilada" role="img" aria-label="Peso comercial: ${fmtT(m.biologica.t_dia_op)} t de masa biológica y ${fmtT(m.agua.t_dia_op)} t de agua retenida">
        <span style="width:${m.biologica.t_dia_op / tot * 100}%;background:var(--s1)" title="Masa biológica"></span><span style="width:${m.agua.t_dia_op / tot * 100}%;background:var(--s1);opacity:.35" title="Agua retenida"></span></div>
      <p class="pequeno"><span class="muted">Barra completa = peso comercial.</span> Tramo sólido = masa biológica · tramo claro = agua retenida (${pct(m.agua.t_dia_op / tot, 1)} del peso vendido).</p>
      ${tabla(["Comestible (productos + coproductos)", "Por día operativo", "Por día calendario", "Por año"].map((x, i) => x),
        `<tr><td><strong>Masa biológica</strong> (carne y tejidos, sin agua)</td><td class="n">${fmtT(m.biologica.t_dia_op)} t</td><td class="n">${fmtT(m.biologica.t_dia_cal)} t</td><td class="n">${fmt(m.biologica.t_anio)} t</td></tr>
         <tr><td><strong>Agua retenida</strong> en producto (no es carne)</td><td class="n">${fmtT(m.agua.t_dia_op)} t</td><td class="n">${fmtT(m.agua.t_dia_cal)} t</td><td class="n">${fmt(m.agua.t_anio)} t</td></tr>
         <tr class="total"><td><strong>Peso comercial</strong> = biológica + agua</td><td class="n">${fmtT(m.comercial.t_dia_op)} t</td><td class="n">${fmtT(m.comercial.t_dia_cal)} t</td><td class="n">${fmt(m.comercial.t_anio)} t</td></tr>`)}
      <p class="pequeno">${badge("pvdp", "absorción 6 % y goteo 30 %: SUP-042; límite 8 % FTE-168")}</p>`;
    const comest = r.items.filter((i) => (i.clase === "A" || i.clase === "B") && i.t_dia_op > 1e-9);
    const barras = barrasHTML(comest.map((i) => ({ n: i.etiqueta, v: i.t_dia_op, c: i.clase === "A" ? "var(--s1)" : "var(--s7)" })), "t por día operativo (peso comercial) · azul = producto principal, violeta = coproducto");
    const tab = tabla(["Producto", "kg por ave", "t por día operativo", "t por año"],
      comest.map((i) => `<tr><td>${esc(i.etiqueta)} <span class="muted pequeno">(${i.clase === "A" ? "principal" : "coproducto"})</span></td><td class="n">${fmt(i.kg_ave, 3)}</td><td class="n">${fmtT(i.t_dia_op)}</td><td class="n">${fmt(i.t_anio)}</td></tr>`).join("") +
      `<tr class="total"><td>Total comestible</td><td class="n">${fmt(r.agregados.comestible.kg_ave, 3)}</td><td class="n">${fmtT(r.agregados.comestible.t_dia_op)}</td><td class="n">${fmt(r.agregados.comestible.t_anio)}</td></tr>`);
    const cfg = r.configuraciones;
    const rowC = (etq, k, d) => `<tr><td>${etq}</td>${["A", "B", "C"].map((c) => `<td class="n${c === e.config ? " sel" : ""}">${k === "flujos_comestibles_distintos" ? fmt(cfg[c][k]) : fmt(cfg[c][k], d == null ? 2 : d)}</td>`).join("")}</tr>`;
    const confs = `<div class="tabla-envoltura"><table class="comp"><thead><tr><th>t por día operativo a ${fmt(aves)} aves</th><th>${NOMBRE_CONFIG.A}</th><th>${NOMBRE_CONFIG.B}</th><th>${NOMBRE_CONFIG.C}</th></tr></thead><tbody>
      ${rowC("Producto principal", "producto_principal_t")}${rowC("Coproductos comestibles", "coproductos_t")}${rowC("Total comestible", "comestible_t")}
      ${rowC("Huesos (subproducto)", "huesos_t")}${rowC("CMS producida", "cms_t")}${rowC("Subproductos no comestibles", "subproductos_c_t")}
      ${rowC("Masa que pasa por trozado (biológica)", "kg_trozado_t")}${rowC("Masa que pasa por deshuese (biológica)", "kg_deshuese_t")}
      ${rowC("Flujos comestibles distintos (con frío y canal propio)", "flujos_comestibles_distintos")}${rowC("Coproductos por t de producto principal", "coproductos_por_t_de_producto_principal")}
      </tbody></table></div><p class="pequeno muted">Comparación física, sin margen: más proceso = más productos distintos que colocar, más frío y más mano de obra. La configuración elegida está resaltada. ${badge("pvdp", "balance v1.1")}</p>`;
    const exp = tabla(["Parte (100 % a exportación)", "Días de faena para 25 t", "Contenedores por mes", ""],
      r.exportacion.map((x) => `<tr><td>${esc(x.etiqueta)}</td><td class="n">${fmt(x.dias_para_contenedor, 1)}</td><td class="n">${fmt(x.contenedores_mes_si_100pct, 1)}</td><td>${badge("pvdp", "carga de reefer de 25 t, FTE-135 débil")}</td></tr>`).join(""));
    return `<div class="aviso-caja"><strong>Tener masa disponible no significa tener comprador.</strong> Cada tonelada de esta pestaña es física; ninguna está vendida (demanda documentada ≈ 0).</div>` +
      tarjeta("Masa biológica, agua retenida y peso comercial", masa + explica("masa")) +
      tarjeta(`Productos y coproductos · configuración ${NOMBRE_CONFIG[e.config]}`, barras + `<div style="margin-top:12px">${tab}</div>` + explica("productos")) +
      tarjeta("Configuraciones comerciales A / B / C a esta escala", confs) +
      tarjeta("Exportación: ¿cuánto tarda en llenarse un contenedor?", `<div class="aviso-caja"><strong>No es demanda.</strong> Capacidad física de generar lotes si el 100 % de la parte fuera a exportación. Exportación en la demanda = 0 (SUP-022); ningún mercado habilitado confirmado.</div>` + exp);
  }

  function vSubproductos(r) {
    const s = r.subproductos, ag = r.agregados;
    const filas = [
      ["Plumas húmedas (con agua de escaldado)", s.plumas, "var(--s2)"], ["Vísceras no comestibles", s.visceras, "var(--s5)"],
      ["Cabezas", s.cabeza, "var(--s5)"], ["Sangre recuperada (85 %)", s.sangre, "var(--s8)"], ["Huesos y residuo óseo de CMS", s.huesos, "var(--s5)"],
      ["Otros no comestibles (garras descarte, piel/grasa a rendering)", s.otros_c, "var(--s5)"]].filter((x) => x[1].t_dia_op > 1e-9);
    const barras = barrasHTML(filas.map(([n, v, c]) => ({ n, v: v.t_dia_op, c })), "t por día operativo (masa biológica + agua adherida)");
    const tab = tabla(["Material", "Valor", "Unidad", "Estado"],
      filas.map(([n, v]) => filaTabla(n, fmtT(v.t_dia_op), "t", PER.op, "pvdp")).join("") +
      filaTabla("Materia prima potencial de rendering (todos los no comestibles)", fmtT(s.rendering_potencial.t_dia_op), "t", PER.op, "pvdp", "", "total") +
      filaTabla("Ídem por año", fmt(s.rendering_potencial.t_anio), "t", PER.anio, "pvdp") +
      filaTabla("Sólidos a retirar (C + decomisos + contenido intestinal)", fmtT(s.solidos_a_retirar.t_dia_op), "t", PER.op, "pvdp", "DPV-066") +
      filaTabla("<span class='muted'>Sangre drenada total (no sumar con la recuperada)</span>", fmtT(s.sangre_drenada.t_dia_op), "t", PER.op, "pvdp", "", "sub") +
      filaTabla("<span class='muted'>Pluma biológica (sin agua; no sumar)</span>", fmtT(s.plumas_bio.t_dia_op), "t", PER.op, "pvdp", "", "sub") +
      filaTabla("Residuos y efluentes", fmtT(ag.residuos_d.t_dia_op), "t", PER.op, "pvdp") +
      filaTabla("Mermas y pérdidas", fmtT(ag.perdidas_p.t_dia_op), "t", PER.op, "pvdp") +
      filaTabla("Receptor de subproductos identificado", "ninguno", "", "", "campo", "DPV-065 · DPV-080"));
    const coms = tabla(["Coproducto comestible sin comprador identificado", "Valor", "Unidad", "Estado"],
      filaTabla("Garras (grado A + segunda)", fmtT(s.garras.t_dia_op), "t", PER.op, "pvdp") +
      filaTabla("Carcasa-esqueleto", fmtT(s.carcasa_esqueleto.t_dia_op), "t", PER.op, "pvdp", "sin comprador baja a subproducto (SUP-046)"));
    return `<div class="aviso-caja"><strong>Tener masa disponible no significa tener comprador.</strong> Un subproducto sin receptor es un residuo que cuesta retirar (SUP-046, SUP-049).</div>` +
      tarjeta("Subproductos no comestibles", barras + `<div style="margin-top:12px">${tab}</div>` + explica("subproductos")) +
      tarjeta("Coproductos que pueden terminar como subproducto", coms);
  }

  function vInventario(r) {
    const I = r.inventario, e = r.entradas, ip = I.por_base.dias_produccion, ic = I.por_base.dias_calendario;
    const caja = (b, t, etq, formula) => `<div class="caja-estado ${e.base_inventario === b ? "activa sobra" : ""}" style="${e.base_inventario === b ? "" : "opacity:1"}">
      <div class="pequeno"><strong>${etq}</strong>${e.base_inventario === b ? " · elegida" : ""}</div><div class="valor">${fmtT(t.comestible_total_t)} t</div>
      <div class="pequeno muted">${formula}</div></div>`;
    const dos = `<div class="resultado-demanda">
      ${caja("dias_produccion", ip, `${fmt(e.dias_inventario)} días de producción en stock`, `${fmtT(ip.flujo_t_dia)} t ${PER.op} × ${fmt(e.dias_inventario)} días`)}
      ${caja("dias_calendario", ic, `${fmt(e.dias_inventario)} días calendario de cobertura`, `${fmtT(ic.flujo_t_dia)} t despachadas ${PER.cal} × ${fmt(e.dias_inventario)} días`)}</div>
      <p class="nota-caja" style="margin-top:10px">Diferencia: <strong>${fmtT(ip.comestible_total_t - ic.comestible_total_t)} t</strong>. ${fmt(e.dias_inventario)} días calendario de cobertura equivalen a <strong>${fmt(I.equivalencia_dias_produccion_de_dias_calendario, 1)} días de producción</strong> (× ${fmt(e.dias_anio)}/365). Comestible total (A + B, peso comercial): cota superior.</p>`;
    const rep = I.reparto;
    const perf = tabla(["Categoría (perfil " + esc(I.perfil) + ": " + esc(I.perfil_nombre) + ")", "Días de producción", "Días calendario", "Días"],
      `<tr><td>Refrigerado (${pct(rep.refrigerado)})</td><td class="n">${fmtT(ip.refrigerado_t)} t</td><td class="n">${fmtT(ic.refrigerado_t)} t</td><td>${fmt(e.dias_inventario)}</td></tr>
       <tr><td>Congelado (${pct(rep.congelado)})</td><td class="n">${fmtT(ip.congelado_t)} t</td><td class="n">${fmtT(ic.congelado_t)} t</td><td>${fmt(e.dias_congelado)}</td></tr>
       <tr><td>Exportación (${pct(rep.exportacion)})</td><td class="n">${fmtT(ip.exportacion_t)} t</td><td class="n">${fmtT(ic.exportacion_t)} t</td><td>${fmt(e.dias_congelado)}</td></tr>
       <tr class="total"><td>Total por perfil</td><td class="n">${fmtT(ip.refrigerado_t + ip.congelado_t + ip.exportacion_t)} t</td><td class="n">${fmtT(ic.refrigerado_t + ic.congelado_t + ic.exportacion_t)} t</td><td></td></tr>`) +
      `<p class="pequeno muted">Perfiles de destino ilustrativos, no demanda ${badge("supuesto", "SUP-055")}. El refrigerado usa los días de inventario; congelado y exportación, los días de congelado (Parámetros avanzados).</p>`;
    const sub = tabla(["Subproductos que requieren frío si no se retiran en el día", "Valor", "Unidad", "Estado"],
      filaTabla(`Sangre, vísceras, cabezas y huesos · ${fmt(e.dias_inventario)} días de producción`, fmtT(I.subproductos_frio_t), "t", PER.stock, "pvdp", "solo se generan en días de faena"));
    const selector = `<div class="chips" style="margin-bottom:10px"><span class="pequeno muted" style="align-self:center">Base elegida:</span>
      <button type="button" class="chip" data-inv="dias_produccion" aria-pressed="${e.base_inventario === "dias_produccion"}">Días de producción en stock</button>
      <button type="button" class="chip" data-inv="dias_calendario" aria-pressed="${e.base_inventario === "dias_calendario"}">Días calendario de cobertura</button></div>`;
    return tarjeta("Inventario: dos bases temporales", selector + dos + explica("inventario")) +
      tarjeta("Separación por destino", perf) + tarjeta("Subproductos con frío", sub + `<p class="pequeno muted">Cámaras, potencia frigorífica y equipos no están dimensionados (12_energia_frio).</p>`);
  }

  function vComparador() {
    const R = S.SLOTS.map((s) => resultados[s]);
    const E = S.SLOTS.map((s) => estado.escenarios[s]);
    const cab = `<tr><th>Campo</th>${S.SLOTS.map((s, i) => `<th><span class="letra">${s}</span>${esc(E[i].nombre)}<br><button type="button" class="btn-sec" data-editar="${s}" style="margin-top:4px;min-height:28px;padding:2px 8px">${s === estado.activo ? "editando" : "editar"}</button></th>`).join("")}</tr>`;
    const sec = (t) => `<tr class="seccion"><td colspan="4">${t}</td></tr>`;
    const ent = (etq, f) => `<tr><td>${etq}</td>${E.map((e, i) => `<td>${R[i].ok ? f(e, R[i]) : "entradas inválidas"}</td>`).join("")}</tr>`;
    const res = (etq, f, d, sinRel) => {
      const vals = R.map((r) => (r.ok ? f(r) : null));
      const a = vals[0];
      return `<tr><td>${etq}</td>${vals.map((v, i) => `<td>${v === null ? "—" : (typeof d === "function" ? d(v) : fmt(v, d || 0))}${!sinRel && i > 0 && v !== null && a ? `<span class="rel">×${fmt(v / a, 2)} vs A</span>` : ""}</td>`).join("")}</tr>`;
    };
    const t = `<div class="tabla-envoltura"><table class="comp"><thead>${cab}</thead><tbody>
      ${sec("Entradas")}
      ${ent("Capacidad instalada (aves/día operativo)", (e, r) => fmt(e.escala) + (r.fuera_rango.escala ? "<br><span class='pequeno'>fuera del rango principal</span>" : ""))}
      ${ent("Días/semana · días/año", (e) => `${e.dias_semana} · ${fmt(e.dias_anio)}`)}
      ${ent("Horas netas", (e) => fmt(e.horas_netas, 1))}
      ${ent("Peso · edad · mortalidad · FCR", (e, r) => `${fmt(e.peso, 1)} kg · ${e.edad} d · ${pct(e.mortalidad, 1)} · ${fmt(e.fcr, 2)}` + (r.escenario_matematico ? "<br><span class='pequeno'>escenario matemático</span>" : "") + (r.fuera_rango.peso ? "<br><span class='pequeno'>peso: extrapolación</span>" : ""))}
      ${ent("Utilización operativa asumida", (e) => pct(e.utilizacion))}
      ${ent("Demanda · método", (e, r) => `${esc(r.demanda.escenario.nombre)} · ${e.metodo}`)}
      ${ent("Configuración comercial", (e) => NOMBRE_CONFIG[e.config])}
      ${ent("Inventario · perfil", (e) => `${e.dias_inventario} d ${e.base_inventario === "dias_produccion" ? "de producción" : "calendario"} · ${e.perfil_destino}`)}
      ${ent("Granjas propias", (e) => pct(e.pct_propio))}
      ${sec("Aves y granjas")}
      ${res("Aves faenadas por año", (r) => r.central.aves_anio)}
      ${res("t vivas por año", (r) => r.central.t_vivas_anio)}
      ${res("Pollitos BB por semana plena", (r) => r.produccion.pollitos_alojados_semana_plena)}
      ${res("Plazas de granja", (r) => r.produccion.capacidad_alojamiento_pollitos)}
      ${res("m² de galpón", (r) => r.produccion.m2_galpon)}
      ${res("Alimento t/año", (r) => r.produccion.alimento_t_anio)}
      ${sec("Planta y productos")}
      ${res("Ritmo de línea (aves/h netas, a capacidad)", (r) => r.capacidad.ritmo_aves_h)}
      ${res("Producto principal (t/día op.)", (r) => r.central.producto_principal_t_dia, fmtT)}
      ${res("Comestible: masa biológica (t/día op.)", (r) => r.masa.biologica.t_dia_op, fmtT)}
      ${res("Comestible: agua retenida (t/día op.)", (r) => r.masa.agua.t_dia_op, fmtT)}
      ${res("Comestible: peso comercial (t/día op.)", (r) => r.masa.comercial.t_dia_op, fmtT)}
      ${res("Peso comercial (t/día calendario)", (r) => r.masa.comercial.t_dia_cal, fmtT)}
      ${res("Rendering potencial (t/día op.)", (r) => r.subproductos.rendering_potencial.t_dia_op, fmtT)}
      ${res("t/día que entran (aves vivas)", (r) => r.logistica.aves_vivas_recibidas_faenadas_t_dia, fmtT)}
      ${res("t/día que salen (comestible + sólidos)", (r) => r.logistica.producto_comestible_sale_t_dia + r.logistica.subproductos_solidos_salen_t_dia, fmtT)}
      ${sec("Demanda vs capacidad (método de cada escenario)")}
      ${res("Producción simulada (aves/día op.)", (r) => r.capacidad.aves_procesadas_dia_op)}
      ${res("Capacidad requerida por la demanda (aves/día op.)", (r) => r.demanda.sel.aves_necesarias_dia_operativo, 0, true)}
      ${res("Factor demanda/capacidad instalada", (r) => r.demanda.sel.factor_demanda_capacidad, (v) => pct(v), true)}
      ${res("Utilización requerida por demanda", (r) => r.demanda.sel.utilizacion_requerida_por_demanda, (v) => pct(v), true)}
      ${res("Cobertura con la producción simulada", (r) => r.demanda.sel.cobertura_operativa, (v) => pct(v, 1), true)}
      ${res("Cobertura máxima a plena capacidad", (r) => r.demanda.sel.cobertura_maxima_plena_capacidad, (v) => pct(v, 1), true)}
      ${res("Demanda no atendida con producción simulada (kg/día cal.)", (r) => r.demanda.sel.kg_no_atendidos_operativo_dia_cal, 0, true)}
      ${res("Demanda no atendida a plena capacidad (kg/día cal.)", (r) => r.demanda.sel.kg_no_atendidos_dia_cal, 0, true)}
      ${res("Capacidad ociosa operativa (aves/día op.)", (r) => r.capacidad.capacidad_ociosa_operativa, 0, true)}
      ${res("Capacidad disponible respecto de la demanda (aves/día op.)", (r) => r.demanda.sel.capacidad_disponible_respecto_demanda, 0, true)}
      ${res("kg sin destino a plena escala (kg/día cal.)", (r) => r.demanda.sel.kg_sin_destino_plena_escala, 0, true)}
      ${sec("Inventario")}
      ${res("Inventario en días de producción (t)", (r) => r.inventario.por_base.dias_produccion.comestible_total_t, fmtT)}
      ${res("Inventario en días calendario (t)", (r) => r.inventario.por_base.dias_calendario.comestible_total_t, fmtT)}
      ${sec("Alertas")}
      ${res("Avisos activos", (r) => r.alertas.filter((a) => a.nivel === "aviso").length, 0, true)}
      <tr><td>Títulos</td>${R.map((r) => `<td class="pequeno" style="text-align:left">${r.ok ? r.alertas.filter((a) => a.nivel === "aviso").map((a) => esc(a.titulo)).join("<br>") : r.errores.map(esc).join("<br>")}</td>`).join("")}</tr>
      ${sec("Economía del proyecto")}
      ${["CAPEX (USD)", "OPEX (USD/año)", "EBITDA", "VAN · TIR · payback"].map((x) => `<tr class="futuro"><td>${x}</td><td>versión futura</td><td>versión futura</td><td>versión futura</td></tr>`).join("")}
      </tbody></table></div>`;
    return tarjeta("Comparador de escenarios A / B / C", `<p class="nota-caja">Cada columna guarda <strong>sus propios parámetros</strong>. Para cambiarlos, elegí el escenario en la barra superior (o «editar») y modificá el panel de la izquierda. «×n vs A» es solo una razón física: <strong>no hay ganador</strong>.</p>` + t + explica("comparador"));
  }

  function vSupuestos() {
    const e = act(), pr = P.produccion;
    const sup = [
      ["SUP-052", "Escala = aves faenadas por día operativo a capacidad operativa (utilización 100 %)", "entrada «escala»"],
      ["SUP-025", "Calendario: 250 días/año con 5 d/sem · 300 con 6 d/sem", `${P.calendarios["5"]} / ${P.calendarios["6"]} días`],
      ["SUP-053", "Horas netas de faena 6 / 8 / 10 / 16 h como sensibilidad", "entrada «horas netas»"],
      ["SUP-027", "Perfiles de mercado (peso / edad)", Object.keys(pr.perfiles).map((k) => `${k} ${fmt(pr.perfiles[k].peso, 1)} kg / ${pr.perfiles[k].edad} d`).join(" · ")],
      ["SUP-026", "Niveles de desempeño (mortalidad, DOA, días entre lotes, densidad)", Object.keys(pr.desempenos).map((k) => `${k}: ${pct(pr.desempenos[k].mort)} · ${fmt(pr.desempenos[k].doa * 100, 1)} % · ${pr.desempenos[k].vacio} d · ${pr.desempenos[k].kg_m2} kg/m²`).join(" | ")],
      ["SUP-028", "FCR de campo base por perfil", Object.keys(pr.perfiles).map((k) => `${k} ${fmt(pr.perfiles[k].fcr_base, 2)}`).join(" · ")],
      ["SUP-058", "Mismo peso vivo en granja y en planta (merma de ayuno fuera)", "—"],
      ["SUP-036", "Composición primaria del ave y pendientes con el peso (válido 2,0–3,8 kg)", "balance v1.1"],
      ["SUP-042", "Chiller por inmersión: absorción 6 %, goteo 30 % del agua absorbida", "balance v1.1"],
      ["SUP-050", "Variante de referencia: 2,9 kg, rendimiento y condenas medios, inmersión, configuración B", "fija en v0.1"],
      ["SUP-021", "Escenarios de demanda = valores de prueba de orden de magnitud", DATA.demanda.escenarios.filter((d) => d.bloque === "escenario_comercial").map((d) => `${d.nombre} ${fmt(d.total_kg_dia)} kg/día`).join(" · ")],
      ["SUP-022", "Exportación = 0 en la demanda hasta negociación de nivel ≥ 5", "0 kg/día"],
      ["SUP-023", "Mixes M1–M3 y 0,75 kg de pechuga por kg de milanesa", `factor ${fmt(DATA.demanda.factor_milanesa, 2)}`],
      ["SUP-054", "Conversión de demanda en aves: M0 ave completa y M1–M3 parte limitante", "entrada «conversión»"],
      ["SUP-060", "Tres métricas: factor, utilización y cobertura; bases temporales", "—"],
      ["SUP-055", "Perfiles de destino P1–P3 (ilustrativos)", Object.keys(P.perfiles_destino).map((k) => `${k} ${pct(P.perfiles_destino[k].reparto.refrigerado)}/${pct(P.perfiles_destino[k].reparto.congelado)}/${pct(P.perfiles_destino[k].reparto.exportacion)}`).join(" · ")],
      ["SUP-056", "Inventario conceptual con dos bases temporales", "entrada «inventario»"],
      ["SUP-033", "Aves por camión 4.000–7.000 (sin fuente)", P.aves_por_camion_vivo.map((x) => fmt(x)).join("–")],
    ];
    const pend = [["DPV-003", "Volumen, mix, precio y condiciones de compra de la red de supermercados"], ["DPV-037", "Mix y formato de compra por producto y local"],
      ["DPV-004", "Volumen de venta actual de la carnicería familiar"], ["DPV-048", "Productores integrables: m², ubicación, estado"],
      ["DPV-084", "Capacidades útiles de vehículos"], ["DPV-054", "Captura y transporte de aves vivas"], ["DPV-065 / DPV-080", "Receptores de subproductos y rendering"],
      ["DPV-066", "Normativa sobre destino de subproductos y decomisos"], ["DPV-083", "Escala mínima eficiente"]];
    const umb = S.UMBRALES;
    const m = DATA.meta;
    return tarjeta("Estado de los datos", explica("estados").replace("<details class=\"explica\">", "<details class=\"explica\" open>")) +
      tarjeta("Supuestos que usa el simulador", tabla(["ID", "Supuesto", "Valor en el simulador", "Estado"], sup.map(([id, d, v]) => `<tr><td><strong>${id}</strong></td><td>${esc(d)}</td><td>${esc(v)}</td><td>${badge("supuesto")}</td></tr>`).join("")) +
        `<p class="pequeno muted">Detalle y fuentes: 00_gestion_proyecto/supuestos.md (este simulador no lo modifica).</p>`) +
      tarjeta("Datos de campo pendientes", tabla(["ID", "Dato", "", "Estado"], pend.map(([id, d]) => `<tr><td><strong>${id}</strong></td><td>${esc(d)}</td><td></td><td>${badge("campo")}</td></tr>`).join("")) +
        `<p class="pequeno muted">Registro completo: 00_gestion_proyecto/datos_por_validar.md.</p>`) +
      tarjeta("Pendiente de verificación documental primaria (PVDP)", `<ul><li>Rendimientos de faena, cortes, deshuese y subproductos del balance v1.1 (FTE-140, FTE-142, FTE-161 a FTE-184).</li><li>Perfiles productivos de manuales genéticos (FTE-140, FTE-142, FTE-143) y referencias de campo (FTE-050, FTE-154).</li><li>Carga de 25 t por contenedor reefer de 40' (FTE-135, débil).</li><li>Límite de 8 % de agua retenida (FTE-168, prensa).</li></ul>`) +
      tarjeta("Umbrales de las alertas (de interfaz, no datos)", `<p class="nota-caja">${esc(S.TXT_ILUSTRATIVO)} No son reglas industriales: CAPEX y OPEX determinarán qué utilización es realmente baja.</p>` + tabla(["Alerta", "Umbral", "Origen", ""],
        `<tr><td>Utilización baja (asumida o requerida por demanda)</td><td class="n">${pct(umb.utilizacion_baja)}</td><td><strong>Umbral visual ilustrativo</strong>; pendiente de calibración económica y operativa</td><td></td></tr>
         <tr><td>Alto volumen de subproductos</td><td class="n">${fmt(umb.subproductos_flujo_industrial_t)} t/día</td><td>escenarios_escala.md §10 (flujo industrial ~5,3 t/día)</td><td></td></tr>
         <tr><td>Inventario alto</td><td class="n">${umb.inventario_alto_dias} días</td><td><strong>Umbral visual ilustrativo</strong> (una semana); pendiente de calibración económica y operativa</td><td></td></tr>
         <tr><td>Ritmo por encima del rango estudiado</td><td class="n">${fmt(umb.ritmo_max_estudiado)} aves/h</td><td>20.000 aves/día a 8 h netas</td><td></td></tr>
         <tr><td>Pollo por local</td><td class="n">${umb.kg_local_max} kg/local/día</td><td>Extremo del rango de la red (AL10)</td><td></td></tr>
         <tr><td>Escenario matemático: peso y edad</td><td class="n">±15 % de ${umb.ganancia_diaria_ref_g.join("–")} g/día</td><td>Guía de producción, indicador 6; tolerancia de interfaz</td><td></td></tr>
         <tr><td>Escenario matemático: FCR</td><td class="n">±${fmt(umb.fcr_desvio_max, 2)} del FCR interpolado</td><td>Diferencia medio–desfavorable (SUP-026); tolerancia de interfaz</td><td></td></tr>
         <tr><td>Rango principal estudiado: escala</td><td class="n">2.500–20.000 aves/día</td><td>23_plan_expansion (motor: 500–30.000)</td><td></td></tr>
         <tr><td>Rango principal estudiado: peso</td><td class="n">2,2–3,5 kg</td><td>04_balance_masa (motor: 2,0–3,8)</td><td></td></tr>`)) +
      tarjeta("Versión de los modelos y verificación", `<p>Datos generados el <strong>${esc(m.generado)}</strong> (commit ${esc(m.commit_repositorio)}) por <code>${esc(m.generador)}</code>. Pruebas de los modelos al generar: <strong>${esc(m.tests_modelos)}</strong>.</p>` +
        tabla(["Modelo", "Versión", "Último commit", "SHA-256 (inicio)"], Object.keys(m.archivos_fuente).map((k) => `<tr><td>${esc(m.archivos_fuente[k].ruta)}</td><td class="n">${esc(m.versiones_modelos[k] || "—")}</td><td>${esc(m.archivos_fuente[k].ultimo_commit)}</td><td><code>${esc(m.archivos_fuente[k].sha256.slice(0, 12))}</code></td></tr>`).join("")) +
        `<p style="margin-top:8px">Autoverificación en este navegador: <strong>${autover.ok}/${autover.total}</strong> valores coinciden con los modelos (tabla central del CSV y casos calculados en Python).${autover.ok === autover.total ? " " + badge("modelo") : ' <strong style="color:var(--critico-texto)">Hay diferencias: regenerar datos.</strong>'}</p>`);
  }

  function vEconomia() {
    return `<article class="tarjeta deshabilitado"><h2>Economía del proyecto</h2><p><strong>Disponible en una versión posterior.</strong></p>
      <p>Esta versión (v0.1) es solo física. No se muestran ni se estiman CAPEX, OPEX, precios, ingresos, EBITDA, VAN, TIR, payback ni capital de trabajo monetario, porque esos módulos (19_capex, 20_opex, 21_modelo_financiero) todavía no están construidos. Inventar esas cifras violaría la regla 3 del proyecto («no inventar datos»).</p>
      <p>Cuando existan, esta sección usará los mismos escenarios A/B/C, sin cambiar la estructura del simulador.</p></article>`;
  }

  const VISTAS = { resumen: vResumen, demanda: vDemanda, produccion: vProduccion, planta: vPlanta, productos: vProductos,
    subproductos: vSubproductos, inventario: vInventario, comparador: vComparador, supuestos: vSupuestos, economia: vEconomia };

  function renderVista() {
    const r = resultados[estado.activo];
    const v = $("#vista");
    const global = ["comparador", "supuestos", "economia"].includes(ui.pestana);
    if (!global && !r.ok) {
      v.innerHTML = tarjeta("No se puede calcular este escenario", `<p>Corregí las entradas marcadas en el panel de alertas. El simulador no extrapola fuera de los rangos de los modelos.</p>`);
      return;
    }
    ESC_MAT = !!(r.ok && r.escenario_matematico);
    v.innerHTML = (global ? "" : banderas(r)) + VISTAS[ui.pestana](r);
  }

  function renderPie() {
    const m = DATA.meta;
    $("#pie").innerHTML = `Simulador v${esc(m.simulador_version)} · modelos: escala v${esc(m.versiones_modelos.escala)}, producción v${esc(m.versiones_modelos.produccion)}, balance v${esc(m.versiones_modelos.balance)}, subproductos v${esc(m.versiones_modelos.subproductos)} · datos generados ${esc(m.generado)} (commit ${esc(m.commit_repositorio)}) ·
      autoverificación ${autover.ok}/${autover.total} · ${esc(m.aviso)}`;
  }

  function actualizar(excepto) {
    recalcular();
    syncForm(excepto);
    renderSelector();
    renderAlertas(resultados[estado.activo]);
    renderVista();
    guardar();
  }
  function renderTodo() {
    recalcular();
    renderPanel();
    renderSelector();
    renderPestanas();
    renderAlertas(resultados[estado.activo]);
    renderVista();
    renderPie();
    guardar();
  }

  // ============================================================================================
  // Autoverificación al cargar (el motor reproduce los modelos con los datos embebidos)
  // ============================================================================================
  const autover = (function () {
    let ok = 0, total = 0;
    const cerca = (a, b) => Math.abs(a - b) <= Math.max(1e-6, 1e-9 * Math.max(Math.abs(a), Math.abs(b)));
    DATA.referencia_tabla_central.forEach((x) => {
      total++;
      const r = S.calcular(DATA, Object.assign(S.entradasPorDefecto(DATA), { escala: x.escala, dias_semana: x.dias_semana, dias_anio: x.dias_anio, utilizacion: 1 }));
      if (r.ok && cerca(r.central[x.variable], x.valor)) ok++;
    });
    DATA.casos_prueba.produccion.forEach((c) => {
      const e = c.entrada;
      const r = S.produccion(P, e.aves, e.dias_semana, e.dias_anio, { edad: e.edad, peso: e.peso, fcr: e.fcr, mort: e.mort, doa: e.doa, vacio: e.vacio, kg_m2: e.kg_m2 });
      total++; if (Object.keys(c.salida).every((k) => cerca(r[k], c.salida[k]))) ok++;
    });
    DATA.casos_prueba.demanda.forEach((c) => {
      const e = c.entrada, k = S.kgPorAve(DATA, e.config, e.peso);
      const res = e.metodo === "M0" ? S.resultadoM0(e.demanda_kg_dia_cal, k)
        : S.avesPorMix(e.demanda_kg_dia_cal, DATA.demanda.mixes[e.metodo], DATA.rendimientos_mix[S.clavePeso(e.peso)], DATA.demanda.factor_milanesa, DATA.demanda.rol_mix);
      const cmp = S.compararDemanda(e.escala, e.dias_anio, e.demanda_kg_dia_cal, res);
      total++; if (["factor_demanda_capacidad", "utilizacion_planta", "cobertura_demanda", "kg_no_atendidos_dia_cal", "kg_sin_destino_plena_escala"].every((k) => cerca(cmp[k], c.salida[k]))) ok++;
    });
    return { ok, total };
  })();

  // ============================================================================================
  // Arranque y eventos globales
  // ============================================================================================
  function aplicarTema() {
    const html = document.documentElement;
    if (ui.tema === "auto") html.removeAttribute("data-theme"); else html.setAttribute("data-theme", ui.tema);
    $("#btn-tema").textContent = "Tema: " + { auto: "automático", light: "claro", dark: "oscuro" }[ui.tema];
  }

  cargar();
  aplicarTema();
  enlazarPanel();
  renderTodo();

  $("#leyenda-estados").innerHTML = `<strong>Estado de los datos</strong> — no todos los números tienen la misma certeza:<ul>${Object.keys(ESTADOS).map((k) => `<li>${badge(k)} <span class="pequeno">${esc(ESTADOS[k].tip)}</span></li>`).join("")}</ul>`;
  $("#btn-leyenda").addEventListener("click", (ev) => {
    const l = $("#leyenda-estados"); l.hidden = !l.hidden; ev.currentTarget.setAttribute("aria-expanded", String(!l.hidden));
  });
  $("#btn-tema").addEventListener("click", () => {
    ui.tema = { auto: "light", light: "dark", dark: "auto" }[ui.tema]; aplicarTema(); guardar();
  });
  $("#btn-parametros").addEventListener("click", (ev) => {
    const p = $("#panel-entradas"); p.classList.toggle("abierto"); ev.currentTarget.setAttribute("aria-expanded", String(p.classList.contains("abierto")));
  });
  $("#selector-escenarios").addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-slot]"); if (!b) return;
    estado = S.clonar(estado); estado.activo = b.dataset.slot; renderTodo();
  });
  $("#pestanas").addEventListener("click", (ev) => {
    const b = ev.target.closest("[data-p]"); if (!b) return;
    ui.pestana = b.dataset.p; renderPestanas(); renderVista(); guardar();
  });
  $("#vista").addEventListener("click", (ev) => {
    const ed = ev.target.closest("[data-editar]");
    if (ed) { estado = S.clonar(estado); estado.activo = ed.dataset.editar; renderTodo(); return; }
    const inv = ev.target.closest("[data-inv]");
    if (inv) cambiar("base_inventario", inv.dataset.inv);
  });
})();
