# INDICE `v3`: **la chiusura dei `103` segnali dei presidi**

> **Mandato di Luca del 2026-10-09** *(relayed dal guardiano, che ha letto i `103` segnali uno
> per uno)*. Nessuna corsa, simulatore `b8c21049` intatto. Sei punti, **un commit per punto**.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### **LA COSA PIU' IMPORTANTE: `F1` ERA MIO, E IL GUARDIANO HA RAGIONE**

Il guardiano scrive: *«`F1` (`49`): quasi tutto rumore, ### **e la regola era mia**. Citare un
assioma non vuol dire essere gemelle»*. ### ⛔ **E' vero, e il difetto e' di FORMULAZIONE, non
di codice:** `D24` e' un difetto dell'era `1` che ### **viola `A2`**, e `A2` vale per
### **entrambe** le ere — *«differiscono»* e' ### **giusto che sia vero**, e non e' una
mescolanza. ### **Ho misurato: `42` dei `49` segnali puntano a `STANDARD`, `PRESIDIO` o
`NON_DEFINITA`**, quindi la restrizione del punto `1` ne lascia ### **`7`**.

### ⚠ **E io avevo scritto nel referto dei presidi che `12` dei `49` erano verso segnaposto, e
### l'ho presentato come «da decidere»:** era ### **la metà del problema vista per un quarto.**
Non avevo guardato che gli altri `30` puntavano ad ### **assiomi e presidi**, cioe' a cose che
### **per definizione valgono per entrambe le ere.** ### **Il guardiano l'ha visto leggendo, io
no, e lo scrivo.**

### **CHE COSA CREDO, E PUO' RIVELARSI FALSO**

**`a` Il punto `2` e' il lavoro vero.** `71` voci `CRITERIO`/`FISICA` → `METODO`, e il mandato
chiede di separare ### **le eccezioni: le voci il cui testo NON e' un criterio ma un ESITO
MISURATO** → classe `MISURA`, dominio `FISICA`. ### **Previsione: fra `3` e `12` esiti**
*(`REGISTRO_FISICA:P5` e' l'esempio dato; credo che il grosso di `REGISTRO_FISICA:*` siano
criteri veri)*.

**`b` `F4`: la regola dell'intestazione.** Ho guardato le `30` righe segnalate e credo che
### **la distinzione sia GRAMMATICALE, non semantica:** nelle vere *(`## APERTO CURA1-CORTO`)*
### **l'ID e' il SOGGETTO dell'intestazione**; nelle false *(`### 1.2 ⚠ E LA LETTURA CHE DECIDE
DAVVERO — dichiarata POST-HOC, non era fissata prima`)* ### **l'ID e' dentro la prosa**, usato
come aggettivo o come verbo *(`RI-LETTO`, `RI-VERIFICATI`, `SOVRA-CORREGGE`)*.

**`c` `TEMPO-LUCE` e `MASSE-COERENTI` NON si ripristinano dall'intestazione che `F4` ha
segnalato.** Entrambe sono segnalate da un'intestazione in cui l'ID sta ### **dentro la prosa**
*(`# RAMPA-2 — CHI USA IL TEMPO-LUCE O cs…`, `### ⚠ E il limite va detto: e' la scena
MASSE-COERENTI a 3 masse`)*. ### **Se sono davvero da ripristinare, la definizione sta ALTROVE**
— e il mandato lo dice: *«cerca ### **TUTTE** le sue definizioni nel repo»*. ### ⛔ **E qui c'e'
un difetto di `F4` che dichiaro adesso: `F4` SI FERMA AL PRIMO FILE** *(`break`)*, quindi
### **non ha mai cercato tutte le definizioni.** Il punto `5` ha bisogno di un attrezzo
### **diverso da `F4`**, che spazzi ### **tutto il repo**.

### ⛔ **CHE COSA NON SO, E NON INVENTO**

1. **Se gli ID corti siano omonimi o no.** Il guardiano scrive *«`S1`, `S3`, `T1`, `H1`–`H3`,
   `D3`, `D4`, `F4`, `F5` hanno ### **quasi certamente** piu' significati»*. ### **«Quasi
   certamente» non e' una misura:** li cerco, e ### **decido dal numero di definizioni
   trovate**, non dall'aspettativa.
2. **Quante voci `CRITERIO`/`FISICA` siano esiti.** Non lo so, e ### **non lo decido per
   percentuale:** leggo le `71`, e ### **ciascuna che tratto come esito va nel referto CON LA
   SUA FRASE**, come il mandato chiede.
3. **Se `F1` ristretto lasci ancora rumore.** `7` segnali e' poco, ma ### **non li ho letti.**
4. **Se la regola dell'intestazione tagli anche qualcosa di vero.** ### **Il collaudo lo dice
   solo per `POST-HOC` e `TW-1`**, che sono i due casi che il mandato fissa.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### **LE DUE REGOLE NUOVE, FISSATE QUI PRIMA DI APPLICARLE**

> ### ① **`F4`: QUANDO UN'INTESTAZIONE DEFINISCE**
>
> Si toglie dall'inizio della riga, **ripetutamente**: i `#`, gli spazi, i **simboli non
> alfanumerici** *(`⛔` `✅` `⚠` `⭐` `➜` `①` `*` backtick `—` `§`)*, la **numerazione**
> *(`5.`, `1.2`, `5-bis.`, `§38`)* e **una parola di stato** *(`APERTO`, `CHIUSO`, `APERTA`,
> `CHIUSA`, `RISOLTO`, `SOSPESO`)*.
> ### ✔ **E' una DEFINIZIONE se il resto COMINCIA con l'ID** *(come token)* ### **e dopo l'ID
> restano almeno `3` caratteri non bianchi** — *«senza contenuto»* significa **niente dopo
> l'ID**.
> ### ⛔ **Le RIGHE DI TABELLA non cambiano:** `| `ID` | …` resta una definizione, ed e' per
> questo che `TW-1` deve continuare a scattare.

> ### ② **PUNTO `2`: QUANDO UN TESTO E' UN ESITO E NON UN CRITERIO**
>
> ### **Un CRITERIO prescrive**, e si riconosce dai verbi e dalle formule del giudizio:
> *«DEVE»*, *«si verifica»*, *«basta»*, *«serve»*, *«byte-identico»*, *«controllo positivo»*,
> *«caso che deve fallire»*, una **soglia** *(`>`, `<`, `>=`)*.
> ### **Un ESITO riporta una misura**: un numero o un intervallo **come risultato**
> *(`0.74-0.76`, `=`, `%`)*, ### **e nessun verbo prescrittivo.**
> ### ⚠ **La regola SELEZIONA i candidati; la decisione la prendo LEGGENDO**, e ### **ogni
> voce trattata come esito va nel referto CON LA FRASE** — il mandato lo chiede, e senza la
> frase la decisione **non e' verificabile**.

### **I PASSI**

| | il passo | che cosa DECIDE |
|---|---|---|
| `1` | `F1` ignora le voci citate `STANDARD`, `PRESIDIO`, `NON_DEFINITA`; `C5` diventa omonimo; `Z100` e `C5-INVARIANTI` chiudono con eccezione | ### **da `49` a `7`**, e i `7` si leggono |
| `2` | le `71` `CRITERIO`/`FISICA` → `METODO`; gli **esiti** → `MISURA`/`FISICA` | ### **la mescolanza piu' grossa che resta**, e la classe `CRITERIO` torna **una cosa sola** |
| `3` | gli `8` segnali di `F2` → eccezione **che cita la frase del «sostituisce»**; `ENERGIA-NON-DEFINITA` → ### **solo la nota**, NON si tocca | niente: registra una **domanda a Luca** |
| `4` | `F3`: le cure chiuse col sigillo → eccezione; gli altri **si leggono** | difetto **della LEGGE** ⇒ resta `FISICA`; **del testo o dello strumento** ⇒ si sposta |
| `5` | un attrezzo nuovo cerca **TUTTE** le definizioni **in tutto il repo**; `F4` prende la regola ① | ripristina · omonimo · resta etichetta |
| `6` | controlli + referto `doc/REFERTO_indice_v3_segnali.md` | — |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura |
|---|---|
| `F1` dopo il punto `1` | ### **`7` segnali**, cioe' `49 - 42`. ### **Se ne restano piu' di `10`, la mia misura dei `42` era sbagliata** |
| il collaudo di `F1` | `B2`/`Z31` ### **deve ancora scattare.** Se non scatta, la restrizione ha tagliato troppo ⇒ ### **FERMO** |
| il punto `2` | gli **esiti** fra `3` e `12`. ### **Se sono piu' di `20`, non e' un'eccezione: e' un'altra regola**, e lo scrivo invece di applicarla |
| `F3` dopo il punto `2` | ### **`10` segnali** *(`15` meno le `5` `CRITERIO`: `COMPONENTI:B1`, `COMPONENTI:B10`, `REGISTRO_FISICA:A6`, `REGISTRO_FISICA:C2`, `REGISTRO_FISICA:V6`)*, di cui `4` chiudono con eccezione e ### **`6` si leggono** |
| il collaudo di `F4` | ### **`POST-HOC` NON deve scattare**, ### **`TW-1` a `6e5e75b` DEVE.** Meno di `2` su `2` ⇒ **FERMO** |
| il collaudo intero | ### **almeno `17` su `17`** *(i `15` di oggi piu' i `2` nuovi)*. Meno ⇒ **FERMO** |

### ⛔ **CHE COSA MI FA FERMARE**

1. **`B2`/`Z31` non scatta piu'** dopo la restrizione di `F1` ⇒ ho tagliato ### **il caso
   vero** insieme al rumore.
2. **`POST-HOC` scatta ancora** o **`TW-1` non scatta** ⇒ la regola ① e' sbagliata.
3. **Gli esiti del punto `2` sono piu' di `20`** ⇒ non e' un'eccezione, e' una regola che Luca
   non ha scritto: ### **lo dico, non la applico.**
4. **Una voce del punto `4` non la so leggere** ⇒ ### **la lascio dov'e' e lo scrivo**, invece
   di spostarla per riempire la casella.
5. **Il punto `5` trova un ID definito in un solo posto ma SENZA contenuto** ⇒ non e' nessuno
   dei tre casi del mandato ⇒ ### **lo elenco a parte**, non lo infilo nel caso che somiglia
   di piu'.

### **`L-STELLA`: le cinque domande di `doc/STELLA_POLARE.md`**

### ⛔ **NON SI APPLICA, e il perche' e' parte della risposta:** nessuna legge cambia, il
simulatore non si tocca *(`b8c21049`)*, niente gira. Si spostano voci fra classi e domini
### **dell'indice dei difetti**, e si stringono due rilevatori. ### **Le cinque domande
chiedono di un gradino di robustezza fisica, di numeri o leggi aggiunti, del verso
EM-curvatura e di emergente-contro-imposto: su un cambiamento che non entra nel simulatore NON
HANNO UN SOGGETTO.**

### ⚠ **E una cosa che il punto `2` cambia e che va detta:** `71` voci passano da `FISICA` a
`METODO`. ### **Non e' una decisione di fisica** — il guardiano lo dichiara: *«e' un mio
criterio di classificazione»* — e ### **tutte restano SOSPESE o CHIUSE**, quindi
### **non cambia nulla per l'era `2`, solo l'ordine.** ### **Ma `FISICA` perde `71` voci su
`439`, cioe' un sesto**, e chi legge i conteggi di ieri e di domani deve trovare scritto
perche'.

---

## ③ TODO DEL NEXT STEP — *operativo*

- [ ] **`1`** `F1`: la restrizione + il collaudo rifatto. `C5` → `meta.omonimo`; `Z100` e
      `C5-INVARIANTI` → `eccezione_presidio`. **Elenca i `7` che restano.**
- [ ] **`2`** le `71` `CRITERIO`/`FISICA` → `METODO`; gli **esiti** → `MISURA`/`FISICA`,
      ### **con la frase, nel referto.**
- [ ] **`3`** gli `8` di `F2` → eccezione **che cita il «sostituisce»**;
      `ENERGIA-NON-DEFINITA` → ### **solo la nota.**
- [ ] **`4`** `F3`: `POTENZE-1`, `RAMPA-1`, `Z124`, `G3` → eccezione; gli altri `6`
      ### **letti per intero.**
- [ ] **`5`** l'attrezzo che cerca **TUTTE** le definizioni; `F4` con la regola ①;
      collaudo su `POST-HOC` e `TW-1`.
- [ ] **`6`** controlli + `doc/REFERTO_indice_v3_segnali.md`, voce per voce.
- [ ] **par.6** a ogni commit: **inventario** *(gli attrezzi nuovi, col blob)* e
      **par9/schema** *(la regola ① e quella della classe `CRITERIO`)*.
      ### **FISICA: non si applica.**
- [ ] **`storico-commit`** dopo ogni commit, perche' `F5` lo pretende al commit dopo.
