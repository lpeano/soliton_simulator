# I TEMPI DELLA SUITE E DEI COMMIT *(mandato di Luca `2026-11-15` `23:49`; SOLO LETTURA)*

> **La decisione di Luca:** **prima di accelerare la suite, si sa dove va il tempo.** **Nessuna proposta adottata:** le strade *(parallelo, riuso per sha1, suite leggera)* le decide Luca coi numeri.

## 1. LE PREMESSE DAL CODICE *(cosa credo prima di guardare, e cosa NON so)*

- **`committa2.py`** *(uno strumento mio, fuori dal repo, nello scratchpad)* **scrive dalle `15:3x` un log per commit, `commit_log_<HHMMSS>.txt`: ogni riga dei hook col secondo dall'avvio di `git commit`.** **Nel log NON ci sono i lucchetti ne' il push:** **l'uscita di `committa2`** *(`c2_*.txt`)* **ha il totale** *(la riga `R3 uscita 0 in N s`)*, **quindi i lucchetti + `git commit` + il push si vedono solo INSIEME, come differenza.**
- **`collauda.py` stampa gia' una tabella col tempo di OGNI collaudo** *(«il collaudo / dove / secondi / esito»)*, **e le uscite delle suite girate oggi sono nello scratchpad**: **il punto 2 si fa dalle suite gia' girate, nessuna suite in piu'.**
- **In fila o in parallelo:** **credo IN FILA** *(un ciclo che chiama `subprocess.run`, che aspetta)*: **lo dice il codice.**
- **La somma «esatta»:** **cerco la parola `"esatta"` nel file del collaudo.** ### **Cosa NON so:** **un collaudo che importa un modulo che usa `fsum` non si vede cosi': dichiarato.**
- **Il carico:** **le corse APERTE dal registro del ramo `strumento-mattone`** *(dove stanno tutte le corse di oggi)*; **le suite e le prove fuori registro NON contate: dichiarato.**
- **I log e le suite vengono da tre posti** *(il principale, il worktree del mattone, il clone su E:)* **e da due interpreti** *(C: ed E:)*: **la tabella li mette insieme; il ramo di ogni commit e' scritto.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO

1. **Lo script `doc/referti_l2/tempi_suite_conta.py`** *(fuori da `csv/` e da `primo_ordine/`: non e' sorvegliato dalla suite, e il mandato non vuole una suite in piu' solo per misurare)*: **legge i log, le uscite di `committa2`, le tabelle delle suite del giorno, `collauda.py` col parser** *(`ast`, nessun import)* **e il registro.**
2. **Il referto `doc/referti_l2/tempi_suite.txt`:** **(1) una tabella per commit** *(l'ora, il ramo, il commit, il totale, i hook, il «fuori», le corse aperte, i tre passi piu' lenti)*; **ogni passo dei hook con la mediana e il massimo; (2) i collaudi in ordine di tempo** *(la mediana sulle suite del giorno, il massimo)*, **la quota dei primi `5`, quali hanno `"esatta"`; (3) in fila o in parallelo.**
3. **Mi farebbe FERMARE:** **una tabella di una suite che non si legge** *(meno di `60` righe: scartata, scritto)*; **un nome della tabella che non e' nella lista di `collauda.py`** *(scritto, non indovinato)*.

## 3. TODO DEL NEXT STEP

- [ ] **questa carta** *(commit, push)*
- [ ] **lo script** *(commit, push, PRIMA di girarlo)*
- [ ] **il referto** *(commit col verdetto)*; **la relazione sul principale**
- [ ] **poi la coda:** **il codice di H1 nel clone** *(la suite sui byte nuovi in corso)*, **D2b `--fma si`, i tempi del motore.**
