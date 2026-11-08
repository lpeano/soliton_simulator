# -*- coding: utf-8 -*-
r"""**B1: IL BILANCIO LOCALE DI NORMA ED ENERGIA SU `TBS`** *(il task history `doc/TASK_HISTORY/2026-11-08_bilancio_locale_B1.md`; la proposta della sez. `11.2`
del task history `2026-11-07_u1_prototipo_verificato`)*. [[PIANO-2D-3D]]

    python csv/solitone/bilancio_b1.py > doc/referti_l2/bilancio_b1.txt

### **Lo stato:** `E:\soliton_simulator\libreria\TBS_100000_completo.npz` *(validato da `LIB1-0`)*; **`N = 100` tick col ciclo della corsa** *(`AC.tick`, poi `BO.assorbi`
con `c(t) F3`)*, **gli operatori di `mot.operatori` AVVOLTI in memoria e rimessi all'uscita** *(il nucleo non si tocca)*.
### **I DEVE:** `B1-0` *(i tick avvolti = `dopo_stato["100000"]` di `TBS`, al bit)*; `B1-n1` *(i pezzi per nodo conservano `M_k` e `V_k`)*, `B1-n2` *(gli spostamenti
conservano la norma dell'arco)*, **entro `N 6 eps max rho`** *(la forma di Luca)*; `B1-F` *(di Luca: un trasferimento a distanza imposto a mano: `B1-n1` lo vede)*.
### **`B1-e`, stampato:** quale pezzo cambia il TOTALE dell'energia; la sorgente dei pezzi per nodo per regione; l'oscillazione del totale.
### ⚠ **Il bilancio telescopico per pezzi si chiude PER COSTRUZIONE** *(il task history, premessa `3`)*: **il residuo «del tick meno flusso meno bordo» E' `B1-n1`, e si
stampa senza contarlo due volte.**
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
TICK0 = 100000                 # ### lo stato completo della libreria (12defa7b): t 15000
N_B1 = 100                     # ### = DOPO_STATO di corsa_accensione: B1-0 contro dopo_stato["100000"] (scelta di protocollo mia, dichiarata)
GRADO = 6                      # ### la forma di Luca: N 6 eps max rho (6 il grado dei triangoli)
EPS_F = 1e-6                   # ### B1-F: la frazione di M_i spostata a mano (mia, per un DEVE FALLIRE, dichiarata)
FILE_LIB = os.path.join("E:" + os.sep, "soliton_simulator", "libreria", "TBS_%06d_completo.npz" % TICK0)
D_ARCO = {"spostamento_trasporto": "psi", "spostamento_scalare": "phi"}   # ### i soli pezzi che spostano norma fra nodi (tick.OPERATORE)

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
    import _dove_va_la_materia as DV
    import _libro_dei_conti as LC
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    for m in ("__init__", "bordo", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr = CA.serie(CORSA)[0]
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    dopo = {}
    for r in rr:
        dopo.update(r.get("dopo_stato") or {})
    bor = rr[0]["bordo"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    eps = float(np.finfo(float).eps)
    print("=" * 130)
    print("B1, IL BILANCIO LOCALE (il task history 2026-11-08_bilancio_locale_B1): %s dallo stato completo %s, N %d tick col ciclo della corsa; la stima N %d eps max rho; EPS_F %g"
          % (CORSA, FILE_LIB, N_B1, GRADO, EPS_F))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            w_in = DC.forma(z, rec["larghezza"])[0]
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        e_K = P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, mot, par = z["st"], z["inc"], z["mot"], z["par"]
        nodo = np.asarray(inc.nodo)
        n, m = inc.n, inc.m
        L = int(z["L"])
        g_e, gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        fascia = gn > 0.0
        cuore = z["rr"] <= V.R_VICINO * w_in
        regioni = {"cuore": cuore & ~fascia, "fascia": fascia, "resto": ~cuore & ~fascia}
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def carica():
            with np.load(FILE_LIB) as d:
                assert int(d["t"]) == TICK0
                for k in chiavi:
                    st[k][...] = d[k]

        def per_nodo():
            M = np.bincount(nodo, weights=np.sum(np.abs(st["psi_h"]) ** 2, axis=1), minlength=n)
            Vn = np.bincount(nodo, weights=np.abs(st["phi_h"]) ** 2, minlength=n)
            return M, Vn

        def per_arco():
            return (np.sum(np.abs(st["psi_h"]) ** 2, axis=1).reshape(m, 2).sum(axis=1), (np.abs(st["phi_h"]) ** 2).reshape(m, 2).sum(axis=1))

        def tot():
            return LC.conti_per_nodo(inc, mot, st, e_K, V.LAM_ZERO, par)["tot"].copy()

        def nuovo_registro():
            return {"nodoM": np.zeros(n), "nodoV": np.zeros(n), "arcoM": np.zeros(m), "arcoV": np.zeros(m), "flussoM": np.zeros(n), "flussoV": np.zeros(n),
                    "bordoM": np.zeros(n), "bordoV": np.zeros(n), "tickM": np.zeros(n), "tickV": np.zeros(n), "dE": {}, "srcE": np.zeros(n), "arcE": np.zeros(n),
                    "bordoE": np.zeros(n), "Etot": [], "pezzi": {}}

        def misura_pezzo(reg, nome, fai):
            M0, V0 = per_nodo()
            a0M, a0V = per_arco()
            E0 = tot()
            out = fai()
            M1, V1 = per_nodo()
            a1M, a1V = per_arco()
            dE = tot() - E0
            reg["pezzi"][nome] = reg["pezzi"].get(nome, 0) + 1
            reg["dE"][nome] = reg["dE"].get(nome, 0.0) + float(np.sum(dE))
            if nome == "bordo":
                reg["bordoM"] += M1 - M0
                reg["bordoV"] += V1 - V0
                reg["bordoE"] += dE
            elif nome in D_ARCO:
                reg["flussoM"] += M1 - M0
                reg["flussoV"] += V1 - V0
                reg["arcoM"] += a1M - a0M
                reg["arcoV"] += a1V - a0V
                reg["arcE"] += dE
            else:
                reg["nodoM"] += M1 - M0
                reg["nodoV"] += V1 - V0
                reg["srcE"] += dE
            return out

        op = mot.operatori
        veri = dict(op)

        def avvolgi(reg):
            for nome, f in veri.items():
                def w(st_, par_, fr_, _f=f, _n=nome):
                    return misura_pezzo(reg, _n, lambda: _f(st_, par_, fr_))
                op[nome] = w

        def ciclo(reg, t):
            Mt0, Vt0 = per_nodo()
            AC.tick(z, t, K)
            misura_pezzo(reg, "bordo", lambda: BO.assorbi(st, g_e, BO.c_di(t, tab_c, K, omega) * phi_v))
            Mt1, Vt1 = per_nodo()
            reg["tickM"] += Mt1 - Mt0
            reg["tickV"] += Vt1 - Vt0
            reg["Etot"].append(float(np.sum(tot())))

        # ------------------------------------------------------------------ la corsa avvolta
        carica()
        esito("DEVE PASSARE: B1-R0 lo stato della libreria = lo stato di TBS registrato a %d (al bit, ogni chiave)" % TICK0, V.shas(z) == stati[TICK0]["sha"], os.path.basename(FILE_LIB))
        M_start, V_start = per_nodo()
        tolM = N_B1 * GRADO * eps * float(np.max(M_start))
        tolV = N_B1 * GRADO * eps * float(np.max(V_start))
        print("  la stima: N %d x %d x eps x max rho = %.3e (M), x max Lambda = %.3e (V); max rho %.6e, max Lambda %.6e; il cuore %d nodi, la fascia %d, il resto %d"
              % (N_B1, GRADO, tolM, tolV, float(np.max(M_start)), float(np.max(V_start)), int(regioni["cuore"].sum()), int(regioni["fascia"].sum()), int(regioni["resto"].sum())))
        reg = nuovo_registro()
        reg["Etot"].append(float(np.sum(tot())))
        try:
            avvolgi(reg)
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                for t in range(TICK0 + 1, TICK0 + N_B1 + 1):
                    ciclo(reg, t)
        finally:
            op.clear()
            op.update(veri)
        assert all(op[k] is veri[k] for k in veri), "mot.operatori rimessi"
        esito("DEVE PASSARE: B1-0 i %d tick AVVOLTI da %d = dopo_stato[%d] di TBS (al bit, ogni chiave): gli avvolgimenti sono trasparenti" % (N_B1, TICK0, TICK0),
              V.shas(z) == dopo[str(TICK0)], "i pezzi per tick %s" % {k: v // N_B1 for k, v in sorted(reg["pezzi"].items())})
        rn1M, rn1V = float(np.max(np.abs(reg["nodoM"]))), float(np.max(np.abs(reg["nodoV"])))
        rn2M, rn2V = float(np.max(np.abs(reg["arcoM"]))), float(np.max(np.abs(reg["arcoV"])))
        esito("DEVE PASSARE: B1-n1 i pezzi per nodo conservano M_k e V_k: max_k |somma Delta M_k| entro %.3e, |somma Delta V_k| entro %.3e" % (tolM, tolV),
              rn1M <= tolM and rn1V <= tolV, "M %.3e (%.3f della stima), V %.3e (%.3f)" % (rn1M, rn1M / tolM, rn1V, rn1V / tolV))
        esito("DEVE PASSARE: B1-n2 gli spostamenti conservano la norma dell'arco: max_a |somma Delta (capo 0 + capo 1)| entro %.3e (psi), %.3e (phi)" % (tolM, tolV),
              rn2M <= tolM and rn2V <= tolV, "psi %.3e (%.3f), phi %.3e (%.3f)" % (rn2M, rn2M / tolM, rn2V, rn2V / tolV))
        resM = reg["tickM"] - reg["flussoM"] - reg["bordoM"]
        resV = reg["tickV"] - reg["flussoV"] - reg["bordoV"]
        print("  il residuo del tick meno il flusso meno il bordo (= B1-n1, non contato due volte): max_k M %.3e, V %.3e; contro B1-n1: %.3e, %.3e"
              % (float(np.max(np.abs(resM))), float(np.max(np.abs(resV))), float(np.max(np.abs(resM - reg["nodoM"]))), float(np.max(np.abs(resV - reg["nodoV"])))))
        print("  il bordo: M_ass totale %.6e (somma per nodo, segno: tolto), V %.6e; il flusso per nodo: somma_k %.3e (M), %.3e (V) -- un flusso puro somma a zero"
              % (-float(np.sum(reg["bordoM"])), -float(np.sum(reg["bordoV"])), float(np.sum(reg["flussoM"])), float(np.sum(reg["flussoV"]))))
        # ------------------------------------------------------------------ B1-e
        Et = np.array(reg["Etot"])
        osc = float(np.max(Et) - np.min(Et))
        print("### B1-e L'ENERGIA (stampata, senza verdetto: la premessa 4): E_tot da %.9e a %.9e; l'oscillazione (max - min) sui %d tick %.3e" % (Et[0], Et[-1], N_B1, osc))
        for nome in sorted(reg["dE"]):
            print("    (e1) %-24s somma_k Delta tot_k sui %d tick %+.6e (%d chiamate; rapporto all'oscillazione %+.3f)" % (nome, N_B1, reg["dE"][nome], reg["pezzi"][nome], reg["dE"][nome] / osc if osc > 0 else float("nan")))
        for nome, msk in regioni.items():
            src = reg["srcE"][msk]
            print("    (e2) la sorgente dei pezzi per nodo, %-7s: max_k |.| %.3e, somma |.| %.3e, somma %+.3e; i pezzi d'arco: somma %+.3e; il bordo: somma %+.3e"
                  % (nome, float(np.max(np.abs(src))) if src.size else 0.0, float(np.sum(np.abs(src))), float(np.sum(src)), float(np.sum(reg["arcE"][msk])), float(np.sum(reg["bordoE"][msk]))))
        print("    (e3) max_k |sorgente| / oscillazione del totale %.3f; somma_k |sorgente| / oscillazione %.3f" % (float(np.max(np.abs(reg["srcE"]))) / osc, float(np.sum(np.abs(reg["srcE"]))) / osc))
        print("  ### LE DUE DIVISIONI D'ARCO (meta' e meta'; tutto al nodo di coda): NON FATTE -- vorrebbero per_nodo riscritto, una seconda fonte del libro dei conti (il task history, premessa 4): chiedo")
        # ------------------------------------------------------------------ B1-F
        carica()
        regF = nuovo_registro()
        Mf, _Vf = per_nodo()
        i_ = int(np.argmax(Mf))
        j_ = int(((i_ // L + L // 2) % L) * L + (i_ % L + L // 2) % L)
        assert Mf[j_] > 0.0, "il nodo lontano ha norma nulla: il trasferimento a mano non si scala"
        eF = EPS_F * float(Mf[i_])
        try:
            avvolgi(regF)
            with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
                ciclo(regF, TICK0 + 1)

                def a_mano():
                    Mi, _v = per_nodo()
                    st["psi_h"][nodo == i_] *= math.sqrt(1.0 - eF / Mi[i_])
                    st["psi_h"][nodo == j_] *= math.sqrt(1.0 + eF / Mi[j_])
                M0f = float(np.sum(per_nodo()[0]))
                misura_pezzo(regF, "a mano", a_mano)
                dMt = float(np.sum(per_nodo()[0])) - M0f
                ciclo(regF, TICK0 + 2)
        finally:
            op.clear()
            op.update(veri)
        tolF = 2 * GRADO * eps * float(np.max(Mf))
        rF = float(np.max(np.abs(regF["nodoM"])))
        print("  B1-F: %g di norma (EPS_F x M_i) dal nodo %d (il cuore, M %.6e) al nodo %d (agli antipodi, M %.6e) fra i tick %d e %d; il totale di M cambia di %.3e"
              % (eF, i_, float(Mf[i_]), j_, float(Mf[j_]), TICK0 + 1, TICK0 + 2, dMt))
        esito("DEVE FALLIRE: B1-F col trasferimento a mano B1-n1 passa: max_k |somma Delta M_k| entro la stima di 2 tick %.3e" % tolF, not rF <= tolF,
              "%.3e ai nodi %s" % (rF, sorted(int(x) for x in np.argsort(-np.abs(regF["nodoM"]))[:2])))
        assert all(op[k] is veri[k] for k in veri), "mot.operatori rimessi"
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
