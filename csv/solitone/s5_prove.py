# -*- coding: utf-8 -*-
r"""**S5.2: LE PROVE DEL LAPSE** *(sul ramo laterale; Luca `2026-11-11` `11:33` e `13:22`; il task history `doc/TASK_HISTORY/2026-11-09_laterale_mb.md`, sez. `31.15`)*. [[PUNTO-FISSO-CS-SOLITONE]]

    python csv/solitone/s5_prove.py --prova L1 > doc/referti_l2/s5_lapse_vuoto.txt
    python csv/solitone/s5_prove.py --prova L2 > doc/referti_l2/s5_lapse_energia.txt

**T-L1:** il vuoto `c(10000) F3`, `psi = 0`: il banco *(`rho_c = rho_0 / 1e-2`)* = il tick di oggi al bit per `1000` tick, e calmo *(la rms di `Lambda` sotto `1e-13`)*.
**T-L2:** `TBS` a `10000`, `5000` tick per `rho_0 / rho_c` in `{1e-3, 1e-2, 1e-1}`; `E_N` ogni `10` tick: la pendenza entro `3` errori di Sokal; le norme entro `1e-13`; l'escursione a `s` e a `s/2`
*(lo stesso tempo fisico, `rho_0/rho_c = 1e-2`)*, il rapporto fra `3.2` e `4.8`; accanto `N = 1` e M-rho istantanea; **DEVE FALLIRE:** il banco senza la reazione, la pendenza oltre `3` errori.
**`rho_0`** = la `rho` media del centro del solitone *(`r < w_in`)*.
"""
import hashlib
import math
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if os.path.dirname(_QUI) not in sys.path:
    sys.path.insert(0, os.path.dirname(_QUI))
import solitone  # noqa: E402,F401  (i percorsi)
from solitone import carta_punto_fisso as CPF  # noqa: E402

N_L1 = 1000                       # ### Luca: 1000 tick
FERMI = (1, 10, 100, 1000)
R_L1 = 1e-2                       # ### sez. 31.15
CALMO = 1e-13                     # ### sez. 31.15: il criterio di (v0a)
N_L2 = 5000                       # ### Luca: 5000 tick
OGNI = 10                         # ### sez. 31.15
RAPPORTI = (1e-3, 1e-2, 1e-1)     # ### Luca
R_ACCANTO = 1e-2                  # ### sez. 31.15: N = 1, M-rho, senza reazione, s/2 a questo rapporto
N_S, N_S2 = 1000, 2000            # ### sez. 31.15: lo stesso tempo fisico a s e a s/2
RAPP_ESC = (3.2, 4.8)             # ### Luca
N_ERR = 3.0                       # ### Luca
TOLL_NORMA = 1e-13                # ### Luca
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


def sha(a):
    return hashlib.sha1(np.ascontiguousarray(a).tobytes()).hexdigest()[:16]


def pendenza(t, y):
    """### la retta su `y(t)`, l'errore gonfiato di `sqrt(2 tau_int)` dei residui *(come U2)*: `(p, ep, tau)`."""
    from solitone import stazionarieta as SZ
    t, y = np.asarray(t, float), np.asarray(y, float)
    p, cov = np.polyfit(t, y, 1, cov=True)
    res = y - np.polyval(p, t)
    tr = float(SZ.tau_int(res)[0])
    return float(p[0]), math.sqrt(cov[0, 0]) * math.sqrt(2.0 * max(tr, 0.5)), tr


def main():
    import _deriva_congelato as DC
    import _dove_va_la_materia as DV
    import _presidio
    import _screening_forme_s3 as SF
    import _solitone_vuoto_congelato as VC
    import _stato_fermo as SFM
    import _triangoli_bassa_energia as BE
    import _vuoto_vivo_B as V
    import tick as TK
    import composizione as CM
    from solitone import bordo as BO
    from solitone import corsa_accensione as CA
    from solitone import tick_lapse as TL
    from solitone import toro as TO
    prova = sys.argv[sys.argv.index("--prova") + 1]
    assert prova in ("L1", "L2"), "--prova L1 | L2"
    for m in ("__init__", "corsa_accensione", "carta_punto_fisso", "tick_lapse", "toro", "bordo", "stazionarieta"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    for m in ("tick", "flussi_parziali", "energia_pesata"):
        _presidio.avvia(os.path.join(os.path.dirname(os.path.dirname(_QUI)), "primo_ordine", m + ".py"))
    _presidio.avvia(__file__)
    sol, vuoto, s = V.CORSE[CA.NOME]
    rr0 = CA.serie(CPF.CORSA)[0]
    w_in = float(rr0[0]["w_in"])
    stati = {x["t"]: x for r in rr0 for x in (r.get("stati") or [])}
    with np.load(os.path.join(CA.DIR_NPZ, CA.FASE)) as d:
        tab, omega, K = d["c"].copy(), float(d["omega"]), int(d["K"])
    c = BO.c_di(CPF.TICK_D4, tab, K, omega)
    t00 = time.time()
    print("=" * 130)
    print("S5.2 (sez. 31.15), la prova %s: s %g; w_in %.6f" % (prova, s, w_in))
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
        st, mot, par, inc = z["st"], z["mot"], z["par"], z["inc"]
        n, Lt = inc.n, z["L"]
        chiavi = sorted(k for k, v in st.items() if isinstance(v, np.ndarray))
        xs = stati[CPF.TICK_D4]

        def carica():
            for k in chiavi:
                st[k][...] = salvato[k]
            with np.load(xs["file"]) as d:
                for k in chiavi:
                    st[k][...] = d[k]
            assert all(SFM.sha(st[k]) == v for k, v in xs["sha"].items() if k in st), "lo stato NON e' quello registrato"

        def vuoto():
            for k in chiavi:
                st[k][...] = salvato[k]
            st["psi_h"][...] = 0.0
            st["phi_h"][...] = c * phi_v

        carica()
        rho = TL.rho_di(mot, st)
        vv = np.arange(n)
        c1, c2 = TO.centro(rho, vv // Lt, vv % Lt, Lt)[:2]
        pos = TO.scarti(vv // Lt, vv % Lt, c1, c2, Lt)
        rho_0 = float(rho[np.hypot(pos[:, 0], pos[:, 1]) < w_in].mean())
        print("### rho_0 = la rho media del centro (r < w_in) di %s: %.6f" % (os.path.basename(xs["file"]), rho_0))
        with SF.forma(VC.FORMA), BE.conv(DC.ZERO):
            if prova == "L1":
                legge = ("rho_c", rho_0 / R_L1)
                vuoto()
                ogg = {}
                for k in range(1, N_L1 + 1):
                    TL.tick_di_oggi(mot, st, par, s)
                    if k in FERMI:
                        ogg[k] = (sha(st["psi_h"]), sha(st["phi_h"]))
                vuoto()
                ban = {}
                for k in range(1, N_L1 + 1):
                    TL.tick(mot, st, par, s, legge)
                    if k in FERMI:
                        ban[k] = (sha(st["psi_h"]), sha(st["phi_h"]))
                lam = mot.densita_vuoto(st)
                rms = float(np.std(lam))
                for k in FERMI:
                    print("    tick %4d: oggi psi %s phi %s; il banco psi %s phi %s" % (k, ogg[k][0], ogg[k][1], ban[k][0], ban[k][1]))
                esito("T-L1: il vuoto, il banco (rho_c = rho_0 / %g) = il tick di oggi AL BIT ai tick %s" % (R_L1, FERMI), all(ogg[k] == ban[k] for k in FERMI))
                esito("T-L1: il vuoto resta calmo, la rms di Lambda al tick %d sotto %g" % (N_L1, CALMO), rms < CALMO, "%.3e" % rms)
            else:
                def corsa(nome, n_tick, passo, legge, s_):
                    """### `passo`: "lapse", "senza", "oggi", "mrho". `E_N / s` ogni `OGNI` tick, le norme."""
                    carica()
                    t0 = time.time()
                    tt, EE, npsi, nphi = [], [], [], []

                    def campiona(k):
                        tt.append(k * s_)
                        EE.append(TL.energia(mot, st, par, s_, legge) / s_)
                        npsi.append(float(np.sum(np.abs(st["psi_h"]) ** 2)))
                        nphi.append(float(np.sum(np.abs(st["phi_h"]) ** 2)))
                    campiona(0)
                    for k in range(1, n_tick + 1):
                        if passo == "lapse":
                            TL.tick(mot, st, par, s_, legge)
                        elif passo == "senza":
                            TL.tick(mot, st, par, s_, legge, senza_reazione=True)
                        elif passo == "oggi":
                            TL.tick_di_oggi(mot, st, par, s_)
                        else:
                            mot.cs = TL.cs_di(mot, st, s_, legge)
                            mot.lambda_c = None
                            TK.percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
                        if k % OGNI == 0:
                            campiona(k)
                    p, ep, tr = pendenza(tt, EE)
                    esc = float(np.max(EE) - np.min(EE))
                    dpsi = float(np.max(np.abs(np.array(npsi) / npsi[0] - 1.0)))
                    dphi = float(np.max(np.abs(np.array(nphi) / nphi[0] - 1.0)))
                    print("  %s: %d tick (%.0f s); E_N/s all'inizio %.10e, alla fine %.10e; l'escursione %.4e (relativa %.3e); la pendenza %+.4e +- %.1e per unita' di tempo (%.2f errori; tau_int %.2f); le norme: psi %.2e, phi %.2e"
                          % (nome, n_tick, time.time() - t0, EE[0], EE[-1], esc, esc / abs(EE[0]), p, ep, abs(p) / ep, tr, dpsi, dphi))
                    sys.stdout.flush()
                    return {"p": p, "ep": ep, "esc": esc, "dpsi": dpsi, "dphi": dphi}
                print("### T-L2: l'energia E_N / s (coi pesi dello stato), %d tick, ogni %d; rho_c = rho_0 / r" % (N_L2, OGNI))
                ris = {}
                for r in RAPPORTI:
                    ris[r] = corsa("il lapse, r %g" % r, N_L2, "lapse", ("rho_c", rho_0 / r), s)
                    esito("T-L2 r %g: nessuna deriva, la pendenza entro %g errori" % (r, N_ERR), abs(ris[r]["p"]) <= N_ERR * ris[r]["ep"], "%.2f errori" % (abs(ris[r]["p"]) / ris[r]["ep"]))
                    esito("T-L2 r %g: le norme di psi e phi entro %g" % (r, TOLL_NORMA), max(ris[r]["dpsi"], ris[r]["dphi"]) < TOLL_NORMA, "%.2e" % max(ris[r]["dpsi"], ris[r]["dphi"]))
                la = ("rho_c", rho_0 / R_ACCANTO)
                a1 = corsa("il lapse a s, r %g" % R_ACCANTO, N_S, "lapse", la, s)
                a2 = corsa("il lapse a s/2, r %g" % R_ACCANTO, N_S2, "lapse", la, s / 2.0)
                rap = a1["esc"] / a2["esc"]
                esito("T-L2: l'escursione scende come dtau^2: il rapporto (s contro s/2, lo stesso tempo fisico) fra %g e %g" % RAPP_ESC, RAPP_ESC[0] <= rap <= RAPP_ESC[1], "%.4f" % rap)
                uno = corsa("N = 1 (il tick di oggi)", N_L2, "oggi", ("uno",), s)
                print("    l'escursione del lapse (r %g) contro N = 1: %.4f" % (R_ACCANTO, ris[R_ACCANTO]["esc"] / uno["esc"]))
                mr = corsa("M-rho istantanea, r %g" % R_ACCANTO, N_L2, "mrho", la, s)
                print("    M-rho istantanea: la pendenza a %.2f errori (attesa diversa da zero)" % (abs(mr["p"]) / mr["ep"]))
                sr = corsa("il lapse SENZA la reazione, r %g" % R_ACCANTO, N_L2, "senza", la, s)
                esito("T-L2-F: senza la reazione, nessuna deriva (la pendenza entro %g errori)" % N_ERR, abs(sr["p"]) <= N_ERR * sr["ep"], "%.2f errori" % (abs(sr["p"]) / sr["ep"]), deve=False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s; %.0f s in tutto" % (OK[0], OK[1], len(FALLITE), FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
