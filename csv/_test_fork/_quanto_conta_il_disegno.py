# -*- coding: utf-8 -*-
"""QUANTO CONTA IL DISEGNO: `L_disegno / d`, per regione, nel tempo, e contro il CENTRO. [§1]

⚠ SOLA LETTURA. Nessuna fisica eseguita, nessun `.pkl` scritto, nessuna cura.

PERCHE' ESISTE, e il fatto e' VERIFICATO dal sorgente (non copiato da un mandato):
  `pozzo_grafo` **dichiara** nel suo docstring *«il pozzo non usa la geometria del rendering: ogni
  nodo riceve il contributo di intensita' dei vicini diviso per la DISTANZA REALE dell'arco»*.
  **E poi calcola:**
      v = self.pos[jj] - self.pos[ii]
      L = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
      phi_g += I / L
  **`pos` E' IL DISEGNO** *(la produce `rilassa_disegno()`, che e' un layout)*. **La distanza reale
  dell'arco esiste, ed e' `d`.** Il commento dice il **falso**.

LA DOMANDA: **quanto sono diverse?** Se `L_disegno/d ~ 1` ovunque, il danno e' piccolo. Se e'
lontano da 1, o **dipende da dove si sta nel disegno**, allora **la gravita' di oggi e' in buona
parte un effetto del LAYOUT**, e il disegno **impone un centro** a una legge che non dovrebbe averne.

LE LETTURE, FISSATE PRIMA (mandato del 2026-09-22 §1):
  * `L_disegno/d` **~ 1 ovunque** -> il danno del disegno sulla gravita' e' **piccolo**;
  * **lontano da 1**, o **dipendente dal centro** -> **la gravita' di oggi e' in buona parte un
    effetto del disegno.**

⚠ IL CRITERIO E' COLLAUDATO PRIMA SU DUE CASI A RISPOSTA NOTA (`P1-sexies`): uno che DEVE dire
  «dipende dal centro» e uno che DEVE dire «non dipende». **Un criterio che non puo' fallire non e'
  un criterio.**
ASCII PURO.
"""
import glob
import gzip
import io
import os
import pickle
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
ARCH = os.path.join(RADICE, "csv", "_test_fork", "_val600")
OUT = os.path.join(RADICE, "csv", "_test_fork", "_diag_D", "QUANTO_CONTA_IL_DISEGNO.txt")
N_VUOTO, N0_SEMINA = 900, 2391
# la soglia del giudizio: |r| di Pearson fra `L/d` e la distanza dal centro del DISEGNO.
# ⚠ NON e' scelta: e' il valore sotto IPOTESI NULLA a 3 sigma, `3/sqrt(N)`, calcolato per ogni
#   snapshot dal suo N. Con N ~ 5e5 vale ~0.004, quindi qualunque correlazione vera lo supera.


def regione(k):
    return np.where(k < N_VUOTO, 0, np.where(k < N0_SEMINA, 1, 2))


def collaudo(W):
    """P1-sexies: il criterio si collauda su due casi a RISPOSTA NOTA, prima di usarlo."""
    rng = np.random.default_rng(7)
    N = 20000
    r = rng.random(N) * 10.0
    # caso A: il rapporto DIPENDE dal raggio -> il criterio DEVE dire «dipende»
    a = 1.0 + 0.05 * r + rng.normal(0, 0.01, N)
    # caso B: il rapporto NON dipende -> il criterio DEVE dire «non dipende»
    b = 1.0 + rng.normal(0, 0.5, N)
    soglia = 3.0 / np.sqrt(N)
    ra = float(np.corrcoef(r, a)[0, 1])
    rb = float(np.corrcoef(r, b)[0, 1])
    okA, okB = abs(ra) > soglia, abs(rb) <= soglia
    W("COLLAUDO DEL CRITERIO su due casi a RISPOSTA NOTA (`P1-sexies`), PRIMA di usarlo:\n")
    W("  soglia = 3/sqrt(N) = %.5f   (il valore sotto IPOTESI NULLA a 3 sigma, non scelto)\n"
      % soglia)
    W("  caso A, rapporto che DIPENDE dal raggio   -> r = %+.4f  atteso |r| > soglia  -> %s\n"
      % (ra, "OK" if okA else "*** IL CRITERIO NON LO VEDE ***"))
    W("  caso B, rapporto INDIPENDENTE dal raggio  -> r = %+.4f  atteso |r| <= soglia -> %s\n"
      % (rb, "OK" if okB else "*** IL CRITERIO SEGNALA IL FALSO ***"))
    W("  -> il criterio %s\n\n" % ("DISTINGUE i due casi" if (okA and okB)
                                   else "*** NON DISTINGUE: non lo uso ***"))
    return okA and okB


def main():
    files = sorted(glob.glob(os.path.join(ARCH, "scena_*.pkl.gz")))
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# QUANTO CONTA IL DISEGNO -- `L_disegno / d`, per regione, nel tempo, contro il CENTRO\n")
    W("# SOLA LETTURA sugli snapshot di `_val600`. Nessuna fisica eseguita.\n")
    W("# `L_disegno` = |pos[j] - pos[i]|, esattamente come la calcola `pozzo_grafo`.\n")
    W("# `d` = la lunghezza VERA dell'arco.\n#\n")
    if not collaudo(W):
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1
    if not files:
        W("*** NESSUNO SNAPSHOT in %s ***\n" % ARCH)
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    W("LA DISTRIBUZIONE DI `L_disegno / d`, snapshot per snapshot\n")
    W("%8s %9s | %9s %9s %9s %9s | %9s\n"
      % ("passo", "archi", "p1", "mediana", "p99", "max", "frazione > 2"))
    W("-" * 78 + "\n")
    righe = []
    for p in files:
        with gzip.open(p, "rb") as f:
            a = pickle.load(f)["attrs"]
        pos = np.asarray(a["pos"], float)
        ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
        d = np.asarray(a["d"], float)
        n = len(np.asarray(a["psi"]))
        m = (ii < n) & (jj < n)
        L = np.linalg.norm(pos[jj[m]] - pos[ii[m]], axis=1)
        rap = L / np.maximum(d[m], 1e-300)
        passo = int(a.get("_db_step", -1))
        righe.append((passo, ii[m], jj[m], pos, rap, n))
        W("%8d %9d | %9.4f %9.4f %9.4f %9.4f | %9.4f\n"
          % (passo, len(rap), float(np.percentile(rap, 1)), float(np.median(rap)),
             float(np.percentile(rap, 99)), float(np.max(rap)),
             float(np.mean(rap > 2.0))))

    # ---------------- per REGIONE, sull'ultimo snapshot
    passo, ii, jj, pos, rap, n = righe[-1]
    W("\nPER REGIONE, all'ultimo snapshot (passo %d)\n" % passo)
    W("%-16s %9s | %9s %9s %9s\n" % ("regione dell'arco", "archi", "p1", "mediana", "p99"))
    W("-" * 60 + "\n")
    ri, rj = regione(ii), regione(jj)
    et = ("vuoto", "massa", "nato")
    gruppi = [("vuoto-vuoto", (ri == 0) & (rj == 0)),
              ("massa-massa", (ri == 1) & (rj == 1)),
              ("nato-nato", (ri == 2) & (rj == 2)),
              ("CONFINE vuoto-massa", ((ri == 0) & (rj == 1)) | ((ri == 1) & (rj == 0))),
              ("CONFINE con nato", ((ri == 2) & (rj != 2)) | ((rj == 2) & (ri != 2)))]
    for nome, sel in gruppi:
        if not np.any(sel):
            W("%-16s %9d | %9s %9s %9s\n" % (nome, 0, "-", "-", "-")); continue
        r = rap[sel]
        W("%-16s %9d | %9.4f %9.4f %9.4f\n"
          % (nome, int(np.sum(sel)), float(np.percentile(r, 1)),
             float(np.median(r)), float(np.percentile(r, 99))))

    # ---------------- contro il CENTRO del disegno
    W("\nIL DISEGNO IMPONE UN CENTRO? -- correlazione fra `L/d` e la distanza dal CENTRO\n")
    W("del disegno (baricentro delle posizioni), sul PUNTO MEDIO di ogni arco.\n")
    W("%8s %9s | %10s %10s | %s\n" % ("passo", "archi", "r Pearson", "soglia 3s", "giudizio"))
    W("-" * 78 + "\n")
    giudizi = []
    for passo, ii, jj, pos, rap, n in righe:
        centro = pos[:n].mean(axis=0)
        mid = 0.5 * (pos[ii] + pos[jj])
        dist = np.linalg.norm(mid - centro, axis=1)
        ok = np.isfinite(dist) & np.isfinite(rap)
        N = int(np.sum(ok))
        soglia = 3.0 / np.sqrt(max(N, 1))
        r = float(np.corrcoef(dist[ok], rap[ok])[0, 1]) if N > 3 else float("nan")
        dip = abs(r) > soglia
        giudizi.append(dip)
        W("%8d %9d | %+10.5f %10.5f | %s\n"
          % (passo, N, r, soglia,
             "DIPENDE DAL CENTRO" if dip else "non dipende"))

    W("\n" + "=" * 78 + "\n")
    W("ESITO CONTRO LE LETTURE FISSATE PRIMA\n")
    W("=" * 78 + "\n")
    med_u = float(np.median(righe[-1][4]))
    lontano = abs(med_u - 1.0) > 0.10
    W("  mediana di `L_disegno/d` all'ultimo snapshot: %.4f\n" % med_u)
    W("  -> %s\n" % ("LONTANO da 1 (oltre il 10 per cento): il disegno NON e' una buona"
                     " approssimazione della distanza vera" if lontano
                     else "vicino a 1: il disegno approssima bene la distanza vera"))
    W("  dipendenza dal centro: %d snapshot su %d dicono DIPENDE\n"
      % (sum(giudizi), len(giudizi)))
    W("\n")
    if lontano or all(giudizi):
        W("*** LA GRAVITA' DI OGGI E' IN BUONA PARTE UN EFFETTO DEL DISEGNO. ***\n")
    elif not any(giudizi) and not lontano:
        W("*** IL DANNO DEL DISEGNO SULLA GRAVITA' E' PICCOLO. ***\n")
    else:
        W("*** ESITO MISTO: si legge riga per riga, e si dice cosi'. ***\n")
    W("\nLIMITI: UN seme, UNA scena, 5 snapshot. E il rapporto `L/d` dice quanto le due distanze\n")
    W("  differiscono, NON quanto quella differenza sposti la fisica: per quello serve la prova di\n")
    W("  spegnimento (`G3`).\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
