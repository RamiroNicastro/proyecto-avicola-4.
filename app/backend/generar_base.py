"""Genera app/escenarios_base/: presets estructurales (sin valores económicos) y el DEMO_ARTIFICIAL.

    python3 app/backend/generar_base.py

Los presets NO tienen precios, costos, demanda ni capital: solo nombre, objetivo, perfil de análisis y la plantilla de
curva de ramp-up ILUSTRATIVA del motor (SUP-196, rotulada SUPUESTO_MODELO por el propio motor).
"""
import json
import os
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend import demo, escenario as ES, motor as M     # noqa: E402
else:
    from . import demo, escenario as ES, motor as M

PRESETS = (
    ("preset_conservador", "PRESET CONSERVADOR (estructura vacía)", "REDUCIR_RIESGO", "PLANTILLA_CONSERVADOR",
     "Estructura para un escenario prudente: objetivo robustez, curva de arranque lenta ilustrativa. SIN valores económicos."),
    ("preset_base", "PRESET BASE (estructura vacía)", "GANAR_MAS", "PLANTILLA_BASE",
     "Estructura para un escenario central: objetivo VAN, curva de arranque ilustrativa BASE. SIN valores económicos."),
    ("preset_expansivo", "PRESET EXPANSIVO (estructura vacía)", "CRECER", "PLANTILLA_EXPANSIVO",
     "Estructura para un escenario de crecimiento: objetivo capacidad, trayectorias multietapa habilitadas. SIN valores económicos."),
)


def presets():
    out = []
    for eid, nombre, obj, plantilla, desc in PRESETS:
        e = ES.nuevo(nombre, "PRESET")
        e["id"], e["descripcion"] = eid, desc
        e["creado"] = e["modificado"] = "2026-10-05T00:00:00"
        e["simple"]["objetivo"] = obj
        e["experto"]["plantilla"] = plantilla
        e["experto"]["trayectorias"] = eid == "preset_expansivo"
        out.append(ES.validar(e))
    return out


def demo_fijo():
    e = demo.escenario_demo()
    e["creado"] = e["modificado"] = "2026-10-05T00:00:00"
    return e


def escribir(carpeta=None):
    carpeta = carpeta or os.path.join(M.APP_DIR, "escenarios_base")
    os.makedirs(carpeta, exist_ok=True)
    for e in presets() + [demo_fijo()]:
        with open(os.path.join(carpeta, f"{e['id']}.json"), "w", encoding="utf-8") as fh:
            json.dump(e, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
    return carpeta


if __name__ == "__main__":
    print("escenarios base en", escribir())
