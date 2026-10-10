# LE REGOLE DI GESTIONE DELL'ERA `2` — **il mandato `5` di `6`, l'ULTIMO della coda**

> ### 📌 **IL RITO:** questo file si committa e si pusha ### **PRIMA del lavoro**, così
> l'ordine è ### **verificabile da git** invece che **asserito da me**.

> **I cinque punti:** `1` ogni regola è una ### **voce** · `2` la sezione di `CLAUDE.md`
> si ### **GENERA** · `3` una sezione ### **«LAVORARE NELL'ERA `2`»** · `4` il dettaglio in
> `doc/REGOLE/` ### **legato alla voce** · `5` i ### **controlli**, e
> `CLAUDE.md` ### **rigenerato BYTE-IDENTICO**.

---

## `1.` RAGIONAMENTO PRELIMINARE — ### **cosa credo PRIMA di guardare, e cosa NON so**

### **LA FORMA DI QUESTO MANDATO, e perché è l'ultimo**

### ⭐ **QUESTO MANDATO CHIUDE IL CERCHIO, e il mandato stesso lo dice:** il `par.0` di
`CLAUDE.md` pretende già che *«una regola nuova entra qui con al massimo `3` righe, il
dettaglio in `doc/REGOLE/par<N>.md`»*, e `csv/_struttura_regole.py`
### **impedisce le catene.** ### ⛔ **Ma quelle `3` righe le scrivo IO a mano, e niente
verifica che esistano davvero la voce e il file.** ### ✅ **Generarle dall'indice rende la
struttura VERA invece che RISPETTATA.**

### ⚠ **E IL RISCHIO DI QUESTO MANDATO E' DIVERSO DA TUTTI I PRECEDENTI: tocca il file che
GOVERNA il lavoro.** ### ⛔ **Un errore qui non fa cadere un collaudo: fa sparire una
regola** — e una regola sparita ### **non si vede, perché il file è più corto e sembra più
pulito.** ### ✅ **Quindi il presidio che conta non è «il generato coincide»: è
### **NESSUNA REGOLA SI PERDE**, confrontata con `git`.

### **CHE COSA HO GIA' MISURATO, prima di scrivere questo file**

| | la misura | il numero |
|---|---|---|
| `a` | `CLAUDE.md` | ### **`295` righe** su un tetto di `400` *(`H-RIGHE`)* — ### **`105` di margine** |
| `b` | le regole ### **citate** in `CLAUDE.md` | ### **`23`**, e ### ✅ **TUTTE hanno già una voce** *(`14` `PRESIDIO`, `9` `STANDARD`)* |
| `c` | i file di dettaglio | ### **`12`** in `doc/REGOLE/`, uno per paragrafo |

### ⭐ **E IL `(b)` CAMBIA IL LAVORO: il punto `1` non deve creare `23` voci, deve creare
quelle che MANCANO** — e il mandato dice quali cercare: le regole ### **nate nei mandati
del `2026-10-09`.**

### **CHE COSA NON SO, e lo scrivo adesso**

1. ### **quante regole di gestione nate il `2026-10-09` NON hanno voce.** Il mandato ne
   nomina ### **otto** e dice *«e le altre: elencate TUTTE nel referto»* — ### ⛔ **quindi
   il censimento è parte del lavoro, non un preliminare**, e il numero
   ### **lo scrivo dopo averlo visto.**
2. ### **se il dettaglio di una regola possa stare in `doc/REGOLE/par<N>.md`** quando la
   regola ### **non appartiene a un paragrafo.** Il punto `4` dice
   *«`doc/REGOLE/<file>.md` legato alla sua voce»*: ### ⚠ **i `12` file di oggi sono
   `par<N>.md`, cioè legati a un PARAGRAFO, non a una VOCE** — e questa è
   ### **una differenza che devo guardare, non assumere.**
3. ### **se `CLAUDE.md` si possa generare SENZA perdere la prosa.** I paragrafi non sono
   elenchi di regole: ### **sono testo con dentro delle regole.** ### ⛔ **Generare
   <<la sezione delle regole>> presuppone che esista UNA sezione, e oggi
   NON ESISTE: le regole stanno nel par.`11` E nel par.`12` E dentro gli altri.**

---

## `2.` PROGETTAZIONE DEL RAGIONAMENTO

### **L'ORDINE, e perché**

| | che cosa | perché qui |
|---|---|---|
| `1` | ### **IL CENSIMENTO**: quali regole di gestione esistono, quali hanno voce, quali no | ### ⛔ **prima di generare una sezione devo sapere CHE COSA ci va** — e il mandato dice *«elencate TUTTE nel referto»* |
| `2` | ### **LE VOCI che mancano**, ognuna col ### **file di dettaglio** e ### **CHI LA FA RISPETTARE** | il punto `1`, e ### **<<chi la fa rispettare>> è il campo che rende `A9` verificabile** |
| `3` | ### **IL GENERATORE** della sezione, e il presidio che ### **rifiuta la modifica a mano** | il punto `2` |
| `4` | ### **«LAVORARE NELL'ERA `2`»** | il punto `3`, e si scrive ### **dopo** il generatore perché deve starci dentro il tetto |
| `5` | ### **I CONTROLLI** e il referto | il punto `5` |

### **LE LETTURE, FISSATE ADESSO**

| | la misura | la lettura che fisso PRIMA |
|---|---|---|
| ### **le regole perse** | l'insieme delle regole citate ### **PRIMA e DOPO**, da `git` | ### ⛔ **DEVE essere `0`.** ### **È il solo controllo che conta davvero**, e `CLAUDE.md` più corto ### **non è un successo: è un sospetto** |
| `CLAUDE.md` | le righe | ### **DEVE restare `<= 400`** *(`H-RIGHE`)*, e ### **se la sezione generata lo sfonda, si accorcia la SINTESI, non si alza il tetto** |
| il rigenerato | byte | ### **DEVE coincidere**, e la modifica a mano ### **DEVE essere rifiutata** — nei due versi |
| le regole duplicate | stesso contenuto in due voci | ### **SEGNALE**, non errore: il mandato lo dice così |
| `valida` | tutti i presidi | ### **DEVE passare**, e i segnali ### **non devono crescere** *(oggi `19`)* |

### **CHE COSA MI FAREBBE FERMARE**

| | il caso | che faccio |
|---|---|---|
| `a` | la sezione generata ### **non ci sta** nelle `400` righe | ### **FERMO e lo scrivo.** ### ⛔ **Alzare `H-RIGHE` sarebbe la manopola che `A1` vieta**, ed è la stessa cosa che `P-MOD` mi ha impedito ieri sul tetto delle righe |
| `b` | una regola ### **si perde** | ### ⛔ **FERMO.** È il difetto che questo mandato può introdurre, ed è ### **il solo che non si vede guardando il file** |
| `c` | il dettaglio di una regola ### **non ha un file** | ### **lo creo**, perché il punto `4` lo pretende — ### **ma se una regola non ha niente da dire oltre la sua riga, LO DICO** invece di gonfiare un file |
| `d` | generare la sezione ### **cambierebbe il senso** di un paragrafo | ### **FERMO.** ### **`CLAUDE.md` è il file che governa il lavoro: un errore qui non fa cadere un collaudo, FA SPARIRE UNA REGOLA** |

### **LA STELLA POLARE** *(`L-STELLA`)*

### ⚠ **NON SI APPLICA, e il perché è parte della risposta:** questo mandato
### **non tocca `primo_ordine/`**, non aggiunge nessuna legge, non fa girare nessuna scena.
### **Tocca il FLUSSO DI LAVORO.** ### ⭐ **Ma una delle cinque domande ha una risposta che
scrivo adesso: <<quante leggi aggiunge?>> — ZERO, e il mandato è l'unico della coda che
può RIDURRE il numero delle regole**, perché ### **generarle dall'indice fa emergere i
duplicati** *(il punto `5` li chiede come segnale)*. ### **`9-ter` dice che a parità di
effetto vince chi ne ha meno.**

---

## `3.` TODO DEL NEXT STEP

- [ ] il **CENSIMENTO** delle regole di gestione: quali hanno voce, quali no, e **quali nate il `2026-10-09`**
- [ ] le **voci che mancano**, ognuna col **file di dettaglio** e **CHI LA FA RISPETTARE**
- [ ] il **generatore** della sezione di `CLAUDE.md`, e il presidio che **rifiuta la modifica a mano** — nei due versi
- [ ] la sezione **«LAVORARE NELL'ERA `2`»**
- [ ] i **controlli**: `valida`, **byte-identico**, **zero regole perse**, duplicati come **segnale**
- [ ] il **referto** `doc/REFERTO_regole_era2.md`, e `_avanzamento.md`
