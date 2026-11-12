# -*- coding: utf-8 -*-
r"""**LE LETTURE DELLE COMPONENTI E DEL VUOTO DI G1, RICALCOLATE DAGLI npz** *(Luca `2026-11-12` `16:10`; nessun tick, nessuna corsa del simulatore)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_g1_componenti_letture.py > doc/referti_l2/campo_g1_componenti/letture.txt

**Legge SOLO** `doc/referti_l2/campo_g1_componenti/g1_comp_gamma000.npz` e `g1_comp_gamma020.npz` *(`e5c4b62b`)*. **Le definizioni** *(Luca, dal guardiano)*:
- **gli anelli:** la distanza euclidea dal centro della materia *(il `centro` dell'npz, `toro.centro`)*, con `A1 = (1, 0)`, `A2 = (-1/2, sqrt 3/2)` e gli scarti periodici *(`toro.scarti`)*;
- **`sigma = 1`:** le componenti `c` dispari *(`c = 2 (2 k + e) + sigma`)*; **la direzione `k`:** le componenti `4 k .. 4 k + 3`;
- **`dphi = somma_j |phi_j|^2 - 6`** *(`phi2_rif` vale `1` per componente: controllato)*;
- **il deficit = somma di `max(-dphi, 0)`; l'eccesso = somma di `max(dphi, 0)`; il centro del buco = `toro.centro` del deficit.**
### **I DEVE** *(Luca)*: **i numeri del guardiano ricalcolati entro l'`1%` relativo** *(`0.05` assoluto per i centri)*; **DEVE FALLIRE:** **il centro del buco calcolato con la materia al posto del deficit** *(a `2000` tick, `gamma +0.02`: deve dare il centro della materia, non `42.8`)*.
**I valori del guardiano** *(il mandato delle `16:10`)* **e come li leggo** *(dichiarato)*: **i centri `c1` della materia e del buco a `0` e `2000`; il deficit entro `R < 20` dalla posizione INIZIALE a `0` e `2000`;
il deficit entro `R < 20` dalla posizione ATTUALE a `2000` *(«l'anello piu' debole»)*; **nel controllo il centro del buco fra `40.4` e `40.6` e il deficit entro `R < 20` da `2243` a `2600`.** **I valori dati come «circa»** *(le frazioni, `dphi` degli anelli)* **si stampano accanto, non sono DEVE.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

DIR = os.path.join(os.path.dirname(os.path.dirname(_QUI)), "doc", "referti_l2", "campo_g1_componenti")
ANELLI = ((0, 6), (6, 12), (12, 16), (16, 19), (19, 25), (30, 40))   # ### Luca
T_A = (0, 1000, 1800, 2000)                                           # ### Luca (a, b)
T_C = (0, 480, 1000, 1480, 1800, 2000)                                # ### Luca (c)
T_D = (0, 1000, 1800, 2000)                                           # ### Luca (d)
R_DEF, R_NORMA = 20.0, 12.0                                           # ### Luca (d)
TOLL_REL, TOLL_CEN = 0.01, 0.05                                       # ### Luca
GUARD = {("mat", 0.02, 0): 40.5, ("mat", 0.02, 2000): 65.9, ("buco", 0.02, 0): 40.4, ("buco", 0.02, 2000): 42.8,
         ("def_ini", 0.02, 0): 2159.0, ("def_ini", 0.02, 2000): 2791.0, ("def_att", 0.02, 2000): 1375.0,
         ("def_att", 0.0, 0): 2243.0, ("def_att", 0.0, 2000): 2600.0}   # ### il guardiano (16:00), il mandato delle 16:10
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


def main():
    import _presidio
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "toro.py"))
    _presidio.avvia(__file__)
    A1, A2 = TO.vettori()
    print("=" * 130)
    print("LE LETTURE DELLE COMPONENTI E DEL VUOTO DI G1 (Luca 2026-11-12 16:10), RICALCOLATE DAGLI npz di e5c4b62b; nessun tick; A1 %s, A2 %s" % (tuple(A1), tuple(A2)))
    print("=" * 130)
    print("  ### dal codice della scena (s5_caduta_solitone_componenti.py, come G1): ogni tick e' tick.percorri_tick con TUTTO l'ordine (len(composizione.ORDINE)):")
    print("  ### i pezzi del vuoto girano, phi EVOLVE con la legge piena; cs = s N per tutti i nodi; la forma (a) aggiunge una fase alla sola psi")
    ris = {}
    for g in (0.0, 0.02):
        f = os.path.join(DIR, "g1_comp_gamma%03d.npz" % int(round(g * 1000)))
        with np.load(f) as d:
            tt, P2, F2, cen, rif = d["t"], d["psi2"].astype(np.float64), d["phi2"].astype(np.float64), d["centro"], d["phi2_rif"]
        L = P2.shape[-1]
        assert float(rif.min()) == 1.0 == float(rif.max()), "phi2_rif NON e' 1 per componente"
        v = np.arange(L * L)
        i1, i2 = v // L, v % L

        def R_da(c1, c2):
            X = TO.scarti(i1, i2, c1, c2, L)
            return np.hypot(X[:, 0], X[:, 1])
        ris[g] = (tt, P2, F2, cen, L, i1, i2, R_da)
        print("### gamma %+.2f: %s, %d fotogrammi, L %d" % (g, os.path.basename(f), len(tt), L))
        # ------------------------------------------------ (a) sigma = 1 e le direzioni k per anello; (b) dphi per anello
        for t in T_A:
            j = int(np.where(tt == t)[0][0])
            R = R_da(*cen[j])
            p = P2[j].reshape(12, -1)
            dphi = F2[j].reshape(6, -1).sum(axis=0) - 6.0
            righe = []
            for a, b in ANELLI:
                m = (R >= a) & (R < b)
                tot = p[:, m].sum()
                s1 = p[1::2][:, m].sum() / tot
                kf = [p[4 * k:4 * k + 4][:, m].sum() / tot for k in range(3)]
                righe.append("R %2d-%2d: sigma1 %.4f, k %.3f %.3f %.3f, dphi %+.3f" % (a, b, s1, kf[0], kf[1], kf[2], float(dphi[m].mean())))
            print("  tick %4d (il centro %.3f %.3f): %s" % (t, cen[j][0], cen[j][1], "; ".join(righe)))
        print("  la norma per sigma: sigma0 %.5f, sigma1 %.5f (tick 0)" % (P2[0][0::2].sum() / P2[0].sum(), P2[0][1::2].sum() / P2[0].sum()))
        # ------------------------------------------------ (c) il buco
        for t in T_C:
            j = int(np.where(tt == t)[0][0])
            dphi = F2[j].reshape(6, -1).sum(axis=0) - 6.0
            de = np.maximum(-dphi, 0.0)
            cb = TO.centro(de, i1, i2, L)[:2]
            print("  tick %4d: il centro c1 della materia %.3f, del buco %.3f (c2 %.3f, %.3f); il deficit %.1f, l'eccesso %.1f; dphi minimo %+.3f"
                  % (t, cen[j][0], cb[0], cen[j][1], cb[1], de.sum(), np.maximum(dphi, 0.0).sum(), dphi.min()))
            ris[(g, "buco", t)] = cb[0]
            ris[(g, "mat", t)] = cen[j][0]
        # ------------------------------------------------ (d) il deficit dalla posizione iniziale e attuale; la norma entro R < 12 dalla iniziale
        for t in T_D:
            j = int(np.where(tt == t)[0][0])
            dphi = F2[j].reshape(6, -1).sum(axis=0) - 6.0
            de = np.maximum(-dphi, 0.0)
            Ri, Ra = R_da(*cen[0]), R_da(*cen[j])
            rho = P2[j].reshape(12, -1).sum(axis=0)
            ris[(g, "def_ini", t)] = float(de[Ri < R_DEF].sum())
            ris[(g, "def_att", t)] = float(de[Ra < R_DEF].sum())
            print("  tick %4d: il deficit entro R < %g dalla posizione INIZIALE %.1f, dall'ATTUALE %.1f; la norma entro R < %g dalla iniziale %.5f"
                  % (t, R_DEF, ris[(g, "def_ini", t)], ris[(g, "def_att", t)], R_NORMA, rho[Ri < R_NORMA].sum() / rho.sum()))
    print("-" * 130)
    print("### IL CONFRONTO COI NUMERI DEL GUARDIANO")
    for (che, g, t), gv in GUARD.items():
        cc = ris[(g, che, t)]
        cen_ = che in ("mat", "buco")
        ok = abs(cc - gv) <= TOLL_CEN if cen_ else abs(cc - gv) <= TOLL_REL * abs(gv)
        esito("%s, gamma %+.2f, tick %d: il guardiano %g, CC %.3f" % (che, g, t, gv, cc), ok, "la differenza %+.3f%s" % (cc - gv, "" if cen_ else " (%.2f%%)" % (100 * (cc - gv) / gv)))
    cb_ctrl = [ris[(0.0, "buco", t)] for t in T_C]
    esito("il controllo: il centro c1 del buco fra 40.4 e 40.6 (entro 0.05)", min(cb_ctrl) >= 40.35 and max(cb_ctrl) <= 40.65, "da %.3f a %.3f" % (min(cb_ctrl), max(cb_ctrl)))
    # ------------------------------------------------ DEVE FALLIRE: il centro «del buco» calcolato con la materia
    tt, P2, F2, cen, L, i1, i2, R_da = ris[0.02]
    rho = P2[-1].reshape(12, -1).sum(axis=0)
    cm = TO.centro(rho, i1, i2, L)[0]
    esito("il centro del buco calcolato con la MATERIA al posto del deficit = 42.8 entro 0.05 (gamma +0.02, tick 2000)", abs(cm - 42.8) <= TOLL_CEN, "%.3f (la materia)" % cm, deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
