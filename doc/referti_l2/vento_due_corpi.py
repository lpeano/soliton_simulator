# -*- coding: utf-8 -*-
r"""**[M2245-27] A5, IL VENTO A DUE CORPI** *(DECISIONE DI LUCA, 2026-11-27 22:45; la carta `doc/CARTA_mitosi.md`, A5; solo letture)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/vento_due_corpi.py > doc/referti_l2/vento_due_corpi.txt

**Gli stati:** `M2034/coppia/d1`, da `k 0` a `6000` ogni `250`. **I due corpi:** `coppia_a0.a0` *(i due massimi; gli stati non DUE si stampano e
restano fuori dalla media)*. **`J_phi`** = la formula di `vuoto_giro3.py` *(`rho_phi grad theta`, `theta` la fase di `somma conj(phi_v) phi` per nodo,
i nodi `(m1 +- 1, m2)`, `(m1 +- 1, m2 +- 2)`)*: **radiale attorno a ciascun corpo** negli anelli `[8, 16)` e `[16, 32)` *(negativo = verso il corpo)*;
**lungo l'asse:** i nodi a meno di `2` dal segmento fra i due corpi *(il parametro `t` in `[0, 1]`)*, `J` proiettata sul versore verso il punto
medio della coppia *(il baricentro: masse uguali)*, **positivo = verso il baricentro**. **Per finestra di `500`:** la media sugli stati DUE della finestra.
**Casi noti** *(quelli di `vuoto_giro3`, V1)*: sul vuoto fresco la corrente `0` entro `1e-9`; DEVE FALLIRE con una fase `q y`.
"""
import json
import math
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import coppia_a0 as A0  # noqa: E402
import vuoto_giro3 as VG  # noqa: E402

D1 = A0.D1
KS = list(range(0, 6001, 250))
ANELLI = ((8.0, 16.0), (16.0, 32.0))
LARGHEZZA_ASSE = 2.0
FIN = 500
OK = {}


def esito(che, ok, nota=""):
    OK[che] = bool(ok)
    print("  DEVE: %-100s %s %s" % (che, "PASSA" if ok else "### FALLISCE", nota))
    sys.stdout.flush()


def main():
    import _presidio
    VG.F1.avvia()
    _presidio.avvia(os.path.join(_QUI, "coppia_a0.py"))
    _presidio.avvia(os.path.join(_QUI, "vuoto_giro3.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M2245-27] A5, IL VENTO A DUE CORPI (la carta doc/CARTA_mitosi.md, A5): J_phi radiale attorno a ciascun corpo e lungo l'asse, M2034/coppia/d1")
    print("=" * 130)
    with VG.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        pv = np.asarray(Z["phi_v"]).copy()
        Z["metti"]()
    vic = (((m1 - 1) % L) * L + m2, ((m1 + 1) % L) * L + m2, ((m1 - 1) % L) * L + (m2 - 2) % L, ((m1 + 1) % L) * L + (m2 + 2) % L)
    # ### (V1)
    rv, Zv = VG.per_nodo(pv, pv, nodo, n)
    jx, jy = VG.correnti(rv, Zv, vic)
    jm = float(max(np.max(np.abs(jx)), np.max(np.abs(jy))))
    esito("(V1) il vuoto fresco: la corrente 0 entro 1e-9", jm < 1e-9, "max |J| %.1e" % jm)
    y = (m2 * VG.S3 / 2.0)[nodo]
    q = 2.0 * math.pi * 2.0 / (L * VG.S3 / 2.0)
    rq, Zq = VG.per_nodo(pv * np.exp(1j * q * y), pv, nodo, n)
    jx, jy = VG.correnti(rq, Zq, vic)
    esito("(V1) DEVE FALLIRE lo zero: una fase q y da' una corrente lungo y", float(np.max(np.abs(jy))) > 1e-6, "max |J_y| %.3e" % float(np.max(np.abs(jy))))
    meta = json.load(open(os.path.join(D1, "serie.json"), encoding="utf-8"))["meta"]
    centro = meta["centro_coppia"]
    G = A0.geometria()
    TO = G["TO"]
    dxy = np.asarray(TO.scarti(m1, m2, centro[0], centro[1], L))[:, :2]
    print("  il centro della coppia %s (dal meta di d1/serie.json); L %d, n %d" % (["%.3f" % x for x in centro], L, n))
    print("-" * 130)
    print("  k      A0         d     corpo 1: J_r [8,16)  [16,32)      corpo 2: J_r [8,16)  [16,32)      l'asse: J verso il baricentro (nodi)")
    righe = {}
    for k in KS:
        f = os.path.join(D1, "stato_%06d.npz" % k)
        r = A0.a0(G, f, centro)
        if r["nloc"] != 2:
            print("  %5d  %-9s  (non DUE: fuori dalla media)" % (k, r["verd"]))
            continue
        X = A0.L2.leggi(f)
        rho, Zn = VG.per_nodo(X["phi_h"], pv, nodo, n)
        jx, jy = VG.correnti(rho, Zn, vic)
        p = [dxy[i] for i in r["loc"]]
        corpi = []
        for i in r["loc"]:
            d = np.asarray(TO.scarti(m1, m2, float(m1[i]), float(m2[i]), L))[:, :2]
            dd = np.hypot(d[:, 0], d[:, 1])
            jr = (jx * d[:, 0] + jy * d[:, 1]) / np.maximum(dd, 1e-300)
            corpi.append([float(jr[(dd >= a) & (dd < b)].mean()) for a, b in ANELLI])
        # ### l'asse: dal corpo 1 al corpo 2 con l'immagine piu' vicina
        d1 = np.asarray(TO.scarti(m1, m2, float(m1[r["loc"][0]]), float(m2[r["loc"][0]]), L))[:, :2]
        s = np.asarray(TO.scarti(np.array([float(m1[r["loc"][1]])]), np.array([float(m2[r["loc"][1]])]), float(m1[r["loc"][0]]), float(m2[r["loc"][0]]), L))[0, :2]
        ls = float(np.hypot(*s))
        u = s / ls
        t = (d1 @ u) / ls
        perp = np.abs(d1[:, 0] * u[1] - d1[:, 1] * u[0])
        sel = (t >= 0.0) & (t <= 1.0) & (perp < LARGHEZZA_ASSE) & (np.abs(t - 0.5) * ls > 0.5)
        verso = np.where(t < 0.5, 1.0, -1.0)            # ### verso il punto medio: +u prima della meta', -u dopo
        jax = (jx * u[0] + jy * u[1]) * verso
        ja = float(jax[sel].mean())
        righe[k] = (corpi, ja)
        print("  %5d  %-9s  %6.2f       %+.4e  %+.4e        %+.4e  %+.4e        %+.4e (%d)" % (
            k, r["verd"], ls, corpi[0][0], corpi[0][1], corpi[1][0], corpi[1][1], ja, int(sel.sum())))
    print("-" * 130)
    print("  PER FINESTRA DI %d (la media sugli stati DUE; i due corpi mediati insieme per anello)" % FIN)
    for a in range(0, 6000, FIN):
        ks = [k for k in righe if a <= k < a + FIN]
        if not ks:
            print("  [%4d, %4d): nessuno stato DUE" % (a, a + FIN))
            continue
        r8 = np.mean([[righe[k][0][0][0], righe[k][0][1][0]] for k in ks])
        r16 = np.mean([[righe[k][0][0][1], righe[k][0][1][1]] for k in ks])
        ax = np.mean([righe[k][1] for k in ks])
        print("  [%4d, %4d) (%d stati): J radiale [8,16) %+.4e, [16,32) %+.4e (negativo = verso il corpo); lungo l'asse %+.4e (positivo = verso il baricentro)" % (a, a + FIN, len(ks), r8, r16, ax))
    tutti = list(righe)
    if tutti:
        r8 = np.array([[righe[k][0][0][0], righe[k][0][1][0]] for k in tutti]).ravel()
        r16 = np.array([[righe[k][0][0][1], righe[k][0][1][1]] for k in tutti]).ravel()
        ax = np.array([righe[k][1] for k in tutti])
        print("### su tutti gli stati DUE (%d): J radiale [8,16) media %+.4e (negativi %d su %d); [16,32) media %+.4e (negativi %d su %d); l'asse media %+.4e (positivi %d su %d)" % (
            len(tutti), r8.mean(), int((r8 < 0).sum()), len(r8), r16.mean(), int((r16 < 0).sum()), len(r16), ax.mean(), int((ax > 0).sum()), len(ax)))
    fall = [k for k, v in OK.items() if not v]
    print("### %d DEVE: %d PASSANO, %d FALLISCONO %s" % (len(OK), len(OK) - len(fall), len(fall), fall))
    print("=" * 130)
    return 0 if not fall else 1


if __name__ == "__main__":
    sys.exit(main())
