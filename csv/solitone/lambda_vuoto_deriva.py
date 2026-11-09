# -*- coding: utf-8 -*-
r"""**T1, LA DERIVA DI `Lambda` DEL VUOTO A `cs` SPENTO** *(sul ramo laterale; Luca `2026-11-09` `20:13`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `23`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/lambda_vuoto_deriva.py > doc/referti_l2/lambda_vuoto_deriva.txt

**Il vuoto F3 da solo** *(la scena di `carta_punto_fisso`, `psi = 0`, `phi` = il vuoto della corsa)*, **`mot.lambda_c = None`** *(`cs` spento)*, **`1000` tick di `tick.tick`.**
**A ogni tick, per nodo, `Delta Lambda` in valore e in ulp; la deriva cumulata ai tick `1`, `10`, `100`, `1000`; la pendenza in log-log della rms fra `10` e `1000`.**
**T1-F** *(DEVE FALLIRE)*: **in una seconda corsa, `Lambda` di un nodo spostato di `1e-12` al tick `500`; «la misura non lo vede».** **Le letture:** `v1` / `v2` *(limitata, passeggiata)* / `v3`.
"""
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_TICK = 1000                  # ### sez. 23
T_INIEZIONE = 500              # ### sez. 23
DELTA_L = 1e-12                # ### sez. 23 (Luca)
TICK_STAMPA = (1, 10, 100, 1000)
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


def corsa(st, mot, par, foto, iniezione):
    import tick as TK
    for k, v in foto.items():
        st[k][...] = v
    mot.lambda_c = None
    L = [mot.densita_vuoto(st).copy()]
    for t in range(1, N_TICK + 1):
        if iniezione and t == T_INIEZIONE:
            nodo0 = mot.inc.nodo == 0
            st["phi_h"][nodo0] *= np.sqrt(1.0 + DELTA_L / L[-1][0])
        TK.tick(st, mot, par)
        L.append(mot.densita_vuoto(st).copy())
    return np.array(L)


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    from solitone import corsa_accensione as CA
    for m in ("__init__", "corsa_accensione", "carta_punto_fisso"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    t00 = time.time()
    print("=" * 130)
    print("T1, LA DERIVA DI Lambda DEL VUOTO A cs SPENTO (sez. 23): il vuoto F3 della corsa %s, %d tick; T1-F: %g su un nodo al tick %d" % (CPF.CORSA, N_TICK, DELTA_L, T_INIEZIONE))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CPF.CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CPF.CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par = z["st"], z["mot"], z["par"]
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        foto = {k: v.copy() for k, v in st.items() if isinstance(v, np.ndarray)}
        print("### la scena: %d nodi; mot.cs %s; Lambda all'inizio min %.17g max %.17g" % (mot.inc.n, "None" if mot.cs is None else "array (min %.6g, max %.6g)" % (float(np.min(mot.cs)), float(np.max(mot.cs))), float(mot.densita_vuoto(st).min()), float(mot.densita_vuoto(st).max())))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            L = corsa(st, mot, par, foto, False)
            Li = corsa(st, mot, par, foto, True)
    ulp = np.spacing(np.abs(L[0]))
    dL = np.abs(np.diff(L, axis=0))
    print("  |Delta Lambda| per tick (tutti i nodi, tutti i tick): max %.3e (%.1f ulp), media %.3e (%.2f ulp); i tick con Delta Lambda = 0 ovunque: %d su %d"
          % (float(dL.max()), float((dL / ulp).max()), float(dL.mean()), float((dL / ulp).mean()), int(np.sum(np.all(dL == 0, axis=1))), N_TICK))
    D = L - L[0]
    rms = []
    for t in TICK_STAMPA:
        r_ = float(np.sqrt(np.mean(D[t] ** 2)))
        rms.append(r_)
        print("  la deriva Lambda(t) - Lambda(0) al tick %4d: max %.3e (%.1f ulp), media %+.3e, rms %.3e" % (t, float(np.abs(D[t]).max()), float((np.abs(D[t]) / ulp).max()), float(D[t].mean()), r_))
    tt = np.arange(10, N_TICK + 1)
    rr = np.sqrt(np.mean(D[tt] ** 2, axis=1))
    if np.all(rr > 0):
        pend = float(np.polyfit(np.log(tt), np.log(rr), 1)[0])
    else:
        pend = float("nan")
    print("  la pendenza in log-log della rms della deriva fra t 10 e t %d: %s" % (N_TICK, "%.3f" % pend if pend == pend else "non definita (rms = 0 in qualche tick)"))
    vis = float(np.max(np.abs(Li[T_INIEZIONE:] - L[T_INIEZIONE:])))
    esito("T1-F la misura NON vede lo spostamento di %g al tick %d (max|Lambda_iniettata - Lambda| < %g dopo)" % (DELTA_L, T_INIEZIONE, 0.5 * DELTA_L), vis < 0.5 * DELTA_L, "%.3e" % vis, deve=False)
    if float(dL.max()) == 0.0:
        lett = "v1: Lambda costante AL BIT"
    elif pend == pend and pend >= 0.75:
        lett = "v3: una deriva SISTEMATICA (la pendenza %.3f)" % pend
    elif pend == pend and pend >= 0.25:
        lett = "v2: pochi ulp, come una passeggiata casuale (la pendenza %.3f)" % pend
    else:
        lett = "v2: pochi ulp, LIMITATA (la pendenza %s)" % ("%.3f" % pend if pend == pend else "non definita")
    print("  LA LETTURA: (%s)" % lett)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
