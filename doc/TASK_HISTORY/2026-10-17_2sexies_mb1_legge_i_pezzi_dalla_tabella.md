# `2-sexies` — **`M-B1` NON COPRE LA LEGGE CHE GIRA**

*(mandato unico del guardiano del `2026-10-17`, punto `2`, su mandato di Luca.
Base: `ed6e300d`. E' **il `2` dell'ordine nuovo**, dopo il pezzo `8`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *e il difetto l'ho usato IERI come prova*

### ⛔⛔ **IL DIFETTO, misurato**

`_misura_mb1.PEZZI` e' **una lista A MANO di `6` id**:

```
CAMM-GROVER · CAMM-SPOSTAMENTO · CAMM-GROVER-VUOTO · CAMM-SPOSTAMENTO-VUOTO ·
CAMM-MONETA-SPIN · CAMM-SATURAZIONE
```

> ### ⛔ **CONTIENE `CAMM-SATURAZIONE`**, che dal `2026-10-15` e' ### **FUORI
> dall'ordine**; e ### **NON CONTIENE `CAMM-MATERIA-VUOTO`**, che e' ### **la legge che
> GIRA.**
> ### ⛔⛔ **E IERI L'HO USATO COME PROVA:** ho scritto *«`M-B1` PASSA: tutti i `12` pezzi
> coincidono AL BIT»* per giustificare lo spostamento di `percorri_tick` — e
> ### **quei `12` pezzi non contenevano il flusso che gira.**
> ### ✅ **La conclusione reggeva per altri due numeri** *(la distanza del passo intero,
> `0.000000e+00`, che il flusso lo CONTIENE; e la prova al carattere)*, ### **ma la frase
> che ho scritto era appoggiata al numero sbagliato.**

### ⭐ **E IL MANDATO CHIEDE LA REGOLA GIUSTA:** `[[STRUMENTO-LEGGE-DALLA-TABELLA]]` —
### **i pezzi si leggono dall'ordine di composizione**, e la misura ### **ALZA** se un
pezzo dell'ordine ### **non e' misurabile al bit.**

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE**

| | credo che… | e ### **NON LO SO** |
|---|---|---|
| `a` | i pezzi ### **DISTINTI** dell'ordine siano ### **`6`**, come oggi: l'ordine ha `12` voci ma e' ### **palindromo**, quindi le ripetizioni si contano una volta | ### ⚠ **se fossero `5` o `7`, il conteggio del referto cambia**, e il mandato chiede ### **i numeri vecchi accanto** |
| `b` | il ### **set** cambi: ### **fuori la saturazione, dentro `CAMM-MATERIA-VUOTO`** | — |
| `c` | ci sia un ### **secondo falso-uno nascosto**: `contro()` confronta i blocchi ### **per POSIZIONE** e asserisce solo `len(ba) == len(bb)` | ### ⛔ **se i due alberi avessero ordini DIVERSI, confronterebbe pezzi DIVERSI credendoli uguali** — e non lo so, perche' ### **nessuno l'ha mai provato** |

### ⛔⛔ **E SE `(c)` E' VERO, E' PIU' GRAVE DEL DIFETTO DEL MANDATO:** leggere i pezzi
dalla tabella ### **fa diventare la lista DIVERSA FRA I DUE ALBERI** se la tabella e'
cambiata — cioe' ### **la cura del punto `2` APRE quel buco**, se non si chiude insieme.
### ✅ **Quindi il file dei byte deve portare ANCHE GLI ID**, e `contro()` deve
### **asserire che le due liste coincidono.**

---

## 2. PROGETTAZIONE — *i passi, i criteri, e cosa mi FERMA*

| | il passo | il criterio |
|---|---|---|
| `1` | `PEZZI` ### **si deriva**: gli id ### **DISTINTI** dell'ordine di composizione, nell'ordine di prima apparizione | il conteggio e' ### **un numero del referto**, coi vecchi accanto |
| `2` | la misura ### **ALZA** se un pezzo dell'ordine ### **non e' applicabile** *(non e' in `OPERATORE`, o il motore non ha quell'operatore)* | il messaggio ### **nomina l'id** |
| `3` | il file dei byte porta ### **gli ID**, e `contro()` ### **asserisce che le due liste coincidono** | ### ⛔ **se non coincidono, il confronto NON PARTE:** confrontare pezzi diversi credendoli uguali e' ### **peggio di non confrontare** |
| `4` | ### **il caso che DEVE fallire:** un id nell'ordine che la misura ### **non sa applicare** | ### **ALZA**, e il braccio lo verifica ### **sulla chiave giusta** |
| `5` | ### **il controllo positivo:** `CAMM-MATERIA-VUOTO` e' ### **fra i pezzi confrontati**, e coincide ### **AL BIT** contro `8c7b928` | se non coincidesse, ### **STOP e relaziono** |
| `6` | il referto dice ### **il set nuovo e quello vecchio**, e il conteggio ### **coi numeri di prima** | — |

### ⛔ **E UNA COSA CHE NON FARO':** non tolgo `CAMM-SATURAZIONE` *«perche' e' superata»* —
### **esce DA SOLA**, perche' ### **non e' nell'ordine.** ### **La differenza conta:** se
Luca la rimettesse nell'ordine, ### **rientrerebbe da sola.**

---

## 3. TODO

1. `primo_ordine/_misura_mb1.py`: `PEZZI` ### **dall'ordine**, l'assert di applicabilita',
   gli ### **id nel file dei byte**, e `contro()` che ### **li confronta.**
2. i ### **due bracci** *(il caso che deve fallire, il controllo positivo su
   `CAMM-MATERIA-VUOTO`)* nel `--collaudo`.
3. il referto, con ### **il set nuovo e quello vecchio.**
4. la relazione, la RIPRESA e la riga della coda.
