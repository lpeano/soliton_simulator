# -*- coding: utf-8 -*-
"""ESTRAZIONE GREZZA DI TUTTI I DATI SU DISCO DEL RAMO D -- un file di testo per Claude web.

Legge i `.pkl.gz` gia' scritti dal ramo D e ne tira fuori **tutto cio' che c'e'**, senza
interpretare: per ogni snapshot, **ogni scalare col suo valore** e **ogni array con la sua forma e
i suoi percentili**. Chi legge il file deve poter fare le proprie domande senza rifare il lavoro.

⚠ E' una LETTURA: non tocca il run, non scrive nella sua cartella, non modifica nulla.
⚠ COSTA CPU (decomprime i `.gz`) e il ramo D sta girando: **un file alla volta**, e si stampa
  quanto ci mette, cosi' il costo e' visibile invece che nascosto.
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import sys
import time

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, ".."))
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_ab_D")
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "DATI_ramoD_2026-09-21.txt")
PCT = (0, 1, 5, 25, 50, 75, 95, 99, 100)


def riga_arr(nome, v):
    v = np.asarray(v)
    if v.dtype.kind in "fc" and v.size:
        w = np.real(v).ravel()
        fin = np.isfinite(w)
        p = np.percentile(w[fin], PCT) if fin.any() else [float("nan")] * len(PCT)
        return ("%-22s shape=%-14s dtype=%-9s  nonfinite=%d  " % (nome, str(v.shape), v.dtype,
                                                                  int((~fin).sum()))
                + "  ".join("p%d=%.6g" % (q, x) for q, x in zip(PCT, p)))
    if v.dtype.kind in "iub" and v.size:
        u, c = np.unique(v.ravel(), return_counts=True)
        if len(u) <= 6:
            return ("%-22s shape=%-14s dtype=%-9s  valori: %s"
                    % (nome, str(v.shape), v.dtype,
                       ", ".join("%s x%d" % (a, b) for a, b in zip(u, c))))
        p = np.percentile(v.ravel(), PCT)
        return ("%-22s shape=%-14s dtype=%-9s  " % (nome, str(v.shape), v.dtype)
                + "  ".join("p%d=%.6g" % (q, x) for q, x in zip(PCT, p)))
    return "%-22s shape=%-14s dtype=%-9s  (vuoto o non numerico)" % (nome, str(v.shape), v.dtype)


def main():
    f = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl*")))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    o.write("# DATI GREZZI DEL RAMO D -- estrazione di tutto cio' che e' su disco\n")
    o.write("# %d snapshot trovati in %s\n" % (len(f), os.path.relpath(ARCH, RADICE)))
    o.write("# EPOCA 2: CHI_COOP + SCALA_MIN + COES_ADIM accesi, piu' la cura del mondo-dopo-i-flag\n")
    o.write("# LA CARTELLA DEL RUN NON E' STATA MODIFICATA: sola lettura.\n")
    o.write("# percentili riportati: %s\n" % (PCT,))
    o.write("#\n# ⚠ COSA QUESTO FILE NON E': non e' un'analisi. Nessun numero qui e' interpretato.\n")
    o.write("#   Chi legge deve poter fare le proprie domande senza rifare l'estrazione.\n\n")
    for p in f:
        t0 = time.time()
        with gzip.open(p, "rb") as fh:
            s = pickle.load(fh)
        a = s["attrs"]
        passo = os.path.basename(p).split("_")[1].split(".")[0]
        o.write("=" * 100 + "\n")
        o.write("SNAPSHOT  passo %s   file %s   %.1f MB\n"
                % (passo, os.path.basename(p), os.path.getsize(p) / 2 ** 20))
        o.write("  blob=%s  committed_blob=%s  commit=%s  branch=%s  dirty=%s\n"
                % (s.get("blob"), s.get("committed_blob"), s.get("commit"),
                   s.get("branch"), s.get("dirty")))
        o.write("=" * 100 + "\n")
        sca = {k: v for k, v in a.items() if not isinstance(v, np.ndarray)}
        arr = {k: v for k, v in a.items() if isinstance(v, np.ndarray)}
        o.write("\n-- SCALARI (%d), col loro valore --\n" % len(sca))
        for k in sorted(sca):
            o.write("  %-30s %s\n" % (k, sca[k]))
        o.write("\n-- ARRAY (%d), forma + percentili --\n" % len(arr))
        for k in sorted(arr):
            o.write("  " + riga_arr(k, arr[k]) + "\n")
        # le grandezze che il mandato chiede come criteri ASSOLUTI
        try:
            d = np.asarray(a["d"]); d0 = np.asarray(a["d0"])
            LAM = 0.8
            st = np.abs(d - d0) / np.maximum(d0, 1e-300)
            o.write("\n-- CRITERI ASSOLUTI (derivati, e la derivazione e' questa riga) --\n")
            o.write("  archi sotto LAM(%.2f):   d=%d   d0=%d   (su %d archi)\n"
                    % (LAM, int((d < LAM).sum()), int((d0 < LAM).sum()), len(d)))
            o.write("  min(d)=%.9f  min(d0)=%.9f\n" % (d.min(), d0.min()))
            o.write("  mediana d=%.6f  d0=%.6f  d/d0=%.6f\n"
                    % (np.median(d), np.median(d0), np.median(d / np.maximum(d0, 1e-300))))
            o.write("  stress |d-d0|/d0:  p50=%.6g  p99=%.6g  max=%.6g\n"
                    % (np.percentile(st, 50), np.percentile(st, 99), st.max()))
            vd = np.asarray(a["vd"])
            o.write("  |vd|:  p50=%.6g  p99=%.6g  max=%.6g\n"
                    % (np.percentile(np.abs(vd), 50), np.percentile(np.abs(vd), 99),
                       np.abs(vd).max()))
            peq = np.asarray(a["peq"])
            nan = int(np.sum(~np.isfinite(peq)))
            o.write("  peq:  non finiti=%d   <=0: %d   min finito=%.6g\n"
                    % (nan, int(np.sum(peq[np.isfinite(peq)] <= 0)),
                       peq[np.isfinite(peq)].min() if np.isfinite(peq).any() else float("nan")))
            pc = np.asarray(a["perc_chi"])
            o.write("  carica perc_chi:  N(+1)=%d  N(-1)=%d  differenza=%d\n"
                    % (int((pc > 0).sum()), int((pc < 0).sum()),
                       int((pc > 0).sum() - (pc < 0).sum())))
            if "perc_geom" in a:
                pg = np.asarray(a["perc_geom"])
                o.write("  geometria perc_geom:  N(+1)=%d  N(-1)=%d   diversi da perc_chi: %d\n"
                        % (int((pg > 0).sum()), int((pg < 0).sum()),
                           int((pg[:len(pc)] != pc[:len(pg)]).sum())))
        except Exception as e:
            o.write("\n-- CRITERI ASSOLUTI: NON calcolabili (%s) --\n" % e)
        o.write("\n")
        print("  passo %s letto in %.1f s" % (passo, time.time() - t0))
    o.close()
    print("\nscritto %s  (%.1f KB)" % (os.path.relpath(OUT, RADICE), os.path.getsize(OUT) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
