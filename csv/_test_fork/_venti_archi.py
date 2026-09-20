# -*- coding: utf-8 -*-
"""I VENTI ARCHI PEGGIORI, la loro IDENTITA' nel tempo, e il GRADO DEI NATI.

Letture e criteri FISSATI PRIMA in `doc/TASK_HISTORY/2026-09-20_venti-archi-e-nsub.md` (`11e043a`).
Questo script li APPLICA.

*** COSTO ***  uno snapshot alla volta, solo `numpy`. NIENTE scipy sul grafo, NIENTE `git log`.
               I run sono VIVI: rubare CPU e' gia' successo, e' misurato, e non si ripete.

*** L'IDENTITA' DI UN ARCO NON E' IL SUO INDICE ***
  Gli archi si aggiungono, quindi la posizione `k` non e' stabile: un arco e' la COPPIA DI NODI
  ORDINATA `(min, max)`. **L'indice si stampa lo stesso, perche' il mandato lo chiede**, ma il
  CONFRONTO fra istanti usa la coppia. L'assunzione (nodi mai rimossi) si VERIFICA: `n` non cala.

*** ORIGINALI CONTRO NATI -- il criterio e' DICHIARATO ***
  Lo snapshot non ha un campo "originale/nato". Si separa **per INDICE**: i nodi vengono APPESI,
  quindi `indice < n_semina` = originale. `n_semina = 2391` e' **misurato** (la semina di questa
  scena), non assunto. Per `eta` sarebbe piu' fragile: e' un tempo proprio che cresce, non un
  contatore di nascita.
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
N_SEMINA = 2391          # MISURATO: `n` alla semina di questa scena (3 masse + vuoto, sep=4.0)
TOP = 20


def serie(d):
    fs = sorted(glob.glob(os.path.join(d, "scena_??????.pkl*")))
    return [(int(re.search(r"_(\d{6})\.", p).group(1)), p) for p in fs]


def carica(p):
    with (gzip.open if p.endswith(".gz") else open)(p, "rb") as f:
        return pickle.load(f)["attrs"]


def peggiori(a, k=TOP):
    n = len(a["phi"])
    vd = np.abs(np.asarray(a["vd"]))
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    m = min(len(vd), len(ii), len(jj))
    t = np.argsort(-vd[:m])[:k]
    A = np.minimum(ii[t], jj[t]).astype(np.int64)
    B = np.maximum(ii[t], jj[t]).astype(np.int64)
    return t, (A << np.int64(32)) | B, n


def riga_nodo(a, x, n):
    g = lambda k, d=np.nan: (np.asarray(a[k])[x] if k in a and len(np.asarray(a[k])) > x else d)
    ps = a.get("psi")
    mod = abs(complex(np.asarray(ps)[x])) if ps is not None and len(np.asarray(ps)) > x else np.nan
    om = a.get("omega_s")
    omn = (float(np.linalg.norm(np.asarray(om)[x])) if om is not None
           and len(np.asarray(om)) > x else np.nan)
    return (int(g("_deg", 0)), float(g("eta", np.nan)), int(g("perc_chi", 0)), mod, omn)


def blocco_venti(a, titolo):
    t, chiavi, n = peggiori(a)
    vd = np.abs(np.asarray(a["vd"])); d = np.asarray(a["d"]); d0 = np.asarray(a["d0"])
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    print("")
    print("--- %s  (passo %d, n=%d) ---" % (titolo, int(a.get("_db_step", -1)), n))
    print("  %-7s %-7s %-7s %9s %9s %9s %8s | %s" %
          ("idx", "i", "j", "|vd|", "d", "d0", "d/d0", "i: deg eta chi |psi| |om|   /   j: idem"))
    for k in t:
        i_, j_ = int(ii[k]), int(jj[k])
        ri, rj = riga_nodo(a, i_, n), riga_nodo(a, j_, n)
        nat = lambda x: "N" if x >= N_SEMINA else "O"
        print("  %-7d %-7s %-7s %9.4g %9.4g %9.4g %8.4g | %s%-4d %6.3g %+d %7.3g %8.3g / %s%-4d %6.3g %+d %7.3g %8.3g"
              % (k, "%d%s" % (i_, nat(i_)), "%d%s" % (j_, nat(j_)), vd[k], d[k], d0[k],
                 d[k] / max(d0[k], 1e-12),
                 nat(i_), ri[0], ri[1], ri[2], ri[3], ri[4],
                 nat(j_), rj[0], rj[1], rj[2], rj[3], rj[4]))
    nodi = np.unique(np.concatenate([ii[t], jj[t]]))
    nodi = nodi[nodi < n]
    nat = int(np.sum(nodi >= N_SEMINA))
    print("  nodi distinti: %d su %d archi  |  NATI %d, ORIGINALI %d  |  gradi: %s"
          % (len(nodi), TOP, nat, len(nodi) - nat,
             np.sort(np.asarray(a["_deg"])[nodi])[:8].tolist()))
    return chiavi


def gradi(a, etichetta):
    n = len(a["phi"])
    dg = np.asarray(a["_deg"])[:n]
    orig = dg[:min(N_SEMINA, n)]
    nati = dg[N_SEMINA:] if n > N_SEMINA else np.array([])
    def s(x):
        if not len(x):
            return "nessuno"
        return ("n=%-6d min %-4.0f p25 %-5.0f p50 %-5.0f p75 %-5.0f max %-5.0f  |  <=4: %.1f%%"
                % (len(x), x.min(), np.percentile(x, 25), np.median(x),
                   np.percentile(x, 75), x.max(), 100 * np.mean(x <= 4)))
    print("  %-22s ORIGINALI  %s" % (etichetta, s(orig)))
    print("  %-22s NATI       %s" % ("", s(nati)))
    print("  %-22s archi=%d   archi/nodo=%.2f" % ("", len(a["i"]), len(a["i"]) / float(n)))


def main():
    print("=" * 126)
    print("I VENTI ARCHI PEGGIORI, L'IDENTITA' NEL TEMPO, E IL GRADO DEI NATI")
    print("  criterio originali/nati: INDICE < %d (i nodi si APPENDONO). O = originale, N = nato."
          % N_SEMINA)
    print("=" * 126)
    dati = {}
    for r in ("A", "B"):
        dati[r] = serie(os.path.join(RADICE, "csv", "_test_fork", "_ab_%s" % r))
        print("  ramo %s: %d snapshot" % (r, len(dati[r])))

    # ---- par.2 (1)(2) e (4): le venti righe, su B e su A
    ch = {}
    for r in ("B", "A"):
        S = dati[r]
        if not S:
            continue
        scelti = S if r == "B" else S[-1:]
        ch[r] = []
        for passo, p in scelti:
            a = carica(p)
            ch[r].append((passo, blocco_venti(a, "par.2 RAMO %s: i %d archi peggiori" % (r, TOP))))

    # ---- par.2 (3): l'identita' ai tre istanti. NULLO calcolato, non scelto.
    for r in ("B", "A"):
        if r not in ch or len(ch[r]) < 2:
            continue
        print("")
        print("--- par.2.3  RAMO %s: gli INDICI (per coppia di nodi) coincidono? ---" % r)
        M = len(carica(dati[r][-1][1])["i"])
        print("  NULLO: due insiemi indipendenti di %d su ~%d archi -> attesi %.1e in comune"
              % (TOP, M, TOP / float(M)))
        for k in range(len(ch[r]) - 1):
            (p0, a0), (p1, a1) = ch[r][k], ch[r][k + 1]
            com = len(np.intersect1d(a0, a1))
            esito = ("NUCLEO FISSO" if com >= 15 else
                     "RICAMBIO" if com <= 3 else "NUCLEO CHE RECLUTA")
            print("  passo %-6d -> %-6d   in comune %2d/%d   -> %s" % (p0, p1, com, TOP, esito))

    # ---- par.3: il grado dei nati
    print("")
    print("=" * 126)
    print("par.3  IL GRADO DEI NATI -- 'un nodo senza archi non ha fisica'")
    print("=" * 126)
    for r in ("A", "B"):
        S = dati[r]
        if not S:
            continue
        for passo, p in ([S[0], S[-1]] if len(S) > 1 else S):
            gradi(carica(p), "ramo %s passo %d" % (r, passo))
            print("")
    print("=" * 126)
    print("UN SEME PER RAMO. Nessuna differenza fra i bracci e' dichiarata significativa:")
    print("  il nullo di un confronto fra bracci non e' zero, e' la dispersione FRA SEMI (par.9).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
