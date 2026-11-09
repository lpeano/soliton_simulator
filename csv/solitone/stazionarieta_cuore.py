# -*- coding: utf-8 -*-
r"""**IL CUORE CHE BOCCIA SEMPRE: LA PROVA DEL CAMPIONAMENTO** *(Luca `2026-11-09` `12:02`; il task history `doc/TASK_HISTORY/2026-11-07_allungamenti_coppia_30000.md`, sez. `7.17`)*. [[PIANO-2D-3D]]

    python csv/solitone/stazionarieta_cuore.py > doc/referti_l2/stazionarieta_cuore.txt

**Il cuore** *(`M_dentro`)* **di `TB3` e `TBS`, con `W = 6 x 311` e `10 x 311`** *(`P` del cuore di `TB3`)*; **per `TBS` anche il ripiego `6000`, senza verdetto** *(il suo `P` non c'e')*.
**Il controllo positivo:** `ST-F-C` e `ST-R` di `stazionarieta_v3` coi due `W` sulla base. **Le letture:** `c1` *(passa: la finestra era corta)*, `c2` *(boccia: deriva; la pendenza e la vita)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

P_CUORE_TB3 = 311.0            # ### sez. 7.17 (il referto di f3dd15b1)
MULTIPLI = (6.0, 10.0)         # ### Luca 12:02
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


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    from solitone import stazionarieta as ST
    from solitone import stazionarieta_v3 as S3
    for m in ("corsa_accensione", "stazionarieta", "stazionarieta_v3"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    s = V.CORSE[CA.NOME][2]
    WW = [k * P_CUORE_TB3 for k in MULTIPLI]
    print("=" * 130)
    print("IL CUORE, LA PROVA DEL CAMPIONAMENTO (sez. 7.17): W %s (= %s x P %g del cuore di TB3); per TBS anche il ripiego %g, senza verdetto" % (WW, MULTIPLI, P_CUORE_TB3, ST.W_RIPIEGO))
    print("=" * 130)
    # ------------------------------------------------------------ il controllo positivo sulla base (le righe di stazionarieta_v3.main)
    ts = np.arange(0.0, 30000.0, 1.5)
    rg = np.random.default_rng(S3.SEME)
    e = rg.normal(size=len(ts))
    ar = np.empty(len(ts))
    ar[0] = e[0]
    for i_ in range(1, len(ts)):
        ar[i_] = S3.PHI_BASE * ar[i_ - 1] + e[i_]
    base = ar + S3.AMP_BASE * np.sin(2 * math.pi * ts / S3.P_BASE)
    t_c = np.arange(ST.PASSO_CONTROLLI, ts[-1] + 1e-9, ST.PASSO_CONTROLLI)
    for W in WW:
        _tx, rr = S3.lettura_w(ST, ts, {"x": base}, {"x": W}, t_c)
        ris = float(np.median([ST.FATTORE_DIFF * d["x"][2] for _T, _o, _f, d in rr]))
        txc, _r = S3.lettura_w(ST, ts, {"x": base + S3.DERIVA * ts}, {"x": W}, t_c)
        c = S3.FATT_R * ris / (2.0 * W)
        txa, _r = S3.lettura_w(ST, ts, {"x": base + c * ts * ts}, {"x": W}, t_c)
        print("  W %.0f: la risoluzione sulla base %.4e" % (W, ris))
        esito("ST-F-C a W %.0f: la deriva costante piu' la base, il regime raggiunto" % W, txc is not None, "da t %s" % txc)
        esito("ST-R a W %.0f: l'accelerazione a %g volte la risoluzione risulta nel regime" % (W, S3.FATT_R), txa is not None, "da t %s" % txa, deve=False)
    # ------------------------------------------------------------ il cuore
    for nome in ("TB3", "TBS"):
        print("-" * 130)
        t, ser = ST.serie_singolo(nome, s)
        x = ser["cuore"]
        t_c = np.arange(ST.PASSO_CONTROLLI, t[-1] + 1e-9, ST.PASSO_CONTROLLI)
        lista = WW + ([ST.W_RIPIEGO] if nome == "TBS" else [])
        for W in lista:
            t_x, righe = S3.lettura_w(ST, t, {"cuore": x}, {"cuore": W}, t_c)
            print("### %s, il cuore, W %.0f%s" % (nome, W, " (il ripiego, senza verdetto)" if W == ST.W_RIPIEGO else ""))
            print("    %s" % "  ".join("%.0f:%s(%.1f)" % (T, "ok" if d["cuore"][3] else "NO", abs(d["cuore"][1] - d["cuore"][0]) / (ST.FATTORE_DIFF * d["cuore"][2]) if d["cuore"][2] else float("inf")) for T, _o, _f, d in righe))
            sel = t >= t[-1] - W
            pd, pde = ST.pendenza(t[sel], x[sel])
            vita = x[-1] / abs(pd) if pd != 0 else float("inf")
            lett = ("c1: il regime raggiunto da t %.0f: la finestra era troppo corta" % t_x) if t_x is not None else "c2: il cuore DERIVA a 30000"
            if nome == "TBS":
                lett = "(senza verdetto: il P del cuore di TBS non c'e', la domanda a Luca) " + lett
            print("    LA LETTURA: %s; la pendenza nell'ultima finestra %+.4e +- %.1e per unita'; M_dentro %.4e; la VITA estrapolata del cuore %.3e unita' (una ESTRAPOLAZIONE)" % (lett, pd, pde, x[-1], vita))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
