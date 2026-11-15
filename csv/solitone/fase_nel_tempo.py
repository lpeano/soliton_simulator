# -*- coding: utf-8 -*-
r"""**LA FASE RELATIVA NEL TEMPO** *(Luca `2026-11-14` `23:32`, «ma sono tutti in fase?»; solo lettura; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21`, `21.6`)*.

    python csv/solitone/fase_nel_tempo.py > doc/referti_l2/mattone/fase_nel_tempo.txt

### **La funzione `fase` di `legame.py` COPIATA e CORRETTA:** **in `legame.py` i francobolli** *(la scena di TBS, `L 81`)* **si facevano DENTRO la scena di S162 aperta, e lo stato del modulo** *(`V.L`)* **si rompeva**
*(la corsa delle `01:07`: `ValueError` in `mattone.scena.metti`)*; **qui si fanno PRIMA.** **`legame.py` e' in uso da `scena-vuota`: non si tocca** *(dichiarato)*. **La misura: negli stati salvati di (T-fase) e
(T-sfasati) a `500`, ..., `2000`, `arg <psi_i, psi_j>` col pezzo di `i`** *(i nodi entro `14` dal suo centro)* **SPOSTATO sul vertice di `j`** *(la differenza fra i vertici e' un multiplo di `3`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

R_PEZZO_FASE = 14.0


def fase():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "mattone_triangolo.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("(fase_nel_tempo.py: la funzione fase di legame.py, corretta)")
    print("LA FASE RELATIVA NEL TEMPO (Luca 23:32, «ma sono tutti in fase?»; solo lettura): arg <psi_i, psi_j> col pezzo di i (entro %g nodi dal suo centro) SPOSTATO sul vertice di j" % R_PEZZO_FASE)
    print("=" * 130)
    FR = {v: [MTR.francobollo(k) for k in MTR.VARIANTI[v]] for v in ("fase", "sfasati")}     # ### i francobolli PRIMA della scena di S162 (la correzione)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n, righe = Z["L"], Z["n"], Z["righe"]
        m1, m2 = Z["m1"], Z["m2"]
        for v in ("fase", "sfasati", "video"):
            fs = os.path.join(MT.DIR_REF, "triangolo_%s_serie.npz" % v)
            if not os.path.exists(fs):
                print("### (T-%s): la serie non c'e'" % v)
                continue
            sv = np.load(fs)
            stati = [(k, os.path.join(MT.DIR_E, "triangolo_%s_%05d.npz" % (v, k))) for k in (500, 1000, 1500, 2000)]
            if v not in MTR.VARIANTI:
                print("### (T-%s): i vertici non si rifanno da qui (la variante e' in memoria in triangolo_video.py): saltato" % v)
                continue
            frs = FR[v]
            vertici = MTR.posti(Z["bordo"]["c0"], frs, L)
            print("### (T-%s): i vertici %s" % (v, vertici))
            for k, f in stati:
                if not os.path.exists(f):
                    print("    k %4d: manca %s" % (k, f))
                    continue
                with np.load(f) as d:
                    psi = d["psi_h"]
                j = int(np.nonzero(sv["k"] == k)[0][0])
                cen = [(float(sv["c1_" + q][j]), float(sv["c2_" + q][j])) for q in "ABC"]
                riga = []
                for a, b in ((0, 1), (1, 2), (0, 2)):
                    from solitone import toro as TO
                    dd = np.hypot(*TO.scarti(m1, m2, cen[b][0], cen[b][1], L).T[:2])
                    vb = np.nonzero(dd <= R_PEZZO_FASE)[0]
                    s1, s2 = vertici[b][0] - vertici[a][0], vertici[b][1] - vertici[a][1]
                    va = ((m1[vb] - s1) % L) * L + (m2[vb] - s2) % L
                    z = complex(np.sum(np.conj(psi[righe[va]]) * psi[righe[vb]]))
                    riga.append("%s-%s %+7.1f" % ("ABC"[a], "ABC"[b], math.degrees(math.atan2(z.imag, z.real))))
                print("    k %4d: %s gradi" % (k, "  ".join(riga)))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(fase())
