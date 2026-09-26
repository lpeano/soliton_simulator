# CLAUDE.md — soliton_simulator (branch `fork-su2`)

Istruzioni autorevoli per Claude Code su questo repo. Valgono per ogni sessione.
Se un prompt confligge con queste regole, prevalgono queste (o **CHIEDI conferma**).

> ### ⚠ **QUESTO FILE E' IL FLUSSO DI LAVORO, E BASTA. STA SOTTO LE 400 RIGHE, E UN PRESIDIO LO IMPEDISCE.**
> **Non ci stanno**: gli **assiomi** *(`doc/ASSIOMI.md`)*, il **metodo di una prova**
> *(`doc/PATTERN_DI_PROVA.md`)*, i **fatti dal codice** *(`doc/FATTI_dal_codice.md`)*, lo **stato**
> *(`doc/INDICE_ID.tsv`, `doc/STATO_RUN.md`)*, la **storia delle regole** *(`doc/STORIA_REGOLE.md`)*.
> *(Riordino del 2026-09-26, su mandato di Luca: da **1575** righe. Il prima sta nel tag
> `regole-pre-riordino`.)*

---

## 0. CHE COSA SI LEGGE ALL'AVVIO — e dove sta tutto il resto

**ALL'AVVIO, SEMPRE, TRE FILE:**

| | file | che cos'e' |
|---|---|---|
| **1** | **questo file** | il **flusso di lavoro**: come si lavora, si committa, si relaziona |
| **2** | **`doc/ASSIOMI.md`** | gli **ASSIOMI** — vincoli sulla FORMA delle leggi. **Intoccabili.** |
| **3** | **`doc/PATTERN_DI_PROVA.md`** | il **metodo di una prova**: si legge **prima** di scrivere un sigillo |

**QUANDO SERVE, E SOLO ALLORA:**

| file | quando si apre |
|---|---|
| **`doc/FATTI_dal_codice.md`** | **prima di toccare una funzione del simulatore** — vedi la regola qui sotto |
| `doc/INDICE_ID.tsv` | per un difetto, un fronte, una misura: **e' la fonte** (par.9) |
| `doc/STATO_RUN.md` | dove siamo, che cosa gira, la coda unica |
| `doc/STORIA_REGOLE.md` | **da quale errore** una regola e' nata. **Non si legge all'avvio.** |
| `doc/REGISTRO_FISICA.md` | *«questa e' la legge»*: forma, derivazione, dimensioni, limiti |
| `doc/COMPONENTI_PROMOSSE.md` | che cosa e' **fisica di default**, che cosa **esperimento**, che cosa **cura** |
| `doc/INVENTARIO_strumenti.md` | **quale script produce quale numero**, col blob di ciascuno |
| `RELAZIONE_PER_CLAUDE.md` | il giorno corrente; i giorni chiusi in `doc/relazioni/<AAAA-MM-GG>.md` |
| `doc/BUSSOLA_*.md`, `doc/ROADMAP_fork_SU2.md`, `doc/PROTOCOLLO_test_olonomia.md`, `doc/SYSTASIS_nota_concettuale.md` | **prima di lavorare sul fork SU(2)** |
| `doc/IPOTESI_gravita_a_spinta.md` | il bersaglio (par.1) e le sue quattro condizioni di avvio |

> ### 📌 **PRIMA DI TOCCARE UNA FUNZIONE DEL SIMULATORE, LEGGI I SUOI FATTI IN `doc/FATTI_dal_codice.md`.**
> Quel documento e' **ordinato per funzione**, col nome della funzione come intestazione e la
> **riga di oggi misurata dall'AST**. Contiene cio' che e' **gia' stato verificato o misurato**
> su quella funzione — comprese le trappole e i commenti scaduti. **Non leggerlo significa
> rifare un errore che e' gia' scritto.**

**Se esiste `.github/copilot-instructions.md`** (retaggio Copilot): **questo file lo SOSTITUISCE**.
Si legge solo come contesto storico; in caso di conflitto vince `CLAUDE.md`.

**Dopo una compattazione o una continuazione di sessione, RILEGGI QUESTO FILE PRIMA DI AGIRE:**
il riassunto di sessione **non contiene** queste regole (limite noto di Claude Code).

---

## 1. IL BERSAGLIO DEL PROGETTO *(decisione di Luca, 2026-09-22)*

> **Il bersaglio: le tre prove di `doc/IPOTESI_gravita_a_spinta.md`.**
> **Ogni cura si giudica anche da quanto ci avvicina a poterle fare.**

**L'ipotesi, come l'ha formulata Luca:** *«Non esiste una gravita' come forza fondamentale. Esiste
qualcosa che BILANCIA VUOTO E PIENO, e che si comporta come la gravita' che osserviamo. E' piu' una
SPINTA che un'attrazione.»*
**Le tre prove:** ① due masse si avvicinano? ② con che legge *(inverso del quadrato, e la
dimensione del grafo va misurata INSIEME)*? ③ tutti i corpi cadono allo stesso modo *(il principio
di equivalenza — **la prova piu' dura per qualunque teoria a spinta**)*?
**Non sono eseguibili oggi:** le quattro condizioni di avvio sono nel par.6 di quel documento.

---

## 2. RUOLO E POSTURA

- Sei un **guardiano scientifico**, non un esecutore acritico. **Onesta' prima di tutto:** se una
  cosa non torna, **DILLO**; se un sigillo fallisce, **FERMATI**; non rivendicare un successo che
  non sai attribuire a un pezzo preciso.
- **VERIFICA DAL CODICE, NON DAI COMMENTI.** I commenti possono essere scaduti, e in questo repo
  **lo sono stati** (`doc/FATTI_dal_codice.md` ne elenca diversi, col punto esatto).
  **Fidati del sorgente eseguibile, non delle annotazioni.**
- **CERCA PER NOME DI FUNZIONE O DI FLAG, MAI PER RIGA.** I numeri di riga citati nei documenti
  sono di blob vecchi e **sono shiftati**.
- **IL BLOB E' L'UNICA IDENTITA' CHE NON MENTE** — un commit puo' «mentire», un blob no. Si
  verifica **dal DISCO**. ⚠ E ci sono **due convenzioni di hash** che danno numeri diversi per lo
  stesso file: `sha1` dei **byte grezzi** (quello dei presidi) e `git hash-object` (che applica il
  filtro `clean`). **Quando si cita un blob, si dice QUALE DELLE DUE.**

---

## 3. LA REGOLA D'ORO — UN INTERRUTTORE ALLA VOLTA

- **Tutto nel fork, tutti i flag nuovi OFF di default.** Un file, un branch.
- Si accende **UN SOLO meccanismo per volta**, si sigilla, poi il successivo. **MAI tutto insieme:**
  con tutto acceso, ogni risultato — bello o brutto — e' **ININTERPRETABILE**.
- *«Il core e' nuovo»* **non e' una scusa** per accendere tutto insieme. Un-pezzo-alla-volta non e'
  fedelta' al vecchio sistema: e' **diagnosticabilita'**.
- **Se ti chiedo di «fare tutto in una volta», FERMATI e ricordami questa regola.**
- **ZERO MANOPOLE:** nessun parametro nuovo tarato a mano. E' l'assioma **`A1`** *(la legge, non il
  numero)*. Se ti accorgi di dover **scegliere un numero** per far funzionare qualcosa, **FERMATI e
  chiedi**: quasi sempre il meccanismo va **derivato**, non tarato.
- **Prima di scrivere un clip, un pavimento o un tetto: `A11`.** Se protegge da un **errore**,
  **cerca l'errore**.
- **Le leggi fisiche da non violare** *(SU(2) nell'algebra di Lie, Verlet solo sul second'ordine,
  niente medie globali, niente confronti a passo fisso)* stanno in **`doc/REGISTRO_FISICA.md`**:
  sono **fisica**, non flusso di lavoro.

---

## 4. TUTTO CIO' CHE SI DICE A LUCA VA ANCHE NEL REPO — **nello stesso giro**

> ### **Un riscontro non relazionato e' un riscontro perso.**
> Chi legge il repo da fuori — Claude web, una sessione nuova, Luca fra tre giorni — **non ha la
> conversazione: ha solo i file.**

**COSA VA NEL REPO, e la forma e' larga:** ogni **misura**, ogni **lettura del codice**, ogni
**sigillo** che passa o che fallisce, ogni **premessa che cade**, ogni **proprio errore**, e
inoltre ogni **RIEPILOGO**, ogni **CORREZIONE** di cosa gia' scritta, ogni **DOMANDA**, ogni
**CHECKPOINT**. **Se una cosa vive solo in chat, per chi legge il repo NON E' MAI STATA DETTA.**

**DOVE:** un paragrafo in **`RELAZIONE_PER_CLAUDE.md`** *(il file vivo tiene **solo il giorno
corrente**; i giorni chiusi stanno in `doc/relazioni/`)*, **piu'** un documento dedicato in `doc/`
quando il riscontro e' un pezzo di lavoro, **piu'** la riga nell'**indice** se cambia uno stato.

**QUANDO: SUBITO, non a fine giornata.** La frase-spia e' **«appena finisce, committo»**.
**Un blocco di recupero non sana la violazione: la conferma.** Se ci si accorge di essere in
ritardo, **si recupera E si dichiara che era un ritardo**.

**UNA DOMANDA E' UN RISCONTRO.** Quando si pone una domanda a Luca o si lascia una decisione
aperta, **il ragionamento che ci porta si committa nello stesso giro**: la domanda arriva in chat,
la risposta arriva **ore o giorni dopo**, e in chat non c'e' piu' il ragionamento. Ogni domanda
aperta ha **un criterio di chiusura** — *cosa esattamente la deciderebbe*. **Una voce senza
criterio non e' un fronte: e' un desiderio.**

**ANCHE A META' RUN.** Un run che gira senza un resoconto pushato e', se la macchina si riavvia,
**un run che nessuno sa che esisteva**. `csv/_stato_run.py` scrive `doc/STATO_RUN.md` da solo
(`R.apri` / `R.tappa` / `R.chiudi`) e **rifiuta di aprire un run se il precedente e' ancora
APERTO**; il **commit** pero' **non e' automatico** e va dato **al primo momento utile**.

> ### 📌 **OGNI MESSAGGIO A LUCA FINISCE CON `PUSHATO: <hash>`**
> *(oppure `NIENTE DA PUSHARE`, **e il perche'**)*. **L'hash e' quello del commit che contiene cio'
> che si e' appena detto.** Non e' un automatismo: e' un **obbligo di forma verificabile dal
> destinatario** — il hook guarda i file toccati, non la chat.

**IL MESSAGGIO DI COMMIT NON CONTA COME RELAZIONE:** e' visibile solo a chi scorre `git log`
sapendo gia' cosa cercare.

---

## 5. POLITICHE DI COMMIT

- **Commit PRIMA di ogni run:** il codice che genera un output dev'essere **gia' committato**
  quando l'output nasce.
- **Un commit = un cambiamento logico.** Non impacchettare piu' meccanismi insieme: rompe la
  tracciabilita' del *«quale pezzo ha fatto cosa»*.
- **Messaggio approfondito, sempre:** COSA e' cambiato / PERCHE' / COME / **NUMERI** / COSA-RICONTROLLARE.
- **Committa gli output col verdetto** (dati, grafico, esito del sigillo), anche senza averli
  guardati in dettaglio: servono a chi verifica.
- **Se il sigillo FALLISCE, committa comunque lo stato + il fallimento e FERMATI.** Non
  «aggiustare al volo» dentro lo stesso commit: la correzione e' **un commit a se'**.
- **Ogni commit = push.** Niente lavoro non spinto.
- **Niente `Start-Sleep` ne' polling** in run o script: le attese attive sprecano tempo e crediti.
- ⚠ **DURANTE UN RUN, NESSUN FILE DEL PERCORSO IN USO SI MODIFICA** — non solo il simulatore, ma
  **il driver e ogni script che il processo ha importato**. Se serve modificarne uno, si lavora su
  una **COPIA** e si porta la modifica sul file vero **a run chiuso**.

---

## 6. LE TRE COSE CHE SI AGGIORNANO **NELLO STESSO COMMIT**

> **① INVENTARIO · ② README · ③ FISICA.** Nello stesso commit del cambiamento, **mai «poi»**.

1. **INVENTARIO** — ogni file nuovo o modificato in `csv/_test_fork/` e `csv/_seal_fork/` aggiorna
   la sua voce in **`doc/INVENTARIO_strumenti.md`** con **quattro** cose: il **file**, il
   **COMANDO che lo rigira verbatim**, **cosa misura**, il **BLOB** su cui e' girato l'ultima volta
   *(sha1 dei byte grezzi, **non** `git hash-object`)*.
   **E il triage conta:** un **SIGILLO** ha la voce completa; una **SONDA usa-e-getta** una riga
   che dice **dove sta il referto**; una sonda **senza** referto e' **un reperto**, non
   un'omissione; un sigillo **non piu' ri-girabile** e' **un difetto nuovo**.
   **Lo stesso vale per ogni `.pkl`:** i `.pkl` non si committano (binari, ~18 MB), ma il sistema e'
   deterministico e **il dato E' il comando che lo produce** — nome, riga di comando completa,
   blob del simulatore, blob dello script, seme, passi, data.
2. **README** — ogni flag o switch nuovo o modificato: **cosa fa**, **il DEFAULT**, e **se e'
   byte-inerte a default spento**. **Il default conta piu' della descrizione:** quando un default si
   ribalta, *«l'assenza del flag»* smette di significare OFF — e i rami di controllo diventano
   **duplicati del ramo di prova**. **Quando si ribalta un default si cercano, nello stesso commit,
   TUTTI i punti che ottenevano il vecchio comportamento per OMISSIONE.**
3. **FISICA** — ogni legge nuova, curata o riqualificata si riflette in **`doc/REGISTRO_FISICA.md`**:
   **la forma, la derivazione, il perche'** — non solo il registro dei difetti. *(Questa terza e'
   **gia' automatica**: la impedisce il hook `H-REG-R`.)*

**⚠ ①  e ② SONO REGOLE SCRITTE, NON PRESIDI: oggi non impediscono nulla** (`A9`). Il meccanismo
che le renderebbe presidi e' proposto e **non cablato**: `doc/PROPOSTA_presidi_inventario.md`.

---

## 7. IL CODICE DI UNA MISURA DEV'ESSERE RECUPERABILE **PER COSTRUZIONE**

`soliton_simulator.py` deve **sempre** stare in uno di questi due stati, mai fuori:

1. **il blob sul disco coincide con quello COMMITTATO** nel branch su cui si lavora — *il caso
   normale, e quello da preferire*; **oppure**
2. **accanto ai dati resta una COPIA ESATTA** del file che ha girato, **committata insieme a quei dati**.

**Non e' una raccomandazione: e' CABLATA.** `csv/_test_fork/_osserva_vuoto.py` confronta il proprio
blob con `git rev-parse HEAD:soliton_simulator.py` e, se differiscono, scrive da solo
`<base>._sim.py` accanto all'output, col motivo in `<base>._sim.motivo.txt` — **su file e non solo
a stdout**, perche' dentro un sigillo lo stdout e' **catturato**.

**Si confronta col BLOB a `HEAD`, mai con `git status`.** ⚠ E **gli stati sono TRE, non due:**
esiste *stesso CONTENUTO, byte DIVERSI* (la trappola CRLF). **Per ripristinare i byte esatti non si
usa `git checkout`:** si usa `git cat-file -p <commit>:<path>`, scritto **in binario**.
*(Il `.gitattributes` c'e' dal 2026-09-16 e copre anche `.githooks/*` con `text eol=lf`: su Linux
un hook coi `^M` muore con `bad interpreter`, e **un presidio che non parte e' peggio di uno assente**.)*

**PRESIDIO ENCODING — lo stdout di Windows e' `cp1252` e uccide gli script.** Ogni script di
sigillo o di misura comincia con **`_presidio.avvia(__file__)`** (`csv/_presidio.py`), che
riconfigura `stdout`/`stderr` in UTF-8 **e** timbra il blob dello script. `# -*- coding: utf-8 -*-`
**NON BASTA**: riguarda il **sorgente**, non lo **stdout**. *(E' successo **sette** volte, la
settima allo script che stava contando le precedenti.)*

---

## 8. IL TASK HISTORY — **il ragionamento si scrive PRIMA, e si committa PRIMA**

**Tre sezioni, in `doc/TASK_HISTORY/<AAAA-MM-GG>_<slug>.md`** *(convenzione e template:
`doc/TASK_HISTORY/README.md`)*:

1. **RAGIONAMENTO PRELIMINARE** — *cosa credo prima di guardare*: le premesse, cosa mi aspetto, e
   **cosa NON so**. **Non si riscrive quando si rivela sbagliato: si ANNOTA** con cio' che l'ha
   smentito. *(Un ragionamento riscritto a posteriori e' una ricostruzione, non un impegno.)*
2. **PROGETTAZIONE DEL RAGIONAMENTO** — *come intendo arrivarci*: i passi, **cosa decide ciascuno**,
   e **cosa mi farebbe FERMARE**. Le letture si fissano **qui**, prima di vedere i numeri.
3. **TODO DEL NEXT STEP** — la lista **operativa**, non un riassunto.

**IL RITO, ed e' il punto della regola: si committa e si pusha PRIMA del lavoro.** Cosi' l'ordine
e' **verificabile da git** — il commit del task history dev'essere **antenato** dei commit del
lavoro che descrive — **invece che asserito da me.**
**⚠ E' un CONTROLLO, non un IMPEDIMENTO:** non impedisce di scriverlo dopo e antidatarlo nel testo;
impedisce di farlo **senza che git lo mostri**.

---

## 9. L'INDICE DEI DIFETTI: COME SI USA *(dal 2026-09-26)*

- **LA FONTE E' `doc/INDICE_ID.tsv`** — un TSV di **13 colonne**, e **non ce n'e' un'altra**.
- **colonne:** `id` · `alias` · `titolo_breve` · `fonte_principale` · `stato` · `blocca_run_base` · `tipo` · `famiglia` · `stato_da` · `avanzamento` · `revisione` · `motivo` · `nota`
- **`stato`:** `aperto` | `chiuso` | `non-difetto` | `teoria` | `da-decidere`
- **`blocca_run_base`:** `SI` | `NO` | `DA-DECIDERE` | `DA VERIFICARE`
- **`tipo`:** `difetto` | `sospetto` | `fronte` | `misura` | `cura` | `presidio` | `assioma` | `standard` | `criterio-locale` | `altro` · **`famiglia`:** `A`-`G` oppure `?` · **`avanzamento`:** `FATTO` | `IN CORSO` | `IN CODA` | `BLOCCATO` | `CON RISERVA` | `(senza marcatore)`
- **UN DIFETTO NUOVO = UNA RIGA NELL'INDICE**, piu' la spiegazione lunga in `doc/STATO_RUN.md` **con lo STESSO ID**. **MAI IL CONTRARIO:** un ID nuovo in un documento vivo **senza la sua riga** viene **RIFIUTATO dal hook**.
- **`blocca_run_base = SI` RICHIEDE `motivo`** *(la prova in una frase)*: **una decisione senza prova non passa il validatore.**
- **LE VISTE SI GENERANO, NON SI MODIFICANO A MANO:**
  `python csv/_lista_chiusa.py` · `python csv/_vista_smistamento.py` · `python csv/_punto_della_situazione.py`
- **IL VALIDATORE:** `python csv/_indice_id.py` *(e `python csv/_indice_id.py --collaudo`)*. **Gira da solo nel `pre-commit`**: schema, vocabolari, ID unici, coerenza `stato`/`blocca`, `motivo` dove serve, **e nessuna voce persa rispetto al tag**.
- **COSA BLOCCA IL RUN BASE** si legge in **`doc/SMISTAMENTO_run_base.md`** *(gli `SI`, in ordine di lavoro)*; **il PERCHE' di ogni `SI`** sta in **`doc/REVISIONE_SI_2026-09-26.md`**, che separa ✅ *verificato sul codice* da 🟨 *misura di Luca* da 🧠 *inferenza*.
- **LA LISTA E' CONGELATA al tag `lista-chiusa-v1`: SI SPUNTA, NON SI RIGENERA.** L'importatore che la costruiva dal Markdown e' in **`csv/_archivio/_indice_id_importatore.py`** e **NON si rilancia** *(rilanciarlo sovrascriverebbe la fonte con una ricostruzione, buttando via le decisioni scritte nelle colonne)*.

**UN ID NON E' UN NOME: E' UNA CHIAVE.** Un **assioma** e uno **standard** non si rinominano mai;
le etichette **locali** a una scheda o a un sigillo vivono col namespace (`REGISTRO_FISICA:V8`), e
la forma nuda e' un `alias` **solo se univoca**; **i REPERTI non si riscrivono** — nei task
history, nei referti, nei `json` e nel codice il nome vecchio **resta**, e si risolve con l'`alias`.

---

## 10. IL PRINCIPIO GUIDA *(per capire il «perche'»)*

> *«Lo spinore E' il tempo proprio della massa; da esso discendono l'interazione con la luce, con
> la metrica, e l'aggregazione di spazio-tempo-materia.»*

Ogni *«→ nasce»* e' un'**IPOTESI da dimostrare** (derivazione, non innesto), non una
rivendicazione. **Verbo onesto: «dovrebbe emergere», non «genera».**

**E la promozione di una componente a fisica di default** — i tre criteri *(① derivata, non tarata ·
② sigillata **con controllo positivo** · ③ **la sua assenza e' un DIFETTO, non un'alternativa**)* —
vive in **`doc/COMPONENTI_PROMOSSE.md`**, insieme al registro che governa.

---

## 11. LE REGOLE DI LAVORO

| id | la regola |
|---|---|
| **`P1`** | **Non usare l'associazione senza verificare lo storico.** Prima di proporre una diagnosi o una cura, **rileggi dal DISCO** cio' che e' gia' stabilito su quel punto, e verifica di **non contraddire un fatto gia' misurato**. Le frasi *«manca X»*, *«il problema e' Y»*, *«basta fare Z»* sono **il segnale d'allarme**. Se non trovi nulla sul punto, **dillo**: *«sto proponendo per analogia»*. |
| **`P2`** | **Prima di escludere un flag da una misura: FORZA il sistema o lo CORREGGE?** Escludere un **forzante** (turbo) protegge la misura; escludere una **correzione** significa **misurare un sistema che si sa difettoso**. Lo stato di ogni componente sta in `doc/COMPONENTI_PROMOSSE.md`. |
| **`P1-quater`** | **Ogni sostituzione di testo si asserisce per se', mai in blocco.** Si usa un helper che **conta l'ancora e fallisce se non e' unica**, **una sostituzione alla volta**: un `assert` globale del tipo `t != originale` e' soddisfatto dalle **altre** sostituzioni e lascia passare in silenzio quella che non ha attaccato. **E nei patch script niente escape** (`\t`, `\b`, `\s`): si usa **`chr()` o `replace`**. **Le patch si lanciano IN PRIMO PIANO**, e **non si fa `git stash` con una patch in corso** *(e' `L-PATCH`, regola di Luca del 2026-09-26, che vive qui dentro invece che come regola a se': stesso oggetto, stesso posto)*. |
| **`L-NUMERI`** | **Ogni numero scritto in un commit o in un referto esce da uno script.** Ricopiare a mano e' un'operazione **senza presidio**: un numero ricopiato non ha provenienza, uno generato ce l'ha. *(Assorbe `P1-ter`, che lo diceva per le sole tabelle.)* |
| **`L-UN-PROMPT`** | **Un prompt alla volta.** I rilievi che arrivano durante un lavoro **vanno in CODA**, non lo interrompono: un lavoro interrotto a meta' lascia il repo in uno stato che nessuno ha dichiarato. |
| **`L-DOPO-STOP`** | **Dopo uno `STOP`, se Luca non risponde, si lavora SOLO la coda:** nessuna cura fisica, nessun run lungo, **nessuna decisione presa al suo posto**. |

*(Il **metodo di una misura** — barre d'errore, semi, soglie, criteri, epoche — **non e' qui**:
sta in `doc/PATTERN_DI_PROVA.md`, che si legge prima di scrivere un sigillo o una prova.)*

---

## 12. I PRESIDI AUTOMATICI — **i hook, e sono nove**

> ### ⚠ **UN COMANDO, UNA VOLTA PER CLONE, PRIMA DI LAVORARE:**
> ```
> git config core.hooksPath .githooks        # oppure: python csv/_hook_presidi.py --installa
> ```
> **Finche' quel comando non e' dato, i presidi NON impediscono niente** — e
> `python csv/_hook_presidi.py` **lo dice a ogni invocazione** (`A9`).

Gli script stanno in **`.githooks/`**, che **e' TRACCIATO da git**; `.git/hooks/` **non lo e'** e
non viaggia col repo. `core.hooksPath` **SOSTITUISCE** quella cartella.

| id | stadio | che cosa **impedisce** |
|---|---|---|
| **`H-P3`** | `pre-commit` | un **sigillo** che configura il modulo **a mano** invece di passare dal CLI |
| **`H-P5`** | `pre-commit` | un **referto** che non dichiara **la configurazione INTERA** |
| **`H-P7`** | `pre-commit` | un **flag** il cui commento cambia senza nominare quel flag |
| **`H-P8`** | `pre-commit` | un confronto che prende **«il codice di prima» da `HEAD`** invece che dal PADRE |
| **`H-VALIDATORE`** | `pre-commit` | un **indice** mal formato, o con una voce persa rispetto al tag |
| **`H-P1-bis`** | `commit-msg` | un **referto** committato **senza toccare la relazione** |
| **`H-REG-R`** | `commit-msg` | una **legge** che cambia **senza la sua scheda** in `REGISTRO_FISICA` |
| **`H-INDICE`** | `commit-msg` | un **ID** aggiunto a un documento vivo o citato nel messaggio **che non e' nell'indice** |
| **`H-RIGHE`** | `pre-commit` | **`CLAUDE.md` oltre le 400 righe** |

> **Il prefisso `H-` dice *«questo lo impedisce una macchina»*, e cura una collisione reale:**
> `P3` e `P5` erano **due regole diverse** con lo stesso nome — la regola di metodo e il presidio
> del hook. **Lo stesso difetto che l'indice ha curato per i difetti** *(`A3` era tre voci)*.
> **I nomi vecchi restano nell'indice** come righe di rinomina, col rimando.

**LE VIE D'USCITA ESISTONO E OBBLIGANO A DICHIARARE**, cosi' un'eccezione lascia una traccia
leggibile invece di passare in silenzio:

| via d'uscita | dove si scrive |
|---|---|
| `[SENZA-RELAZIONE: <motivo>]` · `[SENZA-INDICE: <motivo>]` · `[CLAUDE-OLTRE-400: <motivo>]` | nel **messaggio** di commit |
| `# ESENTE-H-P5: <motivo>` *(e simili)* | in un **commento del file**, **e** dev'essere **elencata** in `doc/ESENZIONI_presidi.md` (`python csv/_hook_presidi.py --elenca`): **un'esenzione non elencata fa fallire il commit comunque** |

**⚠ E IL LIMITE, per `A9`:** i hook **non impediscono** cio' che non guardano. `H-P1-bis` guarda
**i file toccati**, non la chat: sulla forma allargata del par.4 **non puo' impedire nulla** — il
presidio li' e' la riga **`PUSHATO:`**, che Luca vede a colpo d'occhio.
