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
