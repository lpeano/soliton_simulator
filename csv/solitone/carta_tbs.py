# -*- coding: utf-8 -*-
r"""**`TBS`: LA PARTENZA SIMMETRIZZATA DI `TS` COL BORDO DI `TB3`, CONTRO `TS` E `TB3`** *(Luca `2026-11-04` `18:31`, `2026-11-05` `13:16`; il task history `doc/TASK_HISTORY/2026-11-05_TBS_simmetrizzata_col_bordo.md`)*
    python csv/solitone/carta_tbs.py > doc/referti_l2/tbs_corsa.txt
### **Le letture di Luca, scritte prima:** (t1) `TBS` non parte entro `30000`: due casi su due col bordo, il solitone isolato e' fermo; (t2) parte: il bordo non basta a fermare il moto, il caso di `TB3`
era di un seme fortunato; (t3) altro. ### **I DEVE:** `P0` il primo campione di `TBS` e' quello di `TS` *(`per` ed `E`, al bit)*; `P0-F` *(deve fallire)* e' quello di `TB3`; `BR` la tabella di `c(t)`,
`g_max`, `R_A` di ogni pezzo; `BM` il bilancio `M` + assorbita di `TBS` meno la deriva di `M` di `TS` agli stessi tick entro `TOLL_B`, `BM-F` *(deve fallire)* con la deriva per `2`; `BV`; `A4`;
`ST-L` *(mio)* ogni stato completo su `E:` si rilegge al bit *(gli sha registrati in corsa)*; `ST-M` *(Luca `13:16`)* lo stato ricaricato da' `M` *(la somma per nodi del bordo)* e il centro periodico *(`toro.centro`
su `EL.densita`, come il campione)* AL BIT del campione allo stesso tick; `ST-M-F` *(deve fallire)* contro il campione di `100` tick dopo.
### **Le misure:** l'arresto; a blocchi di `1000` velocita', direzione, cuore, `w`, alone di `TBS`, `TS`, `TB3` *(fino alla fine di `TBS`)*; vaga o corre; lo spostamento; **quando la simmetria si rompe, contro `TS`**;
la fase del vuoto nella fascia *(la lettura 5.3 di `TB3`)*; `M`, `V`, `E` assorbite per blocco, l'energia di `TBS` *(con l'assorbita)* contro `TS`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

TOLL_B = 1e-10                 # ### Luca 21:52: il bilancio (e 2026-11-04 18:31: contro il gemello senza bordo)
BLOCCO = 1000.0
PARTENZE = "TS ~4000, F0 ~9500, TF3 ~16000"   # ### le partenze sparse gia' viste (Luca 09:00)
SOGLIE_SIMM = (1e-12, 1e-6, 1e-2)             # ### Luca: quando la simmetria si rompe (come ts_corsa)

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


def primo_sopra(tt, xx, sg):
    i = np.flatnonzero(np.asarray(xx) > sg)
    return float(tt[i[0]]) if len(i) else None


def main(argv):
    del argv
    import _energia_del_legame as EL
    import _presidio
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import carta_deriva as CD
    from solitone import carta_tf3_lunga as T3
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "bordo", "corsa_accensione", "carta_deriva", "carta_tf3_lunga", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("TBS: LA PARTENZA SIMMETRIZZATA DI TS COL BORDO DI TB3 (Luca 2026-11-04 18:31, 2026-11-05 13:16) CONTRO TS E TB3; TOLL_B %g BLOCCO %g" % (TOLL_B, BLOCCO))
    print("  le letture di Luca, scritte prima: (t1) non parte entro 30000: due casi su due col bordo, il solitone isolato e' fermo; (t2) parte: il bordo non basta a fermare il")
    print("  moto, il caso di TB3 era di un seme fortunato e la lettura (b1) non regge da sola; (t3) altro.")
    print("  ### le due cautele di (b1) (Luca 18:31): una corsa sola per caso, e le partenze senza bordo erano SPARSE (%s); il bordo toglie INSIEME il rientro dal toro e l'alone" % PARTENZE)
    print("=" * 130)
    rb, cb, _d, _a = CA.serie("TBS")
    if not rb:
        print("### TBS: NESSUN PEZZO")
        return 1
    _rs, cs, _d, _a = CA.serie("TS")
    _r3, c3, _d, _a = CA.serie("TB3")
    L = rb[0]["L"]
    b0 = rb[0]["bordo"]
    ult = rb[-1]
    esito("DEVE PASSARE: P0 il primo campione di TBS e' quello di TS (per ed E, al bit)", cb[0]["per"] == cs[0]["per"] and cb[0]["E"] == cs[0]["E"], "t %d" % cb[0]["t"])
    esito("DEVE FALLIRE: P0-F il primo campione di TBS e' quello di TB3 (per, al bit)", not cb[0]["per"] == c3[0]["per"], "w TBS %.6f, TB3 %.6f" % (cb[0]["per"]["w"], c3[0]["per"]["w"]))
    esito("DEVE PASSARE: BR ogni pezzo: la stessa tabella di c(t) (sha), lo stesso g_max e R_A, e quelli di TB3", all(r["bordo"]["sha_c"] == b0["sha_c"] and r["bordo"]["g_max"] == b0["g_max"] and r["bordo"]["R_A"] == b0["R_A"] for r in rb)
          and b0["sha_c"] == _r3[0]["bordo"]["sha_c"] and b0["g_max"] == _r3[0]["bordo"]["g_max"], "sha %s, g_max %g, R_A %g" % (b0["sha_c"], b0["g_max"], b0["R_A"]))
    tt = np.array([c["t"] for c in cb]) * s
    eM = np.array([(c["bordo"]["M"] + c["bordo"]["M_ass"]) / b0["M0"] - 1.0 for c in cb])
    eV = np.array([(c["bordo"]["V"] + c["bordo"]["V_ass"]) / b0["V0"] - 1.0 for c in cb])
    print("  ### il bilancio M + assorbita = M0 da solo (un numero): il peggiore %.3e a t %.1f; all'ultimo %.3e" % (float(np.abs(eM).max()), tt[int(np.argmax(np.abs(eM)))], eM[-1]))
    mS = {c["t"]: c["E"]["totale"]["M"] for c in cs}
    ok_t = all(c["t"] in mS for c in cb)
    dS = np.array([mS[c["t"]] / mS[0] - 1.0 if c["t"] in mS else np.nan for c in cb])
    dB = np.abs(eM - dS)
    esito("DEVE PASSARE: BM il bilancio M + assorbita di TBS meno la deriva di M di TS agli stessi tick entro %g a ogni campione" % TOLL_B, ok_t and float(np.nanmax(dB)) <= TOLL_B,
          "il peggiore %.3e a t %.1f; la deriva di TS all'ultimo %+.3e; campioni senza TS: %d" % (float(np.nanmax(dB)), tt[int(np.nanargmax(dB))], dS[-1], sum(1 for c in cb if c["t"] not in mS)))
    dB2 = np.abs(eM - 2.0 * dS)
    esito("DEVE FALLIRE: BM-F lo stesso confronto con la deriva di TS per 2, entro %g a ogni campione" % TOLL_B, not (ok_t and float(np.nanmax(dB2)) <= TOLL_B),
          "il peggiore %.3e a t %.1f" % (float(np.nanmax(dB2)), tt[int(np.nanargmax(dB2))]))
    esito("DEVE PASSARE: BV il bilancio V + assorbito = V0 entro %g a ogni campione" % TOLL_B, float(np.abs(eV).max()) <= TOLL_B, "il peggiore %.3e" % float(np.abs(eV).max()))
    esito("DEVE PASSARE: A4 TBS il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rb), "")
    print("  TBS: %d pezzi, fino al tick %d di %d (tempo %.2f); ### L'ARRESTO: %s" % (len(rb), ult["t1"], ult["t_fine"], ult["t1"] * s,
          ult.get("fermata") or ("la fine a %g" % (ult["t_fine"] * s) if ult["t1"] >= ult["t_fine"] else "### NON FINITA")))
    t_fine = float(tt[-1])
    # ------------------------------------------------------------------ gli stati completi su E:
    per_t = {c["t"]: c for c in cb}
    stati = [x for r in rb for x in (r.get("stati") or [])]
    ok_l, ok_m, ok_f, righe_st = True, True, True, []
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
    attesi = len(CA.STATI["TBS"]) if ult["t1"] >= ult["t_fine"] else None
    esito("DEVE PASSARE: ST-L ogni stato completo su E: si rilegge al bit (gli sha di ogni chiave registrati in corsa)%s" % ("" if attesi is None else ", e sono %d" % attesi),
          bool(stati) and ok_l and (attesi is None or len(stati) == attesi), "%d stati, %d byte" % (len(stati), sum(r[4] for r in righe_st)))
    esito("DEVE PASSARE: ST-M lo stato ricaricato da' M (la somma per nodi del bordo) e il centro periodico AL BIT del campione allo stesso tick (Luca 13:16)", bool(stati) and ok_m,
          "; ".join("t %.0f %s" % (r[0] * s, "al bit" if r[2] else "### NO") for r in righe_st[:4]) + (" ..." if len(righe_st) > 4 else ""))
    esito("DEVE FALLIRE: ST-M-F lo stesso confronto col campione di 100 tick dopo", bool(stati) and ok_f, "%d stati, nessuno uguale al campione di 100 tick dopo" % len(righe_st) if ok_f else "### uno e' uguale")
    mm = [r.get("mappe") for r in rb if r.get("mappe")]
    print("  le mappe su E:: %d file, %d istantanee, %d byte" % (len(mm), sum(m["istantanee"] for m in mm), sum(m["byte"] for m in mm)))
    # ------------------------------------------------------------------ quando la simmetria si rompe: TBS contro TS
    print("-" * 130)
    print("### QUANDO LA SIMMETRIA SI ROMPE: |S x - c x| / |x| per psi_h (con sigma_z) e phi_h; il primo tempo sopra ogni soglia, TBS contro TS (Luca: %s)" % (SOGLIE_SIMM,))
    for chi in ("psi", "phi"):
        for nome, camp in (("TBS", cb), ("TS", cs)):
            tq = np.array([c["t"] for c in camp if "simm" in c]) * s
            xx = [c["simm"][chi] for c in camp if "simm" in c]
            def fmt(v, f):
                return (f % v) if v is not None else "mai"
            dec = " ".join("1e%d %s" % (e, fmt(primo_sopra(tq, xx, 10.0 ** e), "%.1f")) for e in range(-15, 0))
            soglie = "; ".join("%g: %s" % (sg, fmt(primo_sopra(tq, xx, sg), "%.2f")) for sg in SOGLIE_SIMM)
            print("  %-4s %-3s: %s; ogni decade: %s" % (chi, nome, soglie, dec))
    # ------------------------------------------------------------------ la corsa, contro TS e TB3, fino a dove arriva TBS
    tot = {}
    for nome, camp in (("TBS (F3, simm., il bordo)", cb), ("TS (F3, simmetrizzata)", cs), ("TB3 (F3, il bordo)", c3)):
        tq, X, ww, fl, al = T3.traiettoria(camp, L, s)
        m_ = tq <= t_fine
        tq, X, ww, fl, al = tq[m_], X[m_], ww[m_], fl[m_], al[m_]
        righe = CD.finestre(nome, tq, X, ww, fl, 0.0, t_fine + 1.0, BLOCCO, False)
        print("-" * 130)
        print("### %s: %d campioni fino a %.1f (la fine di TBS)" % (nome, len(tq), tq[-1]))
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
    print("### IL BORDO PER BLOCCO: la fase del vuoto nella fascia PRIMA dell'assorbimento (la lettura 5.3 di TB3: <<forzatura>> se |a - 1| >= d medio, con arg a dello stesso segno per 3")
    print("    blocchi consecutivi); M, V, E assorbite nel blocco (relative a M0, V0, E0); la materia dentro (g = 0) alla fine del blocco; l'energia di TBS con l'assorbita contro TS senza bordo")
    eTS = {c["t"]: c["E"]["totale"]["tot"] for c in cs}
    print("  %-17s %-10s %-10s %-10s %-11s %-4s %-10s %-10s %-10s %-10s %-10s %-10s" % ("blocco", "d medio", "d max", "|a-1|", "arg a", "coe", "M ass", "V ass", "E ass", "M dentro", "E TBS", "E TS"))
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
        et = (eTS[blk[-1]["t"]] / eTS[0] - 1.0) if blk[-1]["t"] in eTS else float("nan")
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
