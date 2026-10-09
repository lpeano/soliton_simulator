# -*- coding: utf-8 -*-
"""IL GENERATORE DI `stato.py` — **tenuto in un file suo, e il perché è una lezione.**

> ### ⛔ **Il primo tentativo era una funzione dentro `_genera.py`, scritta da una patch che
> costruiva Python che costruiva Python.** ### **Tre livelli di virgolette annidate**, e
> l'ho già pagato ### **tre volte in tre giorni** *(una stringa spezzata a metà che non si
> chiudeva)*.
>
> ### ✔ **Qui il codice generato si compone da righe SEMPLICI**, e questo file
> ### **si scrive una volta e si legge.**

### ⭐ **E `stato.py` SI GENERA, invece di essere scritto a mano:** il mandato lo elenca
fuori da `termini/`, e la tentazione era dichiarare le variabili lì. ### ⛔ **Ma la tabella
è l'UNICA fonte**, e una variabile dichiarata ### **in due posti** — la tabella e il
modulo — ### **divergerebbe.**

### ⚠ **È una mia decisione di progetto, e la dichiaro:** se Luca preferisce `stato.py`
scritto a mano, ### **`P-E3` diventa il presidio che tiene insieme DUE dichiarazioni**
invece di una generata — ### **più debole, e va saputo.**
"""
NL = chr(10)
Q = chr(34) * 3


def stato_py(varia, imp):
    """### Il sorgente di `primo_ordine/stato.py`, ### **dalla tabella.**"""
    L = ["# -*- coding: utf-8 -*-",
         Q + "GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.",
         "",
         "### **LO STATO:** le variabili, ciascuna col suo ### **ID di",
         "`doc/indice/variabili.jsonl`** - e `P-E3` verifica che la corrispondenza sia",
         "### **in biiezione.**",
         "",
         "### " + chr(0x26A0) + " **E NESSUNA GEOMETRIA:** la decisione `9` e- ### **APERTA**,",
         "e `A17` vieta che una posizione entri nella fisica. ### **Il simbolo `pos` non",
         "esiste.**",
         Q,
         "import numpy as np",
         "",
         "# ### L-IMPRONTA del blocco `variabili` della tabella: `P-E2` la confronta.",
         "IMPRONTA = " + repr(imp),
         "",
         "# ### (nome, tipo, ID della voce in `doc/indice/variabili.jsonl`)",
         "VARIABILI = ("]
    for v in varia:
        L.append("    (%r, %r, %r)," % (v["nome"], v["tipo"], v["voce"]))
    L += [")",
          "",
          "",
          "def nuovo(n):",
          "    " + Q + "### Uno stato vuoto per `n` nodi.",
          "",
          "    ### " + chr(0x26D4) + " **Nessun arco qui: gli archi sono del GRAFO**, e il",
          "    grafo ### **non e- una variabile di stato.**",
          "    " + Q,
          "    st = {}",
          "    for nome, tipo, _voce in VARIABILI:",
          "        if tipo == 'complesso_c2_nodo':",
          "            st[nome] = np.zeros((n, 2), dtype=complex)",
          "        elif tipo == 'reale_nodo':",
          "            st[nome] = np.zeros(n, dtype=float)",
          "        else:",
          "            # ### " + chr(0x26D4) + " **Un tipo d-ARCO o una `coppia_coniugata`",
          "            # ### non si costruisce qui:** il primo ha bisogno del ### **GRAFO**,",
          "            # ### la seconda ### **non la usa nessuna legge** *(decisione `13`,",
          "            # ### APERTA)*.",
          "            raise NotImplementedError(",
          "                'il tipo ' + repr(tipo) + ' non si costruisce ancora: serve il'",
          "                ' grafo, o e- la decisione 13 (APERTA)')",
          "    return st",
          ""]
    return NL.join(L) + NL
