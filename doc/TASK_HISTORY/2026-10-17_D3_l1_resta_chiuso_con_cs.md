# `D3` — **`L1` RESTA CHIUSO CON `cs` DINAMICO**

> ### 📌 **Il punto `D3` del mandato unico del `2026-10-16`**, coi criteri
> ### **fissati nella tabella di `doc/TASK_HISTORY/2026-10-17_D_cs_lambda_nel_motore.md`
> ### PRIMA del codice**, e qui NON si cambiano:
> ### **`0` violatori del tempo proprio** · ### **`M-B2` pendenza `>= 1.9` su `>= 4`
> dimezzamenti** · ### **`W A W A^-1 = 1` a `<= 8` ulp su `>= 8` stati** ·
> ### **norme `M` e `V` conservate.**

> ### ⛔ **E QUESTO FILE SI COMMITTA PRIMA DEL LAVORO**, perche' l'ordine sia
> ### **verificabile da `git`** *(questo commit e' ANTENATO dei commit del codice)*
> ### **invece che asserito da me.**

---

## 0. LA STELLA POLARE — *rimanda, e dice PERCHE'*

### ⛔ **`D3` NON AGGIUNGE NESSUNA LEGGE E NON CAMBIA NESSUNA FORMA:** la legge e'
### **`cs` al centro del palindromo**, ed e' ### **quella di `D2`.** ### **Le cinque
risposte sono quelle di `D0`-`D2`**, nel task history di `D`, e ### **riscriverle qui
sarebbe una SECONDA copia che puo' divergere.**
### ✅ **Quello che `D3` fa e' UNA MISURA:** prende i ### **quattro criteri con cui
`L1` e' stato chiuso** e li rigira ### **con la forma ACCESA.**
### ⚠ **E se uno dei quattro cade, `L1` NON e' chiuso con `cs`** -- ed e'
### **un risultato da relazionare, non da aggiustare.**

---

## 1. RAGIONAMENTO PRELIMINARE — *cosa credo, e cosa NON so*

### 📌 **I TRE FATTI CHE HO LETTO PRIMA DI PROGETTARE** *(e sono misure di OGGI,
a forma SPENTA, non risultati di `D3`)*:

| | il fatto, a forma SPENTA | da dove |
|---|---|---|
| `1` | ### **`0` violatori su `12` pezzi** del tempo proprio | `_collauda_tempo_proprio.py`, `4` su `4` |
| `2` | ### **`M-B2` pendenza `1.965` su `5` dimezzamenti**, e la controprova *(ordine vecchio)* da' `0.837` | `_misura_mb2.py` |
| `3` | la simmetria e' ### **`<= 8` ulp su `8` semi** *(`SEMI` e `ULP_SIMMETRIA = 8.0`)* | `_misura_completa_l2.py` |

### ✅ **Quindi i quattro criteri di `D3` sono SODDISFATTI OGGI a forma spenta:**
### **la domanda e' SOLO se la forma accesa li rompe**, e questo e' il modo giusto di
porla *(se fossero rotti anche a forma spenta, `D3` non misurerebbe `cs`)*.

### ⭐ **CHE COSA CREDO, PRIMA DI GUARDARE**

### `1)` **Il tempo proprio: credo che REGGA**, e il motivo e' che `cs` ### **MOLTIPLICA**
`dtau` *(`dtau_nodo` restituisce `dtau * cs`)*: un pezzo che dipendeva da `dtau`
### **dipende ancora da `dtau`**, perche' `cs` non e' zero -- e ### **`cs = 0` e' vietato
alla costruzione** *(decisione di Luca del `2026-10-17`)*.
### ⚠ **MA NON LO SO:** se un pezzo usasse `cs` in modo da cancellare la dipendenza,
il censimento lo direbbe. ### **E' esattamente perche' non lo so che si misura.**

### `2)` **`M-B2` con `cs`: credo che la pendenza resti `~2`**, perche' `D2` ha
### **GIA' misurato** che la valutazione al centro conserva il secondo ordine
*(`2.001` contro `0.997` della variante ingenua)*.
### ⚠ **MA `D2` lo ha misurato su UNA SUA pendenza** *(l'errore fra un passo e due
mezzi passi)*, ### **NON su `H_tot` di `M-B2`** -- e sono ### **due numeri diversi.**
### ⛔ **Quindi questo braccio puo' DAVVERO fallire**, e non e' un passaggio a vuoto.

### `3)` **La simmetria su `8` stati: credo che REGGA**, perche' la ho ### **appena
misurata su UNO stato e tre `dtau`** *(`2`-`6` ulp)*. ### ⚠ **Ma `8` stati includono
### **configurazioni di nodi vuoti diverse** *(`VUOTI_PER_SEME`)*, e la banda la' e'
### **`8` ulp, non `4096`** -- cioe' ### **`512` volte piu' stretta.**
### ⛔ **E QUESTO E' IL BRACCIO CHE MI ASPETTO PIU' FRAGILE**, per un motivo preciso:
il punto fisso di `cs` si ferma ### **agli ulp** *(`EPS_CS = 8 eps`)*, quindi
### **introduce un errore DI ARROTONDAMENTO che la forma spenta non ha.** ### **Se
sfonda gli `8` ulp, il numero si riporta e NON si allarga la banda.**

### `4)` **Le norme: credo che si conservino ESATTAMENTE**, e questa e' la piu' solida:
`cs` ### **non aggiunge un termine** -- scala il tempo proprio dentro pezzi che sono
### **unitari per costruzione.** ### ⚠ **E se NON si conservassero sarebbe un difetto
GRAVE**, perche' vorrebbe dire che `cs` entra ### **dove non deve.**

### ⛔⛔ **CIO' CHE NON SO, e lo scrivo adesso:**
### `a)` ### **con che `Lambda_c` si misura.** Non e' una manopola: si prende
### **la MEDIA di `Lambda` sulla scena** *(rapporto `1`)*, com'e' stato fatto per la
`PTheta`. ### **Un rapporto diverso darebbe numeri diversi, e questo va DETTO.**
### `b)` ### **se il costo e' sostenibile:** il punto fisso costa fino a
### **`74` giri** *(misurato)*, e `M-B2` gira ### **fino a `512` tick**. ### **Potrebbe
voler dire minuti**, e se sfonda il budget ### **lo si dice invece di tagliare i
dimezzamenti in silenzio.**
### `c)` ### **se gli strumenti esistenti si possono riusare**: `_misura_mb2._tick_ordine`
e `_misura_theta_nonlineare.passo` ### **percorrono il tick DA SOLI**, cioe' NON passano
da `tick.tick`. ### **Quindi accendere `cs` sul motore NON basta a farli misurare con
`cs`** -- e questo e' un fatto, non un'opinione: l'ho letto.

---

## 2. PROGETTAZIONE — *i passi, cosa decide ciascuno, e cosa mi FERMA*

### ⛔ **UN FILE NUOVO, `_collauda_cs_l1.py`**, e ### **nessuna copia delle leggi**:
`h_tot` si ### **importa** da `_misura_mb2`, la simmetria usa ### **`passo_cs` di
`_misura_theta_nonlineare`** *(che ho scritto per la `PTheta`)*, i semi e la banda si
### **importano** da `_misura_completa_l2`. ### ✅ **Un criterio che vive in due posti
diverge**, ed e' la regola `STRUMENTO-LEGGE-DALLA-TABELLA` applicata ai CRITERI.

| | il passo | cosa DECIDE | cosa mi FERMA |
|---|---|---|---|
| `1` | il censimento del tempo proprio ### **con `cs` acceso** | se `cs` cancella la dipendenza da `dtau` di qualche pezzo | ### **un solo violatore**: si riporta QUALE pezzo e con che numero, e si ferma |
| `2` | `M-B2` ### **con `cs` al centro**, `>= 4` dimezzamenti | se la forma conserva il secondo ordine ### **su `H_tot`** | pendenza ### **`< 1.9`**: si riporta la scala dei rapporti e ### **non si tocca la banda** |
| `3` | la simmetria su ### **`>= 8` stati**, banda `8` ulp | se la forma regge la banda STRETTA | ### **`> 8` ulp**: si riporta il peggio e il seme, e ### **la banda resta `8`** |
| `4` | le norme `M` e `V` su una corsa | se `cs` entra dove non deve | ### **qualunque deriva oltre gli ulp**: e' un difetto, non un numero |
| `5` | ### **il caso che DEVE fallire**, per OGNI braccio | che i quattro bracci ### **possano** dire no | ### **un braccio che non fallisce col caso finto e' un FALSO-UNO**, e si ferma |

### ⭐ **E IL BRACCIO `0`, PRIMA DI TUTTI:** a forma ### **SPENTA** questo file deve
dare ### **gli stessi numeri degli strumenti originali, AL BIT dove sono al bit.**
### ⚠ **Senza di lui, un numero diverso non si saprebbe attribuire a `cs` o a una mia
riscrittura.**

### ⛔ **IL CASO CHE DEVE FALLIRE, e viene da `D2`:** ### **`cs` a INIZIO PASSO.**
`D2` ha misurato che perde il secondo ordine *(`0.997`)* e la `PTheta` *(`3e14` ulp)*:
### **qui deve far cadere il braccio `2` e il braccio `3`.**
### ✅ **E per il braccio `1` il caso finto c'e' gia':** un pezzo
### **reso indipendente da `dtau`** *(il `2-septies` lo usa)*.

---

## 3. TODO DEL NEXT STEP

1. `_collauda_cs_l1.py`: il braccio `0` *(forma spenta = strumenti originali)*, poi i
   quattro bracci accesi, poi i casi che DEVONO fallire.
2. ### **Misurare il COSTO** della suite con `D3` dentro: se il `pre-commit` sfonda i
   `500` s, `D3` va in ### **`solo-CI`** -- e il numero si scrive.
3. Il referto ### **dal blob committato**, la `RIPRESA`, la relazione.
4. ### ⛔ **Se un criterio cade: si committa la misura, si spiega, e SI FERMA.**
   ### **Non si aggiusta un parametro per farlo passare.**