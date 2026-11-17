# -*- coding: utf-8 -*-
r"""**A4: I SEI SETTORI E LO SPECCHIO** *(Luca `2026-11-17` `16:38`; la carta `doc/TASK_HISTORY/2026-11-17_mitosi_verso_il_test.md`, sez. `1`)*.

    E:\python\py3132\python.exe doc/referti_l2/settori_specchio.py > doc/referti_l2/settori_specchio.txt

**I settori:** `6` da `60` gradi attorno a un CENTRO, **i bordi sulle direzioni del reticolo** *(`0, 60, 120, ...` gradi: `A1` e le sue rotazioni)*; **un arco appartiene al settore del suo punto medio**; **un arco col punto medio SUL bordo** *(entro `1e-9` gradi)* **o nel centro: PARI MERITO, nessuna nascita.**
**La prova** *(la mappa dei nodi e degli archi di `specchio_carta.py`)*: **lo specchio a `30` gradi per il centro** *(`theta -> 60 - theta`: il settore `s` va in `-s mod 6`)* **e l'inversione** *(`theta -> theta + 180`: `s -> s + 3 mod 6`)* **mandano OGNI arco nel settore immagine, e i pari merito in pari merito.** **Il caso che DEVE fallire:** il centro NON su un nodo *(il baricentro del mattone, non arrotondato)*: lo specchio del reticolo non passa per lui, e l'equivarianza si rompe.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
_SOL = os.path.join(_RADICE, "csv", "solitone")
_CSV = os.path.join(_RADICE, "csv")
for _p in (_QUI, os.path.join(_QUI, "mattone"), _SOL, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)

TOLL = 1e-9


def settori(m1, m2, ii, jj, L, centro):
    """### il settore di ogni arco (`-1` = pari merito: sul bordo o nel centro)."""
    from solitone import toro as TO
    Di = TO.scarti(m1[ii], m2[ii], centro[0], centro[1], L)[:, :2]
    de = TO.scarti(m1[jj], m2[jj], m1[ii], m2[ii], L)[:, :2]
    mid = Di + 0.5 * de
    r = np.hypot(mid[:, 0], mid[:, 1])
    th = (np.degrees(np.arctan2(mid[:, 1], mid[:, 0])) + 360.0) % 360.0
    s = np.floor(th / 60.0).astype(int) % 6
    resto = th - 60.0 * np.floor(th / 60.0)
    pari = (r < 1e-9) | (np.minimum(resto, 60.0 - resto) < TOLL)
    return np.where(pari, -1, s)


def main():
    import _presidio
    import mattone as MT
    import specchio_carta as SPC
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "mattone", "specchio_carta.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("A4: I SEI SETTORI E LO SPECCHIO (Luca 2026-11-17 16:38)")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        nodo = np.asarray(Z["mot"].inc.nodo)
    with np.load(os.path.join(MT.DIR_E, "L162_MGU_03000.npz")) as d:
        psi = d["psi_h"].copy()
    ii, jj = nodo[0::2], nodo[1::2]
    v = np.arange(n)
    m1, m2 = (v // L).astype(float), (v % L).astype(float)
    rho = np.zeros(n)
    np.add.at(rho, nodo, np.abs(psi[:, 0]) ** 2 + np.abs(psi[:, 1]) ** 2)
    cb = TO.centro(rho, m1, m2, L)[:2]
    p0 = (int(round(cb[0])) % L, int(round(cb[1])) % L)
    A1, A2 = TO.vettori()
    d30 = 2 * A1 + A2
    ang = math.atan2(d30[1], d30[0])
    esiti = []
    for nome_c, centro in (("il nodo p0 = %s (il baricentro arrotondato)" % (p0,), (float(p0[0]), float(p0[1]))), ("il baricentro NON arrotondato (%.3f, %.3f): DEVE FALLIRE" % cb, (float(cb[0]), float(cb[1])))):
        s = settori(m1, m2, ii, jj, L, centro)
        print("-" * 130)
        print("### il centro: %s; gli archi per settore %s; i pari merito %d" % (nome_c, [int(np.sum(s == q)) for q in range(6)], int(np.sum(s < 0))))
        risultati = []
        for nome_m, M, f in (("lo specchio a 30 gradi", None, lambda q: (-q) % 6), ("l'inversione", -np.eye(2), lambda q: (q + 3) % 6)):
            if M is None:
                sig, scarto, _M = SPC.mappa_nodi(L, m1, m2, p0, ang)
            else:
                P = np.outer(m1 - p0[0], A1) + np.outer(m2 - p0[1], A2)
                q = (P @ M.T) @ np.linalg.inv(np.column_stack([A1, A2])).T
                qi = np.rint(q)
                scarto = float(np.max(np.abs(q - qi)))
                sig = ((qi[:, 0].astype(int) + p0[0]) % L) * L + (qi[:, 1].astype(int) + p0[1]) % L
            ap, _rov = SPC.mappa_archi(ii, jj, sig)
            atteso = np.where(s < 0, -1, np.vectorize(f)(np.maximum(s, 0)))
            sbagliati = int(np.sum(s[ap] != atteso))
            print("    %s (la mappa per il nodo p0, lo scarto %.1e): gli archi nel settore sbagliato o col pari merito non conservato: %d su %d" % (nome_m, scarto, sbagliati, len(ap)))
            risultati.append(sbagliati)
        if centro == (float(p0[0]), float(p0[1])):
            esiti.append(("col centro sul nodo dello specchio: settori e pari merito equivarianti (0 sbagliati) per lo specchio e l'inversione", all(x == 0 for x in risultati)))
        else:
            esiti.append(("DEVE FALLIRE: col centro fuori dal nodo dello specchio l'equivarianza si rompe", any(x > 0 for x in risultati)))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
