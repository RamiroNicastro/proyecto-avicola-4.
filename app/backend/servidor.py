"""Servidor HTTP local (biblioteca estándar; sin dependencias) — API JSON + archivos estáticos de app/web.

Errores: el usuario recibe un mensaje manejable {"ok": false, "error": {"codigo", "mensaje", "ref"}}; el traceback
completo va a app/datos_locales/logs/app.log con la misma referencia. Nunca se envía un traceback a la interfaz.
Concurrencia: las llamadas a los motores se serializan con un lock (los motores usan cachés de módulo).
"""
import json
import mimetypes
import os
import threading
import traceback
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

from . import almacen as A
from . import escenario as ES
from . import exportar as X
from . import motor as M
from . import proyecto as PR
from . import servicios as S
from . import version as V

WEB = os.path.join(M.APP_DIR, "web")
LOCK = threading.RLock()
MAX_BODY = 20 * 1024 * 1024


class ErrorPeticion(Exception):
    pass


def _esc(body):
    e = body.get("escenario")
    if e is None:
        raise ErrorPeticion("Falta el escenario en la petición.")
    return e


def _req(body, k):
    if body.get(k) in (None, ""):
        raise ErrorPeticion(f"Falta el campo {k}.")
    return body[k]


def _id(body):
    return body.get("alternativa") or None


RUTAS_GET = {
    "/api/estado": lambda q: {"version": V.info(), "progreso": PR.progreso(), "cache": dict(S.ESTADISTICAS),
                              "semaforo": S.TX.SEMAFORO, "disclaimer": S.TX.DISCLAIMER},
    "/api/catalogo": lambda q: dict(M.catalogo(), objetivos_simples={k: {"objetivo": o, "texto": t}
                                                                     for k, (o, t) in ES.OBJETIVOS_SIMPLES.items()},
                                    costos_unitarios=ES.COSTOS_UNITARIOS, semaforo=S.TX.SEMAFORO,
                                    alertas=S.TX.CODIGOS_ALERTA, quiebres=[q[0] for q in S.QUIEBRES]),
    "/api/escenarios": lambda q: A.listar(),
    "/api/validacion": lambda q: {"plan": PR.plan_validacion(), "prioridad": PR.prioridad_validacion(), "progreso": PR.progreso()},
    "/api/evidencia": lambda q: PR.evidencia(),
    "/api/trazabilidad": lambda q: PR.trazabilidad(),
    "/api/riesgos_cualitativos": lambda q: PR.riesgos_cualitativos(),
    "/api/staging": lambda q: {"filas": A.staging_listar(), "tipos": list(A.TIPOS_DATO),
                               "nota": "STAGING: datos cargados a mano, SIN clasificar. No son evidencia ni entran al motor."},
}

RUTAS_POST = {
    "/api/nuevo": lambda b: ES.nuevo(b.get("nombre") or "Escenario nuevo"),
    "/api/validar": lambda b: ES.validar(_esc(b)),
    "/api/simular": lambda b: S.simular(_esc(b), _id(b)),
    "/api/comparar": lambda b: S.comparar(_esc(b), b.get("ids") or []),
    "/api/optimizar": lambda b: S.optimizar(_esc(b)),
    "/api/alternativas": lambda b: S.alternativas_resumen(_esc(b)),
    "/api/modulos": lambda b: S.modulos_alternativa(_req(b, "alternativa")),
    "/api/traza": lambda b: S.traza_alternativa(_esc(b), _req(b, "alternativa")),
    "/api/riesgo/sensibilidad": lambda b: S.sensibilidad(_esc(b), _id(b), b.get("variables"), b.get("shocks")),
    "/api/riesgo/tornado": lambda b: S.tornado(_esc(b), _id(b), b.get("metrica") or "VAN", b.get("variables")),
    "/api/riesgo/sens2d": lambda b: S.sensibilidad_2d(_esc(b), _id(b), b.get("vx") or "precio_venta", b.get("vy") or "alimento",
                                                      b.get("shocks")),
    "/api/riesgo/stress": lambda b: S.stress(_esc(b), _id(b), b.get("stresses")),
    "/api/riesgo/quiebres": lambda b: S.quiebres(_esc(b), _id(b)),
    "/api/riesgo/montecarlo": lambda b: S.montecarlo(_esc(b), _id(b), b.get("n"), b.get("semilla")),
    "/api/costo_unitario": lambda b: S.costo_unitario(_esc(b), _req(b, "alternativa"), _req(b, "concepto"), _req(b, "precio")),
    "/api/escenarios": lambda b: A.guardar(_esc(b)),
    "/api/escenarios/importar": lambda b: A.importar(_esc(b)),
    "/api/exportar/json": lambda b: A.exportar(_esc(b)),
    "/api/staging": lambda b: A.staging_agregar(b.get("dato") or {}),
}

RUTAS_TEXTO = {   # respuestas no JSON
    "/api/exportar/csv": ("text/csv; charset=utf-8", lambda b: X.csv_resultado(_esc(b), _id(b))),
    "/api/exportar/resumen": ("text/html; charset=utf-8", lambda b: X.resumen_html(_esc(b), _id(b))),
}


def manejar(metodo, ruta, body=None):
    """Despacho sin HTTP (lo usan los tests de flujo). Devuelve (status, tipo, contenido)."""
    try:
        with LOCK:
            if metodo == "GET" and ruta in RUTAS_GET:
                return 200, "json", {"ok": True, "datos": S._limpio(RUTAS_GET[ruta]({}))}
            if metodo == "GET" and ruta.startswith("/api/escenarios/"):
                return 200, "json", {"ok": True, "datos": A.leer(ruta.rsplit("/", 1)[1])}
            if metodo == "GET" and ruta.startswith("/api/documento/"):
                try:
                    return 200, "json", {"ok": True, "datos": {"texto": PR.documento(ruta.rsplit("/", 1)[1])}}
                except KeyError:
                    raise ErrorPeticion("Documento no disponible desde la app.")
            if metodo == "POST" and ruta in RUTAS_POST:
                return 200, "json", {"ok": True, "datos": S._limpio(RUTAS_POST[ruta](body or {}))}
            if metodo == "POST" and ruta in RUTAS_TEXTO:
                tipo, fn = RUTAS_TEXTO[ruta]
                return 200, tipo, fn(body or {})
            if metodo == "POST" and ruta.startswith("/api/escenarios/") and ruta.endswith("/duplicar"):
                return 200, "json", {"ok": True, "datos": A.duplicar(ruta.split("/")[3], (body or {}).get("nombre"))}
            if metodo == "POST" and ruta.startswith("/api/escenarios/") and ruta.endswith("/renombrar"):
                return 200, "json", {"ok": True, "datos": A.renombrar(ruta.split("/")[3], (body or {}).get("nombre") or "sin nombre")}
            if metodo == "DELETE" and ruta.startswith("/api/escenarios/"):
                return 200, "json", {"ok": True, "datos": A.eliminar(ruta.rsplit("/", 1)[1])}
        return 404, "json", {"ok": False, "error": {"codigo": "NO_ENCONTRADO", "mensaje": f"Ruta {ruta} inexistente."}}
    except (ES.ErrorEscenario, ErrorPeticion) as e:
        msg = str(e).strip("'")
        cod = msg.split(":")[0] if msg.split(":")[0].isupper() and "_" in msg.split(":")[0] else "ENTRADA_INVALIDA"
        return 400, "json", {"ok": False, "error": {"codigo": cod, "mensaje": msg}}
    except (M.mf.ErrorFinanciero, M.mr.ErrorRiesgo, M.mcx.ErrorCapex, M.mo.ErrorOpex) as e:
        ref = uuid.uuid4().hex[:8]
        A.log_error(f"{ref} {metodo} {ruta} (motor)", traceback.format_exc())
        cod = "OVERRIDE_INCOMPATIBLE" if M.mf.OVERRIDE_INCOMPATIBLE in str(e) else "MOTOR_RECHAZO_LA_ENTRADA"
        return 422, "json", {"ok": False, "error": {"codigo": cod, "mensaje": S.TX.mensaje_error_motor(e), "ref": ref}}
    except Exception:   # noqa: BLE001 — se registra y se responde con un mensaje de usuario
        ref = uuid.uuid4().hex[:8]
        A.log_error(f"{ref} {metodo} {ruta}", traceback.format_exc())
        return 500, "json", {"ok": False, "error": {"codigo": "ERROR_INTERNO", "ref": ref,
                                                    "mensaje": f"Ocurrió un error interno (referencia {ref}). El detalle técnico "
                                                               "quedó en app/datos_locales/logs/app.log."}}


class Manejador(BaseHTTPRequestHandler):
    server_version = "AppAvicola/" + V.APP_VERSION

    def log_message(self, fmt, *args):     # consola limpia; los errores van al log
        pass

    def _responder(self, status, tipo, contenido):
        if tipo == "json":
            data = json.dumps(contenido, ensure_ascii=False, default=str).encode("utf-8")
            ct = "application/json; charset=utf-8"
        else:
            data = contenido.encode("utf-8") if isinstance(contenido, str) else contenido
            ct = tipo
        self.send_response(status)
        self.send_header("Content-Type", ct)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _estatico(self, ruta):
        rel = "index.html" if ruta in ("/", "") else unquote(ruta.lstrip("/"))
        dest = os.path.realpath(os.path.join(WEB, rel))
        if not dest.startswith(os.path.realpath(WEB)) or not os.path.isfile(dest):
            return self._responder(404, "text/plain; charset=utf-8", "no encontrado")
        tipo = mimetypes.guess_type(dest)[0] or "application/octet-stream"
        if tipo.startswith("text/") or tipo in ("application/javascript",):
            tipo += "; charset=utf-8"
        with open(dest, "rb") as fh:
            self._responder(200, tipo, fh.read())

    def _body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n > MAX_BODY:
            raise ErrorPeticion("Petición demasiado grande.")
        raw = self.rfile.read(n) if n else b"{}"
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except ValueError:
            raise ErrorPeticion("El cuerpo de la petición no es JSON válido.")

    def do_GET(self):
        ruta = urlparse(self.path).path
        if ruta.startswith("/api/"):
            return self._responder(*manejar("GET", ruta))
        return self._estatico(ruta)

    def do_POST(self):
        ruta = urlparse(self.path).path
        try:
            body = self._body()
        except ErrorPeticion as e:
            return self._responder(400, "json", {"ok": False, "error": {"codigo": "ENTRADA_INVALIDA", "mensaje": str(e)}})
        return self._responder(*manejar("POST", ruta, body))

    def do_DELETE(self):
        return self._responder(*manejar("DELETE", urlparse(self.path).path))


def crear_servidor(host="127.0.0.1", puerto=8765):
    return ThreadingHTTPServer((host, puerto), Manejador)
