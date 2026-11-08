# -*- coding: utf-8 -*-
r"""**T3, d5 E d6: LA SORGENTE SPENTA E LA NORMA RISCALATA** *(Luca `2026-11-08` `16:40`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14.7`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3d.py > doc/referti_l2/u1_t3d.txt

### **La scena e lo stato di `u1_t3c`**; **`G6`** *(`N_D` avanti, `T`, `N_D` avanti, `T`)*: **(0) senza campo; (1) col campo a `e*` e la sorgente; (d5) col campo a `e*` e la SORGENTE
SPENTA; (d6) col campo e la sorgente, `psi -> sqrt(f) psi`, `f = 1e-3, 1e-1`** *(le cache `rho` rifatte)*. **Le letture di Luca:** **(d5) `~1e-12` -> la sorgente; (d6) lo scarto scala
con la norma** *(la pendenza di `log` contro `log f` fra `0.5` e `1.5`, mia)* **-> l'arrotondamento di `J`.** **Una sola forma** *(non compatto: `u1_t3c` le ha date uguali)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TICK0 = 100000
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
E0_PROVA = 0.1
EB_MODERATO = 0.1
F_NORMA = (1e-3, 1e-1, 1.0)    # ### Luca 16:40: per esempio x1e-3 e x1e-1
PENDENZA = (0.5, 1.5)          # ### mia, dichiarata: "scala con la norma" = lineare in rho
VICINO = 10.0                  # ### come u1_t3c: entro 10 volte la soglia assoluta
EPS = float(np.finfo(float).eps)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che[:118], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main():
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _u1_prototipo as U1
    from solitone import _u1_oggi as UO
    from solitone import accensione as AC
    for m in ("__init__", "_u1_oggi", "accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    N_D = U1.N_D
    tol = 2 * N_D * 6.0 * EPS
    print("=" * 130)
    print("T3, d5 E d6: LA SORGENTE SPENTA E LA NORMA RISCALATA (Luca 16:40): %s; N_D %d; le norme %s; la soglia assoluta %.3e" % (FILE_LIB, N_D, F_NORMA, tol))
    print("=" * 130)
    with UO.scena(E0_PROVA, "noncompatto") as (z, campo, K, s):
        st, mot = z["st"], z["mot"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]

        def avanti(c, n, t0, eb=None):
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    if c is None:
                        AC.tick(z, t, K)
                    else:
                        UO.tick(z, t, K, c, True)
                        if eb is not None:
                            eb[0] = max(eb[0], float(np.max(np.abs(c.e * c.B()))))

        def T_senza():
            psi = st["psi_h"]
            psi[...] = np.conj(psi[:, ::-1]).copy()
            st["phi_h"][...] = np.conj(st["phi_h"]).copy()

        def T_con(c, con_A):
            UO.rovescia(st, mot, c)
            if not con_A:
                c.A[...] = -c.A
                UO.scrivi_U(mot, c)

        def G6(c, con_A):
            carica()
            psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
            avanti(c, N_D, TICK0)
            if c is None:
                T_senza()
            else:
                T_con(c, con_A)
            avanti(c, N_D, TICK0 + N_D)
            if c is None:
                T_senza()
            else:
                T_con(c, con_A)
            return max(U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"]))

        def scala(f):
            carica()
            st["psi_h"][...] = st["psi_h"] * math.sqrt(f)
            r = np.zeros(z["inc"].n)
            np.add.at(r, z["inc"].nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            st["rho"][...] = r

        def G6s(c, sorgente, f):
            if f == 1.0:
                carica()
            else:
                scala(f)
            psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(TICK0 + 1, TICK0 + N_D + 1):
                    if c is None:
                        AC.tick(z, t, K)
                    else:
                        UO.tick(z, t, K, c, sorgente)
            if c is None:
                T_senza()
            else:
                T_con(c, True)
            with a_, b_:
                for t in range(TICK0 + N_D + 1, TICK0 + 2 * N_D + 1):
                    if c is None:
                        AC.tick(z, t, K)
                    else:
                        UO.tick(z, t, K, c, sorgente)
            if c is None:
                T_senza()
            else:
                T_con(c, True)
            return max(U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"]))

        UO.scrivi_U(mot, UO.campo_della_scena(z, 0.0, "noncompatto"))
        r0 = G6s(None, True, 1.0)
        print("  (0) SENZA il campo: %.3e (la soglia assoluta %.3e)" % (r0, tol))
        eb0 = [0.0]
        carica()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        avanti(c0, N_D, TICK0, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("  e* = %g sqrt(%g / %.4e) = %.6e (come u1_t3b)" % (E0_PROVA, EB_MODERATO, eb0[0], e_star))
        r1 = G6s(UO.campo_della_scena(z, e_star, "noncompatto"), True, 1.0)
        print("  (1) col campo e la sorgente: %.3e (%.1f volte (0))" % (r1, r1 / r0))
        r5 = G6s(UO.campo_della_scena(z, e_star, "noncompatto"), False, 1.0)
        print("  (d5) col campo e la SORGENTE SPENTA: %.3e (%.1f volte (0))" % (r5, r5 / r0))
        r6 = {}
        for f in F_NORMA:
            r6[f] = r1 if f == 1.0 else G6s(UO.campo_della_scena(z, e_star, "noncompatto"), True, f)
            r6z = G6s(None, True, f) if f != 1.0 else r0
            print("  (d6) la norma x %g: col campo %.3e, senza campo %.3e" % (f, r6[f], r6z))
            sys.stdout.flush()
        lf = np.log10(np.array(F_NORMA))
        pend = float(np.polyfit(lf, np.log10(np.array([r6[f] for f in F_NORMA])), 1)[0])
        print("  (d6) la pendenza di log10(scarto) contro log10(f): %.3f (fra %g e %g: scala con la norma)" % (pend, PENDENZA[0], PENDENZA[1]))
    print("=" * 130)
    l5 = r5 <= VICINO * tol
    l6 = PENDENZA[0] <= pend <= PENDENZA[1]
    print("  LA LETTURA (Luca 16:40): (d5) %s; (d6) %s" % ("la sorgente: senza, G6 torna vicino alla soglia" if l5 else "NON la sorgente sola: senza, G6 resta lontano",
                                                     "lo scarto SCALA con la norma: l'arrotondamento di J" if l6 else "lo scarto NON scala con la norma"))
    esito("DEVE PASSARE: d5 senza la sorgente G6 su TBS col campo e' vicino alla soglia (entro %g x %.2e)" % (VICINO, tol), l5, "%.3e" % r5)
    esito("DEVE PASSARE: d6 lo scarto col campo scala con la norma (la pendenza fra %g e %g)" % PENDENZA, l6, "%.3f" % pend)
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
