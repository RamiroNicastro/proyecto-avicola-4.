"""Versión de la app, del motor y del commit (#47). Toda simulación exportada lleva este sello."""
import os
import subprocess
from datetime import date

from . import motor as M

APP_VERSION = "1.1.0"
APP_FECHA = "2026-10-05"
_CACHE = {}


def _git(*args):
    try:
        return subprocess.run(["git", *args], cwd=M.RAIZ, capture_output=True, text=True, timeout=5).stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def info():
    if not _CACHE:
        commit = _git("rev-parse", "--short", "HEAD")
        sucio = bool(_git("status", "--porcelain", "--", "21_modelo_financiero", "22_riesgos", "19_capex", "20_opex"))
        _CACHE.update({"version_app": APP_VERSION, "fecha_app": APP_FECHA, "version_motor": M.versiones_motor(),
                       "commit": commit or "desconocido", "fecha_commit": _git("log", "-1", "--format=%cs") or "desconocida",
                       "rama": _git("rev-parse", "--abbrev-ref", "HEAD") or "desconocida",
                       "motor_con_cambios_locales": sucio, "fecha_ejecucion": date.today().isoformat()})
    return dict(_CACHE)


def sello():
    i = info()
    return {"version_app": i["version_app"], "version_motor": i["version_motor"], "commit": i["commit"],
            "fecha_commit": i["fecha_commit"], "motor_con_cambios_locales": i["motor_con_cambios_locales"]}
