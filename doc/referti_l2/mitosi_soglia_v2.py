# -*- coding: utf-8 -*-
r"""**[M0237-3] LA SOGLIA DI NASCITA, LA V2: SULLA VIA VERA DI MITOSI** *([M2034], DECISIONE DI LUCA 2026-11-26 20:34, D1; la carta `doc/CARTA_mitosi.md`, «D1 e D2»; `mitosi_soglia.py` e' usato e non si riscrive: era costruito su `mitosi_lunga.corsa`, che NON e' la via di MITOSI)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia_v2.py noto > doc/referti_l2/mitosi_soglia_v2_noto.txt     (K3, K3b)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia_v2.py corsa --s 0.5         (0.5 e 2; dalla coda, dopo d1', d2', d3')
    E:\python\py3132\python.exe doc/referti_l2/mitosi_soglia_v2.py lettura > doc/referti_l2/mitosi_soglia_v2.txt

**La via vera, in due fasi** *(D1)*: **fase 1** `mitosi_rami.ciclo(..., "mitosi", prima_nascita_35976, 36250)` *(la v1, «lo scatto del tronco» compreso)*; **fase 2** `mitosi_rami_v2.ciclo(..., "mitosi", <lo stato 36250 della fase 1>, fino)` *(la v2, la regola `mitosi_regola_v2`)*. **Una sola differenza, in memoria: `contatore.QUANTO = s 2 pi`**, su entrambi i nomi del modulo. Le uscite in `E:/soliton_simulator/controllo/M0237/soglia_v2_<s>/fase1|fase2/`. **(K3)** la fase 1 a soglia `2 pi` = MITOSI a `36000` e `36250` al bit; **(K3b)** la fase 2 a soglia `2 pi` da `MITOSI/stato_36250` a `36500` = MITOSI_V2 a `36500` al bit.
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
K0, K1, K_FINE = 35976, 36250, 35976 + 6000
BASE = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M0237")
SOGLIE = (0.5, 1.0, 2.0)


def soglia(s):
    import contatore as CN
    from solitone import contatore as CN2
    CN.QUANTO = CN2.QUANTO = float(s) * 2.0 * math.pi
    return CN.QUANTO


def fase1(s, d):
    import mitosi_rami as MR1
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami.py"))
    os.makedirs(d, exist_ok=True)
    q = soglia(s)
    print("### [M0237-3 v2] fase 1 (mitosi_rami, la v1): s %.2f, QUANTO %.15f; da %s a %d; in %s" % (s, q, SORGENTE, K1, d))
    sys.stdout.flush()
    return MR1.ciclo("soglia_%.1f_fase1" % s, "mitosi", SORGENTE, K1, None, d_out=d)


def fase2(s, f, fino, d):
    import mitosi_rami_v2 as MR2
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_rami_v2.py"))
    os.makedirs(d, exist_ok=True)
    q = soglia(s)
    print("### [M0237-3 v2] fase 2 (mitosi_rami_v2): s %.2f, QUANTO %.15f; da %s a %d; in %s" % (s, q, f, fino, d))
    sys.stdout.flush()
    return MR2.ciclo("soglia_%.1f_fase2" % s, "mitosi", f, fino, None, d_out=d)


def al_bit(a_f, b_f):
    a, b = np.load(a_f), np.load(b_f)
    return [x for x in b.files if x != "meta" and (x not in a.files or not np.array_equal(a[x], b[x]))]


def noto():
    import _presidio
    _presidio.avvia(__file__)
    d = os.path.join(BASE, "soglia_v2_noto")
    assert not glob.glob(os.path.join(d, "*", "stato_*.npz")), "%s ha gia' degli stati" % d
    cod, k, _f = fase1(1.0, os.path.join(d, "fase1"))
    ok = True
    for kk in (36000, 36250):
        dv = al_bit(os.path.join(d, "fase1", "stato_%05d.npz" % kk), os.path.join(MD.R, "MITOSI", "stato_%05d.npz" % kk))
        ok = ok and not dv
        print("  DEVE: (K3) la fase 1 a soglia 1, lo stato %d = MITOSI AL BIT (ogni chiave tranne meta)   %s  diverse %s" % (kk, "PASSA" if not dv else "### FALLISCE", dv))
    cod2, k2, _f2 = fase2(1.0, os.path.join(MD.R, "MITOSI", "stato_36250.npz"), 36500, os.path.join(d, "fase2"))
    dv = al_bit(os.path.join(d, "fase2", "stato_36500.npz"), os.path.join(MD.R, "MITOSI_V2", "stato_36500.npz"))
    ok = ok and not dv and cod == 0 and cod2 == 0
    print("  DEVE: (K3b) la fase 2 a soglia 1 da MITOSI/stato_36250, lo stato 36500 = MITOSI_V2 AL BIT   %s  diverse %s" % ("PASSA" if not dv else "### FALLISCE", dv))
    print("### (K3, K3b) %s (i codici %s, %s)" % ("PASSANO" if ok else "### FALLISCONO", cod, cod2))
    return 0 if ok else 1


def corsa(s):
    import _presidio
    _presidio.avvia(__file__)
    d = os.path.join(BASE, "soglia_v2_%.1f" % s)
    assert not glob.glob(os.path.join(d, "*", "stato_*.npz")), "%s ha gia' degli stati: non si riscrive" % d
    cod, k, _f = fase1(s, os.path.join(d, "fase1"))
    f36 = os.path.join(d, "fase1", "stato_%05d.npz" % K1)
    if cod != 0 or not os.path.exists(f36):
        print("### FERMO: la fase 1 a s %.2f si e' fermata a k %s (codice %s), senza lo stato %d" % (s, k, cod, K1))
        return 2
    cod2, k2, _f2 = fase2(s, f36, K_FINE, os.path.join(d, "fase2"))
    print("### la fase 2 a s %.2f: codice %s, k %s" % (s, cod2, k2))
    return 0 if cod2 == 0 else 2


def nascite_di(cartelle):
    N = {}
    for c in cartelle:
        ff = sorted(glob.glob(os.path.join(c, "nascite_*.json")))
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
    print("[M0237-3 v2] LA SOGLIA DI NASCITA SULLA VIA VERA (la carta doc/CARTA_mitosi.md): le nascite in [%d, %d) a soglia 0.5, 1, 2 contro N(s) = N_1/s, entro il 20%%" % (K0, K_FINE))
    print("=" * 130)
    K = {1.0: nascite_di([os.path.join(MD.R, "MITOSI"), os.path.join(MD.R, "MITOSI_V2")])}
    for s in (0.5, 2.0):
        d = os.path.join(BASE, "soglia_v2_%.1f" % s)
        K[s] = nascite_di([os.path.join(d, "fase1"), os.path.join(d, "fase2")])
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
    os.chdir(os.path.abspath(os.path.join(_QUI, "..", "..")))     # ### dal lanciatore di lapse-u: la radice del worktree mitosi
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    ap.add_argument("--s", type=float, choices=(0.5, 2.0))
    a = ap.parse_args(argv)
    if a.cosa == "corsa":
        return corsa(a.s)
    return {"noto": noto, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
