# COMMIT 6b DEL RIORDINO — `MITOSI_2LAM` diventa LEGGE, in forma GENERALE

*(mandato del guardiano, piano par. 6b. **Questo file e' committato PRIMA del codice**,
par.8, cosi' l'ordine e' verificabile da git invece che asserito da me.)*

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo prima di misurare*

### **LA LEGGE, come il mandato la fissa**

> Un arco si divide **solo se** `FRAZ_NASCITA * d >= LAM` **E**
> `(1 - FRAZ_NASCITA) * d >= LAM`, **sempre**, senza condizione sul flag.

**COSA CREDO, e perche' lo credo PRIMA di girare.** A `t = 0.5` la legge nuova e quella
vecchia sono **la stessa condizione, esattamente**:

```
FRAZ_NASCITA = 0.5  ->  0.5*d >= LAM  AND  0.5*d >= LAM   (i due rami COINCIDONO)
il cancello vecchio ->  d >= 2.0*LAM
```

e `0.5*d >= LAM` equivale a `d >= 2*LAM` **al bit**, perche' la moltiplicazione per `0.5` e
per `2.0` e' ### **esatta in IEEE-754** *(sono potenze di due: la mantissa non cambia, cambia
solo l'esponente)*. ### **Quindi mi aspetto il braccio `A` IDENTICO AL BYTE con
`--mitosi-2lam`, e non <<quasi>>.**

### ⚠ **IL LIMITE DI QUESTA CERTEZZA, dichiarato:** vale per `d` **finito e normale**. Su un
`d` subnormale il raddoppio resta esatto ma il dimezzamento puo' perdere l'ultimo bit; `d` e'
una lunghezza d'arco con un pavimento a `0.05`, quindi il caso non si presenta — **ma e' una
premessa sul dominio, non un teorema sul codice.**

### 📌 **E IL PIANO DICEVA *«calo di `n` al 72»*: QUELLA PREVISIONE VALE SOLO SENZA IL FLAG.**
Con `--mitosi-2lam` il cancello c'e' gia', quindi **non puo' cambiare niente**. ### **Il calo
si vedra' nella scena SENZA il flag, dove oggi passano archi corti** — ed e' il braccio `B`.
*(Lo scrivo qui perche' il mandato lo chiede, e perche' una previsione applicata alla scena
sbagliata si legge come una smentita della legge.)*

### **I FATTI MISURATI DAL GUARDIANO**

*(Linux, numpy 2.5.3, seme 11, 72 passi. **Sulla mia piattaforma i conteggi cambiano**, e il
referto del 6a lo ha gia' dimostrato: `16/14/6/6` suoi contro `14/12/4/4` miei.)*

| scena | candidati | `d < 1.6` | `1.6 <= d < 2.0` | `d >= 2.0` | `_g_m2l_negati` |
|---|---|---|---|---|---|
| **con** `--mitosi-2lam` | 11 | 2 **rifiutati** | 2 **ammessi** | 7 | **2** |
| **senza** | 23 | 8 **ammessi**, poi troncati da `_nasce` | — | — | — |

### **COSA NON SO, e non voglio fingere di sapere**

1. ### **se sulla MIA piattaforma esistono candidati con `1.6 <= d < 2.0`.** Il caso
   `C-bis (i)` *(cancello vecchio `d >= 2*LAM` con `t = 0.4`)* ### **ne ha BISOGNO per poter
   fallire**: con `t = 0.4` la legge nuova chiede `d >= 2.5*LAM`, la vecchia `d >= 2*LAM`, e
   la differenza vive ### **esattamente in quella finestra.** ### ⛔ **Se non ci sono, quel
   caso che <<deve fallire>> PASSEREBBE PER ASSENZA DI MATERIA — un `FALSO-ZERO`. Allora li
   COSTRUISCO e lo DICHIARO**, come il mandato permette;
2. quale ramo di soglia decide la divisione in queste scene *(`TORS_4PI` / `3*pi` oppure
   `PHI_CRIT`)* e in che intervallo stanno le soglie locali. ### **Il mandato chiede di
   riportarlo, e io non l'ho mai misurato;**
3. la distribuzione di `|tw|` degli archi rifiutati per `LAM`. ### **Non so dove stia rispetto
   a `PHI_CRIT` e a `3*pi`** — e quel numero serve al `6c`, non al `6b`;
4. ### **quanti siti trovera' il mio censimento.** Vedi il paragrafo qui sotto: ne ho gia'
   visti tre che non sono nella lista del guardiano.

### ⚠ **CHE COSA HO GIA' GUARDATO PRIMA DI SCRIVERE QUESTO FILE, e lo dichiaro invece di far
finta di no:** ho letto il cancello *(`if MITOSI_2LAM and len(c):`)*, il default a `:457`, il
sito del CLI, il blocco `[flag-inerti]` e **il modello di `PAV_COM`**, che e' il flag inerte
da imitare. ### **E ho fatto un `grep` per nome**, che trova **tre siti non nella lista del
mandato**: `:3471`, `:8929`, `:11129`.

### **Sono COMMENTI, non codice** — ma `:8929` **asserisce la legge**
*(«NESSUN PAVIMENTO: `d >= LAM` con `SEMINA_LAM`/`MITOSI_2LAM`»)*, e dopo la cura quella
asserzione diventa **vera senza condizioni**: un commento che resta condizionale
### **sarebbe scaduto il giorno stesso**, ed e' esattamente la classe di difetto che
`doc/FATTI_dal_codice.md` elenca. ### **Il censimento dall'AST decidera' se sono tre o piu'; e
se trovo altro CODICE non previsto, mi FERMO.**

### 📌 **E `doc/FATTI_dal_codice.md` NON HA una voce per `decidi_divisione` ne' per
`MITOSI_2LAM`** *(verificato con `grep`)*. ### **Non e' una scusa, e' un fatto da aggiungere:**
il par.0 dice che quel file si legge prima di toccare una funzione — e qui **non c'era niente
da leggere.**

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *come intendo arrivarci*

| passo | cosa DECIDE | cosa mi farebbe FERMARE |
|---|---|---|
| **①** il **censimento dall'AST**, confrontato con la lista del guardiano **dalla macchina** | se il perimetro e' quello dichiarato | ### **un sito di CODICE non previsto: STOP e lo dico** |
| **②** il **codice**: cancello incondizionato in forma generale, archivio del ramo vecchio, flag dichiarato inerte, contatori nuovi | — | un contatore che non so attribuire a **un ramo preciso** |
| **③** il **sigillo**, committato **prima** di girare | se la legge e' la stessa dove deve esserlo e diversa dove deve | ### **qualunque criterio che fallisce** |
| **④** il **run staccato**, non bufferizzato | — | — |

### **I CRITERI DEL SIGILLO, fissati QUI, prima di vedere i numeri**

| | che cosa |
|---|---|
| **`0`** | la patch committata applicata al *prima* (`c18c9bf6`) da' **il blob di oggi** |
| **`A`** | ### **IDENTICO AL BYTE** sulle tre scene del driver *(`corta`, `lunga`, `altro_seme`, **con** `--mitosi-2lam`)*, stato **e** contatori. ### ⚠ **I contatori NUOVI esistono solo nell'<<oggi>>: si SEPARANO PER NOME e si RIPORTANO, e NON contano come differenza di stato.** ### ⛔ **Ma la separazione e' per NOME ATTESO, non per <<sta solo nell'oggi>>:** un attributo nuovo che io **non ho previsto** ### **FA FALLIRE il braccio**. Altrimenti l'esclusione diventa un buco in cui passa qualunque cosa — ed e' `FALSO-ZERO` |
| **`B`** | la scena **senza** `--mitosi-2lam`: ### **NON identica, ed e' ATTESO.** ### **`B1`** nell'oggi `_sm_trd_mitosi == 0` **e** `_sm_trd0_mitosi == 0`, e nel *prima* **non** sono zero: si riportano **entrambi**, perche' ### **uno zero atteso vale solo se accanto c'e' il numero che era.** ### **`B2`** a **ogni** divisione ammessa, `min(t, 1-t) * d >= LAM`, verificato ### **evento per evento**, non in media. ### **`B3`** si riportano candidati, rifiuti **per cancello**, `n` e archi al 72 *prima/oggi*, `|tw|` dei rifiutati, `_g_m2l_dmin` |
| **`C`** | una copia con **`FRAZ_NASCITA = 0.4`**, su **tutte** le scene: `_sm_trd_mitosi == 0` e **ogni** `d` ammesso ha `0.4 * d >= LAM` |
| **`C-bis`** | ### **TRE copie che DEVONO fallire** *(troncamenti `> 0` oppure `B2` violato)*: ### **(i)** `t = 0.4` col cancello **VECCHIO** `d >= 2*LAM` · ### **(ii)** `t = 0.4` col **solo** `(1-t)*d >= LAM` · ### **(iii)** `t = 0.6` col **solo** `t*d >= LAM`. ### ⛔ **Il caso (i) richiede candidati con `1.6 <= d < 2.0`: si VERIFICA che esistano sulla mia piattaforma, e se mancano si COSTRUISCONO e si DICHIARA** |
| **`D`** | con `--mitosi-2lam` l'avvio stampa `MITOSI_2LAM` fra i `[flag-inerti]`, **e** l'archivio contiene il cancello vecchio ### **verbatim** |

### ⛔ **E SE UN CRITERIO FALLISCE: FERMARSI E RIPORTARE, non aggiustare il criterio.**

### **PERCHE' `(ii)` E `(iii)` SONO DUE CASI E NON UNO.** Un cancello a **una sola meta'**
sbaglia ### **solo sul lato che non guarda**: con `t = 0.4` il troncone corto e' quello di
`t`, quindi il controllo sul solo `(1-t)` lo **manca**; con `t = 0.6` il corto si **scambia**,
e lo manca il controllo sul solo `t`. ### **Due copie provano che la congiunzione serve DA
ENTRAMBI I LATI, e una sola proverebbe meta' della legge.**

## 3. TODO DEL NEXT STEP

1. ☐ **committare e pushare QUESTO FILE** *(par.8)*, con la voce aperta dello Schwinger
2. ☐ il **censimento dall'AST** + voce d'inventario, committato, poi girato — ### **e il
   confronto con la lista del guardiano lo fa LA MACCHINA, non io a occhio**
3. ☐ il **verdetto del censimento**: solo i siti previsti? *(se no, **STOP**)*
4. ☐ il **codice** + la **patch**, piu' `csv/_cure_verificate.py`, il commento di `:457`
   *(rispettando `csv/_presidio_commenti_flag.py`)*, `doc/REGISTRO_FISICA.md`,
   `doc/TABELLA_nascita.md`, `doc/CONTRATTO_nascita.md` se l'ordine cambia,
   `doc/FATTI_dal_codice.md`, l'inventario
5. ☐ il **sigillo** a sei bracci *(`0`, `A`, `B`, `C`, `C-bis`, `D`)*, committato **prima**
6. ☐ il **run STACCATO** e non bufferizzato, poi il **referto** nel commit dopo
7. ☐ **STOP** — e il guardiano verifica

### ⚠ **E IL `6c` NON SI TOCCA:** la distribuzione di `|tw|` si **misura e si riporta**, non si
usa per cambiare una soglia. *(`A1`: la legge, non il numero.)*

---

## **LA STELLA POLARE — le cinque risposte, scritte PRIMA del codice**

*(`L-STELLA`, `doc/STELLA_POLARE.md`. **Il «perche'» e' parte della risposta.**)*

### **① `A14`: questa legge conserva energia e carica LOCALMENTE?**

### ✅ **SI, e fa di piu': NE TOGLIE UNA VIOLAZIONE.** Il cancello **non modifica lo stato**:
**rifiuta un evento**. Una decisione a monte non muove ne' energia ne' carica — ### **non e'
un taglio, e' un NON-ACCADIMENTO.**
### 📌 **E IL PUNTO CHE CONTA:** oggi gli archi piu' corti di `LAM` nascono comunque e
### **`_nasce` li ALZA** — cioe' **modifica una lunghezza dopo averla creata**, che e' un
### **tipo (3)** della classificazione dei numeri a mano *(proiezione/pavimento/clip)* e
### **viola `A14` per costruzione, qualunque sia il valore.** ### **Il `6b` rende quel
troncamento IRRAGGIUNGIBILE sul sito della mitosi**, e il criterio `B1`
*(`_sm_trd_mitosi == 0` e `_sm_trd0_mitosi == 0`)* ### **e' esattamente la misura di quella
affermazione.**
### ⚠ **E NON LA TOGLIE DOVE NON GUARDA:** lo Schwinger continua a produrre archi sotto `LAM`
*(`46` nel referto `1927b45`)*, ed e' `SCHW-SOTTO-LAM`, ### **registrata e NON curata dal 6b.**

### **② A quale dei TRE GRADINI di `ROBUSTEZZA-FISICA` arriva?**

### ⛔ **A NESSUNO, e si applica solo per una parte — perche' il `6b` NON AFFERMA UN RISULTATO
DI FISICA:** rende **incondizionata una legge**. Non c'e' un fenomeno di cui dire *«e'
emergente»*.
### **Cio' che il `6b` afferma sono due cose, e si misurano diversamente:** ### **(a)** una
### **IDENTITA'** *(con il flag, byte-identico)*, e per quella il gradino **(a)** e' il
criterio giusto — ### **tre scene, due semi, confronto DOPO OGNI PASSO**; ### **(b)** una
### **CONSEGUENZA MISURATA** *(i troncamenti vanno a zero senza il flag)*, che e' un fatto sul
codice, non una conclusione di fisica.
### ⚠ **I gradini (b) e (c) NON SI APPLICANO, e dirlo e' la risposta:** non c'e' nessuna legge
pratica da spegnere per vedere se il fenomeno resta, perche' ### **il fenomeno E' la legge.**

### **③ Aggiunge un numero o una legge? Di che TIPO? Compensa un difetto?**

### ✅ **NON AGGIUNGE NESSUN NUMERO.** Usa `FRAZ_NASCITA` — che esiste dal `6a` ed e' un
### **tipo (2), una TOPPA** da derivare — e `LAM`, che e' la scala della teoria.
### 📌 **E SULLE LEGGI IL CONTO VA IN DIMINUZIONE, che e' il criterio `9-ter`:** oggi ci sono
### **DUE comportamenti** *(col flag e senza)*; dopo il `6b` ce n'e' ### **UNO**. Il ramo
«senza» ### **esce dal sorgente e va in archivio**, e il flag resta ### **inerte come
`PAV_COM`** *(decisione 3 di Luca: si conserva tutto)*.
### ⛔ **E NON COMPENSA UN DIFETTO: lo TOGLIE.** Il `6b` non mette una legge davanti a un
problema — ### **rende irraggiungibile un tipo (3)**, cioe' fa l'opposto di cio' che
`AUDIT-CURE` cerca.

### **④ Tocca `rho`, `c_s` o il SEGNO? In quale VERSO dell'accoppiamento?**

### ✅ **NO, e la risposta e' MISURATA e non asserita.** Il cancello legge `d` *(lunghezza
d'arco)* e `LAM`. ### **Non legge `rho`, non legge `c_s`, non legge il segno.**
### 📌 **E CIO' CHE LO RENDE VERIFICABILE E' IL CENSIMENTO:** `a7ef047` elenca
### **ogni** sito di `MITOSI_2LAM` dall'AST, e il perimetro del `6b` e' quello. ### **Dentro
`decidi_divisione` esiste un criterio di densita'** *(`0.5*(I[a]+I[b]) >= QMIN_M *
median(peq)`)*, ### **e il `6b` NON LO TOCCA** — e' una riga `ALTRO` del censimento del punto
medio, non un sito del flag.
### ⚠ **Quindi `EM-CURVATURA-BIDIREZIONALE` non si applica, e il *«perche'»* e' che il sito
cambiato non sta su quel percorso.**

### **⑤ Emergente o imposto?**

### ⛔ **IMPOSTO, DI PROPOSITO, E DICHIARATO: e' una LEGGE, non una misura.** `A13` alla
nascita e' un vincolo che **si mette**, e il `6b` esiste per metterlo **senza condizioni**.
> ### 📌 **E QUI STA LA TRAPPOLA DA SCRIVERE PRIMA, perche' dopo sarebbe una scusa:** il
> piano prevede un **calo di `n` al passo 72** nella scena senza flag. ### **Quel calo e'
> IMPOSTO PER COSTRUZIONE** — meno nascite ammesse, meno nodi — ### **e NON va presentato
> come un fenomeno emergente.** ### **E' la conseguenza aritmetica del cancello, e il referto
> deve dirlo con queste parole.**

---

## **ANNOTAZIONE del 2026-10-04 — DUE NOTE DAL GUARDIANO, e lo STOP era del MANDATO**

### **① LO STOP NON ERA DEL CODICE, ed e' il guardiano a dichiararlo.** Il mandato del `6b`
elencava ### **tre** file fuori dal simulatore; il censimento ne ha trovati ### **undici in
piu'**, e il guardiano dichiara che ### **li aveva gia' visti in una ricerca precedente** e
che la lista di tre era ### **la sua omissione.** ### ✅ **Quindi: `0` siti di CODICE non
previsti, e lo STOP e' dovuto AL MANDATO, non al codice.** *(Il suo censimento indipendente
coincide col mio: `7` righe di codice tutte previste, `6` commenti fuori lista, `15` file
fuori — dove io ne conto `14`, e la differenza e' nei due difetti del mio strumento,
dichiarati e in coda.)*

### **② «UN SIGILLO SI RIGIRA AL SUO COMMIT», e questa regola NON E' SCRITTA in `CLAUDE.md`.**

> **`72` sigilli su `79` leggono il simulatore DAL DISCO.** Quindi *«ri-girabile»* non vuol
> dire *«gira sull'`HEAD` di oggi»*: vuol dire ### **ri-girabile AL SUO COMMIT**. ### **Ed e'
> per questo che l'inventario registra IL BLOB** — il blob non e' una decorazione, e' ### **la
> coordinata che rende il sigillo ri-eseguibile.**

### ⚠ **CONSEGUENZA SUL PAR.6, e non la scrivo in `CLAUDE.md`:** la frase *«un sigillo non
piu' ri-girabile e' un difetto nuovo»* ### **va letta con questa regola accanto**, altrimenti
ogni cura che cambia il simulatore trasformerebbe **tutti** i sigilli precedenti in difetti.
### ⛔ **Ma metterla in `CLAUDE.md` e' una DECISIONE DI LUCA, non mia e non del guardiano:**
sta qui come nota, e il par.6 resta come e'.

### ✅ **E PERCIO' `_sigillo_cura5_a13nascita.py` E `_sigillo_frazione_t.py` NON SI TOCCANO.**
Nelle loro voci d'inventario va **una riga** che dice a quale commit si rigirano e che dal
`6b` il cancello e' incondizionato. ### **`_sigillo_cura5_a13nascita.py` non aveva NESSUNA
voce d'inventario** *(verificato con `grep`)*: va creata, col commit e i blob.

### **I NUMERI DEI DUE SIGILLI, letti da `git` e non a memoria**

| sigillo | commit | blob del sigillo | blob del simulatore |
|---|---|---|---|
| `_sigillo_cura5_a13nascita.py` | **`7fcd9c7`** *(2026-09-25)* | `06c6b3f4` | **`d9f113e9`** |
| `_sigillo_frazione_t.py` *(referto intero)* | **`1927b45`** | `838fc5c9` | **`c18c9bf6`** |
| `_sigillo_frazione_t.py` *(complemento `C-bis`)* | **`f288eff`** | `94224cb7` | `c18c9bf6` |

### ⚠ **E il sigillo del `6a` ha DUE punti di sigillatura, non uno:** il referto intero e il
complemento girarono da ### **blob diversi dello stesso sigillo** *(`838fc5c9` e
`94224cb7`)*. ### **Registrarne uno solo renderebbe non ri-girabile metà del lavoro.**

### **③ I DUE DIFETTI DEL MIO CENSIMENTO restano in CODA**, per decisione del guardiano: si
contava da solo, e non riconosceva `_driver_prima.py` come reperto *(e' una copia del
**driver**, non del simulatore)*. ### **Un commit a se', DOPO il `6b`.**

---

## **ANNOTAZIONE del 2026-10-04 — IL SIGILLO DEL `6b` E' GIRATO SU UNA SCENA SBAGLIATA**

*(rilievo del guardiano su `f94ff2c`. **Si ANNOTA, non si riscrive**: par.8.)*

### ⛔ **LA CAUSA, letta dal codice e non dedotta:** in `_sigillo_legge_2lam.py` la funzione
`costruisci()` **scriveva A MANO** due attributi:

```python
m._NMASSE_VIDEO["n"]   = 2        # <- a mano
m._NMASSE_VIDEO["sep"] = 3.0      # <- a mano
```

mentre i sigilli del **4**, del **5** e del **`6a`** li **LEGGONO dal CLI del driver**:
`max(2, int(getattr(a, "nmasse", 2)))` e `float(getattr(a, "sep", 3.0))`.
### **E' un attributo a mano: `H-P3`.** ### **E il driver passa `--nmasse 3` e
`--sep 6.1158`** *(verificato stampando i token dell'argv)*, quindi la mia scena aveva
**`2208` nodi al passo 150** invece dei **`~12800`** della scena vera.

### **LE TRE CONSEGUENZE, tutte nel referto `f94ff2c`**

| cosa avevo scritto | che cos'e' davvero |
|---|---|
| *«il primo candidato arriva al passo **74**»* *(in `5f03401`, e anche in `REGISTRO_FISICA` e `FATTI_dal_codice`)* | ### **e' il 74 DI QUELLA SCENA.** Sulla scena del driver il primo candidato e' al **`42`** — ### **come avevo misurato IO nel `6a`** |
| *«le scene da 72 passi NON portano statistica del cancello»* | ### **FALSO** per la scena del driver |
| `B1` sulla scena `corta` **vuoto** | era vuoto ### **per questo**, non per una proprieta' della legge |

### 📌 **E LA COSA PEGGIORE NON E' IL NUMERO SBAGLIATO: e' che l'avevo CONTRADDETTO IO.** Nel
`6a` avevo misurato il primo evento al **42**, e nel `6b` ho scritto **74** ### **senza
accorgermi che i due numeri non potevano stare insieme** — stessa scena nominale, stesso seme.
### **Due misure incompatibili sullo stesso oggetto, e non ho fatto la domanda.** *(`P1`: non
usare l'associazione senza verificare lo storico.)*

### **LA RIMISURA INDIPENDENTE DEL GUARDIANO** *(Linux, numpy 2.5.3, seme 11, 72 passi,
lockstep su **tutti** gli attributi)*:

| | |
|---|---|
| **con** `--mitosi-2lam` | *prima* e *oggi* **identici** salvo i 4 contatori nuovi · `n = 12812`, archi `471575` |
| **senza** | `_sm_trd_mitosi` **`16 → 0`**, `_sm_trd0_mitosi` **`14 → 0`**, prima differenza al passo **`42`** |
| ### **e OGGI SENZA FLAG** | da' `n = 12812`, archi `471575`, `_g_sm_nascite = 18`: ### **gli stessi numeri del PRIMA CON FLAG** |

### **LA CURA, in quattro punti**

| | |
|---|---|
| **①** | `costruisci()` legge `nmasse` e `sep` **dal CLI**, piu' un **controllo che PUO' fallire**: il sigillo stampa `n` e gli archi alla costruzione e **FALLISCE** se `nmasse`/`sep` non coincidono con quelli dell'**argv**. ### ⚠ **E il riferimento si estrae DAI TOKEN DELL'ARGV, non da `costruisci`:** un controllo calcolato dalla funzione che deve controllare sarebbe ### **sempre d'accordo con lei** — il controllo del controllore fatto dal controllore |
| **②** | **braccio `E`, nuovo:** ### **OGGI SENZA FLAG deve essere IDENTICO AL BYTE a PRIMA CON FLAG**, su tutte le scene. ### **E' la prova piu' diretta che il flag e' inerte**, e ### **ne' `A` ne' `B` la danno:** `A` confronta *prima CON* contro *oggi CON*, `B` misura *oggi SENZA* contro *prima SENZA*. ### **Nessuno dei due incrocia i due stati che DEVONO coincidere.** |
| **③** | `B1` corretto: se nel ### **PRIMA** i troncamenti sono **gia' zero**, il braccio stampa ### **VUOTO e NON PASSA.** Uno zero atteso vale solo se accanto c'e' un numero **diverso da zero** |
| **④** | il sigillo intero **rigirato sulla scena giusta**, referto con un **nome proprio nuovo**. ### **Il referto `f94ff2c` resta come REPERTO: non si cancella e non si riscrive** |

### ⚠ **UN LIMITE MINORE, da registrare e non curare qui** *(il guardiano lo mette in coda)*:
**`_g_m2l_tw_rif` e' una LISTA nello stato della rete che CRESCE SENZA LIMITE** per tutto il
run. Nelle scene misurate sono `19` valori, quindi non e' un problema **oggi** — ma e'
### **una struttura non limitata dentro `net.__dict__`**, e un run lungo la farebbe crescere
con ogni rifiuto. ### **La forma si decide nel commit della cura dei due difetti del
censimento**, che e' il prossimo in coda.
