# -*- coding: utf-8 -*-
r"""**B1 (iii), IL CONTROLLO DEL RACCORDO PRIMA DEL TORO `L 162`** *(sul ramo laterale; Luca `2026-11-10` `13:42`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `27.8`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/b1_raccordo.py > doc/referti_l2/b1_iii_l162.txt

**Lo stato di `TBS` a `10000`** *(il blocco `81 x 81`)* **messo in un toro `L 162`, spostato di `O = 40` nodi su tutti e due gli indici** *(il centro `40.5` va a `80.5`; F3 ha periodo `1` nodo, lo spostamento non conta)*, **riempito con `c(10000) F3`**
*(`bordo.c_di`, la tabella `fase_F3.npz`)*. **Gli archi del blocco che non avvolgono il toro `81` portano lo stato; gli altri, il riempimento.** **IL SALTO:** `max |phi - c F3|` **sulle estremita' degli archi del blocco
che toccano un nodo del suo orlo** *(`m1` o `m2` in `{0, 80}`)*, **e `max |psi|` sugli stessi.** **Oltre `1e-12`: (iii) si salta** *(Luca)*. **Il controllo positivo:** lo stesso conto sullo stato a `t 0` *(prima di ogni assorbimento)*.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

L_GRANDE = 162                 # ### Luca: il toro L 162
O = 40                         # ### lo spostamento del blocco (dichiarato: il centro 40.5 -> 80.5)
TOLL = 1e-12                   # ### Luca: il salto oltre 1e-12, (iii) si salta
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota="", deve=True):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-104s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:104], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()
    return buono


def salto(phi81, psi81, nodo81, L81, nodo162, F3g, c):
    """### **Il blocco nel toro grande:** `(salto di phi sull'orlo, max |psi| sull'orlo, archi portati, archi dell'orlo)`."""
    m81 = nodo81.reshape(-1, 2)
    i, j = m81[:, 0], m81[:, 1]
    a1, a2, b1, b2 = i // L81, i % L81, j // L81, j % L81
    dentro = (np.abs(b1 - a1) <= 1) & (np.abs(b2 - a2) <= 1)          # ### gli archi che non avvolgono il toro 81
    I = (a1 + O) * L_GRANDE + (a2 + O)
    J = (b1 + O) * L_GRANDE + (b2 + O)
    g = nodo162.reshape(-1, 2)
    idx = {(int(p), int(q)): k for k, (p, q) in enumerate(g)}
    arch = np.array([idx.get((int(p), int(q)), -1) for p, q in zip(I, J)])
    assert np.all(arch[dentro] >= 0), "un arco del blocco NON ha il suo arco nel toro grande con lo stesso verso"
    orlo = dentro & ((a1 == 0) | (a1 == L81 - 1) | (a2 == 0) | (a2 == L81 - 1) | (b1 == 0) | (b1 == L81 - 1) | (b2 == 0) | (b2 == L81 - 1))
    e81 = np.concatenate([2 * np.flatnonzero(orlo), 2 * np.flatnonzero(orlo) + 1])
    e162 = np.concatenate([2 * arch[orlo], 2 * arch[orlo] + 1])
    sp = float(np.max(np.abs(phi81[e81] - c * F3g[e162])))
    ss = float(np.max(np.abs(psi81[e81])))
    return sp, ss, int(np.sum(dentro)), int(np.sum(orlo))


def main():
    import _presidio
    import _solitone_dal_fondo as SD
    import _stato_fermo as SFM
    import _vuoto_vivo_B as V
    from solitone import bordo as BO
    from solitone import carta_punto_fisso as CPF
    from solitone import carta_statiche as CS
    from solitone import corsa_accensione as CA
    for m in ("__init__", "bordo", "carta_statiche", "corsa_accensione", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    print("=" * 130)
    print("B1 (iii), IL RACCORDO (sez. 27.8): lo stato di %s nel toro L %d, spostato di %d; il riempimento c(t) F3 (fase_F3.npz, K %d, omega %.17g); TOLL %g" % (CPF.CORSA, L_GRANDE, O, K, omega, TOLL))
    print("=" * 130)
    letti = {}
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (_rec, z, _phi0, _pK):
        L81 = z["L"]
        nodo81 = np.asarray(z["inc"].nodo).copy()
        for t in (0, CPF.TICK_D4):
            xs = stati[t]
            with np.load(xs["file"]) as d:
                ph, ps = d["phi_h"].copy(), d["psi_h"].copy()
            assert SFM.sha(ph) == xs["sha"]["phi_h"] and SFM.sha(ps) == xs["sha"]["psi_h"], "lo stato NON e' quello registrato"
            letti[t] = (ph, ps)
            print("### lo stato a t %d: %s (sha di phi_h e psi_h come registrati)" % (t, os.path.basename(xs["file"])))
    with CS.scena_con(V.N, L_GRANDE), V.scena(s, vuoto, V.EPS) as (_rec, zg, _phi0, _pK):
        assert zg["L"] == L_GRANDE
        nodo162 = np.asarray(zg["inc"].nodo).copy()
        F3g = SD.fondo_con_fasi(zg["inc"], L_GRANDE, tuple(dict(SD.FASI)["F3"]))
    ris = {}
    for t in (0, CPF.TICK_D4):
        c = BO.c_di(t, tab, K, omega)
        sp, ss, nd, no = salto(letti[t][0], letti[t][1], nodo81, L81, nodo162, F3g, c)
        ris[t] = sp
        print("  t %5d: c(t) %+.12f %+.12fi; %d archi del blocco portati, %d toccano l'orlo; IL SALTO max|phi - c F3| sull'orlo %.3e; max|psi| sull'orlo %.3e" % (t, c.real, c.imag, nd, no, sp, ss))
    esito("il controllo positivo: a t 0 (prima di ogni assorbimento) il salto sull'orlo entro %g" % TOLL, ris[0] <= TOLL, "%.3e" % ris[0])
    print("-" * 130)
    if ris[CPF.TICK_D4] > TOLL:
        print("  ### IL SALTO a t %d e' %.3e, oltre %g: (iii) SI SALTA (Luca), dichiarato" % (CPF.TICK_D4, ris[CPF.TICK_D4], TOLL))
    else:
        print("  IL RACCORDO REGGE a t %d (%.3e <= %g): (iii) si puo' fare (la corsa, in un commit a se')" % (CPF.TICK_D4, ris[CPF.TICK_D4], TOLL))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
