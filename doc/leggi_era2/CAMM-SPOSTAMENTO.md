# `CAMM-SPOSTAMENTO`

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

| | |
|---|---|
| **tipo** | `pezzo_unitario` |
| **operatore** | `spostamento_trasporto`, azione `arco` |
| **ambito** | `psi_h` |
| **impronta della riga** | `a27f35454a5d2c56` |
| **assiomi soddisfatti** | `A13` · `A16` |


## LA SCHEDA, dalla tabella

`hop(theta) = alpha I + beta S_U` sull'ARCO (punti `F1` e `F2`), con `alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`, `S_U = [[0, U^dagger],[U, 0]]` e `theta = pi dtau_arco/dtau_rif`. ### ⭐ DAL 2026-10-15 E' UN FLUSSO PARZIALE (strada `(B)`): `S_U` e' hermitiana E unitaria, quindi con `P- = (I - S_U)/2` si ha `exp(i pi P-) = S_U` -- lo spostamento di prima E' questo flusso ALL'ANGOLO `pi`, e a `theta = pi` torna AL BIT (`M-B1`). ### ⭐ E `dtau_arco` E' LA MEDIA ARMONICA dei due nodi (`B-3`), `2 dtau_i dtau_j/(dtau_i + dtau_j)`, perche' e' la somma dei tempi di attraversamento delle DUE META' dell'arco, ciascuna alla velocita' del proprio nodo. L'ipotesi <<due meta' uguali>> e' DICHIARATA, non dimostrata. ### ⚠ E IL CONO RESTA: `theta <= pi` PER COSTRUZIONE, perche' `dtau <= dtau_rif` (`B-5`: il tick e' l'orologio piu' veloce possibile). NESSUN TETTO E NESSUN CLIP (`A11`): un `dtau` oltre il cono ALZA. ### E' una PERMUTAZIONE composta col trasporto `U(2)`, e non un prodotto matrice-vettore: la parte `U(1)` di `U` e' l'elettromagnetismo, la parte `SU(2)` la geometria. ### E `A13` c'e' perche' la SCALA MINIMA E' UN ARCO: sotto l'arco non esiste niente, nemmeno una distanza. ### AZIONE `arco`: scambia le due estremita' dello stesso arco.

