#!/usr/bin/env python3
"""Corre todos los tests de la app: backend + flujos HTTP (unittest) y flujos en navegador (Playwright, si está).

    python3 app/tests/correr_tests.py            # todo
    python3 app/tests/correr_tests.py --sin-ui   # solo Python (sin navegador)

Los datos locales de los tests van a una carpeta temporal: nunca tocan app/datos_locales ni la evidencia.
"""
import argparse
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
APP = os.path.dirname(AQUI)


def puerto_libre():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def modulo_playwright():
    if os.environ.get("PLAYWRIGHT_MODULE"):
        return os.environ["PLAYWRIGHT_MODULE"]
    if not shutil.which("npm"):
        return None
    try:
        raiz = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    m = os.path.join(raiz, "playwright", "index.mjs")
    return m if os.path.exists(m) else None


def correr_ui():
    if not shutil.which("node"):
        print("UI: OMITIDO (node no instalado; los flujos se cubren por HTTP en test_flujos.py)")
        return 0
    mod = modulo_playwright()
    env = dict(os.environ, APP_AVICOLA_DATOS=tempfile.mkdtemp(prefix="app_avicola_ui_"))
    puerto = puerto_libre()
    srv = subprocess.Popen([sys.executable, os.path.join(APP, "app.py"), "--no-abrir", "--puerto", str(puerto)], env=env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        url = f"http://127.0.0.1:{puerto}/"
        for _ in range(100):
            try:
                urllib.request.urlopen(url + "api/estado", timeout=2)
                break
            except OSError:
                time.sleep(0.2)
        env_ui = dict(env, APP_URL=url)
        if mod:
            env_ui["PLAYWRIGHT_MODULE"] = mod
        r = subprocess.run(["node", os.path.join(AQUI, "flujos_ui.mjs")], env=env_ui, timeout=1800)
        if r.returncode == 3:
            print("UI: OMITIDO (playwright no disponible)")
            return 0
        return r.returncode
    finally:
        srv.terminate()
        srv.wait(timeout=10)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sin-ui", action="store_true")
    a = ap.parse_args()
    os.environ.setdefault("APP_AVICOLA_DATOS", tempfile.mkdtemp(prefix="app_avicola_tests_"))
    sys.path.insert(0, APP)
    suite = unittest.defaultTestLoader.discover(AQUI, pattern="test_*.py", top_level_dir=APP)
    res = unittest.TextTestRunner(verbosity=2).run(suite)
    codigo = 0 if res.wasSuccessful() else 1
    if not a.sin_ui:
        print("\nFlujos en navegador (Playwright):")
        codigo = codigo or correr_ui()
    print("\nRESULTADO:", "OK" if codigo == 0 else "FALLAS")
    sys.exit(codigo)


if __name__ == "__main__":
    main()
