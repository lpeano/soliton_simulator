# `PROVA-LOCALE`  — ### ⚠ **PROVA: NON E' FISICA DECISA**

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

> ### ⚠ **E LA LEGGE E' DICHIARATA `prova: true`:** serve a ### **collaudare la catena**, non a dire come va il mondo. ### **Nessuna fisica e' decisa qui.**

| | |
|---|---|
| **tipo** | `termine_nodo` |
| **espressione** | `(g/2)*(psi_0c*psi_0 + psi_1c*psi_1)**2` |
| **ambito** | `psi` |
| **impronta della riga** | `5518865ea31421ca` |
| **assiomi soddisfatti** | `A16` · `A17` |

## I PARAMETRI

> ### ⛔ **`A1`: LA LEGGE, NON IL NUMERO.** Ogni parametro porta ### **il valore E l'origine** — e un numero senza origine e' ### **una manopola.**

| | valore | origine |
|---|--:|---|
| `g` | `0.5` | ### VALORE DI PROVA, NON DERIVATO. Come `K`: viene DA NIENTE. |

## LA DERIVATA, GENERATA

> ### ⭐ **`dH/dpsi*` per differenziazione simbolica**, con `psi` e `psi*` ### **simboli INDIPENDENTI** *(Wirtinger)*. ### **Non e' scritta a mano in nessun posto.**

| rispetto a | `dH/d(...)` |
|---|---|
| `psi_0c` | `g*psi_0*(psi_0*psi_0c + psi_1*psi_1c)` |
| `psi_1c` | `g*psi_1*(psi_0*psi_0c + psi_1*psi_1c)` |

## LA SCHEDA, dalla tabella

Il termine locale `(g/2) (psi^dag psi)^2`: dipende SOLO dal nodo, e serve a collaudare che il generatore sappia (1) derivare una NON LINEARITA', (2) tenere il termine di nodo CIECO sui vicini -- i simboli `psi_i`/`psi_j` NON ESISTONO nel suo ambiente. ### Soddisfa `A17` perche' non nomina nessuna posizione: non potrebbe, il simbolo e' VIETATO.

