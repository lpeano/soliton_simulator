# `CAMM-MONETA-SPIN`

> ### ⛔ **QUESTA SCHEDA E' GENERATA** da `primo_ordine/leggi/leggi.yaml` *(`primo_ordine/_genera.py`)*: ### **non si modifica a mano.**

| | |
|---|---|
| **tipo** | `pezzo_unitario` |
| **operatore** | `moneta_spin`, azione `estremita` |
| **ambito** | `psi_h` |
| **impronta della riga** | `75bcd40bccb090c7` |
| **assiomi soddisfatti** | `A16` · `A13` |

## I PARAMETRI

> ### ⛔ **`A1`: LA LEGGE, NON IL NUMERO.** Ogni parametro porta ### **il valore E l'origine** — e un numero senza origine e' ### **una manopola.**

| | valore | origine |
|---|--:|---|
| `eps` | `0.5` | ### IL VALORE DEL BANCO, NON UNA TARATURA. `0.5` e' il valore con cui tutte le letture del banco congelato sono state fatte, e il CRITERIO DI PASSAGGIO pretende che il generato riproduca quelle letture: cambiarlo qui vorrebbe dire confrontare DUE ESPERIMENTI. ### La sua origine FISICA resta aperta, ed e' il posto `A1` (il tempo proprio locale): `eps * dtau` e' cio' che conta, e la forma di `dtau` NON e' decisa. |


## LA SCHEDA, dalla tabella

`exp(-i eps dtau sigma.n)` per ESTREMITA' (punto `F1`). E' qui che SPIN e DIREZIONE si legano, ed e' ESATTA e non un'esponenziale numerica: `exp(-i a sigma.n) = cos a I - i sin a (sigma.n)` perche' `(sigma.n)^2 = I` quando `|n| = 1`. ### Quindi nessun errore di troncamento, e la forma e' UNITARIA AL BIT. ### AZIONE `estremita`: agisce su una estremita' per volta, e NON legge il vicino.

