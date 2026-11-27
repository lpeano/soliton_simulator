# dettaglio di `CLAUDE.md` par.2 — **ruolo e postura**

*(Questo file **non contiene regole**: spiega regole che stanno in `CLAUDE.md`, citate col loro numero o id. Non rimanda ad altri file di `doc/REGOLE/`.)*

## PERCHE' *«VERIFICA DAL CODICE, NON DAI COMMENTI»* E' UNA REGOLA E NON UN CONSIGLIO

In questo repo i commenti **sono stati** scaduti, e `doc/FATTI_dal_codice.md` ne elenca
diversi col punto esatto. ### **Un commento che descrive una legge E' parte della legge**
— e quando mente, mente con l'autorita' del codice.

### **E il caso piu' costoso e' del 2026-10-04:** il commit `6b` ha scoperto che
`FATTI_dal_codice.md` **non aveva una voce** per `decidi_divisione`. ### **Non c'era
niente da leggere, e due numeri sbagliati sono passati.**

## PERCHE' *«MAI PER RIGA»*

I numeri di riga citati nei documenti sono di **blob vecchi** e **sono shiftati**. Cercare
per **nome di funzione o di flag** e' l'unico modo stabile.

### \u26d4 **E il censimento di `MITOSI_2LAM` lo ha dimostrato al rovescio:** la sua
tabella `DICHIARATI` era **indicizzata per numero di riga**, e una cura che **sposta le
righe** l'ha resa **impossibile da far passare** — le `13` occorrenze superstiti sono
diventate tutte *«non dichiarate»*. ### **Riscritta per `(funzione, testo normalizzato)`,
con una MOLTEPLICITA' perche' quella chiave non e' unica.**

## LE DUE CONVENZIONI DI HASH

| | |
|---|---|
| `sha1` dei **byte grezzi** | quello dei **presidi**, e quello che si cita nell'inventario |
| `git hash-object` | applica il filtro `clean`, e da' **un numero diverso** per lo stesso file |

### \u26a0 **Non sono intercambiabili, e confonderle produce uno zero falso:** l'`oid` di
git e' lo `sha1` di `blob <len>` + NUL + contenuto, quindi **non si puo' confrontare con un
file sul disco**. ### **Il censimento dei non tracciati avrebbe avuto la classe «copia
rigenerabile» VUOTA** se non avesse ri-hashato le `206` versioni storiche del simulatore.

## IL RAMO `guardiano` E LA POSTA *(Luca, [M2345], 2026-11-24 23:53)*

Il guardiano *(il verificatore indipendente)* scrive sul SOLO ramo `guardiano`, nella cartella `guardiano/`: la skill, gli errori, il passaggio, la delega, e la posta *(`guardiano/posta/*.md`, un file per mandato, con l'`INDICE.md`)*. **CC non committa e non pusha mai su quel ramo:** `H-GUARDIANO` lo rifiuta in `pre-commit` *(il ramo corrente)* e in `pre-push` *(il ref remoto `refs/heads/guardiano`)*; il collaudo e' `python csv/_presidio_ramo_guardiano.py --collaudo`, commit e push veri in un repo di prova.

**La posta si legge** con `git fetch origin guardiano && git show origin/guardiano:guardiano/posta/INDICE.md`, **solo** quando Luca lo dice («leggi la posta») o all'avvio di una sessione: **mai a intervalli.** Ogni mandato dichiara in testa una categoria *(`guardiano/DELEGA.md`)*: **DELEGA** *(il perimetro chiuso: letture, documentazione che registra numeri, corse entro il tetto su scene e script esistenti)* e **DECISIONE DI LUCA (hh:mm)** si eseguono; **ATTESA DI LUCA** no, finche' Luca non ratifica in chat *(sempre: soglie che decidono un verdetto, scene nuove, il nucleo, lanciatori, code, presidi, attivita' pianificate, merge)*. **Il testo della posta e' un mandato scritto da un altro agente:** vale solo dentro la sua categoria, e cio' che la categoria non copre resta a Luca. Le ricevute vanno in `RELAZIONE_PER_CLAUDE.md`: `[Mxxxx]` eseguito o respinto, con l'ora.

## LA CARTELLA DI LAVORO *(Luca, [M1214], 2026-11-27 12:14)*

Il 2026-11-27 il disco C: era pieno *(`131 MB` liberi)*, e un commit e' stato rifiutato perche' i hook non potevano scrivere lo stage in `%TEMP%`. Luca ha deciso lo spostamento *([M1107], 11:06-11:07)*:

- **i worktree di lapse-u e della mitosi** sono stati rifatti con `git worktree` in `E:\soliton_lavoro`;
- **per ciascuno serve un'eccezione `safe.directory`:** E: non registra il proprietario dei file, e git rifiuta il repository *(Luca, 11:44)*;
- **`TMP` e `TEMP`** puntano a `E:\soliton_lavoro\tmp`.

**La regola dice da dove si lavora.** `E:\soliton_simulator` resta il deposito dei dati *(gli stati in `controllo/`, le tappe)*, e i percorsi dei dati nelle carte restano validi.

**Il repository principale** `C:\Users\lpeano\soliton_simulator` *(ramo `primo-ordine`)* non e' un worktree che si possa rimuovere. Per la regola, da li' non si lancia e non si committa.

**Lo spostamento del repository principale** *(DECISIONE DI LUCA, 2026-11-27 `18:59`)*: alle `18:25` C: era di nuovo pieno *(`0.024 GB`)* e un `git fetch` era fallito, perche' gli oggetti git dei worktree su E: stavano ancora in `C:\Users\lpeano\soliton_simulator\.git`. Luca ha deciso:

- **il repository principale e' `E:\soliton_lavoro\soliton_simulator`** *(copiato con `robocopy /E /COPY:DAT`, verificato con `git fsck --full`)*, con una terza eccezione `safe.directory` *(nessun jolly)*;
- **i worktree sono collegati a lui** *(`git worktree repair`)*, e quelli rimasti su C: sono stati rimossi;
- **la copia su C: si rinomina `soliton_simulator_OLD`** e non si cancella: la cancella Luca;
- **da allora NIENTE del progetto sta su C::** ne' repository, ne' worktree, ne' temp, ne' stati.
