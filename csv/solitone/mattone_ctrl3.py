# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DEL METODO SUL MATTONE COTTO, S7''** *(Luca `2026-11-14` `09:34`, A3; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `15`)*.

    python csv/solitone/mattone_ctrl3.py --caso MGU --registro mattone-ctrl3-<caso> > <scratchpad>/mattone_ctrl3_<caso>.txt   (poi doc/referti_l2/mattone/ctrl3_<caso>.txt)

### **S7'':** **il francobollo del mattone COTTO** *(`doc/referti_l2/mattone/cottura_<caso>.json`)* **su `L 162` nella scena di S162** *(come S7 e S7': lo spostamento multiplo di `3`, la fase allineata)*,
**`1250` tick a campi pieni; i primi `250` l'ASSESTAMENTO** *(scritti, non giudicati)*; **il giudizio sui tick `250`-`1250`: S5' entro il `25%` di S5' del mattone cotto; il centro fermo entro `0.2` nodi;
la media del picco fra `250`-`750` e `750`-`1250` cambia meno del `2%`.** **Il tick di `mattone_cottura.Corsa`** *(coi conti R-CONTI)*; **il respiro, il picco, il centro ogni `10` tick.**
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
import mattone as MT  # noqa: E402
import mattone_cottura as CT  # noqa: E402

N_TICK, ASSESTAMENTO = 1250, 250        # ### S7'' (Luca 09:34)
SOGLIA_PICCO = 0.02                     # ### S7'': la media del picco fra 250-750 e 750-1250
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


def francobollo(caso):
    """### Il francobollo del mattone cotto *(come `mattone.controllo`)*: `(fr, E_sol, cottura)`."""
    with open(os.path.join(MT.DIR_REF, "cottura_%s.json" % caso), encoding="utf-8") as fh:
        ct = json.load(fh)
    assert ct["cotto"], "il mattone %s NON e' cotto" % caso
    t_m = MT.T_BASE + int(ct["k"])
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z81:
        with np.load(ct["file"]) as d:
            Z81["metti"]({k: d[k] for k in Z81["chiavi"]})
        rho81 = MT.rho_di(Z81)
        c81 = MT.centro_di(Z81, rho81)
        st81 = {k: Z81["st"][k].copy() for k in Z81["chiavi"]}
        E81 = MT.energia(Z81)
        MT.vuoto_fresco(Z81, t_m)
        phi_rif81 = Z81["st"]["phi_h"].copy()
        E81_vuoto = MT.energia(Z81)
        Z81["metti"](st81)
        fr = MT.ritaglia(Z81, c81, phi_rif81)
    return fr, E81 - E81_vuoto, ct


def main(argv):
    import _presidio
    for m in ("mattone", "mattone_cottura", "conti"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso", required=True, choices=CT.CASI)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    caso = x.caso
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO if caso == "MGU" else 0.0
    fr, E_sol, ct = francobollo(caso)
    print("=" * 130)
    print("S7'' (%s; Luca 09:34, A3): il francobollo del mattone COTTO (%s, k %d; S5' %.4f) su L 162 nella scena di S162; %d tick, i primi %d l'ASSESTAMENTO"
          % (caso, ct["file"], ct["k"], ct["s5p"], N_TICK, ASSESTAMENTO))
    print("=" * 130)
    print("### il francobollo: R_t %.1f (l'anello del vuoto %d); %d nodi; il centro d'origine %s; E_sol %.6e" % (fr["R_t"], fr["anello_vuoto"], len(fr["w"]), fr["centro"], E_sol))
    S = {k: [] for k in ("k", "rmax", "resp", "c1", "c2", "M")}
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c_s = MT.centro_di(Z, MT.rho_di(Z))
        cd = [int(round(c_s[i])) for i in (0, 1)]
        cd = [cd[i] - ((cd[i] - fr["centro"][i]) % 3) for i in (0, 1)]
        t0 = MT.G2.T0
        MT.vuoto_fresco(Z, t0)
        E_v162 = MT.energia(Z)
        D = MT.incolla(Z, fr, cd, True)
        salto = MT.energia(Z) - E_v162 - E_sol
        print("### incollato a %s; il salto di energia all'incollatura %.6e (Delta %.6f)" % (cd, salto, D))
        C = MT.Campi(Z, caso, rho_c, MT.PB.E_DECISO)
        if C.campo is not None:
            rho = MT.rho_di(Z)
            C.campo.A[...] = 0.0
            C.campo.E[...] = C.gauss(e * (rho - rho.mean()))
            C.campo.e = e
            C.e_prec = e
        R = CT.Corsa(Z, C)
        gmax = [C.residuo()]

        def misura(k):
            rho = MT.rho_di(Z)
            c = MT.centro_di(Z, rho)
            S["k"].append(k)
            S["rmax"].append(float(rho.max()))
            S["resp"].append(MT.respiro(rho))
            S["c1"].append(c[0])
            S["c2"].append(c[1])
            S["M"].append(float(rho.sum()))
            R.etichette([c])
        misura(0)
        R.inizio(0)
        t1 = t_tappa = time.time()
        for k in range(1, N_TICK + 1):
            R.passo(k, t0 + k, 1.0, e)
            if k % CT.OGNI == 0:
                misura(k)
                if k % MT.OGNI_GAUSS == 0:
                    gmax.append(C.residuo())
                    print("    k %5d  il respiro %.4f  il picco %.4e  il centro (%.3f, %.3f)  (%.0f s)" % (k, S["resp"][-1], S["rmax"][-1], S["c1"][-1], S["c2"][-1], time.time() - t1))
                    sys.stdout.flush()
            if time.time() - t_tappa >= MT.TAPPA_S:
                MT.tappa(x.registro, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (time.time() - t1) / k, MT.memoria_gb()))
                t_tappa = time.time()
        print("-" * 130)
        print("### %d tick in %.0f s" % (N_TICK, time.time() - t1))
        R.tabella(["sol"])
        L = Z["L"]
    kk = np.array(S["k"])
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "ctrl3_%s_serie.npz" % caso), salto=salto, **{k: np.array(v) for k, v in S.items()})
    print("### R-CONTI-3: la deriva del centro, il picco ogni %d tick" % CT.OGNI_CONTI)
    for p in range(0, N_TICK + 1, CT.OGNI_CONTI):
        i = int(np.nonzero(kk == p)[0][0])
        print("    k %5d  il centro (%.4f, %.4f), la deriva %.4f nodi; il picco %.4e; la massa %.10e" % (p, S["c1"][i], S["c2"][i], MT.distanza(L, (S["c1"][i], S["c2"][i]), (S["c1"][0], S["c2"][0])), S["rmax"][i], S["M"][i]))
    ff = CT.finestre_s5(kk, S["resp"], 0, N_TICK)
    print("### S5' PER FINESTRE (la retta tolta): %s   (la prima e' l'ASSESTAMENTO: scritta, non giudicata)" % " ".join("%d-%d %.4f" % f for f in ff))
    s5, _ff = CT.s5p(kk, S["resp"], N_TICK)
    gg = (kk >= ASSESTAMENTO) & (kk <= N_TICK)
    sp = max(MT.distanza(L, (S["c1"][i], S["c2"][i]), (S["c1"][np.nonzero(gg)[0][0]], S["c2"][np.nonzero(gg)[0][0]])) for i in np.nonzero(gg)[0])
    pk = np.array(S["rmax"])
    p1, p2 = float(pk[(kk >= 250) & (kk <= 750)].mean()), float(pk[(kk > 750) & (kk <= 1250)].mean())
    dp = abs(p2 - p1) / p1
    print("### IL GIUDIZIO S7'' (tick %d-%d): S5' %.4f contro il mattone cotto %.4f (il rapporto %.3f; la tolleranza %g); il centro %.4f (la soglia %g); il picco medio %.4e -> %.4e (%.4f; la soglia %g)"
          % (ASSESTAMENTO, N_TICK, s5, ct["s5p"], s5 / ct["s5p"], MT.TOLL_RESPIRO, sp, MT.FERMO_CENTRO, p1, p2, dp, SOGLIA_PICCO))
    if caso == "MGU":
        print("    il residuo di Gauss: il massimo %.3e (sotto %g)" % (max(gmax), MT.TOLL_GAUSS))
    esito("S7'': S5' entro il %d%% del mattone cotto" % int(100 * MT.TOLL_RESPIRO), abs(s5 - ct["s5p"]) <= MT.TOLL_RESPIRO * ct["s5p"], "%.4f contro %.4f" % (s5, ct["s5p"]), True)
    esito("S7'': il centro fermo entro %g nodi sui tick %d-%d" % (MT.FERMO_CENTRO, ASSESTAMENTO, N_TICK), sp <= MT.FERMO_CENTRO, "%.4f" % sp, True)
    esito("S7'': la media del picco fra 250-750 e 750-1250 cambia meno del %g" % SOGLIA_PICCO, dp < SOGLIA_PICCO, "%.4f" % dp, True)
    if caso == "MGU":
        esito("il residuo di Gauss sotto %g a ogni controllo" % MT.TOLL_GAUSS, max(gmax) < MT.TOLL_GAUSS, "%.3e" % max(gmax), True)
    print("=" * 130)
    print("ESITO: S7'' %s; %d/%d controlli come devono; fallite: %s; %.0f s in tutto" % ("PASSA" if not FALLITE else "### NON PASSA", OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
