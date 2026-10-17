# -*- coding: utf-8 -*-
"""GENERATO da `primo_ordine/leggi/leggi.yaml` - NON si modifica a mano.

### ⭐ **L-ORDINE DI COMPOSIZIONE, come DATO.** Il passo ### **E-** questa
lista, e l-esecutore unico la legge: generare qui una seconda funzione
`passo()` violerebbe il presidio che dice ### **un solo esecutore.**

### ⛔ **E le RIPETIZIONI sono il punto:** la composizione di Strang usa
### **lo stesso pezzo DUE VOLTE**, e la somma delle frazioni di una legge
### **fa `1` esatto** -- lo schema lo verifica.
"""

IMPRONTA = '2e7f795d2a52fbe7'

# ### `(id della legge, frazione di passo, tipo)`
ORDINE = (
    ('CAMM-MATERIA-VUOTO', 0.5, 'flusso'),
    ('CAMM-FASE-VUOTO', 0.5, 'flusso'),
    ('CAMM-MONETA-SPIN', 0.5, 'pezzo_unitario'),
    ('CAMM-GROVER', 0.5, 'pezzo_unitario'),
    ('CAMM-SPOSTAMENTO', 0.5, 'pezzo_unitario'),
    ('CAMM-GROVER-VUOTO', 0.5, 'pezzo_unitario'),
    ('CAMM-SPOSTAMENTO-VUOTO', 0.5, 'pezzo_unitario'),
    ('CAMM-SPOSTAMENTO-VUOTO', 0.5, 'pezzo_unitario'),
    ('CAMM-GROVER-VUOTO', 0.5, 'pezzo_unitario'),
    ('CAMM-SPOSTAMENTO', 0.5, 'pezzo_unitario'),
    ('CAMM-GROVER', 0.5, 'pezzo_unitario'),
    ('CAMM-MONETA-SPIN', 0.5, 'pezzo_unitario'),
    ('CAMM-FASE-VUOTO', 0.5, 'flusso'),
    ('CAMM-MATERIA-VUOTO', 0.5, 'flusso'),
)


def leggi_in_ordine():
    """### Gli `id` nell-ordine, ### **con le ripetizioni.**"""
    return tuple(x[0] for x in ORDINE)

