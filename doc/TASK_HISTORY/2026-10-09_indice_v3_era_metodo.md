# INDICE `v3`: **l'era delle voci di metodo e strumenti**

> **Mandato di Luca del 2026-10-09**, quattro punti, **un commit per punto**. Nessuna corsa,
> simulatore `b8c21049` intatto.
>
> ### ⚠ **Si committa e si pusha PRIMA del lavoro** *(par.8)*.

---

## ① RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐ **IL GUARDIANO DICHIARA UN SUO ERRORE, E IO L'HO APPLICATO**

*«La regola «metodo = era `ENTRAMBE`» era ### **troppo grossa**»*. ### ⛔ **E l'ho applicata
io**, nel punto `2` della chiusura dei segnali: `58` voci `CRITERIO`/`FISICA` → `METODO`, e
### **nessuna di quelle `58` ha cambiato era** — ma `35` voci di `METODO` e
`INFRASTRUTTURA` erano `ENTRAMBE` ### **per inerzia**, non per lettura.

### **LA DISTINZIONE NUOVA, come la scrive il guardiano:**

| | |
|---|---|
| ### **`ENTRAMBE`** | una ### **REGOLA DI LAVORO** o ### **uno strumento che sopravvive** |
| ### **era `1`** | cio' che riguarda un ### **OGGETTO CONCRETO dell'era `1`** — un sigillo di una cura, la scena `(ii)`, il pilota, un `.pkl`, il blob `b8c21049`, ### **una funzione o un flag di `soliton_simulator.py`** |

### **CHE COSA CREDO, E PUO' RIVELARSI FALSO**

**`a` Le due misure del punto `1` tornano, e le ho fatte PRIMA di scrivere questo file.**
`F7` esteso *(era `1`, ### **qualsiasi dominio**)* violerebbe ### **su `16` voci**, e sono
### **esattamente** le `14` `CENS-*` `APERTE` piu' `D32-CONTATORE` e `RAMI-OFF-CURA2` —
### **cioe' esattamente quelle che il mandato nomina.** ### **E anche stavolta `F7` e' sicuro
PERCHE' LA CURA VIENE PRIMA**, non per caso.

**`b` Le `35` voci del punto `2` esistono tutte**, sono ### **tutte `ENTRAMBE`/`APERTA`**, e
nessuna e' `CHIUSA`: quindi vanno tutte a ### **era `1`/`SOSPESA`.**

**`c` Credo che le eccezioni del punto `2` siano ZERO**, e questa e' la previsione che puo'
cadere. ### **I due casi limite li ho letti:** `REGISTRO_FISICA:A1` e `S1` dicono *«flag
SPENTO = byte-identico, firma dei byte, un processo per braccio»* — una ### **FORMA** che vale
per qualunque era. ### ⛔ **Ma il soggetto e' un FLAG**, e la forma generica ### **vive gia'
in `doc/PATTERN_DI_PROVA.md`**, che e' il posto delle regole di prova: ### **questa voce e' il
criterio di QUEL sigillo.** ### **Se sbaglio, e' qui che sbaglio.**

**`d` `F8` segnalera' poche voci**, e credo ### **fra `3` e `15`**: le `ENTRAMBE` scendono a
`138`, e i marcatori sono ### **stretti** *(un flag si riconosce da `--`, non dalla parola
«flag»)*.

### ⛔ **CHE COSA NON SO, E NON INVENTO**

1. **Se fra le voci che il mandato dice di LASCIARE `ENTRAMBE` ce ne sia qualcuna che `F8`
   segnala.** `PRESIDIO-RIFIUTO-SOLO-SIGILLI` ha *«sigilli»* nel nome. ### **Se segnala, lo
   ELENCO e non lo correggo**, e il mandato lo dice: *«i segnali che restano NON si
   correggono»*.
2. **Quanto sia stretto «un oggetto concreto».** Un `.pkl` lo e'; *«il comparatore del
   lockstep»* ### **lo e' meno**, ed e' una mia lettura. ### **Va nel referto come tale.**
3. **Se `F8` debba guardare anche le `CHIUSA`.** Il mandato dice ### **«stato non `CHIUSA`»**,
   e lo prendo alla lettera: una voce chiusa ### **non si sposta piu'.**

---

## ② PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### ⛔ **L'ORDINE NON E' LIBERO, ed e' la seconda volta in due giri**

> Il punto `1` dice ### **«PRIMA porta a `SOSPESA` le voci che oggi lo violano»**, e poi si
> estende `F7`. ### **Un presidio bloccante si accende DOPO che cio' che blocca e' curato**,
> altrimenti ### **il lotto che lo curerebbe non e' piu' applicabile** — `F7` fa fallire la
> validazione, e la validazione gira ### **dentro `aggiorna-lotto`.**
>
> ### **E dentro il punto `2` l'ordine e' nello STESSO lotto:** `era = 1` e `stato = SOSPESA`
> ### **insieme**, perche' `era 1` + `APERTA` ### **e' esattamente cio' che `F7` vieta.**

### **I PASSI**

| | il passo | che cosa DECIDE |
|---|---|---|
| `1a` | le `16` voci che violano `F7` esteso → `SOSPESA` | la regola vale per ### **qualsiasi dominio**, non solo `FISICA` |
| `1b` | `F7` esteso, ### **resta un ERRORE** | il `pre-commit` impedisce ### **una voce dell'era `1` che non sia `SOSPESA`/`CHIUSA`/`SUPERATA`** |
| `2` | le `35` a era `1`/`SOSPESA`, ### **dominio e classe INVARIATI** | la distinzione ### **regola-di-lavoro contro oggetto-concreto** |
| `3` | `F8`, ### **SEGNALA** | cio' che resta `ENTRAMBE` ### **e nomina un oggetto dell'era `1`** |
| `4` | controlli + referto `doc/REFERTO_indice_v3_era_metodo.md` | — |

### **LE LETTURE SI FISSANO QUI, PRIMA DI VEDERE I NUMERI**

| | la lettura |
|---|---|
| il punto `1a` | ### **`16` voci**, e sono quelle che il mandato nomina. ### **Un numero diverso e' un difetto mio, non un dato** |
| il collaudo di `F7` | ### **DEVE scattare** su `CENS-A4` a `72e452f` *(in una COPIA)*. Se non scatta ⇒ **FERMO** |
| dopo il punto `1a` | ### **`0`** voci dell'era `1` con stato diverso da `SOSPESA`/`CHIUSA`/`SUPERATA`; se non e' `0`, ### **`F7` non si accende** |
| il punto `2` | `era ENTRAMBE` ### **`173` → `138`**; `era 1` ### **`461` → `496`.** Le eccezioni: ### **previste ZERO** |
| il collaudo di `F8` | ### **DEVE scattare su `T3a` a `72e452f`**, ### **NON deve** su `P6` ne' su `FALSO-ZERO`. Meno di `3` su `3` ⇒ **FERMO** |
| `F8` sull'indice vero | fra `3` e `15` segnali |
| il collaudo intero | ### **almeno `29` su `29`** *(i `26` di oggi piu' `1` di `F7` e `3` di `F8`)* |

### ⛔ **CHE COSA MI FA FERMARE**

1. **Le voci che violano `F7` esteso non sono `16`** ⇒ la mia misura o la lista del mandato
   non coincidono ⇒ ### **lo scrivo prima di toccare niente.**
2. **`CENS-A4` non scatta** nel collaudo ⇒ `F7` non guarda cio' che credo.
3. **`P6` o `FALSO-ZERO` scattano in `F8`** ⇒ i marcatori sono ### **troppo larghi**, e la
   parola *«flag»* o *«blob»* ### **non e' un oggetto concreto.**
4. **Una delle `35` risulta una REGOLA per l'era `2`** ⇒ ### **NON la sposto**, e la frase va
   nel referto. ### **E se sono piu' di `5`, la distinzione del guardiano e' piu' fine di
   come l'ho capita, e lo dico invece di applicarla.**
5. **`F8` segnala una voce che il mandato dice di LASCIARE `ENTRAMBE`** ⇒ ### **la elenco e
   NON la sposto**: un segnale su una decisione del mandato ### **e' una domanda, non un
   difetto.**

### **`L-STELLA`: le cinque domande di `doc/STELLA_POLARE.md`**

### ⛔ **NON SI APPLICA, e il perche' e' parte della risposta:** nessuna legge cambia, il
simulatore non si tocca *(`b8c21049`)*, niente gira. Si sposta ### **l'era di `51` voci** e si
accendono ### **due presidi** sull'indice dei difetti. ### **Le cinque domande chiedono di un
gradino di robustezza fisica, di numeri o leggi aggiunti, del verso EM-curvatura e di
emergente-contro-imposto: su un cambiamento che non entra nel simulatore NON HANNO UN
SOGGETTO.**

### ⚠ **Ma una cosa va detta, come per il punto `2` del giro scorso:** `era ENTRAMBE` perde
### **`35` voci su `173`, cioe' un quinto**, e `era 1` ne guadagna altrettante. ### **Non e'
una decisione di fisica** — e' ### **un criterio di classificazione del guardiano**, che
dichiara di aver sbagliato il precedente — e ### **tutte restano `SOSPESE`**, quindi
### **non cambia nulla per l'era `2`, solo l'ordine.** ### **Chi legge i conteggi di ieri e di
domani deve trovare scritto perche'.**

---

## ③ TODO DEL NEXT STEP — *operativo*

- [ ] **`1a`** le `16` a `SOSPESA` *(14 `CENS-*`, `D32-CONTATORE`, `RAMI-OFF-CURA2`)*.
      ### **PRIMA di `F7`.**
- [ ] **`1b`** `F7` esteso a ### **qualsiasi dominio**, resta un ERRORE, piu' il braccio su
      `CENS-A4` a `72e452f`.
- [ ] **`2`** le `35` a era `1`/`SOSPESA`, ### **dominio e classe invariati**, `era` e `stato`
      ### **nello stesso lotto**. Le eccezioni ### **nel referto, con la frase.**
- [ ] **`3`** `F8` *(segnala)*, i tre bracci di collaudo, e i segnali ### **elencati voce per
      voce con la frase, NON corretti.**
- [ ] **`4`** controlli + `doc/REFERTO_indice_v3_era_metodo.md`, con ### **l'errore del
      guardiano dichiarato.**
- [ ] **par.6** a ogni commit: **inventario** e **par9** *(`F7` esteso, `F8`, la distinzione
      regola-contro-oggetto)*. ### **FISICA: non si applica.**
- [ ] **`storico-commit`** dopo ogni commit, e ### **le due VISTE GENERATE nel `git add`** —
      nel giro scorso le ho dimenticate.
