# -*- coding: utf-8 -*-
r"""**[M0237-0] LE TRE PROVE SULLA MITOSI: I DATI PRIMA DEI NUMERI** *(DECISIONE DI LUCA, 2026-11-25 02:37, dalla posta; la carta `doc/CARTA_mitosi.md`, sez. «Le tre prove»; solo letture, a costo zero)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_dati.py > doc/referti_l2/mitosi_dati.txt

**Le corse** *(in `E:/soliton_simulator/controllo/mitosi_rami/`)*: **TRONCO** *(senza nascite, fino alla prima, `prima_nascita_35976.npz`)*, **MITOSI** *(da `35976` a `36250`)*, **MITOSI_V2** *(da `36250` a `45976`)*. **Le nascite:** i `nascite_*.json` dell'ultimo stato di MITOSI e di MITOSI_V2, unite per `k`. **La fiammata** *(Luca)*: il primo `k` di nascita in cui l'intervallo alla nascita dopo scende sotto `1/10` del PRIMO intervallo. **La deriva di fondo:** `E` *(la serie `E` di `controllo_senza_bordo.Misure`, ogni `50` tick)* sul TRONCO, sullo stesso numero di tick della fiammata, prima della prima nascita.
"""
import glob
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))

R = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "mitosi_rami")
CORSE = ("TRONCO", "MITOSI", "MITOSI_V2")


def ultimo(d, pref):
    ff = sorted(glob.glob(os.path.join(R, d, pref + "_*.*")))
    ff = [f for f in ff if not f.endswith(".sha1")]
    return ff[-1] if ff else None


def serie(d):
    f = ultimo(d, "serie")
    if f is None:
        return None, None
    with np.load(f) as z:
        return f, {x: z[x].copy() for x in z.files}


def main():
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0237-0] I DATI DELLA CORSA MITOSI (la carta doc/CARTA_mitosi.md, Le tre prove): le nascite, la fiammata, gli stati, la deriva di fondo")
    print("=" * 130)
    for c in CORSE:
        st = sorted(glob.glob(os.path.join(R, c, "stato_*.npz")))
        pn = sorted(glob.glob(os.path.join(R, c, "prima_nascita_*.npz")))
        print("  %-10s: %d stati (%s .. %s); prima_nascita: %s" % (c, len(st), os.path.basename(st[0]) if st else "-", os.path.basename(st[-1]) if st else "-", [os.path.basename(x) for x in pn]))
    N = {}
    for c in ("MITOSI", "MITOSI_V2"):
        f = ultimo(c, "nascite")
        b = json.load(open(f, encoding="utf-8"))
        print("  le nascite di %s: %s, %d voci" % (c, os.path.basename(f), len(b)))
        for x in b:
            N.setdefault((int(x["k"]), int(x["a"])), x)
    nasc = [N[q] for q in sorted(N)]
    ks = np.array([int(x["k"]) for x in nasc])
    print("  LE NASCITE (unite): %d; i k: dal %d al %d; le prime 12: %s" % (len(ks), ks[0], ks[-1], " ".join(str(k) for k in ks[:12])))
    dk = np.diff(ks)
    d1 = int(dk[0])
    i_f = next((i for i in range(len(dk)) if dk[i] < d1 / 10.0), None)
    kf = int(ks[i_f]) if i_f is not None else None
    print("  il primo intervallo %d tick; la fiammata (il primo intervallo sotto %.1f): alla nascita %s, k %s" % (d1, d1 / 10.0, None if i_f is None else i_f + 1, kf))
    for k0 in range(int(ks[0] // 500 * 500), int(ks[-1]) + 1, 500):
        m = (ks >= k0) & (ks < k0 + 500)
        print("    [%5d, %5d): %3d nascite" % (k0, k0 + 500, int(m.sum())))
    fS = {}
    for c in CORSE:
        f, S = serie(c)
        fS[c] = (f, S)
        if S is not None:
            print("  la serie di %s: %s, k da %d a %d (%d punti); E da %+.10e a %+.10e" % (c, os.path.basename(f), int(S["k"][0]), int(S["k"][-1]), len(S["k"]), float(S["E"][0]), float(S["E"][-1])))
    k_fine = int(fS["MITOSI_V2"][1]["k"][-1])
    if kf is not None:
        D = k_fine - kf
        Tk, TE = fS["TRONCO"][1]["k"], fS["TRONCO"][1]["E"]
        k1 = int(ks[0])
        ia = int(np.argmin(np.abs(Tk - (k1 - D))))
        ib = int(np.argmin(np.abs(Tk - k1)))
        der = abs(float(TE[ib] - TE[ia])) / abs(float(TE[ib]))
        print("### la fiammata dura %d tick (da k %d a k %d). LA DERIVA DI FONDO sul TRONCO sugli stessi %d tick prima della prima nascita: E(%d) %+.10e, E(%d) %+.10e: |dE|/|E| = %.3e" % (
            D, kf, k_fine, D, int(Tk[ia]), float(TE[ia]), int(Tk[ib]), float(TE[ib]), der))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
