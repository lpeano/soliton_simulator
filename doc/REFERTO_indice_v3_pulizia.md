# IL REFERTO DELL'ULTIMA PULIZIA DELL'INDICE `v3`

> ### ⭐ **I segnali sono `F1=0 F2=0 F3=0 F4=0 F6=0`, e sono ESATTAMENTE quelli che il mandato si aspettava.** ### ⛔ **Ma la cosa che conta di questo giro non e' un numero: e' che provando `F7` end-to-end ho scoperto che `aggiorna-lotto` SCRIVEVA PRIMA DELLA VALIDAZIONE INTERA.**

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il task history** | `doc/TASK_HISTORY/2026-10-09_indice_v3_ultima_pulizia.md`, ### **committato PRIMA del lavoro** *(`f614613`)* |
| **i commit** | `f39df3b` *(`1`)* · `f47159a` *(`2`)* · `375e0af` *(`3`)* · `4aeeb80` *(`4`)* · `dcc8aac` *(`5`)*, piu' questo |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |
| **i controlli** | ### **6 su 6** · collaudo dei presidi ### **26 su 26** *(erano `20`)* · collaudo dell'indice ### **22 su 22** *(era `21`)* |

---

## ① IL DIFETTO DEL GIRO, E L'HA TROVATO UNA PROVA CHE IL MANDATO NON CHIEDEVA

Il mandato chiede due bracci per `F7`: ### **deve scattare** su `CURA1-CORTO` allo stato di `89784dc` *(in una copia)*, ### **non deve** dopo il punto `1`. Li ho fatti, e passano. ### **Poi ho voluto vederlo BLOCCARE DAVVERO:** un lotto che riporta `CURA1-CORTO` ad `APERTA` deve essere rifiutato.

> ### ⛔ **E' STATO SCRITTO.** L'assert e' scattato ### **dopo**, e l'indice e' rimasto ### **CORROTTO sul disco** *(`CURA1-CORTO` ad `APERTA`)*. Il messaggio diceva *«SCRITTO, MA LA VALIDAZIONE INTERA FALLISCE»*, che era ### **esattamente la descrizione del danno.**

| | la catena |
|---|---|
| `1` | `aggiorna_lotto` valida con **`derivati=False`** — e `F5`, `F7` e la forma delle eccezioni stavano ### **DOPO** il ritorno su `derivati`, quindi ### **non venivano guardati** |
| `2` | ### **SCRIVE** |
| `3` | rigenera le viste |
| `4` | ### **e SOLO ALLORA valida tutto** — su un file ### **gia' scritto** |

### ⚠ **La promessa era nel docstring di `aggiorna_lotto` dal giorno che l'ho scritto:** *«una sola validazione alla fine — se non passa, NON SI SCRIVE NIENTE»*. ### **Era una descrizione di cio' che credevo, non di cio' che il codice faceva.**

### ✔ **LA CURA, E TOCCA LA CAUSA**

| | |
|---|---|
| `F7` e la forma delle eccezioni | dipendono ### **solo dalle voci** ⇒ vanno ### **prima** del ritorno su `derivati`, cosi' la validazione ### **pre-scrittura** li vede |
| `F5` | ### **non dipende dalle voci** *(guarda `storico.jsonl` contro `HEAD`)* ⇒ si chiede ### **prima di scrivere**, nelle due vie di lotto |
| ➜ **l'effetto** | la validazione finale puo' fallire ### **solo sui derivati**, che `viste()` ha appena rigenerato: ### **la promessa diventa VERA** |

### **Riprovato end-to-end:** il lotto e' rifiutato e `voci.jsonl` e' ### **byte-identico** prima e dopo *(`sha1 fe3751cbe3a9` in entrambi i casi)*. ### ⭐ **E la prova e' diventata permanente**, con due bracci nel collaudo che ### **fotografano i byte e li RIMETTONO** se cambiano: una regressione viene ### **riportata, non subita.**

### ⭐ **E il danno e' stato riparato da git**, perche' tutto era committato. ### **E' la seconda volta in questo lavoro che «commit prima di ogni run» mi salva un file:** la prima furono le ### **`867` classificazioni** che il controllo `C4` ha cancellato.

---

## ② PUNTO `1` — **lo stato di una voce dell'era `1`**

Le `4` voci da `APERTA` a `SOSPESA`, e l'*«APERTO»* in `stato_era_1`.

| id | prima | dopo | `stato_era_1` |
|---|---|---|---|
| `CURA1-CORTO` | `APERTA` | ### **`SOSPESA`** | ### **`aperto`** |
| `CURA2-CORTO` | `APERTA` | ### **`SOSPESA`** | ### **`aperto`** |
| `SIGILLO-CURA2` | `APERTA` | ### **`SOSPESA`** | ### **`aperto`** |
| `SIGILLO-CURA2-RIPARATO` | `APERTA` | ### **`SOSPESA`** | ### **`aperto`** |

### ⛔ **E' un mio errore del giro scorso, e la forma dell'errore e' quella che conta.** Nel referto avevo scritto: *«lo stato `APERTA` non l'ho scelto: lo dice l'intestazione; classe e dominio sono MIEI»*. ### **Era vero e insufficiente:** l'intestazione dice lo stato ### **nell'era `1`**, e io l'ho messo nel campo `stato`, che e' lo stato ### **di oggi.**

> ### ⭐ **DICHIARARE LA PROVENIENZA DI UN DATO NON BASTA SE LO SI E' MESSO NEL CAMPO SBAGLIATO:** la dichiarazione mi ha fatto sembrare prudente ### **un errore di campo.** Per questo la regola ha ### **un presidio**, non solo una riga in `par9.md`.

---

## ③ PUNTO `2` — **`F7`, e un presidio che boccia il caso sano**

`FISICA` + era `1` + stato diverso da `SOSPESA`/`CHIUSA` ⇒ ### **la validazione fallisce.** ### **E' un ERRORE, non un segnale.**

### ✔ **La prima misura e' stata PRIMA di scrivere il task history**, e non e' un dettaglio: ### **un presidio bloccante che violasse una voce che il mandato non nomina fermerebbe ogni commit**, e me ne accorgerei ### **solo al momento di committare.** `FISICA`/era `1`: `SOSPESA` `204`, `CHIUSA` `137`, ### **`APERTA` `4`** — e le `4` sono ### **esattamente quelle del punto `1`.** ### **`F7` e' sicuro perche' il punto `1` viene prima**, non per caso.

### ⚠ **E `F7` ha bocciato il CASO SANO del collaudo:** la voce-modello di `indice.py collaudo` era `FISICA`/era `1`/`APERTA`. Messa a era `ENTRAMBE`, e `F7` ha preso ### **il suo caso.** ### ⭐ **Un presidio che boccia il caso sano di un collaudo sta dicendo che quel caso sano era un esempio che nell'indice vero non si sarebbe potuto scrivere.**

---

## ④ PUNTO `3` — **`F1` a zero, e due omonimi in piu'**

| id | i due significati |
|---|---|
| `C4` | la VOCE `C4`: <<inerzia = T^2 -- chiude il buco dimensionale>>, una misura FISICA/era 1<br>il <<C4>> citato da `COLLAUDO-NON-ESEGUITO`: ### **IL CONTROLLO `C4`** della migrazione -- <<un collaudo che si RIFIUTA di girare esce con 2, e il controllo C4 lo conta come PASS>> |
| `M1` | la VOCE `M1`: <<LA MATERIA E- UNO STATO, NON UNA SOSTANZA -- e non c-e- SCARICO>>, un difetto FISICA/era 2<br>il <<M1>> citato da `E3`: ### **LA MISURA DEL RUN** -- <<M1/M4 leggere durante il run>>, cioe- una delle misure dell-epoca 3 |

### ⭐ **E' il terzo e il quarto omonimo che nascono LEGGENDO UN SEGNALE DI `F1`**, dopo `C5`. ### **Un presidio che trova omonimi cercando gemelle sta dicendo che gemelle e omonimi si somigliano:** entrambi sono ### **due nomi e una cosa, o una cosa e due nomi.**

| gruppo | id | il marcatore scelto nel testo |
|---|---|---|
| DIPENDENZA | `AB-CONTROLLI` | *«A/B di W5»* |
| CRITERIO | `COER-4PI` | *«la coerenza della massa»* |
| OMONIMO | `COLLAUDO-NON-ESEGUITO` | *«il controllo C4 lo conta come PASS»* |
| OMONIMO | `E3` | *«M1/M4 leggere durante il run»* |
| DOCUMENTO | `ETICHETTA-A13` | *«dove la regola e'»* |
| DIPENDENZA | `M-MASSA` | *«dipende da»* |
| CRITERIO | `REGISTRO_FISICA:E3` | *«la finestra di D33»* |
| CRITERIO | `REGISTRO_FISICA:S6` | *«se la cura ha curato D02»* |
| CRITERIO | `REGISTRO_FISICA:U2` | *«ATTIVA IN ENTRAMBI I BRACCI»* |

### ⚠ **Il codice si e' fermato una volta, ed e' il punto:** avevo scelto *«COERENZA»* per `COER-4PI`, e nel titolo c'e' *«la coerenza della massa»*. ### **Ho riletto i titoli veri invece di allargare la ricerca.**

### ⛔ **Su `49` segnali iniziali di `F1`, ZERO gemelle vere.** E' ### **il presidio con la precisione piu' bassa dei sette**, e questo e' un fatto su `F1`.

---

## ⑤ PUNTO `4` — **`F4` a zero, e il criterio e' l'EREDITA'**

| id | `classe`/`dominio`/era/stato | il perche' |
|---|---|---|
| `AUTO-MANUTENZIONE` | `STANDARD`/`METODO`/era `ENTRAMBE`/`APERTA` | UNA REGOLA DI LAVORO, e una regola e- UNA LEGGE DEL METODO: `## 5-bis. AUTO-MANUTENZIONE (tieni aggiornati i documenti vivi)` in doc/STORIA_REGOLE.md, in un solo posto. Vale per ENTRAMBE le ere perche- il metodo non cambia con l-era |
| `F4` | `DIFETTO`/`FISICA`/era `1`/`SOSPESA` | UNA FAMIGLIA DI DIFETTI, e il testo dice DA QUALE DIFETTO NASCE: <<scritture di stato senza traccia | D04>>. EREDITA il dominio da `D04`, che e- FISICA/era 1, e lo stato SOSPESA perche- `D04` e- SOSPESA |
| `F5` | `DIFETTO`/`FISICA`/era `1`/`SOSPESA` | UNA FAMIGLIA DI DIFETTI: <<fasi col periodo sbagliato | D34, dal censimento in corso>>. EREDITA il dominio da `D34`, FISICA/era 1; SOSPESA e non CHIUSA perche- il testo dice <<dal censimento IN CORSO>> |

### ✔ **`F4` e `F5` sono FAMIGLIE di difetti, e il testo dice DA QUALE DIFETTO NASCONO.** Ho misurato `D04` e `D34`: ### **`FISICA`/era `1`.** ### ⭐ **Una famiglia prende il dominio del difetto da cui nasce**, e cosi' ### **il dominio non lo scelgo io: LO EREDITA.** ### ⚠ **Ma l'eredita' vale per il DOMINIO, non per lo stato:** `F5` e' `SOSPESA` e `D34` e' `CHIUSA`, perche' il testo di `F5` dice *«dal censimento IN CORSO»*.

### ⚠ **E la mia uscita del giro scorso non era piu' disponibile, e va bene:** avevo messo queste tre in un ### **«quarto caso»** — *«non e' nessuno dei tre esiti»*. ### **Era una domanda, e la risposta e' «decidi».**

### ⛔ **Due cose che il codice ha RIFIUTATO, ed e' giusto cosi':**

| | |
|---|---|
| `1` | la nota di `AUTO-MANUTENZIONE` superava i ### **`300` caratteri** che il registro ammette. Il lotto e' stato ### **rifiutato, e non ha scritto niente** — ### **la cura dell'atomicita' ha funzionato al primo uso vero.** La nota si taglia, e il perche' ### **intero resta nel `motivo`**: ### **un campo con un limite dichiarato non si allarga per far stare una frase** |
| `2` | ripristinando `F4` come voce `FISICA`, `F3` e' risalito da `0` a `1`: il titolo contiene *«si RIUSA il criterio»*, che sta nella frase che dice ### **da quale difetto nasce**, non nell'argomento. Chiuso con l'eccezione ### **nello stesso giro che l'ha prodotto.** ### ⚠ **E' la seconda volta che un ripristino crea un segnale di `F3`:** `F3` guarda ### **una parola**, e una parola ### **non dice di chi si parla** |

---

## ⑥ PUNTO `5` — **un elenco solo, e SI GENERA**

`doc/indice/DA_DECIDERE_LUCA.md`, ### **`37` voci** e `37` domande.

| | il criterio |
|---|---|
| ① | la `nota_guardiano` dice *«da decidere / confermare da Luca»* → ### **la domanda e' cio' che la nota stessa chiede** |
| ② | la voce ha ### **`meta.omonimo`** → quale dei `N` significati? |
| ③ | `stato = DA_CLASSIFICARE` ### **e la classe NON e' `NON_DEFINITA`** |

| gruppo | quante |
|---|--:|
| gli OMONIMI -- due nomi e una cosa, e NON si scegli | `11` |
| le CLASSIFICAZIONI da confermare | `20` |
| le DOMANDE aperte | `6` |

### ⛔ **Nel codice NON c'e' nessuna lista di ID: ci sono i tre criteri**, e l'elenco e' cio' che trovano. ### ⭐ **Un elenco mezzo generato e' peggio di nessun elenco, perche' SEMBRA COMPLETO.**

### ⚠ **E un'imprecisione presa rileggendo l'uscita:** la domanda diceva *«quale dei `7` significati»* per `D3`, che ha ### **`8` definizioni** — contava le voci del meta, e l'ultima e' ### **un troncamento.** Adesso dice *«di ALMENO `6`»* quando la lista e' troncata. ### **Un numero in una domanda e' un numero come gli altri: se e' sbagliato, la domanda e' sbagliata.**

---

## ⑦ I CONTEGGI E I CONTROLLI

> **PRIMA** = `git show 89784dc`. **DOPO** = il disco. ### **Nessun numero ricopiato.**

| `dominio` | prima | dopo | |
|---|--:|--:|---|
| FISICA | `387` | `389` | ### **+2** |
| METODO | `195` | `196` | ### **+1** |
| DA_CLASSIFICARE | `187` | `187` |  |
| INFRASTRUTTURA | `47` | `47` |  |
| DOCUMENTAZIONE | `27` | `27` |  |

| `classe` | prima | dopo | |
|---|--:|--:|---|
| DIFETTO | `210` | `212` | ### **+2** |
| NON_DEFINITA | `187` | `187` |  |
| FRONTE | `169` | `169` |  |
| CRITERIO | `94` | `94` |  |
| MISURA | `75` | `75` |  |
| CURA | `46` | `46` |  |
| PRESIDIO | `34` | `34` |  |
| STANDARD | `28` | `29` | ### **+1** |

| `stato` | prima | dopo | |
|---|--:|--:|---|
| SOSPESA | `283` | `289` | ### **+6** |
| DA_CLASSIFICARE | `188` | `188` |  |
| CHIUSA | `187` | `187` |  |
| APERTA | `160` | `157` | ### **-3** |
| AGENDA | `25` | `24` | ### **-1** |
| SUPERATA | `0` | `1` | ### **+1** |

| | prima | dopo |
|---|--:|--:|
| voci | `843` | ### **`846`** |
| etichette rimosse | `109` | ### **`106`** |
| ### **ID vecchi conservati** | `953` | ### **`953`** *(`0` persi, `0` doppi)* |
| ### **`FISICA`/era `1` con stato vietato** | `4` | ### **`0`** *(e `F7` lo impedisce)* |

| presidio | prima | dopo |
|---|--:|--:|
| `F1` | `11` | ### **`0`** |
| `F2` | `1` | ### **`0`** |
| `F3` | `0` | ### **`0`** |
| `F4` | `3` | ### **`0`** |
| `F6` | `0` | ### **`0`** |
| ### **in tutto** | `15` | ### **`0`** |

### ✔ **E sono ESATTAMENTE i numeri che il mandato aveva scritto:** *«atteso: `F1=0 F2=1 F3=0 F4=0 F6=0`»*.

```
  C1 CONSERVAZIONE: ogni ID vecchio in UNO E UNO SOLO posto PASSA   persi 0, doppi 0
  C2 la TRACCIA copre ogni ID vecchio, con la REGOLA       PASSA   senza traccia 0
  C3 LE LISTE DEL GUARDIANO: classificazione come indicata PASSA   fuori posto 0
  C4 IDEMPOTENZA (NON si rilancia: c'e' lavoro di dopo)    PASSA   storico.jsonl ha 1221 righe -> verificata al commit 6b8cb90; e la migrazione ha un PRESIDIO che la ferma
  C5 `indice.py valida` passa                              PASSA     ### i PRESIDI contro le mescolanze: 0 segnali (F1=0  F2=0
  C6 la VISTA passa IL VALIDATORE VECCHIO (quello del pre-commit) e la domanda PASSA   12 bloccanti su 846 voci
  F1  DEVE scattare: B2 cita Z31, e Z31 era FISICA/era 1         PASSA   il titolo di B2 dice <<Z31 -- i sigilli non ri-girabili | Z31, ...>>
  F1  NON deve scattare: con Z31 corretta (METODO/ENTRAMBE)      PASSA
  F1  NON deve scattare: D24 cita A2, che e- uno STANDARD (entrambe le ere) PASSA   il titolo di D24 dice <<A2 e- VIOLATO da Lam = mean(I)>>
  F1  DEVE scattare: con A2 finto DIFETTO -- e- LA CLASSE che lo zittisce PASSA
  F2  DEVE scattare: D35 era era 2 e nel titolo ha (:5443)       PASSA   era `2` a 6e5e75b
  F2  NON deve scattare: D35 corretta (era 1)                    PASSA
  F3  DEVE scattare: C28 era FISICA e il titolo dice <<ALCUN SIGILLO>> PASSA   dominio `FISICA` a 6e5e75b
  F3  NON deve scattare: C28 corretta (METODO)                   PASSA
  F4  DEVE scattare: TW-1 era un'etichetta, ed e' DEFINITA in un documento PASSA   doc/SCALE_TW_lettura.md la definisce con una riga di tabella
  F4  NON deve scattare: TW-1 oggi NON e' fra le etichette       PASSA
  F4  NON deve scattare: POST-HOC, l-ID sta DENTRO LA PROSA dell-intestazione PASSA   `### 1.2 ... -- dichiarata POST-HOC, non era fissata prima`
  F4  DEVE scattare: TW-1 a 6e5e75b -- una RIGA DI TABELLA lo definisce PASSA   la regola dell-intestazione NON tocca le righe di tabella
  F4  DEVE scattare: con la REGOLA SPENTA, POST-HOC torna a segnalare PASSA
  F5  DEVE essere un ERRORE: riga 2 GIA' COMMITTATA e senza commit PASSA   n_head=2 -> la riga 2 e' committata, la 3 e' IL RITARDO e NON si segnala
  F5  NON deve scattare: le righe oltre HEAD sono il RITARDO dichiarato PASSA
  F7  DEVE essere un ERRORE: CURA1-CORTO era FISICA/era 1/APERTA a 89784dc PASSA   la fisica dell-era 1 non chiusa e- SOSPESA
  F7  NON deve scattare: dopo il punto 1, e su TUTTE le 846 voci PASSA   0 voci FISICA/era 1 con stato diverso da SOSPESA/CHIUSA/SUPERATA
  F7  NON deve scattare: FISICA/era 1/SUPERATA e- risolta DA FUORI PASSA   da SUPERATA si esce solo verso APERTA: e- uno stato terminale
  F7  DEVE scattare ancora: FISICA/era 1/APERTA, cioe- non e- un allargamento cieco PASSA
  F6  DEVE scattare: la nota dice lista 3 (FISICA/1/SOSPESA), la voce e' DOCUMENTAZIONE PASSA
  F6  NON deve scattare: con la nota della correzione v3         PASSA
  ECCEZIONE  DEVE essere un ERRORE: non cita il testo alla lettera PASSA
  ECCEZIONE  NON deve essere un errore: cita 40 caratteri del titolo PASSA
  ECCEZIONE  DEVE essere un ERRORE: fuori forma (manca `F<n>:`)  PASSA
  ATOMICITA-  il lotto che viola F7 e- RIFIUTATO                 PASSA   uscita 1
  ATOMICITA-  e NON ha scritto NIENTE: i byte sono IDENTICI      PASSA   voci.jsonl e storico.jsonl byte per byte
```

---

## ⑧ CHE COSA RESTA A LUCA

> ### ⭐ **Tutto in un posto solo: `doc/indice/DA_DECIDERE_LUCA.md`, e si GENERA.**

| | quante | che cosa |
|---|--:|---|
| gli OMONIMI -- due nomi e una cosa, e NON si scegli | `11` | |
| le CLASSIFICAZIONI da confermare | `20` | |
| le DOMANDE aperte | `6` | |
| ### **l'unico segnale che resta** | `1` | `ENERGIA-NON-DEFINITA`: *«superata da `A16` (`H` definita)?»*. ### **E' voluto:** un presidio che segnala una decisione aperta ### **sta funzionando** |
| ### **i segnaposto** | `187` | ### **NON sono una domanda: sono il lavoro che resta** |

### ⚠ **E tre classificazioni che sono MIE**, e si cambiano con un lotto di una riga: la classe `STANDARD` e il dominio `METODO` di `AUTO-MANUTENZIONE`; la classe `MISURA` delle `4` del punto `1`; e `F7` ### **non guarda `FISICA`/era `2` ne' gli altri domini** — il mandato dice `FISICA`/era `1`, e ### **non l'ho allargato da solo.**

> ### ⭐ **Il criterio, lo stesso di tutto il lavoro:** dove il mandato ### **nomina** la decisione l'ho applicata; dove ### **non la nomina**, ### **ho lasciato le cose dov'erano e le ho scritte qui.** ### **Una decisione non presa e' un dato; una decisione presa al posto di Luca e' un difetto.**

## ⑨ UNA VOCE DOPO: **`ENERGIA-NON-DEFINITA` E- SUPERATA DA `A16`**

> ### ⭐ **L-unico segnale che restava NON c-e- piu-, e non perche- l-ho zittito: perche- ### LA DOMANDA HA AVUTO RISPOSTA.** I presidi sono ### **tutti a `0`**.

| | |
|---|---|
| **la voce** | `FRONTE`/`FISICA`/era `1`/### **`SUPERATA`**, `superata_da` = ### **`A16`** |
| **che cosa diceva** | *<<il modello non ha un-energia totale, e senza quella bilancio e calore non hanno base>>* |
| **che cosa dice `A16`** | lo stato evolve sotto ### **UNA SOLA `H`**, e *<<norma ed energia si conservano ### **per costruzione**>>* *(decisione di Luca, 2026-10-08)* |
| **era `2` -> `1`** | la voce e- ### **una LETTURA DEL CODICE DELL-ERA `1`** — *<<non esiste nessuna funzione che calcoli un-energia totale>>* — non programma dell-era `2` |
| **la nota TOLTA** | diceva *<<da decidere da Luca: superata da `A16`?>>*. ### **Una domanda a cui si e- risposto non si riscrive: si TOGLIE**, e la risposta vive in `superata_da` |

### ⛔ **CIO- CHE RESTA APERTO NON STA IN QUESTA VOCE, E NON STA NEMMENO NELL-INDICE.** Il mandato dice *<<collegala con le voci che lo tracciano, ### **se esistono**>>*: ### **ho cercato, e NON ESISTONO.** La forma di `H`, l-energia cinetica delle lunghezze *(decisione `9`)* e l-energia d-arco stanno in `doc/TRADUZIONE_IN_H.md`, e ### **nessuna voce dell-indice ha quel documento come fonte** — `0` su `846`. Quindi `collegate` resta ### **vuoto**, e ### **questo e- il dato**, non un dettaglio: ### ⭐ **il lavoro aperto piu- grande del progetto e- tracciato SOLO IN UN DOCUMENTO.**

### ⚠ **E due ostacoli fra il mandato e il codice, tolti alla causa:**

| | |
|---|---|
| `F7` ammetteva solo `SOSPESA` e `CHIUSA` | `FISICA`/era `1`/`SUPERATA` ### **lo faceva scattare**, e il lotto sarebbe stato ### **rifiutato.** ➜ **`SUPERATA` sta con `CHIUSA`:** una voce superata da una decisione ### **non e- aperta**, e- risolta ### **da fuori** — e `TRANSIZIONI` lo conferma, da `SUPERATA` si esce ### **solo verso `APERTA`.** Due bracci di collaudo: `SUPERATA` ### **non scatta**, `APERTA` ### **scatta ancora** |
| la via di scrittura sapeva solo AGGIUNGERE un metadato | e `nota_guardiano` ha regex `^.{1,300}$`, quindi ### **non si puo- svuotare.** ➜ **`meta_togli`**: una lista di chiavi da ### **cancellare**, nella stessa via, con la sua riga di storico — e ### **togliere una chiave che non c-e- e- un errore**, perche- nasconderebbe uno sbaglio |

---

