# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### **LO STATO:** le variabili, ciascuna col suo ### **ID di
`doc/indice/variabili.jsonl`** - e `P-E3` verifica che la corrispondenza sia
### **in biiezione.**

### ⚠ **E NESSUNA GEOMETRIA:** la decisione `9` e- ### **APERTA**,
e `A17` vieta che una posizione entri nella fisica. ### **Il simbolo `pos` non
esiste.**
"""
import numpy as np

# ### L-IMPRONTA del blocco `variabili` della tabella: un presidio la confronta.
IMPRONTA = 'ff5c058ce3e855b7'

# ### (nome, tipo, ID della voce in `doc/indice/variabili.jsonl`)
VARIABILI = (
    ('psi', 'complesso_c2_nodo', 'V-PSI-ERA2'),
)


def nuovo(n):
    """### Uno stato vuoto per `n` nodi.

    ### ⛔ **Nessun arco qui: gli archi sono del GRAFO**, e il
    grafo ### **non e- una variabile di stato.**
    """
    st = {}
    for nome, tipo, _voce in VARIABILI:
        if tipo == 'complesso_c2_nodo':
            st[nome] = np.zeros((n, 2), dtype=complex)
        elif tipo == 'reale_nodo':
            st[nome] = np.zeros(n, dtype=float)
        else:
            # ### ⛔ **Un tipo d-ARCO o una `coppia_coniugata`
            # ### non si costruisce qui:** il primo ha bisogno del ### **GRAFO**,
            # ### la seconda ### **non la usa nessuna legge** *(decisione `13`,
            # ### APERTA)*.
            raise NotImplementedError(
                'il tipo ' + repr(tipo) + ' non si costruisce ancora: serve il'
                ' grafo, o e- la decisione 13 (APERTA)')
    return st

