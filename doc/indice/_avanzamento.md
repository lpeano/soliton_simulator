# L'AVANZAMENTO DELLA FASE `2` — **dove siamo, e il comando per riprendere**

> ### ⛔ **QUESTO FILE SI AGGIORNA A OGNI LOTTO**, con un commit e un push. Se il lavoro si
> interrompe, ### **si riparte da qui senza rifare niente.**

| | |
|---|---|
| ramo | `primo-ordine` |
| punto di ritorno | tag ### **`pre-indice-v2`** *(prima dello schema `2`)* |
| schema in vigore | ### **`3`** *(la classe `NON_DEFINITA`)* |
| simulatore | `b8c21049`, ### **non toccato** |

---

## ✔ **FATTO**

| | |
|---|---|
| ### **schema `3`** | la classe ### **`NON_DEFINITA`** nel vocabolario, col validatore che la ### **vieta** con uno stato diverso da `DA_CLASSIFICARE`. Collaudo: ### **`21` su `21`** *(due casi nuovi: `NON_DEFINITA` con `APERTA` ### **rifiutata**, e il caso sano)* |
| ### **`aggiorna-lotto`** | la ### **stessa** via di scrittura, in blocco: una riga di storico ### **per voce**, le stesse asserzioni, e ### **una validazione prima** *(senza i derivati, che sono stale per costruzione)* ### **piu' una INTERA dopo** |
| ### **punto `1` (a)** | ### **`233`** segnaposto → classe `NON_DEFINITA`. ### ⚠ **`ESENTE-P3` ESCLUSO:** e' un segnaposto per titolo, ma la ### **lista `1` di Luca** lo ha fatto una voce vera — ### **una decisione dichiarata batte il titolo** |
| ### **punto `1` (b)** | le ### **`51` `TEORIA`** corrette: la classe viene dal ### **`tipo_era1` DICHIARATO**. ### ⭐ **`TEORIA` era il vecchio STATO `teoria` trasportato come CLASSE**, ed e' un difetto della migrazione. `K2a` `K2b` → `CRITERIO`/`METODO`, padre `OSSERVABILE-P1`; `T3a` `T3b` → padre `DRIVER-SCENA-II`; `M0a` → `DIFETTO`/`INFRASTRUTTURA` |
| ### **punto `1` (c)** | ### **`20`** assiomi e principi: `16` → `FISICA`, `4` → `METODO`, tutti era `ENTRAMBE`, con `nota_guardiano` ### **«da confermare da Luca»** |
| ### **punto `1` (d)** | ### **`9`** voci da `INFRASTRUTTURA` a `METODO`, col motivo di ciascuna |

| ### **il mandato `2` di `6`** | le ### **`43` decisioni di Luca**: ### **`42` applicate**, una ### **non applicabile** *(`Z47`: `CHIUSA` -> `AGENDA` e' una transizione ### **vietata**)*. Nove lotti, ### **uno per blocco**, cosi' si vede ### **quale decisione ha prodotto quale riga**. ### **ID persi: `0`** *(`990` a `a7485c8` -> `994`)*. Referto: `doc/REFERTO_decisioni_43_era2.md` |
| ### **`P-ID`** | un ID che ### **nasce** non puo' coincidere con un ID, un alias o un significato di omonimo, e ha ### **>= `4` caratteri**. Collaudo ### **`11`/`11`** |
| ### **il criterio `②` di `da-decidere`** | ### **TOLTO**, per decisione di Luca: *<<la domanda si chiude>>* ### **e** *<<il metadato omonimo resta>>* si possono soddisfare entrambe ### **solo se non e' il metadato a generare la domanda.** `DA_DECIDERE_LUCA.md`: ### **`15` -> `4` voci** |
| ### **`H-INDICE` curato** | verificava ### **il PREFISSO invece dell'ID**, per ### **`122` ID su `887`** *(`A9`)*. `estendi()` allunga il match al ### **piu' lungo ID NOTO**, e un intervallo resta un intervallo. ### **`122` -> `0`**, collaudo `13`/`13` |

| ### **il mandato `3` di `6`** | il ### **piano** `doc/PIANO_era2.md` *(`F0`-`F4`, ognuna con ### **ingresso e uscita misurabile**)*, l'### **albero delle scelte** *(`doc/ALBERO_era2.yaml`, `10` nodi, `3` archi, ### **`0` PRESA**)*, e ### **`P-ALB`** dentro `indice.py valida`. Referto: `doc/REFERTO_piano_era2.md` |
| ### ⭐ **e quattro difetti trovati PRIMA di cominciare** | eseguendo il primo passo del task history *(«leggere ### **dal codice** chi valida `decisioni.jsonl`»)*: `REPLAY-CIECO-ALLE-CANCELLAZIONI` *(### **`13` su `13` con `4` record cancellati**)*, `DUE-VIE-SU-LEGGI-JSONL`, `H-INDICE-IGNORA-I-VOCABOLARI`, `FORMA-SPEZZA-ID` *(### **`122` ID su `887`**)*. ### **Tutti curati, tutti con un collaudo** |
| ### **il quarto stato di `P-T2`** | ### **`GENERATO`**: `assiomi.jsonl` e `decisioni.jsonl` erano dichiarati `REPERTO` *(«non ha una via di scrittura»)* e ### **invece sono generati** — e ### **il blob non se ne accorgeva**, perché un generatore stabile dà sempre gli stessi byte |

| ### **il mandato `4` di `6`** | la ### **terza parte dell'infrastruttura**, ### **sette punti su sette**: `P-DET` *(determinismo, ### **due processi byte-identici**)* · `P-DIM` *(le dimensioni, e il generatore ### **rifiuta**)* · `P-SIM` *(simmetrie ### **simboliche**, conservazioni ### **numeriche** con soglie ### **DERIVATE**)* · `P-GRAFO` *(il grafo valido ### **a ogni passo**, costo ### **`5.7%`**)* · `P-BARRIERA` *(i hook come barriera, ### **codice `3`**)* · `P-TEMPI` *(un comando, i tempi, ### **budget `44.4` s su `120`**)* · `P-GUIDA` *(la guida ### **ESEGUITA**)*. Referto: `doc/REFERTO_infrastruttura_era2_terza.md` |
| ### ⭐ **e i presidi mi hanno corretto `12` volte** | e ### **TRE hanno cambiato il DISEGNO**: due volte `P-MOD` mi ha detto che ### **il collaudo di un modulo in fondo alla catena degli import non puo' vivere dentro quel modulo**, e una volta mi ha ### **impedito di alzare un tetto** — la manopola piu' facile di tutte |
| ### ⚠ **e due previsioni del task history** | la trappola `(a)` *(il punto `5` rompe la CI)* ### **ha TENUTO**; la `(b)` *(due processi non daranno byte identici)* era ### **SBAGLIATA**, e il perche' e' misurato: `numpy.savez` ### **azzera l'ora nello ZIP** |

| ### **il mandato `5` di `6`, l'ULTIMO** | le ### **regole di gestione**: ogni regola è una ### **VOCE** col suo dettaglio e ### **CHI LA FA RISPETTARE**, e le ### **DUE** sezioni di `CLAUDE.md` ### **si generano dall'indice** *(modificate a mano: RIFIUTATE)*. Piu' la sezione ### **«LAVORARE NELL'ERA `2`»** e il suo `doc/REGOLE/par13.md`. Referto: `doc/REFERTO_regole_era2.md` |
| ### ⭐ **e il numero che prima non esisteva** | ### **`9` regole su `25` non hanno NESSUNO che le faccia rispettare** *(`A9`)*: fino a oggi `CLAUDE.md` lo diceva ### **in prosa**, e una prosa ### **non si conta** |
| ### ⚠ **e due contatori mi hanno detto il FALSO** | *«ne hai perse OTTO»* e *«le hai perse TUTTE»* — ### **nessuno dei due riconosceva `[[ID]]`.** ### **Il confronto con `git` diceva `0` PERSE, ed era quello giusto** |

**L'ultimo lotto applicato:** `doc/indice/_lotti/correzioni.jsonl` — ### **`313` voci**,
`313` righe di storico, e la validazione ### **intera** passa.

---

## ⛔ **CHE COSA RESTA**

| ordine | che cosa | quante |
|--:|---|--:|
| `1` | `doc/REGOLE/par9.md` allo schema in vigore *(commit da solo)* | — |
| `2` | le voci ### **vere** `DA_CLASSIFICARE`: le `tipo_era1 = altro` e quelle senza evidenza | ### **`247`** |
| `3` | le ### **`CHIUSE` senza dominio** *(ricevono solo dominio ed era)* | ### **`184`** |
| `4` | i ### **segnaposto** `NON_DEFINITA`: alias, etichetta, o concetto da definire | ### **`233`** |
| `5` | il referto `doc/REFERTO_indice_v2_fase2.md` | — |

---

## 📌 **IL COMANDO PER RIPRENDERE**

```
cd /c/Users/lpeano/soliton_simulator
git pull                                        # ramo primo-ordine
python csv/indice.py valida                     # deve passare
python csv/indice.py cerca --stato DA_CLASSIFICARE   # che cosa resta

# per LEGGERE un lotto (descrizione, fonte, metadati dell'era 1 -- MAI il solo titolo):
python csv/indice.py mostra --stato DA_CLASSIFICARE --segnaposto NO --da 0 --quante 50

# per APPLICARE un lotto:
python csv/indice.py aggiorna-lotto doc/indice/_lotti/<nome>.jsonl
```

### ⚠ **E LE REGOLE DEL LAVORO, perche' chi riprende non le ritrovi altrove:**

| | |
|---|---|
| ### **si legge il CONTENUTO** | `descrizione`, `fonte`, e i metadati dell'era `1`. ### ⛔ **MAI il solo titolo, e MAI per parola chiave** |
| ### **il motivo CITA** | ogni `--motivo` riporta una frase della descrizione o della fonte. ### **Niente motivi generici**, e il lotto ### **rifiuta** un motivo sotto i `20` caratteri |
| ### ✔ **il dubbio e' un esito** | se il contenuto non basta, la voce ### **RESTA `DA_CLASSIFICARE`** con `meta.motivo_dubbio`. ### **Non c'e' un numero minimo da classificare** |
| ### **la mescolanza non si forza** | due cose di dominio diverso in una voce ⇒ `meta.da_dividere = true` e una proposta in `nota_guardiano`. ### **La divisione la decide Luca** |
| ### **le liste del guardiano NON cambiano** | salvo le correzioni `(c)` e `(d)` del punto `1`. ### **Un disaccordo va nel REFERTO, non nell'indice** |

---

## 📌 **STATO AL 2026-10-09** — *aggiornato a ogni lotto*

| | |
|---|--:|
| voci | `846` |
| ### **`DA_CLASSIFICARE` vere** *(non segnaposto)* | ### **`1`** |
| ### **segnaposto `NON_DEFINITA`** | ### **`187`** |
| ### **righe di storico** | ### **`1628`** |

```
classe    DIFETTO=200  NON_DEFINITA=187  MISURA=141  FRONTE=109  CRITERIO=90  CURA=56  PRESIDIO=34  STANDARD=29
dominio   FISICA=383  METODO=198  DA_CLASSIFICARE=187  INFRASTRUTTURA=49  DOCUMENTAZIONE=29
era       1=538  DA_CLASSIFICARE=188  ENTRAMBE=96  2=24
stato     SOSPESA=369  DA_CLASSIFICARE=188  CHIUSA=182  APERTA=82  AGENDA=24  SUPERATA=1
```

### ✔ **FATTO IN QUESTO GIRO:** la ### **TAPPA `5a`**: `hamiltoniana.py` — `H` e `dH/dpsi*` ### **in un solo posto**, i termini caricati ### **da `termini/` via `LEGGE`**, e la somma ### **in ordine canonico per ID.** ### ⛔ **E la misura dice una cosa che non supponevo:** `H` con `fsum` e' ### **identica sotto permutazione**, il gradiente ### **NO** — quindi ### **l'ordine canonico PORTA CARICO**, e `gradiente_grezzo()` lo prova.

### ⛔ **RESTA, e il mandato NON e' chiuso:** la tappa `5` *(lo schedulatore a STRATI, i due integratori candidati, il cono, i sei casi che DEVONO fallire)* e la `6` *(il referto)*.

### 📌 **E IN CODA, QUATTRO VOCI CON UN ORDINE DICHIARATO DA LUCA:** ① ### **chiusa** *(assorbita)* · ② le decisioni sulle `43` domande · ③ il piano d'azione e l'albero delle scelte · ④ ### **i metodi dell'era `1` nell'era `2`.**

**Ultimo lotto applicato:** `doc/indice/_lotti/era2_registri.jsonl` — ### **la tappa `5a` NON scrive sull'indice.**

---

## ✅ **MANDATO `1` DI `6` DELLA CODA: CHIUSO** — *la seconda parte dell-infrastruttura, `16` punti* *(2026-10-10)*

> ### ⛔ **Il referto: `doc/REFERTO_seconda_parte_era2.md`**, generato da `csv/_referto_seconda_parte.py` — ### **ogni numero esce dall-uscita dei collaudi** *(`L-NUMERI`)*.

| | |
|---|---|
| **i punti** | ### **`14` su `16` CHIUSI**; `3` e `11(a)` ### **APERTI su una decisione di Luca** *(`DEC-NASCITA-PSI`, `DEC-REGOLA-FORMA`)* |
| **i presidi nuovi** | `P-M1` · `P-C1` · `P-T1` · `P-T2` · `P-T3` · `P-R1` · `P-RIF` · `P-ES1` · `P-MOD` · `P-AB` · `P-E9` — ### **undici**, tutti con la loro voce e cablati |
| **i collaudi** | ### **`20` comandi, tutti passati** *(il conto sta nella tavola `2.` del referto)* |
| **i metodi dell-era `1`** | `120` nel perimetro: ### **`90` PORTATO**, `17` `DA_PORTARE`, `5` `DA_DECIDERE`, `8` `NON_SI_APPLICA` |
| **le leggi** | ### **`3`, e `3` di prova** — cioe- ### **ZERO leggi vere**, e il punto `10` lo rende ### **stampato** |
| **il simulatore** | `b8c21049`, ### **NON toccato** |

### ⚠ **E QUEL CHE RESTA APERTO E- SCRITTO nella sezione `5.` del referto:** le due decisioni di fisica, il buco di `H-FISICA-FUORI-LISTA`, `metadati.jsonl` come ### **reperto per necessita-**, la CI ### **mai osservata girare**, e il ### **budget del `pre-commit`** — che e- il punto `6` della TERZA parte.

### ➡ **PROSSIMO: il mandato `2` di `6`** — *le decisioni di Luca sulle `43` domande*.

---

## ✅ **LA CODA DEL `2026-10-10` E- FINITA** — *### **DODICI mandati**, e il quadro e- questo*

| il mandato | esito |
|---|---|
| le ### **cinque voci** della coda del `2026-10-09` | ### ✅ **chiuse** *(`26` commit)* |
| le ### **correzioni** della coda `+` le quattro regole di Luca | ### ✅ **`5` punti su `5`**, e la verifica su clone pulito e- ### **verde nei due ambienti** |
| `Z47` da ### **CHIUSA** a ### **SUPERATA** | ### ✅ **`5` passi su `5`**, ogni fatto verificato con `git show` |
| il `pre-commit` valida ### **lo STAGE** e non il disco | ### ✅ **`3` punti su `3`**, e la suite ### **lascia l-albero come l-ha trovato** |
| le ### **sei decisioni** di fisica | ### ✅ **`6` su `6`** — con ### **DUE differenze** dall-albero, scritte e non corrette |
| le ### **domande aperte** diventano voci | ### ✅ **`4` punti su `4`**: tre campi, il ciclo che blocca, `prossima`, e la lista |
| la ### **camminata a moneta** | ### ✅ **`6` punti su `7`**; il punto `4` ### **non si puo- eseguire**, e il motivo e- registrato |
| le ### **memorie** e il ### **disegno `3D`** | ### ✅ **`3` su `3`** |
| il ### **tempo proprio locale** e la ### **`cs` locale** | ### ✅ **`8` punti su `8`** |

### ⛔ **E UNA DECISIONE DI LUCA FERMA TRE PUNTI DI DUE MANDATI, e- UNA SOLA, ed e- QUESTA:** ### **il VUOTO LOCALE viene PRIMA o DOPO `D9`?**

> ### ✅ **Se PRIMA** — come dice il punto `6` delle sei decisioni — la catena dell-albero va girata, e si sbloccano ### **il punto `4` della camminata** *(il vuoto locale da proposta a decisione)*, ### **il punto `1` delle sei** *(la divisione, che aspetta `D6`)*, e ### **la domanda `VUOTO-LOCALE-DETERMINISTICO`** della lista.
> ### ⛔ **Se DOPO**, quei due punti vanno riscritti.
>
> ### ⚠ **L-albero dice `D9` → `D13` → `D6` → `D7`**, cioe- ### **il vuoto TERZO**; e ### **l-albero vince**, come Luca ha scritto ### **cinque volte** in questa coda. ### **Quindi la differenza e- SCRITTA e la catena NON e- stata toccata.**

### ➡ **E LA PROSSIMA DOMANDA DELLA LISTA LA DICE IL COMANDO:** `python csv/indice.py prossima` — oggi ### **[[DOMANDA-QUANTITA-CONSERVATA]]: esiste una moneta isotropa, causale e simmetrica fra le bande con una quantita- conservata?** ### **Aperte `11`, di cui pronte `5`.**

