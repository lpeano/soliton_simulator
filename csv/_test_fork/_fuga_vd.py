# -*- coding: utf-8 -*-
"""LA FUGA DI `|vd|`: serie nel tempo, forma della coda, e IDENTITA' degli archi veloci.

Letture e criteri FISSATI PRIMA in `doc/TASK_HISTORY/2026-09-20_fuga-vd-ramoB.md` (`012549f`),
committato prima di guardare i numeri. Questo script li APPLICA.

*** COSTO -- il vincolo esplicito del mandato ***
  UNO SNAPSHOT ALLA VOLTA, e solo `numpy` su array per-arco: percentili e `argpartition` su ~528k
  float sono millisecondi. **NIENTE scipy sul grafo, NIENTE `git log`.** Il costo reale e' l'I/O
  (~36 MB compressi a snapshot), e si legge **una volta sola** tenendo i risultati in memoria.
  I run sono VIVI: rubare CPU e' gia' successo, e' misurato, e non si ripete.

*** ⚠ L'IDENTITA' DI UN ARCO NON E' IL SUO INDICE ***
  Gli archi si aggiungono (`528031 -> 528158`), quindi la posizione `k` negli array NON e' stabile.
  Un arco si identifica con la **COPPIA DI NODI ORDINATA** `(min(i,j), max(i,j))`, impacchettata in
  un intero a 64 bit per poterla confrontare con `np.intersect1d`.
  **L'assunzione -- che i nodi non vengano RIMOSSI -- viene VERIFICATA, non assunta:** si controlla
  che `n` non cali fra snapshot consecutivi, e se cala si dichiara la misura non valida.

*** IL NULLO DELLA SOVRAPPOSIZIONE SI CALCOLA, NON SI SCEGLIE ***
  Due insiemi indipendenti di `K` archi su `M` danno sovrapposizione attesa `~K/M`: per `K = 100` su
  `528k` vale **`1.9e-4`**. Quindi QUALUNQUE sovrapposizione apprezzabile e' un segnale.
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
DT, CS_M = 0.01, 2.0        # dichiarati: NON si importa il simulatore (costerebbe e non serve)
SOGLIE = (1.0, 3.0, 10.0, 30.0, 100.0)
K = 100                      # quanti archi "veloci" si seguono per l'identita'


def serie(d):
    fs = sorted(glob.glob(os.path.join(d, "scena_??????.pkl*")))
    return [(int(re.search(r"_(\d{6})\.", p).group(1)), p) for p in fs]


def chiave_archi(ii, jj):
    """(min,max) impacchettata: l'identita' STABILE di un arco. Richiede nodi < 2**31."""
    a = np.minimum(ii, jj).astype(np.int64)
    b = np.maximum(ii, jj).astype(np.int64)
    return (a << np.int64(32)) | b


def leggi(p):
    with (gzip.open if p.endswith(".gz") else open)(p, "rb") as f:
        a = pickle.load(f)["attrs"]
    n = len(a["phi"])
    vd = np.abs(np.asarray(a["vd"]))
    d = np.asarray(a["d"])
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    m = min(len(vd), len(ii), len(jj), len(d))
    vd, d, ii, jj = vd[:m], d[:m], ii[:m], jj[:m]
    top = np.argpartition(vd, -min(K, m))[-min(K, m):]
    top = top[np.argsort(-vd[top])]
    return dict(passo=int(a.get("_db_step", -1)), n=n, archi=m,
                vmax=float(vd.max()), p50=float(np.percentile(vd, 50)),
                p99=float(np.percentile(vd, 99)), p999=float(np.percentile(vd, 99.9)),
                dmed=max(float(np.median(d)), 0.1),
                conte=[int(np.sum(vd > s)) for s in SOGLIE],
                kt=chiave_archi(ii[top], jj[top]),
                d0=np.asarray(a["d0"])[:m], dd=d, vdd=vd, iii=ii, jjj=jj,
                pc=np.asarray(a["perc_chi"])[:n], eta=np.asarray(a["eta"])[:n], top=top)


def n3(v, dmed):
    return float(np.ceil(v * DT / (0.1 * dmed)))


def main():
    print("=" * 118)
    print("LA FUGA DI |vd| -- criteri FISSATI PRIMA in doc/TASK_HISTORY/2026-09-20_fuga-vd-ramoB.md")
    print("=" * 118)
    dati = {}
    for r in ("A", "B"):
        d = os.path.join(RADICE, "csv", "_test_fork", "_ab_%s" % r)
        dati[r] = [leggi(p) for _, p in serie(d)]
        print("  ramo %s: %d snapshot" % (r, len(dati[r])))

    for r in ("A", "B"):
        S = dati[r]
        if not S:
            continue
        print("")
        print("--- par.2.1  RAMO %s: LA SERIE NEL TEMPO ---" % r)
        print("  %-7s %-7s %10s %10s %10s %10s %6s %8s" %
              ("passo", "n", "|vd|.p50", "|vd|.p99", "|vd|.p999", "|vd|.MAX", "n3", "r_k"))
        prev = None
        for s in S:
            rk = (s["vmax"] / prev) if prev else float("nan")
            print("  %-7d %-7d %10.4g %10.4g %10.4g %10.4g %6.0f %8s" %
                  (s["passo"], s["n"], s["p50"], s["p99"], s["p999"], s["vmax"],
                   n3(s["vmax"], s["dmed"]), ("%.2f" % rk) if prev else "--"))
            prev = s["vmax"]
        print("  conteggi  #{|vd| > %s}:" % (", ".join(str(x) for x in SOGLIE)))
        for s in S:
            print("    passo %-7d %s" % (s["passo"], s["conte"]))

    # ---- par.2.2 IDENTITA', e prima la verifica che l'identita' REGGA
    for r in ("A", "B"):
        S = dati[r]
        if len(S) < 2:
            continue
        print("")
        print("--- par.2.2  RAMO %s: gli archi veloci sono GLI STESSI? (primi %d per |vd|) ---" % (r, K))
        cali = [(S[k]["passo"], S[k]["n"], S[k + 1]["n"])
                for k in range(len(S) - 1) if S[k + 1]["n"] < S[k]["n"]]
        if cali:
            print("  *** `n` CALA fra snapshot: l'identita' (i,j) NON regge. %s ***" % cali[:3])
            continue
        print("  (verificato: `n` non cala mai -> l'identita' per coppia di nodi e' valida)")
        M = S[-1]["archi"]
        print("  NULLO: due insiemi indipendenti di %d archi su %d -> sovrapposizione attesa %.2e"
              % (K, M, K / float(M)))
        for k in range(len(S) - 1):
            a, b = S[k]["kt"], S[k + 1]["kt"]
            com = len(np.intersect1d(a, b))
            J = com / float(len(np.union1d(a, b)))
            print("  passo %-6d -> %-6d   comuni %3d/%d   Jaccard %.3f   (nullo %.2e)"
                  % (S[k]["passo"], S[k + 1]["passo"], com, K, J, K / float(M)))

    # ---- par.2.3 DOVE STANNO, sull'ultimo snapshot di ogni ramo
    for r in ("A", "B"):
        S = dati[r]
        if not S:
            continue
        s = S[-1]
        t = s["top"]
        print("")
        print("--- par.2.3  RAMO %s: DOVE STANNO i %d archi piu' veloci (passo %d) ---"
              % (r, K, s["passo"]))
        dd, d0 = s["dd"][t], s["d0"][t]
        rap = dd / np.maximum(d0, 1e-12)
        print("  |vd|      p50 %-10.4g max %-10.4g" % (np.median(s["vdd"][t]), s["vdd"][t].max()))
        print("  d         p50 %-10.4g   contro la mediana di TUTTI gli archi %-10.4g"
              % (np.median(dd), np.median(s["dd"])))
        print("  d0        p50 %-10.4g   contro TUTTI %-10.4g" % (np.median(d0), np.median(s["d0"])))
        print("  d/d0      p50 %-10.4g  min %-10.4g  max %-10.4g   (<1 = COMPRESSO)"
              % (np.median(rap), rap.min(), rap.max()))
        nodi = np.unique(np.concatenate([s["iii"][t], s["jjj"][t]]))
        nodi = nodi[nodi < s["n"]]
        pc = s["pc"][nodi]
        print("  nodi coinvolti: %d distinti su %d archi  (%.2f nodi per arco = %s)"
              % (len(nodi), K, len(nodi) / float(K),
                 "REGIONE LOCALIZZATA" if len(nodi) < 1.6 * K else "sparsi"))
        print("  perc_chi dei nodi: +1 %d   -1 %d   0 %d   |  nel sistema: +1 %d  -1 %d"
              % (int(np.sum(pc > 0)), int(np.sum(pc < 0)), int(np.sum(pc == 0)),
                 int(np.sum(s["pc"] > 0)), int(np.sum(s["pc"] < 0))))
        et = s["eta"][nodi]
        print("  eta dei nodi:     p50 %-10.4g   contro TUTTI %-10.4g   (bassa = NEONATI)"
              % (np.median(et), np.median(s["eta"])))
    print("")
    print("=" * 118)
    print("UN SEME PER RAMO. Nessuna differenza fra i bracci e' dichiarata significativa:")
    print("  il nullo di un confronto fra bracci NON e' zero, e' la dispersione FRA SEMI (par.9),")
    print("  che questo esperimento non misura. E NON e' un verdetto: e' una misura.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
