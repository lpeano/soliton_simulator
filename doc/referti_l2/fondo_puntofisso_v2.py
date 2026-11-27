# -*- coding: utf-8 -*-
r"""**[M1540] IL PUNTO FISSO -- LA V2: LA FASE (i) A 6000 TICK PER GIRO, GLI STATI OGNI 100** *(DECISIONE DI LUCA, 2026-11-24 15:40; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-quater`; `fondo_puntofisso.py` e' usato e non si riscrive)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v2.py corsa          (M1540_puntofisso_v2, dalla coda: tre giri)
    E:\python\py3132\python.exe doc/referti_l2/fondo_puntofisso_v2.py lettura > doc/referti_l2/fondo_puntofisso_v2.txt

**Tre differenze, IN MEMORIA:** `K_GIRO = 6000`, `OGNI = 100`, la cartella `M1330/puntofisso_v2`. **Il resto invariato** *(Luca)*: `fondo_puntofisso.giro` e `.corsa` cosi' come sono.
"""
import argparse
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_puntofisso as PF  # noqa: E402

PF.K_GIRO, PF.OGNI = 6000, 100
PF.DIR = os.path.join(PF.CTRL, "M1330", "puntofisso_v2")


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "fondo_puntofisso.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1540] IL PUNTO FISSO, LA V2 (la carta sez. 3-quater): %d tick per giro, w ogni %d; il criterio (w_max - w_min)/w_medio < %.0f%% sull'ultimo giro" % (PF.K_GIRO, PF.OGNI, 100 * PF.SOGLIA))
    print("=" * 130)
    G = []
    for g in range(1, PF.GIRI + 1):
        f = os.path.join(PF.DIR, "giro_%d" % g, "giro.json")
        if not os.path.exists(f + ".sha1"):
            break
        PF.controlla(f)
        G.append(json.load(open(f, encoding="utf-8")))
    for x in G:
        ws = x["w"]
        print("  giro %d: w (k 0, %d, ..., %d): %s" % (x["giro"], PF.OGNI, PF.K_GIRO, " ".join("%.2f" % w for w in ws)))
        print("          i minimi ai k %s; il periodo %s; (max - min)/medio %.4f%s" % (x["minimi_k"], x.get("periodo"), (max(ws) - min(ws)) / float(np.mean(ws)), ("; ### FERMO: " + x["fermo"]) if "fermo" in x else ""))
    if len(G) == PF.GIRI and "fermo" not in G[-1]:
        ws = G[-1]["w"]
        r = (max(ws) - min(ws)) / float(np.mean(ws))
        print("### IL CRITERIO sull'ultimo giro: %.4f %s %.2f: %s" % (r, "<" if r < PF.SOGLIA else ">=", PF.SOGLIA, "PASSA" if r < PF.SOGLIA else "NON PASSA"))
    else:
        print("### IL CRITERIO: NON MISURATO (%d giri su %d)" % (len(G), PF.GIRI))
    print("=" * 130)
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "lettura"))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        import _presidio
        _presidio.avvia(__file__)
        return PF.corsa()
    return lettura()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
