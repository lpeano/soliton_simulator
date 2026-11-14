# -*- coding: utf-8 -*-
r"""**IL CONTROLLO DEL METODO RIVISTO, S7'** *(Luca `2026-11-14` `00:53`; la revisione del guardiano DOPO il fallimento di S7, dichiarata; il task history
`doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `12`)*.

    python csv/solitone/mattone_ctrl2.py --caso MG|MU|MGU --registro mattone-ctrl2-<caso> > <scratchpad>/mattone_ctrl2_<caso>.txt

### **S7':** **il francobollo incollato su `L 162`** *(come S7: la scena di S162, il francobollo del mattone a `5000`, lo spostamento multiplo di `3`)*, **`1250` tick; i primi `250` sono
l'ASSESTAMENTO** *(misurati e scritti, non giudicati)*; **il giudizio sui tick `250`-`1250`: il respiro entro il `25%` di quello del mattone negli ultimi `1000` tick, il centro fermo entro `0.2` nodi.**
**Il ciclo di `mattone.controllo` COPIATO** *(non e' parametrico nella durata e non salva la serie; `mattone.py` NON si tocca)*; **la serie del respiro e del centro ogni `50` tick in un npz.**
### **DEVE** *(la riproducibilita')*: **i primi `1000` tick danno il respiro e lo spostamento del centro del controllo S7 di prima** *((MG): `0.1068` e `0.0785`, a tutte le cifre stampate)*.
"""
import argparse
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

N_TICK, ASSESTAMENTO = 1250, 250        # ### S7' (Luca 00:53)
FINESTRA = 250                          # ### A1: il respiro in finestre di 250 tick
PRIMA = {"MG": (0.1068, 0.0785)}        # ### il controllo S7 di prima (dbfbaf31): il respiro e lo spostamento, come stampati (4 cifre)
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


def main(argv):
    import _presidio
    for m in ("mattone",):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--caso", required=True, choices=MT.CASI)
    ap.add_argument("--registro")
    x = ap.parse_args(argv)
    caso = x.caso
    t00 = time.time()
    rho_c = MT.rho_c_assoluto()
    f81 = os.path.join(MT.DIR_E, "%s_%05d.npz" % (caso, MT.K_RAMPA + MT.N_PIENO))
    serie = np.load(os.path.join(MT.DIR_REF, "%s_serie.npz" % caso))
    kk = serie["k"]
    ult = kk >= kk[-1] - MT.N_PIENO
    amp_m = float(serie["resp"][ult].max() - serie["resp"][ult].min())
    t_m = MT.T_BASE + MT.K_RAMPA + MT.N_PIENO
    print("=" * 130)
    print("S7' (%s; Luca 00:53): il francobollo del mattone (%s) su L 162 nella scena di S162; %d tick, i primi %d l'ASSESTAMENTO; il respiro del mattone negli ultimi %d tick %.4f"
          % (caso, f81, N_TICK, ASSESTAMENTO, MT.N_PIENO, amp_m))
    print("=" * 130)
    # ---------------------------------------------------------------- COPIATO da mattone.controllo (il francobollo e l'incollatura)
    with MT.scena(MT.CORSA_BASE, MT.T_BASE) as Z81:
        with np.load(f81) as d:
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
    E_sol = E81 - E81_vuoto
    print("### il francobollo: R_t %.1f (l'anello del vuoto %d); %d nodi; il centro d'origine %s; E_sol %.6e" % (fr["R_t"], fr["anello_vuoto"], len(fr["w"]), fr["centro"], E_sol))
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
            C.campo.E[...] = C.gauss(MT.PB.E_DECISO * (rho - rho.mean()))
            C.campo.e = MT.PB.E_DECISO
            C.e_prec = MT.PB.E_DECISO
        rho = MT.rho_di(Z)
        kk2, R, cen, gmax = [0], [MT.respiro(rho)], [MT.centro_di(Z, rho)], C.residuo()
        t1 = t_tappa = time.time()
        for k in range(1, N_TICK + 1):
            C.tick(k, t0 + k, 1.0, MT.PB.E_DECISO if caso in ("MU", "MGU") else 0.0)
            if k % MT.OGNI == 0:
                rho = MT.rho_di(Z)
                kk2.append(k)
                R.append(MT.respiro(rho))
                cen.append(MT.centro_di(Z, rho))
                if k % MT.OGNI_GAUSS == 0:
                    gmax = max(gmax, C.residuo())
                if k % 250 == 0:
                    print("    k %5d  il respiro %.4f  il centro (%.3f, %.3f)  (%.0f s)" % (k, R[-1], cen[-1][0], cen[-1][1], time.time() - t1))
                    sys.stdout.flush()
            if time.time() - t_tappa >= MT.TAPPA_S:
                MT.tappa(x.registro, "k %d; %.3f s per tick; la memoria libera %.2f GB" % (k, (time.time() - t1) / k, MT.memoria_gb()))
                t_tappa = time.time()
    kk2 = np.array(kk2)
    R = np.array(R)
    C1 = np.array([c[0] for c in cen])
    C2 = np.array([c[1] for c in cen])
    os.makedirs(MT.DIR_REF, exist_ok=True)
    np.savez_compressed(os.path.join(MT.DIR_REF, "ctrl2_%s_serie.npz" % caso), k=kk2, respiro=R, c1=C1, c2=C2, salto=salto)

    def finestra(a, b):
        ii = (kk2 >= a) & (kk2 <= b)
        amp = float(R[ii].max() - R[ii].min())
        sp = max(MT.distanza(Z["L"], (C1[i], C2[i]), (C1[ii][0], C2[ii][0])) for i in np.nonzero(ii)[0])
        return amp, sp
    print("-" * 130)
    print("### %d tick in %.0f s" % (N_TICK, time.time() - t1))
    print("### IL RESPIRO PER FINESTRE DI %d TICK (picco-picco) e lo spostamento del centro:" % FINESTRA)
    for a in range(0, N_TICK, FINESTRA):
        amp, sp = finestra(a, a + FINESTRA)
        print("    tick %4d-%4d: il respiro %.4f; il centro %.4f nodi%s" % (a, a + FINESTRA, amp, sp, "   (l'ASSESTAMENTO: misurato, non giudicato)" if a < ASSESTAMENTO else ""))
    a1000, s1000 = finestra(0, 1000)
    a_g, s_g = finestra(ASSESTAMENTO, N_TICK)
    print("    i primi 1000 tick (come S7): il respiro %.4f, il centro %.4f; IL GIUDIZIO S7' (tick %d-%d): il respiro %.4f contro il mattone %.4f (il rapporto %.3f; la tolleranza %g), il centro %.4f (la soglia %g)"
          % (a1000, s1000, ASSESTAMENTO, N_TICK, a_g, amp_m, a_g / amp_m, MT.TOLL_RESPIRO, s_g, MT.FERMO_CENTRO))
    if caso in ("MU", "MGU"):
        print("    il residuo di Gauss: il massimo %.3e" % gmax)
    if caso in PRIMA:
        esito("la riproducibilita': i primi 1000 tick = il controllo S7 di prima (%.4f e %.4f, 4 cifre)" % PRIMA[caso], ("%.4f" % a1000, "%.4f" % s1000) == ("%.4f" % PRIMA[caso][0], "%.4f" % PRIMA[caso][1]),
              "%.4f e %.4f" % (a1000, s1000), True)
    passa = abs(a_g - amp_m) <= MT.TOLL_RESPIRO * amp_m and s_g <= MT.FERMO_CENTRO and (caso == "MG" or gmax < MT.TOLL_GAUSS)
    print("=" * 130)
    print("ESITO: S7' %s; %d/%d controlli come devono; fallite: %s; %.0f s in tutto" % ("PASSA" if passa else "### NON PASSA", OK[0], OK[1], FALLITE, time.time() - t00))
    return 0 if (passa and not FALLITE) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
