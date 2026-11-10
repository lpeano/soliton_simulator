# -*- coding: utf-8 -*-
r"""**T3, IL TEMPO DI MEMORIA `tau_Lambda`** *(sul ramo laterale; Luca `2026-11-09` `20:13`, ripartito `2026-11-10` `01:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `26`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/tau_lambda.py > doc/referti_l2/tau_lambda.txt

**Il passo delle mappe** *(`mappe.OGNI`)* **contro `1/omega`** *(stampato)*; **al posto della `tau_int` dalle mappe, il rilassamento di `Lambda` dopo un disturbo `1 + 1e-6`** **su tre nodi** *(centro, raggio `17`, raggio `25`,
lungo `+x`)*, **`TBS` a `10000` tick, `cs` spento, `1000` tick; `tau_Lambda` = il primo tick con `|DeltaLambda| <= e^{-1} |DeltaLambda(0)|`.** **T3-P, T3-F** *(DEVE FALLIRE)*; **le letture t1/t2.**
"""
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_f1 as F1  # noqa: E402
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 1000                  # ### sez. 26.2
RAGGI = (0.0, 17.0, 25.0)      # ### sez. 26.2: centro, guscio, vuoto
DISTURBO = 1e-6                # ### sez. 26.2
SOGLIA_F = 1e-9                # ### sez. 26.2: T3-F
RAPPORTO_T1 = 10.0             # ### sez. 26.3 (mio, dichiarato)
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


def corsa(st, mot, par, nodo, omega=None):
    """### `N_TICK` tick a `cs` spento; `Lambda` del `nodo` a ogni tick *(il tick 0 compreso)*; `omega`: la lista in cui mettere `omega_v` del primo tick."""
    import composizione as CM
    import tick as TK
    lam = [float(mot.densita_vuoto(st)[nodo])]
    for k in range(1, N_TICK + 1):
        phi0 = st["phi_h"].copy()
        mot.lambda_c = None
        TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
        if k == 1 and omega is not None:
            omega.append(F1.omega_v(phi0, st["phi_h"], mot.inc.nodo, mot.inc.n))
        lam.append(float(mot.densita_vuoto(st)[nodo]))
    return np.array(lam)


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "toro", "carta_punto_fisso", "carta_f1", "mappe"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0, _camp = CA.serie(CPF.CORSA)[:2]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    t00 = time.time()
    print("=" * 130)
    print("T3, IL TEMPO DI MEMORIA tau_Lambda (sez. 26): %s a %d tick, cs spento; il disturbo 1 + %g su un nodo ai raggi %s; %d tick" % (CPF.CORSA, CPF.TICK_D4, DISTURBO, RAGGI, N_TICK))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        xs = stati[CPF.TICK_D4]

        def carica():
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
        carica()
        rho = np.zeros(inc.n)
        np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
        nodi = np.arange(inc.n)
        Lt = z["L"]
        c1, c2 = TO.centro(rho, nodi // Lt, nodi % Lt, Lt)[:2]
        pos = TO.scarti(nodi // Lt, nodi % Lt, c1, c2, Lt)
        scelti = []
        for R in RAGGI:
            d = np.hypot(pos[:, 0] - R, pos[:, 1])
            scelti.append(int(np.argmin(d)))
        print("### i nodi: %s" % "; ".join("raggio %g -> nodo %d (x %+.2f, y %+.2f)" % (R, i, pos[i, 0], pos[i, 1]) for R, i in zip(RAGGI, scelti)))
        ris = {}
        om = []
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            carica()
            base = {i: None for i in scelti}
            t1 = time.time()
            lam_tutti = []
            import composizione as CM
            import tick as TK
            lam_tutti.append(mot.densita_vuoto(st)[scelti].copy())
            for k in range(1, N_TICK + 1):
                p0 = st["phi_h"].copy()
                mot.lambda_c = None
                TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                if k == 1:
                    om.append(F1.omega_v(p0, st["phi_h"], inc.nodo, inc.n))
                lam_tutti.append(mot.densita_vuoto(st)[scelti].copy())
            lam_tutti = np.array(lam_tutti)
            for j, i in enumerate(scelti):
                base[i] = lam_tutti[:, j]
            print("### la base: %.0f s" % (time.time() - t1))
            carica()
            rip = corsa(st, mot, par, scelti[0])
            esito("T3-P la base rifatta contro se stessa: DeltaLambda = 0 esatto sul nodo del centro a ogni tick", bool(np.all(rip == base[scelti[0]])), "max %.3e" % float(np.max(np.abs(rip - base[scelti[0]]))))
            for R, i in zip(RAGGI, scelti):
                carica()
                est = inc.nodo == i
                st["phi_h"][est] *= math.sqrt(1.0 + DISTURBO)
                t1 = time.time()
                ris[i] = corsa(st, mot, par, i)
                print("### il disturbo al raggio %g (nodo %d): %.0f s" % (R, i, time.time() - t1))
    w = om[0]
    print("-" * 130)
    print("  IL PASSO DELLE MAPPE: mappe.OGNI = %d tick; omega_v del vuoto (la mediana sui nodi oltre il raggio 30, il primo tick della base) %.6f per tick, 1/omega %.3f tick: il passo e' %.1f volte 1/omega"
          % (MP.OGNI, float(np.median(w[np.hypot(pos[:, 0], pos[:, 1]) > 30.0])), 1.0 / float(np.median(w[np.hypot(pos[:, 0], pos[:, 1]) > 30.0])), MP.OGNI * float(np.median(w[np.hypot(pos[:, 0], pos[:, 1]) > 30.0]))))
    for R, i in zip(RAGGI, scelti):
        dl = ris[i] - base[i]
        d0 = abs(float(dl[0]))
        esito("T3-F il disturbo NON si vede sul nodo al raggio %g (|DeltaLambda(0)|/Lambda sotto %g)" % (R, SOGLIA_F), d0 / base[i][0] < SOGLIA_F, "%.3e" % (d0 / base[i][0]), deve=False)
        sotto = np.flatnonzero(np.abs(dl) <= math.exp(-1.0) * d0)
        tau = int(sotto[0]) if len(sotto) else None
        inv = 1.0 / float(w[i]) if w[i] > 0 else float("inf")
        rap = (tau / inv) if tau is not None else float("inf")
        lett = "t1" if rap > RAPPORTO_T1 else "t2"
        print("  raggio %5g (nodo %d): Lambda %.6f; omega_v %.6f per tick, 1/omega %.3f tick; DeltaLambda/DeltaLambda(0) ai tick 1, 2, 5, 10, 50, 100, 1000: %s; tau_Lambda %s; il rapporto tau/(1/omega) %s: (%s)"
              % (R, i, base[i][0], float(w[i]), inv, " ".join("%+.3e" % (float(dl[k]) / float(dl[0])) for k in (1, 2, 5, 10, 50, 100, N_TICK)),
                 "%d tick" % tau if tau is not None else "oltre %d" % N_TICK, "%.3f" % rap if rap != float("inf") else "infinito", lett))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
