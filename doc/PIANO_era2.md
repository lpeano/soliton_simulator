# IL PIANO D'AZIONE DELL'ERA `2` — **cinque fasi, e ognuna ha un CRITERIO DI USCITA MISURABILE**

> ### ⛔ **QUESTO FILE NON E' UN ELENCO DI BUONE INTENZIONI.** Ogni fase ha un
> **criterio di INGRESSO** *(che cosa deve essere vero per cominciarla)* e un
> **criterio di USCITA** *(che cosa deve essere vero per dirla finita)*, e
> ### **l'uscita deve essere MISURABILE: se non si può misurare, è un desiderio, non un
> criterio.**

> ### 📌 **L'ALBERO DELLE SCELTE sta in `doc/ALBERO_era2.yaml`**, e il presidio che lo
> guarda è **`P-ALB`** *(`csv/_albero_era2.py`, dentro `python csv/indice.py valida`)*.
> ### **La fase `F2` È quell'albero**, percorso nel suo ordine.

> **Il bersaglio del progetto non cambia:** le tre prove di
> `doc/IPOTESI_gravita_a_spinta.md`. ### **Questo piano è la strada, non la meta.**

---

## LE CINQUE FASI, in una tabella

| | la fase | che cosa fa | dove si misura l'uscita |
|---|---|---|---|
| **`F0`** | ### **CHIUSURA** | riordino, decisioni, infrastruttura — ### **tutto verificato dal guardiano** | `doc/REFERTO_*_era2*.md`, e la verifica del guardiano |
| **`F1`** | ### **REGOLE DI FORMA** | ogni accoppiamento fra nodi è un ### **bilineare**; ### **nessun `dt` da grandezze globali**; le misure globali ### **solo negli osservatori** | il ### **generatore RIFIUTA** ciò che non ha quella forma |
| **`F2`** | ### **LE DECISIONI** | l'albero delle scelte, ### **nel suo ordine** | `P-ALB`, e i nodi `presa` in `decisioni.jsonl` |
| **`F3`** | ### **LE LEGGI** | le leggi in tabella, ### **UNA alla volta**, con sigillo e referto | il conto delle leggi ### **`prova: false`**, e un sigillo per ognuna |
| **`F4`** | ### **LE PRIME MISURE** | `O4`, `Z47`, `I1`, la dilatazione degli orologi come gravità, `U(1)` come elettromagnetismo | un referto per misura, coi suoi ### **criteri fissati prima** |

### ⚠ **E L'ORDINE NON E' DECORATIVO:** `F1` prima di `F2` perché ### **una regola di forma
restringe ciò che una decisione può scegliere**; `F2` prima di `F3` perché ### **una legge
scritta prima della decisione che la governa è una decisione presa di nascosto**; `F3` prima
di `F4` perché ### **una misura su una tabella di leggi finte misura il simulatore, non la
natura.**

---

## `F0` — **CHIUSURA**

| | |
|---|---|
| **INGRESSO** | nessuno: ### **è la fase in cui siamo** |
| **che cosa comprende** | il riordino dell'indice *(schema `3`)*, le ### **`43` decisioni** di Luca, l'infrastruttura dell'era `2` in ### **tre parti**, le ### **regole di gestione** |
| ### ⛔ **USCITA** | ① `python csv/indice.py valida` ### **passa**, e i segnali ### **non crescono**; ② ogni presidio dell'era `2` ha un ### **collaudo nei due versi** che passa, e ### **sta nel `pre-commit` o nella CI**; ③ `DA_DECIDERE_LUCA.md` contiene ### **solo domande che aspettano Luca**, non difetti miei; ④ ### **il guardiano ha verificato** i commit della fase |
| **dove si misura** | `doc/REFERTO_seconda_parte_era2.md`, `doc/REFERTO_decisioni_43_era2.md`, `doc/REFERTO_piano_era2.md`, e i due referti dell'infrastruttura |

### 📌 **LO STATO DI OGGI, misurato:** `valida` ### **passa**, i segnali sono ### **`19` e
non sono cresciuti**, il simulatore è ### **`b8c21049` intatto**, e
`DA_DECIDERE_LUCA.md` ha ### **`5` voci** — ### **tutte domande per Luca**, nessuna un
difetto mio. ### ⚠ **Restano la TERZA parte dell'infrastruttura e le REGOLE DI GESTIONE:**
`F0` ### **non è chiusa.**

---

## `F1` — **LE REGOLE DI FORMA**

> ### ⛔ **Questa fase non aggiunge leggi: RESTRINGE QUELLE CHE SI POSSONO SCRIVERE.**
> ### ⭐ **Ed è il posto più economico del piano**, perché una regola di forma
> ### **impedisce una classe intera di errori una volta per tutte**, invece di cercarli
> uno a uno nei sigilli.

| | |
|---|---|
| **INGRESSO** | ### **`F0` chiusa**: le regole di forma si scrivono nel generatore, e un generatore che cambia mentre l'infrastruttura si muove ### **non si può sigillare** |
| ### **la regola `(a)`** | ### **ogni accoppiamento fra nodi è un BILINEARE** `psi_i^dag (...) psi_j` |
| ### **la regola `(b)`** | ### **nessun `dt` da grandezze globali** |
| ### **la regola `(c)`** | ### **le misure globali SOLO negli osservatori** |
| ### ⛔ **USCITA** | per ognuna delle tre: il ### **generatore RIFIUTA** una legge che la viola, e il rifiuto è ### **collaudato nei due versi** *(una legge che la rispetta passa, una che la viola è rifiutata ### **per la chiave giusta**)* |

### ⭐ **E LA REGOLA `(a)` E' GIA' VERA SENZA ESSERE UNA REGOLA**, ed è un fatto misurato:
il termine di prova `PROVA-HOPPING` ### **ha esattamente quella forma.** ### ⚠ **Non è un
caso né una scelta: è la forma più semplice che ACCOPPIA DUE NODI** — ed è per questo che
l'ho scelta come prova. ### ⛔ **Ma il generatore OGGI NON LA PRETENDE**, e
### **finché non la pretende non è una regola: è un'abitudine.** *(È il punto che il
mandato del piano nomina da sé.)*

### 📌 **E LA REGOLA `(c)` HA GIA' IL SUO MECCANISMO:** `A17` *(«ogni comportamento è
determinato solo dal suo ambito»)* e il campo `ambito` delle leggi. ### **Quindi `(c)` è
in buona parte l'estensione di un presidio che c'è**, non un presidio nuovo — e
### **`9-ter` dice di preferire proprio questo.**

---

## `F2` — **LE DECISIONI, NELL'ORDINE DELL'ALBERO**

| | |
|---|---|
| **INGRESSO** | ### **`F1` chiusa**: una decisione presa senza le regole di forma ### **può scegliere una forma che poi si dovrà disfare** |
| **la catena** | `D9` geometria → `D13` memorie → `D6` vuoto → `D7` divisione |
| **gli altri nodi** | `INT` *(l'integratore)*, e `D4`, `D2`, `D11`, `D12`, `T4` |
| **le radici già prese** | `A16`, `A17` — ### **e sono ASSIOMI**, non scelte di questa fase |
| ### ⛔ **USCITA** | ① ogni nodo dell'albero è ### **`presa: true`**; ② `P-ALB` ### **passa**, cioè ### **nessuno è stato preso prima di quelli da cui dipende**; ③ ogni decisione presa ha la sua ### **scheda in `doc/REGISTRO_FISICA.md`**, perché `H-REG-R` la pretende |
| **dove si misura** | `python csv/_albero_era2.py` *(nodi, archi, `presa`)*, e `doc/indice/decisioni.jsonl` |

### ⛔ **DUE COSE BLOCCANO QUESTA FASE OGGI, e sono registrate, non taciute:**
### **`DEC-ALBERO-CINQUE-SENZA-ARGOMENTO`** *(di `D4`, `D2`, `D11`, `D12`, `T4` il repo non
dice di che cosa si decida, e nemmeno quali siano «le decisioni `1`, `3`, `10`»)*, e
### **`DEC-NASCITA-PSI`** con ### **`DEC-REGOLA-FORMA`**, che sono decisioni di fisica che
aspettano Luca. ### **`F2` non può nemmeno cominciare prima che Luca risponda al primo.**

### ⛔ **E DUE REGOLE DI LUCA DEL `2026-10-10` VINCOLANO `D9` PRIMA CHE SIA PRESA.**
### **[[VETTORI-DAI-BILINEARI]]**: vettori e tensori ### **SOLO dai bilineari dello
spinore** *(`psi^dag sigma psi` sul nodo, `psi_i^dag psi_j` sull'arco)* e dalle ### **fasi
e olonomie sugli archi** — ### **MAI dalle posizioni**, che rafforza `A17`.
### **[[ISOTROPIA-MISURATA]]**: qualunque esito di `D9` dovra' ### **farsi misurare
l'isotropia** prima che si parli di un campo emerso.
### ⚠ **Non decidono `D9`: ne restringono le USCITE AMMESSE** — ed e' la ragione
per cui stanno qui e non nel `yaml` dell'albero, che tiene ### **le scelte**, non i vincoli
su di esse.

### 📌 **E SU `D9` LUCA HA GIA' DICHIARATO UNA DIREZIONE:** *«lo spazio emerge grazie alla
mitosi»* — la mitosi crea ### **i nodi e gli archi** *(la topologia)*, le relazioni fra gli
stati `psi` ne danno ### **la metrica**: è la ### **`9(b)`**. ### ⚠ **E IL MANDATO DICE,
NELLA STESSA FRASE, CHE LA DIREZIONE NON E' UNA DECISIONE PRESA:** *«il confronto `(a)`/`(b)`
su `PROVA` resta, con i criteri fissati PRIMA»*. ### ⭐ **Tenere separate quelle due cose è
esattamente il lavoro di `P-ALB`**, ed è il motivo per cui la direzione sta nel `yaml`
### **come nota e non come stato.**

---

## `F3` — **LE LEGGI, UNA ALLA VOLTA**

> ### ⛔ **È la regola d'oro del repo applicata alla fisica:** ### **un interruttore alla
> volta**, si accende, ### **si sigilla**, poi il successivo. ### **Mai tutto insieme: con
> tutto acceso ogni risultato è ININTERPRETABILE.**

| | |
|---|---|
| **INGRESSO** | ### **`F2` chiusa** per la decisione che governa quella legge. ### ⚠ **Non tutta `F2`: la legge che dipende da `D9` aspetta `D9`, non `D7`** — ed è a questo che serve l'albero |
| **il rito di OGNI legge** | ① la riga in `primo_ordine/leggi/leggi.yaml` con ### **`prova: false`**, i suoi `assiomi` e i `parametri` ### **con VALORE e ORIGINE**; ② `python primo_ordine/_genera.py` — ### **il codice NON si scrive a mano**; ③ il ### **sigillo** sul modello di `primo_ordine/sigilli/_modello.py`, coi criteri ### **fissati prima** e il criterio ### **`deve-fallire` OBBLIGATORIO** *(`P-E9`)*; ④ il ### **referto**; ⑤ le ### **cinque domande di `doc/STELLA_POLARE.md`** nel task history *(`L-STELLA`)*; ⑥ la ### **scheda in `doc/REGISTRO_FISICA.md`** *(`H-REG-R`)* |
| ### ⛔ **USCITA** | ① ### **zero leggi `prova: true`** nella tabella; ② ogni legge ha ### **un sigillo che passa AL SUO COMMIT**, con ### **un controllo positivo che POTEVA fallire**; ③ `P-E1`…`P-E9` ### **passano**; ④ ### **nessuna manopola**: ogni parametro ha un'### **ORIGINE**, e `A1` lo pretende |
| **dove si misura** | `python primo_ordine/timbro.py` *(il conto delle leggi esce dalla ### **TABELLA**)*, e `csv/_seal_fork/`, `doc/leggi_era2/` |

### 📌 **LO STATO DI OGGI, misurato:** la tabella ha ### **`3` leggi, TUTTE `prova: true`**
→ ### ⛔ **ZERO LEGGI VERE.** ### **E non è un difetto: è il punto di partenza dichiarato**
— l'infrastruttura è stata costruita su leggi finte ### **proprio perché una legge finta non
può far sembrare vero un risultato.**

### ⚠ **E UNA COSA DA NON DIMENTICARE, perché è un difetto APERTO:**
### **`H-FISICA-FUORI-LISTA` legge la lista dal DISCO**, quindi una modifica non committata
alla lista ### **autorizza un commit.** ### **In `F3` quel buco conta più che in `F0`.**

---

## `F4` — **LE PRIME MISURE**

| | |
|---|---|
| **INGRESSO** | ### **`F3` chiusa** per le leggi che quella misura coinvolge. ### ⛔ **Una misura su leggi finte misura il simulatore, non la natura** |
| **le misure** | `O4` · `Z47` · `I1` · la ### **dilatazione degli orologi come gravità** · ### **`U(1)` come elettromagnetismo** |
| ### ⛔ **USCITA** | per ognuna: un referto con ① i criteri ### **fissati PRIMA** di vedere i numeri; ② le ### **barre d'errore** e ### **più di un seme** *(`P3`: niente statistica senza una barra)*; ③ un ### **controllo positivo** e un caso che ### **DEVE fallire**; ④ la ### **configurazione INTERA** dichiarata *(`P5`)* |
| **dove si misura** | `doc/REFERTO_*`, e l'indice |
| ### ⭐ **E UN CRITERIO IN PIU', deciso da Luca il `2026-10-10`** | ### **[[ISOTROPIA-MISURATA]]**: l'### **isotropia del supporto** — in particolare del grafo ### **nato dalla mitosi** — e' un criterio ### **MISURATO**, e la propagazione deve venire ### **uguale lungo direzioni diverse**, ### **PRIMA** di dire che un campo e' emerso. ### ⚠ **Oggi NON ha materia** *(nessuna geometria, nessuna direzione)*, e ### **dipende da `D9`**: senza `D9` non c'e' niente su cui misurare una direzione — ### **non e' un ritardo, e' una DIPENDENZA** |

### ⭐ **E QUESTA FASE E' LA PRIMA CHE PARLA DEL BERSAGLIO.** Le tre prove di
`doc/IPOTESI_gravita_a_spinta.md` — ### **due masse si avvicinano? con che legge? tutti i
corpi cadono allo stesso modo?** — ### **vivono DOPO `F4`**, e le quattro condizioni di
avvio stanno nel par. `6` di quel documento. ### ⚠ **Scriverlo qui serve a una cosa sola:
non far sembrare `F4` la fine.**

---

## IL TABELLONE DI CONTROLLO — **dove si guarda, a ogni fase**

| il comando | che cosa dice |
|---|---|
| `python csv/indice.py valida` | l'indice intero, ### **e `P-ALB` dentro** |
| `python csv/_albero_era2.py` | nodi, archi, `presa`, ### **senza argomento noto** |
| `python csv/indice.py da-decidere` | ### **ciò su cui si aspetta Luca**, generato |
| `python primo_ordine/timbro.py` | il conto delle leggi ### **dalla TABELLA** |
| `python csv/_metodi_era2.py` | i metodi dell'era `1` ### **portati o no** |
| `python csv/_replay_registri.py` | i dieci registri, e i ### **generati byte-identici** |

### ⛔ **E UNA REGOLA CHE VALE PER TUTTE LE FASI:** un criterio di uscita che
### **non esce da un comando** non è un criterio. ### **Se una fase si dichiara chiusa, si
dice CON QUALE COMANDO.**
