# PROPOSTA — **rendere PRESIDI le tre regole del par.5-novies**

> **⚠ QUESTO DOCUMENTO PROPONE E BASTA. NIENTE E' CABLATO.** Il mandato del 2026-09-20 dice:
> *«PROPONI E RIPORTA PRIMA DI CABLARLO. Non cablare da solo.»*
> **Decide Luca.**

---

## 1. IL PROBLEMA, misurato dal disco il 2026-09-20

```
strumenti  csv/_test_fork/*.py      79      in INVENTARIO   19   (24 %)   ->  60 MANCANTI
sigilli    csv/_seal_fork/*.py      45      in INVENTARIO    8   (18 %)   ->  37 MANCANTI
                                                                     TOTALE  97 MANCANTI
flag CLI   add_argument()           93      nel README      38   (41 %)   ->  55 MANCANTI
```

**⚠ I NUMERI SONO PEGGIORI DI QUELLI DA CUI IL MANDATO PARTIVA** (`81 / 34 / 47`, il 42 %), **e la
differenza non e' un dettaglio:** quel conto **non includeva `csv/_seal_fork/`**, cioe' proprio i
**sigilli** — che sono la categoria dove l'omissione costa di piu', perche' un sigillo non
inventariato e' un sigillo che **nessuno rigirera'**, ed e' la definizione di `Z31`.

**E il difetto NON e' l'abbandono:** l'inventario e' **vivo**, aggiornato stamattina.
**Il difetto e' che l'aggiornamento dipende dal RICORDARSENE.**
**`A9`: un presidio che dipende dal ricordarsene non e' un presidio.**
**`Z31` e' gia' successo TRE volte, l'ultima dopo essere stato citato due volte nella stessa
sessione** — la prova piu' forte che la buona volonta' non basta.

---

## 2. IL CRITERIO DI VALUTAZIONE — **`A9`: IMPEDISCE o RICORDA?**

Un meccanismo vale come presidio **solo se non dipende da un atto volontario**. Tutto il resto e'
una nota, e va chiamato nota.

**E un secondo criterio, che il mandato stesso impone:**
> *«un presidio che blocca un run per un difetto di DOCUMENTAZIONE sarebbe peggio del difetto.»*

**Quindi il meccanismo giusto non e' il piu' severo: e' quello che non dipende dalla memoria E non
puo' far perdere lavoro.**

---

## 3. I CANDIDATI, valutati — **e il primo che viene in mente e' il peggiore**

| # | meccanismo | `A9` | costo | rischio | verdetto |
|---|---|---|---|---|---|
| **(a)** | **un SIGILLO** che confronta il disco con l'inventario e FALLISCE se divergono | **RICORDA** — qualcuno deve girarlo | basso | nessuno | **insufficiente da solo.** E' esattamente il difetto che deve curare: dipende dal ricordarsi di girarlo |
| **(b)** | **un HOOK di commit** su `csv/_test_fork/*.py` | **IMPEDISCE** | basso | ⚠ **vive in `.git/hooks`, NON nel repo: chi clona non ce l'ha**, e un `--no-verify` lo salta | **parziale.** Con `core.hooksPath` verso una cartella del repo entrerebbe nel repo, **ma resta una `git config` locale da ricordarsi** — il difetto, di nuovo |
| **(c)** | **un controllo dentro `_presidio.avvia()` che BLOCCA** | **IMPEDISCE** | basso | ⚠⚠ **bloccherebbe uno strumento perche' non e' documentato** — e spesso uno strumento si scrive, si gira, e SOLO DOPO si capisce cosa vale la pena scrivere. **Farebbe perdere lavoro per un difetto di prosa** | **DA SCARTARE**, ed e' il candidato che sembrava migliore |
| **(d)** | **`_presidio.avvia()` che SCRIVE invece di bloccare** — un REGISTRO automatico | **IMPEDISCE l'OBLIO, non l'esecuzione** | ~zero | basso | **✅ E' LA PROPOSTA** |

### 3.1 Perche' **(d)**, e perche' e' DERIVATA e non scelta

**`_presidio.avvia()` fa gia' tutto il lavoro difficile** *(verificato dal codice, `csv/_presidio.py`,
126 righe)*: **calcola lo sha1 dei byte grezzi**, **chiede a git se il file e' tracciato e se
differisce da HEAD**, e **RIFIUTA gia' di girare un sigillo il cui blob non e' committato.**

> **Il precedente esiste gia' ed e' della categoria giusta: `avvia()` blocca su un difetto di
> RIPRODUCIBILITA'. Non blocca, e non deve bloccare, su un difetto di DOCUMENTAZIONE.**

**La proposta e' una riga in piu' in una funzione che gia' gira a ogni strumento lanciato:**
**appendere a `doc/_REGISTRO_STRUMENTI.tsv`** *(machine-readable, append-only)*:
```
data	percorso	sha1-byte	tracciato/modificato	riga-di-comando-completa
```
**Cosi' la META' MECCANICA dell'inventario — il file, il blob, il comando, l'ultima volta che e'
girato — SI SCRIVE DA SOLA.** Resta manuale **solo** la meta' che una macchina non puo' sapere:
**cosa misura**, e **se e' un sigillo o una sonda**.

**E allora il candidato (a) DIVENTA efficace**, che da solo non lo era: un sigillo che confronta il
**registro automatico** con `INVENTARIO_strumenti.md` **ha qualcosa di vero contro cui confrontare**,
invece di una lista di file che nessuno ha promesso di aggiornare.

### 3.2 Per il **README** il problema e' piu' facile, e si chiude da solo
I flag **si enumerano meccanicamente** — sono le `add_argument()` del simulatore, e oggi sono **93**.
**Un sigillo che confronta quei 93 nomi col testo del `README` e FALLISCE se ne manca uno** e'
sufficiente, **perche' i flag cambiano solo quando cambia il simulatore**, e il simulatore ha gia'
un rito di gate. **Qui (a) basta**: non c'e' il problema del «ricordarsi di girarlo», perche' lo
gira il gate.

---

## 4. ⚠ LA TERZA REGOLA **NON E' MECCANIZZABILE**, e lo dico invece di fingere

**③ FISICA — *«ogni legge nuova, curata o riqualificata va riflessa nella documentazione di
fisica»* — NON HA UN MECCANISMO, e non ne propongo uno finto.**

**Perche', e non e' pigrizia:** una macchina puo' contare i file e i flag perche' sono **enumerabili
dal codice**. **Non puo' sapere se una LEGGE e' cambiata**, ne' se cio' che e' scritto nel documento
di fisica **corrisponde** alla legge. Un controllo che segnalasse ogni `diff` al simulatore
**segnalerebbe tutto**, e **un allarme che suona sempre non lo legge nessuno** — e' il difetto
gia' misurato il 2026-09-19 sui blob nelle voci dei registri.

> **ESITO ONESTO: per ③ NON C'E' UN MECCANISMO. Resta una regola scritta, ed e' registrata come
> tale nel par.5-novies.** Il mandato autorizza esplicitamente questo esito, e **meglio dichiararlo
> che cablare un presidio finto.**

---

## 5. COSA SERVIREBBE PER CABLARLO — e **perche' NON si puo' fare oggi**

**⚠ `csv/_presidio.py` E' IMPORTATO DAI DUE RUN A/B CHE STANNO GIRANDO ADESSO.**
Il par.9 di `CLAUDE.md` dice: *«durante un run, nessun file del percorso in uso si modifica: non
solo il simulatore, ma anche il DRIVER e ogni script che il processo ha importato.»*

> **Quindi, anche se Luca approvasse ORA, il cablaggio di (d) NON si fa prima che i due run siano
> chiusi.** **Lo scrivo qui perche' questo e' esattamente il punto in cui il vincolo verrebbe
> aggirato in buona fede** — ed e' gia' successo il 2026-09-19, col driver.

**L'ordine, se approvato:**
1. **a run CHIUSI**, la riga in `_presidio.avvia()` + il file `doc/_REGISTRO_STRUMENTI.tsv`;
2. **il sigillo dei FLAG contro il `README`** *(indipendente da (d): si puo' fare anche subito,
   perche' non tocca nessun file in uso)*;
3. **il sigillo del registro automatico contro l'`INVENTARIO`**, che ha senso **solo dopo (1)**,
   quando il registro ha qualcosa dentro.

---

## 6. LE TRE DOMANDE PER LUCA

1. **(d) si cabla?** — `_presidio.avvia()` che **scrive** un registro automatico, **senza mai
   bloccare**. *(Il mio parere: si', ed e' l'unico dei quattro che soddisfa `A9` senza poter far
   perdere lavoro.)*
2. **il sigillo dei flag contro il `README` si fa subito?** — non tocca file in uso, e chiuderebbe
   **55 flag su 93** che oggi non sono documentati.
3. **③ FISICA resta una regola scritta?** — non ho un meccanismo, e non voglio proporne uno finto.

---

**LIMITI DI QUESTO DOCUMENTO:** i conteggi vengono da **una** passata sul disco del 2026-09-20
*(`csv/_test_fork/*.py` e `csv/_seal_fork/*.py`, escluse 5 copie del simulatore/driver;
«presente in inventario» = **il basename compare nel testo** di `doc/INVENTARIO_strumenti.md`)*.
**Il criterio di presenza e' GROSSOLANO**: conta che il nome ci sia, **non** che la voce sia
completa di comando e blob — quindi **`19` e `8` sono LIMITI SUPERIORI**, e le voci davvero
complete possono essere meno.
