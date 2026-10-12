# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-SATURAZIONE** -- `flusso`

La saturazione `N_k = Lambda_k G(h_k / Lambda_k)` con `G(x) = x - arctan x` (punto `F5`). ### SENZA NESSUNA COSTANTE `g`, e la scala e' IL VUOTO LOCALE: e' questo che rende il termine RELAZIONALE invece di tarato. ### `esatto: true` NON E' UNA PROMESSA: il flusso si integra in forma CHIUSA, e un collaudo lo verifica -- un flusso <<esatto>> che sbaglia all'ordine `dtau^2` sarebbe un flusso APPROSSIMATO CHE MENTE. ### E LA SUA DERIVATA E' AL PIU' `1` (`G'(x) = x^2/(1+x^2)`), che e' il fatto misurato dietro l'ipotesi <<la saturazione e' una LENTE e non una BUCA>> (`PERCHE-NON-LEGA`).

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = 'fbd8b8e9c2239730'
LEGGE = 'CAMM-SATURAZIONE'
TIPO = 'flusso'
AMBITO = ('psi_h', 'phi_h', 'Lambda', 'h_int')
PARAMETRI = {}
POSTO = None
VOCE_DECISIONE = None

GENERATORE = 'Lambda*(h_int/Lambda - atan(h_int/Lambda))'
ESATTO = True


def applica(st, motore, frazione):
    """### Applica questo pezzo allo stato, ### **tramite il MOTORE.**

    ### ⛔ **NON fa la fisica qui dentro:** la fisica e- ### **un
    operatore del motore**, e questo modulo e- ### **il legame fra la tabella
    e lui.**
    """
    quale = LEGGE
    fai = getattr(motore, 'operatori', {}).get(quale)
    if fai is None:
        raise NotImplementedError(
            'il motore non ha l-operatore ' + repr(quale)
            + ': questo modulo e- un LEGAME, e un legame senza il suo'
            + ' operatore ALZA invece di tornare un risultato finto')
    return fai(st, PARAMETRI, frazione)

