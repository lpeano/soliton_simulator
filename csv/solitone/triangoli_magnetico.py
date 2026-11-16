# -*- coding: utf-8 -*-
r"""**IL CAMPO MAGNETICO NEI TRIANGOLI** *(Luca `2026-11-15` `13:56`; SOLO LETTURA)*.

    python csv/solitone/triangoli_magnetico.py > doc/referti_l2/mattone/triangoli_magnetico.txt

**`B` = il rotore di `A` del prototipo U** *(`_u1_prototipo.Campo.B`: per PLACCHETTA, la somma con segno di `A` sui tre archi; le placchette «su» `p = v` e «giu» `p = n + v` percorse tutte e due in senso ANTIORARIO:
`B > 0` = la circolazione di `A` antioraria; dal codice)*. **Nessuna definizione nuova.** **«Sui nodi»** *(mia lettura, dichiarata)*: **`B` per placchetta, al suo baricentro** *(«su»: `(m1 + 2/3, m2 + 1/3)`, «giu»: `(m1 + 1/3, m2 + 2/3)` negli indici)*.
**Dagli stati salvati** *(`A` = `campo_A`)*: **il triangolo a `120` gradi** *(`triangolo_t120_00500` ... `02000`)* **e (T-fase) col mattone di `L 162`** *(il video, `triangolo_video_00500` ... `02000`)*; **al tick `0` `A = 0`** *(la corsa parte da `A = 0`: `B = 0`, scritto)*.
**Per ogni stato:** **il centro del triangolo = la media dei tre centri della serie a quel tick; `B` medio e il suo segno sul disco di raggio `8`** *(le placchette col baricentro entro `8`)*; **il FLUSSO totale `somma B` dentro il cerchio di raggio `30`.**
### **La previsione del guardiano** *(scritta prima)*: **a `120` gradi `B` al centro diverso da zero e di segno COSTANTE** *(la materia che gira e' una corrente circolare)*; **in fase `B` circa zero.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

TICK = (500, 1000, 1500, 2000)
R_DISCO, R_FLUSSO = 8.0, 30.0
CORSE = (("T120", "triangolo_t120"), ("T-fase (video)", "triangolo_video"))


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    print("=" * 130)
    print("IL CAMPO MAGNETICO NEI TRIANGOLI (Luca 13:56; solo lettura): B = il rotore di A (_u1_prototipo.Campo.B, per placchetta, antiorario positivo); il disco di raggio %g, il flusso entro %g" % (R_DISCO, R_FLUSSO))
    print("### la previsione del guardiano (prima): a 120 gradi B al centro diverso da zero e di segno costante; in fase B circa zero")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L, n = Z["L"], Z["n"]
        C = MT.Campi(Z, "MGU", rho_c, e)
        cam = C.campo
        v = np.arange(n)
        m1, m2 = (v // L).astype(float), (v % L).astype(float)
        p1 = np.concatenate([m1 + 2.0 / 3.0, m1 + 1.0 / 3.0])
        p2 = np.concatenate([m2 + 1.0 / 3.0, m2 + 2.0 / 3.0])
        assert cam.P.shape[0] == 2 * n
        print("    %-16s %6s  %-26s %12s %6s %12s %12s %12s  %s" % ("la corsa", "k", "il centro", "B medio (8)", "segno", "B min (8)", "B max (8)", "flusso (30)", "max |B| ovunque"))
        for nome, pref in CORSE:
            serie = np.load(os.path.join(MT.DIR_REF, "%s_serie.npz" % pref))
            print("    %-16s %6d  %-26s %12s %6s %12s %12s %12s  (A = 0 al tick 0: B = 0)" % (nome, 0, "--", "0", "0", "0", "0", "0"))
            for k in TICK:
                with np.load(os.path.join(MT.DIR_E, "%s_%05d.npz" % (pref, k))) as d:
                    cam.A[...] = d["campo_A"]
                B = cam.B()
                j = int(np.nonzero(serie["k"] == k)[0][0])
                c = (float(np.mean([serie["c1_" + q][j] for q in "ABC"])), float(np.mean([serie["c2_" + q][j] for q in "ABC"])))
                r = np.hypot(*TO.scarti(p1, p2, c[0], c[1], L).T[:2])
                dentro, cerchio = r <= R_DISCO, r <= R_FLUSSO
                bm = float(B[dentro].mean())
                print("    %-16s %6d  (%8.3f, %8.3f)       %+12.4e %6s %+12.4e %+12.4e %+12.4e  %.4e" % (nome, k, c[0], c[1], bm, "+" if bm > 0 else ("-" if bm < 0 else "0"), float(B[dentro].min()), float(B[dentro].max()),
                      float(B[cerchio].sum()), float(np.max(np.abs(B)))))
            print("-" * 130)
        Z["metti"]()
    print("    (il flusso su TUTTO il toro e' zero per costruzione: ogni arco sta in due placchette con segni opposti)")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
