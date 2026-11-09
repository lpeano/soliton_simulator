# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-SPOSTAMENTO-VUOTO** -- `pezzo_unitario`

`hop(theta) = alpha I + beta S` sul vuoto (punto `F4`), SENZA `U`: `S` e' la permutazione PURA. ### E il <<senza `U`>> non e' una semplificazione: `phi` e' NEUTRO, quindi non ha carica da trasportare -- e dargli una `U` vorrebbe dire dargli una carica che non ha. ### ⭐ DAL 2026-10-15 E' UN FLUSSO PARZIALE come quello dello spinore, con lo STESSO `dtau_arco` (la media armonica di `B-3`) e lo STESSO `omega` (`B-4`): a `theta = pi` torna lo scambio di prima AL BIT. ### ⚠ E <<in posto con una fetta rovesciata>> NON SI PUO' PIU': ogni lato nuovo dipende da ENTRAMBI i lati vecchi, non solo dall'altro. ### ⭐⭐ DAL 2026-11-08 LO ZERO SIMMETRICO (Luca 14:19, <<ORA>>; la revisione del nucleo, voce 1): lo spostamento del vuoto e' `exp(i theta (I - 2P)/2)`, cioe' la forma qui sopra a `theta/2`, DUE VOLTE, poi `conj(z)` (`z = e^{i theta}` a `theta/2`, per arco): in aritmetica esatta `e^{-i theta/2}` per la forma di prima, la STESSA legge per una fase, e lo zero dell'energia che la MAPPA chiama <<quello fisico>>. ### E' cio' che OGNI corsa dell'era 2 faceva gia' in memoria (`_zero_simmetrico`): `flussi_parziali.hop_phi` fa le stesse operazioni nello stesso ordine, e il braccio 0 lo prova AL BIT. ### A `theta = pi` NON torna piu' il pezzo di prima AL BIT: torna `-i` volte quello.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = '9114aa5b417597f6'
LEGGE = 'CAMM-SPOSTAMENTO-VUOTO'
TIPO = 'pezzo_unitario'
AMBITO = ('phi_h',)
PARAMETRI = {}
POSTO = None
VOCE_DECISIONE = None

OPERATORE = 'spostamento_scalare'
AZIONE = 'arco'


def applica(st, motore, frazione):
    """### Applica questo pezzo allo stato, ### **tramite il MOTORE.**

    ### ⛔ **NON fa la fisica qui dentro:** la fisica e- ### **un
    operatore del motore**, e questo modulo e- ### **il legame fra la tabella
    e lui.**
    """
    quale = OPERATORE
    fai = getattr(motore, 'operatori', {}).get(quale)
    if fai is None:
        raise NotImplementedError(
            'il motore non ha l-operatore ' + repr(quale)
            + ': questo modulo e- un LEGAME, e un legame senza il suo'
            + ' operatore ALZA invece di tornare un risultato finto')
    return fai(st, PARAMETRI, frazione)

