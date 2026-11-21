# -*- coding: utf-8 -*-
r"""**IL CAMPO CHI CON LA MASSA (PORTATA `100` NODI) E LO SFONDO FISSO: IL PROFILO STATICO, `kappa`, LA DERIVA, IL CRITERIO DEL SEGNO** *(la decisione di Luca `2026-11-21` `16:39`; il task history `doc/TASK_HISTORY/2026-11-21_lapse_u.md` del ramo `lapse-u`, sez. `8`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/chi_massa.py > doc/referti_l2/chi_massa.txt

**Solo lettura.** `u = s Q - e0 rho` *(`chi_segno.Q_di`, `cs = s`)*; `m0` = la media a `k 0` di C2 *(`controllo_senza_bordo.prepara`)*; **con la massa:** `psi_m = (c_chi^2 L + m^2)^{-1} (u - m0)`, `m = 1/100`; **senza:** `psi_0 = L^+ (u - media u) / c_chi^2`; **`kappa`** da `kappa^2 psi_m,c = - ln(1 - a)` a C2 `k 3000`; `1 - N = 1 - exp(- kappa^2 psi)`.
**IL CRITERIO NUOVO** *(sez. `8.3`)*: `1 - N > 0` su ogni nodo con `r < 25`, e la media per anello che NON cresce dall'anello `24` all'`80`, a `k 3000`, `15000`, `29000`. **LA DERIVA** *(quasi statica)*: `1 - exp(- kappa^2 (media u - m0) / m^2)` sugli stati ogni `250` tick fino a `29000`, e a `1e5` per estrapolazione lineare *(dichiarata)*.
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
import chi_segno as CSG            # ### usato, non riscritto: Q_di, rho_di, anello, C_CHI
import chi_sfondo as CSF           # ### usato, non riscritto: file_di, carica, K_FINE

PORTATA = 100.0
M2 = (1.0 / PORTATA) ** 2
STATI_K = (3000, 15000, 29000)
ANELLI = list(range(0, 31, 2)) + list(range(35, 81, 5))


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
    c2 = CSG.C_CHI ** 2
    print("=" * 150)
    print("IL CAMPO CHI CON LA MASSA (la portata %.0f nodi, m^2 %.1e) E LO SFONDO FISSO (Luca 2026-11-21 16:39; il task history del ramo lapse-u, sez. 8)" % (PORTATA, M2))
    print("=" * 150)
    with CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        mot = Z["mot"]
        n, s = mot.inc.n, float(Z["s"])
        ii, jj = np.asarray(mot.inc.ii, dtype=np.int64), np.asarray(mot.inc.jj, dtype=np.int64)
        m = len(ii)
        a_ = np.arange(m)
        D = sp.csr_matrix((np.concatenate([np.ones(m), -np.ones(m)]), (np.concatenate([jj, ii]), np.concatenate([a_, a_]))), shape=(n, m))
        Lap = (D @ D.T).tocsc()
        risolvi_m = spl.factorized((c2 * Lap + M2 * sp.identity(n, format="csc")).tocsc())
        risolvi_0 = spl.factorized(Lap[1:, 1:])

        def u_di():
            Q, _H = CSG.Q_di(Z, s)
            rho = CSG.rho_di(Z)
            return s * Q - e0 * rho, rho

        # -------------------------------------------------------- il caso noto: il vuoto -> chi = 0 al bit
        MT.vuoto_fresco(Z, t0)
        uv, _ = u_di()
        pv = risolvi_m(uv - uv.mean())
        print("### IL CASO NOTO (il vuoto uniforme, la sorgente meno la sua media): psi_m max |%.3e| -> %s" % (float(np.max(np.abs(pv))), "ZERO AL BIT" if np.all(pv == 0.0) else "NON zero al bit"))
        CSB.prepara(Z, 186, False, rho_c, e, t0)
        u0, _ = u_di()
        m0 = float(u0.mean())
        print("### m0 (la media di u a k 0 di C2) %+.12e" % m0)
        # -------------------------------------------------------- i tre stati: i profili, kappa, il criterio
        kappa = None
        crit = {}
        for k in STATI_K:
            meta = CSF.carica(Z, CSF.file_di(k))
            u, rho = u_di()
            c = [float(x) for x in meta["centro"]]
            r = np.hypot(*TO.scarti(Z["m1"], Z["m2"], c[0], c[1], Z["L"]).T[:2])
            c0n = int(np.argmin(r))
            pm = risolvi_m(u - m0)
            p0 = np.zeros(n)
            p0[1:] = risolvi_0((u - u.mean())[1:])
            p0 = (p0 - p0.mean()) / c2
            if kappa is None:
                a = 1.0 - 1.0 / (1.0 + rho[c0n] / rho_c)
                kappa = math.sqrt(-math.log(1.0 - a) / pm[c0n]) if pm[c0n] > 0 else None
                print("### KAPPA (UNA volta, C2 k 3000): a %.10e, psi_m al centro %+.6e -> kappa %s (DERIVATO); c0 = kappa m0 = %s" % (
                    a, pm[c0n], "%.10e" % kappa if kappa else "NON DEFINITO", "%+.10e" % (kappa * m0) if kappa else "-"))
                a_c = a
                if kappa is None:
                    return 1
            uM = 1.0 - np.exp(-kappa ** 2 * pm)
            u0_ = 1.0 - np.exp(-kappa ** 2 * p0)
            prof = [CSG.anello(r, uM, R) for R in range(24, 81)]
            dentro = bool(np.all(uM[r < 25.0] > 0.0))
            cresce = [R for R, (x, y) in zip(range(25, 81), zip(prof[:-1], prof[1:])) if y > x]
            ok = dentro and not cresce
            crit[k] = ok
            print("-" * 150)
            print("### k %d (il centro, il nodo %d): il profilo statico, 1 - N con la massa e senza (lo stesso kappa); accanto 1 - N(rho)" % (k, c0n))
            print("      r     1 - N (massa)     1 - N (senza)      1 - N(rho)")
            for R in ANELLI:
                if R == 0:
                    print("    %3d   %13.6e   %13.6e   %13.6e" % (R, uM[c0n], u0_[c0n], 1.0 - 1.0 / (1.0 + rho[c0n] / rho_c)))
                else:
                    print("    %3d   %13.6e   %13.6e   %13.6e" % (R, CSG.anello(r, uM, R), CSG.anello(r, u0_, R), CSG.anello(r, 1.0 - 1.0 / (1.0 + rho / rho_c), R)))
            print("    all'anello 60 sul centro: con la massa %.4f, senza %.4f" % (CSG.anello(r, uM, 60) / uM[c0n], CSG.anello(r, u0_, 60) / u0_[c0n]))
            print("    ### IL CRITERIO NUOVO: 1 - N > 0 su ogni nodo con r < 25: %s (il minimo %+.6e); la media per anello non cresce dall'anello 24 all'80: %s -> %s" % (
                dentro, float(uM[r < 25.0].min()), "SI'" if not cresce else "NO, cresce agli anelli %s" % cresce, "PASSA" if ok else "NON PASSA"))
            print("    ### P-X9 (1 - N all'anello 60 sopra il 3%% del centro, con la massa): %.4f -> %s" % (CSG.anello(r, uM, 60) / uM[c0n], "VERA" if CSG.anello(r, uM, 60) / uM[c0n] > 0.03 else "FALSA"))
        # -------------------------------------------------------- la deriva con la massa
        ks = list(range(250, CSF.K_FINE + 1, 250))
        dm = []
        for k in ks:
            CSF.carica(Z, CSF.file_di(k))
            u, _ = u_di()
            dm.append(float(u.mean()) - m0)
        dm = np.array(dm)
        K = np.array(ks, dtype=float)
        rall = 1.0 - np.exp(-kappa ** 2 * dm / M2)
        sel = K >= 3000
        b1, b0 = np.polyfit(K[sel], dm[sel], 1)
        d5 = b0 + b1 * 1e5
        r5 = 1.0 - math.exp(-kappa ** 2 * d5 / M2)
        print("-" * 150)
        print("### LA DERIVA CON LA MASSA (quasi statica): media chi = kappa (media u - m0) / m^2; il rallentamento uniforme 1 - exp(-kappa^2 (media u - m0) / m^2)")
        for k in (250, 1000, 3000, 5000, 10000, 15000, 20000, 25000, 29000):
            i = ks.index(k)
            print("    k %6d   media u - m0 %+.6e   il rallentamento %+.6e   sul centro %+.4e" % (k, dm[i], rall[i], rall[i] / a_c))
        mx = float(np.max(np.abs(rall))) / a_c
        print("    l'estrapolazione LINEARE a 1e5 (il fit da k 3000 a 29000: %+.4e + %+.4e k): media u - m0 %+.6e, il rallentamento %+.6e, sul centro %+.4e" % (b0, b1, d5, r5, r5 / a_c))
        print("### P-X8 (la deriva sotto l'1%% del centro a ogni tempo): il massimo sugli stati %.4e, a 1e5 %.4e -> %s" % (mx, abs(r5) / a_c, "VERA" if mx < 0.01 and abs(r5) / a_c < 0.01 else "FALSA"))
        print("### P-X10 (il criterio nuovo a k 3000, 15000, 29000): %s -> %s" % (crit, "VERA" if all(crit.values()) else "FALSA"))
    print("=" * 150)
    return 0


if __name__ == "__main__":
    sys.exit(main())
