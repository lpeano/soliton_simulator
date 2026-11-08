# -*- coding: utf-8 -*-
r"""**T3: I DEVE DI BASE DELL'INNESTO `U(1)` SUL TICK DI OGGI** *(il task history `doc/TASK_HISTORY/2026-11-07_u1_prototipo_verificato.md`, sez. `2` e `13`)*. [[U1-PROTOTIPO-TRIANGOLI]]

    python csv/solitone/u1_t3.py > doc/referti_l2/u1_t3.txt

### **La scena:** `_u1_oggi.scena(e, forma)` *(la costruzione della corsa)* **con lo stato di `TBS` a `t = 15000`** *(il tick `100000`, `E:\soliton_simulator\libreria\TBS_100000_completo.npz`)*,
**SENZA il bordo** *(non e' parte del tick; toglierebbe carica senza corrente)*. **`e` = `_u1_prototipo.E_PROVA`, `forma` = `compatto`, `noncompatto`:** il verdetto vale in TUTTE.
### **`G0` PER PRIMO** *(se fallisce lo script si ferma)*: **(i)** la scena di `_u1_oggi` col campo scritto *(`U = I`)* e il tick NON avvolto = la scena costruita come la corsa, AL BIT;
**(ii)** il campo acceso a `e = 0` *(non compatto: a `e = 0` il compatto e' `0/0`)* = (i) sulla materia AL BIT; **`G0-F`** `e = 0.1`: la materia cambia. **`G2`** `|U^dag U - I|` a ogni tick,
**`G2-F`** `U (1 + 1e-6)`. **`G4`** la gauge *(la decisione `(1)`)*, **`G4-F`** `chi` solo su `psi`. **`G5`** Gauss, **`G5-F`** la sorgente spenta *(per la chiave giusta)*.
**`G6`** `N_D` avanti, `T`, `N_D` avanti, `T`; **`G6-F`** senza `A -> -A`. **`D6`** il tick col campo commuta con `R180 x sigma_z` *(la rotazione di `carta_d0`; un arco ruotato e'
ROVESCIATO: `A`, `E` cambiano segno)*; **`D6-F`** lo stesso con `U = 1`. ### **I DEVE FALLIRE a `e = 0.3029`, nelle due forme.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TICK0 = 100000                 # ### TBS a t = 15000 (s = 0.15): la sez. 13.1 del task history
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
IMPRONTA = "2e7f795d2a52fbe7"  # ### composizione.IMPRONTA, la sez. 2
TOLL_U = 1e-12                 # ### G2, la sez. 2 (la verifica di motore.Geometria)
MODULO_F = 1e-6                # ### G2-F, la sez. 2
N_D6 = 10                      # ### D6: il N_TICK di carta_d0
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
    import _vuoto_vivo_B as V
    import composizione as CM
    from solitone import _u1_oggi as UO
    from solitone import accensione as AC
    from solitone import carta_impulso as CI
    from solitone import corsa_accensione as CA
    for m in ("__init__", "_u1_oggi", "accensione", "carta_impulso", "corsa_accensione"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(os.path.join(os.path.dirname(_QUI), "_u1_prototipo.py"))
    _presidio.avvia(__file__)
    N_B, N_C, N_D, E_PROVA, AREA, TOLL_REL, TOLL_ROTTA = U1.N_B, U1.N_C, U1.N_D, U1.E_PROVA, U1.AREA, U1.TOLL_REL, U1.TOLL_ROTTA
    e_f = E_PROVA[1]
    print("=" * 130)
    print("T3, I DEVE DI BASE DELL'INNESTO U(1) SUL TICK DI OGGI: la scena di _u1_oggi, lo stato %s (tick %d); e %s; forme %s; N_B %d, N_C %d, N_D %d, N_D6 %d; nessun bordo"
          % (FILE_LIB, TICK0, ["%.4f" % e for e in E_PROVA], U1.FORME, N_B, N_C, N_D, N_D6))
    print("  l'impronta della composizione: %s (attesa %s)" % (CM.IMPRONTA, IMPRONTA))
    print("=" * 130)
    esito("DEVE PASSARE: G0-I l'impronta della composizione e' quella della sez. 2", CM.IMPRONTA == IMPRONTA, CM.IMPRONTA)

    def con_forma():
        return SF.forma(VC.FORMA), BE.conv(DC.ZERO)

    # ------------------------------------------------------------------ G0 (i): la scena della corsa, il riferimento
    sol, vuoto, s = V.CORSE[CA.NOME]
    K = int(round(CA.CORSE["TBS"][0] / s))
    with V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        import _dove_va_la_materia as DV
        from solitone import protetto as P
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        for k, v in salvato.items():
            z["st"][k][...] = v
        chiavi = sorted(k for k, v in z["st"].items() if isinstance(v, np.ndarray))
        with np.load(FILE_LIB) as d:
            assert int(d["t"]) == TICK0
            for k in chiavi:
                z["st"][k][...] = d[k]
        a_, b_ = con_forma()
        with a_, b_:
            for t in range(TICK0 + 1, TICK0 + N_B + 1):
                AC.tick(z, t, K)
        rif = V.shas(z)
    print("  G0 il riferimento: la scena della corsa, %d tick da %d: %d chiavi" % (N_B, TICK0, len(rif)))

    with UO.scena(E_PROVA[0], "noncompatto") as (z, campo, K2, _s):
        assert K2 == K, (K2, K)
        st, inc, mot = z["st"], z["inc"], z["mot"]
        n_nodi, nodo = inc.n, inc.nodo

        def carica():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]

        def rho():
            r = np.zeros(n_nodi)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return r

        def uscarto():
            U = mot.geo.U
            return float(np.max(np.abs(np.einsum("aji,ajk->aik", np.conj(U), U) - np.eye(2)[None])))

        def corri(c, n, sorgente=True, t0=TICK0, g2=None):
            a_, b_ = con_forma()
            with a_, b_:
                for t in range(t0 + 1, t0 + n + 1):
                    UO.tick(z, t, K, c, sorgente)
                    if g2 is not None:
                        g2[0] = max(g2[0], uscarto())

        def nuovo(e, forma):
            c = UO.campo_della_scena(z, e, forma)
            return c

        # ------------------------------------------------------------------ G0 (i), (ii), G0-F
        carica()
        c0 = nuovo(E_PROVA[0], "noncompatto")
        a_, b_ = con_forma()
        with a_, b_:
            for t in range(TICK0 + 1, TICK0 + N_B + 1):
                AC.tick(z, t, K)
        sh = V.shas(z)
        div_i = sorted(k for k in rif if sh.get(k) != rif[k])
        if not esito("DEVE PASSARE: G0 (i) la scena di _u1_oggi col campo scritto (U = I), il tick NON avvolto, %d tick = la scena della corsa AL BIT (ogni chiave)" % N_B,
                     not div_i, "diverse %s" % div_i):
            return fine()
        carica()
        c0 = nuovo(0.0, "noncompatto")
        corri(c0, N_B)
        sh = V.shas(z)
        div_ii = sorted(k for k in rif if sh.get(k) != rif[k])
        if not esito("DEVE PASSARE: G0 (ii) il campo ACCESO a e = 0 (non compatto), il tick avvolto con la sorgente, %d tick: la materia AL BIT del riferimento" % N_B,
                     not div_ii, "diverse %s; max|A| %.1e max|E| %.1e" % (div_ii, float(np.max(np.abs(c0.A))), float(np.max(np.abs(c0.E))))):
            return fine()
        carica()
        c0 = nuovo(E_PROVA[0], "noncompatto")
        corri(c0, N_B)
        sh = V.shas(z)
        div_f = sorted(k for k in rif if sh.get(k) != rif[k])
        esito("DEVE FALLIRE: G0-F e = %.4f: la materia AL BIT del riferimento" % E_PROVA[0], bool(div_f),
              "diverse %s; max|A| %.1e max|E| %.1e" % (div_f, float(np.max(np.abs(c0.A))), float(np.max(np.abs(c0.E)))))

        # ------------------------------------------------------------------ G2-F: il controllo sa fallire
        carica()
        c0 = nuovo(e_f, "compatto")
        U_salva = mot.geo.U.copy()
        mot.geo.U[...] = mot.geo.U * (1.0 + MODULO_F)
        uf = uscarto()
        mot.geo.U[...] = U_salva
        esito("DEVE FALLIRE: G2-F U scritta con un modulo 1 + %g: |U^dag U - I| <= %g" % (MODULO_F, TOLL_U), not uf <= TOLL_U, "%.3e" % uf)

        righe = []
        for forma in U1.FORME:
            for e in E_PROVA:
                fa = e == e_f
                r = {"forma": forma, "e": e}
                g2 = [0.0]
                # -------------------------------------------------- G4: la gauge
                rng = np.random.default_rng(U1.SEME_CHI)
                chi = rng.uniform(-math.pi, math.pi, n_nodi)
                carica()
                c1 = nuovo(e, forma)
                corri(c1, N_B, g2=g2)
                rho1, E1, B1 = rho(), c1.E.copy(), c1.B().copy()
                prove = (("chi", True),) + ((("solo_psi", False),) if fa else ())
                for modo, con_A in prove:
                    carica()
                    c2 = nuovo(e, forma)
                    st["psi_h"] *= np.exp(1j * chi[nodo])[:, None]
                    if con_A:
                        c2.A += (chi[c2.jj] - chi[c2.ii]) / e
                    UO.scrivi_U(mot, c2)
                    amax = float(np.max(np.abs(c2.A)))
                    corri(c2, N_B, g2=g2)
                    amax = max(amax, float(np.max(np.abs(c2.A))))
                    r_rho = U1.rel(rho1, rho())
                    r_eB = U1.rel(e * B1, e * c2.B(), 2.0 * math.pi)
                    dE = float(np.max(np.abs(E1 - c2.E)))
                    stima = N_B * 6.0 * EPS * amax / AREA
                    r[modo] = (r_rho, r_eB, dE, stima)
                g = r["chi"]
                r["G4"] = g[0] <= TOLL_REL and g[1] <= TOLL_REL and g[2] <= g[3]
                if fa:
                    r["G4-F"] = r["solo_psi"][0]
                # -------------------------------------------------- G5: Gauss
                for sorgente in ((True, False) if fa else (True,)):
                    carica()
                    c5 = nuovo(e, forma)
                    rho0 = rho()
                    G0 = c5.div() - e * (rho0 - rho0.mean())
                    peg, chiave, emax, drho = 0.0, 0.0, 0.0, 0.0
                    a_, b_ = con_forma()
                    with a_, b_:
                        for t in range(TICK0 + 1, TICK0 + N_C + 1):
                            UO.tick(z, t, K, c5, sorgente)
                            g2[0] = max(g2[0], uscarto())
                            rr = rho()
                            G = c5.div() - e * (rr - rr.mean())
                            peg = max(peg, float(np.max(np.abs(G - G0))))
                            chiave = max(chiave, float(np.max(np.abs((G - G0) + e * (rr - rho0)))))
                            emax = max(emax, float(np.max(np.abs(c5.E))))
                            drho = max(drho, float(np.max(np.abs(rr - rho0))))
                    r["G5" if sorgente else "G5-F"] = (peg, N_C * 6.0 * EPS * max(emax, e * float(np.max(rho0))), chiave, emax, drho, e * float(np.max(rho0)))   # ### la scala: max(max|E|, e max rho) -- la sez. 13.4
                # -------------------------------------------------- G6: la reversibilita'
                for con_A in ((True, False) if fa else (True,)):
                    carica()
                    c6 = nuovo(e, forma)
                    psi0, phi0_, A0, E0 = st["psi_h"].copy(), st["phi_h"].copy(), c6.A.copy(), c6.E.copy()
                    corri(c6, N_D, g2=g2)
                    a6 = float(np.max(np.abs(c6.A)))
                    e6 = float(np.max(np.abs(c6.E)))

                    def T_(cc):
                        UO.rovescia(st, mot, cc)
                        if not con_A:
                            cc.A[...] = -cc.A
                            UO.scrivi_U(mot, cc)
                    T_(c6)
                    corri(c6, N_D, t0=TICK0 + N_D, g2=g2)
                    T_(c6)
                    out = (U1.rel(psi0, st["psi_h"]), U1.rel(phi0_, st["phi_h"]), U1.rel(A0, c6.A, a6), U1.rel(E0, c6.E, e6), a6, e6)
                    r["G6" if con_A else "G6-F"] = out
                r["G2"] = g2[0]
                righe.append(r)
                g4, g5, g6 = r["chi"], r["G5"], r["G6"]
                print("  %-11s e %.4f | G4 rho %.1e eB %.1e |dE| %.2e stima %.2e (|dE|/stima %.3f) | G5 %.2e stima %.2e (max|E| %.2e, e max rho %.2e, max|drho| %.2e) | G6 psi %.1e phi %.1e A %.1e E %.1e (max|A| %.1e max|E| %.1e) | G2 %.1e"
                      % (forma, e, g4[0], g4[1], g4[2], g4[3], g4[2] / g4[3], g5[0], g5[1], g5[3], g5[5], g5[4], g6[0], g6[1], g6[2], g6[3], g6[4], g6[5], r["G2"]))
                if fa:
                    print("  %-11s e %.4f | G4-F (solo psi) rho %.2e | G5-F (sorgente spenta) %.2e, la chiave |G - G0 + e(rho - rho0)| %.2e, max|drho| %.2e | G6-F (senza A -> -A) psi %.1e A %.1e"
                          % (forma, e, r["G4-F"], r["G5-F"][0], r["G5-F"][2], r["G5-F"][4], r["G6-F"][0], r["G6-F"][2]))
                sys.stdout.flush()

        # ------------------------------------------------------------------ D6: R180 x sigma_z col campo
        ok_a, dd = CI.assi(inc, z["L"])
        esito("DEVE PASSARE: D6-C l'arco k e' del nodo k // 3 (la premessa di carta_impulso.rotazione)", ok_a, "gli assi %s" % dd)
        carica()
        c_c, _r = CI.centro(z, st["psi_h"])
        m2 = (int(round(2 * c_c[0])), int(round(2 * c_c[1])))
        v_ = np.arange(n_nodi)
        dove = CI.rotazione(inc, z["L"], dd, m2)
        nm = CI.nodo_di(z["L"], m2[0] - v_ // z["L"], m2[1] - v_ % z["L"])
        ka = dove[0::2] // 2                               # ### l'arco k va nell'arco ka[k], ROVESCIATO (la testa nella coda)
        assert np.array_equal(np.sort(ka), np.arange(inc.m)) and np.all(dove[0::2] % 2 == 1)
        PER_E, CON_U = ("psi_h", "phi_h"), ("psi_h", "psi")

        def ruota_tutto(x, c, U):
            y = {k: CI.applica(v, dove if k in PER_E else nm, U if k in CON_U else None) for k, v in x.items()}
            A, E = np.empty_like(c[0]), np.empty_like(c[1])
            A[ka], E[ka] = -c[0], -c[1]
            return y, (A, E)

        def foto(c):
            return {k: st[k].copy() for k in chiavi}, (c.A.copy(), c.E.copy())

        def metti(x, cA, c):
            for k in chiavi:
                st[k][...] = x[k]
            c.A[...], c.E[...] = cA
            UO.scrivi_U(mot, c)

        def scarti(a, b):
            out = {}
            for k in b:
                nb = float(np.linalg.norm(b[k]))
                out[k] = float(np.linalg.norm(a[k] - b[k])) / nb if nb > 0 else float(np.linalg.norm(a[k] - b[k]))
            return out

        d6 = {}
        for forma in U1.FORME:
            for e in E_PROVA:
                carica()
                c = nuovo(e, forma)
                corri(c, N_D6)                                     # ### il campo NON nullo prima della prova
                x1, cA1 = foto(c)
                t1 = TICK0 + N_D6
                for nu in (("sz", "1") if e == e_f else ("sz",)):
                    U = CI.SIGMA[nu]
                    metti(x1, cA1, c)
                    corri(c, N_D6, t0=t1)
                    xa, ca = foto(c)
                    ra, rca = ruota_tutto(xa, ca, U)
                    xr, cr = ruota_tutto(x1, cA1, U)
                    metti(xr, cr, c)
                    corri(c, N_D6, t0=t1)
                    xb, cb = foto(c)
                    sc = scarti(dict(xb, A=cb[0], E=cb[1]), dict(ra, A=rca[0], E=rca[1]))
                    d6[(forma, e, nu)] = sc
                    print("  D6 %-11s e %.4f U %-2s: |T^%d(R x) - R T^%d(x)| relativo per chiave %s; il massimo %.3e (max|A| %.1e)"
                          % (forma, e, nu, N_D6, N_D6, {k: "%.1e" % v for k, v in sc.items()}, max(sc.values()), float(np.max(np.abs(cA1[0])))))
                    sys.stdout.flush()

    # ------------------------------------------------------------------ i verdetti
    print("=" * 130)
    esito("DEVE PASSARE: G2 |U^dag U - I| <= %g a ogni tick di ogni corsa (G4, G5, G6), ogni configurazione" % TOLL_U, all(r["G2"] <= TOLL_U for r in righe),
          "il massimo %.2e" % max(r["G2"] for r in righe))
    esito("DEVE PASSARE: G4 la gauge: rho ed e B <= %g relativo, |dE| <= N 6 eps max|A'| / A_p, ogni configurazione (la decisione (1))" % TOLL_REL, all(r["G4"] for r in righe),
          "rho max %.1e, eB max %.1e, |dE|/stima max %.3f" % (max(r["chi"][0] for r in righe), max(r["chi"][1] for r in righe), max(r["chi"][2] / r["chi"][3] for r in righe)))
    esito("DEVE FALLIRE: G4-F chi solo su psi (U non trasformata): rho <= %g, nelle due forme a e %.4f" % (TOLL_REL, e_f), all(r["G4-F"] > TOLL_REL for r in righe if "G4-F" in r),
          "rho min %.2e" % min(r["G4-F"] for r in righe if "G4-F" in r))
    esito("DEVE PASSARE: G5 Gauss: max|(div E - e rho)(t) - (div E - e rho)(0)| <= N_C 6 eps max(max|E|, e max rho) per %d tick, ogni configurazione (sez. 2 e 13.4)" % N_C,
          all(r["G5"][0] <= r["G5"][1] for r in righe), "il rapporto max %.3f" % max(r["G5"][0] / r["G5"][1] for r in righe))
    esito("DEVE FALLIRE: G5-F la sorgente spenta: Gauss tiene -- e fallisce PER LA CHIAVE GIUSTA: la materia si muove e G - G0 = -e(rho - rho0) entro la stima",
          all(r["G5-F"][0] > r["G5-F"][1] and r["G5-F"][4] > 0 and r["G5-F"][2] <= r["G5-F"][1] for r in righe if "G5-F" in r),
          "rotto %s, chiave %s" % (["%.1e" % r["G5-F"][0] for r in righe if "G5-F" in r], ["%.1e" % r["G5-F"][2] for r in righe if "G5-F" in r]))
    tol6 = 2 * N_D * 6.0 * EPS
    esito("DEVE PASSARE: G6 %d avanti, T, %d avanti, T: psi, phi, A, E di partenza entro N 6 eps = %.2e relativo (N = %d), ogni configurazione" % (N_D, N_D, tol6, 2 * N_D),
          all(max(r["G6"][:4]) <= tol6 for r in righe), "il peggiore %.2e" % max(max(r["G6"][:4]) for r in righe))
    esito("DEVE FALLIRE: G6-F senza A -> -A: lo stato di partenza entro %.2e, nelle due forme a e %.4f" % (tol6, e_f), all(max(r["G6-F"][:4]) > tol6 for r in righe if "G6-F" in r),
          "il migliore %.2e" % min(max(r["G6-F"][:4]) for r in righe if "G6-F" in r))
    esito("DEVE PASSARE: D6 il tick col campo commuta con R180 x sigma_z (entro %g, ogni chiave, A ed E compresi), ogni configurazione" % CI.TOLL_UGUALE,
          all(max(v.values()) <= CI.TOLL_UGUALE for (f_, e_, nu), v in d6.items() if nu == "sz"), "il massimo %.2e" % max(max(v.values()) for (f_, e_, nu), v in d6.items() if nu == "sz"))
    esito("DEVE FALLIRE: D6-F lo stesso con U = 1: commuta entro %g, nelle due forme a e %.4f" % (CI.TOLL_UGUALE, e_f),
          all(max(v.values()) > CI.TOLL_UGUALE for (f_, e_, nu), v in d6.items() if nu == "1"), "il minimo %.2e" % min(max(v.values()) for (f_, e_, nu), v in d6.items() if nu == "1"))
    return fine()


def fine():
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
