# -*- coding: utf-8 -*-
r"""**IL DETERMINISMO E LA FILA DELLA FAMIGLIA BETA, v2** *(Luca `2026-11-20` `11:57`; la carta `doc/TASK_HISTORY/2026-11-20_covariante_e_specchio.md`, sez. `6`)*. [[MITOSI-QUANTO-OLONOMIA]]

    E:\python\py3132\python.exe doc/referti_l2/covariante_det_v2.py A          (A = a, b: due processi)

**Perche' la v2** *(DICHIARATO)*: `covariante_e_famiglia.py det` *(`d6bf4a21`)* **e' caduto nella FILA**: `RuntimeError: nessun vicino di 21125 nella direzione opposta` *(`regole_fase_F3.opposto`)*. **La covariante della carta 1.1 usa il vicino di `i` in `-a` e quello di `j` in `+a`: accanto a un difetto gia' nato quel vicino NON ESISTE** *(il grafo non e' piu' un reticolo)*. **Un riscontro, non un errore da aggirare:** la covariante come scritta **non e' definita su tutto il grafo cresciuto.** **La v2:** **i `100` archi salvati PRIMA della fila** *(la v1 salvava tutto alla fine e ha perso tutto)*; **la fila stampa ogni nascita mentre avviene**; **un candidato dove la covariante non e' definita e' SALTATO e CONTATO** *(`cov_non_definita`)*, come gli altri saltati. **Il resto e' la v1:** `covariante_e_famiglia.nascita`, `tabella`, `sha`, e i file `det_<A>.npz` nello STESSO formato *(cosi' `covariante_e_famiglia.py referto` li legge)*.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import covariante_e_famiglia as CF  # noqa: E402
import nascita_energia_nulla as NN  # noqa: E402
import nascita_dentro_fuori as ND  # noqa: E402


def fila(G, psi, phi, archi, F0p):
    righe, salt = [], {"diviso": 0, "senza_radice": 0, "non_triangolo": 0, "cov_non_definita": 0}
    H = [F0p["tot"]]
    Gc, pc, fc = G, psi, phi
    Fm, Fp = NN.F_mano(Gc, pc, fc), F0p
    for c, a0 in enumerate(archi):
        if len(righe) >= CF.N_FILA:
            break
        i, j = int(G[0][a0]), int(G[1][a0])
        q = np.where((Gc[0] == i) & (Gc[1] == j))[0]
        if len(q) == 0:
            salt["diviso"] += 1
            continue
        try:
            R, rad, _T = CF.nascita(Gc, pc, fc, int(q[0]), Fm, Fp, pieno=False)
        except AssertionError:
            salt["non_triangolo"] += 1
            continue
        except RuntimeError as e:
            salt["cov_non_definita"] += 1
            print("    il candidato %d (l'arco %d: %d -> %d): la covariante NON e' definita (%s)" % (c, int(a0), i, j, e))
            continue
        if rad is None:
            salt["senza_radice"] += 1
            continue
        Gc, pc, fc = rad
        Fp = ND.famiglie(Gc, pc, fc)
        Fm = NN.F_mano(Gc, pc, fc)
        H.append(Fp["tot"])
        righe.append((int(a0), i, j, R["beta"], H[-1] - H[-2], abs(H[-1] - H[-2]) / abs(H[-2])))
        print("    la nascita %2d (il candidato %d, l'arco %d: %d -> %d): beta* %.6f; H(dopo) - H(prima) %+.3e, relativo %.3e" % (len(righe), c, int(a0), i, j, R["beta"], righe[-1][4], righe[-1][5]))
        sys.stdout.flush()
    return righe, salt, np.array(H)


def main(nome):
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "covariante_e_famiglia.py"))
    _presidio.avvia(__file__)
    os.makedirs(CF.DIR_O, exist_ok=True)
    G, psi, phi, archi, r, Tk, centro = NN.carica()
    assert len(archi) == 2929
    F0m, F0p = NN.F_mano(G, psi, phi), ND.famiglie(G, psi, phi)
    sel = list(range(CF.N_DET))
    print("### %s (v2): %d archi; H %.10e" % (nome, len(sel), F0p["tot"]))
    Rs, t0 = [], time.time()
    for q in sel:
        R, _r, _T = CF.nascita(G, psi, phi, int(archi[q]), F0m, F0p)
        Rs.append(R)
    T = CF.tabella(Rs)
    f = os.path.join(CF.DIR_O, nome + ".npz")
    np.savez(f, sel=np.asarray(sel), tempo=time.time() - t0, **T)
    print("### %s: i %d archi salvati PRIMA della fila; lo sha1 dei risultati %s; %.0f s" % (nome, len(sel), CF.sha(T), time.time() - t0))
    sys.stdout.flush()
    righe, salt, H = fila(G, psi, phi, archi, F0p)
    np.savez(f, sel=np.asarray(sel), tempo=time.time() - t0, fila=np.array(righe, dtype=float).reshape(-1, 6), fila_H=H, **T)
    print("### la fila: %d nascite, saltati %s; %.0f s" % (len(righe), salt, time.time() - t0))
    return 0


if __name__ == "__main__":
    sys.exit(main("det_" + sys.argv[1]))
