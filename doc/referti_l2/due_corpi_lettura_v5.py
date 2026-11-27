# -*- coding: utf-8 -*-
r"""**[M0106] D2'' E IL VERDETTO RISCRITTO SUGLI STESSI NUMERI** *(DECISIONE DI LUCA, 2026-11-27 `01:06`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies`, il seguito [M0106], scritta PRIMA; nessuna corsa: gli stessi `25` stati di `M2034/coppia`; `due_corpi_lettura_v4.py` e' usato e non si tocca: la v5 lo fa girare per intero, poi aggiunge)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_lettura_v5.py > doc/referti_l2/due_corpi_fondo_v6_C.txt

**Prima** la v4 intera *(N1, (R), C', i numeri N, `d(k)`; la sua riga di verdetto D2' col segno e' SUPERATA da D2'' e si legge come storia)*; **poi D2''** per finestra valida: VERSO se `Delta d(d1') < 0` e `|Delta d(d1')| > 3 |Delta d(d2')|`; VIA se `Delta d(d1') > 0` e lo stesso rapporto; altrimenti «non distinguibile»; il verso di d2' si stampa e non entra. **In piu':** il minimo di `d(k)` di d1' e il suo tick; il massimo dopo il minimo; il minimo successivo, se c'e' *(un minimo locale interno, cioe' non all'ultimo tick)*, e il periodo; **la tabella per finestra di `500`**: `d` medio, `omega` medio di ciascun corpo, chi al centro *(chi medio su `r < 4` dal baricentro del corpo nella sua meta', media sui `3` stati della finestra)*, per d1', d2' e d3'.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v4 as L4  # noqa: E402

L3, L2, PF, VV = L4.L3, L4.L2, L4.PF, L4.VV
BASE, FIN, KS = L4.BASE, L4.FIN, L4.KS


def main():
    import _presidio
    cod4 = L4.main()
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M0106] D2'' (VERSO LIBERO, LO STESSO INTERVALLO), IL MINIMO, L'OSCILLAZIONE, omega CONTRO d -- SUGLI STESSI 25 STATI (la riga D2' qui sopra e' SUPERATA)")
    print("=" * 130)
    from solitone import toro as TO
    with VV.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        Z["metti"]()
    S, D = {}, {}
    for c in ("d1", "d2", "d3"):
        f = os.path.join(BASE, c, "serie.json")
        PF.controlla(f)
        S[c] = json.load(open(f, encoding="utf-8"))
    for c in ("d1", "d2"):
        sr = np.array(S[c]["serie"])
        D[c] = (sr[:, 0], np.hypot(sr[:, 4] - sr[:, 1], sr[:, 5] - sr[:, 2]))

    def dd(c, k0, k1):
        k, d = D[c]
        return float(d[k == k0][0]), float(d[k == k1][0])
    # ### le finestre valide, rifatte con la stessa regola C' della v4
    om3 = np.array(S["d3"]["omega"][0])
    W3, P3 = {}, {}
    for k in KS:
        X = L2.leggi(os.path.join(BASE, "d3", "stato_%06d.npz" % k))
        r = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
        W3[k], P3[k] = L4.FPC.w_di(r, L), L4.FPC.profondita({"m1": m1, "m2": m2, "L": L}, r, X["chi"])
    pv = [p for p in L4.PERIODI if L4.ok_wp(float(np.mean([W3[k] for k in KS if p[0] <= k <= p[1]])))]
    VAL = [(k0, k1) for k0, k1 in FIN if L4.ok_om(float(om3[k0:k1].mean())) and L4.ok_pz(float(np.mean([P3[k0], P3[k0 + 250], P3[k1]]))) and any(p[0] <= k0 and k1 <= p[1] for p in pv)]
    print("  ### LE FINESTRE VALIDE (C', rifatte): %d su %d" % (len(VAL), len(FIN)))
    print("-" * 130)
    print("D2'': VERSO se Delta d1' < 0 e |Delta d1'| > 3 |Delta d2'|; VIA se Delta d1' > 0 e lo stesso; il verso di d2' si dichiara e non entra")
    print("-" * 130)
    conta = {"VERSO": 0, "VIA": 0, "non distinguibile": 0}
    for k0, k1 in VAL:
        a0, a1 = dd("d1", k0, k1)
        b0, b1 = dd("d2", k0, k1)
        x, y = a1 - a0, b1 - b0
        v = ("VERSO" if x < 0 else "VIA") if abs(x) > 3.0 * abs(y) else "non distinguibile"
        conta[v] += 1
        print("  [%4d, %4d]: Delta d1' %+.6f; Delta d2' %+.6f (%s); |Delta d1'|/|Delta d2'| %.2f  ->  %s" % (k0, k1, x, y, "VERSO" if y < 0 else "VIA", abs(x) / abs(y) if y != 0 else float("inf"), v))
    print("  ### IL VERDETTO D2'' su %d finestre valide: VERSO %d, VIA %d, non distinguibile %d" % (len(VAL), conta["VERSO"], conta["VIA"], conta["non distinguibile"]))
    print("-" * 130)
    print("IL MINIMO DI d(k) DI d1' E L'OSCILLAZIONE RADIALE (dalla serie, ogni 10 tick)")
    print("-" * 130)
    k, d = D["d1"]
    i0 = int(np.argmin(d))
    i1 = i0 + int(np.argmax(d[i0:]))
    print("  il minimo: d %.6f a k %d; il massimo dopo il minimo: d %.6f a k %d%s" % (float(d[i0]), int(k[i0]), float(d[i1]), int(k[i1]), "  (all'ultimo tick)" if i1 == len(d) - 1 else ""))
    if i1 < len(d) - 1:
        i2 = i1 + int(np.argmin(d[i1:]))
        if i2 < len(d) - 1:
            print("  il minimo successivo: d %.6f a k %d; ### IL PERIODO (minimo -> minimo) %d tick" % (float(d[i2]), int(k[i2]), int(k[i2] - k[i0])))
        else:
            print("  ### IL MINIMO SUCCESSIVO NON C'E' nei 6000 tick: d scende fino all'ultimo tick (%.6f a k %d); il mezzo periodo minimo -> massimo e' %d tick (NON un periodo)" % (float(d[i2]), int(k[i2]), int(k[i1] - k[i0])))
    else:
        print("  ### dopo il minimo d sale fino all'ultimo tick: nessun periodo")
    print("-" * 130)
    print("LA TABELLA PER FINESTRA DI 500: d medio (la serie); omega medio per corpo (la serie per tick); chi al centro per corpo (r < 4 dal baricentro nella sua meta', media dei 3 stati)")
    print("-" * 130)
    CHI = {}
    for c, q in L4.CORSE:
        b = S[c]["meta"]["centro_coppia"]
        dxy = np.asarray(TO.scarti(m1, m2, b[0], b[1], L))[:, :2]
        masch = [np.ones(n, bool)] if q == 1 else [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]
        for kk in KS:
            X = L2.leggi(os.path.join(BASE, c, "stato_%06d.npz" % kk))
            rp = np.bincount(nodo, weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=n)
            for j, mm in enumerate(masch):
                w = rp * mm
                cb = (dxy * w[:, None]).sum(axis=0) / w.sum()
                r = np.hypot(dxy[:, 0] - cb[0], dxy[:, 1] - cb[1])
                CHI[(c, j, kk)] = float(X["chi"][mm & (r < 4.0)].mean())
    for k0, k1 in FIN:
        parti = []
        for c, q in L4.CORSE:
            oms = [np.array(o) for o in S[c]["omega"]]
            om = " ".join("%.6f" % float(oms[j][k0:k1].mean()) for j in range(q))
            ch = " ".join("%+.2f" % float(np.mean([CHI[(c, j, x)] for x in (k0, k0 + 250, k1)])) for j in range(q))
            if q == 2:
                kk, dk = D[c]
                dm = float(dk[(kk >= k0) & (kk <= k1)].mean())
                parti.append("%s' d %7.3f omega %s chi %s" % (c, dm, om, ch))
            else:
                parti.append("%s' omega %s chi %s" % (c, om, ch))
        print("  [%4d, %4d]: %s" % (k0, k1, ";  ".join(parti)))
    print("=" * 130)
    return cod4


if __name__ == "__main__":
    sys.exit(main())
