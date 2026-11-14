# -*- coding: utf-8 -*-
r"""**IL BILANCIO DI `Grampa` E DI `(0)_2000`** *(Luca `2026-11-13` `23:47`, B3-B4; `2026-11-14` `00:53`, B2; la carta `doc/TASK_HISTORY/2026-11-14_bilancio_energie.md`)*.

    python csv/solitone/bilancio_corsa.py corsa --braccio Grampa|0_2000 --registro bilancio-<braccio>   (lo stdout nello scratchpad; gli stati su E:\soliton_simulator\bilancio)
    python csv/solitone/bilancio_corsa.py referto > doc/referti_l2/bilancio_grampa.txt

**`corsa`:** **lo stesso braccio di `p6_bracci`** *(la scena di C35-pi a `60000`, il bordo; `Grampa`: `tick_lapse.tick` dentro `p6_bracci.con_rampa(min(1, k/500))`, `rho_c` letto dal meta di
`Grampa.npz`; `0_2000`: `accensione.tick`)*, **`2000` tick** *(il ciclo COPIATO, dichiarato)*; **IN PIU': a ogni tick la massa e `tot` PRIMA e DOPO `bordo.assorbi`; lo stato completo ogni `250` tick su E:.**
### **DEVE: `d` e `M` ogni `50` tick = quelli di `p6_bracci/<braccio>.npz` AL BIT** *(le misure in piu' non cambiano la dinamica)*.
**`referto`:** **i pezzi B1** *(`conti.pezzi`)* **a ogni stato; il moto fra due stati; il residuo; le letture B4; i DEVE: la somma dei pezzi esatta; la massa col bordo entro `1e-12`; DEVE FALLIRE:
il residuo della rampa nullo.**
"""
import argparse
import json
import os
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import conti as CO  # noqa: E402
import p6_bracci as PBR  # noqa: E402
import p6_u_breve as PB  # noqa: E402
import s5_coppia_lapse as G2  # noqa: E402

BRACCI = ("Grampa", "0_2000")
N_TICK, OGNI, OGNI_STATO = 2000, 50, 250      # ### B3: lo stato completo ogni 250
DIR_E = r"E:\soliton_simulator\bilancio"
DIR_REF = os.path.join(os.path.dirname(_CSV), "doc", "referti_l2", "bilancio")
TOLL_MASSA = 1e-12                             # ### il mandato
TAPPA_S = 600.0
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota, deve):
    OK[1] += 1
    buono = passa if deve else not passa
    OK[0] += 1 if buono else 0
    if not buono:
        FALLITE.append(che)
    print("  %s: %-100s %s   %s" % ("DEVE PASSARE" if deve else "DEVE FALLIRE", che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def corsa(nome, registro):
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import _registro_corse as RC
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import carta_coppia as CC
    from solitone import tick_lapse as TL
    from solitone import toro as TO
    for m in ("conti", "p6_bracci", "tick_lapse", "bordo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    assert nome in BRACCI
    with np.load(os.path.join(PBR.DIR_OUT, nome + ".npz")) as d:
        meta = json.loads(str(d["meta"]))
        rif = {"t": d["t"].copy(), "d": d["d"].copy(), "M": d["M"].copy()}
    os.makedirs(DIR_E, exist_ok=True)
    t00 = time.time()
    print("=" * 130)
    print("IL BILANCIO, LA CORSA (%s): la scena di %s a %d; %d tick; rho_c %r (il meta di p6_bracci/%s.npz); lo stato ogni %d su %s" % (nome, G2.CORSA, G2.T0, N_TICK, meta["rho_c"], nome, OGNI_STATO, DIR_E))
    print("=" * 130)
    with CO.scena(G2.CORSA, G2.T0) as Z:
        st, mot, par, L = Z["st"], Z["mot"], Z["par"], Z["L"]
        s, K = Z["s"], Z["K"]
        legge = ("rho_c", meta["rho_c"])
        e0 = G2.eps_top_tl4b()
        x = TO.scarti(Z["m1"], Z["m2"], Z["bordo"]["c0"][0], Z["bordo"]["c0"][1], L)[:, 0]
        M_pt, E_pt = [], []                      # ### a ogni tick: (prima, dopo) il bordo

        def salva(k):
            f = os.path.join(DIR_E, "%s_%05d.npz" % (nome, k))
            np.savez(f, meta=np.array(json.dumps({"braccio": nome, "k": k, "t": G2.T0 + k, "sha": V.shas(Z["z"])})), cs=np.asarray(mot.cs, dtype=float),
                     **{kk: st[kk] for kk in Z["chiavi"]})
        S = {"t": [], "d": [], "M": []}

        def misura(k):
            rho = PB.rho_nodi(st, Z["nodo"], Z["n"])
            a, b = CC.centri_semipiani(rho, Z["m1"], Z["m2"], L, x, 0.0)
            S["t"].append(G2.T0 + k)
            S["d"].append(float(np.hypot(*CC.vettore(a, b, L))))
            S["M"].append(float(np.sum(np.abs(st["psi_h"]) ** 2)))
        misura(0)
        salva(0)
        t1 = t_tappa = time.time()
        for k in range(1, N_TICK + 1):
            t = G2.T0 + k
            if nome == "0_2000":
                AC.tick(Z["z"], t, K)
            else:
                with PBR.con_rampa(min(1.0, k / float(PBR.RAMPA))):
                    TL.tick(mot, st, par, s, legge, eps_a=e0)
            Mp, Ep = float(np.sum(np.abs(st["psi_h"]) ** 2)), CO.totale(Z)
            BO.assorbi(st, Z["g_e"], BO.c_di(t, Z["tab_c"], K, Z["omega"]) * Z["phi_v"])
            M_pt.append((Mp, float(np.sum(np.abs(st["psi_h"]) ** 2))))
            E_pt.append((Ep, CO.totale(Z)))
            if k % OGNI == 0:
                misura(k)
            if k % OGNI_STATO == 0:
                salva(k)
                print("    k %5d  d %.6f  M %.10e  E %.10e  (%.0f s)" % (k, S["d"][-1], S["M"][-1], E_pt[-1][1], time.time() - t1))
                sys.stdout.flush()
            if registro and time.time() - t_tappa >= TAPPA_S:
                import psutil
                RC.tappa(registro, "tick %d; %.3f s per tick; la memoria libera %.2f GB" % (t, (time.time() - t1) / k, psutil.virtual_memory().available / 1e9))
                t_tappa = time.time()
    os.makedirs(DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(DIR_REF, "%s_corsa.npz" % nome), t=np.array(S["t"]), d=np.array(S["d"]), M=np.array(S["M"]), M_pt=np.array(M_pt), E_pt=np.array(E_pt))
    n = min(len(S["d"]), len(rif["d"]))
    dd = [i for i in range(n) if S["d"][i] != rif["d"][i] or S["M"][i] != rif["M"][i]]
    print("-" * 130)
    print("### %d tick in %.0f s (%.3f s per tick)" % (N_TICK, time.time() - t1, (time.time() - t1) / N_TICK))
    esito("d e M ogni %d tick = p6_bracci/%s.npz AL BIT (%d punti)" % (OGNI, nome, n), not dd, "diversi: %d" % len(dd), True)
    print("=" * 130)
    print("ESITO: %d/%d; fallite %s; %.0f s in tutto" % (OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


def referto():
    import _presidio
    from solitone import carta_coppia as CC
    from solitone import toro as TO
    _presidio.avvia(os.path.join(_QUI, "conti.py"))
    _presidio.avvia(__file__)
    _d, _N, mu, _e2 = PB.dati_di_e()
    print("=" * 130)
    print("IL BILANCIO DELLE ENERGIE DI Grampa E DI (0)_2000 (Luca 23:47, la voce 15): i pezzi B1 ogni %d tick (conti.pezzi; R_PEZZO %g); il moto con la STIMA M_in v^2/2, mu %.4f (IPOTESI)" % (OGNI_STATO, CO.R_PEZZO, mu))
    print("=" * 130)
    tab = {}
    with CO.scena(G2.CORSA, G2.T0) as Z:
        L = Z["L"]
        x = TO.scarti(Z["m1"], Z["m2"], Z["bordo"]["c0"][0], Z["bordo"]["c0"][1], L)[:, 0]
        for nome in ("0_2000", "Grampa"):
            c = np.load(os.path.join(DIR_REF, "%s_corsa.npz" % nome))
            righe = []
            for k in range(0, N_TICK + 1, OGNI_STATO):
                with np.load(os.path.join(DIR_E, "%s_%05d.npz" % (nome, k))) as d:
                    Z["metti"]({kk: d[kk] for kk in Z["chiavi"]})
                    if "cs" in d.files and d["cs"].size > 1:
                        Z["mot"].cs = d["cs"].copy()                 # ### i conti col cs del tick (col lapse), come p6_bracci
                        Z["mot"].lambda_c = None
                rho = PB.rho_nodi(Z["st"], Z["nodo"], Z["n"])
                a, b = CC.centri_semipiani(rho, Z["m1"], Z["m2"], L, x, 0.0)
                P = CO.pezzi(Z, [a, b], None)
                righe.append((k, a, b, P))
            Z["metti"]()
            M_pt, E_pt = c["M_pt"], c["E_pt"]
            bordo_M = np.cumsum(M_pt[:, 0] - M_pt[:, 1])          # ### la massa tolta dal bordo, cumulata
            bordo_E = np.cumsum(E_pt[:, 0] - E_pt[:, 1])          # ### l'energia tolta dal bordo, cumulata
            tick_E = np.concatenate([[E_pt[0, 0] - righe[0][3]["tot"]], E_pt[1:, 0] - E_pt[:-1, 1]])    # ### la variazione di tot DENTRO ogni tick (senza il bordo)
            tab[nome] = (righe, bordo_M, bordo_E, tick_E, M_pt)
            print("### (%s) i pezzi ogni %d tick (la materia A, B, fuori; il vuoto A, B, lontano; tot; il residuo = tot(t) - tot(0) + l'energia tolta dal bordo; il moto relativo e la stima)" % (nome, OGNI_STATO))
            E0 = righe[0][3]["tot"]
            for j, (k, a, b, P) in enumerate(righe):
                res = P["tot"] - E0 + (bordo_E[k - 1] if k else 0.0)
                mv = ""
                if j:
                    k0, a0, b0, P0 = righe[j - 1]
                    vA, eA = CO.moto(a0, a, k - k0, L, P["massa"][0], mu)
                    vB, eB = CO.moto(b0, b, k - k0, L, P["massa"][1], mu)
                    mv = "  v A %.3e B %.3e, la stima %.3e" % (vA, vB, eA + eB)
                print("    k %5d  materia %.6e %.6e %.6e  vuoto %.6e %.6e %.6e  tot %.10e  residuo %+.6e%s  (somma esatta %s, tot - pezzi %.2e)" % (
                    k, P["materia"][0], P["materia"][1], P["materia"][2], P["vuoto"][0], P["vuoto"][1], P["vuoto"][2], P["tot"], res, mv, P["somma_esatta_ok"], P["tot_meno_pezzi"]))
    print("-" * 130)
    for nome in ("0_2000", "Grampa"):
        righe = tab[nome][0]
        esito("(%s) la somma dei pezzi = il totale ESATTA a ogni stato" % nome, all(r[3]["somma_esatta_ok"] for r in righe), "%d stati" % len(righe), True)
    _r, bM, _bE, _tE, M_pt = tab["0_2000"]
    M0 = M_pt[0, 0] + 0.0
    Mstart = tab["0_2000"][0][0][3]["M"]
    scarti = [abs((M_pt[k - 1, 1] - Mstart) + bM[k - 1]) / Mstart for k in range(1, N_TICK + 1)]
    esito("(0)_2000 la massa: Delta M + la massa tolta dal bordo = 0 entro %g relativo a ogni tick" % TOLL_MASSA, max(scarti) <= TOLL_MASSA, "il peggiore %.2e" % max(scarti), True)
    _r, _bM, bE, tE, _M = tab["Grampa"]
    rampa = float(np.sum(tE[:PBR.RAMPA]))
    dopo = tE[PBR.RAMPA:]
    rumore = float(np.std(dopo)) * np.sqrt(PBR.RAMPA)
    print("### Grampa: la variazione di tot DENTRO i tick (il residuo senza il bordo): nella rampa (0-%d) %+.6e; dopo, per tick: la media %+.3e, la deviazione %.3e (il rumore su %d tick %.3e)"
          % (PBR.RAMPA, rampa, float(np.mean(dopo)), float(np.std(dopo)), PBR.RAMPA, rumore))
    esito("Grampa: il residuo durante la rampa nullo entro il rumore del dopo-rampa", abs(rampa) <= 3.0 * rumore, "%.3e contro 3 x %.3e" % (abs(rampa), rumore), False)
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("azione", choices=("corsa", "referto"))
    ap.add_argument("--braccio", choices=BRACCI)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    return corsa(x.braccio, x.registro) if x.azione == "corsa" else referto()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
