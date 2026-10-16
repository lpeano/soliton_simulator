# `4` — **`P-R1` ESTESO A TUTTI I FILE DI FISICA: IL CENSIMENTO** *(piu' l'aggiunta `C`)*

*(decisione di Luca del `2026-10-16` alle `09:21`, registrata in `doc/CODA_2026-10-16.md`.
Base: `19c2bda4`.)*

> ### ⛔ **QUESTO FILE SI COMMITTA PRIMA DEL CODICE** *(`CLAUDE.md` §8)*, e
> ### **NIENTE SI BLOCCA in questo pezzo:** il mandato dice *«non dichiarare i rami, non
> cambiare la lista del presidio vero, non toccare il codice di fisica — alcuni rami
> potrebbero essere scelte di fisica nascoste, e quelle le decide Luca»*.

---

## 1. RAGIONAMENTO PRELIMINARE — *il buco, e che cosa credo di trovare*

### ⛔⛔ **IL BUCO, E L'HO TROVATO IO** *(segnalato il `16` ottobre, scritto in `9fbcddf`)*

`P-R1` sorveglia i rami della fisica, ### **ma guarda una lista HARDCODED dentro
`csv/_rami_era2.py`:**

```
stato.py · hamiltoniana.py · passo.py · crescita.py · vuoto.py · termini/*.py
```

> ### ⛔ **E NON GUARDA `motore.py`, `energia.py`, `flussi_parziali.py`,
> `saturazione.py` ne' `materia_vuoto.py`** — cioe' ### **proprio dove sta la maggior
> parte della fisica.**
> ### ⚠ **Il motivo per cui conta:** il rapporto fra codice e indice dev'essere
> ### **INFALLIBILE**, e un presidio che guarda ### **cinque file su ottanta** da'
> ### **la sensazione di coprire la fisica** senza coprirla.

### ⭐ **E LA LISTA SI PUO' DERIVARE, perche' un hook la tiene allineata**

`H-FISICA-FUORI-LISTA` pretende che ### **ogni `.py` sotto `primo_ordine/` stia nella
LISTA** di `csv/_file_fisica.py`. ### ✅ **Quindi derivare dal disco e' sicuro E
sufficiente**, e ### **un file nuovo entra da solo** — che e' quello che il mandato chiede.
### 📌 **E lo verifico come controllo positivo**, invece di fidarmi: ### **il derivato
dev'essere contenuto nel dichiarato**, e se non lo e' ### **e' `H-FISICA-FUORI-LISTA` a
essere rotto**, e lo dico.

### ⭐ **CHE COSA CREDO DI TROVARE, scritto PRIMA di guardare**

| | credo che… | perche' |
|---|---|---|
| `a` | i rami non dichiarati saranno ### **molti**, ordine ### **centinaia** | la lista copre `5` file piu' i generati; i file veri sono ### **`80`**, e `motore.py` da solo ha `~700` righe |
| `b` | la maggior parte sara' in ### **collaudi e misure**, non in moduli di fisica | sono gli `_collauda_*` e `_misura_*`, pieni di `if` di diagnosi |
| `c` | ### **i default nelle firme saranno tantissimi** fuori dalla lista | `scena(...)`, `corri(...)` e i loro simili sono ### **pieni di default**, e il punto `15(b)` li vieta ### **solo nei file della lista** |
| `d` | fra i rami ci sara' ### **almeno una scelta di fisica nascosta** | e' il motivo per cui Luca ha detto ### **di non dichiararli io** |

### ⚠ **E SE `(c)` E' VERO, E' LA COSA PIU' IMPORTANTE DEL CENSIMENTO:** un `default` in una
firma e' ### **un valore che gira senza che nessuno l'abbia scelto**, ed e' `CONFIG-1` —
### **`28` leggi su `31` che giravano SPENTE.** ### **Estendere `P-R1` a tutti i file
significherebbe vietarli la' dove oggi sono la norma**, e quella ### **e' una decisione
grossa, non un allargamento di lista.**

### ⭐⭐ **L'AGGIUNTA `C`: IL BUCO DI `P-ES1`, E SI MISURA**

`P-ES1` cerca ### **la stringa LETTERALE `-1j`** *(`FORMA_PASSO in seg`)*, quindi
### **`- 1j` con lo spazio LO EVADE.** ### ⚠ **Misurato per caso:** la prima stesura
dell'Eulero di `_collauda_materia_vuoto.py`, scritta con lo spazio, ### **non veniva
vista** — il presidio si lamentava dell'### **eccezione ORFANA**, non del passo nascosto.

> ### ✅ **COME SI MISURA IL BUCO:** un rivelatore ### **sull'AST** che trova
> ### **l'unita' immaginaria col segno meno** *(`-1j` come costante, `UnaryOp(-, 1j)`, o un
> prodotto che vi si ripiega)* in una funzione che nomina `dt`, e ### **si confronta con
> cio' che la ricerca LETTERALE trova.** ### **La differenza E' il buco, in numero.**
> ### ⛔ **E NON LO CHIUDO:** *«la decisione su come chiuderlo e' di Luca»* — e `P-ES1` ha
> ### **eccezioni dichiarate** che un rivelatore nuovo potrebbe invalidare.

---

## 2. PROGETTAZIONE DEL RAGIONAMENTO — *i passi, e cosa mi FERMA*

### ⭐ **IL DISEGNO: IL CENSIMENTO NON RISCRIVE LA LOGICA, LA IMPORTA**

```
csv/_censimento_rami.py
    importa  _rami_era2._conta  e  _rami_era2.default_nelle_firme   <-- LA LOGICA VERA
    importa  _un_solo_esecutore.fase_a_mano (la ricerca LETTERALE)  <-- per il confronto
    la lista dei file:  DERIVATA dal disco, e CONFRONTATA col dichiarato
```

### ⛔⛔ **PERCHE' IMPORTA INVECE DI RISCRIVERE:** e' la regola
`[[STRUMENTO-LEGGE-DALLA-TABELLA]]` applicata ### **a un presidio**. ### **Un censimento
che riscrivesse `_conta` misurerebbe la SUA idea di ramo**, non quella di `P-R1` — e il
numero non sarebbe confrontabile con niente.

| | il passo | il criterio, e cosa mi FERMA |
|---|---|---|
| `1` | la lista ### **derivata** dal disco, e ### **contenuta** nel dichiarato | se non lo e', ### **`H-FISICA-FUORI-LISTA` e' rotto** e lo dico invece di proseguire |
| `2` | `P-R1` girato ### **IN SOLA LETTURA** su tutti i file | ### ⛔ **nessun file del repo si scrive**, e il controllo e' `git status` |
| `3` | la tabella: ### **file · rami non dichiarati · ruoli · default nelle firme** | — |
| `4` | il caso che DEVE fallire: un ramo non dichiarato in un file ### **oggi escluso** deve ### **COMPARIRE** | il file finto sta in una cartella ### **TEMPORANEA fuori dal repo** |
| `5` | l'aggiunta `C`: il buco di `P-ES1` ### **in numero** | il rivelatore AST ### **deve trovare** `- 1j` con lo spazio, e la ricerca letterale ### **NON deve trovarlo** — se li trovassero entrambi, ### **il buco non esiste** e lo dico |
| `6` | il referto in `doc/`, dal blob ### **committato** | — |

### ⛔ **E QUESTO PEZZO FINISCE CON LO STOP DI LUCA, dichiarato nel mandato:**
*«dopo il punto `3` ti fermi. Con la tabella in mano Luca decide ### **quali rami sono
tecnici e si dichiarano, quali sono fisica da guardare, e quando il presidio diventa
bloccante**»*.

---

## 3. TODO

1. **`csv/_censimento_rami.py`** — la lista derivata, `P-R1` in sola lettura, la tabella,
   il caso che deve fallire ### **fuori dal repo**, e il buco di `P-ES1` ### **misurato.**
2. **il referto** `doc/REFERTO_censimento_rami.txt`, dal blob ### **committato.**
3. **la voce di `[[P-R1]]`** aggiornata col censimento, e quella di `[[P-ES1]]` col
   ### **numero** del buco.
4. **la RIPRESA** e la **relazione**, con la tabella.
5. ### ⛔ **NIENTE ALTRO**, e poi ### **STOP.**
