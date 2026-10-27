# `H_tot` COL LEGAME `S1` NON E' LA QUANTITA' CONSERVATA DEL PASSO: QUANTO PESA SUI RISULTATI DI OGGI, E IL PEZZO DEL LEGAME LETTO NEL CODICE *(la risposta di Luca delle `19:25` a `998203e9`)*

> **Il mandato:** ### **`1` registrare il risultato** *(una voce `ENERGIA-NON-CONSERVATA-S1`, legata a [[LIBRO-DEI-CONTI]] e [[DECISIONE-LINEARE]])* ### **e l'errore del guardiano `n.74`** *(aveva detto che il passo conserva `H_tot` a meno di `O(s^2)`)*; ### **`2` QUANTO PESA: il rapporto fra la deriva cumulata di `H_tot` e gli scambi misurati in `15df5c63`** *(vuoto, cinetica, legame)* ### **alla vita e a `T_MAX`, e alle stesse ore nel libro dei conti** *(la strada `A`)*: ### **sotto il `5%` degli scambi il verso letto** *(il vuoto cede alla materia)* ### **resta;** ### **`3` IL PEZZO DEL LEGAME, LETTO NEL CODICE** *(nessuna corsa)*: ### **la fase sulla materia e' `dE/drho`, e il vuoto riceve la rotazione gemella `dE/dLambda`?** ### **Per `S1` e per `S3`;** ### **se NO, una prova breve col pezzo reso coerente.**

**LIVELLO:** una lettura del codice e una rivalutazione su dati gia' committati.

## 0. LA STELLA POLARE

1. **`A14`:** ### **quale energia il passo conserva.** 2. **Il gradino:** ### **se i versi letti oggi reggono.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Si legge.**

## 1. IL PUNTO `3`, GIA' LETTO *(dichiarato: prima di questo task history; nessuna corsa)*

| la forma | `E_legame` | `dE/drho` | `dE/dLambda` | che cosa applica il codice |
|---|---|---|---|---|
| ### **`S3`** *(il nucleo)* | `rho ln(rho/(rho+Lambda))` | `ln(rho/(rho+Lambda)) + Lambda/(rho+Lambda)` | `-rho/(rho+Lambda)` | ### **`materia_vuoto.alpha` (r.`80`-`91`) e `beta` (r.`94`-`108`): LE STESSE** *(`68ff3ffd`)* |
| ### **`S1`** *(in memoria)* | `Lambda F_1(x)`, `F_1 = x - arctan x`, `x = rho/Lambda` | `F_1'(x) = x^2/(1+x^2)` | `F_1 - x F_1' = x - arctan x - x^3/(1+x^2)` | ### **`_screening_forme_s3._ab` (r.`60`-`61`), che sostituisce `MV.pezzi` in `forma`: LE STESSE** *(`80ffe96c`)* |

- ### **COME SI APPLICANO** *(`materia_vuoto.applica`, r.`139`-`146`)*: ### **`psi <- exp(-i alpha dtau f) psi`, `phi <- exp(-i beta dtau f) phi`, nodo per nodo** *(`rho` e `Lambda` non cambiano durante il pezzo: e' il flusso ESATTO di `E_legame`)*. ### **`CAMM-FASE-VUOTO` a `lambda_c None` non fa niente** *(`energia_pesata.applica`, r.`375`)*.
- ### **QUINDI: IL VUOTO RICEVE LA ROTAZIONE GEMELLA, per `S1` e per `S3`.** ### **La PUO' FALLIRE del guardiano** *(«il pezzo di oggi non da' al vuoto la rotazione gemella»)* ### **FALLISCE;** ### **la prova col pezzo coerente non serve** *(la condizione non c'e')*, ### **e la seconda PUO' FALLIRE** *(col pezzo coerente la deriva cala di un fattore `3`)* ### **NON E' MISURATA.**
- ### **CHE COSA RESTA APERTO:** ### **ogni pezzo e' il flusso esatto della sua energia** *(le fasi esatte; i pezzi della camminata lineari)*, ### **e la composizione e' palindroma:** ### **la teoria dell'errore all'indietro darebbe un'energia modificata conservata vicina a `H_tot` a meno di `O(s^2)`,** ### **ma SOLO se il passo e' piccolo rispetto alle frequenze** *(`s omega << 1`)*. ### **Qui `s 0.3` e lo spettro largo `2 pi`: `s omega ~ 1.9`** *(e `~ 0.9` a `0.15`)*: ### **un'IPOTESI, non una diagnosi: il passo non e' nel regime asintotico, e le risonanze col gas** *(dopo la rottura)* ### **fanno derivare `H_tot`.**

## 2. LA PROGETTAZIONE DEL PUNTO `2` *(lo script `csv/_peso_deriva.py`; nessuna corsa del simulatore)*

1. ### **`15df5c63`** *(`energia_del_legame.jsonl`, lo zero simmetrico, il tick intero; le quattro corse)*: ### **alla vita** *(`vita20`)* ### **e a `T_MAX`, sul totale: `D = |H_tot(t) - H_tot(0)|` e gli scambi `X_p = |E_p(t) - E_p(0)|` per `p` = vuoto, cinetica, legame;** ### **i rapporti `D/X_p`.**
2. ### **IL LIBRO DEI CONTI, la strada `A`** *(`libro_dei_conti.jsonl`, `N 1e5` `L 48`)*: ### **il residuo del toro intero** *(le entrate e le uscite di `H_tot` del toro, cioe' la deriva)* ### **contro i flussi del disco `2 w_in`** *(VICINO)*, ### **fino alla vita e dopo:** ### **il rapporto delle somme dei valori assoluti, e quello dei saldi.**
3. ### **IL CRITERIO DI LUCA** *(fissato da lui, prima dei numeri)*: ### **il verso resta se `D < 5%` di ogni scambio** *(vuoto, cinetica, legame)*, ### **corsa per corsa, alla vita e a `T_MAX`.** ### **E' una LETTURA per corsa** *(il criterio dice dove il verso regge)*.

## 3. TODO

1. questo task history, da solo; 2. lo script, committato prima; 3. la corsa e il referto; 4. la voce `ENERGIA-NON-CONSERVATA-S1`, l'errore `n.74`, la relazione.
