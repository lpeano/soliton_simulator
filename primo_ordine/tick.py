# -*- coding: utf-8 -*-
"""IL PASSO DELLA CAMMINATA — **un tick, nell'ordine della tabella e non in uno mio.**

> ### ⛔⛔ **PERCHE' QUESTO MODULO ESISTE** *(decisione di Luca del `2026-10-16`
> alle `19:33`)*: `percorri_tick` **percorre l'ordine di composizione**, cioe' **E' il
> passo** — e viveva in `deriva.py`, che e' **una misura.**
> ### ⛔ **Tirare `deriva.py` nel nucleo della fisica ci porterebbe dentro `energia`,
> `corrente`, `deriva_serie`, `deriva_variabile`:** il mandato dice di **non allargare il
> nucleo**, e di **spostare il passo accanto al motore.**
> ### ⚠ **E NON in `composizione.py`**, che **SI GENERA** dalla tabella: scriverci a mano
> e' vietato.

## ⭐ QUESTO MODULO E' UNA **RADICE DEL NUCLEO**, dichiarata e **PROVVISORIA**

`csv/_rami_era2.py` deriva il nucleo come **chiusura degli import** a partire dalle
radici. ### **`tick.py` e' l'ingresso del passo della CAMMINATA**, come `passo.py` lo e'
per la via di `H`. ### ⚠ **La radice e' DICHIARATA**, e lo resta **finche' la tabella
delle leggi non avra' il campo `modulo`** *(pezzo `6` della coda)*: da allora i moduli
delle leggi **si leggeranno da la'**.

### ✅ **E LO SPOSTAMENTO NON HA CAMBIATO UN BIT:** nessuna operazione in virgola
mobile si e' mossa, e il criterio era **`M-B1` AL BIT** piu' il braccio `(c)` di
`_collauda_deriva.py` *(il tick dello strumento contro `tick`, `0.0e+00` su `6` campi)*.
"""
import os
import sys

_QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _QUI)
sys.path.insert(0, os.path.join(_QUI, "leggi"))
import composizione as CM                                     # noqa: E402

# ### ⛔ **LA LEGGE -> L'OPERATORE, e NON e' una mia scelta:** la lista delle leggi e il
# ### loro ordine stanno in `composizione.py`, che e' ### **GENERATA dalla tabella**; qui
# ### c'e' solo ### **il nome con cui il motore registra ciascuna.**
# ### ⚠ **E un `id` che non e' in questa mappa FERMA**, invece di essere saltato in
# ### silenzio: ### **un pezzo del tick che non gira e' un tick diverso.**
OPERATORE = {
    # ### ⭐⭐ **IL FLUSSO CHE GIRA dal `2026-10-15`** *(decisione di Luca)*:
    # ### `CAMM-MATERIA-VUOTO` ### **sostituisce** `CAMM-SATURAZIONE` nell-ordine di
    # ### composizione. ### ⚠ **La riga della saturazione RESTA**, perche- la legge
    # ### resta in tabella e il suo operatore esiste: ### **una riga tolta da qui
    # ### farebbe ALZARE il tick se qualcuno la rimettesse nell-ordine**, invece di
    # ### girare.
    "CAMM-MATERIA-VUOTO": ("CAMM-MATERIA-VUOTO", False),
    "CAMM-SATURAZIONE": ("CAMM-SATURAZIONE", False),
    "CAMM-MONETA-SPIN": ("moneta_spin", True),
    "CAMM-GROVER": ("grover", False),
    "CAMM-SPOSTAMENTO": ("spostamento_trasporto", False),
    "CAMM-GROVER-VUOTO": ("grover_scalare", False),
    "CAMM-SPOSTAMENTO-VUOTO": ("spostamento_scalare", False),
}


def percorri_tick(st, mot, par, salta, al_primo):
    """### IL TICK, PERCORSO IN UN SOLO POSTO: ### **l-ordine della tabella, INTERO.**

    ### ⛔⛔ **ESISTE PERCHE- C-ERANO DUE PERCORSI** *(cura del `2026-10-16`)*:
    `tick` faceva l-ordine intero, `sorgente_per_nodo` applicava ### **un pezzo A MANO,
    per nome**, e poi `CM.ORDINE[1:]` -- cioe- ### **un passo MISTO fra due leggi.** Con
    un solo posto ### **quel difetto non si puo- piu- scrivere.**

    `al_primo(st)` *(se dato)* si chiama ### **dopo il PRIMO pezzo dell-ordine, qualunque
    esso sia**: e- la fotografia dello stato che entra nei pezzi lineari.
    `salta` toglie dei pezzi ### **per id**, e serve a `vuoto_cammina=False`.

    ### ⛔ **E I DUE ARGOMENTI NON HANNO UN VALORE DI COMODO** *(punto `15(b)`, dal
    `2026-10-16`)*: si passa ### **`()` e `None` ESPLICITI.** ### **Un parametro non
    presente e- un ERRORE, non un comportamento a sorpresa** -- e questo modulo e-
    ### **nel NUCLEO**, dove il tetto dei `default` e- ### **ZERO.**
    """
    mot.apri_tick()
    for k, (idl, frazione, _tipo) in enumerate(CM.ORDINE):
        if idl not in salta:
            nome, vuole_par = OPERATORE.get(idl, (None, None))
            assert nome, (
                "la legge `%s` e' nell'ordine di composizione e NON e' in `OPERATORE`:"
                " ### **un pezzo del tick che non gira e' un tick diverso**, e saltarlo in"
                " silenzio sarebbe misurare un'altra cosa" % idl)
            mot.operatori[nome](st, par if vuole_par else {}, frazione)
        if k == 0 and al_primo is not None:
            al_primo(st)
    mot.chiudi_tick()


def tick(st, mot, par):
    """### UN tick, ### **nell'ordine della tabella e non in uno mio.**"""
    percorri_tick(st, mot, par, (), None)
