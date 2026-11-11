# -*- coding: utf-8 -*-
r"""**S5.0 (e)-bis: IL SEGNO DI `h_k` NEL SOLITONE, PER CIASCUNO ZERO** *(sul ramo laterale; Luca `2026-11-11` `13:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.9`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_segno_h.py > doc/referti_l2/s5_segno_h.txt

**Lo stato di `TBS` a `10000`** *(lo sha come in H4)*, `cs = s` uniforme, `mot.lambda_c = None`. **`h_k` = l'energia del nodo** *(`termini_di_h`: il nodo piu' meta' dei suoi archi; a `cs` uniforme e' il
coefficiente della reazione)*, **con O1 e con O4** *(il nodo meno la media dei `6` vicini)*. **Le zone dal centro di `rho`:** il centro `r < w_in`, il guscio `w_in <= r < 3 w_in`, l'alone `3 w_in <= r < 20`,
il vuoto lontano `r >= 20`. **Per zona:** la media, il min, il max, la frazione con `h_k > 0`, e `h_k` meno il vuoto `c F3`. **Il verso atteso della forza** *(31.3)*. **Nessuna scelta dello zero.**
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

R_ZONA = 20.0                   # ### come H4
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


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import energia_pesata as EP
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "corsa_accensione", "bordo", "carta_punto_fisso", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("energia_pesata", "materia_vuoto"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    w_in = float(rr0[0]["w_in"])
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S5.0 (e)-bis (sez. 31.9): il segno di h_k nel solitone di %s a %d; cs = s = %g uniforme, mot.lambda_c = None; w_in %.6f; le zone r < w_in, < 3 w_in, < %g, oltre" % (CPF.CORSA, CPF.TICK_D4, s, w_in, R_ZONA))
    print("=" * 130)
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
        n, Lt, m = inc.n, z["L"], inc.m
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        nodo = np.asarray(inc.nodo)
        coppie = nodo.reshape(m, 2)
        vicini = np.zeros((n, 6), dtype=int)
        conta = np.zeros(n, dtype=int)
        for a_, b_ in coppie:
            vicini[a_, conta[a_]] = b_
            conta[a_] += 1
            vicini[b_, conta[b_]] = a_
            conta[b_] += 1
        assert np.all(conta == 6), "i nodi NON hanno 6 vicini"

        def h_di():
            mot.cs = np.full(n, float(s))
            mot.lambda_c = None
            pn, pa = EP.termini_di_h(mot, st, par)
            e = pn.copy()
            np.add.at(e, coppie[:, 0], 0.5 * pa)
            np.add.at(e, coppie[:, 1], 0.5 * pa)
            return e, float(np.sum(pn)) + float(np.sum(pa))
        # ------------------------------------------------------------------ il vuoto c F3
        for k in chiavi:
            st[k][...] = salvato[k]
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = c * phi_v
        ev, Ev = h_di()
        ev4 = ev - ev[vicini].mean(axis=1)
        print("### il vuoto c F3: h_k (O1) da %.10e a %.10e; (O4) da %.3e a %.3e; il totale %.10e" % (float(ev.min()), float(ev.max()), float(ev4.min()), float(ev4.max()), Ev))
        # ------------------------------------------------------------------ lo stato di TBS a 10000
        xs = stati[CPF.TICK_D4]
        for k in chiavi:
            st[k][...] = salvato[k]
        with np.load(xs["file"]) as d:
            for k in chiavi:
                st[k][...] = d[k]
        assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"
        e, E = h_di()
        esito("la somma di h_k = il totale (entro 1e-9 relativo)", abs(float(np.sum(e)) - E) <= 1e-9 * abs(E), "%.3e" % (float(np.sum(e)) - E))
        e4 = e - e[vicini].mean(axis=1)
        esito("O4: la somma su tutto il toro e' zero (entro 1e-9 del totale O1)", abs(float(np.sum(e4))) <= 1e-9 * abs(E), "%.3e" % float(np.sum(e4)))
        rho = np.zeros(n)
        np.add.at(rho, nodo, np.sum(np.abs(st["psi_h"].reshape(nodo.size, -1)) ** 2, axis=1))
        vv = np.arange(n)
        c1, c2 = TO.centro(rho, vv // Lt, vv % Lt, Lt)[:2]
        pos = TO.scarti(vv // Lt, vv % Lt, c1, c2, Lt)
        rr = np.hypot(pos[:, 0], pos[:, 1])
        zone = (("il centro", rr < w_in), ("il guscio", (rr >= w_in) & (rr < 3 * w_in)), ("l'alone", (rr >= 3 * w_in) & (rr < R_ZONA)), ("il vuoto lontano", rr >= R_ZONA))
        print("### %s: rho totale %.6f; il centro di rho (%.5f, %.5f); il totale E %.10e (il vuoto %.10e)" % (os.path.basename(xs["file"]), float(rho.sum()), c1, c2, E, Ev))
        print("  %-18s %6s %5s %14s %14s %14s %8s %14s %10s" % ("la zona", "nodi", "zero", "media h", "min h", "max h", "f(h>0)", "media h - vuoto", "rho medio"))
        for nome, msk in zone:
            for zz, hh, hv in (("O1", e, ev), ("O4", e4, ev4)):
                x = hh[msk]
                print("  %-18s %6d %5s %+14.6e %+14.6e %+14.6e %8.4f %+14.6e %10.4e" % (nome, int(msk.sum()), zz, float(x.mean()), float(x.min()), float(x.max()), float(np.mean(x > 0)),
                      float((x - hv[msk]).mean()), float(rho[msk].mean())))
        print("  IL VERSO ATTESO DELLA FORZA (31.3: V_k = s N'(rho) h_k, N' < 0): h_k > 0 spinge verso N piu' basso (dove c'e' piu' materia), h_k < 0 verso N piu' alto")
        for nome, msk in zone[:3]:
            print("    %-18s O1: la media %+.4e (%s); O4: la media %+.4e (%s)" % (nome, float(e[msk].mean()), "verso N piu' basso" if e[msk].mean() > 0 else "verso N piu' alto",
                  float(e4[msk].mean()), "verso N piu' basso" if e4[msk].mean() > 0 else "verso N piu' alto"))
        print("  (nessuna scelta dello zero: e' di Luca)")
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
