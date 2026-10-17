# -*- coding: utf-8 -*-
r"""**CHI STA NELLA LISTA DELLA FISICA E LA SUITE NON GIRA.**

> ### ⛔⛔ **PERCHE' ESISTE** *(`2026-10-17`)*: il divieto del vuoto nullo aveva rotto
> ### **tre strumenti** e ### **la suite diceva `59` su `59`**, perche' nessuno dei tre
> era in `collauda.py`. ### **Un collaudo che la suite non gira non e' un collaudo:**
> e' ### **un file che qualcuno dovrebbe ricordarsi di lanciare**
> *(`[[DIFETTO-TRE-MISURE-FUORI-DALLA-SUITE]]`)*.

## ⛔⛔ E IL NUMERO GREZZO E' UN NUMERO ROTTO

### **La prima misura diceva `63` file fuori dalla suite**, e ### **era inutile:** dentro
c'erano ### **le LIBRERIE** *(`motore.py`, `tick.py`, `flussi_parziali.py`…)*, che
### **non hanno un `main` da girare** e si esercitano ### **ATTRAVERSO i collaudi.**
### ✅ **Quindi il censimento ha TRE livelli, e ognuno risponde a una domanda diversa:**

| | il livello | la domanda |
|---|---|---|
| `1` | ### **ESEGUIBILE** *(ha `if __name__ ==`)* | si puo' girare da solo? |
| `2` | ### **GIUDICA** *(ha un verdetto: `OK[0] == OK[1]`, `return 0 if`, `sys.exit(1)`)* | dice ### **si' o no**, o stampa soltanto? |
| `3` | ### **NELLA SUITE** *(il suo comando sta in `collauda.py`)* | qualcuno lo gira ### **senza ricordarselo**? |

### ⚠⚠ **E IL LIVELLO `2` HA UN FALSO POSITIVO MISURATO:** `primo_ordine/leggi/schema.py`
risulta *«giudica»* perche' contiene `sys.exit(1)` — ### **ma e' UN CARTELLO**, e quell'
uscita `1` e' ### **voluta**: dice *«il collaudo non sta piu' qui, gira
`_collauda_schema.py`»*. ### **Un'euristica sul testo non distingue un verdetto da un
cartello**, e lo scrivo invece di lasciare il numero gonfio.

## ⚠ CHE COSA QUESTO FILE NON DICE

### ⛔ **NON dice che un rosso e' un difetto.** Un sigillo si rigira ### **AL SUO
COMMIT**, e ### **un sigillo vecchio che non passa sul blob di oggi NON e' un difetto**
*(regola di Luca)*. ### **Quello che un rosso vuol dire va letto UNO PER UNO**, e con
`--gira` si vede ### **l'esito e il tempo**, non il merito.

Gira con:  python csv/_censimento_suite.py            (il censimento, e basta)
           python csv/_censimento_suite.py --gira     (gira anche i GIUDICI fuori suite)
"""
import io
import os
import re
import subprocess
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)
RADICE = os.path.dirname(_QUI)

# ### ⛔ **I SEGNI DEL VERDETTO, dichiarati**: un file che ne ha almeno uno
# ### ### **dice si' o no**; gli altri ### **stampano.**
SEGNI_VERDETTO = ("OK[0] == OK[1]", "return 0 if", "sys.exit(1)", "ESITO", "esito(")
# ### ⚠ **IL CARTELLO, dichiarato per nome**: `sys.exit(1)` la' dentro e' ### **voluto**,
# ### e non e' un verdetto. ### **Una riga, non un'euristica in piu'.**
CARTELLI = ("primo_ordine/leggi/schema.py",)
# ### ⛔ **L'ERA `1` NON STA NELLA SUITE DELL'ERA `2`, e non e' una dimenticanza.**
FUORI_ERA2 = ("soliton_simulator.py",)
# ### ⚠ **IL TETTO DI UNA CORSA CON `--gira`:** oltre, si scrive ### **<<oltre>>** e si
# ### passa al prossimo. ### **Non e' un giudizio: e' un tempo.**
TETTO_S = 180


def comandi_della_suite():
    """### I `.py` che ### **`collauda.py` fa girare**, dal suo testo."""
    v = io.open(os.path.join(RADICE, "primo_ordine", "collauda.py"),
                encoding="utf-8").read()
    fuori = set()
    for c in re.findall(r'"((?:primo_ordine|csv)/[A-Za-z0-9_./-]+\.py[^"]*)"', v):
        fuori.add(c.split()[0])
    return fuori


def censisci():
    """### `(eseguibili, librerie, giudici_fuori)` ### **dalla LISTA della fisica.**"""
    import _file_fisica as FF
    girati = comandi_della_suite()
    eseguibili, librerie, giudici_fuori = [], [], []
    for f in FF.FILE_FISICA:
        if not f.endswith(".py"):
            continue
        p = os.path.join(RADICE, f)
        if not os.path.exists(p):
            continue
        t = io.open(p, encoding="utf-8").read()
        if "if __name__ ==" not in t:
            librerie.append(f)
            continue
        eseguibili.append(f)
        if f in girati or f in CARTELLI or f in FUORI_ERA2:
            continue
        if any(s in t for s in SEGNI_VERDETTO):
            giudici_fuori.append(f)
    return eseguibili, librerie, giudici_fuori


def main(argv):
    import _presidio
    _presidio.avvia(__file__)
    ese, lib, giu = censisci()
    girati = comandi_della_suite()
    print("=" * 100)
    print("CHI STA NELLA LISTA DELLA FISICA E LA SUITE NON GIRA")
    print("=" * 100)
    print("  la LISTA della fisica:            %3d file `.py`" % (len(ese) + len(lib)))
    print("    ESEGUIBILI (hanno un `main`):   %3d" % len(ese))
    print("    LIBRERIE (nessun `main`):       %3d   ### si girano ATTRAVERSO i collaudi"
          % len(lib))
    print("  i comandi della suite:            %3d" % len(girati))
    print("  ### GIUDICI fuori dalla suite:    %3d   ### tolti %d cartelli e %d dell-era 1"
          % (len(giu), len(CARTELLI), len(FUORI_ERA2)))
    print("-" * 100)
    for f in sorted(giu):
        print("     %s" % f)
    print("-" * 100)
    print("  ### ⚠ E UN ROSSO QUI NON E' UN DIFETTO: un sigillo si rigira AL SUO")
    print("  ###   COMMIT, e uno vecchio che non passa sul blob di oggi NON lo e'.")
    sys.stdout.flush()
    if "--gira" not in argv:
        print("  ### \U0001F4CC `--gira` li fa girare, col loro esito e il loro tempo.")
        print("=" * 100)
        return 0
    print("-" * 100)
    print("  %-42s %7s %8s" % ("file", "codice", "secondi"))
    import time
    for f in sorted(giu):
        t = time.time()
        try:
            r = subprocess.run([sys.executable, os.path.join(RADICE, f)],
                               capture_output=True, timeout=TETTO_S)
            c = str(r.returncode)
        except subprocess.TimeoutExpired:
            c = "oltre"
        print("  %-42s %7s %8.1f" % (f, c, time.time() - t))
        sys.stdout.flush()
    print("=" * 100)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
