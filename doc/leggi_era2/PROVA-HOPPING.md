# `PROVA-HOPPING`  — ### ⚠ **PROVA: NON E' FISICA DECISA**

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

> ### ⚠ **E LA LEGGE E' DICHIARATA `prova: true`:** serve a ### **collaudare la catena**, non a dire come va il mondo. ### **Nessuna fisica e' decisa qui.**

| | |
|---|---|
| **tipo** | `termine_arco` |
| **espressione** | `-K*(psi_i_0c*psi_j_0 + psi_i_1c*psi_j_1 + psi_j_0c*psi_i_0 + psi_j_1c*psi_i_1)` |
| **ambito** | `psi` |
| **impronta della riga** | `f36ea3785e292916` |
| **assiomi soddisfatti** | `A16` |

## I PARAMETRI

> ### ⛔ **`A1`: LA LEGGE, NON IL NUMERO.** Ogni parametro porta ### **il valore E l'origine** — e un numero senza origine e' ### **una manopola.**

| | valore | origine |
|---|--:|---|
| `K` | `1.0` | ### VALORE DI PROVA, NON DERIVATO. `A1` pretende che un numero dica da dove viene: questo viene DA NIENTE, ed e' per questo che la legge e' `prova: true`. Una legge di fisica con un parametro cosi' NON SI SCRIVE. |

## LA DERIVATA, GENERATA

> ### ⭐ **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` ### **simboli INDIPENDENTI** *(Wirtinger)*. ### **Non e' scritta a mano in nessun posto.**

| rispetto a | `dH/d(...)` |
|---|---|
| `psi_i_0c` | `-K*psi_j_0` |
| `psi_i_1c` | `-K*psi_j_1` |
| `psi_j_0c` | `-K*psi_i_0` |
| `psi_j_1c` | `-K*psi_i_1` |

## LA SCHEDA, dalla tabella

Il salto fra due nodi, nella forma BILINEARE `psi_i^dag (...) psi_j + c.c.`. E' il termine piu' semplice che accoppia due nodi, e serve a collaudare che il generatore sappia: (1) distinguere i due capi di un arco, (2) derivare rispetto ai coniugati di ENTRAMBI, (3) accumulare il gradiente sui due capi con `np.add.at`. ### NON E' LA LEGGE DEL SALTO: e' la FORMA PIU' SEMPLICE che ha quella forma.

