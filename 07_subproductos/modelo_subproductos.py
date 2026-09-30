#!/usr/bin/env python3
"""
Escenarios físicos de productos, coproductos y subproductos — Fase 0 (prefactibilidad)
Versión 1.0 · 2026-09-30

QUÉ HACE
  1. Lee el balance de masa v1.1 (../04_balance_masa/modelo_balance_masa.py) SIN modificarlo
     y verifica que sus 21 tests sigan pasando.
  2. Agrupa cada componente del balance en un GRUPO de material (cada componente pertenece a
     un solo grupo: no hay doble conteo) para 6 variantes de configuración y ruta.
  3. Escala los grupos a 2.500 / 5.000 / 10.000 / 20.000 aves faenadas por día (250 días de
     faena/año, SUP-025/SUP-044) y escribe escenarios_subproductos.csv.
  4. Agrega filas DERIVADAS (sumable = "no"): materia prima potencial de rendering, CMS
     potencial alternativa a la venta de esqueleto, sangre drenada, pluma biológica, días para
     completar 25 t de garras grado A. Estas filas NUNCA se suman al control de cierre.
  5. Verifica que los kg/ave declarados en matriz_valorizacion.csv (esta carpeta) y en
     ../06_productos/matriz_productos.csv coincidan con el balance (trazabilidad, regla 15).

QUÉ NO HACE
  No asigna precios, no calcula ingresos, no elige rutas, no dimensiona equipos ni rendering.
  Las escalas son escenarios, no capacidad (regla 9).

UNIDADES
  kg por ave (masa biológica y agua por separado; "total" = biológica + agua incorporada a
  productos y subproductos, SUP-042); t/día por día de faena; t/año = t/día × 250.
  Peso de referencia: 2,9 kg vivo en planta, rendimiento y condenas "medio", chiller por inmersión.

USO
  python3 07_subproductos/modelo_subproductos.py            # tests + CSV
  python3 07_subproductos/modelo_subproductos.py --solo-tests

FORMATO DE LA COLUMNA ref_modelo DE LAS MATRICES (para el test de trazabilidad)
  "V1:higado+corazon+molleja"   suma de masa biológica de esos componentes en la variante V1
  "V1:pata-muslo*0.58"          ídem multiplicado por un factor (muslo = 58 % de la pata-muslo, SUP-038)
  "V1:plumas crudas#total"      masa biológica + agua
  "PRIM:patas"                  componente primario del ave (antes de condenas y acondicionamiento)
  "GRASA"                       grasa abdominal dentro de la carcasa (no separada por defecto)
  "-"                           sin kg por ave (producto elaborado, servicio o salida fuera del balance)
"""
import argparse
import csv
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(RAIZ, "04_balance_masa"))
import modelo_balance_masa as mb  # noqa: E402  (balance v1.1, no se modifica)

VERSION = "1.0"
FECHA = "2026-09-30"
PESO, REND, COND, ENF = 2.9, "medio", "medio", "inmersion"
AVES_DIA = mb.AVES_DIA                     # [2500, 5000, 10000, 20000]
DIAS = mb.DIAS_FAENA_ANIO                  # 250
TOL = 1e-9                                 # kg/ave
TOL_MATRIZ = 0.0006                        # kg/ave: las matrices redondean a 3 decimales
CARGA_CONTENEDOR_T = 25.0                  # t por reefer de 40' ([PVDP · débil], 17_exportacion)

# Variantes: (configuración, rutas, descripción). V1 = referencia del estudio.
VARIANTES = {
    "V1": ("B", {}, "Trozado; carcasa-esqueleto vendida (referencia)"),
    "V2": ("B", {"esqueleto": "cms"}, "Trozado; carcasa-esqueleto a CMS"),
    "V3": ("C", {}, "Deshuesado; carcasa-esqueleto a CMS (defecto de C)"),
    "V4": ("C", {"esqueleto": "venta"}, "Deshuesado; carcasa-esqueleto vendida"),
    "V5": ("C", {"esqueleto": "cms", "cuello": "cms", "hueso_pechuga": "cms", "piel": "rendering"},
           "Deshuesado; esqueleto, cuello y hueso de pechuga a CMS; piel a rendering"),
    "V6": ("A", {}, "Pollo entero"),
}

# Componente del balance -> (id de grupo, nombre del grupo). Cada componente en UN solo grupo.
GRUPO = {
    "pollo entero": ("G01", "Producto principal (A)"),
    "pechuga con hueso": ("G01", "Producto principal (A)"),
    "pata-muslo": ("G01", "Producto principal (A)"),
    "suprema": ("G01", "Producto principal (A)"),
    "solomillo": ("G01", "Producto principal (A)"),
    "muslo deshuesado": ("G01", "Producto principal (A)"),
    "pata con hueso": ("G01", "Producto principal (A)"),
    "pata deshuesada": ("G01", "Producto principal (A)"),
    "alas": ("G02", "Alas"),
    "carcasa-esqueleto": ("G03", "Carcasa-esqueleto vendida"),
    "CMS": ("G04", "CMS"),
    "piel": ("G05", "Piel vendida"),
    "recortes": ("G06", "Recortes"),
    "higado": ("G07", "Menudencias (hígado + corazón + molleja)"),
    "corazon": ("G07", "Menudencias (hígado + corazón + molleja)"),
    "molleja": ("G07", "Menudencias (hígado + corazón + molleja)"),
    "cuello": ("G08", "Cuello"),
    "garras grado A": ("G09", "Garras grado A + segunda"),
    "garras de segunda": ("G09", "Garras grado A + segunda"),
    "plumas crudas": ("G10", "Plumas crudas húmedas"),
    "sangre recuperada": ("G11", "Sangre recuperada"),
    "tracto digestivo": ("G12", "Vísceras no comestibles (tracto + pulmones + otros)"),
    "pulmones": ("G12", "Vísceras no comestibles (tracto + pulmones + otros)"),
    "otros no comestibles": ("G12", "Vísceras no comestibles (tracto + pulmones + otros)"),
    "cabeza": ("G13", "Cabezas"),
    "hueso": ("G14", "Huesos y residuo óseo de CMS"),
    "residuo oseo de CMS": ("G14", "Huesos y residuo óseo de CMS"),
    "piel a rendering": ("G15", "Piel a rendering"),
    "garras descarte": ("G16", "Garras de descarte"),
    "grasa abdominal retirada": ("G17", "Grasa abdominal retirada"),
    "contenido gastrointestinal": ("G18", "Contenido gastrointestinal"),
    "decomiso total": ("G19", "Decomisos (total + parcial)"),
    "decomiso parcial": ("G19", "Decomisos (total + parcial)"),
    "sangre no recuperada": ("G20", "Sangre no recuperada"),
    "merma de acondicionamiento de patas": ("G21", "Merma de acondicionamiento de patas (cutícula)"),
    "agua de goteo del producto": ("G22", "Agua de goteo del producto"),
    "merma de trozado": ("G23", "Mermas de proceso (trozado, deshuese, CMS, evaporación)"),
    "merma de deshuese": ("G23", "Mermas de proceso (trozado, deshuese, CMS, evaporación)"),
    "merma de CMS": ("G23", "Mermas de proceso (trozado, deshuese, CMS, evaporación)"),
    "evaporacion en enfriamiento": ("G23", "Mermas de proceso (trozado, deshuese, CMS, evaporación)"),
    "perdidas no asignadas": ("G24", "Pérdidas no asignadas"),
}

# Familia para el escalado físico pedido (sección 20 del encargo) y clasificación económica
# de REFERENCIA (la clase puede cambiar si no hay comprador: ver mapa_subproductos.md §2).
FAMILIA = {
    "G01": "producto principal", "G02": "coproducto de trozado", "G03": "coproducto de trozado",
    "G04": "CMS", "G05": "piel", "G06": "recortes", "G07": "menudencias", "G08": "menudencias",
    "G09": "garras", "G10": "plumas", "G11": "sangre", "G12": "visceras", "G13": "cabezas",
    "G14": "huesos", "G15": "piel", "G16": "garras", "G17": "grasa", "G18": "residuo",
    "G19": "residuo", "G20": "residuo", "G21": "residuo", "G22": "residuo", "G23": "perdida",
    "G24": "perdida",
}


def balances():
    out = {}
    for v, (cfg, rutas, _) in VARIANTES.items():
        b = mb.balance(PESO, cfg, REND, COND, ENF, rutas)
        mb.verificar_cierre(b)
        out[v] = b
    return out


def agrupar(b):
    """{gid: [nombre, clase_balance, bio, agua]}; falla si un componente no tiene grupo (T2)."""
    g = {}
    for f in b["filas"]:
        if f["componente"] not in GRUPO:
            raise KeyError(f"Componente sin grupo: {f['componente']}")
        gid, nombre = GRUPO[f["componente"]]
        if gid not in g:
            g[gid] = [nombre, f["clase"], 0.0, 0.0]
        elif g[gid][1] != f["clase"]:
            raise ValueError(f"Grupo {gid} mezcla clases {g[gid][1]} y {f['clase']}")
        g[gid][2] += f["bio"]
        g[gid][3] += f["agua"]
    return g


def comp(b, nombres, total=False):
    return sum(f["bio"] + (f["agua"] if total else 0.0) for f in b["filas"] if f["componente"] in nombres)


def valor_ref(ref, bals):
    """Interpreta la columna ref_modelo de las matrices (ver docstring)."""
    ref = ref.strip()
    if ref in ("", "-"):
        return None
    if ref == "GRASA":
        return mb.fraccion_grasa(PESO) * PESO
    if ref.startswith("PRIM:"):
        return mb.fracciones_primarias(PESO, REND)[ref[5:]] * PESO
    v, expr = ref.split(":", 1)
    total = expr.endswith("#total")
    expr = expr.replace("#total", "")
    factor = 1.0
    if "*" in expr:
        expr, f = expr.split("*")
        factor = float(f)
    return comp(bals[v], set(expr.split("+")), total) * factor


def filas_csv(bals):
    filas = []

    def escala(kg):
        d = {f"t_dia_{n}": kg * n / 1000 for n in AVES_DIA}
        d["t_anio_10000"] = kg * 10000 * DIAS / 1000
        return d

    for v, b in bals.items():
        cfg, rutas, desc = VARIANTES[v]
        ruta = mb.resolver_rutas(cfg, rutas)
        base = {"variante": v, "descripcion_variante": desc, "configuracion": cfg,
                "ruta_esqueleto": ruta["esqueleto"], "ruta_cuello": ruta["cuello"],
                "ruta_hueso_pechuga": ruta["hueso_pechuga"], "ruta_piel": ruta["piel"]}
        for gid, (nombre, clase, bio, agua) in sorted(agrupar(b).items()):
            tot = bio + agua
            filas.append({**base, "grupo_id": gid, "material": nombre, "familia": FAMILIA[gid],
                          "clase_balance": clase, "tipo_fila": "grupo", "sumable": "si",
                          "masa_biologica_kg_ave": bio, "agua_kg_ave": agua, "total_kg_ave": tot,
                          "pct_peso_vivo_bio": 100 * bio / PESO, **escala(tot),
                          "nota": ""})
        # Filas derivadas (NO sumables)
        c_tot = sum(f["bio"] + f["agua"] for f in b["filas"] if f["clase"] == "C")
        c_bio = sum(f["bio"] for f in b["filas"] if f["clase"] == "C")
        ampl = comp(b, {"decomiso total", "decomiso parcial", "contenido gastrointestinal"})
        der = [
            ("D01", "Materia prima potencial de rendering (toda la clase C)", c_bio, c_tot - c_bio,
             "Suma de grupos C; solo tiene valor con comprador o rendering habilitado (DEC-027)"),
            ("D02", "Materia prima de rendering ampliada (C + decomisos + contenido GI)", c_bio + ampl,
             c_tot - c_bio, "Solo si la normativa permite enviar decomisos y contenido al digestor (DPV-066)"),
            ("D03", "Sangre drenada total (recuperada + no recuperada)",
             comp(b, {"sangre recuperada", "sangre no recuperada"}), 0.0, "Base para comparar recuperación"),
            ("D04", "Plumas: masa biológica (sin agua adherida)", comp(b, {"plumas crudas"}), 0.0,
             "La harina depende de la materia seca real (DPV-065)"),
            ("D05", "Garras grado A (solo)", comp(b, {"garras grado A"}), 0.0, "Incluida en G09"),
        ]
        if ruta["esqueleto"] == "venta":
            # misma regla que el balance: CMS = rendimiento de CMS × materia prima (SUP-039)
            cms_alt = comp(b, {"carcasa-esqueleto"}) * mb.CMS_RENDIMIENTO[REND]
            der.append(("D06", "CMS potencial si el esqueleto fuera a CMS (ALTERNATIVA, excluyente con G03)",
                        cms_alt, 0.0, "No sumar con la carcasa-esqueleto vendida (rutas exclusivas, SUP-045)"))
        ga = comp(b, {"garras grado A"})
        for gid, nombre, bio, agua, nota in der:
            tot = bio + agua
            filas.append({**base, "grupo_id": gid, "material": nombre, "familia": "derivada",
                          "clase_balance": "-", "tipo_fila": "derivada", "sumable": "no",
                          "masa_biologica_kg_ave": bio, "agua_kg_ave": agua, "total_kg_ave": tot,
                          "pct_peso_vivo_bio": 100 * bio / PESO, **escala(tot), "nota": nota})
        dias = {f"t_dia_{n}": CARGA_CONTENEDOR_T * 1000 / (ga * n) for n in AVES_DIA}
        filas.append({**base, "grupo_id": "D07", "material": "Días de faena para completar 25 t de garras grado A",
                      "familia": "derivada", "clase_balance": "-", "tipo_fila": "derivada (días, no t/día)",
                      "sumable": "no", "masa_biologica_kg_ave": ga, "agua_kg_ave": 0.0, "total_kg_ave": ga,
                      "pct_peso_vivo_bio": 100 * ga / PESO, **dias, "t_anio_10000": "",
                      "nota": "Columnas t_dia_* contienen DÍAS de faena; carga del reefer [PVDP · débil]"})
        # Control
        s_bio = sum(r["masa_biologica_kg_ave"] for r in filas if r["variante"] == v and r["sumable"] == "si")
        s_agua = sum(r["agua_kg_ave"] for r in filas if r["variante"] == v and r["sumable"] == "si")
        filas.append({**base, "grupo_id": "CTRL", "material": "CONTROL: suma de grupos sumables",
                      "familia": "control", "clase_balance": "-", "tipo_fila": "control", "sumable": "-",
                      "masa_biologica_kg_ave": s_bio, "agua_kg_ave": s_agua, "total_kg_ave": s_bio + s_agua,
                      "pct_peso_vivo_bio": 100 * s_bio / PESO, **escala(s_bio + s_agua),
                      "nota": f"Entrada: PV {b['entrada_bio']:.4f} + agua {b['entrada_agua']:.4f}; "
                              f"error {s_bio + s_agua - b['entrada_bio'] - b['entrada_agua']:.2e} kg/ave"})
    return filas


CAMPOS = ["variante", "descripcion_variante", "configuracion", "ruta_esqueleto", "ruta_cuello",
          "ruta_hueso_pechuga", "ruta_piel", "grupo_id", "material", "familia", "clase_balance", "tipo_fila",
          "sumable", "masa_biologica_kg_ave", "agua_kg_ave", "total_kg_ave", "pct_peso_vivo_bio",
          "t_dia_2500", "t_dia_5000", "t_dia_10000", "t_dia_20000", "t_anio_10000", "nota"]


def escribir(filas, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CAMPOS)
        w.writeheader()
        for r in filas:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})


def leer_matriz(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tests(bals, filas, verbose=True):
    res = []

    def chk(n, c, d=""):
        res.append((n, bool(c), d))

    base = mb.ejecutar_tests(verbose=False)
    chk("S01 balance v1.1 intacto: sus 21 tests pasan", all(r for _, r, _ in base) and len(base) == 21,
        f"{sum(r for _, r, _ in base)}/{len(base)}")
    err = max(abs(r["total_kg_ave"] - bals[r["variante"]]["entrada_bio"] - bals[r["variante"]]["entrada_agua"])
              for r in filas if r["tipo_fila"] == "control")
    chk("S02 cierre: Σ grupos sumables = PV + agua incorporada en cada variante", err < TOL, f"error máx {err:.1e}")
    ok = True
    for b in bals.values():
        try:
            agrupar(b)
        except (KeyError, ValueError):
            ok = False
    chk("S03 cada componente del balance en un solo grupo y una sola clase", ok)
    ok = True
    for v, b in bals.items():
        g = agrupar(b)
        ruta = mb.resolver_rutas(VARIANTES[v][0], VARIANTES[v][1])
        cms_esq = sum(f["bio"] for f in b["filas"] if f["etapa"] == "CMS (esqueleto)")
        vend = g.get("G03", [0, 0, 0.0])[2]
        ok &= not (vend > 0 and cms_esq > 0)
        ok &= (ruta["esqueleto"] == "venta") == (vend > 0)
        ok &= not (g.get("G05", [0, 0, 0.0])[2] > 0 and g.get("G15", [0, 0, 0.0])[2] > 0)
    chk("S04 rutas exclusivas: esqueleto vendido XOR CMS de esqueleto; piel vendida XOR a rendering", ok)
    ok = all(r["sumable"] == "no" for r in filas if r["tipo_fila"].startswith("derivada"))
    chk("S05 filas derivadas (rendering potencial, CMS alternativa, días de garras) no sumables", ok)
    ok = all(r["masa_biologica_kg_ave"] >= 0 and r["agua_kg_ave"] >= 0 for r in filas)
    chk("S06 ninguna masa negativa", ok)
    # S07: escalado lineal
    ok = all(abs(r["t_dia_10000"] - r["total_kg_ave"] * 10) < 1e-9 for r in filas
             if r["tipo_fila"] in ("grupo", "control", "derivada"))
    chk("S07 escalado lineal (t/día = kg/ave × aves/día / 1000)", ok)
    d06 = next(r["masa_biologica_kg_ave"] for r in filas if r["variante"] == "V1" and r["grupo_id"] == "D06")
    cms_v2 = sum(f["bio"] for f in bals["V2"]["filas"] if f["etapa"] == "CMS (esqueleto)" and f["componente"] == "CMS")
    chk("S09 CMS potencial (fila derivada de V1) = CMS de la variante V2 calculada por el balance",
        abs(d06 - cms_v2) < TOL, f"{d06:.4f} vs {cms_v2:.4f}")
    # S08: trazabilidad de las matrices
    detalle, ok, n = [], True, 0
    for ruta in (os.path.join(AQUI, "matriz_valorizacion.csv"),
                 os.path.join(RAIZ, "06_productos", "matriz_productos.csv")):
        m = leer_matriz(ruta)
        if m is None:
            ok = False
            detalle.append(f"falta {os.path.basename(ruta)}")
            continue
        for r in m:
            val = valor_ref(r["ref_modelo"], bals)
            if val is None:
                ok &= r["kg_ave"].strip() in ("", "-")
                continue
            n += 1
            if abs(float(r["kg_ave"]) - val) > TOL_MATRIZ:
                ok = False
                detalle.append(f"{r.get('id', '?')}: {r['kg_ave']} vs modelo {val:.4f}")
    chk("S08 kg/ave de matriz_valorizacion.csv y matriz_productos.csv = balance v1.1", ok,
        f"{n} valores verificados" + ("; " + "; ".join(detalle[:5]) if detalle else ""))
    if verbose:
        print(f"\nTESTS — modelo_subproductos.py v{VERSION}")
        for nombre, r, d in res:
            print(f"  [{'OK ' if r else 'FALLA'}] {nombre}" + (f"  ({d})" if d else ""))
        print(f"  Resultado: {sum(r for _, r, _ in res)}/{len(res)} correctos\n")
    return res


def imprimir(filas):
    print("Pollo de 2,9 kg, medio, inmersión — t/día (masa biológica + agua)")
    for v in VARIANTES:
        print(f"\n{v} — {VARIANTES[v][2]}")
        print(f"  {'material':72s} {'kg/ave':>7s} {'2.500':>6s} {'5.000':>6s} {'10.000':>7s} {'20.000':>7s}")
        for r in filas:
            if r["variante"] == v and r["tipo_fila"] in ("grupo", "derivada", "control"):
                mark = "" if r["sumable"] != "no" else " *"
                print(f"  {r['grupo_id']} {r['material'][:66]:66s}{mark:2s} {r['total_kg_ave']:7.4f} "
                      f"{r['t_dia_2500']:6.2f} {r['t_dia_5000']:6.2f} {r['t_dia_10000']:7.2f} {r['t_dia_20000']:7.2f}")
    print("\n  * fila derivada, no sumable")


def main():
    ap = argparse.ArgumentParser(description="Escenarios físicos de subproductos (Fase 0)")
    ap.add_argument("--solo-tests", action="store_true")
    ap.add_argument("--imprimir", action="store_true")
    a = ap.parse_args()
    bals = balances()
    filas = filas_csv(bals)
    res = tests(bals, filas)
    if not all(r for _, r, _ in res):
        print("DETENIDO: al menos una prueba falló. No se genera el CSV.")
        sys.exit(1)
    if a.solo_tests:
        return
    ruta = os.path.join(AQUI, "escenarios_subproductos.csv")
    escribir(filas, ruta)
    print(f"CSV generado: {ruta} ({len(filas)} filas)")
    if a.imprimir:
        imprimir(filas)


if __name__ == "__main__":
    main()
