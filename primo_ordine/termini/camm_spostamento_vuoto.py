# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-SPOSTAMENTO-VUOTO** -- `pezzo_unitario`

Lo spostamento del vuoto (punto `F4`), SENZA `U`. ### E il <<senza `U`>> non e' una semplificazione: `phi` e' NEUTRO, quindi non ha carica da trasportare -- e dargli una `U` vorrebbe dire dargli una carica che non ha.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = '68c3e9df884091ae'
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

