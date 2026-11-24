# -*- coding: utf-8 -*-
r"""**[M0140] omega DURANTE LA CADUTA COL METODO DI 1b** *(DECISIONE DI LUCA, 2026-11-24 01:40; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-undecies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_omega.py noto          (M0140_omega_noto: la tenuta 1b da k 2500, 250 tick)
    E:\python\py3132\python.exe doc/referti_l2/caduta_omega.py corsa         (M0140_caduta_omega: la caduta V2 x1 rifatta, omega per tick)
    E:\python\py3132\python.exe doc/referti_l2/caduta_omega.py lettura >> doc/referti_l2/caduta_parti.txt

**`omega` per tick = `-arg <psi_prima | psi_dopo>`** *(come `tenuta_fondo.corsa`)*. **`noto`:** dalla tenuta 1b a `k 2500` *(`fondo_suite_v2.carica` con quello stato)*, il tick della tenuta per `250` tick *(`C.residuo` alla fase globale)*. **`corsa`:** `fondo_1c.caduta("V2")` con `BASE` = `M1658/c1_omega` e `fondo_1c.ciclo` avvolta *(registra `omega`, confronta `psi_h` con gli stati di `c1_parti` ogni `250`; non salva stati)*.
"""
import argparse
import hashlib
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import fondo_1c as F1  # noqa: E402
import tenuta_fondo as TF  # noqa: E402

CTRL = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658")
TEN = os.path.join(CTRL, "tenuta", "L-1_proiezione_K")
PARTI = os.path.join(CTRL, "c1_parti", "caduta_V2")
BASE_O = os.path.join(CTRL, "c1_omega")
K0, PASSO = 2500, 250


def scrivi(nome, dati):
    os.makedirs(BASE_O, exist_ok=True)
    f = os.path.join(BASE_O, nome)
    assert not os.path.exists(f), "%s c'e' gia': non si riscrive" % f
    open(f, "w", encoding="utf-8").write(json.dumps(dati))
    open(f + ".sha1", "w", encoding="utf-8").write(hashlib.sha1(open(f, "rb").read()).hexdigest() + "\n")


def leggi(nome):
    f = os.path.join(BASE_O, nome)
    if not os.path.exists(f + ".sha1"):
        return None
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == hashlib.sha1(open(f, "rb").read()).hexdigest()
    return json.load(open(f, encoding="utf-8"))


def omega_di(prima, dopo):
    return float(-np.angle(np.vdot(prima, dopo)))


def noto():
    import _presidio
    import ripresa_F0_v2 as RF
    import gravita_due_corpi_misure as GM
    F1.avvia()
    TF.avvia()
    _presidio.avvia(__file__)
    f0 = os.path.join(TEN, "stato_%06d.npz" % K0)
    F1.FS.stato_di = lambda sorgente, kstato: f0
    MV, P0 = F1.TT.nucleo()
    _G20, _ia, e0, MT = F1.CL.parametri()
    om = []
    with F1.TC.scena() as Z:
        C, info, _dxy, _forma, _X = F1.FS.carica(Z, "K", K0)
        n, s = Z["n"], float(Z["s"])
        N = np.ones(n)
        print("### noto: %s; OGNI_GAUSS %d; la fase globale da %d" % (info["file"], MT.OGNI_GAUSS, K0))
        with RF.col_nucleo(MV, P0), MV.forma_esplicita("L-1"):
            assert MV.ATTIVA == "L-1" and MV.pezzi is P0
            for kk in range(1, PASSO + 1):
                prima = Z["st"]["psi_h"].copy()
                F1.CS.tick_var(Z["z"], C.campo, s, e0, N, False, 0)
                om.append(omega_di(prima, Z["st"]["psi_h"]))
                if (K0 + kk) % MT.OGNI_GAUSS == 0:
                    C.residuo()
        psi = Z["st"]["psi_h"].copy()
        Z["metti"]()
    X, _m = GM.leggi(os.path.join(TEN, "stato_%06d.npz" % (K0 + PASSO)))
    al_bit = bool(np.array_equal(psi, X["psi_h"]))
    dmax = float(np.max(np.abs(psi - X["psi_h"])))
    scrivi("noto.json", {"omega": om, "al_bit": al_bit, "dmax": dmax, "da": f0})
    print("### %d tick; omega medio %+.7f; psi_h a %d = lo stato salvato AL BIT: %s (max |d| %.1e)" % (PASSO, float(np.mean(om)), K0 + PASSO, al_bit, dmax))
    return 0


def corsa():
    import _presidio
    import gravita_due_corpi_misure as GM
    TF.avvia()
    _presidio.avvia(__file__)
    F1.BASE = BASE_O
    vero_ciclo = F1.ciclo

    def ciclo(Z, C, quanti, dopo, MV, P0, N, cs_N, segno):
        om, ug = [], []

        def confronta(kk):
            X, _m = GM.leggi(os.path.join(PARTI, "stato_%06d.npz" % kk))
            u = bool(np.array_equal(Z["st"]["psi_h"], X["psi_h"]))
            ug.append((kk, u))
            print("    [confronto] k %d: psi_h = c1_parti AL BIT: %s; omega dell'ultimo tick %+.7f" % (kk, u, om[-1] if om else float("nan")))
            sys.stdout.flush()

        def dopo2(kk, prima):
            dopo(kk, prima)
            om.append(omega_di(prima, Z["st"]["psi_h"]))
            if kk % PASSO == 0:
                confronta(kk)
        confronta(0)
        vero_ciclo(Z, C, quanti, dopo2, MV, P0, N, cs_N, segno)
        scrivi("omega.json", {"omega": om, "uguali": ug})
    F1.ciclo = ciclo
    return F1.caduta("V2")


def lettura():
    import _presidio
    F1.avvia()
    _presidio.avvia(__file__)
    print("-" * 130)
    print("[M0140] LA COLONNA omega, V2: omega per tick = -arg <psi_prima|psi_dopo> (il metodo di tenuta_fondo.corsa, 1b) (la carta sez. 2-undecies)")
    print("-" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    nt, oj = leggi("noto.json"), leggi("omega.json")
    if nt is None or oj is None:
        print("  NON FINITA")
        return 0
    om1b = np.load(os.path.join(TEN, "omega.npy"))
    mio = float(np.mean(nt["omega"]))
    rif = float(om1b[K0:K0 + PASSO].mean())
    esito("il caso noto: omega medio [%d, %d] dalla tenuta 1b ripresa = omega.npy entro 1e-4" % (K0 + 1, K0 + PASSO), abs(mio - rif) <= 1e-4, "%+.7f contro %+.7f (|d| %.1e)" % (mio, rif, abs(mio - rif)))
    print("        (piu' stretto: psi_h a %d AL BIT %s, max |d| %.1e; omega per tick uguale a omega.npy AL BIT: %s)" % (K0 + PASSO, nt["al_bit"], nt["dmax"], list(nt["omega"]) == [float(x) for x in om1b[K0:K0 + PASSO]]))
    altra = float(om1b[K0 - PASSO:K0].mean())
    esito("DEVE FALLIRE: omega.npy su [%d, %d] (un'altra finestra) contro il misurato, oltre 1e-4" % (K0 - PASSO + 1, K0), abs(altra - mio) > 1e-4, "%+.7f contro %+.7f (|d| %.1e)%s" % (altra, mio, abs(altra - mio), "" if abs(altra - mio) > 1e-4 else " ### omega costante entro 1e-4: il caso noto NON distingue"))
    F1.BASE = BASE_O
    t = F1.leggi("caduta_V2")
    F1.BASE = os.path.join(CTRL, "c1")
    v = F1.leggi("caduta_V2")
    esito("la caduta rifatta: la serie = M1658/c1/caduta_V2 AL BIT", t["serie"] == v["serie"])
    ug = oj["uguali"]
    esito("la caduta rifatta: psi_h = gli stati di c1_parti AL BIT a ogni 250 (%d confronti)" % len(ug), all(u for _k, u in ug), str([k for k, u in ug if not u]))
    om = np.array(oj["omega"])
    fin = [(k, float(om[k:k + PASSO].mean()), float(om[k:k + PASSO].std() / np.sqrt(PASSO))) for k in range(0, len(om), PASSO)]
    for k, m, s in fin:
        print("  omega [%4d, %4d] %+.7f +- %.1e" % (k + 1, k + PASSO, m, s))
    print("### omega: l'ultima finestra - la prima %+.3e; il minimo %+.7f, il massimo %+.7f; il gap (0.011870, 0.245338)" % (fin[-1][1] - fin[0][1], min(x[1] for x in fin), max(x[1] for x in fin)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE della colonna omega: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("noto", "corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"noto": noto, "corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
