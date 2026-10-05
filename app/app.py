#!/usr/bin/env python3
"""APP V1 del proyecto avícola — interfaz simple + modo experto sobre el Motor V1.

Inicio rápido (un comando, desde la raíz del repo):

    python3 app/app.py                # abre http://127.0.0.1:8765 en el navegador
    python3 app/app.py --puerto 9000 --no-abrir

Detener: Ctrl+C en la terminal. Sin dependencias externas (Python 3.9+ y un navegador). Ver app/README.md.
"""
import argparse
import os
import sys
import threading
import webbrowser

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend import servidor, version  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="App V1 del proyecto avícola (local)")
    ap.add_argument("--puerto", type=int, default=int(os.environ.get("APP_AVICOLA_PUERTO", 8765)))
    ap.add_argument("--host", default="127.0.0.1", help="127.0.0.1 = solo esta computadora (recomendado)")
    ap.add_argument("--no-abrir", action="store_true", help="no abrir el navegador automáticamente")
    a = ap.parse_args()
    i = version.info()
    srv = servidor.crear_servidor(a.host, a.puerto)
    url = f"http://{a.host}:{a.puerto}/"
    print(f"APP AVÍCOLA v{i['version_app']} · commit {i['commit']} ({i['fecha_commit']}) · motor {i['version_motor']}")
    print(f"Abrí en el navegador: {url}")
    print("Para detener: Ctrl+C")
    if not a.no_abrir:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nApp detenida.")
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()
