# I FILE NON TRACCIATI — **le decisioni di Luca del 2026-10-04, e un controllo che BLOCCA**

*(registrate **PRIMA del lavoro**, par.8. **Niente si cancella dal disco:** nessun
`git clean`, nessun `rm`.)*

## 1. LE DECISIONI, come sono arrivate

| | |
|---|---|
| **`.gitignore`** | `*.pkl.gz`, `*.pickle`; `csv/**/_tmp/`; `csv/**/_sim_*.py`, `_br_*.py`, `_driver_*.py` **con l'eccezione `!`** per le copie committate accanto a un referto *(par.7, stato 2)*; i **nomi GENERICI** delle uscite dei run; i `39` fotogrammi di `_video_g6000` |
| **i 2 `.pkl.gz`** | `git rm --cached`, **restano sul disco**, e nella voce d'inventario vanno percorso, sha1 e comando che li rigenera. ### **La storia non si riscrive** |
| **i 24 `CONFIGURAZIONE`** | si **committano**: altri `15` dello stesso tipo sono gia' tracciati, e descrivono **come sono stati prodotti i dati** *(par.6)* |
| **i 98 citati e non tracciati** | si committano quelli di **testo**; sopra `5 MB` o binari **no**, si elencano e si propone se togliere la citazione o sostituirla col comando |
| **i 15 non citati** | se sono l'uscita di uno strumento committato: si committano **e si aggiunge la citazione** nell'inventario; altrimenti in `.gitignore` **col perche'** |
| **`H-NON-TRACCIATI`** | un hook che **BLOCCA**, con `[SENZA-NON-TRACCIATI: <motivo>]` a inizio riga |
| **la verifica** | il censimento rigirato: la classe `(d)` **vuota**, o solo file elencati col loro motivo |

## 2. DUE CORREZIONI, e una mi riguarda

### ⛔ **ERRORE DEL GUARDIANO, che lui dichiara:** aveva detto a Luca *«27 `.pkl` gia'
committati»*. ### **E' FALSO:** la sua ricerca contava altri file. ### **I binari tracciati
sono DUE `.pkl.gz`**, come il mio censimento — e il referto `0b3b2a0` li nomina per percorso
e per commit *(`4df94a7`)*.

### ⚠ **E UN DISACCORDO COL MIO REFERTO, accolto da Luca, che ha ragione.** Io avevo messo in
evidenza i **57 non citati** come *«il numero che conta»*. ### **Non lo e'. Il numero che
conta sono i 98 CITATI MA NON TRACCIATI.**

> Un file **non citato e non tracciato** e' **rumore**: nessuno lo cerca.
> Un file **CITATO e non tracciato** e' **un riferimento al vuoto**: un documento, un referto
> o l'inventario lo nominano, e ### **chi verifica dal repo va a cercarlo e non lo trova.**
> ### **E' esattamente il caso `_sonda_scherm`** — il referto committato e lo strumento no.

### 📌 **PERCHE' AVEVO GUARDATO DALLA PARTE SBAGLIATA:** avevo cercato *«che cosa ho
dimenticato di committare?»*, che e' una domanda sul **disco**. La domanda giusta e'
*«che cosa promette il repo e non mantiene?»*, che e' una domanda sulle **citazioni**.
### **Il mio censimento calcolava il numero giusto e io ho messo in rilievo l'altro.**

## 3. IL CONTROLLO DEL `COMMIT 1` FALLISCE: **67 file TRACCIATI** sarebbero coperti

Il mandato dice: *«su ogni file TRACCIATO: nessun file tracciato deve risultare coperto da
una regola nuova senza l'eccezione. Se succede, FERMATI.»* ### **Succede.**

| regola proposta | file **TRACCIATI** coperti |
|---|--:|
| `*.pkl.gz` | **2** |
| `*.pickle` | 0 |
| `csv/**/_tmp/*` | **12** *(6 `_br_*.py` + 6 `s11/s12.json`)* |
| `csv/**/_sim_*.py` | **12** |
| `csv/**/_br_*.py` | 6 *(gia' contati, stanno sotto `_tmp/`)* |
| `csv/**/_driver_*.py` | **1** |
| ### **`csv/**/_corsa.txt`** | ### **31** |
| `csv/**/_sigillo.json` | **1** |
| `csv/**/_censimento.json` | **2** |
| `csv/_test_fork/_video_g6000/*.png` | **6** |
| **in tutto, distinti** | ### **67** |

### ⛔ **E IL CASO DECISIVO SONO I 31 `_corsa.txt`: il nome generico E' la convenzione
committata.** Trentuno referti di sigilli e di sonde stanno in git **con quel nome**.
### **Ignorarlo non li toglierebbe da git** *(`.gitignore` non de-traccia niente)*, ma
produrrebbe due cose:

1. una lista di **`!` che oggi ha 67 righe** e che ### **cresce a ogni sigillo nuovo**;
2. ### **un referto scritto nel posto giusto diventerebbe INVISIBILE** se qualcuno dimentica
   la sua riga `!`.

> ### 📌 **E IL SECONDO EFFETTO E' L'OPPOSTO DELLO SCOPO.** La decisione nasce per far
> significare *<<non tracciato>>* = *<<dimenticato>>*. ### **Una regola che rende invisibile
> un referto scritto correttamente fa significare *<<non tracciato>>* = *<<coperto da una
> riga che nessuno ha aggiunto>>*** — cioe' nasconde proprio la classe che si voleva
> illuminare.

### **UN VINCOLO TECNICO, misurato e non supposto:** `csv/**/_tmp/` **con la barra finale
esclude la CARTELLA**, e git ### **non puo' ri-includere un file se una cartella genitore e'
esclusa**. Quindi le `12` eccezioni sotto `_tmp/` ### **non funzionerebbero.** Serve
`csv/**/_tmp/*` *(che esclude le VOCI, non la cartella)*, e questo va verificato con
`git check-ignore`, non assunto.

### **E UN'OSSERVAZIONE SULL'ORDINE, utile:** `*.pkl.gz` ha `2` conflitti, e sono
### **esattamente i due file che il `COMMIT 2` toglie dall'indice.** ### **Facendo il
`COMMIT 2` PRIMA del `COMMIT 1`, quel conflitto si azzera da se'** — senza nessuna eccezione
da scrivere.

## 4. LE DUE STRADE, e la scelta e' di Luca

| | come |
|---|---|
| **(A)** come scritto nel mandato | `67` righe `!`, da mantenere a mano a ogni sigillo nuovo |
| ### **(B)** | ### **non ignorare i nomi generici**, e lasciare che `H-NON-TRACCIATI` *(il `COMMIT 6`)* li faccia **committare**. ### **Trentuno referti dimostrano che la convenzione e' COMMITTARLI**, e il presidio li renderebbe impossibili da dimenticare |

### ⚠ **La `(B)` NON e' un'obiezione alla decisione: e' la stessa decisione ottenuta con il
presidio invece che con l'ignore.** ### **Lo scopo — *non tracciato = dimenticato* — la `(B)`
lo raggiunge committando, la `(A)` ignorando.** ### ⛔ **Non scelgo io** *(`L-DOPO-STOP`)*.

### ✅ **CIO' CHE SI PUO' FARE SENZA DECIDERE NIENTE**, se Luca vuole andare avanti subito:
i `COMMIT 2`, `3`, `4`, `5`, `6` e `7` ### **non dipendono** dalla regola dei nomi generici.
Il solo pezzo bloccato e' la parte del `COMMIT 1` che riguarda ### **`_corsa.txt`,
`_sigillo.json`, `_censimento.json` e i `.png`.**

---

## **ANNOTAZIONE del 2026-10-04 — LUCA SCEGLIE LA (B), e il guardiano dichiara il suo errore**

### **DECISIONE DI LUCA: strada `(B)`.** I nomi generici dei referti **NON si ignorano**: si
**committano**, come vuole la convenzione storica — **i `31` `_corsa.txt` tracciati.**

### ⛔ **ERRORE DEL GUARDIANO, che lui dichiara, ed e' istruttivo PERCHE' E' LA SUA PROPRIA
REGOLA:** il mandato diceva di ignorare i nomi generici, **generalizzando dagli ultimi due
giorni** *(in cui avevo introdotto io la convenzione dei nomi propri)* ### **senza censire il
repo** — che e' esattamente cio' che `P1` chiede a me: *«non usare l'associazione senza
verificare lo storico»*.

> ### 📌 **E LA FORMA DELL'ERRORE E' LA PIU' COMUNE DI TUTTE: prendere le ultime due
> osservazioni per la regola.** ### **Trentuno referti dicevano il contrario, ed erano in
> git.** ### ⚠ **Il mio blocco e' stato giusto NON perche' avessi un'intuizione, ma perche' il
> mandato stesso prescriveva un controllo — *«nessun file tracciato coperto senza
> eccezione»* — e il controllo ha contato `67`.** ### **Il merito e' del controllo, non mio:
> senza quel conto avrei applicato la regola e scoperto il danno dopo.**

### **L'ORDINE NUOVO, come Luca l'ha fissato**

| | |
|---|---|
| **`COMMIT 2` PRIMA del `COMMIT 1`** | come avevo proposto: `git rm --cached` dei due `.pkl.gz`, ### **cosi' il conflitto di `*.pkl.gz` si azzera da se'** |
| **`COMMIT 1` RIDOTTO** | `*.pkl.gz`, `*.pickle`; `csv/**/_tmp/*` *(con l'asterisco, **verificato con `git check-ignore`**)*; le copie del simulatore e le copie **patchate** con le eccezioni `!` ### **solo per quelle gia' tracciate accanto a un referto**; i `39` `.png` del video. ### **NIENTE regole sui nomi generici** |
| **`COMMIT 4`** | i referti con nome generico **citati e non tracciati** ### **SI COMMITTANO** |
| **`COMMIT 6`** | durante un run il referto **in scrittura** si dichiara con la via d'uscita, e ### **si committa a run chiuso** |

### **E IL CONTROLLO RESTA:** nessun file tracciato coperto senza eccezione, ### **altrimenti
si FERMA.**

### **IN CODA, NON ORA** *(registrato come `INVENTARIO-SIGILLI-SENZA-COMMIT`)*: le **79** voci
d'inventario di sigillo senza il commit con cui rigirarle, la **riga duplicata** di
`_h_etc_1.py`, e le **3** voci `.json` piu' le **4** patch elencate fra i sigilli.
### **La cura e' un lavoro a parte.**
