# 2026-11-05 — LA SCANSIONE IN DIMENSIONE *(Luca `2026-11-04` `20:18`-`22:26`, la domanda centrale; IN ATTESA)* -- **LA PROPOSTA, FERMO: NESSUNA CORSA SENZA LA DECISIONE DI LUCA**

> **La domanda centrale** *(la voce `40` della mappa)*: **a quale scala di lunghezza la simmetria discreta del reticolo (`D6`) lascia il posto a una simmetria continua?** Se quella scala coincide con la dimensione del solitone, il modello descrive un piccolo cristallo, non uno spazio continuo. **La richiesta:** proporre come variare la dimensione del solitone **a parita' di tutto il resto**, quali dimensioni, col bordo di `TB3`, il costo e lo spazio.

## 1. LE PREMESSE DAL CODICE
- ### **LA DIMENSIONE NON E' UN PARAMETRO DA GIRARE:** la partenza *(`protetto.partenza`, `"BG"`)* e' **l'inviluppo di `pK`** -- **lo stato di `A` a `K` della scena** *(`V.scena`, costruito alla norma `N = 1e6`)* -- per lo spinore della scelta migliore, normalizzato a `N` *(`protetto.inviluppo`)*. **La larghezza viene dalla scena** *(`rec["larghezza"]`)*: **a `N` fissato, il solitone ha la sua dimensione.**
- **Cosa sappiamo gia':** **lo spessore del bordo `4.79` nodi** *(`forma_solitone.txt`)*; **la dispersione della banda `B` isotropa entro lo `0.1%` sopra `3.25` nodi** *(`omega`)* **e `6.09`** *(`|v_g|`)* *(`isotropia_dispersione.txt`)*; l'esagonalita' di `TB3` `0.46%`-`1.33%` secondo la soglia.
- **Cosa NON so:** **come la larghezza della scena dipende da `N`** *(per un solitone non lineare di solito la larghezza cala con la norma; qui non e' misurato)*; se una scena a un altro `N` passa i controlli della scena di oggi *(`BG-F-0.15`: `mu`, `w_in`, la scelta della coppia)*.

## 2. LA PROPOSTA *(FERMO)*
1. ### **PRIMA, UNA CARTA STATICA, NESSUNA CORSA:** la scena a **`N` = `2.5e5`, `5e5`, `1e6`, `2e6`, `4e6`** *(un fattore `2` fra l'una e l'altra)*: **la larghezza `w`, lo spessore del bordo e l'esagonalita' della partenza** *(la carta della forma sulla densita' a `t 0`)*. **Decide le dimensioni:** le `N` che danno `w` da `~0.5` a `~2` volte quella di oggi.
2. **La via scartata, dichiarata:** **stirare l'inviluppo** di un fattore a `N` fisso **non da' uno stato della scena** *(la partenza rilasserebbe, e la forma misurata sarebbe quella del transitorio)*.
3. **Poi le corse, col bordo di `TB3`** *(`g_max 0.03`, la tabella `c(t)`)*: **una per dimensione** *(`3`-`4`)*, **con le mappe**; **`L` piu' grande se serve** *(il solitone deve stare a `R_A - 3 w >= ~8` nodi dalla fascia, come in `TB3`: per `w` doppio, `L ~160`, `~3.9` volte il costo)*; **`R_A` scalato con `w`** *(o fisso? decide Luca)*.
4. **La misura:** **l'esagonalita' e lo spessore del bordo contro la dimensione**, accanto alla lunghezza d'onda dell'anisotropia *(`isotropia_dispersione.txt`)*: **se l'esagonalita' cala quando il bordo si allarga oltre `~6` nodi**, la forma segue la dispersione; **se no, la forma e' del reticolo a ogni scala provata.**
- **Il costo:** la carta statica, minuti; **le corse `~5.5` ore l'una su `L 81`** *(come `TB3`)*, **`~3.9` volte su `L 160`**; lo spazio come `TB3` *(`~91` MB di mappe su `E:` per corsa su `L 81`, `~3.9` volte su `L 160`)*. **Il numero vero dal primo pezzo.**

## 3. LE DOMANDE A LUCA
1. **La via: la norma `N`** *(e la carta statica prima)*?
2. **Le `N`** *(`2.5e5` .. `4e6`)* e **`R_A` scalato o fisso**.
3. **Le corse** *(quante, con quale `L`)*, dopo la carta statica.

## 4. LA DECISIONE DI LUCA *(`2026-11-05` `15:28`; non mia)*
- **Si' alla carta STATICA:** la dimensione del solitone della scena a `N` da `2.5e5` a `4e6`, **nessuna evoluzione**.
- **Le corse per dimensione: dopo la carta, decide Luca.**
- **Nella coda:** fra una corsa e l'altra, dopo il pilota di `TL120`, insieme alla carta statica della dispersione del vuoto *(la voce `4`)*.
