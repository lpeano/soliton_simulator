# -*- coding: utf-8 -*-
r"""**`S162`: IL SINGOLO DI RIFERIMENTO DI `C35` SU `L 162`, CONTRO `TB3` E `TBS`** *(Luca `2026-11-06`; il task history `doc/TASK_HISTORY/2026-11-06_coppia_corse.md`, sez. `10`)*
    python csv/solitone/carta_s162.py > doc/referti_l2/s162_corsa.txt
### **La geometria** *(sez. `10`)*: il bordo di `C35` *(centro nel punto medio della coppia, `R_A 47.5`)*; il solitone a `17.5` dal centro: **la fascia a `30` nodi da un lato e a `65` dall'altro**; `TB3` a `28` da ogni lato.
### **I DEVE:** `P0` *(la `w` del primo campione = quella di `TB3` entro `TOLL_P0`)*, `P0-F` *(contro `TS`, deve fallire)*, `BR`, `BV`, `A4`, `ST-L`, `ST-M`, `ST-M-F`; **`BM` non c'e'** *(nessun gemello senza bordo su `L 162`)*.
### **Le misure:** i blocchi di `1000` *(velocita', direzione, cuore, `w`, alone)* per `S162`, `TB3`, `TBS`; lo spostamento; l'emissione *(il primo tempo con `M_ass / M0 > SOGLIA_EM`)*; il periodo dominante del cuore *(FFT dopo `T_RAMPA`)*.
### **Le letture** *(mie, scritte prima)*: (f1) la forma entro lo scarto `TBS - TB3`; (f2) il periodo e (f3) il ritardo dell'emissione, stampati senza verdetto.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL_B = 1e-10                 # ### BV (come carta_tbs)
TOLL_P0 = 1e-9                 # ### P0 (mia, sez. 10)
SOGLIA_EM = 1e-8               # ### l'emissione: il primo M_ass / M0 sopra (mia, sez. 10)
T_RAMPA = 1000.0               # ### l'oscillazione: la FFT dopo la rampa
BLOCCO = 1000.0
RITARDO_STIMA = (30.0 - 28.0) / 0.09   # ### sez. 10: la distanza in piu' dal lato vicino, sui fronti di TM1000

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


def periodo(tt, ff):
    """### **Il periodo dominante** di `ff(tt)` dopo `T_RAMPA`: interpolata su una griglia uniforme *(il passo mediano)*, tolta la retta, la FFT; `(periodo, risoluzione in frequenza)`."""
    m = tt > T_RAMPA
    t, f = tt[m], ff[m]
    if len(t) < 8:
        return None, None
    dt = float(np.median(np.diff(t)))
    g = np.arange(t[0], t[-1], dt)
    y = np.interp(g, t, f)
    y = y - np.polyval(np.polyfit(g, y, 1), g)
    F = np.abs(np.fft.rfft(y))
    nu = np.fft.rfftfreq(len(y), dt)
    i = 1 + int(np.argmax(F[1:]))
    return 1.0 / nu[i], float(nu[1])


def main(argv):
    del argv
    import _energia_del_legame as EL
    import _presidio
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import carta_deriva as CD
    from solitone import carta_statiche as CS
    from solitone import carta_tf3_lunga as T3
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "bordo", "corsa_accensione", "carta_deriva", "carta_tf3_lunga", "carta_statiche", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("S162: IL SINGOLO DI RIFERIMENTO DI C35 SU L 162 (Luca 2026-11-06) CONTRO TB3 E TBS; TOLL_B %g TOLL_P0 %g SOGLIA_EM %g T_RAMPA %g BLOCCO %g" % (TOLL_B, TOLL_P0, SOGLIA_EM, T_RAMPA, BLOCCO))
    print("  la geometria (sez. 10): il bordo di C35, il solitone a d/2 dal centro: la fascia a R_A - d/2 da un lato e a R_A + d/2 dall'altro; TB3 a R_A da ogni lato")
    print("  le letture (mie, scritte prima): (f1) la forma entro lo scarto TBS - TB3 a ogni blocco; (f2) il periodo del cuore e (f3) il ritardo dell'emissione, senza verdetto")
    print("=" * 130)
    rb, cb, _d, _a = CA.serie("S162")
    if not rb:
        print("### S162: NESSUN PEZZO")
        return 1
    _rs, cs, _d, _a = CA.serie("TS")
    r3, c3, _d, _a = CA.serie("TB3")
    rt, ct, _d, _a = CA.serie("TBS")
    L = rb[0]["L"]
    b0 = rb[0]["bordo"]
    cop = rb[0]["coppia"]
    ult = rb[-1]
    d2 = 0.5 * cop["d"]
    print("  L %d; la coppia di riferimento d %s segno %s; il bordo R_A %g, g_max %g: la fascia a %.1f e a %.1f nodi dal solitone lungo A1; TB3 R_A %g"
          % (L, cop["d"], cop["segno"], b0["R_A"], b0["g_max"], b0["R_A"] - d2, b0["R_A"] + d2, r3[0]["bordo"]["R_A"]))
    w0, w3, wS = cb[0]["per"]["w"], c3[0]["per"]["w"], cs[0]["per"]["w"]
    esito("DEVE PASSARE: P0 la w del primo campione di S162 = quella di TB3 entro %g relativo (la stessa partenza su un toro piu' grande)" % TOLL_P0, abs(w0 / w3 - 1.0) <= TOLL_P0, "S162 %.12f, TB3 %.12f" % (w0, w3))
    esito("DEVE FALLIRE: P0-F lo stesso contro TS entro %g" % TOLL_P0, not abs(w0 / wS - 1.0) <= TOLL_P0, "TS %.12f" % wS)
    esito("DEVE PASSARE: BR ogni pezzo: la stessa tabella di c(t) (sha), lo stesso g_max e R_A; la tabella e g_max quelli di TB3",
          all(r["bordo"]["sha_c"] == b0["sha_c"] and r["bordo"]["g_max"] == b0["g_max"] and r["bordo"]["R_A"] == b0["R_A"] for r in rb)
          and b0["sha_c"] == r3[0]["bordo"]["sha_c"] and b0["g_max"] == r3[0]["bordo"]["g_max"], "sha %s, g_max %g, R_A %g" % (b0["sha_c"], b0["g_max"], b0["R_A"]))
    tt = np.array([c["t"] for c in cb]) * s
    eM = np.array([(c["bordo"]["M"] + c["bordo"]["M_ass"]) / b0["M0"] - 1.0 for c in cb])
    eV = np.array([(c["bordo"]["V"] + c["bordo"]["V_ass"]) / b0["V0"] - 1.0 for c in cb])
    mS = {c["t"]: c["E"]["totale"]["M"] for c in cs}
    dS = [mS[c["t"]] / mS[0] - 1.0 for c in cb if c["t"] in mS]
    print("  ### il bilancio M + assorbita = M0 da solo (BM non si fa: nessun gemello senza bordo su L 162): il peggiore %.3e a t %.1f; all'ultimo %.3e; la deriva di M di TS (L 81) all'ultimo tempo comune %s"
          % (float(np.abs(eM).max()), tt[int(np.argmax(np.abs(eM)))], eM[-1], ("%+.3e" % dS[-1]) if dS else "nessuno"))
    esito("DEVE PASSARE: BV il bilancio V + assorbito = V0 entro %g a ogni campione" % TOLL_B, float(np.abs(eV).max()) <= TOLL_B, "il peggiore %.3e" % float(np.abs(eV).max()))
    esito("DEVE PASSARE: A4 S162 il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rb), "")
    finita = ult["t1"] >= ult["t_fine"]
    print("  S162: %d pezzi, fino al tick %d di %d (tempo %.2f); ### L'ARRESTO: %s" % (len(rb), ult["t1"], ult["t_fine"], ult["t1"] * s,
          ult.get("fermata") or ("la fine a %g" % (ult["t_fine"] * s) if finita else "### NON FINITA")))
    t_fine = float(tt[-1])
    # ------------------------------------------------------------------ gli stati completi su E:
    per_t = {c["t"]: c for c in cb}
    stati = [x for r in rb for x in (r.get("stati") or [])]
    ok_l, ok_m, ok_f, righe_st = True, True, True, []
    with CS.scena_con(V.N, L):
        with V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
            inc, m1, m2 = z["inc"], np.asarray(z["m1"]), np.asarray(z["m2"])
            for x in stati:
                with np.load(x["file"]) as d:
                    st = {k: d[k] for k in d.files if k != "t"}
                    t_st = int(d["t"])
                letto = t_st == x["t"] and all(SFM.sha(st[k]) == v for k, v in x["sha"].items())
                rho = np.zeros(inc.n)
                np.add.at(rho, inc.nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
                Mb = float(rho.sum())
                rd, _l = EL.densita(inc, st)
                c1, c2 = TO.centro(rd, m1, m2, L)[:2]
                c = per_t.get(t_st)
                uguale = c is not None and Mb == c["bordo"]["M"] and c1 == c["per"]["c1"] and c2 == c["per"]["c2"]
                cF = per_t.get(t_st + 100)
                uguale_F = cF is not None and Mb == cF["bordo"]["M"] and c1 == cF["per"]["c1"] and c2 == cF["per"]["c2"]
                ok_l, ok_m, ok_f = ok_l and letto, ok_m and uguale, ok_f and not uguale_F
                righe_st.append((t_st, letto, uguale, uguale_F, os.path.getsize(x["file"])))
    attesi = len(CA.STATI["S162"]) if finita else None
    esito("DEVE PASSARE: ST-L ogni stato completo su E: si rilegge al bit (gli sha registrati in corsa)%s" % ("" if attesi is None else ", e sono %d" % attesi),
          bool(stati) and ok_l and (attesi is None or len(stati) == attesi), "%d stati, %d byte" % (len(stati), sum(r[4] for r in righe_st)))
    esito("DEVE PASSARE: ST-M lo stato ricaricato da' M e il centro periodico AL BIT del campione allo stesso tick", bool(stati) and ok_m,
          "; ".join("t %.0f %s" % (r[0] * s, "al bit" if r[2] else "### NO") for r in righe_st))
    esito("DEVE FALLIRE: ST-M-F lo stesso confronto col campione di 100 tick dopo", bool(stati) and ok_f, "%d stati, nessuno uguale al campione di 100 tick dopo" % len(righe_st) if ok_f else "### uno e' uguale")
    mm = [r.get("mappe") for r in rb if r.get("mappe")]
    print("  le mappe su E:: %d file, %d istantanee, %d byte" % (len(mm), sum(m["istantanee"] for m in mm), sum(m["byte"] for m in mm)))
    # ------------------------------------------------------------------ i blocchi, contro TB3 e TBS fino alla fine di S162
    blocchi, tot, per_corsa = {}, {}, {}
    for nome, camp in (("S162", cb), ("TB3", c3), ("TBS", ct)):
        tq, X, ww, fl, al = T3.traiettoria(camp, {"S162": L, "TB3": r3[0]["L"], "TBS": rt[0]["L"]}[nome], s)
        m_ = tq <= t_fine
        tq, X, ww, fl, al = tq[m_], X[m_], ww[m_], fl[m_], al[m_]
        per_corsa[nome] = (tq, fl)
        righe = CD.finestre(nome, tq, X, ww, fl, 0.0, t_fine + 1.0, BLOCCO, False)
        print("-" * 130)
        print("### %s: %d campioni fino a %.1f (la fine di S162)" % (nome, len(tq), tq[-1]))
        print("  %-19s %-20s %-9s %-9s %-9s %-9s %-9s" % ("blocco", "X medio", "v/1000", "angolo", "cuore", "w", "alone"))
        bl = []
        for a, b, v, ang, wm, _amp, Xm in righe:
            m = (tq >= a) & (tq < b)
            cu, alo = float(fl[m].mean()), float(al[m].mean())
            bl.append((a, cu, wm, alo))
            print("   %7.0f .. %7.0f (%+8.3f, %+8.3f) %-9.3f %+9.2f %-9.5f %-9.4f %-9.5f" % (a, b, Xm[0], Xm[1], v, ang, cu, wm, alo))
        blocchi[nome] = bl
        vm = max(righe, key=lambda r: r[2])
        print("  la velocita' massima per blocco: %.3f per 1000 a %.0f .. %.0f (%+.2f gradi)" % (vm[2], vm[0], vm[1], vm[3]))
        dX = X[-1] - X[0]
        tot[nome] = (float(math.hypot(*dX)), math.degrees(math.atan2(dX[1], dX[0])), float(tq[-1]), float(np.hypot(X[:, 0] - X[0, 0], X[:, 1] - X[0, 1]).max()))
    print("-" * 130)
    print("### LO SPOSTAMENTO (l'ultimo campione meno il primo, srotolato; e il massimo lungo la strada), fino a %.1f" % t_fine)
    for nome, (d, ang, t, dmax) in tot.items():
        print("  %-6s %8.3f nodi a %+8.2f gradi; il massimo %.3f (a tempo %.1f)" % (nome, d, ang, dmax, t))
    # ------------------------------------------------------------------ (f1) la forma
    print("-" * 130)
    print("### (f1) LA FORMA: per blocco |S162 - TB3| contro |TBS - TB3| (cuore, w, alone)")
    nb = min(len(blocchi[n]) for n in blocchi)
    peggio = {"cuore": [], "w": [], "alone": []}
    for i in range(nb):
        a = blocchi["S162"][i][0]
        x = [abs(blocchi["S162"][i][j] - blocchi["TB3"][i][j]) for j in (1, 2, 3)]
        y = [abs(blocchi["TBS"][i][j] - blocchi["TB3"][i][j]) for j in (1, 2, 3)]
        for k_, xx, yy in zip(("cuore", "w", "alone"), x, y):
            peggio[k_].append((xx, yy))
        print("   %7.0f: cuore %.3e (TBS %.3e); w %.3e (TBS %.3e); alone %.3e (TBS %.3e)" % (a, x[0], y[0], x[1], y[1], x[2], y[2]))
    for k_, v in peggio.items():
        xs, ys = max(p[0] for p in v), max(p[1] for p in v)
        print("  ### (f1) %-6s il massimo |S162 - TB3| %.3e, il massimo |TBS - TB3| %.3e: %s" % (k_, xs, ys, "ENTRO: il bordo asimmetrico non cambia questa grandezza" if xs <= ys else "FUORI: il bordo asimmetrico la cambia"))
    # ------------------------------------------------------------------ (f2) l'oscillazione
    print("-" * 130)
    for nome, (tq, fl) in per_corsa.items():
        P, dnu = periodo(tq, fl)
        print("  ### (f2) %-5s il periodo dominante del cuore dopo %g: %s (la risoluzione in frequenza %s)" % (nome, T_RAMPA, ("%.2f" % P) if P else "non si legge", ("%.3e" % dnu) if dnu else "-"))
    # ------------------------------------------------------------------ (f3) l'emissione
    print("-" * 130)
    prima = {}
    for nome, camp, r0 in (("S162", cb, rb[0]), ("TB3", c3, r3[0]), ("TBS", ct, rt[0])):
        M0 = r0["bordo"]["M0"]
        tq = [c["t"] * s for c in camp if c["bordo"]["M_ass"] / M0 > SOGLIA_EM and c["t"] * s <= t_fine]
        prima[nome] = tq[0] if tq else None
        print("  ### (f3) %-5s il primo tempo con M_ass / M0 > %g: %s" % (nome, SOGLIA_EM, ("%.1f" % prima[nome]) if prima[nome] is not None else "mai"))
    if prima["S162"] is not None and prima["TB3"] is not None:
        print("  ### (f3) il ritardo S162 - TB3 %.1f; la stima della sez. 10 %.1f (senza verdetto)" % (prima["S162"] - prima["TB3"], RITARDO_STIMA))
    print("  ### per blocco: M, V, E assorbite nel blocco (relative a M0, V0, E0)")
    for nome, camp, r0 in (("S162", cb, rb[0]), ("TB3", c3, r3[0]), ("TBS", ct, rt[0])):
        bb = r0["bordo"]
        prec, a, righe = {"M_ass": 0.0, "V_ass": 0.0, "E_ass": 0.0}, 0.0, []
        while a < t_fine:
            blk = [c for c in camp if a < c["t"] * s <= a + BLOCCO]
            if not blk:
                break
            x = blk[-1]["bordo"]
            righe.append("%.0f: %.2e %.2e %+.2e" % (a, (x["M_ass"] - prec["M_ass"]) / bb["M0"], (x["V_ass"] - prec["V_ass"]) / bb["V0"], (x["E_ass"] - prec["E_ass"]) / bb["E0"]))
            prec = x
            a += BLOCCO
        print("    %-5s %s" % (nome, "; ".join(righe)))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
