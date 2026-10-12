# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-MONETA-SPIN** -- `pezzo_unitario`

`exp(-i eps dtau sigma.n)` per ESTREMITA' (punto `F1`). E' qui che SPIN e DIREZIONE si legano, ed e' ESATTA e non un'esponenziale numerica: `exp(-i a sigma.n) = cos a I - i sin a (sigma.n)` perche' `(sigma.n)^2 = I` quando `|n| = 1`. ### Quindi nessun errore di troncamento, e la forma e' UNITARIA AL BIT. ### AZIONE `estremita`: agisce su una estremita' per volta, e NON legge il vicino.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = '75bcd40bccb090c7'
LEGGE = 'CAMM-MONETA-SPIN'
TIPO = 'pezzo_unitario'
AMBITO = ('psi_h',)
PARAMETRI = {'eps': 0.5}
POSTO = None
VOCE_DECISIONE = None

OPERATORE = 'moneta_spin'
AZIONE = 'estremita'


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

