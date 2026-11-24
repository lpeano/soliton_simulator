# -*- coding: utf-8 -*-
r"""**[M0528] LO STATO DELLE CORSE DEL LAPSE RISOLTO, DAL DISCO** *(la domanda di Luca delle `10:54`: per ogni corsa `k` raggiunto, `s/tick`, le iterazioni medie del punto fisso, l'ultimo stato salvato)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/lapse_vincolo_stato.py > doc/referti_l2/lapse_vincolo_stato.txt

**Sola lettura** da `E:/soliton_simulator/controllo/M0528/`. **Il costo del solutore** non e' cronometrato a parte: si stima come la differenza di `s/tick` fra la corsa col vincolo e quella senza **della stessa scena** *(V2V3 x0.8 e x1.2, che differiscono SOLO per il vincolo; la coppia F0 in antifase contro V2V3 in antifase, che differiscono anche per `cs_N` e la fase: la stima piu' grossa)*, ### **con le corse che giravano insieme** *(fino a `9`)*: e' una stima, non un cronometro.
"""
import glob
import json
import os
import re
import sys

import numpy as np

BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0528")


def ultimo(d, pat):
    f = sorted(glob.glob(os.path.join(d, pat)))
    f = [x for x in f if not x.endswith(".sha1")]
    return f[-1] if f else None


def serie(d):
    fz = ultimo(d, "extra_*.npz")
    if fz:
        with np.load(fz) as z:
            return np.asarray(z["it"]), np.asarray(z["s_tick"])
    fj = ultimo(d, "serie_*.json")
    if fj is None:
        return None, None
    S = json.load(open(fj, encoding="utf-8"))
    it = np.asarray(S["it"]) if "it" in S else None
    return it, np.asarray(S["s_tick"]) if "s_tick" in S else None


def main():
    import _presidio
    _presidio.avvia(__file__)
    R = {}
    print("%-28s %-22s %6s %9s %9s %8s" % ("la cartella", "l'ultimo stato", "k", "s/tick", "it medie", "it max"))
    for d in sorted(glob.glob(os.path.join(BASE, "*"))):
        nome = os.path.basename(d)
        if not os.path.isdir(d) or nome == "casi_noti":
            continue
        st = ultimo(d, "stato_*.npz")
        k = int(re.findall(r"(\d+)", os.path.basename(st))[0]) if st else -1
        it, s = serie(d)
        st_ok = st is not None and os.path.exists(st + ".sha1")
        im = "%.3f" % float(np.mean(it)) if it is not None and len(it) else "--"
        ix = "%d" % int(np.max(it)) if it is not None and len(it) else "--"
        ms = float(np.mean(s)) if s is not None and len(s) else float("nan")
        R[nome] = ms
        print("%-28s %-22s %6d %9.3f %9s %8s" % (nome, os.path.basename(st) + (" (sha1)" if st_ok else " (SENZA sha1)") if st else "--", k, ms, im, ix))
    print("### IL COSTO DEL SOLUTORE, STIMATO (col vincolo meno senza, la stessa scena; le corse insieme):")
    for a, b in (("caduta_V2V3_x0.8_vincolo", "caduta_V2V3_x0.8_senza"), ("caduta_V2V3_x1.2_vincolo", "caduta_V2V3_x1.2_senza"), ("coppia_V2V3_180_vincolo", "coppia_F0_180_senza")):
        print("    %s %.3f - %s %.3f = %+.3f s/tick" % (a, R[a], b, R[b], R[a] - R[b]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
