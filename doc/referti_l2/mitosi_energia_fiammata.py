# -*- coding: utf-8 -*-
r"""**[M0237-2] L'ENERGIA LUNGO LA FIAMMATA** *(DECISIONE DI LUCA, 2026-11-25 02:37, dalla posta; la carta `doc/CARTA_mitosi.md`, «Le tre prove»; a costo zero: stati e registri gia' salvati)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/mitosi_energia_fiammata.py > doc/referti_l2/mitosi_energia_fiammata.txt

**`H(k)`** = la serie `E` *(ogni `50` tick)* di TRONCO, MITOSI, MITOSI_V2; **`E_persa(k)`** = la serie `D_epersa`; **i nodi `n(k)`** = `n` del meta di `stato_36000` meno le sue nascite, piu' le nascite a `k` *(una nascita, un nodo: dichiarato)*; **`DH` per nascita** dai `nascite_*.json`. **(K1)** `H` di `stato_36000` rifatto da `mitosi_regola.energia_corsa` *(lo stato ripreso con `mitosi_lunga.riprendi`, il lapse acceso come nella corsa)* contro la serie `E` a `k 36000`: **il meta non porta `H`, dichiarato.** **(K2)** `-somma DH` = `E_persa` finale entro `1e-9` relativo. **Il verdetto S3:** `|dH|/|H|` fra l'inizio *(il punto della serie piu' vicino a `k 36294`)* e la fine della fiammata, contro `3` volte la deriva di fondo *(`1.891e-05`, il pezzo 0)*.
"""
import glob
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
for _p in (_QUI, os.path.join(_QUI, "..", "..", "csv")):
    if os.path.abspath(_p) not in sys.path:
        sys.path.insert(0, os.path.abspath(_p))
import mitosi_dati as MD  # noqa: E402

R = MD.R
K_FIAMMATA = 36294
DERIVA = 1.891e-05     # ### dal pezzo 0 (mitosi_dati.txt)


def main():
    import _presidio
    import mitosi_lunga as ML
    _presidio.avvia(os.path.join(_QUI, "mitosi_dati.py"))
    _presidio.avvia(os.path.join(_QUI, "mitosi_lunga.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0237-2] L'ENERGIA LUNGO LA FIAMMATA (la carta doc/CARTA_mitosi.md, Le tre prove): H(k), E_persa(k), n(k), DH per nascita; il verdetto S3")
    print("=" * 130)
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
        sys.stdout.flush()
    S = {c: MD.serie(c)[1] for c in MD.CORSE}
    # ### (K1)
    PS = ML.PS
    MT = PS.MT
    f36 = os.path.join(R, "MITOSI", "stato_36000.npz")
    PS.presidi()
    with PS.CV.scena_L(186, PS.FATTORE_R_A * PS.R_OGG_MAX) as Z:
        C, NS, meta, cs = ML.riprendi(Z, f36, MT.rho_c_assoluto(), MT.PB.E_DECISO, True)
        PS.PO.accendi(cs)
        try:
            H36 = ML.MR.energia_corsa(Z, C)
            n36, nas36 = int(Z["mot"].inc.n), int(meta.get("nascite", -1))
        finally:
            PS.LC.spegni()
    km = S["MITOSI"]["k"]
    E36 = float(S["MITOSI"]["E"][int(np.where(km == 36000)[0][0])])
    esito("(K1) H di stato_36000 da energia_corsa = la serie E a k 36000 AL BIT (il meta non porta H)", H36 == E36, "%+.12e contro %+.12e (diff %.3e)" % (H36, E36, H36 - E36))
    # ### le nascite e K2
    N = {}
    for c in ("MITOSI", "MITOSI_V2"):
        for x in json.load(open(MD.ultimo(c, "nascite"), encoding="utf-8")):
            N.setdefault((int(x["k"]), int(x["a"])), x)
    nasc = [N[q] for q in sorted(N)]
    DH = np.array([float(x["DH"]) for x in nasc])
    ks = np.array([int(x["k"]) for x in nasc])
    ep = float(nasc[-1]["E_persa"])
    r = abs(-float(DH.sum()) - ep) / abs(ep)
    esito("(K2) -somma DH delle %d nascite = E_persa finale entro 1e-9 relativo" % len(DH), r < 1e-9, "-somma DH %+.12e, E_persa %+.12e, |d|/|E_persa| %.3e" % (-float(DH.sum()), ep, r))
    print("  DH per nascita: medio %+.4f, da %+.4f a %+.4f; negativi %d su %d; DH_nascita medio %+.4f, DH_flip medio %+.4f" % (
        float(DH.mean()), float(DH.min()), float(DH.max()), int((DH < 0).sum()), len(DH), float(np.mean([x["DH_nascita"] for x in nasc])), float(np.mean([x["DH_flip"] for x in nasc]))))
    n0 = n36 - nas36
    print("  i nodi: n(36000) %d con %d nascite: n0 %d; n(fine) %d" % (n36, nas36, n0, n0 + len(ks)))
    # ### H(k) lungo il tempo
    print("-" * 130)
    print("  H(k), E_persa(k), H + E_persa, le nascite e i nodi, ogni 500 tick (dalle serie)")
    print("-" * 130)
    kk = np.concatenate([S[c]["k"] for c in MD.CORSE])
    EE = np.concatenate([S[c]["E"] for c in MD.CORSE])
    EP = np.concatenate([S["TRONCO"]["D_epersa"] if "D_epersa" in S["TRONCO"] else np.zeros(len(S["TRONCO"]["k"]))] + [S[c]["D_epersa"] for c in ("MITOSI", "MITOSI_V2")])
    o = np.argsort(kk, kind="stable")
    kk, EE, EP = kk[o], EE[o], EP[o]
    for k0 in list(range(26000, 36001, 2000)) + list(range(36000, 46001, 500)):
        i = int(np.argmin(np.abs(kk - k0)))
        nn = int((ks <= kk[i]).sum())
        print("    k %5d: H %+.10e  E_persa %+.6e  H + E_persa %+.10e  nascite %3d  n %d" % (int(kk[i]), float(EE[i]), float(EP[i]), float(EE[i] + EP[i]), nn, n0 + nn))
    ia = int(np.argmin(np.abs(kk - K_FIAMMATA)))
    ib = len(kk) - 1
    dH = float(EE[ib] - EE[ia])
    rr = abs(dH) / abs(float(EE[ia]))
    ver = "FERMA" if rr <= 3.0 * DERIVA else ("CRESCE" if dH > 0 else "CALA")
    print("-" * 130)
    print("### IL VERDETTO S3: H(%d) %+.10e, H(%d) %+.10e; dH %+.6e; |dH|/|H| %.3e contro 3 x deriva %.3e: %s" % (int(kk[ia]), float(EE[ia]), int(kk[ib]), float(EE[ib]), dH, rr, 3.0 * DERIVA, ver))
    dHp = float((EE[ib] + EP[ib]) - (EE[ia] + EP[ia]))
    print("### e H + E_persa sullo stesso tratto: %+.6e (|.|/|H| %.3e)" % (dHp, abs(dHp) / abs(float(EE[ia]))))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
