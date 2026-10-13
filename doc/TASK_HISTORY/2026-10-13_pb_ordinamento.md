# `(P-b)` — **IL MECCANISMO DI ORDINAMENTO: la derivazione**

> **Il mandato:** *«Un meccanismo di ordinamento: qualcosa che rinforza localmente il segno
> prevalente (come un magnete sotto la temperatura critica), con leggi `C`-simmetriche.
> Candidato da esaminare, **non da adottare**: la repulsione nodo/antinodo dell'era `1`
> (antifase -> repulsione), tradotta nella logica dell'era `2`. Le forme vanno a Luca.»*

> ### ⛔ **SENZA CODICE.** ### ⚠ **E CONDIZIONATO: tutto questo vale SE il parametro
> d'ordine e' `q_h` e non `N+ - N-`** — che e'
> **`[[DOMANDA-BANDE-O-SEGNO-LOCALE]]`**, aperta. ### **Lo dichiaro qui e non in fondo.**

---

## 1. ⭐⭐ IL PRIMO RISULTATO: `q_h` E' `C`-DISPARI **ESTREMITA' PER ESTREMITA'** — *e lo DERIVO*

### ⛔ **NEL PIANO AVEVO SCRITTO CHE QUESTO ANDAVA MISURATO** *(previsione `b2`: «la
disparita' GLOBALE e' derivata; quella LOCALE no»)*. ### ✅ **Si deriva, e in cinque righe.**

Sia `q_h = Im[ psi_h^dagger (W psi)_h ]`, dove `psi_h` e' lo **spinore** sull'estremita' `h`.
Sotto la `C` completa: `psi -> i sigma_y psi*`, e **misurato** `C W_U = W_{CU} C`
*(`9c46a68`: `0.000e+00`)*. Allora

> `(C psi)_h^dagger (W_{CU} C psi)_h = (i sigma_y psi_h*)^dagger (i sigma_y (W_U psi)_h*)`
> `                                  = psi_h^T (i sigma_y)^dagger (i sigma_y) (W_U psi)_h*`
> ### **`= psi_h^T (W_U psi)_h*`**  *(perche' `i sigma_y` e' **unitaria**: `(i s_y)^dag (i s_y) = I`)*
> ### **`= coniugato di [ psi_h^dagger (W_U psi)_h ]`**

### ⭐ **E prendendo le due parti:**

| | la densita' | sotto la `C` completa |
|---|---|---|
| `e_h = Re[ psi_h^dag (W psi)_h ]` | l'**energia** | ### ✅ **PARI** |
| **`q_h = Im[ psi_h^dag (W psi)_h ]`** | il **segno** | ### ⭐ **DISPARI, ESATTAMENTE, estremita' per estremita'** |

### ✅ **Quindi `b2` non va misurata: e' un'identita'.** ### ⚠ **E usa DUE cose:** che
`i sigma_y` sia **unitaria** *(vero per costruzione)* e che `C W_U = W_{CU} C`
### **— che e' MISURATO e non assunto.**

### ⭐ **E NOTO UNA COSA:** `e_h` e `q_h` sono **la parte reale e immaginaria dello STESSO
oggetto**. ### **L'energia e il segno sono due facce della stessa correlazione a due
tempi** — e questo spiega perche' `B3` trovava `Im<psi|W psi>` legata a `Q` a `-0.944`:
### **non erano due grandezze che si somigliavano, era una grandezza complessa.**

---

## 2. ⭐ IL SECONDO RISULTATO: LA FORMA CHE ORDINA, E PERCHE' NON ROMPE LA `C`

Sia **`q_k = somma_{h su k} q_h`** *(il segno del nodo: locale, una somma sulle sue
estremita')*. ### **Il termine candidato e':**

> ### ⭐ **`N_ord = - somma_{k,l vicini} J_{kl} q_k q_l`**

| | la proprieta' | perche' vale |
|---|---|---|
| ✅ **`C`-simmetrico** | sotto `C`, `q_k -> -q_k` *(par. `1`)*, quindi `q_k q_l -> q_k q_l`: ### **il PRODOTTO di due dispari e' PARI** |
| ✅ **ORDINA** | l'energia e' **piu' bassa** quando `q_k` e `q_l` hanno **lo stesso segno**: ### **e' il ferromagnete** |
| ✅ **LOCALE** | somma **sugli archi**: portata **`1` arco** per il termine, piu' la portata `1` di `q_h` ⟹ ### **`2` archi, DICHIARATI** |
| ✅ **rompe la simmetria NELLO STATO, non nelle leggi** | la legge e' `C`-pari; e' **il minimo** che non lo e' ⟹ ### **rottura SPONTANEA**, che e' cio' che la strada `(3)` chiede |

### ⭐ **E IL CANDIDATO DEL MANDATO E' GIA' DI QUESTA FAMIGLIA, come sospettavo:**
*«antifase -> repulsione»* vuol dire **energia piu' alta quando i segni sono opposti**,
### **cioe' esattamente `- q_k q_l` col segno giusto.** ### ✅ **La traduzione dall'era `1`
NON e' un innesto: la forma era gia' quella.** ### ⚠ **Ma <<e' della stessa famiglia>> non
e' <<e' la stessa>>**, e la verifica di quale sia il `q` dell'era `1` ### **non l'ho
fatta.**

---

## 3. ⛔ IL TERZO RISULTATO: `J` — **e qui c'era il punto debole del piano**

### ⛔ **Nel piano avevo scritto che `J` era <<la domanda vera>>**, perche'
`CARTA-FISICA-SIMULATORE/F10` ### **vieta le costanti nuove.** ### ⭐ **E adesso ho un
candidato che NON e' una costante.**

### `3.1` IL CONTO DIMENSIONALE, che e' l'unico argomento che ho

| | la grandezza | come si comporta |
|---|---|---|
| `1` | `e_h` e `q_h` | ### **la parte reale e immaginaria dello stesso bilineare in `psi`** ⟹ **la stessa scala** |
| `2` | il termine del vuoto `Lambda_k G(h_k/Lambda_k)` | a `x = h/Lambda` **piccolo** `G(x) ~ x^3/3`, quindi vale **`~ h^3 / Lambda^2`**; a `x` **grande** `~ h` |
| `3` | `h_k` | **la stessa scala** di `e_h` *(entrambi bilineari in `psi` contratti coi versori)* |

### ⭐ **Allora `q_k q_l` ha la scala di `h^2`, e per farne un'ENERGIA serve dividere per
una grandezza della scala di `h`.** ### ✅ **E ce n'e' UNA, locale, gia' in tabella:
`Lambda`.**

> ### ⭐⭐ **IL CANDIDATO: `N_ord = - somma_{k,l vicini} (q_k q_l) / Lambda_{kl}`**
>
> ### **Nessuna costante nuova: `Lambda` e' una VARIABILE DI STATO.**

### ⚠ **E la stessa struttura e' GIA' nel termine del vuoto:** `h^2/Lambda` e' **il primo
termine non banale** dello sviluppo di `Lambda G(h/Lambda)` *(a meno di un fattore `h/Lambda`)*.
### ⭐ **Quindi il termine di ordinamento NON e' di una famiglia nuova: e' della stessa
famiglia del vuoto**, con `q` al posto di `h`. ### ✅ **E questo e' l'argomento piu' forte
che ho**, perche' non e' un'analogia: ### **e' la stessa combinazione di grandezze.**

### `3.2` ⛔ CHE COSA RESTA LIBERO, E VA A LUCA

| | la scelta | perche' non la faccio io |
|---|---|---|
| `1` | **quale `Lambda`**: `Lambda_k`, `Lambda_l`, la loro **media**, o un `Lambda` **dell'arco** | sono **quattro forme**, tutte locali e tutte `C`-pari: ### **la misura le distingue, il ragionamento no** |
| `2` | se `q_k` sia la **somma** sulle estremita' del nodo o la loro **media** | cambia **come scala col grado**, e `A17` *(niente posizioni)* non decide fra le due |
| `3` | se il termine entri **in `H`** *(e quindi nel flusso)* o come **legge NON-H** | e' una scelta di **architettura della tabella**, non mia |

### ⛔ **E UNA COSA CHE NON SO, e la dico perche' pesa:** ### **non ho una DERIVAZIONE del
termine, ho un ARGOMENTO DIMENSIONALE.** ### ⚠ **Il conto dimensionale dice quali forme
sono AMMISSIBILI, non quale e' VERA** — e `A1` chiede **la legge, non il numero**:
### **qui ho ristretto le forme, non derivato la legge.** ### ✅ **Lo dichiaro invece di
spacciare la restrizione per una derivazione.**

---

## 4. ⚠ UN RISCHIO CHE VEDO, E CHE NON ERA NEL PIANO

### ⛔ **Il termine `- q_k q_l / Lambda` non e' limitato dal basso** se `q` puo' crescere:
piu' i vicini si allineano, piu' l'energia scende, e ### **niente lo ferma.**
### ⚠ **Nel ferromagnete lo ferma la normalizzazione dello spin** *(`|s| = 1`)*; qui
### **`q_h` e' limitato dalla norma di `psi`**, che **e' conservata** — quindi
### **probabilmente e' limitato.** ### ⛔ **Ma <<probabilmente>> non basta, e la tentazione
sara' un TETTO su `q`:** ### **`A11` lo vieta senza un errore trovato.**

> ### ⭐ **PREVISIONE, scritta prima:** `|q_k| <= ||psi||^2` per **ogni** stato, perche'
> `q_h` e' la parte immaginaria di un bilineare fra `psi` e `W psi` con `W` **unitaria**, e
> Cauchy-Schwarz da' `|psi_h^dag (W psi)_h| <= |psi_h| |(W psi)_h|`.
> ### ✅ **Se vale, il termine E' limitato e non serve nessun tetto.** ### ⚠ **E' un conto
> che NON ho finito**, e lo dico.

---

## 5. LE PREVISIONI E LE SOGLIE — *per quando ci sara' il codice*

| | la previsione | la soglia |
|---|---|---|
| `b1` | ### ✅ **GIA' DERIVATA:** la forma e' `C`-pari | — *(e' un'identita')* |
| `b2` | ### ✅ **GIA' DERIVATA, e nel piano l'avevo messa come MISURA:** `q_h` e' `C`-dispari estremita' per estremita' | ### ⚠ **La verifica numerica resta utile come CONTROLLO DELLO STRUMENTO**, `< 100` ulp — non come prova |
| `b3` | `J = 1/Lambda` **non e' una costante nuova** | ### ✅ **vero per costruzione** *(`Lambda` e' di stato)* |
| `b4` | il termine e' **limitato**: `|q_k| <= ||psi||^2` | ### **entro ulp** sulla disuguaglianza, su stati casuali |
| `b5` | il termine **ORDINA**: con `N_ord` acceso, due nodi vicini con `q` di segno **opposto** hanno energia **maggiore** che con lo stesso segno | ### **differenza `> 0`** su `>= 100` coppie casuali |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. se `b4` **cadesse** *(il termine non limitato)*, ### **la forma non e' ammissibile**, e
   **non si tappa con un tetto** — si cambia forma.
2. se `[[DOMANDA-BANDE-O-SEGNO-LOCALE]]` dicesse **`N+ - N-`**, allora ### **tutto questo
   paragrafo cade**, perche' `N+` e' **globale** e `F10` la vieta in una legge.
3. e se le **quattro forme** del `3.2` dessero **esiti diversi nella misura**, ### **non
   scelgo io**: si riportano i quattro numeri.

---

## 6. LA STELLA POLARE

| | la domanda | la risposta |
|--:|---|---|
| **1** | conserva **localmente**? | ### ⚠ **Il termine e' locale** *(portata `2` archi, dichiarata)*, ### **ma la sua corrente non l'ho derivata** — e `A14` la chiede. ### **E' il prossimo passo, non questo** |
| **2** | **quale gradino**? | ### **NESSUNO: derivazione, senza codice** |
| **3** | **aggiunge un numero o una legge**? | ### ⛔ **UNA LEGGE** *(il termine di ordinamento)*, e `9-ter` chiede di contarle: **da `3` a `4`**. ### ✅ **MA NESSUN NUMERO**, se `J = 1/Lambda` regge — e quello era il punto debole del piano |
| **4** | tocca `rho`, `c_s` o **il SEGNO**? | ### ⭐ **IL SEGNO E' L'OGGETTO:** `q_h` **e'** il segno, e il termine **lo ordina** |
| **5** | **emergente o imposto**? | ### ⭐ **La `C`-disparita' di `q_h` e' DERIVATA** *(par. `1`)*, e la **rottura** e' **emergente** *(le leggi restano pari)*. ### ⛔ **Il termine e' IMPOSTO**, e la sua forma e' **ristretta da un conto dimensionale, non derivata** |

---

## 7. TODO

1. la **corrente** di `q` *(`A14`)*: `q_k` cambia, e **dove va**? ### ⭐ **E la costruzione
   di `0080cf3` dice come farla**, perche' `q_h` e' un bilineare come `e_h`.
2. finire il conto di `b4` *(il termine e' limitato)*.
3. le **quattro forme** del `3.2` a Luca, **una voce**.
4. ### ⛔ **E NIENTE CODICE finche' `[[DOMANDA-BANDE-O-SEGNO-LOCALE]]` non risponde:** se il
   parametro d'ordine fosse `N+ - N-`, ### **questo pezzo non serve.**

---

## 8. ⛔ `(R1)` — **DIVIDERE PER `Lambda` ESPLODE DOVE IL VUOTO E' SOTTILE**

> **Riserva della verifica esterna, accolta dal mandato di Luca delle `16:11`:** *«Il
> termine del vuoto `Lambda G(h/Lambda)` resta LIMITATO quando `Lambda -> 0`. Invece
> `q_k q_l / Lambda` ESPLODE. E per decisione di Luca il vuoto nasce solo dove c'e' spazio,
> quindi zone a `Lambda` piccolo CI SARANNO.»*

### ✅ **E' GIUSTA, E LA ACCETTO.** E noto che **il mio conto su `q` non la copriva**:
avevo previsto `|q_k| <= ||psi||^2` per Cauchy-Schwarz ### **ed e' VERO** *(`W` e'
unitaria)*, ### ⛔ **ma un limite su `q` NON IMPEDISCE una divergenza in `1/Lambda`.**
### **Avevo controllato il numeratore e non il denominatore.**

### `8.1` ⭐⭐ PERCHE' IL TERMINE DEL VUOTO E' LIMITATO, e **dove sta il trucco**

A `Lambda -> 0` l'argomento `x = h/Lambda -> infinito`, e `G(x) = x - arctan x -> x - pi/2`.
Quindi

> **`Lambda G(h/Lambda) -> Lambda (h/Lambda - pi/2) = h - (pi/2) Lambda -> h`**

### ⭐ **IL TRUCCO NON E' CHE `G` SIA LIMITATA — `G` CRESCE LINEARMENTE.** E' che
`Lambda` **moltiplica** e l'argomento ha `Lambda` **al denominatore di grado `1`**:
### **i due si CANCELLANO.**

### `8.2` ⛔ **E ALLORA `G` NON SI TRASFERISCE, e questo non me lo aspettavo**

La tentazione ovvia e' riusare `G`, cioe' `Lambda G(q_k q_l / Lambda^2)`. ### **Non
funziona:** a `Lambda -> 0` l'argomento va a infinito, `G(u) -> u - pi/2`, e

> **`Lambda (q_k q_l / Lambda^2 - pi/2) = q_k q_l / Lambda - (pi/2) Lambda`** ### **⟹ ESPLODE ANCORA**

### ⭐ **E IL PERCHE' E' PRECISO: l'argomento ha `Lambda` AL GRADO `2`, non `1`.** La
cancellazione che salva il termine del vuoto ### **qui non avviene**, perche' `q_k q_l` e'
**quadratico** dove `h` era **lineare**.

> ### ⛔ **QUINDI SERVE UNA `F` DAVVERO LIMITATA, non una che cresce linearmente come `G`.**
> ### **E' un requisito DIVERSO da quello di `G`**, e lo dico perche' <<l'analogo di `G`>>
> suonava come *«la stessa cosa»*.

### `8.3` ✅ LA FORMA ESISTE, E **NON E' UNICA**

> **`N_ord = - somma_{k,l vicini} Lambda_{kl} F( q_k q_l / Lambda_{kl}^2 )`**,
> con **`F(u) ~ u`** a piccolo argomento e **`F` LIMITATA** a grande.

| | il limite | il conto | |
|---|---|---|---|
| `Lambda` **grande** | argomento `-> 0`, `F ~ u` | `Lambda (q q/Lambda^2) = q q / Lambda` | ### ✅ **piccolo: ritrova la forma ingenua dove e' SICURA** |
| `Lambda -> 0` | argomento `-> infinito`, `F -> F_inf` | `Lambda F_inf -> 0` | ### ✅ **LIMITATO, e in realta' SVANISCE** |

### ⭐⭐ **E CHE SVANISCA HA UNA LETTURA FISICA, e non e' un effetto collaterale:**
### **senza vuoto non c'e' mediazione, quindi non c'e' ordinamento.** ### ✅ **E' il vuoto
come MEDIATORE — l'idea della strada `(A)` — che sopravvive qui come una proprieta'
STRUTTURALE, non come una legge.** ### ⚠ **E lo noto perche' `(A)` e' chiusa come fallita:
la sua INTUIZIONE non lo era.**

### ⛔ **E NON E' UNICA, e lo dichiaro invece di scegliere:** `F(u) = arctan u`,
`F(u) = u/(1 + |u|)`, `F(u) = tanh u` ### **vanno tutte e tre**, nessuna porta costanti
nuove, e ### **nessun argomento che ho le distingue.**

### ⭐ **MA SO DIRE CHE CLASSE DI SCELTA E', ed e' il modo di consegnarla:** e'
### **la stessa classe di `G` stessa** — `G(x) = x - arctan x` e' una forma **scelta** con
quei requisiti. ### ✅ **Quindi `F` la deve scegliere chi ha scelto `G`**, e con lo stesso
tipo di criterio.

### `8.4` ⚠ E UNA CONSEGUENZA CHE NON ERA NELLA RISERVA, da mettere a previsione

### ⛔ **Con `F` LIMITATA il termine di ordinamento SATURA:** oltre un certo
`q_k q_l / Lambda^2` **non cresce piu'**. ### ⚠ **Quindi la forza che ordina si INDEBOLISCE
nelle regioni GIA' molto ordinate**, e questo ### **potrebbe limitare l'ordine
raggiungibile.**

> ### ⭐ **PREVISIONE, scritta prima:** l'ordine di saturazione sara' **`|q| ~ Lambda`**
> *(dove l'argomento e' di ordine `1`)*, ### **e non `|q| ~ ||psi||^2`** che e' il limite
> di Cauchy-Schwarz. ### ⚠ **Cioe' il vuoto fissa la scala dell'ordine**, e dove il vuoto
> e' sottile ### **l'ordine satura PRIMA.**

### ✅ **E NON METTO NESSUN TETTO** *(`A11`)*: la limitatezza viene **dalla forma di `F`**,
### **non da un clip.**

---

## 9. ⛔ `(R2)` — **UN SISTEMA CHIUSO SI ORDINA SOLO SE E' ABBASTANZA FREDDO**

> **Riserva della verifica esterna:** *«La parita' misurata (`a67b68f`) e' lo stato
> all'equilibrio a TEMPERATURA INFINITA del grado di liberta' delle bande. Un termine
> ferromagnetico conservativo produce ordine SOLO se la densita' d'energia del sistema sta
> sotto quella della transizione.»*

### ✅ **E' GIUSTA, E CAMBIA IL SENSO DI `(P-b)`.** Il termine di ordinamento **non e' un
meccanismo che ordina**: e' **un termine che RENDE L'ORDINE un minimo di energia.**
### ⛔ **E un sistema hamiltoniano CHIUSO non scende al minimo: resta sulla sua superficie
di energia.** ### **Quindi il termine, DA SOLO, non ordina niente.**

### `9.1` LA CONDIZIONE, scritta

Sia `u` la densita' d'energia **per nodo** disponibile nel grado di liberta' del segno, e
`J_eff` la **scala del termine di ordinamento** *(`~ q^2/Lambda`, o la sua versione
limitata)*. Allora

> ### ⭐ **l'ordine si forma solo se `u <~ J_eff`** *(a meno di un fattore `O(1)`, che e'
> la temperatura di transizione in unita' di `J`)*.

### ⚠ **E NON CONOSCO quel fattore `O(1)`:** dipende dalla dimensione effettiva del grafo e
dal numero di vicini. ### ⛔ **Quindi la <<soglia>> e' una PREVISIONE DI ESISTENZA, non un
numero** — e scrivere un numero adesso sarebbe inventarlo.

### `9.2` ⭐ LE PREVISIONI, scritte PRIMA

| | la previsione | la soglia |
|---|---|---|
| `r2a` | ### ⛔ **con lo SPAZIO FISSO NON si ordina, nemmeno col termine** | lo squilibrio per regione **si spegne verso la parita'**, come **gia' misurato** senza il termine *(un fattore `623`)*. ### **Se si ordinasse, la mia lettura di `(R2)` e' sbagliata** |
| `r2b` | **con la CRESCITA si ordina, ma SOLO sotto una soglia di diluizione** | la lunghezza di correlazione **cresce** *(coarsening)* **solo** per rampe piu' lente di una velocita' critica, e ### **la velocita' critica SI MISURA** |
| `r2c` | e la **scala dell'ordine** e' fissata dal vuoto | `\|q\| ~ Lambda` al punto di saturazione *(par. `8.4`)* |

### `9.3` ⭐⭐ E IL RAFFREDDAMENTO E' LO STESSO MECCANISMO DEL CONGELAMENTO — *una cosa, non due*

### ⭐ **Il candidato naturale e' la CRESCITA DELLO SPAZIO**, e il mandato lo dice. Ma c'e'
di piu', e lo noto perche' unifica due pezzi che avevo tenuto separati:

| | la crescita dello spazio... | dove sta nel piano |
|---|---|---|
| `1` | ...**abbassa `x = \|h\|/Lambda`**, e con lui **il tasso di mescolamento `Gamma(x)`** | ### **e' `(D2)`–`(D3)`: il congelamento per diluizione** |
| `2` | ...**diluisce l'energia per nodo `u`**, perche' **il vuoto nasce con lo spazio e la materia no** | ### **e' `(R2)`: il raffreddamento** |

> ### ⭐⭐ **SONO LO STESSO MECCANISMO VISTO DUE VOLTE.** Il congelamento per diluizione
> **spegne cio' che disordina**; il raffreddamento **permette a cio' che ordina di
> funzionare**. ### ✅ **E la MISURA e' una sola: `(D3)`/`(D4)`, con e senza il termine di
> ordinamento.**

### ⚠ **E QUESTO CAMBIA L'ORDINE DEL PIANO, e non lo cambio da solo:** `(P-b)` **non si
puo' misurare a spazio fisso** — ### **`r2a` dice che darebbe la parita' QUALUNQUE sia il
termine.** ### ⛔ **Quindi la misura di `(P-b)` E' `(D3)` con il termine acceso**, non una
misura a se'. ### **Lo porto a Luca invece di riordinare il piano.**

---

## 10. ✅ IL RIORDINO DEL PIANO — **accolto da Luca il `2026-10-13` alle `17:58`**

> **Luca:** *«Accolta la tua conclusione di `f23d971`: il termine di ordinamento da solo
> non ordina un sistema chiuso, quindi `(P-b)` NON si misura a spazio fisso. **LA MISURA
> DI `(P-b)` E' `(D3)`/`(D4)` COL TERMINE ACCESO**, confrontata con `(D3)`/`(D4)` col
> termine spento.»*

### ⭐ **Quindi il piano cambia cosi', e il confronto E' la misura:**

| | la corsa | che cosa decide |
|---|---|---|
| `1` | `(D3)`/`(D4)` **col termine SPENTO** | ### **il CONTROLLO:** e' il congelamento per diluizione **da solo** |
| `2` | `(D3)`/`(D4)` **col termine ACCESO** | ### **la misura di `(P-b)`** |
| `3` | ### ⭐ **la DIFFERENZA fra le due** | ### **se il termine ORDINA, e QUANTO** |

### ⛔ **E NON C'E' PIU' UNA MISURA DI `(P-b)` A SE': non esisteva un modo di farla.**
### ⚠ **La previsione `r2a` lo diceva** *(a spazio fisso si ha la parita' **qualunque** sia
il termine)*, e ### **adesso il piano lo riflette invece di tenere in lista una misura che
non si puo' fare.**

### ⭐ **E questo rende `(D3)`/`(D4)` il PUNTO DI CONVERGENZA di due pezzi:** il
**congelamento per diluizione** e il **raffreddamento** sono lo stesso meccanismo,
### **e adesso anche la loro MISURA e' la stessa.**
