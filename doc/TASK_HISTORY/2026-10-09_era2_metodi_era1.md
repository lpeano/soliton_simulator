# ERA `2`, INFRASTRUTTURA (SECONDA PARTE) — **i metodi dell'era `1`, la modularità, i controlli nell'indice, i metadati, i riferimenti, la configurazione**

> ### ⛔ **IL MANDATO HA `16` PUNTI** *(`0`-`15`)*, ed è la **quarta versione** della voce ④ di
> `doc/CODA_2026-10-09.md`: ### **le tre prime sono REPERTI e NON si eseguono**
> *(precedenza registrata in `677685c`)*.

> ### 📌 **IL RITO:** questo file si committa e si pusha ### **PRIMA del lavoro**, così
> l'ordine è ### **verificabile da git** *(questo commit è **antenato** dei commit del
> lavoro)* invece che **asserito da me**.

---

## `1.` RAGIONAMENTO PRELIMINARE — ### **cosa credo PRIMA di guardare, e cosa NON so**

### **IL PRINCIPIO DEL MANDATO, e perché lo riconosco**

> *«Ogni errore è nato da una macchina che leggeva la prosa.»* ### ⛔ **Le decisioni si
> prendono SOLO da campi strutturati a vocabolario chiuso; il testo libero si conserva e si
> protegge, MAI si interpreta per decidere.**

**Non è una frase generica: è il riassunto di sei difetti miei**, e il mandato li elenca.
### **Li confermo tutti e sei** — li ho scritti io, e il guardiano li ha trovati.

### **CHE COSA CREDO PRIMA DI GUARDARE** *(e quindi cosa potrebbe smentirmi)*

| | quello che credo | perché potrebbe essere falso |
|---|---|---|
| `a` | **il punto `12(b)`** *(rinominare `F1`…`F12`)* è ### **il più rischioso di tutti**: quei nomi sono in **decine di messaggi di commit**, che ### **NON si riscrivono** | potrei scoprire che l'`alias` dell'indice risolve già il problema, e che serve ### **meno** lavoro di quanto credo |
| `b` | **il punto `11(a)`** *(«`crescita` e `vuoto` si GENERANO»)* è ### **il più grosso**: oggi quei due file sono **stub**, e il tipo `regola` ### **non è generato** | il generatore ha già `controlla`→`derivata`→`modulo`; una `regola` però ### **non ha una derivata**, quindi la forma potrebbe non riusarsi |
| `c` | **il punto `8`** *(reversibilità)* ### **dovrebbe passare quasi esattamente** per il punto medio implicito, che è **simmetrico nel tempo per costruzione** | ### ⚠ **«dovrebbe» non è «torna»:** il mandato stesso lo dice. E il **locale** ha una composizione palindroma, quindi ### **potrebbe tornare MEGLIO del globale** — o peggio, se le iterazioni del punto fisso non sono simmetriche |
| `d` | **il punto `15(b)`** *(nessun default nascosto)* ### **rifiuterà codice che ho scritto io ieri**: `mezzo_implicito(st, ii, jj, dt, termini, iterazioni=64, toll=1e-14)` ha ### **DUE default** | potrebbe essere che il controllo vada limitato ai **parametri di fisica** e non a quelli del **risolutore** — ### **ma allora il confine va DICHIARATO**, non assunto |
| `e` | **il punto `14(c)`** *(un ID in un commento è vietato)* ### **rifiuterà MOLTI commenti miei** di `primo_ordine/` | li ho contati a occhio e non con uno script: ### **il numero vero lo devo MISURARE prima di promettere una cura** |

### **CHE COSA NON SO, e lo scrivo adesso**

1. ### **quanti metodi dell'era `1` esistono davvero.** Il punto `0` ne elenca una decina per
   nome e poi dice *«e le cure di architettura»*. ### ⛔ **Il censimento lo devo fare IO, con
   uno script, sull'indice** — e il mandato della terza parte dice esplicitamente:
   *«prima di scrivere "N siti", fai TU il censimento e scrivi il numero che hai VISTO»*.
2. ### **se `F1`…`F12` collidono davvero.** Il mandato dice che `F1`-`F3` sono segnaposto e
   `F4`-`F5` difetti. ### **Lo verifico dall'indice, non dalla sua frase.**
3. ### **se il punto `9` *(un solo esecutore)* ha oggi qualcosa da impedire.** Non so se
   esista già uno script che avanza lo stato fuori dallo schedulatore: ### **oggi
   `_collauda_passo.py` chiama `mezzo_implicito` direttamente** — e quindi
   ### **potrebbe essere proprio lui il caso che il presidio deve rifiutare, o l'eccezione
   che va dichiarata.**
4. ### **se il punto `4` *(il veleno)* si può fare senza derivati.** Oggi lo stato è
   ### **solo `psi`**, e ### **non c'è NESSUN derivato da invalidare**: il punto potrebbe
   essere ### **vero e vuoto**, e allora va detto, non simulato.

---

## `2.` PROGETTAZIONE DEL RAGIONAMENTO — ### **i passi, cosa decide ciascuno, e cosa mi farebbe FERMARE**

> ### 📌 **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI.**

### **L'ORDINE, e perché NON è `0`→`15`**

Il mandato elenca i punti; ### **non impone l'ordine di esecuzione.** Lo scelgo per
### **dipendenza**, e lo dichiaro:

| ordine | i punti | perché prima |
|--:|---|---|
| `1` | **`0`** *(il censimento dei metodi)* | ### **è l'unico punto che MISURA invece di costruire**, e dice quanto grande è il resto |
| `2` | **`12`** *(i controlli nell'indice, e il rinominamento)* | ### **ogni presidio nuovo dei punti successivi vuole una VOCE**: farlo dopo vorrebbe dire ### **tornare su ogni presidio** |
| `3` | **`13`** *(metadati e testo libero)* | è ### **il principio del mandato reso codice**, e i punti `14` e `15` ne usano le forme *(citazioni strutturate, vocabolari chiusi)* |
| `4` | **`14`** *(`@rif`)* | usa gli ID **già rinominati** dal `12` |
| `5` | **`15`** *(la configurazione)* | il punto `5` e il `6` *(timbro, salva-riprendi)* vogliono ### **l'impronta della configurazione**, che prima non esiste |
| `6` | **`1`-`4`, `11`** *(domini, nessun ramo, nascita, veleno, modularità)* | toccano ### **il generatore e i moduli di fisica**, e `11(a)` chiede di ### **generare `crescita` e `vuoto`** — cioè il tipo `regola`, che oggi non c'è |
| `7` | **`5`, `6`, `9`, `10`** *(timbro, salva-riprendi, un solo esecutore, conto delle leggi)* | vogliono tutto il resto in piedi |
| `8` | **`7`, `8`** *(il modello di sigillo, la reversibilità)* | ### **sono i due che MISURANO FISICA**, e vanno per ultimi perché usano il timbro e la configurazione |

### **LE LETTURE, FISSATE ADESSO** *(prima di vedere i numeri)*

| | la misura | la lettura che fisso PRIMA |
|---|---|---|
| **`8`** reversibilità, **GLOBALE** | `k` passi avanti e `k` indietro | ### **passa se** l'errore relativo sullo stato è `< 1e-9` a `k = 50`, `dt = 0.01`. ### ⚠ **E mi aspetto che il globale sia PEGGIORE del locale**, perché il punto fisso ha una tolleranza che ### **non è simmetrica nel tempo** |
| **`8`** reversibilità, **LOCALE** | idem | ### **passa se** `< 1e-9`. ### **E se il locale NON fosse migliore del globale, è un ritrovato** — vorrebbe dire che la composizione palindroma ### **non compra la reversibilità che promette** |
| **`8`** il caso che DEVE fallire | lo stesso giro con un integratore ### **non simmetrico** *(Euler esplicito, scritto SOLO per questo)* | ### **DEVE** dare un errore `> 1e-3`: altrimenti ### **la misura non distingue un metodo simmetrico da uno che non lo è**, e il braccio è un `FALSO-UNO` |
| **`2`** nessun ramo | il generatore su un termine con `Max(...)` | ### **DEVE** rifiutare, ### **e NON deve rifiutare** le due leggi di prova |
| **`14(c)`** ID nei commenti | il conteggio sui file di `primo_ordine/` | ### **nessuna lettura da fissare: è un CENSIMENTO.** Il numero si scrive ### **dopo averlo visto**, e non prima |

### **CHE COSA MI FAREBBE FERMARE** *(e dove lo scrivo)*

| | il caso | che faccio |
|---|---|---|
| `a` | il punto `8` **fallisce** *(nessuno dei due integratori torna)* | ### ⛔ **FERMO.** Sarebbe una violazione misurata di `A16`, e ### **non è una cura ovvia**: committo lo stato e il fallimento |
| `b` | il rinominamento del `12(b)` tocca un **reperto** | ### **NON lo riscrivo** *(par.9: i reperti non si riscrivono)*: il nome vecchio resta e si risolve con l'`alias`. ### **Se un reperto diventasse illeggibile, FERMO** |
| `c` | il punto `11(a)` chiede una **decisione di fisica** *(come si genera una `regola`: che forma ha il suo «bilancio»)* | ### **la registro in `doc/indice/DA_DECIDERE_LUCA.md`** e ### **proseguo col mandato successivo**, come Luca ha autorizzato |
| `d` | il punto `15(b)` vorrebbe **togliere i default di `mezzo_implicito`** | ### **è una decisione di confine** *(risolutore contro fisica)*: la **dichiaro nel referto** e, se il resto non ne dipende, ### **proseguo** |
| `e` | un collaudo fallisce e **la cura È ovvia** | ### **la faccio, in un commit a sé** *(par.5: la correzione è un commit a sé)* |

### ⛔ **E UNA COSA CHE NON FARÒ, e la dichiaro prima di cominciare**

Il mandato dice *«ogni presidio collaudato nei due versi»*. ### **Nei DUE versi significa:
che scatti dove dico, E che TACCIA dove dico.** ### ⚠ **Un braccio che prova solo il primo
verso è esattamente il difetto che ho fatto con `F1` e `F8`** — il collaudo provava che la
regola scattasse dove dicevo io, ### **non che la regola fosse giusta.**
### ✔ **Quindi ogni presidio nuovo ha ENTRAMBI i bracci, e dove non li ha lo scrivo.**

---

## `3.` TODO DEL NEXT STEP — ### **la lista OPERATIVA**

- [ ] **`0`** — `doc/METODI_era1_in_era2.md`, ### **dal CENSIMENTO** *(script, non a occhio)*: una riga per metodo *(come si applica · dove · stato)*, e il presidio che ### **rifiuta un metodo citato senza riga**
- [ ] **`12`** — `(a)` ogni controllo una **VOCE** + `PRESIDIO = "<id>"` letto via AST, biiezione · `(b)` ### **il rinominamento di `F1`…`F12`** con `alias`, e i reperti intatti · `(c)` ogni sigillo dichiara `LEGGE` e `CRITERI`
- [ ] **`13`** — `(a)` vocabolari chiusi + chiavi di metadato registrate · `(b)` ### **un controllo BLOCCANTE non legge testo libero** *(e il referto dichiara quali segnalano)* · `(c)` ogni campo di testo cambia **solo con una riga di storico con la sua impronta**, e il replay a **tutti** i registri · `(d)` ### **citazioni STRUTTURATE** `{file, riga, commit, impronta}`, verificate su `git show` · `(e)` UTF-8 normalizzato · `(f)` i generati ### **byte-identici**
- [ ] **`14`** — `primo_ordine/_rif.py` *(`@rif` e `rif()`, ### **byte-inerti, COLLAUDATO**)* · il divieto di ID nei commenti · ### **la vista inversa generata** · `indice.py rinomina` · nessun numero di riga
- [ ] **`15`** — `primo_ordine/config/<nome>.yaml` + schema · ### **nessun default nascosto** *(AST)* · ### **niente interruttori per le leggi** · i confronti `A`/`B` col **campo unico** · i dati con **versione**, **scrittura atomica**, reperti immutabili
- [ ] **`1`**-**`4`**, **`11`** — domini che ### **FERMANO** · ### **nessun ramo nei termini** *(`Min`, `Max`, `Piecewise`, `clip`, `Abs` con soglia)* · la **nascita in un solo punto** · il **veleno** · la **modularità** *(`_mappa.yaml`, tetto di righe, una riga di responsabilità)*
- [ ] **`5`**, **`6`**, **`9`**, **`10`** — il **timbro** · **salva e riprendi** che ### **RIFIUTA se la tabella è cambiata** · ### **un solo esecutore** · il **conto delle leggi**
- [ ] **`7`**, **`8`** — il **modello di sigillo** *(`primo_ordine/sigilli/_modello.py`)* · la ### **REVERSIBILITÀ**, con ### **entrambi** gli integratori e ### **il caso che deve fallire**
- [ ] **il referto**, e `doc/indice/_avanzamento.md` aggiornato
