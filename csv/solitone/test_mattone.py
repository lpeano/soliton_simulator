# -*- coding: utf-8 -*-
r"""**IL COLLAUDO DELLO STRUMENTO «MATTONE»** *(Luca `2026-11-13` `18:47`; i DEVE del mandato che non vogliono una preparazione intera; il task history `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`)*.

    python csv/solitone/test_mattone.py > doc/referti_l2/mattone/collaudo.txt

**DEVE PASSARE:** **(MG) la rampa spenta** *(`r = 1` da subito)*: **`20` tick del tick del mattone = `20` tick di `tick_lapse.tick` AL BIT** *(col bordo)*; **(MU) `e = 0`: `20` tick = `20` tick di `accensione.tick` AL BIT;**
**il francobollo** *(TBS a `10000`)* **ritagliato e incollato SENZA spostarlo nello stesso stato: dentro `R_t` lo stato originale entro `1e-12` relativo.**
**DEVE FALLIRE:** **il francobollo incollato su `L 162` SENZA allineare la fase del vuoto: il salto di energia NON maggiore di quello con la fase allineata.**
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402

N_PROVA = 20                 # ### il mandato: 20 tick
TOLL_FRANC = 1e-12           # ### il mandato
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


def main():
    import _presidio
    import _vuoto_vivo_B as V
    from solitone import accensione as AC
    from solitone import bordo as BO
    from solitone import tick_lapse as TL
    for m in ("mattone", "p6_bracci", "p6_u_breve", "s5_coppia_lapse", "tick_lapse", "_u1_oggi", "bordo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    print("=" * 120)
    print("IL COLLAUDO DEL MATTONE: TBS a %d (L 81), S162 (L 162); %d tick; rho_c %.6f" % (MT.T_BASE, N_PROVA, rho_c))
    print("=" * 120)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z:
        st, mot, par = Z["st"], Z["mot"], Z["par"]
        e0 = MT.G2.eps_top_tl4b()

        def bordo(t):
            BO.assorbi(st, Z["g_e"], BO.c_di(t, Z["tab_c"], Z["K"], Z["omega"]) * Z["phi_v"])
        # ---------------------------------------------------------------- (MG) la rampa spenta
        Z["metti"]()
        for k in range(1, N_PROVA + 1):
            TL.tick(mot, st, par, Z["s"], ("rho_c", rho_c), eps_a=e0)
            bordo(MT.T_BASE + k)
        sha_oggi = V.shas(Z["z"])
        Z["metti"]()
        C = MT.Campi(Z, "MG", rho_c, MT.PB.E_DECISO)
        for k in range(1, N_PROVA + 1):
            C.tick(k, MT.T_BASE + k, 1.0, 0.0)
        sha_m = V.shas(Z["z"])
        div = [k for k in sha_oggi if sha_oggi[k] != sha_m[k]]
        esito("(MG) la rampa spenta: %d tick del mattone = tick_lapse.tick AL BIT (col bordo)" % N_PROVA, not div, "diverse: %s" % div, True)
        # ---------------------------------------------------------------- (MU) e = 0
        Z["metti"]()
        for k in range(1, N_PROVA + 1):
            AC.tick(Z["z"], MT.T_BASE + k, Z["K"])
            bordo(MT.T_BASE + k)
        sha_oggi = V.shas(Z["z"])
        Z["metti"]()
        C = MT.Campi(Z, "MU", rho_c, MT.PB.E_DECISO)
        for k in range(1, N_PROVA + 1):
            C.tick(k, MT.T_BASE + k, 1.0, 0.0)
        sha_m = V.shas(Z["z"])
        div = [k for k in sha_oggi if sha_oggi[k] != sha_m[k]]
        esito("(MU) e = 0: %d tick del mattone = accensione.tick AL BIT (col bordo)" % N_PROVA, not div, "diverse: %s" % div, True)
        Z["metti"]()
        mot.geo.U[...] = Z["U0"]
        # ---------------------------------------------------------------- il francobollo nello stesso toro
        Z["metti"]()
        rho = MT.rho_di(Z)
        c = MT.centro_di(Z, rho)
        st0 = {k: st[k].copy() for k in Z["chiavi"]}
        E_tbs = MT.energia(Z)
        MT.vuoto_fresco(Z, MT.T_BASE)
        phi_rif = st["phi_h"].copy()
        E_tbs_vuoto = MT.energia(Z)
        Z["metti"](st0)
        fr = MT.ritaglia(Z, c, phi_rif)
        print("### il francobollo di TBS a %d: R_t %.1f (l'anello del vuoto %d); %d nodi; il centro %s; il |dphi| medio per anello: %s"
              % (MT.T_BASE, fr["R_t"], fr["anello_vuoto"], len(fr["w"]), fr["centro"], " ".join("%.3g" % x for x in fr["dphi_anelli"])))
        D = MT.incolla(Z, fr, fr["centro"], True)
        vv = ((fr["centro"][0] + fr["o1"]) % Z["L"]) * Z["L"] + (fr["centro"][1] + fr["o2"]) % Z["L"]
        rr = Z["righe"][vv[fr["r"] <= fr["R_t"]]]
        e_psi = float(np.max(np.abs(st["psi_h"][rr] - st0["psi_h"][rr]))) / float(np.max(np.abs(st0["psi_h"])))
        e_phi = float(np.max(np.abs(st["phi_h"][rr] - st0["phi_h"][rr]))) / float(np.max(np.abs(st0["phi_h"])))
        esito("il francobollo ritagliato e incollato SENZA spostarlo nello stesso stato: dentro R_t lo stato entro %g relativo" % TOLL_FRANC, max(e_psi, e_phi) <= TOLL_FRANC,
              "psi %.2e, phi %.2e; Delta %r" % (e_psi, e_phi, D), True)
        Z["metti"]()
    E_sol = E_tbs - E_tbs_vuoto
    # ---------------------------------------------------------------- la fase del vuoto su L 162
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c_s = MT.centro_di(Z, MT.rho_di(Z))
        cd = [int(round(c_s[i])) for i in (0, 1)]
        cd = [cd[i] - ((cd[i] - fr["centro"][i]) % 3) for i in (0, 1)]
        MT.vuoto_fresco(Z, MT.G2.T0)
        E_v = MT.energia(Z)
        salvo = {k: Z["st"][k].copy() for k in Z["chiavi"]}
        salti = {}
        for allinea in (True, False):
            for k in Z["chiavi"]:
                Z["st"][k][...] = salvo[k]
            D = MT.incolla(Z, fr, cd, allinea)
            salti[allinea] = (D, MT.energia(Z) - E_v - E_sol)
        print("### su L 162 a %s (tick %d): il salto di energia E - E(vuoto) - E_sol: allineato %.6e (Delta %.6f), non allineato %.6e" % (cd, MT.G2.T0, salti[True][1], salti[True][0], salti[False][1]))
        esito("il francobollo SENZA allineare la fase del vuoto: il salto di energia non maggiore di quello allineato", abs(salti[False][1]) <= abs(salti[True][1]),
              "%.3e contro %.3e" % (abs(salti[False][1]), abs(salti[True][1])), False)
    print("=" * 120)
    print("ESITO: %d/%d controlli come devono; fallite: %d %s" % (OK[0], OK[1], len(FALLITE), FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
