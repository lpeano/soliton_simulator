# -*- coding: utf-8 -*-
r"""**LA PROVA DEL RIUSO DELLA FATTORIZZAZIONE DI GAUSS** *(Luca `2026-11-15` `14:05`, `15:07`)*.

    python csv/solitone/prova_gauss.py --registro prova-gauss > <scratchpad>/prova_gauss.txt     (poi doc/referti_l2/mattone/prova_gauss.txt)

**Il mattone di `L 162`** *(`L162_MGU_03000`, `U` dal campo)* **da solo nella scena di S162, il bordo da `R_A 60`, G+U, `50` tick col tick di `mattone.Campi`:** **una volta com'e'** *(`spsolve` a ogni tick)*, **una volta col
riuso** *(`gauss_riuso.accendi`)*, **dallo stesso stato.** ### **DEVE PASSARE: lo stato dopo `50` tick col riuso = quello di oggi AL BIT** *(tutte le chiavi, `campo_A`, `campo_E`; `h_int` esclusa)*. **Accanto: il tempo per tick
prima e dopo** *(la macchina CARICA: dichiarato)*; **le fattorizzazioni costruite** *(deve essere `1`)*. **Se non e' al bit: si scrive di quanto e perche', e il riuso NON si usa.**
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
import gauss_riuso as GR  # noqa: E402
import mattone as MT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK = 50


def main(argv):
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_cottura_U", "mattone_triangolo", "gauss_riuso", "p6_u_breve"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    ap = argparse.ArgumentParser()
    ap.add_argument("--registro")
    reg = ap.parse_args(argv).registro
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 130)
    print("IL RIUSO DELLA FATTORIZZAZIONE DI GAUSS (Luca 14:05, 15:07): %s da solo nella scena di S162, il bordo da R_A %g, G+U, %d tick, com'e' e col riuso; la macchina CARICA" % (ct["file"], MTR.R_A_SCENA, N_TICK))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        with np.load(ct["file"]) as d:
            dati = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()

        def gira(riuso):
            Z["metti"](dati)
            C = MT.Campi(Z, "MGU", rho_c, e)
            C.campo.A[...] = A0
            C.campo.E[...] = E0
            C.campo.e = e
            C.e_prec = e
            U1.scrivi_U(Z["mot"], C.campo)
            if riuso:
                GR.accendi()
            t1 = time.time()
            try:
                for k in range(1, N_TICK + 1):
                    C.tick(k, t_s + k, 1.0, e)
                    if reg and k % 10 == 0:
                        MT.tappa(reg, "%s k %d; %.3f s per tick" % ("riuso" if riuso else "oggi", k, (time.time() - t1) / k))
            finally:
                costruite = GR.CACHE["costruite"]
                GR.spegni()
            out = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            out.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
            return out, (time.time() - t1) / N_TICK, costruite
        oggi, t_oggi, _c = gira(False)
        riu, t_riu, costr = gira(True)
        Z["metti"]()
    diverse = []
    for x in sorted(oggi):
        if x in CU.CHIAVI_SERVIZIO:
            continue
        bit = bool(np.array_equal(oggi[x], riu[x]))
        den = float(np.max(np.abs(oggi[x]))) or 1.0
        print("    %-9s AL BIT %s; la differenza relativa massima %.3e" % (x, bit, float(np.max(np.abs(riu[x] - oggi[x]))) / den))
        if not bit:
            diverse.append(x)
    print("-" * 130)
    print("### il tempo per tick: oggi %.3f s, col riuso %.3f s, il rapporto %.3f (la macchina CARICA); le fattorizzazioni costruite col riuso: %d" % (t_oggi, t_riu, t_oggi / t_riu, costr))
    passa = not diverse
    print("  DEVE PASSARE: %d tick col riuso = %d tick di oggi AL BIT (esclusa h_int)   %s   diverse: %s" % (N_TICK, N_TICK, "PASSA" if passa else "### FALLISCE", diverse))
    print("  DEVE PASSARE: una sola fattorizzazione per il campo   %s   %d" % ("PASSA" if costr == 1 else "### FALLISCE", costr))
    print("=" * 130)
    print("ESITO: %s" % ("AL BIT: il riuso per le corse NUOVE (Luca 15:07)" if passa and costr == 1 else "### NON AL BIT (o piu' fattorizzazioni): il riuso NON si usa; il perche' da scrivere"))
    return 0 if (passa and costr == 1) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
