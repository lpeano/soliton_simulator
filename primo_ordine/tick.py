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
import numpy as np                                             # noqa: E402

import composizione as CM                                     # noqa: E402
import flussi_parziali as FP                                  # noqa: E402

# ### ⛔ **LA SOGLIA DEL PUNTO FISSO: gli ULP**, come il mandato chiede *(<<risolto a
# ### punto fisso fino agli ulp>>)*. ### ⚠ **E- RELATIVA al massimo di `cs`**, perche-
# ### un assoluto su una grandezza in `[0, 1)` ### **sarebbe una scala nascosta.**
# ### ⛔⛔ **LA TOLLERANZA E- SCRITTA QUI, E E- UN DOPPIONE DICHIARATO** *(`2026-10-18`)*:
# ### lo stesso numero vive in ### **`flussi_parziali.EPS_PUNTO_FISSO`**, e la via giusta
# ### sarebbe ### **leggerlo da la-.** ### ⚠ **E L-HO PROVATO: NON SI PUO-, e il motivo
# ### e- MISURATO.** Il collaudo di `M-B1` ### **copia il `tick.py` di OGGI in un albero
# ### VECCHIO** *(per mostrare il falso-uno)*, e la- dentro `flussi_parziali` e- quello di
# ### allora: ### **un `EPS_CS = FP.EPS_PUNTO_FISSO` fa ALZARE l-import** *(`AttributeError`)*.
# ### ✅ **Quindi il doppione resta, ma NON in silenzio:** i due ### **si confrontano**
# ### dentro `cs_al_centro` *(non all-import, per la stessa ragione)*, e ### **se divergono
# ### ALZANO.**
EPS_CS = 8.0 * float(np.finfo(float).eps)

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
    # ### ⛔⛔ **LA FASE SUL VUOTO** *(`2026-10-18`, la strada `(d)`)*: ### **VUOLE IL
    # ### `par`**, e non e- un dettaglio -- ### **`Omega` contiene il termine della MONETA**,
    # ### che porta `eps`. ### ⚠ **Senza il `par` quel termine sparirebbe da `H`
    # ### IN SILENZIO**, e `Omega` sarebbe quello di ### **un-ALTRA energia.**
    "CAMM-FASE-VUOTO": ("CAMM-FASE-VUOTO", True),
    "CAMM-SATURAZIONE": ("CAMM-SATURAZIONE", False),
    "CAMM-MONETA-SPIN": ("moneta_spin", True),
    "CAMM-GROVER": ("grover", False),
    "CAMM-SPOSTAMENTO": ("spostamento_trasporto", False),
    "CAMM-GROVER-VUOTO": ("grover_scalare", False),
    "CAMM-SPOSTAMENTO-VUOTO": ("spostamento_scalare", False),
}


def percorri_tick(st, mot, par, salta, al_primo, quanti):
    """### IL TICK, PERCORSO IN UN SOLO POSTO: ### **l-ordine della tabella, INTERO.**

    ### ⛔⛔ **ESISTE PERCHE- C-ERANO DUE PERCORSI** *(cura del `2026-10-16`)*:
    `tick` faceva l-ordine intero, `sorgente_per_nodo` applicava ### **un pezzo A MANO,
    per nome**, e poi `CM.ORDINE[1:]` -- cioe- ### **un passo MISTO fra due leggi.** Con
    un solo posto ### **quel difetto non si puo- piu- scrivere.**

    `al_primo(st)` *(se dato)* si chiama ### **dopo il PRIMO pezzo dell-ordine, qualunque
    esso sia**: e- la fotografia dello stato che entra nei pezzi lineari.
    `salta` toglie dei pezzi ### **per id**, e serve a `vuoto_cammina=False`.

    `quanti` dice ### **QUANTI pezzi applicare**: `len(CM.ORDINE)` e- il tick intero.
    ### ⛔⛔ **ESISTE PER `D2`** *(`2026-10-17`)*: `cs` si valuta ### **sullo stato
    al CENTRO del palindromo**, e per arrivare al centro ### **serve META- del tick.**
    ### ✅ **E serve QUI e non in una copia del ciclo:** un secondo percorso del tick
    ### **e- il difetto che questo modulo esiste per impedire.**

    ### ⛔ **E I TRE ARGOMENTI NON HANNO UN VALORE DI COMODO** *(punto `15(b)`, dal
    `2026-10-16`)*: si passa ### **`()`, `None` e il numero ESPLICITI.** ### **Un parametro
    non presente e- un ERRORE, non un comportamento a sorpresa** -- e questo modulo e-
    ### **nel NUCLEO**, dove il tetto dei `default` e- ### **ZERO.**
    """
    mot.apri_tick()
    for k, (idl, frazione, _tipo) in enumerate(CM.ORDINE[:quanti]):
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


# ### ⛔ **IL TETTO DEI GIRI, e NON e- una manopola:** e- ### **il numero oltre il
# ### quale si DICHIARA che il punto fisso non converge**, e il mandato dice
# ### ### **<<relaziona coi numeri e NON scegliere un altro schema>>.**
# ### ⚠ **Misurato il `2026-10-17`: il MASSIMO dei giri e` 74 (scena nn=16, Lambda_c/Lambda = 0.3), e il tetto di `GIRI_MAX` e` 120 -- cioe` il numero oltre il quale si DICHIARA che non converge.**
# ### ⛔ **E IL 47 DI PRIMA ERA IL MASSIMO SUI SEI REGIMI DI `D2`, che NON
# ### contengono il massimo:** la spazzata a sette punti lo prende, e sta a ### **un
# ### rapporto INTERMEDIO.** ### **Il costo CALA su ENTRAMBI i lati**, quindi `GIRI_MAX`
# ### ### **non si taglia guardando solo i rapporti piccoli.**
GIRI_MAX = 120


def meta_del_palindromo():
    """### ⭐ **IL CENTRO: metà dei pezzi dell-ordine**, e ### **si DERIVA.**

    ### ⚠ **E l-ordine deve avere un numero PARI di pezzi**, altrimenti ### **un
    <<centro>> non esiste** e si ALZA invece di arrotondare.
    """
    n = len(CM.ORDINE)
    assert n % 2 == 0, (
        "l-ordine di composizione ha %d pezzi, che e- DISPARI: un palindromo di %d pezzi"
        " NON HA UN CENTRO fra due pezzi, e `cs` al centro non si puo- definire."
        " ### Si cambia la tabella, non si arrotonda" % (n, n))
    return n // 2


def cs_al_centro(st, mot, par, lambda_c, fp, salta):
    """### `(cs, giri)`: ### **`cs` dallo stato al CENTRO del palindromo, a PUNTO FISSO.**

    ### ⛔⛔ **IL PUNTO DELICATO DI `D2`, con le parole del mandato:** `cs` dipende
    da `Lambda`, e ### **`Lambda` cambia DURANTE il passo**, quindi il tempo proprio
    diventa ### **dinamico.** ### **Un `cs` letto all-INIZIO del passo ROMPE IL
    PALINDROMO.**

    ### ✅ **LA VALUTAZIONE SIMMETRICA:** `cs` si legge ### **sullo stato al centro**,
    e siccome per arrivare al centro serve ### **`cs`**, si itera:

    ```
    cs_0        = cs(Lambda allo stato INIZIALE)        (la prima ipotesi)
    cs_{n+1}    = cs(Lambda allo stato al CENTRO, avanzato con cs_n)
    ```

    ### **e si ferma quando due giri coincidono AGLI ULP.**
    ### ⚠ **L-iterazione gira su una COPIA**: lo stato vero ### **non si muove** finche-
    il `cs` non e- deciso.
    ### ⛔ **E se non converge entro `GIRI_MAX` si ALZA**, perche- il mandato dice
    ### **di relazionare e NON di scegliere un altro schema.**
    """
    meta = meta_del_palindromo()
    # ### ✅ **IL CONFRONTO DEL DOPPIONE, E STA QUI E NON ALL-IMPORT:** in un albero
    # ### vecchio `flussi_parziali` ### **non ha quel nome**, e un confronto all-import
    # ### ### **farebbe ALZARE il collaudo di `M-B1`** -- che e- il motivo per cui il
    # ### doppione esiste. ### ⚠ **Qui invece gira solo quando la forma `cs` gira.**
    assert EPS_CS == getattr(FP, "EPS_PUNTO_FISSO", EPS_CS), (
        "`tick.EPS_CS` (%r) e `flussi_parziali.EPS_PUNTO_FISSO` (%r) sono DIVERSI: sono"
        " lo stesso numero scritto in due posti, e due numeri uguali in due posti"
        " DIVERGONO -- questo assert e- il presidio di quel doppione"
        % (EPS_CS, getattr(FP, "EPS_PUNTO_FISSO", None)))
    # ### ⛔ **IL NUMERO PRIMA DEL VETTORE** *(`2026-10-18`)*: il tick con `cs`
    # ### percorre ### **mezzo palindromo**, e la' dentro c'e' ### **`CAMM-FASE-VUOTO`**,
    # ### che legge `mot.lambda_c`. ### ⚠ **Senza questa riga il pezzo nuovo
    # ### non girerebbe DENTRO il punto fisso**, e il `cs` del centro
    # ### ### **sarebbe quello di un altro passo.**
    mot.lambda_c = float(lambda_c)
    lam = mot.densita_vuoto(st)
    prec = FP.cs(lam, lambda_c, fp).copy()
    for giri in range(1, GIRI_MAX + 1):
        copia = {k: (v.copy() if hasattr(v, "copy") else v) for k, v in st.items()}
        mot.cs = prec
        percorri_tick(copia, mot, par, salta, None, meta)
        nuovo = FP.cs(mot.densita_vuoto(copia), lambda_c, fp).copy()
        scarto = float(np.max(np.abs(nuovo - prec)))
        if scarto <= EPS_CS * float(np.max(np.abs(nuovo))):
            mot.cs = nuovo
            return nuovo, giri
        prec = nuovo
    raise AssertionError(
        "il punto fisso di `cs` NON CONVERGE in %d giri (ultimo scarto %.3e): il mandato"
        " dice di RELAZIONARE coi numeri e NON di scegliere un altro schema, quindi questo"
        " ALZA invece di fermarsi a un valore qualunque" % (GIRI_MAX, scarto))


def tick_con_cs(st, mot, par, lambda_c, salta):
    """### Un tick ### **con `cs` SIMMETRICO**: `(giri,)` che il punto fisso ha speso.

    ### ⛔⛔ **E `salta` NON HA UN VALORE DI COMODO** *(`2026-10-18`)*: serve al
    ### **caso che DEVE fallire di `C1`** -- la stessa corsa ### **senza il termine
    nuovo** -- e passarlo ### **esplicito** e' la regola del nucleo *(zero `default`)*.
    ### ⚠ **E va dato anche al punto fisso**, altrimenti il `cs` del centro
    ### **sarebbe quello di un altro passo.**
    """
    fp = mot._b("tk_cs", (mot.inc.n,), float)
    _c, giri = cs_al_centro(st, mot, par, lambda_c, fp, salta)
    percorri_tick(st, mot, par, salta, None, len(CM.ORDINE))
    return giri


def tick(st, mot, par):
    """### UN tick, ### **nell'ordine della tabella e non in uno mio.**"""
    percorri_tick(st, mot, par, (), None, len(CM.ORDINE))
