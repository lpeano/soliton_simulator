# LE BANDE PIATTE: IL MENU PER LA DECISIONE *([[PIANO-2D-3D]], [[PROGETTO-MASSA-COLLETTIVA]]; il mandato di Luca delle `19:12` del `2026-10-29`)*

> **Il documento NON sceglie: la decisione fra `(A)`, `(B)`, `(C)` e' di Luca.**
> **I numeri:** `doc/referti_l2/bande_piatte.txt` *(`python csv/_bande_piatte.py --referto`, lo script `sha1-BYTE 3d62588b`, `919b610a`; `5/5`)*; il task history `doc/TASK_HISTORY/2026-10-29_bande_piatte_menu.md` *(`c4fe2712`)*.
> **Il quadro:** il tick libero di `S1`, `L 81`, la convenzione `simm` degli strumenti; le energie per unita' di tempo, `-arg(lambda)/s`; `s 0.15` dove non e' detto.

## 0. DA DOVE SI PARTE *(`99b679bc`)*

- Il modo instabile del solitone di `S1` decade in coppia `P0 + Ppi`; il tasso dipende dalla **somma** degli spostamenti delle due piatte *(in direzioni opposte resta `0.1506`)*; nella stessa direzione il modo si spegne fra lo scarto `-0.1` e `-0.4` e fra `+0.4` e `+1.6`; una piatta sola a `+0.8` lo spegne.
- **Un fatto del codice che vale per tutto il filone:** in tutte le scene di `S1` misurate fin qui **`eps = 0`** *(`_solitone_vuoto_congelato.corsa`)*: **la moneta di spin e' spenta**, mentre la tabella ha `eps 0.5`.

## 1. IL PUNTO DI MEZZO: NON E' UNA SIMMETRIA

**Il tick libero della materia** *(dal codice: `composizione.ORDINE`, i pezzi della materia, a `eps 0` la moneta e' l'identita' e il legame lo e' a `rho -> 0`)* e' `T = G S S G`, coi mezzi pezzi `G = exp(-i s (alpha/4)(2 P_u - I))` e `S = exp(-i s (beta/4) R_S)`; **oggi `alpha = beta = pi`.** Il tick ricomposto dai pezzi ridà `A(k)` entro `9.0e-16`.

**Al primo ordine in `s`**, `H1 = (alpha/2)(2 P_u - I) + (beta/2) R_S`:

| che cosa | la formula | misurato *(lo scarto dal primo ordine)* |
|---|---|---|
| `P0`, `Ppi` *(su `ker P_u`)* | `(-alpha ± beta)/2` = `0`, `-pi` | piatte **esatte a ogni `s`**: `7.3e-15`, `7.5e-15` |
| `A`, `B` *(su `span(u, R_S u)`)* | `∓(1/2) sqrt(alpha^2 + 2 alpha beta c(k) + beta^2)` | `4.6e-02`, `1.1e-02`, `2.8e-03` a `s 0.3`, `0.15`, `0.075`: i rapporti `4.07`, `4.02` **(`s^2`)** |
| `c(k)` | l'autovalore di `P_u R_S P_u` | in `[-1/2, 1]`; **`c(K) = c(K') = -1/2`** *(il minimo)*; le due componenti di spin uguali |

**Il punto di mezzo, dalla formula:** `E_A(K) = -mu0`, `mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)`; il mezzo fra le piatte e' `-alpha/2`. **Coincidono se e solo se `beta = alpha`** *(`r = beta/alpha = 1`: il `dtau` dell'arco uguale a quello del nodo)*. Quindi il punto di mezzo e' **`r = 1` piu' `c(K) = -1/2`** *(la geometria del triangolo)*; **il palindromo** rende lo scarto di ordine `s^2` *(`de411167`)*.

**Le prove di simmetria dello spettro** *(a tutte e tre le `s`)*:

| la prova | lo scarto massimo |
|---|---|
| `E(k) = E(-k)` | `≤ 1.9e-14` **(vale)** |
| `E -> -E` senza `Ppi`; `A(k) = -B(k)` | `≤ 1.6e-14` **(vale)**: `A` e `B` speculari rispetto a `P0` |
| `E -> -E` con `Ppi`; `E -> -pi - E` *(stesso `k` e `k -> -k`)* | `3.14` **(non vale)** |

**La conseguenza per la risonanza:** lo scarto libero `E_P0 + E_Ppi - 2 E_A(K) = -alpha + 2 mu0` e' **zero al primo ordine a `r = 1`**: due quanti di `A` a `K` stanno esattamente sulla soglia della coppia `P0 + Ppi`. Misurato: `-0.0884`, `-0.0219`, `-0.0055` a `s 0.3`, `0.15`, `0.075` *(`O(s^2)`)*, uguale a `K` e a `K'`.

## 2. CHE COSA TOCCA

| la grandezza | dipende dal punto `1`? | il fatto |
|---|---|---|
| **`Q_S`** e la moneta `eps` | **no** | `[T, sigma_z] = 0` esatto a `eps 0`; `1.46e-1` a `eps 0.5` *(misurato qui; `doc/PROGETTO_U1.md`: `3.2e-15` e `6.3e-2` col tick intero)*. `Q_S` dipende da `eps` e dalla `U` diagonale, non da `r` |
| **la coppia `K`/`K'`** | **si', allo stesso modo** | `c(K) = c(K') = -1/2`; `A(K) = A(K')`; `E(k) = E(-k)`: le due valli hanno lo stesso punto di mezzo e la stessa soglia |
| **`DOMANDA-CHIRALITA`** | **il candidato `(b)` si'** | `(b)` e' il salto della coppia a `K`, `mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)` *(`2026-10-25_curvatura_parte2.md`)*: **e' la stessa grandezza** che con `r = 1` mette `A(K)` a meta'. `(a)` *(la moneta)* e' la strada `(B2)`; `(c)` *(le valli)* sta in `c(k)`, cioe' nella geometria |
| **il cono di luce di `C2`** | **si', attraverso `r`** | il rapporto fra la `c` della materia e quella della luce in `A1` e' `pi/(4 sqrt(r))` *(`b0edae62`)*; la materia nuda a `r = 1` va a `pi/4` della luce *([[DOMANDA-CONO-EMERGENTE]])* |

## 3. LE PIATTE HANNO STATI COMPATTI

| la piatta | il grappolo minimo | gli stati | le traslazioni *(gli stati di due anelli, `19` nodi)* | il proiettore |
|---|---|---|---|---|
| **`P0`** *(isolata: `A` e `B` a distanza `≥ 1.56`)* | **il triangolo, `3` nodi** | `2` *(uno per spin)* | rango **`4` a ogni `k`** | **esiste locale** *(analitico in `k`: decade esponenzialmente; non compatto)* |
| **`Ppi`** *(tocca `A` a `Gamma`)* | **il triangolo, `3` nodi** | `4` | rango `4` a ogni `k` **tranne `Gamma`** *(`2`)* | **non locale da sola:** a `Gamma` mancano `2` stati, quelli dove tocca `A` |

*(Ogni stato trovato soddisfa `T v = lambda v` entro `1.7e-15`; un nodo solo non ne porta nessuno.)*

## 4. LE TRE STRADE, CON IL COSTO *(il documento NON sceglie)*

### (A) TENERLE COME FISICA

- **Che cosa vuol dire:** il modello ha `8` bande piatte su `12`; il solitone fermo e' instabile per il decadimento in coppia, e **il solitone stabile e' lo stato che respira** *(la lista d'attesa `13`: due corse da stati diversi finiscono nello stesso stato largo)*.
- **Il costo:** nessuna legge cambia; **la soglia e' nel modello a `r = 1`**, quindi **ogni oggetto con un livello vicino a `A(K)` vi e' esposto**. La domanda `13` *(lo stato finale comune)* diventa il lavoro.

### (B) ALLONTANARLE ALLA WILSON *(sul tick libero ricomposto in `csv/`)*

| la modifica | lo scarto libero a `K` | `A(K)` | il costo nel punto `2` |
|---|---|---|---|
| **(B1) il rapporto nodo/arco**, `mu0 = pi/2` fisso: `alpha 2.3416`, `beta 3.5702` *(`r 1.5247`)* | **`+0.806`** | `-3.1e-03`; la curvatura di `A` a `K` da `-3.14e-3` a `-2.66e-3` | **un numero nuovo** *(`A1`: `r` non derivato; la somma delle frazioni di una legge non e' piu' `1`)*; il cono *(`pi/(4 sqrt r)`)* cambia con `r`; `mu0` di `(b)` resta `pi/2` per costruzione, ma `alpha` e `beta` cambiano; `Q_S` e le valli intatti |
| idem, `alpha 3.5416`, `beta 2.4508` *(`r 0.6920`)* | **`-0.395`** | `-2.5e-03`; curvatura `-2.76e-3` | idem |
| **(B2) la moneta della tabella**, `eps 0.5` | `+0.161` *(non arriva a `+0.8`)* | **`-7.96e-02`** *(si muove `A`, non la somma delle piatte)* | `Q_S` rotta *(`1.46e-1`)*; le piatte quasi piatte *(larghezze `0.0017`, `0.0029`)*; e' il candidato `(a)` della chiralita' |
| **(B3) un altro ordine palindromo** *(`S G G S`)* | **`0`** *(`< 1e-14`, a `s 0.15` e `0.075`)* | `0` | nessuno, **e non sposta niente:** con due soli pezzi ogni ordine palindromo e' una rotazione ciclica, cioe' lo stesso spettro |
| **(B4) la convenzione** *(`oggi` contro `simm`)* | **`0`** | sposta tutto di `-pi` | nessuno, **e non sposta niente:** una fase globale per pezzo |

- **Quante modifiche minime esistono:** **una famiglia sola, `(B1)`**, che sposta la somma delle piatte di `+0.8` o `-0.4` tenendo `A(K)` entro `3e-3`. `(B2)` sposta soprattutto `A`; `(B3)` e `(B4)` non spostano niente.
- **Il costo di `(B1)`:** un numero *(`r != 1`)* da derivare; tocca il cono di `C2` e il candidato `(b)` della chiralita'; non tocca `Q_S` ne' le valli.

### (C) CAMBIARE IL LEGAME SULLE PIATTE, RESTANDO LOCALE

- **Il fatto del punto `3`:** `P0` ha stati compatti su un triangolo che generano tutta la banda, quindi **un proiettore locale** *(esponenziale, non compatto)*; `Ppi` no, a `Gamma`.
- **La forma, se Luca la sceglie:** il legame `exp(-i alpha(rho/Lambda) dtau)` che sulle componenti `P0` agisce con una fase diversa. **Basta una piatta:** il tasso dipende dalla somma *(`99b679bc`: `P0` sola a `+0.8` spegne il modo)*.
- **Il costo:** una legge nuova *(9-ter: una cura che aggiunge una legge deve dire perche' non si poteva togliere niente)*; **un proiettore a coda esponenziale non e' compatto** *(la scala minima e' un arco, `A13`)*; su `Ppi` la stessa forma non e' locale.
