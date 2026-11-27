# -*- coding: utf-8 -*-
r"""**[M0106] K4'': IL VUOTO PURO, LA NORMA COME CRITERIO; E LA LETTURA DELLA CORSA DEL VUOTO PURO** *(DECISIONE DI LUCA, 2026-11-27 `01:06`; la carta `doc/CARTA_mitosi.md`, «K4''», scritta PRIMA; `mitosi_vuoto_v2.py` e `mitosi_vuoto_v3.py` sono usati e non si riscrivono)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v4.py noto > doc/referti_l2/mitosi_vuoto_v4_noto.txt       (K4'')
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v2.py corsa       (la corsa: le nascite accese, 6000 tick; dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/mitosi_vuoto_v4.py lettura > doc/referti_l2/mitosi_vuoto_v3.txt

**K4''** sulle uscite della corsa K4 *(`M0237/vuoto_v2_noto`, come la v3)*: **il criterio e' la norma** *(`|Delta somma |phi_h|^2| / somma < 1e-9` fra `36000` e `36250`)*; `|Delta H|` e `H_rif` si stampano e non bloccano. **La lettura** *(dopo la corsa in `M0237/vuoto_v2`)*: le nascite *(si', no; a quali `k`)* da `mitosi_vuoto_v2.lettura`; poi per ogni stato salvato la norma `somma |phi_h|^2`, e la serie `H(k)` dall'ultima `serie_*.npz`.
"""
import glob
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_vuoto_v3 as MV3  # noqa: E402

MV2 = MV3.MV2
D_NOTO = MV3.D_NOTO
D_CORSA = os.path.join(MV2.BASE, "vuoto_v2")


def noto():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_vuoto_v2.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_vuoto_v3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0106] K4'': il vuoto puro senza nascite, la NORMA come criterio; dalla corsa K4 in %s" % D_NOTO)
    print("=" * 130)
    a, b = np.load(os.path.join(D_NOTO, "stato_36000.npz")), np.load(os.path.join(D_NOTO, "stato_36250.npz"))
    na, nb = float(np.sum(np.abs(a["phi_h"]) ** 2)), float(np.sum(np.abs(b["phi_h"]) ** 2))
    with np.load(os.path.join(D_NOTO, "serie_36250.npz")) as z:
        k_, E = z["k"], z["E"]
    h_rif, eb = float(E[k_ == 36000][0]), float(E[k_ == 36250][0])
    rn = abs(nb / na - 1.0)
    ok = rn < 1e-9
    print("  (stampa, non blocca) H_rif %+.12e; H(36250) %+.12e; |Delta H| %.3e; la serie E: %s" % (h_rif, eb, abs(eb - h_rif), "; ".join("k %d %+.3e" % (int(x), float(e)) for x, e in zip(k_, E))))
    print("  DEVE: (K4'') la norma 36000 -> 36250: %.12e -> %.12e (%.2e relativo, entro 1e-9)   %s" % (na, nb, rn, "PASSA" if ok else "### FALLISCE"))
    print("### (K4'') %s" % ("PASSA" if ok else "FALLISCE"))
    print("=" * 130)
    return 0 if ok else 1


def lettura():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mitosi_vuoto_v2.py"))
    cod = MV2.lettura()
    _presidio.avvia(__file__)
    print("-" * 130)
    print("[M0106] LA NORMA E H(k) DELLA CORSA DEL VUOTO PURO (%s)" % D_CORSA)
    print("-" * 130)
    for f in sorted(glob.glob(os.path.join(D_CORSA, "stato_*.npz"))):
        with np.load(f) as z:
            print("  %s: somma |phi_h|^2 %.12e" % (os.path.basename(f), float(np.sum(np.abs(z["phi_h"]) ** 2))))
    ss = sorted(glob.glob(os.path.join(D_CORSA, "serie_*.npz")))
    if ss:
        with np.load(ss[-1]) as z:
            k_, E = z["k"], z["E"]
        m = ~np.isnan(E)
        print("  H(k) da %s: %d valori; %s" % (os.path.basename(ss[-1]), int(m.sum()), "; ".join("k %d %+.3e" % (int(x), float(e)) for x, e in zip(k_[m], E[m]))))
        print("  ### max |H| %.3e" % float(np.max(np.abs(E[m]))))
    else:
        print("  ### nessuna serie")
    print("=" * 130)
    return cod


def main(argv):
    os.chdir(os.path.abspath(os.path.join(_QUI, "..", "..")))
    cosa = argv[0] if argv else ""
    assert cosa in ("noto", "lettura"), "uso: noto | lettura"
    return {"noto": noto, "lettura": lettura}[cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
