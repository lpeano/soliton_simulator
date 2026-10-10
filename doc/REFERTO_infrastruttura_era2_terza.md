# IL REFERTO DELLA TERZA PARTE — **il mandato `4` di `6`**

> ### ⛔ **CONGELATO** *(la forma dichiarata il `2026-10-10`: `csv/_forma_referti.py`)*: questo e- un ### **REPERTO**, cioe- ### **che cosa si e- misurato A UN ISTANTE** — ### **la CI NON lo rigenera**, e il presidio verifica ### **il suo BLOB**. ### **Per rimisurarlo si rigira il suo comando AL SUO COMMIT**, come un sigillo *(`CLAUDE.md` par. `6`)*.

> ### ⛔ **Questo file e' GENERATO da `python csv/_referto_terza_parte.py`: non si scrive a mano, e NESSUN numero e' ricopiato** *(`L-NUMERI`)*.
> **Il simulatore:** `b8c21049`, ### **non toccato.** **Nessuna fisica nuova:** la tabella ha ancora ### **`3` leggi, tutte `prova: true`.**

### ⭐ **QUESTO MANDATO ERA DI IRRIGIDIMENTO: ha preso cose che FUNZIONAVANO PER ABITUDINE e le ha rese OBBLIGATORIE.** Il piano, scritto due mandati prima, lo diceva di una di esse: la forma bilineare era *«gia' vera senza essere una regola»*, e ### **finche' il generatore non la pretende e' un'abitudine.**

---

## `1.` I SETTE PUNTI, e il collaudo di ognuno

| | il punto | il presidio | il collaudo |
|---|---|---|--:|
| `1` | DETERMINISMO | `P-DET` | ### ✅ **`14`/`14`** |
| `2` | DIMENSIONI | `P-DIM` | ### ✅ **`34`/`34`** |
| `3` | SIMMETRIE E CONSERVAZIONI | `P-SIM` | ### ✅ **`13`/`13`** |
| `4` | IL GRAFO VALIDO A OGNI PASSO | `P-GRAFO` | ### ✅ **`11`/`11`** |
| `5` | HOOK COME BARRIERA, CI COME RETE | `P-BARRIERA` | ### ✅ **`11`/`11`** |
| `6` | I TEMPI, E UN SOLO COMANDO | `P-TEMPI` | ### ⛔ **FALLISCE** *(codice `1`)* |
| `7` | LA GUIDA, ESEGUITA | `P-GUIDA` | ### ✅ **`12`/`12`** |
| | ### **IN TUTTO** | | ### ⛔ **`95`/`95`** -- e 1 collaudi NON sono pieni: `0`/`0` |

---

## `2.` I NUMERI MISURATI

| | |
|---|--:|
| i collaudi del comando unico | `### **QUALCUNO FALLISCE**` |
| il `pre-commit` | `84.75` s su un budget di `120` |
| i LENTI, solo in CI | `74.76` s |
| in tutto | `159.51` s |
| la macchina | Windows AMD64, python 3.13.2 |

| il determinismo | |
|---|--:|
| usi di `random` sotto `primo_ordine/` | `7`, di cui GLOBALI `0` |
| due processi, stessa configurazione | ### **byte-identici** |

| le conservazioni, e le soglie ### **DERIVATE** | la deriva | la soglia |
|---|--:|--:|
| `NORMA` *(`passi * eps`: invariante quadratico)* | `1.853e-15` | `4.441e-14` |
| `ENERGIA` *(`dt^2`: metodo simmetrico)* | `3.979e-05` | `1.000e-04` |

### ⭐ **E LE DUE SOGLIE SONO LONTANE DI NOVE ORDINI DI GRANDEZZA, che dice una cosa VERA: la norma e' conservata DALLA STRUTTURA del metodo, l'energia solo APPROSSIMATA.** ### **Dichiararle con la stessa soglia nasconderebbe esattamente questo.**

| il grafo, controllato A OGNI PASSO | |
|---|--:|
| il controllo | `37.584` us |
| un passo GLOBALE | `612.3` us |
| ### **il rapporto** | ### **`6.1383`%** |
| archi scambiati TUTTI | ### **stesso stato AL BIT** |

---

## `3.` CHE COSA I PRESIDI MI HANNO DETTO — ### **e tre volte hanno cambiato il DISEGNO, non una riga**

| | il presidio | che cosa ha visto |
|---|---|---|
| `1` | `P-MOD` | `grafo.py` NON era in mappa, e `passo.py` chiamava `controlla` senza dichiararla |
| `2` | ### **`P-MOD`** | ### ⭐ **IL COLLAUDO DI UN MODULO CHE STA IN FONDO ALLA CATENA DEGLI IMPORT NON PUO' VIVERE DENTRO QUEL MODULO:** il collaudo di `grafo.py` importava `driver` e `passo`, e `passo` importa `grafo` — ### **un CICLO.** ### **E' la stessa ragione per cui `_collauda_passo.py` esiste, e NON L'AVEVO CAPITA** |
| `3` | ### **`P-MOD`** | ### ⭐ **`_genera.py` a `738` righe sul tetto di `700`: *«oltre SI DIVIDE, NON SI ALLUNGA»*.** ### **Alzare il tetto sarebbe stato esattamente la manopola che `A1` vieta** |
| `4` | `P-ES1` | tre collaudi AVANZANO LO STATO, e le eccezioni vanno DICHIARATE col loro perche' di almeno `40` caratteri |
| `5` | `P-C1` | le voci `P-GRAFO` e `P-TEMPI` risultavano ### **tende**: le `SORGENTI` guardavano ### **solo `csv/`**, e un presidio puo' vivere ### **sotto `primo_ordine/`** |
| `6` | `P-RIF` | gli ID `P-C1`, `P-MOD` e `A16` stavano ### **in COMMENTI**: un riferimento che una macchina deve seguire ### **non vive nella prosa.** ### E al terzo giro ### **ha colto SE STESSO** |
| `7` | `P-E6` | la tabella cambiava e ### **la riga del registro dell'era `2` non era nel commit**: porta ### **l'IMPRONTA** della legge, e senza di lei il registro dichiara l'impronta di una tabella ### **che non esiste piu'** |
| `8` | `H-P5` | l'esenzione era ### **dentro il docstring**, dove ### **non e' un commento** |
| `9` | `PI-FISICA-ERA1-NON-SOSPESA` | una voce dell'era `1` non chiusa e' ### **`SOSPESA`**, e lo stato dell'era `1` va in `stato_era_1` |
| `10` | `PI-STORICO-SENZA-COMMIT` | ### **otto volte**, e il rito e' sempre lo stesso: `python csv/indice.py storico-commit` |
| `11` | ### **`P-BARRIERA`** | ### ⭐ **MI HA FERMATO UN'ORA DOPO AVERLA SCRITTA:** ho cambiato il `pre-commit` e lo strumento dell'indice ### **si e' rifiutato di partire.** ### **L'ordine e': si cambia un hook, POI `--scrivi`, POI gli strumenti** |
| `12` | ### **`P-TEMPI`** | ### ⭐ **UNA MIA CLASSIFICAZIONE ASSERITA INVECE CHE MISURATA:** il collaudo della catena era dichiarato *«oltre `120` secondi»* e ### **costa `2.55`.** ### **Quel numero era di un'altra cosa** |

### ⚠ **DODICI CORREZIONI IN SETTE PUNTI, e il numero che conta e' un altro: TRE hanno cambiato il DISEGNO.** ### **Due volte `P-MOD` mi ha detto dove deve vivere un collaudo** *(fuori dal modulo che collauda, se quel modulo sta in fondo alla catena degli import)*, ### **e una volta mi ha impedito di alzare un tetto** — che e' la manopola piu' facile di tutte.

---

## `4.` CHE COSA HO SBAGLIATO IO — ### **e due previsioni, una tenuta e una no**

| | l'errore o la previsione | l'esito |
|---|---|---|
| `1` | la trappola `(a)` del task history: *«il punto `5` puo' ROMPERE LA CI»* | ### ✅ **TENUTA.** Nella CI i hook ### **non sono attivi**, e il mandato preso alla lettera ### **avrebbe fatto fallire SEMPRE la CI.** ### **La barriera TACE fuori dal PC, e lo DICHIARO come mia inferenza** |
| `2` | la trappola `(b)`: *«due processi NON daranno file byte-identici, perche' un `.npz` e' uno ZIP e porta la data»* | ### ⛔ **SBAGLIATA**, e il perche' e' MISURATO: `numpy.savez` scrive `date_time = (1980,1,1,0,0,0)` — ### **AZZERA l'ora.** ### ⭐ **E l'ho verificato in ENTRAMBE le direzioni: prima le due corse, POI l'intestazione dello ZIP — perche' due corse a meno di `2` secondi starebbero nella stessa finestra, e il braccio sarebbe un FALSO-UNO** |
| `3` | il controllo dimensionale dentro `valida_legge`, che leggeva le dimensioni ### **da `variabili`** | ### ⛔ **SALTAVA IN SILENZIO**, e i `34` collaudi dello schema ### **passavano tutti** mentre il generatore ### **accettava `K` di dimensione `E^2`.** ### **Visto solo rompendo la tabella a posta e guardando il codice d'uscita** |
| `4` | il timbro del determinismo | ### ⚠ **STAVA PER MENTIRE:** `avvia()` dice *«ero in tempo?»* e il timbro ### **lo richiama quando `numpy` c'e' gia'** — il driver lo chiama in tempo e il timbro diceva `false`. ### **Curato: il verdetto e' quello della PRIMA chiamata** |
| `5` | <<zero sostituzioni = falso-uno>> nelle simmetrie | ### ⛔ **TROPPO STRETTO**, e il collaudo me l'ha detto rifiutando la mia riga di prova: zero sostituzioni di `U(1)` su una legge ### **senza `psi`** e' ### **invarianza VERA**; `SCAMBIO-DEI-CAPI` con zero sostituzioni ### **e' un falso-uno** |
| `6` | il braccio di `P-ID` che cercava `` `D4` `` ### **come SOTTOSTRINGA** | ### ⛔ **FALSO FALLIMENTO:** `D4` compariva ### **nella DOMANDA di un'altra voce.** ### **E' lo stesso errore di una regex che non distingue un commento da un uso: il TERZO della giornata** |
| `7` | lo split di `_genera.py`, al primo tentativo | ### ⛔ **HO ASSUNTO che `def collaudo()` venisse PRIMA di `def main()`:** il mio slice ha ### **DUPLICATO una regione** e il file si e' ritrovato con ### **due `main`.** ### **Ripristinato dai byte committati e rifatto GUARDANDO l'ordine vero** |
| `8` | un'asserzione in uno script di patch | ### ⛔ **Cercava la parola `--prova` nel testo, e IL COMMENTO CHE INSERIVO LA CONTENEVA:** diceva *«non togliato»* mentre il ramo era via. ### **Adesso guarda `return collaudo()`, cioe' IL CODICE** |

### ⭐ **E LA COSA CHE QUESTE OTTO RIGHE DICONO INSIEME: SEI SU OTTO SONO STATE TROVATE FACENDO GIRARE QUALCOSA, NON RILEGGENDO.** ### **Due le ho viste perche' ho guardato un'uscita DOPO averla scritta** *(il timbro, i tempi)*, ### **e una perche' ho rotto la tabella A POSTA.**

---

## `5.` CIO' CHE RESTA APERTO — ### **scritto, non taciuto**

| | |
|---|---|
| ### **il numero di thread** | ### **NON si verifica**: `threadpoolctl` non e' installato. ### ✅ **Ma i due processi byte-identici dicono cio' che quella verifica direbbe:** se coincidono, i thread ### **non stanno rompendo il determinismo** |
| ### **la CI** | ### **mai osservata girare**, e il passo di `P-BARRIERA` e' il posto dove ### **la mia inferenza sul silenzio in CI si vedrebbe cadere.** ### **La differenza fra <<scritto>> e <<osservato>> e' quella fra una tenda e un muro** |
| ### **`--no-verify`** | ### **NON e' impedibile in locale**, e nessuno strumento puo' accorgersene ### **perche' non viene chiamato.** ### **Lo trova la CI, che non impedisce: FA VEDERE** |
| ### **l'impronta dei hook** | e' in un file ### **tracciato**: chi cambia un hook puo' cambiare anche lei. ### **La barriera non lo impedisce, lo rende VISIBILE IN UNA DIFF** |
| ### **una legge prima della sua decisione** | ### **nessun presidio lo impedisce.** `P-ALB` guarda le ### **decisioni**, non le leggi — e la guida lo dichiara come ### **il suo passo `1`**, che oggi ### **ferma tutto** |
| ### **`H-FISICA-FUORI-LISTA`** | legge la lista ### **dal DISCO**: una modifica non committata ### **autorizza un commit.** ### **Aperto dal mandato `1`** |

---

## `6.` L'ORDINE E' VERIFICABILE DA GIT, non asserito da me

Il task history di questo mandato e' il commit ### **`e2781da`**, e per il rito del par. `8` e' ### **antenato di ogni commit del lavoro.**

### ✅ **Verificato adesso con `git merge-base --is-ancestor`: `e2781da` E' antenato di `HEAD`.**

