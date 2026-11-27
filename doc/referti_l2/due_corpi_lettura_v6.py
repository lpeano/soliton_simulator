# -*- coding: utf-8 -*-
r"""**[M1016] PEZZO 4: A0 SU TUTTI GLI STATI DI d1' E d1'', LA LETTURA COI PICCHI** *(DECISIONE DI LUCA, 2026-11-27 `10:16`, `11:07` (il punto 7: il verdetto usa i picchi), `12:14`, `13:12`; la carta `doc/CARTA_fondo_giusto.md`, il seguito [M1016], «PEZZI 4 E 5», scritta PRIMA della chiusura di d1'')*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/due_corpi_lettura_v6.py > doc/referti_l2/due_corpi_fondo_v7.txt

**`73` stati**, `k 0..18000` ogni `250` *(`M2034/coppia/d1` fino a `6000`, `M2034/coppia/d1L` dopo)*. **(i)** A0 *(`coppia_a0.a0`)*, la norma DEVE entro `1e-9`. **(ii)** per stato: il verdetto, `d_p` *(fra i picchi, se DUE)*, `d_m` *(le meta', dalla serie)*, `R`, `max rho`, `w` per corpo *(`FPC.w_di` sulla meta', se DUE)*, `chi` ai picchi *(media su `r < 4` dal nodo del picco, se DUE)*. **(iii)** i contatti *(tratti non-DUE)*. **(iv)** i minimi di `d_p` fra stati DUE; per ogni contatto `d_p` prima e dopo e il minimo di `d_m` nella serie. **(v)** il periodo fra gli inizi dei contatti. **(vi)** la tabella per finestra di `500`. **(vii)** il verso di `d_p` per tratto DUE.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import coppia_a0 as A0  # noqa: E402

L4 = A0.L4
L2, PF, FPC = L4.L2, L4.PF, L4.FPC
D1 = A0.D1
D1L = os.path.join(L4.BASE, "d1L")
KS = list(range(0, 18001, 250))
FIN = [(k, k + 500) for k in range(0, 18000, 500)]


def cartella(k):
    return D1 if k <= 6000 else D1L


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "coppia_a0.py"))
    _presidio.avvia(__file__)
    print("=" * 140)
    print("[M1016] PEZZO 4: A0 SU %d STATI (d1' e d1''), LA LETTURA COI PICCHI; d_p = fra i picchi (il verdetto), d_m = fra le meta' (per confronto)" % len(KS))
    print("=" * 140)
    G = A0.geometria()
    S = {}
    for c in (D1, D1L):
        f = os.path.join(c, "serie.json")
        PF.controlla(f)
        S[c] = json.load(open(f, encoding="utf-8"))
    centro = S[D1]["meta"]["centro_coppia"]
    assert S[D1L]["meta"]["centro_coppia"] == centro and S[D1L]["meta"]["k_da"] == 6000
    ser = {}
    for c in (D1, D1L):
        for r in S[c]["serie"]:
            ser[int(r[0])] = r
    kser = np.array(sorted(ser))
    dm_ser = np.array([float(np.hypot(ser[k][4] - ser[k][1], ser[k][5] - ser[k][2])) for k in kser])
    om = [np.concatenate([np.array(S[D1]["omega"][j]), np.array(S[D1L]["omega"][j])]) for j in range(2)]
    assert len(om[0]) == 18000, "omega: %d tick, non 18000" % len(om[0])
    dxy = np.asarray(G["TO"].scarti(G["m1"], G["m2"], centro[0], centro[1], G["L"]))[:, :2]
    meta = [dxy[:, 1] < 0.0, dxy[:, 1] >= 0.0]
    T = {}
    for k in KS:
        f = os.path.join(cartella(k), "stato_%06d.npz" % k)
        r = A0.a0(G, f, centro)
        X = L2.leggi(f)
        rho = np.bincount(G["nodo"], weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=G["n"])
        r["dm"] = float(dm_ser[kser == k][0])
        if r["nloc"] == 2:
            r["w"] = [FPC.w_di(rho * mm, G["L"]) for mm in meta]
            r["chi"] = [float(X["chi"][np.hypot(dxy[:, 0] - dxy[i, 0], dxy[:, 1] - dxy[i, 1]) < 4.0].mean()) for i in r["loc"]]
        T[k] = r
    N0 = T[0]["N"]
    print("-" * 140)
    print("(ii) PER STATO")
    print("-" * 140)
    for k in KS:
        r = T[k]
        extra = ("d_p %7.3f; w %.3f %.3f; chi ai picchi %+.2f %+.2f" % (r["dloc"], r["w"][0], r["w"][1], r["chi"][0], r["chi"][1])) if r["nloc"] == 2 else "d_p -"
        print("  k %5d: %-10s %s; d_m %7.3f; R %7.3f; max rho %.4e; N %+.2e" % (k, r["verd"], extra, r["dm"], r["R"], r["rmax"], r["N"] / N0 - 1.0))
    dn = max(abs(T[k]["N"] / N0 - 1.0) for k in KS)
    okn = dn < A0.TOL_NORMA
    print("  DEVE: (la norma) max |N(k)/N(0) - 1| su %d stati = %.3e < 1e-9   %s" % (len(KS), dn, "PASSA" if okn else "### FALLISCE: FERMO"))
    print("-" * 140)
    print("(iii) I CONTATTI (tratti di stati non-DUE) e (iv) I MINIMI")
    print("-" * 140)
    due = [T[k]["nloc"] == 2 for k in KS]
    contatti, i = [], 0
    while i < len(KS):
        if not due[i]:
            j = i
            while j + 1 < len(KS) and not due[j + 1]:
                j += 1
            contatti.append((i, j))
            i = j + 1
        else:
            i += 1
    for a, b in contatti:
        ka, kb = KS[a], KS[b]
        prima = T[KS[a - 1]]["dloc"] if a > 0 else float("nan")
        dopo = T[KS[b + 1]]["dloc"] if b + 1 < len(KS) else float("nan")
        lo, hi = (KS[a - 1] if a > 0 else 0), (KS[b + 1] if b + 1 < len(KS) else 18000)
        msk = (kser >= lo) & (kser <= hi)
        im = int(np.argmin(np.where(msk, dm_ser, np.inf)))
        print("  ### CONTATTO da k %d a k %d (%d stati: %s); R min %.3f; d_p prima %.3f (k %d), dopo %.3f (k %s); d_m min nella serie %.3f a k %d (la riserva: sotto ~2 w le meta' non separano)" % (
            ka, kb, b - a + 1, ", ".join(T[KS[x]]["verd"] for x in range(a, b + 1)), min(T[KS[x]]["R"] for x in range(a, b + 1)), prima, lo, dopo, hi if b + 1 < len(KS) else "-", float(dm_ser[im]), int(kser[im])))
    for x in range(1, len(KS) - 1):
        if due[x - 1] and due[x] and due[x + 1] and T[KS[x]]["dloc"] < T[KS[x - 1]]["dloc"] and T[KS[x]]["dloc"] < T[KS[x + 1]]["dloc"]:
            print("  ### MINIMO di d_p fra stati DUE: %.3f a k %d" % (T[KS[x]]["dloc"], KS[x]))
    print("  ### i contatti: %d; i loro inizi: %s; (v) i periodi fra gli inizi: %s" % (len(contatti), [KS[a] for a, _ in contatti], [KS[contatti[q + 1][0]] - KS[contatti[q][0]] for q in range(len(contatti) - 1)] or "nessuno (meno di due contatti)"))
    print("-" * 140)
    print("(vi) PER FINESTRA DI 500: d_p medio (gli stati DUE), omega medio per corpo (la serie per tick), w medio, chi ai picchi")
    print("-" * 140)
    for k0, k1 in FIN:
        ss = [T[x] for x in (k0, k0 + 250, k1)]
        sd = [s for s in ss if s["nloc"] == 2]
        o = [float(om[j][k0:k1].mean()) for j in range(2)]
        if sd:
            print("  [%5d, %5d]: d_p %7.3f (%d su 3 DUE); omega %.6f %.6f; w %.3f %.3f; chi ai picchi %+.2f %+.2f" % (
                k0, k1, float(np.mean([s["dloc"] for s in sd])), len(sd), o[0], o[1], float(np.mean([s["w"][0] for s in sd])), float(np.mean([s["w"][1] for s in sd])),
                float(np.mean([s["chi"][0] for s in sd])), float(np.mean([s["chi"][1] for s in sd]))))
        else:
            print("  [%5d, %5d]: contatto (0 su 3 DUE); omega %.6f %.6f" % (k0, k1, o[0], o[1]))
    print("-" * 140)
    print("(vii) IL VERSO DI d_p PER TRATTO DUE")
    print("-" * 140)
    i = 0
    while i < len(KS):
        if due[i]:
            j = i
            while j + 1 < len(KS) and due[j + 1]:
                j += 1
            dd = [T[KS[x]]["dloc"] for x in range(i, j + 1)]
            print("  tratto DUE da k %d a k %d (%d stati): d_p da %.3f a %.3f; massimo %.3f a k %d; minimo %.3f a k %d" % (
                KS[i], KS[j], j - i + 1, dd[0], dd[-1], max(dd), KS[i + int(np.argmax(dd))], min(dd), KS[i + int(np.argmin(dd))]))
            i = j + 1
        else:
            i += 1
    print("=" * 140)
    return 0 if okn else 1


if __name__ == "__main__":
    sys.exit(main())
