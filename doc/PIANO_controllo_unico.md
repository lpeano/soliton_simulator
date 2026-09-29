# 🧭 **IL PIANO: IL CONTROLLO UNICO DELLO SCHEDULATORE** *(`RIPIEGHI-ZERO`, 2026-09-29)*

> **Mandato di Luca:** *«La cura dei ripieghi e' il **CONTROLLO UNICO** dello schedulatore, non
> guardie sparse. Nella fase "apri" di ogni passo e subito dopo mitosi: ogni grandezza del
> **REGISTRO** ha lunghezza **ESATTAMENTE `n`** (ne' corta ne' lunga), altrimenti
> `CacheCorta`/`CacheLunga` **con il nome**. Il registro dichiara per ogni grandezza la **regola di
> nascita** (eredita / media / zero / estrazione nuova). Poi le guardie di **sostituzione** dentro
> le leggi si **TOLGONO**; restano solo le vere **inizializzazioni**, separate dagli `OR`.»*

### ⚠ **QUESTO E' UN PIANO: NON C'E' UN BYTE DI FISICA.** Blob del simulatore **`f7541d03`**.
**Ogni numero viene da `doc/REGISTRO_grandezze.md`**, generato da
`csv/_test_fork/_registro_grandezze.py` — **rigirabile**, non ricopiato *(`L-NUMERI`)*.

---

## 1. IL REGISTRO — e ### **una distinzione che il mandato non prevede**

| | per NODO | per ARCO |
|---|---|---|
| grandezze trovate **in automatico** | ### **32** | ### **11** |
| **con** una regola di nascita | **22** | **9** |
| ### **SENZA** regola di nascita | ### **10** | ### **2** |
| di cui la regola e' **DA DECIDERE** | **9** | **5** |
| *«incoerenti nello stesso evento»* | **3** | **3** |

**`32` per nodo sono le `31` della prova a guasto PIU' `phi`**, che non e' un membro: ### **`n` E'
`len(phi)`** *(property `:2063`)*, quindi `phi` e' **il metro**. `m = len(i) = len(j) = 471564`, e
### **zero grandezze ambigue**: `n` e `m` non possono coincidere, quindi la divisione nodo/arco
**non richiede una mia scelta**.

### ⛔ **Le 10 (+2) senza regola di nascita NON sono buchi: sono DERIVATE — e qui il mandato si rompe**

Le ho **lette a mano**, una per una. **Ognuna ha UNA sola scrittura, a piena lunghezza:**

| grandezza | dove nasce | che cos'e' |
|---|---|---|
| `_chi_core_nodi` `_chi_core_rho0` `_chi_core_raggio` `_chi_geom_nodi` | `:2556`-`:2561` `chiralita_core_locale` | **ricalcolate su tutta la rete** |
| `_deg` | `:2066` `_grado` — `bincount` su `n` | **ricalcolata** |
| `_r_corrente` | `:5577` `step` | **ricalcolata** |
| `_g_rampa_prec` | `:4308` `_pesi` | **fotografia della rampa** |
| `_fatt_cs_ultimo` | `:3757` `_passo_spinoriale` | ### **ricalcolata, e il codice dice «DIAGNOSTICO: nessun lettore (Z7)»** |
| `_xi_rumore` | `:3642` `_passo_spinoriale` | ### **il rumore OU — e il figlio NON lo eredita** *(vedi par.4)* |
| `conc_nodi` | `:2058` `__init__`, `.extend` a `:3193` | ### **e ha una AUTO-RIPARAZIONE che TRONCA** *(par.4)* |
| `_dt_e_ultimo` *(arco)* | `:5570` `step` | **ricalcolata** |
| `_sin2_vir` *(arco)* | `:7176` `memoria_hebbiana_moto` | **ricalcolata** |

> ### 📌 **LA CONSEGUENZA, e va detta prima di scrivere il codice: applicare il controllo a TUTTE
> ### E 32 FERMEREBBE UN RUN SANO ALLA PRIMA NASCITA.**
> `mitosi` fa crescere `n` a `:664x` / `:680x`. Una grandezza **derivata** non viene allungata li' —
> viene **riscritta per intero** dalla sua legge, che nella composizione gira **prima** di `mitosi`
> *(`step`)* oppure **al passo dopo**. ### **Quindi al punto «subito dopo mitosi» e' CORTA per
> costruzione, e legittimamente.** E anche all'`apri` del passo seguente, perche' `apri` viene
> **prima** di `step`.

### ➜ **Il registro deve dichiarare DUE CLASSI, non una:**

| classe | che cos'e' | il controllo |
|---|---|---|
| ### **STATO** | ha una **regola di nascita**: si eredita, si media, si azzera o si estrae | ### **`len == n` ESATTAMENTE, ai due punti. Altrimenti `CacheCorta`/`CacheLunga` col nome** |
| ### **DERIVATA** | **ricalcolata a piena lunghezza** dalla sua legge; la sua lunghezza **fra due ricalcoli non e' un invariante** | ### **NON si controlla ai due punti.** Si controlla che **la sua legge la riscriva prima che qualcuno la legga** |

### ⚠ **E la classe non si assegna per fede: si MISURA, ed e' il passo ① del lavoro.**
La sonda *(nessun guasto, solo osservazione)*: su un passo **con nascita** registrare `len(x)` di
tutte e 43 le grandezze **ai due punti di controllo**. ### **La predizione, scritta ORA:** le 22+9
di **STATO** sono `== n`; le 10+2 **DERIVATE** sono **corte**. ### **Se una di STATO risulta corta,
quella e' un BUCO VERO e va curata PRIMA del controllo** — senno' il controllo la trova e ferma un
run sano.

---

## 2. LE REGOLE DI NASCITA — e ### **le «incoerenze» sono DUE EVENTI, non un difetto**

Il registro le **propone dal codice** e **riporta sempre l'espressione**: cio' che non e' evidente
resta **DA DECIDERE**. **Chiare oggi:** `eredita` per `_cs_nodo_prev` `_nb` `_nb_prec` `_nb_ret`
`_psi_prec` `_psi_spin_prec` `psi_spin` `rho_spin` `twp` · `media` per **`psi`** *(la cura del
2026-09-28)* e `phivel` alla mitosi · `zero / costante` per `eta` `mem_mot` `perc_tw` e per quasi
tutto cio' che nasce in `_allaccia`.

### ⛔ **Sei «INCOERENTI» — e per almeno una l'incoerenza E' MIA, non del codice**

`phi_s` `phivel` `pos` *(nodo)* · `_rep` `peq` `vd` *(arco)*. ### **Tutte e sei hanno i due siti
`:664x` e `:680x`**, cioe' **la MITOSI VERA** e **il canale di SCHWINGER** — che stanno **nella
stessa funzione** e che il mio strumento percio' conta come **un solo evento**.

> ### **E il codice dice, DICHIARANDOLO, che sono due eventi diversi:**
> *«[peq-nascita-locale] gli archi della creazione di coppia alla **Schwinger** nascono con `nan` e
> vengono CALIBRATI da `step()` … **L'eredita' della MITOSI non si tocca: un arco che si spezza non
> nasce, CONTINUA.»***
> ### ➜ **Due regole diverse perche' sono DUE NASCITE DIVERSE: una divisione non e' una creazione
> di coppia.** L'etichetta *«incoerente»* e' **sbagliata**, ed e' sbagliata **per la stessa forma
> d'errore delle altre volte**: ho scelto la **grana** sul confine di una **funzione** invece che
> su quello di un **evento fisico**.

### ➜ **Proposta: il registro dichiara QUATTRO eventi** — `semina` · `divisione` · `Schwinger` ·
`allaccio` — con una regola **per evento**. ### **Cosi' le sei «incoerenze» si risolvono senza
aggiungere una legge** *(`9-ter`)*: le leggi ci sono gia', **mancava solo la dichiarazione**.

---

## 3. I PUNTI DELLO SCHEDULATORE

### ✅ **Due risposte che il codice ha gia' dato**

| | |
|---|---|
| la fase **`apri` ESISTE** | e' il **primo** elemento di `PASSO_COMPOSIZIONE` *(`:866`)*, tipo `fase`, dietro c'e' `net._smp_apri`. ### **Il punto di controllo NON e' una fase nuova** |
| e c'e' un **precedente esatto** | `esegui_passo` *(`:1080`)* ha **gia'** una precondizione dello schedulatore: `_ferma_se_oltre_max_nodi(net.n, 0, 'schedulatore: inizio del passo')`, messa **prima del ciclo** perche' ### *«un passo che non si puo' fare NON COMINCIA»* |

### La proposta: **`B`**, e costa **zero leggi nuove**

| | dove | perche' li' |
|---|---|---|
| **① l'`apri`** | in **`esegui_passo`, prima del ciclo**, accanto a `_ferma_se_oltre_max_nodi` | e' una **PRECONDIZIONE**, e una precondizione ### **non deve muoversi con una voce**: `H-ETC-2` **permuta** la composizione, e un controllo dentro `_smp_apri` si sposterebbe con lei |
| **② dopo la mitosi** | **dentro il ciclo**, subito dopo che la voce `'mitosi'` ha girato | e' il **solo** punto del passo in cui `n` cresce |

### ⚠ **E una differenza dal mandato alla lettera, che dichiaro invece di nasconderla:** Luca dice
*«nella fase "apri"»*; io propongo **al momento dell'`apri`, dallo schedulatore**. ### **Se intende
letteralmente dentro `_smp_apri`, si fa cosi' e il piano cambia di una riga** — ma allora il
controllo **si sposta quando la composizione si permuta**, e va detto.

### L'alternativa `A`, e perche' NON la scelgo

Due **voci nuove** nella composizione *(`verifica_registro_apri`, `verifica_registro_mitosi`)*,
tipo `osservatore` come `verifica_invarianti`. ### **Piu' pulita** *(la composizione resta un
DATO, zero nomi cablati nello schedulatore)*, ### **ma costa DUE VOCI NUOVE** nel registro del
passo — e `valida_composizione` **vieta i duplicati** *(regola 4)*, quindi non se ne puo' usare una
sola due volte. ### ➜ **Per `9-ter`, a parita' di effetto vince la variante con MENO leggi: `B`.**

### La forma del controllo

`_ferma_se_registro_incoerente(net, dove)`: scorre **il registro**, e per ogni voce di **STATO**
confronta `len` con `n` *(o con `m`)*. Piu' corta → **`CacheCorta`** col **nome**; piu' lunga →
**`CacheLunga`** col **nome**. ### **`CacheLunga` e' una classe NUOVA, e serve:** la cura del
2026-09-28 comincia con `if quanta >= n: return`, quindi ### **il lato LUNGA e' scoperto** — lo ha
mostrato la prova a guasto *(`psi` LUNGA da' un `ValueError` di broadcast)*.

### ⚠ **E un campo che il mandato non prevede: `puo_essere_assente`**

**«Assente» non e' «di lunghezza sbagliata»** — ed e' la distinzione che Luca mi ha **imposto** in
`lambda_nodi`. `Rete.__init__` crea diverse cache a lunghezza `0` o a `None`, e altre nascono
**pigre**. ### **Un controllo che non distingue i due casi si ferma alla COSTRUZIONE DELLA SCENA:
e' esattamente l'errore che ho fatto in `d14892a5`.**
### ➜ **Serve un quarto campo per voce**, e l'assenza **si CONTA** *(`A8`)*, non solleva.
**Quali possono essere assenti si MISURA** *(passo ② del lavoro)*, non si indovina.

---

## 4. LE GUARDIE DA TOGLIERE — e ### **le tre che NON sono guardie**

I siti stanno in **`doc/RIPIEGHI_classi.md`** *(101 confronti, `(d)` = **58**)*. **Si tolgono le
sostituzioni**; ### **restano le vere inizializzazioni, separate dagli `OR`** *(la condizione fusa
`is None or len(x) < n` si spezza in due, come in `lambda_nodi`)*.

### ⛔ **Ma TRE siti non sono ripieghi, e toglierli CAMBIEREBBE LA FISICA**

| | |
|---|---|
| ### **`_xi_rumore` `:3570`** | il codice lo **dichiara**: *«questo **NON** e' un fallback: e' il **percorso normale della mitosi**; `xi` e' l'**AMBIENTE**, non una proprieta' del nodo, quindi il figlio **NON** lo eredita»*. ### ➜ **E' una REGOLA DI NASCITA — «estrazione nuova» — scritta al sito di LETTURA.** Nel registro si **dichiara**; il ramo **resta** e **conta** *(`A8`)* |
| ### **`conc_nodi` e `_riallinea_tracking`** | `:3274`-`:3275` **allunga E TRONCA** *(`del self.conc_nodi[self.n:]`)*, e il docstring dice *«senza dover patchare ogni singolo punto che crea nodi/archi»* — ### **e' l'ESATTO OPPOSTO del disegno di Luca: una riparazione silenziosa al posto di una regola di nascita.** Chiamata **solo** da `aggiorna_pesi_concorrenza` e `tracking_masse` *(diagnostica)*. ### **Va convertita in regola dichiarata, e la troncatura va MOTIVATA o TOLTA** |
| **`:5750` `step`** | `len(d0) >= n` confronta una grandezza **per ARCO** con il numero dei **NODI**: ### **il ramo non scatta mai**. Non e' un ripiego da togliere, e' ### **un confronto fra due metri diversi, e va corretto o cancellato** |

> ### 📌 **E' il punto che avevo dichiarato PRIMA di guardare** *(`b55514b`)*: **la parte difficile
> non e' togliere le guardie — e' DISTINGUERE la guardia dalla regola di nascita.** ### **Tre su
> tre confermate dal codice.**

---

## 5. I CRITERI DEL SIGILLO — **fissati ORA, prima del codice**

| | criterio | che cosa lo fa FALLIRE |
|---|---|---|
| **A** | ### **la prova a guasto rifatta da' PROTETTO su CORTA E LUNGA per tutte e 31** *(le 32 meno `phi`, che e' il metro)* | **un solo** `INERTE`, `ROTTO RUMOROSO` o `RIPIEGO SILENZIOSO`. ### **«INERTE» NON conta come PROTETTO** |
| **B** | ### **passi SENZA nascite byte-identici sulla scena grande fino al passo 72**, contro `f7541d03`, ### **sul DOMINIO COMUNE** | una sola grandezza diversa. *(Il dominio comune e' obbligatorio: il braccio `E` che sommava su domini diversi l'ho gia' sbagliato una volta.)* |
| ### **C** | ### **IL CASO CHE DEVE FALLIRE** *(`P1-sexies`)*: col controllo **disattivato**, la prova a guasto torna a **`0` su `31`** | se passa anche col controllo spento, ### **il sigillo non sta misurando il controllo** |
| **D** | **controllo positivo sugli ARCHI:** un guasto su una grandezza **per arco** da' **PROTETTO** *(oggi la prova a guasto non le tocca)* | un `INERTE` o un ripiego |
| **E** | **i passi CON nascite girano** fino al 72 **senza** `CacheCorta`/`CacheLunga` | ### **un solo errore su un run sano: vuol dire che ho messo una DERIVATA fra le STATO** |
| **F** | ### **zero `raise` nuovi sparsi:** il conto dei siti di sostituzione **cala**, e il numero di **leggi** non sale *(`9-ter`)* | un controllo che aggiunge guardie invece di toglierle |

### ⚠ **Il criterio `B` e' quello che mi aspetto piu' fragile, e lo dico prima**
Togliere le guardie e' byte-inerte **solo se nessuna scatta in un run sano**. ### **Una misura dice
che DUE scattano** al passo dopo una nascita *(`_rho_sorgente` e `_xi_rumore`, referto `de9c12ed`)*.
Una delle due e' ### **dichiaratamente legittima**. ➜ **Se `B` fallisce, la prima cosa da guardare
e' se ho tolto una regola di nascita credendola una guardia.**

---

## 6. 🛑 **CHE COSA NON DECIDO IO** — e ognuna ha il suo criterio di chiusura

| # | la domanda | che cosa la chiude |
|---|---|---|
| **1** | ### **il registro ha DUE classi (STATO / DERIVATA)?** Senza la distinzione, il controllo ferma un run sano alla prima nascita | la **misura** del passo ①: `len(x)` ai due punti in un passo con nascita. ### **Se le 12 derivate risultano corte, la distinzione serve** |
| **2** | ### **il registro dichiara DUE eventi o QUATTRO?** *(`semina` · divisione · Schwinger · allaccio)* | con **quattro**, le sei «incoerenze» si dissolvono **senza aggiungere leggi**. Con **due**, per sei grandezze **una delle due regole e' un difetto** e va scelta |
| **3** | il **quarto campo** `puo_essere_assente`, con **contatore** invece di errore | la misura del passo ②: quali STATO sono assenti all'`apri` nei primi passi |
| **4** | le **14 «DA DECIDERE»** *(9 nodo + 5 arco: `phi` `phi0` `pos` `omega_s` `perc_chi` `perc_geom` `_psi_spinor` `_spinor_lift` `phivel` · `d` `d0` `i` `j` `tw`)* | le **espressioni** sono in `doc/REGISTRO_grandezze.md`: ### **si leggono e si dichiarano**, una per una. **Non le battezzo io** *(`A1`)* |
| **5** | `apri` **dentro `_smp_apri`** *(alla lettera)* o **precondizione in `esegui_passo`** *(la mia proposta `B`)* | decide Luca. Il costo di ciascuna e' scritto nel par.3 |
| **6** | ### **la TRONCATURA di `_riallinea_tracking`** *(`:3275`)*: si motiva o si toglie? | e' l'unico posto del sistema dove una cache viene **accorciata di proposito**, ed e' in **diagnostica** |
| **7** | `_fatt_cs_ultimo` e' ### **dichiarato «nessun lettore» (Z7)**: sta nel registro o si **archivia**? | se non ha lettori, tenerlo nel registro **aggiunge una voce senza aggiungere una garanzia** |

---

## 7. ⚠ I LIMITI, DICHIARATI

| | |
|---|---|
| ### **il controllo guarda UN SOLO ASSE** | `len` e' il **primo** asse. `pos` `_nb` `_nb_prec` `_nb_ret` `mem_mot` `omega_s` `_xi_rumore` sono `(n,3)`, `_psi_spinor` `_psi_spin_prec` `_spinor_lift` sono `(n,2)`. ### **Un secondo asse sbagliato passerebbe** |
| ### **due punti potrebbero non bastare** | `calcola_psi` riscrive `psi_spin` a `:4421` e `_estendi_psi_spinor` allunga a `:2264`, ### **entrambi a META' PASSO**. Una cache che va corta **fra** i due punti, o **dopo** il secondo, ### **non viene vista** — e la prova a guasto inietta **proprio** fra i due. **Lo avevo dichiarato prima di misurare** *(`b55514b`)* |
| **il grafo delle chiamate e' sui NOMI** | due metodi omonimi verrebbero confusi. Per questo il registro ### **stampa la CATENA**, cosi' ogni voce e' verificabile |
| ### **le LISTE crescono con `.append`, e l'AST non le vede** | `conc_nodi` risulta con **una** scrittura, ma cresce con `.extend` a `:3193` e con l'auto-riparazione. ### **Il registro e' INCOMPLETO per le liste**, e va letto a mano |
| **e' la scena e la configurazione di UN giro** | `nmasse 3`, `sep 6.1158`, seme `11`, passo `30`, ### **zero differenze su 80 booleani** dal driver. Una grandezza che esiste solo con altri flag **non e' in elenco** |
