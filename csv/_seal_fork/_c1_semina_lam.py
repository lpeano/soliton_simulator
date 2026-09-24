# -*- coding: utf-8 -*-
"""`C1` -- **`SEMINA_LAM` SPENTA E' BYTE-IDENTICA?** Un processo per braccio, firma dei byte.

**⚠ E LA RISPOSTA NON PUÒ ESSERE «si'» IN ASSOLUTO, e va detto PRIMA di misurare:** nello stesso
lavoro **`_nasce` ha perso il suo GATE** *(`D38`)*. Prima girava solo con
`SCALA_MIN or SCALA_MIN_PASSO`; ora **sempre**.

  * **con la configurazione del DRIVER** `SCALA_MIN_PASSO` è **acceso**, quindi `_nasce`
    **girava già**: lì la byte-identità deve valere, ed è ciò che questo test misura;
  * **con `--scala-min-passo=off`** i due blob **DEVONO differire**, e **non è un difetto: è la
    cura di `D38`.** Anche questo si misura, come **controllo positivo**: se non differisse,
    la cura non avrebbe fatto niente.

**Riferimento: `csv/_test_fork/_cura2_corto/scena_000120.pkl.gz`** — l'ultimo giro corto, blob
`49fc54d2`. **`SEMINA_LAM` non esisteva: è il «prima» giusto.**

Argv **letta dal driver** *(`csv/_testa_driver.py`)*. ASCII puro.
"""
import gzip
import hashlib
import io
import os
import pickle
import subprocess
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_QUI, "..")))
import _presidio

_presidio.avvia(__file__)

RADICE = os.path.abspath(os.path.join(_QUI, "..", ".."))
RIF = os.path.join(RADICE, "csv", "_test_fork", "_cura2_corto", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_c1_semina")
REF = os.path.join(DEST, "REFERTO.txt")


def firma(v):
    a = np.ascontiguousarray(np.asarray(v))
    return (hashlib.sha1(a.tobytes()).hexdigest()[:16], a.shape, str(a.dtype))


def confronta(A, B, P):
    ug = dv = 0
    diversi, solo = [], 0
    for k in sorted(set(A) | set(B)):
        if k not in A or k not in B:
            solo += 1
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                fa, fb = firma(a), firma(b)
                if fa == fb:
                    ug += 1
                else:
                    dv += 1
                    diversi.append("%s(%s %s != %s %s)" % (k, fa[0][:8], fa[1], fb[0][:8], fb[1]))
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception:
            solo += 1
    P("  UGUALI %d   DIVERSI %d   presenti in uno solo %d\n" % (ug, dv, solo))
    if diversi:
        P("  i DIVERSI: %s\n" % ", ".join(diversi[:10]))
    return ug, dv


def braccio(nome, extra, P):
    d = os.path.join(DEST, nome)
    try:
        os.makedirs(d)
    except OSError:
        pass
    for f in os.listdir(d):
        if f.endswith(".pkl.gz"):
            os.remove(os.path.join(d, f))
    src = ("import os, sys\n"
           "sys.path.insert(0, os.path.join(%r, 'csv'))\n"
           "import runpy, _testa_driver as T\n"
           "sys.argv = ['_scena_video.py', '20', %r] + %r\n"
           "runpy.run_path(T.DRIVER, run_name='__main__')\n"
           % (RADICE, d, list(extra)))
    import time
    t0 = time.time()
    r = subprocess.run([sys.executable, "-c", src], cwd=RADICE, capture_output=True,
                       text=True, encoding="utf-8", errors="replace")
    P("\n  [%s] %.1f s   rc=%d   extra=%s\n" % (nome, time.time() - t0, r.returncode,
                                                list(extra) or "(nessuno)"))
    p = os.path.join(d, "scena_000120.pkl.gz")
    if r.returncode != 0 or not os.path.exists(p):
        P("  *** braccio MORTO ***\n%s\n" % ((r.stdout or "") + (r.stderr or ""))[-2000:])
        return None
    return pickle.load(gzip.open(p, "rb"))["attrs"]


def main():
    try:
        os.makedirs(DEST)
    except OSError:
        pass
    f = io.open(REF, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    P("# `C1` -- `SEMINA_LAM` spenta e' byte-identica?\n#\n")
    P("# Un processo per braccio (`STANDARD 1`), firma dei byte (`STANDARD 2`).\n")
    P("# Riferimento: `_cura2_corto/scena_000120.pkl.gz` (blob 49fc54d2, prima di SEMINA_LAM).\n#\n")
    P("!! LA RISPOSTA NON PUO' ESSERE `si'` IN ASSOLUTO, e lo dico PRIMA di misurare:\n")
    P("   nello stesso lavoro `_nasce` HA PERSO IL GATE (`D38`). Con la configurazione del\n")
    P("   DRIVER `SCALA_MIN_PASSO` e' ACCESO, quindi `_nasce` girava GIA': li' la\n")
    P("   byte-identita' deve valere. Con `--scala-min-passo=off` i due blob DEVONO\n")
    P("   differire, e NON e' un difetto: e' la cura.\n\n")

    RIFA = pickle.load(gzip.open(RIF, "rb"))["attrs"]
    esiti = []

    A = braccio("driver", [], P)
    if A is not None:
        ug, dv = confronta(RIFA, A, P)
        ok = (dv == 0 and ug > 100)
        esiti.append(ok)
        P("  `C1` %s BYTE-IDENTICO con la configurazione del driver\n"
          % ("PASS" if ok else "*** FAIL ***"))
        P("     -> `SEMINA_LAM` spenta non cambia un bit, E `_nasce` senza gate nemmeno:\n")
        P("        girava gia', perche' `SCALA_MIN_PASSO` e' acceso.\n")

    B = braccio("senza_scala_min_passo", ["--scala-min-passo=off"], P)
    if B is not None:
        ug2, dv2 = confronta(RIFA, B, P)
        ok2 = (dv2 > 0)
        esiti.append(ok2)
        P("  CONTROLLO POSITIVO %s: con `--scala-min-passo=off` i blob DEVONO differire\n"
          % ("PASS" if ok2 else "*** FAIL ***"))
        P("     -> e' la cura di `D38`: `_nasce` ora gira anche li', dove prima NO.\n")
        P("     -> se NON differissero, la cura non avrebbe fatto niente.\n")

    n = sum(1 for x in esiti if x)
    P("\n" + "=" * 96 + "\nESITO: %d/%d\n" % (n, len(esiti)) + "=" * 96 + "\n")
    P("*** %s ***\n" % ("`C1` PASSATO." if n == len(esiti) and len(esiti) == 2
                        else "`C1` FALLITO: reperto, commit, STOP."))
    f.close()
    return 0 if (n == len(esiti) and len(esiti) == 2) else 1


if __name__ == "__main__":
    sys.exit(main())
