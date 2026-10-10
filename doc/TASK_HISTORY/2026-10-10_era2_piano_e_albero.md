# IL PIANO D'AZIONE DELL'ERA `2` E L'ALBERO DELLE SCELTE — **il mandato `3` di `6`**

> ### 📌 **IL RITO:** questo file si committa e si pusha ### **PRIMA del lavoro**, così
> l'ordine è ### **verificabile da git** invece che **asserito da me**.

> ### ⛔ **E IL MANDATO DICE UNA COSA CHE GOVERNA TUTTO IL RESTO:** *«solo scrittura del
> piano: ### **nessun codice di fisica, nessuna corsa**»*, e *«### **nessuna scelta di
> fisica in questo mandato**»*.

---

## `1.` RAGIONAMENTO PRELIMINARE — ### **cosa credo PRIMA di guardare, e cosa NON so**

### **LA FORMA DI QUESTO MANDATO**

Il mandato `2` mi portava `43` decisioni **già prese** e il rischio era **tradirne una**.
### ⭐ **Questo è il rovescio: mi chiede di scrivere il PIANO delle decisioni che NON sono
ancora prese**, e il rischio è ### **farne sembrare presa una che non lo è.** ### 📌 **E il
punto `3` del mandato è esattamente il presidio contro quel rischio:** *una decisione
marcata ### **PRESA** con una dipendenza ancora ### **APERTA** → la validazione
### **FALLISCE**.*

### **DUE OSTACOLI CHE HO GIÀ VISTO, e che il mandato non poteva prevedere**

| | l'ostacolo | perché conta |
|---|---|---|
| `a` | ### ⛔ **`doc/indice/decisioni.jsonl` È DICHIARATO `REPERTO` da `P-T2`**, col blob `d8a4fd2fae8c4b3f`, e `REPERTO` significa alla lettera *«il file ### **non cambia**: non ha una via di scrittura, ### **e non deve averla**»*. ### **E il punto `2` del mandato chiede di AGGIUNGERCI NODI.** | ### **Non è un conflitto da aggirare in silenzio:** o il mandato crea la via di scrittura e il file ### **cambia stato**, o i nodi vanno altrove. ### ✅ **Credo che la risposta sia `SOLO-AGGIUNTE`** — lo stato che `citazioni.jsonl` ha già, e che dice *«ogni riga che c'era a `HEAD` c'è ancora, IDENTICA»* — perché io ### **aggiungo** nodi e ### **non tocco** i `25` che ci sono |
| `b` | ### ⛔ **`D2`, `D4`, `D5`, `D6` SONO GIÀ OMONIMI DELL'ERA `1`**, e li ho appena trattati nel mandato `2`. ### **Le `D9`/`D13`/`D6`/`D7` del mandato sono ETICHETTE LOCALI di una lista di Luca**, non ID dell'indice | `par.9`: ### **un'etichetta locale NON è un ID**, e vive col namespace. ### ⚠ **E `P-ID` rifiuta un ID di `2` caratteri e uno che collide con un omonimo:** quindi i nodi dell'albero ### **non possono chiamarsi `D9`** — gli serve un ID vero, con l'etichetta locale ### **in un campo** |

### **CHE COSA NON SO, e lo scrivo adesso**

1. ### ⛔ **DI CINQUE NODI SU DIECI NON CONOSCO L'ARGOMENTO.** Il mandato dice
   *«`D9` ### **geometria** → `D13` ### **memorie** → `D6` ### **vuoto** → `D7`
   ### **divisione**; più `D4`, `D2`, `D11`, `D12`, `T4`, `INT`»*. ### **Per i primi
   quattro l'argomento è scritto**; `INT` lo ricavo dall'integrazione sulla causalità
   *(«un secondo integratore come CANDIDATO, non come scelta: la decide Luca, nodo `INT`
   del piano»)*. ### ⚠ **Ma di `D4`, `D2`, `D11`, `D12`, `T4` il repo NON dice niente**:
   la lista numerata delle decisioni di Luca ### **non è nel repo** — l'ho cercata in
   `CODA`, `PUNTO_DELLA_SITUAZIONE`, nella relazione, nei task history e nell'indice.
   ### ⛔ **NON INVENTO il loro argomento:** creo il nodo con la sua etichetta e
   ### **dichiaro che l'argomento non è nel repo**, e lo chiedo a Luca. ### ⭐ **Inventarlo
   sarebbe esattamente il difetto del mandato precedente, al rovescio: non tradire una
   decisione presa, ma INVENTARNE UNA DA PRENDERE.**
2. ### **che cosa siano «le decisioni `1`, `3`, `10`»**, che il mandato dà come
   ### **radici già prese** accanto ad `A16` e `A17`. ### ⚠ **Stessa lista numerata, stesso
   buco** — e la stessa risposta: ### **non le indovino.**
3. ### **se `decisioni.jsonl` abbia un validatore** che rifiuti un campo nuovo
   *(`dipende_da`)*: è uno dei dieci registri, ma non so se lo schema lo guardi
   ### **a vocabolario chiuso**. ### **Lo leggo dal codice prima di scrivere.**

---

## `2.` PROGETTAZIONE DEL RAGIONAMENTO

### **L'ORDINE, e perché**

| | che cosa | perché |
|---|---|---|
| `1` | ### **LEGGERE DAL CODICE** come `decisioni.jsonl` è validato, e come `P-T2` tratta un `REPERTO` che deve cambiare stato | ### ⛔ **prima di scrivere in un registro devo sapere chi lo guarda** — e `P-T2` lo guarda col BLOB |
| `2` | ### **LA VIA DI SCRITTURA** dei nodi dell'albero, dentro `indice.py`, e il passaggio di `decisioni.jsonl` da `REPERTO` a `SOLO-AGGIUNTE` | ### **un registro con una via di scrittura NON è più un reperto**, e dirlo è metà del lavoro |
| `3` | ### **IL PRESIDIO DELL'ALBERO** *(punto `3`)*, collaudato ### **nei due versi**, ### **PRIMA** di inserire i nodi | ### ⭐ **se il presidio nasce dopo i nodi, non può dire se i nodi erano giusti** — ed è la stessa ragione per cui `P-ID` è nato prima dei lotti |
| `4` | ### **I NODI**, dalla via unica: i quattro con l'argomento scritto, `INT`, e i cinque ### **senza argomento, dichiarati tali** | |
| `5` | ### **`doc/PIANO_era2.md`**: le fasi `F0`-`F4` con ### **ingresso e uscita** | il piano si scrive ### **dopo** l'albero, perché la fase `F2` È l'albero |
| `6` | il ### **referto** e `_avanzamento.md` | il verdetto |

### **LE LETTURE, FISSATE ADESSO**

| | la misura | la lettura che fisso PRIMA |
|---|---|---|
| il presidio dell'albero | una decisione `presa` con una dipendenza `APERTA` | ### **DEVE far FALLIRE `valida`.** ### ⛔ **E il caso che DEVE fallire si costruisce DAI NODI VERI, non a mano** *(`P1-sexies`)* |
| il presidio, al rovescio | l'albero ### **come lo scrivo io** | ### **DEVE passare.** Se non passa, ### **l'albero è sbagliato, non il presidio** |
| `decisioni.jsonl` | i `25` nodi che c'erano | ### **DEVONO esserci tutti, IDENTICI**: è ciò che `SOLO-AGGIUNTE` significa, e `P-T2` lo misura ### **riga per riga** |
| gli ID | il censimento di `P-ID` | ### **nessun nodo nuovo collide**, e ognuno ha ### **≥ `4` caratteri**. ### ⚠ **`D9` non è un ID: lo sarebbe se lo creassi così, e `P-ID` lo RIFIUTEREBBE** |
| le fasi del piano | `F0`-`F4` | ### **ognuna ha ingresso E uscita**, e ### **l'uscita è MISURABILE** — se un'uscita non si può misurare, è un desiderio, non un criterio |

### **CHE COSA MI FAREBBE FERMARE**

| | il caso | che faccio |
|---|---|---|
| `a` | ### **un nodo di cui non conosco l'argomento** | ### ⛔ **NON lo invento.** Creo il nodo con la sua etichetta, ### **dichiaro che l'argomento non è nel repo**, e registro ### **UNA domanda** per i cinque. ### **Il resto del mandato non ne dipende**, quindi proseguo |
| `b` | `P-T2` rifiuta il cambio di stato di `decisioni.jsonl` | ### **FERMO e lo scrivo:** un reperto che cambia è il difetto che `P-T2` esiste per vedere, e ### **se ha ragione lui, i nodi vanno altrove** |
| `c` | il presidio dell'albero ### **non fallisce** sul caso che deve fallire | ### ⛔ **FERMO.** Un presidio che non impedisce è una tenda *(`A9`)*, e ### **un albero senza il suo presidio è un elenco** |
| `d` | mi accorgo di stare ### **scegliendo** una direzione di fisica | ### **FERMO.** Il mandato dice *«nessuna scelta di fisica»*, e ### **la direzione su `D9` che Luca ha dichiarato NON è una decisione presa** — lo dice il mandato stesso, e il presidio del punto `3` serve proprio a tenerle separate |

### **LA STELLA POLARE** *(`L-STELLA`)*

### ⚠ **NON SI APPLICA, e il perché è parte della risposta:** questo mandato
### **non cambia la fisica** — non tocca `primo_ordine/`, non aggiunge nessuna legge alla
tabella, non fa girare nessuna scena. ### **Scrive un PIANO e un ALBERO**, cioè
### **documenti e nodi di registro**, più un presidio che li guarda. ### ⛔ **E le cinque
domande si applicheranno a OGNI commit della fase `F3`**, che è dove le leggi entrano una
alla volta: ### **il piano stesso dovrà dirlo.**

---

## `3.` TODO DEL NEXT STEP

- [ ] leggere **dal codice** chi valida `decisioni.jsonl`, e come `P-T2` tratta il cambio di stato di un `REPERTO`
- [ ] la **via di scrittura** dei nodi dell'albero in `indice.py`, e `decisioni.jsonl` da `REPERTO` a `SOLO-AGGIUNTE`
- [ ] il **presidio dell'albero** *(`presa` con una dipendenza `APERTA` → `valida` FALLISCE)*, collaudato **nei due versi**, **prima** dei nodi
- [ ] i **nodi**: `D9`→`D13`→`D6`→`D7`, `INT`, e i **cinque senza argomento, dichiarati tali** + **una domanda a Luca**
- [ ] **`doc/PIANO_era2.md`**: `F0`-`F4`, ognuna con **ingresso e uscita MISURABILE**
- [ ] il **referto** `doc/REFERTO_piano_era2.md`, e `_avanzamento.md`
