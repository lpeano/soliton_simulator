# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-FORMA-D** -- `flusso`

La forma `(D)` dell'auto-interazione dell'interferenza (punto `F6`), DICHIARATA SPENTA: NON entra nell'ordine di composizione, e il suo posto nella tabella serve a dire CHE ESISTE e che il suo posto e' dichiarato. ### ⛔ PERCHE' SPENTA, con un numero: sulla scena principale a `26000` nodi il segno diretto di questa forma e' PEGGIO del lineare -- meno `21.6%` della frazione entro un arco, a `6.5 sigma` (`doc/REFERTO_legame.md`). ### Non e' neutro: e' SFAVOREVOLE. ### E IL SUO SEGNO E' UN POSTO APERTO (`DOMANDA-QUALE-SEGNO`): la domanda non e' piu' <<quale segno lega>> ma <<quale segno serve QUANDO IL CAMPO C'E'>>, e si decide sulla prova con la `U` dinamica accesa.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = '7b6c204429ebc89d'
LEGGE = 'CAMM-FORMA-D'
TIPO = 'flusso'
AMBITO = ('psi_h', 'phi_h', 'Lambda', 'h_int')
PARAMETRI = {}
POSTO = 'A4'
VOCE_DECISIONE = 'DOMANDA-QUALE-SEGNO'

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

