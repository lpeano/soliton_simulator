# -*- coding: utf-8 -*-
"""L'IPOTESI DELLA COMPRESSIONE di Luca, misurata sugli SNAPSHOT GIA' SCRITTI.

*«`S08_proj` scrive `d0` verso l'ALTO senza che `d` segua, e questo abbassa `d/d0`.»*

DUE PROVE INDIPENDENTI, e servono ENTRAMBE:

  PROVA 1 -- FRA I DUE BRACCI, allo STESSO passo. Se l'ipotesi regge, spegnendo `S08_proj`
    **`d0` deve scendere MOLTO PIU' di `d`**. Il numero che decide e' il RAPPORTO fra le due
    sensibilita': `|Delta d0/d0| / |Delta d/d|`. **Se vale ~1, `d` segue e l'ipotesi CADE.**

  PROVA 2 -- TRASVERSALE, a UN SOLO ISTANTE, dentro il braccio ACCESO.
    ⚠ **E' il presidio del par.9:** *«quando una spiegazione e' temporale, il test che la decide
      non deve contenere il tempo»*. Si ricostruisce `proj` -- l'incremento che `S08_proj`
      scrive -- **esattamente come il codice** (`:5657-5669`), e si guarda se gli archi che
      ricevono di piu' hanno `d/d0` piu' BASSO **nello stesso istante**.

IL CRITERIO, SCRITTO PRIMA:
  (1) L'ipotesi REGGE se `|Delta d0/d0| / |Delta d/d| >= 2` su tutti gli snapshot appaiati.
      Se sta fra `0.8` e `1.25`, `d` segue e **l'ipotesi CADE**. Fra `1.25` e `2`: **non
      deciso**, e si scrive cosi'.
  (2) L'ipotesi REGGE nel trasversale se `proj` e' **prevalentemente positivo** (piu' del
      `60 %` degli archi) **e** la correlazione fra `proj` e `d/d0` e' **negativa**.
      ⚠ Il valore sotto IPOTESI NULLA della correlazione su `N` archi e' `~1/sqrt(N)`: con
        `N ~ 5e5` vale `1.4e-03`. Una correlazione di `0.01` **non e' zero**, ma non e'
        nemmeno un effetto: si riporta col suo nullo accanto.

⚠ IL LIMITE DELLA PROVA 2, dichiarato PRIMA: `proj` e' l'incremento ISTANTANEO, `d/d0` e' una
  STORIA. La correlazione c'e' solo se il meccanismo e' PERSISTENTE sugli stessi archi. Un
  risultato nullo qui **non refuta**: dice che l'istantaneo non predice la storia.

SOLA LETTURA. Nessun run, nessun import del simulatore.
ASCII PURO.
"""
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
OUT = os.path.join(_QUI, "_diag_D", "COMPRESSIONE_MEMMOTO.md")
ACCESO = os.path.join(RADICE, "csv", "_test_fork", "_g4_riferimento")
SPENTO = os.path.join(RADICE, "csv", "_test_fork", "_g4_senza_memmoto")
PASSI = (120, 240, 360, 480, 600)


def leggi(cart, passo):
    p = os.path.join(cart, "scena_%06d.pkl.gz" % passo)
    if not os.path.exists(p):
        return None
    with gzip.open(p, "rb") as f:
        return pickle.load(f)["attrs"]


def proiezione(a):
    """Ricostruisce `proj` ESATTAMENTE come `memoria_hebbiana_moto` (`:5657-5669`)."""
    n = int(len(np.asarray(a["_deg"])))
    psi = np.asarray(a["psi"])
    I = np.abs(psi[:n]) ** 2
    Imed = max(float(np.median(I)), 1e-9)
    ii = np.asarray(a["i"]); jj = np.asarray(a["j"])
    mask = (ii < n) & (jj < n)
    ii, jj = ii[mask], jj[mask]
    mm = np.asarray(a["mem_mot"], float)
    if len(mm) < n:
        return None, None
    pos = np.asarray(a["pos"], float)
    v = pos[jj] - pos[ii]
    L = np.maximum(np.linalg.norm(v, axis=1), 1e-9)
    dirarc = v / L[:, None]
    memedge = 0.5 * (mm[ii] * (I[ii, None] / Imed) + mm[jj] * (I[jj, None] / Imed))
    proj = np.sum(memedge * dirarc, axis=1)
    d0 = np.asarray(a["d0"], float)
    passo_max = 0.01 * float(np.median(d0[mask])) if mask.any() else 0.0
    return np.clip(proj, -passo_max, passo_max), mask


def main():
    o = io.open(OUT, "w", encoding="utf-8", newline="\n")
    W = o.write
    W("# L'IPOTESI DELLA COMPRESSIONE — **`S08_proj` alza `d0` senza che `d` segua?**\n\n")
    W("> Ipotesi di Luca, 2026-09-22. Generato da `csv/_test_fork/_compressione_memmoto.py`.\n")
    W("> **Nessun run:** i due bracci di `G4`, blob `ab685eac`, seme `42`, UN seme, UNA scena.\n\n")

    # ------------------------------------------------ PROVA 1
    W("## PROVA 1 — **fra i DUE BRACCI, allo stesso passo**\n\n")
    W("> Se `S08_proj` alza `d0` **senza che `d` segua**, spegnendolo **`d0` deve scendere molto\n")
    W("> piu' di `d`**. Il numero che decide e' il **rapporto fra le due sensibilita'**.\n\n")
    W("| passo | `med d0` acceso | spento | **`Δd0/d0`** | `med d` acceso | spento | "
      "**`Δd/d`** | **rapporto** | `med d/d0` acceso | spento |\n")
    W("|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    rapporti = []
    for passo in PASSI:
        A = leggi(ACCESO, passo); B = leggi(SPENTO, passo)
        if A is None or B is None:
            W("| %d | — | — | — | — | — | — | — | "
              "— | snapshot ASSENTE |\n" % passo)
            continue
        d0a = float(np.median(np.asarray(A["d0"], float)))
        d0b = float(np.median(np.asarray(B["d0"], float)))
        da = float(np.median(np.asarray(A["d"], float)))
        db = float(np.median(np.asarray(B["d"], float)))
        ra = float(np.median(np.asarray(A["d"], float) / np.maximum(np.asarray(A["d0"], float), 1e-12)))
        rb = float(np.median(np.asarray(B["d"], float) / np.maximum(np.asarray(B["d0"], float), 1e-12)))
        s0 = (d0b - d0a) / d0a
        sd = (db - da) / da
        rap = abs(s0) / abs(sd) if sd != 0 else float("inf")
        rapporti.append(rap)
        W("| %d | %.4f | %.4f | **%+.2f %%** | %.4f | %.4f | **%+.2f %%** | **%.2f** | "
          "%.4f | %.4f |\n"
          % (passo, d0a, d0b, 100 * s0, da, db, 100 * sd, rap, ra, rb))
    if rapporti:
        mn, mx = min(rapporti), max(rapporti)
        if mn >= 2.0:
            v = "**REGGE**: `d0` e' almeno `2x` piu' sensibile di `d` su TUTTI gli snapshot"
        elif mx <= 1.25 and mn >= 0.8:
            v = "**CADE**: `d` segue `d0`"
        else:
            v = "**NON DECISO** dal criterio scritto prima"
        W("\n**IL RAPPORTO va da `%.2f` a `%.2f` — %s.**\n" % (mn, mx, v))

    # ------------------------------------------------ PROVA 2
    W("\n## PROVA 2 — **TRASVERSALE, a UN SOLO ISTANTE, nel braccio ACCESO**\n\n")
    W("> `proj` ricostruito **esattamente come il codice** (`:5657-5669`), col clip "
      "`0.01*median(d0)`.\n")
    W("> **Nessun tempo nel test** *(par.9: una spiegazione temporale si decide su un istante)*.\n\n")
    W("| passo | archi | **`proj > 0`** | `med proj` | `somma proj` | al clip | "
      "**corr(`proj`, `d/d0`)** | nullo `1/√N` |\n")
    W("|--:|--:|--:|--:|--:|--:|--:|--:|\n")
    for passo in PASSI:
        A = leggi(ACCESO, passo)
        if A is None:
            continue
        proj, mask = proiezione(A)
        if proj is None:
            W("| %d | — | | | | | | `mem_mot` piu' corto di `n` |\n" % passo)
            continue
        d = np.asarray(A["d"], float)[mask]
        d0 = np.asarray(A["d0"], float)[mask]
        rr = d / np.maximum(d0, 1e-12)
        N = len(proj)
        pmax = float(np.max(np.abs(proj)))
        al_clip = float(np.mean(np.abs(proj) >= pmax * (1 - 1e-12))) if pmax > 0 else 0.0
        cor = (float(np.corrcoef(proj, rr)[0, 1])
               if N > 2 and np.std(proj) > 0 and np.std(rr) > 0 else float("nan"))
        W("| %d | %d | **%.2f %%** | %+.4e | %+.4e | %.4g | **%+.4f** | `%.1e` |\n"
          % (passo, N, 100 * float(np.mean(proj > 0)), float(np.median(proj)),
             float(np.sum(proj)), al_clip, cor, 1.0 / np.sqrt(N)))

    W("\n## LE LETTURE, fissate PRIMA\n\n")
    W("1. **PROVA 1:** REGGE se `|Δd0/d0| / |Δd/d| >= 2` ovunque · CADE se sta fra "
      "`0.8` e `1.25` · altrimenti **NON DECISO**.\n")
    W("2. **PROVA 2:** REGGE se `proj > 0` in piu' del `60 %` degli archi **e** la correlazione "
      "con `d/d0` e' **negativa** e **sopra il suo nullo `1/√N`**.\n")
    W("\n**⚠ IL LIMITE DELLA PROVA 2, dichiarato PRIMA di vedere i numeri:** `proj` e' "
      "l'incremento **ISTANTANEO**, `d/d0` e' una **STORIA**. Un nullo qui **non refuta**: dice "
      "che l'istantaneo non predice la storia. **La PROVA 1 e' quella che decide.**\n")
    W("\n**LIMITI: UN seme, UNA scena, 600 passi, archivi delle cure (blob `ab685eac`).**\n")
    o.close()
    print(io.open(OUT, encoding="utf-8").read())
    return 0


if __name__ == "__main__":
    sys.exit(main())
