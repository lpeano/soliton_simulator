# IL RISCALDAMENTO DI FLOQUET SU UNA SCENA GRANDE — **previsione PRIMA dei numeri**

> **Mandato di Luca, 2026-10-13, punto `3`:** *«La deriva senza tendenza secolare (`M1a`) e'
> misurata su un ANELLO DI 16 NODI, dove un sistema piccolo puo' tornare su se stesso. Il
> riscaldamento tipico dei sistemi Floquet NON e' escluso. Ripeti `M1a` sulla scena del
> banco (`4m ~ 830`) o su una piu' grande, a `x ~ 1`, per `>= 4000` tick. **Previsione: se
> e' Floquet, una tendenza** (riscaldamento: popolazioni delle bande verso la parita',
> energia locale che sale). **Se resta senza tendenza anche li', dichiaralo.**»*

> ### ✅ **Questo file si committa PRIMA della misura.** ### ⛔ **E lo scrivo perche' oggi
> il rito l'ho GIA' violato una volta**, su `B2` e `B3`: non rifaccio lo stesso.

---

## 1. CHE SCENA USO, E PERCHE' NON UN ANELLO GRANDE

### ⛔ **Un anello di `208` nodi avrebbe la dimensione giusta** *(`4m = 832`)* **e sarebbe
la scelta sbagliata**, e la ragione e' precisa: ### **un trasporto casuale su un anello e'
un sistema `1D` DISORDINATO, e quelli LOCALIZZANO.** ### ⚠ **La localizzazione sopprime il
riscaldamento PER UNA RAGIONE CHE NON C'ENTRA CON FLOQUET**, quindi *«nessuna tendenza»* su
un anello ### **non distinguerebbe <<non si riscalda>> da <<e' localizzato>>.**

### ✅ **Uso un TORO `2D` `10x10`:** `n = 100`, `m = 200`, ### **`4m = 800`** — la
dimensione che il mandato chiede, **grado `4`**, e in due dimensioni la localizzazione da
disordine ### **e' molto piu' debole.**

### ⚠ **E DICHIARO IL LIMITE: NON E' LA SCENA DEL BANCO.** Il banco e' **congelato** e la
sua scena e' **irregolare**; il toro e' **regolare**. ### **La dimensione coincide, la
struttura no** — e se il riscaldamento dipendesse dall'irregolarita', questa misura **non lo
vedrebbe.**

---

## 2. ⭐ LE PREVISIONI, SCRITTE PRIMA DEI NUMERI

### ⚠ **E LA MIA NON COINCIDE CON QUELLA DEL MANDATO, quindi la dico chiaramente.**

| | la grandezza | la previsione del **mandato** | ### ⭐ **la MIA** |
|---|---|---|---|
| `F1` | la **tendenza** di `E(t)` su `4000` tick | ### **una tendenza** *(se e' Floquet)* | ### ⭐ **SI', una tendenza — e piu' netta che sull'anello.** Su `16` nodi il rapporto era `0.004`; qui mi aspetto **`> 1`** |
| `F2` | le **popolazioni delle bande** | verso la **parita'** *(`N+` e `N-` uguali)* | ### ⭐ **SI', verso la parita'** — e questo lo credo **piu' di `F1`** |
| `F3` | l'**energia locale** | **sale** | ### ⚠ **NON LO SO:** `E` non ha un segno privilegiato qui, e *«sale»* dipende da dove parte |

### ⭐ **PERCHE' MI ASPETTO `F2` PIU' DI `F1`, e il motivo e' un fatto GIA' MISURATO:**
`corr(Delta N+, Delta N-) = -1.0000` **esatto**, e `N+ + N-` **non puo' cambiare** *(la
norma e' conservata e il settore `0` e' vuoto)*. ### **Quindi `N+` e `N-` si muovono su un
segmento, e un mescolamento senza tendenza preferita li porta al CENTRO.**
### ⛔ **Il centro E' la parita'**, e la parita' e' **l'unico punto fisso** di un
mescolamento simmetrico: ### **l'equipartizione fra le bande e' l'<<infinita temperatura>>
di questo sistema.**

### ⚠ **E PERCHE' DUBITO DI `F1`:** `E` non e' una quantita' protetta **ne' limitata**, e su
`16` nodi oscillava di **`76`** su una scala di `6`. ### **Una tendenza dentro
un'oscillazione di quell'ampiezza va distinta dal rumore**, e con un seme solo
### **potrei vedere una tendenza che e' solo un pezzo di oscillazione lunga.**

### ⭐ **LE SOGLIE, FISSATE QUI**

| | il criterio | la soglia |
|---|---|---|
| la **tendenza** di `E` | `rapporto = (pendenza x durata) / ampiezza dei residui` | ### **`> 1` = tendenza**, `< 0.3` = nessuna. ### ⚠ **Fra `0.3` e `1` NON CONCLUDO** |
| la **parita'** delle bande | `|N+ - N-| / (N+ + N-)` all'inizio e alla fine | ### **scende di almeno un fattore `2`** = va alla parita' |
| la **materia** | `x = max|h_k|/Lambda_k` all'inizio | ### **`>= 0.5`**, altrimenti la saturazione e' spenta e la misura e' **vacua** |

### ⛔ **CHE COSA MI FAREBBE FERMARE**

1. se `x` venisse `< 0.5` sulla scena grande, ### **la misura e' vacua** e va rifatta col
   modulo del vuoto aggiustato — **non interpretata.**
2. se la tendenza cadesse **fra `0.3` e `1`**, ### **non concludo**: servono piu' tick o
   piu' semi, e con il budget di oggi ### **lo dichiaro come non deciso.**
3. se le popolazioni **si allontanassero** dalla parita', ### **non e' riscaldamento ed e'
   una cosa nuova**: la riporterei senza spiegarla.

---

## 3. TODO

1. il **toro `2D` `10x10`** nello strumento delle bande *(oggi costruisce solo anelli)*.
2. `4000` tick a `x ~ 1`, **salvando durante la corsa**.
3. il referto, e la dichiarazione **in ogni caso** — anche *«nessuna tendenza»*.

---

## 4. ⭐ L'ESITO — **`F2` vera, `F1` falsa, e un difetto MIO nel mezzo**

| | la previsione | l'esito | |
|---|---|---|---|
| `F1` *(mia e del mandato)* | una **tendenza** in `E` | rapporto **`0.0054`** *(casuale)*, **`0.0349`** *(preparato)*; la soglia era `> 1`, e `< 0.3` = nessuna | ### ⛔ **FALSA** |
| `F2` *(mia e del mandato)* | le popolazioni **verso la parita'** | lo squilibrio va `1.000 -> 0.336 -> 0.0658 -> 0.00835`, **un fattore `623`** fino al minimo | ### ✅ **VERA** |
| `F3` *(del mandato)* | l'energia locale **sale** | `E` **oscilla** fra `-107` e `+105` e non sale | ### ⛔ **no** — e avevo scritto *«non lo so»* |

### ⛔ **E `F2` E' VISIBILE SOLO DOPO AVER CORRETTO UN DIFETTO DELLA MIA MISURA, trovato
misurando.** Con lo stato **casuale** lo squilibrio va da `0.00195` a `0.0368`:
### **CRESCE**, e la prima lettura sarebbe stata *«si allontana dalla parita'»* — che era
la mia condizione di stop numero `3`.

### ⭐ **MA UN VETTORE CASUALE PARTE GIA' ALLA PARITA':** ha peso uguale nelle due meta'
dello spettro. ### ⚠ **Da li' non si puo' ANDARE VERSO la parita': si puo' solo andare
via** — cioe' ### **la misura non poteva vedere cio' che il mandato chiede di cercare.**
### ✅ **Corretta preparando lo stato in UNA banda** *(`P+ psi`, squilibrio `1`)*, e
allora si vede.

### ⭐⭐ **E LA CORREZIONE RICONCILIA LE DUE CORSE invece di scegliere fra due letture:**
il valore d'equilibrio dello squilibrio e' **`1/sqrt(4m) = 0.0354`** *(la fluttuazione di
taglia finita)*, contro una media misurata di **`0.0312`** sugli ultimi `20` campioni.
### ✅ **Quindi lo stato casuale NON si allontanava: era GIA' all'equilibrio, e
fluttuava.** ### **Le due corse dicono la stessa cosa.**

### ⭐ **E IL SETTORE `0` E' VUOTO ANCHE SUL TORO** *(`0` su `800`)*: ### **non era una
proprieta' dell'anello**, ed era uno dei <<cosa ricontrollare>> di `efc113b`.

### ⚠ **LA LETTURA, e la dico SEPARATA dai numeri perche' l'ho scritta DOPO:** il sistema
**termalizza nel grado di liberta' DELLE BANDE** *(l'equipartizione e' l'<<infinita
temperatura>> di quel grado)*, ### **ma `E` non cresce**, perche' `E` non e' limitata dal
basso e non ha un serbatoio verso cui salire: **oscilla.**

### ⛔ **E IL MANDATO DICEVA COSA FARE SE NON CI FOSSE TENDENZA: <<se resta senza tendenza
anche li', dichiaralo>>.** ### ✅ **Lo dichiaro: su un toro `2D` `10x10` (`4m = 800`), a
`x = 0.9055`, per `4000` tick, `E` NON MOSTRA UNA TENDENZA SECOLARE.**

### ⚠ **I LIMITI, e il terzo e' il piu' serio:** ① **non e' la scena del banco** *(il toro
e' regolare, il banco irregolare)*; ② **un seme solo**; ### ⛔ **③ `4000` tick NON
ESCLUDONO una tendenza su scale piu' lunghe: con un'ampiezza di `212` una deriva lenta
sarebbe SEPOLTA**; ④ i proiettori sono **spettrali**, quindi tutto cio' che e' <<per
banda>> e' **globale**.
