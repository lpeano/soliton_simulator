# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **CAMM-SPOSTAMENTO** -- `pezzo_unitario`

`hop(theta) = alpha I + beta S_U` sull'ARCO (punti `F1` e `F2`), con `alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`, `S_U = [[0, U^dagger],[U, 0]]` e `theta = pi dtau_arco/dtau_rif`. ### ⭐ DAL 2026-10-15 E' UN FLUSSO PARZIALE (strada `(B)`): `S_U` e' hermitiana E unitaria, quindi con `P- = (I - S_U)/2` si ha `exp(i pi P-) = S_U` -- lo spostamento di prima E' questo flusso ALL'ANGOLO `pi`, e a `theta = pi` torna AL BIT (`M-B1`). ### ⭐ E `dtau_arco` E' LA MEDIA ARMONICA dei due nodi (`B-3`), `2 dtau_i dtau_j/(dtau_i + dtau_j)`, perche' e' la somma dei tempi di attraversamento delle DUE META' dell'arco, ciascuna alla velocita' del proprio nodo. L'ipotesi <<due meta' uguali>> e' DICHIARATA, non dimostrata. ### ⚠ E IL CONO RESTA: `theta <= pi` PER COSTRUZIONE, perche' `dtau <= dtau_rif` (`B-5`: il tick e' l'orologio piu' veloce possibile). NESSUN TETTO E NESSUN CLIP (`A11`): un `dtau` oltre il cono ALZA. ### E' una PERMUTAZIONE composta col trasporto `U(2)`, e non un prodotto matrice-vettore: la parte `U(1)` di `U` e' l'elettromagnetismo, la parte `SU(2)` la geometria. ### E `A13` c'e' perche' la SCALA MINIMA E' UN ARCO: sotto l'arco non esiste niente, nemmeno una distanza. ### AZIONE `arco`: scambia le due estremita' dello stesso arco.

### ⛔ **QUESTO MODULO E- UN LEGAME, non uno stub:** `applica()` chiede
l-operatore ### **al motore**, e se il motore non ce l-ha ### **ALZA** -- non
torna un risultato finto.
"""

IMPRONTA = 'a27f35454a5d2c56'
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

