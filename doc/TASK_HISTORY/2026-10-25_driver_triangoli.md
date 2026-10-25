# IL DRIVER SUI TRIANGOLI *(la parte A del mandato delle 20:44)* -- E LA PREMESSA CHE NON TIENE

> **Il mandato:** di Luca, `2026-10-25`, con la decisione `(1)` delle `20:44`: ### **«il driver passa ai triangoli; la catena resta solo per i collaudi di servizio»** *([[DOMANDA-DRIVER-CAMMINATA]], [[RINOMINA-SCENA-QUADRATO]], [[DECISIONE-SOLO-TRIANGOLI]], [[PROGETTO-MITOSI]])*.
> ### **Il sigillo chiesto:** ### **la scena del driver = `scena_l2.scena_toro("triangoli", ...)` AL BIT;** ### **un tick del driver = un tick dello strumento AL BIT;** ### **i collaudi sulla catena invariati; l'impronta intatta; la suite completa.**

**LIVELLO:** una lettura del codice prima di un cambiamento del nucleo.

## 0. LA STELLA POLARE

1. **`A14`:** ### **non si applica** *(nessuna legge cambia)*. 2. **Il gradino:** ### **la scena del driver.** 3. **Aggiunge un numero o una legge?** ### **No.** 4. **Tocca `rho`, `c_s` o il segno?** ### **No.** 5. **Emergente o imposto?** ### **Il reticolo e' imposto, come oggi.**

## 1. IL RAGIONAMENTO PRELIMINARE, DAL CODICE

- ### **CHE COSA FA IL DRIVER OGGI** *(`primo_ordine/driver.py`, letto per nome)*: ### **`gira` costruisce gli archi con `grafo(scena, nodi)`** *(`catena` o `anello`)*, ### **carica i termini di `leggi_attive`** *(`HAM.carica_termini`)* ### **e avanza con `passo.passo_locale` o `passo.passo_globale`** *(un integratore dell'hamiltoniana, coi parametri `dt`, `iterazioni`, `toll` del risolutore)*. ### **Le leggi che `config/prova.yaml` accende sono `PROVA-HOPPING` e `PROVA-LOCALE`, tutte e due `prova: true`** *(`leggi.yaml`: «servono a collaudare la catena ... NON a dire come va il mondo»)*.
- ### ⚠ **LA PREMESSA CHE NON TIENE: IL DRIVER NON FA GIRARE LA CAMMINATA.** ### **Il tick della camminata e' `tick.tick(st, mot, par)`** *(i `14` pezzi di `composizione.ORDINE` su un `Motore`)*, ### **e lo strumento dei triangoli** *(`csv/_triangoli.py`, `scena_l2.scena_toro`)* ### **restituisce `(inc, mot, st, par)` per QUEL tick.** ### **Il driver non costruisce nessun `Motore` e non chiama `tick`:** ### **«un tick del driver = un tick dello strumento» confronta due dinamiche DIVERSE** *(un integratore di un'hamiltoniana di prova contro la camminata a moneta)*, ### **quindi il sigillo come e' scritto non ha un significato.**
- ### **LE DUE LETTURE POSSIBILI, che NON scelgo:**

| | la lettura | che cosa vuol dire nel codice | il costo | che cosa resta del sigillo |
|---|---|---|---|---|
| `(i)` | ### **solo il GRAFO del driver sui triangoli** | ### **una scena nuova nel vocabolario chiuso di `schema_config.SCENE`, costruita con gli archi di `scena_toro(GRIGLIA_DEL_MODELLO, ...)`;** ### **il campo `nodi` non basta, servono i `lati`** *(un campo nuovo nello schema, o `nodi` come `L x L`)* | ### **piccolo;** ### **ma le leggi che il driver fa girare restano quelle di PROVA:** ### **«il driver sui triangoli» farebbe girare un hopping di prova su un toro a triangoli, non la fisica** | ### **la scena al bit si'; il tick contro lo strumento NO** *(non esiste uno strumento della pipeline di prova sui triangoli)* |
| `(ii)` | ### **il driver fa girare la CAMMINATA** *(il modello: `tick.tick` su `scena_toro`)* | ### **una seconda pipeline nel driver, e uno SCHEMA di configurazione diverso** *(`lati`, `dtau`, `x`, `passi`; niente `dt`, `integratore`, `iterazioni`, `toll`, `leggi_attive`: l'ordine dei pezzi viene da `composizione.ORDINE`, la moneta dalla tabella)* | ### **grande, e tocca regole scritte:** ### **«la configurazione e' UNA»** *(`CLAUDE.md` par. `13`)*, ### **il vocabolario CHIUSO dei campi** *(`schema_config.CAMPI`)*, ### **e il timbro** *(`timbro.timbro` conta le leggi di `leggi_attive`)* | ### **tutto il sigillo ha un significato:** ### **la scena al bit, il tick al bit contro `tick.tick` sulla scena dello strumento** |

- ### **PERCHE' NON SCELGO:** ### **`(ii)` cambia che cosa E' il driver** *(da collaudo della catena tabella -> modulo a motore della fisica)*, ### **e lo schema e' scritto come un presidio** *(«un campo in piu' e' un errore»)*: ### **e' una decisione di struttura, non un'esecuzione;** ### **`(i)` esegue la lettera ma non lo scopo** *(un tick sui triangoli confrontabile)*. ### **La regola: se una cosa non torna, DILLO** *(`CLAUDE.md` par. `2`)*.

## 2. LA PROGETTAZIONE

### **Nessun cambiamento del nucleo in questa parte.** ### **La domanda per Luca:** [[DOMANDA-DRIVER-CAMMINATA]] ### **col criterio di chiusura: Luca sceglie `(i)` o `(ii)`** *(o una terza forma)*; ### **con `(ii)`, lo schema della configurazione della camminata e' parte della risposta.** ### **E la voce aperta chiesta dal mandato:** [[RINOMINA-SCENA-QUADRATO]] *(`scena_l2.scena` costruisce il quadrato e il nome non lo dice; `12` strumenti la usano; NON si rinomina in questo giro)*.

## 3. TODO

1. questo task history, le due voci, la relazione: un commit; ### **`FERMO` sulla parte A;** 2. la parte B *(indipendente dal driver)*; 3. le parti C1 e C2 *(strumenti in `csv/`, indipendenti)*.
