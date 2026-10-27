# LA TORSIONE DEL VUOTO NELLA SUA FORMA D'ENERGIA *(la risposta di Luca delle `16:58` a `76e85c0a`, punto `1`)*

> **Il mandato:** ### **la misura in FASE non e' leggibile** *(`76e85c0a`: gli incrementi per tick fino a `pi`)*; ### **la STESSA ipotesi si misura nella sua forma d'ENERGIA:** ### **per ogni arco la somma nel tempo della differenza dell'energia del vuoto ai due capi** *(`_energia_del_legame.per_nodo`)*, ### **divisa per l'unita' che fa della somma una fase** *(da DICHIARARE)*, ### **sulle stesse corse** *(`N 1e5` `L 48`, `N 1e6` `L 81`, lo zero simmetrico, `2000` tick; `cs` spento: il punto fisso con `cs` acceso e' [[PUNTO-FISSO-CS-SOLITONE]], messo da parte)*. ### **Il primo arco a `2 pi` = il primo in cui la somma arriva a `2 pi`.** *([[TORSIONE-DEL-VUOTO]], [[PROGETTO-MITOSI]])*
> ### **L'AVVERTENZA, da scrivere nel referto:** ### **la fase gira come l'energia solo per uno stato a energia definita; per un vuoto disturbato e' un'approssimazione, e la misura in fase non leggibile non e' una smentita dell'ipotesi.**

**LIVELLO:** una misura.

## 0. LA STELLA POLARE

1. **`A14`:** ### **l'energia contata per nodo, sommata nel tempo.** 2. **Il gradino:** ### **dove la mitosi scatterebbe, nella forma che si puo' leggere.** 3. **Aggiunge un numero o una legge?** ### **No: l'unita' e' quella del tick** *(`s`)*, ### **e `2 pi` e' la soglia dell'era `1`, solo LETTA.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Si misura.**

## 1. L'UNITA', DICHIARATA

- ### **Uno stato a energia definita `E` per unita' di norma gira di `-s E` per tick** *(`74f99039`: `fasi.append(-np.angle(a1/a0))`; la decomposizione `762cb0e8`: `Delta e = -Delta arg / s`)*. ### **Quindi l'energia per unita' di norma del vuoto al nodo `k`:** ### **`eps_k = (e_v(k) + 2 pi lambda Lambda_k)/Lambda_k`** *(`e_v` = `_energia_del_legame.per_nodo(..., "psi_h")`, la materia a zero; `Lambda_k` la densita' del vuoto del nodo; `2 pi lambda` lo spostamento dello zero, `0fb93b8c`)*, ### **e la torsione in forma d'energia dell'arco `a` fra i nodi `i = inc.nodo[2a]`, `j = inc.nodo[2a+1]`:**
  ### **`theta_E(a, t) = -s sum_{t' < t} (eps_i(t') - eps_j(t'))`** *(radianti)*. ### **Lo spostamento dello zero si cancella nella differenza.**
- ### **LA LETTURA CHE CONTROLLA L'UNITA'** *(`u`)*: ### **sul vuoto uniforme senza materia** *(un autostato del tick, `d999cca7`)* ### **la fase misurata per tick di un'estremita' contro `-s eps`:** ### **il rapporto, stampato** *(una lettura: il passo e' un prodotto di pezzi, e l'uguaglianza vale al primo ordine in `s`; non so a quale precisione)*.

## 2. CHE COSA CREDO, E CHE COSA NON SO

- ### **Credo:** ### **sul vuoto uniforme `eps` e' lo stesso a ogni nodo, e la somma resta `0` al bit** *(ogni nodo ha grado `6` e somma gli stessi termini)*. ### **Col solitone `eps` cambia dove il vuoto e' disturbato: il ritmo e' massimo sul bordo** *(la fase in `76e85c0a` era sul bordo a `60` tick)*. ### **Se cala con la distanza: NON SO** *(dopo la rottura il gas disturba tutto il toro)*.
- ### ⚠ **NON SO** ### **se `Lambda_k` va vicino a zero sotto il solitone** *(in `76e85c0a` `|z|` scendeva a `1.5e-5`)*: ### **allora `eps_k` e' un rapporto fra piccoli.** ### **Stampo il minimo di `Lambda_k` nel tempo.**
- ### ⚠ **IL COSTO:** ### **`per_nodo` a OGNI tick** *(la somma nel tempo la vuole)*; ### **lo misuro nella prova di costruzione.**

## 3. LA PROGETTAZIONE *(le letture fissate qui, prima dei numeri)*

1. ### **LE SCENE:** ### **`_energia_del_legame.stato`, `fattore 12`, `S1`, lo zero simmetrico** *(`BE.conv(0.5)`)*, ### **`tick.percorri_tick`** *(il tick intero, `cs` spento)*, ### **`2000` tick.**
2. ### **IL RITMO dell'arco: `omega_a = |theta_E(a, T_MAX)|/T_MAX`;** ### **`r_a` la media delle distanze dei due nodi** *(come `76e85c0a`)*; ### **`VICINO` = `r_a <= 2 w_in`.** ### **I GUSCI: `[2 w_in, 4 w_in)`, `[4 w_in, 8 w_in)`, `>= 8 w_in`.**
3. ### **IL FRENO: la media di `|omega|` per finestra di `250` tick** *(`(theta_E(t+250) - theta_E(t))/250`)*, ### **in tutto il toro e in `VICINO`.**

| | il criterio | il tipo |
|---|---|---|
| `0` | ### **il vuoto UNIFORME senza materia** *(la scena di `N 1e5` con la materia a zero, `2000` tick)*: ### **`max |theta_E| = 0` al bit** | DEVE |
| `1` | ### **il ritmo e' MASSIMO vicino al solitone E CALA con la distanza:** ### **la classe di distanza** *(larga `1`)* ### **con la media di `omega` piu' alta sta in `VICINO`,** ### **E le medie dei tre gusci decrescono** *(a ogni `N`)* | PUO' FALLIRE |

- ### **LE LETTURE** *(nessuna soglia)*: ### **`(u)` il controllo dell'unita';** ### **il primo arco e il primo tick in cui `|theta_E| >= 2 pi`, quanti a `T_MAX`;** ### **il freno: costante, calante o crescente;** ### **il ritmo per classe di distanza;** ### **il minimo di `Lambda_k`.**

### **Mi FERMO** ### **se `0` fallisce.**

## 3-bis. ANNOTAZIONE, PRIMA DELLA CORSA *(la prova di costruzione a `60` tick, `N 1e5`: NON il referto)*

- ### ⛔ **UN MIO ERRORE, TROVATO DALLA LETTURA `(u)`:** ### **`_triangoli_bassa_energia.conv` prende il NOME della convenzione** *(`"simm"` o `"oggi"`)*, ### **e io gli passavo `0.5`: con un numero da' la convenzione di OGGI** *(`nullcontext`)*. ### **Quindi la prova girava con lo zero di oggi, e la fase del vuoto uniforme era `0` contro `-s eps = -0.9425`.** ### **Con `conv("simm")` la fase per tick del vuoto uniforme e' `-0.942477796077` = `-s (e_v/Lambda + pi)` alle `12` cifre:** ### **l'unita' torna** *(una prova in memoria; e' la COSTANTE, che si cancella nelle differenze: non prova la scala delle differenze)*. ### **Lo stesso errore e' nella torsione in FASE** *(`e4a4291a`, `8a518049`: i referti `76e85c0a` e `9a8f9afa` sono allo zero di OGGI)*: ### **corretto nei due script, e la fase si rifa.**
- ### ⚠ **I NUMERI GIA' VISTI** *(allo zero di oggi, `60` tick)*: ### **il controllo `0` passa;** ### **la classe di ritmo massimo `[7, 8)` contro il bordo di `VICINO` `7.61`: la classe STRADDLA il bordo,** ### **e il criterio la conta FUORI** *(conta solo le classi tutte dentro)*. ### **Il criterio NON cambia** *(l'ho visto prima della corsa: cambiarlo ora sarebbe tararlo sui numeri)*; ### **i gusci `5.1e-2 > 8.0e-4 > 1.1e-6`.**

## 4. TODO

1. questo task history, da solo; 2. lo script `csv/_torsione_energia.py`, committato prima della corsa; 3. la corsa; 4. il referto *(con l'avvertenza)*, la relazione, l'indice (`TORSIONE-DEL-VUOTO`).

## 5. IL RISULTATO

- ### **IL REFERTO:** `doc/referti_l2/torsione_energia.{txt,jsonl}` *(`csv/_torsione_energia.py` `sha1-BYTE 6f51d303`, committato e pulito; lo zero simmetrico vero, `conv("simm")`)*. ### **`1/2`: nessun DEVE fallito; la PUO' FALLIRE di Luca cade a META'.** ### **L'AVVERTENZA di Luca e' stampata nel referto:** ### *«la fase gira come l'energia solo per uno stato a energia definita; per un vuoto disturbato e' un'approssimazione, e la misura in fase non leggibile non e' una smentita dell'ipotesi».*
- ### **I CONTROLLI:** ### **`(0)` il vuoto uniforme senza materia: la somma `0` al bit per `2000` tick: PASSA;** ### **`(u)` l'unita': la fase misurata di un'estremita' in un tick `-0.942477796077` = `-s eps`, il rapporto `1.000000000000`** *(e' la costante: non prova la scala delle differenze)*.
- ### ⭐ **IL RITMO E' MASSIMO SUL BORDO DEL SOLITONE, APPENA FUORI DA `VICINO`, E CALA CON LA DISTANZA:** ### **la classe piu' alta `[8, 9)` a `N 1e5`** *(VICINO `<= 7.61`, `w_in 3.81`)* ### **e `[14, 15)` a `N 1e6`** *(VICINO `<= 13.26`, `w_in 6.63`)*: ### **a `2.1`-`2.2` larghezze, non dentro;** ### **i gusci decrescono a tutte e due le taglie:** ### **`5.04e-2 > 4.90e-2 > 1.75e-2`** *(`N 1e5`; i primi due quasi uguali)* ### **e `5.21e-2 > 2.18e-2 > 8.19e-3`** *(`N 1e6`)*. ### **La PUO' FALLIRE `(1)` FALLISCE per la sua prima meta'** *(il massimo in `VICINO`)*; ### **la seconda** *(cala con la distanza)* ### **regge.**
- ### **IL PRIMO ARCO A `2 pi`:** ### **al tick `15`, a `r 7.50`** *(`N 1e5`)*; ### **al tick `16`, a `r 13.03`, `8` archi insieme** *(`N 1e6`)*: ### **sul bordo, prima della vita** *(`140`, `320`)*. ### **A `T_MAX` ci arrivano `5772` archi su `6912` e `15097` su `19683`.**
- ### ⛔ **IL FRENO NON C'E':** ### **la media del ritmo per finestra di `250` tick CRESCE per tutta la corsa** *(`2.32e-2` -> `8.53e-2` a `N 1e5`; `1.38e-2` -> `6.87e-2` a `N 1e6`; in `VICINO` lo stesso, dopo un calo nella seconda finestra a `N 1e5`)*: ### **dopo la rottura il gas disturba tutto il toro, e la torsione d'energia cresce ovunque.**
- ### **IL MINIMO DI `Lambda` per nodo** *(una lettura, per `eps` come rapporto)*: ### **`1.3e-2` e `9.1e-3`** *(contro `6` del vuoto uniforme)*.
