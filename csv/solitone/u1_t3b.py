# -*- coding: utf-8 -*-
r"""**T3, LA DIAGNOSI E IL REGIME MODERATO** *(Luca `2026-11-08` `13:45`; il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `14`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3b.py > doc/referti_l2/u1_t3b.txt

### **d1, d2** *(sullo stato di `TBS` al tick `100000`, `e` = `E_PROVA`, le due forme)*: **per `N = 10, 30, 100`:** `G4` *(`chi` per nodo)*, **d1** *(`chi` UNIFORME, `A` invariato)*,
`G6` *(`N` avanti, `T`, `N` avanti, `T`)*; **la pendenza di `log(errore)` contro `t`, il tempo di e-fold, contro il caos `TAU = 35`** *(una LETTURA, non un DEVE)*.
### **U2, i DEVE nel regime MODERATO** *(le soglie della decisione `(1)`)*: **(m1)** lo stato di `TBS` a `e*` *(`e* = 0.1 sqrt(0.1 / max|0.1 B|)` da una corsa di prova non compatta di
`N_D` tick)*; **(m2)** lo stato piccolo dei sigilli del `24/10` *(il pacchetto di `_u1_prototipo.scena_materia`, `u_K(s)`, la norma `1`)* col vuoto di `TBS`, `e` = `E_PROVA`;
**`G2`, `G4`, `G4-F`, `G6`, `G6-F`.** **Nessun bordo.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TICK0 = 100000                 # ### TBS a t = 15000 (s = 0.15): la sez. 13.1
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
NN = (10, 30, 100)             # ### d2: Luca 13:45
TAU_CAOS = 35.0                # ### carta_coppia.TAU (Luca 2026-11-05 15:28): un e-fold ogni 35; la forchetta di Luca 25-40
FORCHETTA = (25.0, 40.0)
E0_PROVA = 0.1                 # ### la corsa di prova per e* (la sez. 14.1, premessa 3)
EB_MODERATO = 0.1              # ### Luca 13:45: max|e B| ~ 0.1
TOLL_U = 1e-12
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


def efold(N, err, s):
    """### `(tempo di e-fold, pendenza)` ai minimi quadrati di `log(err)` contro `t = N s` *(solo gli `err > 0`)*."""
    t = np.array([n * s for n, x in zip(N, err) if x > 0], dtype=float)
    y = np.log(np.array([x for x in err if x > 0], dtype=float))
    if len(t) < 2:
        return None, None
    p = np.polyfit(t, y, 1)[0]
    return (1.0 / p if p > 0 else float("inf")), p


def main():
    import _deriva_congelato as DC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _u1_prototipo as U1
    from solitone import _u1_oggi as UO
    from solitone import corsa_accensione as CA
    for m in ("__init__", "_u1_oggi", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    E_PROVA, AREA, TOLL_REL, N_B, N_D = U1.E_PROVA, U1.AREA, U1.TOLL_REL, U1.N_B, U1.N_D
    print("=" * 130)
    print("T3, LA DIAGNOSI (d1, d2) E IL REGIME MODERATO (Luca 13:45): lo stato %s; e %s; N %s; TAU del caos %g (la forchetta %s); N_B %d, N_D %d; nessun bordo"
          % (FILE_LIB, ["%.4f" % e for e in E_PROVA], NN, TAU_CAOS, FORCHETTA, N_B, N_D))
    print("=" * 130)
    with UO.scena(E_PROVA[0], "noncompatto") as (z, campo, K, s):
        st, inc, mot = z["st"], z["inc"], z["mot"]
        n_nodi, nodo, L = inc.n, inc.nodo, int(z["L"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica_tbs():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]

        def rho():
            r = np.zeros(n_nodi)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        # ### lo stato piccolo: il pacchetto di _u1_prototipo.scena_materia sulla scena di oggi, il vuoto di TBS
        v = np.arange(n_nodi)
        m1, m2 = v // L, v % L
        d1 = (m1 - L // 2 + L // 2) % L - L // 2
        d2 = (m2 - L // 2 + L // 2) % L - L // 2
        x, y = d1 - 0.5 * d2, d2 * math.sqrt(3.0) / 2.0
        g = np.exp(-(x * x + y * y) / (2.0 * U1.W_MAT * U1.W_MAT))
        cel = g[:, None] * U1.u_K(s)[None, :] * np.exp(2j * np.pi * (m1 + m2) / 3.0)[:, None]
        cel /= np.sqrt(np.sum(np.abs(cel) ** 2))
        psi_piccolo = cel.reshape(st["psi_h"].shape).copy()

        def carica_piccolo():
            carica_tbs()
            st["psi_h"][...] = psi_piccolo
            r = np.zeros(n_nodi)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            st["rho"][...] = r                                      # ### le cache per nodo rifatte dalla loro definizione (la scheda di CAMM-MATERIA-VUOTO)
            la = np.zeros(n_nodi)
            np.add.at(la, nodo, np.abs(st["phi_h"]) ** 2)
            st["Lambda"][...] = la

        def uscarto():
            U = mot.geo.U
            return float(np.max(np.abs(np.einsum("aji,ajk->aik", np.conj(U), U) - np.eye(2)[None])))

        def corri(c, n, t0=TICK0, g2=None, eb=None):
            a_, b_ = SF.forma(VC.FORMA), BE.conv(DC.ZERO)
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    UO.tick(z, t, K, c, True)
                    if g2 is not None:
                        g2[0] = max(g2[0], uscarto())
                    if eb is not None:
                        eb[0] = max(eb[0], float(np.max(np.abs(c.e * c.B()))))

        def gauge(carica, e, forma, N, modi, g2=None):
            """### `{modo: (rho, eB, |dE|, stima)}` contro la corsa di riferimento; `modo` in `chi`, `globale`, `solo_psi`."""
            rng = np.random.default_rng(U1.SEME_CHI)
            chi = rng.uniform(-math.pi, math.pi, n_nodi)
            carica()
            c1 = UO.campo_della_scena(z, e, forma)
            corri(c1, N, g2=g2)
            r1, E1, B1 = rho(), c1.E.copy(), c1.B().copy()
            out = {}
            for modo in modi:
                carica()
                c2 = UO.campo_della_scena(z, e, forma)
                ch = np.full(n_nodi, chi[0]) if modo == "globale" else chi
                st["psi_h"] *= np.exp(1j * ch[nodo])[:, None]
                if modo == "chi":
                    c2.A += (ch[c2.jj] - ch[c2.ii]) / e
                UO.scrivi_U(mot, c2)
                amax = float(np.max(np.abs(c2.A)))
                corri(c2, N, g2=g2)
                amax = max(amax, float(np.max(np.abs(c2.A))))
                out[modo] = (U1.rel(r1, rho()), U1.rel(e * B1, e * c2.B(), 2.0 * math.pi), float(np.max(np.abs(E1 - c2.E))), N * 6.0 * EPS * amax / AREA)   # ### la stima della decisione (1), come u1_t3
            return out

        def reversibile(carica, e, forma, N, con_A, g2=None, eb=None):
            carica()
            c = UO.campo_della_scena(z, e, forma)
            psi0, phi0, A0, E0 = st["psi_h"].copy(), st["phi_h"].copy(), c.A.copy(), c.E.copy()
            corri(c, N, g2=g2, eb=eb)
            a6, e6 = float(np.max(np.abs(c.A))), float(np.max(np.abs(c.E)))
            UO.rovescia(st, mot, c)
            if not con_A:
                c.A[...] = -c.A
                UO.scrivi_U(mot, c)
            corri(c, N, t0=TICK0 + N, g2=g2, eb=eb)
            UO.rovescia(st, mot, c)
            if not con_A:
                c.A[...] = -c.A
                UO.scrivi_U(mot, c)
            return (U1.rel(psi0, st["psi_h"]), U1.rel(phi0, st["phi_h"]), U1.rel(A0, c.A, a6) if a6 > 0 else 0.0, U1.rel(E0, c.E, e6) if e6 > 0 else 0.0)

        # ================================================================== d1, d2
        print("### d1, d2: lo stato di TBS; per N %s: G4 (chi per nodo), d1 (chi uniforme), G6 (N avanti, T, N avanti, T); t = N s per G4 e d1, 2 N s per G6" % (NN,))
        letture = []
        for forma in U1.FORME:
            for e in E_PROVA:
                g4, gl, g6 = [], [], []
                for N in NN:
                    gg = gauge(carica_tbs, e, forma, N, ("chi", "globale"))
                    rv = reversibile(carica_tbs, e, forma, N, True)
                    g4.append(gg["chi"][0])
                    gl.append(gg["globale"][0])
                    g6.append(rv[0])
                    print("  %-11s e %.4f N %3d (t %5.1f): G4 rho %.2e eB %.2e |dE| %.2e | d1 rho %.2e eB %.2e |dE| %.2e | G6 psi %.2e phi %.2e A %.2e E %.2e"
                          % (forma, e, N, N * s, gg["chi"][0], gg["chi"][1], gg["chi"][2], gg["globale"][0], gg["globale"][1], gg["globale"][2], rv[0], rv[1], rv[2], rv[3]))
                    sys.stdout.flush()
                f4, _p = efold(NN, g4, s)
                fl, _p = efold(NN, gl, s)
                f6, _p = efold([2 * n for n in NN], g6, s)
                f4b, _p = efold(NN[:2], g4[:2], s)
                letture.append((forma, e, f4, fl, f6, g4[0], gl[0]))
                print("  %-11s e %.4f: il tempo di e-fold (i tre N) G4 %s, d1 %s, G6 %s; G4 da N 10 a 30 soltanto %s; contro il caos %g"
                      % (forma, e, "%.2f" % f4 if f4 else "-", "%.2f" % fl if fl else "-", "%.2f" % f6 if f6 else "-", "%.2f" % f4b if f4b else "-", TAU_CAOS))
        print("### d2 LA LETTURA (Luca 13:45): (r1) e-fold fra %g e %g o piu' lento -> amplificazione sul caos; (r2) piu' veloce, o grande gia' a N 10 -> un difetto da cercare" % FORCHETTA)
        for forma, e, f4, fl, f6, g10, gl10 in letture:
            r = "(r1)" if (f4 is None or f4 >= FORCHETTA[0]) else "(r2)"
            print("  %-11s e %.4f: G4 e-fold %s -> %s; a N 10 G4 rho %.1e (%.0e volte eps), d1 rho %.1e; d1 %s" % (
                forma, e, "%.2f" % f4 if f4 else "-", r, g10, g10 / EPS, gl10, "cresce come G4 (lo STATO amplifica)" if gl10 > 1e3 * EPS else "all'arrotondamento (la parte LOCALE della gauge)"))
        sys.stdout.flush()

        # ================================================================== U2: il regime moderato
        eb0 = [0.0]
        carica_tbs()
        c0 = UO.campo_della_scena(z, E0_PROVA, "noncompatto")
        corri(c0, N_D, eb=eb0)
        e_star = E0_PROVA * math.sqrt(EB_MODERATO / eb0[0])
        print("### U2, IL REGIME MODERATO: la corsa di prova a e %g non compatto, %d tick: max|e B| %.4e -> e* = %g sqrt(%g / %.4e) = %.6e (scelta di protocollo, Luca 13:45)"
              % (E0_PROVA, N_D, eb0[0], E0_PROVA, EB_MODERATO, eb0[0], e_star))
        casi = [("m1 TBS", carica_tbs, forma, e_star, True) for forma in U1.FORME] + \
               [("m2 piccolo", carica_piccolo, forma, e, e == E_PROVA[1]) for forma in U1.FORME for e in E_PROVA]
        righe = []
        for nome, car, forma, e, fa in casi:
            g2, eb = [0.0], [0.0]
            gg = gauge(car, e, forma, N_B, ("chi", "solo_psi") if fa else ("chi",), g2=g2)
            rv = reversibile(car, e, forma, N_D, True, g2=g2, eb=eb)
            rvF = reversibile(car, e, forma, N_D, False) if fa else None
            g = gg["chi"]
            r = {"nome": nome, "forma": forma, "e": e, "G4": g[0] <= TOLL_REL and g[1] <= TOLL_REL and g[2] <= g[3], "g4": g, "g6": rv, "G2": g2[0], "eB": eb[0],
                 "G4-F": gg["solo_psi"][0] if fa else None, "G6-F": max(rvF) if fa else None}
            righe.append(r)
            print("  %-10s %-11s e %.6f | G4 rho %.2e eB %.2e |dE| %.2e stima %.2e (%.3f) | G6 psi %.2e phi %.2e A %.2e E %.2e | max|e B| %.3e | G2 %.1e%s"
                  % (nome, forma, e, g[0], g[1], g[2], g[3], g[2] / g[3], rv[0], rv[1], rv[2], rv[3], eb[0], g2[0],
                     " | G4-F rho %.2e, G6-F %.2e" % (r["G4-F"], r["G6-F"]) if fa else ""))
            sys.stdout.flush()
    tol6 = 2 * N_D * 6.0 * EPS
    print("=" * 130)
    esito("DEVE PASSARE: U2-G2 |U^dag U - I| <= %g a ogni tick, ogni configurazione del regime moderato" % TOLL_U, all(r["G2"] <= TOLL_U for r in righe), "il massimo %.2e" % max(r["G2"] for r in righe))
    esito("DEVE PASSARE: U2-G4 la gauge nel regime moderato (m1 TBS a e*, m2 lo stato piccolo): rho, eB <= %g, |dE| <= la stima, ogni configurazione" % TOLL_REL, all(r["G4"] for r in righe),
          "rho max %.1e, eB max %.1e, |dE|/stima max %.3f" % (max(r["g4"][0] for r in righe), max(r["g4"][1] for r in righe), max(r["g4"][2] / r["g4"][3] for r in righe)))
    esito("DEVE FALLIRE: U2-G4-F chi solo su psi: rho <= %g" % TOLL_REL, all(r["G4-F"] > TOLL_REL for r in righe if r["G4-F"] is not None), "rho min %.2e" % min(r["G4-F"] for r in righe if r["G4-F"] is not None))
    esito("DEVE PASSARE: U2-G6 %d avanti, T, %d avanti, T nel regime moderato: entro N 6 eps = %.2e (N = %d), ogni configurazione" % (N_D, N_D, tol6, 2 * N_D),
          all(max(r["g6"]) <= tol6 for r in righe), "il peggiore %.2e" % max(max(r["g6"]) for r in righe))
    esito("DEVE FALLIRE: U2-G6-F senza A -> -A: entro %.2e" % tol6, all(r["G6-F"] > tol6 for r in righe if r["G6-F"] is not None), "il migliore %.2e" % min(r["G6-F"] for r in righe if r["G6-F"] is not None))
    print("  registrato: max|e B| nelle corse a e* %s (atteso ~%g)" % (["%.3e" % r["eB"] for r in righe if r["nome"].startswith("m1")], EB_MODERATO))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
