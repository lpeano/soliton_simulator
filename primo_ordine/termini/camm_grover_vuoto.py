# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-GROVER-VUOTO** -- `pezzo_unitario`

`G(theta)` sul vuoto `phi` (punto `F4`), che e' uno SCALARE NEUTRO. ### Mescola le estremita' del nodo come quello dello spinore, e la differenza sta nel pezzo dopo: il vuoto si sposta SENZA `U`. ### ⭐ DAL 2026-10-15 IL TEMPO PROPRIO VALE ANCHE QUI, e il mandato di Luca lo chiede ESPLICITAMENTE: i flussi parziali sono per `psi` E per `phi`. E <<come quello dello spinore>> e' diventato LETTERALE -- e' LA STESSA FUNZIONE, su una vista a UNA componente, perche' `P_u + e^{i theta}(I - P_u)` non dipende da quante componenti ha il campo. ### ⭐ IL SUO POSTO NEL PASSO, dal 2026-10-15 (ordine PALINDROMO): compare DUE VOLTE a frazione 0.5 invece di UNA a frazione 1. ### ⭐⭐ DAL 2026-11-08 LO ZERO SIMMETRICO (Luca 14:19, <<ORA>>; la revisione del nucleo, voce 1): il Grover del vuoto e' `exp(i theta (I - 2P)/2)`, cioe' la forma qui sopra a `theta/2`, DUE VOLTE, poi `conj(z)` (`z = e^{i theta}` a `theta/2`, per nodo): in aritmetica esatta `e^{-i theta/2}` per la forma di prima, la STESSA legge per una fase, e lo zero dell'energia che la MAPPA chiama <<quello fisico>>. ### E' cio' che OGNI corsa dell'era 2 faceva gia' in memoria (`_zero_simmetrico`): `flussi_parziali.grover` fa le stesse operazioni nello stesso ordine, e il braccio 0 lo prova AL BIT. ### A `theta = pi` NON torna piu' il pezzo di prima AL BIT: torna `-i` volte quello.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = 'c42323b9b933ae4f'
LEGGE = 'CAMM-GROVER-VUOTO'
TIPO = 'pezzo_unitario'
AMBITO = ('phi_h',)
PARAMETRI = {}
POSTO = None
VOCE_DECISIONE = None

OPERATORE = 'grover_scalare'
AZIONE = 'nodo'


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

