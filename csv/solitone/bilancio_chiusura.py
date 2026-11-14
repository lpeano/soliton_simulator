# -*- coding: utf-8 -*-
r"""**LA CHIUSURA DELLA VOCE `15`** *(Luca `2026-11-14` `09:34`, C1-C4; la carta `doc/TASK_HISTORY/2026-11-14_bilancio_energie.md`, sez. `8`)*.

    python csv/solitone/bilancio_chiusura.py > doc/referti_l2/bilancio_chiusura.txt

**Solo lettura** *(nessuna corsa)*: **le serie per tick di `bilancio_corsa`** *(`doc/referti_l2/bilancio/<braccio>_corsa.npz`: `E_pt`, `M_pt` = prima e dopo il bordo)* **e lo stato `0` su E:** *(per `tot(0)` e la massa all'inizio)*.
### **C2:** **il residuo `r(k) = tot(k) - tot(0) + l'energia tolta dal bordo fino a k`, mediato in `20` finestre di `100` tick; il rumore di una media `s_w` = la deviazione standard delle `20` medie di
`(0)_2000`** *(scelta mia, dichiarata)*. **C3:** **`D_w` = la media di `Grampa` meno quella di `(0)_2000`; `W = D(1250) - D(500)`** *(`D(c)` sui tick `c - 49` ... `c + 50`)*, **il rumore `2 s_w`;**
**DEVE FALLIRE: `|W|` entro `3` volte il rumore** *(RILETTO sui tick `500`-`1250` DOPO il risultato, dichiarato)*. **C1:** **DEVE: la massa di `(0)_2000` col bordo entro `1e-11` relativo a ogni tick** *(n.157: RIVISTA DOPO il
risultato, dichiarata)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import bilancio_corsa as BC  # noqa: E402
import conti as CO  # noqa: E402
import s5_coppia_lapse as G2  # noqa: E402

FINESTRA = 100                 # ### C2 (Luca 09:34): l'energia in MEDIA su 100 tick
TOLL_MASSA = 1e-11             # ### C1, n.157: RIVISTA DOPO il risultato (dichiarato)
C_PRIMA, C_DOPO = 500, 1250    # ### C3: il DEVE FALLIRE riletto sui tick 500-1250 (dichiarato)
N_ERR = 3.0
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    for m in ("conti", "bilancio_corsa"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("LA CHIUSURA DELLA VOCE 15 (Luca 09:34, C1-C4): l'energia in MEDIA su %d tick; il lavoro dell'accensione di G = Grampa meno (0)_2000; la massa entro %g (n.157, RIVISTA dopo il risultato)" % (FINESTRA, TOLL_MASSA))
    print("=" * 130)
    E0, M0 = {}, {}
    with CO.scena(G2.CORSA, G2.T0) as Z:
        for nome in BC.BRACCI:
            with np.load(os.path.join(BC.DIR_E, "%s_%05d.npz" % (nome, 0))) as d:
                Z["metti"]({kk: d[kk] for kk in Z["chiavi"]})
            c = CO.conti_nodo(Z)
            E0[nome], M0[nome] = float(np.sum(c["tot"])), float(np.sum(c["M"]))
        Z["metti"]()
    res, Mres = {}, {}
    for nome in BC.BRACCI:
        c = np.load(os.path.join(BC.DIR_REF, "%s_corsa.npz" % nome))
        E_pt, M_pt = c["E_pt"], c["M_pt"]
        assert len(E_pt) == BC.N_TICK, (nome, len(E_pt))
        res[nome] = E_pt[:, 1] - E0[nome] + np.cumsum(E_pt[:, 0] - E_pt[:, 1])        # ### r(k), k = 1 ... 2000
        Mres[nome] = (M_pt[:, 1] - M0[nome] + np.cumsum(M_pt[:, 0] - M_pt[:, 1])) / M0[nome]
        print("### (%s) tot(0) %.10e, la massa all'inizio %.10e; il residuo per tick: da %+.3e a %+.3e" % (nome, E0[nome], M0[nome], res[nome].min(), res[nome].max()))
    assert E0["Grampa"] == E0["0_2000"], "i due bracci NON partono dallo stesso tot"
    # ---------------------------------------------------------------- C2: le medie su 100 tick
    nw = BC.N_TICK // FINESTRA
    med = {nome: res[nome].reshape(nw, FINESTRA).mean(axis=1) for nome in BC.BRACCI}
    s_w = float(np.std(med["0_2000"]))
    D = med["Grampa"] - med["0_2000"]
    print("-" * 130)
    print("### C2-C3: il residuo MEDIO per finestra di %d tick, i due bracci e la differenza (il lavoro dell'accensione di G, finestra per finestra)" % FINESTRA)
    print("    %-12s %16s %16s %16s" % ("i tick", "(0)_2000", "Grampa", "Grampa - (0)"))
    for i in range(nw):
        print("    %5d-%5d  %+16.4f %+16.4f %+16.4f" % (i * FINESTRA + 1, (i + 1) * FINESTRA, med["0_2000"][i], med["Grampa"][i], D[i]))
    print("    il rumore di UNA media (la deviazione delle %d medie di (0)_2000): s_w %.4f; per tick, senza media: %.4f (il rapporto %.3f)"
          % (nw, s_w, float(np.std(res["0_2000"])), s_w / float(np.std(res["0_2000"]))))

    def D_c(cc):
        ii = np.arange(cc - 49, cc + 51) - 1          # ### i tick c-49 ... c+50 (indici da 0)
        return float(np.mean(res["Grampa"][ii]) - np.mean(res["0_2000"][ii]))
    W = D_c(C_DOPO) - D_c(C_PRIMA)
    rumore = 2.0 * s_w
    print("### C3: D(%d) %+.4f; D(%d) %+.4f; W = D(%d) - D(%d) = %+.4f; il rumore 2 s_w = %.4f (%.1f volte)"
          % (C_PRIMA, D_c(C_PRIMA), C_DOPO, D_c(C_DOPO), C_DOPO, C_PRIMA, W, rumore, abs(W) / rumore if rumore else float("inf")))
    print("    il lavoro nella rampa (0-%d): D(%d) - D(50) = %+.4f; dopo l'allargamento (%d-2000): D(1950) - D(%d) = %+.4f"
          % (C_PRIMA, C_PRIMA, D_c(C_PRIMA) - D_c(50), C_DOPO, C_DOPO, D_c(1950) - D_c(C_DOPO)))
    print("-" * 130)
    esito("(0)_2000 la massa: Delta M + la massa tolta dal bordo = 0 entro %g relativo a ogni tick (n.157, RIVISTA)" % TOLL_MASSA, float(np.max(np.abs(Mres["0_2000"]))) <= TOLL_MASSA,
          "il peggiore %.2e" % float(np.max(np.abs(Mres["0_2000"]))), True)
    esito("Grampa - (0)_2000: il lavoro W sui tick %d-%d nullo entro %g volte il rumore (RILETTO dopo il risultato)" % (C_PRIMA, C_DOPO, N_ERR), abs(W) <= N_ERR * rumore,
          "%.3e contro %g x %.3e" % (abs(W), N_ERR, rumore), False)
    print("    (Grampa) la massa: il peggiore %.2e (descrittivo)" % float(np.max(np.abs(Mres["Grampa"]))))
    print("=" * 130)
    print("### C4: IL BILANCIO NON RISOLVE L'ENERGIA DEL MOTO (SOTTO IL RUMORE); LA DOMANDA FORZA/COLPETTO PASSA ALLA COPPIA B1.")
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
