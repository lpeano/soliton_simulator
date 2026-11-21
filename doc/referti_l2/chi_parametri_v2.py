# -*- coding: utf-8 -*-
r"""**D3: `kappa` IL NUMERO DI OGGI** *(la decisione di Luca `2026-11-21` `23:13`; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md` del ramo `mitosi`, sez. `4.3`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_parametri_v2.py prova > doc/referti_l2/chi_parametri_v2.txt

**`KAPPA`** = il valore AL BIT del `meta["parametri"]` della corsa del mattone con `chi` *(`stato_03000.npz`)*, **costante**: `parametri_v2` **non legge nessuna posizione**; `m0` = la media di `u = s Q - e0 rho` sullo stato di partenza *(come `chi_tick.parametri`: `"C2"` il `k 0` di C2, `"vuoto"` `vuoto_fresco`, oppure UNO STATO dato)*; **`c0 = KAPPA m0`.**
**`prova` (O8):** `parametri_v2` a partenza `"C2"` = il `meta["parametri"]` della corsa *(`kappa`, `c0`, `m0`)* AL BIT, e = `chi_tick.parametri` di oggi AL BIT; **DEVE FALLIRE:** `KAPPA` col suo ultimo bit cambiato -> `c0` diverso.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_tick as CT  # noqa: E402

KAPPA = 0.0002528944153922671          # ### D3 (Luca 2026-11-21 23:13): il numero di oggi, AL BIT col meta della corsa del mattone con chi; COSTANTE


def parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, partenza="C2", stato=None, kappa=KAPPA):
    """### `(P, m0)`: `m0` dallo stato di partenza; `kappa` il NUMERO; `c0 = kappa m0`. ### Nessuna posizione letta."""
    mot = Z["mot"]
    if stato is not None:
        Z["metti"]({x: stato[x].copy() for x in Z["chiavi"]})
    elif partenza == "C2":
        CSB.prepara(Z, 186, False, rho_c, e, t0)
    else:
        PS.MT.vuoto_fresco(Z, t0)
    m0 = float(CT.u_di(mot, Z["st"], Z["par"], s, e0).mean())
    return CT.Parametri(kappa, kappa * m0, s, e0), m0


def prova():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "chi_tick.py"))
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    MT = PS.MT
    rho_c, t0, e = MT.rho_c_assoluto(), MT.G2.T0, MT.PB.E_DECISO
    f = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "CHI", "mattone", "stato_03000.npz")
    with np.load(f) as d:
        pm = json.loads(str(d["meta"]))["parametri"]
    esiti = []
    print("=" * 130)
    print("O8: KAPPA IL NUMERO DI OGGI (Luca 2026-11-21 23:13, D3): parametri_v2 contro il meta della corsa (%s) e contro chi_tick.parametri" % os.path.basename(f))
    print("=" * 130)
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        s = float(Z["s"])
        Lp = CT.Laplaciano(Z["mot"])
        e0 = float(PS.PO.campi(Z, rho_c, e).e0)
        P2, m02 = parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, "C2")
        P1, m01, _a, _c = CT.parametri(Z, PS, CSB, Lp, rho_c, e, t0, s, e0, "C2")
        Pf, _m = parametri_v2(Z, PS, CSB, rho_c, e, t0, s, e0, "C2", kappa=float(np.nextafter(KAPPA, 1.0)))
        Z["metti"]()
    print("### parametri_v2: kappa %r, c0 %r, m0 %r" % (P2.kappa, P2.c0, m02))
    print("### il meta della corsa: kappa %r, c0 %r, m0 %r" % (pm["kappa"], pm["c0"], pm["m0"]))
    print("### chi_tick.parametri (la posizione): kappa %r, c0 %r, m0 %r" % (P1.kappa, P1.c0, m01))
    ok_m = P2.kappa == pm["kappa"] and P2.c0 == pm["c0"] and m02 == pm["m0"]
    ok_p = P2.kappa == P1.kappa and P2.c0 == P1.c0 and m02 == m01 and P2.c2 == P1.c2 and P2.m2 == P1.m2
    esiti.append(("O8: parametri_v2 = il meta della corsa (kappa, c0, m0) AL BIT", ok_m))
    esiti.append(("O8: parametri_v2 = chi_tick.parametri di oggi AL BIT (kappa, c0, m0, c2, m2)", ok_p))
    esiti.append(("DEVE FALLIRE: kappa con l'ultimo bit cambiato -> c0 diverso (%r)" % Pf.c0, Pf.c0 != pm["c0"]))
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(prova() if sys.argv[1:] == ["prova"] else 2)
