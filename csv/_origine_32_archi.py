# -*- coding: utf-8 -*-
r"""**L'ORIGINE DEI `32` ARCHI: la dispersione a onde lunghe e il `k` del massimo, DAI DATI GIA' COMMITTATI.**

> ### ⛔ **Il task history e' `2026-10-22_origine_32_archi.md`.** ### **NESSUNA CORSA DEL SIMULATORE:** lo script legge SOLO i `jsonl`
> committati e fa i conti *(`L-NUMERI`: ogni numero del documento `doc/ORIGINE_32_ARCHI.md` esce da qui)*.

## CHE COSA CALCOLA
- ### **`c`, la curvatura della dispersione a onde lunghe** *(`omega ~ (1/2) c k^2`)*: `c = v_g(m=1) / k(m=1)` dai rami dispersivi di
  `v_gruppo_m0` *(`np.gradient`: differenze centrate, quindi la riga `m` e' a `m`)*, ### **a lato `32` e `64`**; e la linearita' di `v_g`
  *(`v_g(2)/v_g(1)`, `v_g(3)/v_g(1)`)*.
- ### **il `k` previsto dal modello minimo** *(il massimo dove `(1/2) c k^2 = gamma`)*: ### **`k = sqrt(2 gamma / c)`**, ### **contro il
  `k` misurato** *(il modulo del `k` del massimo, in unita' di `pi`)*, per ogni braccio `R2` sul quadrato nei referti committati.

Gira con:  python csv/_origine_32_archi.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
sys.path.insert(0, _QUI)

import numpy as np                                             # noqa: E402

D = os.path.join(RADICE, "doc", "referti_l2")
RAMI = (3, 4, 5, 9, 10, 11)    # i rami dispersivi (|v_g| massimo > 0.1, d0_risonanza_bis)
SOGLIA = 1e-3 * 0.4018         # sotto la soglia di stabilita' il k del massimo non vuol dire niente
JSONL = os.path.join(D, "origine_32_archi.jsonl")


def leggi(nome):
    return [json.loads(r) for r in io.open(os.path.join(D, nome), encoding="utf-8") if r.strip()]


def curvatura(nome):
    v = leggi(nome)[0]
    g = np.asarray(v["v_gruppo_m0"])
    L = int(v.get("lato") or 32)
    k1 = 2.0 * np.pi / L
    cc = [abs(g[1, a]) / k1 for a in RAMI if abs(g[1, a]) > 0.0]
    r2 = [abs(g[2, a] / g[1, a]) for a in RAMI if abs(g[1, a]) > 0.0]
    r3 = [abs(g[3, a] / g[1, a]) for a in RAMI if abs(g[1, a]) > 0.0]
    return L, float(np.median(cc)), float(min(cc)), float(max(cc)), float(np.median(r2)), float(np.median(r3))


def kmod(k_pi):
    return float(np.sqrt(sum(x * x for x in k_pi)))


def main(argv):
    del argv
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 100)
    print("L'ORIGINE DEI 32 ARCHI: la dispersione a onde lunghe e il k del massimo, DAI DATI COMMITTATI")
    print("=" * 100)
    io.open(JSONL, "w", encoding="utf-8").close()
    c = {}
    for nome in ("d0_risonanza_bis.jsonl", "d0_risonanza_64.jsonl"):
        L, cm, cmin, cmax, r2, r3 = curvatura(nome)
        c[L] = cm
        print("  %-24s lato %d: c = v_g(1)/k(1) = %.4f (rami dispersivi %.4f-%.4f); v_g(2)/v_g(1) %.3f (lineare: 2),"
              " v_g(3)/v_g(1) %.3f (lineare: 3)" % (nome, L, cm, cmin, cmax, r2, r3))
        with io.open(JSONL, "a", encoding="utf-8") as f:
            f.write(json.dumps({"curvatura": nome, "lato": L, "c": cm, "c_min": cmin, "c_max": cmax,
                                "r2": r2, "r3": r3}) + "\n")
    print("  ### c a lato 64 / c a lato 32 = %.4f" % (c[64] / c[32]))
    print("-" * 100)
    righe = []
    for r in leggi("lineare_s1_s4_scala.jsonl"):
        if "lettura" in r:
            righe.append((r["forma"], 0.1, r["lato"], r["lettura"]["max"], kmod(r["lettura"]["k_pi"]), "cb846b2a"))
    for r in leggi("lineare_s1_s4_materia.jsonl"):
        righe.append((r["forma"], r["x"], 32, r["lettura"]["max"], kmod(r["lettura"]["k_pi"]), "b16e58ba"))
    for r in leggi("screening_forme_s3.jsonl"):
        if "braccio" in r and r["braccio"][1] == "Q":
            f, _g, x = r["braccio"]
            kp = [abs(m if m <= 16 else m - 32) * 2.0 / 32 for m in r["dove"]]
            righe.append((f + " (N100)", x, 32, r["max"], kmod(kp), "389093bc"))
    print("  forma         x       lato  gamma max   k misurato (pi)  k previsto sqrt(2 gamma/c) (pi)  scarto in passi di k")
    tab = []
    for f, x, L, g, km, fonte in sorted(righe, key=lambda t: (t[0], t[1], t[2])):
        if g <= SOGLIA:
            print("  %-12s  %-6g  %-4d  %.5f    %.4f           (sotto la soglia di stabilita': non si legge)" % (f, x, L, g, km))
            continue
        kp = np.sqrt(2.0 * g / c[L]) / np.pi
        passi = (km - kp) / (2.0 / L)
        print("  %-12s  %-6g  %-4d  %.5f    %.4f           %.4f                             %+.2f   [%s]"
              % (f, x, L, g, km, kp, passi, fonte))
        tab.append({"forma": f, "x": x, "lato": L, "gamma": g, "k_misurato": km, "k_previsto": float(kp),
                    "passi": float(passi), "fonte": fonte})
    entro1 = sum(1 for t in tab if abs(t["passi"]) <= 1.0)
    print("-" * 100)
    print("  ### il k misurato entro 1 passo di griglia dal previsto: %d su %d" % (entro1, len(tab)))
    with io.open(JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"tabella": tab, "entro_un_passo": entro1, "c": c}) + "\n")
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
