# -*- coding: utf-8 -*-
r"""**IL CAMPO CHI CON LA FORMA (a) E LO SFONDO FISSO: IL SEGNO DELLA SORGENTE NETTA PER ANELLO, `kappa`, LA DERIVA RESIDUA** *(le decisioni di Luca `2026-11-21` `16:05` e `16:08`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `7`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_sfondo.py > doc/referti_l2/chi_sfondo.txt

**Solo lettura.** **`u_k = s Q_k - e0 rho_k`** *(`Q_k` = `chi_segno.Q_di`, `cs = s` uniforme; `e0 = G2.eps_top_tl4b()`)*; **`m0` = la media di `u` a `k 0` di C2** *(`controllo_senza_bordo.prepara`, senza bordo)*; **`c0 = kappa m0`.**
**IL SEGNO** *(la `16:05`)*: `u - m0` per anello `0-23` *(r < 23.5)* POSITIVO su ogni anello, sullo stato di C2 a `k 3000` *(e stampato a `0`, `15000`, `29000`)*; se no FERMO. **`kappa`** = `sqrt(- ln(1 - a) c_chi^2 / psi_c)`, `psi = L^+ (u - media u)` a C2 `k 3000`, `a = 1 - N(rho)` al centro.
**LA DERIVA** *(la `16:08`)*: `R(t) = kappa n (media u(t) - m0)`; `somma pi`, `media chi` coi trapezi sugli stati ogni `250` tick *(C2 da `k 0` a `3000`, il tronco da `3250` a `29000`)*; **il rallentamento uniforme `1 - exp(- kappa media chi)` a `t = 3000`, contro `a`** *(P-X7: sotto il `10%`)*. **P-X6** *(`e0 rho` sotto il `20%` di `s Q` sul mattone)*: col vuoto sottratto e alla lettera.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_RADICE = os.path.dirname(os.path.dirname(_QUI))
for _p in (_QUI, os.path.join(_RADICE, "csv", "solitone"), os.path.join(_RADICE, "csv"), os.path.join(_RADICE, "primo_ordine")):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import chi_segno as CSG            # ### usato, non riscritto: Q_di, rho_di, anello, sha1, C_CHI

E_ = "E:" + os.sep
D_C2 = os.path.join(E_, "soliton_simulator", "controllo", "C2")
D_TR = os.path.join(E_, "soliton_simulator", "controllo", "mitosi_rami", "TRONCO")
K_FINE = 29000
ANELLI_SEGNO = list(range(0, 24))


def file_di(k):
    return os.path.join(D_C2 if k <= 3000 else D_TR, "stato_%05d.npz" % k)


def carica(Z, f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == CSG.sha1(f), "lo sha1 di %s NON coincide" % f
    with np.load(f) as d:
        Z["metti"]({x: d[x].copy() for x in Z["chiavi"]})
        return json.loads(str(d["meta"]))


def main():
    import _presidio
    _presidio.avvia(__file__)
    import prova_scatola5 as PS
    import controllo_senza_bordo as CSB
    import scipy.sparse as sp
    import scipy.sparse.linalg as spl
    from solitone import toro as TO
    MT, CV = PS.MT, PS.CV
    rho_c, t0, e0, e = MT.rho_c_assoluto(), MT.G2.T0, float(MT.G2.eps_top_tl4b()), MT.PB.E_DECISO
    c_chi = CSG.C_CHI
    print("=" * 150)
    print("IL CAMPO CHI CON LA FORMA (a) E LO SFONDO FISSO (Luca 2026-11-21 16:05 e 16:08; il task history del ramo lapse-u, sez. 7)")
    print("=" * 150)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, s = mot.inc.n, float(Z["s"])
        ii, jj = np.asarray(mot.inc.ii, dtype=np.int64), np.asarray(mot.inc.jj, dtype=np.int64)
        m = len(ii)
        a_ = np.arange(m)
        D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([jj, ii]), np.concatenate([a_, a_]))), shape=(n, m))
        risolvi = spl.factorized((D @ D.T).tocsc()[1:, 1:])

        def u_di():
            Q, _H = CSG.Q_di(Z, s)
            rho = CSG.rho_di(Z)
            return s * Q - e0 * rho, Q, rho

        # ------------------------------------------------------------ IL CASO NOTO: il vuoto
        MT.vuoto_fresco(Z, t0)
        uv, Qv, _ = u_di()
        res_v = uv - uv.mean()
        print("### IL CASO NOTO (il vuoto uniforme): u costante %s (%+.10e); u - media u: max |%.3e| (%s)" % (
            bool(np.all(uv == uv[0])), uv[0], float(np.max(np.abs(res_v))), "ZERO AL BIT" if np.all(res_v == 0.0) else "NON zero al bit: lo scarto e' l'arrotondamento della media, dichiarato"))
        q_v = float(Qv[0])
        # ------------------------------------------------------------ k 0 di C2: m0
        CSB.prepara(Z, 186, False, rho_c, e, t0)
        u0, Q0, rho0 = u_di()
        m0 = float(u0.mean())
        print("### k 0 di C2 (controllo_senza_bordo.prepara, senza bordo): media u = m0 = %+.12e (s media Q %+.6e, e0 media rho %.6e); somma e0 rho %.10e" % (
            m0, s * float(Q0.mean()), e0 * float(rho0.mean()), e0 * float(rho0.sum())))
        # ------------------------------------------------------------ gli stati: la media di u nel tempo, il segno, kappa
        ks = [0] + list(range(250, K_FINE + 1, 250))
        medie = {0: m0}
        kappa = None
        ok_segno = True
        for k in ks[1:]:
            meta = carica(Z, file_di(k))
            u, Q, rho = u_di()
            medie[k] = float(u.mean())
            if k in (3000, 15000, 29000):
                c = [float(x) for x in meta["centro"]]
                r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2])
                c0n = int(np.argmin(r))
                w = u - m0
                prof = [w[c0n] if R == 0 else CSG.anello(r, w, R) for R in ANELLI_SEGNO]
                pos = all(x > 0.0 for x in prof)
                mt = r < 25.0
                print("-" * 150)
                print("### k %d: IL SEGNO di u - m0 per anello 0-23: %s -> %s" % (k, " ".join("%+.2e" % x for x in prof), "POSITIVO su ogni anello" if pos else "NEGATIVO o MISTO"))
                print("    il minimo sugli anelli 0-23 %+.4e (all'anello %d); u - m0 al centro %+.6e; entro r 25: somma %+.6e" % (min(prof), int(np.argmin(prof)), w[c0n], float(w[mt].sum())))
                qv = Q - q_v
                print("    ### P-X6: entro r 25, e0 somma rho / s somma (Q - Q_vuoto) = %.4f; alla lettera e0 somma rho / s somma Q = %.4f; al centro e0 rho / s (Q - Q_vuoto) = %.4f" % (
                    e0 * float(rho[mt].sum()) / (s * float(qv[mt].sum())), e0 * float(rho[mt].sum()) / (s * float(Q[mt].sum())), e0 * rho[c0n] / (s * qv[c0n])))
                if k == 3000:
                    ok_segno = pos
                    psi = np.zeros(n)
                    psi[1:] = risolvi((u - u.mean())[1:])
                    psi -= psi.mean()
                    a = 1.0 - 1.0 / (1.0 + rho[c0n] / rho_c)
                    if psi[c0n] > 0.0:
                        kappa = math.sqrt(-math.log(1.0 - a) * c_chi ** 2 / psi[c0n])
                    print("    ### KAPPA (UNA volta, qui): a %.10e; psi al centro %+.6e -> kappa %s (DERIVATO); c0 = kappa m0 = %s" % (
                        a, psi[c0n], "%.10e" % kappa if kappa else "NON DEFINITO", "%+.10e" % (kappa * m0) if kappa else "-"))
                    a_c = a
        # ------------------------------------------------------------ LA DERIVA RESIDUA
        print("-" * 150)
        if kappa is None:
            print("### kappa non definito: la deriva non si calcola")
            return 1
        K = np.array(ks, dtype=float)
        Rt = np.array([kappa * n * (medie[k] - m0) for k in ks])
        P = np.concatenate([[0.0], np.cumsum(0.5 * (Rt[1:] + Rt[:-1]) * np.diff(K))])
        Xm = np.concatenate([[0.0], np.cumsum(0.5 * (P[1:] + P[:-1]) * np.diff(K))]) / n
        print("### LA DERIVA: R(t) = kappa n (media u - m0); somma pi e media chi coi trapezi (ogni 250 tick)")
        print("       k        media u - m0          R(t)            somma pi          media chi       1 - exp(-kappa media chi)    sul centro (a %.4e)" % a_c)
        for i, k in enumerate(ks):
            if k in (250, 500, 1000, 2000, 3000, 5000, 10000, 15000, 20000, 25000, 29000):
                sl = 1.0 - math.exp(-kappa * Xm[i])
                print("    %6d   %+14.6e   %+14.6e   %+14.6e   %+14.6e   %+18.6e        %+.4e" % (k, medie[k] - m0, Rt[i], P[i], Xm[i], sl, sl / a_c))
        i3 = ks.index(3000)
        sl3 = 1.0 - math.exp(-kappa * Xm[i3])
        print("### P-X7 (il rallentamento uniforme in 3000 tick sotto il 10%% di 1 - N al centro): %+.4e / %.4e = %+.4f -> %s" % (sl3, a_c, sl3 / a_c, "VERA" if abs(sl3 / a_c) < 0.1 else "FALSA"))
        print("### IL SEGNO PER ANELLO a k 3000: %s" % ("POSITIVO: la condizione della 16:05 regge" if ok_segno else "NEGATIVO o MISTO: FERMO"))
    print("=" * 150)
    return 0


if __name__ == "__main__":
    sys.exit(main())
