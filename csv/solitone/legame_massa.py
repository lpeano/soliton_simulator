# -*- coding: utf-8 -*-
r"""**L'ENERGIA DI LEGAME A MASSA UGUALE** *(Luca `2026-11-15` `03:19`, (1): la proposta di `0a512f08`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `22.6`)*.

    python csv/solitone/legame_massa.py > doc/referti_l2/mattone/legame_massa.txt

**Solo lettura.** **`b = E3 / M3 - E1 / M1`** *(l'energia per unita' di massa del triangolo meno quella del mattone solo, (T-solo-60); `E0 = 0`: la scena vuota, `0a512f08`)* **e `B_m = M3 b`** *(il legame a massa uguale)*.
**Le energie: `tot + K + V` dalle tabelle R-CONTI** *(la media sugli ultimi `100` tick; `legame.tabella`)*; **le masse TOTALI** *(`somma |psi|^2`)* **dagli stati salvati** *(il triangolo `triangolo_<v>_00500` ... `02000`,
(T-solo) `L162_MGU_00500` ... `02000`)* **e dallo stato `0` RICOSTRUITO con le righe dell'incollatura** *(come `triangolo_mappe.py`)*. ### **Dichiarato:** **le energie sono medie, le masse istantanee; l'errore NON c'e'**
*(le corse non hanno salvato `tot` per tick: il rumore della scena vuota era zero, `0a512f08`)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import legame as LG  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

PUNTI = (0, 500, 1000, 1500, 2000)


def main():
    import _presidio
    for m in ("legame", "mattone", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ref = MT.DIR_REF
    E1 = LG.tabella(os.path.join(ref, "triangolo_solo.txt"))
    E3 = {v: LG.tabella(os.path.join(ref, "triangolo_%s.txt" % v)) for v in ("fase", "sfasati")}
    FR = {v: [MTR.francobollo(k) for k in MTR.VARIANTI[v]] for v in ("solo", "fase", "sfasati")}     # ### i francobolli PRIMA della scena
    M = {}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        st, L = Z["st"], Z["L"]
        for v in ("solo", "fase", "sfasati"):
            centri = MTR.posti(Z["bordo"]["c0"], FR[v], L)
            MT.vuoto_fresco(Z, MT.G2.T0)
            vuoto = {x: st[x].copy() for x in Z["chiavi"]}
            psi = None
            for fr, c in zip(FR[v], centri):
                for x in Z["chiavi"]:
                    st[x][...] = vuoto[x]
                MT.incolla(Z, fr, c, True)
                psi = st["psi_h"].copy() if psi is None else psi + st["psi_h"]
            M[(v, 0)] = float(np.sum(np.abs(psi) ** 2))
            for k in PUNTI[1:]:
                f = os.path.join(MT.DIR_E, ("L162_MGU_%05d.npz" % k) if v == "solo" else ("triangolo_%s_%05d.npz" % (v, k)))
                with np.load(f) as d:
                    M[(v, k)] = float(np.sum(np.abs(d["psi_h"]) ** 2))
        Z["metti"]()
    print("=" * 130)
    print("L'ENERGIA DI LEGAME A MASSA UGUALE (Luca 03:19): b = E3/M3 - E1/M1, B_m = M3 b; le energie MEDIE sugli ultimi 100 tick, le masse TOTALI istantanee; l'errore NON c'e' (dichiarato)")
    print("=" * 130)
    for k in PUNTI:
        print("    (T-solo) k %4d: E1 %.6f  M1 %.6e  E1/M1 %.8f" % (k, E1[k], M[("solo", k)], E1[k] / M[("solo", k)]))
    for v in ("fase", "sfasati"):
        print("### (T-%s)" % v)
        for k in PUNTI:
            e3, e1 = E3[v][k] / M[(v, k)], E1[k] / M[("solo", k)]
            b = e3 - e1
            print("    k %4d: E3 %.6f  M3 %.6e (3 M1 = %.6e)  E3/M3 %.8f  b %+.6e  B_m = M3 b %+.4f  (B di 0a512f08 %+.4f)"
                  % (k, E3[v][k], M[(v, k)], 3 * M[("solo", k)], e3, b, M[(v, k)] * b, E3[v][k] - 3 * E1[k]))
    print("  (b < 0: per unita' di massa il triangolo ha MENO energia del mattone solo; b > 0: PIU'; senza l'errore NON si dice «legato»)")
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
