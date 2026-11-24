# -*- coding: utf-8 -*-
r"""**[M0100] LA CADUTA PER PARTI** *(DECISIONE DI LUCA, 2026-11-24 01:00; la carta `doc/CARTA_fondo_giusto.md`, sez. `2-nonies`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/caduta_parti.py base          (Q_K, prima della corsa, un processo a parte)
    E:\python\py3132\python.exe doc/referti_l2/caduta_parti.py corsa         (M0100_caduta_parti, dalla coda)
    E:\python\py3132\python.exe doc/referti_l2/caduta_parti.py lettura > doc/referti_l2/caduta_parti.txt

**`fondo_1c.caduta("V2")` cosi' com'e'**, con `fondo_1c.BASE` = `M1658/c1_parti` e, IN MEMORIA, `fondo_1c.ciclo` avvolta *(dopo il `dopo` di `caduta`: le parti ogni `10` tick, lo stato ogni `250`)* e `fondo_suite_v2.carica` avvolta *(solo per tenere `dxy` e `info`)*. **Le parti:** `psi_K = psi Q_K* Q_K^T` nodo per nodo *(`Q_K` = `tenuta_fondo.base_k(Z, "K")`, la base della semina)*, `psi_R = psi - psi_K`.
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

BASE_P = os.path.join("E:" + os.sep, "soliton_simulator", "controllo", "M1658", "c1_parti")
BASE_1C = F1.BASE
F_Q = os.path.join(BASE_P, "Q_K.npz")
D_ST = os.path.join(BASE_P, "caduta_V2")
OGNI_STATO, OGNI_PARTI = 250, 10
FINESTRE = ((200, 800), (800, 1400), (1400, 2000))


def sha1(f):
    return hashlib.sha1(open(f, "rb").read()).hexdigest()


def firma(f):
    open(f + ".sha1", "w", encoding="utf-8").write(sha1(f) + "\n")


def controlla(f):
    assert open(f + ".sha1", encoding="utf-8").read().split()[0] == sha1(f), "lo sha1 di %s NON coincide" % f


def calcola_Q():
    with TF.TC.scena() as Z:
        Q, E, m, kv = TF.base_k(Z, "K")
    return Q, E, m, kv


def base():
    import _presidio
    TF.avvia()
    _presidio.avvia(__file__)
    assert not os.path.exists(F_Q), "%s c'e' gia': non si riscrive" % F_Q
    Q, E, m, kv = calcola_Q()
    os.makedirs(BASE_P, exist_ok=True)
    np.savez(F_Q, Q=Q, E=np.array(E), m=np.array(m), kv=kv)
    firma(F_Q)
    print("### Q_K: %s; E %+.7f, la molteplicita' %d, K %s; Q^dag Q - 1: %.1e; sha1 %s" % (
        Q.shape, E, m, kv.tolist(), float(np.max(np.abs(Q.conj().T @ Q - np.eye(Q.shape[1])))), sha1(F_Q)[:8]))
    return 0


def leggi_Q():
    controlla(F_Q)
    with np.load(F_Q) as z:
        return z["Q"].copy()


def parti(psi_h, Q, n, dxy):
    psi = psi_h.reshape(n, 12)
    pk = psi @ Q.conj() @ Q.T
    rK = np.sum(np.abs(pk) ** 2, axis=1)
    rR = np.sum(np.abs(psi - pk) ** 2, axis=1)
    bK = (dxy * rK[:, None]).sum(axis=0) / rK.sum()
    bR = (dxy * rR[:, None]).sum(axis=0) / rR.sum()
    return float(rK.sum()), float(rR.sum()), float(bK[0]), float(bK[1]), float(bR[0]), float(bR[1])


def corsa():
    import _presidio
    TF.avvia()
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
        assert Z["mot"].inc.n == n, "mot.inc.n %d contro Z[n] %d" % (Z["mot"].inc.n, n)
        rho_b = np.bincount(nodo, weights=np.sum(np.abs(Z["st"]["psi_h"]) ** 2, axis=1), minlength=n)
        rho_r = np.sum(np.abs(Z["st"]["psi_h"].reshape(n, 12)) ** 2, axis=1)
        assert np.max(np.abs(rho_b - rho_r)) <= 1e-12 * float(rho_b.max()), "reshape(n, 12) NON e' per nodo: FERMO"
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
            print("    [stato] k %d sha1 %s; f_K %.6f, y_K %+.5f, y_R %+.5f" % (kk, sha1(fz)[:8], serie[-1][1] / (serie[-1][1] + serie[-1][2]), serie[-1][4], serie[-1][6]))
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
        open(fp, "w", encoding="utf-8").write(json.dumps({"colonne": ["k", "norma_K", "norma_R", "x_K", "y_K", "x_R", "y_R"], "serie": serie}))
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
    _presidio.avvia(os.path.join(_QUI, "caduta_finestre.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0100] LA CADUTA PER PARTI (la carta sez. 2-nonies): psi_K = psi Q_K* Q_K^T nodo per nodo, psi_R = psi - psi_K")
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
    P = np.array(json.load(open(fp, encoding="utf-8"))["serie"])
    Q = leggi_Q()
    controlla(os.path.join(D_ST, "dxy.npy"))
    dxy = np.load(os.path.join(D_ST, "dxy.npy"))
    n = dxy.shape[0]
    OK = {}

    def esito(che, ok, nota=""):
        OK[che] = bool(ok)
        print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    esito("CN1 la serie del totale = M1658/c1/caduta_V2 AL BIT", tot["serie"] == vec["serie"], "(%d punti)" % len(tot["serie"]))
    S = np.array(tot["serie"])
    assert np.array_equal(S[:, 0], P[:, 0]), "i k della serie e delle parti NON coincidono"
    y_ric = (P[:, 1] * P[:, 4] + P[:, 2] * P[:, 6]) / (P[:, 1] + P[:, 2])
    d2 = float(np.max(np.abs(y_ric - S[:, 2])))
    esito("CN2 (f_K y_K + f_R y_R) = y entro 1e-12 a ogni punto", d2 <= 1e-12, "max %.1e" % d2)
    X, _m = GM.leggi(os.path.join(D_ST, "stato_002000.npz"))
    p3 = parti(X["psi_h"], Q, n, dxy)
    esito("CN3 le parti dallo stato salvato a k 2000 = la serie AL BIT", tuple(P[-1, 1:]) == p3)
    pf = parti(X["psi_h"], 1.1 * Q, n, dxy)
    yf = (pf[0] * pf[3] + pf[1] * pf[5]) / (pf[0] + pf[1])
    df = abs(yf - S[-1, 2])
    esito("DEVE FALLIRE: CN2 con 1.1 Q_K (non un proiettore) a k 2000", df > 1e-12, "|d y| %.1e%s" % (df, "" if df > 1e-12 else " ### NON FALLISCE"))
    Q2 = calcola_Q()[0]
    esito("CN4 Q_K ricalcolato = il file AL BIT", np.array_equal(Q2, Q))
    print("  LE FRAZIONI f_K = norma_K/(norma_K + norma_R): " + "; ".join("k %d: %.6f" % (int(P[i, 0]), P[i, 1] / (P[i, 1] + P[i, 2])) for i in range(0, len(P), 50)) + "; k 2000: %.6f" % (P[-1, 1] / (P[-1, 1] + P[-1, 2])))
    righe = {"y_K": P[:, 4], "y_R": P[:, 6], "y totale": S[:, 2]}
    for nome, y in righe.items():
        ps = [(float(k), 0.0, float(v), 0.0) for k, v in zip(P[:, 0], y)]
        fs = [CF.fit(ps, *w) for w in FINESTRE]
        print("  %-9s: " % nome + "; ".join("[%4d, %4d] a %+.4e +- %.1e" % (w[0], w[1], a, sa) for w, (a, sa, _n) in zip(FINESTRE, fs)))
    fs0 = [CF.fit(v0["serie"], *w) for w in FINESTRE]
    print("  (riferimento) la V0 del TOTALE di 1c: " + "; ".join("[%4d, %4d] a %+.4e +- %.1e" % (w[0], w[1], a, sa) for w, (a, sa, _n) in zip(FINESTRE, fs0)) + "  ### NON c'e' la V0 per parti: le a per parte sono GREZZE")
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("cosa", choices=("base", "corsa", "lettura"))
    a = ap.parse_args(argv)
    return {"base": base, "corsa": corsa, "lettura": lettura}[a.cosa]()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
