# `CAMM-SPOSTAMENTO`

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

| | |
|---|---|
| **tipo** | `pezzo_unitario` |
| **operatore** | `spostamento_trasporto`, azione `arco` |
| **ambito** | `psi_h` |
| **impronta della riga** | `d3f2ba5cd1933aab` |
| **assiomi soddisfatti** | `A13` · `A16` |


## LA SCHEDA, dalla tabella

`hop(theta) = alpha I + beta S_U` sull'ARCO (punti `F1` e `F2`), con `alpha = (1 + e^{i theta})/2`, `beta = (1 - e^{i theta})/2`, `S_U = [[0, U^dagger],[U, 0]]` e `theta = pi dtau_arco/dtau_rif`. ### ⭐ DAL 2026-10-15 E' UN FLUSSO PARZIALE (strada `(B)`): `S_U` e' hermitiana E unitaria, quindi con `P- = (I - S_U)/2` si ha `exp(i pi P-) = S_U` -- lo spostamento di prima E' questo flusso ALL'ANGOLO `pi`, e a `theta = pi` torna AL BIT (`M-B1`). ### ⭐ E `dtau_arco` E' LA MEDIA ARMONICA dei due nodi (`B-3`), `2 dtau_i dtau_j/(dtau_i + dtau_j)`, perche' e' la somma dei tempi di attraversamento delle DUE META' dell'arco, ciascuna alla velocita' del proprio nodo. L'ipotesi <<due meta' uguali>> e' DICHIARATA, non dimostrata. ### ⚠ E IL CONO RESTA: `theta <= pi` PER COSTRUZIONE, perche' `dtau <= dtau_rif` (`B-5`: il tick e' l'orologio piu' veloce possibile). NESSUN TETTO E NESSUN CLIP (`A11`): un `dtau` oltre il cono ALZA. ### E' una PERMUTAZIONE composta col trasporto `U(2)`, e non un prodotto matrice-vettore: la parte `U(1)` di `U` e' l'elettromagnetismo, la parte `SU(2)` la geometria. ### E `A13` c'e' perche' la SCALA MINIMA E' UN ARCO: sotto l'arco non esiste niente, nemmeno una distanza. ### AZIONE `arco`: scambia le due estremita' dello stesso arco. ### ⭐⭐ DAL 2026-11-08 LO ZERO SIMMETRICO (Luca 14:19, <<ORA>>; la revisione del nucleo, voce 1): lo spostamento e' `exp(i theta (I - 2P)/2)`, cioe' la forma qui sopra a `theta/2`, DUE VOLTE, poi `conj(z)` (`z = e^{i theta}` a `theta/2`, per arco): in aritmetica esatta `e^{-i theta/2}` per la forma di prima, la STESSA legge per una fase, e lo zero dell'energia che la MAPPA chiama <<quello fisico>>. ### E' cio' che OGNI corsa dell'era 2 faceva gia' in memoria (`_zero_simmetrico`): `flussi_parziali.hop_psi` fa le stesse operazioni nello stesso ordine, e il braccio 0 lo prova AL BIT. ### A `theta = pi` NON torna piu' il pezzo di prima AL BIT: torna `-i` volte quello.

