# -*- coding: utf-8 -*-
r"""**I DUE POLI DEL CAMPO ATTORNO AL SOLITONE: `F0` CONTRO `F3`** *(Luca, `2026-11-03` `19:30`, nel mandato delle `19:34`; il task history `doc/TASK_HISTORY/2026-11-03_TM3_campo_F3.md`)*
    python csv/solitone/carta_poli.py > doc/referti_l2/poli_campo.txt
### **Dalle mappe leggere NEL REPO** *(`doc/referti_l2/campo_<corsa>/mappe_leggere.npz`, `float16`; nessun accesso a `E:`)*: `TM1000` *(`F0`)* e, quando c'e', `TM3` *(`F3`)*. Per ogni mappa,
entro `R_POLI` nodi dal centro periodico salvato *(l'immagine piu' vicina)*, `campo.multipoli` di `rho` e di `Lambda - Lambda(t 0)`: l'asse e il modulo relativo del dipolo e del quadrupolo.
### **Un FALSO-ZERO dichiarato:** il dipolo di `rho` attorno al suo centro periodico e' quasi nullo per costruzione. ### **Le letture di Luca, scritte prima:** (p1) su `F3` il quadrupolo
sparisce o cambia asse: i due poli li crea la freccia del vuoto; (p2) su `F3` resta a `-30` gradi: li crea la partenza asimmetrica *(`+58` gradi, `ae60cfb6`)*; (p3) altro.
### **I DEVE:** `P0` il centro salvato e' quello della `rho` `float16` della mappa *(entro `TOLL_C` nodi)*; `P0-F` *(deve fallire)* lo stesso con la `rho` spostata di mezzo lato.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

R_POLI = 14.0                  # ### Luca 19:30: entro 14 nodi dal centro periodico
BLOCCO = 500.0                 # ### come la tabella della portata
TOLL_C = 1e-2                  # ### P0: il centro dalla rho float16 contro il salvato (nodi; float16 ~1e-3 relativo)
CORSE = (("TM1000", "F0"), ("TM3", "F3"))
DIR = os.path.join(solitone.RADICE, "doc", "referti_l2")

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


def dist_indici(a, b, L):
    """### **La distanza sul toro fra due centri dati come INDICI** *(`(c1, c2)`)*, con l'immagine piu' vicina."""
    from solitone import toro as TO
    A1, A2 = TO.vettori()
    d = [((float(x) - float(y) + 0.5 * L) % L) - 0.5 * L for x, y in zip(a, b)]
    D = TO.piu_vicina((d[0] * A1 + d[1] * A2)[None, :], L)
    return float(np.hypot(D[0, 0], D[0, 1]))


def main(argv):
    del argv
    import _presidio
    from solitone import campo as CP
    from solitone import toro as TO
    for m in ("__init__", "toro", "campo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("I DUE POLI DEL CAMPO (Luca 19:30 / 19:34): R_POLI %g BLOCCO %g TOLL_C %g; CORSE %s" % (R_POLI, BLOCCO, TOLL_C, CORSE))
    print("  le definizioni (campo.multipoli, mie, dichiarate): il dipolo sum f D (l'asse atan2, il relativo |p| / sum |f||D|); il quadrupolo sum f (Dx + i Dy)^2 (l'asse arg / 2,")
    print("  modulo 180; il relativo |q| / sum |f||D|^2: 0 isotropo, 1 una retta). ### il dipolo di rho attorno al suo centro e' un FALSO-ZERO (dichiarato)")
    print("=" * 130)
    for corsa, vuoto in CORSE:
        f = os.path.join(DIR, "campo_%s" % corsa, "mappe_leggere.npz")
        print("-" * 130)
        if not os.path.exists(f):
            print("### %s (%s): le mappe leggere non ci sono ancora (%s)" % (corsa, vuoto, f))
            continue
        with np.load(f) as d:
            L = int(d["L"])
            m1, m2 = d["d1"].astype(int) + L // 2, d["d2"].astype(int) + L // 2
            T, RH, DL, CE = d["tempo"], d["rho"], d["dLambda"], d["centro"]
        print("### %s (%s): %d mappe da %s, fino a %.1f" % (corsa, vuoto, len(T), f, T[-1]))
        scarto = 0.0
        for i in range(len(T)):
            c1, c2, _x, _y = TO.centro(RH[i].astype(np.float64), m1, m2, L)
            scarto = max(scarto, dist_indici((c1, c2), CE[i], L))
        esito("DEVE PASSARE: P0 %s il centro salvato e' quello della rho float16 di ogni mappa (entro %g nodi)" % (corsa, TOLL_C), scarto <= TOLL_C, "il peggiore %.3e" % scarto)
        sp = np.empty_like(RH[1])
        sp[((m1 + L // 2) % L) * L + m2] = RH[1]
        c1, c2, _x, _y = TO.centro(sp.astype(np.float64), m1, m2, L)
        d_f = dist_indici((c1, c2), CE[1], L)
        esito("DEVE FALLIRE: P0-F %s la rho della seconda mappa spostata di mezzo lato: il centro e' il salvato entro %g" % (corsa, TOLL_C), not d_f <= TOLL_C, "%.3e nodi" % d_f)
        print("  %-9s %-26s %-26s %-26s %-26s" % ("tempo", "rho: quadrupolo asse/rel", "dLambda: dipolo asse/rel", "dLambda: quadrupolo asse/rel", "rho: dipolo rel (falso-zero)"))
        tab = []
        for i in range(len(T)):
            D = TO.scarti(m1, m2, CE[i][0], CE[i][1], L)
            pr = CP.multipoli(RH[i].astype(np.float64), D, R_POLI)
            pl = CP.multipoli(DL[i].astype(np.float64), D, R_POLI)
            tab.append((float(T[i]), pr, pl))
            print("  %9.2f %+8.2f / %.3e      %+8.2f / %.3e      %+8.2f / %.3e      %.3e" % (T[i], pr["q_asse"], pr["q_rel"], pl["p_asse"], pl["p_rel"], pl["q_asse"], pl["q_rel"], pr["p_rel"]))
        print("  ### a blocchi di %g: l'asse MEDIO del quadrupolo (la media di e^{2 i asse}, pesata col modulo relativo) e la sua coerenza |media| (1 = l'asse fermo)" % BLOCCO)
        for a in np.arange(0.0, T[-1] + 1e-9, BLOCCO):
            sel = [x for x in tab if a <= x[0] < a + BLOCCO]
            if not sel:
                continue
            riga = []
            for che, k in (("rho", 1), ("dLambda", 2)):
                z = np.array([x[k]["q_rel"] * np.exp(2j * math.radians(x[k]["q_asse"])) for x in sel])
                zm = z.mean()
                co = abs(zm) / np.mean(np.abs(z)) if np.mean(np.abs(z)) > 0 else float("nan")
                riga.append("%s %+7.2f (coerenza %.3f)" % (che, 0.5 * math.degrees(math.atan2(zm.imag, zm.real)), co))
            print("    %7.0f .. %7.0f (%2d mappe)  %s" % (a, a + BLOCCO, len(sel), "   ".join(riga)))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
