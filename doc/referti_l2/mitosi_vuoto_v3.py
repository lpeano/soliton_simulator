# -*- coding: utf-8 -*-
r"""**[M0024] K4': IL VUOTO PURO, IL CRITERIO SU H IN ASSOLUTO** *(DECISIONE DI LUCA, 2026-11-27 `00:24`; la carta `doc/CARTA_mitosi.md`, «K4' E LA SOGLIA CHIUSA», scritta PRIMA; `mitosi_vuoto_v2.py` e' usato e non si riscrive: la v3 legge le uscite della sua corsa K4)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v3.py noto > doc/referti_l2/mitosi_vuoto_v3_noto.txt       (K4')

**K4'** sulla corsa K4 di `mitosi_vuoto_v2.py noto` *(`M0237/vuoto_v2_noto`, il modo `c2ext`, le nascite spente, da `35976` a `36250`; il codice della via non e' cambiato, quindi rifarla darebbe gli stessi byte)*. **`H_rif`** = `H` dello stato di partenza *(`vuoto_35976.npz`: `phi_h = a phi_v`, `psi = 0`, cioe' il vuoto fresco sullo stesso reticolo)*, che e' il primo valore della serie `E` *(k `36000`: la serie non misura `35976`)*. **Il ramo:** se `|H_rif| < 1e-9`, il vuoto ha `H` «circa 0» e vale `|Delta H| < 1e-12`; altrimenti vale `|Delta H| < 1e-9 |H_rif|`. **La norma:** `|Delta somma |phi_h|^2| / somma < 1e-9`. **`Delta`** fra `36000` e `36250`, come in K4. **Si stampano anche tutti i valori della serie `E`.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_vuoto_v2 as MV2  # noqa: E402

D_NOTO = os.path.join(MV2.BASE, "vuoto_v2_noto")


def noto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_vuoto_v2.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0024] K4': il vuoto puro senza nascite, il criterio su H in assoluto; dalla corsa K4 in %s" % D_NOTO)
    print("=" * 130)
    for k in (36000, 36250):
        f = os.path.join(D_NOTO, "stato_%d.npz" % k)
        print("  lo stato %s, sha1 registrato %s" % (f, open(f + ".sha1", encoding="utf-8").read().split()[0][:8]))
    a, b = np.load(os.path.join(D_NOTO, "stato_36000.npz")), np.load(os.path.join(D_NOTO, "stato_36250.npz"))
    na, nb = float(np.sum(np.abs(a["phi_h"]) ** 2)), float(np.sum(np.abs(b["phi_h"]) ** 2))
    with np.load(os.path.join(D_NOTO, "serie_36250.npz")) as z:
        k_, E = z["k"], z["E"]
    print("  la serie E: %s" % "; ".join("k %d %+.6e" % (int(x), float(e)) for x, e in zip(k_, E)))
    h_rif = float(E[k_ == 36000][0])
    ea, eb = h_rif, float(E[k_ == 36250][0])
    dh = abs(eb - ea)
    if abs(h_rif) < 1e-9:
        lim, ramo = 1e-12, "|H_rif| %.3e < 1e-9: H circa 0, |Delta H| < 1e-12" % abs(h_rif)
    else:
        lim, ramo = 1e-9 * abs(h_rif), "|Delta H| < 1e-9 |H_rif| = %.3e" % (1e-9 * abs(h_rif))
    rn = abs(nb / na - 1.0)
    okn, okh = rn < 1e-9, dh < lim
    print("  H_rif %+.12e; il ramo: %s" % (h_rif, ramo))
    print("  DEVE: (K4') la norma 36000 -> 36250: %.12e -> %.12e (%.2e relativo, entro 1e-9)   %s" % (na, nb, rn, "PASSA" if okn else "### FALLISCE"))
    print("  DEVE: (K4') H 36000 -> 36250: %+.12e -> %+.12e, |Delta H| %.3e contro %.1e   %s" % (ea, eb, dh, lim, "PASSA" if okh else "### FALLISCE"))
    ok = okn and okh
    print("### (K4') %s" % ("PASSA" if ok else "FALLISCE"))
    print("=" * 130)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(noto())
