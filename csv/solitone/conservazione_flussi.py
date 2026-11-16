# -*- coding: utf-8 -*-
r"""**LA CONSERVAZIONE CON `J_a`, PRIMA DI LEGGERE LE FRECCE** *(Luca `2026-11-15` `03:19`, (2); la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `22.6`)*.

    python csv/solitone/conservazione_flussi.py > doc/referti_l2/mattone/conservazione_flussi.txt

**Dal video** *(`triangolo_video_00500`, `01000`, `01500` su E:; le mappe di `rho` ogni `20` tick in `triangolo_video_mappe.npz`)*, **solo lettura:**
- **(I) L'IDENTITA' su un passo:** **su una COPIA dello stato un `spostamento_trasporto` a frazione `0.5`** *(come `triangolo_flussi.py`: `U` dal campo, il `cs` della scena)*; **`J_a` = la variazione di `|v0|^2` della CODA
dell'arco `a`** *(il segno: negativo quando la materia la lascia)*; **per nodo `- div J` := somma sugli archi con la CODA nel nodo di `J_a` meno la somma su quelli con la TESTA nel nodo** *(la testa cambia di `-J_a`: lo spostamento
mescola solo le due estremita' dello stesso arco)*; **contro la variazione VERA di `rho` per nodo nel passo: deve tornare a meno dell'arrotondamento.**
- **(II) LA DINAMICA:** **`(rho(k + 20) - rho(k - 20)) / 40`** *(le mappe, per tick)* **contro `2 x (- div J)`** *(due spostamenti per tick)*: **la correlazione, il rapporto delle norme, la frazione di nodi col segno uguale**
*(sui nodi dove `rho` cambia piu' dell'`1%` del massimo)*. ### **Dichiarato:** **sul tick vero il passo usa il `cs` del lapse; qui quello della scena; e in un tick si muove materia anche col bordo.**
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

TICK = (500, 1000, 1500)
DT = 20


def main():
    import _presidio
    import _u1_prototipo as U1
    _presidio.avvia(os.path.join(_QUI, "mattone.py"))
    _presidio.avvia(os.path.join(_CSV, "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    mp = np.load(os.path.join(MT.DIR_REF, "triangolo_video_mappe.npz"))
    tk, RHO = np.array(mp["tick"]), mp["rho"]
    print("=" * 130)
    print("LA CONSERVAZIONE CON J_a (Luca 03:19, (2)): (I) l'identita' su un passo; (II) la dinamica: le mappe a k -+ %d contro 2 x (- div J) a k; il video, k %s" % (DT, TICK))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, n, mot = Z["st"], Z["n"], Z["mot"]
        nodo = np.asarray(Z["z"]["inc"].nodo)
        coda, testa = nodo[0::2], nodo[1::2]
        sp = mot.operatori["spostamento_trasporto"]
        for k in TICK:
            with np.load(os.path.join(MT.DIR_E, "triangolo_video_%05d.npz" % k)) as d:
                Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
                A = d["campo_A"].copy()
            C = MT.Campi(Z, "MGU", rho_c, e)
            C.campo.A[...] = A
            U1.scrivi_U(mot, C.campo)
            m = C.campo.m
            rho_prima = MT.rho_di(Z).copy()
            prima = np.sum(np.abs(st["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1).copy()
            sp(st, Z["par"], 0.5)
            J = np.sum(np.abs(st["psi_h"].reshape(m, 2, 2)[:, 0, :]) ** 2, axis=1) - prima
            drho_vero = MT.rho_di(Z) - rho_prima
            Z["metti"]()
            mdiv = np.bincount(coda, weights=J, minlength=n) - np.bincount(testa, weights=J, minlength=n)
            e1 = float(np.max(np.abs(drho_vero - mdiv))) / float(np.max(np.abs(drho_vero)))
            print("### k %d (I) L'IDENTITA' su un passo: max |drho vero - (- div J)| / max |drho vero| = %.3e   %s" % (k, e1, "TORNA" if e1 < 1e-10 else "### NON TORNA"))
            i0, i1 = int(np.nonzero(tk == k - DT)[0][0]), int(np.nonzero(tk == k + DT)[0][0])
            rate = (np.asarray(RHO[i1], dtype=float) - np.asarray(RHO[i0], dtype=float)) / (2.0 * DT)
            pred = 2.0 * mdiv
            sel = np.abs(rate) > 0.01 * np.abs(rate).max()
            corr = float(np.corrcoef(rate[sel], pred[sel])[0, 1])
            rap = float(np.linalg.norm(pred[sel]) / np.linalg.norm(rate[sel]))
            segno = float(np.mean(np.sign(rate[sel]) == np.sign(pred[sel])))
            print("    (II) la dinamica, %d nodi: la correlazione %.4f; |2 (- div J)| / |drho/dt| = %.4f; il segno uguale nel %.1f%% dei nodi" % (int(sel.sum()), corr, rap, 100.0 * segno))
    print("-" * 130)
    print("### IL SEGNO: J_a = la variazione della CODA dell'arco a (negativa se la materia la lascia); - div J per nodo = somma(J delle code) - somma(J delle teste)")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
