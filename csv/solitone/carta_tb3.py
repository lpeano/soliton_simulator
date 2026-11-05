# -*- coding: utf-8 -*-
r"""**`TB3`: `TF3` COL BORDO ASSORBENTE, CONTRO `TF3` + `TF3C` E `TS`** *(Luca `2026-11-03` `21:52`, `2026-11-04` `09:00`, `09:26`; il task history `doc/TASK_HISTORY/2026-11-03_TB3_bordo_assorbente.md`)*
    python csv/solitone/carta_tb3.py > doc/referti_l2/tb3_corsa.txt
### **La domanda di Luca:** il moto parte senza il rientro dal toro? ### **Le letture, scritte prima:** (b1) non parte entro `30000`, o resta sotto `TF3` e `TS`: il moto veniva dal giro del toro;
(b2) parte comunque, con velocita' e persistenza come `TS` / `TF3` / `F0`: il moto e' del solitone; (b3) altro. ### **`TB3` risponde a «parte?», non a «quanto corre»:** l'arresto (i) a `~8` nodi.
### **I DEVE:** `P0` il primo campione di `TB3` e' quello di `TF3` *(la stessa partenza: `per` e `E`, al bit)*; `P0-F` *(deve fallire)* e' quello di `TS`; `BM` il bilancio `M` dentro + assorbita **meno la deriva di `M` di `TF3 + TF3C` agli stessi tick** entro `TOLL_B` *(Luca 2026-11-04 18:31)*, `BM-F` *(deve fallire)* con la deriva per `2`;
`BV` il bilancio `V` dentro + assorbito = iniziale entro `TOLL_B` *(Luca 21:52)* a ogni campione; `BR` ogni pezzo legge la stessa tabella di `c(t)` *(lo sha)* e lo stesso `g_max`; `A4` il libro col `par` della corsa.
### **Le misure:** l'arresto *(tempo e motivo)*; a blocchi di `1000` velocita', direzione, cuore, `w`, alone di `TB3`, `TF3 + TF3C`, `TS` *(fino all'arresto)*; vaga o corre; lo spostamento; la fase del
vuoto nella fascia *(la lettura 5.3)*; `M`, `V`, `E` assorbite per blocco, il mare di materia dentro; l'energia di `TB3` *(con l'assorbita)* contro quella di `TF3` *(il tick vivo non conserva `E` nella rampa)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL_B = 1e-10                 # ### Luca 21:52: il bilancio
BLOCCO = 1000.0
PARTENZE = "TS ~4000, F0 ~9500, TF3 ~16000"   # ### le partenze sparse gia' viste (Luca 09:00)
DERIVA_TICK = "TS: A3 di M +3.875e-12 per 1000 (ts_corsa.txt)"   # ### il bilancio non chiude meglio del tick (5.9)

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
    import _vuoto_vivo_B as V
    from solitone import carta_deriva as CD
    from solitone import carta_tf3_lunga as T3
    from solitone import corsa_accensione as CA
    for m in ("__init__", "bordo", "corsa_accensione", "carta_deriva", "carta_tf3_lunga"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, _vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("TB3: TF3 COL BORDO ASSORBENTE (Luca 21:52, 09:00, 09:26) CONTRO TF3 + TF3C E TS; TOLL_B %g BLOCCO %g" % (TOLL_B, BLOCCO))
    print("  le letture di Luca, scritte prima: (b1) non parte entro 30000, o resta sotto TF3 e TS: il moto veniva dal giro del toro; (b2) parte comunque, con velocita' e")
    print("  persistenza come TS / TF3 / F0: il moto e' del solitone, non della scatola; (b3) altro.")
    print("  ### TB3 risponde a <<il moto parte senza il rientro dal toro?>>, NON a <<quanto corre>>: dopo ~8 nodi la corsa si ferma per costruzione (l'arresto (i), Luca 09:26)")
    print("  ### le partenze gia' viste sono SPARSE (%s): con una corsa sola, una partenza tardiva NON basta a dire (b1)" % PARTENZE)
    print("=" * 130)
    rb, cb, _d, _a = CA.serie("TB3")
    if not rb:
        print("### TB3: NESSUN PEZZO")
        return 1
    _r3, c3, _d, _a = CA.serie("TF3")
    _rc, cc, _d, _a = CA.serie("TF3C")
    _rs, cs, _d, _a = CA.serie("TS")
    L = rb[0]["L"]
    b0 = rb[0]["bordo"]
    ult = rb[-1]
    esito("DEVE PASSARE: P0 il primo campione di TB3 e' quello di TF3 (per ed E, al bit)", cb[0]["per"] == c3[0]["per"] and cb[0]["E"] == c3[0]["E"], "t %d" % cb[0]["t"])
    esito("DEVE FALLIRE: P0-F il primo campione di TB3 e' quello di TS (per, al bit)", not cb[0]["per"] == cs[0]["per"], "w TB3 %.6f, TS %.6f" % (cb[0]["per"]["w"], cs[0]["per"]["w"]))
    esito("DEVE PASSARE: BR ogni pezzo: la stessa tabella di c(t) (sha), lo stesso g_max e R_A", all(r["bordo"]["sha_c"] == b0["sha_c"] and r["bordo"]["g_max"] == b0["g_max"] and r["bordo"]["R_A"] == b0["R_A"] for r in rb),
          "sha %s, g_max %g, R_A %g, omega %.17e" % (b0["sha_c"], b0["g_max"], b0["R_A"], b0["omega"]))
    tt = np.array([c["t"] for c in cb]) * s
    eM = np.array([(c["bordo"]["M"] + c["bordo"]["M_ass"]) / b0["M0"] - 1.0 for c in cb])
    eV = np.array([(c["bordo"]["V"] + c["bordo"]["V_ass"]) / b0["V0"] - 1.0 for c in cb])
    # ### BM (Luca 2026-11-04 18:31; il task history 5.12): il bilancio di TB3 MENO la deriva di M di TF3 + TF3C senza bordo agli stessi tick (E.totale.M, ciascuno
    # ### diviso per il SUO valore a t 0): la tolleranza applicata a cio' che aggiunge il bordo. Il BM vecchio (contro M0) resta stampato come numero, non come DEVE.
    print("  ### il bilancio M + assorbita = M0 da solo (il BM di prima, un numero): il peggiore %.3e a t %.1f; all'ultimo %.3e (%s)"
          % (float(np.abs(eM).max()), tt[int(np.argmax(np.abs(eM)))], eM[-1], DERIVA_TICK))
    mF = {c["t"]: c["E"]["totale"]["M"] for c in list(c3) + list(cc)}
    ok_t = all(c["t"] in mF for c in cb)
    dF = np.array([mF[c["t"]] / mF[0] - 1.0 if c["t"] in mF else np.nan for c in cb])
    dB = np.abs(eM - dF)
    esito("DEVE PASSARE: BM il bilancio M + assorbita di TB3 meno la deriva di M di TF3 + TF3C agli stessi tick entro %g a ogni campione" % TOLL_B, ok_t and float(np.nanmax(dB)) <= TOLL_B,
          "il peggiore %.3e a t %.1f; all'ultimo %+.3e (la deriva di TF3 all'ultimo %+.3e); campioni senza TF3: %d" % (float(np.nanmax(dB)), tt[int(np.nanargmax(dB))], eM[-1] - dF[-1], dF[-1],
                                                                                                        sum(1 for c in cb if c["t"] not in mF)))
    dB2 = np.abs(eM - 2.0 * dF)
    esito("DEVE FALLIRE: BM-F lo stesso confronto con la deriva di TF3 per 2, entro %g a ogni campione" % TOLL_B, not (ok_t and float(np.nanmax(dB2)) <= TOLL_B),
          "il peggiore %.3e a t %.1f" % (float(np.nanmax(dB2)), tt[int(np.nanargmax(dB2))]))
    esito("DEVE PASSARE: BV il bilancio V + assorbito = V0 entro %g a ogni campione" % TOLL_B, float(np.abs(eV).max()) <= TOLL_B, "il peggiore %.3e" % float(np.abs(eV).max()))
    esito("DEVE PASSARE: A4 TB3 il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rb), "")
    print("  TB3: %d pezzi, fino al tick %d di %d (tempo %.2f); ### L'ARRESTO: %s" % (len(rb), ult["t1"], ult["t_fine"], ult["t1"] * s,
          ult.get("fermata") or ("la fine a %g" % (ult["t_fine"] * s) if ult["t1"] >= ult["t_fine"] else "### NON FINITA")))
    t_fine = float(tt[-1])
    # ------------------------------------------------------------------ la corsa, contro TF3 + TF3C e TS, fino a dove arriva TB3
    tot = {}
    for nome, camp in (("TB3 (F3, il bordo)", cb), ("TF3 + TF3C (F3)", c3 + cc), ("TS (F3, simmetrizzata)", cs)):
        tq, X, ww, fl, al = T3.traiettoria(camp, L, s)
        m_ = tq <= t_fine
        tq, X, ww, fl, al = tq[m_], X[m_], ww[m_], fl[m_], al[m_]
        righe = CD.finestre(nome, tq, X, ww, fl, 0.0, t_fine + 1.0, BLOCCO, False)
        print("-" * 130)
        print("### %s: %d campioni fino a %.1f (la fine di TB3)" % (nome, len(tq), tq[-1]))
        print("  %-19s %-20s %-9s %-9s %-9s %-9s %-9s" % ("blocco", "X medio", "v/1000", "angolo", "cuore", "w", "alone"))
        for a, b, v, ang, wm, _amp, Xm in righe:
            m = (tq >= a) & (tq < b)
            print("   %7.0f .. %7.0f (%+8.3f, %+8.3f) %-9.3f %+9.2f %-9.5f %-9.4f %-9.5f" % (a, b, Xm[0], Xm[1], v, ang, float(fl[m].mean()), wm, float(al[m].mean())))
        vm = max(righe, key=lambda r: r[2])
        print("  la velocita' massima per blocco: %.3f per 1000 a %.0f .. %.0f (%+.2f gradi)" % (vm[2], vm[0], vm[1], vm[3]))
        T3.vaga_o_corre(nome, tq, X, righe)
        dX = X[-1] - X[0]
        tot[nome] = (float(math.hypot(*dX)), math.degrees(math.atan2(dX[1], dX[0])), float(tq[-1]), float(np.hypot(X[:, 0] - X[0, 0], X[:, 1] - X[0, 1]).max()))
    print("-" * 130)
    print("### LO SPOSTAMENTO (l'ultimo campione meno il primo, srotolato; e il massimo lungo la strada), fino a %.1f" % t_fine)
    for nome, (d, ang, t, dmax) in tot.items():
        print("  %-28s %8.3f nodi a %+8.2f gradi; il massimo %.3f (a tempo %.1f)" % (nome, d, ang, dmax, t))
    # ------------------------------------------------------------------ il bordo: la fase della fascia, i conti, il mare dentro
    print("-" * 130)
    print("### IL BORDO PER BLOCCO: la fase del vuoto nella fascia PRIMA dell'assorbimento (la lettura 5.3: <<forzatura>> se |a - 1| >= d medio, con arg a dello stesso segno per 3 blocchi")
    print("    consecutivi); M, V, E assorbite nel blocco (relative a M0, V0, E0); la materia dentro (g = 0) alla fine del blocco; l'energia di TB3 con l'assorbita contro TF3 senza bordo")
    eTF = {c["t"]: c["E"]["totale"]["tot"] for c in c3 + cc}
    print("  %-17s %-10s %-10s %-10s %-11s %-4s %-10s %-10s %-10s %-10s %-10s %-10s" % ("blocco", "d medio", "d max", "|a-1|", "arg a", "coe", "M ass", "V ass", "E ass", "M dentro", "E TB3", "E TF3"))
    serie_coe, prec = [], {"M_ass": 0.0, "V_ass": 0.0, "E_ass": 0.0}
    a = 0.0
    while a < t_fine:
        b = a + BLOCCO
        blk = [c for c in cb if a < c["t"] * s <= b and c["bordo"]["fase"] is not None]
        if not blk:
            break
        dm = float(np.mean([c["bordo"]["fase"]["d_medio"] for c in blk]))
        dx = float(np.max([c["bordo"]["fase"]["d_max"] for c in blk]))
        am = float(np.mean([c["bordo"]["fase"]["a_meno_1"] for c in blk]))
        ar = float(np.mean([c["bordo"]["fase"]["arg_a"] for c in blk]))
        coe = am >= dm
        serie_coe.append((coe, np.sign(ar)))
        x = blk[-1]["bordo"]
        eb = (x["E"] + x["E_ass"]) / b0["E0"] - 1.0
        et = (eTF[blk[-1]["t"]] / eTF[0] - 1.0) if blk[-1]["t"] in eTF else float("nan")
        print("   %6.0f .. %6.0f %-10.3e %-10.3e %-10.3e %+-11.3e %-4s %-10.3e %-10.3e %+-10.3e %-10.6f %+-10.3e %+-10.3e"
              % (a, b, dm, dx, am, ar, "SI" if coe else "no", (x["M_ass"] - prec["M_ass"]) / b0["M0"], (x["V_ass"] - prec["V_ass"]) / b0["V0"], (x["E_ass"] - prec["E_ass"]) / b0["E0"],
                 x["M_dentro"] / b0["M0"], eb, et))
        prec = x
        a = b
    forz = [i for i in range(len(serie_coe) - 2) if all(serie_coe[i + j][0] for j in range(3)) and len({serie_coe[i + j][1] for j in range(3)}) == 1]
    print("  ### LA LETTURA 5.3: blocchi coerenti (|a - 1| >= d medio) %d su %d; tre consecutivi coerenti con arg a dello stesso segno: %s"
          % (sum(1 for c_, _s in serie_coe if c_), len(serie_coe), ("SI, dal blocco %d: IL BORDO FORZA IL VUOTO" % forz[0]) if forz else "no: onde, non forzatura"))
    x = cb[-1]["bordo"]
    print("  ### all'ultimo campione: assorbite M %.6e (%.3e M0), V %.6e (%.3e V0), E %.6e (%.3e E0); la materia dentro %.6f M0, nella fascia %.3e M0"
          % (x["M_ass"], x["M_ass"] / b0["M0"], x["V_ass"], x["V_ass"] / b0["V0"], x["E_ass"], x["E_ass"] / b0["E0"], x["M_dentro"] / b0["M0"], x["M_fascia"] / b0["M0"]))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
