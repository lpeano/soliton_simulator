# INDICE `v3`: **le chiusure, le superate, la terza lettura** — e **gli strumenti per l'era `2`**

> **Mandato di Luca del 2026-10-09**, nove punti in ### **due parti**. Nessuna corsa,
> simulatore `b8c21049` intatto.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.
>
> ### 📌 **E QUESTO MANDATO CHIUDE LA CODA:** *«Questo mandato CONTIENE anche il mandato
> base «INDICE E FISICA» che non ti era arrivato: la voce ① di `doc/CODA_2026-10-09.md` e'
> assorbita qui (parte II) e si chiude.»* ### **La parte II E' il mandato che mancava**, e
> le tre correzioni `A`/`B`/`C` della coda ### **sono dentro i punti `6`, `7` e `8`.**

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **LA FRASE CHE GOVERNA LA PARTE I: «IL COMMIT DI CHIUSURA SI RICAVA, NON SI INVENTA»**

Nel giro scorso ho lasciato ### **`47` chiusure non fatte** scrivendo *«un commit non si
inventa»*. ### ⛔ **Era vero a metà.** Non inventarlo era giusto; ### **fermarsi lì era una
rinuncia**: il commit che ha chiuso una voce ### **è scritto nella storia di git**, e
`git log -S'<frase>' --reverse` ### **lo trova.** ### ⭐ **«Non si inventa» non vuol dire
«non si cerca»** — e questa è la correzione che Luca mi fa, e la accetto.

### **COSA CREDO, PUNTO PER PUNTO**

| | cosa credo PRIMA di guardare |
|---|---|
| `1` **il commit si ricava** | ci credo, ed è ### **meglio di quello che facevo:** cercavo uno sha ### **dentro la riga**, e la riga ### **non ha motivo di portarlo.** ### ⚠ **Credo che `git log -S` falliscà su molte frasi**, perché la citazione è ### **normalizzata** *(senza markdown, accenti piegati)* e `-S` cerca ### **i byte**. ### ➜ **Serve la frase COME È NEL FILE**, non come è nel file del guardiano |
| `2` **`F12`** | `chiusura` non vuota ⇒ `CHIUSA`. ### **Credo che le `42` vengano dalla migrazione**, non dal mio lavoro: ### **non so da dove**, ed è la prima cosa da misurare |
| `3` **lo schema** | `superata_da` accetta ### **anche una voce**: ci credo, e ### **chiude il rifiuto di `S02`** del giro scorso. ### ⭐ **E `F9` che ammette `SUPERATA` per `ENTRAMBE` corregge una MIA strettezza:** avevo scritto *«`ENTRAMBE` ⇒ `APERTA` o `CHIUSA`»* ### **alla lettera del mandato**, e una voce `ENTRAMBE` ### **può essere superata da una decisione** |
| `4` **la nota di `G1`** | si ### **toglie**, e il mandato risponde alla domanda che avevo messo nel referto. `CLI-1` e `POTATURA-GUARDIE`: ### **vale il file**, e ### **lo conferma il guardiano** — quindi la mia riconciliazione ### **non è più «mia nella forma»: è confermata** |
| `5` **la terza lettura** | `59` righe. ### ⚠ **E DUE CORREZIONI DEL GUARDIANO A SÉ STESSO**, che cambiano il senso di quello che avevo scritto: la classe `(B)` del censimento è ### **«COSTRUITA E MAI MISURATA»**, non testo falso; e `REGISTRO_FISICA:P*` sono ### **PREVISIONI**, non esiti — quindi ### **`CRITERIO`/`METODO`, non `MISURA`/`FISICA`** |
| `6` **`F11`** | è ### **il presidio più forte di tutti:** dice che l'indice ### **è il replay del suo storico.** ### ⛔ **Non so se passa oggi**, e il mandato dice *«acceso nello STESSO commit in cui passa»*: se non passa, ### **prima si cura ciò che non torna** |
| `7` **la lista e la cartella** | ci credo, ed è la correzione `B` della coda: ### **la cartella NON la scelgo io.** ### ⚠ **Non so quanti presidi nominano `soliton_simulator.py` a mano** — è un censimento da fare ### **prima** di dire un numero |
| `8` **l'ID nel messaggio** | ### **`H-INDICE` esiste già** e controlla gli ID citati; questo è ### **il rovescio**: pretende che ### **ce ne sia almeno uno.** ### ⭐ **E la correzione `C` della coda lo restringe:** *«un referto sotto `doc/`»* è ### **solo `doc/REFERTO_*` e `doc/REPERTO_*`** |

### **COSA NON SO** *(e lo scrivo perché due giri fa una soglia scritta male mi ha quasi fatto fermare per il numero sbagliato)*

1. ### **quante delle `47` frasi `git log -S` trova davvero**, e quante cadono sul tag;
2. ### **da dove vengono le `42` `chiusura` senza `CHIUSA`** — se le ho scritte io, è un mio
   difetto da dichiarare;
3. ### **se `F11` passa oggi.** Se non passa, ### **quante voci non tornano e perché**;
4. ### **quanti punti del codice nominano `soliton_simulator.py`** invece di una lista;
5. ### **se il presidio del punto `8` blocca i miei stessi commit** — i miei citano ID, ma
   ### **va provato, non supposto.**

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, e cosa mi FERMA*

### ⛔ **L'ORDINE NON È LIBERO, E STAVOLTA LO SO PRIMA**

| | il vincolo |
|---|---|
| `1` **prima** di `2` | `F12` pretende `chiusura` ⇒ `CHIUSA`: se le `47` non sono chiuse, ### **`F12` non si può accendere** |
| `3` **prima** di `S02`/`Z21` | lo schema le ### **rifiuta** finché `superata_da` non accetta una voce |
| `2` e `6` **con** la loro cura | ### **stessa lezione, terza e quarta volta:** `indice.py valida` gira nel `pre-commit`, e un presidio bloccante con violazioni in piedi ### **blocca ogni commit del repo** |
| `8` **dopo** `7` | il presidio del punto `8` ### **legge la LISTA** del punto `7` |

| passo | cosa decide | cosa mi FERMA |
|---|---|---|
| `A` | ### **il punto `1`:** il commit di chiusura si ricava. Decide ### **quante delle `47` si chiudono con un commit VERO** e quante col tag | ### ⛔ **se la frase non si trova nel FILE** *(non nel file del guardiano)*: allora non ho cercato la cosa giusta, e mi fermo a capire |
| `B` | ### **il punto `2`:** le `42`. Decide ### **due liste** — la riga chiude *(→ `CHIUSA`)* o non chiude *(→ `chiusura` si svuota)* | ### ⛔ **se `F12` non passa dopo la cura**, non lo accendo e lo dico |
| `C` | ### **il punto `3`:** lo schema, il validatore, il collaudo ### **nei due versi**, poi `S02` e `Z21` | ### ⛔ **se il collaudo negativo NON scatta**, la regola nuova ### **non è una regola: è un permesso** |
| `D` | ### **il punto `4`:** la nota di `G1` via `meta_togli`, e `C3` si allinea al file | — |
| `E` | ### **il punto `5`:** il file `_b.txt`, ### **committato da solo**, poi applicato con la regola del mandato precedente | ### ⛔ **se le righe non sono `59`**, non è il file che Luca ha mandato |
| `F` | ### **il punto `6`:** `F11`, e il collaudo che il mandato detta *(`A2-ANELLO` a mano + viste rigenerate ⇒ ### **DEVE fallire**)* | ### ⛔ **se `F11` non passa sull'indice vero**: ### **si cura ciò che non torna PRIMA**, e se non si può ### **si dice** |
| `G` | ### **il punto `7`:** `csv/_file_fisica.py`, il censimento dei punti che nominano il simulatore, il presidio sulla cartella ### **collaudato su una COPIA** | ### ⛔ **la CARTELLA resta VUOTA.** Se mi trovo a scegliere un nome, ### **mi fermo:** il mandato dice *«NON la scegli tu»* |
| `H` | ### **il punto `8`:** il presidio del messaggio, ### **collaudato nei due versi** | ### ⛔ **se blocca un commit legittimo** nel collaudo, la regola è troppo larga |
| `I` | ### **il punto `9`:** i due referti | — |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura, fissata adesso |
|---|---|
| il commit di chiusura | `git log -S'<frase>' --reverse -- <file>`, ### **il PRIMO.** La frase è ### **quella che sta nel file**, ritrovata dalla citazione; se la citazione non si ritrova nel file, ### **si usa il tag** e il criterio ### **dice quale dei due** |
| `F12` | `chiusura.criterio` **o** `chiusura.commit` non vuoti ⇒ `stato == CHIUSA`. ### **Vuoto = `{}`** |
| `F9` + `SUPERATA` | era `ENTRAMBE` ⇒ `APERTA`, `CHIUSA` ### **o `SUPERATA`**; era `2` ⇒ `AGENDA` |
| `F11` | per ogni voce: ### **i campi dello schema** *(non `aggiornata`, che è un timestamp)* coincidono col `dopo` dell'ultima riga di storico. Senza storico: col proprio stato a ### **`3ef2326`**. Nata dopo `3ef2326` senza storico: ### **errore** |
| la LISTA e la CARTELLA | due costanti in `csv/_file_fisica.py`. ### **La CARTELLA è `""`**, e il presidio su di essa ### **non guarda niente finché è vuota** — e questo ### **va DICHIARATO**, perché un presidio che non guarda niente ### **non è un presidio** *(`A9`)* |
| il punto `8` | *«un referto»* = ### **`doc/REFERTO_*` o `doc/REPERTO_*`**, e basta |

### ⭐ **E UNA COSA CHE SO GIÀ DI DOVER DICHIARARE:** il presidio del punto `7` sulla cartella
### **non impedirà NIENTE finché la cartella è vuota.** ### ⛔ **Per `A9` quello non è un
presidio: è una tenda.** ### ➜ **Lo scrivo nel referto come tale**, e il collaudo gira
### **su una cartella di PROVA in una COPIA** — che è esattamente ciò che il mandato chiede,
e il motivo è questo.

---

## ③ TODO DEL NEXT STEP — *la lista operativa*

- [ ] `A` — punto `1`: `csv/_commit_di_chiusura.py`, le `47` righe, un commit
- [ ] `B` — punto `2`: le `42`, le due liste, e ### **`F12` acceso nello stesso commit**
- [ ] `C` — punto `3`: schema + validatore + collaudo nei due versi, poi `S02` e `Z21`
- [ ] `D` — punto `4`: `meta_togli` su `G1`, e `C3` allineato al file
- [ ] `E` — punto `5`: il file `_b.txt` ### **da solo**, poi le `59` righe
- [ ] `F` — punto `6`: `F11` + il collaudo su COPIA che il mandato detta
- [ ] `G` — punto `7`: `csv/_file_fisica.py`, il censimento, il presidio sulla cartella
- [ ] `H` — punto `8`: l'ID nel messaggio, collaudo nei due versi
- [ ] `I` — punto `9`: `doc/REFERTO_indice_v3_chiusure.md` e
      `doc/REFERTO_strumenti_era2.md`, ### **con la domanda sul nome della cartella**
- [ ] chiudere la voce ① di `doc/CODA_2026-10-09.md`: ### **assorbita**

### **LE CINQUE DOMANDE DI `doc/STELLA_POLARE.md`** *(`L-STELLA`)*

### **Non si applica, e il perché è parte della risposta:** nessuno dei nove punti
### **tocca la fisica.** La parte I cambia `classe`, `dominio`, `era`, `stato`, `chiusura` e
`superata_da` di voci dell'indice; la parte II aggiunge ### **presidi che guardano il repo**
— quali file sono di fisica, dove sta il codice, che cosa dice un messaggio di commit.
### ⭐ **E il punto `7` è l'unico che SFIORA la fisica, ma dal lato opposto:** non cambia una
legge, ### **dichiara dove le leggi vivono.** `soliton_simulator.py` ### **non si apre**, e
il suo blob *(`b8c21049`)* si verifica a ogni commit.
