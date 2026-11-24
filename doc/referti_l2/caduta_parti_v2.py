# -*- coding: utf-8 -*-
r"""**[M0100] LA CADUTA PER PARTI -- LA V2: PER CELLA** *(la v1 `caduta_parti.py` cadde all'avvio sul mio assert, `859a4067`: `psi_h.reshape(n, 12)` e' la CELLA `v` -- i tre archi uscenti --, non il nodo; la carta sez. `2-nonies-bis`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_parti_v2.py corsa         (M0100_caduta_parti_v2, dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/caduta_parti_v2.py lettura > doc/referti_l2/caduta_parti.txt

`Q_K` dal file della v1 *(`caduta_parti.py base`)*. **Le parti cella per cella**, il baricentro con la posizione del nodo `v` della cella; **il totale anche per cella** (`y_T`), accanto a quello per nodo della serie di `fondo_1c.caduta`.
"""
import argparse
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import caduta_parti as CP  # noqa: E402

F1, TF = CP.F1, CP.TF
BASE_P, BASE_1C, D_ST, FINESTRE = CP.BASE_P, CP.BASE_1C, CP.D_ST, CP.FINESTRE
OGNI_STATO, OGNI_PARTI = CP.OGNI_STATO, CP.OGNI_PARTI
sha1, firma, controlla, leggi_Q, calcola_Q = CP.sha1, CP.firma, CP.controlla, CP.leggi_Q, CP.calcola_Q
COLONNE = ["k", "norma_K", "norma_R", "x_K", "y_K", "x_R", "y_R", "x_T", "y_T"]


def parti(psi_h, Q, n, dxy):
    """### per CELLA: `(n_K, n_R, x_K, y_K, x_R, y_R, x_T, y_T)`."""
    psi = psi_h.reshape(n, 12)
    pk = psi @ Q.conj() @ Q.T
    rK = np.sum(np.abs(pk) ** 2, axis=1)
    rR = np.sum(np.abs(psi - pk) ** 2, axis=1)
    rT = np.sum(np.abs(psi) ** 2, axis=1)
    b = [(dxy * r[:, None]).sum(axis=0) / r.sum() for r in (rK, rR, rT)]
    return (float(rK.sum()), float(rR.sum())) + tuple(float(v) for bb in b for v in bb)


def corsa():
    import _presidio
    TF.avvia()
    _presidio.avvia(os.path.join(_QUI, "caduta_parti.py"))
    _presidio.avvia(__file__)
    Q = leggi_Q()
    assert not os.path.exists(D_ST), "%s c'e' gia': non si riscrive" % D_ST
    F1.BASE = BASE_P
    CAT = {}
    vero_carica, vero_ciclo = F1.FS.carica, F1.ciclo

    def carica(Z, *a):
        r = vero_carica(Z, *a)
        CAT["info"], CAT["dxy"] = r[1], r[2]
        return r

    def ciclo(Z, C, quanti, dopo, MV, P0, N, cs_N, segno):
        n, nodo, dxy = Z["n"], np.asarray(Z["mot"].inc.nodo), CAT["dxy"]
        assert Z["mot"].inc.n == n and Z["st"]["psi_h"].size == 12 * n, "le forme: inc.n %d, n %d, psi_h %s" % (Z["mot"].inc.n, n, Z["st"]["psi_h"].shape)
        code = nodo[0::2].reshape(n, 3)
        assert np.array_equal(code, np.repeat(np.arange(n)[:, None], 3, axis=1)), "le code dei tre archi della cella v NON sono v: FERMO"
        os.makedirs(D_ST)
        np.save(os.path.join(D_ST, "dxy.npy"), dxy)
        firma(os.path.join(D_ST, "dxy.npy"))
        serie = []

        def misura(kk):
            serie.append((kk,) + parti(Z["st"]["psi_h"], Q, n, dxy))

        def salva(kk):
            fz = os.path.join(D_ST, "stato_%06d.npz" % kk)
            dati = {x: Z["st"][x] for x in Z["chiavi"]}
            dati.update(campo_A=C.campo.A, campo_E=C.campo.E)
            np.savez(fz, meta=np.array(json.dumps(dict(CAT["info"], k=kk, coll="V2"))), **dati)
            firma(fz)
            u = serie[-1]
            print("    [stato] k %d sha1 %s; f_K %.6f, y_K %+.5f, y_R %+.5f, y_T %+.5f" % (kk, sha1(fz)[:8], u[1] / (u[1] + u[2]), u[4], u[6], u[8]))
            sys.stdout.flush()

        def dopo2(kk, prima):
            dopo(kk, prima)
            if kk % OGNI_PARTI == 0:
                misura(kk)
            if kk % OGNI_STATO == 0:
                salva(kk)
        misura(0)
        salva(0)
        vero_ciclo(Z, C, quanti, dopo2, MV, P0, N, cs_N, segno)
        fp = os.path.join(D_ST, "parti.json")
        open(fp, "w", encoding="utf-8").write(json.dumps({"colonne": COLONNE, "serie": serie}))
        firma(fp)

    F1.FS.carica = carica
    F1.ciclo = ciclo
    return F1.caduta("V2")


def lettura():
    import _presidio
    import gravita_due_corpi_misure as GM
    import caduta_finestre as CF
    F1.avvia()
    TF.avvia()
    for m in ("caduta_finestre.py", "caduta_parti.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0100] LA CADUTA PER PARTI, LA V2 (la carta sez. 2-nonies-bis): psi_K = psi Q_K* Q_K^T CELLA PER CELLA, psi_R = psi - psi_K")
    print("=" * 130)
    F1.BASE = BASE_P
    tot = F1.leggi("caduta_V2")
    F1.BASE = BASE_1C
    vec, v0 = F1.leggi("caduta_V2"), F1.leggi("caduta_V0")
    fp = os.path.join(D_ST, "parti.json")
    if tot is None or not os.path.exists(fp + ".sha1"):
        print("  NON FINITA")
        return 0
    controlla(fp)
    J = json.load(open(fp, encoding="utf-8"))
    assert J["colonne"] == COLONNE
    P = np.array(J["serie"])
    Q = leggi_Q()
    controlla(os.path.join(D_ST, "dxy.npy"))
    dxy = np.load(os.path.join(D_ST, "dxy.npy"))
    n = dxy.shape[0]
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    esito("CN1 la serie del totale (per nodo) = M1658/c1/caduta_V2 AL BIT", tot["serie"] == vec["serie"], "(%d punti)" % len(tot["serie"]))
    S = np.array(tot["serie"])
    assert np.array_equal(S[:, 0], P[:, 0]), "i k della serie e delle parti NON coincidono"
    y_ric = (P[:, 1] * P[:, 4] + P[:, 2] * P[:, 6]) / (P[:, 1] + P[:, 2])
    d2 = float(np.max(np.abs(y_ric - P[:, 8])))
    esito("CN2 (n_K y_K + n_R y_R)/(n_K + n_R) = y_T (cella) entro 1e-12 a ogni punto", d2 <= 1e-12, "max %.1e" % d2)
    X, _m = GM.leggi(os.path.join(D_ST, "stato_002000.npz"))
    p3 = parti(X["psi_h"], Q, n, dxy)
    esito("CN3 le parti dallo stato salvato a k 2000 = la serie AL BIT", tuple(P[-1, 1:]) == p3)
    pf = parti(X["psi_h"], 1.1 * Q, n, dxy)
    yf = (pf[0] * pf[3] + pf[1] * pf[5]) / (pf[0] + pf[1])
    df = abs(yf - pf[7])
    esito("DEVE FALLIRE: CN2 con 1.1 Q_K (non un proiettore) a k 2000", df > 1e-12, "|d y| %.1e%s" % (df, "" if df > 1e-12 else " ### NON FALLISCE"))
    Q2 = calcola_Q()[0]
    esito("CN4 Q_K ricalcolato = il file AL BIT", np.array_equal(Q2, Q))
    fK = P[:, 1] / (P[:, 1] + P[:, 2])
    print("  LE FRAZIONI f_K = n_K/(n_K + n_R): " + "; ".join("k %d: %.6f" % (int(P[i, 0]), fK[i]) for i in range(0, len(P), 50)) + "; k 2000: %.6f" % fK[-1])
    righe = (("y_K", P[:, 4]), ("y_R", P[:, 6]), ("y_T cella", P[:, 8]), ("y nodo", S[:, 2]))
    for nome, y in righe:
        ps = [(float(k), 0.0, float(v), 0.0) for k, v in zip(P[:, 0], y)]
        fs = [CF.fit(ps, *w) for w in FINESTRE]
        print("  %-9s: " % nome + "; ".join("[%4d, %4d] a %+.4e +- %.1e" % (w[0], w[1], a, sa) for w, (a, sa, _n) in zip(FINESTRE, fs)))
    fs0 = [CF.fit(v0["serie"], *w) for w in FINESTRE]
    print("  (riferimento) la V0 del TOTALE di 1c (per nodo): " + "; ".join("[%4d, %4d] a %+.4e +- %.1e" % (w[0], w[1], a, sa) for w, (a, sa, _n) in zip(FINESTRE, fs0)) + "  ### NON c'e' la V0 per parti: le a per parte sono GREZZE")
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
