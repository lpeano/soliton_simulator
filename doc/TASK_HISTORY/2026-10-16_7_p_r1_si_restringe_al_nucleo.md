# `7` — **`P-R1` SI RESTRINGE AL NUCLEO DELLA FISICA, E DIVENTA BLOCCANTE**

*(decisione di Luca del `2026-10-16` alle `19:33`. Base: `c4f60603`. Il referto del pezzo
`4` e' **gia' committato** in `6657ce93`, come il mandato chiede.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *e DUE premesse del mandato non tornano*

### ⭐⭐ **IL NUCLEO, DERIVATO: `9` FILE** *(e non si scrive a mano)*

La chiusura degli import, dalle **radici dichiarate** `passo.py` · `motore.py` ·
`materia_vuoto.py` · `saturazione.py`, **letta da `primo_ordine/_mappa.yaml`**
*(che `P-MOD` tiene allineata al codice)*:

| il file del nucleo | funzioni NON dichiarate | rami | `default` |
|---|---|---|---|
| `flussi_parziali.py` | `0` | `0` | `0` |
| ### **`grafo.py`** | `2` | `6` | ### **`3`** |
| `hamiltoniana.py` | `0` | `0` | `0` |
| `incidenza.py` | `4` | `5` | `0` |
| `materia_vuoto.py` | `3` | `3` | `0` |
| `motore.py` | `4` | `9` | `0` |
| `passo.py` | `0` | `0` | `0` |
| `saturazione.py` | `1` | `1` | `0` |
| `stato.py` | `0` | `0` | `0` |
| ### **IN TUTTO** | ### **`14`** | ### **`24`** | ### **`3`** |

### ⚠ **E LA CHIUSURA SI LIMITA A `primo_ordine/`, dichiarato:** `motore.py` importa
`_presidio`, che vive in `csv/` ed e' **il timbro del blob**, non fisica. ### **Il
perimetro della fisica e' quello di `H-FISICA-FUORI-LISTA`**, e restringersi la' e'
**una regola, non un'eccezione per un file.**

### ⛔⛔ **PREMESSA DEL MANDATO CHE NON TORNA, `n.1`: I `default` NEL NUCLEO NON SONO ZERO**

Il mandato dice *«default nelle firme vietati (tetto zero, ### **gia' rispettato**)»*.
### **Non e' rispettato: `grafo.py` ne ha `3`**, tutti in una funzione:

```
def costo(n=9, archi=None, giri=2000):   # il COSTO del controllo, per il budget
```

> ### ⚠ **`grafo.costo` e' un MISURATORE dentro un modulo del nucleo**, e `grafo.py` entra
> nel nucleo perche' ### **`incidenza.py` lo importa.** ### **Il mandato non lo
> prevedeva** perche' il suo elenco informale *(`motore` `9`, `incidenza` `5`,
> `materia_vuoto` `3`, `percorri_tick` `3`, `energia` `1`, `saturazione` `1`)* ### **non
> conteneva `grafo.py`.**
> ### ✅ **COSA FARO', e non e' una scelta di fisica:** i tre `default` ### **diventano
> argomenti espliciti**, e `main` passa i valori *(che sono i parametri DELLA MISURA, e
> stanno dove sta la misura)*. ### **Nessun numero cambia**, e il ramo `if archi is None`
> ### **resta** con ruolo `default`.

### ⛔⛔ **PREMESSA CHE NON TORNA, `n.2`: `energia.py` NON E' NEL NUCLEO**

Il mandato lo elenca *(`energia.py` `1`)*, ma la chiusura ### **non lo contiene**: nessuna
radice lo importa — ### **lo importa `deriva.py`**, che e' uno strumento.
### ⚠ **Quindi il suo unico ramo NON si dichiara**, e lo dico invece di dichiararlo per
somiglianza con l'elenco.

### ⭐ **E LA COSA CHE IL NUCLEO DERIVATO FA GRATIS:** `crescita.py` e `vuoto.py`
### **non sono importati da NESSUNO** *(misurato)* — sono regole `NON-H` ### **non ancora
cablate nel passo.** ### **Oggi `P-R1` le guarda; col nucleo derivato no** — e
### **ci rientreranno DA SOLE il giorno in cui il passo le importera'.**
### 📌 **Lo stesso vale per `termini/*.py`**, i legami generati, che nessuno importa.
### ⚠ **Lo scrivo perche' la restrizione RINUNCIA a qualcosa:** quei file oggi hanno
### **tutti i rami dichiarati**, e domani non li avranno piu'.

### ⭐⭐ **`percorri_tick`: E' LOGICA DEL PASSO, E VIVE IN UNO STRUMENTO**

`deriva.percorri_tick` ### **percorre l'ordine di composizione**, cioe' **e' il passo**;
ma `deriva.py` e' ### **una misura**, e tirarlo nel nucleo ci porterebbe dentro
`energia`, `corrente`, `deriva_serie`, `deriva_variabile`, `incidenza`…
### ✅ **Il mandato dice di spostarlo**, e lo sposto in ### **un modulo suo,
`primo_ordine/tick.py`**, con `OPERATORE` *(la mappa `id` → operatore)* e `tick`.
### ⛔ **NON in `composizione.py`: quel file SI GENERA**, e scriverci a mano e' vietato.
### 📌 **E `tick.py` diventa UNA RADICE**, perche' e' ### **l'ingresso del passo della
camminata** — come `passo.py` lo e' per la via di `H`. ### ⚠ **La radice e'
DICHIARATA e PROVVISORIA**, come il mandato permette: quando la tabella avra' il campo
`modulo` *(pezzo `6`)*, i moduli delle leggi ### **si leggeranno da la'.**

### ⛔ **CHE COSA NON SO, e lo dico adesso**

| | non so… |
|---|---|
| `a` | se spostare `percorri_tick` ### **cambi un bit**: non dovrebbe *(nessuna operazione float si muove)*, ma ### **`M-B1` lo decide**, e se si muove e' ### **STOP** |
| `b` | se `saturazione.pezzi` *(il limite a `Lambda = 0`)* sia ### **fisica DICHIARATA**: il `docstring` la argomenta con `A11`, ma ### **la scheda della legge NON la nomina** *(verificato con un `grep`)* — e allora il ramo si dichiara col rimando al `docstring`, e ### **il buco della scheda lo RIFERISCO** |

---

## 2. PROGETTAZIONE — *i passi, i criteri, e cosa mi FERMA*

| | il passo | il criterio, e cosa mi FERMA |
|---|---|---|
| `1` | `primo_ordine/tick.py`: `OPERATORE`, `percorri_tick`, `tick`; i `5` chiamanti passano a `TK.*` | ### ⛔ **`M-B1` AL BIT** e il braccio `(c)` di `_collauda_deriva` *(il tick contro `DV.tick`, `0.0e+00`)* ### **invariati**: se si muove un bit, ### **STOP e relaziono** |
| `2` | il nucleo ### **DERIVATO** in `_rami_era2.py`, dalle radici ### **dichiarate** | la chiusura ### **si ricalcola a ogni corsa**: un import nuovo ### **allarga il nucleo da solo** |
| `3` | i ### **`24` + `3` rami** del nucleo dichiarati ### **uno per uno, col motivo** | un `perche'` sotto i `30` caratteri ### **fa fallire `P-R1`** da se' |
| `4` | i `3` `default` di `grafo.costo` ### **diventano espliciti** | ### **tetto `0`**, e `main` passa i valori della misura |
| `5` | `P-R1` ### **BLOCCANTE** nel `pre-commit`, e ### **fuori dal nucleo NON si applica** | il `pre-commit` resta ### **sotto i `500 s`** |
| `6` | i ### **tre casi che DEVONO fallire** + ### **uno che deve PASSARE**, su file finti ### **FUORI dal repo** | se il caso che deve passare fallisce, la regola ### **blocca fuori dal nucleo** e non va bene |
| `7` | la scheda in `doc/REGOLE`, `CLAUDE.md` ### **rigenerato**, la voce del presidio | — |

### ⛔⛔ **I RAMI CHE SONO FISICA, E CHE NON DECIDO**

| | dove | che cosa faro' |
|---|---|---|
| `a` | `materia_vuoto.N`, `.alpha`, `.beta` — `if np.any(vivi)` | ### **si dichiara col rimando alla scheda della legge**: la singolarita' eliminabile a `rho = 0` e' ### **fisica GIA' decisa** *(punto `5(a)` del mandato)* |
| `b` | `motore._somma_per_nodo` — `if self.sommatoria == "numpy"` | ### **si dichiara**, e ### ✅ **la scelta E' GIA' un argomento esplicito del motore** *(`Motore.__init__(self, inc, geo, st, dtau, sommatoria)`, ### **senza default** — verificato)*: il punto `5(b)` e' ### **soddisfatto, non da fare** |
| `c` | `corrente.instrada` — `np.abs(c) > tol` | ### **`corrente.py` e' FUORI dal nucleo** *(lo importa `deriva`)*, e per `A11` la domanda *«da che errore protegge quella soglia?»* ### **va nella RIPRESA come domanda aperta** — ### **non la decido** |
| `d` | `saturazione.pezzi` — `if np.any(buoni)` | il limite a `Lambda = 0`, argomentato nel `docstring` con `A11` ma ### **assente dalla scheda**: si dichiara col rimando al `docstring`, e ### **il buco si RIFERISCE** |

### ⚠ **E DUE COSE CHE NON FARO', perche' il mandato le vieta o non le chiede:**
### **non allargo il nucleo** per tenerci uno strumento *(punto `2`)*, e
### **non scrivo eccezioni file per file** *(punto `4`)*.

---

## 3. TODO

1. `primo_ordine/tick.py` + i `5` chiamanti + `_mappa.yaml` + `csv/_file_fisica.py`;
   poi ### **`M-B1` e il braccio `(c)`.**
2. `csv/_rami_era2.py`: il nucleo ### **derivato dalle radici dichiarate**, le `27` righe
   di `RAMI`, il tetto `0` sui `default`, e ### **fuori dal nucleo non si applica.**
3. `primo_ordine/grafo.py`: i `3` `default` ### **espliciti.**
4. i ### **tre casi che devono fallire** e ### **quello che deve passare**, fuori dal repo.
5. `doc/REGOLE/par12.md`, `CLAUDE.md` ### **rigenerato**, la voce di `[[P-R1]]`.
6. il referto, la RIPRESA *(con le ### **due domande aperte**: la soglia `tol` e la scheda
   della saturazione)*, la relazione.
