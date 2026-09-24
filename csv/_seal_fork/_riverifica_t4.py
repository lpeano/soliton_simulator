# -*- coding: utf-8 -*-
"""RIVERIFICA DI `T4` CON LA FIRMA DEI BYTE, e il conto dei NON CONFRONTATI.

> **La frase che ho scritto nel commit `03f6567` e' FALSA:** *«questa modifica puo' solo
> SPOSTARE campi da "diversi" a "uguali", mai il contrario»*.
> **LA SMENTISCE IL MIO STESSO COLLAUDO `K8`:** `+0.0` contro `-0.0` -> `array_equal` dice
> **UGUALE**, la firma dei byte dice **DIVERSO**.
> ### **Quindi `T4` -- che e' un test di IDENTITA' -- poteva essere un FALSO `PASS`.**
> *(Rilievo di Luca, 2026-09-24.)*

**NESSUN RUN NUOVO:** si rileggono gli snapshot **gia' scritti** dai due bracci.

E si fa la seconda cosa che mancava: **il conto dei NON CONFRONTATI**, classificati secondo lo
`STANDARD 3` -- *assenza strutturale* (un campo che in un blob **non esiste**) contro *dato
mancante* (un campo che c'e' e non si e' potuto leggere). **Due `None` non sono un'identita'.**

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
RIF = os.path.join(RADICE, "csv", "_test_fork", "_cura1_corto", "scena_000120.pkl.gz")
SPENTO = os.path.join(_QUI, "_sig_cura2", "inerte", "SPENTO", "scena_000120.pkl.gz")
ACCESO = os.path.join(_QUI, "_sig_cura2", "inerte", "ACCESO", "scena_000120.pkl.gz")
DEST = os.path.join(_QUI, "_sig_cura2", "RIVERIFICA_T4.txt")

# i contatori che la CURA 2 ha introdotto: la loro assenza nel riferimento e' STRUTTURALE,
# non un dato perso -- il blob del riferimento (`dd82794a`) non li aveva.
NUOVI_DELLA_CURA = ("_tum_",)


def firma(v):
    a = np.ascontiguousarray(np.asarray(v))
    return (hashlib.sha1(a.tobytes()).hexdigest()[:16], a.shape, str(a.dtype))


def confronta(A, B, P, eti_a, eti_b):
    ug = dv = 0
    diversi, solo_a, solo_b, illeggibili = [], [], [], []
    for k in sorted(set(A) | set(B)):
        if k not in B:
            solo_a.append(k)
            continue
        if k not in A:
            solo_b.append(k)
            continue
        a, b = A[k], B[k]
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                fa, fb = firma(a), firma(b)
                if fa == fb:
                    ug += 1
                else:
                    dv += 1
                    diversi.append("%s(%s %s %s != %s %s %s)"
                                   % (k, fa[0][:8], fa[1], fa[2], fb[0][:8], fb[1], fb[2]))
            elif a == b:
                ug += 1
            else:
                dv += 1
                diversi.append("%s(%r != %r)" % (k, a, b))
        except Exception as ex:
            illeggibili.append("%s(%s)" % (k, type(ex).__name__))
    P("  UGUALI %d   DIVERSI %d   solo in %s: %d   solo in %s: %d   illeggibili: %d\n"
      % (ug, dv, eti_a, len(solo_a), eti_b, len(solo_b), len(illeggibili)))
    if diversi:
        P("  i DIVERSI: %s\n" % ", ".join(diversi[:12]))
    return ug, dv, solo_a, solo_b, illeggibili


def classifica(nomi, P, dove):
    """`STANDARD 3`: assenza STRUTTURALE o dato MANCANTE? Non si dice «non confrontato»."""
    if not nomi:
        P("    (nessuno)\n")
        return
    for k in nomi:
        strutt = any(k.startswith(p) or p in k for p in NUOVI_DELLA_CURA)
        P("    %-28s %s\n"
          % (k, ("ASSENZA STRUTTURALE -- contatore introdotto DOPO quel blob, %s non "
                 "poteva averlo" % dove) if strutt
             else "⚠ **DA SPIEGARE** -- non e' un contatore della cura"))


def main():
    f = io.open(DEST, "w", encoding="utf-8", newline="\n")

    def P(s):
        sys.stdout.write(s)
        f.write(s)

    P("# RIVERIFICA DI `T4` CON LA FIRMA DEI BYTE -- nessun run nuovo\n#\n")
    P("# La frase del commit `03f6567` era FALSA: la correzione NON puo' solo spostare campi\n")
    P("# da diversi a uguali. `K8` lo dimostra: `+0.0` contro `-0.0` -> `array_equal` UGUALE,\n")
    P("# firma DIVERSA. Quindi `T4` poteva essere un FALSO PASS. (Rilievo di Luca.)\n#\n")

    R = pickle.load(gzip.open(RIF, "rb"))["attrs"]
    S = pickle.load(gzip.open(SPENTO, "rb"))["attrs"]
    A = pickle.load(gzip.open(ACCESO, "rb"))["attrs"]

    P("=" * 96 + "\n1. `T4` RIFATTO -- riferimento `_cura1_corto` contro braccio SPENTO\n"
      + "=" * 96 + "\n")
    ug, dv, sa, sb, ill = confronta(R, S, P, "RIF", "SPENTO")
    ok = (dv == 0 and ug > 100)
    P("\n  -> `T4` con la FIRMA DEI BYTE: %s\n"
      % ("**PASS, e ora l'identita' e' quella vera**" if ok else "*** FAIL ***"))
    P("     `array_equal` diceva `206` uguali e `0` diversi. La firma dice `%d` e `%d`.\n"
      % (ug, dv))
    P("     %s\n" % ("**Le due strade CONCORDANO: il PASS non era falso.**" if ok else
                     "**LE DUE STRADE NON CONCORDANO: il PASS ERA FALSO.**"))

    P("\n" + "=" * 96 + "\n2. I CAMPI NON CONFRONTATI -- `STANDARD 3`\n" + "=" * 96 + "\n")
    P("  *Un sito che cambia lunghezza non ha un delta: si registra come tale, non come `None`.*\n")
    P("  E qui la domanda e' piu' stretta: **assenza STRUTTURALE o dato MANCANTE?**\n\n")
    P("  -- braccio SPENTO contro il riferimento --\n")
    P("  presenti solo nel RIFERIMENTO (%d):\n" % len(sa))
    classifica(sa, P, "il riferimento")
    P("  presenti solo nello SPENTO (%d):\n" % len(sb))
    classifica(sb, P, "il riferimento")
    P("  illeggibili (%d): %s\n" % (len(ill), ", ".join(ill) or "nessuno"))

    P("\n  -- braccio ACCESO contro il riferimento --\n")
    ug2, dv2, sa2, sb2, ill2 = confronta(R, A, P, "RIF", "ACCESO")
    P("  presenti solo nel RIFERIMENTO (%d):\n" % len(sa2))
    classifica(sa2, P, "il riferimento")
    P("  presenti solo nell'ACCESO (%d):\n" % len(sb2))
    classifica(sb2, P, "il riferimento")
    P("  illeggibili (%d): %s\n" % (len(ill2), ", ".join(ill2) or "nessuno"))

    P("\n  ⚠ E I DUE BRACCI NON HANNO LO STESSO NUMERO DI NON CONFRONTATI, ed e' atteso:\n")
    P("     i contatori `_tum_r_*`, `_tum_cs_*`, `_tum_t_*` e `_tum_eulero_*` **esistono solo\n")
    P("     a flag ACCESO**, perche' i metodi che li scrivono girano solo li'. **E' assenza\n")
    P("     STRUTTURALE, non un dato perso**, e per questo il braccio acceso ne ha di piu'.\n")

    P("\n" + "=" * 96 + "\n")
    P("!! COSA RESTA VERO DEL VECCHIO `T4`: il verdetto. COSA NON ERA GIUSTIFICATO: la\n")
    P("   FIDUCIA nel verdetto. Un test di IDENTITA' con un criterio che non vede `+0.0`\n")
    P("   contro `-0.0` puo' passare per la ragione sbagliata, e nessuno lo saprebbe.\n")
    f.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
