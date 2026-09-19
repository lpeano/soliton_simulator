# -*- coding: utf-8 -*-
"""LA QUARTA LETTURA, PER PRIMA -- i nodi di grado 2 sono NEONATI o una STRUTTURA?

Letture FISSATE PRIMA: doc/TASK_HISTORY/2026-09-20_topologia.md (f6d54e9).
NESSUN RUN: i 45 snapshot di _g6000 bastano. Uno alla volta in RAM.

PERCHE' VA PRIMA: se i grado-2 sono neonati non ancora allacciati, la topologia non e' una
struttura ma un TRANSITORIO DEMOGRAFICO, e l'istogramma / il clustering / le catene cambiano
significato. Misurare la forma di un transitorio e chiamarla forma sarebbe l'errore.

IL TEST: si prende l'insieme dei nodi con grado 2 a un passo t0 e si SEGUE IL LORO GRADO negli
snapshot successivi. Gli indici sono stabili perche' i nodi si appendono in coda -- e questo NON si
assume: si VERIFICA (P1).

  il grado CRESCE    -> si allacciano: DEMOGRAFIA
  resta 2 per sempre -> STRUTTURA STABILE

I PRESIDI
 P0  `_deg` deve coincidere col grado RICALCOLATO da i/j su OGNI snapshot letto. Se non coincide,
     `_deg` e' una cache scritta in un altro momento del passo (famiglia Z19) e il resto cade;
     si contano anche auto-anelli e archi DUPLICATI (un arco doppio gonfia il grado).
 P1  STABILITA' DEGLI INDICI, verificata e non assunta: `n` non deve mai calare, e `eta[k]` non
     deve mai DIMINUIRE fra due snapshot consecutivi. Se un indice venisse riusato da un nodo
     nuovo, `eta` crollerebbe: e' il segnale che cerchiamo.
 P2  IL CONTROLLO: si segue anche la coorte dei grado>=3 allo stesso t0. Se crescono TUTTI, la
     crescita dei grado-2 non dice niente di loro (e' il valore sotto ipotesi nulla).
 P3  A3c: mai una mediana sopra due popolazioni. Coorti separate, percentili sempre.

NESSUN NOME. Si riporta la forma, coi numeri.
ASCII PURO.
"""
import glob
import gzip
import os
import pickle
import re
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCHIVIO = os.path.join(RADICE, "csv", "_test_fork", "_g6000")
T0 = [600, 1800]          # due coorti, per non dipendere da un solo istante
ETA_BIN = [0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 1e9]


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def leggi(p):
    """Ritorna SOLO cio' che serve: grado, eta, n. Lo snapshot intero non resta in RAM."""
    with gzip.open(p, "rb") as f:
        at = pickle.load(f)["attrs"]
    n = len(at["eta"])
    i = np.asarray(at["i"])
    j = np.asarray(at["j"])
    deg_ric = np.bincount(np.concatenate([i, j]), minlength=n)[:n]
    deg_sal = np.asarray(at["_deg"])[:n] if "_deg" in at else None
    loop = int((i == j).sum())
    a = np.minimum(i, j).astype(np.int64) * (n + 1) + np.maximum(i, j).astype(np.int64)
    dup = int(len(a) - len(np.unique(a)))
    eta = np.asarray(at["eta"], float)[:n].copy()
    del at, i, j, a
    return dict(n=n, deg=deg_ric, deg_sal=deg_sal, eta=eta, loop=loop, dup=dup,
                narchi=int(deg_ric.sum() // 2))


def pct(a, p):
    return float(np.percentile(a, p)) if len(a) else float("nan")


def main():
    fs = sorted(glob.glob(os.path.join(ARCHIVIO, "scena_??????.pkl*")))
    if not fs:
        print("nessuno snapshot in %s" % ARCHIVIO)
        return 1
    passi = [passo_di(p) for p in fs]
    print("archivio: %d snapshot, passi %d -> %d (cadenza %d)"
          % (len(fs), passi[0], passi[-1], passi[1] - passi[0] if len(passi) > 1 else 0))
    print("")

    print("=" * 118)
    print("P0/P1 -- IL GRADO E' QUELLO SALVATO? GLI INDICI SONO STABILI?  (verificato, non assunto)")
    print("=" * 118)
    print("%-7s %-7s %-9s | %-11s %-7s %-7s | %-26s" %
          ("passo", "n", "archi", "deg!=_deg", "loop", "dup", "eta DIMINUITA su k indici"))
    dati = {}
    eta_prec = None
    p0_ko = p1_ko = 0
    for p, passo in zip(fs, passi):
        d = leggi(p)
        mis = (int(np.sum(d["deg"] != d["deg_sal"])) if d["deg_sal"] is not None
               and len(d["deg_sal"]) == d["n"] else -1)
        cala = 0
        if eta_prec is not None:
            m = min(len(eta_prec), d["n"])
            cala = int(np.sum(d["eta"][:m] < eta_prec[:m] - 1e-12))
        if mis != 0:
            p0_ko += 1
        if cala or (eta_prec is not None and d["n"] < len(eta_prec)):
            p1_ko += 1
        print("%-7d %-7d %-9d | %-11s %-7d %-7d | %d" %
              (passo, d["n"], d["narchi"],
               ("OK" if mis == 0 else ("*** %d ***" % mis if mis > 0 else "ASSENTE")),
               d["loop"], d["dup"], cala))
        eta_prec = d["eta"]
        dati[passo] = dict(deg=d["deg"], eta=d["eta"], n=d["n"])
    print("")
    print("  P0: %s      P1: %s"
          % ("PASSA su tutti gli snapshot" if p0_ko == 0 else "*** FALLISCE su %d ***" % p0_ko,
             "PASSA (indici stabili)" if p1_ko == 0 else "*** FALLISCE su %d ***" % p1_ko))
    if p0_ko or p1_ko:
        print("  -> un presidio non passa: il seguito NON si legge. FERMO.")
        return 2
    print("")

    for t0 in T0:
        if t0 not in dati:
            continue
        S = np.flatnonzero(dati[t0]["deg"] == 2)
        C = np.flatnonzero(dati[t0]["deg"] >= 3)
        print("=" * 118)
        print("COORTE t0 = %d   grado-2: %d su %d (%.1f %%)   grado>=3: %d   [P2: il controllo]"
              % (t0, len(S), dati[t0]["n"], 100.0 * len(S) / dati[t0]["n"], len(C)))
        print("  eta al t0:  grado-2 p25/p50/p75 = %.3f / %.3f / %.3f   |   grado>=3 = %.3f / %.3f / %.3f"
              % (pct(dati[t0]["eta"][S], 25), pct(dati[t0]["eta"][S], 50),
                 pct(dati[t0]["eta"][S], 75), pct(dati[t0]["eta"][C], 25),
                 pct(dati[t0]["eta"][C], 50), pct(dati[t0]["eta"][C], 75)))
        print("=" * 118)
        print("%-7s | %-42s | %-26s" % ("", "COORTE grado-2 al t0", "CONTROLLO grado>=3 al t0"))
        print("%-7s | %-9s %-7s %-7s %-7s %-7s | %-7s %-7s %-7s" %
              ("passo", "ancora2 %", "p25", "p50", "p75", "max", "p25", "p50", "p75"))
        for passo in passi:
            if passo < t0:
                continue
            dg = dati[passo]["deg"]
            if len(dg) <= S.max():
                continue
            s = dg[S]
            c = dg[C]
            print("%-7d | %-9.1f %-7.0f %-7.0f %-7.0f %-7d | %-7.0f %-7.0f %-7.0f"
                  % (passo, 100.0 * np.mean(s == 2), pct(s, 25), pct(s, 50), pct(s, 75),
                     int(s.max()), pct(c, 25), pct(c, 50), pct(c, 75)))
        print("")

    print("=" * 118)
    print("IL GRADO CONTRO L'ETA', allo stesso istante -- se e' demografia, i VECCHI non sono grado-2")
    print("=" * 118)
    for passo in (600, 1800, 2700):
        if passo not in dati:
            continue
        eta = dati[passo]["eta"]
        dg = dati[passo]["deg"]
        print("passo %d  (n = %d)" % (passo, dati[passo]["n"]))
        print("   %-16s %-8s %-8s %-8s %-8s %-10s" %
              ("fascia di eta", "quanti", "deg p25", "deg p50", "deg p75", "grado2 %"))
        for k in range(len(ETA_BIN) - 1):
            m = (eta >= ETA_BIN[k]) & (eta < ETA_BIN[k + 1])
            if not m.any():
                continue
            d2 = dg[m]
            et = "[%.1f, %s)" % (ETA_BIN[k],
                                 "inf" if ETA_BIN[k + 1] > 1e8 else "%.1f" % ETA_BIN[k + 1])
            print("   %-16s %-8d %-8.0f %-8.0f %-8.0f %-10.1f"
                  % (et, int(m.sum()), pct(d2, 25), pct(d2, 50), pct(d2, 75),
                     100.0 * np.mean(d2 == 2)))
        print("")

    print("=" * 118)
    print("I NODI GIA' PRESENTI AL PASSO %d, guardati al passo %d" % (passi[0], passi[-1]))
    print("=" * 118)
    n0 = dati[passi[0]]["n"]
    dg0 = dati[passi[0]]["deg"]
    dgf = dati[passi[-1]]["deg"][:n0]
    s0 = np.flatnonzero(dg0 == 2)
    print("  al passo %d erano %d nodi, di cui %d di grado 2" % (passi[0], n0, len(s0)))
    if len(s0):
        print("  al passo %d quegli STESSI %d nodi: p25/p50/p75 = %.0f / %.0f / %.0f, "
              "ancora grado 2: %.1f %%"
              % (passi[-1], len(s0), pct(dgf[s0], 25), pct(dgf[s0], 50), pct(dgf[s0], 75),
                 100.0 * np.mean(dgf[s0] == 2)))
    print("  e TUTTI gli n=%d di allora: p25/p50/p75 = %.0f / %.0f / %.0f, grado 2: %.1f %%"
          % (n0, pct(dgf, 25), pct(dgf, 50), pct(dgf, 75), 100.0 * np.mean(dgf == 2)))
    print("")
    print("UN SEME, UNA SCENA. Nessun nome, nessuna identificazione: si riporta il grado e l'eta'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
