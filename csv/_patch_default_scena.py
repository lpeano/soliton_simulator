# -*- coding: utf-8 -*-
"""**IL DEFAULT DEL DRIVER DIVENTA LA SCENA `(ii)`(a)** *(decisione di Luca, 2026-09-26)*.

> **«`N-MASSE` e' morta con `SEMINA_LAM`; tenerla come default e' un run che si ferma.»**

| | che cosa cambia | da | a |
|--:|---|---|---|
| **1** | la **scena** di default | `N-MASSE` | **`MASSE-COERENTI`** |
| **2** | il **`--sep`** di default | `4.0` *(la scena `(b)`)* | **`6.1158`** *(la scena `(a)`, «stesso raggio»)* |

**NON E' BYTE-INERTE, ED E' IL PUNTO.** Chi lancia il driver nudo otteneva **un `SystemExit`**
*(`M0c`: `N-MASSE` con `SEMINA_LAM` rifiuta)*; ora ottiene **la scena del run base**. E' la stessa
forma della decisione del 2026-09-24 su `SEP` *(`8` -> `4.0`)*: **il default segue cio' che si
lancia davvero**, e un default che non gira non e' un default.

**I due valori vengono dal registro della fisica**, non da me: `doc/REGISTRO_FISICA.md` misura
`(a)` `--sep 6.1158` -> `r_regione 4.096438`, `raggio_vuoto 12.612238`, `n 12 802`, `471 564`
archi, `QUOTA 0.0966`; `(b)` `--sep 4.0` -> `4 252` nodi, `148 237` archi, `QUOTA 0.0484`.
**`(b)` resta raggiungibile, esplicito: `--sep=4.0`.**

**Ogni sostituzione e' asserita per se'** (`P1-quater`), e **nessun escape**: `chr()` (`L-PATCH`).

    python csv/_patch_default_scena.py --prova
    python csv/_patch_default_scena.py

ASCII puro.
"""
import io
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# ESENTE-H-P5: non importa il simulatore e non lo fa girare. Sostituisce due default nel driver.

NL = chr(10)
_QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(_QUI, ".."))
DRV = "csv/_test_fork/_scena_video.py"

V1 = 'SCENA = "N-MASSE"'
N1 = NL.join([
    '# ⚠ IL DEFAULT E\' LA SCENA `(ii)` DAL 2026-09-26 (decisione di Luca), E NON E\' BYTE-INERTE.',
    '#   `N-MASSE` con `SEMINA_LAM` **RIFIUTA DI PARTIRE** (`_massa`, e la misura 0 lo ha',
    '#   misurato: `M0c`): tenerla come default significava **un default che e\' un run che si',
    '#   ferma**. Chi lancia nudo ora ottiene **la scena del RUN BASE**.',
    '#   `N-MASSE` resta raggiungibile, esplicita: `--scena=N-MASSE` -- e li\' rifiutera\',',
    '#   che e\' il presidio delle scene di epoca pre-`A13` e non un difetto.',
    'SCENA = "MASSE-COERENTI"'])

V2 = 'SEP = "4.0"             # [DECISIONE DI LUCA, 2026-09-24] IL DEFAULT SEGUE LA CAMPAGNA.'
N2 = NL.join([
    'SEP = "6.1158"          # [DECISIONE DI LUCA, 2026-09-26] IL DEFAULT E\' LA SCENA `(ii)`(a).',
    '                        # `6.1158` e\' la scena **`(a)` «STESSO RAGGIO»**; `4.0` e\' la **`(b)`**,',
    '                        # e resta raggiungibile ESPLICITA con `--sep=4.0`.',
    '                        # I numeri vengono da `doc/REGISTRO_FISICA.md`, non da me:',
    '                        #   `(a)` sep 6.1158 -> r_regione 4.096438, raggio_vuoto 12.612238,',
    '                        #         n 12 802, archi 471 564, QUOTA 0.0966',
    '                        #   `(b)` sep 4.0    -> n 4 252, archi 148 237, QUOTA 0.0484',
    '                        # **NON E\' BYTE-INERTE, ed e\' il punto**: il default segue cio\' che',
    '                        # si lancia davvero. Stessa forma della decisione qui sotto.',
    '                        # [DECISIONE DI LUCA, 2026-09-24] IL DEFAULT SEGUE LA CAMPAGNA.'])

LAVORO = [(DRV, [(V1, N1), (V2, N2)])]


if __name__ == "__main__":
    scrivi = "--prova" not in sys.argv[1:]
    print("=" * 92)
    print("IL DEFAULT DEL DRIVER -> SCENA (ii)(a)%s"
          % ("" if scrivi else "   (PROVA: non scrivo)"))
    print("=" * 92)
    for rel, coppie in LAVORO:
        p = os.path.join(RADICE, rel)
        t = io.open(p, encoding="utf-8", newline="").read()
        fatte = 0
        for vecchio, nuovo in coppie:
            if nuovo.split(NL)[-1] in t and vecchio not in t:
                print("  %-34s gia' applicata" % rel)
                continue
            n = t.count(vecchio)
            if n != 1:
                raise SystemExit("%s: ancora attesa 1 volta, trovata %d: %s"
                                 % (rel, n, vecchio[:70]))
            t = t.replace(vecchio, nuovo)
            fatte += 1
        if scrivi and fatte:
            io.open(p, "w", encoding="utf-8", newline=NL).write(t)
        print("  %-34s %d sostituzioni asserite" % (rel, fatte))
    sys.exit(0)
