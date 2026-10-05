#!/usr/bin/env python3
"""
CORRIDA DE TODAS LAS SUITES DEL MOTOR v1 — sesión 21 (auditoría final), 2026-10-05
==================================================================================

Corre las suites vigentes de cada módulo (tests y, donde existen, mutaciones), el validador del simulador HTML y los
tests de integración final, y escribe `registro_tests_final.csv` (SUITE, MODULO, COMANDO, TESTS, MUTACIONES,
RESULTADO, OBSERVACIONES). No modifica modelos. Las suites de 03 y 14 no tienen modo "solo tests": regeneran su CSV
(idéntico mientras el código no cambie) y luego prueban.

Uso
    python3 00_gestion_proyecto/correr_suites_motor.py            # todas (las mutaciones de 22 tardan ~6 min)
    python3 00_gestion_proyecto/correr_suites_motor.py --rapido   # sin las suites de mutaciones
Termina con código 1 si alguna suite falla.
"""
import argparse
import csv
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SALIDA = os.path.join(AQUI, "registro_tests_final.csv")
PY = sys.executable

# (suite, módulo, comando, tipo, patrón de conteo, observaciones)
#   tipo: TESTS | MUTACIONES; patrón: regex con grupos (ok, total) o "contar:<regex ok>|<regex falla>"
SUITES = [
    ("03", "Producción primaria", [PY, "03_produccion_primaria/modelo_escenarios_produccion.py"], "TESTS",
     r"contar:^\s*\[OK\]|^\s*\[FALLA\]", "10 chequeos sobre 72–216 casos; regenera escenarios_produccion.csv (idéntico)"),
    ("04", "Balance de masa", [PY, "04_balance_masa/modelo_balance_masa.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) correctos", ""),
    ("07", "Productos y subproductos", [PY, "07_subproductos/modelo_subproductos.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) correctos", ""),
    ("23", "Escala", [PY, "23_plan_expansion/modelo_escala.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) correctos", ""),
    ("23m", "Escala", [PY, "23_plan_expansion/modelo_escala.py", "--mutaciones"], "MUTACIONES", r"Mutaciones detectadas: (\d+)/(\d+)", ""),
    ("05", "Proceso industrial", [PY, "05_proceso_industrial/modelo_capacidad_proceso.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) tests correctos", ""),
    ("05m", "Proceso industrial", [PY, "05_proceso_industrial/modelo_capacidad_proceso.py", "--mutaciones"], "MUTACIONES", r"(\d+)/(\d+) mutaciones detectadas", ""),
    ("11", "Agua, efluentes, energía y frío", [PY, "11_agua_efluentes/modelo_utilities.py", "--solo-tests"], "TESTS",
     r"contar:^\s+OK\s+U\d+|^\s+FALLA\s+U\d+", "un mismo modelo cubre 11 y 12"),
    ("11m", "Agua, efluentes, energía y frío", [PY, "11_agua_efluentes/modelo_utilities.py", "--mutaciones"], "MUTACIONES",
     r"contar:DETECTADA por|NO DETECTADA", ""),
    ("10", "Localización", [PY, "10_localizacion/modelo_localizacion.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) pruebas superadas", ""),
    ("13", "Logística", [PY, "13_logistica/modelo_logistica.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) pruebas OK", ""),
    ("09", "Layout y obra civil", [PY, "09_layout_obra_civil/modelo_superficies.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) tests OK", ""),
    ("09m", "Layout y obra civil", [PY, "09_layout_obra_civil/modelo_superficies.py", "--mutaciones"], "MUTACIONES", r"(\d+)/(\d+) mutaciones detectadas", ""),
    ("18", "Recursos humanos", [PY, "18_recursos_humanos/modelo_rrhh.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) tests OK", ""),
    ("18m", "Recursos humanos", [PY, "18_recursos_humanos/modelo_rrhh.py", "--mutaciones"], "MUTACIONES", r"(\d+)/(\d+) mutaciones detectadas", ""),
    ("14", "Upstream (incubación, alimento, integración)", [PY, "14_alimento_balanceado/modelo_upstream.py"], "TESTS",
     r"contar:^\s*\[OK\] U\d+|^\s*\[FALLA\] U\d+", "regenera su CSV (idéntico) y prueba; un modelo cubre 14 y 15"),
    ("19", "CAPEX", [PY, "19_capex/modelo_capex.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) tests OK", ""),
    ("19m", "CAPEX", [PY, "19_capex/modelo_capex.py", "--mutaciones"], "MUTACIONES", r"contar:\[DETECTADA\]|\[NO DETECTADA\]", ""),
    ("20", "OPEX y capital de trabajo", [PY, "20_opex/modelo_opex.py", "--solo-tests"], "TESTS", r"(\d+)/(\d+) tests OK", ""),
    ("20m", "OPEX y capital de trabajo", [PY, "20_opex/modelo_opex.py", "--mutaciones"], "MUTACIONES", r"contar:\[DETECTADA\]|\[NO DETECTADA\]", ""),
    ("21", "Modelo financiero", [PY, "21_modelo_financiero/modelo_financiero.py", "--solo-tests"], "TESTS", r"Tests: (\d+)/(\d+) OK", ""),
    ("21m", "Modelo financiero", [PY, "21_modelo_financiero/modelo_financiero.py", "--mutaciones"], "MUTACIONES", r"Mutaciones detectadas: (\d+)/(\d+)", ""),
    ("22", "Riesgo y optimizador", [PY, "22_riesgos/modelo_optimizador.py", "--solo-tests"], "TESTS", r"Tests: (\d+)/(\d+) OK", ""),
    ("22m", "Riesgo y optimizador", [PY, "22_riesgos/modelo_optimizador.py", "--mutaciones"], "MUTACIONES", r"Mutaciones detectadas: (\d+)/(\d+)",
     "escribe 22_riesgos/cobertura_mutaciones.csv"),
    ("sim", "Simulador HTML v0.1", ["node", "validar_simulador.js"], "TESTS", r"(\d+)/(\d+) correctos", "se corre desde 23_plan_expansion/simulador_html"),
    ("INT", "Integración final del motor", [PY, "00_gestion_proyecto/tests_integracion_motor.py"], "TESTS", r"Tests: (\d+)/(\d+) OK",
     "tests de integración final (sesión 21)"),
    ("INTm", "Integración final del motor", None, "MUTACIONES", r"Mutaciones detectadas: (\d+)/(\d+)", "mutaciones de integración (misma corrida que INT)"),
]
NO_CORRIDAS = [
    ("08", "Maquinaria conceptual", "sin suite propia: catálogo consumido y probado por 19 (CAPEX)"),
    ("16", "Normativa", "documental, sin modelo"),
    ("01/17", "Mercado y exportación", "documentales, sin modelo (exportación = módulo futuro de mercado)"),
    ("02", "Demanda", "escenarios en CSV; probados por 21 (E08, F02, F10) e integración (DM01–DM03)"),
]


def contar(patron, texto):
    if patron.startswith("contar:"):
        ok_re, falla_re = patron[len("contar:"):].split("|")
        ok = len(re.findall(ok_re, texto, re.M))
        falla = len(re.findall(falla_re, texto, re.M))
        return ok, ok + falla
    m = re.findall(patron, texto)
    return (int(m[-1][0]), int(m[-1][1])) if m else (None, None)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--rapido", action="store_true", help="omite las suites de mutaciones")
    a = ap.parse_args()
    filas, fallo, salida_int = [], False, ""
    for suite, modulo, cmd, tipo, patron, obs in SUITES:
        if a.rapido and tipo == "MUTACIONES" and suite != "INTm":
            continue
        if cmd is None:
            texto, rc = salida_int, 0
        else:
            cwd = os.path.join(RAIZ, "23_plan_expansion", "simulador_html") if suite == "sim" else RAIZ
            p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
            texto, rc = p.stdout + p.stderr, p.returncode
            if suite == "INT":
                salida_int = texto
        ok, tot = contar(patron, texto)
        res = "OK" if rc == 0 and ok is not None and ok == tot and tot > 0 else "FALLA"
        fallo |= res != "OK"
        print(f"  [{res}] {suite:5s} {modulo}: {ok}/{tot} {tipo.lower()}")
        filas.append({"SUITE": suite, "MODULO": modulo,
                      "COMANDO": " ".join(["python3" if c == PY else c for c in cmd]) if cmd else "(incluida en INT)",
                      "TESTS": f"{ok}/{tot}" if tipo == "TESTS" else "", "MUTACIONES": f"{ok}/{tot}" if tipo == "MUTACIONES" else "",
                      "RESULTADO": res, "OBSERVACIONES": obs})
    for suite, modulo, obs in NO_CORRIDAS:
        filas.append({"SUITE": suite, "MODULO": modulo, "COMANDO": "—", "TESTS": "", "MUTACIONES": "", "RESULTADO": "NO_APLICA",
                      "OBSERVACIONES": obs})
    if not a.rapido:
        with open(SALIDA, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, ["SUITE", "MODULO", "COMANDO", "TESTS", "MUTACIONES", "RESULTADO", "OBSERVACIONES"],
                               lineterminator="\n")
            w.writeheader()
            w.writerows(filas)
        print(f"registro_tests_final.csv: {len(filas)} filas")
    if fallo:
        sys.exit(1)


if __name__ == "__main__":
    main()
