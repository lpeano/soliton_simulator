# 🧹 **RIORDINO DELLE REGOLE — PROPOSTA** *(2026-09-26, sessione nuova)*

> ## ⚠ **E' UNA PROPOSTA: non ho toccato `CLAUDE.md`, ne' i hook, ne' un assioma.**
> **Decide Luca.** Qui c'e' l'inventario di **ogni** regola in vigore, dove finisce, e perche'.

*(**Generata** da `csv/_regole_proposta.py`. **Misurati** dallo script: gli id, le righe di ogni
sezione e documento, i conteggi. **Giudizio mio**: la destinazione di ogni regola, che sta in
`DESTINAZIONE` — **una riga per id**, cosi' si corregge in un posto solo.)*

## 📉 I CONTEGGI, PRIMA E DOPO

| | PRIMA | DOPO *(proposta)* | |
|---|--:|--:|---|
| **regole in vigore** | **76** | **62** | 14 fuse o tolte |
| di cui **automatiche** *(un hook le impedisce)* | 8 | 9 | +1 proposta *(inventario)* |
| **righe di `CLAUDE.md`** | **1576** | **~153** | sotto le **400** del presidio proposto |
| **righe lette all'avvio** | **2714** | **~1291** | esce `par.9` (**671 righe**) e la STORIA |
| **righe di `RELAZIONE_PER_CLAUDE.md`** | **20364** | **~1 giorno** | il resto in `doc/relazioni/` |

> ### 🎯 **IL NUMERO CHE DECIDE:** `par.9` **da sola e' 671 righe su 1576, il 43 % di
> ### `CLAUDE.md` — e NON E' UNA REGOLA: sono FATTI verificati dal codice.**

---

## 🗄 I CINQUE POSTI, uno per categoria

| | dove | che cosa ci va | la regola del posto |
|---|---|---|---|
| **1** | `doc/ASSIOMI.md` | ASSIOMI — **INTOCCABILI** | vincoli sulla FORMA delle leggi. Non si fondono, non si tolgono, non si spostano. |
| **2** | `doc/PATTERN_DI_PROVA.md` | METODO DI MISURA — **max 10 regole** | una riga + **il difetto che previene**. Se ne entra una, ne esce una. |
| **3** | i **hook** *(`.githooks/`, `csv/_hook_*.py`, `csv/_presidio_*.py`)* | IGIENE TECNICA — **automatica** | in `CLAUDE.md` **una riga** che li elenca; **il perche' sta nel messaggio d'errore del hook**. |
| **4** | `CLAUDE.md` | FLUSSO DI LAVORO — **una pagina** | come si lavora: ordine, commit, relazione, indice. **Sotto le 400 righe**, e un presidio lo fa rispettare. |
| **5** | `doc/STATO_RUN.md` + `doc/INDICE_ID.tsv` | STATO E FATTI DAL CODICE | **non sono regole**: sono cio' che il sistema e' oggi. Fuori da `CLAUDE.md`. |

**E la STORIA di ogni regola** *(da quale errore e' nata)* **va in `doc/STORIA_REGOLE.md`:**
un archivio che **NON si legge all'avvio**. Oggi quella storia vive dentro `CLAUDE.md` e pesa
**~338 righe** *(`par.0-ter` 208 + `par.5-quinquies` 130)*: e' il secondo taglio dopo `par.9`.

---

## ❌❌ **DUE COLLISIONI DI NOME, e sono dello stesso tipo che l'indice ha curato per i difetti**

| nome | in `CLAUDE.md` par.0-ter | nei hook |
|---|---|---|
| **`P3`** | nessuna statistica senza barra d'errore | un sigillo che configura il modulo a mano |
| **`P5`** | ogni ramo `else`/fallback va contato | un referto senza la configurazione intera |

> ### **Lo stesso nome per due regole diverse** — ed e' **esattamente** il difetto che il
> ### 2026-09-26 abbiamo curato per i difetti *(`A3` era tre voci)*. **Per le regole non e'
> ### ancora curato.** La proposta: i presidi dei hook prendono il prefisso **`H-`**, che dice
> ### *«questo lo impedisce una macchina»*.

---

## 📋 L'INVENTARIO COMPLETO — 76 regole, ognuna con la sua destinazione

### → POSTO **1**: ASSIOMI — **INTOCCABILI**   *(`doc/ASSIOMI.md`)* — **19 regole**

| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |
|---|---|---|:--:|:--:|---|
| **A1** | la LEGGE, non il numero | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A10** | una sola grandezza puo' legare due domini | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A11** | un limite e' una legge, non una toppa | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A12** | un difetto dimostrato si cura: misurare non e' curare | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A13** | `LAM` e' la scala di Planck del sistema | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A2** | nessuna scorciatoia globale | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A3** | niente si normalizza sul proprio insieme | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A3b** | corollario di `A3` (inline) | `doc/ASSIOMI.md` | — | `TIENI` | corollario: resta dentro `A3`, non diventa una voce a se' |
| **A3c** | due grandezze si confrontano solo se sono confrontabili | `doc/ASSIOMI.md` | — | `TIENI` | corollario metodologico di `A3`: **richiamato** dal posto 2, non copiato |
| **A4** | stratificazione causale | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A5** | causalita' della mediazione | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A6** | inerzia (TEOREMA) | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A7** | conservazione e stato | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A7b** | uno stato non nasce indefinito | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A8** | un ramo silenzioso non e' un ramo | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A8b** | le cache cross-passo | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **A9** | un presidio che non impedisce non e' un presidio | `doc/ASSIOMI.md` | — | `TIENI` | assioma: intoccabile per decisione di Luca |
| **STANDARD 8** | un difetto dimostrato si cura | `doc/PATTERN_DI_PROVA.md` | — | `FONDI` | **e' `A12` parola per parola**: resta l'assioma, e il posto 2 lo **richiama**. Una regola in due posti e' una regola che si puo' aggiornare a metà |
| **par.3** | zero manopole: nessun parametro tarato a mano | `CLAUDE.md` | — | `FONDI` | **e' `A1`** *(la legge, non il numero)*: resta l'assioma, e il posto 4 lo richiama in una riga |

### → POSTO **2**: METODO DI MISURA — **max 10 regole**   *(`doc/PATTERN_DI_PROVA.md`)* — **16 regole**

| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |
|---|---|---|:--:|:--:|---|
| **L-SOGLIA** | una soglia **non si calcola dai dati che giudica**, e si collauda **sul caso nullo** | `prompt di Luca 2026-09-26` | — | `TIENI` | **nuova al posto 2**, e la chiede Luca: nasce dai criteri auto-referenziali *(la soglia `2*std(ON)` che si stringe quando la cura funziona)* e dal criterio con `|x|` che **falliva l'85.89 % su rumore puro** |
| **P1-sexies** | un criterio si collauda su un caso a risposta nota, **e il caso che DEVE fallire e' il piu' importante** | `CLAUDE.md par.0-ter` | — | `TIENI` | e' metodo di misura, non flusso: **cambia posto**, da `CLAUDE.md` a `PATTERN_DI_PROVA` |
| **P3** | nessuna statistica senza barra d'errore, e fra bracci si usa la dispersione FRA SEMI (>= 4 semi) | `CLAUDE.md par.0-ter` | — | `TIENI` | metodo di misura: **cambia posto**. ⚠ **E CAMBIA NOME**: oggi `P3` e' **anche** un presidio del hook, e sono due regole diverse |
| **P4** | prima di misurare se una grandezza cambia, verificare che sia LIBERA di cambiare | `CLAUDE.md par.0-ter` | — | `TIENI` | metodo di misura: cambia posto |
| **P5** | ogni ramo `else`/fallback su un percorso fisico va CONTATO | `CLAUDE.md par.0-ter` | — | `TIENI` | metodo di misura: cambia posto. ⚠ **E CAMBIA NOME**: `P5` e' **anche** un presidio del hook |
| **P6** | ogni CSV di misura porta blob, seme e tutti i flag | `CLAUDE.md par.0-ter` | — | `TIENI` | metodo di misura: cambia posto |
| **STANDARD 1** | un processo per braccio | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto che previene: lo stato condiviso fra due bracci nello stesso processo |
| **STANDARD 10** | una cura non aumenta il numero delle leggi | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: ogni cura che aggiunge un meccanismo invece di togliere una toppa. **Si applica anche alle REGOLE, ed e' il criterio di questa proposta** |
| **STANDARD 2** | firme dei byte, non `max|delta|` | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: `max|delta| = 0` non vede due array di forma diversa |
| **STANDARD 3** | assenza strutturale != dato mancante | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: un sito che cambia lunghezza registrato come `None` |
| **STANDARD 4** | snapshot contro snapshot, allo stesso istante | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: i contatori diagnostici corrono mentre confronti |
| **STANDARD 5** | il controllo dell'involucro, prima di ogni prova | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: lo strumento di lancio non riproduce il riferimento |
| **STANDARD 7** | un giro CORTO prima del giro vero | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | difetto: sette ore buttate per un parametro sbagliato |
| **STANDARD 9** | un'assenza si dichiara solo da una ricerca sull'INTERO file, dall'AST **o da `git log`** | `doc/PATTERN_DI_PROVA.md` | — | `TIENI` | **si AMPLIA di una riga** *(la nuova regola di lavoro)*: `git log` **e' il repo**, e una smentita puo' vivere in un messaggio di commit — **misurato su `D09`** |
| **par.2** | il rito del sigillo, in ordine | `CLAUDE.md` | — | `TIENI` | e' il metodo di una prova: **cambia posto** e diventa la lista di controllo del posto 2 |
| **par.9-bis** | ogni numero porta la sua epoca | `CLAUDE.md` | — | `TIENI` | e' metodo di misura: **cambia posto** |

### → POSTO **3**: IGIENE TECNICA — **automatica**   *(i **hook** *(`.githooks/`, `csv/_hook_*.py`, `csv/_presidio_*.py`)*)* — **9 regole**

| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |
|---|---|---|:--:|:--:|---|
| **H-ANCORA** | un confronto che prende il codice di prima da `HEAD` invece dal PADRE | `hook` | **SI** | `AUTOMATICA` | oggi `P8`: nessuna collisione, ma il prefisso rende l'elenco leggibile |
| **H-CLI** | un sigillo che configura il modulo a mano invece di passare dal CLI | `hook` | **SI** | `AUTOMATICA` | oggi si chiama `P3` **e collide con `P3` di `CLAUDE.md`**: il prefisso `H-` dice *hook* |
| **H-COMMENTI** | un flag il cui commento cambia senza nominare quel flag | `hook` | **SI** | `AUTOMATICA` | oggi `P7` |
| **H-CONFIG** | un referto che non dichiara la configurazione INTERA | `hook` | **SI** | `AUTOMATICA` | oggi `P5`, **collide con `P5` di `CLAUDE.md`** |
| **H-FISICA** | una legge che cambia senza la sua scheda | `hook` | **SI** | `AUTOMATICA` | oggi `REG-R` |
| **H-INDICE** | un ID citato in un documento vivo o nel messaggio che non e' nell'indice | `hook` | **SI** | `AUTOMATICA` | oggi `INDICE` |
| **H-RELAZIONE** | un referto committato senza toccare la relazione | `hook` | **SI** | `AUTOMATICA` | oggi `P1-bis` nel hook: **stesso nome della regola di flusso**, e sono due cose diverse |
| **H-VALIDATORE** | un indice mal formato o con una voce persa | `hook` | **SI** | `AUTOMATICA` | gira nel `pre-commit` dal 2026-09-26 |
| **par.5-novies** | inventario, README e fisica nello stesso commit | `CLAUDE.md` | — | `AUTOMATICA` | ③ *(la fisica)* **e' gia' automatica** (`H-FISICA`); ① *(l'inventario)* e' **candidata a un hook**: un file nuovo in `csv/_test_fork/` o `csv/_seal_fork/` senza voce in `INVENTARIO_strumenti` viene rifiutato. **Finche' non c'e' il hook, resta una riga al posto 4** |

### → POSTO **4**: FLUSSO DI LAVORO — **una pagina**   *(`CLAUDE.md`)* — **24 regole**

| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |
|---|---|---|:--:|:--:|---|
| **L-DOPO-STOP** | dopo uno `STOP`, senza risposta si lavora **solo la coda**: nessuna cura fisica, nessun run lungo | `prompt di Luca 2026-09-26` | — | `TIENI` | **nuova**: e' il confine fra *aspettare* e *decidere al posto di Luca* |
| **L-NUMERI** | ogni numero scritto in un commit o referto **esce da uno script** | `prompt di Luca 2026-09-26` | — | `TIENI` | **assorbe `P1-ter`** *(che diceva la stessa cosa per le sole tabelle)*: piu' larga, e **una regola in meno** |
| **L-PATCH** | le patch si lanciano IN PRIMO PIANO; niente `git stash` con una patch in corso; nei patch script **niente escape**: `chr()` o `replace` | `prompt di Luca 2026-09-26` | — | `TIENI` | **entra dentro `P1-quater`** *(che parla delle sostituzioni di testo)*: stesso oggetto, stesso posto — **nessuna regola nuova** |
| **L-UN-PROMPT** | un prompt alla volta: i rilievi che arrivano durante un lavoro vanno in CODA, non lo interrompono | `prompt di Luca 2026-09-26` | — | `TIENI` | **nuova**: nessuna regola di oggi lo dice, e il difetto che previene e' reale *(un lavoro interrotto a meta' lascia il repo in uno stato che nessuno ha dichiarato)* |
| **P1** | non usare l'associazione senza verificare lo storico | `CLAUDE.md par.0-ter` | — | `TIENI` | e' il prerequisito di scrittura: resta, in **una riga** |
| **P1-bis** | la relazione si scrive nello stesso commit del riscontro | `CLAUDE.md par.0-ter` | — | `FONDI` | **fusa con `P1-bis-bis`, par.5-ter, par.5-sexies e par.5-octies** in UNA regola di flusso: *tutto cio' che si dice a Luca va nel repo nello stesso giro*. **Il hook la rende automatica in parte** (`H-RELAZIONE`) |
| **P1-bis-bis** | ogni messaggio a Luca finisce con `PUSHATO: <hash>` | `CLAUDE.md par.0-ter` | — | `FONDI` | **nella stessa regola di `P1-bis`**: e' la sua forma verificabile dal destinatario |
| **P1-quater** | ogni sostituzione di testo si asserisce per se' | `CLAUDE.md par.0-ter` | — | `TIENI` | resta, **e guadagna la riga sugli escape**: nei patch script niente `\t`/`\b`/`\s`, si usa `chr()` o `replace` — **quattro volte in un giorno un escape e' morto in un patch** |
| **P1-ter** | una tabella di numeri si genera da codice | `CLAUDE.md par.0-ter` | — | `FONDI` | **assorbita dalla regola di lavoro nuova**: *ogni numero scritto in un commit o referto esce da uno script*. Piu' larga e piu' semplice |
| **P2** | prima di escludere un flag: forza il sistema o lo CORREGGE? | `CLAUDE.md par.0-ter` | — | `TIENI` | resta, in una riga, accanto al punto 5 *(lo stato dei flag e' un dato, non una regola)* |
| **par.0** | ruolo e postura: guardiano, verifica dal codice | `CLAUDE.md` | — | `TIENI` | resta **asciugata**: 55 righe oggi, la parte sui blob storici va al posto 5 |
| **par.0-bis** | che cosa si legge all'avvio | `CLAUDE.md` | — | `TIENI` | resta, e **si accorcia**: l'elenco dei documenti d'avvio scende *(vedi i conteggi in testa)* |
| **par.0-ter** | i pattern comportamentali `P1`-`P6` | `CLAUDE.md` | — | `FONDI` | **la sezione sparisce come contenitore**: i `P` vanno al posto giusto *(2 o 4)*, e le 208 righe di storia vanno in `doc/STORIA_REGOLE.md` |
| **par.0-zero** | il bersaglio: le tre prove di `IPOTESI_gravita_a_spinta` | `CLAUDE.md` | — | `TIENI` | e' l'orientamento del progetto: resta, 3 righe |
| **par.1** | un interruttore alla volta | `CLAUDE.md` | — | `TIENI` | regola d'oro del flusso: resta |
| **par.11** | l'indice dei difetti: come si usa | `CLAUDE.md` | — | `TIENI` | **resta, ed e' collaudata** *(`csv/_collaudo_istruzioni.py`, 6/6: la sezione basta da sola)*. Si asciuga solo se il collaudo continua a passare |
| **par.5** | politiche di commit | `CLAUDE.md` | — | `TIENI` | resta, asciugata: molte parti sono **gia' automatiche** nei hook |
| **par.5-octies** | ogni resoconto si committa anche a meta' run | `CLAUDE.md` | — | `FONDI` | **nella regola unica di `P1-bis`** |
| **par.5-quinquies** | il codice di una misura dev'essere recuperabile | `CLAUDE.md` | — | `FONDI` | la **regola** resta in una riga *(blob committato, o copia accanto ai dati)*; le **130 righe di storia** *(la trappola CRLF, le due convenzioni di hash)* vanno in `doc/STORIA_REGOLE.md` |
| **par.5-septies** | il task history si scrive e si committa PRIMA | `CLAUDE.md` | — | `TIENI` | resta, **asciugata a 12 righe**: le tre sezioni e il rito, senza i precedenti |
| **par.5-sexies** | una domanda si committa col suo ragionamento | `CLAUDE.md` | — | `FONDI` | **nella regola unica di `P1-bis`**: una domanda e' un riscontro |
| **par.5-ter** | relazione a ogni riscontro | `CLAUDE.md` | — | `FONDI` | **nella regola unica di `P1-bis`** |
| **par.7** | i documenti di riferimento | `CLAUDE.md` | — | `TIENI` | resta come **elenco**, una riga per documento |
| **par.8** | il principio guida | `CLAUDE.md` | — | `TIENI` | 5 righe: resta |

### → POSTO **5**: STATO E FATTI DAL CODICE   *(`doc/STATO_RUN.md` + `doc/INDICE_ID.tsv`)* — **7 regole**

| id | la regola, in una riga | oggi sta in | automatica? | verdetto | perche' |
|---|---|---|:--:|:--:|---|
| **STANDARD 6** | ogni difetto acclarato si registra SUBITO | `doc/PATTERN_DI_PROVA.md` | — | `FONDI` | **assorbita dal punto 5**: dal 2026-09-26 un difetto nuovo E' una riga dell'indice, e **il hook lo impedisce**. Da regola di metodo a **fatto meccanico** |
| **par.10** | promozione delle componenti | `CLAUDE.md` | — | `TIENI` | il **criterio** *(tre condizioni)* resta in `COMPONENTI_PROMOSSE.md`, dove vive il registro; al posto 4 **una riga** col rimando |
| **par.4** | le regole fisiche da non violare *(SU(2), Verlet, locale pura...)* | `CLAUDE.md` | — | `TIENI` | **non sono regole di lavoro: sono FISICA** → `doc/REGISTRO_FISICA.md`, dove le leggi vivono |
| **par.5-bis** | auto-manutenzione dei documenti vivi | `CLAUDE.md` | — | `FONDI` | **assorbita dal punto 5**: lo stato sta nell'indice, e il validatore lo controlla |
| **par.5-quater** | il registro dei fronti aperti | `CLAUDE.md` | — | `FONDI` | **assorbito dall'indice**: i fronti sono voci, e `RAMIFICAZIONI` e' una fonte dell'indice |
| **par.6** | stato e ordine del lavoro | `CLAUDE.md` | — | `TIENI` | **e' STATO, non una regola** → `STATO_RUN` *(dove gia' vive la coda unica)* |
| **par.9** | i fatti verificati dal codice | `CLAUDE.md` | — | `TIENI` | **671 righe su 1575: il 43 % di `CLAUDE.md` NON E' UNA REGOLA, sono FATTI** → `doc/FATTI_dal_codice.md`, citato dal posto 4 e **letto quando serve**, non all'avvio |

### → **ESCONO** — 1

| id | la regola | verdetto | perche' esce |
|---|---|:--:|---|
| **P1-quinquies** | prima di un clip, un pavimento o un tetto: `A11` | `TOGLI` | **e' solo un puntatore ad `A11`**, che e' un assioma e non si tocca. Un puntatore non e' una regola: **il posto 1 basta** |

---

## 🔒 TRE MECCANISMI CONTRO LA RICRESCITA

| | meccanismo | come si fa rispettare |
|---|---|---|
| **1** | **una regola nuova ne SOSTITUISCE una** *(`STANDARD 10` applicato alle regole)* | il posto 2 ha un **tetto di 10**: il validatore del posto 2 conta le righe della tabella e **rifiuta l'undicesima** |
| **2** | **`CLAUDE.md` non passa le 400 righe** | un **presidio nel `pre-commit`**: conta le righe e **rifiuta il commit** *(con la via d'uscita dichiarata, come gli altri)* |
| **3** | **a ogni tag d'epoca si rivedono le regole MAI SCATTATE** | un presidio che non ha mai rifiutato niente **non sta impedendo niente** (`A9`): o il difetto non esiste piu', o il presidio non funziona. **I hook contano gia' le proprie invocazioni** |

---

## 📁 `RELAZIONE_PER_CLAUDE.md`: **20364 righe** — proposta di archivio

**Il file vivo tiene SOLO il giorno corrente**; i giorni chiusi vanno in
**`doc/relazioni/<AAAA-MM-GG>.md`**, uno per giorno.

**Perche' non e' solo estetica:** la relazione e' il file che una sessione nuova legge **per
primo**, e a 20364 righe **non la legge nessuno per intero** — quindi il suo scopo *(chi arriva da
fuori si allinea senza la conversazione)* **e' gia' perso oggi**. **Un archivio per giorno lo
restituisce**, e il `git log` resta l'indice.

---

## ✅ IL CONTROLLO DA SCRIPT: nessun comportamento si perde

```
id estratti dalle fonti ............ 76
id CON una destinazione ............ 76
id SENZA destinazione .............. 0   <- se non e' 0 lo script SI FERMA
destinazioni orfane (id non trovati) 0   
```

**Lo script si ferma** se un id dell'inventario non ha una destinazione: *nessun comportamento
imposto da Luca puo' sparire in silenzio*. **Ed e' il controllo che rende questa proposta
verificabile invece che persuasiva.**

## ⚠ COSA QUESTA PROPOSTA *NON* DICE

- **non dice che le destinazioni siano giuste**: sono **il mio giudizio**, una riga per id, e si
  correggono in un posto solo. **I numeri sono misurati, le destinazioni no.**
- **non ho scritto i documenti nuovi** *(`STORIA_REGOLE.md`, `FATTI_dal_codice.md`,
  `doc/relazioni/`)*: sono **destinazioni proposte**, e scriverli sarebbe **applicare**.
- **il `~153` di `CLAUDE.md` DOPO e' una STIMA con un'IPOTESI DICHIARATA**, non una misura:
  una sezione che **esce** vale `0`, una **fusa** vale `2` righe *(il rimando)*, una che **resta**
  vale il **40 %** se oggi supera le 20 righe. **La misura vera si fa solo applicando**, e la
  prima versione di questo conto dava **497** — *sopra la soglia che la proposta stessa chiede*:
  **l'ho rifatta invece di arrotondarla.**
- **il tetto di 10 al posto 2 oggi e' SUPERATO in proposta di zero**: gli `STANDARD` restano 8
  *(due fusi)*, e vi si aggiungono **`P1-sexies`, `P3`, `P4`, `P5`, `P6`, `par.2`, `par.9-bis`,
  `L-SOGLIA`**. **Sono 16, e il tetto e' 10: la proposta NON ci sta, e lo dico.** Serve una
  seconda fusione, e la propongo in coda a questo documento.

### ⚠ **IL CONTO DEL POSTO 2 NON TORNA: 16 regole per un tetto di 10**

**Lo dico invece di nasconderlo.** La fusione che propongo, e che porterebbe il posto 2 a **10**:

| si fondono | in una regola sola | perche' |
|---|---|---|
| `P3` + `P6` + `par.9-bis` | **«un numero senza la sua barra d'errore, il suo seme, i suoi flag e la sua EPOCA non e' un dato»** | sono tutte e tre *«un numero va qualificato»*: la barra, la provenienza, l'epoca |
| `P4` + `L-SOGLIA` | **«prima di misurare, verifica che la grandezza sia LIBERA di cambiare; e una soglia non si calcola dai dati che giudica»** | sono il **test vuoto** visto da due lati: una grandezza ancorata a se stessa, e una soglia ancorata ai propri dati |
| `STANDARD 3` + `STANDARD 4` | **«si confronta lo stesso istante, e cio' che NON C'E' si registra come assente»** | entrambe parlano di **che cosa si confronta con che cosa** |

**Con queste tre fusioni il posto 2 va a 10**, e il totale delle regole scende ancora di **4**.
