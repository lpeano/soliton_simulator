# `3` — **LA REGOLA `STRUMENTO-LEGGE-DALLA-TABELLA`, E IL SUO PRESIDIO**

*(decisione di Luca del `2026-10-16` alle `13:25`, registrata per intero in
`doc/CODA_2026-10-16.md`. Base: `627d434b`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE**, e il commit del task history
> dev'essere **ANTENATO** dei commit del lavoro: cosi' l'ordine e' **verificabile da
> `git`** invece che asserito da me *(`CLAUDE.md` §8)*.

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo PRIMA di guardare, e cosa NON so*

### ⭐⭐ **LA REGOLA NASCE DA UN CONTO, E IL CONTO E' MIO**

In un giorno sono emersi ### **SETTE** strumenti con la legge vecchia scritta dentro —
`h_tot` di `M-B2`, `ordine_lineare` di `_misura_theta_n`, la sostituzione **per nome** di
`_misura_statica_l2`, il **`7`** delle guardie di `P-R1`, `deriva.satura`,
`deriva.sorgente_per_nodo` e il braccio `(3)` di `_collauda_deriva`.
### ⛔ **Il motore si e' aggiornato perche' LEGGE DALLA TABELLA; le copie no, e nessuno le
obbligava.**

> ### ⚠ **IL MANDATO DICE <<CINQUE>>, E OGGI SONO SETTE:** i due in piu' li ho trovati io
> dopo, nel `2-quater`. ### **Lo scrivo perche' il numero del mandato NON si corregge in
> silenzio.**

### ⭐ **CHE COSA CREDO, PRIMA DI SCRIVERE L'ANALIZZATORE**

| | credo che… | e ### **NON LO SO**, lo dico adesso |
|---|---|---|
| `a` | gli `id` fuori dall'ordine ### **si possono DERIVARE**: sono quelli in `leggi.yaml` che non stanno in `CM.ORDINE` | ### ⚠ **non so se `leggi.yaml` dichiari il MODULO di una legge:** se non lo dichiara, *«l'import del modulo di una legge superata»* ### **non e' derivabile** e serve una mappa — che sarebbe ### **un pezzo di legge nello strumento**, cioe' la malattia che sto curando |
| `b` | le occorrenze ### **legittime** sono poche e ### **concentrate**: il motore *(che registra tutti gli operatori)*, il modulo della legge, il suo legame generato, il suo collaudo | ### ⚠ **non so quante saranno**: se fossero decine, la *«lista di eccezioni dichiarate»* diventerebbe ### **un secondo posto dove la legge e' scritta a mano** |
| `c` | *«un intero letterale confrontato con un conto»* ### **non e' decidibile dall'AST in generale** | ### ⛔ **lo dico PRIMA di misurare:** quello che si puo' fare e' ### **una regola NOMINATA** *(un confronto con un letterale dove l'altro lato nomina la tabella)*, e ### **il suo limite va DICHIARATO**, non nascosto |
| `d` | i ### **docstring** vanno ESCLUSI, i ### **commenti** sono invisibili all'AST | ### ⚠ **e questo e' un BUCO della regola, non una scelta:** un `id` in un commento ### **passa**, ed e' per quello che esiste `P-RIF` |

### ⛔⛔ **E UNA COSA CHE NON FARO', perche' l'ho vista rompersi DUE VOLTE**

Due collaudi di presidio, per provare i casi che devono fallire, ### **scrivono nel repo e
poi ripristinano i byte** — e ### **due volte il ripristino e' fallito** con
`OSError: [Errno 22]`, lasciando l'albero sporco *(una volta `CLAUDE.md` con `L-PATCH`
rinominato `ZL-PATCH`, una volta `leggi.yaml` con una legge finta e due file generati)*.

> ### ✅ **QUINDI L'ANALIZZATORE PRENDE LE RADICI COME ARGOMENTO.** Il presidio vero gli
> passa il repo; il collaudo gli passa ### **una cartella temporanea FUORI dal repo**, coi
> cinque file finti. ### **Nessun file del repo viene toccato da nessun braccio**, e la
> fragilita' che ho riferito ### **non si puo' piu' presentare qui.**

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, cosa decide ciascuno, cosa mi FERMA*

### ⭐ **IL DISEGNO: UNA FUNZIONE PURA, E DUE CHIAMANTI**

```
_analizza(radici, fuori_ordine, parole_tabella, eccezioni) -> (reperti, orfane)
        |                                                        |
        |-- il PRESIDIO vero: radici = il repo                   |-- il COLLAUDO:
        |   fuori_ordine = DERIVATO da leggi.yaml e ORDINE       |   radici = una cartella
        |   eccezioni    = la lista dichiarata                   |   TEMPORANEA, fuori dal repo
```

### **I QUATTRO REPERTI CHE CERCA, e come**

| | che cosa | come, ### **con l'AST** | il criterio |
|---|---|---|---|
| `1` | un `id` di legge ### **fuori dall'ordine** | ogni `Constant` di tipo `str`, ### **piu' le concatenazioni** `"CAMM-" + "SATURAZIONE"` e le `f-string` a pezzi costanti, ### **ripiegate** prima del confronto | il valore ripiegato ### **e'** uno degli `id` fuori dall'ordine |
| `2` | l'### **import** del modulo di una legge fuori dall'ordine | `Import` / `ImportFrom` | il nome del modulo ### **sta nella mappa legge→modulo**, ### ⛔ **che va DERIVATA o DICHIARATA — e se va dichiarata, lo scrivo** |
| `3` | un ### **intero letterale** confrontato con un conto | `Compare` dove ### **un lato e' un letterale `int >= 2`** e l'altro ### **nomina la tabella** *(`ORDINE`, `LEGGI`, `FLUSSI`, `OPERATORI`, `legami`, `guardie`, `termini`)* | e' ### **una regola NOMINATA**, e il limite si dichiara |
| `4` | un'eccezione ### **ORFANA** | il confronto fra la lista e i reperti | un'eccezione che ### **non corrisponde a nessun reperto** ### **fa fallire** |

### **LA SECONDA FONTE, e come si riconosce**

Un modulo la dichiara con ### **un dizionario a livello di modulo**,
`SECONDA_FONTE = {"<funzione>": "<motivo>"}`. Il presidio pretende, ### **dentro quella
funzione**, ### **almeno un `assert` o un `raise`** — cioe' ### **il confronto che ALZA** —
e che il modulo ### **importi il modulo della legge che gira.**

> ### ⚠ **E QUESTO E' UN CONTROLLO NECESSARIO, NON UNA PROVA:** un `assert` dentro la
> funzione ### **non dimostra** che confronta la cosa giusta. ### **Lo dichiaro come
> limite** invece di far credere che il presidio capisca la fisica.

### **I CINQUE CASI CHE DEVONO FALLIRE** *(ciascuno un file nella cartella temporanea)*

### ① un `id` fuori dall'ordine ### **scritto a mano**; ### ② lo stesso `id` ### **per
concatenazione di stringhe** *(«una forma equivalente non deve evadere come lo spazio con
`P-ES1`»)*; ### ③ un ### **conto letterale** confrontato con la tabella; ### ④ una
### **seconda fonte SENZA il confronto**; ### ⑤ un'### **eccezione ORFANA.**

### **I CRITERI, FISSATI QUI**

| | il criterio | cosa mi FERMA |
|---|---|---|
| `1` | i cinque casi ### **falliscono tutti e cinque**, ciascuno ### **per la sua chiave** e non per un'altra | se uno passa, il braccio e' ### **vacuo** e lo dico |
| `2` | ### **il controllo che POTREBBE fallire:** la stessa cartella temporanea ### **ripulita** non da' nessun reperto | se da' reperti, l'analizzatore ### **vede fantasmi** |
| `3` | sul repo di oggi: ### **ogni reperto e' o CURATO o in ECCEZIONE DICHIARATA**, e ### **zero orfane** | ### ⛔ **se una cura richiede una scelta di FISICA, NON la prendo:** la scrivo come domanda per Luca e la committo |
| `4` | il `pre-commit` resta ### **sotto i `500 s`** | il presidio nuovo ### **misurato col suo tempo**, e se sfonda il budget e' ### **un segnale, non un rifiuto** |
| `5` | ### **nessun file del repo scritto da nessun braccio** | l'albero ### **pulito** dopo il collaudo: `git status` e' il controllo |

### ⛔⛔ **E LA REGOLA D'ORO: QUESTO COMMIT NON CURA NIENTE DELLA FISICA.** Il presidio
### **nasce NON BLOCCANTE se trova piu' di cio' che la lista copre**, e le cure stanno
### **in coda** *(`2-quinquies`, `2-sexies`, `2-septies`)* — ### **un interruttore alla
volta.**

---

## 3. TODO DEL NEXT STEP

1. **la voce della REGOLA** — `STRUMENTO-LEGGE-DALLA-TABELLA`, `classe: STANDARD`,
   `dominio: METODO`, con `meta.in_claude` e `meta.dettaglio_regola: par11.md`:
   ### **`CLAUDE.md` §11 SI GENERA**, e a mano sarebbe ### **rifiutato** *(`P-REG`)*.
2. **la voce del PRESIDIO** — `P-TAB`, `classe: PRESIDIO`, con
   `meta.dettaglio_regola: par12.md`; e il ### **dettaglio** in `doc/REGOLE/par11.md` e
   `par12.md` *(`csv/_struttura_regole.py` pretende che nessuna regola si perda)*.
3. **`csv/_strumento_dalla_tabella.py`** — `_analizza(...)` pura, il presidio, i
   ### **cinque casi che devono fallire** in una cartella ### **temporanea fuori dal
   repo**, e il controllo che ### **potrebbe** fallire.
4. **la lista delle ECCEZIONI DICHIARATE**, una riga per file e simbolo, ### **col
   motivo** — e l'orfana che ### **fa fallire.**
5. **`primo_ordine/collauda.py`** — il presidio nella lista, ### **coi tempi**; e
   `.githooks/pre-commit` se la lista non si legge da la'.
6. **il referto** `doc/REFERTO_strumento_dalla_tabella.txt` ### **dal blob committato**,
   la tabella file/simbolo/esito ### **nella relazione**, la RIPRESA.
7. ### ⛔ **e se un reperto chiede una scelta di fisica: una DOMANDA PER LUCA**, non una
   cura mia.
