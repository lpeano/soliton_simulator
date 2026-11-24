# -*- coding: utf-8 -*-
r"""**[M0329-F1] IL FILM LEGGERO DI TUTTO IL TRONCO** *(la richiesta di Luca del `2026-11-22` dopo le `12:12`; la carta `doc/TASK_HISTORY/2026-11-22_girandola_chi.md`, sez. `8`; SOLA LETTURA dei film dei blocchi)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/film/girandola_film_leggero.py --scene t120 t120r28 t000 > doc/referti_l2/film/girandola_film_leggero.txt

**Le fonti:** i blocchi in `doc/referti_l2/film/` e in `E:\soliton_simulator\controllo\girandola_blocchi\`, contigui. **Gli stati** con `k` multiplo di `1000`: `rho`, `Jx`, `Jy`, `chi` in `float16`, i centri in `float32`. **Il file** `doc/referti_l2/film/girandola_<scena>_leggero.npz`, sotto i `50 MB`. **Per il video, non per le misure** *(il `float16`)*.
"""
import argparse
import glob
import hashlib
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(os.path.dirname(_QUI)))
for _p in (os.path.dirname(_QUI), os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
FUORI = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "girandola_blocchi")
OGNI = 1000                     # ### Luca: uno stato ogni 1000 tick
NOTA = "float16: per il video, non per le misure (rho sotto ~6e-05 perde precisione o va a zero); le misure leggono i film interi dei blocchi"


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def blocchi(q):
    fs = {}
    for d in (_QUI, FUORI):
        for f in glob.glob(os.path.join(d, "girandola_%s_*.npz" % q)):
            m = re.match(r"girandola_%s_(\d{5})_(\d{5})\.npz$" % q, os.path.basename(f))
            if m:
                fs.setdefault((int(m.group(1)), int(m.group(2))), f)
    out = sorted((a, b, f) for (a, b), f in fs.items())
    assert out and out[0][0] == 0, "%s: manca il blocco da k 0" % q
    for x, y in zip(out, out[1:]):
        assert y[0] == x[1], "%s: il blocco %d-%d non comincia dove finisce %d-%d: FERMO" % (q, y[0], y[1], x[0], x[1])
    return out


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", nargs="+", choices=("t120", "t120r28", "t000"), required=True)
    x = ap.parse_args(argv)
    print("=" * 130)
    print("[M0329-F1] IL FILM LEGGERO DI TUTTO IL TRONCO: uno stato ogni %d tick; %s" % (OGNI, NOTA))
    print("=" * 130)
    for q in x.scene:
        bl = blocchi(q)
        out, ks = {}, []
        for a, b, f in bl:
            print("  %s %05d-%05d  %s (sha1 %s)" % (q, a, b, f, sha1(f)[:8]))
            with np.load(f) as F:
                if not out:
                    for c in ("L", "x", "y", "vertici", "G0"):
                        if c in F.files:
                            out[c] = F[c]
                for k in [int(v) for v in F["k"]]:
                    if k % OGNI or k in ks:
                        continue
                    s = "_%06d" % k
                    for c in ("rho", "Jx", "Jy", "chi"):
                        out[c + s] = F[c + s].astype(np.float16)
                    for c in ("centri_bari", "centri_max"):
                        out[c + s] = F[c + s].astype(np.float32)
                    ks.append(k)
        assert ks == sorted(ks), "i k fuori ordine: FERMO"
        out.update(k=np.array(ks, dtype=np.int32), quale=np.array(q), nota=np.array(NOTA))
        ff = os.path.join(_QUI, "girandola_%s_leggero.npz" % q)
        np.savez_compressed(ff, **out)
        mb = os.path.getsize(ff) / 1e6
        ul = out["rho_%06d" % ks[-1]]
        print("### %s: %d stati (k %d ... %d), %.2f MB, sha1 %s; rho float16 a k %d: il massimo %.1f, i nodi a zero %d su %d" % (
            q, len(ks), ks[0], ks[-1], mb, sha1(ff)[:8], ks[-1], float(ul.max()), int(np.sum(ul == 0)), ul.size))
        assert mb <= 50.0, "sopra i 50 MB: FERMO"
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
