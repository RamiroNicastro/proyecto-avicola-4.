"""Exportación de un escenario y su resultado (#48, #49): CSV y resumen ejecutivo imprimible (HTML listo para PDF).

No genera PowerPoint. Todo lo exportado lleva el sello de versión (app, motor, commit), la etiqueta del universo
(SIMULACION_HIPOTETICA_NO_VALIDADA / CASO_PRUEBA_ARTIFICIAL_NO_ES_PROYECTO) y el disclaimer.
"""
import csv
import html
import io

from . import escenario as ES
from . import presentacion as TX
from . import servicios as S
from . import version as V


def _fmt(v, formato):
    if v is None:
        return ""
    if formato == "usd":
        return f"{v:,.0f}"
    if formato == "pct":
        return f"{v * 100:.2f} %"
    if formato in ("anios", "veces", "num"):
        return f"{v:.2f}"
    if formato == "t":
        return f"{v:,.1f}"
    return str(v)


def _plano(prefijo, x, out):
    if isinstance(x, dict):
        for k, v in x.items():
            _plano(f"{prefijo}.{k}" if prefijo else str(k), v, out)
    elif isinstance(x, list):
        if all(not isinstance(v, (dict, list)) for v in x):
            out.append((prefijo, "|".join("" if v is None else str(v) for v in x)))
        else:
            for i, v in enumerate(x):
                _plano(f"{prefijo}[{i}]", v, out)
    else:
        out.append((prefijo, "" if x is None else x))


def csv_resultado(esc, aid=None):
    esc = ES.validar(esc)
    sim = S.simular(esc, aid)
    etiqueta = sim.get("etiqueta")
    filas = [("SELLO", k, str(v), "", "", "") for k, v in V.sello().items()]
    filas += [("ESCENARIO", "nombre", esc["nombre"], "", "", etiqueta), ("ESCENARIO", "tipo", esc["tipo"], "", "", etiqueta),
              ("ESCENARIO", "solo_demostracion", str(bool(esc.get("solo_demostracion"))), "", "", etiqueta)]
    simples = []
    _plano("simple", esc["simple"], simples)
    filas += [("INPUT_SIMPLE", k, v, "", "ESCENARIO", etiqueta) for k, v in simples]
    if sim.get("resultado") == "ALTERNATIVA":
        filas.append(("RESULTADO", "alternativa", sim["alternativa"]["id"], "", "", etiqueta))
        for card in sim["tarjetas"]:
            for it in card["items"]:
                if it.get("estado") in ("TEXTO", "SEMAFORO"):
                    filas.append(("RESULTADO", f"{card['titulo']} · {it['etiqueta']}", it.get("texto"), "", it["estado"], etiqueta))
                else:
                    falta = "; ".join(f"{f['texto']}" for f in it.get("faltan") or [])
                    filas.append(("RESULTADO", f"{card['titulo']} · {it['etiqueta']}", _fmt(it.get("valor"), it.get("formato")),
                                  it.get("formato"), it["estado"] + (f" — {falta}" if falta else ""), etiqueta))
        for b, xs in (sim["detalle"].get("faltantes") or {}).items():
            for x in xs:
                filas.append(("FALTANTE", b, x, "", "PENDIENTE", etiqueta))
    else:
        filas.append(("DECISION", "resultado", sim.get("resultado"), "", "", etiqueta))
        ni = sim.get("no_invertir") or {}
        filas.append(("DECISION", ni.get("titulo", ""), ni.get("texto", ""), "", "", etiqueta))
    for a in sim.get("alertas") or []:
        filas.append(("ALERTA", a["codigo"], a["texto"], "", "", etiqueta))
    filas.append(("DISCLAIMER", "", TX.DISCLAIMER, "", "", ""))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["SECCION", "CAMPO", "VALOR", "UNIDAD_O_FORMATO", "ESTADO", "ETIQUETA"])
    w.writerows(filas)
    return buf.getvalue()


def _e(x):
    return html.escape("" if x is None else str(x))


def resumen_html(esc, aid=None):
    """Resumen ejecutivo imprimible del escenario (#49)."""
    esc = ES.validar(esc)
    sim = S.simular(esc, aid)
    sello = V.sello()
    demo = esc.get("solo_demostracion")
    marca = "SOLO DEMOSTRACIÓN — DATOS FICTICIOS" if demo else "SIMULACIÓN HIPOTÉTICA — NO VALIDADA"
    partes = [f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Resumen de escenario</title><style>
body{{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1d2433;background:#fff;margin:0;padding:24px 32px;font-size:13px;line-height:1.45}}
h1{{font-size:20px;margin:0 0 4px}}h2{{font-size:15px;margin:22px 0 8px;border-bottom:1px solid #d5dbe6;padding-bottom:4px}}
.marca{{border:2px dashed #b45309;color:#92400e;background:#fffbeb;padding:8px 12px;font-weight:700;letter-spacing:.04em;margin:10px 0}}
table{{border-collapse:collapse;width:100%;margin:6px 0}}td,th{{border:1px solid #e1e6ef;padding:4px 6px;text-align:left;vertical-align:top}}
th{{background:#f3f5f9}}.nc{{color:#9a3412;font-weight:600}}.mut{{color:#5b6475}}.disc{{margin-top:24px;border-top:1px solid #d5dbe6;padding-top:8px}}
@media print{{body{{padding:0}}.noprint{{display:none}}}}</style></head><body>
<button class="noprint" onclick="window.print()">Imprimir / guardar PDF</button>
<h1>Resumen de escenario: {_e(esc['nombre'])}</h1>
<div class="mut">App {_e(sello['version_app'])} · motor {_e(', '.join(f'{k} {v}' for k, v in sello['version_motor'].items()))} ·
commit {_e(sello['commit'])} ({_e(sello['fecha_commit'])}) · etiqueta {_e(sim.get('etiqueta'))}</div>
<div class="marca">{marca}</div>"""]
    s = esc["simple"]
    filas = []
    _plano("", {k: v for k, v in s.items() if k not in ("demanda", "precios_venta", "costos_unitarios")}, filas)
    partes.append("<h2>Inputs principales</h2><table>" + "".join(f"<tr><th>{_e(k)}</th><td>{_e(v)}</td></tr>" for k, v in filas) + "</table>")
    if s["demanda"]:
        partes.append("<table><tr><th>Producto</th><th>Canal</th><th>Categoría</th><th>Volumen</th></tr>" + "".join(
            f"<tr><td>{_e(l['producto'])}</td><td>{_e(l['canal'])}</td><td>{_e(l['categoria'])}</td><td>{_e(l.get('valor'))} {_e(l['unidad'])}"
            f"{' (toma todo)' if l.get('toma_todo') else ''}</td></tr>" for l in s["demanda"]) + "</table>")
    if s["precios_venta"]:
        partes.append("<table><tr><th>Precio</th><th>Valor</th><th>Estado</th><th>Fuente</th></tr>" + "".join(
            f"<tr><td>{_e(p['producto'])} · {_e(p['canal'])}</td><td>{_e(p.get('valor'))} {_e(p.get('moneda'))}/kg</td>"
            f"<td>{_e(p['estado'])}</td><td>{_e(p.get('fuente'))}</td></tr>" for p in s["precios_venta"]) + "</table>")
    if sim.get("resultado") == "ALTERNATIVA":
        fj = sim["alternativa"]
        partes.append(f"<h2>Arquitectura evaluada</h2><p>{_e(fj['id'])} — {_e(TX.CONFIG_TITULO.get(fj['configuracion'], ''))}</p>")
        partes.append("<h2>Resultados</h2><table>")
        for card in sim["tarjetas"]:
            for it in card["items"]:
                if it.get("estado") in ("TEXTO", "SEMAFORO"):
                    val = _e(it.get("texto"))
                elif it["estado"] == "VALOR":
                    val = _e(_fmt(it["valor"], it["formato"])) + (f"<div class='mut'>{_e(it.get('explicacion'))}</div>" if it.get("explicacion") else "")
                else:
                    val = f"<span class='nc'>{_e(it['estado'].replace('_', ' '))}</span>" + "".join(
                        f"<div class='mut'>{_e(f['texto'])}</div>" for f in it.get("faltan") or [])
                partes.append(f"<tr><th>{_e(card['titulo'])} · {_e(it.get('etiqueta'))}</th><td>{val}</td></tr>")
        partes.append("</table>")
        try:
            tor = S.tornado(esc, fj["id"], "VAN", ["precio_venta", "alimento", "demanda", "capex", "utilizacion", "dias_cobro"])
            if tor["calculable"]:
                partes.append("<h2>Sensibilidad (VAN, one-way)</h2><table><tr><th>Variable</th><th>Amplitud del VAN</th></tr>" + "".join(
                    f"<tr><td>{_e(t['VARIABLE'])}</td><td>{_e(_fmt(t.get('SWING'), 'usd'))}</td></tr>"
                    for t in tor["tornado"] if t.get("SWING") is not None) + "</table>")
            else:
                partes.append(f"<h2>Sensibilidad</h2><p class='nc'>{_e(tor['nota'])}</p>")
            st = S.stress(esc, fj["id"])
            partes.append("<h2>Riesgos (stress)</h2><table><tr><th>Stress</th><th>Estado</th><th>VAN</th><th>Δ VAN</th></tr>" + "".join(
                f"<tr><td>{_e(r['NOMBRE'])}</td><td>{_e(r['ESTADO'])}</td><td>{_e(_fmt(r.get('VAN'), 'usd'))}</td>"
                f"<td>{_e(_fmt(r.get('DELTA_VAN'), 'usd'))}</td></tr>" for r in st["filas"]) + "</table>")
        except ES.ErrorEscenario as e:
            partes.append(f"<p class='nc'>{_e(e)}</p>")
        falt = sim["detalle"].get("faltantes") or {}
        partes.append("<h2>Evidencia y faltantes</h2>" + f"<p>Cobertura de evidencia: {_e(_fmt(fj.get('cobertura_evidencia'), 'pct'))} — "
                      f"{_e(fj.get('cobertura_nota'))}</p>")
        if falt:
            partes.append("<ul>" + "".join(f"<li><b>{_e(b)}</b>: {_e('; '.join(x))}</li>" for b, x in falt.items()) + "</ul>")
        partes.append("<h2>Qué hacer ahora</h2><ol>" + "".join(f"<li>{_e(a['accion'])} <span class='mut'>{_e(a.get('dpv'))}</span></li>"
                                                              for a in sim.get("que_hacer") or []) + "</ol>")
    else:
        ni = sim.get("no_invertir") or {}
        partes.append(f"<h2>{_e(ni.get('titulo'))}</h2><p>{_e(ni.get('texto'))}</p><p class='mut'>{_e(ni.get('por_que'))}</p>"
                      + "".join(f"<div>{_e(r)}</div>" for r in ni.get("reglas") or []))
    partes.append("<h2>Alertas</h2><ul>" + "".join(f"<li><b>{_e(a['codigo'])}</b> — {_e(a['texto'])}</li>" for a in sim.get("alertas") or []) + "</ul>")
    partes.append(f"<div class='disc'><b>Aviso.</b> {_e(TX.DISCLAIMER)}</div></body></html>")
    return "\n".join(partes)
