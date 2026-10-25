# LA CURVATURA, PARTE 2 SULLA CARTA: ESISTE UNA LUNGHEZZA CHE NON TOCCA LA MASSA?

> **Il mandato:** di Luca, `2026-10-25` *([[PROGETTO-CURVATURA]], [[LORENTZ-MATERIA-INTERFERENZA]])*, ### **con le due DECISIONI DI LUCA delle `17:27`** *(si registrano col referto)*: ### **`(1)` si accetta la lettura «la deflessione in `A1` non e' `R1`»; non si cerca ora perche' non arriva a `R2`; `(2)` ne' `A2` ne' `(C)` adesso: prima questa parte; `A1` resta come prototipo, col difetto diagnosticato** *(la massa per meta' dall'arco)*.
> ### **SULLA CARTA: il generatore, nessuna corsa di dinamica, nessun file del nucleo; `B-4`, `B-5`, l'impronta `2e7f795d2a52fbe7` intatte.** ### **Lo script `csv/_curvatura_parte2.py`, il referto `doc/referti_l2/curvatura_parte2.{txt,jsonl}`.**

**LIVELLO:** una misura sul generatore.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*. 2. **Il gradino:** ### **`(c)` la struttura di campo debole** *(`H = cs m + cs^3 p^2/2m`)*. 3. **Aggiunge un numero o una legge?** ### **Cerca se una famiglia a due pesi CONTIENE la soluzione: nessuna legge.** 4. **Tocca `c_s`?** ### **Si': come le lunghezze entrano negli angoli.** 5. **Emergente o imposto?** ### **La domanda e' se la soluzione esista; la sua scelta sarebbe di Luca.**

## 1. LE SCELTE *(fissate qui)*

- ### **LA FAMIGLIA:** ### **`H(alpha, beta) = alpha (I - P_u) + beta P_-`** *(il flusso del nodo e quello dello spostamento; `A1` e' `alpha = 1`, `beta = r`)*; ### **con la moneta: `- gamma (eps/pi) somma sigma.n`** *(il blocco `12 x 12` dello spin; `gamma = 1` la moneta fissa, `gamma = alpha` la moneta che scala col nodo: TUTTE E DUE riportate)*.
- ### **GLI ZERI** *(`mu = z - lambda`)*: ### **`Z1 = (alpha + beta)/2`** *(lo scarto `-theta/2` di ogni pezzo: lo zero simmetrico generalizzato)*; ### **`Z2 = 0`** *(lo zero di oggi)*; ### **`Z3` = il punto medio della coppia a `K`** *(lo zero che rende la coppia simmetrica `+-mu0`: se coincide con `Z1`, si dice)*.
- ### **LE MISURE:** ### **`mu0` e `x = sqrt(2 mu0 a)`** *(la curvatura fine di `_curvatura_prototipo.x_di`, `k <= 0.01`)* ### **per la banda di `K` col `mu0 > 0`.** ### **`20` coppie `(alpha, beta)` casuali in `[0.2, 3]`** *(il seme `7`)*.
- ### **LE CONDIZIONI `(c)`:** ### **`mu0 = 1/2` e `x = r/4`;** ### **la soluzione numerica** *(Newton su `(alpha, beta)` dal valore della formula, e un minimo del residuo sulla griglia `alpha, beta` in `[0.05, 4]`, passo `0.01`, dove la formula non da' soluzione)* ### **a `r` in `(0.5, 0.8, 0.9, 0.95, 1.0, 1.05, 1.25, 2.0)`.**
- ### **`P2`, GLI INGRESSI DEL PASSO VERO** *(dal codice, `composizione.ORDINE`)*: ### **sulla carta, nel referto.**

## 2. I CRITERI *(del mandato)*

| | il criterio | il tipo |
|---|---|---|
| `1` | `P0`: `A1` riprodotto entro `1e-8` *(`mu0 = sqrt(1 - r + r^2)/2`, `x = sqrt(r)/4` a `r` `0.5`, `1`, `2`)* | DEVE |
| `2` | a `alpha = beta = 1` il generatore e' quello di oggi al bit *(`_u1_terzo.H_gen`)* | DEVE |
| `3` | le formule `(a)` entro `1e-8` sulle `20` coppie | PUO' FALLIRE |
| `4` | `(c)`: nessuna soluzione per `r > 1` con `Z1` *(`r` `1.05`, `1.25`, `2`)* | PUO' FALLIRE |
| `5` | `(d)`: con `eps 0.5`, sulla soluzione di `(c)`, `mu0` indipendente da `r` entro `1e-6` | PUO' FALLIRE |
| `6` | `A1` soddisfa le due condizioni | ### **DEVE FALLIRE, la chiave: `mu0` a `r 2` = `0.866`, non `0.5`** |

## 3. TODO

1. questo task history, da solo; 2. lo script, prima dei numeri; 3. la corsa; 4. il referto, le decisioni di Luca nell'indice e nella relazione.
