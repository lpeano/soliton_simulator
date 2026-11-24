# -*- coding: utf-8 -*-
r"""**[M0118-02] K A PARITA' DI MASSA, FORMA DIVERSA -- LA LETTURA NELLE DUE CONVENZIONI** *(DECISIONE DI LUCA [M0118-00], 01:25: la convenzione della sagoma e' quella della cima; `k_forma.py` era in uso dalle corse e non si tocca)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/k_forma_v2.py > doc/referti_l2/k_forma.txt

**Per 1c, a2, l0.7:** `m*`, **K VUOTO e K CIMA** *(`fondo_s3_v2.due_K`, `omega_psi(N1)` dell'orologio V2 di 1c)* sull'intera `[200, 2000]` e sulle finestre di `600`; **per l0.7 anche con `m*(1c)`** *(«a parita' di massa»)*; **le eta a due a due** su `[200, 2000]` *(non dipendono dalla convenzione)*.
"""
import math
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import k_forma as KF  # noqa: E402
import fondo_s3_v2 as S3V2  # noqa: E402

F1 = KF.F1


def lettura():
    import _presidio
    import caduta_finestre as CF
    F1.avvia()
    for m in ("k_forma.py", "eotvos_fondo.py", "fondo_s3_v2.py", "caduta_finestre.py"):
        _presidio.avvia(os.path.join(_QUI, m))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0118-02] K A PARITA' DI MASSA, FORMA DIVERSA, NELLE DUE CONVENZIONI: 1c, a2 (norma x4), l0.7 (larghezza 0.7)")
    print("=" * 130)
    F1.BASE = KF.BASE_1C
    dD, w1 = S3V2.pendenze()
    print("  d Delta/dN %+.6f (VUOTO); omega_psi(N1) %+.7f (CIMA, l'orologio V2 di 1c a N 1)" % (dD, w1))
    R = {}
    for nome, base in (("1c", KF.BASE_1C), ("a2", KF.BASE_A2), ("l0.7", KF.BASE_L07)):
        x = KF.legge(base)
        if x is None:
            print("  %s: NON FINITA" % nome)
            continue
        ms, sms, s2, s0, A = x
        R[nome] = dict(ms=ms, A=A, s2=s2, s0=s0)
        print("  %-5s m* %+.4f +- %.4f:" % (nome, ms, sms))
        for w in S3V2.FINESTRE:
            a, sa, _ = CF.fit(s2, *w)
            a0, sa0, _ = CF.fit(s0, *w)
            da, sda = a - a0, math.hypot(sa, sa0)
            kv, kc, sv, scc = S3V2.due_K(da, sda, A, ms, dD, w1)
            if w == (200, 2000):
                R[nome].update(da=da, sda=sda, kv=kv, kc=kc)
            print("    [%4d, %4d]: a - a(V0) %+.4e +- %.1e;   K VUOTO %+.4f +- %.4f;   K CIMA %+.4f +- %.4f" % (w[0], w[1], da, sda, kv, sv, kc, scc))
    if "l0.7" in R and "1c" in R:
        r, r1 = R["l0.7"], R["1c"]
        kv1, kc1, _sv, _sc = S3V2.due_K(r["da"], r["sda"], r["A"], r1["ms"], dD, w1)
        print("### l0.7 con m*(1c) (a parita' di massa): K VUOTO %+.4f, K CIMA %+.4f; con m*(l0.7): K VUOTO %+.4f, K CIMA %+.4f" % (kv1, kc1, r["kv"], r["kc"]))
        print("### K(l0.7)/K(1c) (lo stesso nelle due convenzioni): %.4f con m*(l0.7), %.4f con m*(1c)" % (r["kc"] / r1["kc"], kc1 / r1["kc"]))
    nomi = [x for x in ("1c", "a2", "l0.7") if x in R]
    for i in range(len(nomi)):
        for j in range(i + 1, len(nomi)):
            p, q = R[nomi[i]], R[nomi[j]]
            eta = 2.0 * abs(p["da"] - q["da"]) / (p["da"] + q["da"])
            se = 4.0 * math.hypot(q["da"] * p["sda"], p["da"] * q["sda"]) / (p["da"] + q["da"]) ** 2
            print("### eta(%s, %s) = %.4f +- %.4f (su [200, 2000])" % (nomi[i], nomi[j], eta, se))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(lettura())
