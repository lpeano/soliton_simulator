# IL SIMULATORE DELL'ERA `2` — **il piano dei pezzi, PRIMA del codice**

> ### ⛔ **QUESTO FILE SI COMMITTA *PRIMA* DEL CODICE** *(par.8)*, e il mandato lo ripete:
> *«la task history del simulatore, prima del codice»*. ### **Le soglie si fissano QUI.**

**Mandato:** `[[SIMULATORE-ERA-2]]` punto `(b)`, riordinato da Luca il `2026-10-12`
*(`979ad60`)*: ### **il simulatore viene PRIMA della derivazione.**
**L'architettura:** `[[ARCHITETTURA-ERA1-RIUSATA]]` *(`50a2d83`)*.
**La fisica:** `[[CARTA-FISICA-SIMULATORE]]` — `F1`..`F10` decisi, `A1`..`A5` posti
dichiarati.
**Il vincolo:** `[[MEMORIA-PER-TICK]]`, dal **primo** commit di codice.

---

## 1. RAGIONAMENTO PRELIMINARE — *che cosa c'e', che cosa manca, e dove sbaglierei*

### ✅ **LO STATO DI PARTENZA, misurato adesso e non ricordato**

| | |
|---|---|
| `python primo_ordine/collauda.py` | ### **`40` su `40` passano** |
| `python csv/indice.py valida` | ### **passa** |
| `leggi.yaml` | ### **`3` leggi, TUTTE `prova: true`** " cioe' ### **ZERO leggi vere** |
| i tipi di legge | `termine_nodo` · `termine_arco` · `regola` · `osservatore` |
| i tipi di variabile | `complesso_c2_nodo` · `reale_nodo` · `reale_arco` · `fase_arco` · `coppia_coniugata` *(ammessa e **non usata**: decisione `13`)* |
| ### ⚠ **il `pre-commit` costa `151.4` s** | oltre il budget di `120`, e il collaudo lo dice: ### **un presidio che si spegne perche' costa troppo NON E' UN PRESIDIO** *(`A9`)* |

### ⛔ **E IL DISALLINEAMENTO CENTRALE, che non risolvo di nascosto**

> **`complesso_c2_nodo` dice *«`psi`, `C²` sul NODO»*. ### Ma `F1` dice *«stato sulle
> ESTREMITA' d'arco»*.**

### **Non e' una scelta di fisica: `F1` e' DECISO.** E' una **estensione dello schema** che
`F1` **pretende**, e va fatta: servono **`complesso_c2_estremita`** *(`psi` in `C²` per
estremita')* e **`reale_estremita`** *(`phi`)*. ### ⚠ **Ma la FORMA dell'estensione e' una
scelta di progetto mia, e la dichiaro** *(sotto, `P1`)*.

### ⛔ **E IL SECONDO DISALLINEAMENTO, piu' profondo**

> **I pezzi del passo della camminata NON SONO termini di `H`.**

La moneta di spin, il Grover, lo spostamento con trasporto sono ### **operatori UNITARI**,
non addendi di un'hamiltoniana: si **compongono**, non si **sommano**. ### **Lo schema di
oggi sa esprimere `H` e non sa esprimere una COMPOSIZIONE.** Serve un tipo nuovo
*(`pezzo_unitario`)* e un tipo per i flussi esatti *(`flusso`)*, piu' l'**ordine di Strang
dichiarato in tabella**.

### **CHE COSA NON SO, e dove mi aspetto di sbagliare**

1. **se il criterio di passaggio AL BIT sia raggiungibile** con la scrittura in-place: un
   `out=` cambia **dove** si somma, non **come**, ma `numpy` puo' scegliere un percorso
   diverso " e allora la differenza e' di **ulp**, non di algebra. ### **Non lo so, e si
   MISURA: il numero di ulp si conta, non si assume.**
2. **quanto costa davvero la struttura `CSR` con il raddoppio**: il tetto `m1` l'ho fissato
   a `4` volte lo stato **per un conto di progetto**, non per una misura;
3. **se l'ordine di Strang vada in tabella come LISTA o come CAMPO di ogni pezzo**: la
   prima dice *«l'ordine e' una legge»*, la seconda *«ogni pezzo sa dove sta»*. ### **La
   prima mi sembra giusta perche' l'ordine e' UNO, ma non ho un argomento che chiuda.**

---

## 2. IL PIANO DEI PEZZI — **sei, e ognuno col suo commit**

| | il pezzo | che cosa produce | come si verifica |
|---|---|---|---|
| `1` | ### **questa task history** | il piano e le soglie | l'ordine e' **verificabile da git** |
| `2` | lo **SCHEMA** | i tipi sulle estremita' *(`psi` in `C²`, `phi`)*, la struttura fissa *(archi in array, vicini in `CSR` con capacita' che raddoppia)*, i tipi di legge `pezzo_unitario` e `flusso`, l'**ordine di Strang** in tabella | lo schema **rifiuta** cio' che non rispetta la forma, e un collaudo lo prova **nei due versi** |
| `3` | la **TABELLA** | `F1`..`F10` come leggi, `A1`..`A5` come **posti dichiarati** al comportamento attuale | la **biiezione** legge ↔ file ↔ voce ↔ scheda *(`P-E1`, che c'e' gia')* |
| `4` | il **GENERATORE** | il codice sotto `termini/`, e il ### **presidio VERO** che rifiuta di accendere un posto aperto **senza la sua voce di decisione** | un collaudo che prova ad accendere un posto **senza voce** e verifica che il generatore ### **RIFIUTI** |
| `5` | il **MOTORE** | doppio contenitore, scrittura in-place, punto unico di scrittura, cache **che portano la taglia**, contatori dei ripieghi, checkpoint e ripresa, salvataggio durante la corsa | i collaudi `m1`..`m4` e il determinismo fra **due processi** |
| `6` | il **CRITERIO DI PASSAGGIO** | il confronto col banco congelato | `s1`..`s4` qui sotto |

---

## 3. LE SOGLIE — **fissate QUI, e nessuna si tara dopo**

### ⭐ **LA MEMORIA** *(dal censimento, `[[MEMORIA-PER-TICK]]`)*

| | la soglia | come si misura |
|---|---|---|
| `m1` | la memoria della **scena** sta ### **entro `4` volte lo stato** | privata **dopo** la costruzione meno **prima**, su **due** taglie |
| `m2` | il rapporto fra due taglie e' ### **stabile entro il `20%`** | cioe' **proporzionale agli archi** |
| `m3` | la memoria **per tick** e' ### **piatta** *(pendenza compatibile con `0` a `3 sigma`)* | la via che la diagnosi usa gia' |
| `m4` | tutte e tre si ### **TIMBRANO con la corsa**, col costo per tick | " |

### ⛔ **IL CRITERIO DI PASSAGGIO**

| | la soglia | la mia previsione |
|---|---|---|
| `s1` | sulle scene del banco *(regolare, irregolare, cubico, geometrico)* il passo generato da' ### **`max|psi_gen − psi_banco| = 0` ESATTO** | ### **non lo so**: dipende dal `(2)` sopra |
| `s2` | se non e' `0`, si riporta ### **in ULP**, contati e non stimati, e ### **si DICHIARA l'operazione che li introduce** | se c'e' una differenza, ### **e' nello spostamento con trasporto** *(e' il pezzo con l'`einsum`)* |
| `s3` | la **norma** si conserva come nel banco: ### **stessa scala di errore**, non *«piccola»* | `~10^-14` su `2m` estremita' |
| `s4` | e il **passo inverso** ricompone lo stato: ### **relativo a `64 eps`** | regge, come nel banco |

### ⚠ **E UNA SOGLIA CHE NON SCRIVO, e dico perche':** non metto una soglia sul
**TEMPO** del passo generato. ### **Il tempo di una macchina non e' una proprieta' del
repo** " e il collaudo dell'era `2` lo dice gia' del `pre-commit`. ### **Si MISURA e si
TIMBRA, e non rifiuta.**

---

## 4. I POSTI DICHIARATI — **`A1`..`A5` piu' TRE miei**

### ⛔ **I CINQUE DELLA CARTA, al comportamento attuale**

| | il posto | comportamento attuale |
|---|---|---|
| `A1` | tempo proprio locale, forma di `cs`, come la materia scrive su `Lambda` | ### **`cs = 1`**, come il `v3` |
| `A2` | `U` dinamica, criterio di mitosi, connessione del nato, ridistribuzione | ### **SPENTE** |
| `A3` | la grandezza conservata da promuovere a energia | ### **nessuna promozione** |
| `A4` | segno della saturazione e via del campo | ### **segno diretto**, come il `v3` *(e la **via del campo** e' ora **decisa**: `[[DOMANDA-VIA-DEL-CAMPO]]`)* |
| `A5` | versori relazionali | ### **versori della scena**, provvisori |

### ⭐ **E TRE POSTI CHE NASCONO DA QUESTO PIANO, dichiarati adesso perche' sono MIEI**

| | il posto | il comportamento che metto, e perche' |
|---|---|---|
| `P1` | **la forma dei tipi sulle estremita'**: `complesso_c2_estremita` come **tipo nuovo**, oppure `complesso_c2_nodo` con un **campo `dominio: estremita`** | metto il ### **tipo nuovo**, perche' il dominio decide ### **quanti simboli** esistono e ### **quali lati** *(`i`/`j`)* ha una legge " e nascondere quella differenza in un campo la renderebbe ### **invisibile all'ambiente** |
| `P2` | **l'ordine di Strang**: una **lista** in tabella, oppure un **campo per pezzo** | metto la ### **lista**, perche' l'ordine e' ### **UNO** e una lista si legge in un posto " ### ⚠ **ma non ho un argomento che chiuda, e resta un posto** |
| `P3` | **la crescita della `CSR`**: raddoppio, oppure ricostruzione a evento | metto il ### **raddoppio**, per il conto del censimento *(`O(m)` ammortizzato contro `O(m²)`)* " e il ### **prezzo** *(fino al doppio)* sta ### **dentro `m1`** |

### ⛔ **E LA REGOLA CHE IL MANDATO MI DA' E CHE SEGUO:** se un pezzo richiede una scelta
di fisica **non gia' decisa**, ### **NON la scelgo**: diventa un posto dichiarato e vado
avanti.

---

## 5. LA STELLA POLARE — **le cinque risposte, PRIMA del codice** *(`L-STELLA`)*

| | la domanda | la risposta |
|---|---|---|
| `1` | **`A14`: conserva energia e carica LOCALMENTE?** | ### **La CARICA si', per costruzione:** ogni pezzo del passo e' ### **UNITARIO**, e la composizione di unitari e' unitaria " quindi `|psi|` e `|phi|` si conservano ### **separatamente**, e il criterio `s3` lo ### **misura** invece di dedurlo. ### ⚠ **E l'energia NON si nomina:** `A3` e' un posto dichiarato, e la grandezza conservata ### **si chiama col suo nome** |
| `2` | **a quale dei TRE GRADINI arriva?** | ### **`(a)` robusto: SI'**, le soglie sono significativita' e ulp contati. ### **`(b)` regge togliendo la legge pratica: E' IL CRITERIO DI PASSAGGIO** " coi posti al comportamento attuale il generato ### **E'** il `v3`. ### ⛔ **`(c)` coincide con un limite noto: SI', ed e' il piu' forte che ho** " il ### **banco congelato**, al bit |
| `3` | **aggiunge un numero o una legge?** | ### ⭐ **NESSUN NUMERO NUOVO.** Le leggi `F1`..`F10` sono ### **quelle del banco, riscritte in tabella**: il conto delle leggi ### **non sale**, e `9-ter` e' rispettato perche' la tabella ### **TOGLIE** una duplicazione *(oggi la stessa fisica vive in `proto_camminata/` **e** in `primo_ordine/`)*. ### ⚠ **E aggiunge TRE POSTI** *(`P1`..`P3`)*, che sono ### **di progetto e non di fisica** |
| `4` | **tocca `rho`, `c_s` o il SEGNO?** | ### **Nessuno dei tre:** `cs = 1` e il segno ### **diretto** sono i **comportamenti attuali** dei posti `A1` e `A4`, cioe' ### **quelli del `v3`** " e il criterio di passaggio ### **pretende che lo restino** |
| `5` | **emergente o imposto?** | ### ⛔ **QUESTO PEZZO NON FA EMERGERE NIENTE, e dirlo e' importante:** porta in tabella una fisica ### **gia' misurata**. ### **Cio' che deve emergere** *(il legame col campo, lo spazio che nasce)* ### **viene DOPO**, ai punti `(a)` e `(d)` dell'ordine. ### ⭐ **E il controllo che PUO' fallire e' il criterio di passaggio stesso:** se il generato ### **non** riproduce il banco, ### **il porting e' sbagliato** " e lo dice un numero |

---

## 6. TODO DEL NEXT STEP

| | il passo | cosa mi FERMA |
|---|---|---|
| `1` | committare e pushare **questo file** | " |
| `2` | lo **schema**: i due tipi di estremita', `pezzo_unitario`, `flusso`, l'ordine di Strang | se lo schema non riesce a ### **rifiutare** una forma sbagliata ⟹ **FERMO** |
| `3` | la **tabella** `F1`..`F10` | se una legge chiede un numero che non ho ⟹ ### **posto dichiarato**, non una scelta |
| `4` | il **generatore** e il suo **presidio vero** | se il presidio ### **non impedisce** ⟹ **FERMO**: sarebbe `A9` di nuovo |
| `5` | il **motore** e i collaudi `m1`..`m4` | `m1` oltre `4` volte lo stato ⟹ **FERMO** e si guarda dove |
| `6` | il **criterio di passaggio** `s1`..`s4` | `s1` diverso da `0` **senza** che `s2` sappia dire **quale operazione** ⟹ **FERMO** |

### ⛔ **E LA COSA CHE NON FARO': TOCCARE IL BANCO.** `[[BANCO-CONGELATO]]` dice che
`proto_camminata/` e' un ### **riferimento**: il criterio di passaggio lo ### **legge**,
e non lo cambia ### **nemmeno di un byte.**

---

## ✅ **ANNOTAZIONE: IL POSTO `P2` E' CHIUSO — L'ORDINE DI STRANG E' UNA LISTA** *(argomento del guardiano, accettato da Luca, `2026-10-12`)*

### ⭐ **L'ARGOMENTO CHE CHIUDE, e si regge da solo:** la composizione di Strang usa ### **LO STESSO PEZZO DUE VOLTE** — `N(dtau/2)` → passo lineare → `N(dtau/2)`. ### ⛔ **Un CAMPO PER PEZZO non puo' esprimere un pezzo che compare due volte:** un campo dice *«questo pezzo sta al posto `k`»*, e un pezzo che sta ### **a due posti** vorrebbe ### **due valori nello stesso campo.** ### ✅ **Una LISTA lo esprime senza sforzo**, perche' una lista ### **ammette ripetizioni.**

### 📌 **E IL SECONDO ARGOMENTO E' UN'ANALOGIA, e la dichiaro per quello che e':** il guardiano cita `A10` *(«una sola fonte dell'ordine»)*. ### ⚠ **`A10` parla letteralmente dei DOMINI DELLA FISICA** — *«dove due domini devono parlarsi il PONTE dev'essere UNO SOLO»* — quindi qui ### **non e' una prova, e' una somiglianza di forma**: la lista e' ### **un ponte solo**, i campi sparsi sono ### **tanti ponti che possono contraddirsi.** ### **La somiglianza regge, ma il lavoro lo fa il primo argomento.**

### ⛔ **QUINDI `P2` NON E' PIU' UN POSTO DICHIARATO: E' DECISO.** L'ordine di composizione va in tabella come ### **UNA LISTA**, e lo schema ### **deve ammettere le ripetizioni** — cioe' ### **un collaudo verifica che una lista con lo stesso pezzo due volte PASSI**, e che l'assenza dell'ordine ### **RIFIUTI.**

### ✅ **E I POSTI MIEI SCENDONO DA TRE A DUE:** restano `P1` *(i tipi di estremita' come tipo nuovo)* e `P3` *(la crescita col raddoppio)*. ### **Entrambi hanno il loro argomento; quello di `P2` me l'ha dato il guardiano.**

