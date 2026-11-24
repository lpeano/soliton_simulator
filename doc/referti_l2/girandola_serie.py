# -*- coding: utf-8 -*-
r"""**[M0329-M1] LA SERIE DI TUTTO IL TRONCO: LA ROTAZIONE CUMULATA DEI TRE CENTRI E IL LATO MEDIO** *(la richiesta di Luca del `2026-11-22` `10:32`; la carta `doc/TASK_HISTORY/2026-11-22_girandola_chi.md`, sez. `7.3`; SOLA LETTURA dei film)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/girandola_serie.py --scene t120 t120r28 t000 > doc/referti_l2/girandola_serie.txt

**I dati:** i film `film/girandola_<scena>_<da>_<fino>.npz` in ordine *(ogni blocco comincia dove finisce il precedente)*. **Per stato:** i tre `centri_bari`, `G_k` la loro media, l'angolo di ogni centro attorno a `G_k` srotolato su TUTTA la serie, la rotazione cumulata da `k 0` *(per centro e la media)*, il lato medio. **I tratti:** gli incrementi della rotazione media dello stesso segno, col loro inizio, fine e ampiezza, e lo scarto quadratico dei tre incrementi accanto.
"""
import argparse
import glob
import hashlib
import math
import os
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import girandola_chi_v3 as GC  # noqa: E402

FILM = os.path.join(_QUI, "film")


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def blocchi(q):
    fs = []
    for f in glob.glob(os.path.join(FILM, "girandola_%s_*.npz" % q)):
        m = re.match(r"girandola_%s_(\d{5})_(\d{5})\.npz$" % q, os.path.basename(f))
        if m:
            fs.append((int(m.group(1)), int(m.group(2)), f))
    fs.sort()
    assert fs and fs[0][0] == 0, "%s: manca il blocco da k 0" % q
    for a, b in zip(fs, fs[1:]):
        assert b[0] == a[1], "%s: il blocco %d-%d non comincia dove finisce %d-%d: FERMO" % (q, b[0], b[1], a[0], a[1])
    return fs


def serie(q):
    ks, cen = [], []
    fs = blocchi(q)
    print("=" * 130)
    print("LA SERIE DI %s: %d blocchi, %s" % (q, len(fs), "; ".join("%d-%d (sha1 %s)" % (a, b, sha1(f)[:8]) for a, b, f in fs)))
    print("=" * 130)
    for _a, _b, f in fs:
        with np.load(f) as F:
            for k in [int(x) for x in F["k"]]:
                assert not ks or k > ks[-1], "%s: k %d fuori ordine: FERMO" % (q, k)
                ks.append(k)
                cen.append(F["centri_bari_%06d" % k].astype(float))
    ang = [GC.angoli(c, c.mean(axis=0)) for c in cen]
    rot = []
    for j in range(3):
        s_ = GC.srotola([a[j] for a in ang])
        rot.append([v - s_[0] for v in s_])
    rot = np.array(rot)                                    # ### (3, stati)
    media = rot.mean(axis=0)
    lato = [float(np.mean([np.hypot(*(c[a] - c[b])) for a, b in ((0, 1), (1, 2), (2, 0))])) for c in cen]
    print("  k       la rotazione cumulata (gradi): i tre centri | la media   l'incremento (la media; lo scarto dei tre)   il lato medio")
    inc, sc = [0.0], [0.0]
    for i, k in enumerate(ks):
        if i:
            d3 = rot[:, i] - rot[:, i - 1]
            inc.append(float(d3.mean()))
            sc.append(float(d3.std()))
        print("  %6d  %+8.3f %+8.3f %+8.3f | %+8.3f   %+8.4f (%.4f)   %8.4f" % (k, rot[0, i], rot[1, i], rot[2, i], media[i], inc[i], sc[i], lato[i]))
    print("  I TRATTI (gli incrementi della rotazione media dello stesso segno):")
    tratti = []
    i = 1
    while i < len(ks):
        sg = np.sign(inc[i])
        j = i
        while j + 1 < len(ks) and np.sign(inc[j + 1]) == sg:
            j += 1
        amp = float(media[j] - media[i - 1])
        tratti.append((ks[i - 1], ks[j], amp, float(np.mean(sc[i:j + 1]))))
        i = j + 1
    for a, b, amp, s in tratti:
        print("    k %6d -> %6d  %+8.4f gradi (lo scarto medio dei tre incrementi %.4f; %d stati)" % (a, b, amp, s, (b - a) // 250))
    grandi = [t for t in tratti if abs(t[2]) > t[3]]
    cambi = sum(1 for x, y in zip(grandi, grandi[1:]) if np.sign(x[2]) != np.sign(y[2]))
    print("  la lettura (sez. 7.3): %d tratti, %d con l'ampiezza sopra lo scarto dei tre, %d cambi di segno fra questi: %s" % (
        len(tratti), len(grandi), cambi, "DONDOLA" if cambi > 1 else "non dondola (la descrizione coi numeri sopra)"))
    print("  in sintesi: la rotazione media a k %d %+.3f gradi (il massimo %+.3f a k %d, il minimo %+.3f a k %d); il lato medio da %.4f a %.4f (il massimo %.4f a k %d)" % (
        ks[-1], media[-1], media.max(), ks[int(np.argmax(media))], media.min(), ks[int(np.argmin(media))], lato[0], lato[-1], max(lato), ks[int(np.argmax(lato))]))
    return ks, media, lato


def main(argv):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "girandola_chi_v3.py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", nargs="+", choices=("t120", "t120r28", "t000"), required=True)
    x = ap.parse_args(argv)
    for q in x.scene:
        serie(q)
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
