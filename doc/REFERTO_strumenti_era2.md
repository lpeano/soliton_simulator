# IL REFERTO DEGLI STRUMENTI DELL'ERA `2`

> ### ⛔ **LA DOMANDA A LUCA, e il referto esiste anche per farla:**
> ### 📌 **COME SI CHIAMA LA CARTELLA DEL CODICE DELL'ERA `2`?**
> Finche' non ha un nome, `H-FISICA-FUORI-LISTA` ### **non impedisce niente**, e per `A9` ### **non e' un presidio: e' una TENDA.** ### ✔ **Il codice c'e', il collaudo gira su una cartella di PROVA, e il giorno in cui il nome arriva il presidio diventa vero ### cambiando UNA STRINGA** in `csv/_file_fisica.py`.

| | |
|---|---|
| **quando** | `2026-10-09`, ramo `primo-ordine` |
| **il mandato** | la ### **parte II** di *«le chiusure, le superate, la terza lettura, e gli strumenti per l'era `2`»* — cioe' ### **il mandato «INDICE E FISICA» che non mi era arrivato**, piu' le tre correzioni `A`/`B`/`C` della coda |
| **la coda** | ### **la voce ① di `doc/CODA_2026-10-09.md` si CHIUDE qui**: era l'integrazione, e il mandato l'ha assorbita |
| **il simulatore** | `b8c21049`, ### **NON toccato** — nessuna corsa |

---

## ① CHE COSA BLOCCA, E CHE COSA E' SOLO SCRITTO

> ### ⭐ **`A9`: «un presidio che non impedisce non e' un presidio: e' una TENDA».** Questa tabella e' ### **l'unica cosa che conta** in un referto sugli strumenti — e un referto che non distingue le due colonne ### **racconta piu' sicurezza di quella che c'e'.**

| strumento | stadio | ### **BLOCCA?** | che cosa impedisce |
|---|---|---|---|
| ### **`F11`** | `indice.py valida`, nel `pre-commit` | ### **SI'** | una voce che ### **non coincide col `dopo` della sua ultima riga di storico**: cioe' ### **una scrittura a mano in `voci.jsonl`** |
| ### **`F12`** | `indice.py valida`, nel `pre-commit` | ### **SI'** | una `chiusura` ### **piena su una voce che non e' `CHIUSA`** |
| ### **`H-ID-OBBLIGATORIO`** | `commit-msg` | ### **SI'** | un commit che tocca ### **un file della LISTA** o un ### **`doc/REFERTO_*`/`doc/REPERTO_*`** e ### **non cita nessun ID** |
| ### **la LISTA** *(`FILE_FISICA`)* | letta da `H-REG-R` e `H-P7` | ### **SI', per interposta persona** | quei due presidi ### **non scrivono piu' il nome a mano**: il giorno in cui la fisica vive in due file ### **li seguono** |
| ### **l'`assert len(FILE_FISICA) == 1`** | all'import di `H-REG-R` e `H-P7` | ### **SI'** | che quei due presidi ### **guardino solo il primo file di una lista lunga**: il giorno in cui la lista cresce ### **si FERMANO** |
| ### ⛔ **`H-FISICA-FUORI-LISTA`** | `pre-commit` | ### ⛔ **NO, OGGI NO** | dovrebbe impedire ### **un `.py` sotto la cartella dell'era `2` fuori dalla LISTA**, ma ### **la cartella e' VUOTA**: `intrusi()` torna ### **sempre `[]`.** ### **E' una TENDA, e il nome lo decide Luca** |

### ✔ **E I TRE CABLATI SI VERIFICANO LEGGENDO IL HOOK, non questa tabella:**

| | dichiarato | ### **cablato davvero** |
|---|---|---|
| `H-FISICA-FUORI-LISTA` | si' | ### **si'** |
| `H-ID-OBBLIGATORIO` | si' | ### **si'** |
| `F11`, `F12` | `doc/REGOLE/par9.md` | ### **si'**: `indice.py valida` gira nel `pre-commit` *(`csv/_hook_presidi.py`, blocco `[INDICE v2]`)* |

---

## ② `F11`: **l'indice e' il REPLAY del suo storico**

| | |
|---|---|
| la regola | ogni voce coincide ### **campo per campo** col `dopo` della sua ### **ULTIMA** riga di storico; una voce ### **senza storico** coincide col suo stato a ### **`3ef2326`**; una voce ### **nata dopo e senza storico** e' un errore |
| ### ⭐ **perche' e' il piu' forte** | gli altri guardano ### **se un campo e' plausibile**; `F11` guarda ### **se il campo e' ARRIVATO DA UNA SCRITTURA DICHIARATA** |
| ### **e rende vera una regola che era solo SCRITTA** | il par.9 dice *«si scrive SOLO con `indice.py aggiorna`»* ### **dal primo giorno**, e per `A9` era ### **una tenda.** ### **Adesso impedisce** |
| oggi | ### **`0` violazioni** su `848` voci, `38` senza storico |

### ⚠ **E LA MANOMISSIONE CHE IL MANDATO DETTA LA VEDE ANCHE `F7`, e lo dico:** `A2-ANELLO` e' ### **era `1`**, e `F7` vieta era `1` + `APERTA`. ### **Quel caso prova che `F11` SCATTA, non che SERVA.** ### ✔ **Per provare che serve ho cercato una manomissione che nessun altro veda, e l'ho trovata: il `titolo`.** Nessun presidio lo confronta con niente — cambiarlo a mano passa ### **vocabolari, stati, ere e viste rigenerate** — e ### **solo `F11` lo vede.**

### ⛔ **E DUE COSE CHE `F11` NON VEDE, dichiarate:**

| | |
|---|---|
| una manomissione che tocca ### **ANCHE lo storico** | `F11` prova che i due file ### **CONCORDANO**, non che siano ### **veri.** ### **La difesa contro quello e' git, non `F11`** |
| un cambio del solo campo ### **`aggiornata`** | e' ### **fuori dal confronto**: e' un timbro di ### **quando**, e lo riscrive ogni lotto. ### **E' il prezzo dichiarato per non fallire su ogni voce toccata due volte** |
| se il tag ### **non si legge** | `F11` ### **TACE** invece di accusare: senza il punto di partenza non si puo' dire se una voce senza storico sia giusta |

---

## ③ LA LISTA E LA CARTELLA

| | |
|---|---|
| ### **`FILE_FISICA`** | `soliton_simulator.py` |
| ### **`CARTELLA_ERA_2`** | ### ⛔ **`""` — «da decidere da Luca»** |
| chi legge la LISTA | `csv/_hook_fisica.py` *(`H-REG-R`)* · `csv/_presidio_commenti_flag.py` *(`H-P7`)* · `csv/_hook_id_obbligatorio.py` *(`H-ID-OBBLIGATORIO`)* |
| ### ⚠ **e chi la nominava a mano** | erano ### **`3`**, e il censimento l'ho fatto ### **prima di dire il numero.** Il terzo *(`csv/_hook_presidi.py`)* lo nomina ### **dentro un testo d'aiuto**, non come percorso |
| ### ⛔ **e mettere un file nella LISTA COSTA** | gli si mettono addosso ### **TRE presidi**: `H-REG-R` *(nessuna legge senza la sua scheda)*, `H-P7` *(il commento di ogni flag)* e `H-ID-OBBLIGATORIO` *(un ID nel messaggio)*. ### **Non si aggiunge per comodita'** |

### **IL COLLAUDO: `12`/`12`, su una cartella di PROVA in una COPIA**

### ⭐ **E tre bracci provano che con la cartella VUOTA il presidio TACE.** ### **Un presidio che tace va provato che taccia**, altrimenti nessuno sa se tace perche' e' ### **spento** o perche' e' ### **rotto.**

---

## ④ `H-ID-OBBLIGATORIO`: **il rovescio di `H-INDICE`**

| | |
|---|---|
| la regola | un commit che tocca ### **un file della LISTA** o un ### **`doc/REFERTO_*` / `doc/REPERTO_*`** ### **cita almeno un ID** dell'indice |
| ### ⭐ **era MEZZO controllo** | `H-INDICE` verifica che gli ID citati ### **esistano**; che ### **ce ne sia almeno UNO** ### **non lo chiedeva nessuno** — la stessa forma di difetto di `F12` |
| ### ⛔ **e «un referto» e' SOLO due prefissi** | la ### **correzione `C`** della coda: *«non qualunque file sotto `doc/`»*. ### **La mia definizione era LARGA**, e una definizione larga in un presidio ### **rifiuta commit che nessuno voleva rifiutare** |
| il collaudo | ### **`11`/`11`, nei due versi** — e un braccio prova che `doc/STATO_RUN.md`, `doc/REGOLE/par9.md` e `doc/indice/voci.jsonl` ### **NON contano** |
| ### ⚠ **la via d'uscita e' la STESSA di `H-INDICE`** | `[SENZA-INDICE: <motivo>]`, a inizio riga: dichiararla ### **spegne entrambi** per quel commit. E' una scelta, e la dichiaro: ### **chi non ha ID da citare non ha nemmeno ID da verificare** |

---

## ⑤ LE TRE CORREZIONI DELLA CODA, E DOVE SONO FINITE

| | la correzione | dove |
|---|---|---|
| `A` | `migrazione_era1.jsonl` ### **NON contiene i valori dei campi**; le voci senza storico ### **coincidono col loro stato a `3ef2326`** | ### **dentro `F11`**: la costante si chiama `FINE_MIGRAZIONE`, e ### **non ho mai letto `migrazione_era1.jsonl` per i valori** |
| `B` | la cartella dell'era `2` ### **NON ESISTE e NON la scegli tu** | ### **`CARTELLA_ERA_2 = ""`**, e ### **la domanda e' in testa a questo referto** |
| `C` | *«un referto sotto `doc/`»* = ### **SOLO `doc/REFERTO_*` e `doc/REPERTO_*`** | ### **dentro `H-ID-OBBLIGATORIO`** *(`REFERTI`)*, col ### **braccio negativo** che prova che gli altri file di `doc/` non contano |

### ✔ **E LA VOCE ① DELLA CODA SI CHIUDE QUI.** Era arrivata ### **senza il suo mandato base**, e il mandato di oggi ### **l'ha assorbita.** ### ⭐ **Si chiude quando il lavoro e' fatto, non quando e' letto.**

---

## ⑥ CHE COSA RESTA A LUCA

| | che cosa |
|---|---|
| ### 📌 **IL NOME DELLA CARTELLA DELL'ERA `2`** | finche' manca, `H-FISICA-FUORI-LISTA` ### **e' una tenda.** Una stringa in `csv/_file_fisica.py`, e poi ### **va ricollaudato sull'albero vero**: il collaudo di oggi gira su una copia |
| ### **se `T0` e `T4` sono troppo larghi** | sono ### **due livelli di ricerca che ho aggiunto io**, e il mandato ne nominava tre |
| ### **`F11` non vede una manomissione che tocchi ANCHE lo storico** | la difesa contro quello ### **e' git, non `F11`** |
| ### **il campo `aggiornata` e' fuori dal confronto di `F11`** | prezzo dichiarato |
| ### **i `14` presidi del §`12`** | sono ### **due in piu-** di stamattina, e ### **uno dei due non impedisce niente** |

> ### ⭐ **E la cosa che porto fuori da questo giro:** ### **`F12` e `H-ID-OBBLIGATORIO` erano MEZZI CONTROLLI** — l'uno chiedeva *«se e' `CHIUSA`, dove sta la chiusura?»* e non *«se c'e- la chiusura, e' `CHIUSA`?»*; l'altro *«gli ID citati esistono?»* e non *«ce n'e- almeno uno?»*. ### **Una sola delle due direzioni non e' un controllo: e' MEZZO controllo** — e la meta' che manca ### **non si vede, perche' tace.**

