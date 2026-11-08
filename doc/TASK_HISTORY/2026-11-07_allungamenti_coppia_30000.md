# 2026-11-07 — GLI ALLUNGAMENTI DELLE CORSE DELLA COPPIA FINO A `30000` *(Luca `2026-11-07` `10:26`)*

**Il mandato** *(nella sostanza)*: **finire i lavori in corso, poi allungare tutte le corse della coppia fino a `t 30000`** -- `C35-0`, `C35-pi`, `S162` da `10000` a `30000` **ripresi dall'ultimo stato salvato**, `C50-0` **direttamente da `0` a `30000`** *(scelta del guardiano, dichiarata)*; mappe e stati come prima, ciascuno col suo referto sull'intervallo intero e le mappe leggere; **dopo `C35-0` e `C35-pi` allungate, il referto della coppia rifatto fino a `30000`**, con le letture `m1`-`m4` scritte prima. **Un calcolo alla volta; il nucleo non si tocca** *(salvo la cura dell'`assert` delle `10:06`, nel suo commit)*; **nessun peso si regola.**

**Le premesse di Luca** *(dalle mappe di `C35-0`, la lettura del guardiano)*: **i due «nuclei» del vuoto** *(`dLambda > 0` dentro l'ovale)* **da `+-17.5` a circa `+-15` entro `t 4500`-`7200`, poi fermi fra `28` e `30` nodi di distanza fino a `9900`**; **la materia oscilla fra i nuclei e il centro** *(un ritmo di `~1800`-`3000` unita' di tempo)*; **l'involucro e' ovale** *(due nuclei separati, non un solitone di massa doppia, che sarebbe rotondo)*; **in `3000` unita' dopo l'avvicinamento uno o due «respiri»: non basta per dire se l'oggetto e' stabile, si fonde o si separa.**

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. ### **Il meccanismo di ripresa C'E' gia', e non e' una continuazione con un nome nuovo:** **ogni pezzo di una corsa riparte da `db/accensione_lenta/<nome>.npz`** *(`corsa_accensione`, `f_rip`: lo stato intero, scritto alla fine di ogni pezzo)*, **e la corsa si dice «finita» quando `t1 >= t_fine` dell'ultimo pezzo.** **Oggi `CORSE[<nome>] = (1000, 10000)` per tutte e quattro**: ### **alzare il `10000` a `30000` basta perche' il pezzo dopo riparta da `66667` tick, cioe' `t 10000`.** **La strada di `TF3C`** *(un nome nuovo con `CONTINUA`)* **non serve**: **i jsonl restano della stessa corsa**, e le carte la leggono intera.
2. **I file di ripresa ci sono:** `C35-0.npz`, `S162.npz`, `C35-pi.npz` *(quest'ultimo in scrittura: `C35-pi` e' in volo)*; **l'ultima riga di `C35-0` e di `S162` ha `t1 = t_fine = 66667`, `fermata` `None`** *(niente arresto: la corsa e' finita per tempo)*, **e porta `sha_fine`** *(gli `sha` di ogni chiave dello stato alla fine)*.
3. ### **Cio' che cambia nel codice** *(da verificare chiave per chiave, prima del commit)*: **`CORSE[_n]`** *(il `30000`)*, **`STATI[_n]`** *(gli stati ogni `1500` fino a `30000`: `0 .. 30000`, `21` stati, come `TBS`)*. ### ⚠ **`t_fine` entra anche nella stima del disco e nel referto** *(`fatta = ult["t1"] >= ult["t_fine"]`)*: **le righe vecchie hanno `t_fine` `66667`, le nuove `200000`**; **da guardare che nessuna carta legga `t_fine` della PRIMA riga per decidere** *(`carta_s162`: `ult`, l'ultima: va bene)*.
4. ### **Il DEVE della ripresa che il driver permette** *(Luca: «il primo pezzo ripreso contro un pezzo ricalcolato dallo stato precedente, se il driver lo permette»)*: **SI', lo permette:** **lo stato completo a `t 9000`** *(tick `60000`, salvato su `E:`)* **e' l'inizio dell'ultimo pezzo** *(`60000 -> 66667`)*. **Il DEVE `R-1`** *(proposto)*: ### **dallo stato a `60000`, `6667` tick col tick della corsa, il bordo compreso, e gli `sha` di ogni chiave = `sha_fine` dell'ultima riga, al bit**: **cioe' la corsa ininterrotta, rifatta, arriva allo stato da cui la ripresa parte.** **E `R-0`** *(per costruzione, poco costoso)*: **gli `sha` del file di ripresa = `sha_fine`.** ### **Il costo di `R-1`: `~45` minuti per corsa** *(`6667` tick, a `~0.40` s per tick sul pezzo di `C35-pi`: `4281` s per `10000`)*; ### ⚠ **e' un calcolo, quindi va in fila, uno alla volta, prima del primo pezzo ripreso.** **Se Luca lo vuole piu' corto:** `R-0` piu' il DEVE `ST1` gia' nel referto *(da ogni stato salvato `100` tick al bit)*, **che pero' non copre il punto di ripresa.**
5. **`C50-0` da `0` a `30000`:** **la prima corsa di quel nome, quindi `C0` breve all'inizio** *(come le altre)*. ### **Il suo referto vuole ancora una decisione di Luca: il singolo di riferimento col bordo di `C50`** *(`R_A 55`; `S162` ha quello di `C35`)*.
6. **I referti «sull'intervallo intero»:** **`carta_s162`** confronta con `TB3` e `TBS` **fino alla fine di `S162`** *(`TBS` arriva a `30000`; `TB3`: da guardare fin dove arriva)*; **`carta_coppia`** ha i tempi dei profili scritti *(`0 .. 9990`)*: **per `30000` vanno estesi** *(un cambio di codice, committato prima di girare)*.
7. **Il disco:** **le mappe di `C35-0` `112` MB e gli stati `61` MB su `10000`** *(misurati con `du`)*: **`~340` e `~180` MB a `30000`**, **per quattro corse `~2` GB su `E:`** *(oggi `212` GB liberi)*; **su `C:` `22` GB liberi** *(il FERMO e' sotto `6`)*.
8. **Che cosa NON so:** **se `R-1` passa al bit** *(il bordo e' fuori dal nucleo, ma deterministico)*; **se la stima di `~7.3` ore per `10000` regge** *(i pezzi di `C35-pi` costano `4281` e `3931` s, mentre la carta della coppia girava accanto)*.

## 2. PROGETTAZIONE DEL RAGIONAMENTO *(le letture si fissano QUI, prima dei numeri)*

- **L'ordine** *(Luca)*: **(A) finire cio' che e' in corso** -- `C35-pi` fino a `10000` e il suo referto; il referto ufficiale della coppia `C35-0` / `C35-pi` contro `S162` *(coi centri del vuoto)*; **le decisioni delle `10:06`** *(la cura dell'`assert` del nucleo, IS2 con le soglie derivate, IS3 col confronto deciso, `LIB0`-`LIB2`, ciascuno col suo referto)*; le mappe leggere di `C35-pi`. **(B) gli allungamenti, uno alla volta:** `C35-0`, `C35-pi`, `S162` *(da `10000` a `30000`)*, `C50-0` *(da `0` a `30000`)*. **(C) dopo ogni corsa:** il referto, poi le carte brevi in coda, poi la corsa successiva.
- **Il codice degli allungamenti** *(un commit, a `C35-pi` finita: `corsa_accensione.py` e' nel suo percorso)*: `CORSE` e `STATI` delle quattro corse; **il DEVE della ripresa** *(`R-0`, `R-1`, come comando a se', `--ripresa <nome>`, prima del primo pezzo ripreso)*; ### **il DEVE che ogni corsa vecchia resti al bit** *(le righe esistenti non si riscrivono; la cassetta)*.
- **Il costo** *(Luca)*: **`~15` ore per allungamento, `~22` per `C50-0`, `~66` in tutto**; **la stima vera dopo il primo pezzo di ciascuno**; **lo spazio su `C:` ed `E:` nel commit della stima.**
- ### **LE LETTURE, scritte PRIMA** *(Luca)*, **per il referto della coppia rifatto fino a `30000`:**
  - **(m1)** **i nuclei restano separati a una distanza stabile: una «molecola»;**
  - **(m2)** **si avvicinano e si fondono in un solitone rotondo di massa doppia;**
  - **(m3)** **si separano;**
  - **(m4)** **altro.**
  **Il criterio:** **le stesse grandezze del referto** *(`d(t)`, i centri del vuoto, l'escursione per blocco, la forma)* **sull'intervallo intero; nessuna soglia mia nuova.** ### ⚠ **«Rotondo» vuole una misura della forma** *(l'ovalita' dell'involucro)*: **la carta della forma esiste** *(`carta_forma.py`, sul singolo)*; **come la si applica alla coppia lo scrivo prima del codice del referto rifatto.**
- **Che cosa mi farebbe FERMARE:** **`R-0` o `R-1` che fallisce** *(la ripresa non e' la corsa ininterrotta)*; **una corsa vecchia che non resta al bit**; **`C:` sotto `6` GB.**

## 3. TODO DEL NEXT STEP

1. **Questo task history, la riga della MAPPA, la relazione: un commit.**
2. **(A), nell'ordine:** la carta di `C35-0` *(in corso, l'eccezione delle `10:20`)*; `C35-pi` fino a `10000`, i suoi jsonl, `D6`, la cassetta; il referto ufficiale della coppia; **la cura dell'`assert`** *(il task history prima, la voce del difetto, il commit del nucleo, la suite)*; **IS2 e IS3**; **`LIB0`-`LIB2`** *(il codice di `libreria.py` prima)*; **le mappe leggere di `C35-pi`.**
3. **(B):** **il codice degli allungamenti** *(`CORSE`, `STATI`, `--ripresa`)*, `D6`, la cassetta; **per ciascuna corsa:** `R-0` e `R-1`, il primo pezzo, **la stima vera e lo spazio nel commit**, poi i pezzi fino a «finita», il referto, le mappe leggere.
4. **(C):** **il referto della coppia rifatto fino a `30000`** *(i profili estesi, la forma dell'involucro)*, con `m1`-`m4`.

## 4. L'ARRESTO PER STAZIONARIETA' *(l'aggiunta di Luca delle `10:35`)*: **LA PROPOSTA, e il FERMO prima del codice**

- **La decisione di Luca:** **oltre al tetto di `30000`, un ARRESTO quando l'oggetto e' stazionario** *(le grandezze che lo descrivono smettono di cambiare in media, pur continuando a oscillare)*: **non spendere ore dove il processo e' gia' concluso.** ### **«Stazionario» vuol dire NELLA FINESTRA OSSERVATA, non per sempre** *(`TF3` e' stato fermo `16000` unita' e poi e' partito)*: ### **nei referti si scrive «stazionario da `t X` entro la finestra osservata», mai «finito».** ### ⛔ **FERMO PRIMA DEL CODICE: la definizione esatta la decide Luca.**

### 4.1 LE PREMESSE DAL CODICE *(da dove si leggerebbe ogni grandezza, alla fine di un pezzo)*

1. **Un pezzo e' `10000` tick = `1500` unita' di tempo** *(`V.PEZZO`)*: ### **il controllo si fa ogni `1500` unita'**, dai jsonl e dalle mappe gia' scritte su `E:` *(le mappe di un pezzo si scrivono alla sua fine)*, ### **senza toccare il tick.**
2. **Per le coppie, dove sta ciascuna grandezza:**
   - **la distanza dei nuclei del vuoto e quella dei centri della materia:** **dalle MAPPE** *(le stesse funzioni di `carta_coppia`: `centri_vuoto`, `centri_semipiani`)*, **una ogni `100` tick**;
   - **l'allungamento dell'involucro:** **dalle mappe**, il tensore d'inerzia di `rho` attorno al centro periodico *(il rapporto degli assi; oggi NON e' in nessuna carta: codice nuovo, con un suo DEVE su una forma sintetica)*;
   - **`E_int`** *(o `E + E_ass`)*: **dai campioni** *(`E` per termini e `bordo.E_ass`)*, **piu' `E[0]` del vuoto `c(t) F3`, che va CALCOLATO** *(`conti_per_nodo` a ogni campione, come `carta_coppia`)*: ### **e' il pezzo costoso del controllo**; ### ⚠ **e `E_int` vuole anche `S162` agli stessi tempi** *(`E[C] - 2 E[S] + E[0]`)*: **per l'allungamento di `C35-0` e di `C35-pi` `S162` arriva a `30000` DOPO, nell'ordine di Luca** *(`C35-0`, `C35-pi`, poi `S162`)*. ### **Quindi durante gli allungamenti delle coppie `E_int` NON si puo' calcolare oltre `10000`;** **si puo' `E + E_ass` della coppia da sola** *(che e' `E_int` piu' termini del singolo e del vuoto)*. **Da decidere** *(sotto, `q-s2`)*.
   - **il ritmo di emissione:** **`bordo.M_ass` dei campioni** *(la massa assorbita cumulata)*, **la sua pendenza per unita' di tempo.**
3. **Per `S162`:** **il centro periodico** *(`per`)*, **`w`**, **il cuore** *(`f_liscia`)*, **il ritmo di emissione** *(`bordo.M_ass`)*: **tutti nei campioni.**
4. ### **Per il DEVE FALLIRE su `TF3`:** **`TF3` NON ha bordo**, quindi **non ha `M_ass`**: **il ritmo di emissione non esiste.** **Il sostituto che propongo:** **la pendenza dell'alone** *(`alone` nei campioni)*. ### **E `TF3` arriva a `16000`; `TF3C` la continua fino a `30000`** *(la partenza del moto e' a `16000`, proprio al confine fra le due)*: ### **il DEVE FALLIRE va applicato a `TF3 + TF3C` concatenate**, altrimenti l'intervallo che contiene la partenza **non c'e'.**
5. ### ⚠ **UN CONTO CHE CAMBIA IL VALORE DELL'ARRESTO, e lo scrivo prima** *(da uno script, nella sessione: il primo controllo e' la prima fine di pezzo con `t >= inizio + 2 W`, l'arresto due pezzi dopo)*:

   | le finestre contate da | `W` | il primo controllo | l'arresto | il risparmio sul tetto `30000` |
   |---|---|---|---|---|
   | `t 1000` *(dopo la rampa)* | `6000` | `13500` | `16500` | `13500` |
   | `t 1000` | `5400` *(`3 x 1800`)* | `12000` | `15000` | `15000` |
   | `t 1000` | `7200` *(`3 x 2400`)* | `16500` | `19500` | `10500` |
   | `t 1000` | `9000` *(`3 x 3000`)* | `19500` | `22500` | `7500` |
   | `t 10000` *(l'allungamento)* | `6000` | `22500` | `25500` | `4500` |
   | `t 10000` | `7200` | `25500` | `28500` | `1500` |
   | `t 10000` | `9000` | `28500` | `31500` | ### **nessuno: oltre il tetto** |

   ### **Quindi l'arresto risparmia qualcosa solo se le finestre si contano da `t 0`** *(le serie partono da li': i jsonl e le mappe sono gli stessi)*, **e solo se l'oggetto e' gia' stazionario da presto.** **La proposta: contarle dalla fine della rampa** *(`t >= 1000`)*.

### 4.2 LA PROPOSTA *(di Luca, coi dettagli che il codice vuole; decide Luca)*

- **(s-G) LE GRANDEZZE:**
  - **per le coppie:** la distanza dei due nuclei del vuoto; la distanza dei centri della materia; l'allungamento dell'involucro; `E_int` *(o `E + E_ass`, `q-s2`)*; il ritmo di emissione;
  - **per `S162`:** il centro *(la sua distanza dalla partenza)*, `w`, il cuore, il ritmo di emissione.
- **(s-W) LE FINESTRE:** **`W = 3 P`**, **`P` il periodo del respiro stimato dalla serie della distanza dei centri della materia** *(il picco del periodogramma dopo la rampa, tolta la retta; la stima e il suo errore stampati)*; **se non si stima, `W = 6000`.** ### **Da dichiarare prima, quindi:** **`P` si stima UNA volta** *(alla fine del primo pezzo dell'allungamento, dalla serie da `1000` a `10000`)* **e poi resta fisso**, ### **altrimenti la finestra si sposterebbe insieme ai dati.**
- **(s-S) LA SOGLIA:** **due finestre adiacenti** *(`[t - 2W, t - W]` e `[t - W, t]`)* **con medie che differiscono meno di `2` volte l'errore statistico della differenza**, **per TUTTE le grandezze**; **l'arresto quando vale per TRE controlli di fila** *(le fini di tre pezzi consecutivi)*.
  - **L'errore della media con la correlazione:** ### **la proposta mia: le MEDIE A BLOCCHI** *(`batch means`)*: **la finestra divisa in blocchi di lunghezza `P`** *(un periodo: dentro un blocco l'oscillazione si media)*, **l'errore = la deviazione delle medie dei blocchi divisa `sqrt(numero dei blocchi)`**; **con `W = 3 P` sono `3` blocchi**: **un errore stimato da `3` numeri e' ROZZO** *(dichiarato)*. **L'alternativa:** il tempo di autocorrelazione integrato *(`sigma^2 2 tau_int / N`)*, **che pero' vuole una finestra di taglio, cioe' un altro numero.**
  - **«Differiscono meno di `2` volte»:** **l'errore della DIFFERENZA** *(`sqrt(e1^2 + e2^2)`)*, **non della media sola**: **lo scrivo perche' sono due cose diverse** *(un fattore `sqrt 2`)*.
- **(s-E) IN PIU', COME STIMA E NON COME ARRESTO:** **l'adattamento `d(t) = d_fin + A e^{-t / tau}`** alla distanza dei nuclei *(e alle altre grandezze, se monotone)*, **`tau`, `d_fin` e il loro errore** *(dalla matrice di covarianza dei minimi quadrati, con la stessa correzione per la correlazione)* **stampati a ogni referto**: **quanto manca, se manca.** ### **«Se monotone»:** **la proposta: il segno della pendenza delle medie a blocchi e' lo stesso in tutti i blocchi dopo la rampa.**
- **(s-T) IL TETTO DI `30000` RESTA.**
- **(s-D) I DEVE:**
  - **`ST-S`** *(stampa dove avrebbe fermato)*: **il criterio applicato a posteriori a `S162` da `0` a `10000`, a `TB3` e a `TBS` fino a `30000`.** **Un controllo di sensatezza, non un DEVE che passa o fallisce** *(un singolo legato dovrebbe risultare stazionario presto)*. ### ⚠ **Con `W = 6000` e tre controlli, `S162` a `10000` NON PUO' risultare stazionario** *(il primo arresto possibile e' a `16500`, la tabella della premessa `5`)*: **la stampa direbbe «non stazionario entro `10000`» PER COSTRUZIONE** -- ### **un FALSO-ZERO, da sapere prima.** **Su `TB3` e `TBS` fino a `30000` invece si puo'.**
  - **`ST-F`** *(DEVE FALLIRE, di Luca)*: **applicato a `TF3 + TF3C`, NON dichiara stazionario l'intervallo che contiene la partenza** *(`16000`)*: ### **cioe' nessun arresto con `t - 2W <= 16000 <= t`.**
  - **In piu', miei:** **`ST-P`** *(il periodo stimato su una serie sintetica `sin` di periodo noto, entro il passo del periodogramma)*; **`ST-B`** *(le medie a blocchi su una serie sintetica stazionaria con rumore noto: l'errore entro un fattore dichiarato)*; **`ST-I`** *(il tensore d'inerzia su un'ellisse sintetica di rapporto noto)*.
- **La lettura nel referto:** **«stazionario da `t X` entro la finestra osservata»**, mai «finito».

### 4.3 LE DOMANDE A LUCA *(il FERMO; il criterio di chiusura: le sue risposte, scritte qui)*

1. **(q-s1) Le finestre contate da `t 0`** *(dopo la rampa)* **o dall'inizio dell'allungamento?** **Da `0` il risparmio massimo e' `13500` per corsa con `W = 6000`; dall'allungamento `4500`, e con `W = 9000` nessuno** *(la tabella della premessa `5`)*. **La mia proposta: da `0`.**
2. **(q-s2) `E_int` durante gli allungamenti delle coppie:** **`S162` a `30000` arriva DOPO `C35-0` e `C35-pi`** *(il tuo ordine)*: **(a) `E + E_ass` della coppia da sola** *(la mia proposta)*, **(b) `S162` allungato PRIMA delle coppie** *(l'ordine cambia)*, **(c) `E_int` tolto dalle grandezze dell'arresto.**
3. **(q-s3) L'errore della media:** **le medie a blocchi di lunghezza `P`** *(`3` blocchi per finestra: rozzo)* **o il tempo di autocorrelazione integrato** *(un taglio in piu')*?
4. **(q-s4) Il ritmo di emissione per `TF3`** *(senza bordo):* **la pendenza dell'alone?**
5. **(q-s5) Il periodo `P`:** **stimato una volta all'inizio dell'allungamento e poi fisso** *(la mia proposta)*?
6. **(q-s6) `C50-0`, che parte da `0`:** **il periodo non si stima prima di avere la serie**: **`W = 6000` fino alla prima stima** *(dopo il pezzo che arriva a `10000`)*, **poi `3 P`?**

- ### **Il codice degli allungamenti** *(la sez. `3`, punto `3`)* **ASPETTA queste risposte:** **l'arresto entra nello stesso codice.** **Il resto della coda (A) non dipende da qui, e va avanti.**

## 5. LE DECISIONI DI LUCA DEL `2026-11-07` `10:50` *(il FERMO della sez. `4.3` CHIUSO)*

1. ### **(q-s1) Le finestre contate da `t 0`, dopo la rampa** *(`t >= 1000`)*.
2. ### **(q-s2) (a): `E + E_ass` della coppia da sola** *(«per la stazionarieta' basta che smetta di cambiare; i termini del singolo e del vuoto sono costanti o stazionari a loro volta»)*. **L'ordine degli allungamenti resta: `C35-0`, `C35-pi`, `S162`, `C50-0`.**
3. ### **(q-s3) Il tempo di autocorrelazione integrato, col taglio automatico standard** *(la finestra di Sokal)*, **non i tre blocchi.** **Come lo scrivo nel codice** *(dichiarato qui, prima)*: **`tau_int(M) = 1/2 + somma_{k=1..M} rho(k)`**, **`M` il piu' piccolo con `M >= c tau_int(M)`**, ### **`c = 5`** *(il valore dato da Sokal, e quello di `emcee`: e' un numero, ma lo standard, non scelto da me sui dati)*; **l'errore della media `sigma sqrt(2 tau_int / N)`**, **`rho` dalla serie della finestra con la media tolta**, **i campioni ogni `10` tick** *(il passo dei jsonl)* **o ogni `100`** *(le mappe)*.
4. ### **(q-s4) Per `TF3`: il ritmo di emissione dalla pendenza dell'alone.**
5. ### **(q-s5) Il periodo `P` stimato una volta all'inizio dell'allungamento, poi fisso.**
6. ### **(q-s6) `C50-0`: `W = 6000` fino alla prima stima di `P`** *(dopo il pezzo che arriva a `10000`)*, **poi `W = 3 P`.**
- **Il resto come proposto:** **`ST-S` su `S162`, `TB3`, `TBS`** *(«devono risultare stazionari»)*, **`ST-F` su `TF3 + TF3C`** *(non stazionario l'intervallo con la partenza)*; **la lettura «stazionario da `t X` nella finestra osservata», mai «finito».**
- ### ⚠ **Una nota onesta, da dire PRIMA del codice:** **per `S162` da `0` a `10000` lo `ST-S` NON PUO' dare «stazionario»** *(con `W = 6000` il primo arresto possibile e' a `16500`: la tabella della sez. `4.1`, premessa `5`)*. **Luca lo vuole «stazionario»:** ### **su `S162` a `10000` lo `ST-S` stampera' «non stazionario entro `10000`» PER COSTRUZIONE** *(e lo scrivero' accanto, non come fallimento)*; **su `TB3` e `TBS`** *(fino a `30000`)* **si puo'.** **Se Luca lo vuole come DEVE che passa su `S162`, servono finestre piu' corte su quella corsa: una sua decisione.**
- ### ⚠ **E una dal referto di `C35-0`** *(sez. `6` del task history della coppia)*: **le mappe hanno `t` in TICK**: **il codice dell'arresto userà `t * s`** *(lo stesso errore non due volte)*.
- **Avanti:** **il codice degli allungamenti con l'arresto** *(a `C35-pi` finita: `corsa_accensione.py` e' nel suo percorso; un file nuovo per l'arresto si puo' scrivere prima)*, **i DEVE, la cassetta, poi le corse.**

## 6. IL MANDATO DI LUCA DEL `2026-11-08` `00:52`: **GLI ALLUNGAMENTI PARTONO SUBITO, IN PARALLELO ALLE PROVE CORTE** *(le decisioni delle `10:26` e delle `10:50` restano)*

**Le decisioni, come le ha scritte Luca:** **gli allungamenti fino a `30000` partono SUBITO** *(erano in fondo alla coda, dietro il lavoro su `U`)*. ### **ECCEZIONE DICHIARATA a «un calcolo alla volta»:** **UNA corsa lunga alla volta** *(gli allungamenti, in sequenza fra loro)* **gira IN PARALLELO alle prove corte della coda**; **prima di partire memoria e core liberi**; **si scrive di quanto la corsa lunga rallenta mentre girano le prove corte** *(tick al secondo)*; **se le risorse non bastano: i numeri, e si CHIEDE.** **L'ordine:** `C35-0` *(da `10000` a `30000`)*, `C35-pi`, `S162`, `C50-0` *(da `0`)*. **L'arresto per stazionarieta':** **se e' implementato e provato si usa; se NON lo e', la corsa NON aspetta**: gira fino a `30000` con la ripresa e i salvataggi, **e il criterio si applica DOPO, sui dati, come lettura -- dichiarato.** **`R-1` PRIMA di partire.** **Leggi di oggi** *(vuoto `F3`, `cs` spento, `U` congelata, il bordo delle corse originali)*; **nucleo intatto.**

### 6.1 LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

1. ### **L'ARRESTO PER STAZIONARIETA' NON E' IMPLEMENTATO** *(nessun file di `csv/solitone/` contiene `stazionari`: letto dal disco)*. ### **Quindi, come Luca ha deciso: le corse girano fino al tetto `30000`, e il criterio della sez. `5` si applica DOPO, sui jsonl e sulle mappe, come LETTURA** *(«stazionario da `t X` entro la finestra osservata»)*. **Dichiarato.** **I salvataggi:** **gli stati completi di `I1` non sono pronti** *(I1 e' piu' in la' nella coda)*; **restano quelli di oggi**: **il file di ripresa a ogni pezzo** *(`db/accensione_lenta/<nome>.npz`)* **e gli stati completi ogni `1500` unita'** *(`STATI`, su `E:`)*, **estesi a `0 .. 30000`** *(`21`, come `TBS`)*.
2. **Lo stato delle quattro corse** *(letto dai jsonl)*: **`C35-0`, `C35-pi`, `S162`: `7` pezzi, l'ultimo `60000 -> 66667`, `t_fine` `66667`, `fermata` `None`; `7` stati e `7` mappe su `E:`; il file di ripresa c'e'.** **I secondi dell'ultimo pezzo** *(`6667` tick)*: **`2600`, `2739`, `2613`** -- ### **`~0.39`-`0.41` s per tick**, cioe' **`~2.5` tick al secondo.** **`C50-0`: nessun pezzo.**
3. **Il codice che cambia** *(`corsa_accensione.py`, un commit, PRIMA di ogni corsa)*: **`CORSE[<n>] = (1000, 30000)`** per le quattro; **`STATI[<n>]` = `0, 1500, .., 30000`**; ### **un comando `--ripresa <nome>`** *(`R-0`, `R-1`, `R-1-F`)*. **Poi `D6`** *(`LIBRERIA_RIFERITA` sul commit del codice)* **e la cassetta.**
4. ### **`R-1`, COME SI FA PERCHE' SIA LA STESSA CORSA E NON UNA COPIA:** **non riscrivo il ciclo del tick: rigiro `corsa(nome)` STESSA** *(la stessa funzione, lo stesso tick, lo stesso bordo, le stesse misure e mappe)* **in una SABBIERA**: **una cartella dei jsonl con i pezzi FINO A `50000`** *(cosi' il pezzo «prossimo» e' `60000 -> 66667`)*, **una cartella di ripresa con lo stato completo a `t 9000`** *(`<nome>_stato_060000.npz` su `E:`, la stessa forma del file di ripresa)* **piu' la tabella `fase_F3.npz` e il file a `T_acc`**, **una cartella `E:` per mappe e stati**, **e `CORSE[<nome>]` col `t_fine` DELL'ULTIMA RIGA** *(`66667`: con il `30000` nuovo il pezzo andrebbe a `70000`)*. **Le cartelle vere si rimettono nel `finally`.**
   - **`R-0`** *(DEVE PASSARE)*: **gli `sha` del file di ripresa = `sha_fine` dell'ultima riga; gli `sha` dello stato a `60000` = quelli registrati nella riga che lo salvo' = `sha_fine` del pezzo che finisce a `60000`.**
   - ### **`R-1`** *(DEVE PASSARE)*: **il pezzo rifatto nella sabbiera ha `sha_fine` = quello della riga vera, AL BIT, ogni chiave; e i campioni, `D`, `dopo_stato`, il bordo e lo `sha1` del file delle mappe sono gli STESSI.**
   - **`R-1-F`** *(DEVE FALLIRE, il confronto vede una differenza)*: **lo `sha_fine` rifatto = quello dell'ultima riga di un'ALTRA corsa** *(`C35-pi` per `C35-0`, `C35-0` per le altre)*.
   - **E stampa i file del repo che il processo ha importato** *(da `sys.modules`)*: ### **sono i file che NON SI TOCCANO finche' una corsa lunga gira** *(par. `5`: ogni pezzo e' un processo nuovo, che li RILEGGE)*.
5. **Il costo:** **`R-1` `~45` minuti per corsa**; **un allungamento `~200000 - 66667 = 133333` tick, `~14.6` ore a `0.395` s per tick** *(senza le prove corte accanto)*; **`C50-0` `200000` tick, `~22` ore.** ### **La stima vera, e il rallentamento, si misurano** *(sotto)*.
6. **Il disco:** **su `C:` `21` GB liberi** *(il FERMO e' sotto `6`)*, **su `E:` `212`** *(misurati con `df`)*; **la RAM `13.1` GB libera su `34.1`, `12` core logici** *(`6` fisici)*, **la CPU al `5`%** *(misurati con `psutil`, prima di partire: nessun mio processo python in volo)*.
7. **Che cosa NON so:** **se `R-1` passa al bit** *(il bordo e le mappe dentro `corsa` sono deterministici, ma non l'ho mai rifatto)*; **di quanto le prove corte rallentano la corsa** *(`numpy` usa piu' thread: due processi se li contendono)*.

### 6.2 PROGETTAZIONE *(le letture si fissano QUI)*

- **IL RALLENTAMENTO, come si misura:** ### **i secondi per tick di ogni pezzo** *(il campo `secondi` del jsonl diviso i tick del pezzo)*, **confrontati con i pezzi `6`-`7` delle corse originali** *(`~0.39`-`0.41` s per tick, senza prove accanto)*; **per ogni pezzo si scrive se una prova corta girava accanto e quale** *(dai miei log, con gli orari)*. **Il numero: `tick al secondo` con e senza prove, e il rapporto.**
- ### **IL FERMO PER LE RISORSE** *(Luca: «se non bastano, i numeri e CHIEDERE»)*: **la RAM libera sotto `4` GB, o `C:` sotto `6` GB, o una prova corta che rallenta la corsa di piu' del doppio** -- ### ⚠ **queste tre soglie sono MIE, e le DICHIARO come soglie di AVVISO, non di fisica:** **quando una scatta mi fermo e chiedo, non decido.**
- **L'ordine:** **(1)** il codice e il suo commit; **(2)** `D6` e la cassetta; **(3)** `R-1` su `C35-0`; **(4)** se passa, l'allungamento di `C35-0` in background *(il driver dei pezzi, con il file-semaforo `FERMA`)*; **poi `R-1` di `C35-pi` e il suo allungamento, `R-1` di `S162` e il suo, `C50-0` da `0`.**
- **I referti:** a fine corsa **`carta_coppia`** *(la stessa carta di `838e4b45`: `d`, `E_int`, la fase relativa, `A-S` col limite del caos, l'assorbito)*, **coi tempi dei profili estesi a `30000`** *(un cambio di codice di `carta_coppia.py`, committato prima di girarla)*, **e la LETTURA di stazionarieta' della sez. `5`** *(un file nuovo, coi suoi DEVE `ST-P`, `ST-B`, `ST-I`, `ST-S`, `ST-F`: si scrive mentre le corse girano, perche' non e' nel loro percorso)*.
- **Che cosa mi fa FERMARE:** **`R-0` o `R-1` che falliscono** *(la ripresa non e' la corsa)*; **`R-1-F` che passa**; **la cassetta che non passa**; **le soglie delle risorse.**

### 6.3 TODO

1. **Questa sezione, la MAPPA: commit e push.**
2. **`corsa_accensione.py`:** `CORSE`, `STATI`, `ripresa()` e `--ripresa`; l'INVENTARIO col blob; commit e push.
3. **`D6`** *(`LIBRERIA_RIFERITA`)* **e la cassetta:** commit e push.
4. **`--ripresa C35-0`** *(in background)* -> il referto `doc/referti_l2/ripresa_C35-0.txt`, commit e push.
5. **Se passa: il driver dei pezzi di `C35-0` in background; la riga della MAPPA «allungamenti in corso» con la stima d'arrivo; commit e push.**
6. **Accanto, la coda corta:** IS3 q1/q2 *(`carta_statiche.py`: NON e' nel percorso della corsa, da verificare con la lista di `R-1`)*, poi B1, I1/I3, T1-T5.

### 6.4 LA CASSETTA DOPO `D6` SU `e726ae0e`: `107/108` -- **FALLISCE `D6` (l'isolamento), UN MIO ERRORE**

- **`csv/_u1_oggi.py` e `csv/_u1_carica_e.py` importano la libreria da FUORI `csv/solitone/`** *(miei, `2026-11-07`, senza la cassetta dopo)*. **Gli altri `107` controlli passano**: **i test della libreria e il `D6` dei blob.**
- ### **Il criterio della sez. `6.2` («la cassetta che non passa» mi ferma) era scritto per PROTEGGERE LA CORSA:** **la parte della cassetta che la protegge** *(i test della libreria al bit, nessun `.py` della libreria cambiato)* **PASSA.** **Quindi: lo stato e il fallimento committati; la cura** *(i due script in `csv/solitone/`)* **un commit a se'; `R-1` parte accanto, dichiarato.** **Se Luca la legge diversamente, mi fermo.**
