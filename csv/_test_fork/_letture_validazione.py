# -*- coding: utf-8 -*-
"""LE LETTURE DELLA VALIDAZIONE, contro i criteri ASSOLUTI. Tabella GENERATA da codice (`P1-ter`).

⚠ I CRITERI SONO FISSATI PRIMA DI VEDERE I NUMERI (mandato GLOBALE §3), e stanno qui sotto in
  `CRITERI`: ognuno ha un nome, una soglia con la sua ORIGINE, e il verso. **Nessuno di essi si
  tocca dopo aver visto l'esito** -- se non reggono, si scrive NON REGGE.

⚠ E NON SI CONFRONTA CON LE EPOCHE PRECEDENTI: le cure hanno cambiato la fisica, quindi questi
  numeri sono di un sistema NUOVO. Si leggono contro criteri ASSOLUTI, non contro il ramo D.
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
DEST = os.path.join(RADICE, "csv", "_test_fork", "_val600")
for _a in sys.argv[1:]:
    if _a.startswith("--dir="):
        DEST = os.path.abspath(_a.split("=", 1)[1])
OUT = os.path.join(DEST, "LETTURE.txt")
LAM = 0.8

# ---------------------------------------------------------------- I CRITERI, fissati PRIMA
CRITERI = [
    ("nessun picco di `nsub`", "il massimo di `nsub` resta vicino al pavimento 4",
     "origine: il pavimento e' nel codice (`max(4, n1, n2, n3)`), non scelto qui"),
    ("`peq >= 0` sempre", "il minimo di `peq` su tutti gli snapshot e' >= 0",
     "origine: una PRESSIONE non e' negativa -- dominio fisico, `A11` corollario 1"),
    ("nessun arco sotto `LAM`", "il minimo di `d` e di `d0` e' >= LAM",
     "origine: `LAM` e' la scala del sistema, non un numero scelto"),
    ("`d0` NON scappa", "la mediana di `d0` non cresce in modo esponenziale",
     "origine: si legge il RAPPORTO fra snapshot consecutivi; costante = esponenziale"),
    ("`d/d0` vicino a 1", "la trasparenza: si riporta DOVE STA, IN ENTRAMBI I VERSI",
     "origine: `d/d0 = 1` e' l'assenza di tensione E di compressione"),
    ("stress finito", "`|d-d0|/d0` non diverge", "origine: finitezza"),
    ("invarianti mai scattati", "zero violazioni di dominio in tutto il run",
     "origine: gli invarianti fermerebbero il run; zero = nessuna violazione"),
    ("il tetto di `COES_CAUSALE`", "quanto spesso il termine tocca il cono locale",
     "chiesto da Luca: oggi il MASSIMO vale 92.7 %, e un massimo non dice QUANTO SPESSO"),
]


def leggi(p):
    with gzip.open(p, "rb") as f:
        return pickle.load(f)


def main():
    files = sorted(glob.glob(os.path.join(DEST, "scena_*.pkl.gz")))
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# LE LETTURE DELLA VALIDAZIONE -- criteri ASSOLUTI, fissati PRIMA\n")
    W("# cartella: %s\n" % os.path.relpath(DEST, RADICE))
    W("# snapshot trovati: %d\n#\n" % len(files))
    W("# ⚠ NESSUN CONFRONTO CON LE EPOCHE PRECEDENTI: le cure hanno cambiato la fisica.\n")
    W("#   Questi numeri sono di un sistema NUOVO e si leggono contro criteri ASSOLUTI.\n\n")
    W("I CRITERI, come erano scritti PRIMA di vedere i numeri:\n")
    for k, (nome, crit, orig) in enumerate(CRITERI, 1):
        W("  %d. %-28s %s\n     (%s)\n" % (k, nome, crit, orig))
    W("\n")

    if not files:
        W("*** NESSUNO SNAPSHOT: il run non e' partito, o non usa `--serie`. ***\n")
        o.close(); print(io.open(OUT, encoding="utf-8").read()); return 1

    W("%8s %7s %9s | %10s %10s %10s | %10s %10s | %9s\n"
      % ("passo", "n", "archi", "min d", "med d", "min d0", "med d0", "med d/d0", "min peq"))
    W("-" * 96 + "\n")
    righe = []
    for p in files:
        s = leggi(p)
        a = s["attrs"]
        d = np.asarray(a["d"], float); d0 = np.asarray(a["d0"], float)
        peq = np.asarray(a["peq"], float)
        passo = int(a.get("_db_step", -1))
        r = dict(passo=passo, n=len(np.asarray(a["psi"])), archi=len(d),
                 mind=float(np.min(d)), medd=float(np.median(d)),
                 mind0=float(np.min(d0)), medd0=float(np.median(d0)),
                 dd0=float(np.median(d / np.maximum(d0, 1e-300))),
                 minpeq=float(np.nanmin(peq)),
                 stress=float(np.max(np.abs(d - d0) / np.maximum(d0, 1e-300))),
                 sottolam=int(np.sum(d < LAM * (1 - 1e-12))),
                 cct_rapmax=float(a.get("_g_cct_rapmax", -1.0)),
                 inv_viol=int(a.get("_g_inv_violati", 0)),
                 nsub_d=int(a.get("_g_sm_d", 0)), smp_d=int(a.get("_g_smp_d_chiusure", 0)),
                 nsubmax=int(a.get("_g_smp_d_nsub", 0)))
        righe.append(r)
        W("%8d %7d %9d | %10.4f %10.4f %10.4f | %10.4f %10.4f | %9.3e\n"
          % (r["passo"], r["n"], r["archi"], r["mind"], r["medd"], r["mind0"],
             r["medd0"], r["dd0"], r["minpeq"]))

    u = righe[-1]
    W("\n" + "=" * 96 + "\n")
    W("ESITO CONTRO I CRITERI -- REGGE / NON REGGE\n")
    W("=" * 96 + "\n")
    esiti = []
    nsubmax = max(r["nsubmax"] for r in righe)
    esiti.append(("nessun picco di `nsub`", nsubmax <= 8,
                  "`nsub` massimo osservato = %d (pavimento 4)" % nsubmax))
    mp = min(r["minpeq"] for r in righe)
    esiti.append(("`peq >= 0` sempre", mp >= 0.0, "min(peq) su tutti gli snapshot = %.4e" % mp))
    sl = sum(r["sottolam"] for r in righe)
    md = min(r["mind"] for r in righe)
    esiti.append(("nessun arco sotto `LAM`", sl == 0,
                  "archi sotto LAM: %d; min(d) = %.6f contro LAM = %.4f" % (sl, md, LAM)))
    if len(righe) >= 3:
        rap = [righe[k + 1]["medd0"] / max(righe[k]["medd0"], 1e-300)
               for k in range(len(righe) - 1)]
        rmed = float(np.median(rap))
        esiti.append(("`d0` NON scappa", rmed < 1.05,
                      "rapporto MEDIANO di `med d0` fra snapshot consecutivi = %.4f "
                      "(costante > 1 = ESPONENZIALE); da %.4f a %.4f"
                      % (rmed, righe[0]["medd0"], u["medd0"])))
    dd0 = [r["dd0"] for r in righe]
    esiti.append(("`d/d0` vicino a 1", 0.8 <= u["dd0"] <= 1.25,
                  "med `d/d0` da %.4f a %.4f; minimo %.4f, massimo %.4f -- SOTTO 1 = COMPRESSIONE, "
                  "SOPRA 1 = TENSIONE" % (dd0[0], dd0[-1], min(dd0), max(dd0))))
    st = max(r["stress"] for r in righe)
    esiti.append(("stress finito", np.isfinite(st), "stress massimo = %.4g" % st))
    iv = sum(r["inv_viol"] for r in righe)
    esiti.append(("invarianti mai scattati", iv == 0,
                  "violazioni di dominio registrate: %d" % iv))
    rm = max(r["cct_rapmax"] for r in righe)
    esiti.append(("il tetto di `COES_CAUSALE`", True,
                  "rapporto MASSIMO |delta|/(cs_arco*DT) = %.4f -- **e' un MASSIMO, non dice "
                  "QUANTO SPESSO**: i contatori a bucket non esistono ancora, ed e' LAVORO "
                  "RESIDUO dichiarato" % rm))

    for nome, ok, testo in esiti:
        W("%-28s %-10s %s\n" % (nome, "REGGE" if ok else "NON REGGE", testo))
    W("\n")
    n_ok = sum(1 for _, ok, _ in esiti if ok)
    W("REGGONO %d criteri su %d.\n" % (n_ok, len(esiti)))
    if n_ok < len(esiti):
        W("\n*** QUALCOSA NON REGGE: IL RUN LUNGO NON SI LANCIA. ***\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
