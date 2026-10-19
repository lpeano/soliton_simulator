# -*- coding: utf-8 -*-
r"""**IL PUNTO FISSO DI `cs` CHE NON CONVERGE A TAGLIA `32`, RAPPORTO `0.01`** — *riprodotto.*

> ### ⛔ **PERCHE' ESISTE** *(`2026-10-19`)*: il passo `B` *(`ec0d5f7f`, `8b2bdb16`)* ha
> trovato che a taglia `32` e `Lambda_c/Lambda_medio = 0.01` il punto fisso di `cs`
> ### **non converge col ramo SPENTO**, cioe' con ### **lo schema di DEFAULT** a `cs`
> dinamico. Il guardiano l'ha riprodotta: ### **un CICLO DI PERIODO `2`** al tick `6`.
> ### **Qui la riproduco io, coi miei numeri.** ### ⛔ **E' UNA OSSERVAZIONE: nessuna cura,
> nessuna scelta.**

## ⭐ COME, SENZA COPIARE IL CICLO

`tick.cs_al_centro` chiama `FP.cs` ### **una volta per la prima ipotesi e una per giro**:
le sue uscite ### **SONO gli iterati** `x_0, x_1, ...`. ### **Si registrano in memoria**
avvolgendo `FP.cs` per la durata della corsa, e ### **il ciclo che gira e' quello del
repo.**

## ⭐ CHE COSA RIPORTA

Il tick *(contato da `1`)* in cui il punto fisso alza; ### **`|x_n - x_{n-1}|`** e
### **`|x_n - x_{n-2}|`** all'ultimo giro *(un periodo `2` ha il primo grande e il secondo
piccolo)*; i ### **nodi che oscillano** *(quelli dove `|x_n - x_{n-1}|` supera la
tolleranza di `cs_al_centro`)*, con ### **`Lambda`** di ciascuno nello stato di quel tick, e
il confronto con `Lambda_c`.

## ⛔ IL CONFRONTO

### **La taglia `16` allo STESSO rapporto** *(`Lambda_c = 0.08`, il valore di `C5`)*
### **deve convergere** in tutti gli `8` tick: e' il caso in cui lo strumento ### **non**
deve trovare un ciclo.

Gira con:  python csv/_ciclo_cs.py
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

import numpy as np                                             # noqa: E402

import _costo_punti_fissi as CPF                               # noqa: E402

IRAPPORTO = 0                # D2.SPAZZATA[0] = 0.08: il rapporto 0.01 di C5
TAGLIE = (32, 16)            # quella che non converge, e il confronto


def corsa(taglia):
    """### `(esito, dati)`: ### **gli iterati di `cs` di ogni tick**, fino all'errore."""
    import flussi_parziali as FP
    import tick as TK
    lc, lam_m, rapp = CPF.lambda_c(taglia, IRAPPORTO)
    _inc, mot, st, par = CPF.scena(taglia)
    FP.accendi_cs(mot, lc, st)
    vero = FP.cs
    iterati = []

    def cs(lam, lambda_c, fuori):
        r = vero(lam, lambda_c, fuori)
        iterati.append(np.array(r, copy=True))
        return r
    FP.cs = cs
    try:
        for t in range(1, CPF.TICK + 1):
            del iterati[:]
            lam_tick = mot.densita_vuoto(st).copy()
            try:
                TK.tick_con_cs(st, mot, par, lc, ())
            except AssertionError as e:
                return "NON CONVERGE", {"tick": t, "iterati": list(iterati),
                                        "lam": lam_tick, "lc": lc, "lam_m": lam_m,
                                        "rapp": rapp, "msg": str(e)[:100]}
    finally:
        FP.cs = vero
    return "CONVERGE", {"tick": CPF.TICK, "lc": lc, "lam_m": lam_m, "rapp": rapp}


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    import tick as TK
    print("=" * 100)
    print("IL PUNTO FISSO DI `cs` A RAPPORTO 0.01: IL CICLO, RIPRODOTTO -- un'OSSERVAZIONE")
    print("=" * 100)
    print("  la scena e lo stato di `C5` (csv/_costo_punti_fissi.scena), `cs` acceso,"
          " tick.tick_con_cs, ramo del punto medio SPENTO (default)")
    print("  la tolleranza di cs_al_centro: EPS_CS = %.3e (relativa al max di cs);"
          " GIRI_MAX = %d" % (TK.EPS_CS, TK.GIRI_MAX))
    ok = True
    for taglia in TAGLIE:
        esito, d = corsa(taglia)
        print("-" * 100)
        print("### TAGLIA %d   Lambda_c = %.4f   Lambda_medio = %.4f   rapporto = %.4f   -> %s"
              % (taglia, d["lc"], d["lam_m"], d["rapp"], esito))
        if esito == "CONVERGE":
            print("     tutti gli %d tick convergono" % d["tick"])
            ok &= taglia != 32
            continue
        ok &= taglia == 32
        x = d["iterati"]
        n = len(x) - 1
        d1 = np.abs(x[-1] - x[-2])
        d2 = np.abs(x[-1] - x[-3])
        print("     il punto fisso ALZA al tick %d (contato da 1), dopo %d giri: %s"
              % (d["tick"], n, d["msg"]))
        print("     all'ultimo giro: max|x_n - x_{n-1}| = %.3e   max|x_n - x_{n-2}| = %.3e"
              % (float(np.max(d1)), float(np.max(d2))))
        print("     ### un periodo 2 ha il primo GRANDE e il secondo PICCOLO")
        print("     max|x_n - x_{n-2}| lungo gli ultimi giri (dal piu' vecchio):")
        print("        %s" % "  ".join("%.1e" % float(np.max(np.abs(x[k] - x[k - 2])))
                                       for k in range(max(2, n - 9), n + 1)))
        tol = TK.EPS_CS * float(np.max(np.abs(x[-1])))
        osc = np.where(d1 > tol)[0]
        print("     i nodi che oscillano (|x_n - x_{n-1}| > tolleranza): %d" % len(osc))
        print("        %-6s %-12s %-12s %-12s %s"
              % ("nodo", "Lambda", "cs pari", "cs dispari", "|differenza|"))
        for k in osc[np.argsort(-d1[osc])]:
            print("        %-6d %-12.5f %-12.6f %-12.6f %.3e"
                  % (k, d["lam"][k], x[-1][k], x[-2][k], d1[k]))
        peggio = int(osc[np.argmax(d1[osc])]) if len(osc) else -1
        if peggio >= 0:
            print("     il PEGGIORE e' il nodo %d: Lambda = %.4f, %s Lambda_c = %.4f"
                  % (peggio, d["lam"][peggio],
                     "SOTTO" if d["lam"][peggio] < d["lc"] else "sopra", d["lc"]))
        print("     Lambda minimo della rete in quel tick: %.4f (nodo %d)"
              % (float(np.min(d["lam"])), int(np.argmin(d["lam"]))))
    print("=" * 100)
    print("### IL CONFRONTO: 32 non converge e 16 converge allo stesso rapporto -> %s"
          % ("SI'" if ok else "### NO"))
    print("### ⛔ OSSERVAZIONE: nessuna cura, nessuna scelta. La decisione e' di Luca.")
    print("=" * 100)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
