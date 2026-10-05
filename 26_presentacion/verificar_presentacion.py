"""Verificación del paquete ejecutivo V1 (26_presentacion). Solo biblioteca estándar.

Uso:  python3 26_presentacion/verificar_presentacion.py

Controla que el PPTX abra como paquete OOXML, que cada lámina tenga notas, que los mensajes clave estén en
todas las piezas, que no haya placeholders ni rutas técnicas en las láminas, que no aparezcan montos ni
rentabilidades, que las cifras centrales coincidan con la auditoría final del motor y que cada fuente del
CSV de trazabilidad exista. Sale con código 1 si algún control falla.
"""
import csv
import re
import sys
import zipfile
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
PPTX = AQUI / "presentacion_nicas_doipe_v1.pptx"
AUDITORIA = RAIZ / "00_gestion_proyecto" / "auditoria_final_motor_v1.md"

resultados = []


def control(nombre, ok, detalle=""):
    resultados.append((nombre, bool(ok), detalle))


def texto_xml(xml):
    return " ".join(re.findall(r"<a:t>([^<]*)</a:t>", xml))


def numero(nombre):
    return int(re.search(r"(\d+)\.xml$", nombre).group(1))


# 1. El PPTX abre y tiene la estructura esperada
with zipfile.ZipFile(PPTX) as z:
    control("P01 PPTX es un zip OOXML íntegro", z.testzip() is None and "ppt/presentation.xml" in z.namelist())
    slides = sorted([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)], key=numero)
    notas = {numero(n): texto_xml(z.read(n).decode("utf-8")) for n in z.namelist() if re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", n)}
    rels = {numero(n.replace("_rels/", "").replace(".rels", "")): z.read(n).decode("utf-8") for n in z.namelist() if re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", n)}
    textos = {numero(n): texto_xml(z.read(n).decode("utf-8")) for n in slides}

control("P02 entre 18 y 24 láminas principales + anexo de 5 a 8", 23 <= len(slides) <= 32, f"{len(slides)} láminas")
# cada lámina tiene su notesSlide con texto sustantivo
sin_notas = []
for i in textos:
    r = rels.get(i, "")
    m = re.search(r'Target="\.\./notesSlides/notesSlide(\d+)\.xml"', r)
    if not m or len(notas.get(int(m.group(1)), "")) < 120:
        sin_notas.append(i)
control("P03 todas las láminas tienen notas del presentador", not sin_notas, f"sin notas: {sin_notas}")

todo = " ".join(textos.values())

# 2. Mensajes clave
claves = [("MOTOR V1", "COMPLETO ESTRUCTURALMENTE"), ("APP V1", "LISTA"), ("DECISIÓN REAL", "NO")]
for n in (1, 2, len(textos) - 6):  # portada, mensaje ejecutivo, conclusión (antes del anexo)
    t = textos[n]
    falta = [a for a, b in claves if a not in t or b not in t]
    control(f"M0{n if n < 3 else 3} mensajes clave en la lámina {n}", not falta, f"faltan: {falta}")
for doc in ("guion_presentacion.md", "resumen_ejecutivo_1_pagina.md", "README.md"):
    t = (AQUI / doc).read_text(encoding="utf-8")
    ok = ("COMPLETO ESTRUCTURALMENTE" in t) and ("LISTA" in t) and (("LISTO_DECISION_REAL = NO" in t) or ("LISTO PARA DECISIÓN REAL" in t and "**NO**" in t))
    control(f"M04 mensajes clave en {doc}", ok)

# 3. Sin placeholders ni rutas técnicas en las láminas
control("C01 sin placeholders", not re.search(r"lorem|ipsum|\bxxx+\b|\[insert|TODO:|TBD", todo, re.I))
control("C02 sin rutas técnicas en las láminas", not re.search(r"\b[\w/-]+\.(py|csv|json|md)\b|00_gestion_proyecto|app/app\.py", todo))

# 4. Sin montos inventados ni rentabilidades
montos = re.findall(r"(?:USD|US\$|\$)\s?[\d.,]+\s?(?:M|millones|mil)?", todo)
control("C03 el único monto en USD es la referencia de 2 M", all(re.sub(r"\s", "", m) in ("USD2M",) for m in montos), f"{montos}")
control("C04 ninguna rentabilidad publicada (VAN/TIR/payback con cifra)",
        not re.search(r"(VAN|TIR|payback|EBITDA)\s*(=|:|de)\s*-?\s*(USD\s*)?\d", todo, re.I))
control("C05 no afirma demanda asegurada de los supermercados",
        not re.search(r"supermercados[^.]{0,40}(son|como) demanda asegurada", todo, re.I) and "Los ~90 supermercados están acá hoy" in todo)
control("C06 no recomienda invertir", not re.search(r"recomend\w+ (invertir|la inversión)|conviene invertir\b(?! *$)", todo.replace("Si conviene invertir", ""), re.I))
control("C07 USD 2 M siempre como referencia no comprometida", "no comprometido" in todo and "no se compara contra USD 2 M" in todo.replace("Por eso no se compara", "no se compara"))
control("C08 explica que el motor simula con datos cargados", "Sí puede simular" in todo)

# 5. Consistencia con la auditoría final del motor
aud = AUDITORIA.read_text(encoding="utf-8")
pares = [
    ("70/70 tests de integración", "70 / 70"), ("15/15 mutaciones", "15 / 15"), ("0 de 61 corridas", None),
    ("0 de 54 alternativas", "0 de 54"), ("180 DPV, **ninguno validado**", "0 de 180"), ("104 DEC, **todas abiertas**", "104 decisiones"),
    ("**76** (71 abiertas, 4 corregidas", "71 abiertas"), ("0 de 624 celdas verificadas", "0 de 624"),
]
for en_aud, en_deck in pares:
    ok = en_aud in aud and (en_deck is None or en_deck in todo)
    control(f"A01 auditoría «{en_aud}» ↔ deck «{en_deck}»", ok)
control("A02 conclusión de la auditoría = no recomienda", "no** recomienda una inversión" in aud or "no recomienda comprar" in aud)

# 6. Trazabilidad
filas = list(csv.DictReader(open(AQUI / "fuentes_y_trazabilidad_presentacion.csv", encoding="utf-8")))
faltan = [f["ID"] for f in filas if not (RAIZ / f["DOCUMENTO_FUENTE"]).exists()]
control("T01 cada fuente del CSV existe en el repo", filas and not faltan, f"{len(filas)} filas; faltan {faltan}")
control("T02 etiquetas del CSV válidas", all(f["ETIQUETA"] in {"ESTADO", "ESTIMACIÓN", "ESCENARIO", "PENDIENTE", "SUPUESTO", "EVIDENCIA"} for f in filas))
for cap in ("app_inicio.png", "app_simular.png", "app_estado.png", "app_validacion.png"):
    control(f"T03 captura {cap} presente", (AQUI / "capturas" / cap).exists())

ok_total = all(ok for _, ok, _ in resultados)
for nombre, ok, det in resultados:
    print(("OK   " if ok else "FALLA") + "  " + nombre + (f"  ({det})" if det and not ok else ""))
print(f"\n{sum(ok for _, ok, _ in resultados)}/{len(resultados)} controles OK")
sys.exit(0 if ok_total else 1)
