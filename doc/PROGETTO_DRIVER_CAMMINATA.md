# IL PROGETTO DEL DRIVER DELLA CAMMINATA *(un documento: nessun codice, nessuna scelta)*

> **Il mandato:** di Luca, `2026-10-26`, la decisione `(1)` delle `08:57` *([[DOMANDA-DRIVER-CAMMINATA]], chiusa con la lettura `(ii)`; [[DECISIONE-SOLO-TRIANGOLI]], [[SUITE-NEL-COMMIT]])*: ### **il driver fara' girare la CAMMINATA** *(`tick.tick` sulla scena a triangoli)*. ### **Il task history: `doc/TASK_HISTORY/2026-10-26_driver_camminata.md`.**
> ### **Le funzioni sono citate per NOME** *(`CLAUDE.md` par. `2`)*.

## 1. CHE COSA E' OGGI

- ### **`primo_ordine/driver.py`: la pipeline delle leggi di PROVA.** ### **`gira(c)`:** ### **gli archi da `grafo(scena, nodi)`** *(`catena` o `anello`)*, ### **i termini di `leggi_attive`** *(`HAM.carica_termini`; oggi `PROVA-HOPPING` e `PROVA-LOCALE`, `prova: true`)*, ### **lo stato `ST.nuovo` riempito dal `Generator(seme)`, l'integratore `passo.passo_locale` o `passo_globale`** *(coi parametri del risolutore `iterazioni`, `toll`)*, ### **gli osservatori** *(`PROVA-NORMA`)* ### **e l'energia `HAM.energia` prima e dopo.** ### **`main`: un argomento solo** *(il file)*, ### **il timbro in testa, lo stato salvato in `db_era2/` col timbro accanto.**
- ### **LO SCHEMA** *(`config/schema_config.py`)*: ### **`CAMPI` = `versione, scena, nodi, seme, dt, passi, integratore, iterazioni, toll, leggi_attive, osservatori, confronto`, TUTTI obbligatori, il vocabolario CHIUSO** *(«un campo in piu' e' un errore»)*; ### **`SCENE = (catena, anello)`; `INTEGRATORI = (globale, locale)`; il globale solo con `confronto: true`.**
- ### **IL TIMBRO** *(`timbro.timbro`)*: ### **l'impronta della tabella** *(`leggi.yaml`)*, ### **dei GENERATI** *(`stato.py`, `termini/`, `osservatori/`)*, ### **della configurazione, il conto delle leggi dalla tabella** *(`conto_leggi`: per tipo, di prova, le variabili)*, ### **le versioni, il determinismo.** ### **`righe_timbro` stampa `scena`, `nodi`, `seme`, `dt`, `passi`, `integratore`, `leggi_attive`.**
- ### **CHI LO USA:** ### **`_collauda_determinismo`** *(lancia `driver.py` su `config/prova.yaml` e verifica l'ordine `DET.avvia` prima di `numpy`, via AST)*; ### **`_collauda_grafo`, `_collauda_simmetrie`, `_collauda_passo`, `_collauda_cs`** *(leggono `config/prova.yaml`: la catena di `9` nodi; i raggi del cono di `_collauda_passo` sono quelli della catena)*.
- ### ⚠ **LA CAMMINATA NON PASSA DAL DRIVER:** ### **il tick vero e' `tick.tick(st, mot, par)`** *(`percorri_tick` sui `14` pezzi di `composizione.ORDINE`, impronta `2e7f795d2a52fbe7`)* ### **su un `Motore`;** ### **oggi lo chiamano gli STRUMENTI** *(`csv/_triangoli.camminata` e i suoi figli; `scena_l2.scena_toro` costruisce `(inc, mot, st, par)`)* ### **e i collaudi del nucleo** *(`_collauda_tempo_proprio`, `_collauda_cs`, `_collauda_cs_centro`, `_collauda_cs_l1`, `_collauda_deriva`, `_collauda_scala`: importano `tick`)*. ### **Nessun programma del nucleo fa girare la fisica da una configurazione** *(l'errore `n.68` del guardiano)*.

## 2. CHE COSA DIVENTA *(la lettura `(ii)`)*

### **Un programma che, dato UN file di configurazione:** ### **`(1)` costruisce `scena_l2.scena_toro(GRIGLIA_DEL_MODELLO, lati, dtau, x)`** *(`GRIGLIA_DEL_MODELLO = "triangoli"`)*; ### **`(2)` prepara lo stato iniziale** *(la scena uniforme di `scena_toro`, o un pacchetto, o un grumo: e' un campo della configurazione)*; ### **`(3)` fa girare `tick.tick(st, mot, par)` per `passi` tick** *(i `par` dalla TABELLA: la moneta `EPS_MONETA`, mai dal file se la tabella la fissa)*; ### **`(4)` misura** *(le norme `M` e `V`, `H_tot` o `G` di `energia_pesata`, `cs` se acceso: le misure NOMINATE nel file, come gli osservatori di oggi)*; ### **`(5)` timbra e salva come oggi.**

## 3. LE OPZIONI *(con il costo e cio' che rompono; nessuna scelta)*

| | l'opzione | il costo | cio' che rompe | cio' che resta |
|---|---|---|---|---|
| `(A)` | ### **UNA SECONDA PIPELINE nello stesso `driver.py`** *(un campo `motore: prova | camminata` sceglie `gira_prova` o `gira_camminata`)* | ### **medio:** ### **lo schema diventa DUE vocabolari** *(i campi validi dipendono da `motore`)*, ### **e `valida` deve saperlo** | ### **la regola «un campo in piu' e' un errore» si deve riscrivere come «un campo in piu' PER QUELLA pipeline»;** ### **`_collauda_determinismo` lancia il driver: deve restare uguale per `prova.yaml`** | ### **un solo punto d'ingresso, un solo `main`, lo stesso timbro e lo stesso `salva`** |
| `(B)` | ### **UN DRIVER NUOVO** *(`primo_ordine/driver_camminata.py`, con il SUO schema `config/schema_camminata.py` e la sua configurazione `config/camminata.yaml`)* | ### **medio-basso:** ### **un file nuovo, un collaudo nuovo;** ### **il driver di prova NON si tocca** | ### ⚠ **«la configurazione e' UNA»** *(`CLAUDE.md` par. `13`)*: ### **due schemi = due configurazioni;** ### **va chiesto a Luca se la regola parla di UNA PER PROGRAMMA o di UNA in tutto il nucleo** | ### **i collaudi della catena INVARIATI per costruzione** *(non leggono il file nuovo)*; ### **`P-E4`** *(«nessuno importa `driver`»)* ### **vale anche per il nuovo** |
| `(C)` | ### **IL DRIVER DI OGGI SOSTITUITO** *(la catena tolta, i collaudi riscritti sui triangoli)* | ### **alto** | ### **i collaudi della catena** *(`_collauda_passo`, `_collauda_grafo`, `_collauda_simmetrie`, `_collauda_cs`, `_collauda_determinismo`)* ### **vanno ridefiniti** *(il contrasto `1` di `6ea2ba20`)* | ### **contro la decisione `(1)` del `2026-10-25`, `20:44`: «la catena resta solo per i collaudi di servizio»** |

## 4. LO SCHEMA DELLA CONFIGURAZIONE DELLA CAMMINATA *(i campi candidati, tutti obbligatori come oggi)*

| il campo | che cos'e' | da dove viene oggi |
|---|---|---|
| `versione` | il formato | come oggi |
| `griglia` | ### **NON un campo:** ### **e' `scena_l2.GRIGLIA_DEL_MODELLO`** *(`DECISIONE-SOLO-TRIANGOLI`)*; ### **il quadrato solo come `quadrato_di_servizio` ESPLICITO** *(un campo `servizio: true`?)* | `scena_toro(griglia, ...)` vuole il nome |
| `lati` | i due lati del toro | `scena_toro(..., lati, ...)` |
| `dtau` | il passo *(`s` sul tick: `B-5`, il cono, `s <= 1`)* | `scena_toro(..., dtau, ...)` |
| `x` | ### **l'ampiezza della materia uniforme** *(`sqrt(x)`)* | `scena_toro(..., x)` |
| `stato_iniziale` | ### **la scena uniforme, un pacchetto, un grumo: a vocabolario chiuso** | oggi negli strumenti |
| `passi` | quanti tick | come oggi |
| `eps` | ### ⚠ **NON nel file se la tabella lo fissa:** ### **oggi `scena_l2.EPS_MONETA = 0.5`, e gli strumenti di `csv/` la cambiano in memoria** *(la precisazione del sigillo `36040a07`)* | `scena_l2.EPS_MONETA` |
| `cs` | ### **la forma di `cs` accesa o spenta, e `lambda_c`** *(«`lambda_c` SI PASSA, SEMPRE: nessun valore predefinito»)* | `flussi_parziali.cs` |
| `misure` | ### **gli ID delle misure** *(come `osservatori`)* | `osservatori/` |
| `seme` | ### **serve solo se lo stato iniziale ha una parte casuale** *(la scena uniforme no)*: ### **«un campo che nessuno legge e' una manopola»** | come oggi |

### **E I CAMPI DI OGGI che la camminata NON legge:** ### **`nodi`** *(lo danno i `lati`)*, ### **`dt`** *(e' `dtau`)*, ### **`integratore`, `iterazioni`, `toll`, `confronto`** *(il tick e' una composizione di pezzi esatti, non un risolutore)*, ### **`leggi_attive`** *(⚠ l'ordine viene da `composizione.ORDINE`: ACCENDERE un pezzo per ID dal file sarebbe una manopola; `percorri_tick` ha gia' un argomento `salta`, che gli strumenti usano per spegnere `CAMM-MATERIA-VUOTO`)*.

## 5. IL TIMBRO DELLA CAMMINATA

- ### **OGGI conta le leggi di `leggi.yaml` e stampa `leggi_attive`;** ### **per la camminata deve timbrare cio' che ha girato:** ### **l'impronta della COMPOSIZIONE** *(`composizione.IMPRONTA`, oggi `2e7f795d2a52fbe7`)*, ### **i `14` pezzi in ordine** *(gli id e le frazioni)*, ### **i pezzi SALTATI** *(se `salta` diventa un campo)*, ### **la griglia, i lati, `dtau`, `x`, `eps` dalla tabella, la forma di `cs` e `lambda_c`**, ### **le impronte di `scena_l2.py`, `motore.py`, `tick.py` e dei file della chiusura del nucleo di `P-R1`** *(non solo dei GENERATI: la camminata non e' generata da `leggi.yaml`)*, ### **le versioni e il determinismo come oggi.**
- ### **`riprendi` rifiuta se cambiano** *(come oggi)* ### **l'impronta della composizione o della chiusura del nucleo.**

## 6. IL SIGILLO CHE IL CODICE DOVRA' PASSARE

| | la prova | il criterio |
|---|---|---|
| `(a)` | ### **la scena del driver = `scena_l2.scena_toro("triangoli", lati, dtau, x)`** | ### **AL BIT** *(`_triangoli_forza.byte_attr` su `Incidenza`, `Motore`, lo stato)* |
| `(b)` | ### **un tick del driver = `tick.tick` sulla scena dello strumento** | ### **AL BIT** |
| `(c)` | ### **`N` tick del driver = `N` tick di `csv/_triangoli.camminata`** *(con `salta` vuoto: ⚠ `camminata` salta `CAMM-MATERIA-VUOTO`, quindi il confronto va fatto col salto UGUALE)* | ### **AL BIT** |
| `(d)` | ### **i collaudi della catena invariati** *(il driver di prova e `config/prova.yaml` AL BIT prima e dopo, con l'opzione `(A)`)* | ### **la suite intera** |
| `(e)` | ### **l'impronta `2e7f795d2a52fbe7` e `leggi.yaml` intatti** | ### **al bit** |
| `(f)` | ### **un campo fuori vocabolario, la griglia `quadrato` senza `servizio`, un `eps` nel file quando la tabella lo fissa** | ### **DEVONO essere RIFIUTATI** |
| `(g)` | ### **«il driver gira la camminata ma la scena e' il quadrato»** | ### **DEVE FALLIRE, per la chiave giusta: il grado `6` a ogni nodo** |

## 7. LE DOMANDE PER LUCA

1. ### **`(A)` una seconda pipeline nello stesso driver, o `(B)` un driver nuovo?** *(`(C)` va contro la decisione delle `20:44`)*
2. ### **«LA CONFIGURAZIONE E' UNA»** *(`CLAUDE.md` par. `13`)*: ### **vuol dire UNA per programma** *(e allora `(B)` la rispetta)* ### **o UNA in tutto il nucleo** *(e allora `(B)` chiede di cambiarla)*?
3. ### **Lo stato iniziale: a vocabolario chiuso** *(uniforme, pacchetto, grumo)*, ### **e chi decide le forme del pacchetto e del grumo** *(oggi sono negli strumenti di `csv/`)*?
4. ### **`eps`: dalla tabella** *(`scena_l2.EPS_MONETA`)* ### **e mai dal file?** ### **E allora le misure a `eps` diverso** *(che oggi gli strumenti fanno in memoria)* ### **restano negli strumenti?**
5. ### **`CAMM-MATERIA-VUOTO` saltato** *(come fa `csv/_triangoli.camminata`)* ### **o acceso nel driver?** ### **E se si salta, e' un CAMPO** *(`salta`)* ### **o una configurazione di servizio?**
6. ### **`cs`: la forma acceso o spento, e `lambda_c`** *(non deciso)*: ### **nel file, e obbligatorio?**
7. ### **Il timbro della camminata come al §5: basta, o anche le impronte di `csv/` usati per lo stato iniziale?**
