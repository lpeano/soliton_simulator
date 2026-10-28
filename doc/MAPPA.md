# LA MAPPA DEL LAVORO — lo stato, in un posto solo

> ### **LA FONTE DELLO STATO DEL LAVORO** *(la decisione di Luca del `2026-10-27`, `21:41`; [[MAPPA-DEL-LAVORO]])*: ### **il guardiano non ha memoria fra le sessioni, quindi lo stato sta QUI, nel repo.**
> ### **LA REGOLA DI MANUTENZIONE:** ### **ogni commit che chiude un referto o registra una decisione aggiorna la riga che lo riguarda, NELLO STESSO COMMIT** *(nei FILE CAMBIATI)*; ### **la regola sta in `doc/PATTERN_DI_PROVA.md`.**
> ### **LA REGOLA DI LAVORO** *(`2026-10-27`)*: ### **niente domande nuove in esecuzione finche' non arrivano le risposte che decidono la direzione** *(la sezione `3`)*; ### **le idee nuove vanno nella LISTA IN ATTESA** *(la sezione `4`)*, ### **non in coda.**
> ### **Aggiornata al:** `2026-10-28`, mattina *(lo zero del vuoto chiuso; la domanda sulla chiralita' in attesa; la bussola, sezione `6`; la domanda sulla gobba del vuoto in attesa, `10:40`)*.

## 1. CHE COSA FUNZIONA, MISURATO

| | il fatto | il commit |
|---|---|---|
| 1 | ### **la scena a triangoli nel nucleo** *(al bit contro quella in memoria)* | `36040a07`, `2d996edc` |
| 2 | ### **la luce isotropa, e a `1` nel tempo proprio** | `0764d566`, `afba052b` |
| 3 | ### **la gravita' senza curvatura, attrattiva e universale** *(con lo zero simmetrico)* | ### **lo zero simmetrico** *(`_segno_gravita`, `_zero_simmetrico`)* |
| 4 | ### **la materia mai oltre la luce** *(`v_max/s 0.5992864` a `r 1`)* | `afba052b` |
| 5 | ### **i difetti non intrappolano** *(nessuno stato legato al difetto)* | `74b4bce4` |
| 6 | ### **la geometria del conteggio per la LUCE:** ### **il cono converge di `pi/3`, niente `1/b`** | `b99ba2b1` |
| 7 | ### **e per la MATERIA:** ### **la materia converge di `pi/3` entro lo `0.1%`** *(la luce entro lo `0.3%` a `b 24`)*; ### **il fascio che attraversa la cucitura esce tutto in `K'`;** ### **la voce `LUCE-MATERIA-CONO` CHIUSA** *(con le due cautele)* | `e48e7414`, `e2df0e2e` |
| 8 | ### **il solitone esiste col vuoto FERMO** *(`N 1e6`, stabile fino a `2000` tick)* | `74f99039` |
| 9 | ### **con lo zero fisico il legame e' il `63%` dei costituenti, il solitone il `37%`** | `0fb93b8c`, `442b704a` |
| 10 | ### **il vuoto da solo e' STABILE, non solo stazionario** | `532598c7` |
| 11 | ### **`H_tot` conservata a `O(s^2)` col risolutore a ogni `s`** *(i rapporti `3.25`, `3.69`, `3.95`; a `s 0.075` la deviazione e' lo `0.49%` della perdita del vuoto)* | `99eb7a42` |
| 12 | ### **il legame e' coerente: il vuoto riceve la rotazione gemella** *(`S1` e `S3`)* | `acbdfb88` |
| 13 | ### **i pesi del passo = quelli di `termini_di_h`** *(`H_tick = H_tot`)* | `a33daa09` |
| 14 | ### **la carica `sigma_z` a due segni, conservata a `eps 0`** | `8dea8c95` |
| 15 | ### **lo strumento del libro dei conti conta giusto** *(i conti di `15df5c63` a `1e-16`; la strada `A`)* | `4f6a4bd7` |
| 16 | ### **dal vuoto del FONDO il vuoto prende energia dalla materia** *(il verso si rovescia; a `s 0.075`)* | `76eecbf5` |

## 2. CHE COSA NON FUNZIONA ANCORA, E PERCHE'

| | il fatto | il perche', per quanto si sa | il commit |
|---|---|---|---|
| 1 | ### **il solitone si scioglie col tick intero** *(vive `320` tick a `N 1e6`)* | ### **il vuoto gli cede energia;** ### **il verso regge, la spartizione si fida da `s 0.075`** | `15df5c63`, `abd5a809`, `99eb7a42` |
| 2 | ### **la nascita libera energia che il vuoto uniforme non prende** | ### **il vuoto uniforme e' al massimo;** ### **lo spostamento dello zero NON e' il canale** *(chiuso, Luca `08:31`)*; ### **dove va resta aperto: da riprovare dal vuoto del fondo** *(`76eecbf5`)* | `d999cca7`, `f7ee87a9`, `43c3a298` |
| 3 | ### **il vuoto uniforme e' il MASSIMO del generatore** | ### **per la FORMA** *(`-pi` per due proiettori)*; ### **il fondo a `-2 pi` e' un flusso, torsione `pi`** | `787296da` |
| 4 | ### **`v_b` della materia = `pi/4` della luce** | ### **una violazione di Lorentz a bassa energia della materia NUDA** | `b0edae62`, `afba052b` |
| 5 | ### **la particella elementare pesa quanto la grana** | -- | `25cada4e` |
| 6 | ### **lo spazio curvo non nasce ancora dalla materia** | ### **la curvatura e' imposta** *(il cono scritto nel grafo)* | -- |
| 7 | ### **`A1` chiusa** | ### **la luce va come `cs^2`** | `31ee70cc` |
| 8 | ### **il punto fisso di `cs` non converge col solitone, gia' al tick `0`** | ### **la voce aperta [[PUNTO-FISSO-CS-SOLITONE]]; si riprende dopo il vuoto sul fondo** | `76e85c0a`, `05c080f8` |
| 9 | ### **il driver non fa girare la camminata** | ### **e' la pipeline delle leggi di PROVA** *(l'errore `n.68`)* | -- |

## 3. LE DOMANDE CHE DECIDONO LA DIREZIONE

| | la domanda | lo stato | il commit |
|---|---|---|---|
| `a` | ### **la materia sul cono come la luce?** | ### **SI'** | `e48e7414` |
| `b` | ### **il vuoto in cima e' la causa dei due problemi** *(il solitone che si scioglie, la nascita)*? | ### **IN PARTE:** ### **il vuoto uniforme e' il massimo per la forma;** ### **dal fondo il vuoto PRENDE energia dalla materia** *(il verso si rovescia)*, ### **ma il solitone vive solo `1.6`-`1.9` volte di piu', non `4`: c'e' un'altra causa** | `787296da`, `76eecbf5` |
| `c` | ### **dove va l'energia, nei due versi?** | ### **lo strumento c'e'** *(la strada `A`)*: ### **il vuoto lontano rimanda indietro** *(`915` tick in entrata su `1860` dopo la vita)* | `4f6a4bd7` |

## 4. LA LISTA IN ATTESA *(idee da NON eseguire finche' la sezione `3` non e' chiusa)*

| | l'idea | dove sta |
|---|---|---|
| 1 | ### **il cono di luce emergente** | [[DOMANDA-CONO-EMERGENTE]] *(`ceba2925`)* |
| 2 | ### **la torsione come quanto d'azione; la mitosi dove gli orologi differiscono** | `doc/PROGETTO_MITOSI.md` 3(a); ### **in forma d'energia col `cs` spento** *(`80dc4d4a`)*: ### **il ritmo massimo sul bordo della buca, nessun freno;** ### **col `cs` acceso BLOCCATA** *([[PUNTO-FISSO-CS-SOLITONE]])* |
| 3 | ### **la materia accoppiata alla luce** | `doc/PROGETTO_U1.md`; [[PROGETTO-MASSA-COLLETTIVA]] *(l'ordine dei lavori)* |
| 4 | ### **il solitone con la sua buca** | ### **PROMOSSO** *(Luca, `22:59`)*: ### **IN CORSO** *(lo script `327e5ad8`; le corse della rampa girano)* |
| 5 | ### **lo zero del vuoto** *(l'ipotesi di Luca delle `01:26`)* | ### **CHIUSA come canale di gravita'** *(Luca, `2026-10-28` `08:31`)*: ### **l'additivo a bande opposte, il proporzionale e' un altro modo di scrivere `cs`** *(`43c3a298`, [[ZERO-DEL-VUOTO]])* |
| 6 | ### **i nodi ciascuno al proprio ritmo** | -- |
| 7 | ### **due solitoni che si attraggono attraverso il vuoto** | -- |
| 8 | ### **la nascita in un vuoto a somma nulla per nodo** | `doc/PROGETTO_MITOSI.md` 3(c) |
| 9 | ### **la banda di sotto come antimateria** | [[DOMANDA-BANDA-ANTIMATERIA]]; ### **la lettura delle `08:31`: per un potenziale additivo le due bande gia' come cariche opposte** *(una lettura, non una misura; `43c3a298`)* |
| 10 | ### **la valle come carica** *(e il momento angolare modulo `6`)* | [[DOMANDA-VALLE-CARICA]] |
| 11 | ### **la chiralita': quale grandezza del modello e'?** *(la moneta di spin, le due componenti che il salto a `K` mescola, le valli `K`/`K'`)* | [[DOMANDA-CHIRALITA]] *(Luca, `2026-10-28` `08:52`; `doc/TASK_HISTORY/2026-10-28_chiralita.md`)*; ### **si apre insieme alle due domande sulla carica** |
| 12 | ### **la gobba del vuoto e il segno della gravita':** ### **sul fondo la massa fa un pozzo o una collina di `cs`, e la materia di prova cade verso la massa o se ne allontana?** *(una lettura della prova breve, non una misura: `Lambda` `4.30` al centro contro `0.97` lontano)* | [[DOMANDA-GOBBA-SEGNO-GRAVITA]] *(Luca, `2026-10-28` `10:40`; `doc/TASK_HISTORY/2026-10-28_gobba_segno_gravita.md`)*; ### **si apre dopo il referto della rampa e dopo [[PUNTO-FISSO-CS-SOLITONE]]** |

## 5. LE DECISIONI APERTE DI LUCA *(con la raccomandazione del guardiano)*

| | la decisione | la raccomandazione |
|---|---|---|
| 1 | ### **`S1` contro `S4`** | ### **`S1`, dopo il vuoto sul fondo** |
| 2 | ### **lo zero nel nucleo** | ### **il simmetrico e' quello fisico; il nucleo non si tocca ora** |
| 3 | ### **`cs` per estremita' o per nodo** | ### **per estremita', se si fa la mitosi** |
| 4 | ### **le forme della mitosi** | -- *(`doc/PROGETTO_MITOSI.md`)* |
| 5 | ### **la carica, la costante, il campo compatto** | ### **la norma provvisoria, una costante debole di prova, compatto** *(`doc/PROGETTO_U1.md` par.`8`, `8-bis`)* |
| 6 | ### **il driver della camminata** | ### **`7` domande, non urgente** |
| 7 | ### **la moneta di spin (`eps`)** | ### **la sua origine fisica e' aperta;** ### **spegnerla rende la carica `sigma_z` conservata, ma la riduce a «due specie separate»** |

## 6. LA BUSSOLA: CHE COSA SERVIREBBE PER UN SISTEMA COMPLETO *(Luca, `2026-10-28` `08:58`)*

> ### **«Nessuna teoria della gravita' quantistica oggi ha un sistema completo; questa bussola serve a sapere con precisione che cosa manca, non a misurare un ritardo.»**
> ### ⛔ **NON E' UNA CODA E NON E' LA LISTA IN ATTESA: E' UN ORIENTAMENTO.** ### **Nessuna voce di questa sezione si esegue senza essere prima promossa** *(alla lista in attesa, poi alla coda)* ### **da una decisione di Luca.**

### `(A)` CIO' CHE C'E', ALMENO IN PARTE

| | che cosa | dove |
|---|---|---|
| 1 | ### **la luce e il campo `U(1)` con la legge di Gauss** | `doc/PROGETTO_U1.md`, [[PROGETTO-U1]] |
| 2 | ### **la gravita' come «lo spazio dice alla materia come muoversi»:** ### **la caduta da `cs`; il cono per luce e materia** | ### **la sezione `1`, righe `3`, `6`, `7`;** `e48e7414` |
| 3 | ### **l'energia e i suoi bilanci** | [[LIBRO-DEI-CONTI]] *(`4f6a4bd7`)* |
| 4 | ### **il vuoto e la sua posizione nello spettro** *(in cima o sul fondo)* | `787296da`, `76eecbf5` |
| 5 | ### **la massa come legame; l'oggetto collettivo** *(il solitone con la sua buca, in coda)* | `0fb93b8c`; [[PROGETTO-MASSA-COLLETTIVA]] |
| 6 | ### **la carica, la chiralita', il cono di luce unico** | ### **la lista in attesa** *(righe `1`, `9`, `10`, `11`)* |

### `(B)` CIO' CHE SAPPIAMO MANCARE *(solo i titoli)*

| | che cosa | dove |
|---|---|---|
| 1 | ### **la seconda meta' della gravita': la materia che curva lo spazio** *(la regola della mitosi)*; ### **senza, ne' la legge di Newton nel suo limite ne' le onde gravitazionali** | `doc/PROGETTO_MITOSI.md`, [[PROGETTO-MITOSI]]; ### **la sezione `2`, riga `6`** |
| 2 | ### **il `3+1`: tutto e' in 2D** | `doc/PIANO_2D_3D.md` *([[PIANO-2D-3D]])*, `doc/PROGETTO_FCC.md` |
| 3 | ### **l'invarianza di Lorentz:** ### **i due coni** *(`v_b = pi/4`)*; ### **le fette** *(i nodi ciascuno al proprio ritmo)* | ### **la sezione `2`, riga `4`** *(`b0edae62`, `afba052b`)*; ### **la lista in attesa, riga `6`** |
| 4 | ### **il dizionario con le unita' fisiche** | [[DECISIONE-L1-NATURA-A-SIMULATORE-B]] |
| 5 | ### **le altre forze:** ### **la debole** *(la sola che distingue la chiralita')*; ### **la forte;** ### **il fork `SU(2)` dell'era `1` come inizio** | ### **il ramo `fork-su2`;** [[DOMANDA-CHIRALITA]] |

### `(C)` LE DOMANDE NON ANCORA FATTE *(le piu' profonde per prime)*

| | la domanda | dove |
|---|---|---|
| 1 | ### **MOLTE PARTICELLE E LA STATISTICA:** ### **il modello e' un'onda sola; fermioni e bosoni;** ### **e' lo stesso nodo della carica `(a)`;** ### **senza, il modello e' una teoria di campi classici** | [[DOMANDA-BANDA-ANTIMATERIA]] |
| 2 | ### **LA MISURA E LE PROBABILITA':** ### **la regola di Born e il risultato unico di una misura in una camminata deterministica e reversibile;** ### **la meccanica quantistica relazionale ha una risposta sua** | -- |
| 3 | ### **LE CONSERVAZIONI DELL'IMPULSO E DEL MOMENTO ANGOLARE:** ### **sulla griglia solo in forma ridotta;** ### **nel limite continuo da controllare** | [[DOMANDA-VALLE-CARICA]] *(il momento angolare modulo `6`)* |
| 4 | ### **LA COSMOLOGIA:** ### **se i nodi solo nascono l'universo cresce: con quale ritmo, da quale stato iniziale;** ### **l'energia del vuoto e la costante cosmologica** | `787296da` |

## 7. LA CODA DI OGGI, IN ORDINE *(`PRECEDENZA-IN-CODA`)*

| | il lavoro | lo stato |
|---|---|---|
| 1 | ### **il vuoto sul fondo `(c-iii)`: il solitone dal fondo a `s 0.075`** *(`F0` la scelta di Luca, `F1`-`F3` la famiglia)* | ### **FATTO: `5/6`** *(`76eecbf5`)* |
| 2 | ### **lo zero del vuoto** *(l'ipotesi di Luca delle `01:26`; il testo nella relazione e in `PROGETTO_MITOSI` 3(c))* | ### **CHIUSO:** ### **la DEVE `(0)` entro `1e-12` relativo, `1/3`** *(Luca `08:31`; il commit di `zero_del_vuoto_c0.txt`)*; ### **l'ipotesi come canale di gravita' chiusa** *(`43c3a298`)* |
| 3 | ### **il solitone con la sua buca** *(la rampa del vuoto; il mandato delle `22:59`)* | ### **IL PROSSIMO** |

## 8. GLI ERRORI DEL GUARDIANO, DAL `n.54`

| | l'errore | dove |
|---|---|---|
| `n.54` | ### **la coda in 2D scritta come misurata** | `RELAZIONE_PER_CLAUDE.md` |
| `n.55` | ### **le rotazioni dello spazio in 2D: solo `U(1)`; lo spin interno resta `SU(2)`** | `RELAZIONE_PER_CLAUDE.md` |
| `n.56` | ### **una delle tre imprecisioni della sezione `G`** | `RELAZIONE_PER_CLAUDE.md` |
| `n.57` | ### **i numeri di `a/a_H`** | ### **nel mandato** |
| `n.58` | ### **`L ~ 1/1.37`** | ### **nel mandato** |
| `n.59` | ### **NON REGISTRATO NEL REPO** | -- |
| `n.60` | ### **NON REGISTRATO NEL REPO** | -- |
| `n.61` | ### **una proprieta' locale del passo: si misura gia' in 2D** | `doc/PROGETTO_U1.md` |
| `n.62` | ### **la soglia andava ricavata dalla grandezza di `A`** | `RELAZIONE_PER_CLAUDE.md` |
| `n.63` | ### **aveva consigliato una soluzione** *(il compatto modulo `2 pi/e`, il `chi` piccolo)* ### **che non poteva passare** | ### **nel mandato** |
| `n.64` | ### **la previsione `x(r) = r/4` cade** *(la massa sente `r` a meta')* | `RELAZIONE_PER_CLAUDE.md` |
| `n.65` | ### **le unita'** *(`c = r s` archi per tick = `r` per tempo proprio)* | `RELAZIONE_PER_CLAUDE.md` |
| `n.66` | ### **la DEVE a `1e-4` su un riferimento non verificato** *(`v_max/s`)* | `doc/TASK_HISTORY/2026-10-25_curvatura_0bis.md` |
| `n.67` | ### **NON REGISTRATO NEL REPO** | -- |
| `n.68` | ### **il driver creduto il programma della camminata** *(e' la pipeline delle leggi di prova)* | `RELAZIONE_PER_CLAUDE.md` |
| `n.69` | ### **il riferimento di Dirac creduto a `v_max/v_b = 1`** *(e' `2/sqrt 3`)* | `RELAZIONE_PER_CLAUDE.md` |
| `n.70` | ### **`D7` raccomandata senza controllare le dipendenze dell'albero** | `RELAZIONE_PER_CLAUDE.md` |
| `n.71` | ### **la raccomandazione delle `01:17` non controllo' la diagnosi** *(la causa era il segno del tempo)* | `doc/TASK_HISTORY/2026-10-27_c2_materia.md` |
| `n.72` | ### **il vuoto «stazionario» non provato stabile** *(risolto dalla misura: stabile)* | `RELAZIONE_PER_CLAUDE.md`, `532598c7` |
| `n.73` | ### **la premessa «la corrente d'energia gia' nel nucleo»:** ### **e' di un'altra energia** | `RELAZIONE_PER_CLAUDE.md` |
| `n.74` | ### **ANNULLATO** *(Luca, `21:27`)*: ### **«il passo conserva `H_tot` a meno di `O(s^2)`» era GIUSTO** | `aa03a6c1` |
| `n.75` | ### **alle `19:25` ha accettato la non conservazione da un confronto con stati di partenza non confrontabili** *(`998203e9`)* ### **e ha chiamato errore un'affermazione corretta** | `aa03a6c1` |
