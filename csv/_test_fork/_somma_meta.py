# -*- coding: utf-8 -*-
"""**`np.sum(concatenate([x, x]))` E' IDENTICA AL BIT A `2 * np.sum(x)`? NO.**

### Nasce da un RILIEVO DEL GUARDIANO sul mio task history del `COMMIT 6a` *(2026-10-03)*,
e il rilievo e' giusto.

## ⛔ **CHE COSA AVEVO SCRITTO, E PERCHE' ERA SBAGLIATO**

Nel task history `621cfbd` ho scritto che portando `_nasce` da ### **una chiamata con
`md = 2`** su un array di `n` voci a ### **una chiamata con `md = 1`** su un array di `2n`
*(le due meta' `t*d` e `(1-t)*d`)*, a `t = 0.5` ### **<<tutti e quattro i numeri
coincidono>>**.

| il contatore | che cos'e' | coincide? |
|---|---|---|
| `_g_sm_nascite` | ### **un intero**, `+1` per invocazione | ### **SI'** |
| `_sm_tr<q>_<sito>` | ### **un intero**, `md * ntr` | ### **SI'** |
| `_sm_vis<q>_<sito>` | ### **un intero**, `md * v.size` | ### **SI'** |
| ### **`_sm_lun<q>_<sito>`** | ### **un FLOAT**: `md * sum(LAM - v)` sui troncati | ### **NO** |

### ➜ **E il motivo e' l'ASSOCIATIVITA':** `np.sum` su `2n` elementi somma in un ordine
*(e con una riduzione a coppie)* che ### **non e' `2 *` la somma su `n`**. ### **Gli interi
non se ne accorgono, i float SI'.**

## ✅ **LA FORMA CHE REGGE, e la misura la conferma**

### **`fab_a + fab_b`** -- la somma calcolata ### **PER META'** e poi sommata. A `t = 0.5` le
due meta' sono ### **identiche**, quindi `s + s`, e ### **`s + s == 2 * s` E' ESATTO** perche'
il raddoppio e' uno scalamento per una potenza di due.

### \U0001f4cc **E il difetto NON e' accademico, e conta nel `6b`:** con `t != 0.5` le due
meta' ### **sono diverse**, `t*d` puo' scendere ### **sotto `LAM`** anche con `d >= 2 LAM`
*(`0.4 * 1.6 = 0.64 < 0.8`)* -- e allora ### **i troncamenti ci sono davvero**, e `_fab`
### **non e' piu' zero.**

**COMANDO:** `python csv/_test_fork/_somma_meta.py`
**USCITA:** `csv/_test_fork/_somma_meta/`
"""
import hashlib
import io
import json
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_QUI, ".."))
import _presidio   # noqa: E402

_presidio.avvia(__file__)

import numpy as np   # noqa: E402

FUORI = os.path.join(_QUI, "_somma_meta")
NL = chr(10)
TAGLIE = (2, 3, 4, 9, 17, 33, 128)
PROVE = 2000
SEME = 20261003
LAM = 0.8


def principale():
    out = []

    def stampa(*x):
        s = " ".join(str(y) for y in x)
        out.append(s)
        print(s)

    if not os.path.isdir(FUORI):
        os.makedirs(FUORI)
    rng = np.random.default_rng(SEME)
    stampa("=" * 100)
    stampa("np.sum(concatenate([x, x])) E' IDENTICA AL BIT A 2 * np.sum(x)?")
    stampa("=" * 100)
    stampa("  strumento .. %s (sha1 byte grezzi)"
           % hashlib.sha1(io.open(os.path.abspath(__file__), "rb").read()).hexdigest()[:8])
    stampa("  %d prove per taglia, seme %d, numpy %s" % (PROVE, SEME, np.__version__))
    stampa("")
    stampa("  LE TRE FORME messe a confronto, su x di taglia n:")
    stampa("    (A)  np.sum(np.concatenate([x, x]))   <- UNA chiamata su 2n (md = 1)")
    stampa("    (B)  2.0 * np.sum(x)                  <- la chiamata di OGGI (md = 2)")
    stampa("    (C)  np.sum(x) + np.sum(x)            <- PER META' e sommate (la cura)")
    stampa("")
    stampa("  %-6s %14s %14s   %s" % ("n", "(A) != (B)", "(C) != (B)", "verdetto"))
    stampa("  " + "-" * 72)
    righe = []
    for n in TAGLIE:
        dA = dC = 0
        for _ in range(PROVE):
            # ### I VALORI SONO QUELLI DI `_fab`: `LAM - v` sui troncati, cioe' POSITIVI
            #   e piccoli. Si generano come `v` sotto `LAM` e si misura `LAM - v`.
            v = rng.uniform(0.0, LAM, n)
            x = LAM - v
            a = float(np.sum(np.concatenate([x, x])))
            b = 2.0 * float(np.sum(x))
            c = float(np.sum(x)) + float(np.sum(x))
            dA += int(a != b)
            dC += int(c != b)
        righe.append({"n": n, "A_diverse": dA, "C_diverse": dC, "prove": PROVE})
        stampa("  %-6d %14d %14d   %s"
               % (n, dA, dC,
                  ("(A) DIVERGE, (C) tiene" if dA and not dC
                   else "(A) tiene" if not dA and not dC
                   else "*** (C) DIVERGE: la cura non regge ***")))
    stampa("")
    tot_A = sum(r["A_diverse"] for r in righe)
    tot_C = sum(r["C_diverse"] for r in righe)
    stampa("=" * 100)
    stampa("### IL VERDETTO")
    stampa("###   (A) np.sum(concatenate([x, x])) contro 2*np.sum(x):")
    stampa("###       DIVERSE in %d casi su %d  ->  NON e' identica al bit."
           % (tot_A, len(TAGLIE) * PROVE))
    stampa("###   (C) np.sum(x) + np.sum(x) contro 2*np.sum(x):")
    stampa("###       DIVERSE in %d casi su %d" % (tot_C, len(TAGLIE) * PROVE))
    if tot_A and not tot_C:
        stampa("###")
        stampa("###   *** IL RILIEVO DEL GUARDIANO E' GIUSTO, E LA MIA RIGA ERA SBAGLIATA. ***")
        stampa("###   Avevo scritto che <<tutti e quattro i numeri coincidono>>: vale per i")
        stampa("###   TRE INTERI (_g_sm_nascite, _sm_tr, _sm_vis) e NON per il FLOAT _sm_lun,")
        stampa("###   che e' md * sum(LAM - v) sui troncati.")
        stampa("###   LA CAUSA E' L'ASSOCIATIVITA': np.sum su 2n elementi somma in un ordine")
        stampa("###   che non e' 2 * la somma su n. Gli interi non se ne accorgono.")
        stampa("###")
        stampa("###   LA FORMA CHE REGGE: _fab PER META' e sommata (fab_a + fab_b). A t = 0.5")
        stampa("###   le due meta' sono IDENTICHE, quindi e' s + s -- e s + s == 2*s e'")
        stampa("###   ESATTO, perche' il raddoppio e' uno scalamento per una potenza di due.")
        stampa("###")
        stampa("###   E IL DIFETTO CONTA NEL 6b: con t != 0.5 le due meta' sono DIVERSE, e")
        stampa("###   t*d puo' scendere SOTTO LAM anche con d >= 2 LAM (0.4*1.6 = 0.64 < 0.8).")
        stampa("###   Allora i troncamenti CI SONO, e _fab non e' piu' zero.")
    elif not tot_A:
        stampa("###   *** (A) NON DIVERGE MAI: il rilievo non si riproduce con questi dati,")
        stampa("###   e va capito prima di correggere il task history. ***")
    stampa("=" * 100)

    esito = {"strumento": hashlib.sha1(
        io.open(os.path.abspath(__file__), "rb").read()).hexdigest(),
        "numpy": np.__version__, "seme": SEME, "prove_per_taglia": PROVE,
        "righe": righe, "A_diverse_totale": tot_A, "C_diverse_totale": tot_C,
        "A_identica_al_bit": tot_A == 0, "C_identica_al_bit": tot_C == 0}
    io.open(os.path.join(FUORI, "_somma_meta.json"), "w", encoding="utf-8",
            newline=NL).write(json.dumps(esito, indent=1, ensure_ascii=False))
    io.open(os.path.join(FUORI, "_corsa.txt"), "w", encoding="utf-8",
            newline=NL).write(NL.join(out) + NL)
    print("  referto .. %s" % FUORI)


if __name__ == "__main__":
    principale()
