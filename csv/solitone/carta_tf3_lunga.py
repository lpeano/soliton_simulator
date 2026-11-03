# -*- coding: utf-8 -*-
r"""**`TF3` CONTINUATA FINO A `30000`** *(Luca, le decisioni corrette dopo `fe409582`; il task history `doc/TASK_HISTORY/2026-11-03_TF3_lunga.md`)*:
### **`TF3` + `TF3C` (il vuoto `F3`) accanto a `TP1000` + `DG1000` (il vuoto `F0`, la versione rada del repo), il centro periodico srotolato.**
    python csv/solitone/carta_tf3_lunga.py > doc/referti_l2/tf3_lunga.txt      # dopo la corsa TF3C
### **I DEVE:** `C0` il primo pezzo di `TF3C` parte dall'ultimo di `TF3` *(il `t0`, e lo stato di ripresa `TF3.npz` al bit dello `sha_fine` di `TF3`)*; `C0-F` *(deve fallire)* lo
`sha_fine` del primo pezzo di `TF3C` uguale a quello del primo di `DG1000`; `C1` lo `sha_vuoto` e' quello di `fondo_con_fasi(F3)`; `A3` *(`accensione.a3`, `TF3` + `TF3C`)*; `A4`.
### **Le misure a blocchi di `1000`, da `0` a `30000`:** la velocita', la direzione *(e i coseni con `A1`, `A2`, `A1+A2`)*, `ln s` *(`carta_deriva.logaritmo`)*, la freccia del vuoto
sotto il solitone *(`F3`: in ogni campione; `F0`: dagli stati completi di `TM1000` e `DG1000`)*, il cuore, `w`, l'alone; ### **i blocchi oltre la fine valida** *(`3 w >= R`)*
**marcati con `*`, non tagliati.** **Nessuna soglia, nessun tempo di partenza** *(`TM` abbandonato)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

BLOCCO = 1000.0                # ### Luca: a blocchi di 1000, come TF3
FINE = 30000.0                 # ### Luca: fino a 30000
STATI_F0 = (("TM1000", (13333, 40000, 66667)), ("DG1000", (133333, 200000)))   # ### la freccia di F0: gli stati completi su E: (TM1000 al bit di TP1000; DG1000 a 20000, 30000)

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


def traiettoria(camp, L, s):
    """### **`(tt, X, w, cuore, alone)`:** il centro periodico srotolato *(come `carta_deriva.dati`)*, su una lista di campioni gia' unita."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    tt = np.array([c["t"] for c in camp]) * s
    c1 = np.array([c["per"]["c1"] for c in camp])
    c2 = np.array([c["per"]["c2"] for c in camp])
    u1 = np.concatenate([[0.0], np.cumsum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)])
    u2 = np.concatenate([[0.0], np.cumsum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)])
    X = u1[:, None] * A1 + u2[:, None] * A2
    return tt, X, np.array([c["per"]["w"] for c in camp]), np.array([c["per"]["f_liscia"] for c in camp]), np.array([c["per"]["alone"] for c in camp])


def coseni(v):
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    n = math.hypot(*v)
    if n == 0:
        return (float("nan"),) * 3
    return tuple(float(np.dot(v, a) / (n * math.hypot(*a))) for a in (A1, A2, A1 + A2))


def main(argv):
    del argv
    import _presidio
    import _solitone_dal_fondo as SD
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import carta_deriva as CD
    from solitone import carta_giri as CG
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    from solitone import vuoto as VU
    for m in ("__init__", "toro", "vuoto", "accensione", "corsa_accensione", "carta_deriva", "carta_giri"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    print("=" * 130)
    print("TF3 CONTINUATA FINO A 30000 (Luca, le decisioni corrette dopo fe409582): TF3 + TF3C (F3) accanto a TP1000 + DG1000 (F0, la rada); BLOCCO %g FINE %g STATI_F0 %s"
          % (BLOCCO, FINE, STATI_F0))
    print("  le letture di Luca, scritte prima: (f1) la deriva parte e corre come su F0, piu' tardi: la freccia di fondo e' un acceleratore, la causa e' altrove; (f2) la velocita'")
    print("  torna bassa: su F3 il solitone vaga; (f3) parte ma resta molto piu' lento: la freccia di fondo conta per la forza; (f4) altro. * = oltre la fine valida (3 w >= R)")
    print("=" * 130)
    r3, c3, _d, _a = CA.serie("TF3")
    rc, cc, _d, _a = CA.serie("TF3C")
    rp, cp, _d, _a = CA.serie("TP1000")
    rg = CG.rade()
    cg = [c for r in rg for c in r["campioni"]]
    if not rc:
        print("### TF3C: NESSUN PEZZO")
        return
    L = r3[0]["L"]
    # ------------------------------------------------------------------ i DEVE
    ult3 = r3[-1]
    with np.load(os.path.join(CA.DIR_NPZ, "TF3.npz")) as d:
        t_rip = int(d["t"])
        sh = {k: SFM.sha(d[k]) for k in sorted(d.files) if k != "t"}
    esito("DEVE PASSARE: C0 il primo pezzo di TF3C parte dall'ultimo di TF3 (t0 = t1, e TF3.npz al bit dello sha_fine di TF3, ogni chiave)",
          rc[0]["t0"] == ult3["t1"] == t_rip and sh == ult3["sha_fine"], "t0 %d, t1 di TF3 %d, t di TF3.npz %d; %d chiavi" % (rc[0]["t0"], ult3["t1"], t_rip, len(sh)))
    esito("DEVE FALLIRE: C0-F lo sha_fine del primo pezzo di TF3C e' quello del primo di DG1000 (lo stesso tempo, il vuoto diverso)",
          rc[0]["sha_fine"] != rg[0]["sha_fine"], "t0 TF3C %d, DG1000 %d" % (rc[0]["t0"], rg[0]["t0"]))
    with V.scena(s, "fondo", V.EPS) as (_rec, z, _phi0, _pK):
        inc = z["inc"]
        idx, dirs = VU.celle(inc, L)
        phi3 = SD.fondo_con_fasi(inc, L, CA.fasi_vuoto("TF3C"))
        esito("DEVE PASSARE: C1 lo sha_vuoto di TF3C e' quello di fondo_con_fasi(%s)" % (CA.fasi_vuoto("TF3C"),), all(r["sha_vuoto"] == SFM.sha(phi3) for r in rc), "")
        frs = {}
        for nome, tt_ in STATI_F0:
            for t in tt_:
                f = os.path.join(CA.base_e(nome), "stati", nome, "%s_stato_%06d.npz" % (nome, t))
                with np.load(f) as d:
                    frs[t * s] = VU.freccia_media(VU.freccia(d["phi_h"], idx, dirs))
    ca = c3 + cc
    t3 = np.array([c["t"] for c in ca]) * s
    okM, nM = AC.a3(t3, np.array([c["E"]["totale"]["M"] for c in ca]), ca[-1]["t"], V.TOLL_NORMA)
    okV, nV = AC.a3(t3, np.array([c["E"]["totale"]["V"] for c in ca]), ca[-1]["t"], V.TOLL_NORMA)
    esito("DEVE PASSARE: A3 TF3 + TF3C M e V (accensione.a3)", okM and okV, "M %s; V %s" % (nM, nV))
    esito("DEVE PASSARE: A4 TF3C il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rc), "")
    ult = rc[-1]
    print("  TF3C: %d pezzi, fino al tick %d di %d (tempo %.2f)%s" % (len(rc), ult["t1"], ult["t_fine"], ult["t1"] * s, "" if ult["t1"] >= ult["t_fine"] else " ### NON FINITA"))
    # ------------------------------------------------------------------ le misure
    R = TO.meta_periodo(L)
    tot = {}
    for nome, camp, conf in (("TF3 + TF3C (F3)", ca, True), ("TP1000 + DG1000 rada (F0)", cp + cg, False)):
        tt, X, ww, fl, al = traiettoria(camp, L, s)
        m_ = tt <= FINE
        tt, X, ww, fl, al = tt[m_], X[m_], ww[m_], fl[m_], al[m_]
        fine = CD.fine_valida(tt, ww, R, BLOCCO)
        fm = np.array([c["freccia"]["modulo"] if "freccia" in c else np.nan for c in camp])[m_]
        fsc = np.array([c["freccia"]["scarto"] if "freccia" in c else np.nan for c in camp])[m_]
        righe = CD.finestre(nome, tt, X, ww, fl, 0.0, min(FINE, tt[-1] + 1.0), BLOCCO, False)
        print("-" * 130)
        print("### %s: %d campioni fino a %.1f; la fine valida (3 w < R = %.2f) %g" % (nome, len(tt), tt[-1], R, fine))
        print("  %-19s %-20s %-9s %-9s %-23s %-9s %-9s %-9s %-11s %-11s" % ("blocco", "X medio", "v/1000", "angolo", "cos A1 / A2 / A1+A2", "cuore", "w", "alone", "|freccia|", "scarto"))
        for a, b, v, ang, wm, _amp, Xm in righe:
            m = (tt >= a) & (tt < b)
            cs = coseni((math.cos(math.radians(ang)) * v, math.sin(math.radians(ang)) * v))
            print("  %s%7.0f .. %7.0f (%+8.3f, %+8.3f) %-9.3f %+9.2f %+6.3f / %+6.3f / %+6.3f %-9.5f %-9.4f %-9.5f %-11.4e %-11.4e"
                  % ("*" if a >= fine else " ", a, b, Xm[0], Xm[1], v, ang, cs[0], cs[1], cs[2], float(fl[m].mean()), wm, float(al[m].mean()),
                     float(np.nanmean(fm[m])) if np.isfinite(fm[m]).any() else float("nan"), float(np.nanmax(fsc[m])) if np.isfinite(fsc[m]).any() else float("nan")))
        CD.logaritmo(nome, tt, X, 1000.0, min(FINE, tt[-1] + 1.0), BLOCCO)
        dX = X[-1] - X[0]
        tot[nome] = (float(math.hypot(*dX)), math.degrees(math.atan2(dX[1], dX[0])), float(tt[-1]))
    print("-" * 130)
    print("### LA FRECCIA DI F0 SOTTO IL SOLITONE, dagli stati completi (TM1000 al bit di TP1000; DG1000): il modulo medio, lo scarto massimo fra i nodi, |la media|")
    for t in sorted(frs):
        mm = np.array(frs[t]["media"])
        print("  tempo %8.2f: modulo %.6f scarto %.3e |media| %.4e" % (t, frs[t]["modulo"], frs[t]["scarto"], float(np.sqrt(np.sum(mm ** 2)))))
    print("-" * 130)
    print("### LO SPOSTAMENTO TOTALE (l'ultimo campione fino a %g meno il primo, srotolato)" % FINE)
    for n_, (d_, a_, t_) in tot.items():
        print("  %-28s %.3f nodi a %+.2f gradi (a tempo %.1f)" % (n_, d_, a_, t_))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))


if __name__ == "__main__":
    main(sys.argv[1:])
