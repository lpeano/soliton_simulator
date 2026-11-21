# -*- coding: utf-8 -*-
r"""**IL CASO NOTO FISICO DI E2, CORRETTO: LA COVARIANTE SUL VUOTO F3 PURO** *(la correzione di Luca `2026-11-20` `12:10`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_e_specchio.md`, sez. `5`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/covariante_vuoto_F3.py > doc/referti_l2/covariante_vuoto_F3.txt

**La correzione** *(l'errore `n.191` del guardiano)*: **la covariante RIPRISTINA la norma, e a norma fissata l'energia del vuoto non dipende dal numero dei nodi** *(A3, carta della mitosi `13.3`)*: **l'attesa NON e' `DH_cov = H / n`** *(come scritto nella carta 1.4 e stampato da `covariante_e_famiglia.py referto`: SUPERATA)*. **L'attesa:** **`DH_cov` vicino a `0`**, con un residuo atteso dalle estremita' nuove di `k` e `l` *(la media di due direzioni con fasi F3 diverse ne riduce l'ampiezza)*.
**La misura:** sul vuoto F3 puro *(la scena S162, `psi = 0`, l'arco di `regole_fase_F3.py`)*: **`DH_cov`** *(la covariante di `covariante_e_famiglia.py`)* e, accanto, **la covariante con l'estremita' nuova di `k` e di `l` presa da UNA direzione invece che dalla media** *(verso `i`; e, accanto, verso `j`)*: **la parte dovuta a `k` e `l` = `DH_cov - DH_una`.** **Se quella parte spiega il residuo, il caso e' letto: POST-HOC, dichiarato** *(la correzione arriva prima della misura, ma il criterio «spiega» si legge sui numeri)*.
**Il caso noto del CODICE** *(Q-A4)*: `cov_grezza` di questo script con la media = `covariante_e_famiglia.cov_grezza` AL BIT.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "mattone")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import covariante_e_famiglia as CF  # noqa: E402
import nascita_energia_nulla as NN  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402
import regole_fase_F3 as RF  # noqa: E402


def cov_una(G, x, a, nodi, keep, m2, verso):
    """### La covariante con l'estremita' nuova di `k` (e di `l`) presa da UNA direzione: verso `i` o verso `j`."""
    ii, jj, _nn, _vec = G
    y = CF.cov_grezza(G, x, a, nodi, keep, m2)
    b = m2 - 4
    v = nodi[verso]
    y[2 * (b + 2) + 1] = RF.estremita_di(ii, jj, x, nodi["k"], v)
    y[2 * (b + 3) + 1] = RF.estremita_di(ii, jj, x, nodi["l"], v)
    return y


def normata(y, x, s_old, s_new):
    Nb, Na = CF.norma(x, s_old), CF.norma(y, s_new)
    if Nb > 0.0 and Na > 0.0:
        y[s_new] *= math.sqrt(Nb / Na)
    return y


def main():
    import _presidio
    import _massa_nei_difetti as MD
    import mattone as MT
    _presidio.avvia(os.path.join(_QUI, "covariante_e_famiglia.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("IL CASO NOTO FISICO DI E2, CORRETTO (Luca 2026-11-20 12:10): LA COVARIANTE SUL VUOTO F3 PURO")
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        L = Z["L"]
        ii, jj, nn, dirs = MD.toro(L)
        phi_v = np.asarray(Z["phi_v"]).copy()
    G = (ii, jj, nn, np.asarray(dirs, dtype=float))
    psi0 = np.zeros((len(phi_v), 2), dtype=complex)
    a = 3 * (81 * L + 81)
    F0 = ND.famiglie(G, psi0, phi_v)
    with np.errstate(invalid="ignore", divide="ignore"):
        P = NN.preparo(G, psi0, phi_v, a)
    nodi, keep, m2 = P["out"][3], P["out"][4], len(P["G2"][0])
    s_old, s_new = CF.stelle(G, P["G2"], nodi)
    esiti = []
    ref = CF.cov_grezza(G, phi_v, a, nodi, keep, m2)
    mia = cov_una(G, phi_v, a, nodi, keep, m2, "i")
    b = m2 - 4
    mia[2 * (b + 2) + 1] = 0.5 * (RF.estremita_di(ii, jj, phi_v, nodi["k"], nodi["i"]) + RF.estremita_di(ii, jj, phi_v, nodi["k"], nodi["j"]))
    mia[2 * (b + 3) + 1] = 0.5 * (RF.estremita_di(ii, jj, phi_v, nodi["l"], nodi["i"]) + RF.estremita_di(ii, jj, phi_v, nodi["l"], nodi["j"]))
    esiti.append(("il caso noto del codice: cov_una con la media rimessa = covariante_e_famiglia.cov_grezza AL BIT", bool(np.array_equal(mia, ref))))
    Cp = CF.cov(G, psi0, a, P, s_old, s_new)
    Cf = CF.cov(G, phi_v, a, P, s_old, s_new)
    D = ND.delta(F0, ND.famiglie(P["G2"], Cp, Cf))
    print("### il vuoto F3 puro (S162, L %d, n %d, l'arco %d: %d -> %d; k %d, l %d); H %.10e" % (L, nn, a, ii[a], jj[a], nodi["k"], nodi["l"], F0["tot"]))
    print("### DH_cov (la covariante, la media in k e l) %+.6e; per termine: %s" % (D["tot"], ", ".join("%s %+.4e" % (k, D[k]) for k in CF.CHIAVI[:-1])))
    k_end = 2 * (b + 2) + 1
    print("    le ampiezze prima del fattore: l'estremita' nuova di k |media| %.6f contro |verso i| %.6f e |verso j| %.6f; il fattore della stella %.6f" % (
        abs(ref[k_end]), abs(RF.estremita_di(ii, jj, phi_v, nodi["k"], nodi["i"])), abs(RF.estremita_di(ii, jj, phi_v, nodi["k"], nodi["j"])),
        math.sqrt(CF.norma(phi_v, s_old) / CF.norma(ref, s_new))))
    for verso in ("i", "j"):
        y = normata(cov_una(G, phi_v, a, nodi, keep, m2, verso), phi_v, s_old, s_new)
        Du = ND.delta(F0, ND.famiglie(P["G2"], Cp, y))
        print("### la covariante con k e l presi da UNA direzione (verso %s): DH %+.6e; la parte dovuta a k e l (DH_cov - DH_una) %+.6e (%.1f%% di DH_cov); per termine: %s" % (
            verso, Du["tot"], D["tot"] - Du["tot"], 100.0 * (D["tot"] - Du["tot"]) / D["tot"] if D["tot"] != 0 else float("nan"),
            ", ".join("%s %+.4e" % (k, Du[k]) for k in CF.CHIAVI[:-1])))
    print("### accanto (regole_fase_F3.txt): FA sullo stesso arco dH +3.476457e+00")
    print("-" * 130)
    for nm, ok in esiti:
        print("  DEVE: %-118s %s" % (nm, "PASSA" if ok else "### FALLISCE"))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
