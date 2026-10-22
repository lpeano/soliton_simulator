# -*- coding: utf-8 -*-
r"""**DA DOVE VIENE LA MASSA DELLA CAMMINATA? `Delta` e `c` in funzione dello spostamento parziale `s = dtau`** *(`cs` spento)*.

> ### ⛔ **Il task history e' `2026-10-22_massa_spostamento.md`.** ### **`dtau` e `eps` SOLO nella scena, a griglia FISSA** *(in memoria)*;
> ### **`leggi.yaml` e l'impronta intatti.** Le funzioni sono quelle di `csv/_moneta_massa.py` *(`dispersione`, `fit_massa`)*: ### **la stessa
> misura, a `dtau` diversi.**

Gira con:  python csv/_massa_spostamento.py
"""
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.dirname(_QUI)
_PO = os.path.join(RADICE, "primo_ordine")
for _p in (_QUI, _PO, os.path.join(_PO, "leggi")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import numpy as np                                             # noqa: E402

LATI = (32, 64)
EPS_LISTA = (0.5, 0.0)
DTAU_LISTA = (0.03125, 0.0625, 0.125, 0.25, 0.5, 1.0)
PICCOLI = (0.03125, 0.0625, 0.125)
TOLL = 0.05
C_82 = {32: 0.3894, 64: 0.3882}
JSONL = os.path.join(RADICE, "doc", "referti_l2", "massa_spostamento.jsonl")
OK = [0, 0]


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    print("  %-82s %s   %s" % (che[:82], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def rel(v):
    v = [x for x in v if np.isfinite(x)]
    return (max(v) - min(v)) / abs(np.mean(v)) if v else float("inf")


def main(argv):
    del argv
    import _moneta_massa as MM
    import _presidio
    _presidio.avvia(__file__)
    import composizione as CM
    print("=" * 100)
    print("DA DOVE VIENE LA MASSA DELLA CAMMINATA? Delta e c in funzione di s = dtau (cs spento), a griglia fissa")
    print("=" * 100)
    print("  il passo: %d pezzi, impronta %s (intatto); la camminata sola esatta; i rami dispersivi della materia;"
          " il fit sqrt(Delta^2 + v^2 k^2) - Delta fino a 0.25 pi" % (len(CM.ORDINE), CM.IMPRONTA))
    print("-" * 100)
    sys.stdout.flush()
    io.open(JSONL, "w", encoding="utf-8").close()
    out = {}
    for L in LATI:
        k1 = 2.0 * np.pi / L
        for eps in EPS_LISTA:
            for dt in DTAU_LISTA:
                kk, vg, rm, vgm = MM.dispersione(L, dt, eps)
                cc = [abs(vg[1, a]) / k1 for a in MM.RAMI if abs(vg[1, a]) > 0.0]
                c_ref = float(np.median(cc)) if cc else float("nan")
                disp = [b for b in range(rm.shape[1]) if float(np.max(np.abs(vgm[:, b]))) > 0.1]
                sel = kk <= 0.25 * np.pi + 1e-12
                f = [MM.fit_massa(kk[sel], rm[sel, b] - rm[0, b]) for b in disp]
                r21 = [float(abs(vgm[2, b] / vgm[1, b])) for b in disp if vgm[1, b]]
                cv1 = [abs(vgm[1, b]) / k1 for b in disp]
                r = {"lato": L, "eps": eps, "dtau": dt, "s": dt, "c_ref": c_ref, "dispersivi": len(disp),
                     "Delta": float(np.median([x[0] for x in f])) if f else float("nan"),
                     "v": float(np.median([x[1] for x in f])) if f else float("nan"),
                     "scarto_fit": max([x[2] for x in f], default=float("nan")),
                     "c": float(np.median(cv1)) if cv1 else float("nan"),
                     "r21": float(np.median(r21)) if r21 else float("nan")}
                out[(L, eps, dt)] = r
                print("  lato %d eps %-4g s = dtau %-8g: c(82b40ca1) %.4f; materia %d rami: Delta %.5f, v %.5f, c %.5f,"
                      " v_g(2)/v_g(1) %.3f, fit %.3f" % (L, eps, dt, c_ref, len(disp), r["Delta"], r["v"], r["c"], r["r21"],
                                                       r["scarto_fit"]))
                sys.stdout.flush()
                with io.open(JSONL, "a", encoding="utf-8") as fh:
                    fh.write(json.dumps(r) + "\n")
    print("-" * 100)
    for L in LATI:
        esito("DEVE RIUSCIRE: lato %d eps 0.5 dtau 0.125, la c di 82b40ca1 entro 1e-4" % L,
              abs(out[(L, 0.5, 0.125)]["c_ref"] - C_82[L]) <= 1e-4,
              "%.5f contro %.4f" % (out[(L, 0.5, 0.125)]["c_ref"], C_82[L]))
    print("### LE LETTURE (a eps 0)")
    let = {}
    for L in LATI:
        D = [out[(L, 0.0, dt)]["Delta"] for dt in DTAU_LISTA]
        C = [out[(L, 0.0, dt)]["c"] for dt in DTAU_LISTA]
        Dp = [out[(L, 0.0, dt)]["Delta"] for dt in PICCOLI]
        Cp = [out[(L, 0.0, dt)]["c"] for dt in PICCOLI]
        r1 = out[(L, 0.0, 1.0)]["r21"]
        tutti = rel(D) <= TOLL and rel(C) <= TOLL
        piccoli = rel(Dp) <= TOLL and rel(Cp) <= TOLL
        lineare = abs(r1 - 1.0) <= TOLL
        parab = abs(r1 - 2.0) <= 2 * TOLL
        salto = all(out[(L, 0.0, dt)]["Delta"] > 0.05 * np.mean(Dp) for dt in DTAU_LISTA if dt < 1.0)
        if tutti:
            v = "GROVER (Delta e c non dipendono da s)"
        elif piccoli and lineare and salto:
            v = "S E' LA MASSA (secondo la previsione: costanti a s piccolo, lineare a s = 1)"
        else:
            v = "NON DECIDIBILE"
        print("  lato %d: Delta su tutti gli s %s (scarto %.3f); c %s (scarto %.3f); a s piccolo Delta %.3f c %.3f; a s = 1"
              " v_g(2)/v_g(1) %.3f -> %s; il salto c'e' per s < 1? %s -> ### %s"
              % (L, ["%.3f" % x for x in D], rel(D), ["%.4f" % x for x in C], rel(C), rel(Dp), rel(Cp), r1,
                 "LINEARE" if lineare else ("PARABOLICA" if parab else "NE' L'UNA NE' L'ALTRA"), salto, v))
        let[L] = {"Delta": D, "c": C, "scarto_D": rel(D), "scarto_c": rel(C), "scarto_D_piccoli": rel(Dp),
                  "scarto_c_piccoli": rel(Cp), "r21_s1": r1, "lineare_s1": bool(lineare), "salto": bool(salto),
                  "verdetto": v}
    print("### IL CONTO DI DIMENSIONI, COI NUMERI")
    for L in LATI:
        print("  lato %d, eps 0.5: c per unita' di tempo a dtau 0.03125/0.0625/0.125: %s; v: %s" % (
            L, ["%.4f" % out[(L, 0.5, dt)]["c"] for dt in PICCOLI], ["%.4f" % out[(L, 0.5, dt)]["v"] for dt in PICCOLI]))
    with io.open(JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"letture": {str(k): v for k, v in let.items()}}) + "\n")
    print("=" * 100)
    print("LA MASSA DALLO SPOSTAMENTO: %d su %d controlli   %s" % (OK[0], OK[1], "### TUTTI PASSATI" if OK[0] == OK[1]
                                                                  else "### CI SONO BUCHI"))
    print("=" * 100)
    return 0 if OK[0] == OK[1] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
