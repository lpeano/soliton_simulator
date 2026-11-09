# -*- coding: utf-8 -*-
r"""**F1, LA MEMORIA (`A15`): LA PROVA** *(sul ramo laterale; Luca `2026-11-09` `16:18`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `18`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/carta_f1.py > doc/referti_l2/carta_f1.txt

**`cs` costante dentro il tick** *(`mot.cs`, `mot.lambda_c`, `tick.percorri_tick` intero)*; **al confine il trapezio** `cs' = [cs (1 - r/2) + r L] / (1 + r/2)`, `L = FP.cs(Lambda, Lambda_c)`,
`r = omega_v` *(la rotazione di fase del vuoto nel tick appena fatto, per nodo)*. **(q1)** `cs'` della legge; **(q2)** `cs_primo = 0`. **Il calore della memoria:** `g_pesata(cs') - g_pesata(cs)` sullo stesso stato.
**I DEVE:** `F1-V` *(il vuoto: `cs = s` entro `8 eps`)*; `F1-I` *(l'inversa del trapezio al confine entro `1e-14` relativo)*; `F1-F` *(DEVE FALLIRE: la regola esplicita invertita col trapezio)*.
"""
import contextlib
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 200                   # ### sez. 18.6
N_VUOTO = 50                   # ### sez. 18.6
DELTA = 1e-8                   # ### sez. 18.6: la perturbazione sul centro
EPS = CPF.EPS
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def trapezio(cs, L, r):
    return (cs * (1.0 - 0.5 * r) + r * L) / (1.0 + 0.5 * r)


def inversa(cs1, L, r):
    return (cs1 * (1.0 + 0.5 * r) - r * L) / (1.0 - 0.5 * r)


@contextlib.contextmanager
def cs_primo_zero(attivo):
    import energia_pesata as EP
    vera = EP.cs_primo

    def zero(lam, lambda_c, fuori):
        fuori[...] = 0.0
        return fuori
    if attivo:
        EP.cs_primo = zero
    try:
        yield
    finally:
        EP.cs_primo = vera


def omega_v(st0_phi, st1_phi, nodo, n):
    """### la rotazione di fase del vuoto nel tick, per nodo: l'angolo di `somma conj(phi0) phi1` sulle estremita' del nodo."""
    z = np.zeros(n, dtype=complex)
    np.add.at(z, nodo, np.sum(np.conj(st0_phi) * st1_phi, axis=1))
    return np.abs(np.angle(z))


def corsa(st, mot, par, lc, cs0, n_tick, q2, stampa):
    import composizione as CM
    import energia_pesata as EP
    import flussi_parziali as FP
    import tick as TK
    fp = np.zeros(mot.inc.n)
    cs = cs0.copy()
    calore = 0.0
    storia = []
    with cs_primo_zero(q2):
        for k in range(1, n_tick + 1):
            phi0 = st["phi_h"].copy()
            mot.cs = cs.copy()
            mot.lambda_c = float(lc)
            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
            r = omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n)
            L = FP.cs(mot.densita_vuoto(st), lc, fp).copy()
            g0 = EP.g_pesata(mot, st, par)
            cs1 = trapezio(cs, L, r)
            mot.cs = cs1.copy()
            g1 = EP.g_pesata(mot, st, par)
            calore += float(g1 - g0)
            cs = cs1
            norma = float(np.sum(np.abs(st["psi_h"]) ** 2))
            storia.append(cs.copy())
            if stampa and (k <= 5 or k % 10 == 0):
                print("    tick %4d: max|cs - L| %.3e; cs min %.6f max %.6f; r min %.4f max %.4f; la norma %.12f; il calore della memoria (somma) %+.6e" % (k, float(np.max(np.abs(cs - L))), float(cs.min()), float(cs.max()), float(r.min()), float(r.max()), norma, calore))
                sys.stdout.flush()
    return storia


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import flussi_parziali as FP
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr, _camp = CA.serie(CPF.CORSA)[:2]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("F1, LA MEMORIA (sez. 18): %s a %d tick; %d tick per modo (q1, q2); il vuoto %d tick; la perturbazione %g sul centro" % (CPF.CORSA, CPF.TICK_D4, N_TICK, N_VUOTO, DELTA))
    print("=" * 130)
    # ------------------------------------------------------------------ F1-I, F1-F: l'inversa al confine (aritmetica)
    rg = np.random.default_rng(CPF.SEME)
    cs_ = rg.uniform(0.01, 0.3, 1000)
    L_ = rg.uniform(0.01, 0.3, 1000)
    r_ = rg.uniform(0.0, 1.5, 1000)
    d1 = float(np.max(np.abs(inversa(trapezio(cs_, L_, r_), L_, r_) - cs_) / cs_))
    esito("F1-I l'inversa del trapezio al confine ridà cs entro 1e-14 relativo (1000 terne a caso)", d1 <= 1e-14, "%.2e" % d1)
    esplicita = cs_ + r_ * (L_ - cs_)
    d2 = float(np.max(np.abs(inversa(esplicita, L_, r_) - cs_) / cs_))
    esito("F1-F la regola ESPLICITA invertita col trapezio ridà cs entro 1e-14", d2 <= 1e-14, "%.2e" % d2, deve=False)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        # ------------------------------------------------------------------ F1-V: il vuoto F3 da solo
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        lc = float(np.mean(mot.densita_vuoto(st))) * (1.0 - s) / s
        print("### Lambda_c = %.12f" % lc)
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            cs0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(inc.n)).copy()
            sv = corsa(st, mot, par, lc, cs0, N_VUOTO, False, False)
        dv = max(float(np.max(np.abs(c - s))) for c in sv)
        esito("F1-V il vuoto F3 da solo, %d tick: cs = s entro 8 eps relativo" % N_VUOTO, dv <= 8 * EPS * s, "%.3e" % dv)
        # ------------------------------------------------------------------ la scena
        xs = stati[CPF.TICK_D4]
        for modo, q2 in (("(q1) cs' della legge", False), ("(q2) cs' = 0", True)):
            ris = []
            for pert in (0.0, DELTA):
                with np.load(xs["file"]) as d:
                    for k in chiavi:
                        st[k][...] = d[k]
                assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
                rho = np.zeros(inc.n)
                np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                vv = np.arange(inc.n)
                L_ = z["L"]
                c1, c2 = TO.centro(rho, vv // L_, vv % L_, L_)[:2]
                pos = TO.scarti(vv // L_, vv % L_, c1, c2, L_)
                rr_ = np.hypot(pos[:, 0], pos[:, 1])
                with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                    cs0 = FP.cs(mot.densita_vuoto(st), lc, np.zeros(inc.n)).copy()
                    cs0[rr_ < 1.0] += pert
                    print("### %s, la perturbazione %g sul centro (%d nodi)" % (modo, pert, int(np.sum(rr_ < 1.0))))
                    try:
                        ris.append(corsa(st, mot, par, lc, cs0, N_TICK, q2, pert == 0.0))
                        print("    arrivata a %d tick" % N_TICK)
                    except Exception as e:
                        print("    ### ALZA: %s: %s" % (type(e).__name__, str(e)[:120]))
                        ris.append(None)
            if all(x is not None for x in ris):
                dd = [float(np.max(np.abs(a - b))) for a, b in zip(ris[0], ris[1])]
                print("  %s: la differenza fra le due corse, tick per tick (1, 2, 5, 10, 20, 50, 100, 200): %s" % (modo, " ".join("%.2e" % dd[k - 1] for k in (1, 2, 5, 10, 20, 50, 100, 200) if k <= len(dd))))
                cr = [dd[k] / dd[k - 1] for k in range(1, min(len(dd), 20)) if dd[k - 1] > 0]
                print("  %s: il fattore di crescita per tick, la mediana sui primi 20: %.4f" % (modo, float(np.median(cr)) if cr else float("nan")))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
