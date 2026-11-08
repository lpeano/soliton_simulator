# -*- coding: utf-8 -*-
r"""**T3, d4: LA REVERSIBILITA' SULLO STATO DI `TBS` SENZA IL CAMPO, IL BRACCIO DI CONTROLLO** *(Luca `2026-11-08` `14:39`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14.5`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3c.py > doc/referti_l2/u1_t3c.txt

### **La scena e lo stato di `u1_t3b`** *(`_u1_oggi.scena`, `TBS` al tick `100000`, nessun bordo)*: **(0) senza il campo** *(il tick di oggi, `T` = `psi -> sigma_x psi*`, `phi -> phi*`)*,
**`N_D` avanti, `T`, `N_D` avanti, `T`**; **(1) col campo a `e*`** *(`e* = 0.1 sqrt(0.1 / max|0.1 B|)`, rifatto come in `u1_t3b`)* **nelle due forme.** ### **Le letture di Luca:** **(m1) (0) `~2.5e-10`:
la materia caotica; (m2) (0) vicino alla soglia assoluta: la `U(1)` aggiunge irreversibilita'.** ### **Il criterio se (m1)** *(Luca, dichiarato: dopo i numeri, ancorato al braccio di controllo)*:
**`G6-C` (1) / (0) `<= 2` nelle due forme.** **DEVE FALLIRE `G6-C-F`:** lo stesso rapporto con (1) senza `A -> -A`.
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
FATTORE = 2.0                  # ### Luca 14:39: il criterio del braccio di controllo
VICINO = 10.0                  # ### la lettura (m2): (0) entro 10 volte la soglia assoluta N 6 eps (il "vicino" di Luca, reso un numero da me: dichiarato)
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
    print("T3, d4: G6 SULLO STATO DI TBS SENZA IL CAMPO (il braccio di controllo) E COL CAMPO A e* (Luca 14:39): %s; N_D %d; il criterio (1)/(0) <= %g; la soglia assoluta %.3e"
          % (FILE_LIB, N_D, FATTORE, tol))
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

        # ------------------------------------------------------------ (0) senza il campo
        UO.scrivi_U(mot, UO.campo_della_scena(z, 0.0, "noncompatto"))     # ### U = I esatto (A = 0, e = 0)
        r0 = G6(None, True)
        print("  (0) SENZA il campo (U = I): %d avanti, T, %d avanti, T: max(psi, phi) relativo %.3e (la soglia assoluta %.3e)" % (N_D, N_D, r0, tol))
        lettura = "(m2)" if r0 <= VICINO * tol else "(m1)"
        print("  LA LETTURA (Luca 14:39): %s -- %s" % (lettura, "la U(1) aggiunge irreversibilita': FERMO" if lettura == "(m2)" else "la materia caotica amplifica l'arrotondamento"))
        # ------------------------------------------------------------ e*, poi (1) col campo
        eb0 = [0.0]
        carica()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        avanti(c0, N_D, TICK0, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("  e* = %g sqrt(%g / %.4e) = %.6e (come u1_t3b)" % (E0_PROVA, EB_MODERATO, eb0[0], e_star))
        r1, r1f = {}, {}
        for forma in U1.FORME:
            r1[forma] = G6(UO.campo_della_scena(z, e_star, forma), True)
            r1f[forma] = G6(UO.campo_della_scena(z, e_star, forma), False)
            print("  (1) %-11s e* %.6e: G6 %.3e (rapporto a (0) %.3f); senza A -> -A %.3e" % (forma, e_star, r1[forma], r1[forma] / r0, r1f[forma]))
            sys.stdout.flush()
    print("=" * 130)
    esito("DEVE PASSARE: d4 la lettura e' (m1): senza il campo l'errore NON e' vicino alla soglia assoluta (> %g x %.2e)" % (VICINO, tol), lettura == "(m1)", "%.3e" % r0)
    esito("DEVE PASSARE: G6-C su TBS: (1) col campo a e* / (0) senza <= %g, nelle due forme (il criterio di Luca 14:39)" % FATTORE, all(r1[f] / r0 <= FATTORE for f in r1),
          "%s" % {f: "%.3f" % (r1[f] / r0) for f in r1})
    esito("DEVE FALLIRE: G6-C-F lo stesso rapporto senza A -> -A: <= %g" % FATTORE, all(r1f[f] / r0 > FATTORE for f in r1f), "%s" % {f: "%.2e" % (r1f[f] / r0) for f in r1f})
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
