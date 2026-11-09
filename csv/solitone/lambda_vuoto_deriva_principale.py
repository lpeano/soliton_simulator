# -*- coding: utf-8 -*-
r"""**D1, LA DERIVA DI `Lambda` DEL VUOTO SUL NUCLEO CONGELATO DEL PRINCIPALE** *(Luca `2026-11-09` `23:02`; il task history `doc/TASK_HISTORY/2026-11-09_d1_deriva_lambda_principale.md`)*. [[PIANO-2D-3D]] [[H-NUCLEO-CONGELATO]]

    python csv/solitone/lambda_vuoto_deriva_principale.py > doc/referti_l2/lambda_vuoto_deriva_principale.txt
    python csv/solitone/lambda_vuoto_deriva_principale.py --senza-avvolgimento > doc/referti_l2/lambda_vuoto_deriva_principale_nucleo.txt

### **D1-bis** *(il task history di D1, sez. `6`: la correzione di un mio errore)*: **con `--senza-avvolgimento` la scena si costruisce IDENTICA, ma i tick girano con `contextlib.nullcontext()`
### al posto di `BE.conv(DC.ZERO)`**, che sul principale AVVOLGE in memoria `grover`/`hop_psi`/`hop_phi` con lo zero simmetrico: **cosi' gira il nucleo congelato com'e' sul disco.**

### **LA COPIA, SUL PRINCIPALE, di `csv/solitone/lambda_vuoto_deriva.py` del laterale** *(`141711d3`, blob `b4610021`, sha1 dei byte grezzi; l'eccezione di Luca a U1)*, **con le cinque modifiche
### della sez. `2` del task history:** `CORSA` scritta qui *(`carta_punto_fisso` non c'e')*; i timbri *(`ramo.py`)*; questa docstring; **i numeri del laterale LETTI dal suo referto committato**; **le letture w1/w2/w3.**
**Il testo che segue e' quello del laterale** *(T1)*:

**Il vuoto F3 da solo** *(la scena di `carta_punto_fisso`, `psi = 0`, `phi` = il vuoto della corsa)*, **`mot.lambda_c = None`** *(`cs` spento)*, **`1000` tick di `tick.tick`.**
**A ogni tick, per nodo, `Delta Lambda` in valore e in ulp; la deriva cumulata ai tick `1`, `10`, `100`, `1000`; la pendenza in log-log della rms fra `10` e `1000`.**
**T1-F** *(DEVE FALLIRE)*: **in una seconda corsa, `Lambda` di un nodo spostato di `1e-12` al tick `500`; «la misura non lo vede».** **Le letture:** `v1` / `v2` *(limitata, passeggiata)* / `v3`.
"""
import contextlib
import hashlib
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)

CORSA = "TBS"                  # ### D1 (1): il valore di carta_punto_fisso.CORSA sul laterale (il file non c'e' sul principale)
LATERALE = ("zero-nel-nucleo", "81c690a8", "doc/referti_l2/lambda_vuoto_deriva.txt")   # ### D1 (4): il referto di T1, letto con git show
SENZA = "--senza-avvolgimento" in sys.argv[1:]   # ### D1-bis (sez. 6)
TOLL_W1 = 0.10                 # ### D1 (5): «entro il 10%» (Luca)
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


def laterale():
    """### D1 (4): **i numeri di T1 letti dal referto committato del laterale** *(nessun numero ricopiato a mano)*: `{tick: (max, media, rms)}`, la pendenza, `|dL|` max/media, i tick fermi."""
    import re
    import subprocess
    radice = os.path.dirname(os.path.dirname(_QUI))
    testo = subprocess.check_output(["git", "show", "%s:%s" % (LATERALE[1], LATERALE[2])], cwd=radice).decode("utf-8")
    tab = {}
    for m in re.finditer(r"al tick\s+(\d+): max ([-+0-9.e]+) \(([0-9.]+) ulp\), media ([-+0-9.e]+), rms ([-+0-9.e]+)", testo):
        tab[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)))
    pe = re.search(r"fra t 10 e t \d+: ([-0-9.]+)", testo)
    dl = re.search(r"max ([0-9.e+-]+) \(([0-9.]+) ulp\), media ([0-9.e+-]+) \(([0-9.]+) ulp\); i tick con Delta Lambda = 0 ovunque: (\d+) su (\d+)", testo)
    assert sorted(tab) == list(TICK_STAMPA) and pe and dl, "il referto del laterale non si legge"
    return tab, float(pe.group(1)), tuple(float(dl.group(k)) for k in (1, 2, 3, 4)) + (int(dl.group(5)), int(dl.group(6)))


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
    from solitone import ramo as R
    for m in ("__init__", "corsa_accensione", "ramo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    ramo, testo = R.stato_del_repo()
    print("### D1: il ramo %r; il divieto P3 attivo: %s (alza solo con mot.cs E mot.lambda_c non None; qui lambda_c = None)" % (ramo, R.ATTIVO[0]))
    t00 = time.time()
    print("=" * 130)
    print("T1, LA DERIVA DI Lambda DEL VUOTO A cs SPENTO (sez. 23): il vuoto F3 della corsa %s, %d tick; T1-F: %g su un nodo al tick %d" % (CORSA, N_TICK, DELTA_L, T_INIEZIONE))
    print("=" * 130)
    with CA.con_L(CA.LCORSA.get(CORSA)), V.scena(s, vuoto, V.EPS) as (rec, z, phi0, pK):
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            DC.forma(z, rec["larghezza"])
        salvato = {k: v.copy() for k, v in z["st"].items() if isinstance(v, np.ndarray)}
        V.partenza(sol, z, phi0, pK, s)
        DV.autovettori(DV.matrice(z, phi0, DV.AMP))
        phi_v = CA.vuoto_della_corsa(z, CORSA)
        for k, v in salvato.items():
            z["st"][k][...] = v
        st, mot, par = z["st"], z["mot"], z["par"]
        st["psi_h"][...] = 0.0
        st["phi_h"][...] = phi_v
        foto = {k: v.copy() for k, v in st.items() if isinstance(v, np.ndarray)}
        hs = hashlib.sha1()
        for k in sorted(foto):
            hs.update(k.encode("utf-8"))
            hs.update(np.ascontiguousarray(foto[k]).tobytes())
        print("### D1-bis: lo sha1 dei byte dello stato di partenza (tutte le chiavi ndarray, in ordine): %s; la modalita': %s" % (hs.hexdigest()[:16], "SENZA avvolgimento (il nucleo del disco)" if SENZA else "con BE.conv(DC.ZERO) (come T1)"))
        print("### la scena: %d nodi; mot.cs %s; Lambda all'inizio min %.17g max %.17g" % (mot.inc.n, "None" if mot.cs is None else "array (min %.6g, max %.6g)" % (float(np.min(mot.cs)), float(np.max(mot.cs))), float(mot.densita_vuoto(st).min()), float(mot.densita_vuoto(st).max())))
        import flussi_parziali as FP
        with SF.forma(VC.FORMA), (contextlib.nullcontext() if SENZA else BE.conv(DC.ZERO)):
            print("### D1-bis, il controllo positivo: dentro i tick FP.grover e' %s.%s, FP.hop_phi e' %s.%s" % (FP.grover.__module__, FP.grover.__qualname__, FP.hop_phi.__module__, FP.hop_phi.__qualname__))
            L = corsa(st, mot, par, foto, False)
            Li = corsa(st, mot, par, foto, True)
    ulp = np.spacing(np.abs(L[0]))
    dL = np.abs(np.diff(L, axis=0))
    print("  |Delta Lambda| per tick (tutti i nodi, tutti i tick): max %.3e (%.1f ulp), media %.3e (%.2f ulp); i tick con Delta Lambda = 0 ovunque: %d su %d"
          % (float(dL.max()), float((dL / ulp).max()), float(dL.mean()), float((dL / ulp).mean()), int(np.sum(np.all(dL == 0, axis=1))), N_TICK))
    tabL, pendL, dlL = laterale()
    print("    ACCANTO, il laterale (%s, %s): max %.3e (%.1f ulp), media %.3e (%.2f ulp); i tick fermi %d su %d" % (LATERALE[1], LATERALE[2], dlL[0], dlL[1], dlL[2], dlL[3], dlL[4], dlL[5]))
    D = L - L[0]
    rms = []
    for t in TICK_STAMPA:
        r_ = float(np.sqrt(np.mean(D[t] ** 2)))
        rms.append(r_)
        print("  la deriva Lambda(t) - Lambda(0) al tick %4d: max %.3e (%.1f ulp), media %+.3e, rms %.3e" % (t, float(np.abs(D[t]).max()), float((np.abs(D[t]) / ulp).max()), float(D[t].mean()), r_))
        print("    ACCANTO, il laterale al tick %4d: max %.3e (%.1f ulp), media %+.3e, rms %.3e" % ((t,) + tabL[t]))
    tt = np.arange(10, N_TICK + 1)
    rr = np.sqrt(np.mean(D[tt] ** 2, axis=1))
    if np.all(rr > 0):
        pend = float(np.polyfit(np.log(tt), np.log(rr), 1)[0])
    else:
        pend = float("nan")
    print("  la pendenza in log-log della rms della deriva fra t 10 e t %d: %s" % (N_TICK, "%.3f" % pend if pend == pend else "non definita (rms = 0 in qualche tick)"))
    print("    ACCANTO, il laterale: %.3f" % pendL)
    dP, dLat = float(D[N_TICK].mean()), tabL[N_TICK][2]
    rapp = dP / dLat if dLat != 0 else float("nan")
    print("  la deriva media per tick (al tick %d, diviso %d): il principale %+.4e, il laterale %+.4e; il rapporto principale/laterale %.6f" % (N_TICK, N_TICK, dP / N_TICK, dLat / N_TICK, rapp))
    vis = float(np.max(np.abs(Li[T_INIEZIONE:] - L[T_INIEZIONE:])))
    esito("T1-F la misura NON vede lo spostamento di %g al tick %d (max|Lambda_iniettata - Lambda| < %g dopo)" % (DELTA_L, T_INIEZIONE, 0.5 * DELTA_L), vis < 0.5 * DELTA_L, "%.3e" % vis, deve=False)
    if float(dL.max()) == 0.0 or not (pend == pend and pend >= 0.75):
        lett = "w2: nessuna deriva sistematica sul principale (%s; la pendenza %s): l'ha introdotta il v2" % ("Lambda costante AL BIT" if float(dL.max()) == 0.0 else "non costante", "%.3f" % pend if pend == pend else "non definita")
    elif abs(rapp - 1.0) <= TOLL_W1:
        lett = "w1: la stessa deriva entro il %.0f%% (il rapporto %.6f, la pendenza %.3f): del tick di sempre, non del v2" % (100 * TOLL_W1, rapp, pend)
    else:
        lett = "w3: una deriva diversa (il rapporto principale/laterale %.6f, la pendenza %.3f)" % (rapp, pend)
    print("  LA LETTURA: (%s)" % lett)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
