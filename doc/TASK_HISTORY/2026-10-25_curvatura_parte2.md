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

## 4. IL RISULTATO *(dopo `519c391f`)*

### **IL REFERTO DELLA PARTE `2`:** `doc/referti_l2/curvatura_parte2.{txt,jsonl}` *(`csv/_curvatura_parte2.py` `sha1-BYTE e2282e17` al commit `519c391f`; il task history `cd7aa992`)*. ### **`6/6`.**

- ### **I CONTROLLI:** ### **a `alpha = beta = 1` il generatore e' `_u1_terzo.H_gen` AL BIT; `A1` riprodotto entro `1.7e-10`** *(`mu0` `0.4330127019`, `0.5`, `0.8660254038`; `x` `0.1767766955`, `0.2500000002`, `0.3535533906` a `r` `0.5`, `1`, `2`)*.
- ### **`P1 (a)`: LE FORMULE DEL GUARDIANO TENGONO entro `1.7e-10` su `20` coppie casuali:** ### **`mu0 = (1/2) sqrt(alpha^2 - alpha beta + beta^2)`, `x^2 = alpha beta/16`** *(lo zero `Z1 = (alpha + beta)/2`)*.
- ### **`P1 (b)`, GLI ZERI:** ### **`Z3`** *(il punto medio della coppia a `K`)* ### **COINCIDE con `Z1` entro `1.6e-15` a ogni coppia: lo zero che rende la coppia simmetrica E' `(alpha + beta)/2`;** ### **con `Z2`** *(lo zero di oggi)* ### **la coppia non e' simmetrica** *(`mu0` `-0.36`, `-1.09` a `alpha 0.80`, `beta 0.65`)* ### **e un membro non ha `x` reale** *(`x^2 < 0`)*; ### **la ricerca grossa** *(passo `0.2`)* ### **non trova una soluzione con `Z2`** *(il residuo minimo `1.2e-2` a `r 0.9`, `2.9e-2` a `r 1.25`)*; ### **quella con `Z3` e' la stessa di `Z1`** *(la griglia grossa da' `5.5e-4` a `r 0.9`: e' la risoluzione della griglia, la soluzione di `Z1` sta fra due punti)*.
- ### **`P1 (c)`, LE DUE CONDIZIONI con `Z1`:** ### **la soluzione `alpha, beta = [sqrt(1 + 3 r^2) +- sqrt(1 - r^2)]/2` VERIFICATA sul generatore a `r` `0.5`, `0.8`, `0.9`, `0.95`, `0.99`, `1`** *(`mu0 = 0.5000000000`, `x = r/4` entro `2e-10`)*: ### **a `r 0.9` il ramo `+` e' `alpha 1.14396`, `beta 0.70807`, il ramo `-` lo scambio;** ### **PER `r > 1` NESSUNA soluzione reale** *(`(alpha - beta)^2 = 1 - r^2 < 0`; il residuo minimo sulla griglia `1.25e-4` a `r 1.05`, `3.1e-3` a `1.25`, `5.0e-2` a `2`)*. ### **QUALE RAMO E' CONTINUO CON OGGI:** ### **TUTTI E DUE arrivano a `(1, 1)` a `r = 1`, con un punto di diramazione a radice** *(`sqrt(1 - r^2)`: la derivata in `r` diverge a `r = 1`)*: ### **nessuno dei due e' liscio attraverso `r = 1`, e nessuno e' preferito dalla continuita'.**
- ### **`P1 (d)`, LA MONETA** *(`eps 0.5`, sul ramo `+`)*: ### **con la moneta FISSA** *(`gamma = 1`)* ### **i livelli della coppia sono `+-0.52471925` a ogni `r`: indipendenti da `r` entro `1.6e-15`** *(PUO' FALLIRE: PASSA)*; ### **con la moneta che scala col nodo** *(`gamma = alpha`)* ### **variano di `8.0e-3`.**
- ### **LA CHIAVE:** ### **`A1` ha `mu0 = 0.866025` a `r 2`, non `0.5`** *(DEVE FALLIRE: PASSA)*.

### **`P2`, GLI INGRESSI DELLA LUNGHEZZA NEL PASSO VERO** *(dal codice: `composizione.ORDINE`, `14` pezzi; sulla carta)*:

| il pezzo *(due volte, a `0.5`)* | dove agisce | e' un flusso di proiettore? | sul generatore |
|---|---|---|---|
| `CAMM-GROVER` | il nodo | si' *(`P_u`)* | ### **`alpha`** |
| `CAMM-SPOSTAMENTO` | l'arco | si' *(`P_-`)* | ### **`beta`** |
| `CAMM-MONETA-SPIN` | l'estremita' *(il nodo)* | si' *(`sigma.n = 2 P_n - I`)* | ### **un TERZO peso `gamma`, fuori da `(alpha, beta)`** *(la `(d)`)* |
| le due meta' del palindromo separate | -- | -- | ### **a `s -> 0` conta solo la SOMMA** *(Lie-Trotter)*: ### **le differenze entrano a `O(s^2)`, non nelle condizioni** |
| `CAMM-GROVER-VUOTO`, `CAMM-SPOSTAMENTO-VUOTO` | il vuoto | si' | ### **una coppia `(alpha_v, beta_v)` del VUOTO, disaccoppiata dalla materia al primo ordine** *(entra attraverso il legame)* |
| `CAMM-MATERIA-VUOTO` | il nodo | ### **NO: una fase che dipende da `rho` e `Lambda`, non lineare** | fuori dalla famiglia *(e fuori dalla camminata degli strumenti dei triangoli)* |
| `CAMM-FASE-VUOTO` | il vuoto | spento *(`lambda_c = None`)* | -- |

### **IL TERZO PESO, `gamma` della moneta:** ### **la `(d)` dice che la moneta FISSA non rompe `mu0`; LE CONDIZIONI `(c)` CON `gamma` LIBERO** *(se aprono `r > 1`)* ### **NON le ho rifatte** *(servirebbe la curvatura del blocco `12 x 12`: un mandato a se', dichiarato)*.

### **`P3`, LA LETTURA** *(informazione per Luca, non scelte)*: ### **la soluzione esiste solo per `r = cs/cs_rif <= 1`:** ### **con `cs_rif` = il vuoto imperturbato** *(la scelta di prova delle `16:26`)* ### **e `cs = Lambda/(Lambda + Lambda_c)`** *(la materia consuma il vuoto: `cs` piu' basso vicino alla materia)*, ### **`r <= 1` vale OVUNQUE ci sia materia, e il vuoto imperturbato e' il massimo di `cs`;** ### **ma dove il vuoto fosse piu' denso del riferimento** *(un'onda di `cs`, una zona senza materia sopra il fondo)* ### **`r > 1` e la famiglia non ha soluzione:** ### **la condizione `r <= 1` diventerebbe un VINCOLO su `cs_rif`** *(il massimo di `cs` possibile, come `B-5` per `s`)*.
