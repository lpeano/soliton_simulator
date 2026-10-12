# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-SPOSTAMENTO** -- `pezzo_unitario`

`psi'[partner(h)] = U[h] psi[h]` (punti `F1` e `F2`): E' IL CONO, un arco per tick, cioe' LA VELOCITA' DELLA LUCE del sistema. ### E' una PERMUTAZIONE composta col trasporto `U(2)`, e non un prodotto matrice-vettore: la parte `U(1)` di `U` e' l'elettromagnetismo, la parte `SU(2)` la geometria. ### E `A13` c'e' perche' la SCALA MINIMA E' UN ARCO: sotto l'arco non esiste niente, nemmeno una distanza. ### AZIONE `arco`: scambia le due estremita' dello stesso arco.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = 'eb856d8c56f3928c'
LEGGE = 'CAMM-SPOSTAMENTO'
TIPO = 'pezzo_unitario'
AMBITO = ('psi_h',)
PARAMETRI = {}
POSTO = None
VOCE_DECISIONE = None

OPERATORE = 'spostamento_trasporto'
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

