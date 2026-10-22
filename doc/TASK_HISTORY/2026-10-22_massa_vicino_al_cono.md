# LA MASSA DELLA CAMMINATA VICINO AL CONO: `Delta` IN FUNZIONE DI `s` FRA `0.5` E `1`, E LA PROVA CHE CONTA SOLO `s`

> **Il mandato:** decisione di Luca del `2026-10-22` alle `21:26`, dopo `7fc47558`. ### **MISURE: `leggi.yaml` e l'impronta INTATTI; nessuna regola di
> scala cambiata.**

**LIVELLO:** `L2`, misure.

## 0. LA STELLA POLARE

1. **`A14`:** non si applica *(nessuna legge cambia)*.
2. **Il gradino:** `(a)` ### **a `s = 1` la camminata di Grover discreta** *(il cono, `7fc47558`)*; `(b)` ### **`cs` messo a mano, uniforme**; `(c)` ### **il
   cono di Dirac della camminata di Grover** *(il limite noto)*.
3. **Aggiunge un numero o una legge?** ### **No:** `dtau` e `cs` SOLO nella scena.
4. **Tocca `rho`, `c_s` o il segno?** ### **`cs` SI'**, ed e' la domanda: ### **la massa dipende da `cs` attraverso `s`?**
5. **Emergente o imposto?** ### **Misurato.**

## 1. ⛔ L'ERRORE `n.36` DEL GUARDIANO *(dal mandato)*

### **Nel mandato delle `20:03` il controllo «`c = 0.3882` a lato `64`, `dtau 0.125`» era sbagliato**: ### **quel valore e' a `dtau 0.0625`** *(`82b40ca1`)*. ###
*(`7fc47558` l'aveva committato come fallito, e mostrato `0.3882` alla riga giusta.)*

## 2. L'IPOTESI, LA PREVISIONE, IL METODO

- ### **L'IPOTESI DEL GUARDIANO** *(non verificata)*: ### **`s = dtau cs / dtau_rif` contiene `cs`**; ### **se la massa dipende da quanto `s` e' lontano da `1`**
  *(a `s = 1` sparisce, `7fc47558`)*, ### **allora la massa dipende dalla velocita' della luce locale** -- ### **l'idea di Luca «`cs` governa la massa».**
- ### ⭐ **LA PREVISIONE, A MANO** *(MIA)*: ### **a `s = 1` la camminata e' la camminata di Grover discreta, con un CONO** *(un punto di Dirac a `k = 0`)*; ###
  **allontanarsi da `s = 1` e' una perturbazione `delta = 1 - s` degli angoli** *(il Grover e lo scambio a `pi s`)*, ### **e un punto di Dirac generico si apre
  LINEARMENTE nella perturbazione**: ### **`Delta ~ (1 - s)^p` con `p = 1`.** ### ⚠ **L'incertezza, dichiarata:** ### **se una simmetria cancella il termine
  lineare, `p = 2`** *(il salto al secondo ordine)*; ### **non ho fatto il conto della simmetria.** ### **E `Delta` per unita' di tempo e' la fase per tick
  divisa per `dtau = s`: vicino a `1` la divisione non cambia l'esponente.**
- ### **IL METODO** *(il problema di `7fc47558`: a `s 0.5` «i rami si avvolgono»)*: ### **le fasi PER TICK** *(`-angle(lambda)`, prima di dividere per `dtau`)*;
  ### **i rami SEGUITI PER CONTINUITA' in `k`** *(lungo `(m, 0)`: a ogni passo il ramo di `k + 1` e' quello col vettore proprio piu' sovrapposto a quello di `k`)*;
  ### **le fasi di un ramo SROTOLATE** *(`np.unwrap`)*. ### **`Delta`, `v`: il fit `phi_b(k) - phi_b(0) = sqrt(Dt^2 + vt^2 k^2) - Dt`** *(per tick, `k <= 0.25 pi`)*,
  ### **`Delta = Dt / dtau`**; la pendenza a `k` piccolo `v_g(1)`; `c = v_g(1)/k(1)`. ### **Il settore della materia; i rami dispersivi** *(`|v_g|` massimo `> 0.1`
  per tick, dichiarato)*. ### **Se a qualche `s` il fit resta impossibile** *(scarto oltre `5%`)*, ### **lo si dice e non si legge.**
- ### **LA MISURA 2, `cs` A MANO:** ### **`mot.cs` = un vettore UNIFORME** *(non `accendi_cs`: niente `Lambda_c`, quindi la fase del vuoto resta spenta)*, ###
  **`dtau_nodo = dtau * cs`**. ### ⚠ **Che cosa la prova vede:** ### **ogni pezzo che usasse `mot.dtau` invece di `dtau_nodo`** *(per esempio la moneta)* ### **farebbe
  differire le due coppie.** ### **`eps 0.5` e `eps 0`.**

## 3. LE LETTURE *(copiate dal mandato)*

- ### **LA MASSA SI SPEGNE AL CONO** se `Delta` ### **decresce monotono** con `s` e ### **va a zero a `s = 1`** *(entro la risoluzione)*; ### **il fit `Delta ~ (1 - s)^p`
  fra `0.8` e `0.99`**, `p` stampato e confrontato con la previsione.
- ### **CONTA SOLO `s`** se le fasi per tick ### **coincidono entro `1e-10` per ogni coppia** della misura `2`: ### **allora la massa dipende da `cs` attraverso `s`.**
- ### **Le stesse letture a lato `32` e `64`** *(entro `1%`)*.

## 4. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_massa_vicino_al_cono.py`: commit, corsa, referto, la relazione con ### **UNA domanda** *(la regola di scala, alla luce di `Delta(s)`)*. ### **NESSUNA REGOLA
   CAMBIATA.**
