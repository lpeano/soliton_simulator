# -*- coding: utf-8 -*-
r"""**[M1016] A0: DUE CORPI O UNA NUBE? E LO «SVANIRE» E' DI SCALA O DI NORMA?** *(DECISIONE DI LUCA, 2026-11-27 `10:16`; la carta `doc/CARTA_fondo_giusto.md`, sez. `3-vicies`, il seguito [M1016], scritta PRIMA; sola lettura, nessuna corsa)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/coppia_a0.py > doc/referti_l2/coppia_a0.txt

**Per ogni stato** di `M2034/coppia/d1` *(`25`, da `0` a `6000` ogni `250`)*: **(i)** la norma `N = somma |psi_h|^2`, **DEVE** `|N(k)/N(0) - 1| < 1e-9` *(se fallisce: FERMO)*; **(ii)** `max rho_psi`, il suo nodo e la sua posizione; **(iii)** i massimi locali della lisciatura `s` *(la media di `rho_psi` sul disco di raggio `2`, `19` nodi, gli offset di reticolo esatti, periodico)*: `s(i) >= s(j)` su tutto il disco e `s(i) > 0.30 max s`; **(iv)** `R = sqrt(somma rho r^2 / somma rho)` dal baricentro totale. **Il verdetto:** DUE CORPI *(2 massimi)*, UNO *(1)*, ALTRO *(n)*; il tick della fusione. **(K1)** `stato_000000`: `2` massimi a distanza entro `1` da `41.57`. **(K2)** `giro_3/stato_003000.npz`, centrato sul nodo del suo massimo: `1` massimo. `a0()` e' riusabile *(il pezzo 4, i `73` stati)*.
"""
import json
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_lettura_v4 as L4  # noqa: E402

L2, PF, VV = L4.L2, L4.PF, L4.VV
D1 = os.path.join(L4.BASE, "d1")
K2_STATO = os.path.join(L4.GIRO3, "stato_003000.npz")
SOGLIA, RAGGIO, TOL_NORMA, D0, TOL_K1 = 0.30, 2.0, 1e-9, 41.57, 1.0


def geometria():
    """### la scena della coppia: `nodo, n, L, m1, m2`, e gli offset del disco di raggio `2`."""
    from solitone import toro as TO
    with VV.F1.TC.scena() as Z:
        nodo, n, L = np.asarray(Z["mot"].inc.nodo), Z["n"], Z["L"]
        m1, m2 = np.asarray(Z["m1"], int), np.asarray(Z["m2"], int)
        Z["metti"]()
    assert np.array_equal(m1 * L + m2, np.arange(n)), "il nodo NON e' m1 L + m2: la lisciatura per offset non vale"
    A1, A2 = TO.vettori()
    off = [(a, b) for a in range(-3, 4) for b in range(-3, 4) if np.hypot(*(a * np.asarray(A1) + b * np.asarray(A2))) <= RAGGIO + 1e-12]
    assert len(off) == 19, "il disco di raggio 2 ha %d nodi, non 19" % len(off)
    vic = np.array([((m1 + a) % L) * L + (m2 + b) % L for a, b in off])  # (19, n)
    return dict(nodo=nodo, n=n, L=L, m1=m1, m2=m2, vic=vic, TO=TO)


def a0(G, f, centro):
    """### A0 su uno stato: la norma, il massimo, i massimi locali, il raggio della nube."""
    X = L2.leggi(f)
    p2 = np.sum(np.abs(X["psi_h"]) ** 2, axis=1)
    N = float(p2.sum())
    rho = np.bincount(G["nodo"], weights=p2, minlength=G["n"])
    s = rho[G["vic"]].mean(axis=0)
    loc = np.where((s >= s[G["vic"]].max(axis=0)) & (s > SOGLIA * s.max()))[0]
    dxy = np.asarray(G["TO"].scarti(G["m1"], G["m2"], centro[0], centro[1], G["L"]))[:, :2]
    cb = (dxy * rho[:, None]).sum(axis=0) / rho.sum()
    R = float(np.sqrt((rho * ((dxy[:, 0] - cb[0]) ** 2 + (dxy[:, 1] - cb[1]) ** 2)).sum() / rho.sum()))
    im = int(np.argmax(rho))
    dist = float(np.hypot(*(dxy[loc[0]] - dxy[loc[1]]))) if len(loc) == 2 else float("nan")
    nm = len(loc)
    verd = "DUE CORPI" if nm == 2 else ("UNO" if nm == 1 else "ALTRO (%d)" % nm)
    return dict(N=N, rmax=float(rho.max()), im=im, pmax=dxy[im], nloc=nm, loc=loc, dloc=dist, R=R, cb=cb, verd=verd, smax=float(s.max()), sloc=s[loc])


def tabella(G, cartella, ks, centro):
    """### A0 su tutti gli stati di una cartella; stampa la tabella e rende `(righe, ok_norma, fusione)`."""
    righe = {}
    for k in ks:
        righe[k] = a0(G, os.path.join(cartella, "stato_%06d.npz" % k), centro)
    N0 = righe[ks[0]]["N"]
    for k in ks:
        r = righe[k]
        print("  k %5d: N %.12e (%+.2e); max rho %.4e al nodo %d (%+.2f, %+.2f); massimi %d [%s]%s; R %.4f  ->  %s" % (
            k, r["N"], r["N"] / N0 - 1.0, r["rmax"], r["im"], r["pmax"][0], r["pmax"][1], r["nloc"],
            ", ".join("%.3e" % v for v in r["sloc"]), ("; fra i due %.3f" % r["dloc"]) if r["nloc"] == 2 else "", r["R"], r["verd"]))
    dn = max(abs(righe[k]["N"] / N0 - 1.0) for k in ks)
    ok = dn < TOL_NORMA
    print("  DEVE: (la norma) max |N(k)/N(0) - 1| = %.3e < %.0e   %s" % (dn, TOL_NORMA, "PASSA" if ok else "### FALLISCE: FERMO, E' UN ERRORE"))
    fus = next((ks[i] for i in range(1, len(ks)) if righe[ks[i]]["nloc"] == 1 and righe[ks[i - 1]]["nloc"] == 2), None)
    return righe, ok, fus


def main():
    import _presidio
    _presidio.avvia(os.path.join(_QUI, "due_corpi_lettura_v4.py"))
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1016] A0: DUE CORPI O UNA NUBE? LA NORMA, IL MASSIMO, I MASSIMI LOCALI (> %.0f%% della lisciatura di raggio %.0f), IL RAGGIO DELLA NUBE" % (100 * SOGLIA, RAGGIO))
    print("=" * 130)
    G = geometria()
    f = os.path.join(D1, "serie.json")
    PF.controlla(f)
    centro = json.load(open(f, encoding="utf-8"))["meta"]["centro_coppia"]
    print("-" * 130)
    print("I CASI NOTI")
    print("-" * 130)
    k1 = a0(G, os.path.join(D1, "stato_000000.npz"), centro)
    ok1 = k1["nloc"] == 2 and abs(k1["dloc"] - D0) < TOL_K1
    print("  DEVE: (K1) stato_000000: %d massimi, a distanza %.3f (entro %.0f da %.2f)   %s" % (k1["nloc"], k1["dloc"], TOL_K1, D0, "PASSA" if ok1 else "### FALLISCE"))
    PF.controlla(K2_STATO)
    X = L2.leggi(K2_STATO)
    im = int(np.argmax(np.bincount(G["nodo"], weights=np.sum(np.abs(X["psi_h"]) ** 2, axis=1), minlength=G["n"])))
    k2 = a0(G, K2_STATO, (G["m1"][im], G["m2"][im]))
    ok2 = k2["nloc"] == 1
    print("  DEVE: (K2) %s (un oggetto solo, centrato sul nodo %d): %d massimi; R %.4f   %s" % (K2_STATO, im, k2["nloc"], k2["R"], "PASSA" if ok2 else "### FALLISCE"))
    print("-" * 130)
    print("A0 SUI %d STATI DI d1' (%s)" % (len(L4.KS), D1))
    print("-" * 130)
    righe, okn, fus = tabella(G, D1, L4.KS, centro)
    print("-" * 130)
    print("  ### IL VERDETTO PER STATO: %s" % "; ".join("%d %s" % (k, righe[k]["verd"]) for k in L4.KS))
    print("  ### IL TICK DELLA FUSIONE (il primo UNO dopo un DUE): %s" % (fus if fus is not None else "nessuno"))
    print("  ### max rho da k 0 a k 6000: %.4e -> %.4e (rapporto %.3f); R: %.4f -> %.4f" % (righe[0]["rmax"], righe[6000]["rmax"], righe[6000]["rmax"] / righe[0]["rmax"], righe[0]["R"], righe[6000]["R"]))
    print("  ### (a) contro (b): la norma %s; %s" % ("FERMA" if okn else "NON FERMA", "vale (a): la materia si allarga, non si perde" if okn else "### FERMO: la norma cala, e' un errore"))
    print("=" * 130)
    return 0 if (ok1 and ok2 and okn) else 1


if __name__ == "__main__":
    sys.exit(main())
