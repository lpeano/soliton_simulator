# -*- coding: utf-8 -*-
r"""**T3, L'ULTIMA PROVA: (iii) L'AMPLIFICAZIONE ATTRAVERSO `e^2 rho`** *(Luca `2026-11-08` `20:57` e `21:49`, M4; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14.13`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3g.py > doc/referti_l2/u1_t3g.txt

### **La scena, lo stato e le righe di `u1_t3f`** *(`TBS` al tick `100000`, `e*` rifatto nello stesso ordine)*, **non compatto, norma piena.** **`G6` = `N_D` avanti, `T`, `N_D` avanti, `T`.**
**(0)** senza campo e col campo a `e*` coi due mezzi: **i numeri di `u1_t3f` alle cifre che quel referto stampa** *(qui stampati interi)*.
**(ii) NON si gira** *(Luca `21:49`: vuota per costruzione, i due mezzi sono uno dopo l'altro con lo stesso `E`; il task history sez. `14.13`)*.
**(iii)** `G6` a `e*`, `e* / 2`, `e* / 4`; **`D(e) = G6(e) - G6(senza)`** sull'assoluto di `psi`; **i due rapporti** e la classe *(`e^2`, lineare, piu' ripido, non scala)*.
**I controlli del classificatore:** `C-E2` *(DEVE PASSARE)*, `C-E1` *(DEVE FALLIRE)*. **`_u1_prototipo`, `_u1_oggi`, `u1_t3f` non si toccano.**
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
U1F = {"senza": 6.303e-12, "col": 5.266e-09}   # ### u1_t3f (d6' a norma x 1): l'assoluto di psi, alle cifre stampate
DIVISORI = (1, 2, 4)                            # ### Luca 20:57 (iii)
CLASSI = ((4.0 / 1.5, 4.0 * 1.5, "e^2"), (4.0 / 3.0, 4.0 / 1.5, "lineare"))   # ### sez. 14.13 (iii)
RUMORE_D = 2.0                                  # ### sez. 14.13: D sotto 2 volte G6(senza) non si legge
EPS = float(np.finfo(float).eps)
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-110s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:110], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def classe(r1, r2):
    """### la classe dei due rapporti `D(e) / D(e/2)`: la stessa per tutti e due, se no `non concludo`."""
    def una(r):
        for lo, hi, nome in CLASSI:
            if lo <= r < hi or (nome == "e^2" and r == hi):
                return nome
        if r > CLASSI[0][1]:
            return "piu' ripido di e^2"
        return "non scala con e"
    a, b = una(r1), una(r2)
    return a if a == b else "non concludo (%s, %s)" % (a, b)


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
    print("T3, (iii) (Luca 20:57 e 21:49): %s; N_D %d; i divisori di e* %s; la soglia assoluta %.3e" % (FILE_LIB, N_D, DIVISORI, tol))
    print("=" * 130)
    with UO.scena(E0_PROVA, "noncompatto") as (z, campo, K, s):
        st, mot, inc = z["st"], z["mot"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica(f=1.0):
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]
            if f != 1.0:
                st["psi_h"][...] = st["psi_h"] * math.sqrt(f)
                r = np.zeros(inc.n)
                np.add.at(r, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                st["rho"][...] = r

        def U_identita():
            UO.scrivi_U(mot, UO.campo_della_scena(z, 0.0, "noncompatto"))     # ### la cura del mio errore: U = I esatto
            assert float(np.max(np.abs(mot.geo.U - np.eye(2)[None]))) == 0.0

        def avanti(c, n, t0, ridotto, eA=None, eb=None):
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    if c is None:
                        AC.tick(z, t, K)
                        continue
                    c.spinta(0.5)
                    assert not ridotto, '(ii) non si gira (Luca 21:49)'
                    with U1.avvolto(mot, c, True):
                        AC.tick(z, t, K)
                    c.spinta(0.5)
                    if eA is not None:
                        eA[0] = max(eA[0], float(np.max(np.abs(c.e * c.A))))
                    if eb is not None:
                        eb[0] = max(eb[0], float(np.max(np.abs(c.e * c.B()))))

        def T_(c):
            if c is None:
                psi = st["psi_h"]
                psi[...] = np.conj(psi[:, ::-1]).copy()
                st["phi_h"][...] = np.conj(st["phi_h"]).copy()
            else:
                UO.rovescia(st, mot, c)

        def G6(c, n, ridotto):
            """dallo stato CORRENTE: (relativo, assoluto psi, assoluto phi, max|e A|)."""
            psi0, phi0 = st["psi_h"].copy(), st["phi_h"].copy()
            eA = [0.0]
            avanti(c, n, TICK0, ridotto, eA)
            T_(c)
            avanti(c, n, TICK0 + n, ridotto, eA)
            T_(c)
            return (max(U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"])),
                    float(np.max(np.abs(psi0 - st["psi_h"]))), float(np.max(np.abs(phi0 - st["phi_h"]))), eA[0])

        # ------------------------------------------------------------ (0), e*
        U_identita()
        carica()
        r0 = G6(None, N_D, False)
        print("  (0) SENZA il campo: relativo %.3e; assoluto psi %.3e phi %.3e" % r0[:3])
        eb0 = [0.0]
        carica()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        avanti(c0, N_D, TICK0, False, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("  e* = %g sqrt(%g / %.4e) = %.6e (come u1_t3b)" % (E0_PROVA, EB_MODERATO, eb0[0], e_star))
        # ------------------------------------------------------------ (0) e (iii): la norma piena, l'ordine delle righe di u1_t3f (d6', f = 1)
        U_identita()
        carica()
        senza = G6(None, N_D, False)
        print("  (0) senza campo, norma piena: assoluto psi %r (u1_t3f %.3e)" % (senza[1], U1F["senza"]))
        G = {}
        for d in DIVISORI:
            carica()
            G[d] = G6(UO.campo_della_scena(z, e_star / d, "noncompatto"), N_D, False)
            print("  (iii) e* / %d: assoluto psi %r; phi %.3e; relativo %.3e" % (d, G[d][1], G[d][2], G[d][0]))
            sys.stdout.flush()
    print("=" * 130)
    esito("(0) senza campo = u1_t3f alle cifre stampate", float("%.3e" % senza[1]) == U1F["senza"], "%.3e" % senza[1])
    esito("(0) col campo a e* coi due mezzi = u1_t3f alle cifre stampate", float("%.3e" % G[1][1]) == U1F["col"], "%.3e" % G[1][1])
    esito("C-E2 un D costruito come e^2 (rapporti 4, 4) classificato e^2", classe(4.0, 4.0) == "e^2", classe(4.0, 4.0))
    esito("C-E1 un D costruito come e (rapporti 2, 2) classificato e^2", classe(2.0, 2.0) == "e^2", classe(2.0, 2.0), deve=False)
    D = {d: G[d][1] - senza[1] for d in DIVISORI}
    print("  (iii) D(e*) %.3e, D(e*/2) %.3e, D(e*/4) %.3e; G6(senza) %.3e" % (D[1], D[2], D[4], senza[1]))
    if D[4] < RUMORE_D * senza[1]:
        let_iii = "NON RISOLTO: D(e*/4) sotto %g volte G6(senza)" % RUMORE_D
    else:
        r1, r2 = D[1] / D[2], D[2] / D[4]
        let_iii = "i rapporti %.3f e %.3f: %s" % (r1, r2, classe(r1, r2))
    print("  LA LETTURA (iii): %s" % let_iii)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
