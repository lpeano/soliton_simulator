# -*- coding: utf-8 -*-
r"""**[M1107] B5: LA CHIAVE NON SALVATA** *(DECISIONE DI LUCA, 2026-11-27 `11:07` e `11:44`; lettura dentro una corsa, nessun lancio in coda; la via e' quella di `due_corpi_fondo_v8.py`)*. [[PROGETTO-MITOSI]]

    E:\python\py3132\python.exe doc/referti_l2/b5_chiave.py > doc/referti_l2/b5_chiave.txt

**Dentro una corsa:** `costruisci` + `parametri` della v6 *(la via di d1')*, poi `250` tick col `D.ciclo` della v2 *(la mia scelta, dichiarata: `k 250` invece di `5750`; il meccanismo del salvataggio e' lo stesso a ogni multiplo di `250`, e la prova finale resta K0' a `5750`)*. **L'istantanea A:** tutto cio' che e' raggiungibile da `Z` *(senza `Z["st"]` duplicato)*, `Z["z"]`, il motore `mot`, `C`, `C.campo`, `X`, `P`: gli array numpy, gli scalari, le liste di numeri e le matrici sparse *(`.data`)*, fino a profondita' `4`. **Lo stato si salva** come `due_corpi_fondo_v4.corsa` *(le chiavi di `st`, `campo_A`, `campo_E`, `chi, pi, theta_a`)* in un file temporaneo su E:. **Poi una scena nuova:** `costruisci` + `parametri`, e la carica di quel file come `due_corpi_fondo_v7.Ripresa`. **L'istantanea B**, e il confronto voce per voce: uguali, diverse *(con `max |d|` e relativo)*, presenti in una sola. **Le diverse sono le candidate.**
"""
import json
import numbers
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
import due_corpi_fondo_v8 as V8  # noqa: E402

V7 = V8.V7
D, V6, CT, GD = V7.D, V7.V6, V7.CT, V7.GD
K = 250
TMPF = os.path.join("E:" + os.sep, "soliton_lavoro", "tmp", "b5_stato_%06d.npz" % K)
PROF = 4


def foto(radici):
    """### `{percorso: valore}`: gli array, gli scalari, le liste di numeri, le sparse, raggiungibili dalle radici."""
    out, visti = {}, set()

    def va(o, p, d):
        if isinstance(o, np.ndarray):
            if o.dtype != object:
                out[p] = o.copy()
            return
        if isinstance(o, (bool, numbers.Number, np.generic)):
            out[p] = np.asarray(o).copy()
            return
        if hasattr(o, "tocsr") and hasattr(o, "data"):
            out[p + ".data"] = np.asarray(o.data).copy()
            return
        if isinstance(o, (str, bytes)) or callable(o) and not hasattr(o, "__dict__") or d >= PROF:
            return
        if id(o) in visti:
            return
        visti.add(id(o))
        if isinstance(o, dict):
            for k, v in o.items():
                va(v, "%s[%r]" % (p, k), d + 1)
        elif isinstance(o, (list, tuple)):
            if o and all(isinstance(x, (numbers.Number, np.generic)) for x in o):
                out[p] = np.asarray(o).copy()
            else:
                for i, v in enumerate(o):
                    va(v, "%s[%d]" % (p, i), d + 1)
        elif hasattr(o, "__dict__") and not isinstance(o, type) and type(o).__module__ not in ("builtins",) and not hasattr(o, "__file__"):
            for k, v in vars(o).items():
                if not callable(v) or isinstance(v, np.ndarray):
                    va(v, "%s.%s" % (p, k), d + 1)
    for nome, o in radici:
        va(o, nome, 0)
    return out


def radici(Z, C, X, P):
    return [("Z", {k: v for k, v in Z.items() if k not in ("st",)}), ("st", Z["st"]), ("C", C), ("X", X), ("P", P)]


def main():
    V7.avvia()
    import _presidio
    _presidio.avvia(__file__)
    print("=" * 130)
    print("[M1107] B5: LA CHIAVE NON SALVATA: la corsa continua a k %d contro la stessa ricaricata dal file appena scritto" % K)
    print("=" * 130)
    with GD.TC.scena() as Z:
        Lp = CT.Laplaciano(Z["mot"])
        C, info, X = V6.costruisci(Z, 2, V6.STATO_G3)
        P, Pon, m0 = D.parametri(Z, C, True)
        D.ciclo(Z, C, P, Lp, X, K, lambda kk, prima: None)
        A = foto(radici(Z, C, X, P))
        dati = {x: Z["st"][x] for x in Z["chiavi"]}
        dati.update(campo_A=C.campo.A, campo_E=C.campo.E, **{q: X[q] for q in CT.CHIAVI_CHI})
        os.makedirs(os.path.dirname(TMPF), exist_ok=True)
        np.savez(TMPF, meta=np.array(json.dumps({"k": K})), **dati)
        print("  la corsa continua: %d tick; l'istantanea A ha %d voci; lo stato salvato in %s (%d chiavi)" % (K, len(A), TMPF, len(dati)))
        Z["metti"]()
    with GD.TC.scena() as Z:
        C, info, X = V6.costruisci(Z, 2, V6.STATO_G3)
        P, Pon, m0 = D.parametri(Z, C, True)
        with np.load(TMPF) as z:
            for x in Z["chiavi"]:
                Z["st"][x][...] = z[x]
            C.campo.A[...] = z["campo_A"]
            C.campo.E[...] = z["campo_E"]
            for q in CT.CHIAVI_CHI:
                X[q][...] = z[q]
        B = foto(radici(Z, C, X, P))
        Z["metti"]()
    print("  la ricarica: l'istantanea B ha %d voci" % len(B))
    print("-" * 130)
    print("LE VOCI DIVERSE (le candidate), poi quelle presenti in una sola istantanea")
    print("-" * 130)
    uguali, diverse = 0, []
    for p in sorted(set(A) & set(B)):
        a, b = A[p], B[p]
        if a.shape == b.shape and a.dtype == b.dtype and np.array_equal(a, b, equal_nan=a.dtype.kind in "fc"):
            uguali += 1
            continue
        if a.shape == b.shape and a.dtype.kind in "fcib" and b.dtype.kind in "fcib":
            d = np.abs(a.astype(complex) - b.astype(complex))
            m = float(np.nanmax(d)) if d.size else 0.0
            r = m / max(float(np.nanmax(np.abs(a))) if a.size else 0.0, 1e-300)
            diverse.append((p, "forma %s; max |d| %.3e; relativo %.3e; diversi %d su %d" % (a.shape, m, r, int(np.count_nonzero(d)), d.size)))
        else:
            diverse.append((p, "forma o tipo diversi: %s %s contro %s %s" % (a.shape, a.dtype, b.shape, b.dtype)))
    for p, t in diverse:
        print("  ### DIVERSA: %s: %s" % (p, t))
    solo_a, solo_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))
    for p in solo_a:
        print("  solo nella corsa continua: %s %s" % (p, A[p].shape))
    for p in solo_b:
        print("  solo nella ricarica: %s %s" % (p, B[p].shape))
    print("-" * 130)
    print("### %d voci in comune: %d uguali, %d DIVERSE; %d solo in A, %d solo in B" % (len(set(A) & set(B)), uguali, len(diverse), len(solo_a), len(solo_b)))
    print("=" * 130)
    return 0


if __name__ == "__main__":
    sys.exit(main())
