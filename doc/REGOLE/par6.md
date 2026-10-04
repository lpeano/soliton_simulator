# dettaglio di `CLAUDE.md` par.6 — **inventario, README, fisica**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col
loro numero. Non rimanda ad altri file di `doc/REGOLE/`.)*

## ① L'INVENTARIO: le quattro cose, e perche' quattro

Ogni file nuovo o modificato in `csv/_test_fork/` e `csv/_seal_fork/` aggiorna la sua voce in
`doc/INVENTARIO_strumenti.md` con: il **file**, il **COMANDO che lo rigira verbatim**, **cosa
misura**, il **BLOB** su cui e' girato l'ultima volta.

### ⚠ **IL BLOB E' LO `sha1` DEI BYTE GREZZI, NON `git hash-object`.** Sono **due convenzioni
diverse** che danno **numeri diversi per lo stesso file**: l'`oid` di git e' lo `sha1` di
`blob <len>\0 + contenuto`, e **non si puo' confrontare con un file sul disco**.
### **Il censimento dei non tracciati ci e' inciampato:** senza ri-hashare le `206` versioni
storiche del simulatore, la classe *«copia rigenerabile»* sarebbe stata **vuota** — un
`FALSO-ZERO` prodotto dal confondere i due hash.

### **IL TRIAGE**

| | |
|---|---|
| un **SIGILLO** | la voce **completa** |
| una **SONDA usa-e-getta** | una riga che dice **dove sta il referto** |
| una sonda **senza referto** | e' **un reperto**, non un'omissione |
| un sigillo **non piu' ri-girabile AL SUO COMMIT** | e' **un difetto nuovo** |

## «AL SUO COMMIT» — perche' non e' una sfumatura

*(decisione di Luca, 2026-10-04.)* **Un sigillo si rigira con `git checkout` del commit che ha
sigillato**, e l'inventario ne registra **il commit e il blob**.
### **`72` sigilli su `79` leggono il simulatore DAL DISCO**, quindi senza questa precisazione
**ogni cura trasformerebbe TUTTI i sigilli precedenti in difetti.**

### ⛔ **E LA MIA CONCLUSIONE SBAGLIATA LO HA DIMOSTRATO:** avevo scritto che il sigillo di
`CURA 5` diventava *«un difetto nuovo»* per effetto del commit `6b`. ### **Con la frase
incompleta era una lettura difendibile — ed e' per questo che la frase e' cambiata.**

### ⚠ **E' una REGOLA SCRITTA, non un presidio** *(`A9`)*: nessun hook verifica che una voce
di sigillo porti il suo commit. ### **E il controllo fatto il 2026-10-04 dice quanto pesa:
`79` voci su `82` sotto `csv/_seal_fork/` NON hanno un commit con cui rigirarle, e il blob
c'e' sempre.** ### **La regola nasce vera e per il `96 %` non applicata** — il debito e'
registrato come `INVENTARIO-SIGILLI-SENZA-COMMIT`.

## I `.pkl`, e il `.pkl.gz` che la regola non copriva

I `.pkl` **non si committano** *(binari, ~18 MB)*, ma il sistema e' **deterministico** e **il
dato E' il comando che lo produce** — nome, riga di comando completa, blob del simulatore,
blob dello script, seme, passi, data.

### ⛔ **E LA REGOLA ERA INCOMPLETA, in silenzio:** `.gitignore` aveva `*.pkl` ma **non**
`*.pkl.gz`, e un pattern combacia col **nome intero** — `x.pkl.gz` finisce in `.gz`.
### **Risultato: DUE `.pkl.gz` erano committati** *(dal commit `4df94a7`)*, cioe' la decisione
era **gia' stata violata due volte** dalla forma compressa. ### ✅ **Tolti dall'indice il
2026-10-04, e il comando che li recupera e' `git cat-file -p 4df94a7:<percorso>`, verificato
al byte** — perche' **il comando che li ha PRODOTTI non e' identificabile**: nessuno strumento
committato scrive quel percorso.

## ② IL README: il default conta piu' della descrizione

Ogni flag o switch nuovo o modificato: **cosa fa**, **il DEFAULT**, e **se e' byte-inerte a
default spento**.

### 📌 **PERCHE' IL DEFAULT CONTA PIU' DELLA DESCRIZIONE:** quando un default si **ribalta**,
*«l'assenza del flag»* **smette di significare OFF** — e i rami di controllo diventano
**duplicati del ramo di prova**, cioe' un confronto che non confronta niente.
### **Quindi quando si ribalta un default si cercano, NELLO STESSO COMMIT, tutti i punti che
ottenevano il vecchio comportamento per OMISSIONE.**

## ③ LA FISICA

Ogni legge nuova, curata o riqualificata si riflette in `doc/REGISTRO_FISICA.md`: **la forma,
la derivazione, il perche'** — non solo il registro dei difetti.
### ✅ **Questa terza e' GIA' AUTOMATICA: la impedisce `H-REG-R`** — e non si accontenta di
una riga qualsiasi, pretende che **la diff cada DENTRO la sezione della legge toccata**.

### ⚠ **Una scheda nuova va scritta DENTRO la sezione di chi possiede quella funzione, non in
coda al file:** `H-REG-R` mappa le sezioni **da un marcatore al successivo**, quindi una
scheda appesa in fondo cade nella sezione dell'**ultima** scheda. *(Succeduto col `6b`:
la scheda di `A13` alla nascita finiva in `registro-grandezze`.)*

## IL LIMITE, per `A9`

### ⛔ **① e ② SONO REGOLE SCRITTE, NON PRESIDI: oggi non impediscono nulla.** Il meccanismo
che le renderebbe presidi e' **proposto e non cablato**:
`doc/PROPOSTA_presidi_inventario.md`.

### **E il lavoro sui non tracciati ne ha trovate TRE omissioni in due giorni:**
`_sigillo_cura5_a13nascita.py` e `_sigillo_mem_moto_tutto.py` **non avevano alcuna voce**, e
`_scena_video.py` **non ha una riga propria**. ### **Tre in due giorni e' la misura di quanto
una regola scritta valga meno di un presidio.**
