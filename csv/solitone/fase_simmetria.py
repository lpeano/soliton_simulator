# -*- coding: utf-8 -*-
r"""**LA FASE DEL MATTONE E' UNA SIMMETRIA?** *(Luca `2026-11-15` `01:12`; la carta `doc/TASK_HISTORY/2026-11-13_strumento_mattone.md`, sez. `21.8`)*.

    python csv/solitone/fase_simmetria.py > doc/referti_l2/mattone/fase_simmetria.txt

**Il mattone cotto su `L 162`** *(`L162_MGU_03000`, lo stato col campo; `U` ricostruito dal campo, `d9318470`)* **da solo nella sua scena** *(S162, il bordo da `R_A 60` come (T-solo) che l'ha cotto)*, **G+U, `20` tick col
tick di `mattone.Campi`:** **(i) com'e'; (ii) con `psi` moltiplicato per `exp(i theta)` all'inizio, `theta = pi` e `theta = 2 pi / 3`.**
### **DEVE:** **(ii) dopo `20` tick = `exp(i theta)` per (i) dopo `20` tick: `psi` AL BIT** *(per `theta = pi`: la moltiplicazione per `-1` e' esatta)* **o entro `1e-12` relativo** *(per `2 pi / 3`: la moltiplicazione
per un complesso non e' esatta in virgola mobile; dichiarato)*; **`phi`, `rho`, `Lambda`, `campo_E`, `campo_A` UGUALI AL BIT** *(se non lo sono, si scrive di quanto)*. **`h_int` esclusa** *(chiave di servizio)*.
"""
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
_CSV = os.path.dirname(_QUI)
for _p in (_QUI, _CSV):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import mattone as MT  # noqa: E402
import mattone_cottura_U as CU  # noqa: E402
import mattone_triangolo as MTR  # noqa: E402

N_TICK = 20
TOLL_PSI = 1e-12
PSI = ("psi_h", "psi")                  # ### le due chiavi della materia nello stato: girate tutte e due, confrontate tutte e due
TETA = (("pi", math.pi), ("2 pi / 3", 2.0 * math.pi / 3.0))
OK = [0, 0]
FALLITE = []


def esito(che, passa, nota):
    OK[1] += 1
    OK[0] += 1 if passa else 0
    if not passa:
        FALLITE.append(che)
    print("  DEVE PASSARE: %-100s %s   %s" % (che[:100], "PASSA" if passa else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import json
    import _presidio
    import _u1_prototipo as U1
    from solitone import bordo as BO
    for m in ("mattone", "mattone_cottura_U", "mattone_triangolo"):
        _presidio.avvia(os.path.join(_QUI, m + ".py"))
    _presidio.avvia(__file__)
    rho_c = MT.rho_c_assoluto()
    e = MT.PB.E_DECISO
    with open(os.path.join(MT.DIR_REF, "cottura_L162_MGU.json"), encoding="utf-8") as fh:
        ct = json.load(fh)
    t_s = int(ct["t"])
    print("=" * 130)
    print("LA FASE DEL MATTONE E' UNA SIMMETRIA? (Luca 01:12): %s da solo nella scena di S162, il bordo da R_A %g, G+U, %d tick; (i) com'e', (ii) psi x exp(i theta)" % (ct["file"], MTR.R_A_SCENA, N_TICK))
    print("=" * 130)
    with MT.scena(MT.CORSA_162, MT.T_162) as Z:
        c0 = Z["bordo"]["c0"]
        Z["g_e"] = BO.g_estremita(Z["z"], c0[0], c0[1], MTR.R_A_SCENA, Z["bordo"]["g_max"])[0]
        with np.load(ct["file"]) as d:
            dati = {x: d[x].copy() for x in Z["chiavi"]}
            A0, E0 = d["campo_A"].copy(), d["campo_E"].copy()

        def gira(theta):
            Z["metti"](dati)
            C = MT.Campi(Z, "MGU", rho_c, e)
            C.campo.A[...] = A0
            C.campo.E[...] = E0
            C.campo.e = e
            C.e_prec = e
            U1.scrivi_U(Z["mot"], C.campo)
            if theta is not None:
                for x in PSI:
                    if x in Z["st"]:
                        Z["st"][x][...] = Z["st"][x] * np.exp(1j * theta)
            for k in range(1, N_TICK + 1):
                C.tick(k, t_s + k, 1.0, e)
            out = {x: Z["st"][x].copy() for x in Z["chiavi"]}
            out.update(campo_A=C.campo.A.copy(), campo_E=C.campo.E.copy())
            return out
        base = gira(None)
        for nome, th in TETA:
            g = gira(th)
            for xp in PSI:
                if xp not in g:
                    continue
                atteso = base[xp] * np.exp(1j * th)
                dpsi = float(np.max(np.abs(g[xp] - atteso))) / (float(np.max(np.abs(atteso))) or 1.0)
                bit = bool(np.array_equal(g[xp], atteso))
                print("### theta = %s: %s contro exp(i theta) %s(i): AL BIT %s; la differenza relativa massima %.3e" % (nome, xp, xp, bit, dpsi))
                esito("theta %s: %s = exp(i theta) %s(i) %s" % (nome, xp, xp, "AL BIT" if th == math.pi else "entro %g relativo (dichiarato)" % TOLL_PSI), bit if th == math.pi else dpsi <= TOLL_PSI, "%.3e" % dpsi)
            for x in sorted(k for k in g if k not in PSI and k not in CU.CHIAVI_SERVIZIO):
                u = bool(np.array_equal(g[x], base[x]))
                den = float(np.max(np.abs(base[x]))) or 1.0
                print("    %-10s uguale AL BIT %s; la differenza relativa massima %.3e" % (x, u, float(np.max(np.abs(g[x] - base[x]))) / den))
                if x in ("phi_h", "rho", "Lambda", "campo_E", "campo_A"):
                    esito("theta %s: %s uguale AL BIT" % (nome, x), u, "%.3e" % (float(np.max(np.abs(g[x] - base[x]))) / den))
    print("=" * 130)
    print("ESITO: %d/%d controlli come devono; fallite %s" % (OK[0], OK[1], FALLITE))
    return 0 if not FALLITE else 1


if __name__ == "__main__":
    sys.exit(main())
