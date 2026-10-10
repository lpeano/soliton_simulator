# COME SI AGGIUNGE UNA LEGGE — **dall'idea al referto**

> ### ⛔ **QUESTA GUIDA SI ESEGUE, e un collaudo la esegue DAVVERO** *(`python
> primo_ordine/_collauda_guida.py`)*. ### ⭐ **Quindi non può invecchiare in silenzio: se
> un passo non funziona più, il collaudo FALLISCE.**

> ### 📌 **E OGNI PASSO DICE SE E' MECCANICO O DI DECISIONE.** ### **Un passo MECCANICO si
> esegue** *(un comando, un file, un confronto)*. ### ⛔ **Un passo di DECISIONE non si
> esegue: aspetta Luca** — e il collaudo verifica che sia ### **dichiarato tale**, non che
> si possa fare.

### ⚠ **E LA DISTINZIONE NON E' UNA COMODITA': è il punto che il task history di questo
mandato aveva previsto.** *«Se la guida contiene un passo che richiede una DECISIONE, quel
passo **non è eseguibile** — e allora la guida va scritta in modo che **ogni passo
eseguibile sia MECCANICO**»*.

---

## LA TABELLA DEI PASSI

| | il passo | tipo |
|---|---|---|
| `1` | **la DECISIONE che governa la legge** è `presa` nell'albero? | ### ⛔ **DECISIONE** |
| `2` | la **riga nella tabella** `primo_ordine/leggi/leggi.yaml` | ### ✅ **MECCANICO** |
| `3` | `python primo_ordine/_genera.py` — **il codice NON si scrive a mano** | ### ✅ **MECCANICO** |
| `4` | la **voce nell'indice** e la riga del registro dell'era `2` | ### ✅ **MECCANICO** |
| `5` | il **SIGILLO**, sul modello di `primo_ordine/sigilli/_modello.py` | ### ⛔ **DECISIONE** *(i criteri)* + ### ✅ **MECCANICO** *(il rito)* |
| `6` | le **cinque domande** di `doc/STELLA_POLARE.md` nel task history | ### ⛔ **DECISIONE** |
| `7` | la **scheda** in `doc/REGISTRO_FISICA.md` | ### ✅ **MECCANICO** *(`H-REG-R` la pretende)* |
| `8` | il **referto**, e `python primo_ordine/collauda.py` | ### ✅ **MECCANICO** |

---

## `1.` — ### ⛔ **LA DECISIONE CHE GOVERNA LA LEGGE** *(passo di DECISIONE)*

> ### **Non si scrive una legge prima della decisione che la governa:** sarebbe
> ### **una decisione presa di nascosto.**

```
python csv/_albero_era2.py          # i nodi, e quali sono `presa`
```

### ⛔ **Se il nodo che governa la tua legge NON è `presa: true`, FERMATI.** La fase `F3`
del piano *(`doc/PIANO_era2.md`)* ha come criterio d'ingresso
### **`F2` chiusa per QUELLA decisione** — non per tutte: ### **l'albero è un ordine
PARZIALE**, ed è a questo che serve.

### ⚠ **E oggi `0` nodi su `10` sono `presa`**, quindi ### **questo passo ferma tutto** —
ed è giusto che lo dica una guida, non che lo si scopra dopo.

---

## `2.` — ### ✅ **LA RIGA NELLA TABELLA** *(MECCANICO)*

**Si scrive in `primo_ordine/leggi/leggi.yaml`**, e ### ⛔ **niente si scrive a mano sotto
`primo_ordine/termini/`.** Il formato intero sta ### **in testa a quel file**; qui sta
### **cosa non si può omettere:**

| il campo | che cosa | chi lo pretende |
|---|---|---|
| `id` | `[A-Z][A-Z0-9-]{3,}`, almeno `4` caratteri | `P-ID` |
| `tipo` | `termine_nodo` · `termine_arco` · `regola` · `osservatore` | lo schema |
| `prova` | ### **`false` per una legge vera** | il conto delle leggi |
| `espressione` | sympy, e ### **nessun simbolo di posizione** | `A17` |
| `ambito` | le variabili che ### **PUO'** leggere | lo schema |
| `parametri` | ognuno con `valore`, `origine` **e** `dimensione` | `A1`, `P-DIM` |
| `dimensione` | sull'osservatore; un termine è ### **`E^1`** per forza | `P-DIM` |
| `simmetrie` | ### **almeno `U1-FASE-GLOBALE`** | `P-SIM` |
| `conserva` | `NORMA`, `ENERGIA`, o ### **la lista VUOTA** | `P-SIM` |
| `assiomi` | quali soddisfa — ### **anche vuota, e allora lo dice** | lo schema |
| `scheda` | il testo da cui si genera `doc/leggi_era2/<id>.md` | `P-E7` |

### ⛔ **E `origine` NON E' UNA FORMALITA':** *«un numero senza origine ### **E' UNA
MANOPOLA**»* — `A1`. ### **Se devi SCEGLIERE un numero per far funzionare la legge, il
meccanismo va DERIVATO, e il posto per dirlo è `doc/DA_DECIDERE_LUCA.md`.**

---

## `3.` — ### ✅ **SI GENERA** *(MECCANICO)*

```
python primo_ordine/_genera.py
```

### 📌 **Che cosa fa:** valida la tabella *(forma, divieti, ### **dimensioni**,
### **simmetrie**)*, e ### **genera** `primo_ordine/termini/<id>.py`, la scheda
`doc/leggi_era2/<id>.md` e `primo_ordine/stato.py`.

### ⛔ **E SE LA TABELLA NON PASSA, NON GENERA NIENTE** — non genera a metà. ### **I
messaggi dicono quale legge e perché.**

---

## `4.` — ### ✅ **LA VOCE E LA RIGA DEL REGISTRO** *(MECCANICO)*

```
python csv/indice.py crea-lotto <lotto.jsonl>      # la voce della legge
python csv/indice.py era2-lotto <lotto.jsonl>      # la riga del registro dell'era 2
python csv/indice.py storico-commit                # DOPO il commit, sempre
```

### ⛔ **E LA RIGA DEL REGISTRO VA NELLO STESSO COMMIT DELLA TABELLA**, perché
`P-E6` lo pretende: la riga porta ### **l'IMPRONTA della legge**, e se la tabella cambia
senza di lei ### **il registro dichiara l'impronta di una tabella che non esiste più.**

---

## `5.` — ### ⛔✅ **IL SIGILLO** *(i criteri sono una DECISIONE, il rito è MECCANICO)*

**Il modello:** `primo_ordine/sigilli/_modello.py`. ### **Quattro bracci:**

| | il braccio | che cosa prova |
|---|---|---|
| `zero` | il coefficiente a ### **ZERO** | il *«prima»* è ### **byte-identico PER COSTRUZIONE** — non una copia patchata a mano |
| `g != 0` | il coefficiente ### **acceso** | che la legge ### **cambi qualcosa**, e di quanto |
| `positivo` | una grandezza che ### **POTEVA fallire** | che il sigillo ### **guardi davvero** quella grandezza |
| `deve-fallire` | ### **OBBLIGATORIO** | `P-E9` lo pretende: ### **un sigillo che dice di avere criteri senza averli è PEGGIO di uno senza criteri** |

### ⛔ **I CRITERI SI FISSANO PRIMA DI VEDERE I NUMERI**, nel task history — ed è
### **un passo di DECISIONE**, non un comando.

---

## `6.` — ### ⛔ **LE CINQUE DOMANDE** *(passo di DECISIONE)*

`doc/STELLA_POLARE.md`, nel task history, ### **per iscritto** — anche solo con
*«non si applica, perché …»*, e ### **il «perché» è parte della risposta** *(`L-STELLA`)*.

---

## `7.` — ### ✅ **LA SCHEDA IN `REGISTRO_FISICA`** *(MECCANICO)*

### ⛔ **`H-REG-R` RIFIUTA il commit** se una legge cambia senza la diff
### **dentro la sezione** di quella legge. ### **Non è una raccomandazione: è un hook.**

---

## `8.` — ### ✅ **IL REFERTO E I TEMPI** *(MECCANICO)*

```
python primo_ordine/collauda.py                     # tutti i collaudi, coi TEMPI
```

### 📌 **E i numeri del referto escono da uno script** *(`L-NUMERI`)*: ### **un numero
ricopiato non ha provenienza.**

---

## ⛔ **I TRE ERRORI CHE QUESTA GUIDA ESISTE PER IMPEDIRE**

| | l'errore | chi lo ferma |
|---|---|---|
| `1` | scrivere il codice del termine ### **a mano** | `P-E1`: il file generato e la tabella devono coincidere |
| `2` | una legge con un numero ### **senza origine** | `A1`, e lo schema |
| `3` | una legge scritta ### **prima della decisione che la governa** | ### **nessuno**, e per questo è ### **il passo `1`** |

### ⚠ **E IL TERZO NON HA UN PRESIDIO, e lo dico qui:** `P-ALB` verifica che una decisione
non sia ### **PRESA** prima delle sue, ### **ma nessuno verifica che una LEGGE non sia
scritta prima della sua DECISIONE.** ### ⛔ **È un buco, è dichiarato, e il posto dove si
chiude è la fase `F3`.**
