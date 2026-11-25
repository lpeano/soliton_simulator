# -*- coding: utf-8 -*-
r"""**[M0237-3] LA SOGLIA DI NASCITA A META' E A DOPPIO** *(DECISIONE DI LUCA, 2026-11-25 02:37, dalla posta; la carta `doc/CARTA_mitosi.md`, «Le tre prove»; la formula `N(s) = N_1 / s` scritta PRIMA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia.py corsa --s 0.5     (0.5 e 2: 6000 tick da prima_nascita_35976; dalla coda, dopo [M0137])
    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia.py noto              (K3: soglia 1, da 35976 a 36250, contro MITOSI al bit; dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia.py lettura > doc/referti_l2/mitosi_soglia.txt

**La corsa** e' `mitosi_lunga.corsa` cosi' com'e', con la sorgente `mitosi_rami/TRONCO/prima_nascita_35976.npz` e **una sola differenza, in memoria: `solitone.contatore.QUANTO = s 2 pi`** *(un arco scatta a `|Theta| >= QUANTO`; `scattati()` la legge a ogni chiamata)*. Le uscite in `E:/soliton_simulator/controllo/M0237/soglia_<s>/` *(la cartella si crea prima: `mitosi_lunga.corsa` non la crea)*. **La lettura:** le nascite per finestra di `500` a soglia `0.5`, `1` *(MITOSI e MITOSI_V2 in `[35976, 41976)`)* e `2`, contro `N(s) = N_1 / s`, entro il `20%` *(S3)*.
"""
import argparse
import glob
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_dati as MD  # noqa: E402

SORGENTE = os.path.join(MD.R, "TRONCO", "prima_nascita_35976.npz")
K0, K_FINE = 35976, 35976 + 6000
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0237")
SOGLIE = (0.5, 1.0, 2.0)


def nome_di(s):
    return "M0237" + os.sep + ("soglia_%.1f" % s)


def corsa(s, fino, nome):
    import mitosi_lunga as ML
    import contatore as CN
    from solitone import contatore as CN2
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    d = os.path.join(ML.DIR, nome)
    assert not glob.glob(os.path.join(d, "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % d
    os.makedirs(d, exist_ok=True)
    # ### `mitosi_lunga.riprendi` fa `import contatore` (un modulo di primo livello): QUANTO si mette su ENTRAMBI i nomi dello stesso file
    CN.QUANTO = CN2.QUANTO = float(s) * 2.0 * math.pi
    print("### [M0237-3] la soglia s %.2f: QUANTO = %.15f (2 pi = %.15f), in %s e in %s; la sorgente %s; da %d a %d; le uscite in %s" % (s, CN.QUANTO, 2.0 * math.pi, CN.__file__, CN2.__file__, SORGENTE, K0, fino, d))
    sys.stdout.flush()
    return ML.corsa(nome, K0, fino, True, None, SORGENTE)


def noto():
    """### (K3): soglia 1, da 35976 a 36250, poi gli stati 36000 e 36250 contro MITOSI AL BIT (ogni chiave)."""
    r = corsa(1.0, 36250, "M0237" + os.sep + "soglia_noto")
    out = []
    for k in (36000, 36250):
        a = np.load(os.path.join(BASE, "soglia_noto", "stato_%05d.npz" % k))
        b = np.load(os.path.join(MD.R, "MITOSI", "stato_%05d.npz" % k))
        diverse = [x for x in b.files if x != "meta" and (x not in a.files or not np.array_equal(a[x], b[x]))]
        out.append((k, diverse))
        print("  DEVE: (K3) a soglia 1 lo stato %d = MITOSI AL BIT (ogni chiave tranne meta)  %s  diverse %s" % (k, "PASSA" if not diverse else "### FALLISCE", diverse))
    ok = r == 0 and all(not dv for _k, dv in out)
    print("### (K3) %s" % ("PASSA" if ok else "### FALLISCE"))
    return 0 if ok else 1


def nascite_di(cartelle):
    N = {}
    for c in cartelle:
        ff = sorted(f for f in glob.glob(os.path.join(c, "nascite_*.json")))
        if not ff:
            continue
        for x in json.load(open(ff[-1], encoding="utf-8")):
            N.setdefault((int(x["k"]), int(x["a"])), x)
    return np.array(sorted(k for k, _a in N))


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_dati.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0237-3] LA SOGLIA DI NASCITA (la carta doc/CARTA_mitosi.md): le nascite in [%d, %d) a soglia 0.5, 1, 2 contro N(s) = N_1/s, entro il 20%%" % (K0, K_FINE))
    print("=" * 130)
    K = {1.0: nascite_di([os.path.join(MD.R, "MITOSI"), os.path.join(MD.R, "MITOSI_V2")]),
         0.5: nascite_di([os.path.join(BASE, "soglia_0.5")]), 2.0: nascite_di([os.path.join(BASE, "soglia_2.0")])}
    n1 = int(((K[1.0] >= K0) & (K[1.0] < K_FINE)).sum())
    print("  N_1 (soglia 1, MITOSI + MITOSI_V2 in [%d, %d)): %d" % (K0, K_FINE, n1))
    for k0 in range(K0, K_FINE, 500):
        print("    [%5d, %5d): %s" % (k0, k0 + 500, "  ".join("s %.1f: %3d" % (s, int(((K[s] >= k0) & (K[s] < k0 + 500)).sum())) for s in SOGLIE)))
    for s in (0.5, 2.0):
        ns = int(((K[s] >= K0) & (K[s] < K_FINE)).sum())
        att = n1 / s
        r = ns / att - 1.0 if att else float("nan")
        print("### soglia %.1f: %d nascite contro la formula %.1f: %+.1f%%: %s" % (s, ns, att, 100 * r, "COME LA FORMULA (entro il 20%)" if abs(r) <= 0.20 else "NON come la formula"))
    print("=" * 130)
    return 0


def main(argv):
    os.chdir(os.path.abspath(os.path.join(_QUI, "..", "..")))     # ### dal lanciatore di lapse-u: la cartella di lavoro e' la radice di QUESTO worktree (mitosi)
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "noto", "lettura"))
    ap.add_argument("--s", type=float, choices=(0.5, 2.0))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.s, K_FINE, nome_di(a.s))
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
