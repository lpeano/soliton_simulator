# -*- coding: utf-8 -*-
"""PARTE 1 -- I CINQUE NODI PERSISTENTI al passo 120 contro il 240. SOLO LETTURA DI DUE FILE.

I cinque sono `16`, `481`, `621`, `627`, `837`: i nodi che PERSISTONO fra i venti archi peggiori del
passo 240 e quelli del 360 (`doc/REFERTO_venti_archi_e_nsub.md` par.3.3, Jaccard 0.217 contro un
nullo di 0.005). **L'evento NASCE fra il 120 e il 240: al 120 i nodi in comune col 240 sono ZERO.**

*** LA DOMANDA, ed e' binaria ***
  Al passo 120 quei cinque erano GIA' DIVERSI, o erano normali?
    gia' anomali -> l'innesco e' VISIBILE nello snapshot
    normali      -> l'innesco nasce NEI 120 passi in mezzo, e serve la rigiocata fine

*** «DIVERSO» SI MISURA, NON SI ASSERISCE ***
  Per ogni campo si stampa il **RANGO PERCENTILE** del nodo nella popolazione, non solo il valore.
  Un nodo al `p50` e' normale; uno al `p99.9` e' anomalo, e la soglia non serve inventarla.

*** ⚠ TRE CAMPI CHE IL MANDATO CHIEDE E CHE NON ESISTONO NELLO SNAPSHOT ***
  **`rho`, `inerzia`, `tau` NON sono salvati** -- verificato elencando gli attributi del `.pkl`, non
  assunto. `inerzia` e' calcolata DENTRO `_passo_spinoriale` da `_rho_sorgente()` e non e'
  ricostruibile senza eseguire codice. **Si dichiara invece di stimarli.**
  **Cio' che C'E' e li sostituisce in parte:** `_cs_nodo_prev` (il `cs` per nodo), `rho_spin`,
  `phi_s`, `phivel`. **E `tau = d/cs` e' DERIVABILE per arco** -- si stampa, dichiarato come
  derivato.
ASCII PURO.
"""
import gzip
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
CINQUE = [16, 481, 621, 627, 837]
PASSI = ("000120", "000240")
RAMO = "B"


def carica(st):
    p = os.path.join(RADICE, "csv", "_test_fork", "_ab_%s" % RAMO, "scena_%s.pkl.gz" % st)
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def rango(v, x):
    """rango percentile di x dentro v: 'diverso' MISURATO, non asserito"""
    v = np.asarray(v)
    return 100.0 * float(np.mean(v < x))


def main():
    A = {st: carica(st) for st in PASSI}
    print("=" * 122)
    print("PARTE 1 -- I CINQUE NODI PERSISTENTI (%s), ramo %s, passo %s contro %s"
          % (", ".join(str(x) for x in CINQUE), RAMO, PASSI[0], PASSI[1]))
    print("  fra parentesi il RANGO PERCENTILE nella popolazione: p50 = normale, p99+ = anomalo")
    print("=" * 122)

    # ---------------------------------------------------------------- per NODO
    campi = [
        ("_deg", lambda a: np.asarray(a["_deg"])),
        ("eta", lambda a: np.asarray(a["eta"])),
        ("perc_chi", lambda a: np.asarray(a["perc_chi"])),
        ("|psi|", lambda a: np.abs(np.asarray(a["psi"]))),
        ("|omega_s|", lambda a: np.linalg.norm(np.asarray(a["omega_s"]), axis=1)),
        ("|mem_mot|", lambda a: np.linalg.norm(np.asarray(a["mem_mot"]), axis=1)),
        ("rho_spin", lambda a: np.asarray(a["rho_spin"])),
        ("phivel", lambda a: np.abs(np.asarray(a["phivel"]))),
        ("phi_s", lambda a: np.asarray(a["phi_s"])),
        ("cs (=_cs_nodo_prev)", lambda a: np.asarray(a["_cs_nodo_prev"])),
        ("|pos|", lambda a: np.linalg.norm(np.asarray(a["pos"]), axis=1)),
    ]
    for nome, f in campi:
        print("")
        print("  %s" % nome)
        for st in PASSI:
            a = A[st]
            n = len(a["phi"])
            v = f(a)[:n]
            righe = []
            for x in CINQUE:
                righe.append("%-6d %9.4g (p%-5.1f)" % (x, v[x], rango(v, v[x])))
            print("    passo %s  pop: p50 %-10.4g p99 %-10.4g max %-10.4g" %
                  (st, np.median(v), np.percentile(v, 99), v.max()))
            for r in righe:
                print("      %s" % r)

    # ---------------------------------------------------------------- i loro ARCHI
    print("")
    print("=" * 122)
    print("  I LORO ARCHI -- lo stiramento era GIA' cominciato al passo %s?" % PASSI[0])
    print("=" * 122)
    for st in PASSI:
        a = A[st]
        ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
        d = np.asarray(a["d"]); d0 = np.asarray(a["d0"]); vd = np.abs(np.asarray(a["vd"]))
        m = min(len(ii), len(jj), len(d), len(d0), len(vd))
        ii, jj, d, d0, vd = ii[:m], jj[:m], d[:m], d0[:m], vd[:m]
        rap = d / np.maximum(d0, 1e-12)
        cs = np.asarray(a["_cs_nodo_prev"])
        n = len(a["phi"])
        csa = 0.5 * (cs[np.minimum(ii, n - 1)] + cs[np.minimum(jj, n - 1)])
        tau = d / np.maximum(csa, 1e-12)          # DERIVATO, dichiarato
        print("")
        print("  passo %s   POPOLAZIONE: d/d0 p50 %.4g p99 %.4g max %.4g | |vd| p50 %.4g p99 %.4g max %.4g"
              % (st, np.median(rap), np.percentile(rap, 99), rap.max(),
                 np.median(vd), np.percentile(vd, 99), vd.max()))
        print("    %-7s %6s %10s %10s %10s %10s %10s %10s" %
              ("nodo", "archi", "d/d0 p50", "d/d0 MAX", "|vd| p50", "|vd| MAX", "d MAX", "tau p50"))
        for x in CINQUE:
            s = (ii == x) | (jj == x)
            k = int(s.sum())
            if not k:
                print("    %-7d %6d  (nessun arco)" % (x, k))
                continue
            print("    %-7d %6d %10.4g %10.4g %10.4g %10.4g %10.4g %10.4g"
                  % (x, k, np.median(rap[s]), rap[s].max(), np.median(vd[s]), vd[s].max(),
                     d[s].max(), np.median(tau[s])))
        # e la coppia peggiore fra i cinque
        sel = np.isin(ii, CINQUE) & np.isin(jj, CINQUE)
        if sel.any():
            t = np.argsort(-vd[sel])[:5]
            print("    archi FRA i cinque (%d): i-j | d/d0 | |vd|" % int(sel.sum()))
            for q in t:
                print("      %d-%d  %.4g  %.4g"
                      % (ii[sel][q], jj[sel][q], rap[sel][q], vd[sel][q]))

    print("")
    print("=" * 122)
    print("⚠ NON MISURABILI da questo snapshot, e si dichiara invece di stimarli:")
    print("   `rho`, `inerzia`, `tau` per NODO -- non sono fra gli attributi salvati.")
    print("   `inerzia` e' calcolata dentro `_passo_spinoriale` da `_rho_sorgente()`:")
    print("   non e' ricostruibile senza eseguire codice.")
    print("   `tau` stampato qui sopra e' PER ARCO e DERIVATO come `d/cs`, non lo stesso oggetto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
