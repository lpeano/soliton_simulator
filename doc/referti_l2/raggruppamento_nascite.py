# -*- coding: utf-8 -*-
r"""**M2 E M3: IL RAGGRUPPAMENTO DELLE NASCITE E I LORO ANGOLI** *(il mandato di Luca `2026-11-21` `23:13` e l'aggiunta; la carta `doc/TASK_HISTORY/2026-11-21_orientamento_combinatorio.md`, sez. `3.2`; sola lettura)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/raggruppamento_nascite.py > doc/referti_l2/raggruppamento_nascite.txt

**Lo stato:** il ramo MITOSI `k 36250` *(il grafo, le posizioni del disegno, `Theta`)* e `nascite_36250.json`; la sorgente di `coppie_57.stato`.
**M2:** `S` = la media, dalla seconda nascita, della distanza in passi dalla nascita PRECEDENTE piu' vicina; `10000` estrazioni *(seme `20261121`)* di `9` nodi distinti fra gli ORIGINARI con `r` in `[17.5, 19.5)`; `p = P(S_caso <= S)`.
**M3:** l'angolo di ogni nascita attorno alla sorgente e la distanza dall'asse piu' vicino *(multipli di `60` gradi)*; il MASSIMO delle `9` contro le stesse estrazioni; poi i `20` archi con `|Theta|` piu' alto, l'angolo del punto medio, la distanza dall'asse; **il caso noto:** un `Theta` isotropo sul toro iniziale *(`exp(-(r_mid - 18.9)^2/2)`)*: la distanza media dall'asse dei `20` archi piu' alti contro quella degli archi dell'anello, entro `5` gradi.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import coppie_57 as CP  # noqa: E402

SEME, N_ESTR = 20261121, 10000
ANELLO = (17.5, 19.5)
ASSI_ALTRI = (0.0, 60.0, 120.0, 240.0)


def dall_asse(a):
    x = np.mod(a, 60.0)
    return np.minimum(x, 60.0 - x)


def punti_medi(S, archi):
    """### l'angolo e il raggio del punto medio degli archi, attorno alla sorgente *(nel disegno)*."""
    from solitone import toro as TO
    L = CP.L
    src = S["sorgente"]
    a = TO.scarti(S["m1"][S["ii"][archi]], S["m2"][S["ii"][archi]], S["m1"][src], S["m2"][src], L)
    b = TO.scarti(S["m1"][S["jj"][archi]], S["m2"][S["jj"][archi]], S["m1"][src], S["m2"][src], L)
    m = 0.5 * (a[:, :2] + b[:, :2])
    return np.degrees(np.arctan2(m[:, 1], m[:, 0])) % 360.0, np.hypot(m[:, 0], m[:, 1])


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "coppie_57.py"))
    _presidio.avvia(__file__)
    esiti = []
    print("=" * 130)
    print("M2 E M3, IL RAGGRUPPAMENTO E GLI ANGOLI DELLE NASCITE (Luca 2026-11-21 23:13 e l'aggiunta; la carta sez. 3.2): sola lettura")
    print("=" * 130)
    # ### IL CASO NOTO DI M3: il Theta isotropo sul toro iniziale
    T0 = CP.stato(None)
    tutti = np.arange(len(T0["ii"]))
    ang0, rm0 = punti_medi(T0, tutti)
    th_iso = np.exp(-0.5 * (rm0 - 18.9) ** 2)
    top0 = np.argsort(-th_iso, kind="stable")[:20]
    anello0 = (rm0 >= ANELLO[0]) & (rm0 < ANELLO[1])
    d_top, d_an = float(np.mean(dall_asse(ang0[top0]))), float(np.mean(dall_asse(ang0[anello0])))
    print("### IL CASO NOTO DI M3: Theta isotropo sul toro iniziale: i 20 archi piu' alti a r %.3f..%.3f, la distanza media dall'asse %.3f gradi; gli archi dell'anello (%d) %.3f gradi" % (
        float(rm0[top0].min()), float(rm0[top0].max()), d_top, int(anello0.sum()), d_an))
    esiti.append(("DEVE: il Theta isotropo non preferisce gli assi oltre la grana: |%.3f - %.3f| <= 5 gradi" % (d_top, d_an), abs(d_top - d_an) <= 5.0))
    # ### lo stato k 36250 e le nascite
    f = os.path.join(CP.D, "stato_36250.npz")
    S = CP.stato(f)
    with open(os.path.join(CP.D, "nascite_36250.json"), encoding="utf-8") as fh:
        B = json.load(fh)
    nati = np.array([b["nodi"]["n"] for b in B], dtype=np.int64)
    A = CP.grafo(S)
    src = S["sorgente"]
    print("### lo stato %s (sha1 %s): k %d, n %d; la sorgente %d; %d nascite (i nodi %s)" % (os.path.basename(f), CP.sha1(f)[:8], S["k"], S["n"], src, len(nati), list(nati)))
    # ### M2
    Dn = CP.passi_da(A, nati)[:, nati]
    dmin = [int(np.min(Dn[j, :j])) for j in range(1, len(nati))]
    Sobs = float(np.mean(dmin))
    orig = np.arange(CP.L * CP.L)
    anello = orig[(S["r"][orig] >= ANELLO[0]) & (S["r"][orig] < ANELLO[1])]
    Da = CP.passi_da(A, anello)[:, anello]
    rng = np.random.default_rng(SEME)
    Sc, Mc = np.empty(N_ESTR), np.empty(N_ESTR)
    ang_an, _r_an = CP.angolo_e_r(S, anello, src)
    da_an = dall_asse(ang_an)
    for q in range(N_ESTR):
        sel = rng.choice(anello.size, size=len(nati), replace=False)
        Dq = Da[np.ix_(sel, sel)]
        Sc[q] = float(np.mean([np.min(Dq[j, :j]) for j in range(1, len(nati))]))
        Mc[q] = float(np.max(da_an[sel]))
    p2 = float(np.mean(Sc <= Sobs))
    print("### M2: la distanza in passi dalla nascita precedente piu' vicina: %s; S = %.4f; a caso (%d nodi dell'anello %s, %d estrazioni, seme %d): media %.3f, il 1%% %.3f; p = %.4f" % (
        dmin, Sobs, anello.size, ANELLO, N_ESTR, SEME, float(Sc.mean()), float(np.quantile(Sc, 0.01)), p2))
    pm4 = p2 < 0.01
    print("### P-M4 (il raggruppamento oltre il caso, p < 0.01): %s (p %.4f)" % ("VERA" if pm4 else "FALSA", p2))
    # ### M3: gli angoli delle nascite
    ang, rr = CP.angolo_e_r(S, nati, src)
    da = dall_asse(ang)
    Mobs = float(np.max(da))
    p3 = float(np.mean(Mc <= Mobs))
    print("### M3: le nascite attorno alla sorgente:")
    for j, v in enumerate(nati):
        print("    la nascita %d (k %d), il nodo %d: l'angolo %.2f gradi, r %.3f, dall'asse %.2f gradi" % (j + 1, B[j]["k"], v, ang[j], rr[j], da[j]))
    print("### il massimo dall'asse %.2f gradi; a caso (le stesse estrazioni): il massimo medio %.2f, il 1%% %.2f; p = %.4f" % (Mobs, float(Mc.mean()), float(np.quantile(Mc, 0.01)), p3))
    pm5 = Mobs <= 10.0 and p3 < 0.01
    print("### P-M5 (tutte entro 10 gradi da un asse e p < 0.01): %s" % ("VERA" if pm5 else "FALSA"))
    # ### i 20 archi piu' maturi
    th = np.abs(S["theta"])
    top = np.argsort(-th, kind="stable")[:20]
    angt, rt = punti_medi(S, top)
    dat = dall_asse(angt)
    print("### i 20 archi con |Theta| piu' alto a k %d (dove maturano le prossime nascite):" % S["k"])
    for q, a in enumerate(top):
        print("    l'arco %6d (%d -> %d): |Theta| %.6f, l'angolo %.2f gradi, r %.3f, dall'asse %.2f gradi (l'asse %d)" % (
            a, S["ii"][a], S["jj"][a], th[a], angt[q], rt[q], dat[q], int(round(angt[q] / 60.0)) % 6 * 60))
    vicini = {ax for q in range(20) for ax in ASSI_ALTRI if dat[q] <= 10.0 and abs(((angt[q] - ax + 180.0) % 360.0) - 180.0) <= 10.0}
    pm6 = len(vicini) >= 2
    print("### P-M6 (fra i 20, archi entro 10 gradi da almeno due assi fra 0, 60, 120, 240): %s (gli assi toccati %s)" % ("VERA" if pm6 else "FALSA", sorted(vicini)))
    print("-" * 130)
    for nm, ok in esiti:
        print("  %-110s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0 if all(ok for _n, ok in esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
