# -*- coding: utf-8 -*-
r"""**LA LIBRERIA: GLI STATI COMPLETI, SENZA TAGLIO** *(Luca `2026-11-07` `19:37`; il task history `doc/TASK_HISTORY/2026-11-07_libreria_solitoni_cluster.md`, sez. `15`)*

    python csv/solitone/libreria_stati.py > doc/referti_l2/libreria_stati.txt

### **Per ciascuno dei sette tick di `TBS`** *(`100000 .. 160000`)*: **lo stato COMPLETO** *(tutte le chiavi di `z["st"]`, tutto il toro)* **piu' `D = phi - c(t) F3`, `c(t)` e il centro**,
su `E:\soliton_simulator\libreria\TBS_<tick>_completo.npz`; **il campione registrato dalla corsa a quel tick** *(il bordo e la forma)* **nell'indice**
`doc/referti_l2/libreria_solitoni/indice.json`. **I controlli:** `L0-S`, `R2-S`, `R2`, `LIB1-0`, `R2-F` *(DEVE FALLIRE)*, `LIB1-U`/`LIB1-U-F`, `LIB1-C` *(contro i centri REGISTRATI dalla corsa:
contro l'originale sarebbe zero per costruzione)*; poi `LIB1-P` *(la soglia derivata `t_max omega eps`, Luca `17:55`)* e `LIB1-P-F` *(mio: un tick sfasato)*.
### **Non applicabili** *(riguardano il taglio: Luca `19:37`)*: `LIB1-1`, `LIB1-F`, `L3`, `L3-F`, `LIB2`. **L'oggetto ritagliato resta nell'indice come «ritagliato, non validato».**
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"
TICK_LIB = tuple(range(100000, 160001, 10000))    # ### t 15000 .. 24000: sette (la sez. 2.1)
TOLL_C = 0.2                                      # ### LIB1-C (Luca 00:32): nodi
N_LIB1 = 2000                                     # ### la sez. 2.3
DOPO = 100                                        # ### corsa_accensione.DOPO_STATO: LIB1-0
N_R2 = 100                                        # ### R2: i tick dopo la rilettura (= DOPO: LIB1-0 dalla stessa ripartenza)
TOLL_U = 1e-12                                    # ### LIB1-U (la sez. 2.3)
EPS = float(np.finfo(float).eps)                  # ### LIB1-P (Luca 17:55): t_max omega eps
DIR_E = os.path.join("E:" + os.sep, "soliton_simulator", "libreria")
DIR_REPO = os.path.join(solitone.RADICE, "doc", "referti_l2", "libreria_solitoni")
NON_APPLICABILI = ("LIB1-1", "LIB1-F", "L3", "L3-F", "LIB2")
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota=""):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  %-118s %s   %s" % (che, "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def sha1_file(f):
    import hashlib
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import protetto as P
    from solitone import toro as TO
    for m in ("__init__", "toro", "bordo", "accensione", "corsa_accensione", "protetto"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr = CA.serie(CORSA)[0]
    camp = {c["t"]: c for r in rr for c in r["campioni"]}
    stati = {x["t"]: x for r in rr for x in (r.get("stati") or [])}
    dopo = {}
    for r in rr:
        dopo.update(r.get("dopo_stato") or {})
    bor = rr[0]["bordo"]
    K = int(round(CA.CORSE[CORSA][0] / s))
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab_c, omega = d["c"].copy(), float(d["omega"])
    print("=" * 130)
    print("LA LIBRERIA, GLI STATI COMPLETI SENZA TAGLIO (Luca 19:37): %s ai tick %s; R2 %d tick, LIB1-C %g nodi per %d tick, LIB1-U %g; il bordo c0 %s R_A %g g_max %g; K %d"
          % (CORSA, list(TICK_LIB), N_R2, TOLL_C, N_LIB1, TOLL_U, bor["c0"], bor["R_A"], bor["g_max"], K))
    print("### NON APPLICABILI (riguardano il taglio, Luca 19:37): %s -- nessun verdetto" % ", ".join(NON_APPLICABILI))
    print("=" * 130)
    os.makedirs(DIR_E, exist_ok=True)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        P.e_K(z)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, inc, L = z["st"], z["inc"], int(z["L"])
        nodo = np.asarray(inc.nodo)
        n = inc.n
        v_ = np.arange(n)
        m1, m2 = v_ // L, v_ % L
        g_e, _gn, _r = BO.g_estremita(z, bor["c0"][0], bor["c0"][1], bor["R_A"], bor["g_max"])
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))

        def rif(t):
            return BO.c_di(t, tab_c, K, omega) * phi_v

        def ciclo(t):
            """### Un tick della corsa: `AC.tick`, poi il bordo con `c(t) F3` *(le righe di `corsa_accensione`)*."""
            AC.tick(z, t, K)
            BO.assorbi(st, g_e, rif(t))

        def centro():
            r = np.zeros(n)
            np.add.at(r, nodo, np.sum(np.abs(st["psi_h"]) ** 2, axis=1))
            return np.array(TO.centro(r, m1, m2, L)[:2])

        def dist(cA, cB):
            A1, A2 = TO.vettori()
            q = ((np.asarray(cB) - np.asarray(cA) + 0.5 * L) % L) - 0.5 * L
            return float(np.hypot(*(q[0] * A1 + q[1] * A2)))

        def carica_corsa(t):
            x = stati[t]
            with np.load(x["file"]) as d:
                assert int(d["t"]) == t
                for k in chiavi:
                    st[k][...] = d[k]
            return V.shas(z) == x["sha"]

        def carica_lib(f, t, con_D=True):
            """### Dal file della libreria; `con_D` `False`: `phi = c(t) F3`, SENZA il disturbo del vuoto (`R2-F`)."""
            with np.load(f) as d:
                assert int(d["t"]) == t
                for k in chiavi:
                    st[k][...] = d[k]
                if not con_D:
                    st["phi_h"][...] = rif(t)

        indice_f = os.path.join(DIR_REPO, "indice.json")
        indice = json.load(open(indice_f, encoding="utf-8"))
        for o in indice.get("oggetti", []):
            o["stato"] = "ritagliato, non validato (Luca 2026-11-07 19:37: L3 non chiusa; il taglio rimandato ai cluster)"
        indice["stati_completi"] = []
        indice["stati_completi_nota"] = ("Luca 2026-11-07 19:37: gli stati COMPLETI, non tagliati (tutte le chiavi di z st, tutto il toro), piu' D = phi - c(t) F3, c(t) e il centro; "
                                         "il campione registrato dalla corsa a quel tick; R2 al bit; L3 non si applica")
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            for t in TICK_LIB:
                print("### IL TICK %d (t %g)" % (t, t * s))
                esito("DEVE PASSARE: L0-S lo stato di %s al tick %d ha gli sha del jsonl" % (CORSA, t), carica_corsa(t), os.path.basename(stati[t]["file"]))
                c0 = centro()
                ct = complex(BO.c_di(t, tab_c, K, omega))
                f = os.path.join(DIR_E, "%s_%06d_completo.npz" % (CORSA, t))
                np.savez(f + ".tmp.npz", D=st["phi_h"] - rif(t), c_t=np.array(ct), centro=c0, t=t, L=L, **{k: st[k] for k in chiavi})
                os.replace(f + ".tmp.npz", f)
                ogg = {"file": f, "byte": os.path.getsize(f), "sha1": sha1_file(f), "tick": t, "t": t * s, "sha_stato": stati[t]["sha"], "chiavi": chiavi,
                       "centro": [float(c0[0]), float(c0[1])], "c_t": [ct.real, ct.imag], "campione": camp.get(t)}
                indice["stati_completi"].append(ogg)
                print("  %s, %d byte, sha1 %s; le chiavi %s; il centro (%.4f, %.4f); c(t) %+.12f %+.12fi" % (os.path.basename(f), ogg["byte"], ogg["sha1"][:12], chiavi, c0[0], c0[1], ct.real, ct.imag))
                # ------------------------------------------------------ R2-S, R2, LIB1-0, R2-F
                assert sha1_file(f) == ogg["sha1"]
                carica_lib(f, t)
                esito("DEVE PASSARE: R2-S il file della libreria riletto ridà gli sha del jsonl", V.shas(z) == stati[t]["sha"], "")
                sh = []
                for con_D in (True, True, False):
                    carica_lib(f, t, con_D)
                    for u in range(t + 1, t + N_R2 + 1):
                        ciclo(u)
                    sh.append(V.shas(z))
                esito("DEVE PASSARE: R2 il file riletto e ripartito due volte per %d tick col ciclo della corsa: gli sha di ogni chiave coincidono al bit" % N_R2, sh[0] == sh[1], "%d chiavi" % len(sh[0]))
                esito("DEVE PASSARE: LIB1-0 la ripartenza dal file per %d tick ridà gli sha di dopo_stato della corsa al bit" % DOPO, sh[0] == dopo[str(t)], "")
                esito("DEVE FALLIRE: R2-F lo stesso SENZA il disturbo del vuoto (phi = c(t) F3): gli sha coincidono", not (sh[2] == sh[0]), "")
                # ------------------------------------------------------ LIB1-U, LIB1-U-F
                carica_lib(f, t)
                st0 = {k: st[k].copy() for k in chiavi}
                a = 0.7
                ciclo(t + 1)
                dopo_a = {k: st[k].copy() for k in ("psi_h", "phi_h")}
                for k in chiavi:
                    st[k][...] = st0[k]
                st["psi_h"] *= np.exp(1j * a)
                st["phi_h"] *= np.exp(1j * a)
                AC.tick(z, t + 1, K)
                BO.assorbi(st, g_e, rif(t + 1) * np.exp(1j * a))
                eU = max(float(np.max(np.abs(st[k] - dopo_a[k] * np.exp(1j * a)))) / float(np.max(np.abs(dopo_a[k]))) for k in ("psi_h", "phi_h"))
                for k in chiavi:
                    st[k][...] = st0[k]
                st["psi_h"] *= np.exp(1j * a)
                ciclo(t + 1)
                eUF = max(float(np.max(np.abs(st[k] - dopo_a[k] * np.exp(1j * a)))) / float(np.max(np.abs(dopo_a[k]))) for k in ("psi_h", "phi_h"))
                esito("DEVE PASSARE: LIB1-U la fase globale e^{i 0.7} su psi e phi (e sul vuoto di riferimento) commuta con un tick entro %g" % TOLL_U, eU <= TOLL_U, "%.3e" % eU)
                esito("DEVE FALLIRE: LIB1-U-F la fase solo su psi: entro %g" % TOLL_U, not (eUF <= TOLL_U), "%.3e" % eUF)
                # ------------------------------------------------------ LIB1-C contro i centri REGISTRATI dalla corsa
                carica_lib(f, t)
                d0 = dist(centro(), (camp[t]["per"]["c1"], camp[t]["per"]["c2"]))
                dc, manca = [], 0
                for j, u in enumerate(range(t + 1, t + N_LIB1 + 1)):
                    ciclo(u)
                    if u in camp:
                        dc.append(dist(centro(), (camp[u]["per"]["c1"], camp[u]["per"]["c2"])))
                    elif j % 10 == 9:
                        manca += 1
                print("  LIB1-C il controllo di scala: la distanza al tick %d fra il centro dal file e quello registrato %.3e nodi; %d confronti, %d campioni mancanti" % (t, d0, len(dc), manca))
                esito("DEVE PASSARE: LIB1-C la ripartenza dal file: la distanza dal centro registrato dalla corsa entro %g nodi per %d tick (ogni 10)" % (TOLL_C, N_LIB1),
                      len(dc) > 0 and max(dc) <= TOLL_C, "il massimo %.3e" % (max(dc) if dc else float("nan")))
            # ---------------------------------------------------------- LIB1-P, LIB1-P-F
            fasi = [complex(BO.c_di(t, tab_c, K, omega)) for t in TICK_LIB]
            arg = [math.atan2(x.imag, x.real) for x in fasi]
            dfa = max(abs(math.remainder(x - arg[0], 2 * math.pi)) for x in arg)
            lim_p = TICK_LIB[-1] * abs(omega) * EPS
            x1 = complex(BO.c_di(TICK_LIB[-1] + 1, tab_c, K, omega))
            dfF = abs(math.remainder(math.atan2(x1.imag, x1.real) - arg[0], 2 * math.pi))
            print("### LIB1: c(t) ai tick %s: le fasi %s; omega %.15f per tick" % (list(TICK_LIB), " ".join("%+.12f" % x for x in arg), omega))
            esito("DEVE PASSARE: LIB1-P tutti gli stati alla stessa fase di c(t) entro t_max omega eps = %.3e (Luca 17:55)" % lim_p, dfa <= lim_p, "%.3e" % dfa)
            esito("DEVE FALLIRE: LIB1-P-F lo stesso con l'ultimo tick sfasato di 1 (%d)" % (TICK_LIB[-1] + 1), not (max(dfa, dfF) <= lim_p), "%.3e" % dfF)
        with open(indice_f, "w", encoding="utf-8", newline="\n") as h:
            json.dump(indice, h, ensure_ascii=False, indent=1)
        print("### L'INDICE %s: %d stati completi; l'oggetto ritagliato marcato «ritagliato, non validato»" % (os.path.relpath(indice_f, solitone.RADICE), len(indice["stati_completi"])))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
