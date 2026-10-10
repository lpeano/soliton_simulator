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
IMPRONTA = '825d6e697bae0a9a'

# ### (nome, tipo, ID della voce in `doc/indice/variabili.jsonl`)
VARIABILI = (
    ('psi', 'complesso_c2_nodo', 'V-PSI-ERA2'),
)

# ### I DOMINI, dal TIPO *(punto `1`)*: `(nome, tipo, forma)`.
# ### ⛔ **E IL CONTROLLO FERMA, NON TRONCA:** troncare
# ### ### **nasconde** la violazione e cambia la fisica in silenzio
# ### *(un ramo silenzioso non e- un ramo)*; fermare ### **la mostra.**
DOMINI = (
    ('psi', 'complesso_c2_nodo', 'finito'),
)


def controlla_domini(st, dove):
    """### I domini di tutte le variabili. ### **FERMA, non tronca.**

    ### ⛔ **Solleva `AssertionError` col NOME della variabile,
    la FORMA violata e ### **dove** e- successo** -- perche- un controllo che
    ferma senza dire ### **che cosa** ha visto ### **costringe a rifare la
    corsa per saperlo.**
    """
    for nome, _tipo, forma in DOMINI:
        v = st[nome]
        if forma in ('finito', 'finito-pos', 'fase-2pi'):
            cattivi = int(np.sum(~np.isfinite(v)))
            assert cattivi == 0, (
                'DOMINIO VIOLATO (' + dove + '): la variabile ' + nome
                + ' ha ' + repr(cattivi) + ' componenti NON FINITE'
                + ' (forma ' + forma + '). ### Il controllo FERMA e NON TRONCA:'
                + ' troncare cambierebbe la fisica in silenzio')
        if forma == 'finito-pos':
            cattivi = int(np.sum(np.real(v) <= 0.0))
            assert cattivi == 0, (
                'DOMINIO VIOLATO (' + dove + '): la variabile ' + nome
                + ' ha ' + repr(cattivi) + ' componenti <= 0'
                + ' (forma ' + forma + ')')
    return True


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

