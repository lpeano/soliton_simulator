# -*- coding: utf-8 -*-
r"""**`D0'`: LA CORSA RUOTATA CONTRO L'IMMAGINE DI `TP1000`** *(Luca, le decisioni dopo `ae60cfb6`, (a); il task history `doc/TASK_HISTORY/2026-11-03_D0_ruotata_e_TS.md`)*
    python csv/solitone/carta_d0_confronto.py > doc/referti_l2/d0_confronto.txt
### **La previsione di Luca:** `D0R` e' l'immagine ruotata di `TP1000`; **scrivere da quando smettono di esserlo.** ### **`carta_d0`** *(il tick vivo commuta, `5.2e-15`)*: **la
previsione e' vera per costruzione fino all'arrotondamento**; qui si misura **quanto in fretta l'arrotondamento le separa.**
### **I DEVE:** `Z0` la partenza e il vuoto registrati di `D0R` sono quelli di `corsa_accensione.ruotata` ricalcolati *(lo sha)*; `Z0-F` *(deve fallire)* la partenza di `D0R` e' quella
di `TP1000` *(non ruotata)*; `A3` su `D0R`; `A4` il libro col `par`.
### **Le misure, NESSUNA SOGLIA DI «SEPARAZIONE»:** per ogni campione `d(t)`, la distanza sul toro fra il centro periodico di `D0R` e l'immagine `m2 - c` di quello di `TP1000`;
per blocco di `1000` il massimo di `d`; **il primo tempo in cui `d` supera ogni decade** *(`1e-14` .. `1e0`: una griglia dichiarata, non una soglia)*; agli stati *(`TM1000`, al bit
di `TP1000`)* lo scarto per chiave `|st_D0R - R st_TM1000| / |R st_TM1000|`; lo spostamento totale e la sua direzione contro quella ruotata di `TP1000`.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

BLOCCO = 1000.0
DECADI = tuple(10.0 ** k for k in range(-14, 1))   # ### la griglia dichiarata delle decadi (non una soglia)
LUCA = (1e-12, 1e-6, 1e-2)     # ### Luca dopo eaa5e3ec: quanto il sistema amplifica le differenze

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
    from solitone import carta_d0 as D0
    from solitone import carta_impulso as CI
    from solitone import corsa_accensione as CA
    from solitone import toro as TO
    for m in ("__init__", "accensione", "corsa_accensione", "carta_impulso", "carta_d0", "toro"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    A1, A2 = TO.vettori()
    print("=" * 130)
    print("D0': D0R CONTRO L'IMMAGINE RUOTATA DI TP1000 (Luca dopo ae60cfb6, (a)): %s (s %g); BLOCCO %g; DECADI 1e-14 .. 1e0" % (CA.NOME, s, BLOCCO))
    print("  la previsione di Luca: l'immagine ruotata di TP1000 (lo spostamento a +6.9 gradi da +A1); carta_d0: il tick vivo commuta (5.2e-15), la previsione e' vera per")
    print("  costruzione fino all'arrotondamento: qui QUANTO in fretta l'arrotondamento separa le due corse")
    print("=" * 130)
    rd, cd, _d, _a = CA.serie("D0R")
    rp, cp, _d, _a = CA.serie("TP1000")
    if not rd:
        print("### D0R: NESSUN PEZZO")
        return 1
    L = rd[0]["L"]
    m2 = tuple(rd[0]["ruotata"]["m2"])
    with V.scena(s, vuoto, V.EPS) as (_rec, z, phi0, pK):
        chiavi = [k for k, v in z["st"].items() if isinstance(v, np.ndarray)]
        salvato = {k: z["st"][k].copy() for k in chiavi}
        p0, _info = V.partenza(sol, z, phi0, pK, s)
        for k in chiavi:
            z["st"][k][...] = salvato[k]
        x_rot, m2b = CA.ruotata(z, salvato, p0)
        esito("DEVE PASSARE: Z0 la partenza e il vuoto registrati di D0R sono quelli di corsa_accensione.ruotata ricalcolati (lo sha; m2 uguale)",
              all(r["ruotata"]["sha_partenza"] == SFM.sha(x_rot["psi_h"]) and r["ruotata"]["sha_vuoto"] == SFM.sha(x_rot["phi_h"]) for r in rd) and tuple(m2b) == m2,
              "m2 %s; %d pezzi" % (m2, len(rd)))
        esito("DEVE FALLIRE: Z0-F la partenza di D0R e' quella di TP1000 (NON ruotata)", rd[0]["ruotata"]["sha_partenza"] != SFM.sha(p0), "")
        inc = z["inc"]
        _ok, dd = CI.assi(inc, L)
        v_ = np.arange(inc.n)
        dove = CI.rotazione(inc, L, dd, m2)
        nm = CI.nodo_di(L, m2[0] - v_ // L, m2[1] - v_ % L)
    t3 = np.array([c["t"] for c in cd]) * s
    okM, nM = AC.a3(t3, np.array([c["E"]["totale"]["M"] for c in cd]), cd[-1]["t"], V.TOLL_NORMA)
    okV, nV = AC.a3(t3, np.array([c["E"]["totale"]["V"] for c in cd]), cd[-1]["t"], V.TOLL_NORMA)
    esito("DEVE PASSARE: A3 D0R M e V (accensione.a3)", okM and okV, "M %s; V %s" % (nM, nV))
    esito("DEVE PASSARE: A4 D0R il libro col par della corsa", all(r.get("libro") == "col par della corsa" and r["eps"] == V.EPS for r in rd), "")
    ult = rd[-1]
    print("  D0R: %d pezzi, fino al tick %d di %d (tempo %.2f)%s" % (len(rd), ult["t1"], ult["t_fine"], ult["t1"] * s, "" if ult["t1"] >= ult["t_fine"] else " ### NON FINITA"))
    # ------------------------------------------------------------------ d(t): il centro contro l'immagine
    tp = {c["t"]: c for c in cp}
    comuni = [c for c in cd if c["t"] in tp]
    tt = np.array([c["t"] for c in comuni]) * s
    dist = []
    for c in comuni:
        q = tp[c["t"]]["per"]
        e1 = ((c["per"]["c1"] - (m2[0] - q["c1"]) + 0.5 * L) % L) - 0.5 * L
        e2 = ((c["per"]["c2"] - (m2[1] - q["c2"]) + 0.5 * L) % L) - 0.5 * L
        dist.append(float(np.hypot(*(e1 * A1 + e2 * A2))))
    dist = np.array(dist)
    print("-" * 130)
    print("### d(t) = |c_D0R - (m2 - c_TP1000)| sul toro (nodi), il centro periodico; %d campioni comuni fino a %.1f" % (len(tt), tt[-1]))
    print("  il primo tempo in cui d supera ogni decade:")
    for dec in DECADI:
        i = np.nonzero(dist > dec)[0]
        print("    d > %.0e: %s" % (dec, ("tempo %.2f (d %.3e)" % (tt[i[0]], dist[i[0]])) if len(i) else "mai"))
    tre = []
    for dec in LUCA:
        i = np.nonzero(dist > dec)[0]
        tre.append("%.0e: %s" % (dec, ("%.2f" % tt[i[0]]) if len(i) else "mai (fino a %.1f)" % tt[-1]))
    print("  ### LUCA dopo eaa5e3ec: il tempo a cui TP1000 e la sua immagine smettono di coincidere (il centro) entro %s" % "; ".join(tre))
    print("  per blocco: il massimo di d, il cuore, w, l'alone delle due corse")
    for a in np.arange(0.0, tt[-1] + 1e-9, BLOCCO):
        m = (tt >= a) & (tt < a + BLOCCO)
        if not m.any():
            continue
        idx = np.nonzero(m)[0]
        fd = np.mean([comuni[i]["per"]["f_liscia"] for i in idx])
        fp = np.mean([tp[comuni[i]["t"]]["per"]["f_liscia"] for i in idx])
        wd = np.mean([comuni[i]["per"]["w"] for i in idx])
        wp = np.mean([tp[comuni[i]["t"]]["per"]["w"] for i in idx])
        ad = np.mean([comuni[i]["per"]["alone"] for i in idx])
        ap = np.mean([tp[comuni[i]["t"]]["per"]["alone"] for i in idx])
        print("    %7.0f .. %7.0f  max d %.3e  cuore %.6f / %.6f  w %.5f / %.5f  alone %.6f / %.6f" % (a, a + BLOCCO, dist[m].max(), fd, fp, wd, wp, ad, ap))
    # ------------------------------------------------------------------ gli stati
    print("-" * 130)
    print("### GLI STATI: |st_D0R - R st_TM1000| / |R st_TM1000| per chiave (TM1000 al bit di TP1000)")
    for t in sorted({int(round(x / s)) for x in CA.STATI["D0R"]}):
        fd = os.path.join(CA.base_e("D0R"), "stati", "D0R", "D0R_stato_%06d.npz" % t)
        ft = os.path.join(CA.base_e("TM1000"), "stati", "TM1000", "TM1000_stato_%06d.npz" % t)
        if not (os.path.exists(fd) and os.path.exists(ft)):
            print("    t %d: manca %s" % (t, fd if not os.path.exists(fd) else ft))
            continue
        with np.load(fd) as a_, np.load(ft) as b_:
            xa = {k: a_[k] for k in chiavi}
            rb = D0.ruota({k: b_[k] for k in chiavi}, dove, nm, CI.SIGMA["sz"])
        sc = D0.scarti(xa, rb)
        print("    tempo %8.2f (tick %d): %s" % (t * s, t, {k: "%.3e" % v for k, v in sc.items()}))
    # ------------------------------------------------------------------ lo spostamento
    print("-" * 130)
    for nome, camp in (("D0R", cd), ("TP1000", cp)):
        c1 = np.array([c["per"]["c1"] for c in camp])
        c2 = np.array([c["per"]["c2"] for c in camp])
        u1 = np.sum(((np.diff(c1) + 0.5 * L) % L) - 0.5 * L)
        u2 = np.sum(((np.diff(c2) + 0.5 * L) % L) - 0.5 * L)
        X = u1 * A1 + u2 * A2
        print("  lo spostamento totale di %-7s (fino a %.1f): %.3f nodi a %+.2f gradi" % (nome, camp[-1]["t"] * s, math.hypot(*X), math.degrees(math.atan2(X[1], X[0]))))
    print("=" * 130)
    print("ESITO: %d/%d controlli passano; DEVE fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
