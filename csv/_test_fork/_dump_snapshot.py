# -*- coding: utf-8 -*-
"""DUMP COMPLETO DI UNO SNAPSHOT -- tutte le chiavi, in SOLA LETTURA.

PERCHE': il run a 6000 passi si e' FERMATO di scrivere dopo il passo 2700 (frame 450 su 1000),
con il processo VIVO e la CPU al 99.6 % su un solo core. Non si puo' interrogare il processo, ma
lo SNAPSHOT del passo 2700 c'e' ed e' completo: e' lo stato immediatamente PRIMA del blocco.

*** NON TOCCA NULLA ***
Apre i `.pkl.gz` in SOLA LETTURA e scrive il proprio output FUORI dalla cartella del run. Il
processo che sta girando non viene sfiorato -- e' l'unica cosa che si possa fare mentre un run e'
in corso, ed e' esattamente il motivo per cui l'archivio esiste.

COSA STAMPA
  1. i METADATI di versione (blob, commit, branch, dirty) e lo stato dell'RNG
  2. OGNI chiave degli `attrs`: per gli array shape, dtype, NaN/inf, min/p01/mediana/p99/max;
     per gli scalari il valore
  3. i PERCENTILI delle grandezze che possono degenerare
  4. il TREND delle stesse grandezze sugli ultimi snapshot -- un valore isolato non dice se una
     cosa sta esplodendo, due lo dicono
  5. i CONTATORI (A8): tutti i `_*` interi, che sono i rami contati del codice

Un dump non e' una diagnosi. Qui ci sono i NUMERI; la lettura sta nel referto che li accompagna.
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

ARCH = sys.argv[1] if len(sys.argv) > 1 else os.path.join("csv", "_test_fork", "_g6000")
N_TREND = 10
DEGEN = ("d", "d0", "tw", "twp", "phivel", "omega_s", "peq", "vd", "_rep", "rho_spin",
         "_r_corrente", "eta", "pos", "psi", "psi_spin", "_sin2_vir", "_xi_rumore", "mem_mot")


def carica(p):
    ap = gzip.open if p.endswith(".gz") else open
    with ap(p, "rb") as f:
        return pickle.load(f)


def passo_di(p):
    return int(re.search(r"_(\d{6})\.", p).group(1))


def stat(v):
    a = np.abs(np.asarray(v, float)).ravel()
    fin = np.isfinite(a)
    a = a[fin]
    if not a.size:
        return None
    return dict(nonfin=int(np.sum(~fin)), mn=a.min(), p01=np.percentile(a, 1),
                med=np.median(a), p99=np.percentile(a, 99), mx=a.max())


def main():
    fs = sorted(glob.glob(os.path.join(ARCH, "scena_??????.pkl*")))
    if not fs:
        print("NESSUNO SNAPSHOT in %s" % ARCH)
        return 2
    ult = fs[-1]
    st = carica(ult)
    at = st["attrs"]
    print("=" * 100)
    print("DUMP DELLO SNAPSHOT  %s" % os.path.basename(ult))
    print("archivio: %s   snapshot presenti: %d  (dal passo %d al %d)"
          % (ARCH, len(fs), passo_di(fs[0]), passo_di(fs[-1])))
    print("=" * 100)

    print("")
    print("--- 1. METADATI DI VERSIONE ---")
    for k in ("blob", "committed_blob", "commit", "branch", "dirty", "content_hash", "code_hash"):
        print("   %-16s %s" % (k, st.get(k)))
    rng = st.get("rng_state") or {}
    print("   rng_state        bit_generator=%s  has_uint32=%s"
          % (rng.get("bit_generator"), rng.get("has_uint32")))
    print("   n=%d   archi=%d   _db_step=%s"
          % (len(at.get("eta", [])), len(at.get("i", [])), at.get("_db_step")))

    print("")
    print("--- 2. TUTTE LE CHIAVI (%d) ---" % len(at))
    print("%-26s %-16s %-9s %11s %11s %11s %11s %11s" %
          ("chiave", "shape", "dtype", "min", "p01", "mediana", "p99", "MAX"))
    for k in sorted(at):
        v = at[k]
        if isinstance(v, np.ndarray):
            s = stat(v)
            if s is None:
                print("%-26s %-16s %-9s   (vuoto)" % (k, str(v.shape), v.dtype))
                continue
            flag = "  <<< %d NON FINITI" % s["nonfin"] if s["nonfin"] else ""
            print("%-26s %-16s %-9s %11.4g %11.4g %11.4g %11.4g %11.4g%s" %
                  (k, str(v.shape), v.dtype, s["mn"], s["p01"], s["med"], s["p99"], s["mx"], flag))
        elif isinstance(v, (list, tuple)):
            vuoti = sum(1 for x in v if hasattr(x, "__len__") and len(x) == 0)
            print("%-26s %-16s %-9s   len=%d  elementi vuoti=%d"
                  % (k, "", type(v).__name__, len(v), vuoti))
        elif isinstance(v, dict):
            print("%-26s %-16s %-9s   len=%d" % (k, "", "dict", len(v)))
        else:
            print("%-26s %-16s %-9s   %r" % (k, "", type(v).__name__, v))

    print("")
    print("--- 3. PERCENTILI delle grandezze che possono degenerare ---")
    print("%-14s %10s %10s %10s %10s %10s %10s %10s" %
          ("", "p50", "p90", "p99", "p99.9", "MAX", "MAX/p50", "n>10*p50"))
    for k in DEGEN:
        v = at.get(k)
        if not isinstance(v, np.ndarray):
            continue
        a = np.abs(np.asarray(v, float)).ravel()
        a = a[np.isfinite(a)]
        if not a.size:
            continue
        p50 = np.median(a)
        print("%-14s %10.4g %10.4g %10.4g %10.4g %10.4g %10.4g %10d" %
              (k, p50, np.percentile(a, 90), np.percentile(a, 99), np.percentile(a, 99.9),
               a.max(), a.max() / p50 if p50 else float("inf"),
               int(np.sum(a > 10 * p50)) if p50 else -1))

    print("")
    print("--- 4. TREND sugli ultimi %d snapshot ---" % N_TREND)
    print("%-8s %-8s %-9s %s" % ("passo", "n", "archi",
                                 " ".join("%-11s" % k[:11] for k in
                                          ("d0 MAX", "d MAX", "phivel MAX", "omega MAX",
                                           "rho_sp MAX", "r MIN", "fr r<1e-4", "eta MAX"))))
    for p in fs[-N_TREND:]:
        a2 = carica(p)["attrs"]
        g = lambda k: np.abs(np.asarray(a2[k], float)).ravel()
        r = np.asarray(a2["_r_corrente"], float)
        r = r[np.isfinite(r)]
        print("%-8d %-8d %-9d %-11.4g %-11.4g %-11.4g %-11.4g %-11.4g %-11.4g %-11.4f %-11.4g" %
              (passo_di(p), len(a2["eta"]), len(a2["i"]), g("d0").max(), g("d").max(),
               g("phivel").max(), g("omega_s").max(), g("rho_spin").max(),
               r.min() if r.size else float("nan"),
               float(np.mean(r < 1e-4)) if r.size else float("nan"), g("eta").max()))

    print("")
    print("--- 5. CONTATORI (A8: ogni ramo contato) ---")
    for k in sorted(at):
        v = at[k]
        if k.startswith("_") and isinstance(v, (int, np.integer)) and not isinstance(v, bool):
            print("   %-28s %d" % (k, v))

    print("")
    print("--- 6. ARCHI PIU' DEGENERI (d0 contro d) ---")
    d0 = np.asarray(at["d0"], float)
    d = np.asarray(at["d"], float)
    i, j = np.asarray(at["i"]), np.asarray(at["j"])
    print("   archi totali %d;  d0>10: %d   d0>50: %d   d0>100: %d   d0>200: %d"
          % (len(d0), int((d0 > 10).sum()), int((d0 > 50).sum()),
             int((d0 > 100).sum()), int((d0 > 200).sum())))
    ordine = np.argsort(d0)[::-1][:10]
    print("   %-8s %-12s %-12s %-12s %-8s %-8s" % ("rango", "d0", "d", "d/d0", "nodo i", "nodo j"))
    for r_, k in enumerate(ordine):
        print("   %-8d %-12.4f %-12.6f %-12.4e %-8d %-8d"
              % (r_ + 1, d0[k], d[k], d[k] / d0[k] if d0[k] else float("nan"), i[k], j[k]))
    print("")
    print("FINE DUMP. Questi sono NUMERI, non una diagnosi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
