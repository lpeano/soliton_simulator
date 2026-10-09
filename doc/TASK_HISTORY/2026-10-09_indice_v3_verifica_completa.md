# INDICE `v3`: **le correzioni della VERIFICA COMPLETA del guardiano**

> **Mandato di Luca del 2026-10-09**, sei punti, **un commit per punto**. Nessuna corsa,
> simulatore `b8c21049` intatto.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⛔ **IL FATTO PIU' IMPORTANTE DI QUESTO GIRO, E LO SCRIVO PER PRIMO: IL FILE NON C'E'**

Il mandato dice *«Ti allego `doc/indice/_lotti/correzioni_guardiano_2026-10-09.jsonl` (`165`
righe: `id`, `cambia`, `citazione`, `conf`). Mettilo in quel percorso e committalo PRIMA di
applicare.»*

### **Il file NON e' arrivato.** Ho cercato: ### **nel percorso chiesto** *(non esiste)*,
### **in tutta la storia di git** *(`git log --all -- '*correzioni_guardiano*'`: niente)*, e
### **sul disco** *(`find /c/Users/lpeano -iname '*guardiano*'`: niente)*.

> ### 📌 **E IL PUNTO `3` E' IL FILE.** Non e' un allegato di contorno: e' ### **il lavoro**.
> Senza di esso non si possono applicare ### **`165` righe**, non si sa ### **quali voci sono
> nel file** *(il punto `2` lo chiede: «per quelle che NON sono nel file …»)*, e non si
> possono contare ### **applicate / non applicate / lasciate** *(il punto `6`)*.

### ⛔ **E C'E' UN SECONDO IMPEDIMENTO, PIU' DURO, CHE RIGUARDA L'ORDINE DEL MANDATO**

Il punto `1` dice *«NUOVI PRESIDI, ENTRAMBI ERRORI (validazione bloccante), ### **PRIMA delle
correzioni**»*, e dichiara che ### **`5` voci violano `F9` oggi** *(«sono nel file»)*.

> ### 📌 **`indice.py valida` GIRA NEL `pre-commit`** *(`csv/_hook_presidi.py`, il blocco
> `[INDICE v2]`)*: se torna diverso da `0`, ### **BLOCCA OGNI COMMIT DEL REPO**, non solo le
> scritture sull'indice.
>
> ### ⛔ **Quindi un presidio BLOCCANTE acceso PRIMA della cura non e' «rischioso»: e'
> IMPOSSIBILE.** Il commit che accende `F9` ### **sarebbe bloccato dal suo stesso hook**,
> perche' l'hook gira il codice ### **dell'albero di lavoro**, cioe' il presidio appena
> scritto, su un indice che lo viola ancora. ### **Non esiste un ordine in cui «presidi, poi
> correzioni» funzioni in due commit separati.**

### ⭐ **E QUESTA E' LA TERZA VOLTA IN TRE GIRI.** `F5` *(storico senza commit)* e `F7` *(era
`1` + stato vietato)* hanno dato la stessa lezione: ### **«un presidio bloccante acceso prima
della cura rende inapplicabile il lotto che lo curerebbe»**. ### ⚠ **Le prime due volte l'ho
scoperto SBATTENDOCI. Questa volta lo scrivo prima**, e la lezione nuova e' che
### **il costo non e' l'indice: e' il REPO INTERO.**

### **COSA CREDO, PUNTO PER PUNTO**

| | cosa credo PRIMA di guardare |
|---|---|
| `1` **`F9`** | la forma e' chiara: `ENTRAMBE` ⇒ `APERTA`\|`CHIUSA`, `2` ⇒ `AGENDA`. ### **Credo che violi piu' delle `5` voci nominate**, perche' `era 2` ha `24` voci e il mandato non dice che sono tutte `AGENDA` |
| `1` **`F10`** | `CRITERIO` ⇒ `METODO`: oggi `CRITERIO` sono `90` voci e il dominio `METODO` ne ha `198`. ### **Non so quante violino**, e il mandato ### **non ne nomina nessuna** — se ne violano alcune ### **che non sono nel file, il file non le cura e il presidio resta impossibile da accendere** |
| `2` **«IL FATTO»** | ### **ci credo, ed e' un difetto MIO.** `decidi_stato` cerca la parola `FATTO` con i confini di parola, e ### **«IL FATTO che …» non dice che una cosa e' fatta: introduce una frase.** Lo stesso per `FATTO:` *(due punti)*, che e' ### **un'etichetta di campo**, non un verdetto |
| `2` le sei attese | `SOGLIA-MITOSI-3PI`, `Z23`, `Z46`, `Z56`, `Z66`, `Z74`. ### **Credo che cambino tutte e sei**, e credo che ### **ce ne siano altre** |
| `3` | ### **non eseguibile senza il file** |
| `4` **STANDARD vs PRESIDIO** | ci credo, ed e' ### **la distinzione di `A9`**: un `PRESIDIO` e' cio' che ### **IMPEDISCE**; una regola scritta ### **non impedisce niente** ed e' uno `STANDARD`. ### ⚠ **Credo di aver classificato `PRESIDIO` per PAROLA** — se il titolo dice «presidio» — e ### **non per cio' che il repo fa** |
| `4` **in vigore = `APERTA`** | ci credo, e ### **non e' ovvio:** una regola in vigore «non ha niente da fare», e io ho chiuso ### **cio' che non aveva lavoro residuo.** ### ⭐ **Ma una regola non si «finisce»: VALE** — ed e' la stessa frase degli assiomi del giro scorso |
| `5` **la nota di `G1`** | ci credo: nel giro scorso `G1` e' passata a `CHIUSA` e ### **la `nota_guardiano` dice ancora `SOSPESA`.** Credo che ### **`F6` NON la trovi**, perche' l'ho scritto per le note che parlano di ### **classe e dominio**, non di stato |

### **COSA NON SO** *(e lo scrivo perche' il punto `8` del giro scorso mi ha insegnato che
una soglia scritta male e' peggio di nessuna soglia)*

1. ### **quante voci violano `F9` e `F10` oggi.** E' la prima misura del giro, ed e'
   ### **read-only**;
2. ### **quali delle sei voci del punto `2` sono nel file del guardiano** — e senza il file
   ### **non lo sapro'**;
3. se `F10` viola su voci ### **che il file non nomina**: in quel caso
   ### **il punto `1` e' impossibile anche QUANDO il file arriva**, e va detto a Luca;
4. ### **se il file contiene campi che il mio schema non ha** *(`cambia` e `conf` non sono
   campi dell'indice: sono campi del FILE)*.

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, e cosa mi FERMA*

### ⛔ **L'ORDINE NON E' QUELLO DEL MANDATO, E LO DICHIARO PRIMA DI MUOVERMI**

Il mandato dice *«presidi PRIMA delle correzioni»*. ### **Non si puo'**, per la ragione
scritta sopra: il commit che li accende e' bloccato dal suo stesso hook.
### ➜ **Faccio tutto cio' che e' INDIPENDENTE dal file, lascio i presidi SPENTI e
COLLAUDATI**, e il passo che li accende ### **e' lo stesso commit che applica il file.**

| passo | cosa decide | cosa mi FERMA |
|---|---|---|
| `A` | ### **LA MISURA, read-only:** quante voci violano `F9` e quante `F10` oggi, elencate. Decide ### **se il punto `1` e' possibile QUANDO il file arriva** | niente: e' una lettura |
| `B` | ### **`F9` e `F10` SCRITTI E COLLAUDATI SU COPIA**, e ### **NON inseriti nel validatore vero.** Il collaudo e' quello che il mandato chiede: ### **`F9` DEVE scattare su `A2` a `80eaf82`** | ### ⛔ **se `F9` NON scatta su `A2`**, la regola che ho scritto non e' quella del mandato: mi fermo |
| `C` | ### **IL PUNTO `2`, SOLO CONTROLLO:** la regola corretta di `FATTO` *(non preceduto da `IL`/`il`, non seguito da `:`)*, rigirata sul punto `1` del giro scorso, e ### **l'elenco delle voci che cambiano** | ### ⛔ **se una delle sei attese NON cambia**, la mia regola non e' quella del mandato: ### **mi fermo e lo scrivo**, come nel giro scorso |
| `D` | ### **IL PUNTO `5`:** `F6` cerca la nota di `G1`. Se non la trova, ### **`F6` si estende agli STATI** e si collauda su `G1`. ### **`F6` e' un SEGNALE, non un errore: non blocca niente** | ### ⛔ **se `F6` esteso scattasse su decine di voci**, l'estensione e' troppo grossa: mi fermo e la ridico |
| `E` | ### **IL PUNTO `4`, la parte che NON dipende dal file:** le regole di `CLAUDE.md` §`11` a `STANDARD`, i cablati di §`12` a `PRESIDIO`, e ### **`H-FILE`, `H-NON-TRACCIATI`, `H-STASH` a `APERTA`** *(il mandato li nomina)* | ### ⛔ **`L-SOGLIA` e `STANDARD-4` «sono nel file»**: NON li tocco |
| `F` | ### **IL REFERTO E LA DOMANDA A LUCA** | — |
| `G` | ### ⛔ **NON ESEGUIBILE: il punto `3`** *(il file)*, la parte del punto `2` che distingue «nel file / non nel file», il punto `6` nei suoi conteggi di righe applicate, e ### **l'accensione di `F9`/`F10`** | ### **il file** |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura, fissata adesso |
|---|---|
| `F9` | `str(era) == "ENTRAMBE"` ⇒ `stato ∈ {APERTA, CHIUSA}`; `str(era) == "2"` ⇒ `stato == AGENDA`. ### **Gli stati `DA_CLASSIFICARE` si saltano** *(un segnaposto non ha ancora uno stato, ed e' la stessa scelta del punto `1` del giro scorso)* |
| `F10` | `classe == "CRITERIO"` ⇒ `dominio == "METODO"`. ### **Nessuna eccezione**, e se ne serve una ### **la decide Luca** |
| `FATTO` | conta ### **solo se** non e' precedut0 da `IL`/`il` *(parola intera, immediatamente prima)* ### **e** non e' seguito da `:`. ### **Tutto il resto della regola del punto `1` resta com'e'** |
| una regola «in vigore» | ### **in vigore = citata in `CLAUDE.md` oggi** *(§`11` o §`12`)*. ### ⛔ **Non «mi pare in uso»: si legge dal file** |

### ⭐ **E UNA COSA CHE NON FARO', perche' il giro scorso mi ha insegnato a dirlo prima:**
### **non invento quali voci sono nel file.** Il punto `2` dice *«per quelle che NON sono nel
file del guardiano, rileggi la riga e decidi»*: ### **senza il file ogni voce e' «forse nel
file»**, e decidere su una voce che il guardiano ha gia' deciso ### **significa sovrascrivere
la sua decisione con la mia.** ➜ **Il punto `2` si ferma al CONTROLLO.**

---

## ③ TODO DEL NEXT STEP — *la lista operativa*

- [ ] `A` — misurare `F9` e `F10` sull'indice vero, ### **read-only**, con l'elenco
- [ ] `B` — scrivere `F9` e `F10` ### **spenti**, e collaudarli su copia: `F9` su `A2`
- [ ] `C` — la regola corretta di `FATTO`, e ### **l'elenco di controllo** del punto `2`
- [ ] `D` — il punto `5`: `F6` su `G1`, esteso agli stati se non la trova
- [ ] `E` — il punto `4`, la parte indipendente dal file
- [ ] `F` — `doc/REFERTO_indice_v3_verifica_completa.md`, `_avanzamento.md`, la relazione
- [ ] ### ⛔ **FERMO su `3` e sul resto di `6`:** servono le `165` righe
- [ ] quando il file arriva: ### **un solo commit** che ① mette il file, ② accende `F9` e
      `F10`, ③ applica il lotto. ### **Perche' in due commit non si puo'**

### **LE CINQUE DOMANDE DI `doc/STELLA_POLARE.md`** *(`L-STELLA`)*

### **Non si applica, e il perche' e' parte della risposta:** nessuno dei sei punti
### **tocca la fisica.** Si cambiano `classe`, `dominio`, `era` e `stato` di voci
dell'indice, piu' due presidi che guardano ### **l'indice**, non il simulatore.
### **`soliton_simulator.py` non si apre**, e il suo blob *(`b8c21049`)* si verifica a
ogni commit.
