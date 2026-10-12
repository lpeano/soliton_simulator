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
         "# ### L-IMPRONTA del blocco `variabili` della tabella: un presidio la confronta.",
         "IMPRONTA = " + repr(imp),
         "",
         "# ### (nome, tipo, ID della voce in `doc/indice/variabili.jsonl`)",
         "VARIABILI = ("]
    for v in varia:
        L.append("    (%r, %r, %r)," % (v["nome"], v["tipo"], v["voce"]))
    L += [")",
          "",
          "# ### I DOMINI, dal TIPO *(punto `1`)*: `(nome, tipo, forma)`.",
          "# ### " + chr(0x26D4) + " **E IL CONTROLLO FERMA, NON TRONCA:** troncare",
          "# ### ### **nasconde** la violazione e cambia la fisica in silenzio",
          "# ### *(un ramo silenzioso non e- un ramo)*; fermare ### **la mostra.**",
          "DOMINI = ("]
    import schema as _SCH
    for v in varia:
        L.append("    (%r, %r, %r)," % (v["nome"], v["tipo"],
                                        _SCH.DOMINI[v["tipo"]]))
    L += [")",
          "",
          "",
          "def controlla_domini(st, dove):",
          "    " + Q + "### I domini di tutte le variabili. ### **FERMA, non tronca.**",
          "",
          "    ### " + chr(0x26D4) + " **Solleva `AssertionError` col NOME della variabile,",
          "    la FORMA violata e ### **dove** e- successo** -- perche- un controllo che",
          "    ferma senza dire ### **che cosa** ha visto ### **costringe a rifare la",
          "    corsa per saperlo.**",
          "    " + Q,
          "    for nome, _tipo, forma in DOMINI:",
          "        v = st[nome]",
          "        if forma in ('finito', 'finito-pos', 'fase-2pi'):",
          "            cattivi = int(np.sum(~np.isfinite(v)))",
          "            assert cattivi == 0, (",
          "                'DOMINIO VIOLATO (' + dove + '): la variabile ' + nome",
          "                + ' ha ' + repr(cattivi) + ' componenti NON FINITE'",
          "                + ' (forma ' + forma + '). ### Il controllo FERMA e NON TRONCA:'",
          "                + ' troncare cambierebbe la fisica in silenzio')",
          "        if forma == 'finito-pos':",
          "            cattivi = int(np.sum(np.real(v) <= 0.0))",
          "            assert cattivi == 0, (",
          "                'DOMINIO VIOLATO (' + dove + '): la variabile ' + nome",
          "                + ' ha ' + repr(cattivi) + ' componenti <= 0'",
          "                + ' (forma ' + forma + ')')",
          "    return True",
          "",
          "",
          # ### ⛔ **E `m` NON HA UN VALORE DI COMODO, perche- il punto `15(b)` lo VIETA:**
    # ### *<<un parametro NON PRESENTE e- un ERRORE, non un comportamento a sorpresa>>.*
    # ### ⭐ **E qui il divieto ha ragione due volte:** un `m` di comodo vorrebbe dire
    # ### ### **uno stato della taglia sbagliata che gira senza che nessuno l-abbia scelto**
    # ### -- ed e- esattamente cio- che il repo ha misurato altrove.
          "def nuovo(n, m):",
          "    " + Q + "### Uno stato vuoto per `n` nodi e, se serve, `m` ARCHI.",
          "",
          "    ### " + chr(0x2B50) + " **E `m` NON E- UN-AGGIUNTA DI COMODO: lo stato della",
          "    camminata e- DIMENSIONATO DAGLI ARCHI.** Lo spinore della camminata vive",
          "    sulle ### **ESTREMITA- D-ARCO** *(punto `F1` della carta della fisica)*, e",
          "    un grafo con `n` nodi ne ha ### **`2 m`** -- un numero che ### **`n` non",
          "    contiene.**",
          "",
          "    ### " + chr(0x26A0) + " **E `m` E- OBBLIGATORIO, per il punto `15(b)`:**",
          "    un parametro non presente e- ### **un errore**, non un comportamento a",
          "    sorpresa -- e un `m` di comodo darebbe ### **uno stato della taglia",
          "    sbagliata che gira senza che nessuno l-abbia scelto.**",
          "",
          "    ### " + chr(0x26D4) + " **E il grafo NON diventa una variabile di stato:**",
          "    `m` entra come ### **TAGLIA**, non come dato -- gli archi restano ### **del",
          "    GRAFO.**",
          "    " + Q,
          "    st = {}",
          "    ne = 2 * int(m)",
          "    for nome, tipo, _voce in VARIABILI:",
          "        if tipo == 'complesso_c2_nodo':",
          "            st[nome] = np.zeros((n, 2), dtype=complex)",
          "        elif tipo == 'reale_nodo':",
          "            st[nome] = np.zeros(n, dtype=float)",
          "        elif tipo in ('complesso_c2_estremita', 'complesso_estremita'):",
          "            # ### " + chr(0x26D4) + " **ENTRAMBI COMPLESSI, e il vuoto",
          "            # ### lo e- per DECISIONE DI LUCA del 2026-10-12:** la `C` lo",
          "            # ### CONIUGA e la saturazione gli da- una FASE, e su un reale",
          "            # ### ### **la prima sarebbe l-identita- e la seconda",
          "            # ### impossibile.**",
          "            st[nome] = np.zeros((ne, 2), dtype=complex) \\",
          "                if tipo == 'complesso_c2_estremita' \\",
          "                else np.zeros(ne, dtype=complex)",
          "        else:",
          "            # ### " + chr(0x26D4) + " **Un tipo d-ARCO o una `coppia_coniugata`",
          "            # ### non si costruisce qui:** il primo e- ### **dell-arco e non",
          "            # ### dell-estremita-**, la seconda ### **non la usa nessuna legge**",
          "            # ### *(decisione `13`, APERTA)*.",
          "            raise NotImplementedError(",
          "                'il tipo ' + repr(tipo) + ' non si costruisce ancora: serve il'",
          "                ' grafo, o e- la decisione 13 (APERTA)')",
          "    return st",
          ""]
    return NL.join(L) + NL
