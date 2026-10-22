# IL DOCUMENTO DI RACCOLTA SU `cs` E `Lambda_c`: CHE COSA E' GIA' STATO CHIESTO, DECISO E LASCIATO APERTO

> **Il mandato:** decisione di Luca del `2026-10-22` alle `20:52`, in fondo alla coda *(eseguito dopo `7fc47558`)*. ### **Un DOCUMENTO: nessun
> codice di fisica, nessuna corsa; nessuna decisione.**

**LIVELLO:** un documento.

## 0. LA STELLA POLARE

### **Non si applica nessuna delle cinque domande** *(nessuna legge, nessun risultato nuovo)*: ### **il documento raccoglie, non decide.** ### **La
lettura di oggi** *(sez. `3` del mandato)* ### **e' dichiarata come tale.**

## 1. IL METODO DELLA RICERCA, DICHIARATO PRIMA *(cosi' la raccolta e' ripetibile)*

### **Uno script, `csv/_raccolta_cs.py`, che stampa TUTTO e conta** *(il referto `doc/referti_l2/raccolta_cs.txt` e `.jsonl`)*. ### **Le parole** *(una
espressione regolare sola, che non distingue maiuscole)*: ### **`cs` come parola intera** *(non dentro un'altra parola)*, ### **`Lambda_c`**, ### **`LAMBDA-C`**,
### **`CAMM-FASE-VUOTO`**, ### **`cs_al_centro`**, ### **`accendi_cs`**, ### **`CS-` all'inizio di un ID.** ### **Dove si cerca, e come si conta:**

| | dove | come si conta |
|---|---|---|
| `A` | ### **le voci dell'indice** *(`doc/indice/voci.jsonl`)* | ### **una voce conta se la parola sta nell'ID, nel titolo, o se `CAMM-FASE-VUOTO` sta nel suo campo `leggi`**; ### **a parte, contate, quelle dove sta SOLO nella descrizione** |
| `B` | ### **i nodi di decisione** *(`doc/ALBERO_era2.yaml`)* | un nodo conta se la parola sta nel suo blocco |
| `C` | ### **le sezioni della mappa** *(`doc/MAPPA_DIPENDENZE.md`)* | un'intestazione `#` conta se la parola sta nell'intestazione |
| `D` | ### **i task history** *(`doc/TASK_HISTORY/*.md`)* | un file conta se la parola sta nel titolo o nelle prime `3000` lettere |
| `E` | ### **i referti** *(`doc/referti_l2/*.txt`)* | un file conta se il NOME contiene `cs`, `lambda_c`, `fase_vuoto`, `strada_d` |
| `F` | ### **le leggi** *(`primo_ordine/leggi/leggi.yaml`)* | ### **la scheda di `CAMM-FASE-VUOTO`**, e le leggi che la citano |

### ⚠ **I LIMITI, dichiarati prima:** ### **una ricerca per PAROLA non e' una lettura:** trova `cs` dove c'e' la parola, ### **non dove si parla della
velocita' locale della luce con altre parole**; ### **il criterio `D` e `E` e' piu' largo per i task history e piu' stretto per i referti.** ### **Lo
script NON decide niente** *(`[[DECISIONE-VUOLE-UN-CAMPO]]`: un documento non e' una decisione di programma)*.

### Come si scrivono le schede

- ### **Le voci dell'era `2`** *(tutte, una scheda ciascuna)*: la domanda o la decisione ### **alla lettera** *(titolo, e la descrizione dove serve)*, ###
  **la data e il commit** *(campo `creata`, e il commit trovato da `storico-commit`)*; lo stato di oggi; ### **che cosa si era concluso**; ### **che cosa
  era rimasto aperto, e perche'** *(uno strumento, un dato, una decisione di Luca)*.
- ### **Le voci dell'era `1`** *(il motore vecchio)*: ### **in una tabella**, con stato e titolo: ### **riguardano un `cs` che non e' quello di oggi.**
- ### **I nodi, la mappa, i task history, i referti:** ### **elencati e contati**, coi rimandi.

## 2. CHE COSA CREDO PRIMA

- ### **Che le domande aperte su `cs` siano poche e che si ripetano** *(la forma, il valore di `Lambda_c`, dove vive `Lambda_c`)*, ### **e che la piu' antica
  sia la piu' ripetuta.**
- ### **Che il nome `cs` sia usato per DUE cose**: ### **il `cs` dell'era `1`** *(`_cs_nodo`, col suo pavimento)* ### **e quello dell'era `2`** *(`Lambda/(Lambda +
  Lambda_c)`)* -- ### **un omonimo come `LINEARE`.**
- ### **Che lo strumento che manca a molte domande sia arrivato in questi giorni** *(la stabilita' lineare, il criterio dell'accoppiamento)*.

## 3. TODO

1. Questo task history, ### **committato DA SOLO.**
2. `csv/_raccolta_cs.py`: commit, corsa, il referto.
3. `doc/RACCOLTA_CS.md`; ### **la relazione con la sintesi e UNA domanda** *(da quale domanda su `cs` ripartire)*. ### **NESSUNA SCELTA.**
