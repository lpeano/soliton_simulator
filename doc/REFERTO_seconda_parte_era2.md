# IL REFERTO DELLA SECONDA PARTE — **i `16` punti dei metodi dell'era `1` nell'era `2`**

> ### ⭐ **IL PRINCIPIO DEL MANDATO, e il metro con cui mi giudico:** *«ogni errore e' nato da una macchina che leggeva la prosa»*. ### ⛔ **Le decisioni si prendono SOLO da campi strutturati a vocabolario chiuso; il testo libero si conserva e si protegge, MAI si interpreta per decidere.**

**Il simulatore dell'era `1`: `b8c21049`, NON toccato** *(verificato per `sha1` in ogni commit)*. ### ⛔ **E NESSUNA DECISIONE DI FISICA E' STATA PRESA:** il conto delle leggi e' ### **`3`, e `3` sono `prova: true`** — cioe' ### **ZERO leggi vere.**

---

## `1.` I `16` PUNTI, UNO PER UNO

| | il punto | che cosa c'e' | dove |
|---|---|---|---|
| **`0`** | il censimento dei metodi | ### **`120` metodi, `120` righe** — e il mandato ne nominava *«una decina»* | `P-M1` |
| **`1`** | i domini che FERMANO | `3` forme a vocabolario chiuso, il controllo ### **generato** e chiamato ### **a ogni passo** *(`2` chiamate, via AST)* | `stato.py::controlla_domini` |
| **`2`** | nessun ramo nei termini | `11` nomi vietati; ### **`21` rami dichiarati** in `9` funzioni, e ### **`0` default** | `P-R1` |
| **`3`** | la nascita in un solo punto | ### ⛔ **APERTO: serve una decisione di Luca** *(`DEC-NASCITA-PSI`)* | `DA_DECIDERE_LUCA.md` |
| **`4`** | il veleno | ### ⚠ **VERO E VUOTO, e il numero lo MISURA:** `0` derivati, perche' lo stato e' solo `psi` | `_collauda_passo.py` sez. `(I)` |
| **`5`** | il timbro | l'impronta di ### **tabella, generati e configurazione**, piu' scena, seme, versioni e ### **il conto delle leggi** | `timbro.py` |
| **`6`** | salva e riprendi | ### **la ripresa RIFIUTA** se tabella, generati o configurazione sono cambiati — ### **rifiuta, non avverte** | `timbro.py::riprendi` |
| **`7`** | il modello di sigillo | ### **`4`/`4`**, e il *«prima»* ### **non e' piu' una copia patchata**: si ottiene mettendo a ### **zero il coefficiente** | `sigilli/_modello.py` |
| **`8`** | la REVERSIBILITA' | entrambi gli integratori tornano entro ### **`4e-15`** su `4` semi — ### **quattro ordini sotto la lettura fissata** *(`1e-9`)* | `_collauda_passo.py` sez. `(G)` |
| **`9`** | un solo esecutore | `6` eccezioni ### **dichiarate** su `3` file, e guarda ### **le chiamate E I NOMI** | `P-ES1` |
| **`10`** | il conto delle leggi | ### **`3`, di cui `3` di prova** — stampato dal ### **timbro** E dal ### **referto** | `timbro.py::conto_leggi` |
| **`11`** | la modularita' | `22` moduli ### **in mappa**, tetto `700` righe; ### ⛔ **`11(a)` e' APERTO** *(`DEC-REGOLA-FORMA`)* | `P-MOD` |
| **`12`** | i controlli nell'indice | ### **`31` presidi dichiarati dal codice**; `F1`…`F12` ### **rinominati** con alias namespaced; ogni sigillo dichiara `LEGGE` e `CRITERI` | `P-C1`, `P-E9` |
| **`13`** | metadati e testo libero | ### **`6` `ERRORE` non toccano la prosa**, `6` `SEGNALE` la leggono; `10` registri *(5 REPERTO, 4 REPLAY, 1 SOLO-AGGIUNTE)*; `10` citazioni ### **ri-verificate su `git show`** | `P-T1`, `P-T2`, `P-T3` |
| **`14`** | i riferimenti nel codice | `@rif` ### **byte-inerte, verificato con `is`**; `4` riferimenti e ### **il verso opposto GENERATO**; e `indice.py rinomina` ### **in un colpo** | `P-RIF`, `_rinomina.py` |
| **`15`** | la configurazione e i dati | `11` campi ### **tutti obbligatori**, ### **zero default** nella fisica, ### **nessun interruttore per le leggi**, e il ### **campo UNICO** in un `A`/`B` | `schema_config.py`, `P-AB` |

### ⛔ **DUE PUNTI RESTANO APERTI, e NON per dimenticanza:** il `3` *(con che stato nasce un nodo)* e l'`11(a)` *(che codice genera una `regola`)* chiedono ### **una DECISIONE DI FISICA**, e ### **non la prendo al posto di Luca.** Registrate in `DA_DECIDERE_LUCA.md`, come lui ha autorizzato.

---

## `2.` I COLLAUDI — ### **presi dall'uscita dei comandi**

| il collaudo | il comando, ### **verbatim** | esito |
|---|---|---|
| i presidi dell-era 2 | `python csv/_presidi_era2.py --collaudo` | ### ✅ **`22`/`22`** |
| `P-M1` i metodi | `python csv/_metodi_era2.py --collaudo` | ### ✅ **`8`/`8`** |
| `P-C1` i controlli nell-indice | `python csv/_controlli_nell_indice.py --collaudo` | ### ✅ **`8`/`8`** |
| `P-T1` il testo libero | `python csv/_testo_e_metadati.py --collaudo` | ### ✅ **`11`/`11`** |
| `P-T2` il replay dei registri | `python csv/_replay_registri.py --collaudo` | ### ✅ **`13`/`13`** |
| `P-T3` le citazioni strutturate | `python csv/_citazioni_strutturate.py --collaudo` | ### ✅ **`14`/`14`** |
| `P-R1` i rami dichiarati | `python csv/_rami_era2.py --collaudo` | ### ✅ **`12`/`12`** |
| `P-RIF` i riferimenti nel codice | `python csv/_rif_nel_codice.py --collaudo` | ### ✅ **`10`/`10`** |
| `P-ES1` un solo esecutore | `python csv/_un_solo_esecutore.py --collaudo` | ### ✅ **`8`/`8`** |
| `P-MOD` la modularita- | `python csv/_modularita_era2.py --collaudo` | ### ✅ **`10`/`10`** |
| `P-AB` i confronti e i dati | `python csv/_confronti_e_dati.py --collaudo` | ### ✅ **`13`/`13`** |
| il rinominamento, sul piano | `python csv/_rinomina.py` | ### ✅ **`11`/`11`** |
| `@rif` byte-inerte | `python primo_ordine/_rif.py` | ### ✅ **`14`/`14`** |
| lo schema delle leggi | `python primo_ordine/leggi/schema.py` | ### ✅ **`25`/`25`** |
| lo schema della configurazione | `python primo_ordine/config/schema_config.py` | ### ✅ **`24`/`24`** |
| il generatore | `python primo_ordine/_genera.py --prova` | ### ✅ **`22`/`22`** |
| il modello di sigillo | `python primo_ordine/sigilli/_modello.py` | ### ✅ **`4`/`4`** |
| i presidi dell-indice | `python csv/_collaudo_presidi_indice.py` | ### ✅ **`67`/`67`** |
| i controlli della migrazione | `python csv/_controlli_indice_v2.py` | ### ✅ **`6`/`6`** |
| il collaudo della catena | `python primo_ordine/_collauda_passo.py` | ### ⚠ **SALTATO: e' LENTO** *(oltre `120` secondi)*, e la CI lo passa con `--con-lenti` |

### **In tutto: `302` bracci passati**, su `19` comandi *(e `1` saltato perche' LENTO, dichiarato)*.

---

## `3.` I METODI DELL'ERA `1`: DOVE SONO ARRIVATI

| | quanti |
|---|--:|
| **`PORTATO`** | `90` |
| **`DA_PORTARE`** | `17` |
| **`DA_DECIDERE`** | `5` |
| **`NON_SI_APPLICA`** | `8` |
| **in tutto** | ### **`120`** |

### ⚠ **E `DA_PORTARE` NON E' ZERO, ed e' giusto che non lo sia:** `17` metodi ### **si applicano e non ci sono ancora** — e la colonna `dove` di ciascuno ### **dice quale punto li portera'.** ### **Dichiarati, non nascosti.**

---

## `4.` CHE COSA HO SBAGLIATO, E CHE COSA MI HA CORRETTO

> ### ⭐ **QUESTA E' LA SEZIONE CHE CONTA.** Un referto che elenca solo cio' che funziona ### **non dice se i presidi funzionano** — lo dice ### **l'elenco delle volte che mi hanno fermato.**

| | che cosa ho sbagliato | chi me l'ha detto |
|---|---|---|
| `1` | `A16` e `A17` NON ERANO NELL'INDICE — i due assiomi che ### **governano l'era `2`**, e `A16` ### **da' il nome al ramo** — e li ho citati in ### **ogni commit** sotto una ### **mia** dichiarazione `[SENZA-INDICE]`, che li ha ### **nascosti per due giorni** | ### **`P-RIF`**, rifiutando un `@rif` verso `A17` |
| `2` | avevo rinominato la chiave delle eccezioni ### **nel codice e non nei dati**: `32` eccezioni dichiarate ### **avevano smesso di combaciare**, e i segnali sono passati da `19` a `53` | ### **il numero**, e l'ho spiegato ### **guardando CHI scatta**, non indovinando |
| `3` | avevo iniettato un ### **`CR` vero** in una descrizione *(escape interpretati in un heredoc)*, e il `CR` ### **rompeva una vista**: `valida` legge a newline universali, e un `CR` ### **diventa un `LF` in lettura** | ### **il validatore**, con un messaggio che accusava *«modificata a mano»* — ### **che era falso** |
| `4` | ho passato ### **`csv` INTERO** a `git add`, e ho committato ### **`54.687` righe** *(tre copie del simulatore)*. ### **Ma due dei cinque file erano strumenti VERI dimenticati**, e la mia eccezione li descriveva male | ### **il `git show --stat`**, e la regola del guardiano *(«non tracciato deve voler dire DIMENTICATO»)* |
| `5` | `H-FISICA-FUORI-LISTA` ### **giudica i percorsi STAGED e legge la lista DAL DISCO**: una modifica non committata ### **autorizza un commit** | ### **io**, guardando perche' il commit era passato — e la cura ### **e' dichiarata, non fatta** |
| `6` | la mia previsione sul punto `8` *(«il globale PEGGIORE del locale»)* ### **non regge**: con un seme sembrava vera, ### **con quattro il rapporto oscilla di un fattore `3.7`** e tutti i valori stanno al ### **limite della macchina** | ### **la misura a quattro semi**, che ho fatto ### **invece di fermarmi al primo** — ed e' il difetto che `P3` nomina |
| `7` | il mio rilevatore del punto `9` guardava ### **solo le CHIAMATE**, e il driver scrive `avanza = PA.passo_locale` e poi chiama `avanza(…)`: ### **non vedeva niente** | ### **`P-ES1` stesso**, con un'eccezione ### **ORFANA** |
| `8` | avevo messo `gradiente` fra le funzioni che *«avanzano»*, e il presidio ha accusato ### **`hamiltoniana.py`, che lo DEFINISCE** | ### **`P-ES1`**: calcolare `dH/dpsi*` ### **non e' avanzare lo stato** |
| `9` | la mia prima regola di attribuzione delle righe di storico filtrava ### **per CHIAVE**, e un ID puo' stare fra le etichette ### **E avere storico da quando era una voce** | ### **`34` errori di `P-T2`**, tutti dello stesso difetto |
| `10` | `pianifica` del rinominamento guardava solo `collegate`, `padre`, `alias`: ### **`assiomi`, `leggi` e `variabili` SONO riferimenti strutturati** | ### **il collaudo**, che ha detto *«`0` voci»* su `A17` |
| `11` | il mio collaudo di `P-ES1` aveva un ### **difetto di aliasing**: `salva` era ### **lo stesso dizionario** che il ripristino rimetteva | ### **il braccio finale** *(«rimesso tutto a posto, TACE»)* |
| `12` | due script di chiusura ### **non erano idempotenti**, e al secondo giro ### **inghiottivano la riga DOPO** *(l'indice di fine cercava il primo terminatore)*. ### **Due volte lo stesso errore** | ### **`P-M1`**, entrambe le volte |
| `13` | `P-T1`: avevo messo `split` e `lower` fra le chiamate vietate, e ha rifiutato `PI-STORICO-SENZA-COMMIT` — ### **spezzare un file in righe non e' interpretare una prosa** | ### **`P-T1` stesso** |
| `14` | il mio script di patch e' morto su ### **`cp1252`** stampando un'icona: ### **il presidio di encoding del par.`7`, che e' successo nove volte** | ### **l'eccezione**, a meta' lavoro |

### ⭐ **E IL CONTO E' LA COSA DA GUARDARE: `14` errori miei, e ### `9` me li hanno detti i presidi** — non io rileggendo.

### ✅ **E DUE PRESIDI HANNO PRESO SE' STESSI**, senza che lo prevedessi: `P-M1` ha rifiutato il commit chiedendo ### **la propria riga** appena la sua voce e' nata, e `P-C1` ha fatto lo stesso appena l'ho dichiarato. ### **E `P-RIF` si e' fatto PIU' FORTE appena l'indice si e' completato:** con `A16` e `A17` fra le voci ha trovato ### **`4` commenti in piu'**, che prima ### **erano invisibili.**

---

## `5.` CHE COSA RESTA APERTO

| | che cosa | perche' |
|---|---|---|
| `1` | ### **`DEC-NASCITA-PSI`**: con che stato nasce un nodo | il vincolo e' stretto *(la norma totale si conserva: `psi = 0` e' ### **vietato**, la copia del padre la ### **raddoppia**)*, ### **ma quale divisione e con che fase e' di Luca** |
| `2` | ### **`DEC-REGOLA-FORMA`**: che codice genera una `regola` | un `termine_*` ### **si deriva**; una `regola` ha `ingressi`/`uscite`/`bilancio`, e ### **che codice ne venga fuori e' fisica** |
| `3` | il buco di `H-FISICA-FUORI-LISTA` *(legge la lista ### **dal disco**)* | ### **misurato e dichiarato**, non curato: la cura e' ### **leggerla dall'indice di git**, ed e' un commit a se' |
| `4` | `metadati.jsonl` e' un ### **`REPERTO` per NECESSITA'** | ha ### **una via di scrittura** e ### **zero storico**: oggi il presidio lo tratta come reperto, ### **ma e' un BUCO** |
| `5` | la ### **CI non e' mai stata osservata girare** | e ### **non e' un presidio**: senza protezione del ramo gira ### **dopo** il push e ### **non impedisce niente** *(`A9`)*. ### **La cura — gli hook verificati all'avvio — e' la TERZA parte** |
| `6` | il ### **budget del `pre-commit`** | i collaudi lenti ### **superano i `120` secondi**, e oggi stanno ### **solo nella CI**: ### **il budget dichiarato e' il punto `6` della TERZA parte**, e questo e' ### **il primo posto dove e' servito** |

---

*(Referto generato da `csv/_referto_seconda_parte.py`: ### **ogni numero esce dall'uscita dei comandi della tavola `2.`** o dalle tabelle strutturate dei presidi — `L-NUMERI`. I lenti si passano con `--con-lenti`.)*
