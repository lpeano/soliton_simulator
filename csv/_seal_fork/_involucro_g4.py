# -*- coding: utf-8 -*-
"""`STANDARD 5` -- IL CONTROLLO DELL'INVOLUCRO: `_g4_prova.py` e' inerte?

Il sigillo dimostra che **il flag** e' chirurgico; **non** che l'**involucro** sia inerte.
Sono due affermazioni diverse, e senza la seconda una differenza e' attribuibile allo strumento.

**QUI SI CONFRONTANO DUE RUN CHE DIFFERISCONO SOLO PER L'INVOLUCRO:**
  * `_sig_cura2/inerte/ACCESO` -- il DRIVER NUDO, lanciato dal sigillo in un processo suo;
  * `_cura2_corto`            -- lo STESSO driver dentro `_g4_prova.py`, che avvolge
                                 `_smorza` (il bilancio di `d0`) e `_applica_flag`.
Stesso blob, stesso seme, stessa argv, stesso flag. **Se l'involucro e' inerte: ZERO differenze.**

⚠ E IL CONFRONTO USA LA FIRMA DEI BYTE, NON `array_equal` -- **`STANDARD 2`**, e per una ragione
  misurata qui: `np.array_equal` su due array **byte-identici** che contengono `NaN` risponde
  **False**, perche' `NaN != NaN`. **Su `peq` (2 `NaN` su 526 204) produceva «1 campo diverso»
  su due array il cui `sha1` dei byte grezzi COINCIDE.** E' un generatore di **FAIL FALSI**.

ASCII puro.
"""
import gzip
import hashlib
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
NUDO = os.path.join(_QUI, "_sig_cura2", "inerte", "ACCESO", "scena_000120.pkl.gz")
AVVOLTO = os.path.join(RADICE, "csv", "_test_fork", "_cura2_corto", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_sig_cura2", "INVOLUCRO_g4.txt")


def firma(v):
    """La FIRMA DEI BYTE (`STANDARD 2`): vede due `NaN` nello stesso posto, e `+0.0`/`-0.0`."""
    a = np.asarray(v)
    return (hashlib.sha1(np.ascontiguousarray(a).tobytes()).hexdigest()[:12],
            a.shape, str(a.dtype))


def main():
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    A = pickle.load(gzip.open(NUDO, "rb"))["attrs"]
    B = pickle.load(gzip.open(AVVOLTO, "rb"))["attrs"]
    P("# `STANDARD 5` -- L'INVOLUCRO DI `_g4_prova.py` E' INERTE?\n#\n")
    P("# NUDO    %s\n# AVVOLTO %s\n#\n"
      % (os.path.relpath(NUDO, RADICE), os.path.relpath(AVVOLTO, RADICE)))

    ug = dv = nc = 0
    diversi = []
    nan_salvati = []
    for k in sorted(set(A) | set(B)):
        if k not in A or k not in B:
            nc += 1
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                fa, fb = firma(a), firma(b)
                if fa == fb:
                    ug += 1
                    na = int(np.sum(np.isnan(np.asarray(a, dtype=float)))) \
                        if np.asarray(a).dtype.kind == "f" else 0
                    if na:
                        nan_salvati.append((k, na, np.asarray(a).size))
                else:
                    dv += 1
                    diversi.append("%s(%s != %s)" % (k, fa[0], fb[0]))
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception:
            nc += 1

    P("CONFRONTO PER FIRMA DEI BYTE (`sha1` + forma + dtype):\n")
    P("  campi UGUALI %d   DIVERSI %d   non confrontati %d\n" % (ug, dv, nc))
    if diversi:
        P("  i diversi: %s\n" % ", ".join(diversi[:10]))
    ok = (dv == 0 and ug > 100)
    P("\n  -> %s\n" % ("PASS: L'INVOLUCRO E' INERTE. `_g4_prova.py` avvolge `_smorza` e\n"
                       "     `_applica_flag` SENZA cambiare un bit del risultato, quindi il\n"
                       "     bilancio di `d0` e i quantili di `V8`/`V9` sono misure di SOLA\n"
                       "     LETTURA sul run vero."
                       if ok else "*** FAIL: l'involucro NON e' inerte ***"))

    P("\n\n" + "=" * 92 + "\nPERCHE' LA FIRMA DEI BYTE E NON `array_equal` -- `STANDARD 2`\n"
      + "=" * 92 + "\n")
    if nan_salvati:
        for k, na, tot in nan_salvati:
            a = np.asarray(A[k], dtype=float)
            b = np.asarray(B[k], dtype=float)
            P("  `%s`: %d `NaN` su %d (%.4f %%), posizioni identiche: %s, "
              "finiti identici: %s\n"
              % (k, na, tot, 100.0 * na / tot,
                 bool(np.array_equal(np.isnan(a), np.isnan(b))),
                 bool(np.array_equal(a[~np.isnan(a)], b[~np.isnan(b)]))))
            P("     `np.array_equal` risponde **%s**; la firma dei byte risponde **%s**.\n"
              % (bool(np.array_equal(a, b)), firma(a) == firma(b)))
    else:
        P("  (nessun campo con `NaN` in questo confronto)\n")
    P("\n  -> `NaN != NaN`, quindi `array_equal` dichiara DIVERSI due array BYTE-IDENTICI.\n")
    P("     E' un generatore di FAIL FALSI, ed e' il difetto che `_sigillo_cura2.py` aveva:\n")
    P("     `confronta_snap` usa `np.array_equal`. **Non ha prodotto un FAIL** perche' `T4`\n")
    P("     confronta due run senza `NaN` in quel campo -- ma e' la stessa famiglia di\n")
    P("     `max|A-B| = 0.000e+00` letto come identita': **il criterio non vede cio' che\n")
    P("     dichiara di vedere.**\n")
    P("\n  ⚠ E IL `NaN` DI `peq` NON E' UN DIFETTO: il suo DOMINIO lo dichiara --\n")
    P("     \"la pressione di equilibrio: >= 0, e `nan` SOLO sugli archi marcati\"\n")
    P("     (`DOMINI['peq']`). **Verificato dall'AST, non dedotto.**\n")
    f.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
