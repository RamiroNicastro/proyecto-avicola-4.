"""Persistencia local de la app (separada de la evidencia).

  app/datos_locales/escenarios/<id>.json   escenarios guardados (JSON versionado)
  app/datos_locales/staging/cotizaciones_staging.jsonl   datos cargados a mano (cotizaciones, facturas, …) en STAGING
  app/datos_locales/logs/app.log           detalle técnico de errores

Nada de esto se lee como evidencia: la evidencia central (base_precios_venta.csv, base_costos_opex.csv,
inputs_financieros.csv, …) solo cambia con una edición explícita y fuera de la app, con su fuente y su nivel E1–E5.
La carpeta datos_locales/ está en .gitignore (se puede cambiar con la variable APP_AVICOLA_DATOS).
"""
import copy
import json
import os
import re
import uuid

from . import escenario as ES
from . import motor as M
from . import version as V

DATOS = os.environ.get("APP_AVICOLA_DATOS") or os.path.join(M.APP_DIR, "datos_locales")
BASE = os.path.join(M.APP_DIR, "escenarios_base")
TIPOS_DATO = ("cotizacion", "factura", "mercado", "escenario", "otro")
CAMPOS_STAGING = ("concepto", "valor", "unidad", "moneda", "fecha", "fuente", "observaciones", "tipo")


def carpeta(*p):
    d = os.path.join(DATOS, *p)
    os.makedirs(d, exist_ok=True)
    return d


def _ruta_esc(eid):
    if not re.fullmatch(r"[A-Za-z0-9_\-]{1,64}", eid or ""):
        raise ES.ErrorEscenario("Identificador de escenario inválido.")
    return os.path.join(carpeta("escenarios"), f"{eid}.json")


def listar():
    out = []
    for nombre in sorted(os.listdir(BASE)):
        if nombre.endswith(".json"):
            with open(os.path.join(BASE, nombre), encoding="utf-8") as fh:
                e = json.load(fh)
            out.append({"id": e["id"], "nombre": e["nombre"], "tipo": e["tipo"], "solo_demostracion": e.get("solo_demostracion"),
                        "modificado": e.get("modificado"), "origen": "BASE (solo lectura)", "descripcion": e.get("descripcion", "")})
    for nombre in sorted(os.listdir(carpeta("escenarios"))):
        if nombre.endswith(".json"):
            try:
                with open(os.path.join(carpeta("escenarios"), nombre), encoding="utf-8") as fh:
                    e = json.load(fh)
                out.append({"id": e["id"], "nombre": e["nombre"], "tipo": e["tipo"], "solo_demostracion": e.get("solo_demostracion"),
                            "modificado": e.get("modificado"), "origen": "GUARDADO", "descripcion": e.get("descripcion", "")})
            except (OSError, ValueError, KeyError):
                continue
    return out


def leer(eid):
    for d in (BASE, carpeta("escenarios")):
        r = os.path.join(d, f"{eid}.json")
        if os.path.exists(r):
            with open(r, encoding="utf-8") as fh:
                return ES.validar(json.load(fh))
    raise ES.ErrorEscenario(f"No existe el escenario {eid}.")


def guardar(esc):
    esc = ES.validar(esc)
    if os.path.exists(os.path.join(BASE, f"{esc['id']}.json")):
        raise ES.ErrorEscenario("Los escenarios base (presets y demo) son de solo lectura: use DUPLICAR.")
    esc["modificado"] = ES.ahora()
    esc["sello"] = V.sello()
    with open(_ruta_esc(esc["id"]), "w", encoding="utf-8") as fh:
        json.dump(esc, fh, ensure_ascii=False, indent=1)
    return esc


def duplicar(eid, nombre=None):
    e = copy.deepcopy(leer(eid))
    e["id"] = uuid.uuid4().hex[:12]
    e["nombre"] = nombre or f"{e['nombre']} (copia)"
    e["creado"] = e["modificado"] = ES.ahora()
    return guardar(e)


def renombrar(eid, nombre):
    e = leer(eid)
    e["nombre"] = nombre
    return guardar(e)


def eliminar(eid):
    if os.path.exists(os.path.join(BASE, f"{eid}.json")):
        raise ES.ErrorEscenario("Los escenarios base no se pueden eliminar.")
    r = _ruta_esc(eid)
    if not os.path.exists(r):
        raise ES.ErrorEscenario(f"No existe el escenario {eid}.")
    os.remove(r)
    return {"eliminado": eid}


def exportar(esc):
    e = ES.validar(esc)
    e["sello"] = V.sello()
    e["exportado"] = ES.ahora()
    return e


def importar(obj, conservar_id=False):
    e = ES.validar(obj)
    if not conservar_id or os.path.exists(os.path.join(BASE, f"{e['id']}.json")):
        e["id"] = uuid.uuid4().hex[:12]
    e["importado"] = ES.ahora()
    return guardar(e)


# ---------------------------------------------------------------------------------------------
# STAGING de datos cargados a mano (#32): nunca se convierten en E1/E2/E3 ni entran al motor
# ---------------------------------------------------------------------------------------------
def staging_ruta():
    return os.path.join(carpeta("staging"), "cotizaciones_staging.jsonl")


def staging_agregar(d):
    faltan = [c for c in ("concepto", "valor", "unidad", "moneda", "fecha", "fuente", "tipo") if d.get(c) in (None, "")]
    if faltan:
        raise ES.ErrorEscenario("Faltan campos obligatorios: " + ", ".join(faltan))
    if d["tipo"] not in TIPOS_DATO:
        raise ES.ErrorEscenario(f"Tipo {d['tipo']} no admitido {TIPOS_DATO}.")
    try:
        float(d["valor"])
    except (TypeError, ValueError):
        raise ES.ErrorEscenario("El valor debe ser numérico (separador decimal: punto).")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(d["fecha"])):
        raise ES.ErrorEscenario("Fecha en formato AAAA-MM-DD.")
    fila = {c: d.get(c) for c in CAMPOS_STAGING}
    fila.update(id=uuid.uuid4().hex[:10], registrado=ES.ahora(), estado_staging="STAGING_SIN_CLASIFICAR",
                nivel_evidencia="SIN_CLASIFICAR (la clasificación E1–E5 la hace el analista según guia_recoleccion_evidencia.md)",
                incorporado_a_evidencia=False)
    with open(staging_ruta(), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(fila, ensure_ascii=False) + "\n")
    return fila


def staging_listar():
    if not os.path.exists(staging_ruta()):
        return []
    with open(staging_ruta(), encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def log_error(contexto, texto):
    with open(os.path.join(carpeta("logs"), "app.log"), "a", encoding="utf-8") as fh:
        fh.write(f"[{ES.ahora()}] {contexto}\n{texto}\n\n")
