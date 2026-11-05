# -*- coding: utf-8 -*-
r"""**LA CORONA IN MOVIMENTO: LA FINESTRA FITTA E IL FLUSSO ATTRAVERSO GLI ANELLI** *(Luca `2026-11-04` `20:18`-`22:26`; il task history `doc/TASK_HISTORY/2026-11-05_forma_isotropia_corona.md`, 1.3)*
    python csv/solitone/carta_corona.py > doc/referti_l2/corona_tb3.txt
### **Solo lettura da `E:`** *(le mappe `float32` di `TB3`, una ogni `100` tick; lo sha1 dei file contro `doc/referti_l2/mappe_indice_TB3.txt`)*. ### **(a)** la finestra fitta: le istantanee con `t` da `T_FIN[0]`
a `T_FIN[1]` nel repo come `doc/referti_l2/campo_TB3/finestra_fitta.npz` *(`float16`, le chiavi delle mappe leggere; `dLambda` rispetto a `Lambda` a `t 0`)*. ### **(b)** il flusso: `M_in(r)` la massa entro
`r` dal centro per `r` in `RAGGI`, `Phi(r) = -(M_in(t_i+1) - M_in(t_i)) / dt`, con due centri dichiarati *(quello di ogni mappa, e quello FISSO della finestra)*; **dai `float32`, non dal file `float16`.**
### **I DEVE:** `CO-I` *(mio)* lo sha1 dei file usati = l'indice; `CO0` la massa di ogni istantanea della finestra *(`float32`)* = `M` del campione di `TB3` allo stesso tick entro `TOLL`; `CO0-F` *(deve fallire)*
contro il campione di `100` tick dopo, **solo se puo' fallire** *(se la massa cambia in `100` tick meno di `TOLL`, non si mette: dichiarato prima)*. **La parte (c)** *(la corrente e i vortici)* **e' ferma:**
su `E:` la fase di psi non c'e' *(`doc/referti_l2/campo_TB3/diag_e_tb3.txt`)*.
"""
import glob
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

T_FIN = (19250.0, 20750.0)     # ### Luca: 1500 unita' di tempo attorno a 20000
RAGGI = (22.0, 26.0, 30.0)     # ### Luca: gli anelli 22, 26, 30
TOLL = 1e-6                    # ### Luca: come F1 di campo_TB3
EPS32 = 2.0 ** -24             # ### l'arrotondamento relativo di un float32 (il limite dell'errore della somma: somma rho * EPS32)
DIR_REF = os.path.join(solitone.RADICE, "doc", "referti_l2")

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
    from solitone import campo as CP
    from solitone import carta_campo as CC
    from solitone import corsa_accensione as CA
    from solitone import mappe as MP
    from solitone import toro as TO
    for m in ("__init__", "campo", "carta_campo", "corsa_accensione", "mappe", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    _sol, _vuoto, s = V.CORSE[CA.NOME]
    print("=" * 130)
    print("LA CORONA IN MOVIMENTO (Luca 2026-11-04 20:18-22:26): TB3 da E: (float32, ogni %d tick); la finestra t %g .. %g; RAGGI %s; TOLL %g" % (MP.OGNI, T_FIN[0], T_FIN[1], RAGGI, TOLL))
    print("  ### la parte (c), la corrente e i vortici: FERMA (su E: la fase di psi non c'e'; diag_e_tb3.txt); se e quando salvarla lo decide Luca")
    print("=" * 130)
    idx = CC.indice("TB3")
    ff = sorted(glob.glob(os.path.join(MP.RADICE, "TB3", "TB3_*.npz")))
    t0_tick, t1_tick = T_FIN[0] / s, T_FIN[1] / s
    usati, T, RH, LA = [], [], [], []
    with np.load(ff[0]) as d:
        L0 = d["Lambda"][0].astype(np.float64)
        d1, d2, L = d["d1"], d["d2"], int(d["L"])
        assert int(d["t"][0]) == 0
    for f in ff:
        with np.load(f) as d:
            tt = d["t"]
            sel = [i for i in range(len(tt)) if t0_tick <= tt[i] <= t1_tick and int(tt[i]) not in T]
            if sel:
                usati.append(f)
                for i in sel:
                    T.append(int(tt[i]))
                    RH.append(d["rho"][i].astype(np.float64))
                    LA.append(d["Lambda"][i].astype(np.float64))
    o = np.argsort(T)
    T = np.array(T)[o]
    RH = np.array(RH)[o]
    LA = np.array(LA)[o]
    esito("DEVE PASSARE: CO-I lo sha1 dei file di E: usati = l'indice (mappe_indice_TB3.txt)", all(MP.sha1(f) == idx[f][1] for f in usati), "%d file: %s" % (len(usati), ", ".join(os.path.basename(f) for f in usati)))
    print("  la finestra: %d istantanee, tick %d .. %d (tempo %.1f .. %.1f), il passo %s tick" % (len(T), T[0], T[-1], T[0] * s, T[-1] * s, sorted(set(np.diff(T).tolist()))))
    # ------------------------------------------------------------------ CO0
    camp = {c["t"]: c["E"]["totale"]["M"] for c in CA.serie("TB3")[1]}
    M = RH.sum(axis=1)
    e0 = np.array([abs(M[i] / camp[int(T[i])] - 1.0) for i in range(len(T))])
    esito("DEVE PASSARE: CO0 la massa di ogni istantanea della finestra (float32) = M del campione di TB3 allo stesso tick, entro %g relativo" % TOLL, float(e0.max()) <= TOLL, "il peggiore %.2e" % e0.max())
    dm = np.array([abs(camp[int(t) + 100] / camp[int(t)] - 1.0) for t in T if int(t) + 100 in camp])
    print("  ### CO0-F (contro il campione di 100 tick dopo): la massa cambia in 100 tick fra %.2e e %.2e relativo" % (dm.min(), dm.max()))
    if dm.max() <= TOLL:
        print("  ### CO0-F NON SI METTE: la massa cambia in 100 tick meno di %g ovunque nella finestra, quindi non potrebbe fallire (dichiarato prima, task history 1.3)" % TOLL)
    else:
        eF = np.array([abs(M[i] / camp[int(T[i]) + 100] - 1.0) for i in range(len(T)) if int(T[i]) + 100 in camp])
        esito("DEVE FALLIRE: CO0-F la stessa massa contro il campione di 100 tick dopo, entro %g" % TOLL, not float(eF.max()) <= TOLL, "il peggiore %.2e" % eF.max())
    # ------------------------------------------------------------------ (a) la finestra fitta
    m1, m2 = d1.astype(int) + L // 2, d2.astype(int) + L // 2
    cen = np.array([TO.centro(r, m1, m2, L)[:2] for r in RH])
    out = os.path.join(DIR_REF, "campo_TB3", "finestra_fitta.npz")
    CC.salva(out, t=T, tempo=(T * s).astype(np.float32), rho=RH.astype(np.float16), dLambda=(LA - L0).astype(np.float16), centro=cen.astype(np.float32),
             d1=d1.astype(np.int16), d2=d2.astype(np.int16), L=np.int64(L), ogni=np.int64(1))
    b = os.path.getsize(out)
    with np.load(out) as d:
        e16 = float(np.max(np.abs(d["rho"].astype(np.float64).sum(axis=1) / M - 1.0)))
    print("  ### (a) %s: %d byte, %d mappe (una ogni %d tick = %g unita' di tempo); dLambda rispetto a Lambda a t 0 (min %.9f, max %.9f)"
          % (os.path.relpath(out, solitone.RADICE), b, len(T), MP.OGNI, MP.OGNI * s, L0.min(), L0.max()))
    print("  ### la massa del file float16 contro i float32: il peggiore %.2e relativo (un numero, non un DEVE: il file e' per il video)" % e16)
    # ------------------------------------------------------------------ (b) il flusso
    print("-" * 130)
    dt = MP.OGNI * s
    fisso = TO.centro(RH.mean(axis=0), m1, m2, L)[:2]
    print("### (b) IL FLUSSO Phi(r) = -(M_in(t_i+1) - M_in(t_i)) / %g, positivo verso l'esterno; il centro FISSO (la finestra mediata) (%.4f, %.4f); il centro di ogni mappa si muove di %.3f, %.3f (std degli indici)"
          % (dt, fisso[0], fisso[1], float(np.std(cen[:, 0])), float(np.std(cen[:, 1]))))
    print("  il rumore della somma float32: |errore di M_in| <= M_in * 2^-24, cioe' fino a %.3f; quello di una differenza fino al doppio" % (float(M.max()) * EPS32))
    neg = {}
    for nome_c, centri in (("ogni mappa", cen), ("fisso", np.array([fisso] * len(T)))):
        print("  il centro: %s" % nome_c)
        for R in RAGGI:
            Min = np.array([float(RH[i][CP.anelli(m1, m2, centri[i][0], centri[i][1], L, float("inf"))[1] < R].sum()) for i in range(len(T))])
            dM = np.diff(Min)
            Phi = -dM / dt
            rum = 2.0 * Min[:-1] * EPS32
            n_neg = int(np.sum((Phi < 0) & (np.abs(dM) > rum)))
            neg[(nome_c, R)] = n_neg
            print("    r %4g: M_in medio %.4f; Phi medio %+.4e +- %.4e (min %+.4e, max %+.4e); intervalli col flusso verso l'INTERNO oltre il rumore: %d su %d"
                  % (R, Min.mean(), Phi.mean(), Phi.std(), Phi.min(), Phi.max(), n_neg, len(Phi)))
    print("  ### LA LETTURA, scritta prima (task history 1.3): «la materia rientra» se a 26 e a 30 ci sono intervalli col flusso verso l'interno oltre il rumore IN ENTRAMBE le scelte del centro")
    rientra = all(neg[(c, R)] > 0 for c in ("ogni mappa", "fisso") for R in (26.0, 30.0))
    una = any(neg[(c, R)] > 0 for c in ("ogni mappa", "fisso") for R in (26.0, 30.0))
    print("  ### il caso: %s" % ("la materia RIENTRA (a 26 e 30, in entrambe le scelte del centro)" if rientra else
                              ("i negativi NON stanno in tutte e quattro (r 26, 30 per i due centri): %s; non si legge come rientro" % ", ".join("%s r %g: %d" % (c, R, neg[(c, R)]) for c in ("ogni mappa", "fisso") for R in (26.0, 30.0))
                               if una else "nessun intervallo col flusso verso l'interno oltre il rumore a 26 e 30")))
    print("  ### a 30 l'anello e' dentro la fascia del bordo (R_A 28)")
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
