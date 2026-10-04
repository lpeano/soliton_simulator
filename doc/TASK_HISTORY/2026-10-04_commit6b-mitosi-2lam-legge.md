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
