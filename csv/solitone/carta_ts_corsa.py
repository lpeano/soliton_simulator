# -*- coding: utf-8 -*-
r"""**`TS`: LA PARTENZA SIMMETRIZZATA SU `F3`, CONTRO `TF3` + `TF3C`** *(Luca, dopo `aad1435a` e `21:14`; il task history `doc/TASK_HISTORY/2026-11-03_D0_ruotata_e_TS.md`, sez. 8-9)*
    python csv/solitone/carta_ts_corsa.py > doc/referti_l2/ts_corsa.txt
### **Lo stato iniziale e' invariante per `S` = `R180` x `sigma_z` x `(phi -> -phi)` fino all'arrotondamento, e `S` commuta col tick vivo** *(`test_simmetrica` `S1`, `S4`; `carta_d0` `D-T`)*: il
seme della rottura puo' venire solo dall'arrotondamento. ### **Le letture di Luca, scritte prima:** (s1) parte lo stesso, piu' tardi: l'instabilita' e' del modello, il seme e' l'arrotondamento;
(s2) non parte entro `30000`: la corsa era dovuta alla nostra costruzione; (s3) altro.
### **I DEVE:** `T0` la partenza registrata e' `corsa_accensione.partenza_ts` ricalcolata *(lo sha)*; `T0-F` *(deve fallire)* e' la partenza di oggi *(`V.partenza`)*; `T1` al primo campione
l'asimmetria di `psi_h` e di `phi_h` entro `TOLL`; `A3`, `A4`. ### **Le misure:** il primo tempo in cui l'asimmetria supera ogni decade *(e quelli di Luca `1e-12`, `1e-6`, `1e-2`)*; a
blocchi di `1000` la velocita', la direzione, il cuore, `w`, l'alone di `TS` accanto a `TF3` + `TF3C`; lo spostamento totale; vaga o corre *(`carta_tf3_lunga.vaga_o_corre`)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL = 1e-12                   # ### T1: come test_simmetrica
LUCA = (1e-12, 1e-6, 1e-2)     # ### Luca dopo aad1435a: quando la simmetria si rompe
DECADI = tuple(10.0 ** k for k in range(-15, 1))
BLOCCO = 1000.0

OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-120s %s   %s" % (che[:120], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return passa


def main(argv):
    del argv
    import _presidio
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import carta_deriva as CD
    from solitone import carta_tf3_lunga as T3
    from solitone import corsa_accensione as CA
    for m in ("__init__", "accensione", "protetto", "corsa_accensione", "carta_deriva", "carta_tf3_lunga"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("TS: LA PARTENZA SIMMETRIZZATA SU F3 (Luca dopo aad1435a e 21:14) CONTRO TF3 + TF3C; TOLL %g LUCA %s BLOCCO %g" % (TOLL, LUCA, BLOCCO))
    print("  le letture di Luca, scritte prima: (s1) parte lo stesso, piu' tardi: l'instabilita' e' del modello, il seme e' l'arrotondamento; (s2) non parte entro 30000: la")
    print("  corsa era dovuta alla nostra costruzione; (s3) altro. La previsione di Luca dopo D0R: (s1) la piu' probabile")
    print("=" * 130)
    rt, ct, _d, _a = CA.serie("TS")
    if not rt:
        print("### TS: NESSUN PEZZO")
        return 1
    _r3, c3, _d, _a = CA.serie("TF3")
    _rc, cc, _d, _a = CA.serie("TF3C")
    L = rt[0]["L"]
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        ts = CA.partenza_ts(z, phi0, pK, s)
        for k, v in salvato.items():
            z["st"][k][...] = v
        p_oggi, _info = V.partenza(sol, z, phi0, pK, s)
    esito("DEVE PASSARE: T0 la partenza registrata di TS e' corsa_accensione.partenza_ts ricalcolata (lo sha, ogni pezzo)", all(r["sha_partenza_ts"] == SFM.sha(ts["psi"]) for r in rt),
          "%d pezzi; m2 %s; l'autovalore %+.15f; mu %.12f" % (len(rt), ts["m2"], ts["autovalore"], ts["mu"]))
    esito("DEVE FALLIRE: T0-F la partenza di TS e' quella di oggi (V.partenza)", rt[0]["sha_partenza_ts"] != SFM.sha(p_oggi), "")
    s0 = ct[0]["simm"]
    esito("DEVE PASSARE: T1 al primo campione (t %d) l'asimmetria di psi_h e di phi_h entro %g" % (ct[0]["t"], TOLL), s0["psi"] <= TOLL and s0["phi"] <= TOLL,
          "psi %.3e (c %+.6f), phi %.3e (c %+.6f)" % (s0["psi"], s0["c_psi"][0], s0["phi"], s0["c_phi"][0]))
    t3 = np.array([c["t"] for c in ct]) * s
    okM, nM = AC.a3(t3, np.array([c["E"]["totale"]["M"] for c in ct]), ct[-1]["t"], V.TOLL_NORMA)
    okV, nV = AC.a3(t3, np.array([c["E"]["totale"]["V"] for c in ct]), ct[-1]["t"], V.TOLL_NORMA)
    esito("DEVE PASSARE: A3 TS M e V (accensione.a3)", okM and okV, "M %s; V %s" % (nM, nV))
    esito("DEVE PASSARE: A4 TS il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rt), "")
    ult = rt[-1]
    print("  TS: %d pezzi, fino al tick %d di %d (tempo %.2f)%s" % (len(rt), ult["t1"], ult["t_fine"], ult["t1"] * s, "" if ult["t1"] >= ult["t_fine"] else " ### NON FINITA"))
    # ------------------------------------------------------------------ quando la simmetria si rompe
    print("-" * 130)
    ap = np.array([c["simm"]["psi"] for c in ct])
    af = np.array([c["simm"]["phi"] for c in ct])
    print("### QUANDO LA SIMMETRIA SI ROMPE: |S x - c x| / |x| per psi_h (con sigma_z) e phi_h (con il segno nel c), %d campioni fino a %.1f" % (len(t3), t3[-1]))
    for nome, a in (("psi_h", ap), ("phi_h", af)):
        tre = []
        for dec in LUCA:
            i = np.nonzero(a > dec)[0]
            tre.append("%.0e: %s" % (dec, ("%.2f" % t3[i[0]]) if len(i) else "mai (fino a %.1f)" % t3[-1]))
        print("  ### LUCA: %s supera %s" % (nome, "; ".join(tre)))
        righe = []
        for dec in DECADI:
            i = np.nonzero(a > dec)[0]
            righe.append("%.0e %s" % (dec, ("%.1f" % t3[i[0]]) if len(i) else "mai"))
        print("    %s, ogni decade: %s" % (nome, "  ".join(righe)))
    # ------------------------------------------------------------------ la corsa, contro TF3 + TF3C
    tot = {}
    for nome, camp in (("TS (F3, simmetrizzata)", ct), ("TF3 + TF3C (F3)", c3 + cc)):
        tt, X, ww, fl, al = T3.traiettoria(camp, L, s)
        m_ = tt <= T3.FINE
        tt, X, ww, fl, al = tt[m_], X[m_], ww[m_], fl[m_], al[m_]
        righe = CD.finestre(nome, tt, X, ww, fl, 0.0, min(T3.FINE, tt[-1] + 1.0), BLOCCO, False)
        print("-" * 130)
        print("### %s: %d campioni fino a %.1f" % (nome, len(tt), tt[-1]))
        print("  %-19s %-20s %-9s %-9s %-9s %-9s %-9s" % ("blocco", "X medio", "v/1000", "angolo", "cuore", "w", "alone"))
        for a, b, v, ang, wm, _amp, Xm in righe:
            m = (tt >= a) & (tt < b)
            print("   %7.0f .. %7.0f (%+8.3f, %+8.3f) %-9.3f %+9.2f %-9.5f %-9.4f %-9.5f" % (a, b, Xm[0], Xm[1], v, ang, float(fl[m].mean()), wm, float(al[m].mean())))
        vm = max(righe, key=lambda r: r[2])
        print("  la velocita' massima per blocco: %.3f per 1000 a %.0f .. %.0f (%+.2f gradi)" % (vm[2], vm[0], vm[1], vm[3]))
        T3.vaga_o_corre(nome, tt, X, righe)
        dX = X[-1] - X[0]
        tot[nome] = (float(math.hypot(*dX)), math.degrees(math.atan2(dX[1], dX[0])), float(tt[-1]))
    print("-" * 130)
    print("### LO SPOSTAMENTO TOTALE (l'ultimo campione meno il primo, srotolato)")
    for nome, (d, ang, t) in tot.items():
        print("  %-28s %8.3f nodi a %+8.2f gradi (a tempo %.1f)" % (nome, d, ang, t))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
