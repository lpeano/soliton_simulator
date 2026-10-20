# IL PRESIDIO `PI-ERA-STATO` CONTRO `CLAUDE.md` par.`13`: `SOSPESA` PER LE VOCI DELL'ERA `2`

> **Il mandato:** decisione di Luca del `2026-10-20` alle `18:55`, sulla domanda di `68446777`.
> ### **Infrastruttura dell'indice: nessun codice di fisica, nessuna corsa.** Impronta
> `2e7f795d2a52fbe7` e `leggi.yaml` intatti; ### **il conto della base proiettata in corso
> (blob `3e054285`) non si tocca.**

**LIVELLO:** infrastruttura.

## 1. RAGIONAMENTO PRELIMINARE — cosa credo, PRIMA di leggere il presidio per intero

- **Cio' che ho visto finora** *(solo il messaggio d'errore di `crea-lotto`, in `68446777`)*: ### **«`PI-ERA-STATO` `GRIGLIA-A-TRIANGOLI`: era `2` con stato `SOSPESA`. L'era `2` NON E' COMINCIATA: una sua voce APERTA e' `AGENDA`. Una voce DECISA o CHIUSA invece puo' stare cosi': una domanda a cui Luca ha risposto NON E' «in agenda»».**
- **Cosa credo:**
  - ### **che il fatto «l'era `2` non e' cominciata» sia SCRITTO nel presidio** *(una regola o una costante in `csv/indice.py`, del tempo in cui era vero)*, ### **e non letto da una fonte che si aggiorna**: `CLAUDE.md` par.`13` e' stato corretto il `2026-10-19` *(«l'era `2` E' COMINCIATA»)*, e se il presidio leggesse da li' non avrebbe rifiutato;
  - ### **che `SOSPESA` nello schema sia nata per le voci dell'era `1`**: lo schema pretende `stato_era_1` non vuoto per `SOSPESA` *(`doc/INDICE_SCHEMA.md`, «i campi obbligatori per stato»)*, ### **e questo fa pensare a «voce aperta di un'era CHIUSA»**, non a «in attesa per scelta»;
  - ### **che `AGENDA` sia «da fare, quando l'era `2` comincera'»**.
- ### **Quindi credo che la risposta stia FRA i due rami del bivio:** la fonte e' ferma *(primo ramo)*, ### **ma la definizione di `SOSPESA` potrebbe essere legata all'era `1`** *(secondo ramo)*. ### **La diagnosi deve dire quale dei due pesa, con le citazioni.**
- **Cosa NON so:** dove sta la regola; se `SOSPESA` ha una definizione scritta; da quale decisione nasce.

## 2. LA DIAGNOSI — tre domande, ciascuna con la citazione ALLA LETTERA del sorgente

- **a)** ### **DOVE** il presidio prende «l'era `2` non e' cominciata»: una costante, un campo di `_indice_meta.json`, una tabella, un'altra fonte?
- **b)** ### **CHE COSA significa `SOSPESA`** nello schema, e ### **da quale decisione** nasce la regola *(`storico.jsonl`, task history, `CLAUDE.md`)*: «voce aperta in attesa per scelta» oppure «voce aperta di un'era CHIUSA»?
- **c)** ### **CHE COSA significa `AGENDA`** nello schema.

### IL BIVIO, fissato qui *(dal mandato)*

- ### **Se il presidio ricava «era `2` non cominciata» da una fonte FERMA** *(una costante o un campo mai aggiornato)* ### **che contraddice `CLAUDE.md` par.`13`: e' un DIFETTO DELLA FONTE** → punto `3`.
- ### **Se invece `SOSPESA` e' riservata per definizione alle voci di un'era CHIUSA, e `AGENDA` e' lo stato giusto per una voce rimandata dell'era corrente: il presidio HA RAGIONE**, la raccomandazione del guardiano cade → ### **NESSUNA modifica**, la voce resta `AGENDA`, e si scrive per Luca la definizione con la citazione. ### **STOP.**
- ### **Se non e' ne' l'uno ne' l'altro: STOP**, e la domanda torna a Luca con le citazioni.

## 3. LA CORREZIONE *(solo nel primo ramo)*

- ### **Si corregge LA FONTE del fatto** *(lo stato dell'era)*, ### **NON si allenta la regola:** il presidio legge lo stato dell'era ### **da UN solo posto**, coerente con `CLAUDE.md` par.`13`. ### **Se le fonti sono due, si dichiara quale vince e perche', e un controllo nuovo le confronta** *(se divergono, il validatore FALLISCE)*.
- ### **I CASI** *(copiati dal mandato prima dei numeri)*:
  - ### **DEVE RIUSCIRE:** `GRIGLIA-A-TRIANGOLI` in `SOSPESA` passa il validatore;
  - ### **DEVE FALLIRE:** una voce finta di un'era che non esiste *(era `9`)* in `SOSPESA`: il presidio la rifiuta;
  - ### **DEVE FALLIRE:** la fonte dell'era riportata a «era `2` non cominciata»: ### **il controllo di coerenza con `CLAUDE.md` fallisce.**
  - ### **I casi finti si costruiscono in memoria o in un file temporaneo, MAI nell'indice.**
- ### **Il collaudo del presidio** *(`doc/COLLAUDO_presidio_indice.txt`)* rigenerato e committato, ### **col numero dei casi.**

## 4. LA VOCE E IL CONTO

- `GRIGLIA-A-TRIANGOLI` da `AGENDA` a `SOSPESA` ### **con la procedura dell'indice per una modifica** *(lotto, storico)*, e la frase «SOSPESA nell'intenzione di Luca» tolta dalla descrizione.
- ### **La voce speculativa NON e' ancora registrata** *(preparata fuori dal repo, in attesa del referto della base proiettata)*: ### **quel mandato la registra direttamente in `SOSPESA`**, se il primo ramo regge.
- ### **Il conto, da script:** quante voci dell'era `2` sono in `SOSPESA` e in `AGENDA` ### **prima e dopo.**

## 5. TODO

1. Questo task history, ### **committato DA SOLO.**
2. La diagnosi con le citazioni; il ramo del bivio.
3. Nel primo ramo: la correzione della fonte, i casi, il collaudo; poi la voce.
4. La relazione: il ramo, le citazioni, i casi, il conto, ### **e l'errore `n.25` del guardiano** *(la mitosi come «assorbitore» detta «gia' registrata» alle `15:17`, e non lo era)*. ### **Nessuna voce si crea per lei: la decisione e' di Luca.**
