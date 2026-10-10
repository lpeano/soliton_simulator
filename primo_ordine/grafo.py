# -*- coding: utf-8 -*-
"""PUNTO `4` DELLA TERZA PARTE — **IL GRAFO VALIDO A OGNI PASSO, e una violazione FERMA.**

> ### ⛔ **Il mandato, alla lettera:** *«**IL GRAFO VALIDO A OGNI PASSO:** archi
> simmetrici, niente auto-archi, niente doppioni, indici coerenti; violazione →
> **FERMO**»*.

### ⭐ **PERCHE' <<A OGNI PASSO>> E NON <<ALLA COSTRUZIONE>>.** Oggi il grafo lo costruisce
`driver.py::grafo` da una scena a vocabolario chiuso, e ### **alla costruzione è giusto per
costruzione.** ### ⛔ **Ma nell'era `2` la MITOSI aggiungerà nodi e archi mentre il sistema
gira** *(è la direzione dichiarata su `D9`)*, e ### **in quel momento <<giusto alla
costruzione>> non vuol dire più niente.** ### ✅ **Quindi il controllo nasce ADESSO, quando
non ha ancora materia per fallire, e sarà già lì quando l'avrà.**

| | che cosa impedisce | perché **FERMA** invece di correggere |
|---|---|---|
| `1` | un ### **auto-arco** *(`i == j`)* | un termine d'arco su `i == j` ### **non è un accoppiamento: è un termine di nodo travestito** — e correggerlo togliendolo ### **cambierebbe la fisica in silenzio** |
| `2` | un ### **doppione** *(lo stesso arco due volte)* | l'energia di quell'arco ### **conterebbe DUE VOLTE**, e il risultato sarebbe ### **sbagliato senza sembrarlo** |
| `3` | un ### **indice fuori intervallo** | è un errore di programma, e ### **`numpy` lo tradurrebbe in un `IndexError` lontano dal punto dove è nato** |
| `4` | le ### **due liste di lunghezza diversa** | `ii` e `jj` sono ### **le due metà di una lista di coppie**: se hanno lunghezza diversa, ### **non esiste la lista di coppie** |
| `5` | ### **la stessa coppia in entrambi i versi** *(`(i,j)` e `(j,i)`)* | il grafo è ### **non orientato**, e un arco scritto nei due versi è ### **un doppione che non sembra un doppione** |

### ⚠ **E <<ARCHI SIMMETRICI>> HA UN SECONDO SIGNIFICATO, che un controllo per passo NON
può verificare:** che ### **la FISICA tratti `(i,j)` e `(j,i)` allo stesso modo.**
### ✅ **Quello si misura UNA VOLTA, nel collaudo: si scambiano `ii` e `jj` su TUTTI gli
archi e si pretende che il passo dia lo STESSO STATO AL BIT.** ### ⛔ **È un controllo
più forte del primo, e più costoso: per questo sta nel collaudo e non nel passo.**

### 📌 **E `PRESIDIO = "P-GRAFO"` E' UNA DICHIARAZIONE, non un commento:** il controllo
dei presidi nell'indice ### **legge quel nome**, e una voce `PRESIDIO` che
### **nessun codice dichiara** è ### **una tenda** *(`A9`)*. ### ⚠ **E la frase sta nel
DOCSTRING e non in un commento accanto alla riga, perché `P-RIF` me l'ha rifiutata:
un riferimento che una macchina deve seguire NON PUO' VIVERE NELLA PROSA DI UN
COMMENTO** — o è un `@rif(...)`, o sta nella documentazione.

### 📌 **IL COSTO E' MISURATO, non stimato** *(`python primo_ordine/grafo.py`)*: il punto
`6` del mandato dà un budget, e ### **un presidio che decuplicasse il costo del passo si
spegnerebbe il primo giorno** — che è il difetto di `A9`.
"""
import os
import sys

import numpy as np

_QUI = os.path.dirname(os.path.abspath(__file__))
if _QUI not in sys.path:
    sys.path.insert(0, _QUI)

PRESIDIO = "P-GRAFO"


def errori(ii, jj, n, dove):
    """### Gli errori del grafo, o `[]`. ### **Non solleva: li RESTITUISCE.**

    ### ⛔ **Separare <<trovare>> da <<fermare>> serve al collaudo:** il caso che
    ### **DEVE fallire** si costruisce ### **chiamando questa**, senza dover
    ### **catturare un-eccezione** -- e un braccio che cattura un-eccezione
    ### **non sa DI QUALE eccezione si tratta.**
    """
    err = []
    ii = np.asarray(ii)
    jj = np.asarray(jj)
    if ii.shape != jj.shape:
        err.append("`GRAFO` %s: `ii` ha forma %s e `jj` %s. ### Sono LE DUE META- di una "
                   "lista di coppie: se hanno forma diversa, la lista di coppie NON "
                   "ESISTE" % (dove, ii.shape, jj.shape))
        return err
    if ii.size == 0:
        return err
    fuori = np.flatnonzero((ii < 0) | (ii >= n) | (jj < 0) | (jj >= n))
    if fuori.size:
        err.append("`GRAFO` %s: %d indici FUORI da [0, %d): archi %s. ### E- un errore di "
                   "programma, e `numpy` lo tradurrebbe in un `IndexError` LONTANO dal "
                   "punto dove e- nato" % (dove, fuori.size, n, fuori[:4].tolist()))
    auto = np.flatnonzero(ii == jj)
    if auto.size:
        err.append("`GRAFO` %s: %d AUTO-ARCHI (archi %s). ### Un termine d-arco su `i == "
                   "j` non e- un accoppiamento: e- un termine di nodo TRAVESTITO -- e "
                   "togliere l-arco cambierebbe la fisica IN SILENZIO"
                   % (dove, auto.size, auto[:4].tolist()))
    # ### ⛔ **LA CHIAVE CANONICA `(min, max)`**: la stessa che usa `passo.py::strati`,
    # ### e ### **non introduce una direzione.**
    a = np.minimum(ii, jj)
    b = np.maximum(ii, jj)
    chiavi = a.astype(np.int64) * np.int64(n) + b.astype(np.int64)
    _u, conte = np.unique(chiavi, return_counts=True)
    if int(conte.max()) > 1:
        quanti = int((conte > 1).sum())
        err.append("`GRAFO` %s: %d archi DOPPI (la coppia compare piu- di una volta, "
                   "anche se nei due versi). ### L-energia di quell-arco conterebbe DUE "
                   "VOLTE, e il risultato sarebbe SBAGLIATO SENZA SEMBRARLO"
                   % (dove, quanti))
    return err


def controlla(ii, jj, n, dove):
    """### **FERMA** se il grafo non e- valido *(punto `4`: violazione → FERMO)*.

    ### ⚠ **Non tronca e non corregge:** correggere ### **cambierebbe la fisica in
    silenzio**, e un ramo silenzioso ### **non e- un ramo** *(`A8`)*.
    """
    err = errori(ii, jj, n, dove)
    assert not err, "### IL GRAFO NON E- VALIDO:" + "".join(
        chr(10) + "  " + x for x in err)


def costo(n=9, archi=None, giri=2000):
    """### Il costo del controllo, ### **MISURATO** -- per il budget del punto `6`."""
    import time
    if archi is None:
        ii = np.arange(n - 1, dtype=int)
        jj = np.arange(1, n, dtype=int)
    else:
        ii, jj = archi
    t0 = time.perf_counter()
    for _ in range(giri):
        controlla(ii, jj, n, "misura")
    t1 = time.perf_counter()
    return (t1 - t0) / giri


def main(argv):
    """### I NUMERI del controllo. ### **Il collaudo sta in `_collauda_grafo.py`.**

    ### ⛔ **E CI STA PER UNA RAGIONE CHE `P-MOD` MI HA DETTO RIFIUTANDO IL COMMIT:**
    il collaudo deve costruire ### **lo stato come lo costruisce il driver**, quindi
    importa `driver`, `passo`, `schema_config` e `stato` -- e ### **`passo` importa
    `grafo`.** ### ⭐ **Dichiarare quegli import qui creerebbe un CICLO, e `P-MOD`
    lo rifiuta: il collaudo di un modulo che sta IN FONDO alla catena degli import non
    puo- vivere dentro quel modulo.**
    """
    del argv
    t = costo()
    print("  il controllo del grafo: %.3f us per chiamata (catena, 9 nodi, 8 archi)"
          % (t * 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
