# -*- coding: utf-8 -*-
r"""**[M2305] LE TENUTE AL FONDO A K, LA V2: AMPIEZZA E LARGHEZZA DELLA SEMINA** *(Luca, 2026-11-23 23:05; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-sexies`; `tenuta_fondo.py` e' usato -- 1b -- e non si riscrive: qui le sue funzioni, con `prepara` sostituita IN MEMORIA)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo_v2.py casi_noti > doc/referti_l2/tenuta_fondo_v2_casi_noti.txt
    E:\python\py3132\python.exe doc/referti_l2/tenuta_fondo_v2.py corsa --forma L-1 --ampiezza 0.5 --larghezza 1.0       (3000 tick)

**La semina** `proiezione_K` di 1b, in piu': **la larghezza** `s` -- lo stampo *(dopo `caduta_libera.prepara`, prima della portante)* ricampionato `psi(v) <- psi(nodo piu' vicino a c + (x_v - c)/s)`, riportato alla norma di prima; **l'ampiezza** `f` -- `psi` moltiplicato per `f` DOPO la proiezione. **Le cartelle:** `E:/soliton_simulator/controllo/M1658/tenuta_v2/<forma>_a<f>_l<s>`. **Il caso noto:** `f = 1`, `s = 1` a `k 0` = `M1658/tenuta/L-1_proiezione_K/stato_000000` AL BIT; **DEVE FALLIRE:** `s = 0.7` diverso.
"""
import argparse
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import tenuta_fondo as TF  # noqa: E402

DIR2 = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "tenuta_v2")
OK = {}


def esito(che, ok, nota=""):
    ok = None if ok is None else bool(ok)
    OK[che] = ok
    print("  DEVE: %-110s %s %s" % (che, {True: "PASSA", False: "### FALLISCE", None: "NON MISURATO"}[ok], nota))


def ricampiona(Z, info, s):
    """### lo stampo ricampionato di un fattore `s` attorno al centro, la norma di prima."""
    from solitone import toro as TO
    n, L = Z["mot"].inc.n, Z["L"]
    c = info["centro"]
    d = np.asarray(TO.scarti(Z["m1"], Z["m2"], c[0], c[1], L))[:, :2]
    A1, A2 = TO.vettori()
    Av = np.array([np.asarray(A1, float)[:2], np.asarray(A2, float)[:2]]).T
    dm = np.linalg.solve(Av, (d / float(s)).T).T
    m1 = (int(c[0]) + np.rint(dm[:, 0]).astype(np.int64)) % L
    m2 = (int(c[1]) + np.rint(dm[:, 1]).astype(np.int64)) % L
    src = m1 * L + m2
    assert np.all(np.asarray(Z["m1"])[np.arange(n)] * L + np.asarray(Z["m2"])[np.arange(n)] == np.arange(n)), "l'indice del nodo NON e' m1 L + m2"
    psi = Z["st"]["psi_h"].reshape(n, 12)
    norma = float(np.sum(np.abs(psi) ** 2))
    nuovo = psi[src].copy()
    nuovo *= math.sqrt(norma / float(np.sum(np.abs(nuovo) ** 2)))
    Z["st"]["psi_h"][...] = nuovo.reshape(Z["st"]["psi_h"].shape)


def con_semina(f, s):
    import caduta_libera as CL

    def prepara(Z, sem):
        assert sem == "proiezione_K", sem
        Z["_base"] = TF.base_k(Z, "K")
        C, info = CL.prepara(Z)
        if s != 1.0:
            ricampiona(Z, info, s)
        extra = TF.semina(Z, info, sem)
        Z.pop("_base", None)
        if f != 1.0:
            Z["st"]["psi_h"][...] = Z["st"]["psi_h"] * float(f)
        extra.update(ampiezza=float(f), larghezza=float(s))
        return C, info, extra
    TF.prepara = prepara


def corsa(forma, f, s, k_fino):
    con_semina(f, s)
    d_out = os.path.join(DIR2, "%s_a%.1f_l%.1f" % (forma, f, s))
    return TF.corsa(forma, "proiezione_K", k_fino, d_out=d_out)


def casi_noti():
    import gravita_due_corpi_misure as GM
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2305] I CASI NOTI DELLE SEMINE (in memoria)")
    print("=" * 130)
    X, _m = GM.leggi(os.path.join(TF.DIR, "L-1_proiezione_K", "stato_000000.npz"))
    S1 = {}
    con_semina(1.0, 1.0)
    TF.corsa("L-1", "proiezione_K", 0, salva_file=False, snap=S1)
    dv = [x for x in S1[0] if not np.array_equal(S1[0][x], X[x])]
    esito("la semina ampiezza 1, larghezza 1 a k 0 = M1658/tenuta/L-1_proiezione_K/stato_000000 AL BIT", not dv, "diversi %s" % dv)
    S2 = {}
    con_semina(1.0, 0.7)
    TF.corsa("L-1", "proiezione_K", 0, salva_file=False, snap=S2)
    esito("DEVE FALLIRE: la larghezza 0.7 diversa a k 0 (psi_h)", not np.array_equal(S2[0]["psi_h"], X["psi_h"]), "max|d psi_h| %.3e" % float(np.max(np.abs(S2[0]["psi_h"] - X["psi_h"]))))
    S3 = {}
    con_semina(2.0, 1.0)
    TF.corsa("L-1", "proiezione_K", 0, salva_file=False, snap=S3)
    r = float(np.sum(np.abs(S3[0]["psi_h"]) ** 2) / np.sum(np.abs(X["psi_h"]) ** 2))
    esito("l'ampiezza 2: la norma x4", abs(r - 4.0) < 1e-12, "%.15f" % r)
    fall = [k for k, v in OK.items() if v is False]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), sum(1 for v in OK.values() if v), len(fall), fall))
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("casi_noti", "corsa"))
    ap.add_argument("--forma")
    ap.add_argument("--ampiezza", type=float, default=1.0)
    ap.add_argument("--larghezza", type=float, default=1.0)
    ap.add_argument("--fino", type=int, default=3000)
    a = ap.parse_args(argv)
    if a.cosa == "casi_noti":
        return casi_noti()
    import _presidio
    _presidio.avvia(__file__)
    return corsa(a.forma, a.ampiezza, a.larghezza, a.fino)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
